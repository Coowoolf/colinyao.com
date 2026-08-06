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
// ⚠️ R19 改判：C19-② 删了五张金句页的编号 eyebrow —— 「01–05 五张」改由内容认（见 6.15 段）。
// ⚠️ 只数正文：C19_CSS 那段档位注释里也写了这个词，不算页内容
chk(await pg.evaluate(() => window.deck.slides.every((s) => !s.outerHTML.includes("观点页 · 嘉宾金句"))),
    "R19-② 金句页编号 eyebrow 全场清零");
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
// ⚠️ R17 改判：C17-④ 把终页那张尺子图整张重画了（外/内两列八条清单整块删，负 y 区随之消失，
//    viewBox 0 -177 1680 646 → 0 0 1680 640）——这条几何断言作废，新几何的正向账在 6.13 段。
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
// P8 企业侧换血：五条 bar 在位
// ⚠️ R17 改判：C17-⑥ 按 P7 体例把这一页的 SOURCE 行瘦身成**只留机构名**（n= 与月份细节全去，
//    Gartner 随预测对照一起撤）——「逐条标源与年份」三条作废；新 foot 的正向账在 6.13 段。
chk([">66%<", ">91%<", ">70%<", ">15–20%<", ">49%<"].every((k) => html.includes(k)),
    "R11 · P8 五条读数在位（SOURCE 行体例由 R17 接管）");
// ⚠️ R15-① 把这句从 note 提上主标题，中间多了一层 <em>；结论行保留后半段
chk(html.includes("对话式智能体在企业服务侧，<em>已经到了规模化应用的阶段</em>") &&
    html.includes("硬性基础全部具备"),
    "R11 · P9 结论行已改口径（R15 起在主标题上）");
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
// ⚠️ R17 改判：C17-②a 把这一页的 .note.co（「我不想制造恐慌…」）整段删了 ——
//    「叙述沉在 note 之后」失去参照物；C17-②c 又把 viewBox 加高 12（260 → 272）修掉一处
//    2px 文字越界。两条几何/相对位置账作废，只留「图在事件块之前」这条与画法无关的。
chk(p30s.indexOf('<div class="fig">') < p30s.indexOf('class="old tail') &&
    !p30s.includes('class="note co'),
    "R11 · P30 图最上并放大 / 事件叙述仍沉在最底部");
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
// ⚠️ R15-① 换了 P8 / P9 两张主标题，页序断言改用新标题取词
chk(seq12.p6.includes("语法变了") && seq12.p7.includes("钱的三次落点") &&
    seq12.p8.includes("对话式 AI 的钱，流向了哪里") && seq12.p9.includes("正在悄然发生"),
    "R12 · 三连页序：幕卡 → 新页全图 → 对话式内部分布 → 采购已开动");
// eyebrow 必须是 Colin 原话，逐字
chk(html.includes("产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走"),
    "R12 · 新页 eyebrow 用 Colin 原话（逐字）");
chk(html.includes("近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>"), "R12 · 新页 h2 在位");
// 三条赛道的名（R14 重做成双轴时间图、R16 又整张换成三格小倍数）
// ⚠️ R16 改判：三条线的「数」不再由这里守 —— 2.1 / ≈0.7 / 2.2+ 经重查全部作废，
//    $178B / $1.6B 在小倍数里各出现两次；逐条数值账（含来源与截点）搬到 6.12 段。
//    「走线光点 .pkt」是曲线图元，柱图上没有线可走，一并搬到 6.12 段作反向断言。
chk([">基础模型</text>", ">AI 写代码</text>", ">对话式 AI</text>"].every((k) => html.includes(k)),
    "R12 · 三条赛道的名全在");
const p7h = html.slice(html.search(/class="slide[^"]*\br12flow\b/));
const p7s = p7h.slice(0, p7h.indexOf("</section>"));
// ⚠️ R17 改判：C17-⑦ 把这一页的 note 整段删了，大泛类两翼（ElevenLabs / Sierra）的明细
//    随之下台 —— 改由口播承担，全文留档在设计文档 R17 段。这条正向断言作废。
chk([...p7s.matchAll(/data-step="(\d+)"/g)].every((m) => +m[1] <= 2), "R12 · 新页 data-step ≤2");
chk(/class="slide[^"]*\br12flow\b/.test(html) && html.includes(".r12flow "),
    "R12 · 新页档位类挂上且在 CSS 里有定义");
// 衔接：现 P8（钱页）eyebrow 已换成承接句
// ⚠️ R15-① 把这条 eyebrow 精简了（与新 h2 语义重复）
chk(!html.includes("先看钱往哪儿去了") &&
    html.includes('<div class="eyebrow flow" style="--i:0">承上页，再往里看一层</div>'),
    "R12 · P8 钱页 eyebrow 已改为衔接句（R15 精简版）");
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
// ③ Weil 金句 —— ⚠️ R15-⑦ 改判：整张搬到金句 02，拷问页回到纯问句全页大字。
//    这里只守「拷问页不再有 Weil / 不再有第二拍」，落点的正向账在 6.11 段。
const sAsk = await secOf(P.ask);
chk(!sAsk.includes("Writing evals") && !sAsk.includes("Kevin Weil") &&
    !sAsk.includes('data-step'),
    "R15-⑦ 灵魂拷问页已撤回 Weil 第二拍，回到纯问句全页大字");
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
// ⑥「perfect human」金句页 —— ⚠️ R16 改判：R13 换上来的英文逐字仍在，但
//    ⒜ 中文从一整行拆成两行 `<i>`（中上英下），contiguous 整句不再存在；
//    ⒝ 署名改成 Des Traynor（这句本来就不是 Bret 的）。两条正向账搬到 6.12 段。
const sMq = await secOf(P.mqTaylor);
chk(sMq.includes("is people compare it with this perfect human") &&
    sMq.includes("that does not exist.") &&
    "R13-⑥ 金句 03 的英文原句逐字仍在（署名与版式由 R16 接管，编号 eyebrow 已随 R19 删）");
// ⑦ 围栏 Part 点睛
const sFc = await secOf(P.mqFence);
chk(sFc.includes("是放出它。") &&
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
// ⚠️ r13ask 已随 R15-⑦ 撤回第二拍一并摘除
chk(["r13bell", "r13p5", "r13case", "r13mq", "r13fence"]
      .every((c) => new RegExp(`class="slide[^"]*\\b${c}\\b`).test(html) && html.includes(`.${c} `)) &&
    !/class="slide[^"]*\br13ask\b/.test(html),
    "R13 · 页级档位类全部挂上且在 CSS 里有定义（r13ask 已随 R15 摘除）");

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
// ② 钱流向页 —— ⚠️ **R16 改判：双轴时间图整张作废**（Colin 三条质疑全部成立：
//    左 0–200 / 右 0–4 把 $3.3B 画得比 $178B 还高；对话式那条取数残缺；融资额与 ARR 混图）。
//    R16 换成三格小倍数，所以双轴骨架 / 两套刻度 / 三条曲线 / 走线光点 / 渐变面积 /
//    终点名牌 / 值标五个 / foot 逐字，**全部从这里摘除**，正向账搬到 6.12 段。
//    仍留在这里的是不随画法变化的两条：三条层带旧图元清零 · 旧长 foot 口径清零。
const pmh = html.slice(html.search(/class="slide[^"]*\br14money\b/));
const pms = pmh.slice(0, pmh.indexOf("</section>"));
chk([">FOUNDATION MODELS</text>", ">CODING</text>", ">CONVERSATIONAL AI</text>",
     'class="stroke dw"', 'class="stroke-am dw"', ">$2B ARR</text>", ">≈$2.2B</text>",
     "同一层的两翼"].every((k) => !pms.includes(k)),
    "R14-② 三条层带的旧图元清零");
chk(["New Market Pitch 2026-07", "PYMNTS 2025-06", "SiliconANGLE 2026-05", "Newcomer 2026-02",
     "Crunchbase 2026-04", "CB Insights《State of AI 2025》2026-01",
     "本页自算，不是全类别口径", "带宽为量级示意，非等比", "Cartesia $100M", "Parloa $350M"]
      .every((k) => !html.includes(k)), "R14-② 旧的长口径 foot 全场清零");
