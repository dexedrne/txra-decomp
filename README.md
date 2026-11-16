# txra-decomp

A matching decompilation of **Tokyo Xtreme Racer Advance** for the Game Boy Advance (game code BTZE): C and ARM/Thumb assembly source that rebuilds the original 4 MiB cartridge image byte for byte. The repository also contains a static recompiler that translates the game's original machine code into a native PC program ([status below](#native-recompiler)).

**Status: complete by the project's [definition of done](docs/FINISH.md#definition-of-done).** All 228 entries in the function map are done. 194 functions are written in C that compiles to the original bytes, covering 92.9% of the mapped instruction bytes. 31 documented routines stay assembly by design (7.1%), because each depends on a machine property that compiled C does not produce. The other 3 entries are labels inside C functions. The rebuilt ROM is byte-identical to the original: SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487`.

<!-- progress:start -->
**194 of 228 functions** match the original compiler output byte for byte (85.1% of functions). In mapped instruction bytes, the exact C owners cover **92.9% of the game code** (79,486 of 85,578 bytes).

`█████████████████░░░` functions   `███████████████████░` code

_The rest of the 85,578 instruction bytes is documented assembly (6,092, 7.1%). No C owner remains: every one of the 228 entries is complete (194 exact C, 3 labels inside installed owners, 31 documented assembly interfaces). Counting literal pools, the 194 replacements hold 93,542 bytes, more than the mapped instruction bytes, so the pool-inclusive ratio in `progress.json → functions_matched_c` (109.3%) mixes two units and is not used here. See [the finish tracker](docs/FINISH.md)._
<!-- progress:end -->

## What "complete" means

