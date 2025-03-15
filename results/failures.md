# Failure analysis

Generated, not written by hand. Categories are defined in `FAILURES.md`.

## `fact_lookup_oracle` — 0 failures of 64 cases

No failures.

## `naive_top1` — 61 failures of 64 cases

| Category | Count |
|---|---:|
| `over-abstention` | 36 |
| `segment-or-subtotal-row` | 24 |
| `answered-unanswerable` | 1 |

<details><summary>Every failing case</summary>

| Case | Category | Predicted | Expected |
|---|---|---:|---:|
| `aapl-2022-assets` | `segment-or-subtotal-row` | 14124000000 | 352755000000 |
| `aapl-2022-cash` | `segment-or-subtotal-row` | 6223000000 | 23646000000 |
| `aapl-2022-net-income` | `over-abstention` | None | 99803000000 |
| `aapl-2022-operating-income` | `segment-or-subtotal-row` | 316199000000 | 119437000000 |
| `aapl-2022-revenue` | `over-abstention` | None | 394328000000 |
| `aapl-2023-assets` | `over-abstention` | None | 352583000000 |
| `aapl-2023-cash` | `segment-or-subtotal-row` | 6223000000 | 29965000000 |
| `aapl-2023-net-income` | `over-abstention` | None | 96995000000 |
| `aapl-2023-operating-income` | `segment-or-subtotal-row` | 298085000000 | 114301000000 |
| `aapl-2023-revenue` | `over-abstention` | None | 383285000000 |
| `aapl-2024-assets` | `over-abstention` | None | 364980000000 |
| `aapl-2024-cash` | `segment-or-subtotal-row` | 6223000000 | 29943000000 |
| `aapl-2024-net-income` | `over-abstention` | None | 93736000000 |
| `aapl-2024-operating-income` | `segment-or-subtotal-row` | 95846000000 | 123216000000 |
| `aapl-2024-revenue` | `over-abstention` | None | 391035000000 |
| `aapl-2025-assets` | `over-abstention` | None | 359241000000 |
| `aapl-2025-cash` | `segment-or-subtotal-row` | 94949000000 | 35934000000 |
| `aapl-2025-net-income` | `over-abstention` | None | 112010000000 |
| `aapl-2025-operating-income` | `segment-or-subtotal-row` | 307003000000 | 133050000000 |
| `aapl-2025-revenue` | `over-abstention` | None | 416161000000 |
| `googl-2022-assets` | `segment-or-subtotal-row` | 14124000000 | 365264000000 |
| `googl-2022-cash` | `segment-or-subtotal-row` | 5520000000 | 21879000000 |
| `googl-2022-net-income` | `over-abstention` | None | 59972000000 |
| `googl-2022-operating-income` | `segment-or-subtotal-row` | 91855000000 | 74842000000 |
| `googl-2022-revenue` | `over-abstention` | None | 282836000000 |
| `googl-2023-assets` | `over-abstention` | None | 402392000000 |
| `googl-2023-cash` | `segment-or-subtotal-row` | 5520000000 | 24048000000 |
| `googl-2023-net-income` | `over-abstention` | None | 73795000000 |
| `googl-2023-operating-income` | `segment-or-subtotal-row` | 95858000000 | 84293000000 |
| `googl-2023-revenue` | `over-abstention` | None | 307394000000 |
| `googl-2024-assets` | `over-abstention` | None | 450256000000 |
| `googl-2024-cash` | `segment-or-subtotal-row` | 5520000000 | 23466000000 |
| `googl-2024-net-income` | `over-abstention` | None | 100118000000 |
| `googl-2024-operating-income` | `segment-or-subtotal-row` | 95858000000 | 112390000000 |
| `googl-2024-revenue` | `over-abstention` | None | 350018000000 |
| `googl-2025-assets` | `over-abstention` | None | 595281000000 |
| `googl-2025-cash` | `segment-or-subtotal-row` | 5520000000 | 30708000000 |
| `googl-2025-net-income` | `over-abstention` | None | 132170000000 |
| `googl-2025-operating-income` | `segment-or-subtotal-row` | 121263000000 | 129039000000 |
| `googl-2025-revenue` | `segment-or-subtotal-row` | 5050000000 | 402836000000 |
| `msft-2022-assets` | `segment-or-subtotal-row` | 14124000000 | 364840000000 |
| `msft-2022-cash` | `segment-or-subtotal-row` | 101746000000 | 13931000000 |
| `msft-2022-net-income` | `over-abstention` | None | 72738000000 |
| `msft-2022-operating-income` | `segment-or-subtotal-row` | 106430000000 | 83383000000 |
| `msft-2022-revenue` | `over-abstention` | None | 198270000000 |
| `msft-2023-assets` | `over-abstention` | None | 411976000000 |
| `msft-2023-cash` | `segment-or-subtotal-row` | 101746000000 | 34704000000 |
| `msft-2023-net-income` | `over-abstention` | None | 72361000000 |
| `msft-2023-operating-income` | `over-abstention` | None | 88523000000 |
| `msft-2023-revenue` | `over-abstention` | None | 211915000000 |
| `msft-2024-assets` | `over-abstention` | None | 512163000000 |
| `msft-2024-cash` | `segment-or-subtotal-row` | 101746000000 | 18315000000 |
| `msft-2024-net-income` | `over-abstention` | None | 88136000000 |
| `msft-2024-operating-income` | `over-abstention` | None | 109433000000 |
| `msft-2024-revenue` | `over-abstention` | None | 245122000000 |
| `msft-2025-assets` | `over-abstention` | None | 619003000000 |
| `msft-2025-cash` | `over-abstention` | None | 30242000000 |
| `msft-2025-net-income` | `over-abstention` | None | 101832000000 |
| `msft-2025-operating-income` | `over-abstention` | None | 128528000000 |
| `msft-2025-revenue` | `over-abstention` | None | 281724000000 |
| `unanswerable-unknown-company` | `answered-unanswerable` | 4381000000 | None |

