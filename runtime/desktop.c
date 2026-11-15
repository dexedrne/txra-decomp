#include "desktop.h"
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
/* Small host-only lettering. It never touches the guest framebuffer. */
static const uint8_t glyphs[][5] = {{0x7e, 0x11, 0x11, 0x11, 0x7e},
                                    {0x7f, 0x49, 0x49, 0x49, 0x36},
                                    {0x3e, 0x41, 0x41, 0x41, 0x22},
                                    {0x7f, 0x41, 0x41, 0x22, 0x1c},
                                    {0x7f, 0x49, 0x49, 0x49, 0x41},
                                    {0x7f, 9, 9, 9, 1},
                                    {0x3e, 0x41, 0x49, 0x49, 0x7a},
                                    {0x7f, 8, 8, 8, 0x7f},
                                    {0x41, 0x41, 0x7f, 0x41, 0x41},
                                    {0x20, 0x40, 0x41, 0x3f, 1},
                                    {0x7f, 8, 0x14, 0x22, 0x41},
                                    {0x7f, 0x40, 0x40, 0x40, 0x40},
                                    {0x7f, 2, 0x0c, 2, 0x7f},
                                    {0x7f, 4, 8, 0x10, 0x7f},
                                    {0x3e, 0x41, 0x41, 0x41, 0x3e},
                                    {0x7f, 9, 9, 9, 6},
                                    {0x3e, 0x41, 0x51, 0x21, 0x5e},
                                    {0x7f, 9, 0x19, 0x29, 0x46},
                                    {0x46, 0x49, 0x49, 0x49, 0x31},
                                    {1, 1, 0x7f, 1, 1},
                                    {0x3f, 0x40, 0x40, 0x40, 0x3f},
                                    {0x1f, 0x20, 0x40, 0x20, 0x1f},
                                    {0x3f, 0x40, 0x38, 0x40, 0x3f},
                                    {0x63, 0x14, 8, 0x14, 0x63},
                                    {7, 8, 0x70, 8, 7},
                                    {0x61, 0x51, 0x49, 0x45, 0x43},
                                    {0x3e, 0x51, 0x49, 0x45, 0x3e},
                                    {0, 0x42, 0x7f, 0x40, 0},
                                    {0x42, 0x61, 0x51, 0x49, 0x46},
                                    {0x21, 0x41, 0x45, 0x4b, 0x31},
                                    {0x18, 0x14, 0x12, 0x7f, 0x10},
                                    {0x27, 0x45, 0x45, 0x45, 0x39},
                                    {0x3c, 0x4a, 0x49, 0x49, 0x30},
                                    {1, 0x71, 9, 5, 3},
                                    {0x36, 0x49, 0x49, 0x49, 0x36},
                                    {6, 0x49, 0x49, 0x29, 0x1e}};
