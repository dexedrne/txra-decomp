# 15 November: integration of finish pass 2 (label: integrate2)

Branch `work/finish2-int`, started from main d74aed0. It merges the five finish-pass-2 branches, installed matches first. Two C replacements are added (08002854 and 0800421C); none is removed. Every build, measurement and check ran on worker A; the laptop only edited files and resolved merges. No push and no merge into main.

## Merge order and result

| Branch | Commit | Result |
| --- | --- | --- |
| finish2-stream | e9e4a24 | Clean. Installs `func_08002854` (6,456 bytes, covers 08003786), `tools/asm_interfaces.py` reclassification, `tests/test_match4.py` assertion. |
| finish2-hud | 951fd9a | Conflicts in `tools/rom.cfg`, `README.md`, `docs/FINISH.md`, `docs/map/finish.json` and `progress.json`. `rom.cfg` keeps both match entries (`func_08002854`, then `func_0800421C`). README and `FINISH.md` are rewritten to the combined state. The two generated files took the stream side and were then regenerated (below). `hand_matches_added` is 85 (83 on main, plus one per hand install, as earlier single installs did). |
| finish2-renderer | 5e77e8b | Clean (round note, candidates, search tools and receipts). |
| finish2-contact | 1ff9e6f, 06882f2 | Clean (round note, candidate, loop-pass tables, search and dump tools). |
| finish2-sound | f0825df | Clean (round note, candidate, search tools and differential check). |

Bookkeeping added in the HUD merge, mirroring what the stream lane did for its owner: the stale `0x0800421C` `C-candidate` row and its `OWNER_END` extent are removed from `tools/asm_interfaces.py`. They no longer affected any output, because installed entries are skipped before classification. The stale 080051FE fragment row is left alone; that label has not been an entry since 11/14.

`asm/program.s` merged automatically. The tree `make` regenerated on worker A differs from the auto-merge only in where one `.thumb` directive sits (now just before `func_080064A4`, the first owner still listed as assembly), so the regenerated file is committed (sha256 `647acfa0…`). `docs/map/finish.json` (`f35199a0…`) and `progress.json` (`85f29774…`) were regenerated on worker A and copied back. All three are metadata or listing text with no ROM bytes.

## Totals, main → integrated

| | main (d74aed0) | work/finish2-int |
| --- | ---: | ---: |
| Registry entries | 228 | 228 |
| Exact C replacements | 189 (73,162 bytes with pools, 85.5%) | **191** (83,742 bytes with pools, 97.9%) |
| `completion`: complete entries | 222 of 228 | **225 of 228** (191 exact C + 3 covered labels + 31 assembly) |
| Covered labels | 2 (0800D570, 0800D630) | 3 (+08003786) |
| Instruction bytes inside exact owners | 60,234 (70.4%) | **70,192 (82.0%)** |
| Documented assembly | 6,092 (7.1%) | 6,092 (7.1%) |
| Remaining C owners | 5 + 08003786 continuation: 19,252 instruction bytes, 20,380 with pools | **3**: 9,294 instruction bytes (10.9%), 9,800 with pools |

Instruction-byte figures are the mapped code blocks of `tools/rom.cfg` inside each owner's extent including pools; the same calculation reproduces the 11/14 total of 19,252.

## Remaining owners, re-measured on the integrated tree (worker A)

`tools/measure_candidate.py` on each lane's best near-miss gives the same bytes and compiled hashes as the lane receipts:

| Owner | Profile | Differing bytes (11/14 → 11/15) | Output / target | Frame | Instruction edits | Compiled sha256 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 080064A4 sound | old | 3,227 → **1,598** | 3,820 / 3,828 | 100 / 108 | 283 | 9320af76… |
| 08016DA8 renderer | arm | 2,446 → **880** | 4,288 / 4,288 | 96 / 96 | 367 | 762d5807… |
| 080181C0 contact | arm | 919 → **158** | 1,684 / 1,684 | 72 / 72 | 74 | d9a63955… |

None of these candidates is installed.

## Validation (worker A, final merged tree)

- `make clean; make -j8`: 191 `C match` lines, including `func_08002854: C match (6456 bytes)` and `func_0800421C: C match (4124 bytes)`; `build/txra.gba: OK`; SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- `make recomp`: `Emitted 228 functions, 258 load/run entries`.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed`, with `fallback=0 unknown=0 unsupported=0`.
- `tools/map_completeness.py`: 7 closure notes, 11 flagged unknown spans and 1 rejected odd pointer, the same as 11/14.
- `tools/asm_interfaces.py --completeness`: classes assembly-interface 31, covered-by-installed-owner 3, C-candidate 3; 0 verification failures. `finish.json` is byte-identical on a second run.
- `tools/progress.py`: `completion` 225 of 228, `remaining_c_owners` 080064A4, 08016DA8, 080181C0, `remaining_c_owner_bytes_including_pools` 9,800.
- `tools/rom_map.py --refine-diff`: 0 removed, 0 added.

README and the `docs/FINISH.md` verdict, definition-of-done and tracker rows are updated to these numbers.

matches installed: 08002854 (stream owner, 6,456 bytes; covers 08003786) and 0800421C (HUD owner, 4,124 bytes), both from their lanes; exact C 189 -> 191, completion 222 -> 225 of 228
near-misses improved: 080064A4: 3227 -> 1598; 08016DA8: 2446 -> 880; 080181C0: 919 -> 158 (lane results, re-measured identical on the integrated tree)
what blocks the rest: register allocation in all three remaining owners: the sound owner's spilled 0x67 master-volume temporary (frame 100 vs 108, which shifts everything after 08006DC4), the renderer's global-allocation order at 08016E44 cascading through reload's round-robin choice, and the contact owner's strength-reduced pointer losing the priority race to k
