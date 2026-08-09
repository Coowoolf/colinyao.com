// QA · robot26 北京站还原 + R24 内容演进（37 页 · 单一视觉 · 纯黑底）
// ─────────────────────────────────────────────────────────────────────────
// 骨架仿 conf 家族（qa-confv2.mjs / qa-aiot26-conf-c7.mjs）。检查项：
//   ① 37 页 · 零 pageerror · deck 初始化
//   ② 逐页分步数 = PPT 的单击次数（动线表，见 robot26-动效动线研究.md）
//   ③ 零溢出：所有可见文字的行盒都在 1920×1080 舞台内；有填充/描边的卡片不漏字
//   ④ --len 机检：每条 .dw/.dwa 的 --len 与它自己的 getTotalLength() 对得上
//   ⑤ 填充率表：逐页 ink 覆盖率（太空/太满都会在这里露出来）
//   ⑥ 视频锚点：P22 的 <video data-play-step> 在位、poster/src 可达
//   ⑦ 资产 200：所有 /decks/assets/robot26/* 都能取到
// R22 增补（换 Colin 暗色模板 / 会场痕迹清零 / 金句校号 / mono 裁字）：
//   ⑧ 会场痕迹清零：双 logo 条与「RTE 2026 春夏巡游」在源码与 DOM 里都为 0
//   ⑨ 模板 token 在位：底流场 8 条曲线 / 栏线网格 / 上下导轨 / 34 页落款 / slide 背景 transparent
//   ⑩ 金句连号：3 张金句页 MONEY QUOTE · 01–03 OF 03，PIN 与 MQ 同号（R24：MQ04 删页）
//   ⑪ mono 标签零裁切：点名的一族逐个实测行数 = 1，且行盒不越过容器内边界
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
const STEPS = [0, 5, 0, 0, 4, 5, 0, 0, 8, 5, 2, 3, 3, 5, 6, 4, 4, 3, 3, 0,
               1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];  // R24：37 页

// 容器 chromium 无 H.264：P22 视频必然报这个，白名单豁免
const MEDIA_EXEMPT = /err:?\s*4|MEDIA_ELEMENT_ERROR|DEMUXER_ERROR|not supported|NotSupportedError/i;

// R22 · 会场痕迹黑名单（源码级 grep，命中即 FAIL）
const VENUE = [/logo-woshipm/i, /logo-rte/i, /woshipm/i, /人人都是产品经理/, /起点课堂/, /春夏巡游/, /RTE\s*2026/i];
// R22 · mono 标签零裁切名单：(页, data-sid) —— 这一族必须单行
const MONO_ONE_LINE = [  // R24 顺延（P11 拆三 +2 · 老 P33 删 −1）
  [2, "28"], [3, "10"], [6, "46"], [7, "4"], [19, "5"], [23, "31"], [32, "49"],   // 来源行 / 出处角标
  [11, "a7"], [12, "b10"],                                                        // R24 新来源行
  [4, "10"], [26, "10"], [27, "4"],                                               // ★ MONEY QUOTE
  [4, "14"], [26, "16"], [27, "17"],                                              // 钉子 · PIN
  [2, "2"], [3, "2"], [5, "2"], [6, "2"], [7, "2"], [8, "2"], [9, "2"], [10, "2"],
  [11, "a2"], [12, "b2"], [13, "2"], [14, "2"], [15, "2"], [16, "2"], [17, "2"],
  [18, "2"], [19, "3"], [20, "2"], [21, "2"], [22, "2"], [23, "2"], [25, "2"],
  [28, "2"], [29, "2"], [30, "2"], [31, "2"], [32, "2"], [33, "3"], [34, "2"],
  [35, "2"], [37, "8"],                                                           // eyebrow
];

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
if (n !== 37) fails.push(`页数 ${n} ≠ 37`);

// ── ② 分步数 ────────────────────────────────────────────────────────────
const got = await pg.evaluate(() => window.deck.maxStep);
STEPS.forEach((want, i) => {
  if (got[i] !== want) fails.push(`P${i + 1} 分步数 ${got[i]} ≠ 动线表 ${want}`);
});

