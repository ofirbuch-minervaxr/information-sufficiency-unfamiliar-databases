# Work Schedule v0.1 (three tracks)

Draft for Ofir and Gilad to adjust. Today is Thu 26 Nov 2026. The schedule assumes direction **A-refined** (controlled removal, 3 outcomes, name the missing information). It changes little if you pick another direction, except weeks 1-2. **All dates are assumptions**: proposal at week 5 (about 16-18 Nov), interim at week 9 (about 14-18 Dec), final at week 13 (about 11-15 Jan). Confirm the real dates with the course (decision D5). Owners are proposals. Weeks run Sunday to Thursday.

# Tracks and how they connect

| Track | Output | Feeds |
|---|---|---|
| Practical | Generator, data, evaluation code, baselines, fine-tuned model, repository | Gives the Presentation its tables and graphs |
| Presentation | Interim deck, final deck, README | Forces us to understand and defend the Practical track |
| Learning | The study pack (`07_Study_Pack_EN.md`) and one checkpoint per task | Needed to present and answer questions |

**Rule: a task is "done" only when the owner can explain it to the other person in 5 minutes without notes.**

# Plan to the interim presentation (3 weeks)

| Week | Practical | Presentation | Learning |
|---|---|---|---|
| **W1: 29 Nov - 3 Dec** | **Decide D1-D5** (both, by Sun 29 Nov). Label rules and the 30-example agreement check (both; kappa). Start the pilot generator: 3-5 databases (Ofir) | Merge the two proposal decks into one; draft slide 1 and the novelty sentence | Study pack pages 1, 2 and 3; checkpoint: explain the labels, ground truth and kappa to each other |
| **W2: 6 - 10 Dec** | Finish the pilot (about 100 examples, SQL validated, removal log) (Ofir). Evaluation harness: prompts, JSON parsing, macro-F1, false-sufficient rate, over-refusal (Gilad). Scale toward about 30 databases / 1,000 examples, split by database | Slide 2 from `02_Related_Work.md` (pick 4-7 rows, recheck counts on Scholar) | Page 3 and 4; checkpoint: why split by database, why "always sufficient" is a baseline |
| **W3: 13 - 17 Dec** | EDA; real database labelled by hand (about 50 questions, both label, kappa); baselines (zero-shot, few-shot, prompt-only, always-sufficient, one large model); error analysis (both) | Slides 3, 4 and 5; run the course Midterm Report Reviewer bot; rehearse twice | Page 5 and 6; checkpoint: present the five slides to each other and answer the self-check questions |
| **Interim presentation** | | **Date to confirm with the course** | |

**If the interim date is earlier than 14 Dec:** cut the real set to 30 questions, run baselines on a 100-example subset, and say so on the plan slide.

# After the interim (to the final)

| Period | Practical | Presentation | Learning |
|---|---|---|---|
| 20 Dec - 1 Jan | LoRA fine-tuning of Qwen2.5-1.5B-Instruct and Gemma-3-1B-it on Colab T4, 3 seeds (Ofir) | Fix the deck from the instructor's feedback | Page 4: LoRA, seeds; checkpoint: explain what is frozen |
| 3 - 7 Jan | Ablations and calibration (ECE) (Gilad); test on the real database | Start the results tables and graphs | Calibration; checkpoint: explain ECE |
| 10 - 14 Jan | Final run, freeze results | Final deck, run the Final Presentation reviewer bot, rehearse | Self-check, full run-through |
| Week 13 and end of semester + 2 weeks | Repository: README sections, code, data, results; Repository Submission Validator bot | **Final presentation** | |

# Working rhythm

| What | When |
|---|---|
| Two 30-minute syncs | For example Sun and Wed: what is done, what is blocked, who explains what |
| Short written status | After each sync, 3 lines in the shared chat |
| Re-plan | Every Sunday: move tasks, never silently slip; the schedule is expected to change, the point is to keep moving |
| Decisions that need both of you | D1 direction, D2 success criteria, D3 real database, D4 generator model and budget, D5 dates |
| Everything else | Decide it yourselves, note it, move on |

# Risks and fallbacks

| Risk | Fallback |
|---|---|
| Two annotators disagree (low kappa) | Merge UNDERSPECIFIED and NOT_PRESENT into one class |
| The LLM generator produces invalid databases or SQL | Stricter templates; validate by executing the SQL |
| The small model breaks the JSON format | Constrained decoding or a shorter output format |
| Not enough time for 30 databases | 15 databases, report it honestly |
| Colab out of memory | Shorter prompts or QLoRA |
| The fine-tuned model does not transfer to the real database | Report it as the finding and analyse why |
