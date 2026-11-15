# ROM and execution map

All addresses below are hexadecimal bus addresses; ends are exclusive. ROM
file offset is address minus 08000000. `tools/rom.cfg` drives generation and
replacement. `docs/map/*.json` are reproducible metadata, never raw ROM data.

| Range | Kind / evidence | Confidence |
| --- | --- | --- |
| 08000000–08000004 | ARM branch to 080000C0 | high |
| 08000004–080000A0 | cartridge logo/reserved header bytes; private incbin | high |
| 080000A0–080000C0 | decoded cartridge fields / reserved bytes | high |
| 080000C0–080000FC | reset, IRQ/system stacks, BIOS IRQ hook, BX THUMB initializer; pool | high |
| 080000FC–08000218 | ARM IRQ dispatcher, prioritized interrupt selection | high |
| 08000218–0800027C | signed software division | high semantics; library attribution provisional |
| 0800027C–080002C0 | unsigned software division | high semantics |
| 080002C0–080002CC | entry/IRQ literal pool | high |
| 080002CC–080018B4 | ARM rendering helpers / IWRAM copy sources with embedded literals | high copy evidence; semantics provisional |
| 080018B4–08002000 | unresolved gap / data; not declared executable | low |
| 08002000–080165BC | predominantly THUMB game, platform, audio and drawing routines, pools and switch tables | mixed direct-call high / prologue medium |
| 080076F4–08007B28 | ARM audio mixing routine, copied to 03006AA0 | high |
| 080165BC–08018864 | ARM IWRAM routine sources, literals, some overlapping copy ranges | high copy evidence |
| 08018854–08018A54 | ARM DMA initializer and literal pool; overlaps last copy's tail | high |
| 08018A54–08018DE0 | BIOS wrappers and EEPROM support with pools | high |
| 08018DE0–08018E1C | THUMB register-call veneers and alignment | high |
| 08018E1C–08018E7C | memcpy-style routine and alignment | high semantics |
| 08018E7C–08018E8C | two THUMB-to-ARM veneers | high |
| 08018E8C–08018EC4 | 14-entry IRQ callback table | high |
| 08018EC4–08400000 | data/unresolved (contains EEPROM identifier at 0801FF84) | deliberately not claimed all data |

The broad rows overlap where copy sources overlap; use the nonoverlapping
`map/splits.json` for exact byte coverage. It distinguishes ARM, THUMB, literal,
and unresolved spans. Unresolved does **not** mean non-executable. Discovery now
scans pointer-shaped words throughout all 4 MiB, with bounded leaf/prologue
validation and recursive descent. This has not established executable code
beyond the existing program region. The exact code/data/fill partition is now
`tools/rom.cfg` → `mapping`; the older splits inventory describes instructions
and pools only. Byte identity proves encoding and
placement, not that every candidate classification is semantically correct.

## Header and startup

Entry word EA00002E branches to 080000C0. The title field is TXRA followed by
padding; game code BTZE, maker field 4Z, fixed byte 96, main-unit code 00,
device type 00, software version 00, complement checksum 4F, and zero reserved
fields. The header checksum is validated by the verification tool; the copyrighted logo remains an incbin slice.

Reset selects IRQ mode 12 and stack 03007FA0, then system mode 1F and stack
03007F00. It stores 080000FC to 03007FFC and BXes to 080020B9 (THUMB 080020B8).
That initializer disables IME, forces blank, initializes WAITCNT, uses DMA3 to
zero EWRAM and most IWRAM, then copies 800 bytes starting at 080000FC to
03004DE0 and updates the IRQ hook. These copied bytes include adjacent code and
literals: 800 bytes is a transfer size, not the IRQ handler's function size.

The IRQ dispatcher checks timer1 first (bit 3), then VBlank/HBlank/VCount and
remaining bits in increasing order. The callback table starts at 08018E8C.
Most entries use the empty callback 08015DA4; VBlank uses 08014E8C, VCount uses
08015D68, timer callbacks use 08015CF0. Runtime IRQ entry is 03004DE0.

