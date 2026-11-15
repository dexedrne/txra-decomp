#include "gba.h"
#include <stdlib.h>
#include <string.h>
bool generated_dispatch(GBA *g) {
    (void)g;
    return false;
}
void execute(unsigned *regs, unsigned *ps, unsigned op, int thumb) {
    GBA *g = calloc(1, sizeof(*g));
    memcpy(g->r, regs, 64);
    g->cpsr = *ps;
    g->quota = 1;
    if (thumb)
        wr16(g, regs[15], op);
    else
        wr32(g, regs[15], op);
    fallback(g);
    memcpy(regs, g->r, 64);
    *ps = g->cpsr;
    free(g);
}
