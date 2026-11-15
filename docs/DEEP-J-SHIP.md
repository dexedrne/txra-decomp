# TXRA deep hand matching, slice j

Seven more routines build from ordinary C, and the ROM stays byte-identical.
Accepted totals move from **138 functions / 22,568 bytes / 26.509%** to
**145 / 27,934 / 32.813%** of the 85,132 mapped code bytes. Every match uses
the `old` profile. No flags, inline assembly or output patches.

| Commit | Entry | Bytes | What made it match |
| --- | --- | ---: | --- |
| c152b4d | 080020B8 | 708 | Count-up row copy (destination base hoisted first). The following clear loop reuses the outer counter `i`; that makes the outer `i + 1` isolated for GCSE's PRE, which then leaves it at the latch. |
| ea485d7 | 08010910 | 320 | The `g_03002E58` zero is an always-zero narrowed shift that only combine can prove, so CSE does not merge it into the `emitted` flag register; the old `do {} while (0)` workaround goes away. The exact original expression is unknown. |
| 1d5ee95 | 0800EDF4 | 530 | One palette read per channel (08015128's idiom) and a destination pointer computed before the colour is packed. |
| f11e4e1 | 0800BBD4 | 492 | Each camera-offset product in its own function-level variable shared by both blocks (not tied to the shift result); a block-scoped mask variable in the second block. |
| f29c4b8 | 08012A50 | 632 | Rewritten from the matched sibling 08012CC8; screen-base select as `g_03005FC0 == 0 ? 0x0600A000 : 0x06000000`. |
| 615146c | 080130BC | 1240 | Name-entry screen on the same template; the frame counter is reused after the loop as the letter count. |
| 2c915d8 | 08013594 | 1444 | Mode menu with two ten-way switches on the same template; case labels in the original emission order 0, 1, 8, 9, 2, 3. |

All 45 selected entries are accounted for in
[deep-j/OUTCOMES.md](deep-j/OUTCOMES.md). Two drafts improved without
matching, kept in `docs/deep-j/drafts/`: 08013E74 (85 to 18 differing
instructions; `k` and the cached record pointer swap r4/r5, a global-allocation
priority of 1.64 against 2.4) and 0800B4D8 (new draft on the title-loop
template, 273 normalized lines; loop.c strength-reduces `g_03002A30 + 384`
into a hoisted constant that the original keeps as `reg + 384`). 08008914
was worked without a match (the original keeps the constants 1 and 255 in
registers and spills two other values). 0800C850 was only read; its dead
`next + 1` increment is still unexplained. Eight C seeds were not reached
(080162F8, 080154AC, 0800AF4C, 0800CB5C, 080098DC, 0800E498, 0800F2D0 and
the ARM seed 080165BC). The 14 assembly, BIOS and runtime entries were
already recorded in `docs/asm-only.md`; no new entries were added.

`tools/review_deep_j.py` renders the review pictures and one muted clip
outside the repository (`txra-review/deep-j/`, run with the
venv's site-packages on `PYTHONPATH` because the venv has no Pillow).

Validation: after every match `make` ends in `build/txra.gba: OK`, `cmp` with
the base ROM is identical, and the 170-test suite passes. The generated
`docs/map/indirect.json` drifts locally during `make` and was restored, not
committed.
