// Kinetic-type kit for the type edition (typo.ts). Every word appears on the frame its sung onset falls in
// (data/timing_eu.json: analysis/timing_eu.py), held vowels multiply for as long as the note holds, baselines follow
// the sung pitch, and the drums move the paper (kick: the platen presses, snare: the sheet flips, hat: the type jitters).
// Europe's own clock (the background type) runs at a stepped rate that speeds up through the song: 6 fps in
// verse 1, 60 fps in the last chorus.
import { C, ink } from '../engine/palette';
import { F, font, layout } from '../engine/type';
import { clamp, ease, hash } from '../engine/util';

export const W = 1920, H = 1080;
export type Ctx = CanvasRenderingContext2D;

export interface KWord {
  w: string; start: number; end: number;
  syl: [string, number, number][];
  notes: [number, number, number, number][];
  hold?: [number, number, number];
  peak?: number | null;
  li: number; wi: number;
}
export interface KLine { n: number; text: string; orig: string; eu: boolean; start: number; end: number; words: KWord[] }
export interface Timing {
  duration: number; bpm: number; beats: number[]; downbeats: number[];
  sections: { name: string; start: number; end: number }[];
  onsets: Record<string, [number, number][]>;
  lines: KLine[];
  notes: [number, number, number, number][];
}

export async function loadTiming(): Promise<Timing> {
  const j = await (await fetch('data/timing_eu.json')).json();
  j.lines.forEach((l: KLine, li: number) => l.words.forEach((w, wi) => { w.li = li; w.wi = wi; }));
  return j;
}

// ------------------------------------------------------------------ time
/** Half a 60 fps frame: a word shows on the first frame whose time is within half a frame of its onset. */
export const HALF = 1 / 120;
export const shown = (w: { start: number }, t: number) => t >= w.start - HALF;
export const age = (w: { start: number }, t: number) => t - w.start;
/** Sung progress through a word, 0..1. */
export const sung = (w: KWord, t: number) => clamp((t - w.start) / Math.max(0.05, w.end - w.start));
/** Stepped time on a clock of `fps` generations per second (Europe's clock). */
export const step = (t: number, fps: number) => Math.floor(t * fps + 1e-6) / fps;
/** Press: the platen meets the paper on the onset frame and lets go over ~5 frames (1 -> 0). */
export const press = (a: number, k = 26) => (a < -HALF ? 0 : Math.exp(-Math.max(0, a) * k));
/** A 16th note at the song's tempo (132 bpm). */
export const S16 = 60 / 132.007 / 4;

// ------------------------------------------------------------------ Europe's clock
/** Europe's frame rate per section: it speeds up through the song (and stops for August). */
export const EU_FPS: Record<string, number> = {
  intro: 6, verse1: 6, pre1: 8, chorus1: 10, break1: 10, verse2: 12, pre2: 12, chorus2: 15, verse3: 20, pre3: 20,
  chorus3: 2, bridge: 30, chorus4: 60, outro: 60,
};

