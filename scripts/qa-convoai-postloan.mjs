// QA · convoai-postloan《AI 驱动的智能贷后催收解决方案》（15 页 · CONF 家族 · 双主题 · 零分步）
// 从 qa-convoai-eli5.mjs 改。家族共有的闸门（页数 / noindex / sig / 板 / 溢出 / 主题切换 /
// 键盘翻页 / console / deckSwap 常显）逐条继承；本 deck 独有的闸是它存在的理由：
//
//   ⑥ **表达红线反向闸**（这份 deck 最重要的一条）：
//      催债 / 施压催收 / 逼迫还款 / 强催 / 轰炸外呼 / 暴力催收 —— 六词全文 0 出现。
//      ⚠「强催」是**子串**红线：任何一次「加强催收管理」都会当场触闸，这是刻意的。
//      「回收率」不得与具体百分比同句（大纲风险提示：不承诺任何提升比例）。
//      客户名一个不进（含内部在谈的「光潽」）· Call Agent / 价格 / staging / 盲测 /
//      32,000 全不入（本 deck 定位是引擎基础设施 + 解决方案，不是产品页）· a[href] = 0。
//
//   ⑦ **事实在场闸 + 数字白名单反向闸**：行业侧每一个数都逐字来自大纲，
//      Agora 侧每一个数都逐字来自家族 canon。出现白名单以外的数字 = 有人新造了一个数。
//      白名单是**穷举**的（见 NUM_OK），改一个数就得同时改这里 —— 这正是它的用处。
//      同时钉死已仲裁的口径：大纲 P12「800 亿分钟 / 200+ 国家和地区」是英文官网旧口径，
//      不许回归（正确宾语是「200+ **全球节点**」）。
//
//   ⑧ **SOURCE ledger 闸**：五张数据页（P3/P4/P7/P9/P12）各恰好一行，
//      严格四段制 `SOURCE · 来源 · 样本或时间窗 · 事实截止 2026.08`，来源只写机构名不写 URL。
//
//   ⑬ **语言切换钮闸**（2026-08-30）：<button>（不是 <a>）· 常显 · 指向东南亚英文版 ·
//      print 隐藏 · 不挂 data-step · 与主题钮同角不重叠。互跳 round-trip 实测在
//      qa-convoai-postloan-en.mjs 的 ⑮ 段（两头都走，跑一次就够）。
//
//   ⑨ **P8 质量语言闸**：每页至多一枚 .mo-breathe（唯一 hot 件）；
//      带 SVG 图的页必须有图例（.fig 里至少一组图例线样）；零分步（页内 0 枚 [data-step]）。
//
// 用法：node scripts/qa-convoai-postloan.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8777 node scripts/qa-convoai-postloan.mjs
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const N = 15;
const BOARD = { 1: 'title', 15: 'title' };          // 其余一律 content
const SRC_PAGES = new Set([3, 4, 7, 9, 12]);        // SOURCE ledger 只在这五张数据页
// 六词红线（大纲第 6 节「不推荐表达」逐字）——「强催」是子串闸，会命中「加强催收」
const BANNED = ['催债', '施压催收', '逼迫还款', '强催', '轰炸外呼', '暴力催收'];
// 产品 / 商务红线（名单从 qa-convoai-engine.mjs 与 qa-convoai-eli5.mjs 拷来 + 本轮点名）
const REDLINE = ['Call Agent', '¥8,500', '¥2,999', '¥5,501', '8,500', '2,999', '5,501',
  'staging', '盲测', '32,000'];
// 客户名单：qa-convoai-info.mjs 的 CASES 逐字同源 + 「光潽」（内部在谈客户，本轮点名）
const CASES = ['光潽', '集贤科技', 'Robopoet', 'luwu', 'Pophie', '商汤', 'MiniMax',
  '智谱清言', '星野', '灵机一动', 'LOOKTECH', 'HeyCyan', 'LOOKEE', '莲偶科技', '豆神 AI'];
