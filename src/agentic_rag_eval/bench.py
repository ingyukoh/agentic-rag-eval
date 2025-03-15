from __future__ import annotations

from .eval import run


def main() -> int:
    results = run()
    for result in results.values():
        print(
            f"{result['name']}: task_success={result['task_success']:.1%}, "
            f"answerability={result['answerability_accuracy']:.1%}, "
            f"citation={result['citation_accuracy']:.1%}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
