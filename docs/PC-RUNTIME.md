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
separately and supply `--rom` when launching outside the repository; a bare ROM
path (`txra-pc cartridge.gba`, or a file dropped on the executable) also works.
macOS and other desktop platforms have not been tested.

## Windows build

The Windows x86-64 executable is cross-built with MinGW-w64 GCC and the official
SDL2 MinGW development SDK (`SDL2-devel-2.30.x-mingw.tar.gz` from the SDL GitHub
releases; unpack it outside the repository). On Debian-family hosts install
`gcc-mingw-w64-x86-64` and `binutils-mingw-w64-x86-64`.

```
make windows SDL2_WINDOWS_ROOT=/path/to/SDL2-2.30.12/x86_64-w64-mingw32
make package-windows SDL2_WINDOWS_ROOT=/path/to/SDL2-2.30.12/x86_64-w64-mingw32
```

`make windows` runs `tools/build_pc.py --target windows` (`--sdl2-root` or
`TXRA_SDL2_WINDOWS_ROOT` also select the SDK) and writes
`build/windows/txra-pc.exe`, `SDL2.dll` and `SDL2-LICENSE.txt`. The recompiled
code and runtime use the same optimization flags as Linux. The executable is a
GUI-subsystem program that imports only `SDL2.dll`, `KERNEL32.dll` and
`msvcrt.dll`; libgcc is linked in, the stack reserve is 8 MiB like a Linux main
thread, and the link carries no timestamp, so the same sources and toolchain give
the same file. Its manifest (`runtime/windows/`) selects the UTF-8 code page, so
user folders and ROM paths with non-ASCII names work, declares Windows 10/11 and
never requests elevation. Per-monitor DPI awareness keeps the nearest-neighbor
picture sharp on scaled displays.

`make package-windows` (`tools/package_windows.py`) writes
`build/release/windows/txra-pc-windows-x86_64.zip`, a `SHA256SUMS` for it and a
receipt JSON with file hashes, DLL imports and toolchain versions. The zip holds
one folder with the executable, `SDL2.dll`, `README-PC.txt` (from
`runtime/windows/README-PC.txt`), the SDL2 license and `SHA256SUMS` for those
files. Entries carry fixed timestamps (`SOURCE_DATE_EPOCH` when set). It never
contains the ROM or any data taken from it.

Windows-specific behavior, all behind `_WIN32`:

- Saves, bindings, screenshots and logs live in `%APPDATA%\dexedrne\TXRA\`
  (SDL's user folder). Saves are published with `MoveFileEx`, because C
  `rename` cannot replace an existing Windows file.
- Started from a console, output goes to that console; redirected output works
  as usual. Started from Explorer, startup errors (missing or unsupported ROM,
  SDL failures, rejected bindings) appear in a dialog, and the log is written
  to `last-run.log` in the user folder. `--headless` never shows dialogs.
- The one-time legacy save import uses an exclusive `_open`, since the
  `msvcrt.dll` C runtime this build links has no `"x"` open mode. `last-run.json` reports process CPU time
  from `GetProcessTimes`, because `clock()` measures wall time on Windows.

Frame hashes, frame times, run statistics and the unknown-target log are written
in binary mode on every platform, so a Windows run produces byte-identical files
and `tools/check_accuracy.py --existing DIR` can check it.

Under Wine 11.21 the packaged executable reproduced the 4300-frame accuracy
golden and the 37,200-frame career plus 2,200-frame reload goldens exactly:
every frame hash, PCM byte, final state, guest cycle and sample count, and the
career save, with no fallback, unknown or unsupported operations. The
`tests/save-input.txt` route (3700 frames from a fresh save) made two save
writes, the second replacing the existing file, and left the same save and frame
hashes as Linux. ROM and save paths with Cyrillic and CJK names worked. A
physical Windows PC, its display, audio devices and controllers, and the
no-console dialog and log path remain untested.

`tools/rom_bytes_scan.py FILE...` counts ROM bytes embedded in build outputs:
every non-trivial 32-byte window (`--window N` changes the length) of the ROM's
non-code regions from `tools/rom.cfg`, with code regions counted separately. It
prints counts and ROM offsets only. For the Windows executable, `generated.c` and
the compiled recompiled code it found no ROM data or code windows at 32 bytes,
nor at 16 bytes for the executable. The only ROM-derived constants in the
generated code are the CRC-32 and the instruction words guarding RAM-resident
code (6321 compare immediates, 23,026 bytes), which are compiled into
instructions rather than stored as a table.

With the supported ROM available as `baserom.gba`, `make recomp` also works.
The original matching build remains available through `make` and `make check`;
it still needs the separate tools described in TOOLS.md.

## Linux release package

```
python3 tools/build_pc.py /path/to/your/cartridge.gba
make package-pc
```

`tools/package_pc.py` writes `build/release/txra-pc-linux-x86_64.tar.gz` holding the
stripped executable, `README-PC.txt` (from `docs/release/README-PC-linux.txt`) and
`SHA256SUMS`, plus an outer `SHA256SUMS` and `receipt.json`. The archive is
reproducible for a given executable: sorted entries, fixed owners and modes,
`SOURCE_DATE_EPOCH` (or the commit date) as the timestamp and no gzip timestamp.

Packaging uses the supported ROM only to verify the result. `tools/scan_embedded_rom.py`
searches the stripped executable for every 32-byte run of the ROM's non-code
regions from `tools/rom.cfg` (runs with fewer than 8 distinct byte values are
counted but skipped) and packaging stops if any run is found. It also attributes
every instruction case in `build/generated.c` to the ROM region it was lifted
from. Only counts are printed or recorded. The executable needs glibc 2.34 or newer
(only `__libc_start_main` needs more than 2.14 when built on a current toolchain)
and the system SDL2 library.

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
under `$XDG_DATA_HOME` or `~/.local/share`, on Windows under `%APPDATA%`; the startup log prints the selected
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
