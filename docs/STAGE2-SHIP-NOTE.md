# Stage 2 handoff

The native PC build boots and reaches the real game title. Start, name entry,
class selection, a car purchase and the main/race menus run through original
guest code. This is recompilation first; the four matching C replacements and
byte-identical original build remain intact.

## Changed

* `recomp/generate.py`: ROM/map-driven static ARM and THUMB translation, 228
  mapped functions plus 30 execution-address variants, direct mapped BL calls,
  internal-label dispatch, RAM encoding guards and an interpreter fallback.
* `runtime/`: SDL window/audio/controller/keyboard integration, guest CPU/state,
  memory, DMA, scanline bitmap/OBJ composition, affine coordinates, blending,
  timers/IRQ, PSG/FIFO audio, EEPROM serialization and atomic file persistence.
* `make recomp`, runtime checks, optional reference CPU comparisons, scripted
  keypad review recording, and jobs-board `progress.json` reporting compiled
  symbols and separately reviewed boot/title/playability milestones.
* Fixed three boot failures found in execution: banked system stack preservation
  on IRQ entry, DMA source alignment for copied THUMB code, and restoring the
  IRQ bank's stack pointer after every handler return. RAM code is checked before
  translated execution so a copied or changed instruction cannot silently use a
  stale translation.

## Validation and pictures

`33a43d7` contains the runtime, generator, checks, recorder and progress reporter
on `stage2-native-recomp`. The following handoff/marker commit completes this
branch; its hash is available from `git log -1`. The local main reference remains
at the stage-1 handoff; no merge was made.

Validation passed:

* Byte-identical `make`, expected ROM fingerprint, and all **6/6** original
  integration tests.
* **100** runtime assertions, including serial EEPROM plus backing-file
  persistence, repeated IRQ bank switches and misaligned DMA-source regression.
* **26,112** independent arithmetic comparisons: 18,592 THUMB and 7,520 ARM.
* A sanitized 960-frame boot/Start run with no reported memory/undefined-behavior
  failures; the earlier sanitized runtime assertions also passed.
* Compiled versus interpreter-only execution over 180 frames: identical guest
  memory/register fingerprint (`856087a6`) and byte-identical captured pixels.
* Two failure checks: missing ROM and a same-size ROM with a wrong fingerprint
  both reject cleanly before execution.
* The full native review ran **4,000 frames / 374,500,128 instructions**:
  374,434,806 compiled steps, 65,322 fallback steps, nine unique fallback PCs,
  zero unsupported instructions. Acceleration and both steering directions are
  visible in the final clip. `playable: true` is limited to this short scripted
  drive; a full race is still unverified.
* All **six** clips are muted VP9 WebM at 30 fps, 6–8 seconds each, and
  103,844–1,669,767 bytes each. Their durations/size/stream checks passed. Every
  delivered picture and sampled frames from every clip were visually inspected. No ROM, extracted assets, generated translation, save,
screenshot or clip is included in the commits. All review images come from our
own native executable. There was no browser session, push, deployment or merge.

Review destination: `txra-review/stage2/`. `NOTES.md` and
`captions.json` describe every image and clip. Compare `before-boot.png` with
`title.png`; the former is the first failed native boot, the latter is the
repaired title from the same full framebuffer viewpoint. `name-entry.png`,
`class-selection.png`, `main-menu.png` and `latest.png` show progression through
the game. `driving-attempt.webm` shows the short drive; `race-start.webm` shows the
race presentation. The other four clips cover startup and animated menus.

## Owner directions

* **Recomp first, decomp later:** delivered static native translation/runtime;
  no new matching-C decompilation work was prioritized.
* **Show progress on the jobs board:** root `progress.json` now reports mapped
  and actually compiled functions, boots, reaches_title and playable, with a
  plain evidence note. Emission alone is never counted as compilation.
* **Review clips and captions:** native startup/menu/race captures are recorded
  as muted 30-fps WebM clips, with a 4 MB size ceiling and per-file captions.
* No live `OWNER-NOTES.md` was present at the repeated checks during this job.
  The file was checked again immediately before the final handoff.

## Remaining limits

This is a bootable native execution port, not a completed hardware-accuracy or
full-playthrough milestone. Timing uses three clocks per instruction; DMA bus
arbitration, tiled background modes, windows/mosaic and precise affine reference
latching remain unfinished. Audio has square/wave/noise/FIFO paths but sweep,
stereo and detailed channel behavior need listening/reference comparison.
Multiplayer is disconnected. No physical-controller session has been verified.

Some shop/main-menu money labels appear clipped against the left edge in still
captures. Panel animation, windowing and timing need a reference comparison
before changing the game's drawing behavior; this is not declared fixed. The
title and name-entry screen are readable. A complete race, all routes,
in-game save/reload and comparison against original execution are not yet
verified. The EEPROM protocol and backing-file persistence have automated tests;
that does not substitute for the game's own save menu round trip.

The nine observed fallback addresses are the copied IRQ epilogue at
`03004ED8` through `03004EF8` in four-byte steps. They run successfully; no new
function-map completeness claim is made. Undefined CPU encodings or unsupported
BIOS calls still report failure rather than pretending to execute them.
