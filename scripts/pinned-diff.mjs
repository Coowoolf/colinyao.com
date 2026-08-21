// 静态帧比对：把两份 deck 的同一页在「animation-duration:0 + transition 归零」下各截一帧，
// 逐像素比对 —— 这是「动效关掉 = 原图逐像素」纪律的自证工具（P8 冻结页、P10 代码归一都靠它）。
// 用法：A=http://localhost:8777/decks/_base.html B=http://localhost:8899/decks/convoai-engine.html \
//       PAGES=8,10 THEME=light node scripts/pinned-diff.mjs
// RM=1：两边都按 prefers-reduced-motion:reduce 渲染 —— 验「动效全关 = 原图逐像素」这条硬红线。
//
// SELFPIN=1（2026-08-21 加 · 单份 deck 的「100% 帧 = 静态原图」自证）：
//   不比两份 deck，而是把**同一个 URL** 拍两帧 ——
//     a = prefers-reduced-motion:reduce（动效全关：装饰件 display:none、真几何件 animation:none）
//     b = animation-duration:0s + animation-delay:0s（浏览器把每个动画钉在 **100% 帧**上），
//         并额外把纯装饰件（.mo-packet / .mo-halo / .mo-ghost）隐掉 —— 它们在 a 里本来就是
//         display:none，不隐掉的话差异会全落在「装饰件存在与否」上，测不出真正想测的东西。
//   两帧逐像素相等 ⇔ 所有**真几何件**（.mo-drift / .mo-cycle / .mo-pulse / .mo-breathe 的载体）
//   的 100% 帧与静态原图完全重合 ⇒ dash 走满整周期、scale 回 1、opacity 回静态值。
//   这就是运动语言那条硬红线的机器自证。A 传 URL，B 可省略。
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const A = process.env.A, B = process.env.B || process.env.A;
const PAGES = (process.env.PAGES || '10').split(',').map(Number);
const THEME = process.env.THEME || 'light';
const OUT = process.env.OUT || '/tmp/pinned-diff';
const SELFPIN = process.env.SELFPIN === '1';
mkdirSync(OUT, { recursive: true });
const KILL = '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}';
const NODECO = '.mo-packet,.mo-halo,.mo-ghost{display:none!important;}';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
async function shoot(url, n, path, side) {
  const rm = process.env.RM === '1' || (SELFPIN && side === 'a');
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1,
    ...(rm ? { reducedMotion: 'reduce' } : {}) });
  if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const pg = await ctx.newPage();
  await pg.goto(url + '#1', { waitUntil: 'load' });
  await pg.addStyleTag({ content: KILL });
  // SELFPIN 的 b 帧：真几何件钉在 100% 帧，纯装饰件与 a 帧（reduced-motion）一样隐掉
  if (SELFPIN && side === 'b') await pg.addStyleTag({ content: NODECO });
  await pg.evaluate(() => document.fonts.ready);
  // 背景板是 CSS background-image（不是 <img>），img.complete 盖不住它：
  // 显式把每张板子的 URL 交给 Image().decode() 等一遍。少了这一步，700ms 的静置在
  // reduced-motion 与常态两条渲染路径上会各自赶不上一次解码 —— 两帧就差出整块底纹
  // （2026-08-21 实测：同一页两次跑，一次 0 差异、一次 15 万像素，随机漂）。
  await pg.evaluate(() => {
    const urls = new Set();
    document.querySelectorAll('.conf-bg').forEach((el) => {
      const m = /url\("?([^")]+)"?\)/.exec(getComputedStyle(el).backgroundImage);
      if (m) urls.add(m[1]);
    });
    [...document.images].forEach(i => urls.add(i.currentSrc || i.src));
    return Promise.all([...urls].filter(Boolean).map(u => new Promise((res) => {
      const im = new Image(); im.onload = im.onerror = () => res(); im.src = u;
    })));
  });
  // ⚠ 必须等 deck.js 自己那对 requestAnimationFrame 先落地再翻页：
  //   deck.go() 用 rAF(rAF(() => cur.classList.add('visible'))) 触发入场，而 rAF 在**首帧绘制前**
  //   不会执行。goto 返回之后它可能仍然挂着，直接 classList.toggle 会被它随后补回来 ——
  //   结果是 P1 与目标页同时 visible（页码位上叠出一个鬼影「1」，2026-08-21 实测）。
  //   三帧之后再翻页，deck 的那一对早已跑完，我们的赋值才是最终态。
  await pg.evaluate((k) => new Promise((res) => {
    const run = () => {
      // 先把 visible 全摘掉再重挂：deck.js 在 KILL 样式注入**之前**就给 #1 挂上了 visible，
      // 那条 1.05s 的入场 transition 已经在飞 —— 中途改 transition-duration 不会重定向
      // 正在跑的 transition（CSS 规范），所以 700ms 后拍到的是半途的 .rise（实测 P1 抖 3px）。
      // 摘掉再挂 = 在 KILL 生效后重新起一次 transition ⇒ 瞬时落位，两帧才可复现。
      document.querySelectorAll('.slide').forEach((el) => el.classList.remove('visible'));
      void document.body.offsetWidth;
      document.querySelectorAll('.slide').forEach((el, j) => {
        el.classList.toggle('active', j === k - 1); el.classList.toggle('visible', j === k - 1);
        el.querySelectorAll('[data-step]').forEach(x => x.classList.add('on'));
      });
      res();
    };
    requestAnimationFrame(() => requestAnimationFrame(() => requestAnimationFrame(run)));
  }), n);
  await pg.waitForTimeout(700);
  await pg.screenshot({ path, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await ctx.close();
}
for (const n of PAGES) {
  await shoot(A, n, `${OUT}/a-p${n}.png`, 'a');
  await shoot(B, n, `${OUT}/b-p${n}.png`, 'b');
  console.log(`P${n} ${THEME}${SELFPIN ? ' [SELFPIN 静态 vs 100%帧]' : ''}: `
    + `两帧已出 ${OUT}/a-p${n}.png / b-p${n}.png（逐像素比对交给 compare-frames.py）`);
}
await b.close();
