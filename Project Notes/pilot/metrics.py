"""Shared metrics for the pilot. Fine labels: ANSWERABLE, AMBIGUOUS, UNDERSPECIFIED, NOT_PRESENT."""
FINE = ["ANSWERABLE", "AMBIGUOUS", "UNDERSPECIFIED", "NOT_PRESENT"]
THREE = ["ANSWERABLE", "AMBIGUOUS", "NOT_ANSWERABLE"]


def fine(label, reason):
    if label == "NOT_ANSWERABLE":
        return reason if reason in ("UNDERSPECIFIED", "NOT_PRESENT") else "NOT_PRESENT"
    return label if label in ("ANSWERABLE", "AMBIGUOUS") else "ANSWERABLE"


def three(f):
    return "NOT_ANSWERABLE" if f in ("UNDERSPECIFIED", "NOT_PRESENT") else f


def f1_per_class(gold, pred, labels):
    out = {}
    for lab in labels:
        tp = sum(1 for g, p in zip(gold, pred) if g == lab and p == lab)
        fp = sum(1 for g, p in zip(gold, pred) if g != lab and p == lab)
        fn = sum(1 for g, p in zip(gold, pred) if g == lab and p != lab)
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        out[lab] = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
    return out


def summary(gold_f, pred_f):
    g3, p3 = [three(x) for x in gold_f], [three(x) for x in pred_f]
    f4, f3 = f1_per_class(gold_f, pred_f, FINE), f1_per_class(g3, p3, THREE)
    insuff = [i for i, g in enumerate(g3) if g != "ANSWERABLE"]
    ans = [i for i, g in enumerate(g3) if g == "ANSWERABLE"]
    fs = sum(1 for i in insuff if p3[i] == "ANSWERABLE") / len(insuff) if insuff else float("nan")
    orr = sum(1 for i in ans if p3[i] != "ANSWERABLE") / len(ans) if ans else float("nan")
    return {"n": len(gold_f), "macro3": sum(f3.values()) / 3, "macro4": sum(f4.values()) / 4,
            "false_sufficient": fs, "over_refusal": orr, "f1": f4,
            "acc4": sum(1 for g, p in zip(gold_f, pred_f) if g == p) / len(gold_f)}


def line(name, s):
    per = " ".join(f"{k[:5]}={v:.2f}" for k, v in s["f1"].items())
    return (f"{name:<30} n={s['n']:<3} macroF1(3)={s['macro3']:.2f} macroF1(4)={s['macro4']:.2f} "
            f"false-suff={s['false_sufficient']:.2f} over-refusal={s['over_refusal']:.2f} | F1 {per}")
