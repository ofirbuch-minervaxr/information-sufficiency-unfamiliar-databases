"""Build the pilot dataset from database specs by controlled removal (label known by construction).

Usage:  python -I build_dataset.py --specs specs --out data/pilot.jsonl --test-dbs db_a,db_b [--seed 7]

Per answerable question (variant -> label):
  full          nothing removed                                   -> ANSWERABLE
  drop_col      a needed column deleted (doc and rows too)        -> NOT_ANSWERABLE / NOT_PRESENT
  drop_doc      the doc of a needed column blanked (if the question needs a doc) -> NOT_ANSWERABLE / UNDERSPECIFIED
  control_doc / control_col  something the question does NOT need removed -> ANSWERABLE (control)
Per ambiguous question:
  ambiguous     both readings supported, nothing resolves it      -> AMBIGUOUS
  resolved      the resolving note added to the table description -> ANSWERABLE
Every variant also gets ~15% of the docs of unneeded columns blanked at random, so "a doc is missing" is not a cue by itself.
"""
import argparse
import collections
import glob
import json
import os
import random

NOISE_P = 0.15


def render(spec, drop_cols=frozenset(), blank_docs=frozenset(), notes=None):
    notes = notes or {}
    lines = [f"Database: {spec['db_id']} ({spec['domain']})"]
    samples = []
    for t in spec["tables"]:
        keep = [i for i, c in enumerate(t["columns"]) if f"{t['name']}.{c['name']}" not in drop_cols]
        desc = " ".join([t["description"]] + notes.get(t["name"], []))
        lines.append(f"Table {t['name']}: {desc}")
        for i in keep:
            c = t["columns"][i]
            r = f"{t['name']}.{c['name']}"
            doc = "" if r in blank_docs else c.get("doc", "")
            pk = " (primary key)" if c.get("pk") else ""
            lines.append(f"  - {c['name']} {c['type']}{pk}" + (f": {doc}" if doc else ""))
        names = ", ".join(t["columns"][i]["name"] for i in keep)
        rows = "; ".join(str(tuple(row[i] for i in keep)) for row in t["rows"][:3])
        samples.append(f"{t['name']}({names}): {rows}")
    fks = [f"{a} -> {b}" for a, b in spec.get("foreign_keys", []) if a not in drop_cols and b not in drop_cols]
    if fks:
        lines.append("Foreign keys: " + ", ".join(fks))
    lines.append("Sample rows (first 3 per table):")
    lines += ["  " + s for s in samples]
    return "\n".join(lines)


def build(spec, split, rng):
    all_cols = [f"{t['name']}.{c['name']}" for t in spec["tables"] for c in t["columns"]]
    doc_cols = [f"{t['name']}.{c['name']}" for t in spec["tables"] for c in t["columns"] if c.get("doc")]
    fk_cols = {x for pair in spec.get("foreign_keys", []) for x in pair}
    pk_cols = {f"{t['name']}.{c['name']}" for t in spec["tables"] for c in t["columns"] if c.get("pk")}
    out = []

    def noise(protected, dropped=()):
        return {r for r in doc_cols if r not in protected and r not in dropped and rng.random() < NOISE_P}

    def rec(base, text, ctx, label, reason, missing, variant):
        out.append({"id": f"{spec['db_id']}:{base}:{variant}", "db_id": spec["db_id"], "split": split,
                    "base_id": f"{spec['db_id']}:{base}", "question": text, "context": ctx, "label": label,
                    "reason": reason, "missing_refs": missing, "variant": variant})

    for q in spec["questions"]:
        prot = set(q["needs_columns"]) | {d["column"] for d in q.get("needs_docs", [])}
        rec(q["id"], q["text"], render(spec, blank_docs=noise(prot)), "ANSWERABLE", None, [], "full")
        victim = rng.choice(q["needs_columns"])
        rec(q["id"], q["text"], render(spec, drop_cols={victim}, blank_docs=noise(prot, {victim})),
            "NOT_ANSWERABLE", "NOT_PRESENT", [victim], "drop_col")
        if q.get("needs_docs"):
            d = rng.choice(q["needs_docs"])
            blank = noise(prot) | {d["column"]}
            rec(q["id"], q["text"], render(spec, blank_docs=blank), "NOT_ANSWERABLE", "UNDERSPECIFIED",
                ["doc:" + d["column"]], "drop_doc")
        irr_cols = [c for c in all_cols if c not in prot and c not in pk_cols and c not in fk_cols]
        irr_docs = [c for c in doc_cols if c not in prot]
        if irr_cols and (rng.random() < 0.5 or not irr_docs):
            v = rng.choice(irr_cols)
            rec(q["id"], q["text"], render(spec, drop_cols={v}, blank_docs=noise(prot, {v})),
                "ANSWERABLE", None, [], "control_col")
        elif irr_docs:
            v = rng.choice(irr_docs)
            rec(q["id"], q["text"], render(spec, blank_docs=noise(prot) | {v}), "ANSWERABLE", None, [], "control_doc")

    for a in spec.get("ambiguous", []):
        prot = set(a.get("needs_columns", []))
        glosses = ["reading: " + r["gloss"] for r in a["readings"]]
        rec(a["id"], a["text"], render(spec, blank_docs=noise(prot)), "AMBIGUOUS", None, glosses, "ambiguous")
        rn = a["resolving_note"]
        rec(a["id"], a["text"], render(spec, blank_docs=noise(prot), notes={rn["table"]: [rn["text"]]}),
            "ANSWERABLE", None, [], "resolved")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--specs", default="specs")
    ap.add_argument("--out", default="data/pilot.jsonl")
    ap.add_argument("--test-dbs", default="")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    test_dbs = {x for x in args.test_dbs.split(",") if x}
    rows = []
    for path in sorted(glob.glob(os.path.join(args.specs, "*.json"))):
        with open(path, encoding="utf-8") as f:
            spec = json.load(f)
        rng = random.Random(f"{args.seed}:{spec['db_id']}")  # per-database seed: adding a database never changes the others
        rows += build(spec, "test" if spec["db_id"] in test_dbs else "train", rng)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    key = lambda r: r["label"] if not r["reason"] else r["reason"]  # noqa: E731
    tab = collections.Counter((r["split"], key(r)) for r in rows)
    print(f"{len(rows)} examples from {len({r['db_id'] for r in rows})} databases -> {args.out}")
    for split in ("train", "test"):
        print(f"  {split}: " + ", ".join(f"{k}={tab[(split, k)]}" for k in ("ANSWERABLE", "AMBIGUOUS", "UNDERSPECIFIED", "NOT_PRESENT")))


if __name__ == "__main__":
    main()
