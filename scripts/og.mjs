import { chromium } from "playwright-core";
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 2 });
await p.goto("file:///tmp/og.html");
await p.waitForTimeout(800);
await p.screenshot({ path: "public/og.png" });
await b.close();
console.log("og done");
