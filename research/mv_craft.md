# EUROBOOM: music-video craft research

Prepared 2026-09-29 for a ~2:30 satirical pop video about Europe and AI: papery JS animation, partly rotoscoped over AI-generated plates, maximalist kinetic type, limited palette, archival inserts, an illustrated pop lead with backup dancers, aimed at tech Twitter/X.

**Method.** Web sources are linked inline. I checked every K-pop timestamp frame by frame on 360p copies of the official uploads (accurate to ±0.5 s). Cut statistics come from ffmpeg scene-change detection (`select='gt(scene,0.18)'`). Flashes and strobe frames count as cuts, so the counts can be off by about ±15 %. Drop times come from measured RMS loudness. View counts were read with yt-dlp on 2026-09-29. The web-search quota ran out partway through, so anything I couldn't verify is either marked or left out.

---

## 1. K-pop: how the videos steer attention and hold it

### 1.1 Measured pacing (14 videos, 2016–2026)

| MV (year) · director | views | avg shot | 1st cut | cuts/10 s: first 30 s → whole MV | busiest 10 s (× own avg) | on screen in the busiest window |
|---|---|---|---|---|---|---|
| TWICE "TT" (2016) | 720 M | 1.9 s | 6.4 s | 2.3 → 5.2 | 3:41 (2.3×) | final chorus + costume inserts |
| BLACKPINK "DDU-DU DDU-DU" (2018) · Seo Hyun-seung | 2.41 B | 0.8 s | 8.3 s | 8.3 → 12.9 | 2:51 (2.7×) | final chorus, new neon kaleidoscope set |
| Stray Kids "God's Menu" (2020) | 578 M | 2.6 s | 0.25 s | 5.7 → 3.8 | 0:00 (3.5×) | cold-open montage |
| BTS "Dynamite" (2020) · Yong-seok Choi (Lumpens) | 2.14 B | 1.6 s | 8.0 s | 2.0 → 6.0 | 3:16 (2.3×) | final chorus, outdoor green field |
| LE SSERAFIM "ANTIFRAGILE" (2022) | 286 M | 1.0 s | 1.8 s | 6.0 → 9.7 | 3:06 (2.3×) | final chorus |
| NewJeans "Ditto" Side A (2022) · Shin Woo-seok | 66 M | 1.8 s | 5.0 s | 6.0 → 5.6 | 0:18 (2.1×) | camcorder montage of friends |
| NewJeans "Super Shy" (2023) · Shin Hee-won | 299 M | 1.1 s | 3.5 s | 6.3 → 9.3 | 1:34 (1.8×) | bus/street flash-mob chorus |
| ILLIT "Magnetic" (2024) | 356 M | 1.5 s | 1.5 s | 8.0 → 6.7 | 2:28 (2.1×) | final chorus |
| aespa "Supernova" (2024) · Ha Jung-hoon | 256 M | 1.2 s | 6.6 s | 11.0 → 8.5 | 0:26 (2.8×) | pre-chorus object inserts |
| aespa "Whiplash" (2024) · Meltmirror | 319 M | 0.7 s | 6.9 s | 12.0 → 14.8 | 0:57 (2.8×) | hook + text flashes |
| ROSÉ & Bruno Mars "APT." (2024) · Daniel Ramos, Bruno Mars | 2.69 B | 1.9 s | 5.9 s | 4.0 → 5.2 | 0:51 (1.9×) | "apateu" chant chorus |
| KATSEYE "Gnarly" (2025) · Cody Critcheloe | 235 M | 0.7 s | 5.1 s | 11.0 → 14.0 | 0:52 (2.4×) | chorus on green stage |
| BLACKPINK "JUMP" (2025) | 435 M | 5.5 s | 6.5 s | 2.7 → 1.8 | 0:27 (4.5×) | screaming-crowd / giant-mouth montage |
| BLACKPINK "GO" (2026) | 96 M | 0.75 s | 5.1 s | 7.3 → 13.3 | 1:46 (2.8×) | sci-fi pod/ocean montage |

What the numbers say:
- **In 12 of the 14 videos, the busiest 10 seconds run 1.8–2.8× the video's own average cut rate.** The outliers are God's Menu's cold open (3.5×) and JUMP's long takes (4.5×). That peak comes either on the first hook (Supernova, Whiplash, APT., Gnarly) or on the last chorus (TT, DDU-DU, Dynamite, ANTIFRAGILE, Magnetic). Cutting speeds up toward those points rather than holding flat.
- **Openings got faster.** In 2016–2020 the first 30 s were slower than the rest of the video (TT 2.3 vs 5.2; Dynamite 2.0 vs 6.0). In 2024–25 they match or beat the average (Magnetic 8.0 vs 6.7; Supernova 11.0 vs 8.5; Gnarly 11.0).
- **Energy comes either from cutting or from what's inside the frame.** Whiplash and Gnarly use ~0.7 s shots. APT. (1.9 s shots, one pink set) is the most-viewed video here, and its energy comes from graphics drawn over the footage. JUMP (5.5 s) gets its energy from CG crowds moving within long takes. For a JS animation, motion inside the frame costs less than cuts.

### 1.2 Devices: what each is, an example with timestamp, and why it works

