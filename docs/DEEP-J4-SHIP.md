# TXRA: finishing the saved j3 near misses (j4)

Accepted totals move from **154 functions / 35,832 bytes / 42.090%** to
**156 / 37,824 / 44.430%** of the 85,132 mapped code bytes. Both matches use
the `old` profile with no flags, inline assembly or output patches.

| Entry | Bytes | Result |
| --- | ---: | --- |
| 0800841C | 452 | Exact match (palette fade by track tile). |
| 0800BDC0 | 1540 | Exact match (AI lane choice). |
| 08016C18 | 400 (ARM) | Not matched; draft improved from 126 to 80 normalized rows. |

## 0800841C

The j3 draft was 3 instructions off: the third range block loaded the tile byte
into r0 instead of r1. A copy of the compiler with logging in `global.c`
showed why. Global allocation merges register preferences along every chain
of dying registers (`expand_preferences`), and this compiler makes allocnos
even of locally allocated pseudos. The first block's tile byte inherits r1
from the record pointer; the third block's chain runs through the add where the
GCSE copy of the `g_03001E60` base dies, and that copy prefers r0 (it is
copied from the first load in r0). Preferences are unions, so the lowest one,
r0, wins. No sharing, splitting, type or declaration-order change inside the
range blocks can remove it (about 4,000 variants were swept to confirm).

The original avoids it with one function-level variable that is both the tile
byte of all three blocks and the blue channel inside both fade loops. In the
loops that variable is live while the green channel holds r0, so it conflicts
with r0 and takes its preferred r1 everywhere.

## 0800BDC0

The j3 draft was 353 normalized rows off (the earlier "255" used a looser
count). Five changes, found one at a time:

- The angle delta is the loop counter `i`, not its own variable. As its own
  variable it took r1 in global allocation, reload then spilled r1 for a
  zero-offset `ldrsh` and moved it to r8, which cost spills around it. Shared
  with the counter it takes r5 (353 to 181 rows).
- The steering flag clear casts `field_44` to `s16`, so the mask stays `-2`
  (`movs`/`negs`) rather than becoming a pooled `0xFFFE`.
- The lane timer is `*t += 1; *t &= 511;`. In one statement the and is done
  in HImode and reload copies the 511 through r5.
- The first neighbour loop compares the other car's `field_42`, not
  `field_48` (the original reads pointer + 10 from `field_38`). This was a
  real error in the draft, not a register issue.
- The last `else if (A || B)` of the lap-time chain is two `else if`
  branches with the same store. That shortens the live length of the
  `g_03001E60` base copy from 190 to 186 insns, so its allocation priority
  (1,935) beats the index product's (1,904). The base is placed first and
  takes r6, and the product gets r8, as in the original.

## 08016C18 (ARM, not matched)

Three of the j3 differences are solved in the kept draft
(`docs/deep-j3/drafts/func_08016C18.c`, arm profile):

- The outer loop is built with a label and `goto`. This compiler only runs
  loop optimisation on C loop statements, so the 0x02014000 base is no longer
  hoisted and is added as two immediates on each pass, like the original.
- The base is a `u32 base` local, so combine no longer folds it into a
  shifted add.
- An unused 12-byte local (`s32 pad[3]`) gives the original 0x18 frame and
  its slots at -56/-60/-64.

What is left is the order of the projection arithmetic: the original loads
and multiplies in a different order and keeps different values live. Swapping
the operands of all ten multiplies and both sums (4,096 variants) changes
nothing, because the compiler puts operands in a fixed order anyway.
Statement order and splitting the temporaries are the next things to try.

## Validation

After each match `make` ends in `build/txra.gba: OK`, `cmp` with the base
ROM is identical and the 170-test suite passes. `docs/map/indirect.json` drifts during `make` and was
restored, not committed. No OWNER-NOTES.md was present in the repository.