`map/copies.json` records that transfer, two sound-init code transfers from 08007398,
and ten later DMA copies from 08018854,
called via 08018E84. Their sources, destinations, lengths, modes, and triggers
are explicit. The audio copies are ARM 080076F4→03006AA0 (960 bytes) and THUMB
08006270→030068A0 (1E0 bytes). DMA aligns the latter
source pointer 08006271. Some ranges include mixed code/data tails, overlap,
and provide multiple runtime aliases.
No executable EWRAM copy or self-modification has been proven. Preserve every
DMA in sequence; a recompiler must not treat these as disjoint linker sections.

## Machine-readable inventories

- `map/functions.json`: start, exclusive reachable end, ARM/THUMB mode,
  confidence/evidence, discontiguous reachable instruction spans and IWRAM
  aliases. Ends exclude literal pools and are inferred, not original symbol sizes.
- `map/pointers.json`: bounded even-PC THUMB switch tables, their complete target
  lists, contiguous pointer-table candidates, and individual pointer references.
  Adjacent words in a copy initializer's literal pool are candidates, not proven
  callback arrays. The IRQ table is independently confirmed by the dispatcher.
- `map/indirect.json`: every decoded BX / MOV-PC site, register, return pattern,
  locally known target, and bounded switch targets where recovered.
- `map/hardware.json`: exact resolved access sites, values when provable,
  candidate I/O literals, unresolved memory bases, and known RAM references.

The function list is a **candidate inventory, not complete**. The reviewed
IRQ epilogue is now included in this inventory, bringing it to 229 entries
(205 THUMB, 24 ARM); it is no longer counted only in a supplemental native map. Entry/IRQ paths,
BL targets, literal BX targets, copy starts, pointer tables, and unreferenced
PUSH-LR prologues seed recursive decoding. Fourteen bounded switch tables recover
many internal blocks. Branch targets are labels, not automatically functions.
Unresolved callback values, unreferenced leaves, RAM aliases, and the tail of the
ROM need runtime coverage before a static recompiler can claim completeness.


## Whole-ROM code and data pass

Every span in `mapping` records only file offset, size, type and format. Spans
partition the whole image without gaps or overlaps; unknown spans explicitly
remain unknown. Code takes precedence over all data heuristics, and named
structures take precedence over generic read evidence. Percentages use the
whole ROM as denominator. Data on the board includes header, pools, tables,
graphics, audio, text and fill; fill is also reported separately here.

| Classification | Bytes | ROM share |
| --- | ---: | ---: |
| code | 85,132 | 2.0297% |
| data | 147,511 | 3.5169% |
| graphics | 1,033,288 | 24.6355% |
| audio | 504,914 | 12.0381% |
| table | 1,224,000 | 29.1824% |
| text | 27,395 | 0.6531% |
| compressed | 327,791 | 7.8151% |
| fill | 122,281 | 2.9154% |
| unknown | 721,992 | 17.2136% |

The original instruction-only measurement was 85,096 bytes and zero mapped data
bytes. Code now includes the 36-byte executed IRQ epilogue. The larger improvement
is data evidence, not a claim that thousands of additional functions were found.
`progress.json` preserves all milestone fields and the board's exact ROM keys.
`functions_found` counts candidate starts; instruction coverage is the union of
code spans, never a sum of overlapping function extents or IWRAM aliases.

## Region inventory

These rows summarize 256 KiB file-offset windows, with exclusive ends. Assets
can cross window boundaries. Exact small blocks and formats are in the config;
no row claims that its unobserved gaps are data simply because neighbors are.

