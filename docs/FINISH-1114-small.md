# Small targets, 14 November

No exact replacement was installed. Two registry entries that were labels inside
installed exact owners are folded into those owners. The registry goes from
**237 to 235 entries** on this branch. Code bytes, matched bytes (73,162) and
the 189 installed replacements are unchanged. The full ROM still hashes
4197339d4add74bb40ed02a8fba5e58096afb487.

## Targets

| Entry | Finding | Action this pass |
| --- | --- | --- |
| 080095C4 (14) | Shared epilogue of `func_08008A88`, which has been installed exact since 11/2 (08008A88-080095E4, pool included). Two BLs, at 08008B08 and 08008C76, are long gotos to it. Eight local B instructions also reach it. | Folded. Two `far_jumps` entries; the 08008A88 extent now ends at 080095D2. |
| 0800D960 (8) | Tail label inside `func_0800D51C`, installed exact (0800D51C-0800E498). Its only reference is the BL at 0800E3DC, the dispatcher's case 4. It stores 1 to a state word and branches back to 0800D630. | Folded. One `far_jumps` entry. 0800D570 and 0800D630 are left to the d630 lane. |
| 080051FE (16) | HUD owner epilogue. | Nothing done here. Branch `work/finish-hud` (38a80e4) already folds it with the same mechanism. |
| 0800735C (12), 08007368 (16) | Loop continuation and epilogue of the sound owner 080064A4. | Not duplicated. The mixer lane's worktree adds `far_jumps` for all seven sound-owner long branches. |
| 080064A4 (622) | Prologue of one complete sound owner: 080064A4-08007378, pool through 08007398, 3,828 bytes. Its best retained C (`sound-owner-1111`) differs in 3,227 bytes, with 1,472 instruction edits. | No C attempt this pass. The mixer lane works on the same owner, and one round of edits cannot close a gap that size. |

Evidence for the folds: the compiled output of the installed C has exactly two
`far jump` BLs in `func_08008A88` and five in `func_0800D51C`. Those five are
the 0800D960 jump plus four into 0800D570/0800D630. In every case the target
returns through the owner's stacked lr. The instruction after each BL is
reached by the preceding conditional branch, so `splits.json` and the code
partition do not change.

The tooling is the `far_jumps` support from `work/finish-hud`:
`tools/analyze.py`, `tools/inventory.py` and `tools/code_audit.py` are
byte-identical to that commit and to the mixer lane's copy, so those files
merge cleanly. Merging `tools/rom.cfg` means concatenating the `far_jumps`
lists. After that, `docs/map/functions.json` should be regenerated with `make`
on a worker rather than hand-merged.

## Validation (worker D)

- `make -B all`: `build/txra.gba: OK`, SHA-1 4197339d…b487, with 189 C matches.
- `make check`: 261 tests ran, OK (skipped=1). This includes a new metadata test that pins the three far jumps and the repaired extents.
- `make recomp`: 235 functions and 266 load/run entries emitted.
- `make check-runtime`: 446 runtime assertions passed.
- `make check-mapping`: 15 tests OK.
- `tools/progress.py` ran afterwards: 235 found / 211 Thumb / 235 recompiled.

Only `functions.json` and `progress.json` changed among the regenerated metadata.

## Finish line (base 62841be, 48 unmatched entries)

- **5** are labels inside installed exact owners, so they have no bytes left to
  match: 08007B40, 080095C4, 0800D570, 0800D630 and 0800D960.
- **31** are assembly interfaces: startup/IRQ, division, ARM raster with a
  private ABI, BIOS, register-call and interworking veneers. Under the rules
  they cannot become C matches.
- **12** belong to just **5 unfinished C owners**: stream 08002854 (+08003786),
  HUD 0800421C (+080051FE), sound 080064A4 (+5 labels), renderer 08016DA8 and
  contact 080181C0. Together they hold 19,252 unmatched code bytes, and every
  one is hundreds to thousands of bytes from exact.
- The headline **85.5%** divides matched bytes *including pools* (73,162) by
  code-only bytes (85,578). Matches cover **60,234 of 85,578 code bytes (70.4%)**.
  Of what is left, 19,252 code bytes are in the five owners and 6,092 are in the
  31 assembly interfaces.
- Map completeness: the code region (through about 08019000) has only 657
  unknown bytes, almost all 2-byte aligners. The other 719,165 unknown bytes lie
  in the asset area. Earlier bounded scans found no code there (331 prologue
  candidates rejected; a 5,732-check leaf scan found zero). That is strong
  evidence but not proof.

matches installed: none (189 exact replacements remain; registry 237 -> 235 by folding 080095C4 into func_08008A88 and 0800D960 into func_0800D51C)
near-misses improved: none (080064A4 sound owner unchanged at 3227 differing bytes; 080051FE, 0800735C and 08007368 are handled as labels by the hud and mixer lanes)
what blocks the rest: my remaining targets are all parts of the 3,828-byte sound owner, whose best C is still about 1,470 instruction edits from exact, and the mixer lane is working on that same owner.
