import { chromium } from "playwright-core";
import { mkdirSync } from "fs";

const OUT = "/tmp/shots";
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });

async function shot(name, path, { width = 1440, height = 900, scrollTo = null, settle = 2600 } = {}) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1.5 });
  await page.goto(`http://localhost:3000${path}`, { waitUntil: "networkidle" });
  if (scrollTo !== null) {
    await page.evaluate((y) => window.scrollTo({ top: y, behavior: "instant" }), scrollTo);
  }
  await page.waitForTimeout(settle);
  await page.screenshot({ path: `${OUT}/${name}.png` });
  await page.close();
  console.log("✓", name);
}

await shot("01-home-hero", "/");
await shot("02-home-stats", "/", { scrollTo: 900 });
await shot("03-home-ideas", "/", { scrollTo: 1650 });
await shot("04-home-mq", "/", { scrollTo: 2600 });
await shot("05-home-talks", "/", { scrollTo: 3400 });
await shot("06-talks-top", "/talks");
await shot("07-talks-list", "/talks", { scrollTo: 1200 });
await shot("08-ideas-top", "/ideas");
await shot("09-ideas-cards", "/ideas", { scrollTo: 1100 });
await shot("10-about", "/about");
await shot("11-mobile-hero", "/", { width: 390, height: 844 });
await shot("12-mobile-talks", "/talks", { width: 390, height: 844, scrollTo: 700 });

await browser.close();
console.log("done");
