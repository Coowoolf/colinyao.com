// QA · convoai-info v2（8 页 · CONF 家族 · 双主题 · P4/P5/P7 各 1 步 build）
// 2026-08-21 家族语言重建轮改写。闸门清单：
//   ①  页数 N=8 / noindex / 页码 sig / 主题态 / console 零错
//   ②  分步：逐页比对 data-steps 与页内 [data-step] 最大值（两边必须自洽）
//   ③  溢出：画布溢出 + 卡内溢出（含 card-c 深层孙节点）
//   ④  背景板：每页恰一块、板型对、主题源对
//   ⑤  P1 hero-art 双源互斥 + ⑨ hero 盒不出画布
//   ⑥  逐页图片真加载
//   ⑦  deckSwap 真实切换（板源 + hero 双源 + eco 双源）+ **常显闸**（opacity ≥ .5）
//   ⑩  P7 eco-art 双源可见性与主题
//   ⑪  引擎详解抽屉：chip「22 页」/ Enter 展开 / iframe 22 页 / Esc 收回 / 方向键恢复 /
//       引擎 deck 自身可达 + **主题跟随**（宿主切主题 → iframe 内 data-theme 跟着翻）
//   ⑬  **深链**：P5 → 引擎 #16（Call Agent 章）· P6 → 引擎 #19（R1）——
//       断言 iframe 内 .slide.active 的 data-p 落点；P4 → #1
//   ⑫  口径锁：P2 四大数 + 近一半 + IDC 注 + SOURCE / P5 96.5% + 2,475 / P8 三不三步逐字
//   ⑭  红线反向闸：价格 / staging / 引擎 P16 的「盲测 · 32,000」/ 旧分类学 / 旧措辞
//   ⑮  P7 案例墙 14 家客户名逐字（名单硬编码在本文件，改名必须两处同改）
// 用法：node scripts/qa-convoai-info.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8899 node scripts/qa-convoai-info.mjs
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8777';
const N = 8;
const EXP_STEPS = [0, 0, 0, 1, 1, 0, 1, 0];
const BOARD = { 1: 'title' };            // 其余一律 content
const HERO = { 1: 'hero-cover-v2' };     // hero-art 只上封面
const ECO = { 7: 'ecosystem-stack-v4' }; // eco-art 只上 P7 生态主视觉（polish-v4）
// P7 案例墙客户名：逐字对照公开卡片上烧录的品牌（客户当面的 deck 一字不能错）
const CASES = ['集贤科技', 'Robopoet', 'luwu',
  'Pophie', '商汤', 'MiniMax', '智谱清言', '星野', '灵机一动',
  'LOOKTECH', 'HeyCyan', 'LOOKEE', '莲偶科技', '豆神 AI'];
// 深链契约：页 → 引擎章号
const DEEPLINK = [{ page: 5, chip: 'agentExpand', hash: 16 }, { page: 6, chip: 'physExpand', hash: 19 }];
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const errs = [];
pg.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
pg.on('console', m => {
  if (m.type() === 'error' && !(m.location()?.url || '').includes('favicon')) errs.push(m.text());
});
if (THEME === 'dark') await pg.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
await pg.goto(BASE + '/decks/convoai-info.html#1', { waitUntil: 'load' });
// 动效归零：入场是 transition（.rise 起手 translateY(42px)），不掐掉就会把「还没落位」
// 读成「卡片冲出 .sh 盒」的假溢出（occlusion-scan.mjs 同一手法）
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.waitForTimeout(900);

// ① 页数 + noindex + sig + 主题态
const meta = await pg.evaluate(() => ({
  n: document.querySelectorAll('.slide').length,
  noindex: !!document.querySelector('meta[name="robots"][content*="noindex"]'),
  sigs: [...document.querySelectorAll('.slide .sig')].map(s => s.textContent),
  theme: document.documentElement.getAttribute('data-theme'),
}));
ok(meta.n === N, `① 页数 ${meta.n} != ${N}`);
ok(meta.noindex, '① 缺 noindex');
ok(meta.sigs.length === N && meta.sigs.every((s, i) => s === `${i + 1}/${N}`), '① 页码 sig 不齐');
ok(THEME === 'dark' ? meta.theme === 'dark' : meta.theme !== 'dark', `① 主题态异常 ${meta.theme}`);

