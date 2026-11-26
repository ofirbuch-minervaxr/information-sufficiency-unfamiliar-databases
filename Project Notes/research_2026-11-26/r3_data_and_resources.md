# r3 - Real datasets, "natural removal", existing releases, documentation generation

Checked 2026-11-26 on primary pages (arXiv, GitHub API, Hugging Face API and cards, the local PDFs in `sources/papers/`). Nothing larger than 50 MB was downloaded (sizes come from HEAD requests and the HF/GitHub APIs). "Own count" = computed by streaming the public JSON, nothing saved. **UNVERIFIED** = not confirmed on a primary page.

## 0. Bottom line
1. **Natural removal on BIRD works for NOT_PRESENT and UNDERSPECIFIED, only partly for AMBIGUOUS, and only with a necessity test.** Published net drops from removing the evidence are 8-21 EX points (humans: -20.6), so labelling "evidence removed => UNDERSPECIFIED" blindly would be wrong for roughly 80-90% of questions. Expected yield 10-25% of questions (my inference from those numbers, UNVERIFIED).
2. BIRD gives for free what the synthetic route must generate: real databases (69 train, 11 dev: split by database is natural), human questions, a human-written "missing information" sentence (the evidence), and description CSVs. BIRD and Spider data are CC BY-SA 4.0, so any released derivative must stay share-alike.
3. Biggest pitfalls: annotation noise (49% of Financial dev items noisy; BIRD Mini-Dev flagged 52.8% before correction), evidence that leaks the SQL, contamination, long prompts.
4. Reuse now: `bird_sql_dev_20251106`, corrected Mini-Dev, `mini-interact` (masked-knowledge labels), CLARITY data, TriageSQL / TrustSQL / AmbiQT / AMBROSIA as transfer tests. PRACTIQ = code only. ABISS repo is still "COMING SOON". FALCON and AIR: no release found.
5. **Flag for the novelty sentence:** BAR-SQL (2601.10318, Qwen3-1.7B, SFT+GRPO on synthetic reject/clarify data incl. "dimension definitions removed from schema"), PASCAL (EMNLP 2026 main, "Information Sufficiency Hypothesis", training-free) and LatentRefusal (2601.10398, answerability probe). No published "detect missing -> generate documentation -> re-check" loop found (about 8 searches; absence UNVERIFIED).

