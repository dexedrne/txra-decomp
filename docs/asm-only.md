The following two reports preserve independent work from the same frozen slice. Their totals and unfinished classifications describe their respective baselines. The merged build includes five distinct matches from these reports, including 08018E88, and supports both historical and modern ARM compilation. Current combined totals are recorded in DECOMP.md and progress.json.

## Earlier main report

# Slice c: assembly interfaces and broken boundaries

These entries were selected from the fixed 109-match baseline. This is a scope
classification, not a proposal to install assembly as C or to delete mapped code.
The evidence is from the entry, its callers and the reachable return paths.

| Entry | Classification | Evidence / action |
| --- | --- | --- |
| 08018DE8 | Register-call veneer | Branches through r2 while preserving its caller's return address. Both historical and current Thumb compiler probes emit a call with a return frame instead. Keep the ABI thunk. |
| 08018DF4 | Register-call veneer | Input is the nonargument register r5. Ordinary external C parameters cannot express this interface. |
| 08018E00 | Register-call veneer | Input is the nonargument register r8. |
| 08018E0C | Register-call veneer | Input is the nonargument register r11. |
| 08018E7C | Mixed-state division veneer | Changes instruction state with BX PC; its ARM continuation branches into division. A two-byte mapped prefix is not a standalone ordinary C routine. |
| 08018A54 | BIOS veneer | CpuFastSet software interrupt followed by return. The available C compilers need an assembly interface for this BIOS instruction. |
| 080000C0 | Startup assembly | Changes processor mode, installs banked stack pointers and IRQ entry, then enters Thumb code. |
| 080000FC | IRQ assembly / incomplete span | Reads SPSR, changes processor mode and dispatches through the interrupt table; its mapped span stops before the complete return sequence. |
| 08000218 | Division runtime assembly | Flag-dependent sign normalization and conditional shift/subtract division implement an ABI helper. Keep the runtime interface; do not recursively compile a C division operator into itself. |
| 08000324 | Private renderer entry / fragment | Reads r6-r11 and inherited stack state without ordinary argument definitions; includes conditional unrolled stores and XOR exchanges. Recover the enclosing rendering unit. |
| 08000AA0 | Private renderer helper | Consumes high registers, incoming condition flags and caller stack values. The caller preserves r7/r8 around its BL. A generic C declaration loses live inputs. |
| 080005D8 | Renderer with private helper ABI | Saves r4-r12 and invokes 08000AA0 with the private register interface. Recovery needs a reviewed assembly boundary or the combined rendering unit, rather than an invented ordinary C prototype. |

The renderer classification concerns the observed private calling convention. It
does not prove that every arithmetic operation in those routines was handwritten.

| Entry | Boundary problem | Required next step |
| --- | --- | --- |
| 080095C4 | Shared epilogue restores an existing frame | Find the enclosing entry; do not count a matching epilogue as a function. |
| 08007B28 | Stops after 24 bytes of initialization, with a live frame | Recover the rest of the enclosing body and its pools. |
| 0800D51C | Stops after 84 bytes of initialization, with a live frame | Resolved: the installed 3,964-byte C owner (commit 1a16ef6) covers 0800D51C-0800E498, including 0800D570, 0800D630 and 0800D960. |
| 08003786 | Uses inherited stack offset D0 and calls without saving LR | Recover the enclosing function; current validation rejects the entry. |
| 08006776 | Repaired 11/14: previously started mid-mixer and called without saving LR | Its only reference, the BL at 08007358, is a reviewed `far_jumps` entry in `tools/rom.cfg`. The 080064A4 owner now runs 080064A4..08007378 (pool through 08007398); 08006712, 08006740, 08006776, 0800735C and 08007368 are interior labels, not registry entries. Frame slots: `docs/FINISH-1114-mixer.md`. |
| 0800421C | Repaired 11/14: previously fell through the next mapped entry | The long BL at 08004232 is a reviewed `far_jumps` entry in `tools/rom.cfg`; the registry owner now runs 0800421C..0800520E including its epilogue, and 080051FE is no longer a separate entry. |

