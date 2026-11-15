# 15 November: integration of finish pass 5 (label: integrate5)

Branch `work/finish5-int`, started from main 1670de2 (the finish-pass-4 integration). It merges the three finish-pass-5 branches. The sound lane installed 080064A4 as exact C, so exact C goes from 192 to 193 and `completion` from 226 to 227 of 228. The two renderer lanes installed nothing. Every build, measurement and check ran on worker A; the laptop only merged and edited documentation. No push and no merge into main.

## Merge order and result

| Branch | Commits | Merge | Result |
| --- | --- | --- | --- |
| finish5-sound | 5a46ebc, 5ed5471, 2044819 | e1be343 | Clean, merged first because it installs a match. `src/generated/func_080064A4.c`, its `tools/rom.cfg` entry, the `tools/asm_interfaces.py` row and extent changes, the updated far-jump test, the regenerated `asm/program.s`, `docs/map/finish.json` and `progress.json`, README and tracker totals, round note and receipts (`finish5-1115/sound/`). |
| finish5-rendA | cb9967c | 3b90d5b | Clean. Round note, sources (`h7x2.c`, `tx1_a.c`, `v1b.c` and others), three diagnostic compiler hooks, the forced-order search tool, forced orders and receipts (`finish5-1115/rendA/`). Docs only. |
| finish5-rendB | 1a87d3a | 6012763 | Clean. Round note, seven experiment sources (`s002_dyr_txip.c` and others), diagnostic hooks, search and anneal tools and receipts (`finish5-1115/rendB/`). Docs only. |

All three lanes branched from 1670de2. The renderer lanes touch only new paths under their own folders, so nothing overlapped with the sound install and there was nothing to resolve. Neither renderer lane installed, so there was no choice to make between them; both are kept as records.

## Totals, main → integrated

| | main (1670de2) | work/finish5-int |
| --- | ---: | ---: |
| Registry entries | 228 | 228 |
| Exact C replacements | 192 (85,426 bytes with pools) | **193** (89,254 bytes with pools) |
| `completion`: complete entries | 226 of 228 | **227 of 228** (193 exact C + 3 covered labels + 31 assembly) |
| Instruction bytes inside exact owners | 71,804 (83.9%) | **75,274 (88.0%)** |
| Documented assembly | 6,092 (7.1%) | 6,092 (7.1%) |
| Remaining C owners | 2: 7,682 instruction bytes (9.0%), 8,116 with pools | **1**: 08016DA8, 4,212 instruction bytes (4.9%), 4,288 with pools |
| 080064A4 sound, differing bytes | 90 | **0 (installed)** |
| 08016DA8 renderer, best differing bytes | 49 (distance 23) | 49 (distance 23, unchanged) |
| `hand_matches_added` | 86 | 87 |

`progress.json → functions_matched_c.percent_of_mapped_code` now reads 104.295, because it divides pool-inclusive matched bytes by mapped instruction bytes. The README quotes the instruction-byte share (88.0%) instead, as the sound lane set it up.

## Owners re-measured on the integrated tree (worker A)

| Owner | Source | Profile | Differing bytes | Output / target | Frame | Instruction edits | Compiled sha256 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 080064A4 sound | `src/generated/func_080064A4.c` (installed) | old | **0**, `"exact": true` | 3,828 / 3,828 | 108 | 0 | e3916782… |
| 08016DA8 renderer | `finish4-1115/renderer/c/g6.c` (not installed) | arm | 49 | 4,288 / 4,288 | 96 | 23 | 734c5e9d… |

Source sha256 90b6777c… (sound) and 1b535c18… (renderer) and compiler sha256 90bdd572… (old) and 34268789… (ARM) match the lane receipts and the finish-4 integration. rendB's `receipts/g6-remeasure.json`, taken on worker B, records a different compiler file hash (26d884f0…) with the same compiled output hash.

## What the renderer lanes established

Both lanes agree on the cartridge's allocation for the projection loop (0801737A..080173F8): dy is written in place and reused as the final depth, which takes lr; tx is computed in place; and tx, ty and the sin*dz product are global rather than local pseudos, so no local takes lr before dy. With that and one forced sched1 order of the loop block, the whole function comes out exact in a diagnostic compiler:

- rendA, `h7x2.c` and `tx1_a.c`: plain C that already gets that allocation (each of the three values goes in a function-scope variable that the direct path also uses for one point-to-packet copy, so flow sees two blocks and makes it global, and combine folds the direct-path copy back). Byte-identical with only the loop block's sched1 order forced; 3,801 bytes off as compiled, because the natural order differs.
- rendB, `s002_dyr_txip.c`: g6 with dy reused for the depth and dy and tx built in place. 18 bytes with the forced order alone; 0 with lr refused to local-alloc in that block, or with tx, ty and sin*dz forced non-local.

What blocks the install: no natural source yet makes sched1 emit the dy subtraction before the DF8 load (rendA: once DF8*dy is picked, the subtraction is ready one cycle before the load and nothing else is ready then) and the gOffset.x load after the depth store. The diagnostic hooks are for diagnosis only; their effect cannot be installed.

## Validation (worker A, final merged tree)

- `make clean; make -j8`: rc 0; 193 `C match` lines, including `func_080064A4: C match (3828 bytes)` and `func_080181C0: C match (1684 bytes)`; `build/txra.gba: OK`; SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `tools/measure_candidate.py src/generated/func_080064A4.c 080064A4 08007398 old`: `"exact": true`, `"different_bytes": 0`, `"instruction_distance": 0`, `"emitted_bytes": 3828`, `"local_frame_bytes": 108`, `"checker_rejection": null`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- `make recomp`: rc 0.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed`, with `fallback=0 unknown=0 unsupported=0`.
- `tools/map_completeness.py --output build/mc.json`: 7 problems, 11 flagged unknown spans, 1 odd pointer proposal; entries 182 reachable, 39 unreferenced, 7 reached only from those. Unchanged.
- `tools/asm_interfaces.py --completeness build/mc.json`: classes assembly-interface 31 (6,092 bytes), covered-by-installed-owner 3 (6,406), C-candidate 1 (4,288); `"failures": []`. `docs/map/finish.json` regenerates byte-identical to the committed file, also on a second run.
- `tools/progress.py`: `completion` 227 of 228, `remaining_c_owners` `["0x08016DA8"]`, `remaining_c_owner_bytes_including_pools` 4,288.
- `tools/rom_map.py --refine-diff build/d.json`: 0 removed, 0 added.
- `make` and the tools above regenerate `asm/program.s`, `progress.json`, `docs/map/finish.json`, `tools/rom.cfg` and `docs/map/functions.json` byte-identical to the committed files (the sound lane had already regenerated them), so no regenerated file changed in this commit.

README and the `docs/FINISH.md` verdict and 08016DA8 tracker row now cite the finish-pass-5 notes. The worker copy and logs on worker A were removed afterwards.

matches installed: 080064A4 (sound owner, 3,828 bytes with pool, 108-byte frame; exact C 192 -> 193, completion 226 -> 227 of 228)
near-misses improved: 080064A4: 90 -> 0 (installed); 08016DA8: 49 -> 49 (unchanged; what-ifs reach 0 only with a forced sched1 order)
what blocks the rest: only 08016DA8 remains: the register allocation is reproduced by plain C, but no natural source makes sched1 emit the dy subtraction before the DF8 load and the gOffset.x load after the depth store in the projection loop
