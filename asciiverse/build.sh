#!/bin/sh
# Builds 0verkill's client, server and bot. Linux: run inside alpine:3.22
# for fully static binaries; macOS: run on the runner, with CC_ARCH set to
# x86_64 or arm64. 0verkill needs no libraries beyond libc and libm.
#   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
# Leaves 0verkill, server and bot in the repository root. The data folder is
# compiled in as /usr/share/0verkill (system packages); each program first
# looks for data/ in the current folder, which is how av runs it.
set -eu
if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base autoconf automake >/dev/null
  ldflags="-static"
else
  ldflags=""
fi
cc="cc${CC_ARCH:+ -arch $CC_ARCH}"
autoreconf -fi >/dev/null 2>&1
./configure --prefix=/usr --datadir=/usr/share CC="$cc" LDFLAGS="$ldflags" >/dev/null
# the data path is a compiler flag, so stale objects would keep an old one
make clean >/dev/null 2>&1 || true
make 0verkill server bot >/dev/null
strip 0verkill server bot
