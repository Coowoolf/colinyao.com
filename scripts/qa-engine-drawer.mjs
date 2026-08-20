// 抽屉实测 · convoai-info P4 → Enter → 引擎 deck iframe
// 断言：iframe 内 .pp 数 == 16；iframe 内 html[data-theme] 与宿主一致（浅浅 / 深深各一组）
// 2026-08-20：引擎 deck 扩页 13 → 16（补双工三模式 / 全双工工作原理 / VAD 三张机理页）
// 用法：node scripts/qa-engine-drawer.mjs        （BASE 默认 8777）
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8777';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const fails = [];
for (const theme of ['light', 'dark']) {
  const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } });
  if (theme === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const pg = await ctx.newPage();
  await pg.goto(BASE + '/decks/convoai-info.html#4', { waitUntil: 'load' });
  await pg.waitForTimeout(2400);            // 等 P4 整页入场走完（.rise --i:4 ≈ 1.2s）
  await pg.evaluate(() => document.activeElement?.blur());
  await pg.keyboard.press('Enter');
  await pg.waitForTimeout(300);
  const opened = await pg.evaluate(() => document.getElementById('engineOverlay').hidden === false);
  if (!opened) { fails.push(`[${theme}] Enter 未展开 overlay`); await ctx.close(); continue; }
  const r = await pg.waitForFunction(() => {
    const f = document.getElementById('engineFrame'), d = f && f.contentDocument;
    if (!(d && d.readyState === 'complete' && d.querySelectorAll('.pp').length)) return false;
    return {
      pp: d.querySelectorAll('.pp').length,
      sec: d.querySelectorAll('section').length,
      inner: d.documentElement.getAttribute('data-theme'),
      host: document.documentElement.getAttribute('data-theme'),
      title: d.title,
      sigLast: d.querySelector('.slide[data-p="16"] .sig')?.textContent,
    };
  }, null, { timeout: 10000 }).then(h => h.jsonValue()).catch(() => null);
  if (!r) { fails.push(`[${theme}] iframe 未就绪`); await ctx.close(); continue; }
  const want = theme === 'dark' ? 'dark' : null;
  if (r.pp !== 16) fails.push(`[${theme}] iframe .pp 数 ${r.pp} != 16`);
  if (r.sec !== 16) fails.push(`[${theme}] iframe section 数 ${r.sec} != 16`);
  if ((r.host || null) !== want) fails.push(`[${theme}] 宿主主题 ${r.host} != ${want}`);
  if ((r.inner || null) !== want) fails.push(`[${theme}] iframe 主题 ${r.inner} != ${want}（未跟随宿主）`);
  if (r.inner !== r.host) fails.push(`[${theme}] iframe 与宿主主题不一致 ${r.inner} / ${r.host}`);
  if (r.title !== '声网 · 对话式 AI 引擎 · 产品介绍') fails.push(`[${theme}] iframe title「${r.title}」`);
  if (r.sigLast !== '16/16') fails.push(`[${theme}] iframe P16 sig「${r.sigLast}」!= 16/16`);
  console.log(`· ${theme}：.pp=${r.pp} section=${r.sec} 宿主=${r.host || 'light'} iframe=${r.inner || 'light'} sigLast=${r.sigLast}`);
  await ctx.close();
}
await b.close();
console.log(fails.length ? '✗ FAIL\n' + fails.map(f => '  ' + f).join('\n') : '✓ PASS · 抽屉两组主题均跟随宿主 · iframe 16 页');
process.exit(fails.length ? 1 : 0);
