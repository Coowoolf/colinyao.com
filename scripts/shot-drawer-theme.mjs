// 终审素材 · 抽屉开着时宿主切主题的前后两帧（验主题实时联动）
// 用法：node scripts/shot-drawer-theme.mjs   → /tmp/drawer-before.png · /tmp/drawer-after.png
import { chromium } from 'playwright-core';
const BASE = process.env.BASE || 'http://localhost:8777';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const pg = await ctx.newPage();
await pg.goto(BASE + '/decks/convoai-info.html#4', { waitUntil: 'load' });
await pg.evaluate(() => document.fonts.ready);
await pg.waitForTimeout(2200);
await pg.evaluate(() => document.activeElement?.blur());
await pg.keyboard.press('ArrowRight');          // P4 的 step1（04 · OPEN 那行 chips）
await pg.waitForTimeout(900);
await pg.keyboard.press('Enter');               // 展开抽屉
await pg.waitForFunction(() => {
  const d = document.getElementById('engineFrame')?.contentDocument;
  return d && d.readyState === 'complete' && d.querySelectorAll('section').length > 0;
}, null, { timeout: 15000 });
// 抽屉里翻到 P8 产品架构大图，两帧对比更能看出主题跟随
await pg.evaluate(() => { document.getElementById('engineFrame').contentWindow.location.hash = '#8'; });
await pg.waitForTimeout(2600);
await pg.screenshot({ path: '/tmp/drawer-before.png', clip: { x: 0, y: 0, width: 1920, height: 1080 } });
// overlay（z 10002）盖住 .deck-swap（z 1100），坐标点击会命中 scrim；直接派发按钮 click
await pg.evaluate(() => document.getElementById('deckSwap').click());
await pg.waitForTimeout(2200);
await pg.screenshot({ path: '/tmp/drawer-after.png', clip: { x: 0, y: 0, width: 1920, height: 1080 } });
const st = await pg.evaluate(() => ({
  host: document.documentElement.getAttribute('data-theme'),
  inner: document.getElementById('engineFrame').contentDocument.documentElement.getAttribute('data-theme'),
}));
console.log('· 切换后 host=' + (st.host || 'light') + ' iframe=' + (st.inner || 'light'));
await b.close();
