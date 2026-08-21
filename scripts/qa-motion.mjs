// QA · deck 级运动语言（convoai-engine 动效全覆盖轮）
// 逐条验四条硬红线：
//   ① 原语只有五个 + halo 伴件，且每个动效元素都真的挂上了 keyframes（没有拼错的类名）
//   ② 动效元素不携带文字：任何挂了原语类的元素，自身与子树里不得有非空文本节点
//   ③ 非当前页一律 animation-play-state:paused
//   ④ prefers-reduced-motion / print 全关：装饰件 display:none、真几何件 animation:none
//   ⑤ 逐页「保守克制」双闸：**原语种类** ≤ 6（就是全集，防止把新动画偷偷塞进来）+
//      **DOM 运动元素** ≤ 30（防糊满）。注意一件事可能是多个元素：P11 的 25 根包雨是一件事，
//      P6 的 5 段接头包为了恒速各带各的 duration，也是一件事。
// 用法：node scripts/qa-motion.mjs      （BASE 默认 8899）
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8899';
const OK_NAMES = new Set(['moFlow', 'moPulse', 'moBreathe', 'moHalo']);
const SEL = '.mo-packet,.mo-drift,.mo-cycle,.mo-pulse,.mo-breathe,.mo-halo';
const fails = [];
const ok = (c, m) => { if (!c) fails.push(m); };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

async function open(opts = {}) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, ...opts });
  const pg = await ctx.newPage();
  await pg.goto(BASE + '/decks/convoai-engine.html#1', { waitUntil: 'load' });
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
  // ③ 非当前页暂停
  const play = await pg.evaluate((sel) => {
    document.querySelectorAll('.slide').forEach((s, i) => s.classList.toggle('active', i === 7));
    const st = { active: new Set(), other: new Set() };
    document.querySelectorAll('.slide').forEach((s, i) => {
      s.querySelectorAll(sel).forEach(el => {
        (i === 7 ? st.active : st.other).add(getComputedStyle(el).animationPlayState);
      });
    });
    return { active: [...st.active], other: [...st.other] };
  }, SEL);
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

await b.close();
if (fails.length) { console.log('\n✗ FAIL ' + fails.length + '\n' + fails.map(f => '  · ' + f).join('\n')); process.exit(1); }
console.log('\n✓ PASS · 五原语 / 不携带文字 / 非当前页暂停 / reduced-motion + print 全关');
