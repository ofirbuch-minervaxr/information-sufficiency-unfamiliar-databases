# Honest assessment: does this project have a future?

Written 2026-11-26 by Claude from the sources in `sources/` and the links Ofir sent.
Status: **working proposal.** Items marked **[DECIDE]** belong to Ofir and Gilad.
This is not a systematic literature search: about 14 papers checked (see `02_Related_Work.md`).

## 1. Verdict

| Question | Answer |
|---|---|
| Is it a good *course* project? | **Yes.** It is the course's own recipe: a task with no data, so generate synthetic data, then compare fine-tuned vs off-the-shelf models (`1023_ProjectRequirements`, p.2). |
| Is it a *new research direction*? | **No.** Every component is already published. The combination is only incrementally new, and not proven new. |
| What can actually sink it? | Not novelty. (1) labels the model cannot tell apart, (2) a model that learns the generator's habits instead of the task, (3) scope vs time: the interim is about 3 weeks away. |

A modest novelty claim is fine for this course if it is stated honestly and the experiment is clean. A negative or mixed result with a good error analysis is also a valid outcome.

## 2. What is already published (checked)

| Idea in our deck | Already done by | What they did |
|---|---|---|
| Trained detector: answerable vs unanswerable, across domains | TriageSQL (2020) | RoBERTa classifier, 60% F1 |
| **Remove information to create labelled examples** | Know What I Don't Know (ACL Findings 2023); PRACTIQ (NAACL 2025) | KWIDK deletes a schema column to make an unanswerable example, or deletes it and adds two similar columns to make an ambiguous one (WikiSQL/WTQ). PRACTIQ edits Spider schemas and removes cell values. |
| Two plausible readings = ambiguous, checked by execution | AMBROSIA 2024, Disambiguate-First 2025, AIR 2026 | Same rule as ours (readings that give different results). **Cite them for it.** |
| Several interpretations; schema-only context | AmbiQT 2023, AIR 2026, IntentRL (cited in AIR), FALCON 2026 | AIR beats the RL-trained IntentRL under schema-only context, with no training |
| Abstain or ask the user | RTS 2025, ABISS 2026 | conformal abstention at schema linking; interactive clarification and feedback |
| Synthetic data + fine-tune small Qwen | FALCON 2026 (the one Gilad flagged) | Qwen2.5-1.5B/3B on 5.5k synthetic NL-to-SQL pairs. It is SQL generation. Its ambiguity filter has 28.6% recall (by design, 98.9% specificity). It is **not** sufficiency detection. |

## 3. What I could not find (the possible gap)

- A **small open LLM, LoRA-tuned on synthetic data, that judges whether the *given database information* is sufficient**, says what is missing and what to do next, and is tested on **unseen databases and one real database**.
- PRACTIQ itself lists "fine-tune open-source LLMs on data from our framework" as future work and says it did not do it. That is a citable, honest gap.
- Removing **documentation, keys and sample rows** (not only columns or values) as the labelling mechanism: not seen in the papers I read (ABISS removes BIRD "evidence" only to validate its questions). This is the weakest claim. Verify with the Scholar queries in `02_Related_Work.md`.

## 4. Honest novelty sentence (proposed wording)

> Prior work builds ambiguous/unanswerable question sets by editing schemas and evaluates large prompted models. We test whether *small* open models, LoRA-tuned on *synthetic* databases with *controlled removal of documentation, keys and sample rows*, learn to recognise insufficient information on unseen databases, and whether that transfers to a real database.

It makes no claim that detection, ambiguity, abstention or synthetic data are new.

## 5. Proposed objective (testable) [DECIDE thresholds]

**Question.** On databases never seen in training, does a LoRA-tuned ~1B model answer *less often when information is missing* than zero-shot, few-shot and prompt-only baselines, without refusing too much?

- **H1** The fine-tuned model beats the best small-model baseline on macro-F1 (unseen databases).
- **H2** The gain survives on the real database (a smaller gain is acceptable).
- **H3** False-sufficient rate drops while over-refusal stays within a tolerance.
- Reference points: "always sufficient", prompt-only ("answer only from the context"), and one large prompted model as a ceiling.
- Fix the success numbers **before** running anything. Placeholders: +10 macro-F1 points; false-sufficient rate halved; over-refusal at most +5 points.
- Any result is reportable. If fine-tuning does not beat the prompt-only baseline, that is the finding.

