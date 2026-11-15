# PC runtime handoff

TXRA runs as a desktop game with a resizable, aspect-correct window, integer
scaling, fullscreen, a cream/warm-charcoal/amber PC pause overlay, configurable keyboard
and standard controller mappings, screenshots, and held 3x/half-speed debug keys.
Normal gameplay retains the original framebuffer. The controller Guide button
or Menu+Back chord opens the PC menu; Start stays available to the game.

Implementation commit: `74ca127`. The following handoff commit contains this note,
the completion marker, final reviewed progress, and the final chart measurements.
All commits use the requested author. No push, deployment, merge or stash occurred.

## Changes

- Prefer accelerated vsynced presentation, report a software fallback, center
  nearest-neighbor integer or aspect-fit output, and preserve the 3:2 picture.
  Focus loss pauses; keyboard and controller menu actions do not leak through to
  gameplay when resuming. Poll host input once per guest frame rather than once
  per small instruction quota, removing substantial front-end overhead.
- Preserve 32768 Hz guest stereo and resample to the opened stereo device rate,
  requesting 48 kHz and 480 device frames. Prefill about 40 ms, keep the normal
  output queue around 40–70 ms, apply backpressure to bound latency, and clear
  stale output during pause/mute/debug-speed transitions. Debug speeds are silent.
  Frame deadlines carry fractional ticks and rebase after long stalls.
- Create per-user saves/bindings/screenshots/diagnostics through SDL's application
  folder. Import a legacy working-directory EEPROM once without replacing an
  existing profile or deleting the original. Preserve 512-byte and 8192-byte saves.
  Reset asks for confirmation in the menu, retains a timestamped backup, and
  restarts the guest. Failed persistence reports failure; reset can be cancelled.
- `tools/build_pc.py` takes a player-supplied ROM and creates one executable,
  checks its fingerprint, handles paths with spaces, and replaces an existing
  output atomically so rebuilding works while an older executable is running.
  The native build uses system Python when the old matching environment is absent.
  SDL2 remains a system runtime dependency; no ROM or asset directory is packaged.
- `tests/runtime-golden.json` and `tools/check_accuracy.py` lock a fresh recorded
  4300-frame input route to the pre-polish frame hashes, every PCM byte, final
  state and sample-clock totals. Golden metadata is tracked; raw audio, frames,
  generated code, executables, EEPROMs and all ROM-derived material stay private.
  README and `docs/PC-RUNTIME.md` describe building, running, rebinding and reset.

## Validation

- 118 existing runtime assertions, 57 new desktop assertions, 22 desktop flow
  checks and 15 mapping/classifier tests passed. Standard virtual-controller
  checks passed for ten buttons, stick dead zone, diagonal input, disconnect and
  reconnect. New mapping tests also exercise a remapped face button and dead zone.
- Desktop checks cover binding-file round-trip and transactional rejection,
  exact integer/aspect viewport pixels, overlay isolation, screenshot dimensions,
  reset backup, stereo conversion, bounded queue and clearing on pause.
- Fresh-process tests cover legacy 512-byte migration, preserving an existing
  8192-byte profile, command-line reset, menu reset and cancellation, retained
  backup bytes, invalid bindings, and missing, wrong-size, wrong-fingerprint and
  oversized ROM rejection. A ROM path and output path containing spaces build and
  run successfully. The requested ROM remains an ignored root symlink.
- The final 4300-frame golden check passes: all frame hashes, every PCM byte,
  machine state and clock/sample counts match the unmodified runtime. There are
  zero fallback steps, unknown execution targets or unsupported instructions.
- A packaged 12500-frame full race reaches the loss result. Its first 4300 frames
  and PCM prefix match the pre-polish recording. The shipping executable's full
  frame hashes, audio hash, machine state and final result pixels are checked
  against this complete run. This proves a completed loss, not a win or career
  completion. The final reviewed progress record is bound to the shipping build.
