"""Extra diagnostic prints (finish4 sound lane), applied after trace_patch.py and
trace_patch2.py to the private compiler copy on a worker; then `make old -j1`.
TXWATCH=pseudo[,pseudo..]: at each find_reg of a watched pseudo, print its conflict mask,
pass-0 mask, regs_someone_prefers, preferences and every conflicting allocno with its hard
register so far, refs, live length and priority.  TXDBG letter A: the full allocation order
with priorities and preference masks (after prune_preferences).
Diagnostic only: compare its assembly with the official compiler before trusting a trace."""
def sub1(path, old, new):
    t = open(path).read()
    if t.count(new) == 1 and new != old:
        return
    assert t.count(old) == 1, (path, old[:60], t.count(old))
    open(path, 'w').write(t.replace(old, new))

PRI = """static int
tx_pri (int a)
{
  return (int) (((double) (floor_log2 (allocno_n_refs[a]) * allocno_n_refs[a])
		 / allocno_live_length[a]) * 10000 * allocno_size[a]);
}
static int
tx_watched (int r)
{
  char *s = getenv ("TXWATCH");
  if (! s)
    return 0;
  while (*s)
    {
      if (atoi (s) == r)
	return 1;
      while (*s && *s != ',') s++;
      if (*s) s++;
    }
  return 0;
}

/* Assign a hard register to ALLOCNO; look for one that is the beginning"""
sub1('global.c', """
/* Assign a hard register to ALLOCNO; look for one that is the beginning""", "\n" + PRI)

sub1('global.c', """	     allocno_n_refs[allocno], allocno_live_length[allocno], allocno_calls_crossed[allocno]);
""", """	     allocno_n_refs[allocno], allocno_live_length[allocno], allocno_calls_crossed[allocno]);
  if (tx_watched (allocno_reg[allocno]))
    {
      int k;
      fprintf (stderr, "GW reg=%d best=%d pri=%d used1=%lx nopref=%lx someone=%lx pref=%lx copy=%lx full=%lx sofar=%lx\\n",
	       allocno_reg[allocno], best_reg, tx_pri (allocno), (unsigned long) used1, (unsigned long) used_nopref,
	       (unsigned long) regs_someone_prefers[allocno], (unsigned long) hard_reg_preferences[allocno],
	       (unsigned long) hard_reg_copy_preferences[allocno], (unsigned long) hard_reg_full_preferences[allocno],
	       (unsigned long) regs_used_so_far);
      for (k = 0; k < max_allocno; k++)
	if (k != allocno && (CONFLICTP (allocno, k) || CONFLICTP (k, allocno)))
	  fprintf (stderr, "  GWc reg=%d hard=%d refs=%d len=%d pri=%d pref=%lx full=%lx\\n", allocno_reg[k],
		   reg_renumber[allocno_reg[k]], allocno_n_refs[k], allocno_live_length[k], tx_pri (k),
		   (unsigned long) hard_reg_preferences[k], (unsigned long) hard_reg_full_preferences[k]);
    }
""")

sub1('global.c', """      prune_preferences ();
""", """      prune_preferences ();
      if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'A'))
	for (i = 0; i < max_allocno; i++)
	  {
	    int r = allocno_order[i];
	    fprintf (stderr, "GA ord=%d reg=%d refs=%d len=%d pri=%d pref=%lx copy=%lx full=%lx someone=%lx conf=%lx\\n",
		     (int) i, allocno_reg[r], allocno_n_refs[r], allocno_live_length[r], tx_pri (r),
		     (unsigned long) hard_reg_preferences[r], (unsigned long) hard_reg_copy_preferences[r],
		     (unsigned long) hard_reg_full_preferences[r], (unsigned long) regs_someone_prefers[r],
		     (unsigned long) hard_reg_conflicts[r]);
	  }
""")
sub1('global.c', """static int *allocno_order;
""", """static int *allocno_order;
static int tx_pri (int);
static int tx_watched (int);
int tx_listed (const char *, int);
""")

sub1('global.c', """      qsort (allocno_order, max_allocno, sizeof (int), allocno_compare);
""", """      if (getenv ("TXLEN") || getenv ("TXREFS"))
	{
	  /* Diagnostic experiment only: TXLEN=pseudo:len[,..] / TXREFS=pseudo:refs[,..] set an
	     allocno's live length / reference count before the allocation order is computed.  */
	  int pass2;
	  for (pass2 = 0; pass2 < 2; pass2++)
	    {
	      char *s = getenv (pass2 ? "TXREFS" : "TXLEN");
	      while (s && *s)
		{
		  int ps = -1, v = -1;
		  if (sscanf (s, "%d:%d", &ps, &v) == 2 && ps < max_regno && reg_allocno[ps] >= 0)
		    {
		      if (pass2)
			allocno_n_refs[reg_allocno[ps]] = v;
		      else
			allocno_live_length[reg_allocno[ps]] = v;
		      fprintf (stderr, "%s pseudo=%d v=%d\\n", pass2 ? "REFS" : "LEN", ps, v);
		    }
		  while (*s && *s != ',') s++;
		  if (*s) s++;
		}
	    }
	}
      qsort (allocno_order, max_allocno, sizeof (int), allocno_compare);
""")


sub1('global.c', """            if (reg_renumber[regno] < 0 && N_REG_CLASSES > 1)
              find_reg (order, 0, 0, 0, 0);
""", """            if (getenv ("TXSPILL") && tx_listed ("TXSPILL", regno))
              {
                fprintf (stderr, "SPILLED pseudo=%d\\n", regno);
                continue;
              }
            if (reg_renumber[regno] < 0 && N_REG_CLASSES > 1)
              find_reg (order, 0, 0, 0, 0);
""")
sub1('global.c', """static int
tx_watched (int r)
{""", """int
tx_listed (const char *var, int r)
{
  char *s = getenv (var);
  if (! s)
    return 0;
  while (*s)
    {
      if (atoi (s) == r)
	return 1;
      while (*s && *s != ',') s++;
      if (*s) s++;
    }
  return 0;
}
static int
tx_watched (int r)
{""")
sub1('local-alloc.c', """	reg_qty[i] = -2;
      else
	reg_qty[i] = -1;""", """	reg_qty[i] = -2;
      else
	reg_qty[i] = -1;
      if (getenv ("TXNOLOCAL") && tx_listed ("TXNOLOCAL", i))
	reg_qty[i] = -1;""")
sub1('local-alloc.c', """#include <stdlib.h>
""", """#include <stdlib.h>
extern int tx_listed (const char *, int);
""")

print('patched3')
