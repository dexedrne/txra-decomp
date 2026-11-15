#!/bin/bash
# dump.sh SRC.c OUTDIR FLAGS... : compile one candidate with RTL dumps on a worker (diagnostic only)
set -e
SRC=$1; OUT=$2; shift 2
mkdir -p "$OUT"
PRE=$(python3 -c "import sys; sys.path[:0]=['tools','recomp']; import llm_match as m; print(m.PRELUDE, end='')")
if grep -q 'typedef unsigned char u8;' "$SRC"; then cp "$SRC" "$OUT/t.c"; else { printf '%s' "$PRE"; cat "$SRC"; } > "$OUT/t.c"; fi
~/opt/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-gcc -E -P -Isrc "$OUT/t.c" -o "$OUT/t.i"
cd "$OUT" && ~/opt/agbcc/agbcc_arm t.i -O2 -mthumb-interwork "$@" -o t.s
