#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-postloan.py ·《AI 驱动的智能贷后催收解决方案》15 页 · **私享**
# CONF 家族 · conf-light 默认 · 单文件双主题 —— 从 build-convoai-engine.py 抄骨架
#   （同一套 DECK_CSS token / conf-light·dark 背景板 / deck.js 运行时 / noindex /
#    五个运动原语逐字复用，不新造 keyframes 名）。
#
# ── 这份 deck 是什么 ───────────────────────────────────────────────────────
#   受众：银行 / 消费金融公司 / 互联网金融平台 / 小贷 / AMC 的贷后、风控、合规、
#   技术负责人。场景：销售方案汇报。定位是**引擎基础设施 + 解决方案**，
#   不是 Call Agent 产品页 —— 价格 / staging / 盲测 / 32,000 / 产品名一律不入。
#   发布形态：私享链接 /convoai-postloan，只在 deckRoutes 注册，不进任何索引数组。
#
# ── 内容蓝本（唯一）─────────────────────────────────────────────────────────
#   Colin_Knowledge_Vault/+Inbox/ai-debt-collection-ppt-outline.md
#   14 页大纲 + 第 4 节「建议补充页：试点 KPI」= 本 deck 的 15 页。
#   插入位置按 Colin 指令：**试点 KPI 插在落地场景（P13）之后** ⇒ 大纲 P14 结尾顺延为 P15。
#
# ── 数字与口径纪律（本 deck 的最高优先级，改任何一个数之前先读完这一段）────────
#   ① **行业侧数字逐字用大纲的**，一个不新造、不外推，每个都带大纲给的来源机构名 + 时点：
#        3.7 万亿 / 1.51% / 239.2 万亿   国家金融监督管理总局 · 2026Q1 末
#        6.87 亿张                        新华网转述人民银行数据 · 2026Q1 末
#        6.96 亿张                        中国人民银行清算总中心 · 2025 年末
#        5 年留痕 / 三不得                《消费金融公司管理办法》（湖南省人民政府转载）
#        GB/T 45251-2025                  全国标准信息公共服务平台 · 2025.02.28 发布实施
#        59.8 / 137.7 亿美元 · CAGR 9.72% Fortune Business Insights · 2025→2034
#        49 / 93 亿美元                   Grand View Research · 2023→2030
#   ② **Agora 侧硬数只用家族 canon**（从 build-convoai-engine.py 现行页逐字取）：
#        650ms 端到端 / 340ms 打断 / 95% 环境干扰屏蔽（引擎 P5 三件极致原句）
#        SAL 选择性注意力锁定 · AI-VAD · 优雅打断 · AI QoS 弱网（引擎 P7–P11）
#        900亿+ 单月支撑通话分钟数（引擎 P21 四卡之一）· 200+ 全球节点 SD-RTN（引擎 P21 页头注）
#        OpenAI Realtime API 全球首批合作伙伴（引擎 P22 锚点行）
#   ③ **已仲裁**：大纲 P12「800 亿分钟 / 200+ 国家和地区」是 agora.io 英文官网旧口径，
#        与司内现行 canon（900亿+ 单月分钟数 / 200+ **全球节点** SD-RTN）冲突 ——
#        本 deck **不用**大纲那一组，用家族 canon。理由：同一家公司在两份对外材料上
#        给出两个数量级不同的分钟数，客户当场就会问，而我们没有能自圆的口径。
#        「200+」的正确宾语是**节点**，不是国家和地区（引擎 deck 已就此纠过一次错）。
#
# ── 表达红线（构建期断言 + qa 反向闸双保险）──────────────────────────────────
#   六词全文 0 出现：催债 / 施压催收 / 逼迫还款 / 强催 / 轰炸外呼 / 暴力催收
#     ⚠「强催」是**子串**红线：写「加强催收管理」会当场触闸，本 deck 一律写
#       「完善催收管理」「催收管理制度」。规范原文里的「不得暴力、威胁、恐吓」
#       因为「暴力」后面跟的是顿号，不构成「暴力催收」，可以照抄。
#   「回收率」不得与具体百分比同句 —— 本 deck 不承诺任何提升比例（大纲风险提示）。
#   客户名一个不进（含「光潽」，内部在谈客户，反向闸点名）。
#   Call Agent 产品名 / 价格 / staging / 盲测 / 32,000 全不入。a[href] = 0。
#   「催收」一词本身可用（行业正名），但标题与叙事优先「贷后催收 / 逾期资产管理 /
#   智能运营」（大纲第 6 节推荐表达）。
#
# ── 家族硬指标 ────────────────────────────────────────────────────────────
#   · 五运动原语（mo-packet / mo-drift / mo-cycle / mo-pulse / mo-breathe + mo-halo 伴件）
#     keyframes 名逐字复用，不新造。
#   · 浅色默认（金融机构投屏），双主题齐备，deckSwap 常显 chip。
#   · .slide:not(.active) 暂停 / prefers-reduced-motion / print 三路关断。
#   · **全 deck 零分步**（data-steps 全 0、页内一枚 [data-step] 都没有）——
#     常显容器挂 data-step 会被 motion.css 的「裸容器 step0 → opacity:0」兜底规则
#     摁成透明整页（引擎 deck P19/P20 踩过），方案汇报场景也不需要分步。
#   · P8 质量语言六条（本 deck 的图页逐条对表，见各页页头注）：
#     ① 类型化线 + 图例   ② 每页唯一 hot 件（= 至多一枚 .mo-breathe）
#     ③ 线带「流的什么」标注                ④ 闭环优先
#     ⑤ 数字带时序标                        ⑥ 域分带
#   · SOURCE ledger 家族格式：`SOURCE · <来源名> · <样本或时间窗> · 事实截止 2026.08`
#     （来源写机构名，不写 URL —— 投屏上一条 URL 谁也读不出来，且会诱发点击。）
#
# 结构（15 页；★ = 大纲第 4 节的补充页）：
#   P1  封面（title 板）              P2  总览 · 五点逻辑链（flow 带 · 运动件）
#   P3  行业现状 · 万亿级底座         P4  存量经营 · 6.87 亿张 + 四象限
#   P5  产业链八环闭环（**标杆动效页** · cycle 原语环行）
#   P6  三难五拆（hot 三角 + 五难）   P7  合规倒逼（三不得 · 5 年留痕 · GB/T）
#   P8  五个趋势                      P9  市场三层空间（域分带 + 两条测算公式）
#   P10 AI 势在必行（六价值 + 七行对比表）
#   P11 智能催收 Agent 能力闭环（**第二动效重点** · 中枢 hub + 八模块）
#   P12 Agora 优势（四能力 + SD-RTN 底座带）
#   P13 落地三阶段 + 试点建议         P14 试点 KPI ★         P15 结尾（title 板）
#
# 重建：python3 scripts/build-convoai-postloan.py
# 自检：node scripts/qa-convoai-postloan.mjs（THEME=dark 二跑）
#      DECK=postloan node scripts/qa-motion.mjs
#      DECK_URL=…/convoai-postloan.html node scripts/occlusion-scan.mjs（双分辨率 × 双主题）
#      A=…/convoai-postloan.html SELFPIN=1 node scripts/pinned-diff.mjs
#
# ── 踩过的坑（与母版同一份，移植 SVG 必守）─────────────────────────────────
#   · svg 一律 style="width:100%;height:auto"，.sh 高度 = width×viewBoxH/viewBoxW
#   · SVG 里换色一律写内联 style="fill:…"（呈现属性压不过 .fig .lbl/.ttl 的 CSS fill）
#   · .dw 的 --len 必须≈路径长度，否则线不出来；虚线不能走 .dw（dasharray 会被压掉）
#   · content 背景板自带一条 accent 细线在 y848–852（x120–761）：那一带不放文字，
#     rule(850) 正好压住它当收口线
#   · 网格（.g2/.g3/.g4/.g5）一律写 height:100%，否则卡片溢出 .sh 盒 → TEXT-x-SPILL
# ═══════════════════════════════════════════════════════════════════════════
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
OUT = ROOT / "public" / "decks" / "convoai-postloan.html"
B = "/decks/assets/conf-boards/"

def css(name):
    return (SRC / name).read_text(encoding="utf-8")

FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>"""

# ── 背景板（两张：title 给 P1/P15，content 给其余）──────────────────────────
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

# ── 本 deck 专属 CSS（引擎版 DECK_CSS 的贷后版：删掉引擎专属的 r1-card / vid /
#    lock / nrow 件，保留 token 体系与 kk/hh/sub/seclab/rule/chip/card-c 家族组件）──
DECK_CSS = """<style id="convoai-postloan-deck">
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
/* 投影可读性（与 convoai-engine / convoai-info 逐字同源）：.sig 与 .src 各提一档。
   ⚠ 色阶只能走 color，不许用 opacity —— 入场系（.slide.visible .flow）本来就在动
     opacity，写在类上的那一档会被它整条压掉。 */
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 17px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--ink-3);}
.src{font:500 17px/1.4 var(--f-mono);letter-spacing:.08em;
  color:color-mix(in srgb,var(--ink-2) 55%,var(--ink-3));}
/* 版式件（与 convoai-engine 同源） */
.kk{font:700 20px/1 var(--f-mono);letter-spacing:.28em;color:var(--accent);}
.hh{font:700 68px/1.16 var(--f-cn);letter-spacing:-.02em;color:var(--ink);}
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
/* ══ deck 级运动语言 · 五个运动原语（从 build-convoai-engine.py 逐字复用）════════
   原语与语义一一对应（改页前先对表）：
     ① .mo-packet  能量包 —— 宽 stroke 低透明 dash 段沿实线主数据流漂移，方向与箭头一致。
        纯装饰件 ⇒ 静态语域直接 display:none。
     ② .mo-drift   虚线漂移 —— 事件 / 控制 / 参考线的 dash 慢爬，比包慢一档。
        载体是页面真线 ⇒ 静态语域只 animation:none，线本身照画。
     ③ .mo-pulse   脉冲 —— 命中 / 事件标 opacity 明暗，错峰 delay。载体自带 opacity 时
        必须把 --mo-hi 设成它的静态值，否则动画会把 opacity 顶成 1。
     ④ .mo-breathe hot 件呼吸 —— scale ≤1.03，**每页至多一处**，落在该页唯一 hot 件上；
        伴件 .mo-halo 是向外扩散的光晕（100% 帧 opacity:0 ⇒ 静态语域零痕迹）。
     ⑤ .mo-cycle   闭环绕行 —— 环 / 回路上的 dash 永续绕圈（P5 八环 / P11 质检回流弧）。
   纪律（硬红线，四条）：
     · 每条 keyframes 的 100% 帧 = 静态原图：dash 位移必须走完整周期（offset 是
       dasharray 周期的整数倍）、scale 回 1、opacity 回静态值、halo 回 0。
       自证工具 scripts/pinned-diff.mjs（SELFPIN=1）。
     · 动效元素不携带文字：文字要么在动效件之外，要么单拆一枚静态 text。
     · prefers-reduced-motion 与 print 全关（装饰件摘掉、真几何件停帧）。
     · 非当前页一律 animation-play-state:paused。 */
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
/* 静态语域（纸 / 降级）：装饰件摘掉，真几何件停在 100% 帧 */
@media print{
  .mo-packet,.mo-halo,.mo-ghost{display:none!important;}
  .mo-drift,.mo-cycle,.mo-pulse,.mo-breathe{animation:none!important;}}
@media (prefers-reduced-motion:reduce){
  .mo-packet,.mo-halo,.mo-ghost{display:none!important;}
  .mo-drift,.mo-cycle,.mo-pulse,.mo-breathe{animation:none!important;}}
/* 只有当前页在跑（.slide.active 由 deck.js 给，翻页即换） */
.slide:not(.active) .mo-packet,.slide:not(.active) .mo-drift,.slide:not(.active) .mo-cycle,
.slide:not(.active) .mo-pulse,.slide:not(.active) .mo-breathe,.slide:not(.active) .mo-halo{
  animation-play-state:paused;}
/* ── P10 七行对比表：8 行（1 表头 + 7 行）必须落进 rule(850) 以上的 300px 盒里 ────
   ⚠ 选择器必须写成 `table.mini.ai-diff`（0,2,3）：components.css 里的
     `table.mini tbody td`（0,1,3）比裸 `.ai-diff tbody td`（0,1,2）**更特指**，
     写弱了会被它整条压回 11px padding / 18px / 1.45 —— 第一版就是这么把最后
     两行（数据沉淀 / 客户体验）挤出 rule(850) 之外的，截图实锤。
   版式账：th ≈ 13×1.2 + 8 + 1 = 25；td = 8+8 + 17×1.3 + 1 = 39.1；
     25 + 7×39.1 = 299 ⇒ 落进 300 的盒。**加一行必须重算这一笔。** */
table.mini.ai-diff tbody td{padding:8px 14px 8px 0;font-size:17px;line-height:1.3;}
table.mini.ai-diff thead th{font-size:13px;padding-bottom:8px;}
/* AI 那一列整列上一层极淡 accent 底：表格的单元格文本都很短（「可弹性扩展」四个字），
   不给底色的话右边 40% 读起来像「表格没画完」。这是把域分带（P8 质量语言第 ⑥ 条）
   用到表上 —— 一列 = 一个域，色带把它整条圈出来，而不是靠七个孤立的粉字去暗示。 */
