/* iPhone shell: see ios.h. */
#include "ios.h"
#include "romscan.h"
#include "touch.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

static struct {
    GBA *g;
    Audio *audio;
    Desktop *desktop;
    SDL_Window *window;
    SDL_Renderer *renderer;
    TouchLayout layout;
    TouchState touch;
    bool overlay;    /* hidden while a controller is in use, back on the next touch */
    bool background; /* between did-enter-background and will-enter-foreground */
    bool left_foreground, reopen_audio;
    bool scale_chosen;            /* by the player (settings file) or from the screen at start */
    bool sound_off;               /* the player's Sound choice (not a failed audio device) */
    SDL_Window *message_window;   /* set once the window is in the app's scene */
    bool error_shown;
    char documents[4096], save[4096], settings[4096];
} ios = {.overlay = true};

void ios_hints(void) {
    SDL_SetHint(SDL_HINT_ORIENTATIONS, "LandscapeLeft LandscapeRight");
    /* Edge swipes need a second swipe, so the controls near the edges are safe to use. */
    SDL_SetHint(SDL_HINT_IOS_HIDE_HOME_INDICATOR, "2");
    /* Game sound plays with the silent switch on, like other games. */
    SDL_SetHint(SDL_HINT_AUDIO_CATEGORY, "playback");
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, "metal");
    SDL_SetHint(SDL_HINT_TOUCH_MOUSE_EVENTS, "0");
    SDL_SetHint(SDL_HINT_ACCELEROMETER_AS_JOYSTICK, "0");
    /* A race with a controller has no touches: keep the screen awake. */
    SDL_SetHint(SDL_HINT_IDLE_TIMER_DISABLED, "1");
}

const char *ios_documents(void) {
    if (!ios.documents[0]) {
        const char *home = getenv("HOME");
        snprintf(ios.documents, sizeof(ios.documents), "%s/Documents", home ? home : ".");
        mkdir(ios.documents, 0755);
    }
    return ios.documents;
}

bool ios_background(void) {
    return ios.background;
}

const char *ios_save_path(const char *pref) {
    char folder[4096], old[4096];
    snprintf(folder, sizeof(folder), "%s/Saves", ios_documents());
    mkdir(folder, 0755);
    snprintf(ios.save, sizeof(ios.save), "%s/txra.sav", folder);
    /* Builds before 1.2.0 kept the save in Application Support: move it over once. */
    snprintf(old, sizeof(old), "%stxra.sav", pref);
    struct stat st;
    if (stat(ios.save, &st) != 0 && stat(old, &st) == 0 && rename(old, ios.save) == 0)
        fprintf(stderr, "Moved the save to Documents/Saves\n");
    return ios.save;
}

void ios_load_settings(const char *pref, Desktop *desktop, bool *sound) {
    snprintf(ios.settings, sizeof(ios.settings), "%ssettings.ini", pref);
    FILE *f = fopen(ios.settings, "r");
    if (!f)
        return;
    char line[128];
    while (fgets(line, sizeof(line), f)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!strcmp(line, "scale=integer") || !strcmp(line, "scale=fill")) {
            desktop->integer = line[6] == 'i';
            ios.scale_chosen = true;
        } else if (!strcmp(line, "sound=off"))
            ios.sound_off = true;
    }
    fclose(f);
    if (ios.sound_off)
        *sound = false;
}

void ios_save_settings(bool sound_changed) {
    if (!ios.settings[0] || !ios.desktop)
        return;
    ios.scale_chosen = true;
    if (sound_changed)
        ios.sound_off = ios.desktop->muted;
    FILE *f = fopen(ios.settings, "w");
    if (f) {
        fprintf(f, "# TXRA pause-menu choices, rewritten when they change.\nscale=%s\nsound=%s\n",
                ios.desktop->integer ? "integer" : "fill", ios.sound_off ? "off" : "on");
        if (fclose(f) == 0)
            return;
    }
    fprintf(stderr, "Settings not saved: %s\n", ios.settings);
}

void ios_error_window(SDL_Window *window) {
    ios.message_window = window;
}

void ios_show_error(const char *message) {
    /* UIKit shows the alert over SDL's window, which must already be in the app's scene. */
    if (!ios.message_window)
        return;
    SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_ERROR, "TXRA", message, ios.message_window);
    ios.error_shown = true;
}

