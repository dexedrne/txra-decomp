.global _start
_start:
.include "asm/header.s"
.include "asm/crt0.s"
.include "asm/arm_engine.s"
.include "asm/program.s"
.include "asm/data_unresolved.s"