## 1. Resource table (real databases and successors)
| Resource | Size | License | URL | Usable for | Main risk |
|---|---|---|---|---|---|
| BIRD train, filtered | 6,601 of 9,428 Q, 69 DBs; jsonl 2.7 MB + `train_column_meaning.json` 0.8 MB; `train.zip` 8.9 GB | CC BY-SA 4.0 | huggingface.co/datasets/birdsql/bird23-train-filtered ; bird-bench.github.io | training pool for evidence/description/column removal, split by DB | contamination, noise, 8.9 GB (E: only) |
| BIRD dev, cleaned 2025-11-06 | 1,534 Q, 11 DBs; json 0.95 MB; `dev.zip` 346 MB; test 1,789 Q / 15 DBs hidden | CC BY-SA 4.0 | huggingface.co/datasets/birdsql/bird_sql_dev_20251106 | real-database test; fields `question, evidence, SQL, difficulty`; per-DB `database_description/*.csv` (original_column_name, column_name, column_description, data_format, value_description: field list confirmed on mirrors and Wretblad, not on the official spec) | public since 2023 |
| BIRD Mini-Dev + corrected "Arcwise-Plat" | 500 Q, 11 DBs; `minidev.zip` 801 MB; corrected 2026-02-21, Mini-Dev refreshed 2026-10-28 | CC BY-SA 4.0 | github.com/bird-bench/mini_dev ; github.com/uiuc-kang-lab/text_to_sql_benchmarks | cleanest subset for the necessity test (fixes SQL, ambiguity, schema) | only 500 Q |
| Spider 1.0 | 10,181 Q, 5,693 SQL, 200 DBs, 138 domains; train 8,659 / dev 1,034 / test hidden; zip ~100 MB UNVERIFIED | data CC BY-SA 4.0 (repo Apache-2.0) | yale-lily.github.io/spider ; github.com/taoyds/spider | column/table deletion (NOT_PRESENT), split by DB | **no documentation** (SEED had to generate it); heavily contaminated |
| Spider-DK / -Syn / -Realistic | 535 pairs (265 modified; 5 knowledge types T1-T5) / Spider-dev based, count UNVERIFIED / 508 | MIT / MIT / not stated | github.com/ygan/Spider-DK ; github.com/ygan/Spider-Syn ; doi.org/10.5281/zenodo.5205322 | hard ANSWERABLE controls (paraphrase, omitted column names, domain knowledge) | answerable only, no unanswerable labels |
| Dr.Spider | 15,269 Q in 17 sets; DB sets: schema-synonym 2,619, schema-abbreviation 2,853, DBcontent-equivalence 382; archive size UNVERIFIED (git-LFS) | Apache-2.0 code, CC BY 4.0 annotations | github.com/awslabs/diagnostic-robustness-text-to-sql | opaque-name controls; abbreviation without docs = UNDERSPECIFIED candidates | answerable by construction |
| Spider 2.0 (lite/snow/dbt) | 632 tasks (547/547/68); ~740-810 columns per DB; **82 tasks (12.97%) ship external docs** | MIT | github.com/xlang-ai/Spider2 | documentation removal, but only 82 tasks | needs BigQuery/Snowflake accounts; DBs too wide for 1B models; Snowflake account suspended 2026-08-12 |
| BIRD-Interact (mini-interact / lite / full) | 300 SQLite tasks, 26 DBs, repo 99 MB / 300 / 600 PostgreSQL; JSON 0.2-0.3 MB | CC BY-SA 4.0 | huggingface.co/datasets/birdsql/mini-interact ; bird-interact.github.io | **ready-made removal labels**: knowledge-base entries masked (`is_mask`, `deleted_knowledge`), `critical` vs `non_critical` ambiguity, clear `query` vs ambiguous `amb_user_query`; 10 experts accepted 95.3% of 300 sampled annotations | small; lite/full gold SQL only by e-mail; DBs benchmark-built |
| LiveSQLBench (base-lite / base-full-v1 / large-v1) | 270 tasks 18 DBs / 600 tasks 22 DBs / 480 tasks 18 DBs; hierarchical knowledge base per DB | CC BY 4.0 or BY-SA 4.0 (cards disagree) | livesqlbench.ai ; huggingface.co/datasets/birdsql/livesqlbench-base-lite | knowledge-base removal; 2025-26 data, less contaminated | gold SQL withheld (e-mail); no ambiguity fields in base set |
| BIRD-History (Findings EMNLP 2026) | 1,393 tasks, 11 DBs (BIRD dev) | CC BY-SA 4.0 | github.com/zjuidg/BIRD-History | per-task `history_knowledge` + SQL clause that needs it = gold "missing information" text | pre-filtered, criterion UNVERIFIED |
| KaggleDBQA | 8 real Kaggle DBs, 272 eval Q (of 400); column descriptions, `db_overview`, value enums | repo LICENSE.md (GitHub: unspecified); paper: DBs redistributable | github.com/Chia-Hsuan-Lee/KaggleDBQA | small real DB with **real documentation** (fits Colab) | 2021; descriptions alone did not help RAT-SQL (13.56 -> 12.43 EM) |
| SynSQL-2.5M | 2.54M samples, 16,583 synthetic DBs; data.json 9.4 GB, databases.zip 54 MB, tables.json 307 MB | Apache-2.0 | huggingface.co/datasets/seeklhy/SynSQL-2.5M | ready-made synthetic DBs (skip LLM database generation) | docs/evidence not confirmed; DBs look small (54 MB zip for 16.6K DBs: inference) |

## 2. Natural-removal feasibility verdict
**Verdict: YES as a real-database test set and a top-up training source; NO as the only training source.** Needs a necessity test on the exact visible context. A hybrid (train on synthetic + natural, test on natural BIRD-dev and one hand-labelled DB) is the credible story.

**Removal -> label** (labels as in `05_Label_Rules.md`)
| Removal on a real DB | Label | Condition | Published effect / yield |
|---|---|---|---|
| Drop the evidence sentence (definition, formula, threshold, term->value) | UNDERSPECIFIED (AMBIGUOUS only if a 2nd supported reading runs and differs) | necessity test passes; value not shown in descriptions/sample rows | net -8 to -21 EX (table below) |
| Drop `column_description` / `value_description` of a column the gold SQL uses | UNDERSPECIFIED | name opaque and rows do not reveal it | all descriptions together: 2-10 EX; at most ~29% of columns are hard enough to need one (27% ambiguity-prone + 2% domain-dependent; reading mine) |
| Drop sample/representative values | UNDERSPECIFIED only if the code is visible nowhere else | necessity test | -2 to -3 EX (CodeS ablation) |
| Drop PK/FK info | UNDERSPECIFIED if the join is not guessable from names | necessity test | <= 0.7 EX: **low yield, skip** |
| Delete the column/table the gold SQL needs | NOT_PRESENT | no other visible column can hold it | ~40% of "unanswerable" candidates are still solvable (ABISS stage 7: 39.6% rejected); TriageSQL ExtKnow F1 0.54 |
| Add a near-duplicate column or drop the doc that separated two similar columns | AMBIGUOUS | executing both readings gives different results | needs an extra "alternative reading" step; or take it from mini-interact / AMBROSIA / AmbiQT |
| Remove something the question does not need | unchanged (control) | - | most single removals fall here |
| Evidence-free questions | ANSWERABLE | 10.2% of dev, 7.2% of train (own count) | natural controls |

