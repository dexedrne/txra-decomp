# Sound owner 080064A4, 15 November (label: sound)

Target: the sound owner **080064A4..08007378** (pool through 08007398, 3,828 bytes). This range
includes the folded mixer labels 08006712, 08006740, 08006776, 0800735C and 08007368.

No exact replacement was installed. The installed total stays **189**, and `src/`, `tools/rom.cfg`
and the registry are unchanged. The new uninstalled near-miss roughly halves the distance:

| Measure (`tools/measure_candidate.py`, `old`, strict end 08007398) | 11/11 retained | this round |
| --- | ---: | ---: |
| Differing bytes | 3,227 | **1,598** |
| Instruction edit distance | 1,472 | **283** |
| Emitted / target bytes | 3,808 / 3,828 | 3,820 / 3,828 |
| Local frame / target | 100 / 108 | 100 / 108 |
| Original instructions identical in a text alignment (of 1,725) | 543 | **1,546** |

Source and receipts: [finish2-1115-sound](near-misses/finish2-1115-sound/README.md). The
source sha256 is `4765bf75…` and the compiled sha256 is `9320af76…`. The source is plain
structured C: no padding, inline assembly, fixed registers or widened checker.

## What changed

The 11/11 source came from automated search. This round discarded it and wrote the owner again
from `asm/program.s` in the original statement order. A choice-point search over
semantics-preserving source alternatives then ran on worker B. Each step below was confirmed by
compile and measure.

| Step | Differing bytes | Edit distance | Identical rows |
| --- | ---: | ---: | ---: |
| 11/11 retained | 3,227 | 1,472 | 543 |
| Fresh rewrite: real restart `do`/`while`, original statement order | 3,217* | 1,148 | 817 |
| Expression idioms (control `ldrh`, pitch/flags forms) | 3,193* | 1,102 | 857 |
| `command = 0` is the value stored into the fade flag | 3,332* | 948 | 1,033 |
| Block-scoped arpeggio index | 3,054* | 758 | 1,179 |
| Block-scoped tone-start, effect-loop and noise-tick locals (first in-length result) | 2,714 | 624 | 1,290 |
| Slide temporary, inline tick arpeggio index | 2,877* | 572 | 1,364 |
| `{ s32 *durations = gDurations; … }` around the note fields | 1,718 | 378 | 1,457 |
| Separate slide-envelope pointer | 1,675 | 309 | 1,526 |
| Noise-slide reload form, combined master-volume assignment | 1,608 | 291 | 1,540 |
| Mix-buffer index blocks (final) | **1,598** | **283** | **1,546** |

\* The output was longer than 3,828 bytes, so the checker rejected it as a diagnostic.

The structural findings are written up in the receipts README:

- the restart loop and its preheader;
- block-scoped temporaries, which decide local versus global allocation;
- the duration block, which also stops loop.c from hoisting `&voice[i].cursor` and its extra
  stack slot.

## Behaviour check

`diff32.py` compiles the new source and the 11/11 source unchanged for i386 and runs them
freestanding on seeded synthetic states. All mapped memory and the ordered hook calls must match.

- With one documented correction to the 11/11 reference, both runs are byte-identical: 1000/1000
  states with seed 1115 and 1000/1000 with seed 2026.
- The 11/11 source stores the rest-sample step to voice offset 0x40. The original stores it at
  0x30: 08007314 stores through sp+76, which holds 0x030077A0 + 72*i.
- Without the correction, 130/300 states are identical; the rest differ only in that field.

This is a bounded C-to-C regression check, not an original-instruction oracle or a gameplay test.
The old seven-group fixture harness assumes 32-bit host pointers inside structs and does not build
against the new pointer-typed source on the 64-bit host.

## Search runs (worker B)

decomp-permuter is not installed on worker B. In its place, `wsearch.py` ran detached on worker B with
JOBS 6 to 8 at nice 5, in eight sessions with 25 to 50 minute limits, about 65 minutes of search in
all. Each session was stopped by its exact PIDs once it plateaued. Measurements used the unchanged
compiler path; nothing outside the worker copy `~/txra-sound` was written. That copy was removed
at the end.

## Validation (worker B, this branch)

- `make -j8`: 189 `C match` lines, `build/txra.gba: OK`, SHA-1 4197339d4add74bb40ed02a8fba5e58096afb487.
- `make check`: `Ran 279 tests`, `OK (skipped=1)`.
- No admission check was run, because nothing was installed.

## What blocks an exact match

1. **8 bytes of length and 8 bytes of frame.** The original keeps the 0x67 master-volume
   temporary memory-resident at sp+96, with an unused slot at sp+100 and the command index at
   sp+104. This source keeps the temporary in r1, so everything after 08006DC4 sits 6 bytes early.
   This dominates the positional differing-byte count; with the length right, most of those bytes
   would line up. Scope, type, operand-order and combined-assignment forms did not change it.
2. **Envelope tick slide sections.** The slide pointer, `72*i` and the cursor address take a
   rotated register set, leaving about 105 register-only rows in 08006776..08006D62.
3. **Small leftovers.**
   - Zero-constant placement in the mix-buffer clear.
   - Effect-loop register roles.
   - The operand order of `gFadeLevel * 17`.

matches installed: none (189 exact replacements unchanged; 080064A4 not exact)
near-misses improved: 080064A4: 3227 -> 1598 differing bytes (instruction distance 1472 -> 283; 3,820/3,828 bytes, frame 100/108)
what blocks the rest: the original spills the 0x67 master-volume temporary to sp+96, plus an unused slot and the index at sp+104. Here it stays in r1, which leaves the output 8 bytes short with everything after 08006DC4 shifted. About 105 register-only rows also remain in the envelope-tick slide allocation.
