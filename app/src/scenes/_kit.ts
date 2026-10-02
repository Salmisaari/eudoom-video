// Shared drawing kit for EU Edition plates: images, the Twelve,
// the split-flap DELAY board, stamps, caption slips and karaoke typography.
// Everything draws in logical 1920x1080 px with palette colours only (the print pass does the rest).
import { C, ink } from '../engine/palette';
import { F, font } from '../engine/type';
import type { Lyrics, Line, Word } from '../engine/lyrics';
import { clamp, ease } from '../engine/util';

export const W = 1920, H = 1080;
export type Ctx = CanvasRenderingContext2D;

// ------------------------------------------------------------------ images
const imgCache = new Map<string, HTMLImageElement>();
export function loadImage(src: string) {
  return new Promise<HTMLImageElement>((res, rej) => {
    const i = new Image();
    i.onload = () => { imgCache.set(src, i); res(i); };
    i.onerror = () => rej(new Error('image failed: ' + src));
    i.src = src;
  });
}
export const img = (src: string) => imgCache.get(src);

export type Treat = 'line' | 'photo' | 'color';
export const FILTER: Record<Treat, string> = {
  line: 'grayscale(1) brightness(1.12) contrast(3.2)', // engravings print as solid line art
  photo: 'grayscale(1) brightness(1.18) contrast(1.3)', // photos are screened in black
  color: 'brightness(1.32) contrast(1.22) saturate(1.45)', // paintings are separated into the four inks
};

/** Draw image `im` so that its (u,v) centre point lands at (x,y) with scale s (px per image px), rotation r. */
export function drawImageAt(c: Ctx, im: HTMLImageElement, x: number, y: number, s: number, treat: Treat, rot = 0, u = 0.5, v = 0.5) {
  c.save();
  c.translate(x, y); c.rotate(rot); c.scale(s, s);
  c.filter = FILTER[treat];
  c.drawImage(im, -u * im.width, -v * im.height);
  c.filter = 'none';
  c.restore();
}

/** Scale that makes the image cover (or fit inside) a w x h box. */
export const coverScale = (im: HTMLImageElement, w: number, h: number) => Math.max(w / im.width, h / im.height);
export const fitScale = (im: HTMLImageElement, w: number, h: number) => Math.min(w / im.width, h / im.height);

// ------------------------------------------------------------------ type helpers
export function setFont(c: Ctx, fam: string, px: number) { c.font = font(fam, px); }
export function textW(c: Ctx, s: string) { return c.measureText(s).width; }

/** Fit a single-line string to width by choosing a size (<= max). */
export function fitSize(c: Ctx, fam: string, s: string, w: number, max: number, min = 10) {
  setFont(c, fam, 100);
  const k = w / Math.max(1, textW(c, s));
  return clamp(100 * k, min, max);
}

/** Greedy wrap of words into lines at a given font. */
export function wrap(c: Ctx, words: string[], maxW: number) {
  const lines: string[][] = [];
  let cur: string[] = [];
  for (const w of words) {
    const test = [...cur, w].join(' ');
    if (cur.length && textW(c, test) > maxW) { lines.push(cur); cur = [w]; } else cur.push(w);
  }
  if (cur.length) lines.push(cur);
  return lines;
}

// ------------------------------------------------------------------ karaoke
/** The line being sung around t (with an early show window), for display. */
export function lineFor(ly: Lyrics, t: number, early = 0.35): Line | null {
  let best: Line | null = null;
  for (const l of ly.lines) if (t >= l.start - early) best = l;
  if (!best) return null;
  const idx = ly.lines.indexOf(best);
  const next = ly.lines[idx + 1];
  const lastEnd = best.words[best.words.length - 1]!.end;
  if (!next && t > lastEnd + 1.2) return null;
  return best;
}
export const wordProg = (w: Word, t: number) => clamp((t - w.start) / Math.max(0.05, w.end - w.start), 0, 1);

/**
 * Poster lyric: the whole line printed large in a column, each word highlighted with a yellow
 * marker stroke from its sung start to its end. Words not yet sung print in full ink already
 * (it is a printed poster); the highlighter is the karaoke.
 */
