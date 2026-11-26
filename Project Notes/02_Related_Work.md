# Related work (checked 2026-11-26)

Citation counts are from **OpenAlex**. Google Scholar numbers are usually higher: re-check on Scholar before putting them on a slide. The 2026 papers are too new to have citations.
Depth: **F** = read parts of the full text, **A** = abstract only.

| # | Paper (venue, year) | Cites | Task | Method / data | Result | What it means for us | Depth |
|---|---|---|---|---|---|---|---|
| 1 | **Know What I Don't Know** (Wang et al.; ACL Findings 2023) | 79 | Detect, localise and explain ambiguous/unanswerable text-to-SQL questions | Counterfactuals: delete a schema column for unanswerable; delete it and add two similar columns for ambiguous; WikiSQL/WTQ; weakly supervised DTE tagger | Best on real and generated examples (abstract) | Closest precedent for "remove information, get a label". Single table, column level, encoder tagger. No documentation/keys/samples, no LoRA LLM. | F |
| 2 | **PRACTIQ** (Dong et al.; NAACL 2025) | 45 | Conversational text-to-SQL with 4 ambiguous + 4 unanswerable categories | Programmatic schema/value edits of Spider dev + LLM, ~2,800 conversations; 9-way category classification + SQL | Best few-shot: Claude 3.5 Sonnet, 77.4% | Closest benchmark. **Authors name fine-tuning open models as future work: our gap.** | F |
| 3 | TriageSQL (Zhang et al.; arXiv 2020) | 30 | Classify answerable vs 4 unanswerable types, cross-domain | RoBERTa on Spider-derived data | 60% F1 | Early trained-classifier precedent; cross-domain is hard | A |
| 4 | AMBROSIA (Saparina & Lapata; arXiv 2024) | 77 | Ambiguity benchmark: scope, attachment, vagueness | Databases generated from scratch so the ambiguity persists; interpretations + SQL | Even the best LLMs struggle | Supports generating databases from scratch; execution-based interpretations | A |
| 5 | AmbiQT (Bhaskar et al.; EMNLP 2023) | 99 | 3,000+ questions with two plausible SQLs | Lexical and structural ambiguity | benchmark | Standard ambiguity benchmark; possible transfer test | A |
| 6 | Disambiguate First, Parse Later (Saparina & Lapata; ACL Findings 2025) | 30 | Interpretations before SQL | Infilling model trained with execution-validated annotation | Better interpretation coverage | Execution validates meanings: supports our ambiguity rule | A |
| 7 | Reliable Text-to-SQL with Adaptive Abstention, "RTS" (ACM, DOI 10.1145/3709719, 2025) | 47 | Abstain or ask a human when context is insufficient | Conformal "branching point" prediction at schema linking; BIRD | More reliable | Abstention precedent; metric ideas | A |
| 8 | TrustSQL (arXiv 2024) | 38 | Reliability: answer feasible questions, abstain on infeasible ones | Penalty-based scoring | benchmark | Metric design: penalise a wrong answer more than an abstention | A |
| 9 | **ABISS** (Sullutrone et al.; arXiv 2607.23340, Jul 2026) | 0 | Classify ambiguous/unanswerable questions, clarify, give feedback | 8-category taxonomy; 10-stage council-validated generation from any seed database; interactive simulation; 8 open models, 7B-122B | Recognition 70.5% vs classification 59.1% (Nemotron, ABISS-BIRD) | Evaluation, not training. Its "Evidence Necessity" stage removes evidence to test that it is needed: removal used for validation. | F |
| 10 | **AIR** (Yin et al., Capital One; EMNLP 2026 main, paper 2446) | 0 | Resolve ambiguity | Training-free: anchor + adversary agents; execution proves the readings differ; **schema-only context** | AMBROSIA F1 0.679 vs IntentRL 0.618; 1.76 vs 5.00 outputs per query | Schema-only plus several interpretations is already studied. Its "extensional ambiguity" is our rule. | F |
| 11 | **FALCON** (Lee et al., UCSC/Adobe; AKBC 2026) | 0 | Ambiguity-aware synthetic NL-to-SQL data | SQL-then-NL, persona seeding, alignment filter, alternative SQL for ambiguous questions; fine-tunes Qwen2.5-3B/1.5B (LoRA r16, alpha 32, lr 2e-4, 2-3 epochs, 5.5k examples) | Tested on Spider test | Same small Qwen models and a usable LoRA recipe. SQL generation, not sufficiency. | F |
| 12 | SchemaBridge (arXiv 2611.17044, Nov 2026) | 0 | Design schemas from text; describe schemas | 902 schemata; fidelity per element | Human requirements under-specify schemas (no model above 0.27 referential F1) | Evidence that missing information is real and measurable | A |

Full abstracts and counts: `sources/literature_metadata_2026-11-26.txt`. PDFs: `sources/papers/` (rows 1, 2, 9, 10, 11).

## Suggested rows for interim slide 2
The course wants 3 or more papers, recent and well cited. Candidates: KWIDK (79), PRACTIQ (45), AMBROSIA (77), RTS (47), plus ABISS, AIR and FALCON as the 2026 papers.
The guide also asks: which methods we reuse, which baselines, which datasets and metrics are standard, and which limitation we address (see `03_Interim_Plan.md`).

## Close the gap yourselves (this is also required reading)
On Google Scholar, newest first, scan titles from 2025-2026:
1. "Cited by" of KWIDK and of PRACTIQ. This is the best trick: later work that does what we plan shows up there.
2. `"text-to-SQL" "unanswerable" fine-tuned "small language model" synthetic`
3. `"information sufficiency" OR "answerability" database schema LLM "missing information"`
4. `undocumented database LLM question answering "insufficient" metadata clarification`

Write down any paper that trains a small LLM on synthetic data to judge sufficiency. If one exists, the novelty sentence in `01_Honest_Assessment.md` section 4 must change.

## Reading split (proposed, so each of you learns the field)
Ofir: KWIDK, PRACTIQ, ABISS. Gilad: AMBROSIA, AIR, FALCON.
Each writes 5 lines: task, data, method, result, what it leaves open. Swap and discuss.
