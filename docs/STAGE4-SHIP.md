# Stage 4 ship note

The local matching loop selects candidate THUMB functions, asks the configured
local service for C, compiles it with the matching compiler, compares bytes and
rebuilds the whole ROM before retaining a replacement. It can run continuously,
waits during outages or while an unrelated model is loaded, and writes status and
logs under the ignored build directory. Fake-model runs use separate status.
Implementation commit: df6059c. The ship note and marker are in the following
commit.

There are still four matched C functions, totaling 54 bytes including pools and
alignment, approximately 0.063% of mapped instruction bytes. The service refused
connections throughout this job, including the last check. The real loop entered
its retry wait; zero real guesses were made, so its success rate is not yet
measurable and there are no new matches or naming proposals. The ROM was copied
locally and remains ignored.

`make check` passed 10 tests, including four loop tests, and the full ROM SHA-1
check passed. There are no new pictures or clips: this job changes an offline
matching tool and did not change visible game behavior.

Remaining work: exercise the loop against the live service and inspect resulting
matches; external-call relocations are currently rejected, so such functions cannot
yet be matched. Semantic names are only proposed for manual evidence review, not
applied automatically. The candidate-boundary and coverage measurements are
inferred, and the percentage includes pools in its numerator. A process can be
started with `python3 tools/llm_match.py --forever`; it was not left running.

Owner notes: `OWNER-NOTES.md` was absent on every check, including the final
check, so no additional notes were received.
