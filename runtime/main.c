#include "audio.h"
#include "desktop.h"
#include "gba.h"
#include "input.h"
#include <SDL.h>
#include <errno.h>
#include <inttypes.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <fcntl.h>
#include <io.h>
#include <sys/stat.h>
/* The Windows build uses the GUI subsystem, so it starts without a console.
   Reuse the launching console when there is one; otherwise startup errors are
   shown in a dialog and the log goes to last-run.log in the user folder. */
static bool no_console, dialogs;
static void host_console(void) {
    HANDLE err = GetStdHandle(STD_ERROR_HANDLE);
    if (err && err != INVALID_HANDLE_VALUE)
        return;
    if (AttachConsole(ATTACH_PARENT_PROCESS)) {
        freopen("CONOUT$", "w", stdout);
        freopen("CONOUT$", "w", stderr);
    } else
        no_console = dialogs = true;
}
static double cpu_time(void) {
    FILETIME created, exited, kernel, user;
    if (!GetProcessTimes(GetCurrentProcess(), &created, &exited, &kernel, &user))
        return 0;
    return ((((uint64_t)kernel.dwHighDateTime << 32) | kernel.dwLowDateTime) +
            (((uint64_t)user.dwHighDateTime << 32) | user.dwLowDateTime)) /
           1e7;
}
#endif
static void fatal(const char *format, ...) {
    char message[1024];
    va_list args;
    va_start(args, format);
    vsnprintf(message, sizeof(message), format, args);
    va_end(args);
    fprintf(stderr, "%s\n", message);
#ifdef _WIN32
    if (dialogs)
        SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_ERROR, "TXRA", message, NULL);
