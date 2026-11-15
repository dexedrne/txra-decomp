# Renderer finish pass 6, whole-loop shape lane, 15 November (label: shape)

Target: **08016DA8** (ARM renderer, 4,288 bytes, owner end 08017E68), projection loop
0801737A..080173F8. **No exact match was installed.** `src/`, the registry and every installed
replacement are unchanged, so the admission gate and the full rebuild were not run. The best
honest near-miss is still finish 4's `g6.c`: 49 differing bytes, distance 23, 4,288 bytes,
frame 96, compiled sha256 734c5e9d... (re-measured on worker D with the official ARM compiler,
`finish6-1115/shape/receipts/g6-remeasure.json`).

Every compile, trace and search ran on worker D through `txra-remote.sh`. Only metadata came back
(scores, uid orders, dependence links, hashes). Instruction listings were looked at on screen
only, without encodings or pool words, and none are committed.

## Result

| Source / family | Real compile (official compiler) | Notes |
| --- | --- | --- |
| `g6.c` (finish 4) | **49**, distance 23 | still best |
| `h7x2.c` (finish 5, `shape/c/base.c`) | 3,801, 4,352 long | allocation exact only with a forced sched1 order |
| Loop shapes on h7x2: `<= 3`, `do/while` (both forms), `while`, inline `static inline` helper | 3,800 to 3,801 | identical or near-identical RTL |
| Pointer iteration over gScratch (4 forms); inline helper taking a `Vec3 *`; depth before screen x/y (2 forms) | 3,157 to 3,579; 3,019; 3,663 | change loop.c's givs or which offset field is hoisted |
| Empty loop as a sched1 barrier, 3 constructs x 20 positions | 2,322 or worse | loop notes change loop.c everywhere in the loop |
| `shape/c/d8w.c`: h7x2 + DF8 load in a direct-path-shared variable | **72**, distance 32, 4,288 | natural DF8-first order gives the cartridge's y-region registers |
| Same with F58 instead of DF8 | 72 | same regime |
| Birthing final tx (`u = tx - k`, or a shared `q`) | 3,789 to 3,795 | sched1 emits (b) by itself, but sin*dz sinks below the ty mla |
| Integer-cast addresses (`((Vec3 *)0x...)`) for depth/offset/camera/table, with and without source-hoisted z | 2,387 or worse | |
| Random "generic temporaries" homes, 2,000 | best 66 | `homes.py` |
| Random statement orders x options, 3,000 | best 72 | `perm.py`; order barely matters, the options decide |
| Exhaustive structural options, 5,040 | best 49 (g6 itself), next 65 | `structopts.py`; reproduces g6 and h7x2 byte for byte |

## 1. Why the projection loop cannot get the cartridge order from h7x2's RTL (proof)

The scheduler model of this compiler, read from `gcc_arm` and confirmed with a new dependence
trace (`slink_patch.py`, `TXDBG=K`, receipts `sched1-links-h7x2.txt`):

- `ldsched` is `no` for the default CPU: loads and stores occupy the `core` unit with ready and
  issue delay 2, multiplies with 16. ALU insns use no unit, so they are never blocked.
- `arm_adjust_cost` only lowers load-after-store from the pool or stack. It does **not** zero
  anti or output dependences, so those cost the producer's full latency (16 after a multiply).
- When an insn becomes ready and sets a single-set pseudo that is live, `adjust_priority` gives
  it LAUNCH priority (0x7f000001). Ties then go to the class against the last scheduled insn and
  finally to the higher LUID.

Backward list scheduling of the h7x2 block (1641 = `dy -= cam.y`, 1697 = DF8 load,
1698 = DF8*dy): when 1698 is picked at time T, 1641 (ALU, cost 1) is ready at T+1 and 1697
(load, cost 2) at T+2. At T+1 every load, store and multiply is blocked by the core unit
(1698 is a multiply). For 1641 not to be picked at T+1, an ALU insn X must be ready at T+1.
An ALU insn becomes ready one cycle after its last consumer, so X needs a dependence link to
1698. 1698's links are its two operands (1697, 1641) and anti/output links on its destination.
In the cartridge's registers that destination is r1, whose previous value (camy) is read only
by 1641 itself, and no other register is shared. An X that was ready earlier would have been
picked during the 15 cycles before T (the multiply gap) unless higher-ranked insns filled them,
and those would sit between 1698 and the next multiply. In the orders known to keep the
allocation (the required order and its single-move neighbours, section 2) the only insn that
may sit next to 1698 is 1692 (tz shift), so the gap cannot be filled. So **no LUID order, priority or birthing status can make
sched1 emit 1641 before 1697 with this insn set**, and pseudo sharing cannot add the missing
link without contradicting the cartridge's hard registers.

The only mechanisms left are an extra insn that disappears later or a block boundary:

- A copy of the y chain (`d = dy;` feeding both multiplies) is exactly the missing X
  (1641 -> X -> 1698, then DF8 wins T+2 on LAUNCH). It never survives: CSE replaces `d` by `dy`
  unless `d` is a multi-block variable, and then combine folds the minus into the copy
  (`cw_*` variants: 1641 becomes `w = -y - camy`; 75 bytes). Combine is only stopped by
  `use_crosses_set_p` or a volatile insn in between, which needs a register reuse that the
  cartridge's allocation does not have.
- Loop notes make the next insn a full barrier, but every empty-loop construct at every one of
  the 20 statement positions changes loop.c's induction variables or hoisting (2,322+).

