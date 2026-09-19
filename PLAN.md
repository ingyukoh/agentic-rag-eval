# Build plan

## What this repository is for

A single public artifact that lets a Toptal matcher, or a technical client, answer four
questions in under a minute: *what is this, does it work, did he build it, can I check?*

The design constraint driving every decision below is that the reader is **skeptical and
in a hurry**. Depth is welcome but must sit underneath something instantly graspable —
never in front of it.

## Why one repository and not several

A portfolio of five repositories reads as five partial identities. The failure mode being
corrected here is breadth without a defensible specialization: a reviewer who has to
explain too many transfers stops explaining and moves on. One repository, one identity —
production AI/LLM systems engineering with evaluation rigor.

## Why this project and not a computer-vision one

Direct, provable experience is strongest in computer vision, OCR, and recognition. Current
demand, measured against a 25-job sample, is not: AI/LLM/agentic/RAG appears in 80% of
eligible roles, LLM explicitly in 52%, evaluation and benchmarking in 16%, and computer
vision or OCR in **0%**.

Building the strongest available evidence for a skill nobody is currently buying is a
comfortable mistake. The transferable asset from the CV and quant work is not the domain —
it is *measurement discipline*, and that transfers completely into LLM evaluation, which
is exactly the scarce skill in that demand distribution.

## Sequence

Each phase ends in a working, committed, green-CI state. Nothing is published to the
results table before it is measured.

### Phase 1 — Corpus and fixed evaluation set
Ingest a pinned set of SEC 10-K filings; build the question set with ground-truth answers
and source spans; content-hash it and commit the hash.

*Why first:* the questions must be frozen before any system exists to score against them.
A benchmark authored after seeing results is worthless, and building in this order makes
that impossible rather than merely discouraged.

### Phase 2 — Retrieval layer and non-agentic baseline
Hybrid BM25 + dense retrieval with reciprocal rank fusion. Single-shot answering on top.

*Why the baseline comes before the agent:* the baseline is the control. Building it second
would make it a thing constructed to lose. Building it first — and making it genuinely
good — is what makes the eventual comparison mean something.

### Phase 3 — Evaluation harness
Exact-match accuracy on numeric answers, abstention behavior on deliberately unanswerable
questions, p50/p95 latency, and cost per question.

*Why abstention is a first-class metric:* in finance, a confidently wrong number is far
more costly than "not found." A system that only optimizes accuracy will hallucinate on
the questions it should refuse. Measuring refusal separately is the difference between a
demo and something a regulated business could consider.

### Phase 4 — Agentic system
The LangGraph state machine: plan, retrieve, grade evidence, refine, synthesize, verify
numerically against source spans, abstain on exhausted budget.

*Why verification is the interesting step:* the failure mode of RAG on financial documents
is retrieving the right page and still reporting the wrong number — off by a scale factor,
or from the prior-year column. Re-checking the emitted figure against the cited span
catches a class of error that better retrieval alone does not.

### Phase 5 — Cassette record/replay
Record every model response; replay deterministically by default.

*Why this matters more than it looks:* it turns "trust my screenshot" into "run it
yourself, offline, free." It also makes CI meaningful — tests exercise the real control
flow on every push without spending a cent — and it makes the benchmark reproducible years
from now, after the underlying model has been deprecated.

### Phase 6 — Failure analysis
Categorize every error by cause, with counts, including the cases where the agent loses to
the baseline.

*Why publish the losses:* every portfolio claims success, so success claims carry almost no
information. A specific, quantified account of where the system breaks is the credible
signal, and it is the section a senior reviewer reads first to decide whether the author
actually understands the system or just got it working.

### Phase 7 — First screen
90-second terminal recording, results table, architecture diagram, ownership statement.

*Why last:* it is a summary. Producing it earlier would mean writing claims and then
building toward them, which is how portfolios end up overstating.

## Honesty constraints

These are binding, not aspirational.

- No number appears in the README that has not been produced by a committed, runnable script.
- The evaluation set is hashed before results exist.
- Cases where the agentic system underperforms the baseline are published in the same table
  as the wins, not relegated to a footnote.
- The repository is described as a portfolio system. It has not been deployed for a client,
  and it does not retroactively demonstrate years of production LLM experience — it
  demonstrates current ability and engineering discipline, which is a different and smaller
  claim, stated plainly.
