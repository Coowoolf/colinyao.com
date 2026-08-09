// QA · robot26 北京站 PPT 一比一还原（36 页 · 单一视觉 · 纯黑底）
// ─────────────────────────────────────────────────────────────────────────
// 骨架仿 conf 家族（qa-confv2.mjs / qa-aiot26-conf-c7.mjs）。检查项：
//   ① 36 页 · 零 pageerror · deck 初始化
//   ② 逐页分步数 = PPT 的单击次数（动线表，见 robot26-动效动线研究.md）
//   ③ 零溢出：所有可见文字的行盒都在 1920×1080 舞台内；有填充/描边的卡片不漏字
//   ④ --len 机检：每条 .dw/.dwa 的 --len 与它自己的 getTotalLength() 对得上
//   ⑤ 填充率表：逐页 ink 覆盖率（太空/太满都会在这里露出来）
//   ⑥ 视频锚点：P22 的 <video data-play-step> 在位、poster/src 可达
//   ⑦ 资产 200：所有 /decks/assets/robot26/* 都能取到
// 已知豁免：容器 chromium 无 H.264 解码，P22 的 <video> 必然抛 `err:4`（MEDIA_ELEMENT_ERROR）
//   —— 与 scripts/qa-media.mjs 同一处理，白名单放行，不算 pageerror。
//
// 用法：(cd public && python3 -m http.server 8899 &) ; node scripts/qa-robot26.mjs
//       或先 npm run dev（3000 端口），传 PORT=3000 走路由 /robot26。
import { chromium } from "playwright-core";
import { execSync } from "child_process";
import fs from "fs";

const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const PORT = process.env.PORT || 8899;
const URL = PORT === "3000" ? "http://localhost:3000/robot26"
                            : `http://localhost:${PORT}/decks/robot26.html`;
const SHOT = "/tmp/qa/robot26";
fs.mkdirSync(SHOT, { recursive: true });

