"""Guards on the benchmark itself.

The v0.1 benchmark reported 100% for the agentic path, but a ten-line dictionary
lookup scored 100% too: the evaluation could not tell a real system from a stub.
These tests exist so that failure mode cannot come back silently. They assert
properties of the *measurement*, not of the model.
"""

from __future__ import annotations

import pytest

from agentic_rag_eval.corpus import load_chunks, load_documents
from agentic_rag_eval.docqa import AgenticVerified, NaiveTop1, TopKExtract
from agentic_rag_eval.eval.docbench import run
from agentic_rag_eval.retrieval.text_bm25 import ChunkBM25, tokenize


@pytest.fixture(scope="module")
def results():
    return run()


def test_corpus_is_real_filing_text():
    docs = load_documents()
    assert len(docs) == 12
    # Real 10-Ks are long; a fact table masquerading as a corpus would not be.
    assert all(d.text_chars > 100_000 for d in docs)
    assert len(load_chunks()) > 3_000


def test_comma_grouped_figures_survive_tokenization():
    assert "394328" in tokenize("Total net sales $ 394,328 8 %")


def test_no_system_saturates_the_benchmark(results):
    """A perfect score means the task is too easy, not that the system is finished."""
    for name, r in results.items():
        assert r["task_success"] < 1.0, f"{name} saturated the benchmark"


def test_benchmark_separates_systems(results):
    """Naive, strong-baseline and agentic paths must land on distinct scores."""
    naive = results["naive_top1"]["task_success"]
    strong = results["bm25_topk_extract"]["task_success"]
    agent = results["agentic_verified"]["task_success"]
    assert naive < strong < agent


def test_ground_truth_lookup_cannot_pass_as_grounded_retrieval(results):
    """The v0.1-style oracle knows every answer but cites no filing text."""
    oracle = results["fact_lookup_oracle"]
    assert oracle["value_accuracy"] == 1.0
    assert oracle["citation_grounded_when_answered"] == 0.0


def test_agent_never_answers_an_unanswerable_question(results):
    """Abstention is a safety property: a confident wrong figure is the costly error."""
    bad = [f for f in results["agentic_verified"]["failures"]
           if f["category"] == "answered-unanswerable"]
    assert bad == []


def test_systems_cannot_see_the_ground_truth_table():
    """Retrieval systems are constructed from chunks alone."""
    retriever = ChunkBM25(load_chunks())
    for system in (NaiveTop1(retriever), TopKExtract(retriever), AgenticVerified(retriever)):
        assert not hasattr(system, "by_key")
