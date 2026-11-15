# Complete streaming owner

This round adds the first complete structured C hypothesis for
08002854..0800418C, including the internal 08003786 continuation. The first
validated complete draft differs in **6,312 bytes**; the retained rewrite
differs in **6,106**. Output grows 5,160 → 6,120 of the original 6,456 bytes,
and instruction edit distance improves 2,747 → 2,661. The local frame changes
164 → 156 bytes; the original reserves 268. Nothing is installed or counted
as an exact match.

Joining the continuation in the private analysis database removes the false
recursive-call interpretation. Its backward long transfer is the second
iteration of a two-column scenery loop, and its return restores the original
268-byte frame. The public registry and ROM remain unchanged. All comparisons
cover the full enclosure and pools; the 3,890-byte registry prefix is never
used as a checker boundary.

The complete shape is a directional wrapped five-row window, a 24-point and
24-face clear, optional banks, three road strips, two wall seams, bridge
panels and two scenery columns. Source and point rows are 28 bytes, faces
56 bytes, and each ring row reserves 24 entries. Road, bank and wall texture
descriptors have three-, four- and five-word strides. Scenery uses range and
equality guards, with seven-, four-, eight- and fifteen-point construction
paths; there is no switch table. The matched geometry helpers remain normal
calls, with their four/five arguments and order preserved.

The first original-instruction check caught swapped left/right wall seams;
that rejected draft was corrected before the complete baseline was frozen.
The retained rewrite then restores repeated row-field/table lookup expressions,
duplicates the directional window setup and uses a point-base plus emitted
index. Those changes account for the measured improvement. Later store-order,
seam-lifetime and angle-capture variants do not beat it. They are retained only
as compressed measurement receipts, not alternative implementations to ship.

The final independent emulator check passes **480 synthetic states** against
the original instructions and original geometry helpers, comparing all EWRAM,
IWRAM outside the stack, saved registers, stack restoration and **11,998
ordered helper calls**. Cases cover both directions, wrapped positions, every
scenery value 0..19, unchanged/changed wall types and mixed scenery columns.
Arch cases retain their bridge/bank seam dependency; this is not proof for
arbitrary malformed track data. Original lookup data remains private. No
helper is mocked and no emulator snapshot or ROM slice is saved.

The hypothesis is still far from matching: 336 output bytes are missing,
the frame is 112 bytes smaller, and table/field addressing and scratch lifetimes
remain different throughout the owner. Next recover the bank and road
descriptor stores around their helper calls, together with the per-phase
point cursor and count lifetimes. Preserve the complete geometry and the
original-instruction runner while doing that; do not pad the output or add
scratch solely to increase the frame.

A final focused pass also measures reloaded scenery fields and per-case point
bases, separately and together. It finds no lower complete-owner byte count.
The retained source and reviewed media are unchanged. A deliberately swapped
wall seam is rejected by the original-instruction check as a negative control.

Reproduce with `tools/measure_candidate.py`, entry 08002854, end 0800418C,
profile `old`, and `tools/check_stream_original1112c.py` for the independent
synthetic comparison. The baseline source is `stream-baseline.c`.
