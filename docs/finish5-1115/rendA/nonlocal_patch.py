"""Diagnostic what-if hook for a private copy of agbcc's gcc_arm/local-alloc.c (never used for
matching): TXNONLOCAL="pseudo,pseudo,..." makes local-alloc leave those pseudos to global
allocation (as if they had two deaths or spanned blocks). Unchanged without the variable."""
p = 'local-alloc.c'
t = open(p).read()
old = """      if (REG_BASIC_BLOCK (i) >= 0 && REG_N_DEATHS (i) == 1
	  && (reg_alternate_class (i) == NO_REGS
	      || ! CLASS_LIKELY_SPILLED_P (reg_preferred_class (i))))
	reg_qty[i] = -2;
      else
	reg_qty[i] = -1;
"""
new = """      if (REG_BASIC_BLOCK (i) >= 0 && REG_N_DEATHS (i) == 1
	  && (reg_alternate_class (i) == NO_REGS
	      || ! CLASS_LIKELY_SPILLED_P (reg_preferred_class (i))))
	reg_qty[i] = -2;
      else
	reg_qty[i] = -1;
      if (getenv ("TXNONLOCAL"))
	{
	  char *s = getenv ("TXNONLOCAL");
	  while (s && *s)
	    {
	      if (atoi (s) == i)
		reg_qty[i] = -1;
	      s = strchr (s, ',');
	      if (s) s++;
	    }
	}
"""
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, new))
print('nonlocal patched')
