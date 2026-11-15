# Matching workflow

The reconciled build replaces **156 functions / 37,824 bytes / 44.430%** of the
85,132 mapped instruction bytes with ordinary C. This combines deep slice a's
seven complete matches with main's ARM tail thunk, library copy and two full
switch dispatchers. Deep-d adds four distinct Thumb replacements (1,460 bytes).
Deep slice f adds the 300-byte sound-channel snapshot at 08006070. All eight
compiler profiles remain available.

## Deep slice f: compilation units

08006070 matches only when compiled after its ROM neighbours. The historical
compiler numbers constant-pool labels across a whole file, and the global CSE
pass hashes those label names. The order in which it visits hoisted address
constants therefore depends on how many constants earlier functions used, and
that order decides register ties. `src/generated/unit_08005C7C.c` includes the
sixteen routines 08005C7C-0800622A in ROM order; every one of them is verified
from that unit. Each per-function file still compiles alone; only 08006070
needs the unit. Register ties that no source change resolves may need the same
treatment: test the function after its matched predecessors before searching
further. See `docs/COMPILER.md`.
## Deep slice c and dispatcher recovery

Deep slice c adds the four-byte ARM tail thunk at 08018E88 with `modern-arm`.
See `docs/COMPILER.md`, `docs/DEEP-C-SHIP.md` and `docs/deep-c/` for the limited
compiler evidence, forty-entry audit and twenty-one unfinished C bodies.
Slice b adds the 94-byte copy at 08018E1C with `old-no-interwork`, plus the
632-byte dispatcher at 08002500 and 1,104-byte dispatcher at 08012600 with the
default profile. Their 94-entry and 105-entry switch tables and final pools
are included. These are source matches without new desktop execution evidence.

## Deep slice a recovery

Deep slice a adds the complete
236-byte coordinate transform at 080164D0. Typed three-component vectors retain
the shared field bases; reusing x/y/z after each stage and retaining the original
y before overwriting it reproduce the register lifetimes. Each fixed-point
right shift must stay inside its producing expression: separate assignments
change both allocation and instruction count. The default compiler profile
reproduces every instruction, pool and alignment byte, and the forced full ROM
rebuild passes. Deep slice a also recovers 08017E68 as the first complete ARM
C replacement, adding 252 bytes with the explicit `arm` profile. Its descending
queue loop and ordered callback dispatch reproduce the original frame and
interworking calls. `tools/setup.sh` supplies the matching ARM compiler, and the
normal build and trial judge both verify the same complete bytes.

The 368-byte palette/sprite submission routine at 0801533C is also exact. Its
five stack arguments are actual parameters rather than uninitialized lifted
locals. A shared palette-base temporary initialized before each DMA pointer,
and reusing the search index for insertion, reproduce the allocation and pools.

0800C9C4 now matches all 408 bytes. The 100-byte record has a signed word at
offset 24, replacing four formerly unknown bytes without changing layout. Direct
indexed record accesses, a named initial coordinate address, ordered table loads
and reusing the slope temporary reproduce the entire interpolation routine.

Round 10 adds **zero** exact
replacements after **324,571 recorded fresh source/profile trials** across all
fifteen retained eligible unfinished drafts. Each target received at least 25
minutes of accumulated active wall time, sharing one five-process compiler pool.
Twelve drafts improved, but none matched; failed drafts remain outside the build.
See `docs/MATCH10-SHIP.md` and `docs/match10-search/` for per-function scores,
closest complete text diffs, histories, throughput and resume accounting.

Round 8 added the complete 116-byte packet sender at 08014988. Round 9 added
zero replacements within its angle/queue scope; its historical baseline was
108 functions / 10,582 bytes. The angle was already installed, and queue remains
an uninstalled four-instruction / nine-byte miss. Round 10 independently
reverified the installed angle, sibling and packet across their complete bytes
and next-entry boundaries. See `docs/MATCH9-SHIP.md` for the earlier queue work.
Round 7 adds three functions; its fifteen-addition target remains incomplete.
See `docs/MATCH7-SHIP.md` for accounting, review pictures and retained near misses.
Round 6 added two functions; its fifteen-addition target remained incomplete.
See `docs/MATCH6-SHIP.md` for accounting and the retained near misses.
Round 5 added one function; see `docs/MATCH5-SHIP.md`.
Round 4 has added two functions; its fifty-addition target remains unfinished.
See the round-4 status below and `docs/MATCH4-SHIP.md`.

The historical round-3 baseline ended at 100 functions / 9,084 bytes.
Round 3 has added **40 functions / 6,200 bytes**, starting from the
60-function / 2,884-byte baseline supplied by the previous combined work.
Every installation passed a complete compiler comparison and a forced full
rebuild ending in `build/txra.gba: OK`. The entire ROM remains byte-identical.
Matched spans include literal pools and in-function alignment: their ratio to
85,132 mapped instruction bytes is approximately **10.670%**, not exact source
coverage. All forty requested additions are complete.

1. Install local tools with `bash tools/setup.sh` and supply the private ROM as
   `baserom.gba`. Never commit the ROM, extracted content or generated binaries.
   `make` must end in `build/txra.gba: OK`; `make check` runs the Python tool tests
   with the configured environment, which includes the decoder dependencies.
2. Read `docs/map/functions.json` and follow callers, branches and literal pools
   before accepting a function boundary. Some very small entries are shared
   blocks or epilogues within a larger routine; their size alone is not evidence
   that they can be independently compiled. Leave these unmatched until their
   enclosing routine is recovered. Do not count a matching prefix as a function.
3. Write ordinary C in `src/generated/func_XXXXXXXX.c` with address names until
   evidence establishes semantics. Typed layout guesses belong in `src/types.h`.
   Offset field names record layout only; semantic field names require agreement
   from at least two functions. Two table-transform routines share the provisional
   three-word `TxraTriple`; accesses to the larger record retain offset names.
4. Preprocess with the modern compiler's `-E -P -Isrc`, then compile with
   `old_agbcc -O2 -mthumb-interwork`. The historical executable is cc1, so raw
   preprocessor directives cannot be fed directly to it. No inline assembly,
   handwritten instruction words or patched compiler output are accepted.
   The recorded `modern-arm` exception compiles ARM C with the flags documented
   in `COMPILER.md`; all existing Thumb profiles keep their original options.
