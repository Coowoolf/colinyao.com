// QA · deck 级运动语言（convoai-engine 动效全覆盖轮）
// 逐条验四条硬红线：
//   ① 原语只有五个 + halo 伴件，且每个动效元素都真的挂上了 keyframes（没有拼错的类名）
//   ② 动效元素不携带文字：任何挂了原语类的元素，自身与子树里不得有非空文本节点
//   ③ 非当前页一律 animation-play-state:paused
//   ④ prefers-reduced-motion / print 全关：装饰件 display:none、真几何件 animation:none
//   ⑥ 运动件名册：哪几页带常驻动效是**声明**出来的，不是随缘的 —— 页序重排（Call Agent 章
//      把 R1 从 P13 搬到 P19）或某页动效被误删，这一闸当场报出来。
//   ⑤ 逐页「保守克制」双闸：**原语种类** ≤ 6（就是全集，防止把新动画偷偷塞进来）+
//      **DOM 运动元素** ≤ 30（防糊满）。注意一件事可能是多个元素：P11 的 25 根包雨是一件事，
//      P6 的 5 段接头包为了恒速各带各的 duration，也是一件事。
// 用法：node scripts/qa-motion.mjs              （引擎 deck · BASE 默认 8899）
//      DECK=info node scripts/qa-motion.mjs    （convoai-info v2 · 8 页）
// 两份 deck 共用同一套原语与同一套纪律 —— 这份脚本只换 URL 与名册，闸门代码一字不分叉。
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8899';
const OK_NAMES = new Set(['moFlow', 'moPulse', 'moBreathe', 'moHalo']);
// ── 运动件名册（**声明**出来的，不是随缘的）──────────────────────────────────
// engine（22 页口径 · 2026-08-21 Call Agent 章 + 视频页）：
//   P2 实时决策 / P3 双工三模式 ◆ / P4 全双工 / P6 语音链路 / P7 VAD / P8 打断 / P9 SAL /
//   P10 大图 / P11 弱网 / P12 多模态 / P13 编排 / P14 接入架构 / P17 大脑五区 ■ / P18 成长飞轮 ■
//   （P8/P9/P10 三页的内容 2026-08-23 轮转过一次，见下）
//   P17（大脑侧视图）是全 deck 动效最重的一页：五区放电脉动 ×5 + 神经火花 ×8 +
//   输出重拍 + hot 盒 breathe/halo + 输入常驻包 = 17 件 / 4 种原语。
//   给它单加一条**下限**闸：低于 12 件就说明「五区一起工作」的编排被改瘦了。
//   2026-08-23 三数章重构 + P3 动效轮，名册两处变化（集合恰好只多了一页 P3）：
//     · **P3 双工三模式入册**（Colin 点名）：两列之间的两条方向通道上跑包 ——
//       单工 1 包（另一向的线画出来但永远无包）/ 半双工 2 包严格互斥 / 全双工 2 包同时在途。
//       它是全 deck 唯一一页「运动模式本身就是定义」的图，所以另加 ⑦ 半双工互斥闸（见下）。
//     · 页序在 6–10 区间轮转（原 8 大图 → 10 / 原 9 打断 → 8 / 原 10 SAL → 9）：
//       名册集合 {8,9,10} 恰好不变，但**每页的内容换了**，所以 floor 逐页跟着内容走 ——
//       P8 打断 4 件 / P9 SAL 11 件 / P10 大图 16 件，任何一页被搬错都会掉到下限之下。
//   不入册：P1 封面 · P5 三件极致 · P15 场景 · P16 成绩单 ·
//           P19 R1 实拍 · P20 视频页 · P21 Why Agora · P22 OpenAI 末页
// info（8 页 · 2026-08-21 家族语言重建轮）：
//   P2 时间线活动带 + No.1 hot 环 / P3 三主干 + 底座 hot / P4 版本活动带 + 抽屉 chip hot /
//   P5 Agent 骨架图（四路供给 + 安全域）+ 96.5% hot / P6 R1 实拍图组 hot ×2 /
//   P7 生态五层域分带 + L2 hot 标记 / P8 三支流合流（本 deck 标杆页）
//   不入册：P1 封面（引擎 P1 同例 —— 会动的封面只会抢主标）
const DECKS = {
  engine: { url: '/decks/convoai-engine.html',
            roster: [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18],
            floor: { 3: 4, 8: 4, 9: 11, 10: 16, 17: 12 }, pauseProbe: 7 },
  info:   { url: '/decks/convoai-info.html', roster: [2, 3, 4, 5, 6, 7, 8],
            floor: { 8: 6 }, pauseProbe: 7 },
};
const DECK = DECKS[process.env.DECK || 'engine'];
if (!DECK) { console.log('未知 DECK：' + process.env.DECK); process.exit(1); }
const ROSTER = DECK.roster;
const FLOOR = DECK.floor;      // 指定页的运动件下限（点名，别泛化成全表配额）
const SEL = '.mo-packet,.mo-drift,.mo-cycle,.mo-pulse,.mo-breathe,.mo-halo';
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

