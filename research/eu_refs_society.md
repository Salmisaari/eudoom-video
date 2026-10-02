# EU edition: society references for L16, L19, L22, L26, L34 (+ hooks, L28)

Research 30 Sep 2026 for the director's note: each new section tells a story in motion, with precise, historically meaningful references. No code changed.

**How to read this**
- "Verified" means I opened the page (or its API record, or the PDF) and read the fact there. Anything seen only in a search snippet, or not found, is in **Flags**.
- Image rights follow `research/archive.md`: OK worldwide = PD in the EU and the US, with a CC0/PDM or faithful-2D reproduction.
- Beat times are the animatic's current word times.
  - `data/eu_words.json` is empty (`{}`), so `relyric()` splits the old words' span by letter count.
  - Re-check every sync point against the sung EU take before building.

| Line | Words (s), as the animatic currently sets them |
|---|---|
| L16 | I 49.56 · feel 49.66 · my 50.00 · AC 50.27 · temperatures 50.43 · rearranging 51.38–52.83 |
| L19 | I 60.58 · hear 60.71 · the 60.95 · basic 61.10 · income 61.55 · gloom 62.09–62.54 |
| L22 | One 66.22 · E 66.42 · thirty 66.52 · faxes 66.98 · a 67.34 · second 67.44–69.76 |
| L26 | Sharp 81.21 · left 81.80 · overseas 82.00 · and 82.72 · there 82.96 · you 83.48 · are 83.93–85.00 |
| L34 | Open 105.96 · Europe 106.31 · borders 106.84 · blues 107.46–108.45 (the evacard cuts at 108.55) |
| L28 | NATO 89.28 · please 90.64 · don't 92.46 · let 92.94 · me 93.32 · go 94.30–95.47 |

---

## L16 "I feel my AC temperatures rearranging" (shot `bubble`, paper, 12 fps)

The current shot is CERN bubble tracks with a cookie-law caption. It has nothing to do with AC, so replace it.

### References (verified)
1. **Spain, Real Decreto-ley 14/2022, art. 29** (1 Aug 2022; BOE núm. 184, 2 Aug 2022).
   - Rule: no cooling below **27 °C** and no heating above **19 °C**.
   - Scope: administrative buildings, shops, cinemas, stations and airports.
   - Buildings must display *"carteles explicativos de las medidas obligatorias de ahorro"*.
   - Temporary: in force until 1 Nov 2023.
   - Sources: https://www.boe.es/buscar/act.php?id=BOE-A-2022-12925
2. **The 2003 heatwave, and Europe's answer.**
   - The toll: more than 70,000 additional deaths in 16 European countries (Robine et al., *C. R. Biologies* 331:171–178, 2008). In France, excess deaths reached about 14,800 by 20 Aug (INSERM, Hémon & Jougla, 25 Sep 2003: "14 800 le 20 août").
   - Answer 1: the **law of 30 June 2004** created the *journée de solidarité*. Pentecost Monday became a worked, unpaid day; it raised €3.5bn in 2025.
   - Answer 2: the **arrêté of 7 July 2005** requires every nursing home to have a fixed cooling system or at least one cooled room (*"une pièce rafraîchie"*).
   - Context: 19% of European households had AC in 2022, against 90% in the US (IEA data via Euronews).
   - Sources:
     - https://comptes-rendus.academie-sciences.fr/biologies/articles/10.1016/j.crvi.2007.12.001/
     - https://www.inserm.fr/wp-content/uploads/2017-11/inserm-rapportthematique-surmortalitecaniculeaout2003-rapportetape.pdf
     - https://www.franceinfo.fr/replay-radio/le-vrai-du-faux/vrai-ou-faux-la-journee-de-solidarite-creee-apres-la-canicule-de-2003-n-a-t-elle-pas-du-tout-servi-a-climatiser-les-ehpad_8060588.html
     - https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000633683
     - https://www.euronews.com/2024/06/18/air-conditioning-use-has-more-than-doubled-in-europe-since-1990
