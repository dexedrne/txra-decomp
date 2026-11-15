#include "input.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char *actions[] = {"a",    "b",  "select", "start", "right",
                                "left", "up", "down",   "r",     "l"};
void bindings_default(Bindings *b) {
    *b = (Bindings){{SDL_SCANCODE_X, SDL_SCANCODE_Z, SDL_SCANCODE_BACKSPACE, SDL_SCANCODE_RETURN,
                     SDL_SCANCODE_RIGHT, SDL_SCANCODE_LEFT, SDL_SCANCODE_UP, SDL_SCANCODE_DOWN,
                     SDL_SCANCODE_S, SDL_SCANCODE_A},
                    {SDL_CONTROLLER_BUTTON_A, SDL_CONTROLLER_BUTTON_B, SDL_CONTROLLER_BUTTON_BACK,
                     SDL_CONTROLLER_BUTTON_START, SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
                     SDL_CONTROLLER_BUTTON_DPAD_LEFT, SDL_CONTROLLER_BUTTON_DPAD_UP,
                     SDL_CONTROLLER_BUTTON_DPAD_DOWN, SDL_CONTROLLER_BUTTON_RIGHTSHOULDER,
                     SDL_CONTROLLER_BUTTON_LEFTSHOULDER},
                    12000};
}
bool bindings_write(const Bindings *b, const char *path) {
    FILE *f = fopen(path, "w");
    if (!f)
        return false;
    fprintf(f,
            "# SDL scancode names and standard controller button names. Restart to reload.\n"
            "# a/b are south/east on both controller families; guide opens the PC menu.\n"
            "deadzone=%d\n",
            b->deadzone);
    for (int i = 0; i < 10; i++)
        fprintf(f, "key.%s=%s\npad.%s=%s\n", actions[i], SDL_GetScancodeName(b->keyboard[i]),
                actions[i], SDL_GameControllerGetStringForButton(b->buttons[i]));
    bool ok = !ferror(f);
    return fclose(f) == 0 && ok;
}
bool bindings_load(Bindings *b, const char *path) {
    FILE *f = fopen(path, "r");
    if (!f)
        return false;
    Bindings next = *b;
    char line[256];
    unsigned number = 0;
    bool ok = true;
    while (fgets(line, sizeof(line), f)) {
        number++;
        line[strcspn(line, "\r\n")] = 0;
        if (!line[0] || line[0] == '#')
            continue;
        char *value = strchr(line, '=');
        if (!value) {
            ok = false;
            break;
        }
        *value++ = 0;
        if (!strcmp(line, "deadzone")) {
            char *end;
            long v = strtol(value, &end, 10);
            if (*end || v < 0 || v > 30000) {
                ok = false;
                break;
            }
            next.deadzone = (int)v;
            continue;
        }
        bool found = false;
        for (int i = 0; i < 10; i++) {
            if (!strncmp(line, "key.", 4) && !strcmp(line + 4, actions[i])) {
                SDL_Scancode sc = SDL_GetScancodeFromName(value);
                if (sc == SDL_SCANCODE_UNKNOWN) {
                    ok = false;
                    break;
                }
                next.keyboard[i] = sc;
                found = true;
            } else if (!strncmp(line, "pad.", 4) && !strcmp(line + 4, actions[i])) {
                SDL_GameControllerButton bt = SDL_GameControllerGetButtonFromString(value);
                if (bt == SDL_CONTROLLER_BUTTON_INVALID) {
                    ok = false;
                    break;
                }
                next.buttons[i] = bt;
                found = true;
            }
        }
        if (!found || !ok) {
            ok = false;
            break;
        }
    }
    if (ferror(f))
        ok = false;
    fclose(f);
    if (ok)
        *b = next;
    else
        fprintf(stderr, "Invalid binding at line %u; file rejected\n", number);
    return ok;
}
unsigned bindings_keys(const Bindings *b, SDL_GameController *pad, const Uint8 *k) {
    unsigned keys = 0;
    bool attached = pad && SDL_GameControllerGetAttached(pad);
    for (unsigned i = 0; i < 10; i++)
        if ((k && k[b->keyboard[i]]) ||
            (attached && SDL_GameControllerGetButton(pad, b->buttons[i])))
            keys |= 1u << i;
    if (attached) {
        int x = SDL_GameControllerGetAxis(pad, SDL_CONTROLLER_AXIS_LEFTX),
            y = SDL_GameControllerGetAxis(pad, SDL_CONTROLLER_AXIS_LEFTY);
        if (x > b->deadzone)
            keys |= 16;
        if (x < -b->deadzone)
            keys |= 32;
        if (y < -b->deadzone)
            keys |= 64;
        if (y > b->deadzone)
            keys |= 128;
    }
    return keys;
}
void controller_event(SDL_GameController **pad, const SDL_Event *event) {
    if (event->type == SDL_CONTROLLERDEVICEREMOVED && *pad &&
        SDL_JoystickInstanceID(SDL_GameControllerGetJoystick(*pad)) == event->cdevice.which) {
        SDL_GameControllerClose(*pad);
        *pad = NULL;
    }
    if (!*pad &&
        (event->type == SDL_CONTROLLERDEVICEADDED || event->type == SDL_CONTROLLERDEVICEREMOVED)) {
        for (int i = 0; i < SDL_NumJoysticks(); i++) {
            if (SDL_IsGameController(i) && (*pad = SDL_GameControllerOpen(i)))
                break;
        }
    }
}
unsigned controller_keys(SDL_GameController *pad) {
    Bindings b;
    bindings_default(&b);
    return bindings_keys(&b, pad, NULL);
}
