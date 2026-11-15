# Renderer owner 08016DA8 installed as exact C, finish pass 6, 15 November (label: base)

Branch `work/finish6-base` from main bb4608a. Every compile, trace, measurement, build and
check ran on worker C (official `agbcc_arm` sha256 `34268789…`). Nothing was built on the laptop.
No ROM bytes were copied, printed or committed; only measurement JSON, insn-uid logs, our own
compiler output and sanitized listings (mnemonics, no encodings, no pool words) were read.

**The ARM track-face renderer 08016DA8..08017E68 is now exact C and installed** as
`src/generated/func_08016DA8.c`, registered in `tools/rom.cfg` (offset 93608, size 4,288 with
the pool, `arm` profile, `-O2 -mthumb-interwork`). It went from **49 differing bytes to 0**.
Exact C goes from 193 to **194**, and `progress.json → completion` from 227 to
**228 of 228**. **No C owner remains.**

The installed source is plain structured C: no padding, inline assembly, hand bytes, fixed or
explicit registers, register variables, volatile or checker changes. Measurement receipt for
the installed file: exact, source sha256 `12df7a98…`, compiled sha256 `7fa142f8…`
(`finish6-1115/base/receipts/measure.jsonl`, last line).

## Result

| Source | Differing bytes | Instruction distance | Emitted / target | Frame |
| --- | ---: | ---: | ---: | ---: |
| finish 4 `g6.c` (best before) | 49 | 23 | 4,288 / 4,288 | 96 |
| finish 5 `h7x2.c` (allocation-exact under a forced sched1 order) | 3,801 | 354 | 4,352 | 96 |
| `gensv.py`: h7x2 + a `sv = dy` copy kept global through the direct path (all 16 forms) | 75 | 26 | 4,288 | 96 |
| `c/sib0.c`: h7x2 with the loop written like 08016C18 | **0** | 0 | 4,288 | 96 |
| `c/sib1.c`: g6 with the loop written like 08016C18 | **0** | 0 | 4,288 | 96 |
| installed (sib1 with the depth written to `g_030055F0[i].z`, header) | **0** | 0 | 4,288 / 4,288 | 96 |

All numbers are official-compiler measurements (`tools/measure_candidate.py`, receipts in
`finish6-1115/base/receipts/measure.jsonl`). `sib1.c` also passes the 11/14 synthetic
differential checker on the pre-install tree: 199 fixtures, 0 failures, all 1,053 instruction
addresses executed (`receipts/check-sib1.json`). After the install the checker cannot run any
more, because its reference executor reads the textual listing of 08016DA8, which the install
replaces by the verified leaf; the compiled bytes are the original's.

## The projection loop that was missing

The installed ARM sibling **08016C18** (point-grid projection, exact since 11/2) does the same
camera transform and the same pitch rotation as this loop, with the same compiler profile.
None of the earlier renderer rounds had used it as a template. Its statements, copied into the
renderer unchanged except for the renderer's own arrays, give the exact function at once:

```c
for (i = 0; i < 4; i++) {
    s32 x, y, z, xx, zz, saved_y, factor;
    x = gScratch[i].x;
    y = -gScratch[i].y;
    z = gScratch[i].z;
    x -= gCamera.x;
    y -= gCamera.y;
    z -= gCamera.z;
    xx = (x * g_03002A18 - z * g_03001B28) >> 12;
    saved_y = y;
    zz = (x * g_03001B28 + z * g_03002A18) >> 12;
    y = (saved_y * g_03000DF8 - zz * g_03005F58) >> 12;
    z = (saved_y * g_03005F58 + zz * g_03000DF8) >> 12;
    x = xx + gOffset.x;
    z += gOffset.y;
    y += gOffset.z;
    g_030055F0[i].z = y;
    z <<= 3;
    y >>= 1;
    factor = g_0804F330[y + 0x10000];
    gCurPacket->x[i] = (((x << 3) * factor) >> 16) + 60;
    gCurPacket->y[i] = ((z * factor) >> 15) + 80;
}
```

Why it works, from the private tracing compiler (finish 3/4/5 patches plus rendA's hooks,
`buildcc.sh`; its assembly is identical to the official compiler's for every source traced):

1. **The copy survives to sched1.** `y` is reassigned (the depth) before the second use of
   `saved_y`, so CSE can rewrite only the first product back to `y` (`DF8*y`); the copy
   `saved_y = y` stays because `saved_y` is still needed by the ty multiply-add. Combine leaves
   it because `y` is still live after the copy. **regmove** (`optimize_reg_copy_1`) then moves
   the first product onto `saved_y`, so `y` dies at the copy (insn 1679 in the `-dN` dump:
   `REG_DEAD y`; insn 1700 now reads `saved_y`).
2. **sched1 then produces the order finish 5 required.** In the backward list scheduler,
   once `DF8*saved_y` is picked (T-120 in the `TXDBG=S` log), the copy is the only ready insn
   at T-121 (an ALU insn, birthing, so it gets the launch priority). The dy subtraction becomes
   ready only at T-122, together with the DF8 load, whose launch priority wins; the subtraction
   follows at T-123. Program order is therefore `dy -= cam.y; load DF8; saved_y = y; DF8*saved_y`,
   which is the cartridge's (a) (rendA's "race", which this scheduler cannot win without an insn
   between the subtraction and the product). The gOffset.x load also lands after the depth
   store, (b), with no further change.
