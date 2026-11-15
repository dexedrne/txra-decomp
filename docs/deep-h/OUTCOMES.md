# Deep slice h outcomes

Selection: the 101 unmatched entries from `tools/rank_targets.py` on main at 128
matches, sorted by `(bytes, address)`, taking zero-based odd indices `[1::2]`:
50 entries. The even-index half belongs to the parallel slice and was not
touched. Distances count changed instruction lines against the complete target
including pools.

| Outcome | Entries |
| --- | ---: |
| Exact match, installed | 5 |
| C, improved this round (draft in `drafts/`) | 2 |
| C, worked this round without improvement | 1 |
| C, earlier seed kept, not reworked this round | 15 |
| Assembly or BIOS/runtime entry (already in `docs/asm-only.md`) | 15 |
| Fragment, shared epilogue or broken boundary | 12 |

## Worked this round

| Entry | Bytes | Before | After | What decided it |
| --- | ---: | --- | --- | --- |
| 0800B908 | 716 | 10 insns (one r8/r9 swap) | **exact** | Global-allocation tie, 0.1373 against 0.1395. Live length is counted on the RTL before combine, so a `u16` narrowing that combine later deletes still lengthens the hoisted `&g_03000000`. The second (+8192) rotation keeps its angle in a `u16`; the first uses an `s32`. |
| 08009D94 | 496 | 16 insns | **exact** | `combine_regs` in local-alloc only ties a result to a dying operand that is block-local. The untied `width` shows its temporary was a multi-block variable: the corner height goes into `distance`, then `width = distance >> 2`. |
| 08015128 | 216 | 48 insns | **exact** | Each channel reads the palette entry again; CSE merges the reads into one halfword pseudo with several uses, which combine cannot fold into the load (the `lsls #16 / lsrs #21` unpacking). `r, g, b` are function-level variables shared by both loops. |
| 08014FF4 | 308 | seed | **exact** | Same idioms. The toward-white blend is stepwise: extract, `31 - x`, `x *= k; x /= 8` as separate statements (one expression folds `*2/8` to `/4`), `31 - x`. |
| 08007398 | 376 | 44 insns | **exact**, in `unit_08005C7C.c` | A signed `bge` pointer loop is a reversed index loop: `check_dbra_loop` reverses a count-up loop from zero with one non-volatile store, which forces every giv to be reduced and eliminates the counter. The first wave fill stores through a plain `u16 *` (`vu16` blocks the reversal). The last tie, between two hoisted DMA addresses, breaks on the `.LC` label names, so the routine is compiled after its ROM-order neighbours. |
| 08014CE4 | 424 | 35 insns | 2 insns (one misplaced) | `g_0300000C = width = 120`; one `s` pointer and one `i` counter shared by both copy loops. Left: loop 1 hoists the 256 stride in the first loop pass (threshold 26 - 4x3 = 14 >= 14 real insns), so it lands before the counter copy. The original needs one more real insn or hoisted invariant in loop 1. |
| 080020B8 | 708 | 71 insns | 7 insns | Both clears are count-up loops over the globals (reversed by the loop optimiser), and `g_030001E0[0] = 1` indexes the array directly. Left: GCSE PRE hoists the outer `i + 1` above the inner copy loop, and the two copy bases swap registers. |
| 08013E74 | 310 | 85 insns | unchanged | The constant 64 lives in r9 for the whole function and `+39` is added before it. GCSE does not propagate it, but our build turns the hoisted `top = 64` into an equivalent constant and re-associates `x + 39 + top`. Not resolved. |

## Classification of the other entries

| Entry | Bytes | Outcome |
| --- | ---: | --- |
| 08018DE4, 08018DEC, 08018DF4, 08018DFC, 08018E04, 08018E0C, 08018E14 | 2 each | Assembly: register-call BX veneers. |
| 08018E84 | 2 | Assembly: `bx pc` state switch. |
| 08018A54 | 4 | Assembly: CpuFastSet SWI veneer. |
| 08018E80 | 4 | Assembly: ARM branch into the division runtime. |
| 08000218 | 100 | Assembly: signed division runtime. |
| 080000FC | 248 | Assembly: IRQ entry. |
| 080010B8, 080016E0, 08000BF0 | 336, 452, 1224 | Assembly: ARM rasterisers with private register inputs. |
| 0800735C, 08006712, 08006740, 0800D570, 08003786, 0800D630 | | Fragments inside larger routines. |
| 080051FE | 16 | Shared epilogue. |
| 08007B28, 0800D51C, 080064A4, 08008A88, 0800421C | | Boundary-blocked. |
| 0800C850 | 352 | C seed (deep-c) checked: 135 insns, a different callee-saved set, not close. |
| 0800841C, 08012A50, 080154AC, 0800CB5C, 0800B4D8, 080098DC, 080130BC, 0800F2D0 | | C, earlier seeds or notes kept; no retained source close enough to work this round. |
| 0800EDF4, 08013594, 0800AF4C, 0800E498 | | C with real switch tables; seeds kept. |
| 08016C18, 080165BC | 400, 1628 | ARM C seeds, not reworked. |
