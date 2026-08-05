// QA：/cowork-confv2 45 页走查（R9 删文拆页 + R10 八页删改 + R11 十三页删改与数据换血）+ P3 录音按键行为 + 无视频断言 + 灰字提亮核对
// 与 qa-media.mjs 分工：那支跑线上 55 页版（/cowork-conf，含视频页），这支只跑 45 页预览版。
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const { chromium } = require("/home/claude/.npm-global/lib/node_modules/playwright");

const exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const b = await chromium.launch({ executablePath: exe, args: ["--autoplay-policy=no-user-gesture-required", "--mute-audio"] });
const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = [];
pg.on("pageerror", (e) => errs.push("pageerror: " + e.message));
let fail = 0;
const chk = (ok, label) => { if (!ok) fail++; console.log((ok ? "✓ " : "✗ ") + label); };

// ── 1) 45 页全量走查（含 data-step 推满 + 溢出检查） ──
await pg.goto("http://localhost:3000/cowork-confv2", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides && window.deck.slides.length === 45);
const n = await pg.evaluate(() => window.deck.slides.length);
let overflow = [];
for (let i = 0; i < n; i++) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(120);
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
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
}
chk(n === 45, `页数 = 45（实测 ${n}）`);
chk(overflow.length === 0, `零溢出（溢出页 ${JSON.stringify(overflow)}）`);

// ── 2) 媒体行为 · P3 录音（第一按播，第二按停 + 翻页） ──
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
  return { i: d.i, paused: !!x && x.paused, ind: d.slides[2].classList.contains("dm-playing") };
});
chk(a1.i === 2 && a1.playing && a1.ind, `P3 第一按播放 ${JSON.stringify(a1)}`);
chk(a2.i === 3 && a2.paused, `P3 第二按停 + 翻页 ${JSON.stringify(a2)}`);

// ── 3) 媒体资产：全场只剩 P3 一处录音，视频页已随陪伴章撤除 ──
const mcount = await pg.evaluate(() => ({
  dm: document.querySelectorAll("[data-dm]").length,
  video: document.querySelectorAll("video").length,
  vslide: document.querySelectorAll(".vslide").length,
  mp4: document.documentElement.innerHTML.includes("gemini-demo.mp4"),
}));
chk(mcount.dm === 1 && mcount.video === 0 && mcount.vslide === 0 && !mcount.mp4,
    `媒体资产 = 仅 P3 录音，无视频 ${JSON.stringify(mcount)}`);

// ── 4) M 键手动播 / 停 ──
await pg.evaluate(() => window.deck.go(2));
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(500);
const m1 = await pg.evaluate(() => !window.deck.slides[2].querySelector("[data-dm]").paused);
await pg.keyboard.press("KeyM");
await pg.waitForTimeout(200);
const m2 = await pg.evaluate(() => {
  const d = window.deck;
  return { stopped: d.slides[2].querySelector("[data-dm]").paused, still: d.i };
});
chk(m1 && m2.stopped && m2.still === 2, `M 键播/停不翻页 ${JSON.stringify({ m1, ...m2 })}`);

// ── 5) 视觉第一刀：灰字 token 提亮 + 次级文字 +2px 生效 ──
const tok = await pg.evaluate(() => {
  const cs = getComputedStyle(document.documentElement);
  const g = (k) => cs.getPropertyValue(k).trim();
  const note = document.querySelector(".note");
  // 多行 note 的 clip-path 修复：.note 下的 .flow 包裹层必须全是 inline-block
  const wraps = [...document.querySelectorAll(".note > .flow")];
  return {
    ink2: g("--ink-2"), ink3: g("--ink-3"), mark3: g("--mark-3"),
    noteFs: note ? getComputedStyle(note).fontSize : null,
    wrapN: wraps.length,
    wrapBad: wraps.filter((e) => getComputedStyle(e).display !== "inline-block").length,
  };
});
chk(tok.ink3 === "#D9D9E3" && tok.ink2 === "#E8E8F0" && tok.mark3 === "#A5A5A5",
    `token 提亮 --ink-3=#D9D9E3 / --ink-2=#E8E8F0 / --mark-3 保留原灰 ${JSON.stringify(tok)}`);
