# Sound owner 080064A4 installed as exact C, finish5 round, 15 November (label: sound)

Branch `work/finish5-sound` from main 1670de2. Every compile, trace, measurement, build and
check ran on worker A (old_agbcc sha256 `90bdd572…`). Nothing was built on the laptop. No ROM
bytes were copied, printed or committed.

**The sound owner 080064A4..08007398 is now exact C and installed** as
`src/generated/func_080064A4.c`, registered in `tools/rom.cfg` (offset 25764, size 3,828 with
the pool, default `old` profile, `-O2 -mthumb-interwork`). It went from **90 differing bytes
to 0**. Exact C goes from 192 to **193**, and `progress.json → completion` from 226 to
**227 of 228**. **One C owner remains**: 08016DA8 (renderer).

| Step (receipts in `finish5-1115/sound/progression.json`) | Bytes | Frame | Edits | Differing |
| --- | ---: | ---: | ---: | ---: |
| finish4 near-miss | 3,828 | 108 | 87 | 90 |
| finish4 + tone note-start envelopes on the shared `slide` pointer (alone) | 3,852 | 108 | 268 | 1,063 |
| finish4 + slide pitch sums in the function-level `gain` temporary (alone) | 3,836 | 108 | 689 | 3,303 |
| both of the above | 3,828 | 108 | 20 | 23 |
| + 0x69 command value through a block temporary (alone on finish4: 87) | 3,828 | 108 | 17 | 20 |
| + `gTempoCounter += gTempo;` (alone on finish4: 91) | 3,828 | 108 | 15 | 18 |
| + effect stop flag kept in `gain` (alone on finish4: 72) | 3,828 | 108 | 0 | **0** |
| installed (unused `p` and `effect` removed, `gain` renamed `tmp`, header) | 3,828 | 108 | 0 | **0** |

The installed source is plain structured C: no padding, inline assembly, fixed or explicit
registers, register variables or checker changes. Measurement receipt:
[measure.json](finish5-1115/sound/measure.json) (exact, compiled sha256 `e3916782…`, source
sha256 `90b6777c…`).

## How the three allocator decisions were found

The finish4 debug build was rebuilt on worker A as `~/txra-sound5-cc` (the finish4
`trace_patch.py`..`trace_patch3.py` plus a new `trace_patch4.py`, which adds the what-if
`TXNOMOVE=uid`: loop.c never moves that movable). With no override set, its assembly was
identical to the official compiler's for every source traced ("traced==official"). What-ifs are
diagnosis only; every number in the table above is from the official measure path.

### 1. Envelope tick (region D, 67 rows): the shared pointer must take r2

What-ifs on the finish4 source: `TXLEN=38:110` alone (pointer priority 3.93, above the
`&slide[cursor]` temporaries at 3.86) changes nothing, because the slide sum `p` (8.33) still
takes r2 first; `TXLEN=38:110,23:200` (pointer above the temporaries, `p` below the pointer)
makes the region exact. So two natural changes were needed together:

- The tone note-start code (`START_TONE`) loads its volume, arp and slide envelopes into the same
  `slide` pointer as the tick code and the noise channel, instead of a block-local `seq`. The
  pointer goes from refs 72 / live length 193 (2.24) to 180 / 318 (**3.96**), above the
  temporaries. Alone it changes the note-start code (3,852 bytes), because `p` still takes r2
  first and the pointer lands on r3 everywhere.
- The slide pitch sum no longer has its own variable: it uses the function-level `gain`
  temporary (the fade gain of the mix-buffer scale loop, dead by then). The merged temporary is
  live across the scale loop's local `b` (r2, a local-alloc quantity), so global allocation
  cannot give it r2; it takes **r3**, which is exactly the original's register for the sum.
  Alone it changes the code shape (3,303); with the pointer change, the whole envelope tick and
  note-start code match (23 bytes left, region B only).

### 2. Tempo block (5 rows): local-alloc must give the gTempo address r2

gcse inserts a load of the gTempo address at the end of the tempo block for the 0x69 command
(`gTempo = ...`) inside the voice loop. In the finish4 source, the second loop pass moves that
command's address load out of the command loop (insn 4171: savings 1, lifetime 5, threshold
26 × 1 × 5 = 130 ≥ 120 insns), with its REG_EQUAL constant, so the gcse register dies and is
deleted. `TXNOMOVE=4171` made the tempo block exact. With the 0x69 command written
`{ u32 t = commands[gVoices[i].command + 1]; gTempo = t; }`, the address is loaded just before
the store (lifetime 1, not moved), the gcse register survives, cse2 turns its insertion into a
copy of the tempo block's own address register, and that register now lives until the end of
the block. Local-alloc's three-quantity sort then sees address [4,14) priority 3,000, counter
value 5,000 and tempo value 10,000 (both comparisons "better"), allocates tempo value r0,
counter value r1, address **r2**, and global allocation gives the counter address **r3**. The
gcse register itself is never allocated (constant equivalence), so its copy is deleted and the
0x69 code is unchanged. `gTempoCounter += gTempo;` gives the original load order (counter first).

