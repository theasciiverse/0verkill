#!/usr/bin/env python3
"""Records asciiverse/0verkill.cast, 0verkill's catalog preview, at 100x30
(hub/RECORDING.md): a local game through asciiverse/0verkill-play (server
and two bots), joined with Enter, then about 25 s of running, jumping and
shooting. Usage, from the repo root after building:
    python3 asciiverse/record-preview.py"""
import os, pty, shutil, signal, struct, subprocess, fcntl, select, tempfile, termios, time

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stage = tempfile.mkdtemp()
for f in ("0verkill", "server", "bot", "asciiverse/0verkill-play"):
    shutil.copy2(f"{root}/{f}", stage)
for d in ("data", "grx"):
    shutil.copytree(f"{root}/{d}", f"{stage}/{d}")
env = dict(os.environ, HOME=stage, TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8")
L, R, U = b"\x1b[D", b"\x1b[C", b"\x1b[A"
moves = [R, R, R, b"z", b"z", U, R, R, b"z", L, L, U, b"z", b"z", R, R, R, U, b"z", L, L, L, b"z", U,
         R, R, b"z", b"z", L, U, L, b"z", R, R, R, b"z", U, L, L, b"z", b"z", R, U, R, b"z"]
keys = [(4.0, b"\r"), (3.0, b"")] + [(0.45, k) for k in moves] + [(3.0, b"")]

pid, fd = pty.fork()
if pid == 0:
    os.execvpe("asciinema", ["asciinema", "rec", "--overwrite", "-q", "-i", "2",
        "--capture-env", "TERM,COLORTERM,LANG", "-c", f"{stage}/0verkill-play",
        f"{root}/asciiverse/0verkill.cast"], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))
for wait, key in keys:
    end = time.time() + wait
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.05)
        if r:
            try: os.read(fd, 65536)
            except OSError: break
    if key: os.write(fd, key)
# end the client the way a player quitting does; 0verkill-play then stops
# server and bots, and asciinema ends with it
for p in subprocess.run(["pgrep", "-f", r"^\./0verkill -i 127\.0\.0\.1"], capture_output=True, text=True).stdout.split():
    os.kill(int(p), signal.SIGKILL)
while True:
    r, _, _ = select.select([fd], [], [], 0.2)
    if r:
        try:
            if not os.read(fd, 65536): break
        except OSError: break
    if os.waitpid(pid, os.WNOHANG)[0]: break
shutil.rmtree(stage, ignore_errors=True)
