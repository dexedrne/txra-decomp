"""Diagnostic what-if hook for the private tracing cc1 (never used for matching):
TXNONLOCAL="pseudo,pseudo,..." makes local-alloc treat those pseudos as non-local (left to
global-alloc), as if they had two deaths. Without the variable the compiler is unchanged."""
p = 'local-alloc.c'
t = open(p).read()
old = """	reg_qty[i] = -2;
      else
	reg_qty[i] = -1;
    }"""
new = """	reg_qty[i] = -2;
      else
	reg_qty[i] = -1;
    }
  if (getenv ("TXNONLOCAL"))
    {
      char *s = getenv ("TXNONLOCAL");
      while (s && *s)
	{
	  int r = atoi (s);
	  if (r >= FIRST_PSEUDO_REGISTER && r < max_regno)
	    reg_qty[r] = -1;
	  s = strchr (s, ',');
	  if (s) s++;
	}
    }"""
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, new))
print('nonlocal patched')
