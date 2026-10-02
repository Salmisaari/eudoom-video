// Claude (EU Edition), the idol, drawn in ink by the engine (no generated footage).
// Orange suit, black bob, paper skin. Worn props: the AI-GENERATED (Art. 50) label, a residence-permit
// lanyard, a tethered-cap earring and a mic on a tether. She animates on 5s: pose, mouth, blinks and the
// outline boil all step together at 12 generations/s. The mouth reads data/visemes.json (analysis/visemes.py).
// Units: full figure has its face centre at (0,-118) and feet at +300; the bust has its face centre at (0,0).
import { C, ink } from '../engine/palette';
import { F, font } from '../engine/type';
import { clamp, hash } from '../engine/util';

type Ctx = CanvasRenderingContext2D;
type P2 = [number, number];
export type Viseme = 'X' | 'M' | 'F' | 'A' | 'E' | 'O' | 'U' | 'L' | 'S';
export type Pose = 'sing' | 'stamp' | 'chair' | 'back' | 'cap' | 'burst' | 'reach' | 'walk' | 'stand';
export type Brow = 'flat' | 'plead' | 'fierce';

const GEN = 12; // the idol's clock, generations per second
const TAU = Math.PI * 2;
const gen = (t: number) => Math.floor(t * GEN + 1e-6);
/** Boil: each part shifts by up to ±a units once per generation, like a re-cut paper sheet. */
const jit = (g: number, k: number, a = 1.3) => (hash(g, k) - 0.5) * 2 * a;

/** Viseme keys [t, shape] from the letter alignment; each shape holds until the next key. */
export class MouthChart {
  constructor(private keys: [number, Viseme][]) {}
  static async load() {
    const r = await fetch('data/visemes_eu.json');
    if (!r.ok || !(r.headers.get('content-type') ?? '').includes('json')) throw new Error('data/visemes_eu.json missing (run audio/el_music/eu_words.py)');
    return new MouthChart((await r.json()).keys);
  }
  private idx(t: number) {
    let lo = 0, hi = this.keys.length - 1;
    while (lo < hi) { const m = (lo + hi + 1) >> 1; if (this.keys[m]![0] <= t) lo = m; else hi = m - 1; }
    return lo;
  }
  /** Shape for the generation containing t: the one covering most of it, except that a lip closure (M)
   *  or F covering a quarter of it wins, so plosives don't drop out at 12 fps. */
  at(t: number): Viseme {
    const g0 = gen(t) / GEN, g1 = g0 + 1 / GEN;
    const cover = new Map<Viseme, number>();
    for (let i = this.idx(g0); i < this.keys.length && this.keys[i]![0] < g1; i++) {
      const a = Math.max(g0, this.keys[i]![0]), b = Math.min(g1, this.keys[i + 1]?.[0] ?? Infinity);
      if (b > a) cover.set(this.keys[i]![1], (cover.get(this.keys[i]![1]) ?? 0) + b - a);
    }
    for (const v of ['M', 'F'] as const) if ((cover.get(v) ?? 0) >= 0.25 / GEN) return v;
    let best: Viseme = 'X', bw = 0;
    for (const [v, w] of cover) if (w > bw) { best = v; bw = w; }
    return best;
  }
}

export interface IdolOpts {
  open?: number; // vocal level 0..1, scales the vowel shapes
  beat?: number; // beat phase 0..1
  mouth?: MouthChart;
  vis?: Viseme; // overrides the chart
  brow?: Brow;
  flip?: boolean;
  key?: string; // outline colour (paper on black grounds)
  suit?: string; // suit ink (the Twelve wear yellow)
  dancer?: boolean; // one of the Twelve: hair in a bun, no lanyard, label, earring or props
  hand?: P2; // pose 'cap': the raised hand placed by the scene (figure units), e.g. gripping a bottle cap
}

// ------------------------------------------------------------------ parts
let K: string = C.black; // outline ink for the figure being drawn

