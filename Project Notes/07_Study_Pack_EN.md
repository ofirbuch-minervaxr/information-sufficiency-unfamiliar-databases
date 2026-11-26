# Study Pack: Recognizing Sufficiency in Unfamiliar Databases

Ofir Buchshtab and Gilad Kogan · LLM course, Holon Institute of Technology · v0.1, 26 Nov 2026. One page per topic, made for printing. This is the *learning* track: after each page you should be able to explain the topic without notes.

# 1. The project on one page

**The problem.** Someone asks a question about a database they do not know. Before anything is answered or any SQL is written, a system should decide: **is the information it can see enough to answer?** A confident wrong answer is worse than "I need more information".

**What the system sees:** the question, plus the visible context: schema (tables, columns), documentation, keys, and sometimes a few sample rows.

**What it must say (three outcomes):**

| Outcome | Meaning | Example on a shop database |
|---|---|---|
| ANSWERABLE | One clear reading, all needed facts visible | "How many customers live in Haifa?" (`customers.city` exists) |
| AMBIGUOUS | Two or more supported readings with different results; return the top 2 | "Who is our top customer?" (by revenue or by number of orders?) |
| NOT_ANSWERABLE, UNDERSPECIFIED | The column is visible but a needed fact is missing | "How many returned orders?" (`orders.status` has codes 1-5, no document says which code means returned) |
| NOT_ANSWERABLE, NOT_PRESENT | Nothing relevant exists | "How old is each customer?" (no birth date or age anywhere) |

It also returns **what is missing** and a **next action**: answer, ask the user (clarify), request documentation, or abstain.

**The research question.** Does training small open models on synthetic data, built by removing information in a controlled way, improve detection of insufficiency and naming of the missing information, and does it hold on databases the model never saw?

**The three tracks of the work** (they depend on each other):

| Track | What it is | Why it exists |
|---|---|---|
| Practical | The working system: data generator, evaluation code, baselines, fine-tuned model, repository | The course requires a fine-tuned model and a repository |
| Presentation | Interim deck (week 9), final deck (week 13), README | The grade is mostly what we can show and defend |
| Learning | These summaries and the checkpoints | We must explain every choice live, in front of the instructor |

<pagebreak>

# 2. Synthetic data and "ground truth by construction"

**Why synthetic.** No labelled dataset exists for exactly this task, and labelling real databases by hand is slow. Instead we generate data where the right answer is known, because we caused it.

**The recipe**

| Step | What happens | Why |
|---|---|---|
| 1 | An LLM invents a complete database: schema, documentation, sample rows | We know everything that is true |
| 2 | It writes a question and the SQL that answers it; we run the SQL to check that it works | Guarantees the question is answerable on the full database |
| 3 | We **remove one piece of information** in a controlled way and record what was removed | The removal is the experiment |
| 4 | The label follows from what was removed | Ground truth without human labelling |
| 5 | **Necessity test:** the label may change only if the removed piece was *needed* for the question | Otherwise the model is rewarded for noticing edits, not for reasoning |
| 6 | **Control examples:** remove something irrelevant, label stays ANSWERABLE | Stops the model learning "something was removed, so refuse" |
| 7 | Split train / validation / test **by database** | See leakage below |

**Removal to label (summary of `05_Label_Rules.md`)**

| What we do | Label |
|---|---|
| Delete a needed column or table | NOT_ANSWERABLE, NOT_PRESENT |
| Keep the column but remove the document that defines a needed code or meaning | NOT_ANSWERABLE, UNDERSPECIFIED |
| Add a second, similar column (for example `revenue` and `net_revenue`) | AMBIGUOUS |
| Remove something the question does not need | ANSWERABLE (control) |

**Leakage, in plain words.** If the same database appears in training and in test, the model can memorise it and look smart. So the test databases must never appear in training. A second leak: the generator leaves fingerprints (an LLM writes documents in a recognisable style). Controls and a small **real, hand-labelled database** used for testing only guard against that.

**Be able to explain:** why we generate the full database first and then remove information; why a control example is needed; what leakage looks like.

<pagebreak>

# 3. Labels, agreement, metrics and baselines

**Cohen's kappa (do two people label the same way?).** Two annotators label the same 30 examples. Kappa is agreement *beyond what chance would give*. Rough reading: 0.80 or more strong (freeze the rules); 0.60-0.79 usable (fix rules, relabel the disagreements); below 0.60 the labels are too vague (simplify). `agreement/agreement.py` computes it. Why it matters: if two humans cannot agree, a model cannot learn it.

**Why not just accuracy.** If 70% of examples are ANSWERABLE, a model that always says ANSWERABLE scores 70% and never helps anyone. So we use:

| Metric | In plain words | Why |
|---|---|---|
| **macro-F1** | Compute F1 per class, then average with equal weight | A big class cannot hide failure on a small one |
| **false-sufficient rate** (the headline) | Of the cases where information was insufficient, how often the model still said "answerable" | This is the dangerous mistake |
| **over-refusal** | Of the cases where information was enough, how often the model refused | A model that always refuses has false-sufficient 0 but is useless, so report both |
| **missing-info F1** | Does the named missing information match what we removed? | Tests the "name what is missing" claim |
| **calibration (ECE)** | When the model says 80% sure, is it right 80% of the time? Group predictions into confidence bins and compare confidence with accuracy | Verbalised confidence ("I am 90% sure") is weak; we use the probability of the status token instead |

**Baselines (the bar the trained model must beat).**