bool ios_error_shown(void) {
    return ios.error_shown;
}

static void layout(void) {
    int w = 0, h = 0, ww = 0, wh = 0;
    SDL_GetRendererOutputSize(ios.renderer, &w, &h);
    SDL_GetWindowSize(ios.window, &ww, &wh);
    float unit = ios_display_scale(ios.window);
    if (unit <= 0)
        unit = ww > 0 ? (float)w / ww : 1;
    float l, t, r, b;
    ios_safe_insets(ios.window, &l, &t, &r, &b);
    if (!ios.scale_chosen && ios.desktop && w > 0 && h > 0) {
        ios.scale_chosen = true;
        ios.desktop->integer = touch_default_integer(w, h, unit, l * unit, t * unit, r * unit, b * unit);
        fprintf(stderr, "Scale: %s (this screen's default)\n", ios.desktop->integer ? "integer" : "fill");
    }
    touch_layout(&ios.layout, w, h, unit, l * unit, t * unit, r * unit, b * unit,
                 ios.desktop && ios.desktop->integer);
    static float last[7];
    float now[7] = {(float)w, (float)h, unit, l, t, r, b};
    if (memcmp(now, last, sizeof(now))) {
        memcpy(last, now, sizeof(now));
        fprintf(stderr, "Layout: %dx%d pixels, %.2fx, safe-area insets %.0f %.0f %.0f %.0f points\n", w, h,
                unit, l, t, r, b);
    }
}

/* Runs inside the app delegate callbacks (SDL calls event watches synchronously), before iOS
   may suspend the app, so the save is on disk even if the app is then killed. */
static int SDLCALL app_watch(void *unused, SDL_Event *e) {
    (void)unused;
    switch (e->type) {
    case SDL_APP_WILLENTERBACKGROUND:
        ios.left_foreground = true;
        if (ios.desktop && !ios.desktop->paused) {
            ios.desktop->paused = true;
            ios.desktop->selected = 0;
        }
        touch_reset(&ios.touch);
        if (ios.g)
            eeprom_flush(ios.g);
        if (ios.audio)
            audio_clear(ios.audio);
        if (ios.g)
            fprintf(stderr, "Leaving the foreground at frame %u: paused, save on disk (%s)\n",
                    ios.g->frame, ios.g->save_dirty ? "WRITE FAILED" : "ok");
        break;
    case SDL_APP_DIDENTERBACKGROUND:
        ios.background = true;
        if (ios.g)
            eeprom_flush(ios.g);
        break;
    case SDL_APP_TERMINATING:
    case SDL_APP_LOWMEMORY:
        if (ios.g)
            eeprom_flush(ios.g);
        break;
    case SDL_APP_WILLENTERFOREGROUND:
        ios.background = false;
        break;
    case SDL_APP_DIDENTERFOREGROUND:
        ios.background = false;
        /* Not at launch: only after the app was interrupted or in the background. */
        ios.reopen_audio = ios.left_foreground;
        ios.left_foreground = false;
        break;
    }
    return 1;
}

void ios_attach(GBA *g, Audio *audio, Desktop *desktop, SDL_Window *window,
                SDL_Renderer *renderer) {
    ios.g = g;
    ios.audio = audio;
    ios.desktop = desktop;
    ios.window = window;
    ios.renderer = renderer;
    touch_reset(&ios.touch);
    SDL_AddEventWatch(app_watch, NULL);
}

/* ---- drawing ---------------------------------------------------------------------------- */

static const uint8_t *glyph(int ch) {
    const uint8_t *g = desktop_glyph(ch);
    if (g)
        return g;
    static const struct {
        char c;
        uint8_t g[5];
    } extra[] = {{'.', {0, 0x60, 0x60, 0, 0}},       {':', {0, 0x36, 0x36, 0, 0}},
                 {'-', {8, 8, 8, 8, 8}},             {'/', {0x20, 0x10, 8, 4, 2}},
                 {'>', {0, 0x41, 0x22, 0x14, 8}},    {'(', {0, 0x1c, 0x22, 0x41, 0}},
                 {')', {0, 0x41, 0x22, 0x1c, 0}},    {',', {0, 0x50, 0x30, 0, 0}},
                 {'\'', {0, 5, 3, 0, 0}},            {'!', {0, 0, 0x5f, 0, 0}},
                 {'?', {2, 1, 0x51, 9, 6}},          {'_', {0x40, 0x40, 0x40, 0x40, 0x40}},
                 {'+', {8, 8, 0x3e, 8, 8}},          {'=', {0x14, 0x14, 0x14, 0x14, 0x14}}};
    for (size_t i = 0; i < sizeof(extra) / sizeof(extra[0]); i++)
        if (extra[i].c == ch)
            return extra[i].g;
    return NULL;
}