// ------------------------------------------------------------------ the band
export class Band {
  constructor(public T: Timing) {}
  section(t: number) { return this.T.sections.find((s) => t >= s.start && t < s.end) ?? this.T.sections[this.T.sections.length - 1]!; }
  euFps(t: number) { return EU_FPS[this.section(t).name] ?? 12; }
  /** Europe's stepped time at t. */
  eu(t: number) { return step(t, this.euFps(t)); }
  beatAt(t: number) {
    const b = this.T.beats;
    if (t <= b[0]!) return (t - b[0]!) / (b[1]! - b[0]!);
    if (t >= b[b.length - 1]!) return b.length - 1 + (t - b[b.length - 1]!) / (b[b.length - 1]! - b[b.length - 2]!);
    let lo = 0, hi = b.length - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (b[m]! <= t) lo = m; else hi = m; }
    return lo + (t - b[lo]!) / (b[hi]! - b[lo]!);
  }
  timeOfBeat(i: number) {
    const b = this.T.beats, n = b.length, p = (b[n - 1]! - b[0]!) / (n - 1);
    if (i <= 0) return b[0]! + i * p;
    if (i >= n - 1) return b[n - 1]! + (i - n + 1) * p;
    const k = Math.floor(i); return b[k]! + (b[k + 1]! - b[k]!) * (i - k);
  }
  /** The last onset of a kind at or before t: [time, strength] (or null). */
  last(kind: string, t: number): [number, number] | null {
    const l = this.T.onsets[kind]; if (!l?.length) return null;
    let lo = 0, hi = l.length;
    while (lo < hi) { const m = (lo + hi) >> 1; if (l[m]![0] <= t + HALF) lo = m + 1; else hi = m; }
    return lo ? l[lo - 1]! : null;
  }
  /** Decaying pulse of the last onset of a kind (1 on the hit frame). */
  pulse(kind: string, t: number, half = 0.09) {
    const o = this.last(kind, t); if (!o) return 0;
    return o[1] * Math.pow(0.5, Math.max(0, t - o[0]) / half);
  }
  count(kind: string, t: number) {
    const l = this.T.onsets[kind] ?? []; let n = 0; for (const [x] of l) if (x <= t + HALF) n++; else break; return n;
  }
  /** Sung pitch (MIDI) at t, from the vocal's notes (NaN between notes). */
  pitch(t: number) {
    for (const [m, a, b] of this.T.notes) if (t >= a && t < b) return m;
    return NaN;
  }
}

// ------------------------------------------------------------------ words that sing
const VOWEL = /[AEIOUYÄÖÜaeiouyäöü]/;
/**
 * The word as it sounds at t: while its held note sounds, the held syllable's vowel repeats once per 16th note
 * (DOOOOOM), up to `max` extra letters; the letters stay once the note is over.
 */
export function sungText(w: KWord, _t: number, _max = 6, upper = true): string {
  // the word as written, always (2026-10-01: no repeated letters for held notes; holds are shown by motion, holdOpen)
  return upper ? w.w.toUpperCase() : w.w;
}
/** How far a held note has opened the word, 0..1: the tracking widens over the hold and closes over 0.25 s after. */
export function holdOpen(w: KWord, t: number): number {
  if (!w.hold || w.hold[1] - w.hold[0] < 0.45 || t < w.hold[0]) return 0;
  const [h0, h1] = w.hold;
  if (t <= h1) return ease.outCubic(clamp((t - h0) / (h1 - h0)));
  return 1 - ease.inOutCubic(clamp((t - h1) / 0.25));
}
/** Letter spacing for a word at size px (a held note opens it up to 14 % of the size). Set it before measuring. */
export function track(c: Ctx, w: KWord | undefined, t: number, px: number, amt = 0.14) {
  const k = w ? holdOpen(w, t) : 0;
  c.letterSpacing = `${(px * amt * k).toFixed(2)}px`;
  return k;
}
/** Progress through the word's held note (0 before, 1 after). */
export const holdP = (w: KWord, t: number) => (w.hold ? clamp((t - w.hold[0]) / Math.max(0.05, w.hold[1] - w.hold[0])) : sung(w, t));

/** Words of a line shown at t. */
export const shownWords = (l: KLine, t: number) => l.words.filter((w) => shown(w, t));
/** The word being (or last) sung in a line at t, or null before its first word. */
export function current(l: KLine, t: number): KWord | null {
  let c: KWord | null = null;
  for (const w of l.words) if (shown(w, t)) c = w;
  return c;
}

// ------------------------------------------------------------------ type setting
export function setF(c: Ctx, fam: string, px: number) { c.font = font(fam, px); }
export function tw(c: Ctx, s: string) { return c.measureText(s).width; }
/** Size (px) at which `s` in `fam` is exactly `w` wide. */
export function sizeFor(c: Ctx, fam: string, s: string, w: number) { setF(c, fam, 100); return (100 * w) / Math.max(1, tw(c, s)); }

