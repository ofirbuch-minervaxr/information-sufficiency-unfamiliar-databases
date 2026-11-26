# R1 - How the LLM/GenAI course judges projects (course intelligence)

2026-11-26. Scope: LLM/GenAI course only (Vision-robustness guides ignored). Read: the 3 local files + apartsin.com pages as raw text (Moodle is not public). Quoting limit: one verbatim quote only; everything else is paraphrase with a source tag (decoded in section 8) so wording can be checked at the URL.

## 1. Bottom line
1. Reward function: projects are "judged primarily on scientific innovation" [EXP] - a real, identifiable novel element in the problem, data, method or result. Product value is only a floor; engineering serves the science.
2. The instructor's own recipe [K]: a novel task with no ready dataset -> generate synthetic train AND test data -> compare several models, a few fine-tuned vs a few off-the-shelf. Examples: GPT-4o attribute-based data + fine-tuned SBERT / Phi-3 vs pretrained GPT; Stable-Diffusion dog-breed data + fine-tuned CNN / ViT / VLM.
3. Non-negotiable: at least one trained or fine-tuned model (prompt-only fails), a credible baseline, error analysis, fair same-split comparison, a reproducible repo whose numbers match the slides.
4. No weight: API wrappers and single-prompt projects, re-implementations or cosmetic variants, trivial or already-solved problems, invented citations.
5. Changing direction is normal (interim has a what-changed slide); a full topic swap after approval is NOT FOUND in any rule - ask.
6. Your resources fit the course's assumptions: free Colab/Kaggle GPUs; a small OpenRouter budget is usually allocated per project [LLM, GPU].

## 2. The key page, project-requirements [REQ]
| Item | What it says |
|---|---|
| Grading | A build checklist, not the rubric; grading is delegated to the criteria page. 13 core requirements in 4 phases (framing 1-3; research/data/baselines 4-7; evaluation/delivery 8-10; rigor/progress/depth 11-13), each with anti-patterns, plus 6 graduate-only extras. No weights, points, penalties or dates. (Index blurbs say 12 requirements / 5 criteria; the pages list 13 / 6 - trust the pages.) |
| Novelty (Req 4) | Problem or approach needs a significantly novel element: not already solved, meaningfully different from prior solutions, real and identifiable (problem, data, method or application). Weak: re-solving a solved problem, cosmetic re-implementation, no prior-work check, novel title over an off-the-shelf solution, mistaking personal novelty for novelty to the field. [PROP]: no new architecture needed, a strong engineering/experimental contribution counts; API integration alone is not a contribution. |
| Fine-tuning (Req 8) | At least one compared approach must be trained or fine-tuned; zero/few-shot alone is explicitly insufficient. Several non-trivial approaches compared fairly (weak: one model, minor parameter variants, unfair setup, single metric). Echoed in proposal plan [PROP]; midterm: prompt-only is fine as baseline, trained model planned or under way [MID]; final: mandatory, 3+ models incl. trained + zero/few-shot, same data/split/metrics [FIN]. |
| Strong topics (Req 1-3) | Clearly defined, meaningful, preferably unmet need; named users, tangible value, measurable success criteria; evidence from literature/industry/statistics; ML task derived from the need, not from the data at hand; systematic, reproducible data method. |
| Weak topics | Trivial or artificial problem; already well solved without differentiation; opinion or generic-AI-trend motivation without numbers; feature-driven; arbitrary dataset or data that poorly represents the problem; a project that could have been built before the course [MIS]. |
| Progress / depth (Req 12-13) | Steady milestones and acted-on feedback (weak: little after proposal, ignored feedback, last-minute build); depth = decisions you can defend, not pipeline size. |
| Graduate extras | Research-grade contribution, 3+ genuinely different models incl. a recent SOTA method, ablations, repeated runs, arXiv-style report. Whether they apply to you: NOT FOUND. |

