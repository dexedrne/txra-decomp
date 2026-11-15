# 0800421C: mixed smoke induction and temporary roles

Complete structured-C **nonmatches**, uninstalled and uncounted. Every strict
comparison covers 0800421C..08005238, including the shared return and final pools,
under the unchanged historical `old -O2 -mthumb-interwork` profile.

| Source | Output bytes | Frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained 11/9 primary | 4,096 | 36 | 1,084 | 3,831 |
| `func_0800421C.c` | 4,120 | 36 | 1,056 | 3,434 |
| `instruction-control.c` | 4,124 | 36 | 1,051 | 3,497 |
| Original owner | 4,124 | 36 | — | 0 |

The primary improves the full-owner comparison by **397 differing bytes** and
28 instruction edits while retaining the original frame. The control has the
original output length and five fewer instruction edits, but 63 more differing
bytes. Neither is an exact or partial replacement; size/frame agreement has no
admission authority.

The first smoke search now keeps moving count/x/y/z pointers and a distinct
16-byte offset. The first spawn stores count/y/z through base plus offset and x
through its component pointer; the two field_30 paths use component pointers.
Its bound follows the moving y pointer, preserving the original mixed induction
rather than the previously exhausted all-index/all-record/all-component shapes.
The six shared transform aliases and entry-initialized affine pointer remain.

Separating all temporaries in a phase is not consistently helpful. The retained
source gives the opening overlay its own source/index capture, and gives the
projected effects separate row index, glyph, y and transform-size roles, while
preserving the other shared scalar lifetimes. These ordinary C scopes recover
both original overlay stack slots at sp+20/+24. Granular role merges after the
mixed smoke pass produced the final improvement. No widths, compiler profile,
register bindings, assembly, artificial writes, state objects or padding changed.

The bounded searches cover the mixed first loop, the subsequent smoke update
loop, shared bases, phase scopes, granular merges, declaration order and existing
learned patterns. `search-summary.json` gives deduplicated counts and oversize
source counts; `search.json.gz` pins every visited source/output identity. Some
closer diagnostic outputs cross the owner end and were excluded from retained
selection. They never received a larger checker boundary. Invalid C declaration
hypotheses are recorded as compile failures, not successful checks.

Each retained source passes 1,024 existing synthetic state and ordered-helper-call
fixtures against the prior semantic C draft, with strict warnings and undefined-
behavior sanitization. The six transform aliases still point inside the scratch
array. These checks are **not an independent original-instruction oracle**, real
game execution, or proof for invalid gear/mode values, arbitrary aliases and
hardware effects. The reference and fixture implementation are unchanged.

Reproduce from the repository root with the existing project Python environment:

```
python tools/measure_candidate.py docs/near-misses/hud-owner-1109b/func_0800421C.c 0800421C 08005238 old build/hud-1109b-check
python3 docs/near-misses/hud-owner-1109/check_source.py --candidate docs/near-misses/hud-owner-1109b/func_0800421C.c
python3 docs/near-misses/hud-owner-1109/check_source.py --candidate docs/near-misses/hud-owner-1109b/instruction-control.c
```

Next concrete step: keep the recovered mixed smoke loop and scalar stack slots,
then recover the opening overlay's source/zero/counter lifetimes around
08004280..080042E8. The original keeps source in a low callee-saved register,
zero in a high register across the transform call, and the sprite-counter address
in another high register; the candidate exchanges those lifetimes and moves the
first pools. Try a block-local zero used across both opening helper calls while
ending the sprite-index capture at the first sprite. Compare the complete owner,
not just the four-byte size deficit. The separate control proves that closing
that deficit alone does not recover the bytes. Do not pad it or repeat the
second smoke loop's all-pointer/reset-index alternatives measured here.

Only the best candidate's full sanitized diff is uncompressed. The control diff
and search manifests are gzip files; no ROM slice, extracted binary, literal-pool
contents or raw instruction encodings are retained here.
