from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from agentic_rag_eval.sec import load_facts, verify_manifest

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_files_match_manifest() -> None:
    verify_manifest(ROOT)


def test_corpus_has_real_sec_provenance() -> None:
    facts = load_facts(ROOT / "data" / "sec_facts.jsonl")
    assert len(facts) >= 50
    assert {fact.ticker for fact in facts} == {"AAPL", "MSFT", "GOOGL"}
    assert all(fact.accession and "sec.gov/Archives/edgar" in fact.source_url for fact in facts)


def test_tampering_is_detected(tmp_path: Path) -> None:
    data = tmp_path / "data"
    questions = data / "questions"
    questions.mkdir(parents=True)
    (data / "sec_facts.jsonl").write_text("{}\n")
    (data / "provenance.json").write_text("{}\n")
    (questions / "questions.json").write_text("[]\n")
    files = ["data/sec_facts.jsonl", "data/provenance.json", "data/questions/questions.json"]
    manifest = {
        "sha256": {
            name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() for name in files
        }
    }
    (data / "manifest.json").write_text(json.dumps(manifest))
    verify_manifest(tmp_path)
    (questions / "questions.json").write_text("[{}]\n")
    with pytest.raises(RuntimeError, match="Frozen evidence changed"):
        verify_manifest(tmp_path)
