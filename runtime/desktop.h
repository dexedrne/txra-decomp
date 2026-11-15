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
#endif
