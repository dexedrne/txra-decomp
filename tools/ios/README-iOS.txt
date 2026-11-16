TXRA for iPhone (unsigned IPA, release candidate)
=================================================

A native iPhone build of Tokyo Xtreme Racer Advance, made by statically
recompiling the game's own code. NO GAME DATA IS INCLUDED: there is no ROM,
graphics, music, sound or text in this app. You need your own dump of the
cartridge, and the app reads it from its own folder on your iPhone.


What you need
-------------
* An iPhone with iOS 15 or newer.
* A sideloading tool (see Install) and an Apple ID. A free Apple ID works.
* Your own 4 MiB cartridge dump. Its SHA-1 must be
    4197339d4add74bb40ed02a8fba5e58096afb487
  Check it on a computer with:  shasum -a 1 /path/to/your/cartridge.gba
  Any other file is refused.


Install
-------
The IPA is unsigned on purpose: a signature would carry the name of the
person who signed it. An iPhone only runs signed apps, so tapping or opening
the IPA on the phone does nothing. Install it with a sideloading tool that
signs the app with YOUR Apple ID while installing it:

  AltStore or SideStore   install the tool on the iPhone, then open
                          txra-ios-1.2.0-unsigned.ipa with it (My Apps, +)
  Sideloadly              on a Windows PC or Mac: connect the iPhone, drop
                          the IPA in, enter your Apple ID, press Start

With a free Apple ID the signature lasts 7 days. After that the app does not
open until it is signed again: AltStore and SideStore can refresh it for you
(AltStore needs its AltServer helper running on a computer nearby; SideStore
refreshes on the phone), or install the IPA again with Sideloadly. A free
Apple ID can keep 3 sideloaded apps at a time. Re-signing with the same tool
and Apple ID keeps your save. Installing with another tool or Apple ID can
give the app a different identity, which starts with an empty TXRA folder:
copy your save out first (see Saves).

The first time, iOS has to trust your Apple ID as a developer:
  Settings > General > VPN & Device Management > your Apple ID > Trust
and on iOS 16 or newer turn on
  Settings > Privacy & Security > Developer Mode   (the iPhone restarts)


Add your cartridge dump
-----------------------
1. Open the Files app.
2. Go to Browse > On My iPhone > TXRA. (Open TXRA once first if the folder
   is not there yet.)
3. Put your .gba dump in that folder. Any file name works; baserom.gba is
   tried first. AirDrop, iCloud Drive, or Finder / Apple Devices file sharing
   over a cable all work. You can also share a .gba file to TXRA from
   another app.
4. Open TXRA. If it still shows the instructions, tap the screen.

The app reads the file on the iPhone only. It never uploads or copies it
anywhere else.


Controls
--------
Touch:
  D-pad           bottom left, 8 directions; keep the thumb down and slide
  A / B           bottom right (press between them for both)
  L / R           top corners
  Select / Start  left and right, middle
  Pause           under L; the play button resumes
Several fingers work at once, so you can steer and accelerate together.

Controllers (MFi, Xbox, PlayStation DualShock 4 and DualSense), paired in
the iPhone's Bluetooth settings:
  Game A / B        South / east face button (A / B, Cross / Circle)
  Start / Select    Menu or Options / View or Create
  Directions        D-pad or left stick
  R / L             Right / left shoulder
  Pause menu        Menu/Options + View/Create pressed together, or the
                    Home button (on some controllers iOS keeps the Home
                    button for itself; the pair always works)
The touch controls hide while a controller is used and come back as soon as
you touch the screen.


Pause menu
----------
  Resume
  Scale        Fill (the picture fills the screen height) or Integer (whole-
               number scaling: a slightly smaller, perfectly even picture
               that leaves more room for the controls). iPhones with a
               Home button start in Integer, so the controls stay off the
               speed and gear readout; the others start in Fill.
  Sound        on / off
  Screenshot   saved to the TXRA folder in Files
  Reset save   starts a new save; the old one is kept as a backup file in
               the Saves folder (see Saves)

Scale and Sound are remembered the next time you open TXRA.
Tap a row, or use the D-pad and A. Going to the Home Screen, a call or Siri
pauses the game, and it waits in this menu when you come back. iOS apps do
not quit themselves: close TXRA from the app switcher as usual.


Saves
-----
The save is in Files > On My iPhone > TXRA > Saves, as txra.sav. It is
written about a second after the game saves, and again whenever TXRA leaves
the screen, so closing the app or restarting the iPhone does not lose
progress. Reset save renames the old one to txra.sav.reset-<number>.bak in
the same folder.

Re-signing, or installing a newer version over the old app with the same
tool and Apple ID, keeps the save. Deleting the app deletes its folder and
the save with it, so copy txra.sav somewhere else first (Files: press and
hold it, then Share or Copy). To bring a save back, close TXRA in the app
switcher, put the file in the Saves folder as txra.sav, then open TXRA.


Sound
-----
Game sound plays even with the silent switch on, like other games, and music
from other apps pauses while TXRA plays. Use the volume buttons, or Sound in
the pause menu.


Troubleshooting
---------------
* Tapping the IPA does nothing, or "Unable to install": install it with a
  sideloading tool (see Install).
* TXRA stopped opening after about a week: the free signature ran out.
  Refresh it in AltStore or SideStore, or install the IPA again.
* "Untrusted Developer": Settings > General > VPN & Device Management.
* The app says the file is not the supported dump: check the SHA-1 above.
  Other revisions, regions, or trimmed or padded files are not supported.
* No sound: check the volume, Sound in the pause menu, and whether a call or
  another app is using the audio.


Check the download
------------------
    shasum -a 256 -c SHA256SUMS      (sha256sum -c SHA256SUMS on Linux)


Release candidate status
------------------------
Tested in the iOS Simulator (iOS 27.2): the same 37,200-frame scripted career
and save reload that check the PC builds reproduce every frame hash, every
sound sample and the save, and frame timing holds the game's 59.73 Hz. Not
yet tested: a physical iPhone, how the touch controls feel, physical
controllers, and installing through each sideloading tool.
