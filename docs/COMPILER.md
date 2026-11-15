# Compiler evidence

The THUMB code is consistent with the GCC 2.9 / 2.95-era ARM toolchain family
preserved by agbcc. Exact vendor release and original project flags remain
unproven. `old_agbcc` is a working matching compiler, not a proven identification
of the original executable.

Four independently compiled C routines match exactly using `-O2
-mthumb-interwork`: 0800D188 (24 bytes including pool/alignment), 08014518
(12), 080147C0 (16), and 08015DA4 (2). The last is an empty leaf and carries little
compiler-identification weight. The other three match register choices, ordering,
instructions, PC-relative pool placement, constants, and alignment.

The regular agbcc variant also produces the same assembly for these examples.
These leaves therefore do not distinguish old/new agbcc variants. Their generated
banner is `gcc 2.9-arm-000512 for Thumb/elf`. GCC 14.3.1 with `-O2 -mthumb
-mcpu=arm7tdmi` differs: the clear routine uses r2/r3 rather than r0/r1 and loads
zero before the address; the bitfield getter uses left/right shifts instead of
AND plus shift. Modern devkitARM is not installed or experimentally compared;
its GCC lineage alone is not evidence of an exact match.

A larger sample at 080020B8 saves r4-r7/lr, moves high registers into low
registers, saves those, and returns by popping the saved return address into a
low register then BX. The ROM also uses even-PC THUMB switch tables and
register-call veneers. These support the older GCC interpretation but are not
unique compiler fingerprints. ARM routines such as 08018854 use `mov ip, sp`,
full frame-register saves, and an fp-based epilogue, unlike the hand-oriented
entry/IRQ code.

## Runtime library and BIOS evidence

- 08000218 is a signed software division routine, with sign normalization and
  shift/subtract division; 0800027C is unsigned division. 08018E7C switches to ARM
  then branches to 08000218. `__divsi3` / `__udivsi3` are provisional semantic
  names, not a verified symbol recovery. A separate `__modsi3` is not identified.
- 08018DE0 through 08018E18 are four-byte `_call_via_rX`-style BX veneers,
  followed by padding. The actual register is recorded in `map/indirect.json`.
- 08018E1C behaves as memcpy: aligned 16-byte chunks, then words, then bytes,
  returning the original destination. Attribution to a particular library
  revision has not been established.
- 08018A54 uses THUMB SWI 0C (CpuFastSet); 08018A58 uses SWI 0B (CpuSet).
  No LZ77, Huffman, or BIOS Div call has been found in decoded code. This is not
  proof of absence in unresolved regions.
- 08018A5C selects EEPROM geometry for sizes 4 and 64; 08018AA4 is DMA transfer
  support; 08018B24 / 08018D48 participate in block read/write. 08018D02 reads
  bits from the EEPROM aperture. The EEPROM_V124 identifier is at 0801FF84.
- Sound routines around 08005F00–08007600 touch PSG, FIFO DMA, and timers.
  m4a/Sappy attribution is **not established**. No marker-name match was found
  for the candidate engines searched; absence of a string is weak evidence.

