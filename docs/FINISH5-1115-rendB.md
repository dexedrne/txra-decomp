# Renderer finish pass 5, shape lane, 15 November (label: rendB)

Target: **08016DA8** (ARM renderer, 4,288 bytes, owner end 08017E68). This lane tried
different source *shapes* for the projection loop on top of finish 4's `g6.c` (49 differing
bytes). **No exact match was installed.** `src/`, the registry and every installed
replacement are unchanged, so the admission gate and the full rebuild were not run. The best
honest near-miss is still `finish4-1115/renderer/c/g6.c` (49 bytes, distance 23, re-measured
on worker B with the same compiled sha256, `rendB/receipts/g6-remeasure.json`).

Every compile, trace and search ran on worker B. Only metadata (scores, uid orders, hashes) and
sanitized instruction listings (mnemonics, no encodings, no pool words, looked at on screen
as in earlier rounds) came back; nothing ROM-derived is committed.

## Main result: the cartridge's allocation, reproduced exactly in a what-if

With three new diagnostic hooks in a private copy of `agbcc_arm`'s cc1 (applied on top of
finish 3's and finish 4's trace patches; without the environment variables the compiler is
unchanged and its assembly equals the official compiler's), the **whole function compiles
to 0 differing bytes, distance 0, 4,288 bytes, frame 96**
(`rendB/receipts/whatif-nonlocal.txt`, `whatif-lrblocked.txt`). The source is
`rendB/c/s002_dyr_txip.c` (sha256 c7632ed8..., which keeps g6's header comment so that the
hash in `receipts/hashes.txt` matches), i.e. g6.c with the loop body:

```c
dx = gScratch[i].x;  dx -= gCamera.x;
dy = -gScratch[i].y; dy -= gCamera.y;
dz = gScratch[i].z - gCamera.z;
tx = dx * g_03002A18; tx -= dz * g_03001B28;
tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;
t  = dy * g_03000DF8 - tz * g_03005F58;
ty = dy * g_03005F58 + tz * g_03000DF8;
dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);
dy = gOffset.z + (t >> 12);      /* the depth reuses dy */
g_030055F8[i].x = dy; dy >>= 1;
f = g_0804F330[dy + 0x10000];
gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;
gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;
```

plus two things that no plain spelling produced:

1. **A specific sched1 order of the projection block** (forced with `TXS1ORDER`, hook
   `order_patch.py`). In statement terms it is the natural order except that (a) the
   `g_03000DF8` load comes after `dy -= gCamera.y`, (b) `tz >>= 12` sits between that load
   and `DF8*dy`, and (c) the `gOffset.x` load comes after the depth store:
   `... -y, dy -= cam.y, ld DF8, tz >>= 12, DF8*dy, DF8*tz, ld F58, F58*tz, ty mla, tx -= s,
   t, w, store w, ld gOffset.x, sx, w >>= 1, ...`
   (uids in `whatif-nonlocal.txt`; whatif spec `1694>1639 1689>1694 1699>1713 1722>1755`).
   Order alone gives 18 bytes (`whatif-orderonly.txt`): every r0-r3/r12 choice, the
   r1 sharing of cam.y and `DF8*dy`, tz in r12 and DF8 in r2 then match. This confirms finish
   4's reading that the DF8 load must sit between dy and t in sched1.
2. **lr unavailable to local-alloc in the projection block.** The remaining 18 bytes are
   only the long-lived values: the cartridge has tx r4, ty r5, sin*dz r6, dy/w lr; local-alloc
   gives tx lr, ty r4, sin*dz r5 and global-alloc then puts dy/w in r6. Either hook fixes all
   of it: `TXBLOCKREG=18:14` (`blockreg_patch.py`, local-alloc refuses lr in that block) or
   `TXNONLOCAL=727,728,762` (`nonlocal_patch.py`, tx, ty and sin*dz left to global-alloc, as
   if each had two deaths or were referenced in another block). With exactly that set (tx,
   ty, sin*dz) the result is 0. Adding dz, the scratch z load, the cam.x load, the gOffset.y
   load or `F58*tz` keeps 0; adding tz, the tz sum, t, sy, f, `DF8*dy`, `DF8*tz`, `cos*dz`,
   the cos, sin, DF8 or F58 loads, or the gOffset.x load breaks it (11 to 3,797 bytes;
   `TXNONLOCAL` probe on worker B).

So the cartridge's allocation is fully determined: the depth reuses dy (one global pseudo,
two deaths), tx is built in place, the sched1 order above, and the three long-lived
temporaries (tx, ty, sin*dz) are allocated as if lr were not available to them in
local-alloc. The source shape that produces the last two facts is still unknown.

## What was ruled out (all on worker B, official compiler unless marked what-if)

- **Plain spellings never make tx/ty/sin*dz non-local.** `roles.py` (locality of each role
  from the `-dl` register table) on 192 systematic tx/s/ty/sy forms (`gen1.py`) and 1,500
  random spellings with random statement orders (`gen2.py`: temporaries, in-place `*=`/`-=`,
  copies, negations, split shifts): every one leaves all three local. Best official score in
  that family is 70 (as in finish 4).