function shape(c: Ctx, fill: string | null, lw = 3) {
  if (fill) { c.fillStyle = fill; c.fill(); }
  if (lw) { c.strokeStyle = K; c.lineWidth = lw; c.stroke(); }
}
function dot(c: Ctx, x: number, y: number, r: number, fill: string) { c.beginPath(); c.arc(x, y, r, 0, TAU); c.fillStyle = fill; c.fill(); }
function seg(c: Ctx, pts: P2[], w: number, col: string) {
  c.strokeStyle = col; c.lineWidth = w; c.beginPath(); c.moveTo(pts[0]![0], pts[0]![1]);
  for (const p of pts.slice(1)) c.lineTo(p[0], p[1]);
  c.stroke();
}
/** A limb: outline stroke under a fill stroke. */
function limb(c: Ctx, pts: P2[], w: number, col: string) { seg(c, pts, w + 6, K); seg(c, pts, w, col); }

function bobPath(c: Ctx) {
  c.beginPath();
  c.moveTo(-66, 46); c.lineTo(-64, -26); c.quadraticCurveTo(-68, -86, 0, -84); c.quadraticCurveTo(68, -86, 64, -26); c.lineTo(66, 46);
}

function mouthShape(c: Ctx, v: Viseme, open: number) {
  const k = 0.55 + 0.6 * clamp(open);
  c.save(); c.translate(0, 35);
  const hole = (rx: number, ry: number, dy = 0) => { c.beginPath(); c.ellipse(0, dy, rx, Math.max(2, ry), 0, 0, TAU); };
  const teeth = (rx: number, ry: number, dy: number) => { c.save(); hole(rx, ry, dy); c.clip(); c.fillStyle = C.paper; c.fillRect(-rx, dy - ry, rx * 2, Math.min(4, ry)); c.restore(); };
  const tongue = (rx: number, ry: number, dy: number, top = false) => {
    c.save(); hole(rx, ry, dy); c.clip(); c.beginPath(); c.ellipse(0, top ? dy - ry + 3 : dy + ry - 2, rx * 0.6, 4.5, 0, 0, TAU); c.fillStyle = C.orange; c.fill(); c.restore();
  };
  c.lineCap = 'round';
  switch (v) {
    case 'X': c.beginPath(); c.moveTo(-10, 0); c.quadraticCurveTo(0, 3.5, 10, 0); shape(c, null, 3); break;
    case 'M': c.beginPath(); c.moveTo(-12, 0); c.quadraticCurveTo(0, 1.5, 12, 0); shape(c, null, 4.5); c.beginPath(); c.moveTo(-4, 5.5); c.lineTo(4, 5.5); shape(c, null, 2); break;
    case 'F': hole(11, 4, 1); shape(c, C.black, 0); c.fillStyle = C.paper; c.fillRect(-8, -2.5, 16, 3); c.beginPath(); c.moveTo(-11, 3); c.quadraticCurveTo(0, 7, 11, 3); shape(c, null, 3); break;
    case 'S': hole(13, 4.5); shape(c, C.paper, 3); c.beginPath(); c.moveTo(-11, 0); c.lineTo(11, 0); shape(c, null, 1.5); break;
    case 'E': hole(15, 6.5 * k, 1); shape(c, C.black, 3); teeth(15, 6.5 * k, 1); break;
    case 'A': hole(13, 12 * k, 3 * k); shape(c, C.black, 3); teeth(13, 12 * k, 3 * k); tongue(13, 12 * k, 3 * k); break;
    case 'O': hole(9.5, 11 * k, 2); shape(c, C.black, 3.5); break;
    case 'U': hole(6, 6.5, 1); shape(c, C.black, 4.5); break;
    case 'L': hole(12, 9 * k, 2); shape(c, C.black, 3); tongue(12, 9 * k, 2, true); break;
  }
  c.restore();
}

