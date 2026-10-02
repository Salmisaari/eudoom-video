// The story cut, alive (after hybrid.ts, which stays as it was): every archival plate is filmed on the copy stand
// along the lyric. The camera travels to the detail each word is about and lands on it as the word is sung
// (data/timing_eu.json), drifts while a line holds, and the platen presses on every kick. Bruegel's big fish opens
// its mouth on "eat"; Icarus is a ploughman on "stable" and a splash on "begun"; the Turk's hidden operator is the
// "servant"; Pinocchio's nose is the "lies".
import type * as THREE from 'three';
import type { Frame } from '../engine/scene';
import Hybrid from './hybrid';
import { C, ink } from '../engine/palette';
import { F } from '../engine/type';
import { clamp, ease, prog, hash } from '../engine/util';
import { step, S16, arch } from './_kin';
import { img, loadImage, drawImageAt, coverScale, captionSlip, stamp, flapBoard, idolBust, idol, sheet, setFont, W, H, type Treat } from './_kit';

type Ctx = CanvasRenderingContext2D;
/** A camera key: when (a word 'L6:eat', a line 'L6' = its first word, or seconds), the image point at the centre of
 *  the frame (u, v in 0..1) and the zoom over the image's cover scale. */
type Key = [string | number, number, number, number];

// where the camera goes, per shot (focal points read off the plates on a 10 % grid)
const KEYS: Record<string, Key[]> = {
  frank: [['L1:in', 0.3, 0.55, 1.6], ['L1:eyes', 0.2, 0.57, 2.6]],
  chappe: [['L2', 0.5, 0.5, 1.0], ['L2:circuits', 0.32, 0.3, 1.6], ['L2:nervous', 0.62, 0.55, 1.7], ['L3', 0.5, 0.5, 1.05]],
  turk: [['L5', 0.5, 0.5, 1.0], ['L5:servant', 0.5, 0.7, 1.45], ['L5:and', 0.5, 0.55, 1.05], ['L5:boss', 0.4, 0.24, 1.8]],
  bigfish: [['L6:eat', 0.64, 0.47, 1.9], ['L6:me', 0.3, 0.42, 1.8], ['L6:alive', 0.5, 0.5, 1.04]],
  foom: [['L8', 0.5, 0.55, 1.0], ['L8:future', 0.48, 0.47, 1.45], ['L8:foom', 0.47, 0.42, 2.1]],
  pinocchio: [['L11', 0.5, 0.5, 1.0], ['L11:pinocchio', 0.45, 0.32, 1.5], ['L11:lies', 0.47, 0.19, 2.8]],
  icarus: [['L13', 0.5, 0.5, 1.05], ['L13:stable', 0.41, 0.6, 1.9], ['L13:training', 0.31, 0.62, 2.0], ['L13:run', 0.62, 0.56, 1.7],
    ['L14', 0.74, 0.55, 1.7], ['L14:the', 0.8, 0.8, 2.6]],
  neumann: [['L25', 0.5, 0.55, 1.0], ['L25:von', 0.5, 0.47, 1.35], ['L25:neumann', 0.48, 0.45, 2.1], ['L25:obsolete', 0.5, 0.5, 1.15]],
  navier: [['L14:singularity', 0.5, 0.5, 1.0], ['L14:begun', 0.6, 0.3, 2.3]],
  piranesi: [['L32', 0.5, 0.5, 1.0], ['L32:nowhere', 0.45, 0.85, 1.9], ['L32:go', 0.6, 0.45, 1.8]],
  nobel: [['L33', 0.45, 0.45, 1.0], ['L33:lit', 0.45, 0.36, 1.5], ['L33:fuse', 0.43, 0.32, 2.0]],
  jacquard: [['L42', 0.5, 0.5, 1.0], ['L42:foretold', 0.3, 0.55, 1.6], ['L42:loom', 0.38, 0.32, 2.4]],
  habsburg: [['L44', 0.5, 0.3, 1.3], ['L44:recursive', 0.3, 0.44, 2.2], ['L44:self', 0.3, 0.42, 3.0]],
  wanderer: [['L45', 0.5, 0.42, 1.02], ['L45:draghi', 0.53, 0.38, 1.5], ['L45:see', 0.72, 0.5, 1.4]],
  gallery: [[145.97, 0.2, 0.55, 1.4], [148.0, 0.75, 0.5, 1.3]],
};


// The Eurovision shot is printed with the yellow drum swapped for fluorescent green (Riso Fluorescent Green, see
// render()): there, whatever is yellow prints neon green, the bolero's and the Liverpool chorus's lasers.
const FLUO = '#44d62c';
const LIME = C.yellow, GREEN = C.yellow;
/** the member states' flags in the four inks (red prints orange); the EU's own is last */
const FLAGS: ['h' | 'v', string[], string?][] = [ // (yellow prints green in this shot, so no flag here needs yellow)
  ['v', [C.blue, C.paper, C.orange]], // France
  ['v', [GREEN, C.paper, C.orange]], // Italy
  ['v', [GREEN, C.paper, C.orange]], // Ireland
  ['h', [C.orange, C.paper, C.blue]], // the Netherlands
  ['h', [C.orange, C.paper, C.orange]], // Austria
  ['h', [C.orange, C.orange, C.paper, C.orange, C.orange]], // Latvia, 2:1:2
  ['h', [C.blue, C.black, C.paper]], // Estonia
  ['h', [C.orange, C.paper, GREEN]], // Hungary
  ['h', [C.paper, GREEN, C.orange]], // Bulgaria
  ['h', [C.orange, C.paper, ink({ blue: 0.45 })]], // Luxembourg
  ['v', [GREEN, GREEN, C.orange, C.orange, C.orange]], // Portugal, 2:3
  ['h', [C.paper, C.orange]], // Poland
  ['h', [C.orange], 'cross'], // Denmark
  ['h', [C.paper, C.orange], 'wedge'], // Czechia
  ['h', [C.blue], 'stars'], // the EU
];
function flag(c: Ctx, n: number, x: number, y: number, w: number, h: number, wave: number) {
  const [dir, cols, extra] = FLAGS[n]!;
  c.save(); c.transform(1, wave / w, 0, 1, x, y); // the flag shears as it waves
  cols.forEach((col, i) => { c.fillStyle = col; if (dir === 'h') c.fillRect(0, (i * h) / cols.length, w, h / cols.length + 0.5); else c.fillRect((i * w) / cols.length, 0, w / cols.length + 0.5, h); });
  if (extra === 'cross') { c.fillStyle = C.paper; c.fillRect(w * 0.33, 0, h * 0.14, h); c.fillRect(0, h * 0.43, w, h * 0.14); }
  if (extra === 'wedge') { c.fillStyle = C.blue; c.beginPath(); c.moveTo(0, 0); c.lineTo(w * 0.5, h / 2); c.lineTo(0, h); c.closePath(); c.fill(); }
  if (extra === 'stars') { c.fillStyle = C.paper; const r = h * 0.32, q = Math.max(1.5, h * 0.07); for (let k = 0; k < 12; k++) { const an = (k / 12) * Math.PI * 2; c.fillRect(w / 2 + Math.cos(an) * r - q / 2, h / 2 + Math.sin(an) * r - q / 2, q, q); } }
  c.restore();
}

export default class Alive extends Hybrid {
  override async init() {
    await super.init();
    const st = (this as any).shots.find((x: any) => x.id === 'street');
    if (st) { // the Eurovision stage is dark; the plate is the Jury Final photo
      st.fg = C.black; st.hl = C.orange; // black reads on the photo's lit haze
      delete st.cap; // drawn under the board, see d_street
    }
    const bi = (this as any).shots.find((x: any) => x.id === 'basicincome');
    if (bi) {
      delete bi.cap; bi.lyric = 'none'; // see d_basicincome: Utopia holds its own line past the next line's first word
    }
    const us = (this as any).shots.find((x: any) => x.id === 'usine');
    if (us) us.p = { ...(us.p ?? {}), gate: false }; // no bars across Lumière's gate here
    // no tweet: the eye opens the film from 0 and the Official Journal page holds to the end
    { const sh = (this as any).shots as any[], cold = sh.findIndex((x) => x.id === 'cold');
      if (cold >= 0) { sh[cold + 1]!.t0 = 0; sh.splice(cold, 1); }
      const mi = sh.findIndex((x) => x.id === 'mill'); // Utopia's gloom holds a beat longer: Nokia cuts in on the beat after its first word
      if (mi > 0) { const tN = this.when('L20'), b = (this.T.beats as number[]).find((x) => x > tN + 0.05); if (b) { sh[mi]!.t0 = b; sh[mi - 1]!.t1 = b; } }
      const fi = sh.findIndex((x) => x.id === 'frank'); // the eye holds through "of AGI"; Frankenstein's creature opens its eye on "in your eyes"
      if (fi > 0) { const tIn = this.when('L1:in') - 0.02; sh[fi]!.t0 = tIn; sh[fi - 1]!.t1 = tIn; }
      const lp = sh.findIndex((x) => x.id === 'loop');
      if (lp > 0) { sh[lp - 1]!.t1 = sh[lp]!.t1; sh.splice(lp, 1); } }
    { const sh = (this as any).shots as any[], gi = sh.findIndex((x) => x.id === 'gallery'), ri = sh.findIndex((x) => x.id === 'ring');
      if (gi > 0 && ri >= 0) {
        // the outro: the GPU stacks, then the EU ring with her in it, then the Official Journal page alone; the cuts sit on
        // the bar lines (downbeats) about 7 and 12.5 s in, where the music turns; the gallery shot gives way
        const cr = sh[gi + 1]!, barNear = (x: number) => (this.T.downbeats as number[]).reduce((a, b) => (Math.abs(b - x) < Math.abs(a - x) ? b : a));
        const t8 = barNear(sh[ri]!.t0 + 7), t13 = barNear(sh[ri]!.t0 + 12.4);
        sh.splice(gi, 1, { ...sh[ri]!, id: 'eucircle', draw: 'eucircle', t0: t8, t1: t13 });
        sh[ri]!.t1 = t8; cr.t0 = t13; cr.p = { ...(cr.p ?? {}), noIdol: true }; // she had her own shot: the end is the paper alone
      } }
    const shots = (this as any).shots as any[], ci = shots.findIndex((x) => x.id === 'cap');
    if (ci >= 0 && shots[ci + 1]?.id === 'medley') { // the cap holds to the end of the section, up to "Post-"
      const t37 = this.ctx.lyrics.lines[36]!.words[0]!.start - 0.02;
      shots[ci]!.t1 = t37; shots[ci + 1]!.t0 = t37;
    }
    const fm = (this as any).shots.find((x: any) => x.id === 'foom');
    if (fm) fm.p = { ...(fm.p ?? {}), capTop: true }; // its lyric slip runs along the bottom
    const db = (this as any).shots.find((x: any) => x.id === 'db');
    if (db) { db.fg = C.black; db.hl = C.yellow; db.lyric = 'none'; db.capL = ['Ibry’s train graph, Paris–Lyon, in É.-J. Marey, La Méthode graphique, 1885. PD.', 'Steeper is faster. A vertical line would be a train that takes no time.', 'DB long-distance punctuality, June–July 2026: 52.6 %.']; }
    await loadImage('animatic/img/marey-ibry-train-graph-1885.jpg'); await loadImage('animatic/img/holbein-utopia-1518.jpg');
    const om = (this as any).shots.find((x: any) => x.id === 'omega');
    if (om) {
      delete om.cap; // its caption goes bottom left, see d_omega
      om.capL = ['Pierre Teilhard de Chardin, French Jesuit, Le Phénomène humain (Seuil, 1955): fig. 3, and p. 286, “le point Oméga”.', 'Written 1938–40; his order would not let him publish it. It came out months after his death.', 'In the EU public domain since 1 January 2026.'];
    }
    const sc = (this as any).shots.find((x: any) => x.id === 'schnabel');
    if (sc) { // L43 is the black box now, not the plague doctor
      sc.draw = 'lovable'; delete sc.img;
      sc.cap = ['BERT (Devlin et al., 2018) was pre-trained by hiding 15 % of the words, [MASK], and guessing them.', 'Lovable, Stockholm: you say what you want, an app comes back. $13.3 bn (Aug 2026).'];
    }
  }

  /** Song time of a key's 'when'. */
  when(k: string | number): number {
    if (typeof k === 'number') return k;
    const m = /^L(\d+)(?::(.+))?$/.exec(k)!;
    const L = this.T.lines[+m[1]! - 1]!;
    if (!m[2]) return L.words[0]!.start;
    const w = L.words.find((x) => x.w.toLowerCase().replace(/[^a-z0-9]/g, '').startsWith(m[2]!));
    if (!w) throw new Error('no word ' + k);
    return w.start;
  }
  /** The camera at t for a shot: each key is reached in 0.45 s from its word (it lands as the word is sung), then
   *  the frame drifts in 2 % until the next key. */
  view(id: string, t: number, d: { u: number; v: number; z: number }) {
    const ks = KEYS[id];
    if (!ks) return { ...d, z: d.z * (1 + 0.03 * clamp((t % 8) / 8)) };
    let cur = { u: ks[0]![1], v: ks[0]![2], z: ks[0]![3] }, prev = cur, t0 = -1e9;
    for (const [w, u, v, z] of ks) {
      const tw = this.when(w);
      if (t + 1 / 120 < tw) break;
      prev = cur; cur = { u, v, z }; t0 = tw;
    }
    const k = ease.inOutCubic(clamp((t - t0) / 0.45));
    const drift = 1 + 0.02 * clamp((t - t0 - 0.45) / 4);
    return { u: prev.u + (cur.u - prev.u) * k, v: prev.v + (cur.v - prev.v) * k, z: (prev.z + (cur.z - prev.z) * k) * drift };
  }
  /** Draw image `id` to fill a box through the camera (the view never shows past the image's edges). */
  film(c: Ctx, id: string, shot: string, t: number, box: [number, number, number, number], treat: Treat, d = { u: 0.5, v: 0.5, z: 1 }) {
    const im = img(`animatic/img/${id}.jpg`); if (!im) return;
    const [bx, by, bw, bh] = box;
    const vw = this.view(shot, t, d);
    const kick = this.ctx.audio.hit('kick', t, 0.08);
    const sc = coverScale(im, bw, bh) * vw.z * (1 + 0.006 * kick);
    const hu = bw / (2 * im.width * sc), hv = bh / (2 * im.height * sc);
    const u = clamp(vw.u, hu, 1 - hu), v = clamp(vw.v, hv, 1 - hv);
    c.save(); c.beginPath(); c.rect(bx, by, bw, bh); c.clip();
    drawImageAt(c, im, bx + bw / 2, by + bh / 2, sc, treat, 0, u, v);
    c.restore();
    // image point (U, V) -> frame px, and image px -> frame px scale, for things pinned to the picture
    return { at: (U: number, V: number): [number, number] => [bx + bw / 2 + (U - u) * im.width * sc, by + bh / 2 + (V - v) * im.height * sc], sc, h: im.height };
  }