The function map has 228 entries (204 Thumb, 24 ARM). An entry counts as done only if it is one of three things ([definition of done](docs/FINISH.md#definition-of-done)):

1. **Exact C.** The whole function, through the end of its literal pool, compiles to the original bytes with one of the registered compiler profiles, and the full ROM rebuilt with it keeps the original SHA-1. No padding, inline assembly, hand-placed bytes or checker exceptions. 191 of these functions are built with agbcc's GCC 2.9-era compilers; three 4-byte ARM branches are built with a modern GCC (see the caveats below). **194 entries.**
2. **A label inside an exact C function.** A secondary entry point whose bytes come from its installed owner. **3 entries.**
3. **A documented assembly interface.** A routine listed in [`docs/map/finish.json`](docs/map/finish.json) together with the machine property that rules C out. [`tools/asm_interfaces.py`](tools/asm_interfaces.py), a separate audit tool that is not part of `make`, re-measures that property from the ROM each time it runs and fails if it no longer holds. These are reported as assembly and never counted as C. **31 entries, 6,092 bytes.**

`progress.json → completion` reports exactly these classes and reads 228 of 228.

**Why 31 routines stay assembly.** None of them is ordinary compiler output:

| Group | Routines | Bytes | What no compiled C function does |
| --- | ---: | ---: | --- |
| Renderer and rasterizer routines (copied to and run from IWRAM) | 8 | 5,548 | Private register contract: reads fp, r6–r8, sb and sl before defining them, uses lr as a general register, XOR-swaps registers, stores below sp, saves ip without an APCS frame |
| Reset and interrupt handling | 3 | 336 | Processor mode changes and banked stacks through MSR/MRS |
| Division runtime | 2 | 168 | Frameless division routines built on flag-predicated instructions (library origin provisional) |
| BIOS call wrappers | 2 | 8 | `svc` (CpuSet, CpuFastSet) and return |
| Register-call and state-switch veneers | 16 | 32 | libgcc `_call_via_rN` (`bx rN`) and `bx pc` stubs |

Each routine's measured evidence is in [the tracker](docs/FINISH.md#tracker-every-entry-without-its-own-exact-c).

**Is the map itself complete?** [`tools/map_completeness.py`](tools/map_completeness.py) decodes all 37,704 mapped instructions: every call, branch and resolved indirect transfer lands on mapped code, and the 11 indirect sites it cannot resolve are libgcc veneers with no references that never ran in any recorded coverage session. The 719,264 bytes that remain untyped show none of the code idioms found in the mapped code (no BL pair that hits a function entry, no return sequence), and 13 recorded coverage sessions, including a 12,500-frame race, executed nothing outside the map. This is a bounded static and coverage verdict, not a proof: it cannot exclude an unreferenced sequence that uses none of the measured idioms, or code inside a compressed block that no measured path decodes ([evidence and limits](docs/FINISH.md#map-completeness-evidence)).

Two smaller caveats. Four tiny entries counted as C (14 bytes: the reset branch, a `bx lr` and the ARM halves of two veneers) are startup or libgcc assembly in origin whose C form compiles to the same bytes; three of them are the 4-byte ARM branches built with GCC 14.3. Functions keep their address names (`func_08016DA8`); naming and typing the data are not part of the finish definition.

## Building

### What you need

- **Your own cartridge image.** Dump your own copy of the game and place it in the repository root as `baserom.gba`. It must be the 4 MiB BTZE image with SHA-1 `4197339d4add74bb40ed02a8fba5e58096afb487` (check with `sha1sum baserom.gba`). The build reads every data region from this file; none of it is committed.
- x86_64 Linux with Python 3, GNU make, git, curl, tar/xz and a host C compiler.
- The toolchain below. `bash tools/setup.sh` downloads, verifies and builds it without root. The default prefix is `~/opt`; override it with `TXRA_TOOLS` for `setup.sh` and `TOOL_ROOT` for `make` ([details](docs/TOOLS.md)).

```
~/opt/
├── arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/   assembler, linker, objcopy, preprocessor (archive SHA-256 checked);
│                                                       its GCC 14.3 also compiles three 4-byte ARM branches
├── agbcc/                 pret/agbcc at da598c1, built in three variants:
│   ├── old_agbcc          179 functions (177 with plain -O2 -mthumb-interwork)
│   ├── agbcc              4 functions (-O2 or -O1)
│   └── agbcc_arm          8 ARM functions
└── txra-venv/             Python virtual environment with capstone 5.0.6
```

### Commands

```
bash tools/setup.sh
make          # ends with: build/txra.gba: OK
make check
```

| Command | What it does | What it shows |
| --- | --- | --- |
| `make` | Compiles the 194 C functions and compares each with the original bytes (`tools/match.py`), regenerates the assembly listings and the code/data split from `tools/rom.cfg` (`tools/analyze.py`), assembles and links `build/txra.gba`, and checks it against `txra.sha1`. | The source rebuilds the cartridge image byte for byte. The build stops at the first function that differs. |
| `make check` | `make`, then the Python test suite (279 tests). | The mapping, matching, relocation and bookkeeping tools behave as specified. |
| `make clean && make check` | The same from an empty `build/`. | Nothing depends on stale output. |
| `make recomp` | Generates C from the ROM's machine code (`recomp/generate.py`), links it with `runtime/` into `build/txra-pc`, and refreshes `progress.json`. | The native recompiler emits and compiles every mapped function. |
| `make check-accuracy` | Builds `build/txra-pc` and runs a scripted 4,300-frame session (`tests/race-input.txt`) headless. | Every framebuffer hash, every PCM audio byte, the final machine state and the sample clock equal a recorded reference, with no fallback or unknown instruction. The reference is an earlier recording of the same runtime, so this is a regression lock, not a hardware comparison. |
| `make check-runtime` | CPU and hardware-model assertions (446). | Instruction semantics and the hardware model hold. |

Other targets: `make analyze` regenerates the assembly and JSON inventories, `make drafts` writes readable pseudo-C lifted by the recompiler (build output, not committed), `make check-mapping`, `check-desktop`, `check-controller`, `check-touch`, `check-career` and `check-cpu-reference` cover the coverage tools, the PC build and the iPhone touch controls, and `make code-audit` writes metadata-only code-discovery proposals for review.

## Repository layout

| Path | Contents |
| --- | --- |
| `src/` | The C source: one file per function in `src/generated/` (`func_<address>.c`), the compilation unit `unit_08005C7C.c`, which compiles seventeen sound routines in ROM order (08005C7C–0800622A and 08007398; 08006070 matches only that way), four small routines in `leaves.c`, and shared types in `types.h`. |
| `asm/` | `rom.s` and the listings it includes, written by `tools/analyze.py`: assembly for the 31 interfaces, an `.incbin` of each compiled C function, and `.incbin` slices of `baserom.gba` for data. |
| `tools/` | `rom.cfg` (the byte-exact ROM partition, the registered C functions with their compiler profiles, reviewed boundaries) and the build, matching, measurement, audit and review scripts. `tools/ios/` builds the iPhone app. |
| `recomp/` | The static recompiler (`generate.py`), the pseudo-C lifter (`draft.py`) and reviewed observed transfer targets. |
| `runtime/` | The native runtime: ARMv4T semantics and fallback interpreter, GBA memory and hardware model, SDL2 desktop shell, input, audio and EEPROM saves. `runtime/ios/` is the iPhone shell (touch controls, ROM finder, app lifecycle). |
| `tests/` | Python unit tests, C tests for the runtime, controller and desktop layers, scripted input files and golden hashes (metadata only). |
| `docs/` | The finish tracker, map, compiler and hardware notes, machine-readable inventories in `docs/map/`, a note for every matching round, and retained near-miss sources in `docs/near-misses/`. |

Good starting points: [FINISH](docs/FINISH.md), [MAP](docs/MAP.md), [COMPILER](docs/COMPILER.md), [DECOMP](docs/DECOMP.md), [HARDWARE](docs/HARDWARE.md), [TOOLS](docs/TOOLS.md), [RECOMP](docs/RECOMP.md) and [PC-RUNTIME](docs/PC-RUNTIME.md).

## How it was done

The project started on 27 October 2026 from a build that wrapped the original ROM, matched its first four leaf routines the same day, and reached 228 of 228 on 15 November 2026.

1. **Map.** Recursive descent from the reset vector, pointer scans over all 4 MiB, switch-table bounds, DMA copy tracking (much of the ARM code runs from IWRAM) and coverage logs from the native runtime produced `tools/rom.cfg`: a partition of every ROM byte into code, data, fill and unknown, and the 228-entry function map ([map notes](docs/MAP.md)).
2. **Classify.** Each entry was sorted into C work, a label inside another function, or assembly with a measured reason.
3. **Match.** Each function was written in C and compiled with agbcc, which preserves the GCC 2.9-era compiler family the original code is consistent with; the exact original release and flags are not proven ([compiler evidence](docs/COMPILER.md)). `tools/measure_candidate.py` compares a whole candidate with the original: length, stack frame, differing bytes and instruction edit distance. A function is installed only when it is exact and the complete ROM still rebuilds with the original SHA-1. Some matches depend on more than the function itself: 08006070 matches only when compiled after its ROM neighbours, because the compiler numbers literal-pool labels across the whole file and its CSE pass hashes those names ([matching notes](docs/DECOMP.md)).
4. **Finish.** The last large functions were close to the original but still differed, mostly in register allocation, scheduling and loop structure. The finish passes of 14 and 15 November closed them; the later passes traced the compiler's scheduler and register allocator with diagnostic builds of its `cc1` to find the source shape that produces the original choices. Every installed source compiles with the unmodified compiler. Finish pass 2 installed the road stream owner 08002854 (6,456 bytes, last 23 differing bytes closed; [note](docs/FINISH2-1115-stream.md)) and the HUD owner 0800421C (4,124 bytes, a fresh rewrite from 3,144 differing bytes; [note](docs/FINISH2-1115-hud.md)). The last three:
   - **Contact, 080181C0** (ARM, 1,684 bytes, 158 differing bytes to 0). Reaching the probe array through a function-scope pointer keeps the compiler's strength-reduced pointer at full allocation priority, so it takes r6 ahead of the loop counter; reaching the two model-box tables through byte pointers keeps their bases out of the loop preheader's local allocation. [Note](docs/FINISH3-1115-contact.md).
   - **Sound, 080064A4** (Thumb, 3,828 bytes, 90 to 0). The note-start envelopes load into the same pointer as the envelope ticks, and one function-level temporary holds the fade gain, the effect stop flag and the slide pitch sums; with those shared variables, global allocation orders the registers as the original does. [Note](docs/FINISH5-1115-sound.md).
   - **Renderer, 08016DA8** (ARM, 4,288 bytes, 49 to 0). Copying the y offset into `saved_y` before the pitch rotation, as the exact sibling 08016C18 does, gives the first scheduling pass the extra step it needs to place a global load after the dy subtraction; global allocation then gives both variables one register, and the copy disappears from the output. [Note](docs/FINISH6-1115-base.md).

## Native recompiler

`recomp/generate.py` reads the original machine code from your ROM and emits C for every mapped function. Each instruction becomes a call to a pre-decoded semantic operation with constant operands; direct calls become C calls, and computed branches and returns go through a PC-to-function table. Code that the game copies to IWRAM is emitted at its execution address. An ARMv4T fallback interpreter handles anything outside the map and logs it. `runtime/` supplies the GBA side (memory map, scanline scheduler, DMA, timers, PSG and FIFO sound, keypad, EEPROM) and an SDL2 desktop shell with window scaling, fullscreen, a pause menu, keyboard and controller bindings, screenshots and per-user save files. The native build translates the original instructions; it does not compile the decompiled C.

```
python3 tools/build_pc.py /path/to/your/cartridge.gba
./build/txra-pc --rom /path/to/your/cartridge.gba
```

The PC build needs only a C11 compiler, make, Python 3, pkg-config and SDL2 development files. The executable ships no ROM or asset files: it reads the game's data from your ROM at run time.

**Prebuilt executables** for Windows (x86-64, Windows 10 1903+ or 11) and Linux (x86-64, glibc 2.34+, system SDL2) are attached to the [v1.1.0 release](https://github.com/dexedrne/txra-decomp/releases/tag/v1.1.0). They contain the game's program code translated to native code, but no ROM data, graphics, audio or text: to play you still need your own cartridge dump with the SHA-1 above, passed with `--rom` (or dropped onto `txra-pc.exe`). Each archive carries a player README and checksums.

`make package-pc` builds a reproducible Linux archive and `make package-windows` a Windows one (cross-built with MinGW-w64 and SDL2); both check that the executable embeds no ROM data. See [PC build and controls](docs/PC-RUNTIME.md).

**iPhone.** `tools/ios/build.sh` builds the same translated code into an iPhone app (iOS 15 or newer) on a Mac with Xcode. It produces an unsigned IPA: install it with a sideloading tool such as AltStore, SideStore or Sideloadly, which signs it with your own Apple ID (a free one works, but must re-sign every 7 days). The app reads your dump from its folder in the Files app (On My iPhone > TXRA) and has on-screen touch controls and controller support. Like the PC builds it contains no ROM data. See the [iPhone build notes](tools/ios/README.md) and the [player README](tools/ios/README-iOS.txt).

Status:

- The current tree emits and compiles all 228 mapped functions, and `make check-accuracy` passes: the scripted 4,300-frame session runs with no fallback, unknown or unsupported operation and reproduces its recorded framebuffer and audio hashes.
- On 15 November the current Linux executable passed `make check-career`: the 37,200-frame scripted career and the 2,200-frame save reload match every recorded framebuffer hash, PCM byte, state counter and EEPROM save, with no fallback or unknown operation (first reviewed on 6 November, [review](docs/NATIVE-RUNTIME-1106-REVIEW.md)). The Windows executable reproduced the same accuracy, career and reload hashes under Wine.
- The iPhone build, run in the iOS Simulator (iOS 27.2, arm64), reproduced the same career and reload frame hashes, PCM and save as Linux. It has not been run on a physical iPhone, and the touch controls and controllers have not been tried by hand.
- `progress.json` reports `boots`, `reaches_title` and `playable` as false. Those flags turn true only through a recorded review of the exact executable, and no such review has been done for the current build.
- Timing is approximate (three clocks per instruction, not cycle-accurate). Running on a real Windows PC, physical controllers, visible-window presentation and audible fidelity have not been verified. See [native execution](docs/RECOMP.md) and [PC runtime](docs/PC-RUNTIME.md).

## Legal

This repository contains no ROM image and no game assets: no graphics, audio, text or other data from the cartridge. The original program appears only as reconstructed C, as assembly source for the 31 interface routines, and as disassembly excerpts in the matching notes. Every data region is read from your own `baserom.gba` at build time, the native executable reads the game from your ROM at run time, and the metadata in `docs/map/` describes the ROM without reproducing it. Your own build outputs (`build/txra.gba` and the generated C) are derived from your ROM; keep them private. The prebuilt executables on the releases page contain the program's translated code but no ROM data, and run only with your own copy of the game. To build anything you need your own legally obtained copy of the game. Please do not post ROM data in issues or pull requests.

Tokyo Xtreme Racer Advance, Tokyo Xtreme Racer and Game Boy Advance are trademarks of their respective owners. This is an independent research and preservation project, not affiliated with or endorsed by them.

<!-- License: there is no LICENSE file yet. Choose a license and add LICENSE before publishing; until then no license is granted. -->
