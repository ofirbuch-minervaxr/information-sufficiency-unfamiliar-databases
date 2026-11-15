# Draft text for slides 6-8 (Proposal) - copy bullets into the pptx

Source: course requirements PDF (Proposal = 5 slides), project facts from slides 2-3, models/pipeline from `Model and Pipelines/`.
Items marked **[CONFIRM]** are my proposals - you and Gilad decide.

---

## Slide 6 - Models & Methods
*(requirement: processing flow, models per step, adjustments / fine-tuning)*

**Pipeline** (use `Model and Pipelines/mermaid-diagram.png`, split in two images like on slide 6):
- Part A - Data generation: domain -> full database -> validate -> questions with known answers -> incomplete views -> sufficiency label -> structured expected response -> validate -> filter -> split by database
- Part B - Experiments: train/val/test -> zero-shot / few-shot / fine-tuning -> evaluate + error analysis

**Models compared**
- Off-the-shelf (zero-shot + few-shot): Qwen2.5-1.5B-Instruct, Gemma-3-1b-it
- Fine-tuned on synthetic data: same two models with LoRA **[CONFIRM: add a large API model as an upper-bound reference?]**
- A strong LLM is used only as the data generator / label validator, not as a compared model

**Adjustments**
- Prompt: one fixed template (schema + metadata + sample records + question), JSON-only output
- LoRA fine-tuning on structured responses (decision, missing information, explanation, next action) - see `Fine-tuning, What is LoRA.jpg`
- Few-shot: k examples, one per status

---

## Slide 7 - Data Specification & Generation
*(requirement: data requirements, dataset, labeling, synthetic data and how)*

**Requirement:** no public dataset has "is the information enough to answer?" labels -> we generate it.

**Each example =** database context (schema, metadata, sample records) + user question -> label (sufficient / ambiguous / insufficient context / unanswerable) + missing information + explanation + next action

**How we generate (key idea):**
1. Generate a complete, validated database in a chosen domain
2. Generate questions whose answers are known from the full database
3. Create *incomplete views* (remove column descriptions, keys, tables, sample rows, or add misleading names)
4. The label follows from what was removed: answer still derivable = sufficient; several valid readings = ambiguous; needed context removed = insufficient context; data not in the database at all = unanswerable
5. Validate (SQL runs, answers match, labels consistent), filter, **split by database** so test databases are never seen in training

**Size [CONFIRM]:** ~10 domains, ~100 databases, ~25 questions per database -> ~2,500 examples, split ~70/15/15 by database

---

## Slide 8 - Metrics & KPIs
*(requirement: how we measure, quality per step, metrics, protocol, ground truth)*

**Ground truth:** known by construction (we know exactly what was removed), plus a manually checked sample **[CONFIRM sample size, e.g. 100]**

**Main task - sufficiency classification**
- Accuracy and macro-F1 over the 4 statuses, confusion matrix
- **False-sufficient rate** = model answers when it should have said insufficient/unanswerable (the hallucination risk; our headline KPI)

**Output quality**
- Missing-information: precision / recall against the removed items
- Explanation and next action: rubric score from an LLM judge, spot-checked by hand
- JSON validity rate

**Secondary tasks:** SQL execution accuracy, database-explanation quality (judge)

**Data pipeline quality:** % examples removed by each validation step, label agreement between validator and manual check

**Protocol:** test on unseen databases (and one held-out domain), 3 seeds, same prompt for all models, results as table + confusion matrices

---

## Open points for the team
1. Slides 4 and 5 are titled "Novelty - July 25, 2026 / November 12, 2026" and are empty. Per the requirements, novelty belongs inside slide 2 (task description). Fill them (what exists today vs. what is new: synthetic training for sufficiency detection) or merge into slide 3 and delete them.
2. Proposal format is 5 content slides; current deck has 7. Check with Menachem whether 5 is a hard limit.
3. Paste the ChatGPT bot answer (link in Tasks.txt) - I will align this draft with it.
