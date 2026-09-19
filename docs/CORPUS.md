# Corpus

## Source

SEC EDGAR 10-K annual report filings. Filings submitted to the U.S. Securities and
Exchange Commission are public-domain U.S. government records and carry no redistribution
restriction, which is why this corpus was chosen over any commercially licensed document
set: the benchmark must be reproducible by anyone without a data agreement.

## Pinning

Each document is pinned by EDGAR accession number and content hash. The manifest is
committed, so a clone reconstructs the exact corpus the published results were measured
against — not "a recent 10-K," but the identical bytes.

## Why 10-Ks specifically

- Answers are numeric and decidable, so scoring needs no LLM judge.
- Values live in tables, which is the realistic hard case for retrieval.
- Documents are long enough that naive full-context stuffing is not a viable shortcut.
- Terminology collides across companies and years, producing genuine label ambiguity.