interface HeadOpts { vis: Viseme; open: number; brow: Brow; blink: boolean; look: number; g: number; bun?: boolean }
/** Face centre at (0,0): face 46 x 56, chin-length bob, blunt fringe at y = -16. */
function head(c: Ctx, o: HeadOpts) {
  const { g } = o;
  // hair, back layer
  c.save(); c.translate(jit(g, 1), jit(g, 2));
  if (o.bun) { c.beginPath(); c.arc(0, -70, 26, 0, TAU); } else { bobPath(c); c.closePath(); }
  shape(c, C.black, K === C.black ? 0 : 3); c.restore();
  // face
  c.beginPath(); c.ellipse(0, 0, 46, 56, 0, 0, TAU); shape(c, C.paper);
  dot(c, -25, 22, 8, ink({ orange: 0.35 })); dot(c, 25, 22, 8, ink({ orange: 0.35 })); // cheeks, a dot screen
  // eyes, with the orange spark in the iris
  for (const sx of [-1, 1]) {
    const ex = sx * 18, ey = 4;
    if (o.blink) { c.beginPath(); c.moveTo(ex - 10, ey); c.quadraticCurveTo(ex, ey + 5, ex + 10, ey); shape(c, null, 3.5); continue; }
    c.beginPath(); c.ellipse(ex, ey, 10, 7.5, 0, 0, TAU); shape(c, C.paper, 2);
    c.save(); c.clip();
    dot(c, ex + o.look * 3, ey + 0.5, 6.2, C.black);
    dot(c, ex + o.look * 3 + 2, ey - 1.5, 2.2, C.orange);
    c.restore();
    c.beginPath(); c.moveTo(ex - 11, ey + 1); c.quadraticCurveTo(ex, ey - 10, ex + 11, ey + 1); c.moveTo(ex + sx * 10, ey - 1); c.lineTo(ex + sx * 15, ey - 5); shape(c, null, 3.5);
  }
  // brows [outer y, inner y], just under the fringe
  const [bo, bi] = { flat: [-9, -9], plead: [-6, -15], fierce: [-13, -5] }[o.brow];
  for (const sx of [-1, 1]) { c.beginPath(); c.moveTo(sx * 27, bo); c.lineTo(sx * 9, bi); shape(c, null, 4); }
  c.beginPath(); c.moveTo(1, 12); c.quadraticCurveTo(-3, 20, 2, 21); shape(c, null, 2.5); // nose
  mouthShape(c, o.vis, o.open);
  if (o.bun) { // hair scraped back with a centre parting
    c.save(); c.translate(jit(g, 3), jit(g, 4));
    c.beginPath(); c.moveTo(-47, -4); c.quadraticCurveTo(-52, -64, 0, -62); c.quadraticCurveTo(52, -64, 47, -4);
    c.quadraticCurveTo(26, -34, 0, -30); c.quadraticCurveTo(-26, -34, -47, -4); c.closePath(); shape(c, C.black, K === C.black ? 0 : 3);
    c.strokeStyle = C.paper; c.lineWidth = 4; c.beginPath(); c.arc(0, -8, 48, -2.45, -1.95); c.stroke();
    c.restore();
    return;
  }
  // hair, front layer: side curtains and a blunt fringe with cut notches
  c.save(); c.translate(jit(g, 3), jit(g, 4));
  bobPath(c);
  c.lineTo(40, 46); c.quadraticCurveTo(42, 8, 38, -16);
  for (let i = 1; i < 8; i++) c.lineTo(38 - i * (76 / 8), -16 + (i % 2 ? 2.5 : 0));
  c.lineTo(-38, -16); c.quadraticCurveTo(-42, 8, -40, 46); c.closePath();
  shape(c, C.black, K === C.black ? 0 : 3);
  c.strokeStyle = C.paper; c.lineWidth = 4; c.beginPath(); c.arc(0, -26, 48, -2.45, -1.95); c.stroke(); // shine, knocked out of the black
  c.restore();
  // tethered-cap earring below the left curtain
  c.beginPath(); c.moveTo(-53, 46); c.lineTo(-53, 55); shape(c, null, 2);
  c.beginPath(); c.arc(-53, 58, 3, 0, TAU); shape(c, null, 1.5);
  c.beginPath(); c.moveTo(-53, 61); c.quadraticCurveTo(-56, 68, -60, 64); shape(c, null, 1.5);
  c.beginPath(); c.rect(-68, 62, 13, 8); shape(c, C.yellow, 1.5);
}

