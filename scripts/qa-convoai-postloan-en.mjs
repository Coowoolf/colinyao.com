// QA · convoai-postloan-en《AI-Powered Post-Loan Collections》SEA EDITION
//      （15 页 · CONF 家族 · 双主题 · 零分步 · 全英文）
// 从 qa-convoai-postloan.mjs 改。家族共有的闸门（页数 / noindex / sig / 板 / 溢出 /
// 主题切换 / 键盘翻页 / console / deckSwap 常显）逐条继承；英文版独有的四条闸是它存在的理由：
//
//   ⑥ **措辞红线反向闸**（大小写不敏感）：作为我方定位词，六串全文 0 出现 ——
//      debt chasing / chase debtors / pressure tactics / aggressive collection /
//      harass / intimidat。
//      `threaten` **只准出现一次**，且必须落在 P7 引述 SBV 禁令的那一枚 [data-nogate] 节点里
//      （命中数 = 1 且该节点自己包含它 —— 少一条都不算数：只数总数会放过「一次命中但
//      跑到别的页去了」，只查节点会放过「节点里有、别处又多写了一次」）。
//      承诺比例句零出现：整份 deck 只准两个百分数 —— 95%（canon）/ 9.72%（CAGR）。
//
//   ⑬ **CJK 纯度闸**（这份 deck 最独特的一条）：舞台 + 主题钮里一个 CJK 字符都不许有；
//      全页唯一合法的 CJK 是左下角语言钮上的「中文」二字（该节点豁免）。
//      一个漏译的中文词在越南现场就是一处硬伤，肉眼在 15 页里找不全，只能靠闸。
//
//   ⑭ **语言切换钮闸**：<button>（不是 <a> —— a[href]=0 闸还在）· 常显 ·
//      指向中文版 · print 隐藏 · 不挂 data-step · 与主题钮同角不重叠。
//
//   ⑮ **互跳 round-trip 实测**：点英文版的「中文」→ URL 变成中文版 → 中文版加载完成 →
//      点它的「EN」→ 回到英文版。这是「同链路语言切换」这件事唯一算数的证明。
//      ROUNDTRIP=1 只跑这一段并打印完整轨迹（交付物 lang-switch-roundtrip.txt 就是它）。
//
//   ⑦ **事实在场闸 + 数字白名单反向闸**：行业侧每个数都来自 Colin 核过的一手来源，
//      Agora 侧每个数都来自家族 canon。出现白名单以外的数字 = 有人新造了一个数。
//      白名单是**穷举**的（见 NUM_OK），改一个数就得同时改这里。
//
//   ⑯ **.hh 单行闸**（英文版专属版式账）：主标 60px 在 1680 盒里约放 62 个拉丁字符，
//      写到两行就会顶穿 y238 撞上 seclab。用 Range.getClientRects() 数行盒行数 = 1。
//      （不能用 scrollHeight —— .sh 的固定高 90px 比单行内容还高，它恒返回 90。）
//
// 用法：node scripts/qa-convoai-postloan-en.mjs          （THEME=dark 二跑）
//      ROUNDTRIP=1 node scripts/qa-convoai-postloan-en.mjs
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const CN_URL = '/decks/convoai-postloan.html';
const EN_URL = '/decks/convoai-postloan-en.html';
const N = 15;
const BOARD = { 1: 'title', 15: 'title' };          // 其余一律 content
const SRC_PAGES = new Set([3, 4, 7, 9, 12]);        // SOURCE ledger 只在这五张数据页
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
// CJK 区段：CJK 标点 / 扩展 A / 统一表意 / 全角形式
const CJK = /[　-〿㐀-䶿一-鿿＀-￯]/g;
// 措辞红线（作为我方定位词，一次都不许出现）
const BANNED = ['debt chasing', 'chase debtors', 'pressure tactics',
  'aggressive collection', 'harass', 'intimidat'];
// 产品 / 商务红线
const REDLINE = ['Call Agent', '¥8,500', '¥2,999', '¥5,501', '8,500', '2,999', '5,501',
  'staging', '32,000'];
// 客户名单：与 qa-convoai-postloan.mjs 逐字同源
const CASES = ['光潽', '集贤科技', 'Robopoet', 'luwu', 'Pophie', '商汤', 'MiniMax',
  '智谱清言', '星野', '灵机一动', 'LOOKTECH', 'HeyCyan', 'LOOKEE', '莲偶科技', '豆神 AI'];
