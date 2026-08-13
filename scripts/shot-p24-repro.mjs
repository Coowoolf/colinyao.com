import { chromium } from 'playwright-core';
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const URL = 'http://localhost:8899/decks/robot26.html#24';
const b = await chromium.launch({ executablePath: EXE });

// Colin 的窗口：2600×1631 设备px ≈ 1300×815 CSS @dpr2
for (const [name, vw, vh, dsf] of [['colin-1300x815@2', 1300, 815, 2], ['flat-2600x1631', 2600, 1631, 1]]) {
  const ctx = await b.newContext({ viewport: { width: vw, height: vh }, deviceScaleFactor: dsf });
  const pg = await ctx.newPage();
  await pg.goto(URL, { waitUntil: 'networkidle' });
  await pg.waitForTimeout(2500);
  const m = await pg.evaluate(() => {
    const v = document.querySelector('section[data-p="24"] video');
    const r = v.getBoundingClientRect();
    const cs = getComputedStyle(v);
    const stage = document.querySelector('.deck-stage').getBoundingClientRect();
    return { vRect: { x: r.x, y: r.y, w: r.width, h: r.height },
             stage: { x: stage.x, y: stage.y, w: stage.width, h: stage.height },
             layout: { w: cs.width, h: cs.height }, hasControls: v.hasAttribute('controls') };
  });
  console.log(name, JSON.stringify(m));
  await pg.screenshot({ path: `/home/claude/eco-review/p24-repro-${name}.png` });
  await ctx.close();
}
await b.close();
