# TXRA matching round 3

The requested forty new complete C matches are installed: **60 → 100 functions**,
**2,884 → 9,084 bytes**, a gain of **6,200 bytes** including literal pools and
in-function alignment. Every installation passed a forced complete rebuild with
`build/txra.gba: OK`. No prefixes, shared epilogues, instruction arrays or patched
compiler output were counted. Small unmatched entries were inspected first;
fragments were left for recovery with their enclosing routines. Later work
included callers of the newly matched search and transfer routines.

The new replacements cover table and record access, signed arithmetic, transfers,
retry wrappers, slot selection, glyph/image work, a text descriptor, and frame/reset
handling. `src/types.h` centralizes recovered layouts with offset field names;
`docs/MATCH3-LAYOUTS.md` records the access-width and stride evidence. Function
names remain address-based because no new behavior name passed the two-call-site
threshold. Existing ROM behavior and save bytes are preserved by full ROM identity.

The matching workflow now has 21 reviewed C examples with notes, selects up to six
nearby or related examples per prompt, and retains the closest compiled attempt
when a retry regresses. Prompts include shared layouts and matched callee
signatures. `--hard` selects complete functions with 8–40 decoded instructions and
bypasses the deterministic pass. Its read-only dry run was checked with a fake
responder; no new service success-rate benchmark is claimed. The separately running
service checkout was neither changed nor stopped, and historical service statistics
were retained.

Two recorded compiler choices supplement the default. The 72-byte EEPROM selector
uses the installed standard variant. The 88-byte clear loop uses the default
compiler with `-fno-gcse`, which prevents pointer increments from moving before the
inner loop. Both choices are verified in the trial judge, the full build and tests;
they do not prove the original vendor compiler settings.

Accepted batches:

| Commit | New functions | Resulting total |
| --- | ---: | ---: |
| `9fb54a4` | 5 | 65 |
| `4b0c429` | 14 | 79 |
| `bfa5431` | 6 | 85 |
| `e94e1f7` | 9 | 94 |
| `7d949a5` | 6 | 100 |

All commits use the requested identity. Nothing was pushed or deployed, and no
branch was merged. No ROM, extracted asset, generated binary or review image was
committed.

Validation: `make check` passed **109 tests**, including independent recompilation
of all 21 curated examples, relocations, retry feedback, hard-mode selection and
compiler choices. A focused rerun passed **19 tests**. The final `make` printed
`build/txra.gba: OK`, and `cmp baserom.gba build/txra.gba` passed. `git diff --check`
passed. No new gameplay or save/reload session was run; the historical runtime
claims in progress metadata remain historical, with this pass establishing ROM
identity.

Review folder: `txra-review/match3/`.

- `before/matching-status.png` and `after/matching-status.png`: the same view at
  60/2,884 and 100/9,084.
- `matched-functions.png` and `matched-bytes.png`: accepted batches at actual
  commit times, generated only from our configuration and progress metadata.
- `matching-progress.webm`: six seconds, muted, 30 fps, 423,012 bytes, showing the
  accepted replacement milestones.

Every picture folder has `NOTES.md` and `captions.json`. All four final pictures
were opened and inspected for legibility and correct totals. The clip's opening,
middle and closing frames were also inspected. This task changed no game visuals;
the review shows tool output only.

Owner notes: `OWNER-NOTES.md` was absent at the initial read and each subsequent
checkpoint, including the final check. No appended owner requests were skipped.

Remaining work: 129 mapped function candidates are not yet C matches; this count
includes fragments that are not independent routines. Several communication/save
layouts remain provisional and their routines remain unmatched. No live evaluation
of the updated service loop was run. Next work should continue with the remaining
small standalone routines, then their callers, preserving complete ROM identity.
