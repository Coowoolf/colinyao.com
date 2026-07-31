import { chromium } from "playwright-core";
import { execSync } from "child_process";
const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1560, height: 980 } })).newPage();
let fails = [];
for (const [slug, N] of [["tolan", 22], ["newcollege", 92], ["3years", 48], ["cowork", 63], ["aws26", 38]]) {
  const errs = [];
  page.removeAllListeners("pageerror");
  page.on("pageerror", (e) => errs.push(String(e).slice(0, 90)));
  await page.goto(`http://localhost:3000/${slug}`, { waitUntil: "load" });
  await page.waitForTimeout(1200);
  // 点击顶线 60% 处 → 应跳到 ~0.6N
  const box = await page.locator("#deckRuler").boundingBox();
  await page.mouse.click(box.x + box.width * 0.6, box.y + 8);
  await page.waitForTimeout(900);
  const r = await page.evaluate(() => {
    const slides = [...document.querySelectorAll(".slide")];
    const cur = slides.findIndex((s) => s.classList.contains("active")) + 1;
    const fillW = document.querySelector(".dr-fill").getBoundingClientRect().width;
    const trackW = document.querySelector(".dr-track").getBoundingClientRect().width;
    const teeth = document.querySelectorAll(".dr-teeth i").length;
    return { cur, ratio: fillW / trackW, teeth, hash: location.hash };
  });
  const expect = Math.floor(0.6 * N) + 1;
  const ok = Math.abs(r.cur - expect) <= 1 && Math.abs(r.ratio - r.cur / N) < 0.05 && r.teeth > 10 && !errs.length;
  console.log(`${slug}: cur=${r.cur}/${N} (期望≈${expect}) fill=${(r.ratio * 100).toFixed(1)}% teeth=${r.teeth} hash=${r.hash} ${errs[0] ?? ""} ${ok ? "OK" : "FAIL"}`);
  if (!ok) fails.push(slug);
  // 数字键跳页：敲 3 → Enter
  await page.keyboard.type("3");
  await page.keyboard.press("Enter");
  await page.waitForTimeout(700);
  const cur2 = await page.evaluate(() => [...document.querySelectorAll(".slide")].findIndex((s) => s.classList.contains("active")) + 1);
  if (cur2 !== 3) { console.log(`${slug}: digit-jump got ${cur2}`); fails.push(slug + "-digit"); }
}
// hover 态截图（newcollege 92 页 · 刻度齿抽稀）
await page.goto("http://localhost:3000/newcollege", { waitUntil: "load" });
await page.waitForTimeout(1000);
const b = await page.locator("#deckRuler").boundingBox();
await page.mouse.move(b.x + b.width * 0.42, b.y + 6);
await page.waitForTimeout(500);
await page.screenshot({ path: "/tmp/ruler-hover.png", clip: { x: 0, y: 0, width: 1560, height: 120 } });
// 浅底
await page.goto("http://localhost:3000/tolan", { waitUntil: "load" });
await page.evaluate(() => localStorage.setItem("colin-theme", "light"));
await page.reload({ waitUntil: "load" });
await page.waitForTimeout(900);
const b2 = await page.locator("#deckRuler").boundingBox();
await page.mouse.move(b2.x + b2.width * 0.7, b2.y + 6);
await page.waitForTimeout(500);
await page.screenshot({ path: "/tmp/ruler-hover-light.png", clip: { x: 0, y: 0, width: 1560, height: 120 } });
await browser.close();
console.log(fails.length ? "FAILS: " + fails.join(",") : "ALL GREEN");
