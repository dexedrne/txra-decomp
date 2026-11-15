# TXRA deep hand matching, slice j, third pass (j3)

Seven more routines build from ordinary C and the ROM stays byte-identical.
Accepted totals move from **147 functions / 28,714 bytes / 33.729%** to
**154 / 35,832 / 42.090%** of the 85,132 mapped code bytes. Every match uses
the `old` profile. No flags, inline assembly or output patches.

The brief named this "slice j"; earlier slice j and l passes already exist
(`docs/deep-j/`, `docs/deep-l/`, `DEEP-J-DONE`), so this pass is recorded as
j3. Selection: the 82 unmatched entries from `tools/rank_targets.py --json` on
main at 147 matches, sorted by `(bytes, address)`, zero-based odd indices
`[1::2]`: 41 entries. The even-index half belongs to the parallel slice and
was not touched.

| Commit | Entry | Bytes | What made it match |
| --- | --- | ---: | --- |
| 3de47c0 | 0800B3A0 | 310 | Point plot. The pixel value is one function-level variable used by both parity branches; the odd branch then has two local quantities instead of three, so local-alloc's fixed three-element sort no longer forces x >> 1 into r0. |
| 6ea7955 | 0800C850 | 372 | Track-position update on the 0800C9C4 template. The dead `next + 1` is an unused second wrap whose compare jump later deletes; fields indexed directly; row address `at * 28 + base`. |
| 50feb26 | 0800A940 | 764 | Stat scaling. A two-dimensional `s16 [][10]` stats array, one function-level product temporary, and factors built in two statements so fold cannot reassociate them. |
| 513d2c1 | 0800AC3C | 784 | Its sibling. The grade is read through the product temporary; the /16 and /64 factors are two variables (one variable outranks the base registers). |
| 30c3ef3 | 0800A17C | 1096 | Race HUD bars (deep-a draft finished). `TxraRecord.field_4c`, next row taken before the last copy, bonus values held in temporaries before their stores (frees r3 for a PRE reaching register). |
| b4040c6 | 0800C3C4 | 1164 | Steering and heading (deep-c candidate rewritten). Nested flag tests, a direct record access opening each block, one record pointer per block, one shared `diff`. |
| 76fd7ae | 08005238 | 2628 | Menu sprite builder (deep-a draft finished). A two-dimensional column table gives loop.c a second use of `i * 2`, so it strength-reduces it like the original; `slide + 120` inline after the loop, where PRE places it; one shared call-result variable; cursor source through `source`. |

All 41 entries are accounted for in [deep-j3/OUTCOMES.md](deep-j3/OUTCOMES.md).
Two drafts improved without matching, kept in `docs/deep-j3/drafts/`:

- 0800841C (palette fade by track tile): new draft, 3 differing rows. The
  three palette loops match once written with array indexing; the tile byte
  of the first two range blocks gets the original r1 through one shared
  function-level variable, but the third block keeps r0 with every variable,
  type and sharing combination tried (about 300).
- 0800BDC0 (AI lane choice): deep-a's raw-offset draft moved to struct fields
  (673 to 255 normalized rows); the lane switch now matches. Left: the angle
  delta and the index product swap r5 and r8, which shifts later registers.

08016C18 (ARM) was worked without a match: same length, but the original adds
the 0x02014000 base as two immediates per outer iteration where ours hoists
it. Six C seeds were not reached (08010A50, 080095E4 and the ARM bodies
08017F64, 080076F4, 080181C0, 08016DA8). The 14 assembly, BIOS and runtime
entries were already recorded in `docs/asm-only.md`; nothing new was added.

`TxraRecord` gains offset-named fields at 0x30, 0x3a, 0x3e, 0x40, 0x42, 0x44,
0x4a, 0x4c, 0x4e and 0x54, and `TxraRow28` its tile bytes at 0x0e, 0x0f, 0x10
and 0x16. Both layouts are unchanged (same sizes and offsets).

`tools/review_deep_j3.py` renders the review pictures and one muted clip
outside the repository (`txra-review/deep-j/round3/`; run it with
system Python and the venv's site-packages on `PYTHONPATH`, because the venv
has no Pillow).

Validation: after every match `make` ends in `build/txra.gba: OK`, `cmp` with
the base ROM is identical, and the 170-test suite passes. The generated
`docs/map/indirect.json` drifts locally during `make` and was restored, not
committed. No OWNER-NOTES.md was present in the repository during this pass.
The README progress block is rewritten by the project job and was left alone.