| Offset window | Code bytes | Data + fill bytes | Unknown bytes | Known contents |
| --- | ---: | ---: | ---: | --- |
| 000000–040000 | 85,132 | 56,489 | 120,523 | data, table, text |
| 040000–080000 | 0 | 204,946 | 57,198 | data, table |
| 080000–0C0000 | 0 | 262,144 | 0 | table |
| 0C0000–100000 | 0 | 262,144 | 0 | table |
| 100000–140000 | 0 | 262,144 | 0 | table |
| 140000–180000 | 0 | 248,038 | 14,106 | data, graphics, table |
| 180000–1C0000 | 0 | 262,144 | 0 | graphics |
| 1C0000–200000 | 0 | 262,144 | 0 | graphics |
| 200000–240000 | 0 | 262,144 | 0 | graphics |
| 240000–280000 | 0 | 161,214 | 100,930 | compressed, data, graphics |
| 280000–2C0000 | 0 | 136,245 | 125,899 | compressed, data, graphics |
| 2C0000–300000 | 0 | 210,935 | 51,209 | compressed, data, graphics |
| 300000–340000 | 0 | 148,824 | 113,320 | audio, compressed, data, graphics, table |
| 340000–380000 | 0 | 261,053 | 1,091 | audio |
| 380000–3C0000 | 0 | 201,556 | 60,588 | audio, data, table |
| 3C0000–400000 | 0 | 185,016 | 77,128 | data, table |

## Coverage method and evidence

`--coverage <private-output.json>` enables metadata-only logging in the PC build.
The normal build takes no coverage allocations. Successful instruction ticks
record every unique guest PC and ARM/THUMB state, including copied RAM code.
The shared branch helper records computed transfers, interworking and returns.
Reads record the exact accessed ROM bytes through all wait-state mirrors; host
fingerprint checks and video rendering do not become guest ROM reads. DMA logs
aligned source extents, including fixed and decrementing sources. CpuSet and
CpuFastSet log source sizes with fill and rounding accounted for.

