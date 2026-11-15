# 08016DA8: complete body recovery and ARM-profile candidate

The entire control-flow body is now expressed in readable C, including the near
path, all four subquads, projection, rejected-packet writes, special kind-3
records, and depth-list insertion. There are no omitted blocks, TODOs, assembly
inserts or registry changes. All 19 literal target addresses have now been verified on the private host;
completeness of the body is not a claim that all possible inputs have been verified.

`func_08016DA8.c` is the compact semantic reference. `func_08016DA8_match.c` is
the prepared matching-profile source: the original's repeated stores and corner
tests are expanded, while its real loops remain loops. It also uses external
address identities, following accepted ARM neighbors `08017E68` and `08018854`.
`prepare_match.py` deterministically produces it; `--check` detects drift. This
is one evidence-driven source shape, not a compiler/permutation search.

Both sources compile with the installed historical `arm` and `modern-arm`
profiles, with no out-of-line calls. The prepared historical candidate is
**4,028 bytes versus the target extent of 4,288**; the modern candidate is 5,604.
The compact reference is 2,856 / 2,596 respectively. All are known nonmatches by
length. Strict existing relocation handling agrees with the independent linker
using verified target addresses. Source-assembled instructions and all pool words
match the original 4,288-byte extent exactly. The three legal-size C/profile
combinations compare as nonmatches; the 5,604-byte modern matching candidate is
rejected by the unchanged next-entry guard. No accepted replacement, whole-ROM
build, new match, runtime acceptance or performance gain is claimed.

## Instruction map

Ranges below are inclusive instruction addresses, not function boundaries.

| Original range | C block / behavior |
|---|---|
| 08016DA8–08016DD8 | APCS frame; load tick; start `(tick-29)&31`, stop `(tick-6)&31` |
| 08016DDC–08016E04 | Ring row `02033B70 + slot*1344`, remember next slot; skip empty row |
| 08016E08–08016E8C | Four indices at face+4..16, point addresses `02014000+index*28`; capture signed depths; all >767 selects direct path |
| 08016E90–08016F10 | Prepare four-part loop; skip a part only if its original saved corner depth is negative |
| 08016F14–08017004 | Part 0 geometry, component-major stores: A, AB, AC, AD |
| 08017008–080170F4 | Part 1 geometry: AB, B, BC, AC |
| 080170F8–08017204 | Part 2 geometry: AC, BC, C, DC; branch around first pool |
| 08017208–08017304 | Part 3 geometry: AD, AC, DC, D |
| 08017308–0801746C | `project_subquad`: capture camera/offset z once; four points; wrapped MUL/MLA, signed shifts, depth-scratch writes at stride 12; reciprocal projection |
| 08017470–08017508 | Near visibility: one same corner must have unsigned x<=119 and signed y in 0..159 |
| 0801750C–080176E0 | Expand y0/y1 by -1, x0 by -1, x1 by +1, narrow first; y lower and upper passes; x lower and upper passes; branch around second pool |
| 080176E4–08017720 | Near signed winding after expansion/clamps; reject positive result |
| 08017724–080179D4 | Four UV subquad cases, corner-major u/v stores; word averages wrap/ASR before byte narrowing |
| 080179D8–08017A88 | Shared near packet count/kind, original-depth bucket, prepend, advance packet pointer; both empty/nonempty cases |
| 08017A8C–08017A9C | Next part, inclusive 0..3; advance face after fourth part |
| 08017AA8–08017B8C | Direct packet coordinate halfword writes, followed by the same paired-corner visibility rule |
| 08017B90–08017BD8 | Direct winding BEFORE x clamps; preserve next-face address on rejection |
| 08017BDC–08017C6C | Kind-3 side record: flag, wrapped sx1+sx0 (no half!), ASR midpoint sy2/sy0, `(sx1-sx0)<<1`, counter increment |
| 08017C70–08017D6C | Direct x clamps only; four original low-byte UV pairs |
| 08017D70–08017E08, 08017E20–08017E38 | Direct count/kind/bucket/prepend and next-face; branch around final pool |
| 08017E3C–08017E64 | Face sentinel loop; next ring modulo 32; stop comparison; APCS restore/BX |

