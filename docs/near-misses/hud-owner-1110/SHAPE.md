# HUD owner: decompiler-guided comparison

The starting source is the retained 11/9d complete owner: **3,235 differing
bytes**, 4,124 output bytes and a 36-byte local frame. The brief's 3,258-byte
figure predates that source. All measurements keep 0800421C..08005238 and the
historical `old -O2 -mthumb-interwork` profile.

## Analysis view

Ghidra 12.2 imported the private symlink as raw `ARM:LE:32:v4t`, based at
08000000. The 229 registry functions were seeded using their explicit mode and
code spans; pool gaps were excluded. Cartridge data after 08020000 was marked
non-executable. The registry was cross-checked against the assembly labels and
the explicit configuration seeds. The decompiler text and project stay outside
the repository in the private analysis cache. This document describes
observations in our own words; it contains no exported pseudocode.

The inventory splits 080051FE into a function because an early exit uses a
long call instruction to reach it. Its stack restoration shows that it is the
HUD's common epilogue. In the working database, that code was joined to the
owner and the internal transfer was interpreted as a branch. The initial
epilogue export remains a private diagnostic. Neither ROM bytes nor the repo's
inventory was changed. Helper signatures were supplied from our declarations;
their types are analysis assumptions, not recovered source types.

## Observations versus the retained C

| Area | Decompiler observation | Candidate implication |
| --- | --- | --- |
| Entry and exits | One outer enable guard; later mode guards join the same restored-stack return. | The candidate uses early `goto done` exits. Compare nested positive guards with these exits, preserving the separate post-transform mode read. |
| Strip and gauge loops | Countdown strip loops execute four or two draws; text counts upward through six characters; gauge background has three rows and two columns. | The existing counted loops already express these trip counts. There is no HUD switch table to recover. |
| Selection | Gear and map scales use separate equality tests. Glyph classification also uses independent tests. | A switch or mutually exclusive ladder would invent a different source shape. Keep the current independent tests. |
| Record access | Car rows have a 100-byte stride; projected geometry uses 24-byte rows and 12-byte points. Flash and smoke records use a 16-byte stride. | Existing layouts agree with these accesses. The view supports field addresses and strides, but does not independently recover C struct names or types. |
| Flash traversal | A cursor carries the active flag and x field while an index forms size/y addresses. | The retained source spells every access through the index. Try a cursor plus index, with the size field address scoped to its clamp and lookup. |
| Smoke traversal | Allocation carries four field pointers and a byte displacement. Rendering carries a count cursor and z cursor, indexes x, and captures the current y address across helper calls. | Allocation is already close. Rendering still uses one source index for every field; reproduce the mixed traversal without caching scratch values. |
| Temporary lifetimes | Three local words recur through the opening, glyph, gauge, map and projected-effect phases. Register values are reused across regions and split at calls. | Test the observed non-overlapping scalar roles, but do not assume a decompiler variable is an original C variable or force stack slots. |
| Projected effects | Four scratch triples are written before four ordered transforms. Two widths are derived before the first draw; the first projected x is already available, and the sprite tag survives both draws. | Keep all transform aliases and repeated component reads. Compare point-address captures and scalar scope at the width/tag join. |
| Calls | Sound notification precedes the opening scale and sprite; each effect scales before drawing; the two sets of four transforms precede smoke allocation/rendering. | The retained helper order agrees. Read helper bodies to check that transformations can write the shared scratch aliases; do not make them pure for allocation convenience. |

The view is static evidence. It is not execution of the original instructions,
proof of arbitrary aliases, or an installation gate. Any retained rewrite must
still pass the existing source fixtures and complete owner checker.
