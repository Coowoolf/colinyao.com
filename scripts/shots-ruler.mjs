import { chromium } from "playwright-core";
import { execSync } from "child_process";
const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1560, height: 980 } })).newPage();
page.on("pageerror", (e) => console.log("PAGEERROR:", String(e).slice(0, 160)));

// 1. free 态 dark
await page.goto("http://localhost:3000/ruler", { waitUntil: "load" });
await page.waitForTimeout(2600);
await page.screenshot({ path: "/tmp/r1-free-dark.png" });

// 2. hover 钉图
const pin = page.locator(".pin").nth(4);
await pin.hover();
await page.waitForTimeout(500);
await page.screenshot({ path: "/tmp/r2-hover.png" });

// 3. 导览起点卡
await page.click(".rbtn.primary");
await page.waitForTimeout(1300);
await page.screenshot({ path: "/tmp/r3-tour-origin.png" });

// 4. 中途站（外·基准 = 第4站）
for (let i = 0; i < 4; i++) { await page.keyboard.press("ArrowRight"); await page.waitForTimeout(260); }
await page.waitForTimeout(1300);
await page.screenshot({ path: "/tmp/r4-tour-station.png" });

// 5. 终点卡
for (let i = 0; i < 30; i++) await page.keyboard.press("ArrowRight");
await page.waitForTimeout(1400);
await page.screenshot({ path: "/tmp/r5-tour-finale.png" });

// 6. light 主题 free
await page.evaluate(() => localStorage.setItem("colin-theme", "light"));
await page.reload({ waitUntil: "load" });
await page.waitForTimeout(2600);
await page.screenshot({ path: "/tmp/r6-free-light.png" });

// 7. 清单区
await page.evaluate(() => document.getElementById("list")?.scrollIntoView());
await page.waitForTimeout(1600);
await page.screenshot({ path: "/tmp/r7-list-light.png" });

// 8. 移动端 390px（dark, 导览态）
const m = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
await m.goto("http://localhost:3000/ruler", { waitUntil: "load" });
await m.waitForTimeout(2400);
await m.screenshot({ path: "/tmp/r8-mobile.png" });
await m.click(".rbtn.primary");
await m.waitForTimeout(200);
// 前进到一个多 pin 的站
for (let i = 0; i < 4; i++) { await m.tap(".ruler-topbar >> text=下一站 →").catch(() => {}); await m.waitForTimeout(220); }
await m.waitForTimeout(1200);
await m.screenshot({ path: "/tmp/r9-mobile-tour.png" });

// 10. 封面 CTA + 目录活页行
await page.setViewportSize({ width: 1560, height: 980 });
await page.evaluate(() => localStorage.removeItem("colin-theme"));
await page.goto("http://localhost:3000/#toc", { waitUntil: "load" });
await page.evaluate(() => document.getElementById("toc")?.scrollIntoView());
await page.waitForTimeout(2200);
await page.screenshot({ path: "/tmp/r10-toc.png" });

await browser.close();
console.log("shots done");
