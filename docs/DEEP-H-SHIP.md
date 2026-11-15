# TXRA deep hand matching, slice h

Five more routines build from ordinary C, and the ROM stays byte-identical.
Accepted totals move from **128 functions / 18,156 bytes / 21.327%** to
**133 / 20,268 / 23.808%** of the 85,132 mapped code bytes. (The task brief
quoted 20.97%; that figure was the stale header in DECOMP.md, which also had a
leftover merge line. Both are corrected from `tools/rom.cfg`.) Every match
uses the `old` profile. No flags, inline assembly or output patches.

| Commit | Entry | Bytes | What made it match |
| --- | --- | ---: | --- |
| c741f37 | 0800B908 | 716 | A `u16` angle in the second rotation block lengthens a competing value's pre-combine live range and flips one r8/r9 tie. |
| bde43f1 | 08009D94 | 496 | The corner height difference goes into `distance` before `width = distance >> 2`; a block-local temporary would be tied to `width`. |
| f170ffc | 08015128 | 216 | Repeated palette reads (merged by CSE into one halfword value) and channel variables shared by both fade loops. |
| b5f7630 | 08014FF4 | 308 | Same idioms; the toward-white blend is written step by step so the scale is not folded. |
| f916a3f | 08007398 | 376 | Count-up wave-RAM loops through a non-volatile pointer, which the loop optimiser reverses; compiled in the ROM-order sound unit, where the last register tie resolves. |

All 50 selected entries are accounted for in
[deep-h/OUTCOMES.md](deep-h/OUTCOMES.md). Two drafts improved without
matching: 08014CE4 (35 to 2 instructions) and 080020B8 (71 to 7), kept in
`docs/deep-h/drafts/`. 08013E74 did not move.

`tests/test_match4.py` now re-ranks 08015128 as a fixture after it landed (the
same treatment the test already gives 08014614), so the high-register hint is
still exercised.

Validation: `make -B` ends in `build/txra.gba: OK`; `cmp` with the base ROM is
identical; the 170-test suite passes. The generated `docs/map/indirect.json`
drifts locally during `make` and was restored, not committed.
