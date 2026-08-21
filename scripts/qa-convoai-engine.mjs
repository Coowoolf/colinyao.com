// QA · convoai-engine 引擎产品详解（18 页 · CONF 家族 · 双主题 · P6/P7/P15 各 1 步 build）
// 从 qa-convoai-info.mjs 改：BOARD = {1:title, 18:title}，其余 content /
// 删掉 hero-art（⑤⑨）、eco-art（⑩）、抽屉（⑪）三组断言 —— 引擎 deck 不带抽屉。
// 新增：
//   ⑧ P17 数据修正闸 —— 必须含「100万+」「900亿+」「IDC 中国视频云市场报告」，
//      必须不含旧错误口径「93万」「700亿」「覆盖场景 · 20+」「对话式 AI 引擎市场占有率」，
//      也不许回归未批准的「43.4%」具体份额数字
//   ⑩ 机理页 + 大图页内容闸：
//      P3 双工三模式「不能插话」/「选择不插话」· P4 全双工「AEC」/「340ms」·
//      P7 VAD「ten-vad」/「WebRTC VAD」/「语义判停」/「Apache 2.0」，且 P7 不许出现「MIT」
//      （TEN VAD 是 Apache-2.0，写成 MIT 是常见错写，这一条钉死）
//      P8 产品架构大图「AEC」/「打断快路径」/「SOS / EOS」/「SD-RTN」/「650ms」
//   ② 分步闸改为逐页比对 data-steps 与页内实际 [data-step] 的最大值（不再要求全 0）
// 2026-08-20 二轮：VAD 之后插入 P8 产品架构大图，原 P8–P16 全部 +1。
// 2026-08-21 大内容轮 17 → 20：P10 SAL 重做 / P11 弱网补 AI QoS / P12 多模态聚焦视觉 /
//   新增 P13 Physical AI · R1、P14 Physical AI 案例墙、P19 OpenAI 合作（title 板）。
// 2026-08-21 收束轮 20 → 18（本文件当前口径）：删 P14 案例墙、删原 P20 收尾页；
//   原 P15–P18 各 −1（编排 → P14 / 接入架构 → P15 / 场景 → P16 / Why Agora → P17，
//   口径锁跟着搬到 data-p=17）；原 P19 OpenAI → P18 并升为末页（logo 锁定版 + 继承 CTA 行）。
//   随之改动的断言：⑥ P13 两张 R1 实拍图必须真加载；⑦ deckSwap 改常显 chip（不再验隐身）；
//   ⑫ P18 lt/dk 双 logo 的双主题显隐；删掉 P14 案例名闸与 P20 CTA 闸（CTA 断言搬到 P18）。
// 用法：node scripts/qa-convoai-engine.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8777 node scripts/qa-convoai-engine.mjs   （换端口）
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const N = 18;
// 分步页：P6 实时语音链路 / P7 VAD / P15 接入架构，各一步；其余 0
const EXP_STEPS = new Array(N).fill(0);
[6, 7, 15].forEach(p => { EXP_STEPS[p - 1] = 1; });
// title 板两页：P1 封面 / P18 OpenAI 合作（末页 · quote 语域 · logo 锁定版）
const BOARD = { 1: 'title', 18: 'title' };                   // 其余一律 content
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
ok(meta.sigs.length === N && meta.sigs.every((s, i) => s === `${i + 1}/${N}`), `① 页码 sig 不齐（应为 N/${N}）`);
ok(THEME === 'dark' ? meta.theme === 'dark' : meta.theme !== 'dark', `① 主题态异常 ${meta.theme}`);
ok(meta.title === '声网 · 对话式 AI 引擎 · 产品介绍', `① title 漂移「${meta.title}」`);

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

// ③④⑥ 逐页：板（数 / 类 / 主题源）、图加载、溢出（画布溢出 + 卡内溢出）
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

// ⑤ 页内必有 kicker + 标题（title 板的末页没有 kicker，单独放行）
const shape = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map((s, i) => ({
  p: i + 1, kk: !!s.querySelector('.kk'), hh: !!s.querySelector('.hh, .ink'),
})));
shape.forEach(v => {
  ok(v.hh, `⑤ P${v.p} 缺主标题`);
  if (v.p !== N) ok(v.kk, `⑤ P${v.p} 缺 kicker`);
});

