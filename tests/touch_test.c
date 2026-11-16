/* iPhone on-screen controls and ROM finder: plain C, runs on Linux (make check-touch). */
#define _DEFAULT_SOURCE
#include "romscan.h"
#include "touch.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
static unsigned checks;
#define CHECK(c)                                                                                   \
    do {                                                                                           \
        checks++;                                                                                  \
        if (!(c)) {                                                                                \
            fprintf(stderr, "touch check %u failed (line %d): %s\n", checks, __LINE__, #c);        \
            exit(1);                                                                               \
        }                                                                                          \
    } while (0)

static float cx(TouchRect r) {
    return r.x + r.w / 2;
}
static float cy(TouchRect r) {
    return r.y + r.h / 2;
}
static bool within(TouchRect inner, TouchRect outer) {
    return inner.x >= outer.x - 0.5f && inner.y >= outer.y - 0.5f &&
           inner.x + inner.w <= outer.x + outer.w + 0.5f &&
           inner.y + inner.h <= outer.y + outer.h + 0.5f;
}
static bool overlap(TouchRect a, TouchRect b) {
    return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}
static int popcount(unsigned v) {
    int n = 0;
    for (; v; v &= v - 1)
        n++;
    return n;
}

/* Geometry every phone must satisfy. */
static void check_layout_scale(const char *name, int w, int h, float unit, float il, float it,
                               float ir, float ib, bool integer) {
    TouchLayout l;
    touch_layout(&l, w, h, unit, il, it, ir, ib, integer);
    TouchRect g = l.game;
    CHECK(within(g, l.safe));
    CHECK(fabsf(g.w / g.h - 1.5f) < 0.01f);
    if (integer) /* the largest whole-number scale that fits */
        CHECK(fmodf(g.w, 240) == 0 && (g.w + 240 > l.safe.w || g.h + 160 > l.safe.h));
    else /* fills the safe height (wide phones) or width (narrow ones) */
        CHECK(fabsf(g.h - l.safe.h) < 1.5f || fabsf(g.w - l.safe.w) < 1.5f);
    CHECK(fabsf(cx(g) - cx(l.safe)) <= 1 && fabsf(cy(g) - cy(l.safe)) <= 1);
    CHECK(g.x == floorf(g.x) && g.w == floorf(g.w));
    for (int i = 0; i < TOUCH_CONTROLS; i++) {
        CHECK(within(l.visual[i], l.safe));
        CHECK(l.visual[i].w >= 30 * unit && l.visual[i].h >= 30 * unit); /* finger sized */
        CHECK(within(l.visual[i], l.hit[i]));
        /* The middle of every control hits that control. */
        CHECK(touch_hit(&l, cx(l.visual[i]), cy(l.visual[i])) == i);
        for (int j = i + 1; j < TOUCH_CONTROLS; j++) {
            TouchRect a = l.visual[i], b = l.visual[j];
            if (l.round[i] && l.round[j]) /* circles: centre distance */
                CHECK(hypotf(cx(a) - cx(b), cy(a) - cy(b)) >= (a.w + b.w) / 2);
            else
                CHECK(!overlap(a, b));
        }
    }
    /* Controls sit on the sides: the left ones left of the picture centre, right ones right. */
    int left[] = {TOUCH_DPAD, TOUCH_L, TOUCH_SELECT, TOUCH_PAUSE};
    int right[] = {TOUCH_A, TOUCH_B, TOUCH_R, TOUCH_START};
    for (int i = 0; i < 4; i++) {
        CHECK(cx(l.visual[left[i]]) < cx(g) - g.w / 4);
        CHECK(cx(l.visual[right[i]]) > cx(g) + g.w / 4);
    }
    /* The middle half of the picture is never covered by a control. */
    TouchRect middle = {g.x + g.w / 4, g.y, g.w / 2, g.h};
    for (int i = 0; i < TOUCH_CONTROLS; i++)
        CHECK(!overlap(l.visual[i], middle));
    CHECK(touch_hit(&l, cx(g), cy(g)) == TOUCH_NONE);
    /* Scan the whole screen: only A and B may be pressed together by one finger. */
    float step = unit * 2;
    long covered = 0, total = 0;
    for (float y = 0.5f; y < h; y += step)
        for (float x = 0.5f; x < w; x += step) {
            unsigned keys = touch_button_keys(&l, x, y);
            CHECK(popcount(keys) <= 1 || keys == (TOUCH_KEY_A | TOUCH_KEY_B));
            total++;
            if (x >= g.x && x < g.x + g.w && y >= g.y && y < g.y + g.h &&
                (touch_hit(&l, x, y) != TOUCH_NONE))
                covered++;
        }
    /* Share of the picture under drawn controls, and under their (larger) hit areas. */
    long drawn = 0, pixels = 0;
    for (float y = g.y + 0.5f; y < g.y + g.h; y += step)
        for (float x = g.x + 0.5f; x < g.x + g.w; x += step) {
            pixels++;
            for (int i = 0; i < TOUCH_CONTROLS; i++) {
                TouchRect v = l.visual[i];
                bool in = l.round[i] ? hypotf(x - cx(v), y - cy(v)) <= v.w / 2
                                     : x >= v.x && x < v.x + v.w && y >= v.y && y < v.y + v.h;
                if (in) {
                    drawn++;
                    break;
                }
            }
        }
    double share = 100.0 * covered / pixels, drawn_share = 100.0 * drawn / pixels;
    printf("%-26s %4dx%-4d @%.0fx %-7s picture %4.0fx%-4.0f covered: drawn %4.1f%%, hit areas "
           "%4.1f%%\n",
           name, w, h, unit, integer ? "integer" : "fill", g.w, g.h, drawn_share, share);
    CHECK(share < 30 && drawn_share < 15);
    /* B never sits further left than the diagonal, and is never left of A's column on a
       phone where it would fit beside the picture. */
    TouchRect a = l.visual[TOUCH_A], b = l.visual[TOUCH_B];
    CHECK(cx(b) <= cx(a) && cx(b) >= cx(a) - 0.61f * a.w && cy(b) > cy(a));
    /* Wide phones: every control but the D-pad sits entirely beside the picture, so the race
       HUD (speed and gear in the bottom-right corner) stays clear. */
    if ((float)w / h > 2) {
        int beside[] = {TOUCH_L, TOUCH_R, TOUCH_START, TOUCH_SELECT, TOUCH_PAUSE, TOUCH_A, TOUCH_B};
        for (int i = 0; i < 7; i++)
            CHECK(!overlap(l.visual[beside[i]], g));
        CHECK(drawn_share < 4);
    }
    /* Whenever A fits beside the picture, B does too. */
    if (!overlap(a, g))
        CHECK(!overlap(b, g));
    /* The scale a phone starts with: fill where A fits beside the picture (every phone with
       a notch or Dynamic Island), integer on 16:9 phones. */
    CHECK(touch_default_integer(w, h, unit, il, it, ir, ib) == ((float)w / h < 2));
    (void)total;
}
static void check_layout(const char *name, int w, int h, float unit, float il, float it, float ir,
                         float ib) {
    check_layout_scale(name, w, h, unit, il, it, ir, ib, false);
    check_layout_scale(name, w, h, unit, il, it, ir, ib, true);
}

/* A 4.7-inch 16:9 phone starts in integer scale: then every control but the D-pad is beside
   the picture, as on the wide phones. */
static void check_small_phone_integer(void) {
    TouchLayout l;
    touch_layout(&l, 1334, 750, 2, 0, 0, 0, 0, true);
    CHECK(l.game.w == 960 && l.game.h == 640);
    int beside[] = {TOUCH_L, TOUCH_R, TOUCH_START, TOUCH_SELECT, TOUCH_PAUSE, TOUCH_A, TOUCH_B};
    for (int i = 0; i < 7; i++)
        CHECK(!overlap(l.visual[beside[i]], l.game));
}

static void check_dpad_and_fingers(void) {
    TouchLayout l;
    touch_layout(&l, 2796, 1290, 3, 177, 0, 177, 63, false); /* 6.7-inch class phone */
    TouchRect d = l.visual[TOUCH_DPAD];
    float x = cx(d), y = cy(d), r = d.w / 2;
    CHECK(touch_dpad_keys(&l, x, y) == 0);                 /* dead zone */
    CHECK(touch_dpad_keys(&l, x + r * 0.1f, y) == 0);
    static const struct {
        float angle;
        unsigned keys;
    } dirs[] = {{0, TOUCH_KEY_RIGHT},
                {45, TOUCH_KEY_RIGHT | TOUCH_KEY_UP},
                {90, TOUCH_KEY_UP},
                {135, TOUCH_KEY_UP | TOUCH_KEY_LEFT},
                {180, TOUCH_KEY_LEFT},
                {225, TOUCH_KEY_LEFT | TOUCH_KEY_DOWN},
                {270, TOUCH_KEY_DOWN},
                {315, TOUCH_KEY_DOWN | TOUCH_KEY_RIGHT},
                {20, TOUCH_KEY_RIGHT},
                {25, TOUCH_KEY_RIGHT | TOUCH_KEY_UP},
                {65, TOUCH_KEY_RIGHT | TOUCH_KEY_UP},
                {70, TOUCH_KEY_UP}};
    for (size_t i = 0; i < sizeof(dirs) / sizeof(dirs[0]); i++) {
        float a = dirs[i].angle * 3.14159265f / 180;
        for (float k = 0.3f; k <= 3.0f; k += 0.9f) /* also far outside: a held finger slides */
            CHECK(touch_dpad_keys(&l, x + cosf(a) * r * k, y - sinf(a) * r * k) == dirs[i].keys);
    }
    /* Every one of the 8 directions is reachable and no opposite pair ever appears. */
    for (int deg = 0; deg < 360; deg++) {
        float a = deg * 3.14159265f / 180;
        unsigned k = touch_dpad_keys(&l, x + cosf(a) * r * 0.6f, y - sinf(a) * r * 0.6f);
        CHECK(k && popcount(k) <= 2);
        CHECK((k & (TOUCH_KEY_LEFT | TOUCH_KEY_RIGHT)) != (TOUCH_KEY_LEFT | TOUCH_KEY_RIGHT));
        CHECK((k & (TOUCH_KEY_UP | TOUCH_KEY_DOWN)) != (TOUCH_KEY_UP | TOUCH_KEY_DOWN));
    }
    /* A and B: each alone at its centre, both between them. */
    TouchRect a = l.visual[TOUCH_A], b = l.visual[TOUCH_B];
    CHECK(touch_button_keys(&l, cx(a), cy(a)) == TOUCH_KEY_A);
    CHECK(touch_button_keys(&l, cx(b), cy(b)) == TOUCH_KEY_B);
    CHECK(touch_button_keys(&l, (cx(a) + cx(b)) / 2, (cy(a) + cy(b)) / 2) ==
          (TOUCH_KEY_A | TOUCH_KEY_B));
    /* Shoulders reach into the screen corners. */
    CHECK(touch_hit(&l, 1, 1) == TOUCH_L);
    CHECK(touch_hit(&l, 2795, 1) == TOUCH_R);

    /* Multitouch: steer and accelerate at once, slide, lift. */
    TouchState s;
    touch_reset(&s);
    CHECK(touch_keys(&s, &l) == 0);
    CHECK(touch_down(&s, &l, 101, x + r * 0.7f, y) == TOUCH_DPAD);
    CHECK(touch_down(&s, &l, 202, cx(a), cy(a)) == TOUCH_A);
    CHECK(touch_keys(&s, &l) == (TOUCH_KEY_RIGHT | TOUCH_KEY_A));
    touch_move(&s, 101, x - r * 0.5f, y - r * 0.5f); /* slide to up-left */
    CHECK(touch_keys(&s, &l) == (TOUCH_KEY_UP | TOUCH_KEY_LEFT | TOUCH_KEY_A));
    touch_move(&s, 101, x + r * 2.5f, y); /* far off the pad, still steering right */
    touch_move(&s, 202, cx(b), cy(b));    /* slide from A to B */
    CHECK(touch_keys(&s, &l) == (TOUCH_KEY_RIGHT | TOUCH_KEY_B));
    touch_move(&s, 202, cx(l.game), cy(l.game)); /* off every button: released */
    CHECK(touch_keys(&s, &l) == TOUCH_KEY_RIGHT);
    touch_up(&s, 101);
    CHECK(touch_keys(&s, &l) == 0);
    touch_up(&s, 202);
    /* A finger landing on the picture does nothing, even if it slides onto a button. */
    CHECK(touch_down(&s, &l, 303, cx(l.game), cy(l.game)) == TOUCH_NONE);
    touch_move(&s, 303, cx(a), cy(a));
    CHECK(touch_keys(&s, &l) == 0);
    touch_up(&s, 303);
    /* Pause is reported to the caller and holds no game key. */
    TouchRect p = l.visual[TOUCH_PAUSE];
    CHECK(touch_down(&s, &l, 404, cx(p), cy(p)) == TOUCH_PAUSE);
    CHECK(touch_keys(&s, &l) == 0);
    touch_up(&s, 404);
    /* Start, Select, L, R. */
    int controls[] = {TOUCH_START, TOUCH_SELECT, TOUCH_L, TOUCH_R};
    unsigned keys[] = {TOUCH_KEY_START, TOUCH_KEY_SELECT, TOUCH_KEY_L, TOUCH_KEY_R};
    for (int i = 0; i < 4; i++) {
        TouchRect v = l.visual[controls[i]];
        touch_down(&s, &l, 500 + i, cx(v), cy(v));
        CHECK(touch_keys(&s, &l) == keys[i]);
        touch_up(&s, 500 + i);
    }
    /* Eleven fingers: the tenth slot fills, nothing breaks, all lift cleanly. */
    for (int i = 0; i < 11; i++)
        touch_down(&s, &l, 1000 + i, cx(a), cy(a));
    CHECK(touch_keys(&s, &l) == TOUCH_KEY_A);
    for (int i = 0; i < 11; i++)
        touch_up(&s, 1000 + i);
    CHECK(touch_keys(&s, &l) == 0);
    /* The same finger id going down twice reuses its slot. */
    touch_down(&s, &l, 7, cx(a), cy(a));
    touch_down(&s, &l, 7, cx(b), cy(b));
    CHECK(touch_keys(&s, &l) == TOUCH_KEY_B);
    touch_up(&s, 7);
    CHECK(touch_keys(&s, &l) == 0);
}

static void check_menu_mapping(void) {
    TouchLayout l;
    touch_layout(&l, 2796, 1290, 3, 177, 0, 177, 63, false);
    float gx, gy;
    CHECK(touch_to_game(&l, l.game.x, l.game.y, &gx, &gy) && gx == 0 && gy == 0);
    CHECK(touch_to_game(&l, l.game.x + l.game.w - 0.01f, l.game.y + l.game.h - 0.01f, &gx, &gy));
    CHECK(gx > 239.9f && gx < 240 && gy > 159.9f && gy < 160);
    CHECK(!touch_to_game(&l, l.game.x - 1, cy(l.game), &gx, &gy));
    CHECK(!touch_to_game(&l, cx(l.game), l.game.y + l.game.h, &gx, &gy));
    CHECK(touch_menu_item(TOUCH_MENU_X + 1, TOUCH_MENU_Y + 1, 5) == 0);
    CHECK(touch_menu_item(TOUCH_MENU_X + 1, TOUCH_MENU_Y + TOUCH_MENU_STEP, 5) == 1);
    CHECK(touch_menu_item(TOUCH_MENU_X + 100, TOUCH_MENU_Y + 4 * TOUCH_MENU_STEP + 5, 5) == 4);
    CHECK(touch_menu_item(TOUCH_MENU_X + 100, TOUCH_MENU_Y + 5 * TOUCH_MENU_STEP + 1, 5) == -1);
    CHECK(touch_menu_item(TOUCH_MENU_X - 1, TOUCH_MENU_Y + 1, 5) == -1);
    CHECK(touch_menu_item(TOUCH_MENU_X + TOUCH_MENU_W, TOUCH_MENU_Y + 1, 5) == -1);
    CHECK(touch_menu_item(TOUCH_MENU_X + 1, TOUCH_MENU_Y - 1, 5) == -1);
    /* Rows are at least 44 points tall on a 6.7-inch phone (Apple's minimum touch size). */
    CHECK(TOUCH_MENU_STEP * l.game.h / 160 / l.unit >= 44);
    /* Whole-number scale when asked. */
    touch_layout(&l, 2796, 1290, 3, 177, 0, 177, 63, true);
    CHECK(l.game.w == 240 * 7 && l.game.h == 160 * 7);
    touch_layout(&l, 100, 60, 1, 0, 0, 0, 0, true); /* smaller than 1x: fits anyway */
    CHECK(l.game.w <= 100 && l.game.h <= 60);
}

static void write_file(const char *path, const uint8_t *data, size_t n) {
    FILE *f = fopen(path, "wb");
    CHECK(f && fwrite(data, 1, n, f) == n);
    fclose(f);
}

static void check_sha1_and_scan(void) {
    char hex[41];
    rom_sha1_hex((const uint8_t *)"abc", 3, hex);
    CHECK(!strcmp(hex, "a9993e364706816aba3e25717850c26c9cd0d89d"));
    rom_sha1_hex((const uint8_t *)"", 0, hex);
    CHECK(!strcmp(hex, "da39a3ee5e6b4b0d3255bfef95601890afd80709"));
    const char *two = "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq";
    rom_sha1_hex((const uint8_t *)two, strlen(two), hex);
    CHECK(!strcmp(hex, "84983e441c3bd26ebaae4aa1f95129e5e54670f1"));
    uint8_t *million = malloc(1000000);
    CHECK(million != NULL);
    memset(million, 'a', 1000000);
    rom_sha1_hex(million, 1000000, hex);
    CHECK(!strcmp(hex, "34aa973cd4c4daa4f61eeb2bdbad27316534016f"));
    free(million);
    for (size_t n = 50; n < 140; n++) { /* padding boundaries: 55, 56, 63, 64, 119, 120 */
        uint8_t buf[140];
        memset(buf, (int)n, n);
        rom_sha1_hex(buf, n, hex);
        CHECK(strlen(hex) == 40);
    }

    enum { SIZE = 65536 };
    uint8_t *good = malloc(SIZE), *bad = malloc(SIZE), *out = malloc(SIZE);
    CHECK(good && bad && out);
    for (unsigned i = 0; i < SIZE; i++) {
        good[i] = (uint8_t)(i * 7 + (i >> 8));
        bad[i] = (uint8_t)(i * 13);
    }
    char want[41];
    rom_sha1_hex(good, SIZE, want);
    char dir[] = "/tmp/txra-touch-XXXXXX";
    CHECK(mkdtemp(dir) != NULL);
    char path[1024], inbox[512];
    snprintf(inbox, sizeof(inbox), "%s/Inbox", dir);

    RomScan r = rom_scan(dir, want, out, SIZE);
    CHECK(r.result == ROM_SCAN_NONE && r.candidates == 0);
    snprintf(path, sizeof(path), "%s/notes.txt", dir);
    write_file(path, good, SIZE); /* right bytes, wrong extension: ignored */
    snprintf(path, sizeof(path), "%s/.hidden.gba", dir);
    write_file(path, good, SIZE);
    r = rom_scan(dir, want, out, SIZE);
    CHECK(r.result == ROM_SCAN_NONE);
    snprintf(path, sizeof(path), "%s/small.gba", dir);
    write_file(path, good, 100);
    snprintf(path, sizeof(path), "%s/Zeta.GBA", dir);
    write_file(path, bad, SIZE);
    r = rom_scan(dir, want, out, SIZE);
    CHECK(r.result == ROM_SCAN_WRONG && r.candidates == 2);
    CHECK(!strcmp(r.name, "Zeta.GBA")); /* byte order: uppercase first */
    for (unsigned i = 0; i < SIZE; i++)
        CHECK(out[i] == 0);          /* refused data is not left in the buffer */
    CHECK(mkdir(inbox, 0700) == 0);
    snprintf(path, sizeof(path), "%s/shared.gba", inbox);
    write_file(path, good, SIZE);
    r = rom_scan(dir, want, out, SIZE);
    CHECK(r.result == ROM_SCAN_FOUND && !strcmp(r.name, "shared.gba"));
    CHECK(!memcmp(out, good, SIZE));
    snprintf(path, sizeof(path), "%s/other.gba", dir);
    write_file(path, good, SIZE);
    r = rom_scan(dir, want, out, SIZE);
    CHECK(r.result == ROM_SCAN_FOUND && !strcmp(r.name, "other.gba")); /* Documents first */
    snprintf(path, sizeof(path), "%s/baserom.gba", dir);
    write_file(path, good, SIZE);
    r = rom_scan(dir, want, out, SIZE);
    CHECK(r.result == ROM_SCAN_FOUND && !strcmp(r.name, "baserom.gba")); /* preferred name */
    write_file(path, bad, SIZE); /* a wrong baserom.gba falls through to the next file */
    r = rom_scan(dir, want, out, SIZE);
    CHECK(r.result == ROM_SCAN_FOUND && !strcmp(r.name, "other.gba"));

    /* Importing a shared file: own name, then a numbered name, never an overwrite. */
    char imported[1024], src[1024];
    snprintf(src, sizeof(src), "%s/shared.gba", inbox);
    CHECK(rom_import(src, dir, imported, sizeof(imported)));
    snprintf(path, sizeof(path), "%s/shared.gba", dir);
    CHECK(!strcmp(imported, path));
    CHECK(rom_import(src, dir, imported, sizeof(imported)));
    snprintf(path, sizeof(path), "%s/shared-2.gba", dir);
    CHECK(!strcmp(imported, path));
    snprintf(path, sizeof(path), "%s/other.gba", dir);
    CHECK(rom_import(path, dir, imported, sizeof(imported)) && !strcmp(imported, path));
    snprintf(path, sizeof(path), "%s/notes.txt", dir);
    CHECK(!rom_import(path, dir, imported, sizeof(imported)));
    snprintf(path, sizeof(path), "%s/missing.gba", inbox);
    CHECK(!rom_import(path, dir, imported, sizeof(imported)));
    free(good);
    free(bad);
    free(out);
    char command[600];
    snprintf(command, sizeof(command), "rm -r -- '%s'", dir);
    CHECK(system(command) == 0);
}

int main(void) {
    /* Landscape drawable sizes in pixels with safe-area insets (points x scale). */
    check_layout("6.9-inch, Dynamic Island", 2868, 1320, 3, 186, 0, 186, 63);
    check_layout("6.7-inch, Dynamic Island", 2796, 1290, 3, 177, 0, 177, 63);
    check_layout("6.1-inch, Dynamic Island", 2556, 1179, 3, 177, 0, 177, 63);
    check_layout("6.1-inch, notch", 2532, 1170, 3, 141, 0, 141, 63);
    check_layout("5.4-inch, notch", 2340, 1080, 3, 150, 0, 150, 63);
    check_layout("4.7-inch 16:9, Home button", 1334, 750, 2, 0, 0, 0, 0);
    check_layout("4.0-inch 16:9 (smallest)", 1136, 640, 2, 0, 0, 0, 0);
    check_small_phone_integer();
    check_dpad_and_fingers();
    check_menu_mapping();
    check_sha1_and_scan();
    printf("%u touch and ROM-finder assertions passed\n", checks);
}
