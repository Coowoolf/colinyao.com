// ⑳ink · 3D 层「浅 / 暗墨量比」实测（LAB 家族浅底 deck 的专用闸）
//   同一支尺：TOUR.shot().ink = 该页 3D 层的平均 alpha（画了多少墨）。
//   暗底走加色混合、浅底走正常混合 ⇒ 浅色中间调天生容易塌；目标比值 ≥ 0.90。
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8899';
const DECK = process.env.DECK || '/decks/convoai-info.html';
const PAGES = (process.env.P || '1,2,3,4,5,8').split(',').map(Number);
const SEEK = +(process.env.SEEK || 6);
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
const out = {};
for (const th of ['light','dark']) {
  const ctx = await b.newContext({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
  await ctx.addInitScript((t)=>{ try{ localStorage.setItem('colin-theme', t); }catch(e){} }, th);
  const pg = await ctx.newPage();
  await pg.goto(BASE + DECK + '?lab=hold#1', { waitUntil:'load' });
  await pg.waitForTimeout(6500);
  for (const P of PAGES) {
    await pg.evaluate(k=>window.deck.go(k-1), P); await pg.waitForTimeout(2000);
    const s = await pg.evaluate((t)=>{ const T=window.__labTour; T.pace(30); T.seek(t);
      const q=T.shot(4,4); T.pace(0); return { ink:q.ink, cov:q.cov, mean:q.mean }; }, SEEK);
    (out[P] = out[P] || {})[th] = s;
  }
  await ctx.close();
}
await b.close();
let bad = 0;
console.log('页  浅 ink      暗 ink      浅/暗     浅 cov   暗 cov');
for (const P of PAGES) {
  const r = out[P].light.ink / out[P].dark.ink;
  if (r < 0.90) bad++;
  console.log(`P${P}  ${out[P].light.ink.toFixed(5)}   ${out[P].dark.ink.toFixed(5)}   ${r.toFixed(3)} ${r<0.9?' ✗':' ✓'}   ${out[P].light.cov.toFixed(4)}  ${out[P].dark.cov.toFixed(4)}`);
}
console.log(bad ? `✗ ${bad} 页浅/暗墨量比 < 0.90` : '✓ 全部 ≥ 0.90');
process.exit(bad ? 1 : 0);
