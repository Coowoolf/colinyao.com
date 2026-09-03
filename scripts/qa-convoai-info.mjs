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
//   ⑫  口径锁：P2 四大数 + 近一半 + IDC 注 + SOURCE / P5 96.5% + 2,475 /
//       P8 使命 · 愿景两句 + 三簇题注 + 三不三步（细节层）逐字
//   ⑭  红线反向闸：价格 / staging / 引擎 P16 的「盲测 · 32,000」/ 旧分类学 / 旧措辞
//   ⑮  P7 案例墙 14 家客户名逐字（名单硬编码在本文件，改名必须两处同改）
// 2026-09-01 LAB 整体重构轮新增 ⑲/⑳ **WebGL 豁免通道**（照抄 qa-convoai-lab 的闸门体系）：
//   ⑲a  逐页舞台结构：场景名 / data-lab-rect / poster 层 / 打印帧位 / 层序 /
//       poster 组里**一个字也没有**（字必须压在 canvas 之上）
//   ⑲a2 **单渲染器巡游**：全文档 WebGL canvas 恰 1 枚 + 车库在位 + registry 页码表
//   ⑲b  逐页起帧 + 逐页对位（±1.2px）+ 绘制缓冲区跟着矩形走 + poster 淡出 / canvas 淡入
//   ⑲c  **禁用 WebGL 启动 ⇒ 8 页照常完整可读**（速讲版的生命线：客户端多样）
//   ⑲d  prefers-reduced-motion ⇒ 渲一帧停帧　⑲f DPR ≤ 2　⑲g print 藏 canvas 显 poster
//   ⑲e  非激活页 ⇒ canvas 回车库 / rAF 停 / gl-up 全摘　⑲i FPS 自动降级
//   ⑲j  双主题 × 逐 3D 页静置帧 + 材质 token 真的分叉
//   ⑲k  翻页热切换：当前景换人 + 前一景确实走了 leave
//   ⑳clr **净空**：运行时逐顶点 × 构建期解析，两条算路对表；名册 × 活 DOM 对表
//   ⑳chip P4 的 hot 是抽屉 chip —— 正面断言它离 3D 至少 16px
//   ⑳spd A 档流速逐股复算（110 ±30% · 同页极差 ≤1.35×）
//   ⑳net P8「网在生长」：十条边的相位复算 φ_k − k·2π/10 = 0 + 场面构成正面钉死
//        （v3.1 起接替 ⑳rv —— 三条支流一条河退役）
//   ⑳flick 消闪：定拍逐帧亮度突变上限　⑳ink 浅 / 暗墨量比 ≥ 0.90
// 用法：node scripts/qa-convoai-info.mjs        （THEME=dark 二跑）
//      BASE=http://localhost:8899 node scripts/qa-convoai-info.mjs
import { chromium } from 'playwright-core';
import { mkdirSync } from 'fs';
const THEME = process.env.THEME || 'light';
const BASE = process.env.BASE || 'http://localhost:8899';
const N = 8;
// v3 三波收官：P2–P7 每页一枚**细节层**（该页 data-step=1）；P1 封面按规格不带。
// v3.1（P8 重做轮）：P8 也带一枚 —— 三不 / 三步 / OpenAI / DEMO 四件密材料从主版面
// 搬进抽屉，主版面只留使命 · 愿景 · 三种互动。
const EXP_STEPS = [0, 1, 1, 1, 1, 1, 1, 1];
const DETAIL_PAGES = [2, 3, 4, 5, 6, 7, 8];
const BOARD = { 1: 'title' };            // 其余一律 content
// P1 封面自 2026-09-01 起走**声场球**（3D），AI-art 位图退场 ⇒ 全 deck 无 hero-art。
// （对比版 INFO_P1=art 只在终审出图时构建，不进 qa。）
const HERO = {};
const ECO = { 7: 'ecosystem-stack-v4' }; // eco-art 只上 P7 生态主视觉（polish-v4）
// P7 案例墙客户名：逐字对照公开卡片上烧录的品牌（客户当面的 deck 一字不能错）
const CASES = ['集贤科技', 'Robopoet', 'luwu',
  'Pophie', '商汤', 'MiniMax', '智谱清言', '星野', '灵机一动',
  'LOOKTECH', 'HeyCyan', 'LOOKEE', '莲偶科技', '豆神 AI'];
// 深链契约：页 → 引擎章号
const DEEPLINK = [{ page: 5, chip: 'agentExpand', hash: 16 }, { page: 6, chip: 'physExpand', hash: 19 }];
// ── LAB 场景表（qa 与产物两头对表，加错页 / 漏页当场炸）────────────────────
//   P6 'exit' 是第二波加进来的**加法层**（构建开关 INFO_P6=exit｜off）：页上本来没有图，
//   3D 坐在标题右侧那条空带上，poster 是构建期离线投影出来的一枚**无字 figbox**。
//   若产物是 INFO_P6=off 出的，把 6 从这张表里删掉、FLAT_PAGES 改回 [6,7]、
//   ⑳spd 的 14 股 / 6 页改回 13 / 5 —— 这三处是这一枚场景在 qa 里的全部落点。
// v3.1：P8 的 `river`（三条支流一条河）退役，换成 `net`（一张实时网上的三种互动）。
// v3.2：`net`（线框示意图 · Colin 判「丑」「不适配」）再退役，换成 `galaxy`
//       （互动星系 · 12,000 点体积点云 —— 与 P5 五脑区大脑同一语系）。
const LAB_SCENES = { 1: 'voice', 2: 'globe', 3: 'grow', 4: 'duplex', 5: 'brain',
                     6: 'exit', 7: 'wall', 8: 'galaxy' };
const LAB_PAGES = Object.keys(LAB_SCENES).map(Number).sort((a, b) => a - b);
// v3 波C 起**八页全有场景**（P7 的五层生态图搬进细节层，主图换成 3D 星座墙）⇒
// 这张表空了。⑲e「非激活页 ⇒ canvas 回车库」因此改成「把 .active 全摘掉」来验
// （MutationObserver 会照样触发 syncActive —— 判据一格没放松，只是换了个触发法）。
const FLAT_PAGES = [];
// P1 声场球 / P2 地球走构建期离线投影出来的**全屏专用** poster（落在舞台里）；
// 另外四页的 poster 都在 .pp 里：三页是「页上原来那张 SVG」，P6 是加法层自己的
// 那枚无字 figbox（同样在 .pp 里）
const INPAGE = LAB_PAGES.filter(p => p !== 1 && p !== 2);
// ⑳clr 的「两条算路对表」只对 px 投影锁场景 —— P1 声场球 / P2 地球是**球面场景**
// （camSphere），没有 unlock/geoClr 那套机制、也不交 state().clr。
// 地球的净空由 ⑳globe 单独验（弧外包络圆 vs 页上字形行框）。
const CLR_PAGES = LAB_PAGES.filter(p => p !== 1 && p !== 2);
// ── 两条算路的关系：本 deck 自己写的四枚场景（grow / exit / river …）是「中心线 +
//   常量保守半宽」⇒ 构建期解析与运行时逐顶点**必然相等**（±0.5px）。
//   P4 的 ribbon 网格顶点在构建期能逐点复现（`ribbonGeo` 的 Python 同解）⇒ 照旧等式。
//   P5 的 12000 点体积点云、P7 的摆动 / 浮动扫掠不能 ⇒ 构建期给的是**外包络**（下界），
//   按不等式对表：运行时 ≥ 解析 − 0.5。注意方向：下界只会让闸更严，不是放松。
//   P8（v3.2）同理：互动星系整体在转（1 圈/90s）+ 在摇（±6°/17s），点云 / 弧 / 流
//   三件几何逐帧在变 ⇒ 构建期交的是「(r,|w|) 族 × 整圈 φ × 摇摆三档」的**扫掠包络**。
//   下限（16px 加法层规则）与「运行时 ≥ 解析 − 0.5」两条一格没松。
const CLR_BOUND = [5, 7, 8];
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
// 软渲染开关：容器里没有 GPU，不给这三个 flag 连 WebGL 上下文都拿不到
const GL_ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
// 主跑一律带 ?lab=hold（容器软渲染只有个位数 fps，不关掉自动降级就全程 poster，
// ⑲b 那条就验不到「起来了」）。自动降级本身在 ⑲i 用**不带** hold 的 URL 单独验。
const HOLD = '?lab=hold';
const OUT = process.env.OUT || '/home/claude/eco-review';
// 导航超时给到 90s：容器里是 SwiftShader 软渲染，独立上下文段会同时开两个浏览器，
// 七枚场景（含 12000 点的大脑）一起 boot 时首屏 load 会拖过 playwright 的 30s 默认值。
// 这是**跑得动**的问题，不是闸门阈值 —— 判据一格没放松。
const NAV_MS = +(process.env.NAV_MS || 90000);
mkdirSync(OUT, { recursive: true });
const fails = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };
const b = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const errs = [];
pg.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
pg.on('console', m => {
  if (m.type() === 'error' && !(m.location()?.url || '').includes('favicon')) errs.push(m.text());
});
if (THEME === 'dark') await pg.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
await pg.goto(BASE + '/decks/convoai-info.html' + HOLD + '#1', { waitUntil: 'load', timeout: NAV_MS });
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
// 封面自 2026-09-01 改走声场球（3D）⇒ 全 deck 无 hero-art，这一条随之退役；
// 位图那一版（INFO_P1=art）只在终审出图时构建，不进 qa。
if (Object.keys(HERO).length)
  ok(flipped === 'dark' ? (sw.lt === 'none' && sw.dk === 'block') : (sw.dk === 'none' && sw.lt === 'block'),
     `⑦ hero 双源 ${sw.lt}/${sw.dk}`);
