# EU edition: economy lines, historical references (L20, L24, L35, L37, L40)

Research for the director's note: *the new sections must tell a story in motion, not just animate the lyric words.* Written 30 Sep 2026. No code was changed.

## How to read this

- **Word timings.** `data/eu_words.json` is empty, so no line below has its own sung timings yet. The times come from what `relyric()` in `app/src/scenes/animatic.ts` does with `data/lyrics.json`:
  - where the word counts match, each word keeps the original word's slot (L20, L24, L35);
  - otherwise the words are spread by length over the original span (L37, L40).
  - **Check every sync point against the EU vocal before building.** L37 and L40 are the most uncertain.
- **6 fps.** Europe animates at 6 fps, so one drawing is 0.167 s. A 0.3 s word gets about 2 drawings. Put stamps on short words pre-printed; save the stamp that lands live for long words.
- **Sources.** "Opened" means a research agent loaded the page and quoted it. "Snippet only" means the fact came from a search-result summary and was not confirmed on an opened page. Every hi-res URL below returned HTTP 200 with an image type when checked with `curl -sIL`.

## Picks at a glance

| Line | Lyric | Pick | Story beat | PD image |
|---|---|---|---|---|
| L20 | ASML to the moon | **Lithography, Munich 1796**: a press prints the lyric and the moon | Europe invented the printing stone and now prints every chip, and sells none of them in Europe | Senefelder's press, 1819 (Cleveland Museum of Art, CC0); Galileo's moon, 1610 (Smithsonian, CC0) |
| L24 | Forward SAP, backward, repeat | **Keep the Lumière wall.** The wall is SAP's legacy ERP: every demolition is reversed as the deadline moves 2020 → 2025 → 2027 → 2030 → 2033 | The wall that won't come down | Lumière, 1896 (in the bank) |
| L35 | Build unicorns all the way! | **The Unicorn Tapestries** (Brussels-woven, 1495–1505), told panel by panel | Built in the Low Countries, hunted, carried off, fenced in a pen it could leap out of; bought by an American in 1922 | The Met, CC0, 4 panels |
| L37 | Build post AI trends | **Holland's 1720 bubble came late.** The Medley is rebuilt card by card, and the Dutch card lands last | Paris had burst, London was past its peak, then Holland floated its companies | Bubblers Medley (Rijksmuseum, PD, in the bank) |
| L40 | EU Inc fixes things soon | **Europe's one company form, re-proposed since 1970**, with the 1840 metric medal as the bottom card | 1793 → 1840, 1970 → 2001, 2008 withdrawn, 2014 withdrawn, 2026 SOON | Penin's metric medal, 1840 (Musée Carnavalet, CC0) |

---

## L20 · "ASML to the moon" · shot `moon`

- **Original:** "NVDA to the moon".
- **Timings** (1.56 s, about 9 drawings): ASML 62.54–63.36 · to 63.36–63.62 · the 63.62–63.82 · moon 63.82–64.10.
- **Current shot:** Friedrich's *Two Men Contemplating the Moon* as a still, with the caption "ASML → Mistral €1.3bn". It is a static plate, not a story.

### Candidates

**A. Lithography: Munich, 1796 → ASML (recommended)**
- **Senefelder.** Alois Senefelder "discovered a third way in Munich in 1796". In 1799 the Bavarian Elector granted him a "Privilegium exclusivum" for 15 years. He died in 1834. Opened: https://www.dpma.de/english/our_office/publications/milestones/greatinventors/senefelder/index.html
- **ASML.** From the company's history page (opened, https://www.asml.com/en/company/about-asml/history):
  - "In 1984, electronics giant Philips and chip-machine manufacturer Advanced Semiconductor Materials International (ASMI) created a new company to develop lithography systems."
  - It started in "a leaky shed next to a Philips office in Eindhoven".
  - The name was "ASM Lithography", and it listed in Amsterdam and New York in 1995.
- **Why it's meaningful.** ASML is a lithography company by name. The whole film is "printed in Europe". The medium and the company are the same invention, 188 years apart.
- **Optional ancestor.** Niépce's bitumen of Judea "became hard and insoluble" in light, which is the photoresist principle. His *Le Cardinal d'Amboise* dates from 1826. Opened: https://blog.scienceandmediamuseum.org.uk/a-z-of-photography-joseph-nicephore-niepce-first-photograph/
- **The 2026 tail.** Tom's Hardware (Anton Shilov, published 24 Sep 2026) reports a panel at De Balie in Amsterdam. Opened: https://www.tomshardware.com/tech-industry/semiconductors/asml-says-its-sells-absolutely-nothing-in-europe-calls-on-eu-to-help-create-demand
  - ASML's Frank Heemskerk (EVP public affairs): **"We are selling absolutely nothing in Europe."**
  - The article adds that Europe was 0% of ASML revenue in Q1–Q2 2026 "according to ASML's earnings reports".
- **The current caption fact.** ASML led Mistral's €1.7bn Series C with €1.3bn on 9 Sep 2025, for about 11% and the largest stake. Opened via CNBC: https://www.cnbc.com/2025/09/09/ai-firm-mistral-valued-at-14-billion-as-asml-takes-major-stake.html

