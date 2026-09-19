"""Benchmark entry point.

Invoked by `docker compose up bench`. Every run begins by verifying that the frozen
evaluation set still matches its committed hash — a benchmark measured against a
silently edited question set is worse than no benchmark, so this check is a hard gate
rather than a warning.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agentic_rag_eval.eval.dataset import MANIFEST_NAME, load_questions, verify_manifest

REPO_ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_DIR = REPO_ROOT / "data" / "questions"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bench", description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="call model APIs instead of replaying recorded cassettes (requires a key)",
    )
    parser.add_argument(
        "--record",
        action="store_true",
        help="re-record cassettes from this run; implies --live",
    )
    args = parser.parse_args(argv)

    questions_path = QUESTIONS_DIR / "questions.json"
    manifest_path = QUESTIONS_DIR / MANIFEST_NAME

    digest = verify_manifest(questions_path, manifest_path)
    questions = load_questions(questions_path)

    print("agentic-rag-eval")
    print(f"  eval set:   {len(questions)} questions")
    print(f"  manifest:   {digest}")
    print(f"  mode:       {'live' if (args.live or args.record) else 'replay (offline)'}")
    print()

    if not questions:
        print("The evaluation set is empty: ground truth is extracted in Phase 1 and this")
        print("repository does not ship placeholder answers. Nothing to measure yet.")
        print("Build sequence and rationale: PLAN.md")
        return 0

    print("Phases 2-5 pending; see PLAN.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