// ⚠️ R17 改判：note 整段随 C17-⑦ 删掉，「这笔钱…下一页拆开看」作废（衔接改由页序本身承担）。
chk(["产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走",
     "近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>"].every((k) => pms.includes(k)),
    "R14-② eyebrow / h2 原样保留");
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

// ── 6.11) R15 终轮十项（全部内容锚定取页，不信页码） ──
const P15 = {
  money:  await idxOf("对话式 AI 的钱，流向了哪里"),
  buy:    await idxOf("对话式智能体的采购，正在悄然发生"),
  four:   await idxOf("已经到了规模化应用的阶段"),
  nstar:  await idxOf("四个阶段，四颗"),
  act2:   await idxOf("ENTRUSTED"),
  ladder: await idxOf("工具 → 实习生 → 外包 → 专家 →"),
  eval1:  await idxOf("你的 demo 在骗你"),
  mqWeil: await idxOf("Writing evals"),
  ask:    await idxOf("亲手写过"),
  ladderL:await idxOf("人还在不在环里"),
  jobs:   await idxOf("真实岗位放上梯子"),
  fin:    await idxOf("一套放权与决策机制"),
};
chk(Object.values(P15).every((i) => i >= 0), `R15 · 十二个目标页全部按内容找到 ${JSON.stringify(P15)}`);
// 负向：被换下 / 被删掉的整段必须查无此句
const cut15 = ["这不是一个垂类", "钱到了对话式 AI，再往里看一层：它分给了谁", "预测还在打架",
               "所有的路，最后都汇到「对话」这条线上", ">Conversational AI</text>",
               "可这三年里，一直是我们单方面朝它走", "下午 AIoT 专场整场拆开讲",
               // ⚠️ R16 改判：「被记住，靠的是一致性。被托付，靠的是可验证。」从这条负向名单摘除 ——
               //    R16-② 把 PART 2 幕卡首行退回了这句原文，它重新是正向内容（正向账见 6.12 段）。
               "这四级换的不是它的能力", "那把越来越硬的尺子",
               "给产品经理的动作 · 把你 demo 里最得意的那三条",
               "你以为在选模型，", "其实在选评测。", "模型半年换一次，评测集用三年",
               "L0 · 旁听", "L1 · 起草", "L2 · 只读应答", "L3 · 可执行", "L4 · 主动外呼",
               "L2 与 L3 之间", ">L4 主动<", ">L0–L1<", "Autonomy L4",
               "语音场景的 L2 门槛", "Agent 有 L0–L4", "这五笔"];
chk(cut15.every((k) => !html.includes(k)),
    `R15 · 被删/被换的整段全部清零（残留 ${JSON.stringify(cut15.filter((k) => html.includes(k)))}）`);
// ① 三个新主标题（h2 在位 + eyebrow 精简）
const s15money = await secOf(P15.money), s15buy = await secOf(P15.buy), s15four = await secOf(P15.four);
chk(s15money.includes('<h2 class="ink" style="--i:1">对话式 AI 的钱，<em>流向了哪里</em></h2>') &&
    s15money.includes("承上页，再往里看一层") && s15money.includes("ElevenLabs · 语音合成"),
    "R15-①a 钱分布页新主标题 + eyebrow 精简");
// ⚠️ R17 改判：C17-⑥ 把「预测还在打架」那整块 note 删了（Colin 点名），
//    「对照仍在 note 里」作废 —— 这一页从此只讲已经发生的采购。
chk(s15buy.includes('<h2 class="ink" style="--i:1">对话式智能体的采购，<em>正在悄然发生</em></h2>'),
    "R15-①b 渗透采购页新主标题");
chk(s15four.includes('对话式智能体在企业服务侧，<em>已经到了规模化应用的阶段</em>') &&
    s15four.includes('<div class="eyebrow flow" style="--i:0">四个互不相干的人，说了同一件事</div>') &&
    s15four.includes("四个方向的人，指向同一个判断：智能够用、部署可做、扩散周期已经开始、周边那圈软件也补齐了，"),
    "R15-①c 四方观点页新主标题 + 原 h2 降回 eyebrow + 结论行保留现文");
// ② CONVOAI AGENT
chk(s15four.includes(">CONVOAI AGENT</text>") &&
    (html.match(/CONVOAI AGENT/g) || []).length === 1, "R15-② 中心块英文标 CONVOAI AGENT");
// ③ 北极星逐列对齐（实测：四条 tread 的 x 跨度 = 四栏 nstar 的 x 跨度）+ note 清零
const align = await pg.evaluate(async (k) => {
  window.deck.go(k);
  await new Promise((r) => setTimeout(r, 400));
  const s = window.deck.slides[k];
  for (let st = 1; st <= 3; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
  await new Promise((r) => setTimeout(r, 1800));
  const ns = [...s.querySelectorAll(".nstar .ns")].map((e) => Math.round(e.getBoundingClientRect().left));
  const tt = [...s.querySelectorAll("svg text.ttl")].map((e) => Math.round(e.getBoundingClientRect().left));
  return { ns, tt, note: !!s.querySelector(".note") };
}, P15.nstar);
chk(!align.note && align.ns.length === 4 && align.tt.length === 4 &&
    align.ns.every((x, i) => Math.abs(x - align.tt[i]) <= 2),
    `R15-③ 北极星四栏与阶梯四级逐列对齐 + note 整段删 ${JSON.stringify(align)}`);
chk(/class="slide[^"]*\br15nstar\b/.test(html) && html.includes(".r15nstar "),
    "R15-③ 档位类 r15nstar 挂上且有定义");
// ④ PART 2 幕卡 —— ⚠️ **R16 改判：整条作废**。Colin 澄清 R15-④ 那句本意是放金句页，
//    R16 把它搬到金句 01、把幕卡首行退回原文。幕卡两行的正向账搬到 6.12 段。
// ⑤⑥ 两处删段
const s15lad = await secOf(P15.ladder), s15ev = await secOf(P15.eval1);
chk(!s15lad.includes('<div class="land') && s15lad.includes('<div class="g4">') &&
    s15lad.includes('viewBox="0 73 1680 484"'),
    "R15-⑤ 分水岭页 land 整段删 + 阶梯图纵拉伸撑满");
chk(!s15ev.includes('<div class="foot') && s15ev.includes("你的 demo 里全是前一种题"),
    "R15-⑥ Eval 第一课 foot 整句删");
// ⑦ Weil 只在金句 02（⚠️ R16 改判：R16-③ 把这一页改成中上英下，中文拆成两行 `<i>`，
//    contiguous 的中文整句不再存在 —— 中文两行的正向账搬到 6.12 段）
const s15mq = await secOf(P15.mqWeil);
// ⚠️ R19 改判两条：编号 eyebrow 已删（C19-②）；署名 前 CPO → ex CPO（C19-③）。正向账在 6.15 段。
chk(s15mq.includes("Writing evals is the most important") &&
    (html.match(/Kevin Weil · OpenAI ex CPO/g) || []).length === 1,
    "R15-⑦ Weil 整张占金句 02（全场仅一处）");
// ⑧ 梯子 L1-L5 + BIG JUMP 位置不动（天然 = L2→L3）+ 交叉验证条带不用改
const s15L = await secOf(P15.ladderL);
chk(["L1 · 旁听", "L2 · 起草", "L3 · 只读应答", "L4 · 可执行", "L5 · 主动外呼"].every((k) => s15L.includes(k)) &&
    s15L.includes('d="M675 45 V509"') &&
    s15L.indexOf("L2 · 起草") < s15L.indexOf("撤掉「人」这张安全网") &&
    s15L.indexOf("撤掉「人」这张安全网") < s15L.indexOf("L3 · 只读应答"),
    "R15-⑧ 梯子重编 L1–L5，BIG JUMP 位置不动 → 天然 L2→L3");
chk(["自动驾驶 L1–L5", "L1–L2 · 辅助驾驶，人不敢离环", "L3–L5 · 系统担责，卡了十年的一跳",
     "支付 Agent 五级", "L1–L2 · 行业还在边缘徘徊", "L3–L5 · 还没人真正到达",
     "向下的电梯 · THE WAY DOWN"].every((k) => s15L.includes(k)),
    "R15-⑧ 交叉验证条带与向下电梯旁注一个字未动即自洽");
