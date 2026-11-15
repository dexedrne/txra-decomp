# Uninstalled recovery, 11/4 continuation

080076F4 is now a complete installed match in `src/generated/`; its earlier
11/4 draft remains historical. None of the C files in this folder is installed
or counted in the 179-match total.

| File | Output / complete target | What remains |
| --- | --- | --- |
| `func_080181C0.c` | 1,644 / 1,684 bytes, ARM; 60 / 72-byte local frame | Explicit 25-word x/z member arrays and a cached other-car z value improve setup and pair-cache register choices. Rotation loads are still hoisted differently, cached offsets do not match, and allocation remains unresolved. |
| `func_0800421C-frame.c` | 4,200 / 4,124 bytes, old Thumb; 36 / 36-byte local frame | A diagnostic alternative with shared temporaries and a common countdown-size result. It reproduces the local frame size but still differs extensively in instructions, loop hoisting and the smoke-slot search. The 11/3 source remains the semantic reference; this experiment is not a closer complete byte match. |
| `func_080064A4-prefix.c` | 576 diagnostic bytes; incomplete source | Compiled source through the fade, buffer handling, two callbacks, four hardware-channel sequence records and PCM tick gate. The eight-voice PCM body beginning at 08006712 is absent. The final early return is a diagnostic stopping point and changes behavior. It cannot be installed as a prefix match. |

`results.json` records complete compiler comparisons for the first two drafts.
The `.diff.txt` files omit raw instruction encodings and original literal data.
The row score counts additions plus removals in the complete instruction diff,
including shifted branch targets; it is not the normalized score used to guide
local experiments. Neither draft has been independently behavior-verified.
The contact instruction diff falls from the earlier snapshot's 528 rows to
363, while its different-byte count falls from 1,237 to 1,143. It still fails
the complete comparison.

The HUD uses the following non-overlapping phases to share local names:
`scale` becomes `t`, `speed` becomes `n`, selector and tile roles become `c`,
`width` becomes `angle`, and `height` becomes `size`. A wider mutation that
merged simultaneously live scale and divisor values also produced a 36-byte
frame; it was rejected rather than retained as a valid source improvement.
Correct frame size alone does not establish a match.

The sound prefix retains the nine-word fade table as an extern aggregate copied
to a local value; no table contents were extracted into source. Its four
sequence records have a 12-byte stride; their paired voice records have a
72-byte stride. Events advance by five halfwords. The 254/253 stop case,
redirect-to-index-minus-one case, 255 stop case and the four register-pair
writes are now expressed in C. This prefix was checked with the actual old
compiler, but its missing enclosing body prevents meaningful full-frame or
whole-function acceptance.

The smallest remaining mapped entries were rechecked. They are runtime/BIOS
interfaces, raster/interrupt code or already documented internal entries;
covered entries must not be scheduled as independent C functions. The track
streamer and ARM track-face renderer remain at the boundaries documented in
`../hand-20261104/large-bodies.md`. No new standalone match is claimed there.
