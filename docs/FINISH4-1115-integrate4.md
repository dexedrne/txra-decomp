# 15 November: integration of finish pass 4 (label: integrate4)

Branch `work/finish4-int`, started from main 4e61362 (the finish-pass-3 integration). It merges the two finish-pass-4 branches. Neither lane installed a match, so no C replacement is added or removed, and `src/`, `tools/rom.cfg`, the registry, `asm/` and the map files are unchanged. Every build, measurement and check ran on worker A; the laptop only merged and edited documentation. No push and no merge into main.

## Merge order and result

| Branch | Commits | Result |
| --- | --- | --- |
| finish4-sound | bacf3c9 | Clean. Round note, near-miss source and receipts (`near-misses/finish4-1115-sound/`), debug-build patches, what-if and search scripts (`finish4-1115/sound/`). Docs only. |
| finish4-renderer | fec174d .. 498c7e4 (6) | Clean. Round note, sources `g1.c`–`g6.c`, receipts, search and allocator-trace tools and two trace-compiler patches (`finish4-1115/renderer/`). Docs only. |

Both lanes branched from 4e61362 and touch disjoint new paths, so there was nothing to resolve. There were no installed matches to merge first.

## Totals, main → integrated

| | main (4e61362) | work/finish4-int |
| --- | ---: | ---: |
| Registry entries | 228 | 228 |
| Exact C replacements | 192 (85,426 bytes with pools, 99.8%) | 192 (unchanged) |
| `completion`: complete entries | 226 of 228 | 226 of 228 (192 exact C + 3 covered labels + 31 assembly) |
| Instruction bytes inside exact owners | 71,804 (83.9%) | 71,804 (83.9%) |
| Documented assembly | 6,092 (7.1%) | 6,092 (7.1%) |
| Remaining C owners | 2: 7,682 instruction bytes (9.0%), 8,116 with pools | 2 (unchanged) |
| 080064A4 sound, best differing bytes | 159 | **90** |
| 08016DA8 renderer, best differing bytes | 863 (lowest distance 322) | **49** (distance 23) |

## Remaining owners, re-measured on the integrated tree (worker A)

`tools/measure_candidate.py` on each lane's best near-miss gives the same bytes and compiled hashes as the lane receipts:

| Owner | Source | Profile | Differing bytes (finish3 → finish4) | Output / target | Frame | Instruction edits | Compiled sha256 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 080064A4 sound | `near-misses/finish4-1115-sound/func_080064A4.c` | old | 159 → **90** | 3,828 / 3,828 | 108 / 108 | 134 → **87** | b44e8d5a… |
| 08016DA8 renderer | `finish4-1115/renderer/c/g6.c` | arm | 863 → **49** | 4,288 / 4,288 | 96 / 96 | 322 → **23** (lowest finish3 distance; the 863-byte candidate had 381) | 734c5e9d… |

Neither candidate is installed. Source sha256 b6313992… (sound) and 1b535c18… (renderer) match the lane receipts, and so do the compiler hashes (90bdd572… for the old profile, 34268789… for the ARM profile).

What blocks each owner, in short (details in the lane notes):

- **080064A4** ([sound note](FINISH4-1115-sound.md)): 90 bytes, all register choice, from three allocator decisions. The shared envelope pointer must take r2 before the slide sum and the `&slide[cursor]` temporaries (67 rows in region D). The effect loop's `events16` must rank below `stop` (15 rows; it needs a live length of 74 or more). Local-alloc must give the gTempo address r2 (5 rows; not reachable with the current RTL). With the first two forced in the debug build, 5 bytes remain.
- **08016DA8** ([renderer note](FINISH4-1115-renderer.md)): 49 bytes, 22 register rows in the projection loop (0801737A..080173F8). The original's final depth is a non-local pseudo that shares lr with dy, but reusing dy adds a full-latency anti-dependence that changes sched1. cam.y and DF8*dy share r1 only if sched1 puts the DF8 load between `dy` and `t`, which the candidate misses by a one-cycle latency race.

## Validation (worker A, final merged tree)

- `make clean; make -j8`: 192 `C match` lines, including `func_080181C0: C match (1684 bytes)`; `build/txra.gba: OK`; SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`. Run again after the documentation edits, with the same result.
- `make recomp`: `Emitted 228 functions, 258 load/run entries`.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed`, with `fallback=0 unknown=0 unsupported=0`.
- `tools/map_completeness.py`: 7 closure notes, 11 flagged unknown spans and 1 rejected odd pointer; entries 182 reachable, 39 unreferenced, 7 reached only from those. Unchanged. Against the committed receipt `finish-1114/completeness-int.json.gz` the output differs only in four `status` fields (08002854, 0800421C and 080181C0 now `exact C`, 08003786 `inside installed owner 0x08002854`), which record the installs since 11/14; the receipt is left as the 11/14 record.
- `tools/asm_interfaces.py --completeness`: classes assembly-interface 31, covered-by-installed-owner 3, C-candidate 2; `"failures": []`. `docs/map/finish.json` regenerates byte-identical to the committed file, also on a second run.
- `tools/progress.py`: `completion` 226 of 228, `remaining_c_owners` 080064A4, 08016DA8, `remaining_c_owner_bytes_including_pools` 8,116. `progress.json` regenerates byte-identical to the committed file.
- `make` regenerates `asm/program.s` and leaves `tools/rom.cfg` and `docs/map/functions.json` byte-identical to the committed files.
- `tools/rom_map.py --refine-diff`: 0 removed, 0 added.

README and the `docs/FINISH.md` verdict and tracker rows are updated to these numbers. The worker copy and logs on worker A were removed afterwards.

matches installed: none (192 exact C unchanged; completion stays 226 of 228)
near-misses improved: 080064A4: 159 -> 90 (instruction distance 134 -> 87); 08016DA8: 863 -> 49 (instruction distance 322 -> 23); length and frame exact for both
what blocks the rest: register choice only. In 080064A4 the shared envelope pointer must take r2 before the slide temporaries (67 rows), events16 must rank below stop in the effect loop (15 rows) and local-alloc must give the gTempo address r2 (5 rows); in 08016DA8 the projection loop's final depth must share lr with dy without changing sched1, and the DF8 load must land between dy and t so cam.y and DF8*dy share r1 (22 rows)
