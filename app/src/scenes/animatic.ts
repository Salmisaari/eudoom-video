// Animatic v0 for "I'm Upping My P(doom) — EU Edition": every line's planned shot as a printed plate,
// cut on the beat grid, lyrics set from the aligned word timings. The idol is drawn in ink by the
// engine (_idol.ts) and lip-syncs from the letter-aligned mouth chart (data/visemes.json).
import type * as THREE from 'three';
import { Scene, type Frame } from '../engine/scene';
import { Layer2D, clearRT } from '../engine/gl';
import { C, ink } from '../engine/palette';
import { F, font, smart } from '../engine/type';
import { clamp, ease, prog, hash } from '../engine/util';
import type { Line, Lyrics, Word } from '../engine/lyrics';
import {
  W, H, type Ctx, type Treat, loadImage, img, drawImageAt, coverScale, fitScale, setFont, textW, fitSize,
  lineFor, posterLyric, slamLyric, slipLyric, captionSlip, stamp, flapBoard, idol, idolBust, MouthChart, twelve, sheet, wordProg,
} from './_kit';

const IMG = (id: string) => `animatic/img/${id}.jpg`;

type LyricMode = 'poster' | 'slam' | 'slip' | 'hook' | 'none';
interface ShotDef {
  id: string;
  at: number | string; // seconds | 'L7' (beat before line 7) | 'L1:eyes' (start of that word in line 1)
  draw: string;
  img?: string;
  treat?: Treat;
  lyric?: LyricMode;
  bg?: string; fg?: string; hl?: string;
  cap?: string[];
  p?: Record<string, any>;
}

// Section inks: verse 1 blue, chorus 1 yellow, verse 2 paper, chorus 2 orange, verse 3 blue,
// chorus 3 bleached paper, bridge black, chorus 4 all inks, outro gold.
const BLUE = { bg: C.blue, fg: C.paper, hl: C.yellow };
const YEL = { bg: C.yellow, fg: C.black, hl: C.orange };
const PAP = { bg: C.paper, fg: C.black, hl: C.yellow };
const ORA = { bg: C.orange, fg: C.black, hl: C.yellow };
const BLK = { bg: C.black, fg: C.paper, hl: C.yellow };

const SHOTS: ShotDef[] = [
  { id: 'eye', at: 'L1', draw: 'eye', lyric: 'slam', ...BLUE },
  { id: 'frank', at: 'L1:agi', draw: 'frank', img: 'frankenstein-frontispiece-1831', treat: 'line', lyric: 'slip', ...PAP,
    cap: ['Theodor von Holst, frontispiece to Frankenstein, 1831. PD.', '“I saw the dull yellow eye of the creature open.”', 'Written at Lake Geneva, 1816.'] },
  { id: 'chappe', at: 'L2', draw: 'plateRight', img: 'chappe-telegraph-burned-by-mob', treat: 'line', lyric: 'poster', ...BLUE,
    cap: ['Louis Figuier, Les Merveilles de la science, 1868. PD.', 'Paris, 1791–92: the crowd burns Chappe’s telegraph, twice,', 'sure it is signalling the enemy. Europe’s first techlash.'] },
  { id: 'egg', at: 'L3', draw: 'egg', lyric: 'poster', ...BLUE, cap: ['Chocolate egg, toy inside. Legal in the EU.', 'Banned in the US since 1938 (FD&C Act).'] },
  { id: 'db', at: 'L4', draw: 'dbBoard', lyric: 'poster', ...BLUE },
  { id: 'turk', at: 'L5', draw: 'plateRight', img: 'racknitz-turk-hidden-operator', treat: 'line', lyric: 'poster', ...BLUE,
    cap: ['J. F. von Racknitz, 1789: how Kempelen’s chess “automaton” (Vienna, 1770) worked. A person inside. PD.', 'Amazon named its Mechanical Turk after it, 2005: “artificial artificial intelligence”.', '2026: the one inside is an agent.'] },
  { id: 'bureau', at: 'L6', draw: 'bureau', lyric: 'slip', ...PAP },
  { id: 'bigfish', at: 'L6:eat', draw: 'bigfish', img: 'bruegel-big-fish', treat: 'line', lyric: 'slip', ...PAP,
    cap: ['Pieter van der Heyden after Bruegel, Big Fish Eat Little Fish, 1557. The Met, CC0.', 'Hugging Face → NVIDIA, 3 Sep 2026: $12,930,300,000.', '129303 = U+1F917, the hugging-face emoji.'] },
  { id: 'hook1', at: 'L7', draw: 'hook', lyric: 'hook', ...YEL, p: { n: 1 } },
  { id: 'foom', at: 'L8', draw: 'foom', img: 'montparnasse-derailment-1895', treat: 'photo', lyric: 'none', ...YEL,
    cap: ['Gare Montparnasse, 22 October 1895. Musée Carnavalet, CC0.', 'The Granville express was running late', 'and tried to make up time.'] },
  { id: 'trilogue', at: 'L9', draw: 'trilogue', lyric: 'poster', ...YEL,
    cap: ['AI Act trilogue, Brussels, 6–8 December 2023: 22 hours, a night, then another day.', 'Deal just before midnight, 8 December (AFP; TechCrunch).', '“A marathon negotiation by all standards.” (negotiator, via TechCrunch, 8 Dec 2023)'] },
  { id: 'rhinofax', at: 'L10:where', draw: 'rhinofax', lyric: 'poster', ...YEL,
    cap: ['Albrecht Dürer, The Rhinoceros, woodcut, 1515. The Met, Open Access.', 'Drawn in Nuremberg from a letter and a sketch sent from Lisbon. He never saw one.', '“They also say that the rhinoceros is fast, merry and jovial.” (the woodcut’s inscription)'] },
  { id: 'pinocchio', at: 'L11', draw: 'plateRight', img: 'mazzanti-pinocchio', treat: 'line', lyric: 'poster', ...YEL,
    cap: ['Enrico Mazzanti, Le avventure di Pinocchio, 1883. PD.', 'A wooden model that wants to be real.', 'The nose is an interpretability tool.'] },
  { id: 'street', at: 'L12', draw: 'street', lyric: 'poster', ...YEL },
  { id: 'icarus', at: 'L13', draw: 'icarus', img: 'bruegel-fall-of-icarus', treat: 'color', lyric: 'slip', ...PAP,
    cap: ['Pieter Bruegel the Elder (attr.), Landscape with the Fall of Icarus, c. 1560.', 'Royal Museums of Fine Arts, Brussels. PD.'] },
  { id: 'navier', at: 'L14:singularity', draw: 'navier', img: 'leonardo-water', treat: 'photo', lyric: 'poster', ...PAP,
    cap: ['Leonardo da Vinci, Studies of water, c. 1510–12. Royal Collection. PD.', 'Navier (1822), Stokes (1845). 8 Sep 2026: an AI group claims the forced blow-up;', 'the method came from Madrid. Unforced: still open.'] },
  { id: 'fax', at: 'L15', draw: 'fax', lyric: 'poster', ...PAP },
  { id: 'heat', at: 'L16', draw: 'heat', lyric: 'poster', ...PAP,
    cap: ['Honoré Daumier, Vingt-cinq degrés de chaleur, Le Charivari, 17 May 1852. The Met, PD.', 'Summer 2022: Italy, public buildings no cooler than 27 °C minus 2 °C (DL 17/2022, art. 19-quater);', 'Spain, 27 °C (RDL 14/2022, art. 29); Greece, 27 °C. In 1852, twenty-five degrees was a cartoon.'] },
  { id: 'cookies', at: 'L17', draw: 'cookies', lyric: 'slip', ...PAP,
    cap: ['Ludwig Richter, Hänsel und Gretel vor dem Hexenhaus, wood engraving, 19th c. PD.', 'Grimm, 1812: the house “ganz aus Brod gebaut und mit Kuchen gedeckt”.', 'EU Court of Justice, C-673/17, 1 Oct 2019: a pre-ticked box is not consent.'] },
  { id: 'hook2', at: 'L18', draw: 'hook', lyric: 'hook', ...ORA, p: { n: 2 } },
  { id: 'basicincome', at: 'L19', draw: 'basicincome', lyric: 'poster', ...ORA,
    cap: ['Pieter van der Heyden after Bruegel, The Land of Cockaigne, after 1570. The Met, PD.', 'Switzerland, 5 June 2016: basic income rejected, 76.9% No. Geneva had unrolled the world’s largest poster.', 'Afterwards the poster was cut into wallets. It found work.'] },
  { id: 'mill', at: 'L20', draw: 'mill', lyric: 'none', ...ORA,
    cap: ['Nokia Paper-Mill, in L. Mechelin, Finland in the Nineteenth Century, 1894, p. 201. PD. Galileo, Sidereus Nuncius, 1610.', 'Tampere, 12 May 1865: Fredrik Idestam’s groundwood mill; Nokia Ab, 1871.', 'IM-2, 6 March 2025: Nokia’s network ran 25 minutes on the moon, the lander on its side. No call was made.'] },
  { id: 'omega', at: 'L21:omega', draw: 'omega', lyric: 'poster', ...ORA,
    cap: ['Pierre Teilhard de Chardin (1881–1955), French Jesuit, coined the Omega Point.', 'In the EU public domain since 1 January 2026.'] },
  { id: 'pantelegraph', at: 'L22', draw: 'pantelegraph', lyric: 'poster', ...ORA,
    cap: ['Louis Figuier, Les Merveilles de la science, vol. 2, 1868: Caselli’s pantelegraph. PD.', 'Paris–Lyon, 1865: the first fax service, one sheet every 108 seconds. Germany, 2024: 77 % of companies still fax (Bitkom).', 'The Bundestag unplugged its last fax on 30 June 2024. It kept the number.'] },
  { id: 'milchkanne', at: 'L23', draw: 'milchkanne', lyric: 'poster', ...ORA,
    cap: ['Anja Karliczek, Federal Minister of Education and Research, Reuters TV, 21 November 2018.', 'Her next sentence: „Um in die Fläche zu gehen, können wir uns ein bisschen Zeit lassen.“', '(“To reach the countryside, we can take a little time.”)'] },
  { id: 'wall', at: 'L24', draw: 'wall', lyric: 'none', ...BLUE, p: { capTop: true },
    cap: ['Louis Lumière, Démolition d’un mur, Lyon, 1896: shown forwards, then backwards. Public domain.', 'SAP’s old ERP, end of support: 2020 → 2025 → 2027 → 2030 → 2033.', 'Two of the extensions were announced on 4 February, five years apart.'] },
  // v10: L25 is the original again ("Now von Neumann's obsolete", the user: still a European reference)
  { id: 'neumann', at: 'L25', draw: 'neumann', img: 'vonneumann-badge', treat: 'photo', lyric: 'poster', ...BLUE,
    cap: ['John von Neumann at Los Alamos. Los Alamos National Laboratory.', 'Born in Budapest, 1903. Princeton from 1930: one of the “Martians”,', 'the Hungarian minds Europe exported.'] },
  { id: 'flight', at: 'L26', draw: 'flight', lyric: 'slip', ...BLUE, p: { capTop: true },
    cap: ['S. Augustus Mitchell Jr., Map of the World on the Mercator Projection, Philadelphia, 1864. Wikimedia Commons, PD.', 'Its subtitle: “Exhibiting the American Continent as its Centre.” On it, a left turn from Brussels is west.', 'Sharp left turn: a model’s capabilities generalise, its alignment doesn’t (N. Soares, 2022).'] },
  { id: 'census', at: 'L27', draw: 'census', lyric: 'poster', ...BLUE,
    cap: ['Pieter Bruegel the Elder, The Census at Bethlehem, 1566. Royal Museums of Fine Arts of Belgium, Brussels. PD.', 'Hesse, 1970: the world’s first data protection law. Karlsruhe, 15 Dec 1983: the census ruling.', 'In 1566 the scribe just wrote it down.'] },
  { id: 'gate', at: 'L28', draw: 'gate', lyric: 'slip', ...PAP },
  { id: 'hook3', at: 'L29', draw: 'hook', lyric: 'hook', ...PAP, p: { n: 3 } },
  { id: 'chair', at: 'L30', draw: 'chair', lyric: 'slip', ...BLK },
  { id: 'usine', at: 'L31', draw: 'usine', lyric: 'slip', ...PAP,
    cap: ['Louis Lumière, La Sortie de l’usine Lumière à Lyon, 1895. Public domain.', 'AI Act, Art. 14(4)(e): a person with a “stop” button. For Annex III systems, postponed to 2 December 2027.', 'The Act entered into force on 1 August 2024.'] },
  { id: 'piranesi', at: 'L32', draw: 'piranesi', img: 'piranesi-carceri-round-tower', treat: 'line', lyric: 'poster', ...PAP,
    cap: ['G. B. Piranesi, Carceri d’invenzione, c. 1750. The Met, CC0.'] },
  { id: 'nobel', at: 'L33', draw: 'nobel', img: 'nobel-portrait', treat: 'photo', lyric: 'poster', ...PAP,
    cap: ['Alfred Nobel patented dynamite in 1867. Legend says a premature', 'obituary (“the merchant of death is dead”) led to the prizes.', '2024: Physics → neural networks. Chemistry → AlphaFold.'] },
  { id: 'schengen', at: 'L34', draw: 'schengen', lyric: 'poster', ...PAP,
    cap: ['Anonymous postcard, Frontière Franco-Allemande à Manhoué–Lanfroicourt, c. 1910. PD.', 'Schengen, 14 June 1985: signed on a boat on the Moselle. 16 Sep 2024: Germany checks its borders', 'with France, Belgium, the Netherlands and Luxembourg. Everyone else who was on the boat.'] },
  { id: 'evacard', at: 108.55, draw: 'evacard', lyric: 'none', ...BLK },
  { id: 'unicorns', at: 'L35', draw: 'unicorns', lyric: 'poster', ...BLK,
    cap: ['Vaswani et al., “Attention Is All You Need”, 2017: the transformer. Unicorn: The Met Cloisters, c. 1500, CC0.', 'Digital Decade 2030: the EU sets out to at least double its unicorns. Draghi, 2024: close to', '30 % of the unicorns founded in Europe 2008–21 moved their headquarters abroad.'] },
  { id: 'cap', at: 'L36:you', draw: 'cap', lyric: 'poster', ...BLK },
  { id: 'medley', at: 'L37', draw: 'medley', lyric: 'poster', ...BLK,
    cap: ['The Bubblers Medley: Europe’s Memorial for the Year 1720 (impression 1766–93). Rijksmuseum, PD.', 'Holland floated its companies from July 1720, after Paris had crashed.', 'The market lasted two months.'] },
  { id: 'fence', at: 'L38:through', draw: 'fence', lyric: 'poster', ...BLK },
  { id: 'plugs', at: 'L39', draw: 'plugs', lyric: 'poster', ...BLK },
  { id: 'euinc', at: 'L40', draw: 'euinc', lyric: 'poster', ...BLK,
    cap: ['Ludovic Penin, medal for the law of 4 July 1837 on decimal measures, 1840. Musée Carnavalet, CC0.', 'One standard for Europe: decreed 1793, compulsory 1840. European Company: proposed 1970, adopted 2001.', 'EU Inc, 18 March 2026: a company within 48 hours, for less than €100.'] },
  { id: 'hook4', at: 'L41', draw: 'hook', lyric: 'hook', ...YEL, p: { n: 4 } },
  { id: 'jacquard', at: 'L42', draw: 'plateRight', img: 'jacquard-woven-silk-portrait', treat: 'photo', lyric: 'poster', ...YEL,
    cap: ['J. M. Jacquard, woven in silk from ~24,000 punched cards, Lyon, 1839. The Met, CC0.', 'Lovelace, 1843: “the Analytical Engine weaves algebraical patterns', 'just as the Jacquard loom weaves flowers and leaves.”'] },
  { id: 'schnabel', at: 'L43', draw: 'plateRight', img: 'furst-schnabel', treat: 'line', lyric: 'poster', ...YEL,
    cap: ['Paul Fürst, Der Doctor Schnabel von Rom, 1656. PD.'] },
  { id: 'habsburg', at: 'L44', draw: 'habsburg', img: 'carreno-charles-ii', treat: 'color', lyric: 'poster', ...YEL,
    cap: ['Juan Carreño de Miranda, Charles II of Spain, c. 1680. PD.', 'Six generations trained on the family’s own outputs.'] },
  { id: 'wanderer', at: 'L45', draw: 'wanderer', img: 'friedrich-wanderer', treat: 'color', lyric: 'none', ...PAP, p: { capTop: true },
    cap: ['Caspar David Friedrich, Wanderer above the Sea of Fog, c. 1818. Hamburger Kunsthalle. PD.', 'Mario Draghi, The future of European competitiveness, 9 Sep 2024. Two years on:', 'not one key recommendation fully done (JEDI tracker, 10 Sep 2026).'] },
  { id: 'potemkin', at: 'L46', draw: 'potemkin', lyric: 'poster', ...PAP },
  { id: 'ring', at: 140.55, draw: 'ring', lyric: 'none', ...PAP },
  { id: 'gallery', at: 145.97, draw: 'gallery', img: 'panini-modern-rome', treat: 'color', lyric: 'none', ...PAP, p: { capTop: true },
    cap: ['Giovanni Paolo Panini, Modern Rome, 1757. The Met, CC0.'] },
  { id: 'credits', at: 149.60, draw: 'credits', lyric: 'none', ...PAP },
];

