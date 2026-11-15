# Matching round 2, 9 November

All three retained complete-owner C candidates improve the preceding round's
full-target differing-byte counts. **Zero replacements were installed.** The
registry remains at **181 exact entries, 72,524 bytes including pools, 85.19% of
85,132 mapped code bytes, and 229 mapped functions**. `progress.json`, the README
and registry agree. Work remains on work/match-1109, based on 865ee53.

| Owner | Differing bytes before -> after | Instruction edits before -> after | Output / original bytes | Frame / original |
| --- | ---: | ---: | ---: | ---: |
| 08016DA8 | 3,677 -> 3,401 | 855 -> 859 | 4,220 / 4,288 | 120 / 96 |
| 080064A4 | 3,473 -> 3,395 | 1,467 -> 1,452 | 3,656 / 3,828 | 100 / 108 |
| 0800421C | 3,831 -> 3,434 | 1,084 -> 1,056 | 4,120 / 4,124 | 36 / 36 |

ARM's byte improvement has an instruction/frame regression, explicitly shown
above and in its pictures. No size, frame or instruction score substitutes for
complete equality. The checker always receives the original complete-owner end.
All retained sources fit that end and fail equality; oversize diagnostics never
received a larger admission boundary.

## Target passes and commits

- `d47d5a1` — sound preparation identities, shorter cursor/command captures,
  separate sequence hardware results and a shared voice base. The prior phased
  hypothesis's fifth preparation pointer was wrong: it is the volume cursor at
  offset 48, not the arpeggio cursor at offset 64. A corrected six-pointer control
  reaches 1,380 instruction edits, versus the preceding phased control's 1,397,
  but is not the byte winner. Source, profile, diff and next step:
  [sound owner](near-misses/sound-owner-1109b/README.md).
- `a4ca9f5` — typed point indexing, captured source identities and separate
  geometry lifetimes, retaining the near-first flow and projection expressions.
  The byte winner still carries excess spills. A retained single-cursor control
  reduces the frame to 112 but has 3,503 differing bytes. Source, profile, diff
  and next step: [renderer](near-misses/arm-16da8-1109b/README.md).
- `321fa16` — the original mixed smoke-loop induction followed by phase scopes
  and granular scalar-role merges. The opening source/index and projected-effect
  temporaries now have distinct lifetimes while the original shared scratch
  aliases remain. A separate control has the original 4,124-byte size and
  36-byte frame, 1,051 instruction edits and 3,497 differing bytes. Source,
  profile, diff and next step: [HUD owner](near-misses/hud-owner-1109b/README.md).

The final evidence commit is titled `Record second-round review and admission results`.
Every commit uses the requested author without trailers. There was no reset,
rebase, stash, push, deployment or merge into main, and no additional job was started.

The bounded source passes visited 1,527 ARM, 2,112 sound and 4,735 HUD source
identities, producing 402 / 1,418 / 2,519 distinct compiled outputs respectively.
Invalid declaration hypotheses and oversize diagnostic outputs are recorded,
not counted as successful sources or matches. Search summaries and compressed
manifests preserve these outcomes. No projection-induction or car-contact trial
was repeated, and no compiler-family sweep, padding, hand-written bytes, inline
assembly, register binding or additional state object was used.

## Validation

One forced whole-ROM rebuild recompiled and byte-verified **all 181 installed
replacements**, regenerated the inventories and passed the pinned full-ROM
SHA-1 check. The registry is byte-identical to 865ee53. The admission suite ran
**223 tests: 222 passed, one skipped, zero failed**. The existing skip reports
that fewer than two unmatched retained drafts remain for its resumable-search
fixture. No second whole-ROM rebuild was needed. `tools/progress.py` was run and
the README/progress/registry counts were checked afterward.
[Admission receipt](near-misses/admission-1109b.json) pins the registry, build and
log identities and the test counts.

Each of the two retained ARM sources passes **199 independent synthetic memory
fixtures**, 20 fixed expected checks, three layout sizes and 14 field offsets,
reaching all 1,053 original instruction addresses. Each of the two sound sources
passes **seven existing synthetic fixture groups**, with strict warnings and
undefined-behavior sanitization. Each of the two HUD sources passes **1,024 state
and ordered-helper-call fixtures** against the prior semantic C, with the six
scratch aliases and undefined-behavior sanitization intact. Sound/HUD fixtures
are not independent original-instruction oracles. None of these checks establishes
real-game acceptance, arbitrary malformed-state behavior or a new runtime milestone.

All six retained source profiles were reproduced with the unmodified comparison
helper. Final receipt checks confirm that every source hash agrees with its
profile and fixture record, all strict limits are unchanged, and every retained
source is marked uninstalled and non-exact. The three new target folders total
**1,047,389 bytes**. Long search manifests and control diffs are gzip files; only
each best candidate's full sanitized diff is uncompressed. No raw instruction
encoding columns, pool contents, ROM slices or extracted binaries are committed.

## Review pictures and clips

Finished review folder: `txra-review/match-1109b/`.

Key pairs are `before-08016DA8.png` / `after-08016DA8.png`,
`before-080064A4.png` / `after-080064A4.png`, and
`before-0800421C.png` / `after-0800421C.png`. Each uses the same original code view
before and after, with full-owner metrics and the original frame shown. All six
final pictures were opened and inspected. The HUD pair was retaken to omit
stored-data placeholders and expose the actual code rows; the valid ARM and
sound pictures/clips were preserved.

`08016DA8.webm`, `080064A4.webm` and `0800421C.webm` are each **eight seconds,
30 fps, 1600x1000, video-only**. Final sizes are **787,633 / 795,560 / 739,871 bytes**,
all below 4 MB. Decoded frames at 0.5 through 7.5 seconds from each clip were
opened and inspected in `clip-overview.png`. The clips replay code comparisons;
they are not new gameplay footage. No browser, server or browser profile was
created. No vehicle, world or gameplay change requiring a roller or drive was made.

The folder contains five plain sentences in `NOTES.md` and one caption for every
picture/clip in `captions.json`. All ten artifact sizes and SHA256 hashes agree
with [review-1109b.json](near-misses/review-1109b.json), which also records video
properties. Source/compiler hashes are in the target profiles; the build identity
is in the admission receipt. These are the finished source/build/media references
for coordinator review and archival. No storage archive was moved.

## Remaining work and owner notes

All three owners still differ substantially and remain uninstalled. ARM retains
a 24-byte frame excess and four additional instruction edits; separate the
far-path values from the near geometry without a second face cursor before
changing projection. Sound retains an eight-byte frame deficit; continue from
the corrected six-pointer control and recover the voice-base/counter lifetime
across the sequence-to-voice transition. HUD retains a four-byte output deficit
and incorrect opening overlay register lifetimes; keep the recovered smoke loop
and inspect the source/zero/counter lifetimes across the opening helper calls.
Exact next experiments and already exhausted alternatives are in each folder.

No gameplay execution, performance gain, new native milestone or complete match
is claimed. `OWNER-NOTES.md` was absent at the initial, per-target, pre-build,
review and final reads, so there are no appended owner notes left unaddressed.
The private ROM hash was verified and the ROM remained on this host behind the
ignored link. Ignored local build/search scratch is preserved for continuation.
Marker: `MATCH1109B-DONE`.

matches installed: none
near-misses improved: 08016DA8: 3,677 -> 3,401; 080064A4: 3,473 -> 3,395; 0800421C: 3,831 -> 3,434
next target: 0800421C (opening overlay source/zero/counter lifetimes)
