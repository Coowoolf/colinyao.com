// robot26 北京站还原 · 逐页截图（对照 PPT 原稿用）。用法：
//   (cd public && python3 -m http.server 8899 &) ; node scripts/shots-robot26.mjs [起页] [止页]
import { chromium } from "playwright-core";
import { execSync } from "child_process";
import fs from "fs";

const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const from = +(process.argv[2] || 1), to = +(process.argv[3] || 36);
const dir = "/tmp/qa/robot26";
fs.mkdirSync(dir, { recursive: true });

const b = await chromium.launch({ executablePath: exe, args: ["--force-color-profile=srgb"] });
const pg = await (await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
const errs = [];
pg.on("pageerror", (e) => errs.push(String(e)));
await pg.goto("http://localhost:8899/decks/robot26.html", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides.length === 36);

for (let n = from; n <= to; n++) {
  await pg.evaluate((i) => window.deck.go(i), n - 1);
  await pg.evaluate(() => { const d = window.deck; d.step = d.maxStep[d.i]; d.applySteps(); });
  await pg.waitForTimeout(2400);
  await pg.screenshot({ path: `${dir}/p${String(n).padStart(2, "0")}.png` });
}
console.log("pageerrors:", errs.length ? errs.slice(0, 5) : "none");
await b.close();
