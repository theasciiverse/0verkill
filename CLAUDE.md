# 0verkill (Asciiverse packaging)

0verkill, Brainsoft's bloody 2D ASCII-art deathmatch (2000), packaged for
the Asciiverse catalog and as system packages. Not our code: keep changes
small and list every one in PATCHES.md.

- Remotes: `upstream` is github.com/ravener/0verkill (the revival),
  `hackndev` is github.com/hackndev/0verkill, `origin` is
  github.com/theasciiverse/0verkill.
- Branch `asciiverse` = upstream plus our commits.
- Release: tag `v0.16-av.<n>` and push it.
- Local static build: `docker run --rm -v "$PWD":/src -w /src alpine:3.22
  sh asciiverse/build.sh`; autoreconf rewrites install-sh, so `git checkout`
  it afterwards.
- The game is client and server, always: even alone, `0verkill-play` runs a
  local server with two bots. The bots ignore SIGTERM.
- Preview: `python3 asciiverse/record-preview.py` after a build.