**B. The Dutch spyglass → Galileo's moon**
- Hans Lipperhey of Middelburg "on Oct. 2, 1608, … applied for a patent", and was not successful. Galileo built 9-power instruments, turned them on the Moon in Nov 1609 and published in Venice in March 1610. Opened: https://www.lindahall.org/about/news/scientist-of-the-day/hans-lipperhey/
- **Weak spot:** ASML's optics come from Zeiss in Germany, so "Dutch optics to the moon" is a loose rhyme. Better to use only Galileo's moon plate, as the thing A prints.

**C. Méliès, *Le Voyage dans la Lune* (1902)** (film already in the bank: `melies-voyage-dans-la-lune`)
- Piracy: the film was pirated in the US by "Lubin, Selig, Edison and others". In 1903 a New York branch opened under Gaston Méliès "to pursue all counterfeiters and pirates". Opened: https://en.wikipedia.org/wiki/A_Trip_to_the_Moon
- Ruin: Méliès later destroyed his negatives and ran "a tiny boutique selling toys and novelties on the Gare Montparnasse". Opened: https://www.victorian-cinema.net/melies
- **Verdict:** a strong "Europe invents, America monetises" story, but it doesn't touch ASML. Keep it as a fallback.

### Images

| Image | Item page | Hi-res (curl-checked) | Holder · licence as shown |
|---|---|---|---|
| Alois Senefelder, *Art of the Lithograph: Printing Press*, 1819: a lithograph of his own press, clean line art, stone bed and hinged frame | https://clevelandart.org/art/2006.194.16 | https://openaccess-cdn.clevelandart.org/2006.194.16/2006.194.16_print.jpg (2542×3400); TIFF `…/2006.194.16_full.tif` (3936×5264) | Cleveland Museum of Art 2006.194.16 · CC0 ("You can copy, modify, and distribute this work, all without asking permission") |
| Galileo Galilei, *Sidereus Nuncius*, Venice 1610, "half moon" etching | https://library.si.edu/image-gallery/68453 | https://ids.si.edu/ids/deliveryService?id=SIL-2003-20215 (2083×3200) | Smithsonian Libraries · "No Copyright – United States"; CC0 in the Open Access API. A slide scan, slightly soft; the line art survives. |
| Fallback: Friedrich, *Two Men Contemplating the Moon* | https://www.metmuseum.org/art/collection/search/438417 | https://images.metmuseum.org/CRDImages/ep/original/DP-31997-001-NEW.jpg | The Met · CC0 (bank id `friedrich-two-men-moon`) |

### Shot concept: "The stone that prints the moon"

1. **Cut, on the beat before 62.54.** A top-down view of Senefelder's 1819 press plate, printed as solid black line art. The stone is bare.
2. **"ASML" (62.54–63.36, about 5 drawings): slide.** A blue ink roller slides across the stone. With each pass more of the word ASML appears, set in mirror image in Archivo Black, because a stone prints reversed.
3. **"to the" (63.36–63.82, 3 drawings): flip, then slide.** The hinged frame flips down with a sheet in it. The scraper bar slides across, one drawing per syllable.
4. **"moon" (63.82–64.10, 2 drawings): pull.** The sheet peels up toward the lens. It now reads the right way round, **ASML TO THE MOON**, over Galileo's 1610 half-moon printed in blue line art. The highlighter runs along the printed words.
5. **Into L21:** the caption slip slides in.

ASML appears as a word only, never a logo. The shot uses only four inks and the flat copy stand. A printing press fits the rulebook's list of paper actions: a print pull is a feed plus a peel.

**Caption slip**
```
Alois Senefelder, Art of the Lithograph: Printing Press, 1819. Cleveland Museum of Art, CC0.
Galileo Galilei, Sidereus Nuncius, Venice, 1610. Smithsonian Libraries, no known copyright.
Lithography: Munich, 1796. ASML's sales in Europe, first half of 2026: 0%.
```
- **Alternative deadpan (quote rule: speaker, place, date):** `"We are selling absolutely nothing in Europe." Frank Heemskerk, ASML, De Balie, Amsterdam (reported 24 Sep 2026).`
- **Or keep the current fact:** `9 Sep 2025: ASML puts €1.3bn into Mistral.`

### Flags
- **Primary sources not opened.** The primary ASML/Mistral press release timed out (investor.asml.com); the facts rest on CNBC. The 0% figure is Tom's Hardware's reading of ASML's reports, not checked against the reports themselves.
- **Heemskerk panel date.** Unknown; only the article's publication date (24 Sep 2026) is verified.
- **Snippet-only facts.** Lipperhey's refusal in December 1608, Niépce's 1822 Pius VII copy, and the 1923 date for Méliès burning his negatives came from search summaries only.
- **Tight timing on "moon".** Only 2 drawings, so re-time it against the vocal.

---

## L24 · "Forward SAP, backward, repeat" · shot `wall`

- **Original:** "Forward MLP, backward, repeat".
- **Timings:** Forward 74.06–74.84 · SAP 74.84–76.12 · backward 76.12–76.66 · repeat 76.84–77.60.
- **Current shot:** Lumière's wall, played forward, backward, forward, with the overlays BERLIN 1989 / BORDER CHECKS 2024 / EVERY SIX MONTHS. The director liked the wall, so it stays. The overlay no longer matches the sung word "SAP", and L34 ("Open Europe borders blues") now owns borders.

### Candidates

**A. The wall that won't come down: SAP's legacy-ERP deadline (recommended)**

