# Seventh matching pass: measured experiments

Three exact replacements were installed: 08014614 (88 bytes), 0801251C
(226 bytes), and 080123F0 (300 bytes). Each uses the existing old profile.
The fifteen-addition target remains incomplete, with twelve additions left.

summary.json is the aggregate source of counts. It includes 138,476 consumed
source/profile results, of which 14,893 failed compilation or judgment, and
2,408 alternate-flag trials, of which 880 failed compilation or judgment.
Repeated sources and profiles count as repeated trials, not unique assembly.
The three one-trial installation checks have their own manifest entries.
Compilation of a speculative parallel wave may finish additional results that
were not consumed after finding a winner; those are not counted.

The expanded batch finalized 46 entries: 21 eligible standalone entries through
160 instructions and 25 explicit rejections. Its first invocation ended with
signal 15 after 16 finalized entries; the cause was not established. The resumed
invocation preserved those entries and finalized the rest. Unfinished work from
the first invocation is excluded. The decoder loop, decoder split, and first
queue-focused passes were interrupted after their purpose was superseded or
their neighborhood generation stalled; their surviving drafts carry no claimed
trial count. No missing manifest is interpreted as a successful comparison.

The hand-designed grids are reproducible through tools/targeted_search7.py.
The flag grids use tools/flag_search7.py. Paths name the operation or target;
results.json records consumed attempts, planned jobs, errors, best score and
profile. queue_address-declaration-rejected preserves the initial all-rejected
grid; the corrected block-scoped grid is retained separately. No extra compiler
profile found an exact match, and the five build profiles remain unchanged.

The expanded and focused passes use tools/variant_search.py. --focus narrows
mutable statements, --seconds bounds each target, and --resume skips finalized
manifest entries. The final queue-focused pass retained its eleven-instruction
miss at the sixty-second limit. The smaller original queue miss relied on an
incorrectly narrowed source. The retained word-width replacement hypothesis now
has the correct complete extent and instruction shapes, but is not installed.

All accepted results passed uncached next-entry and complete-byte checks, a
forced full rebuild, and comparison of the whole rebuilt ROM. Sources and text
diffs here are hypotheses unless marked exact and installed. Instruction words,
binary ROM slices, extracted assets and build binaries are not retained here.
