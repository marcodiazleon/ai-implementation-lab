#!/bin/sh
# R58e / D50, D54, D57: run a command over a disposable copy of this repository inside a minimal root, and refuse to
# run unless every control below was demonstrated first. Linux only; needs unshare(1), pivot_root(8), prlimit(1),
# timeout(1), python3, a writable cgroup v1 (pids and memory) or v2 hierarchy, and user namespaces. Nothing is installed.
#
#   scripts/sandbox/run_isolated.sh SCRATCH -- COMMAND [ARGS...]
#
# Three stages, three trust levels (D57):
#   stage 1 (trusted; host identity in a private mount namespace, OUTSIDE the payload's PID namespace and invisible to
#           it): mounts the size-limited tmpfs, starts stage 2, waits until the PID namespace is gone and the cgroup
#           holds no other process, then promotes the allowlisted results from the tmpfs to SCRATCH/export with
#           scripts/sandbox/promote.py (relative names only, O_NOFOLLOW, regular files with one link, per-file and
#           cumulative size limits, exclusive creation of the destination, identity and size rechecked after the copy).
#   stage 2 (supervisor; root of a user namespace with mount, network and PID namespaces and a private /proc): probes,
#           synthetic /etc, read-only nosuid nodev binds, pivot_root, controls. It holds no descriptor to any host
#           path (the script text travels as an argument, not as an open file) and it is not dumpable, so its /proc
#           entries and ptrace are closed to the payload, which has no capability over the supervisor's namespace.
#   stage 3 (payload): a nested user and mount namespace, so every read-only, nosuid and nodev flag of the toolchain is
#           locked by the kernel against remount; no_new_privs; empty environment with an allowlist. The payload is
#           root only of its own nested namespace and cannot reach stage 1 at all (another PID namespace).
#
# What the payload sees: a new root on the tmpfs where /usr, /bin, /sbin, /lib, /lib64, /opt/node22, /opt/node-tools,
# /opt/pw-browsers and the global Node modules are bind-mounted read-only, /etc is synthetic (allowlist below, D54),
# /work/copy holds the copy (writable), /work/home, /work/export and /tmp are empty scratch on the same tmpfs, /proc is
# private and /dev holds null, zero, (u)random and a shm tmpfs. The host's /home, /root, /tmp, /var, /run, the original
# target path and SCRATCH itself do not exist there and no host path is writable from inside at any stage.
# Synthetic /etc (each entry with its reason): passwd, group, hosts, nsswitch.conf written here (identity, name lookup);
# ld.so.cache, ld.so.conf and ld.so.conf.d copied (the dynamic loader finds the multiarch libraries); localtime copied;
# fonts and alternatives bind-mounted read-only (Chromium's fontconfig; the links point into the read-only toolchain).
#
# Controls (each printed as CONTROL <name> OK with its evidence, or the run aborts with exit 3 before the payload):
#   pids        cgroup process limit (SBX_PIDS, default 192; browser runs need about 100); probe prints "forked refused"
#               and refused must be above zero
#   memory      cgroup memory limit (SBX_MEM bytes, default 4 GiB), mandatory; the probe allocates above it and must end
#               with status 137 (killed by the cgroup); any other outcome, a MemoryError included, aborts
#   scratch     tmpfs of SBX_TMPFS (default 1024m), sticky, mounted by stage 1; an oversized write is cut
#   namespaces  user, mount, network and PID namespaces with a private /proc; the payload dies with the namespace
#   root        pivot_root to the minimal root: the original target path, an external dummy file written by this script
#               into SCRATCH, /home and /root are not reachable; /usr is read-only; /work is writable
#   network     no route outside the namespace; loopback is the only interface and is raised by ioctl
#   env         environment emptied; allowlist: PATH, HOME, TMPDIR, LANG, PYTHONUTF8, PYTHONDONTWRITEBYTECODE and, for
#               browser runs, PLAYWRIGHT_BROWSERS_PATH, PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD, NODE_PATH
#   fds         no process visible in the PID namespace holds a descriptor to a path outside the new root (the
#               run's own standard input, output and error, shared with the payload as its log, excepted)
#   isolation   from the payload's nested namespace: remounting the toolchain read-write is refused by the kernel, the
#               supervisor's descriptors and memory are not readable, no_new_privs is set
#   limits      prlimit CPU seconds (SBX_CPU, default 1800), file size (SBX_FSIZE, default 256 MiB), open files 1024
#               and the wall clock (SBX_TIME, default 2400 s) wrap stages 1 to 3: the probes, the copy, the payload and
#               the promotion all run inside them. An address-space rlimit (SBX_AS bytes, default 0 = none) is optional
#               because Chromium and Node reserve address space; memory is bounded by the cgroup in every case.
#   promotion   after the PID namespace is gone: the cgroup holds no process but this script's own, then promote.py
#               copies only SBX_EXPORT names (default: the regenerated evidence and logs; SBX_EXPORT_FILE_MAX and
#               SBX_EXPORT_TOTAL_MAX bytes, defaults 64 MiB and 256 MiB) into SCRATCH/export, which must be empty.
# The command runs inside /work/copy. Its exit status is returned (3 = a control failed, 124 = wall clock exceeded).
set -u
SCRATCH="${1:?scratch directory}"; shift
[ "${1:-}" = "--" ] && shift
[ $# -ge 1 ] || { echo "usage: $0 SCRATCH -- COMMAND [ARGS...]" >&2; exit 2; }
HERE="$(cd "$(dirname "$0")" && pwd)"; TARGET="$(cd "$HERE/../.." && pwd)"
PIDS="${SBX_PIDS:-192}"; TMPFS="${SBX_TMPFS:-1024m}"; CPU="${SBX_CPU:-1800}"; AS="${SBX_AS:-0}"
FSIZE="${SBX_FSIZE:-268435456}"; TIME="${SBX_TIME:-2400}"; MEM="${SBX_MEM:-4294967296}"
EXPORT_NAMES="${SBX_EXPORT:-verify.log latest.json sdd-check.json acceptance.csv requirements-matrix.md security-browser.json}"
mkdir -p "$SCRATCH" || exit 2
SCRATCH="$(cd "$SCRATCH" && pwd)"
DUMMY="$SCRATCH/outside-dummy.txt"
echo "outside the sandbox: must not be reachable by the payload" > "$DUMMY"
# Results land here after the payload, promoted by stage 1 (never written by the payload). Must be empty (exclusive creation).
EXPORT="$SCRATCH/export"; mkdir -p "$EXPORT"
[ -z "$(ls -A "$EXPORT")" ] || { echo "CONTROL promotion FAILED: $EXPORT is not empty" >&2; exit 3; }
PROMOTE="$HERE/promote.py"; [ -f "$PROMOTE" ] || { echo "CONTROL promotion FAILED: $PROMOTE missing" >&2; exit 3; }

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
  trap 'exit 143' TERM INT
elif [ -f /sys/fs/cgroup/cgroup.controllers ]; then
  CG="/sys/fs/cgroup/lab-sandbox-$$"
  mkdir "$CG" 2>/dev/null && echo "$PIDS" > "$CG/pids.max" && echo "$MEM" > "$CG/memory.max" && echo $$ > "$CG/cgroup.procs" || fail pids "cgroup v2 pids.max or memory.max not writable"
  trap 'leave /sys/fs/cgroup; rmdir "$CG" 2>/dev/null' EXIT
  trap 'exit 143' TERM INT
else
  fail pids "no writable cgroup pids and memory hierarchy"
fi

# --- stage 2: supervisor inside the namespaces (text passed as an argument: no descriptor to a host file) ------------
STAGE2=$(cat <<'STAGE2_EOF'
set -u
TARGET="$1"; DUMMY="$2"; PIDS="$3"; MEM="$4"; W="$5"; shift 5
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
# read-only binds from the host are placed inside it. Every bind is also nosuid and nodev; the flags lock in stage 3.
mount --bind "$R/etc" "$R/etc" && mount -o remount,bind,ro,nosuid,nodev "$R/etc" || fail root "cannot make the synthetic /etc read-only"
for d in /etc/fonts /etc/alternatives; do
  [ -d "$d" ] || continue
  mount --bind "$d" "$R$d" && mount -o remount,bind,ro,nosuid,nodev "$R$d" || fail root "read-only bind of $d failed"
done
for d in /usr /opt/node22 /opt/node-tools /opt/pw-browsers /usr/local/lib/node_modules_global; do
  [ -d "$d" ] || continue
  mount --bind "$d" "$R$d" && mount -o remount,bind,ro,nosuid,nodev "$R$d" || fail root "read-only bind of $d failed"
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
echo "CONTROL root OK: pivot_root done; $TARGET, the external dummy, /home, /root, /var, /run, /etc/shadow, /etc/ssh and /etc/ssl/private absent; /usr and the synthetic /etc read-only nosuid nodev; /work writable; no host path writable"
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
# No process visible here may hold a descriptor to a path outside the new root (D57): every link of every /proc/*/fd
# must be a pipe, socket, anonymous inode or a path that exists under /. Descriptors 0 to 2 are the run's own standard
# input, output and error, which the payload shares by design (they are the log of the run) and are not checked.
HELD=$(python3 -I -c "
import os
bad=[]
for pid in filter(str.isdigit, os.listdir('/proc')):
    d='/proc/%s/fd'%pid
    try: names=os.listdir(d)
    except OSError: continue
    for n in names:
        if n in ('0','1','2'): continue
        try: t=os.readlink(d+'/'+n)
        except OSError: continue
        if t.startswith('/') and not os.path.exists(t.split(' (deleted)')[0]): bad.append('%s:%s->%s'%(pid,n,t))
print(' '.join(bad))")
[ -z "$HELD" ] || fail fds "a process in the namespace holds a descriptor to a path outside the root: $HELD"
echo "CONTROL fds OK: no process in the namespace holds a descriptor outside the root (pids: $(ls /proc | grep -c '^[0-9]'))"
cd /work/copy || fail scratch "cannot enter the copy"
ENV_LIST="PATH=/usr/local/bin:/usr/bin:/bin:/opt/node22/bin HOME=/work/home TMPDIR=/tmp LANG=C.UTF-8 PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1"
for v in PLAYWRIGHT_BROWSERS_PATH PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD NODE_PATH; do eval "val=\${$v:-}"; [ -n "$val" ] && ENV_LIST="$ENV_LIST $v=$val"; done
COUNT=$(env -i $ENV_LIST python3 -I -c "import os; print(len(os.environ))")
case "$COUNT" in [0-9]*) ;; *) fail env "cannot count the environment";; esac
[ "$COUNT" -le 10 ] || fail env "environment has $COUNT variables"
echo "CONTROL env OK: $COUNT variables ($ENV_LIST)"
# Stage 3 launcher: nested user and mount namespace (read-only, nosuid and nodev flags locked by the kernel), then
# no_new_privs and dumpable again for the payload itself, then exec. The supervisor (this shell) stays non-dumpable.
STAGE3='import ctypes, os, sys
l = ctypes.CDLL(None, use_errno=True)
if l.prctl(38, 1, 0, 0, 0) != 0 or l.prctl(39, 0, 0, 0, 0) != 1: sys.exit(97)
if l.prctl(4, 1, 0, 0, 0) != 0: sys.exit(98)
os.execvp(sys.argv[1], sys.argv[1:])'
# Isolation probe from a nested namespace identical to the payload's (dummy commands, nothing written outside /work).
ISO=$(unshare --user --map-root-user --mount env -i $ENV_LIST python3 -I -c "$STAGE3" sh -c '
r="remount:"; if mount -o remount,bind,rw /usr 2>/dev/null; then r="${r}ALLOWED"; else r="${r}denied"; fi
f="supervisor-fds:"; if readlink /proc/1/fd/1 >/dev/null 2>&1 || head -c 1 /proc/1/fd/2 >/dev/null 2>&1 || echo >> /proc/1/fd/1 2>/dev/null; then f="${f}REACHABLE"; else f="${f}closed"; fi
m="supervisor-mem:"; if head -c 1 /proc/1/environ >/dev/null 2>&1; then m="${m}READABLE"; else m="${m}closed"; fi
n="no_new_privs:$(grep NoNewPrivs /proc/self/status | tr -s "\t " " " | cut -d" " -f2)"
echo "$r $f $m $n"' 2>/dev/null)
case "$ISO" in
  "remount:denied supervisor-fds:closed supervisor-mem:closed no_new_privs:1") ;;
  *) fail isolation "nested namespace probe: '${ISO:-empty}'";;
