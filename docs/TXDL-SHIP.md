# Closest-attempt handoff

TXRA remains at **156 matched functions / 37,824 bytes / 44.430%** of mapped
code. All four current attempts scoring at most 15 were tried in the requested
order, with **zero new exact matches**. Their scores count differing bytes,
not instructions. The low scores came from incomplete boundaries or wrong
behavior, rather than four nearly recovered standalone C functions.

| Entry | Score | What was tried and what remains |
| --- | ---: | --- |
| 08018E84 | 1 | Explicit/implicit returns and a diagnostic ARM-helper call across six Thumb profiles. Target switches state through PC; C returns through LR. Keep the wrapper in assembly. Its ARM half is already matched. |
| 0800D960 | 2 | Split pointer/value lifetimes, restore the missing call, reverse initialization order and explicit void return across six profiles. The target branches into the frame created at 0800D51C; normal calls add a separate frame and overrun the 12-byte block. Recover its full enclosing body. |
| 080095C4 | 10 | Original draft, direct argument return and separate zero temporary across six profiles. Original draft calls null and returns zero; target restores the dispatcher frame and returns live r7. Recover 08008A88 with this shared epilogue. |
| 08007368 | 15 | Original draft, empty return and separate signed/widened temporaries across six profiles. Target restores the 108-byte sound frame; draft performs an unrelated link-state read. Recover 080064A4 with all its internal blocks. |

There were **78 source/profile trials**: 72 byte comparisons and six expected
rejections of invalid Thumb-to-ARM BL relocations. None was exact. The actual
compiler loop, global-optimization and allocation dumps were inspected and
retained in [the per-entry evidence](near-misses/hand-20261031/README.md).
Two older documents incorrectly identified 08006740 as the sound prologue;
they now point to the verified prologue at 080064A4.

The evidence commit is `1ddc3a4` (closest attempts and enclosing frame correction).
The separate handoff commit contains this note and `TXDL-DONE`. No replacement
was installed, so there are no exact-match commits or resolved near-miss files
to retire. The active service and its working tree were neither edited nor
stopped. No push, deployment or merge was performed.

Validation:

- Fresh `make check`: **170 tests passed** in 190.168 seconds; all 156 installed
  C replacements were recompiled and checked before the full ROM rebuild.
- Full ROM SHA-1: `4197339d4add74bb40ed02a8fba5e58096afb487`, identical to the
  owner's supplied ROM. No original bytes or extracted binaries are committed.
- Evidence consistency check: all four eligible entries covered, all six
  profiles present, zero exact results, counts unchanged, no absolute home
  paths or instruction encodings in the retained evidence.
- Final frontier reread: still exactly these four scores at or below 15.
  All eight higher scores are listed in the review; the next is 080051FE at 16.
- `git diff --check`: passed.

No pictures or clips were produced: this task changed matching documentation,
with no gameplay, animation, vehicle, menu, world or runtime changes to show.
No new boot, playability, race or save milestone is claimed.

Still unfinished: all four target entries remain unmatched. The three full
enclosing C bodies were identified but not reconstructed or installed; more
standalone expression changes would not resolve their inherited frames.
Future standalone requests should exclude these fragments and the PC-switch
veneer. That candidate-selection change is a recommendation, not a service
edit made by this job. Fresh analysis also weakened the previously reviewed
indirect-target annotation at 080065CC; that unrelated generated-file change
was reverted. The regeneration discrepancy remains outside this patch.

Owner notes: `OWNER-NOTES.md` was absent at startup, each major step and the
final reread, so there were no appended notes to address or leave unresolved.
The owner's progress request is answered by the verified unchanged count and
the concrete enclosing-body recovery plan above. `TXDL-DONE` marks completion
of this bounded review, not completion of the decompilation.

Matched before/after: 156 / 156; 44.430% / 44.430% of mapped code.
Still fails: one state-switch wrapper and three shared-frame fragments; no exact additions.
Next: recover the three enclosing bodies and stop treating their internal entries as standalone C.
