import { chromium } from "playwright-core";
import { mkdirSync } from "fs";
mkdirSync("/tmp/coworkshots", { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
const errs = [];
p.on("pageerror", e => errs.push("PAGEERROR: " + e.message.slice(0, 160)));
await p.goto("http://localhost:3000/cowork#1", { waitUntil: "networkidle" });
await p.waitForTimeout(2200);
const CHANGED = [42, 52, 53, 54];
const problems = [];
const N = await p.evaluate(() => window.deck.slides.length);
for (let n = 1; n <= N; n++) {
  await p.evaluate(i => window.deck.go(i), n - 1);
  await p.waitForTimeout(CHANGED.includes(n) ? 1900 : 900);
  const steps = await p.evaluate(() => window.deck.maxStep[window.deck.i]);
  for (let s = 0; s < steps; s++) { await p.evaluate(() => window.deck.next()); await p.waitForTimeout(CHANGED.includes(n) ? 1100 : 400); }
  if (CHANGED.includes(n)) await p.waitForTimeout(800);
  const r = await p.evaluate(() => {
    const stage = document.getElementById("deckStage").getBoundingClientRect();
    const slide = document.querySelector(".slide.active");
    const out = []; const tol = 6;
    slide.querySelectorAll("*").forEach(el => {
      if (!el.textContent?.trim() && el.tagName !== "svg" && el.tagName !== "path") return;
      const cs = getComputedStyle(el);
      if (+cs.opacity === 0 || cs.visibility === "hidden") return;
      const b = el.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) return;
      if (b.left < stage.left - tol || b.right > stage.right + tol || b.top < stage.top - tol || b.bottom > stage.bottom + tol)
        out.push(`STAGE-OVF ${el.tagName}.${(el.className.baseVal ?? el.className ?? "").toString().slice(0,20)} txt:${(el.textContent || "").trim().slice(0, 20)}`);
    });
    slide.querySelectorAll("svg").forEach(svg => {
      const sb = svg.getBoundingClientRect();
      svg.querySelectorAll("text").forEach(t => {
        const tb = t.getBoundingClientRect();
        if (tb.width === 0) return;
        if (tb.left < sb.left - 4 || tb.right > sb.right + 4)
          out.push(`SVG-OVF "${t.textContent.slice(0, 24)}" [${Math.round(Math.max(sb.left - tb.left, tb.right - sb.right))}px]`);
      });
    });
    return out;
  });
  if (r.length) problems.push(`slide ${n}: ` + r.join(" | "));
  if (CHANGED.includes(n)) await p.screenshot({ path: `/tmp/coworkshots/d${String(n).padStart(2, "0")}.png` });
}
console.log("slides:", N);
console.log(problems.length ? problems.join("\n") : "NO OVERFLOW");
console.log(errs.length ? errs.join("\n") : "NO PAGE ERRORS");
await b.close();