// 已仲裁：英文官网旧口径不许回归；中国市占信任状不进英文版（对 SEA 听众无效且要解释成本）
const STALE = ['80 billion minutes', '200+ countries', 'IDC', 'No.1 in China'];
// 事实在场闸：[页, [必须出现的串…]]
const FACTS = [
  [3, ['e-Conomy SEA 2025', 'Google, Temasek', 'Digital lending', 'e-wallet']],
  [4, ['61/2020/QH14', '01.01.2021', 'prohibited business investment',
       'National Assembly of Vietnam', 'in-house']],
  [7, ['18/2019/TT-NHNN', '43/2016', 'Article 7', '01.01.2020',
       '5 reminders per day', '07:00', '21:00', 'No third-party contact',
       'Lawful measures only', 'OJK', 'BSP', 'BOT', 'MAS']],
  [9, ['5.98', '13.77', 'CAGR 9.72%', '4.9', '9.3',
       'Fortune Business Insights', 'Grand View Research']],
  [12, ['650ms', '340ms', '95%', '90B+', '200+', 'SAL', 'AI-VAD',
        'Graceful interruption', 'AI QoS', 'global first-batch partner',
        'no vendor lock-in']],
  [14, ['Do not commit to a fixed uplift', 'improvement headroom']],
  [15, ['scale, standardisation and real-time analysis',
        'complex judgement, empathy and exceptions', 'real-time voice infrastructure']],
];
// 数字白名单（穷举）。分四档，改一个数就得同时改这里 —— 这是闸门的用处，不是负担。
//   · 越南法条：61 / 2020 / 14（QH14）/ 01 / 2021（Law 61/2020/QH14，2021-01-01 施行）
//     18 / 2019 / 43 / 2016 / 2 / 7 / 01 / 2020（Circular 18/2019 修订 43/2016 Art.7）
//     5（≤5 次/日）· 07 / 00 / 21（07:00–21:00 时间窗）
//   · 市场：5 / 98（5.98）· 13 / 77（13.77）· 9 / 72（9.72）· 4 / 9（4.9）· 9 / 3（9.3）
//     2023 / 2025 / 2030 / 2034
//   · Agora canon：650 / 340 / 95 / 90 / 200 · 2024（OpenAI Realtime API）
//   · 序号 · 章节号 · 试点参数：01–08（节号 / 环号）/ 1–5（LAYER n / Stage n）/
//     4 / 8（4–8 weeks）/ 0 / 1（M0 / M1）
//   · 事实截止：2026 / 08
// ⚠ **路线条页号（P3–4 / P10–11 / P12–14）不在这张表里**：它们在 builder 里挂了
//   data-nogate="pageref"，扫描时整枝跳过。把 10–15 收进白名单等于给闸门钝化 ——
//   收进去之后任何一个新写的小数字都能蒙混过关（上一轮的短板，本轮修掉）。
const NUM_OK = new Set([
  '0', '1', '2', '3', '4', '5', '7', '8', '9',
  '00', '01', '02', '03', '04', '05', '06', '07', '08',
  '13', '14', '18', '21', '43', '61', '72', '77', '90', '95', '98', '200', '340', '650',
  '2016', '2019', '2020', '2021', '2023', '2024', '2025', '2026', '2030', '2034',
]);
const PCT_OK = new Set(['95%', '9.72%']);

const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
const b = await chromium.launch({ executablePath: CHROME });

