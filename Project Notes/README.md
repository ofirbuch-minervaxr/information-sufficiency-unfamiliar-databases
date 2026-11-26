# Project Notes (local only)

Working notes for *Recognizing Sufficiency in Unfamiliar Databases* (Gilad Kogan and Ofir Buchshtab). Created 2026-11-26.
Shared with Gilad on a GitHub branch (the repo is public, so everything here is visible). Kept local only, through `.git/info/exclude`: `sources/` (paper PDFs, instructor material), `04_Project_History.md` (chat digests) and the `.docx` copies.

| Read in this order | What it is |
|---|---|
| `01_Honest_Assessment.md` | Verdict, what is already published, the proposed objective, problems to fix, decisions D1-D5 |
| `02_Related_Work.md` | 12 checked papers in the interim-slide format, Scholar queries to close the gap, reading split |
| `03_Interim_Plan.md` | Interim requirements vs what we have, dated plan table, learning checkpoints |
| `04_Project_History.md` | Timeline, digests of both ChatGPT chats, the two deck versions, what is local-only |
| `05_Label_Rules.md` | One-page label rules (sections 1-3), worked examples, the 30-example agreement protocol, how the rules map to the generator, pilot record format |
| `06_Summary_and_Decision_HE.md/.docx` | Hebrew summary and decision document for Ofir and Gilad |
| `07_Study_Pack_EN.md/.docx` | Learning track: six one-page English summaries, made for printing |
| `08_Work_Schedule_EN.md/.docx` | Three-track work schedule (practical, presentation, learning), dates assumed |
| `09_Direction_Options_HE.md/.docx` | Direction options after the 26 Nov research (reports in `research_2026-11-26/`), recommendation, week-1 gate, questions for the instructor |
| `agreement/` | Blank author and rater sheets, and `agreement.py` (agreement, Cohen's kappa, confusion matrix, list of disagreements) |
| `sources/` | Papers (PDF), deck versions (text and the 8-slide pptx), abstracts and citation counts, the course midterm guide |

## Status
**Direction chosen 2026-11-26 (Ofir and Gilad): direction 1**, the transfer-first sufficiency judge with three outcomes and the missing information named (see `09`). Ambiguity is a secondary test inside it, the documentation loop is optional, the rest is dropped. Next: label agreement (`05`), the pilot probe (`pilot/`), the task list (`10`). Label rules v0.1 are untested.

## Links
- Repo: https://github.com/ofirbuch-minervaxr/information-sufficiency-unfamiliar-databases
- ChatGPT chat 2 (ideation, 4-status spec): https://chatgpt.com/share/6af8cffc-4560-83ed-af57-5068e66c6ccd
- ChatGPT chat 1 (ambiguity pivot): https://chatgpt.com/share/6b045192-ab10-83ed-be0a-c33c27dcd720
- FALCON: https://aclanthology.org/2026.akbc-1.6/
- AIR: https://aclanthology.org/2026.emnlp-main.2446/
- ABISS: https://arxiv.org/abs/2607.23340
- SchemaBridge: https://arxiv.org/abs/2611.17044
- Know What I Don't Know: https://aclanthology.org/2023.findings-acl.352/
- PRACTIQ: https://aclanthology.org/2025.naacl-long.13/
- AmbiQT: https://aclanthology.org/2023.emnlp-main.436/
- Disambiguate First, Parse Later: https://aclanthology.org/2025.findings-acl.863/
- Course bots: https://www.apartsin.com/teaching/course-bots.html
- Midterm guide: https://www.apartsin.com/teaching/guides/midterm-presentation.html
- Models: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct and https://huggingface.co/google/gemma-3-1b-it