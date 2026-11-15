# Finish pass 2, 15 November: 080181C0 contact rotation (label: contact)

Branch `work/finish2-contact` from main d74aed0. All compiles, measurements and
searches ran on worker B (`agbcc_arm` sha256 `26d884f0…`). The final candidate was
cross-checked on worker A (`agbcc_arm` `34268789…`), which gives the same compiled
hash `d9a63955…`. Nothing was built on the laptop. No ROM bytes were copied,
printed or committed.

**No exact replacement was installed.** The registry, build and match count are
unchanged (189 exact C, completion 222/228). The near-miss improved from **919 to
158 differing bytes**. The output length is now exact (1684/1684, was 1660), the
frame is exact (72/72, was 68), and instruction edits fell from 254 to 74. The first
421 bytes match. Every remaining difference is a register choice. No instruction,
constant, stack slot, branch, pool or layout differs.

## The source feature behind the second loop pass

The 11/14 diagnosis was right about *what* differs: the rerun loop pass hoists the
i*25/i*100 chain. Its explanation, "desirability cannot stop it", was wrong. Each
pass resets the threshold to 28 and lowers it by 3 for every insn it moves, in insn
order. The original's shape appears when **pass 1 spends its whole budget before
the index chains**. Pass 2 then moves the j chain (5 insns) and i*4/i*5, reaches
i*20 with threshold 7, and rejects it (7*2*2 = 28 < 46 insns). i*25 and i*100 then
stay in the loop as "not safe". The compiler dumps confirm this. The move-by-move
tables are in
[near-misses/finish2-1115-contact/LOOP-PASSES.md](near-misses/finish2-1115-contact/LOOP-PASSES.md).

Three things in the source supply the eight invariant insns that pass 1 moves
before the j index:

- the probe array is **indexed** in the loop (`for (k = 0; k <= 5; k++)` with
  `g_030057A0[k].field_00/08`). Strength reduction and dbra reversal then produce
  the original's `add r6, r6, #12` / `subs r7, r7, #1; bpl`;
- `sin[a]` and `cos[a]` of the car heading are **read inside the loop**. `a = field_20
  & 0x3FFF` is computed before the loop;
- record j word 3 (`zpos`), `sin[angle]` and `cos[angle]` are read inside the loop.
  With `cos[angle]` in the loop, `angle*4` dies at the cosine load. So `angle*4` and
  `cos[angle]` are hoisted (to sb and r8, as in the original) but `sin[angle]` is
  not, and it is reloaded every iteration as in the original.

This is "volatile-free aliasing" in the sense the brief asked about. The probe stores have a
known base, so the record and table loads are invariant. Which of them leave the
loop is decided by the threshold, not by alias analysis.

## Further source steps (each re-measured on worker B)

| Step | Bytes | Frame | Edits | Differing |
| --- | ---: | ---: | ---: | ---: |
| 1112b best (block-local pointer, zpos before the loop) | 1660 | 68 | 254 | 919 |
| indexing + in-loop sin[a]/cos[a]/zpos, c2 before the loop | 1684 | 72 | 277 | 1150 (sin[angle] still hoisted) |
| `cos[angle]` also in the loop | 1676 | 72 | 176 | 778 |
| multiply operands as `x * s1`, `xx * sin` (operand order of mul/mla) | 1676 | 72 | 174 | 770 |
| known/collision layout: `if (!known) { collision ... goto } mask |= ...; goto` | 1684 | 72 | 115 | 513 |
| `field_3c *= 4` (one `ldrsh`, no second `ldrh`) | 1676 | 72 | 85 | 221 |
| final clear loop `for (j = 0; j < 4; j++)` (reduced j*4 giv, `sub r3, r3, #4`) | 1684 | 72 | 76 | 165 |
| `if (i == 0 || j == 0)` (no `ldm` peephole) | 1684 | 72 | **74** | **158** |

