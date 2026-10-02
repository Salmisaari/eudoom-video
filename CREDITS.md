# Credits

## Song

- **"I'm Upping My P(doom)".** The lyrics are by [osmarks](https://docs.osmarks.net/hypha/p%28doom%29_song_objectively_correct_interpretation), built on an opening verse and chorus by [MusicPerson](https://www.udio.com/creators/MusicPerson), with lines suggested on the EleutherAI Discord and help from Claude. The original was generated with Udio and released in November 2024 ([YouTube](https://www.youtube.com/watch?v=uEB5E67vcPA)).
- **The "Claude-Pop" version**, made with Suno, was posted by [deckard (@slimer48484)](https://x.com/slimer48484/status/2097752569212756134) in September 2026.
- **The EU edition** (`audio/pdoom_eu.mp3`): 21 lines rewritten and re-sung into the Claude-Pop recording with ElevenLabs Music inpainting, spliced in line by line.
- The MIT license covers this repo's code. The song and lyrics stay with the people above.

## Code

- The renderer, the timing pipeline and the repository layout are built on [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video) by Giacomo Magnanini (MIT; see `LICENSE` and `app/LICENSE.mexicat`). This repo adds the four-ink print pass (`app/src/engine/print.ts`), the EU edition scenes (`app/src/scenes/`), the EU timing map (`analysis/timing_eu.py`) and the song pipeline (`audio/el_music/`).

## Fonts

All fonts are under the SIL Open Font License 1.1; see `app/public/fonts/LICENSES.md`. Archivo, Barlow Condensed, Cormorant, Courier Prime, Noto Serif Display, UnifrakturMaguntia, IBM Plex Mono; single-stroke EMS and Hershey fonts (OFL / public domain).

## Images and film

Plates in `app/public/animatic/img/` and frames in `app/public/animatic/film/`. They are public domain or CC0 (one LANL photo with attribution).

| File | Work | Author / holder | Licence | Source | Note |
|---|---|---|---|---|---|
| `bruegel-big-fish` | Big Fish Eat Little Fish MET DP825754.jpg | Pieter van der Heyden after Pieter Bruegel the Elder, 1557; The Met | CC0 | [link](https://commons.wikimedia.org/wiki/File:Big_Fish_Eat_Little_Fish_MET_DP825754.jpg) |  |
| `bruegel-fall-of-icarus` | Landscape with the Fall of Icarus | After Pieter Bruegel the Elder (possibly an early copy of a lost original), c. 1560s (Commons: 1582–1625); Royal Museums of Fine Arts of Belgium, Brussels | Public domain | [link](https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_Landscape_with_the_Fall_of_Icarus_-_Brussels,_Royal_Museums_of_Fine_Arts_of_Belgium_-_Google_Arts_%26_Culture.jpg) |  |
| `carreno-charles-ii` | Charles II of Spain by Juan Carreño de Miranda.jpg | Juan Carreño de Miranda; Musée des Beaux-Arts de Valenciennes | Public domain | [link](https://commons.wikimedia.org/wiki/File:Charles_II_of_Spain_by_Juan_Carre%C3%B1o_de_Miranda.jpg) |  |
| `chappe-telegraph-burned-by-mob` | Le peuple brûle le télégraphe de Chappe (Fig. 10), from Louis Figuier, 'Les Merveilles de la science', vol. 2 | Louis Figuier (author; illustrator unnamed), 1868 (depicts 1791–92); Printed book (Wikisource/Commons scan of the Figuier djvu) | Public domain | [link](https://commons.wikimedia.org/wiki/File:T2-_d029_-_Fig._10._%E2%80%94_Le_peuple_br%C3%BBle_le_t%C3%A9l%C3%A9graphe_de_Chappe.png) |  |
| `durer-rhinoceros-1515` | The Rhinoceros | Albrecht Dürer, 1515; The Metropolitan Museum of Art, New York (60.708.157) | Public domain | [link](https://www.metmuseum.org/art/collection/search/388482) |  |
| `frankenstein-frontispiece-1831` | Frontispiece to Mary Shelley, 'Frankenstein' (revised edition) | Theodor von Holst (engraved by William Chevalier), 1831; Print in a private collection, Bath (as exhibited at Tate Britain; image via Wikimedia Commons) | Public domain | [link](https://commons.wikimedia.org/wiki/File:Frontispiece_to_Frankenstein_1831.jpg) |  |
| `friedrich-wanderer` | Wanderer above the Sea of Fog, c. 1818 | Caspar David Friedrich; Hamburger Kunsthalle | Public domain | [link](https://commons.wikimedia.org/wiki/File:Caspar_David_Friedrich_-_Wanderer_above_the_sea_of_fog.jpg) |  |
| `furst-schnabel` | Paul Fürst, Der Doctor Schnabel von Rom (Holländer version).png | Paul Fürst, 1656 | Public domain | [link](https://commons.wikimedia.org/wiki/File:Paul_F%C3%BCrst,_Der_Doctor_Schnabel_von_Rom_(Holl%C3%A4nder_version).png) |  |
| `heyden-land-of-cockaigne` | The Land of Cockaigne (after Pieter Bruegel the Elder) | Pieter van der Heyden, after Pieter Bruegel the Elder, after 1570?; The Metropolitan Museum of Art, New York (26.72.44) | Public domain | [link](https://www.metmuseum.org/art/collection/search/338703) |  |
| `holbein-utopia-1518` | Utopia Woodcut (Holbein, 1518).jpg | Ambrosius Holbein, in Thomas More, Utopia (Basel, 1518) | Public domain | [link](https://commons.wikimedia.org/wiki/File:Utopia_Woodcut_(Holbein,_1518).jpg) | cropped to the woodcut |
| `jacquard-woven-silk-portrait` | Joseph Marie Jacquard (woven silk portrait, 'A la mémoire de J. M. Jacquard') | Didier, Petit et Cie (woven by Michel-Marie Carquillat after Claude Bonnefond), 1839; The Metropolitan Museum of Art, New York (31.124) | Public domain | [link](https://www.metmuseum.org/art/collection/search/222531) |  |
| `leonardo-water` | Leonardo da Vinci - RCIN 912661, Studies of water c.1510-12.jpg | Leonardo da Vinci, c. 1510–12; Royal Collection Trust | Public domain | [link](https://commons.wikimedia.org/wiki/File:Leonardo_da_Vinci_-_RCIN_912661,_Studies_of_water_c.1510-12.jpg) |  |
| `marey-ibry-train-graph-1885` | Ibry's Visual Train Schedule.png | Ibry, in É.-J. Marey, La Méthode graphique, 1885 | Public domain | [link](https://commons.wikimedia.org/wiki/File:Ibry%27s_Visual_Train_Schedule.png) |  |
| `mazzanti-pinocchio` | Pinocchio.jpg | Enrico Mazzanti, 1883 | Public domain | [link](https://commons.wikimedia.org/wiki/File:Pinocchio.jpg) |  |
| `mitchell-world-map-1864` | 1864 Mitchell Map of the World on Mercator Projection - Geographicus - World-mitchell-1864.jpg | S. Augustus Mitchell, 1864; Geographicus | Public domain | [link](https://commons.wikimedia.org/wiki/File:1864_Mitchell_Map_of_the_World_on_Mercator_Projection_-_Geographicus_-_World-mitchell-1864.jpg) |  |
| `montparnasse-derailment-1895` | Accident de train de la gare Montparnasse du 22 octobre 1895 | Hippolyte Blancard, 1895; Musée Carnavalet – Histoire de Paris (PH78193) | CC0 | [link](https://www.parismuseescollections.paris.fr/fr/musee-carnavalet/oeuvres/accident-de-train-de-la-gare-montparnasse-du-22-octobre-1895-14e-15e) |  |
| `nobel-portrait` | Alfred Nobel (Bain).png | Bain News Service; Library of Congress | Public domain | [link](https://commons.wikimedia.org/wiki/File:Alfred_Nobel_(Bain).png) |  |
| `nokia-paper-mill` | MECHELIN(1894) p201 Nokia, Paper Mill.jpg | Plate from Leopold Mechelin, Finland in the Nineteenth Century (1894), p. 201, captioned Nokia Paper-Mill. British Library HMNTS 10290.i.4, Mechanical Curator c | Public domain | [link](https://commons.wikimedia.org/wiki/File:MECHELIN(1894)_p201_Nokia,_Paper_Mill.jpg) |  |
| `panini-modern-rome` | Modern Rome (picture gallery) | Giovanni Paolo Panini, 1757; The Metropolitan Museum of Art, New York (52.63.2) | Public domain | [link](https://www.metmuseum.org/art/collection/search/437245) |  |
| `piranesi-carceri-round-tower` | The Round Tower, from 'Carceri d'invenzione' (Imaginary Prisons) | Giovanni Battista Piranesi, ca. 1749–50; The Metropolitan Museum of Art, New York (37.45.3(27)) | Public domain | [link](https://www.metmuseum.org/art/collection/search/337725) |  |
| `racknitz-turk-hidden-operator` | The Turk, Tab. III: cutaway showing the hidden operator (from 'Ueber den Schachspieler des Herrn von Kempelen und dessen Nachbildung') | Joseph Friedrich zu Racknitz, 1789; Humboldt-Universität zu Berlin, University Library (scan via Wikimedia Commons) | Public domain | [link](https://commons.wikimedia.org/wiki/File:Racknitz_-_The_Turk_3.jpg) |  |
| `teilhard-fig3` | Teilhard de Chardin - Le phénomène humain.djvu | Pierre Teilhard de Chardin, Le Phénomène humain (Seuil, 1955) | Public domain | [link](https://commons.wikimedia.org/wiki/File:Teilhard_de_Chardin_-_Le_ph%C3%A9nom%C3%A8ne_humain.djvu) | djvu page 190 (book p. 172), Fig. 3, Schéma symbolisant le développement des Primates; cropped |
| `teilhard-point-omega` | Teilhard de Chardin - Le phénomène humain.djvu | Pierre Teilhard de Chardin, Le Phénomène humain (Seuil, 1955) | Public domain | [link](https://commons.wikimedia.org/wiki/File:Teilhard_de_Chardin_-_Le_ph%C3%A9nom%C3%A8ne_humain.djvu) | djvu page 304 (book p. 286), heading 1. La convergence du personnel et le point Oméga; cropped |
| `vonneumann-badge` | John von Neumann, Los Alamos ID badge photo | Los Alamos National Laboratory | Attribution (LANL) | [link](https://commons.wikimedia.org/wiki/File:JohnvonNeumann-LosAlamos.jpg) | credit LANL |
| `film/usine (frames)` | La Sortie de l'usine Lumière à Lyon (first version) | Louis Lumière, 1895; Institut Lumière restoration, Blu-ray 'Lumière, le cinématographe 1895–1905' (file via Wikimedia Commons) | Public domain | [link](https://commons.wikimedia.org/wiki/File:La_Sortie_de_l%27Usine_Lumi%C3%A8re_%C3%A0_Lyon_I_1895.webm) | frames extracted from the film |
| `film/wall (frames)` | Démolition d'un mur (shown forwards, then in reverse) | Louis Lumière, 1896 (version of 1897); Institut Lumière restoration (file via Wikimedia Commons) | Public domain | [link](https://commons.wikimedia.org/wiki/File:D%C3%A9molition_d%27un_mur_(1897).webm) | frames extracted from the film |
| `caselli-pantelegraph` | Le pantélégraphe Caselli (fig. 73), in Louis Figuier, Les Merveilles de la science, vol. 2, 1868 | Louis Figuier | Public domain | [link](https://commons.wikimedia.org/wiki/File:T2-_d160_-_Fig._73._%E2%80%94_Le_pant%C3%A9l%C3%A9graphe_Caselli.png) |  |
| `caselli-writing-sample` | Exemple d'écriture du pantélégraphe Caselli (fig. 75), in Figuier, 1868 | Louis Figuier | Public domain | [link](https://commons.wikimedia.org/wiki/File:T2-_d163_-_Fig._75._%E2%80%94_Exemple_d%E2%80%99%C3%A9criture_du_pant%C3%A9l%C3%A9graphe_Caselli.png) |  |
| `bruegel-census-bethlehem` | The Census at Bethlehem (The Numbering at Bethlehem), 1566 | Pieter Bruegel the Elder; Royal Museums of Fine Arts of Belgium (Google Art Project) | Public domain | [link](https://commons.wikimedia.org/wiki/File:Pieter_Bruegel_the_Elder_-_The_Numbering_at_Bethlehem_-_Google_Art_Project.jpg) |  |
| `richter-haensel-gretel` | Hänsel und Gretel vor dem Hexenhaus, wood engraving | Ludwig Richter | Public domain | [link](https://commons.wikimedia.org/wiki/File:1903_Ludwig_Richter.jpg) |  |
| `lanfroicourt-border-postcard` | Frontière franco-allemande à Manhoué–Lanfroicourt, postcard, c. 1910 | Anonymous | Public domain | [link](https://commons.wikimedia.org/wiki/File:Le_poteau_fronti%C3%A8re_%C3%A0_Lanfroicourt).jpg) |  |
| `medley-card-quincampoix / -gazette / -dutch` | The Bubblers Medley, or a Sketch of the Times: Being Europe's Memorial for the Year 1720 (impression 1766–93), three cards cropped | Rijksmuseum | Public domain | [link](https://www.rijksmuseum.nl/en/collection/RP-P-1905-6516) | cropped |
| `penin-metric-medal-1840` | Medal for the law of 4 July 1837 on decimal measures, 1840 | Ludovic Penin; Musée Carnavalet | CC0 | [link](https://www.parismuseescollections.paris.fr/fr/musee-carnavalet/oeuvres/commemoration-de-la-loi-du-4-juillet-1837-sur-l-usage-des-mesures-decimales) |  |
| `punch-paul-pry-1844` | Punch, vol. 7, 1844 (Paul Pry at the Post Office) | Punch | Public domain | [link](https://archive.org/details/sim_punch_1844_7/page/n10/mode/1up) |  |
| `unicorn-hunters-enter / -purifies-water / -in-garden / -hunters-return` | The Unicorn Tapestries, South Netherlandish, 1495–1505 | The Met Cloisters (Open Access) | CC0 | [link](https://en.wikipedia.org/wiki/The_Hunt_of_the_Unicorn) | see the Met collection pages for each panel |
| `daumier-vingt-cinq-degres-1852` | Un jour où l'on ne paye pas. Vingt-cinq degrés de chaleur, Le Charivari, 17 May 1852 | Honoré Daumier; The Met | CC0 | [link](https://commons.wikimedia.org/wiki/File:A_Day_When_You_Do_Not_Pay%E2%80%93Twenty-Five-Degree_Heat_(Un_jour_ou_l%27on_ne_paye_pas._Vingt-cinq_degres_de_chaleur_),_from_Le_Public_du_Salon,_published_in_Le_Charivari,_May_17,_1852_MET_DP808259.jpg) | |
| `galileo-moon-1610` | Sidereus Nuncius, Venice, 1610: the half moon | Galileo Galilei; Smithsonian Libraries | Public domain | [link](https://library.si.edu/image-gallery/68453) | |

### Eurovision (L12)

The Liverpool stage in L12 is drawn in code, after the broadcast of the grand final (13 May 2023). No photograph is used.
