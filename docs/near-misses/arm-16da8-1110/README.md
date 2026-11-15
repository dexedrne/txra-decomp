# 08016DA8: positive near-path guards, no byte gain

Complete structured-C **nonmatch**, uninstalled and uncounted. The historical
`arm -O2 -mthumb-interwork` profile and full owner/pool end 08017E68 are unchanged.

| Source | Output bytes | Local frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Retained 11/9d | 4,268 | 108 | 898 | 3,251 |
| `func_08016DA8.c` | 4,268 | 108 | 898 | 3,251 |
| Original owner | 4,288 | 96 | — | 0 |

The retained source uses the decompiler's three positive near-path guards:
nonnegative depth, a visible corner, then nonpositive winding. It reproduces
the **same compiled hash** as the starting candidate and passes the independent
fixtures. This is a source-structure tie, not an improvement or exact match.
The best source available on this branch is 3,251, rather than the 3,249 figure
in the brief; no missing source or profile was invented to reconcile that gap.

[SHAPE.md](SHAPE.md) records the actual view and its stack-alias limitation.
The bounded trials covered projection's mixed-unit traversal, texture ladders
and shared final stores, near empty/nonempty insertion, positive predicates,
early next-part and next-face captures, ring exits and signed loop/depth roles.
No lower-distance output fit the unchanged boundary. Oversize outputs are
rejected diagnostics. The complete 317 source identities and 131 output
identities are recorded in the compressed manifest and
[search-summary.json](search-summary.json).

## Remaining structure

[structural.json](structural.json) separates positional original-address windows
from instruction-shape alignment. Counts include layout displacement and do not
form an additive causal decomposition or a semantic proof.

| Cause | Remaining evidence |
| --- | --- |
| Allocation | 552 aligned pairs differ in register operands; A/C/B offsets, coordinate pointers and packet temporaries retain different spills. |
| Scheduling / selection | 261 original and 254 compiled instruction rows remain unpaired. Corner loads, midpoint scratch writes, depth/count arithmetic and packet construction remain different. |
| Control flow | 22 aligned branch destinations differ, including subdivision skips, packet rejection and the face/ring back edges. |
| Literal pools | 19 original versus 21 compiled referenced words, with 24 differing aligned PC references. Stored values are omitted. |
| Frame | 108 versus the original 96 local bytes; output is 20 bytes short. No padding, volatile spill, fixed-register binding or added frame object is retained. |

Next concrete step: repair or independently annotate the corner-depth
store/indexed-load join in the working decompiler view **before treating its
temporary names as source identities**. Check the stack pointer relation at
08016E30..08016E6C against the indexed load at 08016EF8, using the initial
p-code stores and the repo's assembly. Then compare the four depth values and
A/C/B offset/pointer lifetimes at the near/direct join. The measured projection
induction, positive-guard, texture-tail and next-part/next-face variants have
already stalled; their prettier C shape is not a reason to retain worse bytes.

The source passes the unchanged **199 differential memory fixtures**, 20 fixed
expected checks, three size checks and 14 field-offset checks. All **1,053**
original instruction addresses are reached in the synthetic textual ARM
executor. These are synthetic states, not a real-game run or a byte match.

```
python tools/measure_candidate.py docs/near-misses/arm-16da8-1110/func_08016DA8.c 08016DA8 08017E68 arm build/arm-1110-check
```

The compressed recipes include the unchanged fixture runner's temporary source
selection. Only the best full sanitized diff is plain text; long diagnostic
manifests and the baseline diff are gzip files. No decompiler output or ROM
slice is present.