// 已仲裁：大纲 P12 的英文官网旧口径不许回归
const STALE = ['800 亿分钟', '800亿分钟', '200+ 国家', '200+国家'];
// 事实在场闸：[页, [必须出现的串…]]
const FACTS = [
  [3, ['3.7', '1.51', '239.2', '2026Q1 末', '国家金融监督管理总局']],
  [4, ['6.87', '6.96', '2025 年末', '2026Q1 末', '中国人民银行清算总中心']],
  [7, ['不得暴力、威胁、恐吓', '不得骚扰', '不得向无关第三人催收',
       '至少保存 5 年', 'GB/T 45251-2025', '2025.02.28']],
  [9, ['59.8', '137.7', 'CAGR 9.72%', '49', '93',
       'Fortune Business Insights', 'Grand View Research']],
  [12, ['650ms', '340ms', '95%', '900亿+', '200+', 'SAL 选择性注意力锁定',
        'AI-VAD', '优雅打断', 'AI QoS', '全球首批合作伙伴']],
  [14, ['不建议在没有客户试点数据前承诺固定提升比例',
        '通过试点验证接通、履约、成本和合规指标']],
  [15, ['规模化、标准化和实时分析', '复杂判断、情绪安抚和例外处理', '实时语音基础设施']],
];
// 数字白名单（穷举）。分三档，改一个数就得同时改这里 —— 这是闸门的用处，不是负担。
//   · 行业侧事实（大纲逐字）：3.7 / 1.51 / 239.2 / 6.87 / 6.96 / 45251 / 5 /
//     59.8 / 137.7 / 9.72 / 49 / 93
//   · Agora 侧 canon（引擎 deck 逐字）：650 / 340 / 95 / 900 / 200
//   · 年份 · 时点 · 序号 · 章节号：2023–2034 / 02 / 28 / 03 / 08 / 4 / 8 / 0 / 1 …
// ⚠ 2026-08-30 收紧：**路线条页号（P3–4 / P10–11 / P12–14）不再进白名单** ——
//   它们在 builder 里挂了 data-nogate="pageref"，扫描时整枝跳过。原先为了让页号过闸
//   把 10 / 11 / 12 / 13 / 14 / 15 全收了进来，等于给闸门钝化：收进去之后任何一个
//   新写的小数字都能蒙混过关，「禁止新造数字」这条闸就只剩个名字。
const NUM_OK = new Set([
  '3', '7', '1', '51', '239', '2', '6', '87', '96', '45251', '5',
  '59', '8', '137', '9', '72', '49', '93',
  '650', '340', '95', '900', '200',
  '2023', '2024', '2025', '2026', '2030', '2034', '0', '01', '02', '03', '04', '05',
  '06', '07', '08', '28', '4',
]);
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const errs = [];
pg.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
pg.on('console', m => {
  if (m.type() !== 'error') return;
  if ((m.location()?.url || '').includes('favicon')) return;
  errs.push(m.text());
});
if (THEME === 'dark') await pg.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
await pg.goto(BASE + '/decks/convoai-postloan.html#1', { waitUntil: 'load' });
// 动效归零：入场是 transition（.rise/.spread 起手有位移），不掐掉会把「还没落位」
// 读成「内容冲出 .sh 盒」的假溢出（occlusion-scan.mjs 同一手法）
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(900);

// ① 页数 + noindex + sig + 主题态 + title + a[href]
const meta = await pg.evaluate(() => ({
  n: document.querySelectorAll('.slide').length,
  secs: document.querySelectorAll('section').length,
  noindex: !!document.querySelector('meta[name="robots"][content*="noindex"]'),
  sigs: [...document.querySelectorAll('.slide .sig')].map(s => s.textContent),
  theme: document.documentElement.getAttribute('data-theme'),
  title: document.title,
  links: document.querySelectorAll('.deck-stage a[href]').length,
}));
ok(meta.n === N, `① 页数 ${meta.n} != ${N}`);
ok(meta.secs === N, `① section 数 ${meta.secs} != ${N}`);
ok(meta.noindex, '① 缺 noindex');
ok(meta.sigs.length === N && meta.sigs.every((s, i) => s === `${i + 1}/${N}`), `① 页码 sig 不齐（应为 N/${N}）`);
ok(THEME === 'dark' ? meta.theme === 'dark' : meta.theme !== 'dark', `① 主题态异常 ${meta.theme}`);
ok(meta.title === 'AI 驱动的智能贷后催收解决方案', `① title 漂移「${meta.title}」`);
ok(meta.links === 0, `⑥ a[href] 应为 0，实测 ${meta.links} —— 指路必须是纯文本`);

