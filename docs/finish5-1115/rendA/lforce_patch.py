"""Diagnostic what-if hook for a private copy of agbcc's gcc_arm/local-alloc.c (never used for
matching): TXLFORCE="pseudo:hardreg,..." gives the local qty containing that pseudo that hard
register (unadjusted lifetime) when it is free, before the normal search. Unchanged without it."""
p = 'local-alloc.c'
t = open(p).read()
old = """  for (i = 0; i < next_qty; i++)
    {
      q = qty_order[i];
      if (qty_phys_reg[q] < 0)
	{
#ifdef INSN_SCHEDULING
	  /* These values represent the adjusted lifetime of a qty so"""
new = """  for (i = 0; i < next_qty; i++)
    {
      q = qty_order[i];
      if (qty_phys_reg[q] < 0 && getenv ("TXLFORCE"))
	{
	  char *s = getenv ("TXLFORCE");
	  while (s && *s)
	    {
	      int pr = -1, hr = -1, r, ins, ok;
	      if (sscanf (s, "%d:%d", &pr, &hr) == 2)
		for (r = qty_first_reg[q]; r >= 0; r = reg_next_in_qty[r])
		  if (r == pr)
		    {
		      ok = 1;
		      for (ins = qty_birth[q]; ins < qty_death[q]; ins++)
			if (TEST_HARD_REG_BIT (regs_live_at[ins], hr))
			  ok = 0;
		      if (ok)
			{
			  post_mark_life (hr, qty_mode[q], 1, qty_birth[q], qty_death[q]);
			  qty_phys_reg[q] = hr;
			}
		    }
	      s = strchr (s, ',');
	      if (s) s++;
	    }
	}
      if (qty_phys_reg[q] < 0)
	{
#ifdef INSN_SCHEDULING
	  /* These values represent the adjusted lifetime of a qty so"""
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, new))
print('lforce patched')
