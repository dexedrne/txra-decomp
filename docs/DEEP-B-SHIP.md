# TXRA slice b hand recovery

Three complete C replacements add **1,830 bytes**, taking the total from
**109 functions / 10,698 bytes / 12.566%** to
**112 functions / 12,528 bytes / 14.716%** of the unchanged 85,132 mapped bytes.
Every addition passed an uncached complete-function comparison, a forced full
rebuild, `build/txra.gba: OK`, and whole-ROM byte identity. No partial function,
assembly wrapper, patched output or supplied instruction words count as C.

## Accepted commits

| Commit | Complete replacement | Why it matched |
| --- | --- | --- |
| 270c17c | 08018E1C, 94 bytes | Ordinary library copy loops require `-mno-thumb-interwork` for the original return. The narrow `old-no-interwork` profile is supported by judging and full builds. |
| 9c851f1 | 08002500, 632 bytes | Native switch with 94 entries; typed slot field and separate byte load/decrement preserve the address and register shape. Includes final literal pools. |
| da91d4f | 08012600, 1,104 bytes | Native switches, typed slot fields, independent updates and shared C labels reproduce the 105-entry table and merged tails. Includes all calls and pools. |

The final handoff commit contains this note, the switch-target test correction,
new accepted corpus examples, frozen target list, all 40 outcomes, five unfinished
C seeds and assembly/boundary classifications. No push, merge, deploy or stash
was performed. All commits use the requested owner identity without trailers.

## Validation

- Full `make -j4 check`: **145 tests passed**. An initial run found one stale
  test assumption: switch targets were required to appear as assembly comments.
  The corrected check verifies a matched target's emitted inclusion and its
  complete compiled bytes instead; unmatched targets retain the assembly check.
- Focused corpus/relocation suite after adding both accepted examples:
  **12 tests passed**. The focused compiler/workflow suite passed **10 tests**
  after the third installation; these are included in the full-suite count.
- Both dispatchers also match in either order in one compilation unit with a
  compatible shared slot definition: **4 exact comparisons**. Separate source
  files remain in the matching build.
- The ROM is byte-identical, with the existing SHA-1
  `4197339d4add74bb40ed02a8fba5e58096afb487`. All **112** installed bodies pass
  the build's complete-byte verification.
- The work used sequential compiler trials and at most four cores at nice 15
  or lower scheduling priority. Encoding used two threads. No browser, other
  machine or separately running matcher was used.

## Review folder

`txra-review/deep-b/` contains the running outcome table and the
inspected review media. Every media folder has plain owner notes and captions.
The five pictures use the same before/after summary view and acceptance history:

- `before/matching-status.png` and `after/matching-status.png`: 109 to 112
  complete functions; 10,698 to 12,528 matched bytes.
- `matched-functions.png`, `matched-bytes.png`, `matched-percent.png`: the three
  accepted commits at their commit times, with fixed mapped-byte denominator.
- `matching-progress.webm`: **6 seconds, 30 fps, 180 frames, 300,416 bytes,
  no audio**. It walks through the accepted counts. Full decoding and input
  stream metadata were checked; beginning, middle and final frames were viewed.

These pictures and the clip describe source-recovery progress. Gameplay was not
captured or changed. Vehicle, driving, weather and original-model work did not
apply. No private ROM images, binary extracts or generated compiler artifacts
were committed. The actual review media remain in the requested review folder.

## Per-function outcome and remaining work

Selection was frozen at 7b37a3e, sorting all 120 unmatched entries by mapped
extent size and address, then taking zero-based offset 1 with stride 3. The
40-entry manifest is `docs/deep-b/targets.json`. Do not rerank after each match,
since that changes ownership. `docs/deep-b/OUTCOMES.md` and the review folder
record every entry and what was learned. Other slices' source was not edited.

Three entries matched. Of the remaining 37, ten are preserved assembly contracts
or the strongly suspected assembly division helper; two have unresolved high
register live-ins; six need enclosing frames or corrected complete boundaries;
and nineteen remain ordinary C candidates, including two ARM compiler routines.
These are classifications, not nineteen additional matches or verified rewrites.

