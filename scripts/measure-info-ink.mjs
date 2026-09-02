// 墨迹名册实测器（v3）：逐页把「落在该页 3D 矩形之内的字形行框」量出来，
//   直接打印成可以贴回 builder `_INK` 的 Python 字面量。
//   ⚠ 跳过 .detail 子树 —— 细节层压在 canvas 之上，3D 压不到它（与 qa ⑳clr-a 同一把尺）。
//   用法：P=2,3,8 node scripts/measure-info-ink.mjs
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8899';
const PAGES = (process.env.P || '2,3,4,5,6,8').split(',').map(Number);
const PAD = +(process.env.PAD || 0);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await pg.goto(BASE + '/decks/convoai-info.html?lab=hold#1', { waitUntil: 'load' });
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.waitForTimeout(1500);
for (const P of PAGES) {
  const r = await pg.evaluate(({ k, pad }) => {
    document.querySelectorAll('.slide').forEach((el, i) => {
      el.classList.toggle('active', i === k - 1); el.classList.toggle('visible', i === k - 1);
    });
    const s = document.querySelectorAll(`.slide`)[k - 1];
    const st = document.getElementById('labStage' + k);
    if (!st) return null;
    const rc = (st.dataset.labRect || '').split(',').map(Number);
    const sc = document.querySelector('.deck-stage').getBoundingClientRect();
    const K = sc.width / 1920, out = [];
    const w = document.createTreeWalker(s.querySelector('.pp'), NodeFilter.SHOW_TEXT);
    let t;
    while ((t = w.nextNode())) {
      if (!t.textContent.trim()) continue;
      if (t.parentElement && t.parentElement.closest('.detail')) continue;   // 细节层不登记
      const rg = document.createRange(); rg.selectNodeContents(t);
      for (const q of rg.getClientRects()) {
        if (q.width <= 1 || q.height <= 1) continue;
        const g = [(q.x - sc.x) / K, (q.y - sc.y) / K, q.width / K, q.height / K];
        if (g[0] + g[2] > rc[0] - pad && g[0] < rc[0] + rc[2] + pad
         && g[1] + g[3] > rc[1] - pad && g[1] < rc[1] + rc[3] + pad) out.push(g);
      }
    }
    return { rect: rc, out };
  }, { k: P, pad: PAD });
  if (!r) { console.log(`P${P}: 无舞台`); continue; }
  console.log(`    ${P}: [` + r.out.map(g => '(' + g.map(v => Math.round(v * 10) / 10).join(', ') + ')').join(',\n        ') + '],');
  console.log(`    # ↑ P${P} rect=${r.rect} · ${r.out.length} 处`);
}
await b.close();
