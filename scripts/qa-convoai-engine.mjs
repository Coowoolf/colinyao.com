// QA · convoai-engine 引擎产品详解（16 页 · CONF 家族 · 双主题 · 全页 data-steps=0）
// 从 qa-convoai-info.mjs 改：N=16 / EXP_STEPS 全 0 / BOARD = {1:title, 16:title}，其余 content /
// 删掉 hero-art（⑤⑨）、eco-art（⑩）、抽屉（⑪）三组断言 —— 引擎 deck 不带位图资产，也不带抽屉。
// 新增：
//   ⑧ P15 数据修正闸 —— 必须含「100万+」「900亿+」「43.4%」，
//      必须不含旧错误口径「93万」「700亿」「覆盖场景 · 20+」「对话式 AI 引擎市场占有率」
//   ⑩ 三张新机理页的内容闸（2026-08-20 扩页 13→16）：
//      P3 双工三模式「不能插话」/「选择不插话」· P4 全双工「AEC」/「340ms」·
//      P7 VAD「ten-vad」/「WebRTC VAD」/「语义判停」/「Apache 2.0」，且 P7 不许出现「MIT」
//      （TEN VAD 是 Apache-2.0，写成 MIT 是常见错写，这一条钉死）
// 用法：node scripts/qa-convoai-engine.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8777 node scripts/qa-convoai-engine.mjs   （换端口）
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const N = 16;
const EXP_STEPS = new Array(N).fill(0);
const BOARD = { 1: 'title', 16: 'title' };      // 其余一律 content
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
await pg.goto(BASE + '/decks/convoai-engine.html#1', { waitUntil: 'load' });
// 动效归零：入场是 transition（.rise 起手 translateY(42px)），不掐掉就会把「还没落位」
// 读成「卡片冲出 .sh 盒」的假溢出（occlusion-scan.mjs 同一手法）
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
}));
ok(meta.n === N, `① 页数 ${meta.n} != ${N}`);
ok(meta.secs === N, `① section 数 ${meta.secs} != ${N}`);
ok(meta.noindex, '① 缺 noindex');
ok(meta.sigs.length === N && meta.sigs.every((s, i) => s === `${i + 1}/${N}`), '① 页码 sig 不齐（应为 N/16）');
ok(THEME === 'dark' ? meta.theme === 'dark' : meta.theme !== 'dark', `① 主题态异常 ${meta.theme}`);
ok(meta.title === '声网 · 对话式 AI 引擎 · 产品介绍', `① title 漂移「${meta.title}」`);

// ② 分步数：全 0，且页内不许残留任何 data-step
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => +s.dataset.steps));
EXP_STEPS.forEach((e, i) => ok(steps[i] === e, `② P${i + 1} steps ${steps[i]} != ${e}`));
const stray = await pg.evaluate(() => [...document.querySelectorAll('.slide')]
  .map((s, i) => [i + 1, s.querySelectorAll('[data-step]').length]).filter(([, n]) => n));
stray.forEach(([p, n]) => fails.push(`② P${p} 残留 data-step ×${n}（这份 deck 不许分步）`));

// ③④⑥ 逐页：板（数 / 类 / 主题源）、图加载、溢出（画布溢出 + 卡内溢出）
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
    // 溢出：sh 内容不出画布；卡片内容不冲出卡底
    const out = [];
    s.querySelectorAll('.pp .sh').forEach(el => {
      const r0 = el.getBoundingClientRect();
      [...el.children].forEach(ch => {
        const r1 = ch.getBoundingClientRect();
        if (r1.bottom > 1080 - 6 || r1.right > 1920 + 6 || r1.left < -6) out.push('canvas:' + (el.className || '').slice(0, 40));
      });
      // 网格容器 height:100% 之后，卡片不许冲出所属 .sh 盒（TEXT-x-SPILL 的源头）
      if (el.className.match(/card-c|g4|g3|g2/) || el.querySelector(':scope > .g4,:scope > .g3,:scope > .g2')) {
        el.querySelectorAll('*').forEach(ch => {
          if (ch.getBoundingClientRect().bottom > r0.bottom + 6) out.push('cardspill:' + (el.className || '').slice(0, 44));
        });
      }
    });
    return { bgN: bgs.length, bgCls, bgUrl, badImgs, out };
  }, i);
  ok(r.bgN === 1, `④ P${i} conf-bg 数 ${r.bgN}`);
  const expB = BOARD[i] || 'content';
  ok(r.bgCls === 'conf-bg-' + expB, `④ P${i} 板 ${r.bgCls} != ${expB}`);
  ok(r.bgUrl.includes(THEME === 'dark' ? '-dark.png' : '-light.png'), `④ P${i} 板主题源不符 ${r.bgUrl}`);
  ok(r.badImgs.length === 0, `⑥ P${i} 图未加载 ${r.badImgs.join()}`);
  [...new Set(r.out)].forEach(o => fails.push(`③ P${i} 溢出 ${o}`));
  await pg.waitForTimeout(50);
}

