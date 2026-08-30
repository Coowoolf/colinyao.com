#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-postloan-en.py ·《AI-Powered Post-Loan Collections》15 页 · **私享**
#   = /convoai-postloan 的**东南亚英文版**（SEA EDITION）。
#   从 build-convoai-postloan.py 整体克隆：同版式骨架、同 DECK_CSS token、
#   同 conf-light·dark 背景板、同 deck.js 运行时、同五个运动原语（keyframes 名逐字复用）。
#   **不是直译，是市场重铸** —— 中国侧的三大数 / 卡量 / 部门规章 / 国标全部换成
#   东南亚一手来源的事实（见「已核事实」段），版式与图形一格不动。
#
# ── 这份 deck 是什么 ───────────────────────────────────────────────────────
#   受众：东南亚金融机构（银行 / 消费金融 / fintech 平台）的贷后、风控、合规、
#   技术负责人。首场越南，后续新加坡 / 印尼 / 泰国 / 菲律宾 / 日本 / 韩国。
#   语言：全英文（商务标准，简洁有力）。发布形态：私享链接 /convoai-postloan-en，
#   只在 deckRoutes 注册，不进任何索引数组。
#
# ── 同链路语言切换（2026-08-30 Colin 拍板）────────────────────────────────
#   两份 deck 各挂一枚常显 pill（deckSwap 同款样式体系，左下角同角、摞在主题钮之上）：
#     中文版「EN」→ /convoai-postloan-en    英文版「中文」→ /convoai-postloan
#   ⚠ 必须是 <button> + JS 跳转，**不能用 <a>** —— 两份 deck 的 a[href]=0 闸都还在。
#   ⚠ 预览服务器（8899 / 8777）是静态目录服务，没有 next.config 的 rewrites，
#     所以跳转目标按当前 pathname 是否带 .html 二选一：带 .html ⇒ /decks/xxx.html，
#     否则 ⇒ /xxx（线上路由）。这样 QA 的互跳 round-trip 才跑得起来，线上行为不变。
#
# ── 已核事实（Fable 仲裁过，逐字用；SOURCE 行写机构名，不写 URL）────────────
#   ① 越南《投资法》61/2020/QH14（2021-01-01 起施行）：debt collection services
#      列为禁止投资经营业务 ⇒ 银行与消金机构不能再把催收外包给讨债公司，
#      唯一路径是自建团队 + 技术化运营。→ P4（全 deck 的市场锚点页）
#   ② SBV Circular 18/2019/TT-NHNN（修订 Circular 43/2016 Point dd Clause 2 Article 7，
#      2020-01-01 生效）：每日 ≤5 次提醒 / 07:00–21:00 且须合同约定 /
#      不得向无还款义务的组织或个人催告 / 措施须合法且排除威胁客户的手段。→ P7
#   ③ 全球 debt collection software 市场（沿用中文版 P9 原数，天然全球口径）：
#      Fortune Business Insights 5.98B(2025) → 13.77B(2034)，CAGR 9.72%；
#      Grand View Research 4.9B(2023) → 9.3B(2030)。→ P9
#   ④ e-Conomy SEA 2025（Google / Temasek / Bain）：**只作定性引用** ——
#      digital lending 稳步增长、embedded loans 进电商与电子钱包平台驱动变现。
#      **不写任何贷款余额数字**。→ P3
#   ⑤ Agora canon（从引擎 deck 逐字取再译）：650ms end-to-end / 340ms barge-in /
#      95% environmental-interference shielding（typical values）· SAL · AI-VAD ·
#      graceful interruption · AI QoS · 90B+ minutes monthly · 200+ global nodes ·
#      SD-RTN。→ P12
#      **IDC 中国市占 No.1 不进英文版**（中国市场信任状对 SEA 听众无效且需解释成本，
#      Fable 已裁）。
#   ⑥ 2026-08-30 · Colin ③ · **仅英文版**：OpenAI 口径从「global first-batch partner」
#      改为「named an integration partner at the 2024 OpenAI Realtime API launch」——
#      后者贴 OpenAI 官方发布文可验，前者是我们的转译（官方文里没有「首批」这一层级）。
#      **中文版的家族 canon 本轮不动**（家族级口径变更待 Colin 拍板，见交付报告）。
#   ⑦ 2026-08-30 · Colin ① · vendor 生态（出处 docs.agora.io TTS overview）：
#      17+ TTS providers · Microsoft Azure / ElevenLabs / Google / Amazon Polly /
#      OpenAI / MiniMax。语种表述**限定在 vendor 侧**（"language coverage follows your
#      vendors"），不替任何一家供应商声明它支持哪一种语言。→ P12
#   ⑧ 2026-08-30 · Colin ④ · P3 规模证据带用 info 家族 P2 的两枚 canon，
#      且**避开 P12 已用过的两枚**（90B+ / 200+）：
#      「Top 10,000 RTC-integrated apps (by MAU) 里近一半跑在 Agora」+「1M+ 注册应用」。
#   ⑨ 2026-08-30 · Colin ② · 脱敏 proof point（P13 side note + P15 收尾）：
#      "A leading outbound calling deployment in China now runs 1,000,000+ calls per day."
#      口径由 Colin 给定，逐字用，两处一字不差。
#
# ── 表达红线（构建期断言 + qa 反向闸双保险）──────────────────────────────────
#   作为我方定位词，六串全文 0 出现（大小写不敏感）：
#     debt chasing / chase debtors / pressure tactics / aggressive collection /
#     harass / intimidat
#   `threaten` **只准出现一次**，且必须落在 P7 引述监管禁令的那一枚 [data-nogate] 节点里
#     （QA 断言：全文命中数 = 1 且该命中在豁免节点内）。
#   承诺比例句零出现：整份 deck 只准两个百分数 —— 95%（canon）/ 9.72%（CAGR）。
#   客户名零出现（含「光潽」）· Call Agent 产品名 / 价格 / staging / 盲测 / 32,000 全不入 ·
#   a[href] = 0 · noindex ·
#   **除左下角语言钮的「中文」二字外，全页零 CJK**（QA 纯度闸，豁免该节点）。
#
# ── 英文版的三处版式判断（替 Colin 做的，理由写在这里）────────────────────────
#   ① `--f-cn` 在本 deck 里覆盖成 **Satoshi 优先**的栈（500/700/900 三档全量内嵌）。
#      理由：这是一份要在越南现场投屏的全英文 deck，系统栈（-apple-system / Arial）
#      在 macOS / Windows / 会场借来的机器上宽度各不相同，而英文比中文长 1.6–2 倍，
#      每一处排版账都踩在溢出线上。Satoshi 是家族已内嵌的拉丁面（--f-en 一直在用），
#      内嵌后「我这里量到的宽度 = Colin 现场看到的宽度」。中文版一个字节不动。
#   ② `.hh` 主标从 68px 降到 60px。理由：68px 下 1680px 盒只放得下约 47 个拉丁字符，
#      英文标题写不进去；60px 放得下约 62 个。**本 deck 所有主标一律单行 ≤ 58 字符**
#      （留 8% 余量），QA 有一条 .hh 单行闸（scrollHeight ≤ 80）钉死它。
#   ③ legend() 的标签步进系数从 13.2（CJK 宽度）改到 6.6（拉丁宽度）——
#      不改的话三型图例会散开成一条横穿整页的稀疏虚线。
#
# ── 家族硬指标（与中文版逐条同源）─────────────────────────────────────────
#   · 五运动原语（mo-packet / mo-drift / mo-cycle / mo-pulse / mo-breathe + mo-halo）
#     keyframes 名逐字复用，不新造。
#   · 浅色默认，双主题齐备，deckSwap 常显 chip（英文版按钮文案 DARK / LIGHT）。
#   · .slide:not(.active) 暂停 / prefers-reduced-motion / print 三路关断。
#   · **全 deck 零分步**（data-steps 全 0、页内一枚 [data-step] 都没有）。
#   · 每页至多一枚 .mo-breathe（唯一 hot 件）。
#   · SOURCE ledger 英文四段制：`SOURCE · <机构> · <样本或时间窗> · Facts as of 2026.08`
#
# 结构（15 页；★ = 相对中文版**重铸**的三页）：
#   P1  Cover                          P2  Overview · five-link chain
#   P3  ★ SEA lending boom             P4  ★ Vietnam · the market anchor
#   P5  Value chain · eight stages（**标杆动效页**）
#   P6  Core tension                   P7  ★ Regulatory spec（**第二杀手页**）
#   P8  Five trends                    P9  Market sizing · three layers
#   P10 Why AI                         P11 Capability loop（**第二动效重点**）
#   P12 Why Agora                      P13 Rollout        P14 Pilot KPI
#   P15 Closing
#
# 重建：python3 scripts/build-convoai-postloan-en.py
# 自检：node scripts/qa-convoai-postloan-en.mjs（THEME=dark 二跑）
#      DECK=postloan-en node scripts/qa-motion.mjs
#      DECK_URL=…/convoai-postloan-en.html node scripts/occlusion-scan.mjs（双分辨率 × 双主题）
#      A=…/convoai-postloan-en.html SELFPIN=1 node scripts/pinned-diff.mjs
#
# ── 踩过的坑（与母版同一份，移植 SVG 必守）─────────────────────────────────
#   · svg 一律 style="width:100%;height:auto"，.sh 高度 = width×viewBoxH/viewBoxW
#   · SVG 里换色一律写内联 style="fill:…"（呈现属性压不过 .fig .lbl/.ttl 的 CSS fill）
#   · .dw 的 --len 必须≈路径长度；虚线不能走 .dw（dasharray 会被压掉）⇒ 一律 dline()
#   · content 背景板自带一条 accent 细线在 y848–852：那一带不放文字，rule(850) 压住它
#   · 网格（.g2/.g3/.g4/.g5）一律写 height:100%，否则卡片溢出 .sh 盒 → TEXT-x-SPILL
# ═══════════════════════════════════════════════════════════════════════════
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
OUT = ROOT / "public" / "decks" / "convoai-postloan-en.html"
B = "/decks/assets/conf-boards/"

def css(name):
    return (SRC / name).read_text(encoding="utf-8")

# Satoshi 三档全量内嵌（500 是本 deck 新加的：正文 font-weight:300 会落到它身上）
FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>"""

BOARDS_CSS = """<style id="convoai-boards">
.conf-bg{position:absolute;inset:0;z-index:0;pointer-events:none;background-repeat:no-repeat;
  background-position:center;background-size:cover;opacity:var(--conf-bg-opacity,.58);}
.slide.conf-boarded{background:transparent!important;}
.slide.conf-boarded>.pp{z-index:1;}
.conf-bg-title{--conf-bg-opacity:.66;background-image:url('%(B)stitle-02-orbit-light.png');}
.conf-bg-content{--conf-bg-opacity:.42;background-image:url('%(B)scontent-01-matrix-light.png');}
html[data-theme="dark"] .conf-bg-title{background-image:url('%(B)stitle-02-orbit-dark.png');}
html[data-theme="dark"] .conf-bg-content{background-image:url('%(B)scontent-01-matrix-dark.png');}
html[data-theme="dark"] .conf-bg{filter:saturate(.92);}
</style>""" % {"B": B}

DECK_CSS = """<style id="convoai-postloan-en-deck">
/* ── 英文版判断 ①：全 deck 文字栈换成 Satoshi 优先（见文件头）───────────────
   --f-cn 是家族所有正文 / 标题 / 卡片的字体变量；这里在 :root 上重定义一次，
   同特指度、后来居上，两个主题一起覆盖（dark 块里本来就没有再定义它）。 */
:root{--f-cn:'Satoshi',-apple-system,'Helvetica Neue',Arial,'Noto Sans SC',sans-serif;}
/* 绝对画布 shape 层（robot26 惯例；reference 栈是语义排版系，缺这两行） */
.pp{position:absolute;inset:0;}
.pp .sh{position:absolute;overflow:visible;}
/* conf 家族 token 表里没有 --on-bg，components.css 的 .card.on 靠它上底色 */
:root{--on-bg:linear-gradient(180deg,color-mix(in srgb,var(--accent) 13%,transparent),
    color-mix(in srgb,var(--accent) 3%,transparent)),var(--card-bg);
  --warn-bg:linear-gradient(180deg,color-mix(in srgb,var(--coral) 10%,transparent),
    color-mix(in srgb,var(--coral) 2.5%,transparent)),var(--card-bg);}
html[data-theme="dark"]{--on-bg:linear-gradient(180deg,color-mix(in srgb,var(--accent) 9%,transparent),
    color-mix(in srgb,var(--accent) 2%,transparent)),var(--card-bg);
  --warn-bg:linear-gradient(180deg,color-mix(in srgb,var(--coral) 9%,transparent),
    color-mix(in srgb,var(--coral) 2%,transparent)),var(--card-bg);}
.card .tag.am{color:var(--accent);}
/* 投影可读性（与中文版逐字同源）：色阶只能走 color，不许用 opacity */
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 17px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--ink-3);}
.src{font:500 17px/1.4 var(--f-mono);letter-spacing:.08em;
  color:color-mix(in srgb,var(--ink-2) 55%,var(--ink-3));}
/* 版式件（与中文版同源；.hh 见文件头判断 ②：68 → 60，英文标题一律单行 ≤ 58 字符） */
.kk{font:700 20px/1 var(--f-mono);letter-spacing:.28em;color:var(--accent);}
/* ⚠ 行高 1.32 不是随手写的（英文版专属，中文版是 1.16）：.ink 的液态扫过用的是
   `mask-size:300% 100%`，mask 高度 = 元素盒高度 ⇒ **任何伸出行盒的字形都会被切掉**。
   Satoshi 的 ascent+descent ≈ 1.25em，行高 1.2 时半行距为负，大写字母顶部伸出行盒
   约 1.5px，1280 视口的 occlusion 扫描当场报 15 条 CLIPPED（每页主标各一条）。
   1.32 给出 +0.035em 的正半行距，字形完整落在盒内；行盒 79.2px 仍在 .sh 的 90px 之内。
   **改字号或改行高之前先重算这一笔。** */
.hh{font:700 60px/1.32 var(--f-cn);letter-spacing:-.018em;color:var(--ink);}
.hh strong{color:var(--accent);}
.sub{font:400 26px/1.55 var(--f-cn);color:var(--ink-2);}
.mono-sm{font:500 15px/1.4 var(--f-mono);letter-spacing:.08em;color:var(--ink-3);}
.card-c{background:var(--card-bg);border:1px solid var(--hair);border-radius:20px;}
.card-c.on{border-color:color-mix(in srgb,var(--accent) 52%,transparent);}
/* Infograph 分区件：mono 小节标 + 1px 分隔细线 */
.seclab{font:500 14px/20px var(--f-mono);letter-spacing:.18em;color:var(--ink-3);}
.seclab b{font-weight:700;color:var(--ink-3);}
.hair-rule{background:var(--hair);}
/* 主题词 chip */
.chip{display:inline-block;margin:0 12px 12px 0;padding:11px 18px;border:1px solid var(--hair);
  border-radius:999px;background:var(--card-bg);font:500 18px/1 var(--f-cn);color:var(--ink-2);}
.chip.on{border-color:color-mix(in srgb,var(--accent) 52%,transparent);color:var(--accent);}
/* .fig 内的 SVG 走 width:100%;height:auto，必须解掉 stage.css 的 svg{max-*:100%} */
.fig svg{max-width:none;max-height:none;}
.on-dark b,.on-dark strong{color:inherit;}
/* ══ deck 级运动语言 · 五个运动原语（从中文版逐字复用，不新造 keyframes 名）════
     ① .mo-packet  能量包 —— 纯装饰件 ⇒ 静态语域直接 display:none
     ② .mo-drift   虚线漂移 —— 载体是页面真线 ⇒ 静态语域只 animation:none
     ③ .mo-pulse   脉冲 —— 载体自带 opacity 时必须把 --mo-hi 设成它的静态值
     ④ .mo-breathe hot 件呼吸 —— **每页至多一处**；伴件 .mo-halo 100% 帧 opacity:0
     ⑤ .mo-cycle   闭环绕行 —— 环 / 回路上的 dash 永续绕圈（P5 八环 / P11 回流弧）
   纪律（硬红线，四条）：100% 帧 = 静态原图（自证工具 pinned-diff.mjs SELFPIN=1）/
   动效元素不携带文字 / reduced-motion 与 print 全关 / 非当前页 paused。 */
@keyframes moFlow{to{stroke-dashoffset:var(--mo-off,-200);}}
@keyframes moPulse{0%,100%{opacity:var(--mo-hi,1);}45%{opacity:var(--mo-lo,.35);}}
@keyframes moBreathe{0%,100%{transform:scale(1);}50%{transform:scale(var(--mo-sc,1.03));}}
@keyframes moHalo{0%{opacity:0;transform:scale(1);}30%{opacity:var(--mo-op,.4);}
  100%{opacity:0;transform:scale(var(--mo-sc,1.46));}}
