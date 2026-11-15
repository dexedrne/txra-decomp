# Native runtime integration review handoff

The minimal integration builds cold from the exact parent
`ae40135a0dd438be489489d6f430739b5f2098a5` on `int/native-runtime-1106`;
`bb3934300f7a40b7e4a9c83920420b5404943746` is an ancestor. The stripped executable
matches the required SHA256 exactly:
`f826074ce8e8779f1215ffe0c6b90039376a5a4f0a62265039d650aa38571cbd`.
No runtime, guest semantics, clock, translation configuration or golden changed.
This is a source/fidelity handoff; pacing and platform acceptance remain held.

The parent already contains the 14 selected imported files. Its reviewed runtime
changes cover unsigned power-of-two timer prescalers, bounded audio-wait
measurements and frame CSV, complete input-reader validation, Windows SDL
initialization and existing-save replacement. Mutation/search tools were not
imported. This job adds one stdlib publishing test and an explicitly native-only
career helper. The original career checker still runs both native and reference;
its defaults and all existing callers remain unchanged.

## Cold build and provenance

The owner-supplied ROM was SHA1-verified against
`4197339d4add74bb40ed02a8fba5e58096afb487`. Ignore rules for `baserom.gba` and
`build/native-runtime-1106` were checked before creating the local ROM symlink.
There was no build directory at the start. The existing builder generated and
compiled translation from scratch, then linked runtime and published with
`strip --strip-debug`; no old object or executable was reused.

Reproduction, with the supported private ROM available as ignored `baserom.gba`:

```
nice -n 12 python3 tools/build_pc.py --output build/native-runtime-1106/release-pc
make check-runtime check-controller build/desktop-test check-mapping
./build/desktop-test
python3 tools/check_desktop_flow.py
python3 tools/check_accuracy.py --binary build/native-runtime-1106/release-pc
python3 -m unittest discover -s tests -p test_build_pc.py -v
nice -n 12 python3 tools/check_native_career.py build/native-runtime-1106/full --binary build/native-runtime-1106/release-pc
```

Choose a fresh private career output folder for each replay. All game invocations
used headless, app-only mute and benchmark mode. No interpreter replay was
launched; the current recorded interpreter/reference goldens are the comparison
reference. This helper does not assert that a fresh reference run occurred and
refuses optimized Python, which would disable its assertions.

`native-runtime-1106/build-evidence.json` records exact flags, tool versions and
source/build hashes. Generated C SHA256:
`d2ec9123b89460ede4168fa387677a89872370e62ea3b3f061e465b610f043c5`.
Fresh generated object SHA256:
`75f29e2c544984a04fdd60e878d509d841f1198b8060bf570010b02fb93f46d5`.
Compiler: GCC 16.2.1; binutils 2.47; SDL2 2.32.74; Python 3.14.8; Make 4.4.1.
The generated unit uses the existing trailing `-O1`; runtime uses existing `-O2`.

All 14 selected imports match `import-provenance.json`. All 193 tracked files
under runtime/recomp/src match the pinned parent, individually hashed in
`source-manifest.json`. All 1,221 original parent files were verified unchanged
before writing this final note; a complete manifest is private in
`build/native-runtime-1106/parent-files.json`. The older verified commit object
is absent in this checkout, so this job independently verifies the imported
hashes and exact parent, and retains the coordinator's prior whole-source proof
without claiming to have repeated an unavailable historical-tree comparison.

The existing Makefile invokes `tools/progress.py` after linking. Its cold-build
output rewrote progress metadata because local analysis/milestone artifacts were
absent. That output is retained privately as `build-progress.json`; tracked
`progress.json` was restored byte-for-byte from the pinned parent. Matching,
discovery, original source and progress are unchanged.

## Verification

Focused results: 446 runtime/timer assertions; controller buttons, dead zone,
diagonal, disconnect and reconnect; 69 desktop/audio assertions; 22 desktop-flow
checks; 15 mapping tests; 4,300-frame accuracy matching every framebuffer hash,
PCM byte, state, cycle and sample clock; six input-reader capacity/rejection
boundaries. No assertion or test was disabled, and no broad CPU/performance stack
was rerun.

The new publishing test passes three failure boundaries: partial copy, partial
strip and final replacement failure. Each preserves the existing destination's
bytes and mode and removes only the owned temporary file. Successful same-path
publication preserves bytes and mode; an unrelated similarly named temporary
file survives all cases. One unittest covers these four scenarios. The
native-only helper also refuses `python -O` before creating output or spawning.

Full fresh native career/reload results and numeric counters are recorded in
`native-runtime-1106/verification.json`. Raw frame hashes, PCM, stats, logs,
unknown logs and EEPROM remain private under `build/native-runtime-1106/full`.
The fresh 37,200-frame career and 2,200-frame reload pass every current golden,
including zero fallback/unknown/unsupported and 229 compiled functions. Career
ends at state `9cb2d661`, 10,449,247,680 cycles, 20,408,686 samples and
3,483,082,560 compiled steps. Reload ends at state `fc469aac`, 617,887,584 cycles
and 1,206,811 samples, with zero save writes and unchanged EEPROM. Complete
frame/PCM/save SHA256 values are in the verification evidence. No previous run
substitutes for these fresh recordings.

## Pictures and clips

Private review folder: `build/native-runtime-1106/review/`. `NOTES.md` and
`captions.json` describe every picture and clip. Key pictures are
`before-menu.png`, `after-menu.png`, `before-race.png`, `after-race.png`.
Both same-view pairs are pixel-identical. Baseline pictures/clips are read-only
relative links to existing private artifacts; fresh after captures use this
job's cold-built executable.

Two new eight-second muted WebM clips show menu motion and racing at 30 fps;
each is below 1 MB. The two existing baseline clips are linked rather than
copied. All four are below 4 MB and contain zero audio streams. All fourteen
snapshots were inspected in the sequence sheet, all four key pictures were
inspected, and all four clips' one-second sample sheets were inspected.
`native-runtime-1106/review-evidence.json` records hashes, sizes and inspection
counts. The clips reconstruct captured guest frames at the original intended
speed; they are not presentation-timing evidence. The clipped left money label
and scripted route traffic contacts remain visible. No graphical or guest
behavior change was made to conceal them. No world or vehicle-model work occurred.

## Holds and owner notes

No new paced measurements, fixed-cadence acceptance or performance gain is
claimed. Original 59.72750056960583 Hz semantics are intact. Physical controller,
audible output, visible-window presentation, hardware audio fidelity and Windows
acceptance remain unverified. Neither a Windows compiler nor an SDK is available
locally; no packages were installed and no cross-build is claimed.

`OWNER-NOTES.md` was absent at initial and major-step checks; no appended notes
were available to resolve. It was also absent at the final check; there are no unresolved appended notes.
The prior native pacing report and original recordings/builds were read-only.
No browser, extra session, remote job, API spend, global audio change,
other-process kill/priority change, push, deployment, stash, reset, rebase or main
merge occurred. CPU-heavy commands used nice 12. Disk stayed above the 20 GiB
reserve; no owner data was deleted. ROM, EEPROM, PCM, generated translation,
executables and media remain ignored and are not committed or uploaded.

Implementation/test commit: `6037d76`.
The following evidence commit contains this note and `NATIVE-RUNTIME-1106-DONE`;
`git log -2 --oneline` identifies both. The marker means review handoff only;
coordinator review and merge are still required.
