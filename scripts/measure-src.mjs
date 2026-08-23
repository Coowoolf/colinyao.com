// 小字量尺（2026-08-23 加 · 配 SOURCE ledger 与 kicker 消歧两项用）：
// 逐页量一类元素的**声明盒**与**真实字形框**，报两者之差 —— 盒虚开（字远小于盒）会让
// 「不越界」这类闸失效，盒装不下（over > 0）则是当场溢出。同时回报 computed 的
// font-size / color / opacity，用来自证「字号提一档」这类改动真的落到了页面上。
// 用法：URL=… [THEME=dark] [SEL=.src|.sig|.kk] node scripts/measure-src.mjs
// 只读 deck，不改 deck。
import { chromium } from 'playwright-core';
const URL = process.env.URL, THEME = process.env.THEME || 'light';
const SEL = process.env.SEL || '.src';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme','dark'); } catch(e){} });
const pg = await ctx.newPage();
await pg.goto(URL + '#1', { waitUntil: 'load' });
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(400);
const r = await pg.evaluate((sel) => {
  const out = [];
  document.querySelectorAll('.slide').forEach((s, i) => {
    s.classList.add('active','visible');
    s.querySelectorAll('[data-step]').forEach(x => x.classList.add('on'));
    s.querySelectorAll(sel).forEach(el => {
      const box = el.getBoundingClientRect();
      const rg = document.createRange(); rg.selectNodeContents(el);
      const gr = rg.getBoundingClientRect();
      const cs = getComputedStyle(el);
      out.push({ p: i+1, txt: (el.textContent||'').trim().slice(0,70),
        boxL: Math.round(box.left), boxR: Math.round(box.right), boxW: Math.round(box.width),
        inkL: Math.round(gr.left), inkR: Math.round(gr.right), inkW: Math.round(gr.width),
        inkT: Math.round(gr.top), inkB: Math.round(gr.bottom),
        over: Math.round(gr.width - box.width), fs: cs.fontSize, col: cs.color, op: cs.opacity });
    });
  });
  return out;
}, SEL);
for (const x of r) console.log(`P${String(x.p).padStart(2)} ${x.fs} ${x.col} op=${x.op} box[${x.boxL}..${x.boxR}]w${x.boxW} ink[${x.inkL}..${x.inkR}]w${x.inkW} y[${x.inkT}..${x.inkB}] over=${x.over>0?'+'+x.over:'0'} 「${x.txt}」`);
await b.close();