.mo-packet{animation:moFlow var(--mo-dur,1.8s) linear infinite var(--mo-del,0s);}
.mo-drift{animation:moFlow var(--mo-dur,3.4s) linear infinite var(--mo-del,0s);}
.mo-cycle{animation:moFlow var(--mo-dur,9s) linear infinite var(--mo-del,0s);}
.mo-pulse{animation:moPulse var(--mo-dur,2.4s) ease-in-out infinite var(--mo-del,0s);}
.mo-breathe{animation:moBreathe var(--mo-dur,3.2s) ease-in-out infinite var(--mo-del,0s);
  transform-box:fill-box;transform-origin:center;}
.mo-halo{opacity:0;animation:moHalo var(--mo-dur,3.2s) ease-out infinite var(--mo-del,0s);
  transform-box:fill-box;transform-origin:center;}
@media print{
  .mo-packet,.mo-halo,.mo-ghost{display:none!important;}
  .mo-drift,.mo-cycle,.mo-pulse,.mo-breathe{animation:none!important;}}
@media (prefers-reduced-motion:reduce){
  .mo-packet,.mo-halo,.mo-ghost{display:none!important;}
  .mo-drift,.mo-cycle,.mo-pulse,.mo-breathe{animation:none!important;}}
.slide:not(.active) .mo-packet,.slide:not(.active) .mo-drift,.slide:not(.active) .mo-cycle,
.slide:not(.active) .mo-pulse,.slide:not(.active) .mo-breathe,.slide:not(.active) .mo-halo{
  animation-play-state:paused;}
/* ── P10 七行对比表：8 行（1 表头 + 7 行）必须落进 rule(850) 以上的 300px 盒里 ────
   ⚠ 选择器必须写成 `table.mini.ai-diff`（0,2,3）：components.css 里的
     `table.mini tbody td`（0,1,3）比裸 `.ai-diff tbody td`（0,1,2）**更特指**。
   版式账：th ≈ 13×1.2 + 8 + 1 = 25；td = 8+8 + 17×1.3 + 1 = 39.1；
     25 + 7×39.1 = 299 ⇒ 落进 300 的盒。**加一行必须重算这一笔。** */
table.mini.ai-diff tbody td{padding:8px 14px 8px 0;font-size:17px;line-height:1.3;}
table.mini.ai-diff thead th{font-size:13px;padding-bottom:8px;}
table.mini.ai-diff tbody td:last-child,table.mini.ai-diff thead th:last-child{
  background:color-mix(in srgb,var(--accent) 7%,transparent);padding-left:22px;}
table.mini.ai-diff thead th:last-child{color:var(--accent);}
/* ── P14 五类指标卡：与 P8 的五趋势卡同为 .g5，靠**大号序号**区分语域 ─────────── */
.kpi .n{font-size:34px;}
.kpi .t{font-size:25px;}
.kpi .m{font:400 18px/1.95 var(--f-cn);color:var(--ink-2);}
/* ══ 2026-08-30 修订 · 三件「注解语汇」（判断标 / 口径行 / 页脚注带）════════════
   与中文版逐字同源（同类名、同尺寸、同色阶），只有 .scope.tight 这一档是英文版专属：
   拉丁比中文长 1.6–2 倍，P12 那条供应商名单在 16px 下量到 1753px > 1680 的可用宽，
   收到 14px（1534px）才落得进一行 —— 这是本 deck 一贯的「英文版重算版式账」。 */
.vtag{display:inline-block;padding:3px 10px;border-radius:3px;
  border:1px solid color-mix(in srgb,var(--accent) 34%,transparent);
  background:color-mix(in srgb,var(--accent) 6%,transparent);
  font:500 12px/1.2 var(--f-mono);letter-spacing:.16em;
  color:color-mix(in srgb,var(--accent) 78%,var(--ink-2));}
.scope{font:400 16px/1.35 var(--f-cn);color:var(--ink-3);}
.scope b{font-weight:700;color:var(--ink-2);}
.scope::before{content:"";display:inline-block;width:14px;height:1px;margin-right:10px;
  vertical-align:middle;background:color-mix(in srgb,var(--accent) 60%,transparent);}
.scope.tight{font-size:14px;line-height:1.3;}
.fnote{height:100%;display:flex;flex-direction:column;justify-content:center;gap:8px;
  padding:0 24px;border-radius:10px;
  border:1px dashed color-mix(in srgb,var(--accent) 30%,transparent);
  background:color-mix(in srgb,var(--accent) 4%,transparent);}
.fnote .h{font:500 12px/1.35 var(--f-mono);letter-spacing:.16em;color:var(--ink-3);}
.fnote .b{font:400 19px/1.4 var(--f-cn);color:var(--ink-2);}
.fnote .b b{font-weight:700;color:var(--ink);}
.fnote.on{border-style:solid;border-color:color-mix(in srgb,var(--accent) 52%,transparent);
  background:var(--on-bg);}
.fnote.on .h{color:var(--accent);}
.fnote.on .b b{color:var(--accent);}
.pfline{font:500 22px/1.4 var(--f-cn);color:var(--ink-2);}
.pfline b{font-weight:700;color:var(--accent);}
/* ── 四枚等宽 mono 项的页脚带（P13 试点建议 / P7 区域监管条共用）─────────────── */
.adv{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;height:100%;}
.adv > div{border-left:2px solid color-mix(in srgb,var(--accent) 46%,transparent);
  padding-left:16px;display:flex;flex-direction:column;justify-content:center;gap:7px;}
.adv .h{font:500 13px/1 var(--f-mono);letter-spacing:.16em;color:var(--ink-3);}
.adv .b{font:400 19px/1.4 var(--f-cn);color:var(--ink-2);}
.adv .b b{font-weight:700;color:var(--ink);}
/* ── P7 监管规格卡：四枚 spec 格（2×2）───────────────────────────────────────
   版式账（卡高 428 · padding 28 · 抬头 114.7）：格高 ≤ 121.6 ⇒
   12(mono) + 8 + 21×1.3 + 8 + 正文 ≤ 121.6 ⇒ 正文 ≤ 66px ⇒ **至多两行**。 */
.spec{display:grid;grid-template-columns:1fr 1fr;gap:14px;flex:1;align-content:space-between;}
.spec > div{border-left:2px solid color-mix(in srgb,var(--accent) 46%,transparent);
  padding-left:12px;}
.spec .h{font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);}
.spec .v{margin-top:8px;font:700 21px/1.3 var(--f-cn);color:var(--accent);}
.spec .s{margin-top:8px;font:400 16px/1.4 var(--f-cn);color:var(--ink-2);}
/* 编辑热区（deck.js 依赖） */
.edit-hotzone{position:fixed;top:0;left:0;width:120px;height:80px;z-index:10000;}
.edit-toggle{position:fixed;top:18px;left:18px;z-index:10001;opacity:0;pointer-events:none;
  font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);
  border:1px solid var(--hair);border-radius:3px;padding:7px 12px;background:transparent;cursor:pointer;
  transition:opacity .3s;}
