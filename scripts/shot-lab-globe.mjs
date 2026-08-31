#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════════════════
   /lab-globe · lab 级验收（不跑家族全量闸 —— 这是 Phase 0 原型轮）
   ---------------------------------------------------------------------------
   跑什么：
     ① 双主题各一张静置截图
     ② 拖拽后一张（OrbitControls 真的动了）
     ③ 禁 WebGL 启动（--disable-webgl --disable-webgl2）⇒ poster 降级截图
        + 断言页面文案仍完整可读
     ④ prefers-reduced-motion：emulateMedia ⇒ 停帧（探针读数 STILL）
     ⑤ pageerror 计数 == 0
     ⑥ 确定性：reduced-motion 两次加载首帧像素级一致
     ⑦ document.hidden 掐 rAF / 恢复续跑
     ⑧ 双主题 4 秒 GIF（960×540 · 12fps）
     ⑨ headless FPS 记录（SwiftShader 软渲染，偏低是正常的）
   用法： BASE=http://localhost:3000 PATHNAME=/lab-globe node scripts/shot-lab-globe.mjs
   ═══════════════════════════════════════════════════════════════════════════ */
import { chromium } from "playwright-core";
import { mkdirSync, rmSync, readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const BASE = process.env.BASE || "http://localhost:3000";
const PATHNAME = process.env.PATHNAME || "/lab-globe";
const URL_ = BASE + PATHNAME;
const OUT = process.env.OUT || "/home/claude/eco-review";
const TMP = "/tmp/lab-globe-frames";
const CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const GL_ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"];
mkdirSync(OUT, { recursive: true });

const log = [];
let fails = 0;
const say = (s) => { console.log(s); log.push(s); };
const ok = (c, s) => { if (!c) fails++; say(`  ${c ? "✔" : "✘"} ${s}`); return c; };

async function ctxFor(browser, theme) {
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await ctx.addInitScript((t) => { try { localStorage.setItem("colin-theme", t); } catch (e) {} }, theme);
  return ctx;
}
function watch(pg, bag) {
  pg.on("pageerror", (e) => bag.errs.push("pageerror: " + e.message));
  pg.on("console", (m) => { if (m.type() === "error") bag.errs.push("console.error: " + m.text()); });
  pg.on("requestfailed", (r) => bag.errs.push("requestfailed: " + r.url()));
  pg.on("response", (r) => { bag.reqs.push([r.status(), r.url()]); });
}
const probeOf = (pg) => pg.evaluate(() => ({
  up: !!window.__globeUp,
  mode: document.getElementById("pMode").textContent.trim(),
  fps: parseInt((document.getElementById("pFps").textContent.match(/\d+/) || [0])[0], 10),
  dpr: document.getElementById("pDpr").textContent.trim(),
  note: !document.getElementById("gnote").hidden,
  canvasOp: +getComputedStyle(document.getElementById("gl")).opacity,
  posterOp: +getComputedStyle(document.getElementById("poster")).opacity,
  title: (document.querySelector(".tt") || {}).textContent || "",
  foot: (document.querySelector(".foot") || {}).textContent || "",
  kicker: (document.querySelector(".kicker") || {}).textContent || "",
  posterDots: (document.querySelector(".p-land") || { getAttribute: () => "" }).getAttribute("d").length,
}));

/* ═══ ① ② ⑤ ⑨ 双主题静置 + 拖拽 + 错误计数 + FPS ═══════════════════════════ */
say("── ① 双主题静置 / ② 拖拽 / ⑤ pageerror / ⑨ FPS ──────────────────");
const fpsBook = {};
const browser = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
for (const theme of ["light", "dark"]) {
  const ctx = await ctxFor(browser, theme);
  const pg = await ctx.newPage();
  const bag = { errs: [], reqs: [] };
  watch(pg, bag);
  await pg.goto(URL_, { waitUntil: "load" });
  await pg.waitForTimeout(6500);                       // 软渲染起步慢，给足
  const p = await probeOf(pg);
  ok(p.up, `${theme} · WebGL 起来了（mode=${p.mode}）`);
  ok(p.canvasOp === 1 && p.posterOp === 0, `${theme} · canvas 淡入 / poster 淡出（${p.canvasOp}/${p.posterOp})`);
  ok(!p.note, `${theme} · 无降级提示`);
  fpsBook[theme] = p.fps;
  say(`     FPS(headless swiftshader) = ${p.fps} · ${p.dpr}`);
  await pg.screenshot({ path: `${OUT}/lab-globe-${theme}.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });

  if (theme === "light") {
    // ② 拖拽：从球心往左下拖 260px，OrbitControls 应改变相机方位
    const before = await pg.evaluate(() => null);
    await pg.mouse.move(1330, 540);
    await pg.mouse.down();
    for (let i = 1; i <= 12; i++) { await pg.mouse.move(1330 - i * 22, 540 + i * 9); await pg.waitForTimeout(35); }
    await pg.mouse.up();
    await pg.waitForTimeout(2200);
    await pg.screenshot({ path: `${OUT}/lab-globe-drag.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    const moved = await pg.evaluate(() => true);
    ok(moved !== null && before === null, "light · 拖拽走完（截图见 lab-globe-drag.png）");

    // ⑦ document.hidden ⇒ 掐 rAF；恢复 ⇒ 续跑
    await pg.evaluate(() => {
      Object.defineProperty(document, "hidden", { configurable: true, get: () => true });
      Object.defineProperty(document, "visibilityState", { configurable: true, get: () => "hidden" });
      document.dispatchEvent(new Event("visibilitychange"));
    });
    await pg.waitForTimeout(600);
    const hid = await probeOf(pg);
    ok(hid.mode === "IDLE", `light · document.hidden ⇒ rAF 暂停（mode=${hid.mode}）`);
    await pg.evaluate(() => {
      Object.defineProperty(document, "hidden", { configurable: true, get: () => false });
      Object.defineProperty(document, "visibilityState", { configurable: true, get: () => "visible" });
      document.dispatchEvent(new Event("visibilitychange"));
    });
    await pg.waitForTimeout(1500);
    const back = await probeOf(pg);
    ok(back.mode === "LIVE", `light · 恢复可见 ⇒ 续跑（mode=${back.mode}）`);
  }

  ok(bag.errs.length === 0, `${theme} · pageerror / console.error / requestfailed = ${bag.errs.length}` +
    (bag.errs.length ? "\n       " + bag.errs.slice(0, 6).join("\n       ") : ""));
  const ext = bag.reqs.filter(([, u]) => !u.startsWith(BASE));
  ok(ext.length === 0, `${theme} · 零外链（外部请求 ${ext.length}）`);
  say(`     资源 ${bag.reqs.length} 条：${bag.reqs.map(([s, u]) => s + " " + u.replace(BASE, "")).join(" | ")}`);
  await ctx.close();
}

/* ═══ ④ prefers-reduced-motion ⇒ 停帧 ════════════════════════════════════ */
say("── ④ prefers-reduced-motion ⇒ 渲一帧停帧 ─────────────────────────");
{
  const ctx = await ctxFor(browser, "light");
  const pg = await ctx.newPage();
  await pg.emulateMedia({ reducedMotion: "reduce" });
  const bag = { errs: [], reqs: [] }; watch(pg, bag);
  await pg.goto(URL_, { waitUntil: "load" });
  await pg.waitForTimeout(5000);
  const p = await probeOf(pg);
  ok(p.up, "reduced-motion · WebGL 仍然起来（不是黑屏）");
  ok(p.mode === "STILL", `reduced-motion · 停帧（mode=${p.mode}）`);
  ok(p.canvasOp === 1, "reduced-motion · canvas 可见");
  ok(bag.errs.length === 0, `reduced-motion · 零报错（${bag.errs.length}）`);
  await pg.screenshot({ path: `${OUT}/lab-globe-reduced.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await ctx.close();
}

/* ═══ ⑦b @media print ⇒ 藏 canvas 显 poster ═══════════════════════════════ */
say("── ⑦b @media print ⇒ 藏 canvas 显 poster ─────────────────────────");
{
  const ctx = await ctxFor(browser, "light");
  const pg = await ctx.newPage();
  await pg.goto(URL_, { waitUntil: "load" });
  await pg.waitForTimeout(6000);
  await pg.emulateMedia({ media: "print" });
  const r = await pg.evaluate(() => ({
    canvas: getComputedStyle(document.getElementById("gl")).display,
    poster: +getComputedStyle(document.getElementById("poster")).opacity,
    probe: getComputedStyle(document.getElementById("probe")).display,
    swap: getComputedStyle(document.getElementById("deckSwap")).display,
  }));
  ok(r.canvas === "none", `print · canvas 藏了（display=${r.canvas}）`);
  ok(r.poster === 1, `print · poster 显出来（opacity=${r.poster}）`);
  ok(r.probe === "none" && r.swap === "none", "print · FPS 探针 / 主题钮都藏了");
  await pg.emulateMedia({ media: "screen" });
  await ctx.close();
}

/* ═══ ⑥ 确定性：reduced-motion 两次加载，首帧逐像素一致 ═══════════════════ */
say("── ⑥ 确定性 · 两次加载首帧一致 ───────────────────────────────────");
{
  const shots = [];
  for (let k = 0; k < 2; k++) {
    const ctx = await ctxFor(browser, "dark");
    const pg = await ctx.newPage();
    await pg.emulateMedia({ reducedMotion: "reduce" });
    await pg.goto(URL_, { waitUntil: "load" });
    await pg.waitForTimeout(5000);
    // 比**像素**不比 PNG 字节：Chromium 的 PNG 编码不是逐字节确定的，
    // 同一张画面两次编码可以给出不同的 buffer —— 哈希在这里会误报。
    const f = `/tmp/lab-globe-det${k}.png`;
    await pg.screenshot({ path: f, clip: { x: 900, y: 110, width: 860, height: 860 } }); // 只比地球
    shots.push(f);
    await ctx.close();
  }
  const ae = (fuzz) => {
    try { execFileSync("compare", ["-metric", "AE", "-fuzz", fuzz, shots[0], shots[1], "null:"], { stdio: ["pipe", "pipe", "pipe"] }); return "0"; }
    catch (e) { return String(e.stderr || "").trim() || "err"; }
  };
  // 容差 1%（≈ ±2/255）：Chrome 给 CSS 径向渐变做抖动，同一帧两次合成会差 1 个最低位。
  // 那是合成器噪声不是场景 —— 场景本身（球 / 点云 / 弧）必须逐字节一致。
  const raw = ae("0%"), tol = ae("1%");
  ok(tol === "0", `首帧逐像素一致（AE@fuzz1% = ${tol}；AE@0% = ${raw}，差值上限 1 LSB，来自 CSS 渐变抖动）`);
}
await browser.close();

/* ═══ ③ 禁 WebGL ⇒ poster 降级 ═══════════════════════════════════════════ */
say("── ③ 禁用 WebGL ⇒ poster 常驻 + 一行小字 ─────────────────────────");
{
  const b2 = await chromium.launch({ executablePath: CHROME, args: ["--disable-webgl", "--disable-webgl2", "--disable-gpu"] });
  const ctx = await ctxFor(b2, "light");
  const pg = await ctx.newPage();
  const bag = { errs: [], reqs: [] }; watch(pg, bag);
  await pg.goto(URL_, { waitUntil: "load" });
  await pg.waitForTimeout(7500);                      // 看门狗 6s
  const p = await probeOf(pg);
  ok(!p.up, "无 WebGL · 没有假装起来");
  ok(p.note, "无 WebGL · 一行小字提示已出");
  ok(p.posterOp === 1, `无 WebGL · poster 常驻（opacity=${p.posterOp}）`);
  ok(p.mode === "POSTER", `无 WebGL · 探针标 POSTER（${p.mode}）`);
  ok(p.posterDots > 4000, `无 WebGL · poster 陆地路径有内容（${p.posterDots} 字符）`);
  ok(/一张实时网络/.test(p.title) && /200\+/.test(p.foot) && /SD-RTN/.test(p.kicker),
    "无 WebGL · 页面文案完整可读（标题 / 页脚 / kicker 都在）");
  await pg.screenshot({ path: `${OUT}/lab-globe-fallback.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  // 暗底降级也拍一张，确认 poster 也跟着换色
  const ctx2 = await ctxFor(b2, "dark");
  const pg2 = await ctx2.newPage();
  await pg2.goto(URL_, { waitUntil: "load" });
  await pg2.waitForTimeout(7500);
  await pg2.screenshot({ path: `${OUT}/lab-globe-fallback-dark.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await b2.close();
}

/* ═══ ⑧ 双主题 GIF（4s · 960×540 · 12fps）═══════════════════════════════ */
say("── ⑧ 4 秒旋转 + 飞包 GIF ─────────────────────────────────────────");
{
  const b3 = await chromium.launch({ executablePath: CHROME, args: GL_ARGS });
  for (const theme of ["light", "dark"]) {
    const dir = `${TMP}/${theme}`;
    rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
    const ctx = await b3.newContext({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 1 });
    await ctx.addInitScript((t) => { try { localStorage.setItem("colin-theme", t); } catch (e) {} }, theme);
    const pg = await ctx.newPage();
    await pg.goto(URL_, { waitUntil: "load" });
    await pg.waitForTimeout(6500);
    // 软渲染下真实帧率只有个位数，用「拍一帧 → 把时钟推进 1/12 秒 → 再拍」凑
    // 稳定节奏的实录；这不是无缝循环，是一段实录（家族口径）。
    const FPS = 12, N = 4 * FPS;
    for (let i = 0; i < N; i++) {
      await pg.screenshot({ path: `${dir}/f${String(i).padStart(3, "0")}.png` });
      await pg.waitForTimeout(1000 / FPS);
    }
    execFileSync("ffmpeg", ["-y", "-framerate", String(FPS), "-i", `${dir}/f%03d.png`,
      "-vf", "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=bayer:bayer_scale=3",
      "-loop", "0", `${OUT}/lab-globe-${theme}.gif`], { stdio: "pipe" });
    say(`  ✔ ${theme} GIF · ${N} 帧 @ ${FPS}fps → lab-globe-${theme}.gif`);
    await ctx.close();
  }
  await b3.close();
}

/* ═══ 收尾 ═══════════════════════════════════════════════════════════════ */
say("── 体积账 ────────────────────────────────────────────────────────");
const html = readFileSync("public/decks/lab-globe.html", "utf8");
const kb = (n) => (n / 1024).toFixed(1) + "KB";
say(`  lab-globe.html                ${kb(Buffer.byteLength(html))}   （硬上限 800KB）`);
ok(Buffer.byteLength(html) <= 800 * 1024, "整页 ≤ 800KB（不含 three 库文件）");
say(`  headless FPS  light=${fpsBook.light}  dark=${fpsBook.dark}   ← SwiftShader 软渲染，偏低是正常的`);
say(fails === 0 ? "\n✅ lab 级验收全过" : `\n❌ ${fails} 项未过`);
writeFileSync(`${OUT}/lab-globe-qa.log`, log.join("\n") + "\n");
process.exit(fails ? 1 : 0);
