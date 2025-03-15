# Failure taxonomy

Categories assigned automatically by the harness
([`eval/docbench.py`](src/agentic_rag_eval/eval/docbench.py) → `classify`). Live counts
and every failing case are in [`results/failures.md`](results/failures.md), regenerated on
each run.

| Category | Meaning | Why it happens here |
|---|---|---|
| `wrong-column` | Right filing, right row, wrong fiscal-year column | 10-K tables put two or three years side by side: `Total net sales $ 394,328 8 % $ 365,817 33 % $ 274,515` |
| `wrong-year-document` | The figure was read out of a different year's filing | Filings from adjacent years are near-identical, so lexical retrieval confuses them |
| `wrong-entity` | The figure belongs to another company | Same cause, across issuers |
| `segment-or-subtotal-row` | A segment or component line was read instead of the total | "iPhone", "Services" and "Total net sales" sit in one table |
| `scale-error` | Correct figure, wrong magnitude | Filings tabulate in millions; XBRL reports in units |
| `over-abstention` | Refused a question it could have answered | The cost of requiring corroboration before answering |
| `answered-unanswerable` | Produced a figure where the honest answer is "not in the corpus" | The most expensive error in a financial setting |
| `missing-citation` | Right value, no grounded source | An unciteable number is not an auditable one |

## On publishing the losses

The agentic path's `wrong-column` count is **higher** than the strong baseline's. That is not
hidden here, and the reason matters: the agent answers 56 of 64 questions while the baseline
answers 34, so it is exposed to failure modes the baseline avoids by staying silent. Comparing
raw failure counts between systems with different answer rates is misleading — which is why
task success, answer rate and abstention behavior are all reported side by side.

The one asymmetry that is unambiguous: `answered-unanswerable` is **3** for the baseline and
**0** for the agent.
