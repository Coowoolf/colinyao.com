// P10 常驻动效取帧：同一页连拍 N 帧，用于 GIF 合成 / 人眼比对「是否真的在动」
import { chromium } from 'playwright-core';
const OUT = process.env.OUT || '/tmp/p10frames';
const N = +(process.env.N || 24);
const GAP = +(process.env.GAP || 90);
const THEME = process.env.THEME || 'light';
const fs = await import('fs');
fs.mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme','dark'); } catch(e){} });
const pg = await ctx.newPage();
await pg.goto('http://localhost:8777/decks/convoai-engine.html#10', { waitUntil: 'load' });
await pg.waitForTimeout(2000);
await pg.evaluate(() => {
  document.querySelectorAll('.slide').forEach((el, i) => { el.classList.toggle('active', i === 9); el.classList.toggle('visible', i === 9); });
  if (window.deck) window.deck.i = 9;
});
await pg.waitForTimeout(1600);
const clip = await pg.evaluate(() => {
  const f = document.querySelector('.slide[data-p="10"] .fig');
  const r = f.getBoundingClientRect();
  return { x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height) };
});
for (let i = 0; i < N; i++) {
  await pg.screenshot({ path: `${OUT}/f${String(i).padStart(2,'0')}.png`, clip });
  await pg.waitForTimeout(GAP);
}
console.log('frames', N, 'clip', JSON.stringify(clip));
await b.close();