3. **Celsius's scale was born upside down, and Germany set its own limit.**
   - In 1742 Anders Celsius (Uppsala) set **0 = boiling and 100 = freezing**. It was reversed after his death in 1744; some credit Linnaeus.
   - In his 1742 paper, the calibration step puts the thermometer in melting snow (*"i kram Snö"*) and cites "Tab. VII".
   - Germany's EnSikuMaV (in force 1 Sep 2022 to 15 Apr 2023) capped public offices at **19 °C**, 18 °C for standing work and 12 °C for heavy work.
   - Sources:
     - https://www.lindahall.org/about/news/scientist-of-the-day/anders-celsius/
     - 1742 volume: https://archive.org/details/KonglSwenskaWetenkapsAcademiensVol3
     - https://www.haufe.de/oeffentlicher-dienst/personal-tarifrecht/massnahmen-zum-energiesparen-im-oeffentlichen-dienst-in-kraft_144_574180.html

### Images
- **→ Honoré Daumier, *Un jour où l'on ne paye pas. Vingt-cinq degrés de chaleur*** (Le Public du Salon, *Le Charivari*, 17 May 1852).
  - Lithograph, Met 1980.1114.2. A crowd sweats in the Salon on a free day.
  - Item page: https://www.metmuseum.org/art/collection/search/355825
  - Hi-res: https://images.metmuseum.org/CRDImages/dp/original/DP808259.jpg (2.4 MB; the link resolves).
  - Rights: Met Open Access; the API returns `isPublicDomain: true`.
  - Daumier died in 1879, so the work is PD everywhere: **OK worldwide**. The item page itself returned 429 to my fetch, so the check rests on the API.
- **Celsius's own 1742 thermometer figure** (0 at the top, 100 at the ice point).
  - Commons: https://commons.wikimedia.org/wiki/File:Celsius_original_thermometer.png (Public domain).
  - Hi-res: https://upload.wikimedia.org/wikipedia/commons/a/ad/Celsius_original_thermometer.png
  - Only 63×427 px, so redraw it as line art. I could not find the Tab. VII plate in the IA scan of the 1742 volume; its fold-outs are other plates.
- Alternate: **Willis Carrier, "Apparatus for Treating Air", US Patent 808,897**, 2 Jan 1906 (Buffalo).
  - Holder: National Archives (NAID 7268013).
  - Page: https://docsteach.org/document/patent-treating-air/ ("Public Domain, Free of Known Copyright Restrictions", PDM 1.0).
  - Hi-res drawing: https://patentimages.storage.googleapis.com/65/90/66/df3edc322cbd28/US808897.pdf
  - AC was invented in America; Europe regulates its setting.

### Shot concept: "280 years of rearranging the thermometer" (→ pick)
1. **Cut (beat before 49.56):** the Daumier sheet slides onto the right half, and the crowd sweats.
   - A tall paper thermometer card is pinned beside it, drawn in line as Celsius's figure: numbered 0 to 150 top to bottom, with the modern numbers printed on its back.
   - Its orange mercury rises in 12 fps steps under "I feel my".
2. **"AC" (50.27):** a BOE sheet ("Real Decreto-ley 14/2022 · art. 29") slides in under the print, overlapping its bottom edge.
3. **"temperatures" (50.43):** two stamps hit the thermometer: orange **`27 °C MÍN.`** (cooling), then blue **`19 °C MÁX.`** (heating).
4. **"rearranging" (51.38–52.83):** the thermometer card **flips** end over end (a paper flip on the beat), and the numbers are now the right way up.
   - The two stamps stay put, so 27 and 19 now sit in the wrong places.
   - The mercury drops back to the other end.

Caption slip:
> Honoré Daumier, *Un jour où l'on ne paye pas — Vingt-cinq degrés de chaleur*, *Le Charivari*, 17 May 1852. The Met, Public Domain.
> Spain, Real Decreto-ley 14/2022, art. 29: no air conditioning below 27 °C (2 Aug 2022). Anders Celsius, Uppsala, 1742: 0 = boiling, 100 = freezing.
> *In 1852, 25 degrees was a cartoon. In 2022, 27 was the law.*

**Alternative (darker): "The heatwave rearranged the calendar."**
- On "AC", a nursing-home floor plan with one room stamped `PIÈCE RAFRAÎCHIE (1)` (2005).
- On "temperatures", a calendar leaf, "Lundi de Pentecôte", is stamped `TRAVAILLÉ` (2004).
- On "rearranging", the holiday slides out of the calendar.
- Deadpan line: *"70,000 dead. The answer: one cool room and one more working day."*
- It is strong, but the tone may be too grim for the chorus lead-in.