- **Hypothesis H** (dy local and in lr, depth in a separate global w, y loaded into its own
  variable) cannot work: dy's local-alloc priority (refs 20 over 16 insns) puts it ahead of
  `DF8*tz`, so it always takes r0 (`s030_H.c`; best forced window order 66 with y and w
  non-local).
- **Rotation macro** (one ROT(a, b, c, s, x, y) for the yaw and the pitch rotation, which
  fits both: x = a*c - b*s, y = a*s + b*c): 144 variants (`gen3.py`; six bodies, plain /
  `{}` / `do {} while (0)`, two prologues, four tails). Plain and braced macros compile like
  the expanded statements (best 117); `do {} while (0)` is much worse (2,305+, 4,264 long).
- **Function-scope declarations and dead initializers** of tx/ty/s: no effect (flow drops the
  dead stores before it records references).
- **Natural multi-block reuse.** tx kept in the cross-product variable n (`s020_ntx.c`) works
  as far as it goes: n stays r4 and both clip blocks are unchanged (what-if with forced order
  and ty, sin*dz non-local: 12 bytes, only dy/w and ty swap lr and r5). ty kept in the
  special block's index variable (r5 there, `s060_n_j.c`) changes global allocation of the
  face pointer and &pts[b] (132 in the same what-if). sin*dz has no candidate at all: every
  other r6 value in the cartridge is a pointer (&pts[b], &gCurPacket, &g_03000DE0).
- **Hidden block split.** A dead two-statement conditional (`s053_dead2.c`) survives to flow,
  splits the loop body and makes tx and ty global, but jump2 leaves the dead `cmp` in the
  output. No single split point in the needed order has the right crossing set either
  (`DF8*dy` would cross).
- **Aliasing the depth store with gOffset** (gOffset as `g_030055F8 + 0x988`, `s070`) would
  explain the late gOffset.x load, but it stops loop.c hoisting gOffset.z (3,682, 4,356 long).
- **Compiler flags**: `-mcpu=arm7tdmi`/`-mtune=arm7tdmi` are identical to the default; arm7,
  arm7m, arm8, arm9tdmi and strongarm models are thousands of bytes off. The profile is right.
- **The order is not in the finish-4 spelling space**: `nlanneal.py` annealed 30 minutes over
  perm4's options and statement priorities with tx/ty/sin*dz treated as non-local (so only
  the order mattered): 7,074 candidates, best 81 (`receipts/nlanneal-log.txt`); the same
  what-if scoring of the 1,692 generated spellings gave at best 85.

## Tools (`finish5-1115/rendB/`, worker only)

- Compiler hooks, applied in this order after the finish-3 (`trace_patch_arm`, `pref_patch`,
  `lq_patch`, `force_patch`) and finish-4 (`ff_patch`, `li_patch`) patches to a private copy
  of `~/opt/agbcc/gcc_arm` (with `libiberty/` and `include/` beside it, `objdir` set to the
  copy, `make cc1`): `order_patch.py` (`TXS1ORDER`), `nonlocal_patch.py` (`TXNONLOCAL`),
  `blockreg_patch.py` (`TXBLOCKREG`). What-if only; never used for matching.
- `whatif.py` (forced order + score + listing), `wenum.py` (all dependence-respecting orders
  of a window, bounded displacement), `oanneal.py` (anneal over forced orders),
  `nlscore.py` / `nlanneal.py` (score / search with the three roles non-local),
  `roles.py` (locality of tx, sin*dz, ty, dy/w), `qa.py` (local qtys and global choices of the
  block from a trace), `nat.py` (natural sched1 order with dependences), `blk.py`, `trace.sh`,
  `batch.py`, `sbsr.py`, `mk.py`, `gen1.py`..`gen3.py`, `dies.sh`.

## Reproduce (on a worker)

```sh
W=docs/finish5-1115/rendB    # private cc1 built at ~/rendB-cc/gcc_arm/cc1 as described above
S="1694>1639 1689>1694 1699>1713 1722>1755"
TXNONLOCAL=727,728,762 python3 $W/whatif.py $W/c/s002_dyr_txip.c "$S"   # whatif diff=0
TXBLOCKREG=18:14       python3 $W/whatif.py $W/c/s002_dyr_txip.c "$S"   # whatif diff=0
python3 $W/whatif.py $W/c/s002_dyr_txip.c "$S"                          # whatif diff=18
python3 tools/measure_candidate.py docs/finish4-1115/renderer/c/g6.c 08016DA8 08017E68 arm /tmp/r  # 49
```

The worker copies (`~/txra-rendB`, `~/rendB-cc`) were removed afterwards.

matches installed: none (192 exact C remain; 08016DA8 not installed)
near-misses improved: none (08016DA8: 49 -> 49 differing bytes, g6.c stays best); new what-if: 0 bytes with a forced sched1 order plus lr refused to local-alloc in the projection block (s002_dyr_txip.c)
what blocks the rest: no natural source yet gives the cartridge's sched1 order of the projection block (DF8 load after dy, tz shift before DF8*dy, gOffset.x load after the depth store) or keeps tx, ty and sin*dz out of lr in local-alloc (they must behave as non-local; tx can live in n, sin*dz has no other home)