/** Archivo family for a 0..1 weight and 0..1 width (static instances: 6 widths x 4 weights). */
export const arch = (wt: number, wd = 0.5) => F.archivo(62 + clamp(wd) * 63, 300 + clamp(wt) * 600);

/** Draw text with its cap height centred on y (alphabetic baseline at y + 0.36 size). */
export function textMid(c: Ctx, s: string, x: number, y: number, px: number) { c.fillText(s, x, y + px * 0.36); }

/**
 * Glyph-by-glyph run with per-letter transforms: fn(i, ch) -> { dx, dy, s, r, col } (all optional).
 * Returns the advance width.
 */
export function glyphs(c: Ctx, s: string, x: number, y: number, fam: string, px: number,
  fn?: (i: number, ch: string) => { dx?: number; dy?: number; s?: number; sx?: number; r?: number; col?: string; skip?: boolean } | void, track = 0) {
  const L = layout(s, fam, px, track);
  setF(c, fam, px);
  for (const g of L.glyphs) {
    const o = fn?.(g.i, g.ch) || {};
    if (o.skip) continue;
    c.save();
    c.translate(x + g.x + g.w / 2 + (o.dx ?? 0), y + (o.dy ?? 0));
    if (o.r) c.rotate(o.r);
    const k = o.s ?? 1; c.scale(k * (o.sx ?? 1), k);
    if (o.col) c.fillStyle = o.col;
    c.fillText(g.ch, -g.w / 2, 0);
    c.restore();
  }
  return L.width;
}

/** A band of type exactly `w` wide at baseline y (size from the width), optionally squeezed to height h. Returns size. */
export function band(c: Ctx, s: string, x: number, y: number, w: number, fam: string, o: { h?: number; col?: string; align?: 'left' | 'center' } = {}) {
  const px = sizeFor(c, fam, s, w);
  setF(c, fam, px);
  c.fillStyle = o.col ?? C.black;
  if (o.h && o.h < px * 0.74) { // squeeze vertically to a cap height of h
    c.save(); c.translate(x, y); c.scale(1, o.h / (px * 0.74)); c.fillText(s, 0, 0); c.restore();
  } else c.fillText(s, x, y);
  return px;
}

// ------------------------------------------------------------------ marks
/** Strike-through (EU amendment style: deleted text). */
export function strike(c: Ctx, x0: number, x1: number, y: number, lw: number, col = C.orange) {
  c.fillStyle = col; c.fillRect(x0, y - lw / 2, x1 - x0, lw);
}
/** Redaction bar. */
export function redact(c: Ctx, x: number, y: number, w: number, h: number, k = 1) { c.fillStyle = C.black; c.fillRect(x, y, w * clamp(k), h); }
/** Highlighter stroke behind text (multiply). */
export function marker(c: Ctx, x: number, y: number, w: number, h: number, k = 1, col = C.yellow) {
  if (k <= 0) return;
  c.save(); c.globalCompositeOperation = 'multiply'; c.fillStyle = col;
  c.beginPath(); c.moveTo(x, y + h * 0.06); c.lineTo(x + w * k, y); c.lineTo(x + w * k + 3, y + h); c.lineTo(x - 2, y + h * 1.04); c.closePath(); c.fill();
  c.restore();
}
/** Overprint: draw fn with multiply (two inks make a third). */
export function over(c: Ctx, fn: () => void) { c.save(); c.globalCompositeOperation = 'multiply'; fn(); c.restore(); }

