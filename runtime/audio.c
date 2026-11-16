#include "audio.h"
#include <stdio.h>
bool audio_open(Audio *a) {
    SDL_AudioSpec want = {0};
    want.freq = 48000;
    want.format = AUDIO_S16SYS;
    want.channels = 2;
    want.samples = 480;
    a->device = SDL_OpenAudioDevice(NULL, 0, &want, &a->format, SDL_AUDIO_ALLOW_FREQUENCY_CHANGE);
    if (!a->device) {
        fprintf(stderr, "SDL audio: %s\n", SDL_GetError());
        return false;
    }
    a->stream = SDL_NewAudioStream(AUDIO_S16SYS, 2, 32768, a->format.format, a->format.channels,
                                   a->format.freq);
    if (!a->stream) {
        fprintf(stderr, "Audio converter: %s\n", SDL_GetError());
        audio_close(a);
        return false;
    }
    fprintf(stderr, "Audio: 32768 Hz stereo -> %d Hz stereo, %u device frames\n", a->format.freq,
            a->format.samples);
    return true;
}
void audio_clear(Audio *a) {
    if (!a->device)
        return;
    SDL_PauseAudioDevice(a->device, 1);
    SDL_ClearQueuedAudio(a->device);
    SDL_AudioStreamClear(a->stream);
    a->started = false;
}
bool audio_queue(Audio *a, const void *data, int bytes) {
    if (!a->device)
        return true;
    Uint32 queued = SDL_GetQueuedAudioSize(a->device);
    if (a->started && !queued) {
        a->underruns++;
        SDL_PauseAudioDevice(a->device, 1);
        a->started = false;
    }
    /* About 40-70 ms with normal one-frame batches. Backpressure prevents unlimited latency and
     * clock drift. */
    if (a->started && queued > (Uint32)a->format.freq * 4 * 50 / 1000) {
        Uint64 start = SDL_GetPerformanceCounter();
        do {
            SDL_Delay(1);
            queued = SDL_GetQueuedAudioSize(a->device);
#ifdef TXRA_IOS
            /* An interrupted iOS audio session stops consuming: never hold the game on it. */
            if (SDL_GetPerformanceCounter() - start > SDL_GetPerformanceFrequency() / 4) {
                a->backpressure_ticks += SDL_GetPerformanceCounter() - start;
                audio_clear(a);
                return true;
            }
#endif
        } while (a->started && queued > (Uint32)a->format.freq * 4 * 50 / 1000);
        a->backpressure_ticks += SDL_GetPerformanceCounter() - start;
    }
    if (SDL_AudioStreamPut(a->stream, data, bytes) < 0)
        return false;
    Uint8 buffer[8192];
    int available;
    while ((available = SDL_AudioStreamAvailable(a->stream)) > 0) {
        int n = SDL_AudioStreamGet(a->stream, buffer, SDL_min(available, (int)sizeof(buffer)));
        if (n < 0 || SDL_QueueAudio(a->device, buffer, n) < 0)
            return false;
    }
    queued = SDL_GetQueuedAudioSize(a->device);
    if (queued > a->max_queue_bytes)
        a->max_queue_bytes = queued;
    if (!a->started && queued >= (Uint32)a->format.freq * 4 * 40 / 1000) {
        SDL_PauseAudioDevice(a->device, 0);
        a->started = true;
    }
    return available >= 0;
}
void audio_close(Audio *a) {
    if (a->device)
        SDL_CloseAudioDevice(a->device);
    if (a->stream)
        SDL_FreeAudioStream(a->stream);
    a->device = 0;
    a->stream = NULL;
}
