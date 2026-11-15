# Finish tracker

This tracker covers every mapped entry that has no exact C replacement of its own. It also gives the map-completeness verdict and defines "done". It is regenerated from `docs/map/finish.json` (written by `tools/asm_interfaces.py`) and from the completeness receipt `docs/finish-1114/completeness-int.json.gz` (written by `tools/map_completeness.py` on the integrated 228-entry map; the classify-round receipt for the 237-entry map is `docs/finish-1114/completeness.json.gz`). Both tools run on a worker that has the private ROM. Their outputs contain metadata only.

## Verdict in one paragraph

**No code was found outside the function map; the finish line is the current 228 entries (85,578 mapped code bytes).** On 11/15 the road stream owner 08002854 (with its internal label 08003786; [note](FINISH2-1115-stream.md)) and the HUD owner 0800421C ([note](FINISH2-1115-hud.md)) were installed as exact C ([integration note](FINISH2-1115-integrate2.md)), finish pass 3 installed the contact owner 080181C0 ([note](FINISH3-1115-contact.md), [integration note](FINISH3-1115-integrate3.md)), finish pass 5 installed the sound owner 080064A4 ([note](FINISH5-1115-sound.md), [integration note](FINISH5-1115-integrate5.md)), and finish pass 6 installed the last one, the renderer owner 08016DA8 ([note](FINISH6-1115-base.md); 49 differing bytes since finish pass 4), so **no C owner remains** and every one of the 228 entries is complete. The rest of this paragraph keeps the 11/14 audit wording. The 11/14 round folded nine long-branch labels into their owners (see *Folded 11/14* below), so the registry went from 237 to 228 entries while the mapped code bytes stayed the same. Every transfer out of the mapped instructions lands on mapped code. Code-shaped words in the unmapped bytes do not point at new code. The 719,264 unknown bytes contain no Thumb or ARM code idioms at all. The program enclosure 08000000–08018EC4 is now fully classified. None of the 34 entries without their own C is C work: they are either finished already (3 labels inside installed owners: 0800D570 and 0800D630 in 0800D51C, 08003786 in 08002854) or are assembly interfaces that stay assembly (31). This is a bounded static and coverage verdict, not a proof (see *Limits*). Measured in mapped instruction bytes:

| | Entries | Instruction bytes | Share of 85,578 |
| --- | ---: | ---: | ---: |
| Inside exact C owners (194 replacements, plus 3 internal labels) | 197 | 79,486 | 92.9% |
| Documented assembly interfaces | 31 | 6,092 | 7.1% |
| **Remaining C owners** | 0 | **0** | **0.0%** |

The old README figure (99.8% before the sound install, 104.3% after it, 109.3% now) divides matched bytes *including pools* (93,542 now) by mapped *instruction* bytes, so it mixes two units; the README quotes the instruction-byte share. The table above uses instruction bytes on both sides. No C owner remains; the renderer owner installed in finish pass 6 was the last, 4,288 bytes including pools (two owners and 8,116 bytes before the sound owner was installed; three and 9,800 before the contact owner). (11/14: 191 entries / 60,234 bytes inside exact owners, 5 owners plus 08003786 remaining with 19,252 bytes.)

## Map completeness: evidence

All counts come from `tools/map_completeness.py` on a worker with the private ROM, run against the current partition. They were re-run on the integrated 228-entry map; only the entry-edge counts in item 1 and the reachability split in item 7 changed, because nine former entries are now internal labels.

1. **Closure of mapped code.** The audit decoded all 37,704 mapped instructions.
   - 1,068 calls and 5 tail branches land on entries. 3,435 branches land on internal instructions, and so do the 12 reviewed far-jump BLs (11 `far_jumps` entries and the `interior_labels` goto at 080083BA). None lands outside mapped code. (On the 237-entry map: 1,080 calls and 21 branches to entries, 3,419 internal.)
   - PC-relative literals: 2,454 point into RAM, 662 at ROM data, 229 at hardware registers and 416 are scalars. Of the 38 code-shaped literals, 31 point at function entries. Six load `0x083C100D`, the base of an odd-addressed byte table in the mixer (`ldr; adds; ldrb`), which is data. One loads the DMA destination `0x030068A0`.
   - Resolved indirect targets: 205 returns, 167 switch cases and 33 calls. All 33 calls land on entries, including the IRQ table and copied-RAM aliases.
