// QA：/cowork-confv2 46 页走查（R9 删文拆页 + R10 八页删改 + R11 十三页删改与数据换血 + R12 新页「钱的三次落点」）
//     + P3 录音按键行为 + 无视频断言 + 灰字提亮核对
// 与 qa-media.mjs 分工：那支跑线上 55 页版（/cowork-conf，含视频页），这支只跑 46 页预览版。
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

// ── 1) 46 页全量走查（含 data-step 推满 + 溢出检查） ──
await pg.goto("http://localhost:3000/cowork-confv2", { waitUntil: "networkidle" });
await pg.waitForFunction(() => window.deck && window.deck.slides && window.deck.slides.length === 46);
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
chk(n === 46, `页数 = 46（实测 ${n}）`);
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
               "愿我们在理解"];                                                 // P45 结语
// ⚠️ R13 起「Writing evals / Kevin Weil」不再列进 cut10：那句从终页撤走后放回了灵魂拷问页
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
               "同等时间的有效工作量", "同等产出的用人成本",
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
    p5svg.includes('d="M627 580 H1600"') && p5svg.includes("--len:1010"),
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
    html.includes('<div class="v">1.5%</div>') && html.includes("上线前人工基线 · 内部口径"),
    "R11 · P21 3.08% × 1.5% 双大数对比 + 基线口径标注（度量名/结论句由 R13 纠正）");
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
// ⚠️ R12 在 P6 幕卡后插了新页，R11 那十三页里 P7 起的页号一律 +1（3/4/5 不变）
for (const p of [3, 4, 5, 9, 10, 11, 20, 22, 23, 30, 31, 34, 37]) {
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

// ── 6.8) R12：PART 1 幕卡后新增一页「钱的三次落点」（45 → 46） ──
// 页序：P6 幕卡 → P7 新页（全图）→ P8 钱页（对话式内部分布）→ P9 采购已开动
const seq12 = await pg.evaluate(() => {
  const t = (i) => (window.deck.slides[i].textContent || "").replace(/\s+/g, " ");
  return { p6: t(5), p7: t(6), p8: t(7), p9: t(8) };
});
chk(seq12.p6.includes("语法变了") && seq12.p7.includes("钱的三次落点") &&
    seq12.p8.includes("这不是一个垂类") && seq12.p9.includes("预测还在打架"),
    "R12 · 三连页序：幕卡 → 新页全图 → 对话式内部分布 → 采购已开动");
// eyebrow 必须是 Colin 原话，逐字
chk(html.includes("产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走"),
    "R12 · 新页 eyebrow 用 Colin 原话（逐字）");
chk(html.includes("近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>"), "R12 · 新页 h2 在位");
// 三条线的名与数（R14 已把三条层带重做成双轴时间图，逐条图元账见 6.10）
chk([">基础模型</text>", ">AI 写代码</text>", ">对话式 AI</text>",
     ">$31.4B</text>", ">$88.9B</text>", ">$178B</text>",
     ">$1.6B</text>", ">$3.3B</text>",
     ">$2.1B</text>", ">≈$0.7B</text>", ">$2.2B+</text>"].every((k) => html.includes(k)),
    "R12 · 三条线的名与数全在");
const p7h = html.slice(html.search(/class="slide[^"]*\br12flow\b/));
const p7s = p7h.slice(0, p7h.indexOf("</section>"));
chk((p7s.match(/class="stroke-am pkt"/g) || []).length === 1, "R12 · 对话式那条走线光点在位");
// 大泛类两翼：消费声音侧 / 企业智能体侧各点一个代表名
chk(["ElevenLabs $500M @ $11B", "消费声音侧", "Sierra $950M @ $15B", "企业智能体侧"]
      .every((k) => p7s.includes(k)), "R12 · 对话式层两翼（ElevenLabs / Sierra）标注在位");
chk([...p7s.matchAll(/data-step="(\d+)"/g)].every((m) => +m[1] <= 2), "R12 · 新页 data-step ≤2");
chk(/class="slide[^"]*\br12flow\b/.test(html) && html.includes(".r12flow "),
    "R12 · 新页档位类挂上且在 CSS 里有定义");
// 衔接：现 P8（钱页）eyebrow 已换成承接句
chk(!html.includes("先看钱往哪儿去了") &&
    html.includes("钱到了对话式 AI，再往里看一层：它分给了谁"),
    "R12 · P8 钱页 eyebrow 已改为衔接句");