Behaviour: `tools/check_contact_reference1112b.py` passes **384/384** cases against
the original ARM instructions in Unicorn (all 403 original instruction addresses
visited, 38 contact results). Its narrowing control rejects 250 cases. The control's
text substitution had to target the in-loop coefficient (see `original-fixtures.json`).

## What is left: register allocation (158 bytes)

1. **Rotate loop: the giv against k.** The global allocation order is k > c2 > c1
   > giv. The original needs the giv first (giv r6, k r7, c2 r8, c1 sl, angle*4 sb).
   - The giv's priority is 4*27/108 = 1.0, against k at 5*62/142 = 2.18. The giv's
     54-insn live length is doubled in `update_equiv_regs`. CSE marks its
     initialisation `REG_EQUAL g_030057A0`; the later increment removes the
     equivalence but leaves the doubled length.
   - A source-level pointer gets the same note from the first CSE pass.
   - Diagnostic only, with a patched copy of the same compiler sources on worker B that
     multiplies one pseudo's priority by 4. With the giv first, the rotate loop, test
     loop, collision body and k<=3 loop take the original's registers, and the
     distance falls to 118 bytes and 39 edits. Without the doubling alone, the giv
     (2.0) still loses to k (2.18). So the original must give the giv a shorter live
     range or k a lower priority, and the source feature behind that is not found.
   - Not admissible. The patched compiler was removed afterwards.
2. **j body r0/ip.** j*100 conflicts with hard r0–r3, so it gets ip and the
   `mask & g_080202E4[j]` result takes r0; the original is the reverse. The r0
   conflict comes from local allocation in the preheader. There, `rec+0x20` lives long
   because CSE2 rewrites the hoisted `rec+4` and `rec+12` constants as `rec+0x20 - 28`
   and `rec+0x20 - 20`: the record base copy is gone by then, so the next related
   value is used.
   - Separate `g_03001E64`/`g_03001E6C` symbols break the zpos hoist (839–1395
     bytes).
   - Disabling related values in CSE2 (diagnostic) changes too much (955).
3. In-loop reload order of i*5 / E64 base / j*100 and of zpos / E6C base. These follow
   from 1 and 2.

## Permuter

`tools/contact_search1115.py`: beam search over equivalent rewrites, using the
unchanged `arm` profile only. Its neighbourhood is
`variant_search.mutations` without type or literal changes, operand swaps around
array/field expressions, and a pair list (index sums, `!x`/`x == 0`, declaration
orders, `int`/`s32`). Two runs on worker B with 6–7 workers, about 15 and 19 minutes,
stopped by me, with more than 5,000 compiled candidates in the second run. Result:
no candidate below 158. Additional hand variants (about 60, all receipts
reproducible with `tools/contact_loopdump1115.py`) covered:
- separate loop counters;
- pointer loops with masked in-loop heading indices (m4: correct loop passes, 271);
- `TxraTriple *q = &g_030057A0[k]` (identical to the candidate);
- a function-scope probe pointer (breaks pass 1);
- statement orders, which the scheduler normalises;
- j-body condition forms.

## Receipts

`docs/near-misses/finish2-1115-contact/`:
- `func_080181C0.c`: complete candidate;
- `candidate.json`, `candidate.diff.txt.gz`: `tools/measure_candidate.py`, sanitized;
- `original-fixtures.json`: Unicorn comparison;
- `LOOP-PASSES.md`: both loop passes move by move, plus the allocation analysis.

Tools, all diagnostic and with no admission authority:
- `tools/contact_loopdump1115.py`: loop and allocation dumps of our own C;
- `tools/contact_search1115.py`: the search.

Worker copies (`~/txra-contact`, `~/txra-contact2`, the diagnostic compiler copy) were
removed. No process was left running.

matches installed: none
near-misses improved: 080181C0: 919 -> 158 (exact length 1684/1684 and frame 72/72; 254 -> 74 instruction edits)
what blocks the rest: register allocation only. The pointer giv loses the global priority race to k (its live length is doubled by the REG_EQUAL-to-REG_EQUIV quirk), and preheader local allocation keeps j*100 out of r0. The source feature that gives the original its allocation is not found.
