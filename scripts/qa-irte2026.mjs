// QA：/irte2026（iRTE 2026 实时智能大会 · 产品专场版，46 页）走查。
// 骨架照 scripts/qa-confv2.mjs：46 页 step 推满 + 零溢出 + P3 录音按键行为 + 反向闸。
// 增量闸门（irte 家族专属）：
//   ② logo 盒 (1660,39)–(1883,120) 内不得有任何文字墨迹
//   ③ 四张章节页：像素章节号 / `> ` 当前章 / `PART n · XXX` 小标题
//   ④ 四页案例留白：5 个 .ph-box + eyebrow 含「待定」+ 母稿案例关键词清零
//   ⑤ 一页带走：四个对象 + 四个图标标题
//   ⑥ P2 主场开场口径   ⑦ P1 封面   ⑧ Q&A 尾卡   ⑪ 计算样式抽检
// 跑法：先起静态服务器
//   cd /home/claude/colinyao.com && (setsid nohup python3 -m http.server 8899 --directory public &)
//   node scripts/qa-irte2026.mjs
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");

const BASE = process.env.BASE || "http://127.0.0.1:8899";
const DECK = process.env.DECK || "/decks/irte2026.html";
const exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

const b = await chromium.launch({ executablePath: exe, args: ["--autoplay-policy=no-user-gesture-required", "--mute-audio"] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = [];
pg.on("pageerror", (e) => errs.push("pageerror: " + e.message));
let fail = 0;
const chk = (ok, label) => { if (!ok) fail++; console.log((ok ? "✓ " : "✗ ") + label); };

await pg.goto(BASE + DECK, { waitUntil: "load" });
await pg.waitForFunction(() => window.deck && window.deck.slides && window.deck.slides.length === 46);

// ── 1) 46 页全量走查：data-step 推满 + 溢出检查 + logo 盒墨迹闸 ──────────────
const n = await pg.evaluate(() => window.deck.slides.length);
const overflow = [];
const logoInk = [];
let logoProbed = 0;
for (let i = 0; i < n; i++) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(120);
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const els = [...s.querySelectorAll("[data-step]")];
    const mx = els.length ? Math.max(...els.map((e) => +e.dataset.step || 0)) : 0;
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  });
  await pg.waitForTimeout(60);

  const bad = await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i], r = s.getBoundingClientRect(), out = [];
    s.querySelectorAll("div,p,h1,h2,h3,span,li,td,th").forEach((el) => {
      if (!el.offsetParent) return;
      const b2 = el.getBoundingClientRect();
      if (b2.width && b2.height && (b2.bottom > r.bottom + 4 || b2.right > r.right + 4)) {
        const t = (el.textContent || "").trim().slice(0, 40);
        if (t) out.push(t);
      }
    });
    return out.slice(0, 3);
  });
  if (bad.length) overflow.push({ slide: i + 1, bad });

  // ── logo 盒占位闸 ──────────────────────────────────────────────────────
  // 任务书写的是「盒内 5×3 网格 elementsFromPoint，命中的元素只能是结构容器」。
  // 实测 .wrap / .head / .eyebrow / h2 的**盒子**横跨 x 120–1800，盒闸必然误报
  // （字在左边，盒子铺满整行），所以这里改成同一个盒子上的**文字墨迹闸**：
  // 遍历本页所有文本节点的 Range 矩形 + 所有 <text> 的包围盒，任何一块与
  // (1660,39)–(1883,120) 相交即失败 —— 语义 = 规范 §7「logo 盒内不得有任何别的字」，
  // 比盒闸更严也更准（连 SVG 文字都算）。
  const ink = await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    if (!s.querySelector(".chrome, .act, .qa")) return null;   // 没有 logo 的页不查
    const st = document.getElementById("deckStage").getBoundingClientRect();
    const f = st.width / 1920;
    const box = { l: st.left + 1660 * f, t: st.top + 39 * f, r: st.left + 1883 * f, b: st.top + 120 * f };
    const hit = (q) => !(q.right <= box.l || q.left >= box.r || q.bottom <= box.t || q.top >= box.b);
    const out = [];
    const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    for (let t = w.nextNode(); t; t = w.nextNode()) {
      if (!t.nodeValue || !t.nodeValue.trim()) continue;
      const rg = document.createRange(); rg.selectNodeContents(t);
      for (const q of rg.getClientRects()) if (q.width && q.height && hit(q)) out.push(t.nodeValue.trim().slice(0, 24));
    }
    s.querySelectorAll("text").forEach((e) => {
      const q = e.getBoundingClientRect();
      if (q.width && q.height && hit(q)) out.push("<text>" + (e.textContent || "").trim().slice(0, 20));
    });
    return out.slice(0, 3);
  });
  if (ink) { logoProbed++; if (ink.length) logoInk.push({ slide: i + 1, ink }); }
}
chk(n === 46, `页数 = 46（实测 ${n}）`);
chk(overflow.length === 0, `逐页 step 推满后零溢出（溢出页 ${JSON.stringify(overflow)}）`);
chk(logoInk.length === 0 && logoProbed === 39,
    `logo 盒 (1660,39)–(1883,120) 内无文字墨迹（查了 ${logoProbed} 页 · 越界 ${JSON.stringify(logoInk)}）`);

