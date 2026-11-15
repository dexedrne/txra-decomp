#include "input.h"
#include <assert.h>
#include <stdio.h>
static void pump(SDL_GameController **pad) {
    SDL_Event event;
    SDL_PumpEvents();
    while (SDL_PollEvent(&event)) controller_event(pad, &event);
}
int main(void) {
    assert(SDL_Init(SDL_INIT_GAMECONTROLLER) == 0);
    SDL_GameController *pad = NULL;
    int device = SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_GAMECONTROLLER, 6,
                                          SDL_CONTROLLER_BUTTON_MAX, 0);
    assert(device >= 0);
    pump(&pad);
    assert(pad && controller_keys(pad) == 0);
    SDL_Joystick *joy = SDL_GameControllerGetJoystick(pad);
    const unsigned buttons[] = {SDL_CONTROLLER_BUTTON_A, SDL_CONTROLLER_BUTTON_B,
        SDL_CONTROLLER_BUTTON_BACK, SDL_CONTROLLER_BUTTON_START, SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
        SDL_CONTROLLER_BUTTON_DPAD_LEFT, SDL_CONTROLLER_BUTTON_DPAD_UP,
        SDL_CONTROLLER_BUTTON_DPAD_DOWN, SDL_CONTROLLER_BUTTON_RIGHTSHOULDER,
        SDL_CONTROLLER_BUTTON_LEFTSHOULDER};
    for (unsigned i = 0; i < 10; i++) {
        assert(SDL_JoystickSetVirtualButton(joy, buttons[i], 1) == 0); pump(&pad);
        assert(controller_keys(pad) == (1u << i));
        assert(SDL_JoystickSetVirtualButton(joy, buttons[i], 0) == 0); pump(&pad);
        assert(controller_keys(pad) == 0);
    }
    assert(SDL_JoystickSetVirtualAxis(joy, SDL_CONTROLLER_AXIS_LEFTX, 11000) == 0);
    pump(&pad); assert(controller_keys(pad) == 0);
    assert(SDL_JoystickSetVirtualAxis(joy, SDL_CONTROLLER_AXIS_LEFTX, -20000) == 0);
    assert(SDL_JoystickSetVirtualAxis(joy, SDL_CONTROLLER_AXIS_LEFTY, 20000) == 0);
    pump(&pad); assert(controller_keys(pad) == (32 | 128));
    assert(SDL_JoystickDetachVirtual(device) == 0); pump(&pad);
    assert(!pad && controller_keys(pad) == 0);
    device = SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_GAMECONTROLLER, 6,
                                      SDL_CONTROLLER_BUTTON_MAX, 0);
    assert(device >= 0); pump(&pad); assert(pad);
    SDL_GameControllerClose(pad);
    SDL_JoystickDetachVirtual(device);
    SDL_Quit();
    puts("Controller: ten buttons, dead zone, diagonal, disconnect and reconnect passed");
}
