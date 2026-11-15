# Round 5 search record

`summary.json` aggregates eight retained passes: 143,895 compiler trials,
including 55,960 compilation failures. These are source/profile trials, not a
count of distinct assembly outputs or functions. Early prototype experiments
without a retained manifest are excluded; no matching-speed benchmark is claimed.
Each manifest records its actual bounded attempt count, errors, best distances
and ranked rejection reasons. Later passes revisit previous targets.

The baseline has nineteen unmatched mapped entries with 8–60 instructions.
Six pass the standalone THUMB checks; all six were compiled in rank order.
Thirteen are rejected before compilation, with diagnostic C and rejection text
under `docs/near-misses/rejected/`. Later passes revisit all five still-unmatched
standalone candidates. Workers use all twelve cores at positive nice priority;
the final tool selects nice 10 explicitly. No external model service is used.

The only accepted result is 08018AA4: 128 bytes using `standard-o1`. It passed
an uncached standalone comparison, the forced full build and complete ROM
identity. `accepted-08018AA4.diff.txt` is an exact comparison, not a near miss.
Raw instruction encodings and ROM slices are excluded from these records.

Resume with `python3 tools/variant_search.py ADDRESS docs/near-misses/func_ADDRESS.c`.
Select `--output build/search-next` to keep a new pass separate. `--install`
requires the final uncached comparison with the next-entry boundary, followed
by the existing forced full-build gate. The optional compiler-output cache is
local to a worker with a fixed ROM/symbol snapshot; it cannot bypass installation.
