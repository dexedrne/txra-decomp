# TXRA round 10 — sustained source search, zero new exact replacements

**Matched replacements remain 109 functions / 10,698 bytes / 12.566%.**
All fifteen eligible retained unfinished drafts received at least 1,500 seconds
of accumulated active wall time each. Twelve got closer; none matched the full
target. The task's earlier twelve-addition goal was not an identified list of
twelve unfinished functions. All fifteen eligible retained drafts were searched.
No approximate source was installed or added to `tools/rom.cfg`.

The run recorded **324,571 fresh source/profile trials**, **739,098 repeated
cache observations**, and **1,063,669 consumed observations** overall. Fresh trials
include rejected compilations or judgments. The 15,800 error observations include
repeated cached failures; they are not a count of unique failing sources. No
unique assembly-output count is claimed. The search made 786 random restarts and
147,907 accepted equal-score moves. All counts come from finalized checkpoints.

There is one fixed pool of five compiler processes and up to five simultaneous
target windows. The command was launched with `nice -n 15`; observed inherited
priority was nice 19. The minimum recorded target time is 1,500.000 seconds;
aggregate target-window time is 22,514.020 seconds. Windows include shared-pool
queueing, source generation, scoring and IO, and are not exclusive CPU time.
Five target windows were checkpointed and resumed while expanding the manifest
from twelve entries to all fifteen. Completed windows were retained. Unfinished
speculative work after the last checkpoint is excluded, although its cache entries
may survive. `resume-note.json` records this accounting boundary.

## Per-function results

Scores are instruction-token edit distance / full byte distance; instruction
distance ranks first, with bytes breaking ties. Consequently some closer
instruction scores have worse byte distances. Every row is **unmatched**.
The linked file is the closest complete text diff, without raw instruction words;
its paired `.c` file is the retained source hypothesis. Every final score was
reproduced by an independent uncached compilation. Per-entry result files also
record compiler profile, seed, errors, operator counts and observation throughput.

| Entry | Prior → best I/B | Fresh trials | Fresh/s | Observations incl. cache | Matched / closest diff |
| --- | ---: | ---: | ---: | ---: | --- |
| 08015DA8 | 4/9 → 4/9 | 21,033 | 14.02 | 70,674 | [No; full diff](match10-search/08015DA8/func_08015DA8.diff.txt) |
| 08014104 | 6/10 → 6/10 | 20,384 | 13.58 | 85,032 | [No; full diff](match10-search/08014104/func_08014104.diff.txt) |
| 0800B3A0 | 24/33 → 23/31 | 15,175 | 10.12 | 37,299 | [No; full diff](match10-search/0800B3A0/func_0800B3A0.diff.txt) |
| 08013E74 | 36/69 → 33/90 | 18,332 | 12.22 | 24,773 | [No; full diff](match10-search/08013E74/func_08013E74.diff.txt) |
| 080149FC | 59/161 → 40/167 | 20,396 | 13.57 | 48,422 | [No; full diff](match10-search/080149FC/func_080149FC.diff.txt) |
| 08006270 | 61/156 → 60/181 | 24,546 | 16.35 | 91,120 | [No; full diff](match10-search/08006270/func_08006270.diff.txt) |
| 080063D4 | 73/187 → 72/188 | 29,709 | 19.80 | 113,523 | [No; full diff](match10-search/080063D4/func_080063D4.diff.txt) |
| 08005F8C | 74/172 → 71/118 | 29,203 | 19.46 | 97,987 | [No; full diff](match10-search/08005F8C/func_08005F8C.diff.txt) |
| 080164D0 | 75/224 → 66/174 | 29,129 | 19.41 | 97,495 | [No; full diff](match10-search/080164D0/func_080164D0.diff.txt) |
| 080148B0 | 79/184 → 77/182 | 17,223 | 11.48 | 57,938 | [No; full diff](match10-search/080148B0/func_080148B0.diff.txt) |
| 0800B254 | 86/313 → 83/300 | 23,684 | 15.75 | 74,769 | [No; full diff](match10-search/0800B254/func_0800B254.diff.txt) |
| 08018BE8 | 89/256 → 89/256 | 14,489 | 9.65 | 62,232 | [No; full diff](match10-search/08018BE8/func_08018BE8.diff.txt) |
| 08006070 | 91/164 → 89/165 | 20,878 | 13.92 | 62,915 | [No; full diff](match10-search/08006070/func_08006070.diff.txt) |
| 08010910 | 107/304 → 106/301 | 18,049 | 12.03 | 64,167 | [No; full diff](match10-search/08010910/func_08010910.diff.txt) |
| 0800C850 | 122/170 → 120/193 | 22,341 | 14.88 | 75,323 | [No; full diff](match10-search/0800C850/func_0800C850.diff.txt) |