### 3. Effect loop (15 rows): `events16` must not take r2 or r3

Order needed: base copy (r2), `stop` (r3), `events16` (r4). With `stop` as its own `s16`, the
base copy (refs 4 / length 15, 0.533) ranks below `events16` (10 / 54, 0.556), and no change
of `stop` alone can fix that; the final code fixes refs and length of `events16` (`TXREFS`,
`TXLEN=133:73`, `TXPREF=133:4` and `TXLEN=240:14,134:43` were each exact as what-ifs). The
natural form keeps the stop flag in the same function-level temporary: it is allocated early
(refs 56 / length 75, priority 3.73) and gets r3 as above, so `stop` is r3; without the `s16`
extension pair the base copy's length is 13 (0.615) and it takes r2 ahead of `events16`
(10 / 52, 0.577), which then takes **r4**.

The three edits are behaviour-preserving: `gain`/`tmp` is dead between its uses (the fade gain
ends with the scale loop, the stop flag is set to 0 before use, the pitch sum is set before
use), and the tempo and 0x69 forms compute the same values.

## Behaviour check

`docs/near-misses/finish2-1115-sound/diff32.py`, finish4 source as reference and the installed
source (with its `types.h` include line removed, i386 build) as candidate: **1000/1000**
identical states with seed 1115 and **1000/1000** with seed 2026. C-to-C regression only.

## Install bookkeeping

- `tools/rom.cfg`: `func_080064A4` appended to the one-line `matches` list.
- `tools/asm_interfaces.py`: the `C-candidate` row and the `OWNER_END` extent for 080064A4
  removed; the five long-branch labels (08006712, 08006740, 08006776, 0800735C, 08007368) are
  now `covered-by-installed-owner`, as 08003786 was for 08002854.
- `tests/test_mixer_far_jumps.py`: the listing test now expects the verified leaf
  (`.incbin "build/leaves/func_080064A4.bin"`) and no `loc_`/`func_` labels for the five
  interior addresses; the far-jump, registry and lifter tests are unchanged and pass.
- `asm/program.s`, `docs/map/finish.json` and `progress.json` were regenerated on worker A and
  copied back (listing and metadata only). `hand_matches_added` 86 → 87, as for earlier hand
  installs. README and `docs/FINISH.md` updated to 193 / 227 of 228.
- The finish4 near-miss directory is kept as history; this round's tools, specs (`vgen.py`
  spec files), mini tests and receipts are in [finish5-1115/sound](finish5-1115/sound/).

## Admission and validation (all on worker A, final tree)

- `tools/measure_candidate.py src/generated/func_080064A4.c 080064A4 08007398 old`:
  `"exact": true`, `"different_bytes": 0`, `"instruction_distance": 0`,
  `"emitted_bytes": 3828`, `"local_frame_bytes": 108`.
- `make clean; make -j8`: rc 0, 193 `C match` lines including
  `func_080064A4: C match (3828 bytes)`, `build/txra.gba: OK`, SHA-1
  `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)` (before the listing-test update: 1 failure,
  `test_generated_listing_uses_local_labels`, expected after an install).
- `make recomp`: rc 0. `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and
  sample clock passed` (`fallback=0 unknown=0 unsupported=0`).
- `tools/map_completeness.py --output build/mc.json`: 7 problems, 11 flagged unknown spans,
  1 odd pointer proposal; entries 182 reachable, 39 unreferenced, 7 reached only from those
  (unchanged).
- `tools/asm_interfaces.py --completeness build/mc.json`: assembly-interface 31,
  covered-by-installed-owner 3, C-candidate 1; `"failures": []`; `finish.json` byte-identical
  on a second run.
- `tools/progress.py`: completion 227 of 228, `remaining_c_owners` `0x08016DA8`,
  `remaining_c_owner_bytes_including_pools` 4,288.
- `tools/rom_map.py --refine-diff build/d.json`: 0 removed, 0 added.

## Worker runs (worker A)

All work ran in the worker copy `~/txra-sound5` and the debug-compiler copy `~/txra-sound5-cc`
(label prefix `sound`). Runs were short foreground batches (variant grids of 6 to 63 sources,
what-ifs, traces); the full rebuild and the validation script ran detached with logs and time
limits and were waited for in the foreground. One validation run was stopped by its exact PIDs
after a stale `asm/program.s` was synced over the regenerated one; it was rerun after a clean
rebuild. Both worker copies and the logs were removed at the end.

matches installed: 080064A4 (sound owner, 3,828 bytes with pool, 108-byte frame; exact C 192 -> 193, completion 226 -> 227 of 228)
near-misses improved: 080064A4: 90 -> 0 (installed)
what blocks the rest: only 08016DA8 (renderer) remains, at 49 differing bytes from finish4 (22 register rows in the projection loop); it was not worked in this lane
