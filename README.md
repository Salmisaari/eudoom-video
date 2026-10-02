# I'm Upping My EU Doom — music video

![I see sparks of AGI](docs/preview.png)

A remix of "I'm Upping My P(doom)" with 21 lines rewritten about Europe and sung into the original recording, and a code-rendered music video printed in four inks like a European regulation.

**Watch:** _link coming_

## How it was made

I wrote one prompt in a terminal and let Claude Opus 5.5 run on my laptop overnight for 12 hours. After that came 10 follow-up versions, in which I picked lines by ear and Claude rebuilt scenes. The renders crashed my laptop 8 times along the way.

Claude wrote the code, aligned every word and syllable to the song, re-sang the EU lines with ElevenLabs and rendered each version. It searched the web for the history behind each line and checked the sources.

The prompt, in part:

> Focus on maximalist typography, not a literal rendition of each verse, lyrics always perfectly in sync with the video. Use whisper models and audio analysis tools to get timestamps for *everything* in the song. … I go to sleep so you will have full night to work independently. … please be braver

[`docs/PROCESS.md`](docs/PROCESS.md) is the log of what we tried, what failed and what worked. [`docs/REFERENCES.md`](docs/REFERENCES.md) lists the sources behind every scene.

I'm not a sound or motion engineer. I've studied some of both, and what I brought was taste, an eye for patterns and a lot of ideas from curiosity. Claude did the engineering.

The renderer and the timing pipeline are built on [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video) by Giacomo Magnanini.

## How the problems got solved

1. **Make everything measurable first.** Before any design, Claude built a timing map of the whole song: every word, syllable, note, beat and bass hit. Every frame is a function of that map, so sync is something to check, not a matter of taste.
2. **Generate many, measure, then a person picks.** For each changed line Claude made about nine takes and measured them against the original singer: rhythm, pitch, clarity, words. The best went into folders as OLD and NEW, and I picked by ear. The measurements found causes; the ear decided. When they disagreed ("AC" measured fine but sounded like "AAH"), the ear won.
3. **When something fails, change the approach, not the settings.** Voice changer, text-to-speech and Suno's section edit failed, so we used inpainting. Tuned lines sounded broken, so we spliced whole lines untouched. Illustrations felt flat, so we used real archival plates. A photo's license didn't fit, so we drew the scene.
4. **Small, checked steps, nothing overwritten.** Each change went stills, then an error check over all 9,396 frames, then a preview clip, then the full render. Every version got a new name, so the last good one was always there to compare.
5. **The brief is constraints, not instructions.** Maximalist type, always in sync, real European references, a positive future. After that, plain-language feedback ("too much motion", "the stamp should land on the bass") that Claude turned into code.
6. **Every failure becomes a guardrail.** The laptop crashed, so renders run in memory-guarded chunks. An edit deleted four scenes, so edits go one method at a time with an automatic check. One bad frame corrupted every later frame, so a full error scan runs before every render.
7. **Two tracks in parallel.** A background agent ran the audio rounds while the main session built the picture; heavy jobs took turns.

## Motion engineering

- **Everything keys off the song.** Each word appears on the frame it's sung. A held note is shown by motion (tracking, scale, the page moving), never by stretched letters.
- **A camera over real plates.** Each archival image is filmed by a virtual camera with keyframes on sung words: it lands on the detail a word is about as the word is sung, drifts while a line holds and pushes in on every kick.
- **Motion on the rhythm.** Stamps come down on bass notes with anticipation, impact and rebound. GPU blocks stack three per 16th note, the unicorns come off the line one per beat, the fuse burns to the beat it explodes on, and cuts sit on bar lines.
- **Words that ride the picture.** In L4 the lyric is laid along the loss curve as it is drawn, each word turned to the line's direction.
- **Characters on their own clock.** The figures move at 12 drawings a second with a slight boil, like hand-drawn animation, and the mouth follows the vocal from the alignment.
- **The print.** A final pass prints every frame in four inks with halftone dots and plates slightly out of register. One shot swaps its yellow plate for fluorescent green.

## Sound engineering

- **Timing to the syllable.** The vocal is split from the music (BS-RoFormer), aligned word by word and letter by letter (Whisper cross-checked with CTC forced alignment), syllables are snapped to vocal onsets and notes read with Praat. Beats, bars and every kick, snare and bass note are marked.
- **Replacing a line inside the mix.** ElevenLabs Music regenerates a window of at least 3 seconds with the new words, conditioned lightly on the original. The new line is spliced in whole, at the quietest point near each boundary, with crossfades matched to how correlated the two signals are, and the centre and sides levelled to the original.
- **Small surgical fixes.** Lifting one note that sat a few semitones low, restoring an "s" the separation had lost, closing "zoom" on its m, borrowing 90 ms of a vowel from the same hook earlier in the song, retiming syllables onto the original's vowel grid (Praat).
- **Measuring every take.** Each take is scored against the original singer: syllable timing, pitch in cents, clarity, letter-level confidence, a check of what Whisper hears, and the glide in "ee-yoo". Seams are checked to within half a decibel.