table.mini.ai-diff tbody td:last-child,table.mini.ai-diff thead th:last-child{
  background:color-mix(in srgb,var(--accent) 7%,transparent);padding-left:22px;}
table.mini.ai-diff thead th:last-child{color:var(--accent);}
/* ── P14 五类指标卡：与 P8 的五趋势卡同为 .g5，靠**大号序号**区分语域 ───────────
   （P8 走 .tag 小标；本页走 .n 大数字 + 指标逐条列。两页并排看不会读成同一张。）*/
.kpi .n{font-size:34px;}
.kpi .t{font-size:25px;}
.kpi .m{font:400 18px/1.95 var(--f-cn);color:var(--ink-2);}
/* ── P13 试点建议行：四枚等宽 mono 项，压在收口线之上的页脚带 ─────────────── */
.adv{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;height:100%;}
.adv > div{border-left:2px solid color-mix(in srgb,var(--accent) 46%,transparent);
  padding-left:16px;display:flex;flex-direction:column;justify-content:center;gap:7px;}
.adv .h{font:500 13px/1 var(--f-mono);letter-spacing:.16em;color:var(--ink-3);}
.adv .b{font:400 19px/1.4 var(--f-cn);color:var(--ink-2);}
.adv .b b{font-weight:700;color:var(--ink);}
/* 编辑热区（deck.js 依赖） */
.edit-hotzone{position:fixed;top:0;left:0;width:120px;height:80px;z-index:10000;}
.edit-toggle{position:fixed;top:18px;left:18px;z-index:10001;opacity:0;pointer-events:none;
  font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);
  border:1px solid var(--hair);border-radius:3px;padding:7px 12px;background:transparent;cursor:pointer;
  transition:opacity .3s;}
