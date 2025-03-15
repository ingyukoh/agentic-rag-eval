from __future__ import annotations

import math
import re
from collections import Counter

from ..models import Fact, SearchHit

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9.-]*")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


class BM25Retriever:
    """Transparent lexical control used by both systems."""

    def __init__(self, facts: list[Fact], k1: float = 1.5, b: float = 0.75):
        self.facts = facts
        self.k1 = k1
        self.b = b
        self.tokens = [tokenize(fact.searchable_text) for fact in facts]
        self.counts = [Counter(tokens) for tokens in self.tokens]
        self.avg_len = sum(map(len, self.tokens)) / len(self.tokens)
        frequency: Counter[str] = Counter()
        for tokens in self.tokens:
            frequency.update(set(tokens))
        total = len(facts)
        self.idf = {
            term: math.log(1 + (total - count + 0.5) / (count + 0.5))
            for term, count in frequency.items()
        }

    def search(self, query: str, top_k: int = 8) -> list[SearchHit]:
        terms = tokenize(query)
        hits: list[SearchHit] = []
        for fact, counts, tokens in zip(self.facts, self.counts, self.tokens, strict=True):
            normalizer = 1 - self.b + self.b * len(tokens) / self.avg_len
            score = 0.0
            for term in terms:
                count = counts.get(term, 0)
                if count:
                    score += self.idf.get(term, 0.0) * count * (self.k1 + 1) / (
                        count + self.k1 * normalizer
                    )
            hits.append(SearchHit(fact=fact, score=score))
        hits.sort(key=lambda hit: (-hit.score, hit.fact.id))
        return hits[:top_k]
