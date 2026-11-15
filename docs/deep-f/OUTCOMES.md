# Deep slice f outcomes

Selection: the 105 unmatched entries from `tools/rank_targets.py` on the starting
main (124 matches), sorted by `(bytes, address)`, taking `[1::2]`. The 52 rows are
fixed in [targets.json](targets.json). Distances are against the complete target
including pools: "insns" is changed instruction lines, "bytes" is differing bytes.

| Outcome | Entries |
| --- | ---: |
| Exact match, installed | 1 |
| C, improved this round (draft in `candidates/`) | 7 |
| C, prior seed kept, not reworked this round | 17 |
| Assembly or private register interface | 15 |
| Fragment, shared epilogue or broken boundary | 12 |

## Worked this round

| Entry | Bytes | Before | After | What was learned |
| --- | ---: | --- | --- | --- |
| 08006070 | 300 | 16 insns / 26 bytes (deep-a), 98 lifted | **exact** | Written as the inverse of matched 0800619C with natural array C (18 insns alone). The last two differences are a register tie between hoisted address constants. Global CSE hashes the constant-pool label names, and those numbers carry across a file, so the tie depends on earlier functions. Compiled after matched 08005C7C-08005F8C in ROM order it is exact. Installed via `src/generated/unit_08005C7C.c`. |
| 08014104 | 134 | 6 insns / 10 bytes | 4 insns / 4 bytes | Natural `for (x=0; x<width; x++)` with **signed** x and width lets the loop optimiser reverse the inner loop into the target's count-down. That fixes the r4/r5 pair. Height and the destination base still swap r8/r9: equal reference counts, and the target gives the earlier-set variable the lower register. No declaration order, type, loop form or label offset changed it. |
| 0800B908 | 716 | 23 insns / 32 bytes | 10 insns / 10 bytes | A `u16` angle local for the first rotation and `angle = row + 8192; table[angle & 16383]` for the second give the target's table-load order. What's left is one r8/r9 swap: `conflict` (13 refs / 284 live) loses to `&g_03000000` (8 / 172) by 0.137 to 0.140 priority. Setting `conflict = 0` just before the inner loop flips it but moves the instruction, so the original has a few more refs or a shorter life. |
| 08007398 | 376 | 121 insns / 338 bytes | 44 insns / 60 bytes | Write every address inline and let global CSE hoist them. The target's hoisted DMA sources, destinations and tails are CSE output, not source variables. Use a `dmaRegs` pointer, and a signed pointer-compare loop for the first wave-RAM clear. Remaining: register order in the voice-clear block. The 288/360/432/504 offsets form a +72 chain that a plain `g[4..7].field_00 = 0` does not produce. |
| 08014CE4 | 424 | seed only | 35 insns / 41 bytes | DMA through a `dmaRegs` pointer macro. Forward `for (i=0; i<h; i++)` loops (the loop's own entry test is the `h > 0` check). `dst += x*2` in place. Combined assignment `g_03000004 = scroll = ...` gives the target's store-address-first order. Remaining: global allocation of s/DMA base/control in the copy loops, and counter-versus-256 hoist order. |
| 08015128 | 216 | rejected (r8 read before definition) | 48 insns / 102 bytes | **Resolved as ordinary C.** An uninitialised local `u16 *target` reproduces the saved-but-never-set r8 source pointer exactly. A volatile second pointer gives the `lsls #16 / lsrs #21` unpacking. Indexed up-counting loops give the target's constant / pointer / counter setup order. 08014FF4 is the same fade family reading r9 uninitialised. |
| 08013E74 | 310 | lifted register draft | 85 insns / 171 bytes | New typed quad-list C (shares the 32-byte quad packet with 08009D94). The target keeps the constant 64 in a register and never folds `+39+64`. The original value is therefore not a single-definition constant to global constant propagation. That construct was not found. |
| 08009D94 | 496 | 16 insns / 19 bytes | unchanged (order variant 31) | A local quad pointer reproduces the target's instruction order, but rotates three registers. The width value gets r3 in the target, which means it is allocated globally (lives across blocks) in the original. Kept both drafts; the deep-a draft remains the closest. |

## Classification of the other entries

| Entry | Bytes | Outcome |
| --- | ---: | --- |
| 08018DE4, 08018DEC, 08018DF4, 08018DFC, 08018E04, 08018E0C, 08018E14 | 2 each | Assembly: register-call BX veneers (r1, r3, r5, r7, r9, r11, sp). |
| 08018E84 | 2 | Assembly: `bx pc` state switch into the adjacent ARM code. |
| 08018A54 | 4 | Assembly: CpuFastSet SWI veneer. |
| 08018E80 | 4 | Assembly: ARM branch into the division runtime. |
| 08000218 | 100 | Assembly: signed division runtime. |
| 080000FC | 248 | Assembly: IRQ entry; mapped span is also incomplete. |
| 080010B8, 080016E0, 08000BF0 | 336, 452, 1224 | Assembly: ARM rasterisers with private register inputs. |
| 0800735C, 08006712, 08006740, 0800D570, 08003786, 0800D630 | | Fragments inside larger C routines (enclosing stack or high-register state read without a prologue). |
| 080051FE | 16 | Shared epilogue. |
| 08007B28, 0800D51C, 080064A4, 08008A88, 0800421C | | Boundary-blocked: mapped extent stops mid-body or runs into the next entry. |
| 08014FF4 | 302 | C: same fade family as 08015128, uninitialised r9 source pointer. |
| 0800C850, 0800841C, 08012A50, 080154AC, 0800CB5C, 0800B4D8, 080098DC, 080130BC, 0800F2D0 | | C, earlier seeds kept (deep-b / deep-c / match10). Not reworked this round. |
| 0800EDF4, 08013594, 0800AF4C, 0800E498 | | C with real switch tables (earlier seeds kept). |
| 080020B8 | 708 | C. The only retained draft that responds to label padding (71 to 49 at offsets 3 and 7). It follows ARM-only code, so it probably starts its own Thumb file and the real offset is 0. |
| 08016C18, 080165BC | 400, 1628 | ARM C seeds (conventional frames), not reworked. |
