"""Answering systems that read filing text.

Four systems share one retriever and one corpus, so score differences are
attributable to control flow alone:

  fact_lookup_oracle   Upper-bound control. Reads the ground-truth fact table
                       directly. This is what v0.1 measured; it is reported here
                       only to show what its 100% actually represented.
  naive_top1           Naive stub: top-1 chunk, first large number in it.
  bm25_topk_extract    Strong baseline: top-k chunks, locate the metric label,
                       read the number after it. No planning or verification.
  agentic_verified     Plan -> filtered retrieve -> grade -> extract with column
                       disambiguation -> verify scale and corroboration -> abstain
                       or retry.
"""

from __future__ import annotations

import re
from time import perf_counter

from .agent.system import _parse
from .corpus import Chunk
from .models import Answer
from .retrieval.text_bm25 import ChunkBM25

SCALE = 1_000_000  # every figure in these filings is tabulated in millions

METRIC_ALIASES: dict[str, tuple[str, ...]] = {
    "revenue": ("total net sales", "total revenues", "total revenue"),
    "net_income": ("net income",),
    "operating_income": ("operating income", "income from operations"),
    "assets": ("total assets",),
    "cash": ("cash and cash equivalents",),
}

_NUMBER = re.compile(r"\$?\s*(\d{1,3}(?:,\d{3})+)")


def _numbers_after(text: str, alias: str, limit: int = 4) -> list[int]:
    """Figures following a row label, in column order (most recent year first)."""
    lowered = text.lower()
    out: list[int] = []
    for match in re.finditer(re.escape(alias), lowered):
        tail = text[match.end() : match.end() + 220]
        for found in _NUMBER.finditer(tail):
            out.append(int(found.group(1).replace(",", "")))
            if len(out) >= limit:
                return out
    return out


def _any_number(text: str) -> int | None:
    found = _NUMBER.search(text)
    return int(found.group(1).replace(",", "")) if found else None


def _trace(node: str, started: float, **kw: object) -> dict[str, object]:
    return {"node": node, "duration_ms": (perf_counter() - started) * 1000, **kw}


class FactLookupOracle:
    """Control with privileged access to ground truth. Not a retrieval system."""

    name = "fact_lookup_oracle"

    def __init__(self, facts):
        self.by_key = {(f.ticker, f.metric, f.fiscal_year): f for f in facts}

    def answer(self, query: str) -> Answer:
        plan = _parse(query)
        fact = self.by_key.get((plan["ticker"], plan["metric"], plan["fiscal_year"]))
        if fact is None:
            return Answer(query, None, None, False, None, None, (), "no exact key")
        return Answer(query, fact.value, fact.unit, True, fact.id, fact.source_url, (),
                      "privileged fact-table lookup")


class NaiveTop1:
    name = "naive_top1"

    def __init__(self, retriever: ChunkBM25):
        self.retriever = retriever

    def answer(self, query: str) -> Answer:
        started = perf_counter()
        hits = self.retriever.search(query, top_k=1)
        trace = (_trace("retrieve_top1", started, hits=len(hits)),)
        if not hits:
            return Answer(query, None, None, False, None, None, trace, "no hit")
        chunk, _ = hits[0]
        value = _any_number(chunk.text)
        if value is None:
            return Answer(query, None, None, False, None, None, trace, "no number in chunk")
        return Answer(query, value * SCALE, "USD", True, chunk.chunk_id, None, trace,
                      "first number in top-1 chunk")


class TopKExtract:
    """Strong baseline: real retrieval and label-aware extraction, no agentic control."""

    name = "bm25_topk_extract"

    def __init__(self, retriever: ChunkBM25, top_k: int = 10):
        self.retriever = retriever
        self.top_k = top_k

    def answer(self, query: str) -> Answer:
        started = perf_counter()
        metric = _parse(query)["metric"]
        hits = self.retriever.search(query, top_k=self.top_k)
        trace = (_trace("retrieve_topk", started, k=self.top_k, hits=len(hits)),)
        aliases = METRIC_ALIASES.get(metric, ())
        for chunk, _ in hits:
            for alias in aliases:
                values = _numbers_after(chunk.text, alias)
                if values:
                    return Answer(query, values[0] * SCALE, "USD", True, chunk.chunk_id,
                                  None, trace, f"label '{alias}' in retrieved chunk")
        return Answer(query, None, None, False, None, None, trace, "metric label not found")


