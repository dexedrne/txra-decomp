# Finish pass 6 integration (15 November)

`work/finish6-int` merges the three finish pass 6 lanes onto main bb4608a. The base lane's installed source for the last C owner, 08016DA8 (ARM track-face renderer, 4,288 bytes with pool, 96-byte frame), is kept; the deps lane reached an independent exact source by the same idea (copy the camera-space y into `saved_y` before the pitch rotation, as the installed sibling projections 08016C18 and 080164D0 do) and stays under `docs/finish6-1115/deps/`; the shape lane's notes are kept under `docs/finish6-1115/shape/`.

Checks on worker C, final merged tree:
- `make clean; make -j8`: rc 0, 194 `C match` lines including `func_08016DA8: C match (4288 bytes)`, `build/txra.gba: OK` (SHA-1 4197339d4add74bb40ed02a8fba5e58096afb487).
- `make check`: Ran 279 tests, OK (skipped=1).
- `make check-accuracy`: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed.

matches installed: 08016DA8 (exact C 193 -> 194; completion 227 -> 228 of 228)
near-misses improved: 08016DA8: 49 -> 0 (installed)
what blocks the rest: nothing; every one of the 228 entries is complete (194 exact C, 3 covered labels, 31 documented assembly interfaces)
