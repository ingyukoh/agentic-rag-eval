"""Tests for the eval-set freezing mechanism."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentic_rag_eval.eval.dataset import (
    Question,
    content_hash,
    load_questions,
    verify_manifest,
)

QUESTIONS = Path(__file__).parent.parent / "data" / "questions" / "questions.json"
MANIFEST = Path(__file__).parent.parent / "data" / "questions" / "manifest.sha256"


def _q(qid: str, answer: str | None = "1.0") -> Question:
    return Question(id=qid, question=f"value for {qid}?", answer=answer)


def test_hash_is_stable_under_reordering():
    assert content_hash([_q("a"), _q("b")]) == content_hash([_q("b"), _q("a")])


def test_hash_changes_when_ground_truth_changes():
    assert content_hash([_q("a", "1.0")]) != content_hash([_q("a", "2.0")])


def test_unanswerable_questions_are_distinct_from_empty_answers():
    assert content_hash([_q("a", None)]) != content_hash([_q("a", "")])


def test_duplicate_ids_are_rejected(tmp_path):
    path = tmp_path / "questions.json"
    path.write_text(
        json.dumps([{"id": "x", "question": "?"}, {"id": "x", "question": "?"}]),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate question id"):
        load_questions(path)


def test_committed_eval_set_matches_its_manifest():
    """The frozen set must never drift from its committed hash."""
    assert verify_manifest(QUESTIONS, MANIFEST)


def test_tampering_with_the_eval_set_is_detected(tmp_path):
    questions = tmp_path / "questions.json"
    manifest = tmp_path / "manifest.sha256"
    questions.write_text(json.dumps([{"id": "a", "question": "?", "answer": "1.0"}]), "utf-8")
    manifest.write_text(content_hash(load_questions(questions)), "utf-8")
    assert verify_manifest(questions, manifest)

    questions.write_text(json.dumps([{"id": "a", "question": "?", "answer": "9.9"}]), "utf-8")
    with pytest.raises(ValueError, match="has changed since its manifest"):
        verify_manifest(questions, manifest)
