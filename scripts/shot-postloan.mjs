// 逐页出图 + 15 页联览拼版（做图时的肉眼工具，不是闸门）。
// 用法：node scripts/shot-postloan.mjs                （中文版 · light · 全 15 页 + contact sheet）
//      THEME=dark node scripts/shot-postloan.mjs
//      PAGES=5,11 node scripts/shot-postloan.mjs      （只补拍某几页，不重拼联览）
//      DECK=en node scripts/shot-postloan.mjs         （2026-08-30：东南亚英文版，产出自动改名）
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
import { execSync } from 'child_process';
const BASE = process.env.BASE || 'http://localhost:8899';
const THEME = process.env.THEME || 'light';
// DECK=en ⇒ 英文版（/decks/convoai-postloan-en.html），产出目录与联览文件名都带 -en，
// 两版的图互不覆盖；不传 DECK 时行为与改动前逐字等价。
const EN = process.env.DECK === 'en';
const TAG = EN ? '-en' : '';
const OUT = process.env.OUT || `/home/claude/eco-review/postloan${TAG}-shots-` + THEME;
const ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];
const PAGES = (process.env.PAGES || ALL.join(',')).split(',').map(Number);
const FULL = PAGES.length === ALL.length;
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
const pg = await ctx.newPage();
await pg.goto(BASE + `/decks/convoai-postloan${TAG}.html#1`, { waitUntil: 'load' });
// 入场是 transition（.rise/.spread 起手有位移）；不掐掉就会拍到「还没落位」的中间态
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(800);
for (const n of PAGES) {
  await pg.evaluate((k) => {
    document.querySelectorAll('.slide').forEach((el, j) => {
      el.classList.remove('visible'); el.classList.toggle('active', j === k - 1);
    });
    void document.body.offsetWidth;
    document.querySelectorAll('.slide').forEach((el, j) => el.classList.toggle('visible', j === k - 1));
  }, n);
  await pg.waitForTimeout(160);
  await pg.screenshot({ path: `${OUT}/p${String(n).padStart(2, '0')}.png` });
}
await b.close();
if (FULL) {
  // 15 页 = 3 列 × 5 行，每格缩到 620 宽（联览只看版式与留白，不看小字）
  const dst = `/home/claude/eco-review/postloan${TAG}-contact-${THEME}.png`;
  execSync(`cd ${OUT} && montage p*.png -tile 3x5 -geometry 620x349+8+8 -background '#8a8a8a' ${dst}`);
  console.log('contact sheet → ' + dst);
}
console.log('逐页 → ' + OUT);
