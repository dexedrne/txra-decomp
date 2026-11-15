# Stage 1 handoff

The ROM still rebuilds byte-identically. This is a substantial first execution
map for native recompilation, **not a complete function recovery or a native PC
build**. No ROM, assets, raw slices, screenshots or recordings were committed or
uploaded. All data reads use the owner's ignored base ROM.

## Delivered

- 37,474 decoded instructions / 85,096 candidate code bytes (about 2.03% of the
  entire ROM), including the instructions behind four C replacements. The
  remaining bytes stay as private incbin slices, including unresolved code.
- 228 function candidates with exclusive reachable extents, modes, spans,
  evidence/confidence, and runtime aliases: 90 high / 138 medium confidence.
- 14 bounded THUMB switch tables with 732 entries, eight contiguous pointer-table
  candidates and 198 individual pointer references. Literal-pool adjacency is
  explicitly distinguished from proven dispatch-table evidence.
- 13 code-copy transfers: startup IRQ, two audio copies, and ten later IWRAM
  copies. Overlapping and mixed code/data tails are recorded. No executable
  EWRAM copy is established.
- Every decoded BX / MOV-PC transfer, the fixed IRQ callback set and 13 known
  register-veneer call sites. All 13 call sites now have statically identified
  targets; the loop-invariant final site has a reviewed ROM-slot annotation.
  Uncalled generic veneers still have open target sets. This does not prove
  dynamic completeness or rule out unknown callers.
- Hardware documentation plus 504 locally resolved access sites at 46 distinct
  I/O/aperture addresses. Dynamic/indexed accesses remain explicitly unresolved.
- Four real C matches, 54 bytes including pools/alignment: a memory clear, a
  serial-status bitfield getter, an empty callback, and a store/accumulate leaf.
  The build compiles and verifies these before assembling the full ROM.
- Local setup tooling, compiler comparison evidence, matching workflow, project
  overview, native recompiler plan, six integration checks, and complete ROM
  partition metadata.

## Commits

- `44602e1` — verified assembly split and ROM-backed data slices.
- `27ce3a1` — four byte-matching C replacements.
- `b32551f` — runtime/switch/hardware inventories, reproducible tools and docs.
- This final documentation/marker commit completes the handoff; see the local
  log for its hash. No push, deployment or merge was performed.

## Validation

`make clean && make check` passed: four individual C comparisons, a full 4 MiB
byte comparison and expected SHA-1, plus **6/6 integration tests**. Those tests
cover the header/entry/checksum, complete nonoverlapping partition, function
extents, all 14 switch tables against ROM words and decoded targets, C outputs,
and complete final ROM identity. An incremental `make` also printed
`build/txra.gba: OK`. The local setup script was rerun successfully. A staged-file
policy audit checked 23 source/metadata files for binary content, forbidden
artifact paths/extensions and absolute user-directory paths; it passed.

No emulator boot, native runtime, controller play, save round-trip or timing/
audio comparison was performed. There are no key pictures or webm clips: this
stage changes build/reverse-engineering tooling and has no visual gameplay
change to demonstrate. No test browser was run.

## Owner-note responses

The single live note, dated 10/27 01:20, changed the direction to recompilation
first. Each part was handled as follows:

1. **Prioritize a complete machine-readable function/indirect/copied-code map:**
   delivered the candidate inventory, proven switch targets, callback references,
   per-callsite targets and 13 copies with load/run addresses. **Completeness is
   not achieved.** Prologue-only functions, inferred ends, unreferenced leaves,
   unknown dynamic callers and code outside the explicit 128 KiB discovery bound
   need runtime tracing and further analysis. Confidence and incomplete flags
   expose these limits instead of presenting guesses as facts.
2. **Scope every hardware register in HARDWARE.md:** delivered the resolved site
   inventory and display, memory, DMA, IRQ, timers, PSG/FIFO, input/link, EEPROM
   and BIOS scope. **An exhaustive dynamic register trace is not done:** indexed
   pointers, DMA destinations and conditional execution require runtime coverage.
   No direct affine-matrix write was proven; mode-4 bitmap rendering is the
   current finding, not a claim that affine access is impossible.
3. **Keep matching builds; C becomes optional:** matching is preserved throughout;
   four C matches were already complete and remain useful as a replacement test.
4. **End OVERVIEW with the native recompiler plan:** done, including ARMv4T state/
   flags, indirect dispatch, load/run PC distinction, copied/modified RAM code,
   event timing/VBlank, hardware scope and validation milestones.

OWNER-NOTES.md was reread before this handoff. The coordinator-owned live note
is left as an untracked input file. The handoff marker is `STAGE1-DONE`.

## Remaining work / what still looks wrong

No visual assessment was performed. The main technical limitation is the map's
incomplete coverage, not the rebuild. Function extents are reachable instruction
spans rather than original symbol sizes, and shared tails or copy overlap can
make them look surprising. Data after the scan bound is not proven entirely
non-executable. No runtime trace validates the map or timing. The original
compiler is narrowed to a matching older GCC family, not an exact release;
old/new agbcc agree on these leaves. Audio-engine identity and save layout are
unresolved.

The next stage should add an instrumented local GBA execution reference, close
unknown execution paths and RAM-copy coverage, then generate ARM/THUMB C blocks
with a PC/state dispatcher and the scoped hardware layer. Validate boot and
menus before driving, saves and sound. Keep the byte-identical ROM build as the
safety net throughout.
