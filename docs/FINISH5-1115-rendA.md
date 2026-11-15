# Renderer finish pass 5, 15 November (label: rendA, schedule angle)

Target: **08016DA8** (ARM renderer, 4,288 bytes, owner end 08017E68), projection loop
0801737A..080173F8. No exact match was installed: `src/`, the registry and every installed
replacement are unchanged, so the admission gate and the full rebuild were not run. The best
real near-miss is still finish 4's `g6.c` (49 differing bytes, distance 23). Every compile,
trace and search ran on worker C. Only metadata receipts, insn-uid order lists and sanitized
listings (no encodings, no pool words) were read here.

What this round adds is a complete account of the register allocation in the projection
loop. Real, plain C (`finish5-1115/rendA/c/h7x2.c`) now reproduces the whole function byte
for byte **when sched1 emits the loop block in one particular order**. That order differs from
the order sched1 actually produces in two places, and one of them cannot be produced by this
scheduler from this RTL.

## Result

| Source (`finish5-1115/rendA/c/`) | Real compile | With the forced sched1 order (what-if) |
| --- | --- | --- |
| finish 4 `g6.c` (still best) | 49 bytes, distance 23, 4,288, frame 96 | — |
| `v1.c` g6 + dy in place, dy reused as the depth | 3,798 bytes, 4,352 long | 18 (only r4/r5/r6/lr permuted) |
| `v1b.c` v1 + tx in place | 3,800 bytes | **0** with tx, ty, sin*dz forced non-local |
| `h1.c` v1b + tx shares the header depth[1] variable | 3,802 bytes | **0** with ty, sin*dz forced non-local |
| `h6.c` h1 + sin*dz in a shared `k` | 3,801 bytes | **0** with ty forced non-local |
| **`h7x2.c`** h6 + ty in a shared variable | 3,801 bytes, distance 354, 4,352 long | **0, no other hook** |
| `tx1_a.c` h7x2 with tx shared with a direct-path copy instead | 3,800 bytes | **0, no other hook** |

"Forced sched1 order" means the private compiler's `TXORDER` hook (below) emits the loop
block in the order stored in `orders/<name>.txt`. Every other pass is the official compiler
(`trace.sh` prints "trace asm identical" for all sources without the hook). Receipts:
`receipts/h7x2.json`, `receipts/tx1_a.json` (measure JSON, real compile).

## Diagnostic hooks (private copy of `gcc_arm`, never used for matching)

These apply on top of finish 3's four patches and finish 4's two (`ff_patch.py`, `li_patch.py`).

- `order_patch.py`: `TXORDER=uid,...` makes sched1 emit one block in exactly that order
  (latencies and unit hazards are ignored for that block; an order that breaks a dependence is
  reported as "TXORDER violation"). It also adds `TXDBG=S`, which logs every sched1 pick.
- `nonlocal_patch.py`: `TXNONLOCAL=pseudo,...` leaves those pseudos to global allocation, as
  if they had two deaths or spanned blocks.
- `lforce_patch.py`: `TXLFORCE=pseudo:reg,...` gives the local qty containing the pseudo that
  register, using its unadjusted lifetime.
- Tools: `trace.sh` (official vs private compile plus dumps), `blk.py` (projection block
  before and after sched1, with final registers, the sched1 log and local-alloc qtys),
  `wi.py` (what-if scorer), `ordsearch.py` (hill climb or iterated local search over forced
  orders and non-local sets, optional order constraints `OS_CONSTR=a<b`), `mapord.py`
  (maps an order between candidates by block position), `tryorders.sh`, `ev.sh`.

## Findings

### 1. What the cartridge's allocation requires

The search started from the cartridge's final order (`search-v1.log`). For `v1` it found an
order in which everything matches except a permutation of r4/r5/r6/lr. That permutation
follows from the allocators:

- The rotated x (cos*dx, then tx), ty and the sin*dz product must be **global** allocnos. If
  they are locals, local-alloc hands lr to one of them before global allocation can give it
  to dy. With all three non-local (`v1b` + `TXNONLOCAL`), global allocation gives dy/depth lr
  and then tx r4, ty r5, sin*dz r6: **0 bytes**.
