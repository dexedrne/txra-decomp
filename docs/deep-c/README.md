The following two reports preserve independent work from the same frozen slice. Their totals and unfinished classifications describe their respective baselines. The merged build includes five distinct matches from these reports, including 08018E88, and supports both historical and modern ARM compilation. Current combined totals are recorded in DECOMP.md and progress.json.

## Earlier main report

# Deep hand matching, slice c

The fixed selection is the 120 unmatched entries at baseline `70a58fc`, sorted by
`(bytes, address)`, then `[2::3]`. `targets.json` retains all forty assigned rows.
The selection was not shifted after accepting a new match. No other slice's
unmatched source, boundary or match entry was edited.

The pass adds **one four-byte ARM tail branch**, taking the build from **109 /
10,698 bytes / 12.566%** to **110 / 10,702 bytes / 12.571%**. The same 85,132-byte
mapped-code denominator is used throughout. These counts include emitted pools
where present; they are not a claim of complete source coverage or game execution.

`OUTCOMES.md` gives every assigned entry's result and what was learned.
`../asm-only.md` distinguishes private assembly interfaces from invalid standalone
boundaries and compiler-generated ARM/switch bodies. Twenty-one C candidates
remain unmatched; several retained large bodies are repaired lifts rather than
finished recovery of their original source constructs. None of those hypotheses
is in the matching build. Descriptive local names in hypotheses are provisional.

## Retained evidence

- `seeds/`: full-width C hypotheses, including typed record/voice arrays,
  reconstructed switch cases, stack aggregates and ARM frame locals.
- `audits.json`: independent final uncached comparisons for all twenty-one
  unfinished C candidates. Thumb rows include instruction/byte scores and extent
  checks. ARM rows retain the measured compiler/flag comparisons. A source that
  crosses the next entry remains rejected even if its instruction score improves.
- `verified-spans.json`: the channel initializer's 96-byte loop agrees exactly;
  its setup and tail still do not. This partial span is not counted as a match.
- `compilation-groups.json`: 42 combined-unit judgments, including an already
  matched packet sender as a control. Sound initialization, record initialization
  and packet groups were compiled in both orders with old O2, standard O2 and old
  O1. The two packet-sender equalities are rechecks, not new matches.
- `order-comparison.json`: all 21 target/profile pairs emitted identical complete
  output after reversing unit order. This result applies to these hypotheses; it
  does not establish the original project's translation-unit layout.

The matched packet sender agrees only under its existing old O2 profile in this
experiment. Making the receiver closer with O1 does not establish a blanket O1
setting for its neighbors. The tested historical Thumb executable also rejects
instruction-scheduling flags; rejected options were not treated as successful
comparisons. No randomized variant search or separate matching service was run.

## Source-shape findings

The 72-byte voice layout reproduces the channel initializer's loop, reducing its
retained score from 71/118 to 27/89. Sharing the shifted index, separating source
pointer setup and using named tail globals matter; the final source is still four
bytes short. The packet receiver improves from 40/167 to 17/76 using old O1,
preserving the previously dropped stack store and loading status bytes at their
actual width. Its first 72 bytes and total extent agree; state-pointer reuse and
saved-register allocation remain unresolved.

Several old drafts truncated live pointers or discarded arguments. The byte
blitter at 08008914 takes nine arguments: five values loaded from the incoming
stack are not uninitialized locals. The clamp routine at 0800CEEC divides by six;
its division veneer has two arguments, and the old lift had deleted the second.
0800B908 starts with a by-value four-word table plus a separate sixteen-word copy;
its 88-byte frame is not one undersized scalar buffer. The transfer caller at
0800A68C supplies a fifth stack argument even though the installed callee's C
hypothesis ignores it. These are reasons to repair structural seeds before
searching register permutations.

## Reproduction