3. **The copy disappears in allocation.** Local-alloc gives `saved_y` lr (`;; Register 729 in
   14.` in the `-dl` dump), so no other local takes lr during the pitch rotation (the problem
   rendA solved with three global helper variables). Global allocation then gives `y` lr through
   the copy preference (`GF reg=725 ... best=14 pref=4000 copy=4000`), the copy becomes
   `mov lr, lr` and is deleted. With sched1's order, local-alloc's widened lifetimes give cam.y
   and `DF8*y` r1 and the y load and DF8 r2, as finish 4 had worked out.

So the shared function-scope helpers of rendA's `h7x2.c` (tx in the header depth, k and ty in
the direct path) are not needed: `sib1.c` is finish 4's clean `g6.c` with only the loop body
replaced. Placing a plain copy elsewhere does not work: with `t` kept separate (`sv = dy;
t = sv * DF8 - ...; ty = sv * F58 + ...`), CSE makes the copy dead unless `sv` lives past the
block, and if it does (`gensv.py`, `sv` shared with a direct-path copy), combine folds the dy
subtraction into the copy and the race is back (75 bytes, all 16 placements identical).

## Struct and base angle (this lane's assignment)

Ground truth first: every installed function that touches these globals was grepped.

| Address | Installed exact users | How they declare it |
| --- | --- | --- |
| 03002A18, 03001B28, 03000DF8, 03005F58 | 08016264, 080162F8, 080164D0, 080165BC, 08016C18 | four separate `s32` globals |
| 03005F70 (camera) | 080162F8, 080164D0, 080165BC, 08016C18, 08007B28, 0800B4D8, 0800BBD4, 0800D51C | separate 12-byte triple (`TxraTriple` / `DeepVector`) |
| 03005F80 (offset) | 08016264, 080162F8, 080164D0, 080165BC, 08016C18 | separate 12-byte triple |
| 03000DE0 | 08007B28, 0800B4D8 | separate `u32` scalar |
| 030057A0 (scratch points) | 080162F8, 080164D0, 0800421C, 080095E4, 08009D94, 08009F84, 080181C0 | triple array |
| 030055F8 | none; 080162F8 and 080164D0 write the depth as `.field_08` / `.z` of the triple array at **030055F0** | triple array at 030055F0 |

Then each plausible grouping was rebuilt on the exact source (`genstruct.py`) and measured with
the official compiler:

| Variant | Differing bytes | Emitted | Frame |
| --- | ---: | ---: | ---: |
| s1: depth as `g_030055F0[i].z` (as 080164D0) | **0** | 4,288 | 96 |
| s6: camera as `s32[3]` | **0** | 4,288 | 96 |
| s4: camera + offset in one struct at 03005F70 | 3,585 | 4,320 | 92 |
| s3: count 03000DE0 + pitch cosine 03000DF8 in one struct | 3,267 | 4,316 | 100 |
| s2: view struct at 03005F58 (pitch sine, camera, offset) | 3,673 | 4,324 | 96 |
| s5: s2 + s3 | 3,553 | 4,316 | 100 |

Groupings that let two of these loads share a base register (s2 to s5) change the cartridge's
addressing: the cartridge loads each of the four trig globals, the camera and the offset from
its own literal-pool word with offset 0/4/8, which only separate objects (or a struct whose
first member is the object) produce. So the sine, cosine, camera, offset and counter were
separate objects in the original, as all installed siblings already declare them. The one
grouping that the ground truth supports, the depth as the z word of the 12-byte rows at
030055F0, is byte-neutral and is used in the installed source; the camera as an array is
byte-neutral too but has no support in the siblings and is not used. None of the groupings
changes the sched1 order of the loop block; the order came from the sibling idiom above.

## Install bookkeeping

- `src/generated/func_08016DA8.c`: `sib1.c` with the house header (`types.h` include), the
  depth written to `g_030055F0[i].z` and a descriptive comment.
- `tools/rom.cfg`: `func_08016DA8` (offset 93608, size 4288, `"compiler": "arm"`) appended to
  the one-line `matches` list.
