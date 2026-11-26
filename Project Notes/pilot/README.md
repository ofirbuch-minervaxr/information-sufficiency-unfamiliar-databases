# Pilot generator v0 (feasibility probe, not a result)

Purpose: find out in days, not weeks, whether direction 1 is workable: are the labels recoverable from what a model sees, is there headroom for a trained small model, and can a trivial classifier cheat? The pilot is deliberately small (6 databases, about 280 examples).

Pipeline: **LLM-authored database specs** (`specs/*.json`) -> `validate_spec.py` (runs every gold SQL) -> `build_dataset.py` (controlled removal, label by construction) -> `data/pilot.jsonl` -> probes (naive baselines, blind prompted judges).

Run:
```
python -I validate_spec.py specs/<db>.json
python -I build_dataset.py --specs specs --out data/pilot.jsonl --test-dbs clinic,restaurant_chain
```
`example_spec.json` is a complete small example. Copy its structure exactly.

## Spec format (one JSON file per database)
```
{ "db_id": "...", "domain": "...",
  "tables": [ { "name": "...", "description": "one sentence",
                "columns": [ {"name": "...", "type": "INTEGER|TEXT|REAL", "pk": true (optional), "doc": "one sentence"} ],
                "rows": [ [values in column order], ... ] } ],
  "foreign_keys": [ ["child_table.column", "parent_table.column"] ],
  "questions": [ { "id": "q01", "text": "...", "sql": "...", "needs_columns": ["table.column"],
                   "needs_docs": [ {"column": "table.column", "fact": "plain-words fact the doc provides"} ] } ],
  "ambiguous": [ { "id": "a01", "text": "...", "needs_columns": ["table.column"],
                   "readings": [ {"gloss": "short phrase", "sql": "..."}, {"gloss": "short phrase", "sql": "..."} ],
                   "resolving_note": {"table": "table", "text": "one sentence that makes reading 1 the default"} } ] }
```

## What gets removed (so you know what the validator and the builder rely on)
- `drop_col`: one of the question's `needs_columns` is deleted (with its doc and rows). The question can then not be answered: NOT_PRESENT.
- `drop_doc`: the `doc` of a column listed in `needs_docs` is blanked. The column stays visible but the needed fact is gone: UNDERSPECIFIED.
- `control_*`: something the question does not need is removed. The label stays ANSWERABLE.
- `ambiguous` question: shown as is (AMBIGUOUS), and again with `resolving_note` added to the table description (ANSWERABLE).
- A model sees only the table/column names, docs, foreign keys and the **first 3 rows of each table**.

## Authoring rules (all are checked by a person later; the validator checks what it can)
1. 5-6 tables, 3-8 columns each, 8-12 rows per table (consistent with the foreign keys, realistic values).
2. Every column has a one-sentence `doc`.
3. At least 4 coded or unit-bearing columns (status/type/category codes as integers or short codes; amounts with a currency; durations with a unit) whose doc explains the codes or unit. **The first 3 rows must not reveal what a code means**, and the column name must not make it guessable (name it `status`, `type`, `kind`, `grade`, not `is_returned`).
4. Exactly 10 `questions`: natural, varied wording, the way a business user would ask. No words like column, table, schema, database. Different openings (not ten "How many ..."). The gold `sql` must run and return a non-trivial result on your rows.
5. `needs_columns` lists every column the SQL reads, except pure join keys. For **at least 7 of the 10** questions add `needs_docs`: one column whose doc a reader genuinely needs (code meaning, unit, definition, time basis). `fact` states that fact. A column in `needs_docs` must also be in `needs_columns`.
6. Every needed column must be unique: no other column anywhere may hold the same information (no twins such as `price` and `price_usd` when one is needed). Needed columns must not be inferable from other visible columns.
7. Exactly 5 `ambiguous` questions: vague wording ("busiest", "best", "recent", "top", "how much did X cost") that two different reasonable readings support. Both readings use existing columns, both run, and they return **different** results on your rows. `resolving_note` is a plain sentence that makes reading 1 the default.
8. Do not copy phrasing between databases. No Hebrew. Valid JSON only (no comments, no trailing commas).