// ② 零分步：data-steps 全 0，页内一枚 [data-step] 都不许有
//    （常显容器挂 data-step 会被 motion.css 的兜底规则摁成透明整页 —— 引擎 deck P19 踩过）
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => ({
  d: +s.dataset.steps, n: s.querySelectorAll('[data-step]').length,
})));
steps.forEach((v, i) => {
  ok(v.d === 0, `② P${i + 1} data-steps ${v.d} != 0`);
  ok(v.n === 0, `② P${i + 1} 页内有 ${v.n} 枚 [data-step]（本 deck 应为 0）`);
});

// ③④⑤⑨ 逐页：板 / 图加载 / 溢出 / 出处行 / hot 件唯一 / 图必带图例
for (let i = 1; i <= N; i++) {
  const r = await pg.evaluate((n) => {
    document.querySelectorAll('.slide').forEach((el, k) => {
      el.classList.toggle('active', k === n - 1); el.classList.toggle('visible', k === n - 1);
    });
    const s = document.querySelectorAll('.slide')[n - 1];
    const bgs = [...s.querySelectorAll('.conf-bg')];
    const bgCls = bgs.length === 1 ? [...bgs[0].classList].find(c => c.startsWith('conf-bg-')) : null;
    const bgUrl = bgs.length === 1 ? getComputedStyle(bgs[0]).backgroundImage : '';
    const badImgs = [...s.querySelectorAll('.pp img')].filter(im => !im.complete || im.naturalWidth === 0).map(im => im.src);
    // 溢出：sh 内容不出画布 + 卡内容不冲出卡底（TEXT-x-SPILL 的源头）
    const out = [];
    s.querySelectorAll('.pp .sh').forEach(el => {
      [...el.children].forEach(ch => {
        const c = ch.getBoundingClientRect();
        if (c.bottom > 1080 - 6 || c.right > 1920 + 6 || c.left < -6) out.push('canvas:' + (el.className || '').slice(0, 46));
      });
    });
    s.querySelectorAll('.card,.card-c,.duo>div,.adv>div').forEach(el => {
      const r0 = el.getBoundingClientRect();
      el.querySelectorAll('*').forEach(ch => {
        if (ch.getBoundingClientRect().bottom > r0.bottom + 6) out.push('cardspill:' + (el.className || '').slice(0, 30));
      });
    });
    return {
      bgN: bgs.length, bgCls, bgUrl, badImgs, out,
      srcs: s.querySelectorAll('.src').length,
      kk: !!s.querySelector('.kk'), hh: !!s.querySelector('.hh') || !!s.querySelector('.ink'),
      breathe: s.querySelectorAll('.mo-breathe').length,
      figs: s.querySelectorAll('.fig svg').length,
      // 图例样线：legend() 画的是真线样（.dw / .pop），标签走 text.sm —— 这里只数图的存在
      lands: s.querySelectorAll('.land').length,
    };
  }, i);
  ok(r.bgN === 1, `④ P${i} conf-bg 数 ${r.bgN}`);
  const expB = BOARD[i] || 'content';
  ok(r.bgCls === 'conf-bg-' + expB, `④ P${i} 板 ${r.bgCls} != ${expB}`);
  ok(r.bgUrl.includes(THEME === 'dark' ? '-dark.png' : '-light.png'), `④ P${i} 板主题源不符 ${r.bgUrl}`);
  ok(r.badImgs.length === 0, `④ P${i} 图未加载 ${r.badImgs.join()}`);
  [...new Set(r.out)].forEach(o => fails.push(`⑤ P${i} 溢出 ${o}`));
  ok(r.kk, `③ P${i} 缺 kicker`);
  ok(r.hh, `③ P${i} 缺主标题`);
  ok(r.srcs === (SRC_PAGES.has(i) ? 1 : 0), `⑧ P${i} .src 出处行 ${r.srcs}（名单 ${SRC_PAGES.has(i) ? 1 : 0}）`);
  // ⑨ 每页至多一枚 hot 件（P8 质量语言第 ② 条）
  ok(r.breathe <= 1, `⑨ P${i} 有 ${r.breathe} 枚 .mo-breathe —— 每页至多一枚 hot 件`);
  // 每张内容页都要有落点句（title 板两页除外）
  if (!BOARD[i]) ok(r.lands === 1, `③ P${i} .land 落点句 ${r.lands} 条（内容页应为 1）`);
  await pg.waitForTimeout(30);
}

