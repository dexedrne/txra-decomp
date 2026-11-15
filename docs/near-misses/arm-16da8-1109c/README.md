# 08016DA8: direct-path reads and near geometry allocation

Complete structured-C **nonmatches**, uninstalled and uncounted. The historical
`arm -O2 -mthumb-interwork` profile and full owner/pool end 08017E68 are unchanged.

| Source | Output bytes | Local frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained round 2 | 4,220 | 120 | 859 | 3,401 |
| `func_08016DA8.c` | 4,260 | 108 | 899 | 3,258 |
| `frame-control.c` | 4,252 | 104 | 882 | 3,363 |
| Original owner | 4,288 | 96 | — | 0 |

The primary improves the full-owner distance by **143 differing bytes**, and the
frame excess falls from 24 to 12 bytes. Instruction distance regresses by 40.
The lower-frame control is eight bytes above the original frame and has fewer
instruction edits than the primary, but 105 more differing bytes. These tradeoffs
do not establish a recovered original allocation or authorize installation.

The recorded next step was applied to the single-cursor control first. Direct
screen reads now use their own face-index expressions rather than carrying all
four near-geometry identities into that branch. The primary captures C's direct
point address for depth and screen uses, while A/C/B near x offsets remain
separate from their typed y/z pointers. The point-array base begins at each face;
the ring update no longer carries an unnecessary next-ring value. One face
cursor remains. Projection arithmetic and its induction are unchanged; unsigned
word operations still wrap before signed right shifts.

## Structural diff of the best candidate

[structural.json](structural.json) gives original-address windows, original block
counts and global instruction-shape alignment. Positional differences include
shifts from earlier code; these are **not additive per-cause byte counts**.

| Cause | Remaining region / evidence |
| --- | --- |
| Allocation | 549 shape-aligned pairs differ in register operands. Setup 08016E08..08016EF0 still assigns the index/depth and A/C/B offset/pointer spills differently. The near visibility/texture/packet region 08017470..08017AA8 has 1,188 positional differing bytes in 30 original blocks, the largest remaining window. |
| Scheduling / selection | 261 original and 252 compiled rows remain unpaired by shape alignment. Subdivision 08016EF0..08017308 still schedules corner loads, midpoint sums and scratch writes differently; packet finalization also forms depth sums and bucket addresses differently. |
| Control-flow layout | 22 aligned branch pairs have different encoded destinations. Four subdivision guards, rejection paths and face/ring back edges move. The near-first path and signed visibility/winding tests remain in the semantic source. |
| Literal pools | 19 original versus 21 compiled referenced pool words; 24 aligned PC-reference pairs differ. The first two pool words happen to remain at their original locations while later projection/packet pools shift. No stored values are printed. |
| Frame | 108 versus 96 local bytes; the control is 104. The original depth array is at fp-56..fp-44, with distinct A/B/C offset and pointer spills plus one next-face spill. Extra live values still change later spill placement. |

Next concrete step: keep this source's direct-path reads, then work in packet
finalization, original 080179E8..08017AA8 and the direct path's matching bucket
insertion. The original loads the middle depth pair together, adds A+D before
the middle pair, and carries one next-face slot at fp-124. Recover the depth-pair
load/add lifetime and common next-face value without making a second face cursor
live through subdivision. Compare the full owner and frame after each edit.
Simple far-point aliases, face-address spellings, declaration orders and depth
capture subsets were measured here; do not rerun them as a compiler sweep.

Both retained actual-C sources pass the unchanged independent textual ARM
executor: **199 synthetic memory fixtures**, 20 fixed expected checks, three
layout sizes and 14 field offsets, reaching all **1,053** original instruction
addresses. Stable-input, valid-index and alias assumptions from the existing
fixture still apply. This is not real-game execution or proof for malformed data.
Formatting and removal of the unused ring declaration retain the compiled hash.
Invalid historical-C declaration hypotheses and oversize outputs are recorded
as rejected diagnostics, never matches or successful semantic checks.

```
python tools/measure_candidate.py docs/near-misses/arm-16da8-1109c/func_08016DA8.c 08016DA8 08017E68 arm build/arm-1109c-check
python3 docs/near-misses/arm-16da8-1109c/check_semantics.py
python3 docs/near-misses/arm-16da8-1109c/check_semantics.py --control
```

Only the primary full sanitized diff is uncompressed. The control diff and long
search manifest are gzip files. No ROM slice, extracted binary, raw instruction
encoding or literal-pool content is retained.