080076F4 and 080181C0 have conventional ARM compiler frames. They remain C
candidates, not assembly-only classifications. Both received historical ARM and
current compiler comparisons; neither matched.

080095E4, 0800EDF4 and 08013594 contain bounded compiler switch tables. Their
validator's unresolved-transfer warning is not proof of assembly-only code. The
retained hypotheses restore the cases and shared tails.

08018E88 is the exception to the initial veneer classification: its entire
four-byte ARM branch can be compiled from ordinary C with the recorded
`modern-arm` profile. It is installed and independently tested. The adjacent
Thumb state-changing entry and the underlying initialization body are not claimed
as new C matches.
# Assembly and internal-entry review

Slice b freezes the starting unmatched inventory, sorts by mapped byte size then
address, and takes offset 1 with stride 3. These entries are not ordinary C
replacement candidates. This is a source-recovery classification, not permission
to count wrappers or preserved ROM bytes as matched C.

| Entry | Classification | Evidence and next action |
| --- | --- | --- |
| 08018DE4 | register-call assembly veneer | Branches directly to live r1; no C argument or saved return handling. |
| 08018DF0 | register-call assembly veneer | Branches directly to live r4, a callee-saved register. |
| 08018DFC | register-call assembly veneer | Branches directly to live r7, a callee-saved register. |
| 08018E08 | register-call assembly veneer | Branches directly to live r10, outside C argument registers. |
| 08018E14 | register-call assembly veneer | Branches directly to sp; preserve machine-level entry semantics. |
| 08000000 | ARM entry branch | Single non-linking branch at image entry; preserve assembly startup. |
| 08018E80 | ARM interworking branch | Single non-linking branch to signed division implementation. |
| 0800027C | ARM unsigned division helper | Conditional shift/subtract loop uses carry and shared flags; runtime assembly is the likely origin. |
| 08006712 | internal label of 080064A4 (merged 11/14) | Voice-loop head reached by the reviewed far jump at 08007364; its own BLs are far jumps to 0800735C. No longer a registry entry. |
| 0800735C | internal label of 080064A4 (merged 11/14) | Voice-loop increment (r10 = sp+88, loop while at most 7); reached by far jumps at 0800672C/0800673C. |
| 08007368 | epilogue of 080064A4 (merged 11/14) | Releases the owner's 108-byte frame; reached by far jumps at 080066EC/08006700 and the bgt at 08007362. |

The memory-copy routine at 08018E1C is ordinary C. Its pop-to-pc return indicates
compilation without Thumb interworking; do not classify all runtime helpers as
assembly solely because the ranker labels them helpers.

## Remaining slice b entries with calling-convention or boundary evidence

| Entry | Classification | Evidence and next action |
| --- | --- | --- |
| 080010B8 | assembly rasterizer | Consumes packed inputs in r4/r6/r11, manually stacks input registers, and uses carry across stack updates; the C argument ABI does not describe this entry. |
| 08001218 | assembly rasterizer | Saves r4-r12/lr as one fixed set, performs XOR swaps and flag-dependent packed arithmetic, and calls another raster entry with live registers beyond r0-r3. Preserve its register contract. |
| 08015128 | non-ABI source pointer, provenance unresolved | Saves r8 then reads it as a palette pointer without defining it. An original uninitialized C local is also possible; do not invent an argument or claim proven handwritten assembly. |
| 08014FF4 | non-ABI source pointer, provenance unresolved | Saves r9 then reads it as a palette pointer in two branches without defining it. Same unresolved issue as 08015128. |
| 08007B40 | internal C entry | Starts with BL and writes the enclosing frame before any LR save; its exit consumes an existing frame. Recover the enclosing entry before compiling this body alone. |
| 08008A88 | truncated C unit | Normal prologue and three reviewed switch tables, but the mapped end omits the shared epilogue beginning at 080095C4. The epilogue consumes this function's saved registers. Coordinate enclosing extent ownership. |
| 08002854 | truncated C unit | A normal prologue allocates 268 bytes. Independent reachability continues beyond the mapped end 08003786 to a balanced return through 0800417E. A prefix replacement would be invalid. |