5. Inspect a trial with `python3 tools/diffhint.py 0801604C build/trial.c`.
   Exit status zero means exact bytes across the complete mapped extent and any
   emitted pool; status one reports a mismatch. The bounded instruction diff
   identifies changed registers, ordering, constants, lengths and literal-pool
   words. Adjust types, variable initialization, statement order or loop shape
   and retry using the previous C and that diff. The same formatter feeds retries
   in the local matching loop. Literal data is labelled as data rather than
   interpreted as instructions.
6. Register an accepted replacement under `matches` in `tools/rom.cfg` with its
   offset, source and exact compiler function size. `tools/match.py` recompiles
   every installed replacement, resolves relocations, and verifies every byte.
   The compiler's `.size` excludes incidental assembler section padding after
   a function; real in-function alignment and pools remain in the comparison.
   `make analyze` regenerates assembly around replacements, and the full build
   checks the resulting ROM SHA-1. Keep all intermediate binaries under `build/`.

## Calls and named data

Both installed replacements and trials use `tools/reloc.py`. `symbols()` supplies
mapped `func_XXXXXXXX` names, provisional runtime names and address-only `g_XXXXXXXX`
data names from referenced literals. Existing `gUnk_XXXXXXXX` names remain valid.
Runtime names prefer mapped THUMB veneers when a THUMB call requires one.
`declarations()` emits provisional byte-array externs for literal data references;
use a more precise access type when the instruction widths establish it. Example:

```c
extern u32 g_03000DE4;
extern u16 g_03000B54[];
extern void func_0800761C(u32, u32);
void func_0801604C(u32 value, u32 index)
{
    if (g_03000DE4 == 1) {
        g_03000B54[index] = value;
        func_0800761C(value, index);
    }
}
```

BL relocations resolve mapped THUMB destinations at the trial's real ROM address,
including the relocation's symbol addend. Absolute pool words resolve data,
function pointers with their THUMB bit, or local `.text` addresses. Unknown names,
non-THUMB BL destinations, out-of-range calls, invalid BL encodings, negative or
out-of-bounds relocation offsets and unsupported separate sections are rejected.
Address-only globals have provisional address identity, not guessed semantics.

The shared relocation path existed before this pass; the stale claim that all
relocations were rejected has been removed. This pass adds named-data prompt
context, range/addend checks and end-to-end examples of calls and globals.

## Local matching loop

`python3 tools/llm_match.py --forever` tries unmatched THUMB candidates. Complete,
called/referenced entries come first, with callers whose direct callees are all
matched prioritised; candidates within a group are ordered by size. The loop
first tries `tools/leafgen.py`, including named-global variants, then requests C
from the separately managed local service. `--limit` sets batch size and
`--retries` sets compiler-judged guesses. `--list` shows candidates without requests;
`--dry-run` tests the path without installing anything or contacting the service.
`--commit-message` prints the message for a progress commit with the real counts since
the committed `progress.json`, for example `Local model loop: 42 attempts, 0 matched`;
commit loop progress with `git commit -m "$(python3 tools/llm_match.py --commit-message)"`.

Twenty-one hand-reviewed C examples and compiler notes live in `tools/fewshot/`; prompts
select up to six nearby or directly related examples, along with related installed C, call declarations, global declarations,
the lifted draft and the target instruction listing. Failed trials send both the
previous C and the shared diff into the next retry. Byte distance includes missing
and extra bytes. If a retry regresses or fails compilation, the next prompt also
restores the closest compiled source and its diff. Shared recovered layouts are
included by the judge, and their typed globals take precedence over provisional
byte-array declarations. A successful standalone
comparison is installed only when a forced complete rebuild and SHA-1 check pass;
otherwise source/configuration changes are rolled back. Updating the matches
array preserves the formatting of the existing large mapping table.

The loop checks for unrelated loaded models and serializes requests with its
existing local lock. It waits through outages. `TXRA_OLLAMA_URL` overrides the
service endpoint. Logs and resumable statistics stay in `build/llm-match.log` and
`build/llm-status.json`; dry runs use separate status. Name proposals remain
unreviewed until call/data evidence supports a rename. No benchmark of service
success rate after these changes is claimed: the independently running service
checkout was neither edited nor stopped. Historical request/attempt statistics
are retained, with new hand matches counted separately in `progress.json`.

## Review evidence

`python3 tools/review_match2.py <review-directory>` renders before/after totals,
matched bytes, percentage milestones and a six-second muted 30-fps progress clip.
It reads configuration and progress metadata only. The horizontal chart axis is
accepted replacement order, not elapsed minutes. Notes and captions accompany
every picture and clip. See `docs/MATCH2-SHIP.md` for checks and remaining work.

## Round 3 details

`--hard` sends complete unmatched functions with **8–40 decoded instructions**
directly to the local service, bypassing the deterministic pass. Instruction
counts exclude pools and count each decoded BL as one instruction. `--hard --list`
shows the selection without contacting the service. Balanced-stack validation
rejects shared epilogues and fragments whose reachable body extends beyond their
mapped unit. Matched callees supply their C signatures; other callees retain
explicitly provisional signatures from register-use analysis. `--hard --dry-run`
exercises requests with a fake responder and never installs or updates progress.
The separately running service checkout was neither edited nor stopped.

The default compiler is still `old_agbcc`. A match may explicitly select
`"compiler": "standard"`, meaning the installed `agbcc` variant from the same
pinned toolchain. The EEPROM geometry selector at 08018A5C reproduces its saved
return register and all 72 bytes with this variant; the default variant does not.
The clear loop at 080146F4 uses `"compiler": "old-no-gcse"`, the default
compiler with `-fno-gcse`: ordinary `-O2` hoists its two outer pointer increments
before the inner loop and fails the comparison. This narrow, recorded option
reproduces all 88 bytes. Both trial judging and the full build use the recorded choice, and unknown
variants are rejected. This does not establish the exact original vendor compiler
or flags. No output is patched and no instructions are supplied as data.

