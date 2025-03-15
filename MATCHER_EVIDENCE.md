# Matcher evidence map

Use this page to verify a requirement quickly. Each claim points to code or generated output.

| Requirement | Verifiable evidence | Honest boundary |
|---|---|---|
| Agentic workflow / LangGraph | [`agent/system.py`](src/agentic_rag_eval/agent/system.py): explicit plan → retrieve → grade → verify graph and trace | Deterministic planner; no claim of autonomous production operation |
| RAG / retrieval | [Shared BM25](src/agentic_rag_eval/retrieval/bm25.py) and 60 SEC facts with exact accession provenance | No dense/vector retrieval in this version |
| Evaluation / benchmarking | [64 content-hashed cases](data/questions/questions.json), baseline comparison, [per-case JSON](results/benchmark.json), and [failure report](results/failures.md) | Narrow issuer/metric scope; questions are template-based |
| Hallucination control | Explicit abstention when company, metric, year, unit, or provenance is missing/ambiguous | Not a complete LLM security system |
| Python backend | Typed package, [FastAPI `/health` and `/query`](src/agentic_rag_eval/api.py), Pydantic request contract | Single-process demo service, not a scaled deployment |
| Docker / CI | Offline Docker benchmark and two-version GitHub Actions matrix | No cloud infrastructure is provisioned here |
| Financial data | SEC Company Facts normalization with CIK, XBRL concept, fiscal period, accession, source URL | Not investment advice or full filing interpretation |

## One-sentence positioning

**Production AI/LLM systems engineer with quantitative validation discipline:** I make the
retrieval, verification, abstention, and evaluation behavior inspectable instead of asking a
client to trust a demo.

## Recommended application use

Lead with this repository only for roles emphasizing agentic retrieval, RAG evaluation,
Python/FastAPI backends, document intelligence, financial data, or AI reliability. Do not use
it as evidence for unrelated iOS, frontend, or pure model-training roles.
