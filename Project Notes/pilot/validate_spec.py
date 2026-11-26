"""Validate a pilot database spec (format and rules in README.md).

Usage:  python -I validate_spec.py spec.json [--relaxed]
Exit code 1 when there are errors. Warnings are advice. --relaxed skips the size requirements (for the example).
"""
import json
import re
import sqlite3
import sys


def validate(spec, relaxed=False):
    errs, warns = [], []
    cols = {}
    for t in spec["tables"]:
        names = [c["name"] for c in t["columns"]]
        if len(set(names)) != len(names):
            errs.append(f"{t['name']}: duplicate column names")
        for r in t["rows"]:
            if len(r) != len(names):
                errs.append(f"{t['name']}: row has {len(r)} values for {len(names)} columns: {r}")
        if not relaxed and not 8 <= len(t["rows"]) <= 14:
            errs.append(f"{t['name']}: {len(t['rows'])} rows (need 8-12)")
        for c in t["columns"]:
            cols[f"{t['name']}.{c['name']}"] = c
    if errs:
        return errs, warns

    con = sqlite3.connect(":memory:")
    for t in spec["tables"]:
        ddl = ", ".join(f'"{c["name"]}" {c["type"]}' for c in t["columns"])
        con.execute(f'CREATE TABLE "{t["name"]}" ({ddl})')
        con.executemany(f'INSERT INTO "{t["name"]}" VALUES ({",".join("?" * len(t["columns"]))})', t["rows"])
    for a, b in spec.get("foreign_keys", []):
        if a not in cols or b not in cols:
            errs.append(f"foreign key refers to an unknown column: {a} -> {b}")

    def run(sql):
        try:
            return con.execute(sql).fetchall(), None
        except Exception as e:  # noqa: BLE001
            return None, str(e)

    def trivial(res):
        return (not res) or (len(res) == 1 and all(v in (None, 0) for v in res[0]))

    seen, n_docs = set(), 0
    for q in spec["questions"]:
        qid = q["id"]
        if qid in seen:
            errs.append(f"{qid}: duplicate id")
        seen.add(qid)
        res, err = run(q["sql"])
        if err:
            errs.append(f"{qid}: SQL error: {err}")
        elif trivial(res):
            errs.append(f"{qid}: gold SQL returns nothing, 0 or NULL on your rows; make it return a real result")
        if not q.get("needs_columns"):
            errs.append(f"{qid}: needs_columns is empty")
        for c in q.get("needs_columns", []):
            if c not in cols:
                errs.append(f"{qid}: unknown needed column {c}")
        for d in q.get("needs_docs", []):
            c = d.get("column")
            if c not in cols:
                errs.append(f"{qid}: needs_docs refers to an unknown column {c}")
            elif not cols[c].get("doc"):
                errs.append(f"{qid}: {c} has no doc to remove")
            elif c not in q.get("needs_columns", []):
                errs.append(f"{qid}: doc-needed column {c} must also be listed in needs_columns")
            if not d.get("fact"):
                errs.append(f"{qid}: a needs_docs entry has no fact")
        n_docs += 1 if q.get("needs_docs") else 0
        if re.search(r"\b(columns?|tables?|schema|database)\b", q["text"], re.I):
            warns.append(f"{qid}: question uses schema words; rephrase as a user would")
        for c in q.get("needs_columns", []):
            stem = c.split(".")[1]
            for other in cols:
                o = other.split(".")[1]
                if other != c and len(stem) >= 4 and len(o) >= 4 and (stem in o or o in stem):
                    warns.append(f"{qid}: {other} may be a twin of needed column {c}; make sure it cannot hold the same information")

    for a in spec.get("ambiguous", []):
        aid = a["id"]
        if aid in seen:
            errs.append(f"{aid}: duplicate id")
        seen.add(aid)
        if len(a.get("readings", [])) != 2:
            errs.append(f"{aid}: need exactly 2 readings")
            continue
        outs = []
        for r in a["readings"]:
            res, err = run(r["sql"])
            if err:
                errs.append(f"{aid}: SQL error: {err}")
            elif trivial(res):
                errs.append(f"{aid}: a reading returns nothing, 0 or NULL")
            else:
                outs.append(sorted(map(repr, res)))
        if len(outs) == 2 and outs[0] == outs[1]:
            errs.append(f"{aid}: both readings return the same result; they must differ on your rows")
        for c in a.get("needs_columns", []):
            if c not in cols:
                errs.append(f"{aid}: unknown needed column {c}")
        rn = a.get("resolving_note", {})
        if rn.get("table") not in {t["name"] for t in spec["tables"]} or not rn.get("text"):
            errs.append(f"{aid}: resolving_note needs an existing table and a text")

    if not relaxed:
        if len(spec["questions"]) < 10:
            errs.append(f"only {len(spec['questions'])} questions (need 10)")
        if n_docs < 7:
            errs.append(f"only {n_docs} questions have needs_docs (need at least 7)")
        if len(spec.get("ambiguous", [])) < 5:
            errs.append(f"only {len(spec.get('ambiguous', []))} ambiguous questions (need 5)")
    return errs, warns


def main(argv):
    relaxed = "--relaxed" in argv
    paths = [a for a in argv if not a.startswith("--")]
    bad = 0
    for p in paths:
        with open(p, encoding="utf-8") as f:
            spec = json.load(f)
        errs, warns = validate(spec, relaxed)
        print(f"{p}: {len(errs)} errors, {len(warns)} warnings")
        for e in errs:
            print("  ERROR  ", e)
        for w in warns:
            print("  warning", w)
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
