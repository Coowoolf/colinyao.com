// QA 对外演讲 decks：双主题加载、JS 无错、deck 初始化、主题色正确
import { chromium } from "playwright-core";
import { execSync } from "child_process";

const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const slugs = ["rte24","pm24","convoai","audio25","engine25","era3","prodready","pm25","vibecheck","vibesota","dual26","robot26","gcloud","aws26"];

const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1600, height: 900 } })).newPage();
let fails = [];

for (const theme of ["dark", "light"]) {
  for (const slug of [...slugs, "talkdecks"]) {
    const errs = [];
    page.removeAllListeners("pageerror");
    page.on("pageerror", (e) => errs.push(String(e)));
    await page.goto("http://localhost:3000/" + slug, { waitUntil: "load" });
    await page.evaluate((t) => localStorage.setItem("colin-theme", t), theme);
    await page.reload({ waitUntil: "load" });
    await page.waitForTimeout(400);
    const r = await page.evaluate(() => {
      const isDeck = !!document.querySelector(".deck-stage");
      const active = document.querySelector(".slide.active");
      const bg = getComputedStyle(document.querySelector(".deck-stage") || document.body).backgroundColor;
      const attr = document.documentElement.getAttribute("data-theme");
      const btn = document.getElementById("deckSwap")?.textContent;
      return { isDeck, hasActive: !!active, bg, attr, btn };
    });
    const wantDark = theme === "dark";
    const problems = [];
    if (errs.length) problems.push("pageerror: " + errs[0].slice(0, 90));
    if (slug !== "talkdecks" && !r.hasActive) problems.push("deck not initialized");
    if (wantDark && r.attr !== "dark") problems.push("data-theme missing");
    if (!wantDark && r.attr) problems.push("data-theme not removed");
    if (slug !== "talkdecks") {
      const expect = wantDark ? "rgb(15, 14, 23)" : "rgb(239, 240, 243)";
      if (r.bg !== expect) problems.push(`bg ${r.bg} ≠ ${expect}`);
    }
    const expectBtn = wantDark ? "浅底" : "暗底";
    if (r.btn !== expectBtn) problems.push(`btn "${r.btn}" ≠ ${expectBtn}`);
    if (problems.length) fails.push(`${theme}/${slug}: ${problems.join("; ")}`);
    else console.log(`${theme}/${slug} OK`);
  }
}
// 抽查截图：aws26 双主题 + talkdecks 双主题
for (const [slug, theme] of [["aws26","dark"],["aws26","light"],["talkdecks","dark"],["talkdecks","light"],["rte24","dark"]]) {
  await page.goto("http://localhost:3000/" + slug, { waitUntil: "load" });
  await page.evaluate((t) => localStorage.setItem("colin-theme", t), theme);
  await page.reload({ waitUntil: "load" });
  await page.waitForTimeout(900);
  await page.screenshot({ path: `/tmp/qa-${slug}-${theme}.png` });
}
await browser.close();
console.log(fails.length ? "FAILS:\n" + fails.join("\n") : "ALL GREEN · " + (slugs.length + 1) + " pages × 2 themes");
process.exit(fails.length ? 1 : 0);
