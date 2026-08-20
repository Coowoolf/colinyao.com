// 终审素材 · convoai-engine 16 页 × 浅/深 全量截图（页数从 DOM 读，扩页不用改本文件）
// 用法：node scripts/shot-engine-family.mjs        （产出 /tmp/eng-shots/pNN-{light,dark}.png）
//      BASE=... OUTDIR=... 可换
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const OUT = process.env.OUTDIR || '/tmp/eng-shots';
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const theme of ['light', 'dark']) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  if (theme === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const pg = await ctx.newPage();
  await pg.goto(BASE + '/decks/convoai-engine.html#1', { waitUntil: 'load' });
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(600);
  const n = await pg.evaluate(() => document.querySelectorAll('.slide').length);
  for (let i = 1; i <= n; i++) {
    await pg.evaluate((k) => {
      document.querySelectorAll('.slide').forEach((el, j) => {
        el.classList.toggle('active', j === k - 1);
        el.classList.toggle('visible', j === k - 1);
      });
    }, i);
    await pg.waitForTimeout(2600);            // 让入场动效走完再拍（.dw 生长线最慢，1.2s 不够）
    await pg.screenshot({ path: `${OUT}/p${String(i).padStart(2, '0')}-${theme}.png`,
      clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await ctx.close();
  console.log('· ' + theme + ' 拍完 ' + n + ' 张');
}
await b.close();
