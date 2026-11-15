# Optional native audio frame-event diagnostics

Base: `e9fe392b949e21650d7d9503da183ba8952f9b4e`.

`--frame-times` keeps its original eight CSV columns and appends:

| Column | Meaning |
| --- | --- |
| `audio_underruns` | Existing cumulative queue-zero diagnostic count after this frame's audio operation |
| `audio_underruns_delta` | Increase in that count during this frame's audio operation |
| `audio_backpressure_ms` | Increase in existing backpressure ticks during this frame, converted using the existing SDL performance-counter frequency |

The snapshots occur immediately before the existing audio operation and only
when timings are enabled. No audio structure, queue policy, queue polling,
device request, guest clock, deadline or audio implementation changes. All five
existing timing partitions retain their boundaries. The longer optional CSV
write remains part of the next frame's host/guest measurement, as before.

A queue-zero event identifies the frame where `audio_queue` observed an empty
queue after playback had started. It does not identify the exact instant the
device ran dry, establish an audible underrun, or prove the cause. Muted and
benchmark paths do not exercise normal playback merely by emitting zero counts.

`tools/report_pacing.py` accepts older three/eight-column recordings without
inventing event attribution. The three new columns are optional as a group;
partial columns, invalid counters, nonmonotonic totals, incoherent consecutive
deltas and nonfinite/negative waits are rejected. Waits must fit within their
measured audio phase, allowing the existing 0.00001 ms CSV rounding tolerance.

Each summary reports its observed queue-zero count/events and total measured
backpressure milliseconds. Event records include the original row and available
immediate frame neighbors with their phase columns. A partial or disjoint race
slice may start at a nonzero cumulative count; gaps do not manufacture events or
impose equality between a sampled frame's delta and an unsampled interval.
The complete-route CLI additionally checks the observed delta sum and final
cumulative count against `run.json`. A short reload with no selected race
section reports `race_sections: null`.

Validation: the focused reporter suite passes 13 tests, including existing
legacy/phase cases and new event/partial-slice/CLI rejection fixtures. The new
behavior was exercised against the prior reporter first and failed as expected.
The separately authorized runtime-only incremental build then passed on worker D,
reusing the pinned translation object with the original toolchain and all prior
files unchanged. A real PulseAudio run completed the original 37,200-frame
career and 2,200-frame reload with exact original frame, PCM, save, state,
cycle and sample goldens, plus the retained native PC/instruction references.
All source, binary, controller and mute-gate pins passed; the unique owned
physical audio stream was muted before playback and closed afterward. The
obtained format was 48,000 Hz with 480 device frames.

Both routes recorded zero queue-zero events and zero backpressure time. This
validates native CSV production and the zero-event path; positive native event
attribution remains unexercised. Synthetic event/parser regressions cover that
case but are not a real device-event observation. The measured whole-route
95th-percentile intervals were 16.768869 ms for career and 16.764913 ms for
reload; full numeric provenance is in `AUDIO-FRAME-EVENTS-1107-VALIDATION.json`.
These are existing-workload diagnostics with timing/capture overhead, not a
quiet paired performance comparison, new exact decomp match, speed improvement,
physical display/controller or audible-fidelity acceptance. The guest cadence
and queue policy remain unchanged; raw ROM, frames, PCM and saves stay on the
original host.