// 新页与衔接页填充率 + svg 文字零重叠 + 截图
const r12fill = [];
for (const p of [7, 8]) {
  await pg.evaluate((k) => window.deck.go(k - 1), p);
  await pg.waitForTimeout(160);
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  });
  await pg.waitForTimeout(2400);
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
  r12fill.push({ p, fill: m.ratio, ov: m.ov });
  await pg.screenshot({ path: p === 7 ? "/tmp/qa/r12-new.png" : "/tmp/qa/r12-p8.png" });
}
chk(r12fill.every((x) => x.fill >= 78 && x.fill <= 106 && x.ov === 0),
    `R12 · 新页与衔接页 .body 填充率 78–106% 且 svg 文字零重叠 ${JSON.stringify(r12fill)}`);

// ── 6.9) R13：七处内容修订（全部内容锚定取页，不信页码） ──
// 页号在 46 页版里现算：靠正文找 slide 下标，Colin 的反馈横跨 45/46 两版
const idxOf = async (needle) =>
  await pg.evaluate((n) => window.deck.slides.findIndex((s) => (s.textContent || "").includes(n)), needle);
const P = {
  bell: await idxOf("今年这段通话里，一个人都没有"),
  route: await idxOf("本场提要"),
  ask: await idxOf("亲手写过"),
  eval1: await idxOf("你的 demo 在骗你"),
  case2: await idxOf("一个 Agent 的入职三十天"),
  mqTaylor: await idxOf("One of the biggest fallacies in AI"),
  mqFence: await idxOf("围栏不是拦住它，"),
};
chk(Object.values(P).every((i) => i >= 0), `R13 · 七个目标页全部按内容找到 ${JSON.stringify(P)}`);
// 负向：被换下 / 被改写的六句必须查无此句
const cut13 = ["B 如 Boy", '<div class="l">被识破率</div>', "被投诉「不像人」基线",
               "通话结束前，被对方听出「这是 AI」的比例", "它已经贴到人工坐席自己的极限上了。",
               "一个能被计量的同事，", "计量不是为了管住它，是为了敢把事交给它。",
               "提示词只能拦住一些越权，", "架构的围栏，才是产品经理的护城河。",
               "你能拦住的，只有你先表示出来的那些东西。"];
chk(cut13.every((k) => !html.includes(k)),
    `R13 七处改写到位（残留 ${JSON.stringify(cut13.filter((k) => html.includes(k)))}）`);
