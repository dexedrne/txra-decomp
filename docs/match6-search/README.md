# Round 6 compiler trials

Only complete byte equality followed by a forced full build counts as acceptance.
The accepted functions are 08018B24 (176 bytes, standard-o1) and 0801466C
(136 bytes, old). The final installed sources are in src/generated/.

`expanded/search-results.json` records the completed 2,500-trial-per-entry pass
through eligible entries with at most 120 instructions, plus explicit rejections.
It ran before the new sources were installed; its old EEPROM and link misses
are superseded by the installed results. `angle-unsigned/search-results.json`
is a completed 6,000-trial pass from a hand-written signed-comparison seed.
`packet-focused-final/search-results.json` is the completed focused packet pass.
The two earlier packet-focused folders were interrupted while generating
neighborhoods; they provide retained drafts only, with no counted attempt total.
The EEPROM pass also has a completed manifest when present.

Manual experiment JSON files record `total_jobs`, meaning the size of the
planned source/profile grid. This is not a measured compilation count: exact
matches stop result consumption early. No aggregate attempt count is inferred
from those fields. Compiler flag grids contain one record per measured trial;
unsupported flags are errors, not mismatches. None of the extra flags matched,
and the build's five existing profiles remain unchanged.

The manual grids covered initializer/declaration permutations, register hints,
scalar widths, signed/unsigned arithmetic domains, conditional assignments,
pointer versus integer cursors, statement order, scoped constants, and inline
checksum helpers. Some hypotheses do not preserve behavior; these drafts must
not be installed without the full equality gate. Diff text omits instruction
encodings and no binary ROM slices are retained. The learned transformation
table lives in tools/matching_patterns.json and references accepted sources.
