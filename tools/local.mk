TOOL_ROOT ?= $(HOME)/opt
ARM_BIN ?= $(TOOL_ROOT)/arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-
PYTHON ?= $(if $(wildcard $(TOOL_ROOT)/txra-venv/bin/python),$(TOOL_ROOT)/txra-venv/bin/python,python3)
export TXRA_TOOLS := $(TOOL_ROOT)
