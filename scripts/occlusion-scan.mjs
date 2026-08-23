/* ═══════════════════════════════════════════════════════════════════
   occlusion-scan.mjs · convoai deck「文字遮盖扫描器」
   ───────────────────────────────────────────────────────────────────
   为什么要有这个东西：
     Colin 反复遇到「文字被遮住 / 显示不全」。既有的 qa-convoai.mjs 只查
     元素盒溢出（getBoundingClientRect 的粗盒），查不出：
       ① 两块文字互相压在一起（盒子不重叠、字形行框重叠）
       ② 文字被后画的不透明卡片 / 条 / 图盖住
       ③ 文字被祖先的 overflow:hidden / clip-path / mask 裁掉半行
     而且只查终态 —— 分步（build）过程中的中间态遮盖在现场照样会出现。

   本扫描器：全部页 × 每页全部分步状态 × 双主题，用 Range.getClientRects()
   取「真实字形行框」而不是元素盒，逐对判定三类命中：
     TEXT-TEXT         两块文字的字形行框相交
     TEXT-UNDER-BLOCK  文字被画序更晚的不透明块盖住
     CLIPPED           文字被画布 / overflow:hidden / clip-path / mask 裁切

   用法：node scripts/occlusion-scan.mjs                （默认扫 convoai.html）
         DECK_URL=http://localhost:8777/decks/convoai-info.html node scripts/occlusion-scan.mjs
         VIEWPORT=1280x720 node scripts/occlusion-scan.mjs   （换视口，见下）
   产出：/home/claude/optim/occlusion-report.md
         /home/claude/optim/occlusion-shots/pNN-sS-theme.png
         （DECK_URL 指向别的 deck 时，产出自动改名：convoai-info → occlusion-info.md
           + occlusion-shots-info/；默认 URL 的产出路径一字不变）
   只读 deck，不改 deck。

   ── 视口（2026-08-23 采纳项 H · 补第二档分辨率）─────────────────────────────
   默认仍是 1920×1080（舞台 scale = 1，与此前逐字等价）。VIEWPORT=1280x720 时
   .deck-stage 被 transform:scale(.667) 缩过，getBoundingClientRect 拿到的全是**缩过的**
   设备像素 —— 若原样喂进判定，CANVAS(0,0,1920,1080) 与 MIN_AREA/MIN_SIDE 三个常量
   会同时错位。这里的做法是：所有 DOMRect 一律先经 toStage() 折回**舞台坐标系**
   （减去舞台原点、再除以 scale），于是 CANVAS 与三个阈值的含义在两档分辨率下完全一致，
   两份报告可以直接对照。字号同理（fsz 也要除 scale，否则墨迹框系数算歪）。
   ═══════════════════════════════════════════════════════════════════ */
import { chromium } from 'playwright-core';
import { mkdirSync, writeFileSync } from 'fs';
import { execSync } from 'child_process';
import http from 'http';