// ⑤ 页内必有 kicker + 标题（title 板的 P16 没有 kicker，单独放行）
const shape = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map((s, i) => ({
  p: i + 1, kk: !!s.querySelector('.kk'), hh: !!s.querySelector('.hh, .ink'),
})));
shape.forEach(v => {
  ok(v.hh, `⑤ P${v.p} 缺主标题`);
  if (v.p !== 16) ok(v.kk || v.p === 16, `⑤ P${v.p} 缺 kicker`);
});

// ⑧ P15 数据修正闸：新口径必须在，旧错误口径必须绝迹（全页维度也扫一遍）
//    （扩页 13→16 后 Why Agora 从 P12 挪到 P15，内容一字未动）
const p15 = await pg.evaluate(() => document.querySelector('.slide[data-p="15"]').textContent.replace(/\s+/g, ' '));
const all = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));
[['No.1', 1], ['100万+', 1], ['900亿+', 1], ['43.4%', 1], ['50+', 1],
 ['市场占有率', 1], ['单月支撑通话分钟数', 1], ['全球注册应用数', 1]].forEach(([s]) => {
  ok(p15.includes(s), `⑧ P15 缺「${s}」`);
});
['93万', '700亿', '覆盖场景 · 20+', '覆盖场景', '对话式 AI 引擎市场占有率', '20+ 行业'].forEach(s => {
  ok(!all.includes(s), `⑧ 旧错误口径回归：「${s}」`);
});
ok(p15.includes('SOURCE · 声网官网 / IR 公开口径 · IDC'), '⑧ P15 缺 SOURCE 行');
ok(p15.includes('2014 年成立'), '⑧ P15 缺收尾行');

// ⑩ 三张新机理页内容闸（P3 双工三模式 / P4 全双工工作原理 / P7 VAD）
const pageText = async (p) => pg.evaluate((k) =>
  document.querySelector(`.slide[data-p="${k}"]`).textContent.replace(/\s+/g, ' '), p);
const [p3, p4, p7] = await Promise.all([pageText(3), pageText(4), pageText(7)]);
[['不能插话', p3, 'P3'], ['选择不插话', p3, 'P3'],
 ['单工', p3, 'P3'], ['半双工', p3, 'P3'], ['全双工', p3, 'P3'],
 ['AEC', p4, 'P4'], ['340ms', p4, 'P4'], ['全双工', p4, 'P4'],
 ['WebRTC VAD', p7, 'P7'], ['语义判停', p7, 'P7'], ['TEN VAD', p7, 'P7'],
].forEach(([needle, txt, tag]) => ok(txt.includes(needle), `⑩ ${tag} 缺「${needle}」`));
ok(/ten-vad/i.test(p7), '⑩ P7 缺 ten-vad 仓库地址');
ok(/apache\s*2\.0/i.test(p7), '⑩ P7 缺「Apache 2.0」—— TEN VAD 的开源协议必须写明');
ok(!/\bMIT\b/.test(p7), '⑩ P7 出现「MIT」—— TEN VAD 是 Apache-2.0，不是 MIT');

// ⑦ 主题切换：deckSwap 按钮真实切换（板源跟着翻）
await pg.evaluate(() => {
  window.deck.i = 0;
  document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === 0));
});
const swapVis = await pg.evaluate(() => {
  const b = document.getElementById('deckSwap');
  return b ? { op: +getComputedStyle(b).opacity, pos: getComputedStyle(b).position } : null;
});
ok(swapVis && swapVis.pos === 'fixed', '⑦ deckSwap 缺失或非 fixed');
ok(swapVis && swapVis.op < 0.05, `⑦ deckSwap 默认应隐身，实测 opacity=${swapVis && swapVis.op}`);
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
ok(THEME === 'dark' ? sw.theme !== 'dark' : sw.theme === 'dark', `⑦ 切换后主题态 ${sw.theme}`);
ok(sw.bg.includes('-' + flipped + '.png'), '⑦ 切换后板源未换');
ok(sw.ls === flipped, `⑦ localStorage("colin-theme") 未写入 ${flipped}（实得 ${sw.ls}）`);
ok(sw.label === (flipped === 'dark' ? '浅底' : '暗底'), `⑦ 按钮文案 ${sw.label}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

// ⑨ 键盘翻页（deck.js 运行时接上了）
await pg.evaluate(() => { document.activeElement?.blur(); location.hash = '#1'; });
await pg.waitForTimeout(500);
await pg.keyboard.press('ArrowRight');
await pg.waitForTimeout(350);
const cur = await pg.evaluate(() => document.querySelector('.slide.active')?.dataset.p);
ok(cur === '2', `⑨ 方向键翻页失灵，当前 P${cur}`);

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 全页 data-steps=0 · P15 口径已锁 · 新三页内容闸通过`);
await b.close();
/* 双生闸：/convoai 主路由与 convoai-engine.html 别名必须逐字节一致（同 builder 一次写出） */
{
  const [a, b] = await Promise.all([
    fetch(BASE + '/decks/convoai.html').then(r => r.text()),
    fetch(BASE + '/decks/convoai-engine.html').then(r => r.text()),
  ]);
  if (a !== b) { console.error('✗ 双生不一致：convoai.html ≠ convoai-engine.html'); process.exit(1); }
  console.log('✓ 双生一致 · convoai.html == convoai-engine.html');
}

process.exit(fails.length ? 1 : 0);

