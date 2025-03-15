from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .agent import AgenticSystem
from .retrieval import BM25Retriever
from .sec import load_facts

app = FastAPI(title="SEC Filing RAG Auditor", version="1.0.0")


class Query(BaseModel):
    query: str = Field(min_length=3, max_length=500)


@lru_cache(maxsize=1)
def system() -> AgenticSystem:
    return AgenticSystem(BM25Retriever(load_facts()))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query")
def query(request: Query) -> dict[str, object]:
    answer = system().answer(request.query)
    return {
        "value": answer.value,
        "unit": answer.unit,
        "answerable": answer.answerable,
        "citation_id": answer.citation_id,
        "source_url": answer.source_url,
        "reason": answer.reason,
        "trace": answer.trace,
    }
