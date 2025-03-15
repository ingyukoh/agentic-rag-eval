"""Benchmark entry point: verify the frozen evidence, run every system, write reports."""

from __future__ import annotations

from .eval.docbench import run, write_reports
from .sec import project_root


def main() -> int:
    root = project_root()
    results = run(root)          # aborts if any frozen input has changed
    write_reports(root, results)
    for name, r in results.items():
        print(
            f"{name:22} success={r['task_success']:6.1%} value={r['value_accuracy']:6.1%} "
            f"cited={r['citation_grounded_when_answered']:6.1%} "
            f"answered={r['answered']:2d}/{r['cases']} p50={r['p50_latency_ms']:7.2f}ms"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
