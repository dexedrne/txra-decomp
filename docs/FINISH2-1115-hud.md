# HUD owner 0800421C, 15 November: installed as exact C

The HUD owner 0800421C (4,082 registry bytes, 4,124 bytes through its pool at
08005238) is now an exact C replacement in `src/generated/func_0800421C.c`. It
went from **3,144 differing bytes to 0**. It is installed through the normal
gate: a `tools/rom.cfg` match entry, which `tools/match.py` compiles with the
historical `old` profile (`old_agbcc -O2 -mthumb-interwork`) and verifies byte
for byte, plus a forced full rebuild that must reproduce ROM SHA-1
`4197339d4add74bb40ed02a8fba5e58096afb487`. The source is structured C only: no
inline assembly, padding, hand bytes or checker tricks.

Totals after this change: **190 exact C replacements** (77,286 bytes including
pools). `progress.json → completion` reads **223 of 228**, and **5 entries
remain**: the C owners 08002854, 080064A4, 08016DA8 and 080181C0, plus the
08003786 continuation inside 08002854.

## How it matched

The retained 1112c candidate was not used as the base. Search had shaped it
into an unnatural form (nested scopes, `offset / 16` indexing, a captured
cursor pointer), and its allocation could not be pulled back from there. The
installed source is a fresh rewrite from the disassembly in plain game-code
style. The steps, with measurements, are in
[progression.json](finish2-1115-hud/progression.json):

| Step | Output / frame | Instruction edits | Differing bytes |
| --- | ---: | ---: | ---: |
| 1112c baseline | 4,124 / 36 | 1,023 | 3,144 |
| Fresh rewrite | 4,104 / 40 | 856 | 3,800 |
| Overlay centre, digit sources | 4,112 / 44 | 545 | 2,748 |
| Index-expression loops | 4,104 / 36 | 569 | 3,825 (20-byte shift) |
| Plain smoke-spawn loop | 4,116 / 36 | 140 | 1,725 |
| Map y in two steps | 4,124 / 36 | 23 | 24 |
| Map x in two steps (installed) | 4,124 / 36 | 0 | **0** |

What the original source evidently looked like:

1. **A few function-wide temporaries.** The four stack words are three
   variables spilled for the whole function (`t` at sp+20, `s` at sp+24, `u`
   at sp+28) and one compiler-hoisted address (sp+32, the map y-coefficient
   pointer). Each spilled pseudo gets its own slot, so these three really are
   single reused C variables. The same holds for `i` (sb in every loop, and
   also the 0x62 field and the `field_02 - 16` row), `x` (r4), `y` (sl), `a`
   (r8: gauge angle, hundreds digit, text character, map x coefficient,
   projection width) and `src` (r7). The smoke-loop absolute value is a
   block-local temporary, so it stays in r2.
2. **Loop positions are index expressions.** Examples are
   `((56 + i * 32) & 0x1FF) | 0x8000` and, in the gauge, `98 + i * 16`,
   `172 + j * 32` and `512 + i * 32 + j * 16`. The old compiler's own
   strength reduction creates the incrementing registers. Loop reversal then
   turns every counter used only for the exit test into the down-counting
   `add sb, #-1; bge` form. Its initialisers come after the hoisted
   invariants, which explains the instruction order that hand-written
   `x += 32` could not give.
3. **Attribute words are written as `x | size | slot << 9`.** For example,
   `((x - 16) & 0x1FF) | 0x8000 | (g_03006680 << 9)`. Fold re-associates
   this as `x | ((slot << 9) | size)`, which is the original evaluation
   order. The overlay passes centre (120, 72) minus 32. CSE folds `y` into
   the constant 0x2128, but `x - 32` becomes a separate `movs r6, #88`,
   because Thumb `orr` cannot take an immediate.
4. **Source pointers are assigned to `src`.** In the timer digits, r7 then
   holds `src`, so the digit-table base gets no register and is reloaded from
   the pool before each digit. That reload is what the original does.
5. **The smoke spawn is a plain loop.** It is `for (i = 0; i < 8; i++)` over
   `g_030067F0[i]` with a `break`. Strength reduction and induction-variable
   elimination produce the four field pointers and the offset, and the signed
   `ptr <= base + 0x70` exit test.