`src/types.h` contains provisional shared layouts and selected address-named
globals. See `docs/MATCH3-LAYOUTS.md` for access-width and stride evidence.
No new behavior names have passed the two-call-site naming threshold.

`python3 tools/review_match3.py <directory> --baseline 76f6fea` produces matching
function and byte charts over the actual commit times of accepted batches, the
same-view before/after totals, and a six-second muted 30-fps progress clip. It reads
our configuration, progress metadata and version history only, never ROM data or
game imagery. Charts describe acceptance batches, not a matching-speed benchmark.

## Round 4 status

This pass currently adds **2 complete functions / 444 bytes**: the paired save
unpacking and packing routines, 08013B38 and 08013C08. The total is **102 functions /
9,528 bytes / 11.192%** of the unchanged 85,132 mapped instruction bytes. The
requested fifty additions are **not complete**; forty-eight more are needed.
Each installation passed a forced complete rebuild and ROM identity check.

The combined starting configuration omitted the thirteen reviewed executable
copy ranges recorded in `docs/map/copies.json`. Rebuilding without them silently
reduced the generated inventory to 222 functions / 75,548 instruction bytes.
Restoring those metadata records to `tools/rom.cfg` makes the analyzer reproduce
the reviewed 229-function / 85,132-byte inventory. This is not new code coverage.
The old manually established indirect call at 080065CC still needs its loop-aware
resolver improved; the reviewed indirect metadata is retained.

Shared names and their agreeing accessors are recorded in
`docs/MATCH4-LAYOUTS.md`. The alias table in `tools/reloc.py` supports both semantic
and legacy address names, with no change to placement or bytes. Unknown car and
physics field meanings remain provisional. No function symbol was renamed.

`python3 tools/rank_targets.py --json` reports remaining entries by value per
estimated difficulty, with real dynamic counts first when supplied.
`--smallest-first` provides the boundary-review order used for hand work.
The current coverage files contain session totals and entry-execution evidence,
**not per-function call counts**. Consequently dynamic counts are reported as
unknown; static caller counts and observed entries remain separate evidence.
The ranking also flags obvious non-argument register reads before definition,
excluding prologue saves; this is a rejection hint, not a dominance proof.
The optional `function_call_counts` map in `docs/map/coverage.json` can supply
future measured counters. No counters were invented or inferred from sessions.

There are now 24 few-shot examples, including both new save routines and the
OAM attribute-copy routine. Integer address arithmetic preserves the initial
save cursor register where an equivalent pointer-only expression does not.
Retry diffs now identify the first differing byte, exact prefix and suffix,
length mismatch and register-only instruction-shape changes. Hard-mode prompts
ask for boundary, width and stack checks before local source edits. The separate
service checkout was neither accessed nor modified, and no live-service
success-rate claim is made.

The round-3 chart renderer also accepts `--target-additions 50` so the round-4
review notes expose the shortfall. See `docs/MATCH4-SHIP.md` for validation,
review pictures, accepted commits and remaining work.

## Round 5 compiler search

`python3 tools/variant_search.py --all --budget 15000` searches ranked complete
unmatched THUMB functions with 8–60 instructions. A single target accepts
`ADDRESS draft.c`; `--jobs` defaults to all cores and workers run at nice 10.
`--install` enables the existing forced full-build and whole-ROM identity gate.
Without it, exact candidates remain uninstalled in the output directory.
No service is called. Mapping and copy metadata remain unchanged.

The deterministic beam search compiles local variants, orders them by instruction
Levenshtein distance and then differing bytes, retains source diversity, and tries
multi-edit escapes when a neighborhood is exhausted. It varies scalar widths,
casts, declaration and initializer order, register hints, supported loop shapes,
index/pointer spelling, compound assignments, constants, arithmetic operand order,
early-return shape, and IO volatility. Parameter declaration order is also tried as a provisional signature hypothesis;
final byte equality protects the original machine calling convention.
It is a bounded syntactic search, not an exhaustive C synthesizer. Arbitrary
nested control flow and alias-sensitive rewrites still require better seed drafts.

The comparison extends through referenced pools beyond mapped instruction ends.
Only equality of the complete bytes can stop the search as an exact result;
a zero approximate score alone cannot install a function. The final check also
rejects output crossing the next mapped entry. `docs/near-misses/` retains the
best compiled drafts, compiler profiles, complete instruction diffs and attempt
counts. Rejected fragments are explicitly distinguished from compiled near misses.

Five compiler profiles share the judge and full-build path: old and standard at
`-O2`, old with `-O2 -fno-gcse`, and old and standard at `-O1`; all use
`-mthumb-interwork`. Unknown profiles remain rejected. The EEPROM DMA transfer
routine at 08018AA4 matches all 128 bytes under `standard-o1`, giving direct
matching evidence for that profile. This does not prove the original vendor flags.

`python3 tools/review_match5.py <directory> --baseline cbc2dfe` renders before/after
status, accepted count and percentage over actual commit times, matched bytes,
and a muted six-second 30-fps progress clip using only our metadata.

## Round 6 targeted matching

Two complete replacements add 312 bytes: the 176-byte EEPROM read at 08018B24
with `standard-o1`, and the 136-byte link update at 0801466C with `old`. Each
passed uncached boundary comparison, a forced full build, and whole-ROM identity.
The total is 105 functions / 9,968 bytes / 11.709% of the unchanged 85,132 mapped
instruction bytes. Thirteen of the requested fifteen additions remain.

`tools/matching_patterns.json` records six transformation families with accepted
source evidence. `matching_patterns.py` tries these before ordinary variants:
integer cursors, named saved constants, separate pointer updates, guarded loops,
scaled stack byte offsets, and explicit global pointers. The EEPROM offset
transformation has an integration test that reproduces its full exact output.
The link update also needed its bitmap and destination initializers ordered
alongside the loop setup. Pattern proposals are hypotheses, never acceptance.

