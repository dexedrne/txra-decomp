# ARM compiler comparison and cache identity

ARM candidate compilation previously used Thumb instruction scoring and review
diffs. A single changed ARM instruction was incorrectly counted as two Thumb
instruction changes. Scoring and diffs now take an explicit instruction mode;
legacy callers retain the Thumb default. Compile jobs select the emitted mode,
and both search drivers retain that mode in review output.

The resumable search now uses only the target mode's compiler profiles for
seeding, random restarts and profile neighborhoods. Its context also includes
the actual agbcc_arm executable, or a stable absence marker for Thumb-only
installations. Replacing, installing or removing that compiler invalidates
previous scores and checkpoints. Existing byte-level acceptance, relocation,
complete-extent and next-entry checks are unchanged.

Tests reproduced the scoring, mixed-profile scheduling and missing compiler
fingerprint bugs before the fixes. Fresh worker D validation ran both focused test
files:21run,20passed,1skipped. The existing real compiler/resume fixture skipped
because fewer than two eligible retained unmatched drafts exist. Tests included
real compiler comparisons and cache round trips; no model service was called.

Three independent controls reproduced their complete accepted byte sequences:
modern ARM08018E88(4bytes), historical ARM08017E68(252bytes), historical Thumb
08014518(12bytes). Every corrected instruction/byte score was0/0.

Two retained full080181C0 candidates were freshly compiled with both ARM
profiles. Neither matches the1684-byte target. The older candidate produced
1640bytes with historical ARM(score303instructions/1237bytes); the newer
produced1644bytes(score221/1143). Modern ARM produced1292bytes(score413/1581)
and1408bytes(score414/1556). These are fresh scores of existing hypotheses,
not new source improvements or comparisons with historical Thumb-decoded
ARM scores. No candidate was installed and matching remains179/229.

The private ROM stayed on worker D. Validation used an owned5,232,640-byte temporary
source archive, not a new Git checkout. Compiler scratch directories and that
source fixture were removed; the original ROM hash stayed unchanged. Numeric
proof is ARM-COMPARISON-1107.json; detailed instruction diffs remain in the
owner's local review artifacts.

No runtime, generated native translation, accepted C source, ROM configuration,
clock, audio, controller or game asset changes are included. No new179-function
ROM build, pacing gain, physical device or native gameplay acceptance is claimed.
