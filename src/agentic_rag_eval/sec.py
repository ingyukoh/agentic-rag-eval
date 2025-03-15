from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .models import Fact


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def facts_path() -> Path:
    return project_root() / "data" / "sec_facts.jsonl"


def load_facts(path: Path | None = None) -> list[Fact]:
    source = path or facts_path()
    facts: list[Fact] = []
    with source.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                facts.append(Fact(**json.loads(line)))
    if not facts:
        raise ValueError(f"No facts found in {source}")
    return facts


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_manifest(root: Path | None = None) -> None:
    base = root or project_root()
    manifest = json.loads((base / "data" / "manifest.json").read_text(encoding="utf-8"))
    for relative, expected in manifest["sha256"].items():
        actual = sha256(base / relative)
        if actual != expected:
            raise RuntimeError(
                f"Frozen evidence changed: {relative}\nexpected={expected}\nactual={actual}"
            )
