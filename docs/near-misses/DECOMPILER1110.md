# Headless analysis record

The round used **Ghidra directly**, through `support/analyzeHeadless`. REA 6.7.0
was used for the requested doctor check and its packaged documentation/source
inspection only. Its native provider does accept a raw image and a load/entry
address, and offers a language override. However, it creates a separate full
input-file snapshot before import. That conflicts with this task's ROM no-copy
rule, so the direct headless importer read the existing ignored symlink instead.
No client configuration or registration was changed.

JDK 21 was downloaded from the specified official Adoptium endpoint to
`~/opt/jdk21` and verified as Temurin 21.0.13+9. The current
[Ghidra 12.2 release](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.2_build)
was downloaded to `~/opt/ghidra`; its archive SHA-256 agrees with the value
published on that release. This release's own `application.properties` requires
Java 25. A second official Temurin download, 25.0.5+8, supplies that runtime at
`~/opt/jdk25`; its PATH/JAVA_HOME override was scoped to headless launches.
Archive identities and the final database audit are in
[decompiler-1110.json](decompiler-1110.json).

The project and exports reside in `~/.cache/txra-ghidra/`, with owner-only access.
Ghidra 12.2 rejects a dot-prefixed component in its project locator, so
`~/txra-ghidra-project` is only a symlink into that cache. It is not another
project or ROM copy. The importer used BinaryLoader with load address
08000000, processor `ARM:LE:32:v4t` and initially the default compiler spec.
BinaryLoader's separate image-base property remains zero; the audited memory
block and all target entries are at their correct cartridge addresses. No
rebasing or shifted second image was performed.

The 229 function entries and exact instruction spans came from
`docs/map/functions.json`. All 13 explicit `tools/rom.cfg` entry/mode seeds agree
with that registry. Assembly function-label checks identified five registry
starts without a same-named `asm/program.s` function label; the registry was
used for those starts rather than inventing labels or changing the map. Explicit
TMode values were applied per code span before disassembly; pool gaps were
excluded. Data from 08020000 onward is non-executable. RAM blocks are
uninitialized/writable, cartridge blocks read-only, and the hardware block is
volatile. Function-start scanning, aggressive instruction discovery, embedded
media discovery and parameter-ID inference were disabled for the bounded import.
Normal analysis still discovered a few extra entries: the final private
database contains 232 functions after the common-return repair, not a claim
that the public registry has changed.

The HUD's shared epilogue at 080051FE was first exported independently, then
joined to its owner. The internal long exit transfer was treated as a branch
and the final indirect transfer as a return. This repairs the decompiler's
control-flow interpretation without patching an instruction. Helper signatures
were supplied from our existing declarations, and the signed division stub was
given its two-argument signature. Those are explicit analysis assumptions.
The HUD final body contains 1,810 instructions and 50 call sites; the ARM
renderer contains 1,053 instructions and no outgoing calls. Owner bodies exclude
literal pools; compiler comparisons still cover each complete owner and pools.

APCS was selected for the final working view. For the renderer, default/APCS
views, disabled array splitting and disabled alias blocking all left a
high-level corner-depth stack join unresolved. The initial p-code retains
the stores that the printed high-level view omits. This limitation is described
in [the renderer comparison](arm-16da8-1110/SHAPE.md), and no missing assignments
were copied into our candidate. The final cartridge/RAM permissions remove
spurious mutable-pool interpretations from the earlier import view.

All authored Java scripts are in the compressed
[headless recipes](decompiler-recipes-1110.json.gz); this archive contains
scripts, including diagnostics, **not any exported C or project data**. To
recreate the seed input, write a TSV row per registry entry: hexadecimal start,
mode, and comma-separated inclusive ranges formed from each exclusive-end
`spans` pair. `globals.tsv` is the set of `g_XXXXXXXX` identifiers in the starting
HUD candidate, paired with those addresses. These are repository metadata,
not extracted bytes.

A headless launch uses the cache alias as project location, the ignored
`baserom.gba` as input, `-loader BinaryLoader -loader-baseAddr 0x08000000`,
`-processor ARM:LE:32:v4t`, the recipe script directory, and `-max-cpu 2`.
`SeedTxra` seeds/disassembles the registry spans. `NormalizeHud` repairs the
shared return and signatures, `InspectArm` selects APCS and records diagnostic
views, `RomPermissions` states the memory permissions, and `ExportTxra` writes
the working views to the private cache. `AuditShape` exports only metadata.
`GHIDRA_HEADLESS_JAVA_OPTIONS` points both `java.io.tmpdir` and
`application.cachedir` into the same home cache for final launches. The initial
default temporary cache was audited and cleaned separately; the final private
project remains intact.

No decompiler export, ROM encoding, extracted binary, project database or input
snapshot is committed. Only our own rewritten C, sanitized comparisons, hashes,
metadata and compressed authored recipes are retained. The view is a working
aid; the unchanged semantic and complete-byte gates retain authority.
