# Corpus and provenance

## Source

The checked-in corpus is normalized from the official SEC EDGAR Company Facts API for Apple
(`AAPL`), Microsoft (`MSFT`), and Alphabet (`GOOGL`). It contains five USD concepts for fiscal
years 2022–2025 where available: revenue, net income, operating income, assets, and cash.

This is **not** a copy of complete 10-K documents. It is a narrow XBRL fact corpus chosen so
answers are exact integers and citations can be verified without an LLM judge.

## Selection rule

For each issuer, metric, and fiscal year, `scripts/fetch_sec_facts.py` selects 10-K/FY facts
and takes the record with the latest period end, preventing prior-year comparative columns
inside a later filing from being mistaken for the current fiscal-year value.

## Reproducibility

Each normalized fact stores CIK, XBRL concept, period dates, filing date, accession number,
unit, and an SEC archive URL. `data/manifest.json` hashes the normalized corpus, provenance,
and questions. The benchmark refuses to run when any frozen input drifts.

The SEC API can acquire new filings over time, so rebuilding may change the source payload.
Published results always refer to the committed normalized corpus, not to whatever the API
returns later.
