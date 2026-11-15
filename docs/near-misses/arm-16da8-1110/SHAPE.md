# Renderer owner: decompiler-guided comparison

The best checked-in 11/9d profile reproduces at **3,251 differing bytes**;
the brief's 3,249 figure has no corresponding retained source/profile here.
All comparisons retain 08016DA8..08017E68 and the historical ARM compiler.

The private working project uses `ARM:LE:32:v4t`, cartridge base 08000000,
registry code spans and explicit ARM/Thumb context. The cartridge is read-only,
RAM is uninitialized and writable, and hardware registers are volatile. APCS
was also selected to fit the historical prologue. The exports and all
intermediate views remain outside the repository.

| Area | Observation | Candidate comparison |
| --- | --- | --- |
| Ring and face traversal | A wrapped ring loop surrounds a zero-kind-terminated face loop. Face stride is 56 bytes; the ring stride is 1,344 bytes. | The existing typed face cursor and wrap limits agree. An explicit terminal return compiles identically. |
| Near/direct split | Any one of four signed depths below 768 takes the subdivided path. | The existing four-way short-circuit condition agrees. Unsigned storage plus signed comparisons preserves word semantics. |
| Subdivision | Four parts are visited, skipping a negative corner depth. The geometry cases use independent equality tests. | The source already has four independent cases. The retained rewrite wraps near work in a positive depth predicate instead of an early continue. |
| Projection | The view exposes a vertex count, a word displacement, a byte displacement and a z-component cursor. Camera/offset z values survive the loop. | The source has one vertex index. Explicit mixed-unit traversal was measured, but did not improve the full owner and sometimes increased frame size. |
| Visibility and winding | A visible corner admits expansion/clamping, then nonpositive winding admits texture/packet work. | Positive nested predicates now express this shape directly. The generated owner is byte-identical to the starting candidate, not the cartridge. |
| Texture selection | The four parts form a ladder, with shared final-component stores on some paths. This is not an indirect switch table. | Ladder and common-tail variants were measured. They did not beat the existing independent-test source under the fixed profile. |
| Packet links | Near and direct insertion distinguish empty and nonempty bucket links. | The direct source already retains this branch. Restoring it in the near helper did not lower the owner distance. |
| Layout and calls | Points use 28-byte rows, faces 56-byte rows, and output packets 32-byte rows. The owner has no outgoing function calls. | Existing layouts and the inlined helper organization agree with those observations. There are no internal callees to export for this owner. |

There is a significant limit to the recovered temporaries: Ghidra's high-level
ARM view leaves the indexed corner-depth local apparently uninitialized while
using four scalar depth values elsewhere. The repository assembly plainly
stores those four depths before the indexed test. Naming the local as an array,
disabling array splitting/alias blocking, marking cartridge/RAM permissions
correctly, and selecting APCS did not repair that high-level join. The initial
p-code view retains the actual stores. This is a decompiler stack-alias recovery
limitation, **not evidence of uninitialized behavior in the cartridge**. No C
rewrite was taken from those missing assignments.

The reliable contribution here is the control-flow comparison. The 199-fixture
independent textual-instruction executor remains the semantic check, and exact
full-owner equality remains the installation gate. Neither decompilation nor
the source's closer visual shape supplies installation authority.
