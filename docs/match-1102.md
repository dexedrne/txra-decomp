# Hand matching, November 2026

Functions matched by hand against the real compiler (`old_agbcc -O2
-mthumb-interwork`), each verified by a forced full rebuild that passes the
SHA-1 check and committed on its own.

## 11/2

Nine functions, recorded in the commit log of `feat/match-1102`: the link
packet receive (080149FC), the transparent blitter (08008914), the track-edge
clamp (0800CEEC), the car stat setup (0800AF4C), the roadside marker quads
(080095E4), the car-select input switch (0800E498), the menu info panel
(0800F2D0), the garage confirm handler (08010A50) and the garage screen loop
(0800D51C, which absorbed the mapped fragments 0800D570, 0800D630 and
0800D960). The local model loop also learned to skip mapped entries that lie
inside an already matched function.

## 11/3

### Matched (8 functions, 9,024 bytes)

| Address | Bytes | What it is | The change that made it match |
| --- | ---: | --- | --- |
| 08014104 | 134 | blend blit, 120x48 halfwords | Inner loop as `for (x = 0; x < (s32)width; x++)` with both row pointers rebuilt inside it (loop.c reverses it into the count-down copy of `width`), outer loop as a do/while; `height` and the source base get always-zero terms from the volatile read so CSE leaves them without a constant equivalence. |
| 08013E74 | 310 | three rows of wave-offset quads | The second table index is `(k + 4) & 31` and the phase update is `k = (k + 4) & 31`; the old draft's `k += 4` plus a saved copy swapped r4/r5. |
| 0800B4D8 | 1072 | model viewer loop (title-loop family) | The three in-loop DMAs use one `dest` pointer with `dest + 384` and `dest + 464`, and each model-slot block declares its own `slot`. |
| 080098DC | 1116 | race event handler (result timer, rival challenge, checkpoint bits, clock digits) | Every outcome branch writes its own call-and-clear tail instead of sharing one after an if/else: CSE then still knows the timer register is zero and reuses it for `g_030001BC = 0`, and the identical tails are cross-jumped as in the original. The mode-2 state store is a struct field (`g_03001E60[0].field_4c`), and the copy index is `i + n * 5`. |
| 0800CB5C | 912 | per-car drive update (gear table, shifting, movement, slide decay) | The gear table is `s16 [][5][2]` (so `table + 2` is one shared base for the upper-limit column), the gear-change block re-reads `field_52` instead of caching it, `diff >>= 1` is its own statement, and the sine/cosine lookups mask an already masked heading: combine folds the double mask into the index, which puts the AND after the table base as in the ROM. |
| 08007B28 | 2292 | race main (setup, pre-roll, per-mode player placement, frame loop); absorbs the mapped restart entry 08007B40, reached by a far `goto restart` that the ROM encodes as BL | The 6874 row is built as `n * 28 + (u32)base` with the index read first; the frame-wait loop is a `goto` loop (so loop.c does not hoist `&g_03000B50` out of it); the finish checks are four separate `if (result == k) break;` and the function returns `result`; mode 1 stores the constant 1 (CSE reuses the compared register); `g_030001B8++; g_030001B8 &= 31` as two statements. |
| 08008A88 | 2908 | race pause and result menus (three passes over menu state 11 cases each); absorbs the shared epilogue 080095C4 | Every early exit is `goto done` with `result` returned once at the end (the ROM copies r7 to r0 in the epilogue and reaches it with far BL jumps); in the confirm pass cases 8 and 9 are separate identical bodies whose tails cross-jumping merges. |
| 08014AE0 | 280 | serial (multi-player) interrupt | One temporary serves both buffer swaps. Set in two blocks it becomes a global pseudo, leaving three local quantities in the marker block; see the local-alloc note below. |

Totals after these: 173 matched entries, 67,580 bytes including pools, 79.38%
of mapped code (`progress.json`).

### What worked

* **Read the allocator, not just the diff.** `old_agbcc` accepts `-dl -dg`
  (also `-ds -dL -dc`), and the `.greg` dump prints "Registers to be allocated
  in sorted order" with refs and live length, the conflicts and preferences.
  Priority is `floor_log2(refs) * refs / live_length`; refs are weighted by
  loop depth and recounted after combine, live length is counted by flow
  before combine and doubled for registers with a `REG_EQUIV` note.
