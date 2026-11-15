# 080181C0 rotate loop: what the two loop passes do

Evidence for the retained structural source `func_080181C0.c` in this folder.
The movable reports and register numbers come from compiler debug dumps
(`-dL -dl -dg -dG`) of **our own C**, compiled with the unchanged `arm` profile on
worker A. The original frame layout comes from the disassembly already in
`asm/program.s`. No ROM bytes are involved.

## Original frame (from asm/program.s)

Locals run from fp-0x2c to fp-0x70: 18 words, 72 bytes.

| Slot | Value | Slot | Value |
| --- | --- | --- | --- |
| -0x2c | j | -0x50 | first sine coefficient s1 |
| -0x30 | i | -0x54 | j*100 (record offset) |
| -0x34 | inverse heading | -0x58 | i*5 |
| -0x38 | width | -0x5c | zpos (record j, word 3) |
| -0x3c | height | -0x60 | j+1 |
| -0x40 | pair mask | -0x64 | i+1 |
| -0x44 | result | -0x68 | j*4 |
| -0x48 | known | -0x6c | i*4 |
| -0x4c | i*16 | -0x70 | j*16 |

Inside the six-point loop the original **reloads** record j word 1, record i
words 1 and 3, and the heading sine on every iteration. Only i*5 is hoisted:
i*25 and i*100 are rebuilt from the spilled i*5 on each iteration.

## Why earlier candidates differ

Earlier candidates, including the best one (1112b contact-final: 919 differing
bytes, frame 68), write through a block-local `TxraTriple *p = g_030057A0`.
Alias analysis then knows the stores hit the probe array, so the loop pass hoists
the record and sine loads. Their frames hold hoisted load values instead of
j*100 and i*5.

The retained source declares `p` once at function scope and points it at the
probe array twice, once in each six-element loop. A second set from a non-self
source clears the pointer's alias base (`record_set` in the compiler's
alias.c), so the stores may alias every word load. The record and sine loads
then stay inside the loop, which is what the original does.

## Movable decisions, retained source, unchanged profile

First loop pass (48 insns, threshold 28, minus 3 for each move):

```
455 r204 field-04 symbol copy       moved
459-467 r206-r210 j*4 copy .. j*100 moved  (CSE2 later turns r210 into a copy of the field_00-test offset)
473 r213 i*4 copy                    moved
475 r214 i*5                         moved
477 r215 i*5<<2                      not desirable   <- matches the original
479/481 r216 i*25, r217 i*100        not safe        <- matches the original
498 record-base symbol copy, 512 record+12 address, 521 sine symbol, 525 angle*4: not desirable / not safe
```

Second loop pass (`-frerun-loop-opt`, part of -O2), 38 insns, threshold reset to 28:

```
477 r215 i*5<<2   moved
479 r216 i*25     moved
481 r217 i*100    moved
525 r237 angle*4  moved
```

The first pass alone reproduces the original's hoisting exactly. The second pass
then moves the i-index chain out of the loop, so i*100 lives in a register and
the i*5 slot disappears.

## Diagnostic only: the second pass disabled

With `-fno-rerun-loop-opt` added (`tools/diag_rerun1114.py`), the same source
gives the original's **72-byte frame**, 1676/1684 bytes, 231 edits and 981
differing bytes. The inner loop then has the original's shape: s1 at fp-0x50,
reloaded twice per iteration; j*100 reloaded from a slot; i*25/i*100 rebuilt
from i*5; the record and sine loads inside the loop.

This flag is **not admissible**. With it added, the installed 080165BC, a
neighbour in the same ARM block, emits too many bytes ("output crosses next
candidate boundary"). 08016C18, 08017E68, 08017F64, 08018854 and 080076F4 stay
exact either way. Unless the ARM block was built as separate units with
different flags, the original kept the second pass. Its source therefore has some
feature that stops that pass from moving the i chain. That feature is not yet
identified.

Desirability cannot explain it. In the second pass, i*5<<2 has savings 2 and
lifetime 2, so 28*2*2 = 112 is at least the loop's ~38 insns at full threshold.
The insn must be unsafe, not a movable at all, or the loop must not be rescanned.
Excluded so far: loop shape (`do`/`while`/`for` up or down, index vs pointer),
output temporaries, block-scoped coefficients, the field-04 symbol form.

## Frame order reached

| | Order of spilled values |
| --- | --- |
| original | j i angle width height mask result known **i\*16 s1** j\*100 i\*5 zpos j+1 i+1 j\*4 i\*4 j\*16 |
| retained, profile | j i angle width height mask result known **i\*16 s1** zpos j\*100 j+1 i+1 j\*4 i\*4 j\*16 (68 bytes) |
| 1112b best, profile | j i angle width height mask result known zpos i\*16 A[j] B[i] j+1 i+1 j\*4 i\*4 j\*16 (68 bytes) |
| retained, diagnostic | j i angle width height mask result known i\*16 s1 zpos j\*100 j+1 i+1 j\*4 i\*4 j\*16 angle\*4 (72 bytes) |

Still unexplained: zpos sits after j*100 and i*5 in the original. A
variable declared before the loop gets a lower register number than the in-loop
index chain, so the original's zpos is probably not a plain early declaration.