## 6. Problems to fix before generating data

| # | Problem | Why it matters | Fix |
|---|---|---|---|
| P1 | **"Insufficient context" and "unanswerable" can look identical to the model.** If insufficiency is made by deleting a table or column, the model sees the same thing as when the item never existed. | It cannot learn a difference it cannot see, so the label is noise. | Insufficient = the element is **visible but under-specified** (unlabelled codes, missing join key, unknown units). Deleted tables/columns go into "not answerable from the given information". Both are then identifiable from what the model sees. |
| P2 | **Shortcut learning.** If only "insufficient" examples have missing docs, the model learns "something is missing", not the reasoning. | High score on the synthetic test, nothing on real data. | Also remove *irrelevant* information in "sufficient" examples; balance lengths; test on a different generator and on a real database. |
| P3 | **Fuzzy boundary** between ambiguous and insufficient when docs are removed (two undocumented similar columns). | Subjective labels. | Write the rules on one page; both of you label 30 examples independently; compute Cohen's kappa. If kappa is below about 0.6, simplify the labels *before* scaling. |
| P4 | **Scale.** Deck: ~100 databases / 2,500 examples. Gilad's chat: 30 / 1,200. The ambiguity proposal: 15 / 500. | The interim needs data + EDA + baselines in about 3 weeks. | Pilot first (3-5 databases, ~100 examples), then ~30 databases / ~1,000 examples. |
| P5 | **Baselines must be strong** (course guide: "strong enough to make later improvements meaningful"). | A weak baseline makes any gain meaningless. | Zero-shot, few-shot, prompt-only, always-sufficient, plus one large prompted model on the test set. |
| P6 | **Real test and contamination.** Qwen/Gemma may have seen Spider/BIRD; the generating LLM may share style with the judge. | Inflated numbers. | Hand-label ~50 questions on one real database; say which; report per-database results. |
| P7 | **Verbalised confidence is unreliable in 1B models.** | A calibration claim would be empty. | Use the probability of the status token for ECE, or make calibration secondary. |
| P8 | **Two formulations are in circulation** (section 7). | The team is not building one thing. | Decide D1. |

## 7. Recommended framing: merge the 4-status deck with Gilad's 0/1/2 idea [DECIDE D1]

| | Deck (4 statuses) | Gilad's chat (0/1/2) | **Proposed merge** |
|---|---|---|---|
| Decision | sufficient / ambiguous / insufficient context / unanswerable | unanswerable / unambiguous / ambiguous | **Answerable (one reading) / Ambiguous (two readings, return the top 2) / Not answerable from the given information** |
| Extra output | confidence, missing info, explanation, next action | two ranked interpretations | `missing_information`, `next_action` (answer / clarify / request documentation / abstain), up to 2 interpretations |
| Input | schema + metadata + sample rows | schema only | schema + docs + keys + sample rows, with **information condition as the experimental variable** ("schema-only" is one condition) |
| Ambiguity rule | executed readings differ | plausibility judged by an LLM, no execution | **executed readings differ** (stronger; matches AIR and AMBROSIA) |

"Insufficient context" survives as a *reason* inside the third outcome: visible but undocumented means request documentation; nothing related visible means abstain.
Keep: controlled removal, split by database, real-database test, false-sufficient rate with over-refusal as the counter-metric.

## 8. What changed since the proposal (draft bullets for interim slide 1)

1. Novelty claim narrowed to a controlled combination, crediting KWIDK and PRACTIQ for removal-based data.
2. Statuses reduced from 4 to 3 outcomes, because two classes were not distinguishable from the model's view.
3. Scale reduced and phased: pilot first, then ~30 databases.
4. Information condition added as a controlled variable; schema-only is one setting.
5. Success criteria fixed in advance; stronger baselines, including a large-model reference.

## 9. Decisions for Ofir and Gilad

| ID | Decision | My default |
|---|---|---|
| D1 | 3 outcomes (merge) or keep 4 statuses | merge |
| D2 | Success thresholds in section 5 | the placeholders |
| D3 | Which real database to hand-label | one small public one (Chinook, Northwind or Sakila); a BIRD dev database only with the contamination caveat |
| D4 | Which strong LLM generates the data, and the budget | whichever you already have access to; check the cost on the pilot |
| D5 | Exact interim and final dates | if the proposal was week 5, interim is about mid-December and final about mid-January: **please confirm** |