`variant_search.py --focus 'tail|packet|inverted' ADDRESS seed.c` restricts edits
to statements containing the regex. Sources are normalized before filtering so
whitespace edits do not bypass focus. `--all --max-instructions 120` broadens
the eligible size range. Search keeps bounded cached neighborhoods, caps source
size, limits escapes and generations, and records generation counts. It remains
a bounded syntactic search. Extra compiler flag trials found no exact winner;
the five build profiles are unchanged. No separate matching service was used.

The packet near miss is down from twelve differing instructions to one: a
constant-address reload instead of a saved-register copy. The angle still has
return-narrowing and conditional-shape differences; blit allocation and queue
shape remain unresolved. Completed manifests, manual grid descriptions and
flag trials are retained under `docs/match6-search/`.

`python3 tools/review_match6.py <directory> --baseline 6430112` renders the same
before/after view, counts, bytes and percent over accepted commit times, and a
muted six-second 30-fps progress clip. It uses only our metadata and history.
No new game execution or save-session evidence is claimed.

## Round 7 near-miss continuation

Three complete replacements add 614 bytes: the 88-byte angle difference at
08014614, the 226-byte byte decoder at 0801251C, and its 300-byte halfword sibling
at 080123F0. All use the existing `old` profile, passed uncached boundary checks,
forced full rebuilds, and whole-ROM comparison. The new total is 108 functions /
10,582 bytes / 12.430% of the same 85,132 mapped instruction bytes. Twelve of the
requested fifteen additions remain; this round is incomplete.

The angle needs direct returns for the first two branches and a full-width wrap
result, with offsets distributed in the tail. Both decoders need an explicit
infinite outer loop with separate exits. Direct mask tests preserve the saved
tag's load order. A named addition input fixes the byte decoder's operand order;
direct mask assignments and a direct zero test resolve the halfword sibling.
`tools/matching_patterns.json` now has thirteen transformation families backed by
accepted source. Integration tests reproduce all three new full matches from
retained seeds using the learned templates. They remain compiler hypotheses,
not a trained statistical predictor or substitutes for byte comparison.

The word-width queue draft now has the exact extent and instruction shapes; its
eleven remaining differences exchange scratch and destination registers. Reusing
one scratch variable for addresses and the DMA mask prevents unwanted invariant
hoisting. Packet remains a one-instruction miss, and blit a six-instruction miss.
Their full comparison text, retained sources, focused passes, hand-designed grids,
and compiler flag trials are in docs/match7-search/ and docs/near-misses/.

`variant_search.py --seconds 60` bounds per-target time and retains the best
comparison when time expires. `--resume` skips finalized entries already in the
output manifest, allowing a broader batch to continue without losing completed
measurements. Focused statement extents are cached by parent source and regex.
`tools/targeted_search7.py --help` lists reproducible source grids;
`tools/flag_search7.py ADDRESS seed.c` measures alternate flags without changing
emitted assembly. No extra profile produced an exact match; build profiles remain
unchanged. The broader pass covered 21 standalone entries through 160 instructions
and explicitly rejected 25 other entries. Complete accounting and interrupted
passes are distinguished in docs/match7-search/summary.json.

`python3 tools/review_match7.py <directory> --baseline 6ee9de7` renders same-view
totals, three history charts and a muted six-second 30-fps clip. Only our matching
metadata is shown. Previous gameplay and save claims remain historical; no new
runtime execution is claimed. ARM compilation and recovery of enclosing bodies
for rejected fragments remain unfinished.

## Persistent source search

Run `python tools/search10.py --count 15 --seconds 1500 --active-targets 5` with
the configured local Python environment and `nice -n 15`. The same command
resumes gitignored per-target checkpoints; private hash caches stay under build/.
Five compiler processes are shared across up to five concurrent timed targets.
Counts distinguish fresh source/profile trials from repeated cache observations.
Read the search README for hypothesis limits and checkpoint accounting.
Candidates remain drafts until uncached full-byte and next-entry checks, followed
by a forced complete ROM build, succeed. No partial comparison is a match.

## Deep slice a: line drawing

0800237C is now a complete 386-byte C replacement. The clipping guards precede
octant initialization. Duplicating direction assignments inside each octant
branch preserves the original branch shape. Keeping the second octant test as
an expression after the first loop lets the compiler create its spill after the
color temporary, reproducing both stack slots without register bindings or
padding. Full-ROM validation passes.


08018854 is a complete 512-byte ARM replacement, including its 96-byte pool.
The copied-code ranges have distinct source start and end markers even where an
end shares an address with the next start. Collapsing these identities permits
CSE to retain addresses and shrinks both code and pool. Keeping end markers as
separate externs using the already-supported legacy address spelling reproduces
all ten DMA setups and the original frame scheduling with the default ARM
profile. These names record address identity, not recovered original symbols.

Deep slice a also recovers `080157A0` as ordinary C: its indirect transfer is a 224-entry character switch, not an assembly-only calling convention. Case order follows destination blocks, and one byte offset is reused across uppercase, lowercase and digit range tests and their resulting values. The resulting 1,162 bytes, including the table, match exactly under the default compiler profile; the rebuilt ROM is identical.

The complete deep slice-a handoff is [DEEP-A-SHIP.md](DEEP-A-SHIP.md). Its frozen forty-entry outcome table separates seven exact replacements, eleven assembly/BIOS interfaces, six incomplete frame entries, fifteen unmatched full C drafts and one partial recovery. Matching progress alone does not establish PC boot or gameplay; execution milestones remain unverified.

## Deep hand matching, slice b

The frozen size/address ordering assigns forty entries to this slice. One runtime
copy routine matches; twenty-two ordinary C bodies remain unmatched, seven entries
need ABI or boundary recovery, and ten are assembly entries/veneers or probable
private renderer code. The distinction and uncertainty are recorded per entry in
`docs/deep-b/LOG.md` and `docs/asm-only.md`. No prefix or approximate source was
installed. `docs/deep-b/slice.json` preserves ownership from the 109-match baseline;
do not repartition a shrinking unmatched list during concurrent slices.

See `docs/DEEP-B-SHIP.md` for validation, review media, remaining work and commits.

