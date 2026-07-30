import { chromium } from "playwright-core";
import { mkdirSync } from "fs";
mkdirSync("/tmp/qa5", { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.4 });
// 索引页（暗底）
await p.goto("http://localhost:3000/decks", { waitUntil: "networkidle" });
await p.waitForTimeout(2600);
await p.screenshot({ path: "/tmp/qa5/index-dark.png" });
// 抽查 3 份公众号 deck 暗/浅
const errs = [];
p.on("pageerror", e => errs.push(e.message.slice(0, 80)));
for (const slug of ["tolan", "evalprd", "highagency"]) {
  await p.goto(`http://localhost:3000/${slug}`, { waitUntil: "networkidle" });
  await p.waitForTimeout(2400);
  await p.screenshot({ path: `/tmp/qa5/${slug}-dark.png` });
  await p.evaluate(() => document.getElementById("deckSwap").click());
  await p.waitForTimeout(900);
  await p.screenshot({ path: `/tmp/qa5/${slug}-light.png` });
  await p.evaluate(() => { try { localStorage.setItem("colin-theme", "dark"); } catch {} });
}
console.log("pageerrors:", errs.length ? errs : "none");
// 全量 23 路由 200 检查
const slugs = ["tolan","paperhunt","029tb","voiceeval","openclaw","elys","staas","4mtokens","3days","systemcard","77days","csagent","arch","demolies","turns","evalprd","presence","interrupted","bottleneck","outcome","highagency","awsfde","34days"];
let bad = [];
for (const s of slugs) {
  const r = await p.goto(`http://localhost:3000/${s}`, { waitUntil: "domcontentloaded" });
  if (r.status() !== 200) bad.push(`${s}:${r.status()}`);
  const deckOk = await p.evaluate(() => typeof window.deck === "object" && document.querySelectorAll(".slide").length > 0).catch(() => false);
  if (!deckOk) bad.push(`${s}:no-deck`);
}
console.log(bad.length ? "BAD: " + bad.join(" ") : "all 23 decks OK");
await b.close();
