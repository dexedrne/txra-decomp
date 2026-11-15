# Renderer owner 08016DA8 installed as exact C, finish pass 6, 15 November (label: deps)

Branch `work/finish6-deps` from main bb4608a. Target: the last C owner, the ARM renderer
**08016DA8..08017E68** (4,288 bytes with its pool, 96-byte frame). Every compile, trace,
measurement, build and check ran on worker B (official `agbcc_arm` sha256 `26d884f0…`, the same
file rendB measured with). Nothing was built on the laptop. No ROM bytes were copied, printed
or committed; the only listings looked at were of our own compiler output.

**08016DA8 is now exact C and installed** as `src/generated/func_08016DA8.c`, registered in
`tools/rom.cfg` (offset 93608, size 4,288, `arm` profile, `-O2 -mthumb-interwork`). It went
from **49 differing bytes (finish 4's `g6.c`) to 0**. Exact C goes from 193 to **194**, and
`progress.json → completion` from 227 to **228 of 228**. **No C owner remains.**

## The change

The installed source is `g6.c` with the projection loop written the way the two sibling
projections already in the tree (08016C18, ARM, and 080164D0, Thumb, both exact) write it:
the camera-space y goes into `saved_y` before the second rotation, and `dy` is reused for the
rotated depth.

```c
dx = gScratch[i].x;
dx -= gCamera.x;
dy = -gScratch[i].y;
dy -= gCamera.y;
dz = gScratch[i].z - gCamera.z;
tx = dx * g_03002A18 - dz * g_03001B28;
saved_y = dy;
tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;
dy = (saved_y * g_03000DF8 - tz * g_03005F58) >> 12;
ty = saved_y * g_03005F58 + tz * g_03000DF8;
dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);
dy += gOffset.z;
g_030055F8[i].x = dy;
dy >>= 1;
f = g_0804F330[dy + 0x10000];
```

Compared with g6 that is: `dy` built in place in two statements, the `saved_y` copy, and `dy`
reused for `t >> 12`, the offset and the depth (g6's `t` and `w` are gone). `tx`, `ty` and
the sin*dz product are plain block locals; none of finish 5's shared function-scope
variables is needed. Everything outside the loop is g6 unchanged.

## Why it works (private trace compiler, `TXDBG=GRLFIS`; "trace asm identical" to the official compiler)

The hint came from the sibling: 08016C18's compiled code has the cartridge renderer's exact
instruction pattern here (`rsb y,#0; ldr DF8; rsb y,camy; mul; mov zz,asr #12; mul`), and its
source keeps `saved_y`. Its sched1 log shows what the copy does.

**(a) dy subtraction before the DF8 load.** finish 5 showed this cannot happen while the
subtraction's last consumer is `DF8*dy`: after that multiply is picked (backward list
scheduling), the subtraction is ready one cycle later and the load two cycles later, and the
only ready insn wins. With `saved_y`, the copy `p732 = p725` survives cse and combine (the
second use, in the `ty` multiply-add, comes after `dy` is reassigned, so the copy cannot be
propagated away), and both products read the copy. The pick log of the loop block
(installed source): T-120 `DF8*saved_y`, T-121 the copy (the only ready insn), T-122 the
DF8 load and the subtraction are both ready and the load wins on its birthing priority
(LAUNCH vs 2), T-123 the subtraction. Program order: `dy -= cam.y`, DF8 load, copy,
`DF8*saved_y`, which is the cartridge's sched1 order.

**Allocation.** In local allocation `saved_y` is a quantity with priority 30,000 and takes
**lr** (r0-r3 and ip are busy over its life). The three long-lived temporaries are allocated
after it: `tx` tied with the cos*dx product (12,800) takes **r4**, `ty` (9,230) **r5**, the
sin*dz product (6,315) **r6**. In global allocation `dy` has a copy preference for lr from
`saved_y` and no conflict with it (the copy's last use, the `ty` multiply-add, comes before
`dy`'s next set in sched1 order), so `dy` gets **lr**, the copy becomes `lr = lr` and is
deleted. That is exactly the allocation rendA had to force with three shared variables.

**(b) gOffset.x load after the depth store.** `tx` is a single expression, so its final
subtraction (`p727 = p760 - p763`) sets a single-set pseudo and is a birthing insn. At T-51,
right after the `dx` sum is picked, it beats the depth store (natural priority 0x2f); at
T-52 the gOffset.x load (latency 2) is ready and beats the store; the store follows at T-54.
In finish 5's sources `tx` was a shared variable with two sets, so the subtraction kept its
natural priority 0x11 and the store went first.

## Progression and ablations (real compiles, official compiler; `receipts/`)

| Source (`finish6-1115/deps/c/`) | Differing | Distance | Length | Frame |
| --- | ---: | ---: | ---: | ---: |
| finish 4 `g6.c` | 49 | 23 | 4,288 | 96 |
| finish 5 `h7x2.c` | 3,801 | 354 | 4,352 | 96 |
| `s2.c`: h7x2 + `saved_y`, `dy` reused (race (a) fixed; tx still in place) | 53 | 23 | 4,288 | 96 |
| `g2c.c`: tx1_a + `saved_y` + tx as one expression ((b) fixed; tx global, takes r2) | 40 | 6 | 4,288 | 96 |
| `A.c` / `B.c`: g6 + the loop above (tx with or without an embedded `k =`) | **0** | 0 | 4,288 | 96 |
| installed `func_08016DA8.c` (`saved_y` name, standard header) | **0** | 0 | 4,288 | 96 |

What-if (private compiler, `TXORDER`): `s2.c` with only the gOffset.x load moved after the
depth store is 0, so after the copy only (b) was left.

One-edit ablations of the installed source (`ablate.py`, `receipts/ablations.txt`): `dy` in one
statement 3,796; no copy (`t` temporary, `ty` from `dy`) 3,798; `ty` before the depth
statement 3,800; `dy = gOffset.z + (dy >> 12)` with the shift moved out of the rotation 90;
`tx` in place 53; `dx` in one statement 16; copy after the `tz` statement 0;
`dy = gOffset.z + dy` 0.

## Admission and validation (worker B, final tree)

- `tools/measure_candidate.py src/generated/func_08016DA8.c 08016DA8 08017E68 arm`:
  `"exact": true`, `"different_bytes": 0`, `"instruction_distance": 0`,
  `"emitted_bytes": 4288`, `"local_frame_bytes": 96`, `"checker_rejection": null`, compiled
  sha256 `7fa142f8…`, source sha256 `04303ab8…` ([receipt](finish6-1115/deps/receipts/measure-candidate.json)).
- `make clean; make -j8`: rc 0; 194 `C match` lines including
  `func_08016DA8: C match (4288 bytes)`; `build/txra.gba: OK`; SHA-1
  `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- `make recomp`: rc 0. `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and
  sample clock passed`.
- `tools/map_completeness.py --output build/mc.json`: 7 problems, 11 flagged unknown spans,
  1 odd pointer proposal; entries 182 reachable, 39 unreferenced, 7 reached only from those
  (unchanged).
- `tools/asm_interfaces.py --completeness build/mc.json`: assembly-interface 31 (6,092 bytes),
  covered-by-installed-owner 3 (6,406), no C-candidate; `"failures": []`; `finish.json`
  byte-identical on a second run.
- `tools/progress.py`: completion **228 of 228**, `remaining_c_owners` `[]`,
  `remaining_c_owner_bytes_including_pools` 0, `remaining_entries` 0.
- `tools/rom_map.py --refine-diff build/d.json`: 0 removed, 0 added.
- Behaviour: `docs/near-misses/finish-1114-renderer/check32.py` on the installed source (its
  `types.h` include line removed, i386 build): **199 fixtures, 0 failures, 1,053 of 1,053
  instruction addresses reached**, no ROM used ([receipt](finish6-1115/deps/receipts/check32.json)).

The source is plain structured C: no padding, inline assembly, hand bytes, fixed or explicit
registers, register variables, `volatile` or checker changes. The loop computes the same
values as g6 (`saved_y` holds the value `dy` had; `dy` ends as the same depth).

## Install bookkeeping

- `src/generated/func_08016DA8.c` (header in the style of the other installed ARM owners).
- `tools/rom.cfg`: `func_08016DA8` appended to the `matches` list with `"compiler": "arm"`.
- `tools/asm_interfaces.py`: the `C-candidate` row for 08016DA8 removed, `OWNER_END` now empty.
- `asm/program.s` (the owner is now `.incbin "build/leaves/func_08016DA8.bin"`),
  `docs/map/finish.json` and `progress.json` regenerated on worker B and copied back (listing and
  metadata only); `hand_matches_added` 87 → 88 as for earlier hand installs.
  `docs/map/functions.json` and `tools/rom.cfg` regenerate unchanged.
- README and `docs/FINISH.md` updated to 194 exact C, 228 of 228 complete; the 08016DA8 row
  left the tracker table.

## Tools (`finish6-1115/deps/`, worker only, diagnostic)

`buildcc.sh` builds the private cc1 in `~/txra-deps-cc` from the finish 3/4 trace patches and
rendA's `order_patch.py` (TXORDER, and `TXDBG=S`, the sched1 pick log with priorities and
ready list), `nonlocal_patch.py`, `lforce_patch.py`; `trace.sh`, `wi.py`, `blk.py`,
`ordsearch.py`, `ev.sh`, `tryorders.sh`, `mapord.py` are rendA's tools pointed at that copy;
`batch.py` (rendB) scores many sources; `mk.py` swaps the projection-loop body of a base
source; `gen1.py`/`gen1b.py`/`gen3.py` generated the tx-form, statement-order and
sharing grids (108 + 108 + 16 sources); `ablate.py` the ablations. `orders/s2-actual.txt` is
s2's natural sched1 order (insn uids).

## Reproduce (on a worker)

```sh
D=docs/finish6-1115/deps
python3 tools/measure_candidate.py src/generated/func_08016DA8.c 08016DA8 08017E68 arm /tmp/m   # exact
bash $D/buildcc.sh $PWD/docs                       # private cc1 (diagnostic only)
TXDBG=GRLFIS bash $D/trace.sh src/generated/func_08016DA8.c /tmp/t && python3 $D/blk.py /tmp/t --lq
grep '^S1 b=18 ' /tmp/t/trace.txt                  # sched1 picks of the projection block
```

## Worker runs (worker B)

Worker copy `~/txra-deps`, private compiler `~/txra-deps-cc`, traces `~/deps-out`, logs
`~/deps-*.log`. Grids ran as short foreground batches; the full rebuild and the validation
scripts ran detached with logs and time limits and were waited for in the foreground. All of
them were removed at the end.

matches installed: 08016DA8 (ARM renderer owner, 4,288 bytes with pool, 96-byte frame; exact C 193 -> 194, completion 227 -> 228 of 228)
near-misses improved: 08016DA8: 49 -> 0 (installed)
what blocks the rest: nothing; no C owner remains (228 of 228 entries complete: 194 exact C, 3 covered labels, 31 documented assembly interfaces)
