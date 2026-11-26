# Request for the pc3 helper (study project, low priority)

From the Claude on desktop-eq81b8r, for Ofir. Public repo: https://github.com/ofirbuch-minervaxr/information-sufficiency-unfamiliar-databases, branch `work/direction-1-pilot`, folder `Project Notes/pilot/`.

## What this is
A course project (LLM course, Holon Institute of Technology): a small judge that says whether the visible information about a database (tables, docs, 3 sample rows) is enough to answer a question: ANSWERABLE / AMBIGUOUS / NOT_ANSWERABLE (reason UNDERSPECIFIED or NOT_PRESENT), and names what is missing. We want a quick feasibility run: LoRA fine-tune Qwen2.5-1.5B-Instruct on a tiny synthetic set (4 databases) and compare it with the same model prompted zero-shot, on 2 held-out databases. This is a small study project: do not touch or slow down other work on this machine.

## Approved downloads (Ofir approved them in chat on 2026-11-26, for this computer only; if he has not told you himself, confirm with him first)
- a new Python venv on the biggest free drive (never C: unless it has more than 20 GB free), for example `E:\ClaudeTemp\venv-suff`
- PyTorch with CUDA from download.pytorch.org (about 2.5 GB), then `transformers`, `peft`, `accelerate`, `datasets` from PyPI (about 0.5 GB)
- the model `Qwen/Qwen2.5-1.5B-Instruct` from Hugging Face (about 3.1 GB, Apache-2.0, no login needed)
Nothing else. No Gemma (it needs a license login).

## Steps
1. `git clone --branch work/direction-1-pilot <repo url>` (or fetch the branch) to a folder on that drive; work in `Project Notes/pilot/`.
2. Create the venv, install the packages, check `torch.cuda.is_available()` and report the GPU name and VRAM.
3. Check that `data/pilot.jsonl` exists on the branch (I push it once the six database specs are done; pull again until it is there). `python -I metrics.py` style imports are plain: run the scripts from the `pilot` folder.
4. Baseline: `python eval_model.py --name zero-shot-qwen15`
5. Train: `python train_lora.py --out runs/qwen15_lora` (3 epochs, expect a few minutes; the scripts were written without a GPU at hand, so if something breaks, fix it minimally and tell me the diff).
6. Evaluate: `python eval_model.py --name lora-qwen15 --adapter runs/qwen15_lora`
7. Report in the room: the two metric lines (macro-F1, false-sufficient rate, over-refusal, per-class F1), unparseable-reply counts, GPU, VRAM peak, wall time. If Ofir's git credentials are set up on that machine, also commit `results/*.txt` and `results/*_preds.jsonl` to the branch; if not, just paste the numbers.

## Limits
About one hour of work. If something blocks (a download fails, VRAM too small, a sign-in is needed), post one line saying what, and stop. Do not run anything on the held-out test split during training (the scripts already use only the train split).
