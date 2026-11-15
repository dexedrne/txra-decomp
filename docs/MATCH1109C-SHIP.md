# Matching round 3, 9 November

Three complete-owner structured-C nonmatches are closer. **No replacement was
installed.** The registry remains **181 exact entries, 72,524 bytes including
pools, 85.19% of 85,132 mapped code bytes, and 229 mapped functions**. Registry,
README and `progress.json` agree. Work stayed on `work/match-1109`, based on
ad5b543; main was not changed.

| Owner | Differing bytes before -> after | Instruction edits before -> after | Output / original bytes | Frame / original |
| --- | ---: | ---: | ---: | ---: |
| 0800421C | 3,434 -> 3,258 | 1,056 -> 1,048 | 4,124 / 4,124 | 36 / 36 |
| 08016DA8 | 3,401 -> 3,258 | 859 -> 899 | 4,260 / 4,288 | 108 / 96 |
| 080064A4 | 3,395 -> 3,353 | 1,452 -> 1,415 | 3,692 / 3,828 | 100 / 108 |

The renderer's 40-edit regression is explicit: lower byte distance does not
establish recovered original allocation. Its frame excess shrank from 24 to 12
bytes. Every final comparison uses the unchanged complete owner end and compiler
profile. Matching size or frame never substitutes for equality.

Target passes and commits:

- `8382602` — HUD strip positions, strip index, map scale/base/x and projected
  width lifetimes. The recorded opening zero/source/counter experiment stalled;
  narrower subsequent roles produced the improvement. A separate control has
  3,260 differing bytes and 1,045 instruction edits, with original frame/length.
  [HUD source, structural summary and next step](near-misses/hud-owner-1109c/README.md).
- `91b442a` — renderer direct-path index reads, C point/depth capture, separate
  A/C/B x offsets and y/z pointers, per-face point base and shorter ring state.
  Projection arithmetic and induction were retained. The separate 104-byte-frame
  control has 3,363 differing bytes and 882 instruction edits.
  [Renderer source, structural summary and next step](near-misses/arm-16da8-1109c/README.md).
- `e7304fb` — sound tone-instrument scope, clear-buffer/countdown identity and
  three shorter field-address roles. Work began from the recorded corrected
  six-field control. Its new mixed-sequence/tone control improves instruction
  edits from 1,380 to 1,338, with byte distance unchanged at 3,542.
  [Sound source, structural summary and next step](near-misses/sound-owner-1109c/README.md).
- `62672b1` — focused HUD decimal-gauge follow-up. Separate digit lifetimes,
  quotient/remainder forms and argument captures did not improve either retained
  source. The receipt records that plateau and replaces the now-tested next step.

The final evidence commit is titled `Record third-round comparisons and admission results`.
All commits use the requested author, with no trailers. No reset, rebase, stash,
push, merge, deployment or extra job was used.

Each target README now groups remaining regions by allocation, scheduling /
selection, control-flow layout, literal pools and frame. `structural.json` gives
original block/window counts and a separate instruction-shape alignment. Those
heuristic counts are not additive causal byte attributions or semantic proof.
The largest positional windows are HUD projected effects (838 / 868 bytes),
renderer near visibility/packets (1,188 / 1,592), and sound envelopes
(1,319 / 1,512); earlier shifts contribute to these counts.
`tools/structural_match1109c.py` reproduces the metadata from a retained profile.

Search receipts pin 4,445 HUD, 1,748 renderer and 4,310 sound source identities,
with 1,516 / 281 / 1,357 distinct compiled outputs. Invalid historical-C scope,
macro-member and declaration hypotheses are recorded as rejected diagnostics;
only retained sources receive semantic approval. Oversize diagnostics retain
no admission authority and never receive a larger boundary. There was no
compiler-family sweep, hand-written encoding, assembly, register binding,
padding, artificial write or added state object. Long manifests and control
diffs are gzip files; only each best candidate's full sanitized diff is plain
text. Target folders total **1,155,889 bytes**, below the round's receipt budget.
No ROM slice, extracted binary, raw encoding column or pool content was committed.

Validation is complete. One forced whole-ROM rebuild recompiled and byte-verified
**all 181 installed replacements**, regenerated the inventories and passed the
pinned full-ROM SHA-1 gate. The registry is byte-identical to the starting commit.
Final admission ran **223 tests: 222 passed, one skipped, zero failed**. The existing
skip reports fewer than two unmatched retained drafts for its resumable-search
fixture. The suite was repeated after all retained sources were frozen; both runs passed.
`tools/progress.py` ran afterward; no extra rebuild was needed.
[Admission receipt](near-misses/admission-1109c.json) pins registry, build and log
hashes, counts and the skip reason.

Each of the two HUD sources passes **1,024 state and ordered-call fixtures**
against the prior semantic C, with six transform aliases and undefined-behavior
sanitization. Each of the two renderer sources passes the independent textual
ARM executor's **199 memory fixtures**, 20 fixed expected checks, three layout
sizes and 14 field offsets, reaching all **1,053** original instruction addresses.
Each of the two sound sources passes **seven existing synthetic fixture groups**
with strict warnings and undefined-behavior sanitization. Sound/HUD fixtures are
not independent original-instruction oracles. All six final source hashes agree
with their fixture receipts and profiles from the unmodified comparison helper.
These checks do not establish arbitrary malformed-state behavior or a runtime milestone.

Finished review folder: `txra-review/match-1109c/`.

Key pairs are `before-0800421C.png` / `after-0800421C.png`,
`before-08016DA8.png` / `after-08016DA8.png`, and
`before-080064A4.png` / `after-080064A4.png`. Each pair uses the same original code
view and exposes full-owner byte/instruction/frame measurements. All six final
pictures were opened and inspected. The HUD pair was retaken at the changed
sprite-strip setup after its first gauge view showed unchanged local code;
valid renderer/sound proof was preserved.

`08016DA8.webm`, `080064A4.webm` and `0800421C.webm` are each **eight seconds,
30 fps, 1600x1000, video-only**, sized **805,761 / 739,288 / 747,547 bytes**.
Decoded frames at 0.5 through 7.5 seconds from every final clip were inspected in
`clip-overview.png`. The clips replay code comparisons, not gameplay. No browser,
server or browser profile was created; this code-only pass changed no vehicle,
map or road and requires no roller or drive recording.

The folder has five plain sentences in `NOTES.md` and a caption for every picture
and clip in `captions.json`. All ten media sizes/hashes agree with
[review-1109c.json](near-misses/review-1109c.json). Target profiles pin source and
compiler hashes; the admission receipt pins the build. These are the finished
source/build/media references for coordinator archival. No archive was moved;
ignored local build/search scratch remains available. Free disk remained about
187 GiB, above the 20 GiB reserve.

All three owners remain substantial nonmatches and uninstalled. HUD still has
source/zero/counter allocation differences despite original length/frame. The
renderer retains a 12-byte frame excess and worse instruction distance. Sound
retains an eight-byte frame deficit and a 136-byte output deficit. No new
real-game run, audio playback proof, performance gain or native milestone is
claimed. Next experiments are concrete and source-specific in each README.

`OWNER-NOTES.md` was absent at initial, per-target, validation, capture and final
reads: there are no appended owner notes to list or leave unresolved. The
private ROM hash was verified without printing bytes; it remains on this host
behind the ignored symlink. Marker: `MATCH1109C-DONE`.

matches installed: none
near-misses improved: 0800421C: 3,434 -> 3,258; 08016DA8: 3,401 -> 3,258; 080064A4: 3,395 -> 3,353
next target: 0800421C (source-row component address lifetimes at 08004CD4..08004D20)