ok(flipped === 'dark' ? (sw.elt === 'none' && sw.edk === 'block') : (sw.edk === 'none' && sw.elt === 'block'),
   `⑩ 切换后 eco 双源 ${sw.elt}/${sw.edk}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

/* ═══════════════════════════════════════════════════════════════════════════
   ⑲/⑳ WebGL 豁免通道 · 主跑内联段
   （a 结构 / a2 单渲染器巡游 / b 起帧对位 / e 非激活停 rAF / k 热切换 /
     clr 净空两条算路 / chip / spd / rv 相位 / flick 消闪）
   独立上下文才验得了的五条（禁 WebGL / reduced-motion / print / DPR / 自动降级）
   在文件末尾的「⑲ 独立上下文段」。
   ═══════════════════════════════════════════════════════════════════════════ */
{
  // ── a 结构 ──────────────────────────────────────────────────────────────
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
      posterPoly: [...s.querySelectorAll('.lab-poster')]
        .reduce((n, g) => n + g.querySelectorAll('polygon').length, 0),
      inPP: !!s.querySelector('.pp .lab-stage'),
      order: [...s.children].map(el => (el.className || '').split(' ')[0]).join('>'),
    };
  }));
  struct.forEach((v) => {
    const want = LAB_SCENES[v.p] || null;
    ok(v.scene === want, `⑲a P${v.p} 3D 舞台种类 ${v.scene} != ${want}`);
    ok(v.stage === (want ? 1 : 0), `⑲a P${v.p} .lab-stage 数 ${v.stage}`);
    if (!want) { ok(v.poster === 0, `⑲a P${v.p} 无场景却挂了 poster 层`); return; }
    ok(v.poster >= 1, `⑲a P${v.p} 缺 poster 降级层`);
    ok(v.print === 1, `⑲a P${v.p} 缺打印帧位 .lab-print`);
    ok(!v.inPP, `⑲a P${v.p} 3D 舞台落在 .pp 里了 —— 必须是 .pp 的兄弟`);
    ok(v.order === 'conf-bg>lab-stage>pp', `⑲a P${v.p} 层序漂移：${v.order}`);
    ok(/^\d+,\d+,\d+,\d+$/.test(v.rect || ''), `⑲a P${v.p} 图形区矩形声明缺失：${v.rect}`);
    ok(v.ready === '1', `⑲a P${v.p} 场景没建起来（data-lab-ready=${v.ready}）`);
    // poster 组里一个字也不许有；箭头头（方向标注）也必须留在 canvas 之上
    ok(v.posterText === 0, `⑲a P${v.p} poster 层里裹进了 ${v.posterText} 个文字件`);
    ok(v.posterPoly === 0, `⑲a P${v.p} poster 层里裹进了 ${v.posterPoly} 枚箭头头`);
    if (INPAGE.includes(v.p))
      ok(v.posterInPP >= 1, `⑲a P${v.p} 的图形没有原地留作 poster 层`);
  });

  // ── a2 单渲染器巡游的硬红线 ────────────────────────────────────────────
  {
    const one = await pg.evaluate(() => {
      const all = [...document.querySelectorAll('canvas')];
      return { n: all.length, id: all[0] && all[0].id,
        garage: document.querySelectorAll('.lab-garage').length,
        scenes: document.documentElement.dataset.labScenes,
        ready: window.__labReady,
        ctxOK: (() => { try { const c = all[0];
          return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } })() };
    });
    ok(one.n === 1, `⑲a2 全文档 WebGL canvas ${one.n} 枚 —— 单渲染器巡游只准 1 枚`);
    ok(one.id === 'labGl', `⑲a2 canvas id 漂移：${one.id}`);
    ok(one.garage === 1, '⑲a2 缺 canvas 车库 .lab-garage');
    ok(one.ctxOK, '⑲a2 那一枚 canvas 拿不到 WebGL 上下文');
    ok(one.scenes === LAB_PAGES.join(','),
       `⑲a2 场景 registry 页码表漂移：${one.scenes} != ${LAB_PAGES.join(',')}`);
    ok(one.ready === LAB_PAGES.length, `⑲a2 建起来的场景数 ${one.ready} != ${LAB_PAGES.length}`);
    FLAT_PAGES.forEach(p => ok(!LAB_PAGES.includes(p),
      `⑲a2 P${p} 不该有 3D 场景（P7 定稿生态图 —— 既定判断）`));
  }

  // ── a' 生产页不挂常显探针 ───────────────────────────────────────────────
  {
    const hidden = await pg.evaluate(() => {
      const p = document.getElementById('labProbe');
      return { has: !!p, disp: p ? getComputedStyle(p).display : null,
               flag: document.documentElement.hasAttribute('data-lab-debug') };
    });
    ok(hidden.has, '⑲a 缺 FPS 探针节点（?debug=1 时要用它）');
    ok(!hidden.flag, '⑲a 默认 URL 却挂上了 data-lab-debug');
    ok(hidden.disp === 'none', `⑲a 生产页挂了常显 FPS 探针（display=${hidden.disp}）`);
  }

  // ── b 逐页起帧 + 对位 + poster 交接 ────────────────────────────────────
  for (const P of LAB_PAGES) {
    await pg.evaluate(k => window.deck.go(k - 1), P);
    await pg.waitForTimeout(1500);
    const v = await pg.evaluate((k) => {
      const c = document.getElementById('labGl');
      const st = document.querySelector(`.slide[data-p="${k}"] .lab-stage`);
      const r = c.getBoundingClientRect();
      const sc = document.querySelector('.deck-stage').getBoundingClientRect();
      const K = sc.width / 1920;
      return { mode: c.dataset.labMode, run: c.dataset.labRun, dpr: +c.dataset.labDpr,
        page: +c.dataset.labPage, scene: c.dataset.labScene,
        inStage: c.parentNode === st, glup: st.classList.contains('gl-up'),
        want: (st.dataset.labRect || '').split(',').map(Number),
        got: [(r.x - sc.x) / K, (r.y - sc.y) / K, r.width / K, r.height / K],
        posterOp: [...document.querySelectorAll(`.slide[data-p="${k}"] .lab-poster`)]
          .map(e => +getComputedStyle(e).opacity),
        canvasOp: +getComputedStyle(c).opacity, buf: [c.width, c.height] };
    }, P);
    ok(v.mode === 'LIVE', `⑲b P${P} WebGL 未进 LIVE（mode=${v.mode}）`);
    ok(v.run === '1', `⑲b P${P} 渲染循环没跑（run=${v.run}）`);
    ok(v.page === P && v.scene === LAB_SCENES[P], `⑲b P${P} 当前景不对：P${v.page}/${v.scene}`);
    ok(v.inStage, `⑲b P${P} canvas 没搬进该页舞台`);
    ok(v.glup, `⑲b P${P} .lab-stage 没挂 gl-up —— poster 不会让位`);
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

  // ── e 非激活页 ⇒ canvas 回车库、rAF 停 ─────────────────────────────────
  await pg.evaluate(() => document.querySelectorAll('.slide')
    .forEach(el => el.classList.remove('active')));
  await pg.waitForTimeout(900);
  const off = await pg.evaluate(() => {
    const c = document.getElementById('labGl');
    return { run: c.dataset.labRun, mode: c.dataset.labMode, page: c.dataset.labPage,
      parent: c.parentNode.className,
      glup: [...document.querySelectorAll('.lab-stage.gl-up')].length,
      posterBack: [...document.querySelectorAll('.slide[data-p="8"] .lab-poster')]
        .map(e => +getComputedStyle(e).opacity) };
  });
  ok(off.run === '0', `⑲e 无激活页时渲染循环还在跑（run=${off.run}）`);
  ok(off.mode === 'IDLE', `⑲e 无激活页时 mode=${off.mode}（应为 IDLE）`);
  ok(off.parent === 'lab-garage', `⑲e canvas 没回车库（parent=${off.parent}）`);
  ok(off.page === '0', `⑲e 离场后 data-lab-page 没清（=${off.page}）`);
  ok(off.glup === 0, `⑲e 还有 ${off.glup} 枚舞台挂着 gl-up —— 离场必须把 poster 交还回去`);
  ok(off.posterBack.every(o => o > 0.98),
     `⑲e 离场后 P8 的 poster 没回到常驻态（opacity=${off.posterBack}）`);
  await pg.evaluate(() => window.deck.go(0));
  await pg.waitForTimeout(700);

  // ── k 翻页热切换（P4 → P5 · 两枚相邻 3D 页）────────────────────────────
  {
    await pg.evaluate(() => window.deck.go(3));
    await pg.waitForTimeout(1400);
    const a = await pg.evaluate(() => ({ ...window.__labTour, leaves: { ...window.__labTour.leaves },
      cvsPage: +document.getElementById('labGl').dataset.labPage }));
    await pg.evaluate(() => window.deck.go(4));
    await pg.waitForTimeout(1400);
    const b2 = await pg.evaluate(() => ({ ...window.__labTour, leaves: { ...window.__labTour.leaves },
      cvsPage: +document.getElementById('labGl').dataset.labPage,
      p4glup: document.querySelector('.slide[data-p="4"] .lab-stage').classList.contains('gl-up'),
      p5glup: document.querySelector('.slide[data-p="5"] .lab-stage').classList.contains('gl-up'),
      p4poster: [...document.querySelectorAll('.slide[data-p="4"] .lab-poster')]
        .map(e => +getComputedStyle(e).opacity) }));
    ok(a.scene === 'duplex' && a.cvsPage === 4, `⑲k P4 当前景不是 duplex：${a.scene}/${a.cvsPage}`);
    ok(b2.scene === 'brain' && b2.cvsPage === 5, `⑲k P5 当前景没换成 brain：${b2.scene}/${b2.cvsPage}`);
    ok(b2.mounts === a.mounts + 1, `⑲k 场景热切换没发生（mounts ${a.mounts}→${b2.mounts}）`);
    ok((b2.leaves[4] || 0) === (a.leaves[4] || 0) + 1,
       `⑲k 前一景没走 leave（P4 leaves ${a.leaves[4] || 0}→${b2.leaves[4] || 0}）`);
    ok(!b2.p4glup && b2.p5glup, `⑲k gl-up 没跟着搬家（P4=${b2.p4glup} P5=${b2.p5glup}）`);
    ok(b2.p4poster.every(o => o > 0.98),
       `⑲k 离开 P4 后它的 poster 没回来（opacity=${b2.p4poster}）`);
  }

  // ── ⑳clr 净空：两条独立算路对表 + 墨迹名册 × 活 DOM 对表 ─────────────────
  {
    const covers = (b2, g, tol) =>
      g[0] >= b2[0] - tol && g[1] >= b2[1] - tol
      && g[0] + g[2] <= b2[0] + b2[2] + tol && g[1] + g[3] <= b2[1] + b2[3] + tol;
    for (const P of CLR_PAGES) {
      await pg.evaluate(k => window.deck.go(k - 1), P);
      await pg.waitForTimeout(2400);
      const D = await pg.evaluate((k) => {
        const d = document.getElementById('labStage' + k).dataset;
        // 定拍到第 6 秒再量：P5 的大脑绕竖轴 ±12° 摇摆（周期 17s），
        // 不把钟钉住，同一页两次跑会量到两个数。
        const T0 = window.__labTour; T0.pace(30); T0.seek(6);
        const u = window.__labTour.unit();
        const rc = (d.labRect || '').split(',').map(Number);
        const s = document.querySelector(`.slide[data-p="${k}"]`);
        const sc = document.querySelector('.deck-stage').getBoundingClientRect();
        const K = sc.width / 1920, gs = [];
        const w = document.createTreeWalker(s.querySelector('.pp'), NodeFilter.SHOW_TEXT);
        let t;
        while ((t = w.nextNode())) {
          if (!t.textContent.trim()) continue;
          // 细节层（.detail）压在 canvas **之上**，3D 压不到它 ⇒ 不进净空名册。
          // 与 builder 的 _INK 是同一把尺（那边也不登记面板内的字）。
          if (t.parentElement && t.parentElement.closest('.detail')) continue;
          const r = document.createRange(); r.selectNodeContents(t);
          for (const q of r.getClientRects()) {
            if (q.width <= 1 || q.height <= 1) continue;
            const g = [(q.x - sc.x) / K, (q.y - sc.y) / K, q.width / K, q.height / K];
            // 只管落在该页 3D 矩形之内的字（矩形之外的字轮不到 3D 去压）
            if (g[0] + g[2] > rc[0] && g[0] < rc[0] + rc[2]
             && g[1] + g[3] > rc[1] && g[1] < rc[1] + rc[3]) gs.push(g);
          }
        }
        const out = { clr: +d.labClr, clrMin: +d.labClrMin, rect: rc, gs,
          ink: (d.labInk || '').split(';').filter(Boolean).map(r => r.split(',').map(Number)),
          st: u && u.state ? u.state() : null };
        T0.pace(0);
        return out;
      }, P);
      ok(D.ink.length >= 4, `⑳clr P${P} 墨迹名册只有 ${D.ink.length} 只盒`);
      ok(D.st && isFinite(D.st.clr), `⑳clr P${P} 场景没有交出 state().clr`);
      ok(D.st.clr >= D.clr,
         `⑳clr P${P} 的 3D 压字：运行时实测 ${D.st.clr.toFixed(2)}px < 下限 ${D.clr}px`);
      if (CLR_BOUND.includes(P))
        ok(D.st.clr >= D.clrMin - 0.5,
           `⑳clr P${P} 运行时 ${D.st.clr.toFixed(2)}px 掉到构建期外包络 ${D.clrMin}px 之下`
           + '（借来的场景：解析是运行时的下界，掉下去说明包络算漏了几何）');
      else
        ok(Math.abs(D.st.clr - D.clrMin) <= 0.5,
           `⑳clr P${P} 两条算路分叉：构建期解析 ${D.clrMin}px vs 运行时逐顶点 ${D.st.clr.toFixed(2)}px`);
      // 名册 × 活 DOM：矩形内每一处字形行框都得被名册（或已知穿越名册）盖住
      // 已知穿越名册（与 builder 的 _INK_SKIP 逐条同源，改一处两处一起改）
      const SKIP = {
        4: [[1222, 523, 60, 20]],                        // 旗舰 P4 的 3D 声带掠过「收声让位」
        5: [[971, 723, 18, 20], [881, 659, 18, 20], [721, 489, 18, 20],
            [911, 523, 18, 20], [1151, 479, 18, 20]],    // 五枚区序号本来就印在脑体之内
        // P8 那一条（支流3 被 2D 曲线穿过）随「三条支流一条河」一起退役：
        // 新 P8 的 3D 矩形 (120,350,1680,440) 里没有一处页上的字。
      };
      const reg = D.ink.concat(SKIP[P] || []);
      const miss = D.gs.filter(g => !reg.some(b2 => covers(b2, g, 3)));
      ok(miss.length === 0,
         `⑳clr-a P${P} 有 ${miss.length} 处字形行框不在墨迹名册里（首处 ${
           miss[0] && miss[0].map(v => Math.round(v))}）—— 改了文案就得同步那张表`);
      console.log(`  · ⑳clr P${P}（${LAB_SCENES[P]}）：字形 ${D.gs.length} 处 ⊂ 名册 ${
        reg.length} 只 · 净空 ${D.st.clr.toFixed(2)}px（声明 ${D.clrMin} · 下限 ${D.clr}）`);
    }
  }

  /* ── ⑳globe P2 地球的净空（球面场景专用通道）─────────────────────────────
     地球没有 px 投影锁，交不出 state().clr ⇒ 它走这一条：把「弧的外包络圆」
     （心 = data-lab-globe 的球心，半径 = data-lab-genv）拿去逐处量页上的字形行框，
     下限 16px（加法层规则 —— 页上这块地本来没有图）。
     同时与 builder 的解析算路对表（data-lab-clr-min），两头必须给出同一个数。
     ⚠ 跳过 .detail 子树：细节层压在 canvas 之上，3D 压不到它。 */
  {
    await pg.evaluate(() => window.deck.go(1));
    await pg.waitForTimeout(2000);
    const G = await pg.evaluate(() => {
      const d = document.getElementById('labStage2').dataset;
      const gl = (d.labGlobe || '').split(',').map(Number);
      const env = +d.labGenv;
      const s = document.querySelector('.slide[data-p="2"]');
      const sc = document.querySelector('.deck-stage').getBoundingClientRect();
      const K = sc.width / 1920;
      const w = document.createTreeWalker(s.querySelector('.pp'), NodeFilter.SHOW_TEXT);
      let t, worst = 1e9, at = null, n = 0;
      const dist = (b) => {           // 圆心到字形盒的最短距离 − 包络半径
        const dx = Math.max(b[0] - gl[0], 0, gl[0] - (b[0] + b[2]));
        const dy = Math.max(b[1] - gl[1], 0, gl[1] - (b[1] + b[3]));
        return Math.hypot(dx, dy) - env;
      };
      while ((t = w.nextNode())) {
        if (!t.textContent.trim()) continue;
        if (t.parentElement && t.parentElement.closest('.detail')) continue;
        const r = document.createRange(); r.selectNodeContents(t);
        for (const q of r.getClientRects()) {
          if (q.width <= 1 || q.height <= 1) continue;
          const b = [(q.x - sc.x) / K, (q.y - sc.y) / K, q.width / K, q.height / K];
          n++;
          const dd = dist(b);
          if (dd < worst) { worst = dd; at = b.map(v => Math.round(v)); }
        }
      }
      return { gl, env, worst, at, n, clr: +d.labClr, clrMin: +d.labClrMin,
               mode: document.getElementById('labGl').dataset.labMode,
               page: +document.getElementById('labGl').dataset.labPage };
    });
    ok(G.mode === 'LIVE' && G.page === 2, `⑳globe P2 不在 WebGL 态（${G.mode}/${G.page}）`);
    ok(Math.abs(G.env - 312.06) < 0.5, `⑳globe 弧外包络半径 ${G.env} != 312.06`);
    ok(G.gl.length === 3 && G.gl[0] === 1470 && G.gl[1] === 500 && G.gl[2] === 250,
       `⑳globe 球心/半径漂移：[${G.gl}]`);
    ok(G.worst >= G.clr, `⑳globe 地球压字：最近一处字形行框 ${G.worst.toFixed(1)}px `
       + `< 下限 ${G.clr}px（${G.at}）`);
    ok(Math.abs(G.worst - G.clrMin) <= 1.0,
       `⑳globe 两条算路分叉：构建期解析 ${G.clrMin}px vs 活 DOM ${G.worst.toFixed(2)}px`);
    console.log(`  · ⑳globe P2：字形 ${G.n} 处 · 弧外包络 R=${G.env} · 最近净空 `
      + `${G.worst.toFixed(1)}px（声明 ${G.clrMin} · 下限 ${G.clr}）`);
  }

  // ── ⑳chip P4 的 hot 是抽屉 chip：它绝不许被 3D 压 ────────────────────────
  {
    await pg.evaluate(() => window.deck.go(3));
    await pg.waitForTimeout(1000);
    await pg.evaluate(() => document.querySelectorAll('.slide[data-p="4"] [data-step]')
      .forEach(e => e.classList.add('on')));
    await pg.waitForTimeout(400);
    const c = await pg.evaluate(() => {
      const d = document.getElementById('labStage4').dataset;
      const r = (d.labRect || '').split(',').map(Number);
      const sc = document.querySelector('.deck-stage').getBoundingClientRect();
      const K = sc.width / 1920;
      const q = document.getElementById('engineExpand').getBoundingClientRect();
      const g = [(q.x - sc.x) / K, (q.y - sc.y) / K, q.width / K, q.height / K];
      const dx = Math.max(r[0] - (g[0] + g[2]), 0, g[0] - (r[0] + r[2]));
      const dy = Math.max(r[1] - (g[1] + g[3]), 0, g[1] - (r[1] + r[3]));
      return { d: Math.hypot(dx, dy), decl: (d.labChip || ''), lim: +d.labChipclr, g, r };
    });
    ok(c.d >= c.lim, `⑳chip P4 抽屉 chip 距 3D 矩形仅 ${c.d.toFixed(1)}px（下限 ${c.lim}）`);
    const dc = c.decl.split(',').map(Number);
    ok(dc.length === 4 && Math.abs(dc[0] - c.g[0]) < 3 && Math.abs(dc[1] - c.g[1]) < 3,
       `⑳chip 构建期声明的 chip 盒 [${c.decl}] 与活 DOM [${c.g.map(v => v.toFixed(1))}] 分叉`);
    console.log(`  · ⑳chip P4 抽屉 chip 离 3D 矩形 ${c.d.toFixed(0)}px（下限 ${c.lim}）`);
  }

  // ── ⑳spd A 档流速逐股复算 ───────────────────────────────────────────────
  {
    const rows = await pg.evaluate(() => [...document.querySelectorAll('.lab-stage[data-lab-spd]')]
      .map(el => [+el.dataset.labPage, el.dataset.labSpd]));
    const all = [];
    rows.forEach(([p, s2]) => s2.split(';').filter(Boolean)
      .forEach(r => { const i = r.lastIndexOf(','); all.push({ p, nm: r.slice(0, i), v: +r.slice(i + 1) }); }));
    // v3.2：P8 三稿的股数是 **20** —— 14 条核↔内环互动流（一来一回）+ 6 条内环→外环
    //   径向流。全 deck 因此是 3(P3) + 2(P4) + 1(P6) + 20(P8) = 26 股。
    //   ⚠ 星系的 20 股逐股给了**自己的世界速度**（spd_i = 110·Lw/Lp，与 P3 三条主干同法）
    //     ⇒ 波峰在**屏上**一律 110px/s（参考位姿 spin=0），页内极差 1.00×。
    ok(all.length === 26, `⑳spd A 档股数 ${all.length} != 26`);
    ok(rows.length === 4, `⑳spd A 档页数 ${rows.length} != 4（P1 球 / P2 地球 / P5 大脑不是介质，不进表）`);
    ok(all.filter(r => r.p === 8).length === 20, `⑳spd P8 股数 ${all.filter(r => r.p === 8).length} != 20`);
    all.forEach(r => ok(r.v >= 77 && r.v <= 143,
      `⑳spd P${r.p}「${r.nm}」${r.v}px/s 越出 110±30%（77–143）`));
    const lo = Math.min(...all.map(r => r.v)), hi = Math.max(...all.map(r => r.v));
    ok(hi / lo <= 1.5, `⑳spd 全局极差 ${(hi / lo).toFixed(2)}×`);
    rows.forEach(([p, s2]) => {
      const v = s2.split(';').filter(Boolean).map(r => +r.slice(r.lastIndexOf(',') + 1));
      ok(Math.max(...v) / Math.min(...v) <= 1.35,
         `⑳spd P${p} 页内极差 ${(Math.max(...v) / Math.min(...v)).toFixed(2)}×`);
    });
    console.log(`  · ⑳spd A 档：${rows.length} 页 ${all.length} 股 · ${lo}–${hi}px/s`);
  }

  /* ── ⑳galaxy P8「互动星系」的机器面（解出来的，不是调出来的）───────────────
     ⚠ v3.2：本闸接替 ⑳net —— 二稿那张线框示意图（三簇圆环 + 五角星网）整枚退役。
       判据换成星系自己的账：三环点数与半径 / 盘面倾角 / 转速与摇摆 / 弧与流的股数 /
       **生灭窗**（0.4s 内归零再回卷 · 相位表按 (k·塑性数倒数) mod 1 逐条复算 ·
       life(0)=life(1)=0 ⇒ 回卷处零跳变）/ 深度雾贴真实 z 跨度 /
       三处引线落点离环带 ≥16px（构建期扫掠包络实测，qa 只做对表）。 */
  {
    const d = await pg.evaluate(() => {
      const q = document.getElementById('labStage8').dataset;
      const n = (k) => q[k].split(',').map(Number);
      return { scene: q.labScene, lam: +q.labLam, pts: +q.labPts,
               ring: n('labRing'), r: n('labR'), thick: n('labThick'),
               tilt: +q.labTilt, spin: +q.labSpin, sway: +q.labSway, swayP: +q.labSwayP,
               arcs: +q.labArcs, strands: +q.labStrands, flows: n('labFlows'),
               cyc: +q.labCyc, life: n('labLife'), gs: +q.labGs, floor: +q.labFloor,
               qph: n('labQphase'), half: +q.labHalf, zmax: +q.labZmax,
               lead: n('labLead'), leadclr: +q.labLeadclr };
    });
    ok(d.scene === 'galaxy', `⑳galaxy P8 场景名 ${d.scene} != galaxy`);
    ok(Math.abs(d.lam - 232) < 1e-6, `⑳galaxy 波长 ${d.lam} 不是 lab-kit ⑨ 的 232px`);
    // ① 点数：三环合计恰 12,000（与 P5 大脑同一量级）· 两条环带偶数（交错各半）
    ok(d.pts === 12000 && d.ring.reduce((a, b) => a + b, 0) === 12000,
       `⑳galaxy 三环点数 [${d.ring}] 合计 != 12000（声明 ${d.pts}）`);
    ok(d.ring.length === 3 && d.ring[1] % 2 === 0 && d.ring[2] % 2 === 0,
       `⑳galaxy 环带点数不是偶数，人 / 智能体交错分不平：[${d.ring}]`);
    // ② 三环半径严格递增 + 两道净空缝（不然三环在屏上糊成一团）
    ok(d.r.length === 5 && d.r.every((v, i) => i === 0 || v > d.r[i - 1]),
       `⑳galaxy 三环半径不是严格递增：[${d.r}]`);
    ok(d.r[1] - d.r[0] >= 60 && d.r[3] - d.r[2] >= 50,
       `⑳galaxy 环与环之间的净空缝太窄：[${d.r}]`);
    ok(d.thick.length === 2 && d.thick.every(v => v > 0), `⑳galaxy 环带厚度 [${d.thick}] 非正`);
    // ③ 盘面倾角 / 转速 / 轻摇（P5 大脑同款原语 · 零随机源）
    ok(d.tilt === 62, `⑳galaxy 盘面倾角 ${d.tilt}° != 62°`);
    ok(d.spin === 90 && d.sway === 6 && d.swayP === 17,
       `⑳galaxy 转速 / 摇摆漂移：1 圈/${d.spin}s · ±${d.sway}°/${d.swayP}s`);
    // ④ 弧与流的股数
    ok(d.arcs === 24, `⑳galaxy 智能体间弧 ${d.arcs} 条 != 24`);
    ok(d.strands === 20 && d.flows[0] === 14 && d.flows[1] === 6
       && d.flows[0] + d.flows[1] === d.strands,
       `⑳galaxy 流股数 ${d.strands}（${d.flows}）!= 20（14 + 6）`);
    // ⑤ 生灭窗：0.4s 内归零，相位表逐条复算，且两端恰好为 0（回卷零跳变）
    ok(d.cyc === 20, `⑳galaxy 生长周期 ${d.cyc}s != 20s`);
    ok(Math.abs(d.life[0] - 0.4) < 1e-9, `⑳galaxy 灭窗 ${d.life[0]}s != 0.4s`);
    ok(d.floor > 0 && d.floor < 1 && d.gs > 0 && d.gs < 0.5,
       `⑳galaxy 生长锋的地板 ${d.floor} / 软边 ${d.gs} 越界`);
    const PL2 = 0.7548776662;
    ok(d.qph.length === 10, `⑳galaxy 生灭窗相位表长 ${d.qph.length} != 10`);
    d.qph.forEach((v, k) => ok(Math.abs(v - (k * PL2) % 1) < 2e-4,
      `⑳galaxy 生灭窗相位 ${k} 不是 (k·塑性数倒数) mod 1（${v}）`));
    const W0 = d.life[0] / d.cyc, Wb = d.life[1] / d.cyc;
    const ss = (a2, b2, x) => { const t = Math.max(0, Math.min(1, (x - a2) / (b2 - a2)));
                                return t * t * (3 - 2 * t); };
    const life = (u) => ss(0, Wb, u) * (1 - ss(1 - W0, 1, u));
    ok(life(0) === 0 && Math.abs(life(1)) < 1e-12,
       `⑳galaxy 生灭窗的接头不在最暗处（life(0)=${life(0)} life(1)=${life(1)}）`);
    // ⑥ 深度雾贴真实 z 跨度（松了就等于没有体积 —— px 场景唯一的立体线索）
    ok(Math.abs(d.half - d.zmax) <= 6,
       `⑳galaxy 深度雾半程 ${d.half} 没贴住真实 z 跨度 ${d.zmax}`);
    // ⑦ 三处引线落点离环带 ≥16px（构建期扫掠包络实测）
    ok(d.lead.length === 3, `⑳galaxy 引线落点净空表长 ${d.lead.length} != 3`);
    d.lead.forEach((v, k) => ok(v >= d.leadclr,
      `⑳galaxy 第 ${k + 1} 组标注的引线落点离环带只有 ${v}px（下限 ${d.leadclr}）`));
    console.log(`  · ⑳galaxy P8：三环 [${d.ring}] = ${d.pts} 点 · 半径 [${d.r}] · 倾角 ${
      d.tilt}° · 1 圈/${d.spin}s · 摇 ±${d.sway}°/${d.swayP}s · ${d.arcs} 弧 / ${
      d.strands} 股 · 生灭窗 ${d.life[0]}s 归零 · 生长周期 ${d.cyc}s · 引线净空 [${
      d.lead}]px`);
  }

  // ── ⑳flick 消闪：定拍逐帧亮度突变上限（波B 的第一条验收红线）──────────────
  {
    for (const P of LAB_PAGES) {
      await pg.evaluate(k => window.deck.go(k - 1), P);
      await pg.waitForTimeout(1600);
      const fl = await pg.evaluate(() => {
        const T = window.__labTour; T.pace(24);
        let dMean = 0, dBlk = 0, prev = null;
        for (let i = 0; i < 48; i++) {
          T.seek(3 + i / 24);
          const s = T.shot(8, 8);
          if (prev) {
            dMean = Math.max(dMean, Math.abs(s.mean - prev.mean));
            for (let j = 0; j < s.blocks.length; j++)
              dBlk = Math.max(dBlk, Math.abs(s.blocks[j] - prev.blocks[j]));
          }
          prev = s;
        }
        T.pace(0);
        return { dMean, dBlk };
      });
      ok(fl.dMean <= 4.0, `⑳flick P${P} 整幅亮度帧间跳变 ${fl.dMean.toFixed(2)}/255 > 4.0`);
      ok(fl.dBlk <= 26.0, `⑳flick P${P} 8×8 分块亮度帧间跳变 ${fl.dBlk.toFixed(2)}/255 > 26`);
    }
    console.log(`  · ⑳flick 消闪：${LAB_PAGES.length} 页 × 48 帧逐帧亮度突变全部在档内`);
  }
}

/* ═══ ⑰ 面板闸 · 细节层（v3 新机制）══════════════════════════════════════════
   每一枚细节层面板逐条验四件事：
     ① 收起态：面板挂在该页 data-step="1" 上、opacity 0、不吃指针；
     ② chip「细节 ⏎」按下 ⇒ 面板可见（opacity 1 · deck.step=1 · BUILD 指示器亮 1 格）；
     ③ 展开态**不压** land / SOURCE / 页码（三只盒逐一做 AABB 相交判定）；
     ④ Esc 收回；→ 再展开、← 再收回（面板不是另一套开关，就是家族既有的步进）。
   ⚠ ⑳clr 的净空是按面板**收起态**量的（面板压在 canvas 之上，与 3D 压字无关）——
     这一条与 ⑳clr 是两条独立的闸，别混。 */
{
  const hit = (a, b2, tol) =>
    a[0] < b2[0] + b2[2] - tol && a[0] + a[2] > b2[0] + tol
    && a[1] < b2[1] + b2[3] - tol && a[1] + a[3] > b2[1] + tol;
  for (const P of DETAIL_PAGES) {
    await pg.evaluate(() => { document.activeElement?.blur(); });
    await pg.evaluate((k) => { location.hash = '#' + k; }, P);
    await pg.waitForTimeout(1200);
    const R = () => pg.evaluate((k) => {
      const s = document.querySelector(`.slide[data-p="${k}"]`);
      const sc = document.querySelector('.deck-stage').getBoundingClientRect();
      const K = sc.width / 1920;
      const box = (el) => { if (!el) return null; const q = el.getBoundingClientRect();
        return [(q.x - sc.x) / K, (q.y - sc.y) / K, q.width / K, q.height / K]; };
      const d = s.querySelector('.detail');
      const chip = s.querySelector('.chip-detail');
      return {
        has: !!d, n: s.querySelectorAll('.detail').length,
        step: d ? +d.dataset.step : null, on: d ? d.classList.contains('on') : null,
        op: d ? +getComputedStyle(d).opacity : null,
        pe: d ? getComputedStyle(d).pointerEvents : null,
        disp: d ? getComputedStyle(d).display : null,
        panel: box(d), land: box(s.querySelector('.land')),
        src: box(s.querySelector('.src')), sig: box(s.querySelector('.sig')),
        chipVis: chip ? (getComputedStyle(chip).display !== 'none' && +getComputedStyle(chip).opacity > .01) : false,
        chipTxt: chip ? chip.textContent.trim() : null,
        chipBox: box(chip),
        deckStep: window.deck.step, maxStep: window.deck.maxStep[k - 1],
        buildOn: document.getElementById('deckSteps').classList.contains('on'),
      };
    }, P);
    // ① 收起态
    let v = await R();
    ok(v.has && v.n === 1, `⑰ P${P} 细节层面板数 ${v.n} != 1`);
    ok(v.step === 1, `⑰ P${P} 细节层没挂在 data-step="1" 上（=${v.step}）`);
    ok(v.maxStep === 1, `⑰ P${P} deck 认到的分步数 ${v.maxStep} != 1`);
    ok(!v.on && v.op < 0.02, `⑰ P${P} 面板默认没收起（on=${v.on} opacity=${v.op}）`);
    ok(v.pe === 'none', `⑰ P${P} 收起态面板还在吃指针（pointer-events=${v.pe}）`);
    ok(v.chipVis, `⑰ P${P} 细节层入口 chip 不可见`);
    ok(/细节/.test(v.chipTxt || '') && /⏎/.test(v.chipTxt || ''),
       `⑰ P${P} chip 文案不符「${v.chipTxt}」`);
    ok(v.panel[2] <= 760 + 1 && v.panel[3] <= 640 + 1,
       `⑰ P${P} 面板 ${v.panel[2]}×${v.panel[3]} 越过 760×640`);
    // ② chip 按下 ⇒ 展开
    await pg.click(`.slide[data-p="${P}"] .chip-detail`);
    await pg.waitForTimeout(700);
    v = await R();
    ok(v.on && v.op > 0.98, `⑰ P${P} chip 按下后面板没展开（on=${v.on} opacity=${v.op}）`);
    ok(v.deckStep === 1, `⑰ P${P} chip 没走 deck 的第 1 步（step=${v.deckStep}）`);
    ok(v.buildOn, `⑰ P${P} BUILD 指示器没亮`);
    // ③ 展开态不压 land / SOURCE / 页码
    [['land', v.land], ['SOURCE', v.src], ['页码', v.sig]].forEach(([nm, b2]) => {
      if (!b2) return;
      ok(!hit(v.panel, b2, 0.5),
         `⑰ P${P} 展开态面板压住了 ${nm}（面板 [${v.panel.map(x => Math.round(x))}] `
         + `vs [${b2.map(x => Math.round(x))}]）`);
    });
    ok(v.panel[0] >= 0 && v.panel[1] >= 0 && v.panel[0] + v.panel[2] <= 1920
       && v.panel[1] + v.panel[3] <= 1080, `⑰ P${P} 面板出画布 [${v.panel}]`);
    // ④ Esc 收回 → → 再展开 → ← 再收回
    await pg.keyboard.press('Escape');
    await pg.waitForTimeout(500);
    v = await R();
    ok(!v.on && v.deckStep === 0, `⑰ P${P} Esc 没收回面板（on=${v.on} step=${v.deckStep}）`);
    await pg.keyboard.press('ArrowRight');
    await pg.waitForTimeout(500);
    v = await R();
    ok(v.on && v.deckStep === 1, `⑰ P${P} → 没把面板推上来（step=${v.deckStep}）`);
    await pg.keyboard.press('ArrowLeft');
    await pg.waitForTimeout(500);
    v = await R();
    ok(!v.on && v.deckStep === 0, `⑰ P${P} ← 没把面板收回（step=${v.deckStep}）`);
    console.log(`  · ⑰ 面板闸 P${P}：收起/展开/Esc/→/← 五态全过 · 面板 `
      + `${Math.round(v.panel[2])}×${Math.round(v.panel[3])}`);
  }
  // 只有 DETAIL_PAGES 有面板：别的页一枚都不许有
  const stray = await pg.evaluate(() => [...document.querySelectorAll('.slide')]
    .map((s, i) => [i + 1, s.querySelectorAll('.detail').length]).filter(r => r[1]));
  ok(JSON.stringify(stray.map(r => r[0])) === JSON.stringify(DETAIL_PAGES),
     `⑰ 细节层落点漂移：${JSON.stringify(stray)} != ${JSON.stringify(DETAIL_PAGES)}`);
  // print 语域：面板不上纸（按需内容不上纸）
  await pg.emulateMedia({ media: 'print' });
  const pm = await pg.evaluate(() => [...document.querySelectorAll('.detail')]
    .map(e => getComputedStyle(e).display));
  await pg.emulateMedia({ media: 'screen' });
  ok(pm.length === DETAIL_PAGES.length && pm.every(d => d === 'none'), `⑰ print 语域面板没藏（${pm}）`);
}

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

// P4 · Engine 口径（「2026-03 时点」必须在 seclab 与 SOURCE 行两处都留一份）
[['超低延迟、可打断、高自然度', t4], ['2025.02.18 · v1.0 公测', t4], ['2026.08.11 · v2.11 最新', t4],
 ['VS LIVEKIT · 2026-03 同题评测 · 默认配置口径', t4], ['优雅打断 2.0', t4],
 ['2026-03 时点', t4],
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
// ⑫ P5 · 96.5% cohort 标注（2026-08-23 采纳项 B）：三段口径钉死，且必须紧贴大数下方
//    （落在 96.5% 那只 .sh 之下、漏斗 .sh 之上 —— 漏斗与其余内容一格未动）。
ok(t5.includes('生产外呼 · n=2,475 · 未出现明确 AI 识别信号'), '⑫ P5 缺 96.5% cohort 标注');
{
  const geo = await pg.evaluate(() => {
    const s = document.querySelector('.slide[data-p="5"]');
    s.classList.add('active', 'visible');
    const co = [...s.querySelectorAll('.sh')].find(el => /生产外呼 · n=2,475/.test(el.textContent || ''));
    const big = [...s.querySelectorAll('.sh')].find(el => /96\.5%/.test(el.textContent || ''));
    const fun = [...s.querySelectorAll('.sh')].find(el => /2,475 · 100\.0%/.test(el.textContent || ''));
    const R = (el) => el ? { t: Math.round(el.getBoundingClientRect().top),
                             b: Math.round(el.getBoundingClientRect().bottom),
                             l: Math.round(el.getBoundingClientRect().left) } : null;
    return { co: R(co), big: R(big), fun: R(fun) };
  });
  ok(!!geo.co && !!geo.big && !!geo.fun, '⑫ P5 cohort / 大数 / 漏斗 三件定位失败');
  if (geo.co && geo.big && geo.fun) {
    ok(geo.co.t >= geo.big.t, `⑫ P5 cohort 标注跑到 96.5% 上方了（${geo.co.t} < ${geo.big.t}）`);
    ok(geo.co.b <= geo.fun.t + 4, `⑫ P5 cohort 标注压进漏斗（下缘 ${geo.co.b} > 漏斗顶 ${geo.fun.t}）`);
    ok(geo.co.l === geo.big.l, `⑫ P5 cohort 标注未与大数左对齐（${geo.co.l} != ${geo.big.l}）`);
  }
}

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

/* P8 · 使命与愿景（v3.1 重做）：主标 + 使命 / 愿景两句 + 三簇题注 + land，
   加上搬进细节层的三不 / 三步 / OpenAI / DEMO —— 全部逐字。
   ⚠ 使命 / 愿景两句是 2026-09-02 自 shengwang.cn/aboutus 逐字核实的公司口径，
     一个字都不许改；本页除「2014 年起」外不许出现任何年份 / 日期。 */
[['让实时互动，无处不在。', t8],
 ['使命', t8], ['帮助人们跨越距离实时互动，如聚一堂。', t8],
 ['愿景', t8], ['让实时互动像空气和水一样，无处不在。', t8],
 ['人与人 · 已经发生', t8], ['实时音视频 · 2014 年起', t8],
 ['人与智能体 · 正在发生', t8], ['对话式 AI 引擎 · 企业级智能体 · R1', t8],
 ['智能体与智能体 · 即将发生', t8], ['智能体之间的实时对话与协作', t8],
 ['同一张实时网，服务人与人、人与智能体、智能体与智能体。', t8],
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
// ⑭ P8 反向：河退役之后不许有残句回归；「价值观」本轮不上页面（官网未列，二手且旧）
['三条支流，一条河', '三条支流', '一条河', 'ONE NET · SD-RTN 软件定义实时网络',
 'Engine 的每一次打断', 'Agent 的每一次交付', 'Physical AI 的每一次唤醒',
 '合流点', '价值观', '结果导向', '追求卓越']
  .forEach(n => ok(!ALL.includes(n), `⑭ P8 河 / 未核实口径回归：「${n}」`));

// ⑯ SOURCE ledger 统一闸（2026-08-23 采纳项 C）：出处行走同一枚 .src 类、同一套四段格式
//    `SOURCE · 来源 · 样本或时间窗 · 事实截止 2026.08`。
//    P1 封面与 P3 矩阵**没有事实声明** ⇒ 规格上就不带 SOURCE 行（不是遗漏）。
{
  const led = await pg.evaluate(() => [...document.querySelectorAll('.slide')].flatMap((s, i) =>
    [...s.querySelectorAll('.src')].map(el => ({ p: i + 1, t: (el.textContent || '').trim() }))
  ).filter(x => x.t.startsWith('SOURCE')));
  const SRC_PAGES = [2, 4, 5, 6, 7, 8];
  const live = [...new Set(led.map(x => x.p))].sort((a, b) => a - b);
  ok(live.join(',') === SRC_PAGES.join(','),
     `⑯ SOURCE ledger 覆盖漂移：实测 [${live}] != 名册 [${SRC_PAGES}]`);
  ok(led.length === SRC_PAGES.length, `⑯ SOURCE 行数 ${led.length} != ${SRC_PAGES.length}`);
  // 事实截止日**逐页**取该页来源的核实日：P2/P4–P7 是 2026.08；P8 的使命 · 愿景
  // 是 2026-09-02 当天从声网官网逐字核实的 ⇒ 2026.09。名单写死（不许随便新增）。
  const CUTOFF = [' · 事实截止 2026.08', ' · 事实截止 2026.09'];
  led.forEach(({ p, t }) => {
    ok(t.startsWith('SOURCE · '), `⑯ P${p} SOURCE 行不以「SOURCE · 」起手：「${t}」`);
    ok(CUTOFF.some(c => t.endsWith(c)),
       `⑯ P${p} SOURCE 行未以「· 事实截止 2026.08/09」收尾：「${t}」`);
    ok(t.split(' · ').length >= 3, `⑯ P${p} SOURCE 行不足三段：「${t}」`);
  });
  ok(led.filter(x => x.p === 8 && /事实截止 2026\.09$/.test(x.t)).length === 1,
     '⑯ P8 的 SOURCE 行不是「声网官网 关于我们（使命 · 愿景） · 事实截止 2026.09」');
  const stray = await pg.evaluate(() => [...document.querySelectorAll('.slide .mono-sm')]
    .map(el => (el.textContent || '').trim()).filter(t => t.startsWith('SOURCE')));
  ok(stray.length === 0, `⑯ 仍有 SOURCE 行挂在 .mono-sm 上（未并入 ledger）：${stray.join(' | ')}`);
  // 采纳项 G：.src 与 .sig 都必须是提过一档的 17px（两份 deck 一致）
  const sizes = await pg.evaluate(() => ({
    src: getComputedStyle(document.querySelector('.src')).fontSize,
    sig: getComputedStyle(document.querySelector('.sig')).fontSize,
  }));
  ok(sizes.src === '17px', `⑯ .src 字号 ${sizes.src} != 17px（采纳项 G：投影小字提一档）`);
  ok(sizes.sig === '17px', `⑯ .sig 字号 ${sizes.sig} != 17px（采纳项 G：投影小字提一档）`);
}

// ⑭ 红线反向闸：价格 / staging / 引擎 P16 的盲测口径（两个数据集严禁混写）
['¥8,500', '¥2,999', '¥5,501', '8,500', '2,999', '5,501',
 'callagent-landingpage-staging', 'staging', '盲测', '32,000']
  .forEach(n => ok(!ALL.includes(n), `⑭ 红线：8 页宿主出现「${n}」`));

/* ═══════════════════════════════════════════════════════════════════════════
   ⑲/⑳ WebGL 豁免通道 · 独立上下文段
   —— 下面六条各自需要一套不同的浏览器 / 媒体条件，只能另开上下文跑。
   （THEME=dark 二跑时全部跳过：这几条是主题无关层，跑两遍只是浪费三分钟。）
   ═══════════════════════════════════════════════════════════════════════════ */
if (THEME !== 'dark') {
  /* ── c 禁用 WebGL 启动 ⇒ 8 页照常完整可读 ────────────────────────────────
     速讲版的**生命线**：客户会在各种设备上打开。「3D 起不来」不许等于
     「这份 deck 废了」—— 六页退回 poster 静帧（= 页上原来那张 SVG），
     另外两页本来就没有 canvas，一格不受影响。 */
  {
    const b2 = await chromium.launch({ executablePath: CHROME,
      args: ['--disable-webgl', '--disable-webgl2', '--disable-gpu'] });
    const ctx = await b2.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    const pg2 = await ctx.newPage();
    const err2 = [];
    pg2.on('pageerror', e => err2.push('PAGEERROR ' + e.message));
    await pg2.goto(BASE + '/decks/convoai-info.html#1', { waitUntil: 'load', timeout: NAV_MS });
    await pg2.waitForTimeout(7500);                       // 看门狗 6s
    const fb = await pg2.evaluate((pages) => {
      const one = (p) => {
        const st = document.querySelector(`.slide[data-p="${p}"] .lab-stage`);
        const posters = [...document.querySelectorAll(`.slide[data-p="${p}"] .lab-poster`)];
        return { glup: st.classList.contains('gl-up'),
          posterOp: posters.map(e => +getComputedStyle(e).opacity),
          ink: posters.reduce((n, g) =>
            n + g.querySelectorAll('path,rect,circle,line,polygon,ellipse').length, 0),
          // 「降级层里真的有一张图」用**包围盒**判，不用路径字符数：
          // P2 的活动带是「一条轴 + 五枚圆」，d 串本来就只有 12 个字符，
          // 按字符数判会把一张完整的图误判成空壳。
          bw: posters.reduce((m, g) => { try { return Math.max(m, g.getBBox().width); }
                                         catch (e) { return m; } }, 0) };
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
      ok(u.bw > 100, `⑲c 无 WebGL · P${P} 降级层包围盒只有 ${u.bw.toFixed(0)} 单位宽 —— 这一页降不下去`);
    });
    ok(fb.txt.length === N, `⑲c 无 WebGL · 页数 ${fb.txt.length} != ${N}`);
    fb.txt.forEach((n, i) => ok(n >= 20, `⑲c 无 WebGL · P${i + 1} 正文只剩 ${n} 字 —— 这一页读不了了`));
    // 口径锁在降级态里照样在（poster 只换图，不换字）
    ['No.1', '100万+', '900亿+', '50+', '96.5%', '2,475',
     '让实时互动，无处不在。', '帮助人们跨越距离实时互动，如聚一堂。',
     '让实时互动像空气和水一样，无处不在。',
     'IDC 中国视频云市场报告'].forEach(s2 =>
      ok(fb.all.includes(s2), `⑲c 无 WebGL · 全 deck 缺「${s2}」`));
    CASES.forEach(n => ok(fb.all.includes(n), `⑲c 无 WebGL · 案例墙缺「${n}」`));
    ok(err2.length === 0, `⑲c 无 WebGL · pageerror ${err2.length}：${err2.slice(0, 2).join(' | ')}`);
    for (const [pp, name] of [[8, 'info-fallback'], [1, 'info-fallback-p1']]) {
      await pg2.evaluate(k => window.deck.go(k - 1), pp);
      await pg2.waitForTimeout(2600);
      await pg2.screenshot({ path: `${OUT}/${name}.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    }
    await b2.close();
  }

  /* ── d prefers-reduced-motion ⇒ 渲一帧停帧（不是黑屏，也不是继续转）+ f DPR + g print ── */
  {
    const b3 = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
    const ctx = await b3.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1,
      reducedMotion: 'reduce' });
    const pg3 = await ctx.newPage();
    await pg3.goto(BASE + '/decks/convoai-info.html' + HOLD + '#1', { waitUntil: 'load', timeout: NAV_MS });
    await pg3.waitForTimeout(3500);
    const rm = await pg3.evaluate(() => {
      const c = document.getElementById('labGl');
      return { mode: c.dataset.labMode, run: c.dataset.labRun,
               glup: document.getElementById('labStage1').classList.contains('gl-up') };
    });
    ok(rm.mode === 'STILL', `⑲d reduced-motion · mode=${rm.mode}（应为 STILL）`);
    ok(rm.run === '0', '⑲d reduced-motion · rAF 还在跑');
    ok(rm.glup, '⑲d reduced-motion · 应当渲出一帧并让 poster 让位（不是退回 poster）');

    const ctx2 = await b3.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 3 });
    const pg4 = await ctx2.newPage();
    await pg4.goto(BASE + '/decks/convoai-info.html' + HOLD + '#1', { waitUntil: 'load', timeout: NAV_MS });
    await pg4.waitForTimeout(2500);
    const dpr = await pg4.evaluate(() => ({ dpr: +document.getElementById('labGl').dataset.labDpr,
      dev: window.devicePixelRatio }));
    ok(dpr.dev > 2, `⑲f 上下文 devicePixelRatio=${dpr.dev} —— 这条闸没在真正的高 DPR 下跑`);
    ok(dpr.dpr <= 2, `⑲f DPR 未封顶（devicePixelRatio=${dpr.dev} ⇒ 渲染 DPR=${dpr.dpr}）`);

    await pg4.evaluate(() => window.deck.go(0));
    await pg4.waitForTimeout(1200);
    const pr = await pg4.evaluate(() => {
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
      poAll: [...document.querySelectorAll('.lab-poster')].map(e => +getComputedStyle(e).opacity),
      pi: getComputedStyle(document.getElementById('labPrint1')).display,
      probe: getComputedStyle(document.getElementById('labProbe')).display }));
    ok(pm.poAll.every(o => o === 1), `⑲g print · 有 poster 没显（${pm.poAll.filter(o => o !== 1).length} 枚）`);
    ok(pm.cv === 'none', `⑲g print · canvas 没藏（display=${pm.cv}）`);
    ok(pm.pi === 'block', `⑲g print · 打印帧没盖上去（display=${pm.pi}）`);
    ok(pm.probe === 'none', '⑲g print · FPS 探针没藏');
    await pg4.emulateMedia({ media: 'screen' });
    await b3.close();
  }

  /* ── i FPS 自动降级：**不带** ?lab=hold 的默认 URL，软渲染 <20fps ⇒ 2s 内退 poster ── */
  {
    const b4 = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
    const ctx = await b4.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    const pg5 = await ctx.newPage();
    await pg5.goto(BASE + '/decks/convoai-info.html#1', { waitUntil: 'load', timeout: NAV_MS });
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

  /* ── j 双主题 × 逐 3D 页静置帧 + 材质 token 真的分叉 + ⑳ink 浅/暗墨量比 ──────
     浅底走正常混合、暗底走加色混合 ⇒ 浅色中间调天生容易塌。
     同一支尺（TOUR.shot().ink = 该页 3D 层的平均 alpha）逐页量两遍，比值 ≥ 0.90。 */
  {
    const b5 = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
    const tok = {}, ink = {};
    for (const th of ['light', 'dark']) {
      const ctx = await b5.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
      await ctx.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, th);
      const pg6 = await ctx.newPage();
      await pg6.goto(BASE + '/decks/convoai-info.html' + HOLD + '#1', { waitUntil: 'load', timeout: NAV_MS });
      await pg6.waitForTimeout(6500);
      for (const P of LAB_PAGES) {
        await pg6.evaluate(k => window.deck.go(k - 1), P);
        await pg6.waitForTimeout(P === 1 ? 3200 : 2600);
        const st = await pg6.evaluate((k) => {
          const c = document.getElementById('labGl');
          const el = document.querySelector(`.slide[data-p="${k}"] .lab-stage`);
          const T = window.__labTour; T.pace(30); T.seek(6);
          const s = T.shot(4, 4); T.pace(0);
          return { mode: c.dataset.labMode, page: +c.dataset.labPage,
                   rect: (el.dataset.labRect || '').split(',').map(Number), ink: s.ink };
        }, P);
        ok(st.mode === 'LIVE' && st.page === P,
           `⑲j ${th} · P${P} 静置帧不是 WebGL 态（mode=${st.mode} page=${st.page}）`);
        (ink[P] = ink[P] || {})[th] = st.ink;
        await pg6.screenshot({ path: `${OUT}/info-still-p${P}-${th}.png`,
          clip: { x: st.rect[0], y: st.rect[1], width: st.rect[2], height: st.rect[3] } });
      }
      tok[th] = await pg6.evaluate(() => {
        const cs = getComputedStyle(document.documentElement);
        return { vInk: cs.getPropertyValue('--v-ink').trim(),
                 vAdd: cs.getPropertyValue('--v-add').trim(),
                 gOcean: cs.getPropertyValue('--g-ocean').trim(),
                 gHaloAdd: cs.getPropertyValue('--g-halo-add').trim(),
                 dAdd: cs.getPropertyValue('--d-add').trim(),
                 bAdd: cs.getPropertyValue('--b-add').trim(),
                 gxAdd: cs.getPropertyValue('--gx-add').trim(),
                 gxCore: cs.getPropertyValue('--gx-core-op').trim(),
                 vBack: cs.getPropertyValue('--v-back').trim() };
      });
      await ctx.close();
    }
    await b5.close();
    ok(tok.light.vInk !== tok.dark.vInk, `⑲j 声场球点色两主题相同（--v-ink=${tok.light.vInk}）`);
    ok(tok.light.vAdd !== tok.dark.vAdd, '⑲j 混合模式两主题相同（--v-add）');
    ok(tok.light.gOcean !== tok.dark.gOcean, `⑲j 地球海球色两主题相同（--g-ocean=${tok.light.gOcean}）`);
  ok(tok.light.gHaloAdd !== tok.dark.gHaloAdd, '⑲j 地球光晕混合模式两主题相同（--g-halo-add）');
  ok(tok.light.dAdd !== tok.dark.dAdd, '⑲j 双向声带混合模式两主题相同（--d-add）');
  ok(tok.light.bAdd !== tok.dark.bAdd, '⑲j 大脑混合模式两主题相同（--b-add）');
    ok(tok.light.gxAdd !== tok.dark.gxAdd, '⑲j 互动星系混合模式两主题相同（--gx-add）');
    ok(tok.light.gxCore !== tok.dark.gxCore,
       `⑲j 互动星系核墨量两主题相同（--gx-core-op=${tok.light.gxCore}）`);
    const rows = LAB_PAGES.map(P => [P, ink[P].light / ink[P].dark]);
    rows.forEach(([P, r]) => ok(r >= 0.90,
      `⑳ink P${P} 浅/暗墨量比 ${r.toFixed(3)} < 0.90 —— 浅色中间调塌了`));
    console.log('  · ⑳ink 浅/暗墨量比：' + rows.map(([P, r]) => `P${P} ${r.toFixed(2)}`).join(' · '));
    console.log(`  · WebGL 静置帧已出：${OUT}/info-still-p{${LAB_PAGES}}-{light,dark}.png`);
  }
}

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 分步 P2–P8 各 1 步（七页细节层）`
                           + ` · 深链 P4→#1 / P5→#16 / P6→#19`
                           + ` · LAB ${LAB_PAGES.length} 景 ${LAB_PAGES.join('/')} 起帧对位 / 净空两算路 + ⑳globe / A 档 26 股 / 禁 WebGL 8 页可读`);
await b.close();
process.exit(fails.length ? 1 : 0);
