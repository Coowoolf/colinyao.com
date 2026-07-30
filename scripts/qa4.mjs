import { chromium } from "playwright-core";
import { mkdirSync } from "fs";
mkdirSync("/tmp/qa4", { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
// 浅底 ideas（大母题）+ 3years 浅底金色页
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.4 });
await p.addInitScript(() => { try { localStorage.setItem("colin-theme", "light"); } catch {} });
await p.goto("http://localhost:3000/ideas", { waitUntil: "networkidle" });
await p.waitForTimeout(2800);
await p.screenshot({ path: "/tmp/qa4/ideas-light-big.png" });
await p.goto("http://localhost:3000/3years#25", { waitUntil: "networkidle" });
await p.waitForTimeout(2800);
await p.screenshot({ path: "/tmp/qa4/3years-light-s25.png" });
// 暗底 ideas 大母题
const d = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.4 });
await d.goto("http://localhost:3000/ideas", { waitUntil: "networkidle" });
await d.evaluate(() => window.scrollTo({ top: 400, behavior: "instant" }));
await d.waitForTimeout(2800);
await d.screenshot({ path: "/tmp/qa4/ideas-dark-big.png" });
await b.close();
console.log("done");
