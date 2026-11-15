# ROM mapping round 3 handoff

Implementation commit: `f37f40c` — structural classifiers, checked decoders,
additional coverage inputs, per-range evidence, exact progress and review tools.
The following handoff commit adds this note and `MAP3-DONE`. Nothing was pushed,
deployed, merged or stashed.

Unknown bytes fell from **2,773,133 to 723,196**, a reduction of 2,049,937.
The ROM is **82.76% classified**, up from 33.88%. Mapped code remains 85,132
bytes; data including fill rises from 1,336,039 to 3,385,976 bytes. Function
candidates and recompiled functions remain 229 (205 THUMB, 24 ARM).
`progress.json` retains exactly the previous keys and verified milestone values.

New proofs cover six course arrays with explicit counts and a 28-byte stride,
a complete signed reciprocal projection lookup, fourteen linear indexed texture
banks, twenty-four reverse LZ/RLE containers and twenty-three attached palettes.
Every new range has an evidence line in `docs/map/structures.json`, including
consumer sites, sizes and dimensions or counts. All compressed blocks include
both source size and decoded size. The final nonoverlapping partition and its
format evidence lines are in `tools/rom.cfg`; structures may overlap in the
proof inventory but never inflate the partition counts.

The custom decoder follows 0801251C's literal, repeat, forward-copy and
backward-copy commands. Bounds, initialized output reads and exact ends are
checked. Independent guest CPU execution matches the complete output hash of
all 24 blocks. BIOS LZ77, RLE and both Huffman widths now also have decoded-output
tests; no valid referenced BIOS container was established in this cartridge.
No extracted output, ROM imagery, ROM file, sample or tile data is committed.
The worktree initially lacked its private base ROM; the existing local private
copy was linked into the ignored base-ROM path.

Eleven coverage sessions combine the original six routes with three course
selector probes and two pause-menu probes. The new paths add 206 executed PCs
and 12,643 ROM-read bytes over round 2. Aggregate coverage is 23,523 unique PCs,
928,576 read bytes and zero logger overflow. Full-ROM pointer scanning and
recursive descent still produce 229 candidates and 85,132 code bytes: no new
function was validated. After accounting for copied RAM aliases, 63 candidate
function entries remain unexecuted; the exact list and per-session deltas are
in `docs/map/round3-audit.json`.

Validation:

- `make check`: 34 Python tests pass, including eight structural tests and
  fifteen mapping/logger tests. The final decoder boundary adjustment was
  rechecked with all eight structural tests and all 24 guest comparisons.
- `make`: supported SHA-1 passes; rebuilt ROM and private base compare identical.
- `make recomp`: 229 functions and 260 load/run entries. The final executable's
  hash matches the executable used for the final race and save/reload checks.
- Full 12,500-frame race: 1,170,372,096 native instructions, zero fallback,
  unknown targets or unsupported instructions. All 12,500 frame hashes match
  the round 2 race. All eleven recorded sessions have zero execution failures.
- Runtime checks: 118 assertions pass. Controller checks cover ten buttons,
  dead zone, diagonals, disconnect and reconnect.
- Fresh isolated save/reload: save writes occur; reload writes none and preserves
  the complete save-file hash. Existing saves were not modified.
- Progress-key equality, partition counts, caption completeness and whitespace
  checks pass. The last recursive descent again reports 37,483 instructions,
  229 candidates and eleven unresolved indirect sites.

Review folder: `txra-review/map3/`.

- `before/rom-heat-strip.png` and `after/rom-heat-strip.png`: the same full-ROM
  viewpoint, comparing the round 2 classification with round 3.
- `mapped-progress.png`: exact code/data/fill/unknown percentages before and after.
- `map-progress.webm`: muted VP9 metadata wipe, six seconds, 30 fps, 453,248 bytes.
- All three final pictures and six clip contact frames were visually inspected.
  A clipped subtitle was shortened before the final render. Every media folder
  has plain notes and complete captions. These pictures contain our tools only.

What is not done: 723,196 bytes remain unknown. Smaller graphics and layout
structures, narrow texture sources, auxiliary course records and sound sequence
or instrument formats still lack proven bounds or consumers. The normal-input
selector probes did not start another course; they remain on the selector
screen. The pause probes did not enter replay. Alternate course starts,
advanced career progression, part purchases, full results branches and replay
remain unverified, including entry points 08012CC8 and 08012EB8. No unlock flag,
ROM or save was patched to manufacture reach. No new OAM layout, note format or
4bpp tile ordering was proven. Broader routing and instruction semantics remain
necessary; the unknown bytes were not relabeled to meet a percentage target.

Owner notes: `OWNER-NOTES.md` was absent at the initial read, major-step checks
and final handoff. There were no appended notes to resolve. The requested
pictures, muted review clip, notes, captions and private-ROM handling are done.
No browser or other machine was used. Vehicle rollers and long drive footage
are not applicable to this metadata-only ROM mapping change.