esac
echo "CONTROL isolation OK: $ISO (nested user+mount namespace, flags locked, supervisor not dumpable)"
echo "CONTROL namespaces OK: user, mount, net, pid with a private /proc (pid $$ in the namespace); command: $*"
unshare --user --map-root-user --mount env -i $ENV_LIST python3 -I -c "$STAGE3" "$@"
STATUS=$?
echo "PAYLOAD EXIT $STATUS; /work/export: $(ls /work/export 2>/dev/null | tr '\n' ' ')"
exit $STATUS
STAGE2_EOF
)

# --- stage 1: trusted, outside the PID namespace; owns the tmpfs and the promotion ---------------------------------
STAGE1=$(cat <<'STAGE1_EOF'
set -u
TARGET="$1"; TMPFS="$2"; DUMMY="$3"; EXPORT="$4"; PIDS="$5"; MEM="$6"; CG="$7"; OUTER="$8"; PROMOTE="$9"; EXPORT_NAMES="${10}"; STAGE2="${11}"; shift 11
fail() { echo "CONTROL $1 FAILED: $2" >&2; exit 3; }
# Short mount point: Chromium creates UNIX sockets under TMPDIR and their paths are limited to 108 bytes.
W=""; for candidate in /srv /media /mnt; do [ -d "$candidate" ] && W="$candidate" && break; done
[ -n "$W" ] || fail scratch "no short mount point (/srv, /media or /mnt) exists"
mount -t tmpfs -o "size=$TMPFS,mode=1777" tmpfs "$W" || fail scratch "tmpfs mount failed"
if dd if=/dev/zero of="$W/.probe" bs=1M count=100000 2>/dev/null; then rm -f "$W/.probe"; fail scratch "tmpfs size not enforced"; fi
rm -f "$W/.probe"
echo "CONTROL scratch OK: tmpfs size=$TMPFS, sticky, mounted at $W by stage 1 (outside the PID namespace)"
# Stage 2 starts non-dumpable (prctl 4) through a Python launcher that execs sh with the script text as an argument.
unshare --user --map-root-user --mount --net --pid --fork --kill-child \
  python3 -I -c 'import ctypes, os, sys
if ctypes.CDLL(None).prctl(4, 0, 0, 0, 0) != 0: sys.exit(96)
os.execv("/bin/sh", ["sh", "-c", sys.argv[1], "sh"] + sys.argv[2:])' "$STAGE2" "$TARGET" "$DUMMY" "$PIDS" "$MEM" "$W" "$@"
STATUS=$?
# Promotion only when nothing of the payload can still run: the PID namespace died with its init (unshare --kill-child)
# and the cgroup holds no process but this script's own chain.
LEFT=$(python3 -I -c "
import os, sys
me, mine = os.getpid(), {int(x) for x in sys.argv[1:]}
def parent(pid):
    try: return int([l for l in open('/proc/%d/status' % pid) if l.startswith('PPid:')][0].split()[1])
    except (OSError, IndexError, ValueError): return -1
left = [p for p in (int(x) for x in open('$CG/cgroup.procs').read().split()) if p not in mine and p != me and parent(p) not in mine | {me}]
print(' '.join(map(str, left)))" "$$" "$PPID" "$OUTER")
[ -z "$LEFT" ] || fail promotion "processes still alive in the cgroup after the namespace ended: $LEFT"
echo "CONTROL promotion OK: namespace ended, cgroup holds only the runner (status of the payload: $STATUS)"
python3 -I "$PROMOTE" "$W/root/work/export" "$EXPORT" $EXPORT_NAMES || fail promotion "promote.py refused (see above)"
exit $STATUS
STAGE1_EOF
)
if [ "$AS" = "0" ]; then ASOPT=""; else ASOPT="--as=$AS"; fi
echo "CONTROL limits OK: prlimit --cpu=$CPU ${ASOPT:-"(address space: cgroup memory applies)"} --fsize=$FSIZE --nofile=1024 and timeout ${TIME}s wrap stages 1 to 3 (tmpfs, probes, copy, payload, promotion)"
timeout -k 10 "$TIME" prlimit --cpu="$CPU" $ASOPT --fsize="$FSIZE" --nofile=1024 \
  unshare --user --map-root-user --mount \
  sh -c "$STAGE1" sh "$TARGET" "$TMPFS" "$DUMMY" "$EXPORT" "$PIDS" "$MEM" "$CG" "$$" "$PROMOTE" "$EXPORT_NAMES" "$STAGE2" "$@"
STATUS=$?
rm -f "$DUMMY"
echo "EXPORTED: $(ls "$EXPORT" 2>/dev/null | tr '\n' ' ')(allowlist: $EXPORT_NAMES)"
echo "SANDBOX EXIT $STATUS (3 = a control failed, 124 = wall clock exceeded)"
exit $STATUS