(b) (gOffset.x load after the depth store) has the same character: after `dy >>= 1` at time a,
sx is picked at a+1 and the store is ready at a+2 (anti link, store cost 2) while the
gOffset.x load is ready only at a+3. Only a LAUNCH insn at a+2 can hold the store back, and
the only candidate is `tx -= k`, which is LAUNCH only if the final tx is a single-set pseudo.
That works (`h_u1`: sched1 then emits store, gOffset.x, tx - k, sx by itself), but the final tx
then cannot share r4 with cos*dx (separate pseudos: a local `u` gets r3 from local allocation,
which cannot tie a local to the global tx; a shared global `q` gets r0 from global
allocation), and sin*dz sinks below the ty mla because its multiply slot opens 16 cycles after
the store while nothing else is ready yet.

## 2. Freedom around the required order (`freedom.py`, receipt `freedom-h7x2.txt`)

All legal single-insn moves of rendA's `orders/h7x2.txt` (radius 12, 318 legal): 47 keep 0
bytes. 1692/1698 may swap (tz shift before DF8*dy, rendB's order), 1677 (`tx -= k`) may move
up to four places later (to just before sx), several tail insns move freely. No move of 1641,
1697, 1725 or the depth store keeps 0, so (a) and (b) are hard constraints of that allocation.

## 3. A different regime: DF8 (or F58) as a global allocno

Putting the DF8 load into a function-scope variable that the direct path also uses for one
point-to-packet copy (rendA's trick applied to a load, `d8w.c`) removes the DF8 load from
local allocation and from LAUNCH priority. With the **natural** DF8-first order, the y region
then gets exactly the cartridge's registers (y r2, camy r1, -y and dy lr, DF8 r2), which
rendA could only get with `TXLFORCE`. What remains in the real compile (72 bytes): sum/tz in
r0 instead of r12, DF8*dy in r12 instead of r1, and (b). A forced-order climb from the
(b)-fixed order reaches 17 bytes (`ordsearch-cdf8.txt`; camy r0/DF8 r3 instead of r1/r2), and
an iterated local search from the natural order did not go below that. Adding the birthing
final tx in a second shared variable (`qw_*`, `v4.py`) gives (a) and (b) naturally, but sin*dz
sinks; with only sin*dz put back, 38 bytes (global permutation of tx/k/ty plus the y region).

## 4. Loop-shape findings for the record

- `-O2 -mthumb-interwork` inlines only functions declared `inline` (`flag_inline_functions` is
  set only at -O3). A `static inline` per-vertex helper produces the same RTL as the open-coded
  body (inline parameter copies are removed by CSE), so it cannot carry the shared-variable trick.
- loop.c hoists gCamera.z and gOffset.z only because each is the last use of its struct's base
  address in the loop (`force_movables`); writing the depth first moves the hoist to gOffset.y.
- The scalar loads (sin, cos, DF8, F58) are not invariant for loop.c (`loopdbg_patch.py`,
  `TXDBG=M`: `invariant_p` 0) while the struct field loads are conditionally invariant, so they
  stay in the loop as in the cartridge.

## Tools (`finish6-1115/shape/`, worker only)

- `slink_patch.py` (sched1 dependence links, costs, ready times, birthing; `TXDBG=K`) and
  `loopdbg_patch.py` (loop.c movable decisions; `TXDBG=M`), applied after finish 3, finish 4 and
  rendA's patches to a private `gcc_arm` copy (`./configure --target=arm-elf
  --host=i386-linux-gnu` needs `config.if`, `config.sub`, `install.sh` and `ginclude/` beside
  it). Diagnostic only; `trace.sh` checks the private assembly against the official compiler.
- `freedom.py` (single-move freedom of a forced order), `gen.py` + `v1.py`..`v5.py` (variant
  batches), `homes.py`, `perm.py`, `structopts.py` (search generators), plus rendA's `trace.sh`,
  `blk.py`, `wi.py`, `ordsearch.py`, `mapord.py` pointed at `~/txra-shape-cc`.
- Receipts: batch scores, top lists, the forced-order climb, the dependence trace of the race,
  the freedom probe, and measure JSONs for `g6.c` and `d8w.c`.

## Reproduce (on a worker)

```sh
S=docs/finish6-1115/shape
bash $S/trace.sh $S/c/base.c build/tb                       # "trace asm identical"
TXDBG=SK bash $S/trace.sh $S/c/base.c build/tb; grep -E "T-(119|120|121) " build/tb/trace.txt
python3 $S/freedom.py $S/c/base.c $(cat docs/finish5-1115/rendA/orders/h7x2.txt) 6 12
python3 $S/structopts.py build/s1 && python3 $S/batch.py -j 7 build/s1/*.c | sort -n | head
python3 tools/measure_candidate.py $S/c/d8w.c 08016DA8 08017E68 arm build/r   # 72
```

The worker copies (`~/txra-shape`, `~/txra-shape-cc`) were removed afterwards.

matches installed: none (193 exact C remain; 08016DA8 not installed)
near-misses improved: none in real bytes (08016DA8: 49 -> 49, g6.c stays best); new regime d8w.c (DF8 load as a global allocno) gets the cartridge's y-region registers from the natural sched1 order: 72 real, 17 with a forced order
what blocks the rest: with h7x2's RTL, sched1 provably cannot emit the dy subtraction before the DF8 load (no dependence into DF8*dy can exist under the cartridge's registers) and (b) needs a single-set final tx that cannot share r4 with cos*dx; the missing piece is an RTL in which those two pseudos differ from h7x2 without changing the final registers
