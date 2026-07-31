import { chromium } from "playwright-core";
import { execSync } from "child_process";
const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1560, height: 980 } })).newPage();
page.on("pageerror", (e) => console.log("PAGEERROR:", String(e).slice(0, 140)));

await page.goto("http://localhost:3000/ruler", { waitUntil: "load" });
await page.waitForTimeout(600);
const wrapH = await page.evaluate(() => document.querySelector(".ruler-scrollwrap").getBoundingClientRect().height - innerHeight);
// 时（活性环=最内圈）
await page.evaluate((h) => window.scrollTo({ top: h * 0.15, behavior: "instant" }), wrapH);
await page.waitForTimeout(1900);
await page.screenshot({ path: "/tmp/f1-time-rings.png" });
// 全图（侧轨四字齐亮）
await page.evaluate((h) => window.scrollTo({ top: h * 0.95, behavior: "instant" }), wrapH);
await page.waitForTimeout(1900);
await page.screenshot({ path: "/tmp/f2-all-rail.png" });

// 移动端
const m = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
await m.goto("http://localhost:3000/ruler", { waitUntil: "load" });
await m.waitForTimeout(2400);
await m.screenshot({ path: "/tmp/f3-m-attract.png" });
const mh = await m.evaluate(() => document.querySelector(".ruler-scrollwrap").getBoundingClientRect().height - innerHeight);
await m.evaluate((h) => window.scrollTo({ top: h * 0.15, behavior: "instant" }), mh);
await m.waitForTimeout(2000);
await m.screenshot({ path: "/tmp/f4-m-time.png" });
await m.evaluate((h) => window.scrollTo({ top: h * 0.45, behavior: "instant" }), mh);
await m.waitForTimeout(2000);
await m.screenshot({ path: "/tmp/f5-m-space.png" });
await m.evaluate((h) => window.scrollTo({ top: h * 0.95, behavior: "instant" }), mh);
await m.waitForTimeout(2000);
await m.screenshot({ path: "/tmp/f6-m-all.png" });
// 横向溢出检查
const overflowX = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
console.log("mobile overflow-x px:", overflowX);
await browser.close();
console.log("done");