// ② 分步数：逐页比对 data-steps 与页内 [data-step] 的最大值
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => +s.dataset.steps));
EXP_STEPS.forEach((e, i) => ok(steps[i] === e, `② P${i + 1} steps ${steps[i]} != ${e}`));
const stepMax = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map((s) => {
  const els = [...s.querySelectorAll('[data-step]')];
  return els.length ? Math.max(...els.map(e => +e.dataset.step || 0)) : 0;
}));
EXP_STEPS.forEach((e, i) => ok(stepMax[i] === e,
  `② P${i + 1} 页内 [data-step] 最大值 ${stepMax[i]} != data-steps ${e}`));

// ③④⑤⑥ 逐页：板、hero、图、溢出
for (let i = 1; i <= N; i++) {
  const r = await pg.evaluate((n) => {
    document.querySelectorAll('.slide').forEach((el, k) => {
      el.classList.toggle('active', k === n - 1); el.classList.toggle('visible', k === n - 1);
    });
    const s = document.querySelectorAll('.slide')[n - 1];
    s.querySelectorAll('[data-step]').forEach(el => el.classList.add('on'));   // 量终态
    const bgs = [...s.querySelectorAll('.conf-bg')];
    const bgCls = bgs.length === 1 ? [...bgs[0].classList].find(c => c.startsWith('conf-bg-')) : null;
    const bgUrl = bgs.length === 1 ? getComputedStyle(bgs[0]).backgroundImage : '';
    const heroes = [...s.querySelectorAll('.hero-art')].map(h => ({
      cls: h.className, vis: getComputedStyle(h).display !== 'none', w: h.naturalWidth, fit: getComputedStyle(h).objectFit,
      // ⑨ hero 盒必须整个待在画布里：读内联 left/width，不读 rect（rect 会被舞台裁掉看不出病）
      box: { l: parseFloat(h.style.left), t: parseFloat(h.style.top),
             w: parseFloat(h.style.width), h: parseFloat(h.style.height) },
    }));
    const ecos = [...s.querySelectorAll('.eco-art')].map(e => ({
      cls: e.className, vis: getComputedStyle(e).display !== 'none', w: e.naturalWidth,
      fit: getComputedStyle(e).objectFit, src: e.getAttribute('src'),
    }));
    const badImgs = [...s.querySelectorAll('.pp img')].filter(im => !im.complete || im.naturalWidth === 0).map(im => im.src);
    const out = [];
    s.querySelectorAll('.pp .sh').forEach(el => {
      const r0 = el.getBoundingClientRect();
      [...el.children].forEach(ch => {
        const r1 = ch.getBoundingClientRect();
        if (r1.bottom > 1080 - 6 || r1.right > 1920 + 6 || r1.left < -6) out.push('canvas:' + (el.className || '').slice(0, 40));
      });
      if (el.className.match(/card-c|kpi|five|g12|mx|case|frame|face|cap/)) {
        [...el.children].forEach(ch => {
          if (ch.getBoundingClientRect().bottom > r0.bottom + 6) out.push('cardspill:' + (el.className || '').slice(0, 44));
        });
      }
    });
    // 卡内溢出第二道：card-c 里那层 padding 容器的孙节点也不许冲出卡底
    s.querySelectorAll('.pp .sh.card-c').forEach(el => {
      const r0 = el.getBoundingClientRect();
      el.querySelectorAll('*').forEach(ch => {
        if (ch.getBoundingClientRect().bottom > r0.bottom + 6) out.push('deepspill:' + (el.className || '').slice(0, 44));
      });
    });
    return { bgN: bgs.length, bgCls, bgUrl, heroes, ecos, badImgs, out };
  }, i);
  ok(r.bgN === 1, `④ P${i} conf-bg 数 ${r.bgN}`);
  const expB = BOARD[i] || 'content';
  ok(r.bgCls === 'conf-bg-' + expB, `④ P${i} 板 ${r.bgCls} != ${expB}`);
  ok(r.bgUrl.includes(THEME === 'dark' ? '-dark.png' : '-light.png'), `④ P${i} 板主题源不符`);
  if (HERO[i]) {
    ok(r.heroes.length === 2, `⑤ P${i} hero 数 ${r.heroes.length}`);
    const vis = r.heroes.filter(h => h.vis);
    ok(vis.length === 1, `⑤ P${i} hero 可见数 ${vis.length}`);
    if (vis[0]) {
      ok(vis[0].cls.includes(THEME === 'dark' ? 'dk' : 'lt'), `⑤ P${i} hero 主题错`);
      ok(vis[0].w === 2048, `⑤ P${i} hero 未加载`);
      ok(vis[0].fit === 'contain', `⑤ P${i} hero fit=${vis[0].fit}`);
    }
    r.heroes.forEach((h) => {
      ok(Number.isFinite(h.box.l) && Number.isFinite(h.box.w), `⑨ P${i} hero 盒缺 left/width`);
      ok(h.box.l + h.box.w <= 1920, `⑨ P${i} hero 出画布 left+width=${h.box.l + h.box.w} > 1920`);
      ok(h.box.t + h.box.h <= 1080, `⑨ P${i} hero 出画布 top+height=${h.box.t + h.box.h} > 1080`);
    });
  } else {
    ok(r.heroes.length === 0, `⑤ P${i} 不应有 hero`);
  }
  if (ECO[i]) {
    ok(r.ecos.length === 2, `⑩ P${i} eco-art 数 ${r.ecos.length}`);
    const ev = r.ecos.filter(e => e.vis);
    ok(ev.length === 1, `⑩ P${i} eco-art 可见数 ${ev.length}`);
    if (ev[0]) {
      ok(ev[0].cls.includes(THEME === 'dark' ? 'dk' : 'lt'), `⑩ P${i} eco-art 主题错 ${ev[0].cls}`);
      ok(ev[0].src.includes(`${ECO[i]}-${THEME}.webp`), `⑩ P${i} eco-art 源不符 ${ev[0].src}`);
      ok(ev[0].w > 0, `⑩ P${i} eco-art 未加载 naturalWidth=${ev[0].w}`);
      ok(ev[0].fit === 'cover', `⑩ P${i} eco-art fit=${ev[0].fit}`);
    }
  } else {
    ok(r.ecos.length === 0, `⑩ P${i} 不应有 eco-art`);
  }
  ok(r.badImgs.length === 0, `⑥ P${i} 图未加载 ${r.badImgs.join()}`);
  [...new Set(r.out)].forEach(o => fails.push(`③ P${i} 溢出 ${o}`));
  await pg.waitForTimeout(60);
}