See [the pinned compiler source](https://github.com/pret/agbcc/tree/da598c1d918402c42c0c0d7128ba14567f3175e9)
and [GBA hardware/BIOS reference](https://mgba-emu.github.io/gbatek/).

## ARM tail thunk at 08018E88

The explicit `modern-arm` profile uses the installed GCC 14.3.1 with `-O2
-marm -mcpu=arm7tdmi -mno-thumb-interwork`. It reproduces the entire four-byte
ARM tail branch at 08018E88. Enabling Thumb interworking instead emits a call
with a saved return address. The historical ARM compiler with an omitted frame
pointer retains a redundant save/restore pair before the tail branch.

This is a small interworking trampoline, not evidence that the original program used
the newer compiler. The ARM destination initializes DMA transfers without reading
incoming arguments; its Thumb caller ignores the return value. The emitted branch
leaves all argument and return registers unchanged. The adjacent Thumb state-changing
entry is not included in the replacement. No larger ARM body is claimed here.

Runtime symbol lookup historically prefers Thumb veneers. ARM code can now name
the actual mapped ARM entry as `arm_func_XXXXXXXX`; existing Thumb aliases keep
their prior meanings. ARM branch relocations are checked for instruction shape,
link bit, state, alignment and range, and independently compared with the linker.
## Library return setting

The complete 94-byte copy routine at 08018E1C matches ordinary C with
`old_agbcc -O2 -mno-thumb-interwork`, recorded as `old-no-interwork`.
The same source with interworking enabled emits a different return sequence.
This is evidence for a separately compiled library group, not a reason to
change the surrounding game routines or a definitive vendor identification.
## Verified ARM compilation

The pinned compiler sources also contain an ARM compiler (`gcc_arm`). Building
its `cc1` as `agbcc_arm` with the existing host compatibility changes reproduces
all 252 bytes of 08017E68 under `-O2 -mthumb-interwork`. This includes its APCS
frame, instruction scheduling, indirect interworking calls, embedded pools and
return. An explicit if/else chain produces the dispatch; a switch adds twelve
bytes. This is a compiled-C function, not an assembly-only entry.

`tools/setup.sh` builds this executable in an isolated temporary source copy,
using at most four compiler processes. The explicit `arm` build profile selects
it. The six THUMB profiles, including `old-no-interwork`, retain their flags;
the two ARM profiles are selected only for ARM search targets. ARM functions are
word-aligned. The assembler's `R_ARM_V4BX` records only mark existing BX
instructions for optional compatibility rewriting on older CPUs. ARM7TDMI
supports BX: the matching path validates each marker's alignment, absolute
symbol and BX opcode and leaves those instruction bytes untouched. Unknown
relocations are still rejected. No emitted instruction is patched or supplied
as data.

08018854 independently matches 512 bytes under the same ARM profile. Its DMA
copy ranges require distinct extern start/end markers at shared addresses;
otherwise the compiler merges address lifetimes and pool entries. This gives a
second ordinary-C ARM example with a very different body and delayed frame setup.

## Runtime unit without interworking

The 94-byte copy routine at 08018E1C matches ordinary C with `old_agbcc -O2`
and **without** `-mthumb-interwork` (`old-no-interwork` in the build). Its return
pops directly into pc. The normal interworking profile emits a saved-return
pop followed by BX instead. This is evidence of a separately built runtime
unit, not a reason to change the application-wide flags. The source shape
agrees with the copy routine bundled in the pinned compiler tree: an aligned
four-word loop, a remaining-word loop and a decrement-before-test byte tail.

## Deep slice b diagnostic findings

The pinned tree's ARM backend was built in a local build directory. The smaller
transform at 08016C18 compiles to the same 400-byte length under `-O2` and shows
the same APCS frame family, but its complete bytes differ. The larger standard-
frame routine at 080165BC also produces ordinary ARM C after frame and arithmetic
recovery. Neither is an accepted replacement or an installed compiler profile.
`-O1`, `-O2`, `-Os`, interworking, APCS frame choices and the documented narrow
optimization controls were compared as applicable; none makes the application
candidates exact. The existing blit miss is unchanged when compiled alone or
before/after the assigned strip routine. There is no evidence for a unit-order fix.

The draft layer now distinguishes MLA from long multiplication, resolves simple
ARM literal loads with PC+8, preserves shifted-operand precedence and carries
known runtime-helper arguments through interworking veneers. These are draft
accuracy fixes; the executable decoder already handled MLA. They do not establish
boot or playability. See `docs/DEEP-B-SHIP.md` and `docs/deep-b/LOG.md`.

## Deep matching evidence from slice c

Four larger complete replacements also match under the existing old O2 profile
with Thumb interworking: 08005F8C (228 bytes), 0800B254 (332), 0800A00C
(368) and 0800A68C (532). These comparisons include literal pools and
alignment and pass a byte-identical full ROM build. Indexed records, pointer
formation order, upward source loops and separate destination scopes resolved
the respective allocation/scheduling differences. Flags alone did not.

Placing the neighboring sound routine before or after 08005F8C preserved its
exact bytes. Placing the initializer before or after the 080063D4 buffer draft
preserved that draft's 52-instruction / 114-byte miss. These two checks do not
establish compilation-unit independence for every routine.

At the deep-d baseline, the match compiler/relocation path was Thumb-only.
The merged build now supports historical ARM and modern-arm profiles.
Compiler-shaped ARM bodies 080076F4 and 080181C0 remain unmatched; neither
was converted to hand assembly by inference. See
[the per-entry evidence](asm-only.md) and [the retained C drafts](deep-c/README.md).

Both old and standard Thumb executables are needed by installed replacements.
Setup now builds both variants from the pinned source, serially to respect the
legacy generator dependencies. `diffhint.py` accepts a profile override and
otherwise uses an installed entry's recorded profile; comparisons include
referenced literal tails even when a trial is shorter.

## Constant labels and compilation units

`old_agbcc` gives every constant-pool entry an internal `.LC` label whose number
continues across the whole translation unit. The global CSE pass hashes these
label names when it builds its expression table, and it walks that table in
bucket order when it creates registers for hoisted address constants. The new
register numbers break ties in global allocation. A function can therefore
change register choices depending on how many constants the earlier functions in
its file used, with no change to its own source.

08006070 is the first match that depends on this. Alone it misses by two swapped
address registers (18 instruction differences). Compiled after the matched
routines from 08005C7C in ROM order it is exact, and those routines remain exact
in the same unit. Padding experiments repeat with a period of ten preceding
labels, consistent with the decimal label text in the hash. The recovered unit is
evidence for one original source file covering at least 08005C7C-0800622A; it is
not a source-order claim for the rest of the ROM.
