"""Document-grounded benchmark.

Ground truth comes from SEC's own XBRL company facts, so the answers are not
hand-curated. Answering systems never see that table: they see the question and
3,872 chunks of filing text.

A citation counts only if the cited chunk genuinely contains the reported figure
and belongs to the filing the question asks about. Matching an identifier is not
grounding.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path
from time import perf_counter

from ..corpus import load_chunks
from ..docqa import SCALE, AgenticVerified, FactLookupOracle, NaiveTop1, TopKExtract
from ..retrieval.text_bm25 import ChunkBM25
from ..sec import load_facts, project_root, verify_manifest


def load_cases(root: Path) -> list[dict]:
    return json.loads((root / "data" / "questions" / "questions.json").read_text())


def classify(case: dict, answer, facts, chunk_index) -> str | None:
    """Name the failure using the taxonomy published in FAILURES.md."""
    if case["answerable"]:
        if answer.value is None:
            return "over-abstention" if answer.answerable is False else "retrieval-miss"
        if answer.value == case["expected_value"]:
            return None if answer.citation_id else "missing-citation"
        target = next((f for f in facts if f.id == case["expected_citation"]), None)
        matches = [f for f in facts if f.value == answer.value]
        cited = chunk_index.get(answer.citation_id or "")
        if target and matches:
            other = matches[0]
            if other.metric == target.metric and other.ticker == target.ticker:
                # Same metric, different year. Which defect it is depends on where the
                # figure was read from: a prior-year column of the right filing is a
                # column-selection error; the wrong filing is a retrieval error.
                right_doc = f"{target.ticker.lower()}-{target.fiscal_year}"
                if cited is not None and cited.doc_id == right_doc:
                    return "wrong-column"
                return "wrong-year-document"
            if other.ticker == target.ticker and other.fiscal_year == target.fiscal_year:
                return "wrong-metric-row"
            return "wrong-entity"
        if target and answer.value in (target.value * 1000, target.value // 1000):
            return "scale-error"
        return "segment-or-subtotal-row"
    return None if answer.value is None else "answered-unanswerable"


def grounded(answer, chunk_index) -> bool:
    """Does the cited chunk actually contain the reported figure?"""
    if answer.value is None or answer.citation_id is None:
        return answer.value is None and answer.citation_id is None
    chunk = chunk_index.get(answer.citation_id)
    if chunk is None:
        return False
    return f"{answer.value // SCALE:,}" in chunk.text


def score(system, cases, facts, chunk_index) -> dict:
    rows, failures = [], []
    for case in cases:
        started = perf_counter()
        answer = system.answer(case["query"])
        elapsed = (perf_counter() - started) * 1000
        answerability_ok = answer.answerable == case["answerable"]
        value_ok = answer.value == case["expected_value"]
        citation_ok = grounded(answer, chunk_index)
        success = answerability_ok and value_ok and citation_ok
        category = classify(case, answer, facts, chunk_index)
        rows.append({
            "id": case["id"], "success": success, "answerability_correct": answerability_ok,
            "value_correct": value_ok, "citation_grounded": citation_ok,
            "predicted_value": answer.value, "expected_value": case["expected_value"],
            "latency_ms": elapsed, "reason": answer.reason, "failure": category,
        })
        if category:
            failures.append({"id": case["id"], "category": category,
                             "predicted": answer.value, "expected": case["expected_value"],
                             "reason": answer.reason})
    lat = sorted(r["latency_ms"] for r in rows)
    return {
        "name": system.name, "cases": len(rows),
        "task_success": statistics.mean(r["success"] for r in rows),
        "answerability_accuracy": statistics.mean(r["answerability_correct"] for r in rows),
        "value_accuracy": statistics.mean(r["value_correct"] for r in rows),
        # Grounding is only meaningful where a figure was actually produced;
        # averaging abstentions into it would reward saying nothing.
        "citation_grounded_when_answered": (
            statistics.mean(
                r["citation_grounded"] for r in rows if r["predicted_value"] is not None
            )
            if any(r["predicted_value"] is not None for r in rows)
            else 0.0
        ),
        "answered": sum(r["predicted_value"] is not None for r in rows),
        "p50_latency_ms": statistics.median(lat),
        "p95_latency_ms": lat[min(len(lat) - 1, int(len(lat) * 0.95))],
        "rows": rows, "failures": failures,
    }


def run(root: Path | None = None) -> dict:
    base = root or project_root()
    verify_manifest(base)
    facts = load_facts()
    chunks = load_chunks(base)
    chunk_index = {c.chunk_id: c for c in chunks}
    retriever = ChunkBM25(chunks)
    cases = load_cases(base)

    systems = [
        FactLookupOracle(facts),
        NaiveTop1(retriever),
        TopKExtract(retriever),
        AgenticVerified(retriever),
    ]
    return {s.name: score(s, cases, facts, chunk_index) for s in systems}


if __name__ == "__main__":
    results = run()
    for name, r in results.items():
        print(f"{name:22} success={r['task_success']:6.1%} value={r['value_accuracy']:6.1%} "
              f"cited={r['citation_grounded_when_answered']:6.1%} "
              f"answered={r['answered']:2d}/{r['cases']} p50={r['p50_latency_ms']:7.2f}ms")


def write_reports(root: Path, results: dict) -> None:
    """Regenerate the committed benchmark and failure reports from a live run."""
    out = root / "results"
    out.mkdir(exist_ok=True)
    (out / "benchmark.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    order = ["fact_lookup_oracle", "naive_top1", "bm25_topk_extract", "agentic_verified"]
    note = {
        "fact_lookup_oracle": "control: reads ground truth, never opens a filing",
        "naive_top1": "naive stub",
        "bm25_topk_extract": "strong baseline",
        "agentic_verified": "agentic path",
    }
    lines = [
        "# Benchmark",
        "",
        "Generated by `python -m agentic_rag_eval.bench`. Ground truth is SEC XBRL company",
        "facts; answering systems see only the question and the filing chunks. A citation",
        "counts only when the cited chunk actually contains the reported figure.",
        "",
        "| System | | Cases | Answered | Task success | Value | Grounded citation | p50 ms |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in order:
        r = results[name]
        lines.append(
            f"| `{name}` | {note[name]} | {r['cases']} | {r['answered']} | "
            f"{r['task_success']:.1%} | {r['value_accuracy']:.1%} | "
            f"{r['citation_grounded_when_answered']:.1%} | {r['p50_latency_ms']:.2f} |"
        )
    lines += ["", "Latency is local control-flow time. No hosted model is called anywhere in",
              "this benchmark; every system here is deterministic.", ""]
    (out / "benchmark.md").write_text("\n".join(lines), encoding="utf-8")

    from collections import Counter
    fl = ["# Failure analysis", "",
          "Generated, not written by hand. Categories are defined in `FAILURES.md`.", ""]
    for name in order:
        r = results[name]
        fl.append(f"## `{name}` — {len(r['failures'])} failures of {r['cases']} cases")
        fl.append("")
        counts = Counter(f["category"] for f in r["failures"])
        if not counts:
            fl += ["No failures.", ""]
            continue
        fl += ["| Category | Count |", "|---|---:|"]
        fl += [f"| `{k}` | {v} |" for k, v in counts.most_common()]
        fl.append("")
        fl += ["<details><summary>Every failing case</summary>", "",
               "| Case | Category | Predicted | Expected |", "|---|---|---:|---:|"]
        fl += [f"| `{f['id']}` | `{f['category']}` | {f['predicted']} | {f['expected']} |"
               for f in r["failures"]]
        fl += ["", "</details>", ""]
    (out / "failures.md").write_text("\n".join(fl), encoding="utf-8")