// ⑦ 主题切换：deckSwap 常显 + 真实切换（板源 + hero-art 双源 + eco 双源）
const swapVis = await pg.evaluate(() => {
  const b = document.getElementById('deckSwap');
  const cs = b ? getComputedStyle(b) : null;
  return b ? { op: +cs.opacity, disp: cs.display } : null;
});
ok(!!swapVis, '⑦ 缺 #deckSwap');
if (swapVis) ok(swapVis.disp !== 'none' && swapVis.op >= 0.5,
  `⑦ deckSwap 未常显（opacity=${swapVis.op}）—— 对外发链接的 deck 不能藏切换键`);
await pg.evaluate(() => {
  window.deck.i = 0;
  document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === 0));
});
await pg.click('#deckSwap');
await pg.waitForTimeout(400);
const sw = await pg.evaluate(() => {
  const s = document.querySelectorAll('.slide')[0];
  const p7 = document.querySelectorAll('.slide')[6];
  const disp = (root, sel) => { const e = root.querySelector(sel); return e ? getComputedStyle(e).display : 'MISSING'; };
  return {
    theme: document.documentElement.getAttribute('data-theme'),
    bg: getComputedStyle(s.querySelector('.conf-bg')).backgroundImage,
    lt: disp(s, '.hero-art.lt'), dk: disp(s, '.hero-art.dk'),
    elt: disp(p7, '.eco-art.lt'), edk: disp(p7, '.eco-art.dk'),
  };
});
const flipped = THEME === 'dark' ? 'light' : 'dark';
ok(THEME === 'dark' ? sw.theme !== 'dark' : sw.theme === 'dark', `⑦ 切换后主题态 ${sw.theme}`);
ok(sw.bg.includes('-' + flipped + '.png'), '⑦ 切换后板源未换');
ok(flipped === 'dark' ? (sw.lt === 'none' && sw.dk === 'block') : (sw.dk === 'none' && sw.lt === 'block'),
   `⑦ hero 双源 ${sw.lt}/${sw.dk}`);
