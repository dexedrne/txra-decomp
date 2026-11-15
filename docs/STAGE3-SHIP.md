# Stage three ship note

A battle race is playable from title through its normal loss result. EEPROM save,
process exit and reload restore the same name, purchased purple car and money.
`progress.json` records boots, reaches_title, playable, full_race and saves as true,
bound to the reviewed executable. This is a completed loss, not a win or completed
career. The result menu is captured; a successful return from that result menu to
the garage was not verified.

## Changes and commits

- `a1c04e5` — frame deadlines at 59.72750057 Hz, explicit uncapped benchmark mode,
  edge-split scanlines/timers/sample clocks, HBlank at clock 1008, independently
  routed stereo mixing and FIFO refills, signed sound gain, window and blend
  masks, affine reference latching, controller reconnection, diagnostic capture
  and frame/audio comparison tools, and translation of the nine observed IRQ
  epilogue addresses. The 228-function static inventory is preserved; the reviewed
  epilogue source span and RAM alias live in `recomp/observed.json`.
- `0e72196` — byte writes preserve the programmed timer reload latch rather than
  copying bits from its moving counter.
- The handoff commit containing this note records the input scripts, status,
  review-tool refinements, documentation and completion marker.

The ROM remains ignored, as do generated translation, extracted runtime buffers,
save files and captures. No push, deployment, merge or stash was performed.

## Validation

- 118 runtime assertions pass, including batched versus single-clock timing,
  cascades, FIFO DMA isolation, signed/stereo sound, reload-latch byte writes,
  rectangular/object windows, alpha composition and affine references.
- Six ROM/matching-build integration checks pass; the rebuilt binary matches the
  player-provided ROM. 26,112 arithmetic reference comparisons pass.
- Virtual controller tests pass for ten mapped buttons, stick dead zone,
  diagonal input, disconnect and reconnect. Keyboard mapping remains documented.
- The final native executable and interpreter match all 12,500 framebuffer hashes,
  final machine state, every PCM sample and sample-clock totals. Native execution:
  1,170,372,096 translated instructions; zero fallback steps, unknown execution
  targets or unsupported instructions. The nine stage-two IRQ targets are compiled.
- 6,857,649 stereo sample pairs were generated. Peak magnitude is 7232, with no
  clipped samples. This route uses identical speaker output; synthetic tests
  independently verify separate left/right routing. Captures are muted and no
  listening-quality claim is made.
- A 300-frame paced run with the dummy audio device took 5.023785 seconds against
  a 5.022812-second deadline. The uncapped 12,500-frame run took 157.034007 seconds
  for 209.283829 seconds of guest frames. Deadlines derive from one epoch rather
  than accumulated rounded sleeps.
- `tests/save-input.txt` opens Quest, leaves with B, selects YES and confirms the
  game's SAVE GAME prompt. The 3700-frame process writes an 8192-byte EEPROM file
  twice. After process exit, `tests/reload-input.txt` confirms LOAD GAME in a fresh
  2200-frame process, restores the profile and writes nothing. Save-file SHA-256
  stays unchanged on loading. A separate 512-byte legacy copy loads to identical
  machine state and pixels, remains 512 bytes and preserves every byte.

Private final logs are in `build/stage3-verified/`. The captured session in
`build/stage3-final/` has byte-identical per-frame hashes and PCM to the final
executable's repeated run. `tools/compare_runtime.py` checks the comparisons.

## Pictures and clips

Review folder: `txra-review/stage3/`. Every image and clip has a caption;
the folder and its before/ subfolder each have plain owner notes.

- `before/main-menu.png` versus `main-menu.png`: identical frame 2080 viewpoints.
- `before/race.png` versus `race.png`: identical frame 4000 viewpoints.
- `title.png`, `results.png`, and the separate idle `menu-settled.png`.
- `saved-profile.png` and `reloaded-profile.png`: the same car and money across
  process exit and EEPROM reload; car rotation differs because capture times differ.
- `title-menu.webm`: 8 seconds, with a cut from title/name entry to moving car menus.
- `race-driving.webm`: 8 seconds of acceleration and steering.
- `race-results.webm`: 6 seconds covering the race ending and loss result.

All three clips are muted VP9, 720x480 at 30 fps, respectively 1,339,073,
1,612,129 and 219,826 bytes. Pictures, clip contact frames and the full session's
snapshot contact sheet were visually inspected. These are native SDL captures;
no test browser or browser profile was started for this work.

## Remaining limits

The money label still looks clipped at the left edge. In an idle menu, its display
matches the guest's indexed VRAM bitmap exactly, with zero differing pixels and
an identity affine matrix. The interpreter matches it too. This needs an independent
hardware/reference comparison to distinguish original layout from shared CPU/helper
behavior; host rendering has not been changed to mask it.

CPU instructions still charge three clocks each, with no accurate bus wait states
or DMA arbitration. Frame/scanline/timer/sample clocks and host pacing are improved,
but this is not cycle-accurate hardware emulation. PSG sweep, wave-bank behavior,
exact trigger/envelope edges, mosaic, tiled backgrounds, pixel-level register
changes, some BIOS wait semantics, nested IRQs and multiplayer remain incomplete.
Physical controller play and audible fidelity need a hands-on check. No race win,
career completion or result-menu return to garage is claimed.

## Owner notes

`OWNER-NOTES.md` was absent when checked throughout the work and before handoff.
There were no appended owner notes to resolve. The requested videos, captions,
review notes, privacy restrictions, save preservation and commit identity were
followed. No original models or world/vehicle assets were changed.
