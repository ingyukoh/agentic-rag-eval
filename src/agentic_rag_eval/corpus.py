"""The document corpus: real 10-K text, chunked.

v0.1 retrieved over 60 structured XBRL facts keyed by (ticker, metric, year).
Because every question named exactly those three fields, question and fact were in
bijection and a ten-line dictionary lookup scored 100%. The facts are still the
ground truth, but they are no longer visible to any answering system: systems see
only the question and these chunks.
"""

from __future__ import annotations

import gzip
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .sec import project_root


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    text: str


@dataclass(frozen=True)
class Document:
    doc_id: str
    ticker: str
    cik: str
    fiscal_year: int
    accession: str
    source_url: str
    sha256: str
    raw_bytes: int
    text_chars: int


@lru_cache(maxsize=1)
def load_chunks(root: Path | None = None) -> tuple[Chunk, ...]:
    base = root or project_root()
    path = base / "data" / "corpus" / "chunks.jsonl.gz"
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return tuple(Chunk(**json.loads(line)) for line in handle)


@lru_cache(maxsize=1)
def load_documents(root: Path | None = None) -> tuple[Document, ...]:
    base = root or project_root()
    path = base / "data" / "corpus" / "documents.json"
    return tuple(Document(**row) for row in json.loads(path.read_text(encoding="utf-8")))
