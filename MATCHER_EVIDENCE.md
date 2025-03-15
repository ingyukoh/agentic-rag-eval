# Matcher evidence map

Each claim points to code or generated output that can be checked in minutes.

| Requirement | Verifiable evidence | Honest boundary |
|---|---|---|
| Agentic workflow | [`docqa.py`](src/agentic_rag_eval/docqa.py) — explicit plan → filter → retrieve → grade → verify → abstain/retry, with a per-node trace on every answer | Deterministic control flow; **no LLM is called**. "Agentic" describes the control structure, not a model policy |
| RAG / retrieval | [`text_bm25.py`](src/agentic_rag_eval/retrieval/text_bm25.py) over **3,872 chunks** of 12 real 10-K filings, shared identically by all systems | Lexical only; no dense or hybrid retrieval in this version |
| Evaluation / benchmarking | [Four systems scored](results/benchmark.md), including a control that proves the benchmark discriminates; [per-case JSON](results/benchmark.json) | 3 issuers × 4 years × 5 metrics — narrow by construction |
| Measurement integrity | [`tests/test_discriminative.py`](tests/test_discriminative.py) fails CI if any system saturates the benchmark or if a ground-truth lookup can pass as grounded retrieval | Guards this benchmark, not benchmarks in general |
| Hallucination control | Abstains when the plan is underspecified, the filing is absent, or no figure is corroborated: **0** `answered-unanswerable` vs **3** for the baseline | Not a complete LLM security review |
| Reproducibility | Every input content-hashed in [`data/manifest.json`](data/manifest.json) and verified before the run aborts or proceeds; offline Docker; CI on two Python versions | Single-process demo, no cloud infrastructure |
| Financial data | Ground truth derived from SEC XBRL company facts with CIK, concept, fiscal period and accession; documents pinned by accession and SHA-256 | Not investment advice |
| Engineering judgment | The previous benchmark reported 100% and was **invalidated by a ten-line probe**; the [README](README.md#why-there-is-a-fourth-system-in-that-table) documents how, and the probe is now a permanent row | — |

## One-sentence positioning

**Production AI/LLM systems engineer with quantitative validation discipline:** I make
retrieval, verification and abstention behavior inspectable — and I test whether my own
benchmark can tell a real system from a stub before I report a number from it.

## Where to lead with this

Roles emphasizing agentic retrieval, RAG evaluation, document intelligence, financial data,
or AI reliability. Not evidence for iOS, frontend, or model-training roles.
