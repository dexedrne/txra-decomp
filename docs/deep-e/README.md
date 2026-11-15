# Deep hand matching, slice e

Selection: the 105 unmatched entries from `tools/rank_targets.py --json` at the
start of the round (124 matches), sorted by `(bytes, address)`, zero-based
indices 0, 2, 4, … (53 entries). The other slice takes the odd indices; none of
its entries were touched.

Result: **3 exact matches** (08015DA8, 080063D4, 080148B0; 540 bytes with
pools), taking the build from 124 functions / 20.340% to 127 / 20.974%.
Each was found by reading the target and reasoning about the source shape, not
by a variant search; small variant batches (under 700 compiles each) were used
only to settle a typing or ordering choice once the shape was known.

`drafts/` keeps the closest natural-C hypotheses for the unmatched entries that
were worked on. They compile but are not exact and are not in the build.


| Entry | Bytes | Outcome | What was learned |
|---|---:|---|---|
| 08015DA8 | 118 | **exact** (old O2) | Load src/dst/size into locals before the volatile DMA writes; exit the loop with `goto` past it. A top-of-body `break` is rotated to the bottom by the loop expander (it moves any jump to the loop end within the first 30 insns). |
| 080063D4 | 208 | **exact** (old O2) | Same instructions, wrong registers: the reused buffer index lived across the clear loops, so it went to the global allocator. A separate `next` variable keeps the first index block-local (local-alloc gives it r3, the rest follows). Upward `*p++ = 0` loops give the countdown with the zero loaded first. Declaration order made no difference (648 variants). |
| 080147D0 | 224 | unmatched (C) | Typed the 288-byte link state (two 72-byte buffer triples at +144). Prefix through the CpuSet call and the two pointer stores match exactly. The loop differs: the original keeps `i` alive with an unreduced `(i<<2)+(s+80)` store while two other slots become post-increment pointers and s+144/s+168 are hoisted. Structured loops get fully strength-reduced (one pointer, reversed counter); a goto loop leaves everything unreduced. Neither half matches; O1 and no-gcse are worse. |
| 080149FC | 228 | unmatched (C) | Natural O2 draft now has the exact frame (volatile unused word at sp+0, spilled `out` at sp+12), the 4-entry pointer swap loop and the right total length. The original addresses everything from a pointer to the word at +4 (pool holds 03007A34) and derives the state base as that minus 4; writing `w = &g.field_04` reproduces it. Remaining: inner checksum loop register choice (sum/j/index) and where the state base is computed. Byte distance 138/228. |
| 080148B0 | 214 | **exact** (old O2) | Reading SIOCNT as a copy of a two-halfword bit-field record (the SDK-style multi-play control layout) explains the 32-bit load, the merged `&0x88==8` test and the byte `-65` mask; `s->field_00 = 8` is emitted as a store of the already-tested register. Return via a `u16` local assigned on both branches (direct returns cost 10 bytes). |
| 08014AE0 | 280 | unmatched (C) | Serial interrupt receive. Confirmed pieces: 64-bit copy of the four receive halfwords (a `u64` load, not a struct copy), send register written through the control record's `data` half. The loop has the same partial strength reduction as 080147D0 (i kept, offset giv plus in-loop base, unreduced `i<<2`, 0xFEFE reloaded each pass). The loop dump shows our drafts get every giv reduced and combined; what makes the original skip them is still unknown. Same family as 080147D0: solve one and the other should follow. |
| 08010910 | 320 | unmatched (C) | Number-to-text routine. The existing draft is 46 bytes off: only the `g_03002E58 = 0` store differs (original materialises a fresh zero in r0; ours reuses the `started` flag register r7 via post-reload CSE). The flag must be set early enough to conflict with the incoming argument registers (that is what puts it in r7), yet not be visible as "r7 holds 0" at that store. Tried: flag types u8/u16/s8/s16/s32, init placement after each store, declaration order, a separate zero variable, reusing a parameter as the flag. None closes it. |
| 0800B3A0 | 312 | unmatched (C) | Point-plot routine. The two scale factors loaded before the loop are invariant loads hoisted by the loop optimizer: read the table (declared `const`) inside the loop body and the setup matches exactly, with no hand-made preheader. The `if (mode == k)` chain and screen select match. Remaining: which invariants get hoisted (original hoists `&g_03002E4C`, ours hoists 0xFF00) and the pixel-address operand order. Best natural draft 156/312 bytes off (deep-a draft was 204). |
| 0800BBD4 | 496 | unmatched (C) | Per-frame camera/player update. Using `g_03002E40` directly inside the loop (instead of a pointer set before it) puts its address after the record base in the hoisted order, as in the original (189/496 bytes off, was 194). The remaining difference is block-local register choice in the two camera-offset blocks (scale/base/dx/dz); 45 type/statement-form variants all produce the same allocation, so the cause is not in those expressions. |
| 08008914 | 370 | unmatched (C) | 8-bit blitter in the 256-wide work buffer at 0x02000000. The original keeps `0x02000000 + (row << 8)` as one hoisted value; writing it as a row pointer declared *inside* the inner loop reproduces that form and its position after the inner-loop guard (an expression inline in the index gets the constant split off). Still different: the original also hoists the constants 1 and 255 and spills four words (16-byte frame vs our 8). Existing deep-c draft stays closest by bytes (174); ours is structurally closer in the row setup. |

