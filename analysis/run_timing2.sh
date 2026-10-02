#!/bin/zsh
# Continue the timing pipeline after stems exist: vocals16k, CTC, Whisper, vocal feats, align, analyze.
set -e
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1
until ls stems/karaoke/*.wav >/dev/null 2>&1 && ! pgrep -f "audio-separator ../audio/pdoom.mp3" >/dev/null; do sleep 5; done
f=$(ls stems/karaoke/*[Vv]ocals*.wav 2>/dev/null | grep -v -i instrumental | head -1); [ -n "$f" ] && [ "$f" != "stems/karaoke/lead.wav" ] && mv "$f" stems/karaoke/lead.wav
ls -la stems/karaoke
echo "== vocals16k"; uv run python -c "import common, soundfile as sf; y,sr=common.load_stem('vocals', sr=16000); sf.write(str(common.WORK/'vocals16k.wav'), y, 16000); print(len(y)/16000)"
echo "== ctc"; uv run python ctc_emissions.py
echo "== whisper"; uv run python whisper_run.py turbo
echo "== vocal feats"; uv run python vocal_feats.py
echo "== align"; uv run python align.py --plots
echo "== analyze"; uv run python analyze.py --plots
echo "== DONE"
