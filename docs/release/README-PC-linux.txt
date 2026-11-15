TXRA PC for Linux x86-64 (release candidate)
=============================================

A native PC build of Tokyo Xtreme Racer Advance, made by statically
recompiling the game's own code. NO GAME DATA IS INCLUDED: there is no ROM,
graphics, music, sound or text in this package. You need your own dump of the
cartridge, and the program reads it when it starts.


What you need
-------------
* 64-bit x86 Linux with glibc @GLIBC@ or newer.
* SDL2 (2.0.14 or newer) installed from your distribution:
    Debian, Ubuntu, Mint, Pop!_OS:   sudo apt install libsdl2-2.0-0
    Fedora:                          sudo dnf install SDL2
    Arch:                            sudo pacman -S sdl2-compat
  (Distributions that ship SDL2 through sdl2-compat should work, but only
  SDL 2.30 has been tested.)
* Your own 4 MiB cartridge dump. Its SHA-1 must be
    4197339d4add74bb40ed02a8fba5e58096afb487
  Check it with:  sha1sum /path/to/your/own/cartridge.gba
  Any other file is refused at startup.


Run
---
    tar xzf txra-pc-linux-x86_64.tar.gz
    cd txra-pc-linux-x86_64
    ./txra-pc --rom /path/to/your/own/cartridge.gba

A bare path works too (./txra-pc cartridge.gba). Without a ROM argument it looks
for baserom.gba in the current folder.

Launch options: --fullscreen  --aspect-fit  --no-vsync  --mute
                --no-focus-pause  --save FILE  --bindings FILE
                --reset-save  --help


Controls
--------
  Action                Keyboard              Standard controller
  Game A / B            X / Z                 South / east face button
  Start / Select        Enter / Backspace     Menu or Options / Back or Create
  Directions            Arrow keys            D-pad or left stick
  R / L shoulders       S / A                 Right / left shoulder
  PC pause menu         Escape                Guide, or Menu + Back together
  Fullscreen            F11 or Alt+Enter      Pause menu
  Screenshot            F8                    Pause menu
  Debug 3x / half speed Hold Tab / grave (`)  -

Choose Quit in the Escape menu to exit. Controllers can be connected while
the game runs; keyboard and controller work together. Losing window focus
pauses the game (--no-focus-pause turns that off).


Saves and settings
------------------
Everything is kept in one folder:
    $XDG_DATA_HOME/dexedrne/TXRA/   (normally ~/.local/share/dexedrne/TXRA/)

    txra.sav        your game save (back this file up to keep progress)
    bindings.ini    key and controller bindings
    shot-*.bmp      F8 screenshots
    last-run.json   diagnostics from the last session
    unknown-targets.log  normally empty; send it with a bug report if it is not

The startup log prints the exact paths. A txra.sav left in the folder you
launch from is copied into the save folder once, if none exists there yet.
To rebind, edit bindings.ini and restart (keys use SDL scancode names, buttons
use SDL controller button names, e.g. key.a=Space or pad.a=y). Reset Save in
the pause menu keeps a timestamped .reset-*.bak backup of the old save.


Check the download
------------------
    sha256sum -c SHA256SUMS


Release candidate status
------------------------
Tested on Linux: frame-by-frame picture and audio replays and a long career
replay match the recorded reference results. Not yet tested by hand:
physical controllers, real speakers, and window pacing on every desktop.