  override plate(c: Ctx, s: any, lt: number, dur: number, box: [number, number, number, number], o: { zoom?: number; focus?: [number, number] } = {}) {
    const t = s.t0 + lt;
    c.save(); c.fillStyle = C.paper; c.fillRect(box[0], box[1], box[2], box[3]); c.restore();
    const m = this.film(c, s.img, s.id, t, box, s.treat ?? 'line', { u: o.focus?.[0] ?? 0.5, v: o.focus?.[1] ?? 0.5, z: o.zoom ?? 1 });
    if (m && s.id === 'turk') { c.save(); c.beginPath(); c.rect(box[0], box[1], box[2], box[3]); c.clip(); this.turkAgents(c, t, m); c.restore(); }
  }

  /** Kempelen's Turk (Vienna, 1770) had a person inside; now the one inside is Claude, and the gears are turned by
   *  three more agents. On "boss" the Turk on top gets its tag: the human oversight the AI Act asks for (Art. 14). */
  turkAgents(c: Ctx, t: number, m: { at: (u: number, v: number) => [number, number]; sc: number; h: number }) {
    const sv = this.when('L5:servant'), bo = this.when('L5:boss');
    if (t < sv + 0.12) return;
    const u = m.h * m.sc / 1000; // frame px per 1/1000 of the plate's height
    // Claude, pasted over the hidden operator, at the chess mechanism
    const k = ease.outBack(clamp((t - sv - 0.12) / 0.25));
    const [ox, oy] = m.at(0.645, 0.6);
    const S = 0.62 * u * k, bw = 760, bh = 900;
    if (S > 0.02) {
      c.save(); c.translate(ox, oy); c.scale(S, S); c.rotate(-0.04);
      this.cutout(c, -bw / 2, -260, bw, bh, (g) => idol(g, bw / 2, 260, 1.0, 'reach', t, { ...this.perf(t), suit: C.orange }), 14);
      c.restore();
    }
    // three agents at the gears, each pasted a beat after the last
    [[0.24, 0.66], [0.33, 0.74], [0.27, 0.84]].forEach(([U, V], i) => {
      const at = sv + 0.35 + i * 0.13; if (t < at) return;
      const kk = ease.outBack(clamp((t - at) / 0.2)), [x, y] = m.at(U!, V!), s2 = 0.24 * u * kk;
      if (s2 < 0.02) return;
      c.save(); c.translate(x, y); c.scale(s2, s2);
      this.cutout(c, -380, -200, 760, 900, (g) => idol(g, 380, 260, 1.0, i === 1 ? 'stamp' : 'reach', t, { ...this.perf(t), suit: C.orange, flip: i === 2 }), 14);
      c.restore();
      setFont(c, F.typewriter(700), Math.max(12, 30 * u)); c.fillStyle = C.black;
      c.fillText(`AGENT ${i + 1}`, x - 40 * u, y + 230 * u);
    });
    // the boss on top
    if (t >= bo + 0.05) {
      const [tx, ty] = m.at(0.44, 0.38), kk = ease.outBack(clamp((t - bo - 0.05) / 0.2));
      c.save(); c.translate(tx, ty); c.rotate(-0.08); c.scale(kk, kk);
      sheet(c, -170, -42, 340, 84, 0); setFont(c, F.typewriter(700), 26); c.fillStyle = C.black;
      c.fillText('HUMAN OVERSIGHT', -150, -4); setFont(c, F.typewriter(400), 20); c.fillText('AI Act, Art. 14', -150, 26);
      c.fillStyle = C.orange; c.beginPath(); c.arc(-150, -30, 8, 0, Math.PI * 2); c.fill();
      c.restore();
    }
  }

  // ------------------------------------------------------------ shots re-filmed
  override d_frank(c: Ctx, s: any, t: number) {
    this.film(c, s.img, 'frank', t, [0, 0, W, H], 'line');
    const eyes = this.when('L1:eyes');
    if (t >= eyes + 0.3) { c.save(); c.globalCompositeOperation = 'multiply'; c.fillStyle = C.yellow; c.beginPath(); c.arc(W / 2, H / 2, 70 + 20 * this.ctx.audio.hit('kick', t, 0.1), 0, Math.PI * 2); c.fill(); c.restore(); }
  }

  override d_bigfish(c: Ctx, s: any, t: number, lt: number) {
    this.film(c, s.img, 'bigfish', t, [0, 0, W, H], 'line');
    // the little fish get their names when the camera pulls back on "alive"
    const al = this.when('L6:alive');
    const tags: [string, number, number][] = [['Silo AI → AMD, 2024', 520, 520], ['Stilla → Meta, 2026', 1180, 610], ['Hugging Face → NVIDIA', 830, 380]];
    tags.forEach(([txt, x, y], i) => {
      const at = al + 0.3 + i * 0.17; if (t < at) return;
      const k = ease.outBack(clamp((t - at) / 0.2));
      c.save(); c.translate(x, y - (1 - k) * 60); captionSlip(c, [txt], 0, 0, { size: 26, rot: (i - 1) * 0.05 }); c.restore();
    });
    if (t >= al + 0.85) stamp(c, '$12,930,300,000', 1300, 250, { k: prog(t, al + 0.85, al + 0.95), size: 80, rot: 0.08 });
  }

  override d_foom(c: Ctx, s: any, t: number, lt: number, dur: number) {
    const fm = this.when('L8:foom'), shake = t >= fm ? Math.exp(-(t - fm) * 6) * 14 : 0;
    c.save(); c.translate(Math.sin(t * 90) * shake, Math.cos(t * 77) * shake);
    this.film(c, s.img, 'foom', t, [-20, -20, W + 40, H + 40], 'photo');
    c.restore();
    // FOOM in Futurist parole in libertà, thrown on the word
    const k = prog(t, fm - 0.02, fm + 0.2, ease.outBack);
    if (k > 0) {
      ['F', 'O', 'O', 'M'].forEach((ch, i) => {
        c.save(); c.translate(120 + i * 250, 700 - i * 40); c.rotate(i % 2 ? 0.18 : -0.12); c.scale(k * (1 + i * 0.25), k * (1 + i * 0.25));
        setFont(c, F.display(100, 900), 360); c.fillStyle = i % 2 ? C.orange : C.black; c.fillText(ch, 0, 0); c.restore();
      });
    }
    const L8 = this.ctx.lyrics.lines[7]!;
    if (t >= L8.words[0]!.start - 0.3) this.slipL(c, L8, t, { y: 1030 });
  }

  override d_icarus(c: Ctx, s: any, t: number) {
    this.film(c, s.img, 'icarus', t, [0, 0, W, H], 'color');
    const tl14 = this.when('L14:the');
    if (t >= tl14 + 0.5) stamp(c, 'SINGULARITY', 520, 300, { k: prog(t, tl14 + 0.5, tl14 + 0.58), size: 70, color: C.orange, rot: -0.1 });
  }

  override d_wanderer(c: Ctx, s: any, t: number) {
    const L = this.ctx.lyrics.lines[44]!, never = this.when('L45:never') - 0.25;
    if (t < never) {
      this.film(c, s.img, 'wanderer', t, [0, 0, W, H], 'color');
      // on "Draghi" a paper cut-out of the idol, from behind, slides up at the left edge: a visitor looking at the
      // Wanderer looking at the fog
      const tD = this.when('L45:draghi');
      if (t >= tD - 0.12) {
        const S = 1.6, bw = 640, bh = 900, hx = 170, hy = 560, rise = (1 - ease.outCubic(prog(t, tD - 0.12, tD))) * 700;
        c.save(); c.translate(hx, H); c.rotate(0.04); c.translate(-hx, -H);
        this.cutout(c, hx - bw / 2, hy - 170 + rise, bw, bh, (k) => idol(k, bw / 2, 170 + 118 * S, S, 'back', t));
        c.restore();
      }
      this.slipL(c, L, t);
    } else {
      // Eva-style L card: WE'LL vertical, NEVER KNOW from its foot, each word on its sung frame
      c.fillStyle = C.black; c.fillRect(0, 0, W, H);
      c.fillStyle = C.paper; setFont(c, F.display(62.5, 900), 230);
      c.save(); c.translate(150, 90); c.rotate(Math.PI / 2); c.fillText('WE’LL', 0, 0); c.restore();
      if (t >= this.when('L45:never') - 1 / 120) c.fillText('NEVER', 300, 640);
      if (t >= this.when('L45:know') - 1 / 120) c.fillText('KNOW.', 300, 880);
    }
  }

  override d_bureau(c: Ctx, s: any, t: number) {
    // the queue moves on every bar while she waits: NOW SERVING counts up from 9, her ticket says 812; the camera
    // closes in on her as she pleads
    c.fillStyle = ink({ blue: 0.18 }); c.fillRect(0, 0, W, H);
    const pl = this.when('L6:please'), push = 1 + 0.05 * prog(t, s.t0, pl) + 0.16 * ease.inOutCubic(prog(t, pl - 0.15, pl + 0.35));
    c.save(); c.translate(560, 360); c.scale(push, push); c.translate(-560, -360);
    idolBust(c, 560, 430, 3.4, t, this.perf(t));
    c.restore();
    const au = this.ctx.audio, bar = Math.max(0, Math.floor(au.barAt(t)) - Math.floor(au.barAt(s.t0)));
    const since = au.timeOfBeat(Math.floor(au.beatAt(t) / 4) * 4);
    flapBoard(c, 1240, 120, ['NOW SERVING', `      ${String(9 + bar).padStart(4, '0')}`], t, { cell: 42, cols: 11, since: bar ? since : -9 });
    const shake = Math.exp(-((t - since) % 2) * 8) * 4;
    c.save(); c.translate(Math.sin(t * 60) * shake, 0);
    sheet(c, 1330, 520, 260, 170, -0.05); setFont(c, F.sign(700), 30); c.fillStyle = C.black; c.fillText('YOUR NUMBER', 1360, 580); setFont(c, F.sign(700), 80); c.fillText('0812', 1370, 670);
    c.restore();
    captionSlip(c, ['Output withheld pending human oversight (Art. 14).', `Position 812 in queue. Now serving ${9 + bar}.`], 1150, 800, { size: 20 });
  }

