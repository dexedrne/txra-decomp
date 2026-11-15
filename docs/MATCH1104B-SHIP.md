# 11/4 continuation ship note

The complete four-voice sample mixer, 080076F4, now matches the original ARM
compiler output. Totals advance from 178 entries / 71,440 bytes / 83.917% to
**179 entries / 72,516 bytes / 85.181%** of the existing 85,132 mapped code bytes.

| Commit | Change |
| --- | --- |
| `a89f743` | Automatic current-match filtering and best-score ranking for a mutation-search queue, with five regression tests. |
| `8324b28` | Complete 1,076-byte match for func_080076F4, installed independently. |

The final handoff commit is titled `Record 11/4 mixer match, recovery drafts and review evidence`.

The mixer uses one function-wide sum for both samples and short-lived partial
sums. This preserves the original reloads and r1 result. A multiplication form
for buffer selection recovers the conditional-move order. The final four
position updates must appear in source order 0, 1, 2, 3. No compiler profile,
register binding or emitted instruction was patched.

## Requested merge and night search

`feat/permuter-1103` was missing from the supplied checkout and its local origin.
The available local bundles contain only earlier matching work; the repository
had no unreachable adapter commit either. `tools/permute.py`, score snapshots
and the live scheduled runner were also unavailable. The location was requested
during the job and origin was checked again while matching continued.

Consequently **the requested no-ff merge and live schedule update are not done**.
No merge ref was fabricated. Progress retains the newer numbers and now includes
the additional mixer match. The committed standalone queue helper reads
`tools/rom.cfg`, also excludes entries covered by installed bodies, and ranks
supplied snapshots by their lowest score. It must be imported or called by the
actual runner when that branch becomes available. Its documented CLI is in
`docs/permuter-queue.md`.

08017E68 and 08018E18 are already installed, just like 080165BC and 08017F64;
they should not be rescheduled. 080076F4 is now installed as well. No overnight
score was invented or treated as a byte-comparison score.

## Validation and review

- The original ARM compiler produced a complete exact 1,076-byte mixer,
  including all literal pools. Installation forced a full rebuild of all
  179 installed replacements and passed the complete ROM SHA-1 check.
- `make check`: 177 tests, 176 passed and one skipped. This includes the five
  new queue tests, covering fresh matches, internal covered entries, score
  ranking and the current inventory.
- Review folder: `txra-review/match-1104b/`. Key pictures are
  `before-080076F4.png`, `after-080076F4.png`, `matching-progress.png` and
  `target-filter.png`. Every picture was opened and inspected.
- `080076F4.webm`: 8 seconds, 30 fps, 828,124 bytes, video only. Both halves
  were inspected from decoded frames. It replays the compiler comparison;
  there is no new game-footage or playability claim. Notes and captions cover
  every review picture and clip.

## Remaining work

The uninstalled drafts and measured comparisons are under
`docs/near-misses/hand-20261104b/`. Car-contact rotation hoisting, cached offsets
and allocation remain unresolved. A HUD temporary-sharing experiment reproduces
the 36-byte local frame but still differs substantially. The Thumb sound prefix
now has compiled source through the hardware-channel sequence loop; the PCM
voice body is absent and its diagnostic early end is explicitly marked.
The streamer and ARM track-face renderer remain at the previously documented
recovery boundaries. These are source-recovery aids, not accepted replacements
or independently verified behavior.

No `OWNER-NOTES.md` was present during the work or final owner-note check, so
there are no owner notes left unaddressed. No ROM or extracted binary was staged.
No push, deployment or merge into main was performed. Marker: `MATCH1104B-DONE`.
