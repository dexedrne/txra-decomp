# Native execution

For the current desktop build, controls, saves, pause menu and packaging see
[PC runtime](PC-RUNTIME.md). The stage-three execution and hardware notes below
remain the accuracy reference.

`make recomp` produces `build/txra-pc`. Supply the supported player-owned
`baserom.gba` in the root. The matching `make` / `make check` targets are retained.
No ROM bytes, extracted assets, generated translation, save files, pictures or
recordings belong in version control. ROM-dependent outputs stay in ignored
`build/`; the executable reads all game data from the ROM at runtime and checks
its fingerprint against the translation before execution.

## Build and controls

Linux dependencies: a C11 host compiler, make, pkg-config, SDL2 development
headers/libraries, Python 3, and the existing stage-1 tool environment. The
recompiler itself uses only Python's standard library. Keep the stage-1 compiler
and Python settings in `tools/local.mk` for the original matching build.

```
make recomp
./build/txra-pc
make check check-runtime
```

Keyboard: X = A, Z = B, Enter = Start, Backspace = Select, arrows = directions,
S/A = right/left shoulder, Escape = PC pause menu. A connected standard game controller
uses the face buttons, Start/Back, D-pad or left stick, and shoulder buttons.
Controllers are discovered at startup and on attachment, and reconnect after removal.
SDL's standard face-button mapping is A = south (Cross), B = east (Circle),
Start = Options, Select = Back/Create, R/L = right/left shoulder. The D-pad and
left stick both provide digital directions, with a 12000-unit stick dead zone.
A connected controller and the keyboard can be used together. `make check-controller`
checks this mapping, disconnect and reconnect with an SDL virtual controller;
a physical controller session remains to be checked.
Audio opens as signed 16-bit stereo at 32768 Hz; `--mute` disables the device
without disabling guest audio processing.

The default EEPROM file is now in the per-user application folder; select a separate test file with `--save`.
Existing 512-byte and 8192-byte EEPROM contents load without clearing their
bytes; the unused tail is initialized to FF. Writes persist an 8192-byte backing
image by temporary file plus rename, periodically and at normal exit. The old
file is retained on a failed write. This is a raw EEPROM file, not an application
save-format conversion.

The in-game round trip is now verified: from a fresh profile, enter Quest,
press B to leave it, choose YES on SAVE GAME, then confirm with A. This writes
the EEPROM backing file. Quit the process, restart with the same `--save` path,
press Start, select YES on LOAD GAME, and confirm A. The same name, purchased car
and money load in the main menu, and loading leaves every save-file byte unchanged.
`tests/save-input.txt` (3700 frames, fresh save) and `tests/reload-input.txt`
(2200 frames, existing save) reproduce this without editing game memory. The save
run makes two successful atomic file writes; the reload run makes none. Both
execute without unknown targets or fallback instructions. The populated 512-byte
legacy form also reloads to the identical framebuffer and machine state without
expanding or changing the file.

Useful review commands:

```
./build/txra-pc --headless --mute --benchmark --frames 900 --screenshot build/title.ppm
./build/txra-pc --headless --mute --benchmark --frames 180 --interpreter --stats build/reference.json
./build/txra-pc --headless --mute --benchmark --frames 1200 --auto-start 900
```

`--rom`, `--save`, `--stats`, `--screenshot`, and `--video` take paths. Screenshots
are exact 240x160 PPM framebuffers. Video is raw 240x160 BGRA, every second guest frame. Its source frame rate is
`16777216/561792`; encode with that input rate and `-r 30` for review clips.
`--video-start` and `--video-end` select guest frame bounds (end exclusive).
`--audio-dump` writes interleaved signed 16-bit stereo PCM at 32768 Hz.
`--frame-hashes` writes a hash of every rendered frame; `--snapshots` selects an
existing directory for PPM snapshots every 300 frames. `--unknown-log` selects
a per-run fallback target log so independent tests cannot overwrite each other.
These outputs are private and must stay outside version control.

Normal execution, including headless execution, is limited to
`16777216 / 280896 = 59.72750057` frames per second. Every deadline comes from
the initial performance-counter epoch, with integer quotient/remainder arithmetic,
so rounded delays do not accumulate. `--benchmark` removes the limiter. Audio
samples are generated every 512 guest clocks, independently of host frame pacing.
Paced playback queues all samples; uncapped audio bounds its queue and may discard
samples, so use `--mute` for benchmarks and captures. Device opening errors are
reported rather than silently claiming audio playback. `--input-script` reads lines
`first_frame end_frame hexadecimal_pressed_mask`, with an exclusive end and
bits in KEYINPUT order (A, B, Select, Start, right, left, up, down, R, L). This
injects keypad input through the hardware register, without replacing game
logic. `--trace` writes private register traces to `build/trace.log`; for runs
longer than twelve frames it traces only the last frame. Traces can be large.

## Translation and dispatch