export function posterLyric(c: Ctx, line: Line, t: number, x: number, y: number, w: number, o: { fam?: string; size?: number; color?: string; lead?: number; upper?: boolean; hl?: string; hide?: boolean } = {}) {
  const fam = o.fam ?? F.archivo(75, 900);
  const words = line.words.map((wd) => (o.upper === false ? wd.w : wd.w.toUpperCase()));
  let size = o.size ?? 118;
  setFont(c, fam, size);
  let rows = wrap(c, words, w);
  // shrink until it fits 4 rows and no single word (e.g. POST-CHINCHILLA,) runs past the column
  const widest = () => Math.max(...words.map((s) => textW(c, s)));
  while ((rows.length > 4 || widest() > w) && size > 50) { size -= 6; setFont(c, fam, size); rows = wrap(c, words, w); }
  const lead = (o.lead ?? 0.98) * size;
  let wi = 0;
  const hl = o.hl ?? C.yellow;
  c.textBaseline = 'alphabetic';
  rows.forEach((row, ri) => {
    let cx = x;
    const by = y + ri * lead;
    for (const s of row) {
      const wd = line.words[wi++]!;
      const ww = textW(c, s);
      const p = wordProg(wd, t);
      const visible = !o.hide || t >= wd.start - 0.02;
      if (p > 0) {
        // marker stroke: slightly slanted band behind the word, drawn left to right
        c.save();
        c.globalCompositeOperation = 'multiply';
        c.fillStyle = hl;
        const x0 = cx - size * 0.06, x1 = cx + (ww + size * 0.12) * p;
        c.beginPath();
        c.moveTo(x0, by - size * 0.74); c.lineTo(x1, by - size * 0.78); c.lineTo(x1 + 3, by + size * 0.1); c.lineTo(x0 - 2, by + size * 0.14);
        c.closePath(); c.fill();
        c.restore();
      }
      if (visible) { c.fillStyle = o.color ?? C.black; c.fillText(s, cx, by); }
      cx += ww + size * 0.26;
    }
  });
  return { size, rows: rows.length, lead };
}

/** Slam lyric: only the most recently sung word, huge; earlier words of the line stack small above. */
export function slamLyric(c: Ctx, line: Line, t: number, o: { x?: number; y?: number; w?: number; color?: string; fam?: string; max?: number } = {}) {
  const fam = o.fam ?? F.archivo(62, 900);
  let cur = -1;
  line.words.forEach((wd, i) => { if (t >= wd.start - 0.01) cur = i; });
  if (cur < 0) return;
  const word = line.words[cur]!.w.toUpperCase();
  const x = o.x ?? 90, w = o.w ?? 1740;
  const size = Math.min(o.max ?? 560, fitSize(c, fam, word, w, o.max ?? 560));
  setFont(c, fam, size);
  c.fillStyle = o.color ?? C.black;
  c.textBaseline = 'alphabetic';
  // hit: first 3 frames 6% larger (a stamp pressing), then settle
  const dt = t - line.words[cur]!.start;
  const k = dt < 0.05 ? 1.06 : 1;
  c.save();
  const y = o.y ?? 760;
  c.translate(x, y); c.scale(k, k);
  c.fillText(word, 0, 0);
  c.restore();
  // the sung-so-far line, small, typewriter, above
  setFont(c, F.typewriter(700), 34);
  c.fillStyle = o.color ?? C.black;
  const sofar = line.words.slice(0, cur + 1).map((w) => w.w).join(' ');
  c.fillText(sofar, x + 6, (o.y ?? 760) - size * 0.82 - 24);
}

