// 挑页截图 · convoai-engine（before/after 并置素材用）
// 用法：PAGES=2,3,4 THEME=light OUTDIR=/tmp/eng-before node scripts/shot-eng-pick.mjs
//      分步页一律展开到终态（看内容全貌，不看步态）。
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const OUT = process.env.OUTDIR || '/tmp/eng-pick';
const THEME = process.env.THEME || 'light';
const PAGES = (process.env.PAGES || '').split(',').filter(Boolean).map(Number);
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
const pg = await ctx.newPage();
await pg.goto(BASE + '/decks/convoai-engine.html#1', { waitUntil: 'load' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(600);
for (const i of PAGES) {
  await pg.evaluate((k) => {
    document.querySelectorAll('.slide').forEach((el, j) => {
      el.classList.toggle('active', j === k - 1);
      el.classList.toggle('visible', j === k - 1);
    });
    document.querySelectorAll('.slide')[k - 1]
      .querySelectorAll('[data-step]').forEach(el => el.classList.add('on'));
  }, i);
  await pg.waitForTimeout(2600);
  await pg.screenshot({ path: `${OUT}/p${String(i).padStart(2, '0')}-${THEME}.png`,
    clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  console.log('· p' + i + ' ' + THEME);
}
await ctx.close();
await b.close();
