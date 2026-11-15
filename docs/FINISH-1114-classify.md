# 14 November: map completeness and classification (label: classify)

This branch, `work/finish-classify`, started from main 62841be. It answers whether the function map is complete and classifies every entry that has no exact C. It changes no C source and no match record. All builds, audits and tests ran on a worker with the private ROM; the editing machine only edited files.

## Results

- **Map verdict: complete. The finish line stays at 237 entries.** Evidence is in [FINISH.md](FINISH.md) and `docs/finish-1114/completeness.json.gz`. In summary:
  - Every direct, literal and resolved indirect transfer from the 37,704 mapped instructions lands on mapped code.
  - The 11 "unresolved" indirect sites are dead libgcc veneers with no reference.
  - The pointer scans of all non-code bytes at every alignment yield one validator pass, which is a coincidence: one unaligned reference from inside PCM audio.
  - The 719,264 unknown bytes hold 0 Thumb BL-to-entry pairs, 0 Thumb returns, 0 ARM branches to known code and 0 ARM returns. In mapped Thumb code the same measures are 1,069 BL-to-entry pairs and 184 returns.
- **Data classified.**
  - 546 bytes become `fill / alignment-halfword`: the 273 aligners, which were the last unknown bytes in 08000000–08018EC4.
  - 12 bytes become `table / code-entry-pointer-array`: three slots of the const function-pointer table at 080200C4.
  - Unknown bytes go **719,822 → 719,264**. The rule lives in `tools/rom_map.py` and is reproducible with `--refine-diff`. `docs/map/coverage.json` totals are updated to match.
- **Classification of the 48 entries without their own C** (`docs/map/finish.json`, re-measured by `tools/asm_interfaces.py`):

  | Class | Entries | Mapped instruction bytes |
  | --- | ---: | ---: |
  | Documented assembly interfaces | 31 | 6,092 |
  | Labels inside installed exact owners | 5 | (already counted with their owners) |
  | C owners | 5 | 19,252, including their fragments |
  | Fragments installing with those owners | 7 | (included above) |

  None of the 48 is data misclassified as code.
- **Progress.** `progress.json` keeps every existing key and value except the data and unknown totals. It gains a `completion` block: **225 of 237 complete** (189 exact C, 5 covered labels, 31 assembly interfaces), 12 remaining, and 11 unresolved indirect sites that are unreferenced. Assembly is never counted as C.
- **New tools.**
  - `tools/map_completeness.py`: closure, reference scans, code-likeness, entry reachability.
  - `tools/asm_interfaces.py`: re-measures the reviewed classes.
  - `rom_map.refine_unknown_mask` / `--refine-diff`.
  - `progress.completion`.
  - Synthetic tests in `tests/test_finish_tools.py`, `tests/test_mapping.py` and `tests/test_progress.py`.
- **Validation on the worker.**
  - `make check` passed: 271 tests, 1 existing skip, 0 failures. All 189 installed replacements rebuilt, and the full ROM SHA-1 4197339d4add74bb40ed02a8fba5e58096afb487 is unchanged.
  - The regenerated inventory (asm/, docs/map/*.json) is byte-identical to the committed copy.
  - `make recomp` emitted 237 functions / 268 load-run entries.
- **Flagged, not changed.** 08000000, 08018E18, 08018E80 and 08018E88 (14 bytes) are installed as byte-identical C, although they are startup and libgcc assembly in origin. The README's 85.5% mixes bytes including pools with instruction bytes. In instruction bytes, exact owners hold 70.4%, assembly interfaces 7.1%, and the remaining owners 22.5%.

matches installed: none (this was a classification pass; 189 exact replacements unchanged)
near-misses improved: none (best retained: 08002854 6,106; 0800421C 3,144; 080064A4 3,227; 08016DA8 3,250; 080181C0 919)
what blocks the rest: only the five large C owners remain, each still hundreds to thousands of differing bytes from exact, because of register allocation, frame layout and fragment structure; no further function or unknown-byte code is expected to appear.
