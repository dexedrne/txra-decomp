# Control-flow comparison, 12 November

This pass starts from the actual retained 11/11 HUD candidate: 3,152 differing
bytes, 4,124 total bytes and a 36-byte local frame. The older numbers in the
brief do not describe that source. The comparison end remains 08005238 and the
profile remains the historical Thumb compiler with `-O2 -mthumb-interwork`.

The raw import uses ARM:LE:32:v4t, APCS, and load address 08000000. The 237
registry entries supply exact code spans and instruction modes; pool gaps are
excluded from disassembly. The HUD common return is joined in the private
database, with its internal long transfer interpreted as a branch. Those
analysis overrides change no input bytes or public function boundaries.
Uninitialized writable memory regions and volatile hardware are explicit.
The project and exported views stay in the private cache outside the repo.

| Area | Observed shape and comparison with our C |
| --- | --- |
| Loops and selection | Four/two-item countdown strips, six-character upward text, a three-by-two gauge loop and eight-record map/flash/smoke loops agree with our candidate. Gear/model and glyph choices are independent tests, not switch tables. |
| Fields | Cars use 100-byte records, geometry rows use two 12-byte triples, and flash/smoke records use four words. Our declared strides agree. Recovered addresses do not independently establish the original source type names. |
| Projected coordinates | The first x/y pair is captured before its width guard; the second pair is captured after the first draw and before the second guard. The second width survives the first draw, and a sprite tag survives both draws. Our current candidate captures coordinates inside the guards and shares width/scalar roles with earlier phases. Test captures and separate, nonoverlapping lifetimes without caching scratch across transforms. |
| Flash | The active flag and x field use a cursor while y and the clamped size use an index. Our candidate indexes all four fields. Test a cursor/index mixture and a short-lived size-field address. |
| Smoke | Allocation mixes four field cursors and a byte offset. Rendering carries count and z cursors, indexes x, and retains a y-field address through the helper calls. The allocation shape is already present; rendering still indexes everything. |
| Scratch and calls | Source triples are written before four ordered transforms; each projected draw scales first. Smoke allocation follows both transformed groups, then rendering performs one transform per active record. Our source keeps that order and the six shared scratch aliases. The transform helper writes those aliases; treating it as pure would be wrong. |
| Shared locals | The view reuses three stack words across unrelated phases. Its names represent optimized storage, not proof that the original C reused a particular identifier. Candidate role changes must preserve simultaneously live widths, coordinates and tags. |

The scale helper writes the affine matrix and two global offsets, while the
sprite helper queues transfers and writes sprite attributes. Neither is
assumed to preserve arbitrary aliased memory. The notification helper calls
the sound path only under its enable flag. These are static observations,
not execution evidence. The unchanged C fixtures remain a regression check;
complete byte equality and every whole-ROM gate remain required to install.

The other comparisons are [contact rotation](CONTACT.md), [complete streaming
geometry](STREAM.md) and [the ARM renderer](ARM.md). The stream continuation is
joined only in the private analysis database; neither public registry boundaries
nor original bytes change. The ARM reports distinguish reliable control flow
from the optimized view's unresolved stack aliases.
