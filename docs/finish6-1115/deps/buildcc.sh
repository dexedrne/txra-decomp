#!/bin/bash
# buildcc.sh DOCS : build the private diagnostic ARM cc1 in ~/txra-deps-cc (worker only, never for matching).
# Copies ~/opt/agbcc/{gcc_arm,libiberty,include}, applies finish3/4 trace patches, finish5 rendA hooks and
# this lane's sched1 trace patch (if present), then make clean; make cc1.
set -e
P=${1:?docs dir}
D=$HOME/txra-deps-cc
rm -rf $D; mkdir -p $D
cp -a $HOME/opt/agbcc/gcc_arm $HOME/opt/agbcc/libiberty $HOME/opt/agbcc/include $D/
cd $D/gcc_arm
sed -i "s|^objdir = .*|objdir = $D/gcc_arm|" Makefile
for p in finish3-1115/renderer/trace_patch_arm.py finish3-1115/renderer/pref_patch.py finish3-1115/renderer/lq_patch.py \
         finish3-1115/renderer/force_patch.py finish4-1115/renderer/ff_patch.py finish4-1115/renderer/li_patch.py \
         finish5-1115/rendA/order_patch.py finish5-1115/rendA/nonlocal_patch.py finish5-1115/rendA/lforce_patch.py; do
  python3 $P/$p
done
if [ -f $P/finish6-1115/deps/s1trace_patch.py ]; then python3 $P/finish6-1115/deps/s1trace_patch.py; fi
make clean > ../clean.log 2>&1 || true
nice -n 5 make cc1 > ../build.log 2>&1 && echo built || { tail -20 ../build.log; exit 1; }
