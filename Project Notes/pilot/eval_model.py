"""Evaluate a small causal LM (optionally with a LoRA adapter) on the pilot test split, greedy decoding.

Usage:  python eval_model.py --data data/pilot.jsonl --name zero-shot-qwen15 [--adapter runs/qwen15_lora] [--split test]
Writes results/<name>_preds.jsonl and prints the metric line (macro-F1, false-sufficient rate, over-refusal, per-class F1).
"""
import argparse
import json
import os
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import metrics  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/pilot.jsonl")
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--name", required=True)
    ap.add_argument("--split", default="test")
    ap.add_argument("--max-new", type=int, default=96)
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.bfloat16).cuda()
    if args.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, args.adapter)
    model.eval()

    rows = common.load(args.data, args.split)
    gold, pred, unparsed = [], [], 0
    os.makedirs("results", exist_ok=True)
    with open(f"results/{args.name}_preds.jsonl", "w", encoding="utf-8") as out:
        for r in rows:
            text = tok.apply_chat_template([{"role": "user", "content": common.build_prompt(r)}],
                                           tokenize=False, add_generation_prompt=True)
            ids = tok(text, add_special_tokens=False, return_tensors="pt").to("cuda")
            with torch.no_grad():
                gen = model.generate(**ids, max_new_tokens=args.max_new, do_sample=False)
            reply = tok.decode(gen[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
            d = common.parse(reply)
            if d is None:
                unparsed += 1
                d = {"label": "ANSWERABLE", "reason": None, "missing": ""}  # unparseable counts as an answer attempt
            gold.append(metrics.fine(r["label"], r["reason"]))
            pred.append(metrics.fine(d.get("label"), d.get("reason")))
            out.write(json.dumps({"id": r["id"], "variant": r["variant"], "reply": reply, **d}, ensure_ascii=False) + "\n")
    print(f"{args.name}: {len(rows)} items, {unparsed} unparseable replies")
    print(metrics.line(args.name, metrics.summary(gold, pred)))


if __name__ == "__main__":
    main()
