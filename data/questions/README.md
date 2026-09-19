# Frozen evaluation set

`questions.json` holds the benchmark items. It is **empty until Phase 1** — ground truth
is read out of the filings by hand and verified against the source span before an item is
admitted, and no placeholder answers are committed in the meantime.

`manifest.sha256` is the content hash of the set. It is checked by the test suite on every
push and by the benchmark before it runs: if the questions or their ground truth change
after results were measured, the run fails loudly rather than silently reporting numbers
from a different set. See `src/agentic_rag_eval/eval/dataset.py`.

Roughly 20% of admitted items are deliberately unanswerable (`"answer": null`). A system
that scores well on the answerable questions while confidently inventing values for these
is not a system worth deploying against financial documents, and the metrics are built to
expose that trade-off rather than average it away.

`schema.example.json` shows the record shape. It is illustrative and is not loaded by
anything.
