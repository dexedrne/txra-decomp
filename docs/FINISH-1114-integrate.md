# 14 November: integration of the finish round (label: integrate)

Branch `work/finish-int`, started from main a184d37. That is 62841be plus one PC-runtime overlay commit, which touches no matching file. It merges the nine finish branches. No C replacement was added or removed. Every build and check ran on worker A; the editing machine only edited files.

## Merge order and result

| Branch | Commit | Result |
| --- | --- | --- |
| finish-classify | b140345 | Clean. Brings in map audit, assembly classes, `completion` block and the alignment/pointer-slot data labels. |
| (no branch installed a match) | | |
| finish-hud | 38a80e4 | `progress.json` conflict only (counts; regenerated). |
| finish-mixer | 5649942 | Conflicts in `tools/rom.cfg` (union of `far_jumps`: HUD's 1 plus mixer's 7), `tests/test_match3.py` (all six labels asserted as neither candidate nor skipped), `tests/test_match4.py` (080001F4 as the stable blocked entry; 08007368 and 080051FE absent), `docs/asm-only.md` (both repaired rows kept), README, `progress.json`. |
| finish-small | d916c0c | `rom.cfg` union (+3 `far_jumps`, 11 in all), both metadata tests kept, both asm-only sections kept, README, `progress.json`. |
| finish-b40 | 42c7384 | `rom.cfg`: `interior_labels` added next to `far_jumps`. Both metadata tests and doc sections kept, `progress.json`. |
| finish-d630 | bb4e612 | Clean. One follow-up commit: its ranking test expected 0800D960 as a covered entry, but small folded that label. The test now expects 0800D570/0800D630 as covered, and 0800D960, 08007B40 and 080095C4 as absent. |
| finish-contact | c145921 | Clean (round note, diagnostic source and receipts). |
| finish-renderer | 91c3979 | Clean (round note, candidates and receipts). |
| finish-stream | f20e8e1 | Clean (round note, candidate and receipts). |

The generated files that git merged automatically (`asm/program.s`, `docs/map/functions.json` and the other `asm/` and `docs/map/` inventory files) are byte-identical to what `make` regenerates on worker A from the merged `tools/rom.cfg`. `docs/map/finish.json` and `progress.json` were regenerated there and copied back. They are metadata only, with no ROM bytes.

## Totals, main → integrated

| | main (62841be / a184d37) | work/finish-int |
| --- | ---: | ---: |
| Registry entries | 237 | **228** |
| Exact C replacements | 189 (73,162 bytes with pools) | 189 (73,162) |
| Mapped code bytes | 85,578 | 85,578 |
| Unknown ROM bytes | 719,822 | **719,264** |
| `completion`: complete entries | (not reported) | **222 of 228** (189 exact C + 2 covered labels + 31 assembly) |
| Remaining entries | 48 without own C | **6** (5 C owners + 08003786) |
| Remaining instruction bytes | 19,252 | 19,252 (22.5%) |
| Native recompiler | 237 functions / 268 load-run | 228 / 258 |

In instruction bytes, exact C holds 60,234 (70.4%) and documented assembly 6,092 (7.1%). The README's 85.5% (73,162 / 85,578) divides bytes that include pools by bytes that do not. The README now states both figures.

Best retained candidates, none installed:

| Owner | Before | After |
| --- | ---: | ---: |
| 08002854 | 6,106 | 23 |
| 08016DA8 | 3,250 | 2,446 |
| 0800421C | 3,144 | 3,144 |
| 080064A4 | 3,227 | 3,227 |
| 080181C0 | 919 | 919 |

The stream and renderer figures were re-measured on worker A with the unchanged `tools/measure_candidate.py`. The stream gives 6,456/6,456 bytes, frame 268, 20 edits, 23 differing bytes and compiled sha256 3ea219ef…. The renderer gives 4,288/4,288 bytes, frame 96, 622 edits, 2,446 differing bytes and compiled sha256 7a58e6f0…. Both compiled hashes equal the lane receipts.

## Validation on worker A (final tree)

- `make clean; make -j8`: 189 `C match` lines, `build/txra.gba: OK`. SHA-1 4197339d4add74bb40ed02a8fba5e58096afb487.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- `make recomp`: `Emitted 228 functions, 258 load/run entries`.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `4300 framebuffer hashes, every PCM byte, final state and sample clock passed`. Also `fallback=0 unknown=0 unsupported=0`.
- `tools/map_completeness.py` on the merged map gives the same 7 closure notes, 11 flagged unknown spans and 1 rejected odd pointer as the classify run. Its 12 BLs landing on internal instructions are exactly the 11 reviewed `far_jumps` plus the 080083BA interior-label goto. `rom_map.py --refine-diff` reports 0 changes. `tools/asm_interfaces.py` reports 0 verification failures, and `finish.json` reproduces byte-for-byte on a second run.
- The remote copy `~/txra-integrate` was removed afterwards.

## Left as is

- 0800D570, 0800D630 (inside installed func_0800D51C) and 08003786 (inside 08002854) are still registry entries. Folding them with reviewed `far_jumps` would change only the entry count.
- `docs/map/code-audit.json` was already stale on main and was not regenerated.
- The four 14-byte startup/libgcc entries counted as exact C (08000000, 08018E18, 08018E80, 08018E88) are unchanged.

matches installed: none (189 exact replacements survive the merge; registry 237 -> 228 by folding nine long-branch labels)
near-misses improved: 08002854: 6106 -> 23; 08016DA8: 3250 -> 2446 (both re-measured on worker A; 0800421C 3144, 080064A4 3227, 080181C0 919 unchanged)
what blocks the rest: five complete C owners remain uninstalled. The stream owner needs one block's register allocation (23 bytes), the renderer a register swap plus scheduling, and the HUD, sound and contact owners whole-function allocation, frame or loop-optimization structure that local edits have not reproduced.
