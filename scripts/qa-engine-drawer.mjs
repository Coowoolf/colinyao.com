// 抽屉实测 · convoai-info P4 → Enter → 引擎 deck iframe
// 断言：
//   ① iframe 内 .pp / section 数 == 22；iframe 内 html[data-theme] 与宿主一致（浅浅 / 深深各一组）
//   ② 主题实时联动（2026-08-20 新增）：抽屉开着时点宿主的 deckSwap，
//      iframe 的 data-theme 必须跟着翻（不是只在首帧读一次 localStorage）
//   ②b 反向联动（2026-08-23 采纳项 A · 双向）：抽屉开着时点 **iframe 里那枚 deckSwap**，
//      宿主的 html[data-theme] 与 deckSwap 文案必须跟着翻。通路是「同源 iframe 写
//      localStorage → 宿主 window 收到 storage 事件」，所以只能点按钮触发，
//      调 __setTheme 不写 localStorage、测不到这条通路。
//   ③ eo-close 收回按钮在左上（避让 iframe 右上角的页码 sig）
// 2026-08-20：引擎 deck 二轮扩页 16 → 17（VAD 之后插入产品架构大图）
// 2026-08-21：大内容轮 17 → 20（SAL / 弱网 / 多模态重做 + Physical AI 两页 + OpenAI 一页）
// 2026-08-21 收束轮：20 → 18（删案例墙与旧收尾页，OpenAI 合作升为末页）。
// 2026-08-21 Call Agent 章：18 → 21（新增 Call Agent 三页 + 场景 → Call Agent → R1 重排）。
// 2026-08-21 视频页：21 → 22（R1 之后插 robot26 #24 同款全屏视频页）。
//   同轮引擎 deck 的 deckSwap 改成常显 chip —— 抽屉里它也跟着可见，
//   这是预期行为（抽屉里能切主题合理），主题实时联动逻辑不变，② 仍逐条验。
// 用法：node scripts/qa-engine-drawer.mjs        （BASE 默认 8777）
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8777';
const N = 22;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const fails = [];
for (const theme of ['light', 'dark']) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } });
  if (theme === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const pg = await ctx.newPage();
  await pg.goto(BASE + '/decks/convoai-info.html#4', { waitUntil: 'load' });
  await pg.waitForTimeout(2400);            // 等 P4 整页入场走完（.rise --i:4 ≈ 1.2s）
  await pg.evaluate(() => document.activeElement?.blur());
  // P4 现在有一步 build：先把 04 · OPEN 那行（含 #engineExpand）推上来，再按 Enter
  await pg.keyboard.press('ArrowRight');
  await pg.waitForTimeout(800);
  await pg.keyboard.press('Enter');
  await pg.waitForTimeout(300);
  const opened = await pg.evaluate(() => document.getElementById('engineOverlay').hidden === false);
  if (!opened) { fails.push(`[${theme}] Enter 未展开 overlay`); await ctx.close(); continue; }
  const r = await pg.waitForFunction((n) => {
    const f = document.getElementById('engineFrame'), d = f && f.contentDocument;
    if (!(d && d.readyState === 'complete' && d.querySelectorAll('.pp').length)) return false;
    const cb = document.querySelector('#engineOverlay .eo-close');
    const cs = cb && getComputedStyle(cb);
    const cr = cb && cb.getBoundingClientRect();
    return {
      pp: d.querySelectorAll('.pp').length,
      sec: d.querySelectorAll('section').length,
      inner: d.documentElement.getAttribute('data-theme'),
      host: document.documentElement.getAttribute('data-theme'),
      title: d.title,
      sigLast: d.querySelector(`.slide[data-p="${n}"] .sig`)?.textContent,
      close: cs ? { left: cs.left, top: cs.top, cx: Math.round(cr.left + cr.width / 2) } : null,
    };
  }, N, { timeout: 10000 }).then(h => h.jsonValue()).catch(() => null);
  if (!r) { fails.push(`[${theme}] iframe 未就绪`); await ctx.close(); continue; }
  const want = theme === 'dark' ? 'dark' : null;
  if (r.pp !== N) fails.push(`[${theme}] iframe .pp 数 ${r.pp} != ${N}`);
  if (r.sec !== N) fails.push(`[${theme}] iframe section 数 ${r.sec} != ${N}`);
  if ((r.host || null) !== want) fails.push(`[${theme}] 宿主主题 ${r.host} != ${want}`);
  if ((r.inner || null) !== want) fails.push(`[${theme}] iframe 主题 ${r.inner} != ${want}（未跟随宿主）`);
  if (r.inner !== r.host) fails.push(`[${theme}] iframe 与宿主主题不一致 ${r.inner} / ${r.host}`);
  if (r.title !== '声网 · 对话式 AI 引擎 · 深入讲解') fails.push(`[${theme}] iframe title「${r.title}」`);
  if (r.sigLast !== `${N}/${N}`) fails.push(`[${theme}] iframe P${N} sig「${r.sigLast}」!= ${N}/${N}`);
  // ③ eo-close 在左上：视口左半边（右上角留给 iframe 内的页码 sig）
  if (!r.close || r.close.left === 'auto' || r.close.cx > 960) {
    fails.push(`[${theme}] eo-close 不在左上 ${JSON.stringify(r.close)}`);
  }

  // ② 主题实时联动：抽屉开着 → 触发宿主 deckSwap → iframe 必须跟着翻
  //    注意：overlay（z 10002）盖住了 .deck-swap（z 1100），真人此刻点不到它 ——
  //    坐标点击会命中 scrim 直接把抽屉关掉。这里直接派发按钮自身的 click，
  //    验的是「宿主主题一变、iframe 立刻跟随」这条通路本身（openDrawer 也走同一条）。
  await pg.evaluate(() => document.getElementById('deckSwap').click());
  const flipped = theme === 'dark' ? null : 'dark';
  const live = await pg.waitForFunction((exp) => {
    const d = document.getElementById('engineFrame').contentDocument;
    const inner = d.documentElement.getAttribute('data-theme');
    const host = document.documentElement.getAttribute('data-theme');
    if ((host || null) !== exp || (inner || null) !== exp) return false;
    let ls = null; try { ls = d.defaultView.localStorage.getItem('colin-theme'); } catch (e) {}
    return { inner, host, ls, label: d.getElementById('deckSwap')?.textContent };
  }, flipped, { timeout: 5000 }).then(h => h.jsonValue()).catch(() => null);
  if (!live) {
    const now = await pg.evaluate(() => ({
      host: document.documentElement.getAttribute('data-theme'),
      inner: document.getElementById('engineFrame').contentDocument.documentElement.getAttribute('data-theme'),
    }));
    fails.push(`[${theme}] 主题实时联动失败：宿主翻到 ${flipped}，实测 host=${now.host} iframe=${now.inner}`);
  } else {
    const wantLs = flipped === 'dark' ? 'dark' : 'light';
    if (live.ls !== wantLs) fails.push(`[${theme}] iframe localStorage 未同步（${live.ls} != ${wantLs}）`);
    const wantLabel = flipped === 'dark' ? '浅底' : '暗底';
    if (live.label !== wantLabel) fails.push(`[${theme}] iframe deckSwap 文案未同步（${live.label} != ${wantLabel}）`);
    console.log(`· ${theme} → host→iframe 实时联动：宿主=${live.host || 'light'} iframe=${live.inner || 'light'} ls=${live.ls}`);
  }

  // ②b 反向联动 iframe → 宿主（2026-08-23 采纳项 A）：抽屉开着时点 **iframe 里那枚
  //     deckSwap**，宿主的 html[data-theme] 与 deckSwap 文案必须跟着翻。
  //     必须点它自己的按钮而不是调 __setTheme —— 只有按钮会写 localStorage，
  //     而反向通路正是靠同源 iframe 写 localStorage 在宿主触发的 storage 事件。
  //     此刻宿主是 flipped 态（上一段刚翻过），再点一次应当翻回 theme 起始态。
  {
    const clicked = await pg.evaluate(() => {
      const d = document.getElementById('engineFrame').contentDocument;
      const b = d.getElementById('deckSwap');
      if (!b) return false;
      b.click();
      return true;
    });
    if (!clicked) fails.push(`[${theme}] iframe 内找不到 deckSwap（反向联动无从触发）`);
    else {
      const back = theme === 'dark' ? 'dark' : null;   // 翻回本轮起始主题
      const rev = await pg.waitForFunction((exp) => {
        const host = document.documentElement.getAttribute('data-theme');
        const d = document.getElementById('engineFrame').contentDocument;
        const inner = d.documentElement.getAttribute('data-theme');
        if ((host || null) !== exp) return false;
        return { host, inner, label: document.getElementById('deckSwap')?.textContent };
      }, back, { timeout: 5000 }).then(h => h.jsonValue()).catch(() => null);
      if (!rev) {
        const now = await pg.evaluate(() => ({
          host: document.documentElement.getAttribute('data-theme'),
          inner: document.getElementById('engineFrame').contentDocument.documentElement.getAttribute('data-theme'),
        }));
        fails.push(`[${theme}] 反向联动失败：iframe 翻到 ${back}，宿主仍是 ${now.host}（iframe=${now.inner}）`);
      } else {
        if ((rev.inner || null) !== back) fails.push(`[${theme}] 反向联动后 iframe 自身主题 ${rev.inner} != ${back}`);
        const wantLabel = back === 'dark' ? '浅底' : '暗底';
        if (rev.label !== wantLabel) fails.push(`[${theme}] 反向联动后宿主 deckSwap 文案未同步（${rev.label} != ${wantLabel}）`);
        console.log(`· ${theme} → iframe→host 反向联动：iframe=${rev.inner || 'light'} 宿主=${rev.host || 'light'} 宿主键文案=${rev.label}`);
      }
    }
  }

  console.log(`· ${theme}：.pp=${r.pp} section=${r.sec} 宿主=${r.host || 'light'} iframe=${r.inner || 'light'} sigLast=${r.sigLast} close.left=${r.close && r.close.left}`);
  await ctx.close();
}
await b.close();
console.log(fails.length ? '✗ FAIL\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS · 抽屉两组主题均跟随宿主 + 双向实时联动（host↔iframe）· iframe ${N} 页 · eo-close 左上`);
process.exit(fails.length ? 1 : 0);
