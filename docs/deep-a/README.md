# Deep hand matching, slice a

Seven exact replacements added 3,324 bytes. The frozen allocation and all forty decisions are in [outcomes.md](outcomes.md) and [targets.json](targets.json). The existing mapped-code denominator remains 85,132 bytes.

The `candidates/` files are handwritten, unmatched source hypotheses, not replacements and not validated behavior. They are excluded from the build and have no `rom.cfg` entries. Their score and unresolved source details are in the outcome table. The external review folder `txra-review/deep-a/` retains side-by-side text diffs and profile evidence. Some useful profile outcomes belong to different source hypotheses; do not assume one profile fixes all later edits.

Next useful source lessons:

- Preserve distinct address symbols when original source identities may differ, even when the addresses coincide. The startup range-end markers proved this with a complete ARM match.
- Keep narrowing and signed division stages explicit. The character mapper needs one reused byte offset; stat updates perform /100 and /32 as distinct statements.
- Use named layout fields instead of pointer casts into padding. Offset 24 is a signed word without changing the 100-byte record stride.
- Local creation order matters: the line renderer requires its high-octant expression after the first loop to recover the original stack slots.
- ARM and DMA are not assembly-only classifications. The queue dispatcher and ten startup copies match ordinary C with the ARM compiler profile.
- Recover switch tables before accepting an unresolved-control-transfer rejection. The character mapper became an exact match this way.

The large ARM body `08016DA8` now has a [complete C body recovery and prepared ARM-profile candidate](../near-misses/arm-16da8-1107/README.md), including the near subdivision/projection path. Both sources pass 199 synthetic comparisons against execution of the actual assembly, reaching all 1,053 instruction addresses. All 19 pool targets and the source assembly extent are now verified on the private host; the prepared historical-profile candidate is 4,028 versus 4,288 bytes. It is not a replacement or a proven exact match. This supersedes the earlier partial-recovery status; the old lifted draft still must not be used as arithmetic evidence.