## Entries not hand-matched this round

| Entry | Bytes | Outcome | Evidence / next step |
|---|---:|---|---|
| 08018DE0, 08018DE8, 08018DF0, 08018DF8, 08018E00, 08018E08, 08018E10 | 2 each | asm-only | `bx rN` register-call veneers (r0, r2, r4, r6, r8, r10, r12). They branch on a live register and keep the caller's return address; any C function adds a frame. Already recorded in asm-only.md by slices a–c. |
| 08018E7C | 2 | asm-only | `bx pc` state switch into the ARM division branch; no independent body. |
| 08000000 | 4 | asm-only | ARM reset branch in the cartridge header. |
| 08018A58 | 4 | asm-only | `swi 0x0B` (CpuSet) + `bx lr`; a BIOS call needs an assembly veneer. |
| 0800D960 | 8 | boundary | Internal tail entry of 0800D51C/0800D630: writes a flag and branches back without a frame. |
| 080095C4 | 14 | boundary | Shared epilogue of 08008A88; not a function. |
| 08007368 | 16 | boundary | Shared epilogue restoring an existing 108-byte frame. |
| 080001F4 | 36 | asm-only | IRQ return: banked SPSR/mode restore (MRS/MSR). |
| 080000C0 | 52 | asm-only | Startup: processor-mode switches, banked stacks, IRQ vector install. |
| 0800027C | 68 | asm-only | Unsigned division runtime helper (flag-driven shift/subtract). |
| 080002CC | 88 | asm-only | Private ARM ABI: operands in r6–r11 for the rasterizer. |
| 08000AA0 | 320 | asm-only | Raster helper consuming caller registers and flags. |
| 08000324 | 680 | asm-only | Renderer fragment reading r6–r11 and inherited stack. |
| 080005D8, 08001218 | 1224 each | asm-only | Rasterizers with a private register contract. |
| 08007B40 | 2268 | boundary | Internal C entry that writes an enclosing frame before saving LR. |
| 08006776 | 3046 | boundary | Starts mid-mixer, calls without saving LR. |
| 08002854 | 3890 | boundary | Reachable body runs past the mapped end; needs boundary repair first. |
| 08017F64 | 604 | C candidate (ARM), not attempted | Conventional APCS frame. It is the ARM sibling of 0800B3A0: same framebuffer select and `mode` chain. Solve 0800B3A0 first, then reuse the source shape with the ARM profile. |
| 080076F4, 080181C0, 08016DA8 | 1076 / 1684 / 4288 | C candidate (ARM), not attempted | Conventional APCS frames; earlier ARM-profile drafts did not match. |
| 08006270 | 348 | C candidate, not attempted in depth | Sound channel stream reset; best retained draft 156/356 bytes off. |
| 08018BE8 | 352 | C candidate, not attempted | EEPROM write; drafts far (335/352). |
| 080162F8 | 406 | C candidate, not attempted | Rotation/projection; frame 52 vs 60 in the best draft. |
| 08012CC8, 08012EB8, 0800F008 | 480 / 500 / 712 | C candidate, not attempted | Display/DMA setup family (deep-b notes: addressed local fill, interworking entry). |
| 0800CEEC, 0800A940, 080095E4, 0800AC3C | 620 / 748 / 758 / 772 | C candidate, not attempted | Switch/clamp bodies; prior drafts structurally distant. |
| 0800A17C | 1028 | C candidate, looked at briefly | Menu switch; deep-a draft is the closest large one (ratio 0.80, 446 bytes off), differences spread through allocation. |
| 0800C3C4, 0800BDC0, 08005238, 08010A50 | 1132–6444 | C candidate, not attempted | Large bodies; out of reach this round. |
