"""Diagnostic what-if hook for the private tracing cc1 (never used for matching):
TXFORCE="pseudo:hardreg,..." makes global find_reg give that pseudo that hard register
when it does not conflict.  Without TXFORCE the compiler is unchanged."""
p = 'global.c'
t = open(p).read()
old = """  /* Did we find a register?  */
  if (getenv ("TXDBG")"""
new = """  if (getenv ("TXFORCE"))
    {
      char *s = getenv ("TXFORCE");
      while (s && *s)
	{
	  int pr = -1, hr = -1;
	  if (sscanf (s, "%d:%d", &pr, &hr) == 2 && pr == allocno_reg[allocno]
	      && ! TEST_HARD_REG_BIT (used1, hr))
	    best_reg = hr;
	  s = strchr (s, ',');
	  if (s) s++;
	}
    }
  /* Did we find a register?  */
  if (getenv ("TXDBG")"""
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, new))
print('force patched')