`docs/asm-only.md` distinguishes those categories. In particular, 08008A88 omits
its epilogue at 080095C4, and 08002854 continues beyond its mapped end through
0800417E. Their complete units require coordinated ownership. ARM routines
08016C18 and 080165BC have compiler frames and were tested with the historical
ARM compiler at O2/O1/Os; neither is an installed replacement.

`docs/deep-b/README.md` explains retained source hazards and the next hypotheses:
truncated pointers, missing stack call arguments, omitted division operands,
lost DMA volatility, incorrect glyph shift pairs and omitted ARM MLA operations.
Five retained C seeds compile but remain excluded from the build. Large
register-style drafts still need native variables, real record access and
structured control flow. The image loop and link routine remain unmatched;
restoring the correct byte count alone with wrong shifts is not a solution.

## Owner notes and execution concern

`OWNER-NOTES.md` was absent at startup, major steps and the final read; no appended
notes were available to apply or leave unaddressed. The brief's matching-progress
concern is answered by three new complete replacements. The comment that TXRA
“doesn't seem running” is **not resolved as a desktop runtime issue**: no new
boot, title, playability, race or save milestone was verified. Existing execution
flags remain unverified; the separate matching process was neither contacted nor
modified. The rebuild's byte identity preserves the original ROM behavior.

`DEEP-B-DONE` in the repository and `DONE` in the review folder mark this handoff,
not completion of the full decompilation or a gameplay fix.

Matched before/after: 109 / 112.
Percent before/after: 12.566% / 14.716%.
Next: recover native records and real switches before tuning register-style drafts; check library return flags separately.

# Independent deep-b handoff

Both original handoffs are retained here. Their totals describe separate
historical baselines; current combined totals are in DECOMP.md. The copy
routine is shared and counted once.

# TXRA deep hand matching — slice b

The build now has **110 exact C replacements / 10,792 bytes / 12.677%** of
85,132 mapped code bytes. The baseline was **109 / 10,698 / 12.566%**.
The new replacement is the complete **94-byte copy routine at 08018E1C**.
Its source follows the bundled library implementation. `old_agbcc -O2` without
Thumb interworking reproduces every byte, including its direct return through pc.
The normal application profile adds a different return sequence. The explicit
`old-no-interwork` profile is used by both trial judging and the matching build.

All forty assigned entries have an outcome in [the running log](deep-b/LOG.md).
The assignment was frozen from the initial unmatched ranking, sorted by
`(bytes, address)`, then sliced at zero-based offset 1 with step 3. The frozen
[manifest](deep-b/slice.json) prevents repartitioning after a new match changes
the unmatched list. No function belonging to another slice was modified.

The remaining outcomes are **22 unmatched C bodies**, **7 ABI/boundary recovery
entries**, and **10 assembly entries/veneers or probable private renderer
routines**. These are decisions with differing confidence, not thirty-nine
failed exact installations. [asm-only.md](asm-only.md) distinguishes genuine
register veneers from uncertain private ABIs and incomplete function boundaries.
No prefix or approximate C was installed.

## Source findings

- The closest blit remains a six-token / ten-byte miss: height and destination
  exchange r8/r9, and the inner count moves before source setup. Initializer
  ordering, register hints, widths, typed bases, inline compositor shapes,
  compiler policies and compilation-unit ordering did not resolve it.
- The link-state family now has compilable typed source hypotheses. Switch
  fallthrough, record bases and separate induction variables matter more than
  further blind variants. The packet-state draft improves to 35/163 while keeping
  full-width pointers and parameters. Older search drafts sometimes narrowed
  addresses; those mutations are not trusted source reconstructions.
- Repeated DMA fills expose source scopes and volatile storage that the lifted
  stack slots hide. Some other slots are outgoing stack arguments. The setup
  siblings improved after reconstructing these patterns, but none is exact.
- The 310-byte strip routine has the correct length under old `-O1`, with a
  retained 36/40 miss. Most remaining differences are coordinate and high-register
  allocation. Equal lengths alone are not evidence of equality.
- Bounded dispatchers at 08002500, 08012600 and 08008A88 are ordinary C candidates.
  Their missing computed-entry labels and switches were reconstructed before
  compiling. Ranking rejection was not treated as proof of handwritten assembly.
- The pinned ARM backend was built locally with at most three build workers.
  The smaller transform emits the correct 400-byte length and compiler-style
  frame, but still differs. The larger ARM primitive emitter was made compilable
  after recovering sixteen frame words and multiply-add operations. Neither was
  installed as a replacement or added as an accepted build profile.
