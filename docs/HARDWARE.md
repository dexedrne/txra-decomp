# Hardware scope for native recompilation

The static pass resolves 504 I/O access sites at 46 distinct addresses. This is
an inventory of **proven local addresses**, not an exhaustive dynamic hardware
trace. Each read/write, width-bearing mnemonic, source PC and known write value
is in `map/hardware.json`. Unknown bases remain in `unresolved_memory`; literals
that look like I/O addresses are separately marked as candidates. A 32-bit
access can cover two adjacent halfword registers. Ranges copied by DMA can touch
more registers/memory than their setup instruction's direct address.

## Resolved register accesses

| Address | Register | Access | Example ROM PC | Sites |
| --- | --- | --- | --- | --- |
| 04000000 | DISPCNT | read / write | 080020D0 | 12 |
| 04000004 | DISPSTAT | read / write | 0800212C | 5 |
| 04000006 | VCOUNT | read | 080083E0 | 3 |
| 0400000C | BG2CNT | write | 08007BCC | 9 |
| 04000050 | BLDCNT | write | 08007BD4 | 4 |
| 04000052 | BLDALPHA | write | 08007BDC | 4 |
| 04000054 | BLDY | write | 08007BE2 | 4 |
| 04000060 | SOUND1CNT_L | write | 0800745A | 1 |
| 04000062 | SOUND1CNT_H | write | 0800608A | 5 |
| 04000064 | SOUND1CNT_X | write | 0800608E | 8 |
| 04000068 | SOUND2CNT_L | write | 08006098 | 5 |
| 0400006C | SOUND2CNT_H | write | 0800609C | 7 |
| 04000070 | SOUND3CNT_L | write | 08007432 | 1 |
| 04000072 | SOUND3CNT_H | write | 080060A6 | 5 |
| 04000074 | SOUND3CNT_X | write | 080060AA | 8 |
| 04000078 | SOUND4CNT_L | write | 080060B4 | 5 |
| 0400007C | SOUND4CNT_H | read / write | 080060B8 | 7 |
| 04000080 | SOUNDCNT_L | read / write | 080064D8 | 5 |
| 04000082 | SOUNDCNT_H | read / write | 0800742C | 4 |
| 04000084 | SOUNDCNT_X | write | 08007424 | 2 |
| 040000B8 | DMA0CNT | write | 08014EB0 | 3 |
| 040000BC | DMA1SAD | write | 0800640C | 1 |
| 040000C0 | DMA1DAD | write | 080063FA | 1 |
| 040000C4 | DMA1CNT | read / write | 080063F4 | 4 |
| 040000C8 | DMA2SAD | write | 0800642E | 1 |
| 040000CC | DMA2DAD | write | 08006426 | 1 |
| 040000D0 | DMA2CNT | read / write | 08006420 | 4 |
| 040000D4 | DMA3SAD | write | 080020EA | 81 |
| 040000D8 | DMA3DAD | write | 080020F0 | 81 |
| 040000DC | DMA3CNT | read / write | 080020F4 | 157 |
| 040000DE | DMA3CNT_H | read | 08018AE0 | 1 |
| 04000100 | TM0CNT | write | 08002132 | 4 |
| 04000104 | TM1CNT | write | 0800641C | 3 |
| 0400010C | TM3CNT_L | write | 08014928 | 2 |
| 0400010E | TM3CNT_H | write | 080149CE | 4 |
| 04000120 | SIODATA32 / SIOMULTI0 | read | 08014AF0 | 1 |
| 04000124 | SIOMULTI2 | read | 08014AEE | 1 |
| 04000128 | SIOCNT | read / write | 080147C2 | 8 |
| 0400012A | SIOMLT_SEND | write | 08014B08 | 2 |
| 04000130 | KEYINPUT | read | 08015D7C | 1 |
| 04000134 | RCNT | write | 080147F0 | 1 |
| 04000200 | IE / IF (word access) | read / write | 08000104 | 14 |
| 04000202 | IF | write | 08014922 | 2 |
| 04000204 | WAITCNT | read / write | 080020D8 | 3 |
| 04000208 | IME | read / write | 080020C8 | 17 |
| 0D000000 | EEPROM serial aperture | read | 08018D02 | 2 |

## Display and memory

080161E8 selects DISPCNT 1444/1454: mode 4, BG2 and OBJ, one-dimensional OBJ
mapping, and alternate framebuffer selection. This write crosses a branch,
so its value is established by manual inspection rather than the local
propagator. 08017F64 selects 06000000 / 0600A000 framebuffers. BG2CNT writes
include C083. Palette, bitmap VRAM and OAM transfers occur through DMA3 and
pointer-based rendering; implement their memory regions even when individual
pixel addresses cannot be statically enumerated. Blending registers are used.
No resolved direct write to BG2/BG3 affine matrix/reference registers was found;
that is not proof of absence through DMA or unresolved indexed stores. Mode 4
uses an affine-capable BG, but software road projection is the current inference.

## DMA, interrupts and timing

DMA3 clears EWRAM/IWRAM, installs the IRQ handler and transfers rendering data
and executable code. Its source, destination and full control/count writes must
have immediate memory side effects. Fixed-source and incrementing transfers,
16/32-bit widths and register reads after transfers are visible. DMA1/2 are
configured for FIFO A/B with destination 040000A0 / 040000A4 and control
BE400000. DMA0 control is cleared; its full runtime use is unresolved.
Timers 0/1 configure audio pacing; timer3 and serial interrupt flags also appear.
DISPSTAT, VCOUNT, IE, IF, IME and WAITCNT all need modeled behavior. IRQ dispatch
prioritizes timer1, then display interrupts and other sources; do not collapse
all events into one host frame callback. The spin at 08015E20 requires scheduled
interrupts to make progress. Preserve IF acknowledgement and BIOS IRQ-hook
conventions at 03007FFC.

## Audio and serial input

The game writes PSG channels 1–4, master/mixing control and wave-channel
registers. 04000090 is also present as a wave-RAM literal. FIFO A/B addresses are
confirmed as DMA destinations, not CPU direct-store sites. A hardware layer
needs PSG/wave behavior plus timer-driven FIFO consumption and DMA refill;
two more DMA transfers at 0800747E/0800748A copy an ARM mixer
(080076F4→03006AA0, 960 bytes) and THUMB support
(08006270→030068A0, 1E0 bytes). Engine identity is unproven. KEYINPUT at 04000130 feeds the active-low input and
edge calculation at 08015D78. SIOCNT and multiplayer registers, RCNT and timer3
are touched by link support; begin with explicit deterministic disconnected-link
behavior, then verify menus do not wait forever on it.

## EEPROM and BIOS

08018A5C chooses a descriptor for 4/64 size arguments. Transfer support at
08018AA4 uses DMA3 and waits for completion; reads from 0D000000 occur at
08018D02 and 08018D2C. EEPROM block support occupies 08018B24–08018DDC and the
EEPROM_V124 marker is at 0801FF84. Writes/commands can reach the aperture via DMA,
so a direct-STR scan alone misses them. Implement serial command/address/data
bits and completion behavior; the selected capacity and actual game save layout
still require trace verification. Keep saves additive when introducing host
persistence; no existing game save was modified in this stage.

CpuFastSet (SWI 0C, 08018A54) and CpuSet (SWI 0B, 08018A58) are proven. Other
BIOS services were not found in decoded paths. No emulator boot, save round-trip,
cycle timing, controller session or audio comparison has been run yet. These
are the validation gaps for the next stage, not silently assumed successes.

Register semantics reference: [GBA hardware documentation](https://mgba-emu.github.io/gbatek/).