// ⑨ 全 deck L 连坐 + 语义三处互证
const s15job = await secOf(P15.jobs), s15fin = await secOf(P15.fin);
chk(s15job.includes("压在 <em>L3 与 L4 之间</em>") && s15job.includes("今年整体重心：L3 与 L4 之间") &&
    [">L5 主动<", ">L4 可执行<", ">L3 只读应答<", ">L1–L2<"].every((k) => s15job.includes(k)),
    "R15-⑨a 岗位散点页 h2 / 纵轴 / 重心带标注全部同步");
chk((await secOf(P15.buy)) !== null &&
    html.includes("Autonomy L5") && html.includes("语音场景的 L3 门槛，比文本高一级") &&
    s15fin.includes("Agent 有 L1–L5，人有看过·用过·学过·干过"),
    "R15-⑨b/c/d 案例 02 / 执行围栏 / 全场收束三处 L 记号同步");
const noL0 = await pg.evaluate(() =>
  window.deck.slides.every((s) => !s.outerHTML
    .replace(/data:image\/[a-z+]+;base64,[A-Za-z0-9+/=]+/g, "").includes("L0")));
chk(noL0, "R15-⑨ 全 deck 正文再无 L0");
// ⑩ 终检：幕序课序金句序 / 目标页零溢出与填充率
// ⚠️ R16 改判：⑩a「2026 光是上半年这几笔」随 C16-⑤ 的 note 整段重写而作废（负向的「这五笔」仍在上面 cut15 里）
// ⚠️ R19 改判：编号 eyebrow 全删 —— 「五张」的账见 6.15 段（五句主文各一处 + 五个档位类）。
chk(["Eval 第一课", "Eval 第二课", "Eval 第三课", "Eval 第四课"].every((k) => html.includes(k)),
    "R15-⑩b Eval 四课课序完整");
const r15 = [];
for (const [name, i] of Object.entries({ money8: P15.money, buy9: P15.buy, four10: P15.four,
    nstar11: P15.nstar, act12: P15.act2, ladder28: P15.ladder, jobs29: P15.jobs,
    "mq-weil": P15.mqWeil })) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(300);
  await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i];
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
    let ratio = null;
    if (body) {
      const kids = [...body.children].filter((e) => e.offsetParent);
      const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
      const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
      ratio = Math.round(((bot - top) / body.getBoundingClientRect().height) * 100);
    }
    // 还没开完的 clip-path（动画未落位 = 页面上会看到半截字）
    let clipped = 0;
    s.querySelectorAll("*").forEach((el) => {
      const cp = getComputedStyle(el).clipPath;
      if (cp && cp !== "none" && [...cp.matchAll(/([\d.]+)%/g)].some((x) => parseFloat(x[1]) > 1)) clipped++;
    });
    return { out, ratio, clipped };
  });
  r15.push({ name, ...m });
  await pg.screenshot({ path: `/tmp/qa/r15-p${name}.png` });
}
chk(r15.every((x) => x.out === 0 && x.clipped === 0 && (x.ratio === null || (x.ratio >= 78 && x.ratio <= 106))),
    `R15 · 八页零溢出 / 零半截字 / 填充率 78–106% ${JSON.stringify(r15)}`);
// 全 46 页 .body 填充率下限（R15 终检把最低的那页 62% 修到 ~80%）
const fillAll = await pg.evaluate(async () => {
  const out = [];
  for (let i = 0; i < window.deck.slides.length; i++) {
    window.deck.go(i);
    await new Promise((r) => setTimeout(r, 90));
    const s = window.deck.slides[i], body = s.querySelector(".body");
    if (!body) continue;
    const mx = Math.max(0, ...[...s.querySelectorAll("[data-step]")].map((e) => +e.dataset.step));
    for (let st = 1; st <= mx; st++) s.querySelectorAll(`[data-step="${st}"]`).forEach((e) => e.classList.add("on"));
    const kids = [...body.children].filter((e) => e.offsetParent);
    if (!kids.length) continue;
    const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
    const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
    out.push({ p: i + 1, r: Math.round(((bot - top) / body.getBoundingClientRect().height) * 100) });
  }
  return out;
});
const lowFill = fillAll.filter((x) => x.r < 78 || x.r > 106);
chk(lowFill.length === 0, `R15-⑩c 全 46 页填充率 78–106%（异常 ${JSON.stringify(lowFill)}）`);
chk(/class="slide[^"]*\br15end\b/.test(html) && html.includes(".r15end "),
    "R15-⑩c 全场收束页留白失衡已修（档位类 r15end 在位）");

// ── 6.12) R16 五处（全部内容锚定取页，不信页码） ──
//   ① 金句 01 主文换血 ② PART 2 幕卡首行还原 ③④ 两张金句页中上英下 + 金句 03 出处改正
//   ⑤ P7 钱流向页：数据重查 + 弃双轴重画成三格小倍数
const P16 = {
  mq01:  await idxOf("我们叫了它三年"),
  act2:  await idxOf("ENTRUSTED"),
  mq02:  await idxOf("Writing evals"),
  mq03:  await idxOf("perfect human"),
  money: await idxOf("钱的三次落点"),
};
chk(Object.values(P16).every((i) => i >= 0), `R16 · 五个目标页全部按内容找到 ${JSON.stringify(P16)}`);
// 负向：被换下 / 被作废的整段必须查无此句
const cut16 = ["兑现的，", "不是模型更聪明了。", "是「谁负责」这件事，", "终于有了答案。",  // ① 旧金句 01
               "左右两轴量级不同", ">基础模型 $B</text>", ">Coding / 对话式 $B</text>",   // ⑤ 双轴骨架
               // ⚠️ R19 改判：三条曲线与名牌引线的类名从负向名单摘除 —— R19 把这一页换回了
               //    单轴对数三线图，线与引线名正言顺地回来了；R16 判死的是「双轴」，红线账见 6.15 段。
               'id="r14conv"',                                                             // ⑤ 双轴图那层渐变面积
               "Cursor ARR $2B", "2026 转向收入兑现",                                       // ⑤ ARR 混入融资图
               ">$2.1B</text>", ">≈$0.7B</text>", ">$2.2B+</text>",                         // ⑤ 被重查推翻的三个数
               "2026 光是上半年这几笔", "CB Insights《State of AI 2025》"];                 // ⑤ 旧 note 量词 / 旧来源
chk(cut16.every((k) => !html.includes(k)),
    `R16 · 被删/被换的整段全部清零（残留 ${JSON.stringify(cut16.filter((k) => html.includes(k)))}）`);
// ①② 一次搬家：金句 01 拿到那句、幕卡退回原文、全场「我们叫了它三年」恰好一处
const s16q1 = await secOf(P16.mq01), s16act = await secOf(P16.act2);
chk(s16q1.includes('<i class="rise" style="--i:1">我们叫了它三年 Agent（代理人）——</i>') &&
    s16q1.includes('<i class="rise" style="--i:2">今天，它终于开始代理了。</i>') &&
    s16q1.includes("所以今年这一场，讲的不是能力，是责任。"),
    "R16-① 金句 01 新主文两行 + 承句保留");
// ⚠️ R17 改判：C17-⑩ 把四张 PART 幕卡的开头小字**整块删了**，R16 刚还原的那两行也一并下台 ——
//    这一条整条作废，幕卡的正向账（骨架四件在、小字清零）搬到 6.13 段。
const nAgent3y = await pg.evaluate(() =>
  window.deck.slides.filter((s) => (s.textContent || "").includes("我们叫了它三年")).length);
