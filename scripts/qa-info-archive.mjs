// 离线归档验收：单文件 + 断网打开 ⇒ three 拉不到 ⇒ 6s 看门狗钉死 poster ⇒ **完整可读的 2D 版**
import { chromium } from 'playwright-core';
const F = 'file:///home/claude/eco-review/convoai-info-速讲版-8p.html';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args:['--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport:{width:1920,height:1080}, offline:true });
const pg = await ctx.newPage();
const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
await pg.goto(F, { waitUntil:'load' });
await pg.waitForTimeout(9000);
const r = await pg.evaluate(()=>{
  const c=document.getElementById('labGl');
  const per={};
  [1,2,3,4,5,8].forEach(p=>{ const st=document.querySelector(`.slide[data-p="${p}"] .lab-stage`);
    const ps=[...document.querySelectorAll(`.slide[data-p="${p}"] .lab-poster`)];
    per[p]={ glup: st.classList.contains('gl-up'),
             op: ps.map(e=>+getComputedStyle(e).opacity),
             n: ps.reduce((n,g)=>n+g.querySelectorAll('path,rect,circle,line,polygon,ellipse').length,0) }; });
  return { mode:c.dataset.labMode, run:c.dataset.labRun, parent:c.parentNode.className,
    txt:[...document.querySelectorAll('.slide')].map(s=>s.textContent.replace(/\s+/g,'').length),
    imgs:[...document.querySelectorAll('.slide img')].filter(i=>!i.complete||i.naturalWidth===0).length,
    frame: !!document.getElementById('engineFrame').getAttribute('srcdoc'),
    per,
    all: document.getElementById('deckStage').textContent.replace(/\s+/g,' ') };
});
const must=['No.1','100万+','900亿+','50+','96.5%','2,475','三条支流，一条河','集贤科技','莲偶科技','豆神 AI','IDC'];
console.log('mode=%s run=%s parent=%s srcdoc=%s 图未加载=%d', r.mode, r.run, r.parent, r.frame, r.imgs);
console.log('每页正文字数', r.txt.join('/'));
console.log('poster:', JSON.stringify(r.per));
console.log('口径缺失:', must.filter(m=>!r.all.includes(m)));
console.log('pageerror:', errs.slice(0,3));
await b.close();
