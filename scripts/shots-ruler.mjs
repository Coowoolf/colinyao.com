import { chromium } from "playwright-core";
import { execSync } from "child_process";
const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1560, height: 980 } })).newPage();
page.on("pageerror", (e) => console.log("PAGEERROR:", String(e).slice(0, 160)));

// 1. 首焦待机（attract 第一拍 = 时）
await page.goto("http://localhost:3000/ruler", { waitUntil: "load" });
await page.waitForTimeout(2600);
await page.screenshot({ path: "/tmp/n1-attract-time.png" });
// 2. 待机第二拍 = 空
await page.waitForTimeout(4300);
await page.screenshot({ path: "/tmp/n2-attract-space.png" });

// 3. 滚动叙事：合上
const wrapH = await page.evaluate(() => document.querySelector(".ruler-scrollwrap").getBoundingClientRect().height - innerHeight);
await page.evaluate((h) => window.scrollTo(0, h * 0.03), wrapH);
await page.waitForTimeout(1600);
await page.screenshot({ path: "/tmp/n3-fold.png" });

// 4. 叙事 · 时
await page.evaluate((h) => window.scrollTo(0, h * 0.15), wrapH);
await page.waitForTimeout(1800);
await page.screenshot({ path: "/tmp/n4-dim-time.png" });

// 5. 叙事 · 内
await page.evaluate((h) => window.scrollTo(0, h * 0.56), wrapH);
await page.waitForTimeout(1800);
await page.screenshot({ path: "/tmp/n5-dim-inw.png" });

// 6. 终段全图 + 悬停
await page.evaluate((h) => window.scrollTo(0, h * 0.99), wrapH);
await page.waitForTimeout(2200);
const bb = await page.locator(".cpin-dot").nth(6).boundingBox();
if (bb) { await page.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2); await page.waitForTimeout(500); }
await page.screenshot({ path: "/tmp/n6-all-hover.png" });

// 7. light 全图
await page.evaluate(() => localStorage.setItem("colin-theme", "light"));
await page.reload({ waitUntil: "load" });
await page.waitForTimeout(1200);
const wrapH2 = await page.evaluate(() => document.querySelector(".ruler-scrollwrap").getBoundingClientRect().height - innerHeight);
await page.evaluate((h) => window.scrollTo(0, h * 0.95), wrapH2);
await page.waitForTimeout(1800);
await page.screenshot({ path: "/tmp/n7-all-light.png" });

// 8. light 叙事 · 空
await page.evaluate((h) => window.scrollTo(0, h * 0.35), wrapH2);
await page.waitForTimeout(1800);
await page.screenshot({ path: "/tmp/n8-space-light.png" });

// 9. 移动端待机
const m = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
await m.goto("http://localhost:3000/ruler", { waitUntil: "load" });
await m.waitForTimeout(2600);
await m.screenshot({ path: "/tmp/n9-mobile-attract.png" });
const mh = await m.evaluate(() => document.querySelector(".ruler-scrollwrap").getBoundingClientRect().height - innerHeight);
await m.evaluate((h) => window.scrollTo(0, h * 0.15), mh);
await m.waitForTimeout(1800);
await m.screenshot({ path: "/tmp/n10-mobile-dim.png" });

await browser.close();
console.log("shots done");
