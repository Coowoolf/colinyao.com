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
   ⚠ 静帧与 GIF 一律走 `?lab=hold`：容器里 SwiftShader 只有个位数 fps，
     不关掉自动降级的话拍到的永远是 poster（那是 wave1-fallback.png 的活儿，
     由 qa-convoai-lab.mjs 的 ⑲c 用**真正禁用 WebGL** 的浏览器出）。
   用法： BASE=http://localhost:8777 node scripts/shot-convoai-lab.mjs
         PAGES=17 GIF=17 node scripts/shot-convoai-lab.mjs   （只出某几页）
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
const CONTACT = process.env.CONTACT !== "0";
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
for (const theme of ["light", "dark"]) {
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
console.log("✔ 双主题整页静帧 → wave1-p{n}-{light,dark}.png");

/* ═══ ⑤ 同页双主题左右拼图：终审一眼比「材质真的换了色」═══════════════ */
for (const n of PAGES) {
  try {
    execFileSync("montage", ["-tile", "1x2", "-geometry", "1400x788+6+6",
      `${OUT}/wave1-p${n}-light.png`, `${OUT}/wave1-p${n}-dark.png`,
      `${OUT}/wave1-duo-p${n}.png`], { stdio: "pipe" });
  } catch (e) { console.log(`  ⚠ montage P${n} 失败（不致命）`); }
}
console.log("✔ 双主题拼图 → wave1-duo-p{n}.png");

/* ═══ ②③ 实录 GIF ══════════════════════════════════════════════════════
   软渲染下真实帧率只有个位数，用「拍一帧 → 等 1/12 秒 → 再拍」凑稳定节奏的实录。
   这不是无缝循环，是一段实录（家族口径，与 shot-lab-globe 同）。
   从别的页翻过去 ⇒ 入场（着色器 t 参数）也被录进 GIF 的头几帧。 */
for (const n of GIFS) {
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

await browser.close();
console.log("\n出图完成 →", OUT);
