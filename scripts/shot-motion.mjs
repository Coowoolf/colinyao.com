// 动效连拍：同一页按固定间隔连拍 N 帧（整页 1920×1080），用于 GIF 合成 / 「双帧同格」比对。
// 用法：PAGE=8 N=25 GAP=100 THEME=light OUT=/tmp/mo-p8 node scripts/shot-motion.mjs
// 说明：入场动效先走完（2.6s）再开拍，拍到的只有常驻动效；分步页展开到终态。
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const PAGE = +(process.env.PAGE || 8);
const N = +(process.env.N || 25);
const GAP = +(process.env.GAP || 100);
const THEME = process.env.THEME || 'light';
const OUT = process.env.OUT || '/tmp/mo-frames';
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
const pg = await ctx.newPage();
await pg.goto(`${BASE}/decks/convoai-engine.html#${PAGE}`, { waitUntil: 'load' });
await pg.evaluate(() => document.fonts.ready);
await pg.evaluate((k) => {
  document.querySelectorAll('.slide').forEach((el, j) => {
    el.classList.toggle('active', j === k - 1); el.classList.toggle('visible', j === k - 1);
  });
  document.querySelectorAll('.slide')[k - 1].querySelectorAll('[data-step]').forEach(el => el.classList.add('on'));
}, PAGE);
await pg.waitForTimeout(2800);                       // 入场动效走完，只留常驻动效
for (let i = 0; i < N; i++) {
  await pg.screenshot({ path: `${OUT}/f${String(i).padStart(2, '0')}.png`,
                        clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await pg.waitForTimeout(GAP);
}
console.log(`· P${PAGE} ${THEME} · ${N} 帧 · 间隔 ${GAP}ms → ${OUT}`);
await b.close();
