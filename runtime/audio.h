#ifndef TXRA_AUDIO_H
#define TXRA_AUDIO_H
#include <SDL.h>
#include <stdbool.h>
typedef struct {
    SDL_AudioDeviceID device;
    SDL_AudioSpec format;
    SDL_AudioStream *stream;
    bool started;
    unsigned underruns, max_queue_bytes;
    Uint64 backpressure_ticks;
} Audio;
bool audio_open(Audio *);
void audio_clear(Audio *);
bool audio_queue(Audio *, const void *, int);
void audio_close(Audio *);
#endif
