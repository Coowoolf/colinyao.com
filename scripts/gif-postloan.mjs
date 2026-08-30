// 动效实录：把 convoai-postloan 的某一页按固定帧率连拍成 PNG 序列（交给 PIL 拼 GIF）。
// 容器里没有 H.264 编码器，视频这条路走不通 —— GIF 是这里唯一能出的「会动的证据」。
// 说明：本 deck 各原语的周期互质（26s 环 / 2.4s 中点脉冲 / 2.2s 进出包 / 3.4s 呼吸 …），
//   最小公倍数长到没有意义，所以这不是无缝循环，是**一段实录**。
//   P5 的环是 26s 一圈，四秒只能录到 1/6 圈；录 P5 时把 SECS 拉长（默认脚本给 6s）。
// 用法：PAGE=5 SECS=6 FPS=12 THEME=light OUT=/tmp/gif-pl-p5 node scripts/gif-postloan.mjs
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const PAGE = +(process.env.PAGE || 5);
const SECS = +(process.env.SECS || 6);
const FPS = +(process.env.FPS || 12);
const THEME = process.env.THEME || 'light';
const OUT = process.env.OUT || `/tmp/gif-postloan-p${PAGE}`;
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
const pg = await ctx.newPage();
await pg.goto(`${BASE}/decks/convoai-postloan.html#${PAGE}`, { waitUntil: 'load' });
await pg.evaluate(() => document.fonts.ready);
// 只掐 transition（入场位移），**不掐 animation** —— 常驻动效正是要录的东西
await pg.addStyleTag({ content: '*,*::before,*::after{transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.evaluate((k) => new Promise((res) => {
  const run = () => {
    document.querySelectorAll('.slide').forEach(el => el.classList.remove('visible'));
    void document.body.offsetWidth;
    document.querySelectorAll('.slide').forEach((el, j) => {
      el.classList.toggle('active', j === k - 1); el.classList.toggle('visible', j === k - 1);
    });
    res();
  };
  requestAnimationFrame(() => requestAnimationFrame(() => requestAnimationFrame(run)));
}), PAGE);
await pg.waitForTimeout(900);              // 入场落位 + 背景板解码
const n = Math.round(SECS * FPS), dt = 1000 / FPS;
for (let i = 0; i < n; i++) {
  await pg.screenshot({ path: `${OUT}/f${String(i).padStart(3, '0')}.png`,
    clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await pg.waitForTimeout(dt);
}
console.log(`· P${PAGE} ${THEME} · ${n} 帧 @ ${FPS}fps → ${OUT}`);
await b.close();
