# Failure methodology

The generated, case-level report is [`results/failures.md`](results/failures.md). It lists
every benchmark loss with the system, case ID, predicted value, and reason. Agent failures
must appear with the same prominence as baseline failures.

The current frozen set exposes these categories:

| Category | Detection |
|---|---|
| wrong fiscal year | value or citation differs while issuer and metric match |
| unsupported question guessed | expected abstention but the system returns a fact |
| over-abstention | answerable case returns no value |
| provenance failure | value is present but accession, source URL, or period is missing |
| label ambiguity | planned metric does not identify one exact SEC concept/fact |

The agent has no failures in the current narrow 64-case set. That is explicitly **not** a
claim of production reliability; the README lists the missing comparison, ratio, broad
paraphrase, full-table, and issuer-scale tests.
