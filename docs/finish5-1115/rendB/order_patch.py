"""Diagnostic what-if hook for the private tracing cc1 (never used for matching):
TXS1ORDER="uid,uid,..." (forward order of every insn of ONE block) makes sched1 emit that
block in exactly that order, by picking the wanted insn from the ready list (it waits while
the wanted insn is still queued; aborts if the order breaks a dependence). Without the
variable the compiler is unchanged. Apply after the finish3/finish4 trace patches."""
p = 'sched.c'
t = open(p).read()
old_decl = """  /* Keep life information accurate.  */
  register struct sometimes *regs_sometimes_live;
  int sometimes_max;
"""
new_decl = """  /* Keep life information accurate.  */
  register struct sometimes *regs_sometimes_live;
  int sometimes_max;
  int tx_uids[512], tx_n = 0, tx_pos = 0, tx_spin = 0;
"""
assert t.count(old_decl) == 1
t = t.replace(old_decl, new_decl)
old_init = """  /* Q_SIZE will always be zero here.  */
  q_ptr = 0; clock = 0;"""
new_init = """  if (reload_completed == 0 && getenv ("TXS1ORDER"))
    {
      char *s = getenv ("TXS1ORDER");
      int in_block = 0;
      rtx x;
      while (s && *s && tx_n < 512)
	{
	  tx_uids[tx_n++] = atoi (s);
	  s = strchr (s, ',');
	  if (s) s++;
	}
      for (x = head; x != next_tail; x = NEXT_INSN (x))
	if (INSN_UID (x) == tx_uids[0])
	  in_block = 1;
      if (! in_block)
	tx_n = 0;
      tx_pos = tx_n - 1;
      if (tx_n && file)
	fprintf (file, ";; TXS1ORDER active, %d insns\\n", tx_n);
    }

  /* Q_SIZE will always be zero here.  */
  q_ptr = 0; clock = 0;"""
assert t.count(old_init) == 1
t = t.replace(old_init, new_init)
old_sel = """      SCHED_SORT (ready, new_ready, n_ready);
      if (MAX_BLOCKAGE > 1)
	{
	  new_ready = schedule_select (ready, new_ready, clock, file);"""
new_sel = """      if (tx_n && tx_pos >= 0)
	{
	  int k, found = -1;
	  for (k = 0; k < new_ready; k++)
	    if (INSN_UID (ready[k]) == tx_uids[tx_pos])
	      found = k;
	  if (found < 0)
	    {
	      if (++tx_spin > 100000)
		{
		  fprintf (stderr, "TXS1ORDER: insn %d never became ready\\n", tx_uids[tx_pos]);
		  abort ();
		}
	      n_ready = 0;
	      continue;
	    }
	  {
	    rtx tmp = ready[0];
	    ready[0] = ready[found];
	    ready[found] = tmp;
	  }
	  tx_pos--;
	  n_ready = new_ready;
	  goto tx_chosen;
	}
      SCHED_SORT (ready, new_ready, n_ready);
      if (MAX_BLOCKAGE > 1)
	{
	  new_ready = schedule_select (ready, new_ready, clock, file);"""
assert t.count(old_sel) == 1
t = t.replace(old_sel, new_sel)
old_pick = """      n_ready = new_ready;
      last_scheduled_insn = insn = ready[0];"""
new_pick = """      n_ready = new_ready;
    tx_chosen:
      last_scheduled_insn = insn = ready[0];"""
assert t.count(old_pick) == 1
t = t.replace(old_pick, new_pick)
if '#include <stdlib.h>' not in t[:300]:
    t = '#include <stdlib.h>\n#include <string.h>\n' + t
open(p, 'w').write(t)
print('order patched')