## 3. (a) Grading weights and criteria
| Component | Weeks 5/9/13 schedule: undergrad LLM-NLP (HIT), undergrad GenAI-visual (HIT), grad GenAI audio-visual (BIU) [S-UG, S-GU, S-GB] | Weeks 5/8/13 schedule: grad LLM & Agentic AI, grad GenAI VAEs-to-World-Models [S-G, S-GG] |
|---|---|---|
| Proposal | ungraded: feedback + approval only | 10% |
| Interim | 20% | 20% |
| Final talk | 40% | 20% |
| GitHub repo | 40% | 50% |

Your interim/final (~14-18 Dec, ~11-15 Jan, four weeks apart) fit the left column - inference only; which syllabus is yours is NOT FOUND. Team of two is stated only for graduate offerings.

Six assessment criteria [CRIT], sub-weights NOT FOUND: (1) domain understanding: real need, evidence, limits of existing solutions; (2) solution-space exploration: alternatives compared, choices mapped to requirements; (3) novelty + effective reuse: mark what is reused / adapted / new, do not rebuild libraries or infrastructure; (4) rigorous methodology: clean splits, no leakage, suitable baselines/metrics, error analysis, reproducibility; (5) present and defend: visual abstract, concrete input/output datapoints, results-vs-baseline chart, explain model internals, answer questions personally; (6) reasonable effort toward good performance: 100% not required, but show real attempts (more/better data, stronger models, systematic tuning, error-driven iteration). Reviewer bots check the same guides [BOTS].

## 4. (b) Strong vs weak (paraphrased)
| Strong | Weak |
|---|---|
| Novelty that survives a real literature + repo + product search [MIS] | Quick search, cosmetic copy |
| Novel task with no data -> controlled, validated synthetic data (8-point EDA) [K, SYN, EDA] | Bulk unvalidated synthetic data, synthetic-only evaluation, auto-labels trusted blindly [PROP] |
| Fair multi-model comparison, fine-tuned vs off-the-shelf [REQ, FIN] | Prompt-only, one model, random or deliberately weak baseline [MID] |
| Errors grouped by cause with frequency, impact, fix; failures shown [MID, FIN] | Averages only, cherry-picked wins |
| Defensible decisions; every member explains everything [REQ, CRIT, GH] | Big pipeline, slick demo/UI, buzzwords |
| Repo reproducible; same numbers in README, slides, result files [REQ, GH] | Stale or contradictory artifacts, committed secrets |

## 5. (c) Warnings, (d) project types, (e) changes after the proposal
- Integrity: hallucinated references or unverified AI-generated results count as academic-integrity violations (graduate syllabi); every reported result must be backed by runnable artifacts in the repo (all syllabi). AI tools are encouraged if the team owns every claim [S-UG, AI]. Single-prompt work carries no weight [AI]; hours invested are no defense and time-based appeals are rejected [SML]. Never commit keys/tokens [GH]. Numeric penalties and late policy: NOT FOUND.
- Encouraged: the recipe in 1.2 [K, S-UG]. Accepted novelty sources [PROP]: new application, method adapted to a new domain, combined methods, new or relabeled dataset, new evaluation protocol, methods not compared before, gains in quality/efficiency/explainability, end-to-end integration. Past showcased projects [PAST] (55 LLM-related): common pattern is a domain NLP task on noisy text (clinical, support, HR, logs, Hebrew), LLM-generated synthetic data, fine-tuned small encoder vs zero-shot GPT; also some benchmark/evaluation and RAG/agent-security projects. Discouraged: API/RAG-chatbot wrappers without a trained model, replication, a popular model as the contribution, interface-first work [PROP, REQ, FIN].
- Changes: the interim must state what changed; the guide calls changes expected when honestly explained and lists hidden or unexplained changes and keeping an unrealistic scope as things to avoid [MID]. Graduate syllabi: the interim grade rewards sound diagnosis and iteration, even negative results [S-G]. The proposal is the approval gate (graduate: novelty is a hard requirement checked at proposal; re-implementations are not approved). Re-approval rule for a pivot: NOT FOUND. Cost of a pivot: per the kickoff deck the interim needs data generation + EDA + baseline, and the guide adds a 3+ paper table, error analysis and an owner/date/risk/fallback plan - about 2.5 weeks from today.

