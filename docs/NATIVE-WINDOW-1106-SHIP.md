# Native Linux window review handoff

Actual SDL window creation, software rendering, X11 keyboard events, resizing,
minimum-size enforcement, fullscreen, pause/resume, persisted rebinding and menu
quit passed on a private Xvfb display. Runtime source is unchanged. This closes
the private Linux software-window check only; it does not establish physical
keyboard/controller, accelerated GPU, Windows, hardware display pacing or audible
audio acceptance. The DONE marker means coordinator review handoff only.

Work began Friday November 6 at 17:30 ET, inside the newly authorized evening
window. Exact base:
`c51286ec5005f053022e0fbee0711ab4f2f1af90`. No reset, rebase or base switch occurred.
`docs/NATIVE60-1104-SHIP.md` is absent from this checkout and the adjacent window
checkout. The available `docs/NATIVE-RUNTIME-1106-REVIEW.md`, current desktop
documentation, main/desktop/input code, desktop-flow helper and its callers were
read. Prior pacing figures are retained context, not fresh measurements here.

## Source and cold build pins

All 193 tracked runtime/recomp/src files match the pinned base byte-for-byte.
The sorted JSON source-hash manifest has SHA256
`1194fadff816e7bbb6fca5bf7762d1a61db5e86c412d80f09387cc9c1d6b5572`.
No runtime, input semantics, caps, clock, fidelity, save behavior, golden or
Makefile changed. Existing Make command-line SDL overrides already work.
The post-link progress generator changed local metadata; its output was retained
privately and `progress.json` restored byte-for-byte from the pinned base.

The private ROM was read through an ignored symlink after checking ignore rules;
SHA1 is `4197339d4add74bb40ed02a8fba5e58096afb487`. No ROM was copied or rebuilt.
Only the configured `libsdl2-dev=2.30.0+dfsg-1ubuntu3.1` package was downloaded and
extracted with `dpkg-deb -x` into ignored `build/deps/sdl`. It matches the installed
SDL runtime package version. No OS package installation, dependency installation,
SDK build, sudo, service or global configuration change occurred.

Toolchain: GCC 13.3.0 (`13.3.0-6ubuntu2~24.04.1`), binutils 2.42, Python 3.12.3,
Make 4.3, SDL2 2.30.0. Generation and compilation were cold, using existing Python
and cc, nice 19 and make `-j1`. Runtime flags were
`-O2 -std=c11 -Wall -Wextra -Wno-misleading-indentation`; generated translation
keeps the existing trailing `-O1`. SDL flags were
`-Ibuild/deps/sdl/usr/include/SDL2 -Ibuild/deps/sdl/usr/include/x86_64-linux-gnu -D_REENTRANT`;
link input was the existing `/lib/x86_64-linux-gnu/libSDL2-2.0.so.0` explicitly.
No old object/executable was reused; the new executable is unstripped.

The build used these existing targets, with the SDL overrides above on both Make
invocations:

```
nice -n 19 make -j1 PYTHON=python3 build/generated.o
nice -n 19 make -j1 PYTHON=python3 \
  SDL_CFLAGS='-Ibuild/deps/sdl/usr/include/SDL2 -Ibuild/deps/sdl/usr/include/x86_64-linux-gnu -D_REENTRANT' \
  SDL_LIBS=/lib/x86_64-linux-gnu/libSDL2-2.0.so.0 \
  build/txra-pc build/desktop-test build/controller-test build/runtime-test
```

The actual window harness was launched as follows after creating the private
authorization directory. Race and rebinding runs use its `--scenario` and
`--profile` options, with separate review output paths.

```
WINDOW_OWNER_DISPLAY="${DISPLAY-}" nice -n 19 xvfb-run -a \
  -f "$PWD/build/window-xauth/auth" -e build/window-review/xvfb.log \
  -s '-screen 0 1024x768x24 -nolisten tcp' \
  sh -c 'export WINDOW_PRIVATE_X="$DISPLAY"; timeout 150s python3 tools/check_native_window.py'
```

| Artifact | SHA256 |
| --- | --- |
| Generated C | `d2ec9123b89460ede4168fa387677a89872370e62ea3b3f061e465b610f043c5` |
| Generated object | `97d2cd731564a067bcddefc85342b89834938be958a562e0cec5b36234381f59` |
| Native executable | `7e4bade876fbfab7b0393d98a0de565e72de0ef7892dc8e5aed5802938d9cfd9` |
| Downloaded development package | `8d78c93699aafdb33205ef7712baeefc8d8aa806862fac4c2554f3f8db234da1` |
| Installed SDL shared runtime | `2507acbbe40afe7d3e2e775dd8af00a1dba93579b9e837563032f3d751a9a45b` |

## Actual window and event evidence

`tools/check_native_window.py` uses installed libX11/libXtst through ctypes and
ffmpeg x11grab, with no browser or additional library. Before clients or injected
events, it rejects the owner display, checks the private display marker, Xvfb PID,
non-network server arguments and an authorization file under this build directory.
SDL uses x11/software/dummy audio with `--mute`. Data, settings and runtime paths
are isolated; session-manager, owner bus, accessibility and audio connections are
excluded. The installed Metacity runs only on that private server, without
compositing/session management, with in-memory settings and an unavailable private
bus address. No owner desktop was connected or manipulated.

