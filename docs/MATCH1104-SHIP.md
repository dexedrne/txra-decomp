# Matching, 11/4

Two more complete functions compile byte for byte with the original ARM
compiler. Each was installed only after a forced full rebuild passed the
complete ROM hash check, and each has its own commit.

| Commit | Function | Bytes | Change |
| --- | --- | ---: | --- |
| `535f925` | 080165BC, model emitter | 1,628 | Indexed vertex output, with x/z scaled in place, fixes the remaining allocation and schedule. |
| `e62a678` | 08017F64, sprite blend | 604 | A wide source pixel, shared destination-byte temporary, and separate row/column pointer forms retain the original four induction pointers and addition order. |

Progress is **178 of 229 mapped entries**, **71,440 of 85,132 bytes
(83.917%)**: two entries and 2,232 bytes added. `progress.json`, the README,
and the new 11/4 section of `docs/match-1102.md` agree. The optional mapping
array is absent from this branch's configuration, so the existing inventory
denominator was preserved when updating the two match totals.

## Verification

* Both new complete function outputs, including literal pools, match the ROM.
* Forced full rebuild after each installation: `build/txra.gba: OK`.
* Source formatting was followed by another successful byte-verifying build.
* `make check`: **172 tests, 171 passed, 1 skipped**.
* Both retained unmatched drafts compile with the real ARM profile and remain
  excluded from `tools/rom.cfg`. Their comparisons include the complete output;
  instruction diffs omit data pools using the original spans and assembler
  mapping symbols.
* Review media: **5 pictures and 2 clips**, all captioned. Both clips are
  eight seconds, 30 fps, with no audio; sizes are 819,963 and 845,772 bytes.

## Review

Folder: `txra-review/match-1104/`. It has `NOTES.md`,
`captions.json` and `media-validation.json`. I looked at every picture and
inspected before/after frames extracted from each clip. The before/after
pictures use the same original-code viewpoint.

Key pictures are `matching-progress.png`, `after-080165BC.png` and
`after-08017F64.png`, paired with the corresponding `before-` pictures.
`080165BC.webm` and `08017F64.webm` show the earlier draft and exact output
with a moving line marker. These are compiler comparisons; the game image
and behavior retain the original bytes. `tools/review_match1104.py` reproduces
the folder from the local ROM and compiler.

## Remaining work

The ARM mixer at 080076F4 improved to the correct 1,076-byte size and original
60-byte local frame, with **40 added/removed instruction rows and 110 differing
bytes** remaining. Its buffer-select move order, first sample address reloads,
final sum register and second-sample schedule still differ. The full current
draft and complete diff are retained in `docs/near-misses/hand-20261104/`.

That folder also holds a new full typed car-contact draft for 080181C0:
1,640 bytes against 1,684, frame 64 against 72. It restores the rotations,
six-point contact test and response logic omitted or obscured by the older
register-lift, but its cached offsets and allocation still differ. It has no
independent behavior verification and is not installed.

The HUD's prefix experiments left its frame and loop-hoisting blockers
unresolved; its 11/3 draft remains the current one. The streamer 08002854/08003786, enclosing Thumb
sound routine 080064A4 and ARM track-face renderer 08016DA8 still lack complete
matching C. Their source pieces, array strides and internal-entry boundaries
are recorded in `large-bodies.md` beside the drafts. No fragments or prefixes
were counted as matches. The assembly-interface entries remain unchanged.

## Owner notes and handoff

No `OWNER-NOTES.md` was present at the initial, intermediate or final checks,
so there were no live owner notes to address. No ROM, extracted assets or
binary slices were added. Review media stays outside the repository.
There was no push, deployment, merge or stash. The completion marker is
`MATCH1104-DONE`.