The wall is SAP's old ERP (ECC / Business Suite 7). Demolishing it is the migration. The film reverses and the wall rebuilds itself each time the deadline moves.
- **2020 → 2025.** "in October 2014 SAP extended support from 2020 until 2025." UpperEdge, 5 Feb 2020. Opened: https://upperedge.com/sap/sap-extends-maintenance-options-to-2030-but-the-devil-is-in-the-details/
- **2025 → 2027, optional 2030.** SAP's own support page. Opened: https://support.sap.com/en/release-upgrade-maintenance/maintenance-information/maintenance-strategy/s4hana-business-suite7.html
  - "On February 4, 2020, SAP has announced …"
  - "mainstream maintenance until end of 2027 for SAP Business Suite 7 core applications"
  - "optional extended maintenance until end of 2030"
  - ASUG, same day: https://www.asug.com/insights/sap-extends-maintenance-for-sap-business-suite-7-and-commits-to-sap-s-4hana
- **→ 2033.** SAP News, 4 Feb 2025. Opened: https://news.sap.com/2025/02/sap-erp-private-edition-transition-option-navigate-complex-rise-with-sap-transformations/
  - The "SAP ERP, private edition, transition option" is "available for purchase starting in 2028 and will be active for usage from 2031-2033".
- **Precision.** 2033 is a paid transition option, not an extension of ECC maintenance. Say "transition option to 2033", not "support to 2033".
- **Why it's meaningful.** It is the DELAY meter in software. The two latest moves were both announced on 4 February, five years apart.

**B. Rise and slide**
- **Rise.** Five ex-IBM staff founded "Systemanalyse und Programmentwicklung" in Weinheim in 1972 and wrote their first software at ICI's nylon plant. R/3 was shown at CeBIT 1991 and ready for market in 1992. Opened: https://www.computerwoche.de/article/2652334/die-geschichte-der-sap.html
- **Slide.** Euronews, 14 Feb 2026. Opened: https://finance.yahoo.com/news/software-sector-sell-off-european-060139954.html
  - "SAP has wiped out €188bn over the past year alone, nearly half of its current capitalisation"
  - "heading for its ninth straight month of decline. That's never happened in over 30 years of trading"
  - The trigger: "Anthropic's unveiling of new enterprise plugins for its Claude AI assistant in January".
- **Overlays:** `FORWARD · WEINHEIM 1972` / `BACKWARD · −€188BN` / `REPEAT · 9 RED MONTHS`.
- **Verdict:** more quotable, but a flat "stock went down" beat, and self-referential about Claude. Keep it as the backup overlay.

**C. Keep the current border overlay**
- It is still true. Germany extended checks at all its land borders "from 16 September 2026 until 15 March 2027". Opened: https://eutoday.net/germany-extends-land-border-checks-to-march-2027-as-temporary-schengen-controls-persist/
- The original six-month period: https://www.euronews.com/my-europe/2024/09/10/germany-announces-temporary-border-checks-at-all-land-borders
- **Verdict:** it now fights the sung word and duplicates L34.

**D. WALL-dorf (caption aside at most)**
- SAP's headquarters are in Walldorf.
- John Jacob Astor was born there on 17 July 1763 and became "the first multi-millionaire in the United States". https://en.wikipedia.org/wiki/John_Jacob_Astor
- The Waldorf Hotel (1893) name "is ultimately derived from the town of Walldorf … ancestral home of the Astor family". https://en.wikipedia.org/wiki/Waldorf_Astoria_New_York
- **Verdict:** one hop too many for 3.5 s.

**About the film**
- Catalogue Lumière vue n° 40 (two versions), 6 March 1896, at the Lumière factory in Lyon-Monplaisir. Three workers bring the wall down "in the presence of Auguste Lumière".
- It was projected the same day at the Photo-Club de Lyon.
- Opened: https://catalogue-lumiere.com/demolition-dun-mur-ii/ · https://catalogue-lumiere.com/demolition-dun-mur-i/
- The forward-and-reverse screenings are attested on https://en.wikipedia.org/wiki/D%C3%A9molition_d'un_mur

### Images

| Image | Item page | Hi-res | Holder · licence |
|---|---|---|---|
| Lumière, *Démolition d'un mur* (bank id `lumiere-demolition-mur-reversible`) | https://commons.wikimedia.org/wiki/File:D%C3%A9molition_d%27un_mur_(1897).webm | https://upload.wikimedia.org/wikipedia/commons/3/3e/D%C3%A9molition_d%27un_mur_%281897%29.webm (200, 137 MB) | Institut Lumière restoration via Commons · `{{PD-US-auto-expired\|1948}}`. Do **not** use the "(à l'envers)" file: its added soundtrack is non-free. |
| Optional, for D: Gilbert Stuart, *John Jacob Astor*, 1794 | https://commons.wikimedia.org/wiki/File:John_Jacob_Astor.jpg | https://upload.wikimedia.org/wikipedia/commons/0/01/John_Jacob_Astor.jpg (1643×1998) | Brook Club, New York · `{{PD-Art\|PD-old-auto-expired\|deathyear=1828}}`. Weak provenance: the Commons source is gilbert-stuart.org, not the holder. |
| Optional mythic rhyme: Joseph Wright of Derby, *Penelope Unraveling Her Web*, 1783–84. She unpicks her weaving every night to hold off a deadline. | https://commons.wikimedia.org/wiki/File:Joseph_Wright_of_Derby_-_Penelope_Unraveling_Her_Web_-_87.PA.49_-_J._Paul_Getty_Museum.jpg | https://upload.wikimedia.org/wikipedia/commons/6/64/Joseph_Wright_of_Derby_-_Penelope_Unraveling_Her_Web_-_87.PA.49_-_J._Paul_Getty_Museum.jpg (4095×3306) | J. Paul Getty Museum 87.PA.49 · `{{PD-Art\|PD-old-auto-expired\|deathyear=1797}}`, credited to Getty Open Content. The Getty page's own rights text was not read. |