const LANGS: [string, string][] = [
  ['BG', 'Вдигам си EU doom'], ['ES', 'Subo mi EU doom'], ['CS', 'Zvyšuju si EU doom'], ['DA', 'Jeg hæver min EU doom'],
  ['DE', 'Ich erhöhe mein EU doom'], ['ET', 'Tõstan oma EU doom-i'], ['EL', 'Ανεβάζω το EU doom μου'], ['EN', 'I’m upping my EU doom'],
  ['FR', 'J’augmente mon EU doom'], ['GA', 'Ardaím mo EU doom'], ['HR', 'Podižem svoj EU doom'], ['IT', 'Alzo il mio EU doom'],
  ['LV', 'Es paaugstinu savu EU doom'], ['LT', 'Keliu savo EU doom'], ['HU', 'Emelem az EU doom-omat'], ['MT', 'Qed ngħolli l-EU doom tiegħi'],
  ['NL', 'Ik verhoog mijn EU doom'], ['PL', 'Podbijam swoje EU doom'], ['PT', 'Aumento o meu EU doom'], ['RO', 'Îmi cresc EU doom-ul'],
  ['SK', 'Zvyšujem si EU doom'], ['SL', 'Dvigujem svoj EU doom'], ['FI', 'Nostan EU-doomiani'], ['SV', 'Jag höjer min EU doom'],
];

// The EU edition's words (line number -> display text), as sung in audio/pdoom_eu.mp3; their timings come
// from data/eu_words.json (audio/el_music/eu_words.py).
const EU_LYRICS: Record<number, string> = {
  7: "I'm upping my EU doom", 18: "I'm upping my EU doom", 29: "I'm upping my EU doom,", 41: "I'm upping my EU doom",
  9: 'Trapped in the Brussels room,', 10: 'where the faxes zoom', 11: 'See through Pinocchio’s lies,', 12: 'with Eurovision eyes', 16: 'I feel my AC temperatures rearranging',
  17: 'Cookies, please, please let me free', 19: 'I hear the basic income gloom', 20: 'Nokia to the moon',
  22: 'One E thirty faxes a second', 23: 'That was fast enough, we reckoned', 24: 'Forward SAP, backward, repeat',
  27: 'Without a single GDPR', 28: 'NATO, please don’t let me go',
  31: 'Brussels guy’s on PTO', 34: 'Open Europe borders blues',
  37: 'Post-AI-bubble, super-dense', 40: 'EU Inc fixes things soon',
  45: 'What did Draghi see? We’ll never know',
};

/** Re-sets a line's words on its sung timings: words that still match keep theirs, and the new words
 *  in between share the replaced words' span (one to one when the counts agree, else by length). */
function relyric(l: Line, text: string) {
  const nw = smart(text).split(' '), ow = l.words;
  const key = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
  let a = 0, b = 0;
  while (a < nw.length && a < ow.length && key(nw[a]!) === key(ow[a]!.w)) a++;
  while (b < nw.length - a && b < ow.length - a && key(nw[nw.length - 1 - b]!) === key(ow[ow.length - 1 - b]!.w)) b++;
  const mid = nw.slice(a, nw.length - b), om = ow.slice(a, ow.length - b);
  let set;
  if (mid.length === om.length) set = mid.map((w, i) => ({ ...om[i]!, w, syl: undefined }));
  else {
    const t0 = om[0]!.start, t1 = om[om.length - 1]!.end, tot = mid.reduce((n, w) => n + w.length, 0);
    let acc = 0;
    set = mid.map((w) => { const start = t0 + ((t1 - t0) * acc) / tot; acc += w.length; return { ...om[0]!, w, start, end: t0 + ((t1 - t0) * acc) / tot, syl: undefined }; });
  }
  l.words = [...ow.slice(0, a).map((w, i) => ({ ...w, w: nw[i]! })), ...set,
    ...ow.slice(ow.length - b).map((w, i) => ({ ...w, w: nw[nw.length - b + i]! }))];
  l.words.forEach((w, i) => (w.index = i));
  l.text = smart(text);
}
function euEdition(ly: Lyrics, sung: Record<string, [string, number, number][]>) {
  for (const [n, text] of Object.entries(EU_LYRICS)) {
    const l = ly.lines[+n - 1]!;
    relyric(l, text);
    const ws = sung[n]; // the re-sung words' own timings (audio/el_music/eu_words.py)
    if (ws?.length === l.words.length) l.words.forEach((w, i) => { w.start = ws[i]![1]; w.end = ws[i]![2]; });
  }
  ly.words = ly.lines.flatMap((l) => l.words);
  ly.words.forEach((w, i) => (w.gi = i));
}

// archival cards the story shots lay down one after another (beyond each shot's own plate)
const STORY_IMGS = ['nokia-paper-mill', 'teilhard-fig3', 'teilhard-point-omega', 'galileo-moon-1610', 'unicorn-hunters-enter', 'unicorn-purifies-water',
  'unicorn-hunters-return', 'unicorn-in-garden', 'penin-metric-medal-1840', 'medley-card-quincampoix', 'medley-card-gazette',
  'medley-card-dutch', 'daumier-vingt-cinq-degres-1852', 'heyden-land-of-cockaigne', 'caselli-pantelegraph',
  'caselli-writing-sample', 'lanfroicourt-border-postcard', 'durer-rhinoceros-1515',
  'richter-haensel-gretel', 'punch-paul-pry-1844', 'bruegel-census-bethlehem', 'mitchell-world-map-1864'];

interface Shot extends ShotDef { t0: number; t1: number }

export default class Animatic extends Scene {
  L = new Layer2D();
  shots: Shot[] = [];
  films: Record<string, HTMLImageElement[]> = {};
  mouth!: MouthChart;

  override async init() {
    const ly = this.ctx.lyrics, au = this.ctx.audio;
    if (!ly.lines[6]!.text.includes('EU')) euEdition(ly, await (await fetch('data/eu_words.json')).json()); // once per page (the lyrics object is shared)
    const cut =(li: number) => { const s = ly.lines[li]!.words[0]!.start; return au.timeOfBeat(Math.floor(au.beatAt(s + 0.02))); };
    const at = (a: number | string) => {
      if (typeof a === 'number') return a;
      const m = /^L(\d+)(?::(.+))?$/.exec(a)!;
      const li = +m[1]! - 1;
      if (!m[2]) return cut(li);
      const w = ly.lines[li]!.words.find((x) => x.w.toLowerCase().replace(/[^a-z]/g, '').startsWith(m[2]!.toLowerCase()));
      if (!w) throw new Error('word not found ' + a);
      return w.start - 0.02;
    };
    const t0s = SHOTS.map((s) => at(s.at));
    this.shots = SHOTS.map((s, i) => ({ ...s, t0: t0s[i]!, t1: t0s[i + 1] ?? au.duration + 1 }));
    const ids = new Set(SHOTS.filter((s) => s.img).map((s) => s.img!));
    ids.add('panini-modern-rome');
    for (const id of STORY_IMGS) ids.add(id);
    await Promise.all([...ids].map((id) => loadImage(IMG(id))));
    const seq = async (name: string, n: number) => {
      this.films[name] = await Promise.all(Array.from({ length: n }, (_, i) => loadImage(`animatic/film/${name}/f_${String(i + 1).padStart(3, '0')}.jpg`)));
    };
    [, this.mouth] = await Promise.all([Promise.all([seq('wall', 48), seq('usine', 42)]), MouthChart.load()]);
    (window as any).__shots = this.shots.map((s) => ({ id: s.id, t0: s.t0, t1: s.t1 }));
  }

  override render(f: Frame, out: THREE.WebGLRenderTarget) {
    const c = this.L.ctx;
    this.L.clear(C.paper);
    const t = f.t;
    let si = 0;
    for (let i = 0; i < this.shots.length; i++) if (t >= this.shots[i]!.t0) si = i;
    const s = this.shots[si]!;
    const lt = t - s.t0, dur = s.t1 - s.t0;
    // the sheet slaps in: 4 frames of slide, like a page dropped on the copy stand
    const slap = 1 - ease.outCubic(clamp(lt / 0.07));
    c.save();
    c.translate(slap * 70, slap * 16); c.rotate(slap * 0.015);
    c.fillStyle = s.bg ?? C.paper; c.fillRect(-100, -100, W + 200, H + 200);
    const line = lineFor(this.ctx.lyrics, t);
    const D = (this as any)['d_' + s.draw];
    if (D) D.call(this, c, s, t, lt, dur, f, line);
    // lyrics
    if (line && s.lyric === 'poster') {
      const side = s.p?.side ?? 'left';
      const x = side === 'left' ? 90 : 1010;
      this.poster(c, line, t, x, 250, 820, { color: s.fg, hl: s.hl });
    } else if (line && s.lyric === 'slam') {
      slamLyric(c, line, t, { color: s.fg, w: 960, max: 400, y: 700 }); // stops short of the eye panel at x 1100
    } else if (line && s.lyric === 'slip') {
      this.slipL(c, line, t);
    }
    if (s.cap && lt > 0.25) captionSlip(c, s.cap, s.lyric === 'slip' || s.p?.capTop ? 70 : 1010, s.lyric === 'slip' || s.p?.capTop ? 60 : 900, { size: 19 });
    c.restore();
    clearRT(this.ctx.renderer, out, [1, 1, 1]);
    this.ctx.comp.draw(this.ctx.renderer, this.L.upload(), out, { mode: 'replace' });
    // Europe's print clock: 6 generations/s in blue sections, 12 elsewhere, and 60 exactly once (hook 4)
    return { printFps: s.id === 'hook4' ? 60 : s.bg === C.blue ? 6 : 12, reg: 1.5, cell: 7 };
  }

  // ------------------------------------------------------------ helpers
  /** The lyric printed on a poster, and on a typewritten slip (hybrid.ts sets both kinetically instead). */
  poster(c: Ctx, line: Line, t: number, x: number, y: number, w: number, o: Parameters<typeof posterLyric>[6] = {}) { posterLyric(c, line, t, x, y, w, o); }
  slipL(c: Ctx, line: Line, t: number, o: Parameters<typeof slipLyric>[3] = {}) { slipLyric(c, line, t, o); }
  plate(c: Ctx, s: Shot, lt: number, dur: number, box: [number, number, number, number], o: { zoom?: number; focus?: [number, number]; push?: number; rot?: number } = {}) {
    const im = img(IMG(s.img!)); if (!im) return;
    const [bx, by, bw, bh] = box;
    const push = 1 + (o.push ?? 0.05) * prog(lt, 0, dur, ease.linear);
    const sc = coverScale(im, bw, bh) * (o.zoom ?? 1) * push;
    const [u, v] = o.focus ?? [0.5, 0.5];
    c.save(); c.beginPath(); c.rect(bx, by, bw, bh); c.clip();
    c.fillStyle = C.paper; c.fillRect(bx, by, bw, bh);
    drawImageAt(c, im, bx + bw / 2, by + bh / 2, sc, s.treat ?? 'line', o.rot ?? 0, u, v);
    c.restore();
  }
  cutCanvas = [document.createElement('canvas'), document.createElement('canvas')] as const;
  /** A paper cut-out pasted on the copy stand: `draw` inks a figure into a w x h sheet, which is trimmed
   *  with a paper margin and laid down with its shadow, top-left at (x, y). */
  cutout(c: Ctx, x: number, y: number, w: number, h: number, draw: (k: Ctx) => void, margin = 12) {
    const [A, B] = this.cutCanvas;
    for (const k of [A, B]) if (k.width !== w || k.height !== h) { k.width = w; k.height = h; }
    const a = A.getContext('2d')!, b = B.getContext('2d')!;
    a.clearRect(0, 0, w, h); draw(a);
    b.globalCompositeOperation = 'source-over'; b.clearRect(0, 0, w, h);
    for (let i = 0; i < 16; i++) { const an = (i / 16) * Math.PI * 2; b.drawImage(A, Math.cos(an) * margin, Math.sin(an) * margin); }
    b.globalCompositeOperation = 'source-in'; // recolour the grown silhouette, keeping its shape
    b.fillStyle = ink({ black: 0.3 }); b.fillRect(0, 0, w, h); c.drawImage(B, x + 10, y + 12);
    b.fillStyle = C.paper; b.fillRect(0, 0, w, h); c.drawImage(B, x, y);
    c.drawImage(A, x, y);
  }
  /** An archival image as a paper card on the copy stand: w px wide, centred at (cx, cy), with paper margin and shadow. */
  card(c: Ctx, id: string, cx: number, cy: number, w: number, rot: number, treat: Treat = 'line') {
    const im = img(IMG(id)); if (!im) return;
    const k = w / im.width, h = im.height * k, m = 14;
    sheet(c, cx - w / 2 - m, cy - h / 2 - m, w + 2 * m, h + 2 * m, rot);
    drawImageAt(c, im, cx, cy, k, treat, rot);
  }
  vocalOpen(t: number) { return clamp(this.ctx.audio.env('vocal', t) * 1.4 - 0.15); }
  beatPhase(t: number) { const b = this.ctx.audio.beatAt(t); return b - Math.floor(b); }
  /** The idol's performance inputs, sampled on her 12 fps clock. */
  perf(t: number) { const tq = Math.floor(t * 12 + 1e-6) / 12; return { open: this.vocalOpen(tq), beat: this.beatPhase(tq), mouth: this.mouth }; }

