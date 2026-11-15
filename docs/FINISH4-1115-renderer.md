# Renderer finish pass 4, 15 November (label: renderer)

Target: **08016DA8** (ARM renderer, 4,288 bytes, owner end 08017E68). No exact match was
installed. The registry, `src/` and every installed replacement are unchanged, so the
admission gate and the full rebuild were not run for an install. Every compile,
measurement, trace, search and behaviour check ran on worker C. Nothing ROM-derived left the
worker: only metadata receipts (measure and check JSON) and sanitized instruction listings
(mnemonics with encodings and pool words removed) were read here.

## Result

| Step (source in `finish4-1115/renderer/c/`) | Differing bytes | Instruction distance | Emitted / target | Frame |
| --- | ---: | ---: | ---: | ---: |
| finish 3 best (search B) | 863 | 381 | 4,288 / 4,288 | 96 |
| finish 3 clean source `v2.c` | 3,340 | 614 | 4,292 | 96 |
| `g1.c` = v2 + ring loop as label/goto | 292 | 157 | 4,288 | 96 |
| `g2.c` + one cross-product variable for both paths | 226 | 96 | 4,288 | 96 |
| `g3.c` + projection depth temporary before `ty`, screen x in `dx` | 171 | 79 | 4,288 | 96 |
| `g4.c` + variable-first multiplies, `dx` loaded then adjusted | 139 | 63 | 4,288 | 96 |
| `g5.c` + depth sum as one expression, then `z += 32` | 68 | 31 | 4,288 | 96 |
| **`g6.c`** + natural sum and `z < 0` clamp first in both paths | **49** | **23** | **4,288 / 4,288** | **96** |

`g6.c` is the best near-miss: 49 differing bytes (from 863), instruction distance 23 (from
322), exact length and frame. Its first difference is 0801737A; the header, all four part
blocks, both clip blocks, both finish blocks, the bucket code and the direct path match
byte for byte. All 49 bytes are register choices in the middle of the projection loop
(0801737A..080173F8, 22 rows; two of them are a reload whose pool load moves). g6 passes
the 11/14 synthetic differential checker (199 fixtures, 0 failures, all 1,053 instruction
addresses reached, no ROM used): `receipts/check-g6.json`; measure receipt
`receipts/g6.json`.

g6 is plain structured C with no wrappers: the only constructs a reader might question are
the label/goto ring loop and the two-statement temporaries described below.

## Source facts (each confirmed by compiling, by RTL dumps and by allocator traces)

### 1. The ring loop is a label and a goto, not do/while (863 -> 292)

`flow.c` weights every `REG_N_REFS` by the loop depth (notes counted from 1), and both
allocators rank by `floor_log2(refs) * refs / length`. With the ring loop written
`loop: ... ring = (ring + 1) & 31; if (ring != end) goto loop;` the face header sits at
depth 2 instead of 3, which changes the floor_log2 factor of the depth values but not of the
point pointers:

| header allocno | refs / length at depth 3 | priority | at depth 2 | priority |
| --- | ---: | ---: | ---: | ---: |
| depth[1] | 9 / 15 | 1.800 | 6 / 15 | 0.800 |
| &pts[d] | 12 / 26 | 1.385 | 8 / 26 | 0.923 |
| &pts[c] | 12 / 29 | 1.241 | 8 / 29 | 0.828 |
| &pts[a], &pts[b] | 12 / 31 | 1.161 | 8 / 31 | 0.774 |

The new order (&pts[d] r12, &pts[c] lr, depth[1] r4, &pts[a] r5, &pts[b] r6) is the
cartridge's, which finish 3 had found no ref count for the two pointers could reach. The same one-level
drop settles the part blocks' local-allocation tie (finish 3 item 3): at depth 3 the
midpoint chain wins (refs 18, life 8: 9.0) over the scratch load (refs 6, life 2: 6.0).
Every part block and the spill set then match, and the do/while(0) wrappers the earlier
rounds needed are gone.

