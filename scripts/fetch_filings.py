"""Download the primary 10-K document for each pinned accession and chunk it.

The existing corpus is XBRL *facts* -- structured values keyed by company, metric
and year. That makes the retrieval task a dictionary lookup, which is why the
v0.1 benchmark could not distinguish a real system from a ten-line stub.

This script fetches the underlying filing *documents* so the task becomes what it
claims to be: find the value inside hundreds of pages of prose and tables, where
the same row carries two or three fiscal years side by side.

Documents are pinned by accession number and content-hashed. SEC asks for a
declared User-Agent and no more than 10 requests/second; both are respected.
"""

from __future__ import annotations

import gzip
import hashlib
import html
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = json.loads((ROOT / "data" / "provenance.json").read_text())
USER_AGENT = PROVENANCE["user_agent"]
OUT_DIR = ROOT / "data" / "corpus"

CHUNK_CHARS = 1200
CHUNK_OVERLAP = 200
REQUEST_DELAY_S = 0.25  # well inside SEC's 10 req/s ceiling


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    time.sleep(REQUEST_DELAY_S)
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def primary_document(cik: str, accession: str) -> str:
    """Resolve the main 10-K .htm inside a filing folder via its index.json."""
    stripped = accession.replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{stripped}"
    index = json.loads(get(f"{base}/index.json"))
    names = [item["name"] for item in index["directory"]["item"]]
    candidates = [
        n
        for n in names
        if n.endswith(".htm")
        and not n.endswith("_cal.htm")
        and not n.startswith("R")
        and "ex" not in n.lower().split("-")[-1]
    ]
    # The primary document is the largest plain .htm that is not an exhibit.
    best = max(candidates, key=lambda n: 0 if "ex" in n.lower() else len(n))
    for name in candidates:
        if re.match(r"^[a-z]+-?\d{8}\.htm$", name):
            best = name
            break
    return f"{base}/{best}"


def to_text(raw: bytes) -> str:
    markup = raw.decode("utf-8", errors="ignore")
    markup = re.sub(r"(?is)<(script|style).*?</\1>", " ", markup)
    text = re.sub(r"(?s)<[^>]+>", " ", markup)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def chunk(text: str) -> list[str]:
    step = CHUNK_CHARS - CHUNK_OVERLAP
    pieces = (text[i : i + CHUNK_CHARS] for i in range(0, len(text), step))
    return [piece for piece in pieces if piece.strip()]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    facts = [json.loads(line) for line in (ROOT / "data" / "sec_facts.jsonl").open()]
    filings = sorted({(f["ticker"], f["cik"], f["fiscal_year"], f["accession"]) for f in facts})

    documents, chunks = [], []
    for ticker, cik, year, accession in filings:
        url = primary_document(cik, accession)
        raw = get(url)
        text = to_text(raw)
        doc_id = f"{ticker.lower()}-{year}"
        documents.append(
            {
                "doc_id": doc_id,
                "ticker": ticker,
                "cik": cik,
                "fiscal_year": year,
                "accession": accession,
                "source_url": url,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "raw_bytes": len(raw),
                "text_chars": len(text),
            }
        )
        for i, body in enumerate(chunk(text)):
            chunks.append({"chunk_id": f"{doc_id}-{i:05d}", "doc_id": doc_id, "text": body})
        print(f"{doc_id:12} {len(raw):>9,} bytes -> {len(text):>8,} chars  {url.split('/')[-1]}")

    (OUT_DIR / "documents.json").write_text(json.dumps(documents, indent=2) + "\n")
    with gzip.open(OUT_DIR / "chunks.jsonl.gz", "wt", encoding="utf-8") as handle:
        for row in chunks:
            handle.write(json.dumps(row) + "\n")

    print(f"\n{len(documents)} documents, {len(chunks):,} chunks -> {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
