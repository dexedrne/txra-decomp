# Local toolchain

Run `bash tools/setup.sh`, then `make`. No root access or system changes are required.
The default prefix is `~/opt`; override `TXRA_TOOLS` for setup/Python tools and
`TOOL_ROOT` for make. Prerequisites: x86_64 Linux, Python 3, curl, tar/xz, git,
GNU make, and a host C compiler. The setup script uses a venv without ensurepip
and bootstraps pip if the host Python omits it.

| Component | Exact version / revision | Purpose |
| --- | --- | --- |
| Arm GNU Toolchain | 14.3.Rel1, GCC 14.3.1 20250623, build arm-14.174 | preprocessing, assembler, linker, objcopy, comparison compiler |
| GNU binutils | 2.44.0.20250616 | ARM7TDMI assembly and binary output |
| pret/agbcc | da598c1d918402c42c0c0d7128ba14567f3175e9 | historical `old_agbcc`, `agbcc` and `agbcc_arm` (matching compilers) |
| Historical compiler banner | gcc 2.9-arm-000512 for Thumb/elf | matching C backend |
| Capstone | 5.0.6 | instruction decoder used by our CFG tooling |
| pip | 26.2.2 | isolated dependency installation |

The Arm archive's SHA-256 is
`8f6903f8ceb084d9227b9ef991490413014d991874a1e34074443c2a72b14dbd`.
Setup verifies this before extraction. No compiler binaries or upstream compiler
sources belong in this repository. The matching build uses all three agbcc
variants that setup builds: `old_agbcc` for 179 functions (177 of them with plain
`-O2 -mthumb-interwork`), `agbcc` for 4 and `agbcc_arm` for 8 ARM functions. The
Arm toolchain's GCC 14.3 compiles the remaining three 4-byte ARM branches. The
profile of each function is recorded in `tools/rom.cfg`.
The bootstrap pip script is retrieved over HTTPS; it is not itself pinned.

Sources: [Arm release distribution](https://developer.arm.com/-/media/Files/downloads/gnu/14.3.rel1/binrel/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi.tar.xz),
[pinned compiler sources](https://github.com/pret/agbcc/tree/da598c1d918402c42c0c0d7128ba14567f3175e9),
[Capstone Python API](https://www.capstone-engine.org/lang_python.html).
