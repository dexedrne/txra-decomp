# TXRA deep hand matching, slice g

Five more routines rebuild byte for byte from ordinary C, 2,300 bytes with
pools. The build goes from **128 functions / 18,156 bytes / 21.327%** to
**133 / 20,456 bytes / 24.029%** of the unchanged 85,132-byte mapped-code
denominator. Every match uses an existing profile; no flags, pragmas, inline
assembly or output patches were added. A forced `make -B -j4` prints
`build/txra.gba: OK` and `cmp` confirms the 4 MiB ROM is byte-identical.

## Matches

| Commit | Entry | Bytes | Profile | What made it match |
| --- | --- | ---: | --- | --- |
| b4ef6c4 | 08018BE8 | 352 | standard-o1 | EEPROM write. It is library code: its neighbours 08018AA4/08018B24 already match with `standard-o1`, and earlier drafts were compiled with the default profile (335 bytes off). With the library profile, the sibling read routine's `offset = bits * 2; p = (u16 *)(offset + (u32)buffer)` idiom, one `for (;;)` wait loop that tests the acknowledge first, and `current + (228 - previous)` close it. |
| df16e9d | 080147D0 | 224 | old | Link setup. Every access goes through `g_03007A30` itself instead of a local `s = &g_03007A30`. loop.c hoists an invariant only when `2 * (1 + 12) * savings * lifetime >= insns in the loop`. Through the pointer the loop has 20 RTL insns, so everything is hoisted and reduced; addressed directly it has more than 26, the short-lived `+80` base stays inside, and the third slot is never a strength-reduction candidate, exactly as in the original. `TxraLinkState` now names the buffers at +0x60/+0x78 and the two 72-byte groups at +0x90. |
| 9c04172 | 08012CC8 | 496 | old | Title loop. SDK `DmaClear` shape (block-local `vu32 tmp = 0` declared before the DMA register pointer), an upward `for (j = 0; j < 160; j++)` clear that loop.c reverses into the original signed pointer countdown, and `while (1)` (a `for (;;)` is rotated and moves the literal pool). |
| f442005 | 08012EB8 | 516 | old | The same title loop with three text lines; exact on the first try. |
| aab0009 | 0800F008 | 712 | old | Scene player. Same DMA macros, a `switch` on the scene per frame and another for the scene change, `goto` back to two restart points; exact on the first natural draft. |

## Scope and accounting

All 51 entries are in [deep-g/OUTCOMES.md](deep-g/OUTCOMES.md)
(`deep-g/outcomes.json`).

| Outcome | Entries |
| --- | ---: |
| Exact C match, installed | 5 |
| C, closer draft retained (`deep-g/drafts/`) | 4 |
| C, worked and diagnosed, not matched | 6 |
| Assembly, BIOS or runtime entry (no change) | 18 |
| Boundary fragment (no change) | 6 |
| C candidate not reached | 12 |

Closest remaining, with the cause found:

- 08014AE0 (serial receive), **3 lines** (was 131): the 080147D0 fix plus a
  `u64` receive copy. Left: an r0/r1 swap in the `0xFEFE` store. A traced
  local allocator shows the value register gets twice the address register's
  priority; the original's address had more references, and no natural form
  tried gives that.
- 08014104 (blend blit), **4 lines** (unchanged): a traced global allocator
  shows local-alloc doubles the live length of every REG_EQUIV register before
  priorities are compared. The original order needs `height` and the source
  base without the note and the destination base with it.
- 08006270 (sound mixer), **25 lines** (was ~100): array-indexed mix buffer,
  local position copied to and from the global. Left: hoist order of three
  address constants in the first loop. It does not respond to compiling after
  the sound unit or to 0–40 constant-pool label offsets.
- 08010910 (number to text), 27 lines (unchanged): the stored zero joins the
  flag's CSE class. `do {} while (0)` stops the first CSE pass but the second
  pass merges it again. Turning the second pass off breaks 18 installed
  matches, so the original ran it.
- 0800B3A0 78 lines (was 86) and 0800AC3C 213 lines (new) are in `drafts/`.

## Method notes

One function at a time, reading the target, then the compiler's own pass
dumps (`-dL -dG -dt -dl -dg`). A private copy of the pinned compiler source
with tracing in `global.c` and `local-alloc.c` (in the cache directory, not in
the repository) showed the allocator's real priorities and preferences. Small
variant batches (under 60 compiles each) were used only after a shape
hypothesis. No brute-force search. Builds and compiles ran at nice 15 with at
most 4 jobs. The matcher on worker A was not touched.

`src/types.h`: `TxraRecord` now names the signed halfwords at 0x56, 0x58,
0x5A and 0x60 (both 0800AC3C and 0800A940 scale them; layout unchanged), and
`TxraLinkState` names its buffers (see above).

## What is not done

- The other 46 entries in this slice do not match. Twelve C candidates were
  not reached, including all ARM bodies (08017F64 was only read).
- 0800A940 and 0800AC3C are a pair (stat scaling). Both have the right
  expression shape, but not the register roles: the original keeps the level
  in a high register and rebuilds the factor-row address for the tenth entry.
- The generated `docs/map/indirect.json` changes on this machine during
  `make`. It was restored each time and is not committed (as in slices e/f).
- No boot, title, race or save milestone was reviewed. Those progress fields
  are unchanged.

## Validation

- `make -B -j4`: `build/txra.gba: OK`, whole-ROM `cmp` identical, after each
  match and at the end.
- `make check`: **170 tests passed**.

## Review folder

`txra-review/deep-g/` has NOTES.md, captions.json, LOG.md (the
per-function table) and `drafts/`.

- `before/matching-status.png`, `after/matching-status.png`: 128 → 133,
  21.327% → 24.029%.
- `before/{08018BE8,080147D0,08012CC8}-listing.png` and
  `after/<entry>-listing.png` for all five matches. The original is on the
  left and our compile on the right, aligned by instruction. Red rows differ,
  green rows agree. All after rows are green.
- `matching-findings.png`: the change that made each match.
  `slice-outcomes.png`: all 51 entries by outcome.
- `080147D0-pointer-to-global.webm`: 8 s, 240 frames at 30 fps, no audio,
  1.46 MB. The link-setup loop through a local pointer (red), then through
  the global (all green). It is a listing, not gameplay.

All pictures and frames from both halves of the clip were opened and checked;
the text fits and rows are legible.

## Owner notes

OWNER-NOTES.md was absent at the start, before each major step and at the
finish, so there were no owner notes to act on.

Matched before/after: 128 / 133.
Percent before/after: 21.327% / 24.029%.
Learned: if the original leaves work inside a loop, its loop was longer at loop-optimisation time; address globals directly, and check a library's neighbours for its profile.
