"""Extra diagnostic prints (sound lane), applied after the stream lane's trace_patch.py
to a private copy of agbcc's gcc/ on a worker; then `make old -j1`.
TXDBG letters: O = reload spill-register order per insn (hard reg:uses),
S = pseudos kicked out of a hard reg in finish_spills and stack-slot assignment in alter_reg.
Diagnostic only: compare its assembly with the official compiler before trusting a trace."""
def sub1(path, old, new):
    t = open(path).read()
    if t.count(new) == 1 and new != old:
        return
    assert t.count(old) == 1, (path, old[:60], t.count(old))
    open(path, 'w').write(t.replace(old, new))

sub1('reload1.c', """  for (i = 0; i < FIRST_PSEUDO_REGISTER; i++)
    if (TEST_HARD_REG_BIT (bad_spill_regs, hard_reg_n_uses[i].regno))
      potential_reload_regs[o++] = hard_reg_n_uses[i].regno;
}
""", """  for (i = 0; i < FIRST_PSEUDO_REGISTER; i++)
    if (TEST_HARD_REG_BIT (bad_spill_regs, hard_reg_n_uses[i].regno))
      potential_reload_regs[o++] = hard_reg_n_uses[i].regno;
  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'O'))
    {
      fprintf (stderr, "RO uid=%d", INSN_UID (chain->insn));
      for (i = 0; i < FIRST_PSEUDO_REGISTER; i++)
	if (! TEST_HARD_REG_BIT (bad_spill_regs, hard_reg_n_uses[i].regno))
	  fprintf (stderr, " %d:%d", hard_reg_n_uses[i].regno, hard_reg_n_uses[i].uses);
      fprintf (stderr, "\\n");
    }
}
""")
sub1('reload1.c', """	SET_HARD_REG_BIT (pseudo_previous_regs[i], reg_renumber[i]);
	/* Mark it as no longer having a hard register home.  */
""", """	SET_HARD_REG_BIT (pseudo_previous_regs[i], reg_renumber[i]);
	if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'S'))
	  fprintf (stderr, "SP pseudo=%d from=%d refs=%d bb=%d sets=%d deaths=%d\\n", i, reg_renumber[i],
		   REG_N_REFS (i), REG_BASIC_BLOCK (i), REG_N_SETS (i), REG_N_DEATHS (i));
	/* Mark it as no longer having a hard register home.  */
""")
sub1('reload1.c', """      /* Save the stack slot for later.   */
      reg_equiv_memory_loc[i] = x;
""", """      /* Save the stack slot for later.   */
      reg_equiv_memory_loc[i] = x;
      if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'S'))
	{
	  rtx a = XEXP (x, 0);
	  fprintf (stderr, "SS pseudo=%d from=%d off=%d refs=%d bb=%d\\n", i, from_reg,
		   GET_CODE (a) == PLUS && GET_CODE (XEXP (a, 1)) == CONST_INT ? (int) INTVAL (XEXP (a, 1)) : -1,
		   REG_N_REFS (i), REG_BASIC_BLOCK (i));
	}
""")
sub1('reload1.c', """  delete_address_reloads (output_reload_insn, insn);
  PUT_CODE (output_reload_insn, NOTE);
  NOTE_SOURCE_FILE (output_reload_insn) = 0;
  NOTE_LINE_NUMBER (output_reload_insn) = NOTE_INSN_DELETED;

}
""", """  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'S'))
    fprintf (stderr, "SD uid=%d pseudo=%d store=%d\\n", INSN_UID (insn), REGNO (reg), INSN_UID (output_reload_insn));
  delete_address_reloads (output_reload_insn, insn);
  PUT_CODE (output_reload_insn, NOTE);
  NOTE_SOURCE_FILE (output_reload_insn) = 0;
  NOTE_LINE_NUMBER (output_reload_insn) = NOTE_INSN_DELETED;

}
""")
sub1('reload1.c', """      fprintf (stderr, "\\n");
    }
}
""", """      fprintf (stderr, "\\n");
      if (getenv ("TXUID") && atoi (getenv ("TXUID")) == INSN_UID (chain->insn))
	{
	  int j;
	  EXECUTE_IF_SET_IN_REG_SET
	    (chain->live_before, FIRST_PSEUDO_REGISTER, j,
	     {
	       if (reg_renumber[j] >= 0)
		 fprintf (stderr, "  live_before pseudo=%d hard=%d refs=%d\\n", j, reg_renumber[j], REG_N_REFS (j));
	     });
	  EXECUTE_IF_SET_IN_REG_SET
	    (chain->live_after, FIRST_PSEUDO_REGISTER, j,
	     {
	       if (reg_renumber[j] >= 0)
		 fprintf (stderr, "  live_after pseudo=%d hard=%d refs=%d\\n", j, reg_renumber[j], REG_N_REFS (j));
	     });
	}
    }
}
""")
sub1('reload1.c', """  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'O'))
    {
      fprintf (stderr, "RO uid=%d", INSN_UID (chain->insn));""", """  if (getenv ("TXFORCE"))
    {
      /* Diagnostic experiment only: TXFORCE=uid:reg moves reg to the front.  */
      int fu = -1, fr = -1, k, m;
      if (getenv ("TXFORCE")[0] == 'p')
	{
	  /* TXFORCE=p<pseudo>: use that pseudo's hard reg at the first insn that needs
	     reloads while it is live.  */
	  static int done;
	  int pr = atoi (getenv ("TXFORCE") + 1);
	  if (! done && pr < max_regno && reg_renumber[pr] >= 0
	      && (REGNO_REG_SET_P (chain->live_before, pr) || REGNO_REG_SET_P (chain->live_after, pr)))
	    fu = INSN_UID (chain->insn), fr = reg_renumber[pr], done = 1;
	}
      else
	sscanf (getenv ("TXFORCE"), "%d:%d", &fu, &fr);
      if (fu == INSN_UID (chain->insn))
	for (k = 0; k < o; k++)
	  if (potential_reload_regs[k] == fr)
	    {
	      for (m = k; m > 0; m--)
		potential_reload_regs[m] = potential_reload_regs[m - 1];
	      potential_reload_regs[0] = fr;
	      fprintf (stderr, "FORCED uid=%d reg=%d\\n", fu, fr);
	      break;
	    }
    }
  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'O'))
    {
      fprintf (stderr, "RO uid=%d", INSN_UID (chain->insn));""")