### 2. One cross-product variable for both paths (292 -> 226)

`n = (x3 - x0) * (y1 - y0) - (x1 - x0) * (y3 - y0);` in a function-scope `s32 n`, used by
the part path (`if (n > 0) continue;`) and the direct path (`if (n <= 0) {`). Referenced in
two blocks, `n` is a global allocno (r4) instead of a local qty tied to the first product,
which also moves the packet pointer to r5 and `&gCurPacket` to r6. Both clip blocks match.

### 3. Projection loop (226 -> 139)

- **The final depth has its own variable** (`w`), so the rotated z (`tz`) is a one-death
  local that ties to its mla temporary in place (r12-style `mla; mov rX, rX, asr #12`).
- **The depth product difference is a temporary computed before `ty`:**
  `t = dy * g_03000DF8 - tz * g_03005F58;` then `ty = ...`, and later
  `w = gOffset.z + (t >> 12);`. sched1 (the old backward list scheduler, `sched.c`) picks
  among multiplies that are all at the launch priority by LUID; the cartridge has DF8*dy
  ahead of DF8*tz, which needs that product earlier in insn order. Moving the whole depth
  statement instead changes loop-invariant motion (gOffset.y instead of gOffset.z is
  hoisted; 4,348 bytes).
- **The screen x reuses `dx`** (`dx = gOffset.x + (tx >> 12);`): a two-death pseudo is not a
  local qty, so it is not tied to the dying gOffset.x load (the cartridge has sx in r12,
  the load in r3).
- **Multiplies are written variable-first** (`dx * g_03002A18`): this GCC then emits
  `(mult global var)`, the cartridge's operand order in every `mul`/`mla`.
- **`dx` is loaded, then adjusted**: `dx = gScratch[i].x; dx -= gCamera.x;` puts the load in
  dx's own register, as in the cartridge.

### 4. Finish blocks (139 -> 49)

Both paths, written the same way:

    z = (depth[0] + depth[1] + depth[2] + depth[3]) >> 7;
    z += 32;
    if (z < 0) z = 0;
    gCurPacket->tex = face->tex;
    gCurPacket->mode = 0;
    if (z > 255) z = 255;

GCC regroups the natural sum as (d0 + d3) + (d2 + d1), the cartridge's add tree (all 120
groupings/orders were compiled; the earlier two-statement sum gives the mirrored tree).
Shifting into `z` and adding 32 in place gives the shared register for `z >> 7` and
`z + 32`. Clamping below zero before the two stores puts the clamp's insns ahead of the
stores in insn order, so the backward scheduler places the stores first and the
gCurPacket load becomes ready before the shift; reload then rotates through r3/r8/r12 as in
the cartridge (tex reloaded into r8, zero into r12). The part path, the direct path and the
bucket insertion then match.

## What is left (22 rows, 49 bytes)

The cartridge keeps dy and the final depth in lr, tz in r12, cam.y and the DF8*dy
temporary both in r1, DF8 in r2 and DF8*tz in r0. g6 has dy in r0, tz in lr, cam.y in r12
and t/w/w+0x10000 tied in r1. The allocator traces say:

- **The final depth is not a local qty in the cartridge.** It is tied neither to `t` (r1)
  nor to `w + 0x10000` (r3); `combine_regs` ties a single-block, single-death pseudo to any
  dying input, so the original's depth variable has two deaths or spans blocks. The only
  user-visible value it can share lr with is dy, i.e. `dy = gOffset.z + (t >> 12)`.
- **Reusing dy changes sched1.** The new WAR dependence (the ty mla reads dy, the depth
  writes it) carries the full 16-cycle multiply latency, so the mla becomes ready one cycle
  after `sin*dz` is picked and `sin*dz` moves after it (dz then lives long, a local takes
  lr, dy is pushed to r7 and the whole function spills: 4,352-4,428 bytes). With tx also
  computed in place (`tx = dx * g_03002A18; tx -= dz * g_03001B28;`) the race goes the
  cartridge's way and the loop matches through 0801738B with tz in r12 (85 bytes; 70 with
  ty's terms swapped), but the y-chain then allocates DF8 to lr and dy to r0/r2.