The copy match overlaps the already-installed sibling recovery; the reconciled
union was 120 functions before deep-d rather than counting the copy twice. Deep-b also
contributes ARM literal-load and multiply-accumulate lifting, shifted-operand
precedence fixes, and known argument counts through runtime veneers.

## Deep matching, slice c

The voice initializer at 08005F8C matches all 228 bytes, including its literal
pool and alignment, using the existing `old` profile. A typed eight-element
array of 72-byte voice records and a nine-word preset row reproduce the original
indexed addressing, loop induction, high-register saves and argument stack spill.
The retained register-by-register draft obscured those relationships and even
narrowed the preset pointer. No special compiler flags or output patches are
needed. The forced complete build and whole-ROM comparison pass.

0800B254 adds a complete 332-byte match under the same `old` profile. Explicit
lifetimes for the second record and its first output field reproduce the saved
high registers. Loading the row base before integer byte-offset arithmetic, and
forming the angle output pointer before advancing the row cursor, fixes the last
seven instruction differences. The local 400-byte record spacing is a layout
hypothesis; only observed field offsets are declared. All bytes and the next
entry boundary were verified before the forced byte-identical ROM rebuild.

The related initializer loop at 0800A00C matches all 368 bytes with `old`.
A 100-byte indexed record layout reuses the interpolation shape from 0800B254.
The source loop counts upward from zero through three: the compiler reverses
its unused induction variable, generating the observed countdown. Writing a
countdown directly leaves a two-instruction preheader scheduling miss. This
source-loop distinction, plus declaration order for stack locals, fixes the
complete function without compiler flag changes. Whole-ROM equality passes.

0800A68C matches all 532 bytes, including both literal pools, with `old`.
The accepted palette-transfer shape from 08013FAC supplies the DMA and fade
branches. Initializing the destination after the first DMA source write fixes
pool order. Giving the second destination region its own lexical scope fixes
the remaining 46 register-only differences across the entire first branch.
DMA does not make this function assembly-only. The forced full build and
whole-ROM identity check both pass.

## Deep slice e

The DMA queue flush at 08015DA8 matches all 118 bytes with the `old` profile.
Two source details decide it. The entry's source, destination and size are read
into locals before the three volatile DMA register writes, which keeps three
loop temporaries live and produces the original high-register allocation. The
zero-source exit leaves the loop with `goto` to a label after it; a `break`
lets the loop expander rotate that test to the bottom together with the count
test, and the shape no longer matches.

The sound buffer swap at 080063D4 (timer and FIFO DMA restart,
then clearing the next pair of 44-word buffers) matches all 208 bytes. The
decisive change is a second variable for the next buffer index: with one
variable reused for both indices, the value lives across the clear loops,
becomes a global allocation and pushes every register-setup temporary to a
different register. Writing the clears as upward `*p++ = 0` loops reproduces
the compiler's countdown and its constant ordering.

The link-frame dispatcher at 080148B0 matches all 214 bytes. The serial
control register is read as a 32-bit copy of a multi-player control record:
two halfwords, the first split into bit fields (baud, SI, SD, ID, error,
enable, mode, interrupt enable). That one type explains the word load, the
combined `& 0x88 == 8` test and the byte-wide `-65` mask that clears the
interrupt-enable bit. The return value is a halfword built in a local on both
branches; returning the two expressions directly changes the final registers.

Slice e covers 53 entries (even indices of the size-sorted unmatched list);
the full table is in `docs/deep-e/README.md`. Three idioms worth trying first
on the remaining Thumb bodies: (1) a loop test at the top of the body that
the original keeps at the top means the exit is a `goto` past the loop, not a
`break`; (2) when instructions match but registers do not, look for a variable
the source reused across a loop or call and split it in two; (3) invariant
table loads and row bases that appear before a loop are usually written
inside the loop in the source and hoisted by the compiler. The link unit's
two loops (080147D0, 08014AE0) share an unexplained partial strength
reduction and are the next shared problem to solve.

## Deep slice g