The unsigned division helper's assembly provenance remains a strong runtime
hypothesis, not a recovered vendor attribution. No asm wrapper is counted as C.
The other assembly entries above have explicit machine-register contracts.

## Entries that must not be dismissed as assembly

08002500 and 08012600 were rejected by the ranker as unresolved control
transfers. Both are now full ordinary-C matches: their reviewed switch metadata
was sufficient to recover the original switch constructs. Their compiled sizes
are 632 and 1,104 bytes, including tables and final pools.

080147D0, 08014AE0, 08014CE4 and the larger display-setup routines use hardware
or BIOS facilities, but these do not require handwritten bodies. Addressed stack
fill values, correctly volatile DMA registers and existing BIOS veneers express
them in C. Missing `sp` variables in lifted drafts are not assembly evidence.

08016C18 and 080165BC use conventional ARM compiler frames. The separate
historical ARM compiler was tested at O2, O1 and Os on recovered C drafts; none
matched. Their draft emitter omits multiply-accumulate operations as generic
comments, so the raw drafts are incomplete. Capstone identifies these operations
as MLA. Literal references, frame-local slots and MLA arithmetic were restored in
local trials; no ARM replacement or broad ARM build profile was installed.
# Assembly and incomplete entries: deep slice a

These are exclusion decisions, not accepted C replacements. The slice is fixed from the initial unmatched list sorted by byte extent then address, every third entry from offset zero. No mapping boundaries or other slices are changed.

| Function | Size | Outcome | What was learned |
|---|---:|---|---|
| 08018DE0 | 2 | assembly veneer | BX r0 preserves the caller LR and all arguments; ordinary C indirect call adds a prologue and return. |
| 08018DEC | 2 | assembly veneer | BX r3 register-call ABI; flags and unit order cannot express this transfer as a standard C function. |
| 08018DF8 | 2 | assembly veneer | BX r6 uses a non-argument register and preserves the caller return address. |
| 08018E04 | 2 | assembly veneer | BX r9 uses a non-argument high register and preserves the caller return address. |
| 08018E10 | 2 | assembly veneer | BX ip uses the scratch-register call ABI; retain assembly. |
| 08018E84 | 2 | interworking veneer | BX pc switches to the adjacent ARM code; there is no independent C body. |
| 08018A58 | 4 | BIOS veneer | SWI CpuSet followed by BX lr requires an assembly intrinsic/wrapper; no C replacement claimed. |
| 0800D960 | 8 | shared tail entry | Writes a state flag then branches backwards into 0800D630 without saving LR; standalone C adds a call/return frame. |
| 080051FE | 16 | shared epilogue (merged 11/14) | Releases the HUD's 36-byte frame, restores r8-r10 and r4-r7 and returns; now part of the 0800421C owner, not a registry entry. |
| 080001F4 | 36 | IRQ epilogue | Restores banked exception state using MRS/MSR and SPSR; needs assembly with its entry, not standalone C. |
| 08006740 | 54 | internal label (merged 11/14) | Voice preparation block of 080064A4, reached by the bne at 0800673A and the reviewed far jump at 08006F46; no longer a registry entry. |
| 080002CC | 88 | custom ARM ABI | Passes six operands in r6-r11 and another in r3 to 08000324; two calls preserve a hand-managed lr pointer. Ordinary ABI compilation is not appropriate. |

The shared tail and internal fragments may come from compiled C, but their mapped extents cannot be treated as standalone ABI functions. DMA register access alone is not an assembly-only reason: 08015DA8 remains an ordinary-C candidate.

0800D570 is another internal initialization fragment: its first instruction calls without saving LR, it uses an already-allocated stack frame, and the mapped end falls through. This is a boundary issue rather than evidence of hand-written assembly.

080016E0 is a custom ARM raster inner loop. It consumes live values in r4/r6/r7/r8/r11/r12, saves only selected registers and keeps carry from a shift for a later conditional branch. Its packed two-pixel stores and manually managed row frame require preserving the assembly interface. No ordinary ABI C replacement is claimed.