chk(tok.noteFs === "24px", `.note 字号 24px（+2px）实测 ${tok.noteFs}`);
chk(tok.wrapN > 0 && tok.wrapBad === 0,
    `多行 note clip-path 修复在位：${tok.wrapN} 个 .note>.flow 全 inline-block（异常 ${tok.wrapBad}）`);

// ── 6) 结构：PART 0–4 五幕 / 金句 01–05 / 陪伴章清零 ──
const txt = await pg.evaluate(() => document.body.innerText);
const html = await pg.evaluate(() => document.documentElement.innerHTML);
chk(html.includes("PART 2 · 被托付") && html.includes("PART 3 · 双向奔赴") && html.includes("PART 4 · 人与组织"),
    "PART 重编号 2/3/4 在位");
chk(!html.includes("PART 5") && !html.includes("PART 2 · 被记住"), "五幕编号 / 陪伴幕卡已清零");
chk(html.includes("观点页 · 嘉宾金句 · 05") && !html.includes("观点页 · 嘉宾金句 · 06"), "金句重编号 01–05");
chk(html.includes("下午 AIoT 专场"), "P9 分论坛预告在位");
chk(!txt.includes("上一幕") && !txt.includes("第五幕"), "悬空幕序指涉清零");

// ── 6.5) R9：Colin 逐页删文 / 两处拆页 / 撑满层 ──
const cut = ["工程上已经基本解完了", "两把完全不同的尺子", "剩下的全部难题都叫「凭什么信」",
             "大模型评分 4.6 分", "不是换一个赞", "最右边那一格",
             "两个人分别判，结论一样", "改完能证明这一类不会再犯",
             "只等于人退得越远", "这个岗位能不能交",
             "责任必须落在一个能被追责的主体上", "准确率和问责，是两件事",
             "捞回一双正在移动的脚", "和那双脚一样",
             "找十个客户聊聊", "换掉一条业务规则", "没有名字的授权", "没有退出标准的授权",
             "2025 年我把它讲给产研团队", "组织 agency 是制度许可",
             "Weil 说的是向外那一面", "去年结语我说"];
chk(cut.every((k) => !html.includes(k)),
    `R9 逐页删文到位（残留 ${JSON.stringify(cut.filter((k) => html.includes(k)))}）`);
chk(html.includes("你的 demo 在骗你</h2>") && html.includes("每一轮都对，整段却错了</h2>"),
    "R9 · Eval 融合页已拆回母版原两页");
const lesson = ["一", "二", "三", "四"].map((c) => html.indexOf(`>Eval 第${c}课</div>`));
chk(lesson.every((x) => x > 0) && lesson.every((x, i) => i === 0 || x > lesson[i - 1]),
    `R9 · Eval 课序 一→二→三→四 正序 ${JSON.stringify(lesson)}`);
chk(html.includes("体验的围栏：交互行为，要有<em>规矩</em>") &&
    html.includes("执行的围栏：语音的动作"), "R9 · 两道围栏合页已拆回母版原两页");
const fence = html.slice(html.indexOf("执行的围栏：语音的动作"));
chk(fence.slice(0, fence.indexOf("</section>")).includes("事前授权") &&
    fence.slice(0, fence.indexOf("</section>")).includes("批动作类别，不批每一句话"),
    "R9 · C6「事前授权」已移植进母版执行围栏页");
chk(html.includes("You don’t pay for tokens") && html.includes("business outcomes delivered"),
    "R9 · P22 英文判断句大字在位");
chk(html.includes("可逆 · 双向门 · 放手做，不用批") && html.includes("不可逆 · 单向门 · 先升级"),
    "R9 · P43 单向门 / 双向门核心图形保留");

