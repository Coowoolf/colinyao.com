#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════════════════
   二轮精修 · 波B · 终审出图（闸门在 qa-convoai-lab.mjs 里，这里只出片）
   ---------------------------------------------------------------------------
   出什么：
     waveB-p{2,7,10,13}-{light,dark}.png   四页 · 双主题整页静帧
     waveB-p2.gif    7.0s ← **一个舞台 morph 周期**（两代相位差半周期 ⇒ 台面 7s 一循环，
                            这 7s 里含「波→格」与「格→波」两处变形）
     waveB-p13.gif   6.0s ← 含一次完整热切换（在位机体沿 −z 退到 −320、候选从景深进坞）
     waveB-p7.gif    8.9s ← 地形整幅左移一整趟（8.91s 无缝回卷）
     waveB-p10-ab.png       轻手术前后对比（上 = 改前 = HEAD 的产物 · 下 = 改后）
                            附**零位移**自证：两版的 DOM 标注逐像素相同
     labv2-pairs-sheet.png  16 页双主题并排联览
     labv2-final-contact-dark.png  22 页暗底全联览
   ⚠ GIF **一律用 TOUR.pace 录**（波A 的教训）：容器里 SwiftShader 只有 3–4fps，
     老办法录出来名义 12fps、实际 3.4fps ⇒ 放出来快 3.5×。
   用法：BASE=http://localhost:8899 node scripts/shot-waveb.mjs
        DO=still,gif,ab,pairs,contact node scripts/shot-waveb.mjs
   ═══════════════════════════════════════════════════════════════════════════ */
import { chromium } from 'playwright-core';
import { mkdirSync, rmSync, writeFileSync, existsSync, unlinkSync } from 'node:fs';
import { execFileSync } from 'node:child_process';

const BASE = process.env.BASE || 'http://localhost:8899';
const URL_ = BASE + '/decks/convoai-lab.html?lab=hold';
const OUT = process.env.OUT || '/home/claude/eco-review';
const TMP = '/tmp/waveb-frames';
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const GL = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
const DO = new Set((process.env.DO || 'still,gif,ab,pairs,contact').split(',').map(s => s.trim()));
const PAGES = [2, 7, 10, 13];
const ALL16 = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 21];
// [页, 秒数, 起点]：P2 录一个**舞台周期**（7s）· P13 从热切换前 0.4s 起录 · P7 录一整趟
const GIFS = [[2, 7.0, 0.0], [13, 6.0, 6.0], [7, 8.9, 0.0]];
mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: CHROME, args: GL });

async function open(theme, w = 1920, h = 1080) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await ctx.addInitScript((t) => { try { localStorage.setItem('colin-theme', t); } catch (e) {} }, theme);
  return { ctx, pg: await ctx.newPage() };
}
async function goto(pg, n, wait = 3800) {
  await pg.evaluate((k) => window.deck.go(k - 1), n);
  await pg.waitForTimeout(wait);
  await pg.evaluate(() => document.querySelector('.slide.active')
    .querySelectorAll('[data-step]').forEach(e => e.classList.add('on')));
  await pg.waitForTimeout(1400);          // 等分步的缓动落位
}
const st = (pg) => pg.evaluate(() => {
  const c = document.getElementById('labGl');
  return { mode: c.dataset.labMode, scene: c.dataset.labScene, page: +c.dataset.labPage,
           fps: c.dataset.labFps, dpr: c.dataset.labDpr };
});

