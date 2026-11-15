#!/bin/bash
# mini compile (worker only): mc.sh file.c -> prints the function's thumb asm (official old_agbcc)
ARM=$HOME/opt/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-
CC=${CC:-$HOME/opt/agbcc/old_agbcc}
d=$(dirname $1)
${ARM}gcc -E -P -I$d $1 -o /tmp/sound5_mini_$$.i && $CC /tmp/sound5_mini_$$.i -O2 -mthumb-interwork ${XF:-} -o - 2>${ERR:-/dev/null} | grep -vE '^\s*\.(align|code|globl|type|size|thumb_func|text|word|gcc|file)|^\s*@'
rm -f /tmp/sound5_mini_$$.i
