#!/bin/sh
# R58e / D50: run a command over a disposable copy of this repository inside a minimal root, and refuse to run
# unless every control below was demonstrated first. Linux only; needs unshare(1), pivot_root(8), prlimit(1),
# timeout(1), a writable cgroup v1 (pids and memory) or v2 hierarchy, and user namespaces. Nothing is installed.
#
#   scripts/sandbox/run_isolated.sh SCRATCH -- COMMAND [ARGS...]
#
# What the payload sees: a new root on a size-limited tmpfs where /usr, /bin, /sbin, /lib, /lib64, /opt/node22,
# /opt/node-tools, /opt/pw-browsers and the global Node modules are bind-mounted read-only, /etc is synthetic (allowlist
# below, D54), /work/copy holds the copy (writable), /work/home, /work/export and /tmp are empty scratch on the same
# tmpfs, /proc is private and /dev holds null, zero, (u)random and a shm tmpfs. The host's /home, /root, /tmp, /var,
# /run, the original target path and SCRATCH itself do not exist there and no host path is writable from inside: after
# the payload exits, this script copies the files named in SBX_EXPORT (default: the regenerated evidence and logs)
# from /work/export to SCRATCH/export through a directory descriptor opened before pivot_root and closed for the payload.
# Synthetic /etc (each entry with its reason): passwd, group, hosts, nsswitch.conf written here (identity, name lookup);
# ld.so.cache, ld.so.conf and ld.so.conf.d copied (the dynamic loader finds the multiarch libraries); localtime copied;
# fonts and alternatives bind-mounted read-only (Chromium's fontconfig; the links point into the read-only toolchain).
#
# Controls (each printed as CONTROL <name> OK with its evidence, or the run aborts with exit 3 before the payload):
#   pids        cgroup process limit (SBX_PIDS, default 192; browser runs need about 100); probe prints "forked refused"
#               and refused must be above zero
#   memory      cgroup memory limit (SBX_MEM bytes, default 4 GiB), mandatory; the probe allocates above it and must end
#               with status 137 (killed by the cgroup); any other outcome, a MemoryError included, aborts
#   namespaces  user, mount, network and PID namespaces with a private /proc; the payload dies with the namespace
#   root        pivot_root to the minimal root: the original target path, an external dummy file written by this script
#               into SCRATCH, /home and /root are not reachable; /usr is read-only; /work is writable
#   network     no route outside the namespace; loopback is the only interface and is raised by ioctl
#   scratch     tmpfs of SBX_TMPFS (default 1024m), sticky; an oversized write is cut
#   env         environment emptied; allowlist: PATH, HOME, TMPDIR, LANG, PYTHONUTF8, PYTHONDONTWRITEBYTECODE and, for
#               browser runs, PLAYWRIGHT_BROWSERS_PATH, PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD, NODE_PATH
#   limits      prlimit CPU seconds (SBX_CPU, default 1800), file size (SBX_FSIZE, default 256 MiB), open files 1024
#               and the wall clock (SBX_TIME, default 2400 s) wrap the whole namespace: the pids and memory probes, the
#               copy and the payload all run inside them.
#               An address-space rlimit (SBX_AS bytes, default 0 = none) is optional because Chromium and Node reserve
#               address space; memory is bounded by the cgroup in every case.
# The command runs inside /work/copy. Its exit status is returned (3 = a control failed, 124 = wall clock exceeded).
set -u
SCRATCH="${1:?scratch directory}"; shift
[ "${1:-}" = "--" ] && shift
[ $# -ge 1 ] || { echo "usage: $0 SCRATCH -- COMMAND [ARGS...]" >&2; exit 2; }
TARGET="$(cd "$(dirname "$0")/../.." && pwd)"
PIDS="${SBX_PIDS:-192}"; TMPFS="${SBX_TMPFS:-1024m}"; CPU="${SBX_CPU:-1800}"; AS="${SBX_AS:-0}"
FSIZE="${SBX_FSIZE:-268435456}"; TIME="${SBX_TIME:-2400}"; MEM="${SBX_MEM:-4294967296}"
mkdir -p "$SCRATCH" || exit 2
SCRATCH="$(cd "$SCRATCH" && pwd)"
DUMMY="$SCRATCH/outside-dummy.txt"
echo "outside the sandbox: must not be reachable by the payload" > "$DUMMY"
# Results land here after the payload (copied by the script, never written by the payload).
EXPORT="$SCRATCH/export"; mkdir -p "$EXPORT"

fail() { echo "CONTROL $1 FAILED: $2" >&2; exit 3; }
leave() { echo $$ > "$1/cgroup.procs" 2>/dev/null; }

# --- pids and memory: cgroup limits applied to this shell and everything below it; both mandatory ------------------
if [ -d /sys/fs/cgroup/pids ] && [ -d /sys/fs/cgroup/memory ]; then
  CG="/sys/fs/cgroup/pids/lab-sandbox-$$"; MCG="/sys/fs/cgroup/memory/lab-sandbox-$$"
  mkdir "$CG" 2>/dev/null || fail pids "cannot create $CG"
  echo "$PIDS" > "$CG/pids.max" && echo $$ > "$CG/cgroup.procs" || fail pids "cannot apply pids.max"
  mkdir "$MCG" 2>/dev/null || fail memory "cannot create $MCG"
  echo "$MEM" > "$MCG/memory.limit_in_bytes" && echo $$ > "$MCG/cgroup.procs" || fail memory "cannot apply memory.limit_in_bytes"
  trap 'leave /sys/fs/cgroup/pids; rmdir "$CG" 2>/dev/null; leave /sys/fs/cgroup/memory; rmdir "$MCG" 2>/dev/null' EXIT
elif [ -f /sys/fs/cgroup/cgroup.controllers ]; then
  CG="/sys/fs/cgroup/lab-sandbox-$$"
  mkdir "$CG" 2>/dev/null && echo "$PIDS" > "$CG/pids.max" && echo "$MEM" > "$CG/memory.max" && echo $$ > "$CG/cgroup.procs" || fail pids "cgroup v2 pids.max or memory.max not writable"
  trap 'leave /sys/fs/cgroup; rmdir "$CG" 2>/dev/null' EXIT
else
  fail pids "no writable cgroup pids and memory hierarchy"
fi
INNER="$SCRATCH/inner.sh"
cat > "$INNER" <<'INNER_EOF'
set -u
TARGET="$1"; TMPFS="$2"; DUMMY="$3"; EXPORT="$4"; PIDS="$5"; MEM="$6"; SBX_EXPORT="$7"; shift 7
fail() { echo "CONTROL $1 FAILED: $2" >&2; exit 3; }
mount -t proc proc /proc || fail namespaces "cannot mount /proc in the namespace"
# --- probes, inside prlimit and timeout (the cgroups were applied by the parent) ---------------------------------
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
print(ok,bad)" 2>/dev/null)
case "$PROBE" in
  [0-9]*" "[1-9]*) ;;
  *) fail pids "probe did not prove a refusal (output: '${PROBE:-empty}')";;
