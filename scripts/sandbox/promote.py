"""Promote allowlisted result files from the sandbox tmpfs to the host export directory (R58e, D57).

Runs in stage 1 of scripts/sandbox/run_isolated.sh, on the host side, after the payload's PID namespace is gone. The
source directory was writable by the payload, so nothing in it is trusted:

- names come from the allowlist only and must be plain relative names (no separator, no "..", no leading dot);
- every source is opened relative to a directory descriptor with O_NOFOLLOW and must be a regular file with exactly one
  link (no symlink, hard link, FIFO, device, directory or socket);
- each file is limited to SBX_EXPORT_FILE_MAX bytes and the run to SBX_EXPORT_TOTAL_MAX bytes (defaults 64 MiB and
  256 MiB); the copy reads at most that many bytes even if the file claims otherwise;
- every name is validated before anything is written; the destination is created exclusively (O_CREAT | O_EXCL | O_NOFOLLOW)
  relative to the export directory descriptor, and a refusal removes the destinations this run had created;
- after the copy the source identity (device, inode, links, size) and the destination size are checked again.

Usage: python3 -I promote.py SOURCE_DIR EXPORT_DIR NAME [NAME...]
A missing name is skipped (the payload may not have produced it); any other anomaly is reported and the script exits 3
without promoting the rest. Exit 0 when every present name was promoted.
"""
import os
import re
import stat
import sys

NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
FILE_MAX = int(os.environ.get("SBX_EXPORT_FILE_MAX", str(64 * 1024 * 1024)))
TOTAL_MAX = int(os.environ.get("SBX_EXPORT_TOTAL_MAX", str(256 * 1024 * 1024)))
CHUNK = 1 << 20


CREATED = []  # (dirfd, name) of destinations created by this run, removed when a later name is refused


def refuse(message):
    for dirfd, name in CREATED:
        try:
            os.unlink(name, dir_fd=dirfd)
        except OSError:
            pass
    print(f"PROMOTION REFUSED: {message}", file=sys.stderr, flush=True)
    sys.exit(3)


def open_dir(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    except OSError as error:
        refuse(f"cannot open directory {path}: {error.strerror}")
    if not stat.S_ISDIR(os.fstat(fd).st_mode):
        refuse(f"{path} is not a directory")
    return fd


def promote(source_dir, export_dir, names):
    src = open_dir(source_dir)
    dst = open_dir(export_dir)
    # Phase 1: open and validate every present name (O_NONBLOCK so a FIFO cannot block the open; it is then refused by
    # its type). Nothing is written until every name passed, so a refusal never leaves a partial promotion.
    opened = []
    total = 0
    for name in names:
        if not NAME.match(name) or ".." in name:
            refuse(f"name not allowed: {name!r}")
        try:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NOCTTY | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=src)
        except FileNotFoundError:
            continue
        except OSError as error:
            refuse(f"{name}: cannot open ({error.strerror})")
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            refuse(f"{name}: not a regular file")
        if before.st_nlink != 1:
            refuse(f"{name}: {before.st_nlink} links")
        if before.st_size > FILE_MAX:
            refuse(f"{name}: {before.st_size} bytes exceed the per-file limit {FILE_MAX}")
        total += before.st_size
        if total > TOTAL_MAX:
            refuse(f"{name}: cumulative size {total} exceeds {TOTAL_MAX}")
        opened.append((name, fd, before))
    # Phase 2: exclusive destinations, bounded copy from the already validated descriptors, identity rechecked.
    promoted = []
    for name, fd, before in opened:
        try:
            out = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o644, dir_fd=dst)
        except OSError as error:
            refuse(f"{name}: cannot create the destination exclusively ({error.strerror})")
        CREATED.append((dst, name))
        copied = 0
        while copied < FILE_MAX:
            chunk = os.read(fd, min(CHUNK, FILE_MAX - copied))
            if not chunk:
                break
            os.write(out, chunk)
            copied += len(chunk)
        after = os.fstat(fd)
        written = os.fstat(out).st_size
        os.close(out)
        os.close(fd)
        if (after.st_dev, after.st_ino, after.st_nlink, after.st_size) != (before.st_dev, before.st_ino, 1, before.st_size):
            refuse(f"{name}: source changed during the copy")
        if written != before.st_size or copied != before.st_size:
            refuse(f"{name}: wrote {written} bytes, expected {before.st_size}")
        promoted.append(f"{name}:{copied}")
    os.close(src)
    os.close(dst)
    print(f"PROMOTED {len(promoted)} file(s), {total} bytes: {' '.join(promoted)}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        refuse("usage: promote.py SOURCE_DIR EXPORT_DIR NAME [NAME...]")
    promote(sys.argv[1], sys.argv[2], sys.argv[3:])
