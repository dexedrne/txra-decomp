/* iPhone platform glue that needs UIKit: the program entry, the window scene, safe-area insets
   and files shared to the app ("Open in TXRA"). Compiled only into the iOS app. */
#import <UIKit/UIKit.h>
#include <stdlib.h>
#include "ios.h"
#include "romscan.h"
#include <SDL.h>
#include <SDL_syswm.h>

/* Apps built with the iOS 27 SDK must use the scene life cycle (Info.plist
   UIApplicationSceneManifest), which SDL 2.30 predates: SDL creates a plain UIWindow, and this
   file moves it into the app's window scene. SDL's lifecycle events still work because UIKit
   keeps posting the UIApplication notifications SDL observes. */
static UIWindowScene *app_scene;
static __weak UIWindow *sdl_window;

static void attach_window(void) {
    UIWindow *window = sdl_window;
    if (!app_scene || !window || window.windowScene == app_scene)
        return;
    window.windowScene = app_scene;
    window.frame = app_scene.coordinateSpace.bounds;
    [window makeKeyAndVisible];
}

static UIWindow *uikit_window(SDL_Window *window) {
    SDL_SysWMinfo info;
    SDL_VERSION(&info.version);
    if (!window || !SDL_GetWindowWMInfo(window, &info) || info.subsystem != SDL_SYSWM_UIKIT)
        return nil;
    return info.info.uikit.window;
}

void ios_attach_window(SDL_Window *window) {
    sdl_window = uikit_window(window);
    /* The scene normally connects before SDL_main runs; if not, let UIKit finish launching. */
    for (int i = 0; i < 300 && !app_scene; i++)
        CFRunLoopRunInMode(kCFRunLoopDefaultMode, 0.01, true);
    attach_window();
}

float ios_display_scale(SDL_Window *window) {
    UIWindow *w = uikit_window(window);
    UIScreen *screen = w.windowScene ? w.windowScene.screen : nil;
    /* SDL sizes its Metal drawable with the screen's native scale. */
    return screen ? (float)screen.nativeScale : 0;
}

void ios_safe_insets(SDL_Window *window, float *left, float *top, float *right, float *bottom) {
    *left = *top = *right = *bottom = 0;
    UIWindow *w = uikit_window(window);
    if (!w)
        return;
    UIEdgeInsets insets = w.safeAreaInsets;
    *left = (float)insets.left;
    *top = (float)insets.top;
    *right = (float)insets.right;
    *bottom = (float)insets.bottom;
}

/* A shared file may live outside the sandbox (opened in place from Files or iCloud Drive):
   read it under its security scope and keep a copy in Documents. */
static void import_shared_file(NSURL *url) {
    if (!url.isFileURL)
        return;
    BOOL scoped = [url startAccessingSecurityScopedResource];
    char copied[4096];
    bool ok = rom_import(url.path.fileSystemRepresentation, ios_documents(), copied, sizeof(copied));
    if (scoped)
        [url stopAccessingSecurityScopedResource];
    if (!ok)
        return;
    /* Some shared files arrive as copies in Documents/Inbox; drop the extra copy. */
    NSString *inbox = [@(ios_documents()) stringByAppendingPathComponent:@"Inbox"];
    if ([url.path.stringByStandardizingPath hasPrefix:inbox.stringByStandardizingPath])
        [[NSFileManager defaultManager] removeItemAtURL:url error:nil];
    SDL_Event event;
    SDL_zero(event);
    event.type = SDL_DROPFILE;
    event.drop.file = SDL_strdup(copied);
    if (SDL_PushEvent(&event) != 1) /* before SDL is up, the first ROM scan finds the copy */
        SDL_free(event.drop.file);
}

@interface TXRASceneDelegate : UIResponder <UIWindowSceneDelegate>
@end

@implementation TXRASceneDelegate
- (void)scene:(UIScene *)scene
    willConnectToSession:(UISceneSession *)session
                 options:(UISceneConnectionOptions *)options {
    if ([scene isKindOfClass:[UIWindowScene class]]) {
        app_scene = (UIWindowScene *)scene;
        attach_window();
    }
    for (UIOpenURLContext *context in options.URLContexts)
        import_shared_file(context.URL);
}

- (void)scene:(UIScene *)scene openURLContexts:(NSSet<UIOpenURLContext *> *)contexts {
    for (UIOpenURLContext *context in contexts)
        import_shared_file(context.URL);
}
@end

/* SDL 2.30 keeps the app running after SDL_main returns, which after a startup error would
   leave a frozen screen. Once the player has dismissed the error alert, close the app. */
static int run_game(int argc, char *argv[]) {
    int status = SDL_main(argc, argv);
    if (ios_error_shown())
        exit(status ? status : 1);
    return status;
}

/* SDL.h renamed main() in main.c to SDL_main; this is the real entry point (as in SDL's
   src/main/uikit/SDL_uikit_main.c). */
#undef main
int main(int argc, char *argv[]) {
    return SDL_UIKitRunApp(argc, argv, run_game);
}