- **cam.y and t share r1 only with an insn between them.** Local-alloc first tries each
  qty with its lifetime widened by one insn on each side (`fake_birth`/`fake_death`), so a
  value dying in one insn conflicts with one born in the next. The cartridge's sharing of
  r1 (cam.y, then DF8*dy) and r2 (y load, then DF8) means sched1 put the DF8 load between
  `dy` and `t` (sched2 later moved it up). Our sched1 picks `dy` first because the load,
  launched when `t` is scheduled, is still waiting out its 2-cycle latency.

## Search

- 120 groupings x 2 shift forms x 2 direct forms of the depth sum; 15 x 122 part/direct
  pairs; 96 clamp/store placements (these produced g5 and g6).
- Projection statement orders (`porder.py`): 4,840 on the g2 structure (about 450 scored
  before the structure changed), 5,000 sampled on the separate-depth base, 3,600 sampled on
  four dy-reuse bases; 81 do/while(0) placements; 1,152 structured spellings (`pspace.py`);
  128 tail spellings and 160 explicit-local placements on the dy-reuse family.
- Annealing over spelling options and statement priority on worker C: run D (`perm4.py`, from
  g6, 40 minutes) evaluated 8,763 candidates, best g6; run E (`perm5.py`, dy-reuse family
  from the 70-byte variant, longest-exact-prefix objective, 40 minutes) evaluated 10,848,
  no prefix past 0801739C. Three shorter runs (perm2/perm3, 10-25 minutes) found nothing
  better either. None beat g6.

## Tools (`finish4-1115/renderer/`)

- `porder.py`: dependency-respecting statement orders of the projection loop.
- `pspace.py`: structured projection-loop spellings (in-place forms, variable reuse,
  temporary placement, output order).
- `perm2.py`..`perm5.py`: annealing over those options plus a statement priority list
  (always a topological order, so always behaviour-preserving plain C); perm3 adds explicit
  locals for the four rotation globals, perm4 in-place forms at the block tail, perm5 a
  longest-exact-prefix objective (`PFX=1`).
- `zforms.py`, `zclamp.py`: the depth-sum and clamp/store sweeps behind g5 and g6.
- `ffq.py`, `lq.py`, `s1log.py`, `s1order.py`, `seq.py`: diagnostics (find_free_reg masks with
  qty members, local qty table, sched1 log and order for the projection block, instruction
  sequences of our own output).
- Private tracing compiler patches, applied after finish 3's four: `ff_patch.py`
  (find_free_reg used mask, TXDBG=F) and `li_patch.py` (local-alloc insn numbers, TXDBG=I).
  Assembly stays identical to the official compiler (`trace.sh` prints "trace asm
  identical" for g6).

## Reproduce (on a worker, never the laptop)

```sh
W=docs/finish4-1115/renderer
python3 tools/measure_candidate.py $W/c/g6.c 08016DA8 08017E68 arm /tmp/r
python3 docs/finish3-1115/renderer/sbs2.py $W/c/g6.c --score
python3 docs/near-misses/finish-1114-renderer/check32.py $W/c/g6.c
```

matches installed: none (192 exact C remain; 08016DA8 not installed)
near-misses improved: 08016DA8: 863 -> 49 differing bytes (instruction distance 322 -> 23), 4,288 bytes, frame 96 (g6.c)
what blocks the rest: 22 register rows in the projection loop: the original's final depth is a non-local pseudo sharing lr with dy, but reusing dy adds a full-latency anti-dependence that changes sched1, and the DF8 load must sit between dy and t in sched1 for local-alloc's widened lifetimes to give cam.y and t the same register