Run tools from the repository root with its configured Python environment.
`tools/diffhint.py ADDRESS seeds/func_ADDRESS.c` checks the default old profile.
The receiver's retained score requires `compile_candidate(...,
compiler='old-o1')`, with the mapped next entry and full target extent supplied.
`modern-arm` is accepted by the same judge and full build; its flags and limitations
are in `../COMPILER.md`. The historical ARM comparisons use `agbcc_arm`, not the
Thumb executable.

The review folder is `txra-review/deep-c/`. It retains the compiler
comparison text without raw instruction encodings, build/test logs, combined-unit
source snapshots and the small reproduction helpers under `reproduce/`. The
combined snapshots preserve the exact shared declarations used for that test.
Images and the muted six-second checkpoint replay contain matching metadata only.
No ROM slices, extracted assets, gameplay capture or new runtime milestone are
part of this evidence.

## Incoming deep-d report

# TXRA deep matching, slice c

The frozen assignment uses all 120 initially unmatched entries, sorted by byte extent then address, taking zero-based indices 2, 5, 8, … . Blocked entries remain in the partition. No other slice’s function was changed.

Four exact replacements were accepted. The other entries remain unchanged in the ROM build. Thirteen fresh hand-written C hypotheses are retained in `candidates/`; none is installed or semantically verified. The two largest menu entries received diagnostic control-flow compiler baselines; their full hand reconstruction is unfinished. No extracted ROM data, instruction listings or binaries are committed here.

`candidates.json` records fresh full-pool comparisons of the retained sources. Instruction-edit and byte distances are diagnostic measures, never acceptance. For a draft that fits the next entry boundary, inspect it with `python tools/diffhint.py ADDRESS docs/deep-c/candidates/func_ADDRESS.c --compiler PROFILE --rows 100`. Overlong drafts fail the next-entry guard and need their extent corrected first. The separately managed matching service was not contacted or changed.

Source lessons backed by accepted bytes: indexed typed records recover induction registers and argument spills; pointer formation/evaluation order fixes interpolation scheduling; upward source loops can compile into countdowns with different preheaders; independent destination scopes can resolve register swaps across a complete DMA branch. Sound-group compilation-unit order did not change the accepted initializer or buffer near miss. Ordinary O2 with interworking accepted all four additions.

| Entry | Outcome | Evidence / next step |
| --- | --- | --- |
| 08018DE8 | asm-only | Runtime register-call veneer branches directly through the third argument register. Ordinary C indirect calls add call/return machinery; retain the library veneer. |
| 08018DF4 | asm-only | Runtime register-call veneer uses a callee-saved live-in register outside the C argument ABI. |
| 08018E00 | asm-only | Runtime register-call veneer uses a high-register live-in outside the C argument ABI. |
| 08018E0C | asm-only | Runtime register-call veneer uses a high-register live-in outside the C argument ABI. |
| 08018E7C | asm-only | State-switch veneer enters the following ARM instruction using the current program counter. Requires assembly wrapper. |
| 08018A54 | asm-only | CpuFastSet BIOS entry has only the software interrupt and return. Ordinary C cannot express the software-interrupt opcode; retain the wrapper. |
| 08018E88 | asm-only | ARM half of an interworking veneer tail-branches directly into a runtime helper. Retain the library wrapper; it is not an independent ordinary C body. |
| 080095C4 | boundary-blocked | Shared epilogue restores high registers and a pre-existing stack frame, with no prologue. Recover its enclosing function; never install a matching prefix. |
| 08007B28 | boundary-blocked | Mapped entry contains a prologue and initialization but no epilogue or resolved end. Pool references lie beyond the mapped span; recover enclosing copied code first. |
| 080000C0 | asm-only | Startup changes processor mode and installs two stacks before transferring control. Privileged status-register writes and stack setup require startup assembly. |
| 0800D51C | boundary-blocked | Only the opening initialization block is mapped. It saves registers/stack without restoring them and references later pools. DMA use itself is expressible in C; this is a boundary issue. |
| 08000218 | asm-only | Signed runtime division uses flag-coupled sign normalization and a special zero-divisor return. Retain as an assembly-first library helper pending provenance; this is not a proof that division cannot be expressed in C. The current matching path also lacks historical ARM support. |
| 080063D4 | unmatched | DMA buffer swap is ordinary C. Corrected a byte-sized offset and reconstructed typed buffers and pointer loops. Full-pool score improves from 72 instructions / 188 bytes to 52 / 114, still four bytes short. Both compiler variants, O1/O2/Os, documented flags, named globals, declaration order and loop shapes failed equality; retain as unmatched, not assembly-only. |
| 08005F8C | matched | First typed-record reconstruction matches all 228 bytes under old -O2 -mthumb-interwork. Nine-word preset rows and the existing 72-byte voice type reproduce induction registers and the argument spill. Full make prints OK; whole ROM is byte-identical. No flag changes. |
| 080149FC | unmatched | Packet receive remains ordinary C. A two-word local status array explains the otherwise dead stack-zero store without adding artificial volatile effects. Explicit header address and packet-pointer lifetimes recover much of the stack layout, but checksum-loop hoisting consumes a high register and spills the state. Both compiler variants and all five profiles still differ. Prior draft 40/167 remains closer than the fresh semantic reconstruction. |
| 080000FC | asm-only | IRQ dispatcher saves SPSR, changes processor mode, switches stack context and calls through an interrupt vector. Privileged exception entry requires assembly; mapped extent stops before its return tail. |
| 08007398 | unmatched | Sound initialization is expressible in C, including both DMA copies. Reconstructed indexed voice records, six triples, wave loops and array clears. Old-no-gcse / O1 reproduce the extent; explicit byte cursor gets a 36-instruction / 42-byte miss with a 111-byte suffix. Remaining differences are early zero/stride allocation and halfword-constant hoisting. Other profiles and documented flags did not match. |
| 0800B254 | matched | Full 332-byte match under old. Explicit destination/first-field pointer lifetimes, row-base load before byte-offset arithmetic and angle output address before row advance reproduce allocation and scheduling. Forced make OK and whole-ROM equality. |
| 08000AA0 | asm-only | Raster inner loop takes live values in high registers, uses LR as a table base and carries condition flags across non-flag arithmetic and conditional stores. Custom register contract and nested partial saves indicate hand assembly, not a standalone C ABI body. |
| 0800A00C | matched | All 368 bytes exact under old, including pools and alignment. Reused the 100-byte record / 28-byte row interpolation shape. Declaring row index before slot fixes stack order; testing found against search preserves the high-register comparison. Upward 0..3 source loop causes compiler countdown and fixes final invariant-load scheduling. Full make OK; ROM identical. |
| 0800C850 | unmatched | Record/row crossing and fixed-point rotation reconstructed in ordinary C. Explicit row/record pointer order and interleaved cosine product give correct complete 372-byte extent; old-no-gcse draft differs by 48 instructions / 57 bytes. Remaining allocation swaps affect the integer record offset and rotation temporaries; shared global count address and an apparently dead next-index increment need further source recovery. Both compilers / O1/O2 tried; no asm-only claim. |
| 08008914 | unmatched | Nine-argument transparent byte blit has duplicated forward / mirrored loops over 256-byte rows and halfword read-modify-write. Fresh C reproduces 370-byte extent and first 70 bytes exactly. Shared-store and explicit row-pointer forms change lifetimes and regress. Five profiles compared; remaining main issue is row-base / mask allocation and sharing the output-store tail. |
| 080162F8 | unmatched | Reconstructed four signed fixed-point rotation pairs, translation, depth store and reciprocal-table projection using matched triple/angle routines as evidence. Straight C has exact 472-byte extent but 52-byte frame versus target 60, with 150 instruction / 369 byte differences. Both compilers and all five profiles plus inline rotation helpers tested; temporary-vector lifetimes remain unresolved. |
| 0800BBD4 | unmatched | Recovered camera toggle, reverse record-update loop, six calls per active record, angle save/restore, function-pointer callback and camera modes. Initial 96 bytes match. Natural typed record copy is a 52-instruction / 194-byte miss, four bytes long. Source/destination field-address hoisting and temporary scopes remain unresolved under both compilers / all five profiles. |
| 0800A68C | matched | All 532 bytes exact under old, including two pools. Reused accepted DMA/fade idiom from 08013FAC. Destination initialization after source store fixes pool order; a separate scope for the second destination region fixes 46 register-only differences. Forced build OK; full ROM identical. |
| 0800EDF4 | unmatched | Ranker rejects an unresolved computed switch, but inspection confirms a complete ordinary C body, 17-case color transform and return. Reconstructed all source selections and switch cases; integer byte cursor and separate count limit match full 530-byte extent, pools and case-table destinations. Best draft has exact 168-byte prefix and 43 instruction / 54 byte allocation miss. This is not asm-only or an incomplete epilogue. |
| 0800CEEC | unmatched | Recovered lateral clamp, two angle/reflection branches, signed division by six, feedback fields and inverse rotation. Fresh typed C has the correct 28-byte frame. Five profiles tested; default draft is 672 bytes versus 668. Allocation and repeated array/global pointer lifetimes remain unresolved; no asm-only claim. |
| 08000324 | asm-only | Raster inner loop starts with preloaded r6/r8/r10 values, performs XOR register swaps, writes below SP without allocating a C frame, and uses unrolled flag-dependent halfword stores. It is a custom assembly register contract, not a normal C entry. |
| 0800B908 | unmatched | Reconstructed spawn scan and local lane/model table copies without embedding ROM table contents. Correct 88-byte frame; uncached lane reads and explicit first output pointer yield all 716 bytes of extent. Best default draft has 23 instruction / 32 byte differences: high-register swap for conflict/model table plus trig base-load order and outer-loop scratch allocation. Both compilers, five profiles and focused flags tried. |
| 080095E4 | unmatched | Computed switch is complete ordinary C, not an incomplete body. Reconstructed seven lateral marker positions, two projections, clipping, texture coordinates and depth-list insertion. Default draft 766 bytes versus full 758. Table/pool placement and pointer aliasing differ; four alternate profiles regress. A switch rejection alone is not evidence for hand assembly. |
| 0800CB5C | unmatched | Recovered 100-byte record acceleration, two gear modes, clamps, trigonometric movement, signed bounce decay, heading convergence and drag. Typed source has the correct eight-byte frame but is 32 bytes short; five profile comparisons of reordered initialization do not match. Record/field pointer lifetimes and control-flow structure still need hand work. |
| 080076F4 | compiler-path-blocked | ARM sound mixer has a compiler-style APCS frame and 72-byte voice indexing, unlike the custom raster helpers. Do not label asm-only. The installed match/relocation path emits Thumb only and no historical ARM compiler executable is installed; an ARM acceptance path is required before a C replacement can land. |
| 0800C3C4 | unmatched | Reconstructed steering response/clamps, sound timeout, yaw/visual-heading convergence, tilt easing and camera smoothing. Typed source reproduces the four-byte frame but is 44 bytes short; pointer-base trial and all five profiles fail. Large body remains unfinished C work, not assembly-only. |
| 080005D8 | asm-only | Textured raster front end saves r4-r12/LR, packs texture coordinates into fixed registers, performs XOR vertex swaps and uses paired conditional instructions before calling custom-register helper 08000AA0. Assembly wrapper/calling convention is required. |
| 08013594 | unmatched-baseline | Two complete ten-case menu tables were restored to a diagnostic C control-flow draft. Full target is 1444 bytes, including pools; best of five diagnostic profiles is standard, 1480 bytes with 483 instruction / 1337 byte differences. Requires high-level state-loop and DMA-local reconstruction; only a compiler baseline was completed, not a hand match. |
| 080181C0 | compiler-path-blocked | ARM entry has a compiler-style frame, nested eight-record loops and repeated frame-local loads. This is a different compilation/optimization group, potentially lower optimization; not proven hand assembly. The current Thumb-only compiler/relocation pipeline cannot accept it. Historical ARM compiler and profile support remain missing. |
| 08003786 | boundary-blocked | Entry loads a pre-existing 268-byte frame and has no prologue. Its apparent recursive BL is a long backward loop transfer; the eventual epilogue restores the enclosing frame. Recover the full 08002854 enclosure with this internal label before C matching; do not edit another slice’s enclosing entry here. |
| 08006776 | boundary-blocked | Entry reads pre-existing stack slots and r12, with no prologue or local return. Apparent recursive BL is a long-loop branch from 08007358. Enclosing prologue starts at 080064A4; 08006740 is another internal block. The continuation at 0800735C and epilogue at 08007368 are separately mapped. Requires coordinated boundary recovery, not standalone C. |
| 0800421C | boundary-blocked | Real prologue saves a 36-byte frame, but mapping ends before shared epilogue 080051FE. Early BL to that epilogue is a long transfer, not a conventional returning call. Recover the complete enclosure before comparing; leave the other slice’s epilogue untouched. |
| 08010A50 | unmatched-baseline | Complete large menu/action function with many repeated selection handlers and frequent literal pools. Diagnostic ordinary C control-flow baseline compiles all 2551 source lines. Full target is 6460 bytes including pools. Five profiles compared; best standard-o1 is 6292 bytes, 2740 instruction / 6100 byte differences. High-level repeated-handler and local-lifetime recovery remains unfinished; no exact or playable-game claim. |
