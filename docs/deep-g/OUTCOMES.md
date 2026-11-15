# Deep slice g outcomes

Selection: the 101 unmatched entries from `tools/rank_targets.py --json` on main at 128 matches, sorted by
`(bytes, address)`, taking `[0::2]` (51 entries). The other slice (`[1::2]`) was not touched.
"Lines" below are differing instruction rows from `tools/diffhint.py` against the complete target.

| Outcome | Entries |
| --- | ---: |
| Exact C match, installed | 5 |
| C, closer draft retained | 4 |
| C, worked, diagnosed, not matched | 6 |
| Assembly, BIOS or runtime entry | 18 |
| Boundary fragment | 6 |
| C candidate not reached | 12 |

| Entry | Bytes | Outcome | Notes |
| --- | ---: | --- | --- |
| 080147D0 | 194 | Exact C match, installed | Link setup. Every slot/buffer access through g_03007A30 itself. Through a local pointer the loop has 20 RTL insns and loop.c reduces every giv; directly it has more than 26, so the short-lived s+80 base stays in the loop and the third slot is never reduced, as in the original. |
| 08018BE8 | 352 | Exact C match, installed | EEPROM write. standard-o1 (the EEPROM library profile). Sibling idiom offset=bits*2; p=(u16*)(offset+(u32)buffer); one for(;;) wait loop with the ready/ack test first; current + (228 - previous). |
| 08012CC8 | 480 | Exact C match, installed | Title loop. SDK DmaClear shape (block-local vu32 tmp=0 before the DMA register pointer), upward clear loop that loop.c reverses, while (1) not for (;;). |
| 08012EB8 | 500 | Exact C match, installed | Three-line title loop; 08012CC8 source with three text records, exact on the first try. |
| 0800F008 | 712 | Exact C match, installed | Scene player; same DMA macros, a switch per frame and one for the scene change, gotos to two restart points; exact on the first draft. |
| 08014AE0 | 270 | C, closer draft retained | Serial receive, 3 lines off (was 131). Global-direct accesses (same fix as 080147D0), u64 copy of the receive registers, count loaded before the buffer pointer, other = field_40; field_40 = buf; field_30 = other. Remaining: r0/r1 swap in the 0xFEFE store; traced local-alloc shows the value gets twice the address's priority, so the original's address register had more references. |
| 0800B3A0 | 310 | C, closer draft retained | Point plot, 78 lines off (was 86). Read the flag before the screen base; load both record fields before the multiplies. Remaining: which invariants loop.c hoists (0xFF00 vs &count), a loop-size threshold effect. |
| 08006270 | 348 | C, closer draft retained | Sound stream mixer, 25 lines off (was 100). Array-indexed mix buffer, local pos copied to/from the global, v = dst + *src; src++. Remaining: hoist order of three address constants in the first loop (not label numbering: insensitive to 0-40 pool-label offsets and to compiling after the sound unit). |
| 0800AC3C | 772 | C, closer draft retained | Stat scaling, new draft, 213 lines off. x += ((x<<5)*(level*k))/100 then /32 in a separate step (a single /100/32 folds to /3200); level is an int, only the /12 value is narrowed. Remaining: level in a high register and the factor row as a CSE expression rebuilt for the tenth entry (consistent with CSE's 10-branch path limit). |
| 08014104 | 134 | C, worked, diagnosed, not matched | Blend blit, 4 lines off (unchanged). Traced global-alloc: priority = refs*log2(refs)/live*10000 and local-alloc doubles the live length of REG_EQUIV registers. The target order needs height and the source base without that doubling; no natural single-set constant avoids it. |
| 080149FC | 208 | C, worked, diagnosed, not matched | Link checksum. Global-direct and hybrid w/s forms tried; deep-e's draft (72 lines) stays closest. |
| 08010910 | 298 | C, worked, diagnosed, not matched | Number to text, 27 lines off (unchanged). The stored zero joins the flag's CSE class. do{}while(0) stops CSE pass 1 but CSE pass 2 merges it again; disabling pass 2 breaks 18 installed matches, so the original ran it. |
| 0800CEEC | 620 | C, worked, diagnosed, not matched | Steering routine; read, heavy spilling, not drafted this round. |
| 0800A940 | 748 | C, worked, diagnosed, not matched | Stat scaling sibling of 0800AC3C. Same expression findings; deep-a draft (207 lines) stays closest. |
| 0800A17C | 1028 | C, worked, diagnosed, not matched | Race HUD routine; deep-a draft is 234 lines off at the right length, not reworked. |
| 08018DE0 | 2 | Assembly, BIOS or runtime entry | bx r0 call veneer |
| 08018DE8 | 2 | Assembly, BIOS or runtime entry | bx r2 call veneer |
| 08018DF0 | 2 | Assembly, BIOS or runtime entry | bx r4 call veneer |
| 08018DF8 | 2 | Assembly, BIOS or runtime entry | bx r6 call veneer |
| 08018E00 | 2 | Assembly, BIOS or runtime entry | bx r8 call veneer |
| 08018E08 | 2 | Assembly, BIOS or runtime entry | bx r10 call veneer |
| 08018E10 | 2 | Assembly, BIOS or runtime entry | bx r12 call veneer |
| 08018E7C | 2 | Assembly, BIOS or runtime entry | bx pc switch into ARM division |
| 08000000 | 4 | Assembly, BIOS or runtime entry | ARM reset branch |
| 08018A58 | 4 | Assembly, BIOS or runtime entry | CpuSet SWI veneer |
| 080001F4 | 36 | Assembly, BIOS or runtime entry | IRQ return (banked mode restore) |
| 080000C0 | 52 | Assembly, BIOS or runtime entry | startup mode and stack setup |
| 0800027C | 68 | Assembly, BIOS or runtime entry | unsigned division runtime |
| 080002CC | 88 | Assembly, BIOS or runtime entry | private ARM register interface |
| 08000AA0 | 320 | Assembly, BIOS or runtime entry | raster helper using caller registers |
| 08000324 | 680 | Assembly, BIOS or runtime entry | renderer fragment with private registers |
| 080005D8 | 1224 | Assembly, BIOS or runtime entry | rasterizer with private register contract |
| 08001218 | 1224 | Assembly, BIOS or runtime entry | rasterizer with private register contract |
| 0800D960 | 8 | Boundary fragment | internal tail entry |
| 080095C4 | 14 | Boundary fragment | shared epilogue |
| 08007368 | 16 | Boundary fragment | shared epilogue |
| 08007B40 | 2268 | Boundary fragment | internal entry writing an enclosing frame |
| 08006776 | 3046 | Boundary fragment | starts mid-mixer |
| 08002854 | 3890 | Boundary fragment | body crosses mapped boundary |
| 08008914 | 370 | C candidate not reached | not reached this round |
| 080162F8 | 406 | C candidate not reached | not reached this round |
| 0800BBD4 | 444 | C candidate not reached | not reached this round |
| 08017F64 | 604 | C candidate not reached | ARM blitter, hand-unrolled two pixels per step; read only. |
| 080095E4 | 758 | C candidate not reached | not reached this round |
| 080076F4 | 1076 | C candidate not reached | not reached this round |
| 0800C3C4 | 1132 | C candidate not reached | not reached this round |
| 0800BDC0 | 1540 | C candidate not reached | not reached this round |
| 080181C0 | 1684 | C candidate not reached | not reached this round |
| 08005238 | 2580 | C candidate not reached | not reached this round |
| 08016DA8 | 4288 | C candidate not reached | not reached this round |
| 08010A50 | 6444 | C candidate not reached | not reached this round |

Retained drafts (not in the build) are in `drafts/`; `drafts/before/` holds the earlier drafts used for the before pictures.
