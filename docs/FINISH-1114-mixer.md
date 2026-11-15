# Finish pass 14 November: mixer (08006712, 08006740, 08006776)

No exact replacement was installed. The three targets are not separate functions.
They are labels inside the sound owner **080064A4**, which old GCC reaches with
Thumb `bl` instructions because the jumps are longer than 2 KiB. This pass
repairs that boundary in the map. The owner's C body is still a nonmatch.

## What changed

- **Seven reviewed `far_jumps`** in `tools/rom.cfg`, all with owner 080064A4:

  | BL at | Target | Role in the owner |
  | --- | --- | --- |
  | 080066EC | 08007368 | sequence-loop exit to the owner's own epilogue |
  | 08006700 | 08007368 | tempo accumulator at most 0xFF: return |
  | 0800672C | 0800735C | voice disabled: continue the voice loop |
  | 0800673C | 0800735C | voice has no command stream: continue |
  | 08006F46 | 08006740 | command state 0x65: restart voice preparation |
  | 08007358 | 08006776 | command-loop back edge (state 0x65) |
  | 08007364 | 08006712 | voice-loop back edge while the next index is at most 7 |

  Each displacement is beyond the +/-2,048-byte Thumb `b` range. The owner pushes
  lr at 080064A4. It never reads lr and returns only through the stacked copy at
  08007374, so none of these BLs is a call. Every instruction after a BL is also
  reached by the conditional branch just before it.
- **Registry: 237 -> 232 entries.** 080064A4 now spans **080064A4..08007378**
  (11 spans, 3,796 instruction bytes; pool through 08007398). 08006712, 08006740,
  08006776, 0800735C and 08007368 are `loc_` labels in `asm/program.s`, not entries.
  Mapped code bytes are unchanged (85,578), as are the 189 exact replacements and
  73,162 matched bytes (85.492%).
- **Tools.** The far-jump support in `analyze.py`, `inventory.py` and
  `code_audit.py` is copied hunk for hunk from the HUD pass (38a80e4), so those
  files merge cleanly. `recomp/draft.py` now lifts reviewed far jumps as gotos:
  the 080064A4 draft is one function whose only callees are 08005F8C and
  `_call_via_r1`.
- **Tests.** New `tests/test_mixer_far_jumps.py` covers the config, registry,
  listing and lifter. `test_match3` and `test_match4` no longer expect 08006740 or
  08007368 as fragment entries.

## Frame layout of the owner (108 bytes)

These slots are taken from the listing, counting every `[sp, #n]` access in
080064A4..08007378:

| Slot | Contents |
| --- | --- |
| sp+0..35 | 9-word local array: a 36-byte struct copy at 08006534, indexed (1..6) at 08006546 |
| sp+36 | command state: set to 0x60 at 08006776; 0x65 means restart |
| sp+40 | 9*i (voice word index); 1 store, 9 loads |
| sp+44 | 72*i (voice byte offset) |
| sp+48 | &voice[i].delay (table + 16 + 72*i) |
| sp+52, 72, 76, 80 | per-voice field addresses (pool base + 72*i), all written at 08006740..08006774 |
| sp+56, 60, 64, 96, 104 | command-loop temporaries (08006D82..08006E7E) |
| sp+68 | &voice[i].note (table + 20 + 72*i) |
| sp+84 | note-start temporary (08006F70..080072FE) |
| sp+88 | i + 1, the next voice index (read at 0800735C) |
| sp+92 | 8*i |
| sp+100 | **never accessed** |

The retained candidates have a 100-byte frame, 8 bytes short of the original.
The original keeps one word (sp+100) that nothing ever reads or writes. That
suggests part of the 8-byte gap is a slot the compiler allocated but never used,
not a missing variable. In the original, r10 holds i and r12/r9 hold the voice table base
across the 08006712..08006776 entry.

## Measurements (worker B)

- Retained owner `docs/near-misses/sound-owner-1111/func_080064A4.c`, re-measured
  against the repaired map with `tools/measure_candidate.py ... 080064A4 08007398 old`:
  **3,227 differing bytes, 1,472 instruction edits, 3,808 / 3,828 bytes, frame 100 / 108**.
  These numbers are identical to the 11/11 receipt, so the repair did not change
  the comparison.
- No new C was installed or retained. Over five rounds this owner went from 3,568
  to 3,227 differing bytes. The first difference is still at +0x0A (the frame
  size), and 3,227 of the 3,828 bytes still differ. With roughly 1,470 instruction edits outstanding, local C edits move
  register allocation across the whole 3.8 KB body. Permuter mutations target the
  last few register differences, and decomp-permuter is not installed on worker B, so
  no permuter run was started.
- `make code-audit`: existing entries 193 -> 188, **5 internal-far-jump**,
  **0 proposals**. The committed `code-audit.json` is already stale on unmodified
  main (rejected 567 vs 565 on regeneration), so it is not recommitted here.

## Validation (worker B, this branch)

- `make -B all`: `build/txra.gba: OK`, SHA-1 4197339d4add74bb40ed02a8fba5e58096afb487.
- `make check`: 264 tests, OK (skipped=1).
- `make recomp`: 232 functions, 263 load/run entries emitted.
- `make check-runtime`: 446 runtime assertions passed. `make check-mapping`: 15 tests OK.
- `tools/progress.py` ran afterwards: functions_found / mapped / recompiled 232.

## Merging with the HUD branch (38a80e4)

- `tools/rom.cfg`: both branches add a `far_jumps` list at the same place.
  Keep the **union** (HUD's 08004232 entry plus these seven). Do not keep two
  `far_jumps` keys: JSON would silently drop the first one.
- `tests/test_match3.py`: after both merges, the remaining "known fragment" loop is
  empty. Keep both branches' not-a-candidate/not-skipped assertions.
- `tests/test_match4.py`: HUD switched the blocked-entry check to 08007368, which
  this branch removes. Keep this branch's 080001F4 check.
- `README.md`, `progress.json`, `docs/asm-only.md`: regenerate or merge the counts.
  With both branches merged the registry is 231 entries.

## On the finish line

Five of the 48 "remaining" entries were labels inside one function. The mixer
work is **one 3,828-byte function** (080064A4 with pool), not six. The remaining
count can still grow again: 719,822 ROM bytes are still unknown, and only bounded
static scans have checked them for code.

matches installed: none (189 exact replacements remain; registry 237 -> 232 after folding 08006712, 08006740, 08006776, 0800735C and 08007368 into 080064A4)
near-misses improved: 080064A4 (owner of all three targets): 3227 -> 3227 differing bytes (unchanged; boundary now complete as 080064A4..08007378, pool through 08007398)
what blocks the rest: the whole 3,828-byte owner is still about 1,470 instruction edits from exact, and its register allocation can only be recovered by changing the complete function at once, not by editing one fragment.
