from __future__ import annotations

from time import perf_counter

from ..models import Answer
from ..retrieval import BM25Retriever


class BaselineSystem:
    """A fair single-pass lexical RAG control: retrieve one fact and answer once."""

    def __init__(self, retriever: BM25Retriever):
        self.retriever = retriever

    def answer(self, query: str) -> Answer:
        started = perf_counter()
        hit = self.retriever.search(query, top_k=1)[0]
        trace = ({"node": "retrieve_top1", "duration_ms": (perf_counter() - started) * 1000},)
        if hit.score <= 0:
            return Answer(query, None, None, False, None, None, trace, "no lexical evidence")
        fact = hit.fact
        return Answer(
            query,
            fact.value,
            fact.unit,
            True,
            fact.id,
            fact.source_url,
            trace,
            "single-pass top-1 retrieval",
        )
