// 单页快照工具（调版式用）：node scripts/shot-one.mjs <deck> <page> <theme> <out> [step]
// 例：node scripts/shot-one.mjs convoai-engine 8 light /tmp/p8.png
import { chromium } from 'playwright-core';
const [deck, p, theme, out, step] = process.argv.slice(2);
const BASE = process.env.BASE || 'http://localhost:8899';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (theme === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
const pg = await ctx.newPage();
await pg.goto(`${BASE}/decks/${deck}.html#1`, { waitUntil: 'load' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(500);
await pg.evaluate(([k, s]) => {
  document.querySelectorAll('.slide').forEach((el, j) => {
    el.classList.toggle('active', j === k - 1);
    el.classList.toggle('visible', j === k - 1);
    el.querySelectorAll('[data-step]').forEach(x => x.classList.remove('on'));
  });
  const cur = document.querySelectorAll('.slide')[k - 1];
  cur.querySelectorAll('[data-step]').forEach(el => {
    if ((+el.dataset.step || 0) <= s) el.classList.add('on');
  });
}, [+p, step === undefined ? 9 : +step]);
await pg.waitForTimeout(2600);
await pg.screenshot({ path: out, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
await b.close();
console.log('· ' + out);
