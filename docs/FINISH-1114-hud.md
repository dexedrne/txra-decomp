# HUD owner 0800421C, 14 November

No exact replacement was installed. The installed total stays **189**, covering
73,162 of 85,578 mapped code bytes (85.492%, unchanged). This round's
structural result is a boundary repair: the registry now has **236** entries,
not 237, because the HUD's epilogue is no longer listed as a separate function.

## Boundary repair: 080051FE belongs to 0800421C

Evidence, all from the existing disassembly:

- The 0800421C prologue pushes r4-r7 and lr, then r8-r10, then reserves 36
  bytes. The code at 080051FE releases 36 bytes, restores r8-r10, pops r4-r7,
  pops the saved return address and returns. That undoes exactly what the
  prologue set up.
- The owner's last loop (`ble` at 080051FC) falls straight into 080051FE. The
  local `b` instructions at 08004CB8, 08004E46 and 08005002 also branch to it.
- Only one BL reaches 080051FE, at 08004232, inside the owner and after lr has
  been saved. The epilogue returns through the saved lr, so the link value set
  by that BL is never used. This is the old Thumb compiler's long-branch idiom,
  not a call. Its fall-through at 08004236 is reached anyway by the preceding
  `beq`.

The analyzer used to turn every BL target into a function entry, which split
the epilogue off. The change is a reviewed config entry plus generic support:

- `tools/rom.cfg` gets a new `far_jumps` list holding this one entry (source,
  target, owner, evidence).
- `tools/analyze.py` gives a listed BL no new entry and no fall-through, and
  asserts that the reviewed target still matches.
- `tools/inventory.py` follows a listed BL as a branch when it computes extents.
- `tools/code_audit.py` reports such a target as `internal-far-jump`.

Regeneration changes only these generated outputs:

- In `asm/program.s`, the label `func_080051FE` becomes `loc_080051FE`.
  Assembled bytes are unchanged.
- In `docs/map/functions.json`, the 0800421C entry now ends at 0800520E and
  the 080051FE entry is gone.
- In `progress.json`, the function counts are now 236 found, 212 Thumb,
  236 mapped and 236 recompiled. Code, data and unknown byte totals are
  unchanged.

The edited local files hash the same as the outputs worker B regenerated. Two old
tests used 080051FE as a stand-in for an epilogue fragment. They now use the
sound epilogue 08007368 and assert that 080051FE is not an entry. A new
metadata test pins the far-jump entry and the repaired extent.

The other prior checks used end 08005238, the owner end including its pool,
so the near-miss numbers are not affected. `docs/map/code-audit.json` is not
regenerated here: it was already out of date before this change (its
input-mapping hash does not match the current mapping). Rerunning
`make code-audit` changes only 080051FE's row (existing-entry to
internal-far-jump), plus unrelated rows that had already gone stale.

The same idiom also appears outside this target, and other lanes own it. One
example is 08003786 inside the stream owner. Another is the BL at 08007358
inside the sound owner (08006776/0800735C/08007368). They can reuse
`far_jumps`; this pass does not touch them.

## C attempts (no improvement retained)

All runs used the 1112c candidate as base (`decomp-1112c/func_0800421C.c`,
sha256 f8ecf218…), the `old` profile, and the range 0800421C..08005238. The
base measured 3,144 differing bytes, instruction distance 1,023, 4,124/4,124
bytes and a 36/36-byte frame.

- **Constant-label position.** The base was compiled after a preceding
  function that forces K = 0..19 pool constants. All 20 results are identical
  (3,144 / 1,023). The same harness does reproduce the documented 08006070
  effect: K = 3 or 4 is exact, while K = 0 leaves 26 bytes different. So the
  HUD gap is not a translation-unit label tie, and adding real predecessor
  functions will not close it.
- **Spill-slot roles.** The original keeps exactly four stack words beyond the
  outgoing arguments. Each behaves like one reused C variable, which matches
  the old compiler's one-pseudo-per-variable allocation:
  - sp+20 holds the opening `t`, then gauge values, the absolute speed/20 and
    the smoke loop.
  - sp+24 holds the opening overlay size, the glyph index, the gauge tens
    digit, the map y coefficient and projected-effect values.
  - sp+28 holds the gauge units digit and the projected-effect values.
  - sp+32 holds the hoisted map y-coefficient address.

  The candidate keeps the overlay size in a register. It puts the map
  coefficient in the sp+28 word, and spills `t` in places where the original
  does not.
- **Making the candidate follow those roles locally made it worse.** Overlay
  size as `size`: 3,879. Map y coefficient as `size`: 3,256. As `t`: 3,256.
  `size` plus `t` for the x coefficient: 3,257 with a 32-byte frame. A
  one-region change moves allocation across the whole 4 KB body.

The decomp-permuter is not installed on worker B. Its random mutations target the
final few register differences, not a 1,000-instruction structural gap, so no
permuter run was started.

## Validation (worker B, this branch)

- `make -B all`: `build/txra.gba: OK`. The full ROM still has SHA-1
  4197339d4add74bb40ed02a8fba5e58096afb487.
- `make check`: 261 tests ran, OK (skipped=1).
- `make recomp`: 236 functions and 267 load/run entries emitted.
- `make check-runtime`: 446 runtime assertions passed.
- `make check-mapping`: 15 tests OK.
- `tools/progress.py` ran afterwards.

## Map completeness, for the finish-line question

"48 left" is not a fixed count:

- Some registry entries are fragments of larger owners: shared epilogues,
  long-branch continuations, and partial bodies listed in `asm-only.md`.
  Repairing these lowers the entry count without adding work, as this pass did.
- `unknown_bytes` is still 719,822. That region has not been shown to be free
  of code, so newly discovered functions could raise the count again.

The mapped-code-byte figure (85,578) is the better denominator, but it is also
only as complete as the map.

matches installed: none (189 exact replacements remain; registry 237 -> 236 entries after merging the 080051FE epilogue into 0800421C)
near-misses improved: 0800421C: 3144 -> 3144 (unchanged; the owner's registry boundary is now complete through 0800520E, pool through 08005238)
what blocks the rest: the HUD is still about 1,000 instruction edits away from exact; its four stack words are reused C variables, and getting the original allocation means changing variable roles across the whole function at once, not making local edits.
