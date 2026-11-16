#ifndef TXRA_ROMSCAN_H
#define TXRA_ROMSCAN_H
/* Finds the player's own cartridge dump in a folder (the iPhone app's Documents folder).
   Plain C (POSIX directory calls only), tested on Linux by tests/touch_test.c. */
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum { ROM_SCAN_NONE, ROM_SCAN_WRONG, ROM_SCAN_FOUND };
typedef struct {
    int result;      /* ROM_SCAN_NONE: no .gba file; WRONG: .gba files, none supported; FOUND */
    int candidates;  /* .gba files looked at */
    char name[256];  /* the file used, or the first one refused */
} RomScan;

void rom_sha1(const uint8_t *data, size_t length, uint8_t digest[20]);
void rom_sha1_hex(const uint8_t *data, size_t length, char hex[41]);
/* Looks at every *.gba (any case) in `folder`, then in folder/Inbox (where iOS puts files
   shared with the app). baserom.gba is tried first, then the others in name order. The first
   file of exactly `size` bytes whose SHA-1 is `sha1_hex` is read into `rom`. */
RomScan rom_scan(const char *folder, const char *sha1_hex, uint8_t *rom, size_t size);
/* Copies a .gba file into `folder` under its own name (name-2.gba ... if taken). Files already
   in the folder are left alone. Writes the resulting path to `out`. */
bool rom_import(const char *source, const char *folder, char *out, size_t out_size);
#endif
