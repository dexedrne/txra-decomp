#include "touch.h"
#include <math.h>
#include <stddef.h>

static float clampf(float v, float lo, float hi) {
    return v < lo ? lo : v > hi ? hi : v;
}
static TouchRect square(float cx, float cy, float d) {
    return (TouchRect){cx - d / 2, cy - d / 2, d, d};
}
static TouchRect grow(TouchRect r, float dx, float dy) {
    return (TouchRect){r.x - dx, r.y - dy, r.w + 2 * dx, r.h + 2 * dy};
}
static float cx_of(TouchRect r) {
    return r.x + r.w / 2;
}
static float cy_of(TouchRect r) {
    return r.y + r.h / 2;
}

void touch_layout(TouchLayout *l, int width, int height, float unit, float inset_left,
                  float inset_top, float inset_right, float inset_bottom, bool integer) {
    l->width = width;
    l->height = height;
    l->unit = unit > 0 ? unit : 1;
    float pt = l->unit;
    l->safe = (TouchRect){inset_left, inset_top, width - inset_left - inset_right,
                          height - inset_top - inset_bottom};
    if (l->safe.w < 1 || l->safe.h < 1)
        l->safe = (TouchRect){0, 0, (float)width, (float)height};
    TouchRect s = l->safe;

    /* The picture: largest 3:2 rectangle in the safe area, centred, whole pixels. */
    float scale = fminf(s.w / 240, s.h / 160);
    if (integer && scale >= 1)
        scale = floorf(scale);
    float gw = roundf(240 * scale), gh = roundf(160 * scale);
    l->game = (TouchRect){s.x + floorf((s.w - gw) / 2), s.y + floorf((s.h - gh) / 2), gw, gh};

    /* Control sizes follow the short side of the safe area, within comfortable point sizes. */
    float side = fminf(s.w, s.h);
    float m = clampf(0.035f * side, 10 * pt, 18 * pt);
    float dpad = clampf(0.34f * side, 120 * pt, 165 * pt);
    float ab = clampf(0.18f * side, 62 * pt, 86 * pt);
    float lr_h = clampf(0.12f * side, 40 * pt, 54 * pt), ss_h = clampf(0.085f * side, 30 * pt, 38 * pt);
    float pause = clampf(0.11f * side, 40 * pt, 50 * pt);
    float left = s.x, right = s.x + s.w, top = s.y, bottom = s.y + s.h;
    /* The side column beside the picture. On wide phones L, R, Start, Select and pause fit in
       it completely; the D-pad and A/B reach over the picture edge, translucently. On 16:9
       phones the column is narrow and every control overlaps the edge a little. */
    float column = fmaxf(l->game.x - m / 2 - (left + m), 0);
    float lr_w = clampf(column, 72 * pt, 130 * pt), ss_w = clampf(column, 64 * pt, 90 * pt);
    float column_cx = left + m + fmaxf(column, ss_w) / 2;

    /* Left side, top to bottom: L, pause, Select, D-pad. Right side mirrored: R, Start, A/B. */
    l->visual[TOUCH_L] = (TouchRect){left + m, top + m, lr_w, lr_h};
    l->visual[TOUCH_R] = (TouchRect){right - m - lr_w, top + m, lr_w, lr_h};
    l->visual[TOUCH_DPAD] = (TouchRect){left + m, bottom - m - dpad, dpad, dpad};
    float pause_y = top + m + lr_h + m + pause / 2;
    float pause_x = fmaxf(column_cx, left + m + pause / 2);
    l->visual[TOUCH_PAUSE] = square(pause_x, pause_y, pause);
    float ss_y = (pause_y + pause / 2 + l->visual[TOUCH_DPAD].y) / 2;
    l->visual[TOUCH_SELECT] = (TouchRect){column_cx - ss_w / 2, ss_y - ss_h / 2, ss_w, ss_h};
    l->visual[TOUCH_START] = (TouchRect){right - (column_cx - left) - ss_w / 2, ss_y - ss_h / 2, ss_w, ss_h};
    /* A above and right of B, as on the handheld. B moves left of A only as far as it stays
       beside the picture (the race HUD's speed and gear sit in its bottom-right corner); on a
       narrow column B ends up under A. The centres stay as far apart as in the diagonal, as
       long as A's hit area stays clear of Start's (both grown below). */
    float a_x = right - m - ab / 2, b_y = bottom - m - ab / 2;
    float b_x = clampf(l->game.x + l->game.w + m / 2 + ab / 2, a_x - 0.6f * ab, a_x);
    float a_y = b_y - sqrtf(fmaxf(1.36f * ab * ab - (a_x - b_x) * (a_x - b_x), ab * ab));
    a_y = fminf(fmaxf(a_y, ss_y + 0.8f * ss_h + 0.65f * ab), b_y - ab);
    l->visual[TOUCH_A] = square(a_x, a_y, ab);
    l->visual[TOUCH_B] = square(b_x, b_y, ab);

    for (int i = 0; i < TOUCH_CONTROLS; i++)
        l->round[i] = i == TOUCH_DPAD || i == TOUCH_A || i == TOUCH_B || i == TOUCH_PAUSE;
    /* Hit areas: circles 30% wider (A and B then overlap a little, which presses both),
       boxes grown on every side; shoulders reach the screen corner. */
    for (int i = 0; i < TOUCH_CONTROLS; i++) {
        TouchRect v = l->visual[i];
        l->hit[i] = l->round[i] ? square(cx_of(v), cy_of(v), v.w * 1.3f)
                                : grow(v, v.h * 0.3f, v.h * 0.3f);
    }
    TouchRect *lh = &l->hit[TOUCH_L], *rh = &l->hit[TOUCH_R];
    lh->w += lh->x;
    lh->x = 0;
    lh->h += lh->y;
    lh->y = 0;
    rh->w = width - rh->x;
    rh->h += rh->y;
    rh->y = 0;
}