The 352-byte EEPROM write at 08018BE8 matches with `standard-o1`, the profile
already used by its library neighbours 08018AA4 and 08018B24. Earlier drafts
were compiled with the default profile and were 335 bytes off; under the
library's own profile a plain reading of the target is within a few
instructions. Three details close it. The address check, bit packing and DMA
use the sibling read routine's idiom `offset = bits * 2; p = (u16 *)(offset +
(u32)buffer); p += 66;` with a `u32` offset, which gives the original operand
order and registers. The wait loop is one `for (;;)` whose first statement is
`if (!ready && (EEPROM & 1)) { ready++; if (!wait) break; }`; a nested
`while` would re-test the volatile flag after `ready++`, and the original
jumps straight back into the timing body. The wrap-around sum is written
`current + (228 - previous)`; `current + 228 - previous` is folded to
`current - (previous - 228)`.

The 224-byte link setup at 080147D0 matches with the default profile. Its loop
fills three slot tables from two groups of three 24-byte buffers; the original
keeps the index, turns two slot addresses into post-incremented pointers and
recomputes the third (`(i<<2) + base+80`) every pass. That partial reduction
comes from loop.c's hoisting threshold: an invariant is moved out of the loop
only when `2 * (1 + 12 non-fixed registers) * savings * lifetime >= insns in
the loop`. Writing every access through the global itself
(`g_03007A30.field_50[i] = g_03007A30.field_90[i].field_30`) makes each
`&global + offset` its own loop instruction, so the loop is longer than 26
instructions, the short-lived `+80` base stays inside and its slot is never a
strength-reduction candidate. Through a local `s = &g_03007A30` pointer the
loop has only 20 instructions and everything is reduced. `TxraLinkState` now
names the 24-byte buffers at +0x60/+0x78 and the two 72-byte groups at +0x90.

The 496-byte title loop at 08012CC8 matches with the default profile. Its
palette and video clears are the SDK `DmaClear` shape: a block-local
`vu32 tmp = 0` declared before the DMA register pointer, so the zero is stored
before the register base is loaded (`DMA_SET` / `DMA_CLEAR` macros in the
source). The 160-entry clear is an upward `for (j = 0; j < 160; j++)` that loop.c
reverses into the original signed pointer countdown; a downward counter is kept
as a separate biv. The endless loop is `while (1)`: `for (;;)` gets rotated with
an entry jump, which also moves the first literal pool into the middle.

The 516-byte sibling at 08012EB8 is the same title loop with three text lines
instead of two; the 08012CC8 source with the three text records is exact.

The 712-byte scene player at 0800F008 uses the same idioms and matched on the
first natural draft: `DMA_CLEAR` / `DMA_COPY` through the shared `DMA_SET`
macro, the upward 160-entry clear, a `switch` on the scene for the per-frame
work and another for the scene change once the 240-frame counter runs out, and
`goto` back to the two restart points (video reset and state reset). It returns
the scene number. Its five-argument calls to 08016210 pass the fifth on the
stack.
## Deep slice h

The record-placement routine at 0800B908 matches all 716 bytes
with the `old` profile. The last difference was one r8/r9 swap between the
`conflict` flag and the hoisted address of `g_03000000`. Global allocation
ranks them by refs x log2(refs) / live length, and the two were 0.1373 against
0.1395. Live length is measured on the RTL before combine, so a narrowing that
combine later removes still counts. The first rotation block reads the angle
into an `s32`; the second (+8192) one keeps it in a `u16`. The `u16` truncation
adds two pre-combine instructions to the tail where only the address is live,
the address drops to 0.1348, and `conflict` takes r8 as in the original. The
`u16` on the first block instead hoisted the sine-table address out of the
loop, so the placement of the narrowing is what matters.

The four-corner billboard builder at 08009D94 matches all 496 bytes. The
height difference of the two projected corners goes into `distance`, the
variable that earlier holds the track distance, and the width is
`distance >> 2`. Local allocation ties an instruction's result to an operand
that dies there only when that operand is local to the block. Because
`distance` is used in several blocks, `width` gets its own register (r3) and
the later `x[3] = x - width` ties to it, which is the original allocation.
With a fresh temporary, `width` shared the temporary's register and three
registers rotated.

The palette fade at 08015128 matches all 216 bytes. The source reads each
palette entry three times (`pal[i] & 31`, `(pal[i] >> 5) & 31`,
`(pal[i] >> 10) & 31`); CSE merges the reads into one 16-bit pseudo with
several uses, which combine cannot fold into the load, and that gives the
original `lsls #16 / lsrs #21` unpacking and the separate 16-bit mask. The
`r, g, b` channel variables are declared once for the function and shared by
the fade-in and fade-out loops; that is why they occupy the same registers in
both loops. The fade-in target pointer is a never-assigned local, as in the
original (it reads whatever r8 holds).

The sibling fade at 08014FF4 matches all 308 bytes with the same two idioms
(repeated palette reads, channel variables shared by both loops). Its second
loop blends each target channel toward white. The original works one step at
a time: extract the three fields, invert them (`31 - x`), scale with separate
`*=` and `/=` statements (2, 4 and 6 eighths), and invert back. Writing the
scale as one expression lets the front end fold `x * 2 / 8` into `x / 4`,
and the `31 - (31 - x)` order changes the register sequence.

The sound reset at 08007398 matches all 376 bytes from `unit_08005C7C.c`.
Its two wave-RAM fills are ordinary count-up index loops. The first stores
through a plain `u16 *`: a loop with one non-volatile store that starts at
zero is reversed by the loop optimiser (`check_dbra_loop`), which marks the
counter reversed, forces every address giv to be reduced and then eliminates
the counter. That produces the original decrementing pointer, the signed
`bge` pointer compare and a pointer set-up after the hoisted constants. A
`vu16 *` store blocks the reversal (`loop_has_volatile`). With the pointer
set up late, reload never needs r4 as a spill register, so the eight voice
offsets stay in r3 and the post-reload pass turns them into the `+72` chain.
The last difference is a priority tie between two hoisted DMA addresses. It
breaks on the constant-pool label numbers, so it resolves when the routine is
compiled after other functions; almost every non-zero label offset is exact,
and the unit position is one of them.

Checks that resolved this round, in the order to try them: (1) a register
swap between two values is an allocation-priority tie; compute both priorities
from `-dg -dl` dumps (refs are loop-weighted, live length is twice the
pre-combine instruction span) and look for a source form that adds or removes
pre-combine instructions in one value's range only. (2) The same register for
a value in two loops means one shared variable. (3) A signed pointer compare
in a simple fill loop is a count-up index loop that the loop optimiser
reversed; a volatile store prevents that. (4) If an exact tie remains between
hoisted constants, try the routine after its ROM-order neighbours (label
offsets). The compiler sources in the tool tree (`global.c`, `local-alloc.c`,
`reload1.c`, `loop.c`, `gcse.c`) answer these questions faster than variant
searches.

The 424-byte background scroll copy at 08014CE4 (deep slice i) matches once the
first copy loop writes its transfer length as `bytes/2` like the second one.
Combine reduces `((width - x) * 2) / 2` to a single arithmetic shift, so the
bytes are unchanged, but the loop optimiser's first pass still sees the longer
chain. That makes loop 1 big enough (more real insns, lower hoist threshold)
that the 256 row stride is hoisted in the second pass, after the counter copy,
exactly as in the original. With `bytes >> 1` the stride was hoisted one pass
early and landed before the counter copy.
## Deep slice j

The start-up routine at 080020B8 matches all 708 bytes with the `old`
profile. Two things were left after deep-h. (1) The five-byte row copy is a
count-up index loop, `g_03005FA0[i*5+j] = g_08020C04[i*5+j]`; the destination
address is expanded first, so its base is hoisted first (pool order), while the
loop optimiser reverses the inner loop and reduces both addresses in source
order. Pointer forms tie the two orders together and cannot match. (2) GCSE's
PRE hoisted the outer `i + 1` above the inner loop. Its LCM (`lcm.c`) treats
every delayed block as latest, so an increment after an inner loop that does
not touch `i` is always moved to the end of the block before that loop, unless
the increment's own block is "isolated" on every path to the exit. The original
reuses `i` for the following clear loop (`for (i = 0; i <= 5; i++)
g_030001E0[i] = 0;`): the new `i = 0` makes the next `i + 1` latest there, the
outer latch becomes isolated, and PRE leaves the increment at the latch.
Earlier matches that hoist the increment (08015C2C writes `next = i + 1`) are
the other side of the same rule: which counter a later loop reuses decides
where an outer increment lands.