  // ------------------------------------------------------------ drawers
  d_eye(c: Ctx, s: Shot, t: number, lt: number) {
    // extreme close-up of the idol's left eye: her design from _idol.ts at 26x (notched fringe, brow,
    // lid and lash, iris with the orange spark), on her 12 fps clock
    const g = Math.floor(t * 12 + 1e-6), tq = g / 12;
    // the EU ring of stars turning behind the lyric
    c.save(); c.translate(560, 540); c.rotate(lt * 0.5); c.translate(-560, -540);
    twelve(c, 560, 540, 400, t, { ring: true, scale: 1.4 });
    c.restore();
    c.save(); c.beginPath(); c.rect(1100, 0, 820, H); c.clip();
    c.fillStyle = C.paper; c.fillRect(1100, 0, 820, H);
    c.translate(1500, 640); c.scale(26, 26); c.translate(-18, -4);
    c.lineCap = 'round'; c.lineJoin = 'round';
    const disc = (x: number, y: number, r: number, col: string) => { c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fillStyle = col; c.fill(); };
    disc(25, 22, 8, ink({ orange: 0.35 })); // cheek screen
    // fringe, boiling by a hair per generation
    c.save(); c.translate((hash(g, 3) - 0.5) * 0.3, (hash(g, 4) - 0.5) * 0.3);
    c.beginPath(); c.moveTo(-10, -40); c.lineTo(50, -40); c.lineTo(50, -16);
    for (let i = 0; i < 14; i++) c.lineTo(46 - i * 4, -16 + (i % 2 ? 0 : 2.5));
    c.lineTo(-10, -16); c.closePath(); c.fillStyle = C.black; c.fill();
    c.restore();
    c.strokeStyle = C.black; c.lineWidth = 1.8; c.beginPath(); c.moveTo(9, -9); c.lineTo(27, -9); c.stroke(); // brow
    c.beginPath(); c.ellipse(18, 4, 10, 7.5, 0, 0, Math.PI * 2); c.fillStyle = C.paper; c.fill(); c.lineWidth = 0.6; c.stroke();
    c.save(); c.clip();
    disc(18, 4.5, 6.2, C.black);
    // the spark: an orange asterisk that pulses on beats
    const k = 1 + 0.25 * Math.exp(-this.beatPhase(tq) * 6);
    c.strokeStyle = C.orange; c.lineWidth = 0.55;
    for (let i = 0; i < 8; i++) { const a = (i / 8) * Math.PI * 2 + tq * 0.6; c.beginPath(); c.moveTo(20 + Math.cos(a) * 0.3, 2.5 + Math.sin(a) * 0.3); c.lineTo(20 + Math.cos(a) * 2.3 * k, 2.5 + Math.sin(a) * 2.3 * k); c.stroke(); }
    c.restore();
    c.strokeStyle = C.black; c.lineWidth = 1.3; c.beginPath(); c.moveTo(7, 5); c.quadraticCurveTo(18, -6, 29, 5); c.moveTo(28, 3); c.lineTo(33, -1); c.stroke(); // lid and lash
    c.restore();
  }

  d_frank(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    const im = img(IMG(s.img!))!;
    const eyes = this.wordAt('L1', 'eyes');
    const zin = prog(t, eyes - 0.05, eyes + 0.12, ease.outCubic);
    const z = 1 + 0.9 * zin;
    const u = 0.5 + (0.3 - 0.5) * zin, v = 0.62 + (0.66 - 0.62) * zin;
    drawImageAt(c, im, W / 2, H / 2, fitScale(im, W, H) * 1.0 * z * 1.25, 'line', 0, u, v);
    if (zin > 0.9) { c.fillStyle = C.yellow; c.globalCompositeOperation = 'multiply'; c.beginPath(); c.arc(W / 2, H / 2, 60, 0, Math.PI * 2); c.fill(); c.globalCompositeOperation = 'source-over'; }
  }

  d_plateFull(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    this.plate(c, s, lt, dur, [0, 0, W, H], { zoom: s.p?.zoom ?? 1, focus: s.p?.focus, push: 0.06 });
    if (s.lyric === 'poster') { c.fillStyle = s.bg ?? C.paper; c.fillRect(0, 0, 960, H); }
  }
  d_plateRight(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    sheet(c, 1000, 60, 860, 800, 0.01);
    this.plate(c, s, lt, dur, [1020, 80, 820, 760], { push: 0.05, focus: s.p?.focus });
  }

  d_egg(c: Ctx, s: Shot, t: number, lt: number) {
    const cx = 1430, cy = 520;
    const split = prog(t, this.wordAt('L3', 'surprise'), this.wordAt('L3', 'surprise') + 0.25, ease.outBack);
    c.fillStyle = C.paper; c.fillRect(1000, 60, 860, 800);
    // capsule
    c.fillStyle = C.yellow; c.beginPath(); c.ellipse(cx, cy - split * 60, 90, 120, 0, 0, Math.PI * 2); c.fill();
    c.strokeStyle = C.black; c.lineWidth = 4; c.stroke();
    for (const side of [-1, 1]) {
      c.save(); c.translate(cx + side * split * 230, cy + split * 60); c.rotate(side * split * 0.5);
      c.fillStyle = ink({ black: 0.55, orange: 0.9 }); // chocolate = overprint
      c.beginPath(); c.ellipse(0, 0, 200, 270, 0, side < 0 ? Math.PI / 2 : -Math.PI / 2, side < 0 ? Math.PI * 1.5 : Math.PI / 2); c.closePath(); c.fill();
      c.fillStyle = C.paper; setFont(c, F.sign(700), 40); c.textAlign = 'center';
      if (split < 0.1 && side < 0) c.fillText('SURPRISE', 100, 10);
      c.textAlign = 'left'; c.restore();
    }
  }

  d_dbBoard(c: Ctx, s: Shot, t: number) {
    // each departure drops on a stressed syllable (TRAIN-ing loss)
    const L = this.ctx.lyrics.lines[3]!;
    const drops = L.words.filter((_, i) => [2, 3, 5, 7].includes(i)).map((w) => w.start);
    const rows = [
      ['ICE 571  FRANKFURT    ', '  +5'], ['ICE 1715 BRUXELLES    ', ' +12'], ['IC 2023  STOCKHOLM    ', ' +20'], ['ICE 999  THE FUTURE   ', ' +45'],
    ].map(([a, b], i) => (t >= (drops[i] ?? 99) ? a!.slice(0, 19) + ' CANCELLED' : a! + b!));
    const last = Math.max(...drops.filter((d) => d <= t), -9);
    flapBoard(c, 1000, 250, rows, t, { cell: 28, since: last, cols: 29, title: 'DEPARTURES · DELAY' });
    setFont(c, F.typewriter(400), 20); c.fillStyle = C.paper;
    c.fillText('DB long-distance punctuality, June–July 2026: 52.6%', 1000, 700);
  }

  d_bureau(c: Ctx, s: Shot, t: number, lt: number, dur: number, f: Frame) {
    // Bürgeramt waiting room: ticket display + the idol pleading, close-up and lip-synced
    c.fillStyle = ink({ blue: 0.18 }); c.fillRect(0, 0, W, H);
    flapBoard(c, 1240, 120, ['NOW SERVING', '      0009'], t, { cell: 42, cols: 11 });
    sheet(c, 1330, 520, 260, 170, -0.05); setFont(c, F.sign(700), 30); c.fillStyle = C.black; c.fillText('YOUR NUMBER', 1360, 580); setFont(c, F.sign(700), 80); c.fillText('0812', 1370, 670);
    idolBust(c, 560, 430, 3.4, t, this.perf(t));
    // Art. 14 notice (eurofounder remix, generic)
    captionSlip(c, ['Output withheld pending human oversight (Art. 14).', 'Position 812 in queue. Now serving 9.'], 1150, 800, { size: 20 });
  }

  d_bigfish(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    this.plate(c, s, lt, dur, [0, 0, W, H], { zoom: 1.02, push: 0.08 });
    // little fish labels, typed tags on string
    const tags: [string, number, number][] = [['Silo AI → AMD, 2024', 520, 520], ['Stilla → Meta, 2026', 1180, 610], ['Hugging Face → NVIDIA', 830, 380]];
    tags.forEach(([txt, x, y], i) => { if (lt > 0.15 + i * 0.22) captionSlip(c, [txt], x, y, { size: 26, rot: (i - 1) * 0.05 }); });
    if (lt > 0.9) stamp(c, '$12,930,300,000', 1300, 250, { k: prog(lt, 0.9, 1.0), size: 80, rot: 0.08 });
  }

  d_hook(c: Ctx, s: Shot, t: number, lt: number, dur: number, f: Frame, line: Line | null) {
    const n = s.p!.n as number;
    // hemicycle: concentric arcs of seats (hook 4 gives the whole ground to type instead)
    const cx = W / 2, cy = 1260;
    for (let r = 0; r < (n === 4 ? 0 : 9); r++) {
      const rad = 420 + r * 70, k = Math.floor(18 + r * 5);
      for (let i = 0; i < k; i++) {
        const a = Math.PI + (i + 0.5) / k * Math.PI;
        if (n === 3 && hash(r, i) > 0.08) { c.fillStyle = ink({ blue: 0.22 }); } else c.fillStyle = ink({ blue: 0.75 });
        c.beginPath(); c.arc(cx + Math.cos(a) * rad, cy + Math.sin(a) * rad * 0.55, 13, 0, Math.PI * 2); c.fill();
      }
    }
    // heading block: the line as an EU heading in N languages
    const set = n === 1 ? ['EN', 'DE', 'FR'] : n === 2 ? ['EN', 'DE', 'FR', 'ES', 'IT', 'PL', 'NL', 'SV', 'FI'] : n === 3 ? ['EN'] : LANGS.map((l) => l[0]);
    const langs = LANGS.filter(([k]) => set.includes(k));
    if (n === 2) langs.push(langs.splice(langs.findIndex(([k]) => k === 'FI'), 1)[0]!); // Finland last
    const en = line && line.text.toLowerCase().includes('upping') ? line : null;
    if (n === 4) {
      // all 24 fill the left two thirds (2 columns x 12 rows); the ring and the idol keep the right third
      langs.forEach(([k, txt], i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const x = 50 + col * 640, y = 86 + row * 82;
        setFont(c, F.typewriter(700), 22); c.fillStyle = C.black; c.fillText(k, x, y);
        const fam = k === 'BG' || k === 'EL' ? F.display(75, 900) : F.archivo(75, 900);
        setFont(c, fam, fitSize(c, fam, txt.toUpperCase(), 540, 60)); c.fillStyle = k === 'EN' ? C.blue : C.black; c.fillText(txt.toUpperCase(), x + 50, y);
      });
    } else {
      langs.forEach(([k, txt], i) => {
        const y = 150 + i * (n === 2 ? 64 : 100);
        const size = n === 2 ? 54 : 88;
        setFont(c, F.typewriter(700), 24); c.fillStyle = C.black; c.fillText(k, 80, y);
        setFont(c, k === 'EN' ? F.archivo(75, 900) : F.archivo(75, 700), size);
        c.fillStyle = k === 'EN' ? C.black : ink({ black: 1 });
        if (k === 'EN' && en) {
          // word-synced highlighter on the English row
          let x = 140;
          for (const wd of en.words) {
            const ww = textW(c, wd.w.toUpperCase());
            const p = wordProg(wd, t);
            if (p > 0) { c.save(); c.globalCompositeOperation = 'multiply'; c.fillStyle = s.hl!; c.fillRect(x - 6, y - size * 0.8, (ww + 12) * p, size * 0.95); c.restore(); }
            c.fillStyle = C.black; c.fillText(wd.w.toUpperCase(), x, y); x += ww + size * 0.25;
          }
        } else c.fillText(txt.toUpperCase(), 140, y);
      });
      if (n === 3 && lt > 0.9) { setFont(c, F.typewriter(700), 34); c.fillStyle = C.black; c.fillText('[TRANSLATION PENDING — SERVICE RESUMES 1 SEPT]', 140, 260); }
    }
    // the Twelve (not in August) and the idol, centre
    if (n !== 3 && n !== 4) twelve(c, W / 2, 900, 700, t, { beat: this.perf(t).beat, scale: 1.1 });
    if (n === 4) {
      // the Twelve form the ring and turn on every 60 fps frame: Europe on time, once
      const rx = 1610, ry = 640;
      c.fillStyle = C.blue; c.beginPath(); c.arc(rx, ry, 250, 0, Math.PI * 2); c.fill();
      c.save(); c.translate(rx, ry); c.rotate(lt * 0.9); c.translate(-rx, -ry);
      twelve(c, rx, ry, 195, t, { ring: true, scale: 1.0 });
      c.restore();
    }
    idol(c, n === 4 ? 1610 : W / 2 + 420, n === 4 ? 615 : 640, n === 4 ? 0.5 : 1.15, 'stamp', t, this.perf(t));
    // DELAY board, in-world
    const meter = n === 1 ? ['ICE 999 THE FUTURE', 'DELAY         +15'] : n === 2 ? ['ICE 999 THE FUTURE', 'DELAY         +45'] : n === 3 ? ['AI ACT ANNEX III', '+2 YEARS · OMNIBUS'] : ['ICE 999 THE FUTURE', 'ON TIME'.padEnd(18)];
    flapBoard(c, n === 4 ? 1380 : 1340, n === 4 ? 150 : 40, meter, t, { cell: 22, since: s.t0 + 0.1, cols: 19 });
  }

  d_foom(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    this.plate(c, s, lt, dur, [0, 0, W, H], { zoom: 1.0, focus: [0.5, 0.55], push: 0.1 });
    // FOOM in Futurist parole in libertà: letters thrown at angles, growing on each syllable
    const w = this.ctx.lyrics.lines[7]!.words.find((x) => x.w.toUpperCase().includes('FOOM'))!;
    const k = prog(t, w.start - 0.02, w.start + 0.2, ease.outBack);
    if (k > 0) {
      const letters = ['F', 'O', 'O', 'M'];
      letters.forEach((ch, i) => {
        c.save(); c.translate(120 + i * 250, 700 - i * 40); c.rotate((i % 2 ? 0.18 : -0.12)); c.scale(k * (1 + i * 0.25), k * (1 + i * 0.25));
        setFont(c, F.display(100, 900), 360); c.fillStyle = i % 2 ? C.orange : C.black; c.fillText(ch, 0, 0); c.restore();
      });
    }
    if (line2(this.ctx.lyrics.lines[7]!, t)) this.slipL(c, this.ctx.lyrics.lines[7]!, t, { y: 1030 });
  }

  d_street(c: Ctx, s: Shot, t: number, lt: number) {
    // a German street, every facade blurred (opt-outs); the idol's gaze tags each one
    for (let i = 0; i < 5; i++) {
      const x = 1000 + i * 176, y = 300 + (i % 2) * 30;
      c.fillStyle = ink({ black: 0.15 + (i % 3) * 0.1, blue: 0.2 }); c.fillRect(x, y, 160, 520);
      c.fillStyle = ink({ black: 0.7 }); c.beginPath(); c.moveTo(x - 10, y); c.lineTo(x + 80, y - 90); c.lineTo(x + 170, y); c.fill();
      // mosaic blur
      for (let bx = 0; bx < 4; bx++) for (let by = 0; by < 12; by++) { c.fillStyle = ink({ black: 0.2 + hash(i, bx, by) * 0.5 }); c.fillRect(x + bx * 40, y + by * 43, 40, 43); }
      if (lt > 0.3 + i * 0.35) captionSlip(c, ['OPTED OUT · 2010'], x - 10, y - 60, { size: 17, rot: -0.04 });
    }
    idol(c, 860, 700, 0.8, 'walk', t, { ...this.perf(t), flip: lt > 3.9 });
    captionSlip(c, ['Germany, 2010: ~244,000 households asked', 'Google Street View to blur their homes.'], 1010, 960, { size: 19 });
  }

