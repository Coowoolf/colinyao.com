// QA · convoai-info 一页一章 Infograph 速讲版（8 页 · CONF 家族 · 双主题 · 全页 data-steps=0）
// 从 qa-convoai.mjs 改：N=8 / EXP_STEPS 全 0 / BOARD 只有 title+content / hero 只 P1 /
// ⑧ 步进检查删掉（这份 deck 没有任何分步），⑦ 双源改查 hero-art 的 lt·dk 互斥。
// 视觉升级 R1（2026-08-13）加两条：
//   ⑨ P1 hero 盒 left+width ≤ 1920（原 860+1200=2060 把图右侧顶出画布，防回归）
//   ⑩ P7 .eco-art 双源可见性与主题（和 ⑤ 的 hero-art 断言同一写法）
// 用法：node scripts/qa-convoai-info.mjs        （THEME=dark 二跑）
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const N = 8;
const EXP_STEPS = [0, 0, 0, 0, 0, 0, 0, 0];
const BOARD = { 1: 'title' };            // 其余一律 content
const HERO = { 1: 'hero-cover-v2' };     // hero-art 只上封面
const ECO = { 7: 'eco-panorama-v2' };    // eco-art 只上 P7 生态全景
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
await pg.goto('http://localhost:8777/decks/convoai-info.html#1', { waitUntil: 'load' });
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

// ② 分步数：速讲版必须全 0，且页内不许残留任何 data-step
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => +s.dataset.steps));
EXP_STEPS.forEach((e, i) => ok(steps[i] === e, `② P${i + 1} steps ${steps[i]} != ${e}`));
const stray = await pg.evaluate(() => [...document.querySelectorAll('.slide')]
  .map((s, i) => [i + 1, s.querySelectorAll('[data-step]').length]).filter(([, n]) => n));
stray.forEach(([p, n]) => fails.push(`② P${p} 残留 data-step ×${n}（速讲版不许分步）`));

// ③④⑤⑥ 逐页：板、hero、图、溢出（画布溢出 + 卡内溢出）
for (let i = 1; i <= N; i++) {
  const r = await pg.evaluate((n) => {
    document.querySelectorAll('.slide').forEach((el, k) => {
      el.classList.toggle('active', k === n - 1); el.classList.toggle('visible', k === n - 1);
    });
    const s = document.querySelectorAll('.slide')[n - 1];
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
    // 溢出：sh 内容不出画布；卡片内容不冲出卡底
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
    // ⑨ 出画布回归闸：两个源盒都要 left+width ≤ 1920 且 top+height ≤ 1080
    r.heroes.forEach((h) => {
      ok(Number.isFinite(h.box.l) && Number.isFinite(h.box.w), `⑨ P${i} hero 盒缺 left/width`);
      ok(h.box.l + h.box.w <= 1920, `⑨ P${i} hero 出画布 left+width=${h.box.l + h.box.w} > 1920`);
      ok(h.box.t + h.box.h <= 1080, `⑨ P${i} hero 出画布 top+height=${h.box.t + h.box.h} > 1080`);
    });
  } else {
    ok(r.heroes.length === 0, `⑤ P${i} 不应有 hero`);
  }
  // ⑩ P7 生态全景双源（写法照 ⑤ 的 hero-art：数 2 · 可见 1 · 主题类对 · 真加载）
  if (ECO[i]) {
    ok(r.ecos.length === 2, `⑩ P${i} eco-art 数 ${r.ecos.length}`);
    const ev = r.ecos.filter(e => e.vis);
    ok(ev.length === 1, `⑩ P${i} eco-art 可见数 ${ev.length}`);
    if (ev[0]) {
      ok(ev[0].cls.includes(THEME === 'dark' ? 'dk' : 'lt'), `⑩ P${i} eco-art 主题错 ${ev[0].cls}`);
      ok(ev[0].src.includes(`${ECO[i]}-${THEME}.webp`), `⑩ P${i} eco-art 源不符 ${ev[0].src}`);
      ok(ev[0].w === 2048, `⑩ P${i} eco-art 未加载`);
      ok(ev[0].fit === 'cover', `⑩ P${i} eco-art fit=${ev[0].fit}`);
    }
  } else {
    ok(r.ecos.length === 0, `⑩ P${i} 不应有 eco-art`);
  }
  ok(r.badImgs.length === 0, `⑥ P${i} 图未加载 ${r.badImgs.join()}`);
  [...new Set(r.out)].forEach(o => fails.push(`③ P${i} 溢出 ${o}`));
  await pg.waitForTimeout(60);
}

// ⑦ 主题切换：deckSwap 按钮真实切换（板源 + hero-art 双源）
await pg.evaluate(() => {
  window.deck.i = 0;
  document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === 0));
});
await pg.click('#deckSwap');
await pg.waitForTimeout(400);
const sw = await pg.evaluate(() => {
  const s = document.querySelectorAll('.slide')[0];
  const p7 = document.querySelectorAll('.slide')[6];
  // 少一个源就返回 'MISSING'，让它落成一条 fail —— 别在 getComputedStyle(null) 上炸栈
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
ok(flipped === 'dark' ? (sw.lt === 'none' && sw.dk === 'block') : (sw.dk === 'none' && sw.lt === 'block'),
   `⑦ hero 双源 ${sw.lt}/${sw.dk}`);
// ⑩ eco-art 与 hero-art 同机制（纯 CSS 控可见性）：deckSwap 之后也必须跟着翻
ok(flipped === 'dark' ? (sw.elt === 'none' && sw.edk === 'block') : (sw.edk === 'none' && sw.elt === 'block'),
   `⑩ 切换后 eco 双源 ${sw.elt}/${sw.edk}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n')
                         : `✓ PASS ${THEME} · ${N} 页全绿 · 全页 data-steps=0`);
await b.close();
process.exit(fails.length ? 1 : 0);
