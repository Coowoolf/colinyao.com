// QA · convoai 初次拜访 deck（31 页 · CONF 家族 · 双主题 · hero-art 层）
import { chromium } from 'playwright-core';
const THEME = process.env.THEME || 'light';
const EXP_STEPS = [0,1,1,1,2, 2,3,1, 0,1,1,0,1, 0,1,2,1,1, 0,4,1,1, 1,0,0,0, 1,1,1, 0,0];
const BOARD = {1:'title',4:'quote',8:'quote',9:'ch-eng',14:'ch-agent',19:'ch-phys',29:'quote',31:'title'};
const HERO = {1:'three-engines',7:'three-engines',9:'engine-core',14:'agent-call',19:'physical-family',27:'network-globe'};
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
await pg.goto('http://localhost:8777/decks/convoai-visit.html#1', { waitUntil: 'load' });
await pg.waitForTimeout(900);

// ① 页数 + noindex + sig
const meta = await pg.evaluate(() => ({
  n: document.querySelectorAll('.slide').length,
  noindex: !!document.querySelector('meta[name="robots"][content*="noindex"]'),
  sigs: [...document.querySelectorAll('.slide .sig')].map(s => s.textContent),
  theme: document.documentElement.getAttribute('data-theme'),
}));
ok(meta.n === 31, `① 页数 ${meta.n} != 31`);
ok(meta.noindex, '① 缺 noindex');
ok(meta.sigs.length === 31 && meta.sigs.every((s, i) => s === `${i + 1}/31`), '① 页码 sig 不齐');
ok(THEME === 'dark' ? meta.theme === 'dark' : meta.theme !== 'dark', `① 主题态异常 ${meta.theme}`);

// ② 分步数
const steps = await pg.evaluate(() => [...document.querySelectorAll('.slide')].map(s => +s.dataset.steps));
EXP_STEPS.forEach((e, i) => ok(steps[i] === e, `② P${i + 1} steps ${steps[i]} != ${e}`));

// ③④⑤⑥ 逐页：板、hero、图、溢出
for (let i = 1; i <= 31; i++) {
  const r = await pg.evaluate((n) => {
    const s = document.querySelectorAll('.slide')[n - 1];
    document.querySelectorAll('.slide').forEach((el, k) => {
      el.classList.toggle('active', k === n - 1); el.classList.toggle('visible', k === n - 1);
    });
    s.querySelectorAll('[data-step]').forEach(el => el.classList.add('on'));
    const bgs = [...s.querySelectorAll('.conf-bg')];
    const bgCls = bgs.length === 1 ? [...bgs[0].classList].find(c => c.startsWith('conf-bg-') ) : null;
    const bgUrl = bgs.length === 1 ? getComputedStyle(bgs[0]).backgroundImage : '';
    const heroes = [...s.querySelectorAll('.hero-art')].map(h => ({
      cls: h.className, vis: getComputedStyle(h).display !== 'none', w: h.naturalWidth, fit: getComputedStyle(h).objectFit,
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
      if (el.className.match(/card-c|kpi|five|g12|mx|case|frame/)) {
        [...el.children].forEach(ch => {
          if (ch.getBoundingClientRect().bottom > r0.bottom + 6) out.push('cardspill:' + (el.className || '').slice(0, 44));
        });
      }
    });
    return { bgN: bgs.length, bgCls, bgUrl, heroes, badImgs, out };
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
  } else {
    ok(r.heroes.length === 0, `⑤ P${i} 不应有 hero`);
  }
  ok(r.badImgs.length === 0, `⑥ P${i} 图未加载 ${r.badImgs.join()}`);
  r.out.forEach(o => fails.push(`③ P${i} 溢出 ${o}`));
  await pg.waitForTimeout(60);
}

// ⑦ 主题切换：deckSwap 按钮真实切换（板源 + strip 双源）
await pg.evaluate(() => { window.deck.i = 19; document.querySelectorAll('.slide').forEach((el, k) => el.classList.toggle('active', k === 19)); });
await pg.click('#deckSwap');
await pg.waitForTimeout(400);
const sw = await pg.evaluate(() => {
  const s = document.querySelectorAll('.slide')[19];
  const bg = getComputedStyle(s.querySelector('.conf-bg')).backgroundImage;
  const lt = s.querySelector('.strip img.lt'), dk = s.querySelector('.strip img.dk');
  return { theme: document.documentElement.getAttribute('data-theme'), bg,
           lt: lt ? getComputedStyle(lt).display : null, dk: dk ? getComputedStyle(dk).display : null };
});
const flipped = THEME === 'dark' ? 'light' : 'dark';
ok(THEME === 'dark' ? sw.theme !== 'dark' : sw.theme === 'dark', `⑦ 切换后主题态 ${sw.theme}`);
ok(sw.bg.includes('-' + flipped + '.png'), '⑦ 切换后板源未换');
ok(flipped === 'dark' ? (sw.lt === 'none' && sw.dk === 'block') : (sw.dk === 'none' && sw.lt === 'block'), `⑦ strip 双源 ${sw.lt}/${sw.dk}`);
await pg.click('#deckSwap'); await pg.waitForTimeout(250);

// ⑧ 步进机制抽查（P7 · 3 步）
const stepChk = await pg.evaluate(() => {
  const deck = window.deck;
  deck.i = 6; deck.step = 0;
  document.querySelectorAll('.slide').forEach((el, k) => { el.classList.toggle('active', k === 6); el.classList.toggle('visible', k === 6); });
  const s = document.querySelectorAll('.slide')[6];
  s.querySelectorAll('[data-step]').forEach(el => el.classList.remove('on'));
  const vis0 = [...s.querySelectorAll('[data-step]')].filter(el => el.classList.contains('on')).length;
  s.querySelectorAll('[data-step]').forEach(el => el.classList.toggle('on', (+el.dataset.step || 0) <= 2));
  const vis2 = [...s.querySelectorAll('[data-step]')].filter(el => el.classList.contains('on')).length;
  return { total: s.querySelectorAll('[data-step]').length, vis0, vis2 };
});
ok(stepChk.total === 3 && stepChk.vis0 === 0 && stepChk.vis2 === 2, `⑧ P7 步进 ${JSON.stringify(stepChk)}`);

ok(errs.length === 0, '① console: ' + errs.slice(0, 4).join(' | '));
console.log(fails.length ? '✗ FAIL ' + THEME + '\n' + fails.map(f => '  ' + f).join('\n') : `✓ PASS ${THEME} · 31 页全绿`);
await b.close();
process.exit(fails.length ? 1 : 0);
