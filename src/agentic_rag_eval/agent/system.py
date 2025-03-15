from __future__ import annotations

import re
from time import perf_counter

from langgraph.graph import END, START, StateGraph

from ..models import AgentState, Answer
from ..retrieval import BM25Retriever

COMPANIES = {
    "apple": ("AAPL", "Apple Inc."),
    "aapl": ("AAPL", "Apple Inc."),
    "microsoft": ("MSFT", "Microsoft Corporation"),
    "msft": ("MSFT", "Microsoft Corporation"),
    "alphabet": ("GOOGL", "Alphabet Inc."),
    "google": ("GOOGL", "Alphabet Inc."),
    "googl": ("GOOGL", "Alphabet Inc."),
}

METRICS = {
    "revenue": ("revenue", "sales", "net sales", "total revenue", "revenues"),
    "net_income": ("net income", "profit", "earnings"),
    "operating_income": ("operating income", "income from operations"),
    "assets": ("assets", "total assets"),
    "cash": ("cash", "cash and cash equivalents"),
}


def _event(node: str, started: float, **details: object) -> dict[str, object]:
    return {"node": node, "duration_ms": (perf_counter() - started) * 1000, **details}


def _parse(query: str) -> dict[str, object]:
    lowered = query.lower()
    ticker = next((value[0] for key, value in COMPANIES.items() if key in lowered), None)
    metric = next(
        (name for name, aliases in METRICS.items() if any(alias in lowered for alias in aliases)),
        None,
    )
    years = re.findall(r"\b(20\d{2})\b", lowered)
    return {"ticker": ticker, "metric": metric, "fiscal_year": int(years[-1]) if years else None}


class AgenticSystem:
    """Bounded plan/retrieve/grade/verify workflow with explicit abstention."""

    def __init__(self, retriever: BM25Retriever):
        self.retriever = retriever
        self.graph = self._build_graph()

    def _build_graph(self):
        def plan(state: AgentState) -> AgentState:
            started = perf_counter()
            plan_value = _parse(state["query"])
            return {
                "plan": plan_value,
                "retries": 0,
                "trace": [*state.get("trace", []), _event("plan", started, **plan_value)],
            }

        def retrieve(state: AgentState) -> AgentState:
            started = perf_counter()
            plan_value = state["plan"]
            expanded = (
                f"{state['query']} {plan_value.get('ticker') or ''} "
                f"{plan_value.get('metric') or ''} fiscal year"
            )
            hits = self.retriever.search(expanded, top_k=12)
            return {
                "hits": hits,
                "trace": [
                    *state.get("trace", []),
                    _event("retrieve", started, hit_ids=[hit.fact.id for hit in hits]),
                ],
            }

        def grade(state: AgentState) -> AgentState:
            started = perf_counter()
            plan_value = state["plan"]
            candidates = [
                hit
                for hit in state.get("hits", [])
                if hit.fact.ticker == plan_value.get("ticker")
                and hit.fact.metric == plan_value.get("metric")
                and hit.fact.fiscal_year == plan_value.get("fiscal_year")
                and hit.fact.unit == "USD"
            ]
            return {
                "candidates": candidates,
                "trace": [
                    *state.get("trace", []),
                    _event("grade", started, exact_candidates=[hit.fact.id for hit in candidates]),
                ],
            }

        def verify(state: AgentState) -> AgentState:
            started = perf_counter()
            candidates = state.get("candidates", [])
            if len(candidates) != 1:
                answer = Answer(
                    state["query"],
                    None,
                    None,
                    False,
                    None,
                    None,
                    tuple(state.get("trace", [])),
                    "missing or ambiguous company, metric, fiscal year, or SEC fact",
                )
            else:
                fact = candidates[0].fact
                valid = bool(fact.accession and fact.source_url and fact.period_end)
                answer = Answer(
                    state["query"],
                    fact.value if valid else None,
                    fact.unit if valid else None,
                    valid,
                    fact.id if valid else None,
                    fact.source_url if valid else None,
                    tuple(state.get("trace", [])),
                    "exact metadata match verified against frozen SEC provenance"
                    if valid
                    else "candidate failed provenance verification",
                )
            return {
                "answer": answer,
                "trace": [
                    *state.get("trace", []),
                    _event("verify", started, answerable=answer.answerable),
                ],
            }

        graph = StateGraph(AgentState)
        graph.add_node("plan", plan)
        graph.add_node("retrieve", retrieve)
        graph.add_node("grade", grade)
        graph.add_node("verify", verify)
        graph.add_edge(START, "plan")
        graph.add_edge("plan", "retrieve")
        graph.add_edge("retrieve", "grade")
        graph.add_edge("grade", "verify")
        graph.add_edge("verify", END)
        return graph.compile()

    def answer(self, query: str) -> Answer:
        state = self.graph.invoke({"query": query, "trace": []})
        answer = state["answer"]
        return Answer(
            answer.query,
            answer.value,
            answer.unit,
            answer.answerable,
            answer.citation_id,
            answer.source_url,
            tuple(state["trace"]),
            answer.reason,
        )
