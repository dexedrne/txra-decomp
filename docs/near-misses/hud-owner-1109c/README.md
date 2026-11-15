# 0800421C: strip positions and map/effect lifetimes

Complete structured-C **nonmatches**, uninstalled and uncounted. The unchanged
historical `old -O2 -mthumb-interwork` checker covers the entire owner and pools,
0800421C..08005238. No boundary was enlarged.

| Source | Output bytes | Frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained round 2 | 4,120 | 36 | 1,056 | 3,434 |
| `func_0800421C.c` | 4,124 | 36 | 1,048 | 3,258 |
| `instruction-control.c` | 4,124 | 36 | 1,045 | 3,260 |
| Original owner | 4,124 | 36 | — | 0 |

The primary improves by **176 differing bytes** and eight instruction edits.
The control trades two differing bytes for three fewer instruction edits. Both
have the original frame and length; neither is admissible as a replacement.

The recorded opening-overlay experiment was attempted first: local zero across
both calls, ending the sprite-index capture at its call, source identity and
counter-address scopes. It stalled. Separating the four strip/text horizontal
positions then improved allocation. The retained source also separates the
strip index, map scale/base/x, and projected width from unrelated HUD scalars.
The opening scale selection is an ordinary conditional expression and the sprite
attributes have their own capture. The recovered mixed smoke induction, six
transform aliases, field widths and helper-call order remain intact.

## Structural diff of the best candidate

[structural.json](structural.json) counts positional differences in original
address windows and separately aligns instruction shapes with register names
and local/PC displacements removed. Its counts are layout evidence, **not an
additive causal decomposition** or proof that moved blocks are equivalent.

| Cause | Remaining region / evidence |
| --- | --- |
| Allocation | 525 shape-aligned instruction pairs have different register operands. The opening 08004280..080042EC still assigns source/zero/counter to different saved registers. Map/flash 08004A88..08004C96 and projected effects 08004C96..08004FFA retain long coordinate/base lifetimes. |
| Scheduling / selection | 245 original and 237 compiled instruction rows are unpaired by shape alignment. Sprite argument setup, gauge scalar spills and the projected left/right setup contain reordered or different instruction sequences. The projected-effect window has 838 of 868 bytes different positionally; this includes shifts from earlier regions. |
| Control-flow layout | 71 aligned branch pairs have different encoded destinations. Opening skips, map continues, effect guards and the common return move; no new behavior is inferred from the destination count. |
| Literal pools | 99 original versus 103 compiled referenced pool words; 138 aligned PC-reference pairs differ. The first large pool starts four bytes earlier in the candidate, with later gauge/effect pools also displaced. Stored values are not printed. |
| Frame | Local frame is the original 36 bytes. Matching size/frame leaves the register and stack-slot assignment unresolved; no padding or artificial writes were added. |

A focused follow-up also tried separate decimal speed/hundreds/tens/units
lifetimes, quotient/remainder expressions and shared digit-call arguments in
08004970..08004A10. None beat the retained sources; `hud-gauge` is included in
the manifest and summary rather than being left as an untried next step.

Next concrete step: retain these scopes and recover the source-row component
identities at original 08004CD4..08004D20 and the corresponding second row.
The original keeps a 24-byte row offset, then distinct x/y/z addresses in r5/r4/r2
while it writes the four scratch triples. Capture those component addresses
from the existing row array, keep their lifetime before the four transform
calls, and compare the full owner. Do not introduce cached component values:
the existing scratch aliases and repeated reads must remain visible. Opening
zero/counter combinations, per-effect coordinate/pointer scopes and decimal
role splits stalled here; avoid repeating those neighborhoods.

Both retained sources pass the unchanged **1,024 synthetic state and ordered-call
fixtures** against the prior semantic C, with strict warnings and undefined-
behavior sanitization. This is not an independent original-instruction oracle,
real-game execution, or validation for malformed mode/gear states and arbitrary
aliasing. Formatting and removal of unused declarations reproduce identical
compiled hashes. Search manifests include rejected C scope hypotheses and
oversize diagnostics; only retained sources receive the unchanged strict check.

```
python tools/measure_candidate.py docs/near-misses/hud-owner-1109c/func_0800421C.c 0800421C 08005238 old build/hud-1109c-check
python3 docs/near-misses/hud-owner-1109/check_source.py --candidate docs/near-misses/hud-owner-1109c/func_0800421C.c
python3 docs/near-misses/hud-owner-1109/check_source.py --candidate docs/near-misses/hud-owner-1109c/instruction-control.c
```

Only the primary full sanitized diff is uncompressed. The control diff and long
search manifest are gzip files; no ROM slice, extracted binary, raw instruction
encoding or literal-pool content is retained.
