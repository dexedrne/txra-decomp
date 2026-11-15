# Slice b hand recovery

The frozen inventory is the starting revision 7b37a3e: all unmatched entries
sorted by (mapped extent bytes, address), zero-based offset 1 with stride 3.
`targets.json` preserves the 40 assigned entries; the order is not recomputed
after installing matches. `OUTCOMES.md` records every entry, including helpers
and invalid standalone boundaries. No other slice's source was edited.

Three exact additions total 1,830 bytes. The 94-byte library copy needs
`old-no-interwork`; the 632-byte and 1,104-byte dispatchers use the default
profile. Both dispatchers remain exact when compiled in either order in one
translation unit with a shared record definition (`unit-order.json`). The
standalone build retains separate files and the full ROM identity gate.

## What changed the result

Recovering ordinary source variables was more effective than permuting machine
register variables. The dispatchers use real switches, typed 32-byte records,
independent callback checks and shared C labels. A record field retains a base
plus an immediate offset where a nested byte array may generate an extra
address addition. Keep a byte load and its following decrement as separate
assignments when reproducing the original allocation. Both switch tables had
already been reviewed; the ranker's unresolved-transfer warning was not proof
that they required assembly.

The library copy is ordinary aligned word/byte loops. Its return sequence is
controlled by Thumb interworking, so library and game compiler settings must
be evaluated separately. No emitted assembly was patched.

## Unfinished source hypotheses

The files under `seeds/` are compilable source hypotheses, not verified semantic
replacements. They are outside the build. Their comments and integer addresses
are source-recovery evidence; binary compiler artifacts remain under build/.

| Seed | Useful change | Remaining issue |
| --- | --- | --- |
| 080147D0 | Addressed local for BIOS fill; explicit parallel pointer cursors. | Indexed loop strength reduction and saved pointer allocation. `-fno-strength-reduce` improves shape but is not an installed profile. |
| 080148B0 | Full-width packet pointer, current callee signature, persistent serial pointer and common return. | Two mask calculations omit the original copies; 210 versus 214 bytes. Narrow temporaries regain length by adding wrong shifts. |
| 08014AE0 | Volatile 64-bit hardware snapshot reproduces the high-word-first read and stack pair. | State pointer lifetimes, indexed loop and pool placement. |
| 08006270 | Full-width source pointers and explicit signed-byte averaging. | Reloads, loop allocation and shared final stores. |
| 08016C18 | Ordinary ARM C frame; 24 points per 672-byte group; MLA arithmetic restored. | ARM allocation and scheduling; no ARM acceptance/build profile added. |

## Lifted-draft hazards

Do not assume the retained near-miss score proves a valid source hypothesis.
Several drafts narrow a pointer to a signed halfword, or reuse a narrowed scalar
later as an address. Restore address widths before optimizing a byte score.

Hardware access through a register-valued address lost volatility in the lift.
Restore volatile DMA reads/writes and addressed volatile stack fill values.
Calls through the Thumb-to-ARM entry must keep the actual entry address rather
than naming the ARM implementation as a Thumb BL destination.

Some caller drafts omit fifth outgoing stack arguments because an optimized
matched callee does not read them. Preserve the caller's actual outgoing slot.
Some signed division drafts omit both operands; the physics body uses thirteen
divisions by 100 and one by 12. The large menu body also divides by 100.

In 080154AC, two emitted drafts shift a glyph return left by 24 and then cast
that already-shifted register to a byte, erasing the glyph. The target shifts
right by 24 at that second step. ARM drafts similarly omit MLA as a generic
long-multiply comment and omit parentheses around shifted subtraction operands.
These findings describe draft emission; no desktop runtime diagnosis is claimed.

See ../asm-only.md for assembly contracts, non-ABI live-ins and truncated units.
The three accepted replacements are ordinary C; no wrappers count as C matches.
