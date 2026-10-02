# What we tried until it worked

The working log of the EU edition, condensed: the song, the picture and the operations, including what failed.

I wrote one prompt and let my laptop run overnight for 12 hours. Then came 10 follow-up versions. The renders crashed the laptop 8 times. Everything ran in Claude Code (Claude Opus 5.5) in a terminal on a 16 GB MacBook. I gave the direction and picked; Claude wrote the code, did the research, ran the audio and timing tools and rendered.

## Timeline

| When | Song | Picture |
|---|---|---|
| 29 Sep 2026 | First swap test (one word via ElevenLabs Music inpainting); all EU lines sung in (v1–v4) | Treatment v1 ("printed in Europe": a four-ink print engine); animatics v0–v4; the idol drawn by the engine |
| 30 Sep | Lines judged against the original; untouched takes only; v5–v9 from my picks | Animatics v5–v9: a researched archival plate for most lines |
| Night of 30 Sep | | The overnight brief (below): timing map for every word, syllable, note and drum hit; the kinetic type edition, a hybrid and a mix |
| 1 Oct | v10–v13: Pinocchio, Eurovision eyes, transformers, the L9–10 retake, the 0:59 hook fix, "Post-AI-bubble" | The story cut "filmed" along the lyric (alive v1–v7) and many scene rebuilds |
| 2 Oct | v14: the hook's "EU" sung "ee-YOO" | alive v8–v10: Marey's train graph, Utopia, the GPU outro, the signed page |

In numbers:
- 14 song builds;
- full renders: 10 animatics, 2 type editions, 1 hybrid, 1 mix and 10 versions of the final cut;
- about 115 commits.

The overnight brief, word for word except for the cut middle:

> Now you should still do the final design and especially focus on slides which just put the lyrics there put doesn't
> move. Focus on maximalist typography, not a literal rendition of each verse, lyrics always perfectly in sync with the
> video. Use whisper models and audio analysis tools to get timestamps for *everything* in the song. Study big similar
> innovation limiting things or legistlation that has beel called out against innovation. […] I go to sleep so you will
> have full night to work independently. You can craft anything you want and tomorrow I can then mix and match. Make
> yourself proud and be excited of the intellectual combinations you've found. we have the power to do anything, please
> be braver

Its constraints (maximalist typography, not literal, always in sync, timestamps for everything) are the ones mexicat
described for the original pdoom video. That night produced:
- the timing map;
- the type edition;
- the research behind the later scenes.

The final cut combines that with the story cut from the two days before, and was then refined over the next day.

## The song: changing words inside a finished song

The goal: change 21 lines to EU lyrics without re-singing the song, so the voice, the band and the timing stay the original's.

What failed:
- **ElevenLabs voice changer on singing.** It kept 8–14 % of the melody; sung pitch doesn't survive speech-to-speech.
- **Cloned-voice text-to-speech fitted into the slot.** It wasn't intelligible.
- **Suno's single-word "replace section".** It needs a 10–30 s window, so it can't change one word.
- **Unconditioned inpainting.** It sang the new words 2–4 semitones off the original melody ("quite terrible").
- **Pitch-tuning and time-warping the takes onto the original.** The measurements improved, but I heard every tuned or warped line as broken. Part of the cause: tuning left and right separately halved their correlation.
- **Equal-power crossfades at the seams.** Every seam swelled +2 to +6 dB for 40 ms (the "bug before where the faxes zoom").

What worked:
- **ElevenLabs Music inpainting.** Regenerate a short window (at least 3 s) with the new lyric, conditioned at low strength on the same range of the original, then splice only the new phrase back in. Low strength balances keeping the melody against singing the new words.
- **Whole lines, untouched.** Whole takes spliced in with no tuning and no warping sounded smooth. Where two changed lines touch, take both from one take, so the transition is the singer's own.
- **Small, targeted fixes only.** Examples:
  - lifting the one note that sat 4–5 semitones low;
  - lifting the take's own "s", which separation had left near silent;
  - closing "zoom" on its "m";
  - for the 0:59 hook, borrowing 90 ms of the "E" from the same hook earlier in the song, where the cut had landed inside a held note.
- **Correlation-aware crossfades,** measured at every seam: within ±0.5 dB.

## Measuring against listening

