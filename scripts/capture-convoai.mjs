import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const OUTDIR = process.env.OUTDIR || ('/home/claude/shots-convoai-' + THEME);
import fs from 'fs'; fs.mkdirSync(OUTDIR, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const errs = [];
pg.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
pg.on('console', m => { if (m.type() === 'error') errs.push(m.text() + ' @ ' + (m.location()?.url || '')); });
if (THEME === 'dark') {
  await pg.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
}
await pg.goto('http://localhost:8777/decks/convoai.html#1', { waitUntil: 'load' });
await pg.waitForTimeout(900);
const N = await pg.evaluate(() => document.querySelectorAll('.slide').length);
for (let i = 1; i <= N; i++) {
  await pg.evaluate(n => {
    const deck = window.deck;
    deck.i = n - 1; deck.step = 999;
    deck.render ? deck.render() : null;
    // force final state for capture
    document.querySelectorAll('.slide').forEach((s, k) => {
      const on = k === n - 1;
      s.classList.toggle('active', on);
      s.classList.toggle('visible', on);
    });
    const cur = document.querySelectorAll('.slide')[n - 1];
    cur.querySelectorAll('[data-step]').forEach(el => el.classList.add('on'));
  }, i);
  await pg.waitForTimeout(650);
  await pg.screenshot({ path: `${OUTDIR}/p${String(i).padStart(2, '0')}.png` });
}
console.log('captured', N, 'pages,', THEME);
console.log(errs.length ? errs.slice(0, 8) : 'no console errors');
await b.close();