2. **The 11 "unresolved indirect" sites are dead.** They are the BX instructions of libgcc `_call_via_r3` through `_call_via_sp` (08018DEC–08018E14). Each has 0 BL callers and 0 pointer references at any alignment, and none ran in coverage. `progress.json` now reports them as `indirect_sites_unresolved_but_unreferenced: 11`, so no live indirect transfer is unresolved.
3. **References from non-code bytes.** The audit scanned every byte alignment of every non-code byte.
   - 342 distinct odd ROM pointers target unknown bytes. The reviewed Thumb validator rejects 341 of them.
   - The one that passes (0830060E, 16 bytes) has a single unaligned reference from inside signed PCM audio (083A17AA). Its target lies inside a 24,576-byte unknown block between two VRAM-transfer graphics blocks. It is rejected as a coincidence.
   - Aligned ROM pointers to ARM entries: 95. Of these, 80 are the value 08000000 (the ROM base) and 15 are DMA copy sources of mapped ARM units.
   - Aligned copied-RAM pointers to entries: 26. They sit in the DMA tables, the mixer slots 08332E9C/08332EA0, the renderer dispatch table 083E2280 (five entries, all mapped) and the const function-pointer table 080200C4–080200E4. Every target is a mapped entry.
4. **Code-likeness of the unknown bytes**, compared with mapped code:

   | Measure | Mapped Thumb (69.5 KB) | Mapped ARM (16 KB) | Unknown (719 KB) |
   | --- | ---: | ---: | ---: |
   | Thumb BL pairs hitting a function entry | 1,069 | – | **0** |
   | Thumb `bx lr` / `pop {rN}; bx rN` returns | 37 / 147 | – | **0 / 0** |
   | Address-like targets of PC-relative loads | 88% | – | 1.5% |
   | ARM branch words hitting known ARM code | – | 271 | **0** |
   | ARM `bx`, `bx lr`, `ldm sp!, {..pc}` | – | 27 / 19 / 0 | **0 / 0 / 0** |
   | ARM always-condition words | – | 87% | 0.96% |

   - All 159 dense ARM-condition windows lie in 082B6040–082BA490. Each run holds only 7–13 distinct byte values and no branch, BX or stack operation. The enclosing 17,152-byte span has 11 distinct byte values, about 1.84 bits/byte, and repeats every 256 bytes. This is indexed image data next to observed-read and VRAM data.
   - Six tiny spans in 083D00B0–083DC0D8 (8–112 bytes) have BL-shaped halfword pairs. Every halfword in them is at least 0xF000, so they are small negative values between read records. None hits an entry.
   - All 331 `push {..., lr}` halfwords in unknown bytes were rejected in 11/12b.
5. **Program enclosure.** 08000000–08018EC4 is fully classified. Its only unknown bytes were 273 two-byte gaps: 256 zero and 17 Thumb no-operation aligners. Each sits between code or a pool and a word-aligned pool or entry. They are now `fill / alignment-halfword`. Three unknown slots of the const function-pointer table (080200C4, 080200D4, 080200E0) are now `table / code-entry-pointer-array`. The rules are in `tools/rom_map.py` (`refine_unknown_mask`). The span diff is in `docs/finish-1114/mapping-refine.json.gz`. Unknown bytes went from **719,822 to 719,264**.
6. **Copies, IRQ, sound and multiboot.**
   - All 13 DMA copy sources are fully mapped (code, pools and a few data bytes; 0 unknown).
   - The 14 IRQ table slots resolve to 4 mapped entries. The mixer pointer slots resolve to 080076F4 and 08006270.
   - There is no second copy of the cartridge header logo anywhere in the ROM, so the ROM holds no embedded uncompressed multiboot image.
   - The 13 recorded coverage sessions, including the 12,500-frame race, executed no PC outside the static map (MAP4).