const pageText = async (p) => pg.evaluate((k) =>
  document.querySelector(`.slide[data-p="${k}"]`).textContent.replace(/\s+/g, ' '), p);
const all = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));

// ⑥ 表达红线反向闸（这份 deck 最重要的一条）
BANNED.forEach(w => ok(!all.includes(w),
  `⑥ 表达红线：全 deck 不许出现「${w}」（大纲第 6 节不推荐表达；「强催」是子串闸，会命中「加强催收」）`));
REDLINE.forEach(w => ok(!all.includes(w), `⑥ 红线：全 deck 不许出现「${w}」`));
CASES.forEach(c => ok(!all.includes(c), `⑥ 红线：方案 deck 不上客户名，「${c}」不许入页`));
STALE.forEach(w => ok(!all.includes(w),
  `⑥ 口径红线：英文官网旧口径「${w}」已仲裁不用（正确宾语是「200+ 全球节点 · SD-RTN」）`));
// 「回收率」不得与具体百分比同句
all.split(/[。；！？]/).forEach(sent => {
  if (sent.includes('回收率')) {
    ok(!/\d+(\.\d+)?%/.test(sent),
       `⑥ 红线：「回收率」与具体百分比同句 —— 本 deck 不承诺提升比例：「${sent.trim().slice(0, 50)}」`);
  }
});
// ⑥ **百分数白名单**（比「回收率同句」更锋利的一刀）：整份 deck 只准出现三个百分数 ——
//    1.51%（不良贷款率 · 金监总局）/ 9.72%（CAGR · Fortune BI）/ 95%（环境干扰屏蔽 · 家族 canon）。
//    任何第四个百分数都意味着有人写了一句「提升 X%」，那正是大纲风险提示里点名禁止的事。
const PCT_OK = new Set(['1.51%', '9.72%', '95%']);
const pcts = [...new Set((all.match(/\d+(?:\.\d+)?%/g) || []))].filter(p => !PCT_OK.has(p));
ok(pcts.length === 0,
   `⑥ 红线：出现未登记的百分数 ${pcts.join(' / ')} —— 本 deck 不承诺任何提升比例`);

// ⑦ 事实在场闸
for (const [p, kws] of FACTS) {
  const t = await pageText(p);
  for (const kw of kws) ok(t.includes(kw), `⑦ P${p} 缺在场事实「${kw}」`);
}
// ⑦ 反向：新造数字闸。摘掉页码 sig 与 P2 路线条的页号（都是**本 deck 自己的页码**，
//    不是内容里的数字）—— 不摘的话白名单得把 10–15 全收进去，闸门当场钝化。
const numText = await pg.evaluate(() => {
  const st = document.getElementById('deckStage');
  const skip = new Set([...st.querySelectorAll('.sig,[data-nogate="pageref"]')]);
  const w = document.createTreeWalker(st, NodeFilter.SHOW_TEXT);
  let s = '';
  for (let t = w.nextNode(); t; t = w.nextNode()) {
    let p = t.parentElement, bad = false;
    while (p && p !== st) { if (skip.has(p)) { bad = true; break; } p = p.parentElement; }
    if (!bad) s += t.textContent + ' ';
  }
  return s.replace(/\s+/g, ' ');
});
const nums = [...new Set((numText.match(/\d+/g) || []))].filter(x => !NUM_OK.has(x));
ok(nums.length === 0, `⑦ 出现未登记的数字（禁止新造数字 / 外推）：${nums.join(' / ')}`);