function faceState(t: number, pose: Pose | 'bust', o: IdolOpts): HeadOpts {
  const g = gen(t), open = clamp(o.open ?? 0);
  const vis = o.vis ?? o.mouth?.at(t) ?? (open > 0.2 ? 'A' : 'X');
  const brow = o.brow ?? (pose === 'reach' || pose === 'sing' || pose === 'bust' ? 'plead' : pose === 'stamp' || pose === 'burst' || pose === 'cap' ? 'fierce' : 'flat');
  const blink = (g + 7) % 37 < 2; // ~every 3 s, for 2 generations
  const look = Math.floor(g / 18) % 3 === 2 ? 1 : 0;
  return { vis, open, brow, blink, look, g, bun: o.dancer };
}

/**
 * Suit jacket from the collar (y = c0) to the hem: sloped shoulders (half-width sw, dropping by `drop`),
 * tailored in at the waist (half-width ww at y = wy), out to hw at the hem. `seams` draws the sleeve lines.
 */
function jacket(c: Ctx, g: number, j: { c0: number; hem: number; sw: number; drop: number; wy: number; ww: number; hw: number; seams?: boolean; suit: string; props: boolean; pad: number }) {
  const { c0, sw, drop } = j;
  c.save(); c.translate(jit(g, 5, 0.8), jit(g, 6, 0.8));
  // Eurovision power shoulders: a pointed pad each side, rising from the collar to a tip `pad` past the shoulder
  for (const sx of [-1, 1]) {
    c.beginPath(); c.moveTo(sx * 24, c0); c.lineTo(sx * (sw + j.pad), c0 - j.pad * 0.37); c.lineTo(sx * (sw + j.pad * 0.7), c0 + drop + j.pad * 0.4); c.lineTo(sx * sw * 0.8, c0 + drop + j.pad * 0.5); c.closePath();
    shape(c, j.suit);
  }
  c.beginPath();
  c.moveTo(-26, c0); c.bezierCurveTo(-sw * 0.6, c0, -sw, c0 + drop * 0.35, -sw, c0 + drop);
  c.lineTo(-j.ww, j.wy); c.lineTo(-j.hw, j.hem); c.lineTo(j.hw, j.hem); c.lineTo(j.ww, j.wy);
  c.lineTo(sw, c0 + drop); c.bezierCurveTo(sw, c0 + drop * 0.35, sw * 0.6, c0, 26, c0);
  c.closePath(); shape(c, j.suit);
  if (j.seams) for (const sx of [-1, 1]) { c.beginPath(); c.moveTo(sx * sw * 0.72, c0 + drop * 0.55); c.quadraticCurveTo(sx * sw * 0.66, (c0 + j.hem) / 2, sx * sw * 0.7, j.hem); shape(c, null, 3); }
  c.beginPath(); c.moveTo(-24, c0); c.lineTo(0, c0 + 90); c.lineTo(24, c0); c.closePath(); shape(c, C.paper, 2.5); // shirt
  c.beginPath(); c.moveTo(-26, c0); c.lineTo(-40, c0 + 50); c.lineTo(-4, c0 + 96); c.moveTo(26, c0); c.lineTo(40, c0 + 50); c.lineTo(4, c0 + 96); shape(c, null, 3); // lapels
  if (!j.props) { c.restore(); return; }
  // residence-permit lanyard and card
  c.strokeStyle = C.blue; c.lineWidth = 5; c.beginPath(); c.moveTo(-16, c0 - 2); c.lineTo(-7, c0 + 98); c.moveTo(16, c0 - 2); c.lineTo(7, c0 + 98); c.stroke();
  c.beginPath(); c.rect(-17, c0 + 96, 34, 44); shape(c, C.paper, 2);
  c.fillStyle = C.blue; c.fillRect(-17, c0 + 96, 34, 9);
  c.fillStyle = C.orange; c.fillRect(-12, c0 + 110, 10, 13);
  c.fillStyle = K; c.fillRect(1, c0 + 112, 11, 2); c.fillRect(1, c0 + 118, 8, 2);
  // AI-GENERATED (Art. 50) label on the lapel
  c.save(); c.translate(48, c0 + 36); c.rotate(-0.08);
  c.beginPath(); c.rect(-18, -10, 36, 20); shape(c, C.paper, 1.5);
  c.fillStyle = K; c.textAlign = 'center'; c.font = font(F.typewriter(700), 7); c.fillText('AI-GENERATED', 0, -1.5); c.fillText('Art. 50', 0, 6.5); c.textAlign = 'left';
  c.restore();
  c.restore();
}