7. **Dead code is already mapped.** 182 entries are reachable from reset through code references (191 before the nine reachable labels were folded). 39 have no reference of any kind, and 7 are referenced only from those 39. All 46 never ran in coverage. They are 11 `_call_via` veneers, the unsigned divider 0800027C, `_call_via_lr` 08018E18 and 33 unreferenced C routines that are already installed as exact C. The linker kept unused routines in `.text`, and `.text` is fully mapped.

**Why the 719,264 unknown bytes are not code.** Classified by their neighbours:

| Neighbours | Bytes |
| --- | ---: |
| between data blocks (mostly observed reads) | 333,597 |
| data and graphics | 170,676 |
| between graphics blocks | 153,024 |
| audio | 39,762 |
| compressed and graphics | 15,721 |
| other (tables, text, fill, audio mixes) | 6,484 |

153,387 unknown bytes are in spans that start in the rodata area after the program enclosure (08018EC4–08040000). The rest lie among the asset banks from 08040000 onward. These are untyped sprite fragments, record gaps, image strips and sound data. None of them shows any of the code signals above.

**Limits.** These are static reference and code-shape tests, plus coverage of normal-input routes. They cannot rule out a sequence that nothing references and that uses none of the measured idioms. Nor can they rule out code inside a compressed block that no measured path decodes. The 24 custom-LZ outputs decode to bitmap and bank sizes. A new entry would need new executable evidence, for example a captured PC outside the map. Relabelling data is not such evidence.

## Definition of done

TXRA is **done** when, for the 228-entry map, every entry is one of:

