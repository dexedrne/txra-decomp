#!/bin/bash
# Quick variant probe (worker only): official old_agbcc, print frame and the 0x67 block.
# usage: v.sh <file.c>...
ARM=$HOME/opt/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-
CC=$HOME/opt/agbcc/old_agbcc
mkdir -p build/v
for f in "$@"; do
  b=build/v/$(basename $f .c)
  ${ARM}gcc -E -P -Isrc $f -o $b.i && $CC $b.i -O2 -mthumb-interwork -o $b.s || { echo "$f: compile failed"; continue; }
  echo "== $f $(grep -o 'add\s*sp, sp, #-[0-9]*' $b.s | head -1)"
  awk '/cmp\tr[0-7], #103/{p=1} p{print; n++} n>=18{exit}' $b.s | tr '\t' ' ' | paste -sd ';' | cut -c1-600
done