static float text_width(const char *s, float k) {
    size_t n = strlen(s);
    return n ? (n * 6 - 1) * k : 0;
}

static void draw_text(float x, float y, float k, const char *s, SDL_Color c) {
    SDL_FRect rects[256];
    int n = 0;
    SDL_SetRenderDrawColor(ios.renderer, c.r, c.g, c.b, c.a);
    for (; *s; s++, x += 6 * k) {
        const uint8_t *g = glyph((unsigned char)*s);
        for (int i = 0; g && i < 5; i++)
            for (int j = 0; j < 7; j++)
                if (g[i] & (1 << j)) {
                    rects[n++] = (SDL_FRect){x + i * k, y + j * k, k, k};
                    if (n == 256) {
                        SDL_RenderFillRectsF(ios.renderer, rects, n);
                        n = 0;
                    }
                }
    }
    if (n)
        SDL_RenderFillRectsF(ios.renderer, rects, n);
}

static const SDL_Color SHADOW = {0, 0, 0, 120};

/* Lettering with a dark rim, readable over light and dark pictures alike. */
static void draw_label(float x, float y, float k, const char *s, SDL_Color c) {
    float o = SDL_max(1, SDL_roundf(ios.layout.unit));
    const float offsets[4][2] = {{-o, -o}, {o, -o}, {-o, o}, {o, o}};
    for (int i = 0; i < 4; i++)
        draw_text(x + offsets[i][0], y + offsets[i][1], k, s, SHADOW);
    draw_text(x, y, k, s, c);
}

static void draw_centered(TouchRect r, float k, const char *s, SDL_Color c) {
    draw_label(r.x + (r.w - text_width(s, k)) / 2, r.y + (r.h - 7 * k) / 2, k, s, c);
}

enum { ARC = 10, OUTLINE = 4 * (ARC + 1) };

/* Rounded-rectangle outline (a circle when the radius is half the side), clockwise. */
static int outline(SDL_FPoint *p, TouchRect r, float radius) {
    radius = SDL_min(radius, SDL_min(r.w, r.h) / 2);
    const float centres[4][2] = {{r.x + r.w - radius, r.y + radius},
                                 {r.x + r.w - radius, r.y + r.h - radius},
                                 {r.x + radius, r.y + r.h - radius},
                                 {r.x + radius, r.y + radius}};
    int n = 0;
    for (int c = 0; c < 4; c++)
        for (int i = 0; i <= ARC; i++) {
            float a = (float)M_PI * (-0.5f + 0.5f * c + 0.5f * i / ARC);
            p[n++] = (SDL_FPoint){centres[c][0] + radius * SDL_cosf(a),
                                  centres[c][1] + radius * SDL_sinf(a)};
        }
    return n;
}

static void fill_shape(TouchRect r, float radius, SDL_Color c) {
    SDL_FPoint p[OUTLINE];
    int n = outline(p, r, radius);
    SDL_Vertex v[OUTLINE * 3];
    SDL_FPoint centre = {r.x + r.w / 2, r.y + r.h / 2};
    for (int i = 0; i < n; i++) {
        v[3 * i] = (SDL_Vertex){centre, c, {0, 0}};
        v[3 * i + 1] = (SDL_Vertex){p[i], c, {0, 0}};
        v[3 * i + 2] = (SDL_Vertex){p[(i + 1) % n], c, {0, 0}};
    }
    SDL_RenderGeometry(ios.renderer, NULL, v, 3 * n, NULL, 0);
}

