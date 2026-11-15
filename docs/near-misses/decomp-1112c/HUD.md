# HUD pass

The complete owner improves **3,152 → 3,144 differing bytes**, remaining
uninstalled. Both sources emit 4,124 bytes with 36-byte local frames. Instruction
edit distance changes 1,022 → 1,023, so this is a byte-distance improvement,
not an instruction-distance improvement. The checker end is still 08005238.

The retained change computes the map z coefficient address at its use rather
than carrying a captured pointer, reuses the earlier scalar for map scale,
and gives the map angle its own scope. This follows the decompiler's repeated
coefficient addressing and phase-separated lifetimes. The intermediate
two-byte improvement had a 40-byte frame; the final source recovers 36.
Other measured point captures, flash/smoke cursor mixtures, opening scopes and
call-time arithmetic did not beat the retained complete owner. Compiler and
boundary rejections remain diagnostics, never installable results.

The unchanged prior-C check passes **1,024 state and ordered-call fixtures**
with undefined-behavior sanitization and all six transform aliases. A separate
new check executes the original instructions and original helpers against the
compiled candidate in memory: **192 cases, 185 state-changing cases and 9,194
ordered helper calls agree**. It also checks IWRAM outside the stack region,
saved registers and stack restoration. Inputs are bounded synthetic states;
lookup data is original. No mock helpers, saved emulator image or ROM slice is
used. These checks do not establish arbitrary-state behavior or gameplay, and
do not replace the exact-byte and whole-ROM installation gates.

The structural receipt still shows 524 aligned register-operand differences,
256 original and 250 compiled unpaired instruction rows, and 99 versus 102
referenced pool words. The projected effect region is unchanged at 838
positional byte differences in 868 bytes. Region counts include displacement;
they are layout diagnostics, not additive causal byte counts.

Next: keep the map lifetime change and recover the opening scale stack role
and projected second-width/tag lifetimes together. Moving coordinate captures
or introducing field cursors alone has again stalled. A separate scale local
still stays in a register where the original spills it before the first
scale call. No narrower coefficient, artificial spill or frame padding is
justified by the view.

Reproduce with `tools/measure_candidate.py`, source `func_0800421C.c`, entry
0800421C, end 08005238, profile `old`. The original-instruction runner is
`tools/check_hud_original1112c.py`; it takes candidate and receipt paths.
