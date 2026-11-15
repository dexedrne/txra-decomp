# 08016DA8: direct bucket insertion and packet lifetimes

Complete structured-C **nonmatch**, uninstalled and uncounted. The historical
`arm -O2 -mthumb-interwork` profile and full owner/pool end 08017E68 are unchanged.

| Source | Output bytes | Local frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained round 3 | 4,260 | 108 | 899 | 3,258 |
| `func_08016DA8.c` | 4,268 | 108 | 898 | 3,251 |
| Original owner | 4,288 | 96 | — | 0 |

The retained C improves by **seven differing bytes and one instruction edit**.
The recorded depth-pair/next-face experiment was first. Pair-load/add forms,
common next-face capture placements and the original-like add ordering did not
beat the previous source. The original direct bucket insertion separately
handles empty and nonempty links; restoring that ordinary C branch gives the
improvement. It preserves the same reads, link values and write count.

Further hand passes tested packet count/pointer lifetimes, signed 32-bit
index/depth declarations, typed packet fields, visibility and winding scopes,
and subdivision/face loop exits including a captured next-part identity. None
improved the retained result. Only the direct empty-bucket distinction is kept.
The final focused matching-pattern sweep was bounded to 4,000 source identities
and 15 minutes, around packet insertion, depth values and loop exits. It stopped
at the wall-time bound without another retained improvement.
Unused subdivision/projection templates were removed from the final source;
this reproduces exactly the same compiled owner hash.

## Structural differences

[structural.json](structural.json) separates original-address windows from
instruction-shape alignment. These are heuristic layout comparisons, not
additive causal byte attributions or a semantic proof.

| Cause | Remaining evidence |
| --- | --- |
| Allocation | 552 aligned pairs still differ in register operands. Setup A/C/B offsets and pointers and packet temporaries retain different spills. Near visibility/packets remain the largest window: 1,188 differing bytes in 1,592. |
| Scheduling / selection | 261 original and 254 compiled instruction rows remain unpaired. Subdivision corner loads, midpoint scratch writes and depth/count arithmetic are still selected or scheduled differently. |
| Control-flow layout | 22 aligned branch pairs have different destinations. The retained direct empty-bucket branch is closer, but the original near insertion still has distinct link paths and next-part/next-face joins. |
| Literal pools | 19 original versus 21 compiled referenced words; 24 aligned PC references differ. The first pool locations remain aligned, later projection/packet pools shift. Values are not printed. |
| Frame | 108 versus the original 96 local bytes. The 12-byte excess remains; the output deficit shrinks from 28 to 20 bytes. No padding, extra state object, fixed-register binding or artificial write was introduced. |

Next concrete step: preserve the direct empty-bucket distinction and recover
the current-packet head's pointer identity around original 08017DE4..08017E30.
The original reloads the packet pointer separately in the two link paths;
this C still shares it and emits a conditional link store. Try a typed view of
the existing current-head and bucket-entry globals, with the same physical
addresses and synthetic-memory mapping, to recover those alias/lifetime rules.
Keep count/kind reads and writes in order. Do not add volatility or artificial
reload side effects. The near insertion has the same issue at 08017A48..08017A88.
Simple postincrement/current-part scopes, signedness masks, typed packet fields,
depth add forms and loop-header spellings were already measured here.

The retained source passes the unchanged independent textual ARM executor:
**199 memory fixtures**, 20 fixed expected checks, three size checks and 14
field-offset checks, reaching all **1,053 original instruction addresses**.
Stable-input, valid-index and alias assumptions remain those of the existing
fixtures. This is not real-game execution or validation of malformed data.

`candidate.json` and `candidate-checks.json` pin the actual cleaned source.
The compressed search manifest includes rejected/oversize diagnostics; it has
no admission authority. Only the best full sanitized diff is plain text.
No original binary slice, encoding column or pool contents are retained.

```
python tools/measure_candidate.py docs/near-misses/arm-16da8-1109d/func_08016DA8.c 08016DA8 08017E68 arm build/arm-d-check
```

The schema-2 search archive interns repeated source/output identities and
measurements. Its tables declare every trial column; full 32-byte SHA-256
digests use lossless base64 encoding, while profiles retain hexadecimal hashes.
Every identity, metric and outcome is round-trip checked before packing. Only
random temporary-directory names are normalized in rejected diagnostics.
