# Matching round, 9 November

Choices recorded before compiling any candidate:

1. **08016DA8**, complete 4,288-byte ARM track-face renderer. Required private-host instruction/allocation pass. The prepared 4,028-byte historical-ARM control is the starting point. The already exhausted projection-loop induction experiment will not be repeated, and 080181C0 is excluded as requested.
2. **080064A4**, complete 3,828-byte Thumb sound owner through 08007398. Its complete corrected source has only one historical compiler measurement (2,996 bytes, 832 bytes short); the frame and expanded envelope source shape have not been diagnosed. This is the closest remaining complete source by known size gap after excluding installed entries and exhausted trials; its previous receipt has no byte-distance score.
3. **0800421C**, complete 4,124-byte Thumb HUD owner through 08005238. The retained frame experiment emits 4,200 bytes with 3,892 differing bytes. It is the other remaining complete compiled source with measured nonmatch evidence. Its older semantic draft and allocation/loop-hoisting notes will guide a bounded pass.

The current rank command was run with the existing project Python environment. It admits only 080181C0 and 08016DA8 as standalone mapped candidates; sound/HUD are enclosing owners whose mapped internal labels must not be compiled independently. The current mutation queue excludes all historical small near-misses because they are already installed. The streamer has no complete compiled candidate/score. Selection therefore uses sound and HUD complete-owner evidence rather than stale small-entry scores. Their baseline byte distances will be measured before comparing source hypotheses.

Baseline: 181 registered exact C entries, 72,524 bytes including pools, 85.19% of 85,132 mapped code bytes; 229 mapped functions. This differs from the brief's historical 179 total and agrees with the existing README and reconciliation. No new matches are claimed by this note.

The private ROM hash was verified against the requested SHA1; only an ignored local link was created. No OWNER-NOTES.md was present at the initial read. No browser, gameplay, model or vehicle work is involved in this compiler round.

Results, validation, commits and exact next steps will be appended as each pass completes.

ARM pass completed: 08016DA8 remains uninstalled. Complete comparisons improve
from 1,046 instruction edits / 3,850 differing bytes to 855 / 3,677; output is
4,016 versus 4,288 bytes and the frame is 88 versus 96. The retained source,
full sanitized diff, compiler profile, bounded search manifest and independent
199-fixture check are in docs/near-misses/arm-16da8-1109/. Next is typed point
indexing with the original separate x offsets and y/z pointer lifetimes, not a
repeat of the exhausted projection-induction or car-contact trials.

Sound pass completed: 080064A4 remains uninstalled. The primary complete source
improves 1,541 instruction edits / 3,568 differing bytes to 1,467 / 3,473, and
2,996 output bytes to 3,644 of 3,828. Its frame is 104 versus 108. Separate
validated frame-control and phased-field sources retain useful alternatives:
3,624 bytes / 108-byte frame / 3,498 differing bytes, and 3,716 / 92 / 3,537.
Each passes the seven existing synthetic sound fixture groups with strict
warnings and undefined-behavior sanitization. The bounded allocation/pattern
sweep visited 636 sources and 603 distinct outputs. Evidence and exact next
steps are in docs/near-misses/sound-owner-1109/.

The comparison helper now removes both ordinary instruction encodings and the
single-space Thumb call encoding column, plus literal contents. Three regression
tests cover that privacy filter, the unchanged strict boundary for oversized
diagnostic output, and propagation of unrelated checker failures.

HUD pass completed: 0800421C remains uninstalled. Shared scratch-record aliases
and an entry-initialized affine-counter pointer reduce the old frame experiment
from 4,200 to 4,096 bytes against the 4,124-byte owner, retaining its 36-byte
frame. Instruction distance improves 1,181 to 1,084 and full-owner byte distance
3,894 to 3,831. The older 3,892-byte receipt included two matching bytes outside
the owner; this round counts all overrun bytes as differing and preserves the
strict next-owner rejection. Separate byte/allocation controls are retained.
Each of the three retained HUD sources passes 1,024 synthetic state/call-trace
fixtures against the old C draft, which is not an original-instruction oracle.
The allocation/pattern pass visited 617 sources and 37 compiled outputs.
Evidence and the mixed smoke-loop induction next step are in
docs/near-misses/hud-owner-1109/.