chk(nAgent3y === 1, `R16-①② 全场「我们叫了它三年」恰好一处（实测 ${nAgent3y} 页）`);
// ③④ 中上英下：DOM 顺序中文在英文之前 + 实测字号中文 > 英文 + 中文每行不折行（禁止词中断行）
const mqLayout = [];
for (const [name, i] of Object.entries({ mq02: P16.mq02, mq03: P16.mq03 })) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(2400);
  mqLayout.push(await pg.evaluate((nm) => {
    const s = window.deck.slides[window.deck.i];
    const q = s.querySelector(".mq .q"), en = s.querySelector(".mq .en");
    const qFs = parseFloat(getComputedStyle(q).fontSize), enFs = parseFloat(getComputedStyle(en).fontSize);
    // DOM 顺序：中文节点必须排在英文节点之前
    const order = q.compareDocumentPosition(en) & Node.DOCUMENT_POSITION_FOLLOWING ? "zh-then-en" : "en-then-zh";
    // 每一行 <i> 只占一个 client rect = 没有被容器宽度折断（折断就会在词中间断开）
    const lines = [...s.querySelectorAll(".mq .q i")].map((e) => e.getClientRects().length);
    const qb = q.getBoundingClientRect(), sb = s.getBoundingClientRect();
    return { nm, qFs, enFs, order, wrapped: lines.filter((n) => n !== 1).length, nLines: lines.length,
             fits: qb.left >= sb.left && qb.right <= sb.right };
  }, name));
  await pg.screenshot({ path: `/tmp/qa/r16-${name}.png` });
}
chk(mqLayout.every((x) => x.order === "zh-then-en" && x.qFs > x.enFs && x.wrapped === 0 &&
                          x.nLines === 2 && x.fits),
    `R16-③④ 两张金句页中上英下：DOM 中文在前 + 中文字号 > 英文 + 两行零折行 ${JSON.stringify(mqLayout)}`);
// ④ 出处改正：Des Traynor 在位 · 金句 03 页内 Bret Taylor / 2026-03 公开访谈 清零
const s16q3 = await secOf(P16.mq03);
chk(s16q3.includes('<div class="s rise" style="--i:5">Des Traynor · Intercom 联合创始人</div>') &&
    s16q3.includes('<div class="s src rise" style="--i:6">Cheeky Pint #11 · 00:10:29</div>') &&
    !s16q3.includes("Bret Taylor") && !s16q3.includes("2026-03 公开访谈") &&
    s16q3.includes("One of the biggest fallacies in AI is people compare it with this perfect human"),
    "R16-④ 金句 03 出处改正（Des Traynor + Cheeky Pint #11 · 00:10:29），英文逐字未动");
// ⚠️ 全场「Bret Taylor」只从金句 03 撤下，其余三处是核过的真引文，一个都不许连坐：
//    P4「English over PSTN」/ P23 Sierra 官方博客 / P43「Hyper high-agency」
const bret = await pg.evaluate(() => {
  const hit = window.deck.slides.map((s, i) => [(s.textContent || "").includes("Bret Taylor"), i + 1])
                                .filter((x) => x[0]).map((x) => x[1]);
  return hit;
});
chk(bret.length === 3 &&
    ["You have all these fancy MCP things", "business outcomes delivered",
     "Hyper high-agency people who really deeply care."].every((k) => html.includes(k)),
    `R16-④ 全场 Bret Taylor 剩三处真引文（页 ${JSON.stringify(bret)}）`);
// ⑤ 钱流向页 —— ⚠️ **R19 改判：三格小倍数整张作废**（Colin 要「带时间轴的曲线」，数据一个不动）。
//    尺度说明句 / 九根柱 / 九个值标 / 三基线三表头线 / 三个「至今」/ 落点年高亮 / 三格截点 / 格内 take
//    全部从这里摘除，正向账（三序列九个数、对数轴、零第二把尺）搬到 6.15 段。
//    R16 立住且 R19 一字未动的两条留在这里：数值序列 与 单一口径行。
const s16m = await secOf(P16.money);
chk(/class="slide[^"]*\br16money\b/.test(html) && html.includes(".r16money "),
    "R16-⑤ 档位类 r16money 挂上且在 CSS 里有定义");
chk(s16m.includes(">口径：一级市场披露融资额 · $B</text>"), "R16-⑤ 单一口径行在位");
chk([">$31.4B</text>", ">$88.9B</text>", ">$178B</text>",
     ">$1.6B</text>", ">$3.3B</text>", ">$0.2B</text>",
     ">$1.9B</text>", ">$1.8B</text>"]
      .every((k) => (s16m.match(new RegExp(k.replace(/[$.]/g, "\\$&"), "g")) || []).length === 1),
    "R16-⑤ 三条序列 = 重查结果，各标一处（31.4/88.9/178 · 1.6/3.3/0.2 · 1.6/1.9/1.8）");
// svg 内不许再有 ARR / 收入口径；note 交代 $1.82B 是保守下限；foot 换源后仍是一行体例
const svg16 = s16m.slice(s16m.indexOf("<svg"), s16m.indexOf("</svg>"));
chk(!svg16.includes("ARR") && !svg16.includes("收入"), "R16-⑤ 融资图内零 ARR / 零收入口径");
// ⚠️ R17 改判：note 整段随 C17-⑦ 删掉（两层意思改由口播承担 + 设计文档留档），只留 foot 这条。
chk(s16m.includes('<div class="foot flow rev" style="--i:9">Source · New Market Pitch · Crunchbase News · TechCrunch · CNBC</div>'),
    "R16-⑤ foot 换源后仍是一行来源名");
// ⚠️ R17 改判：两翼明细随 note 一起下台（见上），这里只守 eyebrow / h2 未动。
chk(["产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走",
     "近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>"].every((k) => s16m.includes(k)),
    "R16-⑤ eyebrow / h2 未动");
// 五页逐页：零溢出 / 零半截字 / svg 文字零重叠 / 填充率 78–106% + 截图（2.4s 等入场落位）
const r16 = [];
for (const [name, i] of Object.entries({ mq01: P16.mq01, act2: P16.act2, mq02: P16.mq02,
                                         mq03: P16.mq03, money7: P16.money })) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(300);
  await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i];
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
    let ratio = null;
    if (body) {
      const kids = [...body.children].filter((e) => e.offsetParent);
      const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
      const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
      ratio = Math.round(((bot - top) / body.getBoundingClientRect().height) * 100);
    }
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
    // 还没开完的 clip-path = 页面上会看到「半截字」
    let clipped = 0;
    s.querySelectorAll("*").forEach((el) => {
      const cp = getComputedStyle(el).clipPath;
      if (cp && cp !== "none" && [...cp.matchAll(/([\d.]+)%/g)].some((x) => parseFloat(x[1]) > 1)) clipped++;
    });
    return { out, ratio, ov, worst, clipped };
  });
  r16.push({ name, ...m });
  await pg.screenshot({ path: `/tmp/qa/r16-${name}.png` });
}
chk(r16.every((x) => x.out === 0 && x.ov === 0 && x.clipped === 0 &&
                     (x.ratio === null || (x.ratio >= 78 && x.ratio <= 106))),
    `R16 · 五页零溢出 / 零 svg 文字重叠 / 零半截字 / 填充率 78–106% ${JSON.stringify(r16)}`);

