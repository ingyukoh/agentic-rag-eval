# Design decisions and status

## Objective

Give a skeptical matcher enough evidence in under one minute to answer: what is the system,
does it work inside a stated scope, did Ingyu build the differentiating parts, and can I
reproduce the claim?

## Completed

- [x] Official SEC Company Facts ingestion with accession-level provenance
- [x] 60 normalized facts across three issuers, five metrics, and four fiscal years
- [x] 64 content-hashed evaluation cases, including abstention cases
- [x] Shared transparent BM25 retriever and single-pass baseline
- [x] LangGraph plan → retrieve → grade → verify workflow
- [x] Exact value, citation, answerability, and latency metrics
- [x] Generated per-case JSON and full failure report
- [x] FastAPI contract, Docker execution, tests, and GitHub Actions
- [x] Honest ownership and limitation statements on the first screen

## Deliberately deferred

- Dense/vector retrieval: lexical retrieval is kept visible so the control is auditable.
- Hosted LLM generation: this benchmark isolates orchestration and provenance verification.
- Full filing HTML/table parsing: the first version uses SEC-normalized XBRL Company Facts.
- Cloud deployment: Docker and API boundaries are present, but no cloud-production claim is made.

## Next evidence-strengthening experiments

1. Add a manually authored paraphrase holdout that is never emitted by the data builder.
2. Add comparison, ratio, and multi-fact questions with multiple supporting citations.
3. Expand to issuer-specific concept aliases and publish the resulting failures.
4. Add OpenTelemetry traces and a Postgres/pgvector path only when the larger corpus justifies it.