/** Rubber stamp in one ink (k: 0..1 landing). */
export function stampK(c: Ctx, text: string, x: number, y: number, px: number, col: string, rot = -0.1, k = 1, sub?: string) {
  if (k <= 0) return;
  setF(c, F.sign(700), px);
  const w0 = tw(c, text); setF(c, F.sign(600), px * 0.4); const w1 = sub ? tw(c, sub) : 0;
  const bw = Math.max(w0, w1) + px * 0.7, bh = px * (sub ? 1.6 : 1.2);
  const s = k < 1 ? 1.3 - 0.3 * ease.outCubic(k) : 1;
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s);
  over(c, () => {
    c.strokeStyle = col; c.fillStyle = col;
    c.lineWidth = px * 0.1; c.strokeRect(-bw / 2, -bh / 2, bw, bh);
    c.lineWidth = px * 0.035; c.strokeRect(-bw / 2 + px * 0.15, -bh / 2 + px * 0.15, bw - px * 0.3, bh - px * 0.3);
    c.textAlign = 'center';
    setF(c, F.sign(700), px); c.fillText(text, 0, sub ? -px * 0.02 : px * 0.34);
    if (sub) { setF(c, F.sign(600), px * 0.4); c.fillText(sub, 0, px * 0.48); }
    c.textAlign = 'left';
  });
  c.restore();
}

/** Typewritten note on a paper slip (marginalia: sources, dates, article numbers). */
export function slip(c: Ctx, lines: string[], x: number, y: number, px = 22, rot = 0.01, o: { bg?: string; fg?: string; n?: number } = {}) {
  setF(c, F.typewriter(700), px);
  const n = o.n ?? 1e9; // characters typed so far
  let left = n;
  const shownL = lines.map((l) => { const s = l.slice(0, Math.max(0, left)); left -= l.length; return s; });
  const w = Math.max(...lines.map((l) => tw(c, l))) + px * 1.4, h = lines.length * px * 1.3 + px * 0.9;
  c.save(); c.translate(x, y); c.rotate(rot);
  c.fillStyle = ink({ black: 0.3 }); c.fillRect(5, 6, w, h);
  c.fillStyle = o.bg ?? C.paper; c.fillRect(0, 0, w, h);
  c.fillStyle = o.fg ?? C.black;
  shownL.forEach((l, i) => c.fillText(l, px * 0.7, px * 1.25 + i * px * 1.3));
  c.restore();
  return { w, h };
}

// ------------------------------------------------------------------ textures (pre-rendered once)
const texCache = new Map<string, HTMLCanvasElement>();
/** A pre-rendered canvas (built once by `draw`), for walls of small type that would be slow to set every frame. */
export function tex(key: string, w: number, h: number, draw: (k: Ctx) => void) {
  let cv = texCache.get(key);
  if (!cv) {
    cv = document.createElement('canvas'); cv.width = w; cv.height = h;
    draw(cv.getContext('2d')!);
    texCache.set(key, cv);
  }
  return cv;
}
/** Wrap words to a column width. */
export function wrapTo(c: Ctx, text: string, w: number) {
  const out: string[] = []; let cur = '';
  for (const word of text.split(/\s+/)) {
    const tst = cur ? cur + ' ' + word : word;
    if (cur && tw(c, tst) > w) { out.push(cur); cur = word; } else cur = tst;
  }
  if (cur) out.push(cur);
  return out;
}
/** Draw a texture tiled vertically, scrolled by `dy` px (wraps). */
export function scrollTex(c: Ctx, cv: HTMLCanvasElement, x: number, y: number, h: number, dy: number) {
  const th = cv.height, o = ((dy % th) + th) % th;
  c.save(); c.beginPath(); c.rect(x, y, cv.width, h); c.clip();
  for (let yy = y - o; yy < y + h; yy += th) c.drawImage(cv, x, yy);
  c.restore();
}

// ------------------------------------------------------------------ misc
export const rnd = (...k: number[]) => hash(...k);
export function fill(c: Ctx, col: string) { c.fillStyle = col; c.fillRect(-60, -60, W + 120, H + 120); }
