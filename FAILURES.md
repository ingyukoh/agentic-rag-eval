# Failure analysis

*Populated from Phase 6. Entries are produced by the evaluation harness, not written by
hand — each category below will carry a count, representative question IDs, and the trace
that produced the error.*

The taxonomy the harness classifies into:

| Category | Description |
|---|---|
| `retrieval-miss` | The span containing the answer was never retrieved. |
| `wrong-column` | Correct table retrieved; value read from the wrong fiscal year. |
| `scale-error` | Correct value, wrong magnitude (thousands vs. millions). |
| `label-ambiguity` | "Revenue" vs. "net sales" vs. "total revenues" resolved to the wrong line item. |
| `over-abstention` | Answerable question refused — the cost of the abstention policy. |
| `hallucinated-citation` | Answer cites a span that does not support it. |
| `budget-exhausted` | Retry budget consumed without reaching a verified answer. |

Cases where the agentic system scores **worse** than the baseline are reported here with
the same prominence as the wins. The retry loop is not free: it costs latency and tokens,
and `over-abstention` is the category where it can actively lose.
