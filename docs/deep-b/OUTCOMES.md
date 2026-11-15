# Slice b outcomes

Selection: freeze all 120 unmatched entries at the starting revision, sort by (mapped bytes, address), take zero-based offset 1 and stride 3. This includes helpers and fragments; no other slice entries are modified.

| Address | Bytes | Outcome | Learning |
| --- | ---: | --- | --- |
| 08018DE4 | 2 | assembly veneer | Branch to a live machine register; ordinary C ABI would add argument movement or call/return handling. |
| 08018DF0 | 2 | assembly veneer | Branch to a live machine register; ordinary C ABI would add argument movement or call/return handling. |
| 08018DFC | 2 | assembly veneer | Branch to a live machine register; ordinary C ABI would add argument movement or call/return handling. |
| 08018E08 | 2 | assembly veneer | Branch to a live machine register; ordinary C ABI would add argument movement or call/return handling. |
| 08018E14 | 2 | assembly veneer | Branch to a live machine register; ordinary C ABI would add argument movement or call/return handling. |
| 08000000 | 4 | assembly branch veneer | Bare ARM branch without link; preserve entry/interworking boundary. |
| 08018E80 | 4 | assembly branch veneer | Bare ARM branch without link; preserve entry/interworking boundary. |
| 0800735C | 12 | internal fragment | Reads enclosing stack/high-register state, or consumes unmatched stack saves; recover containing body before matching. |
| 08007368 | 16 | internal fragment | Reads enclosing stack/high-register state, or consumes unmatched stack saves; recover containing body before matching. |
| 08006712 | 46 | internal fragment | Reads enclosing stack/high-register state, or consumes unmatched stack saves; recover containing body before matching. |
| 0800027C | 68 | assembly runtime division | Conditional ARM shift/subtract helper; machine ABI and flag-dependent control flow indicate runtime assembly. |
| 08018E1C | 94 | exact C match | Original library loop with interworking disabled reproduces the full body and return. |
| 08014104 | 134 | unmatched C | Register allocation and setup order; retained 134-byte draft still differs by six instructions. Declaration scopes and both historical compilers did not resolve it. |
| 080147D0 | 194 | new compilable C seed | Undefined sp repaired with an addressed local; BIOS wrapper retained. Strength reduction explains the changed indexed loop, but pointers and return pool still differ. |
| 08015128 | 206 | non-ABI live-in | Saved r8 supplies a source pointer without definition. Need caller convention or evidence of an original uninitialized pointer; no invented C parameter. |
| 080148B0 | 214 | improved C seed | Restored full-width pointers and current packet signature. Persistent serial pointer and common return reproduce the saved registers and tail; two mask operations remain different. |
| 08014AE0 | 270 | new compilable C seed | A volatile 64-bit local reproduces the high-word-first hardware read and eight stack bytes. Loop aliasing, scheduling and saved state still differ. |
| 08014FF4 | 302 | non-ABI live-in | Saved r9 is read as a palette source before initialization in two branches; same unresolved calling convention as 08015128. |
| 08013E74 | 310 | corrected C seed | Removed a narrowed pointer and an unsupported signed-halfword loop cast. O1 now emits the correct 310-byte size, with register and scheduling differences. |
| 080010B8 | 336 | assembly renderer | Entry consumes live r4/r6/r11 and packed register state, uses condition flags across stack updates, and manually restores input registers. |
| 08006270 | 348 | corrected C seed | Removed a pointer truncation and a narrowed register later used as an address. Signed sample averaging must retain arithmetic shifts; loop allocation remains unresolved. |
| 08014CE4 | 366 | new compilable C seed | DMA loops require volatile indexed registers and an addressed stack fill word. DMA is ordinary C here, as in accepted sibling 08014C5C; body and pool still differ. |
| 08016C18 | 400 | ARM C seed, unmatched | Conventional compiler frame; tested the separate ARM compiler at O2/O1/Os. Corrected two MLA operations omitted from the lift and established 24-point groups at 672-byte stride. |
| 0800841C | 430 | unmatched C baseline | Three independent palette paths, signed clamps and 40-halfword loops. Retained matched sound-call signature; register allocation and pool differences remain. |
| 08012CC8 | 480 | unmatched C seed | Addressed local DMA fill and actual Thumb-to-ARM entry are required. Named ARM implementation calls would violate the Thumb relocation rule; retain the entry veneer. |
| 08012EB8 | 500 | unmatched C seed | Same display/DMA setup family as 08012CC8, with three text rows. Addressed local and actual interworking entry repair the baseline; allocation differs. |
| 08012A50 | 614 | unmatched C seed | Repaired the addressed DMA fill local, volatility, interworking entry and an assignment of a void call result. Shares setup with the smaller display routines; layout and scheduling still differ. |
| 08002500 | 624 | exact C match, 632 compiled bytes | Reviewed 94-case switch and typed 32-byte slot field reproduce all instructions, jump entries and pools. Ranker rejection was a switch-analysis limitation. |
| 0800F008 | 712 | unmatched C seed | Restored the fifth outgoing stack argument at three fill calls, preserved DMA reads and used the Thumb interworking entry. Do not treat an optimized callee signature as the original caller prototype. |
| 080154AC | 748 | corrected C seed | Two shift/narrow pairs in the draft erased the returned glyph code. Restored explicit logical right shifts; text layout still differs in stack slots and register allocation. |
| 0800AC3C | 772 | corrected C seed | Draft omitted signed-division operands. Recovered thirteen divisions by 100 and one by 12; signed rounding and multiply order remain essential. Not assembly-only. |
| 0800B4D8 | 1072 | unmatched C seed | Restored volatile stack fill, indexed DMA accesses, interworking entry and void call usage. Grouping record and triple fields changes the address pools but does not yet match. |
| 08012600 | 1094 | exact C match, 1104 compiled bytes | Two ordinary switches and typed slot fields reproduce the 105-case table, shared tails, all calls and final pools. The lifted machine-register variables obscured the original C scopes. |
| 080130BC | 1208 | unmatched C seed | Two copy calls pass a fifth argument at the outgoing stack slot. Retained the separate volatile fill local above it; large menu loop allocation remains unresolved. |
| 08001218 | 1224 | assembly renderer | Fixed register-save set, XOR swaps, flag-dependent packed coordinates and a non-C raster call contract; preserve assembly. |
| 080165BC | 1628 | ARM C seed, unmatched | Conventional compiler frame. Resolved 26 literal loads, 16 frame locals and four MLA operations; ARM O2/O1/Os trials compile but differ. Not assembly-only. |
| 08007B40 | 2268 | internal C entry | Starts with BL and outgoing stack stores before saving LR. Exit restores an inherited frame; the enclosing entry is required. |
| 08008A88 | 2876 | truncated C unit | Three reviewed switch tables are present. The mapped extent excludes its register-restoring epilogue at 080095C4, which is separately mapped; coordinate boundaries before matching. |
| 08002854 | 3890 | truncated C unit | Mapped end is 08003786; reachability continues through a balanced return at 0800417E. Never install only the mapped prefix. |
| 0800F2D0 | 5476 | unmatched C baseline | Large conditional menu body is ordinary C. Restored its missing division-by-100 operands; the register-style baseline is substantially longer. Needs semantic record access and scoped state variables. |