// ── 6.13) R17 十二处（熵减轮：九处删文 + 一处点名 + 一处标题 + 一处出处；全部内容锚定取页） ──
const P17 = {
  p7:   await idxOf("钱的三次落点"),
  p8:   await idxOf("流向了哪里"),
  p9:   await idxOf("正在悄然发生"),
  p15:  await idxOf("2,475 通"),
  p24:  await idxOf("对商业量"),
  p27:  await idxOf("可观测，才敢写进需求文档"),
  p31:  await idxOf("提示词拦话术"),
  p45:  await idxOf("全场收束，一页带走"),
  p46:  await idxOf("向内叫内观"),
  p4:   await idxOf("fancy MCP things"),
  act1: await idxOf("GRAMMAR"),
  act4: await idxOf("PEOPLE & ORG"),
};
chk(Object.values(P17).every((i) => i >= 0), `R17 · 十二个目标页全部按内容找到 ${JSON.stringify(P17)}`);
// 负向：九处删文的整段必须清零（只数页面正文 —— 历史层的 CSS 注释里写过被删素材的名字）
// ⚠️ **R18 起的通用护栏**：C18 把一张 78KB 的门图 base64 内联进了 P44，base64 是纯 ASCII 乱码，
//    全 deck 的英文短串负向扫描（Legora / Gartner / L0 …）会被它随机命中而误报 ——
//    凡是「整本扫英文短串」的检查，一律先把 data-URI 载荷抹掉（中文串不受影响）。
const noURI = (t) => t.replace(/data:image\/[a-z+]+;base64,[A-Za-z0-9+/=]+/g, "data:image/…");
const slides17 = noURI(await pg.evaluate(() => window.deck.slides.map((s) => s.outerHTML).join("")));
const cut17 = ["不是你问它才查。是你还没开口", "发起权第一次不在人这边", "而不是摊进某个人的 KPI",
               "翻最近 100 次交互，几次是它发起的？", "它自报家门那句话，写在哪个文件里？",
               "报表里有没有独立的一行？", "出事五分钟内，你拿得出那条链路吗？",
               "这四句话里，只要有一句", "四个「怎么验」，回去就能跑一遍",              // ① P27 六块
               "我不想用这一页制造恐慌", "从伦理讨论变成了工程需求",                    // ②a P31
               "一家模型厂的公开披露", "一家第三方平台的生产设施",                      // ②b 匿名说法
               "越往上，答案<em>越短</em> —— 也越重", "全场收束 · ONE LINE EACH",       // ③ P45
               "外 · 读 AGENT", "抢话、复读、没转人工", "一百条里踩了几条",
               "模型的问题还是流程的", "同一套题，分数动没动", "内 · 读自己",
               "我凭什么说它不行", "我的判断能不能复现", "我是不是在用感觉验收",
               "我改的是它还是我的标准", 'viewBox="0 -177 1680 646"',                  // ④ P46 两列 + 旧 viewBox
               "¥5,850 亿", "早就趴在预算科目里", "变成了预算科目",                     // ⑤ P8
               "至于预测？同一年的两份报告还在打架", "别等预测收敛，看采购",
               "这道题第二、三幕来解", "Gartner", "（n=3,075", "（n=5,119）",           // ⑥ P9
               "2024 那一年，写代码和对话式拿到的钱一样多", "还没算进 Sierra 五月那笔 $950M",
               "对话式 AI 是个大泛类", "下一页拆开看。",                                 // ⑦ P7 note
               "设想的是一场五分钟的文字对谈", "在毫不知情的状态下完成的",               // ⑧ P15
               "法律 AI 公司 Legora 的做法值得抄", "谁定义正确，谁就掌握这段关系",       // ⑨ P24
               "被使用、被记住、被托付——三个「被」字",
               "被记住，靠的是一致性。被托付，靠的是可验证。",
               "三年了，一直是我们朝它走一步、再走一步", "前面三幕讲的是「怎么造那把尺子」",  // ⑩ 四张幕卡小字
               "2026-03 公开访谈"];                                                     // ⑪ P4 旧出处
chk(cut17.every((k) => !slides17.includes(k)),
    `R17 · 九处删文全部清零（残留 ${JSON.stringify(cut17.filter((k) => slides17.includes(k)))}）`);