ok(flipped === 'dark' ? (sw.elt === 'none' && sw.edk === 'block') : (sw.edk === 'none' && sw.elt === 'block'),
   `⑩ 切换后 eco 双源 ${sw.elt}/${sw.edk}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

// ⑪ 引擎详解抽屉：chip → Enter 展开 → Esc 收回 → deck 按键恢复 → 引擎 deck 自身可达
async function goPage(n, pushSteps) {
  await pg.evaluate(() => { document.activeElement?.blur(); });
  await pg.evaluate((k) => { location.hash = '#' + k; }, n);
  await pg.waitForTimeout(2400);   // 等整页入场走完：.slide 的 visibility 有 .52s 延迟
  for (let k = 0; k < (pushSteps || 0); k++) { await pg.keyboard.press('ArrowRight'); await pg.waitForTimeout(800); }
}
await goPage(4, 1);   // P4 的 04 · OPEN 那行 chips（含 #engineExpand）落在 step1
const chip = await pg.evaluate(() => {
  const c = document.getElementById('engineExpand');
  if (!c) return null;
  const r = c.getBoundingClientRect(), cs = getComputedStyle(c);
  const p4 = document.querySelector('.slide[data-p="4"]');
  return {
    txt: c.textContent, w: r.width, h: r.height, hash: c.getAttribute('data-eng-hash'),
    vis: cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > .01,
    inP4: !!p4 && p4.contains(c), cur: document.querySelector('.slide.active')?.dataset.p,
  };
});
ok(!!chip, '⑪ P4 缺 #engineExpand');
if (chip) {
  ok(chip.inP4, '⑪ #engineExpand 不在 P4 内');
  ok(chip.cur === '4', `⑪ 导航到 P4 失败，当前 P${chip.cur}`);
  ok(chip.vis && chip.w > 0 && chip.h > 0, `⑪ chip 不可见 ${chip.w}×${chip.h}`);
  ok(chip.txt.includes('引擎产品详解'), `⑪ chip 文案不符「${chip.txt}」`);
  ok(chip.txt.includes('22 页'), `⑪ chip 页数口径未跟随引擎 deck 扩章（应含「22 页」）「${chip.txt}」`);
  ok(chip.hash === '1', `⑪ P4 深链章号 ${chip.hash} != 1`);
}
const frameSecs = () => pg.waitForFunction(() => {
  const f = document.getElementById('engineFrame');
  const d = f && f.contentDocument;
  return (d && d.readyState === 'complete' && d.querySelectorAll('section').length)
    ? d.querySelectorAll('section').length : false;
}, null, { timeout: 12000 }).then(h => h.jsonValue()).catch(() => 0);

if (THEME !== 'dark') {                       // overlay 是主题无关层：全套只在浅色跑一遍
  await pg.keyboard.press('Enter');           // ② Enter 展开
  await pg.waitForTimeout(250);
  ok(await pg.evaluate(() => document.getElementById('engineOverlay').hidden) === false,
     '⑪ Enter 未展开 overlay');
  const secs = await frameSecs();
  ok(secs === 22, `⑪ iframe 内 section 数 ${secs} != 22`);
  await pg.waitForTimeout(600);
  const p4land = await pg.evaluate(() => {
    const d = document.getElementById('engineFrame').contentDocument;
    return d.querySelector('.slide.active')?.dataset.p;
  });
  ok(p4land === '1', `⑬ P4 深链落点 P${p4land} != 1`);
  const focused = await pg.evaluate(() => document.activeElement?.id);
  ok(focused === 'engineFrame', `⑪ 展开后焦点不在 iframe（${focused}）`);

  // ⑪ 主题跟随：抽屉开着时宿主切主题，iframe 内必须 live-sync
  await pg.evaluate(() => { window.__setTheme('dark'); });
  await pg.waitForTimeout(500);
  const innerDark = await pg.evaluate(() => document.getElementById('engineFrame')
    .contentDocument.documentElement.getAttribute('data-theme'));
  ok(innerDark === 'dark', `⑪ 抽屉主题未跟随宿主（iframe data-theme=${innerDark}）`);
  await pg.evaluate(() => { window.__setTheme('light'); });
  await pg.waitForTimeout(400);
  const innerLight = await pg.evaluate(() => document.getElementById('engineFrame')
    .contentDocument.documentElement.getAttribute('data-theme'));
  ok(innerLight !== 'dark', `⑪ 抽屉主题回切失败（iframe data-theme=${innerLight}）`);

  await pg.keyboard.press('Escape');          // ③ Esc 收回（焦点在 iframe 内）
  await pg.waitForTimeout(300);
  ok(await pg.evaluate(() => document.getElementById('engineOverlay').hidden) === true,
     '⑪ Esc 未收回 overlay');
  await pg.keyboard.press('ArrowRight');      // deck 按键必须回来：P4 → P5
  await pg.waitForTimeout(400);
  const after = await pg.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
  ok(after === '5', `⑪ Esc 后方向键失灵，当前 P${after}`);

  // ⑬ 深链：P5 → 引擎 #16（Call Agent 章）· P6 → 引擎 #19（R1）
  for (const dl of DEEPLINK) {
    await goPage(dl.page, 0);
    const c = await pg.evaluate((id) => {
      const el = document.getElementById(id);
      if (!el) return null;
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      return { hash: el.getAttribute('data-eng-hash'), txt: el.textContent,
               vis: cs.display !== 'none' && +cs.opacity > .01 && r.width > 0 };
    }, dl.chip);
    ok(!!c, `⑬ P${dl.page} 缺 #${dl.chip}`);
    if (c) {
      ok(c.vis, `⑬ P${dl.page} 深链 chip 不可见`);
      ok(c.hash === String(dl.hash), `⑬ P${dl.page} 深链章号 ${c.hash} != ${dl.hash}`);
    }
    await pg.keyboard.press('Enter');
    await pg.waitForTimeout(300);
    ok(await pg.evaluate(() => document.getElementById('engineOverlay').hidden) === false,
       `⑬ P${dl.page} Enter 未展开 overlay`);
    await frameSecs();
    // 深链跳转要给 hashchange → deck.go → 入场一点时间
    const landed = await pg.waitForFunction((h) => {
      const d = document.getElementById('engineFrame').contentDocument;
      const a = d && d.querySelector('.slide.active');
      return a && a.dataset.p === String(h) ? a.dataset.p : false;
    }, dl.hash, { timeout: 8000 }).then(x => x.jsonValue()).catch(() => null);
    ok(landed === String(dl.hash),
       `⑬ P${dl.page} 深链未落在引擎 #${dl.hash}（实测 ${landed}）`);
    await pg.keyboard.press('Escape');
    await pg.waitForTimeout(300);
    ok(await pg.evaluate(() => document.getElementById('engineOverlay').hidden) === true,
       `⑬ P${dl.page} Esc 未收回`);
  }

  // ④ 引擎 deck 本体：200 + noindex + 22 页
  const res = await fetch(BASE + '/decks/convoai-engine.html');
  const html = await res.text();
  ok(res.status === 200, `⑪ convoai-engine.html HTTP ${res.status}`);
  ok(/noindex/.test(html), '⑪ convoai-engine.html 缺 noindex');
  const nSec = (html.match(/<section/g) || []).length;
  ok(nSec === 22, `⑪ convoai-engine.html section 数 ${nSec} != 22`);
}

