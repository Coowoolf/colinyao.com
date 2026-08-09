// QA：/aiot26（保底版 40 页）+ /aiot26-v3（升维版 35 页）试讲前走查
// 全页 data-step 推满 · 零溢出 · 零 pageerror · V3 默认浅色 · 两张定点截图
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");

const exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const b = await chromium.launch({ executablePath: exe, args: ["--autoplay-policy=no-user-gesture-required", "--mute-audio"] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = [];
pg.on("pageerror", (e) => errs.push("pageerror: " + e.message));

async function walk(route, expect) {
  await pg.goto("http://localhost:3000" + route, { waitUntil: "networkidle" });
  await pg.waitForFunction((n) => window.deck && window.deck.slides && window.deck.slides.length === n, expect);
  const n = await pg.evaluate(() => window.deck.slides.length);
  const overflow = [];
  let steps = 0;
  for (let i = 0; i < n; i++) {
    await pg.evaluate((k) => window.deck.go(k), i);
    await pg.waitForTimeout(110);
    steps += await pg.evaluate(() => {
      const d = window.deck, s = d.slides[d.i];
      const all = [...s.querySelectorAll("[data-step]")];
      const mx = Math.max(0, ...all.map((e) => +e.dataset.step));
      for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
      if (d.step !== undefined) d.step = mx;
      return all.length;
    });
    await pg.waitForTimeout(60);
    const bad = await pg.evaluate(() => {
      const s = window.deck.slides[window.deck.i], r = s.getBoundingClientRect(), out = [];
      s.querySelectorAll("div,p,h1,h2,h3,span,li,td,th,i,b").forEach((el) => {
        if (!el.offsetParent) return;
        const q = el.getBoundingClientRect();
        if (q.width && q.height && (q.bottom > r.bottom + 4 || q.right > r.right + 4 || q.left < r.left - 4)) {
          const t = (el.textContent || "").trim().slice(0, 40);
          if (t) out.push(t);
        }
      });
      return out.slice(0, 3);
    });
    if (bad.length) overflow.push({ slide: i + 1, bad });
  }
  return { route, slides: n, stepEls: steps, overflow };
}

// ── 1) 保底版 /aiot26 · 40 页 ───────────────────────────
const a = await walk("/aiot26", 40);
console.log("/aiot26 ->", JSON.stringify(a));
const mq = await pg.evaluate(() => {
  const t = document.body.textContent;
  const m = t.match(/MONEY QUOTE · \d\d/g) || [];
  return { list: m, uniq: [...new Set(m)].length, p13: window.deck.slides[12].textContent.includes("MONEY QUOTE · 02") && window.deck.slides[12].textContent.includes("3 天扔抽屉") };
});
console.log("/aiot26 MQ:", JSON.stringify(mq));
await pg.evaluate(() => window.deck.go(12));
await pg.waitForTimeout(700);
await pg.evaluate(() => { const s = window.deck.slides[12]; s.querySelectorAll("[data-step]").forEach((e) => e.classList.add("on")); });
await pg.waitForTimeout(400);
await pg.screenshot({ path: "/tmp/qa/final-aiot-mq13.png" });

// ── 2) 升维版 /aiot26-v3 · 35 页 ────────────────────────
const v = await walk("/aiot26-v3", 35);
console.log("/aiot26-v3 ->", JSON.stringify(v));
const v3 = await pg.evaluate(() => ({
  defaultLight: document.documentElement.getAttribute("data-theme") !== "dark",
  bg: getComputedStyle(document.body).backgroundColor,
  eyebrow: window.deck.slides[11].textContent.includes("分水岭不是智能，是角色 —— 今天唯一需要你记住的那张图"),
  formula: window.deck.slides[11].textContent.includes("伙伴感 = 角色一致性 × 共同历史 × 可控临场"),
  mq: (document.body.textContent.match(/MONEY QUOTE · \d\d/g) || []),
  video: document.querySelectorAll("video[data-dm]").length,
}));
console.log("/aiot26-v3 checks:", JSON.stringify(v3));
await pg.evaluate(() => window.deck.go(11));
await pg.waitForTimeout(700);
await pg.evaluate(() => { const s = window.deck.slides[11]; s.querySelectorAll("[data-step]").forEach((e) => e.classList.add("on")); });
await pg.waitForTimeout(500);
await pg.screenshot({ path: "/tmp/qa/final-v3-p12.png" });

// ── 3) 未改 deck 回归 ───────────────────────────────────
for (const [r, n] of [["/cowork", 62], ["/cowork-conf", 55], ["/robot26", 36], ["/aiot26-v2", 26]]  // robot26 2026-08-09 起 = 北京站 PPT 还原 36 页) {
  await pg.goto("http://localhost:3000" + r, { waitUntil: "networkidle" });
  await pg.waitForFunction(() => window.deck && window.deck.slides);
  const got = await pg.evaluate(() => window.deck.slides.length);
  console.log(`${r}: ${got} 页 ${got === n ? "✓" : "✗ 期望 " + n}`);
}

console.log("pageerrors:", errs.length ? errs : "none");
const fail = a.overflow.length || v.overflow.length || errs.length || !v3.defaultLight || !v3.eyebrow || mq.uniq !== 4;
console.log(fail ? "QA FAIL" : "QA PASS");
await b.close();