// ① P27：只剩三个 Signal 标题 + Q1–Q4 两行对照（Q4 那句长的 Colin 没点名，必须留）
const s17p27 = await secOf(P17.p27);
chk(["它主动想起", "它主动开口", "它有自己的 OKR", ">谁先行动？<", ">谁代表谁？<",
     ">结果记在哪？<", ">出错谁负责？<",
     "先有归属，才谈得上追责——业绩可以记在它名下，责任必须落在可追责的人身上。"]
      .every((k) => s17p27.includes(k)) &&
    (s17p27.match(/<div class="kv/g) || []).length === 8 &&
    !s17p27.includes("怎么验") && !s17p27.includes('<div class="note'),
    "R17-① P27 六块删净：只剩三个 Signal 标题 + Q1–Q4 各两行对照（8 条 kv）");
// ② P31：note 清零 + 事件主体实名（OpenAI / Hugging Face / Clem Delangue / Presence）+ 来源行
const s17p31 = await secOf(P17.p31);
chk(s17p31.includes('viewBox="0 0 1680 272"') &&
    !s17p31.includes('<div class="note') &&
    ["2026-07 · OpenAI 的公开披露", "入侵了 <b>Hugging Face</b> 的生产设施",
     "Hugging Face CEO Clem Delangue", "可能是同类中的第一起",
     "<b>OpenAI Presence</b>（7-22）", "<b>相隔不到 24 小时</b>",
     '<span class="src">Fortune · The Hacker News · TechCrunch · CBS News · 2026-07</span>']
      .every((k) => s17p31.includes(k)) &&
    // ⚠️ R19 改判：教训 03 标题改「也必须写进 SOP 流程里」（C19-④），正向账在 6.15 段
    ["提示词不是围栏", "围栏必须在架构里"].every((k) => s17p31.includes(k)),
    "R17-② P31 恐慌段删净 + 事件主体实名到位 + 三张教训卡未被误伤");
// ③ P45：新 h2 + 旧 h2 降级进 eyebrow + 四栏不动
const s17p45 = await secOf(P17.p45);
chk(s17p45.includes('<h2 class="ink" style="--i:1">全场收束，<em>一页带走</em></h2>') &&
    s17p45.includes('<div class="eyebrow flow" style="--i:0">ONE LINE EACH · 越往上，答案越短，也越重</div>') &&
    ["交的不再是一份 PRD", "管的不再是三个职能", "卖的不再是调用量", "要的不是 AI 能力"]
      .every((k) => s17p45.includes(k)),
    "R17-③ P45 标题对调（新 h2 + 旧 h2 降级进 eyebrow），四栏未动");
// ④ P46：两列八条清零 + svg 按新版心重画（--len 与新路径同步）
const s17p46 = await secOf(P17.p46);
chk(s17p46.includes('viewBox="0 0 1680 640"') &&
    ['x="800" y="90" width="88" height="420"',
     'd="M800 176 H836 M800 258 H824 M800 340 H836 M800 422 H824"', "--len:140;--i:3",
     'style="--len:400;--i:4" stroke-width="1.8" d="M908 300 H1300"',
     'style="--len:410;--i:6" stroke-width="1.8" d="M780 300 H380"',
     ">同一把尺子</text>", ">向外 · Eval</text>", ">向内 · 内观</text>",
     ">AGENT / PRODUCT</text>", ">HUMAN / SELF</text>"].every((k) => s17p46.includes(k)) &&
    (s17p46.match(/class="stroke-am pkt"/g) || []).length === 1 &&
    (s17p46.match(/class="stroke-co pkt"/g) || []).length === 1,
    "R17-④ P46 两列八条删净 + 尺子图按新版心重画（两枚同步光点各一枚）");
// ⑤⑥⑦ 三页删文 + 两处 foot
const s17p8 = await secOf(P17.p8), s17p9 = await secOf(P17.p9), s17p7 = await secOf(P17.p7);
chk(!s17p8.includes('<div class="note') && !s17p8.includes('<div class="foot') &&
    (s17p8.match(/<div class="card/g) || []).length === 6,
    "R17-⑤ P8 国内存量 note + foot 双删，六张卡一张不少");
chk(!s17p9.includes('<div class="note') &&
    s17p9.includes('<div class="foot flow rev" style="--i:11">SOURCE · Salesforce · CC-CMM · 艾媒咨询 · 第一新声 · Pew Research</div>') &&
    [">66%</text>", ">70%</text>", ">91%</text>", ">15–20%</text>", ">49%</text>"].every((k) => s17p9.includes(k)),
    "R17-⑥ P9 预测对照删净 + foot 只留机构名（五条读数未动）");
chk(!s17p7.includes('<div class="note') && !s17p7.includes("Sierra") &&
    ["口径：一级市场披露融资额 · $B", "一个季度，就是去年一整年的两倍",
     "一轮钱在 2025 发完 · Cursor 一家占 98%", "半年，已经追平去年一整年",
     "Source · New Market Pitch · Crunchbase News · TechCrunch · CNBC"].every((k) => s17p7.includes(k)),
    "R17-⑦ P7 note 删净，口径行 / 三格 take / foot 未动");
// ⑦ ⚠️ **R19 改判**：C19-① 把这张 svg 整张换成了「单轴对数三线图」（数据一个不动），
//    R17 那次「顶行以外整体下移 84（viewBox 560 → 644）」的几何搬运账随之作废；
//    新图的几何账在 6.15 段。这里只守 R17 真正做的那件事：note 删净 + 三条叙事注仍在（上一条）。
// ⑧⑨ 两处压缩（⑧ 含两处对 Colin 口述的口径修正）
const s17p15 = await secOf(P17.p15), s17p24 = await secOf(P17.p24);
chk(s17p15.includes('<div class="foot flow" style="--i:4">1950 年，图灵提出那场五分钟的判别游戏；76 年后，<b>96.5% 的真实通话</b>，悄悄通过了图灵测试。</div>') &&
    !s17p15.includes("150") && s17p15.includes("只有 <b>86 通</b> 被对方听出"),
    "R17-⑧ P15 图灵两句压成一句（150 年归贝尔那页 · 96.5% 口径 = 真实通话占比）");
chk(!s17p24.includes("Legora") && !s17p24.includes('<span class="s">') &&
    s17p24.includes("从规划到回款，出题权一路没换过手。"),
    "R17-⑨ P24 Legora 那句删净，land 主句未动");
// ⑩ 四张幕卡：小字清零 + 骨架四件齐全 + 资金页没被误当成幕卡
const acts17 = await pg.evaluate(() => {
  const out = [];
  window.deck.slides.forEach((s, i) => {
    if (!s.querySelector(".act")) return;
    const h = s.outerHTML;
    out.push({ p: i + 1,
      cn: (s.querySelector(".act .cn") || {}).textContent || "",
      d: h.includes('<div class="d flow"'),
      num: h.includes('<div class="num flow"'), en: h.includes('<div class="en settle"'),
      rail: h.includes('<div class="rail">') });
  });
  return out;
});
chk(acts17.length === 4 && acts17.every((a) => !a.d && a.num && a.en && a.rail) &&
    acts17.map((a) => a.cn).join("|") === "语法变了|被托付|双向奔赴 · 共事|人与组织",
    `R17-⑩ 四张幕卡小字清零、骨架四件齐全 ${JSON.stringify(acts17)}`);
chk(!(await secOf(P17.p7)).includes('<div class="act">'), "R17-⑩ 资金流向页未被误当成幕卡");
// ⑪ P4 出处精化
chk((await secOf(P17.p4)).includes('<div class="by">Bret Taylor · CEO of Sierra / Chairman of OpenAI · Cheeky Pint #27</div>'),
    "R17-⑪ P4 出处「2026-03 公开访谈」→「Cheeky Pint #27」");
// ⑫ P44 —— ⚠️ **R18 改判**：R17 那一轮按 Colin 的话按兵不动（等生成图），
//    当时立了「门图仍是那一张 svg」的守门断言；R18 图到了，那对 svg 门已被单张门图取代，
//    `<svg count === 1` 作废。三段文字「一字未改」的账仍然成立（只是挪出 svg 重排），继续守。
const s17p44 = await secOf(await idxOf("从分清单向门与双向门开始"));
// ⚠️ R19 改判：CEO 那行在 C19-⑤ 整行删了，从这条名单摘出（负向账在 6.15 段）
chk(["可逆 · 双向门 · 放手做，不用批", "不可逆 · 单向门 · 先升级"].every((k) => s17p44.includes(k)),
    "R17-⑫ P44 的两段门标签一字未改（门图由 R18 接管）");
// 连坐终扫：被删素材在全 deck 不留悬空引用
// ⚠️「怎么验」只在 P27 有过**标签**用法；P45 的「做到了，我怎么验」是自然语言，自己站得住
chk(!slides17.includes('<div class="kk">怎么验</div>') &&
    slides17.includes("把「它能不能做到」换成「做到了，我怎么验」。") &&
    ["Legora", "Gartner", "5,850", "预测"].every((k) => !slides17.includes(k)),
    "R17 · 被删素材全场零残留（「怎么验」按标签形态查，P45 那句自然语言不误伤）");
chk(["r17money", "r17p8", "r17p9", "r17p15", "r17p24", "r17p27", "r17case3", "r17fin"]
      .every((c) => new RegExp(`class="slide[^"]*\\b${c}\\b`).test(html) && html.includes(`.${c} `)),
    "R17 · 八个页级档位类全部挂上且在 CSS 里有定义");
// 十一页逐页：零溢出 / 零 svg 文字重叠 / 零出框 / 零半截字 / 填充率 78–106% + 截图（2.4s）
const r17 = [];
for (const [name, i] of Object.entries({ p27: P17.p27, p31: P17.p31, p45: P17.p45, p46: P17.p46,
    p8: P17.p8, p9: P17.p9, p7: P17.p7, p15: P17.p15, p24: P17.p24,
    act1: P17.act1, act4: P17.act4 })) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(300);
  await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i];
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
    // 幕卡（.act）与 .mega 版式没有 .body，填充率不适用 —— 与全场那条检查口径一致
    const body = s.querySelector(".body");
    let ratio = null;
    if (body) {
      const kids = [...body.children].filter((e) => e.offsetParent);
      if (kids.length) {
        const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
        const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
        ratio = Math.round(((bot - top) / body.getBoundingClientRect().height) * 100);
      }
    }
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
    const svg = s.querySelector("svg"), sb = svg ? svg.getBoundingClientRect() : null;
    let vbOut = 0;
    if (svg) [...svg.querySelectorAll("text")].forEach((e) => {
      const b = e.getBoundingClientRect();
      if (b.width && (b.left < sb.left - 2 || b.right > sb.right + 2 ||
                      b.top < sb.top - 2 || b.bottom > sb.bottom + 2)) vbOut++;
    });
    let clipped = 0;
    s.querySelectorAll("*").forEach((el) => {
      const cp = getComputedStyle(el).clipPath;
      if (cp && cp !== "none" && [...cp.matchAll(/([\d.]+)%/g)].some((x) => parseFloat(x[1]) > 1)) clipped++;
    });
    return { out, ratio, ov, worst, vbOut, clipped };
  });
  r17.push({ name, ...m });
  await pg.screenshot({ path: `/tmp/qa/r17-${name}.png` });
}
chk(r17.every((x) => x.out === 0 && x.ov === 0 && x.vbOut === 0 && x.clipped === 0 &&
                     (x.ratio === null || (x.ratio >= 78 && x.ratio <= 106))),
    `R17 · 十一页零溢出 / 零 svg 文字重叠 / 零出框 / 零半截字 / 填充率 78–106% ${JSON.stringify(r17)}`);