// ═══ ⑮ 互跳 round-trip 实测 ═══════════════════════════════════════════════
//   点 EN 版的「中文」→ URL 变 → 中文版 15 页就位 → 点它的「EN」→ 回到 EN 版。
//   ⚠ 预览服务器是静态目录服务（没有 rewrites），所以两份 deck 的语言钮都按
//     pathname 是否带 .html 二选一 —— 这一段验的正是那条分支在预览环境下真的跑通。
async function roundTrip() {
  const trace = [];
  const say = (s) => { trace.push(s); if (process.env.ROUNDTRIP === '1') console.log(s); };
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } });
  const pg = await ctx.newPage();
  const rt = { ok: true };
  const step = async (from, btnId, btnText, expectPath, expectTitle) => {
    const before = new URL(pg.url()).pathname;
    say(`  · at ${before}`);
    const label = await pg.textContent('#' + btnId);
    const tag = await pg.evaluate((id) => document.getElementById(id).tagName, btnId);
    const links = await pg.evaluate(() => document.querySelectorAll('.deck-stage a[href]').length);
    say(`    button #${btnId} = <${tag.toLowerCase()}> «${label}» · stage a[href]=${links}`);
    if (tag !== 'BUTTON') { rt.ok = false; say(`    ✗ 语言钮不是 <button>（实测 <${tag.toLowerCase()}>）`); }
    if (label.trim() !== btnText) { rt.ok = false; say(`    ✗ 钮文案「${label.trim()}」!= 「${btnText}」`); }
    await Promise.all([pg.waitForNavigation({ waitUntil: 'load' }), pg.click('#' + btnId)]);
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(400);
    const after = new URL(pg.url()).pathname;
    const t = await pg.title();
    const n = await pg.evaluate(() => document.querySelectorAll('.slide').length);
    say(`    → ${after} · title «${t}» · slides=${n}`);
    if (after !== expectPath) { rt.ok = false; say(`    ✗ 落点 ${after} != ${expectPath}`); }
    if (!t.includes(expectTitle)) { rt.ok = false; say(`    ✗ title 不含「${expectTitle}」`); }
    if (n !== N) { rt.ok = false; say(`    ✗ 对方 deck 页数 ${n} != ${N}`); }
    return after;
  };
  say('LANG SWITCH ROUND-TRIP · ' + new Date().toISOString());
  say('base = ' + BASE);
  say('');
  say('[1] EN → CN');
  await pg.goto(BASE + EN_URL + '#1', { waitUntil: 'load' });
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(400);
  await step('en', 'deckLang', '中文', CN_URL, 'AI 驱动的智能贷后催收解决方案');
  say('');
  say('[2] CN → EN');
  await step('cn', 'deckLang', 'EN', EN_URL, 'AI-Powered Post-Loan Collections');
  say('');
  say(rt.ok ? '✓ ROUND-TRIP PASS · 同一条链路上来回切换，两版各自 15 页全量加载'
            : '✗ ROUND-TRIP FAIL');
  await ctx.close();
  return { ok: rt.ok, trace };
}

if (process.env.ROUNDTRIP === '1') {
  const r = await roundTrip();
  await b.close();
  process.exit(r.ok ? 0 : 1);
}

const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const errs = [];
pg.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
pg.on('console', m => {
  if (m.type() !== 'error') return;
  if ((m.location()?.url || '').includes('favicon')) return;
  errs.push(m.text());
});
if (THEME === 'dark') await pg.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
await pg.goto(BASE + EN_URL + '#1', { waitUntil: 'load' });
// 动效归零：入场是 transition（.rise/.spread 起手有位移），不掐掉会把「还没落位」
// 读成「内容冲出 .sh 盒」的假溢出（occlusion-scan.mjs 同一手法）
await pg.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;transition-duration:0s!important;transition-delay:0s!important;}' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(900);

// ① 页数 + noindex + sig + 主题态 + title + lang + a[href]
const meta = await pg.evaluate(() => ({
  n: document.querySelectorAll('.slide').length,
  secs: document.querySelectorAll('section').length,
  noindex: !!document.querySelector('meta[name="robots"][content*="noindex"]'),
  sigs: [...document.querySelectorAll('.slide .sig')].map(s => s.textContent),
  theme: document.documentElement.getAttribute('data-theme'),
  title: document.title,
  lang: document.documentElement.getAttribute('lang'),
  links: document.querySelectorAll('.deck-stage a[href]').length,
}));
ok(meta.n === N, `① 页数 ${meta.n} != ${N}`);
ok(meta.secs === N, `① section 数 ${meta.secs} != ${N}`);
ok(meta.noindex, '① 缺 noindex');
ok(meta.sigs.length === N && meta.sigs.every((s, i) => s === `${i + 1}/${N}`), `① 页码 sig 不齐（应为 N/${N}）`);
ok(THEME === 'dark' ? meta.theme === 'dark' : meta.theme !== 'dark', `① 主题态异常 ${meta.theme}`);
ok(meta.title === 'AI-Powered Post-Loan Collections & Overdue Asset Management',
   `① title 漂移「${meta.title}」`);
ok(meta.lang === 'en', `① <html lang> 应为 en，实测「${meta.lang}」`);
ok(meta.links === 0, `⑥ a[href] 应为 0，实测 ${meta.links} —— 指路必须是纯文本`);