**Necessity: how much accuracy depends on the removed item (published)**
| Source (BIRD dev unless noted) | Without -> with evidence (EX) | Net |
|---|---|---|
| BIRD paper Table 2: GPT-4 / ChatGPT / T5-3B | 30.90->46.35 / 24.05->37.22 / 10.37->23.34 | +15.5 / +13.2 / +13.0 |
| same, **human** (test) | 72.37 -> 92.96 | +20.6 |
| SEED Table IV: SFT CodeS-7B / RSL-SQL(GPT-4o) / CHESS(4o-mini) / DAIL-SQL(GPT-4) | 41.92->54.76 / 54.50->65.78 / 54.69->63.04 / 35.46->56.32 | +12.8 / +11.3 / +8.4 / +20.9 |
| AT&T 2025, MiniDev 500, GPT-4o pipeline | 59.6 -> 72.0 (BIRD metadata kept) | +12.4 |
| DIVER 2026 | "over 10%" drop for all sizes; CodeS trained with evidence loses ~15 EX when literal SQL overlap is removed | - |
| ABISS (LLM-generated questions) | 29.4% of evidence-bearing questions rejected: majority of 3 LLMs answered correctly without it | - |
| Other: PASCAL (BIRD-Interact lite) knowledge base closed -> open 44.3 -> 57.3; Spider 2.0 tasks with docs 11.5% vs 26.6% success (not an ablation); DABStep context layer removed 55-77% -> 14-37%; Dr.Spider schema-abbreviation / synonym: about -17.5 / -20.3 EX averaged over 7 models (derived from its Table 3, UNVERIFIED; headline: best model -14.0% overall, worst perturbation -50.7%) | | |

Net drops are lower bounds on the dependent share (some questions flip both ways), and are much smaller than "all questions have evidence" (89.8% do), hence the 10-25% yield estimate once the positive leg (full context must reach the gold) removes another 20-35% (best systems reach 65-78% dev EX).

**Own counts** (evidence strings): dev 1,534 Q: 157 empty (10.2%); 71.1% contain "refers to"; 20.7% formula-like; **21.0% have an SQL string literal that appears only in the evidence**. Train-filtered 6,601 Q: 472 empty (7.2%); 80.5% "refers to"; 14.1% evidence-only literal. Per-DB questions: dev 64-191, train 5-383.

**Pitfalls**
1. **Evidence is question-specific and leaks SQL** (DIVER: "direct literal overlap with the gold SQL"). Removing it tests "hint present", not "documentation insufficient", and the classifier can learn "no evidence line => UNDERSPECIFIED". Fix: pool all evidence of a DB into a deduplicated glossary, remove only the entries a question needs, and delete every duplicate of the same definition.
2. **Necessity test on the same context the classifier sees** (descriptions, sample rows included): positive leg (full context reaches gold, k>=3 samples, majority) and negative leg (removal fails). Items failing the positive leg are unlabelable, not ANSWERABLE.
3. **Noise**: Financial dev 52/106 items noisy (49%), 20.7% wrong gold SQL; Mini-Dev 52.8% flagged (Jin et al. 2026); BIRD itself revised dev on 2025-11-06. Use the cleaned files and drop items where a strong model with full context disagrees with gold.
4. Deletion is not unanswerable (redundant columns); TriageSQL needed decoy columns to stop "incomplete schema" detection.
5. AMBIGUOUS vs UNDERSPECIFIED is the fuzzy boundary (P3 in `01`): label from removal = UNDERSPECIFIED by default; double-label 30 items.
6. Contamination: BIRD/Spider public since 2018/2023; whether Qwen2.5/Gemma-3 saw them is UNVERIFIED. Split by DB; add a newer set (BIRD-Interact, LiveSQLBench, BIRD-History).
7. Size: dev averages about 73 columns per DB (798 over 11); with descriptions a prompt is about 3-5k tokens (my estimate, UNVERIFIED), so prune schema or train with batch 1 on a T4. The SQL check needs the DB files (dev 346 MB is enough for the test side).
8. Cheapest real-DB pick: lowest noise in the published audit = `superhero` (3/20 noisy, n=20 so weak); highest = financial 49%.
9. Cost estimate: 2-4 x N x k calls, about 9-18k calls for N=1,500, k=3 (UNVERIFIED).

