# Changes from upstream

This is the Asciiverse packaging of 0verkill by Brainsoft (Brain, Clock and
others, 2000; GPL-2.0), version 0.16pre2.

Lineage:
- Brainsoft's 0.16 sources, imported by Marek Vasut in 2008.
- [hackndev/0verkill](https://github.com/hackndev/0verkill) (2008 to 2010):
  compiler-warning fixes and small corrections; remote `hackndev`.
- [ravener/0verkill](https://github.com/ravener/0verkill) (2021 to 2026),
  "takes over from where hackndev left off": a fixed md5 checksum, an
  out-of-bounds memory access fix, and the `extern` declarations GCC 10 and
  newer need. This is `upstream`, and the `asciiverse` branch starts from it.

The md5 fix changes the network checksum, so these builds do not play with
old 0.16 servers, only with each other.

## Code

None of ours.

## Packaging (new files)

- `asciiverse/0verkill-play`: the start script. With no arguments it starts
  a server and two bots and connects the client to them, and stops server
  and bots when the client ends (a watcher covers a closed terminal too).
  With arguments it runs just the client (`-i <host>` joins a server
  elsewhere). Works from an av install and from the system packages.
- `asciiverse/build.sh`: static Linux builds in Alpine, macOS builds per
  architecture. Only the client, server and bot are built.
- `asciiverse/nfpm.yaml`: .deb, .rpm, .apk and Arch packages; server and
  bot are installed as 0verkill-server and 0verkill-bot.
- `asciiverse/record-preview.py`: records the catalog preview, a local game.
- `.github/workflows/release.yml`: builds all of it on a tag.

## Not built

- Windows: the original Win32 port is unmaintained (see upstream's README).
- The X11 client, the level editor and the AVI tools.
