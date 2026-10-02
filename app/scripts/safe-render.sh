#!/bin/zsh
# Crash-safe full video render. One 9399-frame render froze the Mac three times on 2026-09-29 (memory ran out:
# ffmpeg ~2 GB + Chrome GPU ~2.4 GB on top of the desktop apps). This renders 15 s chunks, each in a fresh
# process (memory can't build up, a failure costs one chunk and a re-run resumes), niced, x264 on 4 threads,
# and stops a chunk at the first memory-pressure warning (waits for normal, retries). Then concatenates the
# chunks and muxes the song once.
#   from app/:  nohup scripts/safe-render.sh <name> > ../out/<name>.log 2>&1 &
# Chunks stay in out/chunks_<name>/ (delete them once the final mp4 is checked). Scenes must be stateless.
set -u
zmodload zsh/mathfunc
cd "${0:A:h}/.."
NAME=${1:?usage: safe-render.sh <name>}
ROOT=${PWD:h}
AUDIO=$ROOT/${EUROBOOM_AUDIO:-audio/pdoom.mp3}
DIR=$ROOT/out/chunks_$NAME
FINAL=$ROOT/out/$NAME.mp4
FPS=60 CHUNK=15 PORT=5999 MIN_FREE=20
[[ -e $FINAL ]] && { echo "$FINAL exists, pick a new name"; exit 1; }
[[ -f $AUDIO ]] || { echo "no audio at $AUDIO"; exit 1; }
lsof -ti tcp:$PORT >/dev/null && { echo "port $PORT is in use"; exit 1; }
mkdir -p $DIR
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $AUDIO)
N=$(( int(ceil(DUR / CHUNK)) ))
TOTAL=$(( int(rint(DUR * FPS)) ))

# Stop on real danger only: critical pressure, under MIN_FREE % free, or swap grown by MAX_SWAP MB since the run
# started (the crashes ended with swap exhausted; swap left over from earlier jobs drains slowly and is not this
# run's doing). The "warning" level (2) fires at ~40% free with a busy browser, harmless here.
MAX_SWAP=2048
SWAP0=$(sysctl -n vm.swapusage | awk '{ print int($6) }')
mem_ok() {
  (( $(sysctl -n kern.memorystatus_vm_pressure_level) < 4 )) &&
    (( $(memory_pressure -Q | awk '/percentage/ { print int($5) }') >= MIN_FREE )) &&
    (( $(sysctl -n vm.swapusage | awk '{ print int($6) }') < SWAP0 + MAX_SWAP ))
}
mem() { echo "free $(memory_pressure -Q | awk '/percentage/ { print $5 }'), pressure level $(sysctl -n kern.memorystatus_vm_pressure_level), swap $(sysctl -n vm.swapusage | awk '{ print $6 }')"; }
kill_tree() { local c; for c in $(pgrep -P $1); do kill_tree $c; done; kill -TERM $1 2>/dev/null; }
frames() { ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 $1 2>/dev/null; }
wait_mem() {
  local i
  for i in {1..60}; do mem_ok && return 0; (( i == 1 )) && echo "waiting for memory: $(mem)"; sleep 10; done
  echo "memory did not recover in 10 min: $(mem)"; return 1
}

# one private Vite without HMR for all chunks (a saved file must not reload the page mid-render)
PDOOM_NO_HMR=1 nice -n 10 bunx vite --port $PORT --strictPort > $DIR/vite.log 2>&1 &
VITE=$!
trap 'kill_tree $VITE' EXIT
for i in {1..100}; do curl -sf -o /dev/null http://localhost:$PORT && break; sleep 0.2; done

echo "$NAME: $N chunks of ${CHUNK}s, $TOTAL frames, audio $AUDIO"
for (( i = 0; i < N; i++ )); do
  f=$DIR/c$(printf %02d $i).mp4
  from=$(( i * CHUNK )); range=(--from $from); to=end
  (( i < N - 1 )) && { to=$(( from + CHUNK )); range+=(--to $to); }
  exp=$(( (i == N - 1 ? TOTAL : (from + CHUNK) * FPS) - from * FPS ))
  [[ -f $f ]] && { echo "chunk $i: done already"; continue; }
  for try in 1 2 3; do
    wait_mem || exit 1
    echo "chunk $i (${from}s-$to) try $try, $(mem)"
    t0=$SECONDS
    nice -n 10 bun scripts/render.ts video --url http://localhost:$PORT $range --noaudio \
      --x264 aq-mode=3:threads=4 --out $DIR/tmp.mp4 > $DIR/c$i.log 2>&1 &
    rp=$! stopped=0
    while kill -0 $rp 2>/dev/null; do
      if ! mem_ok; then echo "chunk $i: memory pressure, stopping it ($(mem))"; kill_tree $rp; stopped=1; break; fi
      sleep 2
    done
    wait $rp; rc=$?
    (( stopped )) && continue
    got=$(frames $DIR/tmp.mp4)
    if (( rc == 0 )) && [[ $got == $exp ]]; then
      mv $DIR/tmp.mp4 $f; echo "chunk $i: $got frames in $(( SECONDS - t0 ))s, $(mem)"; break
    fi
    echo "chunk $i failed (exit $rc, ${got:-0}/$exp frames), see $DIR/c$i.log"
  done
  [[ -f $f ]] || { echo "chunk $i: giving up; re-run the same command to resume"; exit 1; }
  sleep 10 # let the machine breathe between chunks
done

for (( i = 0; i < N; i++ )); do echo "file '$DIR/c$(printf %02d $i).mp4'"; done > $DIR/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $DIR/list.txt -i $AUDIO -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 320k -shortest -movflags +faststart $FINAL || { echo "concat/mux failed"; exit 1; }
got=$(frames $FINAL)
[[ $got == $TOTAL ]] || { echo "final has $got frames, expected $TOTAL"; exit 1; }
echo "wrote $FINAL ($got frames, $(ffprobe -v error -show_entries format=duration -of csv=p=0 $FINAL)s)"
