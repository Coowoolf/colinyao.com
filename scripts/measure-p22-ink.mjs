// 量 lab / engine P22 上每一处**字形行框**（Range.getClientRects · 舞台坐标 1920×1080）
//   —— `_P22INK` 的唯一来源：改文案 / 改字号之后重跑一次，把输出贴回 builder。
//   与 qa 的 ㉒a / ⑳galaxy-a 是同一把尺（同一段 TreeWalker + 同一次舞台缩放换算）。
import { chromium } from 'playwright-core';

const BASE = process.env.BASE || 'http://localhost:8899';
const DECK = process.env.DECK || '/decks/convoai-lab.html';
const P = +(process.env.P || 22);
const PAD = +(process.env.PAD || 3);
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const GL = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];

const b = await chromium.launch({ executablePath: CHROME, args: GL });
const out = {};
for (const theme of ['light', 'dark']) {
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto(BASE + DECK + '?lab=hold#' + P, { waitUntil: 'networkidle' });
  if (theme === 'dark') await pg.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
  await pg.evaluate(k => window.deck.go(k - 1), P);
  await pg.waitForTimeout(2600);
  const rows = await pg.evaluate((k) => {
    const s = document.querySelector(`.slide[data-p="${k}"]`);
    const sc = document.querySelector('.deck-stage').getBoundingClientRect();
    const K = sc.width / 1920, o = [];
    const w = document.createTreeWalker(s.querySelector('.pp'), NodeFilter.SHOW_TEXT);
    let t;
    while ((t = w.nextNode())) {
      if (!t.textContent.trim()) continue;
      const r = document.createRange(); r.selectNodeContents(t);
      for (const rc of r.getClientRects())
        if (rc.width > 1 && rc.height > 1)
          o.push({ tx: t.textContent.trim().slice(0, 26),
                   x: (rc.x - sc.x) / K, y: (rc.y - sc.y) / K,
                   w: rc.width / K, h: rc.height / K });
    }
    return o;
  }, P);
  out[theme] = rows;
  await pg.close();
}
await b.close();

// 两档主题取并集（字重 / 字形在两档下会差零点几像素），四周各留 PAD
const all = out.light.map((r, i) => {
  const d = out.dark[i] || r;
  const x0 = Math.min(r.x, d.x), y0 = Math.min(r.y, d.y);
  const x1 = Math.max(r.x + r.w, d.x + d.w), y1 = Math.max(r.y + r.h, d.y + d.h);
  return { tx: r.tx, x: x0 - PAD, y: y0 - PAD, w: x1 - x0 + 2 * PAD, h: y1 - y0 + 2 * PAD };
});
console.log(`# ${DECK} P${P} · ${all.length} 处字形行框（两档并集 + ${PAD}px 留量）`);
for (const r of all)
  console.log(`    (${Math.round(r.x)}, ${Math.round(r.y)}, ${Math.round(r.w)}, ${Math.round(r.h)}),`
    + `   # ${r.tx}`);
