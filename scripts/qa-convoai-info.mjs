// QA · convoai-info 一页一章 Infograph 速讲版（8 页 · CONF 家族 · 双主题 · P4/P5/P7 各 1 步 build）
// 从 qa-convoai.mjs 改：N=8 / BOARD 只有 title+content / hero 只 P1 /
// ② 步进检查改为逐页比对 data-steps 与页内 [data-step] 最大值，⑦ 双源改查 hero-art 的 lt·dk 互斥。
// 视觉升级 R1（2026-08-13）加两条：
//   ⑨ P1 hero 盒 left+width ≤ 1920（原 860+1200=2060 把图右侧顶出画布，防回归）
//   ⑩ P7 .eco-art 双源可见性与主题（和 ⑤ 的 hero-art 断言同一写法）
// 引擎详解抽屉（2026-08-18）再加一条：
//   ⑪ P4 的 #engineExpand chip（step1 上）+ Enter 展开 / Esc 收回的 overlay + 引擎 deck 自身可达
//      （浅色跑全套；深色只跑 chip 可见 —— overlay 是主题无关层）
// 用法：node scripts/qa-convoai-info.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8899 node scripts/qa-convoai-info.mjs   （换端口）
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8777';
const N = 8;
// 2026-08-20：P4（03 SIGNATURE MOVES + 04 OPEN）/ P5（04 CAPABILITIES 12 项）/
// P7（右列案例墙）各加一步 presenter-controlled build，其余页仍为 0
const EXP_STEPS = [0, 0, 0, 1, 1, 0, 1, 0];
const BOARD = { 1: 'title' };            // 其余一律 content
const HERO = { 1: 'hero-cover-v2' };     // hero-art 只上封面
const ECO = { 7: 'ecosystem-stack-v4' }; // eco-art 只上 P7 生态主视觉（polish-v4 换稿）
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

// ② 分步数：逐页比对 data-steps 与页内 [data-step] 的最大值 —— 两边必须自洽，
//    声明了 N 步却没有第 N 步的元素（或反过来）都是现场翻不出来的哑火
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => +s.dataset.steps));
EXP_STEPS.forEach((e, i) => ok(steps[i] === e, `② P${i + 1} steps ${steps[i]} != ${e}`));
const stepMax = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map((s) => {
  const els = [...s.querySelectorAll('[data-step]')];
  return els.length ? Math.max(...els.map(e => +e.dataset.step || 0)) : 0;
}));
EXP_STEPS.forEach((e, i) => ok(stepMax[i] === e,
  `② P${i + 1} 页内 [data-step] 最大值 ${stepMax[i]} != data-steps ${e}`));