## 6. (f) Dates
| Milestone | Public site | Calendar |
|---|---|---|
| Proposal | week 5 | NOT FOUND (status of your proposal not verified) |
| Interim | week 9 (week 8 in graduate LLM / HIT graduate GenAI) | ~14-18 Dec 2026 (coordinator) |
| Final | week 13, self-contained talk | ~11-15 Jan 2027 (coordinator) |
| Repo | 1 week after week 13 (grad); end of course (UG); end-of-semester + 2 weeks [K]; weeks 14-15 [WK] | exact date NOT FOUND; roughly 18-29 Jan 2027 (estimate) |

Process: three in-class talks are mandatory [PART]; register team + public repo name in the course registry (Google sheet on Moodle) and upload slides to the repo as PPT + PDF after each talk [PREP].

## 7. (g) Ask the instructor
1. Which grading split applies to us; is our proposal recorded as approved; may we change topic/method before the interim, and by when?
2. Does a new dataset/benchmark + fine-tuned model vs zero-shot baselines count as scientific innovation, or is a new method/finding expected? Is novelty re-checked at the interim?
3. Does a LoRA/QLoRA tune of a small open model on a T4, a fine-tuned encoder, or a trained head on frozen embeddings satisfy the fine-tuning rule? Minimum number of compared models; do the graduate extras apply?
4. Is a validated synthetic-only test set acceptable, or is a small human-verified real test set required (minimum size)?
5. Exact interim/final slots, talk length, repo deadline; is registry + public repo needed before the interim? Size of the OpenRouter allowance?

NOT FOUND: sub-weights per criterion; team vs individual grading; late penalties; exact calendar dates; reviewer-bot internal prompts (GPT pages expose no content); undergrad team size; talk length. Local note: Tasks.txt and Bonus/My letter.txt are teammate hand-offs on slide format and the evaluator bot - no course rules; the ChatGPT link in Tasks.txt was not opened.

## 8. Sources (tags)
K = local kickoff deck E:\Ai conversation task\Proposal Recommendation\1023_ProjectRequirements.pptx - Shortcut (2).pdf; midterm text = E:\Ai conversation task\Project Notes\sources\course\midterm-guide_text_2026-11-26.txt.
Base https://www.apartsin.com/teaching/ : REQ guides/project-requirements.html; CRIT guides/project-assessment-criteria.html; EXP guides/course-expectations.html; MIS guides/common-misconceptions.html; PROP guides/project-proposal-presentation.html; MID guides/midterm-presentation.html; FIN guides/final-presentation.html; GH guides/github-submission.html; SYN guides/synthetic-data-generation.html; EDA guides/eda-for-synthetic-datasets.html; AI guides/how-to-use-ai.html; SML guides/smart-beats-long.html; PREP guides/in-class-presentation-prep.html; PART guides/course-participation.html; WK guides/weekly-project-plan.html; LLM guides/llm-access.html; GPU guides/free-gpu-resources.html; index guides/index.html#section-about-genai-llm-courses and #section-project-standards-genai-llm; BOTS course-bots.html; PAST hands-on-ai-science-courses-student-projects.html (+ .data.js); S-UG large-language-model-nlp-undergraduate-syllabus.html; S-G large-language-models-and-agentic-ai-graduate-syllabus.html; S-GU deep-generative-models-visual-undergraduate-syllabus.html; S-GB deep-generative-models-audio-visual-graduate-syllabus.html; S-GG generative-ai-vaes-to-world-models-graduate-syllabus.html.
Bots (ChatGPT): LLM proposal https://chatgpt.com/g/g-6a68acab3d8c8191a88cc9d056c47b28-llm-course-proposal-reviewer ; LLM midterm https://chatgpt.com/g/g-6a68aec7d7a0819193fc8c0716ec5674-llm-course-midterm-report-reviewer ; GenAI proposal https://chatgpt.com/g/g-6a68b7e79e7881919d6793716ffacd0a-genai-course-proposal-reviewer ; GenAI midterm https://chatgpt.com/g/g-6a68b86a654c8191bebe4514fc2a3e31-genai-course-midterm-reviewer