- dy reused as the final depth (two deaths, so global) is right: it gives the depth lr, with no
  tie to `t` or to `w + 0x10000`. Finish 4's analysis of the depth was correct. What blocked it
  was the three locals that took lr first.
- Two sub-results: tx must be computed in place (`tx = dx * cos; tx -= dz * sin;`), and a
  function-scope variable that conflicts with dy must not carry an lr preference into
  `regs_someone_prefers`. Reusing `n` for tx fails on exactly this: n prefers r4 and lr from the
  two clip blocks, so dy drops to r5 (`v1n`, v1b with `n` as tx, not kept: 12 bytes forced).

### 2. Making those three values non-local in plain C (new source fact)

The approach is a function-scope variable whose reference in another block disappears after
flow has already recorded it:

    k = pts[b].sy;                 /* direct path, replacing gCurPacket->y[1] = pts[b].sy; */
    gCurPacket->y[1] = k;
    ...
    k = dz * g_03001B28;           /* projection loop */
    tx -= k;

Flow sees `k` in two blocks and marks it global. Combine then folds the direct-path load and
store back into the original code (that path's output is byte-identical), and `k`'s set count
drops back to one. The loop keeps a global allocno that is still single-set, so sched1 still
treats it as a birthing insn. The same works for ty (`ty = pts[c].sx; gCurPacket->x[2] = ty;`,
and also x[1], y[2], x[3], y[3]; x[0] and y[0] break the direct path). tx can share either the
header value (`tx = pts[b].depth; depth[1] = tx;`, `h1`) or a direct-path copy (`tx1_a`).
With these, `h7x2.c` and `tx1_a.c` are allocation-exact under `TXORDER` alone.

### 3. What sched1 actually does with h7x2 (`orders/h7x2-actual.txt`)

The real sched1 order differs from the required order (`orders/h7x2.txt`) in two places:

- **(a) the race.** sched1 emits `DF8 load, dy minus, DF8*dy`. The cartridge needs
  `dy minus, DF8 load, DF8*dy`.
- **(b)** the gOffset.x load comes before the depth computation and store. It must come after
  the store, just before sx.

Fixing (b) alone (`orders/h7x2-step1.txt`) gives 29 bytes; fixing both gives 0. With the real
order, the allocation collapses into spills: 3,801 bytes, 4,352 long.

**(b) can be moved.** At T-51 the store (priority 62) beats `tx -= k` (17), and the gOffset.x
load (latency 2) is not ready until T-52. If tx's final set is a birthing insn (single-set tx,
`c1.c`), `tx -= k` gets LAUNCH priority and the load lands after the store, as required. But
the separate cos*dx temporary then lets the sin*dz multiply sink below the ty mla (the
finish 4 problem again), and the forced-order allocation of that RTL is 14 bytes.

**(a) cannot be produced by this scheduler from this RTL.** The argument:

- In backward list scheduling, once DF8*dy is picked (T), the dy minus is ready at T+1 (ALU,
  cost 1). The DF8 load is ready only at T+2 (load latency 2; `arm_adjust_cost` lowers only
  load-after-store from the pool or the stack).
- At T+1 every load and multiply is blocked by the core unit. An ALU insn is never blocked, so
  any ALU insn that became ready earlier was already scheduled during the stalls before T.
- So the only way to keep the dy minus from being picked at T+1 is another ALU insn that
  becomes ready exactly at T+1. That insn would have to be an operand of DF8*dy, whose only
  operands are the DF8 load and the dy minus.
- Giving the dy minus a later successor fails too. Its successors are DF8*dy, the ty mla and
  the depth write. Putting the ty mla before DF8*dy forces DF8*tz and the DF8 load even
  earlier.
- The tracing log (`TXDBG=S`, `blk.py --log`) shows exactly this sequence at T-119/T-120.
- An anti-dependence would need the DF8 load to write the register of camy (r1) or of
  -y/dy (lr), but DF8 is r2.