The default client is 960x640. Its X11 minimum-size hint is 240x160, and an actual
120x80 resize request is clamped to that minimum by the private window manager.
At 800x600 the 720x480 integer-scaled image has 40-pixel side and 60-pixel vertical
borders. F11 enters 1024x768 fullscreen with a centered 960x640 image, then returns
to 800x600. Geometry is translated to root coordinates before each capture.
Five main pause pictures and two rebinding pause pictures compare every captured
RGB pixel against the F8 native screenshot plus the expected scaling/borders:
seven comparisons, zero mismatches. Nonblank checks also pass.

Actual XTest Escape pauses at guest frame 476 and resumes at the same frame;
the next pause is at frame 1014. Actual Up wraps to Quit and Return exits cleanly.
F8 and F11 also traverse actual SDL keyboard events. For rebinding, only the
private file's `key.start=Return` was changed to `key.start=Q`, then the executable
restarted using that same profile. Actual Q advances the title to name entry;
the file is unchanged after exit. There is no rebinding menu in the current
runtime, so this uses the documented file-edit/restart path. Guest saves and
existing keyboard/pad meanings were not changed.

Early capture failures were retained privately: the capture cursor caused 176
pixel mismatches, bare Xvfb did not provide fullscreen handling, and querying a
temporary SDL probe window caused an Xlib BadWindow. Cursor-free capture, the
private existing window manager, and waiting for completed renderer setup resolved
these harness/environment issues. No actual runtime defect was proved or hidden.
The final helper also converts Xlib errors into checked failures for cleanup.

## Regressions and guest output

Passed: 446 runtime assertions; controller ten-button/dead-zone/diagonal/disconnect/
reconnect checks; 69 desktop/audio assertions; 22 desktop-flow checks; five layout
selfchecks and two rejection checks that refuse unsafe display selections before
opening X11. Optimized Python is also rejected with exit 2 before creating output
or clients, and that refusal was tested. Existing desktop tests are counted
separately from actual window tests.

Two actual-window 4,300-frame race recordings and two fresh headless recordings
use the identical existing `tests/race-input.txt`. All four pass every current
framebuffer hash, PCM byte, final state, cycle and sample-clock golden. The second
pair was recorded to replace a sparse-timestamp video capture. No interpreter run
or full career rerun was needed because runtime source stayed byte-identical.
Each race ends with 229 compiled functions, 402,589,728 compiled steps, zero
fallback/unknown/unsupported, state `25ab436f`, 1,207,769,184 cycles, 2,358,924 audio
samples, audio hash `0cf1545835f3c205`, zero save writes and stopped=false.
Frame-hash-file SHA256:
`2d29524dda28a01c3ba9ada347575337a830eb9365e5639aa05bac6d99c77d7c`;
PCM SHA256: `2cad93185b65bb62cf97e3590e7f295a2cb30d51bd9ae6768e4fa38dbd8aba69`.

These are software-window correctness and fidelity checks, not new pacing
acceptance. No ten-minute backend pacing test was rerun. A process scan found no
live process whose working directory is the retained matching checkout; its files
were untouched and no fresh matching progress is claimed. An unrelated existing
renderer was consuming about one CPU core; its priority and state were untouched.

## Private review and cleanup

Final private review index: `build/native-window-1106/review/`. It contains
relative links, not duplicated movies, with NOTES.md and captions.json for all 14
entries. Key pictures: `default-paused.png`, `resized-letterbox.png`,
`minimum-paused.png`, `fullscreen-paused.png`, `quit-selected.png`,
`race-running.png`, and the rebound before/after pair. `menu.webm` and `race.webm`
are actual X11 window captures: each five seconds, 150 output frames, 30 fps, one
video stream and zero audio streams; sizes are 1,003,172 and 1,304,737 bytes.
Realtime encoding and constant output cadence replace the retained sparse initial
captures. Output cadence does not prove guest presentation timing.

All final pictures and five one-second samples from each clip were visually
inspected. Eleven native BMP screenshots and six final guest PPM pictures were
also inspected in contact sheets. Text and borders look complete at the tested
sizes. Existing guest visuals, HUD and route remain unchanged; no prior actual
window baseline existed to present as a before-fix capture. No vehicle/model or
world changes occurred. Media/frame/save/PCM/generated-C/executable/dependency
artifacts remain only under ignored private `build/`; none are committed/uploaded.

Owned runtime/window-manager/Xvfb PIDs are gone, and the final process scan finds
zero native/Xvfb/Metacity processes. Temporary authorization, profile, cache and
runtime paths are removed; generated binding/save/screenshot evidence is retained
under each run's `native-artifacts`, never in an owner profile. Exact PID checks,
removed paths, source/build/media hashes, counters and frame/window receipts are
in `docs/native-window-1106/evidence.json`; raw logs and source manifest stay
private. Disk remained at 77 GiB free, above the 20 GiB reserve.

`OWNER-NOTES.md` was absent initially, before expensive steps and at the final
check; no appended notes were available or skipped. Windows, physical keyboard/
controller hardware, accelerated GPU, real-display pacing and audible audio
quality remain held. No extra job or session, matching run, owner-process kill,
global service/audio change, push, merge, deployment or external publication occurred.

Helper commits: `08e2c36`, `eda54fb` (optimized-Python refusal). The following
evidence commit contains this report, numeric receipts and a completion
marker; `git log -3 --oneline` identifies all three.
Coordinator review/release is still required.