## 3. Existing releases (ambiguity / unanswerable line)
| Resource | Public? | Link | License | Size | Split by DB? | Label set | Reuse |
|---|---|---|---|---|---|---|---|
| PRACTIQ (NAACL 2025) | **pipeline only**, archived, no data files (repo 417 KB), needs AWS Bedrock | github.com/amazon-science/conversational-ambiguous-unanswerable-text2sql | LICENSE = CC BY-NC 4.0 (GitHub: unspecified); paper says MIT + Spider CC BY-SA | 2,800 conv. (paper) | UNVERIFIED | 4 ambiguous (SELECT column, values within column, values across columns, vague filter) + 4 unanswerable (nonexistent SELECT column / value / WHERE column, unsupported join) + answerable | copy the 8 edit recipes onto our contexts |
| Know What I Don't Know (2023) | code + `data.zip` (Google Drive) | github.com/wbbeyourself/DTE | none stated | ~23k generated problematic examples (WikiSQL/WTQ) + 3,000 real (release UNVERIFIED); per-split counts UNVERIFIED | not stated; single tables | token tags COL/VAL/AMB/UNK | low (single table); method precedent |
| TriageSQL (2020) | yes | github.com/chatc/TriageSQL | CC BY-SA 4.0 | train 434,236; manual test 2,500 (500/type) | **yes, no schema overlap** | answerable, improper, ambiguous, ExtKnow (1-3 columns deleted), non-SQL | test transfer: ExtKnow -> NOT_PRESENT, ambiguous -> AMBIGUOUS (drop improper, non-SQL); RoBERTa F1: ExtKnow 0.54, ambiguous 0.17, avg 0.60 |
| TrustSQL (2024) | yes | github.com/glee4810/TrustSQL | CC BY 4.0 | ATIS, Advising, EHRSQL, Spider; 18.9K feasible, ~2.5K infeasible each in valid and test; repo 6 MB | Spider standard; infeasible only in valid/test | feasible vs 5 infeasible: column-surface/related/unrelated, non-SQL, ext-know (ambiguity excluded) | NOT_PRESENT test + penalty metric RS(c) |
| AMBROSIA (NeurIPS D&B 2024) | yes, **password-protected** (password on project page; authors ask not to re-host) | ambrosia-benchmark.github.io ; github.com/saparina/ambrosia | CC BY 4.0 | 1,277 ambiguous Q (scope 501, attachment 362, vague 414), 2,965 interpretations, 846 DBs (3-5 rows per table), 16 domains; re-split CSV (test 131 ambiguous + 309 unambiguous per AIR) | UNVERIFIED | ambiguity type + interpretations | AMBIGUOUS source in our schema+rows format |
| AmbiQT (2023) | yes | github.com/testzer0/AmbiQT | MIT | >3,000; 4 types; train + validation | built from Spider | two plausible SQLs | AMBIGUOUS test |
| IntentRL (2025) | code + model | github.com/saparina/intentRL ; huggingface.co/irisaparina/IntentRL-Ambig-Text2SQL-4B | MIT (model card) | Qwen3-4B-Instruct-2507, RL on AMBROSIA train | - | multi-interpretation SQL | fine-tuned baseline for the ambiguity side |
| CoSQL (2019) | yes (test unreleased) | yale-lily.github.io/cosql | CC BY-SA 4.0 | 3,007 dialogues, 200 DBs | **yes** (140/20/40 DBs) | user acts incl. AMBIGUOUS, CANNOT_ANSWER (counts only in a figure: UNVERIFIED) | human-labelled turns on Spider DBs |
| CLARITY (ACL Industry 2026) | **yes** | github.com/duyvuleo/clarity | MIT code, data CC BY-SA 4.0 | 19,268 conv.: Spider 12,098 (140 DBs), BIRD 7,170 (11 DBs); 3 MB | no splits given (group by DB) | ambiguity / "confusion" (unanswerability) settings | extra data on real DBs; no human review stated |
| BAR-SQL / Ent-SQL-Bench (2601.10318) | yes | github.com/TianSongS/BAR-SQL | MIT (LICENSE file not listed) | 1,262 test (README also says 1,218); ~20K SFT set not confirmed | enterprise data, UNVERIFIED | 8 task types (4 SQL, 4 clarify/reject) | recipe + baseline (Qwen3-1.7B 8.5% -> SFT 67.6% -> GRPO 91.5%; unseen-DB protocol UNVERIFIED) |
| ABISS (2607.23340) | **no**: README "COMING SOON" | github.com/giosullutrone/ABISS-... | MIT | 7,145 Q (paper) | - | 8 categories / 13 subcategories | only the paper's recipe (stage 5 necessity) |
| AIR (EMNLP 2026) | no release link (arXiv 2610.24248) | - | paper CC BY 4.0 | - | - | - | prompts only; compare on AMBROSIA / AmbiQT |
| FALCON (AKBC 2026) | no link found (arXiv 2610.03625) | - | - | 5,500 synthetic examples used | - | - | LoRA recipe in paper only |
| Others | AmbiSQL (Apache-2.0, 40 queries); PASCAL code MIT `github.com/authurlord/PASCAL_Release` (training-free); Query Carefully OncoMX-NAQ 80 Q, TACO (1,500 real + 13k synthetic), SOMA-SQL, LatentRefusal: no release link found | | | | | | |

