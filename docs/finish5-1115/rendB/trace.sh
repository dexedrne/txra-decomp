#!/bin/bash
# trace.sh SRC.c OUTDIR [extra flags] : compile with official agbcc_arm and the private tracing cc1
# (finish3 + finish4 trace patches, built in ~/rendB-cc), require identical assembly, keep the trace
# (TXDBG, default GRLFI) and -dl/-dg/-dS dumps in OUTDIR. Worker only.
set -e
SRC=$1; OUT=$2; shift 2
mkdir -p "$OUT"
PRE=$(python3 -c "import sys; sys.path[:0]=['tools','recomp']; import llm_match as m; print(m.PRELUDE, end='')")
if grep -q 'typedef unsigned char u8;' "$SRC"; then cp "$SRC" "$OUT/t.c"; else { printf '%s' "$PRE"; cat "$SRC"; } > "$OUT/t.c"; fi
~/opt/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-gcc -E -P -Isrc "$OUT/t.c" -o "$OUT/t.i"
cd "$OUT"
~/opt/agbcc/agbcc_arm t.i -O2 -mthumb-interwork "$@" -o official.s
TXDBG=${TXDBG:-GRLFI} ${TXCC:-$HOME/rendB-cc/gcc_arm/cc1} -quiet t.i -O2 -mthumb-interwork -dl -dg -dS -dL "$@" -o trace.s 2> trace.txt
cmp -s official.s trace.s && echo "trace asm identical" || echo "TRACE ASM DIFFERS"