// ⑫⑭⑮ 口径闸 / 红线反向闸 / 案例墙名单闸
const T = async (k) => pg.evaluate((n) =>
  document.querySelector(`.slide[data-p="${n}"]`).textContent.replace(/\s+/g, ' '), k);
const [t2, t3, t4, t5, t6, t7, t8] = await Promise.all([T(2), T(3), T(4), T(5), T(6), T(7), T(8)]);
const ALL = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));

// P2 · Why Agora 口径锁（与引擎 P21 逐字同源）
[['No.1', t2], ['稳居第一 · 份额超过第 2–8 位总和', t2], ['50+', t2],
 ['突破性自主创新技术（全球发明专利）', t2], ['100万+', t2], ['全球注册应用数', t2],
 ['900亿+', t2], ['单月支撑通话分钟数', t2],
 ['注：IDC《中国视频云市场报告》音视频通信（RTC）赛道 · 份额超过第 2–8 位厂商总和', t2],
 ['SOURCE · 声网官网 / IR 公开口径 · IDC 中国视频云市场报告 · 事实截止 2026.08', t2],
 ['集成 RTC 的 Top 10,000（MAU）App 里，近一半使用声网', t2],
 ['全球首批 Realtime API', t2], ['2024.10.01', t2],
 ['OpenAI Realtime API · Agora 全球首批合作伙伴', t2]]
  .forEach(([n, txt]) => ok(txt.includes(n), `⑫ P2 缺「${n}」`));
