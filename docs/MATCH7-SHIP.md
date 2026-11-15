# TXRA matching round 7 — target incomplete

**Three additions, with twelve of the requested fifteen still missing.**
Matching rises from **105 functions / 9,968 bytes / 11.709%** to
**108 functions / 10,582 bytes / 12.430%**. The denominator stays at 85,132
mapped instruction bytes across 229 mapped functions. Matched spans include
literal pools and in-function alignment. No approximate body is counted.

| Entry | Bytes | Profile | What resolved the mismatch |
| --- | ---: | --- | --- |
| 08014614 | 88 | old | Return the two direct differences early, keep the wrap result wide, and distribute the tail offsets. |
| 0801251C | 226 | old | Structure the outer loop with separate exits, test the masked tag directly, and name the addition input. |
| 080123F0 | 300 | old | Transfer the decoder loop and direct-mask patterns, keep the saved tag halfword-sized, and use direct mask assignments and a direct zero test. |

Each complete replacement passed uncached next-entry and byte checks, the
installation's forced full rebuild, another build after formatting, and comparison
of the entire rebuilt ROM with the private original. No instructions, assembly
output or literal pools were patched. The existing five compiler profiles remain.

## Commits

- `bce6813` — exact angle difference routine and progress update.
- `162e7d0` — exact byte decoder and progress update.
- `180c198` — exact halfword decoder and progress update.
- `9260de8` — learned patterns, measured experiments, improved queue draft,
  fixture fixes, bounded/resumable search and workflow documentation.
- The handoff commit containing this note updates the current header and marker.

All commits use the requested identity, without trailers. Nothing was pushed,
deployed or merged into another branch. The pre-existing untracked package lock
was left alone. The root ROM is the required gitignored sibling symlink.

## Search evidence and remaining work

The retained manifests account for **138,476 consumed source/profile trials**,
including **14,893 compilation or judgment errors**, plus **2,408 alternate-flag
trials**, including **880 errors**. These are repeated measured trials, not unique
compiler outputs or an exhaustive search. Three one-trial installation checks
have separate records. No extra flag combination produced an exact match.

The expanded batch finalized 46 entries: 21 standalone candidates through 160
instructions, plus 25 explicit rejections. Its first invocation ended with signal
15 after 16 finalized entries; the cause was not established. A resumed invocation
preserved those records and finalized the remainder. Unfinished work before that
interruption is excluded from totals. Three superseded or slow preliminary passes
retain drafts but no claimed attempt counts. See docs/match7-search/summary.json
and README.md for complete accounting and reproducible grids.

The learned table now has thirteen source-transformation families backed by
accepted functions. Integration tests reproduce all three new complete matches
from retained seeds. This is an auditable template table, not a trained statistical
predictor. Templates run before ordinary mutations. Focus extents are cached;
per-target time budgets retain the nearest comparison on expiry, and resume skips
finalized manifest entries. No separate matching service or running checkout was
accessed or changed.

| Remaining entry | Instruction / byte distance | What remains |
| --- | ---: | --- |
| 08014988 | 1 / 2 | Saved state register copy versus constant-address reload. |
| 08014104 | 6 / 10 | Height/base register exchange and source/count initialization order. |
| 08015DA8 | 11 / 11 | Scratch and destination registers exchanged; extent and instruction shapes now agree. |

The queue improves on the previous 25-instruction hypothesis and restores its
word-width source. Reusing a scratch variable for addresses and the DMA mask
prevents unwanted invariant hoisting; named address inputs preserve operand order.
It remains uninstalled. The angle's older near-miss files are explicitly marked
historical. Larger seeds still need better C structure; the EEPROM write draft
remains distant. ARM compilation and enclosing-body recovery for rejected
fragments are unfinished. There was no missing-asset or toolchain blocker; the
remaining matching work simply did not yield enough exact functions.

## Validation and review

- Final `make check`: **138 tests passed**.
- Three stale tests initially assumed the newly matched angle was still unmatched.
  Stable eligible fixtures now exercise their original selection/ranking checks;
  the real dry-run test also handles an empty hard-mode selection. No test was
  disabled. The focused fixture suite passed all 14 tests.
- Every installation forced a full matching rebuild. Final `make` prints OK;
  complete ROM comparison passes.
- Mapping, copy ranges and all configuration outside the replacement list are
  unchanged. Generated assembly glue includes the three verified spans.
- `git diff --check` passes. No ROM, binary slice, extracted asset or build binary
  is committed. Runtime and save-session claims in progress.json remain historical;
  no new gameplay session is claimed.

Review folder: `txra-review/match7/`.

- `before/matching-status.png` and `after/matching-status.png`: same-view totals.
- `matched-functions.png`, `matched-bytes.png`, `matched-percent.png`: actual
  accepted batch times, zero-based axes and fixed mapped-code denominator.
- `matching-progress.webm`: **6 seconds, 30 fps, muted, 312,702 bytes**.

All five final pictures and the clip's opening, middle and closing frames were
opened and inspected. Totals agree, text fits, and no visual defect remains in
this metadata review. Every picture folder has NOTES.md and captions.json; every
picture and clip has a caption. Notes explicitly disclose three of fifteen
additions. Only our metadata appears; no game visuals changed and no browser
capture was needed.

OWNER-NOTES.md was absent at the initial, major-step and final checks. There were
no appended owner notes to apply, defer or omit. MATCH7-DONE marks this handoff;
it does not declare the fifteen-addition target complete.

Matched before/after: 105 / 108.
Percent before/after: 11.709% / 12.430%.
Next: resolve packet, blit and queue allocation; twelve requested additions remain.
