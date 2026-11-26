"""LoRA fine-tune of a small causal LM on the pilot train split (plain PyTorch loop, no TRL).

Usage:  python train_lora.py --data data/pilot.jsonl --out runs/qwen15_lora [--model Qwen/Qwen2.5-1.5B-Instruct]
Needs: torch (CUDA), transformers, peft. Written without a GPU at hand: if something breaks, fix it minimally and say what you changed.
"""
import argparse
import os
import random
import sys

import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, get_cosine_schedule_with_warmup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/pilot.jsonl")
    ap.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--out", default="runs/qwen15_lora")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--max-len", type=int, default=2048)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    random.seed(args.seed)
    torch.manual_seed(args.seed)

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.bfloat16).cuda()
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM",
                     target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
    model = get_peft_model(model, cfg)
    for p in model.parameters():
        if p.requires_grad:
            p.data = p.data.float()
    model.print_trainable_parameters()

    def encode(r):
        text = tok.apply_chat_template([{"role": "user", "content": common.build_prompt(r)}],
                                       tokenize=False, add_generation_prompt=True)
        prompt = tok(text, add_special_tokens=False)["input_ids"]
        answer = tok(common.target(r) + "<|im_end|>", add_special_tokens=False)["input_ids"]
        ids = (prompt + answer)[-args.max_len:]
        labels = ([-100] * len(prompt) + answer)[-args.max_len:]
        return torch.tensor([ids]).cuda(), torch.tensor([labels]).cuda()

    train = common.load(args.data, "train")
    data = [encode(r) for r in train]
    print(f"{len(data)} training examples, longest {max(d[0].shape[1] for d in data)} tokens")
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.lr, weight_decay=0.0)
    steps = args.epochs * len(data) // args.accum
    sched = get_cosine_schedule_with_warmup(opt, max(1, steps // 20), max(1, steps))
    model.train()
    n = 0
    for epoch in range(args.epochs):
        random.shuffle(data)
        run = 0.0
        for i, (ids, labels) in enumerate(data):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                loss = model(input_ids=ids, labels=labels).loss
            (loss / args.accum).backward()
            run += loss.item()
            if (i + 1) % args.accum == 0:
                torch.nn.utils.clip_grad_norm_(params, 1.0)
                opt.step()
                sched.step()
                opt.zero_grad()
                n += 1
        print(f"epoch {epoch + 1}: mean loss {run / len(data):.4f} ({n} optimizer steps)")
    model.save_pretrained(args.out)
    print("saved adapter to", args.out)


if __name__ == "__main__":
    main()
