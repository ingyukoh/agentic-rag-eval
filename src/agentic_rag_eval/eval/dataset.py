"""Loading and integrity-checking of the frozen evaluation set.

The evaluation questions are content-hashed and the hash is committed before any
results are produced. This module is what enforces that: if a question, its ground
truth, or its source span is edited after the fact, `verify_manifest` fails and the
benchmark refuses to run. It exists so that "the eval set was not tuned to the
results" is a checkable property rather than a promise.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

MANIFEST_NAME = "manifest.sha256"


@dataclass(frozen=True)
class Question:
    """One evaluation item with a decidable ground-truth answer."""

    id: str
    question: str
    answer: str | None
    """Ground-truth value, or None for a deliberately unanswerable question."""
    unit: str | None = None
    source_doc: str | None = None
    source_span: str | None = None


def canonical_bytes(questions: list[Question]) -> bytes:
    """Serialize questions to a stable byte string, independent of file formatting.

    Sorted by id and emitted with fixed separators so that reordering or reindenting
    the source file does not change the hash, while any change to content does.
    """
    payload = [
        {
            "id": q.id,
            "question": q.question,
            "answer": q.answer,
            "unit": q.unit,
            "source_doc": q.source_doc,
            "source_span": q.source_span,
        }
        for q in sorted(questions, key=lambda q: q.id)
    ]
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def content_hash(questions: list[Question]) -> str:
    """SHA-256 over the canonical serialization."""
    return hashlib.sha256(canonical_bytes(questions)).hexdigest()


def load_questions(path: Path) -> list[Question]:
    """Read a JSON array of question objects."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError(f"{path}: expected a JSON array of questions")
    seen: set[str] = set()
    questions = []
    for item in raw:
        q = Question(
            id=item["id"],
            question=item["question"],
            answer=item.get("answer"),
            unit=item.get("unit"),
            source_doc=item.get("source_doc"),
            source_span=item.get("source_span"),
        )
        if q.id in seen:
            raise ValueError(f"{path}: duplicate question id {q.id!r}")
        seen.add(q.id)
        questions.append(q)
    return questions


def verify_manifest(questions_path: Path, manifest_path: Path) -> str:
    """Raise if the eval set no longer matches its committed hash. Returns the hash."""
    expected = Path(manifest_path).read_text(encoding="utf-8").split()[0].strip()
    actual = content_hash(load_questions(questions_path))
    if actual != expected:
        raise ValueError(
            "Evaluation set has changed since its manifest was committed.\n"
            f"  expected: {expected}\n"
            f"  actual:   {actual}\n"
            "Results measured against a different eval set are not comparable. "
            "If this change is intentional, re-freeze the set and re-run every benchmark."
        )
    return actual
