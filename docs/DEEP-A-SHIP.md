# TXRA deep hand matching — slice a

Seven complete C replacements increased accepted matching from **109 functions / 10,698 bytes / 12.566%** to **116 functions / 14,022 bytes / 16.471%**. The mapped-code denominator remains 85,132 bytes. Each replacement passed an uncached comparison through its full literal-pool extent, the next-entry boundary gate, a forced full rebuild, and whole-ROM byte comparison. No approximate draft was installed.

| Commit | Entry | Full bytes | Source lesson |
|---|---|---:|---|
| fc79512 | 080164D0 | 236 | Nest fixed-point shifts in their producing expressions and reuse vector temporaries. |
| 45b1fb0 | 08017E68 | 252 | Use the existing ARM compiler, descending queue index and ordered callback branches. |
| 8df482c | 0801533C | 368 | Recover five real stack arguments, preserve palette-base lifetime and reuse the search index. |
| 18b646c | 0800C9C4 | 408 | Name signed record offset 24 and preserve direct indexed field addressing. |
| f36467a | 0800237C | 386 | Duplicate octant assignments and create the high-octant comparison after the first loop. |
| bf10207 | 08018854 | 512 | Preserve distinct extern start/end identities even where their addresses coincide. |
| 2c590dd | 080157A0 | 1,162 | Recover the 224-entry switch; reuse the narrowed byte offset in each range result. |

Commit `6c80ea9` updates the existing switch-target integration check to verify targets inside a compiled replacement as well as assembly entries. The new character switch exposed its earlier assembly-comment assumption. This keeps all fourteen switch tables checked, including the actual compiled target bytes and included replacement extent.

The explicit ARM profile uses the pinned compiler's ARM source, built as `agbcc_arm` by the setup script in an isolated source copy. Both the normal matching build and the trial judge use it. Valid aligned `R_ARM_V4BX` markers leave existing BX instructions unchanged; malformed markers and unknown relocations are rejected. The existing five THUMB search profiles are unchanged. The shared record remains 100 bytes after naming its signed word at offset 24.

## Validation

- Final `make -j4 check`: **148 tests passed**, including five new ARM marker/compiler/boundary tests.
- Every accepted match received its own forced full rebuild. Final `make -j4` prints `build/txra.gba: OK`; final `cmp` succeeds.
- ROM SHA-1 remains `4197339d4add74bb40ed02a8fba5e58096afb487`.
- An independently rebuilt ARM compiler reproduced the first ARM match using the documented setup recipe.
- All seven additions belong to the frozen slice-a assignment; all baseline matches are retained. No sibling slice entries or mapping boundaries changed.
- `git diff --check` passes. Compiler work used nice 15 and at most four cores. The separate matching service was not contacted.

The ROM was initially missing from this checkout; the required gitignored symlink to `../txra-baserom/baserom.gba` restored the private input. No ROM, extracted binary, generated compiler output or review imagery is committed.

## Review handoff

The review folder is `txra-review/deep-a/`. It contains the running forty-entry [outcome table](deep-a/outcomes.md), frozen assignment, source hypotheses, side-by-side text diffs, compiler-profile evidence, pictures and clip. Every picture/clip folder has plain `NOTES.md` and complete `captions.json`.

| Review item | What to inspect |
|---|---|
| before/status.png | Initial exact replacements and fixed-denominator coverage. |
| after/status.png | Same view after seven accepted replacements. |
| results.png | The seven recovered routines and their complete byte counts. |
| matching-progress.webm | Six-second metadata replay, VP9, 1440 × 1000, 30 fps, no audio, 452,462 bytes. |

All three review pictures and the clip's midpoint frame were opened and inspected. Text fits and the before/after framing is identical. The clip is explicitly labeled compiler metadata. It is not game footage. There were no new moving gameplay features, vehicle, world or traffic changes to capture.

`tools/review_deepa.py` reproduces the pictures and clip from the retained baseline and current progress. The root marker is `DEEP-A-DONE`.

## Unfinished work and owner notes

All forty assigned entries have a decision in [outcomes.md](deep-a/outcomes.md): seven exact matches, eleven assembly/BIOS interfaces, six shared-frame or incomplete entries, fifteen unmatched complete C drafts, and one partial C recovery. Assembly decisions and boundary evidence are recorded in [asm-only.md](asm-only.md). The fifteen retained [candidate sources](deep-a/candidates) are speculative, excluded from the build and not validated as behavior-correct.

The closest remaining queue, decimal and billboard drafts still have register-lifetime differences. The complete boot/menu initializer still differs in loop scheduling and signed cursor handling. The largest ARM function, 08016DA8, has only partial semantic recovery: its full near-field subdivision and projection body has no complete new candidate. Its lifted draft mislabels MLA and drops shift parentheses; this is a draft presentation limitation, not evidence of a runtime failure. The isolated O1/O2/Os rotation probes establish the ordinary C multiply-accumulate idiom without claiming a function match. Shared-frame entries need coordinated enclosing-function recovery rather than changes across sibling slice boundaries.

A report that the native build did not seem to run was open at the time. This pass recovers exact code and does **not** resolve or verify that runtime issue. Boot, title, playable race and save milestones remain false in `progress.json`; no gameplay success or visual game improvement is claimed. `OWNER-NOTES.md` was absent when checked throughout the work and at final review, so no additional live owner notes were available.

No push, deployment, merge, stash or changes to the separate model loop were performed.
