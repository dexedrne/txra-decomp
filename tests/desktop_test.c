#include "audio.h"
#include "desktop.h"
#include "input.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
static unsigned checks;
#define CHECK(c)                                                                                   \
    do {                                                                                           \
        checks++;                                                                                  \
        if (!(c)) {                                                                                \
            fprintf(stderr, "desktop check %u failed: %s\n", checks, #c);                          \
            exit(1);                                                                               \
        }                                                                                          \
    } while (0)
int main(void) {
    SDL_setenv("SDL_VIDEODRIVER", "dummy", 1);
    SDL_setenv("SDL_AUDIODRIVER", "dummy", 1);
    CHECK(SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_GAMECONTROLLER) == 0);
    char dir[] = "/tmp/txra-desktop-XXXXXX";
    CHECK(mkdtemp(dir) != NULL);
    char path[256];
    snprintf(path, sizeof(path), "%s/bindings.ini", dir);
    Bindings b, loaded;
    bindings_default(&b);
    loaded = b;
    CHECK(bindings_write(&b, path));
    CHECK(bindings_load(&loaded, path));
    CHECK(!memcmp(&b, &loaded, sizeof(b)));
    FILE *f = fopen(path, "w");
    CHECK(f != NULL);
    fputs("key.a=Space\npad.a=y\ndeadzone=18000\n", f);
    fclose(f);
    CHECK(bindings_load(&loaded, path));
    CHECK(loaded.keyboard[0] == SDL_SCANCODE_SPACE);
    CHECK(loaded.buttons[0] == SDL_CONTROLLER_BUTTON_Y);
    CHECK(loaded.deadzone == 18000);
    Uint8 keyboard[SDL_NUM_SCANCODES] = {0};
    keyboard[SDL_SCANCODE_SPACE] = 1;
    CHECK(bindings_keys(&loaded, NULL, keyboard) == 1);
    Bindings previous = loaded;
    f = fopen(path, "w");
    fputs("key.a=Return\ndeadzone=99999\n", f);
    fclose(f);
    CHECK(!bindings_load(&loaded, path));
    CHECK(!memcmp(&loaded, &previous, sizeof(loaded)));
    int device = SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_GAMECONTROLLER, 6,
                                           SDL_CONTROLLER_BUTTON_MAX, 0);
    CHECK(device >= 0);
    SDL_GameController *pad = SDL_GameControllerOpen(device);
    CHECK(pad != NULL);
    SDL_Joystick *joy = SDL_GameControllerGetJoystick(pad);
    CHECK(SDL_JoystickSetVirtualButton(joy, SDL_CONTROLLER_BUTTON_Y, 1) == 0);
    SDL_PumpEvents();
    CHECK(bindings_keys(&loaded, pad, NULL) == 1);
    CHECK(SDL_JoystickSetVirtualButton(joy, SDL_CONTROLLER_BUTTON_Y, 0) == 0);
    CHECK(SDL_JoystickSetVirtualAxis(joy, SDL_CONTROLLER_AXIS_LEFTX, 15000) == 0);
    SDL_PumpEvents();
    CHECK(bindings_keys(&loaded, pad, NULL) == 0);
    CHECK(SDL_JoystickSetVirtualAxis(joy, SDL_CONTROLLER_AXIS_LEFTX, 22000) == 0);
    SDL_PumpEvents();
    CHECK(bindings_keys(&loaded, pad, NULL) == 16);
    SDL_GameControllerClose(pad);
    SDL_JoystickDetachVirtual(device);
    uint32_t source[240 * 160], out[240 * 160];
    for (unsigned i = 0; i < 240 * 160; i++)
        source[i] = 0xffffffff;
    Desktop d = {.integer = true, .speed = 1};
    desktop_pixels(&d, source, out);
    CHECK(!memcmp(source, out, sizeof(out)));
    d.paused = true;
    desktop_pixels(&d, source, out);
    CHECK(memcmp(source, out, sizeof(out)) != 0);
    CHECK(source[0] == 0xffffffff);
    CHECK(out[8 * 240 + 13] == 0xff1b1915);
    d.confirm_reset = true;
    desktop_pixels(&d, source, out);
    CHECK(out[8 * 240 + 13] == 0xff1b1915);
    SDL_Window *w = SDL_CreateWindow("check", 0, 0, 1030, 700, SDL_WINDOW_HIDDEN);
    CHECK(w != NULL);
    SDL_Renderer *r = SDL_CreateRenderer(w, -1, SDL_RENDERER_SOFTWARE);
    CHECK(r != NULL);
    SDL_Texture *t =
        SDL_CreateTexture(r, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, 240, 160);
    CHECK(t != NULL);
    uint32_t *readback = malloc(1030 * 700 * 4);
    CHECK(readback != NULL);
    desktop_present(r, t, w, source, true);
    CHECK(SDL_RenderReadPixels(r, NULL, SDL_PIXELFORMAT_ARGB8888, readback, 1030 * 4) == 0);
    CHECK((readback[29 * 1030 + 35] & 0xffffff) == 0);
    CHECK((readback[30 * 1030 + 35] & 0xffffff) == 0xffffff);
    CHECK((readback[669 * 1030 + 994] & 0xffffff) == 0xffffff);
    CHECK((readback[670 * 1030 + 995] & 0xffffff) == 0);
    desktop_present(r, t, w, source, false);
    CHECK(SDL_RenderReadPixels(r, NULL, SDL_PIXELFORMAT_ARGB8888, readback, 1030 * 4) == 0);
    CHECK((readback[6 * 1030] & 0xffffff) == 0);
    CHECK((readback[7 * 1030] & 0xffffff) == 0xffffff);
    snprintf(path, sizeof(path), "%s/shot.bmp", dir);
    CHECK(desktop_screenshot(out, path));
    SDL_Surface *shot = SDL_LoadBMP(path);
    CHECK(shot && shot->w == 240 && shot->h == 160);
    SDL_FreeSurface(shot);
    remove(path);
    snprintf(path, sizeof(path), "%s/missing.sav", dir);
    CHECK(desktop_backup(path));
    /* A non-empty save must move intact, never be replaced by an empty profile. */
    f = fopen(path, "wb");
    fputs("legacy-save-bytes", f);
    fclose(f);
    CHECK(desktop_backup(path));
    CHECK(access(path, F_OK) != 0);
    Audio audio = {0};
    CHECK(audio_open(&audio));
    CHECK(audio.format.channels == 2);
    int16_t signal[1098];
    for (unsigned i = 0; i < 1098; i += 2) {
        signal[i] = 1000;
        signal[i + 1] = -500;
    }
    for (int i = 0; i < 5; i++)
        CHECK(audio_queue(&audio, signal, sizeof(signal)));
    CHECK(audio.started);
    CHECK(audio.max_queue_bytes < (unsigned)audio.format.freq * 4 / 10);
    for (int i = 0; i < 10; i++)
        CHECK(audio_queue(&audio, signal, sizeof(signal)));
    CHECK(audio.backpressure_ticks > 0);
    Uint64 waited = audio.backpressure_ticks;
    audio_clear(&audio);
    CHECK(audio.backpressure_ticks == waited);
    CHECK(SDL_GetQueuedAudioSize(audio.device) == 0);
    CHECK(!audio.started);
    CHECK(SDL_AudioStreamAvailable(audio.stream) == 0);
    audio_close(&audio);
    free(readback);
    SDL_DestroyTexture(t);
    SDL_DestroyRenderer(r);
    SDL_DestroyWindow(w);
    SDL_Quit();
    /* Remove only this test's private files, including its reset backup. */
    char command[300];
    snprintf(command, sizeof(command), "rm -r -- '%s'", dir);
    CHECK(system(command) == 0);
    printf("%u desktop assertions passed\n", checks);
}
