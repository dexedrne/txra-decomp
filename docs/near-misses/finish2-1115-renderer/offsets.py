import re, sys
prev = None
for n, l in enumerate(open(sys.argv[1]), 1):
    m = re.match(r'^..([0-9A-F]{8}) .*\| ([0-9A-F]{8}) ', l)
    if not m:
        continue
    off = int(m.group(2), 16) - int(m.group(1), 16)
    if off != prev:
        print(n, m.group(1), off)
        prev = off
