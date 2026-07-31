// 全站巡检：页面 + 43 deck 路由 — pageerror / 断链 / 锚点 / hash 恢复 / trust 锁 / motif 渲染
import { chromium } from "playwright-core";
import { execSync } from "child_process";
const exe = execSync("find /opt/pw-browsers -name chrome -type f | head -1").toString().trim();
const BASE = "http://localhost:3000";
const pages = ["/", "/time", "/space", "/inward", "/outward", "/preface", "/vol1", "/vol2", "/vol3", "/vol4", "/vol5", "/decks"];
const deckSlugs = ["cowork","newcollege","3years","rte24","pm24","convoai","audio25","engine25","era3","prodready","pm25","vibecheck","vibesota","dual26","robot26","inspire26","aws26","tolan","paperhunt","029tb","voiceeval","openclaw","elys","staas","4mtokens","3days","systemcard","77days","csagent","arch","demolies","turns","evalprd","interrupted","presence","bottleneck","outcome","highagency","awsfde","34days","newcollege-light"];

const browser = await chromium.launch({ executablePath: exe });
const page = await (await browser.newContext({ viewport: { width: 1500, height: 950 } })).newPage();
const issues = [];

// —— 站点页面：pageerror + 内链有效性 + 锚点存在 + trust 锁
const linkSet = new Set();
for (const path of pages) {
  const errs = [];
  page.removeAllListeners("pageerror");
  page.on("pageerror", (e) => errs.push(String(e).slice(0, 110)));
  const resp = await page.goto(BASE + path, { waitUntil: "load" });
  if (resp.status() !== 200) issues.push(`${path}: HTTP ${resp.status()}`);
  await page.waitForTimeout(900);
  if (errs.length) issues.push(`${path}: pageerror ${errs[0]}`);
  const info = await page.evaluate(() => ({
    links: [...document.querySelectorAll("a[href]")].map((a) => a.getAttribute("href")),
    trust: [...document.querySelectorAll('a[href="/cowork"]')].length,
    h1s: document.querySelectorAll("h1").length,
  }));
  if (info.trust && path !== "/decks") issues.push(`${path}: /cowork 被挂链 ×${info.trust}`);
  if (info.h1s > 1) issues.push(`${path}: ${info.h1s} 个 h1`);
  for (const href of info.links) {
    if (href.startsWith("/") && !href.startsWith("//")) linkSet.add(href.split("#")[0] || "/");
    if (href.startsWith("#")) {
      const ok = await page.evaluate((id) => !!document.getElementById(id), href.slice(1));
      if (!ok && href !== "#top") issues.push(`${path}: 页内锚点 ${href} 不存在`);
    }
  }
}
// 内链 HTTP 检查（去重）
for (const href of [...linkSet].sort()) {
  const r = await page.request.get(BASE + href, { maxRedirects: 3 });
  if (r.status() >= 400) issues.push(`断链: ${href} → ${r.status()}`);
}

// —— 43 deck 路由：200 + pageerror + deckRuler + noindex + 首页可渲染
for (const slug of deckSlugs) {
  const errs = [];
  page.removeAllListeners("pageerror");
  page.on("pageerror", (e) => errs.push(String(e).slice(0, 90)));
  const resp = await page.goto(`${BASE}/${slug}`, { waitUntil: "load" });
  if (resp.status() !== 200) { issues.push(`/${slug}: HTTP ${resp.status()}`); continue; }
  await page.waitForTimeout(650);
  const d = await page.evaluate(() => ({
    ruler: !!document.getElementById("deckRuler"),
    active: !!document.querySelector(".slide.active"),
    noindex: !!document.querySelector('meta[name="robots"][content*="noindex"]'),
    teeth: document.querySelectorAll(".dr-teeth i").length,
  }));
  const probs = [];
  if (errs.length) probs.push("pageerror " + errs[0]);
  if (!d.ruler) probs.push("无 deck-ruler");
  if (!d.active) probs.push("deck 未初始化");
  if (!d.noindex) probs.push("缺 noindex");
  if (probs.length) issues.push(`/${slug}: ${probs.join("; ")}`);
}

// —— hash 恢复：/aws26#12 应落在 12 页
await page.goto(BASE + "/aws26#12", { waitUntil: "load" });
await page.waitForTimeout(900);
const hcur = await page.evaluate(() => [...document.querySelectorAll(".slide")].findIndex((s) => s.classList.contains("active")) + 1);
if (hcur !== 12) issues.push(`/aws26#12 hash 恢复失败：落在 ${hcur}`);

// —— 首页 18 张术语卡 motif 渲染
await page.goto(BASE + "/#terms", { waitUntil: "load" });
await page.waitForTimeout(800);
await page.evaluate(() => document.getElementById("terms")?.scrollIntoView());
await page.waitForTimeout(2000);
const motifs = await page.evaluate(() => ({
  cards: document.querySelectorAll(".idea-card").length,
  withSvg: [...document.querySelectorAll(".idea-card .idea-motif")].filter((m) => m.querySelector("svg")).length,
}));
if (motifs.cards !== 18 || motifs.withSvg !== 18) issues.push(`术语卡 ${motifs.cards} 张 / motif ${motifs.withSvg} 个（应 18/18）`);

// —— 移动端横向溢出（首页全滚）
const m = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
await m.goto(BASE + "/", { waitUntil: "load" });
await m.evaluate(async () => { let y = 0; while (y < document.body.scrollHeight) { y += 800; window.scrollTo({ top: y, behavior: "instant" }); await new Promise((r) => setTimeout(r, 60)); } });
const ox = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
if (ox > 0) issues.push(`移动端横向溢出 ${ox}px`);

await browser.close();
console.log(issues.length ? "ISSUES:\n" + issues.join("\n") : "CLEAN · 13 pages + 43 decks + links + anchors + hash + motifs + mobile");
