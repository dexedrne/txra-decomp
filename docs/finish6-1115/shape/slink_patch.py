"""Diagnostic trace for a private copy of agbcc's gcc_arm/sched.c (never used for matching).
TXDBG contains 'K': in sched1, one "SL" line per dependence link resolved when an insn is
scheduled (consumer uid, producer uid, link kind, cost, remaining ref count, tick, new priority),
and one "SU" line per unit-blocked insn in schedule_select. Output assembly is unchanged."""
p = 'sched.c'
t = open(p).read()
def sub1(old, new):
    global t
    assert t.count(old) == 1, (old[:70], t.count(old))
    t = t.replace(old, new)
sub1("""	  /* Adjust the priority of PREV and either put it on the ready
	     list or queue it.  */
	  adjust_priority (prev);
""", """	  /* Adjust the priority of PREV and either put it on the ready
	     list or queue it.  */
	  adjust_priority (prev);
	  if (reload_completed == 0 && getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'K'))
	    fprintf (stderr, "SL T-%d insn=%d prev=%d kind=%d cost=%d ready_at=T-%d pri=%x birth=%d\\n",
		     clock, INSN_UID (insn), INSN_UID (prev), (int) REG_NOTE_KIND (link), cost,
		     clock + (cost < 1 ? 1 : cost), INSN_PRIORITY (prev), birthing_insn_p (PATTERN (prev)));
""")
sub1("""      if ((INSN_REF_COUNT (prev) -= 1) != 0)
	{
""", """      if ((INSN_REF_COUNT (prev) -= 1) != 0)
	{
	  if (reload_completed == 0 && getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'K'))
	    fprintf (stderr, "SW T-%d insn=%d prev=%d kind=%d cost=%d left=%d\\n",
		     clock, INSN_UID (insn), INSN_UID (prev), (int) REG_NOTE_KIND (link), cost,
		     INSN_REF_COUNT (prev));
""")
open(p, 'w').write(t)
print('slink patched')