### Flags
- Sánchez, Moncloa, 29 Jul 2022 (Fortune): "I'm not wearing a tie and I have asked my ministers not to."
  - This is an English translation. I did not verify the Spanish original, and the Majorca Daily Bulletin gives a different wording.
  - Don't set it as a quote unless the Spanish text is sourced.
- *Vingt-cinq degrés* in 1852 may be Réaumur, not centigrade. Don't convert it; just print "25 degrees".
- The IEA's own commentary didn't carry the EU AC share. The 19% figure is IEA via Euronews.

---

## L19 "I hear the basic income gloom" (shot `basicincome`, orange, 12 fps; about 2 s)

The current shot is the Kela letter with a €560 stamp on "gloom". It is accurate but static: nothing happens to the idea.

### References (verified)
1. **Switzerland, 5 June 2016.**
   - The initiative "Für ein bedingungsloses Grundeinkommen" was rejected by **76.9% No** (1,896,963 votes) to 23.1% Yes (568,905). Turnout was 46.4%, and **no canton** voted in favour; the best was Basel-Stadt at 36%.
   - Three weeks earlier, on 14 May 2016, campaigners unrolled the world's largest poster on the Plaine de Plainpalais, Geneva: **72 × 110 m, about 8,000 m²**.
   - It read *"What would you do if your income were taken care of?"*, with the question in 68 languages round the edge.
   - Afterwards the tarp was **made into bags and wallets**.
   - Sources:
     - https://www.srf.ch/news/schweiz/abstimmungen/abstimmungen/grundeinkommen/wuchtiges-nein-zum-bedingungslosen-grundeinkommen
     - https://www.swissinfo.ch/eng/making-a-big-statement_basic-income-poster-makes-guinness-book/42155334
2. **Finland (Kela), 1 Jan 2017 to 31 Dec 2018.**
   - 2,000 unemployed people aged 25–58 got €560 a month, tax-free. They were drawn at random from benefit recipients in Nov 2016.
   - Final results (6 May 2020): **+6 days of employment** (78 on average), and better wellbeing and trust.
   - Kela wanted to extend the trial to employed people, and the government didn't. Instead its "activation model" tightened conditions from 1 Jan 2018 and was repealed from 2020.
   - Sources:
     - https://stm.fi/en/-/perustulokokeilun-tulokset-tyollisyysvaikutukset-vahaisia-toimeentulo-ja-psyykkinen-terveys-koettiin-paremmaksi
     - https://basicincome.org/news/2018/04/finland-going-through-a-basic-income-experiment/
     - https://valtioneuvosto.fi/en/-/1271139/aktiivimalli-on-kumottu-vuoden-2020-alusta-alkaen (title and snippet only)
3. **The European pedigree.**
   - Juan Luis Vives, *De subventione pauperum* (Bruges, 1526): BIEN calls him "the true father of the idea of a publicly administered minimum income scheme".
   - BIEN itself was founded in Louvain-la-Neuve in September 1986, as the *Basic Income European Network*.
   - BIEN explicitly says More's *Utopia* (1516) is **not** a basic income: subsistence came with compulsory labour.
   - Source: https://basicincome.org/history/

### Images
- **→ Pieter van der Heyden after Bruegel, *The Land of Cockaigne*** (after 1570). Already in the bank as `heyden-land-of-cockaigne`.
  - Met 26.72.44, CC0.
  - Item page: https://www.metmuseum.org/art/collection/search/338703
  - Hi-res: https://images.metmuseum.org/CRDImages/dp/original/DP818319.jpg
  - A knight, a peasant and a scholar asleep under the table: the voters' fear, drawn in 1567.
- Alternate: **Ambrosius Holbein, *The Island of Utopia*** (woodcut, 1518). Folger scan on Commons.
  - Page: https://commons.wikimedia.org/wiki/File:Utopia_Woodcut_(Holbein,_1518).jpg
  - Hi-res: https://upload.wikimedia.org/wikipedia/commons/a/ad/Utopia_Woodcut_%28Holbein%2C_1518%29.jpg (1168×1536).
  - Licence tag: `{{Licensed-PD-Art|PD-old-100|cc-by-sa-4.0}}`. It is PD-Art in the EU (DSM Art. 14) and the US; Folger claims CC BY-SA elsewhere.
  - Treat as OK worldwide, with a courtesy credit.

