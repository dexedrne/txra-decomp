#!/bin/bash
# Diagnostic trace of one C source with the private traced old_agbcc (worker only).
# usage: tr.sh <file.c> <tag> [extra -d flags]   -> build/tr/<tag>.{s,trace,*dumps}
# Compares the traced compiler's assembly with the official one first.
set -e
SRC=$1; TAG=$2; DF=${3:-}
ARM=$HOME/opt/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-
CC=$HOME/opt/agbcc/old_agbcc
TCC=$HOME/txra-sound5-cc/gcc/old_agbcc
mkdir -p build/tr/$TAG
cd build/tr/$TAG
${ARM}gcc -E -P -I../../../src ../../../$SRC -o t.i
$CC t.i -O2 -mthumb-interwork -o off.s
TXDBG=${TXDBG:-LGR} $TCC t.i -O2 -mthumb-interwork $DF -o t.s 2> trace.txt
if cmp -s off.s t.s; then echo "traced==official"; else echo "TRACED DIFFERS"; fi
