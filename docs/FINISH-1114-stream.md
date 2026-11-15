# Stream owner pass, 14 November

Target: the road stream owner **08002854..0800418C** (6,456 bytes with pools), which also contains the **08003786** registry entry.

No exact match was installed. The new full-owner C is **23 differing bytes** from the original. The previous best was 6,106. All 23 bytes are in one 54-byte register-allocation span (0x08002952..0x08002986). The output length (6,456) and frame (268) now match the original exactly. The exact prefix is 254 bytes and the exact suffix is 6,148 bytes.

| Measure | 1112c retained | This pass |
| --- | ---: | ---: |
| Emitted / target bytes | 6,120 / 6,456 | **6,456 / 6,456** |
| Local frame / original | 156 / 268 | **268 / 268** |
| Instruction edit distance | 2,661 | **20** |
| Differing bytes | 6,106 | **23** |

Source: [func_08002854.c](near-misses/finish-1114-stream/func_08002854.c). The full sanitized diff is [candidate.diff.txt](near-misses/finish-1114-stream/candidate.diff.txt) and the measurement is in [candidate.json](near-misses/finish-1114-stream/candidate.json). Profile: `old`, `-O2 -mthumb-interwork`, checker end 0800418C. The C is plain structured code, with no padding, inline assembly, fixed registers or widened checker.

## What changed in the C

The rewrite follows the original statement order, read from `asm/program.s`.

- **Faces are written as `fb[faces].field`**, with a running face count. The compiler folds the face address where the count is a known constant. The scenery loop strength-reduces it into a pointer. This one change restores most of the original 268-byte frame, because the original spills the per-face address temporaries.
- **Points use a cursor.** Each point is written `p->active = 1; p++`. Three separate counters then build the indices: `count` for the current row, `fcount` for the following row and `acount` for the row after.
- **The window setup and the 24-entry clear loop are each written out in both direction branches.** The original duplicates both, so the source does too.
- **Two dead reads of `ROWS[next2]` are kept, as in the original.** One sits at the top: GCSE keeps its address computation alive after the load itself is deleted. The other is a dead `acount += 4` inside the right-bank branch. It keeps the original's leftover load, which only goes away after register allocation.
- **`left_start` is a variable set once to 0.** This reproduces the original `adds r0, #0`, which comes from reload substituting a constant equivalence.
- **Constant-address forms are used for the face and point arrays (0x02033B70, 0x02014000).** They make reload load the constant itself, which matches the original `ldr r2,=…; adds r2,r0,r2`. The pool bytes are identical either way.
- The variable declaration order fixes the order of the GCSE spill slots at sp+244..260 to match the original.

## Behaviour check

`tools/check_stream_original1112c.py` passes **480/480** synthetic states and compares **11,998** ordered helper calls against the original instructions (receipt: [original-checks.json](near-misses/finish-1114-stream/original-checks.json)). This is bounded synthetic evidence, not a proof for arbitrary states and not gameplay evidence. The worker venv lacked `unicorn`, so it was installed into a private, temporary venv on worker D, which was removed afterwards.

## What still blocks an exact match

Every remaining difference comes from one cause. In the original, register r1 is unavailable from the `ring+2` computation through the `first` reload. As a result:

- the `(ring+2)&31` temporary lands in r4 instead of r1;
- the `first` reload uses r3 instead of r1;
- the point-base constant uses r4 instead of r3;
- the four GCSE spill stores in the first clear branch rotate to r5,r0,r1,r2.

Ruled out:

- in-place `ring` updates (ten forms), which raise `ring`'s global-allocation priority and reshuffle r8–r10 across the whole owner;
- duplicating the bases block in each branch, with function-scope or block-scope `ring`;
- temporaries for `first` and the point base;
- 24 random declaration orders (12 on the base candidate, 12 on an in-place variant);
- constant versus symbol bases (this one fixes the face base only).

The `-dl/-dg/-dN` RTL dumps show this comes from local-alloc order and reload's rotating choice of reload register. The original's RTL must keep some value live in r1 over insns ~209..225, and the C that would do that is not yet known.

## Boundaries and map accounting

08003786 is not a separate function. It has no prologue, reuses the 268-byte frame, and is entered only by the `bl` far jump at 0800416A, which is the second pass of a two-column scenery loop. The C above covers it as part of the owner. The public registry was **not** edited this round, for two reasons:

- The native recompiler and the runtime tests (237 functions / 268 load-run entries) treat 08003786 as an entry.
- No installation needed the change: a future install covers 08003786 through the enclosing owner, the same way other covered labels are handled.

For "48 entries left": two of those registry entries, 08002854 and 08003786, are one function. This pass did not look at whether the registry or the unknown bytes hold more code.

Reproduce:

- `tools/measure_candidate.py docs/near-misses/finish-1114-stream/func_08002854.c 08002854 0800418C old <out>`
- `tools/check_stream_original1112c.py <same source> <receipt>`
- `shape_compare.py` in the receipt folder compares `asm/program.s` with compiler output as text. It reads no ROM bytes.
- `rtl_dump.py` in the receipt folder writes the `-dl/-dg/-dN` RTL dumps used for the allocation analysis. Run it on a worker.

Work stayed on `work/finish-stream`, with no push or merge. All builds, compiles and checks ran on worker D.

matches installed: none (08002854 owner not exact; 189 replacements unchanged)
near-misses improved: 08002854 (with internal 08003786): 6106 -> 23 differing bytes (instruction distance 2661 -> 20; size and 268-byte frame now exact)
what blocks the rest: one block's local-alloc/reload register choice (original keeps r1 occupied over ring+2..first reload), not yet reproduced from C.
