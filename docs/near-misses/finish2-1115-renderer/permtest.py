import sys, random, difflib
sys.path.insert(0, 'docs/near-misses/finish2-1115-renderer')
import perm
lines = open(sys.argv[1]).read().split('\n')
print('units', len(perm.units(lines)), 'runs', len(perm.siblings(lines)))
rng = random.Random(1)
for f in (perm.m_move,):
    for k in range(3):
        new = f(lines, rng)
        print('=====', f.__name__, k, 'None' if new is None else '')
        if new:
            for d in list(difflib.unified_diff(lines, new, lineterm='', n=0))[2:14]:
                print(d)