080064A4 has a proper compiled-C prologue and a 108-byte local frame, but its mapped extent ends at 08006712 while preparing live registers for more mixer code. It falls through rather than returning. This is an enclosing-body recovery problem; compiler flags cannot fix it inside the current boundary. The following mapped entry belongs to another slice and is untouched. Status 14 November: the boundary is repaired (seven reviewed far jumps; owner 080064A4..08007378, pool through 08007398).

08000BF0 has a manually arranged 64-byte raster frame and high-register state passed to 080010B8. Vertex sorting uses explicit XOR swaps; a single condition result survives across non-flag-setting arithmetic into later predicated operations. Preserve this assembly interface. A larger C function could call a wrapper, but this body is not claimed as ordinary ABI C.

0800D630 consumes live r6 with no prologue or LR save, accesses the existing local frame, and finally restores the frame created at 0800D51C. Its 0800D570 and 0800D960 entries are internal control-flow entries. Recover the whole enclosing C body in a separate boundary-coordination task; this slice does not change its siblings.

Status 14 November: that enclosing body was recovered and installed on 2 November (commit 1a16ef6). `func_0800D51C` is 3,964 bytes of verified C through 0800E498 (pools included), so 0800D570, 0800D630 and 0800D960 have no remaining bytes to match. `tools/rank_targets.py` now reports such entries as `covered by installed <owner>`. See `docs/FINISH-1114-d630.md`.

Conversely, 0800AF4C, 080157A0 and 0800E498 use normal bounded switch tables. Their indirect transfers are not assembly-only evidence; 080157A0 is now an exact C replacement. 08017E68 and 08018854 are also exact compiled ARM C. The larger 08016DA8 has the same conventional ARM frame family and remains unfinished C recovery rather than an assembly exclusion.

## Independent deep-b review

The following notes describe that branch’s historical baseline; the two switch
dispatchers are already accepted in the merged build, as recorded above.

# Entries that require assembly or boundary recovery

These findings concern slice b of the deep hand matching pass. They are not new
C replacements. A ranking rejection alone does not establish handwritten assembly.

| Entry | Decision | Evidence / next action |
| --- | --- | --- |
| 08018DE4 | Assembly call veneer | Branches through r1 without setting a return address. |
| 08018DF0 | Assembly call veneer | Branches through r4, outside the ordinary argument-register contract. |
| 08018DFC | Assembly call veneer | Branches through r7, outside the ordinary argument-register contract. |
| 08018E08 | Assembly call veneer | Branches through r10; requires an explicit register contract. |
| 08018E14 | Assembly trampoline | Branches through sp; not an ordinary callable C entry. |
| 08000000 | Assembly reset entry | A single ARM branch before any C runtime setup. |
| 08018E80 | Assembly interworking veneer | ARM branch into the signed divider following a Thumb entry. |
| 0800027C | Likely assembly library divider | Conditional ARM subtract/add steps carry flags through the division loop; zero denominator returns without a C division operation. Exact library attribution remains unproven. |
| 0800735C | Merged into 080064A4 (11/14) | Uses stack slot 88 and saved high-register state. Not independently callable. |
| 08007368 | Merged into 080064A4 (11/14) | Shared epilogue removes a 108-byte frame and restores saved high registers. |
| 08006712 | Merged into 080064A4 (11/14) | Uses live r10/r12 and stack slots 88/92. Apparent BL calls are long control-flow edges within the body (now reviewed far jumps). |

DMA and BIOS use alone does **not** make a function assembly-only. Ordinary C
hardware-register access and calls through existing BIOS veneers remain eligible.
The runtime copy routine at 08018E1C is C: the explicit non-interworking compiler
profile reproduces its return and its complete 94-byte body.

08015128 saves r8 and then reads it as a color-source pointer without defining it.
This is not proof of handwritten assembly: an uninitialized original C pointer
could also cause it. There are no mapped direct callers to establish a private
register contract. Keep it outside ordinary C matching until that contract or
original undefined-source behavior is understood.

08014FF4 has the same unresolved palette-source pattern, using saved r9 without
an initial definition. Treat it like 08015128; neither is proven assembly-only.

