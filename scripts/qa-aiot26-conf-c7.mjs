// QA · aiot26-conf C7 轮：37 页全页走查（零溢出 / 零 pageerror）+ 六处改动定点截图
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");

const exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const b = await chromium.launch({ executablePath: exe, args: ["--autoplay-policy=no-user-gesture-required", "--mute-audio"] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = [];
pg.on("pageerror", (e) => errs.push("pageerror: " + e.message));

const ROUTE = "/aiot26-conf";
await pg.goto("http://localhost:3000" + ROUTE, { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides && window.deck.slides.length === 37);
const n = await pg.evaluate(() => window.deck.slides.length);

const overflow = [];
for (let i = 0; i < n; i++) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(110);
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const all = [...s.querySelectorAll("[data-step]")];
    const mx = Math.max(0, ...all.map((e) => +e.dataset.step));
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
    if (d.step !== undefined) d.step = mx;
  });
  await pg.waitForTimeout(70);
  const bad = await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i], r = s.getBoundingClientRect(), out = [];
    s.querySelectorAll("div,p,h1,h2,h3,span,li,td,th,i,b,text,svg").forEach((el) => {
      const q = el.getBoundingClientRect();
      if (!q.width || !q.height) return;
      if (q.bottom > r.bottom + 4 || q.right > r.right + 4 || q.left < r.left - 4 || q.top < r.top - 4) {
        const t = (el.textContent || "").trim().slice(0, 44);
        if (t) out.push(t);
      }
    });
    return [...new Set(out)].slice(0, 4);
  });
  if (bad.length) overflow.push({ slide: i + 1, bad });
}
console.log(JSON.stringify({ route: ROUTE, slides: n, overflow, errs }, null, 1));

// ── 页序表 ─────────────────────────────────────────────
const toc = await pg.evaluate(() =>
  window.deck.slides.map((s, i) => {
    const c = s.querySelector(".chrome span");
    const h = s.querySelector("h2, .cn, .q i, .cc-title");
    return `${String(i + 1).padStart(2, "0")}  ${(c ? c.textContent : (s.querySelector(".act") ? "ACT" : "—")).trim().slice(0, 30).padEnd(30)}  ${(h ? h.textContent : "").trim().slice(0, 40)}`;
  })
);
console.log("\n=== TOC ===\n" + toc.join("\n"));

// ── 关键词断言 ──────────────────────────────────────────
const kw = await pg.evaluate(() => {
  const t = document.body.textContent;
  const want = ["主论坛 · 身份 ⇒ 角色一致性", "主论坛 · 关系 × 历史 ⇒ 共同记忆", "主论坛 · 实时引擎，早就在做 ⇒ 可控临场",
    "ONE TIMELINE", "同一条时间线", "P90 E2E LATENCY < 1.5S", "从人说完最后一个字，到人听到 Agent 说出第一个字",
    "与 Tolan 工程团队一手交流", "接下来只看一件事", "这一幕不讲知识点，只回答五个问题",
    "不是端到端赢了，是异步双模型", "two-model architecture", "会死的是串行，不会死的是分工",
    "6 RTT → 2 RTT", "Active Internet-Draft", "说了不该说的话", "动作延迟"];
  return { missing: want.filter((w) => !t.includes(w)), designSample: (t.match(/设计样例/g) || []).length };
});
console.log("\n=== KEYWORDS ===\n" + JSON.stringify(kw));

// ── 定点截图 ────────────────────────────────────────────
const shots = [["f-p11-multipliers", 10], ["f-p14-ring", 13], ["f-p20-northstar", 19],
  ["f-act04-overview", 21], ["f-video", 25], ["f-gptlive", 26], ["f-q4", 27], ["f-q5", 28], ["f-q1", 22], ["f-q2", 23]];
for (const [name, idx] of shots) {
  await pg.evaluate((k) => window.deck.go(k), idx);
  await pg.waitForTimeout(1500);
  await pg.evaluate(() => { const s = window.deck.slides[window.deck.i]; s.querySelectorAll("[data-step]").forEach((e) => e.classList.add("on")); });
  await pg.waitForTimeout(600);
  await pg.screenshot({ path: `/tmp/qa/${name}.png` });
}

// ── 视频页行为：第一按播 / 第二按翻页 / poster / 兜底 ───────
const VIDX = 25; // 0-based → 第 26 页
await pg.evaluate((k) => window.deck.go(k), VIDX);
await pg.waitForTimeout(900);
const v0 = await pg.evaluate(() => {
  const v = window.deck.slides[window.deck.i].querySelector("video");
  return { has: !!v, poster: v && v.getAttribute("poster"), paused: v && v.paused, i: window.deck.i };
});
await pg.keyboard.press("ArrowRight");
await pg.waitForTimeout(900);
const v1 = await pg.evaluate(() => {
  const v = window.deck.slides[25].querySelector("video");
  return { i: window.deck.i, paused: v.paused, err: v.error && v.error.code, t: v.currentTime };
});
await pg.keyboard.press("ArrowRight");
await pg.waitForTimeout(700);
const v2 = await pg.evaluate(() => ({ i: window.deck.i }));
await pg.evaluate((k) => window.deck.go(k), VIDX);
await pg.waitForTimeout(500);
await pg.keyboard.press("f");
await pg.waitForTimeout(500);
const v3 = await pg.evaluate(() => {
  const s = window.deck.slides[25];
  return { fallback: !!s.querySelector(".vstills") && getComputedStyle(s.querySelector(".vstills")).display };
});
console.log("\n=== VIDEO ===\n" + JSON.stringify({ v0, v1, v2, v3 }));

await b.close();
console.log("\nDONE · errs=" + errs.length + " overflow=" + overflow.length);
