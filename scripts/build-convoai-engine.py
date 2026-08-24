#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-engine.py ·《声网 · 对话式 AI 引擎 · 深入讲解》22 页
# CONF 家族 · conf-light 默认 · 单文件双主题 —— 以 build-convoai-info.py 为母版克隆
#   （同一套 DECK_CSS token / conf-light·dark 背景板 / deck.js 运行时 / noindex / 双主题）
#
# 这份 deck 是 convoai-info P4「引擎产品详解」抽屉的内容（iframe 载入）。
# 2026-08-18 重建：旧版是 Apple 风格 13 页横滚（git 历史里可回溯），
# 内容 1:1 移植、版式用家族语法重绘，只有 P12 的数字口径按 Colin 指错做了修正。
# 2026-08-20 扩为 16 页：补三张「机理」页（双工三模式 / 全双工工作原理 / VAD），
#   全部复用既有家族件（sh/rule/lab/figbox/head/land/rail/box/txt/hline/ah_*/dline/
#   .g3 .g4 .card .card-c .chip .note .mono-sm .seclab .land .table.mini），未开新体系。
# 2026-08-20（二轮 · 已仲裁）扩为 17 页：VAD 之后插入「产品架构大图」，
#   并给 P6 / P7 / P14（今 P14 接入架构）各加一步 build（data-steps + [data-step]）。
# 2026-08-21（大内容轮）扩为 20 页：P10 SAL 重做（三种噪声 · 三层方案 + 双层防御环）／
#   P11 弱网重做（补 AI QoS 断网续播机理）／P12 多模态改造（聚焦视觉模态）／
#   新增 P13 Physical AI · R1 开发套件、P14 Physical AI · 已经上岗（案例墙）、
#   P19 OpenAI 合作（title 板 quote 语域）；原 P13 编排 → P15 并做「箭头语义修」。
# 2026-08-21（收束轮）收到 18 页 —— 加法轮之后的减法轮，四件事：
#   ① 删 P14 案例墙：客户 logo 墙是 convoai-info 的活儿（那份 deck 已有同一批案例），
#      引擎 deck 讲的是引擎怎么工作，一整页缩略图在这条叙事里是插播广告。
#   ② 删原 P20 收尾页：末页金句与 P1 封面是同一句话的两次说法，两页收尾等于没收尾；
#      页上唯一不可替代的东西是 CTA 行 —— 它随页删除会掉入口，故继承到新末页页脚。
#   ③ P13 带实拍图重排（借鉴 robot26 #32 的两张大图卡）。
#   ④ P19 OpenAI 合作升为 P18 末页：加 OpenAI × Agora logo 锁定版 + 继承来的 CTA 行。
#   同轮把 deckSwap 主题键从「默认隐身」改成常显 chip（Colin：「没有浅色切换的键」）。
# 2026-08-21（动效全覆盖轮）三件事，页数不变（仍 18）：
#   ① P10 的常驻动效升格为 **deck 级运动语言**：五个原语（flow-packet / dash-drift /
#      pulse / breathe / cycle）做成可复用类，写在 DECK_CSS 顶部（连纪律一起写在那儿），
#      P2/P4/P6/P7/P8/P9/P11/P12/P13/P14 各按页情套用，P10 自己改用同一套类（视觉零变化）。
#      纪律：100% 帧 = 静态原图 / 动效元素不携带文字 / reduced-motion + print 全关 /
#      非当前页 animation-play-state:paused。自证工具：scripts/qa-motion.mjs（四闸）
#      与 scripts/pinned-diff.mjs（RM=1 两版逐像素比对，全页 0 差异）。
#   ② R1 产品图完整显示（Colin：「图片展示不全，比例看看」）：图在上 / 规格在下的竖卡
#      改成图左 / 规格右的横卡，图窗 380×510 让 cover 由高定标 ⇒ 4:3 原片纵向整幅入画，
#      两块板四边一格不缺。腾挪账见 DECK_CSS 的 .r1-card 段与 R1 页头注释。
#   ③ P3 三张小图改「对话版」：A 在左 / B 在右、时间竖直向下（Colin：「对话 AB 上下关系，
#      左右是不是更贴切？试试看」）。差异两行表与 land 不动；卡高与其后所有 y 不动。
# 2026-08-21（Call Agent 章）18 → 21 页 —— 加三页 + 一次整章重排，两件事：
#   ① 新增 Call Agent 三页（■）：P16 登场 · 成绩单 / P17 五个大脑 · Agent Harness /
#      P18 Loop Engineering · 成长飞轮。文案全部是 Call Agent 官网定稿逐字使用
#      （Colin 已核），红线四条写在 P16 页头：不出价格 / 不出 staging URL /
#      不出四位智能体人名 / 96.5% 必须带「盲测 32,000 名真实客户」口径。
#   ② 页序按 Colin 指令重排：**场景之后接 Call Agent，Call Agent 之后接 R1**。
#      位移对照（正文一个字节没动，只是换了位置）：
#        原 14 编排 → 13 ／ 原 15 接入架构 → 14 ／ 原 16 场景 → 15 ／
#        原 13 R1 → 19 ／ 原 17 Why Agora → 20 ／ 原 18 OpenAI → 21。
#      因此分步页从 [6,7,15] 变成 [6,7,14]，口径锁页从 17 变成 20，
#      title 板两页从 {1,18} 变成 {1,21} —— 三处闸门同步改在 build() 与 qa 里。
#      P12 的 land「让对话，走出屏幕」保留原句（它现在遥指 P19 R1，Colin 已认可）。
# 2026-08-21（视频页）21 → 22 页：Colin 指令「R1 之后再插一页 robot26 #24 同款全屏视频页」——
#   新 P20 = 无人机秀 demo 全屏片子（跨引用 robot26 的 demo.mp4 + demo-poster.jpg），
#   Why Agora → P21、OpenAI 末页 → P22。机制整套复刻 robot26 #24（不带 controls 属性 /
#   悬停呼出 / preload（2026-08-23 起 metadata）/ muted+playsinline / data-play-step 步进开播），
#   播放挂钩写在 build() 的内联脚本里 —— **不改共享 deck.js**（那份 runtime 三份 deck 共用）。
#   连带：分步 [6,7,14] → [6,7,14,20]、口径锁 20 → 21、title 板 {1,21} → {1,22}；
#   bake-archive 把 demo.mp4 换成线上绝对地址（3.1MB 不进 base64，poster 照常内联）。
# 2026-08-23 精修轮（GPT 5.6 review 采纳项 · 已仲裁定案 · 本文件占 C/E/F/G 四项 · 页数不变）：
#   C SOURCE ledger 统一成四段：`SOURCE · 来源 · 样本或时间窗 · 事实截止 2026.08`，
#     全部走新 helper src() 与新类 .src。P5/P7/P8/P11/P19 就地并段（多来源用「/」并列、
#     补「事实截止」收尾），P16/P18/P21 原样（本来就是这个形状），**P17 补上原本缺失的
#     那一行**（与 P16/P18 逐字同源，落在页脚三栏的中栏）。
#     只重排页内既有事实，不新增任何来源 / 样本 / 定义细节；缺口记进交付报告。
#   E P20 首帧：preload none → metadata + 补一枚静态角标 kicker（反白左上角，
#     不挂 data-step、不挂 mo-* 原语）；播放机制一字未动；浅色仍是电影感黑底全幅。
#   F P8 / P14 kicker 消歧：P8 补「ENGINE INTERNALS · 运行时内部链路」，
#     P14 补「INTEGRATION · 客户接入架构」；**只动 kicker 行，标题与图零触碰**。
#   G 投影小字提一档：.sig 与新类 .src 字号 15 → 17、色阶各上一格（与 info builder 逐字同源）。
#
# 2026-08-23 三数章重构 + 封面换主标 + P3 动效（本轮 · 页数不变 22）：
#   ① P1 封面主标换「对话即交互。」（Colin 亲定 · 200px 单行 · 「交互」走 accent），
#      kicker 末段「产品介绍」→「DEEP DIVE · 深入讲解」；原主标「2 行代码…」整句退场。
#   ② P3 双工三模式入运动件名册：两列之间做成**两条方向通道**，包跑在通道上 ——
#      单工只有 A→B 有包、半双工两向严格互斥（占空比 1/3 + 半周期相位差）、
#      全双工两向同时在途。运动模式本身就是三种双工的定义（页头注有相位算法）。
#   ③ 三数章重构（**只在 6–10 区间轮转**，正文一个字节没动，只换位置）：
#        新序 P5 三件极致 → P6 拆 650 → P7 拆 340·前提 → P8 拆 340 → P9 拆 95% → P10 大图收束
#        位移对照：原 8 大图 → 10 ／ 原 9 打断 → 8 ／ 原 10 SAL → 9；P11 起全部原位不动。
#        为什么：原序把大图夹在 P7（前提）与 P9（结论）之间，三个数字的展开被拦腰截断。
#        连带三件：展开页 kicker 前绑数字（EXTREME 01/02/03）／P5 三卡加章内指针 + 导航 land／
#        P10 大图钉三枚数字锚点 chip + 章尾收束句（**只做加法**，大图几何一格未动）。
#        分步页 [6,7,14,20]、title 板 {1,22}、口径锁 21 全部不受影响（重排没碰到它们）。
#
# 结构（22 页；★ = 一轮新增，☆ = 二轮新增，◆ = 2026-08-21 新增 / 重做，■ = Call Agent 章）：
#   P1  封面（title 板）        P2  实时决策        P3  双工三模式 ★（动效即语义 ◆）
#   P4  全双工工作原理 ★        P5  三件极致（三数章目录）  P6  拆 650 · 实时语音链路（build ×1）
#   P7  拆 340 · 前提 · VAD ★（build ×1）  P8  拆 340 · 优雅打断
#   P9  拆 95% · SAL 三噪声三方案 ◆（常驻动效 ◆）
#   P10 大图收束 · 产品架构大图 ☆（三枚数字锚点 ◆）    P11 弱网 · AI QoS ◆
#   P12 多模态 · 聚焦视觉 ◆     P13 开放编排（箭头语义修 ◆）
#   P14 接入架构（build ×1）    P15 典型场景
#   P16 Call Agent 登场 · 成绩单 ■     P17 五个大脑 · Agent Harness ■（架构页 · P8 语言）
#   P18 Loop Engineering · 成长飞轮 ■  P19 Physical AI · R1 ◆（带实拍图）
#   P20 无人机秀 DEMO ▶（全屏视频页 · robot26 #24 同款 · build ×1）
#   P21 Why Agora（口径锁）
#   P22 OpenAI 合作 ◆（title 板 · 末页 · logo 锁定版 + CTA）
#
# ── P13 箭头语义修（2026-08-21 · Colin：「箭头流向会让大家懵逼」）────────────
#   旧版同屏三种箭头语义、两种阅读方向：① 槽内 ⇄ 换装小箭头（accent，与主流同色同粗）
#   ② 左列四条交叉贝塞尔 → 引擎（指右）③ 引擎 → 右列两条贝塞尔（也指右）——
#   ②③ 视觉方向一致而语义相反（进 / 出），引擎被读成「过路站」而非「插槽机」。
#   新版：插槽语义只保留一种阅读方向 =「模块插入引擎」，左右两列的连线一律指向引擎，
#   贝塞尔全部换成正交总线（不交叉）；⇄ 换装只以小号灰件出现在模块块上方；
#   引擎 → 发布带改为无箭头细连线（它是附属说明，不是第三种流向）。
#   同屏箭头语义 = 2（插入 / 换装），图例逐条对上。（该页页号 13 → 15 → 14 → 13）
#
# ── P21 数据口径（Colin 2026-08-18 指错，改为 31p 拜访版 P2 的锁定口径，一字对齐）──
#   旧（错）：No.1 对话式 AI 引擎市场占有率 / 93万+ / 700亿+ / 200+ 覆盖场景 · 20+ 行业
#   新（对）：No.1 市场占有率 / 50+ 技术突破 / 100万+ 注册应用 / 900亿+ 单月分钟数
#            + IDC 43.4% 注 + SOURCE 行
#   200+ 的正确用法是「全球节点 · SD-RTN」，不是覆盖场景 —— 四卡足够，不补第五个数字。
#
# ── 踩过的坑（与母版同一份，移植 SVG 必守）─────────────────────────────────
#   · svg 一律 style="width:100%;height:auto"，.sh 高度 = width×viewBoxH/viewBoxW，
#     否则 stage.css 的 svg{max-height:100%} 会把图压扁
#   · SVG 里换色一律写内联 style="fill:…"，呈现属性 fill= 压不过 .fig .lbl/.ttl 的 CSS fill
#   · .dw 的 --len 必须≈路径长度，否则线不出来
#   · content 背景板自带一条 accent 细线在 y848–852（x120–761）：那一带不放文字，
#     rule(850) 正好压住它当收口线
#   · .pp .sh{overflow:visible}（0,2,0）：需要裁切时写 .pp .sh.CLASS{overflow:hidden}
#   · components.css 的 b,strong{color:var(--ink)} 会压继承色，深色面板里的 b 要 color:inherit
#   · 网格（.g2/.g3/.g4）一律写 height:100%：让卡片撑到 .sh 盒底，
#     否则卡片高度自适应会溢出 .sh 盒 → occlusion-scan 的 TEXT-x-SPILL
# ═══════════════════════════════════════════════════════════════════════════
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
# 2026-08-13 Colin：/convoai 主路由换装本 deck；convoai-engine.html 保留为别名
# （抽屉 iframe/已外发链接指它），双生同字节由本 builder 一次写出，杜绝漂移。
OUT = ROOT / "public" / "decks" / "convoai.html"
OUT_ALIAS = ROOT / "public" / "decks" / "convoai-engine.html"
B = "/decks/assets/conf-boards/"

def css(name):
    return (SRC / name).read_text(encoding="utf-8")

FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>"""

# ── 背景板（两张：title 给 P1/P22，content 给其余）─────────────────────────
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

# ── 本 deck 专属 CSS（母版 DECK_CSS 的引擎版：删掉 info 专属的 hero / eco / 案例墙 /
#    抽屉件，保留 token 体系与 kicker/hh/sub/seclab/rule/chip/card-c 等家族组件）──
DECK_CSS = """<style id="convoai-engine-deck">
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
/* ── 投影可读性（2026-08-23 · GPT 5.6 review 采纳项 G · 与 convoai-info 逐字同源）──
   .sig（页码）与 .src（SOURCE ledger 行）是投影上最先糊掉的两处小字：15px mono 在
   1920 舞台上被会议室投影再缩一道，落到屏上只剩十来个像素，而 --sig-ink(.30) 与
   --ink-3 又各自坐在最弱的一档色阶上。两枚一起提一档 —— 字号 15 → 17、色阶各上一格
   （.sig：--sig-ink → --ink-3；.src：--ink-3 → 向 --ink-2 走 55% 的中间色）。
   ⚠ 色阶只能走 color，**不许用 opacity** —— 入场系（.slide.visible .flow，0,2,0）
     本来就在动 opacity，写在类上的那一档会被它整条压掉（实测 computed 恒为 1）。
   提的是「看得清」，不是「抢眼」：仍旧远轻于正文与主视觉。 */
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 17px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--ink-3);}
.src{font:500 17px/1.4 var(--f-mono);letter-spacing:.08em;
  color:color-mix(in srgb,var(--ink-2) 55%,var(--ink-3));}
/* 版式件（与 convoai-info 同源） */
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
/* chip 的 accent 变体（与 .card.on / .card-c.on 同一套「这一枚是重点」的约定） */
.chip.on{border-color:color-mix(in srgb,var(--accent) 52%,transparent);color:var(--accent);}
/* 移植 inspire26/dual26 版式：.fig 内的 SVG 走 width:100%;height:auto，
   必须解掉 stage.css 的 svg{max-width:100%;max-height:100%}，否则定高 .sh 里会被压扁 */
.fig svg{max-width:none;max-height:none;}
/* 深色面板里的 b：components.css 的 b,strong{color:var(--ink)}（0,0,1）会把它染成主题墨色，
   在深底上等于隐形。本 deck 目前没有烧死深底的面板，规则留作护栏。 */
.on-dark b,.on-dark strong{color:inherit;}
/* ── P10 三种噪声阶梯（.rows 的页级档）───────────────────────────────────
   噪声 / 例子 在同一顶线，方案另起一行并按 01→03 逐级右移 —— 缩进本身就是「递进」。
   .rows .r.hot 在 components.css 里取 --coral（= --accent-deep）；本 deck 的 hot 语汇
   一律是 --accent，这里同权重覆写（两边都是 0,4,0，本表写在 components.css 之后 ⇒ 本表胜）。*/
.nrow .r{padding:44px 0;align-items:flex-start;}
.nrow .r .n{font-size:24px;line-height:1.3;}
.nrow .r .k{font-size:27px;line-height:1.3;width:196px;}
.nrow .r .ex{display:block;font:500 14px/1.5 var(--f-mono);letter-spacing:.06em;color:var(--ink-3);}
.nrow .r .sol{display:block;margin-top:9px;font:400 20px/1.35 var(--f-cn);color:var(--ink-2);}
.nrow .r .sol b{font-weight:700;color:var(--ink);}
.nrow .r .sol i{display:inline-block;margin-left:12px;font-style:normal;
  font:400 15px/1.35 var(--f-cn);color:var(--ink-3);}
.nrow .r.hot .k,.nrow .r.hot .n{color:var(--accent);}
.nrow .r.hot .sol b{color:var(--accent);}
/* ══ deck 级运动语言 · 五个运动原语（2026-08-21 动效全覆盖轮）════════════════
   P10 的常驻动效是这套语言的母本，本轮升格为 deck 级系统：十一页共用同一批
   keyframes / 类，不再一页一套私有动画。原语与语义一一对应（改页前先对表）：
     ① .mo-packet  能量包 —— 宽 stroke 低透明 dash 段沿路径漂移。只挂实线主数据流，
        方向必须与箭头一致（路径按流向写 d，--mo-off 取负 = 顺路径跑）。它是**新增
        的纯装饰件**，不属于页面几何 ⇒ 静态语域直接 display:none。
     ② .mo-drift   虚线漂移 —— 事件 / 控制 / 参考线的 dash 慢爬，比包慢一档。
        载体是页面真线 ⇒ 静态语域只 animation:none，线本身照画。
     ③ .mo-pulse   脉冲 —— 命中 / 事件标（✕、事件 pin、step 徽标）opacity 明暗，错峰 delay。
        --mo-hi / --mo-lo 可调：载体自带 opacity 时必须把 --mo-hi 设成它的静态值，
        否则动画会把 opacity 顶成 1（animation 压过 inline style，一亮就穿帮）。
     ④ .mo-breathe hot 件呼吸 —— scale ≤1.03，每页至多一处，落在该页唯一 hot 件上；
        伴件 .mo-halo 是向外扩散的光晕（100% 帧 opacity:0 ⇒ 静态语域零痕迹）。
     ⑤ .mo-cycle   闭环绕行 —— 环 / 回路上的 dash 永续绕圈（P10 两道防御环 /
        P8 AEC 参考环 / P2 反馈弧）。载体是真几何时同 ②；载体是新增装饰包时再挂 .mo-ghost。
   纪律（硬红线，四条）：
     · 每条 keyframes 的 100% 帧 = 静态原图：dash 位移必须走完整周期（offset 是
       dasharray 周期的整数倍）、scale 回 1、opacity 回静态值、halo 回 0。遮挡扫描器与
       qa 都注入 animation-duration:0s + animation-delay:0s，浏览器把元素直接钉在
       100% 帧上 —— 这一条保证「动效关掉 = 原图逐像素」，几何零漂移。
     · 动效元素不携带文字：文字要么在动效件之外，要么单拆一枚静态 text。
     · prefers-reduced-motion 与 print 全关（装饰件摘掉、真几何件停帧）。
     · 非当前页一律 animation-play-state:paused —— 22 页动画同时跑没有意义。 */
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
/* ── P10 双层防御环 · 常驻环境动效（2026-08-21 · 本轮代码归一到上面的原语）──────
   Colin：「很牛逼但不炫酷，想让它整体动起来」。本页是运动语言的母本；本轮把私有
   keyframes（p10Ring / p10Beam / p10X / p10Agent …）整批换成 deck 级原语类，
   duration / offset / 错峰 delay 逐个原值搬运 ⇒ 视觉零变化，代码归一。
   页级硬约束（改这块之前先读）：两道防御环 **不做 transform 旋转**，只让虚线 dash
   绕圈爬（.mo-cycle）。原因是硬约束不是审美：两环的左侧缺口是「只有目标人声进得来」
   这句话的图形依据，几何一转、缺口就甩走了，整页的论证当场失效。改爬 dash 后观感等价
   （环本就是虚线），语义零损失 —— 外环 26s 走完一整圈周长 867（dash「9 8」×51）、
   内环 18s 反向走完一圈 540（dash「8 7」×36），就是「26s / 18s 自转」。
   智能体圆片 / 光晕走 .mo-breathe 默认的 fill-box 中心：整圆的 fill-box 中心 =
   圆心 (300,196)，与旧版写死的 view-box 原点逐像素等价（带缺口的弧才需要写死原点，
   那两条本来就不缩放）。 */
/* ── Call Agent 章 · 差异三行表（P16）─────────────────────────────────────
   table.mini 的 td 上下 padding 是 11px（1 表头 + 2 行 = 130，见 P3），三行就顶到 176、
   越过 rule(850) 这条收口线。这里只把上下 padding 收到 9px（字号与行高一字不动）：
   1 表头 + 3 行 = 166，落回 168 的盒里。改行数必须重算这一笔。 */
.ca-diff tbody td{padding:9px 16px 9px 0;font-size:19px;}
/* ── R1 实拍图卡（P19 · 2026-08-21「完整显示」轮重排）──────────────────────
   Colin：「图片展示不全，比例看看」。旧版是 620 宽 × 296 高的横图窗（≈2.1:1），
   对 1000×750（4:3）的实拍做 cover 裁切 —— cover 由**宽**定标（scale=.62），
   纵向只看得见 750 里的 477 行：4G 那张的天线顶端、两张的板底排线全被切在窗外。
   「单芯片一体化 + 4G 天线」这句话的图形证据，被图窗自己裁掉了。
   本轮改法（文案一个字不动，只重排版面）：
     · 卡改横向：**图窗占满卡高**（380 × 510），规格右移进 440 宽的右栏。
       图窗高宽比 1.34 > 原片的 0.75 ⇒ cover 改由**高**定标（scale = 510/750 = .68），
       整张原片的 750 行全在窗内、只裁掉左右两侧的空黑边：
       两块板的四边一格不缺，板子还比旧版大一档（旧 .62 → 板宽 273px；今 .68 → 300px）。
     · 横向可见的原片宽 = 窗宽 / .68 = 559px（居中 ⇒ 原片 x220–779），
       两块板的实测墨迹都在 x278–719 内，左右各余 58px 以上。**改窗宽必须重算这一条。**
     · 「共同能力」竖排 chip 栏让位给图卡，改横排 chips 落到收口线之下的页脚带
       （P7「04 · TEN 生态」已有同款破例先例，经 Fable 终审）。
     · 角标 / 图注从图上撤到右栏底部的图注行 —— 4G 那张的天线顶端就落在图窗 y≈40，
       角标压在原位就是直接盖住产品（「不许压产品」优先于「角标压在图上更漂亮」）。
   资产跨 deck 引用 robot26 目录下的两张 webp（1000×750 实拍），不复制文件
   —— bake-archive 的内联正则按资产路径全匹配，跨 deck 引用照吃不误。
   ⚠ 注释里绝不能写出完整的资产路径字面量：那条正则连 CSS 注释一起扫，
   会把带通配符的示例路径当成真资产去找，报一条 miss。 */