#endif
}
static void capture(GBA *g, const char *path) {
    FILE *f = fopen(path, "wb");
    if (!f) {
        perror(path);
        return;
    }
    fprintf(f, "P6\n240 160\n255\n");
    for (unsigned i = 0; i < 240 * 160; i++) {
        uint8_t b[] = {g->pixels[i] >> 16, g->pixels[i] >> 8, g->pixels[i]};
        fwrite(b, 1, 3, f);
    }
    fclose(f);
}
static void boot(GBA *g, const char *save, FILE *unknown, bool trace) {
    /* Retain the supplied ROM; initialize only machine state. */
    memset(g, 0, offsetof(GBA, rom));
    memset(g->ewram, 0, sizeof(*g) - offsetof(GBA, ewram));
    memset(g->eeprom, 255, sizeof(g->eeprom));
    g->save_path = save;
    g->unknown = unknown;
    g->trace = trace;
    FILE *f = fopen(save, "rb");
    if (f) {
        size_t n = fread(g->eeprom, 1, sizeof(g->eeprom), f);
        if (ferror(f))
            fprintf(stderr, "Save read failed after %zu bytes\n", n);
        fclose(f);
    }
    g->audio_hash = 14695981039346656037ULL;
    g->r[15] = 0x08000000;
    g->cpsr = 0xd3;
    g->io[0x130] = 255;
    g->io[0x131] = 3;
    g->io[0x21] = g->io[0x27] = 1;
}
static void help(void) {
    puts("TXRA PC - supply your own supported ROM\n"
         "txra-pc ROM, or --rom FILE --save FILE --bindings FILE --reset-save\n"
         "--fullscreen --aspect-fit --no-vsync --no-focus-pause --mute\n"
         "Esc / controller Guide: PC menu; F11 / Alt+Enter: fullscreen\n"
         "F8: screenshot; hold Tab: 3x; hold grave: half speed\n"
         "Keyboard: X/Z A/B, Enter/Backspace Start/Select, arrows, S/A shoulders\n"
         "Controllers: south/east A/B, Options/Menu Start, Create/Back Select\n"
         "Review: --headless --benchmark --frames N --input-script FILE\n"
         "--stats FILE --frame-hashes FILE --frame-times FILE --audio-dump FILE --screenshot FILE\n"
         "--video FILE --video-start N --video-end N --snapshots DIR\n"
         "--interpreter --trace --coverage FILE --unknown-log FILE\n"
         "--ui-script FILE (frame action pairs for host review automation)");
}
int main(int argc, char **argv) {
    const char *rompath = "baserom.gba", *shot = NULL, *raw = NULL, *stats = NULL, *save = NULL,
               *binding_path = NULL, *ui_script = NULL, *input = NULL, *pcm = NULL,
               *hashpath = NULL, *snapshots = NULL, *unknown = NULL, *coverage = NULL,
               *frame_times = NULL;
    unsigned frames = 0, auto_start = 0, video_start = 0, video_end = ~0u;
    bool headless = false, mute = false, interpreter = false, trace = false, benchmark = false;
    bool reset_save = false, vsync = true, focus_pause = true;
    Desktop desktop = {.integer = true, .speed = 1};
    bool rom_given = false;
#ifdef _WIN32
    host_console();
#endif
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--help")) {
            help();
            return 0;
        } else if (!strcmp(argv[i], "--fullscreen"))
            desktop.fullscreen = true;
        else if (!strcmp(argv[i], "--aspect-fit"))
            desktop.integer = false;
        else if (!strcmp(argv[i], "--no-vsync"))
            vsync = false;
        else if (!strcmp(argv[i], "--no-focus-pause"))
            focus_pause = false;
        else if (!strcmp(argv[i], "--reset-save"))
            reset_save = true;
        else if (!strcmp(argv[i], "--bindings") && i + 1 < argc)
            binding_path = argv[++i];
        else if (!strcmp(argv[i], "--ui-script") && i + 1 < argc)
            ui_script = argv[++i];
        else if (!strcmp(argv[i], "--rom") && i + 1 < argc) {
            rompath = argv[++i];
            rom_given = true;
        }
        else if (!strcmp(argv[i], "--coverage") && i + 1 < argc)
            coverage = argv[++i];
        else if (!strcmp(argv[i], "--frames") && i + 1 < argc)
            frames = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--screenshot") && i + 1 < argc)
            shot = argv[++i];
        else if (!strcmp(argv[i], "--video") && i + 1 < argc)
            raw = argv[++i];
        else if (!strcmp(argv[i], "--stats") && i + 1 < argc)
            stats = argv[++i];
        else if (!strcmp(argv[i], "--save") && i + 1 < argc)
            save = argv[++i];
        else if (!strcmp(argv[i], "--input-script") && i + 1 < argc)
            input = argv[++i];
        else if (!strcmp(argv[i], "--auto-start") && i + 1 < argc)
            auto_start = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--benchmark"))
            benchmark = true;
        else if (!strcmp(argv[i], "--audio-dump") && i + 1 < argc)
            pcm = argv[++i];
        else if (!strcmp(argv[i], "--frame-times") && i + 1 < argc)
            frame_times = argv[++i];
        else if (!strcmp(argv[i], "--frame-hashes") && i + 1 < argc)
            hashpath = argv[++i];
        else if (!strcmp(argv[i], "--snapshots") && i + 1 < argc)
            snapshots = argv[++i];
        else if (!strcmp(argv[i], "--unknown-log") && i + 1 < argc)
            unknown = argv[++i];
        else if (!strcmp(argv[i], "--video-start") && i + 1 < argc)
            video_start = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--video-end") && i + 1 < argc)
            video_end = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--headless")) {
            headless = true;
#ifdef _WIN32
            dialogs = false;
#endif
        }
        else if (!strcmp(argv[i], "--mute"))
            mute = true;
        else if (!strcmp(argv[i], "--trace"))
            trace = true;
        else if (!strcmp(argv[i], "--interpreter"))
            interpreter = true;
        else if (argv[i][0] != '-' && !rom_given) {
            /* A bare path, as passed when a cartridge file is dropped on the executable. */
            rompath = argv[i];
            rom_given = true;
        } else {
            fatal("Unknown option: %s", argv[i]);
            return 2;
        }
    }
    GBA *g = calloc(1, sizeof(*g));
    if (!g)
        return 1;
    FILE *f = fopen(rompath, "rb");
    if (!f) {
        int error = errno;
        if (rom_given)
            fatal("Player ROM: %s\n%s", strerror(error), rompath);
        else
            fatal("Player ROM: %s\nDrop your own cartridge .gba file onto txra-pc, or run "
                  "txra-pc --rom FILE.",
                  strerror(error));
        free(g);
        return 1;
    }
    size_t n = fread(g->rom, 1, sizeof(g->rom), f);
    bool extra = fgetc(f) != EOF;
    fclose(f);
    if (n != sizeof(g->rom) || extra) {
        fatal("Expected a 4 MiB ROM");
        free(g);
        return 1;
    }
    u32 crc = ~0u;
    for (size_t i = 0; i < n; i++) {
        crc ^= g->rom[i];
        for (unsigned b = 0; b < 8; b++)
            crc = (crc >> 1) ^ (0xedb88320u & (0u - (crc & 1)));
    }
    if ((~crc) != recompiled_rom_crc) {
        fatal("ROM does not match this recompiled build; rebuild with the supported player ROM.");
        free(g);
        return 1;
    }
    if (headless)
        SDL_setenv("SDL_VIDEODRIVER", "dummy", 1);
