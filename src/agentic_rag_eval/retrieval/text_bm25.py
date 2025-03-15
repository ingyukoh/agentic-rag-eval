"""BM25 over document chunks.

Shared verbatim by every system in the benchmark. If the baseline and the agent
differ in score, the difference cannot be the retriever -- it is the control flow
built on top of it.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from ..corpus import Chunk

K1 = 1.5
B = 0.75
_TOKEN = re.compile(r"[a-z]+|\d[\d,]*")


def tokenize(text: str) -> list[str]:
    # Comma-grouped figures stay one token: "394,328" must not become "394" + "328".
    return [t.replace(",", "") if t[0].isdigit() else t for t in _TOKEN.findall(text.lower())]


class ChunkBM25:
    def __init__(self, chunks: tuple[Chunk, ...]):
        self.chunks = chunks
        self.docs = [tokenize(c.text) for c in chunks]
        self.freqs = [Counter(d) for d in self.docs]
        self.lengths = [len(d) for d in self.docs]
        self.avg_len = sum(self.lengths) / max(len(self.docs), 1)
        df: Counter[str] = Counter()
        for freq in self.freqs:
            df.update(freq.keys())
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.postings: dict[str, list[int]] = {}
        for i, freq in enumerate(self.freqs):
            for term in freq:
                self.postings.setdefault(term, []).append(i)

    def search(self, query: str, top_k: int = 10, doc_filter: str | None = None):
        terms = tokenize(query)
        scores: Counter[int] = Counter()
        for term in terms:
            idf = self.idf.get(term)
            if idf is None:
                continue
            for i in self.postings[term]:
                if doc_filter and self.chunks[i].doc_id != doc_filter:
                    continue
                tf = self.freqs[i][term]
                norm = tf + K1 * (1 - B + B * self.lengths[i] / self.avg_len)
                scores[i] += idf * (tf * (K1 + 1)) / norm
        ranked = scores.most_common(top_k)
        return [(self.chunks[i], s) for i, s in ranked]
