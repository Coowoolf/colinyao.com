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
//   ⑨ 模板 token 在位：底流场 8 条曲线 / 栏线网格 / 上下导轨 / slide 背景 transparent
//      + R27 改版：37 页右上角连续页码 1/37…37/37（总数派生），落款域名清零
//   ⑩ 金句连号：3 张金句页 MONEY QUOTE · 01–03 OF 03，PIN 与 MQ 同号（R24：MQ04 删页）
//   ⑪ mono 标签零裁切：点名的一族逐个实测行数 = 1，且行盒不越过容器内边界
//      （R27 手排页的单行 mono 元素挂 data-sid="r…"，同一机制续保）
// R27 增补（GPT 5.6 整体视觉优化 · 交付包 2026-08-11 · Fable review 后合入）：
//   ⑯ P2 只剩 2026 / P3 Clutch 口径 87·67·N=422 / P11 speaker 归属与官方口径一致 /
//      P5 sid28@build4 · P6 sid44/46@build5 · P14 标题 build0 常驻 / P17 build 序列 /
//      P28 五节点 timeline（大箭头清零）/ P37 页码 37/37 + 双二维码可加载；
//      非豁免 console error/warning 记 FAIL；R27 触改页逐 build 截图（/tmp/qa/robot26/builds）
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
fs.mkdirSync(`${SHOT}/builds`, { recursive: true });

// PPT <p:timing> 的逐页单击次数（P22 的 1 步 = mediacall playFrom(0)）
const STEPS = [0, 5, 0, 0, 4, 5, 0, 0, 8, 5, 2, 3, 3, 5, 6, 4, 4, 3, 3, 0,
               1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];  // R24：37 页

// 容器 chromium 无 H.264：P22 视频必然报这个，白名单豁免
const MEDIA_EXEMPT = /err:?\s*4|MEDIA_ELEMENT_ERROR|DEMUXER_ERROR|not supported|NotSupportedError/i;

// R22 · 会场痕迹黑名单（源码级 grep，命中即 FAIL）
const VENUE = [/logo-woshipm/i, /logo-rte/i, /woshipm/i, /人人都是产品经理/, /起点课堂/, /春夏巡游/, /RTE\s*2026/i];
// R22 · mono 标签零裁切名单：(页, data-sid) —— 这一族必须单行
const MONO_ONE_LINE = [  // R24 顺延（P11 拆三 +2 · 老 P33 删 −1）· R27 手排页换 r 系 sid
  [2, "28"], [6, "46"], [7, "4"], [19, "5"], [23, "31"], [32, "49"],              // 来源行 / 出处角标
  [3, "r3s"], [11, "r11s"], [12, "r12s"], [13, "r13s"],                           // R27 来源行
  [11, "r11sp"], [11, "r11t"],                                                    // R27 P11 引文卡 speaker/会话号
  [4, "r4k"], [26, "10"], [27, "4"],                                              // ★ MONEY QUOTE
  [4, "r4p"], [26, "16"], [27, "17"],                                             // 钉子 · PIN
  [2, "2"], [5, "2"], [6, "2"], [7, "2"], [8, "2"], [9, "2"], [10, "2"],
  [14, "2"], [15, "2"], [16, "2"],
  [18, "2"], [19, "3"], [20, "2"], [21, "2"], [22, "2"], [23, "2"], [25, "2"],
  [29, "2"], [30, "2"], [31, "2"], [32, "2"], [33, "3"], [34, "2"],
  [35, "2"],                                                                      // eyebrow（模型页）
  [3, "r3k"], [11, "r11k"], [12, "r12k"], [13, "r13k"], [17, "r17k"],
  [28, "r28k"], [37, "r37k"],                                                     // eyebrow（R27 手排页）
];
// R27 触改页：逐 build 截图复核（交接清单「不只检查最终态」）
const R27_PAGES = new Set([3, 4, 5, 6, 11, 12, 13, 14, 17, 19, 20, 28, 29, 37]);

