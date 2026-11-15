"""Diagnostic-only debug prints and what-if overrides for a PRIVATE COPY of the
pinned agbcc ARM compiler sources (the gcc_arm/ directory, 2.9-arm-000512).

Copy gcc_arm/ (with its sibling libiberty/ and include/) to a scratch folder on a
worker, run this script inside the copy, then `make cc1`.  With no environment
variable set, the rebuilt cc1 must produce assembly identical to the official
agbcc_arm (checked: same output for every candidate in this round).  Never used
for matching or admission.

TXDBG letters (stderr):  L  local-alloc qty order and chosen register per block
                         G  global find_reg result per allocno
                         U  update_equiv_regs live-length doubling per pseudo
What-if overrides (diagnostic only):
  TXLEN="regno:len,..."   set a pseudo's global-allocation live length
  TXSPILL="regno,..."     keep a pseudo out of local and global allocation
"""
def sub1(path, old, new):
    t = open(path).read()
    assert t.count(old) == 1, (path, old[:60], t.count(old))
    open(path, 'w').write(t.replace(old, new))
def inc(path):
    t = open(path).read()
    if '#include <stdlib.h>' not in t:
        open(path, 'w').write('#include <stdlib.h>\n#include <string.h>\n' + t)

sub1('local-alloc.c', """	  reg_renumber[i] = qty_phys_reg[q] + reg_offset[i];
      }
}
""", """	  reg_renumber[i] = qty_phys_reg[q] + reg_offset[i];
      }
  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'L'))
    {
      int k;
      for (k = 0; k < next_qty; k++)
	{
	  int qq = qty_order[k], rr;
	  fprintf (stderr, "LQ b=%d ord=%d q=%d birth=%d death=%d refs=%d sugg=%d csugg=%d phys=%d regs=",
		   b, k, qq, qty_birth[qq], qty_death[qq], qty_n_refs[qq],
		   qty_phys_num_sugg[qq], qty_phys_num_copy_sugg[qq], qty_phys_reg[qq]);
	  for (rr = qty_first_reg[qq]; rr >= 0; rr = reg_next_in_qty[rr])
	    fprintf (stderr, "%d,", rr);
	  fprintf (stderr, "\\n");
	}
    }
}
""")
sub1('local-alloc.c', """	      REG_LIVE_LENGTH (regno) *= 2;
""", """	      REG_LIVE_LENGTH (regno) *= 2;
	      if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'U'))
		fprintf (stderr, "UE reg=%d uid=%d doubled to %d\\n", regno, INSN_UID (insn), REG_LIVE_LENGTH (regno));
""")
inc('local-alloc.c')

sub1('global.c', """  /* Did we find a register?  */

  if (best_reg >= 0)
""", """  /* Did we find a register?  */
  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'G'))
    fprintf (stderr, "GF reg=%d alt=%d acc=%d retry=%d best=%d refs=%d len=%d\\n",
	     allocno_reg[allocno], alt_regs_p, accept_call_clobbered, retrying, best_reg,
	     allocno_n_refs[allocno], allocno_live_length[allocno]);

  if (best_reg >= 0)
""")
sub1('global.c', """		  /* Hard reg REGNO was used less in total by local regs
		     than it would be used by this one allocno!  */
		  int k;
""", """		  /* Hard reg REGNO was used less in total by local regs
		     than it would be used by this one allocno!  */
		  int k;
		  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'G'))
		    fprintf (stderr, "GK reg=%d kicks hard=%d\\n", allocno_reg[allocno], regno);
""")
sub1('global.c', """	  if (allocno_live_length[i] == 0)
	    allocno_live_length[i] = -1;
	}
""", """	  if (allocno_live_length[i] == 0)
	    allocno_live_length[i] = -1;
	}
      if (getenv ("TXLEN"))
	{
	  char *s = getenv ("TXLEN");
	  while (*s)
	    {
	      int rg = strtol (s, &s, 10), ln;
	      if (*s == ':') s++;
	      ln = strtol (s, &s, 10);
	      if (*s == ',') s++;
	      for (i = 0; i < (size_t) max_allocno; i++)
		if (allocno_reg[i] == rg)
		  allocno_live_length[i] = ln;
	    }
	}
""")
inc('global.c')
sub1('local-alloc.c', """  /* Force loop below to initialize entire quantity array.  */""", """  if (getenv ("TXSPILL"))
    {
      char *s = getenv ("TXSPILL");
      while (*s)
	{
	  int rg = strtol (s, &s, 10);
	  if (*s == ',') s++;
	  if (rg >= FIRST_PSEUDO_REGISTER && rg < max_regno)
	    {
	      reg_qty[rg] = -1;
	      REG_LIVE_LENGTH (rg) = -1;
	    }
	}
    }

  /* Force loop below to initialize entire quantity array.  */""")
print('patched')