We measured every candidate against the original singer:
- BS-RoFormer vocal split;
- CTC forced alignment for words and letters;
- Praat for notes;
- timing for each syllable;
- clarity, width and level.

It found real causes my ear could only call "drift". In L9–10 it was a 0.2 s hole in a held note plus early syllables.

But the ear has the last word:
- **"AC" in L16.** It measured fine on the letter scores, but I heard "AAH". Whisper heard "my ass" / "my air", so Whisper agreed with the ear more than the letter scores did.
- **"Income's soon" in L19.** No take out of 25 made the "s" audible. We kept the original "gloom".
- **The new takes rush the line.** They finished about 1 s early and merged syllables: "plastic is still one word and not Plas Tic". `sylfit.py` retimes a take's syllables onto the original's vowel grid.
- **The "AC" diagnosis itself was wrong once.** The first "-ran-" fix moved the high note off the syllable it belonged to, because CTC places sung vowels late.

What made picking work was simple folders: `L16 OLD.mp3` and `L16 NEW a.mp3`, and I answered "L7 new, L29 old".

## The picture: rounds

- **"Slides that just put the lyrics there."** The first animatics placed static lyric cards over plates.
  - The overnight brief led to the kinetic type edition: every word on its sung frame, checked frame by frame.
  - Then the "alive" cut: each plate filmed by a camera that lands on the detail each word is about, and the press bumps on every kick.
- **No stretched letters.** Holding a note as "EEEEUROPE" read as misspelled noise ("you should have kept the text fixed and use motion design"). Held notes are now shown by motion: tracking, scale, the page moving.
- **Real references instead of illustrations.** Each line got a researched archival plate or document:
  - Bruegel's big fish;
  - Icarus;
  - Kempelen's Turk;
  - Holbein's island of Utopia;
  - Marey's 1885 train graph;
  - Teilhard's own figure for the Omega Point;
  - Mitchell's 1864 world map;
  - the Lumière films.

  Sources are in [REFERENCES.md](REFERENCES.md).
- **L12, Eurovision.** From a jury board, to a drawn Käärijä ("the main point shouldn't be that Sweden won but more that the system won the people"), to a photo of the Jury Final, and back to the drawn arena with his actual moves, studied from the broadcast. The final is the drawn arena in the video's palette, with no photograph.

  The four inks can't print neon green: blue over yellow is olive. So the print pass got a per-shot ink swap, and this shot prints its yellow plate in fluorescent green.
- **L4, the training loss drop.** First a departures board, then Marey's Paris–Lyon timetable, where the loss falls as a vertical line, a train that takes no time. Finally the lyric rides that line word by word.
- **L21, the Omega Point.** Straight lines converging on a circled Ω read "illuminati". We rebuilt it as Teilhard's own image, the meridians of a globe converging at the pole.
- **L19, basic income.**
  - A rumour crossing the Atlantic ("Finland pays everyone").
  - Then the EU citizens' initiative register page ("make it a lot more surface... real world reference").
  - Finally Holbein's Utopia and the idea's European road: Leuven 1516, Bruges 1526, Brussels 1848, Brussels 2026, then "still no place".
- **The outro.** The answer to "was it all for show?" in GPUs:
  - EU €10 bn for AI gigafactories, celebrated;
  - US big tech's ~$700 bn of 2026 AI capex, stacked three blocks per 16th note;
  - 1 : 70.
  - Then the Official Journal page, signed in blue ink and stamped in force. Article 50 names the model.
- **Things taken out:** the opening and closing tweet, the plague doctor, the prison bars, Covid, the Finland flags in the Eurovision crowd, the "people: 1st" stamp.

## Operations

- **The renders crashed the laptop 8 times.** A single-process render of the whole song ran out of memory, between ffmpeg, Chrome's GPU process and the desktop apps.
  - `safe-render.sh` now renders 15-second chunks in fresh processes, with a memory guard.
  - `snap_render.sh` renders from a frozen copy, so editing can continue.
  - Heavy audio jobs and renders take turns.
- **One edit silently deleted four finished scenes.** It replaced a text span between two markers. Scene edits now replace one method at a time, and the method list is compared with the last commit after every edit.
- **A scene that throws in one frame leaks canvas state into all later frames.** Stills don't show it. A perf pass over the whole cut runs before every full render.
- **Never overwrite a version.** Every render and every song build has a new name, so I could always compare.
