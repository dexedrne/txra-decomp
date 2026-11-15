# 08016DA8: near-first control flow and allocation pass

This is a complete structured-C **nonmatch**, never installed. The original
4,288-byte owner and all pools are compared under the unchanged historical
`arm -O2 -mthumb-interwork` profile and strict end 08017E68.

| Measurement | Prepared 11/7 control | Retained 11/9 candidate |
| --- | ---: | ---: |
| Compiled bytes | 4,028 | 4,016 |
| Local frame bytes | 92 | 88 |
| Instruction edit distance | 1,046 | 855 |
| Differing bytes, including missing tail | 3,850 | 3,677 |

The original has a 96-byte local frame. A smaller frame/output is not progress
toward completeness by itself; the improvement claimed here is the full-target
instruction and byte comparison. The retained C puts the near/subdivision path
before the direct path, expands the visibility expression at its call sites,
and spells the projection body in an ordinary local C block. A declaration-order
pass retains the closest instruction/byte pair. No arithmetic width, explicit
register binding, assembly, padding, profile or checker boundary was changed.

`prepare_candidate.py --check` reproduces the retained source. `search.json`
records five ordered source probes, sixteen cached-index/insertion/loop/stride
combinations, sixteen scope/backedge combinations, fifteen typed-global probes,
and thirty-two helper-scope combinations. The allocation/pattern pass then
visited 784 distinct sources and 236 distinct compiled outputs, including the
existing `matching_patterns` transformations. This is a bounded neighborhood,
not exhaustive original-source recovery. The old projection induction variant
and the excluded car-contact function were not rerun. The queued owners remain
uninstalled; `queue-admission.json` keeps their mapped metadata, whose short
sound/HUD extents are not whole-owner acceptance boundaries.

The direct source-index captures and packet-insertion branch variants did not
beat the retained instruction score. Hoisting those captures alone caused new
spills; the pointer/base live ranges still disagree. All their measured outputs
remain in the manifest, rather than being silently counted as matches.

The existing independent textual ARM executor versus actual compiled C passes
199 synthetic memory fixtures, 20 fixed checks, 3 record sizes and 14 field
offsets, reaching all 1,053 original instruction addresses (`semantics.json`).
The same aliasing/stable-input assumptions and unproven malformed cases from
the 11/7 reference apply. This is not a real-game execution or byte-match proof.

Reproduce the complete strict compiler comparison from the repository root:

```
python3 docs/near-misses/arm-16da8-1109/prepare_candidate.py --check
python3 docs/near-misses/arm-16da8-1109/check_semantics.py
# Use the existing project Python environment for Capstone:
python tools/measure_candidate.py docs/near-misses/arm-16da8-1109/func_08016DA8.c 08016DA8 08017E68 arm build/arm-1109-check
```

The `.diff.txt` files retain instruction operands/addresses, with raw encodings
and literal-pool contents removed. JSON records pin the source and compiler;
no ROM slice or binary output is retained here.

Next concrete step: replace the scalar-address geometry reads with typed point
array indexing, preserving separate x-component byte offsets and y/z pointers
outside the four-part loop. Begin at the original 08016E08–08016EF0 setup:
recover the shared point base and original A/B/C offset/pointer spills before
changing projection arithmetic. Current output still allocates 88 rather than
96 local bytes; simply hoisting four pointer values was tested and is insufficient.
Keep the near-first flow and rerun the 199-fixture differential check afterward.
