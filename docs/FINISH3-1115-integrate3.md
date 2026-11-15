# 15 November: integration of finish pass 3 (label: integrate3)

Branch `work/finish3-int`, started from main fa8decd. It merges the three finish-pass-3 branches, installed match first. One C replacement is added (080181C0); none is removed. Every build, measurement and check ran on worker A; the laptop only edited files and resolved merges. No push and no merge into main.

Main had moved past the finish-pass-2 integration (77ab890) that the three lanes branched from. Its seven newer commits come from the local model loop: unreviewed entries in `docs/map/name-proposals.json`, the `llm_attempts`/`llm_requests` counters in `progress.json`, a rewritten footer line in the README progress block, and `tools/rom.cfg` re-serialised with the whole `matches` list on one line. The registry is semantically unchanged by them (same 191 entries, same fields), and no source, listing or map file changed.

## Merge order and result

| Branch | Commits | Result |
| --- | --- | --- |
| finish3-contact | 033dd85, 2a76636 | Conflicts in `tools/rom.cfg` and `README.md`. `rom.cfg` keeps main's one-line `matches` list and appends the `func_080181C0` entry (offset 98752, size 1684, `src/generated/func_080181C0.c`, compiler `arm`); the result parses to exactly the contact branch's registry. The README progress footer takes the contact side (instruction-byte breakdown). Everything else merged automatically: the installed source, the `tools/asm_interfaces.py` removal of the 080181C0 `C-candidate` row and `OWNER_END` extent, `asm/program.s`, `docs/map/finish.json`, `progress.json` (with main's model-loop counters kept), `docs/FINISH.md`, the round note, receipts and diagnostic tools. |
| finish3-renderer | e82d434 | Clean (round note, two search candidates, source-fact candidates, ARM trace-compiler patches, search tools and receipts; docs only). |
| finish3-sound | 085e7ed .. e83c524 (6) | Clean (round note, near-miss and receipts, debug-build patches, templates and search tools; docs only). |

`hand_matches_added` is now 86 (85 on main, plus one for the contact install, as earlier single installs did). The committed diff listings (`near-misses/finish3-1115-sound/candidate.diff.txt`, `finish3-1115/renderer/receipts/bytes.diff.txt.gz`) are disassembly text with literal-pool words replaced by `<literal pool>`, like earlier rounds' listings.

`make` on worker A regenerates `asm/program.s` byte-identical to the merged file (sha256 `4c3bb82f…`). `docs/map/finish.json` (`ad3a4944…`) and `progress.json` (`4d2b2e9f…`) regenerate byte-identical to the committed files, so nothing had to be copied back.

## Totals, main → integrated

| | main (fa8decd) | work/finish3-int |
| --- | ---: | ---: |
| Registry entries | 228 | 228 |
| Exact C replacements | 191 (83,742 bytes with pools, 97.9%) | **192** (85,426 bytes with pools, 99.8%) |
| `completion`: complete entries | 225 of 228 | **226 of 228** (192 exact C + 3 covered labels + 31 assembly) |
| Instruction bytes inside exact owners | 70,192 (82.0%) | **71,804 (83.9%)** |
| Documented assembly | 6,092 (7.1%) | 6,092 (7.1%) |
| Remaining C owners | 3: 9,294 instruction bytes (10.9%), 9,800 with pools | **2**: 7,682 instruction bytes (9.0%), 8,116 with pools |

Instruction-byte figures are the mapped code blocks of `tools/rom.cfg` inside each owner's extent including pools (080064A4 3,470, 08016DA8 4,212; 080181C0 had 1,612).

## Remaining owners, re-measured on the integrated tree (worker A)

`tools/measure_candidate.py` on each lane's best near-miss gives the same bytes and compiled hashes as the lane receipts:

| Owner | Profile | Differing bytes (finish2 → finish3) | Output / target | Frame | Instruction edits | Compiled sha256 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 080064A4 sound | old | 1,598 → **159** | 3,828 / 3,828 | 108 / 108 | 134 | 444d6222… |
| 08016DA8 renderer, search B (fewest bytes) | arm | 880 → **863** | 4,288 / 4,288 | 96 / 96 | 381 | aeb94184… |
| 08016DA8 renderer, search A (lowest distance) | arm | 1,091 | 4,288 / 4,288 | 96 / 96 | 367 → **322** | 2c955554… |

Neither candidate is installed. The sound measurement reports compiler sha256 `90bdd572…` on worker A where the lane receipt from worker B has `b3f3f967…`; the two hosts carry separately built copies of the old compiler, and the compiled output is identical.

The installed contact source measures `"exact": true`, `"different_bytes": 0`, `"instruction_distance": 0`, 1,684 / 1,684 bytes, frame 72, compiled sha256 `960f722b…`, the same as the lane receipt.

## Validation (worker A, final merged tree)

- `make clean; make -j8`: 192 `C match` lines, including `func_080181C0: C match (1684 bytes)`; `build/txra.gba: OK`; SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`. Run again after the documentation edits, with the same result.
- `make recomp`: `Emitted 228 functions, 258 load/run entries`.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`: `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed`, with `fallback=0 unknown=0 unsupported=0`.
- `tools/map_completeness.py`: 7 closure notes, 11 flagged unknown spans and 1 rejected odd pointer, unchanged.
- `tools/asm_interfaces.py --completeness`: classes assembly-interface 31, covered-by-installed-owner 3, C-candidate 2; `"failures": []`. `finish.json` is byte-identical on a second run.
- `tools/progress.py`: `completion` 226 of 228, `remaining_c_owners` 080064A4, 08016DA8, `remaining_c_owner_bytes_including_pools` 8,116; `functions_matched_c` 192 functions, 85,426 bytes with pools.
- `tools/rom_map.py --refine-diff`: 0 removed, 0 added.

README and the `docs/FINISH.md` verdict and tracker rows are updated to these numbers. The worker copy and logs on worker A were removed afterwards.

matches installed: 080181C0 (contact owner, 1,684 bytes, ARM profile, from its lane); exact C 191 -> 192, completion 225 -> 226 of 228
near-misses improved: 080064A4: 1598 -> 159 (length and frame now match); 08016DA8: 880 -> 863 (instruction distance 367 -> 322 in a second candidate); 080181C0: 158 -> 0 (installed)
what blocks the rest: register allocation order only. In 080064A4 the envelope pointers lose r2 to the slide/noise temporaries (97 rows) and the effect-loop and mix-buffer registers are rotated (34 rows); in 08016DA8 the face header needs &pts[d] and &pts[c] allocated before depth[1], the part blocks' midpoint chain must win a priority tie, and the projection loop's pre-store schedule is open
