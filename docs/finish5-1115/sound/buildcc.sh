#!/bin/bash
# Rebuild the private diagnostic compiler (worker only) in ~/txra-sound5-cc: fresh local-alloc.c, loop.c,
# global.c, reload1.c from ~/opt/agbcc/gcc, then the stream lane's trace_patch.py, the finish3
# sound lane's trace_patch2.py, the finish4 trace_patch3.py and this lane's trace_patch4.py; then `make old -j1`.
set -e
D=$HOME/txra-sound5-cc
[ -d $D ] || { cp -a $HOME/opt/agbcc $D; make -C $D/gcc clean > /dev/null; }
cd $D/gcc
for f in local-alloc.c global.c reload1.c loop.c; do cp $HOME/opt/agbcc/gcc/$f .; done
python3 $1/trace_patch.py
python3 $1/trace_patch2.py
if [ -f $1/trace_patch3.py ]; then python3 $1/trace_patch3.py; fi
if [ -f $1/trace_patch4.py ]; then python3 $1/trace_patch4.py; fi
nice -n 5 make old -j1 > ../build.log 2>&1 && echo built
