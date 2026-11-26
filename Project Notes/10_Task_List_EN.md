# Task list (living plan, GitHub-ready)

Direction chosen on 26 Nov 2026 by Ofir and Gilad: **direction 1**, a transfer-first sufficiency judge (three outcomes, the missing information named, trained on controlled-removal data, tested on unseen and real databases). Ambiguity is a secondary test inside it; the documentation loop and the Hebrew-question test are optional extras.

Hours are focused work per person, rough. Owners are proposals: swap freely. Dates are assumptions (decision D5: confirm with the course). **A task is done only after its learning checkpoint**: explain it to the other person in five minutes without notes.

**How to use on GitHub:** one issue per row, title `T07 Large prompted model baseline`, labels `practical`, `presentation` or `learning`, milestones M1-M5, assignee. Ask Claude to open them (the repo is public, so issues are visible).

**Living plan rules:** re-plan every Sunday. Change this file or the issues, never silently slip; add one line to the change log at the bottom. If time runs short, drop in this order: T18, T20, T19, T10.

## Milestones
| | Milestone | Assumed date |
|---|---|---|
| M1 | Rules and decisions | 1 Dec |
| M2 | Pilot data and evaluation harness | 8 Dec |
| M3 | Interim deck | about 14-18 Dec (TBC) |
| M4 | Fine-tuning and transfer results | 1 Jan |
| M5 | Final deck and repository | about 11-14 Jan (TBC) |

## Tasks
| ID | Task | Track | Owner | h | Depends | Done when | Learning checkpoint |
|---|---|---|---|---|---|---|---|
| **M1** | | | | | | | |
| T01 | Confirm success criteria (+10 macro-F1 over the best prompted baseline, false-sufficient rate halved, over-refusal up at most 5 points), the real database, the API budget | practical | both | 1 | | decisions written in `README` | state H1-H3 in your own words |
| T02 | Label agreement: each labels the same 30 hand-made examples (`05_Label_Rules.md` section 6), run `agreement/agreement.py`, fix the rules | learning | both | 3 each | T01 | kappa at least 0.6, rules v1.0 | what kappa measures, why two annotators |
| **M2** | | | | | | | |
| T03 | Review and extend the pilot generator (v0 exists in `pilot/`): read the code, run it, add removal operators, fix label bugs | practical | Ofir | 6 | | generator runs end to end; you can explain every operator | why full database first, then removal; what a control example prevents |
| T04 | Scale the data: about 30 database specs written by an LLM (validator must pass), about 1,000 examples, split by database | practical | Ofir | 8 | T03, budget | `Data/` files and a counts table | why split by database; what leakage looks like |
| T05 | Evaluation harness: prompts, JSON parsing, macro-F1, false-sufficient rate, over-refusal, missing-information score | practical | Gilad | 8 | T03 | `evaluate.py` scores any predictions file | macro-F1 vs accuracy; false-sufficient vs over-refusal |
| T06 | Baselines: always-sufficient, majority, question-only and context-only classifiers (artifact check), zero-shot and few-shot Qwen2.5-1.5B and Gemma-3-1B | practical | Gilad | 8 | T05 | one baseline table on held-out databases | why "always sufficient" is a baseline |
| T07 | Large prompted model baseline through the API, on the test set and the real set | practical | Ofir | 3 | T05, budget | a row in the baseline table | |
| T08 | EDA notebook: class balance, lengths, removal types, per database; one sentence of interpretation under every graph | presentation | Ofir | 5 | T04 | figures in `Visuals/` | |
| T09 | Real test set A: one real database that has documentation, about 50 questions, both label independently | practical | both | 6 each | T02 | `real_test.jsonl`, kappa | why synthetic-only evaluation is a weak pattern |
| T10 | Real test set B (stretch): BIRD dev natural removal with a necessity test (the 346 MB `dev.zip` needs your OK to download) | practical | Gilad | 10 | T05 | at least 100 labelled items | why "evidence removed" is not automatically UNDERSPECIFIED |
| T11 | Error analysis: group the errors, name causes, count them | presentation | both | 4 | T06 | table with examples | |
| **M3** | | | | | | | |
| T12 | Interim deck, slides 1-5 (Ofir 1, 3, 5; Gilad 2, 4) | presentation | both | 8 each | T04, T06, T09 | deck in `Slides/Interim/` | present it to each other |
| T13 | Run the Midterm Report Reviewer bot, fix, rehearse twice | presentation | both | 4 | T12 | bot feedback addressed | |
| **M4** | | | | | | | |
| T14 | LoRA training script on Colab T4, one run per model | practical | Ofir | 8 | T04 | adapters and validation results | what LoRA freezes and what it trains |
| T15 | Three seeds, two models | practical | Ofir | 6 | T14 | mean and spread | why three seeds |
| T16 | Transfer evaluation: held-out databases, real sets, slices of TriageSQL, AMBROSIA, AmbiQT | practical | Gilad | 8 | T14 | transfer table | why an in-distribution gain is not the result |
| T17 | Ablations: no controls, no missing-information output, schema only vs plus docs vs plus rows | practical | Gilad | 8 | T15 | ablation table | |
| T18 | Calibration (ECE from the status-token probability), optional | practical | Gilad | 4 | T15 | ECE and a reliability plot | what ECE measures |
| **M5** | | | | | | | |
| T19 | Optional: gate a SQL generator with the judge, report accuracy at fixed coverage | practical | Ofir | 8 | T15 | one figure | |
| T20 | Optional: Hebrew questions over English schemas as a transfer test | practical | Gilad | 6 | T15 | one table | |
| T21 | Novelty re-scan in early January: Scholar and arXiv for successors of BAR-SQL and for abstain-sql | presentation | Gilad | 3 | | novelty sentence final | |
| T22 | Final deck and the Final Presentation reviewer bot | presentation | both | 10 each | T16, T17 | deck in `Slides/Final/` | |
| T23 | Repository: README sections, reproducibility, the Repository Submission Validator bot | practical | both | 8 each | all | validator passes | |

## Open questions for the instructor
1. Is our proposal recorded as approved, and may we sharpen the direction before the interim without re-approval?
2. Is a validated synthetic test set plus a small human-verified real set (about 50 items) enough, or is a larger real set expected?
3. Does a LoRA fine-tune of a 1-1.5B model, compared with prompted baselines and a large API model, meet the fine-tuning requirement? How many compared models at the interim?
4. If the trained model does not transfer to unseen databases, is a well-analysed negative result acceptable?
5. Exact interim, final and repository dates, and the size of the per-project API allowance.

## Change log
- 2026-11-26: first version after choosing direction 1.
