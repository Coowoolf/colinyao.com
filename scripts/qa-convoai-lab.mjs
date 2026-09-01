// QA · convoai-lab · LAB 家族旗舰（22 页 · 双主题 · P6/P7/P14/P20 各 1 步 build
//      + **十六枚 WebGL 语义场景**（全量 3D 化 · 第一波七枚 + 第二波九枚）：
//        P1 声场球 / P2 决策轨道环 / P3 双工三通道 / P4 双向声带 / P6 语音链路 /
//        P7 声学地形 / P8 打断时序 / P9 双层防御壳 / P10 产品大图分层 / P11 弱网 QoS /
//        P12 视觉视锥 / P13 编排插槽 / P14 三塔握手 / P17 五脑区大脑 / P18 复利螺旋 /
//        P21 SD-RTN 地球；P5/P15/P16/P19/P20/P22 逐页语义审查判定保持 2D）
// 从 qa-convoai-engine.mjs **整体克隆**：22 页断言 / 章序闸 / 口径锁（P21 文案逐字）/
//   Call Agent 三页闸与反向闸 / 视频页闸 / deckSwap / noindex / a[href]=0 / 红线全套
//   一条不减 —— 全量 3D 化没有改正文，所以引擎的每一道闸都必须照样绿。
// 去掉：**双生闸**（lab 是单产物，/convoai 与 /convoai-engine 那一对归引擎 builder）。
// 新增 ⑲ **WebGL 豁免通道**（LAB 家族铁律的机器自证）：
//   a  逐页舞台结构：场景名 / data-lab-rect / poster 层 / 打印帧位 / 层序 /
//      poster 组里**一个字也没有**（字必须压在 canvas 之上）
//   a2 **单渲染器巡游**：全文档 WebGL canvas 恰 1 枚 + 车库在位 +
//      场景 registry 页码表 == {1,4,7,9,17,18,21}
//   b  逐页起帧 + **逐页对位**（canvas 的舞台坐标矩形 ≈ 该页 data-lab-rect，±1.2px）
//      + 绘制缓冲区跟着矩形走 + poster 淡出到 0 / canvas 淡入到 1 + DPR ≤ 2
//   c  **禁用 WebGL 启动 ⇒ 整 deck 22 页照常可读**（七页显各自的 SVG，正文一字不少）
//   d  prefers-reduced-motion ⇒ 渲一帧停帧（mode=STILL / run=0）
//   e  非激活页 ⇒ canvas 回车库、rAF 停、gl-up 全摘、poster 交还
//   f  DPR ≤ 2（deviceScaleFactor=3 的上下文里照样 ≤2）
//   g  @media print ⇒ canvas 藏 / **所有** poster 显；beforeprint 抓到的打印帧非空
//   h  data-* 暴露的周期 / 相位 / 关键几何静态复算：弧相位永不齐步、五区周期互异、
//      P18 站点 x / P7 事件 x 与阈值 / P9 两层半径 / P4 截断 x 全部与页上一致
//   i  FPS 自动降级：默认 URL（软渲染 <20fps）2s 内退 poster；?lab=hold 则保持 LIVE
//   j  双主题 × 逐 3D 页 WebGL 静置帧（各裁自己的图形区）+ 材质 token 真的分叉
//   k  **翻页热切换**：P17 → P18 ⇒ 当前景换人 + 前一景确实走了 leave + gl-up 跟着搬家
// 2026-09-01 二轮精修 · 波A（四页换血 + lab-kit ⑨ audioStream）新增：
//   as 包络平滑度用**收敛阶**判据（步长减半：C² 掉 4×、折角只掉 2×），
//      并**带反证** —— 旧的逐柱采样包络必须过不了这一闸，否则闸是空的
//   s  全局流速复算：A 档 8 页 30 股全部落在 110 ±30%，且任一页内极差 ≤ 1.35×
//   P6  符号行四段三处接缝严丝合缝 + 主路横贯全链 + token 高密度脉冲串
//   P8  让位窗口 = 页上「收声」那段相位括号（840→1040，200px）+ 剖面 1→0
//   P14 光束三段有序 / 等速 / 停驻窗口里三段常亮 / 收尾是「把光抽回去」
//   P18 舞台横跨两图 + 左移 80 + mkRelock 的机器证明（屏点偏差 0）+ 两图墨迹间距 ≥200px
// 用法：node scripts/qa-convoai-lab.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8777 node scripts/qa-convoai-lab.mjs   （换端口）
//
// ── 下面是从引擎母本继承的全部沿革注释（闸门为什么长这样，都在这儿）──
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
// 2026-08-23 三数章重构（页数不变 22 · 只在 6–10 区间轮转）：原 8 大图 → 10 ／ 原 9 打断 → 8 ／
//   原 10 SAL → 9；P11 起全部原位不动，分步 [6,7,14,20]、口径锁 21、title 板 {1,22} 一概不受影响。
//   随之：⑩ 大图闸 8 → 10 并新增 P8 打断页内容闸、⑯ SOURCE 名册 8 → 10、⑰ kicker 消歧 8 → 10、
//   ⑪ SAL 闸 10 → 9、⑬ 补三数章序闸；新增 ⑱「kicker 绑数字 + P5/P10 章内导航」两组闸。
//   同轮 ① title 改「深入讲解」（封面定位随 Colin 主标一起换）。
import { chromium } from 'playwright-core';
import { mkdirSync } from 'node:fs';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const N = 22;
const DECK = '/decks/convoai-lab.html';
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
// 软渲染开关：容器里没有 GPU，不给这三个 flag 连 WebGL 上下文都拿不到
const GL_ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
// ── LAB 场景表（第一波全量 3D 化 · 七枚场景）───────────────────────────────
//   页码表 = 单渲染器巡游的 registry；qa 与产物两头对表，加错页 / 漏页当场炸。
const LAB_SCENES = { 1: 'voice', 2: 'ring', 3: 'lanes', 4: 'duplex', 6: 'chain',
                     7: 'terrain', 8: 'cutin', 9: 'shell', 10: 'bigmap', 11: 'qos',
                     12: 'vision', 13: 'slots', 14: 'towers',
                     17: 'brain', 18: 'spiral', 21: 'globe' };
// poster 就是页上那张 SVG 的十四页（P1/P21 走构建期离线投影出来的专用 poster）
const INPAGE = Object.keys(LAB_SCENES).map(Number).filter(p => p !== 1 && p !== 21);
// 保持 2D 的六页：数字卡 / 成绩单 / 实拍 / 视频 / 末页 —— 故意不在表里，不是漏了
const FLAT_PAGES = [5, 15, 16, 19, 20, 22];
const LAB_PAGES = Object.keys(LAB_SCENES).map(Number).sort((a, b) => a - b);
// LAB 的 WebGL 页：主跑一律带 ?lab=hold（容器软渲染只有个位数 fps，
// 不关掉自动降级的话主跑全程都是 poster，⑲b 那条就验不到「起来了」）。
// 自动降级本身在 ⑲i 用**不带** hold 的 URL 单独验 —— 两条互为对照。
const HOLD = '?lab=hold';
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
const b = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
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
await pg.goto(BASE + DECK + HOLD + '#1', { waitUntil: 'load' });
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
ok(meta.title === '声网 · 对话式 AI 引擎 · 深入讲解 · LAB', `① title 漂移「${meta.title}」`);

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
// 2026-08-23 三数章重构：大图从 P8 挪到 P10（章尾收束），打断从 P9 提到 P8（拆 340 的正文）。
//   下面的页号全部按新序重映射；页内关键词一个字都没动 —— 挪的是位置，不是内容。
const [p3, p4, p7, p8, p10] = await Promise.all(
  [3, 4, 7, 8, 10].map(pageText));