const CHROME    = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const URL       = process.env.DECK_URL || 'http://localhost:8777/decks/convoai.html';
const DECK      = (URL.match(/\/([^/?#]+)\.html/) || [, 'convoai'])[1];   // convoai / convoai-info
const TAG       = DECK === 'convoai' ? '' : '-' + DECK.replace(/^convoai-/, '');
/* 视口：默认 1920×1080（历史行为）。VIEWPORT=1280x720 走缩放档，产出自动带 -1280 后缀，
   两档报告互不覆盖。 */
const VP        = (process.env.VIEWPORT || '1920x1080').split('x').map(Number);
const VIEWPORT  = { width: VP[0] || 1920, height: VP[1] || 1080 };
const VTAG      = VIEWPORT.width === 1920 ? '' : `-${VIEWPORT.width}`;
const OUT_DIR   = process.env.OCC_SHOTS  || `/home/claude/optim/occlusion-shots${TAG}${VTAG}`;
const REPORT    = process.env.OCC_REPORT || (TAG || VTAG
                                             ? `/home/claude/optim/occlusion${TAG}${VTAG}.md`
                                             : '/home/claude/optim/occlusion-report.md');
const THEMES    = ['light', 'dark'];
let TOTAL       = 0;                       // 实际页数，扫描时从页面读回，报告里用它

/* ── 判定阈值（报告里会原样注明）────────────────────────────────
   MIN_AREA  相交面积下限，低于此值视为「边缘 kiss」不报
   MIN_SIDE  相交矩形的最短边下限，进一步压掉 1-3px 抗锯齿级擦边
   INK_K     字形行框系数：行盒往往比字形高（line-height），按 fontSize*INK_K
             居中收缩成「墨迹框」，避免相邻两行的行盒虚假相交            */
const MIN_AREA = +(process.env.MIN_AREA ?? 40);
const MIN_SIDE = +(process.env.MIN_SIDE ?? 3);
const INK_K    = +(process.env.INK_K   ?? 1.0);
const NOSHOT   = process.env.NOSHOT === '1';   // 调阈值时跳过截图，跑得快

/* ═══ 0. 服务器 ═══════════════════════════════════════════════════ */
function probe(url) {
  return new Promise((res) => {
    const req = http.get(url, (r) => { r.resume(); res(r.statusCode); });
    req.on('error', () => res(0));
    req.setTimeout(2500, () => { req.destroy(); res(0); });
  });
}
async function ensureServer() {
  if (await probe(URL) === 200) { console.log('· server 8777 已在'); return; }
  console.log('· server 8777 未响应，拉起 serve.mjs');
  execSync('(setsid nohup node /home/claude/serve.mjs > /tmp/serve.log 2>&1 &)', { shell: '/bin/bash' });
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 300));
    if (await probe(URL) === 200) { console.log('· server 已就绪'); return; }
  }
  throw new Error('serve.mjs 拉起失败，见 /tmp/serve.log');
}

/* ═══ 1. 页内状态设置（直接改 class，比走 deck.go 更确定）═════════
   踩过的坑：只注入 transition-duration:0s 不够 —— 页面加载时 deck.go() 已经
   起跑的那批 transition 不会因为 duration 变 0 而取消，clip-path 会停在
   `inset(-9.57px calc(4.3% - 15.3px) ...)` 这种中间态上，几何全错。
   所以每个状态都：全部 class 摘掉 → 强制回流 → 重新挂（此时 duration=0，
   一步到终值）→ 再把残留的 Animation 一律 finish()。                     */
function setState({ n, s }) {
  const slides = [...document.querySelectorAll('.slide')];
  slides.forEach((el) => {
    el.classList.remove('active', 'visible');
    el.querySelectorAll('[data-step]').forEach(x => x.classList.remove('on'));
  });
  void document.body.offsetWidth;                       // 强制回流，让「未入场态」落定
  const cur = slides[n - 1];
  cur.classList.add('active', 'visible');
  cur.querySelectorAll('[data-step]').forEach((el) => {
    if ((+el.dataset.step || 0) <= s) el.classList.add('on');
  });
  if (window.deck) { window.deck.i = n - 1; window.deck.step = s; }
  void cur.offsetWidth;
  try { document.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} }); } catch (e) {}
}

