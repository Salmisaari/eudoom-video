# Generation stack for the ~150 s music video (research, 2026-09-29)

Scope: the endpoints, parameters, limits and prices needed to produce ~40 generated clips of 4–10 s and ~150 images for a ~150 s music video with an illustrated singing character in a printed look. Everything was read from live pages on 2026-09-29. No paid API was called and no key was used.

How it was checked:
- **fal endpoints:** schemas come from the public OpenAPI files (`https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=<id>`). Prices are quoted from each model's `https://fal.ai/models/<id>/llms.txt`. The endpoint list comes from fal's public catalogue search (`https://api.fal.ai/v1/models?q=...`).
- **Conflicts:** where a fal README disagrees with the OpenAPI schema, the schema is treated as the truth, because it is what the API validates against. Each such conflict is flagged.
- **[unconfirmed]:** marks anything not stated on an official vendor or fal page.

---

## 1. Seedance on fal

Seedance 2.5 is live on fal. The global "Dreamina" endpoints were added on 2026-07-20, the US-hosted copies on 2026-09-19 and the draft-completion endpoint on 2026-09-25. Seedance 2.0, 1.5 Pro and 1.0 Pro are still active. The 1.0 Lite endpoints are deprecated, and requests to 1.0 Lite reference-to-video are rerouted to Grok Imagine Video.

### 1.1 Endpoint matrix

| Endpoint ID | Mode | Duration | Resolutions | FPS | Aspect ratios | Reference inputs | Audio in | Own audio | Seed input | Price (quoted from fal) |
|---|---|---|---|---|---|---|---|---|---|---|
| `bytedance/seedance-2.5/text-to-video` | T2V | `auto`, `"4"`–`"30"` | 480p, 720p, 1080p | 24 fixed¹ | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | none | no | yes (`generate_audio`, default true, same price) | **no** (only returned in the output) | **$0.2205/s** 480p, **$0.4730/s** 720p, **$1.164/s** 1080p. Token rate $0.0214 per 1k tokens (≤720p) and $0.0234 per 1k (1080p) |
| `bytedance/seedance-2.5/image-to-video` | first frame (+ optional last frame) | 4–30 s / auto | 480p, 720p, 1080p | 24 | always `auto` (taken from the image) | `image_url` (required), `end_image_url` | no | yes | **no** | same as T2V. Input images are not billed |
| `bytedance/seedance-2.5/reference-to-video` | references, editing, extension (`task`) | 4–30 s / auto (editing forces auto) | 480p, 720p, 1080p | 24 | auto + 6 ratios | ≤30 images, ≤10 videos, ≤10 audio; ≤50 files in total | **yes** (`audio_urls`) | yes | **yes** | same per-second price. Input-video seconds are billed too, and the total is ×0.6 when any video reference is present (≈$0.2838/s at 720p). Image and audio references are free |
| `bytedance/seedance-2.5/draft/complete` | re-renders a draft at 1080p | same as the draft | 1080p only | 24 | inherited | `draft_id` (valid 7 days, same account) | – | – | – | **$1.164/s** ($0.0234 per 1k tokens)² |
| `bytedance/seedance-2.5/us/{text-to-video,image-to-video,reference-to-video}` | US-hosted copies | 4–30 s | 480p, 720p, 1080p | 24 | same | same | r2v only | yes | r2v only | **$0.2646/s** 480p, **$0.5676/s** 720p, **$1.396/s** 1080p. No `draft` parameter. Not needed for this project |
| `bytedance/seedance-2.0/text-to-video` | T2V | `auto`, `"4"`–`"15"` | 480p, 720p, 1080p, 4k | 24¹ | auto + 6 ratios | none | no | yes | no³ | **$0.3034/s** 720p, **$0.682/s** 1080p ($0.014 per 1k tokens up to 1080p; $0.008 per 1k at 4K, ≈$1.56/s at 16:9, computed) |
| `bytedance/seedance-2.0/image-to-video` | first + last frame | 4–15 s | 480p–4k | 24 | auto + 6 ratios | `image_url`, `end_image_url` | no | yes | no³ | same as 2.0 T2V |
| `bytedance/seedance-2.0/reference-to-video` | references | 4–15 s | 480p–4k | 24 | auto + 6 ratios | ≤9 images, ≤3 videos (2–15 s combined, <50 MB, ~480p–720p each), ≤3 audio (≤15 s combined, ≤15 MB each, **needs at least 1 image or video**); ≤12 files in total | yes | yes | no³ | same per second; ×0.6 with video inputs (≈$0.1814/s at 720p) |
| `bytedance/seedance-2.0/fast/{t2v,i2v,r2v}` | fast tier | 4–15 s | 480p, 720p | 24 | same | same as 2.0 | r2v | yes | no | **$0.2419/s** 720p ($0.0112 per 1k tokens) |
| `bytedance/seedance-2.0/mini/{t2v,i2v,r2v}` | cheapest tier (2026-06-23) | 4–15 s | 480p, 720p | 24 | same | same as 2.0 | r2v | yes | no | **$0.0721/s** 480p, **$0.1547/s** 720p ($0.007 per 1k tokens) |
| `bytedance/seedance-2.0/us/{t2v,i2v,r2v}` | US-hosted | 4–15 s | 480p, 720p | 24 | same | same as 2.0 | r2v | yes | no | $0.1731/s 480p, $0.37/s 720p |
| `fal-ai/bytedance/seedance/v1.5/pro/{text-to-video,image-to-video}` | T2V / I2V + end frame | `"4"`–`"12"` | 480p, 720p, 1080p | [unconfirmed] | 21:9…9:16, auto (default 16:9) | `image_url`, `end_image_url` | no | yes (`generate_audio`) | **yes** (`seed`, -1 = random) | 720p 5 s with audio ≈ **$0.26**; $2.4 per 1M tokens with audio, $1.2 per 1M without |
| `fal-ai/bytedance/seedance/v1/pro/{text-to-video,image-to-video}` | T2V / I2V + end frame | `"2"`–`"12"`, or `num_frames` | 480p, 720p, 1080p (default 1080p) | [unconfirmed] | same | `image_url`, `end_image_url` | no | no | yes | 1080p 5 s ≈ **$0.62**; $2.5 per 1M tokens |
| `fal-ai/bytedance/seedance/v1/pro/fast/{text-to-video,image-to-video}` | fast | 2–12 s | 480p–1080p | [unconfirmed] | same | `image_url` (no end frame) | no | no | yes | 1080p 5 s ≈ **$0.243**; $1.0 per 1M tokens |

¹ fal's token formula is `tokens = height × width × duration × 24 / 1024`, and fal's Seedance 2.5 vs LTX-2.5 comparison says "Seedance 2.5 outputs a fixed 24" fps (https://fal.ai/learn/devs/seedance-2-5-vs-ltx-2-5-pro). The 24 fps figure for 2.0 comes only from the same formula [unconfirmed as an explicit spec].
² The `draft/complete` llms.txt gives $0.0234 per 1k tokens (≈$1.164/s). fal's multi-angle article says "$0.0214 per 1,000 tokens". Budget with the higher, official-endpoint figure.
³ The fal READMEs for 2.0 reference-to-video, 2.0 image-to-video and 2.5 image-to-video list a `seed` parameter, but the OpenAPI schemas do not. Among 2.x endpoints only `seedance-2.5/reference-to-video` accepts `seed` (checked in the schemas on 2026-09-29). fal notes that "results may still vary slightly even with the same seed."

Price per clip, from fal's per-second figures at 16:9:

| Endpoint | 5 s | 10 s |
|---|---|---|
| Seedance 2.5, 480p | $1.10 | $2.21 |
| Seedance 2.5, 720p | $2.37 | $4.73 |
| Seedance 2.5, 1080p | $5.82 | $11.64 |
| Seedance 2.0, 720p | $1.52 | $3.03 |
| Seedance 2.0, 1080p | $3.41 | $6.82 |
| Seedance 2.0 fast, 720p | $1.21 | $2.42 |
| Seedance 2.0 mini, 480p | $0.36 | $0.72 |
| Seedance 2.0 mini, 720p | $0.77 | $1.55 |

These per-second figures are fal's approximations. The token formula is authoritative: Seedance 2.5 at exactly 1280×720 costs $0.462/s (fal's own example: "5s at 720p … ~$2.31"). The budget uses the higher figures.

Dimensions for 16:9 per fal's README: 480p = 864×496, 720p = 1280×720. The 1080p dimensions are not in the README; the 1080p per-second price implies about 2.12 MP per frame [unconfirmed].

1080p on Seedance 2.5 is inconsistently documented:
- The schemas and llms.txt pricing (updated 2026-09-25) include 1080p. fal's 2.5 vs LTX-2.5 (2026-08-17) and 2.5 vs H3 (2026-08-19) comparisons ran it at 1080p.
- The Seedance 2.5 landing page (last updated 2026-08-12) and the 2.5 vs 2.0 article (2026-08-13) still say "up to 720p".
- Treat native 1080p as available but young, and keep 720p + upscale as the fallback (6.6).

### 1.2 Parameter schema: `bytedance/seedance-2.5/reference-to-video` (from OpenAPI)

```
prompt          string | null     "Refer to inputs as @Image1, @Video1, @Audio1" (the README uses [Image1]; the schema uses @Image1)
task            enum  "reference" | "editing" | "extension"   default "reference"
                (editing forces aspect_ratio and duration to auto; extension forces aspect_ratio to auto)
image_urls      list<string>  ≤30; JPG/PNG/WebP/BMP/TIFF/GIF/HEIC/HEIF; ≤30 MB each
video_urls      list<string>  ≤10; MP4/MOV; each 1.8–30.2 s, ≤200 MB; combined ≤30.2 s;
                300–6000 px per side; aspect 0.4–2.5; 24–60 fps
audio_urls      list<string>  ≤10; MP3/WAV; each 1.8–30.2 s, ≤15 MB; combined ≤30.2 s
                (files across all modalities ≤50)
resolution      enum "480p" | "720p" | "1080p"          default "720p"
draft           boolean  default false  -> 480p preview + draft_id (complete at 1080p within 7 days)
duration        enum "auto" | "4" … "30"  (string!)     default "auto"
aspect_ratio    enum "auto" | "21:9" | "16:9" | "4:3" | "1:1" | "3:4" | "9:16"   default "auto"
generate_audio  boolean  default true  (same price either way)
bitrate_mode    enum "standard" | "high"                default "standard"
codec           enum "auto" | "H264" | "H265"           default "auto"
seed            integer | null
end_user_id     string | null
-> output: { video: File{url, content_type, file_name, file_size}, seed: int, draft_id: string|null }
```

