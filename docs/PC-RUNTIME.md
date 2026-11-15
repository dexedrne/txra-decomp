# TXRA on PC

Use a supported player-owned 4 MiB cartridge dump. Its SHA-1 is
`4197339d4add74bb40ed02a8fba5e58096afb487`. The ROM and ROM-derived build outputs
are private inputs, never part of the source repository or a distributable package.

## Build and run

Linux needs a C11 compiler, make, Python 3, pkg-config, and SDL2 development files
(version 2.0.14 or newer for the virtual-controller tests). The PC build does not
need the historical matching compiler or Python packages.

```
python3 tools/build_pc.py /path/to/your/cartridge.gba
./build/txra-pc --rom /path/to/your/cartridge.gba
```

The output is one native executable with no asset directory or embedded ROM.
SDL2 and its platform libraries are system runtime dependencies. Keep the ROM
separately and supply `--rom` when launching outside the repository. This is a
Linux build, not a Windows executable or a statically linked portable bundle.
Other desktop platforms have not been tested.

With the supported ROM available as `baserom.gba`, `make recomp` also works.
The original matching build remains available through `make` and `make check`;
it still needs the separate tools described in TOOLS.md.

## Controls

| Action | Keyboard | Standard controller |
| --- | --- | --- |
| Game A / B | X / Z | South / east face button |
| Start / Select | Enter / Backspace | Menu or Options / Back or Create |
| Directions | Arrows | D-pad or left stick |
| R / L | S / A | Right / left shoulder |
| PC pause menu | Escape | Guide, or Menu + Back together |
| Fullscreen | F11 or Alt+Enter | Pause menu |
| Screenshot | F8 | Pause menu |
| Debug 3x / half speed | Hold Tab / grave | Keyboard |

The two standard controller families use the same SDL mapping. Connect and
reconnect while running; the keyboard and controller can be used together.
Start still belongs to the original game. Escape opens the PC menu; select Quit
there to exit. Navigate that menu with arrows or the D-pad, select with Enter or
the south face button, and go back with Z or the east face button. Focus loss
pauses gameplay; `--no-focus-pause` disables that behavior for capture setups.
Overlay input is held back from the game until released on resuming. The debug
speed badge appears only while a speed key is held. Debug speeds are silent.

## Display and sound

The resizable 960x640 window defaults to nearest-neighbor integer scaling. The
240x160 guest picture remains centered with black borders, including fullscreen
and high-DPI displays. The pause menu offers aspect fit, which preserves 3:2
while filling more of a window. A window smaller than the source falls back to
aspect fit. `--fullscreen`, `--aspect-fit` and `--no-vsync` are launch options.
An accelerated renderer with vsync is preferred, with a reported software
fallback when unavailable. Vsync availability depends on the display driver.
Frame deadlines retain fractional counter ticks at the cartridge's 59.7275 Hz;
large stalls rebase the clock rather than causing a burst of catch-up frames.

The guest generates signed 16-bit stereo at 32768 Hz. SDL converts it to the
opened stereo device rate (48000 Hz requested, 480-frame device buffer requested; the driver may round it).
A roughly 40 ms prefill and bounded queue keep latency low without discarding
normal-speed guest samples. Device clock drift applies queue backpressure.
Pause, mute and speed changes clear stale output, and resume prefills again.
`last-run.json` records underruns and maximum queue duration. `--mute` suppresses
device playback while preserving the guest audio hashes. `--benchmark` is an
uncapped, silent diagnostic mode. Approximate PSG hardware behavior remains
unchanged; an audio hash match does not establish original-hardware fidelity.

## User files, rebinding and reset

SDL creates the per-user `dexedrne/TXRA` application folder. On Linux this lives
under `$XDG_DATA_HOME` or `~/.local/share`; the startup log prints the selected
save and binding paths. It contains `txra.sav`, `bindings.ini`, screenshots named
`shot-*.bmp`, `last-run.json` and the unknown-target diagnostic log.

Existing 512-byte and 8192-byte EEPROM saves load unchanged. If no user-folder
save exists, an old `txra.sav` in the launch directory is copied there once; the
original stays intact. Failed import aborts without deleting the original.
`--save FILE` selects a different backing file and bypasses this import.
Normal saves still use the existing atomic temporary-file/rename path.

Edit `bindings.ini` and restart to rebind. Keys use SDL scancode names, including
names with spaces; controller buttons use SDL standard button names. For example:

```
key.a=Space
pad.a=y
deadzone=16000
```

All ten guest actions are configurable: `a`, `b`, `select`, `start`, `right`,
`left`, `up`, `down`, `r`, `l`. The file created on first launch lists every
mapping. Dead zone accepts 0 through 30000. Invalid files are reported and launch
stops; the file is never silently overwritten. Escape, F8, F11, Alt+Enter, Tab,
grave, Guide and the Menu+Back chord are reserved host controls. Menu navigation
uses the fixed controls above. Left-stick digital directions remain fixed.
`--bindings FILE` selects a separate mapping file. SDL controller mapping
updates can also be supplied through SDL's standard mapping environment.

Reset Save in the PC menu asks for confirmation, flushes pending writes, moves
the old file to a timestamped `.reset-*.bak` beside it, then boots a fresh guest.
A failed write or backup cancels reset. B or Escape cancels confirmation.
`--reset-save` explicitly performs the same backup before boot at launch.
Backups are never automatically deleted. To restore one, close the game, retain
any current save, and copy the desired backup to the chosen save path.
Reset is disabled during input/coverage/raw diagnostic recordings so a capture
cannot silently lose its frame sequence. F8 screenshots include the host overlay;
`--screenshot FILE` retains the original exact guest PPM capture behavior.

## Verification and private review

```
make check-runtime check-desktop
make check-accuracy
```

The 4300-frame golden recording uses `tests/race-input.txt` and a fresh isolated
save. It locks every rendered frame, all PCM bytes, final machine state, guest
clocks and sample counts to the unmodified pre-polish runtime. Only hashes and
counts are tracked; all generated frames and sound remain ignored. A regression
fails until deliberately investigated; there is no automatic golden-update
command. Both runtimes share hardware helpers, so this is a behavior-preservation
check, not independent hardware validation.

`--ui-script FILE` accepts ordered `guest_frame action` rows for host automation:
`pause`, `resume`, `fullscreen`, `screenshot`, `up`, `down`, `accept`, `cancel`,
`quit`. Commands continue while paused, without advancing guest frames.

`tools/review_runtime.py OUTPUT` captures the actual native window in an isolated
local virtual display, exercises keyboard shortcuts and the menu, and removes
its own display/processes and temporary user folder. It needs Xvfb, the X test
extension library, and ffmpeg. Hold a worker capture slot while running it.
Images and muted 30 fps WebM clips belong in the private review folder together
with NOTES.md and captions.json, never in git. Physical controller feel, real
speaker listening and compositor-specific pacing still need an owner session.

Implementation references: SDL's [audio stream conversion](https://wiki.libsdl.org/SDL2/SDL_NewAudioStream),
[user application folders](https://wiki.libsdl.org/SDL2/SDL_GetPrefPath), and
[dummy device timing](https://github.com/libsdl-org/SDL/blob/main/src/audio/dummy/SDL_dummyaudio.c).
The dummy backend rounds its delay to milliseconds; a 480-frame request at
48 kHz gives it an exact 10 ms interval. Real devices choose their own supported
buffer size. The queue-zero counter is a starvation diagnostic, not a direct
measurement of audible device underruns.
