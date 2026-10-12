#!/bin/sh
# R58e / D49: run a command over a disposable copy of this repository under OS isolation, and refuse to run
# unless every control below was demonstrated first. Linux only; needs unshare(1), prlimit(1), timeout(1) and a
# writable cgroup v1 pids (or cgroup v2) hierarchy. Nothing is installed or downloaded.
#
#   scripts/sandbox/run_isolated.sh SCRATCH -- COMMAND [ARGS...]
#
# Controls (each printed as CONTROL <name> OK with its evidence, or the run aborts):
#   pids        cgroup process limit (SBX_PIDS, default 192; browser runs need about 100)
#   namespaces  user, mount, network and PID namespaces; the command is killed with the namespace
#   network     no route outside the namespace; loopback is the only interface and is brought up by ioctl
#   target_ro   the repository is bind-mounted read-only; writes go to a copy on a size-limited tmpfs
#   scratch     tmpfs of SBX_TMPFS (default 1024m), mounted over /srv, /media or /mnt inside the namespace, holds the
#               copy, HOME, TMPDIR and caches; nothing else is writable (SCRATCH on the host only holds the inner script)
#   env         environment emptied; allowlist: PATH, HOME, TMPDIR, LANG, PYTHONUTF8, PYTHONDONTWRITEBYTECODE,
#               PLAYWRIGHT_BROWSERS_PATH, PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD, NODE_PATH (browser runs only)
#   limits      prlimit CPU seconds (SBX_CPU, default 1800), address space (SBX_AS bytes, default 6 GiB; 0 disables
#               it for runs that start Chromium or Node, which reserve address space; the cgroup memory limit
#               SBX_MEM, default 4 GiB, applies in every case),
#               file size (SBX_FSIZE, default 256 MiB), open files 1024, wall clock SBX_TIME (default 2400 s)
# The command runs inside the copy with python3 -I available on PATH. Its exit status is returned.
set -u
SCRATCH="${1:?scratch directory}"; shift
[ "${1:-}" = "--" ] && shift
[ $# -ge 1 ] || { echo "usage: $0 SCRATCH -- COMMAND [ARGS...]" >&2; exit 2; }
TARGET="$(cd "$(dirname "$0")/../.." && pwd)"
PIDS="${SBX_PIDS:-192}"; TMPFS="${SBX_TMPFS:-1024m}"; CPU="${SBX_CPU:-1800}"; AS="${SBX_AS:-6442450944}"
FSIZE="${SBX_FSIZE:-268435456}"; TIME="${SBX_TIME:-2400}"; MEM="${SBX_MEM:-4294967296}"
mkdir -p "$SCRATCH" || exit 2
SCRATCH="$(cd "$SCRATCH" && pwd)"

fail() { echo "CONTROL $1 FAILED: $2" >&2; exit 3; }

# --- pids: cgroup process limit applied to this shell and everything below it ---------------------------------
if [ -d /sys/fs/cgroup/pids ]; then
  CG="/sys/fs/cgroup/pids/lab-sandbox-$$"
  mkdir "$CG" 2>/dev/null || fail pids "cannot create $CG"
  echo "$PIDS" > "$CG/pids.max" && echo $$ > "$CG/cgroup.procs" || fail pids "cannot apply pids.max"
  [ -d /sys/fs/cgroup/memory ] && MCG="/sys/fs/cgroup/memory/lab-sandbox-$$" && mkdir "$MCG" 2>/dev/null \
    && echo "$MEM" > "$MCG/memory.limit_in_bytes" 2>/dev/null && echo $$ > "$MCG/cgroup.procs" 2>/dev/null && MEMNOTE="cgroup memory.limit_in_bytes=$MEM" || MEMNOTE="cgroup memory limit not available"
  trap 'rmdir "$CG" 2>/dev/null; [ -n "${MCG:-}" ] && rmdir "$MCG" 2>/dev/null' EXIT
elif [ -f /sys/fs/cgroup/cgroup.controllers ]; then
  CG="/sys/fs/cgroup/lab-sandbox-$$"
  mkdir "$CG" 2>/dev/null && echo "$PIDS" > "$CG/pids.max" && echo $$ > "$CG/cgroup.procs" || fail pids "cgroup v2 pids.max not writable"
  echo "$MEM" > "$CG/memory.max" 2>/dev/null && MEMNOTE="cgroup memory.max=$MEM" || MEMNOTE="cgroup memory limit not available"
  trap 'rmdir "$CG" 2>/dev/null' EXIT
else
  fail pids "no writable cgroup pids hierarchy"
fi
# Evidence: forks beyond the limit must fail.
PROBE=$(python3 -I -c "
import os,signal,time
ok=bad=0; children=[]
for i in range($PIDS+40):
    try:
        pid=os.fork()
        if pid==0: time.sleep(30); os._exit(0)
        children.append(pid); ok+=1
    except BlockingIOError: bad+=1
for pid in children: os.kill(pid,signal.SIGKILL); os.waitpid(pid,0)
print(ok,bad)")
set -- "$@"
case "$PROBE" in *" 0") fail pids "fork limit not enforced ($PROBE)";; esac
echo "CONTROL pids OK: pids.max=$PIDS, probe forked/refused=$PROBE; $MEMNOTE"

INNER="$SCRATCH/inner.sh"
cat > "$INNER" <<'INNER_EOF'
set -u
SCRATCH="$1"; TARGET="$2"; TMPFS="$3"; CPU="$4"; AS="$5"; FSIZE="$6"; shift 6
fail() { echo "CONTROL $1 FAILED: $2" >&2; exit 3; }
# The scratch tmpfs is mounted over a short existing path inside the private mount namespace (the host directory is
# only shadowed there, never written): Chromium creates UNIX sockets under TMPDIR and their paths are limited to 108 bytes.
RO="$SCRATCH/target"; W=""
for candidate in /srv /media /mnt; do [ -d "$candidate" ] && W="$candidate" && break; done
[ -n "$W" ] || fail scratch "no short mount point (/srv, /media or /mnt) exists"
mkdir -p "$RO"
# A fresh /proc for the PID namespace (private mount namespace, so the host is untouched); Chromium reads /proc/<pid>.
mount -t proc proc /proc || fail namespaces "cannot mount /proc in the namespace"
mount --bind "$TARGET" "$RO" && mount -o remount,bind,ro "$RO" || fail target_ro "bind mount failed"
if touch "$RO/.sandbox-write-probe" 2>/dev/null; then rm -f "$RO/.sandbox-write-probe"; fail target_ro "target is writable"; fi
echo "CONTROL target_ro OK: $TARGET bind-mounted read-only at $RO"
# mode=1777: Chromium refuses a temporary directory that is not sticky and world-writable (it traps on start).
mount -t tmpfs -o "size=$TMPFS,mode=1777" tmpfs "$W" || fail scratch "tmpfs mount failed"
# Evidence: a write larger than the tmpfs must be cut.
if dd if=/dev/zero of="$W/.probe" bs=1M count=100000 2>/dev/null; then rm -f "$W/.probe"; fail scratch "tmpfs size not enforced"; fi
rm -f "$W/.probe"
echo "CONTROL scratch OK: tmpfs size=$TMPFS at $W (oversized write refused)"
python3 -I - <<'PY' || fail network "loopback could not be raised"
import socket, fcntl, struct
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
flags = struct.unpack("16sh", fcntl.ioctl(s, 0x8913, struct.pack("16sh", b"lo", 0)))[1]
fcntl.ioctl(s, 0x8914, struct.pack("16sh", b"lo", flags | 1))
l = socket.socket(); l.bind(("127.0.0.1", 0)); l.listen(1)
socket.create_connection(("127.0.0.1", l.getsockname()[1]), timeout=2)
PY
if python3 -I -c "import socket; socket.create_connection(('1.1.1.1', 443), timeout=3)" 2>/dev/null; then fail network "external connection succeeded"; fi
if python3 -I -c "import socket; socket.getaddrinfo('example.com', 443)" 2>/dev/null; then fail network "name resolution succeeded"; fi
echo "CONTROL network OK: loopback up inside the namespace; external connect and DNS fail"
mkdir -p "$W/home" "$W/tmp" "$W/copy" && chmod 1777 "$W/tmp"
cp -a "$RO/." "$W/copy/" || fail scratch "copy failed"
cd "$W/copy" || fail scratch "cannot enter the copy"
ENV_LIST="PATH=/usr/local/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp LANG=C.UTF-8 PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1"
for v in PLAYWRIGHT_BROWSERS_PATH PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD NODE_PATH; do eval "val=\${$v:-}"; [ -n "$val" ] && ENV_LIST="$ENV_LIST $v=$val"; done
COUNT=$(env -i $ENV_LIST python3 -I -c "import os; print(len(os.environ))")
[ "$COUNT" -le 10 ] || fail env "environment has $COUNT variables"
echo "CONTROL env OK: $COUNT variables ($ENV_LIST)"
if [ "$AS" = "0" ]; then ASOPT=""; else ASOPT="--as=$AS"; fi
echo "CONTROL limits OK: prlimit --cpu=$CPU ${ASOPT:-"(address space unlimited: cgroup memory applies)"} --fsize=$FSIZE --nofile=1024; wall clock by timeout(1)"
echo "CONTROL namespaces OK: user, mount, net, pid (pid $$ in the namespace); command: $*"
exec env -i $ENV_LIST prlimit --cpu="$CPU" $ASOPT --fsize="$FSIZE" --nofile=1024 "$@"
INNER_EOF
timeout -k 10 "$TIME" unshare --user --map-root-user --mount --net --pid --fork --kill-child \
  sh "$INNER" "$SCRATCH" "$TARGET" "$TMPFS" "$CPU" "$AS" "$FSIZE" "$@"
STATUS=$?
echo "SANDBOX EXIT $STATUS (3 = a control failed, 124 = wall clock exceeded)"
exit $STATUS