.edit-toggle.show,.edit-toggle.active{opacity:1;pointer-events:auto;}
.edit-toggle.active{border-color:var(--accent);color:var(--accent);}
@media print{.edit-toggle,.edit-hotzone,.deck-progress,.deck-steps,.deck-swap{display:none!important;}}
</style>"""

# ── 组装件（与母版同签名）────────────────────────────────────────────────────
def sh(cls, style, body, sid=None):
    """本 deck **零分步** ⇒ 这只 helper 刻意不带 step 形参：
       挂不上 data-step，就不会有人在常显容器上误挂一枚（motion.css 的兜底规则
       会把它摁成透明整页 —— 引擎 deck 已经踩过一次）。"""
    a = ' data-sid="%s"' % sid if sid else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (cls, a, style, body)

def rule(y, x=120, w=1680, i=1):
    """分区之间的 1px 细线（高度 1px → 扫描器不当它是覆盖块）"""
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:%dpx;height:1px;--i:%d" % (x, y, w, i), "")

def vrule(x, y, h, i=1):
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:1px;height:%dpx;--i:%d" % (x, y, h, i), "")

def lab(x, y, t, w=680, col=None, i=0):
    """mono 小节标：「01 · MARKET STACK」"""
    c = ";color:%s" % col if col else ""
    return sh("flow seclab", "left:%dpx;top:%dpx;width:%dpx;height:20px;--i:%d%s" % (x, y, w, i, c), t)

def figbox(x, y, w, vbw, vbh, inner, cls="flow", i=0):
    """SVG 装盒：.sh 高度按 viewBox 等比算死，svg 一律 width:100%;height:auto"""
    h = round(w * vbh / vbw)
    return sh(cls, "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (x, y, w, h, i),
              '<div class="fig"><svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg></div>'
              % (vbw, vbh, inner))

def head(kicker, title, kw=1680):
    """每页统一的页眉：kicker y92 / 标题 y148 起（家族版式纪律）"""
    return (sh("flow kk", "left:120px;top:92px;width:%dpx;height:28px" % kw, kicker)
            + sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", title))

def land(t, y=988, x=120, w=1680, i=6):
    return sh("flow", "left:%dpx;top:%dpx;width:%dpx;height:70px;--i:%d" % (x, y, w, i),
              '<div class="land">%s</div>' % t)

def rail(t, y=988):
    return sh("flow mono-sm", "left:120px;top:%dpx;width:1680px;height:24px;--i:7" % y, t)

def src(t, y=1015, x=120, w=1680, i=7, align=None):
    """SOURCE ledger 行（与 convoai-engine / convoai-info 的 src() 同签名同类名）。
       全家族统一四段：SOURCE · <来源> · <样本或时间窗> · 事实截止 2026.08
       **来源写机构名，不写 URL** —— 投屏上没人读得出 URL，且会诱发点击。
       缺哪段就少哪段（不编），缺口记在交付报告里等 Colin 补。"""
    a = ";text-align:%s" % align if align else ""
    return sh("flow src", "left:%dpx;top:%dpx;width:%dpx;height:24px;--i:%d%s" % (x, y, w, i, a), t)

# ── SOURCE ledger 常量（同一份出处出现在多页时只写一次，防两页各自漂移）────────
_SRC_NFRA = ("SOURCE · 国家金融监督管理总局《2026 年一季度银行业保险业主要监管指标数据情况》 · "
             "2026 年一季度末 · 事实截止 2026.08")
_SRC_CARD = ("SOURCE · 新华网转述中国人民银行数据 / 中国人民银行清算总中心《支付体系运行总体情况》 · "
             "2026 年一季度末 / 2025 年末 · 事实截止 2026.08")
_SRC_REG = ("SOURCE · 《消费金融公司管理办法》（湖南省人民政府转载） / 全国标准信息公共服务平台 · "
            "2024.03 发布 / GB&#47;T 45251-2025 于 2025.02.28 发布实施 · 事实截止 2026.08")
_SRC_MKT = ("SOURCE · Fortune Business Insights / Grand View Research · "
            "Debt Collection Software 2025&#8594;2034 / 2023&#8594;2030 · 事实截止 2026.08")
# Agora 侧：与引擎 deck P5（_SRC_TYP）/ P21 逐字同源的「引擎公开口径 · 典型值」
_SRC_AGORA = ("SOURCE · 声网官网 / 引擎发版说明 / IR 公开口径 · 典型值 · 事实截止 2026.08")

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
#     `.dw{stroke-dasharray:var(--len)}` 会把 dasharray 属性整条压掉 —— 虚线会渲染成实线，
#     而图例里那一栏还写着「虚线」，于是图例开始说谎（P8 质量语言第 ① 条当场破功）。
#     第一版的两条「参考基线 / 起步基线」正是这么变成实线的。要虚线一律走 dline()。
def hline(x1, x2, y, col="var(--hair-strong)", w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d H%d" '
            'stroke="%s" stroke-width="%s" fill="none"/>' % (abs(x2 - x1), i, x1, y, x2, col, w))

def vline(x, y1, y2, col="var(--hair-strong)", w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d V%d" '
            'stroke="%s" stroke-width="%s" fill="none"/>' % (abs(y2 - y1), i, x, y1, y2, col, w))

def dline(d, col="var(--hair-strong)", w=2, i=1, dash="7 7", cls="", sty=""):
    """虚线：不能走 .dw —— motion.css 的 .dw{stroke-dasharray:var(--len)} 会把 dasharray
       属性整条压掉，虚线会渲染成实线。这里改挂 .pop（只动 opacity/transform）。"""
    return ('<path class="pop%s" style="--i:%d%s" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-dasharray="%s"/>'
            % ((" " + cls) if cls else "", i, (";" + sty) if sty else "", d, col, w, dash))

def pline(d, col="var(--hair-strong)", w=2, i=1, ln=None):
    """实线任意路径（.dw 走一遍描线入场）。ln 传路径长度（近似即可）。"""
    return ('<path class="dw" style="--len:%d;--i:%d" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none"/>' % (int(ln or 1200), i, d, col, w))

# ── 运动原语 ① 能量包（deck 级）────────────────────────────────────────────
#   压在实线之下的一段粗软 stroke，沿路径漂移。dasharray =「包长 seg + 间隔 ln」，
#   --mo-off 走完一个整周期 ⇒ 100% 帧与 0% 帧逐像素相同（静态原图纪律）。
def packet(d, ln, col=None, w=11, seg=24, dur="1.8s", op=".3", i=2, rev=False, delay=None,
           cls="", cap="round"):
    per = seg + int(ln)
    v = "--mo-off:%d;--mo-dur:%s" % (per if rev else -per, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<path class="pop mo-packet%s" style="--i:%d;%s" d="%s" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-opacity="%s" stroke-linecap="%s" stroke-dasharray="%d %d"/>'
            % ((" " + cls) if cls else "", i, v, d, col or AC, w, op, cap, seg, int(ln)))

def box(x, y, w, h, r=4, hot=False, dashed=False, i=0, cls="", sty=""):
    """家族图框：常态 class="box"（fill card-bg / stroke hair），高亮走 accent 描边。"""
    d = ' stroke-dasharray="7 6"' if dashed else ""
    c = (" " + cls) if cls else ""
    v = (";" + sty) if sty else ""
    if hot:
        return ('<rect class="pop%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
                'fill="none" stroke="var(--accent)" stroke-width="2.5"%s/>' % (c, i, v, x, y, w, h, r, d))
    return ('<rect class="pop box%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'stroke-width="1.4"%s/>' % (c, i, v, x, y, w, h, r, d))

def pulse_dot(x, y, r=7, col=None, lo=".2", hi=None, dur="2.4s", delay=None, i=3):
    """运动原语 ③ 的标准件：钉在流程节点 / 接头上的小圆片，错峰明暗 ——
       读作「这一环刚被点着」。整个 deck 的「一道亮波顺着链路跑」都由它排出来。
       ⚠ 载体自带 opacity 时**必须**把 hi 设成那个静态值（moPulse 的 0%/100% 帧
         写的是 var(--mo-hi,1)）：不设的话动画会把它顶成 1，
         SELFPIN 的「100% 帧 = 静态原图」当场对不上（那是硬红线）。"""
    v = "--i:%d;--mo-lo:%s;--mo-dur:%s" % (i, lo, dur)
    if hi:   v += ";--mo-hi:%s" % hi
    if delay: v += ";--mo-del:%s" % delay
    return ('<circle class="pop mo-pulse" style="%s;fill:%s%s" cx="%d" cy="%d" r="%d"/>'
            % (v, col or AC, (";opacity:%s" % hi) if hi else "", x, y, r))

def halo_rect(x, y, w, h, r=8, col=None, sc="1.06", op=".34", dur="3.6s", delay=None):
    """呼吸光晕（原语 ④ 的伴件 · 矩形版）：100% 帧 opacity:0 ⇒ 静态语域零痕迹。"""
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
    # mono：.lbl 是唯一自带 mono 的类，但它带 text-transform:uppercase（会把「AI 语音」
    # 烧成大写）。要 mono 又要保留大小写时走这一路。
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

# ── deck 级线型系统（引擎 P8 为标杆，本 deck 逐字沿用）─────────────────────────
#   实线 accent        = 业务主流程 / 主数据流
#   虚线 hair-strong   = 事件 / 控制（合规规则、人工接管）
#   点线 accent-deep   = 反馈 / 回流（指标回流、策略迭代）
#   每张图底部一行 mono 迷你图例，只列该页真正用到的线型（画真线样，不用字符画）。
def lg_solid(x, y, col=AC, w=2.5, i=9):
    return hline(x, x + 40, y, col, w, i)
def lg_dash(x, y, col=HS, w=2, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="6 5")
def lg_dot(x, y, col=AD, w=2.4, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="2 6")
def lg_fast(x, y, col=AD, w=5, i=9):
    return hline(x, x + 40, y, col, w, i)
_LGK = {"solid": lg_solid, "dash": lg_dash, "dot": lg_dot, "fast": lg_fast}

def legend(x, y, items, i=9, gap=54):
    """图例行：items = [(kind, 标签)] / [(kind, 标签, 线宽)] / [(kind, 标签, 线宽, 颜色)]。
       kind ∈ solid / dash / dot / fast / fill。图例样线必须与页内真线同粗同色，
       否则「粗一档」「灰一档」在图例里读不出来。步进按标签字数估宽（CJK 13.2px/字）。"""
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
        cx += 50 + int(len(label) * 13.2) + gap
    return "".join(o)

def domain_band(x, y, w, h, label, i=1, r=14):
    """域分带（P8 质量语言第 ⑥ 条）：一块极淡的 accent 底 + 一枚 mono 域名。
       底色走 accent 6%（浅底）/ 见 conf-theme-dual 的 --accent —— color-mix 让它
       在两个主题下都只是「一层雾」，不与 .box 的 card-bg 抢层次。"""
    return ('<rect class="pop" style="--i:%d;fill:color-mix(in srgb,var(--accent) 6%%,transparent);'
            'stroke:color-mix(in srgb,var(--accent) 22%%,transparent);stroke-width:1.2" '
            'x="%d" y="%d" width="%d" height="%d" rx="%d"/>' % (i, x, y, w, h, r)
            + txt(x + 18, y + 26, label, "sm", size=14, col=I3, mono=True, ls=".16em", i=i))


# ═══ P1 · 封面（title 板）══════════════════════════════════════════════════
#   大纲 P1 逐字：主标「AI 驱动的智能贷后催收解决方案」/
#   副标「从人工密集型催收到合规、可追踪、可规模化的智能运营」。
#   视觉纪律（大纲原话）：金融科技风格，**避免任何负面视觉表达** ——
#   所以封面上没有一支箭头、没有一条下行曲线、没有任何「压」「催」的图形隐喻，
#   只有家族标准的 accent 短棒 + 关键词 chip 行。
#   版式账：主标 15 个全角字 × 84px，letter-spacing −.02em ⇒ 墨迹 ≈ 1235px，
#   盒宽 1560 余 325px，单行不折。行盒 84×1.16 = 97.4 > CJK 回退字体内容高
#   （≈84×1.115 = 93.7）⇒ 不会被 .ink 的液态扫过 mask 裁掉一线。
page("title", "".join([
    sh("flow kk", "left:120px;top:206px;width:1500px;height:28px",
       "AGORA · POST-LOAN COLLECTIONS · 贷后催收解决方案"),
    sh("ink", "left:120px;top:286px;width:1560px;height:112px;"
       "font:700 84px/1.16 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "AI 驱动的<strong style='color:var(--accent)'>智能贷后催收</strong>解决方案"),
    sh("spread", "left:120px;top:452px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow sub", "left:120px;top:506px;width:1400px;height:96px;--i:4",
       "从人工密集型催收到合规、可追踪、可规模化的智能运营。"),
    # 关键词 chip 行（大纲 P1「关键词」逐字）
    sh("flow", "left:120px;top:646px;width:1560px;height:60px;--i:5",
       "".join('<span class="chip%s">%s</span>' % (" on" if _k == 4 else "", _t)
               for _k, _t in enumerate(
                   ["AI 语音 Agent", "贷后催收", "逾期资产管理", "实时互动", "Agora"]))),
    sh("flow mono-sm", "left:120px;top:930px;width:1400px;height:24px;--i:6",
       "面向金融机构贷后 / 风控 / 合规 / 技术负责人 · 方案交流参考 · 事实截止 2026.08"),
]))

# ═══ P2 · 总览 ·「从人力驱动转向智能运营驱动」═══════════════════════════════
#   大纲 P2 的五点是一条**逻辑链**（「行业压力长期存在 → 传统模式遇到瓶颈 → 监管和
#   客户体验要求提高 → AI 成为必然方向 → Agora 提供实时语音 AI 底座」，见大纲第 1 节
#   「推荐叙事主线」），所以不排成五张并列卡，而是排成一条 flow 带 ——
#   并列卡会把「因为所以」读成「还有还有」，整份 deck 的骨架就在第二页塌了。
#   P8 质量语言：① 一种线型 + 图例 ② hot = 第五节（Agora，全链的落点）
#   ③ 四条边各带「流的什么」 ⑤ 无数字（本页不引数，数字从 P3 起）。
#   标题与正文都是**手写断行**（每格一个列表），不做 [:n] 机器分块 ——
#   CJK 允许任意两字之间断行，机器分块会把「意图」「难以」这类词劈成两行，
#   在 296 的窄盒里一眼就是错字。盒内可用宽 = 296 − 52 内边距 = 244px：
#   标题 26px ⇒ 每行 ≤ 9 字；正文 18px ⇒ 每行 ≤ 13 字。**改盒宽必须重数这两笔。**
_CHAIN = [
    ("01", ["行业底层需求", "长期存在"],
     ["信贷规模庞大，逾期资产管理", "是金融机构的长期能力"]),
    ("02", ["传统模式遇到边界"],
     ["人工坐席、外包与规则外呼，", "难以同时满足规模、人效", "和合规三件事"]),
    ("03", ["监管环境变化"],
     ["催收行为、数据使用、", "消费者权益保护要求更高"]),
    ("04", ["AI 技术成熟"],
     ["大模型、ASR、TTS、", "意图识别与实时语音交互，", "让智能催收进入可落地阶段"]),
    ("05", ["Agora 价值"],
     ["提供实时语音 AI 基础设施，", "帮助智能催收", "从实验走向生产"]),
]
# 边上的「流的什么」——四条边各一句，说清上一节交给下一节的是什么
_CHAIN_EDGE = ["规模持续", "瓶颈显性化", "要求抬升", "能力就位"]
# 02 · 本篇路线：把五节一链落到具体页号（引擎 deck P5「章内指针」同款做法）——
#   15 页的方案汇报 deck，客户第二页就该知道后面会讲到哪儿、在第几页。
#   这不是新内容，只是把本 deck 自己的结构说出来。
_ROADMAP = [
    ("行业现状", "P3&#8211;4"), ("运营链路", "P5"), ("核心困难", "P6&#8211;7"),
    ("行业趋势", "P8"), ("市场容量", "P9"), ("AI 与架构", "P10&#8211;11"),
    ("Agora 与落地", "P12&#8211;14"),
]
def _chain_fig():
    o, W, G = [], 296, 50
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
        if k < 4:
            o.append(pulse_dot(x + W, 190, 6, AC, lo=".18", dur="2.8s",
                               delay="%.2fs" % (k * .35), i=k + 2))
    o.append(legend(0, 384, [("solid", "叙事主线 · 因果链")]))
    return "".join(o)
page("content", "".join([
    head("OVERVIEW · 一页讲清全篇逻辑",
         "催收行业，正在从「人力驱动」转向<strong>智能运营驱动</strong>。"),
    lab(120, 244, "01 · NARRATIVE CHAIN · 五节一链"),
    figbox(120, 276, 1680, 1680, 410, _chain_fig(), i=1),
    lab(120, 712, "02 · ROADMAP · 本篇路线", i=6),
    sh("flow", "left:120px;top:748px;width:1680px;height:82px;--i:7",
       '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:18px;height:100%">'
       + "".join(
           # 页号那一格挂 data-nogate="pageref"：它是**本 deck 自己的页码**，不是内容里的数字。
           # 不豁免的话，qa 的「新造数字闸」白名单就得把 10–15 全收进去 —— 收进去之后
           # 任何一个新写的小数字都能蒙混过关，闸门当场钝化（上一轮的短板，本轮修掉）。
           '<div style="border-top:1px solid var(--hair);padding-top:14px;display:flex;'
           'flex-direction:column;gap:8px">'
           '<div data-nogate="pageref" style="font:500 13px/1 var(--f-mono);'
           'letter-spacing:.14em;color:var(--accent)">%s</div>'
           '<div style="font:400 19px/1.3 var(--f-cn);color:var(--ink-2)">%s</div></div>'
           % (_p, _t) for _t, _p in _ROADMAP) + '</div>'),
    rule(850),
    land("后面每一章都在回答同一个问题：<strong style='color:var(--accent)'>为什么需要 AI，"
         "为什么是 Agora</strong>。"),
]))

# ═══ P3 · 行业现状 ·「逾期资产管理已成为金融机构长期能力」═══════════════════
#   大纲 P3「可验证事实」逐字：不良贷款余额 3.7 万亿元 / 不良贷款率 1.51% /
#   正常贷款余额 239.2 万亿元，均为 2026 年一季度末（国家金融监督管理总局）。
#   P8 质量语言：⑤ **三个数各带时序标**（2026Q1 末）—— 金融机构的听众第一反应
#   永远是「哪一天的数」，时序标不在图上就得从嘴里补，那就是一次口径事故。
#   ④ 闭环优先：右图不是「放款 → 贷后运营 → 资产质量」三段直线，而是加一条
#   「资产质量 → 风险定价 → 放款」的点线回流 —— 有这条弧，贷后才是**经营能力**
#   而不是末端作业，这正是本页标题那句话的图形依据。
_NPL = [
    ("不良贷款余额", "3.7", "万亿元", "商业银行", True),
    ("不良贷款率",   "1.51", "%",     "商业银行", False),
    ("正常贷款余额", "239.2", "万亿元", "商业银行", False),
]
def _asset_fig():
    o = []
    # ── 三段主链（实线 accent），每段之间带「流的什么」──
    _N = [("放款", "新增信贷投放"), ("贷后运营", "分层 · 触达 · 协商 · 履约"),
          ("资产质量", "不良率 · 拨备 · 利润")]
    for k, (t, s) in enumerate(_N):
        x = 130 + k * 470
        hot = (k == 1)
        if hot:
            o.append(halo_rect(x, 34, 340, 108, 10, sc="1.06", op=".32", dur="3.6s"))
        o.append(box(x, 34, 340, 108, 10, hot=hot, i=k + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.6s" if hot else ""))
        o.append(txt(x + 170, 80, t, "ttl", size=27, anchor="middle", col=AC if hot else None))
        o.append(txt(x + 170, 114, s, "sm", size=16, anchor="middle"))
        if k < 2:
            x1, x2 = x + 340, x + 470
            o.append(packet("M%d 88 H%d" % (x1, x2 - 12), 118, seg=20, dur="1.7s", i=k + 1,
                            delay="%.1fs" % (k * .5)))
            o.append(hline(x1, x2 - 12, 88, AC, 2.5, k + 1))
            o.append(ah_r(x2, 88, AC, 8))
            o.append(txt(x1 + 59, 64, ["资产入账", "回收 · 迁徙"][k], "sm", size=14,
                         anchor="middle", col=I3))
            o.append(pulse_dot(x + 340, 88, 6, AC, lo=".18", dur="2.8s",
                               delay="%.2fs" % (k * .55), i=k + 2))
    # 回流弧两端的接头脉冲（点线语域 ⇒ 走 accent-deep，与弧同色）
    o.append(pulse_dot(1300, 142, 6, AD, lo=".2", dur="3.2s", delay="1.1s", i=5))
    o.append(pulse_dot(300, 152, 6, AD, lo=".2", dur="3.2s", delay="2.2s", i=5))
    # ── 闭环边：资产质量 → 风险定价 → 放款（点线 accent-deep，绕底部）──
    _ARC = "M1300 142 V196 Q1300 214 1282 214 H318 Q300 214 300 196 V152"
    o.append(packet(_ARC, 1090, seg=24, col=AD, w=9, op=".3", dur="7s", i=5, cls="mo-cycle"))
    o.append(dline(_ARC, AD, 3, 5, dash="3 8"))
    o.append(ah_u(300, 146, AD, 7))
    o.append(txt(800, 244, "资产质量回流风险定价与授信策略 —— 贷后是经营能力，不是末端作业",
                 "sm", size=17, anchor="middle", col=AD))
    o.append(legend(130, 292, [("solid", "业务主流程"), ("dot", "反馈 / 回流")]))
    return "".join(o)
page("content", "".join([
    head("MARKET BASE · 万亿级底座", "逾期资产管理，已成为金融机构的<strong>长期能力</strong>。"),
    lab(120, 250, "01 · SCALE · 三个核心数（2026 年一季度末）"),
    sh("", "left:120px;top:288px;width:1680px;height:212px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d;justify-content:center"><div class="tag%s">%s</div>'
           '<div class="stat"><span class="v%s" style="font-size:76px">%s'
           '<span style="font-size:.36em;letter-spacing:0;margin-left:6px">%s</span></span></div>'
           # 时序标：与数字同卡、mono、小一档 —— 数字离开时点就不再是事实
           '<div style="font:500 13px/1 var(--f-mono);letter-spacing:.16em;color:var(--ink-3)">'
           '%s · 2026Q1 末</div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag,
              "" if _on else " w", _v, _u, _who)
           for _i, (_tag, _v, _u, _who, _on) in enumerate(_NPL)) + '</div>'),
    lab(120, 540, "02 · WHY IT MATTERS · 贷后在资产循环里的位置", i=5),
    figbox(120, 576, 1680, 1680, 320, _asset_fig(), i=6),
    rule(850),
    land("贷后催收不是业务末端环节，而是影响资产质量、拨备压力、利润表现与客户关系的"
         "<strong style='color:var(--accent)'>核心风险经营能力</strong>。", y=944),
    src(_SRC_NFRA),
]))

# ═══ P4 · 存量经营 ·「回收效率变得更关键」══════════════════════════════════
#   大纲 P4「可验证事实」两条都用上，因为**两条合起来才是一个时序**：
#     2025 年末 6.96 亿张（人民银行清算总中心）→ 2026Q1 末 6.87 亿张（新华网转述人行）
#   这正是 P8 质量语言第 ⑤ 条「数字带时序标」的范例：单看 6.87 亿张只是一个存量，
#   两点连起来才读得出「增量红利下降、进入存量经营」这句话的证据。
#   ⚠ 两点之间**不画趋势外推**，也不标降幅百分比 —— 大纲没给，我们不造。
#   右侧四象限走大纲原话「账户多、笔数多、客群分散、回收周期短」。
# 手写断行（理由同 P2 的 _CHAIN）：盒内可用宽 = 416 − 48 = 368px，15px CJK ⇒ 每行 ≤ 22 字。
_QUAD = [
    ("账户多",     ["信用卡 · 消费贷 · 现金贷 · 分期 ·", "电商金融，覆盖人群广"]),
    ("笔数多",     ["单笔金额相对小，", "案件量以百万级计"]),
    ("客群分散",   ["地域、职业、还款能力高度离散，", "难用一套话术覆盖"]),
    ("回收周期短", ["账龄迁徙快，", "M0 / M1 的处置窗口以天计"]),
]
def _stock_fig():
    """两点时序：2025 年末 6.96 亿张 → 2026Q1 末 6.87 亿张。
       ⚠ **方向不能画反**（第一版就画反了，把 6.87 画得比 6.96 高，等于宣称卡量在涨）：
         值在**下降**，所以后一个点必须更低。y 只做定性升降，不按比例标尺 ——
         两个点之间的差是 0.09 亿张，按真比例画等于一条水平线，读不出「进入存量经营」。
         因此轴上刻意不放数值刻度、也不写降幅百分比（大纲没给，我们不造）。"""
    o = []
    o.append(txt(40, 60, "全国信用卡和借贷合一卡 · 亿张", "sm", size=17, col=I3))
    # 参考基线（虚线）：两点都挂在它上面，读作「同一把尺子上的两个时点」
    _PTS = [("2025 年末", "6.96", 150, 148, I3), ("2026Q1 末", "6.87", 470, 190, AC)]
    d = "M150 148 L470 190"
    o.append(packet(d, 323, seg=22, dur="3.4s", i=3))
    o.append(pline(d, AC, 2.5, 3, ln=323))
    # 参考基线走 .mo-drift：dash 慢爬（比包慢一档）—— 它是「同一把尺子」的注解线，
    # 不是数据流，所以不给它挂包。off −180 = dash「4 6」周期 10 的 18 个整周期。
    o.append(dline("M40 262 H580", HS, 1.4, 1, dash="4 6", cls="mo-drift",
                   sty="--mo-off:-180;--mo-dur:5s"))
    for k, (lb, v, cx, cy, col) in enumerate(_PTS):
        o.append(dline("M%d %d V262" % (cx, cy), HS, 1.2, k + 2, dash="3 6",
                       cls="mo-drift", sty="--mo-off:-180;--mo-dur:4.2s;--mo-del:-%.1fs" % (k * 1.4)))
        o.append('<circle class="pop mo-pulse" style="--i:%d;--mo-lo:.34;--mo-dur:2.6s;'
                 '--mo-del:%.1fs;fill:%s" cx="%d" cy="%d" r="10"/>'
                 % (k + 2, k * .9, col, cx, cy))
        o.append(txt(cx, cy - 26, v, "ttl", size=40, anchor="middle", col=col, weight=700))
        o.append(txt(cx, 292, lb, "sm", size=16, anchor="middle", col=I3, mono=True, ls=".1em"))
    o.append(txt(310, 232, "增量红利下降", "sm", size=16, anchor="middle", col=I3))
    o.append(legend(40, 344, [("solid", "存量 · 两个时点"), ("dash", "参考基线")]))
    return "".join(o)
def _quad_fig():
    """四象限：2×2 等分格 + 一条贯穿的域分带「高频 · 分散 · 标准化程度较高」。
       域分带是本页的论点（这类资产天然适合 AI 提升触达与运营效率），
       所以它压在四格之上、而不是躲在角落当图注。"""
    o = []
    o.append(domain_band(0, 0, 900, 372, "ASSET PROFILE · 消费金融催收特征", i=1))
    for k, (t, ds) in enumerate(_QUAD):
        cx, cy = 26 + (k % 2) * 432, 52 + (k // 2) * 154
        o.append(box(cx, cy, 416, 138, 8, i=k + 2))
        o.append(txt(cx + 24, cy + 48, t, "ttl", size=26))
        for j, seg in enumerate(ds):
            o.append(txt(cx + 24, cy + 84 + j * 24, seg, "sm", size=15))
    return "".join(o)
page("content", "".join([
    head("STOCK ERA · 存量经营", "消费信贷进入存量经营，<strong>回收效率</strong>变得更关键。"),
    lab(120, 244, "01 · TIME SERIES · 卡量两个时点"),
    figbox(120, 280, 700, 620, 372, _stock_fig(), i=1),
    lab(880, 244, "02 · PROFILE · 四象限特征", i=2),
    figbox(880, 280, 920, 900, 372, _quad_fig(), i=3),
    rule(850),
    # ⚠ land 只准一行：29px×1.5 的行盒 43.5，两行就是 87 > 盒高 70 ⇒ 压到 src 行上。
    #   （第一版正是这么把 SOURCE ledger 盖掉半行的，截图实锤。）
    land("高频、分散、标准化程度较高的资产，天然适合用 AI 提升"
         "<strong style='color:var(--accent)'>触达与运营效率</strong>。", y=944),
    src(_SRC_CARD),
]))

# ═══ P5 · 产业链 ·「催收不是一个动作，而是一条复杂运营链路」（**标杆动效页**）═══
#   大纲 P5 的八个环节逐字入图，并按大纲「建议视觉」做成**闭环**而不是横条流程：
#     账户分层 → 触达策略 → 沟通协商 → 承诺还款 → 履约跟踪 → 争议处理 →
#     合规质检 → 策略迭代 →（回流）账户分层
#   本页是这份 deck 的运动语言母本，动效即语义（cycle 原语环行）：
#     · 椭圆环走 .mo-cycle：**几何绝不旋转**，只让虚线 dash 绕圈爬 ——
#       八个节点是钉在钟面位置上的，环一转、节点与文字就甩走了，整页论证当场失效。
#       环长（Ramanujan 近似，rx=560 / ry=190）≈ 2502；dash「11 10」周期 21，
#       取 119 个整周期 = 2499 作 --mo-off ⇒ 100% 帧 = 0% 帧（静态原图纪律），
#       视觉上 2499/2502 = 99.9% 圈，等同「26s 自转一周」。
#     · 三枚 .mo-packet 沿环绕行（dasharray「26 2502」⇒ 同一时刻每枚包在环上只有一段），
#       相位错开 1/3 周期 —— 读作「同时有多个案件在链路的不同位置上」。
#     · 八枚 .mo-pulse 钉在**相邻节点的中点**（不是节点上，那儿被盒子占了），
#       delay 依次 +0.3s ⇒ 一道亮波顺时针跑，读作「一个环节交给下一个环节」。
#   P8 质量语言：② hot = 08 策略迭代（唯一一枚 .mo-breathe）—— 它是把线接成环的那一节；
#     ③ 闭环边带「回收 · 投诉 · 接通 · 履约 指标」标注（= 大纲第 8 环的原话）；
#     ① 图例两型；④ 闭环优先本身就是本页的论点。
_LINK8 = [
    ("01", "账户分层", "账龄 · 金额 · 风险 · 历史行为"),
    ("02", "触达策略", "电话 · 短信 · Push · 微信 · 邮件"),
    ("03", "沟通协商", "身份核验 · 原因识别 · 方案沟通"),
    ("04", "承诺还款", "记录承诺 · 发送链接 · 设定提醒"),
    ("05", "履约跟踪", "监控兑现 · 决定是否升级策略"),
    ("06", "争议处理", "账单 / 身份争议 · 投诉 · 减免展期"),
    ("07", "合规质检", "话术检查 · 频次控制 · 录音留痕"),
    ("08", "策略迭代", "按回收 · 投诉 · 接通 · 履约 优化"),
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
    # ① 环本体：虚线 + .mo-cycle（几何不转，只有 dash 在爬）
    o.append('<path class="pop mo-cycle" style="--i:1;--mo-off:-%d;--mo-dur:26s" d="%s" '
             'fill="none" stroke="%s" stroke-width="2.4" stroke-dasharray="11 10"/>'
             % (_R8_OFF, _R8_PATH, AC))
    # ② 三枚绕行包（相位 1/3 错开）
    for k in range(3):
        o.append(packet(_R8_PATH, _R8_LEN, seg=26, w=13, op=".26", dur="26s", i=2,
                        delay="-%.2fs" % (k * 26 / 3.0), cls="mo-cycle"))
    # ③ 八枚中点脉冲（顺时针亮波）
    for k in range(8):
        px, py = _ring_pt(-90 + 45 * k + 22.5)
        o.append('<circle class="pop mo-pulse" style="--i:%d;--mo-lo:.18;--mo-dur:2.4s;'
                 '--mo-del:%.2fs;fill:%s" cx="%d" cy="%d" r="7"/>'
                 % (3 + k % 4, k * .3, AD, round(px), round(py)))
    # ④ 八个节点盒（208×76，圆心钉在环上）
    for k, (no, t, d) in enumerate(_LINK8):
        px, py = _ring_pt(-90 + 45 * k)
        x, y = round(px) - 104, round(py) - 38
        hot = (k == 7)
        if hot:
            o.append(halo_rect(x, y, 208, 76, 9, sc="1.09", op=".34", dur="3.4s"))
        o.append(box(x, y, 208, 76, 9, hot=hot, i=(k % 4) + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.4s" if hot else ""))
        o.append(txt(x + 16, y + 27, no, "sm", size=13, col=AC, mono=True, ls=".18em"))
        o.append(txt(x + 46, y + 29, t, "ttl", size=22, col=AC if hot else None))
        o.append(txt(x + 16, y + 58, d, "sm", size=14))
    # ⑤ 闭环边的「流的什么」：08 → 01 那一段（左上弧）。
    #   钉在该段的**中点脉冲**正上方（midpoint k=7 落在 (626, 86)）——
    #   第一版写在 (510,74)，看上去像 08 盒的副标题，读不出它注解的是那条边。
    #   只写「指标回流」四个字：08 节点自己已经叫「策略迭代」，重复一遍是噪声。
    #   横向净空：08 盒右缘 548 / 01 盒左缘 736，四字 16px ≈ 64px 居中于 626 ⇒ 594–658，两侧各留 78。
    o.append(txt(626, 58, "指标回流", "sm", size=16, col=AD, anchor="middle"))
    # ⑥ 环心：本页的论点
    o.append(txt(_R8CX, _R8CY - 10, "八个环节 · 一条闭环", "ttl", size=30, anchor="middle"))
    o.append(txt(_R8CX, _R8CY + 26, "数据 · 语音 · 业务流程 · 合规控制 共同驱动的运营体系",
                 "sm", size=18, anchor="middle"))
    o.append(legend(30, 528, [("solid", "运营主链路"), ("dot", "指标回流")]))
    return "".join(o)
page("content", "".join([
    head("VALUE CHAIN · 八环闭环", "催收不是一个动作，而是一条<strong>复杂运营链路</strong>。"),
    lab(120, 244, "01 · EIGHT STAGES · 分层 → 触达 → 沟通 → 承诺 → 履约 → 争议 → 质检 → 迭代",
        w=1400),
    figbox(120, 276, 1680, 1680, 560, _ring_fig(), i=1),
    rule(850),
    land("催收系统不是「自动打电话」——它是数据、语音、业务流程与"
         "<strong style='color:var(--accent)'>合规控制</strong>共同驱动的运营体系。"),
]))

# ═══ P6 · 困难点 ·「规模、人效、合规三者难兼得」════════════════════════════
#   左：hot 三角。三个顶点两两之间是**取舍边**（拉紧一边就松掉另一边），
#     中心那枚 hot 盒才是本页的命题「三者难兼得」——它是全页唯一的 .mo-breathe。
#     三条边上跑 .mo-packet 绕三角环行 = 张力在三者之间来回倒，读作「按下葫芦浮起瓢」。
#   右：大纲 P6 的五难逐字（触达难 / 人效难 / 策略难 / 合规难 / 质检难），
#     用家族 .rows 排 —— 五条是**并列证据**，不是链路，所以这里刻意不画箭头。
_FIVE = [
    ("01", "触达难", "电话拦截、客户拒接、号码失效，有效沟通率下降；单一电话渠道效果衰减"),
    ("02", "人效难", "坐席培训周期长、优秀经验难复制；业务峰值临时扩人，成本弹性差"),
    ("03", "策略难", "不同账龄、金额、产品、风险等级需要不同话术与节奏，规则策略难实时调整"),
    ("04", "合规难", "话术、频次、外包、投诉处理都需严格管理；人工沟通依赖个人经验"),
    ("05", "质检难", "传统抽检覆盖有限，难以全量；事后质检无法实时阻止风险话术"),
]
_TRI = [("规模", "案件量以百万级计"), ("人效", "坐席产能有上限"), ("合规", "过程必须可追溯")]
_TRI_PT = [(360, 46), (110, 372), (610, 372)]
def _tri_fig():
    o = []
    # 三条取舍边（实线 accent）+ 绕行包
    for k in range(3):
        (x1, y1), (x2, y2) = _TRI_PT[k], _TRI_PT[(k + 1) % 3]
        ln = round(math.hypot(x2 - x1, y2 - y1))
        d = "M%d %d L%d %d" % (x1, y1, x2, y2)
        o.append(packet(d, ln, seg=22, w=10, op=".26", dur="3.2s", i=k + 1,
                        delay="-%.2fs" % (k * 3.2 / 3.0)))
        o.append(pline(d, AC, 2.2, k + 1, ln=ln))
    # 边上的取舍注（三条边中点外侧）
    for (mx, my, t, an) in [(215, 190, "扩规模 → 人效摊薄", "end"),
                            (505, 190, "保合规 → 产能受限", "start"),
                            (360, 404, "抢人效 → 话术失控", "middle")]:
        o.append(txt(mx, my, t, "sm", size=15, col=I3, anchor=an))
    # 三个顶点（各带一枚接头脉冲：张力依次在三个角上顶起来，1.07s 错峰 = 3.2s/3）
    for k, (t, d) in enumerate(_TRI):
        cx, cy = _TRI_PT[k]
        x, y = cx - 95, cy - 31
        o.append(pulse_dot(cx, cy, 34, AC, lo=".04", hi=".13", dur="3.2s",
                           delay="-%.2fs" % (k * 3.2 / 3.0), i=k + 2))
        o.append(box(x, y, 190, 62, 8, i=k + 2))
        o.append(txt(cx, cy - 2, t, "ttl", size=26, anchor="middle"))
        o.append(txt(cx, cy + 22, d, "sm", size=14, anchor="middle"))
    # 中心 hot：本页命题（唯一 .mo-breathe）
    o.append(halo_rect(245, 223, 230, 80, 10, sc="1.1", op=".34", dur="3.4s"))
    o.append(box(245, 223, 230, 80, 10, hot=True, i=5, cls="mo-breathe", sty="--mo-dur:3.4s"))
    o.append(txt(360, 254, "三者难兼得", "ttl", size=26, anchor="middle", col=AC))
    o.append(txt(360, 282, "增人不解决结构问题", "sm", size=15, anchor="middle", col=AC))
    o.append(legend(20, 440, [("solid", "取舍张力 · 此消彼长")]))
    return "".join(o)
page("content", "".join([
    head("CORE TENSION · 三难", "传统催收的核心矛盾：<strong>规模、人效、合规</strong>三者难兼得。"),
    lab(120, 250, "01 · TRADE-OFF · 取舍三角"),
    figbox(120, 292, 720, 720, 470, _tri_fig(), i=1),
    lab(920, 250, "02 · FIVE FRICTIONS · 五个拆解", i=2),
    sh("rise", "left:920px;top:288px;width:880px;height:480px;--i:3",
       '<div class="rows" style="height:100%">' + "".join(
           '<div class="r%s"><div class="n">%s</div><div class="k" style="width:118px">%s</div>'
           '<div class="v">%s</div></div>' % ("" , _n, _k, _v)
           for _n, _k, _v in _FIVE) + '</div>'),
    rule(850),
    land("这些问题不是靠增加人力能解决的——它们是"
         "<strong style='color:var(--accent)'>结构性</strong>的。"),
]))

# ═══ P7 · 困难点 ·「合规要求正在倒逼催收流程数字化」════════════════════════
#   大纲 P7「可验证事实」两条：《消费金融公司管理办法》与 GB/T 45251-2025。
#   「三不得」是把大纲那句长要求按**治理对象**拆成三条（手段 / 频次 / 对象），
#   一个字都不是新加的：大纲原文「不得暴力、威胁、恐吓、骚扰，不得向无关第三人催收」。
#   ⚠ 红线自查：「暴力」后面跟的是顿号，不构成子串「暴力催收」；
#     本页也刻意不写「加强催收管理」（会命中子串红线「强催」），改写「催收管理制度」。
#   底部 duo 走大纲「建议视觉」：过去 = 结果导向催收 / 现在 = 全过程合规运营。
_NOTS = [
    ("手段", "不得暴力、威胁、恐吓"),
    ("频次", "不得骚扰"),
    ("对象", "不得向无关第三人催收"),
]
page("content", "".join([
    head("COMPLIANCE · 合规倒逼", "合规要求，正在倒逼催收流程<strong>数字化</strong>。"),
    lab(120, 250, "01 · REGULATION · 制度与标准"),
    # 左：《消费金融公司管理办法》三不得 + 5 年留痕
    sh("rise card-c", "left:120px;top:288px;width:820px;height:250px;--i:2",
       '<div style="padding:28px 34px;height:100%;display:flex;flex-direction:column">'
       '<div style="font:500 13px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-3)">'
       'MEASURE · 部门规章</div>'
       '<div style="margin-top:12px;font:700 27px/1.3 var(--f-cn);color:var(--ink)">'
       '《消费金融公司管理办法》</div>'
       '<div style="margin-top:16px;display:flex;gap:14px">' + "".join(
           '<div style="flex:1;border-left:2px solid color-mix(in srgb,var(--accent) 46%%,transparent);'
           'padding-left:12px">'
           '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3)">%s</div>'
           '<div style="margin-top:8px;font:700 19px/1.35 var(--f-cn);color:var(--accent)">%s</div></div>'
           % (_h, _b) for _h, _b in _NOTS) + '</div>'
       '<div style="margin-top:auto;font:400 19px/1.5 var(--f-cn);color:var(--ink-2)">'
       '要求建立逾期贷款催收管理制度；催收过程记录须<b style="color:inherit;font-weight:700">'
       '真实、客观、完整、可追溯</b>，相关数据<b style="color:inherit;font-weight:700">至少保存 5 年</b>。'
       '</div></div>'),
    # 右：GB/T 45251-2025
    sh("rise card-c on", "left:980px;top:288px;width:820px;height:250px;--i:3",
       '<div style="padding:28px 34px;height:100%;display:flex;flex-direction:column">'
       '<div style="font:500 13px/1 var(--f-mono);letter-spacing:.18em;color:var(--accent)">'
       'STANDARD · 国家标准</div>'
       '<div style="margin-top:12px;font:700 27px/1.3 var(--f-cn);color:var(--ink)">'
       'GB&#47;T 45251-2025</div>'
       '<div style="margin-top:10px;font:400 22px/1.45 var(--f-cn);color:var(--ink-2)">'
       '《互联网金融 个人网络消费信贷 贷后催收风控指引》</div>'
       '<div style="margin-top:auto;display:flex;align-items:baseline;gap:16px">'
       '<div style="font:900 44px/1 var(--f-en);letter-spacing:-.03em;color:var(--accent)">2025.02.28</div>'
       '<div style="font:400 20px/1.4 var(--f-cn);color:var(--ink-2)">发布并实施</div></div>'
       '<div style="margin-top:12px;font:500 13px/1 var(--f-mono);letter-spacing:.14em;'
       'color:var(--ink-3)">催收行为有了可对表的国家标准</div></div>'),
    lab(120, 578, "02 · SHIFT · 从「结果导向」到「全过程合规」", i=4),
    sh("rise", "left:120px;top:616px;width:1680px;height:212px;--i:5",
       '<div class="duo" style="height:100%">'
       '<div><div class="h">过去 · 结果导向</div>'
       '<div class="b">看回收结果，过程留痕不全</div>'
       '<div class="s">话术依赖个人经验，表达不一致；抽检为主，事后才发现风险；'
       '第三方外包过程难以还原。</div></div>'
       '<div><div class="h">现在 · 全过程合规运营</div>'
       '<div class="b">可管理、可追溯、可解释</div>'
       '<div class="s">制度、流程、授权、外包、频次与话术标准化；录音、记录、摘要、承诺与'
       '投诉处理完整留痕；每一次触达都答得出「为什么联系、用了什么策略、是否合规」。</div></div>'
       '</div>'),
    rule(850),
    land("合规催收不是「少催收」，而是用更可控的方式"
         "<strong style='color:var(--accent)'>提高回收效率</strong>。", y=944),
    src(_SRC_REG),
]))

# ═══ P8 · 趋势 ·「催收行业的五个趋势」═════════════════════════════════════
#   大纲 P8 的五条逐字（合规化 / 标准化 / 智能化 / 协商化 / 内控化）。
#   本页是**结论页**不是机理页：五条并列，故只用 .g5 卡，不上 SVG、不入运动件名册。
#   页脚一句 land 把五条收回主线：AI 不是孤立技术应用，是行业演进的自然结果。
_TRENDS = [
    ("01", "合规化", "从「结果优先」转向「过程与结果并重」，机构需要证明催收动作符合监管、"
                     "内部政策与客户权益保护要求。"),
    ("02", "标准化", "流程、话术、频次、记录、质检逐步标准化，减少人为差异与外包不可控风险。"),
    ("03", "智能化", "AI 用于客户分层、触达时机选择、语音外呼、意图识别、实时质检、"
                     "对话摘要与策略优化。"),
    ("04", "协商化", "从单纯催缴转向还款能力识别、分期方案沟通、争议处理与客户关系修复。"),
    ("05", "内控化", "债权方对第三方催收机构的管理责任更重，需要系统实现策略下发、"
                     "过程监控、质检与审计。"),
]
page("content", "".join([
    head("TRENDS · 五个趋势", "催收行业的<strong>五个趋势</strong>。"),
    lab(120, 250, "01 · FIVE TRENDS · 合规化 · 标准化 · 智能化 · 协商化 · 内控化", w=1200),
    sh("", "left:120px;top:292px;width:1680px;height:520px",
       '<div class="g5" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d"><div class="tag%s">%s</div>'
           '<div class="t">%s</div><div class="d">%s</div></div>'
           % (" on" if _i == 2 else "", 2 + _i, " am" if _i == 2 else "", _n, _t, _d)
           for _i, (_n, _t, _d) in enumerate(_TRENDS)) + '</div>'),
    rule(850),
    land("AI 催收不是孤立的技术应用，而是行业演进方向的"
         "<strong style='color:var(--accent)'>自然结果</strong>。"),
]))

# ═══ P9 · 市场容量 ·「三层空间」════════════════════════════════════════════
#   大纲 P9 的核心是一条**方法论纪律**（也是它的「页面目的」原话）：
#     「避免将不良贷款余额直接等同于市场规模」。
#   所以本页的图形不是柱状对比，而是一个**收窄的三层带**（P8 质量语言第 ⑥ 条域分带）：
#     第一层 风险资产池（最宽）→ 第二层 催收运营支出 → 第三层 AI 技术服务空间（最窄）。
#   每一层之间的下行边带「流的什么」——「愿意为之付费的部分」「可被技术替代 / 增强的部分」，
#   宽度收窄本身就是「不能把上一层当成下一层」的图形证据。
#   右侧第三方交叉参考只放**两家机构的原始区间**，不做平均、不做换算、不外推到中国市场。
#   ⚠ 描述行是**手写断行**（每层一个列表），不做 [:n] 截断 ——
#     第一版用 d[:34] 硬截，把第二层的「管理成本」砍成「管理成」、第三层的「RAG 知识库、
#     录音转写、坐席辅助」整段砍掉。带宽是收窄的（1160 / 870 / 580），
#     所以每层能放的字数本来就不一样，只能一层一层数着写。
_LAYERS = [
    ("第一层", "风险资产池",
     ["银行不良贷款、信用卡逾期、消费贷逾期、网络小贷逾期、分期资产逾期"],
     "反映「需要被管理的资产规模」", 0, 1160),
    ("第二层", "催收运营支出",
     ["人工坐席、外包佣金、呼叫通信、号码资源、催收系统、质检、合规与管理成本"],
     "反映「每年愿意为回收和管理付出的成本」", 145, 870),
    ("第三层", "AI 技术服务空间",
     ["AI 语音 Agent、智能外呼、对话分析、实时质检、策略引擎、",
      "RAG 知识库、录音转写、坐席辅助"],
     "反映「可被 AI 和软件替代、增强或重构的技术服务收入」", 290, 580),
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
        o.append(txt(x + 82, y + 36, t, "ttl", size=25, col=AC if hot else None))
        for j, seg in enumerate(ds):
            o.append(txt(x + 22, y + 66 + j * 22, seg, "sm", size=15))
        o.append(txt(x + 22, y + 104, note, "sm", size=14, col=I3))
        if k < 2:
            nx, nw = _LAYERS[k + 1][4], _LAYERS[k + 1][5]
            cx = nx + nw // 2
            o.append(packet("M%d %d V%d" % (cx, y + 116, y + 134), 18, seg=12, dur="1.4s",
                            i=k + 2, delay="%.1fs" % (k * .6)))
            o.append(vline(cx, y + 116, y + 134, AC, 2.5, k + 2))
            o.append(ah_d(cx, y + 146, AC, 8))
            o.append(txt(cx + 26, y + 136, ["愿意为之付费的部分", "可被技术替代 / 增强的部分"][k],
                         "sm", size=15, col=I3))
            # 收窄肩点：下一层左右两个肩各一枚脉冲 —— 亮的是**被切掉的那两截**，
            # 「不能把上一层当成下一层」这句话的图形证据就在这两个点上。
            for j, sx in enumerate((nx, nx + nw)):
                o.append(pulse_dot(sx, y + 126, 6, AD, lo=".16", dur="3s",
                                   delay="%.2fs" % (k * .7 + j * .35), i=k + 3))
    o.append(legend(0, 452, [("solid", "口径收窄 · 不可直接等同")]))
    return "".join(o)
page("content", "".join([
    # ⚠ 主标不能把三层的名字也塞进来：「市场容量应看三层空间：债权规模、运营支出、软件服务。」
    #   在 68px 下墨迹 ≈ 1700px > 盒宽 1680，第一版被 .hh 的行盒切成两行、第二行又被
    #   .ink 的扫过 mask 裁掉半行（截图实锤）。三层的名字下沉到 seclab 里，那儿有的是地方。
    head("MARKET SIZING · 三层空间", "市场容量应看<strong>三层空间</strong>，不是一个数字。"),
    lab(120, 236, "01 · MARKET STACK · 逐层收窄 · 债权规模 &#8594; 运营支出 &#8594; 软件服务",
        w=1200),
    figbox(120, 268, 1160, 1160, 476, _stack_fig(), i=1),
    # 右：第三方交叉参考（两家机构的原始区间，不平均、不换算、不外推）
    sh("rise card-c", "left:1320px;top:268px;width:480px;height:476px;--i:4",
       '<div style="padding:26px 28px;height:100%;display:flex;flex-direction:column">'
       '<div style="font:500 13px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-3)">'
       'CROSS-CHECK · 第三方交叉参考</div>'
       '<div style="margin-top:10px;font:400 16px/1.5 var(--f-cn);color:var(--ink-3)">'
       '全球 debt collection software 市场规模（两家机构口径并列，不做平均）</div>'
       '<div style="margin-top:20px;padding-top:18px;border-top:1px solid var(--hair)">'
       '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3)">'
       'FORTUNE BUSINESS INSIGHTS</div>'
       '<div style="margin-top:10px;display:flex;align-items:baseline;gap:10px">'
       '<span style="font:900 42px/1 var(--f-en);letter-spacing:-.03em;color:var(--accent)">59.8</span>'
       '<span style="font:400 17px/1 var(--f-cn);color:var(--ink-3)">亿美元 · 2025</span>'
       '<span style="font:500 20px/1 var(--f-mono);color:var(--ink-3)">&#8594;</span>'
       '<span style="font:900 42px/1 var(--f-en);letter-spacing:-.03em;color:var(--accent)">137.7</span>'
       '<span style="font:400 17px/1 var(--f-cn);color:var(--ink-3)">亿美元 · 2034</span></div>'
       '<div style="margin-top:8px;font:500 15px/1 var(--f-mono);letter-spacing:.1em;'
       'color:var(--ink-2)">CAGR 9.72%</div></div>'
       '<div style="margin-top:22px;padding-top:18px;border-top:1px solid var(--hair)">'
       '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3)">'
       'GRAND VIEW RESEARCH</div>'
       '<div style="margin-top:10px;display:flex;align-items:baseline;gap:10px">'
       '<span style="font:900 38px/1 var(--f-en);letter-spacing:-.03em;color:var(--ink)">49</span>'
       '<span style="font:400 17px/1 var(--f-cn);color:var(--ink-3)">亿美元 · 2023</span>'
       '<span style="font:500 20px/1 var(--f-mono);color:var(--ink-3)">&#8594;</span>'
       '<span style="font:900 38px/1 var(--f-en);letter-spacing:-.03em;color:var(--ink)">93</span>'
       '<span style="font:400 17px/1 var(--f-cn);color:var(--ink-3)">亿美元 · 2030</span></div></div>'
       '<div style="margin-top:auto;font:400 15px/1.5 var(--f-cn);color:var(--ink-3)">'
       '两家口径的时间窗与统计范围不同，此处并列呈现，不做平均、不换算到中国市场。</div></div>'),
    lab(120, 768, "02 · FORMULA · 两条推荐测算路径", i=5),
    sh("flow", "left:120px;top:794px;width:1680px;height:48px;--i:6",
       '<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;height:100%">' + "".join(
           '<div style="border-left:2px solid color-mix(in srgb,var(--accent) 46%%,transparent);'
           'padding-left:16px;display:flex;flex-direction:column;justify-content:center;gap:6px">'
           '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.16em;color:var(--ink-3)">%s</div>'
           '<div style="font:500 17px/1.35 var(--f-mono);letter-spacing:.02em;color:var(--ink-2)">%s</div>'
           '</div>' % (_h, _b) for _h, _b in [
               ("路径 A · 自资产侧",
                "可服务逾期资产规模 <b style=\"color:var(--accent)\">×</b> 年度处置 / 催收周转率 "
                "<b style=\"color:var(--accent)\">×</b> 技术服务渗透率 "
                "<b style=\"color:var(--accent)\">×</b> 技术服务收费率"),
               ("路径 B · 自支出侧",
                "催收运营总支出 <b style=\"color:var(--accent)\">×</b> 可技术化替代 / 增强比例 "
                "<b style=\"color:var(--accent)\">×</b> AI 服务渗透率"),
           ]) + '</div>'),
    rule(850),
    land("不要把不良贷款余额直接写成催收市场规模——"
         "<strong style='color:var(--accent)'>三层之间是收窄关系，不是等号</strong>。", y=944),
    src(_SRC_MKT),
]))

# ═══ P10 · AI 势在必行 ·「不是可选项，而是必需品」══════════════════════════
#   大纲 P10 的六项价值 + 七行对比表逐字。表是本页的重心（销售汇报现场客户会照着念），
#   所以六项价值压成 .g3 两行小卡，把纵向空间让给表。
#   ⚠ 版式账：.ai-diff 把 td padding 收到 7px、字号 17、行高 1.3 ⇒
#     1 表头(≈32) + 7 行×(17×1.3+14 ≈ 36) = 284，落进 y546–830 的 284px 盒里，
#     刚好压在 rule(850) 之上。**加一行必须重算这一笔。**
_AIV = [
    ("规模化触达", "AI 承担大量重复性提醒、确认、跟进任务"),
    ("标准化话术", "降低坐席个人表达差异，减少违规话术风险"),
    ("实时理解",   "识别客户意图、情绪、还款能力、争议原因与投诉风险"),
    ("自动记录",   "生成通话摘要、承诺还款信息、客户标签与下一步动作"),
    ("全量质检",   "对每通对话进行合规检测与质量分析"),
    ("人机协同",   "AI 处理高重复低风险场景，人工处理高复杂高敏感场景"),
]
_DIFF7 = [
    ("产能",     "依赖坐席数量",   "可弹性扩展"),
    ("成本",     "边际成本较高",   "高重复任务边际成本下降"),
    ("话术",     "依赖个人经验",   "标准化、可控"),
    ("质检",     "抽检为主",       "全量质检"),
    ("合规",     "事后发现风险",   "实时提示与拦截"),
    ("数据沉淀", "记录不完整",     "自动结构化沉淀"),
    ("客户体验", "波动大",         "更一致、可协商"),
]
page("content", "".join([
    head("WHY AI · 势在必行", "AI 不是可选项，而是<strong>规模化合规催收</strong>的必需品。"),
    lab(120, 244, "01 · SIX VALUES · AI 能解决的核心问题"),
    sh("", "left:120px;top:276px;width:1680px;height:210px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card sm rise" style="--i:%d;justify-content:center">'
           '<div class="t">%s</div><div class="d">%s</div></div>' % (2 + _i, _t, _d)
           for _i, (_t, _d) in enumerate(_AIV)) + '</div>'),
    lab(120, 508, "02 · SIDE BY SIDE · 传统人工催收 vs AI 辅助 / AI 语音催收", i=6, w=1200),
    sh("rise", "left:120px;top:538px;width:1680px;height:300px;--i:7",
       '<table class="mini ai-diff"><thead><tr><th style="width:170px">维度</th>'
       '<th style="width:640px">传统人工催收</th><th>AI 辅助 / AI 语音催收</th></tr></thead><tbody>'
       + "".join('<tr><td>%s</td><td>%s</td><td><span class="k" '
                 'style="color:var(--accent)">%s</span></td></tr>' % r for r in _DIFF7)
       + '</tbody></table>'),
    rule(850),
    land("AI 的价值不是「替代人」，而是"
         "<strong style='color:var(--accent)'>重构催收运营系统</strong>。"),
]))

# ═══ P11 · AI 方案架构 ·「智能催收 Agent 的能力闭环」（**第二动效重点**）═══════
#   大纲 P11 的八个模块逐字入图，按大纲「建议视觉」做中枢 + 环绕架构。
#   P8 质量语言六条逐条对表（这一页是本 deck 的架构语言标杆）：
#     ① 类型化线 + 图例：实线 accent = 主数据流 / 虚线 hair-strong = 事件 · 控制 /
#        点线 accent-deep = 指标回流。三型三色三粗，图例逐条对上。
#     ② 每页唯一 hot 件：中枢 Agent（全页唯一一枚 .mo-breathe + halo）。
#     ③ 每条线带「流的什么」：八条各一句（名单 · 触达策略 / 客户语音 → 文本 / …）。
#     ④ 闭环优先：质检与分析 → 客户分层与策略引擎的点线回流弧绕整图一圈 ——
#        没有这条弧，这张图只是「一堆模块挂在中间那个盒子上」；有了它才是**闭环**，
#        才对得上标题里的那三个字。
#     ⑤ 数字带时序标：本页无数字（数字全部在 P12 的 canon 里，不在架构图上重复）。
#     ⑥ 域分带：左 = 输入域（理解与约束）/ 右 = 输出域（执行与留痕）。
#   动效编排：左四条 + 右四条共八枚 .mo-packet（方向与箭头一致）、
#     两条控制虚线 .mo-drift、回流弧 .mo-cycle 包、中枢 breathe + halo = 13 件 / 5 种原语。
_MOD_IN = [   # (模块名, 副题, 流的什么, 线型)
    ("客户分层与策略引擎", "账龄 · 金额 · 风险 · 历史行为", "名单 · 触达策略", "solid"),
    ("实时语音识别",       "语音转文本，供理解与留痕",     "客户语音 &#8594; 文本", "solid"),
    ("大模型对话引擎",     "理解意图，生成下一步动作",     "意图 · 话术建议", "solid"),
    ("合规规则引擎",       "身份核验 · 话术边界 · 频次",   "边界 · 频次约束", "dash"),
]
_MOD_OUT = [
    ("AI 语音外呼",   "提醒 · 解释 · 协商 · 确认 · 跟进", "合规话术 · 实时对话", "solid"),
    ("业务系统集成",  "CRM · 催收系统 · 还款 · 工单",     "承诺 · 工单 · 还款", "solid"),
    ("质检与分析",    "质检结果 · 回收效果 · 投诉风险",   "全量对话记录", "solid"),
    ("人工接管机制",  "争议 · 投诉 · 身份异常 · 情绪升级", "转人工事件", "dash"),
]
_HUBX, _HUBY, _HUBW, _HUBH = 650, 137, 380, 170
def _hub_fig():
    o = []
    # ⑥ 域分带。带高 452、模块从 y44 起（不是 34）：域名 mono 行的基线在 y26，
    #   模块顶边压到 34 时两者只差 8px，域名读起来像第一个模块的副标题。
    o.append(domain_band(24, 0, 336, 452, "INPUT DOMAIN · 理解与约束", i=1))
    o.append(domain_band(1320, 0, 330, 452, "OUTPUT DOMAIN · 执行与留痕", i=1))
    # 左列：四个输入模块 → 中枢
    for k, (t, s, flow, kind) in enumerate(_MOD_IN):
        y = 44 + k * 104
        o.append(box(40, y, 304, 76, 8, i=k + 1))
        o.append(txt(58, y + 32, t, "ttl", size=21))
        o.append(txt(58, y + 58, s, "sm", size=14))
        # 正交总线：出盒右缘 → 竖到中枢水平中线段 → 进中枢左缘
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
    # 右列：中枢 → 四个输出模块
    for k, (t, s, flow, kind) in enumerate(_MOD_OUT):
        y = 44 + k * 104
        o.append(box(1336, y, 304, 76, 8, i=k + 1))
        o.append(txt(1354, y + 32, t, "ttl", size=21))
        o.append(txt(1354, y + 58, s, "sm", size=14))
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
    # ④ 闭环回流弧：质检与分析（右三，中心 y=290）→ 客户分层与策略引擎（左一，中心 y=82），
    #    绕整图外圈。右侧竖段走 x=1668（域分带右缘 1650 之外 18px）——
    #    压在带缘上会读成「带的边框」，而它恰恰是**离开输出域**的那条线。
    _ARC = ("M1640 290 H1652 Q1668 290 1668 306 V468 Q1668 484 1652 484 H34 "
            "Q18 484 18 468 V98 Q18 82 34 82 H36")
    o.append(packet(_ARC, 2140, seg=26, col=AD, w=10, op=".28", dur="9s", i=6, cls="mo-cycle"))
    o.append(dline(_ARC, AD, 3, 6, dash="3 8"))
    o.append(ah_r(40, 82, AD, 7))
    o.append(txt(840, 470, "回收 · 投诉 · 接通 · 履约 指标回流 &#8594; 下一轮分层与策略",
                 "sm", size=17, anchor="middle", col=AD))
    # ② 中枢（全页唯一 hot）
    o.append(halo_rect(_HUBX, _HUBY, _HUBW, _HUBH, 14, sc="1.08", op=".32", dur="3.6s"))
    o.append(box(_HUBX, _HUBY, _HUBW, _HUBH, 14, hot=True, i=7, cls="mo-breathe",
                 sty="--mo-dur:3.6s"))
    o.append(txt(840, _HUBY + 56, "智能催收 Agent", "ttl", size=32, anchor="middle", col=AC))
    o.append(txt(840, _HUBY + 92, "中枢：把策略、语音、理解、合规", "sm", size=17, anchor="middle"))
    o.append(txt(840, _HUBY + 118, "串成一次可交付的对话", "sm", size=17, anchor="middle"))
    o.append(txt(840, _HUBY + 148, "不是一个机器人，是一套系统能力", "sm", size=15,
                 anchor="middle", col=AC))
    o.append(legend(24, 528, [("solid", "主数据流"), ("dash", "事件 / 控制"),
                              ("dot", "指标回流")]))
    return "".join(o)
page("content", "".join([
    head("SOLUTION ARCHITECTURE · 能力闭环", "智能催收 Agent 的<strong>能力闭环</strong>。"),
    lab(120, 244, "01 · HUB &amp; EIGHT MODULES · 中枢 + 八模块", w=1200),
    figbox(120, 276, 1680, 1680, 560, _hub_fig(), i=1),
    rule(850),
    land("AI 催收不是单一机器人，而是<strong style='color:var(--accent)'>完整的系统能力</strong>"
         "——闭环靠的是那条指标回流，不是那八个盒子。"),
]))

# ═══ P12 · Agora 优势 ·「让语音 AI 从 Demo 走向生产可用」════════════════════
#   大纲 P12 的四项能力做骨架（实时交互 / 音频工程 / AI 生态集成 / 生产化与规模化），
#   **但硬数一律用司内 canon，不用大纲里的英文官网旧口径**（见文件头「已仲裁」段）：
#     · 650ms 端到端 / 340ms 打断 / 95% 环境干扰屏蔽 —— 引擎 deck P5 三件极致原句
#     · SAL 选择性注意力锁定 · AI-VAD · 优雅打断 · AI QoS —— 引擎 deck P7–P11
#     · 900亿+ 单月支撑通话分钟数 —— 引擎 deck P21 四卡之一
#     · 200+ **全球节点** SD-RTN —— 引擎 deck P21 页头注（宾语是节点，不是国家和地区）
#     · OpenAI Realtime API 全球首批合作伙伴 —— 引擎 deck P22 锚点行
#   底部 SD-RTN 底座带是本页唯一的图：一条**双向**通道（上行客户语音 / 下行智能体语音），
#   包在两条道上同时在途 = 全双工。两枚规模数钉在带上（都带口径标）。
#   本页无 .mo-breathe：hot 语汇让给 .card.on（实时交互是四能力之首）。
_CAP4 = [
    ("01 · REAL-TIME", "实时交互能力",
     "端到端响应延时低至 <b style=\"color:var(--accent)\">650ms</b>；用户随时插话，"
     "<b style=\"color:var(--accent)\">340ms</b> 即时收声。优雅打断让对话节奏接近真人。", True),
    ("02 · AUDIO", "音频工程能力",
     "环境干扰屏蔽 <b style=\"color:var(--accent)\">95%</b>：SAL 选择性注意力锁定 + AI-VAD "
     "语义判停 + 回声消除，嘈杂环境也能精准听清对话人声。", False),
    ("03 · ECOSYSTEM", "AI 生态集成能力",
     "LLM / ASR / TTS 自由组合，不被单一模型或供应商锁定；可与自有风控策略、催收系统、"
     "CRM 与合规规则引擎结合。", False),
    ("04 · PRODUCTION", "生产化与规模化",
     "录音、转写、监控与质量分析等生产环境能力；AI QoS 让极端弱网、瞬时断网也不掉线，"
     "适配高并发、强留痕的金融外呼场景。", False),
]
def _sdrtn_fig():
    o = []
    # 域分带：中间那条就是 SD-RTN
    o.append(domain_band(300, 24, 1080, 128, "SD-RTN · 软件定义实时网", i=1))
    # 两端
    for (x, t, s) in [(20, "智能催收 Agent", "策略 · 理解 · 话术"),
                      (1444, "客户手机", "移动网 · 复杂终端")]:
        o.append(box(x, 46, 216, 84, 8, i=2))
        o.append(txt(x + 108, 80, t, "ttl", size=21, anchor="middle"))
        o.append(txt(x + 108, 108, s, "sm", size=14, anchor="middle"))
    # 双向两条道（全双工：两条同时在途）
    for k, (y, lb, rev) in enumerate([(66, "下行 · 智能体语音", False),
                                      (110, "上行 · 客户语音", True)]):
        d = "M248 %d H1432" % y
        o.append(packet(d, 1184, seg=26, dur="3.4s", i=k + 2, rev=rev,
                        delay="-%.1fs" % (k * 1.7)))
        o.append(hline(248, 1432, y, AC, 2.4, k + 2))
        o.append(ah_r(1436, y, AC, 8) if not rev else ah_l(244, y, AC, 8))
        o.append(txt(1424, y - 12, lb, "sm", size=14, col=I3, anchor="end")
                 if not rev else txt(256, y - 12, lb, "sm", size=14, col=I3))
    # 节点脉冲（七枚，0.4s 错峰 ⇒ 一道亮波沿网横穿）：它们就是「200+ 全球节点」那句话的图形。
    # x 从 370 起、步长 160 ⇒ 370…1330，整排落在 SD-RTN 带（300–1380）之内，
    # 右端与「客户手机」盒（x1444）还有 114px 净空。**改带宽必须重算这一排。**
    for k in range(7):
        o.append('<circle class="pop mo-pulse" style="--i:%d;--mo-hi:.55;--mo-lo:.16;'
                 '--mo-dur:2.8s;--mo-del:%.1fs;fill:%s;opacity:.55" cx="%d" cy="88" r="8"/>'
                 % (k % 4 + 2, k * .4, AD, 370 + k * 160))
    # 两枚规模数（都带口径标）。x 取 340 / 860，与右下角的图例把底行三等分 ——
    # 第一版两枚都挤在 420 / 980，右半（x1100 以后）空着一大块，读成「图没画完」。
    for (x, v, u, note) in [(340, "900亿+", "单月支撑通话分钟数", "IR 公开口径"),
                            (860, "200+", "全球节点 · SD-RTN", "IR 公开口径")]:
        o.append(txt(x, 216, v, "ttl", size=42, col=AC, weight=700))
        o.append(txt(x, 246, u, "sm", size=17))
        o.append(txt(x, 270, note, "sm", size=13, col=I3, mono=True, ls=".12em"))
    o.append(legend(1340, 236, [("solid", "实时音频流 · 双向同时在途")]))
    return "".join(o)
page("content", "".join([
    head("WHY AGORA · 从 Demo 到生产", "Agora 让语音 AI 从 Demo 走向<strong>生产可用</strong>。"),
    lab(120, 244, "01 · FOUR CAPABILITIES · 四项能力"),
    sh("", "left:120px;top:278px;width:1680px;height:250px",
       '<div class="g4" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d"><div class="tag%s">%s</div>'
           '<div class="t">%s</div><div class="d">%s</div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag, _t, _d)
           for _i, (_tag, _t, _d, _on) in enumerate(_CAP4)) + '</div>'),
    lab(120, 562, "02 · INFRASTRUCTURE · 跑在实时互动底座之上", i=6),
    figbox(120, 594, 1680, 1680, 320, _sdrtn_fig(), i=7),
    rule(850),
    land("2024 OpenAI Realtime API 发布，声网为<strong style='color:var(--accent)'>"
         "全球首批合作伙伴</strong>——同样的工程能力，用来支撑贷后场景的每一通对话。", y=944),
    src(_SRC_AGORA),
]))

# ═══ P13 · 落地场景 ·「从低风险场景切入，逐步扩展到智能协商」═══════════════
#   大纲 P13 的三阶段与试点建议逐字。顶部一条**递增梯**（不是并列三卡）——
#   三阶段的关系是「风险与复杂度逐级抬升」，梯形本身就是这句话；
#   包沿梯面向上跑，读作「从阶段 1 走上去」，不是「三选一」。
_STAGES = [
    ("阶段 1", "提醒与确认", ["账单提醒", "还款日前提醒", "轻逾期 M0 / M1 提醒",
                             "承诺还款到期提醒", "还款链接发送和确认"]),
    ("阶段 2", "跟进与解释", ["承诺还款跟进", "分期方案说明", "逾期原因收集",
                             "材料补充提醒", "客户基础问题解答"]),
    ("阶段 3", "协商与质检", ["还款能力初步识别", "个性化方案推荐", "复杂争议转人工",
                             "投诉风险识别", "外包催收质检", "坐席实时辅助"]),
]
_ADVICE = [
    ("选择一个产品", "例如<b>信用卡、消费贷、分期</b>产品"),
    ("选择一个账龄段", "建议从 <b>M0 / M1</b> 或还款提醒开始"),
    ("选择一类低争议客群", "避免一开始进入投诉、争议和法催场景"),
    ("设置试点周期", "<b>4–8 周</b>，对比 AI 与人工 / 传统外呼效果"),
]
def _ladder_fig():
    """三级台阶：细横条 + 上方标名，不是三只大盒子 ——
       大盒子会和下面的三张卡讲同一件事两遍，梯子只负责说「越往右越难」。"""
    o = []
    for k, (_s, _t, _bs) in enumerate(_STAGES):
        x, y, w = 40 + k * 552, 90 - k * 28, 500
        # 台阶条自己按 0.6s 依次亮起 ⇒ 一道亮波从阶段 1 走到阶段 3。
        # ⚠ 前两条自带 opacity:.5，所以 --mo-hi 必须跟着写 .5（moPulse 的 0%/100% 帧是它）
        #   —— 不写就会被动画顶成 1，SELFPIN 的「100% 帧 = 静态原图」当场对不上。
        _hi = None if k == 2 else ".5"
        _v = "--i:%d;--mo-lo:%s;--mo-dur:3.6s;--mo-del:%.1fs" % (k + 1, ".16" if k == 2 else ".2", k * .6)
        if _hi: _v += ";--mo-hi:%s" % _hi
        o.append('<rect class="pop mo-pulse" style="%s;fill:%s%s" x="%d" y="%d" width="%d" '
                 'height="10" rx="5"/>' % (_v, AC, (";opacity:%s" % _hi) if _hi else "", x, y, w))
        o.append(txt(x + w // 2, y - 14, "%s · %s" % (_s, _t), "ttl", size=22,
                     anchor="middle", col=AC if k == 2 else None))
        if k < 2:
            x1, x2 = x + w, x + w + 52
            d = "M%d %d L%d %d" % (x1 + 4, y + 5, x2 - 14, y - 23)
            o.append(packet(d, 56, seg=16, dur="1.6s", i=k + 1, delay="%.1fs" % (k * .5)))
            o.append(pline(d, AC, 2.4, k + 1, ln=56))
            o.append(ah_r(x2 - 2, y - 27, AC, 8))
    o.append(txt(40, 30, "风险与复杂度逐级抬升", "sm", size=16, col=I3))
    # 起步基线走 .mo-drift（图例里那一栏写的就是虚线，线必须真的是虚的）：
    # off −180 = dash「4 6」周期 10 的 18 个整周期 ⇒ 100% 帧 = 静态原图。
    o.append(dline("M40 116 H1640", HS, 1.4, 1, dash="4 6", cls="mo-drift",
                   sty="--mo-off:-180;--mo-dur:5s"))
    o.append(legend(40, 146, [("solid", "上台阶 · 逐级扩展"), ("dash", "起步基线")]))
    return "".join(o)
page("content", "".join([
    head("ROLLOUT · 落地路径", "从<strong>低风险场景</strong>切入，逐步扩展到智能协商。"),
    lab(120, 244, "01 · THREE STAGES · 三阶段"),
    figbox(120, 272, 1680, 1680, 160, _ladder_fig(), i=1),
    # ⚠ 场景条目走**一枚 .d 里的 <br> 列表**，不是六个 .d 子元素：.card 的 flex gap 是 13px，
    #   六个子元素就是 78px 的额外高度，第一版正是这么把阶段 3 的后两条挤出卡底的（截图实锤）。
    #   版式账：卡高 300 = padding 40 + tag 18 + gap 9 + 6 行×(18×1.85 = 33.3) = 267 + 余量 33。
    sh("", "left:120px;top:444px;width:1680px;height:300px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card sm%s rise" style="--i:%d"><div class="tag%s">%s · %s</div>'
           '<div class="d" style="line-height:1.85">%s</div></div>'
           % (" on" if _i == 0 else "", 2 + _i, " am" if _i == 0 else "", _s, _t,
              "<br>".join("· " + _b for _b in _bs))
           for _i, (_s, _t, _bs) in enumerate(_STAGES)) + '</div>'),
    lab(120, 768, "02 · PILOT DESIGN · 试点建议", i=6),
    sh("flow", "left:120px;top:794px;width:1680px;height:48px;--i:7",
       '<div class="adv">' + "".join(
           '<div><div class="h">%s</div><div class="b">%s</div></div>' % (_h, _b)
           for _h, _b in _ADVICE) + '</div>'),
    rule(850),
    land("先在低争议、高重复的场景里把闭环跑通，再往协商与质检扩展——"
         "<strong style='color:var(--accent)'>不需要一次性替换整条链路</strong>。"),
]))

# ═══ P14 · 试点 KPI ·「用可量化指标验证 AI 催收价值」（大纲第 4 节补充页）══════
#   Colin 指令：这一页插在落地场景之后。大纲第 4 节的五类指标逐字。
#   **注意事项的措辞照抄大纲**，一个字不改 —— 这两句是本 deck 的免责边界：
#     「不建议在没有客户试点数据前承诺固定提升比例。」
#     「更稳妥的表达是：通过试点验证接通、履约、成本和合规指标改善空间。」
#   ⚠ 全页不出现任何百分比数字：本页讲的是**要量什么**，不是「能提升多少」。
#   ⚠ 版式判断（替 Colin 做的）：大纲给的是一张「类型 | 指标」两列表，但两列表在 1920 舞台上
#     只吃掉左边 40%，右边 60% 空着 —— 读者第一反应是「这页没做完」，而不是「这页很克制」。
#     所以内容逐字不动，形从表改成**五张卡**（.g5，与 P8 五趋势同族但走 .n 大号序号语域）。
_KPI = [
    ("01", "触达类", ["接通率", "有效沟通率", "短信 / 还款链接点击率"]),
    ("02", "回收类", ["承诺还款率", "承诺履约率", "回收金额", "账龄迁徙率"]),
    ("03", "效率类", ["单案触达成本", "坐席替代率", "人工接管率", "平均处理时长"]),
    ("04", "合规类", ["投诉率", "违规话术命中率", "质检覆盖率", "录音 / 摘要完整率"]),
    ("05", "体验类", ["客户中断率", "负面情绪占比", "协商成功率"]),
]
page("content", "".join([
    head("PILOT KPI · 验证口径", "用<strong>可量化指标</strong>验证 AI 催收价值。"),
    lab(120, 244, "01 · FIVE FAMILIES · 五类指标"),
    sh("", "left:120px;top:276px;width:1680px;height:380px",
       '<div class="g5 kpi" style="height:100%">' + "".join(
           '<div class="card rise" style="--i:%d"><div class="n">%s</div>'
           '<div class="t">%s</div><div class="m">%s</div></div>'
           % (2 + _i, _n, _t, "<br>".join("· " + _m for _m in _ms))
           for _i, (_n, _t, _ms) in enumerate(_KPI)) + '</div>'),
    lab(120, 692, "02 · CAVEAT · 注意事项", i=5),
    sh("flow", "left:120px;top:724px;width:1680px;height:88px;--i:6",
       '<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;height:100%">'
       '<div class="note grey" style="font-size:20px;align-self:center">'
       '不建议在没有客户试点数据前承诺固定提升比例。</div>'
       '<div class="note" style="font-size:20px;align-self:center">'
       '更稳妥的表达是：通过试点验证接通、履约、成本和合规指标<b style="color:var(--accent)">'
       '改善空间</b>。</div></div>'),
    rule(850),
    land("试点的产出不是一个承诺，而是一组"
         "<strong style='color:var(--accent)'>你自己账上的对照数据</strong>。"),
]))

# ═══ P15 · 结尾（title 板）·「未来催收的竞争力」═══════════════════════════
#   大纲 P14 的行业判断四条 + **推荐收尾语逐字**（Colin 点名）。
#   收尾语渲染成**一段连续文本**（不拆成三栏）——三栏视觉更漂亮，但那样
#   textContent 里的分号与句读就断了，「逐字」这三个字也就名存实亡。
#   版式账：主标 76px 双行，盒 1680 居中；行盒 76×1.22 = 92.7 > CJK 内容高
#   （≈76×1.115 = 84.7）⇒ 不会被 .ink 的液态扫过 mask 裁掉一线。
_VERDICT = [
    "逾期资产管理是金融机构长期能力，不是短期运营动作。",
    "传统催收模式的人效、合规和体验瓶颈越来越明显。",
    "AI 可将优质坐席能力、合规规则和运营策略规模化复制。",
    "未来催收不是更高压，而是更智能、更合规、更可协商。",
]
page("title", "".join([
    sh("flow kk", "left:120px;top:118px;width:1680px;height:28px;text-align:center",
       "CLOSING · 行业判断"),
    sh("ink", "left:120px;top:176px;width:1680px;height:200px;text-align:center;"
       "font:700 76px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "未来催收的竞争力，是<br>AI + <strong style='color:var(--accent)'>合规</strong> + "
       "实时交互基础设施。"),
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
    # 推荐收尾语（逐字 · 一段连续文本）
    sh("ink", "left:260px;top:648px;width:1400px;height:190px;text-align:center;"
       "font:700 40px/1.6 var(--f-cn);letter-spacing:-.01em;color:var(--ink)",
       "AI 负责<strong style='color:var(--accent)'>规模化、标准化和实时分析</strong>；"
       "人工负责<strong style='color:var(--accent)'>复杂判断、情绪安抚和例外处理</strong>；"
       "Agora 提供连接 AI 与真实客户对话的"
       "<strong style='color:var(--accent)'>实时语音基础设施</strong>。"),
    sh("flow mono-sm", "left:120px;top:892px;width:1680px;height:24px;text-align:center;--i:6",
       "AGORA · CONVERSATIONAL AI ENGINE · 实时语音 AI 基础设施"),
    # CTA：纯文本 mono 行，不做假链接样式（没有 <a>，不加下划线 / 悬停态）
    sh("flow mono-sm", "left:120px;top:930px;width:1680px;height:24px;text-align:center;--i:7",
       "DEMO / 文档 · agora.io &#8250; 对话式 AI 引擎 · 联系团队"),
]))


# ═══ 组装 ═══════════════════════════════════════════════════════════════════
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
        '<!DOCTYPE html>\n<html lang="zh-CN"><head>\n'
        # 主题初始化：与 convoai-engine / convoai-info 同一个 localStorage 键
        '<script>try{if(localStorage.getItem("colin-theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}</script>\n'
        '<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>AI 驱动的智能贷后催收解决方案</title>\n'
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
        '<button class="deck-swap" id="deckSwap">暗底</button>\n'
        # 2026-08-30 Colin：同链路语言切换 —— 保留原链接，一枚常显 pill 跳到东南亚英文版。
        # ⚠ 必须 <button> + JS，**不能用 <a>**（本 deck 的 a[href]=0 闸还在）。
        # 摆位与主题钮同角（左下），摞在它之上 24 + 28 + 10 = 62px，不打架。
        '<button class="deck-lang" id="deckLang">EN</button>\n'
        # deckSwap 常显 chip（与引擎 deck 逐字同源）：这是一份**发链接**的私享 deck，
        # 「默认隐身 · hover 呼出」在这里等于键不存在。实底 --card-bg-2 而不是
        # transparent —— 左下角坐着 content 板的矩阵纹理，透明底会让 12px mono 掉进纹理里。
        '<style>.deck-swap{position:fixed;left:26px;bottom:24px;z-index:1100;font-family:var(--f-mono,monospace);'
        'font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);'
        'border-radius:3px;padding:7px 12px;opacity:.62;'
        'transition:opacity .3s,color .3s,border-color .3s;background:var(--card-bg-2);cursor:pointer;}'
        '.deck-swap:hover,.deck-swap:focus-visible{opacity:1;color:var(--accent);border-color:var(--accent);}'
        '.deck-swap:focus:not(:focus-visible){outline:none;box-shadow:none;}'
        '@media print{.deck-swap{display:none!important;}}</style>\n'
        # 语言钮：deckSwap 同款样式体系（同角、同尺寸、同透明度节奏），只换 bottom 与文案
        '<style>.deck-lang{position:fixed;left:26px;bottom:62px;z-index:1100;'
        'font-family:var(--f-mono,monospace);'
        'font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);'
        'border-radius:3px;padding:7px 12px;opacity:.62;'
        'transition:opacity .3s,color .3s,border-color .3s;background:var(--card-bg-2);cursor:pointer;}'
        '.deck-lang:hover,.deck-lang:focus-visible{opacity:1;color:var(--accent);border-color:var(--accent);}'
        '.deck-lang:focus:not(:focus-visible){outline:none;box-shadow:none;}'
        '@media print{.deck-lang{display:none!important;}}</style>\n'
        "<script>" + (SRC / "deck.js").read_text(encoding="utf-8") + "</script>\n"
        '<script>(function(){var b=document.getElementById("deckSwap");'
        'function apply(t){if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");b.textContent="浅底";}'
        'else{document.documentElement.removeAttribute("data-theme");b.textContent="暗底";}}'
        'var cur="light";try{cur=localStorage.getItem("colin-theme")||"light";}catch(e){}apply(cur);'
        'window.__setTheme=apply;'
        'b.addEventListener("click",function(){b.blur();'
        'var now=document.documentElement.getAttribute("data-theme")==="dark"?"dark":"light";'
        'var nxt=(now==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",nxt);}catch(e){}apply(nxt);});})();</script>\n'
        # 语言钮跳转：预览服务器（8899 / 8777）是静态目录服务，没有 next.config 的 rewrites，
        # 线上才有 /convoai-postloan-en 路由 —— 按当前 pathname 是否带 .html 二选一，
        # 两个环境都跳得通（QA 的互跳 round-trip 靠这一手才跑得起来）。
        '<script>(function(){var b=document.getElementById("deckLang");if(!b)return;'
        'b.addEventListener("click",function(){b.blur();'
        'var f=/\\.html($|[?#])/.test(location.pathname);'
        'location.href=f?"/decks/convoai-postloan-en.html":"/convoai-postloan-en";});})();</script>\n'
        "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")

    # ── 构建期断言（红线在这里就拦住，别等到 qa）──────────────────────────────
    assert total == 15, "页数漂移：%d != 15" % total
    assert doc.count("<section") == 15, "section 数漂移：%d" % doc.count("<section")
    boards = {i: b for i, (b, _y) in enumerate(PAGES, 1)}
    assert {i for i, b in boards.items() if b == "title"} == {1, 15}, \
        "title 板页漂移：%r" % sorted(i for i, b in boards.items() if b == "title")
    # 零分步：data-steps 全 0，**页内**一枚 data-step 都不许有。
    # ⚠ 只能查 <section> 段：共享 deck.js 与 motion.css 里本来就写着 '[data-step]' 选择器，
    #   拿整份 doc 去查会稳报一条假命中。
    assert doc.count('data-steps="0"') == 15, "data-steps 不全为 0"
    _stage_html = "\n".join(secs)
    assert 'data-step="' not in _stage_html, "出现了 [data-step] —— 本 deck 是零分步 deck"
    # 表达红线六词（子串匹配；「强催」会命中「加强催收」，这是刻意的）
    for _bad in ("催债", "施压催收", "逼迫还款", "强催", "轰炸外呼", "暴力催收"):
        assert _bad not in doc, "表达红线：全 deck 不许出现「%s」" % _bad
    # 客户名 / 产品名 / 价格 / staging / 盲测：本 deck 是引擎基础设施 + 解决方案
    for _bad in ("光潽", "Call Agent", "¥8,500", "¥2,999", "¥5,501",
                 "8,500", "2,999", "5,501", "staging", "盲测", "32,000"):
        assert _bad not in doc, "红线：全 deck 不许出现「%s」" % _bad
    # 已仲裁：大纲 P12 的英文官网旧口径不许回归
    for _bad in ("800 亿分钟", "800亿分钟", "200+ 国家", "200+国家"):
        assert _bad not in doc, "口径红线：英文官网旧口径「%s」已仲裁不用" % _bad
    # a[href] = 0（指路走纯文本）
    assert "<a " not in doc.split('id="deckStage"')[1].split("</div>\n</div>")[0], \
        "舞台里出现了 <a> —— 本 deck 指路必须是纯文本"
    # 「回收率」不得与具体百分比同句
    import re as _re
    _plain = _re.sub(r"<[^>]+>", "", doc)
    for _sent in _re.split(r"[。；！？\n]", _plain):
        if "回收率" in _sent:
            assert not _re.search(r"\d+(\.\d+)?%", _sent), \
                "红线：「回收率」与具体百分比同句 —— 本 deck 不承诺提升比例：%r" % _sent.strip()[:60]
    # SOURCE ledger：五张数据页（P3/P4/P7/P9/P12）各一行、**严格四段制**、
    # 结尾一律「事实截止 2026.08」、来源只写机构名不写 URL。
    # P14 试点 KPI 没有外部出处（那是方法论不是事实），故不挂 ledger 行。
    _srcs = _re.findall(r'<div class="sh flow src"[^>]*>(SOURCE[^<]*)</div>', doc)
    assert len(_srcs) == 5, "SOURCE ledger 行数漂移：%d != 5（%r）" % (len(_srcs), _srcs)
    for _s in _srcs:
        assert _s.startswith("SOURCE · "), "SOURCE 行不以「SOURCE · 」起手：%r" % _s
        assert _s.endswith(" · 事实截止 2026.08"), "SOURCE 行未以事实截止收尾：%r" % _s
        assert _s.count(" · ") == 3, "SOURCE 行不是四段制：%r" % _s
        assert "http" not in _s, "SOURCE 行写了 URL —— 家族格式只写机构名：%r" % _s
    # 行业侧数字在场闸（一个都不许在改版里被搬丢）
    _page_txt = {int(x.split('"')[0]): x
                 for x in doc.split('<section class="slide conf-boarded" data-p="')[1:]}
    for _p, _kws in [(3, ["3.7", "1.51", "239.2", "2026Q1 末"]),
                     (4, ["6.87", "6.96", "2025 年末", "2026Q1 末"]),
                     (7, ["5 年", "GB&#47;T 45251-2025", "2025.02.28"]),
                     (9, ["59.8", "137.7", "9.72", "49", "93"]),
                     (12, ["650ms", "340ms", "95%", "900亿+", "200+"])]:
        for _kw in _kws:
            assert _kw in _page_txt[_p], "P%d 缺在场事实「%s」" % (_p, _kw)
    # Agora canon 在场闸（引擎 deck 逐字同源的四件套）
    for _kw in ("SAL 选择性注意力锁定", "AI-VAD", "优雅打断", "AI QoS"):
        assert _kw in _page_txt[12], "P12 缺 canon「%s」" % _kw
    assert "全球首批合作伙伴" in _page_txt[12], "P12 缺 OpenAI 锚点行"
    # 收尾语逐字（Colin 点名）
    for _kw in ("规模化、标准化和实时分析", "复杂判断、情绪安抚和例外处理",
                "实时语音基础设施"):
        assert _kw in _page_txt[15], "P15 收尾语缺「%s」" % _kw
    # 试点 KPI 页的免责措辞逐字
    for _kw in ("不建议在没有客户试点数据前承诺固定提升比例",
                "通过试点验证接通、履约、成本和合规指标"):
        assert _kw in _page_txt[14], "P14 缺免责措辞「%s」" % _kw
    # 每页至多一枚 .mo-breathe（P8 质量语言第 ② 条「每页唯一 hot 件」）
    for _p, _t in _page_txt.items():
        _n = _t.count("mo-breathe")
        assert _n <= 1, "P%d 有 %d 枚 .mo-breathe —— 每页至多一枚 hot 件" % (_p, _n)
    print("convoai-postloan.html · %d 页 · %dKB · conf-light 默认 · 零分步 · "
          "SOURCE ledger %d 行" % (total, len(doc) // 1024, len(_srcs)))

if __name__ == "__main__":
    build()