</details>

## `bm25_topk_extract` — 56 failures of 64 cases

| Category | Count |
|---|---:|
| `over-abstention` | 29 |
| `segment-or-subtotal-row` | 17 |
| `wrong-entity` | 5 |
| `answered-unanswerable` | 3 |
| `wrong-column` | 1 |
| `wrong-year-document` | 1 |

<details><summary>Every failing case</summary>

| Case | Category | Predicted | Expected |
|---|---|---:|---:|
| `aapl-2022-assets` | `over-abstention` | None | 352755000000 |
| `aapl-2022-cash` | `segment-or-subtotal-row` | 5760000000 | 23646000000 |
| `aapl-2022-net-income` | `wrong-entity` | 72738000000 | 99803000000 |
| `aapl-2022-revenue` | `over-abstention` | None | 394328000000 |
| `aapl-2023-assets` | `over-abstention` | None | 352583000000 |
| `aapl-2023-cash` | `segment-or-subtotal-row` | 5760000000 | 29965000000 |
| `aapl-2023-net-income` | `over-abstention` | None | 96995000000 |
| `aapl-2023-revenue` | `over-abstention` | None | 383285000000 |
| `aapl-2024-assets` | `over-abstention` | None | 364980000000 |
| `aapl-2024-cash` | `segment-or-subtotal-row` | 5760000000 | 29943000000 |
| `aapl-2024-net-income` | `over-abstention` | None | 93736000000 |
| `aapl-2024-revenue` | `over-abstention` | None | 391035000000 |
| `aapl-2025-assets` | `over-abstention` | None | 359241000000 |
| `aapl-2025-cash` | `segment-or-subtotal-row` | 5991000000 | 35934000000 |
| `aapl-2025-net-income` | `over-abstention` | None | 112010000000 |
| `aapl-2025-revenue` | `wrong-entity` | 281724000000 | 416161000000 |
| `googl-2022-assets` | `over-abstention` | None | 365264000000 |
| `googl-2022-cash` | `segment-or-subtotal-row` | 26465000000 | 21879000000 |
| `googl-2022-net-income` | `wrong-entity` | 72738000000 | 59972000000 |
| `googl-2022-operating-income` | `segment-or-subtotal-row` | 91855000000 | 74842000000 |
| `googl-2023-assets` | `over-abstention` | None | 402392000000 |
| `googl-2023-cash` | `segment-or-subtotal-row` | 26465000000 | 24048000000 |
| `googl-2023-net-income` | `wrong-entity` | 88136000000 | 73795000000 |
| `googl-2023-operating-income` | `segment-or-subtotal-row` | 95858000000 | 84293000000 |
| `googl-2023-revenue` | `wrong-column` | 282836000000 | 307394000000 |
| `googl-2024-assets` | `over-abstention` | None | 450256000000 |
| `googl-2024-cash` | `segment-or-subtotal-row` | 26465000000 | 23466000000 |
| `googl-2024-net-income` | `over-abstention` | None | 100118000000 |
| `googl-2024-operating-income` | `segment-or-subtotal-row` | 95858000000 | 112390000000 |
| `googl-2024-revenue` | `over-abstention` | None | 350018000000 |
| `googl-2025-assets` | `over-abstention` | None | 595281000000 |
| `googl-2025-cash` | `segment-or-subtotal-row` | 26465000000 | 30708000000 |
| `googl-2025-net-income` | `over-abstention` | None | 132170000000 |
| `googl-2025-operating-income` | `segment-or-subtotal-row` | 121263000000 | 129039000000 |
| `googl-2025-revenue` | `wrong-entity` | 281724000000 | 402836000000 |
| `msft-2022-assets` | `over-abstention` | None | 364840000000 |
| `msft-2022-cash` | `over-abstention` | None | 13931000000 |
| `msft-2022-operating-income` | `over-abstention` | None | 83383000000 |
| `msft-2022-revenue` | `over-abstention` | None | 198270000000 |
| `msft-2023-assets` | `over-abstention` | None | 411976000000 |
| `msft-2023-cash` | `segment-or-subtotal-row` | 28359000000 | 34704000000 |
| `msft-2023-net-income` | `over-abstention` | None | 72361000000 |
| `msft-2023-operating-income` | `over-abstention` | None | 88523000000 |
| `msft-2023-revenue` | `over-abstention` | None | 211915000000 |
| `msft-2024-assets` | `over-abstention` | None | 512163000000 |
| `msft-2024-cash` | `segment-or-subtotal-row` | 5760000000 | 18315000000 |
| `msft-2024-net-income` | `over-abstention` | None | 88136000000 |
| `msft-2024-operating-income` | `segment-or-subtotal-row` | 69773000000 | 109433000000 |
| `msft-2024-revenue` | `wrong-year-document` | 281724000000 | 245122000000 |
| `msft-2025-assets` | `over-abstention` | None | 619003000000 |
| `msft-2025-cash` | `segment-or-subtotal-row` | 5991000000 | 30242000000 |
| `msft-2025-net-income` | `over-abstention` | None | 101832000000 |
| `msft-2025-operating-income` | `segment-or-subtotal-row` | 69773000000 | 128528000000 |
| `unanswerable-unknown-company` | `answered-unanswerable` | 281724000000 | None |
| `unanswerable-missing-year` | `answered-unanswerable` | 394328000000 | None |
| `unanswerable-outside-window` | `answered-unanswerable` | 72738000000 | None |

