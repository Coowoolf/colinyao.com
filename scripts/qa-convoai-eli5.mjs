// QA · convoai-eli5《讲给五岁的你》（11 页 · CONF 家族 · 双主题 · 全 deck 零分步）
// 从 qa-convoai-engine.mjs 改。家族共有的闸门（页数 / noindex / sig / 板 / 溢出 /
// 主题切换 / 键盘翻页 / console）逐条继承；本 deck 独有的三组闸是它存在的理由：
//
//   ⑥ **ELI5 字数闸**：每页可见正文（.kk 眉标 / .hh 标题 / .sig 页码 / .src 出处行
//      之外的一切，**含图内标签**）≤ 40 个汉字。这一条逼着图自己把话说完 ——
//      少一条闸，ELI5 半年内就会退化成一份小字号产品手册。
//   ⑦ **大图闸**：每页那只 .eli-fig 的面积 ≥ 舞台（1920×1080）的 60%。
//      十一页统一 1680×744 = 60.28%，余量只有 0.28 个百分点 ——
//      任何一次「把图缩一点、给字腾地方」都会当场触闸。
//   ⑧ **canon 原数在场闸**：人话大字与原数小标必须**同页**出现，一对都不许拆：
//      P4 不到半秒 / 340ms · P5 九成半 / 95% · P6 不到一秒 / 650ms ·
//      P10 两百多个驿站 / 200+。人话翻译永远不许顶替事实。
//      配套的反向闸扫「新造数字」：整份 deck 的阿拉伯数字白名单只有
//      650 / 340 / 95 / 200 / 11（页数）/ 1（尺子的 1 秒）/ 2026.08（事实截止）。
//
//   ⑨ 红线反向闸（名单从 qa-convoai-engine.mjs 与 qa-convoai-info.mjs 拷来）：
//      价格 / staging / 盲测 / 32,000 一律不入；**客户名一个不进**（科普 deck 不上案例）；
//      **Call Agent 不进**（本 deck 只讲引擎故事）；**a[href] = 0**（指路走纯文本）。
//
// 用法：node scripts/qa-convoai-eli5.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8777 node scripts/qa-convoai-eli5.mjs
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const N = 11;
const BOARD = { 1: 'title', 11: 'title' };        // 其余一律 content
const CJK_MAX = 40;                                // ELI5 字数闸
const FIG_MIN = 0.60;                              // 大图闸（占 1920×1080 的比例）
// 出处行只该出现在这几页：四张 canon 页 + R1 实拍页 + 末页的指路行
const SRC_PAGES = new Set([4, 5, 6, 9, 10, 11]);
// 客户名单：与 qa-convoai-info.mjs 的 CASES 逐字同源（那份改名，这份要跟着改）
const CASES = ['集贤科技', 'Robopoet', 'luwu',
  'Pophie', '商汤', 'MiniMax', '智谱清言', '星野', '灵机一动',
  'LOOKTECH', 'HeyCyan', 'LOOKEE', '莲偶科技', '豆神 AI'];
// canon 对表：[页, 人话大字, 原数]
const CANON = [[4, '不到半秒', '340ms'], [5, '九成半', '95%'],
               [6, '不到一秒', '650ms'], [10, '两百多个驿站', '200+']];
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
await pg.goto(BASE + '/decks/convoai-eli5.html#1', { waitUntil: 'load' });
// 动效归零：入场是 transition（.rise/.spread 起手有位移），不掐掉会把「还没落位」
// 读成「内容冲出 .sh 盒」的假溢出（occlusion-scan.mjs 同一手法）
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.waitForTimeout(900);

// ① 页数 + noindex + sig + 主题态 + title
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
ok(meta.title === '声网 · 对话式 AI · 讲给五岁的你', `① title 漂移「${meta.title}」`);
ok(meta.links === 0, `⑨ a[href] 应为 0，实测 ${meta.links} —— 指路必须是纯文本`);