1. **First 3 seconds: one legible, strange image or a countdown.**
   - *Gnarly* 0:00–0:05: a member's head is vacuum-packed in a pink supermarket meat tray with a barcode sticker. She lip-syncs inside it, a hand pokes the film at 0:03, and there's no cut for 5 s.
   - *"Golden"* (KPop Demon Hunters MV, dir. [Maggie Kang & Chris Appelhans](https://www.netflix.com/tudum/videos/kpop-demon-hunters-golden-music-video)) 0:00–0:16 opens on a phone showing "GOLDEN coming soon 00:00:00:15". Fans count down on their screens until "00:00:01" and then the song starts.
   - *Magnetic* 0:00–0:04 goes macro mouth/hand (1.5 s), then a wide bedroom, then a glowing star in a palm at 0:03. The concept is on screen within 3 s.
   - What to avoid: *Dynamite* spends 0:00–0:08 on a white label ident, and *ETA* opens on a "Shot on iPhone 14 Pro" card. That works on YouTube, where the viewer already chose the video, but it's fatal in a feed.
   - Why it works: in a feed, frame 0 acts as the poster. One absurd image works as thumbnail, meme and question all at once, and a countdown opens a loop the viewer wants closed.
2. **Centre-framed, direct-to-lens close-ups for whoever is singing.**
   - *Supernova* 1:30–1:38 cuts member by member through frontal close-ups.
   - *DDU-DU* 1:00–1:10 gives Rosé and then Jisoo centred single shots between set pieces.
   - VM Project's Jo Beomjin: "Priority is to bring out each individual idol's image" ([Dazed](https://www.dazeddigital.com/music/article/40602/1/how-to-make-an-iconic-k-pop-music-video)).
   - Why it works: fans track who sings which line, a face-to-lens line becomes its own clip, and on a phone the eye goes to the centre.
   - For us: the lead owns the centre on her lines; dancers frame her and never share it.
3. **Point choreography (the "killing part"), built to be copied in 3 s.**
   - *TT*'s crying-emoticon "TT" hands became a meme ([Wikipedia](https://en.wikipedia.org/wiki/TT_(song))).
   - *DDU-DU*'s finger-gun (1:18) "was not included in the initial choreography" ([Wikipedia](https://en.wikipedia.org/wiki/Ddu-Du_Ddu-Du)), so point moves can be added late, on the hook.
   - *Magnetic*'s Tap–Tilt–Pull finger/wrist move "anyone can mimic in three seconds" drove about 1 B TikTok views across ILLIT content ([Paysable](https://blog.paysable.com/illit-review/)).
   - *Whiplash*'s point move is shoulder isolations ([DIPE](https://www.dipe.co.kr/2308949)).
   - Industry view: a ~15 s hook "can make or break" a song ([Korea Herald, 2026-03-12](https://www.koreaherald.com/article/10692913)), and labels now release challenge clips before the song ([Korea Times, 2026-03-14](https://www.koreatimes.co.kr/entertainment/k-pop/20260314/time-it-takes-to-make-a-k-pop-hit-15-seconds)). The template goes back to Zico's "Any Song" (Jan 2020), where 37 % of the song's streams landed in the challenge window ([JoySauce](https://joysauce.com/any-song-gate-how-one-song-disrupted-the-fabric-of-k-pop-forever/)).
   - Why it works: hand and upper-body moves survive vertical crops and viewers sitting down, and re-performance is free distribution.
4. **Formation reveal on the drop, set up by a dip.**
   - *DDU-DU*: at 1:15–1:16 it cuts from Jisoo's umbrella set to the blue glass-box formation. Loudness dips from 1:17.2 to 1:18.6 and hits at 1:19.2 (measured), and the finger-gun lands at 1:18–1:19.
   - *Magnetic*: loudness dips from 0:34.4 to 0:36.6 and drops at 0:36.9. On the drop a desk of blue paper cranes bursts (0:37), the cranes float (0:39), and then comes the group heart-hands formation (0:41).
   - Rigend's Rima Yoon: "how we put their narrative into points in their choreography"; they "make the draft from the choreography videos" ([EnVi](https://envimedia.co/creative-spotlight-rigend-gets-in-depth-on-the-magic-of-music-videos/)).
   - Why it works: a 1.5–2 s quiet insert resets attention, and the eye gets a new layout exactly when the ear gets a new texture.
5. **Colour-blocked sets assigned to song sections.**
   - *TT* keeps a flat candy-red-curtain-on-green stage for choruses only (1:42–1:51, 2:33–2:36, 2:48–2:57); the verses are in a dim haunted house.
   - *DDU-DU* gives each member one world: Jennie's pink chessboard (0:21–0:33), Lisa's pink shop (0:39–0:45), Rosé's chapel (0:51–0:57). The chorus is a blue glass box (1:15–1:31), and the final chorus a neon kaleidoscope (2:51–3:24).
   - *Whiplash* is mostly set in a white cyclorama full of camera rigs. A full-frame red card at 2:13 switches to a red set for the dance break.
   - *Gnarly* moves white kitchen → red corridor (0:30) → green stage (0:44) → red carpet (1:54).
   - *APT.* uses one pink set for the whole song; its section changes come from graphics, not architecture.
   - Why it works: colour is a map of the song, and clipped fragments stay recognisable by colour alone.
6. **Insert cadence: 1–2 s object inserts clustered before hooks, as recurring motifs.**
   - *Supernova*'s busiest window (0:26–0:36) is punctuated by object inserts: a soccer ball (0:26), sneakers (0:28), a snarling dog (0:32).
   - *Magnetic* cuts to a phone notification (0:42.5) and a hand-drawn unicorn/moon sheet of paper (0:43).
   - *Gnarly*'s sandwich-making inserts (0:08, 0:42, 1:42, 1:52) pay off at the end: the slime "Gnarly" logo sits on the sandwich (2:16).
   - DIGIPEDI's house style is "quick cut editing, prop close-ups" ([The Seoul Story](https://theseoulstory.com/feature-k-pop-music-video-production-the-art-of-visuals/)).
   - Why it works: inserts act as the rhythm section, and motifs that recur can pay off at the end.
7. **Speed ramps and time manipulation just before the last chorus.**
   - *ANTIFRAGILE* 2:33–2:41: eye macro (2:34) → falling meteor (2:35.5) → slow-motion push through hanging debris to a member (2:37–2:41) → final chorus.
   - *Supernova* writes time into the plot ("Giselle's time-looping", [Wikipedia](https://en.wikipedia.org/wiki/Supernova_(Aespa_song))), which shows as motion-echo smears at 2:23.
   - Why it works: slowing time just before the payoff makes the payoff feel faster by contrast.
8. **Text and graphic overlays: sparse and graphic, never full karaoke.**
   - *APT.* (the densest example):
     - Handwritten white script writes on in sync with the vocal, but only for two verse lines: "I'm tryna kiss your lips for real!" (0:23–0:25) and "Come give me something I can feel" (0:29.5–0:31).
     - Cut-out sticker heads sit on lightning-bolt wallpaper (0:14, 2:24, 2:38).
     - A hand-scrawled "APT." multiplies over the silhouettes on each chant (1:25.5–1:28).
     - Cut-out paper eyes and doodled hearts are pasted onto Rosé's face (1:30.5).
     - Brush-lettered "HOLD ON" and "YEAH YEAH" appear, with animated lightning bolts around the silhouettes (1:44, 2:04–2:09).
     - Old-cartoon iris vignettes run through 1:10–1:32.
   - *Whiplash*: one huge "FLASH" (1:02); "ONE" builds to "ONE LOOK GIVE'EM" on white (1:07); tiny tracked caps "CAN'T TOUCH THAT" on a red card (2:13). Reviewers noted that "text flashes felt sophisticated and artistic" ([KpopReviewed](https://kpopreviewed.com/2024/10/26/whiplash-aespa/)).
   - *Golden* builds lyrics out of the world: "GONNA BE GOLDEN" spelled in lightsticks (1:19), "I'M DONE HIDING" on a news billboard (1:22.5), and "LIKE I'M BORN TO BE" as a label over a storm of fake fan tweets (1:25.5–1:28).
   - *TT*'s flat 2-D jack-o'-lantern graphic has "T"-shaped eyes that echo the "TT" gesture (2:39).
   - *ETA* keeps the iPhone camera interface on screen (0:06–0:15), so the interface becomes the frame.
   - *ANTIFRAGILE* sets up its plot with a supermarket TV showing a "NEWS LIVE — METEORITE SPOTTED!" chyron (0:10).
   - Why it works: type punctuates 1–3 lines per section and images carry the rest, which suits sound-off feeds.
9. **Chorus payoff: a new set, peak cut density and a callback.**
   - *DDU-DU* 2:51–3:24 opens a new kaleidoscope set, peaks at 35 cuts in 10 s, and brings back Jennie's mirror-ball tank (2:54).
   - *Dynamite* goes from interiors to an outdoor green field with colour ribbons (3:03–3:39).
   - *ANTIFRAGILE* ends with the group surviving the asteroid and dusting themselves off ([Wikipedia](https://en.wikipedia.org/wiki/Antifragile_(song))), so the joke resolves on the last chorus.
   - Why it works: this is the stretch that gets clipped most, and it rewards the viewers who stayed.
10. **More entry points: sides, parts and POV versions.**
    - *Hype Boy* shipped an intro plus four member versions ([videography](https://en.wikipedia.org/wiki/NewJeans_videography)).
    - *Ditto* shipped Side A and Side B, one for "hope" and one for "despair" ([Wikipedia](https://en.wikipedia.org/wiki/Ditto_(song))).
    - *Supernatural* shipped Part 1 and Part 2 as a 90s TV episode, with opening credits and a next-episode teaser ([NME](https://www.nme.com/news/music/newjeans-supernatural-music-video-3767492)) and 4:3 bookends ([Poptokki](https://www.poptokki.com/newjeans-goes-old-school-with-supernatural/)).
    - Why it works: every version is a new post with a new first frame, and lore invites theory threads.
11. **Aspect ratio as point of view.** *Ditto* Side A switches between pillarboxed 4:3 camcorder shots (the fan "Ban Hee-soo" filming) and 16:9 objective shots. The camcorder "portrayed Hee-soo's close relationship with NewJeans" (Shin Woo-seok, [Wikipedia](https://en.wikipedia.org/wiki/Ditto_(song))). Why it works: the frame tells you who is looking, which gives a free narrative layer.
12. **Show strangers doing the dance.**
    - *Super Shy* stages flash mobs in Lisbon's streets and markets ([Wikipedia](https://en.wikipedia.org/wiki/Super_Shy)).
    - Why it works: the video is both the tutorial and the permission to join in.
    - Europe note: K-pop keeps using Europe as a sunny backdrop: Super Shy (Lisbon), ETA (Barcelona, shot on an iPhone 14 Pro, [Wikipedia](https://en.wikipedia.org/wiki/ETA_(song))), and BTS "Swim" (Lisbon, dir. Tanu Muiño, 5 M views in its first hour, [Wikipedia](https://en.wikipedia.org/wiki/Swim_(BTS_song))). That makes it a mood board ripe for satire.
13. **Short, chorus-first songs.**
    - Recent hits: "Like Jennie" 2:04, "Not Cute Anymore" 2:12, "Overdrive" 2:40, "JUMP" 2:45 (Korea Times).
    - Critic Kim Heon-sik: songs now start by "jumping straight into the chorus from the very beginning" ([Korea Herald](https://www.koreaherald.com/article/10692913)).
    - A 2:30 video sits right in this range.
14. **Satire built into the set.**
    - *DDU-DU* 1:52–1:57: Jisoo stands in front of a mural of herself, surrounded by suited men filming on their phones.
    - *Gnarly* 1:30–1:31.5: a Hollywood sign reads "NOWHERELAND", followed by a crash zoom into it.
    - Why it works: gags on signs survive a screenshot.
15. **Polarise on taste, then deliver on the rewatch.** Gnarly's reaction on X and TikTok was "apocalyptic", and then "the more people listened to it, the more they got it", with a live TV performance flipping opinion ([W Magazine](https://www.wmagazine.com/culture/katseye-gnarly-controversy-reaction)). The fights were reach, and the craft paid off on the second look.

Director warnings worth keeping. Tigercave's Lee Gi-Baek: companies should be careful not "to exhaust the fans". Jo Beomjin: "When all the shots tell a narrative, it feels a little stiff" (both in [Dazed](https://www.dazeddigital.com/music/article/40602/1/how-to-make-an-iconic-k-pop-music-video)).

---

## 2. Rotoscope and drawing over live action

### 2.1 Precedents

**a-ha, "Take On Me" (1985, dir. Steve Barron). A Norwegian band broke America with a pencil.**
- **It flopped twice first.** The Oct 1984 version, promoted with a blue-background performance video, "sold just 300 copies worldwide" and peaked at UK #137. It was re-recorded with Tony Mansfield, then with Alan Tarney ([Sound on Sound](https://www.soundonsound.com/techniques/classic-tracks-ha-take-me); [Mental Floss](https://www.mentalfloss.com/article/641682/a-ha-take-on-me-music-video)).
- **Who paid for it.** Warner's Jeff Ayeroff remembered Michael Patterson's 1981 pencil-animated film *Commuter* and funded a ~$100k video (SOS).
- **How it was made.** The band footage took 2 days to shoot (Mental Floss), at Kim's café in Wandsworth and on a London sound stage ([Wikipedia](https://en.wikipedia.org/wiki/Take_On_Me)). Patterson and Candace Reckinger then rotoscoped "3,000 individual frames" over "16 long weeks" ([Barron via Yahoo](https://www.yahoo.com/entertainment/director-steve-barron-recalls-making-ahas-take-on-me-i-knew-we-were-on-to-something-very-good-190217280.html); Mental Floss says 2,000 sketches in four months).
- **Barron's rule.** He wanted a concept that justified animation, being "a real stickler... for having a motivation for what you were doing — as opposed to just doing it for show or for fashion". The seed idea was "an animated hand reaching out from the comic book into the real world" (Yahoo).
- **On screen (4K official upload):**
  - 0:00–0:36 is an all-pencil race comic on blue-grey paper.
  - At 1:12 a drawn hand reaches out of the page.
  - From 1:24 to 1:54 drawn and live-action figures share the frame.
  - At 3:09 the comic page is physically crumpled.
- **Release trick.** The video went to MTV and dance clubs "a full month before the single" reached stores and radio. The song went to US #1 and spent 23 weeks on the Hot 100 (SOS).
- **Awards and views.** It won six VMAs in 1986, hit 1 B YouTube views on 17 Feb 2020, and passed 2 B by Sept 2024 (Wikipedia).
- **Lesson.** The line between drawn and real is the plot, and the paper is a physical object in the story.

**Linklater, "Waking Life" (2001).** Shot on Mini DV for $2 M. Bob Sabiston's Rotoshop "creates blends between key frame vector shapes", and Linklater "employed a variety of artists, so the movie's feel continually changes" ([Wikipedia](https://en.wikipedia.org/wiki/Waking_Life)). Lesson: style drift is fine when the fiction allows it (here, a dream).

**"A Scanner Darkly" (2006): the cautionary tale.**
- Animation took 15–18 months, with 30 new artists trained from Oct 2004. The budget rose from $6.7 M to $8.7 M.
- In Jan 2005 the producer "changed the locks and seized their workstations" on Sabiston's core team ([Wikipedia](https://en.wikipedia.org/wiki/A_Scanner_Darkly_(film))).
- The work ran at about 500 person-hours per screen-minute ([Today](https://www.today.com/popculture/scanner-turns-live-action-animation-wbna13758165)).
- Lesson: with many hands, consistency has to come from a locked style bible and a small core team.

**Kanye West, "Heartless" (2008, dir. Hype Williams).**
- "65 animators in Hong Kong drawing over every cell". "After picture-lock we had 10 days" to deliver "over 3,000 frames" (Chomet). It's an homage to Ralph Bakshi's *American Pop* ([Wikipedia](https://en.wikipedia.org/wiki/Heartless_(Kanye_West_song))).
- On screen: flat colour fills with almost no linework, over nebula skies, a Warhol soup-can wall (1:33–1:42) and cartoon wallpaper (2:30–2:54).
- Lesson: posterised fills survive a brutal deadline and fit a limited palette, and pop-art backdrops work as archival inserts.

**Gorillaz.**
- *Feel Good Inc.* (2005, Jamie Hewlett & Pete Candeland, Passion Pictures): Hewlett drew the sketches and storyboards, and Passion animated them ([Gorillaz Wiki](https://gorillaz.fandom.com/wiki/Feel_Good_Inc._(Music_Video))).
- *Humility* (2018): 2-D roller-skates through real Venice Beach footage, rotoscoped by Trace VFX, with Jack Black on guitar ([Wikipedia](https://en.wikipedia.org/wiki/Humility_(song))).
- Lesson: an illustrated pop star holds up when the character design is fixed and the character acts against a real world.

**Daft Punk, "Interstella 5555" (2003).** Toei made it with Leiji Matsumoto supervising, for $4 M, between Oct 2000 and Apr 2003, with no dialogue. Four segments premiered as music videos on Toonami on 31 Aug 2001 ([Wikipedia](https://en.wikipedia.org/wiki/Interstella_5555:_The_5tory_of_the_5ecret_5tar_5ystem)). Lesson: a wordless story can be released one episode at a time.

### 2.2 AI in music visuals, 2022–2026, and how each was received

| Work (date) | What the AI did | Reception | Lesson |
|---|---|---|---|
| Kendrick Lamar "The Heart Part 5" (May 2022, Deep Voodoo) | Deepfaked faces (O.J., Kanye, Will Smith, Nipsey…), each performing a verse from that person's perspective | Praised; Grammy wins ([Wikipedia](https://en.wikipedia.org/wiki/The_Heart_Part_5)) | AI as the concept, not a shortcut |
| Corridor "Anime Rock, Paper, Scissors" (26 Feb 2023) | Stable Diffusion over filmed actors; trained on *Vampire Hunter D: Bloodlust* | Backlash: flicker, "inhuman blob" hands, scraping ([KYM](https://knowyourmeme.com/memes/events/corridor-digital-rock-paper-scissors-ai-anime-controversy)) | Real limited animation varies frame counts "at any moment"; "the appeal of anime is in human inconsistency and intuition" ([ANN](https://www.animenewsnetwork.com/feature/2023-03-15/no-you-cant-make-anime-with-ai/.195921)) |
| Linkin Park "Lost" (10 Feb 2023, Shibuya) | Kaiber AI plus a credited team of human animators, anime style ([Stash](https://www.stashmedia.tv/linkin-park-lost-music-video-by-shibuya/)) | Fans angry about the AI ([Nicole Ven](https://nicole-ven.medium.com/why-are-linkin-park-fans-furious-about-new-lost-video-ai-generated-b655300a78fa)), yet a VMA nomination ([Wikipedia](https://en.wikipedia.org/wiki/Lost_(Linkin_Park_song))) | Hybrid credits don't save a generic look |
| Washed Out "The Hardest Part" (May 2024, Paul Trillo) | Sora: ~700 generated clips, prompts "at least 1,000 words each" | "It says nothing, does nothing, is nothing" (Trevor Powers, [Rolling Stone](https://ca.rollingstone.com/en/music/washed-out-made-an-ai-music-video-the-backlash-was-swift/)) | A dreamy AI flow with no joke or claim reads as empty |
| aespa "Supernova" (May 2024) | AI animated facial expressions synced to lyrics inside a live-action MV ([Wikipedia](https://en.wikipedia.org/wiki/Supernova_(Aespa_song))) | Swept Song of the Year awards | Invisible, subordinate AI passes |
| Kalshi NBA Finals ad (Jun 2025, PJ Accetturo) | Veo 3: 300–400 generations → 15 usable clips; $2,000; 2 days | 3 M views on Kalshi's X in a week; tone "between internet memes and Grand Theft Auto" ([Yahoo/BI](https://www.yahoo.com/entertainment/articles/chaotic-kalshi-ad-during-nba-173937071.html), [NPR](https://www.npr.org/2025/06/23/nx-s1-5432712/ai-video-ad-kalshi-advertising-nba-finals)) | Tech Twitter rewards AI chaos that *is* the joke |
| McDonald's NL "It's the Most Terrible Time of the Year" (6 Dec 2025) | Fully AI-generated spot | Pulled after 3 days as "AI slop", "so cynical and unfun" ([Today](https://www.today.com/food/news/mcdonalds-removes-ai-generated-christmas-ad-social-media-backlash-rcna248668)) | Don't be cynical about something people love |
| Rolling Stones "In the Stars" (May 2026, Deep Voodoo) | De-aged faces over body doubles ([LittleThings](https://littlethings.com/entertainment/new-rolling-stones-video-uses-ai)) | "A mini-concert in the heart of the Uncanny Valley" ([Houston Chronicle](https://www.houstonchronicle.com/business/tech/article/rolling-stones-ai-backlash-22256571.php)); defended because "the deepfakes are depicting the artists themselves" ([Digital Camera World](https://www.digitalcameraworld.com/tech/artificial-intelligence/the-rolling-clones-im-critical-of-genai-but-deepfaked-music-video-of-jagger-and-co-hits-differently)) | Consent helps; photoreal faces still hit the uncanny valley |
| Shift Up "Wanna be in LOVE" (31 Jul 2026) | Most scenes AI-generated | "Uncanny, stilted… movements, expressions and transitions", "AI slop"; the CEO's "more than a year" of artist work didn't help ([Aju Press](https://www.ajupress.com/view/20260803150638274)) | Motion quality is what gets judged |
| Tyla "That Girl" (late Jul 2026, Biuro) | AI-assisted animation | Animator Kat Blaque spotted a wrong hand pose and a "floating tiger face"; the studio cited "over 150 hours of compositing" but didn't deny AI ([Blaque in the City](https://blaqueinthecity.com/2026/07/29/yes-tylas-team-used-ai/)) | Getting caught is worse than disclosing up front |

A backdrop to all of this was the March 2025 "Ghibli" wave that followed GPT-4o image generation. Miyazaki's "insult to life itself" resurfaced, and the White House's Ghibli-style post caused "a major backlash" ([Forbes](https://www.forbes.com/sites/danidiplacido/2025/03/27/the-ai-generated-studio-ghibli-trend-explained/), [ABC](https://www.abc.net.au/news/2025-04-03/the-controversial-chatgpt-studio-ghibli-trend-explained/105125570)).

### 2.3 What made the good ones work
1. **The technique is the idea.** Take On Me's hand through the page and Heart Part 5's faces-as-verses both make the method the concept.
2. **Real bodies supply the motion; drawing supplies the style.** Rotoscoping takes care of motion. Deliberately varied timing (on 1s/2s/3s, with holds on accents) and small inconsistencies make it read as human (ANN).
3. **Materials you can see.** Pencil boil, a crumpled page (Take On Me 3:09) and pasted paper eyes (APT. 1:30.5) all show the work.
4. **Irony you point at yourself, with consent.** Kendrick, the Stones and Macron's self-deepfake montage (§4) all use their own faces.
5. **A small core team and a locked bible.** A Scanner Darkly shows what happens without them.

### 2.4 Backlash patterns to avoid
- **Borrowing a living studio's house style** (the Ghibli wave; Corridor's *Vampire Hunter D* training). Build the look from print processes (risograph, newsprint, photocopy), not from a studio.
- **AI tells:** hands, floating parts, faces drifting between frames (Corridor, Tyla). Redraw every hero frame, hold frames on accents, and never let raw plate texture show through.
- **Stilted motion and transitions** (Shift Up). Rotoscope real dancers for the performance, and keep AI plates for backgrounds and fake-archival material.
- **Hiding the AI** (Tyla). State the pipeline on day one, e.g. "AI plates, every frame redrawn by hand", and make the process part of the content (show the before/after).
- **Cynicism aimed at the audience's joy** (McDonald's NL). Satirise institutions, not what fans love.
- **Saying nothing** (Washed Out). Every AI plate has to carry a joke, such as fake EU press footage whose absurd details are the gag.
- **Photoreal deepfakes of real politicians.** Draw them in the caricature tradition instead. The drawing announces that it's satire.

---

## 3. Typographic and kinetic-lyric videos that are genuinely great

- **Bob Dylan, "Subterranean Homesick Blues" (1965, D. A. Pennebaker, *Dont Look Back*).**
  - Donovan, Allen Ginsberg, Bob Neuwirth and Dylan wrote the cue cards.
  - The card can argue with the lyric: when the song says "eleven dollar bills", the card says "20 dollar bills".
  - Shot in an alley by the Savoy Hotel, with Ginsberg chatting in the background. INXS ("Mediate", 1987) and Weird Al ("Bob", 2003) later homaged it ([Wikipedia](https://en.wikipedia.org/wiki/Subterranean_Homesick_Blues)).
- **The Saul Bass line.**
  - Bass aimed for "a simple, visual phrase that tells you what the picture is about and evokes the essence of the story".
  - Examples: *The Man with the Golden Arm*'s white-on-black paper cut-out arm; *Anatomy of a Murder*'s body cut into seven pieces; *North by Northwest*'s credits racing along a skyscraper ([Wikipedia](https://en.wikipedia.org/wiki/Saul_Bass)). *North by Northwest* is recognised as the first feature to use kinetic type extensively ([Wikipedia](https://en.wikipedia.org/wiki/Kinetic_typography)).
  - Bass credited Kon Ichikawa's *Tokyo Olympiad* as an influence on his *Grand Prix* titles.
  - Ichikawa's *Inugami Family* (1976) credits bent giant Mincho characters at right angles along the frame edge. Hideaki Anno homaged that in Evangelion's subtitles and credits, set in Fontworks' Matisse-EB, which fans call the "Eva font" ([ja.wikipedia: 市川崑](https://ja.wikipedia.org/wiki/%E5%B8%82%E5%B7%9D%E5%B4%91), [マティス](https://ja.wikipedia.org/wiki/%E3%83%9E%E3%83%86%E3%82%A3%E3%82%B9_(%E6%9B%B8%E4%BD%93))).
  - The chain runs Bass ↔ Ichikawa → Anno → today's Eva-card edits.
- **Prince, "Sign o' the Times" (1987).** Bill Konersman was hired "based on his graphic design background" ([Wikipedia](https://en.wikipedia.org/wiki/Sign_o%27_the_Times_(song))). The lyrics "take turns shrinking away, cycling around a four-, then two-window square, and sliding by the camera" over a background that "glimmers pink, blue, purple, and yellow to the music" ([People's Graphic Design Archive](https://peoplesgdarchive.org/item/8843/prince-sign-o-the-times-music-video)). With the artist absent, the type is the performer and gets its own choreography.
- **Gondry, mapping visuals to instruments.**
  - Daft Punk's "Around the World" (1997): robots = vocal, athletes = bass, swimmers = keyboard, skeletons = guitar, mummies = drum machine ([Wikipedia](https://en.wikipedia.org/wiki/Around_the_World_(Daft_Punk_song))).
  - The Chemical Brothers' "Star Guitar" (2002) was shot from a train on 10 passes between Nîmes and Valence and plotted on graph paper. Gondry: "we would find elements we would repeat that matched with the instrument themselves, like the drum with the houses or the other train passing by" ([Wikipedia](https://en.wikipedia.org/wiki/Star_Guitar)).
- **OK Go, "Love" (2025).** One 4-minute take with 29 robot arms and mirrors in a Budapest station, no green screen, got on take 37 ([Creative Boom](https://www.creativeboom.com/inspiration/how-grammy-winning-rock-band-ok-go-used-robots-to-make-their-latest-music-video-to-date/)). A real constraint becomes the spectacle.
- **The 1975, "Love It If We Made It" (2018, Adam Powell).** Neon silhouettes of the band play against news footage, with the lyrics at the top of the frame. The song quotes the Trump tweet "Thank you Kanye, very cool!" verbatim, and the end credits list real movements ([Wikipedia](https://en.wikipedia.org/wiki/Love_It_If_We_Made_It)). Verbatim quotation is the satire: the source is the joke.
- **Cautionary: Kanye West, "All of the Lights" (2011).** Gaspar Noé said Hype Williams "copied all the typography of my titles" from *Enter the Void*, whose flashing block letters on black were designed by Tom Kan ([XXL](https://www.xxlmag.com/kanye-west-and-director-hype-williams-accused-of-plagiarizing-all-of-the-lights/)). Homage a type system openly and transform it; don't lift a living designer's work.
- **2020s: type designed into the world.**
  - *Dynamite* paints its title on objects: "DYNAMITE" on an ice-cream truck (1:27), the letters again on a wall (1:54), and a giant "DISCO" sign (1:57).
  - *DDU-DU* turns 3-D pink "BLACKPINK" letters into architecture (1:34–1:48).
  - *APT.*, *Whiplash* and *Golden* are covered in §1.2 #8.
  - Charli XCX's *brat* (2024): Brent David Freaney spent five months and looked at about 500 greens. He chose Arial for its non-"precious" feel and stretched it to "give it a personality", placed so it's "neither small and tasteful nor large and loud". A "brat generator" let anyone make their own, and Kamala HQ adopted it on 22 Jul 2024 ([Wikipedia](https://en.wikipedia.org/wiki/Brat_(album))).
  - Chappell Roan's "HOT TO GO!" spells the title with arms, "like the 'Y.M.C.A.'", and festival crowds do it en masse ([Wikipedia](https://en.wikipedia.org/wiki/Hot_to_Go!)). Type as choreography.

**Rules for big type that feels designed rather than karaoke:**
1. **Budget your lines.** Set 1–3 lines per section, never the whole lyric (APT. sets two verse lines; Whiplash sets hook words only).
2. **Type has two jobs only:** it's either an object in the world (truck, sign, lightsticks, billboard, TV chyron) or a full-frame card. It never floats over the action like subtitles.
3. **Two sync rules:** writing-on follows syllables (APT. 0:23), while card cuts and word builds follow downbeats (Whiplash 1:07).
4. **Extreme scale contrast.** One giant word ("FLASH") next to tiny tracked caps ("CAN'T TOUCH THAT").
5. **A colour card switches sections** (Whiplash's red card leads into the red set).
6. **Let the card contradict the singer** (Dylan's "20 dollar bills"). For satire, the card is the fact-check.
7. **One type system with a fixed grammar** (Matisse-EB with the L-bend; brat's stretched Arial). A system can be memed; an effect can't.
8. **Metaphor over transcription.** Bass's "simple, visual phrase", e.g. the golden arm as a paper cut-out.
9. **Give each layer a stem** (Gondry). For example: type = vocal, dancers = drums, archival flashes = synth stabs.
10. **Leave one designed wrongness in:** brat's awkward size, APT.'s scribbles. Perfect alignment looks like a lyric-video template.

---

## 4. Internet-brutalism and meme collage that work on X (2025–26)

- **The mood cycle.**
  - "It's so over / we're so back" is the "upturn and downturn" cycle tech Twitter runs on. It was established on Twitter by April 2022 (@shamshi_adad), and AI-themed variants arrived in 2023 ([KYM](https://knowyourmeme.com/memes/its-so-over-were-so-back)).
  - Europe's 2025 "so back" material:
    - Macron posted "a compilation of AI-generated deepfake video clips of himself on Instagram" to launch the Paris AI Action Summit (9 Feb 2025).
    - Politico's headline: "'Plug, baby, plug': Macron pushes for French nuclear-powered AI" (10 Feb 2025).
    - Nearly €110 bn in private AI pledges for France, and the Commission's €200 bn InvestAI with four AI gigafactories ([Wikipedia](https://en.wikipedia.org/wiki/AI_Action_Summit_2025)).
  - "So over" material comes from regulation objects, e.g. tethered bottle caps, mandatory in the EU from July 2024 ([Wikipedia](https://en.wikipedia.org/wiki/Tethered_cap)).
  - *Couldn't verify:* specific viral "Europe is so back" posts; the search quota ran out.
  - For us: structure the song as the over/back swing, with one palette per state.
- **Eurovision is the proven lane for Euro-pop satire.**
  - Joost Klein's "Europapa" (NL 2024) is "retro happy hardcore" about open borders and his late father. It was the most-streamed ESC 2024 entry on Spotify and YouTube ([Wikipedia](https://en.wikipedia.org/wiki/Europapa)).
  - Tommy Cash's "Espresso Macchiato" (EE 2025) is a macaronic satire of Italian stereotypes. Lega politicians demanded its exclusion; it placed 3rd with 356 points ([Wikipedia](https://en.wikipedia.org/wiki/Espresso_Macchiato_(song))).
  - Lesson: stereotype satire works when the stereotype gets affection, and the complaints become press.
- **Italian brainrot (Jan 2025 onward).**
  - The formula: AI images of hybrid creatures, a synthetic Italian TTS voice, and "-ini/-ello" names. The first viral one was Tralalero Tralala, a three-legged shark in sneakers ([Wikipedia](https://en.wikipedia.org/wiki/Italian_brainrot)).
  - Then brands piled in: trading cards, and in 2026 Fortnite skins, with Ballerina Cappuccina "the lowest-rated skin in the game".
  - Lesson: it's a European, AI-native meme grammar. Cite it as a 1–2 s cameo, but don't build on it; it's already saturated with brands.
- **Evangelion title cards.** White Matisse-EB on black, bent into L-shapes, descended from Ichikawa (§3). Fontworks sold Matisse-EB as the licensed "Evangelion official font" until July 2020 (ja.wikipedia), which shows how much fans wanted the exact look. Use it for chapter cards (e.g. "EPISODE 3: THE AI ACT"), but draw your own letterforms in the same grammar (see the Noé lesson in §3).
- **Corecore.** TikTok collages of "seemingly unrelated clips" set to "emotionally rousing, somber, or ambient music". #corecore passed 664 M views by Feb 2023 ([Wikipedia](https://en.wikipedia.org/wiki/Corecore)). The juxtaposition is the argument, so each archival clip has to read in under 1 s. Cut on meaning, e.g. the word "regulate" lands on a parliament vote, "innovate" on a rocket.
- **Interface as frame.** ETA's iPhone camera UI and Ditto's camcorder REC framing (§1.2) show how audiences read native interfaces instantly. Obvious props for Europe × AI: cookie banners, "not available in your region" screens, consent dialogs *(my suggestion, not a documented trend)*.

**How pros use these without looking cheap:**
1. **Lock the system first, then be messy inside it.** APT. uses one pink set plus black stickers and brush lettering. brat uses one green and one font, chosen after testing about 500 shades.
2. **Redraw or relight found material into your own palette.** Golden's tweet storm is rendered in the film's own type and light, with a lyric label on top to keep hierarchy (1:25.5–1:28).
3. **Quote real artefacts verbatim.** The 1975 used a Trump tweet; ANTIFRAGILE used a fake news chyron. Real regulation text, real press-release phrasing and real founder tweets hit harder than invented ones.
4. **Parody a format with full production value.** NewJeans' "Supernatural" (a 90s TV episode) and Doechii's "Denial Is a River" (a "faux 90s sitcom", Creative Review's [2025 list](https://www.creativereview.co.uk/music-videos-of-the-year-2025/)).
5. **Aim the irony at yourself.** Macron deepfaking himself read as game, where brands mocking their customers (McDonald's NL) read as cynical.
6. **Arrive early or twist it.** Once brands show up, the format is dead (brainrot's lowest-rated Fortnite skin).
7. **Ship the template.** The brat generator led to Kamala HQ. A JS video can ship its own card generator.

---

## 5. X video performance

### 5.1 What the ranker actually rewards

Source: [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm), `home-mixer/params/param.rs` (README updated 18 Sep 2026). The weights multiply *predicted probabilities*, not raw counts.

| Action | Weight | Action | Weight |
|---|---|---|---|
| share via copy link | **20** | repost | 1 |
| reply (+15 if mutual follow) | **5** | like | 0.5 |
| quote | **5** | click / open link / video open | 0.3 / 0.2 / 0.07 |
| share via DM | 5 | dwell | 0.05 |
| follow author | 4 | video quality view (VQV) | **0.0** (only computed for videos > 10 s) |
| share | 2 | not interested / mute / block / report | −47.5 / −58.8 / −31.2 / −234 |

Other published settings ([vm-ranker/params.rs](https://github.com/xai-org/x-algorithm/blob/main/vm-ranker/params.rs)):
- Out-of-network posts are multiplied by 0.75.
- Each additional post by the same author decays by 0.5, down to a floor of 0.25.
- The code says "directly navigating to a post (i.e., coordinating via groupchat) has no ranking impact". Only engagement on posts served in Home counts.
- For comparison, the 2023 ranker weighted reply 13.5, reply-engaged-by-author 75, like 0.5 and video 50 % playback 0.005 ([twitter/the-algorithm-ml](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md)).

What that means for us:
- **Views earn nothing; being quoted, replied to and link-copied earns rank.** Design for the "send this to the group chat" reflex (copy link = 20).
- **Upload natively.** Link opens score 0.2. Put the YouTube link in the first reply.
- **Space out the cut-downs** to beat the 0.5 author decay, and seed through collaborators' accounts, where the post is in-network for their followers and escapes the 0.75 penalty.
- **Aim the satire at institutions** (Brussels, Big AI, the hype cycle), not at a group of viewers. Mass "not interested" and mute signals (−47.5 / −58.8) outweigh quote-dunks.

### 5.2 Upload specs

Source: [docs.x.com](https://docs.x.com/x-api/media/quickstart/best-practices), modified 2 Sep 2026.
- Post video: 20 min / 8 GB by default; 125 min / 16 GB with Premium. DM video: 140 s by default.
- Recommended aspect ratio 16:9 (landscape or portrait) or 1:1; anything from 1:3 to 3:1 is allowed.
- Max 60 fps; H.264 High profile; AAC-LC audio; at least 5,000 kbps video.
- A 2:30 video posts from any account. The 140 s cap only bites if people forward the file itself in DMs.

### 5.3 First frame and first second
- **Frame 0 is the poster.** Use a readable card or one absurd image (Gnarly's meat tray; Golden's countdown). No ident, no black, no sponsor card (Dynamite's 8-s logo; ETA's card).
- **Show the chorus image within 3 s,** following K-pop's own shift to chorus-first songs (Korea Herald).
- **If the first second is type, keep it to 3–5 words.**

### 5.4 Sound-off, aspect ratio, length
- **Sound-off.** Assume the timeline starts muted.
  - Digiday: 85 % of Facebook video views were silent, and publishers "standardized on text-heavy videos with captions" ([Digiday, 2016](https://digiday.com/media/silent-world-facebook-video/)).
  - Burn the type into the render. Test the whole video muted on a phone: every joke that needs audio needs a type or image twin.
- **Aspect ratio.** Master in 16:9 (YouTube plus the X hero post; the P(doom) reference renders 1920×1080). Keep every load-bearing word and the lead's face inside a centred 1:1 safe zone, so 1:1, 4:5 and 9:16 cut-downs and quote-crops still read.
- **Length.**
  - Hero post: the full 2:30. VQV is weighted 0, but dwell time is scored (`cont_dwell_time` 0.004, `cont_click_dwell_time` 0.4 in param.rs), so dense, rewatchable frames pay.
  - Cut-downs: 12–20 s, which clears the 10 s VQV gate and matches the ~15 s killing-part logic.

### 5.5 What makes people quote-post a video
- **Most quotes are one word.** When Twitter forced a quote prompt in Oct–Dec 2020, "45 percent of them included single-word affirmations", 70 % were under 25 characters, and total sharing fell 20 % ([Engadget](https://www.engadget.com/twitter-ends-quote-tweet-experiment-retweets-003202686.html)). Hand people a chant word they can quote (like "APT." or "Europapa"), and never add friction.
- **Out-group and moral language drive shares.**
  - Each out-group term raised the odds of a share by 67 %, and out-group posts were shared about 2× as often ([Rathje et al., PNAS 2021](https://doi.org/10.1073/pnas.2024292118)).
  - Each moral-emotional word raised diffusion 20 %, mostly within groups ([Brady et al., PNAS 2017](https://doi.org/10.1073/pnas.1618923114)).
  - So name the institutions and cast tech Twitter as the in-group.
- **High arousal spreads.** "Awe" and "anger or anxiety" spread; sadness doesn't ([Berger & Milkman, JMR 2012](https://doi.org/10.1509/jmr.10.0353)). Aim for awe at the craft, mock anxiety about AI doom, and plenty of laughs.
- **Freeze-frame bait.** Dense fine print that rewards pausing (Golden's tweet storm; the real tweets in The 1975). Fake EU directive pages with jokes in the footnotes get screenshotted and quoted.
- **Polarise on taste, never on identity** (Gnarly, §1.2 #15).
- **A remix hook.** A web card generator in the video's type system (the brat precedent).

---

## 20 stealable devices
1. Countdown cold open ("00:00:00:15" → "00:00:01" → drop). *Golden MV, 0:00–0:16*
2. One absurd, thumbnail-ready image held for 5 s with no cut. *Gnarly, face in a meat tray, 0:00–0:05*
3. State the concept in a 3-s macro (a star glowing in a palm). *Magnetic, 0:03*
4. A paper burst on the drop (paper cranes explode, then float). *Magnetic, 0:37–0:40*
5. A ~1.5 s dip, then the point move lands exactly on the drop. *DDU-DU, dip 1:17.2–1:18.6, finger-gun 1:18–1:19*
6. A flat colour-blocked stage reserved for choruses only. *TT, red-on-green stage 1:42, 2:33, 2:48*
7. A full-frame colour card with tiny tracked caps that switches the set. *Whiplash, "CAN'T TOUCH THAT", 2:13*
8. Build the hook word by word, plus one giant single word. *Whiplash, "ONE" → "ONE LOOK GIVE'EM" 1:07; "FLASH" 1:02*
9. Handwritten write-on synced to syllables, for 2 lines only. *APT., 0:23 and 0:30*
10. Cut-out paper eyes and doodles pasted onto a live face. *APT., 1:30.5*
11. Silhouette + brush lettering + animated lightning bolts drawn around the performers. *APT., 1:44, 2:04–2:09*
12. The title written into the set (truck, sign, 3-D letters). *Dynamite 1:27 and 1:57; DDU-DU 1:34*
13. A fake news chyron as the plot's inciting incident. *ANTIFRAGILE, "METEORITE SPOTTED!", 0:10*
14. A tweet-storm collage under a lyric label. *Golden, "LIKE I'M BORN TO BE", 1:25.5*
15. Crowd lights spell out the lyric. *Golden, lightstick "GONNA BE GOLDEN", 1:19*
16. A parody landmark sign with a crash zoom. *Gnarly, "NOWHERELAND", 1:30*
17. A drawn hand reaching out of the page into the live world; the page crumpled at the end. *Take On Me, 1:12 and 3:09*
18. Assign every visual layer to one instrument. *Gondry, Around the World and Star Guitar*
19. A cue card that contradicts the lyric: the fact-check gag. *Dylan, "20 dollar bills" vs the sung "eleven"*
20. Ship a template generator so the audience posts your style. *brat generator → Kamala HQ, Jul 2024*