| Baseline | Why it is there |
|---|---|
| Always "sufficient" | The lazy floor. If the model barely beats it, the task is not learned |
| Prompt-only, zero-shot (Qwen2.5-1.5B-Instruct, Gemma-3-1B-it) | What the small models do with no training |
| Few-shot (a few examples in the prompt) | The fair "prompting" competitor |
| One large prompted model | A reference for how hard the task is |

All on the **same split**. The course guide warns against deliberately weak baselines and against comparing methods on different data.

**Success criteria (proposed, to confirm before running):** +10 macro-F1 over the best prompting baseline, false-sufficient rate at least halved, over-refusal up by no more than 5 points.

<pagebreak>

# 4. Models and fine-tuning

**The models.** Qwen2.5-1.5B-Instruct and Gemma-3-1B-it: small open models (1-1.5 billion parameters) that fit a free Colab T4 GPU (about 16 GB).

**Prompting vs fine-tuning**

| | What changes | Cost | Course status |
|---|---|---|---|
| Zero-shot / few-shot | Only the prompt; weights stay the same | Almost free | Baseline |
| Fine-tuning | The weights are updated on our synthetic examples | GPU time | **Required** in the final system |

**LoRA in one paragraph.** Instead of updating all billions of weights, freeze the base model and train small extra matrices added to some layers (low-rank adapters). That means far fewer trainable numbers, less memory, quick runs, and a small adapter file you can swap in and out. If memory runs out: shorter prompts or QLoRA (the base model stored in 4-bit).

**Training hygiene**

| Item | Rule |
|---|---|
| Splits | Train / validation / test by database; tune on validation, report test once |
| Seeds | Three seeds, report mean and spread. One lucky run proves nothing |
| Output format | Ask for strict JSON (status, reason, missing information, next action); parse it; count unparseable outputs as errors |
| Ablations | Remove one ingredient at a time (for example no controls, no missing-info head) to show what actually helped |
| Overfitting | Training score high, validation low: the model memorised the generator style |

**Be able to explain:** what LoRA changes and what stays frozen; why three seeds; why the fine-tuned model might win on the synthetic test and still fail on the real database.

<pagebreak>

# 5. Related work on one page

Citation counts come from OpenAlex (not Google Scholar) and should be rechecked before the deck.

| Work | What it did | What it leaves for us |
|---|---|---|
| TriageSQL (2020) | Classified unanswerable and ambiguous text-to-SQL questions with RoBERTa, about 60% F1 | Old, weak baseline; no synthetic data, no missing-information naming |
| Know What I Don't Know (ACL Findings 2023) | Created unanswerable examples by **deleting schema columns**, ambiguous ones by adding similar columns | The controlled-removal idea exists; no fine-tuning of small open models |
| AmbiQT (2023), AMBROSIA (2024) | Benchmarks for ambiguous questions | Ambiguity only; not the sufficiency of information |
| PRACTIQ (NAACL 2025) | Edited schemas and values on Spider; best few-shot accuracy 77.4% | Names **fine-tuning open models as future work** |
| ABISS (2026) | 8-category taxonomy, evaluated 8 open models | No training |
| AIR (EMNLP 2026) | Training-free, schema-only; F1 0.679 against IntentRL 0.618 | Prompts big models; no training, no missing-information naming |
| FALCON (AKBC 2026) | Synthetic NL2SQL data, fine-tunes Qwen 1.5B and 3B; its ambiguity filter has 28.6% recall at 98.9% specificity | Generates SQL, not sufficiency; but a very close method, cite it |

**Honest novelty sentence (draft).** Prior work builds unanswerable or ambiguous examples by removing schema information, or prompts large models; we test whether **training small open models** on controlled-removal data improves detection **and naming of the missing information**, and whether this **transfers to unseen and real databases**. The claim is modest and must be checked with a systematic Google Scholar search.

<pagebreak>

# 6. The interim presentation and a self-check

**What the course guide expects (five slides; interim at about week 9, dates to confirm).**

| Slide | Must contain | Where we are |
|---|---|---|
| 1 Project review | Motivation, specification, what changed since the proposal, novelty | Drafted in `01_Honest_Assessment.md` |
| 2 Previous work | At least 3 recent papers in a table (task, method, data, results, limits, relation); what we reuse | 12-paper table in `02_Related_Work.md` |
| 3 Dataset | How the data is generated; **EDA** (class distribution, lengths, types) with interpretation; examples; splits | Nothing yet: needs the pilot |
| 4 Baseline and results | A fair baseline, tables and graphs, **error analysis** | Nothing yet |
| 5 Plan | Table with scope, owner, due date, expected output, **risk and fallback**; last row is the final presentation and repository | Draft in `08_Work_Schedule_EN.md` |

**Things the guide warns against:** repeating the proposal unchanged; graphs with no interpretation; weak baselines; comparing methods on different splits; vague goals such as "improve the model".

**Self-check: answer without notes.**

- What are the three outcomes, and what separates UNDERSPECIFIED from NOT_PRESENT?
- Why is the label known without human annotation?
- What is the necessity test and what does a control example prevent?
- Why split by database?
- Why is accuracy a bad headline, and what are false-sufficient rate and over-refusal?
- Why is "always sufficient" a baseline?
- What does LoRA freeze and what does it train? Why three seeds?
- What exactly is new compared with PRACTIQ and Know What I Don't Know?
- If the model wins on synthetic test data, why is that not yet the result?
