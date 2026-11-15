# Rotation and contact pass

080181C0 improves **1,011 → 1,009 differing bytes**. Instruction edit distance
improves 307 → 305. Output stays 1,660 / 1,684 bytes and the local frame stays
64 / 72 bytes. This is a complete uninstalled ARM candidate using the unchanged
historical profile and 08018854 checker end.

The view shows an eight-record outer traversal and eight-record pair loop,
four independent known-pair tests, six rotated probe points, then six contact
tests. A hit either marks an already known pair or updates both records and
fills empty registration slots. No switch table or outgoing call is present.
The existing 100-byte record and 12-byte probe layouts agree with the accesses.

The useful retained change is an outer-record pair-code capture (`i * 16`)
whose lifetime covers the inner loop. Decompiler suggestions about cached
record addresses, next-index captures and coefficient lifetimes were measured;
none beat that source. In particular, the high-level view moves inverse-angle
arithmetic into the pair setup, but the entry instructions actually compute
and save the masked inverse heading before the outer loop. The retained source
keeps that entry calculation. Decompiled temporary identities are not proof
of original C local identities.

The unchanged C-reference harness passes **768 cases**, including 672 state
changes. Its rejected unsigned-narrowing control differs in 428 cases. A new
independent ARM emulator comparison executes both the original instructions
and the compiled candidate on **192 cases**, with 168 state changes and 30
nonzero return cases. Return values, IWRAM outside the stack, saved registers
and stack restoration agree. Coefficient waves, dimensions and masks in this
second experiment are synthetic; no cartridge data table is exported.

Remaining structure: the candidate has 16 referenced pool words versus 18,
and 140 original / 136 compiled instruction rows remain unpaired in the
heuristic alignment. The missing eight frame bytes and 24 output bytes are
not repaired by width-preserving coefficient scheduling or next-index scopes.
No signed coefficient was narrowed, and no artificial frame object was added.

Next: annotate the entry's cached outer-record byte offset and the two
position-delta loads inside the six-point loop, then recover those address
lifetimes alongside the two coefficient spills. The measured commutative
multiply forms, speed-exchange load order and explicit sine captures have
plateaued. Preserve the new independent original-instruction comparison.

Reproduce the profile with `tools/measure_candidate.py`, entry 080181C0,
end 08018854 and profile `arm`. The state runners are
`tools/check_contact1112.py` and `tools/check_contact_original1112c.py`.
