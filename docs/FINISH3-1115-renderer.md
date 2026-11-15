# Renderer finish pass 3, 15 November (label: renderer)

Target: **08016DA8** (ARM renderer, 4,288 bytes, owner end 08017E68). No exact match was
installed. The registry, `src/` and every installed replacement are unchanged, so the
admission gate and the full rebuild were not run for an install. Every compile,
measurement, trace, search and behaviour check ran on worker C. Nothing ROM-derived left the
worker except the sanitized diff listing that earlier rounds also kept (encodings and pool
words removed) and metadata receipts.

## Result

Measured with `tools/measure_candidate.py` (`arm` profile, strict end 08017E68). Shape and
register rows come from this round's `sbs2.py --score` (its normalisation differs slightly
from the 11/14 `sbs.py`, so the 11/15 rows are re-measured here).

| Candidate | Differing bytes | Instruction distance | Emitted / target | Frame | Shape / register rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| 11/15 best (`finish2-1115-renderer/func_08016DA8.c`) | 880 | 367 | 4,288 / 4,288 | 96 | 113 / 287 |
| 11/15 hoist-order line (`func_08016DA8_order.c`) | 3,294 | 558 | 4,292 | 96 | 68 / 499 |
| `c/o1.c` = order line + Packet `next` type (fact 1) | 3,312 | 552 | 4,292 | 96 | 65 / 494 |
| `c/z1.c` = o1 + in-place `tz` shift (fact 2) | 3,319 | 539 | 4,292 | 96 | 64 / 481 |
| `c/v2.c` = 11/15 clean `v-ref.c` + facts 1 and 2 | 3,340 | 614 | 4,292 | 96 | 60 / 562 |
| **search B (`c/func_08016DA8_bytes.c`)** | **863** | 381 | **4,288 / 4,288** | **96** | 133 / 298 |
| **search A (`c/func_08016DA8_dist.c`)** | 1,091 | **322** | **4,288 / 4,288** | **96** | 110 / 242 |

Search B has the fewest differing bytes so far (880 -> 863); search A has the fewest
instruction edits so far (367 -> 322). Both are permuter output (see *Search*): their
`do { } while (0)` wrappers, reordered stores and swapped operands are behaviour-preserving
plain C, not a claim about how the original was written. Both, and z1, pass the 11/14
synthetic differential checker (`check32.py`: 199 fixtures, 0 failures, all 1,053
instruction addresses reached, no ROM used); receipts in `finish3-1115/renderer/receipts/`.

## Two new source facts (natural C, each confirmed by compiling and by RTL dumps)

1. **The packet's `next` field has the same pointer type as the globals.** The 11/15
   sources declared `typedef struct Packet { ...; struct Packet *next; } Packet;` and the
   globals as `Packet *`. In this GCC, `struct Packet *` and `Packet *` are different
   pointer type nodes with different alias sets (4 and 2 in the `-dl` dump), so sched1 was
   free to sink `p->next = ...` below the `gCurPacket++` store, and cross-jumping then
   merged the two arms' next stores. Declaring `typedef struct Packet Packet;` first and
   `Packet *next;` in the body gives both one alias set: the store keeps its place in both
   arms and the bucket insertion (08017A48..08017A88, both copies) is exact in shape and
   registers (o1).
2. **The projection loop shifts `tz` in place after storing it:**
   `g_030055F8[i].x = tz; tz >>= 1; f = g_0804F330[tz + 0x10000];`. The old backward
   scheduler places a store with no dependants at the end of the block; the write after
   read on `tz` makes the store a predecessor of the shift and the table load, so it is
   issued right after `tz` is computed, as in the cartridge, and the shift is the
   cartridge's in-place `mov lr, lr, asr #1`. 080173D8..08017414 now match in shape (z1).
   `tz = (tz >> 1) + 0x10000;` and `tz >>= 1; tz += 0x10000;` are worse in that region
   (29 and 30 shape rows against 26).

## Tracing compiler for the ARM profile

The stream lane's `trace_patch.py` targets `old_agbcc`; the renderer uses `agbcc_arm`
(gcc 2.9-arm-000512, whose reload, global and local allocators differ in detail). This
round adds `finish3-1115/renderer/trace_patch_arm.py` (reload picks RA/RI, global
`find_reg` results GF), `pref_patch.py` (preference, conflict and used-so-far masks on
each GF line), `lq_patch.py` (local-alloc qty order, priority, lifetime, register) and
`force_patch.py` (`TXFORCE=pseudo:reg,...`, a what-if hook that makes `find_reg` hand a
pseudo a given register). Apply them in that order to a private copy of
`~/opt/agbcc/gcc_arm` (with `libiberty/` and `include/` beside it, `objdir` pointed at the
copy) and run `make cc1`. `trace.sh` compiles with both compilers and requires identical
assembly: identical for o1, z1, both search results and the two 11/15 candidates. The
what-if hook changes code and is never used for matching; it only shows what follows from
one allocation decision.

