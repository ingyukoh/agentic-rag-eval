# Frozen evaluation set

`questions.json` contains 60 answerable numeric questions derived from the normalized SEC
facts and four deliberately unanswerable questions. The records specify exact integer values,
units, and citation IDs.

`../manifest.json` hashes this file together with the fact corpus and provenance file. The
benchmark refuses to run after any silent edit. Refreshing the SEC corpus and re-freezing the
evaluation set requires running `scripts/fetch_sec_facts.py` and then rerunning every result.