/** Subtitle slip: typewritten on a paper strip at the bottom, words highlighted as sung. */
export function slipLyric(c: Ctx, line: Line, t: number, o: { y?: number; size?: number } = {}) {
  const size = o.size ?? 44;
  setFont(c, F.typewriter(700), size);
  const text = line.words.map((w) => w.w).join(' ');
  const tw = textW(c, text);
  const pad = 26, x = (W - tw) / 2, y = o.y ?? 1000;
  c.save();
  c.translate(W / 2, y - size * 0.35); c.rotate(-0.006); c.translate(-W / 2, -(y - size * 0.35));
  c.fillStyle = C.paper;
  c.fillRect(x - pad, y - size - 14, tw + pad * 2, size + 34);
  c.strokeStyle = C.black; c.lineWidth = 2; c.strokeRect(x - pad, y - size - 14, tw + pad * 2, size + 34);
  let cx = x;
  for (const wd of line.words) {
    const ww = textW(c, wd.w);
    const p = wordProg(wd, t);
    if (p > 0) {
      c.save(); c.globalCompositeOperation = 'multiply'; c.fillStyle = C.yellow;
      c.fillRect(cx - 4, y - size * 0.8, (ww + 8) * p, size * 0.98); c.restore();
    }
    c.fillStyle = C.black; c.fillText(wd.w, cx, y);
    cx += ww + textW(c, ' ');
  }
  c.restore();
}

// ------------------------------------------------------------------ props
/** Caption slip: typewritten source line(s), taped at an angle. */
export function captionSlip(c: Ctx, lines: string[], x: number, y: number, o: { size?: number; rot?: number; w?: number } = {}) {
  // bold and a size up: thin 20 px type broke up in the print pass
  const size = (o.size ?? 22) * 1.2;
  setFont(c, F.typewriter(700), size);
  lines = lines.flatMap((l) => wrap(c, l.split(' '), 1300).map((ws) => ws.join(' ')));
  const w = o.w ?? Math.max(...lines.map((l) => textW(c, l))) + 36;
  const h = lines.length * size * 1.3 + 26;
  x = Math.min(x, W - 30 - w); // long slips slide left rather than run off the frame
  y = Math.min(y, H - 24 - h); // and up rather than off the bottom
  c.save(); c.translate(x, y); c.rotate(o.rot ?? 0.012);
  c.fillStyle = ink({ black: 0.3 }); c.fillRect(6, 7, w, h);
  c.fillStyle = C.paper; c.fillRect(0, 0, w, h);
  c.strokeStyle = C.black; c.lineWidth = 1.5; c.strokeRect(0, 0, w, h);
  c.fillStyle = C.black;
  lines.forEach((l, i) => c.fillText(l, 18, 20 + size + i * size * 1.3 - 4));
  // tape
  c.fillStyle = ink({ yellow: 0.45 }); c.fillRect(w * 0.42, -12, 90, 26);
  c.restore();
}

/** Rubber stamp: double-ruled box, rotated, in one ink. `k` 0..1 = how far it has landed. */
export function stamp(c: Ctx, text: string, x: number, y: number, o: { sub?: string; rot?: number; color?: string; size?: number; k?: number } = {}) {
  const size = o.size ?? 90;
  const k = o.k ?? 1;
  if (k <= 0) return;
  setFont(c, F.sign(700), size);
  const tw = textW(c, text);
  setFont(c, F.sign(600), size * 0.42);
  const sw = o.sub ? textW(c, o.sub) : 0;
  const bw = Math.max(tw, sw) + size * 0.8, bh = size * (o.sub ? 1.7 : 1.25);
  const s = k < 1 ? 1.25 - 0.25 * ease.outCubic(k) : 1;
  c.save(); c.translate(x, y); c.rotate(o.rot ?? -0.12); c.scale(s, s);
  c.globalAlpha = k < 1 ? k : 1;
  const col = o.color ?? C.orange;
  c.strokeStyle = col; c.fillStyle = col;
  c.lineWidth = size * 0.11; c.strokeRect(-bw / 2, -bh / 2, bw, bh);
  c.lineWidth = size * 0.04; c.strokeRect(-bw / 2 + size * 0.16, -bh / 2 + size * 0.16, bw - size * 0.32, bh - size * 0.32);
  c.textAlign = 'center'; c.textBaseline = 'alphabetic';
  setFont(c, F.sign(700), size);
  c.fillText(text, 0, o.sub ? -size * 0.02 : size * 0.34);
  if (o.sub) { setFont(c, F.sign(600), size * 0.42); c.fillText(o.sub, 0, size * 0.5); }
  c.restore();
}

