// 禁 WebGL 态实拍：8 页逐页出图（六页退回 poster = 页上原来那张 SVG）——
// 「3D 起不来 ≠ 这份 deck 废了」的实证素材。速讲版会被发给各种设备，这一条是生命线。
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const OUT = process.env.OUT || '/home/claude/eco-review';
const TH = process.env.THEME || 'light';
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--disable-webgl', '--disable-webgl2', '--disable-gpu'] });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await ctx.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, TH);
const pg = await ctx.newPage();
await pg.goto(BASE + '/decks/convoai-info.html#1', { waitUntil: 'load' });
await pg.waitForTimeout(7500);                       // 看门狗 6s
const m = await pg.evaluate(() => document.getElementById('labGl').dataset.labMode);
if (m !== 'POSTER') { console.log('✗ 没有退到 POSTER：' + m); process.exit(1); }
for (let P = 1; P <= 8; P++) {
  await pg.evaluate(k => window.deck.go(k - 1), P);
  await pg.waitForTimeout(2600);
  await pg.evaluate(k => document.querySelectorAll(`.slide[data-p="${k}"] [data-step]`)
    .forEach(e => e.classList.add('on')), P);
  await pg.waitForTimeout(1200);
  await pg.screenshot({ path: `${OUT}/infofb-p${P}-${TH}.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
}
console.log(`· 禁 WebGL 8 页已出（mode=${m}）→ ${OUT}/infofb-p*-${TH}.png`);
await b.close();