## 4. Documentation / evidence generation, evaluated downstream
| Work | Method | Result (BIRD dev EX) | Headroom / limit |
|---|---|---|---|
| Wretblad et al. 2024 (2408.04691) | LLM column descriptions + expert gold set (11 DBs, 798 columns) | gold vs none +1.8 to +9.7 across 6 LLMs (GPT-4o 30.1 -> 33.3); verbose Qwen2-generated beat gold for all 6 | BIRD's own descriptions "perfect" for 40.2% of columns; LLM judge kappa 0.16-0.25; hard columns need a human |
| Gao & Luo 2025 (Alibaba, 2502.20657, code Apache-2.0) | coarse-to-fine + fine-to-coarse; no evidence used | none 37.8/39.1/31.9 -> generated 39.4/39.5/32.7 -> manual 40.2/41.1/34.5 (3 generators) | closes 37-40% of the manual gap, about 1.4 EX left |
| Shkapenyuk et al. 2025 (AT&T, 2505.19988) | profiling + LLM summaries (+ query log, SQL-to-text) | MiniDev, GPT-4o, no hints: none 49.8 / BIRD 59.6 / profiling 61.2 / fused 63.2; hints on: 72.0 / 72.6 / 73.0 | profiling beats human descriptions; hints still add 10-12 |
| SEED 2025 (2506.07423) | evidence from schema, descriptions, executed sample SQL | CodeS-15B 44.4 / 55.4 (human) / 56.8 (SEED); CHESS 54.7 / 63.0 / 56.3; DAIL-SQL 35.5 / 56.3 / 51.6 | closes 19-78% of the gap for GPT pipelines, >100% for SFT CodeS |
| Companion Agents (2601.08838), DIVER (2602.12064) | mine table info / probe DB, build evidence | evidence fully missing: +4.4 to +14.1 / up to +10.8 | - |

**Reading:** on BIRD, generated descriptions are worth about 1-3 EX, generated evidence 5-15. **Loop "detect missing -> generate -> re-check": not found.** Nearest: Wretblad (generate, then expert review of hard columns), PASCAL (diagnose five gap classes, then acquire from schema/knowledge base/user, training-free, no documentation writing), APEX-SQL (2602.16720, hypothesis -> verify by exploratory SQL), SEED/DIVER/Companion (generate without a detection step).

## 5. What to reuse (order)
1. Test side: `bird_sql_dev_20251106` plus corrected Mini-Dev, necessity-tested; one low-noise dev DB hand-labelled; `mini-interact` for masked-knowledge and intent ambiguity; TriageSQL/TrustSQL/AmbiQT/AMBROSIA as out-of-distribution transfer.
2. Train side: synthetic (SynSQL DBs or your own) + BIRD-train removal examples (about 650-1,650 UNDERSPECIFIED candidates from 6,601 Q if the 10-25% yield estimate holds) + CLARITY for ambiguity.
3. Baselines: IntentRL (Qwen3-4B), BAR-SQL recipe; prompt-only large model.
4. Gold "missing information" text: the evidence sentence or BIRD-History `history_knowledge`.

## 6. UNVERIFIED list
Spider zip size and test size; Spider-Syn count; Dr.Spider archive size; KWIDK per-split counts, real-set release, licence; PRACTIQ DB-split; CoSQL act counts; BIRD-Interact DB count and gold-SQL gating for mini-interact; BAR-SQL unseen-DB protocol and SFT-set release; contamination of Qwen/Gemma; yield, token-length and cost estimates; absence of the "detect-generate-re-check" loop. Search queries used generic topic terms only (one contained the phrase "information sufficiency").