6. **The map coordinates are assigned in two steps:**
   `x = -field_04; x = (x * g_0804F330[a + 0x10000]) >> 19;`, and the same
   for `y`. Each value therefore enters the variable's own register before
   the multiply. With `y` alone in two steps the owner was 24 bytes from
   exact. Doing the same for `x` closed it.

Two diagnostics drove the search, and both run on the worker:

- **GCC's own global-allocation dump**. Run
  `old_agbcc t.i -O2 -mthumb-interwork -dg` on the preprocessed candidate and
  read `t.i.greg`; the small wrapper used here is not committed. It lists
  every allocno in priority order
  with refs and live length, and the final hard register of each pseudo.
  Declared variables are the first pseudos (22, 23, ...) in declaration
  order, so the dump shows directly which variable got which register.
- **A call-delimited, segment-by-segment comparison** of the full target and
  compiled listings, with pool words masked. It counts matching shapes
  (ignoring registers) and exact matches per segment, which separates
  structural errors from allocation errors.

## Permuter

decomp-permuter (simonlindholm/decomp-permuter, its own venv) was set up on
worker D for this owner. One detached run started on the 1112c baseline, with
`-j4`, a 2-hour limit and higher weights on the allocation-related passes
(declaration reordering, temporaries, variable removal and substitution, block
insertion, assignment splitting and duplication). In about 30 minutes and
6,200 iterations it lowered its own score from 47,960 to 38,275. It was
stopped, by its own process group, once the rewrite reached exact. Its
outputs were removed with the worker build directory before they were
measured on the project's byte metric. They were superseded in any case. The
permuter clone, its venv and the worker copy were removed at the end.

## Validation (worker D, this branch)

- `make clean; make -j8`: 190 `C match` lines, including
  `func_0800421C: C match (4124 bytes)`, and `build/txra.gba: OK`. SHA-1 is
  `4197339d4add74bb40ed02a8fba5e58096afb487`.
- `make -B all`: `build/txra.gba: OK` with the same SHA-1.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- `make recomp`: `Emitted 228 functions, 258 load/run entries`.
- `make check-runtime`: `446 runtime assertions passed`.
- `make check-mapping`: `Ran 18 tests`, `OK`.
- `make check-accuracy`:
  `Accuracy: 4300 framebuffer hashes, every PCM byte, final state and sample clock passed`.
  It also reports `fallback=0 unknown=0 unsupported=0`.
- `tools/measure_candidate.py src/generated/func_0800421C.c 0800421C 08005238 old`
  gives 4,124 / 4,124 bytes, frame 36 / 36, 0 instruction edits, 0 differing
  bytes and `exact: true`. The compiled sha256 starts `4f9e32de…`. Receipt:
  [measure.json](finish2-1115-hud/measure.json).
- Regenerated outputs: `asm/program.s` replaces the owner's 1,903 listing
  lines with one `.incbin "build/leaves/func_0800421C.bin"`. The local edit
  hashes the same as the worker's regeneration (sha256 `7d15d4e4…`).
  `docs/map/finish.json` drops the C-candidate row. `progress.json` updates
  the counts, and `hand_matches_added` goes from 83 to 84 by hand, as in
  earlier single installs. `finish.json` reproduces byte for byte on a second
  `tools/asm_interfaces.py` run. No ROM bytes or ROM-derived binaries left
  the worker.

## For the remaining owners

The sound owner 080064A4 has the same symptom the HUD had: whole-function
allocation, about 1,470 instruction edits. The same approach is worth trying
there. Rewrite it fresh in plain style. Find the function-wide spilled
variables from the frame's stack words. Write loop positions as index
expressions. Read the `-dg` dump to see which declared variable lands in
which register.

matches installed: 0800421C (HUD owner, 4,124 bytes with pools; exact C 189 -> 190, completion 222 -> 223 of 228)
near-misses improved: 0800421C: 3144 -> 0 (installed as exact C)
what blocks the rest: nothing for the HUD; the 5 remaining entries (C owners 08002854, 080064A4, 08016DA8, 080181C0 and the 08003786 continuation, which installs with 08002854) belong to other lanes and still differ by block allocation, register swap and scheduling, whole-function allocation and frame, and loop-optimization structure respectively.