async function open(opts = {}) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, ...opts });
  const pg = await ctx.newPage();
  await pg.goto(BASE + DECK.url + '#1', { waitUntil: 'load' });
  await pg.waitForTimeout(500);
  return { ctx, pg };
}

// ── ①②⑤ 常态 ──
{
  const { ctx, pg } = await open();
  const r = await pg.evaluate((sel) => {
    const out = { perPage: {}, perPageEl: {}, badName: [], withText: [], noAnim: [] };
    document.querySelectorAll('.slide').forEach((s, i) => {
      const els = [...s.querySelectorAll(sel)];
      const kinds = new Set();
      els.forEach((el) => [...el.classList].filter(c => c.startsWith('mo-')).forEach(c => kinds.add(c)));
      if (els.length) { out.perPage[i + 1] = kinds.size; out.perPageEl[i + 1] = els.length; }
      for (const el of els) {
        const cs = getComputedStyle(el);
        const name = cs.animationName;
        if (name === 'none') { out.noAnim.push(`P${i + 1} ${el.getAttribute('class')}`); continue; }
        name.split(',').map(s => s.trim()).forEach(n => out.badName.push(`P${i + 1}:${n}`));
        const t = (el.textContent || '').replace(/\s+/g, '');
        // ✕ 这一枚是符号标记不是文字（P10/P11 的命中标），单独放行
        if (t && t !== '✕') out.withText.push(`P${i + 1} 「${t.slice(0, 12)}」`);
      }
    });
    return out;
  }, SEL);
  Object.entries(r.perPage).forEach(([p, n]) => {
    ok(n <= 6, `⑤ P${p} 用了 ${n} 种原语 —— 超出原语全集（6）`);
    ok(r.perPageEl[p] <= 30, `⑤ P${p} 运动 DOM 元素 ${r.perPageEl[p]} 个 —— 糊满了`);
  });
  r.badName.forEach(n => ok(OK_NAMES.has(n.split(':')[1]), `① 非原语 keyframes：${n}`));
  ok(r.noAnim.length === 0, `① 挂了原语类却没动画（类名拼错？）：${r.noAnim.join(' / ')}`);
  ok(r.withText.length === 0, `② 动效元素携带文字：${r.withText.join(' / ')}`);
  console.log('· 逐页运动件（原语种类 / DOM 元素）：'
    + Object.entries(r.perPage).map(([p, n]) => `P${p}:${n}/${r.perPageEl[p]}`).join(' '));
  // ⑥ 名册比对：多一页少一页都算漂移（新页忘挂动效 / 老页动效被误删 / 页序重排没同步）
  const live = Object.keys(r.perPage).map(Number).sort((a, b) => a - b);
  ok(live.join(',') === ROSTER.join(','),
     `⑥ 运动件名册漂移：实测 [${live}] != 名册 [${ROSTER}]`);
  Object.entries(FLOOR).forEach(([p, n]) => ok((r.perPageEl[p] || 0) >= n,
    `⑥ P${p} 运动件只剩 ${r.perPageEl[p] || 0} 个（下限 ${n}）—— 编排被改瘦了`));
  // ③ 非当前页暂停
  const play = await pg.evaluate(({ sel, probe }) => {
    document.querySelectorAll('.slide').forEach((s, i) => s.classList.toggle('active', i === probe));
    const st = { active: new Set(), other: new Set() };
    document.querySelectorAll('.slide').forEach((s, i) => {
      s.querySelectorAll(sel).forEach(el => {
        (i === probe ? st.active : st.other).add(getComputedStyle(el).animationPlayState);
      });
    });
    return { active: [...st.active], other: [...st.other] };
  }, { sel: SEL, probe: DECK.pauseProbe });
  ok(play.active.every(v => v === 'running'), `③ 当前页动画未在跑：${play.active}`);
  ok(play.other.every(v => v === 'paused'), `③ 非当前页动画未暂停：${play.other}`);
  console.log(`· play-state 当前页=${play.active} 非当前页=${play.other}`);
  await ctx.close();
}