The number-to-text routine at 08010910 matches all 320 bytes. Its last
difference was the `g_03002E58 = 0` store: the original materialises a fresh
zero in r0, while a literal `0` joins the CSE class of the `emitted = 0` flag
initialised at the top and is stored from the flag's register (cse2 merges it
even when a block boundary stops the first CSE pass). A value that is always
zero but that only combine can prove (here `(u8)x >> 8`) reaches combine
after both CSE passes, folds to a fresh constant there, and gives the
original code; with it the earlier `do {} while (0)` workaround is no longer
needed, and removing it also fixes the r2/r3 choice for the record base. The
exact original expression is unknown; any of several combine-only zeros
(narrowed shift of a parameter) produce the same bytes.

The palette effect routine at 0800EDF4 (530 bytes, with its 18-way switch
table) matches. Two changes to the deep-c draft: the channels are read with
three separate halfword reads, `red = *(u16 *)((i << 1) + base) & 31` and so
on, which CSE merges into one load with the `lsls #16` unpacking and two
separate `#31` constants (the 08015128 idiom); and the destination is a
pointer computed into a variable before the colour is packed,
`dst = (u16 *)((i << 1) + base); color = ...; *dst = color;`. With a
function-level `address` variable the shifted index outranks nothing and the
three channels rotate registers; with the late CSE temporary plus `dst` the
original order (address r2, blue r3, green r4, red r5) falls out.

The per-frame camera routine at 0800BBD4 (492 bytes) matches with the
deep-h `combine_regs` rule applied twice. In both camera blocks the target
writes `muls rV, rS` into the loaded table value and then shifts into a
different register, so each product goes into its own function-level
variable shared by the two blocks (`t1 = g_083D2280[a] * scale; dx = t1 >> 12;`
and likewise `t2` for `dz`): a multi-block product is not tied to the shift
result, and the dying table value is tied to the product instead. In the
second block the `0x3FFF` mask sits in a block-scoped variable set before the
angle subtraction, which loads it first and pushes the record base to r5.

The title-menu loop at 08012A50 (632 bytes) is a sibling of 08012CC8 and
matched by editing that routine's source: a different draw callback, two more
calls, the cursor wrap (`if (--g_030021D8 > 5) g_030021D8 += 6;` and the
mirror for the other key) and the screen-base select. The select must be a
conditional expression with the zero test first,
`g_03000DFC = g_03005FC0 == 0 ? 0x0600A000 : 0x06000000;`; the plain `?:` on
the flag inverts the branch, and an if/else with two stores moves the pool
into the loop. Matched siblings are the fastest start for unmatched ones.

The name-entry screen at 080130BC (1,240 bytes) is the third member of the
title-loop family and was written from scratch on the 08012CC8 template:
the same DMA macros and per-frame calls, a five-way cursor over a 39-cell
letter grid (`g_030014B4`), a six-letter name buffer with backspace, the
"PLAYER" default and two name checks after the loop. The first compile had
only a four-register rotation of long-lived values (frame counter, name base,
the constant 32, key address). The counter wins r7 in the original because
the same variable `i` is reused after the loop to count non-blank letters;
the extra references raise its priority above the hoisted name base.

The mode menu at 08013594 (1,444 bytes, two ten-way switch tables) is the
fourth member of the family. It takes a starting mode, draws per-mode text
(two blinking options in modes 0 and 2), handles keys or timed callbacks per
mode and loops while the chosen next mode equals the current one; modes 1, 3,
8 and 9 restart the screen, the others return. It matched once the case
labels were written in the order the original emits them, 0, 1, 8, 9, 2, 3,
in both switches; the identical tails of cases 0 and 2 are merged by
cross-jumping, so the shared draw code appears only once.

Checks that resolved slice j, in the order to try them: (1) look for a
matched sibling and start from its source (four of seven); (2) read the case
order of a switch from its jump-table targets; (3) when an increment, zero or
product sits in the wrong place or register, ask which variable the original
shares or reuses (an outer counter reused by the next loop, a frame counter
reused as a count, products in their own multi-block variables), because
that decides PRE isolation, local-alloc ties and global priorities; (4) a
constant that the original rematerialises next to a register known to hold
the same value came from an expression only combine can fold.

## Deep slice l

The sound stream mixer at 08006270 (356 bytes with pools) matches standalone
with the `old` profile. Two source details decide it. In the first loop the
channel's sample index is read through a block-scoped pointer to
`g_030079D0[ch]` and the record table through a second pointer to its +16
limit word (`ch`, known to be zero there, is still written). Those shapes make
loop.c hoist the four address constants in the original order: buffer, index
pointer, limit base, then the step global in the second pass after the
strength-reduced buffer pointer. In the two halving loops the mixing temporary
`v` is one function-level variable, so it is allocated globally rather than per
block; its priority (refs 8 over a longer live range) then falls between the
two strength-reduced buffer pointers, which gives the original's r1 for `v` in
both loops and r0/r2 for the pointers. Writing `v >>= 1` as its own statement
sets that live length; the earlier one-expression form left it too short.

Outcomes for all 41 entries of this pass, the improved drafts for 0800B3A0 and
080162F8 and their diagnoses are in [deep-l/OUTCOMES.md](deep-l/OUTCOMES.md) and
[DEEP-L-SHIP.md](DEEP-L-SHIP.md).

## Deep slice j, third pass (j3)

The point plot at 0800B3A0 (310 bytes with pools) matches standalone with the
`old` profile. Deep-l's draft already matched except the odd-x branch, whose
block holds exactly three local quantities (x >> 1, the y * 240 chain with the
address tied to it, and the loaded byte). local-alloc's hand-written
three-element sort compares fixed quantity numbers, so the first-born x >> 1
always wins r0 there. In the original the pixel value is one function-level
variable `v` used by both parity branches (`v = *p; v &= 0xFF; *p = v;` and
the same with 0xFF00). That makes `v` a global pseudo, leaves two local
quantities in the odd block, and the two-element sort then gives the longer,
busier y * 240 chain r0 as in the original. Rule: when a block's register
order looks impossible for local-alloc, count its local quantities; a value
shared with a sibling block removes one.

