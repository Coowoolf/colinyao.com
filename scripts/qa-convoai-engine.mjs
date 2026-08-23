// QA · convoai-engine 引擎产品详解（22 页 · CONF 家族 · 双主题 · P6/P7/P14/P20 各 1 步 build）
// 从 qa-convoai-info.mjs 改：BOARD = {1:title, 22:title}，其余 content /
// 删掉 hero-art（⑤⑨）、eco-art（⑩）、抽屉（⑪）三组断言 —— 引擎 deck 不带抽屉。
// 新增：
//   ⑧ P21 数据修正闸 —— 必须含「100万+」「900亿+」「IDC 中国视频云市场报告」，
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
// 2026-08-21 Call Agent 章 18 → 21（本文件当前口径）：新增 P16 登场 · 成绩单 /
//   P17 五个大脑 · Agent Harness / P18 Loop Engineering · 成长飞轮；页序按 Colin 指令
//   「场景之后接 Call Agent，Call Agent 之后接 R1」重排 ——
//   原 14 编排→13 / 原 15 接入→14 / 原 16 场景→15 / 原 13 R1→19 / 原 17 Why→20 / 原 18 OpenAI→21。
//   随之：N=21、BOARD={1,21}、分步 [6,7,14]、口径锁 data-p=20、实拍图闸 data-p=19、
//   OpenAI logo 闸 data-p=21；新增 ⑬ Call Agent 三页内容闸 + 价格 / staging 反向闸。
// 2026-08-21 视频页 21 → 22（本文件当前口径）：R1（P19）之后插入 P20 无人机秀全屏视频页
//   （robot26 #24 同款机制），Why Agora → P21、OpenAI 末页 → P22。
//   随之：N=22、BOARD={1,22}、分步 [6,7,14,20]、口径锁 data-p=21、logo 闸 data-p=22；
//   新增 ⑭ 视频页闸（video 在位 / 静置态无 controls / muted+playsinline+preload=none+poster /
//   data-play-step=1 / 容器贴 0,0 满幅 / video 计算尺寸 1920×1080 且 object-fit:cover）；
//   ⑤ 版式闸给 P20 开豁免（纯片子页没有 kicker 也没有标题，robot26 #24 同款）；
//   console / pageerror 加媒体类豁免 —— 本容器 chromium 无 H.264，play() 必然 reject，
//   那是环境不是页面（豁免正则抄 qa-robot26.mjs 的 MEDIA_EXEMPT）。
// 用法：node scripts/qa-convoai-engine.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8777 node scripts/qa-convoai-engine.mjs   （换端口）
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const N = 22;
// 分步页：P6 实时语音链路 / P7 VAD / P14 接入架构 / P20 视频页，各一步；其余 0
const EXP_STEPS = new Array(N).fill(0);
[6, 7, 14, 20].forEach(p => { EXP_STEPS[p - 1] = 1; });
// title 板两页：P1 封面 / P22 OpenAI 合作（末页 · quote 语域 · logo 锁定版）
const BOARD = { 1: 'title', 22: 'title' };                   // 其余一律 content
// 纯全屏视频页：没有 kicker、没有标题（robot26 #24 同款「一页只有一支片子」）
const VIDEO_PAGE = 20;
// 媒体类报错豁免：CI 容器的 chromium 不带 H.264 解码器，video.play() 必然 reject、
// 资源解码必然报 DEMUXER_ERROR —— 那是环境的事，不是页面的事（同 qa-robot26.mjs）
const MEDIA_EXEMPT = /err:?\s*4|MEDIA_ELEMENT_ERROR|DEMUXER_ERROR|not supported|NotSupportedError|play\(\) request|no supported source/i;
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const errs = [];
const mediaErrs = [];
pg.on('pageerror', e => (MEDIA_EXEMPT.test(String(e)) ? mediaErrs : errs).push('PAGEERROR ' + e.message));
pg.on('console', m => {
  if (m.type() !== 'error') return;
  if ((m.location()?.url || '').includes('favicon')) return;
  if (MEDIA_EXEMPT.test(m.text())) { mediaErrs.push(m.text()); return; }
  errs.push(m.text());
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
      // 满幅件（.sh.vid 视频页）贴边就是它的规格：版心件要求离画布底 6px，满幅件只验「不出画布」。
      // 不给它开这个口子的话，一只 0,0→1920×1080 的片子会稳报一条假溢出。
      const full = el.classList.contains('vid');
      const bMax = full ? 1080.5 : 1080 - 6, rMax = full ? 1920.5 : 1920 + 6, lMin = full ? -0.5 : -6;
      [...el.children].forEach(ch => {
        const r1 = ch.getBoundingClientRect();
        if (r1.bottom > bMax || r1.right > rMax || r1.left < lMin) out.push('canvas:' + (el.className || '').slice(0, 40));
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
  if (v.p === VIDEO_PAGE) {
    // 纯片子页：**没有主标题**仍然是它的规格；2026-08-23 采纳项 E 给它补了一枚
    // 静态角标 kicker（反白压左上角），所以 kicker 反过来变成必需件。
    ok(!v.hh, `⑤ P${v.p} 视频页不该带主标题（robot26 #24 是纯片子）`);
    ok(v.kk, `⑤ P${v.p} 缺静态角标 kicker（采纳项 E ②）`);
    return;
  }
  ok(v.hh, `⑤ P${v.p} 缺主标题`);
  if (v.p !== N) ok(v.kk, `⑤ P${v.p} 缺 kicker`);
});

// ⑧ P20 数据修正闸：新口径必须在，旧错误口径必须绝迹（全页维度也扫一遍）
//    （页号 16 → 18 → 17 → 20，四张 KPI 数字一字未动；
//     43.4% 具体份额未取得公司批准口径，改为定性表述 + 报告名写全）
const p21 = await pg.evaluate(() => document.querySelector('.slide[data-p="21"]').textContent.replace(/\s+/g, ' '));
const all = await pg.evaluate(() => document.getElementById('deckStage').textContent.replace(/\s+/g, ' '));
['No.1', '100万+', '900亿+', '50+',
 '市场占有率', '单月支撑通话分钟数', '全球注册应用数',
 'IDC 中国视频云市场报告', '份额超过第 2–8 位厂商总和'].forEach((s) => {
  ok(p21.includes(s), `⑧ P21 缺「${s}」`);
});
['93万', '700亿', '覆盖场景 · 20+', '覆盖场景', '对话式 AI 引擎市场占有率', '20+ 行业',
 '43.4%'].forEach(s => {
  ok(!all.includes(s), `⑧ 旧 / 未批准口径回归：「${s}」`);
});
ok(p21.includes('SOURCE · 声网官网 / IR 公开口径 · IDC 中国视频云市场报告 · 事实截止 2026.08'),
   '⑧ P21 SOURCE 行不符');
ok(p21.includes('2014 年成立'), '⑧ P21 缺收尾行');

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
//    2026-08-23 采纳项 C：并入四段 ledger —— 两个来源用「/」并列，补「事实截止」收尾。
const [p5, p11] = await Promise.all([pageText(5), pageText(11)]);
[[p5, 'P5'], [p11, 'P11']].forEach(([txt, tag]) =>
  ok(txt.includes('SOURCE · 声网官网 / 引擎发版说明 公开口径 · 典型值 · 事实截止 2026.08'),
     `⑩ ${tag} 缺 SOURCE 行（典型值口径）`));

// ⑯ SOURCE ledger 统一闸（2026-08-23 采纳项 C）：全 deck 的出处行走同一枚 .src 类、
//    同一套四段格式 `SOURCE · 来源 · 样本或时间窗 · 事实截止 2026.08`。
//    数据页一页一行，一行都不许再退回 .mono-sm（那是页内普通元信息行的类）。
{
  const led = await pg.evaluate(() => [...document.querySelectorAll('.slide')].flatMap((s, i) =>
    [...s.querySelectorAll('.src')].map(el => ({ p: i + 1, t: (el.textContent || '').trim() }))));
  const SRC_PAGES = [5, 7, 8, 11, 16, 17, 18, 19, 21];   // 引擎 deck 的九张数据页
  const live = [...new Set(led.map(x => x.p))].sort((a, b) => a - b);
  ok(live.join(',') === SRC_PAGES.join(','),
     `⑯ SOURCE ledger 覆盖漂移：实测 [${live}] != 名册 [${SRC_PAGES}]`);
  ok(led.length === SRC_PAGES.length, `⑯ SOURCE 行数 ${led.length} != ${SRC_PAGES.length}（有页挂了两行？）`);
  led.forEach(({ p, t }) => {
    ok(t.startsWith('SOURCE · '), `⑯ P${p} SOURCE 行不以「SOURCE · 」起手：「${t}」`);
    ok(t.endsWith(' · 事实截止 2026.08'), `⑯ P${p} SOURCE 行未以「· 事实截止 2026.08」收尾：「${t}」`);
    ok(t.split(' · ').length >= 3, `⑯ P${p} SOURCE 行不足三段：「${t}」`);
  });
  // 旧格式反向闸：全 deck 不许再出现「SOURCE …」却不带事实截止的行
  const stray = await pg.evaluate(() => [...document.querySelectorAll('.slide .mono-sm')]
    .map(el => (el.textContent || '').trim()).filter(t => t.startsWith('SOURCE')));
  ok(stray.length === 0, `⑯ 仍有 SOURCE 行挂在 .mono-sm 上（未并入 ledger）：${stray.join(' | ')}`);
  // 字号/色阶（采纳项 G）：.src 与 .sig 都必须是提过一档的 17px
  const sizes = await pg.evaluate(() => ({
    src: getComputedStyle(document.querySelector('.src')).fontSize,
    sig: getComputedStyle(document.querySelector('.sig')).fontSize,
  }));
  ok(sizes.src === '17px', `⑯ .src 字号 ${sizes.src} != 17px（采纳项 G：投影小字提一档）`);
  ok(sizes.sig === '17px', `⑯ .sig 字号 ${sizes.sig} != 17px（采纳项 G：投影小字提一档）`);
}

// ⑰ kicker 消歧闸（2026-08-23 采纳项 F）：P8 = 引擎内部链路 / P14 = 客户接入架构，
//    两页 kicker 各自带上限定词，翻页时不会读成同一张图的两个版本。
{
  const kick = async (p) => pg.evaluate((k) =>
    (document.querySelector(`.slide[data-p="${k}"] .kk`) || {}).textContent?.trim() || '', p);
  const [k8, k14] = await Promise.all([kick(8), kick(14)]);
  ok(/ENGINE INTERNALS/.test(k8) && /运行时内部链路/.test(k8), `⑰ P8 kicker 缺内部链路限定词：「${k8}」`);
  ok(/INTEGRATION/.test(k14) && /客户接入架构/.test(k14), `⑰ P14 kicker 缺客户接入限定词：「${k14}」`);
  ok(k8 !== k14, '⑰ P8 / P14 kicker 撞车');
}
// ⑩ P6：数字人已移出串行主链（标题也从「端到端链路」改成「实时语音链路」）
const p6 = await pageText(6);
ok(p6.includes('一条深度优化的实时语音链路'), '⑩ P6 标题未改成「实时语音链路」');
ok(p6.includes('数字人 · 可选'), '⑩ P6 缺「数字人 · 可选」虚线支路');
// ⑩ P22 末页：从被删的原 P20 收尾页继承来的 CTA 行（真实入口不许随页消失）
const p22 = await pageText(22);
ok(p22.includes('agora.io › 对话式 AI 引擎'), '⑩ P22 缺 CTA 行（原 P20 收尾页继承）');

// ⑪ 2026-08-21 两轮（大内容轮 + 收束轮）的内容闸
const [p10, p12, p19, p13] = await Promise.all(
  [10, 12, 19, 13].map(pageText));   // p11 / p22 上面已取过，复用
                                     // 页号位移：R1 = 今 P19（原 13）、编排 = 今 P13（原 14）
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
 // P19 · R1 开发套件（原 P13；双源 canon：31p 拜访版 P21 + robot26 #32）
 ['R1-WiFi', p19, 'P19'], ['R1-4G', p19, 'P19'],
 ['2025.03.20', p19, 'P19'], ['2025.09.26', p19, 'P19'],
 ['BK7258', p19, 'P19'], ['UNISOC 8910', p19, 'P19'], ['单芯片一体化', p19, 'P19'],
 ['30000+', p19, 'P19'], ['拿来即用的伙伴感地基', p19, 'P19'],
 ['你做产品与角色', p19, 'P19'],
 // R1 带图重排后新增的两枚角标 / 图注（robot26 #32 原措辞）
 ['[ R1 WI-FI ]', p19, 'P19'], ['[ R1 4G ]', p19, 'P19'],
 ['带「灵动眼睛」PCB', p19, 'P19'], ['带 4G 天线 · 一体化', p19, 'P19'],
 // P13 · 编排（原 P14；箭头语义修后，图例必须自证只有两种插入线型 + 一个换装件）
 ['插入 · 指向引擎', p13, 'P13'], ['按需插入', p13, 'P13'], ['可替换 · 换装', p13, 'P13'],
 ['实时调试', p13, 'P13'],
 // P22 · OpenAI 合作 · 末页（Colin 指令口径：底座 = 对话式 AI 引擎底座；泛化为对话式智能体）
 ['对话式 AI 引擎底座', p22, 'P22'], ['全球最强的 Voice Agent 团队', p22, 'P22'],
 ['对话式智能体', p22, 'P22'], ['全球首批合作伙伴', p22, 'P22'],
 ['A QUIET ENDORSEMENT', p22, 'P22'],
].forEach(([needle, txt, tag]) => ok(txt.includes(needle), `⑪ ${tag} 缺「${needle}」`));
// ⑪ 反向闸：Colin 明确点掉的两处措辞不许回流
ok(!p22.includes('实时通信底座'), '⑪ P22 出现「实时通信底座」—— Colin 指令写「对话式 AI 引擎底座」');
ok(!p22.includes('消费机器人'), '⑪ P22 出现「消费机器人」—— robot26 原句已按指令泛化为「对话式智能体」');
ok(!p22.includes('全球首个'), '⑪ P22 出现「全球首个」—— 首批口径已钉死（info 二轮仲裁 P0）');
// ⑪ 收束轮删页闸：案例墙（P14）与旧收尾页（P20）的内容一律不许残留在任何一页
['集贤科技', 'Robopoet', 'luwu', 'Pophie', 'LOOKTECH', 'HeyCyan', 'LOOKEE',
 '你的场景，多半能对上号', '忘了它是 AI', '把技术藏进体验里'].forEach(nd =>
  ok(!all.includes(nd), `⑪ 已删页内容回流：「${nd}」`));
// ⑪ P19 的 R1 日期只有两枚 canon（robot26 #32 / 31p 拜访版 P21 双源一致），
//    页面上出现的任何 yyyy.mm.dd 都必须落在这两枚里 —— 防止后续改稿写进第三个日期
const _p19dates = [...new Set(p19.match(/\d{4}\.\d{2}\.\d{2}/g) || [])];
ok(_p19dates.every(d => d === '2025.03.20' || d === '2025.09.26'),
   `⑪ P19 出现未授权的 R1 日期：${_p19dates.join(' / ')}`);
// ⑫ P19 两张 R1 实拍图 + P22 双源 logo：跨 deck 引用 robot26 资产，必须真的解出像素
const media = await pg.evaluate(() => {
  const one = (sel) => [...document.querySelectorAll(sel)].map(im => ({
    src: im.getAttribute('src'), w: im.naturalWidth,
    shown: getComputedStyle(im).display !== 'none',
  }));
  return { r1: one('.slide[data-p="19"] .r1-shot img'), lk: one('.slide[data-p="22"] .lock img') };
});
ok(media.r1.length === 2, `⑫ P19 实拍图数 ${media.r1.length} != 2`);
media.r1.forEach((im, i) => {
  ok(im.w > 0, `⑫ P19 实拍图 ${i + 1} 未解码（${im.src}）`);
  ok(/\/decks\/assets\/robot26\/r1-(wifi|4g)\.webp$/.test(im.src || ''),
     `⑫ P19 实拍图 ${i + 1} 路径不是 robot26 跨引用：${im.src}`);
});
ok(media.lk.length === 2, `⑫ P22 logo 锁定版应为 lt/dk 双 img，实测 ${media.lk.length}`);
media.lk.forEach((im, i) => ok(im.w > 0, `⑫ P22 logo ${i + 1} 未解码（${im.src}）`));
{
  const lt = media.lk[0], dk = media.lk[1];
  ok(/openai-agora-light\.png$/.test(lt.src || ''), `⑫ P22 浅色源不符 ${lt.src}`);
  ok(/openai-agora\.webp$/.test(dk.src || ''), `⑫ P22 深色源不符 ${dk.src}`);
  ok(THEME === 'dark' ? (!lt.shown && dk.shown) : (lt.shown && !dk.shown),
     `⑫ P22 logo 双主题显隐反了（theme=${THEME} lt=${lt.shown} dk=${dk.shown}）`);
}

// ⑬ Call Agent 章（2026-08-21 新增三页）内容闸 + 红线反向闸
//    正向：三页各自的关键口径一个都不能掉；96.5% 与「32,000」必须同页出现
//    （盲测口径与 convoai-info P5 的 2,475 通生产口径是两个不同数据集，
//     只写 96.5% 不写 32,000 就等于把两个数据集混成一个）。
//    反向：价格数字（¥8,500 / ¥2,999 / ¥5,501）与 staging URL 全 deck 不许出现 ——
//    商务数字易变、staging 是内部地址，两者上页都是事故。
const [ca16, ca17, ca18] = await Promise.all([16, 17, 18].map(pageText));
[['96.5%', ca16, 'P16'], ['32,000', ca16, 'P16'], ['1,000+', ca16, 'P16'],
 ['句句过审', ca16, 'P16'], ['把线索聊成订单', ca16, 'P16'], ['1/3', ca16, 'P16'],
 ['盲测', ca16, 'P16'], ['第 10,000 通依旧满格', ca16, 'P16'],
 ['五个大脑', ca17, 'P17'], ['动态话术策略选择', ca17, 'P17'],
 ['选择性注意力锁定', ca17, 'P17'], ['真实意图识别', ca17, 'P17'],
 ['情绪感知和生成', ca17, 'P17'], ['大模型流式语音识别', ca17, 'P17'],
 ['0.8 秒', ca17, 'P17'], ['见 P8', ca17, 'P17'], ['Agent Harness', ca17, 'P17'],
 ['快一千倍', ca18, 'P18'], ['留资率提升 12%', ca18, 'P18'], ['2 倍', ca18, 'P18'],
 ['定向微调', ca18, 'P18'], ['DAY 15', ca18, 'P18'], ['DAY 30', ca18, 'P18'],
 ['复盘', ca18, 'P18'], ['迭代', ca18, 'P18'],
].forEach(([needle, txt, tag]) => ok(txt.includes(needle), `⑬ ${tag} 缺「${needle}」`));
ok(/SOURCE · 声网 CALL AGENT 官网 · 外呼智能体 · 事实截止 2026\.08/.test(ca16),
   '⑬ P16 缺 Call Agent SOURCE 行');
ok(/SOURCE · 声网 CALL AGENT 官网 · 外呼智能体 · 事实截止 2026\.08/.test(ca18),
   '⑬ P18 缺 Call Agent SOURCE 行');
['¥2,999', '¥8,500', '¥5,501', 'staging'].forEach(nd =>
  ok(!all.includes(nd), `⑬ Call Agent 红线：全 deck 出现「${nd}」`));
// ⑬ 章序闸：场景（P15）→ Call Agent（16–18）→ R1（P19），Colin 的排序指令钉在这里
const p15 = await pageText(15);
ok(p15.includes('一套引擎'), '⑬ P15 不是「典型场景」页 —— 章序被改动了？');
ok(p19.includes('R1-4G'), '⑬ P19 不是「R1 开发套件」页 —— 章序被改动了？');

// ⑭ P20 视频页闸（robot26 #24 同款机制，逐条对上；这些坑 robot26 都踩过一遍）
//    静置态必须是干净画面：**没有 controls 属性**（Blink 控制条在 .deck-stage 的
//    transform:scale(≠1) 下按未缩放坐标系渲染，条宽与位置全错 —— Colin 截图实锤）。
const vid = await pg.evaluate((vp) => {
  // 先把视频页摆成**现场静置态**（active + visible + step 0）再量 ——
  // .slide 的 visibility 由 .visible 控制，只 toggle .active 量到的会是 hidden（假阴性）。
  document.querySelectorAll('.slide').forEach((el, k) => {
    el.classList.toggle('active', k === vp - 1); el.classList.toggle('visible', k === vp - 1);
    el.querySelectorAll('[data-step]').forEach(x => x.classList.remove('on'));
  });
  const sec = document.querySelector(`.slide[data-p="${vp}"]`);
  const box = sec && sec.querySelector('.sh.vid');
  const v = sec && sec.querySelector('video');
  if (!sec || !box || !v) return null;
  const bs = getComputedStyle(box), vs = getComputedStyle(v);
  const br = box.getBoundingClientRect();
  return {
    src: v.getAttribute('src'), poster: v.getAttribute('poster'),
    ctl: v.hasAttribute('controls'),
    muted: v.hasAttribute('muted'), inline: v.hasAttribute('playsinline'),
    preload: v.getAttribute('preload'), playStep: v.dataset.playStep,
    bx: Math.round(br.left), by: Math.round(br.top),
    bw: Math.round(br.width), bh: Math.round(br.height),
    bl: bs.left, bt: bs.top, ov: bs.overflow,
    boxOpacity: bs.opacity, boxVis: bs.visibility, boxDisplay: bs.display, vOpacity: vs.opacity,
    boxStep: box.getAttribute('data-step'),
    cueStep: (sec.querySelector('.vid-cue') || {}).dataset?.step,
    cueBox: (() => { const c = sec.querySelector('.vid-cue'); if (!c) return null;
      const r = c.getBoundingClientRect(); return `${Math.round(r.width)}x${Math.round(r.height)}`; })(),
    vw: vs.width, vh: vs.height, fit: vs.objectFit, bg: vs.backgroundColor,
    others: sec.querySelectorAll('.pp > .sh').length,
    // 2026-08-23 采纳项 E ②：静态角标 kicker（.sh.kk.vid-kick）
    kick: (() => {
      const k = sec.querySelector('.sh.vid-kick');
      if (!k) return null;
      const ks = getComputedStyle(k), kr = k.getBoundingClientRect();
      return {
        txt: (k.textContent || '').trim(), col: ks.color, cls: k.getAttribute('class'),
        step: k.getAttribute('data-step'),
        mo: [...k.classList].some(c => c.startsWith('mo-')) ||
            !!k.querySelector('[class*="mo-"]'),
        anim: ks.animationName,
        l: Math.round(kr.left), t: Math.round(kr.top),
        r: Math.round(kr.right), b: Math.round(kr.bottom),
        vis: ks.visibility, op: ks.opacity, display: ks.display,
      };
    })(),
    sig: (() => { const s = sec.querySelector('.sig'); if (!s) return null;
      const sr = s.getBoundingClientRect();
      return { l: Math.round(sr.left), r: Math.round(sr.right),
               t: Math.round(sr.top), b: Math.round(sr.bottom), col: getComputedStyle(s).color }; })(),
  };
}, VIDEO_PAGE);
ok(!!vid, `⑭ P${VIDEO_PAGE} 缺 .sh.vid / video`);
if (vid) {
  ok(vid.src === '/decks/assets/robot26/demo.mp4', `⑭ 视频 src 不是 robot26 跨引用：${vid.src}`);
  ok(vid.poster === '/decks/assets/robot26/demo-poster.jpg', `⑭ poster 不符：${vid.poster}`);
  ok(!vid.ctl, '⑭ 静置态带 controls —— transform 缩放下控制条会错位（robot26 实锤）');
  ok(vid.muted, '⑭ video 缺 muted —— 不静音浏览器直接拒绝自动播放');
  ok(vid.inline, '⑭ video 缺 playsinline');
  // 2026-08-23 采纳项 E ①：preload none → metadata。none 的代价是首帧要等一轮网络往返
  // （元数据都没有），metadata 只拉头部几十 KB、不是那 3.1MB，换来「翻到即可播」。
  ok(vid.preload === 'metadata',
     `⑭ preload 应为 metadata（首帧即备，只拉头部不拉 3MB 全片），实测 ${vid.preload}`);
  ok(vid.playStep === '1', `⑭ data-play-step 应为 1，实测 ${vid.playStep}`);
  // ⑭ 静态角标 kicker（采纳项 E ②）：在位 / 逐字 / 反白 / **静态**（不挂 data-step、
  //    不挂 mo-* 原语、computed animation-name 为 none）/ 落在左上角不挡画面主体，
  //    且与右上角的页码 sig 不打架、与底部 hover 控制条不打架。
  ok(!!vid.kick, '⑭ P20 缺静态角标 kicker（.sh.vid-kick）');
  if (vid.kick) {
    const K = vid.kick;
    ok(K.txt === 'PHYSICAL AI · FROM ENGINE TO DEVICE', `⑭ 角标文案漂移：「${K.txt}」`);
    ok(/\bkk\b/.test(K.cls), `⑭ 角标未走家族 kicker 样式（class=${K.cls}）`);
    ok(/rgba\(255,\s*255,\s*255/.test(K.col), `⑭ 角标不是反白（color=${K.col}）`);
    ok(K.step === null, '⑭ 角标挂上了 data-step —— 它是静态文字件，进步进就会闪');
    ok(!K.mo, '⑭ 角标挂上了 mo-* 原语 —— 它不进运动件名册');
    ok(K.anim === 'none', `⑭ 角标带了 animation（${K.anim}）—— 静态件不许动`);
    ok(K.vis === 'visible' && K.display !== 'none' && +K.op > 0.5,
       `⑭ 角标静置态不可见（vis=${K.vis} display=${K.display} opacity=${K.op}）`);
    // 左上角：整体落在画面左半 × 上 1/6，不压中下部的主体，也不进底部控制条带（y≥980）
    ok(K.r < 960 && K.b < 180, `⑭ 角标不在左上角（右缘 ${K.r} / 下缘 ${K.b}）—— 会挡画面主体`);
    ok(K.b < 980, `⑭ 角标下缘 ${K.b} 掉进底部 hover 控制条带`);
    if (vid.sig) ok(K.r < vid.sig.l - 20,
      `⑭ 角标右缘 ${K.r} 逼近页码 sig 左缘 ${vid.sig.l} —— 两枚小字会撞`);
  }
  // ⑭ 空页回归闸（2026-08-21 Colin：「P19 之后多了一个空页面」）：
  //    motion.css 末尾那条兜底规则会把 step0 的「裸容器」摁成 opacity:0 ——
  //    满幅视频盒一旦挂上 data-step，整幅 poster 连同页面一起消失。这两条钉死它。
  ok(!vid.boxStep, '⑭ .sh.vid 又挂上了 data-step —— 这就是「空页」的根因（step0 会被摁成 opacity:0）');
  ok(vid.cueStep === '1', `⑭ 缺零尺寸分步 cue（[data-step="1"]，deck.js 的 maxStep 只认它），实测 ${vid.cueStep}`);
  ok(vid.cueBox === '0x0', `⑭ 分步 cue 不是零尺寸（会在页面上留一块），实测 ${vid.cueBox}`);
  ok(vid.boxOpacity === '1' && vid.boxVis === 'visible' && vid.boxDisplay !== 'none',
     `⑭ 静置态容器不可见（opacity=${vid.boxOpacity} visibility=${vid.boxVis}）—— 空页回归`);
  ok(vid.vOpacity === '1', `⑭ 静置态 video 不可见（opacity=${vid.vOpacity}）`);
  ok(vid.bl === '0px' && vid.bt === '0px', `⑭ 容器未贴 0,0（${vid.bl},${vid.bt}）`);
  ok(vid.bw === 1920 && vid.bh === 1080, `⑭ 容器不是满幅 1920×1080（${vid.bw}×${vid.bh}）`);
  ok(vid.bx === 0 && vid.by === 0, `⑭ 容器左上角不在舞台原点（${vid.bx},${vid.by}）`);
  ok(vid.ov === 'hidden', `⑭ 容器 overflow 应为 hidden，实测 ${vid.ov}`);
  ok(vid.vw === '1920px' && vid.vh === '1080px', `⑭ video 计算尺寸 ${vid.vw}×${vid.vh} != 1920×1080`);
  ok(vid.fit === 'cover', `⑭ video object-fit 应为 cover，实测 ${vid.fit}`);
  ok(/rgb\(0, 0, 0\)/.test(vid.bg), `⑭ video 底色应为 #000（poster 解码前别闪白），实测 ${vid.bg}`);
  // 2026-08-23：视频盒 + 静态角标 = 2 只 .sh（采纳项 E ② 之前是 1 只）。
  // 这条闸的意思一直是「别往纯片子页上堆件」，数字跟着规格走，上限就是这两只。
  ok(vid.others === 2, `⑭ 纯片子页只该有两只 .sh（视频盒 + 静态角标），实测 ${vid.others}`);
}
// ⑭ poster 自证：文件真的 200、真的解出像素、而且画面里**有东西**（不是一片纯色）。
//    「翻到 P20 只看见一张白纸」这种事必须在 CI 里被抓住，不能靠人眼。
{
  const res = await fetch(BASE + '/decks/assets/robot26/demo-poster.jpg');
  ok(res.status === 200, `⑭ poster HTTP ${res.status}`);
  const st = await pg.evaluate(async (src) => {
    const img = new Image(); img.src = src;
    try { await img.decode(); } catch (e) { return { err: String(e) }; }
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0);
    const d = x.getImageData(0, 0, c.width, c.height).data;
    let n = 0, s = 0, s2 = 0, mx = 0;
    for (let i = 0; i < d.length; i += 4) {
      const l = .299 * d[i] + .587 * d[i + 1] + .114 * d[i + 2];
      n++; s += l; s2 += l * l; if (l > mx) mx = l;
    }
    const m = s / n;
    return { w: img.naturalWidth, h: img.naturalHeight, mean: +m.toFixed(2),
             sd: +Math.sqrt(Math.max(0, s2 / n - m * m)).toFixed(2), max: Math.round(mx) };
  }, '/decks/assets/robot26/demo-poster.jpg');
  ok(!st.err, `⑭ poster 解码失败：${st.err}`);
  ok(st.w === 1600 && st.h === 900, `⑭ poster 尺寸 ${st.w}×${st.h} != 1600×900`);
  ok(st.sd > 4 && st.max > 60, `⑭ poster 是一片纯色（sd=${st.sd} max=${st.max}）—— 页面等于空的`);
}
// ⑭ 整页非空 + 电影感黑底恒定：静置态（step 0）整幅截图必须是那支夜景片子，不是主题底板。
//    浅色空页回归时整页平均亮度 239（实测），这一条当场抓住。
//    2026-08-23 采纳项 E ③：**浅色主题下本页照样是黑底全幅**（有意为之，不是 bug）——
//    本脚本双主题各跑一次，这一条在 THEME=light 那一跑里就是「底色恒暗」的断言。
{
  await pg.evaluate((vp) => {
    document.querySelectorAll('.slide').forEach((el, k) => {
      el.classList.toggle('active', k === vp - 1); el.classList.toggle('visible', k === vp - 1);
      el.querySelectorAll('[data-step]').forEach(x => x.classList.remove('on'));   // 回到 step 0
    });
  }, VIDEO_PAGE);
  await pg.waitForTimeout(300);
  const b64 = (await pg.screenshot({ clip: { x: 0, y: 0, width: 1920, height: 1080 } })).toString('base64');
  const st = await pg.evaluate(async (s) => {
    const img = new Image(); img.src = 'data:image/png;base64,' + s; await img.decode();
    const c = document.createElement('canvas'); c.width = 480; c.height = 270;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0, 480, 270);
    const d = x.getImageData(0, 0, 480, 270).data;
    let n = 0, s1 = 0, s2 = 0;
    for (let i = 0; i < d.length; i += 4) {
      const l = .299 * d[i] + .587 * d[i + 1] + .114 * d[i + 2]; n++; s1 += l; s2 += l * l;
    }
    const m = s1 / n;
    return { mean: +m.toFixed(2), sd: +Math.sqrt(Math.max(0, s2 / n - m * m)).toFixed(2) };
  }, b64);
  ok(st.mean < 60, `⑭ P${VIDEO_PAGE} 静置态整页平均亮度 ${st.mean} —— 片子没盖住页面（空页回归）`);
  ok(st.sd > 2, `⑭ P${VIDEO_PAGE} 静置态整页是一片纯色（sd=${st.sd}）`);
}
// ⑭ 悬停呼出：mouseenter 挂 controls、mouseleave 收回（排练手控的唯一入口）
{
  await pg.evaluate((vp) => {
    document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === vp - 1));
  }, VIDEO_PAGE);
  const el = await pg.$(`.slide[data-p="${VIDEO_PAGE}"] video`);
  await el.dispatchEvent('mouseenter');
  const on = await pg.evaluate((vp) => document.querySelector(`.slide[data-p="${vp}"] video`).hasAttribute('controls'), VIDEO_PAGE);
  await el.dispatchEvent('mouseleave');
  const off = await pg.evaluate((vp) => document.querySelector(`.slide[data-p="${vp}"] video`).hasAttribute('controls'), VIDEO_PAGE);
  ok(on, '⑭ mouseenter 未呼出 controls（排练时没法手控）');
  ok(!off, '⑭ mouseleave 未收回 controls');
}
// ⑭ 播放挂钩：翻到该页且分步就位 ⇒ 脚本应当尝试 play()（本容器无 H.264，
//    play() 必然 reject —— 所以验的是「有没有发起」而不是「有没有播成」：
//    用 v.play 被调用过来判定，避免把环境缺编解码器算成页面的错。
{
  const fired = await pg.evaluate((vp) => new Promise((res) => {
    const v = document.querySelector(`.slide[data-p="${vp}"] video`);
    let called = false;
    const orig = v.play.bind(v);
    v.play = () => { called = true; return orig().catch(() => {}); };
    document.querySelectorAll('.slide').forEach((el, k) => {
      el.classList.toggle('active', k === vp - 1);
    });
    // 分步 cue 现在是 video 的兄弟（不再是祖先）—— 页内按 data-play-step 找那一枚
    v.closest('.slide').querySelector(`[data-step="${+v.dataset.playStep || 1}"]`).classList.add('on');
    requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(() => res(called), 120)));
  }), VIDEO_PAGE);
  ok(fired, '⑭ 翻到视频页 + 分步就位后没有发起 play()（播放挂钩没接上）');
  const paused = await pg.evaluate((vp) => new Promise((res) => {
    const v = document.querySelector(`.slide[data-p="${vp}"] video`);
    document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === 0));
    requestAnimationFrame(() => requestAnimationFrame(() => setTimeout(() => res(v.paused && v.currentTime === 0), 120)));
  }), VIDEO_PAGE);
  ok(paused, '⑭ 离开视频页后没有 pause + 归零');
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
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 分步 P6/P7/P14/P20 各 1 步 · P21 口径已锁 · P8 大图闸 · P19 实拍图 + P22 双源 logo 闸 · Call Agent 三页闸 · P20 视频页闸 · deckSwap 常显`);
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

