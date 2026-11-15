#!/bin/bash
# trace.sh SRC.c OUTDIR : compile with the official agbcc_arm and the private tracing cc1
# (~/txra-rendA-cc), require identical assembly, keep TXDBG traces and -dS/-dl/-dg dumps. Worker only.
set -e
SRC=$1; OUT=$2; shift 2
mkdir -p "$OUT"
cp "$SRC" "$OUT/t.c"
~/opt/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-gcc -E -P -Isrc "$OUT/t.c" -o "$OUT/t.i"
cd "$OUT"
~/opt/agbcc/agbcc_arm t.i -O2 -mthumb-interwork "$@" -o official.s
TXDBG=${TXDBG:-GRLFI} ~/txra-rendA-cc/gcc_arm/cc1 -quiet t.i -O2 -mthumb-interwork -dS -dl -dg -dL -dr -dc "$@" -o trace.s 2> trace.txt
cmp -s official.s trace.s && echo "trace asm identical" || echo "TRACE ASM DIFFERS"
