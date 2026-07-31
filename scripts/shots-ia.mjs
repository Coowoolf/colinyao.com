import { chromium } from "playwright-core";
import { execSync } from "child_process";
const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1560, height: 980 } })).newPage();
page.on("pageerror", (e) => console.log("PAGEERROR:", String(e).slice(0, 140)));
// 首页（新 nav 四字）
await page.goto("http://localhost:3000/", { waitUntil: "load" });
await page.waitForTimeout(2600);
await page.screenshot({ path: "/tmp/ia1-home.png" });
// 维度页 /time
await page.goto("http://localhost:3000/time", { waitUntil: "load" });
await page.waitForTimeout(2400);
await page.screenshot({ path: "/tmp/ia2-time.png" });
await page.evaluate(() => window.scrollTo({ top: 900, behavior: "instant" }));
await page.waitForTimeout(1600);
await page.screenshot({ path: "/tmp/ia3-time-list.png" });
// 总目
await page.goto("http://localhost:3000/toc", { waitUntil: "load" });
await page.waitForTimeout(2200);
await page.screenshot({ path: "/tmp/ia4-toc.png" });
// 书
await page.goto("http://localhost:3000/book", { waitUntil: "load" });
await page.waitForTimeout(2400);
await page.screenshot({ path: "/tmp/ia5-book.png" });
// 移动端首页 + 维度页
const m = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
await m.goto("http://localhost:3000/outward", { waitUntil: "load" });
await m.waitForTimeout(2400);
await m.screenshot({ path: "/tmp/ia6-m-outward.png" });
await browser.close();
console.log("done");