Full extent `[08016DA8,08017E68)` is **4,288 bytes**: 1,053 instructions
(4,212 bytes) plus 19 pool words (76 bytes). The 96-byte local allocation plus
44-byte APCS save occupies 140 stack bytes. The source-assembled fixture checks
all internal label offsets and passes the existing ARM leaf admission gate.
Admission is advisory, not a semantic or byte-equality proof.

The mapped caller at `08005F3A` loads the ARM target from pointer slot
`080200D0` through `08018DE0`, resolving to the `03003540` copy. The accepted
startup C copies `0x465` words starting at `08016DA8` to that address. That
copy extends beyond this leaf; it is not a reason to enlarge its C boundary.
Pointer inventory references at `08018A34`, `08018A38`, and `080200D0` were
reviewed. No internal branch leaves this leaf or enters its literal pools.

## Layout and ordering

| Record | Byte offsets and size |
|---|---|
| Point | xyz 0/4/8, active 12 (unused here), sx 16, sy 20, depth 24; stride 28 |
| Face | kind u16 at 0, unused halfword 2, four word indices 4..16, four word u 20..32, four word v 36..48, count u16 at 52, untouched halfword 54; stride 56 |
| Packet | signed halfword x[4] at 0, y[4] at 8, byte u[4] at 16, v[4] at 20, count u16 at 24, kind u16 at 26, next ARM32 address at 28; stride 32 |
| Ring row | 1,344 bytes = 24 face-sized slots; scan ends at zero kind, with **no added 24-face bound** |
| Scratch quad | four triples, stride 12, component-major generation; four projected depths written separately at stride 12 |
| Kind-3 side record | flag at base+16*n, x sum at +4, y midpoint at +8, width at the separate width-base+16*n |

The midpoint operation wraps the **32-bit sum before ASR 1**. Geometry uses
diagonal AC as the center, while UV uses diagonal BD. This difference follows
the instructions and is retained. Signed comparisons, signed halfword loads,
unsigned visibility x loads, byte stores and narrow-before-clamp behavior are
explicit. MUL and MLA retain only the low word; no long multiply is present.
All producing shifts are parenthesized through `asr32`, and multiplication and
address arithmetic use unsigned 32-bit operands to avoid signed overflow UB.

Near and direct paths intentionally differ: near expands/clamps before winding
and clamps y; direct winds before x clamps and leaves y unchanged. Both write
coordinates even when subsequently rejecting the packet. Near uses original
four depths for every subquad's bucket, not its reprojected scratch depths.
The bucket is `ASR7(wrapped depth sum)+32`, clamped signed to 0..255. Kind 2
becomes packet kind 1, kind 4 becomes 2, all others become 0. Insertion writes
next, advances the current pointer by 32, then publishes the previous packet as
the bucket head. No capacity guard absent from the assembly was added.

Principal original frame roles: fp-38/-34/-30/-2C are depths A/B/C/D;
fp-3C is the stop slot; fp-40 is part; fp-44/-48/-4C hold indices B/C/D;
fp-50/-54, -58/-5C and -60/-64 hold A/B/C byte offsets/pointers; fp-68/-6C
capture camera/offset z; fp-70 points to saved depths; fp-74 is next ring;
fp-78 is next part; fp-7C is next face; fp-80 is the scratch z cursor;
fp-84/-88 are the parallel byte/component counters. The LDMDA at 080179E4
and 08017D80 loads depths B then C, despite naming r0 as both base and result.
The C preserves these values and their memory effects without binding C locals
to original registers or claiming an identical compiled frame.

## Literal references and input assumptions

Every PC-relative load uses ARM PC+8. The following table enumerates **all** pool
locations; repeated loads are covered by the range map and source fixture.
All 19 semantic pointer targets were independently verified against the SHA-1-pinned
original on its existing private host. The ROM stayed there and was not modified;
only pointer identities and comparison results were retained.

