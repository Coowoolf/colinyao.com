import { chromium } from "playwright-core";
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
await p.goto("http://localhost:3000/3years#1", { waitUntil: "networkidle" });
await p.waitForTimeout(2200);
const problems = [];
for (let n = 1; n <= 48; n++) {
  await p.evaluate(i => window.deck.go(i), n - 1);
  await p.waitForTimeout(2000);
  const steps = await p.evaluate(() => window.deck.maxStep[window.deck.i]);
  for (let s = 0; s < steps; s++) { await p.evaluate(() => window.deck.next()); await p.waitForTimeout(1200); }
  const r = await p.evaluate(() => {
    const slide = document.querySelector(".slide.active");
    // 收集"文字叶子"元素
    const nodes = [];
    slide.querySelectorAll("text, h1, h2, h3, p, span, div, b, i, td, th").forEach(el => {
      if (el.children.length > 0 && el.tagName !== "text") {
        // 仅收集不含元素子节点的（叶子），或 svg text
        const onlyText = [...el.childNodes].every(c => c.nodeType === 3 || (c.nodeType === 1 && ["B","I","EM","SPAN","BR"].includes(c.tagName) && c.children.length === 0));
        if (!onlyText) return;
      }
      const t = (el.textContent || "").trim();
      if (!t) return;
      const cs = getComputedStyle(el);
      if (+cs.opacity === 0 || cs.visibility === "hidden") return;
      const bb = el.getBoundingClientRect();
      if (bb.width < 4 || bb.height < 4) return;
      nodes.push({ el, t: t.slice(0, 14), bb, svg: el.tagName === "text" });
    });
    const out = [];
    for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], c = nodes[j];
      if (a.el.contains(c.el) || c.el.contains(a.el)) continue;
      // 只关心 svg 文本与 html 文本、或 svg-svg 之间的碰撞（html 排版自身有 flow 不会重叠）
      if (!a.svg && !c.svg) continue;
      const ox = Math.min(a.bb.right, c.bb.right) - Math.max(a.bb.left, c.bb.left);
      const oy = Math.min(a.bb.bottom, c.bb.bottom) - Math.max(a.bb.top, c.bb.top);
      if (ox > 10 && oy > 8) out.push(`"${a.t}" × "${c.t}" (${Math.round(ox)}x${Math.round(oy)})`);
    }
    return [...new Set(out)].slice(0, 5);
  });
  if (r.length) problems.push(`S${n}: ${r.join(" ; ")}`);
}
console.log(problems.length ? "COLLISIONS:\n" + problems.join("\n") : "collisions: none");
await b.close();
