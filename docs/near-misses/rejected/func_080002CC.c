/* Diagnostic lifted draft only; not a compilable near match.
 * Rejection: ARM: needs a separate compiler path
 */
/* func_080002CC  0x080002CC  arm mode, 88 bytes of instructions (pools excluded)
 * callers: none found (entry, pointer or interrupt target)
 * callees: func_08000324
 * matched in C: no
 * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are
 * folded into conditions where a branch uses them. Not compilable as-is. */
void func_080002CC(void) {
    u32 r6, r7, r8, r9, r10, r11;
    lr = *(u32 *)(pc + 0x2FC);
    lr = *(u32 *)lr;
    r6 = *(s16 *)lr;
    r7 = *(s16 *)(lr + 8);
    r8 = *(s16 *)(lr + 2);
    r9 = *(s16 *)(lr + 0xA);
    r10 = *(s16 *)(lr + 4);
    r11 = *(s16 *)(lr + 0xC);
    r3 = *(u16 *)(lr + 0x18);
    func_08000324();
    lr = *(u32 *)(pc + 0x2D4);
    lr = *(u32 *)lr;
    r6 = *(s16 *)(lr + 4);
    r7 = *(s16 *)(lr + 0xC);
    r8 = *(s16 *)(lr + 6);
    r9 = *(s16 *)(lr + 0xE);
    r10 = *(s16 *)lr;
    r11 = *(s16 *)(lr + 8);
    func_08000324();
    return;
}