// ⑧ SOURCE ledger 四段制
const srcRows = await pg.evaluate(() =>
  [...document.querySelectorAll('.deck-stage .src')].map(e => e.textContent.replace(/\s+/g, ' ').trim()));
ok(srcRows.length === 5, `⑧ SOURCE ledger 行数 ${srcRows.length} != 5`);
srcRows.forEach(s => {
  ok(s.startsWith('SOURCE · '), `⑧ SOURCE 行不以「SOURCE · 」起手：「${s.slice(0, 40)}」`);
  ok(s.endsWith('· 事实截止 2026.08'), `⑧ SOURCE 行未以事实截止收尾：「${s.slice(-30)}」`);
  ok((s.match(/ · /g) || []).length === 3, `⑧ SOURCE 行不是四段制：「${s.slice(0, 60)}」`);
  ok(!/https?:/.test(s), `⑧ SOURCE 行写了 URL —— 家族格式只写机构名：「${s.slice(0, 40)}」`);
});

// ⑩ 每页动效名册交给 qa-motion.mjs；这里只验「图页不为零」
const mo = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(
  s => s.querySelectorAll('.mo-packet,.mo-drift,.mo-cycle,.mo-pulse,.mo-breathe,.mo-halo').length));
[2, 3, 4, 5, 6, 9, 11, 12, 13].forEach(p =>
  ok(mo[p - 1] > 0, `⑩ P${p} 在运动件名册上却没有任何常驻动效件`));
// P5 是标杆动效页、P11 是第二动效重点：件数低于下限就说明编排被改瘦了
ok(mo[4] >= 14, `⑩ P5（八环闭环 · 标杆动效页）运动件只剩 ${mo[4]} 个（下限 14）`);
ok(mo[10] >= 11, `⑩ P11（能力闭环 · 第二重点）运动件只剩 ${mo[10]} 个（下限 11）`);

// ⑪ deckSwap 常显 chip + 真实切换（板源 / localStorage / 按钮文案一起验）
await pg.evaluate(() => {
  window.deck.i = 0;
  document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === 0));
});
const swapVis = await pg.evaluate(() => {
  const b = document.getElementById('deckSwap');
  if (!b) return null;
  const r = b.getBoundingClientRect();
  return { op: +getComputedStyle(b).opacity, pos: getComputedStyle(b).position,
           w: Math.round(r.width), h: Math.round(r.height) };
});
ok(swapVis && swapVis.pos === 'fixed', '⑪ deckSwap 缺失或非 fixed');
ok(swapVis && swapVis.op >= 0.5 && swapVis.op <= 0.75,
   `⑪ deckSwap 应为常显 chip（opacity .5–.75），实测 ${swapVis && swapVis.op}`);
