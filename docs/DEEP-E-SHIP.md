# TXRA deep hand matching, slice e

This round added three exact C replacements, 540 bytes including pools. The build
goes from **124 functions / 17,316 bytes / 20.340%** to **127 / 17,856 bytes /
20.974%** of the unchanged 85,132-byte mapped-code denominator. Every match
uses the existing `old` profile (O2, Thumb interworking). No new compiler
profile, inline assembly, output patch or flag change was needed. A forced
`make -B -j4` prints `build/txra.gba: OK` and `cmp` confirms the 4 MiB ROM is
byte-identical.

## Matches

| Commit | Entry | Bytes | What made it match |
| --- | --- | ---: | --- |
| ec499e2 | 08015DA8 | 118 | DMA queue flush. The loop exits with `goto` to a label after the loop. A top-of-body `break` gets moved to the bottom by the loop expander's exit-test rotation. Source, destination and size are loaded into locals before the volatile DMA writes. |
| 936235a | 080063D4 | 208 | Sound buffer swap. The instructions already matched but the registers did not. A separate `next` index keeps the first index local to its block. Upward `*p++ = 0` clear loops give the original countdown. |
| 9d6d63a | 080148B0 | 214 | Link frame dispatcher. The serial control register is read as a 32-bit copy of a two-halfword bit-field record, and the result is built in a `u16` local. |

Supporting commits: 1af3edf fixes `tools/setup.sh`. The isolated ARM compiler
build was missing `libiberty`, so `agbcc_arm` could not be built on a fresh
machine and `make` failed. 60c0c36 and the final handoff commit record the
outcomes, the retained drafts, `progress.json` (`deep_hand_e`), DECOMP.md and
asm-only.md.

## Scope

The scope is the 105 unmatched entries at the start of the round, sorted by
`(bytes, address)`, taking zero-based even indices: 53 entries. The odd-index
slice belongs to the parallel job and was not touched. The full per-entry table
is in [deep-e/README.md](deep-e/README.md).

| Outcome | Entries |
| --- | ---: |
| Exact C match, installed | 3 |
| Worked on; closer natural-C draft retained in `deep-e/drafts/` | 7 |
| Assembly, BIOS or runtime entry (confirms earlier evidence) | 18 |
| Boundary fragment needing its enclosing body | 6 |
| C candidate not reached this round | 19 |

The method was to take one function at a time, compare the target with a clean C
draft and classify the mismatch. The loop dump (`-dL`) was read where
loop-optimizer behaviour was in question. Small variant batches of at most 650
compiles were used only after a shape hypothesis. The three matches and the
improved drafts came from reasoning about source shape. No brute-force search
was run.

## What is not done

- 080147D0 and 08014AE0, the link setup and serial receive routines, share a
  loop shape we cannot reproduce. The original keeps the counter, reduces only
  some address computations and reloads some invariants every pass. Structured
  loops get fully reduced and a `goto` loop gets nothing reduced. This is the
  most valuable unsolved pattern in the link unit.
- 08010910 is 46 bytes off. One zero store reuses a flag register in our
  compile.
- 0800B3A0 (156 off), 0800BBD4 (189 off), 080149FC (138 off) and 08008914 have
  better structure but the wrong register or invariant choices.
- 19 C candidates in this half were not attempted, including all ARM bodies.
  08017F64 is the ARM sibling of 0800B3A0.
- No boot, title, race or save milestone was reviewed. Those progress fields
  are unchanged.

## Validation

- `make -B -j4`: `build/txra.gba: OK`, whole-ROM `cmp` identical, after each
  match and at the end.
- `make check`: **170 tests passed**.
- Build and compile work ran at nice 15 with at most 4 jobs. The matcher on
  worker A was not accessed. No push, deploy or merge.
- The generated `docs/map/indirect.json` changes on this machine during `make`
  (local coverage data differs). It was restored and not committed.

## Review folder

`txra-review/deep-e/`. Each folder has NOTES.md and captions.json.

- `before/matching-status.png` and `after/matching-status.png`: 124 → 127 and
  20.340% → 20.974%, same framing.
- `before/` and `after/` each have one side-by-side listing per match
  (`08015DA8-*`, `080063D4-*`, `080148B0-*`). The original ROM code is on the
  left and our compile on the right. Red rows differ. All rows are green in the
  after pictures.
- `matching-findings.png`: the one change that made each match.
- `slice-outcomes.png`: all 53 entries by outcome.
- `08015DA8-break-to-goto.webm`: 8 s, 240 frames, 30 fps, no audio, 302,572
  bytes. The listing scrolls through the `break` version, then the exact
  `goto` version. It is not gameplay.
- `LOG.md`: the per-function table. `drafts/`: the retained C hypotheses.

All pictures were opened and checked: the text fits and the rows are legible.
Frames from the middle and end of the clip were extracted and viewed.

## Owner notes

OWNER-NOTES.md was absent at the start, before each major step and at the
finish, so there were no owner notes to act on.

Matched before/after: 124 / 127.
Percent before/after: 20.340% / 20.974%.
Learned: when instructions match but registers don't, split a reused variable; a loop exit that stays at the top is a goto, not a break.
