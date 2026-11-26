# R2. Sufficiency, abstention and missing-information literature, plus kill-risk search (checked 2026-11-26)

**Key.** **V** = primary page opened this session (arXiv, ACL Anthology, GitHub, OpenAlex). Numbers were pulled from page text by a fetch tool: re-check before a slide. **UNVERIFIED** = snippet, mirror or unreadable PDF only. No venue = arXiv preprint.
**Coverage.** About 45 web searches (about 30 aimed straight at idea A, 10+ phrasings: removal / deletion / counterfactual; unanswerable / abstain / refuse; sufficiency / missing information; LoRA / small model; GitHub / HuggingFace; KBQA, table-QA, data-agent, tool-call analogues) plus OpenAlex cited-by scans: KWIDK 65 citing works since 2025 (60 title-scanned), PRACTIQ about 45, Sufficient Context 128 since mid-2025 (newest 40 title-scanned).

## 1. Bottom line

1. **Kill-risk: partial overlap, not a kill.** Nothing found does all five of: (a) controlled-removal synthetic data, label by construction; (b) LoRA fine-tune of a <=2B open model; (c) database context (schema + docs/keys/samples); (d) output names the missing information; (e) tests transfer to unseen or real databases. Nearest, **BAR-SQL** (row D1), has (a), (d), a 1.7B model, but tests only on a slice of its own generator.
2. "We train a small sufficiency judge" is **not novel as a method** (same recipe works in tool use, math, RAG). Still defensible: **transfer to unseen and human-labelled databases, artifact controls, exact-match scoring of the named missing element.**
3. Strongest evidence against A: edit artifacts (a scorer blind to the reasoning chain gets AUC .997), fragile transfer (fine-tuned SQL verifiers .78 AUROC in-distribution, about .66 on unseen schemas), prompted GPT-4o already filters 72-100% of infeasible questions (mostly >90%) in TrustSQL.
4. Sufficient Context is text-only; no sufficiency autorater for tables or databases exists (closest: TCR-Bench). No published LoRA-tuned <=2B sufficiency judge found; a prompted Qwen2.5-1.5B judge is at chance (.540), so there is headroom.
5. Recommendation: keep A, re-scoped as **Alt 1** (section 4); make the transfer gap the headline.

## 2. Papers

### A. Sufficient context (RAG) and follow-ups

| Paper | Year / venue | What they did, key numbers | URL |
|---|---|---|---|
| Joren et al., Sufficient Context | ICLR 2025 (poster); arXiv v3 Apr 2025 (V) | LLM autorater for whether the context is sufficient to answer; Gemini-1.5-Pro 1-shot acc .930 / F1 .935 on 115 human labels (FLAMe, fine-tuned PaLM-24B: .878 / .892; TRUE-NLI, T5-11B: .826 / .818). FreshQA / Musique / HotPotQA, sufficient share about 77 / 45 / 44 %. Selective generation (logistic regression on sufficiency + self-rated confidence): +2-10 pts correct-among-answered at equal coverage. Gemma wrong answers 10.2% (no context) to 66.1% (insufficient). LoRA Mistral-7B toward "I don't know": abstains <=2.2%, hallucinates 57-76%. **No inter-annotator agreement.** Repo = prompts + README only | arxiv.org/abs/2411.06037; github.com/hljoren/sufficientcontext |
| RINSE (Chen, Hua, Xiao) | Sep 2026, 2609.37469 (V) | Pre-generation sufficiency from question + passages; paired benchmark by substitution / deletion / question swap. Small heads + frozen Qwen2.5-1.5B probe: pairwise .837 vs Joren prompt on an API frontier model .784 and on Qwen2.5-1.5B **.540** (chance .5). 12 generators answer 40-99% of insufficient questions despite an abstain instruction. Evidence-only classifier still .743 (residual cue). No code found | arxiv.org/abs/2609.37469 |
| Knowing What's Missing (Jain, Garimella) | EACL Findings 2026, 2512.06476 (V) | Llama-3.1-8B names what is missing, GPT-4o checks it is absent; prompting only; labels by removing supporting passages. MuSiQue-Ans 71.9 vs autorater 64.9; Llama-8B as verifier drops to 59.2 | arxiv.org/abs/2512.06476 |
| SURE-RAG; GRAB-RAG; CLADE | 2605.03534; AACL 2026 main 2608.22228; 2611.14355 (V) | SURE-RAG verifier Macro-F1 .908 vs GPT-4o .728 on controlled HotpotQA-RAG, but unsafe-F1 .334 vs .739 on HaluBench (no transfer). GRAB-RAG: frozen 3.8-8B models still answer 41.6% of misleading cases despite an abstain prompt (missing evidence is handled). CLADE: too-coarse evidence cuts abstention 13.8 pts | arxiv.org/abs/2605.03534 |
| TCR-Bench | Jul 2026, 2607.17742 (V) | Only table-sufficiency item found: dense retrievers 18.2% top-1 target, QA F1 .755 (oracle) to .330; fine-tuned answerability is learnable but transfers poorly | arxiv.org/abs/2607.17742 |
| ChainCheck; Better Retrievers, Worse Labels | Nov / Oct 2026, 2611.11965; 2610.40966 (V) | Label audits: chain-blind scorer AUC .997 on edit-built sufficiency pairs; treating no-gold-document contexts as unanswerable has precision .68 falling to .10 | arxiv.org/abs/2611.11965 |

