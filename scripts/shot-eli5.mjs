// 逐页出图 + ELI5 两条硬闸的现场读数（字数 / 图占比）—— 做图时的肉眼工具。
// 用法：node scripts/shot-eli5.mjs            （light · 全 11 页）
//      THEME=dark PAGES=2,7 node scripts/shot-eli5.mjs
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const THEME = process.env.THEME || 'light';
const OUT = process.env.OUT || '/home/claude/eco-review/eli5-shots';
const PAGES = (process.env.PAGES || '1,2,3,4,5,6,7,8,9,10,11').split(',').map(Number);
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
const pg = await ctx.newPage();
await pg.goto(BASE + '/decks/convoai-eli5.html#1', { waitUntil: 'load' });
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.waitForTimeout(800);
for (const n of PAGES) {
  const r = await pg.evaluate((k) => {
    document.querySelectorAll('.slide').forEach((el, j) => {
      el.classList.remove('visible'); el.classList.toggle('active', j === k - 1);
    });
    void document.body.offsetWidth;
    document.querySelectorAll('.slide').forEach((el, j) => el.classList.toggle('visible', j === k - 1));
    const s = document.querySelectorAll('.slide')[k - 1];
    const skip = new Set(); s.querySelectorAll('.kk,.hh,.sig,.src').forEach(e => skip.add(e));
    const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    let body = '';
    for (let t = w.nextNode(); t; t = w.nextNode()) {
      let p = t.parentElement, bad = false;
      while (p && p !== s) { if (skip.has(p)) { bad = true; break; } p = p.parentElement; }
      if (!bad) body += t.textContent;
    }
    const cjk = (body.match(/[一-鿿]/g) || []).length;
    const f = s.querySelector('.eli-fig');
    const fr = f ? f.getBoundingClientRect() : null;
    const out = [];
    s.querySelectorAll('.pp .sh').forEach(el => {
      [...el.children].forEach(ch => {
        const c = ch.getBoundingClientRect();
        if (c.bottom > 1074 || c.right > 1926 || c.left < -6 || c.top < -6) out.push(el.className.slice(0, 30));
      });
    });
    return { cjk, body: body.replace(/\s+/g, ' ').trim().slice(0, 120),
      figPct: fr ? +(fr.width * fr.height / (1920 * 1080) * 100).toFixed(2) : 0, out };
  }, n);
  await pg.waitForTimeout(260);
  await pg.screenshot({ path: `${OUT}/p${String(n).padStart(2, '0')}-${THEME}.png`,
    clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  console.log(`P${n} ${THEME} · 正文汉字 ${r.cjk}/40 · 图占版面 ${r.figPct}% · 溢出 ${r.out.length}`
    + `\n     「${r.body}」`);
}
await b.close();
