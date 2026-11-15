# TXRA deep hand matching, slice l (second pass over the slice-j selection)

One more routine builds from ordinary C and the ROM stays byte-identical.
Accepted totals move from **146 functions / 28,358 bytes / 33.311%** to
**147 / 28,714 / 33.729%** of the 85,132 mapped code bytes. The match uses the
`old` profile; no flags, inline assembly or output patches.

The brief named this "slice j"; an earlier slice j already exists
(`docs/deep-j/`, `DEEP-J-DONE`), so this pass is recorded as slice l to keep
that record intact. Selection: the 83 unmatched entries from
`tools/rank_targets.py --json` on main at 146 matches, sorted by
`(bytes, address)`, zero-based odd indices `[1::2]`: 41 entries.

| Commit | Entry | Bytes | What made it match |
| --- | --- | ---: | --- |
| 846e714 | 08006270 | 356 | Sound stream mixer. In the first loop the sample index is read through a block pointer to `g_030079D0[ch]` and the limit through a second pointer to the record table +16; that reproduces loop.c's hoist order (buffer, index, limit base in pass one, step global in pass two). The mixing temporary is one function-level variable shared by both halving loops, so it is a global allocno whose priority falls between the two buffer pointers; `v >>= 1` as its own statement sets the live length that puts it there. |

All 41 entries are accounted for in [deep-l/OUTCOMES.md](deep-l/OUTCOMES.md).
Two drafts improved without matching, kept in `docs/deep-l/drafts/`:

- 0800B3A0 (point plot): everything except the odd-x branch now matches. The
  pixel address must be written inside the dereference so EXPAND_SUM emits
  `y*240` before `(x>>1)*2 + screen`; `x + (32 + shift)` keeps fold from
  grouping the constant with `shift`; a full-width temporary for the 0xFF00
  mask leaves the constant in the loop and frees r10 for `&g_03002E4C`, as in
  the original. Left: the odd branch swaps r0/r1. With exactly three local
  quantities, local-alloc's three-element hand-sort compares fixed quantity
  numbers rather than the current order and can never allocate the address
  quantity first, so the original block must have a fourth local quantity or
  a non-local `x >> 1`; not found.
- 080162F8 (rotation and projection): 222 to 161 differing rows. The trig
  globals are assigned straight from the tables (destination address loaded
  first) and read back through the globals; centre and delta are a volatile
  two-element local array so every field is a constant stack offset and is
  reloaded like the original. Left: the original frame is 60 bytes (ours 48)
  and the spill choices differ; a coordinate search over operand orders found
  nothing (they are canonicalised).

08008914 was worked without a match (CSE merges the two 255 masks into one
register used outside its block, so loop.c will not hoist it; the original
hoists 1 and 255). 0800B4D8 and 0800CEEC were read and diagnosed only. Seven C
seeds were not reached (080154AC, 0800AF4C, 0800CB5C, 080098DC, 0800E498,
0800F2D0 and the ARM seed 080165BC). The 17 assembly, BIOS and runtime entries
were already recorded in `docs/asm-only.md`; no new entries were needed.

`tools/review_deep_l.py` renders the review pictures and one muted clip
outside the repository (`txra-review/deep-l/`; run it with system
Python and the venv's site-packages on `PYTHONPATH`, because the venv has no
Pillow).

Validation: after the match `make` ends in `build/txra.gba: OK`, `cmp` with
the base ROM is identical, and the 170-test suite passes. The generated
`docs/map/indirect.json` drifts locally during `make` and was restored, not
committed. No OWNER-NOTES.md was present in the repository during this pass.
