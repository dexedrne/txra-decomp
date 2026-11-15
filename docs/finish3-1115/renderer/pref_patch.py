"""Diagnostic: extend the GF trace line with preference masks (private tracing cc1 only)."""
p = 'global.c'
t = open(p).read()
old = """    fprintf (stderr, "GF reg=%d alt=%d acc=%d retry=%d best=%d refs=%d len=%d calls=%d\\n",
	     allocno_reg[allocno], alt_regs_p, accept_call_clobbered, retrying, best_reg,
	     allocno_n_refs[allocno], allocno_live_length[allocno], allocno_calls_crossed[allocno]);"""
new = """    fprintf (stderr, "GF reg=%d alt=%d acc=%d retry=%d best=%d refs=%d len=%d calls=%d used1=%lx someone=%lx pref=%lx copy=%lx full=%lx usf=%lx\\n",
	     allocno_reg[allocno], alt_regs_p, accept_call_clobbered, retrying, best_reg,
	     allocno_n_refs[allocno], allocno_live_length[allocno], allocno_calls_crossed[allocno],
	     (unsigned long) used1, (unsigned long) regs_someone_prefers[allocno],
	     (unsigned long) hard_reg_preferences[allocno], (unsigned long) hard_reg_copy_preferences[allocno],
	     (unsigned long) hard_reg_full_preferences[allocno], (unsigned long) regs_used_so_far);"""
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, new))
print('pref patched')
