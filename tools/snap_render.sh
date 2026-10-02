#!/bin/zsh
# Full render from a frozen copy of the app (src, scripts, config and data copied; node_modules, public and audio
# linked), so the working tree can keep changing while the render runs: safe-render.sh reloads the page for every
# chunk, and a scene edited mid-render would change the later chunks.
#   tools/snap_render.sh <name> alive
# Writes out/<name>.mp4 and out/<name>.log like safe-render.sh; the snapshot stays in out/snap_<name>/ until deleted.
set -eu
ROOT=${0:A:h:h}
NAME=${1:?usage: snap_render.sh <name> <cut>}
CUT=${2:?usage: snap_render.sh <name> <cut>}
SNAP=$ROOT/out/snap_$NAME
[[ -e $SNAP ]] && { echo "$SNAP exists"; exit 1; }
mkdir -p $SNAP/app
cp -R $ROOT/app/src $ROOT/app/scripts $SNAP/app/
cp $ROOT/app/index.html $ROOT/app/vite.config.ts $ROOT/app/package.json $ROOT/app/tsconfig*.json $SNAP/app/ 2>/dev/null || true
ln -s $ROOT/app/node_modules $SNAP/app/node_modules
ln -s $ROOT/app/public $SNAP/app/public
cp -R $ROOT/data $SNAP/data
ln -s $ROOT/audio $SNAP/audio
ln -s $ROOT/out $SNAP/out
cd $SNAP/app
VITE_CUT=$CUT EUROBOOM_AUDIO=${EUROBOOM_AUDIO:-audio/pdoom_eu.mp3} exec scripts/safe-render.sh $NAME
