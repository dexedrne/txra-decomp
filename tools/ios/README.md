# iPhone build

This folder builds the native iPhone app: the same recompiled game code and runtime as the PC builds (`runtime/*.c` plus `build/generated.c` from `recomp/generate.py`), with an iOS shell in `runtime/ios/`, linked against SDL 2.30.12. The result is an **unsigned** IPA for sideloading and a simulator app. Player instructions are in [README-iOS.txt](README-iOS.txt).

| File | What it is |
| --- | --- |
| `build.sh` | The whole build on a Mac: SDL download and build, generated code, app, IPA |
| `make_project.py` | Writes `TXRA.xcodeproj/project.pbxproj` (standard library only; `--check` verifies the committed copy) |
| `TXRA.xcodeproj/` | The generated Xcode project (one app target, no schemes needed) |
| `Info.plist` | Bundle `beer.vyvanse.txra`, TXRA 1.2.0 (1), landscape, Files-app folder, `.gba` document type, controller keys |
| `Assets.xcassets/` | App icon (one 1024-pixel image), launch logo and launch colour |
| `make_icon.py` | Draws the icon and launch logo from code (needs Pillow; outputs are committed) |
| `README-iOS.txt` | Player README for the release |

`runtime/ios/` holds the app side: `ios.c` (ROM instructions screen, touch overlay drawing, lifecycle, remembered Scale/Sound, save location), `touch.c` (layout and hit-testing), `romscan.c` (finds the dump in Documents by SHA-1), `ios_platform.m` (entry point, window scene, safe area, shared files). Everything iOS-specific in the shared runtime is behind `#ifdef TXRA_IOS`; Linux and Windows builds do not compile `runtime/ios/`.

## Build

On a Mac with Xcode (tested with Xcode 27.2 on macOS 26) and an internet connection for the first SDL download:

```
tools/ios/build.sh --rom /path/to/your/cartridge.gba
```

`--device` or `--simulator` builds only one of them. Outputs:

- `build/ios/txra-ios-1.2.0-unsigned.ipa`: `Payload/TXRA.app`, zipped with `zip -X` from a sorted file list with fixed file dates, executable bit kept. The script prints its size and SHA-256.
- `build/ios/simulator/TXRA.app`: the same app for the arm64 iOS Simulator.

Environment: `TXRA_DEPS` (where SDL is downloaded and built, default `build/ios/deps`), `DEVELOPER_DIR` (default `/Applications/Xcode.app/Contents/Developer`), `SOURCE_DATE_EPOCH` (file dates inside the IPA; default `RELEASE_EPOCH` in `build.sh`, 1794700800 = 2026-11-15 00:00 UTC for 1.2.0).

**Reproducing the release IPA.** With the default epoch (leave `SOURCE_DATE_EPOCH` unset), the same commit, Xcode 27.2 and SDL 2.30.12, the IPA is byte-identical to the release, whether built from a git checkout or a source export; compare its SHA-256 with the release's `SHA256SUMS`. Another Xcode version gives a working but different binary.

What the script does:

