#!/bin/bash
# Rebuild the private diagnostic compiler (worker only): fresh local-alloc.c, global.c, reload1.c
# from ~/opt/agbcc/gcc, then the stream lane's trace_patch.py and this lane's trace_patch2.py.
set -e
D=$HOME/txra-sound3-cc
cd $D/gcc
for f in local-alloc.c global.c reload1.c; do cp $HOME/opt/agbcc/gcc/$f .; done
python3 $1/trace_patch.py
python3 $1/trace_patch2.py
nice -n 5 make old -j1 > ../build.log 2>&1 && echo built