1. an **exact C replacement**, passing the admission gate: complete function through its owner and pool end, historical compiler profile, full rebuilt ROM SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`, and no padding, inline assembly, hand bytes or checker tricks;
2. an **internal label inside an installed exact owner** (fragments become this when their owner installs); or
3. a **documented assembly interface** listed in `docs/map/finish.json`, whose defining machine property `tools/asm_interfaces.py` re-measures on every run. These are reported as assembly and never counted as C.

`progress.json → completion` reports exactly this. Today it reads **228 of 228 complete**: 194 exact C, 3 covered labels (0800D570, 0800D630, 08003786) and 31 assembly interfaces. **No entry remains**; finish pass 6 completed the last one, the C owner 08016DA8. Folding the covered labels would lower the entry count further but would not change any byte total.

Typing the remaining unknown data bytes (sprites, records, sound) is a separate, optional data goal. It does not block the decompilation being done.

## Tracker: every entry without its own exact C

Sizes are registry extents (entry start to end, as in `docs/map/finish.json`). For owners, the second number is the complete owner extent including pools and internal fragments, as used by the checker. No C candidate is left in this table. The road stream owner 08002854 ([note](FINISH2-1115-stream.md)) and the HUD owner 0800421C ([note](FINISH2-1115-hud.md)) left this table on 11/15, when their exact C was installed; the contact owner 080181C0 followed in finish pass 3 ([note](FINISH3-1115-contact.md)), the sound owner 080064A4 in finish pass 5 ([note](FINISH5-1115-sound.md)) and the renderer owner 08016DA8 in finish pass 6 ([note](FINISH6-1115-base.md)).

| Entry | Size | Class | Owner / unit | Best differing bytes | Evidence and next step |
| --- | ---: | --- | --- | --- | --- |
| 08003786 | 2,552 | covered (done) | 08002854 | 0 | Internal continuation inside installed func_08002854 (second scenery pass, reached by the far BL at 0800416A). Kept as a registry entry (native recompiler BL target); `tools/rank_targets.py` reports it as covered. |
| 0800D570 | 192 | covered (done) | 0800D51C | 0 | Internal entry inside installed func_0800D51C. Kept as a registry entry (native recompiler BL target); `tools/rank_targets.py` reports it as covered. |
| 0800D630 | 3,662 | covered (done) | 0800D51C | 0 | Internal body inside installed func_0800D51C; its extent now also contains the folded 0800D960 tail. Kept as a registry entry; reported as covered. |
| 080000C0 | 52 | assembly-only | startup | n/a | Reset code. 2 MSR mode changes and banked stack setup, IRQ hook, then BX to Thumb. |
| 080000FC | 248 | assembly-only | irq | n/a | IRQ dispatcher. 3 MRS/MSR on SPSR/CPSR, mode switch, table dispatch. |
| 080001F4 | 36 | assembly-only | irq | n/a | IRQ return tail. 3 MRS/MSR restoring banked state. |
| 08000218 | 100 | assembly-only | division runtime | n/a | Signed division (target of the 08018E7C/E80 veneer). No frame, 11 flag-predicated instructions. Library attribution provisional. |
| 0800027C | 68 | assembly-only | division runtime | n/a | Unsigned division. No frame, 7 carry-predicated instructions. No reference of any kind and never executed. |
| 080002CC | 88 | assembly-only | renderer private ABI | n/a | Front end. LR is written as a general register 4 times. Calls 08000324, which reads fp/r6/r7/r8/sb/sl on entry. |
| 08000324 | 680 | assembly-only | renderer private ABI | n/a | Reads fp/r6–r8/sb/sl before defining them. 6 XOR swaps, 5 stores below SP, 26 predicated instructions. |
| 080005D8 | 1,224 | assembly-only | renderer private ABI | n/a | Saves r4–r12 and lr, including the scratch register ip, without an APCS frame. 17 XOR swaps, 9 LR writes, 33 predicated instructions. Calls 08000AA0 with a private register contract. |
| 08000AA0 | 320 | assembly-only | renderer private ABI | n/a | Reads fp/ip/r4/r6/r7/r8 before defining them. LR is written as a general register. |
| 08000BF0 | 1,224 | assembly-only | renderer private ABI | n/a | Same shape as 080005D8 (17 XOR swaps, 9 LR writes, 33 predicated instructions). Calls 080010B8 privately. |
| 080010B8 | 336 | assembly-only | renderer private ABI | n/a | Reads fp/ip/r4/r6/r7/r8 before defining them. LR is written as a general register. |
| 08001218 | 1,224 | assembly-only | renderer private ABI | n/a | Same shape as 080005D8. Calls 080016E0 privately. |
| 080016E0 | 452 | assembly-only | renderer private ABI | n/a | Reads fp/ip/r4/r6/r7/r8 before defining them. LR is written as a general register. |
| 08018A54 | 4 | assembly-only | BIOS veneer | n/a | SWI 0x0C (CpuFastSet) then return. 2 callers. |
| 08018A58 | 4 | assembly-only | BIOS veneer | n/a | SWI 0x0B (CpuSet) then return. 4 callers. |
| 08018DE0 | 2 | assembly-only | register-call veneer | n/a | `bx r0`, LR untouched (libgcc `_call_via_r0`). 6 callers. |
| 08018DE4 | 2 | assembly-only | register-call veneer | n/a | `bx r1` (`_call_via_r1`). 2 callers. |
| 08018DE8 | 2 | assembly-only | register-call veneer | n/a | `bx r2` (`_call_via_r2`). 5 callers. |
| 08018DEC | 2 | assembly-only | register-call veneer | n/a | `bx r3`. Dead library member: 0 references, never executed. |
| 08018DF0 | 2 | assembly-only | register-call veneer | n/a | `bx r4`. Dead library member. |
| 08018DF4 | 2 | assembly-only | register-call veneer | n/a | `bx r5`. Dead library member. |
| 08018DF8 | 2 | assembly-only | register-call veneer | n/a | `bx r6`. Dead library member. |
| 08018DFC | 2 | assembly-only | register-call veneer | n/a | `bx r7`. Dead library member. |
| 08018E00 | 2 | assembly-only | register-call veneer | n/a | `bx r8`. Dead library member. |
| 08018E04 | 2 | assembly-only | register-call veneer | n/a | `bx sb`. Dead library member. |
| 08018E08 | 2 | assembly-only | register-call veneer | n/a | `bx sl`. Dead library member. |
| 08018E0C | 2 | assembly-only | register-call veneer | n/a | `bx fp`. Dead library member. |
| 08018E10 | 2 | assembly-only | register-call veneer | n/a | `bx ip`. Dead library member. |
| 08018E14 | 2 | assembly-only | register-call veneer | n/a | `bx sp`. Dead library member. |
| 08018E7C | 2 | assembly-only | state-switch veneer | n/a | `bx pc` into the ARM branch 08018E80 (installed). 45 callers (division). |
| 08018E84 | 2 | assembly-only | state-switch veneer | n/a | `bx pc` into the ARM branch 08018E88 (installed). 9 callers (initializer 08018854). |

No entry is classed as data-misclassified. Every entry decodes as reachable instructions with a valid boundary role.

## Folded 11/14 (no longer registry entries)

Each of these nine labels was a registry entry only because a Thumb `bl` used as a goto beyond the 2 KiB branch range (lr already saved, link value never read) targets it; their other references are local branches or fall-through inside the same owner. Each source is a reviewed `far_jumps` entry in `tools/rom.cfg`, except 08007B40, which is a reviewed `interior_labels` entry. `tools/analyze.py` no longer makes them entries, so their bytes now belong to the owner's extent. No code byte moved between code and data; mapped code stays 85,578 bytes.

| Former entry | Owner | Status | Round note |
| --- | --- | --- | --- |
| 080051FE | 0800421C (exact since 11/15) | shared epilogue; owner now ends 0800520E | [hud](FINISH-1114-hud.md), [install](FINISH2-1115-hud.md) |
| 08006712, 08006740, 08006776, 0800735C, 08007368 | 080064A4 (exact since 11/15) | internal labels; owner now ends 08007378 | [mixer](FINISH-1114-mixer.md), [install](FINISH5-1115-sound.md) |
| 080095C4 | func_08008A88 (exact since 11/2) | shared epilogue, already exact | [small](FINISH-1114-small.md) |
| 0800D960 | func_0800D51C (exact since 11/2) | shared tail, already exact | [small](FINISH-1114-small.md) |
| 08007B40 | func_08007B28 (exact since 11/3) | restart label, already exact | [b40](FINISH-1114-b40.md) |

## Notes for the integrator

- **Provenance of four tiny installed entries.** 08000000 (reset `b`), 08018E18 (`bx lr`, which is `_call_via_lr`), 08018E80 and 08018E88 (the ARM halves of the state-switch veneers) are counted as exact C. Their C forms (a tail call and an empty function) are byte-identical and pass the gate, but the original is startup or libgcc assembly. Together they are 14 bytes. This round left them as they are.
- **Two reviewed boundary lists.** `tools/rom.cfg` now has `far_jumps` (11 BL sources: 08004232, seven in 080064A4, 08008B08, 08008C76, 0800E3DC; the BL is a jump and does not fall through) and `interior_labels` (08007B40 inside func_08007B28; the BL still falls through, and the label is dropped as an entry only after its owner's installed match is checked). Both were merged as their branches validated them; converting 08007B40 to a `far_jumps` entry would need its own regeneration check.
- **Three copies of one rasterizer.** The three 1,224-byte front ends and their helpers have identical measured shapes and are copied to separate IWRAM slots. If they are ever written as `.s` source, one macro body would serve all three.
- **Reproduce** on a worker with the ROM:
  `python3 tools/map_completeness.py --output build/mc.json && python3 tools/asm_interfaces.py --completeness build/mc.json && python3 tools/progress.py`.
  `python3 tools/rom_map.py --refine-diff build/d.json` re-derives the alignment and pointer-slot relabelling without coverage captures. `asm_interfaces.py` exits non-zero if a reviewed entry stops showing its defining property, or if an unmatched entry has no reviewed class.