// ③④⑤⑥ 逐页：板、hero、图、溢出（画布溢出 + 卡内溢出）
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
    // 溢出：sh 内容不出画布；卡片内容不冲出卡底
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
    // ⑨ 出画布回归闸：两个源盒都要 left+width ≤ 1920 且 top+height ≤ 1080
    r.heroes.forEach((h) => {
      ok(Number.isFinite(h.box.l) && Number.isFinite(h.box.w), `⑨ P${i} hero 盒缺 left/width`);
      ok(h.box.l + h.box.w <= 1920, `⑨ P${i} hero 出画布 left+width=${h.box.l + h.box.w} > 1920`);
      ok(h.box.t + h.box.h <= 1080, `⑨ P${i} hero 出画布 top+height=${h.box.t + h.box.h} > 1080`);
    });
  } else {
    ok(r.heroes.length === 0, `⑤ P${i} 不应有 hero`);
  }
  // ⑩ P7 生态全景双源（写法照 ⑤ 的 hero-art：数 2 · 可见 1 · 主题类对 · 真加载）
  if (ECO[i]) {
    ok(r.ecos.length === 2, `⑩ P${i} eco-art 数 ${r.ecos.length}`);
    const ev = r.ecos.filter(e => e.vis);
    ok(ev.length === 1, `⑩ P${i} eco-art 可见数 ${ev.length}`);
    if (ev[0]) {
      ok(ev[0].cls.includes(THEME === 'dark' ? 'dk' : 'lt'), `⑩ P${i} eco-art 主题错 ${ev[0].cls}`);
      ok(ev[0].src.includes(`${ECO[i]}-${THEME}.webp`), `⑩ P${i} eco-art 源不符 ${ev[0].src}`);
      // polish-v4 后底图不再是 2048 宽的全景（v4 主视觉 1672×941）：断言退回「真加载」语义
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

// ⑦ 主题切换：deckSwap 按钮真实切换（板源 + hero-art 双源）
await pg.evaluate(() => {
  window.deck.i = 0;
  document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === 0));
});
await pg.click('#deckSwap');
await pg.waitForTimeout(400);
const sw = await pg.evaluate(() => {
  const s = document.querySelectorAll('.slide')[0];
  const p7 = document.querySelectorAll('.slide')[6];
  // 少一个源就返回 'MISSING'，让它落成一条 fail —— 别在 getComputedStyle(null) 上炸栈
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
// ⑩ eco-art 与 hero-art 同机制（纯 CSS 控可见性）：deckSwap 之后也必须跟着翻
ok(flipped === 'dark' ? (sw.elt === 'none' && sw.edk === 'block') : (sw.edk === 'none' && sw.elt === 'block'),
   `⑩ 切换后 eco 双源 ${sw.elt}/${sw.edk}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

// ⑪ 引擎详解抽屉：chip → Enter 展开 → Esc 收回 → deck 按键恢复 → 引擎 deck 自身可达
// 先把焦点从 #deckSwap 上摘掉（抽屉的全局 Enter 拦截会把 deckSwap 的 Enter 让回给按钮），
// 再用 hashchange 正经导航到 P4（deck.go 会把 .active 摆对）。
await pg.evaluate(() => { document.activeElement?.blur(); location.hash = '#4'; });
await pg.waitForTimeout(2400);       // 等整页入场走完：.slide 的 visibility 有 .52s 延迟，.rise --i:4 约 1.2s
// P4 现在有一步 build：04 · OPEN 那行 chips（含 #engineExpand）落在 step1，
// 先按一次方向键把这一步推上来，再量 chip 可见性 —— 讲者现场也是这个顺序。
await pg.keyboard.press('ArrowRight');
await pg.waitForTimeout(900);
const chip = await pg.evaluate(() => {
  const c = document.getElementById('engineExpand');
  if (!c) return null;
  const r = c.getBoundingClientRect(), cs = getComputedStyle(c);
  const p4 = document.querySelector('.slide[data-p="4"]');
  return {
    txt: c.textContent, w: r.width, h: r.height,
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
}
if (THEME !== 'dark') {                       // overlay 是主题无关层：全套只在浅色跑一遍
  await pg.keyboard.press('Enter');           // ② Enter 展开
  await pg.waitForTimeout(200);
  const opened = await pg.evaluate(() => document.getElementById('engineOverlay').hidden);
  ok(opened === false, '⑪ Enter 未展开 overlay');
  const secs = await pg.waitForFunction(() => {
    const f = document.getElementById('engineFrame');
    const d = f && f.contentDocument;
    return (d && d.readyState === 'complete' && d.querySelectorAll('section').length)
      ? d.querySelectorAll('section').length : false;
  }, null, { timeout: 8000 }).then(h => h.jsonValue()).catch(() => 0);
  ok(secs === 22, `⑪ iframe 内 section 数 ${secs} != 22`);
  const focused = await pg.evaluate(() => document.activeElement?.id);
  ok(focused === 'engineFrame', `⑪ 展开后焦点不在 iframe（${focused}）`);

  await pg.keyboard.press('Escape');          // ③ Esc 收回（焦点在 iframe 内）
  await pg.waitForTimeout(250);
  ok(await pg.evaluate(() => document.getElementById('engineOverlay').hidden) === true,
     '⑪ Esc 未收回 overlay');
  await pg.keyboard.press('ArrowRight');      // deck 按键必须回来：P4 → P5
  await pg.waitForTimeout(350);
  const after = await pg.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
  ok(after === '5', `⑪ Esc 后方向键失灵，当前 P${after}`);

  // ④ 引擎 deck 本体：200 + noindex + 22 页（2026-08-21 Call Agent 章 18 → 21 → 视频页 22）
  const res = await fetch(BASE + '/decks/convoai-engine.html');
  const html = await res.text();
  ok(res.status === 200, `⑪ convoai-engine.html HTTP ${res.status}`);
  ok(/noindex/.test(html), '⑪ convoai-engine.html 缺 noindex');
  const nSec = (html.match(/<section/g) || []).length;
  ok(nSec === 22, `⑪ convoai-engine.html section 数 ${nSec} != 22`);
}

// ⑫ 口径闸（2026-08-20 仲裁）：分类学统一 / 主数据措辞 / SOURCE 行 / 去内部指针 / CTA
const T = async (k) => pg.evaluate((n) =>
  document.querySelector(`.slide[data-p="${n}"]`).textContent.replace(/\s+/g, ' '), k);
const [t2, t3, t5, t7, t8] = await Promise.all([T(2), T(3), T(5), T(7), T(8)]);
const ALL = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));
// P3：底座 → 三条产品线 → Engine 两种交付形态
[['一个实时底座，三条产品线', t3], ['THREE PRODUCT LINES', t3], ['ENGINE DELIVERY FORMS', t3],
 ['两种交付形态', t3], ['配套能力 · 工具', t3], ['实时底座', t3]]
  .forEach(([n, txt]) => ok(txt.includes(n), `⑫ P3 缺「${n}」`));
['三台引擎', '两大产品引擎', 'THREE ENGINES', 'DUAL FORM'].forEach(n =>
  ok(!ALL.includes(n), `⑫ 旧分类学口径回归：「${n}」`));
// P2：Realtime API 首批口径 + SOURCE 行
ok(!ALL.includes('全球首个 Realtime API'), '⑫ P2「全球首个 Realtime API」未改成首批口径');
ok(t2.includes('全球首批 Realtime API'), '⑫ P2 缺「全球首批 Realtime API」');
ok(t2.includes('SOURCE · 声网官网 / IR · IDC 中国视频云市场报告 · 公司批准口径 · 事实截止 2026.08'),
   '⑫ P2 缺 SOURCE 行');
// P5：96.5% 措辞 + 安全 chip 拆分
ok(t5.includes('96.5%'), '⑫ P5 缺 96.5%');
ok(t5.includes('通话未出现用户明确识别 AI 的信号'), '⑫ P5 主数据措辞未改');
ok(!ALL.includes('用户以为在跟真人说话'), '⑫ P5 旧措辞「用户以为在跟真人说话」回归');
['99.99% SLA', 'SOC 2', '支持 GDPR 合规'].forEach(n =>
  ok(t5.includes(n), `⑫ P5 安全项缺「${n}」`));
ok(!ALL.includes('99.99% · SOC 2 / GDPR'), '⑫ P5 混合 chip 未拆开');
// P7：脚注去掉内部指针
ok(!ALL.includes('/convoai-visit P23'), '⑫ P7 脚注仍带内部指针 /convoai-visit P23');
ok(t7.includes('从 SD‑RTN 到设备，每一层都由声网托住 · 事实截止 2026.08'), '⑫ P7 脚注不符');
// P8：OpenAI 表述 + 季度限定 + CTA
ok(!ALL.includes('OpenAI 选择我们'), '⑫ P8「OpenAI 选择我们」未改');
ok(t8.includes('2024 OpenAI Realtime API 发布 · 声网为全球首批合作伙伴'), '⑫ P8 OpenAI 表述不符');
ok(t8.includes('典型节奏，视场景与合规而定'), '⑫ P8 缺「一个季度」的限定词');
ok(t8.includes('agora.io › 对话式 AI'), '⑫ P8 缺 CTA 入口文案');

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 分步 P4/P5/P7 各 1 步`);
await b.close();
process.exit(fails.length ? 1 : 0);
