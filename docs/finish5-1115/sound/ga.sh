#!/bin/bash
# Diagnostic (worker only): traced compile of <file.c>; print the align summary and the global
# allocation line (refs, live length, priority, result) of each listed pseudo.
# usage: ga.sh <file.c> <pseudo>...
SRC=$1; shift; T=ga_$(basename $SRC .c)
TXDBG=GA docs/finish5-1115/sound/tr.sh $SRC $T > /dev/null 2>&1
python3 docs/finish5-1115/sound/align.py build/tr/$T/t.s 0 | head -2 | paste -sd ' ' | sed -E "s|build/tr/[^ ]*|$(basename $SRC)|; s/ emit.*DIFF/ DIFF/; s/same.*rows per region://"
for p in "$@"; do
  a=$(grep -E "^GA ord=[0-9]+ reg=$p " build/tr/$T/trace.txt | sed -E 's/ (pref|copy|full|someone|conf)=[0-9a-f]+//g')
  g=$(grep -E "^GF reg=$p " build/tr/$T/trace.txt | tail -1 | sed -E 's/.* best=(-?[0-9]+).*/hard=\1/')
  echo "   $a $g"
done
