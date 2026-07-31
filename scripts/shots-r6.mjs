import { chromium } from "playwright-core";
import { execSync } from "child_process";
const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1560, height: 980 } })).newPage();
page.on("pageerror", (e) => console.log("PAGEERROR:", String(e).slice(0, 120)));
// 1 首焦 attract=时（验证 时 大字不再被 nav 盖）
await page.goto("http://localhost:3000/", { waitUntil: "load" });
await page.waitForTimeout(2600);
await page.screenshot({ path: "/tmp/r6-1-attract-time.png" });
// 2 全图态（验证 空 大字 + 读数栏左下）
const wrapH = await page.evaluate(() => document.querySelector(".ruler-scrollwrap").getBoundingClientRect().height - innerHeight);
await page.evaluate((h) => window.scrollTo({ top: h * 0.95, behavior: "instant" }), wrapH);
await page.waitForTimeout(2000);
await page.screenshot({ path: "/tmp/r6-2-all.png" });
// 3 总目区 + 关于区
await page.evaluate(() => document.getElementById("index")?.scrollIntoView());
await page.waitForTimeout(1800);
await page.screenshot({ path: "/tmp/r6-3-toc.png" });
await page.evaluate(() => document.getElementById("about")?.scrollIntoView());
await page.waitForTimeout(1800);
await page.screenshot({ path: "/tmp/r6-4-about.png" });
// 4 V10 + 3years 双主题首页
for (const [slug, theme] of [["cowork","dark"],["cowork","light"],["3years","dark"],["3years","light"]]) {
  await page.goto(`http://localhost:3000/${slug}`, { waitUntil: "load" });
  await page.evaluate((t) => localStorage.setItem("colin-theme", t), theme);
  await page.reload({ waitUntil: "load" });
  await page.waitForTimeout(1100);
  await page.screenshot({ path: `/tmp/r6-${slug}-${theme}.png` });
}
await browser.close();
console.log("done");
