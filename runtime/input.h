#ifndef TXRA_INPUT_H
#define TXRA_INPUT_H
#include <SDL.h>
#include <stdbool.h>
void controller_event(SDL_GameController **pad, const SDL_Event *event);
unsigned controller_keys(SDL_GameController *pad);
typedef struct {
    SDL_Scancode keyboard[10];
    SDL_GameControllerButton buttons[10];
    int deadzone;
} Bindings;
void bindings_default(Bindings *bindings);
bool bindings_load(Bindings *bindings, const char *path);
bool bindings_write(const Bindings *bindings, const char *path);
unsigned bindings_keys(const Bindings *bindings, SDL_GameController *pad, const Uint8 *keyboard);
#endif
