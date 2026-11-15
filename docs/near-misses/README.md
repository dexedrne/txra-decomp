# 11/9 second complete-owner comparisons

The exact registry stays at **181 entries, 72,524 bytes including pools**.
No replacement was installed. This pass continues the preceding source steps:

| Owner | Differing bytes before / after | Evidence |
| --- | ---: | --- |
| 08016DA8 | 3,677 / 3,401 | [Typed renderer geometry lifetimes](arm-16da8-1109b/README.md) |
| 080064A4 | 3,473 / 3,395 | [Preparation identities and command lifetimes](sound-owner-1109b/README.md) |
| 0800421C | 3,831 / 3,434 | [Mixed smoke induction and temporary roles](hud-owner-1109b/README.md) |

All comparisons cover complete owners, with unchanged compiler profiles and strict
ends. Retained controls expose instruction/frame tradeoffs rather than hiding
them. Each source has pinned fixture evidence; see the [round 2 ship note](../MATCH1109B-SHIP.md)
for admission results, review pictures/clips, commits and the remaining work.
Only each best candidate's full diff is uncompressed; other long receipts use gzip.

# 11/9 complete-owner comparisons

The registry remains at **181 exact C entries**. No new replacement was installed.
The first round's measured nonmatches and concrete next source steps were:

| Owner | Differing bytes before / after | Evidence |
| --- | ---: | --- |
| 08016DA8 | 3,850 / 3,677 | [Renderer control flow and allocation](arm-16da8-1109/README.md) |
| 080064A4 | 3,568 / 3,473 | [Sound field lifetimes](sound-owner-1109/README.md) |
| 0800421C | 3,894 / 3,831 | [Shared HUD scratch aliases](hud-owner-1109/README.md) |

Each folder retains complete C, full sanitized diffs and pinned compiler profiles.
The historical small near-misses below have already been installed or superseded;
use the current registry and the [round report](../MATCH1109-SHIP.md) before choosing
another target. No car-contact trials were repeated.

# Current hand review, 11/4

080165BC, 08017F64 and now 080076F4 match completely and are installed in
`src/generated/`. The retained 11/4 mixer draft is historical; the complete
1,076-byte result is in `src/generated/func_080076F4.c`.

The current car-contact draft is
[hand-20261104b/func_080181C0.c](hand-20261104b/func_080181C0.c).
That folder also retains a diagnostic HUD draft and the source-level prefix
of the enclosing Thumb sound routine. None of those is installed or counted
as a match. See its README for measured comparisons and remaining work, and
[match-1102.md](../match-1102.md) for the accepted matches.

# Round 5 continuation drafts

Historical hand review: [the four attempts scoring at most fifteen](hand-20261031/README.md)
were all tried in the requested order. Their scores count differing **bytes**,
not instructions. None is a standalone ordinary-C function: the closest is a
state-switch veneer, and the other three inherit an enclosing frame. No new
replacement was installed. The review includes compiler dumps, failed probes,
all twelve current scores and concrete enclosing-body recovery boundaries.

These five ordinary C drafts compiled, but **none matches the complete target**.
Do not install them or count them as recovered functions. Each `.json` records
the compiler profile and the pass that produced the retained source; its attempt
count belongs to that pass, not every historical trial for that function.
Each `.diff.txt` includes the full instruction diff, constants and pool locations,
with raw instruction encodings removed. No binary ROM slices are retained here.
Some trial width changes deliberately test provisional type hypotheses and may
change behavior. They are evidence for the next compiler pass, not replacements.

| Entry | Instruction edit distance | Differing bytes | Compiler |
| --- | ---: | ---: | --- |
| 08014614 | 4 | 11 | old |
| 08015DA8 | 25 | 60 | standard-o1 |
| 08014104 | 6 | 10 | old |
| 08014988 | 12 | 50 | old |
| 0801466C | 6 | 10 | old |

The angle draft still emits four extra bytes and crosses the next mapped entry;
its narrowing return is unresolved. The two six-instruction misses involve
register choices and instruction order. The queue and packet routines still need
more substantial source improvements. Every comparison includes referenced
literal pools beyond mapped instruction ends.

`rejected/` contains thirteen diagnostic lifted drafts and rejection texts, **not
compiled near matches**. These include internal fragments, incomplete bodies,
shared epilogues, ARM entries and a runtime helper. No compiler diff exists for
those entries. Recover an appropriate complete body or compiler path first.

Search manifests, the accepted EEPROM result and aggregate accounting are in
`docs/match5-search/`. The accepted routine's C is in
`src/generated/func_08018AA4.c`; it is intentionally outside this near-miss folder.

## Round 6 status

0801466C is now installed as a complete 136-byte match; its round-5 files here
remain historical. The packet files have been updated to the one-instruction,
two-byte miss: a state-address reload instead of a saved-register copy. The
angle, blit and queue entries remain unresolved. The new 176-byte EEPROM read
match is outside this folder. See docs/MATCH6-SHIP.md and docs/match6-search/.

## Round 7 status

08014614 is now installed as a complete 88-byte match. Its older draft and diff
above remain historical, alongside the previously resolved 0801466C files.
The byte and halfword decoders at 0801251C and 080123F0 also matched completely;
their sources are in src/generated/ and their search evidence is in docs/match7-search/.

The queue at 08015DA8 now has a word-width source and the correct 118-byte
extent. Its remaining eleven instruction / eleven byte differences exchange the
scratch and destination registers. This supersedes the older twenty-five-
instruction hypothesis that narrowed the source incorrectly. It is still an
uninstalled hypothesis. Packet remains at one instruction / two bytes, and blit
at six instructions / ten bytes. See docs/MATCH7-SHIP.md for accounting and limits.

## Round 9 angle/queue status

The angle at 08014614 remains an already-installed, complete 88-byte match.
The queue at 08015DA8 is now a four-instruction / nine-byte miss with the correct
118-byte extent. The retained C assigns the destination from the known-zero
source in the empty-queue branch. This changes allocation in the transfer body,
but introduces a zero materialization in that branch, consumes its alignment
padding, and reads the DMA control into r1 instead of r0. It is **not installed**.
An alternative seven-instruction / seven-byte miss keeps identical instruction
shapes and pools; see docs/match9-search/queue-lifetimes/. All comparisons include
the complete mapped extent and pools. The historical round-7 queue is retained
in docs/match7-search/queue_work/. No other family's draft was changed.
