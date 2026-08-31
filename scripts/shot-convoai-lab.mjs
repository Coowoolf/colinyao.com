#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════════════════
   /convoai-lab · 终审出图（不跑闸门 —— 闸门在 qa-convoai-lab.mjs 里）
   ---------------------------------------------------------------------------
   出什么（第一波「全量 3D 化」交付物）：
     ① wave1-p{1,4,7,9,17,18,21}-{light,dark}.png   七枚场景 · 双主题整页静帧
     ② wave1-p17.gif                                 五脑区大脑 4s 实录（全轮之冠，单独出）
     ③ wave1-p9.gif                                  SAL 双层防御壳 4s 实录
     ④ wave1-{p4,p7,p18}.png / wave1-p17.png 等      浅底整页（= ① 的 light 一张，软链名）
     ⑤ wave1-duo-{page}.png                          同页双主题左右拼图（终审一眼比）
     ⑥ lab-contact.png                               22 页联览（浅底一版 · 4×6 montage）
   ── 第二波（2026-08-31 终波 · 九页套件化）的交付物（DO 段开关控制）──────────
     wave2-p{2,3,6,8,10,11,12,13,14}-{light,dark}.png   九枚新场景 · 双主题整页静帧
     wave2-9pages.png                九页 3D 静帧九宫格（暗主题 · 3×3）
     wave2-p10.png / wave2-p3.png    大图分层与三通道两处单独出（暗底整页）
     wave2-p10-light.png             大图的**浅底**同帧（分层度 vs 可读性的终审对照）
     wave2-p11.gif                   弱网「囤着播」4s 实录（本波之冠，单独出）
     lab-final-contact-{light,dark}.png   22 页终版联览（双主题各一版 · 4×6）
     wave2-fallback.png              禁 WebGL 下九页抽三格（P10 / P11 / P13）
   ⚠ 静帧与 GIF 一律走 `?lab=hold`：容器里 SwiftShader 只有个位数 fps，
     不关掉自动降级的话拍到的永远是 poster（那是 fallback 图的活儿，
     用**真正禁用 WebGL** 的浏览器出，见本文件末尾的 w2fallback 段）。
   用法： BASE=http://localhost:8777 node scripts/shot-convoai-lab.mjs
         PAGES=17 GIF=17 node scripts/shot-convoai-lab.mjs   （只出某几页）
         DO=w2,w2grid,w2gif,contact2,w2fallback node scripts/shot-convoai-lab.mjs
   DO 段开关（逗号分隔，默认第一波那四段）：
     w1 双主题静帧 / duo 双主题拼图 / gif 实录 / contact 22 页联览（浅底）
     w2 第二波九页静帧 / w2grid 九宫格 / w2gif 弱网实录 /
     contact2 双主题终版联览 / w2fallback 禁 WebGL 抽三格
   ═══════════════════════════════════════════════════════════════════════════ */
import { chromium } from "playwright-core";
import { mkdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";

const BASE = process.env.BASE || "http://localhost:8777";
const URL_ = BASE + "/decks/convoai-lab.html?lab=hold";
const OUT = process.env.OUT || "/home/claude/eco-review";
const TMP = "/tmp/convoai-lab-frames";
const CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const GL = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"];
// 场景页码表（与 builder 的 LAB_RECTS、qa 的 LAB_SCENES 三处对表）
const PAGES = (process.env.PAGES || "1,4,7,9,17,18,21").split(",").map(Number);
const GIFS = (process.env.GIF || "17,9").split(",").filter(Boolean).map(Number);
// 第二波九页（与 builder 的 LAB_RECTS、qa 的 LAB_SCENES 三处对表）
const W2 = (process.env.W2 || "2,3,6,8,10,11,12,13,14").split(",").filter(Boolean).map(Number);
const DO = new Set((process.env.DO || "w1,duo,gif,contact").split(",").map(s => s.trim()));
const CONTACT = process.env.CONTACT !== "0" && DO.has("contact");
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: CHROME, args: GL });