#ifdef _WIN32
    SDL_SetMainReady();
    /* Draw at physical pixels instead of letting Windows stretch the window
       (blurring the nearest-neighbor picture) on scaled displays. */
    SDL_SetHint(SDL_HINT_WINDOWS_DPI_AWARENESS, "permonitorv2");
#endif
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER | (mute ? 0 : SDL_INIT_AUDIO))) {
        fatal("SDL: %s", SDL_GetError());
        free(g);
        return 1;
    }
    char *pref = SDL_GetPrefPath("dexedrne", "TXRA");
    if (!pref) {
        fatal("Cannot create user folder: %s", SDL_GetError());
        return 1;
    }
#ifdef _WIN32
    if (no_console) {
        char log[4096];
        snprintf(log, sizeof(log), "%slast-run.log", pref);
        FILE *probe = fopen(log, "w");
        if (probe) {
            fclose(probe);
            freopen(log, "w", stderr);
        }
    }
#endif
    char default_save[4096], default_bindings[4096], default_stats[4096], default_unknown[4096];
    snprintf(default_save, sizeof(default_save), "%stxra.sav", pref);
    snprintf(default_bindings, sizeof(default_bindings), "%sbindings.ini", pref);
    snprintf(default_stats, sizeof(default_stats), "%slast-run.json", pref);
    snprintf(default_unknown, sizeof(default_unknown), "%sunknown-targets.log", pref);
    if (!save) {
        save = default_save;
        /* Preserve older working-directory saves without overwriting a user profile. */
        FILE *old = fopen("txra.sav", "rb"), *existing = fopen(save, "rb");
        if (old && !existing && !reset_save) {
#ifdef _WIN32
            /* The Windows C runtime has no "x" mode; create exclusively by hand. */
            int fd = _open(save, _O_WRONLY | _O_CREAT | _O_EXCL | _O_BINARY, _S_IREAD | _S_IWRITE);
            FILE *out = fd < 0 ? NULL : _fdopen(fd, "wb");
#else
            FILE *out = fopen(save, "wbx");
#endif
            bool ok = out != NULL;
            if (out) {
                int c;
                while ((c = fgetc(old)) != EOF)
                    if (fputc(c, out) == EOF) {
                        ok = false;
                        break;
                    }
                if (ferror(old))
                    ok = false;
                if (fclose(out))
                    ok = false;
            }
            if (!ok) {
                if (out)
                    remove(save);
                fprintf(stderr, "Legacy save import failed; original retained\n");
                return 1;
            }
            fprintf(stderr, "Imported legacy save; original retained\n");
        }
        if (old)
            fclose(old);
        if (existing)
            fclose(existing);
    }
    if (!binding_path)
        binding_path = default_bindings;
    if (!stats)
        stats = default_stats;
    if (!unknown)
        unknown = default_unknown;
    fprintf(stderr, "Save: %s\nBindings: %s\n", save, binding_path);
    if (reset_save && !desktop_backup(save)) {
        perror("Save backup");
        return 1;
    }
    boot(g, save, fopen(unknown, "wb"), trace);
    if (coverage && !coverage_start(g)) {
        fprintf(stderr, "Cannot allocate coverage logger\n");
        return 1;
    }
    Bindings bindings;
    bindings_default(&bindings);
    FILE *bf = fopen(binding_path, "r");
    if (bf) {
        fclose(bf);
        if (!bindings_load(&bindings, binding_path)) {
            fatal("Bindings file rejected: %s", binding_path);
            return 2;
        }
    } else if (!bindings_write(&bindings, binding_path)) {
        fatal("Bindings: %s", strerror(errno));
        return 1;
    }
    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "0");
    SDL_Window *window =
        SDL_CreateWindow("TXRA", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 960, 640,
                         headless ? SDL_WINDOW_HIDDEN
                                  : (SDL_WINDOW_RESIZABLE | SDL_WINDOW_ALLOW_HIGHDPI |
                                     (desktop.fullscreen ? SDL_WINDOW_FULLSCREEN_DESKTOP : 0)));
    if (window)
        SDL_SetWindowMinimumSize(window, 240, 160);
    SDL_Renderer *renderer =
        window && !headless
            ? SDL_CreateRenderer(window, -1,
                                 SDL_RENDERER_ACCELERATED |
                                     ((vsync && !benchmark) ? SDL_RENDERER_PRESENTVSYNC : 0))
            : NULL;
    if (!renderer && window)
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE);
    SDL_Texture *texture = renderer ? SDL_CreateTexture(renderer, SDL_PIXELFORMAT_ARGB8888,
                                                        SDL_TEXTUREACCESS_STREAMING, 240, 160)
                                    : NULL;
    if (!texture) {
        fatal("SDL video: %s", SDL_GetError());
        return 1;
    }
    SDL_RendererInfo ri;
    SDL_GetRendererInfo(renderer, &ri);
    fprintf(stderr, "Renderer: %s, vsync %s\n", ri.name,
            ri.flags & SDL_RENDERER_PRESENTVSYNC ? "on" : "off");
    uint32_t display[240 * 160];
    unsigned ui_frames[256], ui_count = 0, ui_index = 0;
    char ui_actions[256][32];
    if (ui_script) {
        FILE *uf = fopen(ui_script, "r");
        if (!uf) {
            perror(ui_script);
            return 1;
        }
        while (ui_count < 256 &&
               fscanf(uf, "%u %31s", &ui_frames[ui_count], ui_actions[ui_count]) == 2)
            ui_count++;
        fclose(uf);
    }
    enum { INPUT_CAPACITY = 8192 };
    unsigned input_start[INPUT_CAPACITY], input_end[INPUT_CAPACITY],
        input_keys[INPUT_CAPACITY], input_count = 0;
    if (input) {
        FILE *script = fopen(input, "r");
        if (!script) {
            perror(input);
            return 1;
        }
        for (;;) {
            unsigned first, end, mask;
            int fields = fscanf(script, "%u %u %x", &first, &end, &mask);
            if (fields == EOF)
                break;
            if (fields != 3 || first >= end || mask > 1023 || input_count == INPUT_CAPACITY) {
                fprintf(stderr, "Invalid input script or more than %u events\n", INPUT_CAPACITY);
                fclose(script);
                return 2;
            }
            input_start[input_count] = first;
            input_end[input_count] = end;
            input_keys[input_count++] = mask;
        }
        fclose(script);
    }
    SDL_GameController *pad = NULL;
    for (int i = 0; i < SDL_NumJoysticks(); i++)
        if (SDL_IsGameController(i)) {
            pad = SDL_GameControllerOpen(i);
            break;
        }
    Audio audio = {0};
    desktop.muted = mute;
    if (!mute && !audio_open(&audio))
        desktop.muted = true;
    FILE *video = raw ? fopen(raw, "wb") : NULL;
    FILE *sound = pcm ? fopen(pcm, "wb") : NULL;
    /* Binary mode keeps diagnostic files byte-identical on every platform. */
    FILE *hashes = hashpath ? fopen(hashpath, "wb") : NULL;
    FILE *timings = frame_times ? fopen(frame_times, "wb") : NULL;
    if (timings)
        fprintf(timings, "frame,interval_ms,work_ms,host_guest_ms,present_ms,capture_ms,audio_ms,pace_ms,audio_underruns,audio_underruns_delta,audio_backpressure_ms\n");
    if ((raw && !video) || (pcm && !sound) || (hashpath && !hashes) || (frame_times && !timings)) {
        fprintf(stderr, "Cannot open capture output\n");
        return 1;
    }
    unsigned shown = 0;
    uint64_t start = SDL_GetPerformanceCounter(), freq = SDL_GetPerformanceFrequency();
    uint64_t deadline = start, previous_frame = start;
    uint64_t deadline_remainder = 0;
    bool chord_down = false, release_input = false;
    double previous_speed = 1;
    bool previous_pause = false, previous_muted = desktop.muted;