function tether(c: Ctx, from: P2, to: P2) {
  c.beginPath(); c.moveTo(from[0] + 2, from[1] + 8); c.quadraticCurveTo(to[0] * 0.3, (from[1] + to[1]) * 0.6, to[0], to[1]); shape(c, null, 2.5);
}
function mic(c: Ctx, hand: P2, head: P2, r = 10) {
  seg(c, [hand, head], r * 0.8, K);
  dot(c, head[0], head[1], r, K);
  c.strokeStyle = C.paper; c.lineWidth = 1.5; c.beginPath(); c.moveTo(head[0] - r * 0.6, head[1] - r * 0.3); c.lineTo(head[0] + r * 0.6, head[1] - r * 0.3); c.stroke();
}

/** Elbow for a hand the scene places: halfway along the shoulder-hand line, bent 28 below it. */
function bend(h: P2): [P2, P2] {
  const dx = h[0] - 112, dy = h[1] + 30, l = Math.hypot(dx, dy) || 1;
  const px = (dx < 0 ? 1 : -1) * dy / l, py = Math.abs(dx) / l;
  return [[(112 + h[0]) / 2 + px * 28, (-30 + h[1]) / 2 + py * 28], h];
}
/** Elbow and hand for one arm (sx -1 = figure's right, on screen left). Two keys per beat. */
function armPose(pose: Pose, sx: number, bp: number, t: number): [P2, P2] {
  const alt = bp < 0.5;
  switch (pose) {
    case 'walk': { const sw = Math.sin(t * 7 + (sx > 0 ? Math.PI : 0)); return [[sx * 88 + sw * 12, 38], [sx * 80 + sw * 32, 110]]; }
    case 'sing': return sx > 0 ? [[88, 30], [28, -30]] : alt ? [[-104, 16], [-156, -44]] : [[-96, 34], [-118, 98]];
    case 'stamp': return alt ? [[sx * 86, -120], [sx * 26, -196]] : [[sx * 92, 10], [sx * 30, 50]];
    case 'reach': return sx > 0 ? [[150, -64], [232, -80]] : [[-64, 40], [-14, -10]];
    case 'cap': return sx > 0 ? [[118, -110], [140, -200]] : [[-96, 30], [-58, 88]];
    case 'burst': return [[sx * 136, -86], [sx * 206, -150]];
    default: return [[sx * 90, 36], [sx * 86, 112]];
  }
}