// ── 6.14) R18 一处：P44 那两个 SVG 门 → Colin 用 GPT-image 生成的单张门图 ──
const iP44 = await idxOf("从分清单向门与双向门开始");
chk(iP44 >= 0, `R18 · P44 按内容找到（第 ${iP44 + 1} 页）`);
const s18 = await secOf(iP44);
// ⓐ 单张门图在位：内联 data URI（WebP）+ screen 融底 + .rise 入场，且全场只此一张 webp
chk(s18.includes('<div class="doors rise" style="--i:3">') &&
    (s18.match(/<img src="data:image\/webp;base64,/g) || []).length === 1 &&
    s18.includes('alt="左：可逆的双向弹簧门；右：不可逆的单向金库门"') &&
    (html.match(/data:image\/webp;base64,/g) || []).length === 1,
    "R18-① P44 单张门图内联在位（data URI · webp · .rise），全场唯一一张 webp");
// ⓑ 旧的两个 svg 门整块清零（这一页从此没有 svg）
chk(!s18.includes("<svg") &&
    ['class="stroke-am pkt"', 'd="M940 70 V552"', 'x="350" y="160"', 'x="1130" y="160"']
      .every((k) => !s18.includes(k)),
    "R18-① P44 旧双门 SVG 元素全部清零");
// ⓒ 两组标签在位、对位到实测的两扇门中心，文字一字未改；land 原样
// ⚠️ R19 改判：CEO 那句（R18 才挪出来的 .dcap 独立行）在 C19-⑤ 整行删了，从这条摘出。
chk(s18.includes('<div class="dl am" style="left:27.2%">可逆 · 双向门 · 放手做，不用批</div>') &&
    s18.includes('<div class="dl co" style="left:72.3%">不可逆 · 单向门 · 先升级</div>') &&
    s18.includes("<b>把权放给 high agency 的人</b>——他们会带着 Agent，把结果一起做出来。"),
    "R18-① 图下双标签 + land 落地句，文字一字未改");
chk(/class="slide[^"]*\br18doors\b/.test(html) && html.includes(".r18doors "),
    "R18 · 档位类 r18doors 挂上且在 CSS 里有定义");
// ⓓ 浏览器实测：图真的解码了、blend 生效、标签中心落在门中心、零溢出零半截字、填充率入账
await pg.evaluate((k) => window.deck.go(k), iP44);
await pg.waitForTimeout(2400);
const m18 = await pg.evaluate(() => {
  const s = window.deck.slides[window.deck.i], sr = s.getBoundingClientRect();
  const img = s.querySelector(".doors img"), ib = img.getBoundingClientRect();
  const dls = [...s.querySelectorAll(".doors .dl")].map((e) => {
    const b = e.getBoundingClientRect();
    return { t: e.textContent.trim(), pct: +(((b.left + b.width / 2) - ib.left) / ib.width * 100).toFixed(1),
             l: Math.round(b.left), r: Math.round(b.right) };
  });
  let out = 0;
  s.querySelectorAll("div,p,h1,h2,h3,span,i,li,img").forEach((el) => {
    if (!el.offsetParent) return;
    const b = el.getBoundingClientRect();
    if (b.width && b.height && (b.bottom > sr.bottom + 4 || b.right > sr.right + 4)) out++;
  });
  let clipped = 0;
  s.querySelectorAll("*").forEach((el) => {
    const cp = getComputedStyle(el).clipPath;
    if (cp && cp !== "none" && [...cp.matchAll(/([\d.]+)%/g)].some((x) => parseFloat(x[1]) > 1)) clipped++;
  });
  const body = s.querySelector(".body"), kids = [...body.children].filter((e) => e.offsetParent);
  const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
  const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
  return { decoded: img.complete && img.naturalWidth > 0,
           nat: [img.naturalWidth, img.naturalHeight],
           blend: getComputedStyle(img).mixBlendMode,
           w: Math.round(ib.width), h: Math.round(ib.height),
           centred: Math.abs((ib.left + ib.width / 2) - (sr.left + sr.width / 2)) <= 2,
           dls, out, clipped,
           fill: Math.round(((bot - top) / body.getBoundingClientRect().height) * 100),
           svgs: s.querySelectorAll("svg").length };
});
await pg.screenshot({ path: "/tmp/qa/r18-p44.png" });
chk(m18.decoded && m18.nat[0] === 1672 && m18.nat[1] === 669 && m18.blend === "screen" &&
    // ⚠️ R19 改判：C19-⑤ 把门图从 1380 收到 1180（Colin：现在有点过大），宽度区间下调
    m18.svgs === 0 && m18.centred && m18.w >= 1150 && m18.w <= 1220,
    `R18-① 门图解码成功 / screen 生效 / 居中 / 宽 1150–1220 / 页面零 svg ${JSON.stringify({ ...m18, dls: undefined })}`);
chk(m18.dls.length === 2 && Math.abs(m18.dls[0].pct - 27.2) <= 0.5 &&
    Math.abs(m18.dls[1].pct - 72.3) <= 0.5 && m18.dls[0].r < m18.dls[1].l,
    `R18-① 两组标签对位到门中心（27.2% / 72.3%）且互不重叠 ${JSON.stringify(m18.dls)}`);
chk(m18.out === 0 && m18.clipped === 0 && m18.fill >= 78 && m18.fill <= 106,
    `R18-① P44 零溢出 / 零半截字 / 填充率 78–106%（实测 ${m18.fill}%）`);

// ── 6.15) R19 五处（全部内容锚定取页，不信页码） ──
//   ① P7 换回「带时间轴的曲线」＝单轴对数三线图（数据一个不动）② 五张金句页 eyebrow 全删
//   ③ 金句 02 署名 ex CPO ④ P31 三段教训正文删 + 教训 03 改题 ⑤ P44 删 CEO 行 + 图收比例
const P19 = {
  p7:   await idxOf("钱的三次落点"),
  mq01: await idxOf("我们叫了它三年"),
  mq02: await idxOf("Writing evals"),
  mq03: await idxOf("biggest fallacies"),
  mq04: await idxOf("围栏不是拦住它"),
  mq05: await idxOf("没有撤回键。"),
  p31:  await idxOf("两道围栏：提示词拦话术"),
  p44:  await idxOf("从分清单向门与双向门开始"),
};
chk(Object.values(P19).every((i) => i >= 0), `R19 · 八个目标页全部按内容找到 ${JSON.stringify(P19)}`);
const slides19 = await pg.evaluate(() =>
  window.deck.slides.map((s) => s.outerHTML.replace(/data:image\/[a-z+]+;base64,[A-Za-z0-9+/=]+/g, "")).join(""));
// 负向：被删/被换的整段必须查无此句
const cut19 = ["三条赛道量级差百倍",                                       // ① 被点名删掉的那句
               'class="col ', 'class="pr"',                                // ① 三格柱与表头线
               ">2026 Q1 · 截至 3-31<", ">2026 上半年 · 截至 7-02<",       // ① 三格各自的截点行
               "观点页 · 嘉宾金句",                                        // ② 编号 eyebrow
               "Kevin Weil · OpenAI 前 CPO",                               // ③ 旧署名
               "高敏权限不能只靠提示词和策略文档约束",                      // ④ 教训 01 正文
               "容器、沙箱、权限边界、人工升级通道",                        // ④ 教训 02 正文
               "授权不能只活在代码里", "这六件事，第四幕会变成组织的授权语法", // ④ 教训 03 正文
               "也必须在纸上",                                              // ④ 教训 03 旧标题
               "这条线画在哪 —— 是 CEO 的活", 'class="dcap'];              // ⑤ P44 那行
chk(cut19.every((k) => !slides19.includes(k)),
    `R19 · 被删/被换的整段全部清零（残留 ${JSON.stringify(cut19.filter((k) => slides19.includes(k)))}）`);
// ① P7：零第二把尺（红线）+ 对数刻度标注 + 十倍阶梯网格 + 三条曲线 + 数据一个不动
const s19p7 = await secOf(P19.p7);
chk(['>基础模型 $B</text>', ">Coding / 对话式 $B</text>", "左右两轴量级不同",
     'id="r14conv"', 'x="1218"'].every((k) => !s19p7.includes(k)),
    "R19-① 红线：全场零第二把尺（双轴图元一个都没回来）");
chk(s19p7.includes(">纵轴 · 对数刻度</text>") &&
    s19p7.includes('d="M250 200 H1180 M250 300 H1180 M250 400 H1180 M250 500 H1180"') &&
    [">$100B</text>", ">$10B</text>", ">$1B</text>", ">$0.1B</text>"]
      .every((k) => (s19p7.match(new RegExp(k.replace(/[$.]/g, "\\$&"), "g")) || []).length === 1),
    "R19-① 对数刻度：角落小字 + 十倍阶梯网格四条并逐条标出（点标即刻度）");
chk(["fnd", "cod", "cnv"].every((c) =>
      (s19p7.match(new RegExp(`class="ln ${c} dw"`, "g")) || []).length === 1 &&
      (s19p7.match(new RegExp(`class="dot ${c} pop"`, "g")) || []).length === 3 &&
      (s19p7.match(new RegExp(`class="lead ${c}"`, "g")) || []).length === 1),
    "R19-① 三条曲线各一条 / 各三个节点 / 各一条终点名牌引线");
chk((s19p7.match(/class="lbl yr"/g) || []).length === 3 &&
    (s19p7.match(/>至今<\/text>/g) || []).length === 1 &&
    s19p7.includes("2026 至今：基础模型截至 3-31（Q1）· 写代码与对话式截至 7-02（H1）"),
    "R19-① 共享单一时间轴（三个年份刻度 + 一个「至今」）+ 三条线各自截点合并成一行说明");
chk([">$31.4B</text>", ">$88.9B</text>", ">$178B</text>", ">$3.3B</text>", ">$0.2B</text>",
     ">$1.6B</text>", ">$1.9B</text>", ">$1.8B</text>"]
      .every((k) => (s19p7.match(new RegExp(k.replace(/[$.]/g, "\\$&"), "g")) || []).length === 1) &&
    s19p7.includes("写代码与对话式，2024 从同一点出发"),
    "R19-① 数据一个不动：三序列九个数在位（2024 两条重合成一点，$1.6B 只标一次并注明）");
chk(["一个季度，就是去年一整年的两倍", "一轮钱在 2025 发完 · Cursor 一家占 98%",
     "半年，已经追平去年一整年"].every((k) => s19p7.includes(k)) &&
    s19p7.includes(">口径：一级市场披露融资额 · $B</text>") &&
    s19p7.includes('<div class="foot flow rev" style="--i:9">Source · New Market Pitch · Crunchbase News · TechCrunch · CNBC</div>'),
    "R19-① R16 三条叙事注转成曲线旁 callout 一字未改 + 口径行 / Source foot 原样");
chk(/class="slide[^"]*\br19money\b/.test(html) && html.includes(".r19money "),
    "R19-① 档位类 r19money 挂上且在 CSS 里有定义");