// ① 贝尔第一通电话
const secOf = async (i) => await pg.evaluate((k) => window.deck.slides[k].outerHTML, i);
const sBell = await secOf(P.bell);
chk(sBell.includes("Mr. Watson — come here — I want to see you.") &&
    sBell.includes("贝尔 · 1876 · 人类第一通电话，今年整 150 年") &&
    sBell.includes("PSTN · 一张跑了 150 年的电话网") &&
    (sBell.match(/<div class="quote/g) || []).length === 2,
    "R13-① 贝尔原话 + 出处行挂在 PSTN/150 年那一页（左栏两条引文）");
// ② 路线图字号回调：站名 46 / PART 标 24 / 副题 25（实测计算值）
const route = await pg.evaluate((k) => {
  const s = window.deck.slides[k], g = (sel) => {
    const e = s.querySelector(sel);
    return e ? Math.round(parseFloat(getComputedStyle(e).fontSize)) : null;
  };
  const c = s.querySelector("circle.fill-am");
  return { txt: g("svg text.txt"), lbl: g("svg text.lbl"), sm: g("svg text.sm"),
           r: c ? +c.getAttribute("r") : null };
}, P.route);
chk(route.txt >= 44 && route.txt <= 48 && route.lbl >= 22 && route.lbl <= 26 &&
    route.sm >= 24 && route.sm <= 26 && route.r === 11,
    `R13-② 路线图回调到优雅档（站名 44–48 / PART 24 / 副题 24–26 / 圆点回收）${JSON.stringify(route)}`);
// ③ Weil 金句在拷问页、且是第二拍
const sAsk = await secOf(P.ask);
chk(sAsk.includes("Writing evals is the most important thing a PM can do in the AI era.") &&
    sAsk.includes("Kevin Weil · OpenAI 前 CPO") && sAsk.includes('data-step="1"') &&
    (html.match(/Writing evals is the most important thing/g) || []).length === 1,
    "R13-③ Weil 金句作 data-step=1 第二拍落在灵魂拷问页（全场仅此一处）");
// ④ 英语习惯拼读法：svg 与关联句两处
const sEv = await secOf(P.eval1);
chk(sEv.includes("A as in Apple · B as in Boy · 0086 · 一位一位念") &&
    sEv.includes("在「A as in Apple、0086」上"),
    "R13-④ A as in Apple · B as in Boy（svg + 关联句同步）");
// ⑤ 3.08% 表意纠正：同一把尺子 + Agent 条更长 + amber
const case2 = await pg.evaluate((k) => {
  const s = window.deck.slides[k];
  const cs = [...s.querySelectorAll(".cmp2 .c")].map((c) => ({
    v: c.querySelector(".v").textContent.trim(),
    l: c.querySelector(".l").textContent.trim(),
    w: c.querySelector(".bar i").getBoundingClientRect().width,
    bg: getComputedStyle(c.querySelector(".bar i")).backgroundColor,
  }));
  return { cs, land: (s.querySelector(".land") || {}).textContent || "" };
}, P.case2);
chk(case2.cs.length === 2 && case2.cs.every((c) => c.l === "意向转化率") &&
    case2.cs[0].v === "3.08%" && case2.cs[1].v === "1.5%" &&
    case2.cs[0].w > case2.cs[1].w * 1.8 && case2.cs[0].bg !== case2.cs[1].bg &&
    case2.land.includes("它已经把人工基线翻了一倍。") && case2.land.includes("不是在"),
    `R13-⑤ 两数同为意向转化率 + Agent 条更长/amber + 主句转向「强过人」${JSON.stringify(case2.cs.map((c) => [c.v, c.l, Math.round(c.w)]))}`);
chk(html.includes("上线前人工基线 · 内部口径"), "R13-⑤ 1.5% 的口径标注保留");
// ⑥ Bret Taylor perfect human 金句页
const sMq = await secOf(P.mqTaylor);
chk(sMq.includes("is people compare it with this perfect human") &&
    sMq.includes("that does not exist.") &&
    sMq.includes("AI 最大的谬误之一，是人们总把它跟一个并不存在的完美的人相比。") &&
    sMq.includes("Bret Taylor · Sierra CEO / OpenAI 董事长") &&
    sMq.includes("观点页 · 嘉宾金句 · 03"),
    "R13-⑥ 金句 03 换成 Bret Taylor 原句（英文主 + 中文译 + 署名行）");
// ⑦ 围栏 Part 点睛
const sFc = await secOf(P.mqFence);
chk(sFc.includes("是放出它。") && sFc.includes("观点页 · 嘉宾金句 · 04") &&
    sFc.includes("围出一条不用人扶的执行流——围栏有多硬，敢交给它的 OKR 就有多重。"),
    "R13-⑦ 围栏 Part 金句重写（一句主 + 一行小字）");
// 七页逐页截图 + 溢出/重叠复核（金句页无 .body，只查溢出）
const shots = { bell: P.bell, route: P.route, ask: P.ask, eval1: P.eval1,
                case2: P.case2, "mq-taylor": P.mqTaylor, "mq-fence": P.mqFence };
const r13bad = [];
for (const [name, i] of Object.entries(shots)) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(160);
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  });
  await pg.waitForTimeout(2200);
  const m = await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i], r = s.getBoundingClientRect();
    let out = 0;
    s.querySelectorAll("div,p,h1,h2,h3,span,i,li").forEach((el) => {
      if (!el.offsetParent) return;
      const b = el.getBoundingClientRect();
      if (b.width && b.height && (b.bottom > r.bottom + 4 || b.right > r.right + 4)) out++;
    });
    const t = [...s.querySelectorAll("svg text")].filter((x) => x.textContent.trim());
    let ov = 0;
    for (let i = 0; i < t.length; i++) for (let j = i + 1; j < t.length; j++) {
      const a = t[i].getBoundingClientRect(), c = t[j].getBoundingClientRect();
      if (!a.width || !c.width) continue;
      if (Math.min(a.right, c.right) - Math.max(a.left, c.left) > 2 &&
          Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top) > 2) ov++;
    }
    return { out, ov };
  });
  if (m.out || m.ov) r13bad.push({ name, ...m });
  await pg.screenshot({ path: `/tmp/qa/r13-p${name}.png` });
}
chk(r13bad.length === 0, `R13 · 七页零溢出零 svg 文字重叠（异常 ${JSON.stringify(r13bad)}）`);
chk(["r13bell", "r13p5", "r13ask", "r13case", "r13mq", "r13fence"]
      .every((c) => new RegExp(`class="slide[^"]*\\b${c}\\b`).test(html) && html.includes(`.${c} `)),
    "R13 · 四个页级档位类全部挂上且在 CSS 里有定义");

