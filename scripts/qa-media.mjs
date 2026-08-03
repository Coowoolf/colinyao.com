// QA：/cowork-conf 66 页走查 + 媒体按键行为（PPT 对齐）+ /cowork 回归
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");

const exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const b = await chromium.launch({ executablePath: exe, args: ["--autoplay-policy=no-user-gesture-required", "--mute-audio"] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = [];
pg.on("pageerror", (e) => errs.push("pageerror: " + e.message));

// ── 1) /cowork-conf 全量走查（含 data-step 推进 + 溢出检查） ──
await pg.goto("http://localhost:3000/cowork-conf", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides && window.deck.slides.length === 63);
const n = await pg.evaluate(() => window.deck.slides.length);
let overflow = [];
for (let i = 0; i < n; i++) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(120);
  // 推满 data-step（媒体页 go 后 next 会先播——走查用 forceStep 直接置步）
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  });
  await pg.waitForTimeout(60);
  const bad = await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i], r = s.getBoundingClientRect(), out = [];
    s.querySelectorAll("div,p,h1,h2,h3,span,li,td,th").forEach((el) => {
      if (!el.offsetParent) return;
      const b2 = el.getBoundingClientRect();
      if (b2.width && b2.height && (b2.bottom > r.bottom + 4 || b2.right > r.right + 4)) {
        const t = (el.textContent || "").trim().slice(0, 40);
        if (t) out.push(t);
      }
    });
    return out.slice(0, 3);
  });
  if (bad.length) overflow.push({ slide: i + 1, bad });
}
console.log("conf slides:", n, "| overflow:", JSON.stringify(overflow));

// ── 2) 媒体行为 · P3 录音 ─────────────────────────────
await pg.evaluate(() => window.deck.go(2));
await pg.waitForTimeout(300);
await pg.keyboard.press("ArrowRight"); // 第一按：播
await pg.waitForTimeout(600);
const a1 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[2].querySelector("[data-dm]");
  return { i: d.i, playing: !!x && !x.paused, ind: d.slides[2].classList.contains("dm-playing"), t: x ? x.currentTime : -1 };
});
await pg.screenshot({ path: "/tmp/qa/conf-p3-playing.png" });
await pg.keyboard.press("ArrowRight"); // 第二按：停 + 翻页
await pg.waitForTimeout(400);
const a2 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[2].querySelector("[data-dm]");
  return { i: d.i, paused: !!x && x.paused, ind: d.slides[2].classList.contains("dm-playing") };
});
console.log("P3 第一按:", JSON.stringify(a1), "→ 第二按:", JSON.stringify(a2));

// ── 3) 媒体行为 · 视频页（自然走入 → 播 → 翻页） ──
await pg.evaluate(() => window.deck.go(22));
await pg.waitForTimeout(300);
// 推满 P24 的 step 后再前进
await pg.evaluate(() => {
  const d = window.deck, s = d.slides[22];
  const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
  for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  if (d.step !== undefined) d.step = mx;
});
await pg.keyboard.press("ArrowRight"); // 进入视频页（不播）
await pg.waitForTimeout(400);
const v0 = await pg.evaluate(() => ({ i: window.deck.i }));
await pg.keyboard.press("ArrowRight"); // 第一按：播视频
await pg.waitForTimeout(900);
const v1 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[23].querySelector("video[data-dm]");
  return { i: d.i, playing: !!x && !x.paused, ind: d.slides[23].classList.contains("dm-playing"), err: x && x.error ? x.error.code : 0, canH264: document.createElement('video').canPlayType('video/mp4; codecs="avc1.42E01E"') };
});
await pg.screenshot({ path: "/tmp/qa/conf-p25-video.png" });
await pg.keyboard.press("ArrowRight"); // 第二按：停 + 翻页
await pg.waitForTimeout(400);
const v2 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[23].querySelector("video[data-dm]");
  return { i: d.i, paused: !!x && x.paused };
});
console.log("进入P25:", JSON.stringify(v0), "第一按:", JSON.stringify(v1), "→ 第二按:", JSON.stringify(v2));

// ── 4) prev 复位 + P 键 ───────────────────────────────
await pg.evaluate(() => window.deck.go(23));
await pg.keyboard.press("ArrowRight");
await pg.waitForTimeout(500);
await pg.keyboard.press("ArrowLeft"); // prev：停 + 回上一页
await pg.waitForTimeout(300);
const r1 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[23].querySelector("video[data-dm]");
  return { i: d.i, paused: x.paused, t: +x.currentTime.toFixed(2) };
});
await pg.evaluate(() => window.deck.go(2));
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(500);
const r2 = await pg.evaluate(() => {
  const x = window.deck.slides[2].querySelector("[data-dm]");
  return { pPlay: !x.paused };
});
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(200);
const r3 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[2].querySelector("[data-dm]");
  return { pStop: x.paused, still: d.i };
});
console.log("prev复位:", JSON.stringify(r1), "M键播:", JSON.stringify(r2), "M键停:", JSON.stringify(r3));

// ── 5) 封面 title + 尾页 title 截图 ───────────────────
await pg.evaluate(() => window.deck.go(0));
await pg.waitForTimeout(500);
await pg.screenshot({ path: "/tmp/qa/conf-cover-title.png" });
const titleOk = await pg.evaluate(() => document.body.textContent.includes("声网 AI 产品线负责人"));
console.log("conf title 线字:", titleOk);

// ── 6) /cowork 回归：62 页、无媒体 ─────────
await pg.goto("http://localhost:3000/cowork", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides);
const mw = await pg.evaluate(() => ({
  slides: window.deck.slides.length,
  media: document.querySelectorAll("[data-dm]").length,
  title: document.body.textContent.includes("声网 AI 产品线负责人"),
  oldTitle: /声网 AI 产品负责人/.test(document.body.textContent),
}));
console.log("/cowork:", JSON.stringify(mw));

console.log("pageerrors:", errs.length ? errs : "none");
await b.close();
