// 动效实录 · LAB 页专用：**TOUR.pace 定拍**（容器里是软渲染，按真实 dt 录出来会快 3–4×）。
//   钟只在 TOUR.step() 里按 1/fps 前进 ⇒ 录多久就是多久，GIF 的速度可以当证据看。
//   DOM 动效在录制期一律掐掉（3D 页上会动的是 canvas；poster 已经淡出，
//   留着 DOM 动画只会与定拍的 3D 打架）。
// 用法：PAGE=8 SECS=6 FPS=12 THEME=light CLIP=100,220,880,640 SCALE=0.75 \
//       OUT=/tmp/gif-info-p8 node scripts/gif-info-lab.mjs
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const PAGE = +(process.env.PAGE || 8);
const SECS = +(process.env.SECS || 6);
const FPS = +(process.env.FPS || 12);
const THEME = process.env.THEME || 'light';
const STEPS = process.env.STEPS === '1';
const CLIP = (process.env.CLIP || '0,0,1920,1080').split(',').map(Number);
const OUT = process.env.OUT || `/tmp/gif-info-p${PAGE}`;
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
const pg = await ctx.newPage();
await pg.goto(`${BASE}/decks/convoai-info.html?lab=hold#${PAGE}`, { waitUntil: 'load' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(6500);
await pg.evaluate(k => window.deck.go(k - 1), PAGE);
await pg.waitForTimeout(2600);
if (STEPS) { await pg.evaluate(k => document.querySelectorAll(`.slide[data-p="${k}"] [data-step]`)
  .forEach(e => e.classList.add('on')), PAGE); await pg.waitForTimeout(900); }
// 入场落位之后再掐 DOM 动效（掐早了卡片停在半程）
await pg.addStyleTag({ content: '*,*::before,*::after{animation:none!important;'
  + 'transition-duration:0s!important;transition-delay:0s!important;}' });
const paced = await pg.evaluate((f) => window.__labTour.pace(f), FPS);
const t0 = await pg.evaluate(() => window.__labTour.clock());
if (!paced) { console.log('✗ 定拍失败（该页没有场景？）'); await b.close(); process.exit(1); }
const n = Math.round(SECS * FPS);
for (let i = 0; i < n; i++) {
  await pg.evaluate(() => window.__labTour.step(1));
  await pg.screenshot({ path: `${OUT}/f${String(i).padStart(3, '0')}.png`,
    clip: { x: CLIP[0], y: CLIP[1], width: CLIP[2], height: CLIP[3] } });
}
const clock = await pg.evaluate(() => { const c = window.__labTour.clock(); window.__labTour.pace(0); return c; });
console.log(`· P${PAGE} ${THEME} · ${n} 帧 @ ${FPS}fps（定拍 · 录了 ${(clock - t0).toFixed(2)}s 场上时间）→ ${OUT}`);
await b.close();
