# 080181C0 rotate loop: why the second loop pass stops at i*20

Evidence for `func_080181C0.c` in this folder. The movable reports come from
compiler debug dumps (`-dL -dG`, plus `-dl -dg` for allocation) of **our own C**,
compiled with the unchanged `arm` profile (`-O2 -mthumb-interwork`) on worker B
(`agbcc_arm` sha256 `26d884f0…`). The comparison with the original uses only the
disassembly already in `asm/program.s`. Tool: `tools/contact_loopdump1115.py`.

## The mechanism: the per-pass threshold budget, not safety

The 11/14 note assumed the rerun loop pass reaches the i-index chain with its
full threshold (28) and concluded that "desirability alone cannot stop it". That
assumption was wrong. `move_movables` lowers the threshold by 3 for every insn it
moves, in insn order, separately in each pass. The original's shape appears when
pass 1 spends its whole budget **before** the index chains, so that pass 2 starts
with the chains still in the loop and runs out exactly after `i*5`.

Three source features put enough invariant movables in front of the j index:

1. The probe array is indexed in the loop (`g_030057A0[k].field_00`, `for (k = 0;
   k <= 5; k++)`). This gives two invariant base constants (`g_030057A0` and
   `g_030057A0+8`). Strength reduction turns the index into the pointer giv
   (`add r6, r6, #12`), and the k biv is reversed into `subs; bpl`, as in the original.
2. The heading coefficients are read inside the loop (`g_083D2280[a]`,
   `g_083C2280[a]`, with `a = field_20 & 0x3FFF` computed before the loop). This adds
   the sine base, `a*4`, the `sin[a]` load, the cosine base and the `cos[a]` load.
3. Record j word 3 (`zpos`) and both output coefficients are read in the loop.
   `cos[angle]` must be in the loop too: then `angle*4` dies at the `cos[angle]`
   load, so `sin[angle]` is no longer forced out with it.

## Pass 1 (57 insns, threshold 28)

```
396 probe base (move-insn)   moved      28 -> 25
419 probe base + 8           moved      -> 22
424 sine base                moved      -> 19
428 a*4                      moved      -> 16
430 sin[a] load              moved      -> 13
433 cosine base              moved      -> 10
439 cos[a] load              moved      -> 7
446 record base              moved      -> 4
450 j*4 copy                 not desirable (4*2*3 = 24 < 57); j*5 .. j*100 not safe
460 record+4                 moved (forces the moved record base)
466 i*4 copy                 not desirable; i*5 .. i*100 not safe
523 record+12                moved (forces the record base)
564 angle*4 copy             not desirable; sin[angle], cos[angle] not safe
```

## Pass 2 (46 insns, threshold reset to 28)

```
450 j*4 copy   moved  -> 25      452 j*5  (forced) moved -> 22
454 j*20       moved  -> 19      456 j*25 (forced) -> 16   458 j*100 (forced) -> 13
466 i*4 copy   moved (13*2*3 = 78 >= 46) -> 10   468 i*5 (forced) -> 7
470 i*20       NOT DESIRABLE (7*2*2 = 28 < 46)   <- the original keeps it in the loop
472 i*25, 474 i*100       not safe                <- rebuilt from i*5 every iteration
478 record j word 1 load  not desirable           <- reloaded in the original
541 record j word 3 (zpos) moved (forced by j*100)  -> spilled at fp-0x5c, as in the original
564 angle*4 copy           moved (4*2*8 = 64 >= 46)  -> sb, as in the original
566 sin[angle] load        not desirable (1*1*8 < 46) <- reloaded in the original
575 cos[angle] load        moved (forced by angle*4) -> r8 (c2), as in the original
```

With this, the rotate loop and its preheader have the original's instruction
sequence, the 72-byte frame and the original stack slot for every spilled value
(s1 -0x50, j*100 -0x54, i*5 -0x58, zpos -0x5c, and so on). The whole owner is
1684/1684 bytes. The first 421 bytes are exact.

## What is left (158 differing bytes, 74 instruction edits)

All of it is register choice. No instruction, constant or stack slot differs.

1. **Rotate-loop register roles.** Ours: k r6, c2 r7, c1 r8, giv sl, angle*4 sb.
   Original: giv r6, k r7, c2 r8, c1 sl, angle*4 sb. Global allocation order (from
   the `.greg` "regs to allocate" list) is k (12th) > c2 > c1 > giv (27th) > angle*4.
   Priorities (`floor_log2(refs)*refs/live`): k 5*62/142 = 2.18; giv 4*27/108 = 1.0.
   The giv's live length (54 insns) is **doubled** by `update_equiv_regs`. CSE puts a
   `REG_EQUAL g_030057A0` note on the giv initialisation, so the register first gets a
   constant equivalence and twice its live length. The increment later removes the
   equivalence but not the doubling. A source-level pointer (`p = g_030057A0; ...
   p++`) gets the same note from the first CSE pass, so it is doubled too (variant
   m4: 92 = 2*46). The k/giv swap also gives the test loop (k r6/r7, j*100 r7/r6),
   the collision body and the k<=3 loop their r6/r7 swaps.
2. **j body r0/ip.** j*100 (pseudo 118) conflicts with hard r0-r3, so it gets ip.
   The and-result of `mask & g_080202E4[j]` (which also supplies the 0 stored to
   probe[4/5].field_08) then takes r0. In the original it is the other way round. The
   r0 conflict comes from local allocation in the preheader. There, `rec+0x20` (for
   field_20) lives long because CSE2 re-expresses the hoisted `rec+4` and `rec+12`
   constants as `rec+0x20 - 28` / `- 20` (related values). Reload later
   rematerialises them as pool loads, so this is visible only in the allocation.

Diagnostics (not admissible, not used for any candidate):
`-fno-rerun-cse-after-loop` moves the giv to r7, still behind k.
