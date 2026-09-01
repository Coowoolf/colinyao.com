// 逐页实拍（双主题 · 定拍 · ?lab=hold）—— 交付物与终审素材都走这一支
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const BASE = process.env.BASE || 'http://localhost:8899';
const OUT = process.env.OUT || '/home/claude/eco-review';
const DECK = process.env.DECK || '/decks/convoai-info.html';
const PAGES = (process.env.P || '1,2,3,4,5,6,7,8').split(',').map(Number);
const THEMES = (process.env.TH || 'light,dark').split(',');
const TAG = process.env.TAG || 'info';
const CLIP = process.env.CLIP === '1';
const SEEK = +(process.env.SEEK || 6);
const STEPS = process.env.STEPS === '1';
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
for (const th of THEMES) {
  const ctx = await b.newContext({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
  await ctx.addInitScript((t)=>{ try{ localStorage.setItem('colin-theme', t); }catch(e){} }, th);
  const pg = await ctx.newPage();
  await pg.goto(BASE + DECK + '?lab=hold#1', { waitUntil:'load' });
  await pg.waitForTimeout(6500);
  for (const P of PAGES) {
    await pg.evaluate(k=>window.deck.go(k-1), P);
    await pg.waitForTimeout(2600);
    if (STEPS) { await pg.evaluate(k=>document.querySelectorAll(`.slide[data-p="${k}"] [data-step]`)
      .forEach(e=>e.classList.add('on')), P); await pg.waitForTimeout(1200); }
    await pg.evaluate((t)=>{ const T=window.__labTour; if(T&&T.unit&&T.unit()){ T.pace(30); T.seek(t);} }, SEEK);
    await pg.waitForTimeout(200);
    const clip = CLIP ? await pg.evaluate((k)=>{ const el=document.querySelector(`.slide[data-p="${k}"] .lab-stage`);
      if(!el) return null; const r=(el.dataset.labRect||'').split(',').map(Number);
      return { x:r[0], y:r[1], width:r[2], height:r[3] }; }, P) : null;
    await pg.screenshot({ path:`${OUT}/${TAG}-p${P}-${th}.png`, clip: clip || { x:0,y:0,width:1920,height:1080 } });
    await pg.evaluate(()=>{ const T=window.__labTour; if(T) T.pace(0); });
  }
  await ctx.close();
}
await b.close();
console.log('shot →', OUT);