// PPT <p:timing> 的逐页单击次数（P22 的 1 步 = mediacall playFrom(0)）
const STEPS = [0, 5, 0, 0, 4, 5, 0, 0, 8, 5, 4, 5, 6, 4, 4, 3, 3, 0, 1, 0,
               0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

// 容器 chromium 无 H.264：P22 视频必然报这个，白名单豁免
const MEDIA_EXEMPT = /err:?\s*4|MEDIA_ELEMENT_ERROR|DEMUXER_ERROR|not supported|NotSupportedError/i;

const fails = [], warn = [];
const b = await chromium.launch({ executablePath: exe, args: ["--force-color-profile=srgb"] });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const pg = await ctx.newPage();
const errs = [], media = [], bad404 = [];
pg.on("pageerror", (e) => (MEDIA_EXEMPT.test(String(e)) ? media : errs).push(String(e)));
pg.on("console", (m) => { if (m.type() === "error" && MEDIA_EXEMPT.test(m.text())) media.push(m.text()); });
pg.on("response", (r) => { if (r.status() >= 400) bad404.push(r.status() + " " + r.url()); });

await pg.goto(URL, { waitUntil: "networkidle" });
await pg.evaluate(() => document.fonts.ready);
const n = await pg.evaluate(() => window.deck?.slides.length || 0);
if (n !== 36) fails.push(`页数 ${n} ≠ 36`);

// ── ② 分步数 ────────────────────────────────────────────────────────────
const got = await pg.evaluate(() => window.deck.maxStep);
STEPS.forEach((want, i) => {
  if (got[i] !== want) fails.push(`P${i + 1} 分步数 ${got[i]} ≠ 动线表 ${want}`);
});

// ── ④ --len 机检 ────────────────────────────────────────────────────────
const lenBad = await pg.evaluate(() => {
  const out = [];
  document.querySelectorAll("svg .dw, svg .dwa").forEach((el) => {
    const declared = parseFloat(getComputedStyle(el).getPropertyValue("--len"));
    let real;
    if (el.tagName === "circle") {
      // .dwa 的 --len 是弧长（周长 × 百分比），真值按 --rest（整周长）反推
      const rest = parseFloat(getComputedStyle(el).getPropertyValue("--rest"));
      real = 2 * Math.PI * el.r.baseVal.value;
      if (Math.abs(real - rest) > 1.5) out.push(["circle --rest", rest, real]);
      return;
    }
    real = el.getTotalLength ? el.getTotalLength() : NaN;
    if (!isFinite(declared) || !isFinite(real)) { out.push(["nan", declared, real]); return; }
    // 声明值必须 ≥ 实长（不然线画不满），且不得夸大 6% 以上（不然起手会「秒出」一截）
    if (declared < real - 1 || declared > real * 1.06 + 4) out.push([el.getAttribute("d")?.slice(0, 28) || "", declared, Math.round(real)]);
  });
  return out;
});
if (lenBad.length) fails.push(`--len 与路径实长不符 ${lenBad.length} 处：` + JSON.stringify(lenBad.slice(0, 6)));

// ── ③ 溢出 + ⑤ 填充率，逐页 ──────────────────────────────────────────────
const fillTable = [];
for (let i = 1; i <= 36; i++) {
  await pg.evaluate((k) => window.deck.go(k), i - 1);
  await pg.evaluate(() => { const d = window.deck; d.step = d.maxStep[d.i]; d.applySteps(); });
  await pg.waitForTimeout(2400);          // 入场 ~1.64s + dw 1.6s+0.44s 错峰 → 2.4s 才拍得到全字
  const r = await pg.evaluate(() => {
    const sec = document.querySelector(".slide.active");
    const stage = document.getElementById("deckStage").getBoundingClientRect();
    const out = { over: [], boxes: 0, ink: 0 };
    const bands = (p) => {
      const rg = document.createRange(); rg.selectNodeContents(p);
      const rs = [...rg.getClientRects()].filter((x) => x.height > 1).sort((a, c) => a.top - c.top);
      if (!rs.length) return [];
      const o = [{ top: rs[0].top, bot: rs[0].bottom, left: rs[0].left, right: rs[0].right }];
      for (const x of rs.slice(1)) {
        const l = o[o.length - 1];
        if (x.top < l.bot - 2) { l.bot = Math.max(l.bot, x.bottom); l.right = Math.max(l.right, x.right); l.left = Math.min(l.left, x.left); }
        else o.push({ top: x.top, bot: x.bottom, left: x.left, right: x.right });
      }
      return o;
    };
    sec.querySelectorAll(".tx").forEach((el) => {
      const cs = getComputedStyle(el);
      const carded = cs.backgroundColor !== "rgba(0, 0, 0, 0)" || parseFloat(cs.borderTopWidth) > 0;
      const box = el.getBoundingClientRect();
      el.querySelectorAll("p").forEach((p) => {
        for (const bd of bands(p)) {
          if (bd.bot > stage.bottom + 1 || bd.top < stage.top - 1 ||
              bd.right > stage.right + 1 || bd.left < stage.left - 1)
            out.over.push(["出台", el.dataset.sid, p.textContent.trim().slice(0, 18)]);
          else if (carded && (bd.bot > box.bottom + 2 || bd.right > box.right + 2))
            out.over.push(["漏卡", el.dataset.sid, p.textContent.trim().slice(0, 18)]);
        }
      });
    });
    // 填充率：所有可见 .sh 的并集面积 / 舞台面积（粗粒度，够看空/满）
    const cells = new Set();
    sec.querySelectorAll(".sh").forEach((el) => {
      const b2 = el.getBoundingClientRect();
      if (b2.width < 2 || b2.height < 2) return;
      out.boxes++;
      const x0 = Math.max(0, Math.floor((b2.left - stage.left) / 32));
      const x1 = Math.min(59, Math.floor((b2.right - stage.left) / 32));
      const y0 = Math.max(0, Math.floor((b2.top - stage.top) / 32));
      const y1 = Math.min(33, Math.floor((b2.bottom - stage.top) / 32));
      for (let x = x0; x <= x1; x++) for (let y = y0; y <= y1; y++) cells.add(x + ":" + y);
    });
    out.ink = Math.round((cells.size / (60 * 34)) * 100);
    return out;
  });
  fillTable.push([i, r.boxes, r.ink]);
  r.over.forEach((o) => fails.push(`P${i} ${o[0]} sid=${o[1]}「${o[2]}」`));
  await pg.screenshot({ path: `${SHOT}/p${String(i).padStart(2, "0")}.png` });
}

// ── ⑥ 视频锚点 ──────────────────────────────────────────────────────────
const vid = await pg.evaluate(() => {
  const v = document.querySelector("video[data-play-step]");
  if (!v) return null;
  return { step: v.dataset.playStep, src: v.getAttribute("src"), poster: v.getAttribute("poster"),
           page: v.closest(".slide").dataset.p };
});
if (!vid) fails.push("P22 视频锚点缺失");
else if (vid.page !== "22" || vid.step !== "1") fails.push(`视频锚点错位：${JSON.stringify(vid)}`);

// ── ⑦ 资产可达 ──────────────────────────────────────────────────────────
if (bad404.length) fails.push("资产 4xx/5xx：" + bad404.slice(0, 5).join(" | "));

console.log("\n填充率表（页 · shape 数 · ink%）");
console.log(fillTable.map(([p, b2, k]) => `P${String(p).padStart(2)}  ${String(b2).padStart(3)}  ${String(k).padStart(3)}%`).join("\n"));
const inks = fillTable.map((x) => x[2]);
console.log(`ink 区间 ${Math.min(...inks)}%–${Math.max(...inks)}%  中位 ${inks.slice().sort((a, c) => a - c)[18]}%`);
console.log("\n视频锚点:", JSON.stringify(vid));
const h264 = await pg.evaluate(() => document.createElement("video").canPlayType('video/mp4; codecs="avc1.42E01E"') || "(空=不支持)");
console.log("chromium H.264 支持:", h264, "· 媒体类报错（已豁免）:", media.length ? media.length + " 条，例：" + media[0].slice(0, 80) : "0 条");
console.log("pageerrors:", errs.length ? errs : "none");
if (errs.length) fails.push("pageerror ×" + errs.length);
console.log("\n" + (fails.length ? "QA FAIL\n" + fails.join("\n") : "QA PASS · 36 页零溢出零 pageerror · 分步数逐页对齐动线表"));
await b.close();
process.exit(fails.length ? 1 : 0);