sub1('global.c', """      expand_preferences ();
""", """      expand_preferences ();
      if (getenv ("TXPREF"))
	{
	  /* Diagnostic experiment only: TXPREF=pseudo:hardreg[,pseudo:hardreg...] adds a
	     register preference before the allocation order is computed.  */
	  char *s = getenv ("TXPREF");
	  while (*s)
	    {
	      int ps = -1, hr = -1;
	      if (sscanf (s, "%d:%d", &ps, &hr) == 2 && ps < max_regno && reg_allocno[ps] >= 0)
		{
		  SET_REGBIT (hard_reg_preferences, reg_allocno[ps], hr);
		  SET_REGBIT (hard_reg_full_preferences, reg_allocno[ps], hr);
		  fprintf (stderr, "PREF pseudo=%d reg=%d\\n", ps, hr);
		}
	      while (*s && *s != ',') s++;
	      if (*s) s++;
	    }
	}
""")
sub1('global.c', """  for (i = max_allocno - 1; i >= 0; i--)
    {
      HARD_REG_SET temp;

      allocno = allocno_order[i];""", """  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'P'))
    for (i = 0; i < max_allocno; i++)
      if (hard_reg_preferences[i] || hard_reg_full_preferences[i] || hard_reg_copy_preferences[i])
	fprintf (stderr, "PF pseudo=%d pref=%lx full=%lx copy=%lx conf=%lx\\n", allocno_reg[i],
		 (unsigned long) hard_reg_preferences[i], (unsigned long) hard_reg_full_preferences[i],
		 (unsigned long) hard_reg_copy_preferences[i], (unsigned long) hard_reg_conflicts[i]);
  for (i = max_allocno - 1; i >= 0; i--)
    {
      HARD_REG_SET temp;

      allocno = allocno_order[i];""")
sub1('global.c', """      qsort (allocno_order, max_allocno, sizeof (int), allocno_compare);
""", """      qsort (allocno_order, max_allocno, sizeof (int), allocno_compare);
      if (getenv ("TXFIRST"))
	{
	  /* Diagnostic experiment only: TXFIRST=pseudo[,pseudo...] moves those allocnos to
	     the front of the allocation order (last listed ends up first).  */
	  char *s = getenv ("TXFIRST");
	  while (*s)
	    {
	      int ps = atoi (s), k, m;
	      if (ps < max_regno && reg_allocno[ps] >= 0)
		for (k = 0; k < max_allocno; k++)
		  if (allocno_order[k] == reg_allocno[ps])
		    {
		      for (m = k; m > 0; m--)
			allocno_order[m] = allocno_order[m - 1];
		      allocno_order[0] = reg_allocno[ps];
		      fprintf (stderr, "FIRST pseudo=%d\\n", ps);
		      break;
		    }
	      while (*s && *s != ',') s++;
	      if (*s) s++;
	    }
	}
""")
sub1('global.c', """  /* Now if one is a hard reg and the other is a global pseudo
     then give the other a preference.  */
""", """  /* Now if one is a hard reg and the other is a global pseudo
     then give the other a preference.  */
  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'Q')
      && ((dest_regno < FIRST_PSEUDO_REGISTER && src_regno >= FIRST_PSEUDO_REGISTER && reg_allocno[src_regno] >= 0)
	  || (src_regno < FIRST_PSEUDO_REGISTER && dest_regno >= FIRST_PSEUDO_REGISTER && reg_allocno[dest_regno] >= 0)))
    fprintf (stderr, "SETPREF dest=%d(%d) src=%d(%d) copy=%d\\n", REGNO (GET_CODE (dest) == SUBREG ? SUBREG_REG (dest) : dest), dest_regno,
	     REGNO (GET_CODE (src) == SUBREG ? SUBREG_REG (src) : src), src_regno, copy);
""")
print('patched2')