.pp .sh.r1-card{overflow:hidden;}                     /* .pp .sh{overflow:visible} 会让图角戳出 20px 圆角 */
.r1-card{display:flex;flex-direction:row;}
.r1-shot{position:relative;flex:none;width:380px;align-self:stretch;overflow:hidden;
  background:#0a0c14;border-right:1px solid var(--hair);}
/* 图必须 width/height 100% + object-fit —— 放大 img 去逼近墨迹会让它的 rect 冲出卡底，
   qa 的 cardspill（只读 rect、不读 overflow:hidden）稳报一条假命中。 */
.r1-shot img{width:100%;height:100%;display:block;object-fit:cover;object-position:center;}
.r1-body{flex:1;display:flex;flex-direction:column;padding:32px 32px 28px;}
/* 主文块垂直居中、图注行钉在卡底：两张卡的规格行因此对齐同一条视觉中线 */
.r1-main{flex:1;display:flex;flex-direction:column;justify-content:center;}
.r1-cap{flex:none;padding-top:14px;border-top:1px solid var(--hair);
  display:flex;align-items:baseline;gap:14px;}
.r1-cap .bdg{flex:none;font:600 12px/1.5 var(--f-mono);letter-spacing:.16em;color:var(--ink-3);}
.r1-cap .cap{font:400 14px/1.5 var(--f-cn);color:var(--ink-3);}
/* 浅色主题下的「暗媒体卡」惯例：深底实拍图直接压在浅版面上会掉进洞里 ——
   给一圈发丝内描边把图从纸面上拎起来（实拍不翻色，只压一档饱和度免得抢页面主色）。 */
html:not([data-theme="dark"]) .r1-shot{box-shadow:inset 0 0 0 1px rgba(17,17,17,.12);}
html:not([data-theme="dark"]) .r1-shot img{filter:saturate(.92) contrast(1.03);}
/* ── 全屏视频页（P20 无人机秀 · robot26 #24 同款）─────────────────────────
   .sh.vid 是唯一一只贴 0,0 的满幅盒（其余 .sh 都在 120 版心里）。整幅 overflow:hidden：
   1280×720 与 1920×1080 同 16:9，cover 理论上不裁一格，但浏览器的取整会差半像素，
   裁掉半像素总比让它顶出舞台强。
   video 一律 background:#000 —— poster 还没解码的那一帧，浅色主题下会露出纸白底，
   在一支夜景片子前面闪一下白，比黑场难看得多。
   ⚠ 不要给 video 加 controls 属性（Blink 控制条在 transform:scale 下错位，robot26 实锤）；
     悬停呼出由 build() 里的内联脚本挂，静置态必须干净。 */
.pp .sh.vid{overflow:hidden;}
/* 分步 cue：零宽零高，只为给 deck.js 的 maxStep 提供一枚 [data-step] 元素。
   它自己会被 motion.css 的「裸容器 step0 → opacity:0」兜底规则摁成透明 —— 正合适，
   本来就不该看见。**绝不要把 data-step 挂回 .sh.vid**（那条兜底规则会连 poster 一起摁没，
   就是 2026-08-21「P19 之后多了一个空页面」的根因）。 */
.vid-cue{position:absolute;left:0;top:0;width:0;height:0;overflow:hidden;pointer-events:none;}
.sh.vid video{display:block;width:100%;height:100%;object-fit:cover;background:#000;
  border-radius:0;outline:0;}
/* 页码 sig 落在片子的右上角：这支片子的右上角是纯黑（实测亮度 1/255），
   浅色主题的 --sig-ink 是 rgba(17,17,17,.30) ⇒ 黑压黑，页码等于没有。
   两个主题都改成半透明白（robot26 #24 同款处理）。选择器用 :has(~ .sh.vid) 从兄弟
   反查视频页 —— 不写 [data-p="20"]，页序一动就失效（本 deck 半个月里已经重排三次了）。
   :has() 的浏览器门槛（Chrome 105）低于本 deck 已经在用的 color-mix()（Chrome 111），
   不构成新的兼容负担。 */
.pp .sig:has(~ .sh.vid){color:rgba(255,255,255,.55);}
/* P20 静态角标 kicker（2026-08-23 采纳项 E ②）：整页只有一支片子，这是唯一一行说明。
   反白压左上角 —— 右上角归页码 sig，画面主体在中下部，hover 才挂上的原生控制条在底部，
   三者各占一角互不打架。`.sh.vid-kick`（0,2,0）压过 `.kk{color:var(--accent)}`（0,1,0）。
   一圈软黑投影：片子的角上万一飘过亮部，字仍旧读得出（poster 那一帧角上是纯黑）。
   **它是静态文字件**：不挂 data-step、不挂任何 mo-* 类 —— 不进运动件名册，
   也躲开 motion.css「裸容器 step0 → opacity:0」的兜底规则（P20 空页事故的根因）。 */
.sh.vid-kick{color:rgba(255,255,255,.74);text-shadow:0 1px 10px rgba(0,0,0,.55);}
/* ── OpenAI × Agora logo 锁定版（P22 末页）───────────────────────────────
   双源同构图，走 convoai-info 的 .hero-art / .eco-art 同一套「CSS 控显隐」机制，
   不用 robot26 的 data-*-src 换源脚本：抽屉 iframe 里宿主切主题只改 html[data-theme]，
   CSS 机制天然跟随，脚本机制还得在 iframe 里再跑一遍换源代码。
   原片 1100×748 四周是大片透明（实测 alpha bbox = x168–929 / y47–527 → 墨迹占宽 69.18%、
   占高 64.17%）。这里**不**做「盒按墨迹开 + img 放大负偏移裁掉透明边」那一套：
   放大后 img 的 getBoundingClientRect 会溢出 .sh 盒 168px，而 occlusion-scan 的
   TEXT-x-SPILL 只读 rect、不读 overflow:hidden ⇒ 稳报一条假命中。
   改法是 .sh 盒 = 原片整幅，img 原样铺满（零定位、零裁切），墨迹落点由盒位倒推：
     盒宽 838 ⇒ 墨迹宽 580 · 左边距 128 · 上边距 36（盒 570 高）。改盒宽必须同步重算 left/top。
   代价是盒底拖一截透明尾巴，在 y 上与下方大字盒重叠 —— 透明就是透明，且 logo 盒在
   文档序上早于大字盒 ⇒ 字画在图之上，扫描器的画序规则判它可读，不算遮盖。 */
.lock img{display:block;width:100%;height:auto;}
.lock img.dk{display:none;}
html[data-theme="dark"] .lock img.lt{display:none;}
html[data-theme="dark"] .lock img.dk{display:block;}
@media print{.r1-shot{box-shadow:none;}}
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
def sh(cls, style, body, step=None, sid=None):
    a = ' data-sid="%s"' % sid if sid else ""
    a += ' data-step="%d"' % step if step is not None else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (cls, a, style, body)

def rule(y, x=120, w=1680, i=1):
    """分区之间的 1px 细线（高度 1px → 扫描器不当它是覆盖块）"""
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:%dpx;height:1px;--i:%d" % (x, y, w, i), "")

def vrule(x, y, h, i=1):
    """竖向 1px 细线（分栏用）"""
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:1px;height:%dpx;--i:%d" % (x, y, h, i), "")

def lab(x, y, txt, w=680, col=None, i=0, step=None):
    """mono 小节标：「01 · SIGNAL PATH」"""
    c = ";color:%s" % col if col else ""
    return sh("flow seclab", "left:%dpx;top:%dpx;width:%dpx;height:20px;--i:%d%s" % (x, y, w, i, c),
              txt, step=step)

def figbox(x, y, w, vbw, vbh, inner, cls="flow", i=0, step=None):
    """SVG 装盒：.sh 高度按 viewBox 等比算死，svg 一律 width:100%;height:auto"""
    h = round(w * vbh / vbw)
    return sh(cls, "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (x, y, w, h, i),
              '<div class="fig"><svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg></div>'
              % (vbw, vbh, inner), step=step)

def head(kicker, title, kw=1680):
    """每页统一的页眉：kicker y92 / 标题 y148 起（家族版式纪律）"""
    return (sh("flow kk", "left:120px;top:92px;width:%dpx;height:28px" % kw, kicker)
            + sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", title))

def land(txt, y=988, x=120, w=1680, i=6):
    return sh("flow", "left:%dpx;top:%dpx;width:%dpx;height:70px;--i:%d" % (x, y, w, i),
              '<div class="land">%s</div>' % txt)

def rail(txt, y=988):
    """英文 mono 收口轨（没有 land 的页用它压住页脚基线）"""
    return sh("flow mono-sm", "left:120px;top:%dpx;width:1680px;height:24px;--i:7" % y, txt)


def src(txt, y=1015, x=120, w=1680, i=7, align=None):
    """SOURCE ledger 行（2026-08-23 采纳项 C · 与 convoai-info 的 src() 同签名同类名）。
       全家族统一四段：SOURCE · <来源> · <样本或时间窗> · 事实截止 2026.08
       缺哪段就少哪段（不编），缺口记在交付报告里等 Colin 补。
       与 rail()/.mono-sm 分成两枚类：.src 是「出处」，G 轮只提 .src 与 .sig
       这两枚投影小字的字号与色阶 —— 别再把普通元信息行混挂到 .src 上。"""
    a = ";text-align:%s" % align if align else ""
    return sh("flow src", "left:%dpx;top:%dpx;width:%dpx;height:24px;--i:%d%s" % (x, y, w, i, a), txt)


# ── SOURCE ledger 常量（同一份出处出现在多页时只写一次，防两页各自漂移）────────
#   P5 三件极致 / P11 弱网：同一套「引擎公开口径 · 典型值」
_SRC_TYP = "SOURCE · 声网官网 / 引擎发版说明 公开口径 · 典型值 · 事实截止 2026.08"

# ── SVG 小件 ────────────────────────────────────────────────────────────────
def ah_r(x, y, col, s=9):
    """向右箭头头（fill 走内联 style）"""
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

def hline(x1, x2, y, col="var(--hair-strong)", w=2, i=1, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d H%d" '
            'stroke="%s" stroke-width="%s" fill="none"%s/>' % (abs(x2 - x1), i, x1, y, x2, col, w, d))

def vline(x, y1, y2, col="var(--hair-strong)", w=2, i=1, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d V%d" '
            'stroke="%s" stroke-width="%s" fill="none"%s/>' % (abs(y2 - y1), i, x, y1, y2, col, w, d))

def dline(d, col="var(--hair-strong)", w=2, i=1, dash="7 7", cls="", sty=""):
    """虚线：不能走 .dw —— motion.css 的 .dw{stroke-dasharray:var(--len)} 会把 dasharray
       属性整条压掉，虚线会渲染成实线。这里改挂 .pop（只动 opacity/transform），破折保留。
       cls / sty：额外类与额外内联变量（挂运动原语用：.mo-drift + --mo-off/--mo-dur）。"""
    return ('<path class="pop%s" style="--i:%d%s" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-dasharray="%s"/>'
            % ((" " + cls) if cls else "", i, (";" + sty) if sty else "", d, col, w, dash))

# ── 运动原语 ① 能量包（deck 级）────────────────────────────────────────────
#   压在实线之下的一段粗软 stroke，沿路径漂移。dasharray = 「包长 seg + 间隔 ln」，
#   --mo-off 走完一个整周期 ⇒ 100% 帧与 0% 帧逐像素相同（静态原图纪律）。
#   ln 传路径长度（近似即可，只决定「同一时刻路上最多一枚包」）。
#   rev=True：包逆着 d 的书写方向跑（用于双向线的回程；正 offset）。
def packet(d, ln, col=None, w=11, seg=24, dur="1.8s", op=".3", i=2, rev=False, delay=None,
           cls="", cap="round"):
    per = seg + int(ln)
    v = "--mo-off:%d;--mo-dur:%s" % (per if rev else -per, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<path class="pop mo-packet%s" style="--i:%d;%s" d="%s" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-opacity="%s" stroke-linecap="%s" stroke-dasharray="%d %d"/>'
            % ((" " + cls) if cls else "", i, v, d, col or AC, w, op, cap, seg, int(ln)))

def box(x, y, w, h, r=4, hot=False, dashed=False, i=0, cls="", sty=""):
    """家族图框：常态走 class="box"（fill card-bg / stroke hair），高亮走 accent 描边。
       cls / sty：挂运动原语用（hot 盒的 .mo-breathe）。"""
    d = ' stroke-dasharray="7 6"' if dashed else ""
    c = (" " + cls) if cls else ""
    v = (";" + sty) if sty else ""
    if hot:
        return ('<rect class="pop%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
                'fill="none" stroke="var(--accent)" stroke-width="2.5"%s/>' % (c, i, v, x, y, w, h, r, d))
    return ('<rect class="pop box%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'stroke-width="1.4"%s/>' % (c, i, v, x, y, w, h, r, d))

def halo_rect(x, y, w, h, r=8, col=None, sc="1.06", op=".34", dur="3.6s", delay=None):
    """呼吸光晕（原语 ④ 的伴件 · 矩形版）：贴着 hot 盒向外扩散再消失。
       100% 帧 opacity:0 ⇒ 静态语域零痕迹（纸面上不会留一枚谜之边框）。"""
    v = "--mo-sc:%s;--mo-op:%s;--mo-dur:%s" % (sc, op, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<rect class="mo-halo" style="%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'fill="none" stroke="%s" stroke-width="2.5" opacity="0"/>'
            % (v, x, y, w, h, r, col or AC))

def txt(x, y, s, cls="txt", size=None, anchor=None, col=None, weight=None, i=None,
        mono=False, ls=None, sty=None):
    st = []
    if sty:    st.append(sty)          # 运动原语的内联变量（--mo-dur / --mo-del …）
    if size:   st.append("font-size:%dpx" % size)
    if col:    st.append("fill:%s" % col)
    if weight: st.append("font-weight:%d" % weight)
    # mono：.lbl 是唯一自带 mono 的类，但它带 text-transform:uppercase（会把「Token 签名」
    # 烧成「TOKEN 签名」）。要 mono 又要保留大小写时走这一路。
    if mono:   st.append("font-family:var(--f-mono)")
    if ls is not None: st.append("letter-spacing:%s" % ls)
    a = ' text-anchor="%s"' % anchor if anchor else ""
    g = ' class="%s"' % cls if cls else ""
    sty = ' style="%s"' % ";".join(st) if st else ""
    return '<text%s x="%d" y="%d"%s%s>%s</text>' % (g, x, y, a, sty, s)

# 波形条（P4 活动带 / P9 双轨波形共用）：定高序列，形态稳定、双主题都读得出。
# hs 可覆盖（必须是写死的常量表，禁止 random / Date —— 两次构建必须逐字节一致）：
# P4 与 P9 各用一组，否则两页的波形轮廓一模一样，读者会以为是同一张图复用。
def _bars(x0, n, cy, col, seed=0, gap=17, w=8, op=None, hs=None):
    hs = hs or [30, 54, 16, 66, 38, 22, 58, 34, 46, 18, 50, 26, 40, 14, 62, 30, 44, 20, 56, 36]
    o = []
    for i in range(n):
        h = hs[(i + seed) % len(hs)]
        o.append('<rect class="pop" style="--i:%d;fill:%s%s" x="%d" y="%d" width="%d" height="%d" rx="%d"/>'
                 % (1 + i % 4, col, (";opacity:%s" % op) if op else "", x0 + i * gap, cy - h // 2, w, h, w // 2))
    return "".join(o)

PAGES = []          # (board, steps, body_html)
def page(board, body, steps=0):
    PAGES.append((board, steps, body))

AC = "var(--accent)"
AD = "var(--accent-deep)"
HS = "var(--hair-strong)"

# ── deck 级线型系统（2026-08-20 三轮「图形升维」· P8 为标杆）────────────────
#   实线 accent        = 音频 / 主数据流
#   虚线 hair-strong   = 事件 / 控制
#   点线 accent-deep   = 参考 / 反馈
#   粗线 accent-deep 5 = 快路径 / 关键通路
#   每张图底部一行 mono 迷你图例，只列该页真正用到的线型（画真线样，不用字符画）。
def lg_solid(x, y, col=AC, w=2.5, i=9):
    return hline(x, x + 40, y, col, w, i)
def lg_dash(x, y, col=HS, w=2, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="6 5")
def lg_dot(x, y, col=AD, w=2.4, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="2 6")
def lg_fast(x, y, col=AD, w=5, i=9):
    return hline(x, x + 40, y, col, w, i)
def lg_dead(x, y, col=HS, w=2, i=9):
    """静默通道（P3 单工的下行方向）：压暗虚线 + 灰箭头 —— 线在，包永远不来。
       与「事件 / 控制」同为 hair-strong 虚线，差别只有 opacity 与那支灰箭头，所以图例样线
       必须逐参数照抄页内真线（_duplex_fig 的 ch_dead：dash 5 5 / opacity .5 / ah_l ink-3），
       否则读者会把这两根灰虚线读成同一种线。箭头是全图例唯一一支 —— 本项的语义本身
       就是「方向」，没有箭头就只剩「一根更淡的虚线」，读不出「哪一头永远不来」。"""
    return (dline("M%d %d H%d" % (x + 40, y, x + 10), col, w, i, dash="5 5", sty="opacity:.5")
            + ah_l(x, y, "var(--ink-3)", 7))
_LGK = {"solid": lg_solid, "dash": lg_dash, "dot": lg_dot, "fast": lg_fast, "dead": lg_dead}

def step_badge(x, y, n, r=16, i=2, halo=None):
    """握手序号徽标（P14 接入架构）：不透明圆片 + accent 序号，压在连线上、线从徽标底下穿过。
       fill 必须是 --card-bg-2（#fffffe / #131320）——  --card-bg 是 72% 透明，
       半透明徽标会让连线从数字里透出来，读成「数字被划掉」。"""
    ring = ('<circle class="mo-halo" style="--mo-sc:2;--mo-op:.5;--mo-dur:3.6s;--mo-del:%s" '
            'cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="2.5" opacity="0"/>'
            % (halo, x, y, r, AC)) if halo else ""
    return (ring
            + '<circle class="pop" style="--i:%d;fill:var(--card-bg-2)" cx="%d" cy="%d" r="%d" '
              'stroke="%s" stroke-width="2"/>' % (i, x, y, r, AC)
            + txt(x, y + 7, str(n), "ttl", size=20, anchor="middle", col=AC, weight=700))
def legend(x, y, items, i=9, gap=54):
    """图例行：items = [(kind, 标签)] / [(kind, 标签, 线宽)] / [(kind, 标签, 线宽, 颜色)]；
       kind ∈ solid / dash / dot / fast / fill / swap。
       第三项给线宽：图例样线必须与页内真线同粗，否则「粗一档」在图例里读不出来。
       第四项给颜色：同一线型靠「粗细 + 灰度」分主次时（P12 加重 / 弱化），图例必须跟着降级。
       fill = 面色块样本（P11 缓存余量）；swap = ⇄ 换装小件（P13）——都不是「线型」，
       但同屏出现就必须进图例，否则读者要自己猜。
       步进按标签字数估宽（CJK 14px/字），够松，不会互相压。"""
    o, cx = [], x
    for it in items:
        kind, label = it[0], it[1]
        w = it[2] if len(it) > 2 else None
        col = it[3] if len(it) > 3 else None
        if kind == "fill":
            o.append('<rect class="pop" style="--i:%d;fill:%s;opacity:.25" x="%d" y="%d" '
                     'width="40" height="13" rx="3"/>' % (i, col or AC, cx, y - 6))
        elif kind == "swap":
            o.append(swap_mark(cx, y, i=i))
        else:
            kw = {"i": i}
            if w is not None: kw["w"] = w
            if col is not None: kw["col"] = col
            o.append(_LGK[kind](cx, y, **kw))
        o.append(txt(cx + 50, y + 5, label, "sm", size=14, i=i))
        cx += 50 + int(len(label) * 13.2) + gap
    return "".join(o)

def swap_mark(x, y, col="var(--ink-3)", i=2, w=34, sty=None):
    """⇄ 换装小件（P13 开放编排）：两支对开的细小箭头，灰度 + 小号 —— 与「插入」主线不同重量级，
       一眼读成注记而不是流向。画真箭头，不用字符 ⇄（字体缺字会掉成豆腐块）。"""
    g = "".join([
        hline(x, x + w - 8, y - 5, col, 1.3, i), ah_r(x + w, y - 5, col, 5),
        hline(x + w, x + 8, y + 5, col, 1.3, i), ah_l(x, y + 5, col, 5)])
    # sty 给运动原语 ③（P13 槽上的 ⇄ 极轻脉冲）：整组一起呼吸，不逐条错峰
    return ('<g class="mo-pulse" style="%s">%s</g>' % (sty, g)) if sty else g

# ═══ P1 · 封面（title 板）══════════════════════════════════════════════════
#   2026-08-23 Colin 亲自定主标：**「对话即交互。」**（四字 + 句号 · 家族标题惯例）。
#   三处连动，其余（脚注 / 背景板 / accent 短棒 / sub 的 y）一个像素不碰：
#     ① kicker 末段「产品介绍」→「DEEP DIVE · 深入讲解」：本 deck 早已不是产品介绍
#        （22 页里 11 张机理图 + 一张运行时大图），封面必须先把定位说对。
#     ② 主标 96px 双行 →  **200px 单行**：四个字要撑住整张封面，就得走家族最大号
#        （全 deck 此前最大字号是 P5 的 132px 数字；封面主标越过它才立得住）。
#        版式账：6 个全角字 × 200 − letter-spacing(-.03em × 200 × 6) ≈ 1164px，
#        盒宽 1500 仍余 336px；行盒 200×1.1 = 220，盒顶 280 ⇒ 墨迹约 290–490，
#        与 accent 短棒（y572）留 82px —— 与旧版双行（墨迹收在 500）的呼吸等价。
#     ③ 原主标「2 行代码，构建自然流畅的对话体验。」整句退场 ——
#        「2 行代码」的论点在 P14 接入页有自己的位置（三方协同 + 握手序号图），
#        不需要挪过来，挪过来反而变成同一论点讲两遍。
#   副题保留现句：它从「补充说明」升格为主标的**支撑句**（低延时 / 可打断 / 听得清
#   正好对上 P5 三件极致的 650 / 340 / 95%，也就是新的 6–10 章）。
page("title", "".join([
    sh("flow kk", "left:120px;top:200px;width:1500px;height:28px",
       "AGORA · CONVERSATIONAL AI ENGINE · DEEP DIVE · 深入讲解"),
    # ⚠ 行高不能照抄家族的 1.1：CJK 回退字体在 200px 下的**内容高**（ascent+descent）实测
    #   223px > 行盒 220px ⇒ 半行距变成 −1.5，文字盒从 .sh 上沿探出 2px，被 .ink 的
    #   液态扫过 mask 裁掉一线（1280×720 档的遮挡扫描当场报 CLIPPED，1920 档卡在阈值边上）。
    #   改 1.16（行盒 232 > 223，半行距 +4.5）并把盒长到 236、顶回抬 4 —— 墨迹位置只挪 2.5px，
    #   两档分辨率都不再有裁切。**改字号必须重算这一笔**（内容高 ≈ 1.115em）。
    sh("ink", "left:120px;top:276px;width:1500px;height:236px;"
       "font:700 200px/1.16 var(--f-cn);letter-spacing:-.03em;color:var(--ink)",
       "对话即<strong style='color:var(--accent)'>交互</strong>。"),
    sh("spread", "left:120px;top:572px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow sub", "left:120px;top:624px;width:1500px;height:48px;--i:4",
       "让人和智能体像真人一样自然对话——低延时、可打断、听得清。"),
    sh("flow mono-sm", "left:120px;top:930px;width:1400px;height:24px;--i:6",
       "仅供方案交流参考 · 事实截止 2026.08"),
]))

# ═══ P2 · 实时决策 ·「对话是一个实时决策的过程」═════════════════════════════
#   2026-08-20 三轮「图形升维」：4 卡 + 弱双轨 → 一张「决策环」。
#   四步不再并排罗列，而是首尾相接成环：听 → 理解 → 判断 → 表达 → 点线反馈弧绕回听。
#   那条点线弧是本页灵魂（「表达时仍在听」）—— 有它才是环，没它只是四段流程。
#   与 P4 的直线泳道互补：P2 讲「因果闭环」，P4 讲「同一时间轴上并行」，不重复画横向轨。
#   hot 件唯一 = 「判断」节点（大一号 + accent 描边）：全页的因在这里。
_MOVES4 = [   # (环上动作, 序号, 原卡标题, 原卡正文) —— 标题与正文与旧版一字不差
    ("听",   "01", "听清 · 认人 · 懂内容",       "分离目标人声、识别说话人，同时理解在说什么"),
    ("理解", "02", "带入对象、场景与情绪",       "结合上下文理解言外之意，而不只是逐字转写"),
    ("判断", "03", "持续判断：继续听，还是开口", "实时权衡时机，不必等一句话彻底说完"),
    ("表达 · 控制节奏", "04", "边说边听，灵活调整节奏", "表达的同时仍在倾听，随时被打断、随时接上"),
]
# 环上四个节点的盒（左上 → 右上 → 右下 → 左下，顺时针）；判断为 hot，大一号
_P2N = [(380, 20, 400, 134), (1000, 20, 400, 134), (980, 250, 440, 154), (380, 260, 400, 134)]
def _loop_fig():
    o = []
    for k, (act, no, ttl, body) in enumerate(_MOVES4):
        x, y, w, h = _P2N[k]
        hot = (k == 2)
        # 运动原语 ④：全页唯一 hot 件（判断节点）呼吸 + 光晕 —— 「因」在这里一直在跳
        if hot:
            o.append(halo_rect(x, y, w, h, 10, sc="1.05", op=".3", dur="3.6s"))
        o.append(box(x, y, w, h, 10, hot=hot, i=k + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.6s" if hot else ""))
        o.append(txt(x + 26, y + (38 if hot else 34), "%s · %s" % (no, act), "sm",
                     size=14, col=AC, mono=True, ls=".14em"))
        o.append(txt(x + 26, y + (80 if hot else 70), ttl, "ttl",
                     size=25 if hot else 23, col=AC if hot else None))
        o.append(txt(x + 26, y + (118 if hot else 104), body, "sm", size=17 if hot else 16))
    # ── 三条实线主流程边（环的正向）：每条都带标注，说清「这一步交出去的是什么」──
    o.append(packet("M780 87 H988", 208, seg=22, dur="2.6s", i=2))
    o.append(hline(780, 988, 87, AC, 2.5, 2)); o.append(ah_r(1000, 87, AC))
    o.append(txt(890, 69, "对象 · 场景 · 情绪", "sm", size=16, anchor="middle"))
    o.append(packet("M1200 154 V238", 84, seg=22, dur="1.2s", i=3))
    o.append(vline(1200, 154, 238, AC, 2.5, 3)); o.append(ah_d(1200, 250, AC))
    o.append(txt(1222, 208, "何时开口", "sm", size=16))
    o.append(packet("M980 327 H792", 188, seg=22, dur="2.4s", i=4))
    o.append(hline(980, 792, 327, AC, 2.5, 4)); o.append(ah_l(780, 327, AC))
    o.append(txt(880, 309, "开口表达", "sm", size=16, anchor="middle"))
    # ── 闭环关键边：点线反馈弧，从「表达」绕回「听清」——本页的灵魂 ──
    #   3px（比实线细一档但看得见）+ 标签压在弯道肘部右侧的月牙里，读者一眼知道它注解谁
    _P2ARC = "M376 327 C 240 327, 170 300, 170 207 C 170 114, 240 87, 360 87"
    o.append(packet(_P2ARC, 330, seg=26, col=AD, w=9, op=".3", dur="4s", i=5, cls="mo-cycle"))
    o.append(dline(_P2ARC, AD, 3, 5, dash="3 8"))
    o.append(ah_r(372, 87, AD, 7))
    o.append(txt(190, 190, "表达时仍在听", "ttl", size=18, col=AD, weight=700))
    o.append(txt(190, 216, "随时被打断、随时接上", "sm", size=15, col=AD))
    # ── 环心：这四件事不是先后，是同一刻 ──
    o.append(txt(900, 196, "同一时刻 · 并行进行", "ttl", size=20, anchor="middle"))
    o.append(txt(900, 224, "持续在听 · 同时在说", "sm", size=15, anchor="middle", mono=True))
    # ── 图例（只列本页用到的两种线型）──
    o.append(legend(0, 440, [("solid", "主数据流"), ("dot", "参考 / 反馈")]))
    return "".join(o)
# 回合制反例条：线性三段，与环形主图形成对照（note 语域 —— 灰、虚线、小一号）
_P2ANTI = "".join(
    [txt(2, 40, "回合制", "sm", size=14, col="var(--ink-3)", mono=True, ls=".16em")]
    + [x for k, s in enumerate(["听完", "想", "说"]) for x in (
        box(120 + k * 150, 16, 110, 40, 20, dashed=True, i=k + 1),
        txt(175 + k * 150, 43, s, "sm", size=17, anchor="middle", col="var(--ink-3)"))]
    + [dline("M%d 36 H%d" % (240 + k * 150, 256 + k * 150), HS, 2, k + 2, dash="5 5")
       for k in range(0, 2)]
    + [ah_r(268 + k * 150, 36, "var(--ink-3)", 7) for k in range(0, 2)]
    + [txt(620, 43, "听完再回答 ✕", "sm", size=17, col="var(--ink-3)")])
page("content", "".join([
    head("REAL-TIME DECISION · 边听边说", "对话，是一个<strong>实时决策</strong>的过程。"),
    lab(120, 236, "01 · FOUR MOVES · 同一时刻发生"),
    figbox(120, 272, 1680, 1680, 470, _loop_fig(), i=1),
    lab(120, 756, "02 · SAME MOMENT · 边说边听", i=6),
    figbox(120, 788, 900, 900, 58, _P2ANTI, i=7),
    rule(850),
    land("自然对话不是“听完再回答”，而是边说边听、持续判断——这正是引擎要还原的能力。"),
]))

# ═══ P3 · 双工三模式 ·「一次对话，线路先分三种」════════════════════════════
#   01 三列等宽卡（120 / 700 / 1280 · w520 —— 与 P5「三件极致」同一栅格）：
#      英文小标 + 模式名 + 极简时序小图 + 机理一句 + 实例一句（末列 .card-c.on = 引擎所在）
#   02 table.mini 两行差异（话轮归属 / 能否插话），末列走 accent
def _duplex_fig(mode):
    """A / B 左右分列 · 时间竖直向下（vb 460×140）
       2026-08-21「对话版」重排（Colin：「对话 AB 上下关系，左右是不是更贴切？试试看」）：
       旧版是 A/B 上下双轨 + 时间横向 —— 「谁在说」和「什么时候说」压在同一根横轴上，
       读者得先把横轴认成时间才看得懂。新版换成聊天记录的心智模型：
       消息左右分列（A 在左 / B 在右）、时间往下走，一眼就知道哪边在说、谁先谁后。
         单工   左列一整条连续块（单向出）／右列永远空 ＋ 一支 A → B 的横箭头
         半双工 左右交替块（像对话气泡），轮次之间横着一道「切换」闸；
                B 在 A 讲话中途尝试出声 → 被闸拦住的 ✕
         全双工 左右块在同一竖直区间重叠（重叠区高亮），插话点画快路径粗箭头（B 横插进 A）
       最左侧是时间轴：竖线 + 无字刻度 + 末端箭头 —— 本页没有已核定的时间数字，
       只给节奏感，绝不发明数字（与旧版同一条纪律）。
       版式账：图窗从 116 长到 134 的 18px，全部由卡内边距腾出来
       （padding 26→20 / fig margin 16→12 / mech margin 16→14 / ex padding 14→12 = 20px，
       再加最紧那张卡原有的 17px 余量）—— 卡高 386 与其后所有元素的 y 全部不动。

       ── 2026-08-23「动效即语义」轮（Colin 点名 P3 要动）────────────────────────
       本页此前不在运动件名册里。它是全 deck 唯一一页「运动模式本身就是定义」的图：
       三种双工的差别，说到底就是**两个方向的包什么时候在途**。所以本轮加的不是装饰，
       是论证 —— 两列之间那 76px 空档（x192–268）做成两条方向通道，包跑在通道上：
         · 单工 SIMPLEX   A→B 通道恒有包；B→A 通道画出来但压暗成静默虚线，**永远无包**
         · 半双工 HALF    两条通道都活，但**严格互斥**：包错峰出现，任何时刻只有一个方向
                          在途（相位算法见下）。原有的「切换」闸与 ✕ 保持静态。
         · 全双工 FULL    两条通道**同时在途**（占空比 100%），这就是「边听边说」。
       半双工互斥的相位算法（qa-motion 用同一套参数静态复算，不靠截帧）：
         包在途窗口占空比 = (L + seg) / (seg + gap)，L 为路径长、seg 为包长、gap 为空挡。
         取 gap = 196 / seg = 14 / L = 56 ⇒ 占空比 = 70/210 = **1/3**；
         两枚包同 duration（3.3s）、相位差 **半个周期**（delay 0 与 −1.65s）
         ⇒ 1/3 < 1/2，两段在途区间必不相交，前后各留 1/6 周期（0.55s）的静默间隙。
       纪律照旧：只用五原语（这里只动到 ① .mo-packet）／包不携带文字／包只在空档里跑，
       不压任何字（「切换」二字在 y57–70，两条通道在 y42 与 y82，各让开 ≥7px）／
       .mo-packet 是纯装饰件，静态语域 display:none ⇒ 100% 帧 = 静态原图。"""
    LX, RX, CW = 44, 268, 148      # A 列 x / B 列 x / 列宽；列间 76 的空档正好放「切换」二字
    CT, CB = 30, 134               # 时间区间（上 / 下）
    # ── 方向通道件（三种模式共用同一套语法，只有「谁活、什么时候活」不同）──
    def ch_r(y, i=3):                       # A → B 活通道：实线 accent + 右箭头
        return hline(194, 250, y, AC, 2.5, i) + ah_r(264, y, AC, 7)
    def ch_l(y, i=3):                       # B → A 活通道：实线 accent + 左箭头
        return hline(266, 210, y, AC, 2.5, i) + ah_l(196, y, AC, 7)
    def ch_dead(y, i=3):                    # 静默通道：压暗虚线 + 灰箭头 —— 线在，包永远不来
        return (dline("M266 %d H206" % y, HS, 2, i, dash="5 5", sty="opacity:.5")
                + ah_l(196, y, "var(--ink-3)", 7))
    def pk(x1, x2, y, ln, dur, mode_cls, delay=None, col=None, i=3):
        """通道上的能量包（原语 ①）。ln 在这里是**空挡长度**（不是路径长）：
           ln = L 时占空比 100%（包恒在途，全双工/单工用）；
           ln 远大于 L 时包只在周期的一小段里出现（半双工互斥用）。
           mode_cls 只是给 qa 认包用的标记类，没有任何样式。"""
        return packet("M%d %d H%d" % (x1, y, x2), ln, col=col, seg=14, w=10, op=".42",
                      dur=dur, i=i, delay=delay, cls=mode_cls)
    def band(x, y, h, on, i=1, col=AC, op=None):
        if on:
            return ('<rect class="pop" style="--i:%d;fill:%s%s" x="%d" y="%d" width="%d" '
                    'height="%d" rx="5"/>' % (i, col, (";opacity:%s" % op) if op else "", x, y, CW, h))
        return ('<rect class="pop" style="--i:%d" x="%d" y="%d" width="%d" height="%d" rx="5" '
                'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 5"/>'
                % (i, x, y, CW, h, HS))
    o = [txt(LX + CW // 2, 18, "A", "ttl", size=20, anchor="middle"),
         txt(RX + CW // 2, 18, "B", "ttl", size=20, anchor="middle")]
    if mode == "simplex":
        # 通道从「居中一支箭头」改成上下两条：上行活（恒有包）／下行静默（永远无包）——
        # 单工之所以是单工，看的不是「有一个方向」，而是**另一个方向的线是死的**。
        o += [band(LX, CT, CB - CT, True, 1), band(RX, CT, CB - CT, False, 2),
              ch_r(62), pk(194, 250, 62, 56, "0.9s", "duplex-simplex"),
              ch_dead(102)]
    elif mode == "half":
        # 三个轮次各 24 高、两道闸夹在轮次之间：30–54 / 闸 62 / 70–94 / 闸 102 / 110–134
        o += [band(LX, 30, 24, True, 1), band(RX, 30, 24, False, 2),
              band(LX, 70, 24, False, 2), band(RX, 70, 24, True, 2),
              band(LX, 110, 24, True, 3), band(RX, 110, 24, False, 3),
              # 两道切换闸：轮次之间必须先让线，才轮到对方（首闸在两列之间断开，让出闸名）
              dline("M%d 62 H%d" % (LX, LX + CW), HS, 2, 2, dash="5 5"),
              dline("M%d 62 H%d" % (RX, RX + CW), HS, 2, 2, dash="5 5"),
              txt(230, 67, "切换", "sm", size=14, anchor="middle", col="var(--ink-3)"),
              dline("M%d 102 H%d" % (LX, RX + CW), HS, 2, 3, dash="5 5"),
              # 冲突瞬间：A 讲话中途 B 想出声 —— 被闸拦住
              txt(RX + CW // 2, 50, "✕", "ttl", size=22, anchor="middle", col=AD),
              # ── 严格互斥的两枚包：轮次 1（A 说 · y30–54）走上通道，轮次 2（B 说 · y70–94）
              #    走下通道。占空比 1/3 + 半周期相位差 ⇒ 两段在途区间必不相交
              #    （相位错了等于把半双工讲成全双工，qa-motion 用参数静态复算钉死这一条）。
              ch_r(42), pk(194, 250, 42, 196, "3.3s", "duplex-half"),
              ch_l(82), pk(266, 210, 82, 196, "3.3s", "duplex-half", delay="-1.65s")]
    else:
        # A 30–102 / B 62–134：重叠区间 62–102 横贯两列高亮 = 同一时刻两边都在说
        o += ['<rect class="pop" style="--i:2;fill:%s;opacity:.13" x="%d" y="62" width="%d" '
              'height="40" rx="5"/>' % (AD, LX - 10, RX + CW + 20 - LX),
              band(LX, 30, 72, True, 1), band(RX, 62, 72, True, 2),
              # 插话瞬间：粗 accent-deep 快路径（与 P8 / P9 同 idiom）—— 从 B 横插进 A
              hline(264, 214, 74, AD, 5, 3), ah_l(198, 74, AD, 7),
              # ── 两个方向同时在途（占空比各 100%，永远同框）：
              #    B→A 的包直接跑在既有的快路径上（accent-deep，与那支箭头同色同向），
              #    A→B 另开一条通道落在 y96 —— 仍在重叠区 62–102 之内，且与快路径
              #    （线宽 5 ⇒ y71.5–76.5）之间留 12px，两枚包（w10 ⇒ ±5）互不相碰。
              pk(264, 214, 74, 50, "0.82s", "duplex-full", col=AD),
              ch_r(96), pk(194, 250, 96, 56, "0.9s", "duplex-full")]
    # 无字刻度的时间轴（竖直向下）
    o.append(vline(14, CT, 122, HS, 1.4, 5))
    o.append(ah_d(14, CB, "var(--ink-3)", 7))
    o += [hline(9, 19, ty, HS, 1.4, 5) for ty in (CT, CT + 26, CT + 52, CT + 78, 122)]
    return "".join(o)
_DUPLEX = [
    ("SIMPLEX", "单工", "simplex",
     "信号只走一个方向，另一端永远只能听",
     "广播 · IVR 语音播报——只能被告知，无法开口", False),
    ("HALF-DUPLEX", "半双工", "half",
     "两个方向轮流占线：必须先把你的话切成完整一段，才轮到它想和说；它说话时，没在听你",
     "对讲机的『Over』 · 传统语音助手的回合制", False),
    ("FULL-DUPLEX", "全双工", "full",
     "两个方向同时在走：边听边说，每一瞬间都在判断要不要出声",
     "人类打电话 · 声网对话式 AI 引擎", True),
]
_DIFF = [
    ("谁掌握话轮", "线路", "静音检测器", "双方实时协商"),
    ("能否插话",   "不能", "等它说完",   "随时"),
]
page("content", "".join([
    head("DUPLEX MODES · 单工 / 半双工 / 全双工", "一次对话，线路先分<strong>三种</strong>。"),
    lab(120, 236, "01 · THREE MODES"),
    ] + [
    sh("rise card-c%s" % (" on" if _on else ""),
       "left:%dpx;top:270px;width:520px;height:386px;--i:%d" % (120 + _i * 580, 2 + _i),
       '<div style="padding:20px 30px;height:100%%;display:flex;flex-direction:column">'
       '<div style="font:500 14px/1 var(--f-mono);letter-spacing:.18em;color:%s">%s</div>'
       '<div style="margin-top:12px;font:700 38px/1.15 var(--f-cn);color:var(--ink)">%s</div>'
       '<div class="fig" style="margin-top:12px">'
       '<svg viewBox="0 0 460 134" style="width:100%%;height:auto">%s</svg></div>'
       '<div style="margin-top:14px;font:400 19px/1.55 var(--f-cn);color:var(--ink-2)">%s</div>'
       '<div style="margin-top:auto;padding-top:12px;border-top:1px solid var(--hair);'
       'font:400 17px/1.5 var(--f-cn);color:var(--ink-3)">%s</div></div>'
       % (AC if _on else "var(--ink-3)", _tag, _name, _duplex_fig(_k), _mech, _ex))
    for _i, (_tag, _name, _k, _mech, _ex, _on) in enumerate(_DUPLEX)
    ] + [
    # 页级迷你图例（三张小图共用一套线型语法，图例只出一次，压在 lab 02 同一基线的右侧）
    # 2026-08-23 补第四项「静默方向」：单工卡的下行是一根压暗虚线（本轮「动效即语义」新加的
    #   —— 单工之所以是单工，看的是**另一个方向的线是死的**），页上有这根线、图例里却没有它，
    #   读者只能把它猜成「事件 / 控制」。四项排完 x≈600 < 图例盒宽 720，仍在盒内。
    figbox(1080, 664, 720, 720, 28,
           legend(0, 14, [("solid", "主数据流"), ("dash", "事件 / 控制"),
                          ("dead", "静默方向"), ("fast", "快路径")]),
           i=5),
    lab(120, 670, "02 · KEY DIFFERENCE · 差异在哪", i=5),
    sh("rise", "left:120px;top:712px;width:1680px;height:130px;--i:6",
       '<table class="mini"><thead><tr><th style="width:230px"></th>'
       '<th style="width:483px">SIMPLEX</th><th style="width:483px">HALF-DUPLEX</th>'
       '<th style="width:484px;color:var(--accent)">FULL-DUPLEX</th></tr></thead><tbody>'
       + "".join('<tr><td>%s</td><td>%s</td><td>%s</td>'
                 '<td style="color:var(--accent)">%s</td></tr>' % _r for _r in _DIFF)
       + '</tbody></table>'),
    rule(850),
    land("二代是「不能插话」，三代是「选择不插话」——一个是线路的物理限制，一个是实时决策。"),
]))

# ═══ P4 · 全双工工作原理 ·「同时在听、在想、在说」══════════════════════════
#   01 三条并行泳道（横向常亮的 accent 线 + NOW 播放头 = 同一瞬间三件事都在跑）
#   02 两枚 hot 标注（.card-c.on）：AEC / 打断快路径；再一条 .note 说清半双工的成因
_LANES = [
    ("1", "听", "LISTEN", "连续拾音 · VAD 持续检测 · 流式 ASR——不切段，不等你说完"),
    ("2", "想", "THINK",  "增量理解 · 每一瞬间都在判断：现在要不要出声"),
    ("3", "说", "SPEAK",  "流式 TTS · 随时可收声让位"),
]
_MECHS = ["AEC 回声消除——不把自己的声音听成用户", "打断快路径——用户插话 340ms 内收声"]
# 2026-08-20 三轮升维：三条「一条线 + 一句话」的泳道 → 三条真正的活动带。
#   听：连续波形带，横贯全程永不中断（中段起是新出现的用户语音，加重）
#   想：等距判定刻度，每一格就是一次「要不要出声」（无字刻度 —— 没有已核定的分格数字）
#   说：TTS 输出块，第二块在 x=1080 被截断；截断点与听带上用户语音块的起点垂直对齐，
#      两点之间是 P8 同款 accent-deep 粗线快路径，标 340ms（deck 内既有口径）
_XIN = 1080          # 用户开口 = TTS 截断 = 快路径的两端，三条泳道共用这一根垂线
_XNOW = 860          # NOW 播放头：此刻听在收、想在判、说在讲 —— 三件事真的同时在跑
def _duplex_lanes():
    o = []
    tops = [6, 120, 234]
    for i, (num, cn, en, body) in enumerate(_LANES):
        t = tops[i]
        by, bh = t + 48, 44           # 活动带
        o.append('<circle class="pop box" style="--i:%d" cx="24" cy="%d" r="16" stroke-width="2"/>'
                 % (i + 1, t + 26))
        o.append(txt(24, t + 33, num, "ttl", size=18, anchor="middle", col=AC))
        o.append(txt(54, t + 34, cn, "ttl", size=28))
        o.append(txt(54, t + 60, en, "lbl", size=13))
        o.append(txt(152, t + 34, body, "txt", size=22))
        if i == 0:      # 听：永不中断的输入波形；_XIN 之后是新出现的用户语音（加重）
            # 运动原语 ①：波形带底下压一列能量包，横贯全程 —— 「听的车道永不关闭」
            o.append(packet("M162 %d H1636" % (by + bh // 2), 420, seg=26, w=13, op=".22", dur="2.4s", i=1))
            o.append(_bars(162, 54, by + bh // 2, "var(--ink-3)", seed=2, gap=17, w=7, op=".42"))
            o.append(_bars(1084, 23, by + bh // 2, AC, seed=6, gap=17, w=8))
            o.append(_bars(1480, 9, by + bh // 2, "var(--ink-3)", seed=13, gap=17, w=7, op=".42"))
            o.append(txt(1084, by - 12, "用户插话", "sm", size=15, col=AC, mono=True))
        elif i == 1:    # 想：等距判定刻度，_XIN 那一格是「让位」的那次判断（实心）
            o.append(hline(160, 1636, by + bh // 2, HS, 1.4, 3))
            for k in range(27):
                x = 160 + k * 56
                hot = abs(x - _XIN) < 28
                o.append(vline(x, by + 4, by + bh - 4, AD if hot else HS, 3 if hot else 1.4, 3))
            o.append(txt(1636, by - 12, "每格一次「要不要出声」", "sm", size=15, anchor="end"))
        else:           # 说：TTS 输出块 —— 第二块在 _XIN 被截断，其后让位（空带）
            for bx, bw in [(160, 452), (700, _XIN - 700)]:
                o.append('<rect class="pop" style="--i:4;fill:%s" x="%d" y="%d" width="%d" '
                         'height="%d" rx="5"/>' % (AC, bx, by, bw, bh))
            o.append(vline(_XIN, by - 6, by + bh + 6, AD, 4, 5))
            o.append('<rect class="pop" style="--i:5" x="%d" y="%d" width="%d" height="%d" rx="5" '
                     'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 6"/>'
                     % (_XIN + 10, by, 1626 - _XIN, bh, HS))
            o.append(txt(_XIN + 22, by - 12, "收声让位", "sm", size=15, col=AD, mono=True))
    # ── 快路径：听见插话 → 判断让位 → 收声，一根 accent-deep 粗线贯穿三带（P8 idiom）──
    o.append(vline(_XIN, 106, 268, AD, 5, 6))
    # 运动原语 ③（轻）：快路径节点脉冲 —— 「340ms 那一下」在跳，但不抢波形
    o.append('<circle class="pop mo-pulse" style="--i:6;--mo-lo:.45;--mo-dur:2.8s;fill:%s" '
             'cx="%d" cy="190" r="8"/>' % (AD, _XIN))
    o.append(ah_d(_XIN, 280, AD, 8))
    o.append(txt(_XIN + 20, 248, "340ms", "ttl", size=20, col=AD, weight=700))
    # ── NOW 播放头：一条竖虚线穿过三条活动带 —— 「同一瞬间」三件事都在跑 ──
    # 运动原语 ②：NOW 播放头的 dash 缓慢下爬（刻度不动、播放头在读）
    o.append(dline("M%d 50 V336" % _XNOW, AC, 1.6, 7, dash="4 8", cls="mo-drift",
                   sty="--mo-off:-24;--mo-dur:1.8s"))
    o.append(txt(_XNOW, 42, "NOW", "lbl", size=14, anchor="middle", col=AC))
    return "".join(o)
page("content", "".join([
    head("FULL-DUPLEX MECHANICS · 工作原理", "<strong>同时</strong>在听、在想、在说。"),
    lab(120, 236, "01 · THREE LANES · 同时在跑"),
    figbox(120, 268, 1680, 1680, 352, _duplex_lanes(), i=1),
    figbox(1080, 630, 720, 720, 28,
           legend(0, 14, [("solid", "音频流"), ("dash", "事件 / 控制"), ("fast", "快路径")]), i=4),
    lab(120, 636, "02 · TWO MECHANISMS · 两个关键机构", i=4),
    ] + [
    sh("rise card-c on", "left:%dpx;top:668px;width:820px;height:74px;--i:%d" % (120 + _i * 860, 5 + _i),
       '<div style="height:100%%;display:flex;align-items:center;gap:18px;padding:0 30px">'
       '<span style="width:10px;height:10px;border-radius:50%%;background:var(--accent);'
       'flex:none"></span>'
       '<span style="font:500 23px/1.4 var(--f-cn);color:var(--ink)">%s</span></div>' % _m)
    for _i, _m in enumerate(_MECHS)
    ] + [
    sh("flow", "left:120px;top:766px;width:1680px;height:54px;--i:7",
       '<div class="note grey">半双工的成因：系统必须先靠静音检测把话「切」成完整一段才开始想'
       '——你停顿一下，它就以为你说完了。</div>'),
    rule(850),
    land("全双工是「时间」维度的能力，与「端到端 / 级联」的链路选型正交"
         "——级联链路同样做到全双工，这正是引擎的做法。"),
]))

# ═══ P5 · 三件极致 ·「把三件事，做到极致」（三数章的**目录页**）════════════════
# 2026-08-23 三数章重构：本页亮完三个数字之后，6–10 页逐个把它们拆开、最后合回一张图。
#   页上因此多两件**纯导航**的东西（不新造数字、不新造主张，只是把既有页序说出来）：
#     ① 每张数字卡右上角一枚章内指针（「↓ P6」「↓ P7–8」「↓ P9」）—— 家族小号 mono，
#        与卡内左上角的「01 · LATENCY」同一档字号色阶，隔着整张卡宽不会打架。
#        340 那张写「↓ P7–8」：判停（P7）是前提、打断（P8）是正文，两页合起来才是这一枚数字。
#     ② 收口线之下补一句 land 指引 —— 本页此前没有 land，这一句正好把页脚压住。
_EXTREMES = [
    ("01 · LATENCY",  "650", "ms", "端到端响应延时", "从说完话到智能体开口，全链路深度优化，低至 650ms。",
     "&#8595; P6"),
    ("02 · BARGE-IN", "340", "ms", "极速打断响应",   "随时插话即时收声，模拟真人对话节奏。",
     "&#8595; P7&#8211;8"),
    ("03 · SHIELD",   "95",  "%",  "环境干扰屏蔽",   "选择性注意力锁定，嘈杂环境也能精准听清对话人声。",
     "&#8595; P9"),
]
page("content", "".join([
    head("REAL-TIME VOICE · 极致实时语音体验", "把三件事，<strong>做到极致</strong>。"),
    lab(120, 236, "01 · THREE EXTREMES"),
    ] + [
    sh("rise card-c", "left:%dpx;top:300px;width:520px;height:500px;--i:%d" % (120 + _i * 580, 2 + _i),
       # 章内指针：绝对定位在卡的**右上角**（.sh 自己是 position:absolute ⇒ 直接作它的定位父），
       # right 30 / top 44 与卡内 padding（44 40）同一条内边距。
       # 为什么钉角、而不是去和左上角那行「01 · LATENCY」对齐同一基线：卡内容是
       # justify-content:center 的，三张卡的正文行数不一样（1 行 / 2 行），小标的 y 本来就
       # 各不相同 —— 跟着它走，三枚指针会歪成三个高度。钉角则三张卡逐像素齐平。
       '<div style="position:absolute;right:30px;top:44px;font:500 14px/1 var(--f-mono);'
       'letter-spacing:.16em;color:var(--ink-3)">%s</div>'
       '<div style="padding:44px 40px;height:100%%;display:flex;flex-direction:column;justify-content:center">'
       '<div style="font:500 14px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-3)">%s</div>'
       '<div style="margin-top:28px;font:900 132px/.92 var(--f-en);letter-spacing:-.035em;color:var(--accent)">'
       '%s<span style="font-size:.38em;letter-spacing:0">%s</span></div>'
       '<div style="margin-top:28px;font:700 32px/1.25 var(--f-cn);color:var(--ink)">%s</div>'
       '<div style="margin-top:14px;font:400 20px/1.65 var(--f-cn);color:var(--ink-2)">%s</div></div>'
       % (_ptr, _tag, _v, _u, _n, _d))
    for _i, (_tag, _v, _u, _n, _d, _ptr) in enumerate(_EXTREMES)
    ] + [
    rule(850),
    # 章内导航句（不是主张，只是把新页序说出来）：三个数各有一页正文，尾页合回大图
    land("三件事，接下来<strong style='color:var(--accent)'>逐页拆开</strong>"
         "——最后合回<strong style='color:var(--accent)'>一张图</strong>。", y=900),
    # 原 rail（纯英文口号）替换为 SOURCE 行：三个数字是全 deck 被引用最多的口径，
    # 必须自带出处与「典型值」限定（2026-08-20 仲裁 P0）。
    # 2026-08-23 采纳项 C：并入四段 ledger —— 两个来源用「/」并列，「典型值」占样本段。
    src(_SRC_TYP),
]))

# ═══ P6 · 实时语音链路 ·「一条深度优化的实时语音链路」══════════════════════
#   2026-08-20 仲裁 P0：数字人移出串行主链 —— TTS 之后分两路并行，
#   主路「语音输出」直达喇叭，虚线支路「数字人 · 可选」挂在主路之外，
#   端到端 650ms 的跨度线因此只跨主路（原版把数字人串在 TTS 与喇叭之间，
#   等于宣称数字人也在 650ms 预算内，与 P5 口径打架）。
#   分步：step1 = 分叉支路与数字人（讲者先讲通主链，再展开可选件）。
_PIPE = [
    # hot 落 AI-VAD：链路里唯一声网自研差异化环节；LLM 是可替换第三方件，高亮它=错误的强调声明
    ("AI-VAD", "智能人声检测", "判断谁在说", True),
    ("ASR",    "语音转写",     "听清说什么", False),
    ("LLM",    "大模型理解",   "想怎么答",   False),
    ("TTS",    "语音合成",     "开口说话",   False),
]
_PIPE_X = [180, 470, 760, 1050]     # 每框 w220，间距 70
def _pipe_fig():
    o = []
    # 入口 / 出口的圆（麦克风 · 喇叭）
    o.append('<circle class="pop box" style="--i:0" cx="70" cy="185" r="44" stroke-width="1.4"/>')
    o.append('<path class="pop" style="--i:0" d="M70 165a10 10 0 0 1 10 10v10a10 10 0 0 1-20 0v-10a10 10 0 0 1 10-10z '
             'M56 183a14 14 0 0 0 28 0 M70 197v9" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % AC)
    o.append(txt(70, 288, "人声输入", "ttl", size=20, anchor="middle"))
    o.append('<circle class="pop box" style="--i:6" cx="1610" cy="185" r="44" stroke-width="1.4"/>')
    o.append('<path class="pop" style="--i:6" d="M1600 173h-10v24h10l16 13V160z M1624 176a10 10 0 0 1 0 18 '
             'M1631 169a18 18 0 0 1 0 32" fill="none" stroke="%s" stroke-width="2.4" '
             'stroke-linecap="round" stroke-linejoin="round"/>' % AC)
    o.append(txt(1610, 288, "语音输出", "ttl", size=20, anchor="middle"))
    # 四个串行环节
    for i, (n, sub, foot, hot) in enumerate(_PIPE):
        x = _PIPE_X[i]
        cx = x + 110
        # 运动原语 ④：本页唯一 hot 件（AI-VAD）呼吸 + 光晕
        if hot:
            o.append(halo_rect(x, 120, 220, 130, 6, sc="1.07", op=".3", dur="3.4s"))
        o.append(box(x, 120, 220, 130, 6, hot=hot, i=i + 1,
                     cls="mo-breathe" if hot else "", sty="--mo-dur:3.4s" if hot else ""))
        o.append(txt(cx, 178, n, "ttl", size=26, anchor="middle",
                     col=AC if hot else None))
        o.append(txt(cx, 214, sub, "sm", size=17, anchor="middle"))
        o.append(txt(cx, 290, foot, "lbl", size=15, anchor="middle"))
    # 主路连接箭头（末段 TTS → 喇叭，中途在 x1415 分叉）
    # 运动原语 ①：每段接头压一枚能量包，方向与箭头一致，恒速 ≈100 单位/秒
    #（短接头过得快、末段长所以久 —— 速度一致才读成同一股流，而不是五处各自闪）
    for x1, x2, k in [(118, 180, 0), (400, 470, 1), (690, 760, 2), (980, 1050, 3), (1270, 1566, 4)]:
        _ln = x2 - 12 - x1
        o.append(packet("M%d 185 H%d" % (x1, x2 - 12), _ln, seg=18, w=9, op=".3",
                        dur="%.2fs" % ((_ln + 18) / 100.0), i=k))
        o.append(hline(x1, x2 - 12, 185, HS, 2, k))
        o.append(ah_r(x2, 185, "var(--ink-3)"))
    # ── step1：分叉点 + 虚线支路 + 数字人（可选件，不在主路上）──
    #   2026-08-20 四轮微调：支路整组左移 40px 并收窄 30px（290→260），
    #   把「数字人 · 可选」盒的右上角与喇叭下的「语音输出」标签拉开 ≥40px
    #   （原 10px：盒右缘 1560 贴着标签左缘 1570，读成两件东西粘在一起）。
    #   左侧同时验过：TTS 脚注「开口说话」右缘 ≈1198，盒左缘 1245 → 47px，两侧都松。
    #   分叉点 x 随盒心一起移到 1375，仍落在 TTS→喇叭那一段主路上，语义与 650ms 口径不变。
    o.append('<g data-step="1">')
    o.append('<circle class="pop" style="--i:1;fill:%s" cx="1375" cy="185" r="6"/>' % AC)
    o.append(dline("M1375 193 V276", HS, 2, 2, dash="6 6", cls="mo-drift",
                   sty="--mo-off:-24;--mo-dur:2.4s"))
    o.append(ah_d(1375, 290, "var(--ink-3)", 7))
    o.append(box(1245, 292, 260, 70, 6, dashed=True, i=3))
    o.append(txt(1375, 322, "数字人 · 可选", "ttl", size=21, anchor="middle"))
    o.append(txt(1375, 348, "口型 / 表情 · 与主路并行", "sm", size=14, anchor="middle"))
    o.append('</g>')
    # 端到端跨度标注（文字在线上方，绝不压线）· 只跨主路，数字人支路在线之上、不计入
    o.append(txt(840, 372, "端到端 650ms", "ttl", size=28, anchor="middle", col=AC, weight=700))
    o.append(dline("M70 400 H1610", AC, 1.6, 6, dash="3 8"))
    o.append(vline(70, 390, 410, AC, 1.6, 6))
    o.append(vline(1610, 390, 410, AC, 1.6, 6))

    # 盒链 + 分叉 + 650ms 是一组（整组上提 46px，收掉标题与图之间的空档）
    chain = "".join(o)
    o = []
    # ── 2026-08-20 三轮升维：链下加一条「增量流带」──────────────────────────
    #   ① 无字小跨度线（4 条，与上方四个盒左对齐、彼此重叠）：每一环不等上一环说完。
    #      刻意无字、无数字 —— 分环耗时没有已核定口径，全 deck 只有 650ms 一个数字。
    #   ② 增量流带：符号从左到右渐变形态（音频帧 → 增量文本 → token → 音频包），
    #      段落标注只用既有词（P8 里的「增量文本」「增量合成 · 随时可截断」）。
    for k, (sx, ex) in enumerate([(150, 620), (450, 920), (750, 1220), (1050, 1620)]):
        y = 432 + k * 12
        o.append('<rect class="pop" style="--i:%d;fill:%s;opacity:%s" x="%d" y="%d" width="%d" '
                 'height="4" rx="2"/>' % (k + 2, AC, [".95", ".72", ".52", ".38"][k], sx, y, ex - sx))
    o.append(packet("M150 518 H1596", 430, seg=26, w=13, op=".2", dur="5s", i=7))
    o.append(hline(150, 1596, 518, HS, 1.4, 7))
    o.append(ah_r(1610, 518, "var(--ink-3)", 7))
    # ① 音频帧（AI-VAD 段）：细密竖条
    for k in range(19):
        h = [16, 26, 12, 30, 20][k % 5]
        o.append('<rect class="pop" style="--i:5;fill:%s" x="%d" y="%d" width="5" height="%d" rx="2"/>'
                 % (AC, 152 + k * 15, 518 - h // 2, h))
    # ② 增量文本（ASR 段）：一截截长出来的文本条
    for k in range(7):
        o.append('<rect class="pop" style="--i:6;fill:%s;opacity:.9" x="%d" y="510" width="%d" '
                 'height="9" rx="4"/>' % (AC, 452 + k * 40, 12 + k * 3))
    o.append(txt(452, 492, "增量文本", "sm", size=15, col=AC, mono=True))
    # ③ token（LLM 段）：一颗颗方块
    for k in range(11):
        o.append('<rect class="pop" style="--i:6;fill:%s;opacity:.85" x="%d" y="509" width="17" '
                 'height="17" rx="4"/>' % (AC, 752 + k * 26, ))
    # ④ 音频包（TTS 段）：越来越密的圆角包，末尾被 accent-deep 截断记号收住
    for k in range(13):
        o.append('<rect class="pop" style="--i:7;fill:%s;opacity:.9" x="%d" y="505" width="26" '
                 'height="26" rx="7"/>' % (AC, 1052 + k * 34, ))
    o.append(txt(1052, 492, "增量合成 · 随时可截断", "sm", size=15, col=AC, mono=True))
    o.append(vline(1502, 498, 538, AD, 4, 8))
    # ── 迷你图例（本页真正用到的三种线型）──
    o.append(legend(0, 554, [("solid", "音频流"), ("dash", "事件 / 控制"), ("fast", "快路径")]))
    return ('<g transform="translate(0,-46)">%s</g><g transform="translate(0,-34)">%s</g>'
            % (chain, "".join(o)))
page("content", "".join([
    head("EXTREME 01 · 650MS · PIPELINE · 实时语音链路", "一条深度优化的<strong>实时语音</strong>链路。"),
    lab(120, 236, "01 · SIGNAL PATH"),
    figbox(120, 274, 1680, 1680, 536, _pipe_fig(), i=1),
    rule(850),
    land("AI-VAD、ASR、LLM、TTS 逐环节协同优化——用户体感是一句接一句，几乎无等待。"),
]), steps=1)

# ═══ P7 · VAD ·「让机器知道，你在说话」════════════════════════════════════
#   01 横向 4 节点 timeline（末节点 hot = 语义判停）  02 工作原理 strip（card-c 单条）
#   03 两张并排卡：开源 TEN VAD / 商业 AI-VAD 进阶版（后者 .card-c.on）
#   04 TEN 生态 chips（尾 chip .chip.on = 商业进阶）  + SOURCE 行
_VADEVO = [
    ("能量 / 过零率", "规则阈值 · 环境一嘈杂就失灵",                        False),
    ("统计模型",      "GMM · WebRTC VAD 一代标配",                          False),
    ("深度学习",      "帧级神经网络 · Silero 等",                            False),
    ("语义判停",      "不只「有没有声」，而是「说完了没有」· SOS/EOS + 语义", True),
]
def _vad_evo():
    """发展 timeline（vb 1680×106）：一条主线 + 4 个节点，末节点填实走 accent"""
    o = [hline(38, 1642, 26, HS, 2, 1), ah_r(1654, 26, "var(--ink-3)")]
    for i, (n, d, hot) in enumerate(_VADEVO):
        x = 30 + i * 400
        cx = x + 8
        if hot:
            o.append('<circle class="mo-halo" style="--mo-sc:2.4;--mo-op:.45;--mo-dur:3.2s" '
                     'cx="%d" cy="26" r="10" fill="none" stroke="%s" stroke-width="2.5" opacity="0"/>'
                     % (cx, AC))
            o.append('<circle class="pop" style="--i:%d;fill:%s" cx="%d" cy="26" r="10"/>' % (i + 2, AC, cx))
        else:
            o.append('<circle class="pop box" style="--i:%d" cx="%d" cy="26" r="9" stroke-width="2"/>' % (i + 2, cx))
        o.append(vline(cx, 36, 46, AC if hot else HS, 1.6, i + 2))
        o.append(txt(x, 76, n, "ttl", size=25, col=AC if hot else None))
        o.append(txt(x, 102, d, "sm", size=16))
    return "".join(o)
_VADSTEP = ["16kHz 分帧（10/16ms）", "每帧输出语音概率", "平滑 / 滞回", "SOS / EOS 事件"]
# ── 2026-08-20 三轮升维：「工作原理」从一条箭头文字条 → 一张真信号图（vb 1680×142）──
#   波形段 → 分帧栅格（刻 10/16ms，唯一已核定的数字）→ 逐帧概率曲线（0–1 纵轴）
#   → 上下两条点线阈值 = 滞回带 → 上穿处钉 SOS 事件 pin、持续低于下阈处钉 EOS pin
#   → 曲线右端叠一层语义层（+ 语义判停）。四个 _VADSTEP 词一个不少，全部就地变成标注。
_VTOP, _VBOT = 62, 96          # 滞回带上/下阈（y），概率 1 在 y=40、0 在 y=124
_VSOS, _VEOS = 880, 1380       # 两枚事件 pin 的 x
def _vad_signal():
    o = []
    # ① 波形段
    o.append(_bars(10, 17, 80, AC, seed=3, gap=17, w=8))
    o.append(hline(300, 312, 80, HS, 2, 2)); o.append(ah_r(324, 80, "var(--ink-3)", 7))
    # ② 分帧栅格：帧级 10/16ms —— 全页唯一的数字口径
    o.append(txt(342, 18, "16kHz 分帧（10/16ms）", "sm", size=14, col="var(--ink-3)", mono=True))
    o.append('<rect class="pop box" style="--i:2" x="342" y="48" width="272" height="64" rx="4" '
             'stroke-width="1.4"/>')
    o += [vline(342 + k * 17, 48, 112, HS, 1, 3) for k in range(1, 16)]
    o.append(hline(614, 626, 80, HS, 2, 3)); o.append(ah_r(638, 80, "var(--ink-3)", 7))
    # ③ 概率纵轴 0–1
    o.append(vline(680, 40, 124, HS, 1.4, 4))
    o.append(txt(672, 46, "1", "sm", size=13, anchor="end"))
    o.append(txt(672, 128, "0", "sm", size=13, anchor="end"))
    o.append(txt(700, 18, "每帧输出语音概率", "sm", size=14, col="var(--ink-3)", mono=True))
    # ④ 滞回带：两条点线阈值（参考语域）+ 极淡填充
    o.append('<rect class="pop" style="--i:4;fill:%s;opacity:.07" x="680" y="%d" width="980" '
             'height="%d" rx="3"/>' % (AD, _VTOP, _VBOT - _VTOP))
    o.append(dline("M680 %d H1660" % _VTOP, AD, 2, 5, dash="2 6", cls="mo-drift",
                   sty="--mo-off:-32;--mo-dur:4s"))
    o.append(dline("M680 %d H1660" % _VBOT, AD, 2, 5, dash="2 6", cls="mo-drift",
                   sty="--mo-off:-32;--mo-dur:4s;--mo-del:-2s"))
    o.append(txt(692, 56, "平滑 / 滞回", "sm", size=13, col=AD, mono=True))
    # ⑤ 逐帧概率曲线（accent 实线）
    o.append('<path class="dw" style="--len:1200;--i:5" d="M680 118 C 770 116, 836 102, 880 62 '
             'C 922 30, 980 40, 1042 48 C 1104 56, 1140 40, 1200 50 C 1256 60, 1272 84, 1302 96 '
             'C 1344 112, 1420 118, 1660 116" fill="none" stroke="%s" stroke-width="3" '
             'stroke-linecap="round"/>' % AC)
    # ⑥ 两枚事件 pin（虚线 = 事件语法）
    for _j, (px, nm) in enumerate([(_VSOS, "SOS"), (_VEOS, "EOS")]):
        _d = "" if _j == 0 else ";--mo-del:-1.2s"
        o.append(dline("M%d 32 V126" % px, HS, 2, 6, dash="6 6", cls="mo-drift",
                       sty="--mo-off:-24;--mo-dur:2.4s" + _d))
        o.append('<circle class="pop mo-pulse" style="--i:6;--mo-dur:2.4s%s;fill:%s" cx="%d" cy="%d" r="6"/>'
                 % (_d, AC, px, _VTOP if px == _VSOS else 117))
        o.append(txt(px + 12, 44, nm, "lbl", size=15, col=AC))
    o.append(txt(1180, 18, "SOS / EOS 事件", "sm", size=14, col="var(--ink-3)", mono=True))
    # ⑦ 声学之上再叠一层语义（商业进阶版的差异，用既有词）
    o.append('<path class="pop mo-drift" style="--i:7;--mo-off:-30;--mo-dur:2.8s" '
             'd="M1430 78 C 1500 62, 1560 54, 1660 46" fill="none" '
             'stroke="%s" stroke-width="3" stroke-dasharray="9 6"/>' % AD)
    o.append(txt(1660, 34, "+ 语义判停", "sm", size=15, col=AD, weight=700, anchor="end"))
    # ⑧ 迷你图例（压在信号图左下角的空位，与 SOURCE / 卡片分层）
    o.append(legend(0, 136, [("solid", "主数据流"), ("dash", "事件 / 控制"), ("dot", "参考 / 反馈")]))
    return "".join(o)
_VADCARDS = [
    (False, "OPEN SOURCE · APACHE 2.0", "我们开源的帧级实时 VAD",
     ["精度优于 WebRTC VAD 与 Silero VAD（公开测试集 PR 曲线）",
      "说→停转换毫秒级捕捉——Silero 有数百 ms 拖尾",
      "RTF 0.015 · 306KB 起 · 全平台 · Python/C/Java/Go/JS"],
     "github.com/ten-framework/ten-vad"),
    (True, "IN ENGINE · 进阶版", "引擎内建的进阶版：声学之上，加语义",
     ["CAN + 语义 + 声学三路融合的判停",
      "三态人声 · 暂停意图 · 误打断防抖",
      "随对话式 AI 引擎交付，免调优开箱"],
     ""),
]
# chips 落 rule(850) 之下作页脚生态带——破例经 Fable 终审裁定（生态链接本属页脚语域）
_TENCHIPS = [("TEN Framework", False), ("TEN VAD", False), ("Turn Detection", False),
             ("Agent Examples", False), ("ConvoAI Engine（商业进阶）", True)]
page("content", "".join([
    head("EXTREME 02 · 340MS · 前提 · VOICE ACTIVITY DETECTION · 从能量检测到语义判停",
         "VAD：让机器知道，<strong>你在说话</strong>。"),
    lab(120, 236, "01 · EVOLUTION · 发展"),
    figbox(120, 264, 1680, 1680, 106, _vad_evo(), i=1),
    lab(120, 388, "02 · HOW IT WORKS · 工作原理", i=3),
    figbox(120, 414, 1680, 1680, 146, _vad_signal(), i=4),
    # ── step1：区 03 两卡 + 区 04 chips（先讲清「什么是判停」，再展开开源 / 商业两条腿）──
    #   信号图吃掉了 02 区的高度，04 的 TEN 生态 chips 下移到收口线之下当落地带
    #   （rule 之下、SOURCE 之上那一段本来就是空的，chips 正好把页脚压住）。
    lab(120, 588, "03 · OPEN SOURCE × IN ENGINE", i=4, step=1),
    ] + [
    sh("rise card-c%s" % (" on" if _on else ""),
       "left:%dpx;top:616px;width:820px;height:226px;--i:%d" % (120 + _i * 860, 5 + _i),
       '<div style="padding:22px 30px;height:100%%;display:flex;flex-direction:column">'
       '<div style="font:500 14px/1 var(--f-mono);letter-spacing:.18em;color:%s">%s</div>'
       '<div style="margin-top:9px;font:700 26px/1.25 var(--f-cn);color:var(--ink)">%s</div>'
       '<div style="margin-top:11px;display:flex;flex-direction:column;gap:5px">%s</div>%s</div>'
       % (AC if _on else "var(--ink-3)", _tag, _ttl,
          "".join('<div style="display:flex;gap:11px;align-items:baseline">'
                  '<span style="color:var(--accent);font:700 15px/1.5 var(--f-mono)">&#8212;</span>'
                  '<span style="font:400 18px/1.5 var(--f-cn);color:var(--ink-2)">%s</span></div>' % _b
                  for _b in _bul),
          ('<div style="margin-top:auto;padding-top:12px;font:500 15px/1 var(--f-mono);'
           'letter-spacing:.06em;color:var(--ink-3)">%s</div>' % _foot) if _foot else ""),
       step=1)
    for _i, (_on, _tag, _ttl, _bul, _foot) in enumerate(_VADCARDS)
    ] + [
    rule(850),
    sh("rise", "left:120px;top:900px;width:1680px;height:52px;--i:8",
       '<div style="display:flex;align-items:center;gap:22px">'
       '<span class="seclab" style="flex:none">04 · TEN 生态</span><div style="flex:1">'
       + "".join('<span class="chip%s">%s</span>' % (" on" if _o else "", _c)
                 for _c, _o in _TENCHIPS) + '</div></div>', step=1),
    # 判停重构落在 V2.6，但 SOS/EOS 是「自 V2.6 起重构」而非「V2.6 才有 VAD」——
    # 原写法「引擎发版说明 V2.6」会被读成后者（2026-08-20 仲裁 P1）。
    # 2026-08-23 采纳项 C：三个来源用「/」并列进来源段，V2.6 判停窗占样本/时间窗段，
    # 补齐家族统一的「事实截止」收尾。
    src("SOURCE · GITHUB.COM/TEN-FRAMEWORK/TEN-VAD / TEN ECOSYSTEM / 引擎发版说明 · "
        "SOS/EOS 判停重构自 V2.6 · 事实截止 2026.08", i=9),
]), steps=1)

# ═══ P8 · 拆 340 ·「想插话就插话，340ms 即时收声」（页号 9→8）══════════════
# 2026-08-23 三数章重构：本页从 P9 提到 P8 —— 它是 P5「02 · 340MS」那一枚数字的**正文**，
#   而 P7（VAD 判停）是它的前提。原序把大图夹在 P7 与本页之间，等于在「前提」与「结论」
#   中间插了一整张总览图，三个数字的展开被拦腰截断。现在 650 / 340 / 95% 连着讲完，
#   大图挪到章尾当收束。kicker 前加「EXTREME 02 · 340MS · 」把页与数字绑死。
# 2026-08-20 三轮升维：双轨波形保留骨架，补三件事 ——
#   ① 对齐关系画清楚：智能体轨的输出块，正好在用户轨语音块开始后 340ms 处被切断
#   ② 上方三段相位括号：侦测 → 收声 → 让位（前两段之和 = 340ms）
#   ③ 340ms 跨度线加粗成 P8 同款 accent-deep 快路径，是全图的主标注（也是唯一 hot 件）
# 2026-08-20 四轮 · 构图再平衡（因果全挤在右半页 x≥900、左下大片空，相位括号 60/100px 局促）：
#   ① 时间轴整体左移并放大 340ms 窗口：_P9IN 900→700、_P9CUT 1060→1040，
#      340px = 340ms（1px = 1ms），因果簇（快路径 / 两条时刻线 / 两枚事件标）落回版心
#   ② 相位括号行重新配比：侦测 140px · 收声 200px · 让位 600px，三段都 ≥140px，标签不再挤
#   ③ 左侧波形补既有词标注「智能体正在说话」；用户轨在插话前补一条无字静默平线
#      （刻意无字 —— 全 deck 只有 340ms 一个时间数字，不能给静默段编一个新的）
#   ④ 波形定高序列换成 P9 专属常量表 _P9HS（与 P4 那张的轮廓区分开）
#   340ms 快路径、切断对齐（智能体轨的切断竖线 = 用户开口 + 340ms）、land 语义全部不动。
_P9IN, _P9CUT = 700, 1040      # 用户开口 / 智能体收声（相距 340px = 340ms，1px = 1ms）
_P9HS = [20, 44, 64, 36, 28, 52, 16, 60, 40, 24, 56, 32, 48, 18, 62, 38, 26, 54, 34, 58, 22, 46, 30]
_P9QUIET = ('<rect class="pop" style="--i:%d;fill:var(--ink-3);opacity:.3" x="%d" y="%d" '
            'width="%d" height="4" rx="2"/>')
def _barge_fig():
    o = []
    # ── 相位括号（三段重新配比：140 / 200 / 600）──
    for x1, x2, nm in [(_P9IN, 840, "侦测"), (840, _P9CUT, "收声"), (_P9CUT, 1640, "让位")]:
        o.append(hline(x1, x2, 62, AD, 2, 1))
        o.append(vline(x1, 62, 74, AD, 2, 1))
        o.append(vline(x2, 62, 74, AD, 2, 1))
        o.append(txt((x1 + x2) // 2, 46, nm, "sm", size=17, anchor="middle", col=AD, weight=700))
    # ── 智能体轨：说到一半被切断，其后是空带（让位）──
    o.append(txt(10, 128, "智能体", "ttl", size=22, col=AC))
    # 左侧波形的既有词标注：这一大段波形在讲什么，之前完全没说
    o.append(txt(170, 74, "智能体正在说话", "sm", size=17, col=AC))
    # 运动原语 ③ · 第 1 拍：智能体正在说（整条波形轻脉冲，文字在组外不跟着闪）
    o.append('<g class="mo-pulse" style="--mo-lo:.62;--mo-dur:3.6s">%s</g>'
             % _bars(170, 51, 120, AC, hs=_P9HS))
    o.append('<rect class="pop" style="--i:3" x="1055" y="88" width="585" height="64" rx="6" '
             'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 6"/>' % HS)
    o.append(_P9QUIET % (3, 1075, 118, 545))       # 让位段：无字静默平线（与用户轨呼应）
    # 第 3 拍：智能体收声（切断竖线；delay 1.4s ⇒ 排在插话之后）
    o.append('<g class="mo-pulse" style="--mo-lo:.34;--mo-dur:3.6s;--mo-del:1.4s">%s</g>'
             % vline(_P9CUT, 82, 158, AD, 4, 3))
    # ── 340ms 快路径：插话 → 收声，粗 accent-deep，两端钉在两条轨之间 ──
    o.append(packet("M%d 230 V196 H%d" % (_P9IN, _P9CUT), 374, seg=30, col=AD, w=14, op=".3",
                    dur="2.4s", i=4))
    o.append('<path class="dw" style="--len:374;--i:4" d="M%d 230 V196 H%d" fill="none" '
             'stroke="%s" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
             % (_P9IN, _P9CUT, AD))
    o.append(ah_u(_P9CUT, 168, AD, 8))
    o.append(txt((_P9IN + _P9CUT) // 2, 184, "340ms", "ttl", size=26, anchor="middle",
                 col=AD, weight=700))
    # ── 用户轨：插话前是无字静默平线，从 _P9IN 起一直在说 ──
    o.append(txt(10, 278, "用户", "ttl", size=22, col="var(--ink-2)"))
    o.append(_P9QUIET % (2, 170, 268, 510))
    o.append(_bars(_P9IN, 55, 270, "var(--ink-2)", seed=3, hs=_P9HS))
    # ── 两条时刻虚线（事件语域）+ 底部标注 ──
    # 第 2 拍：用户插话（事件时刻线；delay .7s ⇒ 夹在说话与收声之间）
    o.append('<g class="mo-pulse" style="--mo-lo:.34;--mo-dur:3.6s;--mo-del:.7s">%s</g>'
             % dline("M%d 74 V320" % _P9IN, HS, 2, 5, dash="6 6"))
    o.append(dline("M%d 74 V320" % _P9CUT, HS, 2, 5, dash="6 6"))
    o.append(txt(_P9IN, 346, "用户插话", "sm", size=18, anchor="middle", col=AD, weight=700))
    o.append(txt(_P9CUT, 346, "智能体收声", "sm", size=18, anchor="middle", col=AC, weight=700))
    # 图例从 y378 提到 y340，与两枚事件标同一条基线：左 = 图例（x0–442），右 = 事件标（x664 起），
    # 中间还留 220px。这一并到一行，图底那条「左边整片空、右边两个字」的空带就没有了，
    # viewBox 也从 396 收到 372，页面重心跟着往上收一档。
    o.append(legend(0, 340, [("solid", "音频流"), ("dash", "事件 / 控制"), ("fast", "打断快路径")]))
    return "".join(o)
page("content", "".join([
    head("EXTREME 02 · 340MS · INTERRUPTION · 优雅打断", "想插话就插话，<strong>340ms 即时收声</strong>。"),
    lab(120, 236, "01 · TIMELINE"),
    figbox(120, 276, 1680, 1680, 372, _barge_fig(), i=1),
    # 图收到 372 后整块 02 上提 24px，note 回到收口线之上一个身位（原 792 → 770），
    # 页面从「上半密、下半散」收成三段等长呼吸：图 276–648 / 02 块 676–820 / 收口线 850。
    lab(120, 676, "02 · WHAT HAPPENS"),
    sh("rise", "left:120px;top:706px;width:1680px;height:54px;--i:4",
       "".join('<span class="chip">%s</span>' % t for t in
               ["智能体正在说话", "用户随时可插话", "340ms 内即时收声、转为倾听"])),
    sh("flow", "left:120px;top:770px;width:1680px;height:50px;--i:6",
       '<div class="note grey">三态人声 · 暂停意图 · 误打断防抖</div>'),
    rule(850),
    land("对话像真人一样你来我往。"),
]))

# ═══ P9 · 拆 95% ·「嘈杂环境里，只听该听的人」（页号 10→9）═════════════════
# 2026-08-23 三数章重构：本页是 P5「03 · 95%」那一枚数字的正文，紧跟在 340 的正文之后 ——
#   三个数字连着拆完，再由 P10 大图收束。kicker 前加「EXTREME 03 · 95% · 」绑数字。
# 2026-08-21 重做 ·「三种噪声 · 三层方案」：
#   旧版把「嘈杂」当成一个问题（一环挡三路），讲不出 SAL 到底进阶在哪。
#   新版左右分工：
#     左 = 三行阶梯（噪声 → 例子 → 方案），方案逐级右移 = 手段一层比一层进阶；
#          03「非对话人人声」是 hot ——它才是 SAL 要解的那一类。
#     右 = 双层防御环：外环「降噪层」滤掉 01/02 两类点线波束（撞环 ✕），
#          03 的点线波束穿过外环（外环在交点处开一个洞，肉眼看得见「穿过去了」），
#          在内环「SAL 声纹层」被挡（✕）；只有目标人声的实线波束从左侧缺口穿两环直达智能体。
#   数字只留既有的「屏蔽 95% 干扰」，不发明第二个。
#   land 源自 Colin aiot26 定稿「前两类是信号问题，第三类是产品判断问题」。
_NOISES = [
    ("01", "稳态背景噪声", "STATIONARY · 例：空调 · 风扇 · 路噪",
     0, "传统降噪算法", "工程成熟 · 稳定手段", False),
    ("02", "瞬态突发", "TRANSIENT · 例：关门 · 犬吠 · 键盘 · 碰撞",
     30, "AI 降噪算法", "模型识别突发形态", False),
    ("03", "非对话人人声", "NON-TARGET SPEECH · 例：电视人声 · 旁人聊天 · 多人同说",
     60, "选择性注意力锁定 SAL · 进阶", "声纹锁定目标人，其余按背景处理", True),
]
_SCX, _SCY = 300, 196                # 场景中心（左移一档：给右侧三束点线让出可读长度）
_SR2, _SR1, _SAG = 138, 86, 54       # 外环（降噪层）/ 内环（SAL 声纹层）/ 智能体
def _ring(r, gap, i, col, dash, cls="", sty=""):
    """左侧留缺口的防御环：缺口正对目标人声波束，所以「只有它能进来」是画出来的，不是说出来的。
       cls / sty：闭环绕行原语（.mo-cycle + --mo-off/--mo-dur）—— 环的几何绝不能转，缺口一转就废。"""
    import math
    dx = math.sqrt(r * r - gap * gap)
    return ('<path class="pop%s" style="--i:%d%s" d="M%.1f %d A %d %d 0 1 1 %.1f %d" fill="none" '
            'stroke="%s" stroke-width="2.4" stroke-dasharray="%s"/>'
            % ((" " + cls) if cls else "", i, (";" + sty) if sty else "",
               _SCX - dx, _SCY - gap, r, r, _SCX - dx, _SCY + gap, col, dash))
def _sal_fig():
    import math
    o = []
    # ── 双层防御环 ──
    # 缺口开到 ±40 / ±34：一来目标人声的波束进得来，二来「声纹锁定 · 只留目标人声」
    # 这行标注要落在缺口里，缺口小于文字高度时弧线会从字上划过去（= 划掉的观感）。
    o.append(_ring(_SR2, 40, 3, HS, "9 8", cls="mo-cycle",
                   sty="--mo-off:-867;--mo-dur:26s"))     # 外环 r138 周长≈867 = dash「9 8」×51
    o.append(_ring(_SR1, 34, 3, AC, "8 7", cls="mo-cycle",
                   sty="--mo-off:540;--mo-dur:18s"))      # 内环 r86 周长≈540 = dash「8 7」×36 · 反向
    o.append(txt(_SCX, 26, "降噪层 · 传统 + AI 降噪", "sm", size=15, anchor="middle",
                 col="var(--ink-3)", mono=True, ls=".08em"))
    o.append(txt(_SCX, 310, "SAL 声纹层", "sm", size=16, anchor="middle", col=AC,
                 mono=True, ls=".1em"))
    # ── 目标人声（左）· 实线波束穿两环直达中心 ──
    o.append('<circle class="pop box" style="--i:1" cx="58" cy="%d" r="35" stroke-width="2"/>' % _SCY)
    o.append('<path class="pop" style="--i:1" d="M58 %da10 10 0 0 1 10 10v8a10 10 0 0 1-20 0v-8a10 10 0 0 1 10-10z '
             'M43 %da15 15 0 0 0 30 0 M58 %dv9" fill="none" stroke="%s" stroke-width="2.4" '
             'stroke-linecap="round"/>' % (_SCY - 22, _SCY - 4, _SCY + 6, AC))
    o.append(txt(58, 254, "目标人声", "ttl", size=20, anchor="middle", col=AC))
    o.append(txt(58, 280, "锁定 · 精准识别", "sm", size=14, anchor="middle"))
    # 能量包：压在实线之下的一段粗软 accent（stroke-opacity .3），沿路径奔向中心。
    # 不改实线本身的 dasharray —— 实线是本页图例「solid = 目标人声」的实物样本，
    # 一旦打成虚线，就和三路「dot = 干扰」的线型区分糊在一起了。
    o.append(packet("M96 %d H234" % _SCY, 162, seg=24, dur="1.6s", i=2))
    o.append(hline(96, 234, _SCY, AC, 3.5, 2)); o.append(ah_r(246, _SCY, AC))
    o.append(txt(140, 170, "声纹锁定 · 只留目标人声", "sm", size=14, anchor="middle", col=AC))
    # ── 智能体（中 · 唯一 hot 件）──
    # 呼吸光晕：压在智能体圆片之下向外扩散再消失（100% 帧 opacity 回 0 ⇒ 静态语域下不留痕）
    o.append('<circle class="mo-halo" cx="%d" cy="%d" r="%d" fill="none" stroke="%s" '
             'stroke-width="2.5" opacity="0"/>' % (_SCX, _SCY, _SAG, AC))
    o.append('<circle class="pop mo-breathe" style="--i:0;fill:var(--card-bg-2);stroke:%s" cx="%d" cy="%d" '
             'r="%d" stroke-width="3"/>' % (AC, _SCX, _SCY, _SAG))
    o.append(txt(_SCX, _SCY - 4, "智能体", "ttl", size=25, anchor="middle"))
    o.append(txt(_SCX, _SCY + 26, "声纹锁定", "sm", size=16, anchor="middle", col=AC))
    # ── 三路噪声点线波束：01/02 撞外环 ✕，03 穿外环、撞内环 ✕ ──
    _SRC = [("稳态背景噪声", 50, _SR2), ("瞬态突发", 196, _SR2), ("非对话人人声", 342, _SR1)]
    # 三路错峰：同 duration 会读成一根线（dash「2 7」×5 = 45 一个整周期）
    _NSTY = ["--mo-off:-45;--mo-dur:3.4s", "--mo-off:-45;--mo-dur:4.2s;--mo-del:-1.1s",
             "--mo-off:-45;--mo-dur:2.9s;--mo-del:-2s"]
    _XSTY = ["--mo-dur:2.4s", "--mo-dur:2.4s;--mo-del:-.8s", "--mo-dur:2.4s;--mo-del:-1.6s"]
    for _k, (n, sy, stop) in enumerate(_SRC):
        dx, dy = _SCX - 613, _SCY - sy
        ln = math.sqrt(dx * dx + dy * dy) or 1
        ux, uy = dx / ln, dy / ln                              # 单位向量：噪声源 → 中心
        o.append('<rect class="pop box" style="--i:4" x="510" y="%d" width="206" height="52" '
                 'rx="26" stroke-width="1.4"/>' % (sy - 26))
        o.append(txt(613, sy + 6, n, "sm", size=17, anchor="middle"))
        px, py = _SCX - ux * stop, _SCY - uy * stop            # 被拦下的那一层的交点
        if stop == _SR1:
            # 穿过外环：在交点上打一个不透明的洞，点线从洞里穿过去 —— 不写字也读得出「过了」
            ox, oy = _SCX - ux * _SR2, _SCY - uy * _SR2
            o.append('<circle class="pop" style="--i:4;fill:var(--card-bg-2)" cx="%.1f" cy="%.1f" '
                     'r="11"/>' % (ox, oy))
        o.append(dline("M%.1f %.1f L%.1f %.1f" % (613 + ux * 96, sy + uy * 96,
                                                  px - ux * 12, py - uy * 12), HS, 2.4, 5, dash="2 7",
                       cls="mo-drift", sty=_NSTY[_k]))
        o.append(txt(px, py + 10, "✕", "ttl mo-pulse", size=26, anchor="middle", col=AD,
                     sty=_XSTY[_k]))
    # ── 名牌：压在两环之下，读者知道这一整套叫什么 ──
    o.append('<rect class="pop" style="--i:6;fill:var(--card-bg-2)" x="150" y="372" width="300" '
             'height="56" rx="28" stroke="%s" stroke-width="2.5"/>' % AC)
    o.append(txt(_SCX, 408, "屏蔽 95% 干扰", "ttl", size=24, anchor="middle", col=AC, weight=700))
    o.append(legend(0, 452, [("solid", "目标人声"), ("dot", "干扰 · 被屏蔽")]))
    return "".join(o)
page("content", "".join([
    head("EXTREME 03 · 95% · SELECTIVE ATTENTION · 三种噪声 · 三层方案", "嘈杂环境里，<strong>只听该听的人</strong>。"),
    lab(120, 240, "01 · THREE NOISES", w=940),
    sh("rise", "left:120px;top:296px;width:940px;height:440px;--i:2",
       '<div class="rows nrow">' + "".join(
           '<div class="r%s"><span class="n">%s</span><span class="k">%s</span><span class="v">'
           '<span class="ex">%s</span>'
           '<span class="sol" style="padding-left:%dpx">&#8594; <b>%s</b><i>%s</i></span>'
           '</span></div>' % (" hot" if _h else "", _n, _k, _ex, _pad, _sol, _note)
           for _n, _k, _ex, _pad, _sol, _note, _h in _NOISES) + '</div>'),
    lab(1080, 240, "02 · TWO-LAYER DEFENSE", w=720),
    figbox(1080, 296, 720, 720, 470, _sal_fig(), i=1),
    rule(850),
    land("前两类是信号问题，第三类是「谁在和我说话」的判断问题——这正是 SAL 的进阶所在。"),
]))

# ═══ P10 · 大图收束 ·「一张图，看懂全双工引擎」（页号 8→10 · 2026-08-20 新增）══
# 2026-08-23 三数章重构：本页从 P8 挪到 P10，从「章中总览」改成「章尾收束」。
#   原序 P5 亮三个数 → P6 拆 650 → P7 VAD 前提 → **P8 大图** → P9 拆 340 → P10 拆 95%：
#   大图坐在两个前提页和它们的结论页中间，读者刚被告知「有三件极致」，第三页就迎面一张
#   全景图 —— 论证被打断，图也因为「还没讲到的东西全在上面」而变成噪声。
#   新序把三个数字连着拆完（P6 / P7–8 / P9），本页压尾：三件事都讲过了，再合回一张图。
#   本轮只做加法（几何一格不动）：图上钉三枚数字锚点 chip（①650 / ②340 / ③95%），
#   页脚补一句收束。锚点落位的账见 _anchor_chip() 与 _bigmap() 里三处调用点的注释。
#   全 deck 唯一一张「大图页」：静置全量、不分步 —— 一张图就要一眼全。
#   viewBox 1680×660 与 .sh 同尺寸 ⇒ 1 svg 单位 = 1 屏幕像素，所有坐标可直接对表。
#   三秒可读性的四个锚点（验收标准）：
#     ① 上行 / 下行两条 accent 车道同时贯穿 → 两件事同时在跑
#     ② AI-VAD 是最大的一只 hot 盒，坐在上行车道正中 → 它是路口
#     ③ accent-deep 粗线从 AI-VAD 垂直插进「语音输出」，旁注「不经过 LLM」→ 打断是快路径
#     ④ 点线从下行车道弯回 AEC，标「参考信号」→ 所以听不见自己
#   版式雷区：content 背景板自带 accent 细线在屏幕 y848–852（= svg y566–570），
#   底部 SD-RTN 条从 y566 起，正好把它压在条内，不会横穿任何文字。
_P8Q, _P8TU, _P8TD = 250, 2.2, 2.6      # 包距（含包长）/ 上行周期 / 下行周期
def _p8ph(dist, T):
    """把「离车道起点的距离」换算成负 delay：负值 ⇒ 动画一上来就在跑（不留首帧静止）。"""
    return -(dist % _P8Q) / float(_P8Q) * T

def _anchor_chip(x, y, n, label, i=9, h=32):
    """三数章锚点 chip（2026-08-23 · 只在本页用）：不透明药丸 + accent 序号圆片 + mono 数字。
       它是**静态件**：不挂 data-step、不挂任何 mo-* 原语 —— 大图页本来就是静置全量的，
       锚点更不该动（会动的锚点等于第二套主视觉，抢的正是它要指的那三处）。
       fill 走 --card-bg-2（#fffffe / #131320，不透明）：--card-bg 是 72% 透明，
       底下的线会从 chip 里透出来，读成「数字被划掉」（step_badge 踩过同一个坑）。
       盒宽按 mono 墨迹算死（15px JetBrains Mono 步进 ≈ .6em + letter-spacing .06em ≈ 9.9px/字），
       左 38 给序号圆片、右 14 呼吸 —— 改字号必须重算这一笔，虚开的盒会让占位闸失效。"""
    w = 38 + int(round(len(label) * 9.9)) + 14
    cy = y + h // 2
    return ('<rect class="pop" style="--i:%d;fill:var(--card-bg-2)" x="%d" y="%d" width="%d" '
            'height="%d" rx="%d" stroke="%s" stroke-width="1.6"/>' % (i, x, y, w, h, h // 2, AC)
            + '<circle class="pop" style="--i:%d;fill:%s" cx="%d" cy="%d" r="10"/>'
              % (i, AC, x + 21, cy)
            + txt(x + 21, cy + 5, str(n), "ttl", size=14, anchor="middle",
                  col="var(--card-bg-2)", weight=700)
            + txt(x + 38, cy + 5, label, "sm", size=15, col=AC, weight=700, mono=True, ls=".06em"))

def _bigmap():
    o = []
    # ── 域分隔（两条竖直 hairline；三域底标见 ⑥ 之上一行）──
    #   走细虚线而不是实线：舞台底纹 .slide::before 每 240px 有一条实心竖 hairline，
    #   实线域分隔会和它撞成同一种东西，读者分不清哪条是「域」。
    o += [dline("M361 96 V562", HS, 1, 0, dash="3 9"),
          dline("M1307 96 V562", HS, 1, 0, dash="3 9")]

    # ── ① 顶部控制面（客户服务器域 · 虚线横条）──
    o.append(box(260, 4, 1390, 62, 8, dashed=True, i=1))
    o.append(txt(284, 42, "客户服务器", "sm", size=14, col="var(--ink-3)", mono=True))
    o.append(txt(955, 32, "客户业务服务器 · REST 控制面", "ttl", size=22, anchor="middle"))
    o.append(txt(955, 58, "Token 签名 · 创建/控制 Agent · Function Call 回调",
                 "sm", size=14, anchor="middle", mono=True))
    o.append(ah_u(1498, 68, "var(--ink-3)", 6))
    o.append(dline("M1498 78 V106", HS, 2, 2, dash="6 6"))
    o.append(ah_d(1498, 114, "var(--ink-3)", 6))
    o.append(txt(1520, 96, "控制 / 事件", "sm", size=15))

    # ── ② 上行车道（左 → 右 · 实线音频流）──
    o.append(txt(150, 108, "上行 · 边听 &#8594;", "sm", size=15, col=AC, mono=True))
    o.append('<circle class="pop box" style="--i:1" cx="70" cy="176" r="38" stroke-width="1.4"/>')
    o.append('<path class="pop" style="--i:1" d="M70 158a9 9 0 0 1 9 9v9a9 9 0 0 1-18 0v-9a9 9 0 0 1 9-9z '
             'M57 174a13 13 0 0 0 26 0 M70 187v8" fill="none" stroke="%s" stroke-width="2.2" '
             'stroke-linecap="round"/>' % AC)
    o.append(txt(70, 236, "MIC", "lbl", size=14, anchor="middle"))
    o.append(box(150, 132, 190, 88, 6, i=2))
    o.append(txt(245, 172, "AEC 回声消除", "ttl", size=21, anchor="middle"))
    o.append(txt(245, 198, "减掉自己的声音", "sm", size=15, anchor="middle"))
    o.append(box(382, 132, 210, 88, 6, i=3))
    o.append(txt(487, 172, "SAL 声纹锁定", "ttl", size=21, anchor="middle"))
    o.append(txt(487, 198, "降噪 · 只留目标人声", "sm", size=15, anchor="middle"))
    # 全图核心件：AI-VAD 大号 hot 盒
    o.append(halo_rect(634, 116, 430, 128, 8, sc="1.05", op=".28", dur="3.4s"))
    o.append(box(634, 116, 430, 128, 8, hot=True, i=4, cls="mo-breathe", sty="--mo-dur:3.4s"))
    o.append(txt(849, 158, "AI-VAD 进阶判停", "ttl", size=30, anchor="middle", col=AC))
    o.append(txt(849, 192, "TEN VAD 声学内核 · 帧级 10/16ms · 开源", "sm", size=16, anchor="middle"))
    o.append(txt(849, 220, "+ 语义判停 · CAN 三路融合 · 商业进阶", "sm", size=16, anchor="middle", col=AC))
    # 角标压在盒的左上角（而不是右上角）：右上角紧邻「→ ASR」那支箭头，读者会把它当箭头的注解
    o.append(txt(640, 106, "帧级 10/16ms", "sm", size=14, col=AC, mono=True))
    o.append(box(1106, 132, 180, 88, 6, i=5))
    o.append(txt(1196, 172, "流式 ASR", "ttl", size=21, anchor="middle"))
    o.append(txt(1196, 198, "增量文本", "sm", size=15, anchor="middle"))
    # 运动原语 ①（2026-08-21 动效轮新增的纯装饰件 · 几何与文字零改动）：
    #   包只在盒与盒之间的接头上跑，**不横穿盒**（盒是半透明 --card-bg，
    #   包从 AI-VAD 盒里穿过去会在「10/16ms」下面留一道荧光笔式的粉块 —— 实测实锤）。
    #   相位按「接头离车道起点 x110 的距离 mod 一个包距」对齐：五段接头依次亮，
    #   读起来就是同一枚包沿整条车道跑，而不是五处各闪各的。
    for x1, x2, k in [(110, 150, 1), (340, 382, 2), (592, 634, 3), (1064, 1106, 4), (1286, 1328, 5)]:
        o.append(packet("M%d 176 H%d" % (x1, x2 - 14), _P8Q - 26, seg=26, w=13, op=".38",
                        dur="%ss" % _P8TU, delay="%.2fs" % _p8ph(x1 - 110, _P8TU), i=k))
        o.append(hline(x1, x2 - 14, 176, AC, 2.5, k))
        o.append(ah_r(x2, 176, AC))

    # ── ③ 右侧中枢（想）：实时编排 ⇄ LLM ──
    o.append(box(1328, 116, 340, 132, 8, hot=True, i=4))
    o.append(txt(1498, 158, "实时编排 · 轮次决策", "ttl", size=25, anchor="middle", col=AC))
    o.append(txt(1498, 194, "此刻要不要出声", "sm", size=16, anchor="middle"))
    o.append(txt(1498, 220, "要不要让位", "sm", size=16, anchor="middle"))
    o.append(ah_u(1498, 252, AC, 6))
    o.append(vline(1498, 262, 312, AC, 2, 5))
    o.append(ah_d(1498, 322, AC, 6))
    o.append(box(1328, 324, 340, 88, 6, i=5))
    o.append(txt(1498, 362, "LLM", "ttl", size=26, anchor="middle"))
    o.append(txt(1498, 392, "MCP · Function Call · 知识库 RAG", "sm", size=14, anchor="middle"))
    # AI-VAD → 编排 的第二类输出：虚线事件（SOS / EOS · 打断），绕开 ASR 从下方走
    o.append(dline("M1030 250 C 1120 316, 1330 316, 1420 258", HS, 2, 5, dash="7 6",
                   cls="mo-drift", sty="--mo-off:-39;--mo-dur:3s"))
    o.append(ah_u(1420, 250, "var(--ink-3)", 6))
    o.append(txt(1100, 276, "SOS / EOS · 打断事件", "sm", size=15, mono=True))

    # ── ④ 下行车道（右 → 左 · 实线音频流）──
    o.append(txt(150, 310, "&#8592; 下行 · 边说", "sm", size=15, col=AC, mono=True))
    o.append(box(1106, 324, 180, 88, 6, i=4))
    o.append(txt(1196, 364, "流式 TTS", "ttl", size=21, anchor="middle"))
    o.append(txt(1196, 390, "增量合成 · 随时可截断", "sm", size=14, anchor="middle"))
    o.append(box(620, 324, 210, 88, 6, i=5))
    o.append(txt(725, 376, "语音输出", "ttl", size=22, anchor="middle"))
    o.append('<circle class="pop box" style="--i:6" cx="70" cy="368" r="38" stroke-width="1.4"/>')
    o.append('<path class="pop" style="--i:6" d="M62 358h-9v21h9l14 11V347z M83 361a9 9 0 0 1 0 15 '
             'M89 355a16 16 0 0 1 0 27" fill="none" stroke="%s" stroke-width="2.2" '
             'stroke-linecap="round" stroke-linejoin="round"/>' % AC)
    o.append(txt(70, 428, "SPK", "lbl", size=14, anchor="middle"))
    for _a, _b, _h, _k in [(1328, 1300, 1286, 5), (1106, 844, 830, 6), (620, 122, 108, 7)]:
        o.append(packet("M%d 368 H%d" % (_a, _b), _P8Q - 26, seg=26, w=13, op=".38",
                        dur="%ss" % _P8TD, delay="%.2fs" % _p8ph(1328 - _a, _P8TD), i=_k))
        o.append(hline(_a, _b, 368, AC, 2.5, _k))
        o.append(ah_l(_h, 368, AC))
    # 分叉：主路继续向左，虚线支路向下挂数字人（不在 650ms 主路上）
    o.append('<circle class="pop" style="--i:6;fill:%s" cx="1000" cy="368" r="6"/>' % AC)
    o.append(dline("M1000 374 V434", HS, 2, 6, dash="6 6"))
    o.append(ah_d(1000, 446, "var(--ink-3)", 7))
    o.append(box(850, 446, 300, 62, 6, dashed=True, i=7))
    o.append(txt(1000, 476, "数字人", "ttl", size=21, anchor="middle"))
    o.append(txt(1000, 499, "口型 / 表情 · 可选", "sm", size=14, anchor="middle"))
    o.append(txt(1170, 484, "不在 650ms 主路上", "sm", size=14, col="var(--ink-3)"))

    # ── ⑤ 两条闭环（全图的灵魂）──
    # (a) AEC 参考环：点线，从下行车道弯回 AEC —— 所以听不见自己
    #     3px 而不是 2.2px：点线本来就比实线弱一档，两个主题下都要一眼看见；
    #     标签压在弯道的「肘部」正上方（不是甩到最左），才读得出它注解的是这条线。
    o.append('<circle class="pop" style="--i:7;fill:%s" cx="560" cy="368" r="6"/>' % AD)
    _P8REF = "M560 362 C 470 320, 360 280, 300 234"
    o.append(packet(_P8REF, 300, seg=22, col=AD, w=9, op=".32", dur="2.2s", i=7, cls="mo-cycle"))
    o.append(dline(_P8REF, AD, 3, 7, dash="3 8", cls="mo-drift", sty="--mo-off:-44;--mo-dur:3.2s"))
    o.append(ah_u(300, 222, AD, 7))
    o.append(txt(372, 252, "参考信号——所以听不见自己", "sm", size=15, col=AD))
    # (b) 打断快路径：accent 粗线，从 AI-VAD 垂直直插「语音输出」，不经过 LLM
    o.append('<g class="mo-pulse" style="--mo-lo:.34;--mo-dur:2.8s">%s%s</g>'
             % (vline(700, 248, 314, AD, 5, 6), ah_d(700, 324, AD, 8)))
    o.append(txt(716, 274, "用户插话 → 340ms 收声", "ttl", size=18, col=AD, weight=700))
    o.append(txt(716, 300, "不经过 LLM", "sm", size=15, col=AD))

    # ── ⑦ 端到端计时标（只跨主路：MIC → 上行 → 中枢 → 下行 → SPK）──
    o.append(txt(500, 514, "端到端 650ms", "ttl", size=24, anchor="middle", col=AC, weight=700))
    o.append(dline("M70 528 H1498", AC, 1.6, 8, dash="3 8"))
    o.append(vline(70, 518, 538, AC, 1.6, 8))
    o.append(vline(1498, 518, 538, AC, 1.6, 8))

    # ── 三域底标 ──
    for _cx, _s in [(180, "终端设备"), (834, "声网引擎云 · 实时音频链路"),
                    (1498, "声网引擎云 · 编排与模型")]:
        o.append(txt(_cx, 560, _s, "sm", size=16, anchor="middle", col="var(--ink-3)"))

    # ── ⑥ 底座横条：SD-RTN ──
    #   这一条必须走不透明的 --card-bg-2（不是 72% 透明的 --card-bg）：
    #   content 背景板自带的 accent 细线正好在 y566–570，半透明条会让它从条里透出来，
    #   看着像条子长了半截粉色上边框。
    o.append('<rect class="pop" style="--i:8;fill:var(--card-bg-2)" x="0" y="566" '
             'width="1668" height="70" rx="8" stroke="var(--hair)" stroke-width="1.4"/>')
    o.append(txt(34, 608, "SD-RTN · 软件定义实时网", "ttl", size=24))
    o.append(ah_l(420, 601, "var(--ink-3)"))
    o.append(hline(432, 1148, 601, HS, 2, 8))
    o.append(packet("M432 601 H1148", 340, seg=20, w=9, op=".24", dur="3.4s", i=8))
    o.append(packet("M1148 601 H432", 340, seg=20, w=9, op=".24", dur="3.8s", i=8))
    o.append(ah_r(1160, 601, "var(--ink-3)"))
    o.append(txt(1634, 608, "端 ↔ 云 双向音频流", "sm", size=16, anchor="end"))

    # ── ⑧ 图例行（figbox 底内 · 与 land 分层）──
    o.append(hline(0, 40, 649, AC, 2.5, 9))
    o.append(txt(50, 654, "音频流", "sm", size=14))
    o.append(dline("M150 649 H190", HS, 2, 9, dash="6 5"))
    o.append(txt(200, 654, "事件 / 控制", "sm", size=14))
    o.append(dline("M340 649 H380", AD, 2.2, 9, dash="2 6"))
    o.append(txt(390, 654, "AEC 参考", "sm", size=14))
    o.append(hline(520, 560, 649, AD, 5, 9))
    o.append(txt(570, 654, "打断快路径", "sm", size=14))

    # ── ⑨ 三数章锚点（2026-08-23 三数章重构 · 只做加法）────────────────────────
    #   P5 亮出 650 / 340 / 95%，P6–P9 逐个拆开，本页收束 —— 三枚 chip 就是「拆过的
    #   那三件事，在这张图上的位置」。**大图几何一格没动**：三枚 chip 全部落在实测空白位，
    #   三处落点各有各的道理（改这三行之前先把这三段读完）：
    #     ① 650MS → x392 y446（端到端计时标「端到端 650ms」正上方 12px）。
    #        650 讲的是**整条主路的跨度**，它的图形依据就是下面那条 M70 528 H1498 的跨度线；
    #        chip 压在跨度线的正上方、标签文字之上一档，读者的视线是「chip → 标签 → 跨度线」。
    #        为什么不放跨度线左端：左端 x70 紧邻 MIC 圆与 SPK 圆，chip 一放就把入口挡住。
    #     ② 340MS → x578 y258（打断快路径竖线 x700 的左侧 20px）。
    #        340 讲的是**打断**，全图唯一一条打断证据就是那根从 AI-VAD 垂直插进「语音输出」
    #        的 accent-deep 粗线。右侧 x716 已经坐着「用户插话 → 340ms 收声 / 不经过 LLM」
    #        两行注，所以 chip 走左侧：上距 AI-VAD 盒底 14px、下距「语音输出」盒顶 34px，
    #        左侧那条 AEC 参考曲线在这一带只走到 x≈390，与 chip 左缘还差 188px。
    #     ③ 95% → x382 y92（SAL 声纹锁定盒正上方 8px）。
    #        95% 讲的是**环境干扰屏蔽**，图上对应的是上行车道第二只盒「SAL 声纹锁定」。
    #        盒的左右两侧都被车道箭头占着（x340–382 / x592–634），上方那条带是全图最空的
    #        一段（顶部控制面在 y66 收尾、车道盒从 y132 起），chip 正好落进去；
    #        左边 21px 外是 x361 那条域分隔虚线，不相碰。
    for _ax, _ay, _an, _al in [(392, 446, 1, "650MS"), (578, 258, 2, "340MS"), (382, 92, 3, "95%")]:
        o.append(_anchor_chip(_ax, _ay, _an, _al))
    return "".join(o)

page("content", "".join([
    # 2026-08-23 采纳项 F · kicker 消歧：本页（引擎内部数据流 · 今 P10）与 P14（客户接入架构）
    # 原来两页 kicker 都以 ARCHITECTURE 起手，翻页时读起来像同一张图的两个版本。
    # 各补一段限定词把「谁的架构」说死。**只动 kicker 一行，标题与大图一个像素不碰。**
    # 三数章重构轮 kicker 维持上轮刚定的这一句（它不绑数字：本页收的是三个数字的**总账**）。
    head("PRODUCT ARCHITECTURE · ENGINE INTERNALS · 运行时内部链路 · FULL-DUPLEX × AI-VAD",
         "<strong>一张图</strong>，看懂全双工引擎。"),
    lab(120, 246, "01 · ONE PICTURE · 上行 / 中枢 / 下行 · 两条闭环"),
    figbox(120, 282, 1680, 1680, 660, _bigmap(), i=1),
    land("听的车道永不关闭，说的车道随时让行——中间站着 AI-VAD。", y=944),
    # 章尾收束句（2026-08-23 三数章重构）：与 land 同一条基线的右半区 ——
    # land 的墨迹实占 ≈750px（29px × 20 余字 + 26px 内边距），x1080 起本来就是空的。
    # 右对齐 26px 与 land 的 29px 差一档：它是章的落款，不跟 land 抢主句的位置。
    sh("flow", "left:1080px;top:958px;width:720px;height:44px;text-align:right;"
       "font:700 26px/1.5 var(--f-cn);color:var(--ink-2);--i:7",
       "<strong style='color:var(--accent)'>三件极致</strong>，都在这张图上。"),
    # 2026-08-23 采纳项 C：本页是一张机理大图，**没有自己的样本或时间窗**（数字全部
    # 回指 P5 的公开口径）⇒ 样本段留空，缺口已记入交付报告。
    # 2026-08-23 三数章重构后，三个数字不再只由 P5 一页交代：P5 亮数 + P6/P7/P8/P9 逐页拆，
    # 本页是章尾收束。指回单页 P5 会把读者送到只有三张数字卡的目录页，正文全在后面四页。
    src("SOURCE · 引擎发版说明 / TEN ECOSYSTEM · 打断/延时口径见 P5–P9 · 事实截止 2026.08", i=9),
]))

# ═══ P11 · 弱网 ·「网络在抖，对话不断」══════════════════════════════════════
# 2026-08-20 三轮升维：一条丢包条 + 一条波浪 → 上下两条对齐的时间带。
#   上带 = 网络状况（正常 → 80% 丢包高密段 → 3–5s 瞬时断网空洞段 → 恢复），
#   下带 = 对话连续性（一条永不中断的音频带，在上带最恶劣区间下方依然连续）。
# 2026-08-21 重做 · 补「AI QoS」机理：
#   旧版中间只坐着一个「抗丢包引擎」黑盒 —— 它解释得了 80% 丢包，解释不了「断网 3–5s
#   还能继续说话」（丢包可以靠冗余补，断网时根本没有包可补）。新版把机制层拆成两个盒，
#   各自对位自己的战场，并且把 AI QoS 的机理画出来：
#     ① 抗丢包引擎（对位 80% 丢包段）· 常规盒 · FEC 前向纠错等冗余手段
#     ② AI QoS · 断网续播（对位断网空洞段）· 本页唯一 hot
#        机理 = 下行 AI 语音包「密集流」持续注入「本地缓存」蓄水条；断网段没有新包进来，
#        缓存条递减放水，下带播放依旧连续；恢复后重新充盈。
#        why 注是 Colin 原话定稿：AI 的语音包幅度与频率远大于人，网络好时多下发的包，
#        够断网时继续播 —— 这一句是本页真正的「因果标注」。
#   两枚数字（80% / 3–5s）与 land 原样，不发明第三个。
_WN_SEGS = [(0, 9, 1), (256, 10, 8), (536, 6, 6), (716, 12, 1)]   # (x0, 包数, 丢包数)
_WN_LOSS = (250, 262)      # 丢包域（x, w）—— 与 seg2 的包条 256–508 对齐
_WN_DARK = (526, 164)      # 断网域（x, w）—— 与 seg3 的空洞 536–676 对齐
def _weaknet_fig():
    o = [txt(0, 18, "网络 · 大量丢包 + 瞬时断网", "lbl", size=15)]
    # ── 域分带（P8 语法）：两段战场从上带一路贯到机制盒，「谁治谁」不用连线也读得出 ──
    o.append('<rect class="pop" style="--i:1;fill:%s;opacity:.055" x="%d" y="28" width="%d" '
             'height="318" rx="6"/>' % (AD, _WN_LOSS[0], _WN_LOSS[1]))
    o.append('<rect class="pop" style="--i:1;fill:%s;opacity:.10" x="%d" y="28" width="%d" '
             'height="318" rx="6"/>' % (AC, _WN_DARK[0], _WN_DARK[1]))
    for x0, n, lost in _WN_SEGS:
        for k in range(n):
            x = x0 + k * 28
            if k < n - lost:
                o.append('<rect class="pop" style="--i:%d;fill:%s" x="%d" y="32" width="22" '
                         'height="60" rx="5"/>' % (1 + k % 3, AC, x))
            else:
                o.append('<rect class="pop" style="--i:%d" x="%d" y="32" width="22" height="60" '
                         'rx="5" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 4"/>'
                         % (1 + k % 3, x, HS))
    o.append(txt(592, 70, "✕", "ttl mo-pulse", size=19, anchor="end", col=AD,
                 sty="--mo-dur:2.2s"))
    o.append(txt(597, 70, "断网", "ttl", size=19, col=AD))
    o.append(txt(382, 114, "80% 丢包", "ttl", size=20, anchor="middle", col=AD, weight=700))
    o.append(txt(606, 114, "3–5s 瞬时断网", "ttl", size=20, anchor="middle", col=AD, weight=700))
    # ── 下行 AI 语音包密集流：注入缓存的那一场雨；断网段（526–690）没有雨 ──
    o.append(txt(0, 112, "下行 AI 语音包 · 密集下发", "lbl", size=14))
    for k in range(31):
        x = 120 + k * 30
        if 512 <= x <= 700:
            continue
        o.append(dline("M%d 128 V158" % x, AC, 2, 2, dash="30 30", cls="mo-drift",
                       sty="--mo-off:-60;--mo-dur:1.1s;--mo-del:-%.2fs" % (0.16 * (k % 7))))
        o.append(ah_d(x, 168, AC, 7))
    # ── 本地缓存：蓄水条。正常段充盈 → 断网段递减放水 → 恢复后重新充盈 ──
    o.append(txt(0, 210, "本地缓存", "lbl", size=15))
    o.append('<rect class="pop" style="--i:3" x="110" y="176" width="914" height="56" rx="8" '
             'fill="none" stroke="%s" stroke-width="1.4"/>' % HS)
    o.append('<path class="pop mo-pulse" style="--i:3;--mo-hi:.26;--mo-lo:.14;--mo-dur:4.4s;'
             'fill:%s;opacity:.26" d="M114 228 L114 182 L526 182 '
             'L690 224 L764 182 L1020 182 L1020 228 Z"/>' % AC)
    # ── 机制层：两个盒各占自己的域（左右各贴着域边，不用连线） ──
    o.append(box(_WN_LOSS[0], 250, _WN_LOSS[1], 96, 10, i=4))
    o.append(txt(_WN_LOSS[0] + _WN_LOSS[1] // 2, 292, "抗丢包引擎", "ttl", size=25, anchor="middle"))
    o.append(txt(_WN_LOSS[0] + _WN_LOSS[1] // 2, 322, "FEC 前向纠错等 · 冗余对抗丢包", "sm", size=14,
                 anchor="middle"))
    o.append(box(_WN_DARK[0], 250, _WN_DARK[1], 96, 10, hot=True, i=5))
    o.append(txt(_WN_DARK[0] + _WN_DARK[1] // 2, 288, "AI QoS", "sm", size=18, anchor="middle",
                 col=AC, mono=True, ls=".12em"))
    o.append(txt(_WN_DARK[0] + _WN_DARK[1] // 2, 324, "断网续播", "ttl", size=24, anchor="middle",
                 col=AC, weight=700))
    # ── why 注（Colin 原话定稿）：AI QoS 为什么可能 ──
    o.append('<rect class="pop" style="--i:6;fill:%s" x="720" y="254" width="3" height="88" rx="2"/>' % AC)
    o.append(txt(742, 288, "AI 说话的语音包幅度与频率远大于人——", "sm", size=16))
    o.append(txt(742, 318, "网络好时多下发的包，够断网时继续播。", "sm", size=16))
    # ── 下带：一条连续不断的音频带，横贯全程 ──
    o.append(txt(0, 386, "对话 · 连续不卡顿", "ttl", size=21, col=AC))
    o.append('<rect class="pop" style="--i:7;fill:%s;opacity:.14" x="0" y="398" width="1024" '
             'height="56" rx="8"/>' % AC)
    _P11W = ("M12 426 Q 72 396 132 426 T 252 426 T 372 426 T 492 426 T 612 426 T 732 426 "
             "T 852 426 T 972 426 T 1012 426")
    o.append(packet(_P11W, 380, seg=30, w=13, op=".26", dur="3s", i=7))
    o.append('<path class="dw" style="--len:1200;--i:7" d="%s" fill="none" '
             'stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (_P11W, AC))
    o.append('<circle class="pop" style="--i:8;fill:%s" cx="1016" cy="426" r="7"/>' % AC)
    o.append(legend(0, 486, [("solid", "音频流 · 语音包"), ("dash", "丢包 / 断网"),
                             ("fill", "本地缓存余量")]))
    return "".join(o)
_P7STAT = [("80", "%", "丢包率下稳定对话"), ("3–5", "s", "瞬时断网自如响应")]
page("content", "".join([
    head("WEAK NETWORK · 弱网也能聊", "网络在抖，<strong>对话不断</strong>。"),
    lab(120, 236, "01 · PACKET LOSS · AI QoS", w=1080),
    figbox(120, 280, 1080, 1080, 510, _weaknet_fig(), i=1),
    lab(1280, 236, "02 · RESILIENCE", w=520),
    ] + [
    sh("rise card-c", "left:1280px;top:%dpx;width:520px;height:230px;--i:%d" % (300 + _i * 260, 2 + _i),
       '<div style="padding:36px 40px;height:100%%;display:flex;flex-direction:column;justify-content:center">'
       '<div style="font:900 92px/.92 var(--f-en);letter-spacing:-.035em;color:var(--accent)">'
       '%s<span style="font-size:.42em;letter-spacing:0">%s</span></div>'
       '<div style="margin-top:18px;font:400 22px/1.4 var(--f-cn);color:var(--ink-2)">%s</div></div>'
       % (_v, _u, _l))
    for _i, (_v, _u, _l) in enumerate(_P7STAT)
    ] + [
    rule(850),
    # land 收窄到 1000，右侧让出 SOURCE 行（同一基线两栏，照 convoai-info P8 的做法），
    # 这样 land 仍落在全 deck 统一的 y988 基线上，翻页时那根 accent 竖条不跳。
    land("极端弱网、瞬时断网也不掉线——移动、车载、户外场景，对话依旧顺畅。", w=1000),
    src(_SRC_TYP, y=1010, x=1010, w=790, align="right"),
]))

# ═══ P12 · 多模态 ·「看得见、认得人的多模态对话」════════════════════════════
# 2026-08-21 改造 · 聚焦视觉模态：
#   标题与中心 hub 保留；辐条重新配重 —— 四条等粗辐条读起来是「四件并列的功能」，
#   而全 deck 的叙事此刻要往 Physical AI（今 P19）走，视觉这一路才是引子。
#     加重（大卡 + 粗线 3.5）：IN 看图识景（端点例 智能眼镜）／ OUT 数字人（端点 语音配合数字人表达）
#     弱化（小 chip + 灰细线 1.6）：声纹锁定（P10 已讲）／ SIP 电话 · VoIP（前序已讲），
#       降为底部次级带并挂 mono 小注「前文已述」——不删，只降权重。
#   线型只有一种（实线 = 主数据流），主次靠「粗细 + 灰度」分，图例跟着降级列两档。
def _p12_card(x, y, w, h, tag, name, desc, i=2, hot=False):
    o = [box(x, y, w, h, 12, hot=hot, i=i)]
    o.append(txt(x + 30, y + 40, tag, "lbl", size=14))
    o.append(txt(x + 30, y + 92, name, "ttl", size=34, col=AC if hot else None))
    o.append(txt(x + 30, y + 132, desc, "sm", size=20))
    return "".join(o)
def _p12_chip(x, y, w, name, i=5, on=False):
    """端点 chip。on=True 是加重辐条的端点（accent 描边 + 主墨字），
       on=False 是次级带的弱化件（灰描边 + 灰字）—— 两者必须区分开，
       否则「端点例」和「前文已述」看起来是同一个重量级，配重就白做了。"""
    return ("".join([
        '<rect class="pop" style="--i:%d" x="%d" y="%d" width="%d" height="56" rx="28" '
        'fill="none" stroke="%s" stroke-width="%s"/>' % (i, x, y, w, AC if on else HS,
                                                        1.8 if on else 1.4),
        txt(x + w // 2, y + 36, name, "sm", size=19, anchor="middle",
            col="var(--ink-2)" if on else "var(--ink-3)")]))
def _io_fig():
    o = []
    # ── 中心 hub（hot）· 尺寸与三轮版一致，整体上提一档收掉图顶那条空带 ──
    o.append(halo_rect(630, 85, 420, 140, 14, sc="1.05", op=".3", dur="3.4s"))
    o.append(box(630, 85, 420, 140, 14, hot=True, i=1, cls="mo-breathe", sty="--mo-dur:3.4s"))
    o.append(txt(840, 145, "对话引擎", "ttl", size=38, anchor="middle"))
    o.append(txt(840, 187, "一套接入", "sm", size=18, anchor="middle", col=AC, mono=True, ls=".16em"))
    # ── 左：感知 · IN（加重）· 端点设备 → 能力大卡 → 引擎 ──
    o.append(txt(20, 30, "感知 · IN", "sm", size=15, col=AC, mono=True, ls=".18em"))
    o.append(_p12_chip(20, 127, 180, "智能眼镜", i=2, on=True))
    o.append(packet("M200 155 H236", 36, seg=16, w=11, op=".34", dur="0.65s", i=2))
    o.append(hline(200, 236, 155, AC, 3.5, 2)); o.append(ah_r(248, 155, AC, 7))
    o.append(_p12_card(256, 70, 316, 170, "VISION", "看图识景", "理解图片视频", i=2))
    o.append(packet("M572 155 H610", 38, seg=16, w=11, op=".34", dur="0.68s", i=3))
    o.append(hline(572, 610, 155, AC, 3.5, 3)); o.append(ah_r(622, 155, AC))
    # ── 右：表达 · OUT（加重）· 引擎 → 能力大卡 → 表达端点 ──
    o.append(txt(1660, 30, "表达 · OUT", "sm", size=15, col=AC, anchor="end", mono=True, ls=".18em"))
    o.append(packet("M1050 155 H1090", 40, seg=16, w=11, op=".34", dur="0.7s", i=3))
    o.append(hline(1050, 1090, 155, AC, 3.5, 3)); o.append(ah_r(1102, 155, AC))
    o.append(_p12_card(1110, 70, 316, 170, "AVATAR", "数字人", "口型表情同步", i=2))
    o.append(packet("M1426 155 H1448", 22, seg=14, w=11, op=".34", dur="0.5s", i=4))
    o.append(hline(1426, 1448, 155, AC, 3.5, 4)); o.append(ah_r(1460, 155, AC, 7))
    o.append(_p12_chip(1468, 127, 212, "语音配合数字人表达", i=4, on=True))
    # ── 底：次级带（弱化）· 前文已述 ──
    o.append(vline(840, 225, 277, "var(--ink-3)", 1.6, 5))
    o.append(hline(600, 1080, 277, "var(--ink-3)", 1.6, 5))
    o.append(txt(840, 306, "前文已述", "sm", size=14, anchor="middle", col="var(--ink-3)",
                 mono=True, ls=".16em"))
    for cx, w, n in [(600, 220, "声纹锁定"), (1080, 260, "SIP 电话 / VoIP")]:
        o.append(vline(cx, 277, 314, "var(--ink-3)", 1.6, 5))
        o.append(_p12_chip(cx - w // 2, 316, w, n, i=6))
    o.append(legend(0, 424, [("solid", "本页重点模态", 3.5),
                             ("solid", "前文已述 · 次级", 1.6, "var(--ink-3)")]))
    return "".join(o)
page("content", "".join([
    head("BEYOND VOICE · 不止于听清", "看得见、认得人的<strong>多模态对话</strong>。"),
    lab(120, 236, "01 · SEE & SPEAK"),
    figbox(120, 292, 1680, 1680, 450, _io_fig(), i=1),
    rule(850),
    land("同一套引擎，看得见、说得出——让对话，走出屏幕。"),
]))

# ═══ P13 · 开放编排 ·「你的模型自由组合，引擎负责编排」（页号 13→15→14→13）══
_MODELS = ["ASR 语音识别", "LLM 大模型", "TTS 语音合成", "数字人"]
_ADDONS = ["视觉理解", "知识库 · RAG"]   # 产品口径：知识库 RAG 是一项能力，不拆
# 2026-08-20 三轮升维：两列盒子 + 曲线 → 一台「插槽机」。
# 2026-08-21「箭头语义修」（Colin：箭头流向会让大家懵逼）——见文件头的诊断与修法。
#   插槽语义只保留一种阅读方向：模块「插入」引擎。
#     · 左右两列的连线一律指向引擎（左列指右、右列指左 ⇒ 全部收敛到中心，不可能被读成穿流）
#     · 贝塞尔全删，改正交总线：每个槽出一条短支线汇到列总线，总线一条主干进引擎（不交叉）
#     · ⇄ 换装件移到模块块「上方」，小号 + 灰度（注记语域，不与流向线抢重量）
#     · 引擎 → 发布带改成无箭头细连线：它是引擎的附属说明，不是第三种流向
#   同屏箭头语义共 2 种（插入 / 换装），图例逐条对上；线型 2 种（实线主链 / 虚线按需）。
def _slot(x, y, w, h, name, i=1, dashed=False):
    """插槽：槽框（可虚线）+ 内模块块 + 块上方的 ⇄ 换装小件（灰、小号 = 注记，不是流向）"""
    o = [box(x, y, w, h, 8, dashed=dashed, i=i)]
    o.append('<rect class="pop" style="--i:%d;fill:var(--card-bg-2)" x="%d" y="%d" width="%d" '
             'height="%d" rx="6" stroke="%s" stroke-width="1.4"/>'
             % (i, x + 14, y + 12, w - 28, h - 24, HS))
    o.append(txt(x + w // 2, y + h // 2 + 8, name, "ttl", size=22, anchor="middle"))
    o.append(swap_mark(x + w - 46, y - 14, i=i,
                       sty="--mo-lo:.5;--mo-dur:5.4s;--mo-del:-%.1fs" % (0.9 * i)))
    return "".join(o)
def _orch_fig():
    o = [txt(250, 26, "可自由替换 · 模型层", "lbl", size=16, anchor="middle", col=AC),
         txt(1430, 26, "按需叠加 · 高阶能力", "lbl", size=16, anchor="middle", col=AC)]
    # ── 左列：四个模型槽 → 支线汇到 x540 总线 → 一条主干进引擎（唯一一枚箭头落在引擎口）──
    _LY = [60, 168, 276, 384]
    for i, n in enumerate(_MODELS):
        y = _LY[i]
        o.append(_slot(60, y, 380, 68, n, i=i + 1))
        o.append(packet("M440 %d H528" % (y + 34), 88, seg=18, w=10, op=".32", dur="1.06s", i=i + 2))
        o.append(hline(440, 528, y + 34, AC, 2, i + 2)); o.append(ah_r(540, y + 34, AC, 7))
    o.append(vline(540, _LY[0] + 34, _LY[3] + 34, AC, 2, 5))
    o.append(packet("M540 260 H606", 66, seg=18, w=11, op=".32", dur="0.84s", i=5))
    o.append(hline(540, 606, 260, AC, 2.5, 5)); o.append(ah_r(618, 260, AC))
    # 集体括号：四个槽共享的一条产品承诺
    o.append(hline(60, 440, 472, AC, 2, 6))
    o.append(vline(60, 460, 472, AC, 2, 6)); o.append(vline(440, 460, 472, AC, 2, 6))
    o.append(txt(250, 502, "可替换 · 可兜底 · 可热切换", "sm", size=18, anchor="middle", col=AC,
                 weight=700))
    # 中枢（唯一 hot 件）
    o.append(halo_rect(620, 180, 440, 160, 16, sc="1.05", op=".3", dur="3.6s"))
    o.append(box(620, 180, 440, 160, 16, hot=True, i=0, cls="mo-breathe", sty="--mo-dur:3.6s"))
    o.append(txt(840, 250, "对话引擎", "ttl", size=36, anchor="middle", col=AC))
    o.append(txt(840, 296, "实时编排", "txt", size=21, anchor="middle"))
    # ── 右列：两个高阶槽（虚线 = 按需）→ 支线汇到 x1140 总线 → 主干「向左」进引擎 ──
    _RY = [168, 296]
    for i, n in enumerate(_ADDONS):
        y = _RY[i]
        o.append(_slot(1240, y, 380, 68, n, i=i + 3, dashed=True))
        o.append(packet("M1240 %d H1152" % (y + 34), 88, seg=18, w=10, op=".32", dur="1.06s", i=i + 3))
        o.append(dline("M1240 %d H1152" % (y + 34), AC, 2, i + 3, dash="7 6"))
        o.append(ah_l(1140, y + 34, AC, 7))
    o.append(dline("M1140 %d V%d" % (_RY[0] + 34, _RY[1] + 34), AC, 2, 5, dash="7 6"))
    o.append(packet("M1140 260 H1086", 54, seg=16, w=11, op=".32", dur="0.7s", i=5))
    o.append(dline("M1140 260 H1086", AC, 2.5, 5, dash="7 6")); o.append(ah_l(1074, 260, AC))
    # 底部小流程带：无箭头细连线（附属说明，不是第三种流向）
    o.append(vline(840, 348, 398, HS, 1.4, 6))
    o.append('<rect class="pop" style="--i:7;fill:var(--card-bg-2)" x="620" y="400" width="440" '
             'height="60" rx="30" stroke="%s" stroke-width="1.4"/>' % HS)
    o.append(txt(840, 438, "实时调试 &#8594; 一键发布", "ttl", size=22, anchor="middle"))
    # 图例第 2 条必须显式给 accent：右列的按需插入线是 accent 虚线，
    # 而 lg_dash 默认取 hair-strong 灰 —— 不给色，图例样线会和页内真线不同色。
    o.append(legend(0, 530, [("solid", "插入 · 指向引擎"), ("dash", "按需插入 · 高阶能力", 2, AC),
                             ("swap", "可替换 · 换装")]))
    return "".join(o)
page("content", "".join([
    head("OPEN & FLEXIBLE · 灵活扩展", "你的模型自由组合，<strong>引擎负责编排</strong>。"),
    lab(120, 236, "01 · ORCHESTRATION"),
    figbox(120, 272, 1680, 1680, 545, _orch_fig(), i=1),
    rule(850),
    land("快速编排 ASR / LLM / TTS / 数字人与语音体验，实时调试、一键发布智能体。"),
]))

# ═══ P14 · 接入架构 ·「2 行代码，三方协同即可上线」（页号 14→16→15→14）═════
def _arch_fig():
    o = []
    # ── 2026-08-20 三轮：与 P8 对齐的一致性 pass ──
    #   ① 三方之间加细虚线域分隔（实线会跟舞台底纹的竖 hairline 撞成同一种东西）
    #   ② 域底标用 P8 同一套词：终端设备 / 客户业务服务器 / 声网引擎云
    #   ③ 线型统一：媒体走实线 accent，REST / Token 走虚线（事件 · 控制语域）+ 迷你图例
    # ── 2026-08-20 四轮：三条并置的静态线 → 带序号的「握手时序」───────────────
    #   ① 取 Token（终端 → 客户服务器 · 虚线）+ 服务端签名，why 标注「密钥不下发终端」
    #   ② 创建 / 控制智能体（客户服务器 → 引擎 · 虚线 REST 控制面）
    #   ③ 实时音视频流（终端 ⇄ 引擎 · 实线双向 · 比家族实线 2.5 粗一档 = 3.5）
    #   版面即时序：①② 走盒顶（左 → 右），③ 走盒底横贯全宽 —— 读序天然是
    #   「左上 → 右上 → 底部全宽」，③ 在空间上就落在 ①② 之后，不用画时间轴也读得出先后。
    #   ①② 的横跑道压在 y58（盒顶 y120 之上），域分隔从 y100 起，两者不相交 ⇒ 域线可以整条不断开
    #   （三轮那次要在 y236–274 断开，是因为「取 Token」标签正压在域线上，成了划掉的观感）。
    o += [dline("M555 100 V500", HS, 1, 0, dash="3 9"),
          dline("M1125 100 V500", HS, 1, 0, dash="3 9")]
    for _cx, _s in [(270, "终端设备"), (840, "客户业务服务器"), (1410, "声网引擎云")]:
        o.append(txt(_cx, 530, _s, "sm", size=16, anchor="middle", col="var(--ink-3)"))
    o.append(legend(0, 566, [("solid", "实时音视频流", 3.5), ("dash", "REST · Token")]))
    # ① 终端设备
    o.append(box(40, 120, 460, 300, 14, i=1))
    o.append(txt(72, 176, "终端设备", "ttl", size=26))
    o.append(txt(72, 224, "App / 智能硬件 / Web", "sm", size=18))
    o.append(box(72, 250, 396, 56, 10, hot=True, i=2))
    o.append(txt(270, 286, "集成声网 SDK", "ttl", size=21, anchor="middle", col=AC))
    o.append(txt(72, 352, "采集人声 · 播放语音 / 数字人", "lbl", size=15))
    # ② 客户业务服务器
    o.append(box(610, 120, 460, 300, 14, i=3))
    o.append(txt(642, 176, "客户业务服务器", "ttl", size=26))
    for k, s in enumerate(["· 鉴权签名，密钥不下发终端", "· 创建 / 控制智能体", "· 业务逻辑 · 知识库"]):
        o.append(txt(642, 228 + k * 38, s, "sm", size=18))
    o.append(txt(642, 386, "通过 REST 调用引擎", "lbl", size=15))
    # ③ 声网对话式 AI 引擎
    o.append(box(1180, 120, 460, 300, 14, hot=True, i=4))
    o.append(txt(1212, 176, "声网对话式 AI 引擎", "ttl", size=26, col=AC))
    for k, s in enumerate(["ASR", "LLM", "TTS", "数字人"]):
        bx, by = 1212 + (k % 2) * 202, 210 + (k // 2) * 66
        o.append(box(bx, by, 186, 52, 8, i=5))
        o.append(txt(bx + 93, by + 34, s, "sm", size=19, anchor="middle"))
    o.append(txt(1212, 386, "实时编排 · 低延时传输", "lbl", size=15))
    # ── step1：三步握手依次亮起 ──
    #   家族的 build 机制是「一步 = 一整层」，所以三步握手仍然是同一步整层推上来：
    #   讲者先摆三个盒子说清「谁是谁」，再一步把 ①②③ 连同序号徽标一起推上来，
    #   顺序由版面（左上 → 右上 → 底部全宽）与徽标数字承担，不拆成三个 data-step。
    o.append('<g data-step="1">')
    # ① 取 Token（终端 → 客户服务器 · 虚线事件/控制语域）
    #   不能用 .lbl —— 它带 text-transform:uppercase，会把「取 Token」烧成「取 TOKEN」，与原稿不符
    o.append(dline("M270 120 V58 H790 V110", HS, 2, 2, dash="6 6"))
    o.append(ah_d(790, 118, "var(--ink-3)", 6))
    o.append(txt(530, 32, "取 Token · 服务端签名", "sm", size=18, anchor="middle"))
    # why 标注（P8「参考信号——所以听不见自己」同款语域）：钉在 ① 正下方，回答「为什么要绕这一趟」
    o.append(txt(530, 94, "密钥不下发终端", "sm", size=15, anchor="middle", col="var(--ink-3)"))
    o.append(step_badge(530, 58, 1, i=2, halo="0s"))
    # ② 创建 / 控制智能体（客户服务器 → 引擎 · 虚线 REST 控制面）
    #   起点 x890 与 ① 的落点 x790 同在服务器盒顶：一收一发，服务器是这一步的枢纽
    o.append(dline("M890 120 V58 H1410 V110", HS, 2, 3, dash="6 6"))
    o.append(ah_d(1410, 118, "var(--ink-3)", 6))
    o.append(txt(1150, 32, "创建 / 控制智能体", "sm", size=18, anchor="middle"))
    o.append(step_badge(1150, 58, 2, i=3, halo="1.2s"))
    # ③ 实时音视频流（终端 ⇄ 引擎 · 实线双向 · 粗一档）—— 建立在 ①② 之后，所以走盒底
    _P15M = "M270 434 V478 H1410 V434"
    o.append(packet(_P15M, 420, seg=30, w=12, op=".28", dur="3.2s", i=4))
    o.append(packet(_P15M, 420, seg=30, w=12, op=".28", dur="3.6s", i=4, rev=True))
    o.append('<path class="dw" style="--len:1228;--i:4" d="%s" '
             'fill="none" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/>' % (_P15M, AC))
    o.append(ah_u(270, 424, AC))
    o.append(ah_u(1410, 424, AC))
    o.append(txt(840, 452, "实时音视频流", "ttl", size=19, anchor="middle", col=AC, weight=700))
    o.append(step_badge(840, 478, 3, i=5, halo="2.4s"))
    o.append('</g>')
    return "".join(o)
page("content", "".join([
    # 2026-08-23 采纳项 F · kicker 消歧（与 P8 成对改）：补「客户」这个限定词 ——
    # 本页画的是客户侧三方怎么接进来，不是引擎内部怎么跑。原「接入架构」被
    # 「客户接入架构」整段吸收，不重复挂两遍。**只动 kicker 一行，标题与图零触碰。**
    head("ARCHITECTURE · INTEGRATION · 客户接入架构", "<strong>2 行代码</strong>，三方协同即可上线。"),
    lab(120, 236, "01 · THREE PARTIES"),
    # viewBox 556→578、盒顶 280→266：③ 的盒底跑道要在「三盒底缘 / 域底标 / 图例」之间
    # 各留出 10px 以上的呼吸（原 556 里只剩 6px，徽标贴着域底标）。
    # 盒底 266+578=844，仍压在 rule(850) 之上，不碰收口线。
    figbox(120, 266, 1680, 1680, 578, _arch_fig(), i=1),
    rule(850),
    land("终端只管采集与播放，密钥与业务逻辑留在你的服务器——2 行代码、15 分钟即可跑通，安全可控、上线快。"),
]), steps=1)

# ═══ P15 · 典型场景 ·「一套引擎，支撑多类场景」（页号 15→17→16→15）═════════
_SCENES = [
    ("01 · OUTBOUND", "AI 外呼",   "客服、营销、风控、调研、关怀通知，成本效率全面提升。"),
    ("02 · DEVICE",   "智能硬件",  "嵌入设备，让设备开口说话，语音控制与智能陪伴。"),
    ("03 · COMPANION", "虚拟陪伴", "情感化对话与互动，24 小时无缝语音陪伴。"),
    ("04 · TUTOR",    "口语陪练",  "模拟真实对话场景，实时反馈与纠正。"),
    ("05 · SERVICE",  "智能客服",  "代替人工坐席，7×24 小时无等候即时响应。"),
    ("06 · MORE",     "更多场景",  "语音助手、教育、金融、政企……按业务快速落地。"),
]
page("content", "".join([
    head("SCENARIOS · 典型场景", "一套引擎，<strong>支撑多类场景</strong>。"),
    lab(120, 236, "01 · SIX SCENARIOS"),
    sh("", "left:120px;top:274px;width:1680px;height:536px",
       '<div class="g3" style="height:100%">' + "".join(
           '<div class="card rise" style="--i:%d;justify-content:center"><div class="tag">%s</div>'
           '<div class="t" style="font-size:30px">%s</div>'
           '<div class="d" style="font-size:19px">%s</div></div>'
           % (2 + _i, _t, _n, _d)
           for _i, (_t, _n, _d) in enumerate(_SCENES)) + '</div>'),
    rule(850),
    rail("AI OUTBOUND · SMART DEVICE · COMPANION · SPEAKING TUTOR · CUSTOMER SERVICE · MORE"),
]))

# ═══ P16 · Call Agent 登场 · 成绩单（2026-08-21「Call Agent 章」新增 ◆）════
#   Colin 的章序指令：场景（P15）之后接 Call Agent 三页，Call Agent 之后才接 R1（P19）。
#   文案全部来自声网 Call Agent 官网定稿（Colin 已逐字核过）——只排版、不改写、不外推。
#   本章三页共用的红线（改稿之前先读这四条）：
#     · 不出现任何价格数字（商务数字易变；「1/3 成本」的定性表述已经覆盖这层意思）
#     · 不出现 staging URL、不出现四位智能体的人名 / 头像
#     · 96.5% 的注必须钉住「盲测 32,000 名真实客户」口径 —— 它与 convoai-info P5 的
#       「2,475 通生产数据」是两个**不同数据集**，混写就是造假
#     · 数字只用官网已有的四个（96.5% / 32,000 / 1,000+ / 150 / 1/3），不发明第五个
#   hot 卡 = 96.5%：任务书逐项标注的「——hot」落在它身上，P17 的收口 mono 也回指这一枚
#   （所以没有把 hot 给中间那张卡 —— 三页里只有这一个数字被后一页当论据引用）。
_CA_SRC = "SOURCE · 声网 CALL AGENT 官网 · 外呼智能体 · 事实截止 2026.08"
_CA_STAT = [
    ("01 · TURING", "96.5%", "的客户听不出 TA 是 AI",
     "盲测 32,000 名真实客户：每 100 人里，只有不到 4 人听出对面是 AI", True),
    ("02 · THROUGHPUT", "1,000+", "通 / 天 · 多路并发",
     "真人销冠约 150 通——TA 的一天 = 销冠的一周", False),
    ("03 · COST", "1/3", "成本",
     "用三分之一的成本，实现一支销冠团队的产能", False),
]
_CA_DIFF = [
    ("状态", "会累、会烦躁", "第 10,000 通依旧满格"),
    ("合规", "即兴发挥，难管控", "句句过审，全程可质检"),
    ("沉淀", "离职即清零", "一处进化，全队同步"),
]
page("content", "".join([
    head("CALL AGENT · 企业级智能体 · AI 外呼",
         "Agent 替你打电话，<strong>把线索聊成订单</strong>。"),
    sh("flow sub", "left:120px;top:246px;width:1680px;height:42px;--i:1",
       "给 Agent 一份客户名单，剩下的交给 TA：懂沟通、能应变、擅转化。"),
    lab(120, 306, "01 · SCORECARD"),
    ] + [
    # 三张成绩单卡：数字 → 说明 → 注。注走 margin-top:auto 钉在卡底 ⇒ 三张卡的注共一条基线，
    # 卡高（270）因此不用迁就最长的那条注 —— 注长一行短一行都不会把上面的大字顶下去。
    sh("rise card-c%s" % (" on" if _on else ""),
       "left:%dpx;top:340px;width:540px;height:270px;--i:%d" % (120 + _i * 570, 2 + _i),
       '<div style="padding:28px 30px;height:100%%;display:flex;flex-direction:column">'
       '<div style="font:500 14px/1 var(--f-mono);letter-spacing:.18em;color:%s">%s</div>'
       '<div style="margin-top:16px;font:900 70px/.92 var(--f-en);letter-spacing:-.035em;'
       'color:var(--accent)">%s</div>'
       '<div style="margin-top:12px;font:700 26px/1.3 var(--f-cn);color:var(--ink)">%s</div>'
       '<div style="margin-top:auto;padding-top:12px;border-top:1px solid var(--hair);'
       'min-height:48px;font:400 16px/1.5 var(--f-cn);color:var(--ink-3)">%s</div></div>'
       % (AC if _on else "var(--ink-3)", _tag, _v, _l, _n))
    for _i, (_tag, _v, _l, _n, _on) in enumerate(_CA_STAT)
    ] + [
    lab(120, 640, "02 · KEY DIFFERENCE · 真人 vs 外呼智能体", i=5),
    # 差异三行走 table.mini + 页级 .ca-diff（把 td 上下 padding 从 11 收到 9）：
    # 三行 + 表头正好落在 168 的盒里，不碰 rule(850) 这条收口线。
    sh("rise", "left:120px;top:676px;width:1680px;height:168px;--i:6",
       '<table class="mini ca-diff"><thead><tr><th style="width:200px"></th>'
       '<th style="width:700px">真人</th>'
       '<th style="width:780px;color:var(--accent)">外呼智能体</th></tr></thead><tbody>'
       + "".join('<tr><td>%s</td><td>%s</td><td style="color:var(--accent)">%s</td></tr>' % _r
                 for _r in _CA_DIFF) + '</tbody></table>'),
    rule(850),
    land("TA 不疲惫、不带情绪、句句合规。", y=944),
    src(_CA_SRC),
]))

# ═══ P17 · 五个大脑 · Agent Harness（2026-08-21「Call Agent 章」新增 ◆ · 同日重做）══
#   2026-08-21 Colin：「不够 fancy —— 要一个脑子、五个区域一起工作、炫酷动起来」。
#   初版是五条并行横带（信息对，但读起来像交换机背板），本轮废弃，改**大脑侧视图**：
#   纯 SVG 手绘贝塞尔的 editorial 线稿（禁位图 / 禁 emoji），一颗脑分五区，五区同时在放电。
#
#   ── 解剖构图（侧视 · 鼻朝右 · 占 viewBox 的 x400–1140 / y40–520）──────────
#   轮廓一条 2.5px 主线闭合：额叶前凸（右）→ 圆润顶盖 → 后枕圆收（左）→ 颞叶下垂叶（下）；
#   小脑半球与脑干各自一只闭合小形，塞在枕叶之下 —— 分开画而不是并进主轮廓，
#   因为「大脑 / 小脑」之间那道裂隙本身就是这张图最容易被读懂的解剖特征。
#   分区边界走**脑沟**（S 形柔和曲线，不是直线切分）：
#     SUL1 中央沟   分开 05 额叶 与 03 顶叶
#     SUL2 外侧裂   分开上方（03/05）与颞叶
#     SUL3 颞上沟   分开 02 颞叶上部 与 01 颞叶下部
#   五区功能映射（区名文案逐字未改，用点线引线拉到脑外左右两栏）：
#     01 大模型流式语音识别 —— 颞叶下部（听觉皮层位，最靠「耳」，输入就从这里进）
#     02 选择性注意力锁定   —— 颞叶上部
#     03 真实意图识别       —— 顶叶（含枕区）
#     04 情绪感知和生成     —— 脑中心深部：画成一枚**环形**小区（边缘系统位，
#                              evenodd 双子路径挖空，画在皮层之上 = 它在皮层之下）
#     05 动态话术策略选择   —— 额叶（最前，输出从它的前缘发出）
#   区内各 2–3 条 0.8px 脑回纹理，低透明 —— 有质感但抢不过主轮廓。
#   所有区填色 / 纹理都 clip 在轮廓里（clipPath），所以 blob 可以画得糙、边界由轮廓裁。
#
#   ── 动效编排（全 deck 最炫的一页，但四条纪律一条不破）─────────────────────
#     ① 五区放电：每区一层 accent 柔和 fill 脉动（静态 .05 → 峰值 .15），
#        周期 2.4/2.7/3.0/3.3/3.6s 各不同 + 错峰负 delay ⇒ 五区肉眼可见全在工作、节奏互异。
#        走 .mo-pulse 但把 --mo-hi 设成**静态值 .05**、--mo-lo 设成峰值 .15 ⇒ 0%/100% 帧
#        = 静态原图（这正是原语文档里「载体自带 opacity 时」那一条的用法，不是反用）。
#     ② 神经火花：8 枚小圆点粒子沿 6 条突触弧线穿行（01→02→03→04→05 的链 + 两条跨区捷径），
#        .mo-packet 的小半径变体（seg 8 / w 8 / round cap ⇒ 一枚带拖尾的光点），速度错峰。
#     ③ 输出节拍：额叶前缘 → 输出盒的粗线 1.6s 一个重拍 .mo-pulse；hot 盒 breathe + halo。
#     ④ 输入常驻：耳位波形 → 颞叶下部的入线一枚常驻 .mo-packet。
#     ⑤ 深色霓虹：主轮廓下面垫一层 12px、低透明的 accent 软描边（**静态**，不带动画 ⇒
#        不进运动件账本，静态帧照样是它）——暗底上整颗脑因此有一圈自然的辉光。
#   运动件合计 17 个 / 4 种原语（原语全集 6，DOM 上限 30，都在线内）。
_BRAIN = (                                   # 大脑半球侧视轮廓（鼻朝右）
    "M1132 262 "
    "C1130 186 1076 116 986 84 "               # 额上隆起
    "C892 50 776 52 690 88 "                   # 顶盖
    "C598 126 530 182 496 244 "                # 后上
    "C466 296 476 330 508 352 "                # 枕极收尖（朝左）
    "C532 368 566 376 600 380 "                # 枕下 → 脑底
    "C632 384 654 402 674 428 "                # 转进颞叶
    "C702 464 774 484 842 478 "                # 颞叶底（下垂叶）
    "C902 472 956 442 984 400 "                # 颞叶前缘
    "C996 380 1000 366 990 356 "               # 颞极上折
    "C972 344 958 336 962 326 "                # 外侧裂切口（浅 · 只咬进 35px）
    "C968 314 990 310 1016 312 "               # 出切口
    "C1064 316 1104 306 1132 262 Z")           # 额下缘 → 回额极
_CEREB = ("M496 348 C540 374 590 388 628 402 C656 412 664 440 648 462 "
          "C626 486 578 490 540 476 C498 460 478 422 482 390 C484 364 488 350 496 348 Z")
_STEM = ("M660 388 C682 412 696 448 698 480 C700 502 678 508 668 492 "
         "C652 462 644 424 648 390 Z")
_SUL1 = "M876 54 C844 122 856 192 894 242 C918 274 930 300 936 318"        # 中央沟
_SUL2 = "M962 326 C904 336 838 348 776 358 C712 368 656 372 612 366"       # 外侧裂（脑内延长）
_SUL3 = "M988 384 C930 396 866 410 806 420 C744 430 700 430 674 420"       # 颞上沟
# 五区 blob：边界逐段抄上面三条脑沟 ⇒ 填色与沟线严丝合缝
#（首版没对齐，五块低透明色叠在一起，整颗脑糊成一团均匀的粉 —— 分区当场读不出来）
_ZONES = [
    ("M876 40 C990 10 1110 100 1160 250 C1170 292 1140 322 1090 318 "
     "C1030 316 968 314 962 326 "
     "C950 320 942 318 936 318 C930 300 918 274 894 242 "
     "C856 192 844 122 876 54 Z", "2.4s", "-0.0s"),                                   # 05 额叶
    ("M876 40 C780 14 720 40 676 78 C580 120 508 178 476 244 "
     "C444 300 458 342 500 360 C548 380 580 376 612 366 "
     "C656 372 712 368 776 358 C838 348 904 336 962 326 "
     "C950 320 942 318 936 318 C930 300 918 274 894 242 "
     "C856 192 844 122 876 54 Z", "3.0s", "-1.1s"),                                   # 03 顶叶+枕
    ("M962 326 C904 336 838 348 776 358 C712 368 656 372 612 366 "
     "C632 384 654 402 674 428 C700 430 744 430 806 420 "
     "C866 410 930 396 988 384 C998 372 992 360 990 356 "
     "C972 344 958 336 962 326 Z", "2.7s", "-0.5s"),                                  # 02 颞叶上
    ("M988 384 C930 396 866 410 806 420 C744 430 700 430 674 420 "
     "C700 476 776 502 848 494 C910 488 968 452 1002 398 Z", "3.3s", "-1.7s"),         # 01 颞叶下
    ("M800 186 C858 186 900 214 900 250 C900 286 858 314 800 314 "
     "C742 314 700 286 700 250 C700 214 742 186 800 186 Z "
     "M800 218 C762 218 734 232 734 250 C734 268 762 282 800 282 "
     "C838 282 866 268 866 250 C866 232 838 218 800 218 Z", "3.6s", "-2.3s"),         # 04 深部环
]
# 区内脑回纹理（0.8px · ink-3 低透明）：顺着各区走向排，密度压着，抢不过主轮廓
_GYRI = [
    "M556 176 C626 142 700 126 768 128", "M516 236 C588 202 664 186 736 188",
    "M500 296 C562 268 632 258 700 262", "M534 344 C588 326 646 320 700 324",
    "M934 102 C996 138 1046 190 1076 254", "M912 158 C972 196 1018 248 1044 306",
    "M902 236 C946 274 982 318 1002 356",
    "M700 382 C766 366 838 350 900 340", "M694 410 C760 394 830 378 892 366",
    "M700 440 C766 460 838 462 900 440", "M726 462 C784 480 848 480 900 462",
]
_ARCS = [   # (d, 长度近似, 周期, delay) —— 01→02→03→04→05 链 + 两条跨区捷径
    ("M856 442 C830 424 806 406 792 392", 90,  "2.2s", "-0.0s"),
    ("M782 378 C720 340 660 282 620 232", 210, "2.6s", "-0.9s"),
    ("M626 226 C672 232 716 240 748 246", 130, "2.4s", "-1.5s"),
    ("M868 252 C920 238 980 220 1030 210", 180, "2.8s", "-0.4s"),
    ("M854 436 C848 380 838 320 828 300", 145, "3.2s", "-1.2s"),   # 捷径 01→04
    ("M616 208 C700 132 900 124 1036 192", 460, "3.6s", "-2.1s"),  # 捷径 03→05
]
_ARC_EXTRA = [(1, "-1.8s"), (3, "-1.9s")]      # 这两条弧各再加一枚粒子 ⇒ 合计 8 枚
_LEADS = [  # (区序号, 引线 d, 标签 x, 标签 y, anchor, 区名)
    ("03", "M606 208 C520 172 440 136 376 116", 366, 122, "end",  "真实意图识别"),
    ("04", "M700 258 C600 272 470 286 376 292", 366, 298, "end",  "情绪感知和生成"),
    ("05", "M1054 212 C1092 190 1126 164 1150 148", 1160, 154, "start", "动态话术策略选择"),
    ("02", "M960 356 C1030 388 1098 422 1146 442", 1160, 448, "start", "选择性注意力锁定"),
    ("01", "M930 462 C1018 486 1094 506 1146 514", 1160, 520, "start", "大模型流式语音识别"),
]
_NUMS = [("01", 860, 456), ("02", 770, 392), ("03", 610, 222), ("04", 800, 256), ("05", 1040, 212)]
def _brain_fig():
    o = ['<defs><clipPath id="p17clip"><path d="%s"/></clipPath></defs>' % _BRAIN]
    # ── ⑤ 霓虹底层（静态 · 不带动画 ⇒ 不进运动件账本）──
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="12" opacity=".07" '
             'stroke-linejoin="round"/>' % (_BRAIN, AC))
    # ── 小脑 / 脑干：先画（= 在大脑之后 / 之下），大脑的填色与轮廓随后压过它们的上缘 ──
    for _d in (_CEREB, _STEM):
        o.append('<path d="%s" fill="var(--card-bg-2)" opacity=".95"/>' % _d)
        o.append('<path d="%s" fill="%s" opacity=".045"/>' % (_d, AC))
        o.append('<path class="dw" style="--len:900;--i:2" d="%s" fill="none" '
                 'stroke="var(--ink-2)" stroke-width="2.2" stroke-linejoin="round"/>' % _d)
    # ── ① 五区放电（全部 clip 在轮廓里）──
    o.append('<g clip-path="url(#p17clip)">')
    for _d, _dur, _del in _ZONES:
        o.append('<path class="mo-pulse" style="--mo-hi:.05;--mo-lo:.15;--mo-dur:%s;--mo-del:%s" '
                 'd="%s" fill="%s" fill-rule="evenodd" opacity=".04"/>' % (_dur, _del, _d, AC))
    # 区内脑回纹理
    for _g in _GYRI:
        o.append('<path d="%s" fill="none" stroke="var(--ink-3)" stroke-width=".8" opacity=".42"/>' % _g)
    # 脑沟（分区边界）：比纹理重一档、比主轮廓轻一档
    for _s in (_SUL1, _SUL2, _SUL3):
        o.append('<path class="dw" style="--len:520;--i:3" d="%s" fill="none" '
                 'stroke="var(--ink-2)" stroke-width="2" opacity=".85"/>' % _s)
    # ── ② 突触弧线 + 神经火花（也 clip 在脑内 —— 火花不该跑到脑外去）──
    for _d, _ln, _dur, _del in _ARCS:
        o.append(dline(_d, AD, 1.2, 4, dash="2 7"))
        o.append(packet(_d, _ln, col=AC, w=8, seg=8, dur=_dur, op=".55", i=4,
                        delay=_del, cap="round"))
    for _k, _del in _ARC_EXTRA:
        _d, _ln, _dur, _ = _ARCS[_k]
        o.append(packet(_d, _ln, col=AC, w=8, seg=8, dur=_dur, op=".55", i=4,
                        delay=_del, cap="round"))
    o.append('</g>')
    # ── 主轮廓 + 小脑 + 脑干（画在填色之上 ⇒ 线稿永远压得住色块）──
    o.append('<path class="dw" style="--len:2600;--i:1" d="%s" fill="none" stroke="var(--ink-2)" '
             'stroke-width="2.5" stroke-linejoin="round"/>' % _BRAIN)
    o.append('<path d="M494 382 C534 400 578 412 616 424" fill="none" stroke="var(--ink-3)" '
             'stroke-width=".8" opacity=".5"/>')
    o.append('<path d="M486 418 C526 438 570 452 610 458" fill="none" stroke="var(--ink-3)" '
             'stroke-width=".8" opacity=".5"/>')
    o.append('<path d="M492 448 C528 466 568 476 604 480" fill="none" stroke="var(--ink-3)" '
             'stroke-width=".8" opacity=".5"/>')
    # 04 环形深部小区：补一圈描边，让「深部结构」读得出是一枚独立器件
    o.append('<g clip-path="url(#p17clip)"><path d="%s" fill="none" stroke="%s" '
             'stroke-width="1.8" opacity=".6" fill-rule="evenodd"/></g>' % (_ZONES[4][0], AC))
    # ── 区序号（静态文字，绝不挂在动效件上）──
    for _n, _x, _y in _NUMS:
        o.append(txt(_x, _y, _n, "sm", size=15, anchor="middle", col="var(--ink-3)", mono=True))
    # ── 引线 + 区名标签 ──
    for _n, _d, _lx, _ly, _anc, _nm in _LEADS:
        o.append(dline(_d, "var(--ink-3)", 1.2, 5, dash="2 5"))
        o.append('<circle class="pop" style="--i:5;fill:%s" cx="%s" cy="%s" r="3.4"/>'
                 % (AC, _d.split()[0][1:], _d.split()[1]))
        o.append(txt(_lx, _ly, _nm, "ttl", size=21, anchor=_anc))
        o.append(txt(_lx + (-0 if _anc == "end" else 0), _ly - 26, _n, "sm", size=13,
                     anchor=_anc, col="var(--ink-3)", mono=True))
    # ── ④ 输入：耳位波形 → 颞叶下部（01 区）──
    o.append(txt(104, 392, "INPUT", "lbl", size=13, anchor="middle"))
    o.append(_bars(46, 7, 436, AC, seed=3, gap=17, w=8))
    o.append(txt(104, 492, "客户语音", "sm", size=16, anchor="middle"))
    _IN = "M206 462 C330 526 452 566 572 566 C662 566 726 532 752 496"
    o.append(packet(_IN, 620, col=AC, w=11, seg=22, dur="2.6s", op=".34", i=2))
    o.append('<path class="dw" style="--len:620;--i:2" d="%s" fill="none" stroke="%s" '
             'stroke-width="2.5"/>' % (_IN, AC))
    o.append(ah_u(756, 486, AC, 8))
    # ── ③ 输出：额叶前缘 → hot 盒（粗 accent-deep 快路径 + 1.6s 重拍）──
    o.append('<g class="mo-pulse" style="--mo-lo:.38;--mo-dur:1.6s">%s%s</g>'
             % (hline(1140, 1372, 268, AD, 5, 6), ah_r(1388, 268, AD, 8)))
    o.append(halo_rect(1400, 198, 262, 140, 8, sc="1.06", op=".3", dur="3.4s"))
    o.append(box(1400, 198, 262, 140, 8, hot=True, i=7, cls="mo-breathe", sty="--mo-dur:3.4s"))
    o.append(txt(1531, 278, "输出 · 最佳回复", "ttl", size=24, anchor="middle", col=AC))
    o.append(txt(1406, 188, "每 0.8 秒", "sm", size=14, col=AC, mono=True))
    return "".join(o)
page("content", "".join([
    head("AGENT HARNESS · 五个大脑 · 并行",
         "客户说话的每一秒里，<strong>五个大脑</strong>在并行工作。"),
    lab(120, 246, "01 · FIVE BRAIN REGIONS · 同时放电"),
    # 图例挪到页眉行右半区（P3「差异表 + 图例同一基线」同款破例）：
    # 主图是一颗满幅的脑，底下留不出图例带 —— 与其把脑压小，不如把图例上提。
    figbox(1090, 238, 710, 710, 30,
           legend(0, 16, [("solid", "输入 · 主通路"), ("fast", "合成输出"),
                          ("dot", "突触弧线"), ("dot", "标注引线", 1.2, "var(--ink-3)")]), i=5),
    figbox(120, 282, 1680, 1680, 580, _brain_fig(), i=1),
    sh("flow", "left:120px;top:876px;width:1680px;height:52px;--i:6",
       '<div class="note">我们把 Agent Harness 带进实时语音交互——五个大脑并行，'
       '每 0.8 秒合成一句恰到好处的回复，自然从容到听不出是 AI。</div>'),
    land("听清、听懂、想透、决断——同时发生。", y=944),
    sh("flow mono-sm", "left:120px;top:1015px;width:1000px;height:24px;--i:7",
       "为什么 96.5% 的客户听不出对面是 AI——答案在这五层。"),
    # 2026-08-23 采纳项 C · 补 P17 缺失的 SOURCE 行（GPT 5.6 实证：Call Agent 三页里
    # 只有这一页没有出处）。与 P16/P18 逐字同源、同一条 y1015 页脚基线 ——
    # 左右两栏原位不动，ledger 落在中间那段 949px 的净空里（实测两栏墨迹 120–494 / 1443–1800）。
    # top 取 1013 而不是 1015：本行 17px、邻栏 15px，基线差 ~2px，抬两格才对得齐。
    src(_CA_SRC, y=1013, x=520, w=880, align="center"),
    sh("flow mono-sm", "left:1100px;top:1015px;width:700px;height:24px;text-align:right;--i:7",
       "跑在对话式 AI 引擎的全双工链路上 · 见 P8"),
]))

# ═══ P18 · Loop Engineering · 成长飞轮（2026-08-21「Call Agent 章」新增 ◆）══
#   左 = 成长曲线（DAY 1 → 30，智能体上扬 vs 真人销冠平线，Day 15 穿越、Day 30 拉开到 2 倍位）
#   右 = 小环图（复盘 → 定位 → 迭代 → 训练，官网 Day 1 的 loop 意象，持续绕行）
#   下 = 三张里程碑卡，DAY 30 是 hot（「2 倍」按任务书用 accent 大字压在句尾）
#   曲线的坐标账（改图前先算这一笔，否则「2 倍」就不是 2 倍了）：
#     基线（零）y=250 · 真人销冠平线 y=160 ⇒ 一倍 = 90px · 两倍 = 180px ⇒ 曲线终点 y=70。
#     穿越点必须**恰好**落在 (700,160)：第二段三次贝塞尔的终点就写死在那里。
#   动效：曲线 .mo-packet（成长在跑）· 平线 .mo-drift（基准线也是活的，只是不长）·
#        穿越点 .mo-pulse · 终点 .mo-breathe + .mo-halo · 小环 .mo-cycle（dash 绕圈，
#        环几何不转 —— 与 P10 双层防御环同一条页级硬约束）。
_CA_MILE = [
    ("DAY 07", "跑完首批数千通迭代 Loop",
     "每一通不理想的电话都被自动分析、改写话术、重新训练、重新仿真测试，留资率提升 12%", False),
    ("DAY 15", "反超真人销冠",
     "黄金时段的转化率正式越过最好的销售，而且差距还在随每一个 Loop 继续拉开", False),
    ("DAY 30", "Loop 沉淀为一轮定向微调",
     "30 天通话数据沉淀为一轮定向微调反哺模型，转化效果稳定拉开到真人销冠的"
     "<b style=\"font:700 26px/1 var(--f-cn);color:var(--accent)\">2 倍</b>", True),
]
_CA_CURVE = ("M150 232 C 260 224, 340 214, 420 204 C 520 192, 620 176, 700 160 "
             "C 830 134, 960 108, 1060 70")
def _loopcurve_fig():
    o = []
    # ── 坐标轴（y 轴只画一截 + 一个箭头 = 「越高越好」，不标刻度：这页讲趋势不讲绝对值）──
    o.append(ah_u(110, 28, HS, 6))
    o.append(vline(110, 40, 250, HS, 1.4, 1))
    o.append(txt(126, 44, "转化效果", "sm", size=15, col="var(--ink-3)", mono=True))
    o.append(hline(110, 1150, 250, HS, 1.4, 1))
    for _x, _d in [(150, "DAY 01"), (420, "DAY 07"), (700, "DAY 15"), (1060, "DAY 30")]:
        o.append(vline(_x, 250, 259, HS, 1.4, 1))
        o.append(txt(_x, 280, _d, "lbl", size=14, anchor="middle"))
    # ── 真人销冠平线（基准）──
    o.append(dline("M150 160 H1060", HS, 2, 2, dash="7 6",
                   cls="mo-drift", sty="--mo-off:-39;--mo-dur:3.4s"))
    o.append(txt(1075, 166, "真人销冠", "sm", size=17, col="var(--ink-3)"))
    # ── 外呼智能体成长曲线 ──
    o.append(packet(_CA_CURVE, 980, seg=28, w=12, op=".32", dur="2.6s", i=3))
    o.append('<path class="dw" style="--len:1020;--i:3" d="%s" fill="none" stroke="%s" '
             'stroke-width="3.4" stroke-linecap="round"/>' % (_CA_CURVE, AC))
    o.append(txt(1075, 76, "外呼智能体", "sm", size=17, col=AC, weight=700))
    # ── 穿越点（DAY 15）：标签甩到点的左上，曲线在那一带是从右下往左下走的，不打架 ──
    o.append('<circle class="pop mo-pulse" style="--i:4;--mo-dur:2.2s;--mo-lo:.34;fill:%s" '
             'cx="700" cy="160" r="9"/>' % AC)
    o.append(txt(688, 138, "反超", "sm", size=18, anchor="end", col=AD, weight=700))
    # ── 终点（DAY 30）：2 倍位 ──
    o.append('<circle class="mo-halo" style="--mo-sc:2.2;--mo-op:.45;--mo-dur:3.2s" '
             'cx="1060" cy="70" r="10" fill="none" stroke="%s" stroke-width="2.5" opacity="0"/>' % AC)
    o.append('<circle class="pop mo-breathe" style="--i:5;--mo-dur:3.2s;fill:%s" '
             'cx="1060" cy="70" r="10"/>' % AC)
    o.append(txt(1060, 42, "2 倍", "ttl", size=26, anchor="middle", col=AC, weight=700))
    o.append(legend(0, 302, [("solid", "外呼智能体"), ("dash", "真人销冠基准")]))
    return "".join(o)
_CA_LOOP = [(190, 59, "复盘"), (286, 155, "定位"), (190, 251, "迭代"), (94, 155, "训练")]
def _loopring_fig():
    o = []
    # 环只让 dash 绕圈（.mo-cycle），几何不转：四个节点是钉在钟面位置上的，一转就乱套。
    # 周长 2πr = 603.2；dash「8 7」周期 15，--mo-off 取 600（= 40 个整周期）⇒ 100% 帧 = 原图。
    o.append('<circle class="pop mo-cycle" style="--i:2;--mo-off:-600;--mo-dur:9s" '
             'cx="190" cy="155" r="96" fill="none" stroke="%s" stroke-width="2.4" '
             'stroke-dasharray="8 7"/>' % AC)
    for _deg in (45, 135, 225, 315):            # 四个缺口上的顺时针方向标
        o.append('<g transform="rotate(%d 190 155)">%s</g>' % (_deg, ah_d(286, 155, AC, 7)))
    for _i, (_x, _y, _nm) in enumerate(_CA_LOOP):
        o.append('<circle class="pop" style="--i:%d;fill:var(--card-bg-2)" cx="%d" cy="%d" r="40" '
                 'stroke="%s" stroke-width="1.6"/>' % (3 + _i, _x, _y, AC))
        o.append(txt(_x, _y + 7, _nm, "ttl", size=20, anchor="middle"))
    o.append(txt(190, 162, "LOOP", "lbl", size=16, anchor="middle"))
    return "".join(o)
page("content", "".join([
    head("LOOP ENGINEERING · 自学习 · 自迭代",
         "和销冠一样擅长复盘成长，只是<strong>快一千倍</strong>。"),
    lab(120, 246, "01 · DAY 1 → DAY 30 · 成长曲线"),
    lab(1420, 246, "02 · THE LOOP", w=380, i=1),
    figbox(120, 276, 1240, 1240, 310, _loopcurve_fig(), i=1),
    figbox(1420, 276, 380, 380, 310, _loopring_fig(), i=2),
    lab(120, 612, "03 · THREE MILESTONES", i=4),
    ] + [
    sh("rise card-c%s" % (" on" if _on else ""),
       "left:%dpx;top:646px;width:540px;height:190px;--i:%d" % (120 + _i * 570, 5 + _i),
       '<div style="padding:24px 26px;height:100%%;display:flex;flex-direction:column">'
       '<div style="font:500 14px/1 var(--f-mono);letter-spacing:.18em;color:%s">%s</div>'
       '<div style="margin-top:10px;font:700 25px/1.25 var(--f-cn);color:%s">%s</div>'
       '<div style="margin-top:10px;font:400 18px/1.55 var(--f-cn);color:var(--ink-2)">%s</div>'
       '</div>' % (AC if _on else "var(--ink-3)", _day, AC if _on else "var(--ink)", _t, _d))
    for _i, (_day, _t, _d, _on) in enumerate(_CA_MILE)
    ] + [
    rule(850),
    land("通话内容自学习，转化效果自迭代。", y=944),
    src(_CA_SRC, i=8),
]))
# ═══ P19 · Physical AI · R1 开发套件（带实拍图 · 页号 13→19）════════════
#   文案双源 canon：31 页拜访版 P21（build-convoai-visit.py）+ robot26 #32（build-robot26-full.py）。
#   两版规格逐字对齐：R1-WiFi 2025.03.20 · BK7258 ／ R1-4G 2025.09.26 · UNISOC 8910 Cat.1。
#   唯一 hot = R1-4G 卡（.card-c.on）与它的「单芯片一体化」规格行 —— robot26 注明这是关键卖点。
#   2026-08-21 重排（Colin：「借鉴 robot26 的展示方式，那个有图片」）：
#     纯文字双卡 → 两张带实拍图的大图卡，资产跨 deck 引用 robot26 原片。
#   2026-08-21「完整显示」轮（Colin：「图片展示不全，比例看看」）：图在上 / 规格在下的
#     竖卡改成 **图左 / 规格右** 的横卡（820 宽 ×510 高，两张占满 1680 版心）——
#     图窗 400×510 让 cover 由高定标，整张 4:3 原片纵向全在窗内，两块板四边一格不缺。
#     腾挪账（版心高度是守恒的，图窗要长高就得有人让位）：
#       · 「共同能力」竖排 chip 右栏 → 横排 chips 落到收口线之下的页脚带（P7 同款破例）
#       · 「30000+」note → 与收口句同一基线的右半区（收口句实占 ≈800，右边本来就是空的）
#       · 角标 / 图注 → 右栏底部的图注行（原位会压住 4G 的天线，见 DECK_CSS 的 .r1-shot 段）
#     卡高 510 / 卡顶 262 / 收口句 786 / rule 850 / land 988 全部原值不动。
_R1KIT = [
    ("R1 · WI-FI · 2025.03.20 发布", "R1-WiFi", "主控 BK7258 · Wi-Fi 联网",
     "面向家居与室内——音箱 · 桌宠 · 陪伴机器人",
     "r1-wifi.webp", "[ R1 WI-FI ]", "带「灵动眼睛」PCB", False),
    ("R1 · 4G · 2025.09.26 发布", "R1-4G", "UNISOC 8910 · Cat.1 单芯片一体化",
     "面向户外 / 随身 / 车载 / 出海设备",
     "r1-4g.webp", "[ R1 4G ]", "带 4G 天线 · 一体化", True),
]
_R1CAPS = ["对话式 AI", "视觉理解", "本地唤醒", "灵动眼睛", "陀螺仪 / NFC / 振动"]
_R26 = "/decks/assets/robot26/"
page("content", "".join([
    head("PHYSICAL AI · R1 开发套件 · GLOBAL FIRST",
         "全球率先发布的<strong>对话式 AI 硬件开发套件</strong>。"),
    lab(120, 236, "01 · TWO FORMATS"),
    ] + [
    sh("rise card-c r1-card r1-%s%s" % ("ab"[_i], " on" if _on else ""),
       "left:%dpx;top:262px;width:820px;height:510px;--i:%d" % (120 + _i * 860, 2 + _i),
       '<div class="r1-shot"><img src="%s%s" alt="声网 R1 开发套件 · %s 实拍"></div>'
       '<div class="r1-body"><div class="r1-main">'
       '<div class="mono-sm" style="color:%s">%s</div>'
       '<h3 style="margin:12px 0 0;font:700 40px/1.15 var(--f-cn);color:var(--ink)">%s</h3>'
       '<div style="margin-top:16px;font:700 21px/1.4 var(--f-cn);color:%s">%s</div>'
       '<div style="margin-top:16px;font:400 18px/1.55 var(--f-cn);color:var(--ink-2)">%s</div>'
       '</div><div class="r1-cap"><span class="bdg">%s</span><span class="cap">%s</span></div>'
       '</div>'
       % (_R26, _img, _nm,
          AC if _on else "var(--ink-3)", _tag, _nm,
          AC if _on else "var(--ink)", _spec, _desc, _bdg, _cap))
    for _i, (_tag, _nm, _spec, _desc, _img, _bdg, _cap, _on) in enumerate(_R1KIT)
    ] + [
    # 786 而不是 848：content 背景板自带一条 accent 细线在 y848–852（x120–761），
    # 30px 大字压上去就是「被划掉」的观感 —— 那一带只留给 rule(850) 当收口线。
    sh("rise", "left:120px;top:786px;width:1000px;height:52px;"
       "font:700 30px/1.4 var(--f-cn);color:var(--ink);--i:6",
       "临场引擎 + 硬件参考设计 = <strong style='color:var(--accent)'>拿来即用的伙伴感地基</strong>。"),
    # note 与收口句同一基线的右半区：收口句实占 ≈800px，1180 起是这一行本来就空着的一半
    sh("flow", "left:1180px;top:786px;width:620px;height:52px;--i:6",
       '<div class="note"><b>30000+</b> 芯片与整机适配——你的形态大概率已支持</div>'),
    rule(850),
    # 02 落在收口线之下当页脚能力带：seclab + 横排 chips 同一行（P7「04 · TEN 生态」同款）
    sh("rise", "left:120px;top:884px;width:1680px;height:56px;--i:7",
       '<div style="display:flex;align-items:center;gap:24px">'
       '<span class="seclab" style="flex:none">02 · SHARED CAPABILITIES</span>'
       '<div style="flex:1">'
       + "".join('<span class="chip">%s</span>' % _c for _c in _R1CAPS) + '</div></div>'),
    land("你做产品与角色，我们做<strong style='color:var(--accent)'>临场与连接</strong>。", w=1000),
    # 2026-08-23 采纳项 C：时间窗取本页两张卡的发布日（与 convoai-info P6 同一份事实）
    src("SOURCE · 声网官网 / R1 公开发布信息 · 2025.03.20 / 2025.09.26 发布 · 事实截止 2026.08",
        y=1010, x=880, w=920, align="right"),
]))

# ═══ P20 · 无人机秀 DEMO · 全屏视频页（2026-08-21 · robot26 #24 同款机制）══
#   Colin 指令：R1（P19）之后插一页 robot26 #24 同款全屏视频页。
#   **纯片子**：无标题、无 land —— 一页只有一支片子，讲者按一下就播。
#   （2026-08-23 采纳项 E ②：补了一枚**静态**角标 kicker 压在左上角，仅此一行字。）
#   复刻的是 robot26 #24 已经踩平的那套机制，逐条对上（改这页之前先读完）：
#     ① 资产跨 deck 引用 robot26 目录，不复制文件（bake 的资产内联按路径全匹配，跨引用照吃）。
#        demo.mp4 3.1MB 不进归档内联 —— bake-archive 里换成线上绝对地址（见那份脚本的
#        _mask_media / MEDIA_ABS），离线打开退回已内联的 poster，在线打开照播。
#     ② **不带 controls 属性**：Blink 的原生控制条在 .deck-stage 的 transform:scale(≠1) 下
#        按未缩放坐标系渲染，条宽与位置全错（robot26 Colin 截图实锤）。悬停才由 JS 呼出，
#        供排练手控；静置态必须是干净画面，qa 的 ⑭ 闸盯着这一条。
#     ③ preload：22 页的 deck 一打开就预拉 3MB 视频是没道理的 —— 但 "none" 走过了头
#        （2026-08-23 采纳项 E ①，改成 "metadata"：只拉头部几十 KB，片体照旧按需拉）。
#     ④ muted + playsinline：不 muted 浏览器会拒绝自动播放（play() 直接 reject）。
#     ⑤ 分步：**容器绝不许挂 data-step** —— 2026-08-21 Colin 报「P19 之后多了一个空页面」，
#        根因就在这里：motion.css 末尾有一条兜底规则
#          .slide.visible [data-step]:not(.on):not(.flow):not(.rise)…{opacity:0}
#        「没有动效类的裸容器」在 step0 一律 opacity:0 —— 满幅视频盒连同 poster 整幅被摁成
#        透明，翻到 P20 就是一张白纸（浅色实测整页平均亮度 239）。此前误以为「没挂入场类
#        就不会被步进隐藏」，那条兜底规则正是专门管这种裸容器的。
#        改法：容器常显（poster 整幅静置可见），另起一枚**零尺寸 cue** 承载 data-step="1" ——
#        deck.js 的 maxStep 是从 [data-step] 元素算的（不读 section 的 dataset.steps，实测过），
#        所以这一枚是「本页有一步 build」的唯一依据；它零宽零高，两种步态都不可见。
#        视频挂 data-play-step="1"，播放脚本按「同一页里 [data-step=N] 是否 .on」判步。
#   1280×720 的片子与 1920×1080 舞台同 16:9 ⇒ object-fit:cover 不裁一格。
#   2026-08-23 采纳项 E · 首帧两改（播放机制一字不动：仍无 controls、仍 hover 呼出、
#   仍 vid-cue 步进、仍 MutationObserver 双钩）：
#     ① preload="none" → "metadata"。none 的代价是**首帧要等**：翻到 P20 时浏览器
#        连元数据都没有，poster 之外一片黑，讲者按下去还要等一轮网络往返。
#        metadata 只拉头部几十 KB（不是那 3.1MB），换来的是翻到即可播。
#     ② 补一枚静态角标 kicker：整页只有一支片子，没有任何字告诉观众「这是在讲什么」。
#        角标反白压在左上角（右上角归页码 sig），画面主体在中下部、hover 控制条在底部，
#        三者互不相碰；**不挂 data-step、不挂任何 mo-* 类** —— 它是纯静态文字件,
#        既不进运动件名册，也不会被 motion.css 的裸容器兜底规则摁成空页。
#     ③ 浅色主题下本页仍是电影感黑底全幅（video 自带 background:#000 + poster 满铺），
#        这是有意为之：qa 的 ⑭ 闸用「静置态整页平均亮度 < 60」双主题各钉一次。
_VID = "/decks/assets/robot26/"
page("content",
     sh("vid", "left:0;top:0;width:1920px;height:1080px;z-index:0",
        '<video data-play-step="1" src="%sdemo.mp4" poster="%sdemo-poster.jpg" '
        'preload="metadata" playsinline muted></video>' % (_VID, _VID))
     # 盒宽 760 而不是随手的 1200：实测墨迹 616px（20px mono · letter-spacing .28em），
     # 盒开到 760 只余 144px 呼吸，右缘 880 稳稳留在画面左半 —— qa ⑭ 按盒（不是按墨迹）
     # 验「角标不越到画面主体上」，盒虚开就等于闸失效。
     + sh("kk vid-kick", "left:120px;top:44px;width:760px;height:28px;z-index:2",
          "PHYSICAL AI · FROM ENGINE TO DEVICE")
     + '<i class="vid-cue" data-step="1" aria-hidden="true"></i>',
     steps=1)

# ═══ P21 · Why Agora ·「跑在声网实时互动底座之上」（页号 16→18→17→20→21）═══
#   数据修正页：四数字与 note / SOURCE 全部与 31 页拜访版 P2 一字对齐。
#   2026-08-20 起整块原样搬运（页号 12 → 15 → 16 → 18 → 17 → 20 → 21），内容一字未动。
#   禁止回归的旧错误数字：93万 / 700亿 /「对话式 AI 引擎市场占有率」/「200+ 覆盖场景 · 20+ 行业」
_WHY = [
    ("市场占有率", "No.1",   "稳居第一 · 份额超过第 2–8 位总和", True),
    ("技术突破",   "50+",    "突破性自主创新技术（全球发明专利）", False),
    ("开发者生态", "100万+", "全球注册应用数",                   False),
    ("生产规模",   "900亿+", "单月支撑通话分钟数",               False),
]
page("content", "".join([
    head("WHY AGORA · 底座实力", "跑在声网<strong>实时互动底座</strong>之上。"),
    sh("", "left:120px;top:300px;width:1680px;height:280px",
       '<div class="g4" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d;justify-content:center"><div class="tag%s">%s</div>'
           '<div class="stat"><span class="v%s" style="font-size:80px">%s</span>'
           '<span class="l">%s</span></div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag,
              "" if _on else " w", _v, _l)
           for _i, (_tag, _v, _l, _on) in enumerate(_WHY)) + '</div>'),
    # 2026-08-20 仲裁 P0：43.4% 这个具体数字未取得公司批准口径，改为「份额超过第 2–8 位
    # 厂商总和」的定性表述并把报告名写全；四张 KPI 卡的数字一个都不动。
    sh("flow", "left:120px;top:650px;width:1680px;height:60px;--i:5",
       '<div class="note grey">注：IDC《中国视频云市场报告》音视频通信（RTC）赛道 · '
       '<b>份额超过第 2–8 位厂商总和</b></div>'),
    # top 794 而非 820：content 背景板自带一条 accent 细线在 y848–852（x120–761），
    # land 落在 820 时字形正压在线上 = 划掉的观感；抬到 794 让那条线落到文字下方当收口横线
    land("2014 年成立，全球最受欢迎的实时音视频云服务提供商——语音智能体，"
         "跑在经海量流量锤炼的底座上。", y=794),
    # 本行与 convoai-info P2 逐字同源，两份 deck 不许分叉（四大数与限定语同理）
    src("SOURCE · 声网官网 / IR 公开口径 · IDC 中国视频云市场报告 · 事实截止 2026.08"),
]))

# ═══ P22 · OpenAI 合作 · 末页（logo 锁定版 + CTA · 页号 19→18→21→22）═══════
#   参照 robot26 #33「A QUIET ENDORSEMENT」，按 Colin 指令泛化两处：
#     ①「实时通信底座」→「对话式 AI 引擎底座」（本 deck 讲的是引擎，不是 RTC 管道）
#     ②「你的消费机器人」→「你的对话式智能体」（本 deck 的听众不限于机器人客户）
#   锚点 mono 行用 convoai-info P8 已核措辞「全球首批合作伙伴」——不写「全球首个」，
#   那是 OpenAI 的事，不是声网的事（info 二轮仲裁 P0 已钉死这一条）。
#   2026-08-21 收束轮 20 → 18：原 P20 收尾页删除，本页升为末页，承接两件事 ——
#     ① OpenAI × Agora logo 锁定版（robot26 双源资产跨引用，lt/dk 双 img CSS 显隐）；
#     ② 从被删收尾页继承的 CTA 行（Fable 裁定：真实入口不能随收尾页一起消失）。
#   版面改为居中：logo 锁定版一居中，左对齐的大字就会读成「浮在旁边」——
#   整页对齐方式必须跟着商标走，这是版面的因果，不是审美偏好。
page("title", "".join([
    sh("flow kk", "left:120px;top:128px;width:1680px;height:28px;text-align:center",
       "2024.10.01 · A QUIET ENDORSEMENT"),
    # 盒 838×570 = 原片整幅；墨迹（= 视觉上的 logo 锁定版）落在 x670–1250 / y196–562，
    # 即宽 580 居中。为什么不按墨迹开盒 —— 见 DECK_CSS 里 .lock 那段。
    sh("spread lock", "left:542px;top:160px;width:838px;height:570px;--i:2",
       '<img class="lt" src="%(A)sopenai-agora-light.png" alt="OpenAI × 声网 Agora 合作标识">'
       '<img class="dk" src="%(A)sopenai-agora.webp" alt="OpenAI × 声网 Agora 合作标识">'
       % {"A": _R26}),
    # 58px / 1560 宽：排满两行且左右各留 180 呼吸；62px/1680 时首行贴死版心边缘。
    sh("ink", "left:180px;top:626px;width:1560px;height:170px;text-align:center;"
       "font:700 58px/1.32 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       # 「寻找」外面这层 nowrap 不是装饰：CJK 允许任意两字之间断行，1560 宽下
       # 首行正好断在「寻 / 找」中间 —— 一个词被劈成两行，读起来像错字。
       "全球最强的 Voice Agent 团队，在为他们的 Realtime API "
       "<span style='white-space:nowrap'>寻找</span>"
       "<strong style='color:var(--accent)'>对话式 AI 引擎底座</strong>时，给出的选择。"),
    sh("spread", "left:900px;top:826px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow", "left:120px;top:868px;width:1680px;height:52px;text-align:center;"
       "font:400 32px/1.5 var(--f-cn);color:var(--ink-2);--i:4",
       "同样的工程能力，我们用来支撑你的对话式智能体。"),
    sh("flow mono-sm", "left:120px;top:966px;width:1680px;height:24px;text-align:center;--i:5",
       "2024 OpenAI Realtime API 发布 · 声网为全球首批合作伙伴"),
    # CTA：纯文本 mono 行，不做假链接样式（没有 <a>，不加下划线/悬停态）
    sh("flow mono-sm", "left:120px;top:1004px;width:1680px;height:24px;text-align:center;--i:6",
       "DEMO / 文档 · agora.io › 对话式 AI 引擎 · 联系团队"),
]))

# ═══ 组装 ═══════════════════════════════════════════════════════════════════
def build():
    total = len(PAGES)
    secs = []
    for i, (board, steps, body) in enumerate(PAGES, 1):
        sig = '<div class="sig">%d/%d</div>' % (i, total)
        secs.append(
            '<section class="slide conf-boarded" data-p="%d" data-steps="%d">\n'
            '  <div class="conf-bg conf-bg-%s" aria-hidden="true"></div>\n'
            '  <div class="pp">%s%s</div>\n</section>' % (i, steps, board, sig, body))
    chrome = ('<div class="deck-grid" aria-hidden="true"></div>'
              '<div class="deck-rail t" aria-hidden="true"></div>'
              '<div class="deck-rail b" aria-hidden="true"></div>')
    doc = (
        '<!DOCTYPE html>\n<html lang="zh-CN"><head>\n'
        # 主题初始化：与 convoai-info 同一个 localStorage 键 —— 同源 iframe 里
        # 引擎 deck 自动跟随宿主主题（抽屉体验的关键，别改键名）
        '<script>try{if(localStorage.getItem("colin-theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}</script>\n'
        '<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>声网 · 对话式 AI 引擎 · 深入讲解</title>\n'
        + FONTS
        + "<style>" + css("conf-theme-dual.css") + "</style>"
        + "<style>" + css("stage.css") + "</style>"
        + "<style>" + css("motion.css") + "</style>"
        + "<style>" + css("components.css") + "</style>"
        + "<style>" + css("conf-chrome.css").split("<svg class=\"deck-flow\"")[0] + "</style>"   # 流场退役：只取 CSS
        + BOARDS_CSS + DECK_CSS
        + "\n</head>\n<body>\n"
        '<div class="deck-viewport">\n  <div class="deck-stage" id="deckStage">\n'
        + chrome + "\n" + "\n".join(secs) + "\n  </div>\n</div>\n"
        '<div class="deck-progress" id="deckProgress"></div>\n'
        '<div class="deck-steps" id="deckSteps"></div>\n'
        '<div class="edit-hotzone" aria-hidden="true"></div>\n'
        '<button class="edit-toggle" id="editToggle">EDIT</button>\n'
        '<button class="deck-swap" id="deckSwap">暗底</button>\n'
        # 2026-08-21 Colin：「没有浅色切换的键」——本 deck 是对外产品文档、常被直接发链接，
        # 从 info 克隆来的「默认隐身 · hover 呼出」在这里等于键不存在。改为常显 chip：
        # 默认 .62（家族可见档 robot26 是 .5，这里略抬一档因为底下压着背景板），hover/focus 1；
        # 实底 --card-bg-2 而不是 transparent —— 左下角坐着 content 板的矩阵纹理，
        # 透明底会让 12px mono 掉进纹理里。只有 @media print 隐藏。
        # ⚠ info deck 的隐身规则不动（那份不是对外发链接的形态，键留给讲者自己按）。
        '<style>.deck-swap{position:fixed;left:26px;bottom:24px;z-index:1100;font-family:var(--f-mono,monospace);'
        'font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);'
        'border-radius:3px;padding:7px 12px;opacity:.62;'
        'transition:opacity .3s,color .3s,border-color .3s;background:var(--card-bg-2);cursor:pointer;}'
        '.deck-swap:hover,.deck-swap:focus-visible{opacity:1;color:var(--accent);border-color:var(--accent);}'
        '.deck-swap:focus:not(:focus-visible){outline:none;box-shadow:none;}'
        '@media print{.deck-swap{display:none!important;}}</style>\n'
        "<script>" + (SRC / "deck.js").read_text(encoding="utf-8") + "</script>\n"
        '<script>(function(){var b=document.getElementById("deckSwap");'
        'function apply(t){if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");b.textContent="浅底";}'
        'else{document.documentElement.removeAttribute("data-theme");b.textContent="暗底";}}'
        'var cur="light";try{cur=localStorage.getItem("colin-theme")||"light";}catch(e){}apply(cur);'
        # __setTheme：宿主（convoai-info 的引擎详解抽屉）切主题时会隔着 iframe 调它，
        # 一次把 data-theme 与按钮文案都对齐。点击时也从 DOM 现场读当前态，
        # 免得闭包里的 cur 被外部改动搞成陈旧值、再点把主题切反。
        'window.__setTheme=apply;'
        'b.addEventListener("click",function(){b.blur();'
        'var now=document.documentElement.getAttribute("data-theme")==="dark"?"dark":"light";'
        'var nxt=(now==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",nxt);}catch(e){}apply(nxt);});})();</script>\n'
        # ── 视频页播放挂钩（P20 无人机秀）─────────────────────────────────────
        #   共享 deck.js 是 CONF 全家共用的 runtime，里面没有 robot26 那套 syncMedia，
        #   **也不去改它**（改一份 runtime 会波及 convoai-info / visit 三份 deck）。
        #   这里在 deck.js 之后套一层壳，两道保险各管一段：
        #     ① 包 deck.go / deck.applySteps —— 实例上写同名属性遮蔽原型方法，
        #        原方法照跑，跑完补一次 sync()。这是**现场翻页**走的路。
        #     ② MutationObserver 盯 .slide 与分步容器的 class —— qa / occlusion-scan /
        #        截图脚本是直接 classList.toggle 的，根本不经过 deck.go，
        #        只有这一道才盯得住。rAF 去抖，一次翻页最多算一次。
        #   判活一律**从 DOM 读**（.active + [data-step].on），不读 deck.i / deck.step：
        #   两条路径共用同一套判据，就不会出现「现场在播、截图里没播」这种分叉。
        '<script>(function(){'
        'var vids=[].slice.call(document.querySelectorAll("video[data-play-step]"));'
        'if(!vids.length||!window.deck)return;'
        # 原生控制条只在悬停时挂（transform:scale 下的错位见 DECK_CSS 的 .sh.vid 段）
        'vids.forEach(function(v){'
        'v.addEventListener("mouseenter",function(){v.setAttribute("controls","");});'
        'v.addEventListener("mouseleave",function(){v.removeAttribute("controls");});});'
        'function sync(){vids.forEach(function(v){'
        'var sec=v.closest(".slide");'
        'var cue=sec&&sec.querySelector(\'[data-step="\'+(+v.dataset.playStep||1)+\'"]\');'
        'var live=!!sec&&sec.classList.contains("active")&&(!cue||cue.classList.contains("on"));'
        # 两道钩子会对同一次翻页各触发一次，这里按当前状态短路 ⇒ 同一次翻页只真的动一次。
        # play() 在没有 H.264 解码器的环境里会 reject（CI 容器就是），吞掉即可 —— 那不是页面的错；
        # reject 之后 v.paused 会翻回 true，下一次 sync 自然会再试，不需要额外的重试逻辑。
        'if(live){if(v.paused){var p=v.play();if(p&&p.catch)p.catch(function(){});}}'
        'else if(!v.paused||v.currentTime){try{v.pause();v.currentTime=0;}catch(e){}}});}'
        '["go","applySteps"].forEach(function(m){var f=window.deck[m];'
        'window.deck[m]=function(){var r=f.apply(this,arguments);sync();return r;};});'
        'var pend=false;var mo=new MutationObserver(function(){if(pend)return;pend=true;'
        'requestAnimationFrame(function(){pend=false;sync();});});'
        'vids.forEach(function(v){var sec=v.closest(".slide");if(!sec)return;'
        'mo.observe(sec,{attributes:true,attributeFilter:["class"]});'
        'sec.querySelectorAll("[data-step]").forEach(function(c){'
        'mo.observe(c,{attributes:true,attributeFilter:["class"]});});});'
        'sync();})();</script>\n'
        "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")
    OUT_ALIAS.write_text(doc, encoding="utf-8")
    assert total == 22, "页数漂移：%d != 22" % total
    assert doc.count("<section") == 22, "section 数漂移：%d" % doc.count("<section")
    boards = {i: b for i, (b, _s, _y) in enumerate(PAGES, 1)}
    assert {i for i, b in boards.items() if b == "title"} == {1, 22}, \
        "title 板页漂移：%r" % sorted(i for i, b in boards.items() if b == "title")
    steps_map = {i: s for i, (_b, s, _y) in enumerate(PAGES, 1) if s}
    assert steps_map == {6: 1, 7: 1, 14: 1, 20: 1}, "分步页漂移：%r" % steps_map
    # 视频页红线：controls 属性绝不许出现在产物里（悬停呼出是 JS 的活儿，不是属性的活儿）
    assert doc.count('<video ') == 1, "视频件数漂移：%d" % doc.count('<video ')
    assert " controls" not in doc.split('<video ')[1].split('>')[0], \
        "视频页写死了 controls —— transform:scale 下会错位（robot26 实锤）"
    # 视频页首帧（2026-08-23 采纳项 E）：preload 必须是 metadata；静态角标必须在位且不带步进
    _vtag = doc.split('<video ')[1].split('>')[0]
    assert 'preload="metadata"' in _vtag, "视频页 preload 不是 metadata：%r" % _vtag
    assert 'class="sh kk vid-kick"' in doc, "视频页缺静态角标 kicker"
    _ktag = doc.split('class="sh kk vid-kick"')[1].split('>')[0]
    assert "data-step" not in _ktag, "视频页角标挂了 data-step —— 静态文字件不许进步进"
    assert "mo-" not in _ktag, "视频页角标挂了 mo-* 原语 —— 它不进运动件名册"
    # Call Agent 章红线（三条，构建期就拦住，别等到 qa）：价格数字 / staging URL 一律不许上页
    for _bad in ("¥8,500", "¥2,999", "¥5,501", "staging"):
        assert _bad not in doc, "Call Agent 红线：全 deck 不许出现「%s」" % _bad
    # SOURCE ledger（采纳项 C）：九张数据页各一行、四段制、结尾一律「事实截止 2026.08」；
    # 旧格式（SOURCE 行挂在 .mono-sm 上）一行都不许剩。
    import re as _re
    _srcs = _re.findall(r'<div class="sh flow src"[^>]*>(SOURCE[^<]*)</div>', doc)
    assert len(_srcs) == 9, "SOURCE ledger 行数漂移：%d != 9（%r）" % (len(_srcs), _srcs)
    for _s in _srcs:
        assert _s.startswith("SOURCE · "), "SOURCE 行不以「SOURCE · 」起手：%r" % _s
        assert _s.endswith(" · 事实截止 2026.08"), "SOURCE 行未以事实截止收尾：%r" % _s
        assert _s.count(" · ") >= 2, "SOURCE 行不足两段：%r" % _s
    _stray = _re.findall(r'<div class="sh flow mono-sm"[^>]*>(SOURCE[^<]*)</div>', doc)
    assert not _stray, "仍有 SOURCE 行挂在 .mono-sm 上（未并入 ledger）：%r" % _stray
    # kicker 消歧（采纳项 F）：P10 大图 / P14 接入各自带限定词，不许再撞成同一句
    assert "ENGINE INTERNALS · 运行时内部链路" in doc, "P10 kicker 缺内部链路限定词"
    assert "ARCHITECTURE · INTEGRATION · 客户接入架构" in doc, "P14 kicker 缺客户接入限定词"
    # ── 三数章重构（2026-08-23）：新序 P5 → 650 → 340前提 → 340 → 95% → 大图 ──
    #   页序是这一轮的全部要点，所以在构建期就按「页号 × 关键词」逐页锚死：
    #   任何一次误搬运（哪怕正文一个字没动）都会在这里当场炸，不必等到 qa。
    _secs = doc.split('<section class="slide conf-boarded" data-p="')
    _page_txt = {int(x.split('"')[0]): x for x in _secs[1:]}
    for _p, _kw in [(5, "01 · THREE EXTREMES"),
                    (6, "EXTREME 01 · 650MS · PIPELINE"),
                    (7, "EXTREME 02 · 340MS · 前提 · VOICE ACTIVITY DETECTION"),
                    (8, "EXTREME 02 · 340MS · INTERRUPTION"),
                    (9, "EXTREME 03 · 95% · SELECTIVE ATTENTION"),
                    (10, "PRODUCT ARCHITECTURE · ENGINE INTERNALS")]:
        assert _kw in _page_txt[_p], "三数章页序漂移：P%d 缺「%s」" % (_p, _kw)
    # P5 的三枚章内指针 + 导航 land；P10 的三枚锚点 chip + 收束句
    for _ptr in ("&#8595; P6", "&#8595; P7&#8211;8", "&#8595; P9"):
        assert _ptr in _page_txt[5], "P5 缺章内指针「%s」" % _ptr
    assert "三件事，接下来" in _page_txt[5], "P5 缺章内导航 land"
    for _al in ("650MS", "340MS", "95%"):
        assert _al in _page_txt[10], "P10 缺锚点 chip「%s」" % _al
    assert "都在这张图上" in _page_txt[10], "P10 缺章尾收束句"
    print("convoai.html + convoai-engine.html（双生） · %d 页 · %dKB · conf-light 默认 · 分步 %r"
          % (total, len(doc) // 1024, steps_map))

if __name__ == "__main__":
    build()
