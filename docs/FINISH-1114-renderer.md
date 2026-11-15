# Renderer finish pass, 14 November (label: renderer)

Target: **08016DA8** (ARM renderer, 4,288 bytes, owner end 08017E68). No exact match was
installed. The registry, `src/` and every installed replacement are unchanged. A forced
rebuild on worker C (`make -j8`) still ends with `build/txra.gba: OK`.

## Result

This round dropped the 11/7–11/12 address-arithmetic source (`MEM32(POINTS + offset)`). It
rewrote the owner from the assembly in ordinary C:

- constant-address arrays for the track points (`0x02014000`, 28-byte records) and faces
  (`0x02033B70`, rows of 24 × 56 bytes);
- one points-base local, which the cartridge keeps in `sb` for the whole function;
- extern IWRAM globals;
- plain `if`/`for` control flow.

| Candidate | Differing bytes | Instruction distance | Emitted / target | Frame / target | Shape rows / register rows |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1112c retained (`decomp-1112c/func_08016DA8.c`) | 3,250 | 897 | 4,268 / 4,288 | 108 / 96 | 410 / 626 |
| **11/14 natural** (`finish-1114-renderer/func_08016DA8.c`) | **2,446** | **622** | **4,288 / 4,288** | **96 / 96** | 95 / 552 |
| 11/14 structural variant (`func_08016DA8_structural.c`) | 3,645 | 658 | 4,296 / 4,288 | 96 / 96 | 77 / 602 |

How each column is measured:

- **Differing bytes and instruction distance** come from the unchanged `tools/measure_candidate.py`
  run (`arm` profile, strict end 08017E68).
- **Shape rows and register rows** come from `sbs.py --score`. It aligns opcodes with register
  names and PC offsets ignored. A *shape* row is a missing, extra or different instruction. A
  *register* row is the same instruction with different registers.

The natural candidate now has the cartridge's exact length and frame. The structural variant
gets more instruction shapes right but emits 8 extra bytes. Its differing-byte count is
positional, so those 8 bytes inflate it.

Both candidates pass the same **199 synthetic differential fixtures** as the 11/7 checker:
48×3 near/far/mixed cases, boundary depths, ring wrap, direct insertion and two-face rows. All
**1,053** original instruction addresses are reached. They run through `check32.py`, which
compiles the unchanged candidate for i386 so that the 32-bit packet and bucket pointers keep
their layout. It links the candidate freestanding, maps synthetic EWRAM, IWRAM and the
reciprocal table at their GBA addresses, and compares against the textual ARM executor of
`arm-16da8-1107/check_semantics.py`.

Two negative controls are rejected, with 49 and 16 failing fixtures. One stores the y clamp as
-173; the other caps the bucket at 254. No ROM bytes are used. These are synthetic states, not
gameplay.

Receipts are in `docs/near-misses/finish-1114-renderer/`:

- both sources;
- the measure JSON for each candidate, with gzipped full diffs;
- `checks.json`, which also records the negative controls;
- `check32.py` and `harness32.c`;
- `sbs.py`, the side-by-side aligner;
- `regs.py`, which reports pseudo-register priority from `-dl -dg` dumps.

The worker C `agbcc_arm` binary hash (`3426878…`) differs from the 1112c host's build (`26d884f…`).
It still reproduces the 1112c baseline exactly: 3,250 bytes, distance 897.

## Source facts established (each confirmed by compile + measure)

- **Points base.** `Point *pts = (Point *)0x02014000` must be a function-scope local. That
  reproduces `mov sb,#0x2000000 … add sb,#0x14000` in the prologue. As a macro it is re-hoisted
  per loop and spilled.
- **Path order.** The near path is the `if` arm and the direct path the `else`, using
  `depth[k] <= 767 || …`.
- **Camera and offset reads.** These are global reads inside the projection loop, not locals.
  The cartridge's camera.z/offset.z pre-loads are made by `loop.c`. It hoists the component
  accessed last and gives it the pointer induction variable. The cartridge pattern needs the
  x, y, z delta order with the screen sums written before the depth, as in the structural
  variant.
- **Visibility.** `x >= 0 && x < 120 && y >= 0 && y < 160` on `s16` fields. Fold merges only
  the leading x pair into the unsigned compare, exactly as the cartridge does.
- **Clamps.** X clamps are `<= -67 → -66` and `> 186 → 186`. Y clamps are `< -175 → -174` and
  `> 335 → 334`. The expand order is `y0--, x0--, y1--, x1++`.