The other 2.5 schemas differ as follows:
- **`image-to-video`:** `image_url` (required), `end_image_url`, `prompt`, `resolution`, `draft`, `duration`, `aspect_ratio` (always `"auto"`), `generate_audio`, `bitrate_mode`, `codec`, `end_user_id`. No `seed`.
- **`text-to-video`:** `prompt` (required) plus the same settings as `image-to-video`. No `seed`.
- **`draft/complete`:** `draft_id` (required), `resolution` (`"1080p"` only), `codec`.
- **Seedance 2.0 reference-to-video:** `prompt` is required, `image_urls` has maxItems 9, `audio_urls` and `video_urls` have maxItems 3, `duration` runs `"4"`–`"15"`, `resolution` adds `"4k"`, and there is no `task`, `draft` or `seed`.

### 1.3 What each capability means for this video

- **Audio input and lip-synced singing:**
  - **2.5 reference-to-video:** only the reference-to-video endpoints take audio (2.5, 2.0, and their fast, mini and US variants). fal's README says audio references are "Used for rhythm, timing, and voice", and that "Audio in the same latent space … makes reference audio usable as an actual timing signal for on-screen action." The official BytePlus demo on fal's Seedance 2.5 page shows "Four performers, one per image reference, sing and dance … Every one of them lip-syncs to the track supplied as an audio reference, with cuts landing on the beat" (https://fal.ai/seedance-2.5).
  - **Accuracy:** nothing official says how accurate the sync is or whether the output starts exactly at the start of the audio reference [unconfirmed]. fal's own comparison says LTX-2.5's audio-to-video "times the visuals to [a supplied track], with no counterpart on Seedance 2.5." In other words, there is no dedicated audio-driven endpoint; audio is one reference among many.
  - **Seedance 2.0 reference-to-video:** it also accepts audio (≤15 s combined). fal documents it as "an audio clip for the soundtrack" or a voiceover. Singing lip-sync to a supplied song on 2.0 [unconfirmed].
  - **T2V and I2V:** they have no audio input. They only voice lines written in double quotes, so they cannot follow a given song.
- **Own audio:** every 2.x endpoint generates sound jointly with the picture (`generate_audio`, same price on or off). Seedance 1.5 generates audio; 1.0 does not. For this video the generated audio is thrown away and the master is laid back in the edit. Keep `generate_audio: true` anyway, because the returned audio is what the sync check cross-correlates against the reference (see 6.4).
- **Multi-shot:** there is no separate endpoint. Label shots in the prompt ("Shot 1: … Shot 2: …", or time ranges such as `[0 to 2.5 seconds] … Cut to …`). BytePlus says timestamps are "an event's time budget, not a precise edit point" (https://fal.ai/learn/devs/how-to-use-seedance-2-5). Without labels, long prompts tend to come out as one continuous take (https://fal.ai/learn/tools/how-to-use-seedance-2-0).
- **First and last frame:** 2.x `image-to-video` takes `end_image_url`. In 2.5 reference mode you can also write "@Image1 is the first frame … @Image2 is the last frame" and add character and style references. The aspect ratio then locks to the first image, and both images should share it or the last frame gets stretched (BytePlus guide).
- **Camera control:** prompt only on 2.x. Terms such as "Dolly zoom, rack focus, tracking shot, handheld, POV, aerial" are documented as working. Seedance 1.x has a `camera_fixed` boolean.
- **Editing and extension:** 2.5 reference-to-video with `task: "editing"` re-shoots or edits a source clip. The output keeps the source's aspect ratio, and its duration can differ by "up to approximately 0.3 seconds". fal's multi-angle guide (https://fal.ai/learn/tools/how-to-create-multi-angle-video-seedance-2-5) keeps a performer's lips on the source audio with a "MOUTH MAP" of TALKING/QUIET windows, built from ElevenLabs Scribe v2 word timings. That pattern is directly reusable for singing.
- **Draft workflow:** set `draft: true` on the global 2.5 endpoints. You get a 480p preview plus a `draft_id`, and `bytedance/seedance-2.5/draft/complete` "renders that task again at 1080p from the ID alone" (fal). How closely the 1080p re-render matches the draft is [unconfirmed]. That the draft is billed at the 480p rate is [unconfirmed] but implied, since the draft overrides resolution.
- **Latency:**
  - **Seedance 2.0:** "Generations complete in under 2 minutes" (https://fal.ai/seedance-2.0).
  - **Market-wide:** fal, September 2026: "Most models take 2-6 minutes per clip" (https://fal.ai/learn/tools/ai-video-generators).
  - **Seedance 2.5:** reference jobs with video inputs "are the slowest of the three endpoints" (fal README). No published figure for 2.5 [unconfirmed]. Plan on minutes per clip and run jobs in parallel through the queue.

### 1.4 Known failure modes (sourced)

| Failure | Evidence | Mitigation |
|---|---|---|
| Timing is approximate, not frame-accurate | BytePlus: "Timestamps allocate time to events; they are not frame-accurate edit points." "For … frame-level timing that must be completely accurate, use prepared reference materials, video generation, and post-production together." | Measure the sync offset on every clip (6.4) and slip it in the edit. Cut audio excerpts to whole-second lengths equal to `duration`. |
| Text rendering and lyric typography | Same BytePlus limitation for "subtitles, formulas, signs". fal tip: "keep on-screen type outside double quotes" (otherwise it gets voiced). 2.5 claims "Improved stability keeps stray subtitles and unwanted background music out", which implies 2.0 had them. | No lyric text in the generated video. Do all typography in post (the pdoom renderer already does this). Add "No subtitles, captions or on-screen text" to every prompt. |
| Two mouths moving on one voice | fal test: "Two speakers in one frame tests lip-sync isolation, where the common failure is both mouths moving on every line." | One singing face per lip-sync shot. Use "the other holds completely still" rules for group shots. |
| Illustrated style drifting toward photography or 3D | fal: "video models tend to move a painted still toward photography once motion starts." Their prompt guard: "Every frame stays a gouache painting on rough paper … never let the image resolve toward photography." | Add a style-hold clause to every prompt. Better still, generate flat, clean shapes and apply the print texture (halftone, riso misregistration, paper) deterministically in post (6.3). |
| Identity drift on turns; wardrobe drift; style bleed | fal: "Identity drift on turns is the failure I see most … reference set containing no profile and no rear view." "Wardrobe drifting while the face holds is the most common." "Style bleed appears when a motion reference carries more than motion." | Build a multi-angle turnaround sheet plus a mouth-shape sheet. Pass separate crops rather than a grid. Name garments in the prompt. Say "use only X" and "do not use Y" for every reference. |
| Too many references | fal: "More references is not automatically better. Each one competes for influence." BytePlus: "Stability may decrease as the number of materials grows" (recommended 1–8 subjects). | Pass 2–4 references per shot. |
| Skipped middle events or rushed endings | fal prompting guide: timing blocks "give Seedance fewer chances to skip the middle or rush to the ending". | One primary change per time block, with explicit end states. |
| Lip-sync quality below SFX quality (2.0) | fal 2.0 guide: "dialogue with lip-sync works, but the audio quality appears to be strongest on sound effects and ambient audio … test the lip-sync quality". | Run the bake-off in 6.2 before committing. |
| Hands | fal: "Hands are the usual failure point in product video." | Frame hands out of lip-sync close-ups, or keep them simple. |
| Seed is not fully deterministic | Schema: "results may still vary slightly even with the same seed." Only 2.5 reference-to-video takes a seed. | Use `draft` → `draft/complete` to lock a chosen take, after confirming that completion reproduces the draft (6.2 / 6.6). |
| Independent user reports on singing lip-sync, drift and text | Not gathered: the session's web-search budget ran out. | [unconfirmed]. Treat 6.2 as the real test. |

---

## 2. Audio-driven lip-sync and singing models on fal

**Method:** about 45 endpoints were checked. Prices are quoted from each endpoint's `llms.txt`, and inputs come from its OpenAPI schema. Source keys (S…, U…) are listed at the end of the section. U-keys are GitHub-issue user reports, marked [user report].

**What was not found:**
- Hedra is **not on fal** (a catalogue search for "hedra" returns nothing).
- **No model is documented on a risograph, halftone or screenprint character**, so texture stability is untested for all of them. Section 6.3 avoids the question by applying the print in post.

### 2A. Image + audio → singing video (generation)

| Endpoint ID | Inputs | Max length / res | Price (quoted) → 10 s | Singing notes | 2D / stylised stability | Seed |
|---|---|---|---|---|---|---|
| `minimax/h3-max/lip-sync/image-to-video` (2026-09-17) | `image_url`, `audio_url`, `resolution`, `enable_transcription`, `seed` | Audio **≥5 s** (pad 4 s shots); the schema says "up to 15 minutes" but the landing page says it clips at 15 s [conflict]. 480P / 768P / 1080P / 2K | "$0.05 per second at 480p, $0.08 per second at 768p, $0.16 per second at 1080p, and $0.32 per second at 2K. A 1.2x multiplier is added to videos over 15 seconds" → $0.50 / $0.80 / $1.60 / $3.20 | Official singing demo. fal: set `enable_transcription` off "for singing, sound-designed audio" so it syncs to the waveform alone (S1) | Official: "2D illustrations and paintings"; "Framing, expression and lighting stay as they are in the source image" (S1). Only 12 days old, so no independent reports | yes ("reproduce a take exactly") |
| `fal-ai/bytedance/omnihuman/v1.5` | `image_url`, `audio_url`, `prompt`, `mask_url`, `resolution` (720p / 1080p), `turbo_mode` | Audio <30 s at 1080p, <60 s at 720p ("720p generation is faster and higher in quality") | "$0.16 per seconds" → $1.60 | Strongest official singing evidence: "crafts a soulful digital singer from a single image and song … natural pauses and breaks … from solo ballads to upbeat concerts" (S2). The paper says it "supports both talking and singing" (S3) | Official: works on "anthropomorphic characters, and stylized cartoons" (S2). It regenerates the whole frame with large motion, so the halftone may be redrawn [unconfirmed] | no |
| `fal-ai/kling-video/ai-avatar/v2/pro` | `image_url`, `audio_url`, `prompt` | Output = audio length. No cap or resolution stated on fal | "$0.115 per seconds" → $1.15 | Kling-Avatar paper: training data includes "singing performances", with a bilingual-singing benchmark (S4) | fal: "cartoons, or stylized characters"; "preserves the exact appearance, style … animating only facial features and subtle head movements" (S5). Least drift by wording | no |
| `fal-ai/kling-video/ai-avatar/v2/standard` | same | same | "$0.0562 per seconds" → $0.56 | Pro has "smoother lip-sync precision" | same | no |
| `fal-ai/sync-lipsync/v3/image-to-video` | `image_url`, `audio_url` | Output = audio length | "$0.1333 per output second" → $1.33 | sync.so on songs: "isolate and upload the vocals track" (S6) | fal: "works with any illustration or animated frame". sync.so: "human-like faces" only (S7, S8) | no |
| `veed/fabric-1.0` (`/fast`) | `image_url`, `audio_url`, `resolution` (480p / 720p) | Not stated | "480p - $0.08 per second, 720p - $0.15 per second" → $0.80 / $1.50 (fast: $0.10 / $0.20 per s) | "Bring your own voiceover, narration, dialogue, or song"; has a music-video example (S9) | "Animate illustrated characters, brand mascots", with head and body motion (S9b) | no |
| `fal-ai/creatify/aurora` | `image_url`, `audio_url`, `prompt`, `guidance_scale`, `audio_guidance_scale`, `resolution` | 480p / 720p | "$0.07 per video second for 480p, $0.14 per video second for 720p" → $0.70 / $1.40 | "an audio clip (speech or song)", "singing avatars" (S11) | "animated characters" | no |
| `fal-ai/infinitalk` | `image_url`, `audio_url`, `prompt`, `seed`, `resolution`, `num_frames` 41–721 | ≈28.8 s at 25 fps | "$0.2 per seconds" → $2.00 | [user report] 4-minute pop-ballad test (U2) | [user report] on anime it "was trying to be realistic rather than stylized" (U3) | yes |
| `fal-ai/ai-avatar/multi` (MultiTalk) | `image_url`, `first_audio_url`, `second_audio_url`, `prompt`, `seed`, `num_frames` 41–241 | ≤9.6 s per call | "$0.2 per seconds" (1.25x above 81 frames) → $2.00–2.50 | README: "Support the generation of cartoon character and singing" (S13) | [user report] anime mouths aren't "traditional" anime; 3D animals failed (U3, U6) | yes |
| `fal-ai/wan/v2.2-14b/speech-to-video` (Wan-S2V) | `image_url`, `audio_url`, `prompt`, `num_frames` 40–120, `frames_per_second`, `resolution`, `seed` | 7.5 s per call at 16 fps | "$0.20 per video second for 720p, $0.15 … 580p, $0.10 … 480p" → $2.00 / $1.50 / $1.00 | Trained on "speaking, singing, and dancing" (S15) | Aimed at realistic footage | yes |
| `fal-ai/longcat-single-avatar/image-audio-to-video` | `image_url`, `audio_url`, `prompt`, `negative_prompt`, `num_segments` 1–10, `resolution`, `seed` | ~5.8 s + 5 s per segment | "$0.3 per video second for 720p, $0.15 … 480p" | "Singer" demos, including a cartoon owl (S16) | **Default `negative_prompt` contains "style, works, paintings"**, which works against an illustrated look; override it | yes |

Also checked, not recommended:
- `mirage-api/avatar-x/reference-to-video` ($0.30/s; 9:16 and 16:9 only; no singing or stylised claim).
- `fal-ai/heygen/avatar4/image-to-video` ($0.10/s; no singing claim).
- `fal-ai/echomimic-v3` ($0.20/s; [user report] its face detector misses anime faces, U5).
- `fal-ai/flashtalk` ($0.02/s; built for speech, 768×448).
- `fal-ai/bytedance/omnihuman` v1 ($0.14/s; superseded by v1.5).

### 2B. General audio-driven video models and reference-to-video models with audio

| Endpoint ID | Audio role | Limits | Price → 10 s | Notes |
|---|---|---|---|---|
| `bytedance/seedance-2.5/reference-to-video` | `audio_urls` references ("rhythm, timing, and voice") | see section 1 | $0.2205 / $0.4730 / $1.164 per s | Official demo lip-syncs 4 performers to a supplied track. Sync accuracy [unconfirmed] |
| `lightricks/ltx-2.5/audio-to-video/pro` / `/fast` | Driving track; optional first-frame `image_url` | Audio 2–20 s (Pro: "maximum of 10 seconds"); 1080p; fps 24/25/50 | "$0.17 per second" (Pro, 1080p) / "$0.13 per second" (fast) → $1.70 / $1.30 | "synchronized to music, dialogue, or a soundtrack". No singing-lip claim. No seed |
| `fal-ai/ltx-2.3-quality/audio-to-video` (+ `/lora`) | Driving track + `image_url`, `seed`, up to 3 LoRAs | Frames follow the audio | "$0.0024075 per megapixel" (≈$0.53 per 10 s at 720p24); LoRA "$0.0027075 per megapixel" | **Default negative prompt includes "style, artwork, painting"** and prompt expansion is on; override both |
| `fal-ai/ltx23-trainer-v2/a2v` | Trains an image+audio→video LoRA (zip of start.png + audio.wav + end.mp4 + caption per clip) | Clips ≥89 frames | "0.006 * steps. With 1000 steps, your request will cost $6.00" | The only fal route to bake the exact print look into an audio-driven model (S29) |
| `fal-ai/wan/v2.7/image-to-video` | `audio_url` "driving audio … 2-30s. Max 15 MB" | 2–15 s; 720p / 1080p | "$0.1 per second for 720p … $0.15 per second" 1080p | Wan 2.7 singing quality [unconfirmed]. Alibaba's Wan 2.5/2.6 docs show a stylised graffiti character rapping to a supplied track (S20) |
| `pixverse/music-video/vibemv` | Whole-song music-video agent: `audio_url`, `image_url`, `style`, `style_image_url`, `music_style`, `lyrics`, `aspect_ratio`, `resolution` | Audio 10 s–6 min | "$0.06 per second" 720p, "$0.09" 1080p → a 150 s song costs $9.00 / $13.50 | PixVerse's API has a `lip_sync_switch` (default off) that **fal does not expose**, so lip-sync on fal is [unconfirmed]. It picks its own shots. Useful only as a cheap animatic or style probe |
| `minimax/h3/reference-to-video` | `reference_audio_urls` ≤3 (≤15 s) | 5–15 s | "$0.06 per second at 768p" | fal: reference audio is used to "transfer or clone that voice", which **regenerates** the audio. Not a verbatim driving track |
| `xai/grok-imagine-video/v1.5/reference-to-video`, `alibaba/happy-horse/v1.1/reference-to-video` | No audio input on fal | – | – | Cannot lip-sync to our vocal |
| `fal-ai/wan/v2.2-14b/animate/move` (video-driven, not audio) | `image_url` + `video_url` of a performance | 480p–720p | "$0.08 per video second" at 720p, billed at 16 frames per video-second (≈$1.20 for a 10 s 24 fps source) | Transfers a filmed singing performance (a real singer, or a photoreal Seedance take) onto the 2D character. Held notes and vibrato come from the real performance [inference] |

### 2C. Video + audio → video (re-lip-sync an existing Seedance clip)

| Endpoint ID | Inputs | Limits | Price (quoted) → 10 s | Notes |
|---|---|---|---|---|
| `fal-ai/sync-lipsync/v3` (sync-3) | `video_url`, `audio_url`, `sync_mode`, `options{model_mode, prompt, active_speaker_detection{auto_detect, coordinates, frame_number, bounding_boxes, face_image}}` | Input ≤4096×2160, ≥480p (1080p recommended) | "$8 per minutes" → $1.33 | Only vendor with official song guidance ("isolate … the vocals track"). "Silent lips can be opened naturally." Processes the whole shot and edits the face region only, so the rest of the frame is kept. Picks the singer in multi-face shots. "human-like faces" only (S6–S8) |
| `fal-ai/sync-lipsync/v2/pro` | `video_url`, `audio_url`, `sync_mode` | – | "$5 per minutes" → $0.83 | Face generated at 512×512 and composited back, which can soften fine texture |
| `veed/lipsync/v2` | `video_url`, `audio_url` | – | "$0.07 for every second of output video" → $0.70 | Official: "animated characters that show a clear, front-facing speaker" (S10). No singing claim |
| `fal-ai/heygen/v3/lipsync/precision` | `video_url`, `audio_url`, `start_time`, `end_time`, `enable_dynamic_duration` (**set false** to keep clip length locked to the music), `disable_music_track` | Partial ranges supported | "$0.1 per seconds" → $1.00 | "frame-accurate". No singing or stylised claims |
| `fal-ai/sync-lipsync/react-1` | `video_url`, `audio_url`, `emotion`, `model_mode` (lips / face / head) | **≤15 s** | "$10 per minutes" → $1.67 | Adds expression and head motion; human-focused |
| `fal-ai/latentsync` | `video_url`, `audio_url`, `guidance_scale`, `seed` | – | "$0.2 for videos up to 40 seconds" | README shows anime demos. [user report] "Face not detected" on cartoons (U4) |
| `fal-ai/kling-video/lipsync/audio-to-video` | `video_url` (2–10 s, 720–1920 px), `audio_url` | ~12 min processing | "$0.014 per input video seconds, rolling up to closest 5 second increment" | Pricing text conflicts with the README [unconfirmed]. Cheapest option |
| `fal-ai/infinitalk/video-to-video` | `video_url`, `audio_url`, `prompt`, `seed` | – | "$0.3 per seconds" → $3.00 | **Do not use as a fix-up**: it re-generates the whole body performance; maintainer: "designed not to copy the body motion" (U1) |

### 2D. Ranking for this video

The same lead-vocal stem drives every candidate. Its backing vocals, ad-libs and long reverb tails are gated out, because they make the mouth move [inference]. The master mix goes back in during the edit.

1. **Image + audio → singing, 2D printed-look character.** Run a bake-off before committing (about $3.55 per 10 s round across the three):
   - `fal-ai/bytedance/omnihuman/v1.5` at 720p: best singing evidence; `mask_url` covers duets.
   - `minimax/h3-max/lip-sync/image-to-video` at 768p with `enable_transcription=false`: seed, explicit 2D claim, cheapest.
   - `fal-ai/kling-video/ai-avatar/v2/pro`: face-only animation wording, least drift.
2. **Video + audio fix-up for Seedance clips:**
   - `fal-ai/sync-lipsync/v3` is first choice.
   - `veed/lipsync/v2` is the budget option.
3. **Full mix vs isolated vocal:**
   - Only sync.so explicitly asks for the isolated vocal.
   - Open audio-driven avatar research (StableAvatar, S28) reports that background music degrades lip-sync.
   - So feed stems and never the full mix, except to LTX audio-to-video or VibeMV, which are built around whole tracks.
4. **Seeds:**
   - Have seeds: H3 Max Lip Sync (the only one promising exact repeats), Seedance 2.5 reference-to-video, the Wan family, InfiniteTalk and MultiTalk, LongCat, LatentSync, and LTX-2.3-quality.
   - No seeds: OmniHuman, Kling Avatar, sync.so, VEED, HeyGen, Creatify.

Sources:
- **S1** https://fal.ai/h3-max-lip-sync
- **S2** https://omnihuman-lab.github.io/v1_5/
- **S3** https://arxiv.org/abs/2502.01061
- **S4** https://arxiv.org/html/2509.09595
- **S5** https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/pro
- **S6** https://sync.so/docs/models/sync-3.md
- **S7** https://sync.so/docs/models/lipsync.md
- **S8** https://sync.so/docs/compatibility-and-tips/improving-lip-sync-quality.md
- **S9** https://fal.ai/veed-fabric-1.0
- **S9b** https://www.veed.io/api
- **S10** https://fal.ai/veed-lipsync-v2
- **S11** https://docs.creatify.ai/api-documentation/aurora/aurora.md
- **S13** https://github.com/MeiGen-AI/MultiTalk
- **S15** https://humanaigc.github.io/wan-s2v-webpage/
- **S16** https://meigen-ai.github.io/LongCat-Video-Avatar/
- **S20** https://www.alibabacloud.com/help/en/model-studio/image-to-video-api-reference
- **S28** https://github.com/Francis-Rings/StableAvatar
- **S29** https://fal.ai/models/fal-ai/ltx23-trainer-v2/a2v
- **U1** https://github.com/MeiGen-AI/InfiniteTalk/issues/11
- **U2** https://github.com/MeiGen-AI/InfiniteTalk/issues/71
- **U3** https://github.com/MeiGen-AI/MultiTalk/issues/206
- **U4** https://github.com/bytedance/LatentSync/issues/115
- **U5** https://github.com/antgroup/echomimic_v3/issues/33
- **U6** https://github.com/MeiGen-AI/MultiTalk/issues/64

Unconfirmed in this section:
- Behaviour on halftone or riso textures, for every model.
- Whether OmniHuman, Kling, H3, Fabric and Aurora cope with a full mix.
- H3 Lip Sync's length cap and 2K price (llms.txt vs landing page), and its `enable_transcription` default.
- Kling Avatar v2's resolution and fps on fal.
- Whether VibeMV on fal lip-syncs at all.
- Which pricing line is right for Kling LipSync.

A deterministic alternative for close-ups: composite mouth shapes from the character sheet using phoneme timing from `align.py`, or from Rhubarb Lip Sync (active; v1.14.0, repo pushed 2026-06). This keeps sync exact and the print look intact. Rhubarb is built for speech, so its accuracy on singing is [unconfirmed].

---

## 3. Image models on fal

Sources:
- fal OpenAPI schema (max reference images) and llms.txt (quoted prices) for each endpoint.
- fal guides: https://fal.ai/learn/tools/ai-character-consistency, https://fal.ai/learn/devs/gpt-image-2-5-vs-gpt-image-2.
- Vendor docs: Google Gemini image, BFL FLUX.2 / klein training, Recraft V4 Styles, Krea 2, Ideogram, Qwen model cards.

fal bills "megapixel" as 1024×1024 px, so 1920×1080 ≈ 2 MP. "150×" means 150 images at the setting shown.

### 3.1 Generation and edit endpoints

| Endpoint ID | Use | Max refs | Resolution | Price (quoted) → 150× | Style ref / LoRA | Seed | Notes |
|---|---|---|---|---|---|---|---|
| `openai/gpt-image-2.5/sunburst/edit`, `openai/gpt-image-2.5/flare/edit` (+ `/text-to-image`) | edit, multi-ref, sheets | **16** + `mask_url` | long edge ≤3840, 0.66–8.29 MP | Token-billed. fal table "including one input image": 1920×1080 high **$0.03960**, 3840×2160 high **$0.10008**, 1920×1080 max $0.15840 → $5.94 at 1080p high | reference images only | no | fal's character-consistency guide builds the 8-panel turnaround and the expression sheet on it. Sunburst: slower, more detail. Extra reference images are billed at $8 per 1M image tokens |
| `fal-ai/nano-banana-pro/edit` (= `fal-ai/gemini-3-pro-image-preview/edit`; t2i `fal-ai/nano-banana-pro`) | edit, multi-ref | 14 (Google: ≤6 objects, ≤5 characters, **≤3 style refs**) | 1K / 2K / 4K | "$0.15 per image … 4K outputs will be charged at double" (+$0.015 with web search) → $22.50 | the only Gemini model with a style-reference slot | yes | SynthID watermark. fal used it at 2K for the Seedance 2.5 multi-angle build |
| `fal-ai/nano-banana-2/edit` | edit | 14 (≤4 characters, no style slot) | 0.5K–4K | "$0.08 per image" (×1.5 at 2K, ×2 at 4K) → $18 at 2K | refs | yes | |
| `bytedance/seedream/v5/pro/edit` (+ `/text-to-image`) | edit, multi-ref | **10** (the last 10 are used) | 1024²–2048² | "$0.0675 + $(0.0045 x number of additional input images)" (≤1536²); "$0.135 + …" (≤2048²) → ≈$12 | refs | **no** | Region-precise edits and layer separation. Used by fal for the Seedance comparison stills |
| `bytedance/seedream/v5/lite/edit` / `bytedance/seedream/v5/flash/edit` | cheap edit | 10 | Lite ≤4096² | "$0.035 per images" / "$0.027 per images" | refs | no | |
| `fal-ai/bytedance/seedream/v4.5/edit` | edit | 10 | 1920–4096 px | "$0.04 per images" → $6 | refs | yes | |
| `bytedance/seedream/v5/pro/layerize` | split into layers | 1 in → 2–17 RGBA layers | ≤2K | "$0.03375 per generated layer" (≤1536²) | – | – | Cut-paper and collage re-compositing, parallax |
| `fal-ai/flux-2-pro/edit` / `fal-ai/flux-2-max/edit` / `fal-ai/flux-2-flex/edit` | edit, multi-ref | 9 / 8 [BFL] / 10 | ≤4 MP | pro: "$0.03 for the first megapixel … $0.015 per extra megapixel of input and output"; max: "$0.07 … first … 0.03 additional"; flex: "$0.05 per megapixel" | refs ("in the style of image N") | yes | |
| `fal-ai/flux-2/lora` | t2i + LoRA | – | 512–2048 px | "**$0.021** per megapixel" → 1080p ≈$0.042 → **$6.23** | ≤3 LoRAs (scale 0–4) | yes | Consumes FLUX.2 trainer LoRAs |
| `fal-ai/flux-2/lora/edit` | edit + LoRA | **4** (each resized to 1 MP) | 512–2048 px | "$0.021 per megapixel of input and output" → 1080p + 3 refs ≈$0.105 → $15.68 | ≤3 LoRAs | yes | The only multi-ref edit endpoint where the **same style LoRA** is active during character insertion |
| `fal-ai/flux-2/klein/9b/base/lora`, `…/9b/base/edit/lora` | budget t2i / edit + LoRA | edit 4 | custom | "$0.02 per megapixels" | ≤3 LoRAs, negative prompt + CFG | yes | BFL publishes a print-style LoRA recipe for klein |
| `alibaba/qwen-image-3/edit` | edit | 1–3 | ≤2048² | "$0.04 … 1K … $0.075 … 2K" | refs | yes | Prompt expansion **on by default**; switch it off |
| `fal-ai/qwen-image-edit-2511` (+ `/lora`) / `fal-ai/qwen-image-edit-2511-multiple-angles` | edit / camera-angle views | 1–3 optimal | input size | "$0.03 per megapixels" / "$0.035 per megapixels" | ≤3 LoRAs / built-in angle LoRA | yes | Angles: rotation 0–360°, elevation −30–90°, zoom. Fills turnaround gaps |
| `ideogram/v4` (+ `/lora`, `/image-to-image/lora`) | t2i / t2i + LoRA / harmonise pass | image-to-image: 1 source | native 2K | "$0.015 per megapixel in BALANCED" (LoRA: "$0.0225 … BALANCED") → $5–8 | V4 LoRAs (≤3) | yes | fal showcase prompts include letterpress, off-register, woodcut and zine collage. Set `expansion_model` to None |
| `fal-ai/ideogram/v3` | t2i with presets | style refs | presets | "$0.03 … TURBO, $0.06 … BALANCED, $0.09 … QUALITY" | **style presets `HALFTONE_PRINT`, `WOODBLOCK_PRINT`, `COLLAGE`, `RETRO_ETCHING`, `VINTAGE_POSTER`, plus `style_codes` and `color_palette`** | yes | Fast print-look probes |
| `fal-ai/ideogram/character` (+ `/edit`, `/remix`) | character-reference gen/edit | **1** character ref + style refs/codes | presets | "$0.1 … TURBO, $0.15 … BALANCED, $0.20 … QUALITY" | style refs / codes | yes | Auto-masks face and hair, tuned for human faces. The web app disables style ref when a character ref is used [API behaviour unconfirmed] |
| `recraft/v4/style/pro/text-to-image` (/ `recraft/v4/style/text-to-image`) | style-locked t2i | 1–10 **style** refs or a saved `style_id` (no character input) | Pro 2K / 1K | "**0.1** per generated image when a **style_id** is provided" (+0.005 to create one) / "0.035" → $15 / $5.25 | `style_id` from `recraft/v4/create-style` ("$0.005 per requests"), `style_match` precise/flexible, `colors` | **no** | Recraft: one reference is safest, and mixed references "collide". Good for generating LoRA training frames |
| `krea/v2/medium/text-to-image` / `fal-ai/krea-2/turbo/style` | t2i + style refs | ≤10 style refs + moodboard / 1–3 refs | 1K / custom | "$0.030 … $0.035 (using image_style_references)" / "$0.01 per megapixels" | style refs, LoRA presets | yes | Cheapest style-reference inference |
| `fal-ai/reve/remix` (+ `/edit`, `/fast/*`) | multi-ref remix | 1–6 | aspect only | "$0.04 per images" (fast "$0.01") | refs via `<img>N</img>` tags | no | Live, but not in catalog search |
| `fal-ai/kling-image/o3/image-to-image` | multi-ref "series" | ≤10 + elements | 1K / 2K / 4K | "$0.028 per image for 1K/2K" | refs | no | `result_type=series` returns 2–9 related images |

Also checked, ranked lower:
- `fal-ai/instant-character` ($0.1/MP, 1 reference).
- `fal-ai/telestyle-v2` (style transfer, $0.035/MP).
- `meta/muse-image/edit` ($0.01, 1–10 refs, no seed).
- `luma/agent/uni-1/v1/edit`.
- `xai/grok-imagine-image/v2.0/edit`.
- GPT Image 2 / 1.5 (superseded).

There is no Midjourney endpoint on fal.

### 3.2 LoRA and style trainers

| Endpoint ID | Price (quoted) | Steps / time | Images | Consumed by |
|---|---|---|---|---|
| `fal-ai/flux-2-trainer-v2` | "0.0064 * steps. With 1000 steps, your request will cost **$6.40**" (1500 steps = $9.60) | default 1000 (100–20000). **Training time not published** | "at least 10"; fal README "9-50 … for style"; ≥1024 px | `fal-ai/flux-2/lora`, `fal-ai/flux-2/lora/edit` |
| `fal-ai/flux-2-trainer-v2/edit` | "0.0056 * steps * reference_multiplier" (≈$11.82 for 1 ref / 1000 steps) | 1000 | before/after pairs | `fal-ai/flux-2/lora/edit` |
| `fal-ai/flux-2-klein-9b-base-trainer` | "0.0043 * steps … 1000 steps … $4.3" | BFL: style 1500–2500 steps (their print-style example was best at 1500) | BFL: **20–40 optimal** | klein 9B base LoRA endpoints |
| `ideogram/v4/trainer` | "0.00675 * steps. With 1000 steps … **$6.75**" | 500–1500 for styles, 1500–3000 for characters (Ideogram manual) | 10–30 | `ideogram/v4/lora`, `ideogram/v4/image-to-image/lora` |
| `fal-ai/krea-2-trainer` | "$0.003 per step (minimum of 100 steps is charged) … $3.00 … 1000 steps" | default 100; 768 px trains "~1.7x faster" | 10–30 (Krea) | `fal-ai/krea-2/turbo/lora` |
| `fal-ai/qwen-image-2512-trainer` | "$0.0015 per step (minimum of 500 steps …)" → $1.50 per 1000 | 1000 | image + caption pairs | `fal-ai/qwen-image-2512/lora` |
| `fal-ai/flux-lora-fast-training` (FLUX.1) | "$2 per training run (scales linearly with steps)" | `is_style` flag | ≥4 | `fal-ai/flux-lora` |
| `recraft/v4/create-style` / `recraft/v4/pro/create-style` | "$0.005 per requests" | instant (no training) | 1–10 | `recraft/v4/style/*` |
| `fal-ai/ideogram/custom-models` | "$40 per training run" | – | 10–100 | `fal-ai/ideogram/custom-models/generate` |
| Video: MiniMax H3 LoRA trainers (t2v, i2v, first-last-frame, reference-to-video-audio) | per step (the rate is on each trainer page) | fal guide: 10–200 clips at exact 24 fps; rank 16, lr 2e-4 | – | H3 LoRA endpoints (https://fal.ai/learn/devs/how-to-train-a-lora-for-minimax-h3) |

None of fal's image trainer pages publish wall-clock training time [unconfirmed].

### 3.3 Recommendations

- **(a) Character sheet from text + references.**
  - **Main tool: `openai/gpt-image-2.5/sunburst/edit`.** It takes up to 16 references, and a 3840×2160 sheet costs $0.10.
  - **Sheets to make:**
    - the fal-documented 4×2 turnaround (full body over head-and-shoulders crop);
    - a 6-panel expression sheet;
    - a 3×3 **mouth chart** for singing: A/I, E, O, U, M/B/P, F/V, L, W/Q, rest, all at the same head angle.
  - Light the sheets flat and leave the panels unlabelled.
  - **Cross-check** identity on `fal-ai/nano-banana-pro/edit` (≤5 character + ≤3 style refs). Fill missing angles with `fal-ai/qwen-image-edit-2511-multiple-angles`.
  - **Don't use as the main tool:** `fal-ai/ideogram/character` and `fal-ai/instant-character`. Both take one reference only and are human-face oriented.
- **(b) Printed look held across 100+ images.**
  - **Main route:**
    1. Curate 25–30 frames in the target print style (same inks, paper and dot pitch; no text, borders or collages). Generate them with `recraft/v4/style/pro/text-to-image` using a `style_id` and `style_match=precise`, or with Ideogram V3's `HALFTONE_PRINT` / `WOODBLOCK_PRINT` presets.
    2. Train a **style LoRA** on `fal-ai/flux-2-trainer-v2` (≈1500 steps, $9.60), with content-only captions and one trigger word.
    3. Generate everything through `fal-ai/flux-2/lora` and `fal-ai/flux-2/lora/edit`.
  - **Alternative:** `ideogram/v4/trainer` → `ideogram/v4/lora`. It has native print vocabulary, 2K output, and an image-to-image LoRA harmonise pass, but no multi-reference insertion.
  - **Known drift and fixes:**
    - *Photoreal creep:* fewer steps (BFL: higher step counts "introduced excessive realism").
    - *Over-clean vector look:* precise style match, paper texture in the references.
    - *Halftone dots rendered as noise:* keep the dot pitch coarse, or better, add the halftone in post (6.3).
    - *Fake text and registration marks:* prompt expansion or Magic Prompt off.
    - *Palette drift:* hex colours or `colors` / `color_palette`, then snap to the ink set in post.
  - GPT Image, Seedream 5, Recraft V4 Styles and Reve have **no seed**, so archive every approved output.
- **(c) Inserting the character into a set.**
  - **Main route: `fal-ai/flux-2/lora/edit`** with the style LoRA (+ an optional character LoRA). Pass the background plate plus 2 crops from the character sheet (≤4 images).
  - **Hard staging or relighting:** `fal-ai/nano-banana-pro/edit`, `openai/gpt-image-2.5/flare/edit` with `mask_url` (paste the approved region back onto the original), or `bytedance/seedream/v5/pro/edit`.
  - **Then:** a low-strength harmonise pass (`ideogram/v4/image-to-image/lora` at ~0.3, or `flux-2/lora/edit`), then the post print pass.
  - **Face or hair fixes:** `fal-ai/ideogram/character/edit`.

**Unconfirmed in this section:**
- Whether a t2i LoRA from `flux-2-trainer-v2` behaves well inside `flux-2/lora/edit`. The pipeline depends on this, so test it first.
- Style drift of Nano Banana Pro, GPT Image 2.5 and Seedream 5 over 100+ images; no official data exists.
- Reference caps for FLUX.2 max / pro / flex (BFL says 8, fal says 9 / 10).
- How extra references are billed on GPT Image 2.5.
- Training times.

---

## 4. fal API mechanics

Sources:
- fal docs (https://fal.ai/docs/llms.txt): inference/queue, webhooks, reliability, fal-cdn, media-expiration, concurrency-limits, pricing, faq, errors.
- fal-client 1.0.3 source (PyPI, released 2026-09-21), read directly.

### 4.1 Mechanics table

| Mechanic | How | Limits / gotchas |
|---|---|---|
| Auth | Header `Authorization: Key $FAL_KEY`. The SDK reads `FAL_KEY` from the environment. | Keys are per account or team. |
| Submit (queue) | `POST https://queue.fal.run/<endpoint_id>` with the input JSON. Returns `request_id`, `response_url`, `status_url`, `cancel_url` and `queue_position`. | "There is no queue size limit." Queued requests are never dropped. |
| Status | `GET …/requests/{id}/status?logs=1` returns `IN_QUEUE` (with `queue_position`), `IN_PROGRESS` (with `logs[]`), or `COMPLETED` (with `metrics.inference_time`, plus `error`/`error_type` if it failed). SSE variant: `…/status/stream`. | A failed request also ends as `COMPLETED`, so always check `error`. |
| Result / cancel | `GET response_url`. `PUT …/cancel` returns 202 / 400 `ALREADY_COMPLETED` / 404. | Cancel while IN_QUEUE: never processed. Cancel while IN_PROGRESS: "may still complete". The SDK's `status/result/cancel(app, id)` build `queue.fal.run/<owner>/<alias>/requests/{id}` without the `/reference-to-video` sub-path, so prefer the URLs returned by submit. |
| Webhooks | `?fal_webhook=<url>` (SDK: `webhook_url=`). The body is `{request_id, status: "OK"/"ERROR", payload, error}`. | Your endpoint must answer 2xx. Retries for up to about 1 h, at most 31 attempts. ED25519-signed (`X-Fal-Webhook-*` headers). |
| Timeouts | `start_timeout` (SDK) sends `X-Fal-Request-Timeout`, a deadline for processing to *start* (504 if missed). `client_timeout` is client-side only. | Once a runner starts, the app's own limit applies (default 3600 s). |
| Priority | `X-Fal-Queue-Priority: normal|low` (SDK `priority=`). | "low" queues behind every normal request on shared models. |
| Retries | The queue retries 503, 504, connection errors and 429 "up to 10 times" (disable with `X-Fal-No-Retry: 1`). The SDK also retries 408/409/429 up to 10 times, and falls back to `queue.falrun.com`. | Only queue-based calls get server-side retries. |
| Upload local files | `fal_client.upload_file(path, lifecycle=StorageSettings(expires_in="30d"))` returns `https://v3b.fal.media/files/b/…`. Pass that URL in `image_urls` / `audio_urls`. Uploads over 100 MB go multipart automatically (10 MB parts). | No file-type restriction at upload. Model limits still apply (Seedance 2.5: images ≤30 MB, audio MP3/WAV ≤15 MB and 1.8–30.2 s, video ≤200 MB). |
| Data URIs | `fal_client.encode_file(path)` produces `data:…;base64,…`. | fal: "not recommended for files larger than a few KB". Whether Seedance accepts data URIs is [unconfirmed]. Use uploads. |
| Retention | Output and input files are public URLs by default. The FAQ says "available for at least 7 days by default"; the Platform Headers page says "forever … if not configured". Set retention per request with `X-Fal-Object-Lifecycle-Preference: {"expiration_duration_seconds": N}`, or account-wide via `PUT https://api.fal.ai/v1/storage/settings`. | "Expired files are permanently deleted." Download every output at once. Request JSON payloads are kept 30 days. Private access: `initial_acl`, plus signed URLs (≤7 days). |
| Concurrency | "Every new account starts with a concurrency limit of **2** … Self-serve limits scale up to **40**", based on paid invoices in the last 4 weeks. Only `IN_PROGRESS` requests count. | The spend thresholds are only shown in the dashboard [unconfirmed]. fal "may apply additional concurrency limits on certain high-demand models". |
| 429 | Queued requests are never rejected for concurrency: they wait and retry with no cap. Direct `fal.run` calls get 429 `concurrent_requests_limit` with `X-Fal-needs-retry: 1`. | Use `submit`/`subscribe`, not `run`, for video. |
| Billing | Prepaid credits, which "expire 365 days from the date of purchase". Only successful outputs are billed; queue wait and cold starts are free. "Server errors (HTTP 500+) are never charged"; 422s "may still be charged if a runner spent GPU time". | Seedance is a **Partner** API: "Standard percentage discounts do not apply." Billing for content-policy blocks and in-progress cancels is [unconfirmed]. Cost per request: `X-Fal-Billable-Units` header, and `GET https://api.fal.ai/v1/models/pricing?endpoint_id=…`. |
| Seedance latency | Official for 2.0 only: "Generations complete in under 2 minutes" (https://fal.ai/seedance-2.0). fal, September 2026: "Most models take 2-6 minutes per clip". | No Seedance 2.5 figure and no user reports [unconfirmed]. Log `Completed.metrics["inference_time"]` per job. At about 3 min per job, 120 takes need about 3 h at concurrency 2 and about 36 min at 10. |

fal-client 1.0.3 surface (from the source):
- **Queue calls:** `submit(app, arguments, *, webhook_url, priority, headers, start_timeout, hint)` returns a `SyncRequestHandle`.
- **Handle methods:** `.request_id`, `.status(with_logs=)`, `.iter_events(with_logs=, interval=0.1)`, `.get(interval=0.1)`, `.cancel()`. The default poll interval of 0.1 s is aggressive; pass `interval=5`.
- **Blocking call:** `subscribe(app, arguments, *, with_logs, on_queue_update, interval, start_timeout, client_timeout)`.
- **By request ID:** `status/result/cancel(app, request_id)`.
- **Uploads:** `upload(bytes, content_type)`, `upload_file(path)`, `upload_image(PIL)`, each with an `_async` variant, plus `AsyncClient`.
- **Types:** `StorageSettings(expires_in="never|immediate|1h|1d|7d|30d|1y"|seconds, initial_acl=StorageACL(...))`, and the status classes `Queued(position)`, `InProgress(logs)`, `Completed(logs, metrics, error, error_type)`.

### 4.2 Python: upload a local PNG + WAV, queue Seedance 2.5, poll, download, complete a draft

The calls follow the fal-client 1.0.3 source, and the same calls were dry-run against a mocked HTTP layer. Nothing was sent to fal.

```python
import json, pathlib, time
import httpx, fal_client                       # pip install "fal-client>=1.0.3"; export FAL_KEY=...

R2V = "bytedance/seedance-2.5/reference-to-video"
keep = fal_client.StorageSettings(expires_in="30d")

def up(p):                                     # local file -> https://v3b.fal.media/files/b/... URL
    return fal_client.upload_file(pathlib.Path(p), lifecycle=keep)

def wait(handle, every=10):
    while True:
        st = handle.status(with_logs=False)
        if isinstance(st, fal_client.Completed):
            if st.error:
                raise RuntimeError(f"{st.error_type}: {st.error}")
            return (st.metrics or {}).get("inference_time")
        time.sleep(every)

def download(url, dst):
    with httpx.stream("GET", url, follow_redirects=True, timeout=600) as r:
        r.raise_for_status()
        with open(dst, "wb") as f:
            for chunk in r.iter_bytes():
                f.write(chunk)

args = {
    "task": "reference",
    "prompt": ("@Image1 is the first frame. @Image2 defines Mira's face, hair and jacket; use only her "
               "appearance. Mira sings the vocal in @Audio1 to camera; lips and jaw follow every syllable "
               "of @Audio1, mouth closed in the rests. Slow push-in. Every frame stays a flat two-ink "
               "risograph print; never resolve toward 3D shading or photography. No subtitles, no text."),
    "image_urls": [up("keyframes/shot07_first.png"), up("sheets/mira_front.png")],
    "audio_urls": [up("audio/shot07_ref.wav")],   # WAV, cut sample-accurately, length == duration
    "duration": "8", "aspect_ratio": "16:9", "generate_audio": True,
    "seed": 1234, "resolution": "480p", "draft": True,  # cheap draft; draft_id returned
}
h = fal_client.submit(R2V, arguments=args, start_timeout=3600,
                      headers={"X-Fal-Object-Lifecycle-Preference":
                               json.dumps({"expiration_duration_seconds": 30 * 86400})})
print("request", h.request_id)                 # persist request_id + args for the shot log
print("inference_time", wait(h))
res = h.get(interval=5)
download(res["video"]["url"], f"renders/shot07_draft_{h.request_id}.mp4")

# after the draft passes QA (section 6.4): re-render the same task at 1080p ($1.164/s)
h2 = fal_client.submit("bytedance/seedance-2.5/draft/complete", arguments={"draft_id": res["draft_id"]})
wait(h2)
download(h2.get(interval=5)["video"]["url"], "renders/shot07_1080p.mp4")
```

Run many shots by calling `submit` for all of them first and then polling each handle. Only `IN_PROGRESS` jobs count toward concurrency, so a full queue is fine.

---

## 5. ElevenLabs: sound effects, music, stems

Sources:
- ElevenLabs OpenAPI (`https://api.elevenlabs.io/openapi.json`);
- API reference and capability pages (`https://elevenlabs.io/docs/...`);
- API pricing (`https://elevenlabs.io/pricing/api`);
- fal llms.txt pages for the fal-hosted copies.

SDK: `elevenlabs` 2.70.0 (2026-09-28). A 3.0.0a1 pre-release exists, so pin `elevenlabs<3`.

| Endpoint | Parameters | Limits | Price |
|---|---|---|---|
| **Sound effects**: `POST https://api.elevenlabs.io/v1/sound-generation` (header `xi-api-key`) | Body: `text` (required); `duration_seconds` number or null ("Must be at least 0.5 and at most 30"; null = the model picks); `prompt_influence` 0–1, default **0.3** ("higher … follow the prompt more closely … less variable"); `loop` bool, default false ("Only available for the 'eleven_text_to_sound_v2 model'"); `model_id`, whose only value is `eleven_text_to_sound_v2`. Query: `output_format`, default `mp3_44100_128` (also mp3_22050_32…mp3_44100_192, pcm_8000…pcm_48000, opus, ulaw/alaw). | Max 30 s per generation. The response is audio bytes. There is no `wav_*` format for SFX on the API (use `pcm_48000` and wrap it). The docs say "WAV at 48 kHz for non-looping effects". Higher-quality formats are plan-gated (mp3_44100_192 needs Creator+, pcm_44100 needs Pro+). | API: **$0.12 per minute**, "billed per generation". Included generations: Starter ($6) 150, Creator ($22) 605, Pro ($99) 3,000. UI: 200 credits per generation (40 credits/s when a duration is set). |
| SFX on fal: `fal-ai/elevenlabs/sound-effects/v2` | `text` (≤450 characters), `duration_seconds` ("0.5-22"), `prompt_influence` (0.3), `loop`, `output_format` | Max 22 s on fal. | "$0.002 per seconds" (same as direct) |
| **Eleven Music**: `POST /v1/music` (also `/stream`, and `/detailed`, which adds word timestamps and a waveform) | `prompt` or `composition_plan`. The plan for v2/v2.5 is `chunks` (≤30) with `text` using `[Verse]` headers, `duration_ms` 3000–120000, positive/negative styles, and `conditioning_ref {song_id, range}` ≤30 s. Other parameters: `music_length_ms` 3000–600000; `model_id` `music_v1` (default) / `music_v2` / `music_v2_5`; `seed`; `force_instrumental`; `generation_mode` (track, loop, ambience, video_to_music); `lyrics_text`; `finetune_id`; `store_for_inpainting`. | Paid plans only. Music concurrency 2 on Starter–Pro. Maximum length is 5 minutes in the docs vs 600000 ms in the schema [unconfirmed]. | **$0.15 per minute** (API). fal `elevenlabs/music/v2.5`: "$0.6 per output audio minute … rounded up" (4× direct). |
| Composition plan / inpainting | `POST /v1/music/plan`. `POST /v1/music/upload` (`extract_composition_plan`) plus a plan that mixes kept `{song_id, range}` chunks with regenerated chunks, to rewrite one section of an existing track. | `song_id` comes back in the response headers. | Upload is priced like generation. Plan pricing [unconfirmed]. |
| **Stem separation**: `POST /v1/music/stem-separation` | multipart `file`; `stem_variation_id` `two_stems_v1` or `six_stems_v1` (default). Returns a ZIP. | "might have high latency" | [unconfirmed]. Local alternatives already in use: Demucs / roformer (free). fal `fal-ai/demucs`: "$0.0007 per seconds". |
| Video to music: `POST /v1/music/video-to-music` | `videos[]` (≤10, ≤200 MB, ≤600 s), `description`, `tags`, `model_id` | 403 without a subscription | [unconfirmed] |
| Audio isolation: `POST /v1/audio-isolation` | multipart `audio` | "Not specifically optimized for isolating vocals from music." Use Demucs for the song. | $0.12/min. fal `fal-ai/elevenlabs/audio-isolation`: $0.1/min |
| Voice changer: `POST /v1/speech-to-speech/{voice_id}` | multipart `audio`; `model_id` (`eleven_multilingual_sts_v2` recommended); `seed`; `remove_background_noise` | ≤5 min per segment. Quality on sung vocals [unconfirmed]. | $0.12/min |
| **Forced alignment**: `POST /v1/forced-alignment` | multipart `file` + `text` → `words[{text, start, end, loss}]`, `characters[...]` | Useful as an independent cross-check of `align.py` word timings in the sync loop (6.4). | Same as speech-to-text: $0.22/hour. fal `fal-ai/elevenlabs/forced-alignment` rounds up to a whole hour ($0.22 per call minimum), so use the direct API. |

**Commercial terms:**
- The free plan "does **not** include a commercial license"; paid plans do.
- The Sound Effects Terms let ElevenLabs sublicense your SFX outputs unless you click "Disable" on the SFX page. Opting out is not retroactive, so do it before generating.
- Whether the same terms apply to outputs generated through fal's ElevenLabs endpoints is [unconfirmed].

**How it helps the sound design:**
- `loop=true` beds and risers, cut on the beat grid.
- `duration_seconds` pinned to beat multiples (at a given BPM, 1 beat = 60/BPM s).
- `prompt_influence` of 0.6–0.8 for repeatable one-shots.
- Six-stem separation or Demucs to duck or replace elements under SFX hits.
- Music inpainting only if the song itself may be edited.

### 5.1 Python (elevenlabs 2.70.0)

```python
import os
from elevenlabs.client import ElevenLabs
client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

def sfx(path, **params):
    audio = client.text_to_sound_effects.convert(model_id="eleven_text_to_sound_v2",
                                                 output_format="mp3_44100_128", **params)
    with open(path, "wb") as f:
        for chunk in audio:                  # Iterator[bytes]
            f.write(chunk)

sfx("sfx_riser_2p5s_loop.mp3",
    text="Tense synth riser, filtered white-noise sweep rising in pitch, seamless loop, no impact at the end",
    duration_seconds=2.5, loop=True, prompt_influence=0.6)
sfx("sfx_impact_0p8s.mp3",
    text="Tight cinematic impact hit, punchy sub-bass thump with short metallic tail, dry",
    duration_seconds=0.8, loop=False, prompt_influence=0.7)
```

### 5.2 curl

```bash
curl --fail-with-body -X POST "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"Tense synth riser, filtered white-noise sweep rising in pitch, seamless loop, no impact at the end",
       "model_id":"eleven_text_to_sound_v2","duration_seconds":2.5,"loop":true,"prompt_influence":0.6}' \
  --output sfx_riser_2p5s_loop.mp3

# same model through fal (queue):
curl -X POST "https://queue.fal.run/fal-ai/elevenlabs/sound-effects/v2" \
  -H "Authorization: Key $FAL_KEY" -H "Content-Type: application/json" \
  -d '{"text":"Tight cinematic impact hit, punchy sub-bass thump, short metallic tail, dry",
       "duration_seconds":0.8,"prompt_influence":0.7,"output_format":"mp3_44100_128"}'
# -> poll status_url, then GET response_url -> {"audio":{"url":...}}
```

---

## 6. Recommended stack + budget

### 6.1 Stack

| Stage | Tool / endpoint | Why |
|---|---|---|
| Song timing (local, free) | `euroboom/analysis`: Demucs `htdemucs_ft` + roformer lead vocal; CTC + Whisper word/syllable timings (`align.py` → `lyrics.json`); beats and downbeats (`analyze.py` → `audio.json`). Cross-check: ElevenLabs `/v1/forced-alignment` ($0.22/h) | Every shot window is anchored to lyric lines and snapped to the beat grid, as in pdoom's `timeline.ts`. Lip-sync excerpts come from these timings |
| Character sheet | `openai/gpt-image-2.5/sunburst/edit` (turnaround, expressions, 3×3 mouth chart); cross-check on `fal-ai/nano-banana-pro/edit`; angles from `fal-ai/qwen-image-edit-2511-multiple-angles` | Up to 16 references; fal's documented sheet workflow |
| Style lock | 25–30 curated frames from `recraft/v4/style/pro/text-to-image` (`style_id`, precise), then a style LoRA on `fal-ai/flux-2-trainer-v2` (~1500 steps, $9.60) + a character LoRA | Tightest texture lock. The same weights drive the plates and the insertion |
| Keyframes and plates (~150 images) | `fal-ai/flux-2/lora` (≈$0.042 per 1080p image); insertion with `fal-ai/flux-2/lora/edit` (≤4 refs); hard shots with `fal-ai/nano-banana-pro/edit` | Cheap, seeded, LoRA-consistent |
| Print finish | One deterministic print shader (6.3) over every still and clip | Identical texture everywhere; no boiling |
| Lip-sync performance shots | Default: `bytedance/seedance-2.5/reference-to-video`, with @Image1 as first frame, @Image2–3 as sheet crops, @Audio1 as the lead-vocal WAV. Iterate with `seed` + `draft:true` at 480p, then finish with `bytedance/seedance-2.5/draft/complete` (1080p). Close-ups may switch to the bake-off winner among `fal-ai/bytedance/omnihuman/v1.5`, `minimax/h3-max/lip-sync/image-to-video` and `fal-ai/kling-video/ai-avatar/v2/pro` (6.2) | Seedance gives camera, body and performance in one pass, with a documented multi-singer lip-sync demo. The dedicated models have stronger singing evidence for faces |
| Lip-sync fix-up | `fal-ai/sync-lipsync/v3` (budget: `veed/lipsync/v2`) driven by the lead-vocal stem | Edits the face only and keeps the rest of the frame |
| Non-lip-sync shots | `bytedance/seedance-2.5/reference-to-video` in first-frame mode at 720p with character refs and `seed` (same price as image-to-video; image refs are free). Budget option: `bytedance/seedance-2.0/image-to-video` at 720p ($0.3034/s) | Identity lock, seed and prompt adherence. The 30 s ceiling is irrelevant for 4–10 s shots |
| Upscale 720p → 1080p | `topaz/upscale/video/precision` ("$0.20 [per 10 s] at 1080p"; Gaia 2 animation model $0.10) or `fal-ai/bytedance-upscaler/upscale/video` ("$0.0072/s" at 1080p) | Roughly 1/60 of the cost of native 1080p Seedance ($1.164/s); the print pass hides the difference |
| SFX / sound design | ElevenLabs `/v1/sound-generation` (Creator plan $22/mo: commercial licence, 605 included generations; opt out of SFX sublicensing first), or `fal-ai/elevenlabs/sound-effects/v2` ($0.002/s) | Loops, risers and impacts timed to the beat grid |
| Assembly | pdoom-style renderer: lyric typography, cuts snapped to beats, 24 fps timeline | The models never render text |
| QA | Verification loop in 6.4 on every take, the draft and the final | Sync is measured, not assumed |

### 6.2 Lip-sync bake-off (≈$41, before production)

Three excerpts, all using the same keyframe (a printed-look close-up) and the same lead-vocal stem:
1. a fast syllabic verse line, about 6 s;
2. a held chorus note with vibrato, about 8 s;
3. a quiet line heavy on plosives (m/b/p), about 6 s.

| Candidate | Setting | Cost (2 takes × 20 s) |
|---|---|---|
| Seedance 2.5 reference-to-video | 480p draft, @Audio1 = lead vocal. A second variant uses the full mix | $8.82 (+ $9.46 for one 720p check of the winner) |
| OmniHuman v1.5 | 720p | $6.40 |
| H3 Max Lip Sync | 768p, `enable_transcription=false`, seed | $3.20 |
| Kling AI Avatar v2 Pro | – | $4.60 |
| sync-3 fix-up | on the Seedance takes | $5.33 |
| VEED lipsync v2 fix-up | on the Seedance takes | $2.80 |

How to judge:
- **Automatic scores:** the 6.4 metrics (lag, r, word hits, rest hits).
- **Blind human ranking:** style fidelity to the keyframe (line, palette, texture), and performance (breaths, held notes).
- **Pick a winner per shot type:** close-up singing vs medium/wide shots with body and camera motion.
- **Draft vs completion:** complete one Seedance draft at 1080p and compare it to the draft. If the motion changes, stop relying on `draft/complete` and use 720p finals + upscale instead.

Seedance singing prompt pattern (uses the BytePlus reference-role syntax; untested for singing):

```
@Image1 is the first frame; keep its composition and camera direction.
@Image2 defines <Singer>'s face, hair and jacket; use only her appearance, not its background.
@Audio1 defines <Singer>'s sung lead vocal. <Singer> sings @Audio1 to camera: lips, jaw and breath
follow every syllable, the mouth stays open through held notes and closes in the rests.
Only <Singer> sings; nobody else moves their mouth. Slow push-in, subtle head sway on the beat.
Every frame stays a flat two-ink risograph print on off-white paper; never resolve toward 3D
shading or photography. No subtitles, captions or on-screen text.
```

Settings: `duration` equals the excerpt length in whole seconds, `aspect_ratio` "16:9", `generate_audio` true (needed for the sync check), and a fixed `seed`.

### 6.3 Keeping the printed look consistent: apply the print in post, don't ask the models for it

This is a recommendation, not a vendor claim.

**Why:**
- Video models redraw fine texture on every frame, so halftone dots and paper grain shimmer ("boil").
- fal observes that "video models tend to move a painted still toward photography once motion starts."
- A deterministic print pass guarantees the same texture on all ~150 stills and ~40 clips.

**How:**
1. Generate the design layer with a style reference or a trained style LoRA (section 3). That layer is composition, character, flat shapes, and a palette limited to 2–3 "inks" plus paper.
2. In the renderer, run one shared print shader over every still and clip:
   - separate the image into 2–3 spot inks;
   - screen each ink as halftone at a fixed angle and LPI;
   - offset each ink by a small misregistration that is constant within a shot (it can re-jitter on downbeats from `data/audio.json` as a "reprint" effect);
   - multiply onto a scanned paper texture;
   - add a little ink spread.
3. Lock the halftone screen to the frame, as in a real print, so the dots never swim with the motion.
4. Add a style-hold clause to every video prompt anyway, e.g. "every frame stays a flat two-ink print … never resolve toward 3D shading or photography", and never let the models render lyrics or other text.

The pdoom renderer (`ref/pdoom-video/app/src/engine`) already has a post-processing chain for grain and halation, so this is an extension of existing code, not a new tool.

### 6.4 Verification loop: lip-sync timing against the song

The loop reuses the existing analysis toolchain in `euroboom/analysis`:
- Demucs and roformer stems;
- CTC plus Whisper word timings (`align.py` → `data/lyrics.json`);
- vocal features at a 5 ms hop (`vocal_feats.py`: RMS, onset, pyin f0, voiced);
- QA plots (`qa_plot.py`).

It adds only `opencv-python`, and `mediapipe` if needed, to `pyproject.toml`.

1. **Cut the reference excerpt sample-accurately, as WAV not MP3.**
   - Use the gapless decode of the master as the time reference, as `analysis/common.py` already does. MP3 encoding adds a priming delay (1105 samples, 23 ms, for the pdoom master). That is about half a frame at 24 fps, which eats half of the ±1-frame tolerance before any model error.
   - Cut: `ffmpeg -i master.wav -af "atrim=start=T0:duration=D,asetpts=PTS-STARTPTS" -ar 48000 -c:a pcm_s16le shotNN_ref.wav`
   - Choose `D` as a whole number of seconds equal to the Seedance `duration` string (4–10). Make a lead-vocal version of the same window from the stem.
2. **Generate.**
   - Seedance 2.5 reference-to-video: `audio_urls=[shotNN_vocal.wav]`, `duration=str(D)`, a fixed `seed`, `generate_audio=true`, `draft=true` at 480p. Use the lead-vocal cut; the full mix is only for the 6.2 variant test.
   - Or the lip-sync model chosen in 6.2.
   - Log the request_id, seed and inputs for every take.
3. **Measure three signals per take** (all on the 24 fps grid; 1 frame = 41.7 ms):
   - **a. Audio offset.** Extract the clip's own audio (`ffmpeg -i clip.mp4 -vn -ac 1 -ar 48000 clip.wav`). Cross-correlate its onset-strength envelope (5 ms hop) with the reference's, searching ±1 s. Result: δ_audio in ms, plus a peak score. A low score means the model re-sang rather than reproduced the track; then trust (b) alone.
   - **b. Visual lip offset.** Build a mouth-aperture signal m[n] per frame:
     - MediaPipe FaceLandmarker inner-lip gap (landmarks 13–14) divided by mouth width (78–308) when a face is detected;
     - otherwise, for flat 2D faces that the detector misses [unconfirmed how often], a tracked mouth ROI (template match from the keyframe) measuring the area of the "mouth-interior" ink colour.
     - Compare m[n] with the lead-vocal RMS envelope v[n] (log, gated by pyin voiced) resampled to 24 fps.
     - Take the lag with maximum Pearson r over ±12 frames. Positive lag means the mouth is late. (Estimator tested on synthetic signals: it recovers −3/0/+2/+5-frame shifts exactly.)
   - **c. Mouth map per word** (the same idea as fal's Seedance "MOUTH MAP" TALKING/QUIET windows):
     - For each sung syllable in `lyrics.json` inside the window, the mouth must be open (m above the clip's 60th percentile) during the vowel.
     - For each rest of 250 ms or more, the mouth must be closed.
     - Report hit rates, and list failing words with timestamps.
4. **Pass criteria:**
   - |lag| ≤ 1 frame. That keeps it inside the EBU R37 tolerance of audio ≤40 ms early / ≤60 ms late [unconfirmed: from memory, the ITU/EBU pages could not be fetched].
   - r ≥ the value measured on the first human-approved clip (start at 0.5).
   - Word hits ≥ 90% and rest hits ≥ 80%.
   - A human spot-check of held notes, breaths and m/b/p closures.
5. **Act on the result:**
   - **Constant non-zero lag:** slip the clip in the edit by the lag (use δ_audio when both measures agree).
   - **Low r or failed words:** regenerate with a new seed, or run the video+audio lip-sync fix-up (6.2) on the lead-vocal excerpt, then re-measure.
   - **Lag drifting** between the first and second half of the clip: shorten or split the shot.
6. **Sign off on the final render, not the draft.** `draft/complete`, or a 720p re-run, is a separate render, so re-run steps 3–5 on it before the clip is final.
7. **Check the whole edit.** After conform:
   - render the timeline with the master audio;
   - recompute the per-shot lags in song time, which catches clips placed at the wrong song position;
   - produce one `qa_plot.py`-style sheet per shot (spectrogram + pitch + word boundaries + m[n]) plus a 6 fps contact sheet for review.
   - Keep the timeline at 24 fps (or 48 fps) so Seedance's fixed 24 fps is never pulled down.

### 6.5 Budget

**Assumed shot plan** (change the counts and the maths follows):
- 15 lip-sync performance shots, averaging 7 s (105 s);
- 25 non-lip-sync shots, averaging 7 s (175 s);
- 40 clips and 280 s of keeper footage in total, about 1.9× the 150 s runtime to allow handles and alternates;
- about 150 images.

All video prices are fal's per-second figures for 16:9.

| Line | Endpoint | Quantity | Unit price | Cost |
|---|---|---|---|---|
| Lip-sync bake-off | 6 candidates (6.2) | – | – | $40.61 |
| Lip-sync drafts | `seedance-2.5/reference-to-video`, 480p draft | 105 s × 3 takes = 315 s | $0.2205/s | $69.46 |
| Lip-sync finals | `seedance-2.5/draft/complete`, 1080p | 105 s | $1.164/s | $122.22 |
| Lip-sync fix-ups | `fal-ai/sync-lipsync/v3` | ~half of finals, 52 s | $8/min | $6.93 |
| Non-lip-sync shots | `seedance-2.5/reference-to-video`, first-frame mode, 720p | 175 s × 2.5 takes = 437.5 s | $0.4730/s | $206.94 |
| Upscale 720p → 1080p | `topaz/upscale/video/precision` | 175 s | $0.20 per 10 s | $3.50 |
| Images, all ~150 finals incl. 2–3 rerolls, 3 LoRA runs, sheets, insertion and harmonise passes | section 3 pipeline (FLUX.2 LoRA, GPT Image 2.5, Nano Banana Pro, Recraft styles) | ~150 finals | – | ≈$95 |
| **fal subtotal** | | | | **$544.66** |
| Contingency (25%) | | | | $136.17 |
| **fal total** | | | | **≈$681** (34% of the ~$2,000 fal budget) |
| ElevenLabs (billed separately) | Creator plan, 1 month | SFX within the 605 included generations | $22 | $22 |
| **Grand total** | | | | **≈$703**, under the $1,000 target |

**Variants:**
- **Lean, ≈$359 on fal with contingency:**
  - lip-sync through `minimax/h3-max/lip-sync/image-to-video` at 768p, 3 takes ($25.20), plus sync-3 fix-ups ($6.93);
  - non-lip-sync on `seedance-2.0/image-to-video` at 720p ($132.74), plus upscale ($3.50);
  - klein-based image pipeline (≈$78), plus the bake-off ($40.61).
- **Premium, ≈$862 on fal with contingency:**
  - every clip finished at native 1080p through 480p drafts → `draft/complete`; non-lip-sync becomes $96.47 + $203.70;
  - premium image path (≈$150).
- **Price anchors:**
  - 10 s of Seedance 2.5 costs $2.21 at 480p, $4.73 at 720p and $11.64 at 1080p;
  - 10 s of H3 Max Lip Sync at 768p costs $0.80;
  - a sync-3 fix-up costs $1.33 per 10 s.

**Throughput:**
- The plan is about 170 video jobs.
- At an assumed 2–6 min per job, that is 3–8.5 h at the starting concurrency of 2, and 35–100 min at 10. Real Seedance 2.5 latency is [unconfirmed]; log `inference_time`.
- Buying credits raises concurrency up to 40, but the spend thresholds are unpublished.
- Submit everything to the queue and poll every 5–10 s.

### 6.6 Decisions and risks to settle in week 1

1. **Does Seedance 2.5 follow the supplied vocal or re-sing it?**
   - Signal: a low δ_audio correlation score in 6.4(a).
   - If it re-sings: use the bake-off winner for close-ups and keep Seedance for wides.
   - Either way, sync-3 is the safety net.
2. **Do fix-up models find a 2D face?** sync.so supports "human-like faces" only, and LatentSync reports "Face not detected" on cartoons.
   - Design the character with a clearly drawn, human-like mouth.
   - Confirm face detection in the bake-off before production.
3. **Does draft completion reproduce the draft?** [unconfirmed] Test once. If it doesn't, finish at 720p and upscale, which costs less anyway.
4. **Is Seedance 2.5 output 1080p?** fal's landing page and one learn article still say "up to 720p", but the schema and llms.txt price 1080p. The 6.5 budget takes the conservative case (1080p completions for the lip-sync shots). If 1080p or draft completion disappoints, the 720p + upscale path is the cheaper fallback (it saves ≈$70 on the lip-sync finals).
5. **Seeds.** 2.5 text-to-video and image-to-video have no seed input, so use reference-to-video for every character shot. Archive the prompt, refs, seed and request_id of every accepted take.
6. **Files.** Download every output at once, and set upload lifecycle to 30 d. Cut WAV excerpts from the gapless master (MP3 priming delay ≈ 23 ms ≈ half a frame).
7. **Moderation.** `content_policy_violation` (422) "may still be charged". Avoid real-person likeness and third-party IP in references and prompts.
8. **Licences.** Seedance and the other fal endpoints listed are marked commercial. ElevenLabs needs a paid plan, with the SFX sublicensing opt-out done before generating. Whether ElevenLabs terms follow outputs generated through fal is [unconfirmed].
