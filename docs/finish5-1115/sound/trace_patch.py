"""Diagnostic-only debug prints for a private copy of the pinned agbcc sources.

Run inside a copy of agbcc's gcc/ directory on a worker, then `make old -j1`.
The rebuilt old_agbcc prints to stderr when TXDBG is set (L = local-alloc qty
decisions per block, G = global find_reg results and local-alloc kick-outs,
R = reload register picks and inheritance). Its assembly output must be compared
with the official compiler before any trace is trusted. Never used for matching.
"""
import re, sys
def sub1(path, old, new):
    t = open(path).read()
    assert t.count(old) == 1, (path, old[:60], t.count(old))
    open(path, 'w').write(t.replace(old, new))

# local-alloc: dump qty decisions per block
sub1('local-alloc.c', """  /* Now propagate the register assignments
     to the pseudo regs belonging to the qtys.  */

  for (q = 0; q < next_qty; q++)
    if (qty_phys_reg[q] >= 0)
      {
	for (i = qty_first_reg[q]; i >= 0; i = reg_next_in_qty[i])
	  reg_renumber[i] = qty_phys_reg[q] + reg_offset[i];
      }
}
""", """  /* Now propagate the register assignments
     to the pseudo regs belonging to the qtys.  */

  for (q = 0; q < next_qty; q++)
    if (qty_phys_reg[q] >= 0)
      {
	for (i = qty_first_reg[q]; i >= 0; i = reg_next_in_qty[i])
	  reg_renumber[i] = qty_phys_reg[q] + reg_offset[i];
      }
  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'L'))
    {
      int k;
      for (k = 0; k < next_qty; k++)
	{
	  int qq = qty_order[k], rr;
	  fprintf (stderr, "LQ b=%d ord=%d q=%d pri=%d birth=%d death=%d refs=%d sugg=%d csugg=%d phys=%d regs=",
		   b, k, qq,
		   (int) (((double) (floor_log2 (qty_n_refs[qq]) * qty_n_refs[qq] * qty_size[qq]) / (qty_death[qq] - qty_birth[qq])) * 10000),
		   qty_birth[qq], qty_death[qq], qty_n_refs[qq], qty_phys_num_sugg[qq], qty_phys_num_copy_sugg[qq], qty_phys_reg[qq]);
	  for (rr = qty_first_reg[qq]; rr >= 0; rr = reg_next_in_qty[rr])
	    fprintf (stderr, "%d,", rr);
	  fprintf (stderr, "\\n");
	}
    }
}
""")
t = open('local-alloc.c').read()
if '#include <stdlib.h>' not in t:
    t = '#include <stdlib.h>\n#include <string.h>\n' + t
    open('local-alloc.c', 'w').write(t)

# global: dump find_reg outcome
sub1('global.c', """  /* Did we find a register?  */

  if (best_reg >= 0)
    {
      register int lim, j;
      HARD_REG_SET this_reg;
""", """  /* Did we find a register?  */
  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'G'))
    fprintf (stderr, "GF reg=%d alt=%d acc=%d retry=%d best=%d refs=%d len=%d calls=%d\\n",
	     allocno_reg[allocno], alt_regs_p, accept_call_clobbered, retrying, best_reg,
	     allocno_n_refs[allocno], allocno_live_length[allocno], allocno_calls_crossed[allocno]);

  if (best_reg >= 0)
    {
      register int lim, j;
      HARD_REG_SET this_reg;
""")
sub1('global.c', """		  /* Hard reg REGNO was used less in total by local regs
		     than it would be used by this one allocno!  */
		  int k;
""", """		  /* Hard reg REGNO was used less in total by local regs
		     than it would be used by this one allocno!  */
		  int k;
		  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'G'))
		    fprintf (stderr, "GK reg=%d kicks hard=%d local_refs=%d local_len=%d\\n",
			     allocno_reg[allocno], regno, local_reg_n_refs[regno], local_reg_live_length[regno]);
""")
t = open('global.c').read()
if '#include <stdlib.h>' not in t:
    t = '#include <stdlib.h>\n#include <string.h>\n' + t
    open('global.c', 'w').write(t)

# reload: dump allocate_reload_reg picks
sub1('reload1.c', """	    /* The reg is OK.  */
	    last_spill_reg = i;
""", """	    /* The reg is OK.  */
	    if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'R'))
	      fprintf (stderr, "RA uid=%d r=%d reg=%d prev=%d n_spills=%d in=%d out=%d\\n",
		       INSN_UID (insn), r, spill_regs[i], last_spill_reg < 0 ? -1 : spill_regs[last_spill_reg], n_spills,
		       reload_in[r] != 0, reload_out[r] != 0);
	    last_spill_reg = i;
""")
sub1('reload1.c', """			      reload_reg_rtx[r] = last_reg;
			      reload_inherited[r] = 1;
""", """			      reload_reg_rtx[r] = last_reg;
			      reload_inherited[r] = 1;
			      if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'R'))
				fprintf (stderr, "RI uid=%d r=%d reg=%d\\n", INSN_UID (insn), r, i);
""")
t = open('reload1.c').read()
if '#include <stdlib.h>' not in t:
    t = '#include <stdlib.h>\n#include <string.h>\n' + t
    open('reload1.c', 'w').write(t)
print('patched')
