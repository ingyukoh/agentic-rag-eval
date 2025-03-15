from __future__ import annotations

import json
import statistics
from pathlib import Path
from time import perf_counter
from typing import Protocol

from ..agent import AgenticSystem
from ..baseline import BaselineSystem
from ..models import Answer
from ..retrieval import BM25Retriever
from ..sec import load_facts, project_root, verify_manifest


class AnsweringSystem(Protocol):
    def answer(self, query: str) -> Answer: ...


def load_cases(root: Path) -> list[dict]:
    return json.loads((root / "data" / "questions" / "questions.json").read_text())


def score(name: str, system: AnsweringSystem, cases: list[dict]) -> dict:
    rows: list[dict] = []
    for case in cases:
        started = perf_counter()
        answer = system.answer(case["query"])
        elapsed = (perf_counter() - started) * 1000
        answerability_correct = answer.answerable == case["answerable"]
        value_correct = answer.value == case["expected_value"]
        citation_correct = answer.citation_id == case["expected_citation"]
        success = answerability_correct and value_correct and citation_correct
        rows.append(
            {
                "id": case["id"],
                "success": success,
                "answerability_correct": answerability_correct,
                "value_correct": value_correct,
                "citation_correct": citation_correct,
                "latency_ms": elapsed,
                "predicted_value": answer.value,
                "reason": answer.reason,
            }
        )
    latencies = [row["latency_ms"] for row in rows]
    ordered = sorted(latencies)
    p95_index = min(len(ordered) - 1, int(len(ordered) * 0.95))
    return {
        "name": name,
        "cases": len(rows),
        "task_success": statistics.mean(row["success"] for row in rows),
        "answerability_accuracy": statistics.mean(
            row["answerability_correct"] for row in rows
        ),
        "value_accuracy": statistics.mean(row["value_correct"] for row in rows),
        "citation_accuracy": statistics.mean(row["citation_correct"] for row in rows),
        "p50_latency_ms": statistics.median(latencies),
        "p95_latency_ms": ordered[p95_index],
        "rows": rows,
    }


def write_reports(root: Path, results: dict) -> None:
    results_dir = root / "results"
    results_dir.mkdir(exist_ok=True)
    (results_dir / "benchmark.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Reproducible benchmark",
        "",
        "Generated from the content-hashed corpus and evaluation set. Accuracy metrics are ",
        "higher-is-better; latency is lower-is-better.",
        "",
        "| System | Cases | Task success | Answerability | Value | Citation | p50 ms | p95 ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for result in results.values():
        lines.append(
            f"| {result['name']} | {result['cases']} | {result['task_success']:.1%} | "
            f"{result['answerability_accuracy']:.1%} | {result['value_accuracy']:.1%} | "
            f"{result['citation_accuracy']:.1%} | {result['p50_latency_ms']:.2f} | "
            f"{result['p95_latency_ms']:.2f} |"
        )
    lines.extend(
        [
            "",
            "The baseline uses the identical frozen corpus and BM25 implementation, but performs "
            "one top-1 retrieval and no planning, metadata grading, provenance verification, or "
            "abstention policy.",
            "",
            "Latency is local control-flow time; no hosted-model call is included.",
        ]
    )
    (results_dir / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    failures = [
        {"system": result["name"], **row}
        for result in results.values()
        for row in result["rows"]
        if not row["success"]
    ]
    failure_lines = [
        "# Failure analysis",
        "",
        "Every failing case is listed; agent losses are not hidden.",
        "",
    ]
    if not failures:
        failure_lines.append(
            "No failures in the frozen set. This does not establish production reliability."
        )
    else:
        for failure in failures:
            failure_lines.append(
                f"- **{failure['system']} / {failure['id']}** — "
                f"predicted `{failure['predicted_value']}`; {failure['reason']}"
            )
    (results_dir / "failures.md").write_text(
        "\n".join(failure_lines) + "\n", encoding="utf-8"
    )


def run() -> dict:
    root = project_root()
    verify_manifest(root)
    facts = load_facts()
    cases = load_cases(root)
    retriever = BM25Retriever(facts)
    results = {
        "baseline": score("single_pass_bm25", BaselineSystem(retriever), cases),
        "agent": score("agentic_metadata_verified", AgenticSystem(retriever), cases),
    }
    write_reports(root, results)
    return results