`throughput.csv` provides exact per-target times and rates. Every target ran for
25.00–25.06 minutes; per-target fresh throughput ranges from 9.65 to 19.80 trials/s.
`history.jsonl` beside each source records best scores and counts approximately
every thirty seconds and at improvements. `totals.json` and `summary.json` are
the aggregate evidence; cached observations must not be presented as new trials.

The historical angle 08014614 (88 bytes), sibling 0801466C (136 bytes), and packet
08014988 (116 bytes) were already installed. Fresh uncached checks pass their
complete extents and next-entry boundaries. These three audits are not new
matches and are not counted among the fifteen timed unfinished entries.

## What changed

`tools/search10.py` adds persistent hash caching, resumable checkpoints, logged
seeds, hill climbing, equal-score moves and seeded multi-edit restarts. The thirteen
learned transformation families enter neighborhoods before shuffled ordinary
operators. Search covers declaration/type/register hints, arithmetic reassociation
and swaps, scalar casts and narrowing/widening, constant placement, bitwise forms,
temporary introduction/copy propagation, conservative scalar assignment order,
pointer/index and offset/field forms, supported loop/if/switch forms, qualifiers,
existing-helper inline hints and local struct field order. The earlier search's
adjacent assignment reordering now excludes loads, calls and nonlocal operands.

These are conservative text-structured neighborhoods, not a complete C parser.
Arbitrary helper extraction/inlining, unrestricted global layout rewrites and
arbitrary control-flow reconstruction are not implemented. Width, qualifiers,
signature and declaration/layout hypotheses can change behavior. Only an
independent complete-byte comparison and next-entry check followed by a full ROM
build could permit installation; no hypothesis crossed that gate here. The closest
queue and blit remain at four and six instruction differences. Larger drafts still
have substantial structural differences; this round did not solve those bodies.

`tools/review_match10.py` renders the live/final charts and muted score replay.
The review was expanded to fifteen rows and queued/active elapsed labels were
checked and corrected. `progress.json` adds search evidence while preserving the
109 exact replacement count and existing execution milestones. `docs/DECOMP.md`
now has one consistent current total and references this evidence. The accepted
replacement list, reviewed layouts, compiler profiles and ROM mapping are unchanged.

## Validation and review

- `make check`: **143 tests passed**, including five new search/operator/resume
  tests. An initial new-test assertion incorrectly required a cold cache; it was
  corrected to allow valid cache hits. No existing test was disabled or changed.
- The real compiler smoke/resume checks pass; the production checkpointed restart
  also retained completed windows and accumulated elapsed time.
- **15 final closest-source audits** reproduce every retained score uncached.
  **3 already-installed audits** pass complete bytes and next-entry boundaries.
- Forced `make -B all` and final `make` print `build/txra.gba: OK`; comparison of
  the entire rebuilt ROM with the original is byte-identical.
- Regenerated indirect-call metadata was restored verbatim. `git diff --check`
  passes. ROM binaries, cache databases, intermediate assembly and private local
  checkpoints are not committed. The gitignored sibling ROM symlink is restored.

Review folder: `txra-review/match10/`.

- `before/matching-status.png` and `after/matching-status.png`: identical framing,
  honestly unchanged accepted totals.
- `search-results.png`: prior/best scores, fresh trial counts and target minutes.
- `score-traces.png`: all fifteen best-score traces, with separate score scales.
- `search-progress.webm`: six-second muted metadata replay at 30 fps, **680,591 bytes**,
  with no audio stream; validation is recorded in `review-validation.json`.
- `logs/`, `search-part1.log`, `search.log`, `totals.json`, `throughput.csv`,
  `tests.log` and `build.log`: our compiler/test output and search metadata only.

All four final pictures were opened and inspected: text fits and before/after
views agree. The clip's opening, middle and closing frames were opened and inspected; all
labels fit and the measured score replay is legible.
Every picture folder has NOTES.md and captions.json; each picture and clip has a
caption. No game footage, ROM slice or extracted asset appears in the review.

## Commits and owner notes

- `7b06a28`: persistent five-worker source search and operator/resume tests.
- `c9e19d3`: live charts, private checkpoint ignore rule and cache-aware assertion.
- The final handoff commit records all fifteen results, completed audits, progress
  explanation, the expanded review renderer, this note and `MATCH10-DONE`.

OWNER-NOTES.md was absent at startup, major steps and the final check. There are
no appended owner notes to apply or defer. The brief's lack-of-progress concern
was addressed with sustained measured compute and retained evidence; **there are
still zero new exact replacements**. No separate matcher process or checkout was
accessed. No push, deployment, merge, stash or execution-milestone claim was made.
The marker denotes completion of this search/handoff, not achievement of new C
matches. Next work needs stronger structural seeds or new neighborhoods for the
persistently unresolved register allocation and control-flow differences.

Matched before/after: 109 / 109.
Percent before/after: 12.566% / 12.566%.
Next: strengthen structural seeds and continue the saved queue/blit searches.