static void stroke_shape(TouchRect r, float radius, float width, SDL_Color c) {
    SDL_FPoint out[OUTLINE], in[OUTLINE];
    int n = outline(out, r, radius);
    outline(in, (TouchRect){r.x + width, r.y + width, r.w - 2 * width, r.h - 2 * width},
            SDL_max(radius - width, 0));
    SDL_Vertex v[OUTLINE * 6];
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        SDL_Vertex a = {out[i], c, {0, 0}}, b = {out[j], c, {0, 0}}, d = {in[i], c, {0, 0}},
                   e = {in[j], c, {0, 0}};
        v[6 * i] = a;
        v[6 * i + 1] = b;
        v[6 * i + 2] = d;
        v[6 * i + 3] = b;
        v[6 * i + 4] = e;
        v[6 * i + 5] = d;
    }
    SDL_RenderGeometry(ios.renderer, NULL, v, 6 * n, NULL, 0);
}

static void triangle(SDL_FPoint a, SDL_FPoint b, SDL_FPoint c, SDL_Color col) {
    SDL_Vertex v[3] = {{a, col, {0, 0}}, {b, col, {0, 0}}, {c, col, {0, 0}}};
    SDL_RenderGeometry(ios.renderer, NULL, v, 3, NULL, 0);
}

/* A triangle on a dark rim: the same triangle pushed out by `rim` pixels from its centre. */
static void rimmed_triangle(SDL_FPoint a, SDL_FPoint b, SDL_FPoint c, float rim, SDL_Color col) {
    SDL_FPoint m = {(a.x + b.x + c.x) / 3, (a.y + b.y + c.y) / 3};
    SDL_FPoint p[3] = {a, b, c}, q[3];
    for (int i = 0; i < 3; i++) {
        float dx = p[i].x - m.x, dy = p[i].y - m.y, d = SDL_sqrtf(dx * dx + dy * dy);
        float k = d > 0 ? (d + 2 * rim) / d : 1; /* corners move ~2x the edge offset */
        q[i] = (SDL_FPoint){m.x + dx * k, m.y + dy * k};
    }
    triangle(q[0], q[1], q[2], SHADOW);
    triangle(a, b, c, col);
}

/* The white outline of a control with a dark ring just outside it. */
static void rimmed_stroke(TouchRect v, float radius, float line, SDL_Color c) {
    stroke_shape((TouchRect){v.x - line, v.y - line, v.w + 2 * line, v.h + 2 * line},
                 radius + line, line, SHADOW);
    stroke_shape(v, radius, line, c);
}

static const SDL_Color FILL = {255, 255, 255, 40}, PRESSED = {255, 177, 42, 120},
                       STROKE = {255, 255, 255, 110}, LABEL = {255, 255, 255, 200},
                       ARROW = {255, 255, 255, 150}, ACCENT = {255, 177, 42, 255};

static void draw_button(int control, bool pressed, const char *label) {
    TouchRect v = ios.layout.visual[control];
    float radius = ios.layout.round[control] ? v.w / 2 : v.h * 0.45f;
    float line = SDL_max(1.5f * ios.layout.unit, 1);
    fill_shape(v, radius, pressed ? PRESSED : FILL);
    rimmed_stroke(v, radius, line, STROKE);
    if (label) {
        float k = SDL_max(1, SDL_floorf(SDL_min(v.h * 0.42f / 7, v.w * 0.7f / (6 * strlen(label)))));
        draw_centered(v, k, label, LABEL);
    }
}

static void draw_pause(bool paused) {
    TouchRect v = ios.layout.visual[TOUCH_PAUSE];
    draw_button(TOUCH_PAUSE, false, NULL);
    float cx = v.x + v.w / 2, cy = v.y + v.h / 2, s = v.w * 0.22f;
    float rim = SDL_max(1, ios.layout.unit);
    if (paused) /* a play triangle: tap to resume */
        rimmed_triangle((SDL_FPoint){cx - s * 0.7f, cy - s}, (SDL_FPoint){cx + s, cy},
                        (SDL_FPoint){cx - s * 0.7f, cy + s}, rim, LABEL);
    else {
        SDL_FRect bars[2] = {{cx - s * 0.8f, cy - s, s * 0.55f, 2 * s},
                             {cx + s * 0.25f, cy - s, s * 0.55f, 2 * s}};
        SDL_FRect rims[2];
        for (int i = 0; i < 2; i++)
            rims[i] = (SDL_FRect){bars[i].x - rim, bars[i].y - rim, bars[i].w + 2 * rim,
                                  bars[i].h + 2 * rim};
        SDL_SetRenderDrawColor(ios.renderer, SHADOW.r, SHADOW.g, SHADOW.b, SHADOW.a);
        SDL_RenderFillRectsF(ios.renderer, rims, 2);
        SDL_SetRenderDrawColor(ios.renderer, LABEL.r, LABEL.g, LABEL.b, LABEL.a);
        SDL_RenderFillRectsF(ios.renderer, bars, 2);
    }
}