// 禁止回归的旧错误数字与旧口径
['93万', '700亿', '对话式 AI 引擎市场占有率', '200+ 覆盖场景', '全球首个 Realtime API', '43.4%']
  .forEach(n => ok(!ALL.includes(n), `⑭ P2 旧口径回归：「${n}」`));

// P3 · 分类学统一（底座 → 三条产品线 → Engine 两种交付形态）
[['一个实时底座，三条产品线', t3], ['ENGINE DELIVERY FORMS', t3], ['两种交付形态', t3],
 ['配套能力 · 工具', t3], ['实时底座 · RTE', t3], ['TEN 开源工具库', t3],
 ['AI 模型评测平台', t3], ['实时转录翻译', t3], ['开发套件', t3]]
  .forEach(([n, txt]) => ok(txt.includes(n), `⑫ P3 缺「${n}」`));
['三台引擎', '两大产品引擎', 'THREE ENGINES', 'DUAL FORM'].forEach(n =>
  ok(!ALL.includes(n), `⑭ 旧分类学口径回归：「${n}」`));

// P4 · Engine 口径
[['超低延迟、可打断、高自然度', t4], ['2025.02.18 · v1.0 公测', t4], ['2026.08.11 · v2.11 最新', t4],
 ['VS LIVEKIT · 2026-03 同题评测 · 默认配置口径', t4], ['优雅打断 2.0', t4],
 ['模型会换代，接口不换人。', t4]].forEach(([n, txt]) => ok(txt.includes(n), `⑫ P4 缺「${n}」`));

// P5 · Agent 口径（**2,475 通生产口径**，与引擎 P16 的盲测口径是两个数据集）
[['96.5%', t5], ['通话未出现用户明确识别 AI 的信号', t5], ['2,475 · 100.0%', t5],
 ['2,180 · 88.1%', t5], ['1,170 · 47.3%', t5], ['86 · 3.5%', t5],
 ['仅 3.5%（86 通）被用户明显感知为 AI。', t5], ['2.05×', t5],
 ['AI ÷ 人 = 2.05 倍 · 日均营销转化率', t5],
 ['99.99% SLA', t5], ['SOC 2', t5], ['支持 GDPR 合规', t5],
 ['全球 SD-RTN 200+ 节点', t5], ['毫秒级分层记忆 RAG 端到端', t5],
 ['MCP + Function Call 开放栈', t5], ['900 亿分钟 RTE 月均支撑', t5]]
  .forEach(([n, txt]) => ok(txt.includes(n), `⑫ P5 缺「${n}」`));
ok(!ALL.includes('用户以为在跟真人说话'), '⑭ P5 旧措辞「用户以为在跟真人说话」回归');
ok(!ALL.includes('99.99% · SOC 2 / GDPR'), '⑭ P5 混合 chip 未拆开');