// ── ④ reduced-motion ──
{
  const { ctx, pg } = await open({ reducedMotion: 'reduce' });
  const r = await pg.evaluate((sel) => {
    const out = { ghostShown: [], animOn: [] };
    document.querySelectorAll('.slide').forEach((s, i) => {
      s.classList.add('active');
      s.querySelectorAll(sel).forEach(el => {
        const cs = getComputedStyle(el);
        const deco = el.classList.contains('mo-packet') || el.classList.contains('mo-halo');
        if (deco && cs.display !== 'none') out.ghostShown.push(`P${i + 1}`);
        if (!deco && cs.animationName !== 'none') out.animOn.push(`P${i + 1}:${cs.animationName}`);
      });
    });
    return out;
  }, SEL);
  ok(r.ghostShown.length === 0, `④ reduced-motion 下装饰件仍显示：${[...new Set(r.ghostShown)]}`);
  ok(r.animOn.length === 0, `④ reduced-motion 下动画未关：${[...new Set(r.animOn)]}`);
  console.log('· reduced-motion：装饰件全隐、真几何件 animation:none');
  await ctx.close();
}

// ── ④ print ──
{
  const { ctx, pg } = await open();
  await pg.emulateMedia({ media: 'print' });
  const r = await pg.evaluate((sel) => {
    const out = { ghostShown: [], animOn: [] };
    document.querySelectorAll('.slide').forEach((s, i) => {
      s.querySelectorAll(sel).forEach(el => {
        const cs = getComputedStyle(el);
        const deco = el.classList.contains('mo-packet') || el.classList.contains('mo-halo');
        if (deco && cs.display !== 'none') out.ghostShown.push(`P${i + 1}`);
        if (!deco && cs.animationName !== 'none') out.animOn.push(`P${i + 1}:${cs.animationName}`);
      });
    });
    return out;
  }, SEL);
  ok(r.ghostShown.length === 0, `④ print 下装饰件仍显示：${[...new Set(r.ghostShown)]}`);
  ok(r.animOn.length === 0, `④ print 下动画未关：${[...new Set(r.animOn)]}`);
  console.log('· print：装饰件全隐、真几何件 animation:none');
  await ctx.close();
}

