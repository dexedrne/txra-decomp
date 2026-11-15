"""Diagnostic what-if hook for the private tracing cc1 (never used for matching):
TXBLOCKREG="block:hardreg" makes local-alloc's find_free_reg refuse that hard register in that
basic block (as if it were live there). Without the variable the compiler is unchanged."""
p = 'local-alloc.c'
t = open(p).read()
old = """static void
block_alloc (b)
     int b;
{"""
new = """static int tx_cur_block = -1;
static void
block_alloc (b)
     int b;
{
  tx_cur_block = b;"""
assert t.count(old) == 1
t = t.replace(old, new)
old2 = "  COPY_HARD_REG_SET (first_used, used);\n"
new2 = """  COPY_HARD_REG_SET (first_used, used);
  if (getenv ("TXBLOCKREG"))
    {
      int bb = -1, hr = -1;
      if (sscanf (getenv ("TXBLOCKREG"), "%d:%d", &bb, &hr) == 2 && bb == tx_cur_block)
	SET_HARD_REG_BIT (first_used, hr);
    }
"""
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, 'w').write(t)
print('blockreg patched')