static void draw_overlay(unsigned keys) {
    const TouchLayout *l = &ios.layout;
    TouchRect d = l->visual[TOUCH_DPAD];
    float cx = d.x + d.w / 2, cy = d.y + d.h / 2, arm = d.w * 0.31f, len = d.w * 0.43f;
    float line = SDL_max(1.5f * l->unit, 1);
    fill_shape(d, d.w / 2, (SDL_Color){255, 255, 255, 22});
    rimmed_stroke(d, d.w / 2, line, STROKE);
    TouchRect horizontal = {cx - len, cy - arm / 2, 2 * len, arm},
              vertical = {cx - arm / 2, cy - len, arm, 2 * len};
    /* A faint dark base under the cross so it still shows on a white picture. */
    fill_shape(horizontal, arm * 0.25f, (SDL_Color){0, 0, 0, 36});
    fill_shape(vertical, arm * 0.25f, (SDL_Color){0, 0, 0, 36});
    fill_shape(horizontal, arm * 0.25f, FILL);
    fill_shape(vertical, arm * 0.25f, FILL);
    /* Held directions light up from the centre to the arm's end. */
    const struct {
        unsigned key;
        TouchRect half;
        float dx, dy;
    } arms[] = {{TOUCH_KEY_RIGHT, {cx, cy - arm / 2, len, arm}, 1, 0},
                {TOUCH_KEY_LEFT, {cx - len, cy - arm / 2, len, arm}, -1, 0},
                {TOUCH_KEY_UP, {cx - arm / 2, cy - len, arm, len}, 0, -1},
                {TOUCH_KEY_DOWN, {cx - arm / 2, cy, arm, len}, 0, 1}};
    for (int i = 0; i < 4; i++) {
        if (keys & arms[i].key)
            fill_shape(arms[i].half, arm * 0.25f, PRESSED);
        float tip = len * 0.86f, base = len * 0.58f, w = arm * 0.28f;
        float dx = arms[i].dx, dy = arms[i].dy;
        rimmed_triangle((SDL_FPoint){cx + dx * tip, cy + dy * tip},
                        (SDL_FPoint){cx + dx * base - dy * w, cy + dy * base + dx * w},
                        (SDL_FPoint){cx + dx * base + dy * w, cy + dy * base - dx * w}, line,
                        (keys & arms[i].key) ? ACCENT : ARROW);
    }
    draw_button(TOUCH_A, keys & TOUCH_KEY_A, "A");
    draw_button(TOUCH_B, keys & TOUCH_KEY_B, "B");
    draw_button(TOUCH_L, keys & TOUCH_KEY_L, "L");
    draw_button(TOUCH_R, keys & TOUCH_KEY_R, "R");
    draw_button(TOUCH_START, keys & TOUCH_KEY_START, "START");
    draw_button(TOUCH_SELECT, keys & TOUCH_KEY_SELECT, "SELECT");
}

unsigned ios_keys(void) {
    return touch_keys(&ios.touch, &ios.layout);
}

void ios_present(SDL_Texture *texture, const uint32_t *pixels) {
    if (ios.background)
        return;
    layout();
    SDL_Renderer *r = ios.renderer;
    SDL_UpdateTexture(texture, NULL, pixels, 240 * 4);
    SDL_SetRenderDrawBlendMode(r, SDL_BLENDMODE_BLEND);
    SDL_SetRenderDrawColor(r, 0, 0, 0, 255);
    SDL_RenderClear(r);
    TouchRect g = ios.layout.game;
    SDL_FRect dst = {g.x, g.y, g.w, g.h};
    SDL_RenderCopyF(r, texture, NULL, &dst);
    bool paused = ios.desktop && ios.desktop->paused;
    if (ios.overlay && !paused)
        draw_overlay(ios_keys());
    if (ios.overlay || paused)
        draw_pause(paused);
    SDL_RenderPresent(r);
}

