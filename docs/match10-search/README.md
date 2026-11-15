# Round 10 persistent compiler search

Run `python tools/search10.py --seconds 1500 --count 15 --active-targets 5` using
the configured local Python environment. There is one fixed pool of five compiler
processes, launched with `nice -n 15`; workers enforce a minimum nice level
of 15. Up to five target windows compete for that pool.
Each target receives at least 1,500 seconds of elapsed search time, including
queueing for the shared pool, scoring, source generation and checkpoint IO.
This is wall time, not 25 minutes of exclusive use of five CPU cores per target.

The final target manifest selects all fifteen retained
unmatched, standalone entries that have a retained draft and score in the prior
near-miss, round-7 or round-9 folders. Historical angle 08014614, sibling
0801466C and packet 08014988 are already installed and excluded. Twelve remaining
additions in the earlier brief was a goal, not an identified twelve-function list.
All selected entries include their original score and draft path in targets.json.
The first twelve-target invocation was checkpointed and restarted with three
additional eligible drafts; resume-note.json records the accounting boundary.
Completed target windows were preserved. Unconsumed work is excluded.

The learned transformation table enters each neighborhood first, followed by
seeded shuffled declaration, arithmetic, cast, qualifier, scalar dependency-safe
order, temporary, pointer/index, pointer/offset, bitwise and control-flow forms.
Existing helpers can switch inline hints; local structs can swap fields. Reviewed
global layouts are never rewritten. Width, layout, qualifiers and signature
variants are hypotheses and need not preserve behavior. No approximate candidate
is safe to install. Every acceptance requires uncached full-extent comparison,
next-entry validation and a complete byte-identical ROM build.

Checkpoints retain the best source, diverse elite sources, current equal-score
walk, RNG state, context fingerprint and counters. Restart the same command to
finish remaining time. An interrupted speculative wave may be replayed: source
hash cache hits prevent recompilation. The queue is regenerated on restart;
resumption is deterministic from its saved RNG state, but not identical to an
uninterrupted queue traversal. Completed windows are skipped without compilation.
The cache is under build/, is never committed, and is invalidated by a hash of the
ROM, compiler/assembler tools, reviewed types, build config and search/judgment
implementation. Review output never contains cached binary results.

Per-entry result.json distinguishes observations (`attempts`, including repeats),
fresh source/profile compilations (`compiled`), cache hits, errors, restarts,
accepted equal-score moves and operators. Error counts include repeated cached
rejections. `variants_per_second` counts observations, not fresh compilations;
use `compiled / seconds` for fresh compilation throughput. Unique compiler output
counts are not inferred. history.jsonl records best score over time at roughly
30-second intervals and improvements. Scores are instruction-token Levenshtein
distance, then full byte distance. Constants, register operands and literal pools
participate. Only [0, 0] is exact. Full text diffs omit raw instruction encodings.

The private cache and checkpoints may be large. Only final sources, diffs,
result manifests and histories are retained as repository evidence. Checkpoints
remain gitignored in their target folders so the same checkout can resume them.
Keep those checkpoints and the private build cache when continuing a run. Logs, charts and a
muted metadata review clip are written to the requested review folder. Nothing
contacts the separately running matcher or a model service.
