#!/bin/bash
# Build the TXRA iPhone app on a Mac with Xcode. Nothing is signed.
#
#   tools/ios/build.sh --rom /path/to/your/cartridge.gba [--device] [--simulator]
#
# Without --device/--simulator both are built. Steps: fetch and verify SDL2, build SDL2 with
# its own Xcode project (static library, arm64 device + arm64 simulator), generate
# build/generated.c from your ROM, build the app, and for the device:
#   build/ios/txra-ios-<version>-unsigned.ipa   (Payload/TXRA.app, zip -X, sha256 printed)
# for the simulator:
#   build/ios/simulator/TXRA.app
# The ROM is read to generate the translated code and to check that the app embeds none of
# its data; it is never copied into the app.
#
# Environment: TXRA_DEPS (SDL download/build folder, default build/ios/deps), DEVELOPER_DIR,
# SOURCE_DATE_EPOCH (file dates inside the IPA; default RELEASE_EPOCH below, so a rebuild from
# a git checkout or a source export gives the same IPA).
set -euo pipefail

VERSION=1.2.0
RELEASE_EPOCH=1794700800  # 2026-11-15 00:00 UTC: file dates inside this version's IPA
MIN_IOS=15.0
SDL_VERSION=2.30.12
SDL_SHA256=ac356ea55e8b9dd0b2d1fa27da40ef7e238267ccf9324704850d5d47375b48ea
SDL_URL=https://github.com/libsdl-org/SDL/releases/download/release-$SDL_VERSION/SDL2-$SDL_VERSION.tar.gz
ROM_SHA1=4197339d4add74bb40ed02a8fba5e58096afb487

ROOT=$(cd "$(dirname "$0")/../.." && pwd -P)
OUT=$ROOT/build/ios
DEPS=${TXRA_DEPS:-$OUT/deps}
export DEVELOPER_DIR=${DEVELOPER_DIR:-/Applications/Xcode.app/Contents/Developer}

ROM= WANT_DEVICE= WANT_SIM=
while [ $# -gt 0 ]; do
    case "$1" in
        --rom) ROM=${2:?--rom needs a file}; shift 2 ;;
        --device) WANT_DEVICE=1; shift ;;
        --simulator) WANT_SIM=1; shift ;;
        -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done
if [ -z "$WANT_DEVICE$WANT_SIM" ]; then WANT_DEVICE=1; WANT_SIM=1; fi
[ -n "$ROM" ] || { echo "Give your own cartridge dump: --rom /path/to/cartridge.gba" >&2; exit 2; }
for tool in xcodebuild xcrun python3 shasum curl tar zip unzip codesign strings lipo; do
    command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }
done
ROM=$(cd "$(dirname "$ROM")" && pwd -P)/$(basename "$ROM")
[ "$(shasum -a 1 "$ROM" | cut -d' ' -f1)" = "$ROM_SHA1" ] ||
    { echo "Not the supported cartridge dump (SHA-1 must be $ROM_SHA1)" >&2; exit 1; }
mkdir -p "$OUT" "$DEPS"
DEPS=$(cd "$DEPS" && pwd -P)

echo "== SDL $SDL_VERSION"
TARBALL=$DEPS/SDL2-$SDL_VERSION.tar.gz
if [ ! -f "$TARBALL" ]; then
    curl -fsSL -o "$TARBALL.part" "$SDL_URL"
    mv "$TARBALL.part" "$TARBALL"
fi
if [ "$(shasum -a 256 "$TARBALL" | cut -d' ' -f1)" != "$SDL_SHA256" ]; then
    echo "SDL download does not match its SHA-256; removed it, run again" >&2
    rm -f "$TARBALL"
    exit 1
fi
SDL_SRC=$DEPS/SDL2-$SDL_VERSION
if [ ! -f "$SDL_SRC/.verified-$SDL_SHA256" ]; then
    rm -rf "$SDL_SRC"
    tar -xzf "$TARBALL" -C "$DEPS"
    touch "$SDL_SRC/.verified-$SDL_SHA256"