// ── ⑦ P3 半双工「两个方向不得同时在途」闸（2026-08-23 · engine 专属）────────────
//    这一条是**静态复算**，不靠截帧：包在途与否完全由四个参数决定 ——
//      路径长 L（getTotalLength）/ 包长 seg 与空挡 gap（stroke-dasharray）/
//      周期 D（animation-duration）/ 相位 δ（animation-delay，可为负）。
//    dashoffset 在一个周期里线性走满 per = seg + gap，包占据路径位置 [d, d+seg]（d = 进度×per），
//    因此「包与路径有交集」的进度窗口是 d ∈ (per−seg, per] ∪ [0, L) —— 一段长 L+seg 的环形区间，
//    起点 per−seg。换算成时间：起点 = D·(per−seg)/per + δ，长度 = D·(L+seg)/per（均对 D 取模）。
//    两枚包同周期时，只要两段环形区间互不相交，就证明**任何时刻至多一个方向有包在途**。
//    设计侧的保证是「占空比 (L+seg)/per = 1/3 < 1/2 且相位差半个周期」；这一闸只管验，不管信。
if ((process.env.DECK || 'engine') === 'engine') {
  const { ctx, pg } = await open();
  const r = await pg.evaluate(() => {
    const read = (cls) => [...document.querySelectorAll(`.slide[data-p="3"] .${cls}`)].map((el) => {
      const cs = getComputedStyle(el);
      const sec = (v) => parseFloat(v) * (/ms$/.test(v.trim()) ? 0.001 : 1);
      const da = cs.strokeDasharray.split(/[\s,]+/).filter(Boolean).map(parseFloat);
      return { L: el.getTotalLength(), seg: da[0], gap: da[1],
               D: sec(cs.animationDuration), del: sec(cs.animationDelay) };
    });
    return { simplex: read('duplex-simplex'), half: read('duplex-half'), full: read('duplex-full') };
  });
  ok(r.simplex.length === 1, `⑦ P3 单工包数 ${r.simplex.length} != 1`);
  ok(r.half.length === 2, `⑦ P3 半双工包数 ${r.half.length} != 2`);
  ok(r.full.length === 2, `⑦ P3 全双工包数 ${r.full.length} != 2`);
  if (r.half.length === 2) {
    const D = r.half[0].D;
    ok(Math.abs(r.half[1].D - D) < 1e-6,
       `⑦ 半双工两包周期不同（${r.half[0].D}s / ${r.half[1].D}s）—— 互斥无法用同一周期证明`);
    const win = r.half.map(({ L, seg, gap, D: d, del }) => {
      const per = seg + gap, len = d * (L + seg) / per;
      const start = (((d * (per - seg) / per + del) % d) + d) % d;
      return { start, len, duty: (L + seg) / per };
    });
    win.forEach((w, i) => ok(w.duty < 0.5,
      `⑦ 半双工包 ${i + 1} 占空比 ${w.duty.toFixed(3)} ≥ 0.5 —— 相位再错也躲不开重叠`));
    const gapFwd = (((win[1].start - win[0].start) % D) + D) % D;
    const gapBwd = (((win[0].start - win[1].start) % D) + D) % D;
    const m1 = gapFwd - win[0].len, m2 = gapBwd - win[1].len;
    ok(m1 > 0 && m2 > 0,
       `⑦ 半双工两向同时在途（互斥破了）：窗口 A [${win[0].start.toFixed(2)}, +${win[0].len.toFixed(2)}] `
       + `／ B [${win[1].start.toFixed(2)}, +${win[1].len.toFixed(2)}]，周期 ${D}s，间隙 ${m1.toFixed(2)}/${m2.toFixed(2)}s`);
    console.log(`· P3 半双工互斥：周期 ${D}s · 占空比 ${win[0].duty.toFixed(3)} · `
      + `静默间隙 ${m1.toFixed(2)}s / ${m2.toFixed(2)}s`);
  }
  // 全双工：两包必须**同时**在途（占空比各 100% ⇒ 无论相位如何都恒重叠）
  r.full.forEach((f, i) => ok((f.L + f.seg) / (f.seg + f.gap) > 0.98,
    `⑦ 全双工包 ${i + 1} 占空比 ${(((f.L + f.seg) / (f.seg + f.gap))).toFixed(3)} —— 「同时在途」不成立`));
  // 单工：B→A 方向永远无包 —— 那条线在 DOM 里是虚线 .pop（不带 .mo-packet）
  const back = await pg.evaluate(() => [...document.querySelectorAll('.slide[data-p="3"] .mo-packet')]
    .map(el => el.getAttribute('d')));
  ok(back.filter(d => /^M194 62/.test(d)).length === 1, '⑦ 单工 A→B 通道上没有包');
  ok(back.filter(d => /^M26[0-9] 10[0-9]/.test(d)).length === 0,
     '⑦ 单工的静默方向上出现了包 —— 单工就不成其为单工了');
  await ctx.close();
}

await b.close();
if (fails.length) { console.log('\n✗ FAIL ' + fails.length + '\n' + fails.map(f => '  · ' + f).join('\n')); process.exit(1); }
console.log(`\n✓ PASS · ${process.env.DECK || 'engine'} · 五原语 / 不携带文字 / 非当前页暂停 / reduced-motion + print 全关`);
