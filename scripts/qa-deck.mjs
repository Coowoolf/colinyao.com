import { chromium } from "playwright-core";
import { mkdirSync } from "fs";
mkdirSync("/tmp/deckshots", { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
const errs = [];
p.on("pageerror", e => errs.push("PAGEERROR: " + e.message.slice(0, 160)));
await p.goto("http://localhost:3000/3years#1", { waitUntil: "networkidle" });
await p.waitForTimeout(2000);

const problems = [];
for (let n = 1; n <= 48; n++) {
  await p.evaluate(i => window.deck.go(i), n - 1);
  await p.waitForTimeout(n <= 2 ? 2600 : 2200);
  // 走完分步
  const steps = await p.evaluate(() => window.deck.maxStep[window.deck.i]);
  for (let s = 0; s < steps; s++) { await p.evaluate(() => window.deck.next()); await p.waitForTimeout(1400); }
  const r = await p.evaluate(() => {
    const stage = document.getElementById("deckStage").getBoundingClientRect();
    const slide = document.querySelector(".slide.active");
    const out = [];
    const tol = 6;
    slide.querySelectorAll("*").forEach(el => {
      if (!el.textContent?.trim() && el.tagName !== "svg" && el.tagName !== "path") return;
      const cs = getComputedStyle(el);
      if (+cs.opacity === 0 || cs.visibility === "hidden") return;
      const b = el.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) return;
      if (b.left < stage.left - tol || b.right > stage.right + tol || b.top < stage.top - tol || b.bottom > stage.bottom + tol) {
        out.push(`${el.tagName}.${(el.className.baseVal ?? el.className ?? "").toString().slice(0, 30)} [${Math.round(b.left - stage.left)},${Math.round(b.top - stage.top)},${Math.round(b.right - stage.left)},${Math.round(b.bottom - stage.top)}] txt:${(el.textContent || "").trim().slice(0, 18)}`);
      }
    });
    return out.slice(0, 4);
  });
  if (r.length) problems.push(`S${n}: ${r.join(" | ")}`);
  if ([1, 3, 7, 11, 13, 17, 20, 21, 24, 26, 27, 31, 36, 40, 42, 47, 48].includes(n)) {
    await p.screenshot({ path: `/tmp/deckshots/s${String(n).padStart(2, "0")}.png` });
  }
}
console.log("errors:", errs.length ? errs : "none");
console.log(problems.length ? "OVERFLOW:\n" + problems.join("\n") : "overflow: none");
await b.close();