async function open(theme, w = 1920, h = 1080) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await ctx.addInitScript((t) => { try { localStorage.setItem("colin-theme", t); } catch (e) {} }, theme);
  const pg = await ctx.newPage();
  return { ctx, pg };
}
// 翻页统一走 deck.go：它会把 .active 与入场一起摆正，3D 层的巡游闸也挂在它上面
async function goto(pg, n, wait = 4200) {
  await pg.evaluate((k) => window.deck.go(k - 1), n);
  await pg.waitForTimeout(wait);
}

/* ═══ ① 七枚场景 · 双主题整页静帧 ═══════════════════════════════════════ */
if (DO.has("w1")) for (const theme of ["light", "dark"]) {
  const { ctx, pg } = await open(theme);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6800);                     // 软渲染起步慢，给足
  for (const n of PAGES) {
    await goto(pg, n);
    const st = await pg.evaluate(() => {
      const c = document.getElementById("labGl");
      return { mode: c.dataset.labMode, scene: c.dataset.labScene,
               fps: c.dataset.labFps, dpr: c.dataset.labDpr, page: c.dataset.labPage };
    });
    console.log(`  ${theme} P${n} · ${st.scene} mode=${st.mode} fps=${st.fps} dpr=${st.dpr}`);
    if (st.mode !== "LIVE" || +st.page !== n)
      console.log(`  ⚠ P${n} 拍到的不是 WebGL 态（mode=${st.mode} page=${st.page}）`);
    await pg.screenshot({ path: `${OUT}/wave1-p${n}-${theme}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await ctx.close();
}
if (DO.has("w1")) console.log("✔ 双主题整页静帧 → wave1-p{n}-{light,dark}.png");

/* ═══ ⑤ 同页双主题左右拼图：终审一眼比「材质真的换了色」═══════════════ */
if (DO.has("duo")) for (const n of PAGES) {
  try {
    execFileSync("montage", ["-tile", "1x2", "-geometry", "1400x788+6+6",
      `${OUT}/wave1-p${n}-light.png`, `${OUT}/wave1-p${n}-dark.png`,
      `${OUT}/wave1-duo-p${n}.png`], { stdio: "pipe" });
  } catch (e) { console.log(`  ⚠ montage P${n} 失败（不致命）`); }
}
if (DO.has("duo")) console.log("✔ 双主题拼图 → wave1-duo-p{n}.png");

/* ═══ ②③ 实录 GIF ══════════════════════════════════════════════════════
   软渲染下真实帧率只有个位数，用「拍一帧 → 等 1/12 秒 → 再拍」凑稳定节奏的实录。
   这不是无缝循环，是一段实录（家族口径，与 shot-lab-globe 同）。
   从别的页翻过去 ⇒ 入场（着色器 t 参数）也被录进 GIF 的头几帧。 */
if (DO.has("gif")) for (const n of GIFS) {
  const dir = `${TMP}/p${n}`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const theme = n === 17 ? "light" : "light";
  const { ctx, pg } = await open(theme, 960, 540);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6500);
  await pg.evaluate((k) => window.deck.go(k - 2 < 0 ? 1 : k - 2), n);   // 先站到邻页
  await pg.waitForTimeout(900);
  await pg.evaluate((k) => window.deck.go(k - 1), n);                   // 再翻进来（录入场）
  const FPS = 12, N = Math.round(4.0 * FPS);
  for (let i = 0; i < N; i++) {
    await pg.screenshot({ path: `${dir}/f${String(i).padStart(3, "0")}.png` });
    await pg.waitForTimeout(1000 / FPS);
  }
  execFileSync("ffmpeg", ["-y", "-framerate", String(FPS), "-i", `${dir}/f%03d.png`,
    "-vf", "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=bayer:bayer_scale=3",
    "-loop", "0", `${OUT}/wave1-p${n}.gif`], { stdio: "pipe" });
  console.log(`✔ wave1-p${n}.gif · ${N} 帧 @ ${FPS}fps · 4.0s（${theme}）`);
  await ctx.close();
}

/* ═══ ⑥ 22 页联览（浅底一版）════════════════════════════════════════════ */
if (CONTACT) {
  const dir = `${TMP}/contact`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open("light");
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6800);
  for (let n = 1; n <= 22; n++) {
    // 分步页拍**终态**（build 走完），联览要看的是这一页最终长什么样
    await pg.evaluate((k) => {
      window.deck.go(k - 1);
      const s = document.querySelectorAll(".slide")[k - 1];
      s.querySelectorAll("[data-step]").forEach((el) => el.classList.add("on"));
    }, n);
    await pg.waitForTimeout(PAGES.includes(n) ? 3800 : 900);
    await pg.screenshot({ path: `${dir}/p${String(n).padStart(2, "0")}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await ctx.close();
  // ⚠ 别把通配符交给 execFileSync（不经 shell，montage 拿到的是字面量 `p*.png`，
  //   它会当没有输入而静默退出）—— 显式把 22 个文件名排好递进去。
  const files = Array.from({ length: 22 },
    (_, i) => `${dir}/p${String(i + 1).padStart(2, "0")}.png`);
  // ⚠ 这台机器上的 montage(IM6) 不吃 -background（无论排在输入前还是后，都会把色号
  //   当成一个文件名去开，报 unable to open image）—— 直接用默认底色，联览图不挑这个。
  execFileSync("montage", ["-tile", "4x6", "-geometry", "480x270+6+6",
    ...files, `${OUT}/lab-contact.png`], { stdio: "pipe" });
  console.log("✔ lab-contact.png · 22 页联览（4×6 · 浅底）");
}

/* ═══════════════════════════════════════════════════════════════════════════
   第二波（终波 · 九页套件化）交付物
   ═══════════════════════════════════════════════════════════════════════════ */
/* ═══ w2 · 九枚新场景 · 双主题整页静帧 ═══════════════════════════════════ */
if (DO.has("w2")) for (const theme of ["light", "dark"]) {
  const { ctx, pg } = await open(theme);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6800);
  for (const n of W2) {
    await goto(pg, n);
    const st = await pg.evaluate(() => {
      const c = document.getElementById("labGl");
      return { mode: c.dataset.labMode, scene: c.dataset.labScene,
               fps: c.dataset.labFps, page: c.dataset.labPage };
    });
    console.log(`  ${theme} P${n} · ${st.scene} mode=${st.mode} fps=${st.fps}`);
    if (st.mode !== "LIVE" || +st.page !== n)
      console.log(`  ⚠ P${n} 拍到的不是 WebGL 态（mode=${st.mode} page=${st.page}）`);
    await pg.screenshot({ path: `${OUT}/wave2-p${n}-${theme}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await ctx.close();
}
if (DO.has("w2")) console.log("✔ 第二波九页双主题静帧 → wave2-p{n}-{light,dark}.png");

/* ═══ w2grid · 九宫格（暗主题）+ 两处单独出 ═════════════════════════════ */
if (DO.has("w2grid")) {
  const files = W2.map((n) => `${OUT}/wave2-p${n}-dark.png`);
  execFileSync("montage", ["-tile", "3x3", "-geometry", "620x349+8+8",
    ...files, `${OUT}/wave2-9pages.png`], { stdio: "pipe" });
  // 大图（P10）与三通道（P3）各单独出一张整页；大图另出浅底同帧，
  // 供终审对照「分层度 vs 可读性」这一处取舍。
  for (const [n, name] of [[10, "wave2-p10"], [3, "wave2-p3"]])
    execFileSync("cp", [`${OUT}/wave2-p${n}-dark.png`, `${OUT}/${name}.png`], { stdio: "pipe" });
  console.log("✔ wave2-9pages.png（3×3 · 暗底）+ wave2-p10.png / wave2-p3.png");
}

/* ═══ w2gif · 弱网「囤着播」实录（本波之冠）═════════════════════════════ */
if (DO.has("w2gif")) for (const n of [11]) {
  const dir = `${TMP}/w2p${n}`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open("dark", 960, 540);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6500);
  await pg.evaluate((k) => window.deck.go(k - 3), n);      // 先站到邻页
  await pg.waitForTimeout(900);
  await pg.evaluate((k) => window.deck.go(k - 1), n);      // 再翻进来（录入场）
  const FPS = 12, N = Math.round(4.5 * FPS);
  for (let i = 0; i < N; i++) {
    await pg.screenshot({ path: `${dir}/f${String(i).padStart(3, "0")}.png` });
    await pg.waitForTimeout(1000 / FPS);
  }
  execFileSync("ffmpeg", ["-y", "-framerate", String(FPS), "-i", `${dir}/f%03d.png`,
    "-vf", "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=bayer:bayer_scale=3",
    "-loop", "0", `${OUT}/wave2-p${n}.gif`], { stdio: "pipe" });
  console.log(`✔ wave2-p${n}.gif · ${N} 帧 @ ${FPS}fps · 4.5s（暗底）`);
  await ctx.close();
}

/* ═══ contact2 · 22 页终版联览（双主题各一版）═══════════════════════════ */
if (DO.has("contact2")) for (const theme of ["light", "dark"]) {
  const dir = `${TMP}/contact-${theme}`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open(theme);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6800);
  const SCENES = new Set([...PAGES, ...W2]);
  for (let n = 1; n <= 22; n++) {
    await pg.evaluate((k) => {
      window.deck.go(k - 1);
      const s = document.querySelectorAll(".slide")[k - 1];
      s.querySelectorAll("[data-step]").forEach((el) => el.classList.add("on"));
    }, n);
    await pg.waitForTimeout(SCENES.has(n) ? 3800 : 900);
    await pg.screenshot({ path: `${dir}/p${String(n).padStart(2, "0")}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await ctx.close();
  const files = Array.from({ length: 22 },
    (_, i) => `${dir}/p${String(i + 1).padStart(2, "0")}.png`);
  execFileSync("montage", ["-tile", "4x6", "-geometry", "480x270+6+6",
    ...files, `${OUT}/lab-final-contact-${theme}.png`], { stdio: "pipe" });
  console.log(`✔ lab-final-contact-${theme}.png · 22 页终版联览（4×6）`);
}

/* ═══ w2fallback · 禁 WebGL 下九页抽三格 ════════════════════════════════
   这一段**必须**另开一个真正禁用 WebGL 的浏览器（不是 ?lab=hold，也不是把 canvas 藏了）——
   它要证的是「3D 起不来 = 页上原来那张 SVG 完整呈现」，抽 P10 大图 / P11 弱网 / P13 插槽
   三格：一张标注最密、一张几何最重、一张换装语义最强。 */
if (DO.has("w2fallback")) {
  const dir = `${TMP}/w2fb`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const b2 = await chromium.launch({ executablePath: CHROME,
    args: ["--disable-webgl", "--disable-webgl2", "--disable-gpu"] });
  const ctx = await b2.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { try { localStorage.setItem("colin-theme", "dark"); } catch (e) {} });
  const pg = await ctx.newPage();
  await pg.goto(BASE + "/decks/convoai-lab.html#1", { waitUntil: "load" });
  await pg.waitForTimeout(7600);                        // 看门狗 6s
  const picks = [10, 11, 13];
  for (const n of picks) {
    await pg.evaluate((k) => {
      window.deck.go(k - 1);
      const s = document.querySelectorAll(".slide")[k - 1];
      s.querySelectorAll("[data-step]").forEach((el) => el.classList.add("on"));
    }, n);
    await pg.waitForTimeout(2600);
    await pg.screenshot({ path: `${dir}/p${n}.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  const st = await pg.evaluate(() => {
    const c = document.getElementById("labGl");
    return { mode: c.dataset.labMode, glup: document.querySelectorAll(".lab-stage.gl-up").length };
  });
  console.log(`  禁 WebGL 态：mode=${st.mode} gl-up=${st.glup}（应为 POSTER / 0）`);
  await b2.close();
  execFileSync("montage", ["-tile", "1x3", "-geometry", "900x506+8+8",
    ...picks.map((n) => `${dir}/p${n}.png`), `${OUT}/wave2-fallback.png`], { stdio: "pipe" });
  console.log("✔ wave2-fallback.png · 禁 WebGL · P10 / P11 / P13 三格");
}

await browser.close();
console.log("\n出图完成 →", OUT);
