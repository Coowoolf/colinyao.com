// 终审截图 · P4 引擎详解抽屉（2026-08-18）
// 四张：P4-LIGHT-REST / P4-DARK-REST / OVERLAY-OPEN / AFTER-ESC → /tmp/eng-shot-*.png
// 顺带把三条自查量出来：chip 的盒与色、eo-sheet 四边留缝、Esc 之后方向键是否真的翻页。
// 用法：node scripts/shot-engine-drawer.mjs      （需要 public 起在 8899）
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8899';
const URL = BASE + '/decks/convoai-info.html';
const IN = 2400;                       // 入场 ≥2.3s
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

async function page(theme) {
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await pg.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, theme);
  await pg.goto(URL + '#4', { waitUntil: 'load' });
  await pg.waitForTimeout(IN);
  return pg;
}

/* ① P4-LIGHT-REST + chip 量测 */
const lt = await page('light');
await lt.screenshot({ path: '/tmp/eng-shot-1.png' });
const chipInfo = await lt.evaluate(() => {
  const c = document.getElementById('engineExpand');
  const sib = c.previousElementSibling;                       // 相邻的普通 chip，用来比对「抢不抢版面」
  const cs = getComputedStyle(c), ss = getComputedStyle(sib);
  const r = c.getBoundingClientRect(), rs = sib.getBoundingClientRect();
  const row = c.closest('.sh').getBoundingClientRect();
  const chips = [...c.closest('.sh').querySelectorAll('.chip')];
  return {
    text: c.textContent,
    box: { w: +r.width.toFixed(1), h: +r.height.toFixed(1), x: +r.x.toFixed(1), y: +r.y.toFixed(1) },
    plainBox: { w: +rs.width.toFixed(1), h: +rs.height.toFixed(1) },
    color: cs.color, border: cs.borderTopColor, bg: cs.backgroundColor, cursor: cs.cursor,
    plainColor: ss.color, plainBorder: ss.borderTopColor,
    chipsN: chips.length, rowW: +row.width.toFixed(1),
    rowUsed: +(chips.reduce((s, e) => s + e.getBoundingClientRect().width + 12, 0)).toFixed(1),
    widthShare: +(r.width / chips.reduce((s, e) => s + e.getBoundingClientRect().width, 0) * 100).toFixed(1),
    sameRow: chips.every(e => Math.abs(e.getBoundingClientRect().y - r.y) < 2),
  };
});
/* hover 态也量一下，确认「可点」的反馈真的成立 */
await lt.hover('#engineExpand'); await lt.waitForTimeout(300);
const chipHover = await lt.evaluate(() => {
  const cs = getComputedStyle(document.getElementById('engineExpand'));
  return { bg: cs.backgroundColor, border: cs.borderTopColor };
});
await lt.mouse.move(960, 200); await lt.waitForTimeout(250);

/* ③ OVERLAY-OPEN：P4 按 Enter → 等 iframe load + 800ms */
await lt.evaluate(() => { document.activeElement?.blur(); });
await lt.keyboard.press('Enter');
await lt.waitForFunction(() => {
  const f = document.getElementById('engineFrame'), d = f && f.contentDocument;
  return !!(d && d.readyState === 'complete' && d.querySelectorAll('section').length === 13);
}, null, { timeout: 10000 });
await lt.waitForTimeout(800);
await lt.screenshot({ path: '/tmp/eng-shot-3.png' });
const sheet = await lt.evaluate(() => {
  const s = document.querySelector('.eo-sheet').getBoundingClientRect();
  const f = document.getElementById('engineFrame');
  return {
    gapL: +s.left.toFixed(1), gapR: +(innerWidth - s.right).toFixed(1),
    gapT: +s.top.toFixed(1), gapB: +(innerHeight - s.bottom).toFixed(1),
    radius: getComputedStyle(document.querySelector('.eo-sheet')).borderRadius,
    frameSecs: f.contentDocument.querySelectorAll('section').length,
    focus: document.activeElement?.id,
    scrollLeft: f.contentWindow.document.getElementById('deck').scrollLeft,
  };
});

/* 在 iframe 里往前翻两页，用来验「关闭不重置进度」 */
await lt.keyboard.press('ArrowRight'); await lt.waitForTimeout(600);
await lt.keyboard.press('ArrowRight'); await lt.waitForTimeout(900);
const innerBefore = await lt.evaluate(() => document.getElementById('engineFrame')
  .contentWindow.document.getElementById('deck').scrollLeft);

/* ④ AFTER-ESC：焦点在 iframe 内按 Esc → 回 P4，overlay 消失 */
await lt.keyboard.press('Escape');
await lt.waitForTimeout(700);
await lt.screenshot({ path: '/tmp/eng-shot-4.png' });
const afterEsc = await lt.evaluate(() => ({
  hidden: document.getElementById('engineOverlay').hidden,
  cur: document.querySelector('.slide.active')?.dataset.p,
}));
/* 方向键是否真的回到 deck 手里：→ 到 P5，← 回 P4 */
await lt.keyboard.press('ArrowRight'); await lt.waitForTimeout(500);
const p5 = await lt.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
await lt.keyboard.press('ArrowLeft'); await lt.waitForTimeout(500);
const backP4 = await lt.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
/* 二次展开：iframe 不重载、进度不丢 */
await lt.keyboard.press('Enter'); await lt.waitForTimeout(600);
const reopen = await lt.evaluate(() => {
  const f = document.getElementById('engineFrame');
  return { hidden: document.getElementById('engineOverlay').hidden,
           scrollLeft: f.contentWindow.document.getElementById('deck').scrollLeft,
           reloaded: f.contentWindow.document.querySelectorAll('section').length };
});
await lt.close();

/* ② P4-DARK-REST */
const dk = await page('dark');
await dk.screenshot({ path: '/tmp/eng-shot-2.png' });
const chipDark = await dk.evaluate(() => {
  const c = document.getElementById('engineExpand'), cs = getComputedStyle(c);
  const r = c.getBoundingClientRect();
  return { color: cs.color, border: cs.borderTopColor, vis: r.width > 0 && r.height > 0,
           theme: document.documentElement.getAttribute('data-theme') };
});
await dk.close();
await b.close();

console.log(JSON.stringify({ chipInfo, chipHover, chipDark, sheet, innerBefore,
                            afterEsc, p5, backP4, reopen }, null, 2));
