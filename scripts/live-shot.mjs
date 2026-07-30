import { chromium } from "playwright-core";
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5 });
await p.goto("https://colinyao.com", { waitUntil: "networkidle", timeout: 45000 });
await p.waitForTimeout(2800);
await p.screenshot({ path: "/tmp/live-colinyao.png" });
await b.close();
console.log("done");