**DF8 first does not work either.** In the natural race order, local-alloc gives the
cartridge's registers only if camy and the y load are marked with their unadjusted
lifetimes (`TXLFORCE=748:1,746:2` on `h7x2-step1` gives 0). In this local-alloc that happens
only for qtys with hard-register suggestions, and nothing in the loop provides one. An
iterated local search over orders that keep the DF8 load before the dy minus
(`search-h7x2-df8-first.log`, `OS_CONSTR`) found nothing better than 15 bytes (camy r3).
Toggling every loop pseudo non-local under the natural order found nothing below 29.

**Barriers.** An empty `do { } while (0)` between the two rotations makes the next insn a
sched1 barrier, and sched1 then keeps dy before the DF8 load. But the loop notes change
loop.c's induction variables for the projection loop (`b1.c`, 2,531 bytes, 4,280 long).
Non-empty wrappers also reweight `REG_N_REFS`. Moving dz before dy, to let a barrier cover
the x/z half, changes loop.c's giv for the z access.

### Ruled out this round (each compiled; numbers are real compiles unless marked)

- The y load in the function-scope `z` (`v2a.c`, 147 bytes) or in `tick` (52). The part-path
  first product in a shared `w` (`t1.c`, 101: n merges w's r2/r3 preferences and leaves r4).
- The direct-path x[0] in a shared `w` (wrecks the header, 3,780).
- ty shared with the special-entry index (header changes, 132 forced).
- Twelve spellings of the depth statement (in place, assignment expressions, reload through
  memory, `/= 2`, `t` reused): all are 49 or spill.
- tx/ty in-place forms that combine merges into mla: `REG_N_DEATHS` stays 1.
- All 32 on/off combinations of the shared-variable tricks on g6 without dy reuse: best 49
  (g6 itself).

## What blocks the rest

The allocation is solved in plain C (`h7x2.c` / `tx1_a.c`): shared function-scope variables
for tx, ty and the sin*dz product, plus dy in place and reused as the depth. Two sched1
decisions are still missing. (a) is that sched1 must emit the dy subtraction before the DF8
load. With DF8*dy consuming both directly, the one-cycle latency race always puts the dy
subtraction directly before DF8*dy, so the original RTL must differ in the y-chain/DF8 region
in a way that leaves the allocation unchanged. (b) is that the gOffset.x load must follow the
depth store, which a birthing tx minus achieves but only at the cost of moving sin*dz.

## Reproduce (on a worker, never the laptop)

```sh
R=docs/finish5-1115/rendA
# private compiler: copy ~/opt/agbcc/gcc_arm with libiberty/ and include/, point objdir at the copy,
# apply finish3 trace_patch_arm, pref_patch, lq_patch, force_patch, finish4 ff_patch, li_patch,
# then $R/order_patch.py, $R/nonlocal_patch.py, $R/lforce_patch.py; make cc1 (paths in trace.sh/wi.py).
bash $R/trace.sh $R/c/h7x2.c /tmp/t                        # "trace asm identical"
TXORDER=$(cat $R/orders/h7x2.txt) python3 $R/wi.py $R/c/h7x2.c   # diff=0 (what-if)
TXORDER=$(cat $R/orders/h7x2-actual.txt) python3 $R/wi.py $R/c/h7x2.c   # the real sched1 order: 3,801
TXLFORCE=748:1,746:2 TXORDER=$(cat $R/orders/h7x2-step1.txt) python3 $R/wi.py $R/c/h7x2.c   # 0
python3 $R/blk.py /tmp/t --log --lq                         # sched1 log and qtys of the loop block
python3 tools/measure_candidate.py $R/c/h7x2.c 08016DA8 08017E68 arm /tmp/r
```

The worker copies (`~/txra-rendA`, `~/txra-rendA-cc`, dumps and logs) were removed after the
receipts were copied.

matches installed: none (192 exact C remain; 08016DA8 not installed)
near-misses improved: none in real bytes (08016DA8 stays 49 differing bytes with g6.c); new allocation-exact source h7x2.c: 0 differing bytes under a forced sched1 order (what-if only), 3,801 as compiled
what blocks the rest: sched1 must emit the dy subtraction before the DF8 load (a one-cycle latency race this scheduler cannot win with DF8*dy consuming both directly) and the gOffset.x load after the depth store; the register allocation itself is reproduced by plain C