## Additional renderer and boundary findings

- 080010B8 has live r7/r8/r11 inputs and a custom save/frame contract. It needs
  its assembly renderer wrapper and private register ABI retained.
- 08001218 likely belongs to the same handwritten renderer family: lr is a
  general register, r4-r12/lr are saved without an APCS frame, and the edge
  helper is called with live private register state. Exact provenance is unknown.
- 08007B40 begins with a call without saving lr, and the preceding entry falls
  through into it. Recover the enclosing unit before compiling this fragment.
- 08002854 validates to balanced code through 0800417E, beyond its mapped end
  08003786. The mapped prefix must not be installed as a complete function.

08016C18 and 080165BC are **ordinary ARM C candidates**, not assembly-only.
Both use compiler-style APCS frames. The locally built pinned ARM compiler
reproduces that family of frame, although neither complete body matches yet.
08002500, 08012600 and 08008A88 contain bounded switches; their ranking rejection
is conservative. Restoring the computed case labels makes their C drafts compile.

## Incoming deep-d report

# Retained assembly and boundary classifications

Slice c inspected these entries directly, rather than treating every small function as an easy C leaf. No inline assembly, embedded instructions, output patches or assembler wrappers were added to the C match count. The library division entry is an assembly-first classification pending provenance. The one-instruction ARM branch is part of a paired state-switch veneer; classifying that wrapper does not prove a C tail call could never produce a branch instruction.

## Runtime wrappers and custom assembly contracts

| Entry | Reason |
| --- | --- |
| 08018DE8 | Runtime register-call veneer branches directly through the third argument register. Ordinary C indirect calls add call/return machinery; retain the library veneer. |
| 08018DF4 | Runtime register-call veneer uses a callee-saved live-in register outside the C argument ABI. |
| 08018E00 | Runtime register-call veneer uses a high-register live-in outside the C argument ABI. |
| 08018E0C | Runtime register-call veneer uses a high-register live-in outside the C argument ABI. |
| 08018E7C | State-switch veneer enters the following ARM instruction using the current program counter. Requires assembly wrapper. |
| 08018A54 | CpuFastSet BIOS entry has only the software interrupt and return. Ordinary C cannot express the software-interrupt opcode; retain the wrapper. |
| 08018E88 | ARM half of an interworking veneer tail-branches directly into a runtime helper. Retain the library wrapper; it is not an independent ordinary C body. |
| 080000C0 | Startup changes processor mode and installs two stacks before transferring control. Privileged status-register writes and stack setup require startup assembly. |
| 08000218 | Signed runtime division uses flag-coupled sign normalization and a special zero-divisor return. Retain as an assembly-first library helper pending provenance; this is not a proof that division cannot be expressed in C. The current matching path also lacks historical ARM support. |
| 080000FC | IRQ dispatcher saves SPSR, changes processor mode, switches stack context and calls through an interrupt vector. Privileged exception entry requires assembly; mapped extent stops before its return tail. |
| 08000AA0 | Raster inner loop takes live values in high registers, uses LR as a table base and carries condition flags across non-flag arithmetic and conditional stores. Custom register contract and nested partial saves indicate hand assembly, not a standalone C ABI body. |
| 08000324 | Raster inner loop starts with preloaded r6/r8/r10 values, performs XOR register swaps, writes below SP without allocating a C frame, and uses unrolled flag-dependent halfword stores. It is a custom assembly register contract, not a normal C entry. |
| 080005D8 | Textured raster front end saves r4-r12/LR, packs texture coordinates into fixed registers, performs XOR vertex swaps and uses paired conditional instructions before calling custom-register helper 08000AA0. Assembly wrapper/calling convention is required. |

## Mapping fragments, not assembly-only decisions

These require enclosing-body recovery. No function belonging to another slice was changed.