### Shot concept: "The wall that won't come down"

The film plays forward, backward, forward, exactly as the code does now. A typewritten tag is **pinned** to the wall's face: `SAP ECC · SUPPORT ENDS 2020`.
1. **"Forward" (74.06): slide.** The film runs forward and the workers push. A yellow slab slides in: `FORWARD · MIGRATE BY 2020`.
2. **"SAP" (74.84–76.12): the fall.** The wall falls in dust and the tag goes down with it. The highlighter runs across SAP.
3. **"backward" (76.12): tear, then stamp.** The film reverses and the wall rises, carrying the tag back up. The date leaf **tears** off to show 2025, and an orange `EXTENDED` stamp lands. Slab: `BACKWARD · 2025 → 2027`.
4. **"repeat" (76.84–77.60, about 4 drawings): feed, then stamp.** The film runs forward again while the tag **feeds** like a tear-off calendar, 2027 → 2030 → 2033. On the last leaf a stamp lands: `TRANSITION OPTION`. Slab: `REPEAT · 2033`.

**Caption slip** (top, `capTop`)
```
Louis Lumière, Démolition d'un mur (vue n° 40), Lyon-Monplaisir, 1896. Institut Lumière restoration via Wikimedia Commons. Public domain.
SAP's old ERP, end of support: 2020 → 2025 (Oct 2014) → 2027/2030 (4 Feb 2020) → paid transition option to 2033 (4 Feb 2025).
Two of the extensions were announced on 4 February, five years apart.
```

### Flags
- **SAP founding date.** A search snippet says 1 April 1972, but sap.com returned 403. Wikipedia says June 1972. Leave the day off.
- **Year SAP moved to Walldorf.** Wikipedia says 1977; Computerwoche says "about 1980". Leave it off.
- **Film year.** The catalogue says 1896, Wikipedia 1895, and the Commons file is labelled 1897. Use the catalogue's 1896, as the current slip does.
- **Reverse projection.** Supported only by secondary sources; no 1896 programme was found.
- **EU public-domain year on the current slip.** The current slip says "In the EU public domain since 2025". The bank says Louis Lumière died in 1948, which gives 2019. 2025 is right only if Auguste (died 1954) counts as co-author. This also affects the `usine` slip. Pick one reading.

---

## L35 · "Build unicorns all the way!" · shot `byline`

- **Original:** "Just transformers all the way!".
- **Timings:** Build 110.18–110.64 · unicorns 110.64–112.52 (held note) · all 112.52–112.78 · the 112.78–112.92 · way 112.92–113.34.
- **Current shot:** a departures board of the transformer paper's authors. It no longer matches the lyric.

### Candidates

**A. The Unicorn Tapestries, woven in the Southern Netherlands, 1495–1505 (recommended)**
- **The series.** Seven hangings that tell one hunt, now at the Met Cloisters. Titles and accession numbers are from the Met API, where every piece returns `isPublicDomain: true` and the credit line "Gift of John D. Rockefeller Jr., 1937":
  - The Hunters Enter the Woods, 37.80.1
  - The Unicorn Purifies Water, 37.80.2
  - The Unicorn Crosses a Stream, 37.80.3
  - The Unicorn Defends Himself, 37.80.4
  - The Unicorn Surrenders to a Maiden, 38.51.1–2 (fragments)
  - The Hunters Return to the Castle, 37.80.5 (the kill, then the body carried slung over a horse)
  - The Unicorn Rests in a Garden, 37.80.6
  - API: https://collectionapi.metmuseum.org/public/collection/v1/objects/467642 (and 467637–467641, 467653)
- **Origin and sale.** "Made in the Southern Netherlands around 1495–1505", "very probably woven in Brussels". They "reportedly were used to cover potatoes" during the French Revolution, and "John D. Rockefeller Jr. bought them in 1922". https://en.wikipedia.org/wiki/The_Hunt_of_the_Unicorn
- **The Met's own text on the garden panel:** "The chain is not secure and the fence is low enough to leap over: The unicorn could escape if he wished." The red stains are pomegranate juice, not blood. https://artsandculture.google.com/asset/the-unicorn-in-captivity-from-the-unicorn-tapestries-unknown/6QHwPO4q4grNtA
- **Why it's meaningful.** A unicorn is made in Brussels, hunted, killed, carried off and fenced in a pen it could leap out of. Then the whole set is bought by an American (1922) and now hangs in New York. It is a European unicorn's life cycle, told in panels 500 years ago.

