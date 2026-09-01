#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════════════════
   二轮精修 · 波A · 终审出图（闸门在 qa-convoai-lab.mjs 里，这里只出片）
   ---------------------------------------------------------------------------
   出什么：
     waveA-p{6,8,14,18}-{light,dark}.png   四页换血 · 双主题整页静帧
     waveA-p8.gif    4.0s   ← 「Audition 感」验收主件
     waveA-p6.gif    4.0s   横贯全链一条流 + token 脉冲串
     waveA-p14.gif   9.3s   一整轮握手（生长 6.24 → 全亮停驻 2.00 → 收 1.00）
     waveA-p18.png          loop 空间环带 + 左移 80px 的整页
     waveA-p18-layout-ab.png  版式 A/B（改前 = HEAD 的产物，改后 = 现在）
   ⚠ GIF **一律用 TOUR.pace 录**：容器里 SwiftShader 只有 3–4fps，
     老办法（截一帧 → 等 1/12 秒 → 再截）录出来名义 12fps、实际 3.4fps
     ⇒ 放出来快 3.5×。本波终审第一位的判据是「速度是否从容」，录快了没法看。
     定拍之后钟只在 step() 里按 1/fps 前进 ⇒ 录多久就是多久（脚本会打印实测流速）。
   用法：BASE=http://localhost:8899 node scripts/shot-wavea.mjs
        DO=still,gif,p18,ab node scripts/shot-wavea.mjs
   ═══════════════════════════════════════════════════════════════════════════ */
import { chromium } from "playwright-core";
import { mkdirSync, rmSync, writeFileSync, existsSync, unlinkSync } from "node:fs";
import { execFileSync } from "node:child_process";

const BASE = process.env.BASE || "http://localhost:8899";
const URL_ = BASE + "/decks/convoai-lab.html?lab=hold";
const OUT = process.env.OUT || "/home/claude/eco-review";
const TMP = "/tmp/wavea-frames";
const CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const GL = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"];
const DO = new Set((process.env.DO || "still,gif,p18,ab").split(",").map(s => s.trim()));
const PAGES = [6, 8, 14, 18];
const GIFS = [[8, 4.0], [6, 4.0], [14, 9.3]];
mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROME, args: GL });

async function open(theme, w = 1920, h = 1080) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await ctx.addInitScript((t) => { try { localStorage.setItem("colin-theme", t); } catch (e) {} }, theme);
  return { ctx, pg: await ctx.newPage() };
}
async function goto(pg, n, wait = 4200) {
  await pg.evaluate((k) => window.deck.go(k - 1), n);
  await pg.waitForTimeout(wait);
}
const st = (pg) => pg.evaluate(() => {
  const c = document.getElementById("labGl");
  return { mode: c.dataset.labMode, scene: c.dataset.labScene, page: +c.dataset.labPage,
           fps: c.dataset.labFps, dpr: c.dataset.labDpr };
});