// ------------------------------------------------------------------ the idol, full figure
export function idol(c: Ctx, x: number, y: number, s: number, pose: Pose, t: number, o: IdolOpts = {}) {
  const g = gen(t), tq = g / GEN, bp = o.beat ?? 0;
  const bob = pose === 'chair' ? 0 : Math.round(Math.sin(bp * TAU) * 5);
  K = o.key ?? C.black;
  const suit = o.suit ?? C.blue;
  c.save(); c.translate(x, y + bob * s); c.scale(o.flip ? -s : s, s);
  c.lineJoin = 'round'; c.lineCap = 'round';
  if (pose === 'chair') chair(c, g, suit);
  else if (pose === 'back') back(c, g, suit);
  else {
    const L = armPose(pose, -1, bp, tq), R = pose === 'cap' && o.hand ? bend(o.hand) : armPose(pose, 1, bp, tq);
    const step = pose === 'walk' ? Math.sin(tq * 7) * 24 : 0, wide = pose === 'burst' || pose === 'stamp' ? 14 : 0;
    // legs (wide trousers) and shoes
    for (const sx of [-1, 1]) {
      const foot: P2 = [sx * (30 + wide) - sx * step, 290];
      limb(c, [[sx * 24, 126], foot], 40, suit);
      c.beginPath(); c.ellipse(foot[0] + sx * 8, foot[1] + 8, 22, 10, 0, 0, TAU); shape(c, C.black, 0);
    }
    if (pose === 'sing') tether(c, R[1], [90, 320]);
    c.beginPath(); c.rect(-11, -68, 22, 26); shape(c, C.paper, 2.5); // neck
    jacket(c, g, { c0: -46, hem: 132, sw: 80, drop: 22, wy: 62, ww: 62, hw: 72, suit, props: !o.dancer, pad: 70 });
    c.save(); c.translate(0, -118); c.rotate(pose === 'sing' ? (bp < 0.5 ? 0.05 : -0.03) : pose === 'reach' ? 0.07 : 0);
    head(c, faceState(t, pose, o));
    c.restore();
    for (const [sx, [e, h]] of [[-1, L], [1, R]] as const) {
      const sh: P2 = [sx * 112, -30]; // sleeves hang from the pads
      limb(c, [sh, [e[0] + jit(g, 10 + sx), e[1]], h], 24, suit);
      c.beginPath(); c.arc(h[0], h[1], 11, 0, TAU); shape(c, C.paper, 2.5);
    }
    if (pose === 'sing') mic(c, R[1], [R[1][0] - 8, R[1][1] - 24]);
    if (pose === 'stamp' && !o.dancer) { // the rubber stamp in both fists
      const hy = L[1][1];
      c.beginPath(); c.rect(-12, hy - 34, 24, 26); shape(c, C.black, 0);
      c.beginPath(); c.rect(-40, hy - 8, 80, 18); shape(c, C.orange, 3);
    }
  }
  c.restore();
  K = C.black;
}

/** Close-up for the lip-synced lines: head and shoulders, face centre at (x, y), face height 112·s. */
export function idolBust(c: Ctx, x: number, y: number, s: number, t: number, o: IdolOpts & { mic?: boolean; tilt?: number } = {}) {
  const g = gen(t), bp = o.beat ?? 0;
  K = o.key ?? C.black;
  c.save(); c.translate(x, y + Math.round(Math.sin(bp * TAU) * 3) * s); c.scale(o.flip ? -s : s, s);
  c.lineJoin = 'round'; c.lineCap = 'round';
  c.beginPath(); c.rect(-12, 48, 24, 34); shape(c, C.paper, 2.5); // neck
  const suit = o.suit ?? C.blue;
  jacket(c, g, { c0: 74, hem: 520, sw: 150, drop: 84, wy: 420, ww: 158, hw: 166, seams: true, suit, props: !o.dancer, pad: 50 });
  c.save(); c.rotate((o.tilt ?? 0) + (bp < 0.5 ? 0.03 : -0.02));
  head(c, faceState(t, 'bust', o));
  c.restore();
  if (o.mic !== false) { // mic held low, clear of the mouth
    const hand: P2 = [58, 170];
    limb(c, [[150, 330], [96, 250], hand], 26, suit);
    c.beginPath(); c.arc(hand[0], hand[1], 13, 0, TAU); shape(c, C.paper, 2.5);
    mic(c, hand, [44, 104], 12);
  }
  c.restore();
  K = C.black;
}

