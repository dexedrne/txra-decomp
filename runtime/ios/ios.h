#ifndef TXRA_IOS_H
#define TXRA_IOS_H
/* iPhone shell around the desktop runtime: hints, the ROM instructions screen, the touch
   overlay and app lifecycle (save flush, pause, audio). Compiled only for the iOS app
   (TXRA_IOS); Linux and Windows builds never include it. */
#include "audio.h"
#include "desktop.h"
#include "gba.h"
#include <SDL.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define TXRA_ROM_SHA1 "4197339d4add74bb40ed02a8fba5e58096afb487"

/* Before SDL_Init: landscape, Metal, playback audio category, no screen dimming. */
void ios_hints(void);
/* The app's Documents folder (Files > On My iPhone > TXRA), created if missing. */
const char *ios_documents(void);
/* Remembers the machine, audio and menu state and installs the lifecycle watch: the save is
   flushed and the game paused as soon as the app leaves the foreground. */
void ios_attach(GBA *g, Audio *audio, Desktop *desktop, SDL_Window *window,
                SDL_Renderer *renderer);
/* Looks for the player's dump in Documents; until one is found, shows the instructions and
   retries on a tap, on return to the app and when a file is shared to the app.
   False if the app is closing. */
bool ios_find_rom(uint8_t *rom, size_t size);
/* Touch, controller-use and app events from the main loop. May set *command (the same
   command numbers as main.c: 1 pause/resume, 6 accept, 7 cancel) and desktop->selected. */
void ios_event(const SDL_Event *event, int *command);
/* GBA keys held on the touch overlay. */
unsigned ios_keys(void);
/* Draws the picture in the safe area plus the overlay; nothing while in the background. */
void ios_present(SDL_Texture *texture, const uint32_t *pixels);
/* True while the app is in the background (no rendering allowed). */
bool ios_background(void);
/* The save file: Documents/Saves/txra.sav, so players see it and its reset backups in the
   Files app and can copy them out. Moves a save from the older place in `pref` once. */
const char *ios_save_path(const char *pref);
/* Scale and Sound from the pause menu, kept in `pref`/settings.ini between launches. Load
   sets desktop->integer (when stored) and clears *sound when it was turned off. Until the
   player picks a scale, the first layout picks one for the screen (touch_default_integer). */
void ios_load_settings(const char *pref, Desktop *desktop, bool *sound);
/* After a Scale or Sound change in the menu; only a Sound change updates the stored Sound
   (so an audio device that failed to open is not remembered as the player's choice). */
void ios_save_settings(bool sound_changed);
/* Startup errors as an alert over SDL's window (once ios_error_window has been given the
   window, after ios_attach_window); the app then closes when the alert is dismissed. */
void ios_error_window(SDL_Window *window);
void ios_show_error(const char *message);
bool ios_error_shown(void);

/* Objective-C side (ios_platform.m). Puts SDL's window into the app's window scene (right
   after SDL_CreateWindow), and reads the safe-area insets in points. */
void ios_attach_window(SDL_Window *window);
void ios_safe_insets(SDL_Window *window, float *left, float *top, float *right, float *bottom);
/* Drawable pixels per point (0 if unknown). SDL's own window size can be stale after the app
   comes back from a portrait-only app, so the layout never relies on it. */
float ios_display_scale(SDL_Window *window);
#endif
