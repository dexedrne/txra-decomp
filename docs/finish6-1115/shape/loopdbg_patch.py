"""Diagnostic trace for a private copy of agbcc's gcc_arm/loop.c (never used for matching).
TXDBG contains 'M': scan_loop prints one "LM" line per single-set insn with why it is or is not
a movable candidate (maybe_never, used-before, invariant_p result, set count, may_trap)."""
p = 'loop.c'
t = open(p).read()
old = """	  /* Don't try to optimize a register that was made
	     by loop-optimization for an inner loop.
	     We don't know its life-span, so we can't compute the benefit.  */
	  if (REGNO (SET_DEST (set)) >= max_reg_before_loop)"""
new = """	  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'M'))
	    fprintf (stderr, "LM uid=%d reg=%d maxb=%d never=%d call=%d inbb=%d inv=%d nset=%d trap=%d\\n",
		     INSN_UID (p), REGNO (SET_DEST (set)), REGNO (SET_DEST (set)) >= max_reg_before_loop,
		     maybe_never, call_passed, reg_in_basic_block_p (p, SET_DEST (set)), invariant_p (src),
		     VARRAY_INT (set_in_loop, REGNO (SET_DEST (set))), may_trap_p (src));
""" + old
assert t.count(old) == 1
t = t.replace(old, new)
if '#include <stdlib.h>' not in t[:300]:
    t = '#include <stdlib.h>\n#include <string.h>\n' + t
open(p, 'w').write(t)
print('loopdbg patched')
