# Deep slice j outcomes

Selection: the 91 unmatched entries from `tools/rank_targets.py --json` on main at 138 matches,
sorted by `(bytes, address)`, taking zero-based odd indices `[1::2]`: 45 entries. The even-index
half belongs to the parallel slice and was not touched.

| Outcome | Entries |
| --- | ---: |
| Exact C match, installed | 7 |
| C, improved draft retained | 2 |
| C, worked, not matched | 1 |
| C, read, not reworked | 1 |
| C, earlier seed kept, not reached | 8 |
| Assembly, BIOS or runtime entry (docs/asm-only.md) | 14 |
| Fragment, shared epilogue or broken boundary | 12 |

| Entry | Outcome | Notes |
| --- | --- | --- |
| 080020B8 | Exact C match, installed | Start-up routine. Row copy as a count-up index loop; the next clear loop reuses the outer counter, which isolates the outer increment for PRE so it stays at the latch. |
| 08010910 | Exact C match, installed | Number to text. The zero store is an always-zero narrowed shift that only combine folds, so CSE cannot merge it into the flag register; the do-while workaround is gone. |
| 0800EDF4 | Exact C match, installed | Palette effect with an 18-way switch. Three separate halfword reads per channel and a destination pointer variable computed before packing. |
| 0800BBD4 | Exact C match, installed | Per-frame camera. Each offset product is its own function-level variable (not tied to the shift result); a block-scoped mask variable in the second block. |
| 08012A50 | Exact C match, installed | Title menu loop, written from the matched sibling 08012CC8; screen-base select as a zero-test conditional expression. |
| 080130BC | Exact C match, installed | Name entry screen on the same template; the frame counter is reused as the letter count after the loop. |
| 08013594 | Exact C match, installed | Mode menu with two ten-way switches on the same template; case labels in the original emission order 0, 1, 8, 9, 2, 3. |
| 08013E74 | C, improved draft retained | 85 to 18 differing instructions (one r4/r5 swap between k and the cached record pointer). Draft in drafts/. |
| 0800B4D8 | C, improved draft retained | New draft on the title-loop template, 273 normalized lines; loop.c strength-reduces g_03002A30 + 384 into a hoisted constant. Draft in drafts/. |
| 08008914 | C, worked, not matched | Row bases inside the inner loop reproduce the hoisted bases; the original keeps 1 and 255 in registers and spills two other values. |
| 0800C850 | C, read, not reworked | Read the target against the deep-c draft (98 differing lines with old-no-gcse, 190 with old); not reworked. An apparently dead next+1 increment in the original is still unexplained. |
| 080162F8 | C, earlier seed kept, not reached | Not reworked this round. |
| 080154AC | C, earlier seed kept, not reached | Not reworked this round. |
| 0800AF4C | C, earlier seed kept, not reached | Not reworked this round. |
| 0800CB5C | C, earlier seed kept, not reached | Not reworked this round. |
| 080098DC | C, earlier seed kept, not reached | Not reworked this round. |
| 0800E498 | C, earlier seed kept, not reached | Not reworked this round. |
| 0800F2D0 | C, earlier seed kept, not reached | Not reworked this round. |
| 080165BC | C, earlier seed kept, not reached | ARM C seed, not reworked. |
| 08018DE4 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r1 call veneer |
| 08018DEC | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r3 call veneer |
| 08018DF4 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r5 call veneer |
| 08018DFC | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r7 call veneer |
| 08018E04 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r9 call veneer |
| 08018E0C | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r11 call veneer |
| 08018E14 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r13 call veneer |
| 08018E84 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx pc state switch (bx r15) |
| 08018A54 | Assembly, BIOS or runtime entry (docs/asm-only.md) | CpuFastSet SWI veneer |
| 08018E80 | Assembly, BIOS or runtime entry (docs/asm-only.md) | ARM branch into the division runtime |
| 08000218 | Assembly, BIOS or runtime entry (docs/asm-only.md) | signed division runtime |
| 080000FC | Assembly, BIOS or runtime entry (docs/asm-only.md) | IRQ entry |
| 080010B8 | Assembly, BIOS or runtime entry (docs/asm-only.md) | ARM rasteriser with private register inputs |
| 08000BF0 | Assembly, BIOS or runtime entry (docs/asm-only.md) | ARM rasteriser with private register inputs |
| 0800735C | Fragment, shared epilogue or broken boundary | fragment inside a larger routine |
| 080051FE | Fragment, shared epilogue or broken boundary | shared epilogue |
| 08007B28 | Fragment, shared epilogue or broken boundary | boundary-blocked |
| 08006712 | Fragment, shared epilogue or broken boundary | fragment |
| 08006740 | Fragment, shared epilogue or broken boundary | fragment |
| 0800D51C | Fragment, shared epilogue or broken boundary | boundary-blocked |
| 0800D570 | Fragment, shared epilogue or broken boundary | fragment |
| 080064A4 | Fragment, shared epilogue or broken boundary | boundary-blocked |
| 08003786 | Fragment, shared epilogue or broken boundary | fragment |
| 08008A88 | Fragment, shared epilogue or broken boundary | boundary-blocked |
| 0800D630 | Fragment, shared epilogue or broken boundary | fragment |
| 0800421C | Fragment, shared epilogue or broken boundary | boundary-blocked |

Retained drafts (not in the build) are in `drafts/`; `drafts/before/` holds earlier drafts used for the before pictures.
