#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════════════════
   三轮「静态页升维」· 终审出图（闸门在 qa-convoai-lab.mjs 里，这里只出片）
   ---------------------------------------------------------------------------
   出什么：
     static-p{22,5,15,16}-{light,dark}.png   四枚加法层 · 双主题整页静帧
     static-p22.gif   6.0s ← 末页的涟漪（**看安静**：两处字标各自泛起、在中途相遇）
     static-p15.gif   6.0s ← 中心辐射（六簇各自的身份微动）
     static-p16-ab.png  P16 加 3D 前 / 后并排（「会不会伤可读性」的对照证据）
     lab-v3-contact-dark.png  22 页终版联览（暗底 · 4×6）
   ⚠ GIF **一律用 TOUR.pace 录**：容器里 SwiftShader 只有 3–4fps，
     按真实 dt 录出来名义 12fps、实际 3.4fps ⇒ 放出来快 3.5×，末页就成了高潮。
   用法：BASE=http://localhost:8899 node scripts/shot-static3.mjs
        DO=still,gif,ab,contact node scripts/shot-static3.mjs
   ═══════════════════════════════════════════════════════════════════════════ */
import { chromium } from 'playwright-core';
import { mkdirSync, rmSync, writeFileSync, existsSync, unlinkSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const BASE = process.env.BASE || 'http://localhost:8899';
const URL_ = BASE + '/decks/convoai-lab.html?lab=hold';
const OUT = process.env.OUT || '/home/claude/eco-review';
const TMP = '/tmp/static3-frames';
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const GL = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
const DO = new Set((process.env.DO || 'still,gif,ab,contact').split(',').map(s => s.trim()));
const PAGES = [22, 5, 15, 16];
// [页, 秒数, 起点]：末页从 t=2 起录 6s（一段完整的相遇扫过）· P15 从 t=1 起录 6s
const GIFS = [[22, 6.0, 2.0], [15, 6.0, 1.0]];
const FULL = { x: 0, y: 0, width: 1920, height: 1080 };
mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROME, args: GL });

async function open(theme) {
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 },
                                         deviceScaleFactor: 1 });
  await ctx.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, theme);
  return { ctx, pg: await ctx.newPage() };
}
async function goto(pg, n, wait = 3400) {
  await pg.evaluate((k) => window.deck.go(k - 1), n);
  await pg.waitForTimeout(wait);
  await pg.evaluate(() => document.querySelector('.slide.active')
    .querySelectorAll('[data-step]').forEach(e => e.classList.add('on')));
  await pg.waitForTimeout(1000);
}
const st = (pg) => pg.evaluate(() => {
  const c = document.getElementById('labGl'), u = window.__labTour.unit();
  return { mode: c.dataset.labMode, scene: c.dataset.labScene, page: +c.dataset.labPage,
           clr: u && u.state ? +u.state().clr.toFixed(1) : null };
});

/* ═══ ① 四页 · 双主题整页静帧 ══════════════════════════════════════════ */
if (DO.has('still')) for (const theme of ['light', 'dark']) {
  const { ctx, pg } = await open(theme);
  await pg.goto(URL_ + '#1', { waitUntil: 'load' });
  await pg.waitForTimeout(6800);
  for (const n of PAGES) {
    await goto(pg, n);
    // 定在「这一页最说明问题」的那一拍上：
    //   P22 t=6.0（一道相遇正扫过 logo 下方）· P5 t=1.1（接力注光正走到落点）
    //   P15 t=7.0（六处微动各在自己的相位上）· P16 常态
    const seek = { 22: 6.0, 5: 1.1, 15: 7.0, 16: 4.0 }[n];
    await pg.evaluate(() => window.__labTour.pace(12));
    await pg.evaluate((t) => window.__labTour.seek(t), seek);
    await pg.waitForTimeout(700);
    console.log(`  ${theme} P${n} ·`, JSON.stringify(await st(pg)));
    await pg.screenshot({ path: `${OUT}/static-p${n}-${theme}.png`, clip: FULL });
    await pg.evaluate(() => window.__labTour.pace(0));
  }
  await ctx.close();
}
if (DO.has('still')) console.log('✔ 四页双主题静帧 → static-p{22,5,15,16}-{light,dark}.png');