LZ77, RLE and Huffman SWI source scanners validate headers, backward references,
tree bounds and consumed compressed sizes. These are metadata scanners, not new
BIOS service implementations: an unsupported decompression SWI still stops the
game explicitly. No such SWI was executed on these routes, and no referenced
valid BIOS-compressed block was established. Synthetic tests cover all three
formats. Signatures alone are not accepted as compressed assets. Format rules
were checked against the primary [BIOS implementation reference](https://github.com/mgba-emu/mgba/blob/master/src/gba/bios.c);
no external implementation was copied into the runtime.

The logger deduplicates sets, not chronological traces. It retains every unique
executed PC/read byte/branch edge/transfer tuple; a full record table marks the
capture incomplete and fails the run. Captures carry a ROM CRC, and mapping tools
reject the wrong fingerprint. RAM execution maps back only through a unique
established copy alias. The native build's existing encoding guards remain in
place; this pass observed no modified-code fallback or ambiguous RAM aliases.

Static recursive descent drains its complete work queue before adding uncovered
runtime PCs. This ordering matters: arbitrary mid-block seeds can destroy the
local constants used for literal pools and switches. A regression test compares
all assembly and inventory outputs with and without already-covered PC seeds.
No captured PC lies outside the final static code map. Coverage, config and review artifacts contain metadata only; no ROM payload,
decoded asset, string or sample content is serialized in those artifacts.

`docs/map/coverage.json` records thirteen scenarios and aggregate coverage. The original six routes are joined by three course-selector probes, three pause-choice probes and a results-choice probe. These probes do not establish another driven course or replay.
The scenarios cover boot/name entry/car purchase, Quest, Quick Race, Time Attack,
Free Run, Change Car, Parts Shop, all five options categories, save, reload and a
complete battle-race loss. Inputs are deterministic keypad scripts, with fresh
isolated EEPROM paths. This is root-screen coverage, not every possible submenu,
part purchase, car, race, course or career branch.

The round 3 full-race run has 1,170,372,096 native instructions with zero fallback,
unknown execution targets or unsupported instructions. The round 3 race matches every one of the round 2 race's 12,500 frame hashes and every final
machine/audio/stat field other than elapsed host time. Save and reload also have
zero fallback; reload leaves the EEPROM hash unchanged. Aggregate PC, branch and
read counts are available in the coverage summary without committing raw logs.

## Data formats and remaining unknowns

Audio is a custom engine, not an assumed standard sound driver. Mixer instructions
at 08007780 and 0800733C establish 16-byte sample records: ROM pointer, declared
byte length, loop control and another field. The length includes four bytes that
the mixer excludes from its fixed-point limit. The 20-byte refill records used
at 080062C0 carry a pointer and a duration in 176-sample periods; their pitched
variant has a fixed-point source limit at +16. Descriptors and signed PCM extents
are classified from those layouts. Song channel maps, sequence opcodes and voice
parameter tables are only partly understood; generic read/table ranges retain
that uncertainty rather than receiving invented exact sequence boundaries.

ROM-to-palette transfers establish BGR555 palette bytes; ROM-to-OAM transfers
establish attribute data. VRAM transfers establish graphics sources, but do not
by themselves distinguish 4/8bpp tiles, indexed bitmaps, tilemaps or affine
lookup data. Those formats stay explicit as unresolved in their format labels.
Referenced null-terminated printable ASCII ranges are text; no text content is
exported. Consecutive ROM pointers and decoded literal/switch spans are tables.
Long FF runs and terminal zero runs are fill evidence; interior zero regions
are not automatically padding, and known structures override fill heuristics.

The remaining bytes lack enough proven structure to claim exact extents. Large course and texture banks are now mapped; their internal semantics remain incomplete. A ROM read proves only that byte, not its whole
neighboring asset. Track/course records, sprite layout tables, affine tables,
nonstandard compression and unreferenced leaf code still need further semantic
work and broader course/career coverage. Eleven unresolved indirect sites are
unexecuted register-call veneers (08018DEC–08018E14); none was executed in these
sessions. All observed indirect targets are native, but that does not prove
all possible targets or every function has been found. This pass is incomplete
at full-ROM classification, and the unknown count is intentional.

## Round 3 structural proofs

Unknown bytes fell from 2,773,133 to 723,196 (2,049,937 fewer). Code remains
85,132 bytes and 229 candidate functions. Mapped data including fill is now
3,385,976 bytes. The improvement comes from complete structures, rather than
expanding a read byte to a guessed neighboring asset.

`docs/map/structures.json` gives a separate evidence line for every new range,
including consumer sites, pointer/count slots and dimensions. Each final config
range's `format` selects its evidence line in `format_evidence`. Overlapping
structural proofs are retained in the inventory; the final config partition
counts each byte once, with code taking precedence.

- Six course arrays at 080CF330, 080E0B4C, 080FC468, 0811216C,
  0812ADCC and 08148CF8 contain 681,940 bytes. Literal-selected counts
  (2,561 / 4,033 / 3,191 / 3,624 / 4,381 / 6,565) and the wrap logic establish
  their bounds. Two independent consumers compute index × 28 and read fields
  within that record. This establishes records, not complete course semantics.
- The 524,288-byte projection table at 0804F330 has 131,072 signed words,
  indexed by signed depth/2 + 65,536. Every nonzero positive/negative pair
  is antisymmetric, the positive half is monotone, and every value differs by
  less than one integer unit from 524,288/index. Zero and boundary sentinels
  are checked. This arithmetic shape explains bytes that superficially resemble
  instructions or arbitrary scalar data.
- Twenty-four referenced reverse byte LZ/RLE containers occupy 327,791 source
  bytes. The routine at 0801251C consumes commands from the end: literals,
  repeated bytes, forward absolute copies and backward absolute copies. The
  caller supplies output length; the tool verifies every copy reads already
  initialized output and both ends match exactly. Sixteen blocks decode to
  65,536 bytes, seven to 38,400 bytes and one to 62,880 bytes. A separate guest
  CPU execution matches all 24 complete output hashes. Output bytes are never
  written to metadata or committed. BIOS LZ77/RLE/Huffman decoders also have
  synthetic output tests; no valid referenced BIOS block was established here.
- Twenty-three aligned trailers, independently referenced and with 256 valid
  15-bit color words each, establish 11,776 palette bytes. These are attached
  to checked indexed-byte containers; merely finding a high-bit-clear run
  elsewhere does not classify a palette.
- The software rasterizer's source table selects fourteen consecutive 65,536-byte
  indexed texture banks (917,504 bytes). Its byte fetch computes y × 256 + x
  from unsigned eight-bit coordinates and packs pixels to the framebuffer.
  The banks are linear indexed sources, not automatically tile sheets. A small
  isolated source in that table is deliberately excluded from the full-bank
  classifier because its UV bounds are narrower.

The full-ROM pointer scan and recursive descent were repeated against the new
coverage. No additional validated function start or instruction span emerged.
The 206 newly executed PCs were already in the static map; 63 candidate function
entries remain unexecuted after accounting for their copied RAM aliases.
`docs/map/round3-audit.json` lists those entries and session deltas. Its register
entry records contain only selected decoder source/destination/count arguments
and numeric screen IDs with frame numbers. They do not contain text or pixels.

## Still unknown and why

721,992 bytes remain unknown. Raw sprite fragments, layout/attribute records,
small texture sources, course-related auxiliary tables and sound sequence or
instrument data still lack reliable complete bounds or sufficiently understood
consumers. Interior zero bytes remain data candidates, not assumed padding.
VRAM transfer sources retain unresolved tile/map ordering when a transfer alone
cannot distinguish 4bpp, 8bpp, affine or map data. No new OAM table or note-opcode
format was proven. No valid referenced BIOS compressed stream was found; a
signature alone is insufficient evidence.

Normal-input probes changed course choices and exercised additional pause/menu
paths, adding 206 executed PCs and 12,643 read bytes over round 2. The probes
returned no reads from a different course array. Alternate course starts,
career progression gates, part purchases, complete results branches and replay
entry therefore remain unverified. The two replay-related entry points at
08012CC8 and 08012EB8 were not observed. Fresh test saves do not provide an
advanced career; no unlock flag, save or ROM was patched to manufacture reach.

## Round 4 referenced-code audit

`tools/code_audit.py` checks all 2,093,759 bytes classified as table,
unknown or generic data in the round 3 baseline. It reads pointer slots at **every byte alignment**,
including isolated callbacks and packed records crossing classification boundaries;
no table stride or original program-region cutoff restricts the search. It also
decodes direct BL targets from established ARM and THUMB spans and follows resolved
BX/veneer targets through unique copied-code aliases. Unresolved aliases remain
explicit rather than being assigned an invented ROM destination.

The metadata journal `docs/map/code-audit.json` contains **927 distinct targets**
from 2,031 odd ROM-pointer references, 1,078 direct calls and 200 resolved indirect
references. Each target retains its reference offsets, original target
classification, disposition and reason:

| Disposition | Targets |
| --- | ---: |
| Already inventoried function entry | 193 |
| Internal bounded-switch target, not a function call | 167 |
| Rejected for acceptance / not established as code | 567 |
| Additional validated function proposal | 0 |

The validator explores conditional paths and allows stores, unlike the older
linear leaf heuristic. It checks ARMv4T encodings, complete reachable decoding,
instruction boundaries, literal conflicts, stack depth, saved return-address
position and explicit returns. Calls must preserve the original return address.
Unresolved transfers, wrong instruction mode, fallthrough into undecodable bytes,
invalid stack use and exhausted validation budgets all retain explicit reasons.
An unsuccessful validation is **not** proof that an unknown range is data.
All 101 budget-limited targets lie inside the independently validated signed
reciprocal lookup structure; the report preserves the limit rather than pretending
they were fully decoded. New ARM call targets would require separate manual
validation; none was found by this pass.

This pass establishes **no additional function or code byte**. The inventory
remains 229 entries (205 THUMB, 24 ARM) and 85,132 instruction bytes; all 229 are
emitted by the native recompiler. Existing switch labels are not promoted to
function entries to increase the count. Several existing routines are large:
the five largest reachable extents contain 5,712, 4,676, 4,212, 3,740 and 3,706
instruction bytes. ROM size and function count alone do not establish missing
executable code. Unreferenced code, unresolved indirect paths and unvisited career
states remain possible; this audit does not claim exhaustive function recovery.

Thirteen deterministic coverage sessions now include a second results-choice
probe and a third pause-choice probe. The latter adds 35 executed PCs and 13,412
read bytes relative to the eleven reproduced round 3 routes; all new PCs were
already in established static instruction spans. Neither probe executes the
unobserved replay entries at 08012CC8 and 08012EB8. `docs/map/round4-audit.json`
retains per-session deltas, screen IDs and remaining unexecuted function entries.

The fresh 12,500-frame race executes 1,170,372,096 native instructions, with zero
fallback, unknown targets or unsupported instructions. Every final machine and
audio field matches the recorded round 3 race summary except elapsed host time.
All thirteen sessions have zero fallback/unknown/unsupported steps and no executed
PC outside the static map after unique IWRAM alias translation. Save/reload
integrity is checked with isolated saves. Current per-frame hashes were recorded;
the previous raw hashes are unavailable for a fresh frame-by-frame comparison.

New read/transfer evidence reduces unknown bytes from 723,196 to **721,992**,
a decrease of 1,204. Mapped data including fill is **3,387,180** bytes. The exact
partition has 948 more generic read-data bytes and 256 more graphics-transfer
bytes; these are data gains, not additional executable code. The 35 extra PCs
add no instruction bytes because they were already statically mapped.

The scan does not automatically publish seeds or change classifications.
Review any future proposal, add a referenced entry to `seeds`, regenerate the
inventory with `tools/analyze.py`, and then rebuild and capture normal-input
coverage before accepting a code range. Code continues to override data evidence
in the partition. No candidate was accepted here, so no code/data boundary was
changed merely to make the totals increase.

## Reproduction

With the private supported ROM in the root, build and record into a fresh ignored
directory. Keep all captures and coverage logs private. No browser is needed.

```sh
make check recomp check-runtime check-controller
python3 tools/coverage_run.py build/coverage/screens --round3
./build/txra-pc --headless --mute --benchmark --frames 12500 \
  --input-script tests/race-input.txt --save build/coverage/race.sav \
  --coverage build/coverage/race-coverage.json --stats build/coverage/race.json \
  --frame-hashes build/coverage/race.hashes
python3 tools/rom_map.py build/coverage/*-coverage.json build/coverage/screens/*-coverage.json
python3 tools/check_structures.py
python3 tools/progress.py
```

For the round 4 audit, save copies of `tools/rom.cfg` and
`docs/map/functions.json` in ignored `build/map4/` before changing classifications.
Use fresh directories for every coverage run. The coverage runner's `--round4`
includes all earlier probes and the two new probes; `--scenario results-next
--scenario pause-third` runs only those additions. `make code-audit` writes the
rejection journal without changing the function map. `make check-code-audit`
runs its synthetic tests. The normal `make check` includes them too.

The split capture used for this handoff is reproducible with:

```sh
python3 tools/coverage_run.py build/map4/screens --round3
python3 tools/coverage_run.py build/map4/extra --scenario results-next --scenario pause-third
# Run the 12,500-frame race command above with output names under build/map4/race/.
python3 tools/rom_map.py build/map4/race/*-coverage.json build/map4/screens/*-coverage.json build/map4/extra/*-coverage.json
python3 tools/mapping_audit.py --baseline build/map4/race/*-coverage.json build/map4/screens/*-coverage.json --sessions build/map4/race/*-coverage.json build/map4/screens/*-coverage.json build/map4/extra/*-coverage.json --baseline-label round3 --output docs/map/round4-audit.json
python3 tools/review_map4.py <private-review-folder> --before-config build/map4/before-config.json --before-functions build/map4/before-functions.json
```

The review renderer requires a clean 12,500-frame session named `race` in the
coverage summary. Keep its stats beside `race-coverage.json` as `race.json`.
The handoff's final-state comparison uses the preceding metadata race summary;
original per-frame hashes were unavailable for comparison, so matching all prior
12,500 framebuffer hashes is not claimed. Current hashes remain private.

`make` retains full ROM SHA-1 verification. `make recomp` consumes the expanded
inventory; generated C and ROM bytes remain ignored. To inspect dynamic code
supplements explicitly, run `tools/analyze.py --coverage <capture paths>` with
the configured Python environment. The current captures add no extra code beyond
the integrated IRQ epilogue. Metadata-only review pictures and the muted 30 fps
WebM are generated by `tools/review_map.py`, using Pillow and an external encoder.

## Unreferenced code gaps, 12 November

Eight complete static candidates were recovered between established routines, including six frameless state/DMA leaves, a link request setter and an EEPROM retry wrapper. The inventory now contains **237 entries (213 Thumb, 24 ARM)** and **85,578 instruction bytes**. Unknown bytes fall from 721,992 to **721,370**; 446 become code and 176 become literal-pool tables. Existing observed read, transfer and execution evidence is preserved. These eight routines have **no reviewed runtime execution evidence**; their names remain suggestions, and the exact-match registry is separate. See [targets and classifications](near-misses/breadth-1112/TARGETS.md) and [boundary review](near-misses/breadth-1112/mapping-review.json).

All eight 11/12 candidates now have complete C replacements verified by the full cartridge rebuild: **189 exact replacements, 73,162 bytes including pools**. All **237** mapped entries compile in the native build; the eight new entries still have no reviewed execution evidence. [Breadth ship note](MATCH1112-SHIP.md).

## 12 November, second breadth review

The early unclassified enclosure at 080018B4 is the shared ARM rasterizer's halfword reciprocal table. The complete 1,025-entry shape is now independently checked, including all rounded Q15 values, the zero-index sentinel and the first following nonmatching halfword. Its 2,050-byte extent ends at **080020B6**; the next two-byte aligner remains outside the table. The classification recovers **1,548 unknown bytes**, reducing the current unknown total to **719,822**. All old read evidence, session totals, function entries and exact replacement records are preserved. This adds **zero functions and zero C matches**: the registry remains **189 of 237**, covering **73,162 bytes including pools** and **85,578 mapped instruction bytes**. [Mapping proof and preserved prior partition](near-misses/breadth-1112b/raster-mapping.json).

## 14 November map-completeness audit

`tools/map_completeness.py` checks four things against the current partition: closure of the mapped instructions, code-shaped references from every non-code byte, code idioms in every unknown span, and the coverage of the copy sources. Its receipt is `docs/finish-1114/completeness.json.gz`.

- All 1,101 direct calls and tail branches to entries, and all 3,419 internal branches, land on mapped instructions.
- Every code-shaped literal and every resolved indirect target lands on an entry. The exceptions are data: a byte-table base and a DMA destination.
- The 11 unresolved indirect sites are dead libgcc `_call_via_r3`…`_call_via_sp` members, with no reference of any kind.
- The unknown bytes contain no Thumb BL to any entry, no Thumb return idiom, no ARM branch to known code, and no ARM `bx` or stack return. The only dense ARM-condition runs are periodic image data at 082B6040–082BA490.

Two reviewed rules in `rom_map.py` (`refine_unknown_mask`) label the last unknown bytes in the program enclosure:

- 273 two-byte aligners become `fill / alignment-halfword` (546 bytes);
- three unknown slots of the const function-pointer table at 080200C4 become `table / code-entry-pointer-array` (12 bytes).

Unknown bytes fall from 719,822 to **719,264**. Function count and code bytes are unchanged at **237 entries / 85,578 bytes**. The map is judged complete; see the verdict and its limits in [FINISH.md](FINISH.md). `rom_map.py --refine-diff` reproduces the relabelling without private coverage captures. The span diff is in `docs/finish-1114/mapping-refine.json.gz`.
