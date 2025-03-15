from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True)
class Fact:
    id: str
    company: str
    ticker: str
    cik: str
    metric: str
    concept: str
    fiscal_year: int
    value: int
    unit: str
    period_start: str | None
    period_end: str
    filed: str
    accession: str
    source_url: str

    @property
    def searchable_text(self) -> str:
        return (
            f"{self.company} {self.ticker} fiscal year {self.fiscal_year} "
            f"{self.metric} {self.concept} {self.value} {self.unit}"
        )


@dataclass(frozen=True)
class SearchHit:
    fact: Fact
    score: float


@dataclass(frozen=True)
class Answer:
    query: str
    value: int | None
    unit: str | None
    answerable: bool
    citation_id: str | None
    source_url: str | None
    trace: tuple[dict[str, object], ...]
    reason: str


class AgentState(TypedDict, total=False):
    query: str
    plan: dict[str, object]
    hits: list[SearchHit]
    candidates: list[SearchHit]
    retries: int
    answer: Answer
    trace: list[dict[str, object]]