- **Bucket.** `z = z > 255 ? 255 : z` (MIN) gives `cmp #255; movge`. An `if` gives
  `cmp #254; movgt`.
- **Insertion.** Each branch is `p = gCurPacket; p->next = …; gCurPacket = p + 1;
  gBuckets[z] = p;`. With that, cross-jumping leaves the shared bucket store and the length
  becomes exact.
- **Declaration order.** `part` is declared before `a…d`. This puts `part` at fp-0x40 and
  b/c/d at fp-0x44…-0x4c.

## What blocks the rest

1. **Register allocation swap (≈100 instructions).** The points base and the scratch pointer
   (shared with `a`) have their `sb`/`sl` roles exactly swapped. There are 44 and 54
   references, with identical counts on both sides. The `-dl -dg` dumps show why the points
   base is allocated first: 157 weighted references over 909 insns gives priority 12,090.
   The scratch pointer has 195 references, but its live length is doubled to 1,274 by
   `update_equiv_regs` because it carries a REG_EQUIV symbol, giving 10,714. Every symbol load
   gets that note at expansion. About 20 semantic-preserving variants left both numbers
   unchanged: types, declaration order, an explicit scratch local, index re-reads and loop
   forms. The next lever is to change how much code outside the part loop the points base is
   live across, or to find a source form whose scratch pointer has no equivalence note.
2. **Face-row address (4 instructions).** The cartridge adds `0x02033B70` to `ring*1344` as
   three immediates and tests `ldrh [r7]`. Under -O2, `expand_binop` forces the constant into
   a register: `preserve_subexpressions_p()` returns 1 with expensive optimizations, and
   rtx_cost is 5. CSE then rewrites the duplicated exit test to `[ring*1344 + K]`. That leaves
   two uses, so combine cannot fold the constant back. These forms all reproduce the forced
   register: for/while/do, an `if`+do-while, an index loop, a 2-D row array, an integer
   address and a local base.
3. **Finish block.** The front end re-associates the four-depth sum. `z = d0 + d3;
   z += d2 + d1` gets separate d0/d3 loads. The cartridge's `sub r0, fp, #0x30;
   ldmda r0, {r0, r1}`, however, implies a register base at `&depth[2]`, which no tried form
   produces; 96 orderings were brute-forced. The texture/mode store is also scheduled earlier
   than in the cartridge.
4. **Smaller reload choices.** A second CURRENT pool load appears as `ldr r6` versus our
   `mov r5, r12`. The special-entry table base is reloaded at a different point. The
   projection multiplies are scheduled differently.

The decomp-permuter was not run. The repository has no permuter adapter
(`permuter-queue.md`), and the dominant differences above are allocator priority and
expansion decisions rather than local ordering. A detached run would also outlive this session
with nobody to harvest it. With the r9/r10 priority question settled, the natural candidate is
the right permuter seed.

## Scope note: what "finished" means

The 85.492% figure (73,162 of 85,578 mapped code bytes, 189 replacements) is measured against
the current 237-entry map. `progress.json` still reports **719,822 unknown bytes**: ROM not yet
classified as code or data. The map has grown before, from 229 to 237 entries. Matching the
remaining mapped entries therefore does not by itself prove the decompilation is complete. This
pass did not change the map.

## Reproduce (on a worker, never the laptop)

```sh
python3 tools/measure_candidate.py docs/near-misses/finish-1114-renderer/func_08016DA8.c 08016DA8 08017E68 arm /tmp/r
python3 docs/near-misses/finish-1114-renderer/sbs.py /tmp/r.diff.txt --score
python3 docs/near-misses/finish-1114-renderer/check32.py docs/near-misses/finish-1114-renderer/func_08016DA8.c
```

About 285 source variants were compiled and measured on worker C. Their scratch outputs
(`~/txra-renderer-out/`) were deleted after the receipts above were copied.

matches installed: none (189 exact replacements remain)
near-misses improved: 08016DA8: 3250 -> 2446 differing bytes (instruction distance 897 -> 622; length 4268 -> 4288 = target; frame 108 -> 96 = target)
what blocks the rest: the allocator gives the points base higher priority than the REG_EQUIV-doubled scratch pointer, so sb/sl come out swapped (~100 instructions); the forced face-row constant plus three scheduling/reload choices account for the remaining non-register differences.