// P6 · Physical AI 口径
[['R1 · WI-FI · 2025.03.20 发布', t6], ['R1 · 4G · 2025.09.26 发布', t6],
 ['面向家居与室内场景——音箱、桌宠、陪伴机器人。', t6],
 ['走出 Wi-Fi 覆盖——户外、随身、车载与出海设备。', t6],
 ['全球率先发布的对话式 AI 硬件开发套件。', t6],
 ['活人感 = 角色立得住 + 临场撑得住。', t6], ['30000+', t6], ['200+', t6], ['毫秒级', t6]]
  .forEach(([n, txt]) => ok(txt.includes(n), `⑫ P6 缺「${n}」`));

// P7 · 案例：脚注去掉内部指针 + 案例墙 14 家逐字
ok(!ALL.includes('/convoai-visit P23'), '⑫ P7 脚注仍带内部指针 /convoai-visit P23');
ok(t7.includes('从 SD‑RTN 到设备，每一层都由声网托住 · 事实截止 2026.08'), '⑫ P7 脚注不符');
ok(t7.includes('L0 连接 · L1 感知 · L2 运行时——三层都有声网'), '⑫ P7 callout 不符');
[['L4', '入口与设备'], ['L3', '应用与结果'], ['L2', 'Agent 运行时'],
 ['L1', '模型与感知'], ['L0', '实时基础设施']].forEach(([c, n]) => {
  ok(t7.includes(c) && t7.includes(n), `⑫ P7 生态层缺「${c} ${n}」`);
});
CASES.forEach(n => ok(t7.includes(n), `⑮ P7 案例墙客户名缺 / 写错：「${n}」`));
ok(t7.includes('14') && t7.includes('声网联合案例 · 均已公开'), '⑮ P7 案例墙计数/题注不符');

// P8 · 合流：三不 + 三步 + 收尾 + OpenAI 句，逐字
[['三条支流，一条河', t8], ['Engine 的每一次打断', t8], ['Agent 的每一次交付', t8],
 ['Physical AI 的每一次唤醒', t8],
 ['都跑在同一张 SD-RTN 软件定义实时网络上——全球 200+ 节点，端到端毫秒级。', t8],
 ['不做 C 端 App', t8], ['不和你的产品竞争用户——你的用户永远是你的。', t8],
 ['不做自有硬件品牌', t8], ['R1 是开发套件，不是消费品——我们停在你需要的那一层。', t8],
 ['不训基座大模型', t8], ['多供应商开放，谁好用接谁——模型进步全部归你享受。', t8],
 ['STEP 1 · 今天', t8], ['注册即用', t8], ['免费额度，当天就能听到第一句回话', t8],
 ['STEP 2 · 两周', t8], ['PoC 共建', t8], ['工程团队陪跑，把你的第一个真实场景跑通', t8],
 ['STEP 3 · 一个季度', t8], ['规模化上线', t8],
 ['SLA、全球部署、多供应商兜底', t8], ['（典型节奏，视场景与合规而定）', t8],
 ['2024 OpenAI Realtime API 发布 · 声网为全球首批合作伙伴。', t8],
 ['DEMO / 文档 · agora.io › 对话式 AI · 联系团队', t8],
 ['让陪伴自然，让生意成单。', t8]].forEach(([n, txt]) => ok(txt.includes(n), `⑫ P8 缺「${n}」`));
ok(!ALL.includes('OpenAI 选择我们'), '⑭ P8「OpenAI 选择我们」未改');

// ⑭ 红线反向闸：价格 / staging / 引擎 P16 的盲测口径（两个数据集严禁混写）
['¥8,500', '¥2,999', '¥5,501', '8,500', '2,999', '5,501',
 'callagent-landingpage-staging', 'staging', '盲测', '32,000']
  .forEach(n => ok(!ALL.includes(n), `⑭ 红线：8 页宿主出现「${n}」`));

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 分步 P4/P5/P7 各 1 步 · 深链 P4→#1 / P5→#16 / P6→#19`);
await b.close();
process.exit(fails.length ? 1 : 0);