esac
echo "CONTROL pids OK: pids.max=$PIDS, probe forked/refused=$PROBE"
# The allocation above the limit must be killed by the cgroup: status 137 (128 + SIGKILL) and nothing else.
python3 -I -c "
b=bytearray($MEM+268435456)
for i in range(0,len(b),4096): b[i]=1
print('allocated')" >/dev/null 2>&1
STATUS=$?
[ "$STATUS" -eq 137 ] || fail memory "allocation above the limit ended with status $STATUS, not 137 (killed by the cgroup)"
echo "CONTROL memory OK: limit=$MEM bytes; probe above the limit killed by the cgroup (status 137)"
# Descriptor to the host export directory, used only by this script after the payload (closed for the payload).
exec 9< "$EXPORT" || fail root "cannot open the export directory"
# Short mount point: Chromium creates UNIX sockets under TMPDIR and their paths are limited to 108 bytes.
W=""; for candidate in /srv /media /mnt; do [ -d "$candidate" ] && W="$candidate" && break; done
[ -n "$W" ] || fail scratch "no short mount point (/srv, /media or /mnt) exists"
mount -t tmpfs -o "size=$TMPFS,mode=1777" tmpfs "$W" || fail scratch "tmpfs mount failed"
if dd if=/dev/zero of="$W/.probe" bs=1M count=100000 2>/dev/null; then rm -f "$W/.probe"; fail scratch "tmpfs size not enforced"; fi
rm -f "$W/.probe"
echo "CONTROL scratch OK: tmpfs size=$TMPFS, sticky, mounted at $W"
R="$W/root"
mkdir -p "$R/usr" "$R/etc" "$R/opt/node22" "$R/opt/node-tools" "$R/opt/pw-browsers" "$R/usr/local/lib/node_modules_global" "$R/proc" "$R/dev/shm" "$R/tmp" "$R/work/copy" "$R/work/home" "$R/work/export" "$R/.old"
chmod 1777 "$R/tmp"
# Synthetic /etc (D54): nothing of the host /etc is bound as a whole.
printf 'root:x:0:0:sandbox:/work/home:/bin/sh\nnobody:x:65534:65534:nobody:/:/usr/sbin/nologin\n' > "$R/etc/passwd"
printf 'root:x:0:\nnogroup:x:65534:\n' > "$R/etc/group"
printf '127.0.0.1 localhost\n::1 localhost\n' > "$R/etc/hosts"
printf 'passwd: files\ngroup: files\nhosts: files\n' > "$R/etc/nsswitch.conf"
for f in /etc/ld.so.cache /etc/ld.so.conf /etc/localtime; do [ -e "$f" ] && cp -L "$f" "$R$f"; done
[ -d /etc/ld.so.conf.d ] && cp -r /etc/ld.so.conf.d "$R/etc/ld.so.conf.d"
for d in /etc/fonts /etc/alternatives; do [ -d "$d" ] && mkdir -p "$R$d"; done
# The synthetic /etc becomes a read-only mount of itself (root in the namespace ignores file modes), then the two
# read-only binds from the host are placed inside it.
mount --bind "$R/etc" "$R/etc" && mount -o remount,bind,ro "$R/etc" || fail root "cannot make the synthetic /etc read-only"
for d in /etc/fonts /etc/alternatives; do
  [ -d "$d" ] || continue
  mount --bind "$d" "$R$d" && mount -o remount,bind,ro "$R$d" || fail root "read-only bind of $d failed"