### Shot concept: "The poster, the nap, the no" (→ pick)
1. **Cut (beat before 60.58), and "hear" (60.71):** the giant poster fills the right half, and the copy stand pans across it at 12 fps.
   - It carries our own typesetting of the text only, no campaign logo: WHAT WOULD YOU DO IF YOUR INCOME WERE TAKEN CARE OF? Tiny repeats in other languages run along its edge.
2. **"basic income" (61.10–62.09):** the poster **folds** down along its middle crease, revealing the Cockaigne engraving underneath, with three men asleep.
3. **"gloom" (62.09):** a Swiss ballot slip slams onto the sleepers, stamped **`NEIN 76,9 %`** in black and blue. The folded poster slides out of frame as a small wallet shape.

Caption slip:
> Pieter van der Heyden after Pieter Bruegel, *The Land of Cockaigne*, after 1570. The Met, Public Domain.
> Switzerland, 5 June 2016: unconditional basic income rejected, 76.9% No; no canton in favour. Three weeks earlier, Geneva unrolled the world's largest poster.
> *Afterwards the poster was cut into wallets. It found work.*

**Keep-Kela alternative** (it pays off chorus 2's "FI last"):
- On "hear", the Kela letter slides in. On "income", the €560 stamp.
- On "gloom", a second stamp: **`ENDED 31.12.2018 · NOT EXPANDED`**.
- Caption: *"Result: +6 days of work a year, less stress. Not continued."*

### Flags
- The Guinness page 404s, so the exact "8,115.53 m²" appears only in search snippets. Use swissinfo's "about 8,000 m² (72 × 110 m)".
- "Not extended" is loose. The trial ran its full planned term, and the government declined Kela's proposed **expansion**. The stamp above says "NOT EXPANDED" for that reason.
- Not verified: the 2013 Bern stunt with 8 million five-rappen coins. Don't use it.

---

## L22 "One E thirty faxes a second" (shot `leibniz`, orange, 12 fps)

The current shot is Leibniz's machine with a 1→30 FAXES/S counter. The counter works; the machine is the wrong machine.

### References (verified)
1. **Caselli's pantelegraph: Europe invented the commercial fax.**
   - Napoleon III saw a demonstration on 10 May 1860 and secured the telegraph lines.
   - The first pantelegram went Lyon to Paris on 10 Feb 1862.
   - Official **Paris–Lyon service began on 16 Feb 1865**. It was extended to Marseille in 1867 and ran until 1870.
   - One sheet, 111 × 27 mm with about 25 handwritten words, took **108 seconds**: about 10⁻² faxes a second.
   - Source: https://en.wikipedia.org/wiki/Pantelegraph (citing Huurdeman 2003 and Burns 2004).
2. **Covid by fax.**
   - Until DEMIS (June 2020), lab reports reached German health offices *"per Fax und auf anderen Wegen"* and were typed in by hand.
   - DEMIS became mandatory for SARS-CoV-2 lab reports on 1 Jan 2021.
   - Source: Diercke, Claus, Rexroth, Hamouda (RKI), *Bundesgesundheitsblatt*, Apr 2021. https://europepmc.org/article/PMC/PMC8042625
3. **The Bundestag unplugs.**
   - In Nov 2023 the Budget Committee ordered every fax machine out of the Bundestag's buildings by **30 June 2024**.
   - The Bundestag **kept a fax number** for citizens.
   - Source: https://www.egovernment.de/schluss-mit-faxen-bundestag-stellt-geraete-ab-a-a70875efb696a25b84c8141bff85b70f/

### Images (same source family as the bank's Chappe plates)
- **→ Figuier, *Les Merveilles de la science*, vol. 2 (1868), Fig. 73, *Le pantélégraphe Caselli*.**
  - The tall cast-iron pendulum machine.
  - Page: https://commons.wikimedia.org/wiki/File:T2-_d160_-_Fig._73._%E2%80%94_Le_pant%C3%A9l%C3%A9graphe_Caselli.png
  - Hi-res: https://upload.wikimedia.org/wikipedia/commons/2/2d/T2-_d160_-_Fig._73._%E2%80%94_Le_pant%C3%A9l%C3%A9graphe_Caselli.png (2740×2721).
  - Licence: `{{PD-old-100-1923}}`, **OK worldwide**.
- **→ Fig. 75, *Exemple d'écriture du pantélégraphe Caselli*.** A real transmitted sheet in visible scan lines.
  - It reads: "Exposition Universelle de 1867 · Appareil autographique de Mr l'abbé Caselli · Paris 1er Avril 1867".
  - Page: https://commons.wikimedia.org/wiki/File:T2-_d163_-_Fig._75._%E2%80%94_Exemple_d%E2%80%99%C3%A9criture_du_pant%C3%A9l%C3%A9graphe_Caselli.png
  - Hi-res: https://upload.wikimedia.org/wikipedia/commons/a/a2/T2-_d163_-_Fig._75._%E2%80%94_Exemple_d%E2%80%99%C3%A9criture_du_pant%C3%A9l%C3%A9graphe_Caselli.png (1767×761, 1-bit).
  - Licence: `{{PD-old-100-1923}}`, **OK worldwide**.
  - It is already halftone-ready, since the scan lines are the image.

### Shot concept: "From one fax per 108 seconds to 10³⁰" (→ pick; it replaces the Leibniz plate)
1. **Cut:** Fig. 73 slides in on the right. Its pendulum is a separate paper cut-out pinned at the pivot.
2. **"One" (66.22):** the pendulum makes one swing, and a counter card below reads `1 FAX / 108 s · PARIS–LYON 1865`.
3. **"E thirty" (66.42–66.98):** the counter flaps through its exponents (flap board) to **`10³⁰ FAXES / s`**, as the shot does now.
4. **"faxes" (66.98):** the receiver **feeds** out a paper strip, the Fig. 75 sheet, scan lines and all.
5. **"second" (67.44–69.76, held):** the strip keeps feeding at 60 fps, the world's clock, and along its margin a date ticker runs 1865 … 1970 … 2020.
   - The last sheet out is a typewritten `SARS-CoV-2 · LABORMELDUNG · PER FAX`, and the Official stamps it `EINGEGANGEN` at 6 fps.

Caption slip:
> Louis Figuier, *Les Merveilles de la science*, vol. 2, 1868: Caselli's pantelegraph. Public domain.
> Paris–Lyon, 16 Feb 1865: the world's first fax service, one sheet every 108 seconds. Germany, 2020: Covid lab results still reached health offices by fax.
> *The Bundestag unplugged its last fax on 30 June 2024. It kept the number.*

Beware the overlap: L10 ("faxes zoom") and L15 (thermal-paper fax) already use fax. This shot is the origin story, so keep the 1865 plate visually distinct from the green-LCD office fax of L15.

### Flags
- Alexander Bain's 1843 British patent (no. 9745, 27 May 1843) appears only in search snippets; Britannica returned 403. Leave Bain out, or verify first.
- The pantelegraph dates and the 108 s figure come from Wikipedia citing Huurdeman and Burns, and I did not read those books. The IEEE paper "The Caselli pantelegraph and its successors, 1859–1871" would confirm them, but its page was empty to my fetch.

---

## L26 "Sharp left overseas and there you are" (shot `ariane`, blue, Europe at 6 fps)

The current shot draws Ariane 501's veer with an OPERAND ERROR stamp. It fitted "sharp left turn"; the new word "overseas" isn't used yet.

### References (verified)
1. **Stieglitz, *The Steerage*: going the other way.**
   - It was photographed in June 1907 aboard the **SS Kaiser Wilhelm II, sailing New York to Bremen**.
   - It is often read as immigrants arriving, but the passengers were **going back to Europe**.
   - The Cleveland Museum of Art says "immigrants returning to Europe"; Wikipedia says they were probably skilled workers on temporary stays.
   - 1907 was Ellis Island's busiest year, with over a million people processed and only 2% excluded (Statue of Liberty–Ellis Island Foundation).
   - Ellis Island opened on 1 Jan 1892 and processed almost 12 million people before closing in 1954 (NPS).
   - Doctors chalked letters on coats, such as "B" for back, "F" for face and "H" for heart (NPS).
   - Sources:
     - https://openaccess-api.clevelandart.org/api/artworks/2019.22
     - https://en.wikipedia.org/wiki/The_Steerage
     - https://www.statueofliberty.org/ellis-island/overview-history/
     - https://www.nps.gov/elis/learn/historyculture/places_immigration.htm
     - https://www.nps.gov/elis/learn/historyculture/people_doctor.htm
2. **Europe's spaceport is overseas.**
   - French Guiana is an EU outermost region (Art. 349 TFEU).
   - De Gaulle announced Kourou on 21 Mar 1964. The first launch (Véronique) was on 9 Apr 1968, and the first Ariane on 24 Dec 1979.
   - **Ariane 501** (4 June 1996) veered at about H0+37 s and broke up at about H0+39 s, at around 4,000 m.
   - Its debris fell over **about 12 km² east of the pad, "nearly all mangrove swamp or savanna"**: still inside the EU.
   - The cause was software reused from Ariane 4, where a 64-bit float converted to a 16-bit signed integer (BH) overflowed (Lions report, 19 July 1996).
   - Sources:
     - https://regions-and-cities.ec.europa.eu/policy/themes/outermost-regions_en
     - https://centrespatialguyanais.cnes.fr/en/ambition-nationale-devenue-europeenne
     - https://www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report
     - https://www-users.cse.umn.edu/~arnold/disasters/ariane5rep.html

### Images
- **→ Alfred Stieglitz, *The Steerage*, 1907, photogravure.** Cleveland Museum of Art 2019.22 (gift of Diann G. and Thomas A. Mann).
  - Item page: https://clevelandart.org/art/2019.22
  - Hi-res: https://openaccess-cdn.clevelandart.org/2019.22/2019.22_print.jpg (1.9 MB), or the TIFF: https://openaccess-cdn.clevelandart.org/2019.22/2019.22_full.tif (113 MB).
  - The museum's open-access API says `share_license_status: CC0`.
  - Stieglitz died in 1946 (PD in the EU since 2017), and the image was published in 1911 (PD in the US): **OK worldwide**.
  - Commons copy: https://commons.wikimedia.org/wiki/File:Alfred_Stieglitz_(American,_1864-1946)_-_The_Steerage_-_2019.22_-_Cleveland_Museum_of_Art.jpg (CC0).
  - Don't use the Met's copies: the Met marks its Steerage prints **not** Open Access.
- For the Kourou version, no PD image was found. The BnF/Gallica coastal maps of Kourou carry non-commercial terms. Keep the engine-drawn trajectory.

### Shot concept: "Claude travels steerage, to Europe" (→ pick)
The print's diagonal gangway splits it in two; Europe's clock is 6 fps.

1. **Cut (beat before 81.21):** *The Steerage* slides in on the right half. A small paper heading card is pinned to the rail: `NEW YORK →`.
2. **"Sharp" (81.21) and "left" (81.80):** the heading card **flips** to `← BREMEN`. The whole print rotates a quarter-turn left on the copy stand, a hard paper turn with no easing.
3. **"overseas" (82.00–82.72):** a long blue paper strip, the Atlantic, **feeds** across the bottom third right to left at 6 fps, and a cut-out liner rides it.
4. **"there you are" (82.96–85.00):** a cut-in to the lower deck, where the orange idol stands among the straw hats.
   - She is the only orange figure in a black-and-blue crowd, and the only person in frame not in the 1907 photo.
   - On "are", the caption slip types in.

Caption slip:
> Alfred Stieglitz, *The Steerage*, 1907. Cleveland Museum of Art, CC0.
> SS Kaiser Wilhelm II, New York to Bremen, June 1907. 1907 was Ellis Island's busiest year: over a million people, the other way.
> *Often read as an arrival. They were going back.*

**Alternative: keep the Ariane plate but give it the overseas payoff.**
- On "left", the veer, as now.
- On "overseas", the grid becomes an outline map strip labelled `KOUROU · GUYANE · EU`.
- On "there you are", debris dots fall inside a hatched patch labelled `≈12 km² · MANGROVE`.
- New caption: *"Ariane 501, Kourou, 4 June 1996. The debris landed in the EU. It is in South America."*

### Flags
- The "brain drain" numbers (researcher emigration and similar) were not researched. Keep the line about 1907, which is verified.
- Busiest-day figures (11,747 on 17 Apr 1907) appear only in search snippets.

---

## L34 "Open Europe borders blues" (shot `mondrian`, bleached paper, chorus 3 "August")

The current shot is Mondrian, where blue floods on "blues". It's graphic, but it's no longer the lyric.

### References (verified)
1. **Schengen, 14 June 1985.**
   - The agreement was signed aboard the **MS *Princesse Marie-Astrid***, moored on the Moselle at Schengen, at the triple border of Luxembourg, France and Germany.
   - Signatories: Belgium, Germany, France, Luxembourg and the Netherlands. They signed the Convention on 19 June 1990, and it came into force in 1995.
   - The **boat was sold to Germany in 1992** and ran as *MS Regensburg* on the Danube for about three decades.
   - Schengen bought it back in 2021, and it was renamed *Prinzessin Marie-Astrid Europa* (inaugurated 14 June 2025).
   - Today: 29 Schengen countries, and over 3.5 million people cross internal borders each day.
   - Sources:
     - https://luxembourg.public.lu/en/society-and-culture/international-openness/schengen-40-ans-histoire-europe-bateau-.html
     - https://home-affairs.ec.europa.eu/policies/schengen/schengen-area_en
2. **"Temporary."** The Commission's official list of member-state notifications of temporary internal border controls (Art. 25 and 28 et seq., Schengen Borders Code, edition dated 21/09/2026):
   - It runs to **508 notifications**, starting with No. 1: France, 21/10/2006.
   - **No. 442, Germany, 16/09/2024 to 15/03/2025:** borders with **France, Belgium, the Netherlands, Luxembourg** and Denmark. Those are all four other countries that signed on the boat.
   - The first German controls were at the Austrian border on 13 Sep 2015 (de Maizière).
   - Sources:
     - https://home-affairs.ec.europa.eu/document/download/11934a69-6a45-4842-af94-18400fd274b7_en?filename=Full-list-MS-notifications_en.pdf
     - https://www.euronews.com/2015/09/13/germany-introduces-temporary-controls-along-austrian-border
3. **Before Schengen, the Moselle border was a handshake at a post.**
   - An anonymous postcard shows the Franco-German border post at Manhoué–Lanfroicourt. French and German officials shake hands at the post, on the line between France and annexed Moselle before WWI.

### Images
- **→ Anonymous postcard, *Frontière Franco-Allemande à Manhoué – Lanfroicourt*** (c. 1907–14; it carries a 5c Semeuse stamp).
  - Page: https://commons.wikimedia.org/wiki/File:Le_poteau_fronti%C3%A8re_%C3%A0_Lanfroicourt).jpg
  - Hi-res: https://upload.wikimedia.org/wikipedia/commons/b/b4/Le_poteau_fronti%C3%A8re_%C3%A0_Lanfroicourt%29.jpg (1556×990).
  - Tag: `{{cc-zero}}`, with source and author "unknown".
  - An anonymous postcard published before 1914 is PD in the EU (anonymous, more than 70 years since publication) and in the US (published before 1931). **OK worldwide, with the rights chain flagged.**
- Bank alternates (Rijksmuseum, PDM):
  - `chodowiecki-arrested-no-passport`, 1780: a traveller detained for having no passport.
  - `passport-netherlands-1822`.

### Shot concept: "The boat, the barrier, notice No. 508" (→ pick; about 2.5 s, 4 beats)
1. **Cut:** a blue paper strip, the Moselle, crosses the frame, and three torn map pieces (LU · FR · DE) meet at a point in the river. A paper boat, `PRINCESSE MARIE-ASTRID · 14.06.1985`, is pinned there. Top right, the Lanfroicourt postcard is pinned, with its striped post.
2. **"Open" (105.96):** a striped barrier arm, cut from the postcard's post, **swings up** on its pin.
3. **"Europe" (106.31):** five small signature stamps land on a treaty slip on the boat: `BE · DE · FR · LU · NL`.
4. **"borders" (106.84):** the arm **drops**. A notice is pinned to it: `NOTIFICATION No. 442 · 16.09.2024 · FR · BE · NL · LU`, which lists all four other boat countries.
5. **"blues" (107.46–108.45):** the boat is unpinned and slides off down the strip toward the Danube, since it was sold to Germany in 1992.
   - The river's blue ink floods the frame, keeping the current "blue floods on 'blues'" beat, and a last stamp lands in the flood: **`TEMPORARY · No. 508`**.

Caption slip:
> Anonymous postcard, *Frontière Franco-Allemande à Manhoué–Lanfroicourt*, c. 1910. Public domain.
> Schengen, 14 June 1985: signed on a boat on the Moselle, where Luxembourg, France and Germany meet. 16 Sep 2024: Germany checks its borders with France, Belgium, the Netherlands and Luxembourg.
> *Everyone else who was on the boat.*

### Flags
- L24 already spends the joke: `wall` prints "BACKWARD · BORDER CHECKS 2024 · REPEAT · EVERY SIX MONTHS". Either change L24's words, or let L24 stay generic and keep the specific payoff (No. 442 and No. 508) for L34.
- The 508 count is from the list edition dated 21/09/2026. It will grow; re-check before release.
- I did not verify the Zollverein "barriers raised at midnight, 1 Jan 1834" scene (the Treitschke passage), so it's not used.
- I did not independently verify the annexation years of Moselle for the caption. The postcard's own caption and the Commons description are the only source, so the caption above avoids dates.

---

## Optional: hooks and L28, where something is clearly stronger

**Hooks (DELAY meter): one precise tweak for hook 4.**
- Deutsche Bahn counts a train as **"pünktlich" if it is at most 5 min 59 s late**. Long-distance punctuality was 54.2% in August 2026.
  - Source: https://www.deutschebahn.com/de/konzern/konzernprofil/zahlen_fakten/puenktlichkeitswerte-6878476
- So at hook 4 the board can flip to **`+5:59 · PÜNKTLICH`** instead of `ON TIME`. Europe is "on time" and still late.
- It also makes L4's `+5` retroactively punctual. Everything else in the hooks stays.

**L28 "NATO, please don't let me go" (gate B42 WASHINGTON DC): the treaty has a let-me-go clause, and it points to Washington.**
- North Atlantic Treaty (Washington, 4 Apr 1949), **Art. 13**: after twenty years, any party may leave "one year after its notice of denunciation has been given to the Government of the United States of America"; **Art. 14**: the treaty is deposited in the US archives.
  - Source: https://www.nato.int/cps/en/natohq/official_texts_17120.htm
- US law since the FY2024 NDAA, §1250A (22 U.S.C. §1928f): a president may not withdraw without two-thirds of the Senate or an Act of Congress.
  - Source: https://www.everycrsreport.com/reports/LSB11256.html
- Image: the treaty itself, page 7 (Arts. 12–14 in English and French), National Archives via DPLA, Public domain (US government record).
  - Page: https://commons.wikimedia.org/wiki/File:North_Atlantic_Treaty_-_DPLA_-_2bb23f2936372ce9f2c3189856e8b49d_(page_7).tiff
  - Hi-res: https://upload.wikimedia.org/wikipedia/commons/7/77/North_Atlantic_Treaty_-_DPLA_-_2bb23f2936372ce9f2c3189856e8b49d_%28page_7%29.tiff (10282×6836).
- Beats:
  1. "NATO": the treaty page slides in beside the gate.
  2. "please": the highlighter runs along Art. 13.
  3. "don't let me": an envelope, `To the Government of the United States of America`, is fed toward the gate slot.
  4. "go": the flap board flips to `NOTICE PERIOD · 1 YEAR`.
- Slip line: *"Since Dec 2023, US law says the president can't leave without the Senate."*
- Flags:
  - The NDAA's enactment date (22 Dec 2023) appears only in snippets.
  - Don't use Ismay's "keep the Americans in…" line. It is widely attributed, but I found no primary place and date, which the quote rule needs.

---

## Picks at a glance
- **L16:** Daumier's 1852 "25 degrees" Salon, the BOE 27 °C decree stamps, and the Celsius thermometer flipping on "rearranging".
- **L19:** the Geneva poster folds to reveal Cockaigne, then `NEIN 76,9 %` on "gloom".
- **L22:** Caselli's pantelegraph (Paris–Lyon 1865, 108 s a sheet); the counter climbs to 10³⁰; the strip feeds into a 2020 Covid fax.
- **L26:** *The Steerage* (1907, New York to Bremen); the heading card flips left, and the idol is aboard going to Europe.
- **L34:** the Schengen boat at the tripoint; the barrier drops with notice No. 442 (the other four boat countries); the boat sails off, and blue floods with `TEMPORARY · No. 508`.
- **Optional:** hook 4 `+5:59 · PÜNKTLICH`; L28 Art. 13 of the treaty.