// ⑧ P17 数据修正闸：新口径必须在，旧错误口径必须绝迹（全页维度也扫一遍）
//    （页号 16 → 18 → 17，四张 KPI 数字一字未动；
//     43.4% 具体份额未取得公司批准口径，改为定性表述 + 报告名写全）
const p17 = await pg.evaluate(() => document.querySelector('.slide[data-p="17"]').textContent.replace(/\s+/g, ' '));
const all = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));
['No.1', '100万+', '900亿+', '50+',
 '市场占有率', '单月支撑通话分钟数', '全球注册应用数',
 'IDC 中国视频云市场报告', '份额超过第 2–8 位厂商总和'].forEach((s) => {
  ok(p17.includes(s), `⑧ P17 缺「${s}」`);
});
['93万', '700亿', '覆盖场景 · 20+', '覆盖场景', '对话式 AI 引擎市场占有率', '20+ 行业',
 '43.4%'].forEach(s => {
  ok(!all.includes(s), `⑧ 旧 / 未批准口径回归：「${s}」`);
});
ok(p17.includes('SOURCE · 声网官网 / IR 公开口径 · IDC 中国视频云市场报告 · 事实截止 2026.08'),
   '⑧ P17 SOURCE 行不符');
ok(p17.includes('2014 年成立'), '⑧ P17 缺收尾行');

// ⑩ 机理页 + 大图页内容闸（P3 双工三模式 / P4 全双工工作原理 / P7 VAD / P8 产品架构大图）
const pageText = async (p) => pg.evaluate((k) =>
  document.querySelector(`.slide[data-p="${k}"]`).textContent.replace(/\s+/g, ' '), p);
const [p3, p4, p7, p8] = await Promise.all([pageText(3), pageText(4), pageText(7), pageText(8)]);
[['不能插话', p3, 'P3'], ['选择不插话', p3, 'P3'],
 ['单工', p3, 'P3'], ['半双工', p3, 'P3'], ['全双工', p3, 'P3'],
 ['AEC', p4, 'P4'], ['340ms', p4, 'P4'], ['全双工', p4, 'P4'],
 ['WebRTC VAD', p7, 'P7'], ['语义判停', p7, 'P7'], ['TEN VAD', p7, 'P7'],
 // ── P8 产品架构大图：四个可读性锚点 + 底座，一个都不能掉 ──
 ['AEC', p8, 'P8'], ['打断快路径', p8, 'P8'], ['SOS / EOS', p8, 'P8'],
 ['SD-RTN', p8, 'P8'], ['650ms', p8, 'P8'],
 ['AI-VAD', p8, 'P8'], ['不经过 LLM', p8, 'P8'], ['参考信号', p8, 'P8'],
 ['客户业务服务器', p8, 'P8'], ['终端设备', p8, 'P8'], ['声网引擎云', p8, 'P8'],
].forEach(([needle, txt, tag]) => ok(txt.includes(needle), `⑩ ${tag} 缺「${needle}」`));
ok(/ten-vad/i.test(p7), '⑩ P7 缺 ten-vad 仓库地址');
ok(/apache\s*2\.0/i.test(p7), '⑩ P7 缺「Apache 2.0」—— TEN VAD 的开源协议必须写明');
ok(!/\bMIT\b/.test(p7), '⑩ P7 出现「MIT」—— TEN VAD 是 Apache-2.0，不是 MIT');
ok(p7.includes('SOS/EOS 判停重构自 V2.6'), '⑩ P7 SOURCE 行未改成「判停重构自 V2.6」口径');
// ⑩ P5 / P11 的 SOURCE 行（三个极致数字 + 弱网数字必须自带出处与「典型值」限定）
const [p5, p11] = await Promise.all([pageText(5), pageText(11)]);
[[p5, 'P5'], [p11, 'P11']].forEach(([txt, tag]) =>
  ok(txt.includes('SOURCE · 声网官网 · 引擎发版说明 公开口径 · 典型值 · 事实截止 2026.08'),
     `⑩ ${tag} 缺 SOURCE 行（典型值口径）`));