| Entry | Reason |
| --- | --- |
| 080095C4 | Shared epilogue restores high registers and a pre-existing stack frame, with no prologue. Recover its enclosing function; never install a matching prefix. |
| 08007B28 | Mapped entry contains a prologue and initialization but no epilogue or resolved end. Pool references lie beyond the mapped span; recover enclosing copied code first. |
| 0800D51C | Only the opening initialization block is mapped. It saves registers/stack without restoring them and references later pools. DMA use itself is expressible in C; this is a boundary issue. Resolved by the installed 3,964-byte owner (1a16ef6). |
| 08003786 | Entry loads a pre-existing 268-byte frame and has no prologue. Its apparent recursive BL is a long backward loop transfer; the eventual epilogue restores the enclosing frame. Recover the full 08002854 enclosure with this internal label before C matching; do not edit another slice’s enclosing entry here. |
| 08006776 | Entry reads pre-existing stack slots and r12, with no prologue or local return. Apparent recursive BL is a long-loop branch from 08007358. Enclosing prologue starts at 080064A4; 08006740 is another internal block. Since 11/14 all seven long BLs in the owner are reviewed far jumps; 08006712, 08006740, 08006776, 0800735C and 08007368 are interior labels and the owner extent is 080064A4..08007378. The complete C owner is still an uninstalled nonmatch. |
| 0800421C | Real prologue saves a 36-byte frame; its epilogue 080051FE is reached by the final loop's fall-through, three local branches and one early long BL whose link value is never used. Since 11/14 that BL is a reviewed far jump and the owner's registry extent ends at 0800520E (pool through 08005238). The C body is still an uninstalled nonmatch. |

## Compiler-shaped ARM bodies

These are explicitly **not** classified as hand assembly. The installed build verifier compiles and extracts Thumb functions; a historical ARM compiler and ARM relocation/acceptance path remain necessary.

| Entry | Reason |
| --- | --- |
| 080076F4 | ARM sound mixer has a compiler-style APCS frame and 72-byte voice indexing, unlike the custom raster helpers. Do not label asm-only. The installed match/relocation path emits Thumb only and no historical ARM compiler executable is installed; an ARM acceptance path is required before a C replacement can land. |
| 080181C0 | ARM entry has a compiler-style frame, nested eight-record loops and repeated frame-local loads. This is a different compilation/optimization group, potentially lower optimization; not proven hand assembly. The current Thumb-only compiler/relocation pipeline cannot accept it. Historical ARM compiler and profile support remain missing. |

## Computed switches remain C candidates

0800EDF4 and 080095E4 have complete bodies and ordinary switch/return structure despite the ranker's unresolved-control-transfer rejection. 08013594 also has complete menu switch tables. Their compiler misses remain C work. DMA use alone is not an assembly-only reason: 0800A68C is a complete 532-byte C match.

## Slice f review

Slice f (52 entries, `docs/deep-f/targets.json`) confirms the earlier veneer,
BIOS, division, IRQ and ARM raster classifications without change. Two entries move
out of the unresolved group:

| Entry | Classification | Evidence |
| --- | --- | --- |
| 08015128 | ordinary C, uninitialised local | A `u16 *` local that is read and incremented but never assigned is placed in r8. The compiler saves r8 and reads it without a definition, exactly as in the ROM. The rest of the fade routine is plain C; now matched exactly in `src/generated/func_08015128.c`. |
| 08014FF4 | ordinary C, uninitialised local | Same palette-fade family; its unassigned source pointer lands in r9. Now matched exactly in `src/generated/func_08014FF4.c`. |

Neither is evidence of handwritten assembly. Both read garbage in the original
program; a faithful C source must keep that bug.
## Deep slice e

Even indices of the 105-entry size-sorted list. No new assembly-only claims:
the eighteen assembly, BIOS and runtime entries and six boundary fragments in this half confirm
the slice a–c evidence above (register-call veneers 08018DE0/DE8/DF0/DF8/E00/
E08/E10, the state-switch veneer 08018E7C, reset branch 08000000, CpuSet
veneer 08018A58, IRQ return 080001F4, startup 080000C0, unsigned division
0800027C, the private-ABI rasterizer entries 080002CC, 08000324, 08000AA0,
080005D8 and 08001218, and the boundary fragments 0800D960, 080095C4,
08007368, 08007B40, 08006776 and 08002854). 08017F64 has a conventional APCS
frame and is the ARM sibling of 0800B3A0; it stays a C candidate. See
`deep-e/README.md`.

