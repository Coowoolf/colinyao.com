// QA 成书结构：双主题截图 + pageerror + 关键元素在场 + 文字碰撞抽查
import { chromium } from "playwright-core";
import { execSync } from "child_process";

const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const pages = ["/", "/book", "/time", "/space", "/inward", "/outward", "/toc", "/preface", "/vol1", "/vol2", "/vol3", "/vol4", "/vol5", "/about"];

const browser = await chromium.launch({ executablePath: exe });
const ctx = await browser.newContext({ viewport: { width: 1500, height: 950 } });
const page = await ctx.newPage();
let fails = [];

for (const theme of ["dark", "light"]) {
  for (const path of pages) {
    const errs = [];
    page.removeAllListeners("pageerror");
    page.on("pageerror", (e) => errs.push(String(e)));
    await page.goto("http://localhost:3000" + path, { waitUntil: "load" });
    await page.evaluate((t) => localStorage.setItem("colin-theme", t), theme);
    await page.reload({ waitUntil: "load" });
    await page.waitForTimeout(700);
    // 滚到底触发全部 Reveal（instant 步进，避免 smooth 动画互相打断导致 IO 丢事件）
    await page.evaluate(async () => {
      await new Promise((res) => {
        let y = 0;
        const t = setInterval(() => {
          y += 450; window.scrollTo({ top: y, behavior: "instant" });
          if (y >= document.body.scrollHeight) { clearInterval(t); res(null); }
        }, 90);
      });
    });
    await page.waitForTimeout(2500); // 等 stagger 入场（--i × 88ms + 1.05s）全部走完再采样
    const r = await page.evaluate(() => ({
      attr: document.documentElement.getAttribute("data-theme"),
      hidden: [...document.querySelectorAll(".flow,.rise,.spread,.settle,.pop,.ink,.dw")].filter(
        (el) => getComputedStyle(el).opacity === "0"
      ).length,
      lockedLinks: [...document.querySelectorAll("a")].filter((a) => a.getAttribute("href") === "/trust").length,
    }));
    const problems = [];
    if (errs.length) problems.push("pageerror: " + errs[0].slice(0, 100));
    if (theme === "light" && r.attr !== "light") problems.push("light not applied");
    if (r.hidden > 0) problems.push(`${r.hidden} elements stuck hidden`);
    if (r.lockedLinks > 0) problems.push("/trust is linked (must stay locked)");
    if (problems.length) fails.push(`${theme}${path}: ${problems.join("; ")}`);
    else console.log(`${theme}${path} OK`);
  }
}

// 截图：封面/目录、序、卷一、卷五（锁定篇）双主题
for (const [path, name] of [["/book", "cover"], ["/preface", "preface"], ["/vol1", "vol1"], ["/vol5", "vol5"]]) {
  for (const theme of ["dark", "light"]) {
    await page.goto("http://localhost:3000" + path, { waitUntil: "load" });
    await page.evaluate((t) => localStorage.setItem("colin-theme", t), theme);
    await page.reload({ waitUntil: "load" });
    await page.waitForTimeout(1100);
    await page.screenshot({ path: `/tmp/book-${name}-${theme}.png` });
    if (name === "vol5") {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(800);
      await page.screenshot({ path: `/tmp/book-${name}-${theme}-end.png` });
    }
  }
}
// 目录区块单独截一张（滚到 toc）
await page.goto("http://localhost:3000/book#toc", { waitUntil: "load" });
await page.evaluate(() => localStorage.removeItem("colin-theme"));
await page.reload({ waitUntil: "load" });
await page.evaluate(() => document.getElementById("toc")?.scrollIntoView());
await page.waitForTimeout(1200);
await page.screenshot({ path: "/tmp/book-toc-dark.png" });

// 碰撞抽查：目录行 + 篇目行文字不重叠
await page.goto("http://localhost:3000/vol1", { waitUntil: "load" });
await page.waitForTimeout(900);
const overlap = await page.evaluate(() => {
  const rows = [...document.querySelectorAll(".piece-row")];
  const bad = [];
  for (const row of rows) {
    const els = [...row.querySelectorAll(".piece-no,.piece-title,.piece-pg")].map((e) => e.getBoundingClientRect());
    for (let i = 0; i < els.length; i++)
      for (let j = i + 1; j < els.length; j++) {
        const a = els[i], b = els[j];
        const x = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
        const y = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
        if (x > 4 && y > 4) bad.push(`${i}/${j} overlap ${Math.round(x)}x${Math.round(y)}`);
      }
  }
  return bad;
});
if (overlap.length) fails.push("vol1 piece-row overlap: " + overlap.join(", "));

await browser.close();
console.log(fails.length ? "FAILS:\n" + fails.join("\n") : "ALL GREEN · 10 pages × 2 themes + collision");
process.exit(fails.length ? 1 : 0);