- `tools/asm_interfaces.py`: the `C-candidate` row for 08016DA8 removed and `OWNER_END`
  emptied (no owner extent is left to check).
- `asm/program.s` (the 08016DA8 listing becomes `.incbin "build/leaves/func_08016DA8.bin"`),
  `docs/map/finish.json` (no C-candidate row; 31 assembly interfaces, 3 covered labels) and
  `progress.json` (194 exact C, completion 228 of 228, `remaining_c_owners` empty) were
  regenerated on worker C and copied back (listing and metadata only); `hand_matches_added` 87 → 88,
  as for earlier hand installs. `docs/map/functions.json` and `tools/rom.cfg` regenerate
  byte-identical.
- README progress block and history, and `docs/FINISH.md` (verdict, totals, done definition,
  tracker row removed) updated to 194 exact C / 228 of 228.
- No test needed a change (no test lists the renderer's interior).

## Admission and validation (worker C, final tree)

- `tools/measure_candidate.py src/generated/func_08016DA8.c 08016DA8 08017E68 arm`:
  `"exact": true`, `"different_bytes": 0`, `"instruction_distance": 0`,
  `"emitted_bytes": 4288`, `"target_bytes": 4288`, `"local_frame_bytes": 96`,
  `"checker_rejection": null`, compiler sha256 `342687894970…`, compiled sha256 `7fa142f8d511…`.
- `make clean; make -j8`: rc 0, 194 `C match` lines including
  `func_08016DA8: C match (4288 bytes)`, `build/txra.gba: OK`, SHA-1
  `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- `make recomp`: rc 0. `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and
  sample clock passed` (`fallback=0 unknown=0 unsupported=0`).
- `tools/map_completeness.py --output build/mc.json`: 7 problems, 11 flagged unknown spans,
  1 odd pointer proposal; entries 182 reachable, 39 unreferenced, 7 reached only from those
  (unchanged).
- `tools/asm_interfaces.py --completeness build/mc.json`: assembly-interface 31 (6,092 bytes),
  covered-by-installed-owner 3 (6,406); no C-candidate; `"failures": []`.
- `tools/progress.py`: `functions_matched_c` 194 (93,542 bytes with pools); completion
  `complete_entries` 228 of 228, `remaining_c_owners` `[]`, `remaining_entries` 0.
- `tools/rom_map.py --refine-diff build/d.json`: 0 removed, 0 added.
- After that run, `asm/program.s`, `docs/map/finish.json`, `progress.json`,
  `docs/map/functions.json` and `tools/rom.cfg` on the worker are byte-identical to the
  committed files (sha256 checked).

## Tools (`finish6-1115/base/`, worker only)

- `buildcc.sh`: private diagnostic `cc1` at `~/base-cc` with finish 3's four patches, finish
  4's two and rendA's `order_patch.py`, `nonlocal_patch.py`, `lforce_patch.py`. Diagnostic only.
- `trace.sh`, `wi.py`, `blk.py`: rendA's tools pointed at that compiler (trace: official vs
  private assembly must be identical; `TXDBG=S` gives the sched1 picks).
- `gensv.py` (copy-variable experiments on h7x2), `genstruct.py` (the struct and base
  groupings above), `batch.sh` (private-compiler scores), `measure_all.sh` (official
  measurements as JSON lines), `validate.sh` (admission measure, `make clean; make -j8` and
  the full check list).
- Sources: `c/sib0.c`, `c/sib1.c`; the generated variants are reproducible from the scripts.

## Reproduce (on a worker, never the laptop)

```sh
B=docs/finish6-1115/base
python3 tools/measure_candidate.py src/generated/func_08016DA8.c 08016DA8 08017E68 arm /tmp/r   # exact
bash $B/measure_all.sh docs/finish4-1115/renderer/c/g6.c $B/c/sib1.c                          # 49, 0
python3 $B/genstruct.py $B/c/struct && bash $B/measure_all.sh $B/c/struct/*.c
bash $B/buildcc.sh && TXDBG=S bash $B/trace.sh $B/c/sib1.c /tmp/t -dN   # sched1 log, regmove dump
bash $B/validate.sh
```

The worker copies (`~/txra-base`, `~/txra-base-s`, `~/base-cc`, `~/base-out`, `~/base-logs`)
were removed after the receipts were copied.

matches installed: 08016DA8 (ARM track-face renderer, 4,288 bytes with pool, 96-byte frame; exact C 193 -> 194, completion 227 -> 228 of 228)
near-misses improved: 08016DA8: 49 -> 0 (installed)
what blocks the rest: nothing; no C owner remains (228 of 228 entries complete: 194 exact C, 3 covered labels, 31 documented assembly interfaces)
