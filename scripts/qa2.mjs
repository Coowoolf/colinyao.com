import { chromium } from "playwright-core";
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
async function shot(name, path, w=1440, h=900, settle=3000) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
  await p.goto(`http://localhost:3000${path}`, { waitUntil: "networkidle" });
  await p.waitForTimeout(settle);
  await p.screenshot({ path: `/tmp/shots/${name}.png` });
  await p.close();
  console.log("✓", name);
}
await shot("hero-v2", "/");
await shot("newcollege-deck", "/newcollege", 1600, 900, 3500);
await b.close();