/* ---- events ----------------------------------------------------------------------------- */

static void reopen_audio(void) {
    ios.reopen_audio = false;
    if (!ios.audio || !ios.audio->device || !ios.desktop)
        return;
    /* After a call, Siri or a long stay in the background the old output can be stale. */
    audio_close(ios.audio);
    ios.audio->started = false;
    if (!audio_open(ios.audio))
        ios.desktop->muted = true;
}

void ios_event(const SDL_Event *e, int *command) {
    Desktop *d = ios.desktop;
    if (ios.reopen_audio)
        reopen_audio();
    switch (e->type) {
    case SDL_FINGERDOWN: {
        ios.overlay = true;
        layout();
        float x = e->tfinger.x * ios.layout.width, y = e->tfinger.y * ios.layout.height;
        if (d && d->paused) {
            float gx, gy;
            if (touch_hit(&ios.layout, x, y) == TOUCH_PAUSE)
                *command = 1;
            else if (touch_to_game(&ios.layout, x, y, &gx, &gy)) {
                if (d->confirm_reset) {
                    int row = touch_menu_item(gx, gy, 4);
                    if (row == 2)
                        *command = 6;
                    else if (row == 3)
                        *command = 7;
                } else {
                    int row = touch_menu_item(gx, gy, desktop_menu_count);
                    if (row >= 0) {
                        d->selected = row;
                        *command = 6;
                    }
                }
            }
            break;
        }
        if (touch_down(&ios.touch, &ios.layout, e->tfinger.fingerId, x, y) == TOUCH_PAUSE)
            *command = 1;
        break;
    }
    case SDL_FINGERMOTION:
        touch_move(&ios.touch, e->tfinger.fingerId, e->tfinger.x * ios.layout.width,
                   e->tfinger.y * ios.layout.height);
        break;
    case SDL_FINGERUP:
        touch_up(&ios.touch, e->tfinger.fingerId);
        break;
    case SDL_CONTROLLERBUTTONDOWN:
        ios.overlay = false;
        break;
    case SDL_CONTROLLERAXISMOTION:
        if (e->caxis.value > 16000 || e->caxis.value < -16000)
            ios.overlay = false;
        break;
    case SDL_CONTROLLERDEVICEREMOVED:
        ios.overlay = true;
        break;
    case SDL_DROPFILE:
        /* A dump shared while the game already runs: nothing to do now. */
        SDL_free(e->drop.file);
        break;
    case SDL_AUDIODEVICEREMOVED:
        if (ios.audio && !e->adevice.iscapture && e->adevice.which == ios.audio->device) {
            ios.reopen_audio = true;
            reopen_audio();
        }
        break;
    }
}

/* ---- the ROM screen --------------------------------------------------------------------- */

