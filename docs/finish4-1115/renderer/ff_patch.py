"""Diagnostic: print find_free_reg's used mask (TXDBG contains F). Private tracing cc1 only."""
p = 'local-alloc.c'
t = open(p).read()
old = """	  if (j == size1)
	    {
	      /* Mark that this register is in use between its birth and death
		 insns.  */
	      post_mark_life (regno, mode, 1, born_index, dead_index);
	      return regno;"""
new = """	  if (j == size1)
	    {
	      /* Mark that this register is in use between its birth and death
		 insns.  */
	      if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'F'))
		fprintf (stderr, "FF q=%d born=%d dead=%d used=%lx sugg=%d -> %d\\n", qty, born_index, dead_index,
			 (unsigned long) used, just_try_suggested, regno);
	      post_mark_life (regno, mode, 1, born_index, dead_index);
	      return regno;"""
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, new))
print('ff patched')
