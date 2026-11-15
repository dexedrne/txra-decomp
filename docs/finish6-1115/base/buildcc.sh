#!/bin/bash
# buildcc.sh : private diagnostic copy of agbcc_arm's cc1 at ~/base-cc (worker only, never for matching).
# Applies finish3 (trace_patch_arm, pref_patch, lq_patch, force_patch), finish4 (ff_patch, li_patch)
# and finish5 rendA (order_patch, nonlocal_patch, lforce_patch) plus this round's sched1 tracer, then make cc1.
set -e
R=$PWD
rm -rf ~/base-cc && mkdir -p ~/base-cc
cp -a ~/opt/agbcc/gcc_arm ~/opt/agbcc/libiberty ~/opt/agbcc/include ~/base-cc/
cd ~/base-cc/gcc_arm
sed -i "s#^objdir = .*#objdir = $HOME/base-cc/gcc_arm#" Makefile
for p in docs/finish3-1115/renderer/trace_patch_arm.py docs/finish3-1115/renderer/pref_patch.py \
         docs/finish3-1115/renderer/lq_patch.py docs/finish3-1115/renderer/force_patch.py \
         docs/finish4-1115/renderer/ff_patch.py docs/finish4-1115/renderer/li_patch.py \
         docs/finish5-1115/rendA/order_patch.py docs/finish5-1115/rendA/nonlocal_patch.py \
         docs/finish5-1115/rendA/lforce_patch.py ${EXTRA_PATCHES:-}; do
  python3 "$R/$p"
done
make cc1 > build.log 2>&1 || { tail -30 build.log; exit 1; }
ls -la cc1