</details>

## `agentic_verified` — 27 failures of 64 cases

| Category | Count |
|---|---:|
| `wrong-column` | 15 |
| `segment-or-subtotal-row` | 8 |
| `over-abstention` | 4 |

<details><summary>Every failing case</summary>

| Case | Category | Predicted | Expected |
|---|---|---:|---:|
| `aapl-2025-cash` | `wrong-column` | 29943000000 | 35934000000 |
| `aapl-2025-revenue` | `segment-or-subtotal-row` | 209586000000 | 416161000000 |
| `googl-2022-assets` | `over-abstention` | None | 365264000000 |
| `googl-2022-cash` | `segment-or-subtotal-row` | 20945000000 | 21879000000 |
| `googl-2022-net-income` | `segment-or-subtotal-row` | 40269000000 | 59972000000 |
| `googl-2022-operating-income` | `segment-or-subtotal-row` | 78714000000 | 74842000000 |
| `googl-2022-revenue` | `segment-or-subtotal-row` | 257637000000 | 282836000000 |
| `googl-2023-assets` | `wrong-column` | 365264000000 | 402392000000 |
| `googl-2023-cash` | `wrong-column` | 21879000000 | 24048000000 |
| `googl-2023-net-income` | `segment-or-subtotal-row` | 76033000000 | 73795000000 |
| `googl-2023-operating-income` | `wrong-column` | 74842000000 | 84293000000 |
| `googl-2023-revenue` | `wrong-column` | 282836000000 | 307394000000 |
| `googl-2024-assets` | `wrong-column` | 402392000000 | 450256000000 |
| `googl-2024-cash` | `wrong-column` | 24048000000 | 23466000000 |
| `googl-2024-net-income` | `wrong-column` | 59972000000 | 100118000000 |
| `googl-2024-operating-income` | `wrong-column` | 84293000000 | 112390000000 |
| `googl-2024-revenue` | `wrong-column` | 307394000000 | 350018000000 |
| `googl-2025-assets` | `wrong-column` | 450256000000 | 595281000000 |
| `googl-2025-cash` | `wrong-column` | 23466000000 | 30708000000 |
| `googl-2025-net-income` | `wrong-column` | 100118000000 | 132170000000 |
| `googl-2025-operating-income` | `wrong-column` | 112390000000 | 129039000000 |
| `googl-2025-revenue` | `wrong-column` | 350018000000 | 402836000000 |
| `msft-2022-assets` | `over-abstention` | None | 364840000000 |
| `msft-2023-assets` | `over-abstention` | None | 411976000000 |
| `msft-2023-net-income` | `segment-or-subtotal-row` | 69274000000 | 72361000000 |
| `msft-2025-assets` | `over-abstention` | None | 619003000000 |
| `msft-2025-operating-income` | `segment-or-subtotal-row` | 69773000000 | 128528000000 |

</details>