bool touch_default_integer(int width, int height, float unit, float inset_left, float inset_top,
                           float inset_right, float inset_bottom) {
    TouchLayout l;
    touch_layout(&l, width, height, unit, inset_left, inset_top, inset_right, inset_bottom, false);
    TouchRect a = l.visual[TOUCH_A];
    return a.x < l.game.x + l.game.w;
}

static bool inside(const TouchLayout *l, int control, float x, float y) {
    TouchRect r = l->hit[control];
    if (l->round[control]) {
        float dx = x - cx_of(r), dy = y - cy_of(r), radius = r.w / 2;
        return dx * dx + dy * dy <= radius * radius;
    }
    return x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h;
}

int touch_hit(const TouchLayout *l, float x, float y) {
    static const int order[] = {TOUCH_PAUSE, TOUCH_L, TOUCH_R, TOUCH_START,
                                TOUCH_SELECT, TOUCH_A, TOUCH_B, TOUCH_DPAD};
    for (size_t i = 0; i < sizeof(order) / sizeof(order[0]); i++)
        if (inside(l, order[i], x, y))
            return order[i];
    return TOUCH_NONE;
}

unsigned touch_dpad_keys(const TouchLayout *l, float x, float y) {
    TouchRect v = l->visual[TOUCH_DPAD];
    float dx = x - cx_of(v), dy = y - cy_of(v), dead = v.w / 2 * 0.16f;
    if (dx * dx + dy * dy < dead * dead)
        return 0;
    /* A direction is held within 67.5 degrees of its axis: eight 45-degree sectors. */
    const float t = 2.41421356f; /* tan(67.5 degrees) */
    unsigned keys = 0;
    if (dx > 0 && fabsf(dy) < dx * t)
        keys |= TOUCH_KEY_RIGHT;
    if (dx < 0 && fabsf(dy) < -dx * t)
        keys |= TOUCH_KEY_LEFT;
    if (dy < 0 && fabsf(dx) < -dy * t)
        keys |= TOUCH_KEY_UP;
    if (dy > 0 && fabsf(dx) < dy * t)
        keys |= TOUCH_KEY_DOWN;
    return keys;
}

unsigned touch_button_keys(const TouchLayout *l, float x, float y) {
    static const struct {
        int control;
        unsigned key;
    } buttons[] = {{TOUCH_A, TOUCH_KEY_A},         {TOUCH_B, TOUCH_KEY_B},
                   {TOUCH_L, TOUCH_KEY_L},         {TOUCH_R, TOUCH_KEY_R},
                   {TOUCH_START, TOUCH_KEY_START}, {TOUCH_SELECT, TOUCH_KEY_SELECT}};
    unsigned keys = 0;
    for (size_t i = 0; i < sizeof(buttons) / sizeof(buttons[0]); i++)
        if (inside(l, buttons[i].control, x, y))
            keys |= buttons[i].key;
    return keys;
}

void touch_reset(TouchState *s) {
    for (int i = 0; i < TOUCH_FINGERS; i++)
        s->finger[i] = (TouchFinger){0};
}

static TouchFinger *find(TouchState *s, int64_t id) {
    for (int i = 0; i < TOUCH_FINGERS; i++)
        if (s->finger[i].used && s->finger[i].id == id)
            return &s->finger[i];
    return NULL;
}

int touch_down(TouchState *s, const TouchLayout *l, int64_t id, float x, float y) {
    int hit = touch_hit(l, x, y);
    TouchFinger *f = find(s, id);
    for (int i = 0; !f && i < TOUCH_FINGERS; i++)
        if (!s->finger[i].used)
            f = &s->finger[i];
    if (f) {
        f->used = true;
        f->id = id;
        f->x = x;
        f->y = y;
        f->control = hit == TOUCH_DPAD || hit == TOUCH_PAUSE ? hit
                     : hit == TOUCH_NONE                    ? TOUCH_NONE
                                                            : TOUCH_BUTTONS;
    }
    return hit;
}

void touch_move(TouchState *s, int64_t id, float x, float y) {
    TouchFinger *f = find(s, id);
    if (f) {
        f->x = x;
        f->y = y;
    }
}

void touch_up(TouchState *s, int64_t id) {
    TouchFinger *f = find(s, id);
    if (f)
        *f = (TouchFinger){0};
}

unsigned touch_keys(const TouchState *s, const TouchLayout *l) {
    unsigned keys = 0;
    for (int i = 0; i < TOUCH_FINGERS; i++) {
        const TouchFinger *f = &s->finger[i];
        if (!f->used)
            continue;
        if (f->control == TOUCH_DPAD)
            keys |= touch_dpad_keys(l, f->x, f->y);
        else if (f->control == TOUCH_BUTTONS)
            keys |= touch_button_keys(l, f->x, f->y);
    }
    return keys;
}

bool touch_to_game(const TouchLayout *l, float x, float y, float *gx, float *gy) {
    TouchRect g = l->game;
    if (g.w <= 0 || g.h <= 0 || x < g.x || y < g.y || x >= g.x + g.w || y >= g.y + g.h)
        return false;
    *gx = (x - g.x) * 240 / g.w;
    *gy = (y - g.y) * 160 / g.h;
    return true;
}

int touch_menu_item(float gx, float gy, int count) {
    if (gx < TOUCH_MENU_X || gx >= TOUCH_MENU_X + TOUCH_MENU_W || gy < TOUCH_MENU_Y)
        return -1;
    int row = (int)((gy - TOUCH_MENU_Y) / TOUCH_MENU_STEP);
    return row < count ? row : -1;
}
