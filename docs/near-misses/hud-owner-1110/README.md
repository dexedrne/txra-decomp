# 0800421C: selection order from the decompiler view

Complete structured-C **nonmatch**, uninstalled and uncounted. The unchanged
historical `old -O2 -mthumb-interwork` checker covers the full owner and pools,
0800421C..08005238.

| Source | Output bytes | Local frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained 11/9d | 4,124 | 36 | 1,013 | 3,235 |
| `func_0800421C.c` | 4,124 | 36 | 989 | 3,168 |
| Original owner | 4,124 | 36 | — | 0 |

The retained source improves by **67 differing bytes and 24 instruction
edits**. The decompiler's ordinary model selection first takes the low model-ID
path, and the gear icon first takes the nonnegative-speed path. Expressing
those two selections in that order improves the complete owner. Their helper
arguments, reads and call order stay the same. No decompiled C was pasted into
this source; these are branch inversions of our retained C.

[SHAPE.md](SHAPE.md) compares the actual decompiler view with the starting
candidate. The other trials followed its temporary lifetimes, mixed flash and
smoke traversal, nested mode guards, projected point/coordinate scopes and
source-base/offset join. They did not beat the retained source. A separate
decimal-workspace hypothesis also lost; it is not claimed as a recovered array.
The 661 measured source identities and 252 compiled output identities are
recorded in [search-summary.json](search-summary.json) and the compressed
manifest. Repeated source identities are measured once. Oversize outputs are
diagnostics and cannot become retained candidates.

## Remaining structure

[structural.json](structural.json) separates original-address positional
windows from instruction-shape alignment. These are layout aids, not additive
causal byte counts or semantic proof.

| Cause | Remaining evidence |
| --- | --- |
| Allocation | 485 aligned instruction pairs differ in register operands. The projected width/tag and coordinate priorities remain different. |
| Scheduling / selection | 297 original and 291 compiled instruction rows remain unpaired. Argument construction and spill loads still differ, especially around the gauges and projected effects. |
| Control flow | 71 aligned branch pairs have different destinations. The two retained selection orders improve the strip region, but later joins remain displaced. |
| Literal pools | 99 original versus 102 compiled referenced words, with 113 differing aligned PC references. Values are omitted. |
| Frame | The original 36-byte frame and 4,124-byte length are retained. Individual slots and register priorities still differ. |

Next concrete step: retain these two selections and inspect the **gauge speed
and digit join at 08004970..08004A10** with the read-only-cartridge view. The
original keeps hundreds across the first draw while tens and units occupy
separate local words; this candidate keeps units in a saved register and
assigns the player-record base differently. Compare an explicit hundreds product
and a separate scaled-tens argument captured before units, keeping all three
digit computations before their draws. Inspect the first differing allocation
at that join rather than expanding another role matrix. Do not repeat the completed five-scalar role sweep, pointer
capture matrix or digit-array hypotheses. Do not introduce volatile spills,
padding, fixed registers or a synthetic frame object.

The retained file passes the unchanged **1,024 state and ordered-call
fixtures**, with six transform aliases, strict warnings and undefined-behavior
sanitization. The reference is prior semantic C, not independently executed
original instructions. Valid-state and alias limits of those fixtures remain.

```
python tools/measure_candidate.py docs/near-misses/hud-owner-1110/func_0800421C.c 0800421C 08005238 old build/hud-1110-check
python docs/near-misses/hud-owner-1109/check_source.py --candidate docs/near-misses/hud-owner-1110/func_0800421C.c
```

Only the best full sanitized diff is plain text. The baseline diff, trial
manifest and authored experiment recipes are compressed; no ROM slice,
instruction encoding, pool contents or decompiler export is included.