const fails = [], warn = [];
const b = await chromium.launch({ executablePath: exe, args: ["--force-color-profile=srgb"] });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const pg = await ctx.newPage();
const THEME = process.env.THEME || "dark";   // R25：双主题各跑一遍（THEME=light 走浅底）
await pg.addInitScript((t) => { try { localStorage.setItem("colin-theme", t); } catch (e) {} }, THEME);
const errs = [], media = [], bad404 = [];
pg.on("pageerror", (e) => (MEDIA_EXEMPT.test(String(e)) ? media : errs).push(String(e)));
pg.on("console", (m) => {   // R27：非豁免的 console error/warning 也记 FAIL（交接清单要求双主题零告警）
  if (/favicon\.ico/.test(m.location()?.url || "")) return;   // 裸静态服务无 favicon；生产由站点框架提供，非 deck 资源
  if (MEDIA_EXEMPT.test(m.text())) { if (m.type() === "error") media.push(m.text()); return; }
  if (m.type() === "error") errs.push("console.error: " + m.text());
  if (m.type() === "warning") warn.push("console.warn: " + m.text());
});
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
if (!/记忆链/.test(SRC) || !/167 万分钟/.test(SRC)) fails.push("R24/R27：P12 推演链不完整");   // R27 重排后口径
if (!/ORDER-OF-MAGNITUDE MODEL/.test(SRC) || !/0\.29/.test(SRC)) fails.push("R24/R27：P12 数量级口径行缺失");
if (!/THE PARTNER LINE/.test(SRC) || !/关系能走多深/.test(SRC)) fails.push("R24/R27：P13 伙伴线缺失");
if (/具身智能明天直接抄|embodied AI copies tomorrow|浪潮的第一站/.test(SRC)) fails.push("R24：MQ04 文案残留（页已删）");
if (/2024 →/.test(SRC)) fails.push("R24：老 P13 era 标签未改（2024 → 应为 2022 →）");
if (!/2022 →/.test(SRC) || !/ChatGPT → GPT-4o/.test(SRC)) fails.push("R24：30 年坐标严谨化未落地");

