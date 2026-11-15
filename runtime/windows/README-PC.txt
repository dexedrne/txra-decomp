TXRA PC for Windows (64-bit)
============================

A native PC port of Tokyo Xtreme Racer Advance: a static recompilation of the
cartridge's machine code, made with the TXRA project. NO GAME DATA IS INCLUDED: this folder has no ROM, graphics,
sound or other cartridge content. You need your own dump of the cartridge.

Required ROM
------------
Tokyo Xtreme Racer Advance cartridge, game code BTZE, 4 MiB (4,194,304 bytes)
SHA-1: {rom_sha1}

Any other dump or revision is refused at startup.

Run
---
1. Unzip the whole folder anywhere. Keep SDL2.dll next to txra-pc.exe.
2. Drag your cartridge .gba file onto txra-pc.exe.
   Or, from a command prompt:  txra-pc.exe --rom "C:\path\to\cartridge.gba"
3. The executable is not code-signed, so Windows SmartScreen may warn the
   first time: choose "More info", then "Run anyway".

Requires 64-bit Windows 10 (version 1903 or newer, for non-ASCII file paths) or Windows 11.

Controls
--------
Action               Keyboard              Controller (Xbox / PlayStation)
Game A / B           X / Z                 A / B  (Cross / Circle)
Start / Select       Enter / Backspace     Menu / View  (Options / Create)
Directions           Arrow keys            D-pad or left stick
R / L                S / A                 Right / left shoulder
PC pause menu        Escape                Guide, or Menu + View together
Fullscreen           F11 or Alt+Enter      Pause menu
Screenshot           F8                    Pause menu
Debug 3x / 0.5x      Hold Tab / hold `     -

Quit from the PC pause menu (Escape, then QUIT). Losing window focus pauses.

Saves and settings
------------------
Everything is kept in your user folder:

    %APPDATA%\dexedrne\TXRA\
    (usually C:\Users\<you>\AppData\Roaming\dexedrne\TXRA\)

  txra.sav          the cartridge EEPROM save
  bindings.ini      key and controller bindings; edit it, then restart
  shot-*.bmp        F8 screenshots
  last-run.log      startup and performance log when started from Explorer or by
                    dragging a ROM onto the exe (from a console the log prints there)
  unknown-targets.log  normally empty; send it with a bug report if it is not
  last-run.json     run statistics

"Reset save" in the pause menu, or --reset-save at launch, first moves the old
save to a timestamped .bak file in the same folder. --save FILE uses another
save file.

Options
-------
--rom FILE  --save FILE  --bindings FILE  --reset-save  --fullscreen
--aspect-fit  --no-vsync  --no-focus-pause  --mute  --help

Checking the download
---------------------
SHA256SUMS lists the SHA-256 of every file in this folder. In PowerShell:

    Get-FileHash .\txra-pc.exe -Algorithm SHA256

Third-party
-----------
SDL2.dll is Simple DirectMedia Layer {sdl_version}, the unmodified official MinGW
build, under the zlib license (SDL2-LICENSE.txt).