The track-position update at 0800C850 (372 bytes) matches with the `old`
profile on the 0800C9C4 template. The dead `adds r0, r7, #1` that earlier
rounds could not explain is a second wrap, `after = next + 1; if (after >=
g_03002E4C) after = 0;`, whose result is never used: flow deletes the dead
`after = 0` but keeps the add because the compare reads it, and the
post-reload jump pass then removes the empty compare-and-branch. Other details:
record fields indexed directly (no record pointer, so the base constant is
loaded before the multiply), the x field address taken before the row base
is read, the row address written as `at * 28 + base` (so the sum ties to the
product as in the original), and the cosine read inline in both rotations
after the sine is held in a variable. `TxraRecord` gains the signed halfword
`field_42` (layout unchanged).

The stat scaling routine at 0800A940 (764 bytes) matches with the `old`
profile. Three source shapes decide it. The per-racer stats are a
two-dimensional `s16 g_030046E0[][10]` array: an element address then folds to
`index * 20 + (base + offset)`, which CSE leaves as the original's per-field
`base + offset` add, where a struct field collapses into one record pointer
with immediate offsets. Each update `field += field * 32 * (coefficient *
factor) / 100 / 32` keeps its product in one function-level temporary that is
loaded, shifted, multiplied and divided in place; this puts the frame (index
and the model row offset spilled to the stack) and every global register in
the original places. The third factor is built in two statements through a
block temporary (`t = third - 4; third = g_03000B60[20] + t;`) so fold cannot
move the `- 4` onto the last byte, and the fourth factor is a block temporary
computed before the update.

Its sibling at 0800AC3C (784 bytes) matches with the same update macro. The
grade is read through `p` before the divide (`p = field_62; grade = p / 32;`),
which reproduces the original's copy ahead of the rounding compare, and the
two level factors (`/ 16` for the first five stats, `/ 64` for the rest) are
separate variables. As one variable the factor outranks the row, index and
base registers and lands in r5; as two it is allocated after them, in r8,
which adds the original's `mov r1, r8` before every multiply (36 bytes).

The race HUD bar routine at 0800A17C (1,096 bytes) matches from deep-a's
retained draft with three changes. The record halfword at 0x4c is a
`TxraRecord` field (`field_4c`, layout unchanged), so its address is formed
from the CSE'd record base like the original. The last two bar rows compute
the next destination row before the first copy. Both bonus stores take their
value from a temporary before the destination address is loaded
(`t = g_08020904[...]; g_030014C0 = t; g_030014A4 += t;` and a zero held in a
block variable): with the address loaded first, a local pseudo sat in r3
across the PRE reaching register for the record base, which then could not
share r3 and cost a copy.

The steering and heading update at 0800C3C4 (1,164 bytes) matches from a
rewrite of deep-c's candidate. In order of effect: the two `field_44` flag
tests are nested ifs (as one `&&` condition fold merges them into a single
`& 48` test); every block opens with a direct `g_03001E60[slot]` access, so
the record base is loaded before the index multiply; each block has its own
record pointer variable (the first lives only between calls and gets r2, the
later one is live across `func_08014614` and gets r7; one shared pointer is
forced into a callee-saved register everywhere); and one `diff` variable
carries both angle differences, the steering decay step (`diff = steer >> 2;
if (steer) steer -= diff;`) and the tilt, with `diff <<= 3` as its own
statement. `TxraRecord` gains the offset-named fields at 0x30, 0x3a, 0x3e,
0x40, 0x44, 0x4e and 0x54 (layout unchanged).

The menu sprite builder at 08005238 (2,628 bytes, the largest routine matched
so far) comes from deep-a's draft with four changes. The draft's hand-made
`offset += 2` variable does not exist in the original: the column table is
`u16 g_080213A4[][5]` and both `item[i]` and `g_080213A4[count][i]` use
`i * 2`, which gives loop.c two uses of the same giv. With one use its
benefit (2, lifetime 3) is "not worth while" against the 1,019-insn loop;
with two it is reduced to the stack slot the original keeps, initialised after
the duplicated exit test. `slide + 120` is written inline after the loop
(no `selected_y` variable): GCSE's PRE then inserts it in the loop entry
block before the compare, exactly where the original computes it. The three
`func_08005C7C` results share one function-level variable; the cursor column
is read through block temporaries (table, then selection, then count); and
the cursor sprite's source goes through the `source` variable.

Slice j3 accounting, retained drafts (0800841C, 0800BDC0) and the remaining
entries are in `docs/DEEP-J3-SHIP.md` and `docs/deep-j3/OUTCOMES.md`.

The palette fade by track tile at 0800841C (452 bytes) finishes the j3 draft.
The tile byte of all three range blocks and the blue channel of both fade
loops are one function-level variable. With separate variables the third
block's byte inherits the r0 preference of the record base copy, which dies in
that block's address sum (preferences are merged along every dying register),
so it lands in r0. Shared with the loop channel, which is live while the
green channel sits in r0, the variable conflicts with r0 and takes r1 in every block
and both loops, like the original.

The AI lane choice at 0800BDC0 (1,540 bytes) finishes the other j3 draft. The
angle delta is the loop counter `i` (sharing gives it r5 in global allocation,
so the index product is left with r8); the lane timer is incremented and
masked in two statements (one statement narrows the 511 mask to HImode and
reload copies it); the steering flag clear casts `field_44` to `s16` so the
mask stays `-2`; the first neighbour loop compares the other car's
`field_42`, not `field_48` (a draft error). Last, the final `else if (A || B)`
of the lap-time chain is two `else if` branches with the same store. That
shortens the live length of the `g_03001E60` base copy from 190 to 186
insns, so its allocation priority (1,935) now beats the index product's
(1,904); the base is allocated first and takes r6, leaving r8 for the product
as in the original.
