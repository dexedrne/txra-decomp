# TXRA deep hand matching — slice f

One **300-byte** routine, 08006070, now builds from ordinary C, and the whole ROM
stays byte-identical. Accepted totals move from **124 functions / 17,316 bytes /
20.340%** to **125 / 17,616 / 20.693%** of the 85,132 mapped code bytes.

## The finding

08006070 copies the sound-channel state; it is the inverse of matched 0800619C.
Natural array C missed by two swapped address registers. Those registers hold
constants that global CSE hoists above the loop. The CSE pass hashes the internal
constant-pool label *names* (`.LCn`), and `n` continues across a whole source file.
So the order in which it creates registers for those constants depends on how many
constants the earlier functions in the same file used. Compiled after the matched
routines from 08005C7C in ROM order, 08006070 is exact, and all sixteen routines in
that unit stay exact. `src/generated/unit_08005C7C.c` includes the existing
per-function files in ROM order. Their typedef lines are now guarded so each file
still compiles alone. Only 08006070 depends on the unit.

The other retained near misses were checked with label offsets 0-9 (0-19 for
08014104 and 08014CE4). Only 080020B8
responds, and it probably starts its own file. Their remaining misses are ordinary
allocation-priority ties, not unit effects.

## Accounting

All 52 selected entries are accounted for in [deep-f/OUTCOMES.md](deep-f/OUTCOMES.md):
1 exact match, 7 C drafts improved this round, 17 C seeds kept, 15 assembly entries,
12 fragments or broken boundaries. 08015128 and 08014FF4 are reclassified from
"non-ABI register read" to ordinary C with an uninitialised local
(`docs/asm-only.md`).

Closest remaining: 08014104 (4 instructions / 4 bytes, one r8/r9 swap) and 0800B908
(10 / 10, one r8/r9 swap). Then 08014CE4 (35 / 41), 08007398 (44 / 60) and
08015128 (48). Drafts are in `docs/deep-f/candidates/`; none is installed.

## Also

`tools/setup.sh` now copies `libiberty` into the temporary ARM compiler build tree;
without it the ARM `cc1` build fails on a fresh machine (missing `obstack.c`).
Regenerating the map reports a small change in `docs/map/indirect.json`
(one veneer call at 080065CC loses its resolved target). It appears with or without
this slice's changes, so it was left uncommitted.

Validation: `make` ends in `build/txra.gba: OK`; the 170-test suite passes.