/* ═══ 2. 页内扫描 —— 全部几何计算都在浏览器里做 ═══════════════════ */
function scanState({ n, MIN_AREA, MIN_SIDE, INK_K }) {
  const slide = document.querySelectorAll('.slide')[n - 1];
  const CANVAS = { l: 0, t: 0, r: 1920, b: 1080 };
  /* 舞台坐标系折算（2026-08-23 采纳项 H）：1280 视口下 .deck-stage 带 scale(.667)，
     DOMRect 全是缩过的设备像素。一律折回舞台坐标，CANVAS 与三个阈值的含义才不随视口漂。
     1920 视口下 SC===1、原点 (0,0) ⇒ 这一层是恒等变换，与改动前逐字等价。 */
  const _st = (document.querySelector('.deck-stage') || slide).getBoundingClientRect();
  const SC = _st.width ? _st.width / 1920 : 1;
  const OX = _st.left, OY = _st.top;
  const toStage = (r) => ({
    l: (r.left - OX) / SC, t: (r.top - OY) / SC,
    r: (r.right - OX) / SC, b: (r.bottom - OY) / SC,
  });
  /* 纯装饰层：整份不参与（遮它 / 被它遮都不算问题）*/
  const DECOR = '.hero-art,.conf-bg,.deck-flow,.deck-grid,.deck-rail,.conf-aura';

  const iw = (a, b) => Math.min(a.r, b.r) - Math.max(a.l, b.l);
  const ih = (a, b) => Math.min(a.b, b.b) - Math.max(a.t, b.t);
  const inter = (a, b) => ({ l: Math.max(a.l, b.l), t: Math.max(a.t, b.t), r: Math.min(a.r, b.r), b: Math.min(a.b, b.b) });
  const areaOf = (a) => Math.max(0, a.r - a.l) * Math.max(0, a.b - a.t);
  const interArea = (a, b) => Math.max(0, iw(a, b)) * Math.max(0, ih(a, b));
  const rnd = (r) => ({ l: Math.round(r.l), t: Math.round(r.t), r: Math.round(r.r), b: Math.round(r.b) });

  /* —— CSS 短路径（从 section 起算，nth-child 保证跨状态稳定）—— */
  function shortPath(el) {
    const seg = [];
    let e = el;
    while (e && e !== slide) {
      const cls = [...e.classList].filter(c => c !== 'on' && c !== 'visible' && c !== 'active');
      const idx = e.parentElement ? [...e.parentElement.children].indexOf(e) + 1 : 1;
      seg.unshift(e.tagName.toLowerCase() + (cls.length ? '.' + cls.join('.') : '') + `:nth(${idx})`);
      e = e.parentElement;
    }
    return seg.join(' > ');
  }
  const brief = (el, txt) => {
    const cls = [...el.classList].filter(c => c !== 'on').join('.');
    const t = (txt || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 20);
    return `${el.tagName.toLowerCase()}${cls ? '.' + cls : ''}${t ? ' 「' + t + '」' : ''}`;
  };

  /* —— 归属组：同一 .sh / .sig 内部的一切互不判定 —— */
  function groupRoot(el) {
    let e = el, last = el;
    while (e && e !== slide) {
      if (e.classList && (e.classList.contains('sh') || e.classList.contains('sig'))) return e;
      last = e; e = e.parentElement;
    }
    return last;
  }

  /* —— 画序（近似 stacking order）：从 section 到自身，逐层 [z, 文档序] —— */
  const ord = new Map();
  let counter = 0;
  function stackChain(el) {
    const arr = [];
    let e = el;
    while (e && e !== slide) { arr.push(e); e = e.parentElement; }
    arr.reverse();
    return arr.map((x) => {
      const cs = getComputedStyle(x);
      const z = (cs.position !== 'static' && cs.zIndex !== 'auto') ? (parseInt(cs.zIndex, 10) || 0) : 0;
      return [z, ord.get(x) ?? 0];
    });
  }
  function cmpStack(a, b) {           // >0 表示 a 画在 b 之上
    const L = Math.min(a.length, b.length);
    for (let i = 0; i < L; i++) {
      if (a[i][0] !== b[i][0]) return a[i][0] - b[i][0];
      if (a[i][1] !== b[i][1]) return a[i][1] - b[i][1];
    }
    return a.length - b.length;
  }

  /* —— 裁剪范围：画布 ∩ 所有 overflow:hidden 祖先 ∩ clip-path ∩ mask 盒 —— */
  /* clip-path:inset() 解析。必须按括号深度切词 —— transition 中间态会出现
     `calc(4.30596% - 15.311px)`，天真的 /\s+/ 切词会把它劈成三段解析出 NaN，
     NaN 一旦混进 reg，`outside <= MIN_AREA` 恒为 false → 刷屏假命中。      */
  function splitTop(str) {
    const out = []; let depth = 0, cur = '';
    for (const ch of str) {
      if (ch === '(') depth++;
      if (ch === ')') depth--;
      if (/\s/.test(ch) && depth === 0) { if (cur) out.push(cur); cur = ''; continue; }
      cur += ch;
    }
    if (cur) out.push(cur);
    return out;
  }
  function lenToPx(tok, base) {
    const t = tok.trim();
    if (/^calc\(/i.test(t)) {                       // 只解 `calc(A% ± Bpx)` 这一种形状
      const inner = t.slice(5, -1);
      const mm = /^\s*(-?[\d.]+)%\s*([+-])\s*(-?[\d.]+)px\s*$/.exec(inner);
      if (!mm) return NaN;
      return (+mm[1]) / 100 * base + (mm[2] === '-' ? -1 : 1) * (+mm[3]);
    }
    if (t.endsWith('%')) { const v = parseFloat(t); return Number.isFinite(v) ? v / 100 * base : NaN; }
    const v = parseFloat(t);
    return Number.isFinite(v) ? v : NaN;
  }
  function parseInset(cp, box) {
    const m = /^inset\((.*)\)\s*$/.exec(cp.trim());
    if (!m) return null;
    const body = m[1].split(/\s+round\s+/)[0].trim();
    const v = splitTop(body);
    if (!v.length) return null;
    const four = v.length === 1 ? [v[0], v[0], v[0], v[0]]
      : v.length === 2 ? [v[0], v[1], v[0], v[1]]
        : v.length === 3 ? [v[0], v[1], v[2], v[1]]
          : [v[0], v[1], v[2], v[3]];
    const W = box.r - box.l, H = box.b - box.t;
    const top = lenToPx(four[0], H), right = lenToPx(four[1], W),
      bottom = lenToPx(four[2], H), left = lenToPx(four[3], W);
    if (![top, right, bottom, left].every(Number.isFinite)) return null;   // 解不动就不裁，宁可漏
    return { l: box.l + left, t: box.t + top, r: box.r - right, b: box.b - bottom };
  }
  const finiteRect = (r) => r && [r.l, r.t, r.r, r.b].every(Number.isFinite);
  function clipRegion(el) {
    let reg = { ...CANVAS };
    const note = [];
    let e = el;
    while (e && e.nodeType === 1) {
      const cs = getComputedStyle(e);
      const bb = e.getBoundingClientRect();
      const box = toStage(bb);
      const bw = box.r - box.l, bh = box.b - box.t;      // 舞台坐标下的尺寸
      if (/hidden|clip|scroll|auto/.test(cs.overflowX) || /hidden|clip|scroll|auto/.test(cs.overflowY)) {
        if (bw > 0 && bh > 0 && !(bw >= 1900 && bh >= 1060) && finiteRect(box)) {
          reg = inter(reg, box); note.push('overflow@' + brief(e, ''));
        }
      }
      if (cs.clipPath && cs.clipPath !== 'none') {
        const cr = parseInset(cs.clipPath, box);
        if (finiteRect(cr)) { reg = inter(reg, cr); note.push('clip-path@' + brief(e, '')); }
      }
      /* .ink 的液态扫过 mask：mask-size 300% 100% / position 0% —— 纵向恰好是元素盒，
         盒外的第二行会被整段 mask 掉（这套 deck 的经典「标题第二行消失」）*/
      const mi = cs.maskImage || cs.webkitMaskImage;
      if (mi && mi !== 'none' && e.classList.contains('ink') && finiteRect(box)) {
        reg = inter(reg, { l: box.l, t: box.t, r: box.l + (box.r - box.l) * 3, b: box.b });
        note.push('ink-mask@' + brief(e, ''));
      }
      e = e.parentElement;
    }
    return { reg, note };
  }

  /* ═══ 遍历：同时收「可见文本行框」和「不透明覆盖块」════════════ */
  const texts = [], blocks = [];
  function alphaOf(c) {
    const m = /rgba?\(([^)]+)\)/.exec(c || '');
    if (!m) return 0;
    const p = m[1].split(',').map(Number);
    return p.length > 3 ? p[3] : 1;
  }
  function walk(el) {
    ord.set(el, counter++);
    if (el.matches && el.matches(DECOR)) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    if (!(parseFloat(cs.opacity) > 0.02)) return;
    if (el.hasAttribute('data-step') && !el.classList.contains('on')) return;   // 未到步

    /* ① 不透明覆盖块 */
    const isImg = el.tagName === 'IMG';
    const hasBg = alphaOf(cs.backgroundColor) > 0.05 || (cs.backgroundImage && cs.backgroundImage !== 'none');
    if ((hasBg || isImg) && !el.classList.contains('dot') && el !== slide) {
      const bx = toStage(el.getBoundingClientRect());
      const bw = bx.r - bx.l, bh = bx.b - bx.t;
      const full = bw >= 1900 && bh >= 1060;
      if (bw >= 6 && bh >= 6 && !full) blocks.push({ el, rect: bx });
    }

    /* ② 文本行框：只取「直接文本子节点」，用 Range 拿真实字形行框 */
    const fsz = (parseFloat(cs.fontSize) || 16) / SC;      // 折回舞台坐标下的字号
    for (const node of el.childNodes) {
      if (node.nodeType !== 3) continue;
      const raw = node.nodeValue;
      if (!raw || !raw.trim()) continue;
      const rg = document.createRange();
      rg.selectNodeContents(node);
      for (const dr of rg.getClientRects()) {
        const r = toStage(dr);
        const rw = r.r - r.l, rh = r.b - r.t;
        if (rw < 4 || rh < 4) continue;
        const inkH = Math.min(rh, fsz * INK_K);
        const pad = (rh - inkH) / 2;
        texts.push({
          el, txt: raw.trim(),
          rect: { l: r.l + 1, t: r.t + pad, r: r.r - 1, b: r.b - pad },
        });
      }
    }
    for (const c of el.children) walk(c);
  }
  walk(slide);

  texts.forEach(t => { t.g = groupRoot(t.el); t.st = stackChain(t.el); });
  blocks.forEach(b => { b.g = groupRoot(b.el); b.st = stackChain(b.el); });

  const related = (a, b) => a === b || a.contains(b) || b.contains(a);
  const hits = [];

  /* —— a) TEXT-TEXT —— */
  for (let i = 0; i < texts.length; i++) {
    for (let j = i + 1; j < texts.length; j++) {
      const A = texts[i], B = texts[j];
      if (A.g === B.g) continue;                       // 同一 .sh / 行内 strong·em·span
      if (related(A.el, B.el) || related(A.g, B.g)) continue;
      const w = iw(A.rect, B.rect), h = ih(A.rect, B.rect);
      if (w < MIN_SIDE || h < MIN_SIDE || w * h <= MIN_AREA) continue;
      hits.push({
        type: 'TEXT-TEXT', area: Math.round(w * h), box: rnd(inter(A.rect, B.rect)),
        aPath: shortPath(A.g), bPath: shortPath(B.g),
        a: brief(A.el, A.txt), b: brief(B.el, B.txt),
      });
    }
  }

  /* —— b) TEXT-UNDER-BLOCK：块画在文字之后才算「盖住」—— */
  for (const T of texts) {
    for (const K of blocks) {
      if (T.g === K.g) continue;                       // 卡内自己的字不算
      if (related(T.el, K.el) || related(T.g, K.g)) continue;
      if (cmpStack(K.st, T.st) <= 0) continue;         // 块在文字之前画 → 文字在上，可读
      const w = iw(T.rect, K.rect), h = ih(T.rect, K.rect);
      if (w < MIN_SIDE || h < MIN_SIDE || w * h <= MIN_AREA) continue;
      hits.push({
        type: 'TEXT-UNDER-BLOCK', area: Math.round(w * h), box: rnd(inter(T.rect, K.rect)),
        aPath: shortPath(T.g), bPath: shortPath(K.g),
        a: brief(T.el, T.txt), b: brief(K.el, ''),
      });
    }
  }

  /* —— c) TEXT-x-SPILL：块「越界溢出」自己的 .sh 盒，撞到别人的字 ——
     典型：`.pp .sh{overflow:visible}`（0,2,0）压过 `.strip{overflow:hidden}`（0,1,0），
     `height:auto` 的位图按原始比例撑出盒外几百 px，砸在下一排卡片上。
     这类不看画序：块盖字 = 字被遮；字盖块 = 字压在一张本不该在那儿的图上，都要报。 */
  for (const K of blocks) {
    const S = K.g;
    if (S === K.el) continue;                        // 块本身就是 .sh，不算越界
    const box = toStage(S.getBoundingClientRect());
    const B = K.rect;
    const bands = [];
    if (B.t < box.t - 4) bands.push({ l: B.l, t: B.t, r: B.r, b: Math.min(B.b, box.t) });
    if (B.b > box.b + 4) bands.push({ l: B.l, t: Math.max(B.t, box.b), r: B.r, b: B.b });
    if (B.l < box.l - 4) bands.push({ l: B.l, t: B.t, r: Math.min(B.r, box.l), b: B.b });
    if (B.r > box.r + 4) bands.push({ l: Math.max(B.l, box.l), t: B.t, r: B.r, b: B.b });
    if (!bands.length) continue;
    for (const T of texts) {
      if (T.g === S || related(T.el, K.el) || related(T.g, S)) continue;
      let best = null;
      for (const bd of bands) {
        const w = iw(T.rect, bd), h = ih(T.rect, bd);
        if (w < MIN_SIDE || h < MIN_SIDE || w * h <= MIN_AREA) continue;
        if (!best || w * h > best.a) best = { a: w * h, r: inter(T.rect, bd) };
      }
      if (!best) continue;
      hits.push({
        type: 'TEXT-x-SPILL', area: Math.round(best.a), box: rnd(best.r),
        aPath: shortPath(T.g), bPath: shortPath(S),
        a: brief(T.el, T.txt),
        b: `${brief(K.el, '')} 溢出所属 ${brief(S, '')} 盒外 ` +
           `${Math.round(Math.max(box.t - B.t, B.b - box.b, box.l - B.l, B.r - box.r))}px`,
      });
    }
  }

  /* —— d) CLIPPED —— */
  for (const T of texts) {
    const { reg, note } = clipRegion(T.el);
    if (!finiteRect(reg)) continue;
    const outside = areaOf(T.rect) - interArea(T.rect, reg);
    if (!Number.isFinite(outside) || outside <= MIN_AREA) continue;
    const dirs = [];
    if (T.rect.l < reg.l - 0.5) dirs.push(`左出 ${Math.round(reg.l - T.rect.l)}px`);
    if (T.rect.t < reg.t - 0.5) dirs.push(`上出 ${Math.round(reg.t - T.rect.t)}px`);
    if (T.rect.r > reg.r + 0.5) dirs.push(`右出 ${Math.round(T.rect.r - reg.r)}px`);
    if (T.rect.b > reg.b + 0.5) dirs.push(`下出 ${Math.round(T.rect.b - reg.b)}px`);
    hits.push({
      type: 'CLIPPED', area: Math.round(outside), box: rnd(T.rect),
      aPath: shortPath(T.g), bPath: note[note.length - 1] || 'canvas 1920×1080',
      a: brief(T.el, T.txt), b: (note.length ? note.join(' / ') : '画布 1920×1080') + ' · ' + dirs.join('·'),
    });
  }
  return { hits, nText: texts.length, nBlock: blocks.length };
}