ok(swapVis && swapVis.w > 0 && swapVis.h > 0, '⑪ deckSwap 尺寸为 0');
await pg.click('#deckSwap');
await pg.waitForTimeout(400);
const sw = await pg.evaluate(() => {
  const s = document.querySelectorAll('.slide')[0];
  return {
    theme: document.documentElement.getAttribute('data-theme'),
    bg: getComputedStyle(s.querySelector('.conf-bg')).backgroundImage,
    ls: (() => { try { return localStorage.getItem('colin-theme'); } catch (e) { return null; } })(),
    label: document.getElementById('deckSwap').textContent,
  };
});
const flipped = THEME === 'dark' ? 'light' : 'dark';
ok(THEME === 'dark' ? sw.theme !== 'dark' : sw.theme === 'dark', `⑪ 切换后主题态 ${sw.theme}`);
ok(sw.bg.includes('-' + flipped + '.png'), '⑪ 切换后板源未换');
ok(sw.ls === flipped, `⑪ localStorage("colin-theme") 未写入 ${flipped}（实得 ${sw.ls}）`);
ok(sw.label === (flipped === 'dark' ? '浅底' : '暗底'), `⑪ 按钮文案 ${sw.label}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

// ⑬ 语言切换钮（2026-08-30 同链路语言切换）：<button>（不是 <a> —— 本 deck 的
//    a[href]=0 闸还在）· 常显 · 指向东南亚英文版 · print 隐藏 · 不挂 data-step ·
//    与主题钮同角不重叠。**互跳 round-trip 的实测在 qa-convoai-postloan-en.mjs ⑮ 里**
//    （那一段两头都走，放在英文版那边跑一次就够，不必两份 QA 各跳一遍）。
const lang = await pg.evaluate(() => {
  const el = document.getElementById('deckLang');
  const sw = document.getElementById('deckSwap');
  if (!el || !sw) return null;
  const r = el.getBoundingClientRect(), s = sw.getBoundingClientRect();
  const overlap = !(r.right < s.left || r.left > s.right || r.bottom < s.top || r.top > s.bottom);
  return { tag: el.tagName, txt: el.textContent.trim(), op: +getComputedStyle(el).opacity,
           pos: getComputedStyle(el).position, w: Math.round(r.width), h: Math.round(r.height),
           step: el.hasAttribute('data-step'), overlap, inStage: !!el.closest('.deck-stage'),
           gap: Math.round(s.top - r.bottom) };
});
ok(lang, '⑬ 缺语言切换钮 #deckLang');
if (lang) {
  ok(lang.tag === 'BUTTON', `⑬ 语言钮必须是 <button>（a[href]=0 闸），实测 <${lang.tag}>`);
  ok(lang.txt === 'EN', `⑬ 语言钮文案应为「EN」，实测「${lang.txt}」`);
  ok(lang.pos === 'fixed', `⑬ 语言钮非 fixed（${lang.pos}）`);
  ok(lang.op >= 0.5 && lang.op <= 0.75, `⑬ 语言钮应为常显 pill（opacity .5–.75），实测 ${lang.op}`);
  ok(lang.w > 0 && lang.h > 0, '⑬ 语言钮尺寸为 0');
  ok(!lang.step, '⑬ 语言钮挂了 data-step —— 本 deck 零分步');
  ok(!lang.inStage, '⑬ 语言钮跑进舞台里了（它是 chrome，不是页内容）');
  ok(!lang.overlap, '⑬ 语言钮与主题钮重叠 —— 同角摆位必须互不打架');
  ok(lang.gap >= 4 && lang.gap <= 24, `⑬ 语言钮与主题钮间距 ${lang.gap}px（应在 4–24 之间）`);
}
await pg.emulateMedia({ media: 'print' });
const printHidden = await pg.evaluate(() => ({
  lang: getComputedStyle(document.getElementById('deckLang')).display,
  swap: getComputedStyle(document.getElementById('deckSwap')).display,
}));
ok(printHidden.lang === 'none', `⑬ print 下语言钮未隐藏（${printHidden.lang}）`);
ok(printHidden.swap === 'none', `⑬ print 下主题钮未隐藏（${printHidden.swap}）`);
await pg.emulateMedia({ media: 'screen' });
const langJs = await pg.evaluate(() =>
  [...document.querySelectorAll('script')].map(s => s.textContent).join('\n'));
ok(/deckLang[\s\S]{0,400}convoai-postloan-en\.html/.test(langJs)
   && /deckLang[\s\S]{0,400}"\/convoai-postloan-en"/.test(langJs),
   '⑬ 语言钮的跳转目标不是英文版（应同时覆盖 /decks/*.html 预览与 /convoai-postloan-en 线上两条路径）');

// ⑫ 键盘翻页（共享 deck.js 运行时接上了）
await pg.evaluate(() => { document.activeElement?.blur(); location.hash = '#1'; });
await pg.waitForTimeout(500);
await pg.keyboard.press('ArrowRight');
await pg.waitForTimeout(350);
const cur = await pg.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
ok(cur === '2', `⑫ 方向键翻页失灵，当前 P${cur}`);

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
  : `✓ PASS ${THEME} · ${N} 页全绿 · 六词红线全清 · 客户名 0 · a[href]=0 · `
    + `数字白名单闸通过 · SOURCE ledger 5 行四段制 · hot 件每页 ≤1 · deckSwap 常显 · 语言钮就位`);
await b.close();
process.exit(fails.length ? 1 : 0);