.edit-toggle.show,.edit-toggle.active{opacity:1;pointer-events:auto;}
.edit-toggle.active{border-color:var(--accent);color:var(--accent);}
@media print{.edit-toggle,.edit-hotzone,.deck-progress,.deck-steps,.deck-swap,.deck-lang{display:none!important;}}
</style>"""

# ── 组装件（与母版同签名）────────────────────────────────────────────────────
def sh(cls, style, body, sid=None):
    """本 deck **零分步** ⇒ 这只 helper 刻意不带 step 形参。"""
    a = ' data-sid="%s"' % sid if sid else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (cls, a, style, body)

def rule(y, x=120, w=1680, i=1):
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:%dpx;height:1px;--i:%d" % (x, y, w, i), "")

def vrule(x, y, h, i=1):
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:1px;height:%dpx;--i:%d" % (x, y, h, i), "")

def lab(x, y, t, w=680, col=None, i=0):
    c = ";color:%s" % col if col else ""
    return sh("flow seclab", "left:%dpx;top:%dpx;width:%dpx;height:20px;--i:%d%s" % (x, y, w, i, c), t)

def figbox(x, y, w, vbw, vbh, inner, cls="flow", i=0):
    h = round(w * vbh / vbw)
    return sh(cls, "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (x, y, w, h, i),
              '<div class="fig"><svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg></div>'
              % (vbw, vbh, inner))

def head(kicker, title, kw=1680):
    """每页统一的页眉：kicker y92 / 标题 y148 起（家族版式纪律）。
       ⚠ 英文主标一律**单行 ≤ 58 字符**：60px 下 1680px 盒约放 62 字符，
         写到 2 行会顶穿 y238 撞到 seclab（QA 有 .hh 单行闸）。"""
    return (sh("flow kk", "left:120px;top:92px;width:%dpx;height:28px" % kw, kicker)
            + sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", title))

def land(t, y=988, x=120, w=1680, i=6):
    return sh("flow", "left:%dpx;top:%dpx;width:%dpx;height:70px;--i:%d" % (x, y, w, i),
              '<div class="land">%s</div>' % t)

def rail(t, y=988):
    return sh("flow mono-sm", "left:120px;top:%dpx;width:1680px;height:24px;--i:7" % y, t)

def src(t, y=1015, x=120, w=1680, i=7, align=None):
    """SOURCE ledger 行。英文版四段：SOURCE · <机构> · <样本或时间窗> · Facts as of 2026.08
       **来源写机构名，不写 URL** —— 投屏上没人读得出 URL，且会诱发点击。"""
    a = ";text-align:%s" % align if align else ""
    return sh("flow src", "left:%dpx;top:%dpx;width:%dpx;height:24px;--i:%d%s" % (x, y, w, i, a), t)

# ── 2026-08-30 修订集的三只件（与中文版同签名同语义，文案换英文）──────────────
def viewtag(y, t="AGORA VIEW", x=1360, w=440, i=0):
    """判断标：给**趋势断言**加一枚小标（P2 / P8 / P10）。标题主句保留，
       但页面上必须有一处告诉客户「这句是我们的看法，不是可验证事实」。"""
    return sh("flow", "left:%dpx;top:%dpx;width:%dpx;height:24px;--i:%d;text-align:right"
              % (x, y, w, i), '<span class="vtag">%s</span>' % t)

def scopenote(y, t, x=120, w=1680, i=5, cls="", h=24, nogate=None):
    """口径限定行：钉在数据件 / 法条件正下方。
       ledger 回答「哪来的」，口径行回答「适用到哪儿、不能推成什么」。
       nogate="vendor"：P12 的 TTS 供应商名单挂这一枚（qa 的客户名反向闸整枝跳过它 ——
       名单里是**我们接入的供应商**，不是客户案例；豁免只放这一枚节点）。"""
    ng = ' data-nogate="%s"' % nogate if nogate else ""
    return sh("flow scope%s" % ((" " + cls) if cls else ""),
              "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (x, y, w, h, i),
              ('<span%s>%s</span>' % (ng, t)) if ng else t)

def fnote(x, y, w, h, hd, body, on=False, i=8):
    """页脚注带：收口线之下、落点句之上。细虚线 = 要求框架 / 补充条款；
       .on 实线 accent = 证据件（P13 的脱敏 proof point）。"""
    return sh("flow", "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (x, y, w, h, i),
              '<div class="fnote%s"><div class="h">%s</div><div class="b">%s</div></div>'
              % (" on" if on else "", hd, body))

# ── SOURCE ledger 常量（同一份出处出现在多页时只写一次，防两页各自漂移）────────
# 2026-08-30：P3 加了一条「already at scale on Agora」证据带（两枚 info 家族 canon），
#   所以这一行的来源段里必须同时出现 Agora website / IR —— 一页两种出处，ledger 要写全。
#   ⚠ 版式账：.src 是 17px mono + .08em，1680px 的盒里放得下约 145 个字符。
#     第一版写成「Agora website & public IR disclosure」量到 1861px 当场折行、
#     第二行被画布下缘切掉半行（截图实锤）——「public … disclosure」收成「IR」，
#     「lending balances」收成「loan balances」，量到 1629px 才落定。
_SRC_SEA = ("SOURCE &#183; Google, Temasek &amp; Bain e-Conomy SEA 2025 / Agora website "
            "&amp; IR &#183; qualitative reference, no loan balances cited "
            "&#183; Facts as of 2026.08")
_SRC_VN = ("SOURCE &#183; National Assembly of Vietnam, Law on Investment No. 61/2020/QH14 &#183; "
           "effective 01.01.2021 &#183; Facts as of 2026.08")
_SRC_SBV = ("SOURCE &#183; State Bank of Vietnam Circular No. 18/2019/TT-NHNN &#183; "
            "amends Circular 43/2016, effective 01.01.2020 &#183; Facts as of 2026.08")
_SRC_MKT = ("SOURCE &#183; Fortune Business Insights / Grand View Research &#183; "
            "Debt Collection Software 2025&#8594;2034 / 2023&#8594;2030 &#183; Facts as of 2026.08")
# 2026-08-30 补 Agora docs：P12 的 17+ 家 TTS 供应商名单出自 docs.agora.io 的
#   TTS overview，与官网 / 发版说明不是同一份材料，来源段里必须写出来。
_SRC_AGORA = ("SOURCE &#183; Agora website / Agora docs / engine release notes / public IR "
              "disclosure &#183; typical values &#183; Facts as of 2026.08")
# 2026-08-30 新增：P13 的脱敏 proof point。生产部署口径的外部事实 ⇒ 自带一行 ledger
#   （P13 因此成为第六张数据页）。
_SRC_PROOF = ("SOURCE &#183; Agora production deployment (anonymized) &#183; "
              "daily call volume &#183; Facts as of 2026.08")

# ── SVG 小件（与母版同签名）──────────────────────────────────────────────────
def ah_r(x, y, col, s=9):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x - s - 2, y - 6, x - s - 2, y + 6)

def ah_l(x, y, col, s=9):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x + s + 2, y - 6, x + s + 2, y + 6)

def ah_d(x, y, col, s=9):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x - 6, y - s - 2, x + 6, y - s - 2)

def ah_u(x, y, col, s=9):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x - 6, y + s + 2, x + 6, y + s + 2)

#   ⚠ hline / vline **不接受 dash**：它们走 .dw，而 motion.css 的
#     `.dw{stroke-dasharray:var(--len)}` 会把 dasharray 属性整条压掉。要虚线一律走 dline()。
def hline(x1, x2, y, col="var(--hair-strong)", w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d H%d" '
            'stroke="%s" stroke-width="%s" fill="none"/>' % (abs(x2 - x1), i, x1, y, x2, col, w))

def vline(x, y1, y2, col="var(--hair-strong)", w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d V%d" '
            'stroke="%s" stroke-width="%s" fill="none"/>' % (abs(y2 - y1), i, x, y1, y2, col, w))

def dline(d, col="var(--hair-strong)", w=2, i=1, dash="7 7", cls="", sty=""):
    return ('<path class="pop%s" style="--i:%d%s" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-dasharray="%s"/>'
            % ((" " + cls) if cls else "", i, (";" + sty) if sty else "", d, col, w, dash))

def pline(d, col="var(--hair-strong)", w=2, i=1, ln=None):
    return ('<path class="dw" style="--len:%d;--i:%d" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none"/>' % (int(ln or 1200), i, d, col, w))

def packet(d, ln, col=None, w=11, seg=24, dur="1.8s", op=".3", i=2, rev=False, delay=None,
           cls="", cap="round"):
    per = seg + int(ln)
    v = "--mo-off:%d;--mo-dur:%s" % (per if rev else -per, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<path class="pop mo-packet%s" style="--i:%d;%s" d="%s" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-opacity="%s" stroke-linecap="%s" stroke-dasharray="%d %d"/>'
            % ((" " + cls) if cls else "", i, v, d, col or AC, w, op, cap, seg, int(ln)))

def box(x, y, w, h, r=4, hot=False, dashed=False, i=0, cls="", sty=""):
    d = ' stroke-dasharray="7 6"' if dashed else ""
    c = (" " + cls) if cls else ""
    v = (";" + sty) if sty else ""
    if hot:
        return ('<rect class="pop%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
                'fill="none" stroke="var(--accent)" stroke-width="2.5"%s/>' % (c, i, v, x, y, w, h, r, d))
    return ('<rect class="pop box%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'stroke-width="1.4"%s/>' % (c, i, v, x, y, w, h, r, d))

def pulse_dot(x, y, r=7, col=None, lo=".2", hi=None, dur="2.4s", delay=None, i=3):
    v = "--i:%d;--mo-lo:%s;--mo-dur:%s" % (i, lo, dur)
    if hi:   v += ";--mo-hi:%s" % hi
    if delay: v += ";--mo-del:%s" % delay
    return ('<circle class="pop mo-pulse" style="%s;fill:%s%s" cx="%d" cy="%d" r="%d"/>'
            % (v, col or AC, (";opacity:%s" % hi) if hi else "", x, y, r))

def halo_rect(x, y, w, h, r=8, col=None, sc="1.06", op=".34", dur="3.6s", delay=None):
    v = "--mo-sc:%s;--mo-op:%s;--mo-dur:%s" % (sc, op, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<rect class="mo-halo" style="%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'fill="none" stroke="%s" stroke-width="2.5" opacity="0"/>' % (v, x, y, w, h, r, col or AC))

def txt(x, y, s, cls="txt", size=None, anchor=None, col=None, weight=None, i=None,
        mono=False, ls=None, sty=None):
    st = []
    if sty:    st.append(sty)
    if size:   st.append("font-size:%dpx" % size)
    if col:    st.append("fill:%s" % col)
    if weight: st.append("font-weight:%d" % weight)
    if mono:   st.append("font-family:var(--f-mono)")
    if ls is not None: st.append("letter-spacing:%s" % ls)
    a = ' text-anchor="%s"' % anchor if anchor else ""
    g = ' class="%s"' % cls if cls else ""
    sty2 = ' style="%s"' % ";".join(st) if st else ""
    return '<text%s x="%d" y="%d"%s%s>%s</text>' % (g, x, y, a, sty2, s)

PAGES = []          # (board, body_html) —— 本 deck 零分步，故不带 steps 位
def page(board, body):
    PAGES.append((board, body))

AC = "var(--accent)"
AD = "var(--accent-deep)"
HS = "var(--hair-strong)"
I3 = "var(--ink-3)"

# ── deck 级线型系统（与中文版逐字同源）────────────────────────────────────────
#   实线 accent = 业务主流程 / 主数据流；虚线 hair-strong = 事件 / 控制；
#   点线 accent-deep = 反馈 / 回流。每张图底部一行 mono 迷你图例，只列该页真用到的线型。
def lg_solid(x, y, col=AC, w=2.5, i=9):
    return hline(x, x + 40, y, col, w, i)
def lg_dash(x, y, col=HS, w=2, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="6 5")
def lg_dot(x, y, col=AD, w=2.4, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="2 6")
def lg_fast(x, y, col=AD, w=5, i=9):
    return hline(x, x + 40, y, col, w, i)
_LGK = {"solid": lg_solid, "dash": lg_dash, "dot": lg_dot, "fast": lg_fast}

# 英文版判断 ③：步进系数 13.2（CJK）→ 6.6（拉丁）——不改的话图例会散成一条稀疏虚线
_LG_CW = 6.6
def legend(x, y, items, i=9, gap=54):
    o, cx = [], x
    for it in items:
        kind, label = it[0], it[1]
        w = it[2] if len(it) > 2 else None
        col = it[3] if len(it) > 3 else None
        if kind == "fill":
            o.append('<rect class="pop" style="--i:%d;fill:%s;opacity:.25" x="%d" y="%d" '
                     'width="40" height="13" rx="3"/>' % (i, col or AC, cx, y - 6))
        else:
            kw = {"i": i}
            if w is not None: kw["w"] = w
            if col is not None: kw["col"] = col
            o.append(_LGK[kind](cx, y, **kw))
        o.append(txt(cx + 50, y + 5, label, "sm", size=14, i=i))
        cx += 50 + int(len(label) * _LG_CW) + gap
    return "".join(o)

def domain_band(x, y, w, h, label, i=1, r=14):
    """域分带：一块极淡的 accent 底 + 一枚 mono 域名。"""
    return ('<rect class="pop" style="--i:%d;fill:color-mix(in srgb,var(--accent) 6%%,transparent);'
            'stroke:color-mix(in srgb,var(--accent) 22%%,transparent);stroke-width:1.2" '
            'x="%d" y="%d" width="%d" height="%d" rx="%d"/>' % (i, x, y, w, h, r)
            + txt(x + 18, y + 26, label, "sm", size=14, col=I3, mono=True, ls=".16em", i=i))


# ═══ P1 · Cover（title 板）═════════════════════════════════════════════════
#   视觉纪律（与中文版同）：金融科技风格，**避免任何负面视觉表达** ——
#   封面上没有箭头、没有下行曲线、没有任何「压」的图形隐喻，
#   只有家族标准的 accent 短棒 + 关键词 chip 行。
#   版式账：主标 72px 双行（"AI-Powered Post-Loan Collections" 在 Satoshi 700 下
#   量得 15.92em ⇒ ×72 = 1146px < 盒宽 1560；第二行 14.14em ⇒ 1018px），
#   行盒 72×1.28 = 92.2，双行 184px ⇒ 落进 y270 起的 190px 盒，与 y470 的 accent 棒不打架。
#   （1.28 而不是 1.16：.ink 的 mask 高度 = 元素盒高度，Satoshi 的字形高约 1.25em，
#    行高低于它时大写字母顶部会被 mask 切掉一线 —— 见 DECK_CSS 里 .hh 那一段的长注。）
page("title", "".join([
    # 2026-08-30：kicker 补锚点市场 —— 这一版的事实骨架（61/2020/QH14 · 18/2019/TT-NHNN）
    # 全部是越南一手来源，封面上写清楚 VIETNAM ANCHOR，客户拿到新加坡 / 印尼场的时候
    # 一眼知道哪些条款要重配。另一份是 CHINA EDITION。（量得 1056px < 盒宽 1500。）
    sh("flow kk", "left:120px;top:206px;width:1500px;height:28px",
       "AGORA &#183; POST-LOAN COLLECTIONS &#183; SEA EDITION &#183; VIETNAM ANCHOR"),
    sh("ink", "left:120px;top:270px;width:1560px;height:190px;"
       "font:700 72px/1.28 var(--f-cn);letter-spacing:-.022em;color:var(--ink)",
       "AI-Powered <strong style='color:var(--accent)'>Post-Loan Collections</strong><br>"
       "&amp; Overdue Asset Management"),
    sh("spread", "left:120px;top:470px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow sub", "left:120px;top:524px;width:1500px;height:96px;--i:4",
       "From manpower-intensive operations to compliant, traceable, "
       "scalable intelligent operations."),
    sh("flow", "left:120px;top:660px;width:1560px;height:60px;--i:5",
       "".join('<span class="chip%s">%s</span>' % (" on" if _k == 4 else "", _t)
               for _k, _t in enumerate(
                   ["Voice AI Agent", "Post-Loan Collections", "Overdue Asset Management",
                    "Real-Time Interaction", "Agora"]))),
    sh("flow mono-sm", "left:120px;top:930px;width:1500px;height:24px;--i:6",
       "For post-loan, risk, compliance and technology leaders at financial institutions "
       "&#183; Solution briefing &#183; Facts as of 2026.08"),
]))

# ═══ P2 · Overview ·「五节一链 + 本篇路线」════════════════════════════════════
#   五点是一条**逻辑链**，所以排成 flow 带而不是五张并列卡 ——
#   并列卡会把「因为所以」读成「还有还有」。
#   版式账（英文版重算，中文版是 W296/G50）：W=260 / G=95 ⇒ 5×260 + 4×95 = 1680。
#     盒内可用宽 = 260 − 52 = 208px：标题 26px ⇒ 每行 ≤ 15 字符；正文 18px ⇒ ≤ 26 字符。
#     G 从 50 加宽到 95 是为了让边上的「流的什么」放得下英文（14px 下 ≤ 15 字符）——
#     中文四个字 56px 塞得进 50 的缝，英文两个词塞不进，会被下一只盒子盖掉半截。
_CHAIN = [
    ("01", ["Demand is", "structural"],
     ["Large credit portfolios", "make overdue asset", "management a standing", "capability."]),
    ("02", ["The old model", "hits a ceiling"],
     ["Agents, outsourcing and", "rule-based dialing cannot", "deliver scale, efficiency", "and compliance at once."]),
    ("03", ["Regulation has", "moved first"],
     ["Conduct, data use and", "customer protection are", "now written into law."]),
    ("04", ["AI is ready"],
     ["LLM, ASR, TTS, intent", "detection and real-time", "voice make this", "deployable today."]),
    ("05", ["Agora's role"],
     ["Real-time voice AI", "infrastructure that takes", "collections from pilot", "to production."]),
]
_CHAIN_EDGE = ["Scale holds", "Limits show", "Bar rises", "Tech lands"]
_ROADMAP = [
    ("Market &amp; Vietnam", "P3&#8211;4"), ("Operating chain", "P5"), ("Core tension", "P6&#8211;7"),
    ("Trends", "P8"), ("Market sizing", "P9"), ("AI &amp; architecture", "P10&#8211;11"),
    ("Agora &amp; rollout", "P12&#8211;14"),
]
def _chain_fig():
    o, W, G = [], 260, 95
    for k, (no, ttl, body) in enumerate(_CHAIN):
        x = k * (W + G)
        hot = (k == 4)
        if hot:
            o.append(halo_rect(x, 40, W, 300, 10, sc="1.04", op=".3", dur="3.6s"))
        o.append(box(x, 40, W, 300, 10, hot=hot, i=k + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.6s" if hot else ""))
        o.append(txt(x + 26, 84, no, "sm", size=14, col=AC, mono=True, ls=".18em"))
        for j, seg in enumerate(ttl):
            o.append(txt(x + 26, 138 + j * 34, seg, "ttl", size=26, col=AC if hot else None))
        for j, seg in enumerate(body):
            o.append(txt(x + 26, 216 + j * 28, seg, "sm", size=18))
        if k < 4:
            x1, x2 = x + W, x + W + G
            o.append(packet("M%d 190 H%d" % (x1, x2 - 12), G - 12, seg=18, dur="1.6s",
                            i=k + 1, delay="%.1fs" % (k * .35)))
            o.append(hline(x1, x2 - 12, 190, AC, 2.5, k + 1))
            o.append(ah_r(x2, 190, AC, 8))
            o.append(txt(x1 + G // 2 - 6, 166, _CHAIN_EDGE[k], "sm", size=14,
                         anchor="middle", col=I3))
            # 出线口的接头脉冲：五节按 0.35s 依次亮起 ⇒ 一道亮波从 01 跑到 05
            o.append(pulse_dot(x + W, 190, 6, AC, lo=".18", dur="2.8s",
                               delay="%.2fs" % (k * .35), i=k + 2))
    o.append(legend(0, 384, [("solid", "Narrative spine &#183; cause and effect")]))
    return "".join(o)
page("content", "".join([
    head("OVERVIEW &#183; THE WHOLE STORY IN ONE PAGE",
         "From headcount-driven collections to <strong>intelligent operations</strong>."),
    lab(120, 244, "01 &#183; NARRATIVE CHAIN &#183; FIVE LINKS"),
    # 「from headcount-driven to intelligent operations」是行业判断，不是可验证事实
    viewtag(242),
    figbox(120, 276, 1680, 1680, 410, _chain_fig(), i=1),
    lab(120, 712, "02 &#183; ROADMAP &#183; HOW THIS DECK RUNS", i=6),
    sh("flow", "left:120px;top:748px;width:1680px;height:82px;--i:7",
       '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:18px;height:100%">'
       + "".join(
           # 页号那一格挂 data-nogate="pageref"：它是**本 deck 自己的页码**，不是内容里的数字。
           # 不豁免的话，qa 的「新造数字闸」白名单就得把 10–15 全收进去 —— 收进去之后
           # 任何一个新写的小数字都能蒙混过关，闸门当场钝化。
           '<div style="border-top:1px solid var(--hair);padding-top:14px;display:flex;'
           'flex-direction:column;gap:8px">'
           '<div data-nogate="pageref" style="font:500 13px/1 var(--f-mono);'
           'letter-spacing:.14em;color:var(--accent)">%s</div>'
           '<div style="font:400 19px/1.3 var(--f-cn);color:var(--ink-2)">%s</div></div>'
           % (_p, _t) for _t, _p in _ROADMAP) + '</div>'),
    rule(850),
    land("Every chapter answers the same question: "
         "<strong style='color:var(--accent)'>why AI, and why Agora</strong>."),
]))

# ═══ P3 · ★重铸 ·「东南亚的信贷增长，把贷后做成一项长期能力」═══════════════════
#   中文版这一页是三个中国大数（不良余额 / 不良率 / 正常贷款余额）。
#   英文版**不搬中国数、也不新造东南亚数** —— e-Conomy SEA 2025 只做定性引用
#   （Colin 已核：digital lending 稳步增长 / embedded loans 进电商与钱包平台驱动变现），
#   所以左半从「三张数字卡」改成「三张定性卡」，右半的资产循环闭环图原样保留：
#   有那条「资产质量 → 风险定价 → 放款」的点线回流，贷后才是**经营能力**而不是末端作业，
#   这正是本页标题那句话的图形依据（P8 质量语言第 ④ 条：闭环优先）。
_SEA3 = [
    ("DIGITAL LENDING", "Growing steadily",
     "Digital lending across Southeast Asia continues to grow steadily year on year.", True),
    ("EMBEDDED CREDIT", "Bundled into platforms",
     "Loans are increasingly embedded into e-commerce and e-wallet journeys.", False),
    ("MONETIZATION", "A profit driver",
     "Embedded lending has become one of the clearest monetization paths for platforms.", False),
]
def _asset_fig():
    o = []
    _N = [("Origination", "New credit extended"),
          ("Post-loan operations", "Segment &#183; contact &#183; negotiate &#183; fulfill"),
          ("Asset quality", "NPL ratio &#183; provisions &#183; profit")]
    for k, (t, s) in enumerate(_N):
        x = 130 + k * 470
        hot = (k == 1)
        if hot:
            o.append(halo_rect(x, 22, 340, 108, 10, sc="1.06", op=".32", dur="3.6s"))
        o.append(box(x, 22, 340, 108, 10, hot=hot, i=k + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.6s" if hot else ""))
        o.append(txt(x + 170, 68, t, "ttl", size=26, anchor="middle", col=AC if hot else None))
        o.append(txt(x + 170, 102, s, "sm", size=15, anchor="middle"))
        if k < 2:
            x1, x2 = x + 340, x + 470
            o.append(packet("M%d 76 H%d" % (x1, x2 - 12), 118, seg=20, dur="1.7s", i=k + 1,
                            delay="%.1fs" % (k * .5)))
            o.append(hline(x1, x2 - 12, 76, AC, 2.5, k + 1))
            o.append(ah_r(x2, 76, AC, 8))
            o.append(txt(x1 + 59, 52, ["Assets booked", "Recovery &#183; migration"][k], "sm", size=14,
                         anchor="middle", col=I3))
            o.append(pulse_dot(x + 340, 76, 6, AC, lo=".18", dur="2.8s",
                               delay="%.2fs" % (k * .55), i=k + 2))
    o.append(pulse_dot(1300, 130, 6, AD, lo=".2", dur="3.2s", delay="1.1s", i=5))
    o.append(pulse_dot(300, 140, 6, AD, lo=".2", dur="3.2s", delay="2.2s", i=5))
    _ARC = "M1300 130 V182 Q1300 198 1282 198 H318 Q300 198 300 182 V140"
    o.append(packet(_ARC, 1082, seg=24, col=AD, w=9, op=".3", dur="7s", i=5, cls="mo-cycle"))
    o.append(dline(_ARC, AD, 3, 5, dash="3 8"))
    o.append(ah_u(300, 134, AD, 7))
    o.append(txt(800, 228, "Asset quality feeds risk pricing and credit policy &#8212; "
                           "post-loan is a management capability, not a back-end task",
                 "sm", size=17, anchor="middle", col=AD))
    o.append(legend(130, 262, [("solid", "Core business flow"), ("dot", "Feedback loop")]))
    return "".join(o)
page("content", "".join([
    head("MARKET CONTEXT &#183; SOUTHEAST ASIA",
         "In Southeast Asia, collections is a <strong>standing capability</strong>."),
    lab(120, 250, "01 &#183; WHAT IS HAPPENING &#183; DIGITAL AND EMBEDDED LENDING", w=1000),
    sh("", "left:120px;top:288px;width:1680px;height:212px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d;justify-content:center">'
           '<div class="tag%s">%s</div><div class="t">%s</div><div class="d">%s</div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag, _t, _d)
           for _i, (_tag, _t, _d, _on) in enumerate(_SEA3)) + '</div>'),
    lab(120, 540, "02 &#183; WHY IT MATTERS &#183; WHERE POST-LOAN SITS IN THE ASSET CYCLE",
        w=1000, i=5),
    # viewBox 高 292→276：图内最深的墨是 y262 的图例（+ 字形下缘 ≈ 268），
    # 收到 276 之后图盒底边落在 852，把 y860 起的证据带整条让出来。
    figbox(120, 576, 1680, 1680, 276, _asset_fig(), i=6),
    rule(850),
    # ── 规模证据带（2026-08-30 · Colin ④）────────────────────────────────────
    #   这一页原本全是**定性**（e-Conomy 只作定性引用，一个贷款余额都不写），
    #   对越南的银行来说「趋势我知道，你们做过什么」是下一句必问。
    #   两枚数都取自 info 家族 P2 的 canon，且**刻意避开 P12 已用过的两枚**
    #   （90B+ 分钟 / 200+ 节点）—— 同一份 deck 里把同一个数说两遍，第二遍就贬值了。
    fnote(120, 860, 1680, 72, "ALREADY AT SCALE ON AGORA",
          "<b>Nearly half</b> of the top <b>10,000</b> RTC-integrated apps (by MAU) run on "
          "Agora &#183; <b>1M+</b> registered applications worldwide.", on=True, i=7),
    land("NPL management is a permanent function, not an "
         "<strong style='color:var(--accent)'>end-of-pipe task</strong>.", y=944),
    src(_SRC_SEA),
]))

# ═══ P4 · ★重铸 · 越南锚点页 ·「催收必须自建、数字化、合规」═══════════════════
#   这是全 deck 的**市场锚点页**：2021 年禁令是一条法律事实，不是趋势判断 ——
#   它把「要不要上系统」这个可选题变成了「怎么上」的必答题。
#   主视觉三段式：Before 2021 外包 → From 1 Jan 2021 禁止 → 唯一路径 自建 + 技术。
#   hot 件落在中段（禁令本身），全页唯一一枚 .mo-breathe。
_VN3 = [
    ("BEFORE 2021", "Outsourced collections",
     ["Banks and finance companies could hand", "overdue books to third-party agencies."], 0, False),
    ("FROM 1 JAN 2021", "A prohibited business line",
     ["&#8220;Debt collection services&#8221; became a", "prohibited business investment activity."], 605, True),
    # 2026-08-30 · GPT review P0-4 采纳：段标从「THE ONLY PATH」改为中性的
    #   「WHAT REMAINS · IN-HOUSE」。禁令三段式结构一格不动（页面冲击力靠的是那三段，
    #   不是这四个字），但「唯一路径」是我们替法律下的结论 —— 法律禁的是**催收服务
    #   这条经营业务线**，贷款机构自催的合规责任本来就在它自己身上。
    ("WHAT REMAINS &#183; IN-HOUSE", "Built and run by the lender",
     ["Lenders run collections themselves, with", "systems carrying scale and compliance."], 1210, False),
]
_VN_MEAN = [
    ("Build the team", "Collections becomes an in-house function with its own headcount, "
                       "training and quality bar."),
    ("Build the system", "Process, scripts, contact frequency and records have to be held by "
                         "systems, not by individuals."),
    ("Prove the process", "Every contact has to be explainable and auditable long after "
                          "the call has ended."),
]
def _vn_fig():
    o = []
    for k, (era, t, ds, x, hot) in enumerate(_VN3):
        if hot:
            o.append(halo_rect(x, 30, 470, 152, 10, sc="1.05", op=".32", dur="3.6s"))
        o.append(box(x, 30, 470, 152, 10, hot=hot, dashed=(k == 0), i=k + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.6s" if hot else ""))
        o.append(txt(x + 24, 64, era, "sm", size=13, col=AC if hot else I3, mono=True, ls=".18em"))
        o.append(txt(x + 24, 104, t, "ttl", size=24, col=AC if hot else None))
        for j, seg in enumerate(ds):
            o.append(txt(x + 24, 136 + j * 24, seg, "sm", size=16))
        if k < 2:
            x1, x2 = x + 470, x + 605
            o.append(packet("M%d 106 H%d" % (x1, x2 - 12), 123, seg=20, dur="1.7s", i=k + 1,
                            delay="%.1fs" % (k * .5)))
            o.append(hline(x1, x2 - 12, 106, AC, 2.5, k + 1))
            o.append(ah_r(x2, 106, AC, 8))
            # 「No alternative」与段标是同一句断言的两处出口，一起改中性：
            # 第二条边说的是「责任留在贷款机构手上」，那是法律事实，不是我们的推论。
            o.append(txt(x1 + 62, 84, ["Banned by law", "Duty retained"][k], "sm", size=14,
                         anchor="middle", col=I3))
            o.append(pulse_dot(x + 470, 106, 6, AC, lo=".18", dur="2.8s",
                               delay="%.2fs" % (k * .55), i=k + 2))
    o.append(legend(0, 206, [("solid", "Legal turning point &#183; one direction only")]))
    o.append(domain_band(0, 228, 1680, 100,
                         "LAW ON INVESTMENT NO. 61/2020/QH14 &#183; NATIONAL ASSEMBLY OF VIETNAM"))
    # 2026-08-30 · GPT review P0-4：论证句改写。原句「outsourcing is no longer available」
    #   只说了一半，读者会把它接成「所以你必须买技术」。写全的版本是两句：
    #   ① 法律禁的是**催收服务这条经营业务线**（这是可引的法条）
    #   ② 贷款机构的自催合规责任本来就在（这也是法条）—— 技术是把它做到规模的方式，
    #      不是法定义务。第二句把「必须上系统」这个我们最想让客户得出的结论，
    #      交回给客户自己去下，而不是替法律下。
    #   两行分开写（单行 981px 已接近 1680 的可用宽，硬塞会顶到 viewBox 右缘）。
    o.append(txt(18, 284, "Since 01.01.2021, providing debt collection services is a "
                          "prohibited business line.", "sm", size=18))
    o.append(txt(18, 310, "Lenders retain responsibility for compliant in-house collections "
                          "&#8212; technology is how that scales, not a statutory mandate.",
                 "sm", size=18))
    return "".join(o)
page("content", "".join([
    head("VIETNAM &#183; THE MARKET ANCHOR",
         "Vietnam: collections must now be <strong>in-house and digital</strong>."),
    lab(120, 244, "01 &#183; THE 2021 TURNING POINT &#183; OUTSOURCING WAS CLOSED, NOT NARROWED",
        w=1200),
    figbox(120, 272, 1680, 1680, 330, _vn_fig(), i=1),
    lab(120, 636, "02 &#183; WHAT IT MEANS FOR LENDERS", i=4),
    sh("", "left:120px;top:668px;width:1680px;height:168px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card sm%s rise" style="--i:%d;justify-content:center">'
           '<div class="t">%s</div><div class="d">%s</div></div>'
           % (" on" if _i == 1 else "", 5 + _i, _t, _d)
           for _i, (_t, _d) in enumerate(_VN_MEAN)) + '</div>'),
    rule(850),
    land("Outsourcing is no longer an option &#8212; "
         "<strong style='color:var(--accent)'>capability has to be built</strong>.", y=944),
    src(_SRC_VN),
]))

# ═══ P5 · Value chain 八环闭环（**标杆动效页** · cycle 原语环行）═══════════════
#   动效即语义：椭圆环走 .mo-cycle（**几何绝不旋转**，只让虚线 dash 绕圈爬 ——
#   环一转，八个节点与文字就甩走了，整页论证当场失效）。
#   环长（Ramanujan 近似，rx=560 / ry=190）≈ 2502；dash「11 10」周期 21，
#   取 119 个整周期 = 2499 作 --mo-off ⇒ 100% 帧 = 0% 帧（静态原图纪律）。
#   三枚 .mo-packet 相位错开 1/3 周期 = 同时有多个案件在链路的不同位置上；
#   八枚 .mo-pulse 钉在相邻节点的中点，delay 依次 +0.3s ⇒ 一道亮波顺时针跑。
#   ⚠ 英文版把节点盒从 208×76 加宽到 268×92（两行副题）——
#     触达渠道要在这一页本地化列全（Zalo / WhatsApp / LINE / KakaoTalk），
#     176px 的中文盒装不下。加宽后八只盒两两不相交（已逐对复算，见下表）：
#       k0(706..974, 26..118) k1(1102..1370, 82..174) k2(1266..1534, 216..308)
#       k3(1102..1370, 350..442) k4(706..974, 406..498) k5(310..578, 350..442)
#       k6(146..414, 216..308) k7(310..578, 82..174)
#     环心可用横带 = 414..1266（852px），竖带 = 118..406（288px）。
_LINK8 = [
    ("01", "Segmentation", ["Aging &#183; amount &#183; risk &#183; behavior"]),
    ("02", "Contact strategy", ["Phone &#183; SMS &#183; app push &#183; email",
                                "Zalo &#183; WhatsApp &#183; LINE &#183; KakaoTalk"]),
    ("03", "Conversation", ["Verify identity &#183; reason &#183; options"]),
    ("04", "Promise to pay", ["Log promise &#183; send link &#183; set reminder"]),
    ("05", "Fulfillment tracking", ["Monitor payment &#183; escalate if needed"]),
    ("06", "Dispute handling", ["Billing &#183; identity &#183; complaint &#183; relief"]),
    ("07", "Compliance QA", ["Script checks &#183; frequency &#183; recording"]),
    ("08", "Strategy iteration", ["Tune on recovery, complaints, contact"]),
]
_R8CX, _R8CY, _R8RX, _R8RY = 840, 262, 560, 190
_R8_LEN = 2502          # Ramanujan 近似周长；改 rx/ry 必须重算这一笔与下面的 off
_R8_OFF = 2499          # = 21 × 119（dash「11 10」的整周期）⇒ 100% 帧 = 静态原图
_R8_PATH = ("M%d %d A %d %d 0 0 1 %d %d A %d %d 0 0 1 %d %d"
            % (_R8CX - _R8RX, _R8CY, _R8RX, _R8RY, _R8CX + _R8RX, _R8CY,
               _R8RX, _R8RY, _R8CX - _R8RX, _R8CY))
def _ring_pt(deg):
    r = math.radians(deg)
    return (_R8CX + _R8RX * math.cos(r), _R8CY + _R8RY * math.sin(r))
def _ring_fig():
    o = []
    o.append('<path class="pop mo-cycle" style="--i:1;--mo-off:-%d;--mo-dur:26s" d="%s" '
             'fill="none" stroke="%s" stroke-width="2.4" stroke-dasharray="11 10"/>'
             % (_R8_OFF, _R8_PATH, AC))
    for k in range(3):
        o.append(packet(_R8_PATH, _R8_LEN, seg=26, w=13, op=".26", dur="26s", i=2,
                        delay="-%.2fs" % (k * 26 / 3.0), cls="mo-cycle"))
    for k in range(8):
        px, py = _ring_pt(-90 + 45 * k + 22.5)
        o.append('<circle class="pop mo-pulse" style="--i:%d;--mo-lo:.18;--mo-dur:2.4s;'
                 '--mo-del:%.2fs;fill:%s" cx="%d" cy="%d" r="7"/>'
                 % (3 + k % 4, k * .3, AD, round(px), round(py)))
    for k, (no, t, ds) in enumerate(_LINK8):
        px, py = _ring_pt(-90 + 45 * k)
        x, y = round(px) - 134, round(py) - 46
        hot = (k == 7)
        if hot:
            o.append(halo_rect(x, y, 268, 92, 9, sc="1.08", op=".34", dur="3.4s"))
        o.append(box(x, y, 268, 92, 9, hot=hot, i=(k % 4) + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.4s" if hot else ""))
        o.append(txt(x + 16, y + 30, no, "sm", size=13, col=AC, mono=True, ls=".18em"))
        o.append(txt(x + 52, y + 32, t, "ttl", size=22, col=AC if hot else None))
        for j, d in enumerate(ds):
            o.append(txt(x + 16, y + 60 + j * 20, d, "sm", size=14))
    # 闭环边的「流的什么」：08 → 01 那一段（左上弧），钉在该段中点脉冲 (626, 86) 正上方。
    # 净空复算：y58 的一行只与 k0 盒（706..974, 26..118）在竖向重叠，横向离它 80px。
    o.append(txt(626, 58, "Metrics loop back", "sm", size=16, col=AD, anchor="middle"))
    o.append(txt(_R8CX, _R8CY - 10, "Eight stages &#183; one loop", "ttl", size=30, anchor="middle"))
    o.append(txt(_R8CX, _R8CY + 26, "An operating system driven by data, voice, "
                                    "workflow and compliance control",
                 "sm", size=18, anchor="middle"))
    o.append(legend(30, 528, [("solid", "Operating chain"), ("dot", "Metrics feedback")]))
    # 图注（2026-08-30 · GPT review P1-9 采纳-轻）：环形图把八环画成等权节点，
    # 客户容易读成「06 dispute」「07 QA」只是链路上的两站 —— 实际上这两件贯穿全链。
    # 几何一格不动（改几何要重算八只盒的净空）。
    o.append(txt(1650, 533, "Dispute handling &amp; compliance QA span all eight stages",
                 "sm", size=16, anchor="end", col=I3))
    return "".join(o)
page("content", "".join([
    head("VALUE CHAIN &#183; EIGHT STAGES, ONE LOOP",
         "Collections is not one action &#8212; it is an <strong>operating chain</strong>."),
    lab(120, 244, "01 &#183; EIGHT STAGES &#183; SEGMENT &#8594; CONTACT &#8594; CONVERSE "
                  "&#8594; PROMISE &#8594; FULFILL &#8594; DISPUTE &#8594; QA &#8594; ITERATE",
        w=1400),
    figbox(120, 276, 1680, 1680, 560, _ring_fig(), i=1),
    rule(850),
    land("A collections system is not auto-dialing &#8212; it is data, voice, workflow and "
         "<strong style='color:var(--accent)'>compliance control</strong>."),
]))

# ═══ P6 · Core tension ·「规模、人效、合规三者难兼得」═════════════════════════
#   左：hot 三角。三个顶点两两之间是**取舍边**（拉紧一边就松掉另一边），
#     中心那枚 hot 盒才是本页命题 —— 全页唯一的 .mo-breathe。
#     三条边上跑 .mo-packet 绕三角环行 = 张力在三者之间来回倒。
#   右：五难并列证据，用家族 .rows —— 并列不是链路，所以这里刻意不画箭头。
#   ⚠ 英文版把顶点内移（(360,48)/(140,372)/(580,372)）并把顶点盒加宽到 240 ——
#     中文版的 (110,372) 配 240 宽盒会把左顶点顶到 x=-10（画布外）。
_FIVE = [
    ("01", "Contact",
     "Call blocking, refusals and dead numbers cut effective contact; a phone-only channel "
     "keeps losing reach."),
    ("02", "Productivity",
     "Agent training is slow and top performers are hard to clone; peak volume means hiring, "
     "and cost stops flexing."),
    ("03", "Strategy",
     "Aging, amount, product and risk each need a different script and rhythm; rule-based "
     "policies are slow to change."),
    ("04", "Compliance",
     "Scripts, frequency, outsourcing and complaints all need managing; manual conversations "
     "rest on individual judgment."),
    ("05", "Quality assurance",
     "Sampling covers a fraction of calls, and post-hoc review cannot stop a risky script "
     "while it is being spoken."),
]
_TRI = [("Scale", "Case volume in the millions"),
        ("Productivity", "Agent capacity has a ceiling"),
        ("Compliance", "Every step must be traceable")]
_TRI_PT = [(360, 48), (140, 372), (580, 372)]
def _tri_fig():
    o = []
    for k in range(3):
        (x1, y1), (x2, y2) = _TRI_PT[k], _TRI_PT[(k + 1) % 3]
        ln = round(math.hypot(x2 - x1, y2 - y1))
        d = "M%d %d L%d %d" % (x1, y1, x2, y2)
        o.append(packet(d, ln, seg=22, w=10, op=".26", dur="3.2s", i=k + 1,
                        delay="-%.2fs" % (k * 3.2 / 3.0)))
        o.append(pline(d, AC, 2.2, k + 1, ln=ln))
    for (mx, my, t, an) in [(212, 178, "Scale up &#8594; productivity thins", "end"),
                            (508, 178, "Compliance first &#8594; capacity caps", "start"),
                            (360, 430, "Maximize productivity &#8594; scripts drift", "middle")]:
        o.append(txt(mx, my, t, "sm", size=15, col=I3, anchor=an))
    for k, (t, d) in enumerate(_TRI):
        cx, cy = _TRI_PT[k]
        x, y = cx - 120, cy - 33
        o.append(pulse_dot(cx, cy, 34, AC, lo=".04", hi=".13", dur="3.2s",
                           delay="-%.2fs" % (k * 3.2 / 3.0), i=k + 2))
        o.append(box(x, y, 240, 66, 8, i=k + 2))
        o.append(txt(cx, cy - 2, t, "ttl", size=25, anchor="middle"))
        o.append(txt(cx, cy + 22, d, "sm", size=14, anchor="middle"))
    o.append(halo_rect(210, 222, 300, 84, 10, sc="1.1", op=".34", dur="3.4s"))
    o.append(box(210, 222, 300, 84, 10, hot=True, i=5, cls="mo-breathe", sty="--mo-dur:3.4s"))
    o.append(txt(360, 254, "Hard to hold all three", "ttl", size=24, anchor="middle", col=AC))
    o.append(txt(360, 282, "Headcount does not fix structure", "sm", size=15,
                 anchor="middle", col=AC))
    o.append(legend(20, 458, [("solid", "Trade-off tension &#183; one gives when another pulls")]))
    return "".join(o)
page("content", "".join([
    head("CORE TENSION &#183; THREE-WAY TRADE-OFF",
         "Scale, productivity and compliance <strong>pull against each other</strong>."),
    lab(120, 250, "01 &#183; TRADE-OFF &#183; THE TRIANGLE"),
    figbox(120, 288, 720, 720, 470, _tri_fig(), i=1),
    lab(920, 250, "02 &#183; FIVE FRICTIONS &#183; WHERE IT BREAKS", i=2),
    sh("rise", "left:920px;top:280px;width:880px;height:520px;--i:3",
       '<div class="rows" style="height:100%">' + "".join(
           '<div class="r"><div class="n">%s</div><div class="k" style="width:215px">%s</div>'
           '<div class="v">%s</div></div>' % (_n, _k, _v)
           for _n, _k, _v in _FIVE) + '</div>'),
    rule(850),
    land("These are <strong style='color:var(--accent)'>structural</strong> problems "
         "&#8212; more headcount does not solve them."),
]))

# ═══ P7 · ★重铸 · 第二杀手页 ·「监管已经把合规催收的规格写好了」═══════════════
#   中文版这一页讲的是中国的部门规章 + 国标；英文版换成 SBV Circular 18/2019/TT-NHNN
#   的四条**可执行规格**（频次 / 时间窗 / 对象 / 手段），做成一张「监管规格卡」——
#   这四条不是倡议，是参数：系统能在每一通电话上守住，人守不住每一通。
#   ⚠ `threaten` 全 deck 只准出现在下面 04 · MEANS 那一格里（引述监管禁令），
#     该格挂 data-nogate="threaten"，QA 断言全文命中数 = 1 且落在该节点内。
#   ⚠ 区域条**只列监管机构名**，不写各国具体条款（未核）——
#     论点是「合规按市场配置」，不是「我们知道每个国家怎么规定」。
_SPEC4 = [
    ("01 &#183; FREQUENCY", "&#8804; 5 reminders per day",
     "Debt reminder contact is capped at five times a day.", False),
    ("02 &#183; TIME WINDOW", "07:00&#8211;21:00 only",
     "Contact only inside the window agreed in the loan contract.", False),
    # 2026-08-30 · GPT review P0-6：「No third-party contact」在合规负责人耳朵里是
    #   「不得联系任何第三方」—— 那不是条款说的。条款限的是**无还款义务的第三人**
    #   （担保人、共同债务人、监管要求的联系对象都不在禁令里）。标题写全，副文照旧。
    ("03 &#183; WHO", "No contact with non-obligor third parties",
     "No reminders or collection messages to organizations or people with no obligation "
     "to repay, unless a regulator requires it.", False),
    ("04 &#183; MEANS", "Lawful measures only",
     "Measures must be lawful, and must exclude threatening the customer.", True),
]
_REGULATORS = [
    ("INDONESIA", "<b>OJK</b> &#183; Otoritas Jasa Keuangan"),
    ("PHILIPPINES", "<b>BSP</b> &#183; Bangko Sentral ng Pilipinas"),
    ("THAILAND", "<b>BOT</b> &#183; Bank of Thailand"),
    ("SINGAPORE", "<b>MAS</b> &#183; Monetary Authority of Singapore"),
]
page("content", "".join([
    # 2026-08-30 · GPT review P0-6：kicker 从「VIETNAM AND THE REGION」收紧到
    #   「VIETNAM · FINANCE-COMPANY GUARDRAILS」—— 本页四条规格全部来自
    #   Circular 18/2019 修订的**消费金融公司消费信贷框架**，不是越南全行业的通则，
    #   更不是「the region」的通则。原 kicker 把适用范围放大了两次。
    head("REGULATORY SPEC &#183; VIETNAM &#183; FINANCE-COMPANY GUARDRAILS",
         "Regulation has already written the <strong>collections spec</strong>."),
    lab(120, 244, "01 &#183; THE SPEC &#183; SBV CIRCULAR 18/2019/TT-NHNN"),
    # 左：监管规格卡（四条 spec 格 · 2×2）
    sh("rise card-c", "left:120px;top:280px;width:1020px;height:428px;--i:2",
       '<div style="padding:28px 34px;height:100%;display:flex;flex-direction:column">'
       '<div style="font:500 13px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-3)">'
       'CIRCULAR &#183; STATE BANK OF VIETNAM</div>'
       '<div style="margin-top:12px;font:700 27px/1.3 var(--f-cn);color:var(--ink)">'
       'Circular 18/2019/TT-NHNN</div>'
       '<div style="margin-top:10px;font:400 19px/1.4 var(--f-cn);color:var(--ink-2)">'
       'Amends Circular 43/2016, Point dd, Clause 2, Article 7 &#183; effective 01.01.2020</div>'
       '<div class="spec" style="margin-top:18px">' + "".join(
           '<div%s><div class="h">%s</div><div class="v">%s</div><div class="s">%s</div></div>'
           % (' data-nogate="threaten"' if _ng else "", _h, _v, _s)
           for _h, _v, _s, _ng in _SPEC4) + '</div></div>'),
    # 右：论点（规格只有系统能在规模上守住）
    sh("rise card-c on", "left:1180px;top:280px;width:620px;height:428px;--i:3",
       '<div style="padding:28px 32px;height:100%;display:flex;flex-direction:column">'
       '<div style="font:500 13px/1 var(--f-mono);letter-spacing:.18em;color:var(--accent)">'
       'WHY IT MATTERS</div>'
       '<div style="margin-top:14px;font:700 32px/1.28 var(--f-cn);letter-spacing:-.01em;'
       'color:var(--ink)">A spec only systems can enforce at scale.</div>'
       '<div style="margin-top:20px;font:400 19px/1.55 var(--f-cn);color:var(--ink-2)">'
       'Frequency caps, time windows, third-party limits and language limits are '
       'parameters, not guidance.</div>'
       '<div style="margin-top:14px;font:400 19px/1.55 var(--f-cn);color:var(--ink-2)">'
       'A system can hold them on every call and log the evidence. A person cannot hold '
       'them on every call, every day, at volume.</div>'
       '<div style="margin-top:14px;font:400 19px/1.55 var(--f-cn);color:var(--ink-2)">'
       'Every contact then answers three questions: why this customer, what strategy, '
       'and was it compliant.</div></div>'),
    # 适用范围小注（2026-08-30 · GPT review P0-6）：钉在规格卡正下方 ——
    #   四条参数是「消费金融公司消费信贷」框架下的，不是越南全行业通则。
    # 版式账：规格卡底 708 → 适用范围小注 712（4px，读作「注解上面那张卡」）→
    #   seclab 750（14px，读作「换段了」）→ 区域条 780（h56：13 + 7 + 19×1.4 = 46.6 ≤ 56）。
    scopenote(712, "Scope: Circular 18/2019 sits inside the consumer-lending framework for "
                   "<b>finance companies</b> &#8212; not a whole-of-market rule.",
              x=120, w=1020, i=4),
    # 区域条标题改写（2026-08-30 · GPT review P0-6）：原文写「EACH MARKET HAS ITS OWN
    #   CONDUCT RULES」会被读成「我们知道每个市场怎么规定」。这一条实际只列了**监管机构名**，
    #   所以标题里必须先说 REGULATOR NAMES ONLY，再说配置论点。一条国别规则都不新增。
    lab(120, 750, "02 &#183; ACROSS THE REGION &#183; REGULATOR NAMES ONLY &#8212; EACH MARKET "
                  "HAS ITS OWN RULEBOOK, CONFIGURED PER MARKET", w=1400, i=5),
    sh("flow", "left:120px;top:780px;width:1680px;height:56px;--i:6",
       '<div class="adv">' + "".join(
           '<div><div class="h">%s</div><div class="b">%s</div></div>' % (_h, _b)
           for _h, _b in _REGULATORS) + '</div>'),
    rule(850),
    land("Compliance is a <strong style='color:var(--accent)'>configuration</strong>, "
         "not a promise &#8212; per market, per rulebook.", y=944),
    src(_SRC_SBV),
]))

# ═══ P8 · Five trends ═══════════════════════════════════════════════════════
#   本页是**结论页**不是机理页：五条并列，故只用 .g5 卡，不上 SVG、不入运动件名册。
_TRENDS = [
    ("COMPLIANCE-FIRST", "Compliance first",
     "The bar moves from outcome only to process and outcome. Institutions must show that "
     "every action met regulation, internal policy and customer-protection rules."),
    ("STANDARDIZATION", "Standardization",
     "Process, language, contact frequency, records and quality review become standard, "
     "cutting person-to-person variance and outsourcing risk."),
    ("INTELLIGENCE", "Intelligence",
     "AI is used for segmentation, contact timing, voice outreach, intent detection, "
     "real-time quality review, call summaries and strategy tuning."),
    ("NEGOTIATION", "Negotiation",
     "The work moves from reminding to assessing capacity to repay, discussing installment "
     "options, resolving disputes and repairing the relationship."),
    ("INTERNAL CONTROL", "Internal control",
     "Lenders carry more responsibility for third-party agencies, and need systems to push "
     "strategy, monitor process, review quality and audit."),
]
page("content", "".join([
    head("TRENDS &#183; FIVE DIRECTIONS",
         "Five directions the industry is <strong>already moving in</strong>."),
    lab(120, 250, "01 &#183; FIVE TRENDS &#183; COMPLIANCE &#183; STANDARDIZATION &#183; "
                  "INTELLIGENCE &#183; NEGOTIATION &#183; CONTROL", w=1400),
    # 这五条与页脚「natural next step」都是判断句（没有哪家机构发布过这五条）
    viewtag(248),
    sh("", "left:120px;top:292px;width:1680px;height:520px",
       '<div class="g5" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d"><div class="tag%s">%s</div>'
           '<div class="t">%s</div><div class="d">%s</div></div>'
           % (" on" if _i == 2 else "", 2 + _i, " am" if _i == 2 else "", _n, _t, _d)
           for _i, (_n, _t, _d) in enumerate(_TRENDS)) + '</div>'),
    rule(850),
    land("AI in collections is not an isolated tool &#8212; it is the "
         "<strong style='color:var(--accent)'>natural next step</strong>."),
]))

# ═══ P9 · Market sizing ·「三层空间」════════════════════════════════════════
#   本页的方法论纪律：**不要把不良贷款余额直接等同于市场规模**。
#   所以图形不是柱状对比，而是一个**收窄的三层带**（域分带语言）——
#   宽度收窄本身就是「不能把上一层当成下一层」的图形证据。
#   右侧第三方交叉参考只放两家机构的原始区间，不做平均、不做换算、不外推到任何单一市场。
_LAYERS = [
    ("LAYER 1", "Risk asset pool",
     ["Bank NPLs, credit-card arrears, consumer-loan arrears, platform and installment lending arrears"],
     "Reflects the volume of assets that has to be managed", 0, 1160),
    ("LAYER 2", "Collections operating spend",
     ["Agents, outsourcing fees, telecom and number costs, systems, QA, compliance and management"],
     "Reflects what is spent each year on recovery and control", 145, 870),
    ("LAYER 3", "AI technology services",
     ["Voice AI agents, outbound automation, conversation analytics, real-time QA,",
      "strategy engines, RAG knowledge bases, transcription and agent assist"],
     "Reflects what AI and software can replace, augment or rebuild", 290, 580),
]
def _stack_fig():
    o = []
    for k, (no, t, ds, note, x, w) in enumerate(_LAYERS):
        y = 16 + k * 146
        hot = (k == 2)
        if hot:
            o.append(halo_rect(x, y, w, 116, 10, sc="1.05", op=".32", dur="3.6s"))
        o.append(box(x, y, w, 116, 10, hot=hot, i=k + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.6s" if hot else ""))
        o.append(txt(x + 22, y + 34, no, "sm", size=13, col=AC, mono=True, ls=".18em"))
        o.append(txt(x + 118, y + 36, t, "ttl", size=25, col=AC if hot else None))
        for j, seg in enumerate(ds):
            o.append(txt(x + 22, y + 62 + j * 20, seg, "sm", size=15))
        o.append(txt(x + 22, y + 104, note, "sm", size=14, col=I3))
        if k < 2:
            nx, nw = _LAYERS[k + 1][4], _LAYERS[k + 1][5]
            cx = nx + nw // 2
            o.append(packet("M%d %d V%d" % (cx, y + 116, y + 134), 18, seg=12, dur="1.4s",
                            i=k + 2, delay="%.1fs" % (k * .6)))
            o.append(vline(cx, y + 116, y + 134, AC, 2.5, k + 2))
            o.append(ah_d(cx, y + 146, AC, 8))
            o.append(txt(cx + 26, y + 136,
                         ["The part someone pays for",
                          "The part technology can replace or augment"][k], "sm", size=15, col=I3))
            # 收窄肩点：亮的是**被切掉的那两截** —— 「不能把上一层当成下一层」的图形证据
            for j, sx in enumerate((nx, nx + nw)):
                o.append(pulse_dot(sx, y + 126, 6, AD, lo=".16", dur="3s",
                                   delay="%.2fs" % (k * .7 + j * .35), i=k + 3))
    o.append(legend(0, 452, [("solid", "Narrowing scope &#183; not interchangeable")]))
    return "".join(o)
page("content", "".join([
    head("MARKET SIZING &#183; THREE LAYERS",
         "Market size is <strong>three layers</strong>, not one number."),
    lab(120, 236, "01 &#183; MARKET STACK &#183; DEBT VOLUME &#8594; OPERATING SPEND "
                  "&#8594; SOFTWARE", w=1200),
    figbox(120, 268, 1160, 1160, 476, _stack_fig(), i=1),
    sh("rise card-c", "left:1320px;top:268px;width:480px;height:476px;--i:4",
       '<div style="padding:26px 28px;height:100%;display:flex;flex-direction:column">'
       '<div style="font:500 13px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-3)">'
       'CROSS-CHECK &#183; THIRD PARTIES</div>'
       # 2026-08-30 · GPT review P1-10 采纳：这两组数是**全球品类**的软件市场，
       # 与左侧三层收窄的第三层不是一回事，更不是任何一家机构的可服务市场。
       # 不标这一枚，客户会把 13.77B 当成「我们能卖多大」——那正是本页要防的事。
       '<div class="vtag" style="margin-top:12px">GLOBAL CATEGORY PROXY &#183; NOT YOUR SAM</div>'
       # 上一版这一行是两行（「not averaged」也写在这里）—— 那句话卡底的注里已经有，
       # 收成一行给判断标腾出高度，信息一个字没少。
       '<div style="margin-top:10px;font:400 16px/1.5 var(--f-cn);color:var(--ink-3)">'
       'Global debt collection software market.</div>'
       '<div style="margin-top:20px;padding-top:18px;border-top:1px solid var(--hair)">'
       '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3)">'
       'FORTUNE BUSINESS INSIGHTS</div>'
       '<div style="margin-top:12px;display:flex;align-items:baseline;gap:10px">'
       '<span style="font:900 40px/1 var(--f-en);letter-spacing:-.03em;color:var(--accent)">5.98</span>'
       '<span style="font:500 20px/1 var(--f-mono);color:var(--ink-3)">&#8594;</span>'
       '<span style="font:900 40px/1 var(--f-en);letter-spacing:-.03em;color:var(--accent)">13.77</span>'
       '<span style="font:400 17px/1 var(--f-cn);color:var(--ink-3)">USD bn</span></div>'
       '<div style="margin-top:10px;font:500 15px/1 var(--f-mono);letter-spacing:.1em;'
       'color:var(--ink-2)">2025 &#8594; 2034 &#183; CAGR 9.72%</div></div>'
       '<div style="margin-top:22px;padding-top:18px;border-top:1px solid var(--hair)">'
       '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3)">'
       'GRAND VIEW RESEARCH</div>'
       '<div style="margin-top:12px;display:flex;align-items:baseline;gap:10px">'
       '<span style="font:900 38px/1 var(--f-en);letter-spacing:-.03em;color:var(--ink)">4.9</span>'
       '<span style="font:500 20px/1 var(--f-mono);color:var(--ink-3)">&#8594;</span>'
       '<span style="font:900 38px/1 var(--f-en);letter-spacing:-.03em;color:var(--ink)">9.3</span>'
       '<span style="font:400 17px/1 var(--f-cn);color:var(--ink-3)">USD bn</span></div>'
       '<div style="margin-top:10px;font:500 15px/1 var(--f-mono);letter-spacing:.1em;'
       'color:var(--ink-2)">2023 &#8594; 2030</div></div>'
       '<div style="margin-top:auto;font:400 15px/1.5 var(--f-cn);color:var(--ink-3)">'
       'The two windows and industry coverage differ &#8212; GVR spans non-financial use '
       'cases. Shown side by side, not averaged and not converted to any single market.</div></div>'),
    lab(120, 768, "02 &#183; FORMULA &#183; TWO WAYS TO SIZE IT", i=5),
    sh("flow", "left:120px;top:794px;width:1680px;height:48px;--i:6",
       '<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;height:100%">' + "".join(
           '<div style="border-left:2px solid color-mix(in srgb,var(--accent) 46%%,transparent);'
           'padding-left:16px;display:flex;flex-direction:column;justify-content:center;gap:6px">'
           '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.16em;color:var(--ink-3)">%s</div>'
           '<div style="font:500 17px/1.35 var(--f-mono);letter-spacing:.02em;color:var(--ink-2)">%s</div>'
           '</div>' % (_h, _b) for _h, _b in [
               ("PATH A &#183; FROM THE ASSET SIDE",
                "Serviceable overdue assets <b style=\"color:var(--accent)\">&#215;</b> turnover "
                "<b style=\"color:var(--accent)\">&#215;</b> tech penetration "
                "<b style=\"color:var(--accent)\">&#215;</b> service rate"),
               ("PATH B &#183; FROM THE SPEND SIDE",
                "Collections operating spend <b style=\"color:var(--accent)\">&#215;</b> "
                "tech-addressable share <b style=\"color:var(--accent)\">&#215;</b> AI penetration"),
           ]) + '</div>'),
    rule(850),
    land("Do not write NPL balances down as market size &#8212; "
         "<strong style='color:var(--accent)'>the layers narrow</strong>.", y=944),
    src(_SRC_MKT),
]))

# ═══ P10 · Why AI ═══════════════════════════════════════════════════════════
#   六项价值压成 .g3 两行小卡，把纵向空间让给下面那张表（销售现场客户会照着念）。
#   ⚠ 版式账：.g3 两行在 216px 盒里每行 97px；.card.sm 内容 = 40 + 29.4 + 9 + 27.4 = 105.8，
#     justify-content:center ⇒ 上下各溢 4.4px（闸门阈值 6px）。
#     **所以每张卡的 .d 必须单行（≤ 58 字符）** —— 折成两行就是 ±20px，当场触闸。
_AIV = [
    ("Scale of contact", "AI absorbs high-volume reminders and follow-ups."),
    ("Consistent language", "Less variance between agents, less script risk."),
    ("Real-time understanding", "Intent, sentiment, capacity to repay, complaint risk."),
    ("Automatic records", "Summaries, payment promises, tags and next actions."),
    ("Full-coverage QA", "Compliance checks on every call, not on a sample."),
    ("Human and AI together", "AI takes repetitive work; people take complex cases."),
]
_DIFF7 = [
    ("Capacity",            "Bound by headcount",               "Scales elastically"),
    ("Cost",                "High marginal cost per case",      "Marginal cost falls on repetitive work"),
    ("Language",            "Depends on individual experience", "Standardized and controllable"),
    ("Quality review",      "Sampling only",                    "Every conversation reviewed"),
    ("Compliance",          "Risk found after the fact",        "Prompted and blocked in real time"),
    ("Data",                "Records are incomplete",           "Structured automatically"),
    ("Customer experience", "Varies widely",                    "More consistent, more negotiable"),
]
page("content", "".join([
    head("WHY AI &#183; FROM OPTION TO REQUIREMENT",
         "AI is not optional &#8212; it is how <strong>compliant scale</strong> works."),
    lab(120, 244, "01 &#183; SIX VALUES &#183; WHAT AI ACTUALLY SOLVES"),
    # 「AI is not optional」是本 deck 最强的一句主张，也最该标出它是主张
    viewtag(242),
    sh("", "left:120px;top:272px;width:1680px;height:216px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card sm rise" style="--i:%d;justify-content:center">'
           '<div class="t">%s</div><div class="d">%s</div></div>' % (2 + _i, _t, _d)
           for _i, (_t, _d) in enumerate(_AIV)) + '</div>'),
    lab(120, 510, "02 &#183; SIDE BY SIDE &#183; TRADITIONAL MANUAL COLLECTIONS VS "
                  "AI-ASSISTED / AI VOICE", i=6, w=1200),
    sh("rise", "left:120px;top:540px;width:1680px;height:300px;--i:7",
       '<table class="mini ai-diff"><thead><tr><th style="width:210px">Dimension</th>'
       '<th style="width:600px">Traditional manual collections</th>'
       '<th>AI-assisted / AI voice collections</th></tr></thead><tbody>'
       + "".join('<tr><td>%s</td><td>%s</td><td><span class="k" '
                 'style="color:var(--accent)">%s</span></td></tr>' % r for r in _DIFF7)
       + '</tbody></table>'),
    rule(850),
    land("The value of AI is not replacing people &#8212; it is "
         "<strong style='color:var(--accent)'>rebuilding the operation</strong>."),
]))

# ═══ P11 · Capability loop（**第二动效重点** · 中枢 hub + 八模块）═══════════════
#   P8 质量语言六条逐条对表：
#     ① 三型线 + 图例（实线主数据流 / 虚线事件·控制 / 点线指标回流）
#     ② 每页唯一 hot 件：中枢 Agent（唯一 .mo-breathe + halo）
#     ③ 每条线带「流的什么」（八条各一句）
#     ④ 闭环优先：质检与分析 → 分层与策略引擎的点线回流弧绕整图一圈 ——
#        没有这条弧，这张图只是「一堆模块挂在中间那个盒子上」
#     ⑤ 本页无数字（数字全在 P12 的 canon 里，不在架构图上重复）
#     ⑥ 域分带：左 = 输入域 / 右 = 输出域
#   ⚠ 英文版把中枢从 380×170 加宽到 440×180（英文要三行副题），
#     _HUBX 随之从 650 挪到 620 ⇒ 左总线竖段 520..586 < 608 ✓、右总线 1160..1094 > 1060 ✓。
_MOD_IN = [   # (模块名, 副题, 流的什么, 线型)
    ("Segmentation &amp; strategy", "Aging &#183; amount &#183; risk &#183; behavior",
     "List &#183; contact strategy", "solid"),
    ("Real-time speech recognition", "Speech to text for understanding and record",
     "Customer speech &#8594; text", "solid"),
    ("LLM dialogue engine", "Reads intent, decides the next action",
     "Intent &#183; script guidance", "solid"),
    ("Compliance rule engine", "Identity checks &#183; language limits &#183; frequency",
     "Limits &#183; frequency", "dash"),
]
_MOD_OUT = [
    ("AI voice outreach", "Remind &#183; explain &#183; negotiate &#183; confirm",
     "Compliant script &#183; live dialogue", "solid"),
    ("Business system integration", "CRM &#183; collections &#183; payment &#183; tickets",
     "Promise &#183; ticket &#183; payment", "solid"),
    ("Quality review &amp; analytics", "QA results &#183; recovery &#183; complaint risk",
     "Full conversation records", "solid"),
    ("Human handover", "Disputes &#183; complaints &#183; identity &#183; escalation",
     "Handover events", "dash"),
]
_HUBX, _HUBY, _HUBW, _HUBH = 620, 132, 440, 180
def _hub_fig():
    o = []
    o.append(domain_band(24, 0, 336, 452, "INPUT &#183; UNDERSTAND &amp; LIMIT", i=1))
    o.append(domain_band(1320, 0, 330, 452, "OUTPUT &#183; EXECUTE &amp; RECORD", i=1))
    for k, (t, s, flow, kind) in enumerate(_MOD_IN):
        y = 44 + k * 104
        o.append(box(40, y, 304, 76, 8, i=k + 1))
        o.append(txt(58, y + 32, t, "ttl", size=19))
        o.append(txt(58, y + 58, s, "sm", size=13))
        my = _HUBY + 34 + k * 34
        d = "M344 %d H%d V%d H%d" % (y + 38, 520 + k * 22, my, _HUBX - 12)
        ln = (520 + k * 22 - 344) + abs(my - (y + 38)) + (_HUBX - 12 - (520 + k * 22))
        if kind == "solid":
            o.append(packet(d, ln, seg=20, dur="2.2s", i=k + 1, delay="%.1fs" % (k * .4)))
            o.append(pline(d, AC, 2.4, k + 1, ln=ln))
        else:
            o.append(dline(d, HS, 2, k + 1, dash="7 6", cls="mo-drift",
                           sty="--mo-off:-260;--mo-dur:4s"))
        o.append(ah_r(_HUBX, my, AC if kind == "solid" else HS, 8))
        o.append(txt(360, y + 26, flow, "sm", size=14, col=I3))
    for k, (t, s, flow, kind) in enumerate(_MOD_OUT):
        y = 44 + k * 104
        o.append(box(1336, y, 304, 76, 8, i=k + 1))
        o.append(txt(1354, y + 32, t, "ttl", size=19))
        o.append(txt(1354, y + 58, s, "sm", size=13))
        my = _HUBY + 34 + k * 34
        d = "M%d %d H%d V%d H%d" % (_HUBX + _HUBW, my, 1160 - k * 22, y + 38, 1324)
        ln = (1160 - k * 22 - (_HUBX + _HUBW)) + abs(y + 38 - my) + (1324 - (1160 - k * 22))
        if kind == "solid":
            o.append(packet(d, ln, seg=20, dur="2.2s", i=k + 1, delay="%.1fs" % (.2 + k * .4)))
            o.append(pline(d, AC, 2.4, k + 1, ln=ln))
        else:
            o.append(dline(d, HS, 2, k + 1, dash="7 6", cls="mo-drift",
                           sty="--mo-off:-260;--mo-dur:4s"))
        o.append(ah_r(1336, y + 38, AC if kind == "solid" else HS, 8))
        o.append(txt(1316, y + 26, flow, "sm", size=14, col=I3, anchor="end"))
    _ARC = ("M1640 290 H1652 Q1668 290 1668 306 V468 Q1668 484 1652 484 H34 "
            "Q18 484 18 468 V98 Q18 82 34 82 H36")
    o.append(packet(_ARC, 2140, seg=26, col=AD, w=10, op=".28", dur="9s", i=6, cls="mo-cycle"))
    o.append(dline(_ARC, AD, 3, 6, dash="3 8"))
    o.append(ah_r(40, 82, AD, 7))
    o.append(txt(840, 470, "Recovery, complaints, contact and fulfillment metrics feed the "
                           "next round of segmentation", "sm", size=17, anchor="middle", col=AD))
    o.append(halo_rect(_HUBX, _HUBY, _HUBW, _HUBH, 14, sc="1.08", op=".32", dur="3.6s"))
    o.append(box(_HUBX, _HUBY, _HUBW, _HUBH, 14, hot=True, i=7, cls="mo-breathe",
                 sty="--mo-dur:3.6s"))
    o.append(txt(840, _HUBY + 56, "Collections Agent", "ttl", size=32, anchor="middle", col=AC))
    o.append(txt(840, _HUBY + 92, "The hub that turns strategy, voice,", "sm", size=17,
                 anchor="middle"))
    o.append(txt(840, _HUBY + 116, "understanding and compliance into", "sm", size=17,
                 anchor="middle"))
    o.append(txt(840, _HUBY + 140, "one deliverable conversation", "sm", size=17, anchor="middle"))
    o.append(txt(840, _HUBY + 166, "Not a bot &#8212; a system capability", "sm", size=15,
                 anchor="middle", col=AC))
    o.append(legend(24, 528, [("solid", "Main data flow"), ("dash", "Events / control"),
                              ("dot", "Metrics feedback")]))
    return "".join(o)
page("content", "".join([
    head("SOLUTION ARCHITECTURE &#183; CAPABILITY LOOP",
         "The capability loop of a <strong>collections agent</strong>."),
    lab(120, 244, "01 &#183; HUB AND EIGHT MODULES", w=1200),
    figbox(120, 276, 1680, 1680, 560, _hub_fig(), i=1),
    rule(850),
    # 治理要求带（2026-08-30 · GPT review P1-11 采纳-轻）。
    # ⚠ 措辞是**要求框架**，不是产品功能声明 —— 写的是「a compliant deployment must
    #   provide」，不是「we provide」。架构图右侧四个输出模块讲的是能力，
    #   这一带讲的是**验收标准**；两件事写成一件就是过度承诺。
    fnote(120, 866, 1680, 74,
          "GOVERNANCE REQUIREMENTS &#183; ACCEPTANCE CRITERIA, NOT A FEATURE LIST",
          "A compliant deployment must provide: <b>PII masking &amp; encryption</b> &#183; "
          "<b>recording &amp; summary retention</b> &#183; <b>AI disclosure &amp; consent</b> "
          "&#183; <b>audit logs</b> &#183; <b>human handover</b> &#183; "
          "<b>emergency stop</b>.", i=8),
    land("AI collections is not one bot &#8212; it is a "
         "<strong style='color:var(--accent)'>system capability</strong>; "
         "the loop is that feedback line, not the eight boxes."),
]))

# ═══ P12 · Why Agora ·「让语音 AI 从 Demo 走向生产可用」════════════════════════
#   硬数一律用司内 canon（见文件头「已核事实」⑤）。
#   模型生态那一条按 Colin 点名强调 **bring your own ASR/TTS/LLM per market and language,
#   no vendor lock-in** —— 这是 SEA 多语言市场的真论点；
#   **不声称任何具体语种支持**（越南语 / 泰语 ASR 口径未核，见交付报告）。
#   底部 SD-RTN 底座带：一条**双向**通道（上行客户语音 / 下行智能体语音），
#   包在两条道上同时在途 = 全双工。两枚规模数钉在带上（都带口径标）。
#   本页无 .mo-breathe：hot 语汇让给 .card.on（实时交互是四能力之首）。
_CAP4 = [
    ("01 &#183; REAL-TIME", "Real-time interaction",
     "End-to-end response as low as <b style=\"color:var(--accent)\">650ms</b>; barge-in "
     "captured in <b style=\"color:var(--accent)\">340ms</b>. Graceful interruption keeps "
     "the rhythm human.", True),
    ("02 &#183; AUDIO", "Audio engineering",
     "<b style=\"color:var(--accent)\">95%</b> environmental-interference shielding: SAL "
     "selective attention lock, AI-VAD and echo cancellation.", False),
    ("03 &#183; ECOSYSTEM", "Model ecosystem",
     "Bring your own ASR, TTS and LLM per market and language &#8212; no vendor lock-in.", False),
    ("04 &#183; PRODUCTION", "Production scale",
     "Recording, transcription, monitoring and quality analysis; AI QoS holds the call on "
     "weak and dropping networks.", False),
]
def _sdrtn_fig():
    o = []
    o.append(domain_band(300, 24, 1080, 128, "SD-RTN &#183; SOFTWARE-DEFINED REAL-TIME NETWORK"))
    for (x, t, s) in [(20, "Collections Agent", "Strategy &#183; reasoning &#183; script"),
                      (1444, "Customer handset", "Mobile network &#183; varied devices")]:
        o.append(box(x, 46, 216, 84, 8, i=2))
        o.append(txt(x + 108, 80, t, "ttl", size=20, anchor="middle"))
        o.append(txt(x + 108, 108, s, "sm", size=13, anchor="middle"))
    for k, (y, lb, rev) in enumerate([(66, "Downlink &#183; agent speech", False),
                                      (110, "Uplink &#183; customer speech", True)]):
        d = "M248 %d H1432" % y
        o.append(packet(d, 1184, seg=26, dur="3.4s", i=k + 2, rev=rev,
                        delay="-%.1fs" % (k * 1.7)))
        o.append(hline(248, 1432, y, AC, 2.4, k + 2))
        o.append(ah_r(1436, y, AC, 8) if not rev else ah_l(244, y, AC, 8))
        o.append(txt(1424, y - 12, lb, "sm", size=14, col=I3, anchor="end")
                 if not rev else txt(316, y - 12, lb, "sm", size=14, col=I3))
    # 节点脉冲（七枚，0.4s 错峰 ⇒ 一道亮波沿网横穿）：它们就是「200+ global nodes」的图形
    for k in range(7):
        o.append('<circle class="pop mo-pulse" style="--i:%d;--mo-hi:.55;--mo-lo:.16;'
                 '--mo-dur:2.8s;--mo-del:%.1fs;fill:%s;opacity:.55" cx="%d" cy="88" r="8"/>'
                 % (k % 4 + 2, k * .4, AD, 370 + k * 160))
    for (x, v, u, note) in [(300, "90B+", "minutes of real-time audio/video supported monthly",
                             "Public IR disclosure"),
                            (900, "200+", "global nodes &#183; SD-RTN", "Public IR disclosure")]:
        o.append(txt(x, 216, v, "ttl", size=42, col=AC, weight=700))
        o.append(txt(x, 246, u, "sm", size=17))
        o.append(txt(x, 270, note, "sm", size=13, col=I3, mono=True, ls=".12em"))
    o.append(legend(1330, 240, [("solid", "Real-time audio &#183; both ways live")]))
    return "".join(o)
page("content", "".join([
    head("WHY AGORA &#183; FROM DEMO TO PRODUCTION",
         "Agora takes voice AI from demo to <strong>production</strong>."),
    lab(120, 244, "01 &#183; FOUR CAPABILITIES"),
    sh("", "left:120px;top:278px;width:1680px;height:250px",
       '<div class="g4" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d"><div class="tag%s">%s</div>'
           '<div class="t">%s</div><div class="d">%s</div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag, _t, _d)
           for _i, (_tag, _t, _d, _on) in enumerate(_CAP4)) + '</div>'),
    # 供应商生态实证行（2026-08-30 · Colin ①，出处 docs.agora.io TTS overview）。
    # ⚠ 位置在四张能力卡**之外**：四卡内容高已经吃到 209/190，往卡里再塞当场冲出卡底
    #   （QA 的 cardspill 闸阈值 6px）。
    # ⚠ 字号 14px（.scope.tight）：这句在 16px 下量到 1753px > 可用宽 1656 会折行，
    #   14px 是 1534px ⇒ 单行落定。英文版重算版式账，与文件头 ②③ 同一条理由。
    # ⚠ 表述**限定在 vendor 侧**：语种覆盖跟着供应商走，我们不替任何一家供应商
    #   声明它支持哪一种语言（那是他们的口径，不是我们的）。
    scopenote(534, "<b>17+ TTS providers integrated</b> &#8212; Microsoft Azure, ElevenLabs, "
                   "Google, Amazon Polly, OpenAI, MiniMax and more; ASR/LLM equally pluggable. "
                   "Language coverage follows your vendors &#8212; Microsoft Azure alone ships "
                   "Vietnamese and Thai voices.", i=5, cls="tight", nogate="vendor"),
    lab(120, 570, "02 &#183; INFRASTRUCTURE &#183; RUNNING ON A REAL-TIME INTERACTION BACKBONE",
        w=1200, i=6),
    figbox(120, 602, 1680, 1680, 312, _sdrtn_fig(), i=7),
    rule(850),
    # 2026-08-30 · Colin ③：OpenAI 口径改成 OpenAI 官方发布文可验的表述。
    #   「global first-batch partner」是我们的转译，官方文里没有「首批」这个层级；
    #   「named an integration partner at the launch」是发布文里点得到名的事实。
    #   ⚠ 中文版的 canon **本轮不动**（家族级口径变更待 Colin 拍板，见交付报告）。
    land("Agora was <strong style='color:var(--accent)'>named an integration partner</strong> "
         "at the 2024 OpenAI Realtime API launch.", y=944),
    src(_SRC_AGORA),
]))

# ═══ P13 · Rollout ·「从低风险场景切入，逐步扩展到智能协商」═══════════════════
#   顶部一条**递增梯**（不是并列三卡）——三阶段的关系是「风险与复杂度逐级抬升」，
#   梯形本身就是这句话；包沿梯面向上跑 = 「从阶段 1 走上去」，不是「三选一」。
#   触达渠道本地化与 P5 同源（Zalo / WhatsApp / LINE / KakaoTalk）。
_STAGES = [
    ("Stage 1", "Reminders and confirmation",
     ["Statement reminders", "Pre-due-date reminders", "Early-stage M0 / M1 reminders",
      "Promise-to-pay due reminders", "Sending and confirming payment links"]),
    ("Stage 2", "Follow-up and explanation",
     ["Promise-to-pay follow-up", "Explaining installment options",
      "Collecting reasons for arrears", "Document top-up reminders",
      "Answering basic customer questions"]),
    ("Stage 3", "Negotiation and QA",
     ["First-pass capacity-to-repay assessment", "Personalized plan recommendations",
      "Complex disputes routed to a human", "Complaint-risk detection",
      "Quality review of outsourced collections", "Real-time agent assist"]),
]
_ADVICE = [
    ("PICK ONE PRODUCT", "Credit card, consumer loan or installment"),
    ("PICK ONE AGING BAND", "Start at <b>M0 / M1</b> or payment reminders"),
    ("PICK A LOW-DISPUTE SEGMENT", "Avoid complaints, disputes and legal cases"),
    ("SET A PILOT WINDOW", "<b>4&#8211;8 weeks</b> against the current process"),
]
def _ladder_fig():
    """三级台阶：细横条 + 上方标名，不是三只大盒子 ——
       大盒子会和下面的三张卡讲同一件事两遍，梯子只负责说「越往右越难」。"""
    o = []
    for k, (_s, _t, _bs) in enumerate(_STAGES):
        x, y, w = 40 + k * 552, 90 - k * 28, 500
        # ⚠ 前两条自带 opacity:.5 ⇒ --mo-hi 必须跟着写 .5（moPulse 的 0%/100% 帧是它），
        #   不写就会被动画顶成 1，SELFPIN 的「100% 帧 = 静态原图」当场对不上。
        _hi = None if k == 2 else ".5"
        _v = "--i:%d;--mo-lo:%s;--mo-dur:3.6s;--mo-del:%.1fs" % (k + 1, ".16" if k == 2 else ".2", k * .6)
        if _hi: _v += ";--mo-hi:%s" % _hi
        o.append('<rect class="pop mo-pulse" style="%s;fill:%s%s" x="%d" y="%d" width="%d" '
                 'height="10" rx="5"/>' % (_v, AC, (";opacity:%s" % _hi) if _hi else "", x, y, w))
        o.append(txt(x + w // 2, y - 14, "%s &#183; %s" % (_s, _t), "ttl", size=22,
                     anchor="middle", col=AC if k == 2 else None))
        if k < 2:
            x1, x2 = x + w, x + w + 52
            d = "M%d %d L%d %d" % (x1 + 4, y + 5, x2 - 14, y - 23)
            o.append(packet(d, 56, seg=16, dur="1.6s", i=k + 1, delay="%.1fs" % (k * .5)))
            o.append(pline(d, AC, 2.4, k + 1, ln=56))
            o.append(ah_r(x2 - 2, y - 27, AC, 8))
    o.append(txt(40, 30, "Risk and complexity rise step by step", "sm", size=16, col=I3))
    # 起步基线走 .mo-drift（图例写的是虚线，线必须真的是虚的）：
    # off −180 = dash「4 6」周期 10 的 18 个整周期 ⇒ 100% 帧 = 静态原图。
    o.append(dline("M40 116 H1640", HS, 1.4, 1, dash="4 6", cls="mo-drift",
                   sty="--mo-off:-180;--mo-dur:5s"))
    o.append(legend(40, 146, [("solid", "Stepping up &#183; extend by stage"),
                              ("dash", "Starting baseline")]))
    return "".join(o)
page("content", "".join([
    head("ROLLOUT &#183; THREE STAGES",
         "Start low-risk, then extend to <strong>negotiation</strong>."),
    lab(120, 244, "01 &#183; THREE STAGES"),
    figbox(120, 272, 1680, 1680, 160, _ladder_fig(), i=1),
    # ⚠ 场景条目走**一枚 .d 里的 <br> 列表**，不是六个 .d 子元素：.card 的 flex gap 是 13px，
    #   六个子元素就是 78px 的额外高度，会把阶段 3 的后两条挤出卡底。
    sh("", "left:120px;top:444px;width:1680px;height:300px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card sm%s rise" style="--i:%d"><div class="tag%s">%s &#183; %s</div>'
           '<div class="d" style="line-height:1.85">%s</div></div>'
           % (" on" if _i == 0 else "", 2 + _i, " am" if _i == 0 else "", _s, _t,
              "<br>".join("&#183; " + _b for _b in _bs))
           for _i, (_s, _t, _bs) in enumerate(_STAGES)) + '</div>'),
    lab(120, 768, "02 &#183; PILOT DESIGN", i=6),
    sh("flow", "left:120px;top:794px;width:1680px;height:48px;--i:7",
       '<div class="adv">' + "".join(
           '<div><div class="h">%s</div><div class="b">%s</div></div>' % (_h, _b)
           for _h, _b in _ADVICE) + '</div>'),
    rule(850),
    # ── 页脚注带（2026-08-30）：左 proof point（Colin ②）· 右 试点第五条（GPT P1-12）──
    # ⚠ 为什么第五条不并进上面那排 `.adv`：五等分后每格净宽只剩 302px，
    #   现有四条里最长的一条实测 364px，五列一上全部折行、当场冲出 48px 的盒
    #   （QA 的 .adv>div cardspill 闸阈值 6px）。两件都是「试点建议区的注脚」，
    #   同排落在收口线之下，语域一致，中英两版结构逐格对齐。
    fnote(120, 858, 860, 74, "PROOF POINT &#183; AGORA PRODUCTION DEPLOYMENT (ANONYMIZED)",
          "A leading outbound calling deployment in China now runs "
          "<b>1,000,000+</b> calls per day.", on=True, i=8),
    fnote(1020, 858, 780, 74, "05 &#183; SET A HOLDOUT",
          "Hold out a control group; pre-set the primary metric and compliance guardrails.",
          i=8),
    land("Prove the loop in low-dispute, high-repetition work first &#8212; "
         "<strong style='color:var(--accent)'>no need to replace the whole chain at once</strong>.",
         y=944),
    src(_SRC_PROOF),
]))

# ═══ P14 · Pilot KPI ═══════════════════════════════════════════════════════
#   ⚠ 全页不出现任何百分比数字：本页讲的是**要量什么**，不是「能提升多少」。
#   注意事项的措辞是本 deck 的免责边界，按 Colin 点名逐字定：
#     "Do not commit to a fixed uplift before you have pilot data from your own book."
#     "The safer statement: validate improvement headroom on contact, fulfillment,
#      cost and compliance through a pilot."
_KPI = [
    ("01", "Contact", ["Connect rate", "Effective conversation rate", "SMS / link click rate"]),
    ("02", "Recovery", ["Promise-to-pay rate", "Promise fulfillment rate", "Amount recovered",
                        "Aging migration rate"]),
    ("03", "Efficiency", ["Cost per case contacted", "Agent substitution rate",
                          "Human handover rate", "Average handling time"]),
    ("04", "Compliance", ["Complaint rate", "Non-compliant script hits", "QA coverage",
                          "Recording &amp; summary coverage"]),
    ("05", "Experience", ["Call drop-off rate", "Share of negative sentiment",
                          "Negotiation success rate"]),
]
page("content", "".join([
    head("PILOT KPI &#183; HOW TO MEASURE",
         "Prove the value with <strong>measurable indicators</strong>."),
    lab(120, 244, "01 &#183; FIVE FAMILIES OF INDICATORS"),
    sh("", "left:120px;top:276px;width:1680px;height:380px",
       '<div class="g5 kpi" style="height:100%">' + "".join(
           '<div class="card rise" style="--i:%d"><div class="n">%s</div>'
           '<div class="t">%s</div><div class="m">%s</div></div>'
           % (2 + _i, _n, _t, "<br>".join("&#183; " + _m for _m in _ms))
           for _i, (_n, _t, _ms) in enumerate(_KPI)) + '</div>'),
    lab(120, 692, "02 &#183; CAVEAT", i=5),
    # 2026-08-30：caveat 从两栏改三栏，补一条**口径字典**要求（GPT P1-13 采纳-轻）。
    # 版式账：三栏每栏净宽 (1680 − 2×32)/3 − 27 = 511.7px；英文在 20px 下第二条要三行
    #   （3×32 + 12 = 108 > 盒高 88）⇒ 三条一律降到 18px：最长一条量得 918px ⇒ 两行，
    #   2×28.8 + 12 = 69.6 ≤ 88 ✓。**加第四条必须重算这一笔。**
    sh("flow", "left:120px;top:724px;width:1680px;height:88px;--i:6",
       '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:32px;height:100%">'
       '<div class="note grey" style="font-size:18px;align-self:center">'
       'Do not commit to a fixed uplift before you have pilot data from your own book.</div>'
       '<div class="note" style="font-size:18px;align-self:center">'
       'The safer statement: validate <b style="color:var(--accent)">improvement headroom</b> '
       'on contact, fulfillment, cost and compliance through a pilot.</div>'
       '<div class="note grey" style="font-size:18px;align-self:center">'
       'Every KPI ships with a <b style="color:var(--accent)">metric dictionary</b>: '
       'definition, numerator, denominator, time window and de-duplication.</div></div>'),
    rule(850),
    land("A pilot does not produce a promise &#8212; it produces "
         "<strong style='color:var(--accent)'>your own control data</strong>."),
]))

# ═══ P15 · Closing（title 板）══════════════════════════════════════════════
#   收尾语渲染成**一段连续文本**（不拆成三栏）——三栏视觉更漂亮，但那样
#   textContent 里的分号与句读就断了。
#   版式账：主标 60px 双行，行盒 60×1.32 = 79.2，双行 158px ⇒ 落进 y176 起的 200px 盒。
#   （行高同 .hh 的 1.32，理由见 DECK_CSS 里 .hh 那一段：低于 1.25 会被 .ink 的 mask 切顶。）
_VERDICT = [
    "Overdue asset management is a standing capability, not a short-term operating task.",
    "The limits of the traditional model on productivity, compliance and experience keep "
    "getting clearer.",
    "AI can replicate strong agent behavior, compliance rules and operating strategy at scale.",
    "The future of collections is smarter, more compliant and more open to negotiation.",
]
page("title", "".join([
    sh("flow kk", "left:120px;top:118px;width:1680px;height:28px;text-align:center",
       "CLOSING &#183; WHERE THIS GOES"),
    sh("ink", "left:120px;top:176px;width:1680px;height:200px;text-align:center;"
       "font:700 60px/1.32 var(--f-cn);letter-spacing:-.018em;color:var(--ink)",
       "The future of collections is<br>AI + <strong style='color:var(--accent)'>compliance"
       "</strong> + real-time interaction infrastructure."),
    sh("spread", "left:900px;top:414px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow", "left:120px;top:472px;width:1680px;height:130px;--i:4",
       '<div class="g4" style="height:100%">' + "".join(
           '<div style="border-top:1px solid var(--hair);padding-top:18px;'
           'display:flex;flex-direction:column;gap:10px">'
           '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.16em;color:var(--ink-3)">'
           '0%d</div>'
           '<div style="font:400 19px/1.5 var(--f-cn);color:var(--ink-2)">%s</div></div>'
           % (_i + 1, _v) for _i, _v in enumerate(_VERDICT)) + '</div>'),
    sh("ink", "left:260px;top:640px;width:1400px;height:200px;text-align:center;"
       "font:700 38px/1.6 var(--f-cn);letter-spacing:-.01em;color:var(--ink)",
       "AI handles <strong style='color:var(--accent)'>scale, standardization and real-time "
       "analysis</strong>; humans handle <strong style='color:var(--accent)'>complex judgment, "
       "empathy and exceptions</strong>; Agora provides the "
       "<strong style='color:var(--accent)'>real-time voice infrastructure</strong> "
       "that connects AI to real customer conversations."),
    # 收尾证据句（2026-08-30 · Colin ②）：整份 deck 到这里全是论证，
    # 最后给一条**已经在跑**的脱敏证据。收尾语三分句一个字不动，证据另起一行。
    # 摆位：收尾语三行到 y822 收住，证据句压在下面 —— 与 y892 的页脚带留出 44px。
    sh("flow", "left:120px;top:840px;width:1680px;height:32px;text-align:center;--i:5",
       '<span class="pfline">A leading outbound calling deployment in China now runs '
       '<b>1,000,000+</b> calls per day.</span>'),
    sh("flow mono-sm", "left:120px;top:892px;width:1680px;height:24px;text-align:center;--i:6",
       "AGORA &#183; CONVERSATIONAL AI ENGINE &#183; REAL-TIME VOICE AI INFRASTRUCTURE"),
    # CTA：纯文本 mono 行，不做假链接样式（没有 <a>，不加下划线 / 悬停态）
    sh("flow mono-sm", "left:120px;top:930px;width:1680px;height:24px;text-align:center;--i:7",
       "DEMO / DOCS &#183; agora.io &#8250; Conversational AI Engine &#183; Contact the team"),
]))


# ═══ 组装 ═══════════════════════════════════════════════════════════════════
# 语言切换钮（两份 deck 同款；本文件负责英文版那一枚：「中文」→ /convoai-postloan）。
# ⚠ 必须 <button> + JS，不能用 <a>（a[href]=0 闸）。
# ⚠ 字体栈显式带 CJK 回退：JetBrains Mono 不覆盖「中文」二字。
LANG_CSS = (
    '<style>.deck-lang{position:fixed;left:26px;bottom:62px;z-index:1100;'
    "font-family:'JetBrains Mono','SF Mono',ui-monospace,'PingFang SC','Noto Sans CJK SC',"
    "'Noto Sans SC',monospace;"
    'font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);'
    'border-radius:3px;padding:7px 12px;opacity:.62;'
    'transition:opacity .3s,color .3s,border-color .3s;background:var(--card-bg-2);cursor:pointer;}'
    '.deck-lang:hover,.deck-lang:focus-visible{opacity:1;color:var(--accent);border-color:var(--accent);}'
    '.deck-lang:focus:not(:focus-visible){outline:none;box-shadow:none;}'
    '@media print{.deck-lang{display:none!important;}}</style>\n')
LANG_JS = (
    '<script>(function(){var b=document.getElementById("deckLang");if(!b)return;'
    'b.addEventListener("click",function(){b.blur();'
    # 预览服务器是静态目录服务（没有 rewrites），线上才有 /convoai-postloan 路由：
    # 按当前 pathname 是否带 .html 二选一，两个环境都跳得通。
    'var f=/\\.html($|[?#])/.test(location.pathname);'
    'location.href=f?"/decks/convoai-postloan.html":"/convoai-postloan";});})();</script>\n')

def build():
    total = len(PAGES)
    secs = []
    for i, (board, body) in enumerate(PAGES, 1):
        sig = '<div class="sig">%d/%d</div>' % (i, total)
        secs.append(
            '<section class="slide conf-boarded" data-p="%d" data-steps="0">\n'
            '  <div class="conf-bg conf-bg-%s" aria-hidden="true"></div>\n'
            '  <div class="pp">%s%s</div>\n</section>' % (i, board, sig, body))
    chrome = ('<div class="deck-grid" aria-hidden="true"></div>'
              '<div class="deck-rail t" aria-hidden="true"></div>'
              '<div class="deck-rail b" aria-hidden="true"></div>')
    doc = (
        '<!DOCTYPE html>\n<html lang="en"><head>\n'
        # 主题初始化：与 convoai-engine / convoai-info / 中文版同一个 localStorage 键
        '<script>try{if(localStorage.getItem("colin-theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}</script>\n'
        '<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>AI-Powered Post-Loan Collections &amp; Overdue Asset Management</title>\n'
        + FONTS
        + "<style>" + css("conf-theme-dual.css") + "</style>"
        + "<style>" + css("stage.css") + "</style>"
        + "<style>" + css("motion.css") + "</style>"
        + "<style>" + css("components.css") + "</style>"
        + "<style>" + css("conf-chrome.css").split("<svg class=\"deck-flow\"")[0] + "</style>"
        + BOARDS_CSS + DECK_CSS
        + "\n</head>\n<body>\n"
        '<div class="deck-viewport">\n  <div class="deck-stage" id="deckStage">\n'
        + chrome + "\n" + "\n".join(secs) + "\n  </div>\n</div>\n"
        '<div class="deck-progress" id="deckProgress"></div>\n'
        '<div class="deck-steps" id="deckSteps"></div>\n'
        '<div class="edit-hotzone" aria-hidden="true"></div>\n'
        '<button class="edit-toggle" id="editToggle">EDIT</button>\n'
        '<button class="deck-swap" id="deckSwap">DARK</button>\n'
        '<button class="deck-lang" id="deckLang">中文</button>\n'
        # deckSwap 常显 chip（与中文版逐字同源）：这是一份**发链接**的私享 deck，
        # 「默认隐身 · hover 呼出」在这里等于键不存在。
        '<style>.deck-swap{position:fixed;left:26px;bottom:24px;z-index:1100;font-family:var(--f-mono,monospace);'
        'font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);'
        'border-radius:3px;padding:7px 12px;opacity:.62;'
        'transition:opacity .3s,color .3s,border-color .3s;background:var(--card-bg-2);cursor:pointer;}'
        '.deck-swap:hover,.deck-swap:focus-visible{opacity:1;color:var(--accent);border-color:var(--accent);}'
        '.deck-swap:focus:not(:focus-visible){outline:none;box-shadow:none;}'
        '@media print{.deck-swap{display:none!important;}}</style>\n'
        + LANG_CSS
        + "<script>" + (SRC / "deck.js").read_text(encoding="utf-8") + "</script>\n"
        '<script>(function(){var b=document.getElementById("deckSwap");'
        'function apply(t){if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");b.textContent="LIGHT";}'
        'else{document.documentElement.removeAttribute("data-theme");b.textContent="DARK";}}'
        'var cur="light";try{cur=localStorage.getItem("colin-theme")||"light";}catch(e){}apply(cur);'
        'window.__setTheme=apply;'
        'b.addEventListener("click",function(){b.blur();'
        'var now=document.documentElement.getAttribute("data-theme")==="dark"?"dark":"light";'
        'var nxt=(now==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",nxt);}catch(e){}apply(nxt);});})();</script>\n'
        + LANG_JS
        + "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")

    # ── 构建期断言（红线在这里就拦住，别等到 qa）──────────────────────────────
    _stage_html = "\n".join(secs)
    _plain = re.sub(r"<[^>]+>", " ", _stage_html)
    _low = _plain.lower()
    assert total == 15, "页数漂移：%d != 15" % total
    assert doc.count("<section") == 15, "section 数漂移：%d" % doc.count("<section")
    boards = {i: b for i, (b, _y) in enumerate(PAGES, 1)}
    assert {i for i, b in boards.items() if b == "title"} == {1, 15}, \
        "title 板页漂移：%r" % sorted(i for i, b in boards.items() if b == "title")
    assert doc.count('data-steps="0"') == 15, "data-steps 不全为 0"
    assert 'data-step="' not in _stage_html, "出现了 [data-step] —— 本 deck 是零分步 deck"
    # 措辞红线（大小写不敏感，子串匹配）
    for _bad in ("debt chasing", "chase debtors", "pressure tactics",
                 "aggressive collection", "harass", "intimidat"):
        assert _bad not in _low, "表达红线：全 deck 不许出现「%s」" % _bad
    # `threaten` 只准出现一次，且必须落在 P7 的 [data-nogate] 节点里
    assert _low.count("threaten") == 1, \
        "红线：threaten 出现 %d 次 —— 只准 P7 引述监管禁令那一处" % _low.count("threaten")
    _ng = re.findall(r'<div data-nogate="threaten">(.*?)</div>\s*</div>', _stage_html, re.S)
    assert len(_ng) == 1 and "threaten" in _ng[0].lower(), \
        "红线：threaten 不在 [data-nogate] 豁免节点内"
    # 客户名 / 产品名 / 价格 / staging / 盲测
    for _bad in ("光潽", "Call Agent", "8,500", "2,999", "5,501",
                 "staging", "32,000"):
        assert _bad not in doc, "红线：全 deck 不许出现「%s」" % _bad
    # 已仲裁：英文官网旧口径不许回归 / 中国市占信任状不进英文版
    for _bad in ("80 billion minutes", "200+ countries", "IDC", "No.1 in China"):
        assert _bad not in _stage_html, "口径红线：「%s」已仲裁不进英文版" % _bad
    # a[href] = 0（指路走纯文本；语言钮是 <button>）
    assert "<a " not in doc.split('id="deckStage"')[1].split("</div>\n</div>")[0], \
        "舞台里出现了 <a> —— 本 deck 指路必须是纯文本"
    # **CJK 纯度闸**：舞台里一个 CJK 字符都不许有（语言钮在舞台之外，不受此闸）
    _cjk = re.findall(r"[　-〿㐀-䶿一-鿿＀-￯]", _plain)
    assert not _cjk, "CJK 纯度闸：舞台里出现了 %r" % sorted(set(_cjk))[:12]
    # 语言钮：<button> + 「中文」+ 指向中文版
    assert '<button class="deck-lang" id="deckLang">中文</button>' in doc, "缺语言切换钮"
    assert '/convoai-postloan' in LANG_JS, "语言钮未指向中文版"
    # 百分数白名单：整份 deck 只准 95% 与 9.72%
    _pcts = set(re.findall(r"\d+(?:\.\d+)?%", _plain))
    assert _pcts <= {"95%", "9.72%"}, \
        "红线：出现未登记的百分数 %r —— 本 deck 不承诺任何提升比例" % sorted(_pcts - {"95%", "9.72%"})
    # SOURCE ledger：五张数据页（P3/P4/P7/P9/P12）各一行、严格四段制、Facts as of 2026.08 收尾
    _srcs = re.findall(r'<div class="sh flow src"[^>]*>(SOURCE[^<]*)</div>', doc)
    # 2026-08-30：P13 落了一枚脱敏 proof point（生产部署口径的外部事实）⇒ 入册，六行。
    assert len(_srcs) == 6, "SOURCE ledger 行数漂移：%d != 6（%r）" % (len(_srcs), _srcs)
    for _s in _srcs:
        _t = _s.replace("&#183;", "·").replace("&amp;", "&")
        assert _t.startswith("SOURCE · "), "SOURCE 行不以「SOURCE · 」起手：%r" % _t
        assert _t.endswith(" · Facts as of 2026.08"), "SOURCE 行未以 Facts as of 收尾：%r" % _t
        assert _t.count(" · ") == 3, "SOURCE 行不是四段制：%r" % _t
        assert "http" not in _t, "SOURCE 行写了 URL —— 家族格式只写机构名：%r" % _t
    # 事实在场闸（一个都不许在改版里被搬丢）
    _page_txt = {int(x.split('"')[0]): x
                 for x in doc.split('<section class="slide conf-boarded" data-p="')[1:]}
    for _p, _kws in [(3, ["e-Conomy SEA 2025", "Google, Temasek", "Digital lending",
                          "e-wallet"]),
                     (4, ["61/2020/QH14", "01.01.2021", "prohibited business investment",
                          "National Assembly of Vietnam"]),
                     (7, ["18/2019/TT-NHNN", "43/2016", "Article 7", "01.01.2020",
                          "5 reminders per day", "07:00", "21:00",
                          "No contact with non-obligor third parties",
                          "OJK", "BSP", "BOT", "MAS"]),
                     (9, ["5.98", "13.77", "9.72", "4.9", "9.3",
                          "Fortune Business Insights", "Grand View Research"]),
                     (12, ["650ms", "340ms", "95%", "90B+", "200+", "SAL",
                           "AI-VAD", "Graceful interruption", "AI QoS",
                           "named an integration partner", "no vendor lock-in"])]:
        for _kw in _kws:
            assert _kw in _page_txt[_p], "P%d 缺在场事实「%s」" % (_p, _kw)
    # ── 2026-08-30 修订集在场闸（改一处就得在这里对上一处）─────────────────────
    # A 版本标
    assert "SEA EDITION" in _page_txt[1] and "VIETNAM ANCHOR" in _page_txt[1], "P1 缺版本标"
    # B 判断标：只在 P2 / P8 / P10（判断）与 P9（品类代理指标），各一枚，别处零枚
    for _p in range(1, 16):
        _n = _page_txt[_p].count('class="vtag"')
        _exp = 1 if _p in (2, 8, 9, 10) else 0
        assert _n == _exp, "P%d 的 .vtag 数 %d != %d" % (_p, _n, _exp)
    for _p in (2, 8, 10):
        assert "AGORA VIEW" in _page_txt[_p], "P%d 的判断标未写 AGORA VIEW" % _p
    # C 口径限定
    assert "GLOBAL CATEGORY PROXY" in _page_txt[9] and "NOT YOUR SAM" in _page_txt[9], \
        "P9 缺代理指标标注"
    assert "GVR spans non-financial use cases" in _page_txt[9], "P9 缺两报告口径差异小注"
    # D P4 措辞弱化：THE ONLY PATH / No alternative 都不许回归
    for _bad in ("THE ONLY PATH", "No alternative"):
        assert _bad not in _page_txt[4], "P4 措辞红线：「%s」已弱化，不许回归" % _bad
    for _kw in ("WHAT REMAINS", "prohibited business line",
                "Lenders retain responsibility", "not a statutory mandate"):
        assert _kw in _page_txt[4], "P4 缺弱化后的论证句「%s」" % _kw
    # E P7 精度
    assert "FINANCE-COMPANY GUARDRAILS" in _page_txt[7], "P7 kicker 未收紧适用范围"
    assert "VIETNAM AND THE REGION" not in doc, "P7 旧 kicker「VIETNAM AND THE REGION」不许回归"
    assert "consumer-lending framework for" in _page_txt[7], "P7 缺适用范围小注"
    assert "REGULATOR NAMES ONLY" in _page_txt[7], "P7 区域条未写明只列机构名"
    # F1 vendor 生态：名单挂在 [data-nogate="vendor"] 里，全 deck 只此一枚
    assert doc.count('data-nogate="vendor"') == 1, "vendor 豁免节点应恰好一枚"
    for _kw in ("17+ TTS providers integrated", "Microsoft Azure", "ElevenLabs",
                "Amazon Polly", "MiniMax", "Language coverage follows your vendors"):
        assert _kw in _page_txt[12], "P12 缺 vendor 生态「%s」" % _kw
    assert "Agora docs" in _page_txt[12], "P12 的 SOURCE 行未补 Agora docs 出处"
    # F2 极致三件的限定词（as low as / typical values）—— 一个都不许被抹掉
    assert "as low as" in _page_txt[12], "P12 缺「as low as」限定词"
    assert "typical values" in _page_txt[12], "P12 的 SOURCE 行缺 typical values 限定"
    # F3 OpenAI 口径：旧转译不许回归
    assert "global first-batch partner" not in doc, "P12 旧 OpenAI 转译不许回归"
    # G proof point：P13 side note + P15 收尾，两处逐字同源
    for _p in (13, 15):
        assert "A leading outbound calling deployment in China now runs" in _page_txt[_p] \
            and "1,000,000+" in _page_txt[_p], "P%d 缺 proof point" % _p
    assert "Agora production deployment (anonymized)" in _page_txt[13], \
        "P13 缺 proof point 的 SOURCE 归属"
    # H P3 规模证据带（两枚数都不许与 P12 重复）
    for _kw in ("ALREADY AT SCALE ON AGORA", "10,000", "1M+", "registered applications"):
        assert _kw in _page_txt[3], "P3 缺规模证据带「%s」" % _kw
    for _dup in ("10,000", "1M+"):
        assert _dup not in _page_txt[12], "P3 的规模数「%s」与 P12 撞车了" % _dup
    assert "Agora website" in _page_txt[3], "P3 的 SOURCE 行未补 Agora 出处"
    # I 轻量补强四件
    assert "span all eight stages" in _page_txt[5], "P5 缺全流程图注"
    assert "A compliant deployment must provide" in _page_txt[11], "P11 缺治理要求带"
    assert "ACCEPTANCE CRITERIA, NOT A FEATURE LIST" in _page_txt[11], \
        "P11 治理带缺「要求框架而非功能声明」的标头"
    assert "SET A HOLDOUT" in _page_txt[13], "P13 缺试点第五条"
    assert "metric dictionary" in _page_txt[14], "P14 caveat 缺口径字典一条"
    # J 美式拼写闸（构建期先拦一道，qa 里还有一道）
    for _bad in ("standardisation", "monetisation", "fulfilment", "judgement",
                 "personalised", "ageing", "dialling", "organis",
                 "instalment", "behaviour", "maximise", "standardised"):
        assert _bad not in _plain.lower(), "拼写闸：英式拼写「%s」不许出现（本 deck 全美式）" % _bad
    # fulfil 裸词干单独查（不能进上表——fulfilment 已改 fulfillment，含 fulfil 前缀会误伤）
    import re as _re
    assert not _re.search(r"\bfulfil\b", _plain, _re.I), "拼写闸：英式 fulfil 不许出现（美式 fulfill）"
    # 收尾语（Colin 点名的三分句）
    for _kw in ("scale, standardization and real-time analysis",
                "complex judgment, empathy and exceptions",
                "real-time voice infrastructure"):
        assert _kw in _page_txt[15], "P15 收尾语缺「%s」" % _kw
    # 试点 KPI 页的免责措辞
    for _kw in ("Do not commit to a fixed uplift", "improvement headroom"):
        assert _kw in _page_txt[14], "P14 缺免责措辞「%s」" % _kw
    # 每页至多一枚 .mo-breathe
    for _p, _t in _page_txt.items():
        _n = _t.count("mo-breathe")
        assert _n <= 1, "P%d 有 %d 枚 .mo-breathe —— 每页至多一枚 hot 件" % (_p, _n)
    print("convoai-postloan-en.html · %d 页 · %dKB · conf-light 默认 · 零分步 · "
          "SOURCE ledger %d 行 · CJK 纯度闸通过" % (total, len(doc) // 1024, len(_srcs)))

if __name__ == "__main__":
    build()
