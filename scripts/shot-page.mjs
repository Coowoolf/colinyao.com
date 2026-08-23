// 终审素材取帧器（2026-08-23 加）：把 deck 的指定页 / 指定主题 / 指定步进态钉成静态一帧。
// 与 pinned-diff.mjs 的取帧姿势逐条同源（KILL 归零 → 等字体 → 等背景板与图解码 →
// 三帧之后再翻页，绕开 deck.js 那对 rAF）—— 所以出的图与 qa / 遮挡扫描量到的是同一帧。
// 用法：URL=… PAGE=7 THEME=light OUT=/tmp/a.png [STEP=0] [CLIP=x,y,w,h] node scripts/shot-page.mjs
//   STEP 省略 = 终态（全部 [data-step] 都 on）；CLIP 省略 = 整幅 1920×1080。
// 配 scripts/compose-review.py 拼对照图。只读 deck，不改 deck。
import { chromium } from 'playwright-core';
const URL = process.env.URL, PAGE = +(process.env.PAGE || 1), THEME = process.env.THEME || 'light';
const OUT = process.env.OUT, STEP = +(process.env.STEP || 9);
const CLIP = process.env.CLIP ? process.env.CLIP.split(',').map(Number) : null;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme','dark'); } catch(e){} });
const pg = await ctx.newPage();
await pg.goto(URL + '#1', { waitUntil: 'load' });
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.evaluate(() => document.fonts.ready);
await pg.evaluate(() => { const u=new Set(); document.querySelectorAll('.conf-bg').forEach(el=>{const m=/url\("?([^")]+)"?\)/.exec(getComputedStyle(el).backgroundImage); if(m)u.add(m[1]);}); [...document.images].forEach(i=>u.add(i.currentSrc||i.src)); return Promise.all([...u].filter(Boolean).map(s=>new Promise(r=>{const im=new Image(); im.onload=im.onerror=()=>r(); im.src=s;}))); });
await pg.evaluate(({k,st}) => new Promise((res)=>{ const run=()=>{ document.querySelectorAll('.slide').forEach(el=>el.classList.remove('visible')); void document.body.offsetWidth; document.querySelectorAll('.slide').forEach((el,j)=>{ el.classList.toggle('active', j===k-1); el.classList.toggle('visible', j===k-1); el.querySelectorAll('[data-step]').forEach(x=>{ if((+x.dataset.step||0)<=st) x.classList.add('on'); else x.classList.remove('on'); }); }); res(); }; requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(run))); }), {k:PAGE, st:STEP});
await pg.waitForTimeout(800);
await pg.screenshot({ path: OUT, clip: CLIP ? {x:CLIP[0],y:CLIP[1],width:CLIP[2],height:CLIP[3]} : {x:0,y:0,width:1920,height:1080} });
await b.close();
console.log('· ' + OUT);