// ② 零分步：data-steps 全 0，页内一枚 [data-step] 都不许有
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => ({
  d: +s.dataset.steps, n: s.querySelectorAll('[data-step]').length,
})));
steps.forEach((v, i) => {
  ok(v.d === 0, `② P${i + 1} data-steps ${v.d} != 0`);
  ok(v.n === 0, `② P${i + 1} 页内有 ${v.n} 枚 [data-step]（本 deck 应为 0）`);
});

// ③④⑤⑨⑯ 逐页：板 / 图加载 / 溢出 / 出处行 / hot 件唯一 / 落点句 / .hh 单行
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
    s.querySelectorAll('.card,.card-c,.duo>div,.adv>div,.spec>div').forEach(el => {
      const r0 = el.getBoundingClientRect();
      el.querySelectorAll('*').forEach(ch => {
        if (ch.getBoundingClientRect().bottom > r0.bottom + 6) out.push('cardspill:' + (el.className || '').slice(0, 30));
      });
    });
    // ⑯ .hh 单行闸。⚠ 不能用 scrollHeight：.sh 的固定高度（90px）比单行内容还高，
    //   scrollHeight 恒返回 90，闸门永远读不到「折了没有」。改用 Range 数**行盒行数**：
    //   selectNodeContents + getClientRects() 会按行返回矩形（<strong> 会把一行切成
    //   多个矩形），所以按 top 去重（容差 2px）才是真正的行数。
    const hh = s.querySelector('.hh');
    let hhLines = 0;
    if (hh) {
      const rg = document.createRange();
      rg.selectNodeContents(hh);
      const tops = [];
      [...rg.getClientRects()].forEach(r => {
        if (r.width < 1 && r.height < 1) return;
        if (!tops.some(t => Math.abs(t - r.top) < 2)) tops.push(r.top);
      });
      hhLines = tops.length;
    }
    return {
      bgN: bgs.length, bgCls, bgUrl, badImgs, out,
      srcs: s.querySelectorAll('.src').length,
      kk: !!s.querySelector('.kk'), hh: !!s.querySelector('.hh') || !!s.querySelector('.ink'),
      hhLines,
      hhTxt: hh ? hh.textContent.trim().slice(0, 40) : '',
      breathe: s.querySelectorAll('.mo-breathe').length,
      figs: s.querySelectorAll('.fig svg').length,
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
  ok(r.breathe <= 1, `⑨ P${i} 有 ${r.breathe} 枚 .mo-breathe —— 每页至多一枚 hot 件`);
  if (!BOARD[i]) {
    ok(r.lands === 1, `③ P${i} .land 落点句 ${r.lands} 条（内容页应为 1）`);
    ok(r.hhLines === 1,
       `⑯ P${i} 主标 ${r.hhLines} 行（英文主标一律单行）：「${r.hhTxt}」`);
  }
  await pg.waitForTimeout(30);
}

const pageText = async (p) => pg.evaluate((k) =>
  document.querySelector(`.slide[data-p="${k}"]`).textContent.replace(/\s+/g, ' '), p);
const all = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));
const allLow = all.toLowerCase();

// ⑥ 措辞红线反向闸（大小写不敏感）
BANNED.forEach(w => ok(!allLow.includes(w),
  `⑥ 措辞红线：全 deck 不许把「${w}」写成我方定位词`));
REDLINE.forEach(w => ok(!all.includes(w), `⑥ 红线：全 deck 不许出现「${w}」`));
CASES.forEach(c => ok(!all.includes(c), `⑥ 红线：方案 deck 不上客户名，「${c}」不许入页`));
STALE.forEach(w => ok(!all.includes(w),
  `⑥ 口径红线：「${w}」已仲裁不进英文版`));
// `threaten` 只准一次，且必须落在 P7 的 [data-nogate] 豁免节点里 ——
// 两头都要查：只数总数会放过「命中跑到别的页」，只查节点会放过「节点里有、别处又多写一次」。
const thrCount = (allLow.match(/threaten/g) || []).length;
ok(thrCount === 1,
   `⑥ 红线：threaten 出现 ${thrCount} 次 —— 只准 P7 引述 SBV 禁令那一处（该节点已挂 data-nogate）`);
const nogate = await pg.evaluate(() => {
  const els = [...document.querySelectorAll('.deck-stage [data-nogate="threaten"]')];
  return { n: els.length, hit: els.filter(e => /threaten/i.test(e.textContent)).length,
           page: els.map(e => e.closest('.slide')?.dataset.p) };
});
ok(nogate.n === 1 && nogate.hit === 1 && nogate.page[0] === '7',
   `⑥ [data-nogate] 豁免节点异常：数量 ${nogate.n} / 含 threaten ${nogate.hit} / 落在 P${nogate.page}`);