done
for d in /usr /opt/node22 /opt/node-tools /opt/pw-browsers /usr/local/lib/node_modules_global; do
  [ -d "$d" ] || continue
  mount --bind "$d" "$R$d" && mount -o remount,bind,ro "$R$d" || fail root "read-only bind of $d failed"
done
for l in bin sbin lib lib64; do [ -L "/$l" ] && ln -s "usr/$l" "$R/$l"; done
for n in null zero random urandom; do touch "$R/dev/$n" && mount --bind "/dev/$n" "$R/dev/$n" || fail root "cannot provide /dev/$n"; done
ln -s /proc/self/fd "$R/dev/fd"; ln -s /proc/self/fd/0 "$R/dev/stdin"; ln -s /proc/self/fd/1 "$R/dev/stdout"; ln -s /proc/self/fd/2 "$R/dev/stderr"
mount -t tmpfs -o size=256m,mode=1777 tmpfs "$R/dev/shm" || fail root "cannot mount /dev/shm"
cp -a "$TARGET/." "$R/work/copy/" || fail scratch "copy failed"
mount --rbind "$R" "$R" && mount -t proc proc "$R/proc" || fail root "cannot prepare the new root"
cd "$R" && pivot_root . .old && cd / && umount -l /.old && rmdir /.old || fail root "pivot_root failed"
# Evidence after the switch: host paths gone, toolchain read-only, scratch writable.
[ ! -e "$TARGET" ] || fail root "original target path $TARGET is reachable"
[ ! -e "$DUMMY" ] || fail root "external dummy file is reachable"
[ ! -e /home ] && [ ! -e /root ] && [ ! -e /var ] && [ ! -e /run ] && [ ! -e /export ] || fail root "/home, /root, /var, /run or /export is reachable"
for f in /etc/shadow /etc/gshadow /etc/ssh /etc/ssl/private /etc/sudoers; do [ ! -e "$f" ] || fail root "$f is reachable"; done
if touch /usr/.sandbox-write-probe 2>/dev/null; then fail root "toolchain is writable"; fi
if python3 -I -c "open('/etc/hosts','a')" 2>/dev/null; then fail root "/etc is writable"; fi
touch /work/.sandbox-write-probe && rm -f /work/.sandbox-write-probe || fail root "scratch is not writable"
echo "CONTROL root OK: pivot_root done; $TARGET, the external dummy, /home, /root, /var, /run, /etc/shadow, /etc/ssh and /etc/ssl/private absent; /usr and the synthetic /etc read-only; /work writable; no host path writable"
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
cd /work/copy || fail scratch "cannot enter the copy"
ENV_LIST="PATH=/usr/local/bin:/usr/bin:/bin:/opt/node22/bin HOME=/work/home TMPDIR=/tmp LANG=C.UTF-8 PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1"
for v in PLAYWRIGHT_BROWSERS_PATH PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD NODE_PATH; do eval "val=\${$v:-}"; [ -n "$val" ] && ENV_LIST="$ENV_LIST $v=$val"; done
COUNT=$(env -i $ENV_LIST python3 -I -c "import os; print(len(os.environ))")
case "$COUNT" in [0-9]*) ;; *) fail env "cannot count the environment";; esac
[ "$COUNT" -le 10 ] || fail env "environment has $COUNT variables"
echo "CONTROL env OK: $COUNT variables ($ENV_LIST)"
echo "CONTROL namespaces OK: user, mount, net, pid with a private /proc (pid $$ in the namespace); command: $*"
env -i $ENV_LIST "$@" 9<&-
STATUS=$?
# Parent side of the namespace, after the payload: copy only the allowlisted names out of /work/export.
for name in $SBX_EXPORT; do [ -f "/work/export/$name" ] && cp "/work/export/$name" "/proc/self/fd/9/$name"; done
echo "EXPORTED: $(ls /work/export 2>/dev/null | tr '\n' ' ')(allowlist: $SBX_EXPORT)"
exit $STATUS
INNER_EOF
if [ "$AS" = "0" ]; then ASOPT=""; else ASOPT="--as=$AS"; fi
echo "CONTROL limits OK: prlimit --cpu=$CPU ${ASOPT:-"(address space: cgroup memory applies)"} --fsize=$FSIZE --nofile=1024 and timeout ${TIME}s wrap copy, probes and payload"
timeout -k 10 "$TIME" prlimit --cpu="$CPU" $ASOPT --fsize="$FSIZE" --nofile=1024 \
  unshare --user --map-root-user --mount --net --pid --fork --kill-child \
  sh "$INNER" "$TARGET" "$TMPFS" "$DUMMY" "$EXPORT" "$PIDS" "$MEM" "${SBX_EXPORT:-verify.log latest.json sdd-check.json acceptance.csv requirements-matrix.md security-browser.json}" "$@"
STATUS=$?
rm -f "$DUMMY"
echo "SANDBOX EXIT $STATUS (3 = a control failed, 124 = wall clock exceeded)"
exit $STATUS