// ── 6.10) R14：① P2 舞台 → 讲台 ② 钱流向页重做成双轴时间图 + 来源瘦身 ──
const P14 = {
  p2: await idxOf("第三次，站上同一个讲台"),
  money: await idxOf("近三年，钱的三次落点"),
};
chk(Object.values(P14).every((i) => i >= 0), `R14 · 两个目标页按内容找到 ${JSON.stringify(P14)}`);
// ① 讲台在 / 舞台零（正文范围；母版 CSS 注释里的「固定舞台」不算页内容）
const s14p2 = await secOf(P14.p2);
chk(s14p2.includes("第三次，站上同一个讲台") && s14p2.includes("回到讲台") && !s14p2.includes("舞台"),
    "R14-① P2 讲台在、全页零「舞台」");
const stageLeft = await pg.evaluate(() =>
  window.deck.slides.filter((s) => (s.textContent || "").includes("舞台")).length);
chk(stageLeft === 0 && !html.includes("第三次，站上同一个舞台"),
    `R14-① 全场 46 页正文零「舞台」（残留 ${stageLeft} 页）`);
// ② 双轴时间图：骨架 / 三条线 / 名牌 / 两翼 / 小注 / 面积 / 光点
const pmh = html.slice(html.search(/class="slide[^"]*\br14money\b/));
const pms = pmh.slice(0, pmh.indexOf("</section>"));
chk(pms.includes('d="M230 120 V470 M1200 120 V470"') &&
    (pms.match(/class="gd"/g) || []).length === 1 &&
    (pms.match(/class="axb"/g) || []).length === 1 &&
    pms.includes(">基础模型 $B</text>") && pms.includes(">Coding / 对话式 $B</text>"),
    "R14-② 双轴骨架：左右两轴 + 一套共用网格 + 基线 + 两个 mono 轴标");
chk(['x="212" y="127" text-anchor="end">200<', 'x="212" y="477" text-anchor="end">0<',
     'x="1218" y="127">4<', 'x="1218" y="477">0<'].every((k) => pms.includes(k)),
    "R14-② 左轴 0–200 / 右轴 0–4 刻度在位（两套落在同五条网格线上）");
chk(['class="lbl yr" x="300" y="508"', 'class="lbl yr" x="720" y="508"',
     'class="lbl yr" x="1140" y="508"', '>至今</text>',
     "左右两轴量级不同 · 左轴 0–200，右轴 0–4（$B）"].every((k) => pms.includes(k)),
    "R14-② X 轴三刻度 + 2026「至今」+ 双轴量级防误读小注");
chk((pms.match(/class="ln fnd dw"/g) || []).length === 1 &&
    (pms.match(/class="ln cod dw"/g) || []).length === 1 &&
    (pms.match(/class="ln cnv dw"/g) || []).length === 1 &&
    (pms.match(/class="stroke-am pkt"/g) || []).length === 1,
    "R14-② 三条曲线各一条 + 对话式那条挂走线光点");
chk(pms.includes('class="ln cod dw" style="--len:490;--i:6" d="M300 330 C 440 322 580 210 720 181"') &&
    !pms.includes("stroke-dasharray") && !pms.includes("$2B ARR") &&
    pms.includes("2026 转向收入兑现 · Cursor ARR $2B"),
    "R14-② Coding 线止于 2025、无虚线补第三点，ARR 只作末端小注（不上融资轴）");
chk(pms.includes('fill="url(#r14conv)"') && pms.includes('id="r14conv"') &&
    html.includes(".r14money #r14conv .g0{stop-color:var(--amber);stop-opacity:.22;}"),
    "R14-② 对话式曲线下的 amber 低透明度渐变面积在位");
chk(['x="1262" y="150">基础模型</text>', 'x="1262" y="196">$178B</text>',
     'x="750" y="154">AI 写代码</text>', 'x="891" y="154">$3.3B</text>',
     'x="1262" y="270">对话式 AI</text>', 'x="1262" y="316">$2.2B+</text>'].every((k) => pms.includes(k)) &&
    (pms.match(/class="sm wing pop"/g) || []).length === 2 &&
    (pms.match(/class="lead (fnd|cnv) pop"/g) || []).length === 2,
    "R14-② 三条曲线各自终点挂名牌（两条带引线）+ 2026 点旁两翼小标");