| Pool address | Target / role |
|---|---|
| 08017198 | 030001B8, ring tick (load at 08016DB0) |
| 0801719C | 030057A0, scratch geometry write base (08016EC4) |
| 080176B4 | 03005F70, camera triple |
| 080176B8 | 030057A0, scratch geometry read base |
| 080176BC | 03005F80, projection offset triple |
| 080176C0 | 03002A18, first rotation coefficient |
| 080176C4 | 03001B28, second rotation coefficient |
| 080176C8 | 03000DF8, second rotation coefficient pair |
| 080176CC | 03005F58, second rotation coefficient pair |
| 080176D0 | 030055F8, projected-depth scratch write base |
| 080176D4 | 0804F330, reciprocal table base |
| 080176D8 | 030021C4, current packet pointer |
| 08017AA0 | 030021C4, same pointer in near insertion |
| 08017AA4 | 03000670, 256 bucket heads |
| 08017E0C | 030021C4, same pointer in direct path |
| 08017E10 | 03000DE0, kind-3 side-record counter |
| 08017E14 | 03000AD0, kind-3 record base |
| 08017E18 | 03000ADC, kind-3 width base |
| 08017E1C | 03000670, bucket heads in direct insertion |

The pointer identities are recorded in `pool-target-addresses.json`. The depth
scratch is 030055F8; the special record and width bases are 03000AD0 and
03000ADC. The earlier synthetic record addresses were replaced in both test
and candidate bindings. Their separation and alias relationships remain explicit.
`private-host-comparison.json` records source-assembly equality and the bounded
C comparisons. The original runner returned 1 because its final summary rejected
any exception, including the expected oversized-candidate rejection. The retained
result classifies that unchanged boundary guard as a nonmatch; it was not bypassed.

Behavioral assumptions: valid aligned source indices and sentinel-terminated
rows; valid packet/side-record capacities; stable camera/coefficient globals
through the leaf; source geometry/faces, scratch, packet output, bucket heads
and globals do not destructively overlap beyond the intentional packet/list
and side-record aliases. The original also has no input/capacity guards.
Malformed arbitrary aliasing or concurrent mutation is not proven equivalent:
the C can reload invariant indices at different times. Signed conversion and
right shift use the established little-endian, two's-complement GCC ARM32
conventions; the synthetic host uses the same conversions. Projection-table
indices are reproduced without inventing near-depth division guards.

## Checks and how to reproduce

```sh
python3 docs/near-misses/arm-16da8-1107/prepare_match.py --check
python3 docs/near-misses/arm-16da8-1107/check_semantics.py
python3 docs/near-misses/arm-16da8-1107/check_semantics.py --candidate func_08016DA8_match.c
~/opt/txra-venv/bin/python docs/near-misses/arm-16da8-1107/check_profiles.py
~/opt/txra-venv/bin/python -m unittest discover -s tests -p test_arm_rank.py -v
```

The differential check compiles the real C with host GCC and compares complete
synthetic memory against a separate executor parsing the actual assembly
instructions, preserving simultaneous LDM reads, flags, conditional writes,
modular arithmetic and register aliases. It does not use the C algorithm as its
oracle. Each candidate passes **199 fixtures**, reaching all **1,053 instruction
addresses**, including empty/nonempty lists, all four subquads, near/direct
visibility and culling, kind-3 records, kinds 2/4, thresholds -1/0/766/767/768,
signed extremes, word/halfword overflow, nonzero transforms ring wrap, and a second face before the same row sentinel on both near/direct paths.
Visiting an instruction does not establish every predicate outcome or every
possible state. Real ROM data, real table values and device execution are absent.

Each run also checks **20 fixed expected arithmetic/visibility/clamp results**,
**3 record sizes**, and **14 field offsets**. Those are focused consistency
checks, not independent whole-function comparison. The differential comparison
excludes only the test stack interval 03007D00..03007DFF. The existing admission
suite passes **23 tests**; no real-ROM-dependent tests were invoked. Compiler
and source hashes, sizes, relocation/linker evidence and test summaries are in
the adjacent JSON files. All compilation fixtures are temporary and removed.

The README count correction is separately backed by
`registry-reconciliation.json`: 181 unique nonoverlapping existing C entries,
72,524 bytes, 229 mapped functions and 85,132 mapped code bytes, agreeing with
`progress.json`. It records the existing registry, not newly verified matches.

Next, inspect the private-host instruction differences for source/allocation changes
within the existing ARM profile. The prepared historical candidate remains 4,028
versus 4,288 bytes, so nothing is installed. Complete byte equality and all existing
whole-ROM gates are required before acceptance. No 080181C0 trials were repeated.
