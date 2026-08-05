// QA：/cowork-confv2 43 页走查（R8 聚焦版）+ P3 录音按键行为 + 无视频断言 + 灰字提亮核对
// 与 qa-media.mjs 分工：那支跑线上 55 页版（/cowork-conf，含视频页），这支只跑 43 页预览版。
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");

const exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const b = await chromium.launch({ executablePath: exe, args: ["--autoplay-policy=no-user-gesture-required", "--mute-audio"] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = [];
pg.on("pageerror", (e) => errs.push("pageerror: " + e.message));
let fail = 0;
const chk = (ok, label) => { if (!ok) fail++; console.log((ok ? "✓ " : "✗ ") + label); };

// ── 1) 43 页全量走查（含 data-step 推满 + 溢出检查） ──
await pg.goto("http://localhost:3000/cowork-confv2", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides && window.deck.slides.length === 43);
const n = await pg.evaluate(() => window.deck.slides.length);
let overflow = [];
for (let i = 0; i < n; i++) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(120);
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
chk(n === 43, `页数 = 43（实测 ${n}）`);
chk(overflow.length === 0, `零溢出（溢出页 ${JSON.stringify(overflow)}）`);

// ── 2) 媒体行为 · P3 录音（第一按播，第二按停 + 翻页） ──
await pg.evaluate(() => window.deck.go(2));
await pg.waitForTimeout(300);
await pg.keyboard.press("ArrowRight");
await pg.waitForTimeout(600);
const a1 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[2].querySelector("[data-dm]");
  return { i: d.i, playing: !!x && !x.paused, ind: d.slides[2].classList.contains("dm-playing") };
});
await pg.keyboard.press("ArrowRight");
await pg.waitForTimeout(400);
const a2 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[2].querySelector("[data-dm]");
  return { i: d.i, paused: !!x && x.paused, ind: d.slides[2].classList.contains("dm-playing") };
});
chk(a1.i === 2 && a1.playing && a1.ind, `P3 第一按播放 ${JSON.stringify(a1)}`);
chk(a2.i === 3 && a2.paused, `P3 第二按停 + 翻页 ${JSON.stringify(a2)}`);

// ── 3) 媒体资产：全场只剩 P3 一处录音，视频页已随陪伴章撤除 ──
const mcount = await pg.evaluate(() => ({
  dm: document.querySelectorAll("[data-dm]").length,
  video: document.querySelectorAll("video").length,
  vslide: document.querySelectorAll(".vslide").length,
  mp4: document.documentElement.innerHTML.includes("gemini-demo.mp4"),
}));
chk(mcount.dm === 1 && mcount.video === 0 && mcount.vslide === 0 && !mcount.mp4,
    `媒体资产 = 仅 P3 录音，无视频 ${JSON.stringify(mcount)}`);

// ── 4) M 键手动播 / 停 ──
await pg.evaluate(() => window.deck.go(2));
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(500);
const m1 = await pg.evaluate(() => !window.deck.slides[2].querySelector("[data-dm]").paused);
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(200);
const m2 = await pg.evaluate(() => {
  const d = window.deck;
  return { stopped: d.slides[2].querySelector("[data-dm]").paused, still: d.i };
});
chk(m1 && m2.stopped && m2.still === 2, `M 键播/停不翻页 ${JSON.stringify({ m1, ...m2 })}`);

// ── 5) 视觉第一刀：灰字 token 提亮 + 次级文字 +2px 生效 ──
const tok = await pg.evaluate(() => {
  const cs = getComputedStyle(document.documentElement);
  const g = (k) => cs.getPropertyValue(k).trim();
  const note = document.querySelector(".note");
  // 多行 note 的 clip-path 修复：.note 下的 .flow 包裹层必须全是 inline-block
  const wraps = [...document.querySelectorAll(".note > .flow")];
  return {
    ink2: g("--ink-2"), ink3: g("--ink-3"), mark3: g("--mark-3"),
    noteFs: note ? getComputedStyle(note).fontSize : null,
    wrapN: wraps.length,
    wrapBad: wraps.filter((e) => getComputedStyle(e).display !== "inline-block").length,
  };
});
chk(tok.ink3 === "#D9D9E3" && tok.ink2 === "#E8E8F0" && tok.mark3 === "#A5A5A5",
    `token 提亮 --ink-3=#D9D9E3 / --ink-2=#E8E8F0 / --mark-3 保留原灰 ${JSON.stringify(tok)}`);
chk(tok.noteFs === "24px", `.note 字号 24px（+2px）实测 ${tok.noteFs}`);
chk(tok.wrapN > 0 && tok.wrapBad === 0,
    `多行 note clip-path 修复在位：${tok.wrapN} 个 .note>.flow 全 inline-block（异常 ${tok.wrapBad}）`);

// ── 6) 结构：PART 0–4 五幕 / 金句 01–05 / 陪伴章清零 ──
const txt = await pg.evaluate(() => document.body.innerText);
const html = await pg.evaluate(() => document.documentElement.innerHTML);
chk(html.includes("PART 2 · 被托付") && html.includes("PART 3 · 双向奔赴") && html.includes("PART 4 · 人与组织"),
    "PART 重编号 2/3/4 在位");
chk(!html.includes("PART 5") && !html.includes("PART 2 · 被记住"), "五幕编号 / 陪伴幕卡已清零");
chk(html.includes("观点页 · 嘉宾金句 · 05") && !html.includes("观点页 · 嘉宾金句 · 06"), "金句重编号 01–05");
chk(html.includes("下午 AIoT 专场"), "P9 分论坛预告在位");
chk(!txt.includes("上一幕") && !txt.includes("第五幕"), "悬空幕序指涉清零");

// ── 7) 封面 title ──
await pg.evaluate(() => window.deck.go(0));
await pg.waitForTimeout(400);
await pg.screenshot({ path: "/tmp/qa/confv2-cover.png" });
chk(await pg.evaluate(() => document.body.textContent.includes("声网 AI 产品线负责人")), "封面 title 线字");

// ── 8) /cowork-conf 线上版未被波及：仍 55 页 + 视频页在 ──
await pg.goto("http://localhost:3000/cowork-conf", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides);
const base = await pg.evaluate(() => ({
  slides: window.deck.slides.length,
  video: document.querySelectorAll("video[data-dm]").length,
  ink3: getComputedStyle(document.documentElement).getPropertyValue("--ink-3").trim(),
}));
chk(base.slides === 55 && base.video === 1 && base.ink3 === "#A5A5A5",
    `/cowork-conf 未被波及：55 页 + 视频在 + --ink-3 原值 ${JSON.stringify(base)}`);

console.log("pageerrors:", errs.length ? errs : "none");
console.log(fail === 0 && errs.length === 0 ? "QA confv2 · ALL GREEN" : `QA confv2 · FAIL ${fail}`);
await b.close();
process.exit(fail === 0 && errs.length === 0 ? 0 : 1);
