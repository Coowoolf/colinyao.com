#!/usr/bin/env node
/* 深浅一致性巡检（二轮精修 · 波B ⑤）
   ---------------------------------------------------------------------------
   病灶是系统性的：暗底走**加色混合**、浅底走正常混合 ⇒ 同一批 alpha 在浅底上
   跌到阈值下（Colin 说的「浅色下雾 / alpha 塌掉」）。
   这把尺子逐页量两件事（同 tick gl.readPixels，与 ⑲p7 同一条通道）：
     ink 平均 alpha（这一页画了多少墨）· cov alpha≥8 的像素占比（铺了多广）
   然后给出**浅 / 暗比值**。比值越接近 1，两版看起来越像同一份 deck。
   用法：node scripts/qa-lab-ink.mjs [--json out.json]
*/
import { chromium } from 'playwright-core';
import { writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
const BASE = process.env.BASE || 'http://localhost:8899';
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const GL = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
const PAGES = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 21];
const AT = 3.0;                       // 统一定在 t=3.0s 那一帧量（两版同拍，才有可比性）

/* 「墨量」= **合成之后**相对纸/幕底色的亮度偏离（不是 canvas 的 alpha）——
   病灶正是「同一批 alpha，暗底加色一压就亮、浅底正常混合一压就没」，
   所以尺子必须量合成结果，不能量 alpha。底色取该区域**众数亮度**（纸面/幕面占绝对多数）。
   量化交给 python（PIL）：这里只负责把两版的图形区逐页截下来。 */
const TMP = process.env.INKTMP || '/tmp/lab-ink';
mkdirSync(TMP, { recursive: true });

const b = await chromium.launch({ executablePath: CHROME, args: GL });
const out = {};
for (const theme of ['light', 'dark']) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await ctx.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, theme);
  const pg = await ctx.newPage();
  await pg.goto(BASE + (process.env.DECKF || '/decks/convoai-lab.html') + '?lab=hold#1', { waitUntil: 'load' });
  await pg.waitForTimeout(6800);
  for (const p of PAGES) {
    await pg.evaluate((k) => window.deck.go(k - 1), p);
    await pg.waitForTimeout(1500);
    await pg.evaluate(() => document.querySelector('.slide.active')
      .querySelectorAll('[data-step]').forEach(e => e.classList.add('on')));
    await pg.waitForTimeout(2200);   // 等分步的缓动落位（semOp 一类的 ease 不settle 就没有可比性）
    const rect = await pg.evaluate((t) => {
      const T = window.__labTour; T.pace(30); T.seek(t);
      const el = document.getElementById('labStage' + document.querySelector('.slide.active').dataset.p);
      const r = el.getBoundingClientRect();
      return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)];
    }, AT);
    const clip = { x: rect[0], y: rect[1], width: rect[2], height: rect[3] };
    const buf = await pg.screenshot({ clip });
    /* 第二张：把 canvas 藏掉再拍同一格 —— 两张的差就是**3D 这一层**贡献的墨。
       不这么做，量到的一大半是压在图形区上的 DOM 文字（两版对称，会把比值稀释掉）。 */
    await pg.evaluate(() => { document.getElementById('labGl').style.visibility = 'hidden'; });
    await pg.waitForTimeout(120);
    const buf0 = await pg.screenshot({ clip });
    await pg.evaluate(() => { document.getElementById('labGl').style.visibility = ''; });
    await pg.evaluate(() => window.__labTour.pace(0));
    writeFileSync(`${TMP}/${theme}-p${p}.png`, buf);
    writeFileSync(`${TMP}/${theme}-p${p}-off.png`, buf0);
    (out[p] = out[p] || {})[theme] = rect;
  }
  await ctx.close();
}
await b.close();
const PY = `
import sys, json
from PIL import Image
pages = json.loads(sys.argv[1]); tmp = sys.argv[2]
rows = []
def meas(f):
    """两把尺子：
       ① comp  合成之后相对众数底色的亮度偏离（读者眼里的「这一页有多少墨」）
       ② solo  同一格里「canvas 开 / 关」两张的差（**3D 这一层自己**贡献的墨）
       comp 会被压在图形区上的 DOM 文字稀释（两版对称），所以调参看 solo，
       终审看 comp —— 两把一起报，不许只挑好看的那把。"""
    a = Image.open(f).convert("L"); b = Image.open(f.replace(".png", "-off.png")).convert("L")
    pa = list(a.getdata()); pb = list(b.getdata()); n = len(pa)
    h = [0]*256
    for v in pa: h[v] += 1
    bg = h.index(max(h))
    cs = 0; cc = 0; ss = 0; sc = 0
    for i in range(n):
        d = abs(pa[i] - bg); cs += d
        if d >= 4: cc += 1
        e = abs(pa[i] - pb[i]); ss += e
        if e >= 4: sc += 1
    return (cs/n/255.0, cc/float(n), ss/n/255.0, sc/float(n))
for p in pages:
    il, cl, sl, scl = meas("%s/light-p%d.png" % (tmp, p))
    idk, cd, sd, scd = meas("%s/dark-p%d.png" % (tmp, p))
    rows.append({"p": p, "inkL": il, "inkD": idk, "covL": cl, "covD": cd,
                 "ink": il/(idk or 1), "cov": cl/(cd or 1),
                 "solo": sl/(sd or 1), "solocov": scl/(scd or 1)})
print(json.dumps(rows))
`;
const rows = JSON.parse(execFileSync('python3', ['-c', PY, JSON.stringify(PAGES), TMP],
                                     { maxBuffer: 1 << 26 }).toString());
const f = (x) => x.toFixed(2);
console.log('页   ink(浅)  ink(暗)  墨量比值   覆盖率比值   3D 层墨量比值  3D 层覆盖率比值');
rows.forEach(r => console.log(`P${String(r.p).padEnd(3)} ${r.inkL.toFixed(4)}   ${r.inkD.toFixed(4)}   ${f(r.ink)}       ${f(r.cov)}         ${f(r.solo)}           ${f(r.solocov)}`));
const inks = rows.map(r => r.ink), covs = rows.map(r => r.cov);
const avg = (a) => a.reduce((x, y) => x + y, 0) / a.length;
const sol = rows.map(r => r.solo), sco = rows.map(r => r.solocov);
console.log(`\n合成墨量比值 ${f(Math.min(...inks))}–${f(Math.max(...inks))}（均 ${f(avg(inks))}） · 覆盖率比值最低 ${f(Math.min(...covs))}（P${rows[covs.indexOf(Math.min(...covs))].p}）`);
console.log(`3D 层墨量比值 ${f(Math.min(...sol))}–${f(Math.max(...sol))}（均 ${f(avg(sol))}） · 覆盖率比值最低 ${f(Math.min(...sco))}（P${rows[sco.indexOf(Math.min(...sco))].p}）`);
const ji = process.argv.indexOf('--json');
if (ji > 0 && process.argv[ji + 1]) writeFileSync(process.argv[ji + 1], JSON.stringify(rows, null, 1));