**B. The narwhal as unicorn (Ole Worm, Copenhagen)**
- ***Museum Wormianum*** (1655), p. 282, "Unicornu marinum". The text says the tusk "pro vero Unicornu habeatur & ematur": it is held, and bought, as true unicorn. Worm dates his sight of a skull with the tusk attached to 1636. Read on the page scan.
- **Reading's account.** The University of Reading dates the public proof to 1638: https://collections.reading.ac.uk/special-collections/2020/05/12/a-cabinet-of-curiosities-ole-worms-museum-wormianum-1655/
- **Rosenborg's throne.** "it was said to be made of unicorn horn, but in fact, the material is narwhal tooth". Made 1662–1671 and used at coronations until 1840. https://denkongeligesamling.dk/en/rosenborg/room/the-knights-hall
- **Why it's meaningful.** Europe priced unicorns above gold and seated its king on them, and they were whales all along.

**C. The word itself**
- **Coinage.** Aileen Lee, TechCrunch, 2 Nov 2013, "Welcome To The Unicorn Club": "39 companies", all US software companies, and "unicorns apparently don't exist". https://techcrunch.com/2013/11/02/welcome-to-the-unicorn-club/
- **Optional current tag.** Bending Spoons agreed to buy Miro on 10 Sep 2026 for $1.355bn EV, against a $17.5bn valuation.
  - https://techcrunch.com/2026/09/10/bending-spoons-to-buy-collaboration-tools-maker-miro-for-1-36b-90-less-than-its-2022-valuation/
  - https://investors.bendingspoons.com/newsroom/bending-spoons-agrees-to-acquire-miro
  - Caveat: Miro is headquartered in San Francisco and Amsterdam, so don't call it simply European.

### Images (The Met CC0 · via Met API `isPublicDomain: true`)

| Panel | Item page | Hi-res | Size |
|---|---|---|---|
| The Hunters Enter the Woods, 37.80.1 | https://www.metmuseum.org/art/collection/search/467637 | https://images.metmuseum.org/CRDImages/cl/original/DP118981.jpg | 3345×3792 |
| The Unicorn Purifies Water, 37.80.2 | https://www.metmuseum.org/art/collection/search/467638 | https://images.metmuseum.org/CRDImages/cl/original/DP118983.jpg | 3755×3658 |
| The Hunters Return to the Castle, 37.80.5 | https://www.metmuseum.org/art/collection/search/467641 | https://images.metmuseum.org/CRDImages/cl/original/DP118989.jpg | 3883×3699 |
| The Unicorn Rests in a Garden, 37.80.6 | https://www.metmuseum.org/art/collection/search/467642 | https://images.metmuseum.org/CRDImages/cl/original/DP118991.jpg | 2715×3848 |
| Fallback B: Worm's narwhal woodcut, p. 282 | https://archive.org/details/gri_museumwormia00worm/page/282/mode/1up | https://archive.org/download/gri_museumwormia00worm/page/n311.jpg | 1935×3000 page · Getty Research Institute via Internet Archive, "NOT_IN_COPYRIGHT" |

The tapestries are woven colour, not line art. Screen them as halftone with the photo treatment, or posterise them to two inks on the black bridge ground.

### Shot concept: "A unicorn's life, in four sheets"

1. **"Build" (110.18): slide.** *The Hunters Enter the Woods* slides in from the left onto the black ground, and BUILD lands as the poster lyric.
2. **"unicorns" (110.64–112.52, held): slide, then pin.** *The Unicorn Purifies Water* slides over it. The copy stand pans flat from the ring of spears to the kneeling unicorn while the highlighter runs the whole held note. About halfway (≈111.6) a yellow price tag is **pinned** to the unicorn's flank: `≥ $1,000,000,000`.
3. **"all the" (112.52): slide, then flip.** *The Hunters Return to the Castle* slides over, with the unicorn carried off slung over a horse. The tag **flips**: `ACQUIRED` (or `SOLD −92%` with the Miro caveat).
4. **"way!" (112.92): cut, then stamp.** Cut to *The Unicorn Rests in a Garden*. An orange stamp lands on the low fence: `WAY OUT →`. The gate is open. Hold.

