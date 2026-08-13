import { chromium } from 'playwright-core';
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const URL = 'http://localhost:8899/decks/robot26.html#24';
const b = await chromium.launch({ executablePath: EXE });

// ① Colin 窗口比例（1300×815 CSS @2x，letterbox 场景）静置态
const c1 = await b.newContext({ viewport: { width: 1300, height: 815 }, deviceScaleFactor: 2 });
const p1 = await c1.newPage();
await p1.goto(URL, { waitUntil: 'networkidle' });
await p1.waitForTimeout(2200);
await p1.screenshot({ path: '/home/claude/eco-review/p24f-colinwin-rest.png' });
// ② 同窗口 · 悬停视频 → controls 呼出（排练手控可用性验证）
await p1.mouse.move(650, 400);
await p1.waitForTimeout(600);
const hov = await p1.evaluate(() => document.querySelector('section[data-p="24"] video').hasAttribute('controls'));
await p1.screenshot({ path: '/home/claude/eco-review/p24f-colinwin-hover.png' });
// 移出 → 收回
await p1.mouse.move(650, 812);
await p1.waitForTimeout(400);
const out = await p1.evaluate(() => document.querySelector('section[data-p="24"] video').hasAttribute('controls'));
console.log('hover-controls:', hov, '| after-leave:', out);
await c1.close();

// ③ 真机 16:9（1920×1080，scale=1）· 步进播放 1.5s 处截帧
const c2 = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const p2 = await c2.newPage();
await p2.goto(URL, { waitUntil: 'networkidle' });
await p2.waitForTimeout(2200);
await p2.keyboard.press('ArrowRight');   // build 1 → syncMedia 触发播放
await p2.waitForTimeout(1500);
const st = await p2.evaluate(() => { const v = document.querySelector('section[data-p="24"] video');
  return { paused: v.paused, t: +v.currentTime.toFixed(2), ctl: v.hasAttribute('controls') }; });
console.log('16:9 play-state:', JSON.stringify(st));
await p2.screenshot({ path: '/home/claude/eco-review/p24f-169-playing.png' });
await c2.close();
await b.close();
console.log('ok');