// ── ⑭ R25 · conf 双主题：变量化 + 引导 + 切换 ────────────────────────────
if (/color:#FFFFFF|color:#D4B7F9|color:#FFFFFE/.test(SRC)) fails.push("R25：仍有未变量化的主题字面色");
if (!/html lang="zh-CN" data-theme="dark"/.test(SRC)) fails.push("R25：默认暗主题缺失");
if (!/colin-theme/.test(SRC)) fails.push("R25：colin-theme 引导/切换缺失");
if (!/deckSwap/.test(SRC)) fails.push("R25：deckSwap 按钮缺失");
const themeNow = await pg.evaluate(() => ({
  attr: document.documentElement.getAttribute("data-theme"),
  slideBg2: getComputedStyle(document.querySelector(".deck-stage")).backgroundColor,
  ink: getComputedStyle(document.querySelector(".slide")).color,
}));
if (THEME === "dark" && themeNow.attr !== "dark") fails.push("R25：dark 期望但主题态=" + themeNow.attr);
if (THEME === "light" && themeNow.attr === "dark") fails.push("R25：light 期望但主题态仍为 dark");

// ── ⑮ R26 · 浅色资产双源（交付包 2026-08-11）───────────────────────────
const LIGHT_PNGS = ["robot-face-light.png","cat-day1-light.png","cat-day30-light.png","cat-day365-light.png",
  "era-1990s-light.png","era-2010s-light.png","era-2024-light.png","era-now-light.png",
  "comfort-faces-light.png","openai-agora-light.png","living-room-light.png"];
for (const f of LIGHT_PNGS)
  if (!fs.existsSync(`public/decks/assets/robot26/${f}`)) fails.push(`R26：浅色资产缺失 ${f}`);
const dual = await pg.evaluate(() => [...document.querySelectorAll("img[data-dark-src][data-light-src]")].map((im) => ({
  src: im.getAttribute("src"), dark: im.dataset.darkSrc, light: im.dataset.lightSrc,
})));
if (dual.length !== 11) fails.push(`R26：双源图 ${dual.length} 张 ≠ 11`);
dual.forEach((d) => {
  if (THEME === "light" && !/-light\.png$/.test(d.src)) fails.push(`R26：light 下图源未切换 ${d.src}`);
  if (THEME === "dark" && !/\.webp$/.test(d.src)) fails.push(`R26：dark 下图源不是原 webp ${d.src}`);
});
const dims = await pg.evaluate(async () => {
  const out = [];
  for (const im of document.querySelectorAll("img[data-dark-src][data-light-src]")) {
    const load = (u) => new Promise((ok) => { const t = new Image(); t.onload = () => ok([t.naturalWidth, t.naturalHeight]); t.onerror = () => ok(null); t.src = u; });
    const a = await load(im.dataset.darkSrc), b = await load(im.dataset.lightSrc);
    out.push({ dark: im.dataset.darkSrc, a, b });
  }
  return out;
});
dims.forEach(({ dark, a, b }) => {
  if (!a || !b) fails.push(`R26：图加载失败 ${dark}`);
  else if (a[0] !== b[0] || a[1] !== b[1]) fails.push(`R26：尺寸不一致 ${dark} ${a} vs ${b}`);
});
// R27：P17 整页重排后，对比度红线落在 .r27-face-card 定色上，两主题同测
const p17 = await pg.evaluate(() => {
  const g = (sel) => { const el = document.querySelector(`section[data-p="17"] ${sel} h3`);
    return el ? getComputedStyle(el).color : null; };
  return { mid: g(".r27-face-card.mid"), right: g(".r27-face-card.deep") };
});
if (p17.mid !== "rgb(13, 13, 13)") fails.push(`R27：P17 中卡文字 ${p17.mid} ≠ rgb(13,13,13)`);
if (p17.right !== "rgb(255, 255, 254)") fails.push(`R27：P17 右卡文字 ${p17.right} ≠ rgb(255,255,254)`);
if (THEME === "light") {
  const vid = await pg.evaluate(() => { const el = document.querySelector('section[data-p="24"] .sh.vid');
    const r = el.style; return { w: r.width, l: r.left, cw: el.getBoundingClientRect ? getComputedStyle(el).width : null }; });
  if (vid.cw !== "1760px") fails.push(`R26：light 下 P24 影院卡宽 ${vid.cw} ≠ 1760px`);
} else {
  const vid = await pg.evaluate(() => getComputedStyle(document.querySelector('section[data-p="24"] .sh.vid')).width);
  if (vid !== "1920px") fails.push(`R26：dark 下 P24 视频宽 ${vid} ≠ 1920px 满幅`);
}

// ── ⑨ R22 模板 token 在位 + R27 连续页码（落款域名退役）──────────────────
const tpl = await pg.evaluate(() => ({
  flow: document.querySelectorAll(".deck-stage > .deck-flow path").length,
  grid: !!document.querySelector(".deck-stage > .deck-grid"),
  rail: document.querySelectorAll(".deck-stage > .deck-rail").length,
  sigs: [...document.querySelectorAll(".slide .sig")].map((el) => [
    +el.closest(".slide").dataset.p, el.textContent.trim()]),
  slideBg: getComputedStyle(document.querySelector(".slide")).backgroundColor,
}));
if (tpl.flow !== 0) fails.push(`R28：流场应已退役，仍见 ${tpl.flow} 条曲线`);   // skill 2026-08-12：CONF 换背景板
if (!tpl.grid) fails.push("栏线网格 .deck-grid 缺失");
if (tpl.rail !== 2) fails.push(`发丝导轨 ${tpl.rail} 条 ≠ 2`);

// ── ⑰ R28 · CONF 背景板（默认组合四板 · 双主题成对 · 每页一张）──────────
const r28 = await pg.evaluate(() => {
  const secs = [...document.querySelectorAll(".slide")];
  const per = secs.map((s) => ({
    p: +s.dataset.p, boarded: s.classList.contains("conf-boarded"),
    bgs: [...s.querySelectorAll(".conf-bg")].map((el) =>
      [...el.classList].find((c) => c.startsWith("conf-bg-")) || "?"),
    img: s.querySelector(".conf-bg") ? getComputedStyle(s.querySelector(".conf-bg")).backgroundImage : "",
  }));
  return { per, distinct: [...new Set(per.flatMap((x) => x.bgs))] };
});
r28.per.forEach(({ p, boarded, bgs }) => {
  if (!boarded || bgs.length !== 1) fails.push(`R28：P${p} 背景板数 ${bgs.length}（应恰好 1 且挂 conf-boarded）`);
});
// R28.1（Colin）：内容板按幕轮换——P2-13 Matrix · P15-25 Side Rail · P28-36 Axis Map
const BOARD_MAP = { 1: "conf-bg-title-02", 37: "conf-bg-title-02", 4: "conf-bg-quote-02",
  26: "conf-bg-quote-02", 27: "conf-bg-quote-02", 14: "conf-bg-chapter-03",
  2: "conf-bg-content-01", 13: "conf-bg-content-01", 15: "conf-bg-content-02",
  25: "conf-bg-content-02", 28: "conf-bg-content-03", 36: "conf-bg-content-03" };
for (const [p, want] of Object.entries(BOARD_MAP)) {
  const got = r28.per.find((x) => x.p === +p)?.bgs[0];
  if (got !== want) fails.push(`R28：P${p} 板 ${got} ≠ ${want}`);
}
if (r28.distinct.length !== 6) fails.push(`R28.1：板种类 ${r28.distinct.length} ≠ 6（${r28.distinct}）`);
r28.per.slice(0, 1).forEach(({ img }) => {
  const wantSuffix = THEME === "dark" ? "-dark.png" : "-light.png";
  if (!img.includes(wantSuffix)) fails.push(`R28：${THEME} 主题下板图源 ${img.slice(0, 90)} 未切 ${wantSuffix}`);
});
const boardLoad = await pg.evaluate(async () => {
  const urls = [...new Set([...document.querySelectorAll(".conf-bg")].map((el) =>
    getComputedStyle(el).backgroundImage.replace(/^url\("|"\)$/g, "")))];
  const out = [];
  for (const u of urls) {
    const ok = await new Promise((res) => { const im = new Image(); im.onload = () => res(im.naturalWidth === 2048 && im.naturalHeight === 1152); im.onerror = () => res(false); im.src = u; });
    out.push([u.split("/").pop(), ok]);
  }
  return out;
});
boardLoad.forEach(([f, ok]) => { if (!ok) fails.push(`R28：背景板加载/尺寸异常 ${f}（应 2048×1152）`); });
if (tpl.sigs.length !== n) fails.push(`R27：页码 ${tpl.sigs.length} 个 ≠ ${n}（37 页每页必挂）`);
tpl.sigs.forEach(([p, t]) => {
  if (t !== `${p}/${n}`) fails.push(`R27：P${p} 页码「${t}」≠ ${p}/${n}`);
  if (/colinyao\.com/i.test(t)) fails.push(`R27：P${p} 页码残留域名落款`);
});
if (!/rgba\(0, 0, 0, 0\)|transparent/.test(tpl.slideBg)) fails.push(`slide 背景 ${tpl.slideBg} 不透明，底流场会被盖住`);

// ── ⑯ R27 · 内容口径 + 动效锚点（交付包清单 · Fable review 修正后的定稿态）──
if (/RETENTION SHAPE OF CONSUMER ROBOTS, 2025/.test(SRC)) fails.push("R27：P2 年份 2025 残留");
if (!/RETENTION SHAPE OF CONSUMER ROBOTS, 2026/.test(SRC)) fails.push("R27：P2 年份 2026 缺失");
for (const tk of ["CLUTCH CONSUMER AI SUPPORT STUDY", "N=422"])
  if (!SRC.includes(tk)) fails.push(`R27：P3 口径缺「${tk}」`);
const r27 = await pg.evaluate(() => {
  const q = (s) => document.querySelector(s), qa = (s) => [...document.querySelectorAll(s)];
  const txt = (el) => (el ? el.textContent.trim() : null);
  return {
    p3nums: qa('section[data-p="3"] .r27-metric .num').map((el) => el.textContent.trim()),
    // P11 · speaker 归属（官方口径：Jensen 追问句，感叹两句是 Ilya）
    p11: qa('section[data-p="11"] .r27-dialogue').map((el) => ({
      who: txt(el.querySelector(".who")), say: txt(el.querySelector(".say")), step: el.dataset.step })),
    p11quote: txt(q('section[data-p="11"] .r27-quote-card .speaker')),
    p5sid28: (q('section[data-p="5"] [data-sid="28"]') || {}).dataset?.step,
    p6sid44: (q('section[data-p="6"] [data-sid="44"]') || {}).dataset?.step,
    p6sid46: (q('section[data-p="6"] [data-sid="46"]') || {}).dataset?.step,
    p14anchor: [q('section[data-p="14"] [data-sid="2"]'), q('section[data-p="14"] [data-sid="3"]')]
      .map((el) => el ? (el.dataset.step || "none") : "missing"),
    p17: { strip: !!q('section[data-p="17"] .r27-face-strip img'),
           stripStep: (q('section[data-p="17"] .r27-face-strip') || {}).dataset?.step,
           cards: qa('section[data-p="17"] .r27-face-card').map((el) => el.dataset.step),
           note: (q('section[data-p="17"] .r27-note') || {}).dataset?.step },
    p28: { ms: qa('section[data-p="28"] .r27-milestone').length,
           pins: qa('section[data-p="28"] .r27-pin').length,
           arrows: qa('section[data-p="28"] svg .arr, section[data-p="28"] [class*="arrow"]').length },
    p37qr: qa('section[data-p="37"] .sh img').map((im) => im.naturalWidth > 0),   // R27.1c：裸图回归，白卡退役
    p37sig: txt(q('section[data-p="37"] .sig')),
  };
});
if (r27.p3nums.join("|") !== "87%|67%") fails.push(`R27：P3 双环读数 ${r27.p3nums} ≠ 87/67`);
if (r27.p11.length !== 2) fails.push(`R27：P11 对话卡 ${r27.p11.length} 张 ≠ 2`);
else {
  const [j, il] = r27.p11;
  if (j.who !== "JENSEN HUANG" || !/Only one billion words\?/.test(j.say) || j.step !== "1")
    fails.push(`R27：P11 第一张对话卡应为 JENSEN「Only one billion words?」@build1，实为 ${JSON.stringify(j)}`);
  if (il.who !== "ILYA SUTSKEVER" || !/amazing/.test(il.say) || !/not a lot/.test(il.say) || il.step !== "2")
    fails.push(`R27：P11 第二张对话卡应为 ILYA「That's amazing. That's not a lot.」@build2，实为 ${JSON.stringify(il)}`);
}
if (!/^ILYA SUTSKEVER/.test(r27.p11quote || "")) fails.push(`R27：P11 引文卡 speaker ${r27.p11quote}`);
if (r27.p5sid28 !== "4") fails.push(`R27：P5 总结底栏 step=${r27.p5sid28} ≠ 4`);
if (r27.p6sid44 !== "5" || r27.p6sid46 !== "5") fails.push(`R27：P6 结论面 step=${r27.p6sid44}/${r27.p6sid46} ≠ 5/5`);
if (r27.p14anchor.join(",") !== "none,none") fails.push(`R27：P14 章节锚点应 build0 常驻，实为 ${r27.p14anchor}`);
// R27.1（Colin 反馈）：先太木@1、太腻@2，恰好与人物 strip 同拍 @3，结论 @4
if (!r27.p17.strip) fails.push("R27：P17 人物 strip 缺失");
if (r27.p17.stripStep !== "3") fails.push(`R27.1：P17 strip step=${r27.p17.stripStep} ≠ 3（应与恰好同拍）`);
if (r27.p17.cards.join(",") !== "1,3,2" || r27.p17.note !== "4")
  fails.push(`R27.1：P17 build 序列 cards=${r27.p17.cards} note=${r27.p17.note} ≠ 太木1/恰好3/太腻2 + 结论4`);
if (r27.p28.ms !== 5 || r27.p28.pins !== 5) fails.push(`R27：P28 节点 ${r27.p28.ms}/pin ${r27.p28.pins} ≠ 5/5`);
if (r27.p28.arrows) fails.push("R27：P28 大箭头残留");
if (r27.p37qr.length !== 2 || !r27.p37qr.every(Boolean)) fails.push(`R27：P37 二维码 ${JSON.stringify(r27.p37qr)}`);
if (r27.p37sig !== `37/${n}`) fails.push(`R27：尾页页码「${r27.p37sig}」≠ 37/${n}`);

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
  if (R27_PAGES.has(i)) {                 // R27：触改页逐 build 截图（交接清单「不只检查最终态」）
    const ms = await pg.evaluate(() => window.deck.maxStep[window.deck.i]);
    for (let s = 0; s <= ms; s++) {
      await pg.evaluate((k) => { const d = window.deck; d.step = k; d.applySteps(); }, s);
      await pg.waitForTimeout(s === 0 ? 1800 : 1050);
      await pg.screenshot({ path: `${SHOT}/builds/p${String(i).padStart(2, "0")}-s${s}-${THEME}.png` });
    }
  }
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
    // R27：手排页不走 .tx/<p> 结构，同一把「出台」尺子直接量 .sh 内容（含 svg 文字）
    sec.querySelectorAll(".sh:not(.tx)").forEach((el) => {
      if (!el.textContent.trim()) return;
      for (const bd of bands(el)) {
        if (bd.bot > stage.bottom + 1 || bd.top < stage.top - 1 ||
            bd.right > stage.right + 1 || bd.left < stage.left - 1)
          out.over.push(["出台", el.dataset.sid || el.className.slice(3, 30),
                         el.textContent.trim().slice(0, 18)]);
      }
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
    sec.querySelectorAll(".tx, [data-sid^='r']").forEach((el) => {   // R27：r 系 sid 元素同尺续保
      const cs = getComputedStyle(el);
      const inner = { l: el.getBoundingClientRect().left + parseFloat(cs.paddingLeft || 0),
                      r: el.getBoundingClientRect().right - parseFloat(cs.paddingRight || 0) };
      const ps = el.querySelectorAll("p").length ? [...el.querySelectorAll("p")] : [el];
      ps.forEach((p) => {
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
if (errs.length) fails.push("pageerror/console.error ×" + errs.length);
if (warn.length) { console.log("console.warn:", warn.slice(0, 5)); fails.push("console.warn ×" + warn.length); }  // R27：零告警红线
console.log("\n" + (fails.length ? "QA FAIL\n" + fails.join("\n") : `QA PASS · 37 页零溢出零 pageerror · 分步对齐 · 主题=${THEME}`));
await b.close();
process.exit(fails.length ? 1 : 0);
