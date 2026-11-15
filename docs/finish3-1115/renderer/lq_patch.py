"""Diagnostic: local-alloc qty trace (TXDBG contains L) for the private tracing cc1 (from the stream lane)."""
p = 'local-alloc.c'
t = open(p).read()
old = """  for (q = 0; q < next_qty; q++)
    if (qty_phys_reg[q] >= 0)
      {
	for (i = qty_first_reg[q]; i >= 0; i = reg_next_in_qty[i])
	  reg_renumber[i] = qty_phys_reg[q] + reg_offset[i];
      }
}
"""
new = """  for (q = 0; q < next_qty; q++)
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
"""
assert t.count(old) == 1, t.count(old)
t = t.replace(old, new)
if '#include <stdlib.h>' not in t[:300]:
    t = '#include <stdlib.h>\n#include <string.h>\n' + t
open(p, 'w').write(t)
print('lq patched')