// ⑩ P6：数字人已移出串行主链（标题也从「端到端链路」改成「实时语音链路」）
const p6 = await pageText(6);
ok(p6.includes('一条深度优化的实时语音链路'), '⑩ P6 标题未改成「实时语音链路」');
ok(p6.includes('数字人 · 可选'), '⑩ P6 缺「数字人 · 可选」虚线支路');
// ⑩ P18 末页：从被删的原 P20 收尾页继承来的 CTA 行（真实入口不许随页消失）
const p18 = await pageText(18);
ok(p18.includes('agora.io › 对话式 AI 引擎'), '⑩ P18 缺 CTA 行（原 P20 收尾页继承）');

// ⑪ 2026-08-21 两轮（大内容轮 + 收束轮）的内容闸
const [p10, p12, p13, p14] = await Promise.all(
  [10, 12, 13, 14].map(pageText));   // p11 / p18 上面已取过，复用
[// P10 · 三种噪声 · 三层方案（噪声名 + 方案名一个都不能掉，land 是 Colin aiot26 定稿）
 ['稳态', p10, 'P10'], ['瞬态', p10, 'P10'], ['非对话人', p10, 'P10'],
 ['传统降噪', p10, 'P10'], ['AI 降噪', p10, 'P10'], ['SAL', p10, 'P10'],
 ['屏蔽 95% 干扰', p10, 'P10'],
 ['前两类是信号问题', p10, 'P10'],
 // P11 · 弱网两机制（AI QoS 是本轮新增的机理，FEC / 本地缓存是它的两个抓手）
 ['AI QoS', p11, 'P11'], ['断网续播', p11, 'P11'], ['FEC', p11, 'P11'],
 ['本地缓存', p11, 'P11'], ['80% 丢包', p11, 'P11'], ['3–5s 瞬时断网', p11, 'P11'],
 // P12 · 聚焦视觉模态（加重两路在，弱化两路仍在图上但降权）
 ['看图识景', p12, 'P12'], ['智能眼镜', p12, 'P12'], ['数字人', p12, 'P12'],
 ['声纹锁定', p12, 'P12'], ['SIP 电话', p12, 'P12'], ['前文已述', p12, 'P12'],
 ['让对话，走出屏幕', p12, 'P12'],
 // P13 · R1 开发套件（双源 canon：31p 拜访版 P21 + robot26 #32）
 ['R1-WiFi', p13, 'P13'], ['R1-4G', p13, 'P13'],
 ['2025.03.20', p13, 'P13'], ['2025.09.26', p13, 'P13'],
 ['BK7258', p13, 'P13'], ['UNISOC 8910', p13, 'P13'], ['单芯片一体化', p13, 'P13'],
 ['30000+', p13, 'P13'], ['拿来即用的伙伴感地基', p13, 'P13'],
 ['你做产品与角色', p13, 'P13'],
 // P13 带图重排后新增的两枚角标 / 图注（robot26 #32 原措辞）
 ['[ R1 WI-FI ]', p13, 'P13'], ['[ R1 4G ]', p13, 'P13'],
 ['带「灵动眼睛」PCB', p13, 'P13'], ['带 4G 天线 · 一体化', p13, 'P13'],
 // P14 · 编排（原 P15；箭头语义修后，图例必须自证只有两种插入线型 + 一个换装件）
 ['插入 · 指向引擎', p14, 'P14'], ['按需插入', p14, 'P14'], ['可替换 · 换装', p14, 'P14'],
 ['实时调试', p14, 'P14'],
 // P18 · OpenAI 合作 · 末页（Colin 指令口径：底座 = 对话式 AI 引擎底座；泛化为对话式智能体）
 ['对话式 AI 引擎底座', p18, 'P18'], ['全球最强的 Voice Agent 团队', p18, 'P18'],
 ['对话式智能体', p18, 'P18'], ['全球首批合作伙伴', p18, 'P18'],
 ['A QUIET ENDORSEMENT', p18, 'P18'],
].forEach(([needle, txt, tag]) => ok(txt.includes(needle), `⑪ ${tag} 缺「${needle}」`));
// ⑪ 反向闸：Colin 明确点掉的两处措辞不许回流
ok(!p18.includes('实时通信底座'), '⑪ P18 出现「实时通信底座」—— Colin 指令写「对话式 AI 引擎底座」');
ok(!p18.includes('消费机器人'), '⑪ P18 出现「消费机器人」—— robot26 原句已按指令泛化为「对话式智能体」');
ok(!p18.includes('全球首个'), '⑪ P18 出现「全球首个」—— 首批口径已钉死（info 二轮仲裁 P0）');
// ⑪ 收束轮删页闸：案例墙（P14）与旧收尾页（P20）的内容一律不许残留在任何一页
['集贤科技', 'Robopoet', 'luwu', 'Pophie', 'LOOKTECH', 'HeyCyan', 'LOOKEE',
 '你的场景，多半能对上号', '忘了它是 AI', '把技术藏进体验里'].forEach(nd =>
  ok(!all.includes(nd), `⑪ 已删页内容回流：「${nd}」`));