/**
 * Split-flap board: rows of cells; a changed cell flips through random glyphs for a few frames
 * (the accelerating world's clock) before settling. `rows` are strings; `since` when they last changed.
 */
export function flapBoard(c: Ctx, x: number, y: number, rows: string[], t: number, o: { cell?: number; since?: number; cols?: number; ink?: string; title?: string } = {}) {
  const cw = o.cell ?? 44, ch = cw * 1.42, gap = cw * 0.1;
  const cols = o.cols ?? Math.max(...rows.map((r) => r.length));
  const bg = o.ink ?? C.black;
  const bw = cols * (cw + gap) + gap * 3, bh = rows.length * (ch + gap) + gap * 3 + (o.title ? ch * 0.7 : 0);
  c.fillStyle = bg; c.fillRect(x, y, bw, bh);
  let oy = y + gap * 2;
  if (o.title) {
    setFont(c, F.sign(700), ch * 0.5); c.fillStyle = C.yellow; c.textBaseline = 'alphabetic';
    c.fillText(o.title, x + gap * 2, oy + ch * 0.5); oy += ch * 0.7;
  }
  const GL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-:·';
  setFont(c, F.sign(700), ch * 0.82);
  c.textAlign = 'center'; c.textBaseline = 'alphabetic';
  rows.forEach((r, ri) => {
    for (let ci = 0; ci < cols; ci++) {
      const cx = x + gap * 2 + ci * (cw + gap), cy = oy + ri * (ch + gap);
      c.fillStyle = ink({ black: 1, blue: 0.35 }); c.fillRect(cx, cy, cw, ch);
      c.fillStyle = bg; c.fillRect(cx, cy + ch / 2 - 1.5, cw, 3); // the hinge
      let g = r[ci] ?? ' ';
      const since = o.since ?? -9;
      const settle = since + 0.05 + ci * 0.022 + ri * 0.05;
      if (t >= since && t < settle) g = GL[Math.floor((t * 60 + ci * 7 + ri * 3) % GL.length)]!;
      c.fillStyle = C.paper;
      c.fillText(g, cx + cw / 2, cy + ch * 0.82);
    }
  });
  c.textAlign = 'left';
  return { w: bw, h: bh };
}

// ------------------------------------------------------------------ the idol (drawn in _idol.ts)
import { idol } from './_idol';
export { idol, idolBust, MouthChart, type Pose, type Viseme } from './_idol';

/** The Twelve: yellow dancers. Ring (from above, as stars) or a row. */
export function twelve(c: Ctx, cx: number, cy: number, r: number, t: number, o: { ring?: boolean; beat?: number; scale?: number } = {}) {
  const s = o.scale ?? 1;
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2 - Math.PI / 2;
    const x = o.ring ? cx + Math.cos(a) * r : cx - r + (i / 11) * r * 2;
    const y = o.ring ? cy + Math.sin(a) * r : cy;
    c.fillStyle = C.yellow;
    if (o.ring) { // top-down: a five-pointed star per dancer
      c.beginPath();
      for (let k = 0; k < 10; k++) {
        const rr = (k % 2 ? 0.42 : 1) * 30 * s, aa = (k / 10) * Math.PI * 2 - Math.PI / 2;
        c.lineTo(x + Math.cos(aa) * rr, y + Math.sin(aa) * rr);
      }
      c.closePath(); c.fill();
    } else { // the idol's rig in yellow, doing the point move in unison; feet at y + 70·s
      const sd = 0.34 * s;
      idol(c, x, y + 70 * s - 300 * sd, sd, 'stamp', t, { beat: o.beat, suit: C.yellow, dancer: true, vis: 'X' });
    }
  }
}

/** A sheet of paper with a drop shadow (a tint, as a photocopied edge would print). */
export function sheet(c: Ctx, x: number, y: number, w: number, h: number, rot = 0, col: string = C.paper) {
  c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(rot);
  c.fillStyle = ink({ black: 0.3 }); c.fillRect(-w / 2 + 10, -h / 2 + 12, w, h);
  c.fillStyle = col; c.fillRect(-w / 2, -h / 2, w, h);
  c.restore();
}