static void box(uint32_t *p, int x, int y, int w, int h, uint32_t c) {
    for (int j = y; j < y + h && j < 160; j++)
        for (int i = x; i < x + w && i < 240; i++)
            if (i >= 0 && j >= 0)
                p[j * 240 + i] = 0xff000000 | c;
}
static void text(uint32_t *p, int x, int y, const char *s, uint32_t c) {
    for (; *s; s++, x += 6) {
        int ch = *s;
        if (ch >= 'a' && ch <= 'z')
            ch -= 32;
        const uint8_t *g = ch >= 'A' && ch <= 'Z'   ? glyphs[ch - 'A']
                           : ch >= '0' && ch <= '9' ? glyphs[26 + ch - '0']
                                                    : NULL;
        if (g) {
            for (int i = 0; i < 5; i++)
                for (int j = 0; j < 7; j++)
                    if (g[i] & (1 << j))
                        box(p, x + i, y + j, 1, 1, c);
        } else if (ch == '.')
            box(p, x + 2, y + 6, 1, 1, c);
        else if (ch == ':') {
            box(p, x + 2, y + 2, 1, 1, c);
            box(p, x + 2, y + 5, 1, 1, c);
        } else if (ch == '-')
            box(p, x, y + 3, 5, 1, c);
        else if (ch == '/') {
            for (int j = 0; j < 5; j++)
                box(p, x + 4 - j, y + j + 1, 1, 1, c);
        }
    }
}
void desktop_notice(Desktop *d, const char *s) {
    snprintf(d->notice, sizeof(d->notice), "%s", s);
    d->notice_until = SDL_GetTicks() + 2500;
}
void desktop_pixels(const Desktop *d, const uint32_t *source, uint32_t *p) {
    memcpy(p, source, 240 * 160 * 4);
    if (d->paused) {
        for (int i = 0; i < 240 * 160; i++)
            p[i] = 0xff000000 | ((p[i] & 0xfefefe) >> 1);
        box(p, 12, 7, 216, 146, 0x5e564b);
        box(p, 13, 8, 214, 144, 0x1b1915);
        text(p, 24, 17, "TXRA", 0xffefd0);
        text(p, 114, 17, "PAUSED", 0xffb12a);
        if (d->confirm_reset) {
            text(p, 24, 42, "RESET THIS SAVE?", 0xffb12a);
            text(p, 24, 60, "OLD FILE IS BACKED UP.", 0xffefd0);
            text(p, 24, 79, "A / ENTER TO RESET", 0xffefd0);
            text(p, 24, 97, "B / ESC TO CANCEL", 0xffefd0);
        } else {
            const char *items[] = {"RESUME",
                                   d->fullscreen ? "FULLSCREEN: ON" : "FULLSCREEN: OFF",
                                   d->integer ? "SCALE: INTEGER" : "SCALE: ASPECT FIT",
                                   d->muted ? "SOUND: OFF" : "SOUND: ON",
                                   "SCREENSHOT",
                                   "RESET SAVE",
                                   "QUIT"};
            for (int i = 0; i < 7; i++) {
                if (i == d->selected)
                    box(p, 21, 35 + i * 12, 198, 11, 0x3a332a);
                text(p, 27, 37 + i * 12, items[i], i == d->selected ? 0xffb12a : 0xffefd0);
            }
            text(p, 24, 128, "ARROWS / D-PAD   A: SELECT", 0xb8ad9b);
            text(p, 24, 140, "ESC / GUIDE: RESUME", 0xb8ad9b);
        }
    }
    if (!d->paused && d->speed != 1) {
        box(p, 4, 4, 100, 13, 0x1b1915);
        text(p, 8, 7, d->speed > 1 ? "DEBUG 3X" : "DEBUG 0.5X", 0xffb12a);
    }
    if (d->notice[0] && (Sint32)(d->notice_until - SDL_GetTicks()) > 0) {
        box(p, 3, 146, 234, 12, 0x1b1915);
        text(p, 6, 149, d->notice, 0xffb12a);
    }
}
void desktop_present(SDL_Renderer *r, SDL_Texture *t, SDL_Window *w, const uint32_t *p,
                     bool integer) {
    (void)w;
    int width, height;
    SDL_GetRendererOutputSize(r, &width, &height);
    double scale = SDL_min(width / 240.0, height / 160.0);
    if (integer && scale >= 1)
        scale = (int)scale;
    SDL_Rect dst = {0, 0, (int)(240 * scale), (int)(160 * scale)};
    dst.x = (width - dst.w) / 2;
    dst.y = (height - dst.h) / 2;
    SDL_UpdateTexture(t, NULL, p, 240 * 4);
    SDL_SetRenderDrawColor(r, 0, 0, 0, 255);
    SDL_RenderClear(r);
    SDL_RenderCopy(r, t, NULL, &dst);
    SDL_RenderPresent(r);
}
bool desktop_screenshot(const uint32_t *p, const char *path) {
    SDL_Surface *s = SDL_CreateRGBSurfaceWithFormatFrom((void *)p, 240, 160, 32, 240 * 4,
                                                        SDL_PIXELFORMAT_ARGB8888);
    if (!s)
        return false;
    int rc = SDL_SaveBMP(s, path);
    SDL_FreeSurface(s);
    return rc == 0;
}
bool desktop_backup(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f)
        return errno == ENOENT;
    fclose(f);
    char backup[4096];
    snprintf(backup, sizeof(backup), "%s.reset-%lld-%u.bak", path, (long long)time(NULL),
             SDL_GetTicks());
    /* Refuse to replace any previous backup. */
    f = fopen(backup, "rb");
    if (f) {
        fclose(f);
        return false;
    }
    return rename(path, backup) == 0;
}