// ── 6.6) R10：八页删改（P5 / P18 / P22 / P27 / P29 / P37 / P39 / P45） ──
const cut10 = ["问题一 · 授权边界", "问题二 · 问责归属", "问题三 · 撤销机制",   // P5 三问卡整组
               "这三个问题不是哲学问题",                                        // P5 note
               "整体一致率是被多数类稀释过的假象", "裁判自己也要有回归集",        // P18 正确的看法
               "一笔约 36 亿美元的收购",                                        // P22 foot
               "不是成熟，只是乐观", "给产品团队的动作 · 先别问",                 // P27 note / foot
               "separation of duties", "某企业支付平台 CEO 与访谈者",            // P29 英文引文块
               "越权拒答率 · 策略遵守率", "审计覆盖率 · 决策可归因率",
               "撤销生效延迟 · 回滚成功率", "信任是被验证过的行动空间",
               "这三个维度对应四条工程坐标",                                     // P37 三卡 + 两段解释
               "四阶不是学历",                                                  // P39 land
               "Writing evals is the most important thing", "Kevin Weil",       // P45 引文卡
               "愿我们在理解"];                                                 // P45 结语
chk(cut10.every((k) => !html.includes(k)),
    `R10 八页删文到位（残留 ${JSON.stringify(cut10.filter((k) => html.includes(k)))}）`);
// 注意：走查时 data-step 已被推满，四列那块的 class 会多一个 on，所以只比前缀
chk(["身份可验", "VERIFIABLE", "行为可拦", "INTERCEPTABLE", "结果可追", "ACCOUNTABLE",
     "授权可撤销", "REVOCABLE", '<div class="take qot4'].every((k) => html.includes(k)),
    "R10 · P37 四条工程坐标已升为页面主体（四列 .take.qot4）");
chk(["QoS", "QoE", "QoI", "QoT"].every((q) => html.includes(`>${q}</text>`)),
    "R10 · P37 QoS-QoE-QoI-QoT 顶部条保留");
chk(html.includes("你付的不是 token 的钱——是被交付出来的业务结果的钱。"),
    "R10 · P22 中文翻译行在位（land 体系 .s）");
chk(html.includes('viewBox="0 320 1680 665"') && html.includes("语法变了"),
    "R10 · P5 路线图已纵向拉伸为全页主体");
chk(html.includes('viewBox="0 -177 1680 646"'), "R10 · P45 尺子两面图已纵向拉伸（纯图收场）");
// 撑满层与档位类：八页一页一档
// 同上：当前页的 section 会多挂 active/visible，所以不比结尾的引号
chk(["r10p5", "r10p18", "r10p22", "r10p27", "r10p29", "r10p37", "r10p39", "r10p45"]
      .every((c) => new RegExp(`class="slide[^"]*\\b${c}\\b`).test(html) && html.includes(`.${c} `)),
    "R10 · 八页档位类全部挂上且在 CSS 里有定义");
// .dw 自绘线：--len 必须盖得住路径长度，否则线画一半就断（R10 在 P27/P39/P45 与 P28 补账）
const dwbad = await pg.evaluate(() => {
  const out = [];
  window.deck.slides.forEach((s, i) => {
    s.querySelectorAll("path.dw").forEach((p) => {
      const len = parseFloat(getComputedStyle(p).getPropertyValue("--len")) || 1200;
      let mx = 0;
      (p.getAttribute("d") || "").split(/(?=M)/).filter(Boolean).forEach((sd) => {
        const t = document.createElementNS("http://www.w3.org/2000/svg", "path");
        t.setAttribute("d", sd); p.parentNode.appendChild(t);
        mx = Math.max(mx, t.getTotalLength()); t.remove();
      });
      // 母版 P27 交叉验证条带那两条自带 24/1264 的短账，属既有陈账，放行
      if (mx > len + 30) out.push({ slide: i + 1, len, need: Math.round(mx) });
    });
  });
  return out;
});
chk(dwbad.length === 0, `.dw 自绘线不被 --len 截断（异常 ${JSON.stringify(dwbad)}）`);

