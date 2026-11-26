"""Naive baselines and artifact probes on the pilot data (pure Python, no libraries).

Usage:  python -I probe_baselines.py data/pilot.jsonl

Trains on the train databases, tests on the held-out databases. If a classifier that sees only the question,
or only the context, scores well above 'always answerable', the data has an artifact a model could exploit.
"""
import collections
import json
import math
import re
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python -I does not add the script folder
import metrics  # noqa: E402


def toks(s):
    return re.findall(r"[a-z0-9_]+", s.lower())


class NaiveBayes:
    def fit(self, docs, labels):
        self.classes = sorted(set(labels))
        self.prior = {c: math.log(labels.count(c) / len(labels)) for c in self.classes}
        self.counts = {c: collections.Counter() for c in self.classes}
        for d, lab in zip(docs, labels):
            self.counts[lab].update(toks(d))
        self.vocab = set().union(*[set(c) for c in self.counts.values()])
        self.total = {c: sum(self.counts[c].values()) for c in self.classes}

    def predict(self, d):
        t = [w for w in toks(d) if w in self.vocab]
        score = {c: self.prior[c] + sum(math.log((self.counts[c][w] + 1) / (self.total[c] + len(self.vocab) + 1)) for w in t)
                 for c in self.classes}
        return max(score, key=score.get)


def main(path):
    rows = [json.loads(line) for line in open(path, encoding="utf-8")]
    train = [r for r in rows if r["split"] == "train"]
    test = [r for r in rows if r["split"] == "test"]
    gold = [metrics.fine(r["label"], r["reason"]) for r in test]
    ytr = [metrics.fine(r["label"], r["reason"]) for r in train]
    print(f"train {len(train)} examples ({len({r['db_id'] for r in train})} databases), "
          f"test {len(test)} examples ({len({r['db_id'] for r in test})} databases)\n")
    print(metrics.line("always ANSWERABLE", metrics.summary(gold, ["ANSWERABLE"] * len(gold))))
    maj = collections.Counter(ytr).most_common(1)[0][0]
    print(metrics.line(f"majority of train ({maj[:5]})", metrics.summary(gold, [maj] * len(gold))))
    feats = {"NB question only": lambda r: r["question"], "NB context only": lambda r: r["context"],
             "NB question + context": lambda r: r["question"] + " " + r["context"]}
    for name, fn in feats.items():
        nb = NaiveBayes()
        nb.fit([fn(r) for r in train], ytr)
        print(metrics.line(name, metrics.summary(gold, [nb.predict(fn(r)) for r in test])))


if __name__ == "__main__":
    main(sys.argv[1])
