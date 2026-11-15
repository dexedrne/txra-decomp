# 0800421C: shared scratch aliases and HUD allocation

All sources here are complete structured-C **nonmatches**, uninstalled and
uncounted. The owner includes the shared return at 080051FE and its final pools:
0800421C..08005238, 4,124 bytes. The original local frame is 36 bytes.

| Source | Output bytes | Frame | Instruction edit distance | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Prior 11/4 frame experiment | 4,200 | 36 | 1,181 | 3,894 |
| `func_0800421C.c` | 4,096 | 36 | 1,084 | 3,831 |
| `byte-control.c` | 4,104 | 36 | 1,124 | 3,830 |
| `allocation-control.c` | 4,012 | 44 | 1,071 | 3,888 |

The primary keeps the original frame and reduces instruction distance by 97 and
byte distance by 63. The byte control differs by one fewer byte but has forty
more instruction edits. The allocation control has the best instruction score
of this neighborhood but an incorrect 44-byte frame. None is a partial match or
replacement, and no frame/output padding was introduced.

Six separately named transform words are aliases of scratch records 8 and 9:
03005800..03005814 are offsets 96..116 from 030057A0. Expressing those assignments
through the existing triple array recovers the original shared address base and
reduces the frame experiment from 4,200 to 4,104 bytes. An explicit affine-counter
pointer, initialized at function entry before all conditional loops, produces the
retained 4,096-byte version. It still reads/writes the original global; no new
state object or cached counter value was introduced.

The smoke search was tried with its original index, a record pointer and four
component pointers. The record loop shrinks the code but does not beat the
primary's complete byte comparison. Six non-overlapping scalar role merges,
block-local sprite indices and declaration permutations were also measured.
`search.json` records twelve ordered shapes, 128 role/scope combinations, sixteen
mask probes, three safely initialized cursor controls, and the allocation/pattern
pass's 617 distinct sources / 37 distinct compiled outputs. Compiler profile
stays `old -O2 -mthumb-interwork`. No register pin or assembly was used.

The baseline exceeds the true next-owner end by 76 bytes, so the unchanged
checker rejects it. The independent compiler diagnostic can still measure it;
that diagnostic has no admission/installation authority and never supplies a
larger limit to the checker. Here every overrun byte counts as differing; the
older 3,892-byte receipt compared that tail with the following owner's bytes.
All retained new versions fit the unchanged strict end and fail exact equality.

Each retained source passes 1,024 synthetic state/ordered-helper-call fixtures
against the prior semantic C draft, with undefined-behavior sanitization. The
synthetic linker preserves all six transform aliases inside the scratch array.
The fixture covers display timers, menu/race states, valid gears and map modes,
reverse speed, letter/digit/space names, flash clamps, projected effects and
empty/full smoke searches. It checks complete touched state and ordered helper
arguments. It is **not** an independent original-instruction oracle or real game
execution. Projection/draw helpers are deterministic synthetic stubs, and invalid
gear/mode values, arbitrary aliases and hardware effects remain unproven.

Native checks use strict warnings except the inherited signed/unsigned glyph
range idiom; its unsigned comparison is deliberate and unchanged. They use O0
and separate translation units so synthetic linker aliases are observed through
real calls. Target comparisons always use the original historical O2 profile.

Reproduce with the existing project Python environment:

```
python tools/measure_candidate.py docs/near-misses/hud-owner-1109/func_0800421C.c 0800421C 08005238 old build/hud-1109-check
python3 docs/near-misses/hud-owner-1109/check_source.py
python3 docs/near-misses/hud-owner-1109/check_source.py --candidate docs/near-misses/hud-owner-1109/byte-control.c
python3 docs/near-misses/hud-owner-1109/check_source.py --candidate docs/near-misses/hud-owner-1109/allocation-control.c
```

Next concrete step: recover the mixed smoke-loop induction forms at
08005004..080050F0. The original retains count/x/y/z pointers plus a separate
16-byte offset; its first spawn path stores through base+offset, while the two
field_30 spawn paths use the component pointers. The tested all-index,
all-record and all-component versions do not reproduce that combination.
Keep the shared scratch aliases and entry-initialized affine pointer, express
those distinct store forms in C, then rerun the 1,024 regression fixtures and
whole-owner byte comparison. Do not add padding to close the 28-byte size gap.