**Caption slip**
```
South Netherlandish (woven), The Unicorn Rests in a Garden, from the Unicorn Tapestries, 1495–1505.
The Met Cloisters, Gift of John D. Rockefeller Jr., 1937. Public domain (CC0).
Woven in Brussels. Bought by an American in 1922.
```
- **Alternative deadpan (the Met's catalogue text):** `"The chain is not secure and the fence is low enough to leap over." (The Met)`

**Fallback (B), same timing:** Worm's narwhal slides in on "Build". On "unicorns" a tag is pinned: `HELD AND BOUGHT AS TRUE UNICORN`. On "way!" it is stamped `WHALE · 1636`.

### Flags
- **Met pages.** The item pages hit a bot check, so public-domain status rests on the Met API plus the Met's text as mirrored on Google Arts & Culture.
- **"Woven in Brussels."** Wikipedia says "very probably". If you want to be strict, use "Woven in the Southern Netherlands".
- **Worm's date.** 1638 comes from the Reading blog only; Worm's own text says 1636 for seeing the skull.
- **Throne date.** The royal house says 1660; the Royal Danish Collection says 1662–1671. No public-domain photo of the throne was verified.
- **Miro's discount.** $17.5bn was "late 2021" in TechCrunch's text but "2022" in its headline. The headline says "90% less", while the EV maths gives −92%.
- **Unverified.** The "Delaware flip" idea was not verified.

---

## L37 · "Build post AI trends" · shot `medley`

- **Original:** "Post-Chinchilla, super-dense".
- **Timings (estimated by word length over 115.20–117.02):** Build ≈115.20–115.74 · post ≈115.74–116.16 · AI ≈116.16–116.37 · trends ≈116.37–117.02.
- **Current shot:** a still of the Bubblers Medley, with the caption "The last bubble Europe led".
- **Reading of the lyric:** Europe builds *after* the trend. It arrives at the bubble as it bursts.

### Candidates

**A. Holland's 1720 bubble came late (recommended).** Frehen, Goetzmann & Rouwenhorst, "New Evidence on the First Financial Bubble", NBER w15332 (2009), published in *JFE* 108(3), 2013. Opened: https://www.nber.org/system/files/working_papers/w15332/w15332.pdf
- **What the paper says:**
  - "In the Netherlands, a number of new firms were capitalized in 1720, beginning in July with the creation of Stad Rotterdam and extending through October."
  - "The shares of Stad Rotterdam began trading in mid‑July, after the peak of the South Sea Company."
  - "…a flood of new issues at the end of September and the beginning of October; just as the global crisis hit London and the Netherlands… The Dutch new issues market lasted a brief two months."
  - "The financial bubble in Holland began later than the bubbles in France or Britain." and "No city wished to be left out."
- **Paris burst first.** "By May 21, Law was forced to deflate the value of banknotes and cut the stock price." NY Fed, Liberty Street Economics. Opened: https://libertystreeteconomics.newyorkfed.org/2014/01/crisis-chronicles-the-mississippi-bubble-of-1720-and-the-european-debt-crisis/
- **The Medley already says it.** Its top-left card, "The Dutch Bubblers", read off the hi-res scan: *"The Dutch, who once were thought to be / A crafty Generation, / Are grown as foolish now we see, / As any Neighb'ring Nation: / They coppy England, England, France, / In vile destructive Bubbles"*. The word "England" really is engraved twice.
- **A dated card.** The Medley also contains *The London Gazette* for "Tuesday August 16. 1720" (Old Style), with a Whitehall notice against "Stocks not Warranted by Law".
- **Why it's meaningful.** It is the earliest precise case of "build post-trend": Holland copied the scheme after Paris had burst and London had peaked. Its lasting product was the post-mortem book, *Het Groote Tafereel der Dwaasheid* ("The Great Mirror of Folly", Amsterdam, 1720).

**B. Neuer Markt, Frankfurt (1997–2003).** Germany's copy of Nasdaq.
- Bundesbank Discussion Paper 15/2010: "In March 1997, the Neuer Markt in Germany opened."
- It peaked on 10 March 2000 at 8,583 points (NEMAX All Share) and closed on 5 June 2003.
- Opened: https://web.archive.org/web/20130514195255/http://www.bundesbank.de/Redaktion/EN/Downloads/Publications/Discussion_Paper_1/2010/2010_07_23_dkp_15.pdf
- **Weaknesses:** no public-domain image, and it copied the trend rather than arriving late to it.

**C. The book as the product (an end beat for A).** Holland's lasting output from 1720 was the post-mortem. The title print of *Het Groote Tafereel der Dwaasheid* is headed "Spiegel des Papieren Waerelds" ("Mirror of the Paper World"). The Leviathan idea from the original treatment no longer fits the new lyric. Tulips don't rhyme either, because in 1637 the Dutch led the trend.

### Images (Rijksmuseum item pages say "Copyright: Public domain")

| Image | Item page | Hi-res | Size |
|---|---|---|---|
| *The Bubblers Medley … Europes Memorial for the Year 1720*. Anonymous; publisher Carington Bowles, London; **this impression 1766–1793** (after the 1720 design); RP-P-1905-6516 (in the bank) | https://www.rijksmuseum.nl/en/collection/RP-P-1905-6516 | https://iiif.micr.io/XijwS/full/max/0/default.jpg | 4376×5810 |
| *Het koffiehuis Quincampoix te Amsterdam*, 1720, RP-P-OB-83.514. The Kalverstraat coffeehouse, "het centrum van de actiehandel te Amsterdam"; the border names projects in Muiden, Utrecht, Harlingen, Weesp and Rotterdam | https://www.rijksmuseum.nl/en/collection/RP-P-OB-83.514 | https://iiif.micr.io/wxmzh/full/max/0/default.jpg | 5412×4264 |
| *De geest van Erasmus verlaat Rotterdam*, 1720, RP-P-OB-83.519. The windhandel drives Erasmus out of Rotterdam | https://www.rijksmuseum.nl/en/collection/RP-P-OB-83.519 | https://iiif.micr.io/HXRTT/full/max/0/default.jpg | 4396×5772 |
| Title print, *Tafereel der Dwaasheid*, Jacob Folkema after Arnold Houbraken, 1720, RP-P-AO-28-59-1 | https://www.rijksmuseum.nl/en/collection/RP-P-AO-28-59-1 | https://iiif.micr.io/tgGDJ/full/max/0/default.jpg | 4546×5838 |

### Shot concept: "Last card on the pile"

The set-up: the bridge's black field, with the poster lyric on the left. On the right, the Medley is rebuilt card by card at 6 fps, printed as line art. Every card is cropped from the one Medley scan, so no new asset is needed. Depth comes only from paper shadow.
1. **"Build" (≈115.20): slide, then stamp.** The rue Quincampoix card (Paris) slides in. An orange stamp lands: `PARIS · BURST MAY 1720`.
2. **"post" (≈115.74): feed, then stamp.** *The London Gazette* sheet **feeds** in over it, showing "AUGUST 16. 1720". A blue stamp lands: `LONDON · PAST PEAK`.
3. **"AI" (≈116.16): slide, then pin.** The "Dutch Bubblers" card slides in last and lands crooked on top. A typewritten slip is **pinned** under it: "They coppy England, England, France".
4. **"trends" (≈116.37–117.02): stamp.** An orange stamp lands on the Dutch card: `OPENED JULY 1720 · CLOSED OCT 1720`.
5. **Optional, on the cut to L38: fold.** The pile **folds** shut into the *Tafereel* title print, "Mirror of the Paper World".

**Caption slip**
```
The Bubblers Medley, or a Sketch of the Times: Being Europes Memorial for the Year 1720.
Anon., publ. Carington Bowles, London, impression 1766–93. Rijksmuseum, Amsterdam. Public domain.
Holland floated its companies from July 1720, after Paris had crashed. The market lasted two months.
```

### Flags
- **"~40 Dutch companies" is not verified.** The paper speaks of "more than thirty traded companies" plus about forty more firms. Don't print a count.
- **South Sea peak date.** Not independently checked; the claim rests on the NBER phrase "after the peak". The `CLOSED OCT 1720` stamp follows the paper's "through October" and "two months". If you want the stamp to say November, find a source first.
- **Coffeehouse name.** That the Amsterdam coffeehouse was named after the Paris street is inference, not stated on the Rijksmuseum page.
- **Unopened sources.** The Harvard Baker (South Sea Bubble collection) and Yale Beinecke pages could not be opened.
- **Impression date.** The slip must give the impression date (1766–93), not only 1720. The current slip omits it.
- **The current slip's line** "The last bubble Europe led" is fair for 1720 as a whole, but it tells the opposite story from the new lyric (Europe late, not leading). Replace it with the "after Paris had crashed" line.

---

## L40 · "EU Inc fixes things soon" · shot `euinc`

- **Original:** "RLHF goes askew".
- **Timings (estimated by word length over 120.76–124.52):** EU ≈120.76–121.14 · Inc ≈121.14–121.70 · fixes ≈121.70–122.64 · things ≈122.64–123.77 · soon ≈123.77–124.52.
- **Current shot:** an EU–INC form whose 27 boxes tick, stamped `SOON` / `SINCE 2024`.

### Candidates

**A. The company form Europe keeps re-proposing, 1970 → 2026 (recommended)**
- **European Company (SE).** Council Regulation (EC) No 2157/2001 "of 8 October 2001 on the Statute for a European company (SE)". Opened: https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX%3A32001R2157%3AEN%3AHTML
  - Recital 9: "Since the Commission's submission in 1970 of a proposal … amended in 1975".
  - Art. 70: "This Regulation shall enter into force on 8 October 2004."
- **Exact 1970 date.** "Proposal presented on June 30, 1970, O.J. 1970, C 124/1" (German Law Journal, footnote 2). Opened: https://www.cambridge.org/core/journals/german-law-journal/article/european-company-a-challenge-to-academics-legislatures-and-practitioners/40A023B41E910DD9B03C9FB2234ED5B7
- **Where the idea started.** Pieter Sanders' inaugural lecture in Rotterdam, 1959, "Naar een Europese Naamlooze Vennootschap?". The regulation followed "approximately 40 years later". The same document lists SAP among the best-known German SEs, a quiet link to L24.
  - Opened: https://cdn.arbitration-icca.org/s3fs-public/document/media_document/pietersanders_100_years_english.pdf
  - Erasmus University: https://www.eur.nl/en/esl/events/piet-sanders-lecture-series-2022/about-piet-sanders
- **European Private Company (SPE).** COM(2008) 396, 25 June 2008. EUR-Lex: "Date of end of validity: 21/05/2014; Withdrawn". Opened: https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:52008PC0396
- **Single-member company (SUP).** COM(2014) 212, 9 April 2014. EUR-Lex: "end of validity: 04/07/2018; Withdrawn". Opened: https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=celex:52014PC0212
- **EU Inc.** Commission, 18 March 2026: "founding an EU Inc. company within 48 hours, for less than €100", with agreement called for "by the end of 2026". Opened: https://commission.europa.eu/news-and-media/news/eu-inc-making-business-easier-european-union-2026-03-18_en
  - The petition launched on 14 Oct 2024: https://techcrunch.com/2024/10/27/founders-and-vcs-back-a-pan-european-c-corp-but-an-eu-inc-has-a-rocky-road-ahead/
  - Status: "1,418 amendments … dated 22 July 2026". No committee vote had been scheduled as of 29 Sep; the Irish presidency wants trilogues in November. https://the28thregime.eu/progress
- **Why it's meaningful.** 31 years from proposal to adoption, then two withdrawn successors, then "soon". It is the DELAY meter in company law, and it lands right before hook 4 flips the board to ON TIME.

**B. The metre: "À tous les temps, à tous les peuples" (1793 → 1840)**
- **Dates.** Law of 18 Germinal an III (7 April 1795). The platinum metre dedicated "to all times and all men" was deposited in 1799. The system was "exclusively adopted with the law of 4 July 1837", from 1 January 1840. Opened: https://metrologie-francaise.lne.fr/en/metrology/history-units
- **The reversal.** Napoleon's 1812 decree on *mesures usuelles* partly undid it. Wikipedia only: https://en.wikipedia.org/wiki/Mesures_usuelles
- **The object.** Musée Carnavalet ND4508, a medal by Ludovic Penin, 1840.
  - Obverse: "A TOUS LES TEMPS A TOUS LES PEUPLES … DECRET DU 14 THERMIDOR AN 1 [1 Aug 1793] … 1. JANVIER 1840 USAGE EXCLUSIF DES MESURES DECIMALES. LOI DU 4 JUILLET 1837."
  - Reverse: "UNITE DES MESURES".
  - It is a medal celebrating a 47-year wait for one European standard, and it rhymes with EU Inc's "One Europe. One Standard."

**C. The oldest known share: VOC, Enkhuizen chamber, 9 Sep 1606** (brief)
- Six city chambers merged into one company.
- Commons credits the Westfries Archief and marks it public domain.
- The 20 March 1602 charter date was not verified.
- The VOC's colonial history makes it a risky punchline. Not recommended.

### Images

| Image | Item page | Hi-res (curl-checked) | Holder · licence |
|---|---|---|---|
| Ludovic Penin, medal commemorating the law of 4 July 1837 on decimal measures, 1840 (obverse; reverse also available) | https://www.parismuseescollections.paris.fr/fr/musee-carnavalet/oeuvres/commemoration-de-la-loi-du-4-juillet-1837-sur-l-usage-des-mesures-decimales | https://www.parismuseescollections.paris.fr/sites/default/files/atoms/images/CAR/lpdp_70242-29.jpg (3000×2243); reverse `…/CAR/lpdp_70689-50.jpg` (5401×4038) | Musée Carnavalet · CC0 |
| *Usage des nouvelles mesures*, Labrousse after Delion, 15 March 1800 (bank id `usage-nouvelles-mesures-1800`) | https://www.parismuseescollections.paris.fr/fr/musee-carnavalet/oeuvres/usage-des-nouvelles-mesures | https://www.parismuseescollections.paris.fr/sites/default/files/atoms/images/CAR/aze_carg023035_001.jpg (1300×2048; Commons has a larger copy) | Musée Carnavalet · CC0 (per the bank; only the URL was re-checked) |
| VOC share, 9 Sep 1606 | https://commons.wikimedia.org/wiki/File:VOC_aandeel_9_september_1606.jpg | https://upload.wikimedia.org/wikipedia/commons/e/ed/VOC_aandeel_9_september_1606.jpg (1826×1329) | Westfries Archief, Hoorn · Public domain (Commons) |
| Official Journal L 294, 10.11.2001 (Reg. 2157/2001), as a document | EUR-Lex link above | n/a | © European Union: **not public domain**, reusable with acknowledgement. The EUR-Lex legal notice itself could not be opened. |

### Shot concept: "One standard, soon" (A, with the medal from B as the bottom card)

The medal is the shot's one archival object, so it carries the caption slip. The forms are drawn by us in Courier Prime. Every stamp except SOON is pre-printed, because "EU" and "Inc" last only 2–3 drawings.
1. **Cut, on the beat before 120.76: pin.** Penin's 1840 medal is **pinned** to the black ground: "À TOUS LES TEMPS, À TOUS LES PEUPLES".
2. **"EU" (≈120.76): slide.** A typewritten sheet slides over it: `PROPOSAL · STATUTE FOR A EUROPEAN COMPANY · 30.06.1970`. It already carries a blue stamp, `ADOPTED 08.10.2001`, and a margin tag, `31 YEARS`.
3. **"Inc" (≈121.14): slide.** `EUROPEAN PRIVATE COMPANY · COM(2008) 396` slides on top, with an orange stamp: `WITHDRAWN 21.05.2014`.
4. **"fixes" (≈121.70): slide.** `SINGLE-MEMBER COMPANY · COM(2014) 212` follows, stamped `WITHDRAWN 04.07.2018`.
5. **"things" (≈122.64): slide, then tick.** The existing EU–INC form (18.03.2026) lands on top. Its 27 boxes tick one row per drawing at 6 fps, and the footer types `1,418 AMENDMENTS`.
6. **"soon" (≈123.77–124.52): stamp.** The orange `SOON` stamp lands at the start of the held note. Change the sub-line from `SINCE 2024` to `SINCE 1970`. Through the hold the stamp changes only through the registration re-rolls. Then hook 4 cuts to PÜNKTLICH.

If this is too dense for 3.8 s, drop step 1 and the SPE sheet. The core is 1970 → 2001, SUP withdrawn, then SOON.

**Caption slip**
```
Ludovic Penin, medal for the law of 4 July 1837 on decimal measures, 1840. Musée Carnavalet, Paris. CC0.
One standard for Europe: decreed 1793, compulsory 1 January 1840. European Company: proposed 1970, adopted 2001.
EU Inc, 2026: incorporation within 48 hours.
```

### Flags
- **OJ C 124 (1970).** The date that issue was published is not verified. Don't confuse it with "OJ C 124, 21.5.1990", which is Parliament's 1990 opinion.
- **1966 Sanders draft.** Not found.
- **The 1,418 amendments.** The project notes (`research/zeitgeist.md`) say "by 17 Jul", but the source dates them 22 July 2026.
- **Motto attribution.** Crediting the motto to Condorcet was not verified; the motto itself is on the medal.
- **The 1812 decree.** Sourced from Wikipedia only.
- **Timings.** These are the least certain of all five lines. Check where "soon" really sits in the EU vocal.
