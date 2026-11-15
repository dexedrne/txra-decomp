# Hand matching, 11/3 continued (ship note)

## What changed

Three more functions match byte for byte, each committed on its own and
verified by a clean full rebuild that ends in `build/txra.gba: OK`:

| Address | Bytes | Function |
| --- | ---: | --- |
| 080154AC | 756 | text layout with word wrap |
| 08016C18 | 400 (ARM) | point-grid camera projection |
| 080162F8 | 472 | car model vertex projection |

Progress: **176 of 229 functions, 69,208 of 85,132 bytes (81.3%)**, in
`progress.json` and the README progress block. Techniques and blockers are in
the "11/3, continued" section of `docs/match-1102.md`.

## Near misses kept (docs/near-misses/hand-20261103/)

| Address | State |
| --- | --- |
| 080165BC (ARM, 1,628 bytes) | 21 instruction lines from a match, same length and frame; only the vertex-loop tail's schedule/allocation differs. |
| 080076F4 (ARM, 1,076 bytes) | setup, frame and buffer select match; the mixing loop is scheduled differently. |
| 08017F64 (ARM, 604 bytes) | 87 aligned lines; induction-variable shape of the inner loop differs. |
| 0800421C (Thumb, 4,066 bytes) | first complete draft of the HUD drawer; loop.c hoisting and global allocation still differ. |

## Validation

`make clean && make` ends in `build/txra.gba: OK` after every install; the
unit tests (`python -m unittest discover -s tests`, 172 tests, 1 skipped) pass.
`docs/map/indirect.json` drifts during `make` and was restored, not committed.

## Not done

The track streamer (08002854 with 08003786), the Thumb sound mixer (080064A4
and fragments), 080181C0 and 08016DA8 were not attempted beyond reading. No
OWNER-NOTES.md was present in the repository, so there were no owner notes to
act on. This is a ROM-matching job: there are no game pictures or videos.