## Changing the words of a finished song

The part I'm most proud of is the remix itself: changing the words inside an existing song, so the voice, the band and the timing stay the original's.

How it works:
- **Inpainting.** ElevenLabs Music regenerates a short window of the song (at least 3 seconds) with the new lyric, conditioned at low strength on the same stretch of the original. Low strength keeps the melody while the new words get sung.
- **Whole lines, untouched.** Each new line is spliced back in as the singer sang it. Pitch-tuning and time-warping measured better but sounded broken.
- **Measured against the original.** Every take is compared with the original singer: the vocal split, letter-level alignment, the notes, the syllable timing, clarity and width. Whisper checks the words.
- **Picked by ear.** Each changed line goes into a folder as OLD and NEW, and a person picks.

It isn't perfect yet. A few lines still sound slightly off:
- **L16** "I feel my AC temperatures rearranging": six syllables sit on the notes of the original's "atoms", so a few notes are off the melody.
- **L19** "I hear the basic income gloom": "gloom" doesn't close on its m and can sound like "glue".
- **L29** and **L40**: "EU" isn't sung as a clean "ee-yoo".
- **L37** "Post-AI-bubble": the glide between A and I is short.
- A few splices are audible if you listen closely.

The scripts are in `audio/el_music/`, and [`docs/PROCESS.md`](docs/PROCESS.md) has everything that failed along the way. If you take it further, with a better vocal model, a cleaner splice or a whole new song, open an issue or a pull request.

## Layout

- `audio/pdoom_eu.mp3`: the EU edition of the song.
- `audio/el_music/`: the song pipeline: ElevenLabs Music inpainting (`eu*_inpaint.py`), measuring takes against the original (`compare.py`, `line_round.py`, `pick_gate.py`, `sylfit.py`) and the song builds (`final*.py`). Each build's `v*_sources.json` lists which take each line comes from.
- `analysis/timing_eu.py`: writes `data/timing_eu.json` from BS-RoFormer stems, Whisper, CTC forced alignment, Praat notes and the drum, bass and synth onsets.
- `data/`: the timing map (words, syllables, notes, beats, onsets) and the mouth shapes for the lip-sync.
- `app/`: the renderer, TypeScript + three.js with bun + Vite.
  - `src/engine/`: mexicat's engine plus `print.ts`, the four-ink print pass.
  - `src/scenes/alive.ts`: the video. It builds on `animatic.ts` and `hybrid.ts`; `_idol.ts`, `_kit.ts` and `_kin.ts` hold the shared drawing and type code.
  - `public/animatic/`: the archival plates and film frames.
- `research/`: research notes behind the scenes.
- `tools/`: `snap_render.sh` and helpers.

## Requirements

[bun](https://bun.sh), Google Chrome and ffmpeg with libx264. The analysis and song tools need [uv](https://docs.astral.sh/uv/); the song tools also need your own ElevenLabs API key and an upload of the song (`audio/el_music/upload.json`, not included). The render's memory guard uses macOS's `memory_pressure`.

## Preview

```sh
cd app
bun install
bunx vite
```

Open `http://localhost:5173`. `?t=23` starts at 23 seconds. Space plays and pauses, ← and → seek, `,` and `.` step one frame.

## Render the video

```sh
mkdir -p out
tools/snap_render.sh eudoom alive          # out/eudoom.mp4, 1920×1080 at 60 fps, with the song
```

The render runs in 15-second chunks, each in a fresh browser process, and pauses when memory gets tight. A single-process render froze a 16 GB Mac. It takes about 30–40 minutes.

Check for scene errors before a full render:

```sh
cd app && bun scripts/render.ts perf --from 0 --to 156.6 | grep "render error"
```

## Regenerate the timing data

The renderer only needs the committed `data/*.json`. To rebuild them you need the song's BS-RoFormer vocal stem (audio-separator, `model_bs_roformer_ep_317`); the models download several GB:

```sh
cd analysis
uv run python timing_eu.py vocal whisper ctc words write
```

## Credits

- **Song:** "I'm Upping My P(doom)", lyrics by osmarks, built on an opening verse and chorus by MusicPerson; the original was made with Udio in 2024. The recording is the "Claude-Pop" version made with Suno by deckard (@slimer48484). The EU lines were written for this edition and re-sung with ElevenLabs Music.
- **Renderer:** [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video) (MIT).
- **Plates:** public-domain and CC0 archive images from The Met, the Rijksmuseum, Carnavalet, the British Library, the Smithsonian and Wikimedia Commons. Every image is listed in [CREDITS.md](CREDITS.md).
- **Fonts:** SIL Open Font License.

## License

The code is under the [MIT License](LICENSE), which keeps the pdoom-video copyright. The song and lyrics stay with the people who wrote and made them. The fonts and images keep their own terms (see CREDITS.md).
