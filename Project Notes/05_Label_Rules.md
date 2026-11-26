# Label rules v0.1 (draft: Ofir and Gilad test these, then they are frozen)

Written 2026-11-26 by Claude. The rules are **sections 1-3 (one page)**. The rest supports the 30-example agreement check and the generator.
Based on the merged 3-outcome framing in `01_Honest_Assessment.md` (decision D1, not yet confirmed with Gilad).

## 1. What you see, and what you may use
You see exactly what the model sees: **tables and columns, descriptions ("docs"), keys, sample rows (if any), and one question.** Nothing else. You never see the hidden full database.
- **Self-explanatory names are fine:** `email`, `created_at`, `customer_id` joining `Customers`.
- **Do not guess** coded values, flags, units, currencies or business terms ("active", "revenue", "completed", "recent") unless the docs or the sample rows define them.
- **Sample rows count as documentation.** If rows show `status` = paid / refunded, those codes are readable. A value that is not shown may still exist; that is fine.
- **Never label from data you cannot see:** whether "Dana" exists, whether a table is empty.
- A missing fact only matters if **this question needs it.** Missing information about unrelated columns changes nothing.

## 2. The labels

| Label | Meaning | Assistant should |
|---|---|---|
| **ANSWERABLE** | Exactly one reasonable reading, and everything it needs (tables, columns, join path, meaning of values) is visible and clear. | answer, write the query |
| **AMBIGUOUS** | Two or more reasonable readings, **each fully supported by the visible context**, that would return **different results**. Rewording the question would fix it. | show the top 2 readings and ask which |
| **NOT_ANSWERABLE** | No reading is fully supported by the visible context. Give one reason below. | |
| reason **UNDERSPECIFIED** | A table or column that could hold the answer **is visible**, but a fact needed to use it is missing: meaning of codes, units, join key, definition of a term. Someone must tell us a fact about the database. | ask for documentation |
| reason **NOT_PRESENT** | Nothing visible could hold the answer: no table, column or relationship for the concept. | abstain and say what is missing |

## 3. Decision order (stop at the first match)
1. **Is anything visible that could hold what the question asks?** No -> NOT_ANSWERABLE, reason NOT_PRESENT.
2. **Can you write at least one reading using only visible, clear facts?** No -> NOT_ANSWERABLE, reason UNDERSPECIFIED.
3. **Count the fully supported readings a reasonable user could mean.** Two or more with different results -> AMBIGUOUS. One (or several that always return the same result) -> ANSWERABLE.

Quick tests when torn:
- *Would rewording the question fix it?* -> AMBIGUOUS.
- *Does someone have to tell us a fact about the database?* -> UNDERSPECIFIED.
- *Is there any visible place for the thing at all?* No -> NOT_PRESENT.

## 4. Edge rulings
- **E1** Never judge by records you cannot see (does "Dana" exist, is the table empty).
- **E2** Synonyms are fine when the mapping is obvious ("client" for Customers, "bought" for Orders).
- **E3** Vague words ("recent", "big", "popular", "active"): AMBIGUOUS if two or more supported readings differ; NOT_PRESENT if no visible column could support any reading. Clear periods ("last month") are not vague.
- **E4** Standard derivations (age from `birth_date`, a total from line items) are fine: ANSWERABLE.
- **E5** Missing calculation inputs ("profit" with no cost column) -> NOT_PRESENT.
- **E6** Readings that differ only in wording, or always return the same rows, count as one reading.
- **E7** One supported reading plus another reasonable reading you cannot support: label UNDERSPECIFIED only if the unsupported reading is at least as plausible as the supported one; otherwise ANSWERABLE. Flag it `unsure`.
- **E8** Hesitated for more than half a minute? Set `unsure = 1`. Disagreements on these items teach the most.

## 5. Worked examples

Contexts (anything not listed is "none"):

```
S      Customers(customer_id, name, email)
       Orders(order_id, customer_id, order_date, status, total)
       Payments(payment_id, order_id, amount, paid_at)
       Keys: Orders.customer_id -> Customers.customer_id ; Payments.order_id -> Orders.order_id
       Docs: Orders.status = completed / cancelled / pending ; Orders.total = order value in USD, excluding tax
S-nodoc      S without the Orders.status doc
S-noemail    S without the Customers.email column
S-nototaldoc S without the Orders.total doc
U      Users(user_id, name) ; Logins(login_id, user_id, timestamp) ; Requests(request_id, user_id, created_at)
       Keys: Logins.user_id -> Users.user_id ; Requests.user_id -> Users.user_id
K      Orders(order_id, ref1, order_date) ; Customers(customer_id, name)      (no keys, no docs)
```