[['不能插话', p3, 'P3'], ['选择不插话', p3, 'P3'],
 ['单工', p3, 'P3'], ['半双工', p3, 'P3'], ['全双工', p3, 'P3'],
 ['AEC', p4, 'P4'], ['340ms', p4, 'P4'], ['全双工', p4, 'P4'],
 ['WebRTC VAD', p7, 'P7'], ['语义判停', p7, 'P7'], ['TEN VAD', p7, 'P7'],
 // ── P8 拆 340 · 优雅打断（原 P9）：时间线上的三段相位与两枚事件标一个都不能掉 ──
 ['340ms 即时收声', p8, 'P8'], ['用户插话', p8, 'P8'], ['智能体收声', p8, 'P8'],
 ['侦测', p8, 'P8'], ['收声', p8, 'P8'], ['让位', p8, 'P8'],
 ['误打断防抖', p8, 'P8'], ['对话像真人一样你来我往', p8, 'P8'],
 // ── P10 大图收束（原 P8）：四个可读性锚点 + 底座，一个都不能掉 ──
 ['AEC', p10, 'P10'], ['打断快路径', p10, 'P10'], ['SOS / EOS', p10, 'P10'],
 ['SD-RTN', p10, 'P10'], ['650ms', p10, 'P10'],
 ['AI-VAD', p10, 'P10'], ['不经过 LLM', p10, 'P10'], ['参考信号', p10, 'P10'],
 ['客户业务服务器', p10, 'P10'], ['终端设备', p10, 'P10'], ['声网引擎云', p10, 'P10'],
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
  const SRC_PAGES = [5, 7, 10, 11, 16, 17, 18, 19, 21];  // 引擎 deck 的九张数据页（大图 8 → 10）
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

// ⑰ kicker 消歧闸（2026-08-23 采纳项 F）：P10 = 引擎内部链路 / P14 = 客户接入架构，
//    两页 kicker 各自带上限定词，翻页时不会读成同一张图的两个版本。
// ⑱ 三数章绑定闸（2026-08-23 三数章重构）：展开页的 kicker 必须以「EXTREME nn · 数字」起手，
//    读者在任何一页都知道「我现在拆的是 P5 亮出的哪一个数」。页序一动这一闸当场报出来。
{
  const kick = async (p) => pg.evaluate((k) =>
    (document.querySelector(`.slide[data-p="${k}"] .kk`) || {}).textContent?.trim() || '', p);
  const [k6, k7, k8, k9, k10, k14] = await Promise.all([6, 7, 8, 9, 10, 14].map(kick));
  ok(/ENGINE INTERNALS/.test(k10) && /运行时内部链路/.test(k10), `⑰ P10 kicker 缺内部链路限定词：「${k10}」`);
  ok(/INTEGRATION/.test(k14) && /客户接入架构/.test(k14), `⑰ P14 kicker 缺客户接入限定词：「${k14}」`);
  ok(k10 !== k14, '⑰ P10 / P14 kicker 撞车');
  [[6, k6, 'EXTREME 01 · 650MS · PIPELINE'],
   [7, k7, 'EXTREME 02 · 340MS · 前提 · VOICE ACTIVITY DETECTION'],
   [8, k8, 'EXTREME 02 · 340MS · INTERRUPTION'],
   [9, k9, 'EXTREME 03 · 95% · SELECTIVE ATTENTION'],
  ].forEach(([p, k, pre]) => ok(k.startsWith(pre), `⑱ P${p} kicker 未绑数字：「${k}」`));
  // 大图页收的是三个数的总账，**不绑单个数字** —— 绑了反而把「收束」读成「第四个数」
  ok(!/^EXTREME/.test(k10), `⑱ P10 大图页不该绑单个数字：「${k10}」`);
}

// ⑱ 三数章导航闸：P5 三张卡各带一枚章内指针 + 一句导航 land；P10 大图钉三枚数字锚点 + 收束句。
{
  const p5nav = await pg.evaluate(() => {
    const s = document.querySelector('.slide[data-p="5"]');
    return {
      ptrs: [...s.querySelectorAll('.card-c')].map(c => {
        const d = [...c.children].find(x => getComputedStyle(x).position === 'absolute');
        return d ? d.textContent.trim() : null;
      }),
      land: (s.querySelector('.land') || {}).textContent?.replace(/\s+/g, '') || '',
    };
  });
  ok(p5nav.ptrs.join('|') === '↓ P6|↓ P7–8|↓ P9',
     `⑱ P5 章内指针漂移：[${p5nav.ptrs.join(' / ')}]`);
  ok(p5nav.land.includes('逐页拆开') && p5nav.land.includes('一张图'),
     `⑱ P5 缺章内导航 land：「${p5nav.land}」`);
  const p10txt = await pageText(10);
  ['650MS', '340MS', '95%'].forEach(a =>
    ok(p10txt.includes(a), `⑱ P10 缺数字锚点 chip「${a}」`));
  ok(p10txt.includes('三件极致，都在这张图上'), '⑱ P10 缺章尾收束句');
}
// ⑩ P6：数字人已移出串行主链（标题也从「端到端链路」改成「实时语音链路」）
const p6 = await pageText(6);
ok(p6.includes('一条深度优化的实时语音链路'), '⑩ P6 标题未改成「实时语音链路」');
ok(p6.includes('数字人 · 可选'), '⑩ P6 缺「数字人 · 可选」虚线支路');
// ⑩ P22 末页：从被删的原 P20 收尾页继承来的 CTA 行（真实入口不许随页消失）
const p22 = await pageText(22);
ok(p22.includes('agora.io › 对话式 AI 引擎'), '⑩ P22 缺 CTA 行（原 P20 收尾页继承）');

// ⑪ 2026-08-21 两轮（大内容轮 + 收束轮）的内容闸
const [p9, p12, p19, p13] = await Promise.all(
  [9, 12, 19, 13].map(pageText));    // p10 / p11 / p22 上面已取过，复用
                                     // 页号位移：R1 = 今 P19（原 13）、编排 = 今 P13（原 14）、
                                     //          SAL = 今 P9（原 10 · 2026-08-23 三数章重构）
[// P9 · 拆 95% · 三种噪声 · 三层方案（噪声名 + 方案名一个都不能掉，land 是 Colin aiot26 定稿）
 ['稳态', p9, 'P9'], ['瞬态', p9, 'P9'], ['非对话人', p9, 'P9'],
 ['传统降噪', p9, 'P9'], ['AI 降噪', p9, 'P9'], ['SAL', p9, 'P9'],
 ['屏蔽 95% 干扰', p9, 'P9'],
 ['前两类是信号问题', p9, 'P9'],
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
// ⑬ 三数章序闸（2026-08-23）：P5 亮三个数 → P6 拆 650 → P7 拆 340 前提 → P8 拆 340 →
//    P9 拆 95% → P10 大图收束。这一闸按**页内正文的身份关键词**认页（不是认 kicker），
//    与 ⑱ 的 kicker 绑定闸互为独立证据：两条一起绿，才叫「页真的搬对了」。
{
  // p5 / p6 / p7 / p8 / p9 / p10 上面都已取过，直接复用（别重取，也别在块里遮蔽同名量）
  [[5, p5, '把三件事'], [5, p5, '端到端响应延时'], [5, p5, '极速打断响应'], [5, p5, '环境干扰屏蔽'],
   [6, p6, '一条深度优化的实时语音链路'], [7, p7, '让机器知道'],
   [8, p8, '想插话就插话'], [9, p9, '只听该听的人'], [10, p10, '看懂全双工引擎'],
  ].forEach(([p, txt, kw]) => ok(txt.includes(kw), `⑬ 三数章序漂移：P${p} 缺「${kw}」`));
  // 反向：大图的身份关键词绝不许再出现在 P8（它已经搬走了）
  ok(!p8.includes('看懂全双工引擎'), '⑬ P8 仍是大图页 —— 三数章重排没生效');
}

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


// ⑲ WebGL 豁免通道 · 主跑内联段
//    （a 结构 / a2 单渲染器巡游 / b 起帧 + 对位 / c poster 交接 / e 非激活停 rAF /
//      k 翻页热切换 / h 相位表静态复算）
//    这一段跑在主浏览器里（带 --use-angle=swiftshader），URL 带 ?lab=hold。
//    单独开上下文才验得了的五条（禁 WebGL / reduced-motion / print / DPR / 自动降级）
//    在文件末尾的「⑲ 独立上下文段」。
{
  // ── a 结构：3D 舞台只出现在场景页；**全文档恰好一枚 canvas**（单渲染器巡游）──
  const struct = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map((s, i) => {
    const st = s.querySelector('.lab-stage');
    return {
      p: i + 1,
      stage: s.querySelectorAll('.lab-stage').length,
      scene: st ? st.dataset.labScene : null,
      rect: st ? st.dataset.labRect : null,
      ready: st ? st.dataset.labReady : null,
      print: s.querySelectorAll('.lab-print').length,
      poster: s.querySelectorAll('.lab-poster').length,
      posterInPP: s.querySelectorAll('.pp .lab-poster').length,
      posterText: [...s.querySelectorAll('.lab-poster')]
        .reduce((n, g) => n + g.querySelectorAll('text').length, 0),
      inPP: !!s.querySelector('.pp .lab-stage'),
      order: [...s.children].map(el => (el.className || '').split(' ')[0]).join('>'),
    };
  }));
  struct.forEach((v) => {
    const want = LAB_SCENES[v.p] || null;
    ok(v.scene === want, `⑲a P${v.p} 3D 舞台种类 ${v.scene} != ${want}`);
    ok(v.stage === (want ? 1 : 0), `⑲a P${v.p} .lab-stage 数 ${v.stage}`);
    if (!want) {
      ok(v.poster === 0, `⑲a P${v.p} 无场景却挂了 poster 层`);
      return;
    }
    ok(v.poster >= 1, `⑲a P${v.p} 缺 poster 降级层`);
    ok(v.print === 1, `⑲a P${v.p} 缺打印帧位 .lab-print`);
    // 层序：背景板 → 3D 舞台 → .pp 正文。舞台掉进 .pp 里就会被入场系的 opacity 连坐。
    ok(!v.inPP, `⑲a P${v.p} 3D 舞台落在 .pp 里了 —— 必须是 .pp 的兄弟`);
    ok(v.order === 'conf-bg>lab-stage>pp', `⑲a P${v.p} 层序漂移：${v.order}`);
    ok(/^\d+,\d+,\d+,\d+$/.test(v.rect || ''), `⑲a P${v.p} 图形区矩形声明缺失：${v.rect}`);
    ok(v.ready === '1', `⑲a P${v.p} 场景没建起来（data-lab-ready=${v.ready}）`);
    // poster 组里一个字也不许有：字要压在 canvas 之上，任何降级路径下都在位
    ok(v.posterText === 0, `⑲a P${v.p} poster 层里裹进了 ${v.posterText} 个文字件`);
    // 十四页的 poster = 页上原来那张 SVG（在 .pp 里）；P1/P21 是专用 poster（在舞台里）
    if (INPAGE.includes(v.p))
      ok(v.posterInPP >= 1, `⑲a P${v.p} 的图形没有原地留作 poster 层`);
  });

  // ── a2 单渲染器巡游的硬红线 ──────────────────────────────────────────
  {
    const one = await pg.evaluate(() => {
      const all = [...document.querySelectorAll('canvas')];
      return {
        n: all.length,
        id: all[0] && all[0].id,
        garage: document.querySelectorAll('.lab-garage').length,
        scenes: document.documentElement.dataset.labScenes,
        ready: window.__labReady,
        ctxOK: (() => { try { const c = all[0];
          return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } })(),
      };
    });
    ok(one.n === 1, `⑲a2 全文档 WebGL canvas ${one.n} 枚 —— 单渲染器巡游只准 1 枚`);
    ok(one.id === 'labGl', `⑲a2 canvas id 漂移：${one.id}`);
    ok(one.garage === 1, '⑲a2 缺 canvas 车库 .lab-garage');
    ok(one.ctxOK, '⑲a2 那一枚 canvas 拿不到 WebGL 上下文');
    // 场景 registry 页码表：本波七页，一页不多一页不少
    ok(one.scenes === LAB_PAGES.join(','),
       `⑲a2 场景 registry 页码表漂移：${one.scenes} != ${LAB_PAGES.join(',')}`);
    ok(LAB_PAGES.length === 16, `⑲a2 全量 3D 化应为 16 页，实为 ${LAB_PAGES.length}`);
    FLAT_PAGES.forEach(p => ok(!LAB_PAGES.includes(p),
      `⑲a2 P${p} 不该有 3D 场景（数字卡 / 成绩单 / 实拍 / 视频 / 末页，逐页语义审查判定保持 2D）`));
    ok(one.ready === LAB_PAGES.length, `⑲a2 建起来的场景数 ${one.ready} != ${LAB_PAGES.length}`);
  }

  // ── a' 生产页不挂常显探针：默认 URL 下 FPS 探针必须是藏的，?debug=1 才显 ──
  {
    const hidden = await pg.evaluate(() => {
      const p = document.getElementById('labProbe');
      return { has: !!p, disp: p ? getComputedStyle(p).display : null,
               flag: document.documentElement.hasAttribute('data-lab-debug') };
    });
    ok(hidden.has, '⑲a 缺 FPS 探针节点（?debug=1 时要用它）');
    ok(!hidden.flag, '⑲a 默认 URL 却挂上了 data-lab-debug');
    ok(hidden.disp === 'none', `⑲a 生产页挂了常显 FPS 探针（display=${hidden.disp}）`);
    const dbg = await pg.evaluate(async (u) => {
      // 另开一个同源页验 ?debug=1 那一路（不动主跑这一页的状态）
      const w = window.open(u, '_blank');
      await new Promise(r => setTimeout(r, 3200));
      const d = w.document.getElementById('labProbe');
      const out = { disp: getComputedStyle(d).display, txt: (d.textContent || '').trim().length };
      w.close();
      return out;
    }, BASE + DECK + '?debug=1#1');
    ok(dbg.disp === 'flex', `⑲a ?debug=1 没把探针显出来（display=${dbg.disp}）`);
    ok(dbg.txt > 6, `⑲a ?debug=1 探针是空的（${dbg.txt} 字）`);
  }

  // ── b 逐页起帧 + 对位 + poster 交接 ──────────────────────────────────
  //    每一枚场景都要：翻过去 ⇒ canvas 搬进该页舞台、贴住 data-lab-rect、
  //    进 LIVE、poster 淡出到 0、canvas 淡入到 1。
  for (const P of LAB_PAGES) {
    await pg.evaluate(k => window.deck.go(k - 1), P);
    await pg.waitForTimeout(1500);
    const v = await pg.evaluate((k) => {
      const c = document.getElementById('labGl');
      const st = document.querySelector(`.slide[data-p="${k}"] .lab-stage`);
      const r = c.getBoundingClientRect();
      const sc = document.querySelector('.deck-stage').getBoundingClientRect();
      const K = sc.width / 1920;
      return {
        mode: c.dataset.labMode, run: c.dataset.labRun, dpr: +c.dataset.labDpr,
        page: +c.dataset.labPage, scene: c.dataset.labScene,
        inStage: c.parentNode === st, glup: st.classList.contains('gl-up'),
        want: (st.dataset.labRect || '').split(',').map(Number),
        got: [(r.x - sc.x) / K, (r.y - sc.y) / K, r.width / K, r.height / K],
        posterOp: [...document.querySelectorAll(`.slide[data-p="${k}"] .lab-poster`)]
          .map(e => +getComputedStyle(e).opacity),
        canvasOp: +getComputedStyle(c).opacity,
        // 绘制缓冲区尺寸必须跟着矩形走（否则 3D 会被拉伸）
        buf: [c.width, c.height],
      };
    }, P);
    ok(v.mode === 'LIVE', `⑲b P${P} WebGL 未进 LIVE（mode=${v.mode}）`);
    ok(v.run === '1', `⑲b P${P} 渲染循环没跑（run=${v.run}）`);
    ok(v.page === P && v.scene === LAB_SCENES[P],
       `⑲b P${P} 当前景不对：P${v.page}/${v.scene}`);
    ok(v.inStage, `⑲b P${P} canvas 没搬进该页舞台`);
    ok(v.glup, `⑲b P${P} .lab-stage 没挂 gl-up —— poster 不会让位`);
    // 逐页对位：canvas 的舞台坐标矩形必须 ≈ 该页声明的 data-lab-rect（±1px）
    const d = v.want.map((x, i) => Math.abs(x - v.got[i]));
    ok(Math.max(...d) <= 1.2,
       `⑲b P${P} canvas 对位偏了：want=[${v.want}] got=[${v.got.map(x => x.toFixed(1))}]`);
    ok(Math.abs(v.buf[0] / v.dpr - v.want[2]) < 2 && Math.abs(v.buf[1] / v.dpr - v.want[3]) < 2,
       `⑲b P${P} 绘制缓冲区尺寸没跟着矩形走：${v.buf} @dpr ${v.dpr}`);
    ok(v.posterOp.length >= 1 && v.posterOp.every(o => o < 0.02),
       `⑲b P${P} poster 没淡出（opacity=${v.posterOp}）`);
    ok(v.canvasOp === 1, `⑲b P${P} canvas 没淡入（opacity=${v.canvasOp}）`);
    ok(v.dpr <= 2, `⑲f P${P} DPR ${v.dpr} > 2（上限 2 是硬的）`);
  }

  // ── e 非激活页 ⇒ canvas 回车库、rAF 停 ───────────────────────────────
  //    （22 页里没有任何一页在偷偷空转 —— 也没有第二块画布在别处渲）
  // 第二波之后 P2 也是 3D 页了 —— 离场闸必须站在**真正没有场景**的一页上。
  // FLAT_PAGES[0] = P5（三件极致 · 三张数字卡），逐页语义审查判定保持 2D。
  await pg.evaluate(k => window.deck.go(k - 1), FLAT_PAGES[0]);
  await pg.waitForTimeout(700);
  const off = await pg.evaluate(() => {
    const c = document.getElementById('labGl');
    return { run: c.dataset.labRun, mode: c.dataset.labMode, page: c.dataset.labPage,
             parent: c.parentNode.className,
             glup: [...document.querySelectorAll('.lab-stage.gl-up')].length,
             posterBack: [...document.querySelectorAll('.slide[data-p="21"] .lab-poster')]
               .map(e => +getComputedStyle(e).opacity) };
  });
  ok(off.run === '0', `⑲e 站在 P${FLAT_PAGES[0]} 上渲染循环还在跑（run=${off.run}）`);
  ok(off.mode === 'IDLE', `⑲e 站在 P${FLAT_PAGES[0]} 上 mode=${off.mode}（应为 IDLE）`);
  ok(off.parent === 'lab-garage', `⑲e canvas 没回车库（parent=${off.parent}）`);
  ok(off.page === '0', `⑲e 离场后 data-lab-page 没清（=${off.page}）`);
  ok(off.glup === 0, `⑲e 还有 ${off.glup} 枚舞台挂着 gl-up —— 离场必须把 poster 交还回去`);
  ok(off.posterBack.every(o => o > 0.98),
     `⑲e 离场后 P21 的 poster 没回到常驻态（opacity=${off.posterBack}）`);

  // ── k 翻页热切换：P17 → P18 ⇒ 当前景换人 + 前一景确实走了 leave ────────
  {
    await pg.evaluate(() => window.deck.go(16));   // P17
    await pg.waitForTimeout(1400);
    const a = await pg.evaluate(() => ({ ...window.__labTour,
      leaves: { ...window.__labTour.leaves },
      cvsPage: +document.getElementById('labGl').dataset.labPage }));
    await pg.evaluate(() => window.deck.go(17));   // P18
    await pg.waitForTimeout(1400);
    const b2 = await pg.evaluate(() => ({ ...window.__labTour,
      leaves: { ...window.__labTour.leaves },
      cvsPage: +document.getElementById('labGl').dataset.labPage,
      p17glup: document.querySelector('.slide[data-p="17"] .lab-stage').classList.contains('gl-up'),
      p18glup: document.querySelector('.slide[data-p="18"] .lab-stage').classList.contains('gl-up'),
      p17poster: [...document.querySelectorAll('.slide[data-p="17"] .lab-poster')]
        .map(e => +getComputedStyle(e).opacity) }));
    ok(a.scene === 'brain' && a.cvsPage === 17, `⑲k P17 当前景不是 brain：${a.scene}/${a.cvsPage}`);
    ok(b2.scene === 'spiral' && b2.cvsPage === 18, `⑲k P18 当前景没换成 spiral：${b2.scene}/${b2.cvsPage}`);
    ok(b2.mounts === a.mounts + 1, `⑲k 场景热切换没发生（mounts ${a.mounts}→${b2.mounts}）`);
    ok((b2.leaves[17] || 0) === (a.leaves[17] || 0) + 1,
       `⑲k 前一景没走 leave（P17 leaves ${a.leaves[17] || 0}→${b2.leaves[17] || 0}）`);
    ok(!b2.p17glup && b2.p18glup, `⑲k gl-up 没跟着搬家（P17=${b2.p17glup} P18=${b2.p18glup}）`);
    ok(b2.p17poster.every(o => o > 0.98),
       `⑲k 离开 P17 后它的 poster 没回来（opacity=${b2.p17poster}）`);
    // 第二波两枚相邻新场景也走一遍（P2 决策环 → P3 三通道）：
    // 十六页共用一枚 canvas，任何一对相邻 3D 页都必须能热切换。
    await pg.evaluate(() => window.deck.go(1));    // P2
    await pg.waitForTimeout(1400);
    const c1 = await pg.evaluate(() => ({ ...window.__labTour, leaves: { ...window.__labTour.leaves } }));
    await pg.evaluate(() => window.deck.go(2));    // P3
    await pg.waitForTimeout(1400);
    const c2 = await pg.evaluate(() => ({ ...window.__labTour, leaves: { ...window.__labTour.leaves },
      p2glup: document.querySelector('.slide[data-p="2"] .lab-stage').classList.contains('gl-up'),
      p3glup: document.querySelector('.slide[data-p="3"] .lab-stage').classList.contains('gl-up') }));
    ok(c1.scene === 'ring' && c2.scene === 'lanes',
       `⑲k P2→P3 热切换没换人：${c1.scene} → ${c2.scene}`);
    ok((c2.leaves[2] || 0) === (c1.leaves[2] || 0) + 1,
       `⑲k P2 没走 leave（${c1.leaves[2] || 0}→${c2.leaves[2] || 0}）`);
    ok(!c2.p2glup && c2.p3glup, `⑲k gl-up 没跟着搬家（P2=${c2.p2glup} P3=${c2.p3glup}）`);
  }

  // ── h 周期 / 相位表静态复算（data-* 暴露的那几张表）──────────────────────
  const dta = await pg.evaluate(() => {
    const D = (p) => document.getElementById('labStage' + p).dataset;
    const v = D(1), g = D(21), b = D(17), r = D(18), t = D(7), sh = D(9), q = D(4);
    // 第二波九页
    const o = D(2), l = D(3), c = D(6), u = D(8), m = D(10),
          qs = D(11), w = D(12), k = D(13), y = D(14);
    const nums = (s) => (s || '').split(',').map(Number);
    const rows = (s) => (s || '').split(';').filter(Boolean).map(x => nums(x));
    return {
      o: { nodes: +o.labNodes, boxes: +o.labBoxes, tilt: +o.labTilt,
           dur: +o.labDur, durBr: +o.labDurBr, hot: +o.labHot },
      l: { seg: +l.labSeg, modes: +l.labModes, dep: +l.labDep,
           simplex: rows(l.labSimplex), half: rows(l.labHalf), full: rows(l.labFull) },
      c: { stations: +c.labStations, steps: +c.labSteps, bands: +c.labBands,
           znear: +c.labZnear, zdeep: +c.labZdeep },
      u: { in: +u.labIn, cut: +u.labCut, fall: +u.labFall, ghost: +u.labGhost },
      m: { layers: +m.labLayers, boxes: +m.labBoxes, zl: nums(m.labZl),
           lanes: +m.labLanes, beams: +m.labBeams, drift: +m.labDrift },
      qs: { dark: nums(qs.labDark), loss: nums(qs.labLoss), heap: nums(qs.labHeap),
            rain: +qs.labRain, rainDark: +qs.labRainDark, out: +qs.labOut },
      w: { apex: nums(w.labApex), mouth: nums(w.labMouth), weak: +w.labWeak,
           zweak: +w.labZweak },
      k: { slots: +k.labSlots, cyc: +k.labCyc, swap: +k.labSwap, cav: +k.labCav },
      y: { towers: +y.labTowers, arcs: +y.labArcs, steps: +y.labSteps,
           z: nums(y.labZ), cyc: +y.labCyc },
      v: { spin: +v.labSpin, amp: +v.labAmp, w0: +v.labW0, pts: +v.labPts,
           hot: nums(v.labHot), harm: (v.labHarm || '').split(';').map(x => nums(x)) },
      g: { spin: +g.labSpin, nodes: +g.labNodes, routes: +g.labRoutes, intro: +g.labIntro,
           dur: nums(g.labArcDur), gap: nums(g.labArcGap), off: nums(g.labArcOff) },
      b: { zper: nums(b.labZper), zoff: nums(b.labZoff), arcs: +b.labArcs,
           sparks: +b.labSparks, sway: +b.labSway, swayP: +b.labSwayP },
      r: { days: nums(r.labDays), turns: +r.labTurns, climb: +r.labClimb },
      t: { pins: nums(t.labPins), band: nums(t.labBand), steps: +t.labSteps },
      s: { rings: nums(sh.labRings), gap: nums(sh.labGap), streams: +sh.labStreams },
      q: { cut: +q.labCut, now: +q.labNow, turns: +q.labTurns },
    };
  });
  // ── 五枚新场景的表：语义常量必须与页上的 SVG 对得上（3D 不许新造坐标）──
  //   P17 五区：周期两两互异 + 全部负起相位 ⇒ 五个大脑「同时在工作、节奏互异」
  ok(dta.b.zper.length === 5, `⑲h P17 五区周期表长度 ${dta.b.zper.length} != 5`);
  ok(new Set(dta.b.zper).size === 5, `⑲h P17 五区周期有重复（${dta.b.zper}）—— 会齐步`);
  ok(dta.b.zoff.filter(x => x <= 0).length === 5, `⑲h P17 起相位不全为负（${dta.b.zoff}）`);
  ok(dta.b.sparks === 8, `⑲h P17 神经火花 ${dta.b.sparks} 枚 != 8（页上 6 弧 + 2 枚补）`);
  ok(dta.b.arcs === 6, `⑲h P17 突触弧 ${dta.b.arcs} 条 != 6`);
  ok(dta.b.sway > 0 && dta.b.sway <= 15,
     `⑲h P17 摇摆 ±${dta.b.sway}° 越界 —— 侧视轮廓是构图身份，不许整圈转`);
  //   P18 四枚站点必须落在页上四条 DAY 刻度的 x 上
  //   （二轮精修 · 波A：整条曲线图**改坐标本身**左移 80 ⇒ 四条刻度一起走 80；
  //    刻度与站点必须同步 —— 只走一边就等于站点指空了）
  ok(String(dta.r.days) === '70,340,620,980', `⑲h P18 站点 x 漂移：${dta.r.days}`);
  ok(dta.r.turns >= 2 && dta.r.turns <= 4.5, `⑲h P18 圈数 ${dta.r.turns} 越界`);
  //   P7 事件柱 x 与滞回带 y 必须与页上一致
  ok(String(dta.t.pins) === '880,1380', `⑲h P7 SOS/EOS 事件 x 漂移：${dta.t.pins}`);
  ok(String(dta.t.band) === '62,96', `⑲h P7 滞回带阈值漂移：${dta.t.band}`);
  ok(dta.t.steps === EXP_STEPS[6], `⑲h P7 场景声明的步数 ${dta.t.steps} 与页面分步不符`);
  //   P9 两层壳半径 = 页上两枚环的半径；三路噪声流
  ok(String(dta.s.rings) === '86,138', `⑲h P9 两层壳半径漂移：${dta.s.rings}`);
  ok(dta.s.streams === 3, `⑲h P9 噪声流 ${dta.s.streams} 路 != 3`);
  ok(dta.s.gap[0] > 0 && dta.s.gap[1] > dta.s.gap[0],
     `⑲h P9 缺口锥角不合法（${dta.s.gap}）—— 内壳的口必须开得比外壳大`);
  // ══ 第二波九页的静态复算（2026-08-31 终波）════════════════════════════════
  //   P2 决策轨道环：四站四盒 · hot 站点 = 「判断」那一支箭头的落点 x1200
  ok(dta.o.nodes === 4 && dta.o.boxes === 4, `⑲h P2 站点/站台数 ${dta.o.nodes}/${dta.o.boxes} != 4/4`);
  ok(dta.o.tilt > 0 && dta.o.tilt <= 1.6, `⑲h P2 环平面倾角系数 ${dta.o.tilt} 越界（微倾斜，不是竖起来）`);
  ok(dta.o.dur > dta.o.durBr, `⑲h P2 支轨没有比主环快一档（${dta.o.dur} vs ${dta.o.durBr}）`);
  ok(dta.o.hot === 1200, `⑲h P2 hot 站点 x 漂移：${dta.o.hot}`);
  //   P3 三通道 —— **语义闸**：半双工任何时刻只有一个方向在途，全双工两向恒同框，
  //   单工回向永远无包。三条全部用页上那套占空比算法在 3D 相位表上复算（不靠截帧）。
  ok(dta.l.modes === 3 && dta.l.seg === 14, `⑲h P3 相位表规格漂移：${dta.l.modes}/${dta.l.seg}`);
  ok(dta.l.dep > 0, `⑲h P3 两列没有拉开深度（dep=${dta.l.dep}）—— 那就不是「空间通道」`);
  const duty = (r) => (r[3] + dta.l.seg) / (dta.l.seg + r[2]);   // r = [T, off, ln, L, live]
  const inFlight = (r, t) => { const d = duty(r); let ph = ((t - r[1]) / r[0]) % 1;
    if (ph < 0) ph += 1; return d >= 0.999 ? true : (ph / d) <= 1; };
  {
    const H = dta.l.half;
    ok(H.length === 2, `⑲h P3 半双工通道数 ${H.length} != 2`);
    ok(Math.abs(duty(H[0]) - 1 / 3) < 1e-6 && Math.abs(duty(H[1]) - 1 / 3) < 1e-6,
       `⑲h P3 半双工占空比不是 1/3（${duty(H[0]).toFixed(4)} / ${duty(H[1]).toFixed(4)}）`);
    ok(Math.abs(Math.abs(H[0][1] - H[1][1]) - H[0][0] / 2) < 1e-6,
       `⑲h P3 半双工两向相位差不是半周期（${H[0][1]} / ${H[1][1]} @T=${H[0][0]}）`);
    let both = 0, none = 0, some = 0;
    for (let t = 0; t < 66; t += 0.005) {
      const n = (inFlight(H[0], t) ? 1 : 0) + (inFlight(H[1], t) ? 1 : 0);
      if (n === 2) both++; else if (n === 0) none++; else some++;
    }
    ok(both === 0, `⑲h P3 半双工互斥被破了：${both} 个采样时刻两个方向同时在途`);
    ok(some > 0 && none > 0, `⑲h P3 半双工不像半双工（在途 ${some} / 静默 ${none}）`);
    const F = dta.l.full;
    ok(F.length === 2 && F.every(r => duty(r) >= 0.999),
       `⑲h P3 全双工不是两向恒在途（${F.map(r => duty(r).toFixed(3))}）`);
    let fboth = 0;
    for (let t = 0; t < 20; t += 0.01) if (inFlight(F[0], t) && inFlight(F[1], t)) fboth++;
    ok(fboth === 2000, `⑲h P3 全双工两向没有永远同框（${fboth}/2000）`);
    const S = dta.l.simplex;
    ok(S.length === 2 && S[0][4] === 1 && S[1][4] === 0,
       `⑲h P3 单工回向不是静默通道（${S.map(r => r[4])}）`);
    ok(duty(S[0]) >= 0.999, `⑲h P3 单工正向不是恒在途（${duty(S[0]).toFixed(3)}）`);
  }
  //   P6 链路：四站 · 一步 build · 四条增量流带 · 两端近中间深
  ok(dta.c.stations === 4, `⑲h P6 站点 ${dta.c.stations} 枚 != 4`);
  ok(dta.c.steps === EXP_STEPS[5], `⑲h P6 场景声明的步数 ${dta.c.steps} 与页面分步不符`);
  ok(dta.c.bands === 4, `⑲h P6 增量流带 ${dta.c.bands} 条 != 4`);
  ok(dta.c.znear > dta.c.zdeep, `⑲h P6 深度剖面反了（近 ${dta.c.znear} / 深 ${dta.c.zdeep}）`);
  //   P8 打断：两根事件 x 与页上一致，340px = 340ms；让位段是 ghost 不是消失
  ok(dta.u.in === 700 && dta.u.cut === 1040, `⑲h P8 事件 x 漂移：${dta.u.in}/${dta.u.cut}`);
  ok(dta.u.fall === 340, `⑲h P8 快路径跨度不是 340（=${dta.u.fall}）`);
  ok(dta.u.ghost > 0 && dta.u.ghost < 0.4,
     `⑲h P8 让位档 ${dta.u.ghost} 越界 —— 让位是「陡降成 ghost」，不是消失也不是照常`);
  //   P10 大图（谨慎页）：五层 · 十一只盒 · **视差位移必须是 0**（可读性红线）
  ok(dta.m.layers === 5 && dta.m.zl.length === 5, `⑲h P10 分层数 ${dta.m.layers} != 5`);
  ok(new Set(dta.m.zl).size === 5, `⑲h P10 五层深度有重复（${dta.m.zl}）—— 那就没分层`);
  ok(dta.m.boxes >= 10, `⑲h P10 盒表只有 ${dta.m.boxes} 只 —— 大图的盒没进 3D`);
  ok(dta.m.lanes >= 4 && dta.m.beams >= 5, `⑲h P10 车道/层间束 ${dta.m.lanes}/${dta.m.beams} 太少`);
  ok(dta.m.drift === 0,
     `⑲h P10 声明了 ${dta.m.drift} 的视差位移 —— 大图页的红线是「一格不许挪」，必须是 0`);
  //   P11 QoS：断网段上游**一枚包都不许有**；缓存堆覆盖整条时间轴；下游包流不断
  ok(String(dta.qs.dark) === '526,164', `⑲h P11 断网域漂移：${dta.qs.dark}`);
  ok(String(dta.qs.loss) === '250,262', `⑲h P11 丢包域漂移：${dta.qs.loss}`);
  ok(dta.qs.rainDark === 0,
     `⑲h P11 断网段还有 ${dta.qs.rainDark} 枚上游包 —— 断网了上游就该停发`);
  ok(dta.qs.rain > 20, `⑲h P11 上游包只有 ${dta.qs.rain} 枚 —— 「密集下发」不成立`);
  ok(dta.qs.out > 0, `⑲h P11 下游包流 ${dta.qs.out} 枚 —— 「囤着播」要靠它不断`);
  ok(dta.qs.heap[0] < dta.qs.dark[0] && dta.qs.heap[1] > dta.qs.dark[0] + dta.qs.dark[1],
     `⑲h P11 缓存堆没有横跨断网段（堆 ${dta.qs.heap} / 断网 ${dta.qs.dark}）`);
  //   P12 视觉：视锥锥顶在眼镜 chip 上、锥口就是「看图识景」那只卡；次级带保持最远
  ok(String(dta.w.apex) === '110,155', `⑲h P12 视锥锥顶漂移：${dta.w.apex}`);
  ok(String(dta.w.mouth) === '256,70,316,170', `⑲h P12 视锥锥口不是「看图识景」卡：${dta.w.mouth}`);
  ok(dta.w.weak === 2, `⑲h P12 次级带 ${dta.w.weak} 件 != 2`);
  ok(dta.w.zweak < -100, `⑲h P12 次级带没被推远（z=${dta.w.zweak}）—— 页上弱化了，3D 不许捡回来`);
  //   P13 插槽机：六槽 · 一次只换一只 · 换装时长短于一轮
  ok(dta.k.slots === 6, `⑲h P13 插槽 ${dta.k.slots} 只 != 6`);
  ok(dta.k.swap > 0 && dta.k.swap < dta.k.cyc,
     `⑲h P13 热切换 ${dta.k.swap}s 不短于一轮 ${dta.k.cyc}s —— 会变成整排一起换`);
  ok(dta.k.cav > 0, `⑲h P13 插槽没有腔深（cav=${dta.k.cav}）—— 那就不是插槽`);
  //   P14 三塔：纵深严格递减（终端近 → 服务器 → 引擎云远）· 三道弧 · 一步 build
  ok(dta.y.towers === 3 && dta.y.arcs === 3, `⑲h P14 三塔三弧漂移：${dta.y.towers}/${dta.y.arcs}`);
  ok(dta.y.steps === EXP_STEPS[13], `⑲h P14 场景声明的步数 ${dta.y.steps} 与页面分步不符`);
  ok(dta.y.z[0] > dta.y.z[1] && dta.y.z[1] > dta.y.z[2],
     `⑲h P14 三塔没有纵深排布（${dta.y.z}）—— 终端要最近、引擎云要最远`);
  ok(dta.y.cyc > 0, `⑲h P14 握手没有轮次周期`);

  //   P4 截断 x = 页上「用户插话 = TTS 截断 = 快路径」共用的那根垂线
  ok(dta.q.cut === 1080, `⑲h P4 截断 x 漂移：${dta.q.cut}`);
  ok(dta.q.now === 860, `⑲h P4 NOW 播放头 x 漂移：${dta.q.now}`);
  // 声场球：三枚谐波权重归一 ⇒ 包络 |W| ≤ 1（振幅有上界，不会把球撑破构图）
  const wsum = dta.v.harm.reduce((a, h) => a + h[0], 0);
  ok(dta.v.harm.length === 3, `⑲h 声场球谐波枚数 ${dta.v.harm.length} != 3`);
  ok(Math.abs(wsum - 1) < 1e-6, `⑲h 谐波权重未归一（Σa=${wsum}）—— |W| 会越过 1`);
  ok(dta.v.amp > 0 && dta.v.amp <= 0.09, `⑲h 呼吸振幅 ${dta.v.amp} 越界（克制上限 .09）`);
  ok(dta.v.spin >= 90, `⑲h 封面自转 ${dta.v.spin}s/圈 —— 必须比地球（60s）慢，别抢主标`);
  ok(dta.v.hot[0] < dta.v.hot[1], `⑲h 波峰上色区间反了（${dta.v.hot}）`);
  ok(dta.v.pts >= 2000 && dta.v.pts <= 8000, `⑲h 点云 ${dta.v.pts} 枚 —— 太疏糊成球、太密烧片元`);
  // 谐波频率两两不整除 ⇒ 包络永不重复（齐步 = 呼吸变心跳，语义就错了）
  for (let i = 0; i < 3; i++) for (let j = i + 1; j < 3; j++) {
    const r = dta.v.harm[j][1] / dta.v.harm[i][1];
    ok(Math.abs(r - Math.round(r)) > 0.05, `⑲h 谐波 ${i}/${j} 频率成整数比（${r}）—— 会齐步`);
  }
  // ── 地球弧：静态复算「永不齐步」──────────────────────────────────────
  //    原型的说法是「周期两两不整除 + 负起相位 ⇒ 任意时刻 3–5 条在飞」。
  //    光比周期比值不够：6 号槽与 2 号槽的周期同为 9.3，但起相位差 3.9s ——
  //    周期相同而相位错开，照样永不同步。所以这里**真的把六个槽跑一遍**：
  //      ① 600s 窗口内任意时刻在飞条数落在 [1,6]，且从不为 0（球上永远有包）；
  //      ② 逐对验相位：周期相同的两槽，起相位差不许是周期的整数倍（那才叫齐步）。
  ok(dta.g.dur.length === 6 && dta.g.gap.length === 6 && dta.g.off.length === 6,
     `⑲h 弧相位表长度不齐（${dta.g.dur.length}/${dta.g.gap.length}/${dta.g.off.length}）`);
  const per = dta.g.dur.map((d, i) => d + dta.g.gap[i]);
  for (let i = 0; i < per.length; i++) for (let j = i + 1; j < per.length; j++) {
    if (Math.abs(per[i] - per[j]) > 1e-9) continue;          // 周期不同 ⇒ 天然错开
    let d = (dta.g.off[i] - dta.g.off[j]) % per[i];
    if (d < 0) d += per[i];
    ok(Math.min(d, per[i] - d) > 0.2,
       `⑲h 弧槽 ${i}/${j} 同周期(${per[i]}s)且相位只差 ${d.toFixed(2)}s —— 会齐步`);
  }
  let live = { min: 99, max: 0 };
  for (let t = 0; t < 600; t += 0.05) {
    let n = 0;
    for (let i = 0; i < 6; i++) {
      let tl = (t - dta.g.off[i]) % per[i]; if (tl < 0) tl += per[i];
      if (tl < dta.g.dur[i]) n++;
    }
    live.min = Math.min(live.min, n); live.max = Math.max(live.max, n);
  }
  ok(live.min >= 1, `⑲h 有时刻球上一条弧都没有（min=${live.min}）—— 网看着是死的`);
  ok(live.max <= 6, `⑲h 同时在飞 ${live.max} 条 —— 超出槽数`);
  ok(live.max - live.min >= 2, `⑲h 在飞条数恒定在 ${live.min}–${live.max} —— 六槽事实上齐步了`);
  ok(dta.g.off.filter(x => x < 0).length >= 4, `⑲h 负起相位不足（${dta.g.off}）`);
  console.log(`  · 弧相位静态复算：600s 窗口内同时在飞 ${live.min}–${live.max} 条 / 六槽`);
  ok(dta.g.nodes >= 200, `⑲h 节点 ${dta.g.nodes} 枚 —— 页上写着「200+ 全球节点」`);
  ok(dta.g.intro > 0 && dta.g.intro <= 1.2, `⑲h 入场 ${dta.g.intro}s 越界`);

  // ── h' 移植没漂移：三张表必须与 /lab-globe 原型逐字相同（数据单一真相自证）──
  {
    const proto = await fetch(BASE + '/decks/lab-globe.html').then(r => r.text());
    const grab = (k) => (proto.match(new RegExp(k + '\\s*=\\s*(\\[[^\\]]*\\]|"[^"]*")')) || [])[1] || '';
    const arr = (k) => grab(k).replace(/[[\]]/g, '').split(',').map(Number);
    ['dur', 'gap', 'off'].forEach((key, i) => {
      const want = arr(['ARC_DUR', 'ARC_GAP', 'ARC_OFF'][i]);
      ok(want.length === dta.g[key].length && want.every((x, k) => Math.abs(x - dta.g[key][k]) < 1e-9),
         `⑲h' 弧相位表与 /lab-globe 原型分叉（${key}：${dta.g[key]} vs ${want}）`);
    });
    const pn = grab('NODE_TABLE').replace(/"/g, '').split(';').length;
    const pr = grab('ROUTE_TABLE').replace(/"/g, '').split(';').length;
    ok(pn === dta.g.nodes, `⑲h' 节点表与原型分叉（${dta.g.nodes} vs ${pn}）`);
    ok(pr === dta.g.routes, `⑲h' 取道表与原型分叉（${dta.g.routes} vs ${pr}）`);
  }

  // ── 材质色红线：运行时里一个色号都不许写死（构建期已拦一道，这里是运行期复验）──
  {
    const html = await fetch(BASE + DECK).then(r => r.text());
    const mod = (html.split('<script type="module">')[1] || '').split('</script>')[0]
      .replace(/\/\*[\s\S]*?\*\//g, ' ').replace(/^\s*\/\/.*$/gm, ' ');
    [/#[0-9a-fA-F]{3,8}\b/, /\brgba?\(/, /\bhsla?\(/].forEach((re) =>
      ok(!re.test(mod), `⑲ 材质色红线：LAB 运行时写死了色号（${re}）`));
    // three 零外链：库文件只准指自托管路径
    ok(!/src="https?:\/\/(?!colinyao)/.test(html.split('<body')[0]), '⑲ head 里出现外链');
    ok(html.includes('"three":"/decks/assets/three/three.module.min.js"'), '⑲ importmap 未指自托管 three');
  }


  /* ═══════════════════════════════════════════════════════════════════════
     ⑲as / ⑲s / ⑲(P6,P8,P14,P18) —— 二轮精修 · 波A 的机器自证
     ═════════════════════════════════════════════════════════════════════ */
  // ── ⑲as 包络平滑度：**收敛阶**判据（不是量 max|Δ²| 的绝对值）─────────────
  //   max|Δ²| 的绝对值随采样步长走，量它没有意义。真正区分「有角 / 没角」的是
  //   **步长减半时它掉多少倍**：C² 光滑的函数掉 4×（O(h²)），折角只掉 2×（O(h)）。
  //   闸里带反证 —— **旧的逐柱采样包络必须过不了这一闸**，否则这一闸是空的。
  {
    const u8 = await pg.evaluate(() => {
      const el = document.querySelector('.lab-stage[data-lab-page="8"]');
      return { as: el.dataset.labAs, hs: el.dataset.labHs, bar: el.dataset.labBar,
               duck: el.dataset.labDuck, spd: el.dataset.labSpd };
    });
    const [aS, fS, phS, lamS] = u8.as.split('|');
    const A = aS.split(',').map(Number), F = fS.split(',').map(Number);
    const PH = phS.split(',').map(Number), LAM = +lamS;
    ok(Math.abs(A.reduce((x, y) => x + y, 0) - 1) < 1e-9,
       `⑲as 谐波权重未归一（Σa=${A.reduce((x, y) => x + y, 0)}）—— en 不再恒 ∈[0,1]，锯齿就回来了`);
    for (let i = 0; i < F.length; i++) for (let j = i + 1; j < F.length; j++) {
      const r = F[j] / F[i];
      ok(Math.abs(r - Math.round(r)) > 0.05, `⑲as 谐波 ${i}/${j} 成整数比（${r}）—— 包络会齐步`);
    }
    // 新：解析包络（与着色器 envAt 逐字同式）
    const envNew = (u) => { const k = 2 * Math.PI / LAM;
      return 0.5 + 0.5 * A.reduce((s2, a, i) => s2 + a * Math.sin(k * F[i] * u + PH[i]), 0); };
    // 旧：逐柱采样 + 线性插值（_P9HS 那张定高表本人）—— 反证用
    const HS = u8.hs.split(',').map(Number), [BX, GAP] = u8.bar.split(',').map(Number);
    const envOld = (u) => { const x = u + BX;
      const k = Math.floor((x - BX) / GAP), t = ((x - BX) / GAP) % 1;
      const a = HS[((k % HS.length) + HS.length) % HS.length];
      const b2 = HS[(((k + 1) % HS.length) + HS.length) % HS.length];
      return (a + (b2 - a) * t) / 2; };
    const d2max = (f, hStep) => { let m = 0;
      for (let u = 40; u < 1400; u += hStep)
        m = Math.max(m, Math.abs(f(u - hStep) - 2 * f(u) + f(u + hStep)));
      return m; };
    const order = (f) => d2max(f, 0.5) / d2max(f, 0.25);
    const oN = order(envNew), oO = order(envOld);
    ok(oN > 3.6, `⑲as 新包络的收敛阶只有 ${oN.toFixed(2)}×（C² 光滑应 ≈4×）—— 还有折角`);
    ok(oO < 2.6, `⑲as 反证失效：旧逐柱包络竟也拿到 ${oO.toFixed(2)}× —— 这一闸是空的`);
    ok(oN / oO > 1.5, `⑲as 新旧包络的收敛阶没拉开（${oN.toFixed(2)} vs ${oO.toFixed(2)}）`);
    console.log(`  · ⑲as 包络收敛阶：新 ${oN.toFixed(2)}× / 旧逐柱 ${oO.toFixed(2)}×（步长减半，C² 应掉 4×、折角只掉 2×）`);
    // 让位窗口 = 页上「收声」那段相位括号（840→1040，200px），不是旧版 60px 断崖
    const DK = u8.duck.split(',').map(Number);
    ok(DK[0] === 840 && DK[1] === 1040, `⑲(P8) 让位窗口漂移：${u8.duck}`);
    ok(DK[1] - DK[0] === 200, `⑲(P8) 让位窗口 ${DK[1] - DK[0]}px != 200`);
    ok(DK[0] > dta.u.in && DK[1] === dta.u.cut,
       `⑲(P8) 让位窗口没有落在「插话 → 收声」之间（${u8.duck} vs ${dta.u.in}/${dta.u.cut}）`);
    const p8 = await pg.evaluate(async () => {
      window.deck.go(7); await new Promise(r => setTimeout(r, 900));
      const u = window.__labTour.unit(); return u && u.state ? u.state() : null; });
    ok(p8 && p8.gA[0] > 0.98 && p8.gA[2] < 0.02 && Math.abs(p8.gA[1] - 0.5) < 0.02,
       `⑲(P8) 让位剖面不是「窗口内 1→0」：${p8 && p8.gA}`);
    ok(p8 && p8.spd.every(x => Math.abs(x - 110) < 1e-6),
       `⑲(P8) 两条声轨的波峰速度不是 110px/s：${p8 && p8.spd}`);
  }
  // ── ⑲(P6) 符号行三处接缝：有缝就不是一条流 ─────────────────────────────
  {
    const c6 = await pg.evaluate(async () => {
      const el = document.querySelector('.lab-stage[data-lab-page="6"]');
      window.deck.go(5); await new Promise(r => setTimeout(r, 900));
      const u = window.__labTour.unit();
      return { seg: el.dataset.labSeg, seam: el.dataset.labSeam, span: el.dataset.labSpan,
               tok: +el.dataset.labToken, st: u && u.state ? u.state() : null };
    });
    const SEG = c6.seg.split(';').map(r => r.split(',').map(Number));
    ok(SEG.length === 4, `⑲(P6) 符号行 ${SEG.length} 段 != 4`);
    for (let i = 0; i < 3; i++)
      ok(SEG[i][1] === SEG[i + 1][0],
         `⑲(P6) 第 ${i + 1} 处接缝有缝：${SEG[i][1]} → ${SEG[i + 1][0]} —— 那就不是一条流`);
    ok(c6.seam === '452,752,1052', `⑲(P6) 接缝 x 漂移：${c6.seam}`);
    ok(c6.span === '70,1610', `⑲(P6) 主路不是横贯全链（${c6.span}）`);
    ok(c6.tok === 2, `⑲(P6) token 段下标漂移：${c6.tok}`);
    ok(c6.st && c6.st.pulses >= 20,
       `⑲(P6) token 脉冲串只有 ${c6.st && c6.st.pulses} 枚 —— 「高密度」不成立`);
    ok(c6.st && String(c6.st.seam) === '452,752,1052',
       `⑲(P6) 运行时的接缝与页上不一致：${c6.st && c6.st.seam}`);
  }
  // ── ⑲(P14) 光束三段有序与常亮 ─────────────────────────────────────────
  {
    const y14 = await pg.evaluate(() => {
      const el = document.querySelector('.lab-stage[data-lab-page="14"]');
      return { beam: +el.dataset.labBeam, route: el.dataset.labRoute.split(',').map(Number),
               grow: +el.dataset.labGrow, hold: +el.dataset.labHold,
               rel: +el.dataset.labRel, cyc: +el.dataset.labCyc };
    });
    ok(String(y14.route) === '634,634,1228', `⑲(P14) 三段路由长漂移：${y14.route}`);
    ok(Math.abs(y14.route.reduce((a, b2) => a + b2, 0) / y14.beam - y14.grow) < 1e-6,
       `⑲(P14) 生长时长不是「三段 ÷ ${y14.beam}px/s」（${y14.grow}）`);
    ok(Math.abs(y14.cyc - (y14.grow + y14.hold + y14.rel)) < 1e-6,
       `⑲(P14) 一轮 ${y14.cyc} != 生长 ${y14.grow} + 停驻 ${y14.hold} + 收 ${y14.rel}`);
    ok(y14.hold >= 2, `⑲(P14) 全亮停驻 ${y14.hold}s < 2s —— 那一帧是本页的重点帧`);
    const probe = await pg.evaluate(async (T) => {
      window.deck.go(13); await new Promise(r => setTimeout(r, 1000));
      document.querySelector('.slide.active').querySelectorAll('[data-step]')
        .forEach(e => e.classList.add('on'));
      const t = window.__labTour; t.pace(12);
      const out = [];
      for (const s2 of T){ t.seek(s2); out.push(t.unit().state()); }
      t.pace(0);
      return out;
    }, [1.0, 2.5, 5.0, 7.0, 8.9]);
    const [h1, h2, h3, h4, h5] = probe.map(p => p.head);
    // 三段**有序**：任一时刻，前一段没走完，后一段就不许起步
    probe.slice(0, 4).forEach((p, i) => {
      for (let k = 1; k < 3; k++)
        ok(p.head[k] === 0 || p.head[k - 1] >= p.route[k - 1] - 1e-6,
           `⑲(P14) 第 ${k + 1} 段抢跑（t=${[1, 2.5, 5, 7][i]}s：${p.head.map(x => x.toFixed(0))}）`);
    });
    ok(h1[0] > 0 && h1[1] === 0 && h1[2] === 0, `⑲(P14) t=1.0s 不该只有第一段在走：${h1}`);
    ok(h2[0] >= 634 - 1e-6 && h2[1] > 0 && h2[2] === 0, `⑲(P14) t=2.5s 时序不对：${h2}`);
    ok(h3[0] >= 634 - 1e-6 && h3[1] >= 634 - 1e-6 && h3[2] > 0, `⑲(P14) t=5.0s 时序不对：${h3}`);
    // **常亮**：停驻窗口里三段全部到顶（这就是「①②③ 都通了」那一帧）
    ok(probe[3].done.every(x => x === 1), `⑲(P14) 停驻窗口里三段没有全亮：${probe[3].done}`);
    // 三段**等速**：每段用时 = 段长 ÷ 同一档注光速度
    const t2 = 2.5, t5 = 5.0;
    ok(Math.abs(h2[1] / (t2 - y14.route[0] / y14.beam) - y14.beam) < 1e-3,
       `⑲(P14) 第 2 段不是 ${y14.beam}px/s（${(h2[1] / (t2 - y14.route[0] / y14.beam)).toFixed(1)}）`);
    ok(Math.abs(h3[2] / (t5 - (y14.route[0] + y14.route[1]) / y14.beam) - y14.beam) < 1e-3,
       `⑲(P14) 第 3 段不是 ${y14.beam}px/s`);
    ok(h5[0] < 634 && h5[0] > 0, `⑲(P14) 收尾段不是「把光抽回去」：${h5}`);
    console.log(`  · ⑲(P14) 光束：三段 ${y14.route} ÷ ${y14.beam}px/s = 生长 ${y14.grow}s`
      + ` → 全亮停驻 ${y14.hold}s → 收 ${y14.rel}s = 一轮 ${y14.cyc}s`);
  }
  // ── ⑲(P18) 投影锁 / relock 机器证明 / 两图墨迹间距下限 ─────────────────
  {
    const r18 = await pg.evaluate(async () => {
      window.deck.go(17); await new Promise(r => setTimeout(r, 1000));
      const el = document.querySelector('.lab-stage[data-lab-page="18"]');
      const u = window.__labTour.unit();
      // 两图墨迹间距：左图 svg 内容的右缘 → 右图 svg 内容的左缘（舞台像素）
      const svgs = [...document.querySelectorAll('.slide[data-p="18"] .fig svg')];
      const sc = document.querySelector('.slide[data-p="18"]')
        .getBoundingClientRect().width / 1920;
      const bx = svgs.map(s2 => { const b2 = s2.getBBox(), r2 = s2.getBoundingClientRect();
        return { l: (r2.left + b2.x * sc) / sc, r: (r2.left + (b2.x + b2.width) * sc) / sc }; });
      return { rect: el.dataset.labRect, shift: +el.dataset.labShift,
               days: el.dataset.labDays, base: el.dataset.labBase, ring: el.dataset.labRing,
               gap: bx.length === 2 ? bx[1].l - bx[0].r : -1,
               leftInk: bx.length === 2 ? bx[0].l : -1,
               st: u && u.state ? u.state() : null };
    });
    ok(r18.rect === '120,276,1680,310', `⑲(P18) 舞台没有横跨两图：${r18.rect}`);
    ok(r18.shift === 80, `⑲(P18) 左移量漂移：${r18.shift}`);
    ok(r18.days === '70,340,620,980', `⑲(P18) 四条 DAY 刻度 x 没跟着左移：${r18.days}`);
    ok(r18.base === '70,160,980', `⑲(P18) 「真人销冠」基准虚线的两端漂移：${r18.base}`);
    ok(r18.ring === '190,155,96', `⑲(P18) LOOP 环几何漂移：${r18.ring}`);
    ok(r18.st && r18.st.D === 1500 && r18.st.D0 === 560,
       `⑲(P18) 相机没有换到 D1500：${r18.st && [r18.st.D0, r18.st.D]}`);
    // relock 的**机器证明**：新旧相机下的屏点与雾值偏差必须是 0（不是「小」，是 0）
    ok(r18.st && r18.st.relockDev < 1e-6,
       `⑲(P18) mkRelock 没有逐像素还原：屏点最大偏差 ${r18.st && r18.st.relockDev}px`);
    ok(r18.st && r18.st.fogDev < 1e-9,
       `⑲(P18) mkRelock 之后深度雾变了：${r18.st && r18.st.fogDev}`);
    // 两图墨迹间距下限：终审「两张图偏挤」—— 改前 ≈140px，本波必须 ≥ 200px
    ok(r18.gap >= 200, `⑲(P18) 两图墨迹间距 ${r18.gap.toFixed(0)}px < 200 —— LOOP 还是被挤着`);
    // 左移之后最左墨迹仍须稳在版心（120）之内
    ok(r18.leftInk >= 0, `⑲(P18) 左图墨迹越过 figbox 左缘（${r18.leftInk.toFixed(1)}）`);
    console.log(`  · ⑲(P18) 两图墨迹间距 ${r18.gap.toFixed(0)}px（左移 ${r18.shift}px）`
      + ` · relock 屏点偏差 ${r18.st.relockDev.toExponential(1)}px（D${r18.st.D0}→D${r18.st.D}）`);
  }
  // ── ⑲s 全局流速复算：A 档 30 股全部落在 110 ±30% ───────────────────────
  {
    const rows = await pg.evaluate(() => [...document.querySelectorAll('.lab-stage[data-lab-spd]')]
      .map(el => [+el.dataset.labPage, el.dataset.labSpd]));
    const all = [];
    rows.forEach(([p, s2]) => s2.split(';').filter(Boolean)
      .forEach(r => { const [nm, v] = r.split(','); all.push({ p, nm, v: +v }); }));
    ok(all.length === 30, `⑲s A 档股数 ${all.length} != 30`);
    ok(rows.length === 8, `⑲s A 档页数 ${rows.length} != 8`);
    all.forEach(r => ok(r.v >= 77 && r.v <= 143,
      `⑲s P${r.p}「${r.nm}」${r.v}px/s 越出 110±30%（77–143）`));
    const lo = Math.min(...all.map(r => r.v)), hi = Math.max(...all.map(r => r.v));
    ok(hi / lo <= 1.5, `⑲s 全局极差 ${(hi / lo).toFixed(2)}× —— 同一条河不该有这么大落差`);
    console.log(`  · ⑲s 全局流速：${rows.length} 页 ${all.length} 股 · ${lo}–${hi}px/s · 极差 ${(hi / lo).toFixed(2)}×`);
    // 同页之内也不许有「重要 = 快」的错觉：任一页内极差 ≤ 1.35×
    rows.forEach(([p, s2]) => {
      const v = s2.split(';').filter(Boolean).map(r => +r.split(',')[1]);
      ok(Math.max(...v) / Math.min(...v) <= 1.35,
         `⑲s P${p} 页内极差 ${(Math.max(...v) / Math.min(...v)).toFixed(2)}× —— 同页快慢会被读成主次`);
    });
  }

  // ── P1 kicker 必须挂上家族名（LAB 演绎的唯一一处正文改动）──
  const k1 = await pg.evaluate(() => document.querySelector('.slide[data-p="1"] .kk').textContent.trim());
  ok(k1 === 'AGORA · CONVERSATIONAL AI ENGINE · DEEP DIVE · 深入讲解 · LAB',
     `⑲ P1 kicker 漂移：「${k1}」`);
  // 回到 P1，把主跑收在一个干净状态上
  await pg.evaluate(() => window.deck.go(0));
  await pg.waitForTimeout(400);
}

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 分步 P6/P7/P14/P20 各 1 步 · P21 口径已锁 · 三数章序 P5→P6→P7→P8→P9→P10 · P10 大图闸 + 三锚点 · P19 实拍图 + P22 双源 logo 闸 · Call Agent 三页闸 · P20 视频页闸 · deckSwap 常显`);
await b.close();

/* ═══════════════════════════════════════════════════════════════════════════
   ⑲ WebGL 豁免通道 · 独立上下文段
   —— 下面五条各自需要一套不同的浏览器 / 媒体条件，只能另开上下文跑。
   ═══════════════════════════════════════════════════════════════════════════ */
const OUT = process.env.OUT || '/home/claude/eco-review';
mkdirSync(OUT, { recursive: true });

/* ── c 禁用 WebGL 启动 ⇒ 整 deck 22 页照常可读（LAB 家族最硬的一条）────────
   「3D 起不来」不许等于「这份 deck 废了」：P1/P21 退回 poster 静帧，
   另外 20 页本来就没有 canvas，一格不受影响。 */
{
  const b2 = await chromium.launch({ executablePath: CHROME,
    args: ['--disable-webgl', '--disable-webgl2', '--disable-gpu'] });
  const ctx = await b2.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  if (THEME === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const pg2 = await ctx.newPage();
  const err2 = [];
  pg2.on('pageerror', e => { if (!MEDIA_EXEMPT.test(String(e))) err2.push('PAGEERROR ' + e.message); });
  await pg2.goto(BASE + DECK + '#1', { waitUntil: 'load' });
  await pg2.waitForTimeout(7500);                       // 看门狗 6s
  const fb = await pg2.evaluate((pages) => {
    const one = (p) => {
      const st = document.querySelector(`.slide[data-p="${p}"] .lab-stage`);
      const posters = [...document.querySelectorAll(`.slide[data-p="${p}"] .lab-poster`)];
      return { glup: st.classList.contains('gl-up'),
               posterOp: posters.map(e => +getComputedStyle(e).opacity),
               // 降级层里必须真的有图，不是一个空壳：几何件数 + 路径总长度两头看。
               // （件数比长度稳：P18 的成长曲线是一条长 path，P9 的两枚环各是一条短弧，
               //   只看长度会把「短而多」的页误判成空。）
               ink: posters.reduce((n, g) =>
                 n + g.querySelectorAll('path,rect,circle,line,polygon,ellipse').length, 0),
               // 「墨量」而不是单看 path：第二波九页里 P8 的降级层主体是波形 <rect>、
               // P14 是三只塔与塔内小盒，路径串本来就短 —— 一枚 rect/circle 折算 24 字符。
               dlen: posters.reduce((n, g) => n + [...g.querySelectorAll('path')]
                 .reduce((m, e) => m + (e.getAttribute('d') || '').length, 0), 0) };
    };
    const c = document.getElementById('labGl');
    const txt = [...document.querySelectorAll('.slide')].map(s => s.textContent.replace(/\s+/g, '').length);
    return { cvs: { mode: c.dataset.labMode, run: c.dataset.labRun,
                    parent: c.parentNode.className, n: document.querySelectorAll('canvas').length },
             per: Object.fromEntries(pages.map(p => [p, one(p)])), txt,
             all: document.getElementById('deckStage').textContent.replace(/\s+/g, ' ') };
  }, LAB_PAGES);
  ok(fb.cvs.mode === 'POSTER', `⑲c 无 WebGL · mode=${fb.cvs.mode}（应为 POSTER）`);
  ok(fb.cvs.run === '0', '⑲c 无 WebGL · 还在跑 rAF');
  ok(fb.cvs.parent === 'lab-garage', `⑲c 无 WebGL · canvas 没停在车库（${fb.cvs.parent}）`);
  ok(fb.cvs.n === 1, `⑲c 无 WebGL · canvas 数 ${fb.cvs.n}`);
  LAB_PAGES.forEach((P) => {
    const u = fb.per[P];
    ok(!u.glup, `⑲c 无 WebGL · P${P} 假装起来了（gl-up 还挂着）`);
    ok(u.posterOp.length >= 1 && u.posterOp.every(o => o === 1),
       `⑲c 无 WebGL · P${P} poster 没常驻（opacity=${u.posterOp}）`);
    ok(u.ink >= 3, `⑲c 无 WebGL · P${P} 降级层只有 ${u.ink} 个几何件 —— 这一页降不下去`);
    ok(u.dlen + u.ink * 24 > 260,
       `⑲c 无 WebGL · P${P} 降级层墨量不足（path ${u.dlen} 字符 + ${u.ink} 件）`);
  });
  ok(fb.txt.length === N, `⑲c 无 WebGL · 页数 ${fb.txt.length} != ${N}`);
  fb.txt.forEach((n, i) => ok(n >= (i + 1 === VIDEO_PAGE ? 8 : 20),
    `⑲c 无 WebGL · P${i + 1} 正文只剩 ${n} 字 —— 这一页读不了了`));
  // 口径锁在降级态里照样在（poster 只换图，不换字）
  ['No.1', '100万+', '900亿+', '50+', 'IDC 中国视频云市场报告',
   '节点分布示意', '对话即交互'].forEach(s =>
    ok(fb.all.includes(s), `⑲c 无 WebGL · 全 deck 缺「${s}」`));
  ok(err2.length === 0, `⑲c 无 WebGL · pageerror ${err2.length}：${err2.slice(0, 2).join(' | ')}`);
  await pg2.screenshot({ path: `${OUT}/lab-fallback-p1.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  // 降级态的 P17 大脑（终审交付物 wave1-fallback.png）：这一页是本波之冠，
  // 「3D 起不来 = 页上原来那张 SVG 完整呈现」必须有一张实证。
  for (const [pp, name] of [[17, 'wave1-fallback'], [21, 'lab-fallback']]) {
    await pg2.evaluate(k => window.deck.go(k - 1), pp);
    await pg2.waitForTimeout(2600);    // 家族入场系逐件 stagger，700ms 拍到的是半程
    await pg2.screenshot({ path: `${OUT}/${name}.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await b2.close();
}

/* ── d prefers-reduced-motion ⇒ 渲一帧停帧（不是黑屏，也不是继续转）────────── */
{
  const b3 = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
  const ctx = await b3.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1,
    reducedMotion: 'reduce' });
  const pg3 = await ctx.newPage();
  await pg3.goto(BASE + DECK + HOLD + '#1', { waitUntil: 'load' });
  await pg3.waitForTimeout(3500);
  const rm = await pg3.evaluate(() => {
    const c = document.getElementById('labGl');
    return { mode: c.dataset.labMode, run: c.dataset.labRun,
             glup: document.getElementById('labStage1').classList.contains('gl-up') };
  });
  ok(rm.mode === 'STILL', `⑲d reduced-motion · mode=${rm.mode}（应为 STILL）`);
  ok(rm.run === '0', '⑲d reduced-motion · rAF 还在跑');
  ok(rm.glup, '⑲d reduced-motion · 应当渲出一帧并让 poster 让位（不是退回 poster）');

  /* ── f DPR 上限 2：同一个浏览器里换一个 deviceScaleFactor=3 的上下文 ── */
  const ctx2 = await b3.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 3 });
  const pg4 = await ctx2.newPage();
  await pg4.goto(BASE + DECK + HOLD + '#1', { waitUntil: 'load' });
  await pg4.waitForTimeout(2500);
  const dpr = await pg4.evaluate(() => ({
    dpr: +document.getElementById('labGl').dataset.labDpr,
    dev: window.devicePixelRatio,
  }));
  ok(dpr.dev > 2, `⑲f 上下文 devicePixelRatio=${dpr.dev} —— 这条闸没在真正的高 DPR 下跑`);
  ok(dpr.dpr <= 2, `⑲f DPR 未封顶（devicePixelRatio=${dpr.dev} ⇒ 渲染 DPR=${dpr.dpr}）`);

  /* ── g @media print ⇒ 藏 canvas 显 poster；beforeprint 抓到的帧非空 ── */
  await pg4.evaluate(() => window.deck.go(0));
  await pg4.waitForTimeout(1200);
  const pr = await pg4.evaluate(() => {
    // beforeprint 是同步事件：处理器里「先渲一帧、立刻 toDataURL」才读得到非空帧。
    // 单渲染器巡游下，打印帧只有**当前页**抓得到（纸上其余 3D 页以 poster 为准）。
    window.dispatchEvent(new Event('beforeprint'));
    const im1 = document.getElementById('labPrint1');
    return { s1: (im1.getAttribute('src') || '').length,
             head1: (im1.getAttribute('src') || '').slice(0, 22) };
  });
  ok(pr.s1 > 5000, `⑲g P1 打印帧是空的（dataURL ${pr.s1} 字节）`);
  ok(pr.head1.startsWith('data:image/png;base64'), `⑲g 打印帧不是 PNG dataURL：${pr.head1}`);
  await pg4.emulateMedia({ media: 'print' });
  const pm = await pg4.evaluate(() => ({
    cv: getComputedStyle(document.getElementById('labGl')).display,
    po: +getComputedStyle(document.querySelector('#labStage1 .lab-poster')).opacity,
    // 纸上其余 3D 页的 poster 也必须常驻（canvas 只在当前那一页里）
    poAll: [...document.querySelectorAll('.lab-poster')].map(e => +getComputedStyle(e).opacity),
    pi: getComputedStyle(document.getElementById('labPrint1')).display,
    probe: getComputedStyle(document.getElementById('labProbe')).display,
  }));
  ok(pm.poAll.every(o => o === 1), `⑲g print · 有 poster 没显（${pm.poAll.filter(o => o !== 1).length} 枚）`);
  ok(pm.cv === 'none', `⑲g print · canvas 没藏（display=${pm.cv}）`);
  ok(pm.po === 1, `⑲g print · poster 没显（opacity=${pm.po}）`);
  ok(pm.pi === 'block', `⑲g print · 打印帧没盖上去（display=${pm.pi}）`);
  ok(pm.probe === 'none', '⑲g print · FPS 探针没藏');
  await pg4.emulateMedia({ media: 'screen' });
  await b3.close();
}

/* ── i FPS 自动降级：**不带** ?lab=hold 的默认 URL，软渲染 <20fps ⇒ 2s 内退 poster ──
   容器里 SwiftShader 只有个位数 fps，正好是这条闸的天然测试床。
   同时反证 ?lab=hold 那条路：主跑全程 LIVE（上面 ⑲b 已经验过）。 */
{
  const b4 = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
  const ctx = await b4.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const pg5 = await ctx.newPage();
  await pg5.goto(BASE + DECK + '#1', { waitUntil: 'load' });
  await pg5.waitForTimeout(5000);
  const dg = await pg5.evaluate(() => {
    const c = document.getElementById('labGl');
    return { mode: c.dataset.labMode, run: c.dataset.labRun, deg: c.dataset.labDegraded,
             fps: +c.dataset.labFps,
             glup: document.getElementById('labStage1').classList.contains('gl-up'),
             posterOp: +getComputedStyle(document.querySelector('#labStage1 .lab-poster')).opacity };
  });
  ok(dg.mode === 'POSTER' && dg.deg === '1',
     `⑲i 软渲染下没有自动降级（mode=${dg.mode} fps=${dg.fps}）—— 探针那条闸失效了`);
  ok(dg.run === '0', '⑲i 降级后 rAF 还在跑');
  ok(!dg.glup && dg.posterOp === 1, `⑲i 降级后 poster 没接管（glup=${dg.glup} op=${dg.posterOp}）`);
  await b4.close();
}

/* ── j 双主题 WebGL 静置帧各一张 + 材质真的换了色（不是只换了 DOM）────────── */
{
  const b5 = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
  const lum = {};
  for (const th of ['light', 'dark']) {
    const ctx = await b5.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    await ctx.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, th);
    const pg6 = await ctx.newPage();
    await pg6.goto(BASE + DECK + HOLD + '#1', { waitUntil: 'load' });
    await pg6.waitForTimeout(6500);
    // 逐 3D 页各一张 WebGL 静置帧：只裁该页声明的图形区（页上的字换主题也会变，
    // 把字圈进来等于什么都没量）。七页 × 两主题 = 终审肉眼比对的全部素材。
    for (const P of LAB_PAGES) {
      await pg6.evaluate(k => window.deck.go(k - 1), P);
      await pg6.waitForTimeout(P === 1 ? 3200 : 2600);
      const st = await pg6.evaluate((k) => {
        const c = document.getElementById('labGl');
        const el = document.querySelector(`.slide[data-p="${k}"] .lab-stage`);
        return { mode: c.dataset.labMode, page: +c.dataset.labPage,
                 rect: (el.dataset.labRect || '').split(',').map(Number) };
      }, P);
      ok(st.mode === 'LIVE' && st.page === P,
         `⑲j ${th} · P${P} 静置帧不是 WebGL 态（mode=${st.mode} page=${st.page}）`);
      await pg6.screenshot({ path: `${OUT}/lab-still-p${P}-${th}.png`,
        clip: { x: st.rect[0], y: st.rect[1], width: st.rect[2], height: st.rect[3] } });
    }
    await pg6.evaluate(() => window.deck.go(20));
    await pg6.waitForTimeout(2600);
    await pg6.screenshot({ path: `${OUT}/lab-webgl-still-${th}.png`,
                           clip: { x: 1220, y: 250, width: 500, height: 500 } });
    // 屏上像素读不回来（canvas 不给读、截图在 Node 侧），这里钉住的是**材质 token 层**：
    // three 的每一枚 uniform 都是从这几个变量读的，变量分叉 ⇒ 材质必然分叉。
    // 两张静置帧本身留给终审肉眼与 ImageMagick 比。
    lum[th] = await pg6.evaluate(() => {
      const cs = getComputedStyle(document.documentElement);
      return { land: cs.getPropertyValue('--g-land').trim(),
               node: cs.getPropertyValue('--g-node').trim(),
               ocean: cs.getPropertyValue('--g-ocean').trim(),
               rimPow: cs.getPropertyValue('--g-rim-pow').trim(),
               vInk: cs.getPropertyValue('--v-ink').trim() };
    });
    await ctx.close();
  }
  await b5.close();
  ok(lum.light.ocean !== lum.dark.ocean,
     `⑲j 双主题材质 token 没换（--g-ocean 两边都是 ${lum.light.ocean}）`);
  ok(lum.light.rimPow !== lum.dark.rimPow,
     `⑲j 双主题 fresnel 幂没换（--g-rim-pow 两边都是 ${lum.light.rimPow}）`);
  ok(lum.light.vInk !== lum.dark.vInk,
     `⑲j 声场球点色两主题相同（--v-ink=${lum.light.vInk}）`);
  // 帧本身的差异用 ImageMagick 在交付环节比对，这里只钉住「token 层真的分叉」
  console.log(`  · WebGL 静置帧已出：${OUT}/lab-still-p{${LAB_PAGES}}-{light,dark}.png`
    + `（--g-ocean light=${lum.light.ocean} dark=${lum.dark.ocean}）`);
}

console.log(fails.length ? '✗ FAIL(webgl) ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · WebGL 豁免通道全绿（结构 / 起帧 / 禁 WebGL 22 页可读 / `
                           + `reduced-motion 停帧 / 非激活停 rAF / DPR≤2 / print 非空帧 / 相位表复算 / 自动降级）`);
process.exit(fails.length ? 1 : 0);


