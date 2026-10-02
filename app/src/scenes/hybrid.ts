// The story cut (animatic.ts: every line's researched plate) with its lyrics set kinetically: no line is printed
// before it is sung. Each word rises out of its slot on the frame it is sung (data/timing_eu.json), is pressed in,
// holds its vowel for as long as the note, and the highlighter follows the voice; the typewritten slips type
// themselves a syllable at a time.
import Animatic from './animatic';
import { C } from '../engine/palette';
import type { Line } from '../engine/lyrics';
import { clamp, ease } from '../engine/util';
import { type Timing, type KLine, loadTiming, shown, age, sung, press, sungText, setF, tw, arch, HALF, W } from './_kin';
import { F } from '../engine/type';

type Ctx = CanvasRenderingContext2D;

/** Highlighter band behind a word (source-over: over a multiplied flood a multiplied marker went black). */
function marker(c: Ctx, x: number, y: number, w: number, h: number, k: number, col: string = C.yellow) {
  if (k <= 0) return;
  c.fillStyle = col;
  c.beginPath(); c.moveTo(x, y + h * 0.06); c.lineTo(x + w * k, y); c.lineTo(x + w * k + 3, y + h); c.lineTo(x - 2, y + h * 1.04); c.closePath(); c.fill();
}

export default class Hybrid extends Animatic {
  T!: Timing;

  override async init() {
    await super.init();
    this.T = await loadTiming();
  }

  /** The line to set at t: the story cut shows the next line 0.35 s early (its poster was printed in advance); here
   *  the last line keeps the page while its last word still sounds, then the page is bare until the next first word. */
  kline(line: Line, t: number): KLine | null {
    const L = this.T.lines[line.i];
    if (!L) return null;
    if (t >= L.words[0]!.start - HALF) return L;
    const prev = this.T.lines[line.i - 1];
    return prev && t < prev.end ? prev : null;
  }

  /** The plates that only sat there: pasted in from the right on the cut, then riding the beat. */
  override d_plateRight(c: Ctx, s: any, t: number, lt: number, dur: number) {
    const k = ease.outBack(clamp(lt / 0.28)), beat = this.ctx.audio.beatAt(t), bob = Math.pow(1 - (beat - Math.floor(beat)), 3) * 6;
    c.save(); c.translate((1 - k) * 900, -bob); c.translate(1430, 460); c.rotate(0.012 * Math.sin(t * 1.1)); c.translate(-1430, -460);
    super.d_plateRight(c, s, t, lt, dur);
    c.restore();
  }

  override poster(c: Ctx, line: Line, t: number, x: number, y: number, w: number, o: { size?: number; color?: string; hl?: string } = {}) {
    const L = this.kline(line, t);
    if (!L) return;
    const fam = arch(1, 0.25);
    // the size is chosen on the whole line, unsung, so the layout does not jump: at most 4 rows, no word too wide
    let size = o.size ?? 118;
    const fits = () => {
      setF(c, fam, size);
      let rows = 1, cx = 0, widest = 0;
      for (const wd of L.words) {
        const ww = tw(c, wd.w.toUpperCase()); widest = Math.max(widest, ww);
        if (cx > 0 && cx + ww > w) { rows++; cx = 0; }
        cx += ww + size * 0.26;
      }
      return rows <= 4 && widest <= w;
    };
    while (!fits() && size > 50) size -= 6;
    const lead = size * 0.98, col = o.color ?? C.black;
    let cx = x, cy = y;
    for (const wd of L.words) {
      setF(c, fam, size);
      const s = shown(wd, t) ? sungText(wd, t, 6) : wd.w.toUpperCase();
      const ww = tw(c, s);
      if (cx > x && cx + ww > x + w) { cx = x; cy += lead; }
      if (shown(wd, t)) {
        const a = age(wd, t), rise = 1 - ease.outCubic(clamp(a / 0.13)), k = press(a), p = sung(wd, t);
        const mx = cx - size * 0.06, my = cy - size * 0.78, mw = ww + size * 0.12, mh = size * 0.9;
        marker(c, mx, my, mw, mh, p, o.hl ?? C.yellow);
        const draw = (fill: string) => {
          c.save();
          c.beginPath(); c.rect(cx - 30, cy - size * 1.02, ww + 60, size * 1.26); c.clip(); // the word's slot
          c.translate(cx, cy + rise * size * 1.05); c.scale(1 + 0.07 * k, 1 + 0.07 * k);
          c.fillStyle = fill; c.fillText(s, 0, 0);
          c.restore();
        };
        draw(col);
        // light type on the highlighter goes black where the highlighter has reached
        if (p > 0 && col === C.paper) { c.save(); c.beginPath(); c.rect(mx, my - 4, mw * p + 3, mh + 12); c.clip(); draw(C.black); c.restore(); }
      }
      cx += ww + size * 0.26;
    }
  }

  override slipL(c: Ctx, line: Line, t: number, o: { y?: number; size?: number } = {}) {
    const L = this.kline(line, t);
    if (!L) return;
    const size = o.size ?? 44, y = o.y ?? 1000, pad = 26;
    setF(c, F.typewriter(700), size);
    const full = L.words.map((wd) => wd.w).join(' ');
    const fw = tw(c, full), x = (W - fw) / 2;
    c.save();
    c.translate(W / 2, y - size * 0.35); c.rotate(-0.006); c.translate(-W / 2, -(y - size * 0.35));
    c.fillStyle = C.paper; c.fillRect(x - pad, y - size - 14, fw + pad * 2, size + 34);
    c.strokeStyle = C.black; c.lineWidth = 2; c.strokeRect(x - pad, y - size - 14, fw + pad * 2, size + 34);
    let cx = x;
    for (const wd of L.words) {
      const ww = tw(c, wd.w);
      if (shown(wd, t)) {
        // typed a syllable at a time, as sung
        let n = 0;
        for (const [p, a] of wd.syl) if (t >= a - 1 / 120) n += p.length;
        const typed = wd.w.slice(0, Math.max(1, Math.min(wd.w.length, t >= wd.end ? wd.w.length : n)));
        marker(c, cx - 4, y - size * 0.8, ww + 8, size * 0.98, sung(wd, t));
        c.fillStyle = C.black; c.fillText(typed, cx, y);
      }
      cx += ww + tw(c, ' ');
    }
    c.restore();
  }
}