  /** Käärijä as he moved in the Liverpool final (studied frame by frame from the broadcast): the mic always at his
   *  mouth in one hand; the other arm in the chorus's pirate swing, elbow out at shoulder height and the hand hanging
   *  loose, swinging with the torso side to side, the extremes on the beats; knees wide in a crouch that dips on every
   *  beat. The bolero is two lime puffs bigger than his head and a spiked collar; spiked black leather trousers. Feet
   *  at (x, y). `up` 0..1: the free arm points to the sky (the people's vote); `down`: the mic comes down (the juries'). */
  kaarija(c: Ctx, x: number, y: number, s: number, t: number, up = 0, down = 0) {
    const b = this.ctx.audio.beatAt(t), ph = b - Math.floor(b), p = Math.cos(b * Math.PI), live = 1 - down;
    const sing = clamp(this.vocalOpen(t));
    const cr = (0.55 + 0.35 * (1 - ph) * (1 - ph)) * live * (1 - 0.5 * up) + 0.1 * down; // the crouch, dipping on the beat
    const sway = 0.13 * p * live * (1 - up), hipY = -185 + 55 * cr, hx = -18 * p * live;
    const K = C.black, mix = (u: number[], v: number[], k: number) => [u[0]! + (v[0]! - u[0]!) * k, u[1]! + (v[1]! - u[1]!) * k];
    const blend = (n: number[], u: number[], d: number[]) => mix(mix(n, u, up), d, down);
    const seg = (pts: number[][], w: number, col: string) => { c.strokeStyle = col; c.lineWidth = w; c.beginPath(); c.moveTo(pts[0]![0]!, pts[0]![1]!); for (const q of pts.slice(1)) c.lineTo(q[0]!, q[1]!); c.stroke(); };
    const limb = (pts: number[][], w: number) => { seg(pts, w + 8, K); seg(pts, w, C.paper); };
    c.save(); c.translate(x, y); c.scale(s, s); c.lineJoin = 'round'; c.lineCap = 'round';
    // legs: knees out wide, black leather spiked down the outside seam, black boots on lime soles
    for (const sd of [-1, 1]) {
      const hip = [sd * 16 + hx, hipY], knee = [sd * (44 + 46 * cr), (hipY - 26) / 2 + 4], ank = [sd * (40 + 10 * cr), -28];
      seg([hip, knee, ank], 38, K);
      c.fillStyle = K;
      for (const [u, v] of [[hip, knee], [knee, ank]] as number[][][]) for (const k of [0.3, 0.7]) {
        const q = mix(u!, v!, k); c.beginPath(); c.moveTo(q[0]! + sd * 12, q[1]! - 9); c.lineTo(q[0]! + sd * 34, q[1]!); c.lineTo(q[0]! + sd * 12, q[1]! + 9); c.fill();
      }
      c.beginPath(); c.moveTo(ank[0]! - 22, -34); c.lineTo(ank[0]! + 22, -34); c.lineTo(ank[0]! + 24 + sd * 18, -6); c.lineTo(ank[0]! - 24 + sd * 4, -6); c.closePath(); c.fill();
      c.fillStyle = LIME; c.fillRect(Math.min(ank[0]! - 24 + sd * 4, ank[0]! + 24 + sd * 18) , -8, 52, 8);
    }
    // the upper body swings from the hips
    c.save(); c.translate(hx, hipY); c.rotate(sway);
    c.fillStyle = C.paper; c.beginPath(); c.moveTo(-46, -125); c.lineTo(46, -125); c.lineTo(38, 6); c.lineTo(-38, 6); c.closePath(); c.fill(); c.strokeStyle = K; c.lineWidth = 4; c.stroke();
    c.lineWidth = 3; c.beginPath(); c.moveTo(-34, -78); c.quadraticCurveTo(-16, -70, -4, -80); c.moveTo(34, -78); c.quadraticCurveTo(16, -70, 4, -80); c.moveTo(0, -40); c.lineTo(0, -34); c.stroke();
    c.fillStyle = K; c.fillRect(-42, -4, 84, 14); // waistband
    // the free arm: the pirate swing; to the sky for the people; hanging for the juries
    const FS = [-52, -110], FE = blend([-152 + 10 * p, -122 - 8 * p], [-96, -205], [-62, -40]), FH = blend([FE[0]! + 30 * p - 4, FE[1]! + 84], [-122, -290], [-66, 22]);
    limb([mix(FS, FE, 0.6), FE, FH], 22);
    const cuff = mix(FH, FE, 0.22); c.fillStyle = K; c.beginPath(); c.arc(cuff[0]!, cuff[1]!, 15, 0, Math.PI * 2); c.fill(); // the spiked cuff
    c.fillStyle = C.paper; c.beginPath(); c.arc(FH[0]!, FH[1]!, 13, 0, Math.PI * 2); c.fill(); c.strokeStyle = K; c.lineWidth = 4; c.stroke();
    // the mic arm: elbow out, the mic at his mouth; lowered for the juries
    const MS = [52, -110], ME = blend([98, -62], [98, -62], [80, -30]), MH = blend([24, -140], [24, -140], [46, -36]);
    // the puffs, over the shoulders and upper arms
    for (const [S, E] of [[FS, FE], [MS, ME]] as number[][][]) {
      const m = mix(S!, E!, 0.38), an = Math.atan2(E![1]! - S![1]!, E![0]! - S![0]!);
      c.save(); c.translate(m[0]!, m[1]!); c.rotate(an); c.fillStyle = LIME; c.strokeStyle = K; c.lineWidth = 4;
      for (const [ox, oy, rx, ry] of [[-14, -10, 44, 40], [16, 8, 42, 38], [-4, 14, 40, 34]]) { c.beginPath(); c.ellipse(ox!, oy!, rx!, ry!, 0, 0, Math.PI * 2); c.fill(); c.stroke(); }
      c.lineWidth = 2.5; c.beginPath(); c.moveTo(-30, -26); c.quadraticCurveTo(-8, -6, -26, 22); c.moveTo(8, -24); c.quadraticCurveTo(30, 0, 12, 32); c.stroke();
      c.restore();
    }
    // the bolero's fronts and the spiked collar
    c.fillStyle = LIME; c.strokeStyle = K; c.lineWidth = 4;
    for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(sd * 16, -132); c.lineTo(sd * 50, -130); c.lineTo(sd * 46, -76); c.lineTo(sd * 22, -88); c.closePath(); c.fill(); c.stroke(); }
    c.fillStyle = K; for (let i = 0; i < 9; i++) { const an = Math.PI * (1.08 + (i / 8) * 0.84), r0 = 34, r1 = 54; c.beginPath(); c.moveTo(Math.cos(an - 0.09) * r0, -138 + Math.sin(an - 0.09) * r0 * 0.4); c.lineTo(Math.cos(an) * r1, -138 + Math.sin(an) * r1 * 0.45); c.lineTo(Math.cos(an + 0.09) * r0, -138 + Math.sin(an + 0.09) * r0 * 0.4); c.fill(); }
    c.fillStyle = LIME; c.beginPath(); c.ellipse(0, -136, 40, 15, 0, 0, Math.PI * 2); c.fill(); c.stroke();
    // head: the fringe combed forward, eyes, a shout on the vocal; bowed for the juries
    c.save(); c.translate(0, -150); c.rotate(0.18 * down); c.translate(0, 150);
    c.fillStyle = C.paper; c.beginPath(); c.ellipse(0, -187, 34, 42, 0, 0, Math.PI * 2); c.fill(); c.stroke();
    c.fillStyle = K; c.beginPath(); c.moveTo(-38, -191); c.quadraticCurveTo(-40, -239, 0, -237); c.quadraticCurveTo(40, -239, 38, -191);
    for (let i = 0; i <= 8; i++) c.lineTo(36 - i * 9, -197 + (i % 2) * 6); c.closePath(); c.fill();
    c.beginPath(); c.arc(-12, -181, 3.5, 0, Math.PI * 2); c.arc(12, -181, 3.5, 0, Math.PI * 2); c.fill();
    c.beginPath(); c.ellipse(-2, -159, 10, 3 + 9 * sing * live, 0, 0, Math.PI * 2); c.fillStyle = down > 0.5 ? K : C.orange; c.fill(); c.lineWidth = 3; c.stroke();
    c.restore();
    // the mic arm in front: forearm, fist, the mic
    limb([mix(MS, ME, 0.6), ME, MH], 22);
    const mh = blend([10, -160], [10, -160], [36, -62]), me = [MH[0]! + (MH[0]! - mh[0]!) * 1.3, MH[1]! + (MH[1]! - mh[1]!) * 1.3];
    seg([mh, me], 12, K); c.fillStyle = K; c.beginPath(); c.arc(mh[0]!, mh[1]!, 12, 0, Math.PI * 2); c.fill();
    c.fillStyle = C.paper; c.beginPath(); c.arc(MH[0]!, MH[1]!, 13, 0, Math.PI * 2); c.fill(); c.strokeStyle = K; c.lineWidth = 4; c.stroke();
    c.restore();
    c.restore();
  }

  /** a backing dancer in the chorus move: both elbows out at the shoulders, the hands hanging, swinging side to side
   *  in a wide crouch with him (the broadcast's dancers wore neon pink; the nearest these four inks get) */
  dancer(c: Ctx, x: number, y: number, s: number, t: number, flip = 1) {
    const b = this.ctx.audio.beatAt(t), ph = b - Math.floor(b), p = Math.cos(b * Math.PI) * flip;
    const cr = 0.5 + 0.35 * (1 - ph) * (1 - ph), hipY = -185 + 55 * cr, PINK = ink({ orange: 0.85 }), K = C.black;
    c.save(); c.translate(x, y); c.scale(s, s); c.lineJoin = 'round'; c.lineCap = 'round';
    const seg = (pts: number[][], w: number, col: string) => { c.strokeStyle = col; c.lineWidth = w; c.beginPath(); c.moveTo(pts[0]![0]!, pts[0]![1]!); for (const q of pts.slice(1)) c.lineTo(q[0]!, q[1]!); c.stroke(); };
    for (const sd of [-1, 1]) seg([[sd * 16, hipY], [sd * (46 + 44 * cr), (hipY - 26) / 2], [sd * (46 + 12 * cr), -10]], 46, PINK);
    c.translate(-16 * p, hipY); c.rotate(0.15 * p);
    c.fillStyle = PINK; c.fillRect(-40, -125, 80, 130);
    for (const sd of [-1, 1]) { const E = [sd * 120 + 12 * p, -118 - 10 * p * sd], H = [E[0]! + 26 * p, E[1]! + 74]; seg([[sd * 40, -112], E, H], 26, PINK); c.fillStyle = C.paper; c.beginPath(); c.arc(H[0]!, H[1]!, 11, 0, Math.PI * 2); c.fill(); }
    c.fillStyle = C.paper; c.beginPath(); c.ellipse(0, -172, 30, 37, 0, 0, Math.PI * 2); c.fill();
    c.fillStyle = K; c.beginPath(); c.ellipse(0, -196, 32, 18, 0, Math.PI, 0); c.fill(); c.beginPath(); c.arc(0, -222, 14, 0, Math.PI * 2); c.fill();
    c.restore();
  }

  /** L12, with Eurovision eyes: the grand final, Liverpool, 13 May 2023. Käärijä's Cha Cha Cha had the people:
   *  the televote's 376 was the most of the night, first of 26. The juries gave it 150 and it finished second. The
   *  people's count runs at the world's frame rate, the juries' on Europe's six; the system wins. */
  override d_street(c: Ctx, s: any, t: number, lt: number) {
    const au = this.ctx.audio, ev = this.when('L12:eurovision'), ey = this.when('L12:eyes');
    const pe = ey + 0.4, ju = ey + 1.2, sys = ey + 2.4;
    const up = clamp((t - pe) / 0.25) * (1 - clamp((t - ju) / 0.3)), down = 0; // he keeps dancing through the juries' count
    const bp = au.beatAt(t), ph = bp - Math.floor(bp), kick = au.hit('kick', t, 0.1), snare = au.hit('snare', t, 0.08);
    // the camera: the whole arena, creeping in through the line; in on him for the people's vote, back out for the juries
    const push = 1 + 0.04 * clamp((t - ev) / 3) + 0.12 * ease.inOutCubic(clamp((t - pe + 0.3) / 0.5)) * (1 - ease.inOutCubic(clamp((t - ju) / 0.6)));
    const SX = 680; // the stage's axis
    c.save(); c.translate(SX, 600); c.scale(push, push); c.translate(-SX, -600);
    c.fillStyle = ink({ black: 0.9 }); c.fillRect(-200, -200, W + 400, H + 400);
    // the stands, tier on tier up into the dark, phone lights twinkling
    const tw = Math.floor(t * 8);
    for (let y = 120, r = 0; y < 640; y += 15, r++) for (let x = (r % 2) * 7; x < W; x += 14) {
      c.fillStyle = hash(x, y) > 0.92 && hash(x, y, tw) > 0.45 ? C.paper : ink({ black: 0.7 });
      c.fillRect(x, y, 7, 7);
    }
    for (let i = 0; i < 18; i++) { // beams from the rig and from the floor, crossing, sweeping on the beat, flaring on the snare
      const top = i % 2 === 0, x0 = -40 + i * 110, a = Math.sin(bp * Math.PI * 0.5 + i * 0.9) * 0.45, w = 40 + 60 * snare;
      const y0 = top ? 70 : 640, y1 = top ? H + 60 : -60, dx = Math.sin(a) * 1300;
      c.save(); c.globalAlpha = 0.16 + 0.12 * snare; c.fillStyle = C.paper;
      c.beginPath(); c.moveTo(x0 - 6, y0); c.lineTo(x0 + 6, y0); c.lineTo(x0 + dx + w, y1); c.lineTo(x0 + dx - w, y1); c.closePath(); c.fill(); c.restore();
    }
    // the lasers: a green fan from the rig's centre, turning on the beat (the chorus's look in Liverpool)
    c.save(); c.globalAlpha = 0.18 + 0.2 * snare; c.strokeStyle = C.paper; c.lineWidth = 3;
    for (let i = 0; i < 22; i++) { const an = Math.PI * (0.08 + (i / 21) * 0.84) + Math.sin(bp * Math.PI * 0.5) * 0.12; c.beginPath(); c.moveTo(SX, 60); c.lineTo(SX + Math.cos(an) * 2200, 60 + Math.sin(an) * 2200); c.stroke(); }
    c.restore();
    c.fillStyle = C.black; c.fillRect(-60, 40, W + 120, 34); // the truss
    for (let i = 0; i < 28; i++) { c.fillStyle = (i + Math.floor(bp * 2)) % 3 ? C.paper : ink({ black: 0.45 }); c.beginPath(); c.arc(20 + i * 70, 57, 11, 0, Math.PI * 2); c.fill(); }
    // the LED wall: CHA CHA CHA a word per beat; from "eyes" the broadcast's close-up of him, ten metres tall
    const lx = 230, ly = 110, lw = 900, lh = 430;
    c.fillStyle = C.black; c.fillRect(lx, ly, lw, lh);
    c.save(); c.beginPath(); c.rect(lx, ly, lw, lh); c.clip();
    if (t < ey) {
      setFont(c, arch(1, 0.9), 300); const cw = c.measureText('CHA ').width;
      for (let k = -1; k < 4; k++) {
        const x = lx + 40 + (k - ph) * cw;
        c.fillStyle = k === 1 ? C.paper : ink({ black: 0.62 });
        c.fillText('CHA', x, ly + lh / 2 + 108);
      }
    } else { c.fillStyle = ink({ black: 0.35 }); c.fillRect(lx, ly, lw, lh); this.kaarija(c, lx + lw / 2 + 150, ly + 1450, 3.1, t, up, down); }
    c.restore();
    c.fillStyle = C.black; for (let y = ly; y < ly + lh; y += 9) c.fillRect(lx, y, lw, 3); for (let x = lx; x < lx + lw; x += 9) c.fillRect(x, ly, 3, lh); // the panels' grid
    // the stage: the deck under the wall and a runway out into the crowd, its edge lights chasing on the beat
    const FLOOR = ink({ black: 0.3 });
    c.fillStyle = FLOOR; c.fillRect(150, 540, 1060, 50); c.fillStyle = ink({ black: 0.55 }); c.fillRect(150, 590, 1060, 10);
    c.fillStyle = FLOOR; c.beginPath(); c.moveTo(SX - 70, 600); c.lineTo(SX + 70, 600); c.lineTo(SX + 460, H); c.lineTo(SX - 460, H); c.closePath(); c.fill();
    for (let k = 0; k < 14; k++) {
      const d = k / 13, y = 600 + d * (H - 600), hw = 70 + d * 390;
      c.fillStyle = (k + 40 - Math.floor(bp * 4)) % 4 === 0 ? C.paper : ink({ black: 0.5 });
      for (const sx of [-1, 1]) c.fillRect(SX + sx * hw - 5 - 4 * d, y, 10 + 8 * d, 6 + 6 * d);
    }
    // pyro on the kicks along the deck
    if (kick > 0.25) for (const fx of [190, 400, 960, 1170]) {
      const hgt = 420 * kick;
      for (let j = 0; j < 3; j++) { c.fillStyle = j === 0 ? C.orange : j === 1 ? ink({ orange: 0.5 }) : C.paper; c.beginPath(); c.moveTo(fx - 44 + j * 16, 545); c.lineTo(fx + (j - 1) * 9, 545 - hgt * (1 - j * 0.28)); c.lineTo(fx + 44 - j * 16, 545); c.closePath(); c.fill(); }
    }
    // his four dancers on the deck, in the chorus move
    [-400, -230, 230, 400].forEach((dx, i) => this.dancer(c, SX + dx, 588, 0.5, t, i % 2 ? -1 : 1));
    // the crowd in perspective, both sides of the runway: raised arms, phones, the flags of the member states, jumping on the beat (higher for the people)
    const cheer = 1 + 1.5 * up, ROWS = 11;
    const crowd = (from: number, to: number) => { c.save(); c.beginPath(); c.rect(-200, -200, W + 400, H + 400); c.moveTo(SX - 70, 600); c.lineTo(SX + 70, 600); c.lineTo(SX + 470, H + 10); c.lineTo(SX - 470, H + 10); c.closePath(); c.clip('evenodd'); // never on the runway
      for (let r = from; r < to; r++) {
      const d = r / (ROWS - 1), rad = 6 + 22 * d * d, y0 = 625 + 470 * Math.pow(d, 1.3), gap = rad * 2.9, hw = 70 + ((y0 - 600) / (H - 600)) * 390;
      for (let i = 0, x = -gap + (r % 2) * gap / 2; x < W + gap; i++, x += gap) {
        if (Math.abs(x - SX) < hw + rad * 1.5) continue;
        const k = hash(i, r, 7), y = y0 - Math.max(0, Math.sin((ph + hash(i, r, 3)) * Math.PI * 2)) * rad * 0.6 * cheer;
        if (k > 0.5) {
          const ax = x + rad * 1.2, ay = y - rad * 3.6;
          c.strokeStyle = C.black; c.lineWidth = rad * 0.5; c.beginPath(); c.moveTo(x + rad * 0.7, y); c.lineTo(ax, ay); c.stroke();
          if (k > 0.74) {
            const fw = rad * 3.8, fh = rad * 2.5, n = hash(i, r, 9) < 0.3 ? FLAGS.length - 1 : Math.floor(hash(i, r, 11) * (FLAGS.length - 1));
            flag(c, n, ax, ay - fh - rad * 0.8, fw, fh, Math.sin(t * 9 + i + r) * rad * 0.35);
            c.lineWidth = Math.max(2, rad * 0.15); c.beginPath(); c.moveTo(ax, ay - fh - rad * 0.8); c.lineTo(ax, ay); c.stroke();
          } else if (rad < 12) { if (hash(i, r, tw) > 0.3) { c.fillStyle = C.paper; c.fillRect(ax - 2, ay - 4, 4, 5); } }
          else { c.fillStyle = C.black; c.fillRect(ax - rad * 0.45, ay - rad * 1.6, rad * 0.9, rad * 1.6); c.fillStyle = C.paper; c.fillRect(ax - rad * 0.33, ay - rad * 1.48, rad * 0.66, rad * 1.2); }
        }
        c.fillStyle = C.black; c.beginPath(); c.arc(x, y - rad * 0.8, rad, 0, Math.PI * 2); c.fill(); c.fillRect(x - rad * 1.5, y, rad * 3, rad * 5);
      }
    } c.restore(); };
    crowd(0, 4);
    // the spot on him, opening on "eyes"
    const spot = ease.outCubic(clamp((t - ey) / 0.3));
    if (spot > 0) { c.save(); c.globalAlpha = 0.3 * spot; c.fillStyle = C.paper; c.beginPath(); c.moveTo(SX - 40, 60); c.lineTo(SX + 40, 60); c.lineTo(SX + 190, 770); c.lineTo(SX - 190, 770); c.closePath(); c.fill(); c.restore(); }
    // Käärijä, small on the runway against the wall
    this.kaarija(c, SX, 760, 0.8, t, up, down);
    crowd(4, ROWS);
    // confetti for the people's vote
    if (t >= pe) {
      const ct = t - pe;
      for (let i = 0; i < 220; i++) {
        const x = hash(i, 1) * W, y = -40 + ct * (380 + hash(i, 2) * 300) - hash(i, 3) * 500, r = t * (4 + hash(i, 4) * 6);
        if (y < -30 || y > H) continue;
        c.save(); c.translate(x + Math.sin(t * 3 + i) * 30, y); c.rotate(r);
        c.fillStyle = [LIME, C.paper, C.orange][i % 3]!; c.fillRect(-7, -4, 14, 8); c.restore();
      }
    }
    c.restore();
    if (t - s.t0 > 0.25) captionSlip(c, ['Eurovision 2023, Liverpool, grand final, 13 May:', 'Käärijä, Cha Cha Cha (Finland). Televote 376,', 'the most of the night; juries 150; result 2nd.', 'Drawn after the broadcast.'], 1290, 790, { size: 17 });
    // the board: the people against the juries (on the arena's screen, outside the push)
    if (t >= ev - 1 / 120) {
      const x = 1290, y = 90, k = ease.outCubic(clamp((t - ev) / 0.3));
      c.save(); c.translate((1 - k) * 700, 0);
      c.fillStyle = C.black; c.fillRect(x, y, 580, 620); c.strokeStyle = C.yellow; c.lineWidth = 6; c.strokeRect(x, y, 580, 620);
      setFont(c, F.sign(700), 26); c.fillStyle = C.yellow; c.fillText('GRAND FINAL · LIVERPOOL · 13 MAY 2023', x + 26, y + 44);
      setFont(c, F.sign(700), 44); c.fillStyle = C.paper; c.fillText('KÄÄRIJÄ · CHA CHA CHA', x + 26, y + 100);
      const people = Math.round(376 * ease.outCubic(clamp((t - ev - 0.1) / (pe - ev - 0.1))));
      const juries = Math.round(150 * clamp((step(t, 6) - ju) / 0.6)); // the juries count on Europe's clock
      const row = (ry: number, label: string, sub: string, n: number, bg: string) => {
        c.fillStyle = bg; c.fillRect(x + 26, ry, 528, 150);
        setFont(c, F.sign(700), 54); c.fillStyle = C.black; c.fillText(label, x + 50, ry + 72);
        setFont(c, F.typewriter(700), 20); c.fillText(sub, x + 52, ry + 112);
        c.fillStyle = C.black; c.fillRect(x + 370, ry + 18, 168, 114);
        setFont(c, F.sign(700), 92); c.fillStyle = C.yellow; c.textAlign = 'right'; c.fillText(String(n), x + 526, ry + 108); c.textAlign = 'left';
      };
      row(y + 140, 'THE PEOPLE', 'televote · 1st of 26', people, LIME);
      if (t >= ju - 0.2) row(y + 310, 'THE JURIES', 'professional juries', juries, C.paper);
      if (t >= sys - 0.3) { setFont(c, F.sign(700), 52); c.fillStyle = C.paper; c.fillText('PEOPLE 0 · SYSTEM 1', x + 26, y + 540); }
      c.restore();
    }
    if (t >= sys) stamp(c, 'THE SYSTEM WINS', 1580, 694, { k: prog(t, sys, sys + 0.1), size: 64, color: C.orange, rot: -0.06 }); // under the final score
  }

  /** L35, "Just transformers all the way!": the unicorn factory. The transformer (Vaswani et al., 2017) is the
   *  machine; through the held "transformers" it turns out Europe's AI companies faster and faster down the belt, each a
   *  unicorn off the Cloisters tapestry with its name and valuation; the gauge climbs toward the EU's 2030 target
   *  (at least double the unicorns); one of them takes off abroad (Draghi: close to 30 %, 2008–21). */
  override d_unicorns(c: Ctx, s: any, t: number) {
    const au = this.ctx.audio, tT = this.when('L35:transformers'), tW = this.when('L35:way');
    c.fillStyle = C.black; c.fillRect(0, 0, W, H);
    const kick = au.hit('kick', t, 0.08);
    // the machine: the transformer, drawn as its paper's figure, boxes lighting in turn as it runs
    const mx = 1450, my = 60, mw = 420, mh = 660;
    sheet(c, mx, my, mw, mh, 0.01);
    setFont(c, F.sign(700), 30); c.fillStyle = C.black; c.fillText('ATTENTION IS ALL YOU NEED', mx + 26, my + 48);
    setFont(c, F.typewriter(700), 16); c.fillText('VASWANI ET AL. · 2017 · THE TRANSFORMER', mx + 26, my + 74);
    const boxes = ['OUTPUT PROBABILITIES', 'SOFTMAX', 'LINEAR', 'ADD & NORM', 'FEED FORWARD', 'ADD & NORM', 'MULTI-HEAD ATTENTION', 'POSITIONAL ENCODING', 'INPUT EMBEDDING'];
    const lit = t >= tT ? Math.floor((t - tT) / S16) % boxes.length : -1;
    boxes.forEach((b, i) => {
      const by = my + 100 + i * 58, bx = mx + 60 + (i >= 3 && i <= 6 ? 20 : 0), bw = mw - 120 - (i >= 3 && i <= 6 ? 40 : 0);
      c.fillStyle = boxes.length - 1 - i === lit ? C.yellow : i >= 3 && i <= 6 ? ink({ orange: 0.25 }) : ink({ blue: 0.15 });
      c.fillRect(bx, by, bw, 40); c.strokeStyle = C.black; c.lineWidth = 2.5; c.strokeRect(bx, by, bw, 40);
      setFont(c, F.sign(700), 20); c.fillStyle = C.black; c.textAlign = 'center'; c.fillText(b, bx + bw / 2, by + 27); c.textAlign = 'left';
      if (i < boxes.length - 1) { c.beginPath(); c.moveTo(mx + mw / 2, by + 40); c.lineTo(mx + mw / 2, by + 58); c.stroke(); }
    });
    setFont(c, F.sign(700), 34); c.fillStyle = C.black; c.fillText('N×', mx + 22, my + 100 + 4.6 * 58);
    // one company per beat: born at the machine's mouth on the beat, the belt indexing one slot left on each next beat
    const B = (this.T.beats as number[]).filter((b) => b >= s.t0 && b < s.t1).slice(0, 7), SW = 250;
    const step = (b: number) => ease.outCubic(clamp((t - b) / 0.16));
    const adv = B.reduce((a, b) => a + step(b), 0), made = B.filter((b) => b <= t).length;
    // the gauge on top of the machine: toward the 2030 target
    c.fillStyle = C.black; c.fillRect(mx, my + mh + 10, mw, 70);
    setFont(c, F.sign(700), 22); c.fillStyle = C.yellow; c.fillText('EU UNICORNS · DIGITAL DECADE 2030: × 2', mx + 18, my + mh + 40);
    c.fillStyle = ink({ black: 0.6 }); c.fillRect(mx + 18, my + mh + 52, mw - 36, 16);
    c.fillStyle = C.orange; c.fillRect(mx + 18, my + mh + 52, (mw - 36) * (0.5 + 0.5 * made / 7), 16);
    // the belt, from the machine's mouth to the left edge, moving one slot per beat
    const by = 800;
    c.fillStyle = ink({ black: 0.5, blue: 0.2 }); c.fillRect(40, by, mx + 20 - 40, 34);
    const off = (adv * SW) % 60;
    c.fillStyle = C.black; for (let x = 40 - off; x < mx + 20; x += 60) c.fillRect(x, by + 4, 26, 26);
    for (const rx of [60, mx]) { c.save(); c.translate(rx, by + 60); c.rotate(-adv * SW / 26); c.fillStyle = C.paper; c.beginPath(); c.arc(0, 0, 26, 0, Math.PI * 2); c.fill(); c.fillStyle = C.black; c.fillRect(-26, -3, 52, 6); c.restore(); }
    // the unicorns
    const CO: [string, string][] = [['MISTRAL AI', 'PARIS · €21 BN'], ['ELEVENLABS', 'LONDON · $22 BN'], ['LOVABLE', 'STOCKHOLM · $13.3 BN'],
      ['HELSING', 'MUNICH · €12 BN'], ['BLACK FOREST LABS', 'FREIBURG · $3.25 BN'], ['N8N', 'BERLIN · $2.5 BN'], ['STEALTH', 'NEW · 2026 · NEXT?']];
    const im = img('animatic/img/unicorn-in-garden.jpg');
    CO.forEach(([name, sub], i) => {
      const tb = B[i]; if (tb === undefined || t < tb) return;
      const pop = ease.outBack(clamp((t - tb) / 0.14));
      const stealth = name === 'STEALTH', moved = B.slice(i + 1).reduce((a, b) => a + step(b), 0);
      let x = stealth ? mx - 300 : mx - 250 - SW * moved, y = stealth ? by - 300 : by - 236; // the next one stays at the mouth, lifted
      const abroad = i === 2 && t > tW; // one of them leaves
      if (abroad) { const a = t - tW; x -= 0; y -= a * a * 900 + a * 200; }
      if (x < -260) return;
      c.save(); c.translate(x + 115, y + 110); c.scale(pop * (stealth ? 1.3 : 1), pop * (stealth ? 1.3 : 1)); c.rotate((i % 2 ? -1 : 1) * 0.03 + (abroad ? -0.3 * (t - tW) : 0)); c.translate(-115, -110);
      if (stealth) { c.fillStyle = C.yellow; c.fillRect(-10, -10, 250, 246); }
      sheet(c, 0, 0, 230, 226, 0);
      if (im) { c.save(); c.beginPath(); c.rect(8, 8, 214, 158); c.clip(); drawImageAt(c, im, 115, 87, (214 / im.width) * 1.35, 'color', 0, 0.5, 0.5); c.restore(); }
      if (name === 'STEALTH') { // the next one: still under wraps, its picture redacted, a question mark in yellow
        c.fillStyle = C.black; c.fillRect(8, 8, 214, 158);
        setFont(c, F.display(100, 900), 130); c.fillStyle = C.yellow; c.textAlign = 'center'; c.fillText('?', 115, 140); c.textAlign = 'left';
      }
      setFont(c, F.sign(700), name.length > 12 ? 22 : 28); c.fillStyle = C.black; c.fillText(name, 10, 194);
      setFont(c, F.typewriter(700), 15); c.fillText(sub, 10, 216);
      c.restore();
      if (abroad && t - tW > 0.15) { setFont(c, F.typewriter(700), 20); c.fillStyle = C.paper; c.fillText('→ HQ ABROAD (≈30 %, DRAGHI)', x - 40, y - 20); }
    });
    // the machine shakes on the kick while it works
    if (t >= tT && t < tW + 0.4) { c.fillStyle = C.orange; c.beginPath(); c.arc(mx + mw - 30, my + 30, 10 + 8 * kick, 0, Math.PI * 2); c.fill(); }
    if (t >= tW) stamp(c, 'THE NEXT ONE', mx - 160, by - 300, { k: prog(t, tW, tW + 0.1), size: 60, color: C.orange, rot: -0.1, sub: 'MADE IN EUROPE' });
  }

  /** L43, "From masked pre-training days": the black box. Prompts are thrown in on the eighth notes and finished apps
   *  come back out, but what happens inside stays masked; from "masked" on, the prompts arrive with a word [MASK]ed. */
  d_lovable(c: Ctx, s: any, t: number) {
    const tm = this.when('L43:masked'), E8 = 2 * S16, kick = this.ctx.audio.hit('kick', t, 0.08);
    const bx = 960, by = 230, bw = 560, bh = 590, slot = [bx + bw / 2, by + 8];
    const P = ['make me a CRM', 'a booking app for my café', 'fix the login', 'make it pop', 'add payments', 'dark mode pls', 'a game for my kid', 'SaaS by Friday'];
    const M = ['make me a [MASK]', 'a [MASK] for my café', 'fix the [MASK]', 'make it [MASK]', 'add [MASK]', '[MASK] mode pls', 'a [MASK] for my kid', '[MASK] by Friday'];
    const A = ['crm', 'cafe-booking', 'login', 'pop', 'pay', 'dark', 'kid-game', 'friday'];
    const FLY = 0.45, OUT = 0.18;
    const thrown = P.map((_, i) => s.t0 + 0.02 + i * E8);
    // the answers, coming back out of the box's side and stacking down the right edge
    thrown.forEach((ti, i) => {
      const te = ti + FLY + OUT; if (t < te) return;
      const k = ease.outCubic(clamp((t - te) / 0.22)), x = bx + bw - 260 + k * (1570 - (bx + bw - 260)), y = by + 380 + k * (60 + i * 104 - by - 380);
      c.save(); c.translate(x, y); c.rotate((1 - k) * 0.2 + (i % 2 ? 0.02 : -0.02));
      sheet(c, 0, 0, 320, 92, 0);
      c.fillStyle = C.black; c.fillRect(0, 0, 320, 18); c.fillStyle = C.paper; for (let d = 0; d < 3; d++) { c.beginPath(); c.arc(10 + d * 12, 8, 3, 0, Math.PI * 2); c.fill(); }
      setFont(c, F.typewriter(700), 22); c.fillStyle = C.black; c.fillText(`${A[i]}.lovable.app`, 12, 48);
      setFont(c, F.sign(700), 28); c.fillStyle = C.orange; c.fillText('✓ LIVE', 12, 82);
      c.restore();
    });
    // the box: shut, jolting on each throw it swallows
    const gulp = Math.max(0, ...thrown.map((ti) => 1 - clamp((t - ti - FLY) / 0.12) - (t < ti + FLY ? 1 : 0)));
    c.save(); c.translate(bx + bw / 2, by + bh); c.scale(1 + 0.03 * gulp + 0.01 * kick, 1 - 0.03 * gulp); c.translate(-(bx + bw / 2), -(by + bh));
    c.fillStyle = C.black; c.fillRect(bx, by, bw, bh);
    c.fillStyle = gulp > 0 ? C.orange : ink({ black: 0.6, orange: 0.3 }); c.fillRect(slot[0]! - 120, by + 4, 240, 12); // the slot
    setFont(c, F.sign(700), 110); c.fillStyle = C.paper; c.textAlign = 'center'; c.fillText('LOVABLE', bx + bw / 2, by + 170);
    setFont(c, F.typewriter(700), 24); c.fillText('STOCKHOLM · $13.3 BN', bx + bw / 2, by + 214);
    c.fillStyle = ink({ black: 1, blue: 0.3 }); c.fillRect(bx + 50, by + 260, bw - 100, 280); // the window you can't see through
    setFont(c, F.typewriter(700), 28); c.fillStyle = ink({ black: 0.35 }); c.fillText('what happens in here:', bx + bw / 2, by + 310);
    c.textAlign = 'left'; c.restore();
    if (t >= tm) stamp(c, '[MASK]', bx + bw / 2, by + 420, { k: prog(t, tm, tm + 0.1), size: 130, color: C.orange, rot: -0.05 });
    // the prompts, thrown in from below on the eighth notes
    thrown.forEach((ti, i) => {
      if (t < ti || t >= ti + FLY) return;
      const k = (t - ti) / FLY, sx = 120 + ((i * 263) % 760), x = sx + (slot[0]! - sx) * k, y = 1160 + (slot[1]! - 1160) * k - 360 * Math.sin(Math.PI * k);
      const sc = 1.25 - 0.85 * k * k;
      c.save(); c.translate(x, y); c.rotate((1 - k) * (i % 2 ? 0.5 : -0.4) + k * 0.02); c.scale(sc, sc);
      const txt = ti >= tm ? M[i]! : P[i]!;
      setFont(c, F.typewriter(700), 34); const w = c.measureText(txt).width + 40;
      sheet(c, -w / 2, -32, w, 64, 0); c.fillStyle = C.black; c.fillText(txt, -w / 2 + 20, 11);
      c.restore();
    });
  }

  /** L15, "And you're optimizing, accelerating": the fax runs on the bass. Every bass note feeds one result out of the
   *  machine and a rubber stamp comes down on it, RECEIVED, on the note: it lifts, hangs and drops ahead of each hit
   *  (anticipation, impact, rebound), and the paper takes the knock. */
  override d_fax(c: Ctx, s: any, t: number) {
    c.fillStyle = C.black; c.fillRect(960, 0, 960, H);
    const B = ((this.T as any).onsets.bass as [number, number][]).filter(([b, a]) => b >= s.t0 - 0.02 && b < s.t1 && a >= 0.4).map(([b]) => b); // data/timing_eu.json
    const items = ['ERDŐS UNIT DISTANCE: DISPROVED', 'JACOBIAN CONJECTURE: FALSE', 'IMO 2026: 42/42', 'FERMAT, IN LEAN: 11 DAYS', 'EU INC: PENDING', 'NAVIER–STOKES: 88 H', 'METR HORIZON: DOUBLING', 'FRONTIERMATH: ▲', 'ERDŐS #1043: SOLVED'];
    const LS = 66, HEAD = 590, JOLT = 0.045;
    const n = B.filter((b) => b <= t).length, last = n ? B[n - 1]! : -9;
    const feed = B.reduce((a, b) => a + LS * ease.outCubic(clamp((t - b) / JOLT)), 0);
    const knock = Math.exp(-Math.max(0, t - last) / 0.05) * (n ? 1 : 0); // the paper takes the hit
    // the machine, its display blinking on each note
    c.fillStyle = ink({ black: 0.35, blue: 0.3 }); c.fillRect(1000, 620, 860, 240);
    c.fillStyle = C.black; c.fillRect(1040, 650, 260, 70);
    c.fillStyle = knock > 0.3 ? C.paper : C.yellow; setFont(c, F.sign(700), 30); c.fillText(n ? `RECEIVED ${String(n).padStart(2, '0')}` : 'SENDING…', 1060, 697);
    c.save(); c.beginPath(); c.rect(1000, 0, 860, 620); c.clip(); c.translate(0, 5 * knock);
    c.fillStyle = C.paper; c.fillRect(1030, 0, 800, 640);
    B.forEach((b, i) => {
      if (t < b) return;
      const y = HEAD + LS - (feed - LS * i);
      if (y < -40) return;
      setFont(c, F.typewriter(700), 31); c.fillStyle = C.black; c.fillText(items[i % items.length]!, 1050, y);
      stamp(c, 'RECEIVED', 1736 + (hash(i, 3) - 0.5) * 24, y - 12, { k: prog(t, b, b + 0.05), size: 26, color: C.blue, rot: (hash(i, 5) - 0.5) * 0.16 });
    });
    c.restore();
    // the rubber stamp: drops ahead of each note (accelerating), hits on it, rebounds
    const next = B.find((b) => b > t), hy = HEAD - 30;
    let u = 1; // 1 = up, 0 = on the paper
    if (n && t - last < 0.2) u = ease.outCubic((t - last) / 0.2);
    if (next !== undefined && next - t < 0.12) u = Math.min(u, 1 - ease.inCubic(1 - (next - t) / 0.12));
    const sy = hy - 190 * u;
    c.fillStyle = C.black; c.fillRect(1714, sy - 150, 44, 110); c.beginPath(); c.arc(1736, sy - 156, 38, 0, Math.PI * 2); c.fill(); // the handle
    c.fillStyle = ink({ black: 0.6, orange: 0.4 }); c.fillRect(1648, sy - 46, 176, 38); c.fillStyle = C.blue; c.fillRect(1652, sy - 10, 168, 10); // block and rubber
    captionSlip(c, ['“The internet is new territory for all of us.”', '— Angela Merkel, Berlin, 19 June 2013'], 1010, 900, { size: 19 });
  }

  /** L4, "There was a sudden drop in your training loss": Ibry's graphic timetable, Paris (top) to Lyon (bottom), the
   *  hours across; every printed train is a slope. The loss curve rides it like one of Europe's trains, slow, through
   *  "there was a sudden"; on "drop" it falls straight down to Lyon, a vertical line, the train that takes no time;
   *  then it runs flat along the bottom, and the camera pulls back to the whole graph on "loss". */
  override d_dbBoard(c: Ctx, s: any, t: number) {
    const w = (x: string) => this.when(`L4:${x}`), t0 = this.when('L4'), tS = w('sudden'), tD = w('drop'), tI = w('in'), tL = w('loss');
    const im = img('animatic/img/marey-ibry-train-graph-1885.jpg');
    c.fillStyle = C.paper; c.fillRect(0, 0, W, H);
    if (!im) return;
    // the curve, in image coordinates: slow slope, a hesitation, the drop, the flat
    const P: [number, number, number][] = [[t0, 0.075, 0.03], [tS, 0.42, 0.2], [tD, 0.47, 0.22], [tD + 0.14, 0.48, 0.915], [tL, 0.9, 0.915]];
    const head = (tt: number): [number, number] => {
      if (tt <= P[0]![0]) return [P[0]![1], P[0]![2]];
      for (let i = 1; i < P.length; i++) if (tt <= P[i]![0]) { const [a0, u0, v0] = P[i - 1]!, [a1, u1, v1] = P[i]!, k = (tt - a0) / (a1 - a0); return [u0 + (u1 - u0) * k, v0 + (v1 - v0) * k]; }
      return [P.at(-1)![1], P.at(-1)![2]];
    };
    const [hu, hv] = head(t), back = ease.inOutCubic(clamp((t - (tL - 0.45)) / 0.6));
    let fu = Math.max(0.3, hu - 0.05), fv = Math.min(0.75, Math.max(0.3, hv)), z = 1.9;
    fu += (0.5 - fu) * back; fv += (0.5 - fv) * back; z += (1.0 - z) * back;
    const sc = coverScale(im, W, H) * z, X = 1180 + (960 - 1180) * back, Y = 580 + (540 - 580) * back; // the wide shot is centred: the words are on the line now
    const S = (u: number, v: number) => [X + (u - fu) * im.width * sc, Y + (v - fv) * im.height * sc];
    drawImageAt(c, im, X, Y, sc, 'line', 0, fu, fv);
    // the loss curve, drawn up to now, and its head
    c.strokeStyle = C.orange; c.lineWidth = 12; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath();
    for (let i = 0; i <= 80; i++) { const tt = t0 + (Math.min(t, tL) - t0) * (i / 80), [u, v] = head(tt), [x, y] = S(u, v + (tt > tD + 0.14 ? 0.006 * Math.sin(tt * 40) : 0)); if (i) c.lineTo(x!, y!); else c.moveTo(x!, y!); }
    c.stroke(); c.lineCap = 'butt';
    const [hx, hy] = S(hu, hv); c.fillStyle = C.black; c.beginPath(); c.arc(hx!, hy!, 14, 0, Math.PI * 2); c.fill();
    // the lyric rides the line: each word is set along the curve where the head is when it is sung (pushed along so
    // none overlap), turned to the line's direction ("drop" runs down the vertical), under the line on the way down and
    // over it along the bottom, and pops in on its own frame; the camera's zoom scales them
    const Lw = this.ctx.lyrics.lines[3]!.words, fz = 66 * (z / 1.9), ipx = (u: number, v: number) => [u * im.width, v * im.height];
    const PS: { s: number; u: number; v: number }[] = []; // the path by arc length, in image px
    for (let i = 0, acc = 0; i <= 600; i++) {
      const [u, v] = head(t0 + (tL - t0) * (i / 600));
      if (i) { const [x0, y0] = ipx(PS[i - 1]!.u, PS[i - 1]!.v), [x1, y1] = ipx(u, v); acc += Math.hypot(x1! - x0!, y1! - y0!); }
      PS.push({ s: acc, u, v });
    }
    const at = (sa: number) => { const j = Math.max(1, PS.findIndex((p) => p.s >= sa)), p0 = PS[j - 1]!, p1 = PS[Math.min(j, PS.length - 1)]!; return { u: p1.u, v: p1.v, ang: Math.atan2((p1.v - p0.v) * im.height, (p1.u - p0.u) * im.width || 1e-6) }; };
    const arcOf = (tt: number) => PS[Math.round(clamp((tt - t0) / (tL - t0)) * 600)]!.s;
    setFont(c, arch(1, 0.9), fz);
    let prevEnd = -1e9;
    const lay = Lw.map((wd) => {
      const isDrop = /^drop/i.test(wd.w), txt = wd.w.toUpperCase(), w = (c.measureText(txt).width + 24) / sc;
      let cs = arcOf(isDrop ? tD + 0.07 : wd.start);
      cs = Math.max(cs, prevEnd + w / 2 + 6 / sc); prevEnd = cs + w / 2;
      return { wd, isDrop, txt, cs };
    });
    lay.forEach(({ wd, isDrop, txt, cs }) => {
      if (t < wd.start) return;
      const p = at(cs), [px, py] = S(p.u, p.v), ang = isDrop ? Math.PI / 2 : p.ang;
      const nx = -Math.sin(ang), ny = Math.cos(ang), below = !isDrop && p.v < 0.5, off = isDrop ? fz * 0.2 : below ? fz * 1.05 : -fz * 0.3;
      const k = ease.outBack(clamp((t - wd.start) / 0.12));
      c.save(); c.translate(px! + nx * off, py! + ny * off); c.rotate(ang); c.scale(k, k);
      const tw = c.measureText(txt).width;
      c.fillStyle = C.yellow; c.fillRect(-tw / 2 - 8, -fz * 0.82, tw + 16, fz * 0.98);
      c.fillStyle = C.black; c.textAlign = 'center'; c.fillText(txt, 0, 0); c.textAlign = 'left';
      c.restore();
    });
    if (s.capL && t - s.t0 > 0.25) captionSlip(c, s.capL, 1180, 50, { size: 18 });

    if (t >= tD + 0.14) { // the impact at Lyon, and the tag on the vertical
      const e = t - tD - 0.14, [bx, by] = S(0.48, 0.915);
      if (e < 0.3) { c.strokeStyle = C.orange; c.lineWidth = 6; for (let r = 0; r < 10; r++) { const a = Math.PI + (r / 9) * Math.PI; c.beginPath(); c.moveTo(bx! + Math.cos(a) * 20, by! + Math.sin(a) * 20); c.lineTo(bx! + Math.cos(a) * (20 + 300 * e), by! + Math.sin(a) * (20 + 300 * e)); c.stroke(); } }
      const [mx, my] = S(0.485, 0.68); stamp(c, 'PARIS → LYON · 0 MIN', mx! + 330 + 60 * z, my!, { k: prog(t, tD + 0.14, tD + 0.24), size: 58, color: C.orange, rot: -0.08 });
    }
    if (t >= tL) stamp(c, 'DB 2026: 52.6 % ON TIME', 1450, 770, { k: prog(t, tL, tL + 0.1), size: 46, color: C.blue, rot: -0.06 });
  }

  /** L21, "The Omega Point's coming soon": one climb up Teilhard's own figure (Le Phénomène humain, 1955, fig. 3)
   *  into his image for it, the meridians of the Earth converging at the pole. On "Omega" the camera rises from the
   *  Eocene; above the Pliocene his branches keep splitting, more and more of them, and flow into a turning globe where
   *  they run on as meridians, cross-linked into a denser and denser mesh, nodes lighting up (the noosphere); on
   *  "Point's" everything converges at the pole, which flares; on "coming" the camera pulls back to the whole, the
   *  complexity readout climbs and stops at 99 %; "soon" gets the footnote. */
  override d_omega(c: Ctx, s: any, t: number) {
    const tO = this.when('L21:omega'), tP = this.when('L21:point'), tC = this.when('L21:coming'), tS = this.when('L21:soon');
    const k = 0.9, x0 = 1020, y0 = 200, X = (u: number) => x0 + u * k, Yf = (v: number) => y0 + v * k;
    const tips = [230, 250, 420, 455, 480, 510, 645, 665, 690, 715, 755, 815], TY = Yf(75);
    const GX = X(520), GY = -560, R = 360, tilt = 0.42, spin = t * 0.5; // the globe; its pole is the Omega point
    const pole: [number, number] = [GX, GY - R * Math.cos(tilt)];
    const onGlobe = (th: number, ph: number): [number, number, number] => { // latitude from the pole th, longitude ph -> x, y, depth
      const sx = Math.sin(th) * Math.sin(ph), sy = Math.cos(th), sz = Math.sin(th) * Math.cos(ph);
      return [GX + R * sx, GY - R * (sy * Math.cos(tilt) - sz * Math.sin(tilt)), sz * Math.cos(tilt) + sy * Math.sin(tilt)];
    };
    const climb = ease.inOutCubic(clamp((t - s.t0) / Math.max(0.3, tP - s.t0))), back = ease.inOutCubic(clamp((t - tC + 0.05) / 0.4));
    let cx = 1300, cy = 860 + (pole[1] + 70 - 860) * climb, z = 1.45;
    cx += (1150 - cx) * back; cy += (-220 - cy) * back; z += (0.6 - z) * back;
    c.save(); c.translate(1150, 540); c.scale(z, z); c.translate(-cx, -cy);
    const fig = img('animatic/img/teilhard-fig3.jpg');
    sheet(c, x0 - 14, y0 - 14, 910 * k + 28, 900 * k + 28, 0.004, C.paper);
    if (fig) drawImageAt(c, fig, X(455), Yf(450), k, 'line', 0, 0.5, 0.5);
    const reach = Math.min(TY, cy - 380 / z) + (pole[1] - Math.min(TY, cy - 380 / z)) * back; // how far up things have grown
    const g = clamp((TY - reach) / (TY - pole[1]));
    // the axis through the epochs he printed and the ones he did not
    c.strokeStyle = C.black; c.lineWidth = 4; c.beginPath(); c.moveTo(X(205), TY); c.lineTo(X(205), Math.max(GY + 120, reach)); c.stroke();
    ([['PLÉISTOCÈNE', 120], ['HOLOCÈNE', 300]] as [string, number][]).forEach(([l, dy]) => {
      const y = TY - dy; if (reach > y) return;
      c.lineWidth = 3; c.setLineDash([12, 8]); c.beginPath(); c.moveTo(X(205) - 10, y); c.lineTo(X(850), y); c.stroke(); c.setLineDash([]);
      setFont(c, F.display(62.5, 500), 36); c.fillStyle = C.black; c.textAlign = 'right'; c.fillText(l, X(205) - 20, y + 13); c.textAlign = 'left';
    });
    // the branches keep branching on their way up into the globe's southern meridians
    const N = 24, base = (j: number) => onGlobe(2.15, (j / N) * Math.PI * 2 + spin);
    c.lineWidth = 3;
    tips.forEach((u, i) => {
      for (let b = 0; b < 2; b++) { // each tip splits in two, each half joins a meridian
        const j = (i * 2 + b) % N, [ex, ey, ed] = base(j), sx = X(u), mx = sx + (ex - sx) * 0.5 + (b ? 40 : -40), my = TY + (ey - TY) * 0.55;
        const kk = clamp((TY - reach) / (TY - ey));
        if (kk <= 0) continue;
        c.strokeStyle = ed > 0 ? C.black : ink({ black: 0.4 }); c.setLineDash(i % 3 === 1 ? [] : [12, 8]);
        c.beginPath(); c.moveTo(sx, TY);
        for (let q = 1; q <= 24; q++) { const v = (q / 24) * kk, x = (1 - v) * (1 - v) * sx + 2 * (1 - v) * v * mx + v * v * ex, y = (1 - v) * (1 - v) * TY + 2 * (1 - v) * v * my + v * v * ey; c.lineTo(x, y); }
        c.stroke(); c.setLineDash([]);
      }
    });
    // the globe: meridians to the pole, cross-links between them, nodes lighting up as it fills (the noosphere)
    if (g > 0.55) {
      const gk = clamp((g - 0.55) / 0.45);
      c.strokeStyle = ink({ black: 0.25 }); c.lineWidth = 2; c.beginPath(); c.arc(GX, GY, R, 0, Math.PI * 2); c.stroke();
      for (let j = 0; j < N; j++) {
        const ph = (j / N) * Math.PI * 2 + spin; c.beginPath();
        for (let q = 0; q <= 30; q++) { const th = 2.15 - (2.15 * q / 30) * gk, [x, y, d] = onGlobe(th, ph); if (q === 0) c.moveTo(x, y); else c.lineTo(x, y); if (q === 15) { c.strokeStyle = d > 0 ? C.black : ink({ black: 0.35 }); } }
        c.lineWidth = 2.5; c.stroke();
      }
      const links = Math.floor(260 * gk * gk);
      for (let n = 0; n < links; n++) { // cross-links between neighbouring meridians: complexity
        const j = Math.floor(hash(n, 1) * N), th = 0.25 + hash(n, 2) * 1.8, ph = (j / N) * Math.PI * 2 + spin, ph2 = ph + (Math.PI * 2 / N) * (hash(n, 3) > 0.5 ? 1 : 2);
        const [x1, y1, d1] = onGlobe(th, ph), [x2, y2, d2] = onGlobe(th + (hash(n, 4) - 0.5) * 0.3, ph2);
        if (d1 < 0 && d2 < 0) continue;
        c.strokeStyle = ink({ black: 0.55 }); c.lineWidth = 1.5; c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke();
        if (hash(n, 5) > 0.7) { const on = hash(n, Math.floor(t * 12)) > 0.5; c.fillStyle = on ? C.paper : C.black; c.beginPath(); c.arc(x1, y1, on ? 6 : 4, 0, Math.PI * 2); c.fill(); }
      }
      setFont(c, F.display(62.5, 500), 40); const nw = c.measureText('NOOSPHÈRE').width;
      c.fillStyle = C.black; c.fillRect(GX - R - nw - 40, GY - 26, nw + 20, 50); c.fillStyle = C.paper; c.fillText('NOOSPHÈRE', GX - R - nw - 30, GY + 13);
    }
    // the Omega point: the pole flares, a light, not an eye
    if (t >= tP) {
      const q = ease.outCubic(clamp((t - tP) / 0.2)), hit = Math.exp(-(t - tP) / 0.25), [px, py] = pole, r = 70 + 260 * q + 80 * hit;
      const gr = c.createRadialGradient(px, py, 0, px, py, r);
      gr.addColorStop(0, C.paper); gr.addColorStop(0.25, C.yellow); gr.addColorStop(0.6, ink({ yellow: 1, orange: 0.6 }, 0.8)); gr.addColorStop(1, ink({ yellow: 1, orange: 0.6 }, 0));
      c.fillStyle = gr; c.beginPath(); c.arc(px, py, r, 0, Math.PI * 2); c.fill();
      setFont(c, F.display(62.5, 900), 170); c.fillStyle = C.black; c.textAlign = 'center'; c.fillText('Ω', px, py - 150); c.textAlign = 'left';
      const hd = img('animatic/img/teilhard-point-omega.jpg');
      if (hd && t >= tP + 0.08) { const qq = ease.outCubic(clamp((t - tP - 0.08) / 0.12)); c.save(); c.translate(px + 640, py - 60 - (1 - qq) * 60); c.rotate(-0.025); sheet(c, -300, -54, 600, 108, 0, C.paper); drawImageAt(c, hd, 0, 0, 0.69, 'line', 0, 0.5, 0.5); c.restore(); }
    }
    c.restore();
    // coming: the complexity readout climbs, and stops short
    if (t >= tC) {
      const pct = Math.min(99, Math.floor(80 + 19.9 * clamp((t - tC) / Math.max(0.2, tS - tC))));
      c.fillStyle = C.black; c.fillRect(1440, 60, 440, 64); setFont(c, F.sign(700), 40); c.fillStyle = C.paper; c.fillText(`COMPLEXITY ${pct} %`, 1462, 108);
    }
    if (t >= tS) { // soon: the footnote
      const q = ease.outBack(clamp((t - tS) / 0.1));
      c.save(); c.translate(1640, 200); c.rotate(-0.04); c.scale(q, q);
      sheet(c, -230, -50, 460, 100, 0, C.yellow);
      setFont(c, F.archivo(100, 600), 24); c.fillStyle = C.black; c.fillText('* Will not be initially available', -206, -8); c.fillText('  in the EU.  (Apple, 14 Sep 2026)', -206, 26);
      c.restore();
    }
    if (s.capL && t - s.t0 > 0.25) captionSlip(c, s.capL, 60, 900, { size: 19 });
  }

  /** L20, "Nokia to the moon": the startup chart, literally. The 1865 paper mill is the launch pad and Galileo's 1610 moon
   *  the target. On "Nokia" the classic candybar phone lights up and runs along the flat years of the curve (paper 1865,
   *  rubber 1898, cables 1912, the GSM phone 1992); on "to the" the curve becomes a hockey stick and it rockets; on
   *  "moon" it lands, on its side, like IM-2 did in March 2025. */
  override d_mill(c: Ctx, s: any, t: number) {
    const L = this.ctx.lyrics.lines[19]!, tN = L.words[0]!.start, tTo = L.words[1]!.start, tM = L.words.at(-1)!.start;
    // graph paper over the orange, and the axes of every pitch deck
    c.strokeStyle = ink({ black: 0.18 }); c.lineWidth = 2;
    for (let x = 120; x < 1880; x += 80) { c.beginPath(); c.moveTo(x, 60); c.lineTo(x, 1000); c.stroke(); }
    for (let y = 60; y < 1000; y += 80) { c.beginPath(); c.moveTo(120, y); c.lineTo(1880, y); c.stroke(); }
    c.strokeStyle = C.black; c.lineWidth = 5; c.beginPath(); c.moveTo(120, 60); c.lineTo(120, 1000); c.lineTo(1880, 1000); c.stroke();
    setFont(c, F.sign(700), 26); c.fillStyle = C.black; c.save(); c.translate(100, 560); c.rotate(-Math.PI / 2); c.fillText('GROWTH', 0, 0); c.restore();
    this.card(c, 'galileo-moon-1610', 1600, 270, 400, 0.02);
    this.card(c, 'nokia-paper-mill', 330, 830, 340, -0.02);
    // the curve: the flat years along the bottom to the launch pad, then the rocket's climb, the hockey stick
    const A = [480, 800], B0 = [1180, 760], Cq = [1200, 300], D = [1545, 380];
    const kh = t < tN ? 0 : clamp((t - tN) / (tTo - tN - 0.05)); // the history line, drawn through "Nokia"
    const kf = t < tTo ? 0 : t < tM ? ease.inCubic((t - tTo) / (tM - tTo)) : 1; // the flight
    const flat = (u: number): [number, number] => [A[0]! + (B0[0]! - A[0]!) * u, A[1]! + (B0[1]! - A[1]!) * u - 14 * Math.sin(Math.PI * u)];
    const fly = (u: number): [number, number] => [0, 1].map((j) => (1 - u) * (1 - u) * B0[j]! + 2 * (1 - u) * u * Cq[j]! + u * u * D[j]!) as [number, number];
    c.strokeStyle = C.black; c.lineWidth = 9; c.lineCap = 'round'; c.beginPath();
    for (let i = 0; i <= 40; i++) { const [x, y] = flat((i / 40) * kh); if (i) c.lineTo(x, y); else c.moveTo(x, y); }
    if (kf > 0) for (let i = 0; i <= 40; i++) { const [x, y] = fly((i / 40) * kf); c.lineTo(x, y); }
    c.stroke(); c.lineCap = 'butt';
    ([[0.06, '1865 PAPER'], [0.3, '1898 RUBBER'], [0.55, '1912 CABLES'], [0.8, '1992 GSM PHONE']] as [number, string][]).forEach(([k, l]) => {
      if (kh < k) return; const [x, y] = flat(k);
      c.fillStyle = C.black; c.beginPath(); c.arc(x, y, 9, 0, Math.PI * 2); c.fill(); setFont(c, F.typewriter(700), 22); c.fillText(l, x - 40, y + 44);
    });
    // the pad
    c.fillStyle = C.black; c.fillRect(B0[0]! - 90, B0[1]! + 6, 180, 16); c.fillRect(B0[0]! + 60, B0[1]! - 300, 14, 306);
    // the smoke: building on the pad before lift-off, then a trail
    if (t > tTo - 0.25) for (let j = 0; j < 30; j++) {
      const u = kf - j * 0.02, [x, y] = u > 0 ? fly(u) : [B0[0]! + (hash(j, 1) - 0.5) * 260 * clamp((t - tTo + 0.25) / 0.4), B0[1]! - hash(j, 2) * 40];
      c.fillStyle = ink({ black: 0.08 }, Math.max(0, 0.95 - j * 0.03)); c.beginPath(); c.arc(x! + Math.sin(j * 1.9) * 10, y! + 20, 18 + j * 2.6, 0, Math.PI * 2); c.fill();
    }
    // the rocket, the classic phone in its porthole: upright on the pad, nose along the climb, on its side on the moon
    const [px, py] = kf > 0 ? fly(kf) : [B0[0]!, B0[1]!], [qx, qy] = fly(Math.min(1, kf + 0.01));
    let ang = kf > 0 && kf < 1 ? Math.atan2(qy - py, qx - px) + Math.PI / 2 : 0;
    const landed = t >= tM ? ease.outBack(clamp((t - tM) / 0.25)) : 0;
    if (kf >= 1) ang = (Math.PI / 2 + 0.2) * landed; // down on its side
    const rumble = t > tTo - 0.25 && t < tTo + 0.2 ? Math.sin(t * 90) * 3 : 0;
    c.save(); c.translate(px + rumble, py); c.rotate(ang); c.scale(0.8, 0.8);
    if (t >= tTo && t < tM) { const fl = 90 + 50 * Math.abs(Math.sin(t * 50)); c.fillStyle = C.orange; c.beginPath(); c.moveTo(-34, 0); c.lineTo(0, fl * 1.8); c.lineTo(34, 0); c.closePath(); c.fill(); c.fillStyle = C.yellow; c.beginPath(); c.moveTo(-18, 0); c.lineTo(0, fl); c.lineTo(18, 0); c.closePath(); c.fill(); }
    c.fillStyle = C.black; for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(sd * 40, -90); c.lineTo(sd * 84, 8); c.lineTo(sd * 40, 0); c.closePath(); c.fill(); } // fins
    for (let r = 0; r < 8; r++) for (let k = 0; k < 2; k++) { c.fillStyle = (r + k) % 2 ? C.orange : C.paper; c.fillRect(-40 + k * 40, -260 + r * 32.5, 40, 32.5); }
    c.strokeStyle = C.black; c.lineWidth = 5; c.strokeRect(-40, -260, 80, 260);
    c.fillStyle = C.orange; c.beginPath(); c.moveTo(-40, -260); c.quadraticCurveTo(-36, -330, 0, -360); c.quadraticCurveTo(36, -330, 40, -260); c.closePath(); c.fill(); c.stroke(); // the nose
    c.fillStyle = C.paper; c.beginPath(); c.arc(0, -180, 34, 0, Math.PI * 2); c.fill(); c.stroke(); // the porthole
    c.fillStyle = C.blue; c.beginPath(); c.roundRect(-13, -206, 26, 52, 8); c.fill(); c.fillStyle = ink({ yellow: 0.35, blue: 0.2 }); c.fillRect(-9, -199, 18, 14); // the phone
    c.restore();
    if (t >= tM) { setFont(c, F.typewriter(700), 22); c.fillStyle = C.black; c.fillText('2025 THE MOON', D[0]! - 60, D[1]! + 120); }
    if (t >= tM) stamp(c, '25 MIN ON THE MOON', 1560, 560, { k: prog(t, tM + 0.1, tM + 0.2), size: 40, color: C.black, rot: -0.08, sub: 'IM-2 · 6 MAR 2025 · ON ITS SIDE' });
    this.poster(c, L, t, 90, 130, 760, { color: C.black, hl: C.yellow });
  }

  /** L37, "Post-AI-bubble, super-dense": over the 1720 Bubblers Medley cards an AI bubble inflates on the beat through
   *  "Post-AI-bubble" and pops on "super": what's left is what was left in 1720. */
  override d_medley(c: Ctx, s: any, t: number, lt: number) {
    super.d_medley(c, s, t, lt);
    const [w0, w1] = this.ctx.lyrics.lines[36]!.words, tP = w0!.start, tS = w1!.start, bp = this.ctx.audio.beatAt(t);
    const X = 1380, Y = 470;
    if (t >= tP && t < tS) {
      const g = Math.pow(clamp((t - tP) / (tS - tP)), 0.75), r = 60 + 330 * g + 10 * Math.max(0, Math.cos((bp % 1) * Math.PI * 2)) * g;
      c.save();
      c.fillStyle = ink({ blue: 0.12 }, 0.55); c.beginPath(); c.arc(X, Y, r, 0, Math.PI * 2); c.fill();
      c.strokeStyle = C.paper; c.lineWidth = 8; c.stroke();
      c.strokeStyle = C.paper; c.lineWidth = 10; c.lineCap = 'round'; c.beginPath(); c.arc(X, Y, r * 0.78, -2.5, -1.7); c.stroke(); // the shine
      setFont(c, F.sign(700), 40 + 150 * g); c.fillStyle = C.black; c.textAlign = 'center'; c.fillText('AI', X, Y + (14 + 52 * g)); c.textAlign = 'left';
      c.restore();
    } else if (t >= tS && t < tS + 0.5) { // pop
      const e = t - tS, R = 390;
      c.fillStyle = C.paper;
      for (let i = 0; i < 36; i++) { const a = (i / 36) * Math.PI * 2 + hash(i, 1) * 0.2, d = R + 600 * ease.outCubic(e / 0.5) * (0.6 + 0.6 * hash(i, 2)); c.beginPath(); c.arc(X + Math.cos(a) * d, Y + Math.sin(a) * d + 300 * e * e, 9 * (1 - e / 0.5) + 2, 0, Math.PI * 2); c.fill(); }
    }
    if (t >= tS) stamp(c, 'POP', X - 40, Y + 60, { k: prog(t, tS, tS + 0.08), size: 140, color: C.orange, rot: -0.14 });
  }

  /** L33, "Too late now, we lit the fuse": Nobel. The fuse burns evenly from "lit" to a beat before the next line and
   *  goes off there, dynamite: a fireball out of the fuse's end, the paper flashes, the frame shakes, debris falls. */
  override d_nobel(c: Ctx, s: any, t: number, lt: number, dur: number) {
    const tL = this.when('L33:lit'), B = (this.T.beats as number[]).filter((b) => b > tL + 1 && b < s.t1 - 0.5);
    const tB = B.at(-1) ?? s.t1 - 0.6, e = t - tB, FX = 1880, FY = 900;
    const shake = e >= 0 ? Math.exp(-e / 0.15) * 14 : 0;
    c.save(); c.translate(Math.sin(t * 90) * shake, Math.cos(t * 77) * shake);
    sheet(c, 1100, 70, 620, 720, 0.02);
    this.plate(c, s, lt, dur, [1120, 90, 580, 680]);
    // the fuse: burnt behind the spark, live ahead of it
    const k = clamp((t - tL) / (tB - tL)), sx = 1000 + k * (FX - 1000);
    c.strokeStyle = ink({ black: 0.35 }); c.lineWidth = 4; c.setLineDash([6, 10]); c.beginPath(); c.moveTo(1000, FY); c.lineTo(sx, FY); c.stroke(); c.setLineDash([]);
    c.strokeStyle = C.black; c.lineWidth = 6; c.beginPath(); c.moveTo(sx, FY); c.lineTo(FX, FY); c.stroke();
    if (e < 0) {
      if (t >= tL) for (let i = 0; i < 8; i++) { // sparks
        const a = hash(i, Math.floor(t * 30)) * Math.PI * 2, r = 14 + 26 * hash(i, Math.floor(t * 30), 3);
        c.strokeStyle = i % 2 ? C.yellow : C.orange; c.lineWidth = 3; c.beginPath(); c.moveTo(sx, FY); c.lineTo(sx + Math.cos(a) * r, FY + Math.sin(a) * r); c.stroke();
      }
      c.fillStyle = C.orange; c.beginPath(); c.arc(t >= tL ? sx : 1000, FY, 16 + 6 * Math.sin(t * 40), 0, Math.PI * 2); c.fill();
    } else { // the dynamite goes off
      const R = 60 + 1150 * ease.outExpo(clamp(e / 0.22)), spin = e * 0.6;
      const star = (r: number, col: string) => {
        c.fillStyle = col; c.beginPath();
        for (let i = 0; i < 32; i++) { const a = spin + (i / 32) * Math.PI * 2, rr = i % 2 ? r * (0.55 + 0.15 * hash(i, 7)) : r * (0.9 + 0.2 * hash(i, 9)); c.lineTo(FX + Math.cos(a) * rr, FY + Math.sin(a) * rr); }
        c.closePath(); c.fill();
      };
      star(R, C.orange); star(R * 0.62, C.yellow); star(R * 0.3 * Math.exp(-e / 0.3), C.paper);
      for (let i = 0; i < 40; i++) { // debris, thrown out and falling
        const a = Math.PI * (0.55 + 0.9 * hash(i, 1)), v = 700 + 900 * hash(i, 2), x = FX + Math.cos(a) * v * e, y = FY - Math.abs(Math.sin(a)) * v * e + 1400 * e * e;
        c.fillStyle = i % 3 ? C.black : C.orange; c.save(); c.translate(x, y); c.rotate(e * 12 * (hash(i, 3) - 0.5)); c.fillRect(-9, -5, 18, 10); c.restore();
      }
    }
    c.restore();
    if (e >= 0 && e < 0.12) { c.fillStyle = C.paper; c.globalAlpha = 0.7 * (1 - e / 0.12); c.fillRect(0, 0, W, H); c.globalAlpha = 1; } // the flash
  }

  /** The outro after "Was it all for show?": the answer in GPUs, one block per 10 billion. Europe's public money for
   *  AI gigafactories, up to €10 bn (EU and national; the call for up to seven, 30 July 2026): one block lands on the
   *  first beat, "€10 BN" goes up on it and Europe celebrates (confetti, a flag, the block bouncing on the beats). Then
   *  US big tech's planned AI capex for 2026, about $700 bn (Amazon, Microsoft, Alphabet, Meta): seventy, stacked three
   *  to a 16th while the camera climbs the tower; the party stops; it pulls back to both and holds. The shot runs to the credits (the gallery shot is dropped, see init). */
  override d_ring(c: Ctx, s: any, t: number) {
    const B = (this.T.beats as number[]).filter((b) => b >= s.t0 - 0.05 && b < s.t1), b0 = B[0] ?? s.t0, bU = B[3] ?? s.t0 + 1.4; // Europe's party: three beats
    const N = 70, BH = 34, BW = 300, GY = 980, EX = 420, UX = 1250; // block height and width, the ground, the two stacks
    const PER = 3; // blocks per 16th
    const placed = t < bU ? 0 : Math.min(N, PER * (1 + Math.floor((t - bU) / S16)));
    const tDone = bU + (Math.ceil(N / PER) - 1) * S16, back = ease.inOutCubic(clamp((t - tDone - 0.15) / 0.8));
    const party = t >= b0 + 0.15 ? 1 - clamp((t - bU - 0.25) / 0.4) : 0; // Europe's celebration, until the US stack is well under way
    const top = GY - placed * BH;
    const pre = 1 - clamp((t - bU + 0.3) / 0.4); // close on Europe before the US starts
    let cy = placed ? Math.min(560, top + 300) : 560 + 260 * pre, cx = placed ? 835 : 835 - 415 * pre, z = placed ? 1 : 1 + 0.35 * pre;
    cy += (GY - (N * BH) / 2 + 200 - cy) * back; z += (0.36 - z) * back;
    c.fillStyle = C.paper; c.fillRect(0, 0, W, H);
    c.save(); c.translate(960, 600); c.scale(z, z); c.translate(-cx, -cy);
    c.fillStyle = C.black; c.fillRect(-2000, GY, 6000, 8);
    const gpu = (x: number, y: number, col: string) => { // a GPU board seen from the side: card, two fans, gold edge
      c.save(); c.translate(x, y);
      c.fillStyle = col; c.fillRect(-BW / 2, -BH, BW, BH - 2); c.strokeStyle = C.black; c.lineWidth = 3; c.strokeRect(-BW / 2, -BH, BW, BH - 2);
      c.fillStyle = C.paper; for (const fx of [-70, 70]) { c.beginPath(); c.arc(fx, -BH / 2, 11, 0, Math.PI * 2); c.fill(); }
      c.fillStyle = C.yellow; c.fillRect(-BW / 2 + 20, -6, BW - 40, 4);
      c.restore();
    };
    // Europe: one block on the first beat, bouncing on the beats while it celebrates, "€10 BN" on top
    if (t >= b0) {
      const k = ease.outBack(clamp((t - b0) / 0.12)), bb = this.ctx.audio.beatAt(t), hop = party * 26 * Math.max(0, Math.sin((bb % 1) * Math.PI));
      gpu(EX, GY - (1 - k) * 300 - hop, C.blue);
      const tl = ease.outBack(clamp((t - b0 - 0.2) / 0.15));
      if (tl > 0 && back < 0.5) { c.save(); c.translate(EX, GY - BH - 60 - hop); c.scale(tl, tl); setFont(c, F.sign(700), 72); c.fillStyle = C.blue; c.textAlign = 'center'; c.fillText('€10 BN', 0, 0); c.restore(); }
      if (party > 0) { // the flag, waving on its pole
        const fx = EX + 110, fy = GY - BH - 220 - hop, wv = Math.sin(t * 8) * 8;
        c.strokeStyle = C.black; c.lineWidth = 5; c.beginPath(); c.moveTo(fx, GY - BH - hop); c.lineTo(fx, fy); c.stroke();
        c.save(); c.globalAlpha = party; c.transform(1, wv / 120, 0, 1, fx, fy); c.fillStyle = C.blue; c.fillRect(0, 0, 120, 80);
        c.fillStyle = C.yellow; for (let st = 0; st < 12; st++) { const an = (st / 12) * Math.PI * 2; c.beginPath(); c.arc(60 + Math.cos(an) * 26, 40 + Math.sin(an) * 26, 4, 0, Math.PI * 2); c.fill(); }
        c.restore();
      }
      setFont(c, F.sign(700), 40); c.fillStyle = C.black; c.textAlign = 'center'; c.globalAlpha = 1 - clamp((back - 0.4) / 0.3);
      c.fillText('EU · €10 BN', EX, GY + 60); setFont(c, F.typewriter(700), 20); c.fillText('AI gigafactories, public money', EX, GY + 92); c.fillText('call of 30 July 2026', EX, GY + 118);
      c.textAlign = 'left'; c.globalAlpha = 1;
    }
    // the US: seventy, three to a 16th
    for (let i = 0; i < placed; i++) {
      const ti = bU + Math.floor(i / PER) * S16, k = clamp((t - ti) / 0.07), drop = (1 - ease.outCubic(k)) * 160;
      gpu(UX + ((i % PER) - 1) * 7, GY - i * BH - drop, i % 2 ? ink({ black: 0.85 }) : C.black);
    }
    if (t >= bU - 0.3) {
      setFont(c, F.sign(700), 40); c.fillStyle = C.black; c.textAlign = 'center'; c.globalAlpha = 1 - clamp((back - 0.4) / 0.3);
      c.fillText(`US · $${placed * 10} BN`, UX, GY + 60); setFont(c, F.typewriter(700), 20); c.fillText('big tech AI capex planned for 2026', UX, GY + 92); c.fillText('Amazon, Microsoft, Alphabet, Meta', UX, GY + 118); c.globalAlpha = 1;
      if (placed > 0) { setFont(c, F.sign(700), 64); c.fillStyle = C.orange; c.fillText(`$${placed * 10} BN`, UX, top - 30); }
      c.textAlign = 'left';
    }
    c.restore();
    // confetti over Europe's party (screen space), falling away when it stops
    if (party > 0) {
      const e = t - b0;
      for (let i = 0; i < 160; i++) {
        const x = 120 + hash(i, 1) * 900, y = -40 + e * (300 + hash(i, 2) * 260) - hash(i, 3) * 400;
        if (y < -30 || y > H) continue;
        c.save(); c.globalAlpha = party; c.translate(x + Math.sin(t * 3 + i) * 24, y); c.rotate(t * (4 + hash(i, 4) * 5));
        c.fillStyle = [C.yellow, C.blue, C.paper, C.orange][i % 4]!; c.fillRect(-7, -4, 14, 8); c.restore();
      }
    }
    if (back > 0.6) { // the wide shot's own labels, readable at this scale
      const q = clamp((back - 0.6) / 0.3), sx = (x: number) => 960 + (x - 835) * z, sy = 600 + (GY - cy) * z;
      c.globalAlpha = q; setFont(c, F.sign(700), 46); c.textAlign = 'center';
      c.fillStyle = C.blue; c.fillText('EU €10 BN', sx(EX) - 60, sy + 64);
      c.fillStyle = C.black; c.fillText('US $700 BN', sx(UX) + 60, sy + 64);
      c.textAlign = 'left'; c.globalAlpha = 1;
    }
    if (back > 0.5) stamp(c, '1 : 70', 520, 520, { k: prog(t, tDone + 0.6, tDone + 0.7), size: 120, color: C.orange, rot: -0.08, sub: 'ONE BLOCK = 10 BILLION' });
    if (back > 0.3) captionSlip(c, ['EU: up to €10 bn of EU and national public money for', 'up to seven AI gigafactories (call, 30 July 2026).', 'US: Amazon, Microsoft, Alphabet and Meta plan about', '$700 bn of AI capex in 2026. One block is 10 billion.'], 40, 700, { size: 17 });
    else captionSlip(c, ['EU: up to €10 bn of EU and national public money for up to seven AI gigafactories', '(call, 30 July 2026), €20 bn more hoped for from private investors. US: Amazon, Microsoft,', 'Alphabet and Meta plan about $700 bn of AI capex in 2026. One block is 10 billion.'], 60, 40, { size: 18, w: 1000 });
  }

  /** The outro's second part: the EU ring of stars with her singing in the middle (the original ring shot, see d_ring). */
  d_eucircle(c: Ctx, s: any, t: number, lt: number) { super.d_ring(c, s, t, lt); }

  /** L19, "I hear the basic income gloom": the idea is Europe's own, and 510 years old. Holbein's island of Utopia
   *  (More's Utopia, Basel 1518; first printed at Leuven, 1516), filmed in one slow push; on "income" the idea's European
   *  road is stamped in a row, Leuven 1516 (More), Bruges 1526 (Vives), Brussels 1848 (Charlier), Brussels 2026 (the EU
   *  citizens' initiative); on "gloom" the island goes dark, still u-topia, no place. */
  override d_basicincome(c: Ctx, s: any, t: number) {
    const Ws = this.ctx.lyrics.lines[18]!.words, n = Ws.length;
    const tI = Ws[n - 2]!.start, tG = Ws[n - 1]!.start;
    const im = img('animatic/img/holbein-utopia-1518.jpg'); if (!im) return;
    const bx = 960, by = 40, bh = 1000, bw = bh * (im.width / im.height); // the plate's box (the lyric is on the left)
    // the camera: one slow push from the whole page into the island, settling on "gloom"
    const K: [number, number, number, number][] = [[s.t0, 0.5, 0.5, 1], [tG + 0.2, 0.49, 0.42, 1.25]];
    let u = 0.5, v = 0.5, z = 1;
    for (let i = 1; i < K.length; i++) {
      const [a0, u0, v0, z0] = K[i - 1]!, [a1, u1, v1, z1] = K[i]!;
      if (t >= a0) { const k = ease.inOutCubic(clamp((t - a0) / Math.max(0.05, a1 - a0))); u = u0 + (u1 - u0) * k; v = v0 + (v1 - v0) * k; z = z0 + (z1 - z0) * k; }
    }
    u = clamp(u, 0.5 / z, 1 - 0.5 / z); v = clamp(v, 0.5 / z, 1 - 0.5 / z);
    const slide = 1 - ease.outCubic(clamp((t - s.t0) / 0.14));
    c.save(); c.translate(slide * 700, 0);
    sheet(c, bx - 12, by - 12, bw + 24, bh + 24, 0.004, C.paper);
    c.save(); c.beginPath(); c.rect(bx, by, bw, bh); c.clip();
    drawImageAt(c, im, bx + bw / 2, by + bh / 2, (bh / im.height) * z, 'line', 0, u, v);
    if (t >= tG - 0.08) { const g = ease.outCubic(clamp((t - tG + 0.08) / 0.16)); c.fillStyle = ink({ black: 0.85, blue: 0.5 }, 0.72 * g); c.fillRect(bx, by, bw, bh); } // gloom, landing with the word
    c.restore();
    c.restore();
    // the road, stamped in a row one per 16th from "income"
    const road: [string, string][] = [['LEUVEN 1516', 'MORE, UTOPIA'], ['BRUGES 1526', 'VIVES, FOR THE POOR'], ['BRUSSELS 1848', 'CHARLIER, A DIVIDEND'], ['BRUSSELS 2026', 'THE EU INITIATIVE']];
    road.forEach(([a, b], i) => {
      const ti = tI + i * S16; if (t < ti) return;
      stamp(c, a, 190 + i * 225, 800 + (i % 2) * 14, { k: prog(t, ti, ti + 0.07), size: 34, color: i === 3 ? C.black : C.blue, rot: (i % 2 ? 0.05 : -0.05), sub: b });
    });
    if (t >= tG) stamp(c, 'STILL NO PLACE', bx + bw / 2, by + bh / 2, { k: prog(t, tG, tG + 0.08), size: 78, color: C.orange, rot: -0.1, sub: 'U-TOPIA · COLLECTION OPENS 4 JAN 2027' });
    this.poster(c, this.ctx.lyrics.lines[18]!, t, 90, 250, 820, { color: s.fg, hl: s.hl }); // its own line, held to the cut
    captionSlip(c, ['Ambrosius Holbein, the island of Utopia, in Thomas More, Utopia (Basel, 1518). PD.', 'Utopia: “no place”. Vives, De subventione pauperum (Bruges, 1526); Charlier, Solution du', 'problème social (Brussels, 1848); the EU citizens’ initiative for an unconditional basic income, 2026.'], 60, 920, { size: 17 });
  }

  override d_neumann(c: Ctx, s: any, t: number, lt: number, dur: number) {
    this.d_plateRight(c, s, t, lt, dur);
    // on "Neumann's" the route he took is stamped on the plate
    const nm = this.when('L25:neumann');
    if (t >= nm + 0.15) stamp(c, 'BUDAPEST 1903 → PRINCETON 1930', 1440, 760, { k: prog(t, nm + 0.15, nm + 0.25), size: 40, color: C.orange, rot: -0.06 });
  }

  override render(f: Frame, out: THREE.WebGLRenderTarget) {
    const r = super.render(f, out) as any;
    let si = 0;
    for (let i = 0; i < this.shots.length; i++) if (f.t >= this.shots[i]!.t0) si = i;
    const inks = this.shots[si]!.id === 'street' ? { yellow: FLUO } : undefined; // the Eurovision shot's drum change
    return { ...r, zoom: 1 + 0.006 * this.ctx.audio.hit('kick', f.t, 0.07), inks };
  }
}