/* ═══ ② 实录 GIF（TOUR.pace 定拍 —— 录多久就是多久）══════════════════ */
if (DO.has('gif')) for (const [n, secs, from] of GIFS) {
  const dir = `${TMP}/p${n}`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open(n === 22 ? 'dark' : 'light');   // 末页的星野在暗底上最读得出
  await pg.goto(URL_ + '#1', { waitUntil: 'load' });
  await pg.waitForTimeout(6500);
  await goto(pg, n, 3600);
  await pg.addStyleTag({ content: '*,*::before,*::after{animation-play-state:paused!important}' });
  const FPS = 12, N = Math.round(secs * FPS);
  const t0 = await pg.evaluate(([f, s0]) => { window.__labTour.pace(f);
                                              return window.__labTour.seek(s0); }, [FPS, from]);
  for (let i = 0; i < N; i++) {
    await pg.screenshot({ path: `${dir}/f${String(i).padStart(3, '0')}.png`, clip: FULL });
    await pg.evaluate(() => window.__labTour.step(1));
    await pg.waitForTimeout(40);
  }
  const t1 = await pg.evaluate(() => window.__labTour.clock());
  // 末页的场很淡 —— 调色板给满 256 色、少抖动，否则星野在 GIF 里会被抹掉
  execFileSync('ffmpeg', ['-y', '-framerate', String(FPS), '-i', `${dir}/f%03d.png`,
    '-vf', 'scale=1200:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=256[p];'
         + '[b][p]paletteuse=dither=floyd_steinberg',
    '-loop', '0', `${OUT}/static-p${n}.gif`], { stdio: 'pipe' });
  console.log(`✔ static-p${n}.gif · ${N} 帧 @ ${FPS}fps · 场上钟走了 ${(t1 - t0).toFixed(2)}s`);
  await ctx.close();
}

/* ═══ ③ P16 加 3D 前 / 后并排（「会不会伤可读性」的对照证据）═══════════ */
if (DO.has('ab')) {
  const OLD = 'public/decks/_ab-static3-before.html';
  writeFileSync(OLD, execFileSync('git', ['show', 'HEAD:public/decks/convoai-lab.html'],
                                  { maxBuffer: 1 << 28 }));
  mkdirSync(TMP, { recursive: true });
  const shots = [];
  for (const [file, tag] of [[OLD.replace('public', ''), 'before'],
                             ['/decks/convoai-lab.html', 'after']]) {
    const { ctx, pg } = await open('light');
    await pg.goto(BASE + file + '?lab=hold#1', { waitUntil: 'load' });
    await pg.waitForTimeout(6800);
    await goto(pg, 16);
    const path = `${TMP}/p16-${tag}.png`;
    await pg.screenshot({ path, clip: { x: 100, y: 300, width: 1720, height: 580 } });
    shots.push(path);
    await ctx.close();
  }
  execFileSync('montage', [...shots, '-tile', '1x2', '-geometry', '+0+10',
                           '-background', '#e9eaee', `${OUT}/static-p16-ab.png`]);
  if (existsSync(OLD)) unlinkSync(OLD);
  console.log('✔ static-p16-ab.png（上 = 加 3D 前 · 下 = 加 3D 后）');
}

/* ═══ ④ 22 页终版联览（暗底 · 4×6）═══════════════════════════════════ */
if (DO.has('contact')) {
  const dir = `${TMP}/contact`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open('dark');
  await pg.goto(URL_ + '#1', { waitUntil: 'load' });
  await pg.waitForTimeout(6800);
  const files = [];
  for (let n = 1; n <= 22; n++) {
    await goto(pg, n, 2600);
    const f = `${dir}/p${String(n).padStart(2, '0')}.png`;
    await pg.screenshot({ path: f, clip: FULL });
    files.push(f);
  }
  await ctx.close();
  execFileSync('montage', [...files, '-tile', '4x6', '-geometry', '480x270+6+6',
                           '-background', '#0b0b10', `${OUT}/lab-v3-contact-dark.png`]);
  console.log('✔ lab-v3-contact-dark.png · 22 页 · 4×6');
}
await browser.close();