- 08007B40 falls through from its preceding entry without a new prologue.
  08002854 reaches balanced code through 0800417E, beyond its mapped end
  08003786. Neither mapped prefix is an independently acceptable C function.

Scores above are instruction-token edit distance / byte distance. Switch tables
can be decoded as instructions by that heuristic, so their token scores are
particularly weak. Every installation still requires complete byte equality.
Compiler comparisons were sequential source hypotheses and policy checks. No
throughput, unique-trial total or per-entry forty-minute duration is claimed.
Unfinished source hypotheses and settings are retained in the external review
folder under `retained-drafts/`; they require independent review before reuse.

## Draft correctness fixes

The local draft generator now preserves ARM MLA operands and flags, resolves
simple ARM PC-relative literal loads with PC+8, and parenthesizes shifted
subtraction/address operands. Known runtime signatures now pass through
interworking veneers, preserving division operands that were previously dropped.
The executable decoder already handled MLA; these changes repair diagnostic
source generation. The division caller at 0800AC3C has thirteen divisions by 100
and one by 12, rather than an argument-free helper or one guessed denominator.

## Validation

- `make check -j4`: **148 tests passed**. The earlier exact-copy commit passed
  144 tests; four later regressions cover ARM arithmetic, literal addressing,
  shifted-expression precedence and division arguments through veneers.
- Focused draft checks: **14 tests passed**.
- Forced `make -B all -j4` recompiled and verified all **110** accepted C
  replacements and printed **`build/txra.gba: OK`**.
- Comparison of the entire rebuilt ROM with the supplied ROM is byte-identical.
- The new compiler-profile regression verifies all 94 bytes and demonstrates
  that the default interworking profile fails for this routine.
- All forty frozen entries have exactly one recorded outcome. `git diff --check`
  passes. Analysis-only indirect-call metadata drift was restored verbatim.

The private ROM remains a gitignored sibling symlink. No ROM, extracted asset,
compiler binary or intermediate assembly is committed. Compiler builds, comparisons, tests and review rendering ran at nice
15 or lower priority and used no more than four cores. The separate matching
service and its checkout were not accessed. No browser, remote test machine,
push, deployment, merge or stash was used.

## Review media

Review folder: `txra-review/deep-b/`.

- `before/status.png` and `after/status.png`: identical framing, showing
  109 → 110 functions and 12.566% → 12.677%.
- `outcomes.png`: the forty entries grouped by their final outcomes.
- `matching-review.webm`: **6 seconds, 30 fps, 1152×720, 196,323 bytes**, no audio.
  This is a matching-metadata replay; no gameplay footage is presented.
- `LOG.md`, `retained-drafts/`, `tests.log`, `build.log` and
  `review-validation.json`: per-entry learning, unfinished hypotheses and checks.

All three pictures were opened and inspected. The clip's opening, middle and
closing decoded frames were opened and inspected; labels fit and the matching
figures agree. Each picture/clip folder has NOTES.md and captions.json, with a
caption for every picture and clip. There is no known clipping in these review
figures. The game itself was not visually reviewed in this matching pass.

## Commits and owner notes

- `d123b4a`: exact runtime copy and its explicit compiler profile, matching
  configuration, progress totals and compiler-profile regression.
- `4883c33`: preserves ARM arithmetic and runtime arguments,
  with four focused regressions. The final handoff commit records the forty-entry
  outcomes, compiler findings, review renderer, this note and `DEEP-B-DONE`.
  Exact commit identifiers are also recorded in the external handoff note.

OWNER-NOTES.md was absent at startup, before major steps and at the final check.
There are no appended notes to apply or defer. The supplied owner concern that
TXRA does not seem to be running remains unresolved: this pass proves matching
build equality, and **does not establish a working PC runtime, boot, title,
playability or a completed race**. Existing progress milestones remain false.
The twenty-two ordinary C targets are still unfinished, and the seven ABI or
boundary entries need source/mapping recovery. The marker records this handoff,
not full decompilation or a running-game milestone.

Matched before/after: 109 / 110.
Percent before/after: 12.566% / 12.677%.
Learned: verify library compiler policies and recovered call arguments before tuning allocation.
