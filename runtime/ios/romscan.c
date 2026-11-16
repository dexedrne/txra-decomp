/* strdup and strcasecmp are POSIX; glibc hides them under -std=c11 without this. */
#define _DEFAULT_SOURCE
#include "romscan.h"
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>

static uint32_t rol(uint32_t v, int n) {
    return (v << n) | (v >> (32 - n));
}
static void sha1_block(uint32_t h[5], const uint8_t *p) {
    uint32_t w[80];
    for (int i = 0; i < 16; i++)
        w[i] = (uint32_t)p[i * 4] << 24 | (uint32_t)p[i * 4 + 1] << 16 |
               (uint32_t)p[i * 4 + 2] << 8 | p[i * 4 + 3];
    for (int i = 16; i < 80; i++)
        w[i] = rol(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1);
    uint32_t a = h[0], b = h[1], c = h[2], d = h[3], e = h[4];
    for (int i = 0; i < 80; i++) {
        uint32_t f, k;
        if (i < 20)
            f = (b & c) | (~b & d), k = 0x5a827999;
        else if (i < 40)
            f = b ^ c ^ d, k = 0x6ed9eba1;
        else if (i < 60)
            f = (b & c) | (b & d) | (c & d), k = 0x8f1bbcdc;
        else
            f = b ^ c ^ d, k = 0xca62c1d6;
        uint32_t t = rol(a, 5) + f + e + k + w[i];
        e = d;
        d = c;
        c = rol(b, 30);
        b = a;
        a = t;
    }
    h[0] += a;
    h[1] += b;
    h[2] += c;
    h[3] += d;
    h[4] += e;
}

void rom_sha1(const uint8_t *data, size_t length, uint8_t digest[20]) {
    uint32_t h[5] = {0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0};
    size_t full = length / 64 * 64;
    for (size_t i = 0; i < full; i += 64)
        sha1_block(h, data + i);
    uint8_t tail[128] = {0};
    size_t rest = length - full;
    memcpy(tail, data + full, rest);
    tail[rest] = 0x80;
    size_t blocks = rest + 9 > 64 ? 2 : 1;
    uint64_t bits = (uint64_t)length * 8;
    for (int i = 0; i < 8; i++)
        tail[blocks * 64 - 1 - i] = (uint8_t)(bits >> (8 * i));
    for (size_t i = 0; i < blocks; i++)
        sha1_block(h, tail + i * 64);
    for (int i = 0; i < 20; i++)
        digest[i] = (uint8_t)(h[i / 4] >> (24 - 8 * (i % 4)));
}

void rom_sha1_hex(const uint8_t *data, size_t length, char hex[41]) {
    uint8_t digest[20];
    rom_sha1(data, length, digest);
    for (int i = 0; i < 20; i++)
        snprintf(hex + 2 * i, 3, "%02x", digest[i]);
}

static bool is_gba(const char *name) {
    size_t n = strlen(name);
    return name[0] != '.' && n > 4 && !strcasecmp(name + n - 4, ".gba");
}

static int by_name(const void *a, const void *b) {
    const char *x = *(char *const *)a, *y = *(char *const *)b;
    /* baserom.gba sorts first; then plain byte order, so the choice is reproducible. */
    bool bx = !strcasecmp(x, "baserom.gba"), by = !strcasecmp(y, "baserom.gba");
    if (bx != by)
        return bx ? -1 : 1;
    return strcmp(x, y);
}

/* Returns true when a file matched; updates the scan record either way. */
static bool scan_folder(const char *folder, const char *sha1_hex, uint8_t *rom, size_t size,
                        RomScan *scan) {
    DIR *dir = opendir(folder);
    if (!dir)
        return false;
    char *names[256];
    int count = 0;
    struct dirent *entry;
    while ((entry = readdir(dir)) && count < 256)
        if (is_gba(entry->d_name) && (names[count] = strdup(entry->d_name)))
            count++;
    closedir(dir);
    qsort(names, (size_t)count, sizeof(names[0]), by_name);
    bool found = false;
    for (int i = 0; i < count && !found; i++) {
        char path[4096];
        snprintf(path, sizeof(path), "%s/%s", folder, names[i]);
        struct stat st;
        if (stat(path, &st) || !S_ISREG(st.st_mode))
            continue;
        scan->candidates++;
        bool match = false;
        if ((size_t)st.st_size == size) {
            FILE *f = fopen(path, "rb");
            if (f) {
                size_t n = fread(rom, 1, size, f);
                fclose(f);
                char hex[41];
                if (n == size) {
                    rom_sha1_hex(rom, size, hex);
                    match = !strcasecmp(hex, sha1_hex);
                }
            }
        }
        if (match || scan->result != ROM_SCAN_WRONG) {
            snprintf(scan->name, sizeof(scan->name), "%s", names[i]);
            scan->result = match ? ROM_SCAN_FOUND : ROM_SCAN_WRONG;
        }
        found = match;
    }
    for (int i = 0; i < count; i++)
        free(names[i]);
    return found;
}

RomScan rom_scan(const char *folder, const char *sha1_hex, uint8_t *rom, size_t size) {
    RomScan scan = {ROM_SCAN_NONE, 0, ""};
    char inbox[4096];
    snprintf(inbox, sizeof(inbox), "%s/Inbox", folder);
    if (!scan_folder(folder, sha1_hex, rom, size, &scan))
        scan_folder(inbox, sha1_hex, rom, size, &scan);
    if (scan.result != ROM_SCAN_FOUND)
        memset(rom, 0, size);
    return scan;
}

bool rom_import(const char *source, const char *folder, char *out, size_t out_size) {
    const char *base = strrchr(source, '/');
    base = base ? base + 1 : source;
    if (!is_gba(base) || strlen(base) > 200)
        return false;
    char path[4096];
    snprintf(path, sizeof(path), "%s/%s", folder, base);
    if (!strcmp(path, source)) {
        snprintf(out, out_size, "%s", path);
        return true;
    }
    FILE *in = fopen(source, "rb");
    if (!in)
        return false;
    FILE *dst = NULL;
    for (int n = 1; n < 100 && !dst; n++) {
        if (n > 1)
            snprintf(path, sizeof(path), "%s/%.*s-%d.gba", folder, (int)(strlen(base) - 4), base, n);
        struct stat st;
        if (stat(path, &st) == 0)
            continue;
        dst = fopen(path, "wb");
    }
    bool ok = dst != NULL;
    if (dst) {
        char buffer[65536];
        size_t n, total = 0;
        while ((n = fread(buffer, 1, sizeof(buffer), in)) > 0 && ok) {
            total += n;
            ok = total <= 64u << 20 && fwrite(buffer, 1, n, dst) == n;
        }
        if (ferror(in))
            ok = false;
        if (fclose(dst))
            ok = false;
        if (!ok)
            remove(path);
    }
    fclose(in);
    if (ok)
        snprintf(out, out_size, "%s", path);
    return ok;
}