// ── 2) 页型分布：L2 星空底 11 张（封面 + 4 章节 + 5 金句 + Q&A），正文页纯底 ──
const layout = await pg.evaluate(() => {
  const S = window.deck.slides;
  const l2 = S.map((s, i) => (s.classList.contains("l2") ? i + 1 : 0)).filter(Boolean);
  const bgOK = l2.every((k) => getComputedStyle(S[k - 1]).backgroundImage.includes("data:image/png"));
  const plain = S.filter((s) => !s.classList.contains("l2"))
    .every((s) => getComputedStyle(s).backgroundImage === "none");
  const chromeNo = S.map((s, i) => {
    const c = s.querySelector(".chrome");
    return c ? [i + 1, +c.lastElementChild.textContent.trim()] : null;
  }).filter(Boolean);
  return { l2, bgOK, plain, badNo: chromeNo.filter(([a, b2]) => a !== b2) };
});
chk(JSON.stringify(layout.l2) === JSON.stringify([1, 6, 12, 13, 21, 25, 26, 33, 36, 39, 46]),
    `L2 星空底 11 张 = 封面 / 4 章节 / 5 金句 / Q&A：${JSON.stringify(layout.l2)}`);
chk(layout.bgOK && layout.plain, `L2 页有星空图、正文页纯底（bgOK=${layout.bgOK} plain=${layout.plain}）`);
chk(layout.badNo.length === 0, `chrome 页码 = 页序，无重复无跳号（错位 ${JSON.stringify(layout.badNo)}）`);

