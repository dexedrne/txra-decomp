# Deep slice j, third pass (j3) outcomes

The slice-j selection rule on main at 147 matches: the 82 unmatched entries from
`tools/rank_targets.py --json`, sorted by `(bytes, address)`, zero-based odd indices `[1::2]`: 41 entries.
The even-index half belongs to the parallel slice and was not touched.

| Outcome | Entries |
| --- | ---: |
| Exact C match, installed | 7 |
| C, improved draft retained | 2 |
| C, worked, not matched | 1 |
| C, earlier seed kept, not reached | 6 |
| Assembly, BIOS or runtime entry (docs/asm-only.md) | 14 |
| Fragment, shared epilogue or broken boundary | 11 |

| Entry | Bytes | Outcome | Notes |
| --- | ---: | --- | --- |
| 0800B3A0 | 310 | Exact C match, installed | Point plot. The pixel value is one function-level variable shared by both parity branches, so the odd branch has two local quantities instead of three and local-alloc gives its row offset r0 as in the original. |
| 0800C850 | 352 | Exact C match, installed | Track-position update on the 0800C9C4 template. The dead next + 1 is an unused second wrap (after = next + 1; if (after >= n) after = 0;). Fields indexed directly; row address at * 28 + base. |
| 0800A940 | 748 | Exact C match, installed | Stat scaling. Two-dimensional s16 stats array; one function-level product temporary; first factor in two statements; third factor through a block temporary. |
| 0800AC3C | 772 | Exact C match, installed | Grade stat scaling, same macro as 0800A940. Grade read through p before the divide; the /16 and /64 factors are two variables (global allocation order). |
| 0800A17C | 1028 | Exact C match, installed | Race HUD bars and awards (deep-a draft finished). Record field_4c, next destination row before the last copy, and bonus values held in temporaries before their stores. |
| 0800C3C4 | 1132 | Exact C match, installed | Steering and heading update (deep-c candidate rewritten). Nested flag tests, a direct record access opening each block, one record pointer per block, one shared diff variable. |
| 08005238 | 2580 | Exact C match, installed | Menu sprite builder (deep-a draft finished). Two-dimensional column table so loop.c reduces the shared i * 2 giv; slide + 120 inline after the loop (PRE places it); one shared call-result variable; cursor source through the source variable. |
| 0800841C | 430 | Exact C match, installed after j3 | Palette fade by track tile. Matched after j3: the tile byte of all three range blocks and the blue channel of both fade loops are one function-level variable (src/generated/func_0800841C.c); the draft is kept for the review tool. |
| 0800BDC0 | 1540 | Exact C match, installed after j3 | AI lane choice. Matched after j3 (src/generated/func_0800BDC0.c): delta shares the loop counter, two-statement lane timer, s16 cast for the -2 mask, field_42 in the first neighbour loop, split final else-if; the draft is kept for the review tool. |
| 08016C18 | 400 | C, worked, not matched | ARM point projection (arm profile). After j3: goto outer loop (base added per pass like the original), u32 base local, unused 12-byte local for the 0x18 frame; draft in docs/deep-j3/drafts/func_08016C18.c at 80 normalized rows. The projection arithmetic is still scheduled differently. |
| 08017F64 | 604 | C, earlier seed kept, not reached | ARM; deep-a candidate 207 normalized rows off under the arm profile; not reached. |
| 080095E4 | 758 | C, earlier seed kept, not reached | Mapper reports an unresolved control transfer (bounded switch table); not reached. |
| 080076F4 | 1076 | C, earlier seed kept, not reached | ARM sound mixer; deep-c seed 562 normalized rows off; not reached. |
| 080181C0 | 1684 | C, earlier seed kept, not reached | ARM; deep-c seed 952 normalized rows off; not reached. |
| 08016DA8 | 4288 | C, earlier seed kept, not reached | ARM, 4,288 bytes, conventional APCS frame; no retained draft; not reached. |
| 08010A50 | 6444 | C, earlier seed kept, not reached | 6,444-byte routine; not reached this round. |
| 08018DE4 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r1 call veneer |
| 08018DEC | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r3 call veneer |
| 08018DF4 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r5 call veneer |
| 08018DFC | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r7 call veneer |
| 08018E04 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r9 call veneer |
| 08018E0C | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r11 call veneer |
| 08018E14 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx r13 call veneer |
| 08018E84 | 2 | Assembly, BIOS or runtime entry (docs/asm-only.md) | bx pc state switch |
| 08018A54 | 4 | Assembly, BIOS or runtime entry (docs/asm-only.md) | CpuFastSet SWI veneer |
| 08018E80 | 4 | Assembly, BIOS or runtime entry (docs/asm-only.md) | ARM branch into the division runtime |
| 08000218 | 100 | Assembly, BIOS or runtime entry (docs/asm-only.md) | signed division runtime |
| 080000FC | 248 | Assembly, BIOS or runtime entry (docs/asm-only.md) | IRQ entry |
| 08000AA0 | 320 | Assembly, BIOS or runtime entry (docs/asm-only.md) | private renderer helper (custom register contract) |
| 08000BF0 | 1224 | Assembly, BIOS or runtime entry (docs/asm-only.md) | ARM rasteriser with private register inputs |
| 0800735C | 12 | Fragment, shared epilogue or broken boundary | call without saved LR or outside ROM |
| 080051FE | 16 | Fragment, shared epilogue or broken boundary | invalid stack depth |
| 08007B28 | 24 | Fragment, shared epilogue or broken boundary | unresolved control transfer |
| 08006712 | 46 | Fragment, shared epilogue or broken boundary | call without saved LR or outside ROM |
| 08006740 | 54 | Fragment, shared epilogue or broken boundary | call without saved LR or outside ROM |
| 0800D51C | 84 | Fragment, shared epilogue or broken boundary | path leaves ROM or enters established literal/data pool |
| 0800D570 | 192 | Fragment, shared epilogue or broken boundary | call without saved LR or outside ROM |
| 080064A4 | 622 | Fragment, shared epilogue or broken boundary | reachable body crosses mapped boundary |
| 08007B40 | 2268 | Fragment, shared epilogue or broken boundary | call without saved LR or outside ROM |
| 08006776 | 3046 | Fragment, shared epilogue or broken boundary | call without saved LR or outside ROM |
| 08002854 | 3890 | Fragment, shared epilogue or broken boundary | reachable body crosses mapped boundary |

Retained drafts (not in the build) are in `drafts/`.
