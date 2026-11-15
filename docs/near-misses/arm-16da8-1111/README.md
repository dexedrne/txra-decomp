# 08016DA8 / 11 November

Uninstalled complete-owner near-match.

The serial region search measured **15** alternatives from **20** proposed regions. Whole-function differing bytes: **3251 -> 3251**, with **0** retained improvements. Safety rejections, duplicate sources and target-compiler failures do not count as measurements; compiled boundary or fixture rejections do.

Profile: `arm`, `-O2 -mthumb-interwork`; original checker end `08017E68`. Output is 4268 / 4288 bytes; local frame is 108 bytes. Instruction edit distance is 898 -> 898; this diagnostic is separate from the requested byte-distance objective.

Inherited layout and pool-alias notes: [prior retained source](../arm-16da8-1110/README.md).

`func_08016DA8.c` is the retained source; `candidate.json`, `candidate.diff.txt` and `candidate-checks.json` pin its compiler output and fixture gate. `baseline.json` points at the immutable previous source. `improvements/` contains accepted source revisions when any exist. No original byte slices or object files are stored here.

HUD fixtures compare prior C state and ordered helper calls; sound uses synthetic groups; ARM uses an independent textual instruction executor and synthetic memory. These do not prove arbitrary-state game behavior. Only complete byte equality plus every forced whole-ROM gate can install a replacement.

The selector uses verified debug source maps as positional layout aids. Its bounded statement scanner keeps macros as calls; oversized expanded regions are skipped when complete listings will not fit the request budget. This is not exhaustive source recovery.

See [operation and resuming](../../LOCAL1111-SEARCH.md) and [ship note](../../LOCAL1111-SHIP.md).
