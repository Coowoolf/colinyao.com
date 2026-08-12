import { chromium } from 'playwright-core';
import fs from 'fs';
const ICONS = '/home/claude/eco-review/icons/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
const errs = [];
pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await pg.route(u => u.protocol.startsWith('http'), route => {
  const url = route.request().url();
  const f = ICONS + url.split('/').pop();
  if (url.includes('cdn.jsdelivr.net') && fs.existsSync(f)) {
    route.fulfill({ contentType: 'image/svg+xml', body: fs.readFileSync(f) });
  } else { console.log('ABORT:', url); route.abort(); }
});
const target = process.argv[2] || '/home/claude/eco-review/poster-v12.html';
const out = process.argv[3] || '/home/claude/eco-review/after-4k.png';
await pg.goto('file://' + target, { waitUntil: 'domcontentloaded', timeout: 20000 });
await pg.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 8000 }).catch(() => console.log('WARN: images not all complete'));
await pg.waitForTimeout(700);
const audit = await pg.evaluate(() => {
  const cards = [...document.querySelectorAll('#cai-ecosystem-2026-logo .card')].map(c => ({
    chip: c.querySelector('.chip')?.textContent.trim(),
    ovY: c.scrollHeight - c.clientHeight, ovX: c.scrollWidth - c.clientWidth,
    brands: c.querySelectorAll('.brand').length
  }));
  const imgs = [...document.images];
  const poster = document.querySelector('#cai-ecosystem-2026-logo .poster').getBoundingClientRect();
  const sub = document.querySelector('.sub').getBoundingClientRect();
  const band1 = document.querySelector('.band.blue').getBoundingClientRect();
  const co = document.querySelector('.callout').getBoundingClientRect();
  const ed = document.querySelector('.edition').getBoundingClientRect();
  return { cards,
    imgTotal: imgs.length, imgOK: imgs.filter(i => i.naturalWidth > 0).length,
    poster: { w: poster.width, h: poster.height },
    subGapToBand: +(band1.top - sub.bottom).toFixed(1),
    calloutGapToEdition: +(ed.left - co.right).toFixed(1) };
});
console.log(JSON.stringify(audit, null, 1));
console.log('console errors:', errs.length ? errs.slice(0,5) : 'none');
await pg.locator('#cai-ecosystem-2026-logo .poster').screenshot({ path: out });
await b.close();