* **Block scope decides local versus global allocation.** A variable declared
  inside a basic block that crosses calls is given a callee-saved register by
  local-alloc first; the same variable at function scope is a global allocno
  and can lose that register to a preference (0800B4D8's `slot`).
* **Constant equivalences can be avoided without changing the code.** A term
  that only combine proves is zero (`(u8)v >> 8`) keeps CSE from attaching
  `REG_EQUAL`, so the register keeps an undoubled live length (08014104).
* **Local-alloc orders exactly three quantities differently.** In
  `block_alloc` the two- and three-quantity fast paths call `qty_compare(0, 1)`
  and `qty_compare(1, 2)` on quantity *numbers* while exchanging *positions*;
  with three quantities the double exchange can put them back in creation
  order, so the address loaded first gets r0 and the value r1. Two quantities
  or four or more are sorted properly (value first). Changing how many
  block-local pseudos a block has (for example by making a temporary global)
  flips the r0/r1 choice of a store (08014AE0). `gdb` on `old_agbcc` (it has
  debug info) with a breakpoint at `local-alloc.c:1387` prints the final order.
* **Duplicate tails rather than join them.** Code after an if/else join is a
  new extended basic block for CSE; an equivalence learned from a branch (a
  register known to be zero) is lost there but kept when each branch has its
  own copy of the tail (080098DC).
* **Write the natural loop and let loop.c make the counter.** Hand-written
  count-down copies and saved temporaries in old drafts were the cause of the
  remaining swaps in two of the three matches.
* **Loop-invariant hoisting is decided by `threshold * savings * lifetime >=
  insn_count`** (see the `.loop` dump); which addresses get hoisted, and so
  which ones later spill and are rematerialised from the pool, follows from
  how the source expresses them (0800B4D8's `dest` versus three symbols).
  A loop written with `goto` is invisible to loop.c, which is how the race
  main keeps its frame-wait load inside the loop.
* **Mapped entries reached by BL inside a function are far jumps.** Thumb
  `goto`/`return` targets more than 2 KiB away are emitted as BL; 08007B40
  (race restart) and 080095C4 (menu epilogue) are such labels, and matching
  the enclosing function absorbs them (the candidate list then skips them as
  inside a matched function).
* **Post-reload details follow from register choice, not source.** The
  `subs r0, #236` form of -204 in a race-main draft came from post-reload CSE
  reusing a register that still held 32; it disappeared once the global
  allocation matched.

### Closest unmatched, with the blocker

| Address | Bytes | Best | Blocker |
| --- | ---: | --- | --- |
| 080154AC | 748 | 74 instruction lines | Text layout with word wrap; control flow, frame and all low registers now match (y in r3 through caller-saves, glyph and x+8 in r5/r4). Left: the original keeps the draw index in r8 and spills the measuring index, ours does the opposite, because the hoisted y+8 and font address outrank the draw index. Diagnostic only, not installed: pinning the draw index with a GCC register variable (`register s32 start asm("r8")`) brings it to 20 lines (a reload-register swap in the measuring loop and one extra pool word), which confirms the allocation order is the whole remaining problem. |
| 080162F8 | 406 | 177 lines | Rotation/projection, one basic block. The original frame has 15 spill slots (60 bytes) of which five are never touched: pseudos that reload first spilled and then re-allocated (sine and cosine values end in r9, r10, r12). Reproducing it needs the exact set and numbering of the original temporaries. |
| 08016C18 (ARM) | 400 | 43 lines | Same length, frame and loop; the ARM scheduler orders the projection multiplies differently. 36 operand/statement orderings of the rotation tried this round; none went below 43. |

The two drafts are kept in `docs/near-misses/hand-20261103/`.

### What is left

Thumb: 080154AC and 080162F8 above; the HUD drawer 0800421C (4,066 bytes,
continuing through its shared epilogue 080051FE, about 1,800 instructions of
sprite setup in count-down loops); the track streamer 08002854 with its
continuation 08003786 (about 6.4 KB together); the sound mixer 080064A4 with
its fragments 08006712, 08006740, 08006776, 0800735C and 08007368 (one frame,
about 3.8 KB). ARM: 08016C18, 080076F4, 080165BC, 080181C0, 08017F64,
08016DA8. The remaining entries are assembly interfaces (veneers, BIOS calls,
division runtime, interrupt and raster code) listed in `docs/asm-only.md`.

## 11/3, continued

### Matched (3 functions, 1,628 bytes)

| Address | Bytes | What it is | The change that made it match |
| --- | ---: | --- | --- |
| 080154AC | 756 | text layout with word wrap | The draw loop gets its own index `j = start` (`for (j = start; j < end; j++)`, then `start = end`). The short-lived `j` outranks the hoisted y+8 and font address and takes r8; `start` no longer conflicts with anything in the draw loop and shares r8. No register variable needed. The measure loop is a `while (1)` whose first statement is the empty-text exit; `expand_end_loop` rolls that exit to the bottom, which gives the two copies of `lw = w; end = i`. The wrap test reads `if (first <= 249) { end = i; ... } else { i = end; ... }`. |
| 08016C18 | 400 (ARM) | point-grid camera projection | Written like the Thumb sibling 080164D0: `x = point->x; ... x -= F70.x` loads and offsets in place (each load shares its register with the result), `saved_y = y` before the second rotation, `x = xx + F80.x; z += F80.y; y += F80.z`, `z <<= 3; y >>= 1` in place but `x << 3` inside the sx expression. The unused `pad[3]` from the j4 draft still stands for three spill slots the original reload left untouched. |
| 080162F8 | 472 | car model vertex projection | The first rotation reuses the second rotation's names: `xx = x;` (the copy the original keeps in r8), `saved_y = (y * s1 - z * c1) >> 12`, `zz = ...`, `x = (xx * s2 - zz * c2) >> 12`, `z = ...`, then `x -= dx; y = saved_y - dy; z -= dz`. Found by reading the ARM twin 080165BC, whose scheduled code shows the same `mov lr, x` copy. |

Totals: 176 matched entries, 69,208 bytes including pools, 81.29% of mapped
code (`progress.json`).

### What worked

* **Give a loop its own counter.** When a long-lived variable loses a
  callee-saved register to hoisted loop invariants, a fresh loop variable
  copied from it (`for (j = start; ...)`) has a short live range and a high
  priority; the long-lived variable then no longer conflicts with the loop and
  global-alloc puts it in the same register.
* **ARM multiply operand order follows the source.** For agbcc_arm, `a * b`
  prints as `mul rd, b, a` and `a * b + c` as `mla rd, b, a, c`. Reading the
  operand order in the ROM gives the source order of every product (this
  fixed the backface test and the rotations of 080165BC).
* **`if (v > 10) v = 10;` prints as `cmp #10; movge`.** `>= 10` and `> 9`
  print as `cmp #9; movgt`, and the folded `movgt #40; movle lsl #2` pair seen
  in drafts comes from the wrong comparison, not from the index.
* **Twins decode each other.** The ARM model emitter 080165BC and the Thumb
  vertex projection 080162F8 are the same source; the ARM scheduler hides the
  order but not the copies, and the Thumb allocator hides the copies but not
  the order.
* **Re-read the shared quad pointer where a new extended block starts.** In the
  ARM emitter the original reloads `g_030021C4` exactly after joins, so the
  source uses `g_030021C4->` (with a block-local `q` only for the corner
  stores), and the list insert is `g_030021C4++; g_03000670[depth] =
  g_030021C4 - 1;` (the ROM increments the list pointer before storing the
  bucket). The leftover `cmp r3, #0` with no branch is the merged
  `if (!g_03000670[depth]) ... else ...`.
* **Local arrays show up as consecutive frame words read with `ldm`.** The
  four quad depths of 080165BC are `s32 d[4]`, allocated before every spill
  slot; spill slots then follow declaration order.
* **The model table is `void *g_08020E24[][11]`** (faces, info, then nine
  level-of-detail vertex lists); the 2-D index gives the original `[base, off]`
  operand order where a cast-and-index form gives `[off, base]`.
* **Coordinate descent over source "knobs".** A small generator with knobs
  (statement orders, operand orders, inline vs in-place shifts, declaration
  order) scored by an aligned instruction diff found the setup order of
  080165BC (offsets, faces, counts, level of detail, angles, origin) and the
  sum and depth forms, taking it from 755 to 21 differing lines.

### Closest unmatched, with the blocker

| Address | Bytes | Best | Blocker |
| --- | ---: | --- | --- |
| 080165BC (ARM) | 1628 | 21 instruction lines, same length and frame | Model emitter (vertex projection plus quad list). Everything matches except the vertex-loop tail: with `(z << 3)` inline the registers match but the scheduler moves the sy chain before sx; with `z <<= 3` in place the order matches but global-alloc swaps y and z (ip/lr), because the x*factor product no longer takes ip while z is live. Draft in `docs/near-misses/hand-20261103/`. |
| 080076F4 (ARM) | 1076 | about 100 aligned lines, 1080 bytes | Four-voice sample mixer (positions in 18.14 fixed point, two samples per pass into a 176-byte double buffer). Setup, frame slots and the buffer select match; the loop body is scheduled differently (the original keeps the position updates after the first byte store). |
| 08017F64 (ARM) | 604 | 87 aligned lines, 592 bytes | Sprite blend into VRAM. Frame order (width, height, source) and the per-row source base are right; the original keeps four inner-loop induction pointers (two for the source pixel pair, two for the destination) and spills the next-row index. |

### HUD drawer (0800421C), first full draft

The whole routine is now written out (`docs/near-misses/hand-20261103/func_0800421C.c`,
4,180 bytes against the original 4,124). Section shapes follow the ROM. Two
source habits are confirmed:

* OAM attribute 0 is written `(y & 0xFF) | mode`, even where y is a known
  constant. The mask makes the loop body two RTL insns longer before combine
  removes it, which is exactly what keeps loop.c's cost test
  (`threshold * savings * lifetime >= insn_count`, printed in the `.loop`
  dump with `-dL`) from hoisting `0x6000 | y` out of the sprite loops while
  still hoisting the shared 0x200 and zero.
* One counter variable serves every loop (the ROM keeps it in r9 throughout),
  and x/y are function-wide (r4/r10 in every section).

Still open there: the loop.c hoisting of 0x200 in the two-sprite loop of the
name section, the global allocation of the shared temporaries (the original
spills four of them to sp+20..32), and the smoke-slot search loop.

### What is left

ARM: 080165BC, 080076F4 and 08017F64 above; 080181C0 (1,684 bytes, eighteen frame slots,
nested eight-record loops) and 08016DA8 (4,288 bytes). Thumb: the HUD drawer
0800421C (with its shared epilogue 080051FE), the track streamer 08002854 with
08003786, and the sound mixer 080064A4 with its fragments.

## 11/4

### Matched (2 functions, 2,232 bytes)

| Address | Bytes | What it is | The change that made it match |
| --- | ---: | --- | --- |
| 080165BC | 1,628 (ARM) | model vertex projection and quad emission | Keep `out` as a fixed buffer base and write `out[i].depth`, `out[i].sx`, and `out[i].sy` in the vertex loop. Scale both x and z in place. The indexed output changes the induction-variable conflicts enough to retain the original ip/lr allocation and schedule. The input vertex pointer still advances explicitly. |
| 08017F64 | 604 (ARM) | mode-selected sprite blend into the alternate VRAM page | Use a loop-local `u32 value` and a function-wide `u32 temp` for the preserved destination byte. Read the first source as `*(u16 *)(source + column*2 + row*200)` and the second through `((u16 *)(source + column*2))[row*100 + 1]`. For the second pixel, its low-byte merge uses the row pointer `d[column+1]`, while its high-byte merge and opaque store use the column pointer indexed by `row*120+1`. These preserve the original four induction pointers and both address-addition orders. |

Each function has its own commit and passed a forced full rebuild using the
original ARM compiler. The whole ROM remains byte-identical. Totals are
**178 matched entries, 71,440 bytes including pools, 83.917% of 85,132 mapped
code bytes**. The README rounds the code percentage to 83.9%.

### What worked

* **Change the induction variable, not just the final expression.** Thousands
  of tail-expression variants left the emitter's remaining schedule unchanged.
  Indexing its output array solved both scheduling and register allocation
  together, while retaining ordinary C and the existing compiler profile.
* **A destination-byte temporary matters.** In the sprite blend, narrowing
  the source pixel to `u16` produced duplicate signed/unsigned loads. A wide
  pixel and a shared destination-byte temporary kept one source load and
  supplied the original allocation pressure.
* **Row and column pointer forms are not interchangeable to loop.c.** Two
  equivalent destination expressions were needed in different branches of
  the second pixel. Their difference remains visible as operand order in the
  compiled address additions.
* **Separate sample scopes improve the ARM mixer.** Two signed partial sums
  per output sample, each with its own block, retain the correct sample-read
  registers and keep the first position updates after the first byte store.
  This gets the complete mixer to the correct size and frame without pins
  or assembly, although it still does not match.

### Retained work and limits

The current uninstalled drafts and complete comparisons are in
`docs/near-misses/hand-20261104/`:

| Address | Output / target | Remaining work |
| --- | --- | --- |
| 080076F4 | 1,076 / 1,076 bytes; original 60-byte local frame | 40 added/removed instruction rows, 110 differing bytes. Buffer-select move order and the mixing loop's first reloads, final sum register and second-sample schedule remain. Everything outside that region agrees. |
| 080181C0 | 1,640 / 1,684 bytes; 64 / 72-byte local frame | New full typed car-contact draft, including both rotations, six-point contact testing, response updates and pair-cache handling. Cached offsets and reload allocation remain unresolved. It is not independently behavior-verified. |

The row score counts additions plus removals in a unified instruction diff;
it is not directly comparable with older aligned-row or byte scores.
HUD prefix variable-sharing experiments left its frame and loop-hoisting
blockers unresolved, so the 11/3 draft remains the retained one. The streamer, enclosing Thumb
sound routine and ARM track-face renderer were read in pieces; their initial
source structure, strides, internal-entry boundaries and next recovery pieces
are recorded in `hand-20261104/large-bodies.md`. None is counted as a match.

Progress keeps the existing mapped-byte denominator. `tools/progress.py`
reports zero mapped code when this branch's configuration lacks its optional
`mapping` array, so the two match additions were computed from `rom.cfg`
while preserving the established inventory totals.

Validation: `make check` ran 172 tests (171 passed, 1 skipped), and the final
ROM passed its SHA-1 check. Review pictures and two inspected 8-second muted
30 fps clips are in `txra-review/match-1104/`; both clips are below
1 MB. See `docs/MATCH1104-SHIP.md`. No OWNER-NOTES.md was present.

## 11/4, continued

### Matched (1 function, 1,076 bytes)

| Address | Bytes | What it is | The change that made it match |
| --- | ---: | --- | --- |
| 080076F4 | 1,076 (ARM) | four-voice sample mixer | A function-wide sum serves both output samples; each sample keeps its own short-lived partial sum. This gives the original r1 final sum without moving the first position updates ahead of the first byte store. `buf1 = buf * 176; if (buf == i) buf1 = i;` gives the original conditional-move order. The first sample's position updates are 1, 2, 0, 3; the final updates are 0, 1, 2, 3. |

Commit `8324b28` installs only this complete routine and its generated assembly
replacement. It uses the existing `arm` profile, with no register pins,
assembly insertion or output-byte changes. The complete 1,076-byte comparison
includes the literal pools, and installation passed a forced full rebuild and
the ROM SHA-1 check.

Totals are **179 matched entries, 72,516 bytes including pools, 85.181% of
85,132 mapped code bytes**. The mapped inventory denominator is unchanged.

### Mutation-search queue

Commit `a89f743` adds `tools/permute_queue.py` with five regression tests.
It reads the current `rom.cfg` match list, removes exact matches and internal
entries covered by installed bodies, and orders remaining candidates by their
lowest supplied permuter score. Untried candidates follow, smallest first.
All of 080165BC, 08017F64, 08017E68 and 08018E18 were already installed at the
start of this continuation; 080076F4 is now excluded too.

The requested `feat/permuter-1103` branch, `tools/permute.py` and night runner
were absent from the supplied checkout, local origin and available local
bundles. The branch was requested during the job, and origin was rechecked.
There was no mergeable ref, so no substitute branch or merge commit was
invented. The queue helper is committed and tested, but live schedule integration
and the requested `--no-ff` merge remain outstanding. See
[permuter-queue.md](permuter-queue.md) for the runner interface.

### Further recovery and validation

The uninstalled car-contact draft, a HUD frame experiment and the enclosing
Thumb sound prefix are retained in `docs/near-misses/hand-20261104b/`.
Their README distinguishes measured compiler output from incomplete source
recovery. None contributes to the match totals. The track streamer and ARM
track-face renderer still need their complete enclosing bodies.

`make check` ran **177 tests: 176 passed, one skipped**. The complete rebuilt ROM
passed its SHA-1 check. Four inspected review pictures and one inspected,
muted 8-second 30 fps WebM are in `txra-review/match-1104b/`, with
notes and captions. The clip is compiler evidence, not game footage.
No `OWNER-NOTES.md` was present. See `docs/MATCH1104B-SHIP.md`.
