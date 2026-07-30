import { chromium } from "playwright-core";
import { mkdirSync } from "fs";
mkdirSync("/tmp/qa3", { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.4 });
await p.goto("http://localhost:3000/3years#1", { waitUntil: "networkidle" });
await p.waitForTimeout(2000);
for (const n of [13, 16, 21, 24, 26, 32, 34, 36, 38, 40]) {
  await p.evaluate(i => window.deck.go(i), n - 1);
  await p.waitForTimeout(2400);
  const steps = await p.evaluate(() => window.deck.maxStep[window.deck.i]);
  for (let s = 0; s < steps; s++) { await p.evaluate(() => window.deck.next()); await p.waitForTimeout(1000); }
  await p.screenshot({ path: `/tmp/qa3/d${String(n).padStart(2, "0")}.png` });
}
const h = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5 });
await h.goto("http://localhost:3000/", { waitUntil: "networkidle" });
await h.evaluate(() => window.scrollTo({ top: 800, behavior: "instant" }));
await h.waitForTimeout(2600);
await h.screenshot({ path: "/tmp/qa3/home-stats-ideas.png" });
await h.goto("http://localhost:3000/ideas", { waitUntil: "networkidle" });
await h.evaluate(() => window.scrollTo({ top: 500, behavior: "instant" }));
await h.waitForTimeout(2600);
await h.screenshot({ path: "/tmp/qa3/ideas-live.png" });
await b.close();
console.log("done");