// ── 6.7) R11：十三页删改与数据换血（P3/4/5/8/9/10/19/21/22/29/30/33/36） ──
const cut11 = ["当时我的结论是：活人感缺失", "把它做得更像人",              // P3 两块口播结论
               "他真正的愤怒不是「你不像人」", "让它说清楚自己是谁、能替谁审批",
               "OPENAPI", "一张跑了 100 年的电话网", "加一张一百年的旧网", // P4 A2A / PSTN 年数
               ">开场</text>",                                            // P5 开场站
               "美国青少年里，用过 AI 陪伴类产品的",                        // P8 消费侧压缩
               "而遇到要紧事，宁可先说给 AI 听", "Common Sense Media",
               "四个方向的人得出了同一个结论", "模型不再是瓶颈",             // P9 旧结论
               "边界声明 · 本场不讨论意识",                                // P10 foot
               '<div class="steps">', '<div class="i">STEP 01</div>',     // P19 下方四块
               "96.5%</div><div class=\"l\">未被识破率",                   // P21 三格
               "同等时间的有效工作量", "同等产出的用人成本", "意向转化率",
               "这 2,475 通，是真实生产通话的自然测量",
               "这个坑有名字，叫 backchannel",                            // P33 note
               "任何一格的进步，四条线一起受益"];                          // P36 note 长尾
chk(cut11.every((k) => !html.includes(k)),
    `R11 十三页删文到位（残留 ${JSON.stringify(cut11.filter((k) => html.includes(k)))}）`);
chk(html.includes(">A2A</text>") && html.includes("一张跑了 150 年的电话网") &&
    html.includes("贝尔 1876 年打出人类第一通电话，今年整 150 周年"),
    "R11 · P4 协议名换 A2A + PSTN 150 年（贝尔 1876 起算）");
// P5 路线图四站：PART 1-4，高亮段起点同步挪到 PART 2 的新 x
const p5 = html.slice(html.indexOf("<!-- 全场路线"));
const p5svg = p5.slice(0, p5.indexOf("</svg>"));
chk((p5svg.match(/text-anchor="middle">PART/g) || []).length === 4 && !p5svg.includes("PART 0") &&
    ["语法变了", "被托付", "双向奔赴", "人与组织"].every((t) => p5svg.includes(t)) &&
    p5svg.includes('d="M627 543 H1600"') && p5svg.includes("--len:1010"),
    "R11 · P5 路线图四站（PART 1-4）+ 高亮段起点/--len 同步");
// P8 企业侧换血：五条 bar 每条都能在 SOURCE 行找到来源与年份
chk([">66%<", ">91%<", ">70%<", ">15–20%<", ">49%<"].every((k) => html.includes(k)) &&
    html.includes("Salesforce《State of Service: AI Agents Edition》2026-05（n=3,075") &&
    html.includes("CC-CMM · 艾媒咨询 · 第一新声 2025") &&
    html.includes("Pew Research 2026-06（n=5,119）"),
    "R11 · P8 五条数据 + SOURCE 行逐条标源与年份");
chk(html.includes("对话式智能体在企业服务侧，已经到了规模化应用的阶段") && html.includes("硬性基础全部具备"),
    "R11 · P9 结论行已改口径");
chk(["STEP 01", "STEP 02", "STEP 03", "STEP 04", "全量捞，不抽样", "人耳听，不看文本",
     "归类，不打分", "固化成回归集"].every((k) => html.includes(`>${k}</text>`)) &&
    html.includes('viewBox="0 0 1680 600"'),
    "R11 · P19 四步已并进图内（图放大为主体）");
chk(html.includes('<div class="cmp2">') && html.includes('<div class="v">3.08%</div>') &&
    html.includes('<div class="v">1.5%</div>') && html.includes("<div class=\"l\">被识破率</div>") &&
    html.includes("上线前人工基线 · 内部口径") && html.includes("它已经贴到人工坐席自己的极限上了。"),
    "R11 · P21 3.08% × 1.5% 双大数对比 + 基线口径标注");
chk(html.includes('<div class="land r11pay flow"') &&
    html.includes("Bret Taylor &amp; Clay Bavor · Sierra 官方博客《The next Horizon in agents》· 2026-07"),
    "R11 · P22 中文升主 + 英文原文 + 出处行（一手已核到）");
