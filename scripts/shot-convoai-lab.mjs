#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════════════════
   /convoai-lab · 终审出图（不跑闸门 —— 闸门在 qa-convoai-lab.mjs 里）
   ---------------------------------------------------------------------------
   出什么：
     ① lab-p1-{light,dark}.png    声场球封面 · 双主题静置帧
     ② lab-p21-{light,dark}.png   地球版 Why Agora · 双主题静置帧
     ③ lab-p1.gif / lab-p21.gif   各 3.5s 实录（960×540 · 12fps）
     ④ lab-contact.png            22 页联览（浅底一版 · 6×4 montage）
   ⚠ 静帧与 GIF 一律走 `?lab=hold`：容器里 SwiftShader 只有个位数 fps，
     不关掉自动降级的话拍到的永远是 poster（那是 lab-fallback.png 的活儿，
     由 qa-convoai-lab.mjs 的 ⑲c 用**真正禁用 WebGL** 的浏览器出）。
   用法： BASE=http://localhost:8777 node scripts/shot-convoai-lab.mjs
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
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ executablePath: CHROME, args: GL });

async function open(theme, w = 1920, h = 1080) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await ctx.addInitScript((t) => { try { localStorage.setItem("colin-theme", t); } catch (e) {} }, theme);
  const pg = await ctx.newPage();
  return { ctx, pg };
}
// 翻页统一走 deck.go：它会把 .active 与入场一起摆正，3D 层的激活闸也挂在它上面
async function goto(pg, n, wait = 5200) {
  await pg.evaluate((k) => window.deck.go(k - 1), n);
  await pg.waitForTimeout(wait);
}

/* ═══ ①② 双主题静置帧 ═══════════════════════════════════════════════════ */
for (const theme of ["light", "dark"]) {
  const { ctx, pg } = await open(theme);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6500);                     // 软渲染起步慢，给足
  for (const [n, name] of [[1, "p1"], [21, "p21"]]) {
    await goto(pg, n);
    const st = await pg.evaluate((k) => {
      const c = document.querySelector(`.slide[data-p="${k}"] [data-lab-canvas]`);
      return { mode: c.dataset.labMode, fps: c.dataset.labFps, dpr: c.dataset.labDpr };
    }, n);
    console.log(`  ${theme} P${n} · mode=${st.mode} fps=${st.fps} dpr=${st.dpr}`);
    await pg.screenshot({ path: `${OUT}/lab-${name}-${theme}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await ctx.close();
}
console.log("✔ 双主题静置帧 → lab-p1-{light,dark}.png / lab-p21-{light,dark}.png");

/* ═══ ③ 两页各一段 3.5s 实录 ════════════════════════════════════════════
   软渲染下真实帧率只有个位数，用「拍一帧 → 等 1/12 秒 → 再拍」凑稳定节奏的实录。
   这不是无缝循环，是一段实录（家族口径，与 shot-lab-globe 同）。 */
for (const [n, name] of [[1, "p1"], [21, "p21"]]) {
  const dir = `${TMP}/${name}`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open(n === 1 ? "light" : "dark", 960, 540);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6000);
  // 从 P1 翻到目标页 ⇒ 入场（0.9s 着色器 t 参数）也被录进 GIF 的头几帧
  if (n !== 1) { await pg.evaluate((k) => window.deck.go(k - 1), n); }
  else { await pg.evaluate(() => { window.deck.go(1); }); await pg.waitForTimeout(400);
         await pg.evaluate(() => window.deck.go(0)); }
  const FPS = 12, N = Math.round(3.5 * FPS);
  for (let i = 0; i < N; i++) {
    await pg.screenshot({ path: `${dir}/f${String(i).padStart(3, "0")}.png` });
    await pg.waitForTimeout(1000 / FPS);
  }
  execFileSync("ffmpeg", ["-y", "-framerate", String(FPS), "-i", `${dir}/f%03d.png`,
    "-vf", "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=bayer:bayer_scale=3",
    "-loop", "0", `${OUT}/lab-${name}.gif`], { stdio: "pipe" });
  console.log(`✔ lab-${name}.gif · ${N} 帧 @ ${FPS}fps（${n === 1 ? "浅底" : "暗底"}）`);
  await ctx.close();
}

/* ═══ ④ 22 页联览（浅底一版）════════════════════════════════════════════ */
{
  const dir = `${TMP}/contact`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open("light");
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6500);
  for (let n = 1; n <= 22; n++) {
    // 分步页拍**终态**（build 走完），联览要看的是这一页最终长什么样
    await pg.evaluate((k) => {
      window.deck.go(k - 1);
      const s = document.querySelectorAll(".slide")[k - 1];
      s.querySelectorAll("[data-step]").forEach((el) => el.classList.add("on"));
    }, n);
    await pg.waitForTimeout(n === 1 || n === 21 ? 4200 : 900);
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