/* ═══ ① 四页 · 双主题整页静帧 ══════════════════════════════════════════ */
if (DO.has('still')) for (const theme of ['light', 'dark']) {
  const { ctx, pg } = await open(theme);
  await pg.goto(URL_ + '#1', { waitUntil: 'load' });
  await pg.waitForTimeout(6800);
  for (const n of PAGES) {
    await goto(pg, n);
    // 定在「这一页最说明问题」的那一拍上：
    //   P2 t=7.6 让位峰值（格架正转过去让第二道入射波）· P13 t=7.2 热切换中点
    //   P7 t=1.2（判定晕与晶柱各在一枚事件上）· P10 常态
    const seek = { 2: 7.6, 13: 7.2, 7: 1.2 }[n];
    if (seek !== undefined) {
      await pg.evaluate(() => window.__labTour.pace(12));
      await pg.evaluate((t) => window.__labTour.seek(t), seek);
      await pg.waitForTimeout(900);
    }
    const s = await st(pg);
    console.log(`  ${theme} P${n} · ${s.scene} mode=${s.mode} page=${s.page} dpr=${s.dpr}`);
    await pg.screenshot({ path: `${OUT}/waveB-p${n}-${theme}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    if (seek !== undefined) await pg.evaluate(() => window.__labTour.pace(0));
  }
  await ctx.close();
}
if (DO.has('still')) console.log('✔ 四页双主题静帧 → waveB-p{2,7,10,13}-{light,dark}.png');

/* ═══ ② 实录 GIF（TOUR.pace 定拍）═════════════════════════════════════ */
if (DO.has('gif')) for (const [n, secs, from] of GIFS) {
  const dir = `${TMP}/p${n}`;
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open('light', 1920, 1080);
  await pg.goto(URL_ + '#1', { waitUntil: 'load' });
  await pg.waitForTimeout(6500);
  await goto(pg, n, 3600);
  // 入场走完之后再冻 CSS：本波三页的可见动效全在 canvas 上
  await pg.addStyleTag({ content: '*,*::before,*::after{animation-play-state:paused!important}' });
  const FPS = 12, N = Math.round(secs * FPS);
  const t0 = await pg.evaluate(([f, s0]) => { window.__labTour.pace(f);
                                              return window.__labTour.seek(s0); }, [FPS, from]);
  for (let i = 0; i < N; i++) {
    await pg.screenshot({ path: `${dir}/f${String(i).padStart(3, '0')}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    await pg.evaluate(() => window.__labTour.step(1));
    await pg.waitForTimeout(40);                   // 让 rAF 至少重画一次
  }
  const t1 = await pg.evaluate(() => window.__labTour.clock());
  const probe = await pg.evaluate(() => { const u = window.__labTour.unit();
                                          return u && u.state ? u.state() : null; });
  execFileSync('ffmpeg', ['-y', '-framerate', String(FPS), '-i', `${dir}/f%03d.png`,
    '-vf', 'scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=200[p];[b][p]paletteuse=dither=bayer:bayer_scale=3',
    '-loop', '0', `${OUT}/waveB-p${n}.gif`], { stdio: 'pipe' });
  console.log(`✔ waveB-p${n}.gif · ${N} 帧 @ ${FPS}fps · 场上钟走了 ${(t1 - t0).toFixed(2)}s`
    + (probe && probe.run !== undefined && typeof probe.run === 'number'
       ? ` · 地形实走 ${(probe.run / (t1 - t0 + from)).toFixed(1)}px/s` : ''));
  await ctx.close();
}

/* ═══ ③ P10 轻手术 A/B（改前 = HEAD 的产物 · 改后 = 现在）+ 零位移自证 ═══ */
if (DO.has('ab')) {
  const OLD = 'public/decks/_ab-p10-before.html';
  writeFileSync(OLD, execFileSync('git', ['show', 'HEAD:public/decks/convoai-lab.html'],
                                  { maxBuffer: 1 << 28 }));
  const shots = [], labels = [];
  for (const [file, tag] of [[OLD.replace('public', ''), 'before'], ['/decks/convoai-lab.html', 'after']]) {
    const { ctx, pg } = await open('light');
    await pg.goto(BASE + file + '?lab=hold#1', { waitUntil: 'load' });
    await pg.waitForTimeout(6800);
    await goto(pg, 10);
    const path = `${TMP}/p10-${tag}.png`;
    mkdirSync(TMP, { recursive: true });
    await pg.screenshot({ path, clip: { x: 110, y: 270, width: 1700, height: 680 } });
    shots.push(path);
    /* 零位移自证：把该页所有 DOM 文字件的**外接矩形**逐条抄下来。
       3D 换了皮，坐标一格没动 ⇒ 两版的这张表必须逐条相同。 */
    labels.push(await pg.evaluate(() => [...document.querySelectorAll('.slide[data-p="10"] text')]
      .map(t => { const r = t.getBoundingClientRect();
                  return [t.textContent.trim().slice(0, 8), Math.round(r.x), Math.round(r.y)]; })));
    await ctx.close();
  }
  const same = JSON.stringify(labels[0]) === JSON.stringify(labels[1]);
  const cap = same
    ? `ZERO DRIFT VERIFIED · ${labels[0].length} labels, all at identical x/y`
    : `WARNING: ${labels[0].filter((a, i) => JSON.stringify(a) !== JSON.stringify(labels[1][i])).length} labels moved`;
  execFileSync('montage', ['-tile', '1x2', '-geometry', '1600x+10+10', '-background', '#dcdce2',
    '-label', 'BEFORE  (wave A)', shots[0], '-label', `AFTER  (wave B light surgery) — ${cap}`, shots[1],
    '-pointsize', '22', '-fill', '#222', `${OUT}/waveB-p10-ab.png`], { stdio: 'pipe' });
  if (existsSync(OLD)) unlinkSync(OLD);
  console.log(`✔ waveB-p10-ab.png（上 = 改前 · 下 = 改后）· 零位移自证：${cap}`);
}

/* ═══ ④ 16 页双主题并排联览 ═══════════════════════════════════════════ */
if (DO.has('pairs')) {
  const dir = `${TMP}/pairs`; rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  for (const theme of ['light', 'dark']) {
    const { ctx, pg } = await open(theme);
    await pg.goto(URL_ + '#1', { waitUntil: 'load' });
    await pg.waitForTimeout(6800);
    for (const n of ALL16) {
      await goto(pg, n, 2600);
      await pg.evaluate(() => window.__labTour.pace(24));
      await pg.evaluate(() => window.__labTour.seek(3.0));   // 两版同拍才有可比性
      await pg.waitForTimeout(700);
      await pg.screenshot({ path: `${dir}/${theme}-p${String(n).padStart(2, '0')}.png`,
                            clip: { x: 0, y: 0, width: 1920, height: 1080 } });
      await pg.evaluate(() => window.__labTour.pace(0));
    }
    await ctx.close();
  }
  const files = [];
  for (const n of ALL16) {
    const pp = String(n).padStart(2, '0');
    files.push(`${dir}/light-p${pp}.png`, `${dir}/dark-p${pp}.png`);
  }
  execFileSync('montage', ['-tile', '2x', '-geometry', '760x+6+6', '-background', '#9a9aa2',
    ...files, `${OUT}/labv2-pairs-sheet.png`], { stdio: 'pipe' });
  console.log('✔ labv2-pairs-sheet.png（16 页 · 左浅右暗并排）');
}

/* ═══ ⑤ 22 页暗底全联览 ═══════════════════════════════════════════════ */
if (DO.has('contact')) {
  const dir = `${TMP}/contact`; rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const { ctx, pg } = await open('dark');
  await pg.goto(URL_ + '#1', { waitUntil: 'load' });
  await pg.waitForTimeout(6800);
  for (let n = 1; n <= 22; n++) {
    await pg.evaluate((k) => window.deck.go(k - 1), n);
    await pg.waitForTimeout(2200);
    await pg.evaluate(() => document.querySelector('.slide.active')
      .querySelectorAll('[data-step]').forEach(e => e.classList.add('on')));
    await pg.waitForTimeout(900);
    await pg.screenshot({ path: `${dir}/p${String(n).padStart(2, '0')}.png`,
                          clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  }
  await ctx.close();
  execFileSync('bash', ['-c',
    `montage -tile 4x -geometry 470x+5+5 -background '#0b0b10' ${dir}/p*.png ${OUT}/labv2-final-contact-dark.png`],
    { stdio: 'pipe' });
  console.log('✔ labv2-final-contact-dark.png（22 页 · 暗底）');
}
await browser.close();