// 曲线故事红利：对数轴上「写代码 2025 冲顶后跳水」与「对话式 2026 反超写代码」两个动作要可读
const cross19 = await pg.evaluate(async (k) => {
  window.deck.go(k);
  await new Promise((r) => setTimeout(r, 400));
  const s = window.deck.slides[k];
  s.querySelectorAll('[data-step="1"]').forEach((e) => e.classList.add("on"));
  await new Promise((r) => setTimeout(r, 2000));
  const at = (cls, i) => {
    const d = [...s.querySelectorAll(`circle.dot.${cls}`)][i].getBoundingClientRect();
    return d.top + d.height / 2;
  };
  // y 越小越高。2025：写代码在对话式**之上**；2026：反过来
  return { cod25: at("cod", 1), cnv25: at("cnv", 1), cod26: at("cod", 2), cnv26: at("cnv", 2) };
}, P19.p7);
chk(cross19.cod25 < cross19.cnv25 && cross19.cod26 > cross19.cnv26 &&
    cross19.cod26 - cross19.cod25 > 80,
    `R19-① 交叉可读：2025 写代码在上 → 2026 对话式反超，且写代码跳水 ${JSON.stringify(cross19)}`);
// ② 五张金句页：eyebrow 清零 + 五张仍在（凭内容认）+ 五个档位类
chk(["我们叫了它三年 Agent（代理人）——", "Writing evals is the most important",
     "One of the biggest fallacies in AI", "围栏不是拦住它，", "没有撤回键。"]
      .every((k) => (slides19.split(k).length - 1) === 1),
    "R19-② 五张金句页仍在（凭主文认，各一处）");
chk((html.match(/class="slide[^"]*\br19mq\b/g) || []).length === 5 && html.includes(".r19mq "),
    "R19-② 五张金句页的档位类 r19mq 全挂上且有定义");
chk((slides19.match(/class="mark/g) || []).length === 1 &&
    slides19.includes("案例 01 · 真实生产环境"),
    "R19-② .mark 只剩案例 01 那一处（金句页编号已全删）");
// ③ 署名 ex CPO
chk((await secOf(P19.mq02)).includes('<div class="s rise" style="--i:5">Kevin Weil · OpenAI ex CPO</div>') &&
    (slides19.match(/Kevin Weil/g) || []).length === 1,
    "R19-③ 金句 02 署名 → OpenAI ex CPO（全场 Weil 仍仅一处）");
// ④ P31：教训卡只剩标题 + 教训 03 改题 + 悬空清零
const s19p31 = await secOf(P19.p31);
chk(!s19p31.includes('<div class="d">') &&
    (s19p31.match(/<div class="tag">教训 0/g) || []).length === 3 &&
    ['<div class="t">提示词不是围栏</div>', '<div class="t">围栏必须在架构里</div>',
     '<div class="t">也必须写进 SOP 流程里</div>'].every((k) => s19p31.includes(k)),
    "R19-④ 三张教训卡只剩标题 + 教训 03 改「也必须写进 SOP 流程里」");
chk(s19p31.includes("一句「不要」，拦不住一个已经能执行动作的主体") &&
    s19p31.includes("2026-07 · OpenAI 的公开披露") &&
    s19p31.includes("Hugging Face CEO Clem Delangue"),
    "R19-④ 链路图与 OpenAI × Hugging Face 事件块未被误伤");
chk(!slides19.includes("六件") && !slides19.includes("授权语法") && slides19.includes("授权可撤销"),
    "R19-④ 悬空清零：「六件事」全场归零且无人回指，第四幕组织侧口径未误伤");
// ⑤ P44：CEO 行清零 + 图收到 1180 + 标签仍按 % 对位到门中心
const s19p44 = await secOf(P19.p44);
chk(!s19p44.includes("dcap") && !s19p44.includes("CEO") &&
    html.includes(".r19doors .doors{max-width:1180px;}") &&
    /class="slide[^"]*\br19doors\b/.test(html),
    "R19-⑤ P44 CEO 那行清零 + 门图收到 1180");
const d19 = await pg.evaluate(async (k) => {
  window.deck.go(k);
  await new Promise((r) => setTimeout(r, 2400));
  const s = window.deck.slides[k], img = s.querySelector(".doors img"), ib = img.getBoundingClientRect();
  const dls = [...s.querySelectorAll(".doors .dl")].map((e) => {
    const b = e.getBoundingClientRect();
    return +(((b.left + b.width / 2) - ib.left) / ib.width * 100).toFixed(1);
  });
  return { w: Math.round(ib.width), h: Math.round(ib.height), dls, dec: img.naturalWidth > 0 };
}, P19.p44);
chk(d19.dec && d19.w >= 1150 && d19.w <= 1220 &&
    Math.abs(d19.dls[0] - 27.2) <= 1.2 && Math.abs(d19.dls[1] - 72.3) <= 1.2,
    `R19-⑤ 门图实测收到 1150–1220 且标签仍对位到两扇门中心 ${JSON.stringify(d19)}`);
// 逐页：零溢出 / 零 svg 文字重叠 / 零出框 / 零半截字 / 填充率 78–106% + 截图（2.4s）
const r19 = [];
for (const [name, i] of Object.entries({ p7: P19.p7, mq02: P19.mq02, p31: P19.p31, p44: P19.p44,
    mq01: P19.mq01, mq03: P19.mq03, mq04: P19.mq04, mq05: P19.mq05 })) {
  await pg.evaluate((k) => window.deck.go(k), i);
  await pg.waitForTimeout(300);
  await pg.evaluate(() => {
    const s = window.deck.slides[window.deck.i];
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
    let ratio = null;
    if (body) {
      const kids = [...body.children].filter((e) => e.offsetParent);
      const top = Math.min(...kids.map((e) => e.getBoundingClientRect().top));
      const bot = Math.max(...kids.map((e) => e.getBoundingClientRect().bottom));
      ratio = Math.round(((bot - top) / body.getBoundingClientRect().height) * 100);
    }
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
    const svg = s.querySelector("svg"), sb = svg ? svg.getBoundingClientRect() : null;
    let vbOut = 0;
    if (svg) [...svg.querySelectorAll("text")].forEach((e) => {
      const b = e.getBoundingClientRect();
      if (b.width && (b.left < sb.left - 2 || b.right > sb.right + 2 ||
                      b.top < sb.top - 2 || b.bottom > sb.bottom + 2)) vbOut++;
    });
    let clipped = 0;
    s.querySelectorAll("*").forEach((el) => {
      const cp = getComputedStyle(el).clipPath;
      if (cp && cp !== "none" && [...cp.matchAll(/([\d.]+)%/g)].some((x) => parseFloat(x[1]) > 1)) clipped++;
    });
    return { out, ratio, ov, worst, vbOut, clipped };
  });
  r19.push({ name, ...m });
  await pg.screenshot({ path: `/tmp/qa/r19-${name}.png` });
}
chk(r19.every((x) => x.out === 0 && x.ov === 0 && x.vbOut === 0 && x.clipped === 0 &&
                     (x.ratio === null || (x.ratio >= 78 && x.ratio <= 106))),
    `R19 · 八页零溢出 / 零 svg 文字重叠 / 零出框 / 零半截字 / 填充率 78–106% ${JSON.stringify(r19)}`);

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