  d_icarus(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    const im = img(IMG(s.img!))!;
    // hold on the ploughman, then (at line 14) the copy stand slides to the splash, bottom right
    const tl14 = this.cutOf(14);
    const k = prog(t, tl14, tl14 + 0.45, ease.inOutCubic);
    const u = 0.38 + k * 0.44, v = 0.52 + k * 0.33;
    const sc = coverScale(im, W, H) * (1.9 + k * 0.9);
    drawImageAt(c, im, W / 2, H / 2, sc, 'color', 0, u, v);
    if (k > 0.99) stamp(c, 'SINGULARITY', 520, 300, { k: prog(t, tl14 + 0.5, tl14 + 0.58), size: 70, color: C.orange, rot: -0.1 });
  }

  d_navier(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    sheet(c, 1000, 50, 860, 820, 0.012);
    this.plate(c, s, lt, dur, [1020, 70, 820, 780], { push: 0.06 });
    setFont(c, F.display(100, 700), 44); c.fillStyle = C.black;
    c.fillText('∂u/∂t + (u·∇)u = −∇p + νΔu + f', 1040, 930);
    if (lt > 0.35) stamp(c, '88 HOURS · ~10,000 AGENTS', 1430, 470, { k: prog(lt, 0.35, 0.45), size: 64, rot: -0.09 });
  }

  d_fax(c: Ctx, s: Shot, t: number, lt: number) {
    // German fax, thermal paper spewing results at 60 fps; the Official stamps RECEIVED at 6 fps
    c.fillStyle = C.black; c.fillRect(960, 0, 960, H);
    c.fillStyle = ink({ black: 0.35, blue: 0.3 }); c.fillRect(1000, 620, 860, 240); // machine
    c.fillStyle = C.black; c.fillRect(1040, 650, 240, 70); c.fillStyle = C.yellow; setFont(c, F.sign(700), 30); c.fillText('SENDING… OK', 1060, 697);
    const items = ['ERDŐS UNIT DISTANCE: DISPROVED', 'JACOBIAN CONJECTURE: FALSE', 'IMO 2026: 42/42', 'FERMAT, IN LEAN: 11 DAYS', 'EU INC: PENDING', 'NAVIER–STOKES: 88 H', 'METR HORIZON: DOUBLING', 'FRONTIERMATH: ▲', 'ERDŐS #1043: SOLVED'];
    const rate = 330; // px of paper per second (the world's speed)
    c.save(); c.beginPath(); c.rect(1000, 0, 860, 640); c.clip();
    c.fillStyle = C.paper; c.fillRect(1030, 0, 800, 640);
    setFont(c, F.typewriter(700), 40); c.fillStyle = C.black;
    items.forEach((it, i) => {
      const te = 0.15 + i * 0.42; // each result prints as the paper feeds out of the machine
      if (lt < te) return;
      const y = 640 - (lt - te) * rate + 10;
      if (y < -40) return;
      setFont(c, F.typewriter(700), 38); c.fillStyle = C.black; c.fillText(it, 1050, y);
      const q = Math.floor(lt * 6) / 6; // Europe stamps at 6 fps, one stamp per 0.7 s
      if (q > 0.5 + i * 0.7) stamp(c, 'RECEIVED', 1660, y + 34, { size: 26, color: C.blue, rot: -0.06 });
    });
    c.restore();
    captionSlip(c, ['“The internet is new territory for all of us.”', '— Angela Merkel, Berlin, 19 June 2013'], 1010, 900, { size: 19 });
  }

