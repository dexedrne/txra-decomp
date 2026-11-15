"""Diagnostic-only debug prints for a private copy of agbcc's gcc_arm/ (2.9-arm-000512).
Adapted from docs/finish2-1115/stream/trace_patch.py. Run inside the copy, then `make cc1`.
TXDBG=R prints reload register picks (RA) and inheritance (RI); G prints global find_reg
results (GF) and local-alloc kick-outs (GK). Never used for matching; its assembly must
equal the official agbcc_arm output before a trace is trusted."""
def sub1(path, old, new):
    t = open(path).read()
    assert t.count(old) == 1, (path, old[:60], t.count(old))
    t = t.replace(old, new)
    if '#include <stdlib.h>' not in t[:200]:
        t = '#include <stdlib.h>\n#include <string.h>\n' + t
    open(path, 'w').write(t)

sub1('reload1.c', """	    /* The reg is OK.  */
	    last_spill_reg = i;
""", """	    /* The reg is OK.  */
	    if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'R'))
	      fprintf (stderr, "RA uid=%d r=%d reg=%d prev=%d n_spills=%d in=%d out=%d when=%d opnum=%d\\n",
		       INSN_UID (insn), r, spill_regs[i], last_spill_reg < 0 ? -1 : spill_regs[last_spill_reg], n_spills,
		       reload_in[r] != 0, reload_out[r] != 0, (int) reload_when_needed[r], reload_opnum[r]);
	    last_spill_reg = i;
""")
sub1('reload1.c', """			      reload_reg_rtx[r] = last_reg;
			      reload_inherited[r] = 1;
			      reload_inheritance_insn[r]
				= reg_reloaded_insn[i];
""", """			      reload_reg_rtx[r] = last_reg;
			      reload_inherited[r] = 1;
			      if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'R'))
				fprintf (stderr, "RI uid=%d r=%d reg=%d\\n", INSN_UID (insn), r, i);
			      reload_inheritance_insn[r]
				= reg_reloaded_insn[i];
""")
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
print('patched')