/* ═══ 3. 主流程 ═══════════════════════════════════════════════════ */
await ensureServer();
mkdirSync(OUT_DIR, { recursive: true });

const browser = await chromium.launch({ executablePath: CHROME });
const found = new Map();          // dedupKey -> 记录
let rawHits = 0, states = 0;
const shots = new Set();

for (const theme of THEMES) {
  const ctx = await browser.newContext({ viewport: VIEWPORT, deviceScaleFactor: 1 });
  if (theme === 'dark') await ctx.addInitScript(() => { try { localStorage.setItem('colin-theme', 'dark'); } catch (e) {} });
  const page = await ctx.newPage();
  await page.goto(URL + '#1', { waitUntil: 'load' });
  if (theme === 'dark') { await page.reload({ waitUntil: 'load' }); }
  /* 动效归零：入场是 transition、hero/aura 是 animation，两者都掐掉取终值 */
  await page.addStyleTag({ content: '*,*::before,*::after{animation-duration:0s !important;animation-delay:0s !important;transition-duration:0s !important;transition-delay:0s !important;}' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(400);

  const steps = await page.evaluate(() => [...document.querySelectorAll('.slide')].map(s => +s.dataset.steps || 0));
  TOTAL = steps.length;
  const themeTag = (await page.evaluate(() => document.documentElement.getAttribute('data-theme'))) || 'light';
  if ((theme === 'dark') !== (themeTag === 'dark')) console.log(`! 主题态异常：期望 ${theme} 实得 ${themeTag}`);

  for (let n = 1; n <= steps.length; n++) {
    for (let s = 0; s <= steps[n - 1]; s++) {
      await page.evaluate(setState, { n, s });
      await page.waitForTimeout(70);
      const { hits } = await page.evaluate(scanState, { n, MIN_AREA, MIN_SIDE, INK_K });
      states++;
      rawHits += hits.length;
      if (hits.length) {
        const shotName = `p${String(n).padStart(2, '0')}-s${s}-${theme}.png`;
        if (!shots.has(shotName)) {
          shots.add(shotName);
          if (!NOSHOT) await page.screenshot({ path: `${OUT_DIR}/${shotName}`,
            clip: { x: 0, y: 0, width: VIEWPORT.width, height: VIEWPORT.height } });
        }
        for (const h of hits) {
          const key = `${n}|${h.type}|${h.aPath}|${h.bPath}`;
          const rec = found.get(key);
          if (!rec) {
            found.set(key, {
              page: n, type: h.type, a: h.a, b: h.b, aPath: h.aPath, bPath: h.bPath,
              area: h.area, box: h.box, firstStep: s, firstTheme: theme,
              steps: new Set([s]), themes: new Set([theme]), shot: shotName,
            });
          } else {
            rec.steps.add(s); rec.themes.add(theme);
            if (h.area > rec.area) { rec.area = h.area; rec.box = h.box; }
          }
        }
      }
    }
    process.stdout.write(`\r  ${theme} P${n}/${steps.length} · 累计去重命中 ${found.size}   `);
  }
  console.log('');
  await ctx.close();
}
await browser.close();

/* ═══ 4. 报告 ═════════════════════════════════════════════════════ */
/* 遮盖三类（真的看不见字）同级优先，CLIPPED（字被切掉一截）次之；同级按相交面积降序 */
const SEV = { 'TEXT-TEXT': 0, 'TEXT-UNDER-BLOCK': 0, 'TEXT-x-SPILL': 0, 'CLIPPED': 1 };
const list = [...found.values()].sort((x, y) => (SEV[x.type] - SEV[y.type]) || (y.area - x.area) || (x.page - y.page));

const FIXHINT = {
  'TEXT-TEXT': '两块文字改为互不重叠的栅格位（把后一块的 top 下移到前一块 rect.b + 24px，或缩窄 width 让其换行落在自己的列内）',
  'TEXT-UNDER-BLOCK': '把被压的文字挪出该块的矩形（左右让位 / 上下错行），或让文字元素排在该块之后（DOM 后移即画在其上）',
  'CLIPPED': '放大所属 .sh 的 height / width 到实际行框尺寸，或把文案缩短一行（clip-path/mask 只认元素盒，盒不够就一定被切）',
};
function hint(r) {
  const B = r.box;
  const sh = r.aPath.split('>').pop().trim();
  if (r.type === 'CLIPPED') {
    const m = /([上下左右])出 (\d+)px/.exec(r.b);
    const over = m ? +m[2] : 0;
    if (/下出/.test(r.b)) return `${sh} 的 height 至少再加 ${over + 6}px（或压缩字号 / 把文案减到一行）—— clip-path 只认元素盒，盒装不下就一定切一截`;
    if (/右出/.test(r.b)) return `${sh} 的 width 至少再加 ${over + 8}px，或让文案在盒内换行`;
    return FIXHINT.CLIPPED;
  }
  if (r.type === 'TEXT-x-SPILL') {
    return `给溢出块所属的 .sh 补 \`overflow:hidden\`（\`.pp .sh{overflow:visible}\` 特异度 0,2,0 压过了 \`.strip/.case/.frame{overflow:hidden}\` 的 0,1,0，`
      + `必须写成 \`.pp .sh.strip{overflow:hidden}\` 才生效），或把该位图改成 \`height:100%;object-fit:cover\` 不再按原始比例撑高`;
  }
  if (r.type === 'TEXT-UNDER-BLOCK') {
    return `二选一：覆盖块 ${r.bPath.split('>').pop().trim()} 的 left 右移到 ≥${B.r + 20}（宽度相应收窄），`
      + `或把文字 ${sh} 收进相交区之外（右边界压到 ≤${B.l - 12} / top 下移到 ≥${B.b + 16}）；相交区 x∈[${B.l},${B.r}] y∈[${B.t},${B.b}]`;
  }
  return `错开两块（相交区 x∈[${B.l},${B.r}] y∈[${B.t},${B.b}]）—— 后画的一块 top 改到 ≥${B.b + 20} 或 left 改到 ≥${B.r + 24}`;
}

const byPage = new Map();
for (const r of list) byPage.set(r.page, (byPage.get(r.page) || 0) + 1);
const byType = { 'TEXT-TEXT': 0, 'TEXT-UNDER-BLOCK': 0, 'TEXT-x-SPILL': 0, 'CLIPPED': 0 };
for (const r of list) byType[r.type]++;

const L = [];
L.push(`# ${DECK}.html · 文字遮盖扫描报告`);
L.push('');
L.push(`- 扫描对象：\`public/decks/${DECK}.html\`（${TOTAL} 页 · 舞台 1920×1080）`);
L.push(`- 浏览器视口：**${VIEWPORT.width}×${VIEWPORT.height}**`
  + (VIEWPORT.width === 1920 ? '（舞台 scale = 1）'
     : `（舞台 scale = ${(VIEWPORT.width / 1920).toFixed(3)}，几何全部折回舞台坐标系后再判定）`));
L.push(`- 扫描面：${TOTAL} 页 × 每页全部分步状态（s=0…data-steps）× 双主题 light/dark = **${states} 个状态**`);
L.push(`- 生成时间：${new Date().toISOString()}`);
L.push(`- 扫描器：\`scripts/occlusion-scan.mjs\`（playwright-core · Range.getClientRects 取字形行框）`);
L.push('');
L.push('## 判定口径与最终阈值');
L.push('');
L.push('| 类型 | 判定 |');
L.push('| --- | --- |');
L.push('| `TEXT-TEXT` | 两块文字的字形行框相交（且不同属一个 `.sh`） |');
L.push('| `TEXT-UNDER-BLOCK` | 文字被一个不透明块盖住，且该块在画序上**晚于**文字 |');
L.push('| `TEXT-x-SPILL` | 文字撞上一个「越界溢出自己 `.sh` 盒」的块（位图/色块跑到盒外几百 px），不看画序 |');
L.push('| `CLIPPED` | 文字被画布 / `overflow:hidden` 祖先 / `clip-path` / `.ink` 的 mask 裁掉 |');
L.push('');
L.push(`| 项 | 取值 | 说明 |`);
L.push(`| --- | --- | --- |`);
L.push(`| 相交面积阈值 | **${MIN_AREA} px²** | 低于此值视为边缘 kiss，不报 |`);
L.push(`| 相交最短边 | **${MIN_SIDE} px** | 再压一道，杜绝 1-3px 抗锯齿级擦边误报 |`);
L.push(`| 字形行框系数 | **${INK_K} × font-size** | 行盒按 font-size×${INK_K} 居中收缩成「墨迹框」，相邻行的行盒虚假相交被排除 |`);
L.push(`| 动效处理 | animation/transition 时长归零 | 以 computed 终值判定，不受入场动画中间帧影响 |`);
L.push('');
L.push('排除项（不参与判定）：`.hero-art` 装饰底图、`.conf-bg` 背景板、`.deck-grid/.deck-rail/.conf-aura` 舞台装饰、');
L.push('`.dot` 14×14 图例色块、同一 `.sh`/`.sig` 内部的一切（含行内 `<strong>/<b>/<em>/<span>` 与父文本）、');
L.push('画序早于文字的覆盖块（文字画在其上 → 可读，`.callout-chip`/P23 图上标注这类「有意悬浮」由此自动豁免）。');
L.push('');
L.push('## 统计');
L.push('');
L.push(`| 指标 | 数值 |`);
L.push(`| --- | --- |`);
L.push(`| 去重后命中总数 | **${list.length}** |`);
L.push(`| 原始命中（含跨步/跨主题重复） | ${rawHits} |`);
L.push(`| TEXT-TEXT（文字压文字） | ${byType['TEXT-TEXT']} |`);
L.push(`| TEXT-UNDER-BLOCK（文字被块盖） | ${byType['TEXT-UNDER-BLOCK']} |`);
L.push(`| TEXT-x-SPILL（文字撞上越界溢出的块） | ${byType['TEXT-x-SPILL']} |`);
L.push(`| CLIPPED（文字被裁切） | ${byType['CLIPPED']} |`);
L.push(`| 涉及页数 | ${byPage.size} / ${TOTAL} |`);
L.push(`| 截图 | ${shots.size} 张 · \`${OUT_DIR}/\` |`);
L.push('');
L.push('### 按页分布');
L.push('');
if (byPage.size) {
  L.push('| 页 | 命中数 | 类型 |');
  L.push('| --- | --- | --- |');
  for (const p of [...byPage.keys()].sort((a, b) => a - b)) {
    const ts = list.filter(r => r.page === p);
    const c = {};
    ts.forEach(r => { c[r.type] = (c[r.type] || 0) + 1; });
    L.push(`| P${p} | ${byPage.get(p)} | ${Object.entries(c).map(([k, v]) => `${k}×${v}`).join(' · ')} |`);
  }
} else {
  L.push('_全场零命中。_');
}
L.push('');
L.push('### 先修这三条');
L.push('');
if (list.length) {
  list.slice(0, 3).forEach((r, i) => {
    L.push(`${i + 1}. **P${r.page} · ${r.type} · ${r.area} px²** —— ${r.a} × ${r.b}（截图 \`${r.shot}\`）`);
  });
} else {
  L.push('_无。_');
}
L.push('');
L.push('---');
L.push('');
L.push('## 明细（遮盖三类 TEXT-TEXT / TEXT-UNDER-BLOCK / TEXT-x-SPILL 优先，CLIPPED 次之；同级按相交面积降序）');
L.push('');
if (!list.length) L.push('_无。_');
list.forEach((r, i) => {
  const st = [...r.steps].sort((a, b) => a - b).join(',');
  L.push(`### ${i + 1}. [${r.type}] P${r.page} · ${r.area} px²`);
  L.push('');
  L.push(`- **A（文字）**：\`${r.a}\``);
  L.push(`- **B（${r.type === 'CLIPPED' ? '裁剪源' : '对方'}）**：\`${r.b}\``);
  L.push(`- 相交/越界矩形：\`x ${r.box.l}→${r.box.r} · y ${r.box.t}→${r.box.b}\``);
  L.push(`- 首次出现：**步 s=${r.firstStep}**（${r.firstTheme}）；全部命中步 s=[${st}]；主题 ${[...r.themes].join(' + ')}`);
  L.push(`- 路径 A：\`${r.aPath}\``);
  if (r.type !== 'CLIPPED') L.push(`- 路径 B：\`${r.bPath}\``);
  L.push(`- 截图：\`${r.shot}\``);
  L.push(`- 修复方向：${hint(r)}`);
  L.push('');
});
writeFileSync(REPORT, L.join('\n'), 'utf8');

console.log(`\n✓ 状态 ${states} · 原始命中 ${rawHits} · 去重 ${list.length} · 截图 ${shots.size}`);
console.log(`  TEXT-TEXT ${byType['TEXT-TEXT']} · TEXT-UNDER-BLOCK ${byType['TEXT-UNDER-BLOCK']} · TEXT-x-SPILL ${byType['TEXT-x-SPILL']} · CLIPPED ${byType['CLIPPED']}`);
console.log(`  报告 → ${REPORT}`);
