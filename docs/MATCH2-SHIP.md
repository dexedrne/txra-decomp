Thirty additional functions now rebuild from ordinary C. The total is **25 → 55 functions** and **582 → 2,388 bytes**, a gain of **1,806 bytes**. Approximate matched mapped-code share rises from **0.684% to 2.805%**; literal pools and in-function alignment are included in matched spans. The mapped function inventory and 85,132-byte instruction denominator are unchanged.

Implementation commit: `394812a` — thirty replacements, relocation checks, shared diff feedback, ten curated examples, layout guesses, progress bookkeeping, documentation and review renderer. This note and `MATCH2-DONE` are in the following handoff commit, titled “Record matching verification and review evidence”. Nothing was pushed, deployed or merged.

The shared relocation path already existed at the start; the old document incorrectly said all relocations were rejected. Trials and installed replacements now use tested address-named globals and function declarations. Known literals supply provisional `g_XXXXXXXX` names, existing `gUnk_XXXXXXXX` names remain accepted, and BL addends and invalid offsets/encodings are checked. Separate unsupported data sections and unresolved symbols still fail validation. The matching loop tries callers whose direct callees are matched before other candidates in the same relevance group, then sorts by size.

`tools/diffhint.py` prints a bounded target/compiled instruction diff, including register changes, constants, length and labelled pool words. Retries receive both the previous C and this diff. Comparisons cover the complete mapped extent instead of accepting a prefix. Compiler `.size` boundaries exclude incidental section padding after a function; genuine instruction/pool/alignment bytes are compared unchanged. The ten C-plus-note examples in `tools/fewshot/` are loaded into prompts and all ten independently recompile to their installed spans in tests. Updating the match list preserves the existing mapping table's formatting.

Hand work started with the smallest complete routines, then moved through array access, signed-width operations, loops and callers. The additions include five indirect ROM-pointer wrappers, bounds-checked stores, two table transforms, global slot clearing/swapping, byte copying, key polling, transfer setup, EEPROM comparison and a caller with a signature check. The two transforms use the three-word layout in `src/types.h`. Larger-record fields retain offset names; no speculative game-specific field meanings were added. Every installed source is ordinary C, with no inline assembly or injected instruction data.

Validation:

- Each of the thirty installations passed its compiler byte comparison and a forced full rebuild with the ROM SHA-1 check.
- Final `make check`: **102 tests passed**, including **12 new tests** for diffs, pool rendering, full extents, previous-source retries, declarations, candidate order, BL addends, rejected names/offsets, configuration formatting, function boundaries and the ten compiled examples.
- Final `make` ends in **`build/txra.gba: OK`**. A separate full-file `cmp` of the private ROM and rebuilt ROM also passed.
- Historical request/attempt statistics are retained; the thirty hand matches have a separate progress key. No service requests were made for this work, and the separately managed service checkout was neither edited nor stopped. Its success rate after this change remains unmeasured.
- Mapping metadata outside `matches` is unchanged. No runtime or save-format source was changed. No ROM, extracted assets, compiled binary or raw ROM data was committed.

Review folder: `txra-review/match2/`.

- `before/matching-status.png` and `after/matching-status.png`: the same view, showing function counts, matched byte totals and approximate mapped-code share.
- `matched-percent.png`: each accepted replacement in work order. This is an acceptance-milestone chart, not a wall-clock timing benchmark.
- `matched-bytes.png`: 582 versus 2,388 bytes with the exact gain printed.
- `matching-progress.webm`: six seconds, 30 fps, muted VP9, **378,532 bytes**. The stream listing contains video only. The start, middle and final frames were inspected, along with every PNG; all labels fit and the totals agree.
- Root and both picture subfolders have `NOTES.md` and complete `captions.json`. The clip and pictures show only our metadata tools. No browser or gameplay recording was needed for these matching-tool changes.

Remaining work: **174 mapped functions remain unmatched**. Some tiny map entries are shared epilogues or fragments rather than established standalone compiler units; they were deliberately not counted as new matches. Larger callers, compiler/register-allocation differences, stack-heavy routines and unsupported separate data sections still need work. Two retry-loop variants and an angle-difference routine tried during this pass still differ and were not installed. The progress percentage is approximate, typed layouts are provisional, and gameplay/native execution milestones were not rerun in this matching-only pass. No picture defects remain known.

Owner-note check: `OWNER-NOTES.md` was absent at the initial, intermediate and final reads. There were no appended owner notes to act on or leave unresolved. Review/video notes were fulfilled with four inspected pictures, the muted clip, notes and captions. No vehicle, world, road or original-model work was involved. The completion markers are `MATCH2-DONE` in the repository and `DONE` in the review folder.
