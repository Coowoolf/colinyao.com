import { chromium } from 'playwright-core';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const theme of ['light', 'dark']) {
  const c = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await c.newPage();
  await p.addInitScript(t => { try { localStorage.setItem('colin-theme', t) } catch(e){} }, theme);
  await p.goto('http://localhost:3000/intel-2026-08', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  const H = await p.evaluate(() => document.body.scrollHeight);
  const shots = Math.ceil(H / 900);
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  for (let i = 0; i < shots; i++) {
    await p.evaluate(y => window.scrollTo(0, y), i * 900);
    await p.waitForTimeout(700);
    await p.screenshot({ path: `/tmp/intel-${theme}-${String(i).padStart(2,'0')}.png` });
  }
  console.log(theme, 'height', H, 'shots', shots, 'pageerrors', errs.length);
  await c.close();
}
await b.close();
