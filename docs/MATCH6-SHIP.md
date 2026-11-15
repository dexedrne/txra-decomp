# TXRA matching round 6 — target incomplete

**Two additions, not fifteen.** Matching rises from **103 functions / 9,656 bytes /
11.342%** to **105 functions / 9,968 bytes / 11.709%**. The denominator remains
85,132 mapped instruction bytes, across 229 mapped functions. Matched spans
include literal pools and in-function alignment. **Thirteen additions remain.**

The complete accepted replacements are:

| Entry | Bytes | Profile | Source change that resolved the mismatch |
| --- | ---: | --- | --- |
| 08018B24 | 176 | standard-o1 | Compute the stack-buffer byte offset separately, add the integer buffer address, then advance the halfword pointer. |
| 0801466C | 136 | old | Name bitmap and destination pointers explicitly; initialize the counter, packet cursor, bitmap, destination and byte offset in that order. |

Both passed uncached complete comparison, next-entry boundary checks, an
installation's forced full rebuild and whole-ROM identity. Formatting was
verified before installation. The final `make` prints `build/txra.gba: OK`, and
complete binary comparison with the private original passes. No compiler output
is patched; no partial body or approximate match is counted.

## Commits

- `ef8644f` — complete EEPROM read replacement and progress update.
- `3ed2e18` — complete link input replacement and progress update.
- `fc4fea1` — learned transformations, bounded focused searches, generated
  replacement assembly glue, retained compiler evidence and workflow docs.
- The handoff commit containing this note adds aggregate accounting and the marker.

Commits use the requested identity without trailers. Nothing was pushed or
merged. The pre-existing untracked package lock remains untouched.

## Search and learned transformations

The retained five near-misses were inspected and tested with targeted source
grids: declaration/initializer order, register hints, arithmetic widths and
signedness, branch assignments, integer versus pointer cursors, scoped loop
constants, and checksum helpers. Existing compiler profiles were tried, plus
single-flag alternatives. None of the extra flags produced an exact result;
the build still supports the same five profiles.

Four completed manifests account for **51,450 source/profile trials**, including
**11,306 compilation failures**. They include a 6,000-trial angle pass, a
10,000-trial EEPROM pass, a broader 34,010-trial pass, and a focused 1,440-trial
packet pass. The broader pass searched fourteen eligible entries through 120
instructions and explicitly rejected twenty-two fragments or unsupported entries.
Some targets were visited more than once. Trials are not distinct compiler
outputs or an exhaustive search of possible C sources.

The separate flag grids contain **110 measured trials**, twelve rejected by the
compiler or judge. Manual grids retain their planned `total_jobs`; those values
are deliberately excluded from measured attempt totals because consuming an
exact result ends a grid early. Two preliminary focused packet passes were
interrupted while generating neighborhoods without further compiler progress;
their drafts survive, but no attempt totals are claimed. Completed manifests and
aggregate accounting are in `docs/match6-search/summary.json`.

`tools/matching_patterns.json` now records six transformation families backed by
accepted source: integer cursors, saved constants, separate pointer updates,
guarded loops, stack byte offsets and explicit global pointers. The search tries
these ahead of ordinary mutations. An integration test applies the learned stack
offset transformation to the old pointer seed and reproduces all 176 bytes.
This is an auditable transformation table, not a trained statistical predictor.

`--focus` selects statements around the mismatching source region; normalization
prevents whitespace differences from widening the selected edit. The search now
caches bounded neighborhoods and limits source size, escape depth and generations.
This bounds the expensive neighborhood generation observed in the preliminary
packet passes. `--max-instructions` broadens the old sixty-instruction selection.
All candidates still need the unchanged uncached acceptance and full-build gate.
No separate matching service or its running checkout was accessed or changed.

## Remaining near misses

| Entry | Best instruction / byte distance | What remains |
| --- | --- | --- |
| 08014988 | 1 / 2 | State-address reload where the target copies its saved register. |
| 08014104 | 6 / 10 | Height/base register allocation and source/count initialization ordering. |
| 08014614 | 4 / 11 | Narrow result adds return shifts; widening changes earlier branch sharing and arithmetic. Output still crosses the next entry. |
| 08015DA8 | 25 / 60 | Queue source width, high-register allocation, count address shape and constant lifetime. |

The packet draft improved from twelve differing instructions to one. It remains
uninstalled. 0801466C is resolved; its old round-five draft remains historical.
The updated packet source, full text diff and manifest are in `docs/near-misses/`.
Some trial hypotheses change behavior and must never be used as replacements.
Larger lifted drafts still need better structured seeds; the ARM compiler path
and enclosing-body recovery for rejected fragments remain unfinished.

## Validation and metadata

- `make check`: **132 tests passed**.
- After final search refinements: **6 learned-pattern tests and 11 search tests passed**.
- Both installation builds forced all matching replacements to rebuild and verified the ROM.
- Final `make` and complete ROM binary comparison passed.
- Mapping, copy ranges and reviewed indirect metadata remain unchanged. Generated
  assembly glue now includes the two verified replacement spans.
- Historical gameplay/save claims in progress.json were preserved. No new runtime
  session is claimed; matching preserves the original ROM's behavior.
- `git diff --check` passed. No ROM, binary slice, extracted asset or generated
  build binary is committed.

The missing root ROM link was restored as the required gitignored sibling
symlink. No external asset or service blocker remains.

## Owner review and notes

Review folder: `txra-review/match6/`.

- `before/matching-status.png` and `after/matching-status.png`: same-view totals.
- `matched-functions.png`, `matched-bytes.png` and `matched-percent.png`: accepted
  batch history, fixed denominator and zero-based axes.
- `matching-progress.webm`: **6 seconds, 30 fps, muted, 303,365 bytes**.

All five pictures and the clip's opening, middle and closing frames were opened
and inspected. Totals agree, text fits, and no visual defect remains in this
review output. Every picture folder has NOTES.md and captions.json; every picture
and clip has a caption. Notes explicitly state two of fifteen additions are done.
Only our configuration, progress and history output appears in the media. There
were no game visual changes and no browser capture was required.

OWNER-NOTES.md was absent at the initial, major-step and final checks. There are
no appended owner notes to list, apply or omit. `MATCH6-DONE` marks the handoff;
it does not declare the fifteen-addition target complete.

Matched before/after: 103 / 105.
Percent before/after: 11.342% / 11.709%.
Next: resolve the packet register copy, then blit, angle and queue; thirteen additions remain.
