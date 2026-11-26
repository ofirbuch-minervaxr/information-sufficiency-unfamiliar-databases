"""Shared prompt, target and parsing for the pilot fine-tune and its evaluation."""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_RULES = open(os.path.join(_HERE, "judge_prompt.md"), encoding="utf-8").read().split("Output:")[0].strip()
_OUTPUT = ('Output: one JSON object and nothing else: {"label": "ANSWERABLE|AMBIGUOUS|NOT_ANSWERABLE", '
           '"reason": "UNDERSPECIFIED|NOT_PRESENT|null", "missing": "what is missing, or the two readings, in a few words; empty if answerable"}')


def build_prompt(r):
    return f"{_RULES}\n\n{_OUTPUT}\n\nDatabase information:\n{r['context']}\n\nQuestion: {r['question']}"


def target(r):
    refs = r.get("missing_refs") or []
    if r["reason"] == "UNDERSPECIFIED":
        missing = "definition of " + refs[0].replace("doc:", "")
    elif r["reason"] == "NOT_PRESENT":
        missing = "column " + refs[0]
    elif r["label"] == "AMBIGUOUS":
        missing = " | ".join(x.replace("reading: ", "") for x in refs)
    else:
        missing = ""
    return json.dumps({"label": r["label"], "reason": r["reason"], "missing": missing}, ensure_ascii=False)


def parse(text):
    m = re.search(r"\{.*?\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except ValueError:
        return None


def load(path, split):
    return [r for r in (json.loads(line) for line in open(path, encoding="utf-8")) if r["split"] == split]
