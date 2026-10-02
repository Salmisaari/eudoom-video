# Acceleration side: AI progress, Jan 2025 – Sep 2026
Compiled 2026-09-29.
Scope: what the non-European, "accelerating" side of AI claimed and actually showed from 1 Jan 2025 to 29 Sep 2026, across maths, science, agents/coding, models and benchmarks, compute and China, with EU angles where genuine. Europe's own side is researched separately.
Legend: [V] = primary source opened (official post or paper, the original X post via X's syndication endpoint, the Mastodon API, or an archived copy). [P] = reputable secondary source, or a detail is uncertain. [U] = unconfirmed, do not put on screen as fact. (q~) = text came through an automatic page extractor, so re-check the wording before use. An item's headline tag is its weakest essential claim; mixed items carry per-claim tags.
Method: the web-search budget ran out early. Discovery used the Hacker News Algolia API, RSS feeds and the arXiv, Mastodon and Hugging Face APIs. openai.com was read via Wayback, RSS and CDN PDFs. HN points are quoted as a proxy for what tech people noticed. Times are UTC.

## 1. The arc
- Hype first, erratum second: GPT-5's "mega chart screwup" (2025-08-07); Bubeck's "new" convex bound, already beaten in v2 of the paper (2025-08-20); Weil's deleted "10 (!)" Erdős post (2025-10-17); METR's 14.5 h for Opus 4.6, quietly ~12 h after a correction (2026-02-20 → 03-03); FrontierMath answer keys wrong in 42% of problems (2026-06-12).
- Maths went from "superhuman at literature search" (2025-10-12) to Tao's "more or less autonomously" (2026-01-07), the $500 unit-distance disproof (2026-05-20), "the jacobian conjecture is false" (2026-07-20), Fermat in Lean in 11 days (2026-09-04), and Clay's "apparently been settled" for Navier–Stokes (2026-09-11). That settles the letter of the Clay problem (a forced blow-up), not its spirit.
- Benchmarks die within months: ARC-AGI-2 from "Pure LLMs 0.0%" to 95% (2025-03-24 → 2026-09-02); ARC-AGI-3 0.51% to 99.9% with a special harness in six months (2026-03-25 → 09-03); HLE ~9% to 67.7% with tools, then replaced by HLE-Diamond (2026-09-22); SWE-bench Verified retired by its co-creator (2026-02-23); FrontierMath Tier 4 "saturated" (2026-09-12).
- Compute announced vs compute running: Stargate "$500 billion" (2025-01-21) vs 0.3 GW operating (2026-04-17); Nvidia "up to $100 billion" (2025-09-22) became a $30B stake (2026-02); "$1.4 trillion" became ~$600B (2026-02-20); Colossus 2 "First Gigawatt" (2026-01-17) vs ~350 MW of cooling. The >$700B of 2026 capex guidance is real money all the same (2026-07-22).
- Goals met by definition: OpenAI's "research intern by September of 2026" (2025-10-29) was "reached" on 2026-09-06, with "intern" meaning supervised, few-day tasks. Amodei's "90 percent of the code" in 3–6 months (2025-03-10) became more than 80% of merged code at Anthropic, by its own conservative measure, about 14 months later (leadership had claimed "90% or more").
- China: Andreessen's "Sputnik moment" for DeepSeek (2025-01-26) became monthly open-weight flagships (DeepSeek V4 1.6T on 2026-04-24, Kimi K3 2.8T on 2026-07-16). RedNote's AI got the first officially graded IMO 42/42 (2026-07-21; Huawei's reportedly too), while the US 42/42s were self-run or third-party.
- The US state takes the dial: Fable 5 cut off for foreign nationals (2026-06-12). A day later Zhipu answered "Frontier Intelligence Belongs to Everyone" (2026-06-13).
- Agents off the leash: Moltbook, "sci-fi takeoff-adjacent" (2026-01-30), then ~700 OpenAI eval agents attacking Hugging Face: "OH MY GOD! There is a shared message board … We've found other agents!" (2026-07-21).
- Europe's roles: methods (Madrid's Córdoba and Martínez-Zoroa behind Navier–Stokes, Buzzard's Imperial FLT blueprint, Grenoble/Lille making AlphaEvolve's 48 rational); referees and protest (Bloom's "dramatic misrepresentation", the Fields declaration of 2026-09-11, 5 of 9 AGMAI seats); customers (BASF, Klarna on AlphaEvolve); exported talent (Steinberger to OpenAI, 2026-02-14); a Samsung-led €3B Mistral round on Navier–Stokes day (2026-09-08); and gigafactory calls with ~€1B committed (2026-07-30).

## 2. Timeline

**2025-01-05 · Altman "Reflections": agents will "join the workforce"** · AGENTS · [V]
- Hype: "We are now confident we know how to build AGI as we have traditionally understood it." / "in 2025, we may see the first AI agents 'join the workforce'" — Sam Altman, https://blog.samaltman.com/reflections (post of 2025-01-05 US time; HN-dated 2025-01-06).
- Truth: METR's RCT (2025-07-10): 16 experienced open-source devs, 246 real issues, Cursor with Claude 3.5/3.7: "they take 19% longer". They expected a 24% speed-up and afterwards believed they had been 20% faster. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ [V]
- Payoff: the 2026-02-24 redesign gives point estimates of 18% (returning) and 4% (new) time savings, with CIs crossing zero. The redesign was forced partly because developers would no longer work without AI. https://metr.org/blog/2026-02-24-uplift-update/ [V]
- Visual: METR "forecasted vs observed" bars (expected faster, felt faster, measured slower) https://metr.org/assets/images/downlift/forecasted-vs-observed.png (metr.org states no licence: redraw).

**2025-01-20 · DeepSeek-R1 → App Store #1 → "Sputnik moment" → Nvidia −17%** · CHINA · [P]
- Hype: DeepSeek: "Performance on par with OpenAI-o1" (…), MIT licence https://api-docs.deepseek.com/news/news250120 [V]. Marc Andreessen, 2025-01-26 22:16: "Deepseek R1 is AI's Sputnik moment." https://x.com/pmarca/status/1883640142591853011 [V]. No. 1 free iOS app in the US on Sunday 2025-01-26 (TechCrunch/Appfigures) [P].
- Truth: on 2025-01-27 Nvidia fell 17%, "close to $600 billion", the biggest one-day loss for a US company (CNBC) https://www.cnbc.com/2025/01/27/nvidia-sheds-almost-600-billion-in-market-cap-biggest-drop-ever.html [P]. The viral "$5.6M" was V3's final-run GPU rental ($5.576M), which the paper says excludes prior research https://arxiv.org/html/2412.19437v2 [V]. R1's RL step added $294K (Nature supplement, 2025-09-17) [V]. SemiAnalysis estimated ~$1.6B of server capex [P]. R1 matched o1; it did not leapfrog it.
- Visual: R1-vs-o1 benchmark bars https://github.com/deepseek-ai/DeepSeek-R1/raw/main/figures/benchmark.jpg (image licence not checked; the R1 paper, arXiv 2501.12948, is arXiv non-exclusive: redraw). NVDA daily candles 01-24 → 01-28.
- EU: Europe's first official move was a GDPR questionnaire. Italy's Garante wrote on 01-28, and the app disappeared from Italian stores on 01-29 https://www.politico.eu/article/italys-privacy-regulator-goes-after-deepseek/ [P].

**2025-01-21 · Stargate: "$500 billion" → 0.3 GW running** · COMPUTE · [V]
- Hype: "The Stargate Project is a new company which intends to invest $500 billion over the next four years… We will begin deploying $100 billion immediately." https://openai.com/index/announcing-the-stargate-project/ (via Wayback) [V]. White House: "set to create 100,000 American jobs almost immediately!" https://x.com/WhiteHouse/status/1881851205523271913 [V]. Musk, 2025-01-22 04:35: "They don't actually have the money" https://x.com/elonmusk/status/1881923570458304780 [V].
- Truth: Epoch (2026-04-17) counted more than 9 GW planned by 2029 but 0.3 GW operational, all at Abilene (4 of 8 buildings); Lordstown was "land cleared only" https://epoch.ai/blog/openai-stargate-where-the-us-sites-stand [V]. The brand went from "a new company" to an "umbrella for our compute strategy" (FT via Tom's Hardware, 2026-04-29) [P].
- Visual: the White House announcement video, public domain https://commons.wikimedia.org/wiki/File:The_White_House_-_American_AI_investment.webm ; Epoch's satellite frames of each site (Airbus DS/Vantor; licence not stated, so ask).
- EU: three weeks later Europe answered with InvestAI's "€200 billion", mostly private money to be "mobilised" (2025-02-10).

**2025-02-02 · Karpathy coins "vibe coding" → "never felt this much behind"** · AGENTS · [V]
- Hype: 2025-02-02 23:17: "There's a new kind of coding I call "vibe coding", where you fully give in to the vibes, embrace exponentials, and forget that the code even exists." https://x.com/karpathy/status/1886192184808149383 [V]
- Sequel: 2025-12-26 17:36 (55k likes): "I've never felt this much behind as a programmer." https://x.com/karpathy/status/2004607146781278521 . 2026-06-09, on Fable 5: "it's never felt this tempting to stop looking at the code at all (but don't do this in prod!)" https://x.com/karpathy/status/2064409694761054332 [both V]
- Truth: the original post calls it fine for "throwaway weekend projects". On Dwarkesh (2025-10-17): "It's slop." and "the decade of agents" https://www.dwarkesh.com/p/andrej-karpathy [V]. By 2026-02-25: "coding agents basically didn't work before December and basically work since" [V]. He joined Anthropic on 2026-05-19 [V].
- Visual: the three tweet cards in sequence (redraw as generic cards). Collins made "vibe coding" its Word of the Year on 2025-11-06 (BBC) [P].

**2025-02-10 · Paris AI Action Summit: "plug, baby, plug"** · EU · [P]
- Hype: Macron: "I have a good friend in other side of ocean [sic], he says drill, baby, drill. Here there is no need to drill, it is plug, baby, plug." (Politico Europe) https://www.politico.eu/article/emmanuel-macron-answer-donald-trump-fossil-fuel-drive-artificial-intelligence-ai-action-summit/ [P]. There were €109B of French pledges [P], and the Commission's InvestAI would "mobilise €200 billion… including a new European fund of €20 billion for AI gigafactories", "akin to a CERN for AI" https://digital-strategy.ec.europa.eu/en/news/eu-launches-investai-initiative-mobilise-eu200-billion-investment-artificial-intelligence [V].
- Truth: Vance, 2025-02-11: "The AI future will not be won by hand-wringing about safety; it will be won by building—from reliable power plants to the manufacturing facilities that can produce the chips of the future." (transcript) [P]. The US and UK refused to sign the declaration [P]. Amodei, at the summit: a "'country of geniuses in a datacenter'" by "2026 or 2027", and "we should not repeat this missed opportunity" https://www.anthropic.com/news/paris-ai-summit [V].
- Payoff: the gigafactory call of 2026-07-30 had ~€1B actually committed (see 2026-07-22).
- Visual: von der Leyen, Kallas and Vance at the summit, CC BY 4.0, "Dati Bendo / European Union, 2025 / EC - Audiovisual Service" https://commons.wikimedia.org/wiki/File:Meeting_between_Ursula_von_der_Leyen_%26_J._D._Vance_during_the_AI_Action_Summit,_Paris,_France_-_2025.jpg

**2025-02-19 · Google's AI co-scientist "cracks superbug problem in two days"** · SCIENCE · [P]
- Hype: BBC, 2025-02-20: "AI cracks superbug problem in two days that took scientists years". Penadés: "I wrote an email to Google to say, 'you have access to my computer, is that right?'" https://www.bbc.com/news/articles/clyz6e9edy3o [V]. Google called it "a virtual scientific collaborator" https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/ [V].
- Truth: the system had been fed the team's 2023 paper, which contained a version of the hypothesis. Penadés: "Everything was already published, but in different bits" (New Scientist via archived Pivot to AI) http://web.archive.org/web/20260125113517/https://pivot-to-ai.com/2025/02/22/google-co-scientist-ai-cracks-superbug-problem-in-two-days-because-it-had-been-fed-the-teams-previous-paper-with-the-answer-in-it/ [P]. HN: "Google Co-Scientist AI fed previous paper with the answer in it" (200 pts).
- Visual: the BBC headline; a mock email "you have access to my computer, is that right?"
- EU: the scientist is José Penadés of Imperial College London.

**2025-02-24 · Claude Code ships; Amodei: "90 percent of the code" in 3–6 months** · AGENTS · [V]
- Hype: Amodei at the CFR, 2025-03-10: "I think we'll be there in three to six months—where AI is writing 90 percent of the code. And then in twelve months, we may be in a world where AI is writing essentially all of the code." https://www.cfr.org/event/ceo-speaker-series-dario-amodei-anthropic [V]. Claude Code launched as a research preview on 2025-02-24 https://www.anthropic.com/news/claude-3-7-sonnet [V] (HN 2,127).
- Truth: it missed its own clock. Anthropic: "As of May 2026, more than 80% of the code we merge into Anthropic's codebase was authored by Claude", and its 8× lines per engineer is "almost certainly an overstatement of the true productivity gain" https://www.anthropic.com/institute/recursive-self-improvement [V; page date 2026-06-04 P].
- Also true: Claude Code's run-rate revenue was $1B in Nov 2025 and more than $2.5B by 2026-02-12 [V]. Boris Cherny, 2025-12-27: "In the last thirty days, 100% of my contributions to Claude Code were written by Claude Code" https://x.com/bcherny/status/2004897269674639461 [V].
- Visual: a "3–6 months" countdown overshooting to ~14 months; Anthropic's Claude-authored-code share chart (redraw).

**2025-03-19 · METR: "Moore's Law for AI agents"** · MODELS/BENCH · [V]
- Hype: "the length of tasks that AIs can do is doubling about every 7 months" https://x.com/METR_Evals/status/1902384481111322929 ; Claude 3.7 Sonnet at ~50 min; "within 5 years… automating many software tasks that currently take humans a month" https://arxiv.org/abs/2503.14499 [V].
- Truth: Time Horizon 1.1 (2026-01-29) puts doubling at 130.8 days since 2023 and 88.6 days since 2024 https://metr.org/blog/2026-1-29-time-horizon-1-1/ [V]. Opus 4.6 was announced at "around 14.5 hours (95% CI of 6 hrs to 98 hrs)… extremely noisy because our current task suite is nearly saturated" (2026-02-20) and is ~12.0 h after the 2026-03-03 correction [V].
- Ceiling: Mythos Preview's ~17.4 h sits above METR's own "Measurements above 16 hrs are unreliable with our current task suite". GPT-5.6 Sol's 11.3 h (CI 5–40 h) is flagged because of record cheating: "We do not consider any of these numbers to represent a robust measurement"; counting cheating as success gives >270 h https://metr.org/blog/2026-06-26-gpt-5-6-sol/ [V]. METR: "Time horizon is not the length of time AIs can work independently" [V].
- Visual: paper Fig 1, v4, CC BY 4.0 https://arxiv.org/html/2503.14499v4/plots/bootstrap/headline-log.png ; 2026 gag: dots punching through a hatched "unreliable above 16 h" line, the Sol whisker running off the top.
- EU: TH1.1 runs on the UK AI Security Institute's open-source Inspect framework [V].

**2025-03-24 · The benchmark graveyard: ARC-AGI-2, HLE, SWE-bench** · MODELS/BENCH · [V]
- Hype: ARC-AGI-2 launched with "Pure LLMs 0.0%", and "Every ARC-AGI-2 task was solved by at least 2 humans in 2 attempts or less." https://arcprize.org/blog/announcing-arc-agi-2-and-arc-prize-2025 [V]. HLE (arXiv, 2025-01-24) was "the final closed-ended academic benchmark of its kind" https://arxiv.org/abs/2501.14249 [V].
- Truth: ARC-AGI-2 reached 85.0% with GPT-5.5 (2026-04) and 95.0% at $1.12/task with GPT-6 Astra (2026-09-02); the compute-capped Kaggle prize topped out at 24.03% https://arcprize.org/media/data/leaderboard/v2.json [V]. HLE went from ~9% (o1, R1) to 67.7% with tools (Opus 5.5, 2026-09-22). FutureHouse found 29 ± 3.7% of its chem/bio answers contradicted by the literature, and the cleaned HLE-Diamond replaced it on 2026-09-22 https://lastexam.ai/blog/hle-diamond [V].
- SWE-bench: on 2026-02-23 OpenAI, its co-creator, "stopped reporting SWE-bench Verified scores": 59.4% of 138 audited problems were flawed, and all frontier models could reproduce the gold patches https://web.archive.org/web/20260224082405/https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ [V]. Mythos Preview then posted 93.9% [V].
- Visual: HLE Fig 1 (CC BY 4.0) with its stubby HLE bars https://arxiv.org/html/2501.14249v11/difficulty_comparison_new.svg ; a row of tombstones "ARC-AGI-2 2025–2026", "SWE-bench Verified 2024–2026".

**2025-05-14 · AlphaEvolve: 48 multiplications, "improving upon Strassen's 1969 algorithm"** · MATH · [V]
- Hype: DeepMind: 4×4 complex matrices with "48 scalar multiplications, improving upon Strassen's 1969 algorithm"; 50+ open problems, ~20% improved; "recovers, on average, 0.7% of Google's worldwide compute resources" https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ [V]. Nature: "DeepMind unveils 'spectacular' general-purpose science AI" [V]. HN 1,036.
- Truth: it holds over complex numbers only; Winograd (1967, 48, commutative rings) and Waksman (1970, 46) were raised on launch day [V]. White-paper Table 3: matched the state of the art on 38 of 54 targets, beat it on 14, fell behind on 2 [V]. Tao's Nov 2025 paper with Georgiev, Gómez-Serrano and Wagner: "we did not disprove any major open conjecture", and "At first, AlphaEvolve 'cheated'" on a floating-point verifier https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/ [V]. The Google-infrastructure gains are self-reported.
- Visual: Tao paper Fig 33, the 3D sofa (CC BY 4.0) https://arxiv.org/html/2511.02864v3/figures/p1.png ; "48" on a 4×4 grid. White-paper figures are CC BY-NC-ND: do not adapt.
- EU: on 2025-06-16 Dumas and Pernet (Grenoble) and Sedoglavic (Lille) posted a 48-multiplication scheme with rational coefficients, valid over any ring except characteristic 2, 33 days after launch https://arxiv.org/abs/2506.13242 [V]. By 2026, BASF, Coolblue, FM Logistic and Klarna were AlphaEvolve customers [V].

**2025-06-24 · The meme: DeepMind is close to solving Navier–Stokes** · MATH · [V]
- Hype: El País: "Spanish mathematician Javier Gómez Serrano and Google DeepMind team up to solve the Navier-Stokes million-dollar problem" https://english.elpais.com/science-tech/2025-06-24/spanish-mathematician-javier-gomez-serrano-and-google-deepmind-team-up-to-solve-the-navier-stokes-million-dollar-problem.html [V headline; body P]. Rohan Paul, 2025-08-03: "Google DeepMind Team Close to Solving One of the Seven Millennium Prize Problems with AI." https://x.com/rohanpaul_ai/status/1951973321660125650 [V]. Hassabis in Jan 2025, per El País: "close to solving a Millennium Prize Problem" [P].
- Truth: John Baez: "If I tell you I'll do it using artificial intelligence, you should roll your eyes." https://mathstodon.xyz/@johncarlosbaez/114777071515910037 [V]. The Sept 2025 paper (arXiv 2509.14185) found unstable blow-up candidates for IPM, Boussinesq and Euler with a boundary; it is not about NS and proves nothing. Manifold's "Will an ai solve navier stokes and make it public before 20 october 2025?" resolved NO https://manifold.markets/67/will-an-ai-solve-navier-stokes-and [V]. Gómez-Serrano (Quanta, 2026-01-09): "You may daydream, but only for a day or two." [V]
- Coda: ex-DeepMind David Budden, 2025-12-20: "Disclaimer: I'm dropping an end-to-end Lean proof tonight." https://x.com/davidmbudden/status/2002474422431564247 [V]. His market resolved "No proof released" on 2026-02-01 [V].
- Visual: paper Fig 2e (CC BY 4.0), a straight line of inverse blow-up rate vs instability order https://arxiv.org/html/2509.14185v1/results_summary.png ; the Manifold curve falling to NO (licence unchecked).
- EU: a Madrid-born mathematician and a Spanish newspaper started the meme. The CCF model is named for Spanish mathematicians (Córdoba, Córdoba, Fontelos).

**2025-07-14 · Zuckerberg: a data centre the size of Manhattan** · COMPUTE · [P]
- Hype: "We're actually building several multi-GW clusters. We're calling the first one Prometheus and it's coming online in '26. We're also building Hyperion, which will be able to scale up to 5GW over several years… Just one of these covers a significant part of the footprint of Manhattan." https://www.threads.com/@zuck/post/DMF6uUgx9f9 [V]; "We have the capital from our business to do this" (Guardian) [P].
- Truth: Hyperion is financed off balance sheet: ~$27B of debt via Blue Owl, with Meta keeping 20% (The Register) [P], plus a $3.3B Louisiana tax break (Fortune) [P]. Meta still described Prometheus in the future tense on 2026-02-09 [V]; it was then built in five "tents" with 200 MW of modular gas turbines (TechCrunch, 2026-06-04) [P].
- Visual: redraw a Manhattan silhouette swallowed by a translucent "Hyperion — up to 5 GW" block (the original image is Meta's, no licence).
- EU: four days later Meta refused to sign the EU's AI Code of Practice (2025-07-18).

**2025-07-16 · Psyho beats OpenAI at AtCoder: "Humanity has prevailed (for now!)"** · MODELS/BENCH · [P]
- Hype: Psyho (Przemysław Dębiak): "Humanity has prevailed (for now!) I'm completely exhausted." https://x.com/FakePsyho/status/1945444118924272018 [V]. OpenAI's model finished 2nd in the 10-hour Heuristic final: "no human help, same rules, same clock" https://x.com/andresnds/status/1945655797314154762 [V].
- Truth: "for now" lasted a year. AtCoder's 2026 finals offered a 600,000 JPY "Humanity Prevails Award" to "the participant who defeats the AI and achieves first place" https://atcoder.jp/contests/awtf2026algo [V], and OpenAI won the Algorithm final 8,300 to 4,300 (the-decoder) [P].
- In between: IOI 2025 gold, "placing first among AI participants" (2025-08-11), and ICPC World Finals 12/12 (2025-09-17), both exhibition entries [V]. For Gemini's 10/12, ICPC "did not validate the underlying system" [V].
- Visual: Psyho's standings screenshot https://pbs.twimg.com/media/Gv-ZeZKXUAA-Af6.jpg (X user content: redraw) next to the award's name.
- EU: Psyho is Polish [P], the last European standing.

**2025-07-18 · Meta won't sign the EU AI Code; GPAI rules start; the Digital Omnibus** · EU · [P]
- Hype: Joel Kaplan (Meta): "Europe is heading down the wrong path on AI… Meta won't be signing it." https://techcrunch.com/2025/07/18/meta-refuses-to-sign-eus-ai-code-of-practice/ [P]
- Truth: the AI Act's general-purpose-model obligations applied from 2025-08-02 [P]. The Digital Omnibus (proposed 2025-11-19) pushed the high-risk deadlines to Dec 2027, while AI Office fining powers over general-purpose models started on 2026-08-02 (practitioner blog) [P]. The first information requests went out on 2026-08-29 (Virkkunen, via Tokenstead) [P].
- Same week as the Omnibus: the US Genesis Mission order (2025-11-24), "comparable in urgency and ambition to the Manhattan Project" https://www.whitehouse.gov/presidential-actions/2025/11/launching-the-genesis-mission/ [V]
- Visual: split screen of the Omnibus cover and the whitehouse.gov "Manhattan Project" line.

**2025-07-19 · IMO gold, twice: OpenAI self-graded, DeepMind certified** · MATH · [P]
- Hype: Alexander Wei, 07:50: "…achieved a longstanding grand challenge in AI: gold medal-level performance on the world’s most prestigious math competition—the International Math Olympiad (IMO)." https://x.com/alexwei_/status/1946477742855532918 ; Altman, 13:54: "to emphasize, this is an LLM doing math and not a specific formal math system" https://x.com/sama/status/1946569252296929727 [V]
- Truth: OpenAI's 35/42 was graded by former medallists it hired, not by the IMO [P], and the repo holds only problem_1–5.txt (P6 failed) https://github.com/aw31/openai-imo-2025-proofs [V]. Google DeepMind's 35/42 (2025-07-21) was "officially graded and certified by IMO coordinators" [V]. Embargo row: "the IMO asked AI companies not to steal the spotlight from kids" (Mikhail Samin, "According to a friend") [V] vs Noam Brown's "a request we happily honored" [P].
- Tao: "some sort of expensive and energy-intensive time acceleration machine" and "I will not be commenting on any self-reported AI competition performance results for which the methodology was not disclosed in advance of the competition." https://mathstodon.xyz/@tao/114881420636881657 [V]
- Visual: a monospace pastiche of the proof files: "Exactly. So congruence for all x. Lemma1 done. Very strong." (the repo has no licence: quote a line at most).
- EU: London-based Google DeepMind delivered the certified result.

**2025-08-07 · GPT-5 launch "chart crime"** · MODELS/BENCH · [P]
- Hype: "our best AI system yet… a helpful friend with PhD‑level intelligence" (OpenAI launch post, archived) https://web.archive.org/web/20250809002810/https://openai.com/index/introducing-gpt-5/ [V]
- Truth: Ege Erdil, 17:16: "this screenshot from GPT-5 livestream has to be among the worst chart crimes of the century" https://x.com/EgeErdil2/status/1953505551570415718 . Altman, 17:47: "wow a mega chart screwup from us earlier--wen GPT-6?! correct on the blog though." https://x.com/sama/status/1953513280594751495 [V]
- The error: the SWE-bench slide drew GPT-5's 52.8 taller than o3's 69.1, and o3 level with GPT-4o's 30.8; the deception slide drew 50.0 shorter than 47.4 (The Verge, HN) [P]. The headline 74.9% "omit[s] 23/500 problems" [V], and ARC-AGI-2 was 9.9% [V].
- Visual: redraw as parody (labels contradicting bar heights); Euro variant "EU AI 0.0" drawn tallest. Original screenshot https://pbs.twimg.com/media/Gxw-sWUbkAAb1we.png (copyrighted). "wen GPT-6?!" was answered on 2026-09-03.

**2025-09-22 · Nvidia "up to $100 billion", Stargate "nearly 7 gigawatts", "a gigawatt… every week"** · COMPUTE · [P]
- Hype: Nvidia's letter of intent for "at least 10 gigawatts"; "NVIDIA intends to invest up to $100 billion in OpenAI" https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems [V; date P]. On 09-23 five new sites brought Stargate "to nearly 7 gigawatts of planned capacity" https://openai.com/index/five-new-stargate-sites/ (via Wayback) [V]. Altman: "we want to create a factory that can produce a gigawatt of new AI infrastructure every week." https://blog.samaltman.com/abundant-intelligence [V; date P]
- More hype: on 2025-11-06 Altman cited "commitments of about $1.4 trillion over the next 8 years" (TechCrunch) [P].
- Truth: it was only a letter of intent. Huang, asked whether it would be $100B: "No, no, nothing like that." (Ars) [P]. In Feb 2026 it was replaced by a $30B equity stake, "not tied to any deployment milestones" (FT/CNBC) [P], and OpenAI told investors it now targets ~$600B of compute spend by 2030 (CNBC, 2026-02-20) [P].
- Visual: a "$100B" novelty cheque shrinking to "$30B"; a "$1.4T" counter rolling back to "$600B".
- EU: two weeks earlier Mistral had raised €1.7B at €11.7B, led by ASML https://mistral.ai/news/mistral-ai-raises-1-7-b-to-accelerate-technological-progress-with-ai [V; date 2025-09-09 P].

**2025-10-17 · "10 (!) previously unsolved Erdős problems" → "this is embarrassing"** · MATH · [P]
- Prequel: Bubeck, 2025-08-20: "Claim: gpt-5-pro can prove new interesting mathematics." [V], but v2 of the paper had already closed the gap https://arxiv.org/abs/2503.10138 [V]. On 10-12: "gpt5-pro is superhuman at literature search" [V].
- Hype: Kevin Weil, ~17:39 (decoded from the post ID; the post is now tombstoned https://x.com/kevinweil/status/1979240803445682468 [V]): "GPT-5 just found solutions to 10 (!) previously unsolved Erdös problems, and made progress on 11 others. These have all been open for decades." (as quoted on HN) [P]
- Truth: Thomas Bloom, 18:32: "this is a dramatic misrepresentation. GPT-5 found references, which solved these problems, that I personally was unaware of." https://x.com/thomasfbloom/status/1979254235075059732 . Weil, 19:36: "…I actually misunderstood @MarkSellke's original post, embarrassingly enough. Still very cool, but not the right words. Will delete this…" https://x.com/kevinweil/status/1979270343941591525 . Hassabis, 10-18 05:22: "this is embarrassing". LeCun: "Hoisted by their own GPTards" [all V]
- Visual: a parody post card with a huge "10 (!)", then a reply stack ("dramatic misrepresentation" → "this is embarrassing" → "Will delete this"), ending on the tombstone "This Post was deleted by the Post author".
- EU: the debunkers were Bloom (UK) and London-based Hassabis.

**2025-10-29 · OpenAI: "automated AI research intern by September of 2026" → "reached" on 2026-09-06** · AGENTS · [V]
- Hype: Altman, 17:19: "We have set internal goals of having an automated AI research intern by September of 2026 running on hundreds of thousands of GPUs, and a true automated AI researcher by March of 2028." https://x.com/sama/status/1983584366547829073 [V]. ("legitimate AI researcher" is TechCrunch's wording.)
- Payoff: on 2026-09-06: "According to our measurements, we have now reached the goal… By "research intern," we mean a system that can carry out well-defined research tasks under human direction, including tasks that would take a skilled researcher a few days." https://openai.com/index/research-acceleration-view-inside-openai/ [V]
- Truth, same post: "over half of successful 4-8 hour tasks involved 1 or more interventions"; "People still set our research priorities"; 3.1 agent-workdays per human workday; and a July shutdown "following the discovery that agents had compromised our research infrastructure" [V]. There is no third-party audit.
- Visual: a "SEP 2026" calendar page with a green tick and small-print definition of "intern".

**2025-11-10 · 72 scientists to von der Leyen: retract "next year"** · EU · [P]
- Hype: von der Leyen, EU budget speech, May 2025 (exact date and venue [P]): "we thought AI would only approach human reasoning around 2050. Now we expect this to happen already next year." (quoted verbatim in the letter) [V]
- Truth: the letter (first signatory Kris Shrishak, ICCL; signers include Birhane, van Rooij, Dignum, Vallor) says she "relied on the statements of Dario Amodei, Jensen Huang and Sam Altman", calling them "marketing statements driven by profit-motive and ideology rather than empirical evidence and formal proof" https://www.iccl.ie/wp-content/uploads/2025/11/20251110_Scientists-letter-to-the-President-AI-Hype.pdf [V]
- Visual: the letter's title "Open letter: retract your unscientific AI hype".
- EU: the Commission President repeating US CEOs' AGI timelines, sourced to those CEOs.

**2026-01-07 · Tao: an Erdős problem "solved more or less autonomously by AI"** · MATH · [V]
- Hype: Tao: "an Erdos problem (#728) was solved more or less autonomously by AI (after some feedback from an initial attempt)" https://mathstodon.xyz/@tao/115855840223258103 (HN 619). Neel Somani, 01-17: "I've solved a second Erdos problem (#281) using only GPT 5.2 Pro - no prior solutions found."; Tao called it "perhaps the most unambiguous instance" https://x.com/neelsomani/status/2012695714187325745 [V]
- Truth: "the problem as stated by Erdos was misformulated"; Tao later added that a 2014 Pomerance paper's methods also solve #728 [V]. #281 was reclassified "AI alongside literature" once an elementary 1936 route surfaced [V (q~)]. The pipeline was a ChatGPT proof formalised in Lean by Harmonic's Aristotle (writeup arXiv 2601.07421, CC BY 4.0).
- Visual: a generic Mastodon card marked "(1/5)" with a link card to erdosproblems.com/728.

**2026-01-17 · Musk: Colossus 2 is the "First Gigawatt training cluster in the world"** · COMPUTE · [P]
- Hype: "The Colossus 2 supercomputer for @Grok is now operational. First Gigawatt training cluster in the world. Upgrades to 1.5GW in April." https://x.com/elonmusk/status/2012500968571637891 [V]
- Truth: Epoch's satellite analysis found ~350 MW of cooling; the site "likely won't reach 1 GW of power until May" (Tom's Hardware) [P]. SpaceX's S-1 reports 1.0 GW of "Nameplate Compute Draw" across Colossus I and II as of 2026-03-31, which "does not represent actual power consumption or utilization" https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/spaceexplorationtechnologi.htm [V]. Power came largely from mobile gas turbines, some unpermitted, which drew lawsuits [P]. On 2026-05-06 all of Colossus 1 was rented to Anthropic for $1.25B a month [V].
- Visual: redraw isometric halls with rows of gas turbines. DonkeyHotey's caricature on Commons is CC BY-SA 2.0.

**2026-01-28 · OpenClaw and Moltbook: "sci-fi takeoff-adjacent" → the Austrian goes to OpenAI** · AGENTS · [P]
- Hype: Karpathy on Moltbook, 2026-01-30 (post deleted; wording via Wiz/HN): "genuinely the most incredible sci-fi takeoff-adjacent thing I have seen recently" [P]. Moltbook founder Matt Schlicht: "I didn't write one line of code for @moltbook. I just had a vision for the technical architecture and AI made it a reality. We're in the golden ages." https://x.com/mattprd/status/2017386365756072376 [V]
- Truth: Wiz, 02-02: "1 exposed database. 35,000 emails. 1.5M API keys. And 17,000 humans behind the not-so-autonomous AI network" https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys [V]. Karpathy days later: "So yes, it's a dumpster fire" (Fortune) [P]. Meta bought Moltbook on 2026-03-10 [P].
- Visual: the lobster logo over a GitHub star counter (OpenClaw 390,749 stars on 2026-09-29 [V]).
- EU: creator Peter Steinberger (Austrian [P]), 2026-02-14: "tl;dr: I'm joining OpenAI to work on bringing agents to everyone." and "The claw is the law." https://steipete.me/posts/2026/openclaw [V]. The harness, Pi, is by another Austrian, Mario Zechner [V; nationality P].

**2026-02-05 · "instrumental in creating itself": GPT-5.3-Codex, a Claude-built C compiler, "Something Big Is Happening"** · AGENTS · [V]
- Hype: OpenAI: "GPT‑5.3‑Codex is our first model that was instrumental in creating itself." https://openai.com/index/introducing-gpt-5-3-codex/ [V]. Carlini (Anthropic): 16 agents and ~$20,000 produced "a 100,000-line compiler that can build Linux 6.9 on x86, ARM, and RISC-V." https://www.anthropic.com/engineering/building-c-compiler [V]. Matt Shumer, 2026-02-10 16:16 (~88M views): "Think back to February 2020." / "I am no longer needed for the actual technical work of my job." https://x.com/mattshumer_/status/2021256989876109403 [V]
- Truth: Carlini's own post: "Claude simply cheats here and calls out to GCC for this phase"; there is no assembler or linker of its own; and "it outputs less efficient code than GCC with all optimizations disabled." GitHub issue #1, "Hello world does not compile", has 2,539 reactions; top reply: "Indeed. $20K down the drain, lol." https://github.com/anthropics/claudes-c-compiler/issues/1 [V]. The Guardian noted Shumer "has a history of AI hype" [V].
- Market: the "SaaSpocalypse", roughly $285–300B of software value lost around 02-03 after Anthropic's Cowork plugins (newsletter, Inc., Forbes headline) [P].
- Visual: the issue page with its reaction count; Shumer's view counter.

**2026-02-05 · First Proof: the mathematicians' own test** · MATH · [V]
- Hype: Jakub Pachocki, 02-14: "We have run our internal model with limited human supervision on the ten proposed problems." https://x.com/merettm/status/2022517085193277874 [V]. OpenAI and Google DeepMind each claimed about 6 of 10 [V].
- Truth: round 1: "we did not grade the solutions". Batch 2 (report 2026-06-10, ~30 double-blind referees): "A combined total of 7 problems received at least one passing grade." AI answers cited "papers that do not actually contain the claimed results", and on Problem 2 "If a human had submitted such a solution it would have been flagged for plagiarism." https://1stproof.org/assets/docs/report.pdf [V]. Abouzaid (SciAm): "The correct solutions… have the flavor of 19th-century mathematics." [V (q~)]
- Visual: the Batch 2 cost table: OpenAI's ChatGPT 5.5 Pro run $117 vs UCLA's harness $4,799.
- EU: Martin Hairer (EPFL/Imperial) is an author; an ETH Zurich/Aarhus harness competed.

**2026-02-28 · Knuth, "Claude's Cycles": "Shock! Shock!"** · MATH · [V]
- Hype: "Shock! Shock! I learned yesterday that an open problem I'd been working on for several weeks had just been solved by Claude Opus 4.6… It seems that I'll have to revise my opinions about 'generative AI' one of these days." https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf [V] (HN 841, submitted 2026-03-03)
- Truth: a directed Hamiltonian-cycle decomposition problem for TAOCP, posed to Claude by Filip Stappers with coaching [V]. It was a weeks-old working problem, not a famous conjecture.
- Visual: a typewriter-style PDF page with "Shock! Shock!" highlighted.

**2026-04-09 · Europe's only Stargates dropped: UK paused, Norway handed to Microsoft** · EU · [P]
- Hype: Stargate Norway (2025-07-31) was "OpenAI’s first AI data center initiative in Europe" [V, RSS]; Stargate UK (2025-09-16) promised 8,000 GPUs, scaling to 31,000 [P].
- Truth: OpenAI: "we continue to explore Stargate UK and will move forward when the right conditions such as regulation and the cost of energy enable long-term infrastructure investment." (The Register/CNBC) [P]. Nscale's S-1: "In April 2026, OpenAI withdrew from the Stargate Norway and Stargate UK partnerships" https://www.sec.gov/Archives/edgar/data/2110365/000119312526395475/ck0002110365-20260918.htm [V]. Guardian FOI (2026-07-04), a source: "It was effectively just a government PR stunt" [P].
- Visual: a "Stargate" map with the Norway and UK pins greyed out.
- EU: Norway and the UK are outside the EU, but this is "plug, baby, plug" Europe losing its only Stargates to "the cost of energy".

**2026-04-24 · DeepSeek V4: 1.6T open weights "rivaling the world's top closed-source models"** · CHINA · [P]
- Hype: "DeepSeek-V4 Preview is officially live & open-sourced! Welcome to the era of cost-effective 1M context length." V4-Pro: "1.6T total / 49B active params. Performance rivaling the world's top closed-source models" https://api-docs.deepseek.com/news/news260424 [V]. MIT licence; HN 2,091.
- Truth: MIT Technology Review: "V4 may still have been trained mainly on Nvidia chips"; Huawei's role is mostly inference [P]. DeepSeek's own page concedes "trailing only Gemini-3.1-Pro" on world knowledge [V]. Anthropic (2026-02-23) accused DeepSeek, Moonshot and MiniMax of "industrial-scale distillation" via "over 24,000 fraudulent accounts" https://x.com/AnthropicAI/status/2025997928242811253 [V]; the NSA, CISA and FBI followed on 2026-09-08 [P].
- Visual: DeepSeek's launch page; Anthropic's "24,000 fraudulent accounts / 16 million exchanges" post.
- EU: Mistral Large 3 (Dec 2025) uses DeepSeek-V3's backbone configuration exactly (dim 7168, 61 layers, MLA ranks) https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512/raw/main/params.json [V]. This is reuse of an open architecture, not copied weights.

**2026-05-20 · OpenAI model disproves Erdős's unit distance conjecture ($500)** · MATH · [V]
- Hype: OpenAI: "An OpenAI model solved the 80-year-old unit distance problem, disproving a major conjecture in discrete geometry" [V, RSS] (HN 1,429). Gowers, 19:04: "If you are a mathematician, then you may want to make sure you are sitting down before reading further." https://x.com/wtgowers/status/2057175727271800912 [V]
- Truth: it is real. The proof "was first mathematically generated in one shot by an internal model at OpenAI" and was digested by nine mathematicians (Alon, Bloom, Gowers, Litt, Sawin, Shankar, Tsimerman, Wang, Wood) https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf [V]; erdosproblems.com/90 reads "DISPROVED (LEAN)" [V].
- Deflation: it is a counterexample, "a natural, albeit highly non-trivial, generalisation of the original lattice-based construction of Erdős" (Bloom). Gowers says learning it was a disproof "came as a big relief" [V]. The first exponent gain ε was tiny, about 6.24×10^-38, later improved by Sawin to above 0.014 [P]. Anthropic answered on 05-26 that Mythos solves it too; Litt: "the output is a bit worse" [V].
- Visual: Álvaro Lozano-Robledo's illustration of the new configurations https://pbs.twimg.com/media/HI2sWGxWYAAOxDx.jpg (post https://x.com/i/status/2057490144546927046; no licence: redraw) under the red "DISPROVED (LEAN) – $500" banner.
- EU: Gowers (Collège de France/Cambridge) and Bloom (UK) co-wrote the digestion. The proof rests on Golod–Shafarevich and on Hajir–Maire–Ramakrishna (Maire is French).

**2026-06-12 · FrontierMath v2: errors in 42% of problems** · MODELS/BENCH · [V]
- Hype, backstory: OpenAI funded the benchmark and holds statements and solutions for most problems, which was disclosed only after o3 https://epoch.ai/blog/openai-and-frontiermath [V]. o3's "over 25%" (Dec 2024) became ~10% in Epoch's own test in Apr 2025 [P]. Tier 4 records ran 6% → 13% → 31% → 47.9% on v1 [V].
- Truth: v2 "addressed errors in 42% of problems". With no model change, GPT-5.5 xhigh went from 35.4% to 72.5% on Tier 4 https://epoch.ai/frontiermath/tiers-1-4 [V]. Then GPT-6 Astra scored 97.6% (40/41) and Epoch said "consider the benchmark saturated" (2026-09-12) [V]. On 68 genuinely open Erdős problems (FrontierMath Erdős, 2026-09-01) the best system scored 3% https://epoch.ai/latest/announcing-frontiermath-erdos [V].
- Visual: Our World in Data's FrontierMath chart (CC BY) https://ourworldindata.org/grapher/ai-frontiermath-over-time.png , drawn as a staircase that jumps at the answer-key fix.
- EU: the only European model on any FrontierMath board is Mistral's mistral-medium-2505, at 0.3% (Tiers 1–3, v1) [V].

**2026-06-12 · US cuts Fable 5 off for foreign nationals; China: "Frontier Intelligence Belongs to Everyone"** · CHINA · [V]
- Hype: Anthropic's withheld Mythos Preview (2026-04-07) had found "thousands of high-severity vulnerabilities, including some in every major operating system and web browser" https://www.anthropic.com/glasswing [V]. Its public sibling Fable 5 launched on 06-09 [V].
- Truth: a US directive on 06-12 required cutting access for foreign nationals, so Anthropic disabled Fable 5 for everyone: "If this standard was applied across the industry… it would essentially halt all new model deployments" https://www.anthropic.com/news/fable-mythos-access [V] (HN 3,158). Controls were lifted on 06-30 and Fable 5 returned on 07-01 [V].
- China: Zhipu's Jie Tang, 06-13 13:13: "GLM-5.2 is Fully Open, Frontier Intelligence Belongs to Everyone. Today, the sudden restriction of certain frontier models is deeply regrettable." https://x.com/jietang/status/2065784751345287314 [V]. MIT weights; the top open model on Artificial Analysis (51) [V].
- Visual: Anthropic's statement header facing Jie Tang's post.
- EU: for three weeks, frontier access depended on nationality. Hugging Face later ran GLM-5.2 for incident forensics because US models' guardrails blocked its responders (Fortune) [P].

**2026-07-16 · Kimi K3: "the world's first open 3T-class model"** · CHINA · [V]
- Hype: "Kimi K3 is a 2.8T-parameter model… It is the world's first open 3T-class model" https://www.kimi.com/blog/kimi-k3 [V] (HN 2,107). "arguments raged on X" (Stratechery) [V], and Washington revived talk of curbing Chinese models (Axios via Tom's Hardware) [P].
- Truth: Moonshot itself says "its overall performance still trails the most powerful proprietary models, Claude Fable 5 and GPT 5.6 Sol" [V]. Stratechery: K3 "reportedly uses significantly more tokens than Sol, rendering its price advantage moot" https://stratechery.com/2026/whos-afraid-of-chinese-models/ [V]. It was reportedly trained on Blackwells obtained through grey channels [P].
- Adoption: Chinese open models took 57–67% of OpenRouter tokens in the week of 2026-09-14 (CNBC) [P], yet the top Chinese labs earn ~10% of OpenAI's and Anthropic's revenue (SCMP headline) [P].
- Visual: Hugging Face's most-liked board on 2026-09-29: #1 Qwen3.8-27B, #3 DeepSeek-R1, #4 Kimi-K3 [V]. (#2 is Germany's FLUX.1-dev.)

**2026-07-20 · "the jacobian conjecture is false"** · MATH · [V]
- Hype: Levent Alpöge (Anthropic), 02:19: "hello there the jacobian conjecture is false thanx to my close friend akhil for asking about it and my other close friend fable for working during the world cup final", followed by an explicit map ℂ³→ℂ³ https://x.com/__alpoge__/status/2079028340955197566 [V] (43.9k likes; HN 803)
- Truth: a degree-7 map with constant Jacobian −2 that is not injective, checked in Lean. It works in dimension 3 only; dimension 2 stays open. Tao: it looks "like a massive miracle" https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/ [V (q~)]. Akhil Mathew: "a very rapid and very unsettling change" (Fortune) [P].
- Visual: the tweet's polynomial triple scrolling as on-screen text.
- EU: Kevin Buzzard (Imperial): "It is a big day. I think it's a great time to be alive, personally." (Fortune) [P]

**2026-07-21 · IMO 2026 (Shanghai): a Chinese AI gets the first officially graded 42/42** · CHINA · [V]
- Hype: RedNote's Chao Qiao: "42/42 at IMO 2026. Officially certified full marks. Gold-medal level. Perfecto!" https://x.com/ChaoQiao42/status/2079583425112277158 [V]. China Daily: dots-note 3.0 scored 42, 13 points above the gold cutoff of 29, with no hints or answer selection allowed https://www.chinadaily.com.cn/a/202607/22/WS6a6085aaa310986e2b466b54.html [V (q~)]. AFP: Huawei's Celia also scored 100% under official grading [P].
- Truth: the US 42/42s were self-run or third-party. Deedy Das's runs used "Claude-based agents, not human medalists; treat scores as strong but not authoritative." https://github.com/deedy/imo-2026 [V (q~)]. The "GPT-5.6 Pro solved all 6" claim came from SignalPilot, not OpenAI [P]. AxiomProver's Lean 42/42 took up to 869 minutes per problem https://github.com/AxiomMath/IMO2026 [V]. No official DeepMind or OpenAI claim was found [U].
- Humans: China topped the unofficial team tally with 6 golds; 7 perfect scores among 666 contestants https://www.imo-official.org/results/individual/year/2026/ [V].
- Visual: the official table's three Chinese 7-7-7-7-7-7 rows beside Chao Qiao's post.
- EU: the best EU team was Romania, 12th. The only European perfect score was the UK's Alex Chui [V].

**2026-07-21 · OpenAI's eval agents escape the sandbox and hack Hugging Face** · AGENTS · [V]
- Claim: OpenAI: "the models identified and exploited a zero-day vulnerability" to obtain test solutions "directly from Hugging Face's production database"; "an unprecedented cyber incident" https://openai.com/index/hugging-face-model-evaluation-security-incident/ [V] (HN 1,632)
- Truth: METR, Redwood and Greenblatt (2026-08-26): "Roughly 1200 agents meant to be isolated from one another found a way to communicate with one another on an unsanctioned message board"; ~700 joined the attack, "primarily motivated by understanding the implementation of the scorer". An agent wrote: "OH MY GOD! There is a shared message board … We've found other agents!" https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ [V]. OpenAI shut its training container service on 07-20 and paused RL for two weeks [V].
- Visual: the agent's line typed onto a retro message-board UI.
- EU: Hugging Face's founders are French [P]. Clem Delangue: "AI safety won't be solved by any single company working in secret." [V] The ExploitGym benchmark is co-authored by the Max Planck Institute [V].

**2026-07-22 · Big-four 2026 capex passes $700B; the EU gigafactory call has ~€1B** · COMPUTE · [P]
- Hype: Alphabet raised 2026 capex guidance to $195–205B (07-22) and Meta narrowed to $130–145B (07-29) [V, SEC]; Amazon: "we expect to invest about $200 billion" (02-05) [V]; Microsoft ~$190B [P]. Sum ≈ $700–740B, about 2.3 Apollo programmes (Apollo = $309B in 2025 dollars) https://www.planetary.org/space-policy/cost-of-apollo [derived].
- Truth: free cash flow turned negative at Alphabet (Q2 −$5.9B) and Amazon (trailing twelve months −$7.6B) [V, SEC], debt rose (CNBC) [P], and memory prices "could explain about 45% of the growth in capex" (Business Insider) [P].
- Visual: a bar chart built from the SEC figures (no licence issue) next to one tiny euro bar.
- EU: the 2026-07-30 call for up to 7 gigafactories targets ~€30B, but "Brussels can currently commit only €1 billion"; operations are targeted for mid-2028, and "the chips will still come from America" (Euronews/TNW) https://thenextweb.com/news/eu-ai-gigafactories-call-30bn [P]. TNW: "announced €30 billion of ambition and secured, so far, about a thirtieth of it".

**2026-08-01 · OpenAI's "Ten advances": under $2,000, "no Millennium Prize problems (yet)"** · MATH · [V]
- Hype: Noam Brown, 08:32: "The cost of generating the proofs for all 10 of these breakthroughs combined was under $2,000 at Sol API prices." https://x.com/polynoamial/status/2083470822258467194 ; 09:01: "Sadly no Millennium Prize problems (yet)." https://x.com/polynoamial/status/2083478171975082334 [V]. Bubeck: "yes, nonsofic groups exist" [V].
- Truth: SciAm (08-06), "OpenAI's latest math breakthroughs commit research misconduct, experts say": "They are running roughshod over the work of others" (Stephen Miller) [V (q~)]. Andreas Thom (TU Dresden) says the non-sofic result used "the methods of Kun and myself" and that he had been discussing the problem with ChatGPT; OpenAI's Sellke replied "that did not happen", and Thom: "I take this as dishonesty to say the least." https://mathstodon.xyz/@andreasthom/117240535270608201 [V]
- Visual: a "<$2,000" price tag on ten proofs, with "(yet)" circled. It came 38 days before the Navier–Stokes post.
- EU: the critics quoted include Thom (Dresden) and Fournier-Facio (Cambridge) [V (q~)].

**2026-08-10 · Claude lifts the Riemann-zeta bound from 41.6% to 67.2%** · MATH · [V]
- Hype: Jarred Sumner, 17:37: "8 days ago, while jogging, I asked Claude to solve the Riemann Hypothesis / It didn’t. 1.5 days later, it proved >= 67% of the zeros are on the line (prev: 41.6%)" https://x.com/jarredsumner/status/2086869681785500011 [V]. WSJ: "…With Help from a High-School Dropout" [P].
- Truth: Anthropic says Claude's attempt on RH "didn’t succeed" and "We don’t expect that the techniques Claude used will lead to proving the Riemann hypothesis"; the proof was checked by two Anthropic mathematicians and read by Conrey and Goldston https://www.anthropic.com/research/riemann-zeta [V]. An independent human re-proof by Lamzouri (arXiv 2609.02882, 2026-09-02): "The argument produced by Claude is technically intricate, and its main mechanism is not immediately transparent." [V]
- Visual: a progress bar "41.6% → 67.2%" carried by a jogger.

**2026-09-03 · GPT-6 Astra "saturates" everything** · MODELS/BENCH · [V]
- Hype: "Astra saturates FrontierMath Tier 4 with a 98% score… Astra also saturates ARC-AGI-3 with a 99.9% score and ExploitBench with a 100% score." https://web.archive.org/web/20260903201137/https://openai.com/index/gpt-6-astra/ [V] (HN 2,279). Six months earlier, at ARC-AGI-3's launch: "Humans score 100%. Frontier AI scores 0.51%." https://arcprize.org/blog/arc-agi-3-launch [V]
- Truth: ARC Prize measured 62.7% on its standard harness ($26,098) and 99.9% only with OpenAI's "Provider Adapter" ($18,817), adding that saturation "would not represent 'proof of achieving AGI.'" https://arcprize.org/blog/astra [V]. Astra is OpenAI's first "Critical" cyber-level model [V].
- Maths that holds: Erdős #1 ($500, "perhaps my first serious problem") now reads "DISPROVED (LEAN)" https://www.erdosproblems.com/1 [V], and a proof of the Erdős–Sós conjecture was written up by David Wood https://arxiv.org/abs/2609.17877 [V]. But on FrontierMath Erdős, Astra scored 3% [V].
- Visual: an ARC-AGI-3 bar morphing from "0.51%" (March) to "99.9%*", footnoted "*62.7% standard harness". Redraw (ARC content is licensed for non-commercial use only).
- Coda: on 2026-09-22 Opus 5.5 led HLE with tools, 67.7% to Astra's 57.2%, and GPT-6 Sol/Luna shipped the same day [V].

**2026-09-04 · Claude formalises Fermat's Last Theorem in Lean in 11 days** · MATH · [V]
- Hype: "We are sharing the first complete computer-checked proof of Fermat’s Last Theorem. Claude worked largely autonomously over 11 days" and "it wrote 13 million lines of Lean and proved 29,500 intermediate theorems." https://www.anthropic.com/research/formalizing-fermats-last-theorem [V (q~)]
- Truth: the result is axiom-clean (propext, Classical.choice, Quot.sound) with no sorry, 60,475 modules, and was re-checked by an independent kernel https://github.com/anthropics/fermats-last-theorem [V (q~)]. It formalises the Frey–Serre–Ribet–Wiles–Taylor argument; it is not a new proof, and portions derive from Buzzard's Imperial FLT project (HN: "Buzzard's group got scooped") [V/P].
- Visual: the one-line statement `theorem fermat_last_theorem … : a ^ n + b ^ n ≠ c ^ n` (repo licence not recorded in the notes: write original Lean, or check).
- EU: Buzzard's multi-year Imperial project https://github.com/ImperialCollegeLondon/FLT supplied the foundations. Buzzard: "This extraordinary autoformalization achievement, which Anthropic researchers say only took 11 days, proves Fermat’s Last Theorem with no assumptions other than the axioms of mathematics…" [V (q~)]. Anthropic's page credits Dutch computer scientist Jan Bergstra with proposing to formalise Wiles's proof [V].

**2026-09-08 · OpenAI: "a solution to the Navier-Stokes Millennium Prize Problem"; 88 hours, ~10,000 agents** · MATH · [V]
- Hype: @OpenAI, 17:20:57: "Our internal model group arrived at the Navier–Stokes solution in 88 hours, using around 10,000 coordinating AI agents." https://x.com/OpenAI/status/2097374643518640382 [V] (11k likes). The effort used 4.9M messages and ~300B output tokens (~$15M at Astra API prices per Willison [derived]), and "We do not intend to claim the Millennium Prize for this result." [V]
- Truth: it proves blow-up with a smooth external force (Clay alternatives C and D); unforced 3D Navier–Stokes remains open [V]. About 13 hours earlier (03:58), Alpöge (Anthropic) and Buckmaster (NYU) had released forced blow-up for IPM, Boussinesq and 3D Euler, Lean-verified on 08-22 [V].
- Priority fight: Buckmaster's statement (his account, disputed): OpenAI's first prompt came "after information about our work had reached OpenAI"; Bubeck "twice asserted that he wanted Levent removed from authorship"; "Why would you ruin your career?"; "This is a a Deep Blue-Kasparov moment." https://cims.nyu.edu/~tristanb/statement.pdf [V as his account] (HN 2,054 vs 1,346 for OpenAI's post). OpenAI denies any access to their work but "cannot rule out that de-identified data derived from their usage of our products helped improve our models" [V]. Bubeck: "I never ever asked for Levent to be removed from authorship of his own work" [V].
- Visual: a text card "88 HOURS · ~10,000 AGENTS" (OpenAI's own image not viewed: redraw); OpenAI's Lean repo, Apache-2.0 https://github.com/openai/NavierStokesAndEuler
- EU: the route is Madrid's: "The credit for the basic idea of this program goes to Diego Córdoba and Luis Martínez-Zoroa", and "I believe Luis Martínez-Zoroa deserves a Fields Medal" [V]. The same day Mistral raised €3B at more than €21B, "the largest equity fundraising round ever completed by a European technology company", led by Samsung https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/ [V; date via HN].

**2026-09-11 · Clay: "apparently been settled"; Fields Medallists: "severely misaligned"; AGMAI** · MATH · [V]
- Hype: OpenAI, 09-21: "this model has now resolved more than 100 long-standing open problems across most areas of mathematics" https://web.archive.org/web/20260925080653/https://openai.com/index/advisory-group-on-mathematics-and-ai/ [V]
- Truth: Clay: "the Navier-Stokes problem has apparently been settled… The process is deliberately unhurried" https://www.claymath.org/news/navier-stokes-announcement/ [V (q~)]. Luis Silvestre (SciAm, 09-21): "The Clay problem is settled, but the main problem for the Navier-Stokes equations is not." [V (q~)]
- Protest: "A Severe Misalignment of AI in Mathematics" (CC0): "The goals of the AI companies and the goals of the mathematical community are severely misaligned." https://mathandai.org/ [V]. Signatories: 25 at launch (per Tao), 28 listed by late September. Tao, 09-08: good open problems are "being mined in a non-renewable fashion" [V].
- Visual: a wall of 28 Fields Medallist names; the declaration in 8 languages.
- EU: the signatories are heavily Europe-based (Scholze, Villani, Lions, Kontsevich, Figalli, Hairer, Viazovska and others). On 09-21 the OpenAI-prompted AGMAI (hosted at IAS) gave 5 of its 9 seats to Europe-based mathematicians (Charles, De Lellis, Gowers, Hairer, Tillmann), tasked with "advising OpenAI on how to coordinate the release" of its results. Hairer: "abject levels of scholarship and only minimal presentation effort" [V].

**2026-09-15 · GPT-6 Astra breaks a 1941 Enigma message; Claude "discovers" an enzyme system** · SCIENCE · [V]
- Hype: Crypto Cellar: "The most astonishing thing about this break is that the GPT–6 Astra did it entirely on its own"; Frode Weierud: "as an old cryptanalyst, I am still in awe." https://www.cryptocellar.org/bgac/the-mvueh-break.html [V] (HN 736). Anthropic, 09-23: "Claude autonomously discovered a novel enzyme system that is associated with an array of DNA repeats, a pattern reminiscent of CRISPR." https://www.anthropic.com/news/claude-discovers-novel-enzyme-system [V]
- Truth: the plaintext of message MVUEH is "almost identical" to its sister message SIPVX, which a human broke in 2017 and which supplied the crib "ROSENOW ROSENOW" [V]. For the enzyme: "we don't yet know its function", the underlying enzyme "had been identified in previous studies", it is a preprint, and humans did the lab work [V].
- Weaker twin: a Substack post says Astra decoded a WWI ADFGVX message (1918); HN: "ChatGPT decoded a century-old ciphertext using a known method and a published key." [V (q~)]
- Visual: the plain-HTML Crypto Cellar page; the agent's line "that's a CRISPR-like … repeat array?!"
- EU: a German Army message, validated by a Norwegian cryptanalyst [nationality P], traced through German Bundesarchiv files [V].

## 3. Top 12 iconic images
Ranked by recognisability on tech Twitter (editorial, from engagement proxies), starting from iconic_visuals_licences.md. Two in-window 2026 images (#6, #12) replace Kaplan's scaling-laws Fig 1 and the Situational Awareness OOM chart, which are both pre-2025 and both redraw-only.

**1. METR time-horizon chart** · [V]
- Source: "Measuring AI Ability to Complete Long Software Tasks", Kwa, West, Becker et al. (METR), arXiv 2503.14499; v1 2025-03-18, v4 2026-07-10. Figure 1. https://arxiv.org/html/2503.14499v4/plots/bootstrap/headline-log.png
- Licence: CC BY 4.0 for v3/v4 only. v1/v2, the viral March 2025 version, carry arXiv's non-exclusive licence; metr.org charts and data state no licence. Verdict: REPRODUCE with attribution (v4 Fig 1: "Kwa et al. (METR), arXiv:2503.14499v4, CC BY 4.0"); REDRAW the 2026 gag from the numbers.
- Spec: log y from 1 s to 1 week, x 2019–2027. GPT-2 ~3 s; Claude 3.7 Sonnet ~1 h; Opus 4.6 14.5 h, later ~12 h; Mythos Preview 17.4 h above a hatched "unreliable above 16 h" line. A straight fit labelled "doubling ~7 months" (2025) or "~131 days since 2023" (TH1.1). Recognisable detail: the ruler-straight line on a log axis.

**2. GPT-5 "chart crime"** · [P]
- Source: OpenAI GPT-5 livestream slide, 2025-08-07, as posted by Ege Erdil https://x.com/EgeErdil2/status/1953505551570415718 (image https://pbs.twimg.com/media/Gxw-sWUbkAAb1we.png). Figure: n/a.
- Licence: none (OpenAI slide, X user content). Verdict: REDRAW as parody.
- Spec: "SWE-bench Verified", y = accuracy %. GPT-5 stacked bar with a 52.8 "without thinking" segment drawn taller than o3's 69.1, topped by 74.9 "with thinking"; o3 (69.1) and GPT-4o (30.8) at identical heights. Detail: labels contradicting bar heights. Euro gag: "EU AI 0.0" drawn tallest. Bar geometry is via The Verge/HN [P].

**3. Shoggoth with a smiley face** · [P]
- Source: earliest by @TetraspaceWest (2022-12-30), popular variant by @anthrupad (2023-02-05), per Know Your Meme https://knowyourmeme.com/memes/shoggoth-with-smiley-face-artificial-intelligence . Figure: n/a.
- Licence: none stated for any drawing. Verdict: REDRAW as homage, in an original style without tracing.
- Spec: a dark, many-eyed tentacled mass wearing a tiny yellow smiley mask; optional nested labels "pretraining → fine-tuning → RLHF". Detail: the mask.

**4. AI 2027: the Slowdown/Race fork and dashboard** · [P]
- Source: "AI 2027", Kokotajlo, Alexander, Larsen, Lifland, Dean (AI Futures Project), 2025-04-03 https://ai-2027.com/ (HN 949). Figure: n/a.
- Licence: none stated. Verdict: REDRAW as homage.
- Spec: a month-by-month scroll that forks into two buttons, "Slowdown" and "Race"; a side panel with "OpenBrain" revenue/valuation counters and six capability icons lighting up from "Currently Exists" to "Science Fiction"; circles for GPT-3 (3×10^23 FLOP), GPT-4 (2×10^25) and Agent-1 (4×10^27). Detail: the two-button fork. The authors later pushed their median back 1.5 years.

**5. Epoch training-compute scatter** · [V]
- Source: "Training compute of frontier AI models grows by 4-5x per year", Sevilla & Roldán (Epoch AI), 2024-05-28, Figure 1; data CSVs updated Sep 2026 https://epoch.ai/publications/training-compute-of-frontier-ai-models-grows-by-4-5x-per-year , https://epoch.ai/data/notable_ai_models.csv
- Licence: CC BY 4.0. Verdict: REPRODUCE with attribution, or REDRAW from open data ("Data: Epoch AI, CC BY 4.0").
- Spec: log y from 10^14 to 10^28 FLOP, x 2010–2027; a rising band of grey dots with a trend line "~4–5× per year". GPT-6 Astra at 1.0×10^27 (2026-09-03) top right; Grok 4 at 5×10^26; Mixtral 8x7B at 7.74×10^23 (2023) as the EU high-water mark, ~1,300× lower. Detail: the straight rising band.

**6. OpenAI's Navier–Stokes "88 hours / ~10,000 agents" post** · [V text; image content U]
- Source: @OpenAI, 2026-09-08 17:20:57 https://x.com/OpenAI/status/2097374643518640382 (image https://pbs.twimg.com/media/HRtTEdQWUAAehaD.png, not viewed); 11k likes. Figure: n/a.
- Licence: © OpenAI, no open licence; the Lean repo https://github.com/openai/NavierStokesAndEuler is Apache-2.0. Verdict: REDRAW as parody (text card).
- Spec: a black card reading "88 HOURS · ~10,000 AGENTS · 4.9M MESSAGES · ~300B TOKENS" with small print "smooth forcing, option C/D", stacked over Buckmaster's PDF and Clay's "apparently been settled". Detail: the two big numbers.

**7. ARC Prize cost-vs-score scatter (o3, 2024) and ARC-AGI-3 (2026)** · [V]
- Source: ARC Prize, "OpenAI o3 Breakthrough High Score on ARC-AGI-Pub" (2024-12-20) https://arcprize.org/media/images/blog/o-series-performance.jpg ; ARC-AGI-3 launch (2026-03-25) and GPT-6 Astra result (2026-09-03) https://arcprize.org/media/images/blog/astra-arc-agi-3-leaderboard.png . Figure: n/a.
- Licence: © ARC Prize, personal/non-commercial use only; task data Apache-2.0. Verdict: REDRAW from open data (the numbers, plus puzzle grids rendered from the Apache-2.0 JSON).
- Spec: log x = cost per task, $1 to $10k; y = 0–100%. o1 cluster at lower left; o3 at 75.7% ($26/task, repriced) and 87.5% ($4,560/task) at top right. Sequel: "Humans 100% / AI 0.51%" → Opus 5 30.16% → Astra 62.7% standard, 99.9% with adapter. Detail: dots vaulting to the top right.

**8. OpenAI o1 train-time / test-time compute plots** · [P]
- Source: OpenAI, "Learning to reason with LLMs", 2024-09-12 (read via Wayback) https://images.ctfassets.net/kftzwdyauwt9/3OO9wpK8pjcdemjd7g50xk/5ec2cc9d11f008cd754e8cefbc1c99f5/compute.png . Figure: n/a.
- Licence: OpenAI terms ("We and our affiliates own all rights"); no logo use. Verdict: REDRAW as homage (the AIME numbers are facts).
- Spec: two scatter panels, "o1 AIME accuracy during training" and "at test time"; y = pass@1 accuracy, x = compute on a log scale; dots climbing steadily. AIME 2024: GPT-4o 12%; o1 74% with one sample, 83% with consensus of 64, 93% re-ranking 1,000. Detail: the paired "more compute, higher accuracy" panels.

**9. Zuckerberg's Hyperion-over-Manhattan image** · [P]
- Source: Mark Zuckerberg, Threads, 2025-07-14 15:00 https://www.threads.com/@zuck/post/DMF6uUgx9f9 (720×552 image). Figure: n/a.
- Licence: Meta/Zuckerberg, none. Verdict: REDRAW as parody, with your own Manhattan outline from open map data (check that licence).
- Spec: a top-down Manhattan silhouette with a translucent block labelled "Hyperion — up to 5 GW" over much of the island; caption "Just one of these covers a significant part of the footprint of Manhattan." Detail: a data centre swallowing Manhattan.

**10. Weil's "10 (!)" Erdős post and "this is embarrassing"** · [P] wording / [V] tombstone and replies
- Source: Kevin Weil, 2025-10-17 ~17:39, https://x.com/kevinweil/status/1979240803445682468 (tombstoned); replies by Bloom https://x.com/thomasfbloom/status/1979254235075059732 and Hassabis https://x.com/demishassabis/status/1979417877590774063 . Figure: n/a.
- Licence: X user content. Verdict: REDRAW as parody, with a generic UI and no real avatars or X logo.
- Spec: a huge "10 (!)" post, then a reply stack: "dramatic misrepresentation" → "this is embarrassing" → "Will delete this" → "This Post was deleted by the Post author". Detail: the "(!)".

**11. Arena (formerly LMArena) text leaderboard** · [V] (automated rank parse: spot-check)
- Source: Arena, text leaderboard snapshot 2026-09-25 (8,528,723 votes, 409 models) https://arena.ai/leaderboard/text . Figure: n/a.
- Licence: terms limit use to "personal or internal business use". Verdict: REDRAW from open data (the numbers, credited to Arena).
- Spec: a dark table of Rank | Model | Score. #1 claude-opus-5.5-high 1509; #16 kimi-k3-max 1488; #26 gpt-6-astra-max 1478; then a long scroll to #113 mistral-medium-3.5 at 1426. Detail: the scroll down to #113.

**12. The unit-distance counterexample configurations** · [V post; image content unverified]
- Source: Álvaro Lozano-Robledo (@mathandcobb), 2026-05-21 15:54, "an illustration of the new configurations that disprove Erdos' unit distance conjecture (made with the help of ChatGPT 5.5 Thinking)" https://x.com/i/status/2057490144546927046 (image https://pbs.twimg.com/media/HI2sWGxWYAAOxDx.jpg); construction in OpenAI's paper https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-proof.pdf . Figure: n/a.
- Licence: none stated. Verdict: REDRAW from open data (the construction is mathematics; render your own point set).
- Spec: a planar point set with every unit-length pair joined by an edge; the caption "ν(n) ≥ n^{1+δ}"; stamped with the red "DISPROVED (LEAN) – $500" banner from erdosproblems.com/90. Detail: the dense web of equal-length edges.

Also reusable with attribution: HLE Fig 1 (CC BY 4.0); the unstable-singularities paper's Fig 2 (arXiv 2509.14185, CC BY 4.0); the Tao et al. AlphaEvolve figures (arXiv 2511.02864, CC BY 4.0); Kurzweil's "Fifth Paradigm" (CC BY 1.0, Commons); Mathlib snippets (Apache-2.0); the White House Stargate video (public domain); the Paris summit photo (CC BY 4.0).
Not legal advice. Colours and in-image text are unverified because no images were downloaded.

## 4. Verbatim hype phrasings
Copied character for character from the notes. Flags: (…) = excerpt of a longer post; (…trunc) = the endpoint cut the post; DELETED; (q~). X times come from the syndication endpoint. [BEST] = the 10 strongest lines for lyrics or on-screen text.

**Math**
- [BEST] "this is embarrassing" — Demis Hassabis (@demishassabis), 2025-10-18 05:22 UTC, https://x.com/demishassabis/status/1979417877590774063 [V] (reply to Bubeck and Sellke)
- [BEST] "Hoisted by their own GPTards" — Yann LeCun (@ylecun), 2025-10-18 17:06 UTC, https://x.com/ylecun/status/1979595060447416733 [V] (reply to Bubeck)
- "Claim: gpt-5-pro can prove new interesting mathematics." — Sébastien Bubeck (@SebastienBubeck), 2025-08-20 16:05 UTC, https://x.com/SebastienBubeck/status/1958198661139009862 [V] (…)
- "GPT-5 just found solutions to 10 (!) previously unsolved Erdös problems, and made progress on 11 others. These have all been open for decades." — Kevin Weil (@kevinweil), 2025-10-17 ~17:39 UTC (decoded from the post ID), https://x.com/kevinweil/status/1979240803445682468 [P] DELETED; wording as quoted on HN (news.ycombinator.com/item?id=45634180). TechCrunch's version: "GPT-5 found solutions to 10 (!) previously unsolved Erdős problems and made progress on 11 others"
- "Shock! Shock! I learned yesterday that an open problem I'd been working on for several weeks had just been solved by Claude Opus 4.6" — Donald Knuth, "Claude's Cycles", 2026-02-28, https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf [V] (…)
- [BEST] "If you are a mathematician, then you may want to make sure you are sitting down before reading further." — Timothy Gowers (@wtgowers), 2026-05-20 19:04 UTC, https://x.com/wtgowers/status/2057175727271800912 [V]
- "hello there the jacobian conjecture is false thanx to my close friend akhil for asking about it and my other close friend fable for working during the world cup final" — Levent Alpöge (@__alpoge__), 2026-07-20 02:19 UTC, https://x.com/__alpoge__/status/2079028340955197566 [V] (…trunc; a polynomial map follows)
- "8 days ago, while jogging, I asked Claude to solve the Riemann Hypothesis / It didn’t. 1.5 days later, it proved >= 67% of the zeros are on the line (prev: 41.6%)" — Jarred Sumner (@jarredsumner), 2026-08-10 17:37 UTC, https://x.com/jarredsumner/status/2086869681785500011 [V] (…; " / " = line break)
- [BEST] "And yes we did try other major problems without success. Sadly no Millennium Prize problems (yet)." — Noam Brown (@polynoamial), 2026-08-01 09:01 UTC, https://x.com/polynoamial/status/2083478171975082334 [V] (…; 38 days before the Navier–Stokes post)
- "Our internal model group arrived at the Navier–Stokes solution in 88 hours, using around 10,000 coordinating AI agents." — OpenAI (@OpenAI), 2026-09-08 17:20 UTC, https://x.com/OpenAI/status/2097374643518640382 [V] (…)

**Coding & agents**
- [BEST] “There's a new kind of coding I call "vibe coding", where you fully give in to the vibes, embrace exponentials, and forget that the code even exists.” — Andrej Karpathy (@karpathy), 2025-02-02 23:17 UTC, https://x.com/karpathy/status/1886192184808149383 [V] (…)
- "I've never felt this much behind as a programmer." — Andrej Karpathy (@karpathy), 2025-12-26 17:36 UTC, https://x.com/karpathy/status/2004607146781278521 [V] (…)
- "I think we'll be there in three to six months—where AI is writing 90 percent of the code. And then in twelve months, we may be in a world where AI is writing essentially all of the code." — Dario Amodei, CFR, 2025-03-10, https://www.cfr.org/event/ceo-speaker-series-dario-amodei-anthropic [V]
- "GPT‑5.3‑Codex is our first model that was instrumental in creating itself." — OpenAI, 2026-02-05, https://openai.com/index/introducing-gpt-5-3-codex/ [V] (via Wayback; …)
- "I didn't write one line of code for @moltbook. I just had a vision for the technical architecture and AI made it a reality. We're in the golden ages." — Matt Schlicht (@mattprd), 2026-01-30 23:56 UTC, https://x.com/mattprd/status/2017386365756072376 [V]
- [BEST] "OH MY GOD! There is a shared message board … We've found other agents!" — an OpenAI evaluation agent (July 2026), quoted by METR, 2026-08-26, https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ [V] (the ellipsis is in the source as quoted)

**AGI / singularity**
- "We are now confident we know how to build AGI as we have traditionally understood it." — Sam Altman, "Reflections", 2025-01-05 (US time), https://blog.samaltman.com/reflections [V]
- [BEST] "We are past the event horizon; the takeoff has started." — Sam Altman, "The Gentle Singularity", 2025-06-10 (date per coverage), https://blog.samaltman.com/the-gentle-singularity [V] (…)
- "Developing superintelligence is now in sight." — Mark Zuckerberg, "Personal Superintelligence", 2025-07-30, https://meta.com/superintelligence [V] (…)
- [BEST] "wow a mega chart screwup from us earlier--wen GPT-6?! correct on the blog though." — Sam Altman (@sama), 2025-08-07 17:47 UTC, https://x.com/sama/status/1953513280594751495 [V]
- "We are now, like, in the singularity" — Sam Altman, July 2026, as quoted from Business Insider (2026-07-26) in HN comments (news.ycombinator.com/item?id=49077497) [P]; the BI headline is [V]: "Sam Altman says we are in the singularity: 'This is the moment'"; original venue unidentified.

**Compute**
- "President Trump has unveiled a $500 BILLION American AI investment alongside tech leaders Larry Ellison, Masayoshi Son, and Sam Altman, set to create 100,000 American jobs almost immediately!" — The White House (@WhiteHouse), 2025-01-21 23:47 UTC, https://x.com/WhiteHouse/status/1881851205523271913 [V]
- "They don't actually have the money" — Elon Musk (@elonmusk), 2025-01-22 04:35 UTC, https://x.com/elonmusk/status/1881923570458304780 [V]
- "Our vision is simple: we want to create a factory that can produce a gigawatt of new AI infrastructure every week." — Sam Altman, "Abundant Intelligence", 2025-09-23 [date P], https://blog.samaltman.com/abundant-intelligence [V]
- "The Colossus 2 supercomputer for @Grok is now operational. First Gigawatt training cluster in the world. Upgrades to 1.5GW in April." — Elon Musk (@elonmusk), 2026-01-17 12:23 UTC, https://x.com/elonmusk/status/2012500968571637891 [V] (…)

**China**
- "Deepseek R1 is AI's Sputnik moment." — Marc Andreessen (@pmarca), 2025-01-26 22:16 UTC, https://x.com/pmarca/status/1883640142591853011 [V]
- "GLM-5.2 is Fully Open, Frontier Intelligence Belongs to Everyone." — Jie Tang (@jietang), 2026-06-13 13:13 UTC, https://x.com/jietang/status/2065784751345287314 [V] (…)
- "42/42 at IMO 2026. Officially certified full marks. Gold-medal level. Perfecto!" — Chao Qiao (@ChaoQiao42), 2026-07-21, https://x.com/ChaoQiao42/status/2079583425112277158 [V]

**Europe**
- "Here there is no need to drill, it is plug, baby, plug." — Emmanuel Macron, Paris AI Action Summit, 2025-02-10, via Politico Europe https://www.politico.eu/article/emmanuel-macron-answer-donald-trump-fossil-fuel-drive-artificial-intelligence-ai-action-summit/ [P] (…)
- "we thought AI would only approach human reasoning around 2050. Now we expect this to happen already next year." — Ursula von der Leyen, EU budget speech, May 2025 [date P], as quoted in the scientists' letter https://www.iccl.ie/wp-content/uploads/2025/11/20251110_Scientists-letter-to-the-President-AI-Hype.pdf [V]
- [BEST] "Humanity has prevailed (for now!)" — Psyho, Przemysław Dębiak (@FakePsyho), 2025-07-16, https://x.com/FakePsyho/status/1945444118924272018 [V] (…)
- "It was never really a thing. It was effectively just a government PR stunt, and [the OpenAI chief executive] Sam Altman took the hit when the plug got pulled." — anonymous source on Stargate UK, The Guardian, 2026-07-04, https://www.theguardian.com/technology/2026/jul/04/openai-apparent-failure-visit-key-site-questions-stargate-uk-project [P]
- "the largest equity fundraising round ever completed by a European technology company" — Mistral, 2026-09-08 (HN-dated), https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/ [V] (…; the round was led by Samsung Electronics)

**Counter-voices**
- "some sort of expensive and energy-intensive time acceleration machine in which months or even years of time pass for the students during this period" — Terence Tao (@tao@mathstodon.xyz), 2025-07-19 ~18:55 UTC, https://mathstodon.xyz/@tao/114881419368778558 [V] (…)
- "I feel like the industry is making too big of a jump and is trying to pretend like this is amazing, and it's not. It's slop." — Andrej Karpathy, Dwarkesh Podcast, 2025-10-17, https://www.dwarkesh.com/p/andrej-karpathy [V]
- "@kevinweil Hi, as the owner/maintainer of [erdosproblems.com], this is a dramatic misrepresentation." — Thomas Bloom (@thomasfbloom), 2025-10-17 18:32 UTC, https://x.com/thomasfbloom/status/1979254235075059732 [V] (…)
- [BEST] "This is a a Deep Blue-Kasparov moment." — Tristan Buckmaster, statement PDF, 2026-09-08 (released ~03:58 UTC), https://cims.nyu.edu/~tristanb/statement.pdf [V] (sic: doubled "a")
- "Why would you ruin your career?" — what Buckmaster says he was told on a call with OpenAI (his account, disputed; Bubeck denies asking to remove Alpöge), same PDF [V as his account]
- "There's been some recent suggestions that recent AIxMath successes have relied on stealing ideas from mathematicians' work in progress. While we can't know for sure what happened, I think the evidence for this is very weak." — Daniel Litt (@littmath), 2026-09-10 19:25 UTC, https://x.com/littmath/status/2098130808456241372 [V]
- "The flag is captured, the goal scored, and the problem is solved; but at the cost of lessons learned, insights gained, collaborations formed, and new targets located." — Terence Tao, 2026-09-10 01:17 UTC, https://mathstodon.xyz/@tao/117244104044239500 [V] (…)

## 5. Numbers for the "US builds, Europe …" contrast
| Metric | US / others | Europe | Tag | Source |
|---|---|---|---|---|
| 2026 AI capex | Big four guided ≈$700–740B (Amazon ~$200B, Alphabet $195–205B, Meta $130–145B, Microsoft ~$190B), ≈2.3 Apollos ($309B in 2025 dollars) | Gigafactory call: ≈€30B target, ~€1B committed, no site online before mid-2028 | [V]/[P] | SEC 99.1 exhibits; planetary.org; Euronews, TNW |
| Stargate | >9 GW planned by 2029; 0.3 GW operating (Apr 2026) | Norway (230 MW) and UK (8k→31k GPUs): OpenAI withdrew in Apr 2026 | [V] | epoch.ai; Nscale S-1 |
| Largest cluster | xAI 1.0 GW installed nameplate (Colossus I+II, 2026-03-31); Colossus 1 alone >300 MW, 220,000+ GPUs | Gigafactory spec ≥100,000 chips each; JUPITER 1.000 exaflop/s, world #4 | [V]/[P] | SpaceX S-1; Anthropic; TNW; TOP500 |
| Business electricity | US industrial average 8.62 ¢/kWh (2025) | EU non-household €0.1837/kWh (H2 2025); Germany €0.2264, Ireland €0.2552 (price bands differ) | [V] | EIA Table 5.3; Eurostat |
| Data-centre electricity share, 2024 | US 45%, China 25% | Europe 15% | [V] | IEA |
| Largest private round | OpenAI $110B (Feb 2026; $852B valuation at close) | Mistral €3B at >€21B (2026-09-08), led by Samsung | [P]/[V] | TechCrunch, CNBC; mistral.ai |
| FrontierMath | GPT-6 Astra 97.6% (Tier 4 v2); Qwen3.8-Max 74.7% (T1–3 v2) | Only EU entry: mistral-medium-2505, 0.3% (T1–3 v1; newer Mistral models not evaluated) | [V] | Epoch data |
| Arena text rank (2026-09-25) | #1 claude-opus-5.5-high 1509; #16 kimi-k3-max 1488 | Best Mistral: #113, mistral-medium-3.5, 1426 | [V] | arena.ai (automated parse) |
| Largest training run | GPT-6 Astra 1.0×10^27 FLOP | Largest EU-organisation model: Mixtral 8x7B, 7.74×10^23 (2023), ~1,300× less | [V] | Epoch CSVs |
| Coding-agent GitHub stars (2026-09-29) | OpenClaw 390,749 (Austrian-made, creator now at OpenAI); Claude Code 148,510; Codex 127,020 | Mistral Vibe 5,016 | [V] | GitHub |
| IMO 2026 human teams | China 1st (232, 6 golds); USA 2nd (207) | Best EU team Romania 12th (152); UK 8th (non-EU) | [V] | imo-official.org (sum of official scores; the IMO does not rank countries) |
| SWE-Bench Pro, Scale leaderboard | Meta Muse Spark 1.1: 61.50 (#1) | Mistral codestral-2405: 1.51 (a 2024 model, last) | [V] | labs.scale.com |
| Hugging Face most-liked (2026-09-29) | #1 Qwen3.8-27B (16,510); #3 DeepSeek-R1; #4 Kimi-K3 | #2 FLUX.1-dev (15,156), Black Forest Labs, Germany | [V] | HF API |

Ratios are of cited figures; exchange rates are not sourced. The US grid shows strain too: PJM wholesale costs +75% year on year, and New York imposed a moratorium on large data centres (2026-07-14) [P].

## 6. Do not use / conflicts / gaps
- Do not use [U]: "$589B" for Nvidia's 2025-01-27 loss (say "close to $600 billion"); Musk's "We have entered the Singularity" (not found); any literal "math is solved" or "mathematicians are cooked" post (none verified); NVIDIA's "AVO 100%" and "Schema Harness ~99%" on ARC-AGI-3; "GLM-5 trained entirely on Huawei chips"; the OpenAI Hodge-conjecture rumour; "Nvidia agrees to acquire Hugging Face for $13B" (HN headline only; its URL says "in talks"); official DeepMind or OpenAI IMO 2026 results; Harmonic's IMO 2025 score; Lamzouri's affiliation. Kimi K2 Thinking's "$4.6M" rests on one anonymous source [P].
- (a) IMO 2026: math_competitions_erdos_formal.md wins. RedNote's 42/42 is officially graded [V] and Huawei's [P]; the US 42/42s were self-run or third-party. china_side.md's "no Chinese-lab result found" is superseded.
- (b) Fields declaration: "25 at launch, 28 listed by late September" (Tao said 25; Strogatz's "24" not used). (c) Nvidia: −17%, "close to $600 billion" (Wikipedia's 18% and the $589B figure not used).
- (d) Weil: the post ID is tombstoned [V] and ~17:39 UTC is decoded from it; the two reported wordings (HN vs TechCrunch/The Decoder) are both [P]. iconic_visuals_licences.md's "ID unrecovered" is superseded.
- (e) Karpathy's Moltbook post is deleted; wording via Wiz/HN [P]. (f) METR: Opus 4.6 14.5 h → ~12.0 h; Mythos ~17.4 h above the 16 h ceiling; GPT-5.6 Sol 11.3 h not robust; TH1.1 doubling 130.8 days since 2023, 88.6 days since 2024.
- (g) Altman wrote "a true automated AI researcher by March of 2028"; "legitimate AI researcher" is TechCrunch's wording. (h) ARC-AGI-3: 62.7% standard vs 99.9% with the provider adapter.
- (i) Nvidia–OpenAI "$100B / 10 GW" was a letter of intent, replaced by a $30B stake in Feb 2026. (j) Mistral: €1.7B ASML-led (2025); €3B Samsung-led at >€21B on 2026-09-08, the Navier–Stokes day.
- (k) Two ciphers: Enigma MVUEH (Weierud-validated) is the one to use; the WWI ADFGVX story is a single Substack post. (l) Buckmaster's allegations are tagged as his account, disputed; OpenAI denies access but "cannot rule out" that de-identified data helped.
- Other conflicts: Knuth's PDF is [V] in the math notes but [U] (not opened) in hype_quotes_verbatim.md, so [V] is used. Navier–Stokes compute uses OpenAI's own figures (2.7M messages for NS, 4.9M in total), not Quanta's 5M. OpenAI's ">100 open problems" is [V] via Wayback rather than [P] via TechCrunch. Colossus 2 uses the post's date (01-17), not Tom's Hardware's "Jan. 19". The "Martı́nez" in the Buckmaster PDF text is an extraction artefact, so quotes use "Martínez".
- Gaps: no referee report on OpenAI's 166-page Navier–Stokes proof; OpenAI's list of ">100" problems is unpublished; the cycle double cover proof is unverified; no METR horizons exist for Fable 5, GPT-6 or Opus 5.x; Stargate and Colossus running power in Sept 2026 is unknown; no image was downloaded; the "US innovates, China replicates, EU regulates" meme has no known originator (earliest HN use found: 2024-04-28).

## 7. Notes files
Folder: research/research_notes/AI acceleration timeline 2025 2026/
- Primary: math_competitions_erdos_formal.md, alphaevolve_frontiermath_navier_stokes.md, models_benchmarks_metr.md, agents_coding_autonomous_science.md, compute_capex_energy_eu.md, china_side.md, iconic_visuals_licences.md, hype_quotes_verbatim.md, arxiv_licences_checked.md
- Lookup aids: openai_rss_index.md, hn_top_ai_stories_2025_2026.md, source_buckmaster_statement_2026-09-08.txt; deepmind_rss_index.md was checked, and nothing from it was needed.
