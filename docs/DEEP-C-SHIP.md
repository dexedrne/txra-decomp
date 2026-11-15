The following two reports preserve independent work from the same frozen slice. Their totals and unfinished classifications describe their respective baselines. The merged build includes five distinct matches from these reports, including 08018E88, and supports both historical and modern ARM compilation. Current combined totals are recorded in DECOMP.md and progress.json.

## Earlier main report

# TXRA deep hand matching — slice c

One **four-byte ARM tail branch** at 08018E88 now builds from ordinary C. The
whole ROM remains byte-identical. Accepted totals move from **109 functions /
10,698 bytes / 12.566%** to **110 / 10,702 / 12.571%**, using the same 85,132-byte
mapped-code denominator. **No large function matched.**

Match commit: `ea00348` — Replace the ARM tail thunk with byte-verified C.
The accompanying handoff commit records the forty-entry audit, retained hypotheses,
progress metadata and this note. No push, deployment or merge was performed.

## Scope and implementation

The selection is the baseline's 120 unmatched entries sorted by `(bytes,
address)`, taking `[2::3]`; its forty rows are fixed in
[targets.json](deep-c/targets.json). It was not recalculated after the new match.
The full [outcome table](deep-c/OUTCOMES.md) accounts for every selected entry:

| Outcome | Entries |
| --- | ---: |
| Exact ordinary C replacement | 1 |
| C candidates still unmatched | 21 |
| Assembly or private calling convention | 12 |
| Invalid standalone boundary | 6 |

The new `modern-arm` profile uses the installed current compiler with ARM O2,
ARM7TDMI and Thumb interworking disabled. Enabling interworking retains a call
and return frame, so it misses the tail branch. The ARM destination takes no
incoming arguments and its observed caller ignores the return value. The
replacement covers the entire mapped ARM branch, not the adjacent Thumb
state-changing instruction or the initialization body it reaches. This tiny
match does not identify the original compiler.

The judge and full build share the new profile. ARM branch relocations validate
instruction shape, link bit, state, alignment and range. ARM7TDMI's BX compatibility
hints retain their validated assembler instruction. Explicit `arm_func_XXXXXXXX`
names reach mapped ARM entries without replacing the existing Thumb veneer aliases.
The new checks include a real linker comparison and reject wrong code and
out-of-bound extents. No source supplies instructions as data, inline assembly,
or patched compiler output.

## What helps the next function

- The 72-byte channel layout at 08005F8C reduces the retained instruction/byte
  score from **71/118 to 27/89**. An independent comparison confirms all 96 bytes
  of its loop agree. Its setup/tail and full extent still do not match.
- The packet receiver at 080149FC improves from **40/167 to 17/76** under old O1.
  Preserving its previously discarded stack store and actual byte-width status
  reads gives the exact first 72 bytes and the right full size. Saved-register
  allocation and pointer reuse remain unresolved.
- Several old drafts narrowed live pointers or lost arguments. The byte blitter
  has nine arguments. The division veneer hides two arguments, including the
  clamp routine's denominator six. The spawn routine has a four-word copied
  aggregate plus a separate sixteen-word array, rather than a single-word buffer.
  Switch tables need their cases and shared tails reconstructed before searching.
- Combined sound, record-initializer and packet units were tested in both orders
  with old O2, standard O2 and old O1: **42 judgments**, with **21/21 complete
  outputs unchanged by reversing order**. The already matched packet sender is
  exact only under its existing old O2 setting in this experiment. Those two
  control rechecks are not new matches or evidence for a blanket O1 setting.
- Both large ARM C candidates were tried with the historical ARM executable and
  the current compiler, including optimization, frame and interworking options.
  Neither matched. The conventional ARM frames and bounded switches were not
  incorrectly labeled assembly-only; see [asm-only.md](asm-only.md).

[The evidence guide](deep-c/README.md) links the source hypotheses, independent
final comparisons and group experiment. The larger bodies remain unfinished;
several hypotheses are repaired lifts, not recovered original-level C. No claim
is made that every entry received a forty-minute timed window. These are recorded
source/ABI investigations, not another randomized neighborhood search.

## Validation

- Final forced `make -B -j4 all` prints **`build/txra.gba: OK`**.
- Whole-file `cmp` confirms the rebuilt 4 MiB ROM is byte-identical.
- Final **`make check`: 152 tests passed**, including nine ARM relocation,
  compiler, boundary, negative-code, alias and linker-reference checks.
- Nineteen unfinished Thumb hypotheses were independently recompiled uncached;
  both ARM hypotheses retain their seven-profile comparisons. All remain rejected.
- `git diff --check` passes. The base ROM is an ignored sibling symlink. ROM
  slices, extracted assets, binaries and private intermediate assembly are absent
  from the commit.
- Build invocations used at most four jobs. Source comparisons were serial;
  compiler/build/encoding work used nice 15. The separate matching service was
  neither accessed nor changed.

## Review pictures and clip

Review folder: `txra-review/deep-c/`.

- `before/matching-status.png` and `after/matching-status.png`: same framing and
  denominator; accepted count 109 → 110.
- `matching-findings.png`: the tiny exact branch and the two improved drafts.
- `slice-outcomes-1.png` and `slice-outcomes-2.png`: all forty assigned entries.
- `compiler-checkpoints.webm`: **six seconds, 180 decoded frames, 30 fps,
  no audio, 335,262 bytes**, showing matching checkpoints. It is not gameplay.
- `OUTCOMES.md`, `audits.json`, `logs/`, `reproduce/` and
  `review-validation.json`: reasoning, comparison/build/test evidence and local
  reproduction helpers. The review copy of this ship note also lists both final
  commit hashes.

All five still pictures were opened and inspected. Initial crowded score columns
were spaced out before the final render. Opening, middle and closing video frames
were extracted and opened: labels fit and values are legible. Every image folder
has NOTES.md and captions.json; every picture and clip has a caption.

## Owner notes and unfinished work

OWNER-NOTES.md was absent at startup, major steps and the final check; no appended
owner note was skipped. The open report that the native build did not seem to run is not
claimed fixed by a four-byte decompilation replacement. No boot, title, playable,
race or save milestone was newly reviewed, and those progress fields were left
unchanged. No game execution or launch repair was attempted in this matching pass.

Twenty-one selected C bodies still need deeper reconstruction. Six entries need
boundary recovery with their enclosing functions; the adjacent slice's entries
were left untouched. Twelve private interfaces/startup/BIOS entries remain
assembly responsibilities. The new branch provides very little added source
coverage. `DEEP-C-DONE` marks this review and handoff, not completion of those
remaining bodies.

Matched before/after: 109 / 110.
Percent before/after: 12.566% / 12.571%.
Learned: check interworking flags and call signatures before register tuning.

## Incoming deep-d report

# TXRA deep matching — slice c

Four complete C replacements add **1,460 bytes**. The build moves from **109 / 10,698 bytes / 12.566%** to **113 / 12,158 bytes / 14.281%**, using the unchanged 85,132-byte mapped-code denominator. Every addition includes its literal pools and in-function alignment, fits its next entry boundary, and passed a forced full build ending in `build/txra.gba: OK`. The ROM is byte-identical.

## Accepted commits

| Commit | Entry | Bytes | What resolved the match |
| --- | --- | ---: | --- |
| 3e61952 | 08005F8C | 228 | Eight typed voice records and nine-word preset rows reproduce induction and the argument spill. |
| 4602f08 | 0800B254 | 332 | Explicit output pointer lifetimes, integer row addressing and assignment evaluation order. |
| 388c823 | 0800A00C | 368 | Shared record shape, stack-local declaration order and an upward loop that the compiler turns into a countdown. |
| 2ed25be | 0800A68C | 532 | Destination initialization order and separate lexical scopes for the two transfer regions. |

All four use the existing `old` profile with O2 and Thumb interworking. No new compiler profile, instruction patch, inline assembly or function outside the frozen slice was installed. The final documentation/checking commit accompanies these four matching commits.

## Scope and remaining work

All 120 initially unmatched entries were sorted strictly by `(bytes, address)` and zero-based indices `2, 5, 8, …` were frozen before matching. All 40 assigned entries are accounted for in [the running table](deep-c/README.md) and `deep-c/outcomes.json`: four matches, thirteen hand-written C misses, two large-menu diagnostic C baselines, thirteen retained assembly/library entries, six boundary problems and two compiler-shaped ARM entries needing a different acceptance path. No elapsed-time minimum or exhausted forty-minute quota is claimed.

Thirteen uninstalled source hypotheses and their fresh complete-pool scores are retained under `deep-c/candidates/`. They are provisional C drafts, not recovered source or behavior guarantees. The 23-instruction / 32-byte spawn miss at 0800B908, the 36-instruction / 42-byte sound initializer miss at 08007398, and the 43-instruction / 54-byte palette-effect miss at 0800EDF4 are useful next starting points. The two large menus still need high-level reconstruction; only diagnostic compiler baselines were completed there. None of the 36 remaining entries in this slice was converted or counted as C.

[Assembly and boundary evidence](asm-only.md) distinguishes custom register contracts and BIOS/state-switch wrappers from incomplete mappings. Long backward transfers at 08003786 and 08006776 reuse an existing frame; their apparent recursion is an internal loop branch. 0800421C ends before its shared epilogue. Enclosing entries owned by other slices were left untouched. The division helper's exact library provenance remains unproven. ARM 080076F4 and 080181C0 look compiled and were not mislabeled as hand assembly.

## Compiler and diagnostic findings

O1/O2/Os, both installed Thumb compiler variants, interworking behavior and selected documented optimization flags were measured on source hypotheses. Several scheduler/loop options are rejected by this historical compiler; rejection was never scored as a match. Moving neighboring sound routines before/after the initializer or buffer source did not change the result. The four wins came from source structure, not a compilation-unit-order or flag workaround.

The local ROM symlink was absent and has been restored to the supplied private ROM. The standard compiler executable was also absent, making the baseline build fail at an existing replacement. It was built locally from the pinned source. `tools/setup.sh` now installs both required Thumb variants; its shell syntax check passes. The legacy compiler build requires its existing serial dependency order.

`tools/diffhint.py` now includes referenced literal tails even when a trial is shorter, accepts an explicit profile and defaults to an installed function's recorded profile. Two regression checks cover a short trial's literal tail and an installed nondefault profile. Failed drafts can no longer look artificially closer because the CLI silently stopped before the final pool.

## Validation and review

The final `make -j4 check` passed **145 tests** in 92.504 seconds. The focused diagnostic suite passed 14 tests. A final `make -j4` printed `build/txra.gba: OK`, and direct comparison with the private reference ROM passed. `bash -n tools/setup.sh` and whitespace checks passed. Four additional uncached complete-function comparisons and next-entry checks are recorded in `deep-c/verification.json`. The separately managed matching process was neither contacted nor changed.

Review folder: `txra-review/deep-c/`.

- `before.png` and `after.png`: identical progress-card layout, 109 before and 113 after. Both were opened and inspected.
- `progress.webm`: six seconds, 30 fps, silent VP9, 148,840 bytes; an extracted middle frame was inspected. This records code-recovery totals.
- `NOTES.md`, `captions.json`, `RUNNING.md`, `targets.json`, `outcomes.json` and `summary.json` accompany the review.

Gameplay execution, title/race progress and save behavior were not revalidated. Existing execution milestone fields remain false. The owner's “doesn't seem running” concern is addressed only for this checkout's missing ROM link/compiler and successful ROM build; a running/playable game is still unproven. No game pictures, new animation, car/road assets, gameplay footage or driving route changes are claimed.

## Live owner notes and completion

`OWNER-NOTES.md` was absent at the repeated major-step checks and the final completion check. No live note was silently skipped. No push, deployment, merge, stash, model-service change or ROM/data artifact commit was made. Completion markers are `txra-review/deep-c/DONE` and `/tmp/txra-deep-c.done`, touched after validation and the final note.
