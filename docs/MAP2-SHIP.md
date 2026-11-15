# ROM mapping handoff

Implementation commit: `c1f8c9c` — whole-image pointer discovery, coverage logging,
typed data classification, exact board progress, review tools and regression
checks. The following handoff commit adds this note and `MAP2-DONE`. No push,
deployment, merge or stash was performed.

The ROM is now 33.88% classified, up from 2.03%. Code is 85,132 bytes (2.03%);
data including fill is 1,336,039 bytes (31.85%); 2,773,133 bytes (66.12%) remain
unknown. The candidate inventory has 229 functions, 205 THUMB and 24 ARM, with
14 jump tables. The code increase is the 36-byte previously observed IRQ
epilogue, now integrated into the main inventory. Scanning pointers throughout
all 4 MiB did not establish more executable regions. This is not a claim that
every possible function has been found.

`tools/rom.cfg` contains a complete nonoverlapping partition with offset, size,
type and format for each block. Data includes 504,914 audio bytes from custom
sample descriptors and declared PCM extents, 99,656 graphics-transfer bytes,
20,712 table/literal bytes, 28,005 text bytes, 122,281 fill bytes and 560,471 other
read/header/transfer bytes. Code and known structures override weaker evidence.
Interior zero regions are not assumed to be padding. No valid referenced BIOS
compression block was established; the LZ77/RLE/Huffman source scanners are
covered by synthetic tests. Their presence does not implement previously
unsupported decompression services in the game runtime.

The optional `--coverage` mode records unique guest PCs/modes, computed branch
edges, exact ROM read bytes, and aligned DMA/CpuSet source extents. Capture files
carry the ROM fingerprint and fail explicitly on record-capacity exhaustion.
All six final captures together contain 23,317 executed PCs, 3,576 branch edges
and 915,933 read ROM bytes. Each observed execution PC is in the static map or a
unique established copied-code alias. Eleven indirect sites remain unresolved:
register-call veneers not executed by these inputs.

Six deterministic final coverage scenarios exercise boot, name entry, car
purchase, Quest, Quick Race, Time Attack, Free Run, Change Car, Parts Shop,
options including records and controls, save/reload and a complete battle-race
loss. Inputs and isolated save paths go through normal hardware input; no game
memory or ROM data was patched. Save creates the isolated EEPROM backing file;
reload makes no writes and preserves its hash. Root screens are covered, not
every submenu, car, part purchase, course or career outcome.

Validation:

- `make check`: 26 passing Python tests, including 15 focused mapping/logger tests
  and the additive-descent regression. The matching build passes its full ROM
  SHA-1 check and byte-for-byte equality check.
- `make recomp`: 229 functions emitted, 260 load/run entries. The final executable
  is the same exact executable used by the recorded scenario evidence.
- `make check-runtime`: 118 assertions pass. Controller checks pass for ten
  buttons, dead zone, diagonal input, disconnect and reconnect.
- All six coverage scenarios report zero fallback steps, unknown execution
  targets and unsupported instructions, without logger overflow.
- The full race executes 1,170,372,096 native instructions. A second full race
  with coverage disabled matches all 12,500 framebuffer hashes and every final
  machine/audio/stat field apart from elapsed host time. Both have zero fallback.
- An ordering bug found during verification was repaired: the analyzer drains
  static recursive descent before considering uncovered observed PCs. Seeding
  already-known PCs leaves all assembly and inventory outputs identical.

Private final evidence is under `build/map2/final/`; raw logs, saves, generated
translation and the player-owned ROM remain ignored. Persistent review media
contain our tools only, with no game pictures, extracted assets or ROM payload.

Review folder: `txra-review/map2/`.

- `before/rom-heat-strip.png` and `after/rom-heat-strip.png`: identical viewpoints
  of the whole ROM, coloured by classification, with unknown areas dark.
- `mapped-progress.png`: exact code versus data/fill percentages before and after.
- `map-progress.webm`: metadata-only before/after replay; muted VP9, six seconds,
  30 fps, 497,555 bytes. This is a tool visualization, not gameplay footage.
- Each media folder has plain `NOTES.md` and a caption for every picture/clip.
  All three final pictures and clip contact frames were visually inspected.

What is not done: full-ROM classification, proof of every function and target,
exact track/course layouts, complete song/voice sequence layouts, discrimination
of every 4/8bpp tile/bitmap/tilemap/affine/sprite block, unknown compression and
all courses/career paths. Observing a byte does not establish the full extent of
its neighboring asset. These unknowns stay visible in the config, progress and
review pictures; they were not relabeled wholesale as data. The game's existing
layout issues, hardware timing limits, audio fidelity and physical controller
validation remain outside this mapping change.

Owner notes: `OWNER-NOTES.md` was absent at the initial read, each major step,
and final handoff checks. There were no appended notes to resolve. The requested
review notes, captions, muted clip, private-ROM handling, additive save behavior
and commit identity were followed. No browser or external capture machine was
used; no vehicle, world or original model work was performed.