/* ═══ ① 四页 · 双主题整页静帧 ══════════════════════════════════════════ */
if (DO.has("still")) for (const theme of ["light", "dark"]) {
  const { ctx, pg } = await open(theme);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6800);
  for (const n of PAGES) {
    await goto(pg, n);
    if (n === 14 || n === 6)                       // 分步页拍**终态**（build 走完）
      await pg.evaluate(() => { const s = document.querySelector(".slide.active");
        s.querySelectorAll("[data-step]").forEach(e => e.classList.add("on"));
        window.__labTour && window.__labTour.unit && null; });
    if (n === 14) { await pg.evaluate(() => window.__labTour.pace(12));
                    await pg.evaluate(() => window.__labTour.seek(7.0)); }  // 全亮停驻那一帧
    await pg.waitForTimeout(1400);
    const s = await st(pg);
    console.log(`  ${theme} P${n} · ${s.scene} mode=${s.mode} page=${s.page} dpr=${s.dpr}`);
    await pg.screenshot({ path: `${OUT}/waveA-p${n}-${theme}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    if (n === 14) await pg.evaluate(() => window.__labTour.pace(0));   // 退定拍再翻下一页
  }
  await ctx.close();
}
if (DO.has("still")) console.log("✔ 四页双主题静帧 → waveA-p{6,8,14,18}-{light,dark}.png");

/* ═══ ② 实录 GIF（TOUR.pace 定拍）═════════════════════════════════════ */
if (DO.has("gif")) for (const [n, secs] of GIFS) {
  const dir = `${TMP}/p${n}`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open("light", 1920, 1080);
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6500);
  await goto(pg, n, 3600);
  if (n === 14 || n === 6)
    await pg.evaluate(() => document.querySelector(".slide.active")
      .querySelectorAll("[data-step]").forEach(e => e.classList.add("on")));
  await pg.waitForTimeout(1600);
  // 入场走完之后再冻 CSS：本波三页的可见动效全在 canvas 上（页上的形都已入 poster 层）
  await pg.addStyleTag({ content: "*,*::before,*::after{animation-play-state:paused!important}" });
  const FPS = 12, N = Math.round(secs * FPS);
  const t0 = await pg.evaluate((f) => { window.__labTour.pace(f);
                                        return window.__labTour.seek(0); }, FPS);
  for (let i = 0; i < N; i++) {
    await pg.screenshot({ path: `${dir}/f${String(i).padStart(3, "0")}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    await pg.evaluate(() => window.__labTour.step(1));
    await pg.waitForTimeout(40);                   // 让 rAF 至少重画一次
  }
  const t1 = await pg.evaluate(() => window.__labTour.clock());
  const probe = await pg.evaluate(() => { const u = window.__labTour.unit();
                                          return u && u.state ? u.state() : null; });
  execFileSync("ffmpeg", ["-y", "-framerate", String(FPS), "-i", `${dir}/f%03d.png`,
    "-vf", "scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=200[p];[b][p]paletteuse=dither=bayer:bayer_scale=3",
    "-loop", "0", `${OUT}/waveA-p${n}.gif`], { stdio: "pipe" });
  const walk = probe && probe.run !== undefined ? probe.run : null;
  console.log(`✔ waveA-p${n}.gif · ${N} 帧 @ ${FPS}fps · 场上钟走了 ${(t1 - t0).toFixed(2)}s`
    + (walk !== null ? ` · 波峰实走 ${(walk / (t1 - t0)).toFixed(1)}px/s` : "")
    + (probe && probe.head ? ` · 注光头 ${probe.head.map(x => x.toFixed(0)).join("/")}` : ""));
  await ctx.close();
}

/* ═══ ③ P18 整页（浅底 · loop 空间环带 + 左移 80px）═══════════════════ */
if (DO.has("p18")) {
  const { ctx, pg } = await open("light");
  await pg.goto(URL_ + "#1", { waitUntil: "load" });
  await pg.waitForTimeout(6800);
  await goto(pg, 18);
  const s = await st(pg);
  console.log(`  P18 · ${s.scene} mode=${s.mode} page=${s.page}`);
  await pg.screenshot({ path: `${OUT}/waveA-p18.png`, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await ctx.close();
  console.log("✔ waveA-p18.png");
}

/* ═══ ④ P18 版式 A/B（改前 = HEAD 的产物 · 改后 = 现在）══════════════ */
if (DO.has("ab")) {
  const OLD = "public/decks/_ab-p18-before.html";
  writeFileSync(OLD, execFileSync("git", ["show", "HEAD:public/decks/convoai-lab.html"],
                                  { maxBuffer: 1 << 28 }));
  const shots = [];
  for (const [file, tag] of [[OLD.replace("public", ""), "before"], ["/decks/convoai-lab.html", "after"]]) {
    const { ctx, pg } = await open("light");
    await pg.goto(BASE + file + "?lab=hold#1", { waitUntil: "load" });
    await pg.waitForTimeout(6800);
    await goto(pg, 18);
    const path = `${TMP}/p18-${tag}.png`;
    mkdirSync(TMP, { recursive: true });
    await pg.screenshot({ path, clip: { x: 60, y: 230, width: 1800, height: 400 } });
    shots.push(path);
    await ctx.close();
  }
  execFileSync("montage", ["-tile", "1x2", "-geometry", "1600x+8+8", "-background", "#dcdce2",
    ...shots, `${OUT}/waveA-p18-layout-ab.png`], { stdio: "pipe" });
  if (existsSync(OLD)) unlinkSync(OLD);
  console.log("✔ waveA-p18-layout-ab.png（上 = 改前 · 下 = 改后）");
}
await browser.close();