## Deep slice g

Slice g (51 entries, every second size-sorted unmatched entry from index 0 on
the 128-match main) holds the same eighteen assembly, BIOS and runtime entries
and the same six boundary fragments as slice e; nothing new is classified as
assembly-only. Five ordinary C bodies were matched instead (08018BE8, 080147D0,
08012CC8, 08012EB8, 0800F008). 08018BE8 confirms that the EEPROM library group
is ordinary C compiled with `standard-o1`. The DMA-heavy title and scene loops
(08012CC8, 08012EB8, 0800F008) are plain C written with the SDK `DmaSet` /
`DmaClear` macro shapes, so DMA register use is again not an assembly reason.
See `deep-g/OUTCOMES.md`.

## 14 November: re-measured and recorded

All 31 assembly interfaces above are now listed in `docs/map/finish.json`, together with the 5 C owners, the 08003786 continuation and the 2 labels (0800D570, 0800D630) still listed inside an installed owner. After the 11/14 integration the other six former fragments and three covered labels are no longer registry entries (see `FINISH.md`, *Folded 11/14*). `tools/asm_interfaces.py` re-measures each entry's defining property from the ROM, and exits non-zero if an entry loses it:

- **Register-call veneers.** The 14 entries 08018DE0–08018E14 are each a single `bx rN` with no frame and LR untouched (libgcc `_call_via_rN`). r0, r1 and r2 have 6, 2 and 5 callers. r3 through sp have no reference of any kind.
- **BIOS veneers.** 08018A54 is SWI 0x0C and 08018A58 is SWI 0x0B, each followed by a return.
- **State-switch veneers.** 08018E7C and 08018E84 are each a single `bx pc`. Their ARM halves (08018E80, 08018E88) are installed as byte-identical C tail calls.
- **Startup and IRQ.** 080000C0 has 2 MSR mode changes. 080000FC and 080001F4 have 3 MRS/MSR each.
- **Division.** 08000218 and 0800027C have no frame and 11 and 7 flag- or carry-predicated non-branch instructions. 0800027C has no reference and never ran.
- **Renderer private ABI.**
  - The helpers 08000324, 08000AA0, 080010B8 and 080016E0 read fp, ip, r4 and r6–r11 before defining them.
  - The three front ends 080005D8, 08000BF0 and 08001218 have the same shape: 17 XOR swaps, 9 LR writes, 33 predicated instructions, and r4–r12 and lr saved without an APCS frame. Each calls its helper under that private contract.
  - 080002CC writes LR as a general register and calls 08000324 under the same kind of contract.

`progress.json → completion` counts these 31 as *documented assembly interfaces* (6,092 instruction bytes). They are never counted as C.

## Repaired 11/14: 080095C4 and 0800D960

Both entries were labels inside installed exact owners, reached by Thumb long
branches (BL used as a goto beyond the 2 KiB branch range; the link value is
never read). The installed C emits each of these BLs as a compiler far jump.
`tools/rom.cfg` lists them under `far_jumps` (08008B08 and 08008C76 to the
shared epilogue 080095C4 of `func_08008A88`; 0800E3DC to the 0800D960 tail of
`func_0800D51C`), so neither is a registry entry any more. The 08008A88 extent
now runs through 080095D2; 0800D960 joins the extent that contains its source
(currently the 0800D630 entry). The rows above for these two entries are
historical. See `FINISH-1114-small.md`.

## Resolved 11/14: 08007B28 and 08007B40

Both rows above are stale. The race main 08007B28 has been an installed exact C
replacement since 11/3 (2,292 bytes, 08007B28-0800841C, see `match-1102.md`).
08007B40 is its restart label: the only reference is the BL at 080083BA inside
that body, a `goto` beyond Thumb branch range. `tools/rom.cfg` now lists it
under `interior_labels`, so `tools/analyze.py` keeps it as code but no longer
as a separate registry entry (see `FINISH-1114-b40.md`).
