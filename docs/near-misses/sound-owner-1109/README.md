# 080064A4: complete sound-owner source/allocation pass

All retained files are complete structured-C **nonmatches**, uninstalled and
uncounted. Every strict comparison covers 080064A4..08007398, including pools,
under the original historical `old -O2 -mthumb-interwork` profile.

| Source | Output bytes | Local frame | Instruction edit distance | Differing bytes |
| --- | ---: | ---: | ---: | ---: |
| Prior corrected 11/7 source | 2,996 | 44 | 1,541 | 3,568 |
| `func_080064A4.c` | 3,644 | 104 | 1,467 | 3,473 |
| `frame-control.c` | 3,624 | 108 | 1,476 | 3,498 |
| `phased-fields.c` | 3,716 | 92 | 1,397 | 3,537 |

The target is 3,828 bytes with a 108-byte local frame. The primary candidate
retains the lowest complete byte distance of these validated hypotheses. The
frame control and phased version have different tradeoffs; neither supersedes
the primary's byte score, and frame agreement alone is not an acceptance gate.
The former 832-byte size deficit is now 184 bytes in the primary, 112 in the
phased version. These deficits are distinct from the byte-distance column.

The first private-host diff established that the old C collapsed many original
field-address temporaries into one voice pointer. Source work restores reviewed
field-address identities with the existing 72-byte stride, caches the pointers,
uses constant channel references inside their channel tests, and preserves an
explicit original command index and the two-stage global-volume arithmetic.
All aliases are the existing voice base plus documented field offsets; no table
contents, additional state objects, assembly, padding or register pins are used.
The phased version caches six fields at voice preparation, creates command-only
pointers inside their block, and makes the noise channel accesses constant too.

`search.json` records the bounded source families and measurements, including
narrowed hardware-store temporaries, pointer counts, command backedges, source
scopes and declaration order. Its allocation/pattern sweep visited 636 distinct
sources and 603 compiled outputs using the existing `matching_patterns` rules.
There was no compiler-family sweep. The primary, frame control and phased version
all remain within the original owner end and fail full equality.

Each retained version passes the same seven actual-C synthetic fixture groups
with strict warnings and undefined-behavior sanitization. The test wrapper reuses
the unchanged 11/7 fixture body and supplies linker aliases into the existing
synthetic voice array, just as that fixture already supplies the step-table alias.
It creates no independent field storage. `*-checks.json` pins each tested source.
These are synthetic state assertions derived from the tracked instruction paths,
not an independent processor oracle, real audio/device execution, or coverage of
arbitrary malformed streams/aliasing. The 11/7 source's documented limits remain.

Reproduce from the repository root with the existing project Python environment:

```
python tools/measure_candidate.py docs/near-misses/sound-owner-1109/func_080064A4.c 080064A4 08007398 old build/sound-1109-check
python3 docs/near-misses/sound-owner-1109/check_source.py
python3 docs/near-misses/sound-owner-1109/check_source.py --candidate docs/near-misses/sound-owner-1109/frame-control.c
python3 docs/near-misses/sound-owner-1109/check_source.py --candidate docs/near-misses/sound-owner-1109/phased-fields.c
```

Next concrete step: start from `phased-fields.c` and recover the six preparation
pointer slots (original sp+30, +34, +44, +48, +4C, +50) before tuning the command
block's three additional pointers. Keep the voice counter in its original high
register through those phases by shortening the command/envelope temporary live
ranges; the all-at-once capture instead spills it. Reconcile the 16-byte remaining
frame deficit and per-channel u16 hardware-result lifetime together. The narrowed
store family and simple register-storage hints were already measured here; do not
repeat them as a compiler sweep. Complete byte equality remains mandatory.
