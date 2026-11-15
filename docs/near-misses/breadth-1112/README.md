# Small function recovery, 12 November

Eight independently reviewed functions were discovered in unclassified gaps and installed only after complete compiler-byte equality and a forced whole-ROM rebuild. The three excluded large owners were not edited. No runtime execution is claimed for the new routines.

| Address | Complete bytes | First C byte diff | Final byte diff | Commit |
| --- | ---: | ---: | ---: | --- |
| 0800753C | 24 | 0 | 0 | 96c7c8f |
| 08014790 | 48 | 0 | 0 | 16176f9 |
| 080075DC | 64 | 0 | 0 | a70bc97 |
| 08018DA0 | 62 | 2 | 0 | 4380d0a |
| 08015F98 | 112 | 73 | 0 | 03decc5 |
| 08015F58 | 64 | 20 | 0 | cc9c4c6 |
| 08015E50 | 132 | 107 | 0 | 8da48fa |
| 08015ED4 | 132 | 107 | 0 | f1e71c3 |

The first 08018DA0 comparison included the following two-byte alignment gap. All 62 bytes through its return already matched; the corrected complete-function end is 08018DDE. The aligner is not installed, changed or fabricated. The other seven comparisons include every compiler-owned literal pool.

`TARGETS.md` ranks all small unmatched entries, distinguishes already covered internal labels, and lists the smaller regions inside the remaining owners. `gap-audit-reviewed.json` reproduces the eight independent discoveries from the baseline partition. The earlier broad scan also listed 08002000; that fallthrough proposal was rejected. The final scan blocks existing instruction spans and finds no remaining independent candidate in the tested program enclosure. The reference audit also has no additional proposal. Neither audit is exhaustive proof that the remaining unknown data contains no code.

State, DMA and EEPROM names are descriptive suggestions in the inventory, without renaming any source symbol. Their confidence remains static-candidate confidence. Existing read, transfer and execution evidence is preserved; the coverage metadata explicitly separates the static discovery.

The first three short state/link C drafts were exact. The EEPROM retry is a normal three-try loop through the already matched write and compare helpers. The DMA family needed the source word and repeated neutral value kept in ordinary locals, with a fresh DMA base inside each transfer block. This recovers the compiler’s invariant and literal-pool order without assembly, fixed register bindings, padding, patched bytes or a changed compiler profile.

`baseline-sources/` preserves the first structured C drafts; `candidates/` contains the installed exact sources. Compiler profiles, sanitized differences and hashes are kept next to them. Additional named source/profile pairs preserve measured nonwinning hypotheses; they are not installed. The compressed trial journals retain source hashes and recipe choices. `authored-recipes.json.gz` preserves the actual local recipe scripts and installation driver; every installation still uses the unchanged checker and full-ROM gate.

Reproduce any installed comparison with the configured Python environment and the established profile:

```sh
python tools/measure_candidate.py docs/near-misses/breadth-1112/candidates/func_08015E50.c 08015E50 08015ED4 old build/recheck-08015E50
make -B all
make check
python tools/progress.py
```

Review: `txra-review/breadth-1112/`. The status pair compares 181/229 with 189/237 at the same table view; the code pair compares the first and exact 08015E50 C outputs at the same original instruction view. The two muted 30 fps WebM clips are compiler comparisons, not gameplay. `NOTES.md` and `captions.json` cover every picture and clip. Source, registry, build and finished media identities are recorded for coordinator archival.
