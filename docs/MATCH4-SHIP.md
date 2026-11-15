# TXRA matching round 4 handoff — incomplete

**The fifty-function target is not achieved.** This pass installs **2 new complete
functions**, taking the total from **100 to 102**, and matched bytes from
**9,084 to 9,528**. That is **10.670% to 11.192%** of the unchanged 85,132 mapped
instruction bytes, including compiler pools and in-function alignment in the
numerator. **Forty-eight requested additions remain.** No near match or shared
fragment was counted as a replacement.

The accepted sources are the paired save unpacking and packing routines at
08013B38 and 08013C08, measuring 208 and 236 bytes. Both passed standalone
compiler comparison followed by a forced full rebuild ending in
`build/txra.gba: OK`. The final `make` also printed OK, and comparing the entire
rebuilt ROM with the private original passed. Existing save serialization bytes
are consequently unchanged; no new gameplay or save/reload session was run.
Historical runtime claims in progress metadata remain historical.

Accepted commits:

| Commit | Change |
| --- | --- |
| `0a6cc2d` | Two complete save routines; 102 accepted replacements |
| `be37a11` | Restore thirteen reviewed copy ranges and regenerate replacement assembly |
| `1ad8053` | Shared naming evidence, examples, ranking and retry feedback |

The handoff commit contains this note, the final ranking rejection hints and two
uninstalled continuation trials. Every commit uses the requested identity, with
no trailers. Nothing was pushed, deployed or merged. The handoff marker is
`MATCH4-DONE`; it marks the end of this work record, **not completion of the
fifty-addition target**.

The starting combined configuration had lost executable copy metadata already
present in the reviewed mapping. A forced analysis initially reduced its output
to 222 functions / 75,548 mapped instruction bytes. Restoring the thirteen
existing copy records makes analysis reproduce the reviewed 229 functions /
85,132 bytes. This restoration adds no matched functions or new coverage.
The independently reviewed indirect target at 080065CC is retained: the current
analyzer still loses that loop-derived target on regeneration, so that generated
metadata difference was not accepted.

`src/types.h` and `docs/MATCH4-LAYOUTS.md` establish evidence-backed names for
save staging, held keys, the OAM shadow, EEPROM geometry and sound voices.
Semantic aliases and address names resolve to identical locations. No function
was renamed from a behavioral guess. Car-state and physics field meanings still
need stronger agreement; these remain provisional.

There are 24 verified C examples with notes, up from 21. Hard-mode guidance now
emphasizes complete boundaries, access widths, stack layout and local edits.
Retry feedback identifies the first differing byte, exact prefix/suffix, length
changes and cases where only register choices differ. `tools/rank_targets.py`
reports value per estimated difficulty, optional smallest-first order, observed
entry evidence, static callers, matched callees and rejection hints for shared
epilogues or obvious non-argument register live-ins. Its linear register check
is a rejection aid, not a proof of control-flow dominance or ABI completeness.

The supplied coverage files do not contain per-function call counters. Dynamic
counts therefore remain explicitly unknown rather than being fabricated from
session totals. Future measured counts can be supplied through the documented
metadata field. The separately managed service checkout was neither accessed
nor modified. No service evaluation or updated success rate is claimed.

Validation:

- `make check`: **115 tests passed**, including recompilation of all 24 examples.
- Focused round-4 checks after the final ranking change: **6 tests passed**.
- Both new installations passed forced complete compiler/assembly/ROM rebuilds.
- Final `make`: `build/txra.gba: OK`; whole-ROM comparison passed.
- `git diff --check` passed. No ROM, extracted asset, binary or review image was
  added to version control.

Review folder: `txra-review/match4/`.

- `before/matching-status.png` and `after/matching-status.png`: same-view totals,
  showing 100/9,084 and 102/9,528.
- `matched-functions.png` and `matched-bytes.png`: accepted totals at actual
  commit times, generated only from our configuration and version history.
- `matching-progress.webm`: **6 seconds, 30 fps, muted, 301,396 bytes**. Opening,
  middle and closing frames were opened and inspected, as were all four final
  pictures. Text and totals are legible. No game visuals changed in this pass.

Every review picture folder has `NOTES.md` and `captions.json`; the root notes
explicitly state that forty-eight additions remain. No browser session was
needed for these metadata-only charts and clip.

Owner notes: `OWNER-NOTES.md` was absent at initial, major-step and final checks.
There were no appended owner requests to resolve or omit.

Unfinished work is substantial. The compiler differences in the other hand
trials were not solved, so only two additions were installed. The overlay trial
at 08014104 has matching instruction shapes and pools but ten differing bytes
from register choices; the reverse-copy trial at 080123F0 differs in fourteen
bytes over its 300-byte extent. These two sources and their limitations are
retained in `tools/trials/`, outside the build and few-shot directories. Other
local attempts included wrapped-angle differences, DMA queues, EEPROM transfer,
link packet handling and projection. None of those failed comparisons counts as
progress toward the remaining forty-eight additions.

Next work should resolve the close overlay/decoder allocation differences, then
continue the smallest complete observed entries and callers of recovered
routines. The remaining 127 mapped entries include fragments, veneers and ARM
routines that require separate treatment. No external blocker prevents further
matching; this handoff is an incomplete implementation of the requested target.