// 百分数白名单（比「不承诺提升比例」更锋利的一刀）
const pcts = [...new Set((all.match(/\d+(?:\.\d+)?%/g) || []))].filter(p => !PCT_OK.has(p));
ok(pcts.length === 0,
   `⑥ 红线：出现未登记的百分数 ${pcts.join(' / ')} —— 本 deck 不承诺任何提升比例`);
// 承诺句式（uplift / improve … %）零出现
ok(!/\b(uplift|improve[sd]?|increase[sd]?|boost)\b[^.]{0,40}\d+(?:\.\d+)?%/i.test(all),
   '⑥ 红线：出现「提升 X%」式承诺句');

// ⑬ CJK 纯度闸：舞台 + 主题钮零 CJK；唯一合法 CJK 是语言钮上的「中文」
const purity = await pg.evaluate(() => {
  const grab = (el) => (el ? el.textContent : '');
  return {
    stage: grab(document.getElementById('deckStage')),
    swap: grab(document.getElementById('deckSwap')),
    lang: grab(document.getElementById('deckLang')),
  };
});
const cjkIn = (s) => [...new Set(s.match(CJK) || [])];
ok(cjkIn(purity.stage).length === 0,
   `⑬ CJK 纯度闸：舞台里出现了 ${cjkIn(purity.stage).slice(0, 12).join('')} —— 英文版除语言钮外零 CJK`);
ok(cjkIn(purity.swap).length === 0,
   `⑬ CJK 纯度闸：主题钮文案「${purity.swap}」含 CJK（英文版应为 DARK / LIGHT）`);
ok(purity.lang.trim() === '中文',
   `⑬ 语言钮文案应为「中文」，实测「${purity.lang}」`);

// ⑭ 语言切换钮：<button> · 常显 · 指向中文版 · print 隐藏 · 不挂 data-step · 与主题钮不重叠
const lang = await pg.evaluate(() => {
  const el = document.getElementById('deckLang');
  const sw = document.getElementById('deckSwap');
  if (!el || !sw) return null;
  const r = el.getBoundingClientRect(), s = sw.getBoundingClientRect();
  const overlap = !(r.right < s.left || r.left > s.right || r.bottom < s.top || r.top > s.bottom);
  return {
    tag: el.tagName, op: +getComputedStyle(el).opacity, pos: getComputedStyle(el).position,
    w: Math.round(r.width), h: Math.round(r.height),
    step: el.hasAttribute('data-step'), overlap,
    inStage: !!el.closest('.deck-stage'),
    gap: Math.round(s.top - r.bottom),
  };
});
ok(lang, '⑭ 缺语言切换钮 #deckLang');
if (lang) {
  ok(lang.tag === 'BUTTON', `⑭ 语言钮必须是 <button>（a[href]=0 闸），实测 <${lang.tag}>`);
  ok(lang.pos === 'fixed', `⑭ 语言钮非 fixed（${lang.pos}）`);
  ok(lang.op >= 0.5 && lang.op <= 0.75, `⑭ 语言钮应为常显 pill（opacity .5–.75），实测 ${lang.op}`);
  ok(lang.w > 0 && lang.h > 0, '⑭ 语言钮尺寸为 0');
  ok(!lang.step, '⑭ 语言钮挂了 data-step —— 本 deck 零分步');
  ok(!lang.inStage, '⑭ 语言钮跑进舞台里了（它是 chrome，不是页内容）');
  ok(!lang.overlap, '⑭ 语言钮与主题钮重叠 —— 同角摆位必须互不打架');
  ok(lang.gap >= 4 && lang.gap <= 24, `⑭ 语言钮与主题钮间距 ${lang.gap}px（应在 4–24 之间）`);
}
// print 下两枚 chrome 钮都隐藏
await pg.emulateMedia({ media: 'print' });
const printHidden = await pg.evaluate(() => ({
  lang: getComputedStyle(document.getElementById('deckLang')).display,
  swap: getComputedStyle(document.getElementById('deckSwap')).display,
}));
ok(printHidden.lang === 'none', `⑭ print 下语言钮未隐藏（${printHidden.lang}）`);
ok(printHidden.swap === 'none', `⑭ print 下主题钮未隐藏（${printHidden.swap}）`);
await pg.emulateMedia({ media: 'screen' });
// 跳转目标（只读脚本文本，不真跳 —— 真跳在 ⑮ round-trip 里）
const langHref = await pg.evaluate(() =>
  [...document.querySelectorAll('script')].map(s => s.textContent).join('\n'));