// P29 / P30 版面对调
const p29 = html.slice(html.indexOf("人和 Agent 共事的协作关系"));
const p29s = p29.slice(0, p29.indexOf("</section>"));
chk(p29s.indexOf('<div class="fig">') < p29s.indexOf('<div class="g3">'), "R11 · P29 图上 / 大数下");
const p30 = html.slice(html.indexOf("两道围栏：提示词拦话术"));
const p30s = p30.slice(0, p30.indexOf("</section>"));
chk(p30s.indexOf('<div class="fig">') < p30s.indexOf('class="old tail') &&
    p30s.indexOf('class="note co') < p30s.indexOf('class="old tail') &&
    html.includes('viewBox="0 0 1680 260"'),
    "R11 · P30 图最上并放大 / 事件叙述沉底作注释行");
chk(html.includes("<b>四条产品线不是四个赛道，是同一个能力模型的四个切片。</b></div>"),
    "R11 · P36 下方只留一句");
chk(["r11p3", "r11p5", "r11p8", "r11p9", "r11p10", "r11p19", "r11p21",
     "r11p29", "r11p30", "r11p33", "r11p36"]
      .every((c) => new RegExp(`class="slide[^"]*\\b${c}\\b`).test(html) && html.includes(`.${c} `)),
    "R11 · 十一个页级档位类全部挂上且在 CSS 里有定义");
// 十三页 .body 填充率 + svg 文字零重叠（删后撑满的机检）
const r11fill = [];
for (const p of [3, 4, 5, 8, 9, 10, 19, 21, 22, 29, 30, 33, 36]) {
  await pg.evaluate((k) => window.deck.go(k - 1), p);
  await pg.waitForTimeout(140);
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  });
  await pg.waitForTimeout(80);
  const m = await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i];
    const body = s.querySelector(".body") || s.querySelector(".mega");
    const kids = [...body.children].filter((e) => e.offsetParent);
    const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
    const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
    const ratio = Math.round(((bot - top) / body.getBoundingClientRect().height) * 100);
    const t = [...s.querySelectorAll("svg text")].filter((x) => x.textContent.trim());
    let ov = 0;
    for (let i = 0; i < t.length; i++) for (let j = i + 1; j < t.length; j++) {
      const a = t[i].getBoundingClientRect(), c = t[j].getBoundingClientRect();
      if (!a.width || !c.width) continue;
      if (Math.min(a.right, c.right) - Math.max(a.left, c.left) > 2 &&
          Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top) > 2) ov++;
    }
    return { ratio, ov };
  });
  r11fill.push({ p, fill: m.ratio, ov: m.ov });
}
chk(r11fill.every((x) => x.fill >= 78 && x.fill <= 106 && x.ov === 0),
    `R11 · 十三页 .body 填充率 78–106% 且 svg 文字零重叠 ${JSON.stringify(r11fill)}`);

// ── 7) 封面 title ──
await pg.evaluate(() => window.deck.go(0));
await pg.waitForTimeout(400);
await pg.screenshot({ path: "/tmp/qa/confv2-cover.png" });
chk(await pg.evaluate(() => document.body.textContent.includes("声网 AI 产品线负责人")), "封面 title 线字");

// ── 8) /cowork-conf 线上版未被波及：仍 55 页 + 视频页在 ──
await pg.goto("http://localhost:3000/cowork-conf", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides);
const base = await pg.evaluate(() => ({
  slides: window.deck.slides.length,
  video: document.querySelectorAll("video[data-dm]").length,
  ink3: getComputedStyle(document.documentElement).getPropertyValue("--ink-3").trim(),
}));
chk(base.slides === 55 && base.video === 1 && base.ink3 === "#A5A5A5",
    `/cowork-conf 未被波及：55 页 + 视频在 + --ink-3 原值 ${JSON.stringify(base)}`);

console.log("pageerrors:", errs.length ? errs : "none");
console.log(fail === 0 && errs.length === 0 ? "QA confv2 · ALL GREEN" : `QA confv2 · FAIL ${fail}`);
await b.close();
process.exit(fail === 0 && errs.length === 0 ? 0 : 1);