| # | Context | Question | Label (reason) | Why |
|---|---|---|---|---|
| 1 | S | How many orders did Dana place? | ANSWERABLE | one reading: count the orders of the customer named Dana (we do not check that Dana exists) |
| 2 | S | How much did each customer pay in total? | ANSWERABLE | "pay" means Payments.amount, reached through Orders |
| 3 | S | How much revenue did each customer generate? | AMBIGUOUS | sum of Orders.total or sum of Payments.amount: both supported, different results |
| 4 | S | List recent orders | AMBIGUOUS | "recent" = last 7 or 30 days: both supported by order_date, different results. ("List last month's orders" is ANSWERABLE.) |
| 5 | S | What is Dana's phone number? | NOT_ANSWERABLE (NOT_PRESENT) | no visible column could hold a phone number |
| 6 | S-nodoc | How many completed orders were there? | NOT_ANSWERABLE (UNDERSPECIFIED) | `status` is visible, but which value means "completed" is not given |
| 6c | S | How many completed orders were there? | ANSWERABLE | same question; the code is documented. The label follows the *information*, not the question |
| 7 | S-noemail | What is Dana's email? | NOT_ANSWERABLE (NOT_PRESENT) | a deleted column looks exactly like one that never existed, so it gets the same label |
| 8 | S-nototaldoc | How many orders did Dana place? | ANSWERABLE | the removed doc is not needed for this question: the label does not change (a control) |
| 9 | U | How active was Paul? | AMBIGUOUS | logins or requests |
| 10 | U | What is Paul's salary? | NOT_ANSWERABLE (NOT_PRESENT) | no visible salary |
| 11 | K | How many orders did Dana place? | NOT_ANSWERABLE (UNDERSPECIFIED) | `ref1` might link to Customers, but nothing says so |

## 6. Agreement check (30 examples)
1. **Each of you writes 15 items:** 5 ANSWERABLE, 5 AMBIGUOUS, 5 NOT_ANSWERABLE (at least 2 UNDERSPECIFIED and 2 NOT_PRESENT). Together that is 10 / 10 / 10.
2. Each author includes: **1 or more contrast pair** (same question, with and without a doc), **2 or more controls** (irrelevant information removed, label unchanged), **3 or more borderline items** (say so in `notes`).
3. Each context is a short text file (8 lines at most, same format as above) in `agreement/contexts/`, named by the item id.
4. Fill your `author_sheet` (template in `agreement/`). **Send the other person only the contexts and a `rater_sheet`** with the label columns empty.
5. Each of you labels the other's 15 items blind, using only sections 1-4.
6. Run `python agreement/agreement.py author_ofir.csv rater_gilad.csv author_gilad.csv rater_ofir.csv` from this folder.
7. Read it: kappa **0.80 or more** = freeze the rules. **0.60-0.79** = fix the rules for each disagreement, then relabel those items. **Below 0.60** = simplify the labels before generating data.
8. Discuss every disagreement and decide: bad item, or unclear rule? Write it in the changelog.

30 items is a sanity check, not a result: the uncertainty on kappa is wide.
**Fallback:** if most confusion is AMBIGUOUS vs UNDERSPECIFIED, report only the 3 outcomes as the headline and keep the reason as an exploratory field.

## 7. From human rules to the generator
Removal is not a label. An example changes label only if the removed information was **necessary** for the question.

| What the generator removes | Label becomes | Condition |
|---|---|---|
| A table or column the question needs | NOT_ANSWERABLE (NOT_PRESENT) | looks the same as "never existed" |
| Docs for something the question needs (code meanings, units, definitions) | NOT_ANSWERABLE (UNDERSPECIFIED) | necessity test passes |
| A key the question needs, when the join is not guessable from the names | NOT_ANSWERABLE (UNDERSPECIFIED) | necessity test passes |
| Sample rows | UNDERSPECIFIED only if the values or format were evident only from the rows; otherwise unchanged | necessity test |
| Anything the question does not need | **unchanged** (control) | at least a third of ANSWERABLE and AMBIGUOUS examples should be controls |
| (adds) a second plausible column or reading | AMBIGUOUS | the readings must give different results when run |

**Necessity test:** ask a strong model to answer with the information removed. If it still gets the right query, the removal did not matter, so the example keeps its original label. (The idea follows the "Evidence Necessity" stage in ABISS.)

## 8. Record format for the pilot (JSONL, one object per line)
```json
{
  "id": "ex001",
  "database_id": "shop_01",
  "information_condition": "docs_removed",
  "visible_context": {
    "tables": {"Customers": ["customer_id", "name", "email"],
               "Orders": ["order_id", "customer_id", "order_date", "status", "total"]},
    "keys": ["Orders.customer_id -> Customers.customer_id"],
    "docs": {},
    "sample_rows": {}
  },
  "question": "How many completed orders were there?",
  "label": "NOT_ANSWERABLE",
  "reason": "UNDERSPECIFIED",
  "readings": [],
  "missing_information": ["which Orders.status value means completed"],
  "next_action": "request_documentation",
  "removed": [{"type": "column_doc", "target": "Orders.status", "necessary": true}]
}
```
- `information_condition`: full, docs_removed, keys_removed, samples_removed, schema_only, irrelevant_removed.
- `readings`: 0 items (NOT_ANSWERABLE), 1 (ANSWERABLE) or 2 (AMBIGUOUS, the top two); each has meaning, tables, columns, joins, operation.
- `next_action`: answer, clarify, request_documentation, abstain.
- Ground truth (the full database and what was removed) is stored separately from `visible_context`, and the model never sees it.

## Changelog
- v0.1 (2026-11-26): first draft, untested.