// ------------------------------------------------------------------ special poses
/** Europe in a Chair: on a folding chair, knees up, face buried in her arms. */
function chair(c: Ctx, g: number, suit: string) {
  const fr = (pts: P2[], w: number) => seg(c, pts, w, K);
  fr([[-56, 70], [-44, -70]], 7); fr([[56, 70], [44, -70]], 7); fr([[-46, -52], [46, -52]], 14); // backrest
  c.beginPath(); c.moveTo(-70, 60); c.lineTo(-68, -60); c.quadraticCurveTo(0, -84, 68, -60); c.lineTo(70, 60); c.closePath(); shape(c, suit); // back, hunched
  fr([[-60, 70], [70, 250]], 7); fr([[60, 70], [-70, 250]], 7); fr([[-74, 72], [74, 72]], 9); // seat and crossed legs
  for (const sx of [-1, 1]) { // shins up from the seat, shoes on its edge, knees under her head
    limb(c, [[sx * 26, -30], [sx * 30, 60]], 36, suit);
    c.beginPath(); c.ellipse(sx * 34, 68, 24, 11, 0, 0, TAU); shape(c, C.black, K === C.black ? 0 : 2);
  }
  c.save(); c.translate(jit(g, 1), -62 + jit(g, 2)); // head down on the knees: only the bob shows
  c.beginPath(); c.moveTo(-62, 26); c.quadraticCurveTo(-70, -60, 0, -60); c.quadraticCurveTo(70, -60, 62, 26); c.quadraticCurveTo(0, 36, -62, 26); c.closePath();
  shape(c, C.black, K === C.black ? 0 : 3);
  c.strokeStyle = C.paper; c.lineWidth = 4; c.beginPath(); c.arc(0, -6, 46, -2.5, -1.95); c.stroke();
  c.restore();
  c.save(); c.translate(jit(g, 8, 0.8), jit(g, 9, 0.8)); // forearms wrapped round the shins, crossing
  limb(c, [[-72, -56], [-66, 14], [18, 22]], 24, suit);
  limb(c, [[72, -56], [66, 8], [-16, 12]], 24, suit);
  c.beginPath(); c.arc(22, 22, 11, 0, TAU); shape(c, C.paper, 2.5);
  c.beginPath(); c.arc(-20, 12, 11, 0, TAU); shape(c, C.paper, 2.5);
  c.restore();
}

/** From behind (the Wanderer). */
function back(c: Ctx, g: number, suit: string) {
  for (const sx of [-1, 1]) { limb(c, [[sx * 24, 126], [sx * 34, 290]], 40, suit); c.beginPath(); c.ellipse(sx * 38, 298, 22, 10, 0, 0, TAU); shape(c, C.black, 0); }
  // the jacket's collar rises to meet the bob, so nothing behind her shows through at the neck; the pads, from behind
  for (const sx of [-1, 1]) { c.beginPath(); c.moveTo(sx * 30, -56); c.lineTo(sx * 150, -76); c.lineTo(sx * 129, 4); c.lineTo(sx * 64, 14); c.closePath(); shape(c, suit); }
  c.beginPath(); c.moveTo(-80, -26); c.lineTo(-56, -60); c.quadraticCurveTo(0, -74, 56, -60); c.lineTo(80, -26); c.lineTo(72, 132); c.lineTo(-72, 132); c.closePath(); shape(c, suit);
  for (const sx of [-1, 1]) limb(c, [[sx * 112, -30], [sx * 118, 50], [sx * 96, 116]], 24, suit);
  c.save(); c.translate(jit(g, 1), -118 + jit(g, 2));
  bobPath(c); c.quadraticCurveTo(0, 54, -66, 46); c.closePath(); shape(c, C.black, 0);
  c.strokeStyle = C.paper; c.lineWidth = 4; c.beginPath(); c.arc(0, -26, 48, -2.45, -1.95); c.stroke(); // shine
  c.restore();
}
