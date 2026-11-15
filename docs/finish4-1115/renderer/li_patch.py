"""Diagnostic: print local-alloc insn numbers (TXDBG contains I). Private tracing cc1 only."""
p = 'local-alloc.c'
t = open(p).read()
old = """	  this_insn_number = insn_number;
	  this_insn = insn;
"""
new = """	  this_insn_number = insn_number;
	  this_insn = insn;
	  if (getenv ("TXDBG") && strchr (getenv ("TXDBG"), 'I'))
	    fprintf (stderr, "LI b=%d uid=%d num=%d\\n", b, INSN_UID (insn), insn_number);
"""
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, new))
print('li patched')