chk((pms.match(/class="txt val/g) || []).length === 5,
    "R14-② 值标只在起点/拐点（终点走名牌），恰好五个 —— 不是每点都挂数字");
chk([">FOUNDATION MODELS</text>", ">CODING</text>", ">CONVERSATIONAL AI</text>",
     'class="stroke dw"', 'class="stroke-am dw"', ">$2B ARR</text>", ">≈$2.2B</text>",
     "同一层的两翼"].every((k) => !pms.includes(k)),
    "R14-② 三条层带的旧图元清零");
// foot 瘦身成一行；旧长口径全文撤下（已移入设计文档 R14 段留档）
chk(pms.includes('<div class="foot flow rev" style="--i:9">Source · Crunchbase · ' +
                 "CB Insights《State of AI 2025》· TechCrunch · Bloomberg · CNBC</div>"),
    "R14-② 新 foot 一行在位");
chk(["New Market Pitch 2026-07", "PYMNTS 2025-06", "SiliconANGLE 2026-05", "Newcomer 2026-02",
     "Crunchbase 2026-04", "CB Insights《State of AI 2025》2026-01",
     "本页自算，不是全类别口径", "带宽为量级示意，非等比", "Cartesia $100M", "Parloa $350M"]
      .every((k) => !html.includes(k)), "R14-② 旧的长口径 foot 全场清零");
chk(["产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走",
     "近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>",
     "这笔钱在这一层内部又分给了谁——下一页拆开看。"].every((k) => pms.includes(k)),
    "R14-② eyebrow / h2 / note 三样原样保留");
// 两页逐页截图 + 填充率 / 溢出 / svg 文字重叠复核
const r14 = [];
for (const [name, i] of Object.entries({ p2: P14.p2, money: P14.money })) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(180);
  await pg.evaluate(() => {
    const d = window.deck, s = d.slides[d.i];
    const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  });
  await pg.waitForTimeout(2400);
  const m = await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i], r = s.getBoundingClientRect();
    let out = 0;
    s.querySelectorAll("div,p,h1,h2,h3,span,i,li").forEach((el) => {
      if (!el.offsetParent) return;
      const b = el.getBoundingClientRect();
      if (b.width && b.height && (b.bottom > r.bottom + 4 || b.right > r.right + 4)) out++;
    });
    const body = s.querySelector(".body");
    const kids = [...body.children].filter((e) => e.offsetParent);
    const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
    const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
    const ratio = Math.round(((bot - top) / body.getBoundingClientRect().height) * 100);
    const t = [...s.querySelectorAll("svg text")].filter((x) => x.textContent.trim());
    let ov = 0, worst = null;
    for (let i = 0; i < t.length; i++) for (let j = i + 1; j < t.length; j++) {
      const a = t[i].getBoundingClientRect(), c = t[j].getBoundingClientRect();
      if (!a.width || !c.width) continue;
      if (Math.min(a.right, c.right) - Math.max(a.left, c.left) > 2 &&
          Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top) > 2) {
        ov++; if (!worst) worst = [t[i].textContent.trim(), t[j].textContent.trim()];
      }
    }
    // svg 是否画出了自己的框（双轴图元素多，单独查一次）
    const svg = s.querySelector("svg"), sb = svg ? svg.getBoundingClientRect() : null;
    let vbOut = 0;
    if (svg) [...svg.querySelectorAll("text")].forEach((e) => {
      const b = e.getBoundingClientRect();
      if (b.width && (b.left < sb.left - 2 || b.right > sb.right + 2 ||
                      b.top < sb.top - 2 || b.bottom > sb.bottom + 2)) vbOut++;
    });
    return { out, ratio, ov, worst, vbOut };
  });
  r14.push({ name, ...m });
  await pg.screenshot({ path: `/tmp/qa/r14-${name}.png` });
}
chk(r14.every((x) => x.out === 0 && x.ov === 0 && x.vbOut === 0 && x.fill !== 0 &&
                     x.ratio >= 78 && x.ratio <= 106),
    `R14 · 两页零溢出 / 零 svg 文字重叠 / 零出框 / 填充率 78–106% ${JSON.stringify(r14)}`);
chk(/class="slide[^"]*\br14money\b/.test(html) && html.includes(".r14money "),
    "R14 · 页级档位类挂上且在 CSS 里有定义");

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