- The original game's SAVE GAME sequence writes twice, then a separate process
  loads the profile with zero writes. EEPROM SHA-256 stays unchanged on reload.
  The corresponding pictures show the same money and car; rotation differs.
- The native window was exercised on a private local virtual display: pause,
  fullscreen, both scaling choices, resize, screenshot, held fast/slow speeds,
  reset confirmation/cancel and clean menu exit. All stills and sampled contact
  frames from every clip were inspected. No browser or remote capture machine
  was used, and temporary display processes and user folders were removed.

## Performance

The shipping complete race measured 94.91 fps uncapped: 12500 frames in
131.699793 seconds, 130.079959 CPU seconds, or 98.8% of one CPU core, including
native software presentation. The earlier packaged run measured 85.86 fps:
12500 frames in
145.591985 seconds, 142.833654 CPU seconds, or 98.1% of one CPU core. A shorter 4300-frame check measured approximately
101 fps; worker contention makes these observations, not portable guarantees.
A muted paced 300-frame run took 5.023431 seconds against a 5.022812-second target.

The final 48 kHz stereo dummy-device run took 5.142880 seconds for 300 frames
(58.33 fps), used 86.5% of one core, reported zero queue starvations and reached
66.729 ms maximum queued output. Queue backpressure allows playback to follow
host-device timing; this dummy run is about 2.4% slower than the nominal guest
frame rate. Queue-zero events are conservative diagnostics, not direct audible
underrun measurements. Real-device listening and compositor pacing remain untested.
An isolated diagnostic found the dummy backend draining five seconds of audio in
4.769 seconds with a 512-frame request; a 480-frame request avoids its fractional
millisecond wait interval. No guest sound data or sound-generation timing was changed.

The chart and machine-readable measurements are in the private review folder.
`tools/runtime_report.py` recreates the figure from completed run metadata using
Matplotlib; it is optional and is not required to build or run the game.

## Pictures and clips

Review folder: `txra-review/runtime/`, with NOTES.md and captions.json.

- `before-garage.png` / `after-garage.png` and `before-race.png` / `after-race.png`
  use identical guest frames 2080 and 4000. They are pixel-identical.
- `pause-window.png`, `fullscreen.png`, `aspect-fit.png`, `resized-aspect.png`,
  `resized-integer.png`, `speed-up.png`, `slow-motion.png` and `reset-confirm.png`
  show the new host controls in the actual native window.
- `save-profile.png`, `reload-profile.png`, `race-result.png`, and the standalone
  `performance.png` / `performance.svg` chart complete the still review.
- `desktop-menu.webm`: 9.933 seconds, 231767 bytes; `garage-menu.webm`: 6 seconds,
  1120664 bytes; `race-driving.webm`: 8 seconds, 1517357 bytes. All are muted VP9,
  30 fps and under 4 MB. Every picture and clip has a caption.

## Not done and remaining limits

This is a Linux executable using system SDL2, not a Windows build or fully static
portable bundle. Physical controllers from both supported standard families,
real-speaker quality, and actual compositor/monitor vsync behavior still need an
owner session. The software fallback and virtual-controller paths are verified.
The original PSG approximation, instruction timing, missing hardware behaviors,
multiplayer limitations and other stage-three accuracy caveats remain; hashes
preserve existing behavior and do not independently establish hardware fidelity.
The original left money label still looks clipped in the garage; the matching
before/after pictures retain it rather than changing game output to mask it.
No win, complete career or result-to-garage return is claimed.

The worker lacks the historical matching compiler environment and optional
independent arithmetic-reference package, so the original byte-identical rebuild
and its whole integration suite were not rerun. The PC build and listed focused
checks are independent of those tools. No new models, maps or vehicle assets
were created or modified; the review shows the original cartridge game.

## Owner notes

`OWNER-NOTES.md` was absent at the initial, major-step and final checks. There
were no appended owner notes to resolve. The requested clips, notes, captions,
private artifacts, save preservation, commit identity and no-push instructions
were followed. `RUNTIME-DONE` marks this handoff.
