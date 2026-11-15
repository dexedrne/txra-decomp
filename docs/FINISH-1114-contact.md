# Finish pass 14 November: 080181C0 contact rotation

No exact replacement was installed, and no near-miss improved on bytes. The
registry, build and match count are unchanged at 189 replacements.

**Starting point.** The best existing candidate is the 1112b contact-final
source: **919 differing bytes**, 254 edits, 1,660/1,684 bytes, frame 68/72.
The 1,009-byte figure in the 1112c note was measured against an older baseline;
the 919-byte candidate stays the best. Re-measured on worker A with the unchanged
`arm` profile (`-O2 -mthumb-interwork`, end 08018854), it gives the same 919 / 254 /
frame 68. The agbcc_arm binary on worker A hashes
`342687894970c4ed…`, while the 1112 receipts record `26d884f0…`. Both give the
same result for this candidate.

**Finding.** Compiler debug dumps of our own C show why every candidate so far
misses the original frame. See
[near-misses/finish-1114-contact/LOOP-PASSES.md](near-misses/finish-1114-contact/LOOP-PASSES.md).

- The original reloads the record and sine words inside the six-point loop. That
  means its stores to the probe array must alias those loads. Earlier
  candidates store through a block-local pointer with a known base, so the
  loads get hoisted and the frame fills with the wrong values.
- A function-scope pointer that is set once in each six-element loop loses its
  alias base. With it, the first loop-optimization pass reproduces the
  original's hoisting exactly: the j-offset chain, i*4 and i*5 move out;
  i*5<<2, i*25 and i*100 stay in.
- The rerun loop pass that -O2 enables then moves i*20/i*25/i*100 out as well. That
  is the main remaining structural difference. The spill order now matches the
  original through the first ten values (j … known, i*16, s1).
- Diagnostic only: with `-fno-rerun-loop-opt` the same source reaches the
  original 72-byte frame and the original inner-loop shape (981 differing
  bytes). That flag is not admissible. It breaks the installed neighbour
  080165BC (its output crosses its boundary), while 08016C18, 08017E68, 08017F64,
  08018854 and 080076F4 stay exact with it. So the original source must block the
  second pass's motion some other way, and that mechanism is not found.

Under the real profile the retained structural source scores worse on bytes
(1,049 differing, 248 edits, 1,668 bytes, frame 68). It is kept as structural
evidence, not as the best near-miss.

**Not run:** the permuter. The length (−16/−24 bytes) and frame (68/72) still
differ structurally, so register and ordering permutation cannot close the gap.
decomp-permuter is also not installed on worker A. No boundary repair was needed:
the owner 080181C0–08018854 is complete, with pools at 080185B4, 080187C4 and
08018848. No Ghidra view was used, since worker A is not worker B and the repo's
disassembly was enough.

**Receipts** (all in `docs/near-misses/finish-1114-contact/`):
- `func_080181C0.c`, `candidate.json`, `candidate.diff.txt.gz`: retained structural
  source under the profile.
- `diagnostic-no-rerun.json`, `.diff.txt.gz`: the diagnostic flag result, marked
  `admissible: false`.
- `LOOP-PASSES.md`: movable decisions for both passes, and the frame order compared
  with the original.
- Tool: `tools/diag_rerun1114.py`. It measures with an extra flag, or re-checks the
  installed ARM replacements with it, and has no admission authority.

All compiles ran on worker A. Nothing was built on the laptop. No ROM bytes were
copied or printed.

**Next:** find the source feature that keeps the second loop pass from moving
the i-index chain. In that pass, desirability alone cannot stop it
(28*2*2 ≥ ~38 insns), so the insn must be unsafe, not a movable, or the loop must
not be rescanned. Also explain why zpos is spilled after j*100 and i*5.

**Scope note on "done".** progress.json still reports 719,822 unknown ROM bytes
that are not mapped as code or data. The 237-entry registry is therefore not
known to cover all code, and "48 functions left" is not yet a proven finish
line.

matches installed: none
near-misses improved: none (080181C0 stays at 919 differing bytes; the new structural source reproduces the original's first-pass loop hoisting and frame order through s1, but scores 1049 under the profile)
what blocks the rest: under the required -O2 profile, the second loop-optimization pass moves the inner i-index multiply chain out of the six-point loop, which the original did not; the source feature that prevents this is not yet identified.