// ── ⑧ R22 · 会场痕迹清零（源码 grep + DOM 图片清点）──────────────────────
const SRC = fs.readFileSync("public/decks/robot26.html", "utf8");
VENUE.forEach((re) => { if (re.test(SRC)) fails.push(`会场痕迹残留（源码）：${re}`); });
const imgs = await pg.evaluate(() => [...document.querySelectorAll(".slide img")].map((el) => el.getAttribute("src")));
imgs.filter((s) => !/^data:/.test(s || "")).forEach((s) => {
  if (/logo|woshipm|rte-tour/i.test(s || "")) fails.push(`会场痕迹残留（DOM img）：${s}`);
});
for (const f of ["logo-woshipm.webp", "logo-rte-tour.webp"])
  if (fs.existsSync(`public/decks/assets/robot26/${f}`)) fails.push(`会场 logo 资产未删：${f}`);

// ── ⑫ R23 · 封面背景板：峰会 keyart 清零 + P1/P36 黑字翻 --ink ────────────
if (/cover-ai\.jpg/.test(SRC)) fails.push("R23：cover-ai.jpg 仍被源码引用");
if (fs.existsSync("public/decks/assets/robot26/cover-ai.jpg")) fails.push("R23：cover-ai.jpg 资产未删");
const covers = await pg.evaluate(() => [1, 37].map((p) => {
  const s = document.querySelector(`.slide[data-p="${p}"]`);
  return { p, black: (s.innerHTML.match(/color:#000000/g) || []).length,
           keyart: [...s.querySelectorAll("img")].some((el) => /cover-ai/.test(el.getAttribute("src") || "")),
           inkVar: (s.innerHTML.match(/color:var\(--ink\)/g) || []).length };
}));
covers.forEach(({ p, black, keyart, inkVar }) => {
  if (black) fails.push(`R23：P${p} 残留黑字 ${black} 处`);
  if (keyart) fails.push(`R23：P${p} 仍挂满幅 keyart`);
  if (!inkVar) fails.push(`R23：P${p} 未见 var(--ink) 文字（翻色未生效？）`);
});

// ── ⑬ R24 · P11 拆三 / 老 P13 严谨化 / MQ04 删页 ─────────────────────────
if (!/one billion words/.test(SRC)) fails.push("R24：P11 Ilya 引文缺失");
if (!/NVIDIA GTC SPRING 2023/.test(SRC)) fails.push("R24：P11 引文来源行缺失");
if (!/一道|四步/.test(SRC) || !/167 万分钟/.test(SRC)) fails.push("R24：P12 推演链不完整");
if (!/我们的一生只有 0.29TB/.test(SRC)) fails.push("R24：P12 口径行缺失");
if (!/记忆配额上限/.test(SRC)) fails.push("R24：P13 伙伴线读数缺失");
if (/具身智能明天直接抄|embodied AI copies tomorrow|浪潮的第一站/.test(SRC)) fails.push("R24：MQ04 文案残留（页已删）");
if (/2024 →/.test(SRC)) fails.push("R24：老 P13 era 标签未改（2024 → 应为 2022 →）");
if (!/2022 →/.test(SRC) || !/ChatGPT → GPT-4o/.test(SRC)) fails.push("R24：30 年坐标严谨化未落地");

// ── ⑨ R22 · 模板 token 在位 ─────────────────────────────────────────────
const tpl = await pg.evaluate(() => ({
  flow: document.querySelectorAll(".deck-stage > .deck-flow path").length,
  grid: !!document.querySelector(".deck-stage > .deck-grid"),
  rail: document.querySelectorAll(".deck-stage > .deck-rail").length,
  sig: [...document.querySelectorAll(".slide .sig")].map((el) => +el.closest(".slide").dataset.p),
  sigText: (document.querySelector(".slide .sig") || {}).textContent || "",
  slideBg: getComputedStyle(document.querySelector(".slide")).backgroundColor,
}));
if (tpl.flow !== 8) fails.push(`底流场曲线 ${tpl.flow} 条 ≠ 8`);
if (!tpl.grid) fails.push("栏线网格 .deck-grid 缺失");
if (tpl.rail !== 2) fails.push(`发丝导轨 ${tpl.rail} 条 ≠ 2`);
if (tpl.sig.length !== 34) fails.push(`落款页数 ${tpl.sig.length} ≠ 34（1/24/37 三页不挂）`);
if ([1, 24, 37].some((p) => tpl.sig.includes(p))) fails.push("落款挂到了满幅页（1/24/37）");
if (!/colinyao\.com/i.test(tpl.sigText)) fails.push(`落款文案异常：${tpl.sigText}`);
if (!/rgba\(0, 0, 0, 0\)|transparent/.test(tpl.slideBg)) fails.push(`slide 背景 ${tpl.slideBg} 不透明，底流场会被盖住`);

// ── ⑩ R22 · 金句连号 ────────────────────────────────────────────────────
const mq = [...SRC.matchAll(/MONEY QUOTE · (\d+) OF (\d+)/g)].map((m) => [m[1], m[2]]);
const pin = [...SRC.matchAll(/钉子 · PIN (\d+)/g)].map((m) => m[1]);
if (mq.length !== 3) fails.push(`金句页 ${mq.length} 张 ≠ 3`);
mq.forEach(([i2, of], k) => {
  if (i2 !== String(k + 1).padStart(2, "0")) fails.push(`金句序号错位：第 ${k + 1} 张标了 ${i2}`);
  if (of !== "03") fails.push(`金句总数标成 OF ${of}，应为 OF 03`);
});
if (pin.join(",") !== "01,02,03") fails.push(`PIN 角标序列 ${pin.join(",")} ≠ 01,02,03`);
if (mq.map((x) => x[0]).join(",") !== pin.join(",")) fails.push("MQ 与 PIN 编号不同号");

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
for (let i = 1; i <= 37; i++) {
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
    // ⑪ R22 · mono 标签零裁切：点名的一族逐个量行数 + 量行盒有没有超出容器内边界
    out.mono = [];
    sec.querySelectorAll(".tx").forEach((el) => {
      const cs = getComputedStyle(el);
      const inner = { l: el.getBoundingClientRect().left + parseFloat(cs.paddingLeft || 0),
                      r: el.getBoundingClientRect().right - parseFloat(cs.paddingRight || 0) };
      el.querySelectorAll("p").forEach((p) => {
        const bd = bands(p);
        const rg = document.createRange(); rg.selectNodeContents(p);
        const rs = [...rg.getClientRects()].filter((x) => x.height > 1);
        const over = rs.length ? Math.max(0, Math.max(...rs.map((x) => x.right)) - inner.r,
                                             inner.l - Math.min(...rs.map((x) => x.left))) : 0;
        // 容差 = 本段最大字距：R22 给行尾 run 挂了等量负 margin 把尾字距收回来，
        // 于是 inline 盒会比容器右缘外探正好一个字距 —— 字形本身是贴齐的，不是溢出。
        const tol = Math.max(0, ...[...p.querySelectorAll("span")]
          .map((sp) => parseFloat(getComputedStyle(sp).letterSpacing) || 0)) + 0.6;
        out.mono.push([el.dataset.sid, bd.length, +Math.max(0, over - tol).toFixed(1),
                       p.textContent.trim().slice(0, 34)]);
      });
    });
    return out;
  });
  fillTable.push([i, r.boxes, r.ink]);
  r.over.forEach((o) => fails.push(`P${i} ${o[0]} sid=${o[1]}「${o[2]}」`));
  MONO_ONE_LINE.filter((x) => x[0] === i).forEach(([, sid]) => {
    const hit = r.mono.find((m) => m[0] === sid);
    if (!hit) fails.push(`P${i} mono 标签 sid=${sid} 找不到`);
    else if (hit[1] !== 1) fails.push(`P${i} mono 标签 sid=${sid}「${hit[3]}」折成 ${hit[1]} 行（裁字）`);
    else if (hit[2] > 0.6) fails.push(`P${i} mono 标签 sid=${sid}「${hit[3]}」越界 ${hit[2]}px`);
  });
  await pg.screenshot({ path: `${SHOT}/p${String(i).padStart(2, "0")}.png` });
}

// ── ⑥ 视频锚点 ──────────────────────────────────────────────────────────
const vid = await pg.evaluate(() => {
  const v = document.querySelector("video[data-play-step]");
  if (!v) return null;
  return { step: v.dataset.playStep, src: v.getAttribute("src"), poster: v.getAttribute("poster"),
           page: v.closest(".slide").dataset.p };
});
if (!vid) fails.push("P24 视频锚点缺失");
else if (vid.page !== "24" || vid.step !== "1") fails.push(`视频锚点错位：${JSON.stringify(vid)}`);

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
console.log("\n" + (fails.length ? "QA FAIL\n" + fails.join("\n") : "QA PASS · 37 页零溢出零 pageerror · 分步数逐页对齐动线表"));
await b.close();
process.exit(fails.length ? 1 : 0);
