import { chromium } from "playwright-core";
import { mkdirSync } from "fs";
mkdirSync("/tmp/vibeshots", { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
const errs = [];
p.on("pageerror", e => errs.push("PAGEERROR: " + e.message.slice(0, 160)));
await p.goto("http://localhost:3000/vibecheck#1", { waitUntil: "networkidle" });
await p.waitForTimeout(2200);

const SHOT = new Set([1, 2, 3, 4, 7, 9, 10, 11, 13, 15, 17, 20, 21]);
const problems = [];
const N = await p.evaluate(() => window.deck.slides.length);
for (let n = 1; n <= N; n++) {
  await p.evaluate(i => window.deck.go(i), n - 1);
  await p.waitForTimeout(n <= 2 ? 2400 : 1900);
  const steps = await p.evaluate(() => window.deck.maxStep[window.deck.i]);
  for (let s = 0; s < steps; s++) { await p.evaluate(() => window.deck.next()); await p.waitForTimeout(1200); }
  const r = await p.evaluate(() => {
    const stage = document.getElementById("deckStage").getBoundingClientRect();
    const slide = document.querySelector(".slide.active");
    const out = [];
    const tol = 6;
    // 1) 元素越出舞台
    slide.querySelectorAll("*").forEach(el => {
      if (!el.textContent?.trim() && el.tagName !== "svg" && el.tagName !== "path") return;
      const cs = getComputedStyle(el);
      if (+cs.opacity === 0 || cs.visibility === "hidden") return;
      const b = el.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) return;
      if (b.left < stage.left - tol || b.right > stage.right + tol || b.top < stage.top - tol || b.bottom > stage.bottom + tol)
        out.push(`STAGE-OVF ${el.tagName} txt:${(el.textContent || "").trim().slice(0, 24)}`);
    });
    // 2) SVG text 越出所在 slide 的 svg 视口 或 压到相邻 rect 边界之外
    slide.querySelectorAll("svg").forEach(svg => {
      const sb = svg.getBoundingClientRect();
      svg.querySelectorAll("text").forEach(t => {
        const tb = t.getBoundingClientRect();
        if (tb.width === 0) return;
        if (tb.left < sb.left - 4 || tb.right > sb.right + 4)
          out.push(`SVG-OVF text "${t.textContent.slice(0, 30)}" [${Math.round(tb.right - sb.right)}px past]`);
      });
    });
    // 3) 残留中文
    slide.querySelectorAll("*").forEach(el => {
      for (const c of el.childNodes) if (c.nodeType === 3 && /[一-鿿]/.test(c.textContent))
        out.push(`CN-RESIDUE "${c.textContent.trim().slice(0, 30)}"`);
    });
    return out;
  });
  if (r.length) problems.push(`slide ${n}: ` + r.join(" | "));
  if (SHOT.has(n)) await p.screenshot({ path: `/tmp/vibeshots/d${String(n).padStart(2, "0")}.png` });
}
// light theme spot checks
await p.evaluate(() => { localStorage.setItem("colin-theme", "light"); });
for (const n of [1, 2, 9, 15]) {
  await p.goto(`http://localhost:3000/vibecheck#${n}`, { waitUntil: "networkidle" });
  await p.waitForTimeout(2400);
  const steps = await p.evaluate(() => window.deck.maxStep[window.deck.i]);
  for (let s = 0; s < steps; s++) { await p.evaluate(() => window.deck.next()); await p.waitForTimeout(1100); }
  await p.screenshot({ path: `/tmp/vibeshots/L${String(n).padStart(2, "0")}.png` });
}
console.log("slides:", N);
console.log(problems.length ? problems.join("\n") : "NO PROBLEMS");
console.log(errs.length ? errs.join("\n") : "NO PAGE ERRORS");
await b.close();