## Why it is not exact yet

### 1. The face header: a global-allocation order the natural source cannot produce

At 08016E44 the cartridge has depth[1] in r4, `&pts[c]` in lr and `&pts[d]` in r12; every
source so far has r12 / r4 / lr. All three are global allocnos with no preferences (the
preference masks are empty), and r12/lr are in `regs_used_so_far` from the start, so
`find_reg` simply takes the first free register in `REG_ALLOC_ORDER` (3, 2, 1, 0, 12, 14,
4, ...). The cartridge therefore allocated `&pts[d]`, then `&pts[c]`, then depth[1].
None of three forced alternative assignments triggers a reload kick-out and
reallocation, so the cartridge's order is the global order itself.

The natural source gives depth[1] refs 9 / live 15 (priority 1.800), `&pts[d]` 12/26
(1.385), `&pts[c]` 12/29 (1.241) and `&pts[a]`/`&pts[b]` 12/31 (1.161), with depth[2] at
2.077. The cartridge needs depth[2] > `&pts[d]` > `&pts[c]` > depth[1] > `&pts[a]`. With
the natural live lengths no integer ref count for the two pointers fits that window
(16 refs gives 2.21 and 2.46, 15 gives 1.55 and 1.73), so the original must also change the
live lengths. `do { } while (0)` around the direct path's vertex copies does change them
(loop notes are sched1 barriers), but none of seven variants lands in the window (w1-w3 on
c/d: 2,273-2,275 bytes; per-vertex dv1/dv2: 3,390-3,489 bytes, 4,340-4,348 long; all four dw1/dw2:
2,272-2,277 bytes, header still wrong).

### 2. What that one decision changes (what-if, diagnostic only)