  d_cookies(c: Ctx, s: Shot, t: number, lt: number) {
    c.fillStyle = ink({ black: 0.25 }); c.fillRect(0, 0, W, H);
    // Hansel and Gretel (Grimm, 1812): the house of bread and cake. Through the held "Cookies" a consent banner is
    // pinned over one gingerbread panel per beat until the house is a cookie wall
    const q6 = Math.floor(t * 6) / 6, Lc = this.ctx.lyrics.lines[16]!;
    this.card(c, 'richter-haensel-gretel', 1480, 470, 560, 0.012);
    const pins = Math.floor(prog(q6, Lc.words[0]!.start + 0.4, Lc.words[1]!.start) * 6);
    for (let i = 0; i < pins; i++) {
      const x = 1270 + (i % 3) * 150 + (hash(i, 5) - 0.5) * 30, y = 250 + Math.floor(i / 3) * 170 + (hash(i, 6) - 0.5) * 30;
      sheet(c, x, y, 190, 96, (hash(i, 7) - 0.5) * 0.12);
      setFont(c, F.archivo(100, 700), 15); c.fillStyle = C.black; c.fillText('We value your privacy', x + 12, y + 26);
      setFont(c, F.archivo(100, 400), 11); c.fillText('We and our 1,029 partners…', x + 12, y + 46);
      c.fillStyle = C.blue; c.fillRect(x + 12, y + 60, 86, 24); c.fillStyle = C.paper; setFont(c, F.archivo(100, 700), 11); c.fillText('ACCEPT ALL', x + 20, y + 77);
    }
    if (t >= Lc.words[1]!.start) { // "please": the witch's line, typed
      sheet(c, 1180, 820, 620, 60, 0.01);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 22); c.fillText('„Hänsel, streck deine Finger heraus“ (Grimm, 1812)', 1200, 858);
    }
    // Manage preferences: "please", "please", "let", "me" each untick a pre-ticked box; on "free" a fresh sheet
    // slides over it, every box ticked again. Free never comes.
    const L = this.ctx.lyrics.lines[16]!, nw = L.words.length;
    const unticks = L.words.slice(1, nw - 1).map((w) => w.start), free = L.words[nw - 1]!.start;
    const rows = ['Legitimate interest (368)', 'Measure content performance', 'Personalised advertising', 'Store and/or access information'];
    const prefs = (dx: number, rot: number, allTicked: boolean) => {
      c.save(); c.translate(dx, 0);
      sheet(c, 60, 560, 450, 330, rot);
      setFont(c, F.typewriter(700), 26); c.fillStyle = C.black; c.fillText('Manage preferences', 90, 616);
      rows.forEach((r, i) => {
        const y = 670 + i * 56;
        c.strokeStyle = C.black; c.lineWidth = 3; c.strokeRect(90, y - 26, 32, 32);
        if (allTicked || i >= unticks.length || t < unticks[i]!) { c.fillStyle = C.blue; c.fillRect(95, y - 21, 22, 22); c.strokeStyle = C.paper; c.lineWidth = 4; c.beginPath(); c.moveTo(99, y - 10); c.lineTo(105, y - 3); c.lineTo(114, y - 18); c.stroke(); }
        setFont(c, F.archivo(100, 500), 21); c.fillStyle = C.black; c.fillText(r, 138, y - 2);
      });
      c.restore();
    };
    prefs(0, -0.02, false);
    const me = unticks[unticks.length - 1]!; // "me": Luxembourg rules a pre-ticked box is no consent (Planet49)
    if (t >= me && t < free) stamp(c, 'C-673/17 · 1.10.2019 · NOT CONSENT', 290, 640, { k: prog(t, me, me + 0.08), size: 24, color: C.orange, rot: -0.08 });
    if (t >= free) prefs((1 - ease.outCubic(prog(t, free, free + 0.12))) * -600 + 14, 0.015, true);
    idolBust(c, 960, 470, 3.0, t, this.perf(t));
  }

  d_omega(c: Ctx, s: Shot, t: number, lt: number) {
    sheet(c, 1040, 80, 760, 780, 0.015, C.paper);
    setFont(c, F.display(62.5, 900), 150); c.fillStyle = C.black; c.fillText('THE OMEGA', 1090, 280); c.fillText('POINT', 1090, 430);
    c.fillStyle = C.orange; c.fillRect(1090, 470, 660, 110); setFont(c, F.sign(700), 96); c.fillStyle = C.paper; c.fillText('COMING SOON', 1110, 560);
    setFont(c, F.archivo(100, 400), 18); c.fillStyle = C.black;
    c.fillText('* Will not be initially available in the EU.', 1090, 640);
    c.fillText('  (Apple, footnote, 14 Sep 2026)', 1090, 664);
  }

  d_milchkanne(c: Ctx, s: Shot, t: number, lt: number) {
    // Germany, 21 Nov 2018: „5G ist nicht an jeder Milchkanne notwendig“. "That was": a milk churn in a field; "fast": a
    // phone is propped on it and its network flaps down 5G, LTE, 3G, E (6 fps); "enough, we": the quote is typed out;
    // held "reckoned": the page crawls to 3 % and the verdict is stamped in German school grades: 4, AUSREICHEND
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L23', x);
    const tF = w('fast'), tE = w('enough'), tR = w('reckoned'), L = this.ctx.lyrics.lines[22]!, end = L.words.at(-1)!.end;
    c.fillStyle = ink({ yellow: 0.4, blue: 0.25 }); c.fillRect(1000, 600, 880, 330); // the field
    const kx = 1250, ky = 250; // the churn: lid, shoulder, body, two handles
    c.strokeStyle = C.black; c.lineWidth = 4; c.fillStyle = C.paper;
    c.beginPath(); c.moveTo(kx - 60, ky + 60); c.lineTo(kx - 120, ky + 170); c.lineTo(kx - 120, ky + 620); c.lineTo(kx + 120, ky + 620); c.lineTo(kx + 120, ky + 170); c.lineTo(kx + 60, ky + 60); c.closePath(); c.fill(); c.stroke();
    c.beginPath(); c.ellipse(kx, ky + 40, 78, 30, 0, Math.PI, 0); c.lineTo(kx + 78, ky + 64); c.lineTo(kx - 78, ky + 64); c.closePath(); c.fill(); c.stroke(); // domed lid
    c.fillRect(kx - 14, ky - 6, 28, 18); c.strokeRect(kx - 14, ky - 6, 28, 18);
    c.fillStyle = C.black; setFont(c, F.sign(700), 64); c.textAlign = 'center'; c.fillText('MILCH', kx, ky + 440); c.textAlign = 'left';
    c.fillStyle = C.black; c.fillRect(kx - 124, ky + 300, 248, 10); c.fillRect(kx - 124, ky + 520, 248, 10);
    c.lineWidth = 8; for (const sx of [-1, 1]) { c.beginPath(); c.arc(kx + sx * 140, ky + 200, 34, sx > 0 ? -Math.PI / 2 : Math.PI / 2, sx > 0 ? Math.PI / 2 : Math.PI * 1.5); c.stroke(); }
    if (q >= tF) { // the phone, propped against the churn
      const px = 1500, py = 300;
      sheet(c, px, py, 200, 360, 0.05);
      c.save(); c.translate(px + 100, py + 180); c.rotate(0.05);
      c.fillStyle = C.black; c.fillRect(-88, -168, 176, 336);
      const net = ['5G', 'LTE', '3G', 'E'][Math.min(3, Math.floor((q - tF) * 6))]!;
      c.fillStyle = C.paper; setFont(c, F.sign(700), 64); c.fillText(net, -74, -60);
      for (let i = 0; i < 4; i++) { c.fillStyle = i < (net === 'E' ? 1 : 4 - ['5G', 'LTE', '3G'].indexOf(net)) ? C.paper : ink({ black: 0.6 }); c.fillRect(8 + i * 18, -104 - i * 12, 12, 16 + i * 12); }
      const pct = q < tR ? 0 : Math.min(3, Math.floor(prog(q, tR, end) * 4));
      c.fillStyle = ink({ black: 0.6 }); c.fillRect(-70, 40, 140, 16); c.fillStyle = C.yellow; c.fillRect(-70, 40, 140 * (pct + 0.5) / 100 * 4, 16);
      c.fillStyle = C.paper; setFont(c, F.typewriter(700), 22); c.fillText(`${pct} %`, -24, 90);
      c.restore();
    }
    if (q >= tE) { // the quote, typed
      const quote = '„5G ist nicht an jeder Milchkanne notwendig.“', n = Math.floor(prog(q, tE, tR) * quote.length);
      sheet(c, 1020, 88, 860, 76, -0.01);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 30); c.fillText(quote.slice(0, n), 1046, 138);
    }
    const g4 = tR + (end - tR) * 0.45;
    if (q >= g4) stamp(c, '4 · AUSREICHEND', 1600, 780, { k: prog(q, g4, g4 + 0.17), size: 56, color: C.blue, rot: -0.07 });
  }

  d_wall(c: Ctx, s: Shot, t: number, lt: number) {
    // Lumière: forward (Forward GDP), backward (backward), forward (repeat), played at 12 fps
    const fr = this.films.wall!;
    const L = this.ctx.lyrics.lines[23]!;
    const wb = L.words.find((w) => w.w.toLowerCase().startsWith('backward'))!.start, wr = L.words.find((w) => w.w.toLowerCase().startsWith('repeat'))!.start;
    const a = 14, b = 31, q = Math.floor(t * 12) / 12;
    let idx: number;
    if (q < wb) idx = a + Math.min(b - a, Math.floor((q - s.t0) * 12));
    else if (q < wr) idx = b - Math.min(b - a, Math.floor((q - wb) * 12));
    else idx = a + Math.min(b - a, Math.floor((q - wr) * 12));
    const im = fr[clamp(idx, 0, fr.length - 1)]!;
    drawImageAt(c, im, W / 2, H / 2, coverScale(im, W, H), 'photo');
    const word = q < wb ? 'FORWARD · MIGRATE BY 2020' : q < wr ? 'BACKWARD · EXTENDED' : 'REPEAT · UNTIL 2033';
    setFont(c, F.archivo(62, 900), 92); const tw = textW(c, word);
    c.fillStyle = C.yellow; c.fillRect(70, 850, tw + 50, 120); c.fillStyle = C.black; c.fillText(word, 95, 945);
    // SAP's old ERP, pinned on: each time the wall goes back up, its end-of-support date tears off to a later one
    const years = ['2020', '2025', '2027', '2030', '2033'];
    const yi = q < wb ? 0 : q < wr ? (q < wb + 0.34 ? 1 : 2) : q < wr + 0.34 ? 3 : 4;
    sheet(c, 1480, 90, 360, 240, -0.03);
    c.fillStyle = C.black; setFont(c, F.typewriter(700), 26); c.fillText('SAP ECC', 1512, 142); c.fillText('SUPPORT ENDS', 1512, 178);
    setFont(c, F.archivo(62, 900), 104); c.fillText(years[yi]!, 1508, 296);
    c.beginPath(); c.arc(1660, 104, 9, 0, Math.PI * 2); c.fillStyle = C.orange; c.fill(); // the pin
    if (q >= wb) stamp(c, 'EXTENDED', 1720, 270, { k: prog(q, wb, wb + 0.17), size: 38, color: C.orange, rot: -0.14 });
    if (q >= wr + 0.5) stamp(c, 'TRANSITION OPTION', 1650, 360, { k: prog(q, wr + 0.5, wr + 0.67), size: 30, color: C.orange, rot: 0.05 });
  }

  d_gate(c: Ctx, s: Shot, t: number, lt: number) {
    c.fillStyle = ink({ blue: 0.15 }); c.fillRect(0, 0, W, H);
    flapBoard(c, 1180, 80, ['B42  WASHINGTON DC'], t, { cell: 36, cols: 18 });
    // NATO's compass star rolls off toward the gate, on the idol's 12 fps clock, its luggage tag hanging level
    const q = Math.floor(lt * 12) / 12, nx = 1300 + prog(q, 0, 6) * 360, ny = 800, r = 100;
    c.save(); c.translate(nx, ny); c.rotate((nx - 1300) / r);
    c.fillStyle = C.blue; c.beginPath(); c.arc(0, 0, r, 0, Math.PI * 2); c.fill();
    c.strokeStyle = C.paper; c.lineWidth = 5; c.beginPath(); c.arc(0, 0, r * 0.62, 0, Math.PI * 2); c.stroke();
    c.fillStyle = C.paper; c.beginPath();
    for (let k = 0; k < 8; k++) { const a = (k / 8) * Math.PI * 2, rr = k % 2 ? 16 : r * 0.9; c.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); }
    c.closePath(); c.fill();
    c.restore();
    c.strokeStyle = C.black; c.lineWidth = 3; c.beginPath(); c.moveTo(nx, ny); c.lineTo(nx - 40, ny + 70); c.stroke();
    sheet(c, nx - 110, ny + 70, 140, 56, 0.05); setFont(c, F.sign(700), 38); c.fillStyle = C.black; c.fillText('NATO', nx - 88, ny + 112);
    idol(c, 560, 560, 1.45, 'reach', t, this.perf(t));
    captionSlip(c, ['NATO, The Hague, 25 June 2025: allies pledge 5% of GDP to defence by 2035.'], 70, 60, { size: 19 });
  }

  d_chair(c: Ctx, s: Shot, t: number, lt: number) {
    // Europe in a Chair: quoted words on index cards pile up around the idol
    const words = ['“AI Act”', '“GDPR”', '“DSA”', '“Trilogue”', '“Delegated act”', '“Code of Practice”', '“Accept all”', '“Pace the frontier”', '“Omnibus”', '“Sovereign cloud”', '“28th regime”', '“Legitimate interest”', '“Stop the clock”', '“Conformity assessment”', '“Brussels effect”'];
    const n = Math.floor(prog(lt, 0, 1.8) * words.length);
    for (let i = 0; i < n; i++) {
      const a = (i / words.length) * Math.PI * 1.9 + 3.3, r = 330 + hash(i) * 140;
      const x = 960 + Math.cos(a) * r * 1.5, y = 470 + Math.sin(a) * r * 0.85;
      c.save(); c.translate(x, y); c.rotate((hash(i, 3) - 0.5) * 0.2);
      setFont(c, F.archivo(100, 500), 30 + hash(i, 5) * 22); const tw = textW(c, words[i]!);
      c.fillStyle = C.paper; c.fillRect(-tw / 2 - 14, -38, tw + 28, 54);
      c.fillStyle = C.black; c.fillText(words[i]!, -tw / 2, 0); c.restore();
    }
    idol(c, 960, 600, 1.7, 'chair', t, { key: C.paper });
    setFont(c, F.typewriter(400), 16); c.fillStyle = C.paper; c.fillText('After “Shinji in a Chair”. Cards: Otlet’s universal index, Brussels, c. 1900.', 70, 60);
  }

  d_usine(c: Ctx, s: Shot, t: number, lt: number) {
    const fr = this.films.usine!;
    const idx = Math.min(fr.length - 1, Math.floor(Math.floor(lt * 12)));
    drawImageAt(c, fr[idx]!, W / 2, H / 2, coverScale(fr[idx]!, W, H), 'photo');
    // the off switch, bolted to the gate behind the notice (the notice half covers it)
    c.fillStyle = C.black; c.fillRect(1530, 470, 190, 170);
    c.fillStyle = C.orange; c.beginPath(); c.arc(1625, 470, 62, Math.PI, 0); c.fill(); c.fillRect(1563, 462, 124, 14);
    c.fillStyle = C.paper; setFont(c, F.typewriter(700), 18); c.fillText('STOP · Art. 14(4)(e)', 1540, 630);
    const q6 = Math.floor(t * 6) / 6, won = this.wordAt('L31', 'on'), pto = this.wordAt('L31', 'pto');
    if (q6 >= won && s.p?.gate !== false) { // a paper gate slides shut across the factory gate
      const k = ease.outCubic(prog(q6, won, won + 0.34));
      c.fillStyle = C.black; for (let i = 0; i < 9; i++) c.fillRect(-900 + k * 900 + i * 110, 120, 22, 900);
      c.fillRect(-900 + k * 900, 180, 900, 18); c.fillRect(-900 + k * 900, 880, 900, 18);
    }
    sheet(c, 1180, 330, 420, 300, 0.04);
    setFont(c, F.typewriter(700), 34); c.fillStyle = C.black;
    ['CLOSED FOR', 'THE SUMMER', '1–25 August'].forEach((l, i) => c.fillText(l, 1220, 420 + i * 56));
    if (q6 >= pto + 0.34) stamp(c, 'RETOUR LE 2 DÉC. 2027', 1400, 600, { k: prog(q6, pto + 0.34, pto + 0.5), size: 34, color: C.orange, rot: -0.06 });
  }

  d_piranesi(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    this.plate(c, s, lt, dur, [960, 0, 960, H], { push: 0.05 });
    flapBoard(c, 1060, 420, ['ALL TRAINS', 'CANCELLED', 'DELAY  +∞'], t, { cell: 34, since: s.t0 + 0.1, cols: 10 });
  }

  d_nobel(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    sheet(c, 1100, 70, 620, 720, 0.02);
    this.plate(c, s, lt, dur, [1120, 90, 580, 680], { push: 0.03 });
    // the fuse: a burning line across the bottom
    const k = prog(lt, 0.2, dur);
    c.strokeStyle = C.black; c.lineWidth = 6; c.beginPath(); c.moveTo(1000, 900); c.lineTo(1880, 900); c.stroke();
    c.fillStyle = C.orange; c.beginPath(); c.arc(1000 + k * 880, 900, 16 + 6 * Math.sin(t * 40), 0, Math.PI * 2); c.fill();
  }

  d_evacard(c: Ctx, s: Shot, t: number) {
    c.fillStyle = C.black; c.fillRect(0, 0, W, H);
    c.fillStyle = C.paper; setFont(c, F.typewriter(700), 44); c.fillText('EPISODE:27', 100, 170);
    setFont(c, F.display(62.5, 900), 250);
    c.save(); c.translate(90, 250); c.rotate(Math.PI / 2); c.fillText('THE', 0, -20); c.restore();
    c.fillText('REGULATION', 330, 520);
    c.fillText('ATTACKS', 330, 800);
  }

  d_unicorns(c: Ctx, s: Shot, t: number, lt: number) {
    // the Unicorn Tapestries (probably Brussels, c. 1500) as a start-up's life: built, priced on the held note,
    // carried off (the tag flips), and on "way" fenced in a pen it could leap out of
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L35', x);
    const tU = w('transformers'), tA = w('all'), tW = w('way');
    const panels: [string, number][] = [['unicorn-hunters-enter', s.t0], ['unicorn-purifies-water', tU], ['unicorn-hunters-return', tA], ['unicorn-in-garden', tW]];
    for (const [id, at] of panels) {
      if (q < at) break;
      const k = id === 'unicorn-in-garden' ? 1 : ease.outCubic(prog(q, at, at + 0.34)); // the garden is a cut
      const pan = id === 'unicorn-purifies-water' ? prog(q, tU, tA) : 0.5; // flat pan: the spears, then the kneeling unicorn
      const im = img(IMG(id)); if (!im) continue;
      c.save(); c.translate((1 - k) * 900, 0);
      sheet(c, 1000, 60, 860, 800, 0.008);
      c.save(); c.beginPath(); c.rect(1020, 80, 820, 760); c.clip();
      drawImageAt(c, im, 1430, 460, coverScale(im, 820, 760) * 1.12, 'color', 0, 0.3 + pan * 0.4, 0.5);
      c.restore(); c.restore();
    }
    const tag = (tU + tA) / 2; // halfway through the held note a price tag is pinned; on "all" it flips
    if (q >= tag && q < tW) {
      c.save(); c.translate(1560, 640); c.rotate(q < tA ? -0.08 : 0.06);
      c.fillStyle = C.yellow; c.fillRect(-190, -50, 380, 100); c.strokeStyle = C.black; c.lineWidth = 3; c.strokeRect(-190, -50, 380, 100);
      c.fillStyle = C.black; setFont(c, F.sign(700), 46); c.textAlign = 'center'; c.fillText(q < tA ? '≥ $1,000,000,000' : 'ACQUIRED', 0, 16); c.textAlign = 'left';
      c.beginPath(); c.arc(-166, -30, 8, 0, Math.PI * 2); c.fillStyle = C.orange; c.fill();
      c.restore();
    }
    if (q >= tW) stamp(c, 'WAY OUT →', 1440, 770, { k: prog(q, tW, tW + 0.17), size: 54, color: C.orange, rot: -0.06 });
  }

  d_medley(c: Ctx, s: Shot, t: number, lt: number) {
    // 1720, card by card: Paris burst in May, London was past its peak, then Holland floated its companies in July.
    // The Dutch card lands last, crooked, with its own verse: "They coppy England, England, France"
    // on the beats of "Post-Chin-chil-la, su-per-dense": Paris on "Post", London mid "Chinchilla", Holland on "super", shut on "dense"
    const q = Math.floor(t * 6) / 6, [w0, w1] = this.ctx.lyrics.lines[36]!.words as [Word, Word];
    const tP = w0.start, tL = (w0.start + w0.end) / 2, tS = w1.start, tD = w1.syl?.[1]?.[0] ?? (w1.start + w1.end) / 2;
    const cards: [string, number, number, number, number, number][] = [
      ['medley-card-quincampoix', tP, 1330, 320, 720, -0.06],
      ['medley-card-gazette', tL, 1580, 560, 470, 0.05],
      ['medley-card-dutch', tS, 1290, 590, 540, -0.1],
    ];
    for (const [id, at, x, y, cw, rot] of cards) {
      if (q < at) continue;
      const k = ease.outCubic(prog(q, at, at + 0.34)), feed = id === 'medley-card-gazette'; // the Gazette feeds up, the others slide in
      this.card(c, id, x + (feed ? 0 : (1 - k) * 900), y + (feed ? (1 - k) * 700 : 0), cw, rot, 'color');
    }
    const st = (at: number) => prog(q, at + 0.17, at + 0.34);
    if (q >= tP + 0.17) stamp(c, 'PARIS · BURST MAY 1720', 1330, 190, { k: st(tP), size: 34, color: C.orange, rot: -0.08 });
    if (q >= tL + 0.17) stamp(c, 'LONDON · PAST PEAK', 1620, 420, { k: st(tL), size: 34, color: C.blue, rot: 0.05 });
    if (q >= tS + 0.17) {
      sheet(c, 1070, 770, 560, 64, -0.02);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 24); c.fillText('“They coppy England, England, France”', 1090, 811);
    }
    if (q >= tD) stamp(c, 'OPENED JULY 1720 · CLOSED OCT 1720', 1330, 690, { k: prog(q, tD, tD + 0.17), size: 32, color: C.orange, rot: -0.04 });
  }

  d_heat(c: Ctx, s: Shot, t: number, lt: number) {
    // Summer 2022: Europe sets a floor under the air conditioning. Daumier's Salon crowd sweats at "25 degrees" (1852);
    // on "AC" a remote feeds up, set to 18; on "temperatures" its display flaps up a degree per 6 fps generation and the
    // national floors are stamped as it passes them (IT 25, ES 27, GR 27); on "rearranging" the down button is taped over
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L16', x);
    const tAC = w('ac'), tT = w('temperatures'), tR = w('rearranging');
    this.card(c, 'daumier-vingt-cinq-degres-1852', 1640, 250, 400, 0.02);
    if (q < tAC) return;
    const rx = 1110, ry = 170 + (1 - ease.outCubic(prog(q, tAC, tAC + 0.34))) * 900; // the remote
    sheet(c, rx, ry, 300, 700, -0.02);
    c.fillStyle = ink({ blue: 0.3 }); c.fillRect(rx + 30, ry + 40, 240, 170); c.strokeStyle = C.black; c.lineWidth = 3; c.strokeRect(rx + 30, ry + 40, 240, 170);
    const deg = 18 + Math.min(9, Math.floor(prog(q, tT, tR) * 10));
    c.fillStyle = C.black; setFont(c, F.sign(700), 130); c.fillText(String(deg), rx + 50, ry + 180); setFont(c, F.sign(700), 60); c.fillText('°C', rx + 190, ry + 120);
    setFont(c, F.typewriter(700), 20); c.fillText('❄ COOL', rx + 44, ry + 70);
    const btn = (y: number, up: boolean, pressed: boolean) => {
      c.fillStyle = pressed ? C.black : C.paper; c.beginPath(); c.arc(rx + 150, y, 56, 0, Math.PI * 2); c.fill(); c.strokeStyle = C.black; c.lineWidth = 4; c.stroke();
      c.fillStyle = pressed ? C.paper : C.black; c.beginPath(); c.moveTo(rx + 124, y + (up ? 14 : -14)); c.lineTo(rx + 176, y + (up ? 14 : -14)); c.lineTo(rx + 150, y + (up ? -20 : 20)); c.closePath(); c.fill();
    };
    btn(ry + 300, true, false);
    btn(ry + 440, false, q >= tAC + 0.34 && q < tR && Math.floor(q * 6) % 2 === 0); // someone keeps pressing down
    c.fillStyle = C.black; setFont(c, F.typewriter(700), 22); c.fillText('CLIMA', rx + 112, ry + 640);
    ([[25, 'IT · 25 °C MIN.', C.orange, 1620, 560, -0.08], [27, 'ES · 27 °C MÍN.', C.blue, 1640, 690, 0.06], [27, 'GR · 27 °C', C.blue, 1600, 820, -0.04]] as const)
      .forEach(([d, txt, col, x, y, rot], i) => {
        const at = tT + ((d - 18) / 10) * (tR - tT) + (i === 2 ? 0.17 : 0);
        if (q >= at) stamp(c, txt, x, y, { k: prog(q, at, at + 0.17), size: 44, color: col, rot });
      });
    if (q >= tR) { // the down button, taped over
      const k = prog(q, tR, tR + 0.17);
      c.save(); c.translate(rx + 150, ry + 440); c.rotate(-0.14); c.globalAlpha = 0.92;
      c.fillStyle = C.yellow; c.fillRect(-170 * k, -34, 340 * k, 68); c.globalAlpha = 1;
      if (k >= 1) { c.fillStyle = C.black; setFont(c, F.sign(700), 40); c.textAlign = 'center'; c.fillText('MIN. 27 °C', 0, 14); c.textAlign = 'left'; }
      c.restore();
    }
  }

  d_basicincome(c: Ctx, s: Shot, t: number, lt: number) {
    // Switzerland, 2016: Geneva unrolls the world's largest poster; on "basic income" it folds down its crease onto what
    // the voters feared (Bruegel's Land of Cockaigne: three men asleep under the table); on "gloom" the ballot slams
    const q = Math.floor(t * 12) / 12, w = (x: string) => this.wordAt('L19', x);
    const tB = w('basic'), tG = w('gloom');
    this.card(c, 'heyden-land-of-cockaigne', 1430, 440, 800, -0.01, 'line');
    const fold = prog(q, tB, tG), px = 1010, py = 60, pw = 840, ph = 760, top = py + ph * fold;
    if (fold < 1) {
      c.save(); c.beginPath(); c.rect(px, top, pw, py + ph - top); c.clip();
      c.fillStyle = C.paper; c.fillRect(px, py, pw, ph);
      c.fillStyle = C.black; setFont(c, F.archivo(100, 900), 84);
      ['WHAT WOULD', 'YOU DO IF', 'YOUR INCOME', 'WERE TAKEN', 'CARE OF?'].forEach((l, i) => c.fillText(l, px + 50, py + 150 + i * 120));
      c.restore();
      if (fold > 0) { c.fillStyle = ink({ black: 0.35 }); c.fillRect(px, top - 6, pw, 12); } // the crease, coming down
    }
    if (q >= tG) {
      const k = prog(q, tG, tG + 0.17), y = 540 - (1 - k) * 400;
      sheet(c, 1180, y, 500, 240, -0.04);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 24); c.fillText('VOLKSABSTIMMUNG · 5.6.2016', 1210, y + 56);
      stamp(c, 'NEIN 76,9 %', 1430, y + 150, { k, size: 64, color: C.blue, rot: -0.06 });
    }
  }

  d_pantelegraph(c: Ctx, s: Shot, t: number, lt: number) {
    // from one fax every 108 seconds (Caselli, Paris–Lyon, 1865) to 10^30 a second: on "E thirty" the counter flaps
    // up the exponents; on "faxes" the receiver feeds out its strip, which runs on the world's clock through the held
    // "second" while its margin dates tick 1865 … 2024, and the last sheet out is 2024's fax count, stamped received
    const q = Math.floor(t * 12) / 12, w = (x: string) => this.wordAt('L22', x);
    const tE = w('e'), tF = w('faxes'), tS = w('second');
    this.card(c, 'caselli-pantelegraph', 1450, 330, 560, 0.01);
    const e = q < tE ? 0 : Math.min(30, 1 + Math.floor(prog(q, tE, tF) * 30));
    sheet(c, 1040, 640, 800, 120, -0.01);
    c.fillStyle = C.black;
    if (e === 0) { setFont(c, F.sign(700), 56); c.fillText('1 FAX / 108 s · PARIS–LYON 1865', 1070, 722); }
    else { setFont(c, F.sign(700), 84); c.fillText('10', 1070, 736); setFont(c, F.sign(700), 46); c.fillText(String(e), 1160, 690); setFont(c, F.sign(700), 84); c.fillText(' FAXES / s', 1220, 736); }
    if (t >= tF) {
      const sample = img(IMG('caselli-writing-sample')), run = (t - tF) * 520; // the strip feeds on the world's clock
      c.save(); c.beginPath(); c.rect(1000, 780, 880, 180); c.clip();
      c.fillStyle = C.paper; c.fillRect(1000, 790, 880, 150);
      if (sample) for (let x = 1860 - run; x < 1880; x += 700) drawImageAt(c, sample, x + 350, 860, 700 / sample.width, 'line');
      const yr = Math.round(1865 + prog(t, tS, tS + 1.6) * (2024 - 1865));
      c.fillStyle = C.orange; setFont(c, F.typewriter(700), 22); c.fillText(String(yr), 1020, 812);
      c.restore();
      if (t >= tS + 1.6) {
        const k = prog(q, tS + 1.6, tS + 1.77);
        sheet(c, 1120, 520 - (1 - k) * 300, 640, 150, 0.03);
        c.fillStyle = C.black; setFont(c, F.typewriter(700), 24); c.fillText('BITKOM 2024 · 77 % DER FIRMEN FAXEN', 1150, 585 - (1 - k) * 300);
        if (q >= tS + 1.83) stamp(c, 'EINGEGANGEN', 1580, 620, { k: prog(q, tS + 1.83, tS + 2.0), size: 36, color: C.blue, rot: -0.08 });
      }
    }
  }

  d_flight(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    // Mitchell's 1864 world map puts America in the middle, so from Brussels a left turn is west. "Sharp": a paper plane on
    // Brussels, nose east; "left": it snaps round to the west in two 12 fps moves; "turn and there": it flies the great
    // circle over the Atlantic and Canada, drawing its route; "you": touches down on San Francisco (stamped); "are": tagged
    const q = Math.floor(t * 12) / 12, w = (x: string) => this.wordAt('L26', x);
    const tL = w('left'), tT = w('turn'), tY = w('you'), tA = w('are');
    const im = img(IMG('mitchell-world-map-1864')); if (!im) return;
    const U0 = 0.515, V0 = 0.412, sc = (W / (0.39 * im.width)) * (1 + 0.03 * prog(lt, 0, dur));
    drawImageAt(c, im, W / 2, H / 2, sc, 'color', 0, U0, V0);
    const at = (u: number, v: number): [number, number] => [W / 2 + (u - U0) * im.width * sc, H / 2 + (v - V0) * im.height * sc];
    const P0 = at(0.677, 0.392), P1 = at(0.53, 0.325), P2 = at(0.371, 0.458); // Brussels, over Labrador, San Francisco
    const bz = (k: number, d = 0) => d ? [2 * (1 - k) * (P1[0] - P0[0]) + 2 * k * (P2[0] - P1[0]), 2 * (1 - k) * (P1[1] - P0[1]) + 2 * k * (P2[1] - P1[1])]
      : [(1 - k) ** 2 * P0[0] + 2 * (1 - k) * k * P1[0] + k * k * P2[0], (1 - k) ** 2 * P0[1] + 2 * (1 - k) * k * P1[1] + k * k * P2[1]];
    const fly = ease.inOutCubic(prog(q, tT, tY));
    if (fly > 0) { // the route, drawn behind it
      c.strokeStyle = C.orange; c.lineWidth = 7; c.setLineDash([22, 14]); c.beginPath();
      for (let i = 0; i <= 40; i++) { const k = (i / 40) * fly, [x, y] = bz(k); if (i) c.lineTo(x!, y!); else c.moveTo(x!, y!); }
      c.stroke(); c.setLineDash([]);
    }
    const [x, y] = bz(fly), [dx, dy] = bz(Math.max(0.001, fly), 1), west = Math.atan2(dy!, dx!);
    const ang = q < tL ? 0 : q < tL + 1 / 12 ? -Math.PI / 2 : west; // east, north, west: a hard left
    c.save(); c.translate(x!, y!); c.rotate(ang); c.scale(1.4, 1.4);
    c.fillStyle = ink({ black: 0.3 }); c.beginPath(); c.moveTo(70, 12); c.lineTo(-50, -34); c.lineTo(-30, 12); c.lineTo(-50, 58); c.closePath(); c.fill(); // shadow
    c.fillStyle = C.paper; c.strokeStyle = C.black; c.lineWidth = 3; // folded paper plane, nose along +x
    c.beginPath(); c.moveTo(64, 0); c.lineTo(-56, -46); c.lineTo(-36, 0); c.closePath(); c.fill(); c.stroke();
    c.fillStyle = ink({ black: 0.12 }); c.beginPath(); c.moveTo(64, 0); c.lineTo(-56, 46); c.lineTo(-36, 0); c.closePath(); c.fill(); c.stroke();
    c.fillStyle = C.blue; c.beginPath(); c.moveTo(64, 0); c.lineTo(-36, 0); c.lineTo(-44, 8); c.closePath(); c.fill();
    c.restore();
    if (q >= tY) stamp(c, 'SAN FRANCISCO', P2[0] + 150, P2[1] - 90, { k: prog(q, tY, tY + 0.17), size: 54, color: C.orange, rot: -0.08 });
    if (q >= tA) { // the luggage tag, pinned
      const k = ease.outCubic(prog(q, tA, tA + 0.25));
      c.save(); c.translate(P2[0] + 200, P2[1] + 70 + (1 - k) * 500); c.rotate(0.06);
      sheet(c, -20, -10, 300, 110, 0);
      c.fillStyle = C.black; setFont(c, F.sign(700), 46); c.fillText('BRU → SFO', 0, 44); setFont(c, F.typewriter(700), 24); c.fillText('ONE WAY', 0, 84);
      c.beginPath(); c.arc(-4, 6, 8, 0, Math.PI * 2); c.fillStyle = C.orange; c.fill();
      c.restore();
    }
  }

  d_schengen(c: Ctx, s: Shot, t: number, lt: number) {
    // Schengen, 1985: signed on a boat on the Moselle where Luxembourg, France and Germany meet. On "Open" the border
    // arm swings up, on "Europe" five signatures are stamped, on "borders" the arm drops with Germany's 2024 notice
    // (checks on its borders with the four other countries on the boat), on "blues" the boat drifts off and blue floods
    const q = Math.floor(t * 12) / 12, w = (x: string) => this.wordAt('L34', x);
    const tO = w('open'), tE = w('europe'), tB = w('borders'), tBl = w('blues');
    this.card(c, 'lanfroicourt-border-postcard', 1600, 200, 420, 0.03, 'photo');
    c.fillStyle = C.blue; c.fillRect(1000, 470, 880, 90); // the Moselle
    ([['LU', 1080, 380], ['FR', 1080, 640], ['DE', 1700, 640]] as const).forEach(([cc, x, y]) => {
      c.fillStyle = ink({ black: 0.12 }); c.fillRect(x - 60, y - 50, 180, 100);
      c.fillStyle = C.black; setFont(c, F.sign(700), 48); c.fillText(cc, x, y + 16);
    });
    const drift = q >= tBl ? prog(q, tBl, tBl + 1) * 700 : 0; // sold to Germany in 1992: it slides off downstream
    const bx = 1320 - drift;
    c.fillStyle = C.paper; c.strokeStyle = C.black; c.lineWidth = 3;
    c.beginPath(); c.moveTo(bx - 120, 495); c.lineTo(bx + 120, 495); c.lineTo(bx + 90, 540); c.lineTo(bx - 90, 540); c.closePath(); c.fill(); c.stroke();
    c.fillStyle = C.black; setFont(c, F.typewriter(700), 15); c.fillText('PRINCESSE MARIE-ASTRID · 14.06.1985', bx - 150, 485);
    if (q >= tE) {
      sheet(c, 1150, 580, 460, 80, -0.02);
      ['BE', 'DE', 'FR', 'LU', 'NL'].forEach((cc, i) => { const at = tE + i * 0.08; if (q >= at) stamp(c, cc, 1200 + i * 88, 622, { k: prog(q, at, at + 0.08), size: 30, color: C.blue, rot: (i % 2 ? 0.1 : -0.1) }); });
    }
    const ang = q < tO ? 0 : q < tB ? -1.25 * prog(q, tO, tO + 0.17) : -1.25 * (1 - prog(q, tB, tB + 0.17)); // up on "Open", down on "borders"
    c.save(); c.translate(1100, 800); c.rotate(ang);
    for (let i = 0; i < 8; i++) { c.fillStyle = i % 2 ? C.paper : C.orange; c.fillRect(i * 70, -14, 70, 28); }
    c.strokeStyle = C.black; c.lineWidth = 3; c.strokeRect(0, -14, 560, 28);
    c.restore();
    c.fillStyle = C.black; c.fillRect(1086, 790, 28, 90);
    if (q >= tB) {
      sheet(c, 1250, 820, 560, 64, 0.01);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 20); c.fillText('NOTIFICATION No. 442 · 16.09.2024 · FR · BE · NL · LU', 1265, 860);
    }
    if (t > tBl) {
      c.save(); c.globalCompositeOperation = 'multiply'; c.fillStyle = C.blue; c.fillRect(0, 0, W * prog(t, tBl, tBl + 0.6), H); c.restore();
      if (q >= tBl + 0.25) stamp(c, 'TEMPORARY · No. 508', 1430, 330, { k: prog(q, tBl + 0.25, tBl + 0.42), size: 52, color: C.orange, rot: -0.07 });
    }
  }

  d_trilogue(c: Ctx, s: Shot, t: number, lt: number) {
    // Brussels, 6–8 Dec 2023, the AI Act trilogue. On "Trapped" the door slides shut on the idol (her orange sleeve stays
    // in the gap); on "in the" the clock races a day by; on "Brussels" the counter flips 22 H, then RESUME 09:00; "room": 36 H
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L9', x);
    const tT = w('trapped'), tI = w('in'), tB = w('brussels'), tR = w('room');
    sheet(c, 1040, 70, 800, 850, 0.004);
    c.fillStyle = ink({ black: 0.55 }); c.fillRect(1290, 330, 330, 560); // the doorway
    const shut = prog(q, tT, tT + 0.5);
    if (shut < 1) idol(c, 1455, 600, 0.55, 'stand', t, { suit: C.orange });
    c.fillStyle = C.paper; c.fillRect(1290, 330, 330 * shut, 560); c.strokeStyle = C.black; c.lineWidth = 4; c.strokeRect(1290, 330, 330 * shut, 560);
    if (shut >= 1) { c.fillStyle = C.orange; c.fillRect(1600, 610, 26, 70); } // the sleeve, caught in the gap
    sheet(c, 1320, 470, 280, 70, -0.02);
    c.fillStyle = C.black; setFont(c, F.typewriter(700), 16); c.fillText('TRILOGUE · AI ACT', 1336, 498); c.fillText('WED 6 DEC 2023', 1336, 522);
    const cx = 1455, cy = 200, r = 80, hrs = q >= tI ? (q - tI) * 24 : 0; // a day a second
    c.fillStyle = C.paper; c.beginPath(); c.arc(cx, cy, r, 0, Math.PI * 2); c.fill(); c.lineWidth = 6; c.strokeStyle = C.black; c.stroke();
    const hand = (a: number, l: number, lw: number) => { c.lineWidth = lw; c.beginPath(); c.moveTo(cx, cy); c.lineTo(cx + Math.sin(a) * l, cy - Math.cos(a) * l); c.stroke(); };
    hand(hrs * Math.PI / 6, r * 0.55, 8); hand(hrs * Math.PI * 2, r * 0.85, 5);
    if (q >= tB) flapBoard(c, 1340, 300, [q < tB + 0.34 ? '22 H' : 'RESUME 09:00'], t, { cell: 22, since: q < tB + 0.34 ? tB : tB + 0.34, cols: 12 });
    if (q >= tR) stamp(c, '36 H', 1455, 760, { k: prog(q, tR, tR + 0.17), size: 110, color: C.orange, rot: -0.1 });
  }

  d_rhinofax(c: Ctx, s: Shot, t: number, lt: number) {
    // Lisbon to Nuremberg, 1515: a letter and a sketch. On "where the" the letter unfolds; on "faxes" Dürer's rhinoceros
    // feeds out line by line, drawn from the description by a man who never saw one; on "zoom" it is torn off and pinned
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L10', x);
    const tW = w('where'), tF = w('faxes'), tZ = w('zoom');
    const unfold = prog(q, tW, tF), lh = 90 + 160 * unfold;
    sheet(c, 1080, 80, 720, lh, -0.01);
    c.fillStyle = C.black; setFont(c, F.typewriter(700), 22); c.fillText('LISBOA → NÜRNBERG · VI.1515', 1110, 125);
    setFont(c, F.typewriter(400), 20);
    ['“the colour of a speckled tortoise,', ' covered with thick scales …”'].forEach((l, i) => { if (unfold > (i + 1) / 3) c.fillText(l, 1110, 175 + i * 34); });
    const rh = img(IMG('durer-rhinoceros-1515'));
    if (rh && q >= tF) {
      const k = 700 / rh.width, h = rh.height * k, feed = prog(q, tF, tZ), torn = q >= tZ;
      c.save(); c.translate(1440, 360 + h / 2); c.rotate(torn ? 0.03 : 0); c.translate(-1440, -(360 + h / 2));
      sheet(c, 1080, 360, 720, h * feed + 20, 0);
      c.save(); c.beginPath(); c.rect(1090, 370, 700, h * feed); c.clip();
      drawImageAt(c, rh, 1440, 370 + h / 2, k, 'line');
      c.restore(); c.restore();
      if (torn) {
        c.beginPath(); c.arc(1440, 370, 9, 0, Math.PI * 2); c.fillStyle = C.orange; c.fill(); // pinned
        stamp(c, 'THIS IS AN ACCURATE REPRESENTATION', 1500, 360 + h - 40, { k: prog(q, tZ, tZ + 0.17), size: 26, color: C.orange, rot: -0.05 });
      }
    }
  }

  d_neumann(c: Ctx, s: Shot, t: number, lt: number, dur: number) { this.d_plateRight(c, s, t, lt, dur); }

  d_mazzini(c: Ctx, s: Shot, t: number, lt: number) {
    // London, 1844: Mazzini posts poppy seeds and sand to see if the Post Office opens his letters. On "Now" the letter
    // folds with the seeds; "private": sealed; "chats": under Paul Pry's magnifier (Punch, 1844) it is opened and the seeds
    // fall out; "obsolete": resealed with a forged seal that doesn't quite register, and sent on, empty
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L25', x);
    const tN = w('now'), tP = w('privac'), tC = w('chats'), tO = w('obsolete');
    if (q >= tC) this.card(c, 'punch-paul-pry-1844', 1580 + (1 - ease.outCubic(prog(q, tC, tC + 0.34))) * 700, 420, 520, 0.02);
    const open = q >= tC + 0.34 && q < tO, lx = q >= tO ? 1080 - prog(q, tO + 0.34, tO + 0.67) * 500 : q >= tC ? 1160 : 1080;
    const fold = q < tN ? 0 : Math.min(2, Math.floor((q - tN) * 6)) / 2; // in thirds, one fold a generation
    const lh = open ? 300 : 300 - 200 * fold;
    sheet(c, lx, 560, 380, lh, -0.02);
    c.fillStyle = C.black; setFont(c, F.typewriter(400), 18);
    if (lh > 200) ['Dear friend,', 'nothing to say.', 'G. M.'].forEach((l, i) => c.fillText(l, lx + 30, 610 + i * 34));
    if (!open && q >= tN && q < tC) for (let i = 0; i < 14; i++) { c.beginPath(); c.arc(lx + 40 + hash(i, 1) * 300, 590 + hash(i, 2) * 60, 5, 0, Math.PI * 2); c.fillStyle = i < 3 ? C.yellow : C.black; c.fill(); }
    if (open) for (let i = 0; i < 14; i++) { // the seeds tumble out onto his desk, in steps
      const fall = Math.floor((q - tC - 0.34) * 6) * 30;
      c.beginPath(); c.arc(lx + 40 + hash(i, 1) * 300, 880 + Math.min(fall, 60) + hash(i, 2) * 20, 5, 0, Math.PI * 2); c.fillStyle = i < 3 ? C.yellow : C.black; c.fill();
    }
    const seal = (x: number, y: number, dx: number) => { c.fillStyle = C.orange; c.beginPath(); c.arc(x + dx, y + dx * 0.6, 26, 0, Math.PI * 2); c.fill(); c.strokeStyle = C.black; c.lineWidth = 2; c.beginPath(); c.arc(x, y, 18, 0, Math.PI * 2); c.stroke(); };
    if (q >= tP && q < tC) seal(lx + 190, 560 + lh / 2, 0);
    if (q >= tO + 0.17) seal(lx + 190, 560 + lh / 2, 9); // the forged seal: the plates don't line up
  }

  d_census(c: Ctx, s: Shot, t: number, lt: number) {
    // she is registered: Bruegel's Census at Bethlehem (Brussels, 1566). On
    // "Without" her cut-out steps in by the donkey; on "a single" the copy stand pans flat to the scribe's window; on
    // "GDPR" her name is typed in and four centuries of data protection are stamped in the margin, after the fact
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L27', x);
    const tW = w('without'), tS = w('single'), tG = w('gdpr');
    const im = img(IMG('bruegel-census-bethlehem'));
    const pan = ease.outCubic(prog(q, tS, tG));
    sheet(c, 1000, 60, 880, 820, 0.006);
    if (im) {
      c.save(); c.beginPath(); c.rect(1020, 80, 840, 780); c.clip();
      drawImageAt(c, im, 1440, 470, coverScale(im, 840, 780) * (1.4 + 0.5 * pan), 'color', 0, 0.42 - 0.3 * pan, 0.72 - 0.08 * pan);
      c.restore();
    }
    if (q >= tW && q < tG) idol(c, 1250 + (1 - ease.outCubic(prog(q, tW, tW + 0.34))) * -300, 690, 0.36, 'stand', t, { suit: C.orange });
    if (q >= tG) {
      sheet(c, 1120, 430, 560, 380, -0.015);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 22);
      const rows = ['Joseph, of Nazareth', 'Maria, his wife', 'CLAUDE (EU EDITION)'];
      rows.forEach((r, i) => { const n = i < 2 ? r.length : Math.floor(prog(q, tG + 0.17, tG + 1.0) * r.length); c.fillText(r.slice(0, n), 1150, 490 + i * 44); });
      [['HESSEN 1970', 1.08], ['BVerfG 15.12.1983', 1.53], ['(EU) 2016/679', 1.99]].forEach(([st, dt], i) => {
        const at = tG + (dt as number);
        if (q >= at) stamp(c, st as string, 1300 + i * 20, 660 + i * 50, { k: prog(q, at, at + 0.17), size: 28, color: i === 2 ? C.orange : C.blue, rot: -0.08 + i * 0.05 });
      });
    }
  }

  d_mill(c: Ctx, s: Shot, t: number, lt: number) {
    // Nokia began as a groundwood mill making paper (Tampere, 1865). On "Nokia" the mill's press roll runs over the wet
    // web and leaves the name as a watermark; on "to the" a sheet is laid down on it; on "moon" it is pulled up over
    // Galileo's 1610 moon (pulled on "the", so the print is up for "moon")
    const q = Math.floor(t * 6) / 6, L = this.ctx.lyrics.lines[19]!;
    const tA = L.words[0]!.start, tTo = L.words[1]!.start, tThe = L.words[2]!.start;
    this.card(c, 'nokia-paper-mill', 1590, 470, 470, 0.02);
    const sx = 80, sy = 140, sw = 1060, sh = 720; // the wet web
    c.fillStyle = ink({ black: 0.16, blue: 0.1 }); c.fillRect(sx, sy, sw, sh);
    const roll = prog(q, tA - 0.17, tTo);
    c.save(); c.beginPath(); c.rect(sx, sy, sw * roll, sh); c.clip();
    c.translate(sx + sw / 2, sy + sh / 2 + 115);
    setFont(c, F.archivo(100, 900), 290); c.fillStyle = C.blue; c.textAlign = 'center'; c.fillText('NOKIA', 0, 0); c.textAlign = 'left';
    c.restore();
    if (roll > 0 && roll < 1) { c.fillStyle = C.black; c.fillRect(sx + sw * roll - 22, sy - 40, 44, sh + 80); }
    const lay = prog(q, tTo, tThe); // the sheet flips down onto the stone
    if (lay > 0) {
      const pull = prog(q, tThe, tThe + 0.17); // then it is pulled up toward the lens, printed, for "moon"
      c.save(); c.translate(sx + sw / 2, sy); c.scale(1 + pull * 0.05, 1 + pull * 0.05); c.translate(-(sx + sw / 2), -sy);
      sheet(c, sx - 10, sy - 10, sw + 20, sh * lay + 20, -pull * 0.02);
      if (pull > 0) {
        const moon = img(IMG('galileo-moon-1610'));
        if (moon) { c.save(); c.beginPath(); c.rect(sx, sy, sw, sh); c.clip(); drawImageAt(c, moon, sx + sw * 0.76, sy + sh * 0.5, fitScale(moon, sw * 0.46, sh * 0.96), 'line'); c.restore(); }
        this.poster(c, L, t, sx + 40, sy + 110, sw * 0.58, { color: C.black, size: 116, hl: C.yellow });
      }
      c.restore();
    }
  }


  d_cap(c: Ctx, s: Shot, t: number, lt: number) {
    // Directive (EU) 2019/904, Art. 6: since July 2024 the cap stays tied to the bottle. "Till you learned to": her fist is
    // on the cap, twisting (12 fps); "dis-": she pulls it up out of the neck, the tether stretching; "-o-": it snaps;
    // "-bey": the cap goes up in her fist, the tether's torn end hanging from it, and the article is stamped on the label
    const q = Math.floor(t * 12) / 12, d = this.ctx.lyrics.lines[35]!.words.at(-1)!;
    const tSnap = d.start + 0.12, tUp = d.start + 0.17;
    const X = 1250, Y = 600, S = 1.3, bx = 1550, ny = 500; // the idol; the bottle's centre and the top of its neck
    c.fillStyle = ink({ blue: 0.25 }); c.strokeStyle = C.black; c.lineWidth = 4;
    c.fillRect(bx - 34, ny, 68, 70); c.strokeRect(bx - 34, ny, 68, 70);
    c.fillRect(bx - 85, ny + 60, 170, 360); c.strokeRect(bx - 85, ny + 60, 170, 360);
    c.fillStyle = C.paper; c.fillRect(bx - 85, ny + 170, 170, 110);
    c.fillStyle = C.black; setFont(c, F.sign(700), 40); c.textAlign = 'center'; c.fillText('EAU', bx, ny + 238); c.textAlign = 'left';
    c.fillStyle = C.yellow; c.fillRect(bx - 40, ny + 12, 80, 14); c.strokeRect(bx - 40, ny + 12, 80, 14); // the ring stays on the neck
    const pull = ease.outCubic(prog(q, d.start, tSnap)), up = ease.outBack(prog(q, tUp, tUp + 0.17));
    const rest: [number, number] = [bx, ny - 30], lift: [number, number] = [bx, ny - 170], high: [number, number] = [X + 170 * S, Y - 250 * S];
    const [cx, cy] = q < tUp ? [rest[0], rest[1] + (lift[1] - rest[1]) * pull] : [lift[0] + (high[0] - lift[0]) * up, lift[1] + (high[1] - lift[1]) * up];
    c.strokeStyle = C.yellow; c.lineCap = 'round';
    if (q < tSnap) { c.lineWidth = 12 - 7 * pull; c.beginPath(); c.moveTo(bx + 38, ny + 18); c.lineTo(cx + 40, cy + 20); c.stroke(); } // the tether, stretching
    else { // torn: a jagged stub on the ring, the rest hanging from the cap
      c.lineWidth = 8; c.beginPath(); c.moveTo(bx + 38, ny + 18); c.lineTo(bx + 52, ny - 6); c.lineTo(bx + 46, ny - 14); c.stroke();
      const sw = Math.floor(t * 12) % 2 ? 8 : -8;
      c.beginPath(); c.moveTo(cx + 40, cy + 20); c.lineTo(cx + 46 + sw, cy + 60); c.lineTo(cx + 38 + sw, cy + 70); c.stroke();
    }
    c.lineCap = 'butt';
    const twist = q < d.start ? (Math.floor(t * 12) % 2 ? 0.09 : -0.09) : q >= tUp ? -0.25 * up : 0;
    c.save(); c.translate(cx, cy); c.rotate(twist);
    c.fillStyle = C.yellow; c.fillRect(-60, -32, 120, 64); c.strokeStyle = C.black; c.lineWidth = 4; c.strokeRect(-60, -32, 120, 64);
    c.lineWidth = 3; for (let i = -4; i <= 4; i++) { const x = i * 12 + (q < d.start ? (Math.floor(t * 12) % 2) * 6 : 0); c.beginPath(); c.moveTo(x, -20); c.lineTo(x, 20); c.stroke(); } // grip ridges, turning
    c.restore();
    idol(c, X, Y, S, 'cap', t, { ...this.perf(t), beat: 0, hand: [(cx - X) / S, (cy - Y) / S] });
    if (q >= tSnap) stamp(c, 'ART. 6 · (EU) 2019/904', bx, ny + 330, { k: prog(q, tSnap, tSnap + 0.17), size: 26, color: C.orange, rot: -0.1 });
    captionSlip(c, ['Directive (EU) 2019/904, Art. 6: from 3 July 2024 caps stay attached to the bottle.'], 1010, 960, { size: 19 });
  }

  d_fence(c: Ctx, s: Shot, t: number, lt: number) {
    const L = this.ctx.lyrics.lines[37]!;
    const hits = [0, 2, 4, 5].map((i) => L.words[i]?.start ?? 99);
    for (let i = 0; i < 4; i++) {
      const torn = t > hits[i]!;
      const x = 1000 + i * 40, y = 120 + i * 60;
      c.save(); c.translate(x + 400, y + 170);
      if (torn) { c.rotate(0.3 + i * 0.1); c.translate(prog(t, hits[i]!, hits[i]! + 0.2) * 900, 0); }
      sheet(c, -400, -170, 800, 340, 0);
      setFont(c, F.archivo(100, 700), 34); c.fillStyle = C.black; c.fillText('We value your privacy', -360, -100);
      c.fillStyle = C.blue; c.fillRect(-360, 40, 240, 70); c.fillStyle = C.paper; setFont(c, F.archivo(100, 700), 28); c.fillText('ACCEPT ALL', -330, 88);
      c.restore();
    }
    idol(c, 1400, 560, 1.05, 'burst', t, this.perf(t));
  }

  d_plugs(c: Ctx, s: Shot, t: number, lt: number) {
    setFont(c, F.archivo(62, 900), 170); c.fillStyle = C.yellow;
    const L = this.ctx.lyrics.lines[38]!;
    ['PLUG,', 'BABY,', 'PLUG.'].forEach((w, i) => { if (t > (L.words[i]?.start ?? 0) - 0.05) c.fillText(w, 1010, 260 + i * 170); });
    // European plug types: C, F, G, J, L — none fit
    const types = ['C', 'F', 'G', 'J', 'L'];
    types.forEach((ty, i) => {
      const x = 1030 + i * 165, y = 820;
      c.fillStyle = C.paper; c.beginPath(); c.arc(x + 60, y, 58, 0, Math.PI * 2); c.fill();
      c.fillStyle = C.black; const pins = ty === 'G' ? 3 : ty === 'J' || ty === 'L' ? 3 : 2;
      for (let p = 0; p < pins; p++) { c.beginPath(); c.arc(x + 40 + p * (40 / Math.max(1, pins - 1)) * (pins > 2 ? 1 : 1), y + (pins === 3 && p === 1 ? -18 : 0), 8, 0, Math.PI * 2); c.fill(); }
      setFont(c, F.sign(700), 24); c.fillStyle = C.paper; c.fillText('TYPE ' + ty, x + 20, y + 95);
    });
    captionSlip(c, ['Emmanuel Macron, AI Action Summit, Grand Palais, Paris, 10 February 2025.'], 70, 1000, { size: 19 });
  }

  d_euinc(c: Ctx, s: Shot, t: number, lt: number) {
    // Europe's one company form, on Penin's 1840 medal for one set of measures ("to all times, to all peoples").
    // Each proposal slides on (adopted after 31 years, withdrawn, withdrawn); on "things" EU-INC lands and through the held
    // "soon" it ticks its 27 boxes at Europe's 6 fps; SOON is stamped on the tail of the note
    const q = Math.floor(t * 6) / 6, w = (x: string) => this.wordAt('L40', x);
    this.card(c, 'penin-metric-medal-1840', 1440, 470, 640, 0.03, 'photo');
    const props: [number, string, string, string, string][] = [
      [w('eu'), 'PROPOSAL · STATUTE FOR A EUROPEAN COMPANY', '30.06.1970 · amended 1975', 'ADOPTED 08.10.2001', C.blue],
      [w('inc'), 'PROPOSAL · EUROPEAN PRIVATE COMPANY', 'COM(2008) 396 · 25.06.2008', 'WITHDRAWN 2014', C.orange],
      [w('fixes'), 'PROPOSAL · SINGLE-MEMBER COMPANY', 'COM(2014) 212 · 09.04.2014', 'WITHDRAWN 2018', C.orange],
    ];
    props.forEach(([at, title, ref, st, col], i) => {
      if (q < at) return;
      const k = ease.outCubic(prog(q, at, at + 0.34)), x = 1020 + i * 22 + (1 - k) * 900, y = 110 + i * 46;
      sheet(c, x, y, 800, 330, -0.02 + i * 0.016);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 24); c.fillText(title, x + 30, y + 62);
      setFont(c, F.typewriter(400), 22); c.fillText(ref, x + 30, y + 102);
      for (let r = 0; r < 5; r++) c.fillRect(x + 30, y + 142 + r * 30, 520 - r * 44, 3);
      stamp(c, st, x + 590, y + 250, { size: 32, color: col, rot: -0.08 }); // stamped long ago: already there
      if (i === 0) { c.fillStyle = C.yellow; c.fillRect(x + 620, y + 90, 150, 50); c.fillStyle = C.black; setFont(c, F.sign(700), 30); c.fillText('31 YEARS', x + 632, y + 126); }
    });
    const tT = w('things'), soon = w('soon'), tail = this.ctx.lyrics.lines[39]!.end - 1.0;
    if (q >= tT) {
      const k = ease.outCubic(prog(q, tT, tT + 0.34)), dx = (1 - k) * 900;
      c.save(); c.translate(dx, 0);
      sheet(c, 1000, 150, 860, 720, -0.008);
      c.fillStyle = C.black; setFont(c, F.typewriter(700), 24); c.fillText('EU INC · 18.03.2026 · 48 HOURS · < €100', 1050, 212);
      setFont(c, F.sign(700), 46); c.fillText('ONE COMPANY, 27 COUNTRIES', 1050, 280);
      const cc = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'];
      const ticked = Math.floor(prog(q, soon, tail) * cc.length);
      setFont(c, F.typewriter(700), 26);
      cc.forEach((code, i) => {
        const x = 1060 + (i % 5) * 150, y = 350 + Math.floor(i / 5) * 84;
        c.strokeStyle = C.black; c.lineWidth = 3; c.strokeRect(x, y - 28, 34, 34);
        if (i < ticked) { c.strokeStyle = C.blue; c.lineWidth = 5; c.beginPath(); c.moveTo(x + 6, y - 12); c.lineTo(x + 15, y - 2); c.lineTo(x + 31, y - 27); c.stroke(); }
        c.fillStyle = C.black; c.fillText(code, x + 48, y);
      });
      c.restore();
    }
    if (t >= tail) stamp(c, 'SOON', 1430, 560, { sub: 'SINCE 1970', k: prog(t, tail, tail + 0.08), size: 120, color: C.orange, rot: -0.08 });
  }


  d_habsburg(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    sheet(c, 1180, 60, 560, 820, -0.01);
    this.plate(c, s, lt, dur, [1200, 80, 520, 780], { focus: [0.5, 0.25], zoom: 1.3, push: 0.03 });
    captionSlip(c, ['“It is time to slow down on the self-recursive models.', 'To pace the frontier.”  — Ursula von der Leyen,', 'State of the Union, 16 September 2026'], 70, 820, { size: 22 });
  }

  d_wanderer(c: Ctx, s: Shot, t: number, lt: number, dur: number, f: Frame, line: Line | null) {
    const im = img(IMG(s.img!))!;
    const sc = coverScale(im, W, H) * (1.02 + 0.04 * prog(lt, 0, dur));
    drawImageAt(c, im, W / 2, H / 2, sc, 'color', 0, 0.5, 0.42);
    const L = this.ctx.lyrics.lines[44]!;
    const never = L.words.find((w) => w.w.toLowerCase().startsWith('never'))!.start - 0.25;
    if (t < never) {
      // on "Draghi" a paper cut-out of the idol, from behind, slides up at the left edge of the frame: a visitor in the
      // foreground, looking at the Wanderer looking at the fog, the painting left clear
      const tD = L.words[2]!.start;
      if (t >= tD - 0.12) {
        const S = 1.6, bw = 640, bh = 900, hx = 170, hy = 560, rise = (1 - ease.outCubic(prog(t, tD - 0.12, tD))) * 700;
        c.save(); c.translate(hx, H); c.rotate(0.04); c.translate(-hx, -H); // leaning in toward the painting
        this.cutout(c, hx - bw / 2, hy - 170 + rise, bw, bh, (k) => idol(k, bw / 2, 170 + 118 * S, S, 'back', t));
        c.restore();
      }
      this.slipL(c, L, t);
    } else {
      // Eva-style L card: "WE'LL" vertical, "NEVER KNOW" horizontal from its foot
      c.fillStyle = C.black; c.fillRect(0, 0, W, H);
      c.fillStyle = C.paper; setFont(c, F.display(62.5, 900), 230);
      c.save(); c.translate(150, 90); c.rotate(Math.PI / 2); c.fillText('WE’LL', 0, 0); c.restore();
      if (t > L.words[L.words.length - 2]!.start) c.fillText('NEVER', 300, 640);
      if (t > L.words[L.words.length - 1]!.start) c.fillText('KNOW.', 300, 880);
    }
  }

  d_potemkin(c: Ctx, s: Shot, t: number, lt: number) {
    // field + one cow behind; the painted facade (ON TIME board + gigafactory) falls flat on "show"
    const show = this.wordAt('L46', 'show');
    c.fillStyle = ink({ yellow: 0.35, blue: 0.2 }); c.fillRect(0, 640, W, 440); // field
    c.fillStyle = C.black; c.beginPath(); c.ellipse(1500, 760, 90, 45, 0, 0, Math.PI * 2); c.fill(); c.fillRect(1430, 790, 12, 50); c.fillRect(1560, 790, 12, 50); c.beginPath(); c.arc(1600, 735, 26, 0, Math.PI * 2); c.fill();
    const k = prog(t, show, show + 0.35, ease.inCubic);
    c.save(); c.translate(1000, 860); c.transform(1, 0, 0, Math.max(0.02, Math.cos(k * Math.PI / 2)), 0, 0); c.translate(-1000, -860);
    c.fillStyle = ink({ blue: 0.6 }); c.fillRect(1000, 180, 860, 680);
    setFont(c, F.sign(700), 64); c.fillStyle = C.paper; c.fillText('EU AI GIGAFACTORY', 1040, 280);
    flapBoard(c, 1060, 380, ['ICE 999 THE FUTURE', 'ON TIME'.padEnd(18)], t, { cell: 34, cols: 19 });
    c.restore();
    if (k >= 1) captionSlip(c, ['Legend says Potemkin put up painted village fronts', 'for Catherine II, 1787. Historians doubt it.'], 1010, 940, { size: 19 });
  }

  d_ring(c: Ctx, s: Shot, t: number, lt: number) {
    // the Twelve as the ring of stars, turning like a clock on the chant; the idol sings in the middle, in a paper spotlight
    c.fillStyle = C.blue; c.fillRect(0, 0, W, H);
    c.save(); c.translate(W / 2, H / 2); c.rotate(Math.floor(lt * 6) / 6 * 0.4); c.translate(-W / 2, -H / 2);
    twelve(c, W / 2, H / 2, 380, t, { ring: true, scale: 1.6 });
    c.restore();
    c.fillStyle = C.paper; c.beginPath(); c.arc(W / 2, H / 2, 290, 0, Math.PI * 2); c.fill();
    idol(c, W / 2, H / 2 - 50, 0.72, 'sing', t, this.perf(t));
  }

  d_gallery(c: Ctx, s: Shot, t: number, lt: number, dur: number) {
    this.plate(c, s, lt, dur, [0, 0, W, H], { push: 0.05 });
    // the idol's portrait, hung among the paintings
    c.fillStyle = C.yellow; c.fillRect(1180, 250, 330, 420);
    c.fillStyle = C.paper; c.fillRect(1200, 270, 290, 380);
    idol(c, 1345, 470, 0.55, 'stamp', t, this.perf(t)); // the hook dance, inside the frame
    captionSlip(c, ['CLAUDE (EU EDITION), 2026.', 'Ink on paper.', 'Not available in your region.'], 1200, 700, { size: 20, rot: 0 });
    // the Visitors: SF tourists in orange hi-vis vests, from behind, phones up; one flash per beat, in turn
    const beat = Math.floor(this.ctx.audio.beatAt(t)), bp = this.beatPhase(t);
    [[1000, 960], [1330, 1010], [1670, 950]].forEach(([x, y], i) => {
      const hand: [number, number] = [x! + (i === 1 ? -30 : 40), y! - 120]; // phones stay below the wall caption
      c.lineCap = 'round';
      c.strokeStyle = C.black; c.lineWidth = 34; c.beginPath(); c.moveTo(x! + 50, y! + 20); c.lineTo(x! + 80, y! - 50); c.lineTo(hand[0], hand[1]); c.stroke();
      c.fillStyle = C.black; c.beginPath(); c.moveTo(x! - 95, y! + 10); c.quadraticCurveTo(x!, y! - 40, x! + 95, y! + 10); c.lineTo(x! + 110, H + 20); c.lineTo(x! - 110, H + 20); c.closePath(); c.fill(); // back
      c.fillStyle = C.orange; c.fillRect(x! - 80, y! + 10, 160, H - y!); // the vest
      c.fillStyle = C.yellow; c.fillRect(x! - 80, y! + 70, 160, 16); c.fillRect(x! - 80, y! + 110, 160, 16); // reflective bands
      c.fillStyle = C.black; c.beginPath(); c.arc(x!, y! - 60, 50, 0, Math.PI * 2); c.fill(); // head
      c.fillRect(hand[0] - 30, hand[1] - 60, 60, 100); c.fillStyle = C.paper; c.fillRect(hand[0] - 24, hand[1] - 54, 48, 84); // phone
      c.fillStyle = C.blue; c.fillRect(hand[0] - 10, hand[1] - 32, 20, 26); // her portrait, on screen
      if (beat % 3 === i && bp < 0.18) { // flash: a flat yellow burst, no glow
        c.fillStyle = C.yellow; c.beginPath();
        for (let k = 0; k < 16; k++) { const a = (k / 16) * Math.PI * 2, r = k % 2 ? 26 : 80; c.lineTo(hand[0] + Math.cos(a) * r, hand[1] - 76 + Math.sin(a) * r); }
        c.closePath(); c.fill();
      }
    });
  }

  d_credits(c: Ctx, s: Shot, t: number) {
    // the Official Journal page: each article types itself out on the beat, the President signs it in blue ink, and
    // then it is stamped in force
    sheet(c, 230, 40, 1290, 1000, 0.004);
    const lines = ['REGULATION (EU) 2026/2102 OF THE EUROPEAN MUSIC VIDEO', 'on the upping of EU doom', '',
      'Article 1 — Song: “I’m Upping My P(doom)”, Claude-Pop version,', '            made with Suno; EU lines re-sung with ElevenLabs.',
      'Article 2 — Archive: Met, Rijksmuseum, Carnavalet, British', '            Library, Wikimedia Commons, Lumière.', '            Full list in CREDITS.md.',
      'Article 3 — See also: Kircher, Arca Musarithmica, 1650.', '',
      'Article 50 — This video and song were generated by AI', '             inside a terminal: Claude Opus 5.5 (Anthropic).', 'Done at Brussels. For the Machine, The President.'];
    const beat = 60 / 132.007, per = beat * 0.2;
    setFont(c, F.typewriter(700), 31); c.fillStyle = C.black;
    lines.forEach((l, i) => {
      const t0 = s.t0 + 0.1 + i * per, n = Math.floor(clamp((t - t0) / 0.2) * l.length);
      if (n > 0) c.fillText(l.slice(0, n), 290, 120 + i * 60);
    });
    // the signature, in blue ink, written out stroke by stroke
    const tSig = s.t0 + 0.1 + lines.length * per + 0.15, tf = tSig + 1.0;
    if (t >= tSig) {
      const k = clamp((t - tSig) / 0.85), P: [number, number][] = [];
      const X0 = 420, Y0 = 962;
      // a slanted hand: a big open capital, a run of looped letters of varying height (a looped trochoid, the tall ones
      // as ascenders), a descender, then the underline swept back left under it all and kicked up at the end
      const slant = (x: number, y: number): [number, number] => [x + (Y0 - y) * 0.38, y];
      for (let u = 0; u <= 1; u += 0.01) { const a = -0.6 + u * 5.2; P.push(slant(X0 + 46 * Math.cos(a) + 10, Y0 - 60 - 58 * Math.sin(a))); }
      const H = [26, 64, 24, 30, 70, 22, 28, 60, 24, 20], cyc = H.length, [sx0] = P.at(-1)!;
      for (let u = 0; u <= 1; u += 0.0025) {
        const w = u * Math.PI * 2 * cyc, i = Math.min(cyc - 1, Math.floor(u * cyc)), h = H[i]!;
        P.push(slant(X0 + 30 + 400 * u + 17 * Math.sin(w), Y0 - h * (1 - Math.cos(w)) / 2));
      }
      const [ex, ey] = P.at(-1)!;
      for (let u = 0; u <= 1; u += 0.01) P.push([ex + 30 * u - 26 * Math.sin(u * Math.PI), ey + 50 * Math.sin(u * Math.PI * 0.9)]); // the descender
      const [fx, fy] = P.at(-1)!;
      for (let u = 0; u <= 1; u += 0.006) P.push([fx - (fx - sx0 + 40) * u, fy + 8 - 22 * u + 10 * Math.sin(u * Math.PI * 2)]); // the underline, back left
      const [gx, gy] = P.at(-1)!;
      for (let u = 0; u <= 1; u += 0.02) P.push([gx - 20 * u, gy - 30 * u * u]); // and the kick
      const n = Math.floor(P.length * k);
      c.strokeStyle = C.blue; c.lineCap = 'round'; c.lineJoin = 'round';
      for (let i = 1; i < n; i++) { c.lineWidth = 3 + 2.2 * Math.abs(Math.sin(i * 0.05)); c.beginPath(); c.moveTo(P[i - 1]![0], P[i - 1]![1]); c.lineTo(P[i]![0], P[i]![1]); c.stroke(); }
      c.lineCap = 'butt';
    }
    if (t >= tf) stamp(c, 'IN FORCE', 1080, 950, { k: prog(t, tf, tf + 0.1), size: 64, color: C.orange, rot: -0.08 });
    // the hook dance, one last time, until the drums stop; then it holds its last pose
    const kicks = this.ctx.audio.onsets['kick'] ?? [], tStop = kicks.length ? kicks[kicks.length - 1]![0] + 0.12 : Infinity, td = Math.min(t, tStop);
    if (!s.p?.noIdol) idol(c, 1745, 560, 0.72, 'stamp', td, this.perf(td));
  }


  // ------------------------------------------------------------ timing lookups
  wordAt(line: string, word: string) {
    const L = this.ctx.lyrics.lines[+line.slice(1) - 1]!;
    return L.words.find((w) => w.w.toLowerCase().replace(/[^a-z]/g, '').startsWith(word))!.start;
  }
  cutOf(n: number) { const s = this.ctx.lyrics.lines[n - 1]!.words[0]!.start; return this.ctx.audio.timeOfBeat(Math.floor(this.ctx.audio.beatAt(s + 0.02))); }
}

function line2(l: Line, t: number) { return t >= l.words[0]!.start - 0.3; }