`recomp/generate.py` reads the ROM, `tools/rom.cfg`, and the stage-1 function map.
It emits 229 mapped C functions and 31 run-address variants, including the
reviewed IRQ epilogue now integrated into the function inventory. Every
mapped instruction becomes a C case calling an already decoded semantic
operation with constant operands. This is static operand decoding, rather than
a wrapper which decodes each ROM instruction at runtime. ARM predicates,
register shifts, NZCV, PC reads, interworking, multiply, memory, block transfers
and status-register operations live in `runtime/cpu.c`. The guest registers,
flags, banked stacks and hardware state live in `GBA`.

Mapped ARM and THUMB BL destinations use direct C calls. Returns and computed
branches update guest PC/state; a sorted PC/state-to-C-function table covers
mapped instructions, including internal switch labels. `recomp/observed.json`
retains the reviewed IRQ source span and alias as historical evidence; the
generator skips a supplemental entry whose start is already in the inventory,
so the integrated epilogue is emitted once. Calls can yield when the
instruction quota expires, then resume through this table. Guest return state
stays in guest registers and memory. The quota bounds host recursion.

IWRAM variants are emitted at execution addresses, so branches and PC-relative
loads use their run PC. DMA still copies the real bytes, in order. Each RAM
instruction is checked against the translated encoding before executing: a
changed instruction exits to the decoder, which reads fresh memory on every
step. This handles overlap and modification without a stale decoded-block
cache. ROM/EWRAM/IWRAM accesses use direct region pointers; alignment and bus
side effects stay in the memory helpers.

An ARMv4T fallback decodes unmapped instructions and uses the same semantic
operations. Unknown execution PCs are deduplicated in `build/unknown-targets.log`.
Undefined encodings or unimplemented BIOS services are explicit failures;
claiming that every possible unknown address can execute would be incorrect.
The mapped game's CpuSet/CpuFastSet services have native implementations.
Halt/wait, division and square root are also available. Wait services use minimal interrupt wakeup rather than complete BIOS wait-flag semantics. There is no full BIOS.

## Hardware model and limits

* Scanline scheduling: 1232 clocks/line, 228 lines/frame, VBlank at line 160,
  HBlank at clock 1008, VCount comparison and interrupt flags. IRQ entry/return
  provides the BIOS hook convention, banked stack state and saved context. IRQ
  delivery is serialized; nested IRQ execution is not implemented.
* DMA: immediate, VBlank, HBlank and direct-sound refill; aligned sources,
  fixed/increment/decrement destinations/sources, repeat, count and completion
  flags. Transfers have immediate memory effects; detailed transfer bus timing
  and arbitration are not modeled.
* Four timers with reload, prescaler, cascade, overflow IRQ and FIFO consumption.
  Advances split at each timer overflow, sample clock, HBlank and line boundary;
  batched execution is checked against clock-at-a-time stepping across three frames.
  CPU scheduling currently charges **three clocks per instruction**, not accurate
  instruction/bus timing. This is sufficient for the verified boot/menu path,
  not a timing-accuracy claim.
* Modes 3/4/5 bitmap scanout, affine BG2 coordinates, palette, OAM, normal/affine
  sprites, tile mapping, object priorities, alpha and brightness blending.
  WIN0/WIN1 and object-window masks now gate layers and blending, including
  wrapped window edges. Affine reference writes latch signed 28-bit coordinates,
  increment by PB/PD per visible line and reload at the frame boundary. Hidden
  objects no longer become an extra alpha-blend layer. Object windows, rectangular
  windows, alpha composition and affine latching have framebuffer assertions.
  Mosaic, tiled background modes 0/1/2, pixel-level register effects and exact
  affine-write edge timing remain unfinished. Those tiled modes were not required
  by the observed boot/menu/race path.
* PSG square, wave and noise generation, duty/frequency/volume, length/envelope
  stepping, direct-sound FIFOs and timer-driven DMA refill feed SDL audio.
  The mixer now honors separate speaker routing and PSG speaker gains. FIFO
  refill requests select only the DMA channel assigned to that FIFO, including
  when the FIFOs use different timers. Signed PSG gain and independent speaker
  routing have regression checks. Sound remains approximate: sweep, wave-bank
  behavior and detailed trigger/envelope timing need an independent reference.
  Captures are muted; audible fidelity has not been verified by listening.
* Active-low keypad and serial EEPROM command/read/write protocol, including
  DMA commands, are implemented. Link start clears deterministically to represent
  a disconnected peer; multiplayer and serial IRQ timing are not implemented.

## Verified milestones

The root `progress.json` is the jobs-board status. `tools/progress.py` counts
mapped function symbols actually present in the generated object only when the
object and executable are current relative to the generated source. Emission
alone is not counted. The reviewed boot/title/playability flags come from the
local `build/milestones.json` evidence record, bound to the executable SHA-256; absent or stale evidence defaults to false.
A clean rebuild needs its execution milestones reviewed again.