// ② 全 deck 零分步：data-steps 全 0，页内一枚 [data-step] 都不许有
//    （常显容器挂 data-step 会被 motion.css 的兜底规则摁成透明 = 空白页，
//     引擎 deck 的 P19 已经踩过一次）
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => ({
  d: +s.dataset.steps, n: s.querySelectorAll('[data-step]').length,
})));
steps.forEach((v, i) => {
  ok(v.d === 0, `② P${i + 1} data-steps ${v.d} != 0`);
  ok(v.n === 0, `② P${i + 1} 页内有 ${v.n} 枚 [data-step]（本 deck 应为 0）`);
});

// ③④⑤⑥⑦ 逐页：板 / 图加载 / 溢出 / 字数闸 / 大图闸 / 小注与出处行
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
    // 溢出：sh 内容不出画布
    const out = [];
    s.querySelectorAll('.pp .sh').forEach(el => {
      [...el.children].forEach(ch => {
        const c = ch.getBoundingClientRect();
        if (c.bottom > 1080 - 6 || c.right > 1920 + 6 || c.left < -6) out.push('canvas:' + (el.className || '').slice(0, 40));
      });
      // 卡内溢出：.eli-card 的内容不许冲出卡底（TEXT-x-SPILL 的源头）
      if (el.classList.contains('eli-card')) {
        const r0 = el.getBoundingClientRect();
        el.querySelectorAll('*').forEach(ch => {
          if (ch.getBoundingClientRect().bottom > r0.bottom + 6) out.push('cardspill:eli-card');
        });
      }
    });
    // ELI5 字数闸：数可见正文的汉字，排除 .kk / .hh / .sig / .src 子树
    const skip = new Set(); s.querySelectorAll('.kk,.hh,.sig,.src').forEach(e => skip.add(e));
    const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    let body = '';
    for (let t = w.nextNode(); t; t = w.nextNode()) {
      let p = t.parentElement, bad = false;
      while (p && p !== s) { if (skip.has(p)) { bad = true; break; } p = p.parentElement; }
      if (!bad) body += t.textContent;
    }
    const figs = [...s.querySelectorAll('.eli-fig')];
    const fr = figs.length === 1 ? figs[0].getBoundingClientRect() : null;
    return {
      bgN: bgs.length, bgCls, bgUrl, badImgs, out,
      cjk: (body.match(/[一-鿿]/g) || []).length,
      body: body.replace(/\s+/g, ' ').trim(),
      figN: figs.length, figPct: fr ? fr.width * fr.height / (1920 * 1080) : 0,
      notes: s.querySelectorAll('.note').length,
      srcs: s.querySelectorAll('.src').length,
      kk: !!s.querySelector('.kk'), hh: !!s.querySelector('.hh'),
      text: s.textContent.replace(/\s+/g, ' '),
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
  // ⑥ ELI5 字数闸
  ok(r.cjk <= CJK_MAX,
     `⑥ P${i} 正文 ${r.cjk} 个汉字 > ${CJK_MAX}（ELI5 纪律：大图、少字）「${r.body.slice(0, 60)}」`);
  // ⑦ 大图闸
  ok(r.figN === 1, `⑦ P${i} .eli-fig 应恰好一只，实测 ${r.figN}`);
  ok(r.figPct >= FIG_MIN,
     `⑦ P${i} 大图只占版面 ${(r.figPct * 100).toFixed(2)}% < ${FIG_MIN * 100}%`);
  // 至多一行小注 + 出处行只在名单页
  ok(r.notes <= 1, `③ P${i} 小注 ${r.notes} 行（ELI5 至多一行）`);
  ok(i === 1 ? r.notes === 0 : r.notes === 1, `③ P${i} 小注行数不符（封面 0，其余各 1）`);
  ok(r.srcs === (SRC_PAGES.has(i) ? 1 : 0), `③ P${i} .src 出处行 ${r.srcs}（名单 ${SRC_PAGES.has(i) ? 1 : 0}）`);
  await pg.waitForTimeout(40);
}

const pageText = async (p) => pg.evaluate((k) =>
  document.querySelector(`.slide[data-p="${k}"]`).textContent.replace(/\s+/g, ' '), p);
