"""Diagnostic what-if hook for a private copy of agbcc's gcc_arm/sched.c (never used for matching).
TXORDER="uid,uid,...,uid" (program order, top to bottom, every insn of one block): in sched1 the
block that contains the last listed uid is emitted in exactly that order (latencies and unit
hazards ignored for that block only). A uid that is not dependency-ready when its turn comes is
reported on stderr as "TXORDER violation" and the hook switches off for the rest of the block.
Without TXORDER the compiler is unchanged. Also adds TXDBG=S: one "S1 uid=..." line per insn
scheduled in sched1 with its priority and the ready list at that moment."""
p = 'sched.c'
t = open(p).read()

def sub1(old, new):
    global t
    assert t.count(old) == 1, (old[:70], t.count(old))
    t = t.replace(old, new)

sub1("""static int max_priority;
""", """static int max_priority;
static int tx_active, tx_n, tx_pos, tx_ord[1024];
""")
sub1("""      int cost = insn_cost (prev, link, insn);
""", """      int cost = tx_active ? 1 : insn_cost (prev, link, insn);
""")
sub1("""  CLEAR_REG_SET (reg_pending_sets);
  reg_pending_sets_all = 0;
  clear_units ();
""", """  CLEAR_REG_SET (reg_pending_sets);
  reg_pending_sets_all = 0;
  clear_units ();
  tx_active = 0;
  if (reload_completed == 0 && getenv ("TXORDER"))
    {
      char *s = getenv ("TXORDER");
      rtx x;
      tx_n = 0;
      while (s && *s && tx_n < 1024)
	{
	  tx_ord[tx_n++] = atoi (s);
	  s = strchr (s, ',');
	  if (s) s++;
	}
      for (x = head; x; x = NEXT_INSN (x))
	{
	  if (INSN_UID (x) == tx_ord[tx_n - 1])
	    tx_active = 1;
	  if (x == tail)
	    break;
	}
      tx_pos = tx_n - 1;
      if (tx_active)
	fprintf (stderr, "TXORDER block %d active (%d insns)\\n", b, tx_n);
    }
""")
sub1("""      SCHED_SORT (ready, new_ready, n_ready);
      if (MAX_BLOCKAGE > 1)
	{
""", """      SCHED_SORT (ready, new_ready, n_ready);
      if (tx_active)
	{
	  int k, found = -1;
	  for (k = 0; k < new_ready; k++)
	    if (INSN_UID (ready[k]) == tx_ord[tx_pos])
	      found = k;
	  if (found < 0)
	    {
	      fprintf (stderr, "TXORDER violation uid=%d pos=%d ready:", tx_ord[tx_pos], tx_pos);
	      for (k = 0; k < new_ready; k++)
		fprintf (stderr, " %d", INSN_UID (ready[k]));
	      fprintf (stderr, "\\n");
	      tx_active = 0;
	    }
	  else
	    {
	      rtx tmp = ready[found];
	      for (k = found; k > 0; k--)
		ready[k] = ready[k - 1];
	      ready[0] = tmp;
	      tx_pos--;
	    }
	}
      if (MAX_BLOCKAGE > 1 && ! tx_active)
	{
""")
sub1("""      n_ready = new_ready;
      last_scheduled_insn = insn = ready[0];
""", """      n_ready = new_ready;
      last_scheduled_insn = insn = ready[0];
      if (reload_completed == 0 && getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'S'))
	{
	  int k;
	  fprintf (stderr, "S1 b=%d T-%d uid=%d pri=%x ready:", b, clock, INSN_UID (insn), INSN_PRIORITY (insn));
	  for (k = 1; k < n_ready; k++)
	    fprintf (stderr, " %d(%x)", INSN_UID (ready[k]), INSN_PRIORITY (ready[k]));
	  fprintf (stderr, "\\n");
	}
""")
if '#include <stdlib.h>' not in t[:300]:
    t = '#include <stdlib.h>\n#include <string.h>\n' + t
open(p, 'w').write(t)
print('order patched')
