#ifndef TXRA_TOUCH_H
#define TXRA_TOUCH_H
/* On-screen controls for the iPhone build: layout and hit-testing only.
   Plain C with no SDL or Apple dependency, so tests/touch_test.c runs on Linux. */
#include <stdbool.h>
#include <stdint.h>

/* GBA keypad bits in KEYINPUT order (the order of the bindings in input.c). */
enum {
    TOUCH_KEY_A = 1,
    TOUCH_KEY_B = 2,
    TOUCH_KEY_SELECT = 4,
    TOUCH_KEY_START = 8,
    TOUCH_KEY_RIGHT = 16,
    TOUCH_KEY_LEFT = 32,
    TOUCH_KEY_UP = 64,
    TOUCH_KEY_DOWN = 128,
    TOUCH_KEY_R = 256,
    TOUCH_KEY_L = 512
};

/* Controls. Every control is a circle (D-pad, A, B, pause) or a rounded box (L, R, Start,
   Select); `visual` is what is drawn, `hit` is the larger area that accepts a finger. */
enum {
    TOUCH_NONE = -1,
    TOUCH_DPAD = 0,
    TOUCH_A,
    TOUCH_B,
    TOUCH_L,
    TOUCH_R,
    TOUCH_START,
    TOUCH_SELECT,
    TOUCH_PAUSE,
    TOUCH_CONTROLS,
    TOUCH_BUTTONS = TOUCH_CONTROLS /* finger state: on the button group, re-tested on every move */
};

typedef struct {
    float x, y, w, h;
} TouchRect;

typedef struct {
    int width, height;  /* drawable size in pixels (landscape) */
    float unit;         /* pixels per point */
    TouchRect safe;     /* safe area in pixels */
    TouchRect game;     /* where the 240x160 picture goes, aspect-correct */
    TouchRect visual[TOUCH_CONTROLS];
    TouchRect hit[TOUCH_CONTROLS];
    bool round[TOUCH_CONTROLS];
} TouchLayout;

/* Inset values are pixels (safe-area insets times `unit`). With `integer` the picture uses the
   largest whole-number scale that fits; otherwise it fills the safe height or width. */
void touch_layout(TouchLayout *layout, int width, int height, float unit, float inset_left,
                  float inset_top, float inset_right, float inset_bottom, bool integer);

/* The scale a phone starts with until the player picks one: whole-number when the filled
   picture leaves no room for A beside it (16:9 phones with a Home button), so the controls
   cover less of the race HUD; fill otherwise. */
bool touch_default_integer(int width, int height, float unit, float inset_left, float inset_top,
                           float inset_right, float inset_bottom);

/* Topmost control whose hit area contains the point (TOUCH_NONE if none). */
int touch_hit(const TouchLayout *layout, float x, float y);
/* Keys for a D-pad finger: 8-way with a small dead zone, 45-degree sectors, no outer limit. */
unsigned touch_dpad_keys(const TouchLayout *layout, float x, float y);
/* Keys for a finger on the button group: the button under it, or A+B between A and B. */
unsigned touch_button_keys(const TouchLayout *layout, float x, float y);

enum { TOUCH_FINGERS = 10 };
typedef struct {
    int64_t id;
    int control; /* TOUCH_DPAD, TOUCH_BUTTONS, TOUCH_PAUSE or TOUCH_NONE */
    float x, y;
    bool used;
} TouchFinger;
typedef struct {
    TouchFinger finger[TOUCH_FINGERS];
} TouchState;

void touch_reset(TouchState *state);
/* A finger that lands on the D-pad keeps steering wherever it slides; a finger that lands on a
   button can slide to the other buttons. Fingers that land elsewhere do nothing. Returns the
   control that was hit (TOUCH_PAUSE is a one-shot press for the caller). */
int touch_down(TouchState *state, const TouchLayout *layout, int64_t id, float x, float y);
void touch_move(TouchState *state, int64_t id, float x, float y);
void touch_up(TouchState *state, int64_t id);
unsigned touch_keys(const TouchState *state, const TouchLayout *layout);

/* Pause-menu geometry in GBA pixels, shared by the iPhone menu drawing and its hit-testing. */
enum {
    TOUCH_MENU_X = 21,
    TOUCH_MENU_W = 198,
    TOUCH_MENU_Y = 31,
    TOUCH_MENU_STEP = 18,
    TOUCH_MENU_H = 16
};
/* Screen pixels to GBA pixels inside the picture; false outside it. */
bool touch_to_game(const TouchLayout *layout, float x, float y, float *gx, float *gy);
/* Menu row at GBA coordinates, or -1. */
int touch_menu_item(float gx, float gy, int count);
#endif
