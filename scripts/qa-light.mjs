import { chromium } from "playwright-core";
import { mkdirSync } from "fs";
mkdirSync("/tmp/light", { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
// 站点浅底
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.4 });
await p.addInitScript(() => { try { localStorage.setItem("colin-theme", "light"); } catch {} });
await p.goto("http://localhost:3000/", { waitUntil: "networkidle" });
await p.waitForTimeout(3000);
await p.screenshot({ path: "/tmp/light/site-hero.png" });
await p.evaluate(() => window.scrollTo({ top: 1750, behavior: "instant" }));
await p.waitForTimeout(2400);
await p.screenshot({ path: "/tmp/light/site-ideas.png" });
await p.goto("http://localhost:3000/talks", { waitUntil: "networkidle" });
await p.waitForTimeout(2600);
await p.screenshot({ path: "/tmp/light/site-talks.png" });
// 3years 浅底（原地切换：localStorage 已是 light）
await p.goto("http://localhost:3000/3years#1", { waitUntil: "networkidle" });
await p.waitForTimeout(2600);
await p.screenshot({ path: "/tmp/light/deck-s1.png" });
await p.evaluate(() => window.deck.go(39));
await p.waitForTimeout(2600);
await p.screenshot({ path: "/tmp/light/deck-s40.png" });
await p.evaluate(() => window.deck.go(19));
await p.waitForTimeout(2400);
await p.evaluate(() => window.deck.next());
await p.waitForTimeout(1500);
await p.screenshot({ path: "/tmp/light/deck-s20.png" });
// newcollege：localStorage=light 应自动跳转到浅底版
await p.goto("http://localhost:3000/newcollege", { waitUntil: "networkidle" });
await p.waitForTimeout(3200);
console.log("newcollege landed at:", p.url());
await p.screenshot({ path: "/tmp/light/newcollege.png" });
// 暗底不受影响验证
const d = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.4 });
await d.goto("http://localhost:3000/", { waitUntil: "networkidle" });
await d.waitForTimeout(2600);
await d.screenshot({ path: "/tmp/light/site-hero-dark.png" });
await b.close();
console.log("done");
