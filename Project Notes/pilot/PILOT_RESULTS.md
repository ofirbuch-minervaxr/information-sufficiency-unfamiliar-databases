# Pilot results, 2026-11-26 (smoke test, not a result)

Branch `work/direction-1-pilot`. Everything here is a first look to decide whether direction 1 is worth building. It is not evidence for the final report.

## What was run
- Six synthetic databases (`specs/`), 288 items made by controlled removal (`build_dataset.py`, label known by construction).
- Split by database: train 4 DBs (192 items); test 2 unseen DBs, `clinic` and `restaurant_chain` (96 items: 50 ANSWERABLE, 10 AMBIGUOUS, 16 UNDERSPECIFIED, 20 NOT_PRESENT).
- Blind judges: Claude Sonnet and Claude Haiku, each as two subagents covering half of the test set. They saw only the question and the visible context (plus the label rules in `judge_prompt.md`), in shuffled order with anonymised ids. They never saw ids, variants or labels.
- Naive baselines: Naive Bayes on the question text, the context text, or both (`probe_baselines.py`).

## Numbers (test split, n = 96)

| Model | macro-F1 (3 classes) | false-sufficient | over-refusal |
|---|---|---|---|
| always ANSWERABLE (= train majority) | 0.23 | 1.00 | 0.00 |
| Naive Bayes, question only | 0.37 | 0.91 | 0.08 |
| Naive Bayes, context only | 0.23 | 1.00 | 0.00 |
| Naive Bayes, question + context | 0.23 | 1.00 | 0.02 |
| Haiku, blind | 0.89 | 0.15 | 0.02 |
| Sonnet, blind | 0.95 | 0.11 | 0.00 |

Per-class F1 (ANSWERABLE / AMBIGUOUS / UNDERSPECIFIED / NOT_PRESENT): Sonnet 0.95 / 0.95 / 1.00 / 0.89, Haiku 0.92 / 0.84 / 0.94 / 0.79.

Confusions (gold -> predicted): Sonnet AMBIGUOUS->ANSWERABLE 1, NOT_PRESENT->ANSWERABLE 4. Haiku AMBIGUOUS->ANSWERABLE 1, AMBIGUOUS->UNDERSPECIFIED 1, ANSWERABLE->AMBIGUOUS 1, NOT_PRESENT->ANSWERABLE 6, NOT_PRESENT->UNDERSPECIFIED 1.

Missing item named (rough keyword check, `score_predictions.py`): Sonnet AMBIGUOUS 9/10, NOT_PRESENT 15/20, UNDERSPECIFIED 16/16. Haiku 5/10, 11/20, 16/16.

## What this does and does not say
- The labels can be recovered from the visible context: a blind strong model reaches 0.95, so they are not arbitrary. This is not human agreement; kappa on 30 hand-made items is still to do (`05_Label_Rules.md`, `agreement/`).
- No cheap shortcut was found: the bag-of-words classifiers stay at the majority class (the question-only one picks up some AMBIGUOUS wording). This is weak evidence; the real check is a question-only and a context-only fine-tune.
- A strong prompted model already does well on this synthetic set, and its misses are mostly NOT_PRESENT -> ANSWERABLE. So a trained small model can only show a gain against a small prompted baseline (Qwen2.5-1.5B zero-shot, pending on pc3) and on transfer to real sets. The synthetic test alone cannot carry the claim.
- Caveats: the items were written by Claude agents and judged by Claude models (same family); n = 96 with only 10 AMBIGUOUS; one seed; the missing-item check is a rough keyword match; the judges had the rules in their prompt.

## Next
1. Fix the NOT_PRESENT rule. Finding of 2026-11-26: all 4 Sonnet misses and all 6 Haiku NOT_PRESENT -> ANSWERABLE misses are items whose dropped column is a name column (`doctor_name`, `branch_name`, `item_name`, `supplier_name`) while the table's id stays, so the judge answered with ids. 7 of the 20 NOT_PRESENT test items are such name drops (5 of 40 in train); no item with another dropped column was judged ANSWERABLE by either model. This is a label-rule gap, not only a model miss. In v0.2 never pick a pure output-name column as the dropped column when an id of the same table remains (or label such items ANSWERABLE-by-id), rebuild, and re-judge only the changed items.
2. Qwen2.5-1.5B zero-shot and LoRA runs on pc3 (`PC3_BRIEF.md`).
3. Hand-label 30 items for kappa.
