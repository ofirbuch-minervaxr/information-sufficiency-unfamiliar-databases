"""Score judge predictions against the pilot labels.

Usage:  python -I score_predictions.py data/pilot.jsonl data/judge_map.json <name> pred1.jsonl [pred2.jsonl ...]
Each prediction line: {"jid": "...", "label": "...", "reason": "...", "missing": "..."}.
Missing-information check is rough: does the text mention the removed column (or a gloss word)?
"""
import collections
import json
import re
import sys

import metrics


def words(s, n=4):
    return {w for w in re.findall(r"[a-z]+", s.lower().replace("_", " ")) if len(w) >= n}


def main(pilot, mapfile, name, preds):
    gold = {}
    for line in open(pilot, encoding="utf-8"):
        r = json.loads(line)
        gold[r["id"]] = r
    mapping = json.load(open(mapfile))
    g, p, miss = [], [], collections.defaultdict(list)
    bad = 0
    for path in preds:
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                r = gold[mapping[d["jid"]]]
            except (ValueError, KeyError):
                bad += 1
                continue
            gf = metrics.fine(r["label"], r["reason"])
            g.append(gf)
            p.append(metrics.fine(d.get("label"), d.get("reason")))
            text = str(d.get("missing") or "")
            ref = (r["missing_refs"] or [""])[0]
            if gf == "UNDERSPECIFIED":
                col = ref.split(".")[-1]
                miss[gf].append(col.lower() in text.lower().replace(" ", "_") or bool(words(col, 3) & words(text, 3)))
            elif gf == "NOT_PRESENT":
                miss[gf].append(bool(words(ref.split(".")[-1], 4) & words(text)))
            elif gf == "AMBIGUOUS":
                miss[gf].append(all(words(x) & words(text) for x in r["missing_refs"]))
    print(f"{name}: {len(g)} scored, {bad} unreadable lines")
    print(metrics.line(name, metrics.summary(g, p)))
    conf = collections.Counter(zip(g, p))
    print("confusion (gold -> predicted): " + "; ".join(f"{a[:5]}->{b[:5]}:{n}" for (a, b), n in sorted(conf.items()) if a != b))
    print("missing-info mention (rough): " + ", ".join(f"{k[:5]}={sum(v)}/{len(v)}" for k, v in miss.items()))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
