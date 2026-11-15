# First-stage findings

This is a 4 MiB ARM7TDMI cartridge with THUMB game code, ARM runtime/rendering
code and serial EEPROM support. The project rebuilds it byte for byte from
assembly, four small C matches, and data slices read from the private base ROM.
Nothing here is a running native PC port yet.

080000C0 establishes stacks and the IRQ hook. THUMB initialization starts at
080020B8, clears RAM and installs a copied IWRAM interrupt handler. The loop
around 08002222 selects high-level scenes; 08007B28/08007B40 contain a large
scene/update path with a six-entry state switch at 08007C4E. These are structural
inferences from calls, back edges and switches, not recovered original names.

080161E8 selects DISPCNT 1444 or 1454: mode 4, BG2 and OBJ enabled, with the
frame-select bit toggled. ARM code at 08017F64 selects framebuffer addresses
06000000 / 0600A000. Arithmetic-heavy code around 080164D0 transforms coordinates;
ARM routines copied from 080002CC and 080165BC onward provide rendering work in
IWRAM. The evidence supports software bitmap rendering. The exact road pipeline,
projection stages and draw ordering have not been reconstructed; calling this
hardware mode-7 rendering would go beyond the evidence.

08015D78 reads KEYINPUT, inverts active-low bits, and computes new presses from
previous state. 08015E20 is a wait loop on an interrupt-updated flag. Interrupt
callbacks and timers therefore belong in the first native runtime scope, not
only the renderer. Link/serial accesses around 080147D0–08014C00 also exist.
Sound around 08005F00–08007B28 uses PSG, FIFO DMA and timers; it copies an ARM mixer and a THUMB routine to IWRAM. Its engine identity
is unresolved. EEPROM support is around 08018A5C–08018DDC, with the version
identifier at 0801FF84. See HARDWARE.md for access sites and limitations.

The detailed map is in `map/`: inferred function extents with confidence and
runtime aliases, bounded switch targets, ROM pointer references, indirect
transfers, DMA code copies and hardware accesses. It deliberately marks
completeness false. No execution trace, emulator boot test, exhaustive indirect
coverage, audio-engine attribution, or proof that the tail of ROM contains no
code has been obtained. Four leaf routines match with the old agbcc backend;
the exact original compiler revision remains unproven.

## Native static-recompiler plan

Translate ARMv4T instructions into C basic blocks using the function and block
map, preserving ARM condition flags, PC pipeline reads, unaligned memory
behavior, THUMB state, signed shifts and fixed-width overflow. Load bytes from
the owner's local ROM at build/run time; never package original data in source.
Use a PC-plus-state dispatcher for indirect transfers and returns. Generate
finite switch dispatch from the 14 proven tables; instrument the IRQ and
register-call paths to collect missing targets and trap unknown PCs explicitly.
Do not assume the current function inventory is exhaustive.

For IWRAM code, map each load span to every recorded run address and preserve
copy order and overlap. Translate at **execution addresses**, not the source-ROM
PC: branch destinations and PC-relative calculations need that distinction.
Record writes/DMA into executable RAM, invalidate cached blocks on modification,
and log any previously unseen code rather than assuming RAM stays immutable.
No EWRAM executable mapping has been proven; support discovery there as well.

Implement a small GBA memory/hardware layer: EWRAM/IWRAM, ROM mirrors, palette,
VRAM/OAM, mode-4 scanout plus BG/OBJ composition and blending, DMA side effects,
PSG/FIFO sound, timers, keypad, serial stubs, IRQ/IME/IF semantics and EEPROM
serial protocol. Start with deterministic scheduling at instruction/block
boundaries, advancing timers and VCount and delivering VBlank interrupts;
refine cycle timing from traces where polling, HBlank or FIFO refill requires it.
BIOS CpuSet/CpuFastSet can be host helpers with original semantics. First validate
boot, menus, save/load and a driving session against an emulator trace, then
replace translated blocks with ordinary C over time.