## Final validation and review

The exact registry stays at **181 entries, 72,524 bytes including pools,
85.19% of 85,132 mapped code bytes, and 229 mapped functions**. This round
installs zero replacements. `progress.json`, the README, registry and this
report agree. The baseline already included the two reconciled four-byte
entries; they are not new matches from this round.

| Commit | Work |
| --- | --- |
| `15574a5` | ARM near-first control flow, retained C, complete comparisons and independent synthetic check. |
| `fba65fc` | Sound pointer/allocation recovery, validated controls, comparison helper and three safety regressions. |
| `629a723` | HUD scratch aliases, complete comparisons, controls and state/call-trace fixtures. |

The final evidence commit is titled `Record round comparisons and admission results`.
All commits use the requested author and remain on work/match-1109. No reset,
rebase, stash, push, deployment or merge into main occurred.

One forced whole-ROM rebuild recompiled and byte-verified all **181 installed
replacements**, regenerated the inventories, and passed the pinned full-ROM
SHA-1 check. The registry is byte-identical to the pinned base. No second whole-ROM
rebuild was run. Admission suite: **223 tests, 222 passed, one skipped**. The skip
is the resumable-search test's existing guard because fewer than two unmatched
retained drafts remain for that fixture. `tools/progress.py` was run afterward.
`docs/near-misses/admission-1109.json` records the counts, registry hash and build
identity. Retained target checks separately cover 199 independent ARM synthetic
fixtures, seven sound groups per retained source, and 1,024 prior-C HUD regression
fixtures per retained source; the latter two are not original-instruction oracles.

Review folder: `txra-review/match-1109/`. Key picture pairs are
`before-08016DA8.png` / `after-08016DA8.png`,
`before-080064A4.png` / `after-080064A4.png`, and
`before-0800421C.png` / `after-0800421C.png`. All six final pictures were opened
and inspected. They use the same original code focus, with consecutive compiled
instructions alongside it. A first layout left long gaps around moved code;
the final pictures and clips were regenerated with both columns filled.

`08016DA8.webm`, `080064A4.webm` and `0800421C.webm` are each eight seconds,
30 fps, 1600x1000 and video-only. Final sizes are 1,445,495 / 1,477,759 / 1,355,839 bytes respectively; all are below the required 4 MB limit.
Decoded frames at 0.5 through 7.5 seconds from every clip were visually inspected
in `clip-overview.png`. This is compiler evidence, not new gameplay footage.
The folder contains five plain owner-note sentences and captions for all ten
pictures/clips. `docs/near-misses/review-1109.json` records their sizes, dimensions,
video properties and SHA256 hashes. No browser or server was needed or left running.

All three functions still differ substantially from the original, and none is
ready for installation. ARM frame/point lifetimes remain wrong; sound field
capture phases and hardware-result allocation remain wrong; the HUD mixed
smoke-loop induction forms remain wrong. Their retained C/profile/diff records
and exact next source steps are in their dated folders. No runtime acceptance,
performance gain or new native execution milestone is claimed.

No OWNER-NOTES.md was present at the initial, per-target, pre-build or final
checks, so there are no appended owner notes left unaddressed. The private ROM
remained on this host behind an ignored link. No ROM, extracted binary, literal
table contents or raw ROM instruction-encoding columns were committed. Local build
and search scratch remain ignored for continuation; final source and media hashes
are recorded for the coordinator. Marker: MATCH1109-DONE.

matches installed this round: none
near-misses recorded: 08016DA8 (3,677 bytes differing), 080064A4 (3,473), 0800421C (3,831)
next target: 080064A4 (six preparation pointers, then command-block lifetimes)