// ── 3) 四张章节页（P6 / P13 / P26 / P39） ──────────────────────────────────
const acts = await pg.evaluate(() => [6, 13, 26, 39].map((k) => {
  const s = window.deck.slides[k - 1], a = s.querySelector(".act");
  const cur = a.querySelector(".rail .cur");
  const cs = getComputedStyle(cur, "::before").content.replace(/^["']|["']$/g, "");
  return {
    p: k,
    rects: a.querySelectorAll(".num svg rect").length,
    sr: (a.querySelector(".num .sr") || {}).textContent || "",
    cur: cs + cur.textContent,
    curColor: getComputedStyle(cur).color,
    en: a.querySelector(".en").textContent.trim(),
    cn: a.querySelector(".cn").textContent.trim(),
    logo: getComputedStyle(a, "::after").backgroundImage.includes("data:image/png"),
  };
}));
chk(acts.every((x) => x.rects > 20), `章节页像素号 .num svg rect > 20：${acts.map((x) => x.rects).join("/")}`);
chk(acts.every((x) => x.cur.startsWith("> ")), `章节页当前章以「> 」开头：${JSON.stringify(acts.map((x) => x.cur))}`);
chk(acts.every((x) => x.curColor === "rgb(127, 244, 255)"), `当前章 = 青 #7FF4FF：${acts.map((x) => x.curColor).join(" ")}`);
chk(acts.every((x) => /^PART [1-4] · .+/.test(x.en)), `章节页 .en 形如 PART n · XXX：${JSON.stringify(acts.map((x) => x.en))}`);
chk(acts.every((x) => /^PART [1-4]$/.test(x.sr)), `章节页保留可访问性 .sr：${JSON.stringify(acts.map((x) => x.sr))}`);
chk(acts.every((x) => x.logo), "章节页右上 logo 在位（.act::after）");

// ── 4) 四页案例留白（P15 / P22 / P31 / P32） ───────────────────────────────
const CASE_KW = /96\.5|2,475|3\.08|三十天|Hugging Face|刹车|越权/;
const phs = await pg.evaluate(() => [15, 22, 31, 32].map((k) => {
  const s = window.deck.slides[k - 1];
  return {
    p: k,
    box: s.querySelectorAll(".ph-box").length,
    eb: s.querySelector(".eyebrow").textContent.trim(),
    crumb: s.querySelector(".chrome span").textContent.trim(),
    txt: s.textContent.replace(/\s+/g, " ").trim(),
  };
}));
chk(phs.every((x) => x.box === 5), `留白页 .ph-box = 5：${phs.map((x) => x.box).join("/")}`);
chk(phs.every((x) => x.eb.includes("待定")), `留白页 eyebrow 含「待定」：${JSON.stringify(phs.map((x) => x.eb))}`);
chk(phs.every((x) => x.crumb.includes("CASE")), `留白页 chrome 面包屑照母稿保留：${JSON.stringify(phs.map((x) => x.crumb))}`);
chk(phs.every((x) => !CASE_KW.test(x.txt)),
    `留白页无母稿案例关键词（残留 ${JSON.stringify(phs.filter((x) => CASE_KW.test(x.txt)).map((x) => x.p))}）`);

// ── 5) 一页带走（新 P44） ─────────────────────────────────────────────────
const take = await pg.evaluate(() => {
  const s = window.deck.slides[43];
  return {
    who: [...s.querySelectorAll(".take .who")].map((e) => e.textContent.trim()),
    em: [...s.querySelectorAll(".take .say em")].map((e) => e.textContent.trim()),
    ttl: [...s.querySelectorAll(".fig svg text.ttl")].map((e) => e.textContent.trim()),
    eb: s.querySelector(".eyebrow").textContent.trim(),
    no: s.querySelector(".chrome").lastElementChild.textContent.trim(),
  };
});
chk(JSON.stringify(take.who) === JSON.stringify(["开发者", "客户", "伙伴", "自己"]),
    `一页带走 .who = 开发者/客户/伙伴/自己：${JSON.stringify(take.who)}`);
chk(JSON.stringify(take.ttl) === JSON.stringify(["评测", "结果", "那一格", "放权"]),
    `一页带走 svg ttl = 评测/结果/那一格/放权：${JSON.stringify(take.ttl)}`);
chk(JSON.stringify(take.em) === JSON.stringify(["一套能跑通的评测", "一个岗位的结果", "同一把尺子上的那一格", "我敢不敢放权"]),
    `一页带走四句落点：${JSON.stringify(take.em)}`);
chk(take.eb.includes("从外到内") && take.no === "44", `一页带走 eyebrow / 页码 44：${take.eb} # ${take.no}`);

// ── 6) P2 主场开场 ───────────────────────────────────────────────────────
const p2 = await pg.evaluate(() => {
  const s = window.deck.slides[1];
  return { h2: s.querySelector("h2").textContent.trim(), eb: s.querySelector(".eyebrow").textContent.trim(),
           txt: s.textContent.replace(/\s+/g, " ") };
});
chk(p2.h2 === "交出去的东西，一年比一年重", `P2 h2 = 交出去的东西，一年比一年重（实测「${p2.h2}」）`);
chk(p2.eb.includes("主场 · 从 RTC 到对话式 AI"), `P2 eyebrow = 主场 · 从 RTC 到对话式 AI（实测「${p2.eb}」）`);
chk(["Realtime API · 全球首批合作伙伴", "引擎 1.0 · R1 GA", "Call Agent 全球版"].every((k) => p2.txt.includes(k)),
    "P2 三个节点口径与 /convoai-info 时间轴同源");
chk(!/第三次|首发|独家/.test(p2.txt), "P2 无「第三次 / 首发 / 独家」");

// ── 7) P1 封面 ───────────────────────────────────────────────────────────
const p1 = await pg.evaluate(() => {
  const s = window.deck.slides[0];
  const g = (q) => (s.querySelector(q) || {}).textContent || "";
  return {
    speaker: g(".ic-speaker").trim(), kicker: g(".ic-kicker").trim(),
    date: g(".ic-date").trim(), title: g(".ic-title").replace(/\s+/g, ""),
    spColor: getComputedStyle(s.querySelector(".ic-speaker")).color,
    logo: getComputedStyle(s.querySelector(".ic-logo")).backgroundImage.includes("data:image/png"),
    px: getComputedStyle(s.querySelector(".ic-px")).boxShadow,
  };
});
chk(p1.speaker === "姚光华 Colin｜声网 · AI 产品线负责人", `P1 讲者行（实测「${p1.speaker}」）`);
chk(p1.kicker.startsWith(">"), `P1 kicker 以 > 开头（实测「${p1.kicker}」）`);
chk(p1.spColor === "rgb(150, 255, 157)", `P1 讲者行 = 绿 #96FF9D（实测 ${p1.spColor}）`);
chk(p1.logo && /rgb\(127, 244, 255\)/.test(p1.px) && /rgb\(0, 70, 96\)/.test(p1.px),
    "P1 右中 logo + 四色像素块在位");
chk(p1.date.includes("2026.10.23") && p1.title.includes("双向奔赴·共事"), `P1 日期 / 标题：${p1.date}`);

// ── 8) Q&A 尾卡（P46） ───────────────────────────────────────────────────
const qa = await pg.evaluate(() => {
  const s = window.deck.slides[45];
  return {
    big: s.querySelector(".qa-big").textContent.trim(),
    bigColor: getComputedStyle(s.querySelector(".qa-big")).color,
    line: s.querySelector(".qa-line").textContent.trim(),
    me: s.querySelector(".qa-me").textContent.trim(),
    logo: getComputedStyle(s.querySelector(".qa"), "::after").backgroundImage.includes("data:image/png"),
  };
});
chk(qa.big === "Q&A", `尾卡 .qa-big = Q&A（实测「${qa.big}」）`);
chk(qa.bigColor === "rgb(150, 255, 157)" && qa.logo, `尾卡 Q&A 绿 + 页眉 logo（${qa.bigColor}）`);
chk(qa.line.startsWith(">") && qa.me.includes("colinyao.com"), `尾卡引导句 / 署名：${qa.line} / ${qa.me}`);

// ── 9) 计算样式抽检 ──────────────────────────────────────────────────────
const cs = await pg.evaluate(() => {
  const eb = document.querySelector(".eyebrow");
  const big = document.querySelector(".fig svg text.big");
  const mega = document.querySelector(".mega .num");
  return {
    ebColor: getComputedStyle(eb).color,
    ebBefore: getComputedStyle(eb, "::before").content.replace(/^["']|["']$/g, ""),
    ebBar: getComputedStyle(eb).backgroundImage,
    bigFill: big ? getComputedStyle(big).fill : null,
    megaColor: mega ? getComputedStyle(mega).color : "(本版无 .mega 页：母稿唯一一张 .mega 是 P15，已换成案例留白页)",
    slideBg: getComputedStyle(document.querySelector(".slide")).backgroundColor,
    amber: getComputedStyle(document.documentElement).getPropertyValue("--amber").trim(),
    coral: getComputedStyle(document.documentElement).getPropertyValue("--coral").trim(),
    fcn: getComputedStyle(document.querySelector(".slide")).fontFamily,
  };
});
chk(cs.ebColor === "rgb(178, 155, 255)", `.eyebrow 色 = 薰衣草 rgb(178,155,255)（实测 ${cs.ebColor}）`);
chk(cs.ebBefore === ">", `.eyebrow::before = 「>」（实测「${cs.ebBefore}」）`);
chk(cs.ebBar.includes("rgb(92, 34, 165)"), `.eyebrow 下深紫短条 #5C22A5（实测 ${cs.ebBar.slice(0, 60)}）`);
chk(cs.bigFill === "rgb(150, 255, 157)", `.fig .big fill = 绿 rgb(150,255,157)（实测 ${cs.bigFill}）`);
chk(cs.slideBg === "rgb(8, 12, 20)", `.slide 背景 = rgb(8,12,20)（实测 ${cs.slideBg}）`);
chk(cs.amber === "#96FF9D" && cs.coral === "#7FF4FF", `--amber/--coral = 绿/青（${cs.amber} / ${cs.coral}）`);
console.log(`  · .mega .num：${cs.megaColor}`);
chk(/Source Han Sans CN/.test(cs.fcn) && !/PuHuiTi/.test(cs.fcn), `.slide 字体栈 = 思源黑体（${cs.fcn.slice(0, 72)}…）`);

// ── 10) P3 录音按键行为（照 qa-confv2 §2 / §4） ──────────────────────────
await pg.evaluate(() => window.deck.go(2));
await pg.waitForTimeout(300);
await pg.keyboard.press("ArrowRight");
await pg.waitForTimeout(600);
const a1 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[2].querySelector("[data-dm]");
  return { i: d.i, playing: !!x && !x.paused, ind: d.slides[2].classList.contains("dm-playing") };
});
await pg.keyboard.press("ArrowRight");
await pg.waitForTimeout(400);
const a2 = await pg.evaluate(() => {
  const d = window.deck, x = d.slides[2].querySelector("[data-dm]");
  return { i: d.i, paused: !!x && x.paused };
});
chk(a1.i === 2 && a1.playing && a1.ind, `P3 第一按播放 ${JSON.stringify(a1)}`);
chk(a2.i === 3 && a2.paused, `P3 第二按停 + 翻页 ${JSON.stringify(a2)}`);
await pg.evaluate(() => window.deck.go(2));
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(500);
const m1 = await pg.evaluate(() => !window.deck.slides[2].querySelector("[data-dm]").paused);
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(200);
const m2 = await pg.evaluate(() => ({
  stopped: window.deck.slides[2].querySelector("[data-dm]").paused, still: window.deck.i }));
chk(m1 && m2.stopped && m2.still === 2, `M 键播/停不翻页 ${JSON.stringify({ m1, ...m2 })}`);

// ── 11) 反向闸 ───────────────────────────────────────────────────────────
const html = await pg.evaluate(() => document.documentElement.outerHTML);
const CONF_HEX = ["#9333EA", "#A855F7", "#C084FC", "#FFC000", "#7E22CE", "#B45309"];
chk(!/three|WebGL|<canvas/i.test(html), "无 three / WebGL / <canvas");
chk(!html.includes("image/jpeg") && !html.includes("image/webp"),
    `无 jpeg / webp（母稿封面照 + 金句底 + 门图全撤）`);
chk(CONF_HEX.every((c) => !html.includes(c)), `六个 conf 硬编码色一个不留（残留 ${CONF_HEX.filter((c) => html.includes(c))}）`);
chk(!/单向门|双向门|人人都是产品经理|AI 产品大会|Alibaba PuHuiTi|普惠体/.test(html),
    "conf 文案 / 普惠体残留清零");
chk(html.includes('name="robots" content="noindex, nofollow"'), "noindex meta 在位");
const refs = await pg.evaluate(() => {
  const out = new Set();
  document.querySelectorAll("[src],[href]").forEach((e) => {
    const u = e.getAttribute("src") || e.getAttribute("href");
    if (u && u.startsWith("/")) out.add(u);
  });
  (document.documentElement.outerHTML.match(/url\(['"]?(\/[^'")]+)/g) || []).forEach((m) => out.add(m.replace(/^url\(['"]?/, "")));
  return [...out].sort();
});
chk(JSON.stringify(refs) === JSON.stringify(["/fonts/JetBrainsMono-400.woff2", "/fonts/JetBrainsMono-500.woff2", "/media/cowork/p3-call.mp3"]),
    `站内引用只此三处：${JSON.stringify(refs)}`);
const steps = await pg.evaluate(() => [...document.querySelectorAll("[data-step]")].length);
console.log(`  · data-step 元素数：${steps}`);
chk(errs.length === 0, `pageerror = 0（${JSON.stringify(errs.slice(0, 3))}）`);

console.log(fail === 0 ? `\n全部通过（${n} 页）` : `\n失败 ${fail} 项`);
await b.close();
process.exit(fail ? 1 : 0);