class AgenticVerified:
    """Plan, retrieve under a structural filter, grade, verify, abstain or retry."""

    name = "agentic_verified"

    def __init__(self, retriever: ChunkBM25, top_k: int = 10, max_retries: int = 2):
        self.retriever = retriever
        self.top_k = top_k
        self.max_retries = max_retries

    def answer(self, query: str) -> Answer:
        started = perf_counter()
        plan = _parse(query)
        trace = [_trace("plan", started, **plan)]

        # Abstain before retrieving when the question cannot be grounded in this corpus.
        if not all((plan["ticker"], plan["metric"], plan["fiscal_year"])):
            trace.append(_trace("abstain", started, cause="underspecified plan"))
            return Answer(query, None, None, False, None, None, tuple(trace),
                          "plan incomplete: company, metric or fiscal year missing")

        doc_id = f"{plan['ticker'].lower()}-{plan['fiscal_year']}"
        if doc_id not in {c.doc_id for c in self.retriever.chunks}:
            trace.append(_trace("abstain", started, cause="no such filing", doc_id=doc_id))
            return Answer(query, None, None, False, None, None, tuple(trace),
                          f"no filing for {doc_id} in corpus")

        aliases = METRIC_ALIASES[plan["metric"]]
        doc_chunks = [c for c in self.retriever.chunks if c.doc_id == doc_id]

        for attempt in range(self.max_retries + 1):
            # Refinement widens the query with the metric's own vocabulary.
            expanded = query if attempt == 0 else f"{query} {' '.join(aliases)}"
            step = perf_counter()
            hits = self.retriever.search(expanded, top_k=self.top_k, doc_filter=doc_id)
            trace.append(_trace("retrieve", step, attempt=attempt, doc_filter=doc_id,
                                hits=len(hits)))

            # Gather every candidate the retrieved evidence supports, rather than
            # committing to the first label match.
            step = perf_counter()
            candidates: list[tuple[int, Chunk, str, int]] = []
            for rank, (chunk, _) in enumerate(hits):
                for alias in aliases:
                    # Column disambiguation: filings tabulate the current fiscal year
                    # first, so the leading figure after the row label is this year's.
                    values = _numbers_after(chunk.text, alias)
                    if values:
                        candidates.append((values[0], chunk, alias, rank))
            trace.append(_trace("grade", step, candidates=len(candidates)))
            if not candidates:
                continue

            # Verification: a genuine statement total is restated across the filing
            # (statement, MD&A, segment note). A figure appearing once is usually a
            # segment or subtotal row, so corroboration decides between candidates.
            step = perf_counter()
            scored = []
            for value, chunk, alias, rank in candidates:
                needle = f"{value:,}"
                corroboration = sum(1 for c in doc_chunks if needle in c.text)
                scored.append((corroboration, -rank, value, chunk, alias))
            scored.sort(reverse=True)
            corroboration, _, value, chunk, alias = scored[0]
            trace.append(_trace("verify", step, value=value,
                                corroborating_chunks=corroboration,
                                considered=len(scored)))
            if corroboration < 2:
                continue
            return Answer(query, value * SCALE, "USD", True, chunk.chunk_id, None,
                          tuple(trace),
                          f"'{alias}' current-year column, best-corroborated of "
                          f"{len(scored)} candidates ({corroboration} chunks)")

        trace.append(_trace("abstain", started, cause="no verified value"))
        return Answer(query, None, None, False, None, None, tuple(trace),
                      "no corroborated value after retries")
