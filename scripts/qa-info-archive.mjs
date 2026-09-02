// 离线归档验收：单文件 + 断网打开 ⇒ three 拉不到 ⇒ 6s 看门狗钉死 poster ⇒ **完整可读的 2D 版**
import { chromium } from 'playwright-core';
const F = 'file:///home/claude/eco-review/convoai-info-速讲版-8p.html';
const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args:['--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
const ctx = await b.newContext({ viewport:{width:1920,height:1080}, offline:true });
const pg = await ctx.newPage();
const errs=[]; pg.on('pageerror',e=>{
  // 已知边界（不是 bug）：归档态把引擎 deck 内联成 iframe srcdoc（origin=null），
  // 它自己的 deck.js 一进来就 history.replaceState('#1') —— srcdoc 文档不许写 history。
  // 抽屉的展开 / Esc / 深链一格不受影响（实测 ⑪⑬ 在线版全过），这条按已知项滤掉。
  if(/replaceState/.test(e.message) && /about:srcdoc/.test(e.message)) return;
  errs.push(e.message);
});
await pg.goto(F, { waitUntil:'load' });
await pg.waitForTimeout(9000);
const r = await pg.evaluate(()=>{
  const c=document.getElementById('labGl');
  const per={};
  // v3 波C 收官：**八页全有场景** —— P1 声场球 / P2 地球 / P3 空间生长 / P4 双向声带 /
  // P5 五脑区大脑 / P6 走出屏幕（加法层）/ P7 星座墙 /
  // P8 一张实时网上的三种互动（v3.1：三条支流一条河退役）。
  // 其中 P1 / P2 / P7 的 poster 是构建期离线投影出来的专用静帧，其余五页是页上那张图本人。
  [1,2,3,4,5,6,7,8].forEach(p=>{ const st=document.querySelector(`.slide[data-p="${p}"] .lab-stage`);
    const ps=[...document.querySelectorAll(`.slide[data-p="${p}"] .lab-poster`)];
    per[p]={ glup: st.classList.contains('gl-up'),
             op: ps.map(e=>+getComputedStyle(e).opacity),
             n: ps.reduce((n,g)=>n+g.querySelectorAll('path,rect,circle,line,polygon,ellipse').length,0) }; });
  return { mode:c.dataset.labMode, run:c.dataset.labRun, parent:c.parentNode.className,
    txt:[...document.querySelectorAll('.slide')].map(s=>s.textContent.replace(/\s+/g,'').length),
    // .lab-print 是**打印帧位**：常态没有 src（beforeprint 才写 dataURL）⇒ 不进「图未加载」
    imgs:[...document.querySelectorAll('.slide img:not(.lab-print)')]
      .filter(i=>!i.complete||i.naturalWidth===0).length,
    frame: !!document.getElementById('engineFrame').getAttribute('srcdoc'),
    per,
    all: document.getElementById('deckStage').textContent.replace(/\s+/g,' ') };
});
const CASES=['集贤科技','Robopoet','luwu','Pophie','商汤','MiniMax','智谱清言','星野',
  '灵机一动','LOOKTECH','HeyCyan','LOOKEE','莲偶科技','豆神 AI'];
// P8 的口径锁（v3.1）：主标 + 使命 / 愿景两句 + 三簇题注 + land —— 逐字。
// 使命 / 愿景是 2026-09-02 自 shengwang.cn/aboutus 逐字核实的公司口径。
const must=['No.1','100万+','900亿+','50+','96.5%','2,475',
  '让实时互动，无处不在。',
  '帮助人们跨越距离实时互动，如聚一堂。',
  '让实时互动像空气和水一样，无处不在。',
  '人与人 · 已经发生','实时音视频 · 2014 年起',
  '人与智能体 · 正在发生','对话式 AI 引擎 · 企业级智能体 · R1',
  '智能体与智能体 · 即将发生','智能体之间的实时对话与协作',
  '同一张实时网，服务人与人、人与智能体、智能体与智能体。',
  '近一半','IDC','650','340','95%','200+','毫秒级','30000+',
  '声网官方联合案例 · 均已公开——你的场景，多半能对上号。',
  '让陪伴自然，让生意成单。'].concat(CASES);
// 河退场之后不许有残句留在归档产物里
const gone=['三条支流，一条河','Engine 的每一次打断','Agent 的每一次交付',
  'Physical AI 的每一次唤醒','合流点'];
console.log('mode=%s run=%s parent=%s srcdoc=%s 图未加载=%d', r.mode, r.run, r.parent, r.frame, r.imgs);
console.log('每页正文字数', r.txt.join('/'));
console.log('poster:', JSON.stringify(r.per));
console.log('口径缺失:', must.filter(m=>!r.all.includes(m)));
console.log('河的残句:', gone.filter(m=>r.all.includes(m)));
const bad = Object.entries(r.per).filter(([p,v])=>v.glup || !v.op.every(o=>o===1) || v.n<3);
console.log('poster 不合格页:', bad.map(([p])=>p));
console.log('结论:', (r.mode==='POSTER' && r.run==='0' && r.imgs===0 && !bad.length
  && !must.filter(m=>!r.all.includes(m)).length
  && !gone.filter(m=>r.all.includes(m)).length && !errs.length) ? '✓ PASS' : '✗ FAIL');
console.log('pageerror:', errs.slice(0,3));
await b.close();