Boot, title, menu selection, car purchase and a complete battle-race loss result
are visually verified in this PC build. `tests/race-input.txt` runs 12,500 frames
from a fresh EEPROM, accelerates and steers, and reaches the result screen.
`full_race: true` means a complete race ending in a loss, not a race win or
completion of career mode. All 12,500 frame hashes, final machine state and
6,857,649 stereo sample pairs match the interpreter fallback exactly. The native
run executed 1,170,372,096 translated instructions with no fallback steps, unknown
targets or unsupported instructions. Sound peaks at 7232 with no clipped samples;
the game used identical left/right output on this route, while separate speaker
routing is covered by a synthetic signal regression test. A 300-frame paced run
with SDL's dummy audio device took 5.023785 seconds (target 5.022812 seconds).
The uncapped native race run took 157.034007 seconds for 209.283829 seconds of guest
frames. Actual audio-device listening and a physical controller remain unverified.

The nine stage-two fallback PCs, `03004ED8` through `03004EF8` in ARM mode,
are now statically translated. The extended stage-three native test reports no
unknown execution targets and no fallback steps. Any newly observed address must
be recorded and reviewed before adding a source span and alias to the supplemental
map; changed RAM instructions still fall back to fresh decoding.

`make check-runtime` exercises CPU flags/shifts, PC/interworking, unaligned loads,
RAM mirrors, video bus writes, DMA, timer IRQ acknowledgement, BIOS copies/math,
mode-4 scanout, EEPROM serial round-trip, repeated IRQ bank switches and DMA
source alignment. `make check-cpu-reference` is an optional arithmetic differential
check requiring the `unicorn` Python package; its random vectors exclude
PC-register operand differences between CPU generations. It does not validate
hardware or cycle timing. `--interpreter` additionally permits a whole-runtime
comparison between static translation and fallback decoding; both share semantic
helpers, so that comparison cannot independently prove those helpers correct.

`tests/boot-input.txt` is the reproducible keypad sequence used for the extended
menu check. `python tools/review.py <review-directory>` records native screenshots
and muted 30-fps WebM clips (each under 4 MB), using an isolated save in `build/`.
Use the worker's capture lock while recording. It needs an external encoder and
writes ROM-derived pictures only to the requested private review destination.

## Stage-three verification commands

```
make recomp check-runtime check-controller
make check check-cpu-reference
mkdir -p build/stage3-final/native
./build/txra-pc --headless --mute --benchmark --frames 12500 \
  --input-script tests/race-input.txt --save build/stage3-final/native.sav \
  --stats build/stage3-final/native.json --frame-hashes build/stage3-final/native.hashes \
  --audio-dump build/stage3-final/native.pcm --unknown-log build/stage3-final/unknown.log \
  --snapshots build/stage3-final/native --video build/stage3-final/session.bgra
./build/txra-pc --headless --mute --benchmark --interpreter --frames 12500 \
  --input-script tests/race-input.txt --save build/stage3-final/reference.sav \
  --stats build/stage3-final/reference.json --frame-hashes build/stage3-final/reference.hashes \
  --audio-dump build/stage3-final/reference.pcm --unknown-log build/stage3-final/reference-unknown.log
python3 tools/compare_runtime.py build/stage3-final
python3 tools/review_stage3.py <private-review-directory>
# Add --menu-picture <idle-menu-ppm> to include a separate idle-menu capture.
```

Use fresh, isolated save paths for these runs. The comparison checks every frame,
final machine state, every PCM sample, sample-clock totals and absence of native
fallback/unsupported steps. The interpreter shares semantic helpers and renderer,
so matching it does not establish independent hardware accuracy. The left edge of the menu money label is clipped in both modes, including the
idle menu. A debugger capture confirmed the displayed money region matches the
guest's indexed VRAM bitmap exactly (zero differing pixels); its affine matrix
is identity. This is not fixed by the host renderer changes. An independent
hardware/emulator comparison is still needed to distinguish original game layout
from shared CPU/helper behavior. Neither game layout nor ROM data was patched to
hide it. `menu-settled.png` is a separate idle-menu run, not a claim that this
clipping has been repaired.

Timing constants and FIFO routing were cross-checked against the primary
[mGBA video definitions](https://github.com/mgba-emu/mgba/blob/master/include/mgba/internal/gba/video.h)
and [audio implementation](https://github.com/mgba-emu/mgba/blob/master/src/gba/audio.c).
No external emulator code or ROM-derived generated source is included.


## Whole-ROM mapping and coverage

See `docs/MAP.md` for the current ROM partition and unknown regions. `--coverage`
writes metadata-only unique PC/mode sets, branch edges, exact ROM read intervals,
and DMA/BIOS source extents. It does not change guest instruction timing or save
contents; it has no coverage allocation when omitted. The final 12,500-frame
race matches frame-for-frame and in final machine/audio state with logging on
and off, with zero fallback/unknown/unsupported steps in both runs. Synthetic
logger/classifier tests are part of `make check`; `make check-mapping` runs the
focused subset. `tools/coverage_run.py` runs the menu/options/shop/save/load
scripts into a fresh private directory. ROM-sized coverage means mapped code
plus data plus fill, with unknown bytes reported separately; function counts
remain separate from byte coverage.
