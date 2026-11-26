"""Agreement check for the label rules (05_Label_Rules.md).

Usage:  python agreement.py author_A.csv rater_B.csv [author_B.csv rater_A.csv ...]

Files come in (author, rater) pairs and are joined on the `id` column.
Labels: ANSWERABLE, AMBIGUOUS, NOT_ANSWERABLE.  Reasons (only for NOT_ANSWERABLE): UNDERSPECIFIED, NOT_PRESENT.
"""
import csv
import sys
from collections import Counter

LABELS = ["ANSWERABLE", "AMBIGUOUS", "NOT_ANSWERABLE"]
YES = ("1", "Y", "YES", "TRUE")


def read(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def norm(x):
    return (x or "").strip().upper()


def accuracy(pairs):
    return sum(a == b for a, b in pairs) / len(pairs) if pairs else float("nan")


def kappa(pairs):
    """Cohen's kappa for two raters."""
    n = len(pairs)
    if n == 0:
        return float("nan")
    po = sum(a == b for a, b in pairs) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def main(argv):
    if len(argv) < 2 or len(argv) % 2:
        sys.exit(__doc__)
    rows, missing = [], []
    for i in range(0, len(argv), 2):
        authors, raters = read(argv[i]), read(argv[i + 1])
        for key, a in authors.items():
            r = raters.get(key)
            if r is None or not norm(r.get("rater_label")):
                missing.append(key)
                continue
            rows.append({
                "id": key,
                "a": norm(a.get("author_label")), "b": norm(r.get("rater_label")),
                "ar": norm(a.get("author_reason")), "br": norm(r.get("rater_reason")),
                "unsure": norm(a.get("author_unsure")) in YES or norm(r.get("rater_unsure")) in YES,
            })

    bad_labels = [x["id"] for x in rows if x["a"] not in LABELS or x["b"] not in LABELS]
    if bad_labels:
        print(f"WARNING: unknown label on {bad_labels[:10]} (use {', '.join(LABELS)})\n")

    pairs = [(x["a"], x["b"]) for x in rows]
    k = kappa(pairs)
    print(f"items compared: {len(rows)}   not rated yet: {len(missing)} {missing[:10]}")
    print(f"3-outcome agreement: {accuracy(pairs):.2f}   Cohen's kappa: {k:.2f}")
    sure = [(x["a"], x["b"]) for x in rows if not x["unsure"]]
    print(f"  without items flagged unsure ({len(sure)} left): agreement {accuracy(sure):.2f}, kappa {kappa(sure):.2f}")

    labels = sorted(set(LABELS) | {v for p in pairs for v in p})
    width = max(len(v) for v in labels)
    print("\nconfusion (rows = author's label, columns = rater's label)")
    print(" " * (width + 2) + "  ".join(f"{v[:6]:>6}" for v in labels))
    for a in labels:
        print(f"{a:<{width}}  " + "  ".join(f"{sum(1 for x, y in pairs if x == a and y == b):>6}" for b in labels))

    both_na = [x for x in rows if x["a"] == x["b"] == "NOT_ANSWERABLE"]
    reasons = [(x["ar"], x["br"]) for x in both_na]
    print(f"\nreason (UNDERSPECIFIED vs NOT_PRESENT) on items both called NOT_ANSWERABLE: "
          f"{len(both_na)} items, agreement {accuracy(reasons):.2f}")

    to_discuss = [x for x in rows if x["a"] != x["b"] or (x in both_na and x["ar"] != x["br"])]
    print(f"\nto discuss ({len(to_discuss)}):  id: author label/reason  vs  rater label/reason")
    for x in to_discuss:
        print(f"  {x['id']}: {x['a']}/{x['ar'] or '-'}  vs  {x['b']}/{x['br'] or '-'}" + ("   [unsure]" if x["unsure"] else ""))

    if k != k:  # NaN
        verdict = "kappa is undefined (every item had the same label): add variety"
    elif k >= 0.80:
        verdict = "strong: freeze the rules"
    elif k >= 0.60:
        verdict = "usable: fix the rules for each disagreement, then relabel those items"
    else:
        verdict = "weak: simplify the labels before generating data"
    print(f"\nverdict: {verdict}   (30 items is a sanity check, not a result)")


if __name__ == "__main__":
    main(sys.argv[1:])
