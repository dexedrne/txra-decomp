# Round 9: assigned angle and queue study

No new complete replacement. The assigned angle at 08014614 was installed before
this pass and passes a fresh, uncached 88-byte comparison against its next entry.
The queue at 08015DA8 is the only remaining unmatched entry in these named drafts.
The immediate mapped queue neighbors and the older 0801466C draft are already
installed. Packet, blit and other families were left for the concurrent job.
The five-addition target is not achieved.

## What the C changes do

The starting queue has eleven differing instructions and eleven differing bytes.
Its word source, length, operation shapes, constants and embedded pools agree.
The transfer destination gets r0 while the shared address/mask scratch gets r2.
The old compiler's local allocator handles single-block, single-death values
before its global allocator; merely reordering declarations does not resolve this.

Reusing destination/count values for earlier addresses gives a seven-instruction,
seven-byte miss with identical instruction shapes. Assigning the destination from
the source in the empty-queue branch changes its allocation across blocks, leaving
a four-instruction, nine-byte miss. Because that branch establishes source == 0,
the compiler materializes zero rather than retaining the target's source-register
store. That extra instruction replaces alignment padding, keeping the full extent
at 118 bytes. The DMA readback still targets r1 instead of r0. The first 36 bytes
and last 33 bytes agree. This best-by-distance draft is retained in near-misses/;
queue-lifetimes/ retains the simpler seven-instruction alternative.

Both are hypotheses, never accepted replacements. Four instruction edits is not
four bytes, and neither approximation is included in progress totals.

## Reproducing searches

`tools/targeted_search9.py --grid NAME --jobs 4` runs lifetime, coalescing, tails,
helpers, pointer-work, setup-reuse, dead-parameters, control and zero-branch grids.
Use the historical round-7 queue seed; dependencies on retained best sources are
explicit in the script. Most passes use old; pointer-work and control also measure
standard and old-no-gcse. Every result records consumed trials, not unique output.
Complete equality, not the approximate distance, is the acceptance gate.

The two earlier focused passes use `tools/variant_search.py` with a 120-second
limit, four workers and focus `work|dest|count|addend`, first on the round-7 queue,
then on queue-lifetimes/. The final pass uses the four-instruction seed and focus
`dest|work|count|source`. Their individual manifests retain actual consumed counts.

queue-setup-declarations-rejected/ preserves an initial grid with 1,134 rejected
trials: assignments were interspersed with declarations unsupported by the old C
parser. The corrected setup-reuse pass moves declarations before assignments and
fixes pointer declarator parsing; all 1,143 trials compile. No rejection counts
as matching progress. The coalescing and dead-parameter grids also include parse
rejections, recorded in their manifests.

The preliminary queue-update-reuse grid measures 72 combinations of cursor,
offset or index update; destination, count or scratch temporary; four readback
forms; and before/after-store placement. These are speculative syntactic trials;
some overwrite still-live values and are not semantic replacements. Its count
and the 96-trial initial zero-branch pass did not record error totals. The retained
sources and diffs remain inspectable; missing counts are not invented as zero.
The standalone uncached angle check is accounted separately from queue trials.
No service, external matching checkout or matcher process was accessed.

## Earlier successful transformations retained

The authoritative thirteen-family table remains tools/matching_patterns.json.
No new transformation is promoted to proven evidence in this pass.

| Earlier accepted evidence | C transformation | Why retained |
| --- | --- | --- |
| 08013B38, 08013C08 | Integer cursor before typed pointer | Initial address register identity |
| 08018B24 | Scale stack offset before adding address | Addition operand order |
| 0801466C | Explicit global cursor, ordered loop setup | Loop offset and sink allocation |
| 08014614 | Direct short returns, wide tail, distributed offsets | Narrowing and branch sharing |
| 0801251C, 080123F0 | Structured backedge and direct mask/zero tests | Tag load order and saved register |
| 0801251C | Named addition input | Arithmetic operand order |

See summary.json for aggregate measured trials and docs/MATCH9-SHIP.md for final
validation. No extra compiler profile or approximate function was installed.