1. Checks the ROM's SHA-1 (`4197339d4add74bb40ed02a8fba5e58096afb487`).
2. Downloads `SDL2-2.30.12.tar.gz` from the official libsdl-org GitHub release and checks its SHA-256 (`ac356ea55e8b9dd0b2d1fa27da40ef7e238267ccf9324704850d5d47375b48ea`; the tarball's GPG signature from Sam Lantinga was also checked when this value was pinned).
3. Builds SDL with SDL's own Xcode project, target `Static Library-iOS`, for `iphoneos` and `iphonesimulator`, arm64 only, iOS 15.0. The `.metal` shader source is excluded: SDL ships the compiled shaders as headers (`src/render/metal/SDL_shaders_metal_*.h`), and rebuilding them would need Xcode's optional Metal toolchain.
4. Runs `recomp/generate.py --rom ...` to write `build/generated.c` (ROM-derived; never committed).
5. Builds the app with `xcodebuild -target TXRA` and no signing (`CODE_SIGNING_ALLOWED=NO`, empty identity and team).
6. Checks the executable: no build-machine path or user name in its strings, no dSYM or ROM in the bundle, and `tools/scan_embedded_rom.py` finds 0 ROM data bytes.
7. Device only: removes the linker's identity-free ad-hoc signature so nothing is signed, and packages the IPA.

The app has no entitlements, so a free Apple ID can sideload it. Signing it with your own account in Xcode works too, but a signed build carries the signer's name: do not publish one.

### Build settings worth knowing

- **iOS 15.0 minimum**, the lowest deployment target Xcode 27 accepts (SDL 2.30 itself supports older). arm64, iPhone only.
- **Scene life cycle.** Apps built with the iOS 27 SDK do not launch without a `UIApplicationSceneManifest`. SDL 2.30 predates that requirement, so `ios_platform.m` provides the scene delegate, moves SDL's window into the window scene and handles files opened with the app. SDL's lifecycle events keep working because UIKit still posts the `UIApplication` notifications SDL listens to.
- **`-ffp-contract=off`** keeps the arithmetic identical to the x86-64 builds (clang would otherwise fuse multiply-adds on arm64), so the game produces the same frames and sound on every platform.
- **`-ffile-prefix-map`** for the app and SDL, no debug information, a fully stripped executable and no dSYM: the binary carries no build-machine paths.
- `generated.c` is compiled with `-O1`, as in the Makefile.

## Test in the simulator

Create a simulator of your own and boot it without the Simulator app:

```
xcrun simctl create TXRA-test com.apple.CoreSimulator.SimDeviceType.iPhone-17-Pro-Max com.apple.CoreSimulator.SimRuntime.iOS-27-2
xcrun simctl boot <udid>
xcrun simctl install <udid> build/ios/simulator/TXRA.app
xcrun simctl launch <udid> beer.vyvanse.txra          # shows the ROM instructions
D=$(xcrun simctl get_app_container <udid> beer.vyvanse.txra data)
cp /path/to/your/cartridge.gba "$D/Documents/baserom.gba"
xcrun simctl launch --terminate-running-process <udid> beer.vyvanse.txra
```

The PC command-line options work through `simctl launch` (arguments after the bundle id), with paths inside the app container. The same replay that `make check-career` runs on Linux:

```
cp tests/race-win-input.txt tests/career-reload-input.txt "$D/tmp/"
xcrun simctl launch <udid> beer.vyvanse.txra --rom "$D/Documents/baserom.gba" --headless --mute --benchmark \
    --frames 37200 --input-script "$D/tmp/race-win-input.txt" --save "$D/tmp/career.sav" \
    --stats "$D/tmp/career.json" --frame-hashes "$D/tmp/career.hashes" --audio-dump "$D/tmp/career.pcm"
```

then the reload route (`--frames 2200 --input-script "$D/tmp/career-reload-input.txt"`, same save). When `career.json` appears, compare the SHA-256 of the frame hashes, PCM and save with `tests/career-golden.json`. The app keeps running after the replay (iOS apps do not exit); stop it with `xcrun simctl terminate`. `--frame-times FILE` logs per-frame timing in a normal (visible) run.

The touch layout and hit-testing are plain C and are tested on Linux: `make check-touch` (also part of `make check-desktop`).

## Files the app writes

- `Documents/Saves/txra.sav` and its reset backups `txra.sav.reset-*.bak`: visible in Files (On My iPhone > TXRA > Saves) so players can copy them out. A save from an earlier build in `Library/Application Support/dexedrne/TXRA/` is moved there once.
- `Documents/shot-*.bmp`: pause-menu screenshots.
- `Library/Application Support/dexedrne/TXRA/`: `settings.ini` (Scale and Sound from the pause menu), `bindings.ini` (controller buttons; a damaged file is renamed to `bindings.ini.rejected` and the defaults are used), `last-run.json` and `unknown-targets.log`.

Until the player picks a scale, the app starts in Fill when A fits beside the filled picture (every phone with a notch or Dynamic Island) and in Integer otherwise (16:9 phones with a Home button), where the controls then stay clear of the race HUD. A startup error after the window is up (for example the renderer failing) is shown as an alert, and the app closes when it is dismissed.
