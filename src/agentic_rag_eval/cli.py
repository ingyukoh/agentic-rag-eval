from __future__ import annotations

import argparse
import json

from .agent import AgenticSystem
from .retrieval import BM25Retriever
from .sec import load_facts


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the frozen SEC filing corpus")
    parser.add_argument("query")
    args = parser.parse_args()
    answer = AgenticSystem(BM25Retriever(load_facts())).answer(args.query)
    print(json.dumps(answer.__dict__, indent=2, default=list))