Also seen: Certify (2610.34684, abstention that names open requirements, training-free); TRIO (Findings EMNLP 2026, 2611.02810, SFT judge agent, sizes UNVERIFIED). **Open after Joren:** databases / tables; a trained small judge; label reliability; graded rather than binary sufficiency (authors' own future work).

### B. Missing information, clarification, next action (any domain)

| Paper | Year / venue | What they did, key numbers, evaluation | URL |
|---|---|---|---|
| QuestBench | NeurIPS 2025 D&B, 2503.22674 (V) | One missing variable; pick the right clarifying question; about 40-50% on Logic-Q / Planning-Q; exact-choice metric, no judge | arxiv.org/abs/2503.22674 |
| When2Call | NAACL 2025, 2504.18851 (V) | 4-way: answer / tool call / follow-up / unable; Mixtral rewrites BFCL items (drops one required parameter). Test 3,652; train 6k SFT / 10.5k preference. 4B F1 29.7 to 48.1 (SFT) to 51.0 (preference); Qwen2.5-1.5B baseline 29.9; GPT-4o 61.3. Labels only spot-checked (question quality 82%) | github.com/NVIDIA/When2Call |
| AskToAct | 2503.01940; EMNLP listing UNVERIFIED (V) | Removes parameters from xlam queries (removed value = truth); Qwen2.5-7B LoRA / full SFT; unseen-API test (TaskBench-IC 984). Clarification efficiency 55.3 to 63.4 / 68.1, GPT-4o 74.5. LLM-simulated user + 3-person human study | arxiv.org/abs/2503.01940 |
| RL clarifiers: SAGE-Agent; Abstain-R1; CLARITI; CIGAsk | Findings ACL 2026 (V); ACL 2026, 2026-04, EMNLP 2026 Findings (abstracts only) | SAGE-Agent GRPO 3B / 7B: When2Call acc 36.5 to 65.2 / 36.7 to 62.9, 1.5-2.7x fewer questions (simulated users). Abstain-R1 3B reported competitive with DeepSeek-R1 on unanswerable queries; CLARITI 8B about GPT-5 with 41% fewer questions; judges and data builds UNVERIFIED | aclanthology.org/2026.findings-acl.2028 |
| SUM (Hallucination Tax of RFT) | EMNLP Findings 2025, 2505.13988 (V) | o3-mini deletes key info from DeepScaleR problems; 2 authors checked 300 samples (kappa .52). 10% SUM in RL: refusal .01 to .81 (math), .01 to .94 on SelfAware (out-of-domain), Qwen2.5-7B; Qwen2.5-Math-1.5B barely moves (.00 to .04) | arxiv.org/abs/2505.13988 |
| LHAW; AbstentionBench; Ambig-DS | 2602.10525; NeurIPS 2025 D&B; 2605.09698 (V) | LHAW removes goals / constraints / inputs / context and validates labels by agent trials (outcome-critical vs benign), 285 variants. AbstentionBench: reasoning fine-tuning cuts abstention 24%, scale barely helps. Ambig-DS: agents cannot tell when to ask | arxiv.org/abs/2602.10525 |

**Naming the missing info is evaluated by:** exact choice vs truth (QuestBench), log-prob choice + LLM judge (When2Call), simulated user + tiny human study (AskToAct, SAGE), GPT-4o judge (BAR-SQL), agent trials (LHAW). Removal-based labels allow exact element match with no judge.

### C. Text-to-SQL selective prediction

| Paper | Year / venue | What they did, key numbers | URL |
|---|---|---|---|
| TrustSQL | 2403.15879, "under review", venue UNVERIFIED (V) | ATIS / Advising / EHRSQL / Spider, about 21.4k questions. RS(c): +1 correct answer or correct abstain, 0 abstain on feasible, -c wrong SQL or SQL on infeasible; c in {0, 10, N}. Abstain-all = 50.0; best RS(10) 45.8-51.4 (about abstain-all). Fine-tuned SQLCoder-7B infeasible detector (trained on TriageSQL) filters less than prompted GPT-4o (Spider non-sql 26% vs 91%) | arxiv.org/abs/2403.15879 |
| EHRSQL 2024 shared task | ClinicalNLP 2024, 2405.06673 (V) | Unanswerable 8.8% train / 20% test. RS(10): LG AI + KAIST 81.3 (self-training on pseudo-labelled unanswerables), abstain-all 20; nobody positive at RS(N). Unanswerables are often detectable from n-grams alone (2405.01588) | arxiv.org/abs/2405.06673 |
| RTS | SIGMOD 2025, 2501.10858 (V) | Conformal branching-point probe on fine-tuned DeepSeek-7B; AUC 97.2 / 96.7; false-abstain about 13%; no risk-coverage or penalty metric, no prompting baseline | arxiv.org/abs/2501.10858 |
| What Predicts Correctness; Know When to Abstain | Jul / Nov 2026, 2607.06799; 2611.31190 (V) | LLM-judge ensemble AUROC .82, answers 27% at 24% risk; **fine-tuned verifiers (incl. 7B) .77-.79 in-distribution, about .66 on unseen schemas**. Conformal random forest: Spider AUARC .899, BIRD AUROC .72 vs .79, risk guarantee does not transfer | arxiv.org/abs/2607.06799 |
| LatentRefusal | Findings ACL 2026, 2601.10398 (V) | Probe on frozen Llama-3.1-8B / Qwen3-8B; F1 88.5 / 88.8 (TriageSQL, AMBROSIA, SQuAD2, internal); about 300 training samples, trained per dataset; prompted DeepSeek-Chat 83.2; authors list cross-domain generalisation as a limitation; score only, no naming | aclanthology.org/2026.findings-acl.1007 |
| SQD; Query Carefully; SCARE | COLING 2025; 2512.21345; ML4H 2025, 2511.17559 (V) | SQD: schema-relevance predictor on EHR (details UNVERIFIED). Query Carefully: prompted Llama-3.3-70B, near-perfect for missing column / non-SQL / out-of-domain, 0.5 missing value, 0.3 column ambiguity. SCARE: 4,200 human-verified items, 3 EHR DBs (kappa .86-.91); Gemini-2.5-Flash ambiguous F1 only 46-54, unanswerable 72-81; data on GitHub | arxiv.org/abs/2511.17559 |

**Trained abstainer vs prompting?** No clean head-to-head under risk-coverage. Trained wins are in-distribution (EHRSQL winners, LatentRefusal per dataset, BAR-SQL). Across schemas it reverses: fine-tuned verifiers lose about 12 AUROC points and TrustSQL's transfer-trained 7B detector trails prompted GPT-4o. Small-model points: DeepSeek-7B (RTS), Qwen3-1.7B (BAR-SQL), frozen Qwen2.5-1.5B (RINSE).

### D. Closest hits to idea A

| Item | Year / venue | What it is and the gap | URL |
|---|---|---|---|
| **D1 BAR-SQL** | 2601.10318, Jan 2026 (V, method read) | Seed Mutation deletes schema dimensions (e.g. series_name), makes questions vague, uses undefined metrics; target text names the missing item; about 20k synthetic items; Qwen3-1.7B full-parameter SFT then GRPO (not LoRA). **Gap (e):** Ent-SQL-Bench = 1,262 items from the same generator, GPT-4o judge, apparently one car-sales enterprise domain (database count not reported), no Spider / BIRD / unseen-DB test. 91.5% vs Claude-4.5-Sonnet 48.0, GPT-5 46.0, but prompted baselines score 0-19% on ambiguity / dimension rejection with undisclosed prompts (likely unfair baseline) | arxiv.org/abs/2601.10318; github.com/TianSongS/BAR-SQL |
| D2 Shakespeare-SQL ("To RAG or Not to RAG") | IEEE Access 2026 (DOI from OpenAlex); authors UNVERIFIED | Fine-tuned DeBERTa-v3-base router (answerable / ambiguous / unanswerable) + RAG + LoRA Llama-3.1-8B validator (GRPO); Ambrosia+ adds 2,535 unanswerable questions. Classifies, does not name missing info (per README). Reported 73.0% vs 30.5% coverage UNVERIFIED | github.com/miahoang/shakespeare-sql |
| D3 abstain-sql; ABSTRAIN-SQL | GitHub, Nov 2026, in progress (V) | 480 synthetic DB designs, 13,440 questions (29% to decline), GRPO abstention reward + Learn-then-Test; README says training has not started, no results. Second repo: Qwen3-4B GRPO, no results. A rival could post before 11-15 Jan | github.com/amandipd/abstain-sql |
| D4 External tests, adjacent work | various | PremiseSQL (2610.22158; 1,800 flawed + 1,800 original, prompting only, data distributed separately); ARCS (2610.09396; real DBs, 311 tasks, no open model above 27% EX; HF mirror UNVERIFIED); CLARITY (ACL Industry 2026), SQUAB (EMNLP 2025); When the Bottleneck Shifts (EMNLP 2026 main) already uses the term Information Sufficiency Hypothesis (training-free agent); AAU thesis "Schema Guided Abstention" (PDF unreadable, UNVERIFIED). PRACTIQ ships a generation pipeline on Spider; a ready download is UNVERIFIED | arxiv.org/abs/2610.09396 |

## 3. Kill-risk verdict

**No full match after about 45 searches and the cited-by scans.** Pieces exist: BAR-SQL for (a)+(d)+small model; LatentRefusal / SQD for small trained detectors without naming; AskToAct, When2Call, SUM, LHAW, Knowing What's Missing for the same recipe outside databases. Nothing tests transfer from synthetic removal data to human-labelled databases.
**Novelty sentence, only if still true at submission (re-scan in early January):** "As of 26 Nov 2026 we know of no published work that fine-tunes a <=2B model with LoRA on controlled-removal synthetic database contexts to output a sufficiency label and the missing elements, and tests transfer to unseen synthetic domains and human-labelled external sets. Closest: BAR-SQL (in-distribution, apparently one enterprise domain)."

**Evidence against A**
- *Artifacts:* ChainCheck, EHRSQL n-grams, RINSE's .743 show a classifier can learn "this context looks edited". Needs paired controls (same removal, question that does not need the element) and question-blind / context-blind baselines.
- *Transfer:* .78 to .66 on unseen schemas; LatentRefusal and TCR-Bench report weak transfer. A negative transfer result is plausible.
- *Ceiling:* in-distribution scores will sit near 100% (BAR-SQL 91%, SUM .81-.99), so they are not a result. Large prompted LLMs catch absent columns, but not ambiguity vs missing value (0.3-0.5; SCARE ambiguous F1 46-54; and from team notes PRACTIQ best 77%, ABISS 59-70%): hard classes are where to look.
- *Labels:* a removed column may be redundant or unneeded (LHAW tests outcome-critical vs benign); SUM kappa .52; When2Call question quality 82%; Joren no agreement. High-agreement human sets exist (SCARE .86-.91), so a 100-item audit with kappa is feasible.
- *Tiny models:* the 1.5B math model did not respond at 10% mixture; prompted 1.5B judges sit at chance; prompting and scale do not fix abstention (AbstentionBench, GRAB-RAG).

**Evidence for A:** the recipe works at 3B-8B and transfers across tasks (SUM math to factual QA; AskToAct unseen APIs); When2Call small models go from about 30 to 48-51 F1 with synthetic data; prompted small judges are at chance, so a trained 1.5B has headroom; SCARE and ARCS offer human-labelled external sets.

## 4. Alternatives

**Alt 1 (refined A, recommended): transfer-first sufficiency judge, controlled labels, downstream test.** 40+ synthetic databases, 8+ domains; removal operators (column, table, join key, definition text, sample-row value, near-duplicate rename); label by rule from the gold SQL (referenced element absent = NOT_PRESENT + element list; two candidates = AMBIGUOUS; else ANSWERABLE); paired controls; execution check; 100-item human audit with kappa. LoRA Qwen2.5-1.5B and Gemma-3-1B emit {label, missing[]}; score label F1, exact-set match of missing elements, risk-coverage, RS(c). Splits: leave-domain-out, leave-removal-type-out, then SCARE, TrustSQL-Spider, ARCS. Downstream: gate a SQL generator, report selective accuracy at fixed coverage (Joren protocol). Baselines: same base model prompted with the identical output format, API model on a sample, question-blind and n-gram classifiers, abstain-all.
*Why it can show results:* big in-distribution gains are near-certain; the transfer gap is a measurable, honest result either way. *Fails if:* artifacts inflate scores, transfer collapses (still reportable), 2-6k-token contexts strain the T4. *Closest:* BAR-SQL, KWIDK, PRACTIQ, RINSE, Joren, TrustSQL.

**Alt 2: execution-labelled abstainer for text-to-SQL, cross-schema.** LoRA 1.5B verifier on (question, schema, generated SQL) predicts correctness; train on Spider, test on BIRD dev; AUROC, AUARC, risk at fixed coverage, RS(10); baselines self-consistency, log-prob, prompted 1.5B and API judge, abstain-all.
*Why:* objective labels, standard metrics, numbers to beat (about .66 unseen; BIRD .72). *Fails if:* AUROC stays .7-.8 (modest win), small generators too weak, API cost for generator outputs, crowded (RTS, 2607.06799, 2611.31190, abstain-sql). *Closest:* TrustSQL, RTS, 2607.06799, LatentRefusal.

**Alt 3: ask-or-act on missing parameters, public data, held-out-domain test (safe fallback).** When2Call train (6k / 10.5k) and test (3,652) or AskToAct-style removal on xlam; LoRA 1.5B; SFT vs preference; exact match of the named missing parameter; extra test on database-query tools or held-out tools.
*Why:* no data-generation risk; published baselines (Qwen2.5-1.5B 29.9 F1, 4B 51.0, GPT-4o 61.3). *Fails if:* crowded (AskToAct, SAGE-Agent, When2Call), weak database angle, scoring quirks (4B: 51.0 multiple-choice vs 64.3 LLM judge), noisy synthetic labels. *Closest:* When2Call, AskToAct, SAGE-Agent.

**Plan:** Alt 1 as the main line; keep Alt 3 as a one-week fallback if data generation slips before the 14-18 Dec interim. Minimum to show then: base vs LoRA in-distribution, one leave-domain-out number, one artifact baseline.

## 5. Caveats

UNVERIFIED items are marked inline. Several pages could not be read (COLING PDF body, AAU thesis, ResearchGate, IEEE, Georgia Tech mirror); only abstracts or snippets were used. A third-party "Suffice" results page was excluded (provisional, internally inconsistent). OpenAlex responses carried a notice inviting an API-key signup with an email address: ignored, nothing sent.
