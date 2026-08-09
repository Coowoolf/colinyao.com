// robot26 · 二次自适配标定
// ------------------------------------------------------------------
// PPT 里 525 个文本框开了 PowerPoint 的「溢出时缩排文字」（<a:normAutofit>），
// 它烘焙的 fontScale 是按 Source Han Sans CN 的字宽算出来的。换成本站字体栈后，
// 拉丁字宽变了，少数段落会多折出一行 —— 那才是真正的还原偏差。
//
// 判据（三条，任一命中就二分缩字号）：
//   ① 出台：文字实际画到了 1920×1080 舞台之外；
//   ② 漏卡：文本框自己有填充/描边（是张看得见的卡片），文字画出了卡片；
//   ③ 孤字：最后一行只剩 ≤3 个字符 —— 典型的「差半个字宽多折一行」，
//      而 PPT 原稿里这一段是整行收住的。
// 「框比文字矮一点点」不算溢出：PPT 里大量文本框就是紧贴一行、且无填充无描边，
// PowerPoint 自己也是这么溢出显示的，照搬才是一比一。
//
// 结果写进 scripts/assets/robot26-bj-fit.json，由 build-robot26-bj.py 烘进静态 HTML。
// 幂等：脚本自己会「先清表重建 → 量 → 写表 → 再重建」，所以缩放系数永远是绝对值，
// 反复运行不会层层累乘。
// 用法：(cd public && python3 -m http.server 8899 &) ; node scripts/fit-robot26.mjs
import { chromium } from "playwright-core";
import { execSync } from "child_process";
import fs from "fs";

const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const OUT = "scripts/assets/robot26-bj-fit.json";
const FLOOR = 0.78;

// ① 先清空自适配表并重建，保证测的是「未缩过」的基准版
fs.rmSync(OUT, { force: true });
execSync("python3 scripts/build-robot26-bj.py", { stdio: "inherit" });

const b = await chromium.launch({ executablePath: exe });
const pg = await (await b.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
await pg.goto("http://localhost:8899/decks/robot26.html", { waitUntil: "networkidle" });
await pg.evaluate(() => document.fonts.ready);

const res = await pg.evaluate((FLOOR) => {
  const table = {}, hard = [];
  // 行带 = 竖直方向互不重叠的一组 client rect。
  // 不能按 rect.top 去重：同一行里 200px 的数字和 96px 的 % 号 top 不同，会被误数成两行。
  const bands = (p) => {
    const r = document.createRange();
    r.selectNodeContents(p);
    const rs = [...r.getClientRects()].filter((x) => x.height > 1).sort((a, c) => a.top - c.top);
    if (!rs.length) return [];
    const out = [{ top: rs[0].top, bot: rs[0].bottom, left: rs[0].left, right: rs[0].right }];
    for (const x of rs.slice(1)) {
      const l = out[out.length - 1];
      if (x.top < l.bot - 2) {
        l.bot = Math.max(l.bot, x.bottom); l.right = Math.max(l.right, x.right); l.left = Math.min(l.left, x.left);
      } else out.push({ top: x.top, bot: x.bottom, left: x.left, right: x.right });
    }
    return out;
  };
  // 最后一行剩几个字符（逐字符量，够用且便宜）
  const tailChars = (p) => {
    const bd = bands(p);
    if (bd.length < 2) return 99;
    const y = bd[bd.length - 1].top;
    let n = 0;
    const walk = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walk.nextNode())) {
      for (let i = 0; i < node.length; i++) {
        if (!node.data[i].trim()) continue;
        const r = document.createRange();
        r.setStart(node, i); r.setEnd(node, i + 1);
        const rc = r.getBoundingClientRect();
        if (rc.height > 1 && rc.top >= y - 2) n++;
      }
    }
    return n;
  };
  const stage = document.getElementById("deckStage").getBoundingClientRect();
  document.querySelectorAll(".slide").forEach((sec) => {
    sec.classList.add("visible");
    sec.querySelectorAll("[data-step]").forEach((e) => e.classList.add("on"));
    const p = sec.dataset.p;
    sec.querySelectorAll('.tx[data-af="1"]').forEach((el) => {
      const spans = [...el.querySelectorAll("span")];
      const ps = [...el.querySelectorAll("p")];
      if (!spans.length || !ps.length) return;
      const base = spans.map((s) => parseFloat(getComputedStyle(s).fontSize));
      const cs = getComputedStyle(el);
      const carded = cs.backgroundColor !== "rgba(0, 0, 0, 0)" || parseFloat(cs.borderTopWidth) > 0;
      const box = el.getBoundingClientRect();
      const apply = (k) => spans.forEach((s, i) => (s.style.fontSize = (base[i] * k).toFixed(2) + "px"));
      const ok = () => {
        for (const q of ps) {
          for (const bd of bands(q)) {
            if (bd.bot > stage.bottom - 2 || bd.top < stage.top - 2) return false;            // ① 出台
            if (bd.right > stage.right - 2 || bd.left < stage.left - 2) return false;
            if (carded && (bd.bot > box.bottom - 1 || bd.right > box.right - 1)) return false; // ② 漏卡
          }
          if (tailChars(q) <= 3) return false;                                                 // ③ 孤字
        }
        return !carded || el.scrollWidth <= el.clientWidth + 1;
      };
      if (ok()) return;
      let lo = FLOOR, hi = 1.0, best = null;
      for (let it = 0; it < 10; it++) {
        const k = (lo + hi) / 2;
        apply(k);
        if (ok()) { best = k; lo = k; } else hi = k;
      }
      if (best === null) { hard.push(p + ":" + el.dataset.sid); spans.forEach((s) => (s.style.fontSize = "")); return; }
      let chosen = Math.min(1, Math.round(Math.ceil(best * 200) / 2) / 100);
      apply(chosen);
      if (!ok()) { chosen = Math.max(FLOOR, Math.round((chosen - 0.005) * 1000) / 1000); apply(chosen); }
      table[p + ":" + el.dataset.sid] = chosen;
      spans.forEach((s) => (s.style.fontSize = ""));
    });
  });
  return { table, hard };
}, FLOOR);

const keys = Object.keys(res.table).sort((a, c) => {
  const [p1, s1] = a.split(":").map(Number), [p2, s2] = c.split(":").map(Number);
  return p1 - p2 || s1 - s2;
});
const sorted = {};
for (const k of keys) sorted[k] = res.table[k];
fs.writeFileSync(OUT, JSON.stringify(sorted, null, 1) + "\n");
console.log(`被二次缩排的文本框：${keys.length}`);
console.log(keys.map((k) => `${k}=${sorted[k]}`).join("  ") || "（无）");
if (res.hard.length) console.log(`⚠ 缩到 ${FLOOR} 仍不满足，需人工看：`, res.hard.join(" "));
await b.close();
// ② 带着新表再重建一次，产物即最终 HTML
execSync("python3 scripts/build-robot26-bj.py", { stdio: "inherit" });
