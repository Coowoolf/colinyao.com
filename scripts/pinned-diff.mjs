// 静态帧比对：把两份 deck 的同一页在「animation-duration:0 + transition 归零」下各截一帧，
// 逐像素比对 —— 这是「动效关掉 = 原图逐像素」纪律的自证工具（P8 冻结页、P10 代码归一都靠它）。
// 用法：A=http://localhost:8777/decks/_base.html B=http://localhost:8899/decks/convoai-engine.html \
//       PAGES=8,10 THEME=light node scripts/pinned-diff.mjs
// RM=1：两边都按 prefers-reduced-motion:reduce 渲染 —— 验「动效全关 = 原图逐像素」这条硬红线。
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const A = process.env.A, B = process.env.B;
const PAGES = (process.env.PAGES || '10').split(',').map(Number);
const THEME = process.env.THEME || 'light';
const OUT = process.env.OUT || '/tmp/pinned-diff';
mkdirSync(OUT, { recursive: true });
const KILL = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
async function shoot(url, n, path) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1,
    ...(process.env.RM === '1' ? { reducedMotion: 'reduce' } : {}) });
  if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const pg = await ctx.newPage();
  await pg.goto(url + '#1', { waitUntil: 'load' });
  await pg.addStyleTag({ content: KILL });
  await pg.evaluate(() => document.fonts.ready);
  await pg.evaluate((k) => {
    document.querySelectorAll('.slide').forEach((el, j) => {
      el.classList.toggle('active', j === k - 1); el.classList.toggle('visible', j === k - 1);
      el.querySelectorAll('[data-step]').forEach(x => x.classList.add('on'));
    });
  }, n);
  await pg.waitForTimeout(700);
  await pg.screenshot({ path, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await ctx.close();
}
for (const n of PAGES) {
  await shoot(A, n, `${OUT}/a-p${n}.png`);
  await shoot(B, n, `${OUT}/b-p${n}.png`);
  console.log(`P${n} ${THEME}: 两帧已出 ${OUT}/a-p${n}.png / b-p${n}.png（逐像素比对交给 compare-frames.py）`);
}
await b.close();
