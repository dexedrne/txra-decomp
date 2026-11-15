# Matching build for Tokyo Xtreme Racer Advance (BTZE). Needs your own copy of the ROM as ./baserom.gba (never committed).
include tools/local.mk
AS := $(ARM_BIN)as
LD := $(ARM_BIN)ld
OBJCOPY := $(ARM_BIN)objcopy
CC := $(ARM_BIN)gcc
all: build/txra.gba
	@sha1sum -c txra.sha1
build/rom.o: asm/rom.s $(wildcard asm/*.s) baserom.gba build/leaves/verified build/analysis.stamp
	@mkdir -p build
	$(AS) -mcpu=arm7tdmi -I. -o $@ $<
build/txra.elf: build/rom.o ld_script.ld
	$(LD) -T ld_script.ld -o $@ build/rom.o
build/txra.gba: build/txra.elf
	$(OBJCOPY) -O binary $< $@
clean:
	rm -rf build
.PHONY: all clean

analyze:
	$(PYTHON) tools/analyze.py
.PHONY: analyze

build/leaves/verified: src/leaves.c $(wildcard src/generated/*.c) tools/match.py tools/reloc.py src/types.h tools/rom.cfg baserom.gba
	$(PYTHON) tools/match.py

build/analysis.stamp: tools/analyze.py tools/inventory.py tools/rom.cfg baserom.gba
	$(PYTHON) tools/analyze.py
	@touch $@

check: all
	$(PYTHON) -m unittest discover -s tests -v
.PHONY: check

ROM ?= baserom.gba
HOST_CC ?= cc
HOST_CFLAGS ?= -O2 -std=c11 -Wall -Wextra -Wno-misleading-indentation
SDL_CFLAGS := $(shell pkg-config --cflags sdl2 2>/dev/null)
SDL_LIBS := $(shell pkg-config --libs sdl2 2>/dev/null)

build/generated.c: recomp/generate.py recomp/observed.json docs/map/functions.json tools/rom.cfg $(ROM)
	$(PYTHON) recomp/generate.py --rom "$(ROM)"

build/generated.o: build/generated.c runtime/gba.h
	$(HOST_CC) $(HOST_CFLAGS) -O1 -Iruntime -c $< -o $@

build/txra-pc: build/generated.o $(wildcard runtime/*.c) $(wildcard runtime/*.h)
	$(HOST_CC) $(HOST_CFLAGS) $(SDL_CFLAGS) -Iruntime runtime/*.c build/generated.o $(SDL_LIBS) -o $@
	$(PYTHON) tools/progress.py

recomp: build/txra-pc
.PHONY: recomp

# Readable per-function pseudo-C lifted from the recompiler (build output, not committed).
drafts: recomp/generate.py recomp/draft.py docs/map/functions.json baserom.gba
	$(PYTHON) recomp/generate.py --draft
.PHONY: drafts

build/runtime-test: tests/runtime_test.c runtime/cpu.c runtime/memory.c runtime/hardware.c runtime/coverage.c runtime/gba.h
	@mkdir -p build
	$(HOST_CC) $(HOST_CFLAGS) -Iruntime tests/runtime_test.c runtime/cpu.c runtime/memory.c runtime/hardware.c runtime/coverage.c -o $@

check-runtime: build/runtime-test
	./build/runtime-test
.PHONY: check-runtime

build/cpu-reference.so: tests/cpu_reference.c runtime/cpu.c runtime/memory.c runtime/hardware.c runtime/coverage.c runtime/gba.h
	$(HOST_CC) $(HOST_CFLAGS) -shared -fPIC -Iruntime tests/cpu_reference.c runtime/cpu.c runtime/memory.c runtime/hardware.c runtime/coverage.c -o $@

check-cpu-reference: build/cpu-reference.so
	$(PYTHON) tools/check_cpu_reference.py
.PHONY: check-cpu-reference

build/controller-test: tests/controller_test.c runtime/input.c runtime/input.h
	@mkdir -p build
	$(HOST_CC) $(HOST_CFLAGS) $(SDL_CFLAGS) -Iruntime tests/controller_test.c runtime/input.c $(SDL_LIBS) -o $@

check-controller: build/controller-test
	./build/controller-test
.PHONY: check-controller

build/coverage-test: tests/coverage_test.c runtime/cpu.c runtime/memory.c runtime/hardware.c runtime/coverage.c runtime/gba.h
	@mkdir -p build
	$(HOST_CC) $(HOST_CFLAGS) -Iruntime tests/coverage_test.c runtime/cpu.c runtime/memory.c runtime/hardware.c runtime/coverage.c -o $@

check-mapping: build/coverage-test
	$(PYTHON) -m unittest discover -s tests -p test_mapping.py -v
.PHONY: check-mapping

# Metadata-only code discovery proposals; review before adding seeds.
code-audit:
	$(PYTHON) tools/code_audit.py
check-code-audit:
	$(PYTHON) -m unittest discover -s tests -p test_code_audit.py -v
.PHONY: code-audit check-code-audit

# PC-only builds do not require the matching compiler toolchain.
check-accuracy: recomp
	python3 tools/check_accuracy.py
check-desktop: build/desktop-test check-controller recomp
	./build/desktop-test
	python3 tools/check_desktop_flow.py
build/desktop-test: tests/desktop_test.c runtime/desktop.c runtime/desktop.h runtime/input.c runtime/input.h runtime/audio.c runtime/audio.h
	@mkdir -p build
	$(HOST_CC) $(HOST_CFLAGS) $(SDL_CFLAGS) -Iruntime tests/desktop_test.c runtime/desktop.c runtime/input.c runtime/audio.c $(SDL_LIBS) -o $@
.PHONY: check-accuracy check-desktop

# Windows x86-64 cross-build with MinGW-w64 and the official SDL2 MinGW SDK; the ROM stays separate.
# SDL2_WINDOWS_ROOT is the SDK's x86_64-w64-mingw32 folder (or set TXRA_SDL2_WINDOWS_ROOT).
windows:
	$(PYTHON) tools/build_pc.py --target windows $(if $(SDL2_WINDOWS_ROOT),--sdl2-root "$(SDL2_WINDOWS_ROOT)") "$(ROM)"
package-windows: windows
	$(PYTHON) tools/package_windows.py $(if $(SDL2_WINDOWS_ROOT),--sdl2-root "$(SDL2_WINDOWS_ROOT)")
.PHONY: windows package-windows

# Pick a fresh private directory for another complete recording.
CAREER_OUTPUT ?= build/career-check
check-career: recomp
	python3 tools/check_career.py "$(CAREER_OUTPUT)"
.PHONY: check-career

# Release archive of the Linux executable (no ROM or game data; verified against your ROM).
package-pc: recomp
	python3 tools/package_pc.py
.PHONY: package-pc