ok(/deckLang[\s\S]{0,400}convoai-postloan\.html/.test(langHref)
   && /deckLang[\s\S]{0,400}"\/convoai-postloan"/.test(langHref),
   '⑭ 语言钮的跳转目标不是中文版（应同时覆盖 /decks/*.html 预览与 /convoai-postloan 线上两条路径）');

// ⑦ 事实在场闸
for (const [p, kws] of FACTS) {
  const t = await pageText(p);
  for (const kw of kws) ok(t.includes(kw), `⑦ P${p} 缺在场事实「${kw}」`);
}
// ⑦ 反向：新造数字闸。摘掉页码 sig 与路线条页号（都是**本 deck 自己的页码**，
//    不是内容里的数字）——不摘的话白名单得把 10–15 全收进去，闸门当场钝化。
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

// ⑧ SOURCE ledger 四段制（英文版收尾一律 Facts as of 2026.08）
const srcRows = await pg.evaluate(() =>
  [...document.querySelectorAll('.deck-stage .src')].map(e => e.textContent.replace(/\s+/g, ' ').trim()));
ok(srcRows.length === 5, `⑧ SOURCE ledger 行数 ${srcRows.length} != 5`);
srcRows.forEach(s => {
  ok(s.startsWith('SOURCE · '), `⑧ SOURCE 行不以「SOURCE · 」起手：「${s.slice(0, 40)}」`);
  ok(s.endsWith('· Facts as of 2026.08'), `⑧ SOURCE 行未以 Facts as of 收尾：「${s.slice(-30)}」`);
  ok((s.match(/ · /g) || []).length === 3, `⑧ SOURCE 行不是四段制：「${s.slice(0, 60)}」`);
  ok(!/https?:/.test(s), `⑧ SOURCE 行写了 URL —— 家族格式只写机构名：「${s.slice(0, 40)}」`);
});

// ⑩ 每页动效名册交给 qa-motion.mjs；这里只验「图页不为零」+ 两张重点页的下限
const mo = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(
  s => s.querySelectorAll('.mo-packet,.mo-drift,.mo-cycle,.mo-pulse,.mo-breathe,.mo-halo').length));
[2, 3, 4, 5, 6, 9, 11, 12, 13].forEach(p =>
  ok(mo[p - 1] > 0, `⑩ P${p} 在运动件名册上却没有任何常驻动效件`));
ok(mo[4] >= 14, `⑩ P5（八环闭环 · 标杆动效页）运动件只剩 ${mo[4]} 个（下限 14）`);
ok(mo[10] >= 11, `⑩ P11（能力闭环 · 第二重点）运动件只剩 ${mo[10]} 个（下限 11）`);

// ⑪ deckSwap 常显 chip + 真实切换（英文版按钮文案 DARK / LIGHT）
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
ok(sw.label === (flipped === 'dark' ? 'LIGHT' : 'DARK'), `⑪ 按钮文案 ${sw.label}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

// ⑫ 键盘翻页（共享 deck.js 运行时接上了）
await pg.evaluate(() => { document.activeElement?.blur(); location.hash = '#1'; });
await pg.waitForTimeout(500);
await pg.keyboard.press('ArrowRight');
await pg.waitForTimeout(350);
const cur = await pg.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
ok(cur === '2', `⑫ 方向键翻页失灵，当前 P${cur}`);

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));

// ⑮ 互跳 round-trip（真点、真跳、真加载）
const rt = await roundTrip();
ok(rt.ok, '⑮ 语言互跳 round-trip 失败：\n' + rt.trace.map(l => '    ' + l).join('\n'));
rt.trace.forEach(l => console.log('· ' + l));

console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
  : `✓ PASS ${THEME} · ${N} 页全绿 · 措辞红线全清（threaten 仅 P7 豁免节点 1 次）· `
    + `CJK 纯度闸通过（除语言钮）· 客户名 0 · a[href]=0 · 数字白名单闸通过 · `
    + `SOURCE ledger 5 行四段制 · hot 件每页 ≤1 · 主标全单行 · deckSwap 常显 · 语言互跳 round-trip 通过`);
await b.close();
process.exit(fails.length ? 1 : 0);