static void printable(char *out, size_t size, const char *name) {
    size_t n = 0;
    for (const char *s = name; *s && n + 4 < size; s++) {
        int c = (unsigned char)*s;
        if (c >= 'a' && c <= 'z')
            c -= 32;
        out[n++] = (char)((c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || strchr(" .-_()'!+=", c)
                              ? c
                              : '?');
        if (n == 32 && s[1]) {
            memcpy(out + n, "...", 3);
            n += 3;
            break;
        }
    }
    out[n] = 0;
}

static void draw_rom_screen(const RomScan *scan, bool build_mismatch) {
    layout();
    SDL_Renderer *r = ios.renderer;
    SDL_SetRenderDrawBlendMode(r, SDL_BLENDMODE_BLEND);
    SDL_SetRenderDrawColor(r, 18, 17, 15, 255);
    SDL_RenderClear(r);
    char problem[160] = "", name[48];
    if (build_mismatch)
        snprintf(problem, sizeof(problem), "THIS APP BUILD DOES NOT MATCH THAT DUMP.");
    else if (scan->result == ROM_SCAN_WRONG && scan->candidates == 1) {
        printable(name, sizeof(name), scan->name);
        snprintf(problem, sizeof(problem), "%s IS NOT THE SUPPORTED DUMP.", name);
    } else if (scan->result == ROM_SCAN_WRONG)
        snprintf(problem, sizeof(problem), "NONE OF THE %d .GBA FILES IS THE SUPPORTED DUMP.",
                 scan->candidates);
    const char *lines[] = {problem,
                           "NO GAME DATA IS INCLUDED. TXRA PLAYS YOUR OWN",
                           "DUMP OF THE CARTRIDGE:",
                           "",
                           "1. OPEN THE FILES APP.",
                           "2. GO TO ON MY IPHONE > TXRA.",
                           "3. PUT YOUR .GBA DUMP THERE (4 MIB, ANY NAME).",
                           "   OR SHARE THE FILE TO TXRA FROM ANOTHER APP.",
                           "4. COME BACK AND TAP THE SCREEN.",
                           "",
                           "SHA-1 OF THE SUPPORTED DUMP:",
                           "4197339D4ADD74BB40ED02A8FBA5E58096AFB487"};
    enum { LINES = sizeof(lines) / sizeof(lines[0]) };
    TouchRect s = ios.layout.safe;
    size_t widest = 0;
    for (int i = 0; i < LINES; i++)
        widest = SDL_max(widest, strlen(lines[i]));
    float k = SDL_floorf(SDL_min(s.w * 0.9f / (widest * 6), s.h * 0.86f / ((LINES + 3) * 11)));
    k = SDL_max(k, 1);
    float x = s.x + (s.w - widest * 6 * k) / 2, y = s.y + (s.h - (LINES + 3) * 11 * k) / 2;
    draw_text(x, y, 2 * k, "TXRA", ACCENT);
    y += 3 * 11 * k;
    for (int i = 0; i < LINES; i++, y += 11 * k)
        draw_text(x, y, k, lines[i], i == 0 ? ACCENT : (SDL_Color){255, 239, 208, 255});
    SDL_RenderPresent(r);
}

bool ios_find_rom(uint8_t *rom, size_t size) {
    const char *folder = ios_documents();
    bool rescan = true, mismatch = false;
    RomScan scan = {ROM_SCAN_NONE, 0, ""};
    for (;;) {
        if (rescan) {
            rescan = false;
            scan = rom_scan(folder, TXRA_ROM_SHA1, rom, size);
            fprintf(stderr, "ROM scan: %s (%d .gba files)\n",
                    scan.result == ROM_SCAN_FOUND   ? scan.name
                    : scan.result == ROM_SCAN_WRONG ? "no supported dump"
                                                    : "no .gba file",
                    scan.candidates);
            if (scan.result == ROM_SCAN_FOUND) {
                u32 crc = ~0u;
                for (size_t i = 0; i < size; i++) {
                    crc ^= rom[i];
                    for (unsigned b = 0; b < 8; b++)
                        crc = (crc >> 1) ^ (0xedb88320u & (0u - (crc & 1)));
                }
                if (~crc == recompiled_rom_crc) {
                    /* Leaving the app while this screen showed set the pause flag; there was
                       no game to pause yet, so start playing. */
                    if (ios.desktop)
                        ios.desktop->paused = false;
                    return true;
                }
                mismatch = true;
                memset(rom, 0, size);
            }
        }
        if (!ios.background)
            draw_rom_screen(&scan, mismatch);
        SDL_Event e;
        if (!SDL_WaitEventTimeout(&e, 500))
            continue;
        do {
            switch (e.type) {
            case SDL_QUIT:
                return false;
            case SDL_FINGERUP:
            case SDL_APP_DIDENTERFOREGROUND:
                rescan = true;
                break;
            case SDL_CONTROLLERBUTTONDOWN:
                if (e.cbutton.button == SDL_CONTROLLER_BUTTON_A ||
                    e.cbutton.button == SDL_CONTROLLER_BUTTON_START)
                    rescan = true;
                break;
            case SDL_KEYDOWN:
                if (e.key.keysym.sym == SDLK_RETURN)
                    rescan = true;
                break;
            case SDL_DROPFILE: {
                /* Shared with the app ("Open in TXRA"): keep a copy in Documents. */
                char copied[4096];
                if (rom_import(e.drop.file, folder, copied, sizeof(copied)))
                    fprintf(stderr, "Imported shared file into Documents\n");
                SDL_free(e.drop.file);
                rescan = true;
                break;
            }
            }
        } while (SDL_PollEvent(&e));
    }
}
