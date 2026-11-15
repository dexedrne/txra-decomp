This is the earlier 11/4 snapshot. The mixer was subsequently matched and
installed; see `src/generated/func_080076F4.c`. The next contact draft and
partial sound recovery are in `../hand-20261104b/`.

# Uninstalled drafts, 11/4

Neither C file here matches the complete original. Both compile with the real
`arm` profile; neither is referenced by `tools/rom.cfg`.

| Address | Output / target bytes | Remaining issue |
| --- | ---: | --- |
| 080076F4 | 1,076 / 1,076 | 40 added/removed instruction rows and 110 differing bytes. The frame, voice setup and checks, buffer addresses, output length and function tail agree. The first sample's address reloads, the final sum register, the second sample's schedule and the buffer-select move order differ. |
| 080181C0 | 1,640 / 1,684 | New full typed car-contact draft. The frame is 64 / 72 bytes; cached offsets and most reload allocations differ. This replaces the earlier register-lift as a readable starting point, without claiming an exact match or independent behavior verification. |

`results.json` records complete output comparisons, including literal pools.
The `.diff.txt` files contain decoded instruction text only, without raw ROM
bytes. The row score counts both additions and removals in the unified diff;
it is not the same metric as historical aligned-row or byte scores.

The source pieces and next boundaries for the track streamer, Thumb sound
routine and ARM track-face renderer are in [large-bodies.md](large-bodies.md).
