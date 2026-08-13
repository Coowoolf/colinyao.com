// P7 polish-v4 终审截图：整页 + .eco-visual 放大裁片（浅/深各一组）
// 用法：node scripts/shot-p7-v4.mjs   → /home/claude/eco-review/{p7-light,p7-dark,crop-light,crop-dark}.png
import { chromium } from 'playwright-core';
import fs from 'fs';
const OUTDIR = '/home/claude/eco-review';
fs.mkdirSync(OUTDIR, { recursive: true });
// .eco-visual 盒 = left:120 top:292 w:980 h:552，外扩 20px
const CROP = { x: 120 - 20, y: 292 - 20, width: 980 + 40, height: 552 + 40 };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const THEME of ['light', 'dark']) {
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = [];
  pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  if (THEME === 'dark') {
    await pg.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  }
  await pg.goto('http://localhost:8777/decks/convoai-info.html#7', { waitUntil: 'load' });
  await pg.waitForTimeout(900);
  await pg.evaluate(() => {
    const deck = window.deck;
    deck.i = 6; deck.step = 999;
    deck.render ? deck.render() : null;
    document.querySelectorAll('.slide').forEach((s, k) => {
      const on = k === 6;
      s.classList.toggle('active', on);
      s.classList.toggle('visible', on);
    });
    document.querySelectorAll('.slide')[6].querySelectorAll('[data-step]').forEach(el => el.classList.add('on'));
  });
  await pg.waitForTimeout(2800);   // ≥2.6s：--i 错峰最深 7×88ms + 1.2s clip-path
  await pg.screenshot({ path: `${OUTDIR}/p7-${THEME}.png` });
  await pg.screenshot({ path: `${OUTDIR}/crop-${THEME}.png`, clip: CROP });
  // 顺手回读五层 DOM 行的实际几何，供对齐自查
  const geo = await pg.evaluate(() => {
    const p7 = document.querySelectorAll('.slide')[6];
    const box = p7.querySelector('.eco-visual').getBoundingClientRect();
    const rows = [...p7.querySelectorAll('.eco-layer')].map(el => {
      const r = el.getBoundingClientRect();
      const sm = el.querySelector('small').getBoundingClientRect();
      return { cls: el.className.replace('eco-layer ', ''),
               top: +(r.top - box.top).toFixed(1), mid: +(r.top + r.height / 2 - box.top).toFixed(1),
               bot: +(r.bottom - box.top).toFixed(1),
               smallLeft: +(sm.left - box.left).toFixed(1), smallRight: +(sm.right - box.left).toFixed(1) };
    });
    const chip = p7.querySelector('.callout-chip');
    const cs = getComputedStyle(chip);
    return { box: { w: box.width, h: box.height }, rows,
             chip: { bg: cs.backgroundColor, radius: cs.borderRadius, shadow: cs.boxShadow,
                     borderLeft: cs.borderLeftWidth + ' ' + cs.borderLeftColor, color: cs.color } };
  });
  console.log(THEME, JSON.stringify(geo, null, 1));
  console.log(THEME, 'console errors:', errs.length ? errs.slice(0, 5) : 'none');
  await pg.close();
}
await b.close();
console.log('shots →', OUTDIR);