#ifdef _WIN32
    double cpu_start = cpu_time(); /* clock() measures wall time on Windows */
#else
    clock_t cpu_start = clock();
#endif
    bool refresh_host = true;
    bool quit = false;
    while (!quit && !g->stopped && (!frames || g->frame < frames)) {
        if (refresh_host || desktop.paused) {
            SDL_Event event;
            int command = 0;
            /* Commands use the same path as keyboard/controller events. */
            if (ui_index < ui_count && g->frame >= ui_frames[ui_index]) {
                const char *action = ui_actions[ui_index++];
                if (!strcmp(action, "pause"))
                    command = 1;
                else if (!strcmp(action, "resume")) {
                    desktop.paused = false;
                    desktop.confirm_reset = false;
                } else if (!strcmp(action, "fullscreen"))
                    command = 2;
                else if (!strcmp(action, "screenshot"))
                    command = 3;
                else if (!strcmp(action, "down"))
                    command = 5;
                else if (!strcmp(action, "up"))
                    command = 4;
                else if (!strcmp(action, "accept"))
                    command = 6;
                else if (!strcmp(action, "cancel"))
                    command = 7;
                else if (!strcmp(action, "quit"))
                    quit = true;
            }
            while (SDL_PollEvent(&event)) {
                controller_event(&pad, &event);
                if (event.type == SDL_QUIT)
                    quit = true;
                if (event.type == SDL_WINDOWEVENT &&
                    event.window.event == SDL_WINDOWEVENT_FOCUS_LOST &&
                    event.window.windowID == SDL_GetWindowID(window) && !headless && focus_pause)
                    desktop.paused = true;
                if (event.type == SDL_KEYDOWN && !event.key.repeat) {
                    SDL_Keycode k = event.key.keysym.sym;
                    if (k == SDLK_ESCAPE)
                        command = 1;
                    else if (k == SDLK_F11 ||
                             (k == SDLK_RETURN && (event.key.keysym.mod & KMOD_ALT)))
                        command = 2;
                    else if (k == SDLK_F8)
                        command = 3;
                    else if (desktop.paused) {
                        if (k == SDLK_UP)
                            command = 4;
                        if (k == SDLK_DOWN)
                            command = 5;
                        if (k == SDLK_RETURN || k == SDLK_x)
                            command = 6;
                        if (k == SDLK_z)
                            command = 7;
                    }
                }
                if (event.type == SDL_CONTROLLERBUTTONDOWN) {
                    int b = event.cbutton.button;
                    if (b == SDL_CONTROLLER_BUTTON_GUIDE)
                        command = 1;
                    else if (desktop.paused) {
                        if (b == SDL_CONTROLLER_BUTTON_DPAD_UP)
                            command = 4;
                        if (b == SDL_CONTROLLER_BUTTON_DPAD_DOWN)
                            command = 5;
                        if (b == SDL_CONTROLLER_BUTTON_A || b == SDL_CONTROLLER_BUTTON_START)
                            command = 6;
                        if (b == SDL_CONTROLLER_BUTTON_B)
                            command = 7;
                    }
                }
            }
            bool chord = pad && SDL_GameControllerGetButton(pad, SDL_CONTROLLER_BUTTON_START) &&
                         SDL_GameControllerGetButton(pad, SDL_CONTROLLER_BUTTON_BACK);
            if (chord && !chord_down)
                command = 1;
            chord_down = chord;
            if (command == 1) {
                if (desktop.confirm_reset)
                    desktop.confirm_reset = false;
                else
                    desktop.paused = !desktop.paused;
            }
            if (command == 2) {
                bool next = !desktop.fullscreen;
                if (SDL_SetWindowFullscreen(window, next ? SDL_WINDOW_FULLSCREEN_DESKTOP : 0) == 0)
                    desktop.fullscreen = next;
                else
                    desktop_notice(&desktop, "FULLSCREEN FAILED");
            }
            if (desktop.paused && !desktop.confirm_reset) {
                if (command == 4)
                    desktop.selected = (desktop.selected + 6) % 7;
                if (command == 5)
                    desktop.selected = (desktop.selected + 1) % 7;
            }
            if (command == 7) {
                if (desktop.confirm_reset)
                    desktop.confirm_reset = false;
                else
                    desktop.paused = false;
            }
            if (command == 6 && desktop.paused) {
                if (desktop.confirm_reset)
                    eeprom_flush(g);
                if (desktop.confirm_reset) {
                    if (coverage || input || raw || hashpath || pcm) {
                        desktop_notice(&desktop, "RESET DISABLED DURING CAPTURE");
                        desktop.confirm_reset = false;
                    } else if (g->save_dirty || !desktop_backup(save)) {
                        desktop_notice(&desktop, "SAVE BACKUP FAILED");
                        desktop.confirm_reset = false;
                    } else {
                        FILE *log = g->unknown;
                        boot(g, save, log, trace);
                        shown = 0;
                        desktop.confirm_reset = false;
                        desktop.paused = false;
                        deadline = SDL_GetPerformanceCounter();
                        desktop_notice(&desktop, "SAVE RESET - BACKUP RETAINED");
                    }
                } else
                    switch (desktop.selected) {
                    case 0:
                        desktop.paused = false;
                        break;
                    case 1: {
                        bool next = !desktop.fullscreen;
                        if (SDL_SetWindowFullscreen(window,
                                                    next ? SDL_WINDOW_FULLSCREEN_DESKTOP : 0) == 0)
                            desktop.fullscreen = next;
                        else
                            desktop_notice(&desktop, "FULLSCREEN FAILED");
                        break;
                    }
                    case 2:
                        desktop.integer = !desktop.integer;
                        break;
                    case 3:
                        if (desktop.muted && !audio.device) {
                            if (!SDL_WasInit(SDL_INIT_AUDIO))
                                SDL_InitSubSystem(SDL_INIT_AUDIO);
                            if (!audio_open(&audio)) {
                                desktop_notice(&desktop, "AUDIO DEVICE UNAVAILABLE");
                                break;
                            }
                        }
                        desktop.muted = !desktop.muted;
                        break;
                    case 4:
                        command = 3;
                        break;
                    case 5:
                        desktop.confirm_reset = true;
                        break;
                    case 6:
                        quit = true;
                        break;
                    }
            }
            const uint8_t *k = SDL_GetKeyboardState(NULL);
            desktop.speed = k[SDL_SCANCODE_TAB] ? 3 : k[SDL_SCANCODE_GRAVE] ? 0.5 : 1;
            if (desktop.paused != previous_pause || desktop.speed != previous_speed ||
                desktop.muted != previous_muted) {
                if (desktop.paused != previous_pause)
                    fprintf(stderr, "Host menu %s at frame %u\n",
                            desktop.paused ? "paused" : "resumed", g->frame);
                audio_clear(&audio);
                deadline = SDL_GetPerformanceCounter();
                deadline_remainder = 0;
                release_input = true;
                previous_pause = desktop.paused;
                previous_speed = desktop.speed;
                previous_muted = desktop.muted;
            }
            if (command == 3 || desktop.paused)
                desktop_pixels(&desktop, g->pixels, display);
            if (command == 3) {
                char path[4096];
                snprintf(path, sizeof(path), "%sshot-%lld-%u.bmp", pref, (long long)time(NULL),
                         SDL_GetTicks());
                bool ok = desktop_screenshot(display, path);
                desktop_notice(&desktop, ok ? "SCREENSHOT SAVED" : "SCREENSHOT FAILED");
                if (ok)
                    fprintf(stderr, "Screenshot: %s\n", path);
            }
            if (quit)
                break;
            if (desktop.paused) {
                desktop_present(renderer, texture, window, display, desktop.integer);
                SDL_Delay(8);
                continue;
            }
            unsigned keys = bindings_keys(&bindings, pad, k);
            /* Do not leak overlay accept/cancel/fullscreen chords into the guest. */
            if (!keys)
                release_input = false;
            if (command || release_input || (SDL_GetModState() & KMOD_ALT))
                keys = 0;
            for (unsigned i = 0; i < input_count; i++)
                if (g->frame >= input_start[i] && g->frame < input_end[i])
                    keys |= input_keys[i];
            if (auto_start && g->frame >= auto_start && g->frame < auto_start + 10)
                keys |= 8;
            unsigned key = ~keys & 1023;
            g->io[0x130] = key;
            g->io[0x131] = key >> 8;
            refresh_host = false;
        }
        g->trace = trace && (!frames || frames <= 12 || g->frame + 1 >= frames);
        g->quota = 96;
        irq_check(g);
        while (g->quota > 0 && !g->stopped) {
            if (g->halted) {
                hardware_advance(g, 3);
                g->quota--;
            } else if (interpreter) {
                if (g->in_irq && g->r[15] == 0x138)
                    dispatch(g);
                else
                    fallback(g);
            } else
                dispatch(g);
            irq_check(g);
        }
        if (g->frame != shown) {
            shown = g->frame;
            refresh_host = true;
            if (shown % 60 == 0)
                eeprom_flush(g);
            uint64_t present_start = timings ? SDL_GetPerformanceCounter() : 0;
            desktop_pixels(&desktop, g->pixels, display);
            desktop_present(renderer, texture, window, display, desktop.integer);
            uint64_t present_end = timings ? SDL_GetPerformanceCounter() : 0;
            if (video && shown % 2 == 0 && shown >= video_start && shown < video_end)
                fwrite(g->pixels, 4, 240 * 160, video);
            if (sound)
                fwrite(g->audio, 2, g->audio_len, sound);
            if (hashes) {
                u32 hash = 2166136261u;
                for (unsigned i = 0; i < 240 * 160; i++)
                    hash = (hash ^ g->pixels[i]) * 16777619u;
                fprintf(hashes, "%u %08x\n", shown, hash);
            }
            if (snapshots && shown % 300 == 0) {
                char name[1024];
                snprintf(name, sizeof(name), "%s/%06u.ppm", snapshots, shown);
                capture(g, name);
            }
            uint64_t audio_start = timings ? SDL_GetPerformanceCounter() : 0;
            unsigned underruns_before = timings ? audio.underruns : 0;
            uint64_t backpressure_before = timings ? audio.backpressure_ticks : 0;
            if (!desktop.muted && !benchmark && desktop.speed == 1 && g->audio_len) {
                if (!audio_queue(&audio, g->audio, g->audio_len * 2)) {
                    fprintf(stderr, "Audio queue failed: %s\n", SDL_GetError());
                    desktop.muted = true;
                    audio_clear(&audio);
                }
            }
            g->audio_len = 0;
            uint64_t work_end = SDL_GetPerformanceCounter();
            if (!benchmark) {
                unsigned numerator = desktop.speed > 1 ? 3 : 1,
                         denominator = desktop.speed < 1 ? 2 : 1;
                uint64_t divisor = 16777216ULL * numerator;
                uint64_t ticks = freq * 280896ULL * denominator + deadline_remainder;
                deadline += ticks / divisor;
                deadline_remainder = ticks % divisor;
                uint64_t now = SDL_GetPerformanceCounter();
                /* Rebase after a stall instead of racing to catch up. */
                if (now > deadline + freq / 10)
                    deadline = now;
                while ((now = SDL_GetPerformanceCounter()) < deadline) {
                    uint64_t ms = (deadline - now) * 1000 / freq;
                    if (ms > 1)
                        SDL_Delay(ms - 1);
                    else
                        SDL_Delay(0);
                }
            }
            uint64_t frame_end = SDL_GetPerformanceCounter();
            if (timings)
                fprintf(timings, "%u,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%u,%u,%.6f\n", shown,
                        (frame_end - previous_frame) * 1000.0 / freq,
                        (work_end - previous_frame) * 1000.0 / freq,
                        (present_start - previous_frame) * 1000.0 / freq,
                        (present_end - present_start) * 1000.0 / freq,
                        (audio_start - present_end) * 1000.0 / freq,
                        (work_end - audio_start) * 1000.0 / freq,
                        (frame_end - work_end) * 1000.0 / freq,
                        audio.underruns, audio.underruns - underruns_before,
                        (audio.backpressure_ticks - backpressure_before) * 1000.0 / freq);
            previous_frame = frame_end;
        }
    }
    fprintf(stderr, "timers=%04x/%04x %04x/%04x IE=%04x IF=%04x irq=%u lr=%08x\n",
            g->timer_reload[0], rd16(g, 0x04000102), g->timer_reload[1], rd16(g, 0x04000106),
            rd16(g, 0x04000200), rd16(g, 0x04000202), g->in_irq, g->r[14]);
    fprintf(stderr, "interrupted=%08x return=%08x hook=%08x\n", g->irq_regs[15], g->irq_regs[14],
            rd32(g, 0x03007ffc));
    if (shot)
        capture(g, shot);
    if (video)
        fclose(video);
    if (sound)
        fclose(sound);
    if (hashes)
        fclose(hashes);
    if (timings)
        fclose(timings);
    eeprom_flush(g);
    fprintf(stderr,
            "frames=%u pc=%08x cpsr=%08x instructions=%" PRIu64 " compiled=%" PRIu64
            " fallback=%" PRIu64 " unknown=%u unsupported=%u dispcnt=%04x\n",
            g->frame, g->r[15], g->cpsr, g->instructions, g->compiled_steps, g->fallback_steps,
            g->unknown_count, g->unsupported, g->io[0] | g->io[1] << 8);
    u32 state = 2166136261u;
    const uint8_t *regions[] = {g->ewram, g->iwram, g->io,           g->pal,
                                g->vram,  g->oam,   (uint8_t *)g->r, (uint8_t *)&g->cpsr};
    const size_t lengths[] = {sizeof(g->ewram), sizeof(g->iwram), sizeof(g->io), sizeof(g->pal),
                              sizeof(g->vram),  sizeof(g->oam),   sizeof(g->r),  sizeof(g->cpsr)};
    for (unsigned j = 0; j < 8; j++)
        for (size_t i = 0; i < lengths[j]; i++)
            state = (state ^ regions[j][i]) * 16777619u;
    double elapsed = (double)(SDL_GetPerformanceCounter() - start) / freq;
