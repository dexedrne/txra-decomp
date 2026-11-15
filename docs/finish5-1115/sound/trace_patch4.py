"""Diagnostic what-if (finish5 sound lane), applied after trace_patch.py..trace_patch3.py to the
private compiler copy on a worker; then `make old -j1`.
TXNOMOVE=uid[,uid..]: loop.c move_movables never moves the movable whose insn has one of these
uids (as if it were not desirable).  Prints "NOMOVE uid=" when it applies.
Diagnostic only: compare its assembly with the official compiler before trusting a trace."""
def sub1(path, old, new):
    t = open(path).read()
    if t.count(new) == 1 and new != old:
        return
    assert t.count(old) == 1, (path, old[:60], t.count(old))
    open(path, 'w').write(t.replace(old, new))

sub1('loop.c', """	  if (already_moved[regno]
	      || flag_move_all_movables
	      || (threshold * savings * m->lifetime) >=""", """	  if (getenv ("TXNOMOVE") && tx_listed ("TXNOMOVE", INSN_UID (m->insn)))
	    fprintf (stderr, "NOMOVE uid=%d\\n", INSN_UID (m->insn));
	  else if (already_moved[regno]
	      || flag_move_all_movables
	      || (threshold * savings * m->lifetime) >=""")
t = open('loop.c').read()
if 'extern int tx_listed' not in t:
    t = t.replace('#include "config.h"\n', '#include "config.h"\n#include <stdlib.h>\nextern int tx_listed (const char *, int);\n', 1)
    open('loop.c', 'w').write(t)
print('patched4')
