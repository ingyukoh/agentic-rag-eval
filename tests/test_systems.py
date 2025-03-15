from __future__ import annotations

from agentic_rag_eval.agent import AgenticSystem
from agentic_rag_eval.baseline import BaselineSystem
from agentic_rag_eval.retrieval import BM25Retriever
from agentic_rag_eval.sec import load_facts


def systems():
    retriever = BM25Retriever(load_facts())
    return BaselineSystem(retriever), AgenticSystem(retriever)


def test_agent_returns_exact_value_and_source() -> None:
    _, agent = systems()
    answer = agent.answer("What was Apple's revenue in fiscal year 2024?")
    assert answer.answerable
    assert answer.value == 391_035_000_000
    assert answer.citation_id == "aapl-2024-revenue"
    assert answer.source_url and "sec.gov" in answer.source_url
    assert {event["node"] for event in answer.trace} == {"plan", "retrieve", "grade", "verify"}


def test_agent_abstains_when_year_is_missing() -> None:
    _, agent = systems()
    answer = agent.answer("What was Apple revenue?")
    assert not answer.answerable
    assert answer.value is None
    assert answer.citation_id is None


def test_baseline_is_a_real_single_pass_control() -> None:
    baseline, _ = systems()
    answer = baseline.answer("What was Apple's revenue in fiscal year 2024?")
    assert answer.reason == "single-pass top-1 retrieval"
