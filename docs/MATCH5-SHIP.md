# TXRA matching round 5 — target incomplete

**One new complete match, not forty.** The total moves from **102 to 103
functions**, from **9,528 to 9,656 matched bytes**, and from **11.192% to 11.342%**
of the unchanged 85,132 mapped instruction bytes. Literal pools and in-function
alignment remain included in the numerator. **Thirty-nine requested additions
remain.** No failed draft, partial body or shared epilogue counts as a match.

The accepted routine is the EEPROM DMA transfer at **08018AA4**, all **128 bytes**.
Its ordinary C matches with the standard compiler at `-O1 -mthumb-interwork`.
The default `-O2` does not match this draft. The source passed standalone byte
comparison, the installation's forced full rebuild, another build after formatting,
and complete comparison of the rebuilt ROM with the private original. This is
matching evidence for the recorded profile, not proof of the original vendor flags.

Implementation commits:

- `5e1baa9` — ranked compiler variant search and the exact EEPROM replacement.
- `25dd2b4` — bounded escapes, compiler-output reuse, source variants and review charts.
- The handoff commit containing this note retains the final signature search,
  continuation drafts, all search manifests and completion marker.

All commits use the requested identity and have no trailers. Nothing was pushed,
deployed or merged. The pre-existing untracked package lock is left alone.

## Method and measured result

`tools/variant_search.py` replaces individual source guesses with reproducible
compiler neighborhoods, instruction-level Levenshtein scoring, byte-distance
tie breaking, a diverse retained beam and bounded multi-edit escapes. It explores
statement and declaration order, initialized and separate declarations, scalar
widths and casts, register hints, parameter order hypotheses, supported loop
forms, pointer/index expressions, early-return shape, arithmetic operand order,
constant spellings, compound assignment and IO volatility. The final uncached
byte comparison protects the original calling convention and next-entry boundary.
The profiles cover old/standard `-O2`, old `-O2 -fno-gcse`, and old/standard `-O1`.
The shared build path honors the accepted profile; no compiler output is patched.

All twelve cores are used for compilation, with positive nice priority. The final
tool sets nice 10 explicitly. Targets are visited in ranking order, with each
function's variants compiled in parallel. The optional cache only reuses identical
emitted function assembly inside a worker with fixed ROM/symbol snapshots; the
installation gate remains uncached. The separately running model loop and its
service checkout were not accessed or changed; no service calls were made.

Eight retained passes account for **143,895 source/profile trials**, including
**55,960 compilation failures**. Trials are not distinct assembly outputs, and
repeat passes revisit functions. Early prototype trials without retained
manifests are excluded from that total. The search is bounded and syntactic,
not an exhaustive proof that the remaining functions cannot match.

The baseline ranking has **19 unmatched entries with 8–60 instructions**, of
which **6** pass the standalone THUMB checks. Every one of those six was searched;
all five still-unmatched valid candidates received the later 15,000-trial pass.
The other thirteen have explicit rejection records: two shared epilogues, two
incomplete mapped bodies, two internal mixer fragments, six ARM entries requiring
a separate compiler path, and a runtime helper. Forty additions cannot come from
this fixed selection alone. This is a scope constraint, not an external blocker
or a claim that the broader decompilation is finished.

The best surviving drafts and complete diffs are in `docs/near-misses/`:

| Entry | Instruction distance | Byte distance | Remaining issue |
| --- | ---: | ---: | --- |
| 08014614 | 4 | 11 | Return narrowing adds four bytes and crosses the next entry |
| 08015DA8 | 25 | 60 | Queue allocation and code shape still differ |
| 08014104 | 6 | 10 | Register choices and initialization order |
| 08014988 | 12 | 50 | Packet tail and loop setup differ |
| 0801466C | 6 | 10 | Register choices and initialization order |

These are uninstalled hypotheses; some type variants change behavior and must
not be treated as usable replacements. The thirteen rejected entries retain
explicitly diagnostic lifted C plus rejection text, rather than invented compiler
diffs. `docs/match5-search/summary.json` and the per-pass manifests record all
retained attempt counts and profiles. Diff files contain instruction text and
constants, with raw instruction encodings removed; no ROM slices are stored.

## Build, metadata and validation

The baseline `make` passed. No previous-merge build fix was needed. Mapping and
copy metadata are unchanged. Analysis can regenerate an older indirect resolver's
output; the reviewed indirect metadata was retained verbatim rather than landed.
The tool now preserves reviewed mapping files across its installation build.

- `make check`: **126 tests passed**.
- After the final parameter-order extension: **11 focused search tests passed**.
- Tests cover instruction edit distance, complete pool extent, exact versus
  wrong compiler profile, declaration/initializer variants, guarded loop forms,
  signature variants, all supported profiles and compiler-output cache reuse.
- The accepted function passed the forced full build; final `make` printed OK.
- Whole-ROM comparison passed; no ROM, extracted asset or generated binary is committed.
- Configuration outside the replacement list and all reviewed mapping files are unchanged.
- `git diff --check` passed.

The ROM is supplied through the required gitignored root symlink. Existing
execution claims in `progress.json` remain historical: no new gameplay, race or
save/reload session is claimed. Byte identity preserves the existing ROM behavior.

## Owner review

Review folder: `txra-review/match5/`.

- `before/matching-status.png` and `after/matching-status.png`: same-view totals.
- `matched-functions.png`, `matched-percent.png` and `matched-bytes.png`: actual
  accepted commit times, with unchanged denominator and zero-based axes.
- `matching-progress.webm`: **6 seconds, 30 fps, muted, 297,120 bytes**.

All five pictures and opening/middle/closing clip frames were opened and inspected.
The text and totals are legible and fit. Every picture folder has `NOTES.md` and
`captions.json`; root notes explicitly state one of forty additions is complete.
Only our configuration, progress and version-history output appears in these
charts and clip. No game visuals changed, and no browser capture was needed.

`OWNER-NOTES.md` was absent at initial, major-step and final checks. There were
no appended owner notes to apply or omit. `MATCH5-DONE` marks this handoff;
it does not declare the forty-addition target complete.

Next, remove the remaining allocation differences in the two six-instruction
misses and the angle return, then broaden the function-size range using the same
unchanged mapping. Better seed control flow is still needed for queue and packet
code. A separate ARM compiler path is also unfinished.

Matched before/after: 102 / 103.
Percent before/after: 11.192% / 11.342%.
Next: resolve the retained near misses and expand the eligible size range; 39 additions remain.
