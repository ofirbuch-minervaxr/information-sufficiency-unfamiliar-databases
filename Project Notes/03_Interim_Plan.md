# Interim presentation: what is required, what we have, plan

Sources: `1023_ProjectRequirements` (in `Proposal Recommendation/`) and the instructor's midterm guide (`sources/course/midterm-guide_text_2026-11-26.txt`; page https://www.apartsin.com/teaching/guides/midterm-presentation.html).
**Dates are assumptions**: week 5 proposal, week 9 interim, week 13 final; the proposal was around Nov 16-18, so the interim is about Dec 14-18. **[DECIDE D5: confirm the real dates.]**

## 1. Requirement vs where we stand

| Slide | Required | We have | Missing |
|---|---|---|---|
| 1 Project review | Motivation, specification, **what changed**, novelty/contributions | Proposal deck (two versions, see `04`) | "What changed" (draft in `01` section 8); honest novelty sentence (`01` section 4) |
| 2 Previous work | 3 or more recent, well-cited papers in a table: task, methods, data, results, limitations, relation; which methods/baselines/metrics we reuse | 12-paper table (`02`) | Pick 4-7 rows; re-check counts on Scholar; the "what we reuse / which limitation we address" paragraph |
| 3 Dataset | The data and how it is generated; **EDA** (class distribution, lengths, types); examples; splits | The recipe only | **Any data**; EDA graphs *with interpretation*; split by database |
| 4 Baseline + results | A baseline; results in tables and graphs; **error analysis** | Models and prompts chosen | Baseline numbers; error categories with cause and frequency |
| 5 Plan | Table: scope, owner, due date, expected output, **risk, fallback**; last row = final presentation + repository | Nothing | Table below |

The guide also warns against: repeating the proposal unchanged, graphs with no interpretation, deliberately weak baselines, comparing methods on different splits, and vague tasks such as "improve model". The final system **must include a fine-tuned model**, not only prompting.

## 2. Plan (owners are proposals; dates assumed)

| # | Task | Technical scope | Owner | Due | Output | Risk -> fallback |
|---|---|---|---|---|---|---|
| 0 | Decide D1-D5 (`01` section 9) | framing, thresholds, real database, generator LLM, dates | both | Nov 28 | decisions noted in `01` | none |
| 1 | Label rules + schema JSON + agreement check | one-page rules; both label 30 hand-made examples; Cohen's kappa | both | Nov 30 | `05_Label_Rules.md` (draft written), kappa | low kappa -> merge classes |
| 2 | Pilot generator | 3-5 databases, 2 domains; SQL validation; removal log; ~100 examples | Ofir | Dec 5 | `Data/pilot.jsonl`, `Code/generate.py` | invalid LLM output -> stricter templates |
| 3 | Evaluation harness + prompts | zero-shot, few-shot, prompt-only, always-sufficient; JSON parsing; macro-F1, false-sufficient rate, over-refusal | Gilad | Dec 5 | `Code/evaluate.py` | small model breaks JSON -> constrained decoding |
| 4 | Scale + EDA | ~30 databases / ~1,000 examples; split by database; EDA notebook | Ofir | Dec 9 | `Data/*.jsonl`, `Visuals/eda_*` | generation cost -> fewer databases |
| 5 | Real test set | 1 real database, ~50 questions, both label independently | both | Dec 9 | `Data/real_test.jsonl`, kappa | too few -> 30 |
| 6 | Baselines + error analysis | run on validation/test; group errors; add one large prompted model | both | Dec 11 | `Results/baseline_*.csv` | API limits -> 100-example subset |
| 7 | Interim deck + reviewer bot | slides 1-5; run the course Midterm Report Reviewer Bot; rehearse | both | Dec 12 | `Slides/Interim/` | none |
| 8 | **Interim presentation** | | both | date TBC | | |
| 9 | LoRA fine-tuning | Qwen2.5-1.5B-Instruct and Gemma-3-1B-it; Colab T4; 3 seeds | Ofir | about Jan 2 | adapters, `Results/ft_*.csv` | out of memory -> shorter prompts / QLoRA |
| 10 | Ablations + calibration | information-condition grid; no-clarification ablation; ECE from status-token probability | Gilad | about Jan 8 | `Results/ablation_*.csv` | cut calibration |
| 11 | Final results + deck | tables, graphs, error analysis, limitations; run the Final Presentation bot | both | about Jan 11 | `Slides/Final/` | none |
| 12 | **Final presentation + repository** | README sections; Repository Submission Validator bot | both | week 13 / end of semester + 2 weeks (TBC) | GitHub repo | none |

## 3. Learning checkpoints (so the work is yours, not just generated)

| After task | You should be able to explain, without notes |
|---|---|
| 1 | Why two annotators and kappa; what a "label rule" is |
| 2 | Why we generate the full database first and then remove information (ground truth by construction) |
| 4 | Why split **by database**, and what leakage would look like |
| 6 | Macro-F1 vs accuracy; why "always sufficient" is a baseline; false-sufficient vs over-refusal |
| 9 | What LoRA changes (small adapter matrices, base model frozen); why 3 seeds |
| 10 | What ECE measures and why verbalised confidence is weak |

## 4. Course bots and guides (public pages by the instructor)
- Midterm Report Reviewer (LLM course): https://chatgpt.com/g/g-6a68aec7d7a0819193fc8c0716ec5674-llm-course-midterm-report-reviewer
- Final Presentation reviewer: https://chatgpt.com/g/g-6a68af5f6e9c8191a890a965e890259c-llm-course-review-your-final-presentation
- Repository Submission Validator: https://chatgpt.com/g/g-6a68afd516088191af4236a0a55a333a-llm-course-repo-submission-validator
- All bots: https://www.apartsin.com/teaching/course-bots.html