const all = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));
// 数字闸专用文本：把页码 sig（「3/11」）摘掉 —— 那是 chrome，不是内容里的数字
const numText = await pg.evaluate(() => {
  const st = document.getElementById('deckStage');
  const skip = new Set([...st.querySelectorAll('.sig')]);
  const w = document.createTreeWalker(st, NodeFilter.SHOW_TEXT);
  let s = '';
  for (let t = w.nextNode(); t; t = w.nextNode()) {
    let p = t.parentElement, bad = false;
    while (p && p !== st) { if (skip.has(p)) { bad = true; break; } p = p.parentElement; }
    if (!bad) s += t.textContent + ' ';
  }
  return s.replace(/\s+/g, ' ');
});

// ⑧ canon 原数在场闸：人话大字与原数小标必须同页，一对都不许拆
for (const [p, human, num] of CANON) {
  const t = await pageText(p);
  ok(t.includes(human), `⑧ P${p} 缺人话大字「${human}」`);
  ok(t.includes(num), `⑧ P${p} 缺原数小标「${num}」—— 人话翻译不许顶替事实`);
}
// ⑧ 反向：新造数字闸。整份 deck 出现的数字串必须落在白名单里
//    （650/340/95/200 是 canon；11 是页数；1 是尺子的「1 秒」；2026.08 是事实截止；
//     R1 / SD-RTN / ELI5 里的数字随词一起白名单）
const NUM_OK = new Set(['650', '340', '95', '200', '11', '1', '2026', '08', '5']);
const nums = [...new Set((numText.match(/\d+/g) || []))].filter(x => !NUM_OK.has(x));
ok(nums.length === 0, `⑧ 出现未登记的数字（禁止新造数字）：${nums.join(' / ')}`);

// ⑨ 红线反向闸
['¥8,500', '¥2,999', '¥5,501', '8,500', '2,999', '5,501',
 'staging', '盲测', '32,000', 'Call Agent', '外呼'].forEach(s =>
  ok(!all.includes(s), `⑨ 红线：全 deck 不许出现「${s}」`));
CASES.forEach(c => ok(!all.includes(c), `⑨ 红线：科普 deck 不上案例，客户名「${c}」不许入页`));
// 指路必须是纯文本（不挂链已在 ① 验过 a[href]=0，这里验它真的在末页）
ok((await pageText(11)).includes('colinyao.com/convoai'), '⑨ 末页缺「大人版」指路行');
ok((await pageText(11)).includes('对话即交互'),
   '⑨ 末页缺「对话即交互」—— 与深入讲解版封面同句，家族闭环靠这一句');
// AI QoS 的口径：别写成 FEC（那是另一套机制，本 deck 不讲）
ok(!/\bFEC\b/i.test(all), '⑨ P7 写成了 FEC —— Colin 的 canon 是 AI QoS（网好多带、断网续播）');

// ⑩ 每页都必须带常驻动效（名册细节交给 qa-motion.mjs，这里只验「不为零」）
const mo = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(
  s => s.querySelectorAll('.mo-packet,.mo-drift,.mo-cycle,.mo-pulse,.mo-breathe,.mo-halo').length));
mo.forEach((n, i) => ok(n > 0, `⑩ P${i + 1} 没有任何常驻动效件（本 deck 11 页全上册）`));

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

// ⑫ 键盘翻页（共享 deck.js 运行时接上了）
await pg.evaluate(() => { document.activeElement?.blur(); location.hash = '#1'; });
await pg.waitForTimeout(500);
await pg.keyboard.press('ArrowRight');
await pg.waitForTimeout(350);
const cur = await pg.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
ok(cur === '2', `⑫ 方向键翻页失灵，当前 P${cur}`);

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 字数闸 ≤${CJK_MAX} 汉字 · 大图闸 ≥${FIG_MIN * 100}% · canon 四对人话/原数同屏 · 红线全清 · a[href]=0 · deckSwap 常显`);
await b.close();
process.exit(fails.length ? 1 : 0);
