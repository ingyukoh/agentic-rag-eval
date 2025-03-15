# Reproducible benchmark

Generated from the content-hashed corpus and evaluation set. Accuracy metrics are 
higher-is-better; latency is lower-is-better.

| System | Cases | Task success | Answerability | Value | Citation | p50 ms | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| single_pass_bm25 | 64 | 65.6% | 93.8% | 65.6% | 65.6% | 0.06 | 0.07 |
| agentic_metadata_verified | 64 | 100.0% | 100.0% | 100.0% | 100.0% | 0.43 | 0.46 |

The baseline uses the identical frozen corpus and BM25 implementation, but performs one top-1 retrieval and no planning, metadata grading, provenance verification, or abstention policy.

Latency is local control-flow time; no hosted-model call is included.