// ⑪ P13 的 R1 日期只有两枚 canon（robot26 #32 / 31p 拜访版 P21 双源一致），
//    页面上出现的任何 yyyy.mm.dd 都必须落在这两枚里 —— 防止后续改稿写进第三个日期
const _p13dates = [...new Set(p13.match(/\d{4}\.\d{2}\.\d{2}/g) || [])];
ok(_p13dates.every(d => d === '2025.03.20' || d === '2025.09.26'),
   `⑪ P13 出现未授权的 R1 日期：${_p13dates.join(' / ')}`);
// ⑫ P13 两张 R1 实拍图 + P18 双源 logo：跨 deck 引用 robot26 资产，必须真的解出像素
const media = await pg.evaluate(() => {
  const one = (sel) => [...document.querySelectorAll(sel)].map(im => ({
    src: im.getAttribute('src'), w: im.naturalWidth,
    shown: getComputedStyle(im).display !== 'none',
  }));
  return { r1: one('.slide[data-p="13"] .r1-shot img'), lk: one('.slide[data-p="18"] .lock img') };
});
ok(media.r1.length === 2, `⑫ P13 实拍图数 ${media.r1.length} != 2`);
media.r1.forEach((im, i) => {
  ok(im.w > 0, `⑫ P13 实拍图 ${i + 1} 未解码（${im.src}）`);
  ok(/\/decks\/assets\/robot26\/r1-(wifi|4g)\.webp$/.test(im.src || ''),
     `⑫ P13 实拍图 ${i + 1} 路径不是 robot26 跨引用：${im.src}`);
});
ok(media.lk.length === 2, `⑫ P18 logo 锁定版应为 lt/dk 双 img，实测 ${media.lk.length}`);
media.lk.forEach((im, i) => ok(im.w > 0, `⑫ P18 logo ${i + 1} 未解码（${im.src}）`));
{
  const lt = media.lk[0], dk = media.lk[1];
  ok(/openai-agora-light\.png$/.test(lt.src || ''), `⑫ P18 浅色源不符 ${lt.src}`);
  ok(/openai-agora\.webp$/.test(dk.src || ''), `⑫ P18 深色源不符 ${dk.src}`);
  ok(THEME === 'dark' ? (!lt.shown && dk.shown) : (lt.shown && !dk.shown),
     `⑫ P18 logo 双主题显隐反了（theme=${THEME} lt=${lt.shown} dk=${dk.shown}）`);
}

// ⑦ 主题切换：deckSwap 按钮真实切换（板源跟着翻）
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
ok(swapVis && swapVis.pos === 'fixed', '⑦ deckSwap 缺失或非 fixed');
// 2026-08-21 Colin：「没有浅色切换的键」。本 deck 是对外发链接的产品文档，
// 主题键必须默认可见（家族可见档 .5–.7），不再是 info 那套 hover 才呼出的隐身件。
ok(swapVis && swapVis.op >= 0.5 && swapVis.op <= 0.75,
   `⑦ deckSwap 应为常显 chip（opacity .5–.75），实测 ${swapVis && swapVis.op}`);
ok(swapVis && swapVis.w > 0 && swapVis.h > 0, '⑦ deckSwap 尺寸为 0');
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
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 分步 P6/P7/P15 各 1 步 · P17 口径已锁 · P8 大图闸 · P13 实拍图 + P18 双源 logo 闸 · deckSwap 常显`);
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

