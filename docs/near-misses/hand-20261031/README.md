# Hand review of the current closest attempts

All four attempts with a score at most 15 were read and tried in this order:
08018E84, 0800D960, 080095C4, 08007368. **Zero replacements were added**;
the build remains at 156 functions / 37,824 bytes / 44.430% of mapped code.
The low scores conceal wrong behavior or incomplete function boundaries.

The score in the supplied files is a **byte distance**, not an instruction
count: unequal overlapping bytes plus the length difference. These four are
not register-allocation near matches. Matching an instruction count or suffix
would not recover a complete function.

| Entry | Original score | Classification | Trials | Result |
| --- | ---: | --- | ---: | --- |
| 08018E84 | 1 | Thumb-to-ARM state switch | 18 | Empty C returns through LR; target branches through PC. |
| 0800D960 | 2 | Internal backedge into an inherited frame | 24 | Store is exact; the draft omits the branch. A real C call adds its own frame. |
| 080095C4 | 10 | Shared epilogue / incoming saved-register state | 18 | Draft calls a null pointer and returns zero; target returns live r7 and restores seven saved words. |
| 08007368 | 15 | Shared epilogue / inherited 108-byte frame | 18 | Draft reads unrelated link state; target only restores its enclosing frame. |

Each row's `.txt` contains the actual source probes, default-profile compiler
diffs, loop/global-optimization dumps and final allocation summaries. Machine
instruction encodings are omitted. `outcomes.json` records every trial and the
score frontier, including source fingerprints, with no extracted binary data.
These are **rejected diagnostics**, not sources to install or semantic rewrites.

## 08018E84: state switching, not a return-register tie

The target is `bx pc`. From Thumb address 08018E84 its architectural PC is
08018E88, so execution enters the already matched ARM branch there. LR must
remain available to the helper called by that branch. The retained empty C
instead emits `bx lr` and skips the helper entirely. Explicit and implicit C
returns produce the same two bytes under all six Thumb profiles.

The loop and global-optimization dumps are empty of executable work; allocation
has zero basic blocks and no used hard registers. There is no temporary to
split or share. A diagnostic call to `arm_func_08018E88` emits a Thumb BL plus
push/pop, and the relocation checker correctly rejects its ARM destination.
That does not justify relaxing relocation checks or rewriting the opcode.
Retain the Thumb assembly wrapper. The ARM half is already included in the
156 installed replacements; counting it again would inflate progress.

## 0800D960: omitted control flow and a misidentified entry

The three store instructions and the pool at 0800D968 are already identical.
Changing integer-address arithmetic to a separate typed pointer/value leaves
the two-byte miss unchanged. The missing instruction is an unconditional
backward branch to 0800D630, not a C return.

Adding that call explicitly gives a 20-byte function under every Thumb profile.
Swapping the pointer/value initialization order and writing the call as a
void return still gives 20 bytes with different allocation. The compiler's
loop/global dumps retain a `call_insn`; global allocation uses r0/r1 and
preserves a distinct return. The target does not create a new return address.
Turning interworking off changes the return machinery, but does not turn this
into the original branch.

The original block, including its pool, occupies 12 bytes. The 20-byte probes
overrun into the adjacent case at 0800D96C. Their text diffs therefore include
eight extra target bytes for diagnosis, not a proposed expanded replacement.
The next *mapped function* being much later is insufficient boundary protection.

0800D630 uses incoming r6 and existing saved high registers and locals. The
frame is established at 0800D51C (16 local bytes plus register saves), with
the matching restoration at 0800E46E–0800E47C. Recover 0800D51C through
0800E47E, accounting for the final pools before 0800E498, as one enclosing
body with 0800D570, 0800D630 and 0800D960 as internal labels. A standalone
tail-call spelling cannot establish that contract.

## 080095C4: restore the dispatcher's own frame

The target copies live r7 into r0, restores r8/r9 from two saved words,
restores r4–r7, then pops its original return address into r1 and branches
through it. The prologue at 08008A88 saves those same seven words. Both
ordinary branches and long Thumb BL transfers from that dispatcher reach this
tail; the latter do not make it an independently callable C function.

The supplied draft's `r7` pointer is unused and disappears during optimization.
Its null callback and forced zero return survive in the loop/global dumps.
Global allocation assigns only r0, giving a new LR save and its own pop/bx.
Passing an explicit return value or using a separate zero temporary emits a
small C return but cannot restore the caller's saved r8/r9/r4–r7. All profiles
fail. Recover 08008A88 through 080095D2 and its pools before 080095E4 as a
single dispatcher, with 080095C4 as its shared return label.

## 08007368: no link-state extraction exists in the target

The target adds 108 to SP, restores r8/r9/r10, restores r4–r7, and returns
through the saved LR popped into r0. The real prologue at 080064A4 saves these
registers and subtracts the same 108 bytes. Early BL transfers at 080066EC and
08006700 reach this return directly. 08006740 is an internal block, not the
prologue; two older boundary notes have been corrected accordingly.

The draft's read of `g_03007A30.field_14` is unrelated to these instructions.
The loop/global dumps contain the address load, signed extension and shift;
allocation coalesces all three remaining pseudos into r0. Splitting the signed
byte and widened temporary gives the same 15-byte distance under every profile.
An empty C return also fails. There is no signedness or loop-shape adjustment
that supplies the missing inherited frame. Recover 080064A4 through 08007378,
including its pools before 08007398, keeping 08006712, 08006740, 08006776,
0800735C and 08007368 as internal labels.

## Remaining score frontier

| Entry | Differing bytes | Scope |
| --- | ---: | --- |
| 080051FE | 16 | Outside the requested threshold; also a shared epilogue. |
| 08007B28 | 23 | Outside threshold. |
| 08006740 | 53 | Outside threshold; internal block in the sound enclosure above. |
| 0800D51C | 84 | Outside threshold; opener of the scene enclosure above. |
| 08014104 | 123 | Outside threshold. |
| 08014AE0 | 174 | Outside threshold. |
| 080149FC | 199 | Outside threshold. |
| 08013E74 | 223 | Outside threshold. |

## Reproduction and next work

Run commands from the repository root with the configured Python environment.
For each source probe shown in the text evidence, save that source under
`build/` and run `python tools/diffhint.py ADDRESS build/probe.c --compiler PROFILE`.
The six profiles tried were `old`, `standard`, `old-no-gcse`, `old-o1`,
`standard-o1` and `old-no-interwork`. No modern ARM profile was misapplied to
a Thumb entry. There were 78 compiler comparisons: 72 valid comparisons and
six intentionally rejected Thumb-to-ARM call relocations. None was exact.

To inspect the historical compiler's passes, preprocess with the configured
ARM compiler using `-E -P -Isrc`, then compile that result with
`old_agbcc -O2 -mthumb-interwork -da -o build/probe.s`. The `.loop`, `.gcse`
and `.greg` files beside the preprocessed input supplied the retained evidence.
Full intermediate dumps and all per-profile diffs remain under
`build/near-miss-hand/` locally.

Boundary recovery should precede more source tuning for these three enclosures.
Keep the PC-switch veneer in assembly, and exclude it and the three frame
fragments from future standalone C requests. This review changes no service
files, candidate-selection code, ROM configuration or replacement counts.
