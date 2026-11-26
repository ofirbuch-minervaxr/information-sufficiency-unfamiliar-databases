"""Write anonymised, label-free judge chunks from the test split.

Usage:  python -I make_judge_input.py data/pilot.jsonl data [chunks]
Writes data/judge_chunk_<k>.jsonl (fields: jid, question, context) and data/judge_map.json (jid -> id).
The id of an example names its variant (and so its label), which is why judges only ever see the jid.
"""
import json
import random
import sys

src, outdir = sys.argv[1], sys.argv[2]
k = int(sys.argv[3]) if len(sys.argv) > 3 else 4
rows = [json.loads(line) for line in open(src, encoding="utf-8")]
test = [r for r in rows if r["split"] == "test"]
random.Random(3).shuffle(test)
mapping = {}
for i in range(k):
    with open(f"{outdir}/judge_chunk_{i + 1}.jsonl", "w", encoding="utf-8") as f:
        for r in test[i::k]:
            jid = f"j{len(mapping) + 1:03d}"
            mapping[jid] = r["id"]
            f.write(json.dumps({"jid": jid, "question": r["question"], "context": r["context"]}, ensure_ascii=False) + "\n")
json.dump(mapping, open(f"{outdir}/judge_map.json", "w"), indent=0)
print(len(test), "test items in", k, "chunks")