#ifdef _WIN32
    double cpu_seconds = cpu_time() - cpu_start;
#else
    double cpu_seconds = (double)(clock() - cpu_start) / CLOCKS_PER_SEC;
#endif
    fprintf(stderr,
            "Performance: %.3f fps, %.3f CPU seconds, %.1f%% of one CPU; audio underruns=%u "
            "max_queue=%.1f ms\n",
            elapsed ? g->frame / elapsed : 0, cpu_seconds,
            elapsed ? cpu_seconds * 100 / elapsed : 0, audio.underruns,
            audio.format.freq ? audio.max_queue_bytes * 1000.0 / (audio.format.freq * 4) : 0);
    f = fopen(stats, "wb");
    if (f) {
        fprintf(f,
                "{\"frames\":%u,\"pc\":\"%08x\",\"instructions\":%" PRIu64
                ",\"compiled_steps\":%" PRIu64 ",\"fallback_steps\":%" PRIu64
                ",\"unknown_targets\":%u,\"unsupported\":%u,\"functions_compiled\":%u,\"state_"
                "hash\":\"%08x\",\"cycles\":%" PRIu64
                ",\"audio_samples\":%u,\"audio_hash\":\"%016" PRIx64
                "\",\"save_writes\":%u,\"elapsed_seconds\":%.6f,\"cpu_seconds\":%.6f,\"audio_"
                "underruns\":%u,\"audio_max_queue_ms\":%.3f,\"audio_backpressure_seconds\":%.6f,\"stopped\":%s}\n",
                g->frame, g->r[15], g->instructions, g->compiled_steps, g->fallback_steps,
                g->unknown_count, g->unsupported, recompiled_function_count, state, g->cycles,
                g->audio_samples, g->audio_hash, g->save_writes, elapsed, cpu_seconds,
                audio.underruns,
                audio.format.freq ? audio.max_queue_bytes * 1000.0 / (audio.format.freq * 4) : 0,
                audio.backpressure_ticks / (double)freq,
                g->stopped ? "true" : "false");
        fclose(f);
    }
    if (g->unknown)
        fclose(g->unknown);
    if (pad)
        SDL_GameControllerClose(pad);
    audio_close(&audio);
    SDL_free(pref);
    SDL_DestroyTexture(texture);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    int result = (g->unsupported || g->save_dirty) ? 1 : 0;
    if (coverage && !coverage_finish(g, coverage)) {
        fprintf(stderr, "Coverage output incomplete\n");
        result = 1;
    }
    free(g);
    return result;
}
