void func_08015E20(void) {
    volatile unsigned int *p = (volatile unsigned int *)0x030001B4;
    *p = 0;
    while (*p == 0);
}