With depth[1]/`&pts[c]`/`&pts[d]` forced to r4/lr/r12 on o1, `lr` leaves the spill set
(7 registers -> 6). In the natural source, insn 121 (`d*7`, two reloads of the spilled `d`)
finds lr and r8 free because `&pts[c]` sits in r4, so both become spill registers; with
`&pts[c]` in lr it takes r12 and r8, exactly the cartridge's six (r0-r3, r8, r12). The
round-robin reload rotation then follows the cartridge through most of the part blocks:
shape rows 65 -> 45, register rows 494 -> 300, distance 552 -> 354 (length 4,284: the
cartridge's `ldr r12, [fp, #-84]` reload at 080172C0 is then missing). Forcing two more
globals the cartridge places differently (the clipping block's packet pointer r5, the
long-lived `&gCurPacket` r6) gives 269 register rows and distance 324. z1 with the forced
header: distance 350, 47 / 299 rows.

### 3. Part blocks: a local-allocation tie

In each part's x section the qty of `gScratch[0].x = pts[a].x` (refs 8, life 2) and the
qty of the midpoint chain `(pts[a].x + pts[b].x) >> 1` (refs 24, life 8) tie exactly
(priority 12.0 each at loop depth 4), so qty order decides and the load takes r3; the
cartridge gives the chain r3 and the load r2. At depth 6 (the order line's y/z wrappers)
the chain wins 22.5 to 18 and matches the cartridge; depth 5 ties again, depth 3 would
win. So the cartridge's x sections do not behave like plain statements at depth 4 with
these lifetimes. Wrapping every part statement (pa1/pa2, pg1/pg2 on v2) is worse
(3,355-3,415 bytes, two of them 4,268 long).

### 4. Smaller open items

- **sb/sl.** The clean source (v2) swaps the points base and the scratch pointer: the
  scratch pointer's live length is doubled by its `REG_EQUIV` note, so it needs extra
  references to get ahead of the points base; the order line's y/z wrappers provide them.
- **Clipping block.** The cartridge's back-face cross product result is not tied to the
  first product and takes r4, which pushes the packet pointer to r5 and `&gCurPacket` to
  r6; ours ties it (r0). Not explained.
- **Projection loop.** After fact 2 the remaining difference is sched1 order before the
  store (the cartridge computes `X*dy` before `tz >> 12` and `X*tz`). All 1,052
  dependency-respecting statement orders of the o1 loop and about 270 of 1,492 for z1 were
  scored on that region: the source order is best (27 and 26 shape rows). The forced
  what-if still leaves 24 of o1's 27 shape rows there, so it is mostly not an allocation
  effect.
- **Near-path and direct-path finish blocks** (z sum, tex/mode stores) and the special
  entry's pool loads differ where reload rematerialises `&gCurPacket` and the zero
  constant; these rows remain in the what-if and are not explained.

### Ruled out this round

The experiment sources named in this note (w1-w3 on o1, dv/dw on z1, pa/pg on v2, the
macro and spelling variants on o1) were not kept; each is the named base with the edit
described.

- Constant-address macros for the projection globals (they would make the store and
  table load alias): table only 3,608 bytes / 4,328 long; `g_030055F8` only 3,586 /
  4,316, frame 92; both 3,694 / 4,348; scratch 4,137 / 4,812. They are symbols.
- One shared base for `g_030055F8` and the camera, offset and scratch globals: 3,367 to
  3,761 bytes, 4,300 to 4,428 long.
- 19 spellings of the store and table load (pointer forms, casts, operand order): none
  beats o1 in the projection region; `*(g_0804F330 + (tz >> 1) + 0x10000)` reaches
  4,288 bytes only by folding the +0x10000 into the base constant (one `add` fewer, a
  different pool word), so it is rejected.

## Search

`perm.py` and `clean.py` are the 11/15 tools, unchanged (score `3 * distance + bytes / 3`,
annealed). Three runs on worker C, 45 minutes each, nice 5:

| Run | Start | Workers | Evaluated | Best (bytes / distance, length 4,288) |
| --- | --- | ---: | ---: | --- |
| A | o1 | 5 | 8,520 | 1,091 / 322 |
| B | b1 (11/15 best + fact 1, 1,581 / 399) | 5 | 8,500 | 863 / 381 |
| C | z1 | 3 | 5,436 | 1,513 / 398 |

`clean.py` then reverted every edit that did not change the compiled bytes: A keeps 36
hunks against o1, B keeps 31 against b1. Fact 1 broke the 11/15 best's compensating
errors (880 -> 1,581 bytes and 4 bytes long), which search B repaired with new ones; the
first difference of both search results is still in the face header.

## Receipts (`docs/finish3-1115/renderer/`)

- `c/func_08016DA8_bytes.c`, `c/func_08016DA8_dist.c` (search results), `c/o1.c`,
  `c/z1.c`, `c/v2.c`, `c/b1.c`;
- `receipts/`: measure JSON for all six, `check-*.json` (check32 for both search results
  and z1), `bytes.diff.txt.gz` (sanitized listing for search B), `search-logs.txt` (score
  logs only);
- tools: `trace_patch_arm.py`, `pref_patch.py`, `lq_patch.py`, `force_patch.py`,
  `trace.sh`, `amap.py` (maps each allocated pseudo to the cartridge register by aligned
  operand votes and flags mismatches in global-allocation order), `whatif.py` (compile
  with the private cc1, optional `TXFORCE`), `hstat.py` (header depth/pointer
  refs, live lengths, priorities, registers), `sbs2.py` (full side-by-side and
  `--score`), `rscore.py` (parallel region scorer), `pperm.py` (projection statement
  orders), `hperm.py` (header statement orders), `perm.py`, `clean.py`.

## Reproduce (on a worker, never the laptop)

```sh
W=docs/finish3-1115/renderer
python3 tools/measure_candidate.py $W/c/func_08016DA8_bytes.c 08016DA8 08017E68 arm /tmp/r
python3 $W/sbs2.py $W/c/z1.c --score
python3 docs/near-misses/finish-1114-renderer/check32.py $W/c/func_08016DA8_dist.c
# private tracing compiler (see the section above), then:
bash $W/trace.sh $W/c/z1.c build/tr            # must print "trace asm identical"
python3 $W/amap.py $W/c/z1.c --trace           # global order, cartridge registers
TXFORCE=70:4,75:14,81:12 python3 $W/whatif.py $W/c/o1.c   # header what-if (o1 pseudo numbers)
```

The worker copies (`~/txra-renderer`, `~/txra-renderer-cc`) were deleted after the
receipts were copied.

matches installed: none (191 exact replacements remain; 08016DA8 not installed)
near-misses improved: 08016DA8: 880 -> 863 differing bytes (search B, distance 381); instruction distance 367 -> 322 (search A, 1,091 bytes); both 4,288 bytes, frame 96
what blocks the rest: the face header needs &pts[d] and &pts[c] allocated before depth[1], which no natural spelling found gives (the what-if shows this one decision fixes the spill set and most reload rows), the part blocks' x sections need the midpoint chain to beat a priority tie, and the projection loop's pre-store schedule is still open
