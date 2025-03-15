#!/usr/bin/env python3
"""Build the frozen benchmark corpus from SEC Company Facts.

Benchmark execution is offline. Refreshing this corpus is a separate, explicit
provenance-changing operation.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
USER_AGENT = "Ingyu Koh ingyukoh2@gmail.com"
COMPANIES = {
    "AAPL": ("0000320193", "Apple Inc."),
    "MSFT": ("0000789019", "Microsoft Corporation"),
    "GOOGL": ("0001652044", "Alphabet Inc."),
}
METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_income": ["OperatingIncomeLoss"],
    "assets": ["Assets"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
}
YEARS = range(2022, 2026)


def download(cik: str) -> dict:
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
        return json.load(response)


def choose(rows: list[dict], fiscal_year: int) -> dict | None:
    candidates = [
        row
        for row in rows
        if row.get("form") == "10-K"
        and row.get("fp") == "FY"
        and row.get("fy") == fiscal_year
    ]
    if not candidates:
        return None
    # A 10-K contains comparative years. The current fact has the latest period end.
    return max(candidates, key=lambda row: (row.get("end", ""), row.get("filed", "")))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    DATA.mkdir(exist_ok=True)
    facts: list[dict] = []
    provenance: dict[str, object] = {
        "source": "SEC EDGAR Company Facts API",
        "api": "https://data.sec.gov/api/xbrl/companyfacts/",
        "user_agent": USER_AGENT,
        "companies": {},
    }
    for ticker, (cik, fallback_name) in COMPANIES.items():
        payload = download(cik)
        company = payload.get("entityName", fallback_name).title()
        provenance["companies"][ticker] = {
            "cik": cik,
            "download_url": f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
        }
        us_gaap = payload["facts"]["us-gaap"]
        for metric, concepts in METRICS.items():
            for year in YEARS:
                selected = None
                selected_concept = None
                for concept in concepts:
                    units = us_gaap.get(concept, {}).get("units", {}).get("USD", [])
                    selected = choose(units, year)
                    if selected:
                        selected_concept = concept
                        break
                if not selected or not selected_concept:
                    continue
                accession = selected["accn"]
                facts.append(
                    {
                        "id": f"{ticker.lower()}-{year}-{metric.replace('_', '-')}",
                        "company": company,
                        "ticker": ticker,
                        "cik": cik,
                        "metric": metric,
                        "concept": selected_concept,
                        "fiscal_year": year,
                        "value": int(selected["val"]),
                        "unit": "USD",
                        "period_start": selected.get("start"),
                        "period_end": selected["end"],
                        "filed": selected["filed"],
                        "accession": accession,
                        "source_url": (
                            "https://www.sec.gov/Archives/edgar/data/"
                            f"{int(cik)}/{accession.replace('-', '')}/"
                        ),
                    }
                )

    facts.sort(key=lambda row: (row["ticker"], row["fiscal_year"], row["metric"]))
    facts_file = DATA / "sec_facts.jsonl"
    facts_file.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in facts), encoding="utf-8"
    )
    (DATA / "provenance.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    variants = {
        "revenue": "What was {company}'s revenue in fiscal year {year}?",
        "net_income": "Report {ticker} net income for fiscal {year}.",
        "operating_income": "How much operating income did {company} record in FY {year}?",
        "assets": "What were total assets for {ticker} at fiscal year-end {year}?",
        "cash": "Give {company} cash and cash equivalents for fiscal {year}.",
    }
    cases = [
        {
            "id": row["id"],
            "query": variants[row["metric"]].format(
                company=row["company"], ticker=row["ticker"], year=row["fiscal_year"]
            ),
            "answerable": True,
            "expected_value": row["value"],
            "expected_unit": "USD",
            "expected_citation": row["id"],
        }
        for row in facts
    ]
    for case_id, query in [
        ("unanswerable-unknown-company", "What was Tesla revenue in fiscal year 2024?"),
        ("unanswerable-missing-year", "What was Apple revenue?"),
        ("unanswerable-outside-window", "Report MSFT net income for fiscal 2035."),
        ("unanswerable-unsupported-metric", "What was Alphabet customer churn in fiscal 2024?"),
    ]:
        cases.append(
            {
                "id": case_id,
                "query": query,
                "answerable": False,
                "expected_value": None,
                "expected_unit": None,
                "expected_citation": None,
            }
        )
    questions = DATA / "questions" / "questions.json"
    questions.parent.mkdir(exist_ok=True)
    questions.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "frozen_before_benchmark": True,
        "sha256": {
            "data/sec_facts.jsonl": sha256(facts_file),
            "data/questions/questions.json": sha256(questions),
            "data/provenance.json": sha256(DATA / "provenance.json"),
        },
    }
    (DATA / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"froze {len(facts)} SEC facts and {len(cases)} evaluation cases")


if __name__ == "__main__":
    main()
