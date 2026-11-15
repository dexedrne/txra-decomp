# Track renderer pass

08016DA8 improves **3,251 → 3,250 differing bytes**. Instruction edit distance
improves 898 → 897. Output remains 4,268 / 4,288 bytes, and the local frame
remains 108 / 96 bytes. The candidate is complete, uninstalled and measured
with the unchanged historical ARM profile through 08017E68.

The decompiler view agrees with the retained ring/face traversal, four-part
near path, independent subdivision cases, four-point projection loop,
visibility and winding guards, texture selection and packet insertion. Faces
are 56 bytes, points 28 bytes and packets 32 bytes. There are no outgoing
calls or indirect switch tables to recover in this owner. The retained change
puts face indices and the part counter in the face iteration's scope rather
than the function's outer scope.

The high-level depth-array join remains unreliable. Independent annotation
of the existing assembly establishes four contiguous depth stores at frame
pointer offsets -56, -52, -48 and -44. The address of the first is retained
and later indexed by the part counter. Initial p-code retains these stores;
the optimized printed view presents scalar depths while leaving its indexed
array apparently uninitialized. This is an analysis limitation, not evidence
that the cartridge omits initialization. No missing store was copied out of
that faulty view, and no synthetic assignment was added to the ROM.

The rewritten source passes the unchanged **199 independent differential
memory fixtures**, 20 fixed checks, three size checks and 14 offset checks.
All **1,053 original instruction addresses** are reached by the synthetic
textual ARM executor. These are synthetic states, not gameplay. Eight
alternative integer-pointer spellings failed the host fixture's pointer-width
check and were rejected; the retained source does not contain them. A second
address-form pass uses mapped byte-pointer arithmetic and finds no gain.

Remaining structure: the twelve excess frame bytes and twenty missing output
bytes remain. Point pointers and offsets still differ at the near/direct join,
and packet arithmetic and spills remain displaced. Next independently annotate
the A/C/B offset and pointer lifetimes at the depth-array join; do not infer
their identities from the decompiler's scalar names. Merely moving the direct
point pointer or changing typed component address spelling has plateaued.

Reproduce with `tools/measure_candidate.py`, entry 08016DA8, end 08017E68,
profile `arm`. `arm-candidate-checks.json` records the unchanged executor.
