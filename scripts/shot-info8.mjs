// convoai-info v2 终审截图：8 页 × 双主题 · 每页步进全展开态 · 1920×1080 原尺寸
// 用法：node scripts/shot-info8.mjs            （产物 /tmp/info8/<theme>-pN.png）
//      OUTDIR=/tmp/info8b node scripts/shot-info8.mjs
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const OUT = process.env.OUTDIR || '/tmp/info8';
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const theme of ['light', 'dark']) {
  const c = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  if (theme === 'dark') await c.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const p = await c.newPage();
  for (let i = 1; i <= 8; i++) {
    await p.goto(`${BASE}/decks/convoai-info.html?v=${i}#${i}`, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(1100);
    const steps = await p.evaluate(() => +(document.querySelector('.slide.active')?.dataset.steps || 0));
    for (let k = 0; k < steps; k++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500); }
    await p.waitForTimeout(1200);
    await p.screenshot({ path: `${OUT}/${theme}-p${i}.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    if (theme === 'light') {
      const t = await p.evaluate(() => document.querySelector('.slide.active').textContent.replace(/\s+/g, ' ').trim().slice(0, 70));
      console.log(`P${i} steps=${steps}: ${t}`);
    }
  }
  await c.close();
}
await b.close();
console.log('shots →', OUT);
