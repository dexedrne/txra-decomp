# Native frame-phase diagnostic — integrated; pacing remains unresolved

This diagnostic was developed from `0af329d308d23d6389902e3b595b6fcd2cd5f813`.
It adds attribution to the existing optional `--frame-times` recording so the
next paced run can distinguish emulation/host work, presentation, capture I/O,
audio queuing and deadline waiting. It does not fix or establish the cause of
previous long frames or audio queue-zero events. No new performance result,
matching C function, game-clock change or release is claimed.

The existing first three CSV columns remain `frame,interval_ms,work_ms`.
Five columns are appended:

| Column | Wall time measured |
| --- | --- |
| `host_guest_ms` | Previous frame end through host input, emulation and periodic save flushing; includes the previous timing-row write. |
| `present_ms` | Pixel preparation and the existing presentation call; this is not a GPU-only timer. |
| `capture_ms` | Optional video/PCM/frame-hash/snapshot output after presentation. |
| `audio_ms` | The existing audio queue operation, including any queue backpressure wait. |
| `pace_ms` | The existing frame-deadline wait. |

The first four phases sum to `work_ms`; all five sum to `interval_ms`.
Paused/menu time belongs to the host/guest bucket rather than a guest CPU claim.
The three added counter reads occur only when `--frame-times` is requested.
Normal playback requests no additional clock reads. Guest clocks, mixer,
queue policy, deadline arithmetic, inputs, saves and original 59.72750057 Hz
cadence are unchanged by the patch.

`tools/report_pacing.py` retains legacy three-column reports and leaves those
recordings unattributed. New complete phase captures gain per-phase p50/p95
values under `phase_ms`. Partial phases, nonfinite/negative values and phase
sums inconsistent with recorded work/frame totals are rejected. The 0.00001 ms
partition tolerance accounts for the runtime's six-decimal CSV rounding; it
is not a performance allowance.

Validation so far:

- Five reporter unit tests pass, including legacy, audio attribution, missing
  phases, invalid values, inconsistent sums and nonfinite totals. New behavior
  failed against the old reporter before implementation.
- Strict C11 syntax/format checks pass with `-Wall -Wextra -Werror` and the
  installed SDL2 headers; no ROM is needed for this check.
- Independent review found no blocking issue and independently passed the
  initial four reporter tests. Root's final five-test run also passes.

The incremental private build now passes both untimed and timed 4,300-frame
accuracy runs, all 4,300 phase partitions, six input-reader boundaries, and the
complete 37,200-frame career plus 2,200-frame reload goldens. Every frame hash,
PCM byte, guest state/clock and save matches; compiled functions remain 229
with zero fallback, unknown or unsupported operations. The binary SHA-256 is
`e16b036ca079b0c4fe345ccb3cd4bb24cbc70e5ffe267d804eaeb1aac6d8e76f`.
The already verified generated object was reused after source/header/object
hash checks; this is explicitly not a cold build. Numeric provenance is in
`FRAME-PHASE-TIMING-1106.json`.

Next, record real-backend phase CSVs with the original input sequence and a
separate output folder. A real-backend
run must retain exact app-stream identity/mute checks throughout; adapt the
existing pinned controller to the reviewed new source/binary explicitly rather
than bypassing its provenance guard. Keep ROM, generated translation,
executables, EEPROM, raw frames and PCM private on their authorized hosts.

Worker E was saturated by its existing local model and browser. The correctness
runs used headless, mute and uncapped benchmark mode at nice 19; they are not
comparable speed measurements. No new model job was started. A quieter paced
recording is still required. Optional timing adds measurement overhead, so compare
instrumented captures consistently and do not present them as unchanged-binary
or uninstrumented performance evidence. Those correctness runs alone did not establish paced or physical-platform acceptance. The later measurements below add diagnostic evidence, without establishing a jitter or audible-quality fix.


## Real-backend diagnostic completed on worker D

The new worker D incremental build is `4e4614ba22a64b1f1299b1e779eae3e9940bfcd0604dd4804a5c87bfd3f46f3a`, from the same reviewed runtime. It reused worker D's verified translation object with GCC16.2.1; it is a separate binary from worker E's build. Invalid source and binary pins both refused playback. The actual new binary first passed the original full native career/reload and six input-reader checks in benchmark/mute mode.

Real PulseAudio playback then passed all original 37,200-frame career and 2,200-frame reload frame hashes, PCM bytes, saves, guest state/clocks/samples and native counters. The controller verified the unique app stream/PID, physical ALSA sink and app-only mute before gate release, throughout each run and after stream closure. There were 616 career and 36 reload mute observations. No global audio settings changed; raw outputs remain on worker D.

Career averaged 59.7266926773 fps against the original 59.72750057 Hz clock. It still had one queue-zero diagnostic and a 21.478374 ms frame-interval p95. Reload averaged 59.7257134617 fps with zero queue-zero diagnostics. These nice10, headless, instrumented runs under existing host workload are diagnostics, not a quiet paired speed comparison, audible acceptance or a new matching function. Counts remain 179 C matches / 229 compiled functions.

The career's individual phase p95s were host/guest 9.953970 ms, presentation 2.157308 ms, capture 0.261297 ms, audio 13.506512 ms and pacing 9.854419 ms. Independent percentiles must not be added. Some long frames spent time in host/guest work and others in audio queuing; the data does not establish a single cause or an audio fix. The exact numeric receipts and longest-frame breakdown are in `FRAME-PHASE-TIMING-1106-AUDIO.json`.

The remaining work is to reduce frame-time jitter and understand the queue-zero event through controlled comparisons, then check audible fidelity and physical input/display/platform behavior. Main was unchanged at that measurement point. The original clock remains unchanged; no sample dropping, resampler change or queue-policy relaxation is included here.


## Diagnostic integration, November 7

The optional timing feature is integrated after independent review and fresh
validation of the exact3c4 runtime/tools/tests source shared with4727. The
matching build reproduced the original ROM byte-for-byte. The complete Python
suite ran183 tests:182passed and one search-resume fixture skipped because
fewer than two unmatched retained drafts were available. All446 runtime
assertions and the controller mapping/dead-zone/disconnect checks passed.
Five reporter tests and strict C11 warnings-as-errors checks also passed.
Numeric receipts and log hashes are in FRAME-PHASE-TIMING-1107-INTEGRATION.json.
The isolated test checkout was removed; its borrowed private ROM remained on
worker D. A generated indirect-map delta from tests was preserved there and was
excluded from this integration. No external model or API job was started.

This integrates diagnostics rather than a performance or audio-policy change.
The480-frame device request and original59.72750057Hz clock remain unchanged;
no128-frame experiment is included. Matching C remains179/229. Existing native
career/reload, frame/PCM/save/clock and physical-backend app-stream evidence
supports correctness. Jitter, audible fidelity, physical display/controller and
Windows acceptance remain outstanding. No executable release was published.
