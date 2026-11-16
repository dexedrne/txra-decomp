#ifndef TXRA_DESKTOP_H
#define TXRA_DESKTOP_H
#include <SDL.h>
#include <stdbool.h>
#include <stdint.h>
typedef struct {
    bool paused, fullscreen, integer, muted, confirm_reset;
    int selected;
    double speed;
    char notice[64];
    Uint32 notice_until;
} Desktop;
void desktop_pixels(const Desktop *, const uint32_t *, uint32_t *);
void desktop_present(SDL_Renderer *, SDL_Texture *, SDL_Window *, const uint32_t *, bool);
bool desktop_screenshot(const uint32_t *, const char *);
bool desktop_backup(const char *);
void desktop_notice(Desktop *, const char *);
/* Pause-menu rows in display order, as action numbers 0 resume, 1 fullscreen, 2 scale,
   3 sound, 4 screenshot, 5 reset save, 6 quit. The iPhone build has no fullscreen or quit
   rows (iOS apps are always full screen and do not quit themselves). */
extern const int desktop_menu[];
extern const int desktop_menu_count;
/* 5x7 lettering columns (bit 0 = top row) for A-Z and 0-9, or NULL. */
const uint8_t *desktop_glyph(int ch);
#endif
