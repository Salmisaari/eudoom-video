#!/bin/zsh
# Full timing-map pipeline for audio/pdoom.mp3 -> data/lyrics.json, data/audio.json (+ QA plots)
set -e
cd "$(dirname "$0")"
export PYTHONUNBUFFERED=1
echo "== demucs"; [ -f stems/htdemucs_ft/pdoom/vocals.wav ] || uv run python -m demucs -n htdemucs_ft -o stems ../audio/pdoom.mp3
echo "== karaoke lead"
if [ ! -f stems/karaoke/lead.wav ]; then
  mkdir -p stems/karaoke
  uv run audio-separator ../audio/pdoom.mp3 --model_filename mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt --output_dir stems/karaoke --model_file_dir .cache/audio-separator --output_format WAV
  f=$(ls stems/karaoke/*\(Vocals\)*.wav | head -1); mv "$f" stems/karaoke/lead.wav
fi
echo "== vocals16k"; uv run python -c "import common, soundfile as sf; y,sr=common.load_stem('vocals', sr=16000); sf.write(str(common.WORK/'vocals16k.wav'), y, 16000); print(len(y)/16000)"
echo "== ctc"; uv run python ctc_emissions.py
echo "== whisper"; uv run python whisper_run.py turbo
echo "== vocal feats"; uv run python vocal_feats.py
echo "== align"; uv run python align.py --plots
echo "== analyze"; uv run python analyze.py --plots
echo "== DONE"
