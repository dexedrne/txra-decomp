import itertools, re, sys, os
base = open(sys.argv[1]).read(); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
NAT = "(((depth[0] + depth[1]) + depth[2]) + depth[3])"
SUM = "depth[0] + depth[1] + depth[2] + depth[3]"
lines = ["z = %s >> 7; z += 32;" % NAT, "gCurPacket->tex = face->tex;", "gCurPacket->mode = 0;",
         "if (z < 0) z = 0;", "z = z > 255 ? 255 : z;"]
pat = re.compile(r'( *)' + r'\n\1'.join(re.escape(l) for l in lines))
ms = list(pat.finditer(base))
assert len(ms) == 2, len(ms)
Z = {'b': ["z = (%s) >> 7;" % SUM, "z += 32;"], 'a': ["z = ((%s) >> 7) + 32;" % SUM]}
C2 = {'t': "z = z > 255 ? 255 : z;", 'f': "if (z > 255) z = 255;"}
T, M, C1 = lines[1], lines[2], lines[3]
n = 0
def emit(tag, items, both):
    global n
    s = base
    for which, m in reversed(list(enumerate(ms))):
        if which == 0 or both:
            ind = m.group(1)
            s = s[:m.start()] + ind + ('\n' + ind).join(items) + s[m.end():]
    open('%s/%s.c' % (out, tag), 'w').write(s); n += 1
for zk, zs in Z.items():
    for c2k, c2 in C2.items():
        rest = [T, M, C1, c2]
        for perm in itertools.permutations(range(4)):
            if perm.index(2) > perm.index(3): continue
            items = zs + [rest[k] for k in perm]
            tag = 'r_%s%s_%s' % (zk, c2k, ''.join(map(str, perm)))
            emit(tag + '_p', items, False)
            emit(tag + '_b', items, True)
print(n)
