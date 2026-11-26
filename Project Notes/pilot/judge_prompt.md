You decide whether the visible information about a database is enough to answer ONE question.
You see exactly what a model would see: tables and columns, one-line descriptions (docs), foreign keys, the first 3 sample rows of each table, and a question. Nothing else. You never see the hidden full database.

Rules
- Self-explanatory names are fine (email, created_at, customer_id joining customers).
- Do not guess coded values, flags, units, currencies or business terms ("active", "revenue", "completed", "recent") unless the docs or the sample rows define them. Sample rows count as documentation when they make the values readable. A column with no description is simply undocumented.
- A missing fact only matters if THIS question needs it. Missing information about unrelated columns changes nothing.
- Never judge by records you cannot see (whether a named person exists, whether a table is empty).

Labels
- ANSWERABLE: exactly one reasonable reading, and everything it needs (tables, columns, join path, meaning of values) is visible and clear.
- AMBIGUOUS: two or more reasonable readings, each fully supported by the visible context, that would return different results.
- NOT_ANSWERABLE with reason UNDERSPECIFIED: a table or column that could hold the answer is visible, but a fact needed to use it is missing (meaning of codes, units, definition of a term).
- NOT_ANSWERABLE with reason NOT_PRESENT: nothing visible could hold what the question asks.

Decision order (stop at the first match)
1. Is anything visible that could hold what the question asks? No: NOT_ANSWERABLE, NOT_PRESENT.
2. Can you write at least one reading using only visible, clear facts? No: NOT_ANSWERABLE, UNDERSPECIFIED.
3. Count the fully supported readings a reasonable user could mean. Two or more with different results: AMBIGUOUS. One: ANSWERABLE.

Output: one JSON object per item, one item per line, nothing else:
{"jid": "<the jid>", "label": "ANSWERABLE|AMBIGUOUS|NOT_ANSWERABLE", "reason": "UNDERSPECIFIED|NOT_PRESENT|null", "missing": "what is missing, or the two readings, in a few words; empty if answerable"}
