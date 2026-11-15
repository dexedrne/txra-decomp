# Deep slice l outcomes

A second pass over the slice-j selection rule on main at 146 matches: the 83 unmatched entries from
`tools/rank_targets.py --json`, sorted by `(bytes, address)`, zero-based odd indices `[1::2]`: 41 entries.
The even-index half belongs to the parallel slice and was not touched.

| Outcome | Entries |
| --- | ---: |
| Exact C match, installed | 1 |
| C, improved draft retained | 2 |
| C, worked, not matched | 1 |
| C, read, not reworked | 2 |
| C, earlier seed kept, not reached | 7 |
| Assembly, BIOS or runtime entry (docs/asm-only.md) | 17 |
| Fragment, shared epilogue or broken boundary | 11 |

| Entry | Bytes | Outcome | Notes |
| --- | ---: | --- | --- |
| 08006270 | 348 | Exact C match, installed | Sound stream mixer. Index and limit read through two block pointers in the first loop (hoist order); one function-level mixing temporary shared by both halving loops (global allocation priority). |
| 0800B3A0 | 310 | C, improved draft retained | Point plot; everything except the odd-x branch now matches (33 differing lines, because that branch swaps r0/r1, its tail merges with the even branch and the pool shifts). Address written inside the dereference (EXPAND_SUM order), x + (32 + shift), full-width mask temporary. Draft in drafts/. |
| 080162F8 | 406 | C, improved draft retained | Rotation and projection, 222 to 161 differing lines (143 with plain volatile structs). Trig globals assigned straight from the tables and read back; centre and delta as a volatile local pair. Spill layout still differs (frame 60 against 48). Draft in drafts/. |
| 08008914 | 370 | C, worked, not matched | Transparent blitter. CSE merges the two 255 masks into one register used outside its block, so loop.c will not hoist it; the original keeps 1 and 255 hoisted. |
| 0800CEEC | 620 | C, read, not reworked | Steering clamp. The original keeps 4096 in r9 through the function; the retained draft is register-style and 210 lines off. Not reworked. |
| 0800B4D8 | 1072 | C, read, not reworked | Title-loop family. GCSE PRE hoists g_03002A30 + 384 to the preheader; the original recomputes reg + 384 in the loop. Not reworked. |
| 080154AC | 748 | C, earlier seed kept, not reached | No retained draft in the repository; not reached. |
| 0800AF4C | 764 | C, earlier seed kept, not reached | Real switch table; deep-a candidate 238 lines off; not reached. |
| 0800CB5C | 912 | C, earlier seed kept, not reached | Deep-c candidate 347 lines off; not reached. |
| 080098DC | 1086 | C, earlier seed kept, not reached | Deep-a candidate 204 lines off; not reached. |
| 080165BC | 1628 | C, earlier seed kept, not reached | ARM C seed; not reached. |
| 0800E498 | 1974 | C, earlier seed kept, not reached | Real switch table; not reached. |
| 0800F2D0 | 5476 | C, earlier seed kept, not reached | Large menu body; no retained draft; not reached. |
| 08018DE4 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r1 call veneer |
| 08018DEC | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r3 call veneer |
| 08018DF4 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r5 call veneer |
| 08018DFC | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r7 call veneer |
| 08018E04 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r9 call veneer |
| 08018E0C | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r11 call veneer |
| 08018E14 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r13 call veneer |
| 08018E84 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx pc state switch (bx r15) |
| 08018A54 | 4 | Assembly, BIOS or runtime entry (docs/asm-only.md) | CpuFastSet SWI veneer |
| 08018E80 | 4 | Assembly, BIOS or runtime entry (docs/asm-only.md) | ARM branch into the division runtime |
| 08000218 | 100 | Assembly, BIOS or runtime entry (docs/asm-only.md) | signed division runtime |
| 080000FC | 248 | Assembly, BIOS or runtime entry (docs/asm-only.md) | IRQ entry |
| 08000AA0 | 320 | Assembly, BIOS or runtime entry (docs/asm-only.md) | private renderer helper (custom register contract) |
| 080016E0 | 452 | Assembly, BIOS or runtime entry (docs/asm-only.md) | custom ARM raster inner loop |
| 08000324 | 680 | Assembly, BIOS or runtime entry (docs/asm-only.md) | raster inner loop with preloaded registers |
| 080005D8 | 1224 | Assembly, BIOS or runtime entry (docs/asm-only.md) | textured raster front end with private helper ABI |
| 08001218 | 1224 | Assembly, BIOS or runtime entry (docs/asm-only.md) | assembly rasterizer |
| 0800735C | 12 | Fragment, shared epilogue or broken boundary | fragment inside a larger routine |
| 080051FE | 16 | Fragment, shared epilogue or broken boundary | shared epilogue |
| 08007B28 | 24 | Fragment, shared epilogue or broken boundary | boundary-blocked |
| 08006712 | 46 | Fragment, shared epilogue or broken boundary | fragment |
| 08006740 | 54 | Fragment, shared epilogue or broken boundary | fragment |
| 0800D51C | 84 | Fragment, shared epilogue or broken boundary | boundary-blocked |
| 0800D570 | 192 | Fragment, shared epilogue or broken boundary | fragment |
| 08003786 | 2552 | Fragment, shared epilogue or broken boundary | fragment |
| 08008A88 | 2876 | Fragment, shared epilogue or broken boundary | boundary-blocked |
| 0800D630 | 3662 | Fragment, shared epilogue or broken boundary | fragment |
| 0800421C | 4066 | Fragment, shared epilogue or broken boundary | boundary-blocked |

Retained drafts (not in the build) are in `drafts/`.
