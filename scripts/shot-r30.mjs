import { chromium } from 'playwright-core';
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const URL = 'http://localhost:8899/decks/robot26.html';
const OUT = '/home/claude/eco-review/';

const b = await chromium.launch({ executablePath: EXE });
for (const theme of ['dark', 'light']) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const pg = await ctx.newPage();
  await pg.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, theme);
  for (const p of [3, 24]) {
    await pg.goto(`${URL}#${p}`, { waitUntil: 'networkidle' });
    await pg.waitForTimeout(2800);
    await pg.screenshot({ path: `${OUT}r30-p${p}-${theme}.png` });
  }
  await ctx.close();
}
await b.close();
console.log('shots ok');