fi
# SDL's own Xcode project, target "Static Library-iOS". Its Metal shaders ship precompiled
# (src/render/metal/SDL_shaders_metal_*.h), so the .metal source is left out: that needs
# Xcode's optional Metal toolchain only to rebuild them.
SDL_FLAGS="-ffile-prefix-map=$DEPS/=deps/ -fdebug-prefix-map=$DEPS/=deps/"
sdks=""
[ -n "$WANT_DEVICE" ] && sdks="$sdks iphoneos"
[ -n "$WANT_SIM" ] && sdks="$sdks iphonesimulator"
for sdk in $sdks; do
    lib=$DEPS/sdl-build/sym/Release-$sdk/libSDL2.a
    stamp="$lib.$MIN_IOS.$(printf '%s' "$SDL_FLAGS" | shasum | cut -c1-12)"
    if [ ! -f "$stamp" ]; then
        xcodebuild -project "$SDL_SRC/Xcode/SDL/SDL.xcodeproj" -target "Static Library-iOS" \
            -configuration Release -sdk "$sdk" ARCHS=arm64 ONLY_ACTIVE_ARCH=NO \
            IPHONEOS_DEPLOYMENT_TARGET=$MIN_IOS SYMROOT="$DEPS/sdl-build/sym" OBJROOT="$DEPS/sdl-build/obj" \
            EXCLUDED_SOURCE_FILE_NAMES=SDL_shaders_metal.metal "OTHER_CFLAGS=\$(inherited) $SDL_FLAGS" \
            GCC_GENERATE_DEBUGGING_SYMBOLS=NO CODE_SIGNING_ALLOWED=NO -quiet
        rm -f "$lib".*.*; touch "$stamp"
    fi
    echo "SDL $sdk: $lib"
done

echo "== Translated code from your ROM"
cd "$ROOT"
python3 tools/ios/make_project.py --check
python3 recomp/generate.py --rom "$ROM"

build_app() {  # $1 = sdk; prints the app path
    xcodebuild -project "$ROOT/tools/ios/TXRA.xcodeproj" -target TXRA -configuration Release -sdk "$1" \
        SYMROOT="$OUT/xcode/sym" OBJROOT="$OUT/xcode/obj" TXRA_REPO="$ROOT" TXRA_DEPS="$DEPS" \
        TXRA_SDL_SRC="$SDL_SRC" CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY="" \
        DEVELOPMENT_TEAM="" -quiet >&2
    echo "$OUT/xcode/sym/Release-$1/TXRA.app"
}

check_app() {  # $1 = app; no build-machine paths, no embedded ROM data
    local exe=$1/TXRA
    if strings -a "$exe" | grep -q -F -e "$HOME" -e "/Users/" -e "$(id -un)"; then
        echo "The executable contains a build-machine path or user name" >&2; exit 1
    fi
    find "$1" -name '*.dSYM' -o -name '*.gba' | grep -q . && { echo "dSYM or ROM in the app" >&2; exit 1; }
    python3 tools/scan_embedded_rom.py "$exe" --rom "$ROM" --max-data-bytes 0 --json "$OUT/rom-scan-$2.json" >/dev/null
    echo "ROM data bytes in the executable: 0 ($(basename "$exe"), $2)"
}

if [ -n "$WANT_SIM" ]; then
    echo "== Simulator app"
    app=$(build_app iphonesimulator)
    check_app "$app" simulator
    rm -rf "$OUT/simulator"; mkdir -p "$OUT/simulator"
    cp -R "$app" "$OUT/simulator/TXRA.app"
    echo "$OUT/simulator/TXRA.app"
fi

if [ -n "$WANT_DEVICE" ]; then
    echo "== iPhone app (unsigned)"
    app=$(build_app iphoneos)
    check_app "$app" device
    stage=$OUT/ipa-stage
    rm -rf "$stage"; mkdir -p "$stage/Payload"
    cp -R "$app" "$stage/Payload/TXRA.app"
    # The linker leaves an ad-hoc signature with no identity; drop it so nothing is signed.
    codesign --remove-signature "$stage/Payload/TXRA.app/TXRA" 2>/dev/null || true
    rm -rf "$stage/Payload/TXRA.app/_CodeSignature" "$stage/Payload/TXRA.app/embedded.mobileprovision"
    epoch=${SOURCE_DATE_EPOCH:-$RELEASE_EPOCH}
    [ "$epoch" -ge 315532800 ] || epoch=315532800  # zip dates start in 1980
    stamp=$(TZ=UTC date -r "$epoch" +%Y%m%d%H%M.%S)
    find "$stage/Payload" -exec env TZ=UTC touch -h -t "$stamp" {} +
    chmod -R u+rwX,go+rX,go-w "$stage/Payload"
    ipa=$OUT/txra-ios-$VERSION-unsigned.ipa
    rm -f "$ipa"
    (cd "$stage" && find Payload | LC_ALL=C sort | TZ=UTC zip -X -q -@ "$ipa")
    rm -rf "$stage"
    unzip -l "$ipa" | grep -q ' Payload/TXRA.app/TXRA$' || { echo "IPA layout is wrong" >&2; exit 1; }
    echo "$ipa"
    echo "size $(stat -f %z "$ipa") bytes"
    echo "sha256 $(shasum -a 256 "$ipa" | cut -d' ' -f1)"
fi
