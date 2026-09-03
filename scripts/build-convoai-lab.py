#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-lab.py ·《声网 · 对话式 AI 引擎 · 深入讲解 · LAB》22 页 · **私享**
#   = /convoai 引擎版的 **LAB 家族演绎**（LAB 家族 2026-08-31 立族后的生产首秀 →
#     同日 Colin 拍板：convoai-lab 是 LAB 家族**旗舰**，全量 3D 演绎）。
#   从 build-convoai-engine.py **整体克隆**：22 页、章序、口径、Call Agent 三页、
#   P20 视频页、P10 大图……**正文一个字没动**（build() 末尾有逐页同源自证：
#   非 3D 的 6 页与引擎产物**逐字节**比对，3D 的 14 页逐字比正文 + 比 data-step 集合，
#   P1 只准 kicker 末段加「· LAB」、P21 只准换盒子 + 加角注）。
#
# ── 全量 3D 化 · 第一波（2026-08-31）：单渲染器巡游 + 王牌五页 ───────────────
#   七枚 WebGL 语义场景（其余 15 页照家族 2D，一格不改）：
#     P1  封面「对话即交互。」 → 声场球（球面点云沿法线呼吸 · kicker 末段加「· LAB」）
#     P4  全双工工作原理       → 双向声带（两条对向 ribbon 交错穿行不相撞 · 重叠区高亮）★
#     P7  VAD                  → 声学地形（概率曲线挤出成山脊 + 悬浮判定带 + 事件立柱）★
#     P9  SAL                  → 双层防御壳（三类噪声撞壳弹开 · 目标人声从缺口入核）★
#     P17 五个大脑             → 体积点云大脑（母形 = 页上那条 13 段贝塞尔侧视轮廓）★
#     P18 Loop Engineering     → 复利螺旋（脊线 = 页上那条成长曲线本人）★
#     P21 Why Agora            → SD-RTN 地球（/lab-globe 实现整体移植 · 半屏缩配）
#   逐页语义审查照旧：P5/P15/P16/P19/P20/P22 是数字卡 / 成绩单 / 实拍 / 视频 / 末页，
#   没有 3D 语义 ⇒ 保持 2D。「每 deck 1–3 个 WebGL 页」那条家族铁律对纯 LAB 旗舰不适用。
#   第二波（另九页）直接踩在这套地基上：写一个场景工厂 + 在 LAB_RECTS 里加一行。
#   架构与降级链的完整说明见下面的「LAB 层」大注释块。
#
# ── 全量 3D 化 · 第二波（2026-08-31 · **终波**）：九页套件化升维 ─────────────
#   16 / 22 页跑 WebGL。九枚新场景（★ = 本波）：
#     P2  实时决策    → 决策轨道环 ★（页上那条闭环整条抬进空间 · 微倾斜 ·
#                        四支箭头的落点成发光站点 · 点线反馈弧做**支轨**）
#     P3  双工三模式  → 三条空间通道 ★（A 列在近 / B 列在远，通道真的穿越空间；
#                        单工回向静默无包 / 半双工占空比 1/3 + 半周期互斥 / 全双工恒同框）
#     P6  实时语音链路 → 空间站点序列 ★（两端近、LLM 最深；四条增量流带并行 +
#                        四段粒度逐段变粗的符号流；step1 数字人支路往前弹出主路平面）
#     P8  优雅打断    → 打断时序 ★（两条声轨在深度里交错；过了收声线，
#                        智能体轨 340ms 内陡降成 ghost 并退远，用户轨推到前面）
#     P10 产品大图    → 分层深度化 ★（**谨慎页** · 见下面那条红线）
#     P11 弱网 AI QoS → 囤着播 ★（包雨落进 3D 缓存堆；断网段上游停发、堆矮下去，
#                        下游包流一枚不断 —— 「囤着播」的立体证据）
#     P12 视觉模态    → 相机视锥 ★（锥顶在眼镜 chip、锥口是「看图识景」卡，
#                        画面平面顺着视锥推进对话流；底部次级带保持弱化）
#     P13 开放编排    → 3D 插槽机 ★（槽是背向拉伸的空腔，板卡坐在腔口；
#                        热切换 = 旧板退进腔里、新板从深处升上来，footprint 不变）
#     P14 接入架构    → 三塔握手 ★（终端近 / 客户服务器中 / 引擎云远；
#                        ①②③ 是三道塔间飞弧，按序点亮；时序徽标仍是 DOM）
#
#   ⚑ 本波的地基件是**投影锁**（lab-kit ⑤ 的 mkLock）：把页上的 2D 点抬到深度 z
#     再按 (D−z)/D 预缩放，透视除法正好把这一档除回去 ⇒ **投影落点与 2D 逐像素相同**。
#     第一波五页是「几何本来就没有标签」，第二波九页页页都压着标签（大图一页三十余处），
#     所以「有真深度」与「标签一格不挪」必须同时成立 —— 投影锁就是那个同时。
#     盒体一律 extrudeBack：**前面锁死**、后面沿 −z 退，于是有体积而正面轮廓不动。
#
#   ⚑ P10 是谨慎页，红线写死在场景注释里：**相机不动、层不做视差位移**（data-lab-drift
#     必须是 0，qa 复算）。微视差每移一个像素就有一处标注开始指空；这一页的 3D 是
#     「同一张图有了厚度」，不是「同一张图动起来了」。大图几何一格未动。
#
#   ⚑ P3 是全 deck 唯一一页**图形区坐在卡里**的 3D 页：卡底 72% 不透明会把 canvas
#     压成鬼影，所以 3D 起来时给卡开一扇窗（.p3-win，见 LAB_CSS）。不挂 gl-up 就是原来的卡。
#
#   ⚑ ⑳ 闸（build() 末尾）：第二波九页的几何名册逐条与产物里的 <rect>/<circle>/d= 对表。
#     页面改了图而 3D 没跟上 ⇒ 构建当场炸。P6 那两道 translate 就是这么找出来的。
#
# 重建：python3 scripts/build-convoai-lab.py
# 自检：node scripts/qa-convoai-lab.mjs（THEME=dark 二跑）
#      + DECK=lab node scripts/qa-motion.mjs
#      + DECK_URL=…/convoai-lab.html node scripts/occlusion-scan.mjs
#      + SELFPIN=1 A=…/convoai-lab.html PAGES=1,…,22 node scripts/pinned-diff.mjs
#        然后 MASK="$(grep -o 'data-lab-rect="[^"]*"' 产物 | sed …)" \
#        python3 scripts/compare-frames.py a b（16 块 canvas 区逐页豁免，其余逐像素）
#      + DO=w2,w2grid,w2gif,contact2,w2fallback node scripts/shot-convoai-lab.mjs
#
# ── 下面是从引擎母本原样继承的沿革（改正文之前先读，它记着每一条口径的来历）──
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
# LAB 版是**单产物**（引擎版的双生别名机制不继承）：/convoai 与 /convoai-engine
# 那一对由 build-convoai-engine.py 独占，本 builder 一个字节都不碰它们。
OUT = ROOT / "public" / "decks" / "convoai-lab.html"
ENGINE_REF = ROOT / "public" / "decks" / "convoai-engine.html"   # 同源自证的比对基准
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
  letter-spacing:.12em;color:var(--ink-3);
  /* ── 波B 顺手修：页码 pinned 53px 差异 ────────────────────────────────────
     真因不是「字变了」，是**同一串「1/22」一次走 subpixel 光栅、一次走 grayscale**：
     两次跑的合成层不同（有没有别的元素把它提成独立层），抗锯齿路径就不同，
     逐像素比对当场报 53px 差异。
     ⚠ `-webkit-font-smoothing:antialiased` 在 Linux / Windows Chromium **根本不生效**
       （那是 macOS-only 的属性），拿它治这个病等于没治。
     正解是把它**恒定**提成合成层 —— will-change + translateZ(0) 一起用：
     两次跑都走 grayscale 光栅 ⇒ 22 页 pinned 差异归 0。 */
  will-change:opacity;transform:translateZ(0);}
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
/* ── P22 背景板的右半软遮罩（2026-09-03 · 互动星系入页）──────────────────
   title-02-orbit 的右半是三枚旋转 −25° 的椭圆轨道（中心≈(1470,510)），
   与星系自己的三枚**正**椭圆轮廓环叠在一起就是两套倾角在打架 —— 屏上读成
   「六个环」而不是「三个环」。P22 仍是 title 板页（首尾对仗 P1 不变），
   只把背景板的右半淡掉：左半的 y≈878 hairline 照旧留下当使命 / 愿景块的收口线。
   收口点取 56%（x1075）而不是 60%（x1152）：板上那枚轨道小行星落在页 x≈1108，
   60% 那一档它还剩 23% 不透明度，在星系左边读成一粒来路不明的杂点；
   56% 让板在星系最左缘（外环外缘 x1087.5）**之前**就淡干净。 */
.slide[data-p="22"] .conf-bg{-webkit-mask-image:linear-gradient(90deg,#000 0,#000 50%,transparent 56%);
  mask-image:linear-gradient(90deg,#000 0,#000 50%,transparent 56%);}
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
/* ── LAB · P21 半屏 KPI 卡（只收白边，字号一格不动）────────────────────────
   四张卡从「一行四张 × 1680 宽」改成「2×2 × 930 宽」之后，卡内高度就成了瓶颈：
   家族 .card 的 30/32 padding + gap 13 在 196px 的行高里差 7px。这里把它收到
   24/26 + gap 10（**只动白边**），80px 的数字与 20px 的说明一个像素不改。
   作用域钉死在 .lab-kpi 上：另外 21 页的 .card 一律走家族原值。 */
.lab-kpi .card{padding:24px 26px;gap:10px;}
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

PAGES = []          # (board, steps, body_html, lab_kind)
def page(board, body, steps=0, lab=None):
    """lab：这一页的 3D 舞台种类（"voice" / "globe" / None）。
       None 的页拼装时插入空串 ⇒ 与引擎母本逐字节相同（build() 末尾会验）。"""
    PAGES.append((board, steps, body, lab))

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

# ═══════════════════════════════════════════════════════════════════════════
# LAB 层 · three.js 语义 3D 升维（2026-08-31 · LAB 家族生产首秀 → 第一波全量 3D 化）
# ───────────────────────────────────────────────────────────────────────────
#   convoai-lab 是 LAB 家族的**旗舰**：Colin 2026-08-31 拍板全量 3D 演绎。
#   「每 deck 1–3 个 WebGL 页」那条家族铁律对纯 LAB 旗舰不适用（逐页语义审查照旧：
#   P5/P15/P16/P19/P20/P22 是数字卡 / 成绩单 / 实拍 / 视频 / 末页，没有 3D 语义，保持 2D）。
#
#   第一波七枚场景 —— 单渲染器巡游 + 王牌五页：
#     P1  封面「对话即交互。」   → 声场球（球面点云沿法线呼吸）
#     P4  全双工工作原理         → 双向声带（两条对向 ribbon 交错穿行不相撞）★
#     P7  VAD                    → 声学地形（概率曲线挤出成山脊 + 悬浮判定带 + 事件立柱）★
#     P9  SAL                    → 双层防御壳（三类噪声撞壳 · 目标人声从缺口穿两壳入核）★
#     P17 五个大脑               → 体积点云大脑（母形 = 页上那条 13 段贝塞尔侧视轮廓）★
#     P18 Loop Engineering       → 复利螺旋（脊线 = 页上那条成长曲线本人）★
#     P21 Why Agora              → SD-RTN 地球（lab-globe 实现移植 · 半屏缩配）
#   第二波（2026-08-31 终波）另九页就踩在这套地基上落地：P2 决策轨道环 / P3 三通道 /
#   P6 空间站点序列 / P8 打断时序 / P10 大图分层 / P11 QoS 囤着播 / P12 相机视锥 /
#   P13 插槽机 / P14 三塔握手 —— 逐页只写语义几何，基建一行没重写。
#   本波唯一新增的地基件是 lab-kit ⑤ 的**投影锁**（见那一段的大注释）。
#
# ── ① 单渲染器巡游（本轮最重要的工程）────────────────────────────────────
#   全 deck **只有一个 WebGLRenderer + 一块 canvas**。canvas 常驻车库 .lab-garage
#   （屏外），翻页时被 appendChild 进目标页的 .lab-stage、按该页声明的 data-lab-rect
#   对位，并热切换到该页的场景；目标页没有场景就回车库、canvas 隐身。
#   canvas 在 DOM 里搬家不丢 WebGL 上下文 ⇒ 「同页面 WebGL 上下文上限」这条限制
#   从根上消失（16 个 3D 页也只吃一枚上下文），任一时刻只有一个场景在渲染。
#
# ── ② SVG = poster 层（降级层就是页上原来那张图）────────────────────────
#   每个 3D 页的现有 SVG **原地保留**：页内那一段几何被 <g class="lab-poster"> 裹住，
#   3D 起来（gl-up 且该页场景已渲出第一帧）就淡出、canvas 接管；WebGL 不可用 /
#   自动降级 / print / reduced-motion / 离线归档 ⇒ 它原样呈现，那一页仍是完整的 2D 版。
#   **DOM 文案、kicker、SOURCE、data-step 步进语义零改动** —— 淡出的只有「形」，
#   标签 / 引线 / 图例 / 卡片全部留在 .pp 里压在 canvas 之上（canvas 在 .pp 之下）。
#   build() 末尾有逐页逐字自证：22 页 DOM 文本与引擎母本逐字相同（唯一例外是
#   P1 kicker 末段的「· LAB」），非 3D 的 15 页仍是**逐字节**同源。
#
# ── ③ 共享场景套件 lab-kit（第二波直接复用）──────────────────────────────
#   主题色桥（CSS 变量 → uniform，MutationObserver 延一 rAF）／确定性随机／
#   折线工具（构建期展平 SVG 贝塞尔 → 运行时复活：unpackPoly / polyAt / insideMulti /
#   distToPoly）／px 场景相机（z=0 平面上 1 世界单位 = 1 屏幕像素 ⇒ 页上 SVG 坐标
#   直接搬进 3D，3D 形与它替换掉的 2D 形逐像素同位）／点云 · 线 · 流带三套材质工厂／
#   入场 t 参数／data-step→uniform 桥。每景只写语义几何，不重写基建。
#
#   数据单一真相：陆地位掩码 / 节点表 / 取道表 / 弧相位表**全部从 lab-globe.html 抠**
#   （见 _labg()）；五枚新场景的几何**全部从各页的 SVG 路径字符串展平**（见 lab-kit
#   的几何预处理）。这份 builder 里一个 3D 坐标都不写死 —— 页上的图改了，3D 跟着走。
#
#   降级链（六道，缺一不许上生产）：
#     ① poster 常驻层：P1/P21 是构建期用**与运行时逐字同参的相机矩阵**离线投影出的
#        静态 SVG；另五页是页上原来那张图。不挂 .gl-up 即 poster。
#     ② prefers-reduced-motion ⇒ 渲一帧（入场落位）就停帧
#     ③ @media print ⇒ 藏 canvas、显 poster；beforeprint 先同步渲一帧再 toDataURL
#        写进当前页的 .lab-print（render-then-read：不开 preserveDrawingBuffer，
#        靠「同一 tick 内渲染完立刻读」拿到非空帧，读完即弃 ⇒ 常态零显存代价）。
#        纸上 22 页一起铺开而 canvas 只在其中一页里 ⇒ 其余 3D 页在纸上一律以 poster 为准。
#     ④ document.hidden **与非激活 slide** 双双 cancelAnimationFrame（离开即复位入场参数）
#     ⑤ DPR ≤ 2，再乘舞台缩放
#     ⑥ FPS 探针：连续 2s 平均 < 20 自动退 poster（`?lab=hold` 可关，见下）
#
#   两枚开关（生产特性，不是 QA 后门）：
#     ?debug=1   显出 FPS 探针（生产页默认不挂常显探针，自动降级逻辑照跑）
#     ?lab=hold  关掉自动降级 —— 讲者在弱机 / 软渲染环境下宁可要「慢但活的形」也不要
#                静帧时按这个；截图与录屏管线也走它（容器里 SwiftShader 只有个位数 fps，
#                不给这条路，终审静帧拍到的永远是 poster）。
#
#   材质色：three 代码里**一个色号都没有**，全部 getComputedStyle 读 LAB_CSS 里的
#   --v-* / --g-* / --b-* / --s-* / --r-* / --t-* / --d-*；MutationObserver 盯
#   html[data-theme]，**延一个 rAF** 再 applyTheme（换页交叠时 CSS 变量还没落到新值上，
#   同帧读会读到上一主题的色）。七个场景一起热更新，不只当前那个。
#
# ── 第二波接入指南：加一枚场景要写的六件事（照做即可，基建一行都别重写）──────
#   ① LAB_RECTS 加一行：`P: ("名字", x, y, w, h)` —— 矩形取该页 figbox 的位与尺寸
#      （本 deck 所有 figbox 的 vbw == 盒宽 ⇒ 缩放恒为 1，figure 坐标就是舞台像素）。
#   ② 那一页的 page(...) 末尾加 `lab="名字"`（build() 会与 LAB_RECTS 对表，写错当场炸）。
#   ③ 把该页 SVG 里**属于「形」的那几段**用 lp(...) 裹起来（字一个都别裹）。
#      判据：3D 会替换掉的就是形；标签 / 引线 / 图例 / 数字 / 卡片一律留在外面。
#   ④ 在 lab_k() 里加一段该场景的常量：几何一律用 _poly()/_polym() 从页上的 `d=`
#      展平，周期 / 相位一律用 _sec() 从页上的 --mo-dur/--mo-del 抄 —— 不新造坐标。
#   ⑤ 写 make<名字>(ctx)：只写语义几何。相机用 camPx(w,h,D)（z=0 平面上 1 单位 = 1 像素）、
#      材质用 mkMat(pxShared(D, 深度半程), PX_*_VS, PX_*_FS)、流带用 ribbonGeo、
#      逐点属性用 attrAH。返回 {scene,camera,intro,grab,onDPR,setIntro,draw,applyTheme
#      [,setStep][,onEnter][,onLeave]}，然后挂进 FACTORY 表。
#      ⚠ 深度半程一定要贴着该场景的真实 z 范围收紧 —— 松了就等于没有体积。
#      ⚠ 着色器里用到的每一个 uniform 都要在 VS/FS 里**声明**：漏一个不会报页错，
#        只会整层静默不画（本轮踩过一次：uTime/uCap 没声明，整颗脑云凭空消失）。
#   ⑥ 材质色进 LAB_CSS 的 :root + html[data-theme="dark"] 两处（新起一个 --x-* 前缀），
#      并在 lab_data() 里把该场景的周期 / 相位 / 关键几何摊到 data-* 上供闸门静态复算。
#      qa 的 LAB_SCENES 表跟着加一行 —— 三处对表，加错页 / 漏页当场炸。
#   ⑦（第二波补的第七件事）几何名册进 build() 的 ⑳ 闸：新场景吃的每一只矩形 / 圆 /
#      路径串，都要能在产物里找到原件。这一条是「不新造坐标」从纪律变成机器自证的地方。
#   ⑧（第二波补的第八件事）页上那一组 figure 若带 transform（P6 的两道 translate），
#      3D 必须把同一道平移补上 —— 忘了就整组错位、页上的字全掉到盒外（本波实拍实锤）。
#   ⑨（二轮精修 · 波A 补的第九件事）**流 vs 粒子：这条线上跑的是介质还是事件？**
#      病根一句话：**点状移动不是数据流**。终审原话——「P14 的流动我不喜欢：太快；
#      三个点不像数据流。P6 数据点不足以表达媒体流。P8 想构建声波感但像锯齿。」
#      三条判据 + 三档流速 + 四步写法，照做即可：
#      ▸ 媒体 / 语音 / 数据流 —— **一律连续流带**（lab-kit ⑨ 的 mkStream）。
#        判据：这条线上跑的东西如果「一直在来」，它就是**介质**，必须是一条有厚度、
#        会起伏、**波峰自己往前走**的带子；不是一串沿着线挪的点。
#      ▸ 离散事件才许粒子 / 光束 —— 握手信号、单个包语义、热切换、过站脉冲。
#        判据：这一下**有起点有终点、发生一次就结束**。（P14 的三道握手用 mkBeamMat：
#        光束生长有头有尾有留痕，比三个点多出「到达」这个动作。）
#      ▸ 交界地带（P6 的 ASR→LLM token 段）：允许粒子但必须成「流」——
#        高密度脉冲串（每 N 枚一组，头亮尾淡）+ 极淡载流带垫底。
#        **只要看得出「一颗一颗在飞」，这一段就还没做完。**
#      ▸ 流速三档（品味统一，不是强迫症）：
#          A 连续媒体流 = 110px/s ±30%（摊 `data-lab-spd` 供 ⑲s 复算）；
#          B 离散事件语义自定（P14 注光 400px/s：它是「一下」，不是「一直」）；
#          C 与页面 CSS 同源者（dash 周期 / --mo-dur）**禁止**为统一速度去改。
#      ▸ 写一条流四步：`mkStream(SH, pts, opt)` → `.add(scene)`
#        → `.theme(峰值色, RMS色, op, rmsOp, uBack)` → 把速度写进 `_spd_of()`。
#        **幅度剖面一律走 gain 回调，不写分支代码** —— P8 的 200ms 让位、
#        P6 的过站收窄与由稀到密，全部只是一条 `gain` 回调（零 if 分支）。
# ═══════════════════════════════════════════════════════════════════════════
import math
import re as _re2

_LABG_SRC = (ROOT / "public" / "decks" / "lab-globe.html").read_text(encoding="utf-8")


def _labg(name):
    """从 /lab-globe 原型里抠一枚常量（字符串 / 数组 / 数字都吃）。
       ARC_GAP / ARC_OFF 不带 const（同一条 const 语句里的第二、三个声明），
       所以这条正则**不要求** const 起手。"""
    m = _re2.search(r'\b%s\s*=\s*("(?:[^"]*)"|\[[^\]]*\]|[0-9.]+)' % name, _LABG_SRC)
    if not m:
        raise SystemExit("lab-globe.html 里找不到常量 %s —— 原型改结构了？" % name)
    return m.group(1)


LAND_BITS = _labg("LAND_BITS").strip('"')
LAND_N = int(float(_labg("LAND_N")))
NODE_TABLE = _labg("NODE_TABLE").strip('"')
ROUTE_TABLE = _labg("ROUTE_TABLE").strip('"')
ARC_DUR_S = _labg("ARC_DUR")
ARC_GAP_S = _labg("ARC_GAP")
ARC_OFF_S = _labg("ARC_OFF")

_NODES_LL = [tuple(float(x) for x in s.split(",")) for s in NODE_TABLE.split(";")]
_ROUTES = [tuple(int(x) for x in s.split(",")) for s in ROUTE_TABLE.split(";")]

# ── 舞台 / 相机（poster 与运行时逐字同参；改一个数两边一起改）────────────────
LW, LH, LFOV = 1920, 1080, 30
FPX = (LH / 2) / math.tan(LFOV * math.pi / 360)      # 焦距（像素）= 2015.2957

# ── ① 声场球（P1 封面）· 构图账 ───────────────────────────────────────────
#   封面主标「对话即交互。」200px 单行，实测墨迹 x120–1284 / y280–503。
#   球必须**完全避开这条墨迹**、又要落在版心右缘 1800 之内，两条一起卡死了尺寸：
#     球心 (1555, 578) · 屏上半径 218 ⇒ 静置轮廓 x1337–1773 / y360–796，
#     呼吸振幅 ±7% ⇒ 极值轮廓 x1322–1788 / y345–811。
#     离主标墨迹右缘 38px、离版心右缘 12px、离页脚 mono 行（y942）131px。
#   球心 y 578 不是随手取的：它压在 accent 短棒（y572–576）的中线上 ——
#   左边那枚 120×4 的小棒与右边这颗球共一条水平轴，封面才是一张图不是两块。
VGR, VCX, VCY = 218.0, 1555.0, 578.0
VTILT = -0.18                       # 轻微前倾：线框两极露出来，球才有体积
VSPIN = 96.0                        # 秒 / 圈（比地球的 60s 更慢 —— 封面不抢主标）
VN = 4200                           # 点云枚数
VPOSTER_KEEP = 0.36                 # poster 抽稀比（确定性随机弃取，见 _keep()）
VAMP = 0.070                        # 呼吸振幅（球半径的 7%）
VW0 = 1.15                          # 伪音频基频（rad/s）
# 三枚谐波 (a, w, k, φ)：a 归一到 1 ⇒ 包络 W ∈ [-1,1]；w 两两不整除 ⇒ 永不重复；
# k 是沿 y 轴的空间波数 ⇒ 波是**横跨球面的行波**，不是整颗球一起胀缩（那是气球不是声场）。
VHARM = [(0.55, 1.00, 2.70, 0.00),
         (0.30, 1.63, 4.10, 1.70),
         (0.15, 2.41, 6.30, 3.90)]
VHOT = (0.18, 0.70)                 # 波峰上色区间（只有正向波峰走 accent）
VBACK = 0.22                        # 背面点的余亮：0 = 实心球，1 = 全透 —— 取 .22 是玻璃
VINTRO = 0.9                        # 入场秒数（--ease-flow 节奏）

# ── ② SD-RTN 地球（P21 Why Agora）· 半屏构图账 ───────────────────────────
#   左列（四大数 2×2 + IDC 注）占 x120–1050，地球占右半：
#     球心 (1470, 500) · 屏上半径 250 ⇒ 轮廓 x1220–1720 / y250–750。
#     离左列 170px、离版心右缘 80px、离标题盒下沿（y238）12px、离 land（y794）44px。
#   球径从原型的 414.6 缩到 250（0.60×）：自转 / 弧相位 / 节点密度一格不动，
#   只有相机距离跟着变 —— 缩的是构图，不是内容。
GGR, GCX, GCY = 250.0, 1470.0, 500.0
GTILT = -0.30
GLON0 = 42.0
GY0 = -GLON0 * math.pi / 180.0
GSPIN = 60.0
GLAND_KEEP = 0.14                   # poster 陆地抽稀（球小了，0.20 会糊成实心）
GINTRO = 0.9

D2R = math.pi / 180.0


def _nz(v):
    m = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) or 1.0
    return (v[0] / m, v[1] / m, v[2] / m)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _ll2v(lat, lon, r=1.0):
    p, l = lat * D2R, lon * D2R
    c = math.cos(p)
    return (c * math.sin(l) * r, math.sin(p) * r, c * math.cos(l) * r)


def _rotY(v, a):
    s, c = math.sin(a), math.cos(a)
    return (v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c)


def _rotZ(v, a):
    s, c = math.sin(a), math.cos(a)
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c, v[2])


class Cam:
    """three 的 PerspectiveCamera(FOV) + lookAt(0,0,0) + setViewOffset 的离线等价物。
       给定「球在屏上的半径」反解相机距离 —— 构图先定，参数后算，两边都用这一份。"""

    def __init__(self, gr, cx, cy, ytilt):
        self.gr = gr
        self.CD = math.sqrt(1.0 + (FPX / gr) ** 2)      # |C|：单位球silhouette 半径 = gr
        cy_ = ytilt * self.CD
        self.C = (0.0, cy_, math.sqrt(self.CD ** 2 - cy_ ** 2))
        self.ZA = _nz(self.C)
        self.XA = _nz(_cross((0.0, 1.0, 0.0), self.ZA))
        self.YA = _cross(self.ZA, self.XA)
        self.cx, self.cy = cx, cy

    def project(self, p):
        d = (p[0] - self.C[0], p[1] - self.C[1], p[2] - self.C[2])
        vz = _dot(d, self.ZA)
        if vz > -0.05:
            return None
        return (self.cx + FPX * _dot(d, self.XA) / -vz,
                self.cy - FPX * _dot(d, self.YA) / -vz)

    def front(self, p, r=1.0):
        """球面点是否落在朝前半球（限界判据；r = 该点的实际半径）"""
        return _dot(_nz(p), self.ZA) > r / self.CD


VCAM = Cam(VGR, VCX, VCY, 0.16)
GCAM = Cam(GGR, GCX, GCY, 1.05 / math.hypot(1.05, 4.85))   # 与原型同一个俯角比


def _f1(n):
    return ("%.1f" % n).rstrip("0").rstrip(".") or "0"


def _n3(x):
    """短数字（最多 4 位小数 · 去掉尾零）—— 构建期写 poster 的 SVG 坐标用它。
       与 convoai-info 的 `_n3` **逐字同式**：⑥ 互动星系的 poster 由本文件出，
       两份 deck（info P8 / lab·engine P22）画的是同一批字节。"""
    return ("%.4f" % float(x)).rstrip("0").rstrip(".") or "0"


def _keep(i, frac, salt):
    """确定性随机弃取。**不许用固定步长** —— 黄金角螺旋按 stride 取样会与螺旋自己
       共振，屏上直接一片斜条纹摩尔纹（lab-globe 踩过一次，写在它的页头注里）。"""
    h = math.sin((i + salt) * 127.1) * 43758.5453
    return (h - math.floor(h)) < frac


def _smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3.0 - 2.0 * t)


def _smoother(e0, e1, x):
    """smootherstep（6t⁵−15t⁴+10t³）：一阶与**二阶**导数在两端都归零 ⇒
       相位边界处不但速度接得上，加速度也接得上 —— 波B 的四道相位边界全走它，
       这就是「morph 没有接头」的数学理由（smoothstep 只保证一阶）。"""
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


# ── 声场球：波函数（运行时着色器与这里逐字同式）─────────────────────────────
def _vwave(y, t=0.0):
    return sum(a * math.sin(w * VW0 * t + k * y + p) for a, w, k, p in VHARM)


def _vfib(i, ga, jit):
    """Fibonacci 球面点 + 确定性抖动（与运行时逐字同式）。
       不抖动的话黄金角螺旋在球面上就是一张机制网格，屏上一眼看出是「算出来的」；
       抖一格 mean-spacing 的 0.35 之后才是点云。抖动量固定、无随机源 ⇒
       两次构建逐字节一致，poster 与 WebGL 也永远是同一批点。"""
    y = 1.0 - (2.0 * (i + 0.5)) / VN
    rr = math.sqrt(max(0.0, 1.0 - y * y))
    th = i * ga
    p = [math.cos(th) * rr, y, math.sin(th) * rr]
    h1 = math.sin((i + 1) * 12.9898) * 43758.5453
    j1 = h1 - math.floor(h1) - 0.5
    h2 = math.sin((i + 1) * 78.233) * 24634.6345
    j2 = h2 - math.floor(h2) - 0.5
    ax = (1.0, 0.0, 0.0) if abs(p[1]) > 0.95 else (0.0, 1.0, 0.0)
    t1 = _nz(_cross(p, ax))
    t2 = _cross(p, t1)
    return _nz((p[0] + jit * (j1 * t1[0] + j2 * t2[0]),
                p[1] + jit * (j1 * t1[1] + j2 * t2[1]),
                p[2] + jit * (j1 * t1[2] + j2 * t2[2])))


def _vworld(p, r):
    """object → world：先按呼吸位移撑到 r，再上地轴倾角（poster 只画 t=0，不带自转）"""
    return _rotZ((p[0] * r, p[1] * r, p[2] * r), VTILT)


def _voice_poster():
    """P1 声场球 poster：t=0 的静帧。点云分「前 / 背 / 波峰」三路，线框分「前 / 背」两路。"""
    ga = math.pi * (3.0 - math.sqrt(5.0))
    front, back, hot = [], [], []
    jit = 0.35 * math.sqrt(4.0 * math.pi / VN)
    for i in range(VN):
        if not _keep(i, VPOSTER_KEEP, 11):
            continue
        p = _vfib(i, ga, jit)
        w = _vwave(p[1])
        r = 1.0 + VAMP * w
        wv = _vworld(p, r)
        s = VCAM.project(wv)
        if not s:
            continue
        seg = "M%s %sh.01" % (_f1(s[0]), _f1(s[1]))
        if not VCAM.front(wv, r):
            back.append(seg)
        elif _smoothstep(VHOT[0], VHOT[1], w) > 0.5:
            hot.append(seg)
        else:
            front.append(seg)

    def _poly(pts):
        """一条经/纬线 → 前段串 + 背段串（遇到限界就断笔，两路各自成 path）"""
        fd, bd, fo, bo = "", "", False, False
        for p in pts:
            w = _vwave(p[1])
            r = 1.0 + VAMP * w
            wv = _vworld(p, r)
            s = VCAM.project(wv)
            if not s:
                fo = bo = False
                continue
            if VCAM.front(wv, r):
                fd += ("L" if fo else "M") + _f1(s[0]) + " " + _f1(s[1])
                fo, bo = True, False
            else:
                bd += ("L" if bo else "M") + _f1(s[0]) + " " + _f1(s[1])
                bo, fo = True, False
        return fd, bd

    wf, wb = "", ""
    for lon in range(-180, 180, 30):                      # 12 条经线
        a, b = _poly([_ll2v(lat, lon) for lat in range(-88, 89, 3)])
        wf += a
        wb += b
    for lat in (-60, -30, 0, 30, 60):                     # 5 条纬线
        a, b = _poly([_ll2v(lat, lon) for lon in range(-180, 181, 3)])
        wf += a
        wb += b
    return {"front": "".join(front), "back": "".join(back), "hot": "".join(hot),
            "wire": wf, "wireB": wb,
            "n": len(front) + len(back) + len(hot)}


# ── 地球：poster（lab-globe 的四路，按 P21 构图重投影）──────────────────────
def _gworld(v):
    return _rotZ(_rotY(v, GY0), GTILT)


def _globe_poster():
    import base64 as _b64
    bits = _b64.b64decode(LAND_BITS)
    ga = math.pi * (3.0 - math.sqrt(5.0))
    jit = 0.35 * math.sqrt(4.0 * math.pi / LAND_N)
    land = []
    for i in range(LAND_N):
        if not (bits[i >> 3] & (1 << (i & 7))):
            continue
        if not _keep(i, GLAND_KEEP, 7):
            continue
        y = 1.0 - (2.0 * (i + 0.5)) / LAND_N
        rr = math.sqrt(max(0.0, 1.0 - y * y))
        th = i * ga
        p = [math.cos(th) * rr, y, math.sin(th) * rr]
        # 确定性抖动：与运行时逐字同式（打散黄金角螺旋的摩尔纹）
        h1 = math.sin((i + 1) * 12.9898) * 43758.5453
        j1 = h1 - math.floor(h1) - 0.5
        h2 = math.sin((i + 1) * 78.233) * 24634.6345
        j2 = h2 - math.floor(h2) - 0.5
        ax = (1.0, 0.0, 0.0) if abs(p[1]) > 0.95 else (0.0, 1.0, 0.0)
        t1 = _nz(_cross(p, ax))
        t2 = _cross(p, t1)
        p = _nz((p[0] + jit * (j1 * t1[0] + j2 * t2[0]),
                 p[1] + jit * (j1 * t1[1] + j2 * t2[1]),
                 p[2] + jit * (j1 * t1[2] + j2 * t2[2])))
        w = _gworld((p[0] * 1.004, p[1] * 1.004, p[2] * 1.004))
        if not GCAM.front(w, 1.004):
            continue
        s = GCAM.project(w)
        if s:
            land.append("M%s %sh.01" % (_f1(s[0]), _f1(s[1])))

    def _push(pts, r):
        d, open_ = "", False
        for v in pts:
            w = _gworld((v[0] * r, v[1] * r, v[2] * r))
            if not GCAM.front(w, r):
                open_ = False
                continue
            s = GCAM.project(w)
            if not s:
                open_ = False
                continue
            d += ("L" if open_ else "M") + _f1(s[0]) + " " + _f1(s[1])
            open_ = True
        return d

    grat = ""
    for lon in range(-180, 180, 30):
        grat += _push([_ll2v(lat, lon) for lat in range(-88, 89, 3)], 1.001)
    for lat in (-60, -30, 0, 30, 60):
        grat += _push([_ll2v(lat, lon) for lon in range(-180, 181, 3)], 1.001)

    nodes = []
    for lat, lon in _NODES_LL:
        w = _gworld(_ll2v(lat, lon, 1.012))
        if not GCAM.front(w, 1.012):
            continue
        s = GCAM.project(w)
        if s:
            nodes.append("M%s %sh.01" % (_f1(s[0]), _f1(s[1])))

    # 三条弧：从「两端都朝前」的取道里取首 / 中 / 末（与原型同一条挑法）
    picks = []
    for ia, ib in _ROUTES:
        wa = _gworld(_ll2v(*_NODES_LL[ia]))
        wb = _gworld(_ll2v(*_NODES_LL[ib]))
        if GCAM.front(wa) and GCAM.front(wb):
            picks.append((ia, ib))
    arcs = []
    for ia, ib in ([picks[0], picks[len(picks) // 2], picks[-1]] if picks else []):
        a = _nz(_ll2v(*_NODES_LL[ia]))
        b = _nz(_ll2v(*_NODES_LL[ib]))
        om = math.acos(max(-1.0, min(1.0, _dot(a, b))))
        so = math.sin(om)
        lift = 0.028 + 0.215 * (om / math.pi)
        d, open_ = "", False
        for k in range(73):
            t = k / 72.0
            if so < 1e-6:
                p = a
            else:
                p = tuple((a[j] * math.sin((1 - t) * om) + b[j] * math.sin(t * om)) / so for j in range(3))
            p = _nz(p)
            sc = 1.0 + lift * math.sin(math.pi * t)
            w = _gworld((p[0] * sc, p[1] * sc, p[2] * sc))
            if not GCAM.front(w, sc):
                open_ = False
                continue
            s = GCAM.project(w)
            if not s:
                open_ = False
                continue
            d += ("L" if open_ else "M") + _f1(s[0]) + " " + _f1(s[1])
            open_ = True
        if len(d) > 24:
            arcs.append(d)
    return {"land": "".join(land), "grat": grat, "nodes": "".join(nodes), "arcs": arcs,
            "nLand": len(land), "nNode": len(nodes)}


VPOSTER = _voice_poster()
GPOSTER = _globe_poster()

# ═══════════════════════════════════════════════════════════════════════════
# lab-kit · 构建期几何预处理（2026-08-31 第一波「全量 3D 化」新增）
# ───────────────────────────────────────────────────────────────────────────
#   本轮的五枚新场景（P4 / P7 / P9 / P17 / P18）全部**踩在各页现有 SVG 的几何上**：
#   3D 不是另画一张图，而是把这张图**升到三维**。所以坐标真相只有一份 ——
#   页上的那些 `d=` 路径字符串。这里把它们在构建期展平成折线，随 lab_k() 一起
#   发给运行时；运行时一个坐标都不新造。
#
#   为什么在构建期展平：① 运行时不必带一个贝塞尔解析器；② 展平结果与 poster 用的是
#   同一批控制点 ⇒ 「3D 形」与「SVG 降级形」天然同源（P17 的点云限界就是 SVG 那条
#   13 段贝塞尔本人）；③ 无随机源、两次构建逐字节一致。
# ═══════════════════════════════════════════════════════════════════════════


def _pathpts(d, per=14):
    """极简 SVG path 展平器：吃 M / L / H / V / C / Z（本 deck 的图形件只用这几个）。
       per = 每段三次贝塞尔的采样段数。返回**子路径列表** [[(x,y),...], ...] ——
       04 深部区是一枚环（外圈 + 内圈两条子路径），并成一条会把洞填掉。
       ⚠ 不支持 A / S / 相对指令 —— 页上真出现了会当场抛，不会静默画错。
       （2026-08-31 第二波补上 Q / T：P11 那条「对话 · 连续不卡顿」的波浪用的就是它们。）"""
    toks = _re2.findall(r"[MLHVCQTZmlhvcqtz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    subs, cur, i, cx, cy, sx, sy, cmd = [], [], 0, 0.0, 0.0, 0.0, 0.0, None
    qx, qy = None, None                      # 上一段二次贝塞尔的控制点（T 要反射它）

    def num():
        nonlocal i
        v = float(toks[i]); i += 1
        return v

    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in "Zz":
                cx, cy = sx, sy
                if cur:
                    cur.append((sx, sy))
                continue
        if cmd is None:
            raise SystemExit("path 展平：缺起手指令 %r" % d[:40])
        if cmd == "M":
            if cur:
                subs.append(cur)
            cx, cy = num(), num(); sx, sy = cx, cy
            cur = [(cx, cy)]; cmd = "L"
        elif cmd == "L":
            cx, cy = num(), num(); cur.append((cx, cy))
        elif cmd == "H":
            cx = num(); cur.append((cx, cy))
        elif cmd == "V":
            cy = num(); cur.append((cx, cy))
        elif cmd == "C":
            x1, y1, x2, y2, x3, y3 = num(), num(), num(), num(), num(), num()
            for k in range(1, per + 1):
                u = k / per
                v = 1.0 - u
                cur.append((v*v*v*cx + 3*v*v*u*x1 + 3*v*u*u*x2 + u*u*u*x3,
                            v*v*v*cy + 3*v*v*u*y1 + 3*v*u*u*y2 + u*u*u*y3))
            cx, cy = x3, y3
            qx, qy = None, None
        elif cmd in ("Q", "T"):
            # 2026-08-31 第二波补：二次贝塞尔（P11 那条「对话 · 连续不卡顿」的波浪
            # 用的正是 Q + 一串 T）。T 的控制点 = 上一控制点关于当前点的反射；
            # 上一条不是 Q/T 时反射退化成当前点（SVG 规范原文）。
            if cmd == "Q":
                x1, y1 = num(), num()
            else:
                x1 = 2 * cx - qx if qx is not None else cx
                y1 = 2 * cy - qy if qy is not None else cy
            x2, y2 = num(), num()
            for k in range(1, per + 1):
                u = k / per
                v = 1.0 - u
                cur.append((v*v*cx + 2*v*u*x1 + u*u*x2, v*v*cy + 2*v*u*y1 + u*u*y2))
            qx, qy = x1, y1
            cx, cy = x2, y2
        else:
            raise SystemExit("path 展平：不支持的指令 %r（%r）" % (cmd, d[:40]))
    if cur:
        subs.append(cur)
    return subs


def _decim(pts, tol=1.4):
    """等距抽稀：相邻点距离小于 tol 的丢掉（贝塞尔均匀采样在直段上会挤成一堆）。
       只是压体积，形不变 —— 抽完的折线仍逐点落在原曲线上。"""
    out = [pts[0]]
    for p in pts[1:]:
        if (p[0] - out[-1][0]) ** 2 + (p[1] - out[-1][1]) ** 2 >= tol * tol:
            out.append(p)
    if out[-1] != pts[-1]:
        out.append(pts[-1])
    return out


def _pk1(pts, k=1, dx=0.0, dy=0.0):
    """折线 → 紧凑串「x,y;x,y;…」（k = 小数位，dx/dy = 局部坐标平移）"""
    f = "%%.%df" % k
    def g(v):
        s = (f % v)
        return (s.rstrip("0").rstrip(".") or "0")
    return ";".join(g(p[0] - dx) + "," + g(p[1] - dy) for p in pts)


def _poly(d, per=14, tol=1.4, dx=0.0, dy=0.0):
    """单子路径的展平串（页上绝大多数图形件都是这一类）"""
    return _pk1(_decim(_pathpts(d, per)[0], tol), 1, dx, dy)


def _polym(d, per=14, tol=1.4):
    """多子路径的展平串（子路径之间用 | 隔开；运行时按 even-odd 判内外）"""
    return "|".join(_pk1(_decim(s, tol)) for s in _pathpts(d, per))


def _bbox(d, per=14):
    xs, ys = [], []
    for s in _pathpts(d, per):
        for p in s:
            xs.append(p[0]); ys.append(p[1])
    return [min(xs), min(ys), max(xs), max(ys)]


def _sec(s):
    """「2.4s」/「-1.1s」→ 浮点秒（页上的周期与负起相位逐字搬过来）"""
    return float(str(s).strip().rstrip("s"))


# ── ⑥ 互动星系（P22）的材质 token 与 poster 画法：**三份 deck 共用这一份** ──────
#   info（P8）与引擎母本（P22）都现取这三段字符串 —— 一处改，三处一起动。
#   ⚠ `--l-agent` / `--l-phys` 是 convoai-info 自己的产品线色（那份 deck 的 :root 里
#     有），lab / engine 没有 ⇒ 一律写成 `var(--l-agent,#5b8cff)` 这样**带兜底**的形式：
#     在 info 里仍解析成它自己的变量（像素不变），在 lab / engine 里落到同一枚 hex。
#     浅 / 暗两档的兜底值 = info 两档的取值（浅 #5b8cff/#7b61ff · 暗 #6e96ff/#b78cf0）。
GX_LIGHT = """  /* ── ⑥ 互动星系（P22 末页 · 展望）· 浅底 ──
     色彩纪律：**形**负责分辨三环（实心球核 / 一圈交错点 / 一圈在生长的点），
     色负责分辨三种身份 —— 人 = accent（浅底走 accent-deep 那一档的墨）、
     智能体 = --l-agent 蓝、智能体网 = 蓝紫两色各半。
     浅底走正常混合（同样的墨越叠越灰）⇒ 不透明度整体比暗档高一档、点径粗一档。 */
  --gx-core:var(--accent);      --gx-core-op:.74;  --gx-core-size:2.8;  /* 核 · 人与人 */
  --gx-core-hot:var(--accent-deep);                --gx-core-gain:.60;
  --gx-in-a:var(--accent-deep); --gx-in-a-op:.70;  --gx-in-size:2.8;    /* 内环 · 人 */
  --gx-in-b:var(--l-agent,#5b8cff); --gx-in-b-op:.74;                   /* 内环 · 智能体 */
  --gx-out-a:#3b6ae6;           --gx-out-a-op:.64; --gx-out-size:2.6;   /* 外环 · 智能体 */
  --gx-out-b:#5a41e6;           --gx-out-b-op:.64;                      /* 外环 · 智能体网 */
  --gx-arc:#4a54e2;             --gx-arc-op:.52;                        /* 智能体间弧 */
  --gx-spark:var(--accent);     --gx-spark-op:.88; --gx-spark-size:4.6; /* 弧上的亮斑 */
  --gx-flow:var(--accent);      --gx-flow-op:.40;                       /* 互动流：峰值色 */
  --gx-rms:var(--accent-deep);  --gx-rms-op:.44;                        /* 互动流：RMS 实芯 */
  --gx-rad:var(--l-agent,#5b8cff); --gx-rad-op:.36;                     /* 径向流：峰值色 */
  --gx-rad-rms:#3b6ae6;         --gx-rad-rms-op:.40;
  /* 三枚外缘轮廓环 —— 图的身份（P17 的母形轮廓环同位） */
  --gx-rim:var(--ink-3);        --gx-rim-op:.52;
  --gx-back:.34;                --gx-add:0;
  --gx-poster-dot:2.6;   --gx-poster-p1:.86;  --gx-poster-p2:.74;
  --gx-poster-p3:.60;    --gx-poster-rim:.42; --gx-poster-flow:.46;
  --gx-poster-arc:.40;
"""
GX_DARK = """  /* ⑥ 互动星系 · 暗底：走加色混合，同样的墨越叠越亮 ⇒ 不透明度整体收一档、
     点径收一档；实芯换白芯（身份由峰值色承担），弧与径向流压到「在，但不抢」。 */
  --gx-core:var(--accent);      --gx-core-op:.66;  --gx-core-size:2.6;
  --gx-core-hot:var(--accent);                     --gx-core-gain:.85;
  --gx-in-a:var(--accent);      --gx-in-a-op:.60;  --gx-in-size:2.6;
  --gx-in-b:var(--l-agent,#6e96ff); --gx-in-b-op:.64;
  --gx-out-a:var(--l-agent,#6e96ff); --gx-out-a-op:.54; --gx-out-size:2.5;
  --gx-out-b:var(--l-phys,#b78cf0);  --gx-out-b-op:.54;
  --gx-arc:var(--l-agent,#6e96ff);   --gx-arc-op:.44;
  --gx-spark:var(--accent);     --gx-spark-op:.86; --gx-spark-size:4.4;
  --gx-flow:var(--accent);      --gx-flow-op:.36;
  --gx-rms:var(--ink);          --gx-rms-op:.38;
  --gx-rad:var(--l-agent,#6e96ff);   --gx-rad-op:.32;
  --gx-rad-rms:var(--ink);      --gx-rad-rms-op:.34;
  --gx-rim:var(--ink-3);        --gx-rim-op:.42;
  --gx-back:.26;                --gx-add:1;
  --gx-poster-dot:2.4;   --gx-poster-p1:.80;  --gx-poster-p2:.66;
  --gx-poster-p3:.52;    --gx-poster-rim:.30; --gx-poster-flow:.40;
  --gx-poster-arc:.32;
"""
# poster 的分件：三环各一层抽稀点（零长子路径 + round 线帽 = 点，与 P1/P21 的
# poster 同法）、24 条智能体间弧、20 条流中线、三枚外缘椭圆。一个字都没有。
GX_POSTER = """.gx-p1{fill:none;stroke:var(--gx-core);stroke-width:var(--gx-poster-dot);
  stroke-linecap:round;opacity:var(--gx-poster-p1,.86);}
.gx-p2{fill:none;stroke:var(--gx-in-b);stroke-width:var(--gx-poster-dot);
  stroke-linecap:round;opacity:var(--gx-poster-p2,.74);}
.gx-p2a{fill:none;stroke:var(--gx-in-a);stroke-width:var(--gx-poster-dot);
  stroke-linecap:round;opacity:var(--gx-poster-p2,.74);}
.gx-p3{fill:none;stroke:var(--gx-out-a);stroke-width:var(--gx-poster-dot);
  stroke-linecap:round;opacity:var(--gx-poster-p3,.60);}
.gx-p3b{fill:none;stroke:var(--gx-out-b);stroke-width:var(--gx-poster-dot);
  stroke-linecap:round;opacity:var(--gx-poster-p3,.60);}
.gx-rim{fill:none;stroke:var(--gx-rim);stroke-width:1.4;opacity:var(--gx-poster-rim,.42);}
.gx-flow{fill:none;stroke:var(--gx-flow);stroke-width:2.1;stroke-linecap:round;
  opacity:var(--gx-poster-flow,.56);}
.gx-arc{fill:none;stroke:var(--gx-arc);stroke-width:1.3;opacity:var(--gx-poster-arc,.40);}
"""
GX_CSS = ":root{\n" + GX_LIGHT + '}\nhtml[data-theme="dark"]{\n' + GX_DARK + "}\n" + GX_POSTER

# ── LAB 材质 token + 舞台层 CSS ────────────────────────────────────────────
#   --v-* 声场球 / --g-* 地球 / --b-* 大脑 / --s-* 防御壳 / --r-* 复利螺旋 /
#   --t-* 声学地形 / --d-* 双向声带：**three.js 里一个色号都不写**，全部
#   getComputedStyle 读这里；换主题时 MutationObserver 重读并热更新 uniform。
#   浅底 = 近黑线稿（纸面），暗底 = accent 霓虹（深空）—— 与 lab-globe 同一套语汇，
#   只是 conf 家族的 accent 是玫红 / 淡紫，不是 base 的暖橙（token 名一致，取值跟家族）。
LAB_CSS = """<style id="convoai-lab-3d">
:root{
  /* ── 声场球 · 浅底：纸面上的近黑点云，波峰走 accent ── */
  --v-ink:var(--ink);      --v-dot-op:.94;  --v-dot-size:.0138; --v-dot-min:1.1;
  --v-hot:var(--accent);   --v-hot0:.18;    --v-hot1:.70;  --v-hot-gain:.40;
  --v-wire:var(--ink);     --v-wire-op:.40;
  --v-back:.46;            --v-add:0;
  --v-atmo:var(--accent);  --v-atmo-int:.06;
  --v-poster-dot:2.8;
  /* ── 地球 · 浅底 = 近黑线稿 + accent 节点（lab-globe 逐条同源）── */
  --g-ocean:#f2f2f5;   --g-shade:.34;
  --g-rim:var(--ink);  --g-rim-int:1;    --g-rim-pow:4.2;
  --g-land:var(--ink); --g-land-op:.92;  --g-land-size:.0058; --g-land-lit:.14;
  --g-grat:var(--ink); --g-grat-op:.20;
  --g-node:var(--accent);      --g-node-op:1;   --g-node-size:.0124;
  --g-halo:var(--accent);      --g-halo-op:.40; --g-halo-size:.030; --g-halo-add:0;
  --g-arc:var(--accent-deep);  --g-arc-op:.85;
  --g-head:var(--accent-deep); --g-head-op:.95; --g-head-size:.0128; --g-head-add:0;
  --g-atmo:var(--accent);      --g-atmo-int:.11;
  --g-poster-dot:2.2;  --g-poster-node:4.4;
  /* ── ③ 大脑点云（P17）· 浅底 = 纸面上的体积线稿，放电区走 accent ── */
  --b-ink:var(--ink);          --b-op:.86;  --b-size:2.15; --b-back:.30;
  --b-hot:var(--accent);       --b-gain:.85;   --b-cap:.62; --b-add:0;
  --b-arc:var(--accent-deep);  --b-arc-op:.42;
  --b-spark:var(--accent);     --b-spark-op:.92; --b-spark-size:5.2; --b-spark-add:0;
  --b-flow:var(--accent-deep); --b-flow-op:.80;  --b-flow-size:4.6;
  --b-atmo:var(--accent);      --b-atmo-int:.045;
  /* ── ④ 双层防御壳（P9）· 浅底 ── */
  --s-shell:var(--ink);        --s-shell-op:.20; --s-shell-pow:3.6;
  --s-inner:var(--accent);     --s-inner-op:.18;
  --s-grid:var(--ink);         --s-grid-op:.28;
  --s-n1:var(--ink-3);         --s-n1-op:.52;
  --s-n2:var(--ink-2);         --s-n2-op:.44;
  --s-n3:var(--accent-deep);   --s-n3-op:.82;   --s-noise-size:4;
  --s-target:var(--accent);    --s-target-op:.95; --s-target-size:5;
  --s-core:var(--accent);      --s-core-op:.95;  --s-core-size:4.2;
  --s-add:0;
  /* ── ⑤ 复利螺旋（P18）· 浅底 ── */
  --r-band:var(--accent);      --r-band-op:.76;
  --r-rail:var(--accent);      --r-rail-op:.88;
  --r-node:var(--accent);      --r-node-op:1;    --r-node-size:12;
  --r-spark:var(--accent-deep);--r-spark-op:.92; --r-spark-size:4.6;
  /* 波A：LOOP 投影锁空间环带 + 站点圆的底色 + 补回的「真人销冠」基准虚线 */
  --r-loop:var(--accent);      --r-loop-op:.88;
  --r-loop-rms:var(--accent-deep); --r-loop-rms-op:.85;
  --r-fill:var(--card-bg-2);   --r-fill-op:1;
  --r-base:var(--hair-strong); --r-base-op:.80;
  --r-add:0;
  /* ── ⑥ 声学地形（P7）· 浅底 ── */
  --t-ridge:var(--ink);        --t-ridge-op:.92;
  --t-crest:var(--accent);     --t-crest-op:.85;
  --t-band:var(--accent-deep); --t-band-op:.13;
  --t-prob:var(--accent);      --t-prob-op:.90;
  --t-pillar:var(--accent-deep);--t-pillar-op:.72;
  --t-sem:var(--accent-deep);  --t-sem-op:.70;
  /* 波B 消闪：判定晕 / 语义流带的 RMS 芯 / 前沿馈送带 */
  --t-halo:var(--accent);      --t-halo-op:.80; --t-halo-size:3.4;
  --t-sem-rms:var(--accent);   --t-sem-rms-op:.55;
  --t-feed:var(--accent);      --t-feed-op:.45;
  --t-add:0;
  /* ── ⑦ 全双工双向声带（P4）· 浅底 ── */
  --d-up:var(--accent);        --d-up-op:.70;
  --d-dn:var(--ink-2);         --d-dn-op:.44;
  --d-lap:var(--accent);       --d-lap-op:.95;
  --d-pkt:var(--accent);       --d-pkt-op:.92; --d-pkt-size:4.4;
  --d-cut:var(--accent-deep);  --d-cut-op:.75;
  --d-add:0;
  /* ══ 第二波 · 九枚场景（2026-08-31 终波）· 浅底 = 纸面线稿 ══════════════════
     前缀表：--o-* 决策轨道环(P2) / --l-* 双工三通道(P3) / --c-* 语音链路(P6) /
             --u-* 打断时序(P8) / --m-* 产品大图(P10) / --q-* 弱网 QoS(P11) /
             --w-* 视觉模态(P12) / --k-* 编排插槽(P13) / --y-* 三塔握手(P14) */
  /* --o-* 波B：模态转换剧场（P2）—— 波场走 accent（听得见的那一路），
     星格走近黑墨（想是纸面上的结构），经线是格的骨架，弧是第二道入射波 */
  --o-wave:var(--accent);      --o-wave-op:.62;
  --o-lat:var(--ink);          --o-lat-op:.95;
  --o-wire-op:.56;             --o-dot-size:3;  --o-dot-w:2.6;
  --o-arc:var(--accent-deep);  --o-arc-op:.70;
  --o-arc-rms:var(--accent);   --o-arc-rms-op:.55;
  /* 02「两制对照」：回合制走灰（note 语域，与旧注脚条同一档色阶），
     边说边听走 accent（听得见的那一路），事件标走 accent-deep（离散事件） */
  --o-anti:var(--ink-3);       --o-anti-op:.66;
  --o-anti-rms:var(--ink-2);   --o-anti-rms-op:.42;
  --o-live:var(--accent);      --o-live-op:.66;
  --o-live-rms:var(--accent-deep); --o-live-rms-op:.55;
  --o-evt:var(--accent-deep);  --o-evt-op:.92;
  --o-add:0;
  /* ④ 表达力精进 · 第二波：整格提亮一档 —— 旧值在 3 米外读不出「谁在说」 */
  --l-on:var(--accent);        --l-on-op:.94;
  --l-off:var(--hair-strong);  --l-off-op:.88;
  --l-rail:var(--accent);      --l-rail-op:.90;
  --l-dead:var(--ink-3);       --l-dead-op:.42;
  --l-axis:var(--hair-strong); --l-axis-op:.92;
  --l-pkt:var(--accent);       --l-pkt-op:.95;  --l-pkt-size:7;
  --l-fill-op:.86;
  --l-lap:var(--accent-deep);  --l-lap-op:.30;
  --l-add:0;
  --c-face:var(--ink-2);       --c-face-op:.96;
  --c-hot:var(--accent);       --c-hot-op:.95;
  --c-shell:var(--ink-3);      --c-shell-op:.66;
  --c-rail:var(--ink-3);       --c-rail-op:.52;
  --c-span:var(--accent);      --c-span-op:.42;
  --c-fork:var(--ink-3);       --c-fork-op:.50;
  --c-band:var(--accent);      --c-band-op:.42;
  --c-pkt:var(--accent);       --c-pkt-op:.92;  --c-pkt-size:7;
  --c-glyph-op:.85;
  /* 波A：横贯全链那条流 + 它的 RMS 芯 + token 段的载流垫底 */
  --c-stream:var(--accent);    --c-stream-op:.56;
  --c-rms:var(--accent-deep);  --c-rms-op:.58;
  --c-bed:var(--accent);       --c-bed-op:.54;
  --c-add:0;
  --u-agent:var(--accent);     --u-agent-op:.62;
  --u-user:var(--ink-2);       --u-user-op:.46;
  --u-fast:var(--accent-deep); --u-fast-op:.82;
  --u-cut:var(--hair-strong);  --u-cut-op:.62;
  --u-pkt-op:.95;              --u-pkt-size:8;
  /* 波A：连续媒体流的第二层 —— 峰值淡壳之内那一芯 RMS（Audition 的波形是两层） */
  --u-rms:var(--accent-deep);  --u-rms-b:var(--ink);   --u-rms-op:.62;
  --u-add:0;
  --m-face:var(--ink-2);       --m-face-op:.86;
  --m-hot:var(--accent);
  --m-shell:var(--ink-3);      --m-shell-op:.48;
  --m-lane:var(--accent);      --m-lane-op:.60;
  --m-beam:var(--accent-deep); --m-beam-op:.46;
  --m-pkt:var(--accent);       --m-pkt-op:.92;  --m-pkt-size:6.5;
  /* 波B 轻手术：车道与握手的连续流带（峰值淡壳 + RMS 实芯） */
  --m-flow:var(--accent);      --m-flow-op:.34;
  --m-flow-rms:var(--accent-deep); --m-flow-rms-op:.55;
  --m-add:0;
  --q-heap:var(--accent);      --q-heap-op:.52; --q-heap-size:3.4;
  --q-hot:var(--accent-deep);
  --q-wire:var(--ink-3);       --q-wire-op:.95;
  --q-pkt:var(--accent);       --q-pkt-op:.92;  --q-pkt-size:6;
  --q-out:var(--accent);       --q-out-op:.55;
  --q-bar:var(--accent);       --q-bar-op:.78;
  --q-lost:var(--hair-strong); --q-lost-op:.34;
  --q-dom:var(--accent-deep);  --q-dom-op:.20;
  --q-mech:var(--ink-2);       --q-mech-op:.55;
  --q-hot2:var(--accent);      --q-mechhot-op:.95;
  --q-add:0;
  --w-face:var(--ink-2);       --w-face-op:.86;
  --w-hot:var(--accent);       --w-hot-op:.95;
  --w-shell:var(--ink-3);      --w-shell-op:.48;
  --w-cone:var(--accent-deep); --w-cone-op:.66;
  --w-plane:var(--accent);     --w-plane-op:.90;
  --w-weak:var(--ink-3);       --w-weak-op:.44;
  --w-pkt:var(--accent);       --w-pkt-op:.92;  --w-pkt-size:6.5;
  --w-add:0;
  --k-sock:var(--ink-2);       --k-sock-op:.52;
  --k-wall:var(--ink-3);       --k-wall-op:.62;
  --k-hub:var(--accent);       --k-hub-op:.95;
  --k-bus:var(--accent);       --k-bus-op:.58;
  --k-plate:var(--accent);     --k-plate-op:.80;
  --k-pkt:var(--accent);       --k-pkt-op:.92;  --k-pkt-size:6.5;
  --k-pill-op:.42;
  /* 波B · 编排中枢机：内肋 / 呼吸核 / 异面环 / 发布脉冲 / 往返闭环 /
     模块小巧思 / 候选机体 / 贯通流（不透明度是常数，与 swap 相位零耦合） */
  --k-rib:var(--ink-3);        --k-rib-op:.74;
  --k-core:var(--accent);      --k-core-op:.80; --k-core-size:3.4;
  --k-ring:var(--accent-deep); --k-ring-op:.58;
  --k-pub:var(--accent-deep);  --k-pub-op:.90;
  --k-loop:var(--accent);      --k-loop-op:.52;
  --k-giz:var(--accent-deep);  --k-giz-op:.82; --k-giz-size:3.2;
  --k-cand:var(--ink-3);
  --k-flow:var(--accent);      --k-flow-op:.26;
  --k-flow-rms:var(--accent-deep); --k-flow-rms-op:.55;
  --k-add:0;
  --y-face:var(--ink-2);       --y-face-op:.86;
  --y-hot:var(--accent);       --y-hot-op:.95;
  --y-wall:var(--ink-3);       --y-wall-op:.48;
  --y-arc:var(--accent-deep);  --y-arc-op:.55;
  --y-head:var(--accent);      --y-head-op:1;   --y-head-size:7.5;
  /* 波A：光束生长（管腔注光）与塔右内缘的楼层灯瀑 */
  --y-beam:var(--accent-deep); --y-beam-op:.86;
  --y-floor:var(--accent);     --y-floor-op:.95; --y-floor-size:5.2;
  --y-add:0;
  /* ═══ 三轮「静态页升维」· 三枚加法层 ═══════════════════════════════════
     三枚共同的色域纪律：它们画在**既有版面之外**的空档里，所以整体比另外 17 页
     更暗一档。（2026-09-03：P22 的 --e-* 随「余韵星野」一起退役 —— 末页换成了
     在页 3D 的互动星系，材质走本段末尾的 --gx-*。） */
  /* ── P5 三件极致的底场（伴奏：墨量 ≤ 三卡的 25%）── */
  /* ⑤：集流带比旧的三条微线粗得多，墨量得往回收一档（㉒d 上限 = 三卡的 25%）*/
  --x-flow:var(--accent);      --x-flow-op:.32;
  --x-rms:var(--accent-deep);  --x-rms-op:.50;
  --x-noise:var(--ink-3);      --x-noise-op:.30;
  --x-haze:var(--ink-3);       --x-haze-op:.17; --x-haze-size:2.0;
  --x-beam:var(--accent-deep); --x-beam-op:.88;
  --x-shield:var(--ink-2);     --x-shield-op:.62;
  --x-add:0;
  /* ── P15 中心辐射（核与支线在卡间空档全亮；六簇在卡背后透出三成）── */
  /* ⑦：迷你转子提亮 —— 它得让人一眼认出「那台在 P13 上见过的引擎」 */
  --h-core:var(--accent);      --h-core-op:.78; --h-core-size:2.6;
  --h-dot:var(--accent-deep);  --h-dot-op:.95;  --h-dot-gain:.55;
  --h-ring:var(--accent-deep); --h-ring-op:.92;
  --h-spoke:var(--accent);     --h-spoke-op:.42;
  --h-rms:var(--accent-deep);  --h-rms-op:.58;
  --h-node:var(--accent);      --h-node-op:1;   --h-node-size:4.6;
  --h-far:var(--ink-2);        --h-far-op:1;    --h-far-size:3.4;
  --h-add:0;
  /* ── P16 通话流（均质一束 —— 不给任何一张卡加权，96.5% 的 hot 是页面的事）── */
  /* ⑥：整束提亮 —— 八条 1.8 半宽的细带铺在 30px 的窄带里，旧的 .34 在屏上没有 */
  --n-flow:var(--accent);      --n-flow-op:.70;
  --n-rms:var(--accent-deep);  --n-rms-op:.60;
  --n-add:0;
""" + GX_LIGHT + """}
html[data-theme="dark"]{
  --v-ink:var(--ink-2);    --v-dot-op:.84;  --v-dot-size:.0120; --v-dot-min:1.1;
  --v-hot:var(--accent);   --v-hot0:.16;    --v-hot1:.66;  --v-hot-gain:.80;
  --v-wire:var(--ink);     --v-wire-op:.22;
  --v-back:.26;            --v-add:1;
  --v-atmo:var(--accent);  --v-atmo-int:.17;
  --v-poster-dot:2.6;
  /* ── 地球 · 暗底 = 深空霓虹 ── */
  --g-ocean:#07070c;   --g-shade:.62;
  --g-rim:var(--accent); --g-rim-int:1;   --g-rim-pow:8.0;
  --g-land:var(--ink-3); --g-land-op:.92; --g-land-size:.0046; --g-land-lit:.58;
  --g-grat:var(--ink);   --g-grat-op:.075;
  --g-node:var(--accent);      --g-node-op:1;   --g-node-size:.0110;
  --g-halo:var(--accent);      --g-halo-op:.38; --g-halo-size:.038; --g-halo-add:1;
  --g-arc:var(--accent-deep);  --g-arc-op:.88;
  --g-head:var(--ink);         --g-head-op:1;   --g-head-size:.0130; --g-head-add:1;
  --g-atmo:var(--accent);      --g-atmo-int:.30;
  --g-poster-dot:2.2;  --g-poster-node:4.4;
  /* ── 大脑 · 暗底 = 深空里的一颗发光脑（加色混合，rim 收在 accent 上）── */
  --b-ink:var(--ink-3);        --b-op:.72;  --b-size:1.95; --b-back:.16;
  --b-hot:var(--accent);       --b-gain:1.55;  --b-cap:.96; --b-add:1;
  --b-arc:var(--accent-deep);  --b-arc-op:.38;
  --b-spark:var(--ink);        --b-spark-op:1;   --b-spark-size:5.0; --b-spark-add:1;
  --b-flow:var(--accent);      --b-flow-op:.95;  --b-flow-size:4.6;
  --b-atmo:var(--accent);      --b-atmo-int:.15;
  /* ── 防御壳 · 暗底 ── */
  --s-shell:var(--ink-2);      --s-shell-op:.10; --s-shell-pow:4.2;
  --s-inner:var(--accent);     --s-inner-op:.15;
  --s-grid:var(--ink);         --s-grid-op:.13;
  --s-n1:var(--ink-3);         --s-n1-op:.46;
  --s-n2:var(--ink-2);         --s-n2-op:.40;
  --s-n3:var(--accent-deep);   --s-n3-op:.80;   --s-noise-size:3.4;
  --s-target:var(--accent);    --s-target-op:1;  --s-target-size:5.2;
  --s-core:var(--accent);      --s-core-op:1;    --s-core-size:4.4;
  --s-add:1;
  /* ── 复利螺旋 · 暗底 ── */
  --r-band:var(--accent);      --r-band-op:.34;
  --r-rail:var(--accent);      --r-rail-op:.92;
  --r-node:var(--accent);      --r-node-op:1;    --r-node-size:12.4;
  --r-spark:var(--ink);        --r-spark-op:1;   --r-spark-size:4.8;
  --r-loop:var(--accent);      --r-loop-op:.58;
  --r-loop-rms:var(--ink);     --r-loop-rms-op:.48;
  --r-fill:var(--card-bg-2);   --r-fill-op:1;
  --r-base:var(--ink-3);       --r-base-op:.72;
  --r-add:1;
  /* ── 声学地形 · 暗底 ── */
  --t-ridge:var(--ink-2);      --t-ridge-op:.48;
  --t-crest:var(--accent);     --t-crest-op:.95;
  --t-band:var(--accent-deep); --t-band-op:.16;
  --t-prob:var(--accent);      --t-prob-op:1;
  --t-pillar:var(--accent-deep);--t-pillar-op:.85;
  --t-sem:var(--accent);       --t-sem-op:.95;
  --t-halo:var(--accent);      --t-halo-op:.86; --t-halo-size:3.5;
  --t-sem-rms:var(--ink);      --t-sem-rms-op:.50;
  --t-feed:var(--accent);      --t-feed-op:.48;
  --t-add:1;
  /* ── 双向声带 · 暗底 ── */
  --d-up:var(--accent);        --d-up-op:.72;
  --d-dn:var(--ink-3);         --d-dn-op:.40;
  --d-lap:var(--ink);          --d-lap-op:1;
  --d-pkt:var(--ink);          --d-pkt-op:1;   --d-pkt-size:4.6;
  --d-cut:var(--accent-deep);  --d-cut-op:.85;
  --d-add:1;
  /* ══ 第二波 · 九枚场景 · 暗底 = 深空霓虹（加色混合，与第一波同一套语汇）══════ */
  --o-wave:var(--accent);      --o-wave-op:.58;
  --o-lat:var(--ink);          --o-lat-op:.50;
  --o-wire-op:.24;             --o-dot-size:3.1; --o-dot-w:2.4;
  --o-arc:var(--accent-deep);  --o-arc-op:.72;
  --o-arc-rms:var(--ink);      --o-arc-rms-op:.50;
  --o-anti:var(--ink-3);       --o-anti-op:.58;
  --o-anti-rms:var(--ink-2);   --o-anti-rms-op:.36;
  --o-live:var(--accent);      --o-live-op:.62;
  --o-live-rms:var(--ink);     --o-live-rms-op:.50;
  --o-evt:var(--accent-deep);  --o-evt-op:1;
  --o-add:1;
  --l-on:var(--accent);        --l-on-op:.92;
  --l-off:var(--ink-3);        --l-off-op:.52;
  --l-rail:var(--accent);      --l-rail-op:.86;
  --l-dead:var(--ink-3);       --l-dead-op:.38;
  --l-axis:var(--ink-3);       --l-axis-op:.44;
  --l-pkt:var(--ink);          --l-pkt-op:1;    --l-pkt-size:7.2;
  --l-fill-op:.70;
  --l-lap:var(--accent);       --l-lap-op:.34;
  --l-add:1;
  --c-face:var(--ink-2);       --c-face-op:.52;
  --c-hot:var(--accent);       --c-hot-op:1;
  --c-shell:var(--ink-3);      --c-shell-op:.20;
  --c-rail:var(--ink-3);       --c-rail-op:.40;
  --c-span:var(--accent);      --c-span-op:.34;
  --c-fork:var(--ink-3);       --c-fork-op:.38;
  --c-band:var(--accent);      --c-band-op:.38;
  --c-pkt:var(--ink);          --c-pkt-op:1;    --c-pkt-size:7.2;
  --c-glyph-op:.9;
  --c-stream:var(--accent);    --c-stream-op:.50;
  --c-rms:var(--ink);          --c-rms-op:.50;
  --c-bed:var(--accent);       --c-bed-op:.16;
  --c-add:1;
  --u-agent:var(--accent);     --u-agent-op:.55;
  --u-user:var(--ink-3);       --u-user-op:.40;
  --u-fast:var(--accent-deep); --u-fast-op:.90;
  --u-cut:var(--ink-3);        --u-cut-op:.46;
  --u-pkt-op:1;                --u-pkt-size:8.2;
  --u-rms:var(--ink);          --u-rms-b:var(--ink);   --u-rms-op:.55;
  --u-add:1;
  --m-face:var(--ink-2);       --m-face-op:.50;
  --m-hot:var(--accent);
  --m-shell:var(--ink-3);      --m-shell-op:.18;
  --m-lane:var(--accent);      --m-lane-op:.52;
  --m-beam:var(--accent-deep); --m-beam-op:.52;
  --m-pkt:var(--ink);          --m-pkt-op:1;    --m-pkt-size:6.6;
  --m-flow:var(--accent);      --m-flow-op:.32;
  --m-flow-rms:var(--ink);     --m-flow-rms-op:.50;
  --m-add:1;
  --q-heap:var(--accent);      --q-heap-op:.44; --q-heap-size:3.3;
  --q-hot:var(--ink);
  --q-wire:var(--ink-3);       --q-wire-op:.34;
  --q-pkt:var(--ink);          --q-pkt-op:1;    --q-pkt-size:6.2;
  --q-out:var(--accent);       --q-out-op:.48;
  --q-bar:var(--accent);       --q-bar-op:.70;
  --q-lost:var(--ink-3);       --q-lost-op:.26;
  --q-dom:var(--accent-deep);  --q-dom-op:.26;
  --q-mech:var(--ink-2);       --q-mech-op:.48;
  --q-hot2:var(--accent);      --q-mechhot-op:1;
  --q-add:1;
  --w-face:var(--ink-2);       --w-face-op:.50;
  --w-hot:var(--accent);       --w-hot-op:1;
  --w-shell:var(--ink-3);      --w-shell-op:.18;
  --w-cone:var(--accent);      --w-cone-op:.28;
  --w-plane:var(--ink);        --w-plane-op:1;
  --w-weak:var(--ink-3);       --w-weak-op:.16;
  --w-pkt:var(--ink);          --w-pkt-op:1;    --w-pkt-size:6.6;
  --w-add:1;
  --k-sock:var(--ink-2);       --k-sock-op:.44;
  --k-wall:var(--ink-3);       --k-wall-op:.18;
  --k-hub:var(--accent);       --k-hub-op:1;
  --k-bus:var(--accent);       --k-bus-op:.50;
  --k-plate:var(--ink);        --k-plate-op:.90;
  --k-pkt:var(--ink);          --k-pkt-op:1;    --k-pkt-size:6.6;
  --k-pill-op:.36;
  --k-rib:var(--ink-3);        --k-rib-op:.24;
  --k-core:var(--accent);      --k-core-op:.82; --k-core-size:3.4;
  --k-ring:var(--ink);         --k-ring-op:.52;
  --k-pub:var(--accent);       --k-pub-op:.95;
  --k-loop:var(--accent);      --k-loop-op:.50;
  --k-giz:var(--ink);          --k-giz-op:.80; --k-giz-size:3.3;
  --k-cand:var(--ink-3);
  --k-flow:var(--accent);      --k-flow-op:.24;
  --k-flow-rms:var(--ink);     --k-flow-rms-op:.50;
  --k-add:1;
  --y-face:var(--ink-2);       --y-face-op:.50;
  --y-hot:var(--accent);       --y-hot-op:1;
  --y-wall:var(--ink-3);       --y-wall-op:.18;
  --y-arc:var(--accent);       --y-arc-op:.50;
  --y-head:var(--ink);         --y-head-op:1;   --y-head-size:7.8;
  --y-beam:var(--accent);      --y-beam-op:.90;
  --y-floor:var(--accent);     --y-floor-op:.66; --y-floor-size:5.4;
  --y-add:1;
  /* ═══ 三轮 · 三枚加法层 · 暗底 ═══════════════════════════════════════ */
  --x-flow:var(--accent);      --x-flow-op:.30;
  --x-rms:var(--accent-deep);  --x-rms-op:.46;
  --x-noise:var(--ink-3);      --x-noise-op:.34;
  --x-haze:var(--ink-3);       --x-haze-op:.18; --x-haze-size:2.0;
  --x-beam:var(--accent);      --x-beam-op:.80;
  --x-shield:var(--ink-2);     --x-shield-op:.55;
  --x-add:1;
  --h-core:var(--accent);      --h-core-op:.76; --h-core-size:2.7;
  --h-dot:var(--ink);          --h-dot-op:1;    --h-dot-gain:.60;
  --h-ring:var(--ink);         --h-ring-op:.86;
  --h-spoke:var(--accent);     --h-spoke-op:.38;
  --h-rms:var(--accent-deep);  --h-rms-op:.52;
  --h-node:var(--accent);      --h-node-op:1;   --h-node-size:4.6;
  --h-far:var(--ink-2);        --h-far-op:.92;  --h-far-size:3.4;
  --h-add:1;
  --n-flow:var(--accent);      --n-flow-op:.66;
  --n-rms:var(--ink);          --n-rms-op:.52;
  --n-add:1;
""" + GX_DARK + """}
/* ── 舞台层：压在 .conf-bg 之上、.pp 正文之下 ─────────────────────────────
   两者都是 z-index:0，靠**文档序**分先后（背景板在前、3D 层在后）——
   不去动 `.slide.conf-boarded>.pp{z-index:1}` 那条家族规则，
   动它会连另外那些页的层叠上下文一起改，pinned 同源自证就没得跑了。

   ⚠ 2026-08-31 第一波重构：全 deck **只有一枚** WebGLRenderer + 一块 canvas。
   canvas 常驻页面（车库 .lab-garage），翻页时被 appendChild 进目标页的
   .lab-stage 并按 data-lab-rect 对位；目标页无场景则回车库。
   canvas 元素在 DOM 里搬家**不会丢 WebGL 上下文**，所以浏览器的
   「同页面 WebGL 上下文上限（多数是 16）」这条限制从根上不存在了 ——
   16 个 3D 页也只吃一枚上下文。 */
.lab-stage{position:absolute;inset:0;z-index:0;pointer-events:none;}
.lab-garage{position:fixed;left:-99999px;top:0;width:0;height:0;overflow:hidden;
  pointer-events:none;opacity:0;}
/* 外辉光：垫在 poster / canvas 之下 —— 球体不透明的部分自己挡掉内圈，只露出限界外
   那一圈。WebGL 路与 poster 路共用这一层，两条路的辉光因此逐像素一致，
   软渲染也省了一整屏片元（lab-globe 的账，原样搬）。 */
.lab-atmo{position:absolute;border-radius:50%;pointer-events:none;}
svg.lab-poster{position:absolute;left:0;top:0;width:1920px;height:1080px;display:block;}
.lab-print{position:absolute;display:block;}
.lab-canvas{position:absolute;display:block;}
/* ── poster 层 = 降级层 ────────────────────────────────────────────────────
   P1/P21：构建期离线投影出来的专用 <svg class="lab-poster">（全屏画布）。
   P4/P7/P9/P17/P18：**该页现有的图形 SVG 原地留用** —— 页内那一段几何被
   <g class="lab-poster"> 裹起来，3D 起来就淡出、canvas 接管；起不来 / print /
   reduced-motion 硬降级 / 离线归档 ⇒ 它原样呈现，那一页仍是完整的 2D 版。
   两种形态共用同一条淡出规则：舞台挂 gl-up ⇒ 舞台内的 poster 与其后 .pp 里的
   poster 一起让位（.lab-stage 是 .pp 的**前置兄弟**，所以 `~` 选得到）。 */
svg .lab-poster,.lab-poster{transition:opacity 1.1s var(--ease-flow,cubic-bezier(.22,.9,.24,1));}
.lab-canvas{opacity:0;transition:opacity .9s var(--ease-flow,cubic-bezier(.22,.9,.24,1));}
.lab-stage.gl-up .lab-poster,
.lab-stage.gl-up ~ .pp .lab-poster{opacity:0;}
.lab-stage.gl-up .lab-canvas{opacity:1;}
.lab-canvas.lab-grab{pointer-events:auto;cursor:grab;}
.lab-canvas.lab-grab:active{cursor:grabbing;}
/* ── P3 的卡窗（2026-08-31 第二波 · 全 deck 独此一处）──────────────────────
   P3 是唯一一页**图形区坐在卡里**的 3D 页：canvas 坐在 .pp 之下，而 .card-c 的底
   是 --card-bg（72% 不透明）—— 不开窗，3D 只剩 28% 的鬼影，比它替换掉的 2D 还弱。
   开法：3D 起来时把卡底换成一条纵向硬分段渐变，在 figure 那一带留一段 transparent。
   两侧仍是原样的 --card-bg（同一个变量，同一档透明度）⇒ 卡的观感一格不变，
   只是中间那条 137px 的带子变成一扇真窗。**不挂 gl-up 就是原来的卡**，
   所以禁 WebGL / print / reduced-motion / 离线归档四条路上，P3 与从前逐像素相同。
   数字来历（改卡的 padding / border / 名字行字号就得重算，量法见 LAB_RECTS 的注）：
     卡 border 1px + padding 20 ⇒ 背景定位区（padding box）自卡顶 +1 起算；
     figure 顶在舞台 y372.74、底在 y506.15 ⇒ 区内 101.7 / 235.1；
     canvas 矩形 y372→507 ⇒ 区内 100.95 / 235.95 —— 窗取 100→237，两头各留 1px 余。 */
   窗里不是全透明，留 26% 的卡底（≈18% 白 / 18% 深）：背景板在这一带正好有几块
   矩阵纹理，全透明会让纹理从窗里跳出来、读成「卡上有一块色斑」；留一薄层压住它，
   canvas 仍有八成通透（实拍比过：全透明 vs 26%，3D 亮度肉眼无差，色斑没了）。 */
.lab-stage.gl-up ~ .pp .p3-win{
  background:linear-gradient(180deg,var(--card-bg) 0 100px,
    color-mix(in srgb,var(--card-bg) 26%,transparent) 100px 237px,
    var(--card-bg) 237px 100%);}
/* 打印帧：常态不存在，beforeprint 时才写 src（见 LAB 运行时的 beforeprint 钩子） */
.lab-print{display:none;}
/* ── poster 画法（与运行时着色器同一套 --v-* / --g-* 取值）────────────────── */
.v-dot{fill:none;stroke:var(--v-ink);stroke-width:var(--v-poster-dot);stroke-linecap:round;
  opacity:var(--v-dot-op);}
.v-dot-b{fill:none;stroke:var(--v-ink);stroke-width:var(--v-poster-dot);stroke-linecap:round;
  opacity:calc(var(--v-dot-op)*var(--v-back));}
.v-dot-h{fill:none;stroke:var(--v-hot);stroke-width:calc(var(--v-poster-dot)*1.2);
  stroke-linecap:round;opacity:1;}
.v-wire{fill:none;stroke:var(--v-wire);stroke-width:1;opacity:calc(var(--v-wire-op)*1.5);}
.v-wire-b{fill:none;stroke:var(--v-wire);stroke-width:1;
  opacity:calc(var(--v-wire-op)*var(--v-back)*1.5);}
.g-ocean{fill:var(--g-ocean);}
.g-rim{fill:none;stroke:var(--g-rim);stroke-width:1.1;opacity:calc(var(--g-rim-int)*.55);}
.g-grat{fill:none;stroke:var(--g-grat);stroke-width:1;opacity:calc(var(--g-grat-op)*1.6);}
.g-land{fill:none;stroke:var(--g-land);stroke-width:var(--g-poster-dot);stroke-linecap:round;
  opacity:calc(var(--g-land-op)*.9);}
.g-node{fill:none;stroke:var(--g-node);stroke-width:var(--g-poster-node);stroke-linecap:round;
  opacity:.92;}
.g-arc{fill:none;stroke:var(--g-arc);stroke-width:1.5;opacity:calc(var(--g-arc-op)*.85);}
/* P2 模态转换剧场的降级层（波B）：t*=12.0 那一帧，构建期逐点算出来 ——
   与顶点着色器同参（同一批 _MO_* 常量、同一组公式）⇒ poster 与 canvas 是同一张图。 */
.p2-wave{fill:none;stroke:var(--o-wave);stroke-width:var(--o-dot-w);stroke-linecap:round;
  opacity:var(--o-wave-op);}
.p2-lat{fill:none;stroke:var(--o-lat);stroke-width:var(--o-dot-w);stroke-linecap:round;
  opacity:var(--o-lat-op);}
.p2-row{fill:none;stroke:var(--o-wave);stroke-width:1;
  opacity:calc(var(--o-wire-op)*.62);}
.p2-wire{fill:none;stroke:var(--o-lat);stroke-width:1;opacity:var(--o-wire-op);}
/* 02「两制对照」的 poster：两排带子的静态包络轮廓（构建期 _p2_env_path 逐点算，
   与 AS_VS 同式）+「想」的虚线框 + 两枚事件竖标。字一个不裹（全在组外）。 */
.p2-anti{fill:var(--o-anti);opacity:var(--o-anti-op);}
.p2-live{fill:var(--o-live);opacity:var(--o-live-op);}
.p2-dash{fill:none;stroke:var(--o-anti);stroke-width:2.4;stroke-linecap:round;
  opacity:var(--o-anti-op);}
.p2-evt{fill:none;stroke:var(--o-evt);stroke-width:3;stroke-linecap:round;
  opacity:var(--o-evt-op);}
.p2-evt-d{fill:var(--o-evt);opacity:var(--o-evt-op);}
/* ── FPS 探针：生产页不挂常显探针，?debug=1 才显出来 ───────────────────── */
.lab-probe{position:fixed;left:26px;top:22px;z-index:1100;font:500 11px/1 var(--f-mono);
  letter-spacing:.13em;color:var(--ink-3);opacity:.62;display:none;gap:9px;align-items:center;
  pointer-events:none;text-shadow:0 0 6px var(--stage-bg);}
html[data-lab-debug] .lab-probe{display:flex;}
.lab-probe b{font-weight:500;color:var(--accent);}
.lab-probe .sep{opacity:.4;}
/* ── 降级语域：纸 / reduced-motion ───────────────────────────────────────
   canvas 藏、poster 显、打印帧（若已抓到）盖在 poster 之上。
   transition 一并掐掉：切到 print 时那 1.1s 淡入还在飞，纸上就印了一张半透明的球。
   ⚠ 纸上 22 页一起铺开，而 canvas 只在其中一页里 —— 所以纸上一律以 poster 为准，
     打印帧只是当前页的一层锦上添花。 */
@media print{
  .lab-canvas{display:none!important;}
  .lab-garage{display:none!important;}
  .lab-poster{opacity:1!important;transition:none!important;}
  .lab-print[src]{display:block!important;}
  .lab-probe{display:none!important;}
}
@media (prefers-reduced-motion:reduce){
  .lab-poster,.lab-canvas{transition-duration:.2s!important;}
}
""" + GX_POSTER + """</style>"""


def _cssmax(name):
    """从 LAB_CSS 里现取某个尺寸变量的**最大值**（浅 / 暗两档取大的那一档）——
       净空探针的 pad 与 poster 的点径因此与页面上真正画出来的那一档同源，
       不会两处各写一个数。（与 convoai-info 的 `_cssmax` 逐字同式。）"""
    v = [float(x) for x in _re2.findall(r"%s\s*:\s*([0-9.]+)" % _re2.escape(name), LAB_CSS)]
    assert v, "LAB_CSS 里找不到 %s" % name
    return max(v)


# ── 投影锁的 Python 同解（⑥ 互动星系的构建期几何要用）─────────────────────
#   mkLock（lab-kit ⑤）：页上的 2D 点 (x,y) 抬到深度 z 之后先按 k=(D−z)/D 预缩放，
#   透视除法正好把这一档除回去 ⇒ **投影落点与 2D 逐像素相同**。
#   构建期把同一式子算一遍：poster 直接按页坐标画、K 表下发的是世界折线，
#   两条路不可能是两套解。（与 convoai-info 的 `_lockpt` / `_lock_path` 逐字同式。）
def _lockpt(x, y, z, w, h, D):
    cx, cy = w / 2.0, h / 2.0
    k = (D - z) / D
    return (cx + (x - cx) * k, -(cy + (y - cy) * k), z)


def _lock_path(pts, w, h, D):
    return [_lockpt(p[0], p[1], p[2] if len(p) > 2 else 0.0, w, h, D) for p in pts]


def _xylen(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
               for i in range(len(pts) - 1))


def _lock_len(pts, w, h, D):
    """(页面 xy 长, 世界 xy 长) —— 前者是屏上看得见的那个长度（data-lab-spd 的分子）"""
    return _xylen([(p[0], p[1]) for p in pts]), _xylen(_lock_path(pts, w, h, D))


def _pk3(pts):
    """世界折线打包成 "x,y,z;…"（构建期算一遍，运行时不再算第二遍）"""
    return ";".join("%s,%s,%s" % (_n3(p[0]), _n3(p[1]), _n3(p[2])) for p in pts)


def _arr3(xs):
    return "[" + ",".join(_n3(v) for v in xs) + "]"


def _wpx(w0, pts, D):
    """一条流带在**屏上**的最大半宽：世界半宽 w0 经透视放大 D/(D−z)，取路径上的最大值"""
    return w0 * max(D / (D - q[2]) for q in pts)


# ═══════════════════════════════════════════════════════════════════════════
# 舞台位表：每个 3D 页的**图形区矩形**（舞台坐标 1920×1080）
# ───────────────────────────────────────────────────────────────────────────
#   这张表是「canvas 巡游」的对位真相：翻到某页 ⇒ 单枚 canvas 被 appendChild
#   进该页的 .lab-stage，并按这里的 (x,y,w,h) 摆好。矩形 = 该页 2D 图形所占的
#   那块地，**不是整屏** —— 于是 3D 形与它替换掉的 SVG 形逐像素同位，
#   页上其余的字（标签 / 引线 / 图例 / 卡片）全部照常压在 canvas 之上。
#
#   五枚新场景的局部坐标系 = 该页 figbox 的 viewBox 坐标（本 deck 所有 figbox
#   的 vbw 都等于盒宽 ⇒ 缩放恒为 1，figure 坐标就是舞台像素）。所以场景里
#   一个坐标都不新造：贝塞尔控制点、节点位置、事件 x 全部照抄页上的 SVG。
#
# ── ⑥ 互动星系（P22 末页）的舞台常量：**全家族只在这里定义一次** ────────────
#   引擎母本 `build-convoai-engine.py` 与 `build-convoai-info.py` 都现取这一份
#   （import 本文件当模块）—— 盘心 / 尺度 / 矩形一个数都不许在别处重写。
#   舞台矩形与 figbox 是**同一只盒**（vbw = 盒宽 ⇒ 局部原点同一个，
#   poster / 3D / 净空只算一次）。盘心页坐标 (1440, 530) = 局部 (380, 400)。
GX22 = {"cx": 380.0, "cy": 400.0, "s": 0.75, "rect": (1060, 130, 760, 800)}
LAB_RECTS = {
    # 页  场景名      x     y     w     h      局部坐标原点说明
    1:  ("voice",  1305,  328,  500,  500),   # 球心 (1555,578) 居中 · 呼吸极值 466px 内
    # 表达力精进 ①：470 → 708 —— 舞台从剧场（272–742）一路长到 02「两制对照」
    # 的底（980）。相机仍按剧场原高 470 架 + setViewOffset ⇒ 剧场投影一格不动。
    2:  ("morph",   120,  272, 1680,  708),   # = figbox(120,272,1680,vb1680×470)
                                              #   ∪ figbox(120,780,1680,vb1680×200)
    3:  ("lanes",   151,  372, 1618,  135),   # 三张卡里那三条 figure 带的并集（实测见下）
    4:  ("duplex",  120,  268, 1680,  352),   # = figbox(120,268,1680, vb1680×352)
    # ── 三轮「静态页升维」的四枚**加法层**（页上没有图，3D 是加在版面之外的一层场）──
    #    矩形不是「figbox」，是该页**无字的那块地**：底场 / 无字带 / 空带 / 整页。
    5:  ("three",   120,  780, 1680,  124),   # 卡底 y800 与落点句墨迹 y915 之间的空带
    15: ("hub",     120,  274, 1680,  576),   # 六卡栅格 + 其下的空带（核坐在无字带心）
    6:  ("chain",   120,  274, 1680,  536),   # = figbox(120,274,1680, vb1680×536)
    7:  ("terrain", 780,  414, 1010,  146),   # = figbox 右段（figure x 660→1670）
    8:  ("cutin",   120,  276, 1680,  372),   # = figbox(120,276,1680, vb1680×372)
    9:  ("shell",  1080,  296,  720,  470),   # = figbox(1080,296,720, vb720×470)
    10: ("bigmap",  120,  282, 1680,  660),   # = figbox(120,282,1680, vb1680×660)
    11: ("qos",     120,  280, 1080,  510),   # = figbox(120,280,1080, vb1080×510)
    12: ("vision",  120,  292, 1680,  450),   # = figbox(120,292,1680, vb1680×450)
    13: ("slots",   120,  272, 1680,  545),   # = figbox(120,272,1680, vb1680×545)
    14: ("towers",  120,  266, 1680,  578),   # = figbox(120,266,1680, vb1680×578)
    # ⑥ 三稿：车道整束从「卡底与对照表之间」搬到「对照表与落点句之间」——
    # 卡底是 72% 不透明的 --card-bg，车道排在它上面会从卡里的字底下透出来。
    16: ("calls",   120,  852, 1680,   92),   # 收口线之下、落点句之上的空带
    17: ("brain",   120,  282, 1680,  580),   # = figbox(120,282,1680, vb1680×580)
    # 二轮精修 · 波A：1240 → 1680 —— 舞台横跨**两图**（成长曲线 + LOOP 环带）。
    # 扩的是「区域」，页上的字一格没动：右图 figbox 仍钉在 x1420，环带走投影锁。
    18: ("spiral",  120,  276, 1680,  310),   # = figbox(120,276,1240) ∪ figbox(1420,276,380)
    21: ("globe",  1150,  180,  640,  640),   # 球心 (1470,500) 居中 · 弧顶 1.243r 内
    # 2026-09-03：末页从「余韵星野」（加法层）换成 **互动星系**（在页 3D 页）——
    # 右半舞台对仗 P21 右侧的地球（底座 → 愿景）。矩形 = figbox(1060,130,760, vb760×800)。
    22: ("galaxy",) + GX22["rect"],           # = figbox(1060,130,760, vb760×800)
}
# ── P3 的矩形是全 deck 唯一一处**不能照抄 figbox 参数**的（本 deck 也只有这一页
#    把图形区放进了卡里）：卡是 border-box + 1px 边 + 30px 内边距 ⇒ figure 实宽
#    458（不是 460），缩放 458/460 = .9957；三张卡的 figure 顶实测落在 y372.74。
#    矩形取三条 figure 带的并集（x151→1769，含两道卡间空档 —— 场景在空档里不画东西）。
#    ⚠ 改卡的 padding / border / 名字行字号，这四个数就得重测（scripts 里有量法：
#      getBoundingClientRect('.slide[data-p="3"] .fig svg') / 舞台缩放）。
P3_FIG_S, P3_FIG_DY, P3_FIG_GAP = 458.0 / 460.0, 0.74, 580
LAB_PAGES = sorted(LAB_RECTS)

# ═══════════════════════════════════════════════════════════════════════════
# 第二波 · 九页的几何名册与调参（2026-08-31 · 终波）
# ───────────────────────────────────────────────────────────────────────────
#   两类东西写在这里，泾渭分明：
#     ① **几何名册**（_P10BOX / _P13SLOT / _P14T / _P12WEAK / _Q_RAIN …）——
#        逐条抄自页上的 box() / 路径串。它们不是「新造的 3D 坐标」，是页上那张图
#        本人；build() 末尾有一道 ⑳ 闸把每一条与产物里的 <rect>/<circle>/d= 对表，
#        对不上当场炸（页面改了图、3D 没跟上 ⇒ 构建失败，不会静默错位）。
#     ② **调参**（深度 / 周期 / 相位）—— 3D 独有的那几个数，全部摊进 data-lab-*
#        供闸门静态复算（见 lab_data）。凡是页上已有的周期，一律照抄页上的值。
# ═══════════════════════════════════════════════════════════════════════════
# ── P2 模态转换剧场（二轮精修 · 波B · 王冠一）─────────────────────────────
#   终审（Colin 亲自给的方向）：「我们本质在构建的是拆解对话的本质 —— 听、想、说
#   是第一性原理出发的对话本质，拆解人类在这个过程如何做模态转换。从你的高维去拆解
#   这个理念，不用惧怕人类看不懂，很多情况下我们可以意会。」
#
#   于是这一页不再画「四步接成一个环」（那是流程图的语域），改画**同一段东西换了
#   三次形态**：
#     听 = 入射声波场（等相位线**竖直**的行波 —— 相位只由 x 决定；波长逐字取
#          `K.as.lam` = 232px ⇒ 它与 lab-kit ⑨ 的那条流是**同一种介质**）
#     ↓ 升维
#     想 = 表征星格（34×12×5 点阵被**两道折叠函数**揉成一片流形，内部一道
#          **位移**涟漪从中心往外传 —— 「理解」是几何变换，不是黑盒）
#     ↓ 凝聚
#     说 = 塌回波场，向右倾泻出画
#
#   三态是**同一批顶点的三个解析目标**：顶点着色器按 (wIn,wLat,wOut) 线性插值
#   （MO_HEAD 的 waveAt / latAt），权重和恒为 1。四道相位边界全部走 smootherstep。
#   无缝三件：① 一套顶点一次插值，没有第二套几何；② 生灭窗把接头藏在画外
#   （uLife 归零才换位置 ⇒ 形上零跳变）；③ **两代同场**，相位差半周期（7s）——
#   舞台永不空，而这正是页上「同一时刻 · 并行进行 / 持续在听 · 同时在说」
#   两行落点句本人。
_MO_CYC = 14.0                  # 一代走完三态的整周期
_MO_GEN = 7.0                   # 两代相位差 = 半周期 ⇒ **舞台视觉周期 7s**
#   四道相位边界（秒）：升维起 / 升维止 / 凝聚起 / 凝聚止
#     听 0.00–3.20 ｜升维 3.20–4.90｜想 4.90–8.60｜凝聚 8.60–10.30｜说 10.30–12.80
_MO_PH = (3.20, 4.90, 8.60, 10.30)
#   生灭窗：生 0.00→0.80 淡入 / 灭 12.80→13.60 淡出，13.60–14.00 全暗
#   ⇒ 换位置（t 回卷）永远发生在 uLife = 0 的那 0.4s 里，形上零跳变
_MO_LIFE = (0.00, 0.80, 12.80, 13.60)
#   让位事件：另一代在本代 t=7.00 出生（第二道入射波沿 `_P2ARC` 切进来），
#   格架 **0.56s** 内整片转过 uYaw 让位，其后 **3.10s** 慢慢回正
_MO_YAW = (7.00, 0.56, 3.10)
_MO_YAWA = 0.40                 # 让位偏航角（rad ≈ 22.9°）
#   舞台（figbox 局部坐标）：入射从左缘进、出射向右**出画**（终点越过 vb 右缘 1680）
_MO_X0, _MO_X1, _MO_OUTDX = 300.0, 1560.0, 200.0
_MO_YC = 154.0                  # 舞台中线（局部 y）
_MO_D = 1400.0                  # 相机深度（camPx 的 D）—— poster 的透视用同一个数
_MO_NA, _MO_NB, _MO_NC = 34, 12, 5           # 顶点点阵 34 × 12 × 5 = 2040
_MO_HW, _MO_AMP, _MO_DZ = 72.0, 52.0, 150.0  # 波场纵向半宽 / 波峰振幅 / 五层总深
#   ⚠ 行距 2·HW/(NB−1) = 13.1px，振幅 52 是它的 4.0 倍 ⇒ 眼睛先读到「波」再读到「行」。
#     反过来（振幅 < 行距）读出来就是一张会抖的网格 —— 那正是波A 要治的病。
_MO_LCX, _MO_LW, _MO_LH, _MO_LD = 930.0, 480.0, 160.0, 170.0   # 星格中心 / 三向尺度
_MO_F1, _MO_F2, _MO_FB = 0.20, 0.12, 26.0    # 两道折叠函数的幅度 + 深度隆起
#   ⚠ 深度隆起 26 < 层距 LD/(NC−1) = 42.5：隆起大过层距，五层就会互相穿插，
#     「流形」当场读成一团乱线（本轮实拍锤过一次）。
_MO_RIP, _MO_RLAM, _MO_RPER = 12.0, 168.0, 2.6   # 内部位移涟漪：幅 / 波长 / 周期
_MO_CREST = 0.52                # 波峰亮度增益（与 lab-kit ⑨ 的 uCrest 同语义）
_MO_ARC = (5.60, 7.00, 0.55)    # 第二道入射波沿 `_P2ARC` 的注入窗：起 / 到达 / 余晖
_MO_ARCW = 9.0                  # 那条 audioStream 的基准半宽
_O_HOTCOL = 2                   # 底排四栏里唯一的 hot 栏（= 「判断」，全页的因）
# ═══ 02 · SAME MOMENT「两制对照」（表达力精进 · 第一波 ① · 2026-09-02）═══════
#   病名 A「对照块降级成注脚」：论点的另一半被做成灰色小字条（旧 _P2ANTI =
#   三枚 900×58 的虚线 chip），与上面那座剧场不对等 —— 读者眼里 01 是论证、
#   02 是脚注。治法不是把字条调大，是**换介质**：02 与 01 用同一枚 lab-kit ⑨
#   audioStream、同一档波长（232px）、同一档流速（A 档），画成两排真带子。
#
#   舞台怎么长出来（**剧场逐像素不动**是硬红线）：LAB_RECTS[2] 高 470 → 708，
#   相机仍按**原高 470** 架（camPx(w, _MO_H0, D)），再 `setViewOffset(w,470,0,0,w,708)`
#   —— 视锥只把下缘拉长 238px，投影中心 / 缩放 / 上缘一格不动 ⇒ 剧场那 470 行
#   与从前逐像素相同（⑲b 对位 + A/B 定拍截帧逐像素自证）。多出来的 238px 里
#   z=0 仍是「1 世界单位 = 1px」，两排带子直接画在舞台局部 y 508–708 上。
#
#   ⚠ `rule(850)` **留着**（任务书原议是去掉）：content 背景板自带一条 accent
#     细线在 y847–853（x117–761 · 实测），rule(850) 的既定职责就是压住它当收口线
#     （见文件头「踩过的坑」那一条）。去掉它，02 区里会露出一条 640px 的亮条，
#     而两排带子是半透明的、盖不住它。所以改成：**两排分居 rule 上下**，
#     收口线正好成为「两制」的分界 —— 它一格没横穿任何一排。
_MO_H0 = 470.0                  # 剧场原高：相机按它架，多出来的画布走 setViewOffset
_P2AY = 508.0                   # 02 区在**舞台局部**坐标里的顶（= 页 780 − 舞台顶 272）
_P2AH = 200.0                   # 02 区高（= figbox 的 vb 高）
_P2TX0, _P2TX1 = 200.0, 1680.0  # 两排共用的时间轴（局部 · 页 320–1800）：右端顶到版心
#   右缘 —— 「同分量」的第一层意思就是占地。左端留 200px 给行标「回合制」：
#   它必须**贴着上排**、不能挤到 02 小节标（y757.7–775.7）底下去 —— 那两行会读成
#   「02 · SAME MOMENT / 回合制」一个两行标题，而回合制只管上面那一排。
#   段标（听完 / 想 / 说）与判词（听完再回答 ✕）在带子上方走一条标注行；
#   五处字的 DOM 序与旧 _P2ANTI 逐字相同（同源自证只比正文集合与顺序）。
#   上排 · 回合制 ✕（灰 · 串行）：一条流 + 一条 gain 剖面 —— 听 / 说是实带，
#   段与段之间落到 ghost 档（= 真细线的空档），「想」不是媒体（见下面的虚线框）。
_P2LBY = 10.0                   # 段标行基线（局部 y · 墨迹 776–796）
_P2GY = 50.0                    # 「回合制」基线（局部 y）—— 与上排带子同一条中线
_P2RY, _P2RW = 46.0, 10.0       # 上排 lane 中线 / 基准半宽（局部 y 36–56 = 页 816–836）
_P2SEG = ((0.00, 0.34), (0.38, 0.50), (0.55, 1.00))   # 听 / 想 / 说（u 区间）
_P2SEGE = 0.010                 # 段边界的 smootherstep 半宽（u ⇒ 14.8px）
_P2EVT = 0.72                   # 事件（用户插话）的 u —— **两排共用同一个时刻**：
#   上排在这里只多一枚事件标、带子一格不让位（✕ 的几何含义）；
#   下排在同一根竖线上让位再接回（✓）。不共用同一个 x，这个对照就不成立。
_P2EVH = 17.0                   # 事件竖标半高（带子上下各露 6px）
_P2DKX = (_P2TX0 + (_P2TX1 - _P2TX0) * _P2SEG[1][0],   # 「想」虚线框的 x 区间
          _P2TX0 + (_P2TX1 - _P2TX0) * _P2SEG[1][1])   #   = _P2SEG[1] 换算成 px
_P2DKH = 10.0                   # 「想」虚线框半高（与上排带子同一档高）
#   下排 · 边说边听（accent · 并行）：听 / 想 / 说三条连续带全程在跑。
#   「想」按流质铁律不是媒体 ⇒ 走**低幅带**（gain .6 + 更窄的基准半宽），
#   不另起一套点阵语汇（同一枚原语的第二语义通道就够了）。
#   下排三条 lane 上移一档，把底下那 30px 让给判词「边说边听 ✓」——
#   终审：下排没有任何标签，读者分不出哪条是听 / 想 / 说，也没有与上排 ✕ 对仗的 ✓。
_P2LY = (96.0, 126.0, 156.0)    # 三条 lane 的中线（局部 y）
_P2LW = (9.0, 6.0, 9.0)         # 三条带的基准半宽
_P2LGY = (101.0, 131.0, 161.0)  # 三枚 lane 标「听 / 想 / 说」的基线（与各自带子同中线）
_P2VY = 199.0                   # 「边说边听 ✓」基线（下排之下 · 与上排判词同一列右对齐）
_P2LG = (1.0, 0.60, 1.0)        # 三条带的 gain 档
_P2SPK = 0.22                   # 「说」从 22% 起（前面 22% 只有听与想）
_P2DUCK = 200.0                 # 让位窗口全宽（px 弧长 · 与 P8「收声」那段 200ms
#   括号同一档：本 deck 的时间轴一律 1px = 1ms，见 P8 的 _U_DUCK0/_P9CUT 断言）
# ── P4 双向声带（3D 调参；几何是 _tri_fig 那条时间轴本人）─────────────────
#   二轮精修 · 波A：这几个数从 lab_k() 的字面量提到模块级 —— `_spd_rows(4)` 要用
#   同一批数把两条带的**弧长**算出来，周期才谈得上「由流速反推」。
#
#   ── 表达力精进 · 第一波 ②（2026-09-02）：舞台从文字右缘 +16px 起 ─────────
#   病名 B「3D 件与文字抢地」：旧起点 x0=160（页 x280）在三行说明的**底下**，
#   两条声带一路压着「增量理解 · 每一瞬间…」「流式 TTS · 随时可收声让位」走。
#   三行说明的最右墨迹实测在页 x874.0（第一行），所以起点改到页 x900
#   （局部 780）—— 净空 26px > 加法层规则的 16px，`_P4INK` / `_P4CLRMIN` 逐条断言。
#   跑道从 1476px 缩到 856px，圈数按「保持两次交叉」反推：交叉解在
#   θ = π/2 − .31 + kπ ⇒ 恰好两次要求 2π·turns ∈ [4.403, 7.544)，取 1.15
#   （节距 744px/圈，比旧的 628 更从容）。NOW(页980) / 用户插话(页1204) /
#   340ms(页1220) 三处标注一格没动，仍全部落在带子上。
_D_X0, _D_X1, _D_YC = 780.0, 1636.0, 190.0
_D_AMP, _D_DEP, _D_TURNS, _D_PHASE, _D_N = 104.0, 62.0, 1.15, 0.62, 320
# ── P3 双工三通道 ─────────────────────────────────────────────────────────
_L_DEP, _L_SLAB = 42, 16        # A 面 +42 / B 面 −42（通道真的穿越空间）· 说话块的厚度
# ── 表达力精进 · 第二波 ④（2026-09-02）：三张时序小图「太小太暗」───────────
#   病名 C 的一支：块与通道都细到读不出，三种双工的差别在 3 米外分不出来。
#   三件事，都只动**材质与块尺寸**（图窗 135 / 卡高 386 / 其后所有 y 一格没动）：
#     ① 半双工从「三轮 × 24 高」改成「两轮 × 44 高」—— 轮次少一次，块高翻倍；
#        A 说 → 闸 → B 说 仍是完整的一次轮换，被拦的 ✕ 照旧压在 B 的空块里。
#     ② 方向通道从 2.5px 的线加粗成**半宽 4.5 的带**（页上与 3D 同一档）；
#        3D 里它们从 LineSegments 换成真四边形带 —— 「通道」得看得见宽度才是通道。
#     ③ 全双工的**重叠区高亮**过去只在 2D 上有，3D 起来就没了（那是这一格的论点
#        本身）：把它入册成 _P3LAP，3D 照着画一枚同位的面。
#   半双工的两道闸同理入册成 _P3GATE（3D 过去也没有，一起补上）。
_P3CHW = 4.5                    # 方向通道的半宽（页上 stroke-width = 2×它）
_P3BANDS = {                    # [列(0=A/1=B), y, 高, 在说] —— 逐条抄自 _duplex_fig 的 band()
    "simplex": [(0, 30, 104, 1), (1, 30, 104, 0)],
    "half":    [(0, 30, 44, 1), (1, 30, 44, 0), (0, 90, 44, 0), (1, 90, 44, 1)],
    "full":    [(0, 30, 72, 1), (1, 62, 72, 1)],
}
_P3LAP = (34, 62, 392, 40)      # 全双工的重叠区高亮（页上那只 --i:2 的 rect 本人）
_P3GATE = ((44, 82, 192), (268, 82, 416))   # 半双工的切换闸（两段 · 中间让出「切换」二字）
_P3GATED, _P3GATEG = 5.0, 5.0   # 闸的破折 / 间隔（与页上 stroke-dasharray="5 5" 同参）


def _p3_gate_segs():
    """切换闸的虚线段表（构建期算一遍，页上与 3D 同一批坐标 ⇒ 破折相位不分叉）"""
    out, per = [], _P3GATED + _P3GATEG
    for x0, y, x1 in _P3GATE:
        s = 0.0
        while x0 + s < x1:
            e = min(float(x1), x0 + s + _P3GATED)
            if e - (x0 + s) > 0.5:
                out.append((x0 + s, float(y), e, float(y)))
            s += per
    return out


_P3GATESEG = _p3_gate_segs()
# ═══════════════════════════════════════════════════════════════════════════
# lab-kit ⑨ · audioStream 原语的**参数表**（二轮精修 · 波A · 本波最重要交付）
# ───────────────────────────────────────────────────────────────────────────
#   终审：「P8 想构建声波感但像锯齿，突兀不精致 —— 让它像 Audition 里的声波一样
#   动起来。」旧做法是**逐柱采样再线性插值**（_P9HS 那张定高表）：每根柱的边界
#   都是一处斜率突变，那就是锯齿本身 —— 换多少档平滑都只是把角磨钝，不是没有角。
#   本波换成**解析包络**：四枚谐波叠加，从根上没有角（C^∞）。每个数的来历：
#
#     _AS_A  谐波权重 [.44,.28,.18,.10] —— **Σ = 1.00**，于是
#            en = 0.5 + 0.5·Σaᵢsin(·) 恒 ∈ [0,1] 恒非负：数学上不可能出现锯齿
#            （这一点正是 abs(sin) 做不到的 —— 它在零点有尖角）。
#     _AS_F  频率 [1.00,1.63,2.41,3.67] —— 两两不整除 ⇒ 包络永不重复。
#            齐步的后果不是「不好看」，是**起伏变心跳**：语义就错了。
#     _AS_LAM 波长 232px —— 配 A 档 110px/s ⇒ 2.11s 一次呼吸（人呼吸的量级）。
#     _AS_FLOOR .30 —— 媒体流是**持续供给**：带子最窄也留三成，永不掐断。
#     _AS_GHOST .055 —— aG→0 时的残余幅度：让位 = **细线**，不是消失。
#     _AS_GRAIN/_AS_GRAINL .26 / 46px —— 微粒纹理，与波峰**同速**漂移。
#            不同速会被读成「带子没动、只是在闪」，那正是要治的病。
#     _AS_EDGE  .055 —— 接头渐显渐隐（两条流首尾相接处不许出现硬切口）。
#     _AS_CREST .55  —— 波峰亮度增益：声音走到哪里，看得见。
#     _AS_COMP  .55  —— 内层 RMS 压缩：Audition 的波形是「峰值淡壳 + RMS 实芯」
#            两层，只画一层就只是一条会抖的带子。
#
#   第二语义通道 **aG**：`amp = mix(uGhost,1,aG)` 且 `dyn = mix(1,en,aG)`
#   ⇒ aG→0 时幅度落 ghost 档**且包络一起平掉** = 真细线（不是「小一点的波」）。
#   P8 的 200ms 让位、P6 的过站收窄与由稀到密，全部只是一条 gain 回调，**零分支**。
_AS_A = [0.44, 0.28, 0.18, 0.10]          # Σ = 1.00（构建期断言在 build() 里）
_AS_F = [1.00, 1.63, 2.41, 3.67]          # 两两不整除（构建期断言）
_AS_PH = [0.00, 1.70, 3.10, 4.90]         # 起相位：四枚谐波不在原点齐步
_AS_LAM = 232.0                           # 波长（px）
_AS_FLOOR = 0.30                          # 幅度地板（媒体流永不掐断）
_AS_GHOST = 0.055                         # aG→0 的残余幅度（让位 = 细线）
_AS_GRAIN, _AS_GRAINL = 0.26, 46.0        # 微粒纹理强度 / 粒长（px · 与波峰同速）
_AS_EDGE, _AS_CREST, _AS_COMP = 0.055, 0.55, 0.55   # 接头渐隐 / 波峰增益 / RMS 压缩

# ── 全局流速表（波A ③「速度品味检查」）─────────────────────────────────────
#   A 档基准 110px/s ±30% ⇒ [77.0, 143.0]。旧值差得离谱（同一页里 P2 主环 270
#   vs 支轨 88 差三倍、P4 324/375、P6 主路 296、P9 噪声 50–69 vs 目标 155–217、
#   P14 弧头 352/682），读者的眼睛把「快慢」读成「重要 / 不重要」，那是错的语义。
#   本波把 A 档全部按「路径长 ÷ 目标流速」反推周期 —— 周期是**算出来的**，
#   不是调出来的；`_spd_of()` 把结果摊到 data-lab-spd 上供 ⑲s 逐股复算。
# A 档股数**声明**在这里（不是随缘的）：波A 30 股；波B 再入册 11 股 ——
#   P2 入场弧流 +1（3）｜P7 地形整幅左移 +1（1）｜P10 四车道 + 四握手 +8（8）｜
#   P13 贯通流 +1（10）。⑲s 逐股复算，少一股多一股都当场报。
# 三轮「静态页升维」再入册 20 股 3 页：P5 底场 +7｜P15 六条支线 +6｜P16 通话流 +7
# ⇒ 41 → 61 股、10 → 13 页。P22 的涟漪**故意不在这张表里**（它不是介质，见 ㉒-①）。
# 表达力精进 · 第一波 ① 再入册 4 股（页数不变）：P2 的 02「两制对照」——
#   回合制轨 1 + 并行听 / 想 / 说 3 ⇒ 61 → 65 股、仍 13 页。
# 第二波 ⑤⑥ 改册（页数不变）：P5 底场七股 → **四股**（三支流 + 一集流，−3）／
#   P16 通话流七股 → **八股**（+1）⇒ 65 → 63 股、仍 13 页。
# 2026-09-03 ⑥ 互动星系：P22 从「余韵星野」（**故意不进这张表** —— 涟漪不是介质）
#   换成互动星系，20 股全部是 A 档介质（14 核↔内环 + 6 内环→外环 · λ232 · 110px/s）
#   ⇒ 63 + 20 = **83 股**、13 + 1 = **14 页**。⑲s 那条「P22 不许进表」的断言随之反转。
_SPD_N = 83
_SPD_A = 110.0                  # A 档基准（px/s）
_SPD_TOL = 0.30                 # ±30%：同一条河里允许的语义差异


def _dur_at(length, spd):
    """由「页上像素路径长 ÷ 目标流速」反推周期（秒）—— 本波所有 A 档周期的唯一来源"""
    return float(length) / float(spd)


def _plen(pts):
    """折线的 xy 像素长（页上看得见的那个长度 —— data-lab-spd 的分子）"""
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
               for i in range(len(pts) - 1))


def _plen_d(d, per=14, tol=1.4):
    """一条 SVG 路径展平后的 xy 像素长（与运行时 unpackPoly/polyCum 同源）"""
    return _plen(_decim(_pathpts(d, per)[0], tol))


def _box_u(pts, box, step=2.0):
    """一条折线**落在某只框里**的弧长区间 [u0,u1]（px）—— 波B P13 的 ghost 窗口
       就是这么算出来的：框逐条取自页上的墨迹（模块板 / 字段），
       所以「流在哪里收成细线」由页面决定，不由手感决定。"""
    x0, y0, bw, bh = box
    u, lo, hi = 0.0, None, None
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        seg = math.hypot(bx - ax, by - ay)
        n = max(1, int(seg / step))
        for k in range(n + 1):
            t = k / float(n)
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            if x0 <= x <= x0 + bw and y0 <= y <= y0 + bh:
                uu = u + seg * t
                lo = uu if lo is None else min(lo, uu)
                hi = uu if hi is None else max(hi, uu)
        u += seg
    return None if lo is None else (lo, hi)


def _at_of(pts):
    """折线的「弧长参数取点」—— 与运行时 polyAt(p,c,t) 逐点同解"""
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i-1][0], pts[i][1] - pts[i-1][1]))
    tot = cum[-1] or 1.0

    def at(t):
        L = max(0.0, min(1.0, t)) * tot
        lo, hi = 0, len(pts) - 1
        while lo < hi - 1:
            m = (lo + hi) // 2
            if cum[m] <= L:
                lo = m
            else:
                hi = m
        seg = (cum[hi] - cum[lo]) or 1.0
        u = (L - cum[lo]) / seg
        return (pts[lo][0] + (pts[hi][0] - pts[lo][0]) * u,
                pts[lo][1] + (pts[hi][1] - pts[lo][1]) * u)
    return at


# ── 逐股目标流速（A 档 · 110 ±30%）—— 「同一条河」的品味，不是强迫症 ────────
#   每一股的**周期**都由 `路径长 ÷ 这里的目标流速` 反推（见 _dur_at / lab_k）。
#   P13 总线包（92.9–94.3）本来就在档内，一个数没动 —— 已经对的不去动它。
_SPD_P2 = (110.0, 109.9)                    # 主环 / 支轨（旧：270 vs 88，同页差三倍）
#   表达力精进 · 第一波 ①：02「两制对照」四股（回合制轨 + 并行听 / 想 / 说）
_SPD_P2B = (108.0, 112.0, 106.0, 111.0)
_SPD_P4 = (110.0, 119.9)                    # 上行声带 / 下行声带（旧：324 / 375）
_SPD_P6 = (110.0,                           # 主路（旧：296，12 枚球）
           118.0, 112.0, 105.0, 108.0,      # 音频帧 / 增量文本 / token / 音频包
           120.0, 116.0, 112.0, 108.0)      # 四条增量带
_SPD_P8 = (110.0, 110.0)                    # 智能体轨 / 用户轨（= 波峰行进速度）
_SPD_P9 = (110.0, 97.7, 118.0, 124.6)       # 三路噪声 / 目标人声（旧：50–69 vs 155–217）
_SPD_P12 = (110.1,)                         # 画面平面（旧：77.5）
_SPD_P13 = 108.0                            # 波B：P13 贯通流（一条走完全程）
_SPD_P7 = 110.0                             # 波B：P7 地形整幅左移（A 档基准本人）
_SPD_P10 = (110.0, 109.0, 112.0, 111.0,     # 波B：P10 四条车道
            108.0, 113.0, 107.0, 114.0)     #       + 四道握手（介质 → 流带）
_SPD_P18 = (110.0, 110.1)                   # 复利螺旋 / loop 环流
_Y_BEAM = 400.0                             # B 档：P14 注光速度（离散事件，不进 A 档表）


# ── P6 实时语音链路 ───────────────────────────────────────────────────────
_C_ZNEAR, _C_ZDEEP = 55, -130   # 两端（麦克风 / 喇叭）近 · 链路中段（LLM）最深
_P6ST = [(180, 120, 220, 130, 1),    # AI-VAD（hot · 链路里唯一声网自研差异化环节）
         (470, 120, 220, 130, 0),    # ASR
         (760, 120, 220, 130, 0),    # LLM
         (1050, 120, 220, 130, 0)]   # TTS   —— x 逐条 = _PIPE_X（⑳ 闸对表）
_P6RING = [(70, 185, 44), (1610, 185, 44)]
_P6LINK = [(118, 168), (400, 458), (690, 748), (980, 1038), (1270, 1554)]
_P6BAND = [(150, 620, 432), (450, 920, 444), (750, 1220, 456), (1050, 1620, 468)]
_P6FORK, _P6DH = (1375, 185), (1245, 292, 260, 70)
_P6FLOW = (150, 1596, 518)      # 增量流带主轨（页上那条 hline）
# 四段符号流 (x0, 枚数, 步进, 点径, 周期)：粒度逐段变粗 = 音频帧 → 增量文本 → token → 音频包
_P6GLYPH = [(152, 19, 15, 3.4, 2.6), (452, 7, 40, 6.0, 3.2),
            (752, 11, 26, 8.0, 3.8), (1052, 13, 34, 11.0, 4.4)]
# ── 二轮精修 · 波A：符号行的四段**接缝表**（首尾严丝合缝 ⇒ 读成一条流不是四块）──
#   段界 x 逐个 = 页上四组符号的起始 x（152 / 452 / 752 / 1052），末端 1502 =
#   页上那根 accent-deep 截断记号（「增量合成 · 随时可截断」指的就是它）。
#   三处接缝 452 / 752 / 1052 由 ⑲(P6) 闸逐条复算：有缝就不是一条流。
_P6SEG = [(152, 452), (452, 752), (752, 1052), (1052, 1502)]
_P6SEGNM = ("音频帧", "增量文本", "token", "音频包")
_P6TOKEN = 2                    # token 段的下标：本行唯一允许留粒子的一段（token 本来离散）
_P6X0, _P6X1 = 70, 1610         # 主路：麦克风 → 喇叭，**横贯全链一条流**
_C_PULSE, _C_PULSEN = 13.0, 5   # token 脉冲串：粒距（px）/ 每组枚数（头亮尾淡）
# ── P8 打断时序 ───────────────────────────────────────────────────────────
_U_ZA, _U_ZB = 90, 60           # 智能体轨（在说时）· 用户轨（插话后）各自的深度
_U_ZGH, _U_ZBK = -120, -110     # 让位后的智能体 · 插话前的用户（都退到远处）
_U_TX0, _U_TX1 = 170, 1640      # 两条声轨的时间轴跨度（页上波形的左右缘）
# 让位窗口 = 页上「收声」那一段相位括号本人（840 → _P9CUT）：**200px = 200ms**。
# 旧版是 1040→1100 的 60px 断崖 —— 塌陷的语义位置该由页上的括号决定，不由手感决定。
_U_DUCK0 = 840                  # = _barge_fig() 里「侦测 | 收声」那道括号界
# ── P10 产品大图（谨慎页）·「层」表 ───────────────────────────────────────
#   0 上行带 / 1 中枢 / 2 下行带 / 3 SD-RTN 底座 / 4 客户控制面
_M_ZL = [-30, -80, 30, -170, 80]
_M_LOP = [1.0, 0.94, 1.0, 0.72, 0.82]
_P10BOX = [                      # [x, y, w, h, 层, hot]
    (260, 4, 1390, 62, 4, 0),      (150, 132, 190, 88, 0, 0),
    (382, 132, 210, 88, 0, 0),     (634, 116, 430, 128, 0, 1),
    (1106, 132, 180, 88, 0, 0),    (1328, 116, 340, 132, 1, 1),
    (1328, 324, 340, 88, 1, 0),    (1106, 324, 180, 88, 2, 0),
    (620, 324, 210, 88, 2, 0),     (850, 446, 300, 62, 2, 0),
    (0, 566, 1668, 70, 3, 0),
]
_P10RING = [(70, 176, 38, 0), (70, 368, 38, 2)]
#   ── 波B 轻手术（Colin：「P10 表意已满意」⇒ 只把流动感带进底版，不重构）──
#   末位 med 是**逐条判**出来的，不是一刀切（接入指南 ⑨ 的判据）：
#     med=1 介质 ——「这条线上跑的东西一直在来」⇒ 必须是流带（有厚度、会起伏、
#            波峰自己往前走）：上行 / 下行 / 底座两条车道，
#            实时编排⇄LLM / AEC 参考环 / 底座两道握手。
#     med=0 离散事件 ——「有起点有终点、发生一次就结束」⇒ **保持粒子**：
#            SOS·EOS 事件线、打断快路径、客户控制面。
#   分层 / 投影锁 / **零位移**纪律一格不动（data-lab-drift 仍是 0，⑲h 复算）。
_P10LANE = [                     # [x0, x1, y, 层, 周期, 包数, med]（周期照抄 _P8TU / _P8TD）
    (110, 1328, 176, 0, 2.2, 8, 1), (1328, 108, 368, 2, 2.6, 7, 1),
    (432, 1148, 601, 3, 3.4, 5, 1), (1148, 432, 601, 3, 3.8, 5, 1),
    (70, 1498, 528, 0, 9.9, 0, 0),                  # 端到端 650ms 跨度线（无包，只是尺）
]
_P10BEAM = [                     # [x0,y0,层0, x1,y1,层1, 周期, 包数, med] —— 真的在深度里走
    (1498, 248, 1, 1498, 324, 1, 1.2, 2, 1),        # 实时编排 ⇄ LLM        · 介质
    (1030, 250, 0, 1420, 250, 1, 3.0, 3, 0),        # SOS / EOS · 打断事件  · 离散
    (700, 248, 0, 700, 324, 2, 1.0, 3, 0),          # 打断快路径            · 离散
    (560, 362, 2, 300, 222, 0, 2.2, 3, 1),          # AEC 参考环            · 介质
    (70, 566, 3, 70, 214, 0, 2.8, 2, 1),            # 底座 ↔ 终端           · 介质
    (1498, 566, 3, 1498, 412, 1, 3.0, 2, 1),        # 底座 ↔ 中枢           · 介质
    (1498, 66, 4, 1498, 116, 1, 2.0, 2, 0),         # 客户控制面 → 编排     · 离散
]
_M_MEDL = [i for i, r in enumerate(_P10LANE) if r[6]]     # 介质车道
_M_MEDB = [i for i, r in enumerate(_P10BEAM) if r[8]]     # 介质握手
_M_FLOWW = 5.0                                            # 流带基准半宽
_M_DZ, _M_BEAT = 26, 3.4
# ── P11 弱网 AI QoS ───────────────────────────────────────────────────────
_P11HEAPTOP = "M114 182 L526 182 L690 224 L764 182 L1020 182"   # = 页上蓄水折线的上沿
_P11BIN = (110, 176, 914, 56)
_Q_HX0, _Q_HX1, _Q_HBOT, _Q_HZ, _Q_HN = 114, 1020, 228, 26, 2400
_Q_RAIN = [120 + _k * 30 for _k in range(31) if not (512 <= 120 + _k * 30 <= 700)]
_Q_RY0, _Q_RDUR = 128, 1.1      # 包雨起点 y / 周期（= 页上 --mo-dur:1.1s）
_Q_WY, _Q_WZ, _Q_WW = 426, -40, 9
_Q_ODUR, _Q_OUTN = 3.0, 16      # 下游包流周期（= 页上那条带的 3s）/ 枚数
# 上游网络包条（收到 / 丢掉）逐条来自 _WN_SEGS；两块战场与两只机制盒来自域表。
_P11BAR = [(_x0 + _k * 28, 1 if _k < _n - _lost else 0)
           for (_x0, _n, _lost) in [(0, 9, 1), (256, 10, 8), (536, 6, 6), (716, 12, 1)]
           for _k in range(_n)]
_P11BY, _P11BW, _P11BH = 32, 22, 60
_P11DOM = [(250, 28, 262, 318), (526, 28, 164, 318)]      # 丢包域 / 断网域
_P11MECH = [(250, 250, 262, 96, 0), (526, 250, 164, 96, 1)]   # 抗丢包引擎 / AI QoS（hot）
_Q_BZ, _Q_DOMZ, _Q_MZ, _Q_BDZ = 50, -60, -30, 22
# ── P12 视觉模态 ──────────────────────────────────────────────────────────
_W_APEX, _W_MOUTH = (110, 155), (256, 70, 316, 170)
_W_ZAPEX, _W_ZMOUTH, _W_ZHUB, _W_ZWEAK = 70, -10, -70, -150
_P12BOX = [                      # [x,y,w,h,z,hot]
    (630, 85, 420, 140, _W_ZHUB, 1), (256, 70, 316, 170, _W_ZMOUTH, 0),
    (1110, 70, 316, 170, -10, 0),    (20, 127, 180, 56, _W_ZAPEX, 0),
    (1468, 127, 212, 56, 40, 0),
]
_P12WEAK = [(490, 316, 220, 56), (950, 316, 260, 56)]
_P12WLINE = [(840, 225, 840, 277), (600, 277, 1080, 277),
             (600, 277, 600, 316), (1080, 277, 1080, 316)]
_P12RUN = [(200, 155, _W_ZAPEX, 236, 155, _W_ZMOUTH, 0.65, 2),
           (572, 155, _W_ZMOUTH, 610, 155, _W_ZHUB, 0.68, 2),
           (1050, 155, _W_ZHUB, 1090, 155, -10, 0.70, 2),
           (1426, 155, -10, 1448, 155, 40, 0.50, 2)]
# ── P13 编排中枢机（二轮精修 · 波B · 王冠二）────────────────────────────────
#   终审：「现在的数据是点状移动，流向表意不清，整体呆板，需要把科技感构建出来，
#   每一个模块都可以有小巧思，对整个宏大的叙事更要有感觉。」
#   ⇒ 中枢不再是「一只会呼吸的盒」，是**一台活的机器**：
#     · 机腔深 150（= 单元腔深 52 的 2.9 倍）——全页最大的一处尺度对比，
#       机腔一深，六只槽就成了「插在机身上的模块」而不是「并排的六只盒」；
#     · 三道**逐层内缩**的内肋（37.5px 一道）——腔壁有结构，深度才是「机器内部」；
#     · 腔底一台**呼吸转子**：三枚异面轨道环 + 420 点脉动。
#       「实时调试 / 一键发布」不写第二遍字，写在转子的脉动里 ——
#       每 4.4s 一记发布脉冲从转子下缘沿页上 vline(840,348,398) **注光**进发布槽。
#
#   ── 终审硬伤一的修法（2026-09-01）：核压字 ⇒ 核**放大到字之外**变成轨道 ────
#   病灶不是「太亮」，是**位置**：核原来坐在机腔的几何中心，而「对话引擎 /
#   实时编排」两行字正坐在那里。三枚异面环里必然有一枚是**侧着**的，侧着的圆
#   投影成一条直线段，正好从「引擎」两个字里穿过去；420 点是**实心球**，
#   投影必然盖住中心。把它调暗是回避不是修 —— 那等于承认这台机器的心脏画错了地方。
#   修法：核不再躲在字后面，而是把半径放大到**字盒之外**，成为环抱两行字的
#   一台转子 ⇒ 读成「引擎的核心里坐着这两行字」，语义比原来更准，量级也没缩水。
#   硬指标：转子的任何一处可见几何（环 / 粒子 / 粒径）与两行墨迹盒净空 ≥ 16px，
#   墨迹盒与 ghost 窗口**同源**（_P13INK ⊂ _P13GHOST），构建期逐点断言（见 _k_orb_clear）。
_P13SLOT = [(60, _y, 380, 68) for _y in (60, 168, 276, 384)] \
         + [(1240, _y, 380, 68) for _y in (168, 296)]
_P13HUB = (620, 180, 440, 160)
_K_CYC, _K_SW, _K_CAV = 6.4, 1.6, 52    # 一轮换一只槽 / 一次热切换的时长 / **单元**腔深
_K_HUBCAV, _K_RIB = 150.0, 3            # 机腔深（= 52 × 2.9）/ 内肋道数
_K_CORE_N = 420                         # 呼吸转子的粒子数（一枚没少）
#   三枚轨道环 (ax, ay, az)：az 是**出平面**分量 —— 轨道面绕屏幕 x 轴倾一个角度，
#   三枚 az 正负 / 大小两两不同 ⇒ 真的异面（不是三枚同心圆）。
#   投影后的椭圆必须整只**包住**两行墨迹盒 + 16px 净空，同时整只留在机腔里。
_K_ORB = [(214.0, 70.0,  52.0),         # 外圈：最扁最宽
          (198.0, 72.0, -42.0),         # 中圈：反向倾（与外圈交叉）
          (184.0, 74.0,  26.0)]         # 内圈：最竖 —— 三条椭圆互相穿插
_K_ORB_BR = 0.026                       # 呼吸：整台转子随 beat 只**向外**涨（内界即基准）
_K_ORB_ROLL = (9.7, 12.3, 7.9)          # 三枚环各自「翻滚」一周的秒数（az 走一趟余弦）
_K_ORB_ARC = (0.34, -0.27, 0.21)        # 三枚环上光弧的角速度（圈/秒 · 正负 = 转向相反）
_K_CLR = 16.0                           # 净空硬指标（px · 墨迹盒外缘起算）
_K_PUB = 4.4                            # 发布脉冲周期（秒）
_K_SWZ = -320.0                         # 热切换：在位机体沿 −z 退到这里再淡出
_K_SWA, _K_SWB = (0.0, 0.58), (0.42, 1.0)   # 一进一出**错峰**（退场 / 进场各占的相位段）
_K_LOOP_OFF = 8.0                       # 两条往返闭环分居总线 ±8px（去一条、回一条）
_K_ZSLOT, _K_ZHUB, _K_ZBUS = -20, -80, 0
_P13PILL = (620, 400, 440, 60)          # 实时调试 → 一键发布
_P13BRK = [(60, 472, 440, 472), (60, 460, 60, 472), (440, 460, 440, 472)]   # 四槽集体括号
_P13BUS = [(440, _y + 34, 540, _y + 34) for _y in (60, 168, 276, 384)] \
        + [(540, 94, 540, 418), (540, 260, 618, 260)] \
        + [(1240, _y + 34, 1140, _y + 34) for _y in (168, 296)] \
        + [(1140, 202, 1140, 330), (1140, 260, 1074, 260),
           (840, 348, 840, 398)]
_P13RUN = [(440, _y + 34, 540, _y + 34, 1.06, 1) for _y in (60, 168, 276, 384)] \
        + [(540, 260, 618, 260, 0.84, 1),
           (1240, 202, 1140, 202, 1.06, 1), (1240, 330, 1140, 330, 1.06, 1),
           (1140, 260, 1074, 260, 0.70, 1)]
# ── 贯通流（波B）：语音 → ASR → 左总线 → 中枢 → 发布槽 ────────────────────
#   一条 audioStream 走完全程（lab-kit ⑨）。它是**介质**（语音一直在来），
#   所以是一条有厚度、会起伏、波峰自己往前走的带子，不是一串包。
#
#   ── 终审硬伤二的修法（2026-09-01）：糊成污迹 + 漏出舞台 ────────────────────
#   ① **落点**：原来右端伸到 x1720（页上 1840）—— 越过版心右缘 1800 流向虚空，
#      「流要有落点」这条纪律当场破。改成**终结在发布槽的右缘**（x1060 = 页 1180）：
#      语音 → ASR → 左总线 → 中枢 → 发布槽，到「一键发布」为止，这就是全部语义。
#      左端仍留在画外（−40）：语音进来之前它就在，而 22px 的淡入在**版心左缘之外**
#      就收满 ⇒ 版心边上是一条满幅的带子被画框切住（画外还在继续），不是一个淡出的头；
#      右端同一档反过来用，落在发布槽右缘上的是一记真正的收口，不是硬切也不漏出画外。
#   ② **形态**：原来幅度档相对路径尺度过大（半宽 11 + 地板 .30）⇒ 最窄也有七成宽，
#      读成一朵云不是一条波。这一页把三个数字**只在本页 opt 里**覆写（lab-kit ⑨ 的
#      _AS_* 全局常量一个没动）：半宽 11 → 8、地板 .30 → .12 —— 包络两端的宽度比
#      3.3× → 8.3×，波谷真的收下去；λ 由**全长 ÷ 12** 反推（≈120px）——
#      这条流被 ghost 窗口切成几段，最长的一段净跨度 220px，λ 必须短到
#      **每一段里都装得下一个半波峰**，否则静帧上只剩一坨鼓包。
#      让位档（ghost）反过来抬一档 .055 → .075：宽 8 × .075 = 宽 11 × .055，
#      细线的**绝对**粗细一格没变（「流不断」是纪律，不是这一页的手感）。
_P13FLOW = [(-40, 94), (540, 94), (540, 260), (840, 260), (840, 430), (1060, 430)]
_K_FLOWW, _K_FLOWFLOOR = 8.0, 0.12     # 本页覆写：基准半宽 / 幅度地板
_K_FLOWGHOST = 0.075                   # 本页覆写：让位档（带子瘦了，细线不能跟着瘦没）
_K_FLOWN = 12                          # 全长上的呼吸次数 ⇒ λ = 全长 ÷ 12
_K_FLOWFADE = 22.0                     # 两端渐隐收口的弧长（px）
#   穿模块、穿字段的那几段走 **aG ghost**（剖面收成细线）⇒ 流不断，字读得清。
#   这几只框逐条对着页上的墨迹取：ASR 模块板 / 中枢两行字 / 发布槽那行字。
_P13GHOST = [(74, 72, 352, 44),        # ASR 模块板（不透明，流从它「背后」过）
             (795, 274, 90, 28),       # 中枢「实时编排」
             (760, 226, 160, 40),      # 中枢「对话引擎」
             (716, 414, 248, 30)]      # 发布槽「实时调试 → 一键发布」
#   转子净空断言用的墨迹盒 = ghost 窗口那两只中枢字盒**本人**（同一份真相，不另立一套）
_P13INK = [_P13GHOST[2], _P13GHOST[1]]
_K_GZF = 26.0                          # ghost 窗口的渐隐半宽（px 弧长 · smootherstep）
#   两条往返闭环：中枢 ⇄ LLM（行 y202）/ 中枢 ⇄ TTS（行 y310）。
#   去一条走总线**左** 8px、回一条走总线**右** 8px ⇒ 「往返」在图上分得开。
_K_BUSX = 540
_P13LOOP = [[(620, 255), (_K_BUSX - 8, 255), (_K_BUSX - 8, _y - 5), (444, _y - 5),
             (444, _y + 5), (_K_BUSX + 8, _y + 5), (_K_BUSX + 8, 265), (620, 265)]
            for _y in (202, 310)]
#   发布脉冲：从腔底转子的**下缘**出发，沿页上 vline(840,348,398) 注光进发布槽。
#   起点原来取转子中心 (840,260) —— 那正是「对话引擎 / 实时编排」两行字的位置，
#   整条注光路径竖着劈过两行字（终审硬伤一的第二处）。改到 y336：投影后落在 y331，
#   在「实时编排」墨迹盒下缘（302）之外 29px，且正好贴着转子外圈的下缘出发。
_P13PUB = [(840, 336), (840, 348), (840, 398)]


def _k_flow_lam():
    """贯通流的波长：**全长 ÷ _K_FLOWN 次呼吸**（本页覆写 —— lab-kit ⑨ 的
       _AS_LAM 一个字没动，别的七页照旧吃 232px 那一档）"""
    return _plen(_P13FLOW) / _K_FLOWN


def _k_flow_edge():
    """两端渐隐收口占全长的比例（_K_FLOWFADE px ÷ 全长）。
       左端的几何还在画外 40px 处 ⇒ 淡入在**版心左缘之外**就收满：
       版心边上是一条满幅的带子被画框切住（画外还在继续），不是一个淡出的头。
       右端反过来 —— 落在发布槽右缘上的是一记真正的收口。"""
    return _K_FLOWFADE / _plen(_P13FLOW)


# ── 转子净空的**构建期**断言（终审硬伤一的硬指标）────────────────────────────
#   与运行时逐字同解：投影锁 LZ(x,y,z,zref) 把 (x,y) 抬到 zref 预缩放、再换成真 z，
#   透视除法之后屏点 = 舞台中心 + (页点 − 舞台中心) · (D−zref)/(D−z)。
#   这里把 makeSlots 里那几行 JS 原样翻成 Python，逐点量到两只墨迹盒的距离 ——
#   「≥16px」因此不是手感，是一条构建失败条件。
_K_D = 1500.0                                   # camPx 的相机距离（与 makeSlots 同参）
def _k_proj(px, py, oz):
    """转子上一点（页坐标 px,py + 出平面 oz）投影回舞台像素"""
    _cx, _cy = LAB_RECTS[13][3] / 2.0, LAB_RECTS[13][4] / 2.0
    s = (_K_D - _K_ZHUB) / (_K_D - (_K_ZHUB - _K_HUBCAV * 0.82) - oz)
    return _cx + (px - _cx) * s, _cy + (py - _cy) * s


def _k_orb_center():
    """转子中心的**预像**：投影之后正好落在两行墨迹盒并集的中心"""
    _cx, _cy = LAB_RECTS[13][3] / 2.0, LAB_RECTS[13][4] / 2.0
    sx = (min(b[0] for b in _P13INK) + max(b[0] + b[2] for b in _P13INK)) / 2.0
    sy = (min(b[1] for b in _P13INK) + max(b[1] + b[3] for b in _P13INK)) / 2.0
    k = (_K_D - (_K_ZHUB - _K_HUBCAV * 0.82)) / (_K_D - _K_ZHUB)
    return _cx + (sx - _cx) * k, _cy + (sy - _cy) * k


def _k_orb_at(t):
    """粒子带：三枚环之间的分段线性插值（t=0 内圈 / .5 中圈 / 1 外圈）——
       与 makeSlots 里的 orbAt() 逐字同解。"""
    a, b, s = ((_K_ORB[2], _K_ORB[1], t * 2) if t <= 0.5
               else (_K_ORB[1], _K_ORB[0], (t - 0.5) * 2))
    return tuple(a[i] + (b[i] - a[i]) * s for i in range(3))


def _k_orb_clear(nb=480, naz=9, nt=33):
    """转子（三枚环 + 整条粒子带）到两行墨迹盒的**最小净空**与整体包围盒。
       az 走满 [−az, +az]（环在翻滚）、半径走 [1, 1+_K_ORB_BR]（呼吸只向外涨，
       所以最窄的一档就是基准档 —— 净空的最坏情形在 rad=1）。"""
    ocx, ocy = _k_orb_center()
    mn, bx0, bx1, by0, by1 = 1e9, 1e9, -1e9, 1e9, -1e9
    fams = [_K_ORB[i] for i in range(3)] + [_k_orb_at(k / (nt - 1.0)) for k in range(nt)]
    for ax, ay, az in fams:
        for ir, rad in enumerate((1.0, 1.0 + _K_ORB_BR)):
            for ia in range(naz):
                m = -1.0 + 2.0 * ia / (naz - 1)
                for ib in range(nb):
                    th = 2 * math.pi * ib / nb
                    x, y = _k_proj(ocx + ax * rad * math.cos(th),
                                   ocy + ay * rad * math.sin(th),
                                   az * m * rad * math.sin(th))
                    bx0, bx1 = min(bx0, x), max(bx1, x)
                    by0, by1 = min(by0, y), max(by1, y)
                    if ir == 0:
                        for r in _P13INK:
                            dx = max(r[0] - x, 0.0, x - (r[0] + r[2]))
                            dy = max(r[1] - y, 0.0, y - (r[1] + r[3]))
                            mn = min(mn, math.hypot(dx, dy))
    return mn, (bx0, by0, bx1, by1)


_K_CLR_MIN, _K_ORB_BOX = _k_orb_clear()     # 构建期实测（build() 末尾断言 ≥ _K_CLR）


# ── P14 接入架构三塔 ──────────────────────────────────────────────────────
_P14T = [(40, 120, 460, 300, 0, 0), (610, 120, 460, 300, 1, 0),
         (1180, 120, 460, 300, 2, 1)]
_P14IN = [(72, 250, 396, 56, 0, 1)] \
       + [(1212 + (_k % 2) * 202, 210 + (_k // 2) * 66, 186, 52, 2, 0) for _k in range(4)]
_Y_Z = [90, 0, -110]            # 终端（近）/ 客户服务器（中）/ 声网引擎云（远）
_P14ARC = [("M270 120 V58 H790 V110", 0, 1, 90),
           ("M890 120 V58 H1410 V110", 1, 2, 90),
           ("M270 434 V478 H1410 V434", 0, 2, 120)]
_Y_REST = 0.14                  # 未点亮时的余光档（只留一道可循的痕，不抢已通的三段）
# ── 二轮精修 · 波A：三个点 → **光束生长**（离散事件才许光束，见接入指南 ⑨）──
#   终审：「三个点不像数据流」。病根不在慢一点：三个点没有「到达」这个动作 ——
#   看得见的只是「有东西在那条线上挪」，看不见「它到了对面」。光束生长有头、
#   有尾、走过留痕，一轮读完三次握手，全亮**停驻 2s** 是这一页真正的重点帧。
#   一轮 9.24s 不是拍脑袋：由注光速度 _Y_BEAM=400px/s 反推 ——
#     三段路由 634 / 634 / 1228px（= _P14ARC 三条本人）÷ 400 = 6.24s 生长，
#     + 全亮停驻 2.00s + 收尾 1.00s = 9.24s。三段**同一档速度**，qa 逐段复算。
_Y_HOLD, _Y_REL = 2.00, 1.00
_Y_GROW = sum(_plen_d(_a[0]) for _a in _P14ARC) / _Y_BEAM
_Y_CYC = _Y_GROW + _Y_HOLD + _Y_REL
# 楼层灯瀑：塔**右内缘**的一列楼层灯（不横穿塔身、不压任何一行字）
_Y_FLOOR, _Y_FLOORN, _Y_FLOORD = 18, 9, 2.6      # 距右内缘 / 层数 / 一趟瀑流秒数


def _d_lane(sign, phase):
    """P4 一条声带的 xy 折线（与 makeDuplex 的 lane() 逐点同解，只是不取 z）"""
    out = []
    for i in range(_D_N):
        u = i / (_D_N - 1)
        th = 2 * math.pi * _D_TURNS * u + phase
        out.append((_D_X0 + (_D_X1 - _D_X0) * u, _D_YC - sign * _D_AMP * math.cos(th)))
    return out


def _spiral_pts():
    """P18 复利螺旋的 xy 折线（与 makeSpiral 的 pts 逐点同解 —— 只是不取 z）。
       脊线 = 页上那条成长曲线本人；半径随 t 从 r0 长到 r1，绕轴转 turns 圈。"""
    at = _at_of(_decim(_pathpts(_CA_CURVE, 20)[0], 1.2))
    out = []
    for i in range(_CA_N):
        t = i / (_CA_N - 1)
        c = at(t)
        a, b2 = at(max(0.0, t - 0.004)), at(min(1.0, t + 0.004))
        tx, ty = b2[0] - a[0], b2[1] - a[1]
        tl = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / tl, tx / tl
        rr = _CA_R0 + (_CA_R1 - _CA_R0) * t
        th = 2 * math.pi * _CA_TURNS * t
        out.append((c[0] + nx * rr * math.cos(th), c[1] + ny * rr * math.cos(th)))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 三轮「静态页升维」· 四枚**加法层**场景（2026-09-01 · Colin 点名 P22 + 全 deck 静态页）
# ───────────────────────────────────────────────────────────────────────────
#   Colin：「/convoai-lab#22 作为结尾页是有问题的，这个是平面的，没有任何动效，
#           要对齐一下整体的质量。另外看下这个 deck 里全部的静态页，优化一下。」
#
#   ── 与前两波的**根本差别**：这四页的 3D 是「加法」不是「替换」──────────────
#   前 16 枚场景都在替换页上的一张 SVG 图（poster = 那张图本人，六道降级链的第一道）。
#   P5 / P15 / P16 / P22 页上**根本没有图** —— 只有卡片、logo 与文案。所以：
#     · 3D 在这里是一层**氛围场**：它加在既有版面之外，一件 DOM 都不动；
#     · 它们的**降级层就是整页本身**（WebGL 起不来 = 今天这一页，一个像素不差）
#       ⇒ 这四页**不挂 poster 元素**（挂一枚空 svg 只是骗闸门）。
#       这条判断在 build() 的㉒闸与 qa 的 ⑲a/⑲c 上都写成了机器断言：
#       加法层页必须 poster 件数 = 0，且几何 token 与引擎母本**逐条相同**
#       （比另外 14 页的「逐字同文」更硬 —— 那 14 页允许几何被裹进 poster 组）。
#
#   ── 共同纪律：净空 ≥16px，判据是**字形墨迹盒**不是元素盒 ────────────────────
#   沿用 P13 转子那一套（_K_CLR / _k_orb_clear）：页上每一处**字形行框**（Range
#   .getClientRects 量出来的墨迹，不是 line-height 撑出来的元素盒）逐条登记在
#   `_ADD_INK` 里，构建期逐点解析断言、运行时 `state().clr` 把这一帧真的传上 GPU
#   的顶点投影回舞台像素再量一遍。卡片 / 图片盒**不算墨迹**：卡里那几十像素的空白
#   本来就是版面留白，3D 在那里画东西不压任何字（P15 的六簇正是画在那儿）。
#   ⚠ 墨迹盒会随字体 / 换行变 —— 所以 qa 的 ㉒ 闸每次都从**活 DOM 重量一遍**，
#     与这里登记的逐条对表：改文案而没改这张表 ⇒ 当场报，不会静默压字。
_ADD_CLR = 16.0                 # 净空下限（px · 与 P13 转子同一档）
_ADD_PAD = 0.7                  # 构建期留量（运行时还要减掉点半径 / 线宽的一半）
_ADD_PAGES = (5, 15, 16)        # 加法层页名册（build() 与 qa 三处对表）
#   2026-09-03：P22 退出这张名册 —— 末页从「加在版面之外的一层场」改成
#   **在页 3D 页**（右半舞台的互动星系有自己的 poster，走 _INPAGE 那条自证）。
_PHI2 = 1.3247179572447460      # 塑性数 ρ：R2 低差异序列的底（Roberts, 2018）
#   ⚠ 2026-09-03：R2 序列与确定性随机的 **Python 侧同解**（`_r2` / `_h1p`）随
#     「余韵星野」一起退役 —— 现在只有运行时那两只（`r2()` / `h1()`）还在用，
#     构建期这边不再需要复算它们。⑥ 互动星系自带 `_gx_h1`（同一条式子）。


def _ink_clr(pt, boxes):
    """一点到一组墨迹盒的最小净空（px）"""
    m = 1e9
    for (bx, by, bw, bh) in boxes:
        dx = max(bx - pt[0], 0.0, pt[0] - (bx + bw))
        dy = max(by - pt[1], 0.0, pt[1] - (by + bh))
        d = math.hypot(dx, dy)
        if d < m:
            m = d
    return m


def _poly_clr(pts, boxes, step=3.0):
    """一条折线到一组墨迹盒的最小净空（按 step px 采样 —— 段中间也要量）"""
    m = 1e9
    for i in range(len(pts) - 1):
        ax, ay = pts[i][0], pts[i][1]
        bx, by = pts[i + 1][0], pts[i + 1][1]
        n = max(1, int(math.hypot(bx - ax, by - ay) / step))
        for k in range(n + 1):
            t = k / float(n)
            m = min(m, _ink_clr((ax + (bx - ax) * t, ay + (by - ay) * t), boxes))
    return m


def _pk(pts):
    """折线打包成运行时可复活的串（"x,y;x,y;…" · 1 位小数）——
       加法层四页的几何全部走这一条：**构建期算一遍、运行时不再算第二遍**，
       于是「构建期的净空断言」与「屏上真的画出来的形」不可能是两套解。"""
    return ";".join("%s,%s" % (_f1(q[0]), _f1(q[1])) for q in pts)


def _lerp_poly(pts, n):
    """把一条折线重采样成 n 个等弧长点（喂给 mkStream 的中心线）"""
    at = _at_of(pts)
    return [at(i / float(n - 1)) for i in range(n)]


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ 互动星系（P22 末页 ·「展望」）—— 全家族的**单一真相**
# ───────────────────────────────────────────────────────────────────────────
#   ⚠ 2026-09-03 退役：这里原来是「㉒-① 余韵星野」（quiet 场景 / _E22* / --e-* /
#     makeQuiet / ㉒c 三条克制闸）。Colin 这一轮的意图是**展望**（使命 / 愿景 /
#     三种互动），末页不再是「余韵」—— 整枚场景退役，产物里一行死代码不留。
#
#   这枚场景的发源地是 convoai-info P8（2026-09-03 三稿 · 12,000 点体积点云）。
#   本轮把它整块搬进旗舰当单一真相，三个消费方各取所需：
#     · lab    P22：figbox(1060,130,760, vb760×800) · 盘心局部 (380,400) · 尺度 0.75
#     · engine P22：同一段 page() 代码、同一张 poster（**裸放**，不裹 lp）
#     · info   P8 ：盘心 (860,278) · 尺度 1.0 —— `gx_poster` / `gx_kobj` 现取本文件
#   所以下面每一件都带 (cx, cy, s) 三个参数：形是同一枚，只是落在哪儿、多大。
#   ⚠ s 只缩放**几何**（半径 / 厚度 / 抬升 / 深度雾半程）；带宽 sw、点径 pad、
#     流速 110px/s、波长 λ232 **不缩放** —— 那是全家族同一种介质的常数，
#     不是这枚图形的尺寸。12,000 点**原样**：同一枚星系只是缩小，不是变稀。
#
#   ── 语义（三环由内向外 = 三种互动，一张实时网上）────────────────────────
#     ① 核 · 人与人 · 已经发生      实心体积球核 r≈100，密度剖面与 P17 大脑逐字同式
#     ② 内环 · 人与智能体 · 正在发生 环带 r200–290 厚 ±22，人 / 智能体确定性交错
#     ③ 外环 · 智能体与智能体 · 即将发生 环带 r360–470 厚 ±30，蓝紫各半，网在长
#   14 条核↔内环互动流（一来一回）+ 6 条内环→外环径向流，全部 A 档 110px/s · λ232。
#   整体绕盘轴 1 圈 / 90s 慢转，另叠 P17 同款 ±6° / 17s 轻摇。canvas **零文字**。
_GX_TILT = 62.0                      # 盘面倾角（长轴水平）
_GX_CT = math.cos(math.radians(_GX_TILT))
_GX_ST = math.sin(math.radians(_GX_TILT))
_GX_SPINP = 90.0                     # 自转：1 圈 / 90s（零随机源）
_GX_SWAY, _GX_SWAYP = 6.0, 17.0      # 轻摇 ±6° / 17s（P17 大脑同款原语）
_GX_D = 1400.0                       # camPx 深度
# 深度雾半程**贴真实 z 跨度**：盘面倾斜后 z 跨 ±(470·sin62° + 30·cos62°) = ±429
_GX_HALF = 430.0
# 三环（点数合计 12,000 —— 与 P17 大脑的 12000 点同一量级、同一套点材质）
_GX_CORE_R, _GX_CORE_N = 100.0, 3800
_GX_IN_R0, _GX_IN_R1, _GX_IN_T, _GX_IN_N = 200.0, 290.0, 22.0, 4200
_GX_OUT_R0, _GX_OUT_R1, _GX_OUT_T, _GX_OUT_N = 360.0, 470.0, 30.0, 4000
_GX_N = _GX_CORE_N + _GX_IN_N + _GX_OUT_N
_GX_DREF = _GX_CORE_R                # 核的厚度剖面参考距（与大脑的 dref 同位）
# ── 外环的「网在生长」（生灭窗写法照 P2 剧场：uLife 归零才回卷 ⇒ 形上零跳变）──
#   每点两枚相位：aQ = 生灭窗相位（回卷点各自错开 ⇒ 任一帧只有 2% 的点在灭窗里，
#   整幅亮度**不跳**）；aG = 角度门槛（由稀到密的那道生长锋按角度扫过去）。
_GX_CYC = 20.0                       # 由稀到密的整周期
_GX_LIFE_D = 0.4                     # 灭窗（秒）—— 归零再回卷
_GX_LIFE_B = 1.6                     # 生窗（秒）
_GX_W0 = _GX_LIFE_D / _GX_CYC
_GX_WB = _GX_LIFE_B / _GX_CYC
_GX_GS = 0.18                        # 生长锋的软边（角度相位的半宽）
_GX_FLOOR = 0.34                     # 「稀」的地板（网从来不空）
# ── 流（全部 A 档 110px/s · λ232 —— 与全家族同一种介质）────────────────────
_GX_SN_IN, _GX_SN_RAD = 14, 6        # 核↔内环 14 条（一来一回）· 内环→外环 6 条
_GX_SN = _GX_SN_IN + _GX_SN_RAD
# ⚠ 一稿实拍教训：抬升 60 + 扫角 0.34 + 半宽 3.5 ⇒ 14 条流在屏上是十四道**门框**，
#   整幅被它们劫走。三稿收成**旋臂**：几乎贴着盘面走（抬升 22 ⇒ 屏上只拱起
#   22·sin62°=19px）、角向扫近一个弧度、半宽砍到 2.2 —— 于是它读成「从核里旋出来
#   的流」，而不是罩在核上的一圈拱门。
_GX_LIFT, _GX_RLIFT = 22.0, 14.0     # 越过盘面的高度（出面方向）
_GX_W, _GX_WL = 2.2, 1.9             # 半宽（世界 · **介质常数，不随 s 缩放**）
_GX_SPTS = 48                        # 一条流的取样点数
_GX_SWEEP = 0.92                     # 核↔内环流的角向扫角（弧）
_GX_RSWEEP = 0.48
_GX_INR = 245.0                      # 内环带中线（流的落点半径）
_GX_OUTR = 415.0                     # 外环带中线（弧与径向流的落点半径）
# ── 弧（智能体之间 · 写法照 P21 地球弧：细弧 + 沿弧跑的亮斑）────────────────
_GX_ARCS, _GX_ARC_SEG = 24, 40
_GX_ARC_SPAN = (2, 3, 5)             # 三种跨度（× 2π/24）—— 网有近邻也有远联
_GX_ARC_L0, _GX_ARC_L1 = 12.0, 30.0  # 出面抬升 = L0 + L1·(Δφ/π)
_GX_ARC_DUR = 4.6                    # 一枚亮斑跑完一条弧的秒数
_GX_ARC_FLOOR = 0.30                 # 弧的常亮地板（网从来不空）
# 三枚轮廓环 —— P17 用血写下来的那一条：「轮廓是这张图的身份，给它一根真线」。
# 没有它，三环在屏上只是三层疏密不同的尘。落在三环各自的**外缘**（核的球面 /
# 两条带的外边界）：落在带心会被点云盖住，落在外缘才把三环的边界画出来。
_GX_RIM = (_GX_CORE_R, _GX_IN_R1, _GX_OUT_R1)
_GX_RIM_SEG = 96
_GX_GA = math.pi * (3.0 - math.sqrt(5.0))          # 黄金角（零随机源）
_GX_PL = 0.7548776662                # 塑性数的倒数（生灭窗相位 · 低差异序列）
_GX_SPINN = 48                       # 扫掠包络的采样：整圈 48 档（摇摆另 3 档）
_GX_LEADCLR = 16.0                   # 引线落点离环带的下限（16px 规则）


def _gx_h1(i, s):
    """确定性随机 —— 与运行时 `h1(i,s)` 逐字同式（两次构建、poster 与 WebGL 全同）"""
    x = math.sin((i + 1) * s) * 43758.5453
    return x - math.floor(x)


def _gx_coreT(rho):
    """核的半厚度剖面：与 `makeBrain` 的 brainT **逐字同式**
       T(d) = tmax·sin(π/2·(d/dref)^0.62)，d = 到边界的距离 ⇒ 边界上 T=0。"""
    d = max(0.0, _GX_CORE_R - rho)
    return _GX_CORE_R * math.sin(math.pi / 2 * ((d / _GX_DREF) ** 0.62))


def _gx_page(r, phi, wo, cx, cy, s, spin=0.0, sway=0.0):
    """盘面局部 (半径 r, 角 φ, 出面偏移 w) → (页 x, 页 y, z)。
       ① 自转：φ += spin（绕盘轴）；
       ② 倾角 T：面内的 v 压成 v·cosT，同时被抬进深度 v·sinT；出面的 w 反过来；
       ③ 轻摇 ψ：绕竖轴转 ——「±6°/17s」与 P17 大脑同一枚原语；
       ④ 尺度 s：三个分量一起乘 ⇒ 屏上就是同一枚星系缩小 s 倍（形不变）；
       ⑤ 投影锁（在这之后，由 mkLock / _lockpt 做）：xy 按该点自己的 z 预缩放 ⇒
          **投影落点就是这里的 (x, y)** —— 三环因此在屏上是三枚正椭圆，
          净空可以纯解析地算；深度只管雾与点径（体积感全在那儿）。
       ⚠ s=1.0 时每一步都是 `1.0 * x`（IEEE 精确）⇒ 与 info 三稿逐位同解。"""
    cS, sS = math.cos(math.radians(sway)), math.sin(math.radians(sway))
    a = phi + spin
    u1, v1 = r * math.cos(a), r * math.sin(a)
    y1 = v1 * _GX_CT - wo * _GX_ST
    z1 = v1 * _GX_ST + wo * _GX_CT
    return (cx + s * (u1 * cS) + s * (z1 * sS), cy + s * y1,
            s * (-u1 * sS) + s * (z1 * cS))


def _gx_cloud():
    """三环 12,000 点的**盘面局部**参数（构建期与运行时逐字同式 ⇒ poster = 那一帧）。
       返回 [(名, [(r, φ, w, aA, aH, aS, aQ, aG), …]), …]
         aA 基础不透明度权重 · aH 热度 · aS 点径权重
         aQ 生灭窗相位（外环用）· aG 角度门槛（外环用 · 生长锋按角度扫）"""
    out = []
    # ① 核：向日葵铺点（r=R·√((i+.5)/N) · φ=i·黄金角）—— 密度均匀、零随机源；
    #    厚度走大脑的剖面，深度权重 surf 也照抄（surf^0.40 ⇒ 表面比芯部密一档）。
    core = []
    for i in range(_GX_CORE_N):
        # 铺点几乎均匀（幂 0.56 只做一档轻微向心），**亮度按厚度剖面给**：
        # T(ρ)/tmax 就是这条视线穿过球体的弦长比 ⇒ 中心最亮、边缘化开 = 一颗球，
        # 而不是一块均匀的圆饼（二稿实拍：均匀铺点 + 均匀亮度 = 一枚粉色圆贴纸）。
        rho = _GX_CORE_R * ((i + 0.5) / _GX_CORE_N) ** 0.56
        phi = i * _GX_GA
        T = _gx_coreT(rho)
        surf = _gx_h1(i, 571.3) ** 0.40
        w = (-1.0 if _gx_h1(i, 853.9) < 0.5 else 1.0) * T * surf
        r3 = math.hypot(rho, w) / _GX_CORE_R
        core.append((rho, phi, w,
                     (0.26 + 0.74 * surf) * (0.24 + 0.76 * T / _GX_CORE_R),
                     max(0.0, 1.0 - r3) ** 1.1, surf, 0.0, 0.0))
    out.append(("core", core))
    # ②③ 两条环带：φ 走黄金角（角向恒均匀）、r 与 w 各走一对解耦的哈希 ⇒
    #     r 三角分布（带心密、带缘疏）、w 三角分布（贴盘面密）——「带」而不是「圈」。
    for nm, r0, r1, tk, n, s0 in (("in", _GX_IN_R0, _GX_IN_R1, _GX_IN_T, _GX_IN_N, 0.0),
                                  ("out", _GX_OUT_R0, _GX_OUT_R1, _GX_OUT_T, _GX_OUT_N, 7.0)):
        band = []
        for i in range(n):
            phi = i * _GX_GA
            fr = (_gx_h1(i, 137.9 + s0) + _gx_h1(i, 263.1 + s0)
                  + _gx_h1(i, 389.5 + s0)) / 3.0
            rr = r0 + (r1 - r0) * fr
            w = tk * (_gx_h1(i, 331.7 + s0) + _gx_h1(i, 457.3 + s0) - 1.0)
            edge = 1.0 - abs(w) / tk                      # 贴盘面的点亮一档
            band.append((rr, phi, w, 0.46 + 0.54 * edge, 0.0, 0.55 + 0.45 * edge,
                         (i * _GX_PL) % 1.0, (phi / (2 * math.pi)) % 1.0))
        out.append((nm, band))
    return out


_GX_CLOUD = _gx_cloud()


def _gx_streams():
    """20 条流的**盘面局部**中心线：14 条核↔内环（一来一回）+ 6 条内环→外环。
       核↔内环那一档是真 3D 曲线：起点核面、越过盘面 _GX_LIFT 高、落在内环带中线上；
       出面的抬升经倾角映射成屏上**向上拱起** 22·sin62° = 19px。"""
    o = []
    for k in range(_GX_SN_IN):
        a0 = 2 * math.pi * k / _GX_SN_IN
        pts = []
        for i in range(_GX_SPTS):
            t = i / (_GX_SPTS - 1.0)
            rr = _GX_CORE_R * 1.18 + (_GX_INR - _GX_CORE_R * 1.18) * t
            pts.append((rr, a0 + _GX_SWEEP * t, _GX_LIFT * math.sin(math.pi * t)))
        # 十四条**同向**旋臂（扫角同号）——正负交替会两两对成十四道花瓣，
        # 那是二稿实拍的病；「一来一回」只反**流向**（点序反转），形不动。
        if k % 2:
            pts.reverse()
        o.append(("核↔内环 %02d" % (k + 1), pts, _GX_W))
    for j in range(_GX_SN_RAD):
        a0 = 2 * math.pi * (j + 0.5) / _GX_SN_RAD
        pts = [(_GX_INR + (_GX_OUTR - _GX_INR) * (i / (_GX_SPTS - 1.0)),
                a0 + _GX_RSWEEP * (i / (_GX_SPTS - 1.0)),
                _GX_RLIFT * math.sin(math.pi * i / (_GX_SPTS - 1.0)))
               for i in range(_GX_SPTS)]
        o.append(("内环→外环 %d" % (j + 1), pts, _GX_WL))
    return o


_GX_STREAM = _gx_streams()


def _gx_arclist():
    """24 条智能体间弧：起止角 + 出面抬升 + 亮斑起相位（三种跨度轮转）"""
    o = []
    for k in range(_GX_ARCS):
        a0 = 2 * math.pi * k / _GX_ARCS
        d = _GX_ARC_SPAN[k % 3] * 2 * math.pi / _GX_ARCS
        o.append((a0, a0 + d, _GX_ARC_L0 + _GX_ARC_L1 * (d / math.pi), k / float(_GX_ARCS),
                  0.75 * _GX_OUTR * (1.0 - math.cos(d / 2.0))))
    return o


_GX_ARC = _gx_arclist()


def _gx_arcdip(a0, a1):
    """弧的内切深度：跨度越大越像**弦** —— 0.75 × 该跨度的弦矢。
       贴着环画的长弧读不出「两台智能体连上了」，只读成环上多了一道亮边。"""
    return 0.75 * _GX_OUTR * (1.0 - math.cos(abs(a1 - a0) / 2.0))


def _gx_arcpts(a0, a1, lift, seg=None):
    n = seg or _GX_ARC_SEG
    dip = _gx_arcdip(a0, a1)
    return [(_GX_OUTR - dip * math.sin(math.pi * i / n),
             a0 + (a1 - a0) * i / n,
             lift * math.sin(math.pi * i / n)) for i in range(n + 1)]


def gx_poster(cx, cy, s, thin=4):
    """星系的 **poster**（构建期离线投影 · 一个字都没有 · 不裹 lp —— 由调用方决定）。
       场景每一件都过投影锁 ⇒ 投影落点 = 它的页坐标 ⇒ poster 直接按页坐标画，
       与 WebGL 是同一张图（交接不跳）。件序与 3D 一致：
         外环点 → 24 条弧 → 内环点 → 20 条流中线 → 核点 → 三枚外缘椭圆。
       thin：点云抽稀档（每 thin 枚取一枚）—— 形与密度分布一模一样，只是疏一档。
         · lab / engine P22 走 1/4（≈3,000 枚点）：引擎里它是**永久 2D 正装**，1/8 太稀；
         · info P8 走 1/8（那一份只是降级层，WebGL 一起来就淡出）。
       ⚠ 抽稀是**降级层**的定标，不是另一份几何：取的就是同一批 (r,φ,w)。"""
    o = []

    def dots(cls, rows):
        return ('<path class="%s" d="%s"/>'
                % (cls, "".join("M%s %sh0" % (_n3(q[0]), _n3(q[1])) for q in rows)))
    cloud = {nm: rows for nm, rows in _GX_CLOUD}
    # 外环（蓝 / 紫各半 · 按确定性序交错）
    for cls, par in (("gx-p3", 0), ("gx-p3b", 1)):
        o.append(dots(cls, [_gx_page(p[0], p[1], p[2], cx, cy, s)
                            for i, p in enumerate(cloud["out"])
                            if i % thin == 0 and i % 2 == par]))
    for a0, a1, lift, _ph, _dp in _GX_ARC:
        q = [_gx_page(p[0], p[1], p[2], cx, cy, s)
             for p in _gx_arcpts(a0, a1, lift, seg=24)]
        o.append('<path class="gx-arc" d="M%s"/>'
                 % " L".join("%s %s" % (_n3(t[0]), _n3(t[1])) for t in q))
    # 内环（人 accent / 智能体 蓝 · 按确定性序交错）
    for cls, par in (("gx-p2a", 0), ("gx-p2", 1)):
        o.append(dots(cls, [_gx_page(p[0], p[1], p[2], cx, cy, s)
                            for i, p in enumerate(cloud["in"])
                            if i % thin == 0 and i % 2 == par]))
    for _nm, prm, _w in _GX_STREAM:
        q = [_gx_page(p[0], p[1], p[2], cx, cy, s) for p in prm]
        o.append('<path class="gx-flow" d="M%s"/>'
                 % " L".join("%s %s" % (_n3(t[0]), _n3(t[1])) for t in q))
    o.append(dots("gx-p1", [_gx_page(p[0], p[1], p[2], cx, cy, s)
                            for i, p in enumerate(cloud["core"]) if i % thin == 0]))
    for rr in _GX_RIM:
        o.append('<ellipse class="gx-rim" cx="%s" cy="%s" rx="%s" ry="%s"/>'
                 % (_n3(cx), _n3(cy), _n3(rr * s), _n3(rr * s * _GX_CT)))
    return "".join(o)


def gx_ptpad(s):
    """点云 / 亮斑的**屏上**半径（点径 × 最近处的透视放大 ÷ 2）—— 净空的 pad。
       点径本身是 CSS px（介质常数，不随 s 缩放）；随 s 变的只有那一档透视放大。
       构建期与运行时（Q.ptpad）是同一个数，两条算路不会各算各的。"""
    return max(_cssmax("--gx-core-size"), _cssmax("--gx-in-size"),
               _cssmax("--gx-out-size"), _cssmax("--gx-spark-size")) \
        * _GX_D / (_GX_D - _GX_HALF * s) / 2.0


def _gx_sweep(trips, cx, cy, s, rect, ns=None):
    """(r, |w|, pad) 三元组族 → 扫掠包络的净空探针（舞台像素）。
       自转扫遍整圈 ⇒ φ 本身就是被扫掉的那一维；这里再扫**摇摆**三档与 w 的两个符号。
       运行时量的是族里的**某一帧** ⇒ 解析必然是它的下界。"""
    o = []
    n = ns or _GX_SPINN
    for rr, ww, pad in trips:
        for a in range(n):
            phi = 2 * math.pi * a / n
            for sw in (-_GX_SWAY, 0.0, _GX_SWAY):
                for wsg in ((ww, -ww) if ww else (0.0,)):
                    q = _gx_page(rr, phi, wsg, cx, cy, s, 0.0, sw)
                    o.append((rect[0] + q[0], rect[1] + q[1], pad))
    return o


def _gx_trips(cx, cy, s):
    """净空探针的 (r, |w|, pad) 族 —— 逐件取自真几何，一个数不新造。"""
    t = []
    for i in range(21):                         # 核：厚度剖面的整条外轮廓
        rho = _GX_CORE_R * i / 20.0
        t.append((rho, _gx_coreT(rho), 0.0))
    for r0, r1, tk in ((_GX_IN_R0, _GX_IN_R1, _GX_IN_T),
                       (_GX_OUT_R0, _GX_OUT_R1, _GX_OUT_T)):
        for i in range(5):                      # 环带：r × w 的网格（角点与边全在里面）
            for j in range(3):
                t.append((r0 + (r1 - r0) * i / 4.0, tk * j / 2.0, 0.0))
    for _a0, _a1, _lift, _ph, _dp in _GX_ARC[:3]:   # 弧：三种跨度各取一条
        for p in _gx_arcpts(_a0, _a1, _lift, seg=12):
            t.append((p[0], abs(p[2]), 0.0))
    for _nm, prm, ww in (_GX_STREAM[0], _GX_STREAM[_GX_SN_IN]):   # 流：两种形各取一条
        wp = _wpx(ww, [_gx_page(p[0], p[1], p[2], cx, cy, s) for p in prm], _GX_D)
        for p in prm[::2]:
            t.append((p[0], abs(p[2]), wp))
    return t


def gx_probe(cx, cy, s, rect):
    """整枚星系的净空探针（舞台像素 · 含 pad）—— 构建期解析断言用它逐点量墨迹盒。"""
    pad = gx_ptpad(s)
    return [(x, y, p if p else pad)
            for x, y, p in _gx_sweep(_gx_trips(cx, cy, s), cx, cy, s, rect)]


def gx_lead_clear(ends, cx, cy, s, rect):
    """三处引线落点到**三环扫掠包络**的最小距离（舞台像素）。
       ends = [(r, φ, w), …]（盘面局部 · 未缩放）。构建期 ⓖ / ⑳galaxy 与 qa
       两头拿它对表：落点必须在环带之外 ≥16px —— 机器判据，不是目测。"""
    tri = []
    for i in range(21):
        rho = _GX_CORE_R * i / 20.0
        tri.append((rho, _gx_coreT(rho), 0.0))
    for r0, r1, tk in ((_GX_IN_R0, _GX_IN_R1, _GX_IN_T),
                       (_GX_OUT_R0, _GX_OUT_R1, _GX_OUT_T)):
        for i in range(9):
            for j in range(5):
                tri.append((r0 + (r1 - r0) * i / 8.0, tk * j / 4.0, 0.0))
    band = _gx_sweep(tri, cx, cy, s, rect, ns=96)
    o = []
    for (rr, phi, wo) in ends:
        q = _gx_page(rr, phi, wo, cx, cy, s)
        px, py = rect[0] + q[0], rect[1] + q[1]
        o.append(min(math.hypot(px - t[0], py - t[1]) for t in band))
    return o


def gx_pack(cx, cy, s, w, h):
    """20 股流的世界折线 / 局部串 / 屏上半宽 / 逐股世界速度（构建期算一遍）。
       ⚠ 流速账：A 档 110px/s 是**屏上**的速度。投影锁把页坐标按 k=(D−z)/D 放大进
         世界，所以世界弧长 = ∫k·ds_page；spd_i = 110·Lw/Lp ⇒ 波峰在**屏上**
         恰好 110px/s（参考位姿 spin=0）。data-lab-spd 摊的就是屏上那个 110。"""
    pts, loc, spdrow, wpx, sw, sk, spdv = [], [], [], [], [], [], []
    for idx, (nm, prm, ww) in enumerate(_GX_STREAM):
        q = [_gx_page(p[0], p[1], p[2], cx, cy, s) for p in prm]   # 参考位姿
        Lp, Lw = _lock_len(q, w, h, _GX_D)
        pts.append(q)
        loc.append([(p[0] * s, p[1], p[2] * s) for p in prm])
        wpx.append(_wpx(ww, q, _GX_D))
        sw.append(ww)
        sk.append(1 if idx >= _GX_SN_IN else 0)
        spdv.append(_SPD_A * Lw / Lp)
        spdrow.append((nm, Lp, _SPD_A))
    return dict(w=w, h=h, pts=pts, loc=loc, spd=spdrow, wpx=wpx, sw=sw, sk=sk, spdv=spdv)


def gx_kobj(cx, cy, s, w, h, ink):
    """K 表的 `gx:` 条目 —— 半径 / 厚度 / rim / outr / 抬升 / 深度雾半程 / 流的局部串
       全部按 s 缩放；**sw（带宽）、ptpad、spd、λ 不缩放**（介质常数）。
       makeGalaxy 只读这张表 ⇒ 它天然尺度无关，三个消费方共用同一份 JS。
       ink：调用方给的墨迹名册字面量（"[[x,y,w,h],…]"）。"""
    G = gx_pack(cx, cy, s, w, h)
    return _obj([
        ("D", _n3(_GX_D)), ("half", _n3(_GX_HALF * s)),
        ("c", _arr3([cx, cy])),
        ("tilt", _n3(_GX_TILT)), ("spinP", _n3(_GX_SPINP)),
        ("sway", _n3(_GX_SWAY)), ("swayP", _n3(_GX_SWAYP)),
        ("coreR", _n3(_GX_CORE_R * s)), ("dref", _n3(_GX_DREF * s)),
        ("n0", str(_GX_CORE_N)), ("n1", str(_GX_IN_N)), ("n2", str(_GX_OUT_N)),
        ("r", _arr3([v * s for v in (_GX_CORE_R, _GX_IN_R0, _GX_IN_R1,
                                     _GX_OUT_R0, _GX_OUT_R1)])),
        ("t", _arr3([_GX_IN_T * s, _GX_OUT_T * s])),
        ("cyc", _n3(_GX_CYC)), ("w0", _n3(_GX_W0)), ("wb", _n3(_GX_WB)),
        ("gs", _n3(_GX_GS)), ("floor", _n3(_GX_FLOOR)),
        ("arc", "[" + ",".join(
            "[%s,%s,%s,%s,%s]" % (_n3(_a0), _n3(_a1), _n3(_lf * s), _n3(_ph), _n3(_dp * s))
            for _a0, _a1, _lf, _ph, _dp in _GX_ARC) + "]"),
        ("aseg", str(_GX_ARC_SEG)),
        ("arcdur", _n3(_GX_ARC_DUR)), ("arcfloor", _n3(_GX_ARC_FLOOR)),
        ("outr", _n3(_GX_OUTR * s)), ("spts", str(_GX_SPTS)),
        ("rim", _arr3([v * s for v in _GX_RIM])), ("rimseg", str(_GX_RIM_SEG)),
        ("s", "[" + ",".join('"%s"' % _pk3(_lock_path(q, w, h, _GX_D))
                             for q in G["pts"]) + "]"),
        ("sp", "[" + ",".join('"%s"' % ";".join(
            "%s,%s,%s" % (_n3(t[0]), _n3(t[1]), _n3(t[2])) for t in q)
            for q in G["loc"]) + "]"),
        ("sw", _arr3(G["sw"])),
        ("sk", "[" + ",".join(str(v) for v in G["sk"]) + "]"),
        ("wpx", "[" + ",".join(_n3(v) for v in G["wpx"]) + "]"),
        ("spdv", _arr3(G["spdv"])), ("ptpad", _n3(round(gx_ptpad(s), 3))),
        ("ink", ink),
    ])


# ── ㉒-② P5 三件极致 · 章头的底场（three）──────────────────────────────────
#   语义：这一页是「三件事」的**宣告与索引**，三张数字卡是主角。底场是伴奏 ——
#   三条极细的语义微线在卡下方跑，各自是那件事的**最小表意**，并且都朝下收尾，
#   与卡右上角那三枚章内指针（↓P6 / ↓P7–8 / ↓P9）同向：
#     650ms 延时 = 一记从左到右的**接力**（介质在跑 + 一道注光走完即到）
#     340ms 打断 = 一记**让位**（智能体轨跑到一半落 ghost，用户轨接上并带走收尾）
#     95%  屏蔽 = 一层**薄盾**（三路杂线撞盾消解，只有目标人声从缺口穿过去）
#   ⇒ 底场其实是 P6/P7–8/P9 三章的缩影：读者在索引页就先看见了后面三页的形。
#   克制：底场墨量 ≤ 卡片墨量的 25%（qa ㉒r 用「有/无 canvas 两帧作差」实测）；
#         一根线都不进卡里 —— 三卡的形与字一个像素不动。
_X5RECT = (120, 780, 1680, 124)        # 卡底（y800）与落点句墨迹（y915）之间的空带
_X5INK = [
    (1747, 44, 49, 22), (120, 89, 522, 26), (120, 149, 800, 76), (120, 237, 207, 18),
    (566, 343, 43, 18), (1125, 343, 64, 18), (1726, 343, 43, 18),   # 三枚章内指针
    (161, 392, 438, 308), (741, 409, 438, 283), (1321, 392, 438, 308),   # 三卡内的字
    (150, 915, 609, 32),               # 导航 land
    (120, 1015, 698, 22),              # SOURCE
]
#   ── 表达力精进 · 第二波 ⑤（2026-09-02）：底场重做成「三条支流 → 一条集流」──
#   旧版是三条各讲一件事的极细语义微线（接力 / 让位 / 薄盾）：语义堆得很满，
#   屏上却是三簇互不相干的碎线 —— 读者既读不出三件事，也读不出它们的关系。
#   新版只讲**一件事**，而这一件正是这一页的落点句本人（「三件事，接下来逐页
#   拆开——最后合回一张图」）：三张卡底各垂下一条支流，汇进一条向右的集流带，
#   右端箭头收口。集流带的半宽在每一处汇入点**涨一档**（3.0 → 8.2）——
#   「合回一张图」不是画出来的比喻，是带子自己变粗。
_X5DROPX = (380.0, 960.0, 1540.0)      # 三张卡的水平中点（卡：120/700/1280 · 宽 520）
_X5DROPY = 800.0                       # 卡底
_X5COLY = 875.0                        # 集流带的 y（卡底 800 与落点句墨迹 915 之间）
_X5COLX = (300.0, 1760.0)              # 集流带左右端（右端 = 箭头尖）
_X5ELB = 24.0                          # 支流末端的肘：向右拐进集流带
_X5W = 4.0                             # 支流基准半宽
_X5CW0, _X5CW1 = 3.0, 8.2              # 集流带半宽：起手 → 三条支流全部汇入之后
_X5ARR = 24.0                          # 收口箭头的长（半高 = 它的一半）
_X5HAZE = (140, 806, 1640, 88)         # 底场微粒的铺放区（卡底之下、落点句之上）
_X5HAZEN = 520
_X5HAZER = 1.6                         # 微粒半径留量（--x-haze-size 2.0 ⇒ 半径 1.0 + 余量）
_X5LAM = 138.0                         # 本页 λ 覆写：支流短，λ 得跟着短才看得出起伏
_SPD_P5 = (108.0, 112.0, 106.0, 110.0)  # 三条支流 + 集流带


def _x5_drop(k):
    """一条支流的页坐标折线：卡底垂下 → 一记肘 → 落在集流带上"""
    x = _X5DROPX[k]
    return [(x, _X5DROPY), (x, _X5COLY - 23.0), (x + _X5ELB, _X5COLY)]


_X5COL = [(_X5COLX[0], _X5COLY), (_X5COLX[1], _X5COLY)]
_X5JOIN = tuple(_X5DROPX[k] + _X5ELB - _X5COLX[0] for k in range(3))   # 汇入点的弧长


def _x5_arrow():
    """右端收口箭头的三点（`ah_r` 的 3D 版 —— 页上一个 DOM 件都不新增：
       P5 是加法层页，摘掉这一层必须与母本**逐字节**相同）"""
    x, y, a = _X5COLX[1], _X5COLY, _X5ARR
    return [(x, y), (x - a, y - a * 0.5), (x - a, y + a * 0.5), (x, y)]


# ── ㉒-③ P15 六场景 · 中心辐射（hub）───────────────────────────────────────
#   语义：「一套引擎，支撑多类场景」= **一个核 + 六条支线 + 六簇**。
#   版面给这张图留的路，正好是六张卡之间那条**无字带**：row1 的字止于 y478、
#   row2 的字起于 y631 ⇒ y494–615 整条横带（1680 宽）一个字都没有。核坐在带心
#   (960,556)，六条支线**直线**发散到六簇 —— 真辐射，不是绕来绕去的总线。
#   六簇各落在自家卡的下缘留白里：卡底是 --card-bg（72% 不透明）⇒ 簇在卡**背后**
#   透出来约三成，读成「每个场景自己在跑」；核与支线在卡间空档里是全亮的
#   ⇒ 「中心最亮、六簇微光」这层主次是版面本身给的，不是调出来的。
#   六处身份微动（一处一巧思，全部关在自家 140×40 的簇框里）：
#     外呼=拨号脉冲串 ｜ 智能硬件=设备点阵亮灭 ｜ 虚拟陪伴=柔和呼吸
#     口语陪练=一来一回 ｜ 智能客服=排队消解 ｜ 更多场景=景深处待命的微光星丛
#   ⚠ 中间两卡（02 / 05）的簇**故意不放在核的正上 / 正下方**：那样支线只有 40px，
#     读不成「一条支线」。它们各自挪到卡内的三分位（800 / 1120），
#     顺带让整把扇子有一点旋感 —— 六个方向，不是一面镜子。
_H15RECT = (120, 274, 1680, 576)
_H15INK = [
    (1735, 44, 61, 22), (120, 89, 314, 26), (120, 149, 800, 76), (120, 237, 197, 18),
    (153, 337, 456, 141), (720, 352, 437, 110), (1288, 352, 437, 110),   # row1 三卡的字
    (153, 631, 323, 110), (720, 631, 371, 110), (1288, 631, 437, 110),   # row2 三卡的字
    (120, 988, 826, 20),               # 底部 rail
]
_H15CORE = (960.0, 556.0)
_H15CR = 26.0                          # 旧核的外半径（保留：簇 / 支线的量纲仍按它取）
# ── 表达力精进 · 第二波 ⑦（2026-09-02）：核读不出「引擎」──────────────────
#   旧核是一团点 + 两枚细环 —— 屏上只是一小坨白光，读不出这是引擎。
#   新核 = 与 P13 编排中枢**同血统**的迷你转子：三枚异面椭圆环 + 一条在环之间
#   迁徙的粒子带，参数直接把 _K_ORB 等比缩小。家族一致性在这里就是语义：
#   在 P13 上认过一次的那台转子，在 P15 的中心再出现一次 ⇒ 「一套引擎」。
#   ⚠ 二稿把 _K_ORB 整体等比缩小（36/70），三枚环的**倾角**跟着一起缩 ⇒ 它们
#     几乎共面、边缘朝观众，屏上永远是一枚扁椭圆，认不出转子（终审二波打回）。
#     三稿改成**显式倾角**：一枚近水平（8°）、两枚各倾 ±38°（绕 x 轴），横半轴
#     110 / 96 / 84 —— 三枚环在任何一帧都不共面、投影形状各不相同。倾角还各自
#     慢慢摆动（±_H15ORBAMP），但**不过零** ⇒ 不会有「压成一条线」的那一帧。
#   （rx = 横半轴 · r2 = 环自身的另一条半轴 · tilt = 绕 x 轴的倾角 °）
_H15ORB = ((110.0, 38.0,   8.0),       # 近水平：转子的「赤道」
           ( 96.0, 42.0,  38.0),       # 前倾
           ( 84.0, 44.0, -38.0))       # 后倾（与上一枚交叉）
_H15ORBAMP = 8.0                       # 倾角摆幅（°）—— 不过零，三枚环恒不共面
_H15ORBN = 200                         # 迷你转子的粒子数（P13 是 420，这里是伴奏）
_H15CORER = 7.0                        # **可见的核**：一枚 r≈7 的发光点（三稿新增）
_H15W0, _H15W1 = 2.0, 4.0              # 支线半宽：核端细 → 卡端粗（「流向卡」）


def _h15_orb_box(nth=180, ntl=9):
    """迷你转子在**页坐标**里的包围盒（净空断言用）。
       扫遍三枚环 × 倾角摆幅 × 一整圈 θ × 呼吸两档，并把「翻出核平面之后的透视
       放大」算进去（lockZ 锁在 z = _H15CZ，离面点的放大率 = (D−cz)/(D−z)）。"""
    cx, cy = _H15CORE
    bx, by = 0.0, 0.0
    for rx, r2, tl in _H15ORB:
        for it in range(ntl):
            t = math.radians(tl + _H15ORBAMP * (-1.0 + 2.0 * it / (ntl - 1)))
            for rad in (1.0, 1.0 + _K_ORB_BR):
                for ib in range(nth):
                    th = 2 * math.pi * ib / nth
                    dz = r2 * rad * math.sin(th) * math.sin(t)
                    k = (_H15D - _H15CZ) / (_H15D - (_H15CZ + dz))
                    bx = max(bx, abs(rx * rad * math.cos(th)) * k)
                    by = max(by, abs(r2 * rad * math.sin(th) * math.cos(t)) * k)
    bx = max(bx, _H15CORER); by = max(by, _H15CORER)
    return (cx - bx, cy - by, bx * 2.0, by * 2.0)
#   六簇：[心 x, 心 y, 深度 z, 微动种类]  —— 种类逐条对应页上那六张卡的顺序
_H15CL = [(392.0, 518.0, -140.0, 0), (800.0, 518.0, -200.0, 1), (1527.0, 518.0, -170.0, 2),
          (392.0, 594.0, -180.0, 3), (1120.0, 594.0, -150.0, 4), (1527.0, 594.0, -320.0, 5)]
_H15CLW, _H15CLH = 70.0, 17.0          # 簇框半宽 / 半高（净空判据按这只框逐点量）
_H15D = 1400.0
_H15CZ = 70.0                          # 核所在的那一层（lockZ 的锁面）
_H15LAM = 150.0                        # 本页 λ 覆写：最短的支线只有 165px
_H15W = 3.6
_SPD_P15 = (110.0, 113.0, 108.0, 112.0, 106.0, 109.0)


def _h15_spoke(k):
    """一条支线的页坐标折线（核 → 簇心）—— 直线，六条真发散"""
    c = _H15CL[k]
    return [(_H15CORE[0], _H15CORE[1]), (c[0], c[1])]


# ── ㉒-④ P16 Call Agent 成绩单 · 通话流（calls）────────────────────────────
#   这一页 3D 语义最弱（数字卡 + 对照表），所以做**克制的证据场**，不硬上：
#   「1,000+ 通 / 天 · 多路并发」的可视化 = 一束细密的**通话流**（audioStream 血统），
#   七股并行、从左涌入、过了 x624 之后向右铺开 —— 读作「一直在打、并发在跑」。
#   为什么是「先并拢再铺开」而不是七条平行线：页面左侧 x120–520 有
#   「02 · KEY DIFFERENCE」那行小标，铺开就压字；右半是空的，扇形正好占住。
#   这条形也顺手把上面的成绩单与下面的对照表**缝在一起**（原本两块是断的）。
#   红线：不出价格、不出 staging URL、不出智能体人名；96.5% 的 hot 是页面既有语义，
#   3D **不新造第二处 hot**（流是均质的一束，不给任何一卡加权）。
#   ── 表达力精进 · 第三波 ⑥（2026-09-02 · 三稿）─────────────────────────────
#   二稿把车道排在 y595–624，判据取的是「卡里的字止于 y577」—— **判错了边界**：
#   三张成绩单卡的**盒**到 y610（top340 + 高 270），而卡底是 --card-bg（72% 不透明），
#   车道有一半钻在卡盒底下、从「盲测 32,000…AI」那行字底下透出来，读成卡里的毛刺。
#   **卡盒边才是边界**（卡盒不是墨迹盒，进不了 _N16INK，所以另立一条断言，见 ⑥ 闸）。
#
#   三稿原议是「02 区整体下移 40」把带子腾出来 —— 试了，**不成立**：content 背景板
#   自带一条 accent 细线在 y847–853（x117–761），rule(850) 的既定职责就是压住它；
#   02 区一下移，收口线跟着走到 890，那条亮条就从对照表的第三行里露出来（实拍已确认：
#   一条只到半幅的粉色横杠压在「合规」行的分隔线下面）。而对照表要躲开 847–853，
#   要么整表止于 847（Δ ≤ 3，等于没移）、要么整表起于 853（Δ ≥ 177，撞落点句）——
#   都不可能。⇒ **02 区不能动**，收口线必须留在 850。
#
#   所以改成把**车道整束搬家**：全页在 ≥16px 净空下唯一还剩的空带，是对照表墨迹底
#   （y839）与落点句墨迹顶（y959）之间那 120px。八条 @4.6 间距 + 半宽 1.8 = 35.8px
#   在其中居中 ⇒ 上下各留 42.1px，且整束远在卡盒（610）之外。页面 DOM 一个字节没动
#   （P16 仍走「摘层即母本逐字节」那条最硬的自证）。
_N16CARDB = 610.0                      # 三张成绩单卡的**盒底**（top340 + 高270）
_N16INK = [
    (1735, 44, 61, 22), (120, 89, 539, 26), (120, 149, 1137, 76), (120, 251, 797, 30),
    (120, 307, 153, 18),
    (151, 367, 463, 210), (721, 367, 333, 199), (1291, 367, 320, 199),   # 三张成绩单卡的字
    (120, 641, 400, 18),               # 02 · KEY DIFFERENCE 小标
    (120, 678, 1081, 161),             # 对照表的字（表头 + 三行）
    (150, 959, 450, 32), (120, 1015, 643, 22),
]
_N16TABB = 678 + 161                   # 对照表墨迹底（车道的上界）
_N16LANDT = 959                        # 落点句墨迹顶（车道的下界）
_N16RECT = (120, 852, 1680, 92)        # 舞台矩形跟着车道搬到收口线之下
#   ── 表达力精进 · 第二波 ⑥（2026-09-02）：卡下那把扇子重做 ─────────────────
#   旧版是七股「先并拢再铺开」的扇形：屏上是一团糊光，读不出任何东西。
#   新版把语义钉死成成绩单上那一行数字本人 ——「1,000+ 通 / 天 · 多路并发」：
#   **八条并行细带**横贯卡底与对照表之间向右流，每条带的 gain 剖面是一串
#   **确定性的通话段**（起停各自不同相）⇒ 屏上永远有几路在通话、几路刚挂断，
#   而八条一起在跑就是「并发」。零随机源：段长 / 占空 / 相位全是构建期的定数。
#   三稿把整束搬到对照表与落点句之间那条空带（见上面那一段的账）。
_N16X0, _N16X1 = 120.0, 1800.0
_N16N = 8                              # 股数（「多路并发」——不是一条）
_N16DY = 4.6                           # 相邻两条的间距（三稿：4.0 → 4.6）
_N16W = 1.8                            # 细：单路通话是细的，八路一起才是量
#   整束在 [表底+16, 落点句顶−16] 里居中 —— 上下净空自动相等（构建期实测 42.1px）
_N16LO = _N16TABB + _ADD_CLR
_N16HI = _N16LANDT - _ADD_CLR
_N16Y0 = (_N16LO + _N16HI) / 2.0 - _N16DY * (_N16N - 1) / 2.0
_N16LAM = 196.0
_SPD_P16 = (110.0, 107.0, 113.0, 109.0, 112.0, 106.0, 111.0, 108.0)
#   每条带的通话段：(段周期 px, 占空, 起相位) —— 八条两两不同周期 ⇒ 永不齐步
_N16CALL = tuple((248.0 + 31.0 * k, 0.50 + 0.05 * (k % 3), (k * 0.37) % 1.0)
                 for k in range(_N16N))
_N16CE = 0.055                         # 通话段起停的 smootherstep 半宽（归一化到周期）


def _n16_y(k):
    return _N16Y0 + _N16DY * k


def _n16_lane(k, n=2):
    """一股通话流的页坐标折线：x120→1800 的**水平直线**（并行，不再是扇形）"""
    y = _n16_y(k)
    return [(_N16X0, y), (_N16X1, y)]


# ── 加法层三页的墨迹名册（build() ㉒ 闸与 qa ㉒ 闸共用同一张表）─────────────
_ADD_INK = {5: _X5INK, 15: _H15INK, 16: _N16INK}
_ADD_RECT = {5: _X5RECT, 15: _H15RECT, 16: _N16RECT}


def _box_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]


def _box_hit(box, ink):
    """一只框里有没有落进任何一只墨迹盒（有 ⇒ 只量边界是不够的，得当场报）"""
    x, y, w, h = box
    return any(not (bx + bw <= x or bx >= x + w or by + bh <= y or by >= y + h)
               for (bx, by, bw, bh) in ink)


def _box_gap(a, b):
    """两只矩形的最小间距（相交 ⇒ 0）"""
    dx = max(b[0] - (a[0] + a[2]), a[0] - (b[0] + b[2]), 0.0)
    dy = max(b[1] - (a[1] + a[3]), a[1] - (b[1] + b[3]), 0.0)
    return math.hypot(dx, dy)


def _add_clr_min(p):
    """一页 3D 几何与该页**字形墨迹盒**的最小净空（px · 已扣掉带宽 / 粒半径）。
       与运行时 `state().clr` 是同一个量的两条独立算路：构建期解析、运行期把
       真的传上 GPU 的顶点投影回舞台像素 —— 两边对不上就是两套解，当场报。"""
    if p == 5:
        m = min(_poly_clr(_x5_drop(k), _X5INK) for k in range(3)) - _X5W
        m = min(m, _poly_clr(_X5COL, _X5INK) - _X5CW1)
        m = min(m, _poly_clr(_x5_arrow(), _X5INK) - 1.5)
        assert not _box_hit(_X5HAZE, _X5INK), "㉒ P5 底场铺放区压上了墨迹盒"
        return min(m, _poly_clr(_box_pts(*_X5HAZE), _X5INK) - _X5HAZER)
    if p == 15:
        m = min(_poly_clr(_h15_spoke(k), _H15INK) for k in range(6)) - _H15W1
        _ob = _h15_orb_box()
        assert not _box_hit(_ob, _H15INK), "㉒ P15 迷你转子压上了墨迹盒"
        m = min(m, min(_box_gap(_ob, b3) for b3 in _H15INK))
        for c in _H15CL:
            box = (c[0] - _H15CLW, c[1] - _H15CLH, _H15CLW * 2, _H15CLH * 2)
            assert not _box_hit(box, _H15INK), "㉒ P15 第 %d 簇压上了墨迹盒" % c[3]
            m = min(m, _poly_clr(_box_pts(*box), _H15INK) - 2.5)
        return m
    if p == 16:
        return min(_poly_clr(_n16_lane(k), _N16INK) for k in range(_N16N)) - _N16W
    raise SystemExit("㉒ 未知的加法层页 P%d" % p)


_ADD_CLRMIN = {p: _add_clr_min(p) for p in _ADD_PAGES}


# ═══ 表达力精进 · 第一波：P2 / P4 的净空名册（沿用加法层那把尺子）═══════════
#   加法层四页的 ≥16px 净空规则本来只管「页上没有图、3D 是加在版面之外那一层」
#   的四页。本轮把它借到两页**有图**的页上：
#     P2 —— 02 区是全新长出来的一带，两排带子与五处字必须各走各的；
#     P4 —— 病名 B 的正身：舞台过去就压在三行说明底下。
#   墨迹盒一律**实测**（Range.getClientRects 量的字形行框，不是 line-height 盒），
#   量法与 _ADD_INK 那四页同一条：舞台坐标 1920×1080，(x, y, w, h)。
#   ⚠ 盒子取**两次实测的并集再各留 _INKPAD**：舞台是 transform:scale 的固定 1920
#     画布，不同跑次的缩放取整会让同一处字形漂 ±2.5px；名册宁可宽一档，也不许压字。
_INKPAD = 3.0                    # 名册相对实测墨迹的四周留量（px）
#   P2 同源自证的**白名单**（第二波 0）：下排补的四枚字串，一个不多一个不少
_P2WL_DECL = ("听", "想", "说", "边说边听 ✓")
_P2INK = [                    # 02「两制对照」的五处字（DOM 序 = 阅读序）
    (114, 815, 58, 24),          # 回合制（上排行标 · mono · 左栏，与带子同中线）
    (544, 774, 40, 24),          # 听完（段标行 · 居中于上排 听 段）
    (951, 774, 23, 24),          # 想（段标行 · 居中于「想」虚线框）
    (1447, 774, 23, 24),         # 说（段标行 · 居中于上排 说 段）
    (1685, 774, 111, 24),        # 听完再回答 ✕（段标行行尾判词 · 右对齐 1800）
    (113, 865, 23, 25),          # 听（下排 lane 标 · accent）
    (113, 895, 23, 25),          # 想
    (113, 925, 23, 25),          # 说
    (1707, 962, 91, 26),         # 边说边听 ✓（下排判词 · 右对齐 1800）
]
_P4INK = [                       # 三行说明（病名 B 的对象；其余字不在本轮名册内）
    (268, 285, 609, 32),         # 连续拾音 · VAD 持续检测 · 流式 ASR——不切段，不等你说完
    (268, 399, 466, 32),         # 增量理解 · 每一瞬间都在判断：现在要不要出声
    (268, 513, 272, 32),         # 流式 TTS · 随时可收声让位
]
_INK = {2: _P2INK, 4: _P4INK}
_CLR = {2: _ADD_CLR, 4: _ADD_CLR}   # 下限 16px（与加法层同一档，不许放松）

# ── ⑥ 互动星系（P22）的墨迹名册与净空账 ────────────────────────────────────
#   舞台 = figbox(1060,130,760,800)，右半整块。名册登记三类字：
#     ① 三区标注九行（序号 / 名·状态 / 副行 × 3）—— 它们就画在舞台之内，
#        引线端点必须落在环带之外 ≥16px，字更不许被点云压上；
#     ② 角注（「互动星系示意 …」· 与左列 mono-sm ② 同一条 y1004 基线）；
#     ③ 左列里离舞台 ≤200px 的字形盒 —— 舞台左缘 x1060，所以右缘越过 x860 的
#        那几行（quote 三行 / 使命 · 愿景 / 两行 mono-sm）也入册。
#   盒子一律**实测**（Range.getClientRects 量的字形行框，不是 line-height 盒），
#   四周各留 _INKPAD；量法与 _P2INK / _P4INK 同一条。
#   量法：`node scripts/measure-p22-ink.mjs`（浅 / 暗两档取并集，四周各留 3px）。
#   同一条视觉行被 <span>/<strong> 切成几段的，按行合并成一只盒。
_P22INK = [
    (1732, 41, 67, 28),          # 页码 22/22 —— 舞台右上角之外最近的一处字
    # ── 左列里离舞台（x1060）≤200px 的两行：quote 的一 / 二行，右缘 x983 / x967 ──
    (117, 458, 866, 58),         # quote ①「全球最强的 Voice Agent 团队，在为他们的」
    (117, 521, 850, 58),         # quote ②「Realtime API 寻找 对话式 AI 引擎底座 时，」
    # ── 三区标注九行（就画在舞台之内 —— 点云 / 弧 / 流绝不许压上它们）──────────
    (1077, 180, 22, 23),         # 01
    (1077, 200, 172, 29),        # 人与人 · 已经发生
    (1077, 233, 171, 24),        # 实时音视频 · 2014 年起
    (1781, 180, 22, 23),         # 02
    (1589, 200, 214, 29),        # 人与智能体 · 正在发生
    (1542, 233, 261, 24),        # 对话式 AI 引擎 · 企业级智能体 · R1
    (1781, 784, 22, 23),         # 03
    (1547, 804, 256, 29),        # 智能体与智能体 · 即将发生
    (1615, 837, 188, 24),        # 智能体之间的实时对话与协作
    # ── 角注（右对齐 1800 · 与左列 mono-sm ② 同一条 y1004 基线）────────────
    #    2026-09-03 终审：句子去掉色名之后短了 218px，盒左缘随之右移（右缘不动）。
    (1396, 1001, 407, 26),       # 互动星系示意 · 三环由内向外生长 · 环径不代表规模
]
# 三处引线落点的**盘面局部**参数（引线 d 的首点 = 它的投影 · ⑳galaxy 逐条对表）：
#   01 (r=150, φ=180°) 核与内环之间那圈净空的**正左侧**（实测 21.9px）；
#   02 (r=316, φ=0°)   内环与外环之间那圈净空的**正右侧**（实测 19.1px）——
#      两枚落点都坐在盘面的长轴上，与盘心同一条水平线，读起来是一对；
#   03 (r=600, φ=50°)  外环外缘之外的右下方（实测 31.6px），引线走一段斜向短线。
#   ⚠ 这三组数是**扫掠包络实测**挑出来的，不是画上去的：s=0.75 之后净空跟着缩
#     （16px 下限**不缩**），Fable 设计稿的 (315,−4°) / (530,45°) 分别只剩
#     16.2 / 4.1px —— 沿等值线各挪了一档，落点位移都在 ±12px 之内。
_GX22_LEAD_END = ((150.0, math.pi, 0.0), (316.0, 0.0, 0.0),
                  (600.0, math.radians(50.0), 0.0))
_GX22PACK = gx_pack(GX22["cx"], GX22["cy"], GX22["s"],
                    GX22["rect"][2], GX22["rect"][3])
_GX22_ZMAX = (_GX_OUT_R1 * _GX_ST + _GX_OUT_T * _GX_CT) * GX22["s"]
_GX22_LEAD = gx_lead_clear(_GX22_LEAD_END, GX22["cx"], GX22["cy"], GX22["s"],
                           GX22["rect"])
_GX22_PROBE = gx_probe(GX22["cx"], GX22["cy"], GX22["s"], GX22["rect"])


def _p22_clr_min():
    """星系扫掠包络（含点径 / 带宽 pad）到 P22 字形墨迹盒的最小净空（舞台像素）。
       与运行时 `state().clr` 是同一个量的两条独立算路。"""
    m = 1e9
    for px, py, pad in _GX22_PROBE:
        for b in _P22INK:
            d = _ink_clr((px, py), [b]) - pad
            if d < m:
                m = d
    return m


_P22CLRMIN = _p22_clr_min()


def _p2_geo_boxes():
    """02 区几何的**页坐标**包围盒表（净空断言用；带子按基准半宽取最大外缘）。
       局部 → 页：x + 120 / y + 780（02 figbox 的位）。"""
    X, Y = 120.0, 780.0
    out = [(X + _P2TX0, Y + _P2RY - _P2RW, _P2TX1 - _P2TX0, _P2RW * 2)]      # 上排带
    out.append((X + _P2DKX[0], Y + _P2RY - _P2DKH,                            # 「想」虚线框
                _P2DKX[1] - _P2DKX[0], _P2DKH * 2))
    ex = X + _P2TX0 + (_P2TX1 - _P2TX0) * _P2EVT
    for yc in (_P2RY, _P2LY[2]):                                              # 两枚事件竖标
        out.append((ex - 2.0, Y + yc - _P2EVH, 4.0, _P2EVH * 2))
    for k in range(3):                                                        # 下排三条带
        x0 = _P2TX0 + ((_P2TX1 - _P2TX0) * _P2SPK if k == 2 else 0.0)
        out.append((X + x0, Y + _P2LY[k] - _P2LW[k], _P2TX1 - x0, _P2LW[k] * 2))
    return out


def _p4_geo_lanes():
    """P4 两条声带的**页坐标**折线（局部 → 页：x + 120 / y + 268）"""
    X, Y = LAB_RECTS[4][1], LAB_RECTS[4][2]
    return [[(X + p[0], Y + p[1]) for p in _d_lane(s, ph)]
            for s, ph in ((1, 0.0), (-1, _D_PHASE))]


_P2CLRMIN = min(_box_gap(g, b) for g in _p2_geo_boxes() for b in _P2INK)
_P4CLRMIN = min(_poly_clr(q, _P4INK) for q in _p4_geo_lanes()) - 11.0   # 减掉带子半宽


def _spd_rows(p):
    """A 档（连续媒体流）**逐股速度表**：[(名字, 页上像素路径长, px/s)]。
       这是本波「速度品味检查」的唯一真相 —— 周期由 `长 ÷ 速` 反推（_dur_at），
       结果同时摊进 data-lab-spd 供 ⑲s 复算：表与实现不可能分叉。
       B 档（P14 注光 400px/s，离散事件）与 C 档（页面 CSS 同源）不在这张表里。"""
    if p == 2:
        # 波B：主环 / 支轨 → **入射波场 / 出射波场**。两条都是声波场，波峰速度就是
        # 相速度（A 档）；「长」取波场在页上横跨的像素（入射 X0→X1，出射整体右移
        # _MO_OUTDX 之后越过 vb 右缘 ⇒ 倾泻出画）。
        span = _MO_X1 - _MO_X0
        # 表达力精进 ①：02「两制对照」四股 —— 与剧场同一条河（同介质就是同流速档）
        tw = _P2TX1 - _P2TX0
        return [("入射波场", span, _SPD_P2[0]), ("出射波场", span, _SPD_P2[1]),
                ("入场弧流", _plen_d(_P2ARC, per=18, tol=1.2), _SPD_P2[0]),
                ("回合制轨", tw, _SPD_P2B[0]), ("并行听", tw, _SPD_P2B[1]),
                ("并行想", tw, _SPD_P2B[2]),
                ("并行说", tw * (1.0 - _P2SPK), _SPD_P2B[3])]
    if p == 4:
        return [("上行声带", _plen(_d_lane(1, 0.0)), _SPD_P4[0]),
                ("下行声带", _plen(_d_lane(-1, _D_PHASE)), _SPD_P4[1])]
    if p == 6:
        rows = [("主路", float(_P6X1 - _P6X0), _SPD_P6[0])]
        for k, (a, b2) in enumerate(_P6SEG):
            rows.append((_P6SEGNM[k], float(b2 - a), _SPD_P6[1 + k]))
        for k, (a, b2, _y) in enumerate(_P6BAND):
            rows.append(("增量带%d" % (k + 1), float(b2 - a), _SPD_P6[5 + k]))
        return rows
    if p == 8:
        L = float(_U_TX1 - _U_TX0)
        return [("智能体轨", L, _SPD_P8[0]), ("用户轨", L, _SPD_P8[1])]
    if p == 9:
        d = [346.0 - _SR2, 346.0 - _SR2, 346.0 - _SR1, 346.0 - _SAG * 0.46 * 0.8]
        nm = ("噪声01", "噪声02", "噪声03", "目标人声")
        return [(nm[k], d[k], _SPD_P9[k]) for k in range(4)]
    if p == 7:
        # 波B：地形整幅左移（A 档基准本人）—— 一趟 980 ÷ 110 = 8.91s
        return [("地形整幅", _T_X1 - _T_X0, _SPD_P7)]
    if p == 10:
        # 波B：四条车道 + 四道握手（介质 → 流带）。长度取**页上**的像素路径长。
        rows, k = [], 0
        for i in _M_MEDL:
            r = _P10LANE[i]
            rows.append(("车道%d" % (k + 1), abs(r[1] - r[0]), _SPD_P10[k])); k += 1
        for i in _M_MEDB:
            r = _P10BEAM[i]
            rows.append(("握手%d" % (k - 3), math.hypot(r[3] - r[0], r[4] - r[1]),
                         _SPD_P10[k])); k += 1
        return rows
    if p == 12:
        m, hub = _W_MOUTH, _P12BOX[0]
        L = math.hypot((hub[0] + hub[2] / 2.0) - (m[0] + m[2] / 2.0),
                       (hub[1] + hub[3] / 2.0) - (m[1] + m[3] / 2.0))
        return [("画面平面", L, _SPD_P12[0])]
    if p == 13:
        # 波B：新增**贯通流**（一条 audioStream 走完全程）—— 它是本页唯一的介质，
        # 必须进 A 档表。九股总线包本来就在档内（92.9–94.3），一个数没动。
        out = [("贯通流", _plen(_P13FLOW), _SPD_P13)]
        for k, r in enumerate(_P13RUN):
            L = math.hypot(r[2] - r[0], r[3] - r[1])
            out.append(("总线包%d" % (k + 1), L, L / r[4]))
        return out
    if p == 5:
        # ⑤：底场四股（三条支流 + 一条集流带）—— 都在 A 档，「细」是宽度的事，
        # 不是速度的事：它们与主图那些流是同一条河。
        rows = [("支流%d" % (k + 1), _plen(_x5_drop(k)), _SPD_P5[k]) for k in range(3)]
        rows.append(("集流带", _plen(_X5COL), _SPD_P5[3]))
        return rows
    if p == 15:
        return [("支线%d" % (k + 1), _plen(_h15_spoke(k)), _SPD_P15[k]) for k in range(6)]
    if p == 16:
        return [("通话流%d" % (k + 1), _plen(_n16_lane(k)), _SPD_P16[k])
                for k in range(_N16N)]
    if p == 18:
        return [("复利螺旋", _plen(_spiral_pts()), _SPD_P18[0]),
                ("loop 环流", 2 * math.pi * float(_CA_RING[2]), _SPD_P18[1])]
    if p == 22:
        # ⑥ 互动星系：20 股（14 核↔内环 + 6 内环→外环）。**逐股给自己的世界速度**
        # （spdv = 110·Lw/Lp，见 gx_pack）⇒ 波峰在**屏上**恰好 110px/s，
        # 所以这张表里 20 股一律 110 —— 与全家族同一种介质，同一个数。
        return list(_GX22PACK["spd"])
    return []


def _spd_attr(p):
    r = _spd_rows(p)
    return [("spd", ";".join("%s,%s" % (nm, _f1(s)) for nm, _L, s in r))] if r else []


def lab_data(p):
    """把该页场景的**周期 / 相位 / 关键几何**摊到舞台的 data-* 上（LAB 家族规矩）。
       闸门因此可以静态复算：谐波频率两两不整除、弧相位永不齐步、五区周期互异、
       事件 x 与页上一致……不必去读着色器，也不必截图比对。
       ⚠ 这些值与 lab_k() 出自同一批常量 —— 一处改，两处一起动。"""
    a = []
    if p == 1:
        a += [("spin", VSPIN), ("intro", VINTRO), ("pts", VN), ("amp", VAMP), ("w0", VW0),
              ("harm", ";".join(",".join(str(x) for x in h) for h in VHARM)),
              ("hot", "%s,%s" % VHOT)]
    elif p == 21:
        a += [("spin", GSPIN), ("intro", GINTRO), ("nodes", len(_NODES_LL)),
              ("routes", len(_ROUTES)), ("arc-dur", ARC_DUR_S.strip("[]")),
              ("arc-gap", ARC_GAP_S.strip("[]")), ("arc-off", ARC_OFF_S.strip("[]"))]
    elif p == 17:
        a += [("zper", ",".join(str(_sec(z[1])) for z in _ZONES)),
              ("zoff", ",".join(str(_sec(z[2])) for z in _ZONES)),
              ("arcs", len(_ARCS)), ("sparks", len(_ARCS) + len(_ARC_EXTRA)),
              ("sway", 12), ("sway-p", 17)]
    elif p == 18:
        # 二轮精修 · 波A：整条曲线图**改坐标本身**左移 _CA_DX（不加 transform，见指南 ⑧），
        # 图例留 x0 不跟移；舞台从 1240 扩到 1680 横跨两图，loop 环带走投影锁。
        a += [("days", ",".join(str(_CA_X(x)) for x, _nm in _CA_DAYS)),
              ("turns", _CA_TURNS), ("climb", _f1(_dur_at(_plen(_spiral_pts()), _SPD_P18[0]))),
              ("shift", _CA_DX), ("base", "%d,%d,%d" % (_CA_X(150), 160, _CA_X(1060))),
              ("ring", "%d,%d,%d" % _CA_RING), ("ringdx", _CA_RDX)]
    elif p == 7:
        a += [("pins", "%d,%d" % (_VSOS, _VEOS)), ("band", "%d,%d" % (_VTOP, _VBOT)),
              ("steps", 1),
              # 波B 消闪：周期 / 一趟秒数 / 表长 / 首尾落差（周期化之后必须是 0）
              ("per", _n(_T_X1 - _T_X0)), ("lap", _n((_T_X1 - _T_X0) / _SPD_P7)),
              ("nt", _T_NT), ("seam", _n(round(_vad_tables()[0][-1] - _vad_tables()[0][0], 6)))]
    elif p == 9:
        a += [("rings", "%d,%d" % (_SR1, _SR2)), ("gap", "35,40"), ("streams", 3)]
    elif p == 4:
        # 表达力精进 ②：起点 / 圈数进名册（turns 不再写死字面量），三行说明的
        # 墨迹盒与实测净空一并摊上来 —— 舞台再往左挪一格，构建期就当场炸。
        a += [("cut", _XIN), ("now", _XNOW), ("turns", _n(_D_TURNS)),
              ("x0", "%d" % int(LAB_RECTS[4][1] + _D_X0)),
              ("ink", ";".join("%d,%d,%d,%d" % b for b in _P4INK)),
              ("clr", _n(_CLR[4])), ("clr-min", _f1(_P4CLRMIN))]
    # ── 第二波九页（2026-08-31 · 终波）：闸门静态复算要用的周期 / 相位 / 关键几何 ──
    elif p == 2:
        # 波B · 模态转换剧场：⑲h 用这几张表**复算相位**（不靠截帧）——
        # 三态权重和恒为 1、生灭窗落在 uLife=0 的那一段、让位事件坐在「想」的窗口里、
        # 两代相位差正好是半周期。
        a += [("cyc", _n(_MO_CYC)), ("gen", _n(_MO_GEN)),
              ("ph", ",".join(_n(x) for x in _MO_PH)),
              ("life", ",".join(_n(x) for x in _MO_LIFE)),
              ("yaw", ",".join(_n(x) for x in _MO_YAW)), ("yawa", _n(_MO_YAWA)),
              ("grid", "%d,%d,%d" % (_MO_NA, _MO_NB, _MO_NC)),
              ("verts", _MO_NA * _MO_NB * _MO_NC),
              ("lam", _n(_AS_LAM)),          # 波长逐字取 lab-kit ⑨ ⇒ 同一种介质
              ("boxes", len(_P2N)), ("cols", ",".join(str(b[0]) for b in _P2N)),
              ("hotcol", _O_HOTCOL), ("arc", ",".join(_n(x) for x in _MO_ARC)),
              ("stage", "%d,%d" % (int(_MO_X0), int(_MO_X1 + _MO_OUTDX))),
              # 表达力精进 ①：02「两制对照」—— 剧场原高（相机按它架）/ 02 区顶 /
              # 时间轴 / 三段 u / 事件 u / 让位窗口 / 净空实测
              ("h0", _n(_MO_H0)), ("ay", _n(_P2AY)),
              ("tx", "%d,%d" % (int(_P2TX0), int(_P2TX1))),
              ("seg", ";".join("%s,%s" % (_n(s[0]), _n(s[1])) for s in _P2SEG)),
              ("evt", _n(_P2EVT)), ("duck", _n(_P2DUCK)),
              ("ink", ";".join("%d,%d,%d,%d" % b for b in _P2INK)),
              ("clr", _n(_CLR[2])), ("clr-min", _f1(_P2CLRMIN))]
    elif p == 3:
        # 三种模式的通道相位表：与页上 .mo-packet 的实参逐参同源 ——
        # 闸门用 (L+seg)/(seg+ln) 复算占空比、再逐时刻验半双工「任何时刻只有一个方向在途」。
        a += [("seg", 14), ("modes", 3), ("dep", _L_DEP)]
        for _m in ("simplex", "half", "full"):
            a.append((_m, ";".join("%s,%s,%s,%s,%s" % (c[2], c[3], c[4], c[5], c[6])
                                   for c in _P3CH[_m])))
    elif p == 6:
        a += [("stations", len(_PIPE)), ("steps", 1), ("bands", 4),
              ("znear", _C_ZNEAR), ("zdeep", _C_ZDEEP),
              # 横贯全链一条流的跨度 + 符号行四段的接缝（三处，⑲(P6) 复算「有没有缝」）
              ("span", "%d,%d" % (_P6X0, _P6X1)),
              ("seg", ";".join("%d,%d" % s for s in _P6SEG)),
              ("seam", ",".join(str(_P6SEG[i][1]) for i in range(3))),
              ("token", _P6TOKEN)]
    elif p == 8:
        a += [("in", _P9IN), ("cut", _P9CUT), ("fall", _P9CUT - _P9IN),
              ("ghost", _AS_GHOST),
              # 让位窗口 = 页上「收声」那段相位括号（840→1040，200px），⑲(P8) 逐条复算
              ("duck", "%d,%d" % (_U_DUCK0, _P9CUT)),
              # 解析包络的谐波表（⑲as 收敛阶闸用它复算）
              ("as", "%s|%s|%s|%s" % (",".join(_n(x) for x in _AS_A),
                                      ",".join(_n(x) for x in _AS_F),
                                      ",".join(_n(x) for x in _AS_PH), _n(_AS_LAM))),
              # 反证用：旧版逐柱包络的定高表 + 起点 / 柱距（这一闸它必须过不了）
              ("hs", ",".join(str(v) for v in _P9HS)), ("bar", "170,17")]
    elif p == 10:
        a += [("layers", len(_M_ZL)), ("boxes", len(_P10BOX)), ("zl", ",".join(str(z) for z in _M_ZL)),
              ("lanes", len(_P10LANE)), ("beams", len(_P10BEAM)),
              # 波B 轻手术：介质（→ 流带）与离散事件（保持粒子）各几条 —— 逐条判的结果
              ("med", "%d,%d" % (len(_M_MEDL), len(_M_MEDB))),
              ("evt", len([r for r in _P10BEAM if not r[8]])),
              ("drift", 0)]      # 相机不动、层不做视差位移（可读性红线：0 就是 0）
    elif p == 11:
        a += [("dark", "%d,%d" % _WN_DARK), ("loss", "%d,%d" % _WN_LOSS),
              ("heap", "%d,%d" % (_Q_HX0, _Q_HX1)), ("rain", len(_Q_RAIN)),
              ("rain-dark", sum(1 for x in _Q_RAIN
                                if _WN_DARK[0] <= x <= _WN_DARK[0] + _WN_DARK[1])),
              ("out", _Q_OUTN)]
    elif p == 12:
        a += [("apex", "%d,%d" % _W_APEX), ("mouth", ",".join(str(v) for v in _W_MOUTH)),
              ("weak", len(_P12WEAK)), ("zweak", _W_ZWEAK)]
    elif p == 13:
        a += [("slots", len(_P13SLOT)), ("cyc", _K_CYC), ("swap", _K_SW), ("cav", _K_CAV),
              # 波B · 中枢机：⑲h 逐条复算「机腔 / 内肋 / 核 / 脉冲 / 贯通流 / 闭环 / 热切换」
              ("hubcav", _n(_K_HUBCAV)), ("ribs", _K_RIB),
              ("core", _K_CORE_N), ("pub", _n(_K_PUB)),
              ("pubpath", ";".join("%d,%d" % q for q in _P13PUB)),
              # 终审硬伤一：转子净空 —— 墨迹盒 / 三枚轨道 / 构建期实测净空 / 包围盒
              ("ink", ";".join("%d,%d,%d,%d" % b for b in _P13INK)),
              ("orb", ";".join("%s,%s,%s" % tuple(_n(v) for v in o) for o in _K_ORB)),
              ("clr", _n(_K_CLR)), ("clr-min", _f1(_K_CLR_MIN)),
              # 终审硬伤二：贯通流的落点（页坐标）与发布槽右缘 —— ⑲p13 逐条复算
              ("flow-end", "%d,%d" % (LAB_RECTS[13][1] + _P13FLOW[-1][0],
                                      LAB_RECTS[13][2] + _P13FLOW[-1][1])),
              ("flow-sink", "%d" % (LAB_RECTS[13][1] + _P13PILL[0] + _P13PILL[2])),
              ("flow-amp", "%s,%s,%s,%s" % (_n(_K_FLOWW), _n(_K_FLOWFLOOR),
                                            _n(_K_FLOWGHOST), _f1(_k_flow_lam()))),
              ("flow-len", _n(_plen(_P13FLOW))),
              ("gz", ";".join("%s,%s" % (_f1(g[0]), _f1(g[1]))
                              for g in (_box_u(_P13FLOW, b) for b in _P13GHOST) if g)),
              ("loops", len(_P13LOOP)), ("loop-off", _n(_K_LOOP_OFF)),
              ("busx", _K_BUSX),
              ("swz", _n(_K_SWZ)),
              ("sw-a", ",".join(_n(x) for x in _K_SWA)),
              ("sw-b", ",".join(_n(x) for x in _K_SWB))]
    elif p == 14:
        a += [("towers", len(_P14T)), ("arcs", len(_P14ARC)), ("steps", 1),
              ("z", ",".join(str(z) for z in _Y_Z)), ("cyc", _n(_Y_CYC)),
              # B 档：注光速度 + 三段路由长 + 生长 / 全亮停驻 / 收尾 —— ⑲(P14) 逐条复算
              ("beam", _n(_Y_BEAM)),
              ("route", ",".join(_n(_plen_d(a2[0])) for a2 in _P14ARC)),
              ("grow", _n(_Y_GROW)), ("hold", _n(_Y_HOLD)), ("rel", _n(_Y_REL))]
    # ── 三轮：四枚加法层（共同摊 add / ink / clr —— ㉒ 闸靠这三样逐页复算）──────
    elif p == 5:
        a += [("add", 1), ("lines", 3), ("streams", len(_SPD_P5)),
              ("join", ",".join(_f1(v) for v in _X5JOIN)),
              ("col", "%s,%s,%s" % (_f1(_X5COLX[0]), _f1(_X5COLX[1]), _f1(_X5COLY))),
              ("haze", "%d,%d,%d,%d" % _X5HAZE), ("hazen", _X5HAZEN),
              ("lam", _n(_X5LAM)), ("w", _n(_X5W)), ("cw", _n(_X5CW1))]
    elif p == 15:
        a += [("add", 1), ("core", "%s,%s,%s" % (_f1(_H15CORE[0]), _f1(_H15CORE[1]),
                                                 _f1(_H15CR))),
              ("orb", ";".join("%s,%s,%s" % tuple(_f1(v) for v in o) for o in _H15ORB)),
              ("orbamp", _n(_H15ORBAMP)), ("corer", _n(_H15CORER)),
              ("orbbox", ",".join(_f1(v) for v in _h15_orb_box())),
              ("cl", ";".join("%s,%s,%s,%d" % (_f1(c[0]), _f1(c[1]), _f1(c[2]), c[3])
                              for c in _H15CL)),
              ("clbox", "%s,%s" % (_f1(_H15CLW), _f1(_H15CLH))),
              ("lam", _n(_H15LAM)), ("w", _n(_H15W))]
    elif p == 16:
        a += [("add", 1), ("lanes", _N16N), ("dy", _n(_N16DY)),
              ("band", "%s,%s" % (_f1(_n16_y(0) - _N16W),
                                  _f1(_n16_y(_N16N - 1) + _N16W))),
              ("call", ";".join("%s,%s,%s" % tuple(_f1(v) for v in c)
                                for c in _N16CALL)),
              ("lam", _n(_N16LAM)), ("w", _n(_N16W))]
    elif p == 22:
        # ⑥ 互动星系：尺度 / 点数 / 三环半径与厚度（**已按 s 缩放** = 屏上真值）/
        # 倾角 / 转速与摇摆 / 弧与流的股数 / 生灭窗（0.4s 归零）与它的相位表 /
        # 生长锋周期 / 深度雾 vs 真实 z 跨度 / 三处引线落点的净空
        # —— qa 的 ⑳galaxy 逐条复算（半径除以 s 之后与 info P8 是同一批数）。
        _s = GX22["s"]
        a += [("lam", _n(_AS_LAM)), ("s", _n3(_s)), ("pts", str(_GX_N)),
              ("ring", "%d,%d,%d" % (_GX_CORE_N, _GX_IN_N, _GX_OUT_N)),
              ("r", ",".join(_n3(v * _s) for v in (_GX_CORE_R, _GX_IN_R0, _GX_IN_R1,
                                                   _GX_OUT_R0, _GX_OUT_R1))),
              ("thick", "%s,%s" % (_n3(_GX_IN_T * _s), _n3(_GX_OUT_T * _s))),
              ("tilt", _n3(_GX_TILT)), ("spin", _n3(_GX_SPINP)),
              ("sway", _n3(_GX_SWAY)), ("sway-p", _n3(_GX_SWAYP)),
              ("arcs", str(_GX_ARCS)), ("strands", str(_GX_SN)),
              ("flows", "%d,%d" % (_GX_SN_IN, _GX_SN_RAD)),
              ("cyc", _n3(_GX_CYC)),
              ("life", "%s,%s" % (_n3(_GX_LIFE_D), _n3(_GX_LIFE_B))),
              ("gs", _n3(_GX_GS)), ("floor", _n3(_GX_FLOOR)),
              ("qphase", ",".join(_n3(round((i * _GX_PL) % 1.0, 6)) for i in range(10))),
              ("half", _n3(_GX_HALF * _s)), ("zmax", _n3(round(_GX22_ZMAX, 2))),
              ("lead", ",".join(_n3(round(v, 2)) for v in _GX22_LEAD)),
              ("leadclr", _n3(_GX_LEADCLR))]
    if p in _ADD_PAGES:
        a += [("ink", ";".join("%d,%d,%d,%d" % b for b in _ADD_INK[p])),
              ("clr", _n(_ADD_CLR)), ("clr-min", _f1(_ADD_CLRMIN[p]))]
    elif p == 22:
        # 墨迹名册只给 P22 摊（P2 / P4 的名册留在构建期，页上 DOM 一个属性不许多）
        a += [("ink", ";".join("%d,%d,%d,%d" % tuple(round(v) for v in b)
                               for b in _P22INK)),
              ("clr", _n(_GX_LEADCLR)), ("clr-min", _f1(_P22CLRMIN))]
    return "".join(' data-lab-%s="%s"' % kv for kv in a + _spd_attr(p))


def lab_stage(p):
    """一页的 3D 舞台层：辉光（可选）+ poster（仅 P1/P21 有专用 svg）+ 打印帧位。
       **canvas 不在这里** —— 全 deck 只有一枚，常驻车库，翻页时搬进来。"""
    kind, rx, ry, rw, rh = (LAB_RECTS[p][0],) + LAB_RECTS[p][1:]
    atmo = poster = ""
    if kind == "voice":
        aw = VGR * 2 * 1.35
        atmo = ('<div class="lab-atmo" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;'
                'background:radial-gradient(circle closest-side,transparent 62%%,var(--v-atmo) 74%%,'
                'transparent 87%%);opacity:var(--v-atmo-int)"></div>'
                % (VCX - aw / 2, VCY - aw / 2, aw, aw))
        poster = ('<svg class="lab-poster" id="labPoster1" viewBox="0 0 1920 1080" aria-hidden="true">'
                  '<path class="v-wire-b" d="%s"/>'
                  '<path class="v-dot-b" d="%s"/>'
                  '<path class="v-wire" d="%s"/>'
                  '<path class="v-dot" d="%s"/>'
                  '<path class="v-dot-h" d="%s"/>'
                  '</svg>'
                  % (VPOSTER["wireB"], VPOSTER["back"], VPOSTER["wire"],
                     VPOSTER["front"], VPOSTER["hot"]))
    elif kind == "globe":
        aw = GGR * 2 * 1.35
        atmo = ('<div class="lab-atmo" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;'
                'background:radial-gradient(circle closest-side,transparent 62%%,var(--g-atmo) 74%%,'
                'transparent 87%%);opacity:var(--g-atmo-int)"></div>'
                % (GCX - aw / 2, GCY - aw / 2, aw, aw))
        poster = ('<svg class="lab-poster" id="labPoster21" viewBox="0 0 1920 1080" aria-hidden="true">'
                  '<circle class="g-ocean" cx="%s" cy="%s" r="%s"/>'
                  '<path class="g-grat" d="%s"/>'
                  '<path class="g-land" d="%s"/>'
                  '%s'
                  '<path class="g-node" d="%s"/>'
                  '<circle class="g-rim" cx="%s" cy="%s" r="%s"/>'
                  '</svg>'
                  % (_f1(GCX), _f1(GCY), _f1(GGR), GPOSTER["grat"], GPOSTER["land"],
                     "".join('<path class="g-arc" d="%s"/>' % d for d in GPOSTER["arcs"]),
                     GPOSTER["nodes"], _f1(GCX), _f1(GCY), _f1(GGR)))
    elif kind == "brain":
        # P17 的辉光是一枚横躺的椭圆（脑是横长的）：暗底上给整颗脑一圈自然的环境光。
        # 浅底几乎看不见（--b-atmo-int .045）—— 纸面上不该有光晕。
        atmo = ('<div class="lab-atmo" style="left:938px;top:544px;width:900px;height:620px;'
                'margin-left:-450px;margin-top:-310px;'
                'background:radial-gradient(closest-side,var(--b-atmo),transparent 72%);'
                'opacity:var(--b-atmo-int)"></div>')
    # ── 加法层四页（三轮）：**不挂 poster** ────────────────────────────────
    #    另外 16 页的 poster 是「3D 替换掉的那张图」，降级时它顶上来。这四页
    #    3D 没有替换任何东西（页上本来就没有图）—— 它们的降级层**就是整页本身**：
    #    卡片 / logo / 文案全在 .pp 里，WebGL 起不来时这一页与今天逐像素相同。
    #    挂一枚空 <svg class="lab-poster"> 只是骗闸门，所以这里一个字都不挂，
    #    改由 build() 的 ㉒ 闸与 qa 的 ⑲a/⑲c 正面断言「加法层页 poster 件数 = 0」。
    pr = ('<img class="lab-print" id="labPrint%d" alt="" aria-hidden="true" '
          'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (p, rx, ry, rw, rh))
    return ('<div class="lab-stage" id="labStage%d" data-lab-page="%d" data-lab-scene="%s" '
            'data-lab-rect="%d,%d,%d,%d"%s aria-hidden="true">%s%s%s</div>'
            % (p, p, kind, rx, ry, rw, rh, lab_data(p), atmo, poster, pr))


def lp(*parts):
    """poster 层包装：把一段**图形几何**裹进 <g class="lab-poster">。
       3D 起来（该页场景渲出第一帧）时它淡出、canvas 接管；WebGL 不可用 / 自动降级 /
       print / reduced-motion / 离线归档 ⇒ 它原样呈现，那一页仍是完整的 2D 版。
       ⚠ 只裹「形」，一个字也不裹 —— 标签 / 引线 / 图例 / 数字全部留在外面：
         canvas 坐在 .pp 之下，页上的字因此永远压在 3D 之上，任何路径下都在位。
       一页可以有多个 lab-poster 组（形与字本来就是交错画的），CSS 一并淡出。"""
    return '<g class="lab-poster">%s</g>' % "".join(parts)


# 结构标记：分步组的开闭标签是**骨架**，不能被裹进 poster 组（会裹出错配的嵌套）
_LPSTRUCT = ('<g data-step="1">', '</g>')


def _lpsplit(items, keep=()):
    """把一串 SVG 片段按「形 / 字」自动切开（第二波九页共用这一把刀）：
       连续的形裹进一个 <g class="lab-poster">，带字的片段原位留在外面 ——
       **顺序一个不换**，所以 DOM 文本序列与引擎母本逐字相同（build() 末尾会验）。
       判据只有一条：片段里出现 `<text` 就是「带字的」⇒ 留在 canvas 之上。
       于是 legend() / _anchor_chip() / step_badge() 这类「样线 + 标签」的注记件
       整件留在 DOM 里（图例与时序标号本来就不该被 3D 接管），
       swap_mark() 这类纯形小件照常进 poster。
       keep：额外强制留外的片段（本波暂时用不到，留作护栏）。"""
    out, buf = [], []
    for it in items:
        # 判据两条：① 片段里出现 `<text` 就是「带字的」；② `<polygon` 只有一处出处 ——
        # ah_*() 的箭头头。箭头是**方向标注**，投影锁又保证 3D 线的端点与页上逐像素同位，
        # 所以箭头留在 canvas 之上正好钉住每条 3D 线的流向（3D 里不再重画箭头）。
        if it in _LPSTRUCT or it in keep or "<text" in it or "<polygon" in it:
            if buf:
                out.append(lp(*buf)); buf = []
            out.append(it)
        else:
            buf.append(it)
    if buf:
        out.append(lp(*buf))
    return "".join(out)


# ═══════════════════════════════════════════════════════════════════════════
# 版式分歧名册（波B 新增 · **一处不多一处不少**）
# ───────────────────────────────────────────────────────────────────────────
#   LAB 演绎的定义是「只加 3D，正文一个字节没动」。但六处地方，几何**确实**与
#   引擎母本分了叉 —— 每一处都有非动不可的理由。与其让它们散在各页注释里，
#   不如**声明**成一张表：build() 末尾拿产物与母本逐页对几何 token，
#   实际分叉的页集合必须与这张表的 geom 行**完全相等**（多一页少一页都当场炸），
#   poster 行另有一条针对性的自证。
#   kind：geom = 页上几何 token 与母本不同｜poster = 几何一样、只是 lab-poster 分组不同
_DIVERGE = [
    (1,  "geom",   "封面加声场球 poster + kicker 末段「· LAB」（家族名，全 deck 唯一正文改动）"),
    (21, "geom",   "Why Agora 换盒子（SD-RTN 地球）+ 加「节点分布示意」角注"),
    (18, "geom",   "波A：双轴坐标**左移 80px**（终审「两张图偏挤」）+ 补回「真人销冠」基准虚线"),
    (18, "stage",  "波A：lab-stage 从 1240 扩到 1680 —— 舞台横跨两图（扩的是「区域」，字一格没动）"),
    (2,  "geom",   "波B：四卡四角 → 底排四栏（决策环 → 模态转换剧场；文案零改动、发射顺序对齐母本）"),
    (13, "poster", "波B：_slot() 改分件方式 ⇒ 模块板从 canvas 之上收进 lab-poster 组"
                   "（DOM 坐标一格没动，只是分组）"),
    (3,  "geom",   "表达力精进 ④：三张时序小图提亮加粗 —— 半双工三轮×24 → 两轮×44、"
                   "方向通道 2.5px 线 → 半宽 4.5 的带、重叠区与闸跟着入册"
                   "（图窗 135 / 卡高 386 / 其后所有 y 一格没动）"),
]


def lab_garage():
    """车库：单枚 canvas 的常驻位（页面上唯一一块 WebGL 画布）。
       无场景页 / 未起帧 / 已降级时它就停在这儿，屏外零成本。"""
    return ('<div class="lab-garage" id="labGarage" aria-hidden="true">'
            '<canvas class="lab-canvas" id="labGl" width="16" height="16"'
            ' data-lab-canvas="1" data-lab-mode="BOOT" data-lab-run="0"'
            ' data-lab-page="0" data-lab-scene="" aria-hidden="true"></canvas></div>')

# ── LAB 运行时（① classic 前奏 ② importmap ③ module 本体）────────────────────
#   ① 是 classic script：模块整条挂掉（离线归档里 three 拉不到就是这个情形）它也照跑，
#      6s 看门狗把七页钉死在 poster 上 —— 「起不来 = 一张静图」而不是「起不来 = 一块空白」。
#   ③ 是 module：importmap 指自托管路径，零外链。
LAB_PRELUDE = """<script>
/* LAB 前奏（classic · 模块挂了也照跑）：两枚开关 + poster 看门狗 */
(function(){
  var Q=new URLSearchParams(location.search);
  var L=window.__LAB={
    debug:Q.get('debug')==='1',
    /* ?lab=hold —— 关掉 FPS 自动降级。给两种人用：
       ① 讲者在弱机 / 远程桌面上宁可要「慢但活的形」，不要一张静帧；
       ② 截图与录屏管线（容器里 SwiftShader 只有个位数 fps，不给这条路，
          终审静帧永远拍到 poster）。生产默认**不带**它，降级照跑。 */
    hold:Q.get('lab')==='hold'
  };
  if(L.debug)document.documentElement.setAttribute('data-lab-debug','1');
  setTimeout(function(){
    var c=document.getElementById('labGl');
    if(!c||c.dataset.labMode!=='BOOT')return;
    c.dataset.labMode='POSTER';c.dataset.labRun='0';
    document.querySelectorAll('.lab-stage').forEach(function(s){s.classList.remove('gl-up');});
    document.documentElement.setAttribute('data-lab-poster','1');
  },6000);
})();
</script>
<div class="lab-probe" id="labProbe" aria-hidden="true"></div>
<script type="importmap">
{"imports":{"three":"/decks/assets/three/three.module.min.js"}}
</script>
"""

LAB_MODULE_BODY = r"""
import * as THREE from 'three';
import { OrbitControls } from '/decks/assets/three/OrbitControls.js';

const FLAGS = window.__LAB || { debug:false, hold:false };
const W = K.W, H = K.H;

/* ═══════════════════════════════════════════════════════════════════════════
   lab-kit ①：主题色桥 —— **JS 里一个色号都不写**，全部读 CSS 变量
   ═══════════════════════════════════════════════════════════════════════════ */
const _sw = document.createElement('span');
_sw.style.cssText = 'position:absolute;left:-9999px;top:0';
document.body.appendChild(_sw);
const _col = new THREE.Color();
function cssColor(n){
  // 让浏览器自己把 var() / color-mix() 归一成一个可解析的颜色再进 three。
  // 变量取不到时不兜色号（这一层禁止写死色号）—— 留空即继承 body 的 --ink。
  _sw.style.color = '';
  const v = getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  if (v) _sw.style.color = v;
  const m = getComputedStyle(_sw).color.match(/[\d.]+/g) || [128,128,128];
  return _col.setRGB(m[0]/255, m[1]/255, m[2]/255, THREE.SRGBColorSpace).clone();
}
function cssNum(n, d){
  const v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue(n));
  return isFinite(v) ? v : d;
}
function setBlend(m, add){
  const b = add >= .5 ? THREE.AdditiveBlending : THREE.NormalBlending;
  if (m.blending !== b){ m.blending = b; m.needsUpdate = true; }
}

/* ═══ lab-kit ②：缓动 / 判据 ═══════════════════════════════════════════════
   --ease-flow = cubic-bezier(.22,.9,.24,1) 的数值解：入场用它，
   与 CSS 里所有 flow 过渡同一条曲线（写死一个近似 cubic-out 会和页面其它入场脱拍）*/
function bezier(p1x,p1y,p2x,p2y){
  const ax=1-3*p2x+3*p1x, bx=3*p2x-6*p1x, cx=3*p1x;
  const ay=1-3*p2y+3*p1y, by=3*p2y-6*p1y, cy=3*p1y;
  const fx=(t)=>((ax*t+bx)*t+cx)*t, fy=(t)=>((ay*t+by)*t+cy)*t;
  const dx=(t)=>(3*ax*t+2*bx)*t+cx;
  return (x)=>{ let t=x;
    for(let i=0;i<6;i++){ const e=fx(t)-x, d=dx(t); if(Math.abs(e)<1e-5||d===0)break; t-=e/d; }
    return fy(Math.min(1,Math.max(0,t))); };
}
const easeFlow = bezier(.22,.9,.24,1);
const TAU = Math.PI*2;
/* C¹ 的 smoothstep：本 deck 所有「渐入渐出的剖面」共用它（幅度剖面禁止用硬分支） */
function sstep(a, b, x){ const t = Math.max(0, Math.min(1, (x-a)/(b-a||1e-6)));
                         return t*t*(3-2*t); }
/* C² 的 smootherstep（6t⁵−15t⁴+10t³）：一阶**与二阶**导数在两端都归零。
   波B 的 P2 四道相位边界全走它 —— 形变的速度与加速度都接得上，
   接头处那一记可察觉的「顿」（smoothstep 只保证一阶）就没有了。 */
function smoother(a, b, x){ const t = Math.max(0, Math.min(1, (x-a)/(b-a||1e-6)));
                            return t*t*t*(t*(t*6-15)+10); }
function webglOK(){
  try{ const c=document.createElement('canvas');
    return !!(c.getContext('webgl2')||c.getContext('webgl')||c.getContext('experimental-webgl'));
  }catch(e){ return false; }
}
/* 确定性随机（无随机源 ⇒ 两次加载逐点一致，poster 与 WebGL 也永远是同一批点） */
function h1(i,s){ const x=Math.sin((i+1)*s)*43758.5453; return x-Math.floor(x); }

/* ═══ lab-kit ③：折线工具 ═════════════════════════════════════════════════
   构建期把页上的 SVG 贝塞尔展平成折线发过来（lab_k() 里的几何串），这里复活。
   五枚新场景的每一根线、每一个落点都出自这些折线 —— 3D 不新造坐标。 */
function unpackPoly(s){
  const a=s.split(';'), f=new Float32Array(a.length*2);
  for(let i=0;i<a.length;i++){ const p=a[i].split(','); f[i*2]=+p[0]; f[i*2+1]=+p[1]; }
  return f;
}
function unpackMulti(s){ return s.split('|').map(unpackPoly); }
/* 折线**等弧长重采样**（波B 新增）：一条 mkStream 的 aG 是**逐顶点**属性 ——
   幅度剖面（ghost 窗口）能画多细，取决于这条折线有多少个采样点。
   6 个拐点的折线喂进去，ghost 窗口根本落不到点上（本轮实拍锤过一次）。 */
function resamplePoly(rows, n){
  const cum = [0];
  for(let i = 1; i < rows.length; i++)
    cum.push(cum[i-1] + Math.hypot(rows[i][0]-rows[i-1][0], rows[i][1]-rows[i-1][1]));
  const tot = cum[cum.length-1] || 1, out = [];
  let j = 0;
  for(let k = 0; k < n; k++){
    const d = tot*k/(n-1);
    while(j < cum.length-2 && cum[j+1] < d) j++;
    const t = (d - cum[j])/((cum[j+1]-cum[j]) || 1);
    out.push([rows[j][0] + (rows[j+1][0]-rows[j][0])*t,
              rows[j][1] + (rows[j+1][1]-rows[j][1])*t]);
  }
  return out;
}
function polyCum(p){
  const n=p.length/2, c=new Float32Array(n);
  for(let i=1;i<n;i++){ const dx=p[i*2]-p[i*2-2], dy=p[i*2+1]-p[i*2-1];
    c[i]=c[i-1]+Math.hypot(dx,dy); }
  return c;
}
function polyAt(p,c,t,out){
  const n=p.length/2, L=c[n-1]*Math.min(1,Math.max(0,t));
  let lo=0, hi=n-1;
  while(lo<hi-1){ const m=(lo+hi)>>1; if(c[m]<=L) lo=m; else hi=m; }
  const seg=c[hi]-c[lo] || 1, u=(L-c[lo])/seg;
  out[0]=p[lo*2]+(p[hi*2]-p[lo*2])*u;
  out[1]=p[lo*2+1]+(p[hi*2+1]-p[lo*2+1])*u;
  return out;
}
function insideMulti(polys,x,y){          // even-odd：04 区是个环（外圈减内圈）
  let inside=false;
  for(const p of polys){
    const n=p.length/2;
    for(let i=0,j=n-1;i<n;j=i++){
      const xi=p[i*2],yi=p[i*2+1],xj=p[j*2],yj=p[j*2+1];
      if(((yi>y)!==(yj>y)) && (x < (xj-xi)*(y-yi)/((yj-yi)||1e-9)+xi)) inside=!inside;
    }
  }
  return inside;
}
function distToPoly(p,x,y){
  const n=p.length/2; let best=1e9;
  for(let i=0;i<n-1;i++){
    const ax=p[i*2],ay=p[i*2+1],bx=p[i*2+2],by=p[i*2+3];
    const dx=bx-ax,dy=by-ay, L=dx*dx+dy*dy;
    let t = L>0 ? ((x-ax)*dx+(y-ay)*dy)/L : 0;
    t = t<0?0:(t>1?1:t);
    const qx=ax+dx*t-x, qy=ay+dy*t-y, d=qx*qx+qy*qy;
    if(d<best) best=d;
  }
  return Math.sqrt(best);
}

/* ═══ lab-kit ④：px 场景的通用着色器件 ════════════════════════════════════
   五枚新场景全部工作在**该页 figbox 的 viewBox 坐标**里：相机架成
   「z=0 平面上 1 世界单位 = 1 屏幕像素」，于是页上 SVG 的每个坐标可以直接搬进
   3D，3D 形与它替换掉的 2D 形逐像素同位。深度（z）自然产生透视。
   y 轴取负（SVG 向下为正，three 向上为正）。 */
function camPx(w,h,D){
  const fov = 2*Math.atan((h/2)/D)*180/Math.PI;
  const cam = new THREE.PerspectiveCamera(fov, w/h, D*0.02, D*4);
  cam.position.set(w/2, -h/2, D); cam.lookAt(w/2, -h/2, 0);
  return cam;
}
/* 球面场景（P1/P21）：FOV 由 rect 高度反解，使投影尺度与 poster 的离线相机**逐参相同**
   —— poster 与 WebGL 因此是同一张图，交接时不会「跳一下大小」。 */
function camSphere(w,h,C){
  const fov = 2*Math.atan((h/2)/K.FPX)*180/Math.PI;
  const cam = new THREE.PerspectiveCamera(fov, w/h, 0.1, 200);
  cam.position.set(C[0],C[1],C[2]); cam.lookAt(0,0,0);
  return cam;
}
/* px 点云：uSize 是**屏幕像素直径**；深度雾 uNear/uFar 给体积感；
   aA = 逐点 alpha 权重，aH = 逐点热度（0..1，进 mix(uColor,uHot,·)）。 */
const PX_HEAD = [
  'uniform float uIntro,uTime,uSize,uD,uPx,uNear,uFar;',
  'attribute float aA; attribute float aH;',
  'varying float vFade,vA,vH;',
  'vec4 pxCore(vec3 p,float sz){',
  '  vec4 mv=modelViewMatrix*vec4(p,1.0);',
  '  float z=max(-mv.z,1.0);',
  '  vFade=clamp((uFar-z)/(uFar-uNear),0.0,1.0);',
  '  gl_PointSize=max(sz*uPx*uD/z,0.55);',
  '  return mv;}',
].join('\n');
const PX_PT_FS = [
  'uniform vec3 uColor,uHot; uniform float uOpacity,uBack,uGain,uSoft;',
  'varying float vFade,vA,vH;',
  'void main(){',
  '  vec2 c=gl_PointCoord-0.5; float d=dot(c,c);',
  '  if(d>0.25) discard;',
  '  float a=uOpacity*vA*mix(uBack,1.0,vFade)*smoothstep(0.25,uSoft,d)*(1.0+uGain*vH);',
  '  if(a<0.004) discard;',
  '  gl_FragColor=vec4(mix(uColor,uHot,clamp(vH,0.0,1.0)),clamp(a,0.0,1.0));',
  '  #include <colorspace_fragment>',
  '}',
].join('\n');
const PX_LN_FS = [
  'uniform vec3 uColor,uHot; uniform float uOpacity,uBack,uGain;',
  'varying float vFade,vA,vH;',
  'void main(){',
  '  float a=uOpacity*vA*mix(uBack,1.0,vFade)*(1.0+uGain*vH);',
  '  if(a<0.004) discard;',
  '  gl_FragColor=vec4(mix(uColor,uHot,clamp(vH,0.0,1.0)),clamp(a,0.0,1.0));',
  '  #include <colorspace_fragment>',
  '}',
].join('\n');
/* 一枚场景的共享 uniform（入场 t / 钟 / DPR / 深度雾）：材质各自克隆自己的颜色档，
   但这几枚永远共用同一个对象 ⇒ 一处更新，全场景同步。 */
function pxShared(D, half){
  // uNear/uFar 必须**贴着该场景的真实深度范围**收紧 —— 松了就等于没有体积：
  // 深度雾是 px 场景里唯一的立体线索（没有光照、没有阴影，只有远近的明暗）。
  const h = half || D*0.2;
  return { uIntro:{value:0}, uTime:{value:0}, uD:{value:D}, uPx:{value:1},
           uNear:{value:D-h}, uFar:{value:D+h} };
}
function mkMat(shared, vs, fs, extra){
  const u = Object.assign({}, shared, {
    uSize:{value:2}, uSoft:{value:.06}, uColor:{value:new THREE.Color()},
    uHot:{value:new THREE.Color()}, uOpacity:{value:1}, uBack:{value:.34},
    uGain:{value:1} }, extra||{});
  return new THREE.ShaderMaterial({ uniforms:u, vertexShader:vs, fragmentShader:fs,
                                    transparent:true, depthWrite:false });
}
const PX_PT_VS = PX_HEAD + [
  'void main(){ vA=aA; vH=aH;',
  '  vec4 mv=pxCore(position,uSize);',
  '  gl_Position=projectionMatrix*mv; }'].join('\n');
const PX_LN_VS = PX_HEAD + [
  'void main(){ vA=aA; vH=aH;',
  '  vec4 mv=pxCore(position,1.0);',
  '  gl_Position=projectionMatrix*mv; }'].join('\n');
/* 流带（三角带）：aT 是沿带的参数 —— 入场按 t 「长出来」，流动感也挂在它上面 */
const PX_RB_VS = [
  'uniform float uIntro,uTime,uNear,uFar;',
  'attribute float aT; attribute float aA; attribute float aH;',
  'varying float vT,vA,vH,vFade;',
  'void main(){ vT=aT; vA=aA; vH=aH;',
  '  vec4 mv=modelViewMatrix*vec4(position,1.0);',
  '  float z=max(-mv.z,1.0);',
  '  vFade=clamp((uFar-z)/(uFar-uNear),0.0,1.0);',
  '  gl_Position=projectionMatrix*mv; }'].join('\n');
const PX_RB_FS = [
  'uniform vec3 uColor,uHot; uniform float uOpacity,uBack,uGain,uIntro,uTime,uFlow;',
  'varying float vT,vA,vH,vFade;',
  'void main(){',
  '  float grow=clamp((uIntro*1.15-vT)/0.10,0.0,1.0);',
  '  float flow=0.74+0.26*sin((vT*uFlow-uTime*1.7)*6.2831853);',
  '  float a=uOpacity*vA*mix(uBack,1.0,vFade)*grow*flow*(1.0+uGain*vH);',
  '  if(a<0.004) discard;',
  '  gl_FragColor=vec4(mix(uColor,uHot,clamp(vH,0.0,1.0)),clamp(a,0.0,1.0));',
  '  #include <colorspace_fragment>',
  '}'].join('\n');
/* 逐点属性小工具：aA / aH 两条，所有 px 场景共用 */
function attrAH(geo,n,a0,h0){
  const a=new Float32Array(n), h=new Float32Array(n);
  a.fill(a0===undefined?1:a0); h.fill(h0||0);
  geo.setAttribute('aA', new THREE.BufferAttribute(a,1));
  geo.setAttribute('aH', new THREE.BufferAttribute(h,1));
  return {a,h};
}
/* 流带 ribbon：给一条中心折线 + 半宽函数，织出一条三角带（TubeGeometry 的扁平版）。
   用在 P18 复利螺旋与 P4 双向声带上 —— 两页的「带」是同一个件。 */
function ribbonGeo(pts, halfW, uv, dirs){
  const n = pts.length, pos = new Float32Array(n*2*3), tt = new Float32Array(n*2);
  for(let i=0;i<n;i++){
    const p = pts[i], q = pts[Math.min(n-1,i+1)], r = pts[Math.max(0,i-1)];
    let tx=q[0]-r[0], ty=q[1]-r[1], tz=q[2]-r[2];
    const tl=Math.hypot(tx,ty,tz)||1; tx/=tl; ty/=tl; tz/=tl;
    // 默认：带面法向 = 切线 × 视线(0,0,1) ⇒ 带子始终把宽面朝向观众（P4 的声带要这个）。
    // 传了 dirs 就用它：P18 的复利螺旋要的是**径向**展宽 —— 带面随着绕轴转，
    // 转到贴屏时露出整幅、转到入深时收成一条线，「这是一圈一圈绕上去的」才看得出来。
    let nx, ny, nz;
    if(dirs){ nx=dirs[i][0]; ny=dirs[i][1]; nz=dirs[i][2]; }
    else { nx=ty; ny=-tx; nz=0; }
    let nl=Math.hypot(nx,ny,nz); if(nl<1e-5){ nx=0;ny=1;nz=0;nl=1; }
    nx/=nl; ny/=nl; nz/=nl;
    const w = halfW(i/(n-1));
    pos[i*6]=p[0]+nx*w; pos[i*6+1]=p[1]+ny*w; pos[i*6+2]=p[2]+nz*w;
    pos[i*6+3]=p[0]-nx*w; pos[i*6+4]=p[1]-ny*w; pos[i*6+5]=p[2]-nz*w;
    tt[i*2]=tt[i*2+1]=uv?uv(i/(n-1)):i/(n-1);
  }
  const idx = [];
  for(let i=0;i<n-1;i++){ const a=i*2; idx.push(a,a+1,a+2, a+1,a+3,a+2); }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos,3));
  g.setAttribute('aT', new THREE.BufferAttribute(tt,1));
  g.setIndex(idx);
  return g;
}

/* ═══════════════════════════════════════════════════════════════════════════
   场景 registry · ① 声场球（P1 封面）
   ───────────────────────────────────────────────────────────────────────────
   语义：球面点云沿**法线**呼吸，位移由三枚谐波叠加出的伪音频包络驱动 ——
   「对话的声波」。波数 k 让包络沿 y 轴成行波 ⇒ 看见的是**横跨球面的波带**，
   不是整颗球一起胀缩（那是气球，不是声场）。波峰处点色 mix 向 accent，
   于是「声音走到哪里」在球面上直接看得见。
   克制三条：自转 96s/圈（比地球还慢）· 振幅 7%（球径量级的呼吸，不是抖动）·
   **不给 OrbitControls**（封面是观赏层，一拖就抢主标）。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeVoice(ctx){
  const V = K.v, w = ctx.rect[2], h = ctx.rect[3];
  const scene = new THREE.Scene();
  const camera = camSphere(w, h, V.cam);
  const pivot = new THREE.Group(); pivot.rotation.z = V.tilt; scene.add(pivot);
  const spin  = new THREE.Group(); pivot.add(spin);

  const U = {
    uTime:{value:0}, uIntro:{value:0}, uScale:{value:1},
    uAmp:{value:V.amp}, uW0:{value:V.w0},
    uHA:{value:new THREE.Vector3(V.ha[0],V.ha[1],V.ha[2])},
    uHW:{value:new THREE.Vector3(V.hw[0],V.hw[1],V.hw[2])},
    uHK:{value:new THREE.Vector3(V.hk[0],V.hk[1],V.hk[2])},
    uHP:{value:new THREE.Vector3(V.hp[0],V.hp[1],V.hp[2])},
    uBack:{value:.24}, uHot0:{value:V.hot[0]}, uHot1:{value:V.hot[1]},
  };
  const HEAD = [
    'uniform float uTime,uIntro,uAmp,uW0,uBack;',
    'uniform vec3 uHA,uHW,uHK,uHP;',
    'varying float vFade; varying float vW;',
    'float labWave(float y){',
    '  return uHA.x*sin(uHW.x*uW0*uTime+uHK.x*y+uHP.x)',
    '       + uHA.y*sin(uHW.y*uW0*uTime+uHK.y*y+uHP.y)',
    '       + uHA.z*sin(uHW.z*uW0*uTime+uHK.z*y+uHP.z);}',
    'vec4 labMV(){',
    '  float w=labWave(position.y); vW=w;',
    '  vec3 p=position*(1.0+uAmp*w)*uIntro;',
    '  vec4 mv=modelViewMatrix*vec4(p,1.0);',
    '  vec3 n=normalize(mat3(modelViewMatrix)*normalize(position));',
    '  float facing=dot(n,normalize(-mv.xyz));',
    '  vFade=mix(uBack,1.0,smoothstep(-0.20,0.55,facing));',
    '  return mv;}',
  ].join('\n');
  const PT_VS = HEAD + [
    'uniform float uScale,uSize,uMinPx;',
    'void main(){ vec4 mv=labMV();',
    '  gl_Position=projectionMatrix*mv;',
    '  gl_PointSize=max(uSize*uScale*uIntro/max(-mv.z,0.001),uMinPx*uIntro); }',
  ].join('\n');
  const PT_FS = [
    'uniform vec3 uColor,uHot; uniform float uOpacity,uSoft,uHot0,uHot1,uHotGain;',
    'varying float vFade; varying float vW;',
    'void main(){',
    '  vec2 c=gl_PointCoord-0.5; float d=dot(c,c);',
    '  if(d>0.25) discard;',
    '  float h=smoothstep(uHot0,uHot1,vW);',
    // 波峰不只换色，还抬一档 alpha —— 「声音走到哪里，哪里亮」才是这颗球的语义
    '  float a=clamp(uOpacity*(1.0+uHotGain*h),0.0,1.0)*vFade*smoothstep(0.25,uSoft,d);',
    '  if(a<0.004) discard;',
    '  gl_FragColor=vec4(mix(uColor,uHot,h),a);',
    '  #include <colorspace_fragment>',
    '}',
  ].join('\n');
  const LN_VS = HEAD + 'void main(){ gl_Position=projectionMatrix*labMV(); }';
  const LN_FS = [
    'uniform vec3 uColor,uHot; uniform float uOpacity,uHot0,uHot1,uHotGain;',
    'varying float vFade; varying float vW;',
    'void main(){',
    '  float h=smoothstep(uHot0,uHot1,vW);',
    '  gl_FragColor=vec4(mix(uColor,uHot,h),clamp(uOpacity*(1.0+uHotGain*h),0.0,1.0)*vFade);',
    '  #include <colorspace_fragment>',
    '}',
  ].join('\n');

  const dotMat = new THREE.ShaderMaterial({
    uniforms: Object.assign({}, U, {
      uSize:{value:.005}, uMinPx:{value:1.05}, uSoft:{value:.13}, uHotGain:{value:.4},
      uOpacity:{value:.8}, uColor:{value:new THREE.Color()}, uHot:{value:new THREE.Color()} }),
    vertexShader:PT_VS, fragmentShader:PT_FS, transparent:true, depthWrite:false,
  });
  const wireMat = new THREE.ShaderMaterial({
    uniforms: Object.assign({}, U, {
      uOpacity:{value:.16}, uHotGain:{value:.4},
      uColor:{value:new THREE.Color()}, uHot:{value:new THREE.Color()} }),
    vertexShader:LN_VS, fragmentShader:LN_FS, transparent:true, depthWrite:false,
  });

  // 点云：Fibonacci 球面点阵（与 poster 逐字同式 —— 降级层与运行时是同一批点）
  const N = V.n, GA = Math.PI*(3-Math.sqrt(5)), JIT = 0.35*Math.sqrt(4*Math.PI/N);
  const pos = new Float32Array(N*3);
  const _p=new THREE.Vector3(),_t1=new THREE.Vector3(),_t2=new THREE.Vector3(),_ax=new THREE.Vector3();
  for(let i=0;i<N;i++){
    const y = 1-(2*(i+0.5))/N, r = Math.sqrt(Math.max(0,1-y*y)), th = i*GA;
    _p.set(Math.cos(th)*r, y, Math.sin(th)*r);
    // 确定性抖动：打散黄金角螺旋的机制网格感（与地球陆地点、与 poster 逐字同式）
    const a1=Math.sin((i+1)*12.9898)*43758.5453, j1=a1-Math.floor(a1)-0.5;
    const a2=Math.sin((i+1)*78.233)*24634.6345,  j2=a2-Math.floor(a2)-0.5;
    _ax.set(0,1,0); if(Math.abs(_p.y)>0.95)_ax.set(1,0,0);
    _t1.crossVectors(_p,_ax).normalize(); _t2.crossVectors(_p,_t1);
    _p.addScaledVector(_t1,JIT*j1).addScaledVector(_t2,JIT*j2).normalize();
    pos[i*3]=_p.x; pos[i*3+1]=_p.y; pos[i*3+2]=_p.z;
  }
  const dotGeo = new THREE.BufferGeometry();
  dotGeo.setAttribute('position', new THREE.BufferAttribute(pos,3));
  dotGeo.computeBoundingSphere(); dotGeo.boundingSphere.radius = 1.2;
  const dots = new THREE.Points(dotGeo, dotMat); dots.frustumCulled=false; spin.add(dots);

  // 线框：12 条经线 + 5 条纬线（与 poster 同一组采样 —— 两条路一张图）
  const ll = (lat,lon)=>{ const p=lat*Math.PI/180,l=lon*Math.PI/180,c=Math.cos(p);
    return new THREE.Vector3(c*Math.sin(l), Math.sin(p), c*Math.cos(l)); };
  const wp = [];
  for(let lon=-180;lon<180;lon+=30){ let prev=null;
    for(let lat=-88;lat<=88;lat+=3){ const v=ll(lat,lon); if(prev)wp.push(prev,v); prev=v; } }
  for(const lat of [-60,-30,0,30,60]){ let prev=null;
    for(let lon=-180;lon<=180;lon+=3){ const v=ll(lat,lon); if(prev)wp.push(prev,v); prev=v; } }
  const wire = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(wp), wireMat);
  wire.frustumCulled=false; spin.add(wire);

  const SPIN_W = (Math.PI*2)/V.spin;
  return {
    scene, camera, intro:V.introSec, grab:false,
    onDPR(pr){ U.uScale.value = K.FPX*pr; },
    setIntro(e){ U.uIntro.value = e; },
    draw(dt, clock){ U.uTime.value = clock; spin.rotation.y += dt*SPIN_W; },
    applyTheme(){
      U.uBack.value = cssNum('--v-back',.24);
      U.uHot0.value = cssNum('--v-hot0',.30);
      U.uHot1.value = cssNum('--v-hot1',.92);
      dotMat.uniforms.uColor.value.copy(cssColor('--v-ink'));
      dotMat.uniforms.uHot.value.copy(cssColor('--v-hot'));
      dotMat.uniforms.uOpacity.value = cssNum('--v-dot-op',.8);
      dotMat.uniforms.uSize.value = cssNum('--v-dot-size',.005);
      dotMat.uniforms.uMinPx.value = cssNum('--v-dot-min',1.05);
      dotMat.uniforms.uHotGain.value = cssNum('--v-hot-gain',.4);
      wireMat.uniforms.uHotGain.value = cssNum('--v-hot-gain',.4);
      wireMat.uniforms.uColor.value.copy(cssColor('--v-wire'));
      wireMat.uniforms.uHot.value.copy(cssColor('--v-hot'));
      wireMat.uniforms.uOpacity.value = cssNum('--v-wire-op',.16);
      setBlend(dotMat, cssNum('--v-add',0));
      setBlend(wireMat, cssNum('--v-add',0));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ② SD-RTN 地球（P21 Why Agora）
   实现整体移植自 /lab-globe（位掩码陆地 / 示意节点 / 五槽并发大圆弧 / 双主题材质）。
   弧**不标任何延迟数值**（数字红线）；节点是示意分布，页脚角注写死了这一条。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeGlobe(ctx){
  const G = K.g, w = ctx.rect[2], h = ctx.rect[3];
  const scene = new THREE.Scene();
  const camera = camSphere(w, h, G.cam);

  const U = { uScale:{value:1}, uTime:{value:0}, uIntro:{value:0} };
  const pivot = new THREE.Group(); pivot.rotation.z = G.tilt; scene.add(pivot);
  const spin  = new THREE.Group(); spin.rotation.y = G.y0; pivot.add(spin);

  /* ── ① 海球（遮挡体 + fresnel 塑形）── */
  const oceanU = { uBase:{value:new THREE.Color()}, uRim:{value:new THREE.Color()},
                   uRimInt:{value:.5}, uRimPow:{value:3}, uShade:{value:.3} };
  const ocean = new THREE.Mesh(new THREE.SphereGeometry(0.995,72,48), new THREE.ShaderMaterial({
    uniforms: oceanU,
    vertexShader:[
      'varying vec3 vN; varying vec3 vP;',
      'void main(){ vN=normalize(normalMatrix*normal);',
      '  vec4 mv=modelViewMatrix*vec4(position,1.0); vP=mv.xyz;',
      '  gl_Position=projectionMatrix*mv; }'].join('\n'),
    fragmentShader:[
      'uniform vec3 uBase; uniform vec3 uRim;',
      'uniform float uRimInt; uniform float uRimPow; uniform float uShade;',
      'varying vec3 vN; varying vec3 vP;',
      'const vec3 L=vec3(-0.42,0.50,0.76);',   // 视空间定光：球转、光不转，晨昏线不飘
      'void main(){',
      '  vec3 n=normalize(vN), v=normalize(-vP);',
      '  float f=pow(clamp(1.0-max(dot(n,v),0.0),0.0,1.0),uRimPow);',
      '  float d=max(dot(n,normalize(L)),0.0);',
      '  vec3 c=uBase*(1.0-uShade+uShade*(0.30+0.70*d));',
      '  c+=uRim*(f*uRimInt);',
      '  gl_FragColor=vec4(c,1.0);',
      '  #include <colorspace_fragment>',
      '}'].join('\n'),
  }));
  spin.add(ocean);

  /* ── ② 经纬网（30° 一格，很淡，只做「这是地图」的暗示）── */
  const gratMat = new THREE.LineBasicMaterial({transparent:true, depthWrite:false});
  const gratPts = [];
  const ll2v = (lat,lon,r)=>{ const p=lat*Math.PI/180,l=lon*Math.PI/180,c=Math.cos(p);
    return new THREE.Vector3(c*Math.sin(l)*r, Math.sin(p)*r, c*Math.cos(l)*r); };
  for(let lon=-180;lon<180;lon+=30){ let prev=null;
    for(let lat=-88;lat<=88;lat+=4){ const v=ll2v(lat,lon,1.001); if(prev)gratPts.push(prev,v); prev=v; } }
  for(let lat=-60;lat<=60;lat+=30){ let prev=null;
    for(let lon=-180;lon<=180;lon+=4){ const v=ll2v(lat,lon,1.001); if(prev)gratPts.push(prev,v); prev=v; } }
  const grat = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(gratPts), gratMat);
  spin.add(grat);

  /* ── ③ 陆地点云：位掩码只回答第 i 个候选点「是不是陆地」—— 数据里没有一个坐标 ── */
  const bin = atob(K.landBits);
  const GA = Math.PI*(3-Math.sqrt(5));
  const JIT = 0.35*Math.sqrt(4*Math.PI/K.landN);
  const lp = [];
  const _p=new THREE.Vector3(),_t1=new THREE.Vector3(),_t2=new THREE.Vector3(),_ax=new THREE.Vector3();
  for(let i=0;i<K.landN;i++){
    if(!(bin.charCodeAt(i>>3)&(1<<(i&7))))continue;
    const y=1-(2*(i+0.5))/K.landN, r=Math.sqrt(Math.max(0,1-y*y)), th=i*GA;
    _p.set(Math.cos(th)*r,y,Math.sin(th)*r);
    const a1=Math.sin((i+1)*12.9898)*43758.5453, j1=a1-Math.floor(a1)-0.5;
    const a2=Math.sin((i+1)*78.233)*24634.6345,  j2=a2-Math.floor(a2)-0.5;
    _ax.set(0,1,0); if(Math.abs(_p.y)>0.95)_ax.set(1,0,0);
    _t1.crossVectors(_p,_ax).normalize(); _t2.crossVectors(_p,_t1);
    _p.addScaledVector(_t1,JIT*j1).addScaledVector(_t2,JIT*j2).normalize().multiplyScalar(1.004);
    lp.push(_p.x,_p.y,_p.z);
  }
  const LAND_COUNT = lp.length/3;

  /* 共用的「球面发光点」着色器：圆点 + 边缘淡出 + 受光 + 逐点相位脉冲 + 入场 t */
  const POINT_VS = [
    'uniform float uScale; uniform float uSize; uniform float uMinPx;',
    'uniform float uTime; uniform float uPulse; uniform float uLit; uniform float uIntro;',
    'attribute float aPhase; attribute float aAlpha;',
    'varying float vFade; varying float vA;',
    'const vec3 L=vec3(-0.42,0.50,0.76);',
    'void main(){',
    '  vec4 mv=modelViewMatrix*vec4(position,1.0);',
    '  vec3 n=normalize(mat3(modelViewMatrix)*normalize(position));',
    '  vec3 v=normalize(-mv.xyz);',
    '  float facing=max(dot(n,v),0.0);',
    '  float lit=mix(1.0-uLit,1.0,max(dot(n,normalize(L)),0.0));',
    '  float pulse=1.0+uPulse*sin(uTime*1.7+aPhase);',
    '  vFade=smoothstep(0.0,0.34,facing)*lit;',
    '  vA=aAlpha;',
    '  gl_Position=projectionMatrix*mv;',
    '  gl_PointSize=max(uSize*pulse*uScale*uIntro/max(-mv.z,0.001),uMinPx*uIntro);',
    '}'].join('\n');
  const POINT_FS = [
    'uniform vec3 uColor; uniform float uOpacity; uniform float uSoft;',
    'varying float vFade; varying float vA;',
    'void main(){',
    '  vec2 c=gl_PointCoord-0.5; float d=dot(c,c);',
    '  if(d>0.25) discard;',
    '  float a=uOpacity*vFade*vA*smoothstep(0.25,uSoft,d);',
    '  if(a<0.004) discard;',
    '  gl_FragColor=vec4(uColor,a);',
    '  #include <colorspace_fragment>',
    '}'].join('\n');
  function pointMat(minPx, soft, blend){
    return new THREE.ShaderMaterial({
      uniforms:{ uScale:U.uScale, uTime:U.uTime, uIntro:U.uIntro,
        uSize:{value:.004}, uMinPx:{value:minPx}, uColor:{value:new THREE.Color()},
        uOpacity:{value:1}, uSoft:{value:soft}, uPulse:{value:0}, uLit:{value:0} },
      vertexShader:POINT_VS, fragmentShader:POINT_FS,
      transparent:true, depthWrite:false, blending:blend||THREE.NormalBlending,
    });
  }
  function attachAttrs(geo, count, phased){
    const ph=new Float32Array(count), al=new Float32Array(count);
    for(let i=0;i<count;i++){ ph[i]=phased?(i*2.399963)%6.2831853:0; al[i]=1; }
    geo.setAttribute('aPhase', new THREE.BufferAttribute(ph,1));
    geo.setAttribute('aAlpha', new THREE.BufferAttribute(al,1));
    return al;
  }
  const landGeo = new THREE.BufferGeometry();
  landGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(lp),3));
  attachAttrs(landGeo, LAND_COUNT, false);
  const landMat = pointMat(1.05,.13);
  const landPts = new THREE.Points(landGeo, landMat); landPts.frustumCulled=false; spin.add(landPts);

  /* ── ④ 节点（示意分布）+ 光晕 ── */
  const nodeLL = K.nodeTable.split(';').map(s=>s.split(',').map(Number));
  const NODE_COUNT = nodeLL.length;
  const npos = new Float32Array(NODE_COUNT*3);
  const nvec = [];
  nodeLL.forEach((l,i)=>{ const v=ll2v(l[0],l[1],1.013);
    npos[i*3]=v.x; npos[i*3+1]=v.y; npos[i*3+2]=v.z; nvec.push(ll2v(l[0],l[1],1)); });
  const nodeGeo = new THREE.BufferGeometry();
  nodeGeo.setAttribute('position', new THREE.BufferAttribute(npos,3));
  const nodeAlpha = attachAttrs(nodeGeo, NODE_COUNT, true);
  const nodeMat = pointMat(1.7,.14);
  const haloGeo = new THREE.BufferGeometry();
  haloGeo.setAttribute('position', new THREE.BufferAttribute(npos,3));
  const haloAlpha = attachAttrs(haloGeo, NODE_COUNT, true);
  const haloMat = pointMat(3,.0,THREE.AdditiveBlending);
  const haloPts = new THREE.Points(haloGeo,haloMat); haloPts.frustumCulled=false; spin.add(haloPts);
  const nodePts = new THREE.Points(nodeGeo,nodeMat); nodePts.frustumCulled=false; spin.add(nodePts);

  /* ── ⑤ 飞包：五槽并发大圆弧 + 沿弧飞行的小光点 ── */
  const routes = K.routeTable.split(';').map(s=>s.split(',').map(Number));
  const ARC_DUR=K.arcDur, ARC_GAP=K.arcGap, ARC_OFF=K.arcOff, SEG=128;
  const arcMat = new THREE.LineBasicMaterial({transparent:true, depthWrite:false});
  const slots = [];
  for(let s=0;s<ARC_DUR.length;s++){
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array((SEG+1)*3),3));
    const m=arcMat.clone();
    const line=new THREE.Line(g,m); line.frustumCulled=false; spin.add(line);
    slots.push({g,m,line,route:s%routes.length,pts:new Float32Array((SEG+1)*3),cycle:-1,baseOp:.7});
  }
  const headGeo = new THREE.BufferGeometry();
  headGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(slots.length*3),3));
  const headAlpha = attachAttrs(headGeo, slots.length, false);
  const headMat = pointMat(2.2,.05,THREE.AdditiveBlending);
  const heads = new THREE.Points(headGeo, headMat); heads.frustumCulled=false; spin.add(heads);

  const _a=new THREE.Vector3(),_b=new THREE.Vector3(),_q=new THREE.Vector3();
  function buildArc(slot){
    const ia=routes[slot.route][0], ib=routes[slot.route][1];
    _a.copy(nvec[ia]); _b.copy(nvec[ib]);
    const om=Math.acos(Math.max(-1,Math.min(1,_a.dot(_b)))), so=Math.sin(om);
    const lift=0.028+0.215*(om/Math.PI);
    for(let i=0;i<=SEG;i++){
      const t=i/SEG;
      if(so<1e-6) _q.copy(_a);
      else _q.set(0,0,0).addScaledVector(_a,Math.sin((1-t)*om)/so).addScaledVector(_b,Math.sin(t*om)/so);
      _q.normalize().multiplyScalar(1+lift*Math.sin(Math.PI*t));
      slot.pts[i*3]=_q.x; slot.pts[i*3+1]=_q.y; slot.pts[i*3+2]=_q.z;
    }
    slot.g.attributes.position.array.set(slot.pts);
    slot.g.attributes.position.needsUpdate=true;
    slot.g.computeBoundingSphere();
    slot.dest=ib;
  }
  slots.forEach(buildArc);
  const pulseAmt = new Float32Array(NODE_COUNT);

  function stepSlot(slot,i,t){
    const period=ARC_DUR[i]+ARC_GAP[i];
    let tl=(t-ARC_OFF[i])%period; if(tl<0)tl+=period;
    const cyc=Math.floor((t-ARC_OFF[i])/period);
    if(cyc!==slot.cycle){                       // 换一条取道
      slot.cycle=cyc;
      slot.route=(((cyc*slots.length+i)%routes.length)+routes.length)%routes.length;
      buildArc(slot); slot.pinged=false;
    }
    if(tl>=ARC_DUR[i]){ slot.line.visible=false; headAlpha[i]=0; return; }
    const u=tl/ARC_DUR[i];
    const head=Math.min(1,u/0.62), tail=Math.max(0,(u-0.38)/0.62);
    const i0=Math.floor(tail*SEG), i1=Math.ceil(head*SEG);
    const cnt=Math.max(2,i1-i0+1);
    slot.line.visible=true;
    slot.g.setDrawRange(i0,Math.min(cnt,SEG+1-i0));
    const env=Math.min(1,u/0.06)*Math.min(1,(1-u)/0.12);
    slot.m.opacity=slot.baseOp*env*arcGate;
    if(head<1){
      const hi=Math.min(SEG,Math.round(head*SEG));
      const hp=headGeo.attributes.position.array;
      hp[i*3]=slot.pts[hi*3]; hp[i*3+1]=slot.pts[hi*3+1]; hp[i*3+2]=slot.pts[hi*3+2];
      headAlpha[i]=env*arcGate;
    }else{
      headAlpha[i]=0;
      if(!slot.pinged){ slot.pinged=true; pulseAmt[slot.dest]=1; }
    }
  }

  /* ── 交互：可拖，**禁 zoom**（半屏构图里一放大就顶出版心）；触摸留给 deck 翻页 ── */
  const controls = new OrbitControls(camera, ctx.canvas);
  controls.enableDamping=true; controls.dampingFactor=.065;
  controls.enablePan=false; controls.rotateSpeed=.42;
  controls.enableZoom=false;
  controls.minPolarAngle=.16; controls.maxPolarAngle=Math.PI-.16;
  controls.touches={ONE:null,TWO:null};     // 一指滑动归 deck.js 翻页，别跟讲者抢
  controls.enabled=false;                   // 只有本页在台上时才接管指针
  let dragT=-1e9, clockRef=0;
  controls.addEventListener('start',()=>{dragT=1e9;});
  controls.addEventListener('end',()=>{dragT=clockRef;});

  let arcGate = 0;
  const SPIN_W = (Math.PI*2)/G.spin;
  return {
    scene, camera, intro:G.introSec, grab:true, controls,
    onDPR(pr){ U.uScale.value = K.FPX*pr; },
    setIntro(e){
      U.uIntro.value = e;
      ocean.scale.setScalar(Math.max(1e-3,e));
      grat.scale.setScalar(Math.max(1e-3,e));
      // 弧最后进场：球还没落位就有包在飞，读起来像「先有路后有网」
      arcGate = e < .82 ? 0 : (e-.82)/.18;
    },
    draw(dt, clock){
      clockRef = clock;
      U.uTime.value = clock;
      // 拖拽时停转，松手 2.4s 后缓入恢复（不跟用户抢方向盘）
      let spinK=1; const since=clock-dragT;
      if(since<0) spinK=0; else if(since<2.4) spinK=0; else if(since<4.0) spinK=(since-2.4)/1.6;
      spin.rotation.y += dt*SPIN_W*spinK;
      slots.forEach((s,i)=>stepSlot(s,i,clock));
      headGeo.attributes.position.needsUpdate=true;
      headGeo.attributes.aAlpha.needsUpdate=true;
      let any=false;
      for(let i=0;i<NODE_COUNT;i++){
        if(pulseAmt[i]>0.001){ pulseAmt[i]*=Math.pow(0.12,dt); any=true; }
        else pulseAmt[i]=0;
        nodeAlpha[i]=1+pulseAmt[i]*1.6;
        haloAlpha[i]=1+pulseAmt[i]*3.2;
      }
      if(any||clock<0.1){ nodeGeo.attributes.aAlpha.needsUpdate=true; haloGeo.attributes.aAlpha.needsUpdate=true; }
      controls.update();
    },
    onEnter(){ controls.enabled=true; },
    onLeave(){ controls.enabled=false; },
    applyTheme(){
      oceanU.uBase.value.copy(cssColor('--g-ocean'));
      oceanU.uRim.value.copy(cssColor('--g-rim'));
      oceanU.uRimInt.value=cssNum('--g-rim-int',.5);
      oceanU.uRimPow.value=cssNum('--g-rim-pow',3);
      oceanU.uShade.value=cssNum('--g-shade',.3);
      gratMat.color.copy(cssColor('--g-grat'));
      gratMat.opacity=cssNum('--g-grat-op',.1);
      landMat.uniforms.uColor.value.copy(cssColor('--g-land'));
      landMat.uniforms.uOpacity.value=cssNum('--g-land-op',.8);
      landMat.uniforms.uSize.value=cssNum('--g-land-size',.004);
      landMat.uniforms.uLit.value=cssNum('--g-land-lit',.2);
      nodeMat.uniforms.uColor.value.copy(cssColor('--g-node'));
      nodeMat.uniforms.uOpacity.value=cssNum('--g-node-op',1);
      nodeMat.uniforms.uSize.value=cssNum('--g-node-size',.0105);
      nodeMat.uniforms.uPulse.value=.16;
      nodeMat.uniforms.uLit.value=.10;
      haloMat.uniforms.uColor.value.copy(cssColor('--g-halo'));
      haloMat.uniforms.uOpacity.value=cssNum('--g-halo-op',.24);
      haloMat.uniforms.uSize.value=cssNum('--g-halo-size',.032);
      haloMat.uniforms.uPulse.value=.22;
      setBlend(haloMat,cssNum('--g-halo-add',1));
      headMat.uniforms.uColor.value.copy(cssColor('--g-head'));
      headMat.uniforms.uOpacity.value=cssNum('--g-head-op',1);
      headMat.uniforms.uSize.value=cssNum('--g-head-size',.013);
      setBlend(headMat,cssNum('--g-head-add',1));
      const ac=cssColor('--g-arc'), ao=cssNum('--g-arc-op',.7);
      slots.forEach(s=>{ s.m.color.copy(ac); s.baseOp=ao; });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ③ 五脑区大脑（P17 · 全轮之冠）
   ───────────────────────────────────────────────────────────────────────────
   母形 → 体积：页上那条 **13 段贝塞尔侧视轮廓**（_BRAIN）在构建期展平成折线发过来，
   运行时在它的包围盒里做确定性拒绝采样 —— 落在轮廓里的点才算数。每个点算出它到
   轮廓的距离 d，厚度剖面 T(d)=Tmax·sin(π/2·(d/dref)^0.62) 把它沿 ±z 两侧隆起：
   T 在轮廓上恰好为 0 ⇒ **正视（相机沿 +z）看到的限界就是原来那条轮廓本人**，
   侧视构图这个身份一格没丢；离开轮廓越深越厚，于是一颗有体积的脑。
   三条脑沟（中央沟 / 外侧裂 / 颞上沟）各自把 T 压下一道高斯槽 —— Sylvian 切口
   在 3D 里也是切口，不是被填平的疤。取样偏表面（pow(u,0.40)）⇒ 限界清脆、内部微透。
   五区按 SVG 里那五枚 blob 做点内判定（04 深部环走 even-odd，优先级最高 ⇒ 它压在
   顶叶之上，和 SVG 的绘制序一致）；放电周期与相位逐条抄 _ZONES 的 2.4/2.7/3.0/3.3/3.6s
   与那五个负 delay。8 条突触弧升维成跨半球的空间弧（z 拱 ±A，方向交替），光点沿弧走。
   自转是 ±12° 摇摆而**不是整圈转** —— 侧视轮廓是这张图的身份，转过去就不是脑了。
   「输出 · 最佳回复」hot 盒仍是页上的 SVG 件；脑向它送出的汇聚光流在 canvas 内
   收口到盒侧（x 1386，正是 SVG 那支箭头的落点）。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeBrain(ctx){
  const B = K.b, w = ctx.rect[2], h = ctx.rect[3], D = 1350;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, 200);
  const CONT = unpackPoly(B.cont);
  const ZONES = B.zones.map(unpackMulti);
  const SUL = B.sul.map(unpackPoly);
  const cx = B.c[0], cy = B.c[1];
  const grp = new THREE.Group(); grp.position.set(cx, -cy, 0); scene.add(grp);
  const flows = new THREE.Group(); scene.add(flows);

  /* ── ① 体积点云（母形 → 体积）──────────────────────────────────────────
     厚度剖面 T(x,y)：在轮廓上恰好为 0（⇒ 正视限界 = 原轮廓本人），越深越厚；
     三条脑沟各刻一道高斯槽（Sylvian 最深）；再叠一层程序化脑回涟漪。
     点云与脑沟曲线共用这一个函数 ⇒ 沟线永远贴着表面走，不浮起来也不陷进去。 */
  function brainT(x,y){
    let T = B.tmax*Math.sin(Math.PI/2*Math.pow(Math.min(1,distToPoly(CONT,x,y)/B.dref),0.62));
    for(let k=0;k<3;k++){
      const g = distToPoly(SUL[k],x,y);
      T *= 1 - B.sulD[k]*Math.exp(-(g*g)/(B.sulW[k]*B.sulW[k]));
    }
    return T * (1 + 0.06*Math.sin(0.105*x + 0.082*y + 2.1*Math.sin(0.028*x)));
  }
  function polyBB(P){
    let a=1e9,b=1e9,c=-1e9,d=-1e9;
    for(let i=0;i<P.length;i+=2){ a=Math.min(a,P[i]); c=Math.max(c,P[i]);
      b=Math.min(b,P[i+1]); d=Math.max(d,P[i+1]); }
    return [a,b,c,d];
  }
  const xs=[], ys=[], zs=[], zn=[], sf=[];
  const ZORD = [4,0,1,2,3];          // 04 深部环优先（与 SVG 绘制序一致：它画在最后）
  for(let i=0;i<B.n;i++){
    const x = B.bb[0] + (B.bb[2]-B.bb[0])*h1(i,127.1);
    const y = B.bb[1] + (B.bb[3]-B.bb[1])*h1(i,311.7);
    if(!insideMulti([CONT],x,y)) continue;
    const T = brainT(x,y);
    const surf = Math.pow(h1(i,571.3),0.40);
    const z = (h1(i,853.9)<0.5?-1:1)*T*surf;
    let zone = 1;
    for(const k of ZORD){ if(insideMulti(ZONES[k],x,y)){ zone=k; break; } }
    if(surf < 0.10) continue;          // 芯部太密：贴着中面的那一层丢掉，省片元也更透
    xs.push(x-cx); ys.push(-(y)+cy); zs.push(z); zn.push(zone); sf.push(surf);
  }
  const NP = xs.length;
  const cloudGeo = new THREE.BufferGeometry();
  const cpos = new Float32Array(NP*3), czn = new Float32Array(NP), csf = new Float32Array(NP);
  for(let i=0;i<NP;i++){ cpos[i*3]=xs[i]; cpos[i*3+1]=ys[i]; cpos[i*3+2]=zs[i];
    czn[i]=zn[i]; csf[i]=sf[i]; }
  cloudGeo.setAttribute('position', new THREE.BufferAttribute(cpos,3));
  cloudGeo.setAttribute('aZone', new THREE.BufferAttribute(czn,1));
  cloudGeo.setAttribute('aSurf', new THREE.BufferAttribute(csf,1));
  attrAH(cloudGeo, NP, 1, 0);
  const BR_VS = PX_HEAD + [
    'attribute float aZone; attribute float aSurf;',
    'uniform vec4 uZ; uniform float uZ4; uniform float uCap;',
    'void main(){',
    '  vec3 p=vec3(position.x,position.y,position.z*uIntro);',   // 体积从母形里长出来
    '  float z0=step(-0.5,aZone)*step(aZone,0.5);',
    '  float z1=step(0.5,aZone)*step(aZone,1.5);',
    '  float z2=step(1.5,aZone)*step(aZone,2.5);',
    '  float z3=step(2.5,aZone)*step(aZone,3.5);',
    '  float z4=step(3.5,aZone);',
    '  float fire=z0*uZ.x+z1*uZ.y+z2*uZ.z+z3*uZ.w+z4*uZ4;',
    // 放电不是「整块换成粉」：区内再叠一道横扫的空间相位 ⇒ 看得见电在区里走。
    // 上限压到 uCap（<1）—— 页上那五枚 blob 的填色本来就只有 .05→.15，
    // 3D 版要更亮但不能变成一块荧光贴纸（editorial 不是演唱会）。
    '  float wv=0.55+0.45*sin(uTime*2.6+position.x*0.032+position.y*0.026);',
    '  vH=fire*mix(0.34,1.0,wv)*uCap; vA=aA*mix(0.30,1.0,aSurf);',
    '  vec4 mv=pxCore(p, uSize*(0.72+0.5*aSurf)*(0.90+0.30*fire));',
    '  gl_Position=projectionMatrix*mv;',
    '}'].join('\n');
  const cloudMat = mkMat(SH, BR_VS, PX_PT_FS,
    { uZ:{value:new THREE.Vector4()}, uZ4:{value:0}, uCap:{value:.55} });
  const cloud = new THREE.Points(cloudGeo, cloudMat); cloud.frustumCulled=false; grp.add(cloud);

  /* ── ①b 小脑 + 脑干：页上它们是两枚独立闭合小形，3D 里也必须是两团独立的体积 ──
     「大脑 / 小脑」之间那道裂隙是这张侧视图最容易被读懂的解剖特征，填平就不是脑了。
     aZone = -1 ⇒ 五枚 step 判据全部落空 ⇒ 它们永远不放电（它们不是五个大脑之一）。 */
  {
    const px=[], sfa=[], zna=[];
    B.sub.forEach((sd,si)=>{
      const P = unpackPoly(sd), bx = polyBB(P), tm = B.subT[si];
      for(let i=0;i<B.subN;i++){
        const x = bx[0]+(bx[2]-bx[0])*h1(i,199.7+si*37), y = bx[1]+(bx[3]-bx[1])*h1(i,421.3+si*53);
        if(!insideMulti([P],x,y)) continue;
        const T = tm*Math.sin(Math.PI/2*Math.pow(Math.min(1,distToPoly(P,x,y)/(tm*0.9)),0.62));
        const surf = Math.pow(h1(i,613.1+si*29),0.40);
        if(surf < 0.12) continue;
        px.push(x-cx, -(y)+cy, (h1(i,877.3+si*41)<0.5?-1:1)*T*surf);
        sfa.push(surf); zna.push(-1);
      }
    });
    const n = sfa.length, g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(px),3));
    g.setAttribute('aZone', new THREE.BufferAttribute(new Float32Array(zna),1));
    g.setAttribute('aSurf', new THREE.BufferAttribute(new Float32Array(sfa),1));
    attrAH(g, n, 1, 0);
    const o = new THREE.Points(g, cloudMat); o.frustumCulled=false; grp.add(o);
  }
  /* ── ①c 脑沟：三条沟各自沿脑表两侧走一遍 ⇒ 五枚区岛的边界在 3D 里看得见 ──
     厚度剖面已经在沟位刻了槽，再把沟线本身画出来，「分区」才是画出来的而不是说出来的。 */
  const sulMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  {
    const seg=[], al=[];
    SUL.forEach((P)=>{
      const n=P.length/2;
      for(let side=-1;side<=1;side+=2){
        let prev=null;
        for(let i=0;i<n;i++){
          const x=P[i*2], y=P[i*2+1];
          if(!insideMulti([CONT],x,y)){ prev=null; continue; }
          const q=[x-cx, -(y)+cy, side*brainT(x,y)*0.86];
          if(prev){ seg.push(prev[0],prev[1],prev[2], q[0],q[1],q[2]);
            const e=Math.min(1,Math.min(i,n-1-i)/5); al.push(e,e); }
          prev=q;
        }
      }
    });
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    const ln=new THREE.LineSegments(g,sulMat); ln.frustumCulled=false; grp.add(ln);
  }
  /* ── ①d 母形轮廓环（z=0）：侧视轮廓是这张图的身份，给它一根真线 ──
     ±12° 摇摆时它跟着转、与限界错开一点点 —— 那一点点错位正是「这是个体，不是张图」。 */
  const rimMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  {
    const seg=[], al=[], n=CONT.length/2;
    for(let i=0;i<n-1;i++){
      seg.push(CONT[i*2]-cx, -(CONT[i*2+1])+cy, 0,
               CONT[i*2+2]-cx, -(CONT[i*2+3])+cy, 0);
      al.push(1,1);
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    const ln=new THREE.LineSegments(g,rimMat); ln.frustumCulled=false; grp.add(ln);
  }

  /* ── ② 突触弧：2D 弧升维成跨半球的空间弧（z 拱方向交替 ⇒ 有的从近侧穿过去）── */
  const arcCur = B.arcs.map((s,k)=>{
    const p = unpackPoly(s), n = p.length/2, dir = (k%2)?1:-1, out=[];
    for(let i=0;i<n;i++){ const t=i/(n-1);
      out.push([p[i*2]-cx, -(p[i*2+1])+cy, dir*B.arcA[k]*Math.sin(Math.PI*t)]); }
    return out;
  });
  {
    const seg=[], al=[];
    arcCur.forEach(c=>{ for(let i=0;i<c.length-1;i++){
      const e=Math.min(1,Math.min(i,c.length-2-i)/6);
      seg.push(c[i][0],c[i][1],c[i][2], c[i+1][0],c[i+1][1],c[i+1][2]); al.push(e,e); } });
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    var arcMatB = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,arcMatB); ln.frustumCulled=false; grp.add(ln);
  }
  /* ── ③ 神经火花：8 枚光点沿弧穿行（周期 / 起相位逐条抄 SVG 的 _ARCS）── */
  const SPK = B.spark, spkGeo = new THREE.BufferGeometry();
  const spkPos = new Float32Array(SPK.length*3);
  spkGeo.setAttribute('position', new THREE.BufferAttribute(spkPos,3));
  const spkA = attrAH(spkGeo, SPK.length, 1, 1);
  const spkMat = mkMat(SH, PX_PT_VS, PX_PT_FS); spkMat.uniforms.uSoft.value=.03;
  const spks = new THREE.Points(spkGeo, spkMat); spks.frustumCulled=false; grp.add(spks);

  /* ── ④ 输入：耳位 → 颞叶下部（01 区）的常驻声流（路径 = SVG 的 _IN）── */
  const IN = unpackPoly(B.inp), INC = polyCum(IN), _o=[0,0];
  function inAt(t,out){ polyAt(IN,INC,t,_o);
    out[0]=_o[0]; out[1]=-_o[1]; out[2]=34*Math.sin(Math.PI*t); return out; }
  var inMat;
  {
    const seg=[], al=[], N=48, a=[0,0,0], b=[0,0,0];
    for(let i=0;i<N;i++){
      inAt(i/N,a); inAt((i+1)/N,b);
      seg.push(a[0],a[1],a[2], b[0],b[1],b[2]);
      const e=0.3+0.7*(i/N); al.push(e,e);
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    inMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,inMat); ln.frustumCulled=false; flows.add(ln);
  }
  /* ── ⑤ 输出：额叶前缘的汇聚光流 → 收口到 hot 盒左沿（x 1386，SVG 箭头落点）── */
  const OUTP = [];
  {
    const front=[];
    for(let i=0;i<CONT.length/2;i++){ const X=CONT[i*2], Y=CONT[i*2+1];
      if(X>B.outX) front.push([X,Y]); }
    for(let k=0;k<5;k++){
      const s = front[Math.floor((k+0.5)/5*front.length)] || [B.outX,268];
      const zz = (k-2)*26;
      OUTP.push([[s[0],s[1],zz],[B.out[0],B.out[1],zz*0.35],[B.out2[0],B.out2[1],0]]);
    }
  }
  {
    const seg=[], al=[];
    OUTP.forEach(c=>{
      const N=26;
      for(let i=0;i<N;i++){
        const a=outAt(c,i/N), b=outAt(c,(i+1)/N);
        seg.push(a[0],a[1],a[2], b[0],b[1],b[2]);
        const e=0.35+0.65*(i/N); al.push(e,e);
      }
    });
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    var outMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,outMat); ln.frustumCulled=false; flows.add(ln);
  }
  function outAt(c,t){                 // 二次贝塞尔：脑面 → 收口点 → 盒沿
    const u=1-t;
    return [u*u*c[0][0]+2*u*t*c[1][0]+t*t*c[2][0],
            -(u*u*c[0][1]+2*u*t*c[1][1]+t*t*c[2][1]),
            u*u*c[0][2]+2*u*t*c[1][2]+t*t*c[2][2]];
  }
  const FLOWN = 3*1 + 5*2;             // 输入 3 枚 + 输出五路各 2 枚
  const flowGeo = new THREE.BufferGeometry();
  const flowPos = new Float32Array(FLOWN*3);
  flowGeo.setAttribute('position', new THREE.BufferAttribute(flowPos,3));
  const flowA = attrAH(flowGeo, FLOWN, 1, 1);
  const flowMat = mkMat(SH, PX_PT_VS, PX_PT_FS); flowMat.uniforms.uSoft.value=.03;
  const flowPts = new THREE.Points(flowGeo, flowMat); flowPts.frustumCulled=false; flows.add(flowPts);

  const SWAY = B.sway*Math.PI/180, _t3=[0,0,0];
  return {
    scene, camera, intro:1.15, grab:false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    applyTheme(){
      cloudMat.uniforms.uColor.value.copy(cssColor('--b-ink'));
      cloudMat.uniforms.uHot.value.copy(cssColor('--b-hot'));
      cloudMat.uniforms.uOpacity.value = cssNum('--b-op',.5);
      cloudMat.uniforms.uSize.value = cssNum('--b-size',2);
      cloudMat.uniforms.uBack.value = cssNum('--b-back',.28);
      cloudMat.uniforms.uGain.value = cssNum('--b-gain',1.2);
      cloudMat.uniforms.uCap.value = cssNum('--b-cap',.55);
      setBlend(cloudMat, cssNum('--b-add',0));
      // 脑沟 / 母形轮廓环：走墨色线稿档（比点云重一档，比放电轻一档）
      [sulMat, rimMat].forEach((m,i)=>{
        m.uniforms.uColor.value.copy(cssColor('--b-ink'));
        m.uniforms.uHot.value.copy(cssColor('--b-ink'));
        m.uniforms.uOpacity.value = cssNum('--b-op',.5)*(i ? 0.62 : 0.85);
        m.uniforms.uBack.value = cssNum('--b-back',.28);
        m.uniforms.uGain.value = 0;
        setBlend(m, cssNum('--b-add',0));
      });
      arcMatB.uniforms.uColor.value.copy(cssColor('--b-arc'));
      arcMatB.uniforms.uHot.value.copy(cssColor('--b-arc'));
      arcMatB.uniforms.uOpacity.value = cssNum('--b-arc-op',.3);
      arcMatB.uniforms.uBack.value = cssNum('--b-back',.28);
      spkMat.uniforms.uColor.value.copy(cssColor('--b-spark'));
      spkMat.uniforms.uHot.value.copy(cssColor('--b-spark'));
      spkMat.uniforms.uOpacity.value = cssNum('--b-spark-op',.9);
      spkMat.uniforms.uSize.value = cssNum('--b-spark-size',5);
      spkMat.uniforms.uGain.value = 0;
      setBlend(spkMat, cssNum('--b-spark-add',0));
      [outMat, flowMat, inMat].forEach(m=>{
        m.uniforms.uColor.value.copy(cssColor('--b-flow'));
        m.uniforms.uHot.value.copy(cssColor('--b-flow'));
        m.uniforms.uOpacity.value = cssNum('--b-flow-op',.8);
        m.uniforms.uGain.value = 0;
      });
      flowMat.uniforms.uSize.value = cssNum('--b-flow-size',4.6);
      setBlend(flowMat, cssNum('--b-spark-add',0));
    },
    draw(dt, clock){
      SH.uTime.value = clock;
      // 五区异步放电：周期 / 相位逐条抄 SVG 的 _ZONES（2.4/2.7/3.0/3.3/3.6s + 负 delay）
      const f=[];
      // 占空比收窄（pow 2.2）：大部分时间整颗脑是墨色线稿，只有**正在放电**的那一区
      // 亮起来 —— 五区同时半亮就成了一团粉，读不出「异步」，也不是 editorial。
      for(let k=0;k<5;k++) f.push(Math.pow(0.5-0.5*Math.cos(TAU*(clock-B.zoff[k])/B.zper[k]),2.2));
      cloudMat.uniforms.uZ.value.set(f[0],f[1],f[2],f[3]);
      cloudMat.uniforms.uZ4.value = f[4];
      // ±12° 摇摆（不整圈转 —— 侧视轮廓是构图身份）
      grp.rotation.y = SWAY*Math.sin(TAU*clock/B.swayP);
      // 神经火花
      for(let i=0;i<SPK.length;i++){
        const s=SPK[i], c=arcCur[s[0]];
        let u=((clock-s[2])/s[1])%1; if(u<0)u+=1;
        const j=Math.min(c.length-2,Math.floor(u*(c.length-1))), fu=u*(c.length-1)-j;
        spkPos[i*3]  = c[j][0]+(c[j+1][0]-c[j][0])*fu;
        spkPos[i*3+1]= c[j][1]+(c[j+1][1]-c[j][1])*fu;
        spkPos[i*3+2]= c[j][2]+(c[j+1][2]-c[j][2])*fu;
        spkA.a[i] = Math.min(1,Math.min(u,1-u)*7);
      }
      spkGeo.attributes.position.needsUpdate=true; spkGeo.attributes.aA.needsUpdate=true;
      // 输入 3 枚 + 输出 10 枚（1.6s 重拍 —— 与 SVG 里那条快路径同一个节拍）
      let n=0;
      for(let i=0;i<3;i++){
        let u=((clock/2.6)+i/3)%1;
        inAt(u,_t3); flowPos[n*3]=_t3[0]; flowPos[n*3+1]=_t3[1]; flowPos[n*3+2]=_t3[2];
        flowA.a[n]=Math.min(1,Math.min(u,1-u)*6); n++;
      }
      for(let k=0;k<OUTP.length;k++) for(let m=0;m<2;m++){
        let u=((clock/1.6)+m*0.5+k*0.11)%1;
        const p=outAt(OUTP[k],u);
        flowPos[n*3]=p[0]; flowPos[n*3+1]=p[1]; flowPos[n*3+2]=p[2];
        flowA.a[n]=Math.min(1,Math.min(u,1-u)*6); n++;
      }
      flowGeo.attributes.position.needsUpdate=true; flowGeo.attributes.aA.needsUpdate=true;
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ④ SAL 双层防御壳（P9）
   ───────────────────────────────────────────────────────────────────────────
   页上那两枚「留左缺口的防御环」的真三维化：外壳 = 降噪层（传统 + AI 降噪），
   内壳 = SAL 声纹层，缺口开在 -X（正对页上「目标人声」那一路实线波束）。
   三类噪声从四面八方射向中心的「目标人声」核：01 稳态 / 02 瞬态撞外壳弹开，
   03 非对话人人声穿过外壳、在内壳被挡（这正是 SAL 的进阶所在）；
   只有目标声线从缺口穿两壳直达核。弹开的粒子带衰减轨迹 —— 挡住不是消失。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeShell(ctx){
  const S = K.s, w = ctx.rect[2], h = ctx.rect[3], D = 1100;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, 300);
  const grp = new THREE.Group(); grp.position.set(S.c[0], -S.c[1], 0); scene.add(grp);

  /* ── 壳：fresnel 半透明球面 + 一层很淡的经纬网；-X 方向切一个缺口 ── */
  const SHELL_VS = [
    'uniform float uIntro; varying vec3 vN,vP,vL;',
    'void main(){ vN=normalize(normalMatrix*normal); vL=normalize(position);',
    '  vec4 mv=modelViewMatrix*vec4(position*max(uIntro,0.001),1.0); vP=mv.xyz;',
    '  gl_Position=projectionMatrix*mv; }'].join('\n');
  const SHELL_FS = [
    'uniform vec3 uColor; uniform float uOpacity,uPow,uGap;',
    'varying vec3 vN,vP,vL;',
    'void main(){',
    '  if(vL.x < -uGap) discard;',                 // 缺口：目标人声从这里进来
    '  vec3 n=normalize(vN), v=normalize(-vP);',
    '  float f=pow(clamp(1.0-abs(dot(n,v)),0.0,1.0),uPow);',
    '  float a=uOpacity*f;',
    '  if(a<0.004) discard;',
    '  gl_FragColor=vec4(uColor,a);',
    '  #include <colorspace_fragment>',
    '}'].join('\n');
  function shellMesh(r,gap){
    const m = new THREE.ShaderMaterial({
      uniforms:{ uIntro:SH.uIntro, uColor:{value:new THREE.Color()},
                 uOpacity:{value:.2}, uPow:{value:2.6}, uGap:{value:gap} },
      vertexShader:SHELL_VS, fragmentShader:SHELL_FS,
      transparent:true, depthWrite:false, side:THREE.DoubleSide });
    const o = new THREE.Mesh(new THREE.SphereGeometry(r,54,34), m);
    o.frustumCulled=false; grp.add(o); return {o,m};
  }
  const outer = shellMesh(S.r2, S.gap2), inner = shellMesh(S.r1, S.gap1);
  /* 壳上的经纬细网：让「壳」读成一层膜而不是一团雾（缺口处不画） */
  function shellWire(r,gap){
    const pts=[];
    const v=(la,lo)=>{ const p=la*Math.PI/180,l=lo*Math.PI/180,c=Math.cos(p);
      return [c*Math.sin(l)*r, Math.sin(p)*r, c*Math.cos(l)*r]; };
    const okp=(q)=>(q[0]/r) >= -gap;
    for(let lo=-180;lo<180;lo+=30){ let pv=null;
      for(let la=-84;la<=84;la+=6){ const q=v(la,lo);
        if(pv&&okp(q)&&okp(pv)) pts.push(pv,q); pv=q; } }
    for(let la=-60;la<=60;la+=30){ let pv=null;
      for(let lo=-180;lo<=180;lo+=6){ const q=v(la,lo);
        if(pv&&okp(q)&&okp(pv)) pts.push(pv,q); pv=q; } }
    const g=new THREE.BufferGeometry(), f=new Float32Array(pts.length*3);
    pts.forEach((q,i)=>{ f[i*3]=q[0]; f[i*3+1]=q[1]; f[i*3+2]=q[2]; });
    g.setAttribute('position', new THREE.BufferAttribute(f,3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(pts.length).fill(1),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(pts.length),1));
    const m = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,m); ln.frustumCulled=false; grp.add(ln);
    return m;
  }
  const wire2 = shellWire(S.r2,S.gap2), wire1 = shellWire(S.r1,S.gap1);

  /* ── 核（目标人声）：一小簇点 + 一枚亮心 ── */
  const coreGeo = new THREE.BufferGeometry();
  {
    const n=110, f=new Float32Array(n*3);
    for(let i=0;i<n;i++){
      const u=1-2*(i+0.5)/n, r=Math.sqrt(Math.max(0,1-u*u)), th=i*2.399963;
      const rr=S.rc*(0.55+0.45*h1(i,17.3));
      f[i*3]=Math.cos(th)*r*rr; f[i*3+1]=u*rr; f[i*3+2]=Math.sin(th)*r*rr;
    }
    coreGeo.setAttribute('position', new THREE.BufferAttribute(f,3));
    attrAH(coreGeo, n, 1, 1);
  }
  const coreMat = mkMat(SH, PX_PT_VS, PX_PT_FS); coreMat.uniforms.uSoft.value=.04;
  const core = new THREE.Points(coreGeo, coreMat); core.frustumCulled=false; grp.add(core);

  /* ── 粒子流：三类噪声 + 目标人声，各一枚 Points（颜色分三档，不靠说明靠看）── */
  const PT_VS_S = [
    'uniform float uIntro,uSize,uD,uPx,uNear,uFar,uTime,uR0;',
    'attribute vec3 aDir; attribute float aPh; attribute float aStop; attribute float aDur;',
    'varying float vFade,vA,vH;',
    'void main(){',
    '  float t=fract((uTime+aPh)/aDur);',
    '  float ti=min(t/0.62,1.0), tb=max(0.0,(t-0.62)/0.38);',
    '  float rin=mix(uR0,aStop,ti*ti*(3.0-2.0*ti));',
    '  float rout=aStop+(uR0-aStop)*0.34*tb;',              // 弹开：衰减轨迹
    '  float r=mix(rin,rout,step(0.62,t));',
    '  vec3 p=aDir*r*max(uIntro,0.001);',
    '  vA=(1.0-tb*0.92)*min(1.0,t*16.0)*uIntro; vH=0.0;',
    '  vec4 mv=modelViewMatrix*vec4(p,1.0);',
    '  float z=max(-mv.z,1.0);',
    '  vFade=clamp((uFar-z)/(uFar-uNear),0.0,1.0);',
    '  gl_PointSize=max(uSize*uPx*uD/z,0.55);',
    '  gl_Position=projectionMatrix*mv;',
    '}'].join('\n');
  function stream(n, base, spread, stop, durs, seed, gapFree){
    const g=new THREE.BufferGeometry();
    const pos=new Float32Array(n*3), dir=new Float32Array(n*3);
    const ph=new Float32Array(n), st=new Float32Array(n), du=new Float32Array(n);
    for(let i=0;i<n;i++){
      let dx,dy,dz,l,tries=0;
      do{
        dx=base[0]+spread*(h1(i,seed)*2-1);
        dy=base[1]+spread*(h1(i,seed+11.3)*2-1);
        dz=base[2]+spread*(h1(i,seed+27.9)*2-1)+0.0001*tries;
        l=Math.hypot(dx,dy,dz)||1; dx/=l; dy/=l; dz/=l;
        tries++;
        // 缺口是留给目标人声的：噪声不许从那儿进来（否则「只有它能进」就不成立了）
      }while(!gapFree && dx < -S.gap2*0.86 && tries<8);
      dir[i*3]=dx; dir[i*3+1]=dy; dir[i*3+2]=dz;
      ph[i]=h1(i,seed+3.7)*10; st[i]=stop; du[i]=durs[0]+(durs[1]-durs[0])*h1(i,seed+5.1);
    }
    g.setAttribute('position', new THREE.BufferAttribute(pos,3));
    g.setAttribute('aDir', new THREE.BufferAttribute(dir,3));
    g.setAttribute('aPh', new THREE.BufferAttribute(ph,1));
    g.setAttribute('aStop', new THREE.BufferAttribute(st,1));
    g.setAttribute('aDur', new THREE.BufferAttribute(du,1));
    const m = mkMat(SH, PT_VS_S, PX_PT_FS, { uR0:{value:S.r0} });
    m.uniforms.uSoft.value=.05;
    const o = new THREE.Points(g,m); o.frustumCulled=false; o.matrixAutoUpdate=false; grp.add(o);
    return m;
  }
  // 三路的主方向逐条对上页上那三支点线波束（从右上 / 正右 / 右下射进来）
  // spread 收到 .30：三路必须读成**三束**（对上页上右侧那三枚噪声源），
  // 放到 .70 就成了一层均匀的噪点雾，「三类噪声」当场读不出来。
  // 二轮精修 · 波A：四股的周期由「行程 ÷ 目标流速」反推（S.dur，见 _spd_rows(9)）——
  // 同一股内不再有 ±40% 的随机时长：一股就是一束，束里的粒子当然同速。
  const n1 = stream(120, S.d1, .30, S.r2, [S.dur[0],S.dur[0]], 101.1, false);
  const n2 = stream(104, S.d2, .28, S.r2, [S.dur[1],S.dur[1]], 213.7, false);
  const n3 = stream(92,  S.d3, .26, S.r1, [S.dur[2],S.dur[2]], 331.9, false);
  const tg = stream(34, [-1,0,0], .17, S.rc*0.8, [S.dur[3],S.dur[3]], 457.3, true);
  /* 目标人声主通路：从缺口穿两层壳直达核的一根实线（页上那根 accent 实线波束的升维）。
     三路噪声是点线（撞壳弹开），只有它是一条**连通**的线 —— 「只有它能进来」是画出来的。 */
  var beamMat;
  {
    const seg=[], al=[], N=40;
    for(let i=0;i<N;i++){
      const r0=S.r0*(1-i/N)+S.rc*0.55*(i/N), r1=S.r0*(1-(i+1)/N)+S.rc*0.55*((i+1)/N);
      seg.push(-r0,0,0, -r1,0,0);
      const e=0.35+0.65*(i/N); al.push(e,e);
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    beamMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,beamMat); ln.frustumCulled=false; grp.add(ln);
  }

  return {
    scene, camera, intro:1.0, grab:false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){ SH.uTime.value = clock; },
    applyTheme(){
      outer.m.uniforms.uColor.value.copy(cssColor('--s-shell'));
      outer.m.uniforms.uOpacity.value = cssNum('--s-shell-op',.19);
      outer.m.uniforms.uPow.value = cssNum('--s-shell-pow',2.6);
      inner.m.uniforms.uColor.value.copy(cssColor('--s-inner'));
      inner.m.uniforms.uOpacity.value = cssNum('--s-inner-op',.24);
      inner.m.uniforms.uPow.value = cssNum('--s-shell-pow',2.6);
      [wire2,wire1].forEach((m,i)=>{
        m.uniforms.uColor.value.copy(cssColor(i?'--s-inner':'--s-grid'));
        m.uniforms.uHot.value.copy(cssColor(i?'--s-inner':'--s-grid'));
        m.uniforms.uOpacity.value = cssNum('--s-grid-op',.14)*(i?1.5:1);
        m.uniforms.uGain.value = 0;
      });
      coreMat.uniforms.uColor.value.copy(cssColor('--s-core'));
      coreMat.uniforms.uHot.value.copy(cssColor('--s-core'));
      coreMat.uniforms.uOpacity.value = cssNum('--s-core-op',.95);
      coreMat.uniforms.uSize.value = cssNum('--s-core-size',4.2);
      coreMat.uniforms.uGain.value = 0;
      const nz = cssNum('--s-noise-size',3.6);
      [[n1,'--s-n1','--s-n1-op'],[n2,'--s-n2','--s-n2-op'],[n3,'--s-n3','--s-n3-op']]
        .forEach(([m,c,o])=>{
          m.uniforms.uColor.value.copy(cssColor(c));
          m.uniforms.uHot.value.copy(cssColor(c));
          m.uniforms.uOpacity.value = cssNum(o,.7);
          m.uniforms.uSize.value = nz; m.uniforms.uGain.value = 0;
        });
      beamMat.uniforms.uColor.value.copy(cssColor('--s-target'));
      beamMat.uniforms.uHot.value.copy(cssColor('--s-target'));
      beamMat.uniforms.uOpacity.value = cssNum('--s-target-op',.95)*.8;
      beamMat.uniforms.uGain.value = 0;
      tg.uniforms.uColor.value.copy(cssColor('--s-target'));
      tg.uniforms.uHot.value.copy(cssColor('--s-target'));
      tg.uniforms.uOpacity.value = cssNum('--s-target-op',.95);
      tg.uniforms.uSize.value = cssNum('--s-target-size',5);
      tg.uniforms.uGain.value = 0;
      [n1,n2,n3,tg,beamMat,coreMat].forEach(m=>setBlend(m,cssNum('--s-add',0)));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑤ Loop Engineering · 复利螺旋 + LOOP 投影锁空间环带（P18）
   ───────────────────────────────────────────────────────────────────────────
   左图：页上那条成长曲线（_CA_CURVE）就是这条螺旋的**脊线** —— 2D 图的坐标账
   一格没动，只是让带子绕着它转。半径与带宽随 t 一起长：复利不是「涨得更高」，
   是「每一圈都更宽」。四枚发光站点落在 DAY 01/07/15/30 的 x 上。

   ── 二轮精修 · 波A：右图 LOOP 一起进 3D，舞台横跨两图 ────────────────────
   终审：「P18 的 loop 是非常专业的底层技术，当前偏 2D，至少对齐左侧（螺旋带）
   的转化效果；排版上两张图偏挤。」四件事：
     ① LOOP 用 **投影锁**（mkLock）而不是真旋转 —— 这是唯一能同时满足
        「真倾斜轨道环」与「四站名一格不挪」的做法（真转一下，复盘 / 定位 /
        迭代 / 训练 四个词立刻指空）。环成为一条 mkStream 连续流：
        loop 本来就是「一直在转」，它是介质不是事件。
     ② 舞台 1240 → 1680 横跨两图（LAB_RECTS）：扩的是「区域」，字一格没动。
     ③ 相机 D 560 → 1500：560 档的水平视场 112°，环画到边会被剪斜。
        换相机之后螺旋用 **mkRelock** 逐像素还原 —— 拍板过的形不该因为
        隔壁多了一枚环就变（证明见 lab-kit ⑨ 的 mkRelock 注）。
     ④ 补回「**真人销冠**」基准虚线：旧版 3D 漏画了它，页上那四个字指着一片空白。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeSpiral(ctx){
  const R = K.r, w = ctx.rect[2], h = ctx.rect[3], D = R.D;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  /* 换相机不换观感：螺旋的几何仍按拍板过的 D560 / 旧舞台宽造，
     再整体过一遍 relock —— 屏上逐像素与旧版相同。 */
  const W0 = 1240, RL = mkRelock([W0/2, -h/2], R.D0, [w/2, -h/2], D);
  // 深度雾半程跟着 relock 一起放大 ⇒ 「转到背面那半圈明显暗下去」原样保留
  const SH = pxShared(D, RL.half(R.half));
  const L = mkLock(w, h, D);                       // 右图 LOOP 环带的投影锁
  const SP = unpackPoly(R.spine), SC = polyCum(SP), _o=[0,0];
  const N = R.n, pts=[], nrm=[];
  function spineAt(t){ polyAt(SP,SC,t,_o); return [_o[0],-_o[1],0]; }
  for(let i=0;i<N;i++){
    const t=i/(N-1), c=spineAt(t);
    const a=spineAt(Math.max(0,t-0.004)), b=spineAt(Math.min(1,t+0.004));
    let tx=b[0]-a[0], ty=b[1]-a[1]; const tl=Math.hypot(tx,ty)||1; tx/=tl; ty/=tl;
    const nx=-ty, ny=tx;                            // 脊线的面内法向
    const rr=R.r0+(R.r1-R.r0)*t, th=TAU*R.turns*t;
    pts.push([c[0]+nx*rr*Math.cos(th), c[1]+ny*rr*Math.cos(th), rr*Math.sin(th)]);
    // 径向：带面就展在这个方向上（绕轴转到哪儿，带面就朝哪儿）
    nrm.push([nx*Math.cos(th), ny*Math.cos(th), Math.sin(th)]);
  }
  const ptsR = pts.map(RL.p);                       // relock 之后的落点（站点 / 光点都用它）
  /* ── 螺旋带（ribbon）：宽度随 t 增长，带面沿径向展开 ── */
  const rgeo = RL.geo(ribbonGeo(pts, (t)=>R.w0+(R.w1-R.w0)*t, null, nrm));
  {
    const n=rgeo.attributes.position.count;
    rgeo.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(n).fill(1),1));
    rgeo.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(n),1));
  }
  const bandMat = mkMat(SH, PX_RB_VS, PX_RB_FS, { uFlow:{value:5} });
  bandMat.side = THREE.DoubleSide;
  scene.add(new THREE.Mesh(rgeo, bandMat));
  /* ── 两条轨（带子的上下沿）：带面之外再钉一层线稿，editorial 的骨 ── */
  {
    const seg=[], al=[], hh=[];
    const P=rgeo.attributes.position.array;
    for(let side=0;side<2;side++) for(let i=0;i<N-1;i++){
      const a=(i*2+side)*3, b=((i+1)*2+side)*3;
      seg.push(P[a],P[a+1],P[a+2],P[b],P[b+1],P[b+2]);
      const t=i/(N-1); al.push(0.35+0.65*t,0.35+0.65*t); hh.push(t,t);
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(hh),1));
    var railMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,railMat); ln.frustumCulled=false; scene.add(ln);
  }
  /* ── 脊线轴：页上那条成长曲线本人（z=0 的一根细线）────────────────────
     没有轴，绕轴的带子在屏上就只是一条波浪线；有了轴，「前面那半圈 / 后面那半圈」
     一眼就分得出来 —— 螺旋是绕着**成长曲线**长的，这就是复利的形。 */
  var axisMat;
  {
    const seg=[], al=[], NA=200;
    for(let i=0;i<NA;i++){
      const a=spineAt(i/NA), b2=spineAt((i+1)/NA);
      seg.push(a[0],a[1],0, b2[0],b2[1],0); al.push(1,1);
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    axisMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,axisMat); ln.frustumCulled=false; scene.add(ln);
  }
  /* ── 「真人销冠」基准虚线（波A 补回）────────────────────────────────────
     页上那条 dash「7 6」的 mo-drift 平线：基准线也是活的，只是**不长**。
     dash 相位按页上的 --mo-off:-39 / --mo-dur:3.4s 同参漂移（C 档：页面 CSS 同源，
     不许为了统一流速去改它）。3D 里没有它，页上「真人销冠」四个字就指着空白。 */
  const BD = R.baseDash[0] + R.baseDash[1], BASEN = Math.ceil((R.base[2]-R.base[0])/BD)+2;
  const bgeo = new THREE.BufferGeometry();
  const bpos = new Float32Array(BASEN*6);
  bgeo.setAttribute('position', new THREE.BufferAttribute(bpos,3));
  const bA = fillAH(bgeo, 1, 0);
  const baseMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  scene.add(Object.assign(new THREE.LineSegments(bgeo, baseMat), { frustumCulled:false }));
  /* ── 四枚站点：复盘 / 定位 / 迭代 / 训练 落在 DAY 01/07/15/30 的 x 上 ── */
  const stT = R.days.map(dx=>{
    let best=0, bd=1e9;
    for(let i=0;i<N;i++){ const t=i/(N-1), d=Math.abs(spineAt(t)[0]-dx);
      if(d<bd){bd=d;best=t;} }
    return best;
  });
  const stGeo = new THREE.BufferGeometry();
  {
    const f=new Float32Array(stT.length*3);
    stT.forEach((t,i)=>{ const j=Math.round(t*(N-1));
      f[i*3]=ptsR[j][0]; f[i*3+1]=ptsR[j][1]; f[i*3+2]=ptsR[j][2]; });
    stGeo.setAttribute('position', new THREE.BufferAttribute(f,3));
  }
  const stA = attrAH(stGeo, stT.length, 1, 1);
  const nodeMatR = mkMat(SH, PX_PT_VS, PX_PT_FS); nodeMatR.uniforms.uSoft.value=.02;
  const stPts = new THREE.Points(stGeo, nodeMatR); stPts.frustumCulled=false; scene.add(stPts);
  const haloMatR = mkMat(SH, PX_PT_VS, PX_PT_FS); haloMatR.uniforms.uSoft.value=.24;
  const stHalo = new THREE.Points(stGeo, haloMatR); stHalo.frustumCulled=false; scene.add(stHalo);
  /* ── 爬升的光点 ── */
  const SN = 14, spGeo = new THREE.BufferGeometry();
  const spPos = new Float32Array(SN*3);
  spGeo.setAttribute('position', new THREE.BufferAttribute(spPos,3));
  const spA = attrAH(spGeo, SN, 1, 1);
  const sparkMat = mkMat(SH, PX_PT_VS, PX_PT_FS); sparkMat.uniforms.uSoft.value=.03;
  const sparks = new THREE.Points(spGeo, sparkMat); sparks.frustumCulled=false; scene.add(sparks);

  /* ═══ 右图：LOOP 投影锁空间环带 ═══════════════════════════════════════
     环平面绕水平轴一倾（上沿近、下沿远），**投影锁**把每一个落点按 (D−z)/D
     预缩放 ⇒ 透视除法正好把这一档除回去：屏上仍是页上那枚 r96 的正圆，
     四个站名一格不挪，而深度雾 / 点径 / 前后遮挡全都真的在。
     环本身是一条 mkStream 连续流 —— loop 是「一直在转」，它是介质不是事件。 */
  const RC = [R.ring[0] + R.rdx, R.ring[1]], RR = R.ring[2];
  const ringZ = (y) => -(y - RC[1]) * R.ringTz;
  const loopStr = (function(){
    const NR = 220, p = [];
    for(let i=0;i<=NR;i++){
      const a = i/NR*TAU - Math.PI/2;               // 从「复盘」（钟面 12 点）起手
      const x = RC[0] + Math.cos(a)*RR, y = RC[1] + Math.sin(a)*RR;
      p.push(L(x, y, ringZ(y)));
    }
    // edge:0 —— 闭环没有「接头」；起手角取 −π/2（12 点），那一处正好压在
    // 「复盘」那枚实心站点圆之下，包络的首尾差在屏上根本露不出来。
    return mkStream(SH, p, { w: R.ringW/2, spd: R.ringSpd, edge: 0,
                             lam: TAU*RR/R.ringN }).add(scene);
  })();
  /* 四枚站点圆：**先填底再描边** —— 页上它们是 card-bg-2 的实心圆，
     把环压在身后（不这么画，环就从「复盘」两个字里穿过去）。 */
  const fillMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const ringNodeMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  {
    const fpos = [], fidx = [], lseg = []; let base = 0;
    R.node.forEach((nd) => {
      const nx = nd[0] + R.rdx, ny = nd[1], nz = ringZ(ny);
      const c = L(nx, ny, nz);
      fpos.push(c);
      const NA = 40, ring = [];
      for(let i=0;i<=NA;i++){
        const a = i/NA*TAU;
        ring.push(L(nx + Math.cos(a)*R.nodeR, ny + Math.sin(a)*R.nodeR, nz));
      }
      ring.forEach(q => fpos.push(q));
      for(let i=0;i<NA;i++) fidx.push(base, base+1+i, base+2+i);
      base += NA + 2;
      for(let i=0;i<NA;i++)
        lseg.push([ring[i][0],ring[i][1],ring[i][2], ring[i+1][0],ring[i+1][1],ring[i+1][2]]);
    });
    const fg = new THREE.BufferGeometry();
    const fa = new Float32Array(fpos.length*3);
    fpos.forEach((q,i)=>{ fa[i*3]=q[0]; fa[i*3+1]=q[1]; fa[i*3+2]=q[2]; });
    fg.setAttribute('position', new THREE.BufferAttribute(fa,3));
    fg.setIndex(fidx); fillAH(fg, 1, 0);
    const mesh = new THREE.Mesh(fg, fillMat); mesh.frustumCulled=false; scene.add(mesh);
    const lg = segGeo(lseg); fillAH(lg, 1, 0);
    scene.add(Object.assign(new THREE.LineSegments(lg, ringNodeMat), { frustumCulled:false }));
  }

  return {
    scene, camera, intro:1.35, grab:false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    /* 闸门探针：**mkRelock 的机器证明** —— 逐点比「旧相机(D0, 旧舞台宽) 下的屏点」
       与「新相机(D, 新舞台宽) 下的屏点」，以及深度雾值。两者若真的逐像素还原，
       这两个偏差就必须是 0（不是「小」，是 0）。 */
    state(){
      const pr = (q, cx, DD) => { const k = DD/(DD-q[2]);
        return [cx+(q[0]-cx)*k, -h/2+(q[1]+h/2)*k]; };
      const fg = (z, DD, hf) => ((DD+hf)-(DD-z))/(2*hf);
      let dev = 0, fdev = 0;
      for(let i=0;i<N;i++){
        const o = pr(pts[i], W0/2, R.D0), n2 = pr(ptsR[i], w/2, D);
        dev = Math.max(dev, Math.hypot(o[0]-n2[0], o[1]-n2[1]));
        fdev = Math.max(fdev, Math.abs(fg(pts[i][2], R.D0, R.half)
                                     - fg(ptsR[i][2], D, RL.half(R.half))));
      }
      return { D:D, D0:R.D0, relock:RL.s, relockDev:dev, fogDev:fdev,
               ring:[RC[0],RC[1],RR], base:R.base.slice(),
               climb:R.climb, ringDur:R.ringDur, days:R.days.slice() };
    },
    draw(dt, clock){
      SH.uTime.value = clock;
      loopStr.draw(clock);
      for(let i=0;i<SN;i++){
        let u=((clock/R.climb)+i/SN)%1;
        const j=Math.min(N-2,Math.floor(u*(N-1))), fu=u*(N-1)-j;
        spPos[i*3]  = ptsR[j][0]+(ptsR[j+1][0]-ptsR[j][0])*fu;
        spPos[i*3+1]= ptsR[j][1]+(ptsR[j+1][1]-ptsR[j][1])*fu;
        spPos[i*3+2]= ptsR[j][2]+(ptsR[j+1][2]-ptsR[j][2])*fu;
        spA.a[i]=Math.min(1,Math.min(u*8,(1-u)*5))*(0.45+0.55*u);
      }
      spGeo.attributes.position.needsUpdate=true; spGeo.attributes.aA.needsUpdate=true;
      // 基准虚线：dash 相位按页上 --mo-off:-39 / --mo-dur:3.4s 同参漂移
      const off = (clock/3.4)*39 % BD;
      for(let i=0;i<BASEN;i++){
        const a = R.base[0] - BD + i*BD + off, b2 = a + R.baseDash[0];
        const ca = Math.max(R.base[0], Math.min(R.base[2], a));
        const cb = Math.max(R.base[0], Math.min(R.base[2], b2));
        bpos[i*6] = ca; bpos[i*6+1] = -R.base[1]; bpos[i*6+2] = 0;
        bpos[i*6+3] = cb; bpos[i*6+4] = -R.base[1]; bpos[i*6+5] = 0;
        bA.a[i*2] = bA.a[i*2+1] = cb > ca ? 1 : 0;
      }
      bgeo.attributes.position.needsUpdate=true; bgeo.attributes.aA.needsUpdate=true;
      // 站点呼吸：四枚各自错峰（复盘→定位→迭代→训练 是一圈，不是四盏同时闪）
      for(let i=0;i<stT.length;i++) stA.a[i]=0.62+0.38*(0.5-0.5*Math.cos(TAU*(clock/3.2-i*0.25)));
      stGeo.attributes.aA.needsUpdate=true;
    },
    applyTheme(){
      bandMat.uniforms.uColor.value.copy(cssColor('--r-band'));
      bandMat.uniforms.uHot.value.copy(cssColor('--r-band'));
      bandMat.uniforms.uOpacity.value = cssNum('--r-band-op',.2);
      bandMat.uniforms.uGain.value = 0;
      // uBack 压到 .10：转到轴背后的那半圈几乎隐去 ⇒ 「绕着轴转」是看出来的
      [bandMat,railMat,axisMat].forEach(m=>{ m.uniforms.uBack.value = .10; });
      axisMat.uniforms.uColor.value.copy(cssColor('--r-rail'));
      axisMat.uniforms.uHot.value.copy(cssColor('--r-rail'));
      axisMat.uniforms.uOpacity.value = cssNum('--r-rail-op',.6)*.55;
      axisMat.uniforms.uGain.value = 0;
      railMat.uniforms.uColor.value.copy(cssColor('--r-rail'));
      railMat.uniforms.uHot.value.copy(cssColor('--r-node'));
      railMat.uniforms.uOpacity.value = cssNum('--r-rail-op',.6);
      railMat.uniforms.uGain.value = .5;
      baseMat.uniforms.uColor.value.copy(cssColor('--r-base'));
      baseMat.uniforms.uHot.value.copy(cssColor('--r-base'));
      baseMat.uniforms.uOpacity.value = cssNum('--r-base-op',.8);
      baseMat.uniforms.uGain.value = 0; baseMat.uniforms.uBack.value = .62;
      nodeMatR.uniforms.uColor.value.copy(cssColor('--r-node'));
      nodeMatR.uniforms.uHot.value.copy(cssColor('--r-node'));
      nodeMatR.uniforms.uOpacity.value = cssNum('--r-node-op',.95);
      nodeMatR.uniforms.uSize.value = cssNum('--r-node-size',7);
      nodeMatR.uniforms.uGain.value = 0;
      haloMatR.uniforms.uColor.value.copy(cssColor('--r-node'));
      haloMatR.uniforms.uHot.value.copy(cssColor('--r-node'));
      haloMatR.uniforms.uOpacity.value = cssNum('--r-node-op',1)*.26;
      haloMatR.uniforms.uSize.value = cssNum('--r-node-size',10)*2.6;
      haloMatR.uniforms.uGain.value = 0;
      sparkMat.uniforms.uColor.value.copy(cssColor('--r-spark'));
      sparkMat.uniforms.uHot.value.copy(cssColor('--r-spark'));
      sparkMat.uniforms.uOpacity.value = cssNum('--r-spark-op',.9);
      sparkMat.uniforms.uSize.value = cssNum('--r-spark-size',4.6);
      sparkMat.uniforms.uGain.value = 0;
      // LOOP 环带 + 站点圆（底色读 --r-fill：页上那四枚圆就是 card-bg-2 实心）
      // uBack 压到 .26：环平面一倾之后，下沿（远）明显暗下去 ⇒ 「这是一圈轨道」
      loopStr.theme(cssColor('--r-loop'), cssColor('--r-loop-rms'),
                    cssNum('--r-loop-op',.52), cssNum('--r-loop-rms-op',.55), .26);
      fillMat.uniforms.uColor.value.copy(cssColor('--r-fill'));
      fillMat.uniforms.uHot.value.copy(cssColor('--r-fill'));
      fillMat.uniforms.uOpacity.value = cssNum('--r-fill-op',1);
      fillMat.uniforms.uGain.value = 0; fillMat.uniforms.uBack.value = 1;
      ringNodeMat.uniforms.uColor.value.copy(cssColor('--r-node'));
      ringNodeMat.uniforms.uHot.value.copy(cssColor('--r-node'));
      ringNodeMat.uniforms.uOpacity.value = cssNum('--r-node-op',.95)*.8;
      ringNodeMat.uniforms.uGain.value = 0; ringNodeMat.uniforms.uBack.value = .62;
      [bandMat,railMat,axisMat,nodeMatR,haloMatR,sparkMat,baseMat,fillMat,ringNodeMat]
        .forEach(m=>setBlend(m,cssNum('--r-add',0)));
      setBlend(loopStr.mat, cssNum('--r-add',0));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑥ VAD 声学地形（P7 · 二轮精修 · 波B「消闪三件」）
   ───────────────────────────────────────────────────────────────────────────
   页上那条逐帧语音概率曲线**就是山脊线** —— 把它沿「帧」这个第二轴（深度 z）
   挤出去，能量检测从一条线变成一片地形。

   ── 终审：「色块闪动营造流动感是偷懒的欺骗」——要真流动 ────────────────────
   本页原来有两处**假流动**，两处都是「同一块像素反复变亮变暗」：
     ✕ 滞回面：uFlow = 0 ⇒ flow = .74 + .26·sin(−uTime)，整片**原地明灭**；
     ✕ 立柱帽子：逐帧改 alpha 呼吸。
   换掉它们的**消闪三件**：

   ① **地形整幅**按 A 档 110px/s 向左平移。要平移就得先**周期化**：页上那条曲线
      两端差 2px（y 118 → 116），把这 2px 沿全幅**线性摊掉** ⇒ 首尾的高度接得上、
      斜率也接得上（两端本来近乎水平，摊掉后斜率只差 2/980）。几何**建满两个周期**，
      每帧**只设 scroll.position.x** —— 一格顶点都不重算，闪的物理前提就不存在。
      一趟 980 ÷ 110 = **8.91s**，回卷点上第二周期与第一周期逐点相同 ⇒ 无缝。

   ② **理解光束驻位**在 SOS / EOS 两枚事件 x 上。判断在这里做过一次：
      SOS/EOS 的 DOM 标签钉死在 x=880/1380，而 P7 **不在版式分歧名单**里 ——
      于是取「滚动的是语音，钉住的是判定」，地形从两道光束下面穿过
      ⇒「实时馈送」与「标签不指空」同时成立。
      判定晕的半径是 gap / ons 两张**对材料坐标预计算**的表的连续函数：
        短谷 → 晕涨到一半就收回来；长谷 → 越过判定线，一边收细一边**凝成晶柱落地**。
      阈值只出现在构建期那两张表里；运行时是一路连续插值（节点处一阶导归零的
      smoothstep 内插）—— **零随机、零状态机、零阈值跳变**。

   ③ 语义层从「一条会飘的虚线」改成**贴着折脊走的连续流带**（lab-kit ⑨）
      + 一条**前沿馈送带**（声学的前沿在喂语义）。两条都坐在 scroll 组里，
      随地形一起走 ⇒ 它们的波峰速度就是 110px/s，不额外引入第二个速度。

   闸门：`⑲p7` 用 TOUR.pace 定拍 + **同 tick** gl.readPixels 逐帧量亮度突变
   （整幅上限 4.0/255、8×8 分块上限 26/255）。这一闸量的是「像素有没有跳」，
   不是「代码看起来对不对」。
   ═══════════════════════════════════════════════════════════════════════════ */
/* 滞回带专用片元：**去掉时间项**。共用的 PX_RB_FS 里那句
     flow = .74 + .26·sin((vT·uFlow − uTime·1.7)·2π)
   无论 uFlow 取多少都带着 uTime —— 那就是「整片原地明灭」的出处本人。
   这里换成只随 vT（空间）变的版本 ⇒ 判定面上一格像素都不再随时间抖，
   而且整页的渲染从此**只**通过 run 依赖时钟（run 严格周期）⇒ 回卷逐像素无缝。 */
const T_BAND_FS = [
  'uniform vec3 uColor,uHot; uniform float uOpacity,uBack,uGain,uIntro,uFlow;',
  'varying float vT,vA,vH,vFade;',
  'void main(){',
  '  float grow=clamp((uIntro*1.15-vT)/0.10,0.0,1.0);',
  '  float flow=0.80+0.20*sin(vT*uFlow*6.2831853);',
  '  float a=uOpacity*vA*mix(uBack,1.0,vFade)*grow*flow;',
  '  if(a<0.004) discard;',
  '  gl_FragColor=vec4(uColor,clamp(a,0.0,1.0));',
  '  #include <colorspace_fragment>',
  '}'].join('\n');
function makeTerrain(ctx){
  const T = K.t, w = ctx.rect[2], h = ctx.rect[3], D = 520;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, 95);
  const grp = new THREE.Group(); grp.position.set(0,-T.base,0); grp.rotation.x = T.tilt; scene.add(grp);
  /* scroll 组：**整幅**地形与两条语义带都坐在里面。每帧只动它的 position.x。 */
  const scroll = new THREE.Group(); grp.add(scroll);
  const NT = T.nt, PER = T.per, STEP = PER/(NT-1);
  /* 表取值：节点处一阶导归零的 smoothstep 内插 ⇒ C¹ 连续（线性内插在节点会有折角，
     折角在 8×8 分块的亮度差分上是看得见的一记）。u 先环回一个周期。 */
  function tab(a, u){
    let x = ((u - T.x0) % PER + PER) % PER / STEP;
    const i = Math.floor(x), f = x - i, g = f*f*(3-2*f);
    return a[i % (NT-1)]*(1-g) + a[(i+1) % (NT-1)]*g;
  }
  const crest = (x) => tab(T.hp, x);
  const NX = T.nx, NZ = T.nz, X0 = T.x0, X1 = T.x1, ZW = T.zw;
  const ridge = (z) => Math.exp(-(z*z)/(T.sig*T.sig));
  const hAt = (x,z) => (T.base - crest(x))*ridge(z);
  /* 采样区间：两个周期，再向两侧各外扩 4 格 —— scroll 走到 −980 时，
     可见窗口落在几何的 [979, 1989] 上，不外扩右缘会缺 10px（本轮实拍锤过）。
     第 i 与第 i+(NX−1) 个点整整差一个周期 ⇒ 回卷点上两周期逐点相同。 */
  const I0 = -4, I1 = (NX-1)*2 + 4, NX2 = I1 - I0 + 1;
  const xAt = (k) => X0 + (X1-X0)*(k + I0)/(NX-1);
  /* ── 地形：等深线（沿 x）+ 稀疏的横向筋（沿 z）—— 建满两个周期 ── */
  {
    const seg=[], al=[], hh=[];
    for(let r=0;r<NZ;r++){
      const z=-ZW+2*ZW*r/(NZ-1), aw=Math.pow(ridge(z),.55);
      for(let i=0;i<NX2-1;i++){
        const xa=xAt(i), xb=xAt(i+1);
        seg.push(xa,hAt(xa,z),z, xb,hAt(xb,z),z);
        al.push(aw,aw); hh.push(0,0);
      }
    }
    for(let i=0;i<NX2;i+=14){
      const x=xAt(i);
      for(let r=0;r<NZ-1;r++){
        const za=-ZW+2*ZW*r/(NZ-1), zb=-ZW+2*ZW*(r+1)/(NZ-1);
        const aw=Math.pow(ridge((za+zb)/2),.55)*.66;
        seg.push(x,hAt(x,za),za, x,hAt(x,zb),zb); al.push(aw,aw); hh.push(0,0);
      }
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(hh),1));
    var ridgeMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,ridgeMat); ln.frustumCulled=false; scroll.add(ln);
  }
  /* ── 脊线（z=0）：这一条就是页上那条概率曲线本人 ── */
  {
    const seg=[], al=[];
    for(let i=0;i<NX2-1;i++){
      const xa=xAt(i), xb=xAt(i+1);
      seg.push(xa,hAt(xa,0),0, xb,hAt(xb,0),0); al.push(1,1);
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    var crestMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,crestMat); ln.frustumCulled=false; scroll.add(ln);
  }
  /* ── 滞回带：两枚悬浮半透明面（y 取页上的上下阈值）──
     ⚠ 它**不在 scroll 组里**（判定线是钉住的），而且 uFlow 走**空间相位**：
     flow 只随 vT 变、不随 uTime 变 ⇒ 面上不再有「原地明灭」。 */
  const bandMats=[];
  T.band.forEach((by)=>{
    const y=T.base-by;
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array([
      X0,y,-ZW, X1,y,-ZW, X1,y,ZW, X0,y,ZW]),3));
    g.setAttribute('aT', new THREE.BufferAttribute(new Float32Array([0,.34,.67,1]),1));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array([1,1,1,1]),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(4),1));
    g.setIndex([0,1,2, 0,2,3]);
    const m = mkMat(SH, PX_RB_VS, T_BAND_FS, { uFlow:{value:3} });
    m.side = THREE.DoubleSide;
    const o=new THREE.Mesh(g,m); o.frustumCulled=false; grp.add(o);
    bandMats.push(m);
  });
  /* ═══ ② 理解光束（驻位）：束柱 + 判定晕 + 晶柱 ═══════════════════════════
     三件的形都由 gap / ons 两张表的连续函数给出；一格随机数都没有。 */
  const PIN = T.pins, NP = PIN.length, NR = 56;
  const beamMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const haloMat = mkMat(SH, PX_PT_VS, PX_PT_FS); haloMat.uniforms.uSoft.value = .30;
  const beamGeo2 = new THREE.BufferGeometry();
  const bSegs = NP*(2 + 4);                       // 每枚：2 根束柱 + 4 根晶柱棱
  const bpos = new Float32Array(bSegs*2*3);
  beamGeo2.setAttribute('position', new THREE.BufferAttribute(bpos,3));
  const bA = fillAH(beamGeo2, 1, 0);
  grp.add(Object.assign(new THREE.LineSegments(beamGeo2, beamMat), { frustumCulled:false }));
  const haloGeo = new THREE.BufferGeometry();
  const hpos = new Float32Array(NP*NR*3);
  haloGeo.setAttribute('position', new THREE.BufferAttribute(hpos,3));
  const hA = fillAH(haloGeo, 1, 0);
  grp.add(Object.assign(new THREE.Points(haloGeo, haloMat), { frustumCulled:false }));
  /* ═══ ③ 语义层：贴脊连续流带 + 前沿馈送带（两条都在 scroll 组里）═══════ */
  function ridgePts(dz, lift){
    const p = [];
    for(let i=0;i<NX2;i++){ const x=xAt(i); p.push([x, hAt(x, dz)+lift, dz]); }
    return p;
  }
  const sem  = mkStream(SH, ridgePts(0, 7), { w: T.semW, spd: 0, edge: 0 });
  const feed = mkStream(SH, ridgePts(T.feedZ, 2), { w: T.feedW, spd: 0, edge: 0 });
  scroll.add(sem.mesh); scroll.add(feed.mesh);
  /* 幅度剖面：语义带在**起声强的地方**厚、静音谷里收细；馈送带反过来 ——
     它是「前沿」，在起声之前先鼓起来。两条都只是一条 gain 回调，零分支。 */
  sem.gain((u) => 0.34 + 0.66*tab(T.ons, X0 + u));
  feed.gain((u) => 0.28 + 0.72*tab(T.ons, X0 + u + 46));
  let stepN = 0, semOp = .85, run = 0;
  return {
    scene, camera, intro:1.1, grab:false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    setStep(n){ stepN = n; },
    draw(dt, clock){
      SH.uTime.value = clock;
      /* ① 整幅左移：每帧**只**动这一个数。回卷点上第二周期与第一周期逐点相同。 */
      run = (clock*T.spd) % PER;
      scroll.position.x = -run;
      /* ② 判定晕 / 晶柱：材料坐标 = 屏上的驻位 + 已经滚过去的距离 */
      let b = 0, hq = 0;
      for(let i=0;i<NP;i++){
        const u = PIN[i] + run;
        const on = tab(T.ons, u), gp = tab(T.gap, u);
        const surf = hAt(u, 0), top = T.base - T.pinTop;
        // 判定晕：起声涨、长谷收（短谷 ⇒ 涨到一半就收回来）
        const R = T.halo[0] + T.halo[1]*on*(1 - T.halo[2]*gp);
        const hy = surf + (top-surf)*0.62;
        for(let k=0;k<NR;k++){
          const a = k/NR*TAU;
          hpos[hq*3]   = PIN[i] + Math.cos(a)*R;
          hpos[hq*3+1] = hy + Math.sin(a)*R*0.34;
          hpos[hq*3+2] = Math.sin(a)*R*0.9;
          hA.a[hq] = 0.34 + 0.66*(0.30 + 0.70*on)*(1 - 0.50*gp); hq++;
        }
        // 束柱：两根竖线（钉住的判定）
        for(let k=0;k<2;k++){
          const dx = (k?1:-1)*3.4;
          bpos[b*6]   = PIN[i]+dx; bpos[b*6+1] = surf;      bpos[b*6+2] = 0;
          bpos[b*6+3] = PIN[i]+dx; bpos[b*6+4] = top;       bpos[b*6+5] = 0;
          bA.a[b*2] = 0.55 + 0.45*on; bA.a[b*2+1] = 0.16 + 0.44*on; b++;
        }
        // 晶柱：长谷里越过判定线，一边收细一边落地
        const ph2 = T.pil[0]*gp, pw = T.pil[1]*(1 - T.pil[2]*gp);
        const py0 = surf, py1 = surf + ph2;
        [[-1,-1],[1,-1],[1,1],[-1,1]].forEach(([sx,sz]) => {
          bpos[b*6]   = PIN[i]+sx*pw; bpos[b*6+1] = py0; bpos[b*6+2] = sz*pw*1.2;
          bpos[b*6+3] = PIN[i]+sx*pw*0.42; bpos[b*6+4] = py1; bpos[b*6+5] = sz*pw*0.5;
          bA.a[b*2] = 0.86*gp; bA.a[b*2+1] = 0.20*gp; b++;
        });
      }
      beamGeo2.attributes.position.needsUpdate = true;
      beamGeo2.attributes.aA.needsUpdate = true;
      haloGeo.attributes.position.needsUpdate = true;
      haloGeo.attributes.aA.needsUpdate = true;
      // ③ 两条语义带：uRun 恒 0（波峰钉在材料上，由 scroll 带着走 ⇒ 只有一个速度）
      sem.draw(0); feed.draw(0);
      // data-step → uniform：第 1 步把语义层从「在场但很轻」推到「亮起来」
      const want = stepN>=1 ? semOp : semOp*0.26;
      const cu = sem.mat.uniforms.uOpacity;
      cu.value += (want-cu.value)*Math.min(1,dt*3.2);
      feed.mat.uniforms.uOpacity.value = cu.value*0.55;
    },
    state(){
      return { run, per: PER, spd: T.spd, lap: PER/T.spd, nt: NT,
               seam: T.hp[NT-1] - T.hp[0], scrollX: scroll.position.x,
               halo: PIN.map(x => T.halo[0] + T.halo[1]*tab(T.ons, x+run)
                                  *(1 - T.halo[2]*tab(T.gap, x+run))),
               gap: PIN.map(x => tab(T.gap, x+run)), ons: PIN.map(x => tab(T.ons, x+run)),
               semOp: sem.mat.uniforms.uOpacity.value };
    },
    applyTheme(){
      ridgeMat.uniforms.uColor.value.copy(cssColor('--t-ridge'));
      ridgeMat.uniforms.uHot.value.copy(cssColor('--t-crest'));
      ridgeMat.uniforms.uOpacity.value = cssNum('--t-ridge-op',.4);
      ridgeMat.uniforms.uGain.value = 0;
      ridgeMat.uniforms.uBack.value = .18;
      crestMat.uniforms.uColor.value.copy(cssColor('--t-prob'));
      crestMat.uniforms.uHot.value.copy(cssColor('--t-prob'));
      crestMat.uniforms.uOpacity.value = cssNum('--t-prob-op',.9);
      crestMat.uniforms.uGain.value = 0;
      crestMat.uniforms.uBack.value = .55;
      bandMats.forEach(m=>{
        m.uniforms.uColor.value.copy(cssColor('--t-band'));
        m.uniforms.uHot.value.copy(cssColor('--t-band'));
        m.uniforms.uOpacity.value = cssNum('--t-band-op',.13);
        m.uniforms.uGain.value = 0;
        /* T_BAND_FS 里 flow 只随 vT（**空间**）变：整片原地明灭那一档
           （PX_RB_FS 的 .74+.26·sin(−uTime·1.7)）在这一页彻底不存在。 */
        m.uniforms.uFlow.value = 3;
      });
      beamMat.uniforms.uColor.value.copy(cssColor('--t-pillar'));
      beamMat.uniforms.uHot.value.copy(cssColor('--t-pillar'));
      beamMat.uniforms.uOpacity.value = cssNum('--t-pillar-op',.75)*1.35;
      beamMat.uniforms.uGain.value = 0;
      haloMat.uniforms.uColor.value.copy(cssColor('--t-halo'));
      haloMat.uniforms.uHot.value.copy(cssColor('--t-halo'));
      haloMat.uniforms.uOpacity.value = cssNum('--t-halo-op',.55);
      haloMat.uniforms.uSize.value = cssNum('--t-halo-size',3);
      haloMat.uniforms.uGain.value = 0;
      semOp = cssNum('--t-sem-op',.85);
      sem.theme(cssColor('--t-sem'), cssColor('--t-sem-rms'),
                semOp, cssNum('--t-sem-rms-op',.55), .45);
      feed.theme(cssColor('--t-feed'), cssColor('--t-feed'),
                 cssNum('--t-feed-op',.45), .4, .45);
      [ridgeMat,crestMat,beamMat,haloMat,sem.mat,feed.mat].concat(bandMats)
        .forEach(m=>setBlend(m,cssNum('--t-add',0)));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑦ 全双工双向声带（P4）
   ───────────────────────────────────────────────────────────────────────────
   两条对向流动的 3D 声波 ribbon 在同一段空间里交错穿行 —— 你说的那条自左向右，
   它说的那条自右向左，**投影上反复交叠、深度上永不相撞**：这就是「同时说」
   的立体形（半双工里这两条带子只能轮流出现）。交叠区高亮。
   x=1080 那根竖线（页上「用户插话 = TTS 截断 = 340ms 快路径」的三带共用垂线）
   仍是这一页的转折点：过了它，「它说」那条带子掉成一缕虚影 —— 收声让位。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeDuplex(ctx){
  const Q = K.d, w = ctx.rect[2], h = ctx.rect[3], D = 1400;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, 88);
  const N = 320;
  function lane(sign, phase){
    const out=[];
    for(let i=0;i<N;i++){
      const u=i/(N-1), x=Q.x0+(Q.x1-Q.x0)*u, th=TAU*Q.turns*u+phase;
      out.push([x, -(Q.yc - sign*Q.amp*Math.cos(th)), sign*Q.dep*Math.sin(th)]);
    }
    return out;
  }
  const A = lane( 1, 0), B = lane(-1, Q.phase);
  // 交叠：两条带在投影上靠得多近（|yA-yB|）—— 高亮由它驱动，不是随手点几处
  const lap=[];
  for(let i=0;i<N;i++){
    const d=Math.abs(A[i][1]-B[i][1]);
    lap.push(Math.max(0,Math.min(1,(Q.lap1-d)/(Q.lap1-Q.lap0))));
  }
  function band(P, hw, cut){
    const g = ribbonGeo(P, ()=>hw);
    const n = g.attributes.position.count;
    const a=new Float32Array(n), hgt=new Float32Array(n);
    for(let i=0;i<N;i++){
      const x=P[i][0];
      const k = cut && x>Q.cut ? Q.ghost : 1;
      a[i*2]=a[i*2+1]=k; hgt[i*2]=hgt[i*2+1]=lap[i];
    }
    g.setAttribute('aA', new THREE.BufferAttribute(a,1));
    g.setAttribute('aH', new THREE.BufferAttribute(hgt,1));
    const m = mkMat(SH, PX_RB_VS, PX_RB_FS, { uFlow:{value:cut?-6:6} });
    m.side = THREE.DoubleSide;
    const o=new THREE.Mesh(g,m); o.frustumCulled=false; scene.add(o);
    return m;
  }
  const matA = band(A, Q.hw, false), matB = band(B, Q.hw*0.86, true);
  /* ── 截断标记：x=1080 的那根竖线（页上三条泳道共用的那一根）── */
  var cutMat;
  {
    const seg=[], al=[];
    for(let s=0;s<12;s++){
      const y0=-(Q.cy0+(Q.cy1-Q.cy0)*s/12), y1=-(Q.cy0+(Q.cy1-Q.cy0)*(s+1)/12);
      if(s%2) continue;
      seg.push(Q.cut,y0,0, Q.cut,y1,0); al.push(1,1);
    }
    const g=new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(seg),3));
    g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(al),1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    cutMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ln=new THREE.LineSegments(g,cutMat); ln.frustumCulled=false; scene.add(ln);
  }
  /* ── 包粒子：沿各自的带反向流（它说那一路到截断点就没有了）── */
  const PA=10, PB=8, pkGeo=new THREE.BufferGeometry();
  const pkPos=new Float32Array((PA+PB)*3);
  pkGeo.setAttribute('position', new THREE.BufferAttribute(pkPos,3));
  const pkA = attrAH(pkGeo, PA+PB, 1, 1);
  const pkMat = mkMat(SH, PX_PT_VS, PX_PT_FS); pkMat.uniforms.uSoft.value=.03;
  const pks = new THREE.Points(pkGeo, pkMat); pks.frustumCulled=false; scene.add(pks);
  const cutU = (Q.cut-Q.x0)/(Q.x1-Q.x0);

  return {
    scene, camera, intro:1.2, grab:false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      let n=0;
      for(let i=0;i<PA;i++){
        let u=((clock/Q.durA)+i/PA)%1;
        const j=Math.min(N-2,Math.floor(u*(N-1))), fu=u*(N-1)-j;
        pkPos[n*3]=A[j][0]+(A[j+1][0]-A[j][0])*fu;
        pkPos[n*3+1]=A[j][1]+(A[j+1][1]-A[j][1])*fu;
        pkPos[n*3+2]=A[j][2]+(A[j+1][2]-A[j][2])*fu;
        pkA.a[n]=Math.min(1,Math.min(u,1-u)*9); n++;
      }
      for(let i=0;i<PB;i++){
        let u=1-(((clock/Q.durB)+i/PB)%1);           // 反向：从右往左
        const j=Math.min(N-2,Math.floor(u*(N-1))), fu=u*(N-1)-j;
        pkPos[n*3]=B[j][0]+(B[j+1][0]-B[j][0])*fu;
        pkPos[n*3+1]=B[j][1]+(B[j+1][1]-B[j][1])*fu;
        pkPos[n*3+2]=B[j][2]+(B[j+1][2]-B[j][2])*fu;
        pkA.a[n]=Math.min(1,Math.min(u,1-u)*9)*(u>cutU?Q.ghost:1); n++;
      }
      pkGeo.attributes.position.needsUpdate=true; pkGeo.attributes.aA.needsUpdate=true;
    },
    applyTheme(){
      matA.uniforms.uColor.value.copy(cssColor('--d-up'));
      matA.uniforms.uHot.value.copy(cssColor('--d-lap'));
      matA.uniforms.uOpacity.value = cssNum('--d-up-op',.6);
      matA.uniforms.uGain.value = 1.1;
      matB.uniforms.uColor.value.copy(cssColor('--d-dn'));
      matB.uniforms.uHot.value.copy(cssColor('--d-lap'));
      matB.uniforms.uOpacity.value = cssNum('--d-dn-op',.5);
      matB.uniforms.uGain.value = 1.1;
      cutMat.uniforms.uColor.value.copy(cssColor('--d-cut'));
      cutMat.uniforms.uHot.value.copy(cssColor('--d-cut'));
      cutMat.uniforms.uOpacity.value = cssNum('--d-cut-op',.75);
      cutMat.uniforms.uGain.value = 0;
      pkMat.uniforms.uColor.value.copy(cssColor('--d-pkt'));
      pkMat.uniforms.uHot.value.copy(cssColor('--d-pkt'));
      pkMat.uniforms.uOpacity.value = cssNum('--d-pkt-op',.9);
      pkMat.uniforms.uSize.value = cssNum('--d-pkt-size',4.4);
      pkMat.uniforms.uGain.value = 0;
      [matA,matB,cutMat,pkMat].forEach(m=>setBlend(m,cssNum('--d-add',0)));
    },
  };
}


/* ═══════════════════════════════════════════════════════════════════════════
   lab-kit ⑤ · 第二波套件（九页共用）
   ───────────────────────────────────────────────────────────────────────────
   第二波的九页与第一波的五页有一处根本差别：**这九页的图上全是标签**。
   盒子上压着名字、车道上压着注、握手线上压着序号 —— 一旦 3D 把形挪了半格，
   页上的字就指空了。所以本波的地基件是「投影锁」：

     lockPx —— 把页上的 2D 点 (x,y) 抬到深度 z，再按 (D−z)/D 预缩放；
               透视除法把这一档缩放正好除回去 ⇒ **投影落点与 2D 逐像素相同**。

   于是「有真深度」与「标签一格不挪」不再互斥：
     · 深度雾（uNear/uFar）、点径随 1/z、前后遮挡、包在深度里穿行 —— 立体线索全在；
     · 盒的**前面**锁死在页上那只盒的位置，后面沿 −z 退进去（extrudeBack）
       ⇒ 看得见四面侧壁，而正面轮廓与它替换掉的那只 SVG 盒逐像素重合。
   这条纪律是 P10 大图（谨慎页）能上 3D 的**全部前提**，其余八页照用。
   ═══════════════════════════════════════════════════════════════════════════ */
function mkLock(w, h, D){
  const cx = w / 2, cy = h / 2;
  return function(x, y, z){
    const k = (D - (z || 0)) / D;
    return [cx + (x - cx) * k, -(cy + (y - cy) * k), (z || 0)];
  };
}
function fillAH(g, a0, h0){
  return attrAH(g, g.attributes.position.count, a0 === undefined ? 1 : a0, h0 || 0);
}
function segGeo(pairs){                       // [[x1,y1,z1,x2,y2,z2], …] → LineSegments
  const pos = new Float32Array(pairs.length * 6);
  for(let i = 0; i < pairs.length; i++) for(let k = 0; k < 6; k++) pos[i*6+k] = pairs[i][k];
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  return g;
}
function stripGeo(pts){                       // 一条折线 → Line
  const pos = new Float32Array(pts.length * 3);
  for(let i = 0; i < pts.length; i++){ pos[i*3]=pts[i][0]; pos[i*3+1]=pts[i][1]; pos[i*3+2]=pts[i][2]; }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  return g;
}
function ptsGeo(pts){                         // 一批点 → Points
  return stripGeo(pts);
}
function rectPts(x, y, w, h, z, L){           // 页上一只矩形的四角（闭合 · 投影锁）
  return [L(x,y,z), L(x+w,y,z), L(x+w,y+h,z), L(x,y+h,z), L(x,y,z)];
}
/* 实心面：页上有些「形」是**填实**的（P3 那三张小图里「谁在说」就是一块实心带）——
   只画线框会把语义讲弱一档。两枚三角 + PX_LN 那对着色器（它只输出平色，网格照用）。 */
function quadGeo(p){
  const pos = new Float32Array(12);
  for(let i = 0; i < 4; i++){ pos[i*3]=p[i][0]; pos[i*3+1]=p[i][1]; pos[i*3+2]=p[i][2]; }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos,3));
  g.setIndex([0,1,2, 0,2,3]);
  return g;
}
function segsOfLoop(pts){                     // 闭合折线 → 线段表
  const e = [];
  for(let i = 0; i < pts.length - 1; i++)
    e.push([pts[i][0],pts[i][1],pts[i][2], pts[i+1][0],pts[i+1][1],pts[i+1][2]]);
  return e;
}
/* 背向拉伸：前面锁死、后面沿 −z 退 dz。后面直接取前面的 xy 换 z ——
   透视把它按 (D−z0)/(D−z0+dz) 收小，四面侧壁自然出现，正面轮廓一格不动。 */
function extrudeBack(x, y, w, h, z0, dz, L){
  const f = rectPts(x, y, w, h, z0, L);
  const b = f.map(p => [p[0], p[1], z0 - dz]);
  const e = [];
  for(let i = 0; i < 4; i++) e.push([f[i][0],f[i][1],f[i][2], b[i][0],b[i][1],b[i][2]]);
  return { front: f, back: b, edges: e, segs: segsOfLoop(f).concat(segsOfLoop(b), e) };
}
/* 一枚「盒体」：前框（亮）+ 后框与棱（暗）—— 两套材质，深度层次一眼分得开 */
function boxBody(x, y, w, h, z0, dz, L){
  const f = segsOfLoop(rectPts(x, y, w, h, z0, L));
  const ex = extrudeBack(x, y, w, h, z0, dz, L);
  return { front: f, shell: segsOfLoop(ex.back).concat(ex.edges) };
}
/* 页上 .mo-packet 的**占空比模型**（第二波九页与页面 CSS 共用同一套参数）：
     dasharray = "seg ln"，一个周期 T 内 dash 图案正好平移 (seg+ln) ⇒
     一枚包在长为 Lp 的路径上「在途」的时间占比 = (Lp + seg) / (seg + ln)。
   ln === Lp ⇒ 占空比 1（恒在途）；ln ≫ Lp ⇒ 包只在周期的一小段里出现。
   P3 半双工的严格互斥就是靠这一条 + 半周期相位差静态成立的。 */
function dutyOf(Lp, ln, seg){ return (Lp + (seg||14)) / ((seg||14) + ln); }
function flightU(clock, T, off, duty){        // 返回 [0,1] 的在途参数；不在途返回 −1
  let p = ((clock - off) / T) % 1; if(p < 0) p += 1;
  if(duty >= 0.999) return p;                 // 占空比 1 ⇒ 恒在途
  const u = p / duty;
  return u <= 1 ? u : -1;
}

/* ═══════════════════════════════════════════════════════════════════════════
   lab-kit ⑨ · audioStream —— 连续媒体流原语（二轮精修 · 波A 的地基件）
   编号与「接入指南第 ⑨ 条」对齐：那一条讲**什么时候**该用它，这一段是它本人。
   ───────────────────────────────────────────────────────────────────────────
   病根一句话：**点状移动不是数据流**。一串沿着线挪的球讲的是「有几个包」，
   不是「一直在来」；音频、语音、token、媒体帧全是**介质**，介质必须是一条
   有厚度、会起伏、**波峰自己往前走**的带子。

   三件事让它像 Audition 里的声波，而不是锯齿：
     ① **解析包络**（不是逐柱采样）：en = .5 + .5·Σaᵢsin(2π·fᵢ·(u−run)/λ + φᵢ)。
        Σaᵢ = 1 ⇒ en 恒 ∈ [0,1] 恒非负，**数学上不可能有角**（abs(sin) 不行：
        它在零点是尖的）。旧版逐柱高度表 + 线性插值，每根柱的边界都是一处斜率
        突变 —— 那就是「像锯齿」的病本人，磨多少下都还在。
     ② **波峰自己走**：相位里的 u = aT − uRun，uRun = 流速 × 时钟（px）。
        微粒纹理（grain）用**同一个 u** ⇒ 纹理与波峰同速；不同速会被眼睛读成
        「带子没动、只是在闪」，那正是要治的病。
     ③ **两层**：峰值淡壳 + 内层 RMS 实芯（uComp）。只画一层就只是一条会抖的带子。

   第二语义通道 **aG**（幅度剖面的唯一入口）：
       amp = mix(uGhost, 1, aG)   幅度落到 ghost 档
       dyn = mix(1,      en, aG)  **包络一起平掉**
     ⇒ aG→0 得到的是一条**真细线**，不是「小一点的波」。P8 的 200ms 让位、
       P6 的过站收窄与由稀到密，因此全部只是一条 gain 回调，**零分支代码**。

   写一条流四步（接入指南 ⑨）：
       mkStream(SH, pts, opt) → .add(scene) → .theme(峰值色, RMS色, op, rmsOp, uBack)
       → 把速度写进 _spd_of()（Python 侧 _spd_rows，摊进 data-lab-spd 供 ⑲s 复算）
   ═══════════════════════════════════════════════════════════════════════════ */
const AS = K.as;

const AS_VS = [
  'uniform float uIntro,uTime,uNear,uFar,uRun,uLam,uFloor,uGhost,uLen,uW;',
  'uniform vec4 uA,uF,uPh;',
  'attribute vec3 aN; attribute float aV,aW,aT,aG;',
  'varying float vT,vV,vEn,vG,vFade,vU;',
  // 四枚谐波叠加 —— 权重和为 1 ⇒ 结果恒在 [0,1]，恒非负，C^∞
  'float envAt(float u){',
  '  float k = 6.2831853 / uLam;',
  '  return 0.5 + 0.5*( uA.x*sin(k*uF.x*u + uPh.x) + uA.y*sin(k*uF.y*u + uPh.y)',
  '                   + uA.z*sin(k*uF.z*u + uPh.z) + uA.w*sin(k*uF.w*u + uPh.w) );',
  '}',
  'void main(){',
  '  float u = aT - uRun;',                       // 波峰自己往前走
  '  float en = envAt(u);',
  '  float g  = clamp(aG, 0.0, 1.0);',
  '  float amp = mix(uGhost, 1.0, g);',           // ← 第二语义通道：幅度
  '  float dyn = mix(1.0, en, g);',               // ← 第二语义通道：包络一起平掉
  '  float grow = clamp((uIntro*1.12 - aT/uLen)/0.10, 0.0, 1.0);',
  '  float hw = aW*uW*(uFloor + (1.0-uFloor)*dyn)*amp*grow;',
  '  vec3 p = position + aN*(aV*hw);',
  '  vec4 mv = modelViewMatrix*vec4(p,1.0);',
  '  float z = max(-mv.z, 1.0);',
  '  vFade = clamp((uFar-z)/(uFar-uNear), 0.0, 1.0);',
  '  vT=aT/uLen; vV=aV; vEn=en; vG=g; vU=u;',
  '  gl_Position = projectionMatrix*mv;',
  '}'].join('\n');

const AS_FS = [
  'uniform vec3 uColor,uRms; uniform float uOpacity,uRmsOp,uBack,uEdge,uCrest,uComp,uGrain,uGrainL;',
  'varying float vT,vV,vEn,vG,vFade,vU;',
  // 一维值噪声：微粒纹理（确定性 · 不吃随机源）
  'float h11(float p){ p = fract(p*0.1031); p *= p + 33.33; p *= p + p; return fract(p); }',
  'float n11(float x){ float i = floor(x), f = fract(x); f = f*f*(3.0-2.0*f);',
  '  return mix(h11(i), h11(i+1.0), f); }',
  'void main(){',
  '  float av = abs(vV);',
  // 内层 RMS 实芯（Audition 的波形是「峰值淡壳 + RMS 实芯」两层）
  '  float core = 1.0 - smoothstep(uComp-0.08, uComp+0.08, av);',
  '  vec3 col = mix(uColor, uRms, core*uRmsOp);',
  '  float a = uOpacity*mix(1.0, 1.0+uRmsOp*0.35, core);',
  '  a *= 1.0 + uCrest*(vEn-0.5)*2.0;',                       // 波峰亮度增益
  '  a *= 1.0 + uGrain*(n11(vU/uGrainL)-0.5)*2.0;',           // 微粒：与波峰同速
  '  a *= smoothstep(0.0, uEdge, vT)*smoothstep(0.0, uEdge, 1.0-vT);',   // 接头渐显渐隐
  '  a *= mix(uBack, 1.0, vFade);',
  '  if(a < 0.004) discard;',
  '  gl_FragColor = vec4(col, clamp(a, 0.0, 1.0));',
  '  #include <colorspace_fragment>',
  '}'].join('\n');

/* 一条流的几何：中心折线 + 面内法向 + 逐点半宽 —— 横向位移在 VS 里现算
   （包络每帧都在变，几何不能烘死）。aT 是沿流的**像素**弧长 ⇒ λ 是真的 px。 */
function streamGeo(pts, halfW){
  const n = pts.length;
  const pos = new Float32Array(n*2*3), nrm = new Float32Array(n*2*3);
  const av = new Float32Array(n*2), aw = new Float32Array(n*2);
  const at = new Float32Array(n*2), ag = new Float32Array(n*2).fill(1);
  let acc = 0;
  for(let i = 0; i < n; i++){
    const p = pts[i], q = pts[Math.min(n-1, i+1)], r = pts[Math.max(0, i-1)];
    let tx = q[0]-r[0], ty = q[1]-r[1], tz = q[2]-r[2];
    const tl = Math.hypot(tx, ty, tz) || 1; tx/=tl; ty/=tl; tz/=tl;
    let nx = ty, ny = -tx, nz = 0;                  // 带面朝向观众（媒体流是「看得见幅度」的）
    const nl = Math.hypot(nx, ny, nz) || 1; nx/=nl; ny/=nl; nz/=nl;
    if(i > 0) acc += Math.hypot(p[0]-pts[i-1][0], p[1]-pts[i-1][1]);
    const w = typeof halfW === 'function' ? halfW(i/(n-1), acc) : halfW;
    for(let k = 0; k < 2; k++){
      const j = i*2+k;
      pos[j*3]=p[0]; pos[j*3+1]=p[1]; pos[j*3+2]=p[2];
      nrm[j*3]=nx;  nrm[j*3+1]=ny;  nrm[j*3+2]=nz;
      av[j] = k ? -1 : 1; aw[j] = w; at[j] = acc;
    }
  }
  const idx = [];
  for(let i = 0; i < n-1; i++){ const a = i*2; idx.push(a,a+1,a+2, a+1,a+3,a+2); }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos,3));
  g.setAttribute('aN', new THREE.BufferAttribute(nrm,3));
  g.setAttribute('aV', new THREE.BufferAttribute(av,1));
  g.setAttribute('aW', new THREE.BufferAttribute(aw,1));
  g.setAttribute('aT', new THREE.BufferAttribute(at,1));
  g.setAttribute('aG', new THREE.BufferAttribute(ag,1));
  g.setIndex(idx);
  g.userData.len = acc || 1;
  return g;
}

/* mkStream —— 一条连续媒体流。opt：
     w    基准半宽（px 或 (t, uPx)=>px）
     spd  流速（px/s · A 档 110 ±30%；周期由 Python 侧「长 ÷ 速」反推）
     lam  波长（默认 AS.lam = 232px ⇒ 配 110px/s 恰好 2.11s 一次呼吸） */
function mkStream(SH, pts, opt){
  const o = opt || {};
  const geo = streamGeo(pts, o.w === undefined ? 10 : o.w);
  const n = pts.length;
  const mat = mkMat(SH, AS_VS, AS_FS, {
    uRun:{value:0}, uLam:{value:o.lam || AS.lam}, uLen:{value:geo.userData.len},
    uFloor:{value:o.floor === undefined ? AS.floor : o.floor},
    // ghost 也开成 opt（默认值 = 全局档 ⇒ 别的页一个像素不变）：带子瘦一档的页面，
    // 让位那条细线不能跟着瘦没 —— 「流不断」是纪律，不是这一页的手感。
    uGhost:{value:o.ghost === undefined ? AS.ghost : o.ghost},
    uEdge:{value:o.edge === undefined ? AS.edge : o.edge},
    uCrest:{value:AS.crest}, uComp:{value:AS.comp},
    uGrain:{value:AS.grain}, uGrainL:{value:AS.grainL}, uW:{value:1},
    uRms:{value:new THREE.Color()}, uRmsOp:{value:1},
    uA:{value:new THREE.Vector4(AS.a[0],AS.a[1],AS.a[2],AS.a[3])},
    uF:{value:new THREE.Vector4(AS.f[0],AS.f[1],AS.f[2],AS.f[3])},
    uPh:{value:new THREE.Vector4(AS.ph[0],AS.ph[1],AS.ph[2],AS.ph[3])} });
  mat.side = THREE.DoubleSide;
  const mesh = new THREE.Mesh(geo, mat); mesh.frustumCulled = false;
  const aG = geo.attributes.aG, aT = geo.attributes.aT;
  const spd = o.spd === undefined ? AS.spd : o.spd;
  let gainFn = null, gained = false;
  return {
    mat, mesh, geo, spd, len: geo.userData.len,
    add(sc){ sc.add(mesh); return this; },
    /* 幅度剖面的**唯一**入口：fn(u_px, clock) → 0..1。不写分支代码。 */
    gain(fn){ gainFn = fn; gained = false; return this; },
    /* 峰值色 / RMS 色 / 两档不透明度 / 深度雾底 —— 色号一律来自调用方读的 CSS 变量 */
    theme(peak, rms, op, rmsOp, back){
      mat.uniforms.uColor.value.copy(peak);
      mat.uniforms.uRms.value.copy(rms || peak);
      mat.uniforms.uOpacity.value = op;
      mat.uniforms.uRmsOp.value = rmsOp === undefined ? 1 : rmsOp;
      if(back !== undefined) mat.uniforms.uBack.value = back;
      return this;
    },
    width(w){ mat.uniforms.uW.value = w; return this; },
    draw(clock){
      mat.uniforms.uRun.value = spd * clock;
      if(!gainFn) return;
      const st = gainFn.length < 2;                // 只吃 u ⇒ 静态剖面，算一次就够
      if(st && gained) return;
      for(let i = 0; i < n; i++){
        const g = gainFn(aT.array[i*2], clock);
        aG.array[i*2] = aG.array[i*2+1] = g;
      }
      aG.needsUpdate = true; gained = true;
    },
  };
}

/* ── mkBeamMat · 离散事件的**管腔注光** ──────────────────────────────────
   三个点没有「到达」这个动作。光束生长有头、有尾、走过留痕：
   注光头以 uHead（px，沿路由的弧长）前进，头前是余光档 uRest、头后是全亮，
   头本身用一枚高斯亮斑（uFeather 宽）。几何只要带 aT（px 弧长）即可。 */
const AS_BEAM_VS = PX_HEAD + [
  'uniform float uHead,uFeather,uRest;',
  'attribute float aT;',
  'void main(){',
  '  float lit = 1.0 - smoothstep(uHead-uFeather, uHead, aT);',
  '  vA = aA*mix(uRest, 1.0, lit);',
  '  float d = (aT-uHead)/uFeather;',
  // vH = 注光头那一枚亮斑：进 PX_LN_FS 的 mix(uColor,uHot,vH) 与 (1+uGain*vH)
  '  vH = clamp(aH + exp(-d*d), 0.0, 1.0);',
  '  vec4 mv = pxCore(position, 1.0);',
  '  gl_Position = projectionMatrix*mv;',
  '}'].join('\n');
function mkBeamMat(SH, feather, rest){
  // ⚠ extra 里**不许**再出现 uHot / uColor / uGain —— 那几枚是 mkMat 的颜色档
  //   （本轮踩过：uHot 被一个 float 覆盖，materials 全场 boot 失败）。
  return mkMat(SH, AS_BEAM_VS, PX_LN_FS,
               { uHead:{value:0}, uFeather:{value:feather || 26},
                 uRest:{value:rest === undefined ? .28 : rest} });
}
/* 一条路由 → 带 aT（像素弧长）的线几何，喂给 mkBeamMat */
function beamGeo(pts){
  const g = stripGeo(pts), n = pts.length, t = new Float32Array(n);
  for(let i = 1; i < n; i++)
    t[i] = t[i-1] + Math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1],
                               pts[i][2]-pts[i-1][2]);
  fillAH(g, 1, 0);
  g.setAttribute('aT', new THREE.BufferAttribute(t,1));
  g.userData.len = t[n-1] || 1;
  return g;
}

/* ── mkRelock · 换相机不换观感 ──────────────────────────────────────────
   camPx 下一点 (x,y,z) 的投影放大率 k = D/(D−z)。令 z₁ = z₀·D₁/D₀ ⇒
       D₁/(D₁−z₁) = D₀/(D₀−z₀) = k  且  x,y 不动
   ⇒ **投影落点逐像素不变**；点径 sz·uD/(D−z) 也同步不变（uD 一起换）。
   深度雾半程按同一比例放大即可。于是「为 D₀ 拍板过的形」可以整个搬到 D₁ 上，
   一个像素都不挪 —— P18 的螺旋因此能在换到 D1500（为了把隔壁的 LOOP 环带
   收进视场）之后仍是原来那条螺旋。 */
function mkRelock(c0, D0, c1, D1){
  // 舞台**中心**也可能一起换（P18：1240 宽 → 1680 宽 ⇒ cx 620 → 840）。
  // 屏点 S = c0 + (p−c0)·k；要在新相机下还落在 S 上，解出
  //     p₁ = p₀ + (c1−c0)·z₀/D₀      （k 与上式同 ⇒ z₁ = z₀·D₁/D₀）
  const s = D1/D0, dx = c1[0]-c0[0], dy = c1[1]-c0[1];
  const P = (q) => [q[0] + dx*q[2]/D0, q[1] + dy*q[2]/D0, q[2]*s];
  return {
    s, half(h){ return h*s; }, p:P,
    geo(g){ const a = g.attributes.position.array;
      for(let i = 0; i < a.length; i += 3){
        const q = P([a[i], a[i+1], a[i+2]]);
        a[i] = q[0]; a[i+1] = q[1]; a[i+2] = q[2];
      }
      g.attributes.position.needsUpdate = true; return g; },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑧ 模态转换剧场（P2 · 二轮精修 · 波B · 王冠一）
   ───────────────────────────────────────────────────────────────────────────
   Colin 的方向：「拆解人类在对话里如何做**模态转换**——听、想、说。从你的高维
   去拆解这个理念，不用惧怕人类看不懂。」于是这一页不画流程环，画**同一段东西
   换了三次形态**：

     听 = 入射声波场   等相位线**竖直**的行波（相位只由 x 决定），波长逐字取
                       `K.as.lam` = 232px ⇒ 与 lab-kit ⑨ 的流带**是同一种介质**；
     ↓ 升维
     想 = 表征星格     34×12×5 点阵被两道正交折叠函数揉成一片流形，内部一道
                       从中心往外传的**位移**涟漪 —— 「理解」是几何变换，不是黑盒；
     ↓ 凝聚
     说 = 塌回波场     整片向右倾泻**出画**（出射波场的右端越过舞台右缘）。

   无缝三件（这是「不闪、不跳、不接头」的全部理由）：
     ① **一套顶点、一次插值**：三态是同一批顶点的三个解析目标，顶点着色器按
        (wIn,wLat,wOut) 线性插值，权重和恒为 1 —— 没有第二套几何，也就没有交接。
     ② **四道相位边界走 smootherstep**：一阶与二阶导数在边界都归零 ⇒ 速度与
        加速度都接得上（smoothstep 只保证一阶，形上会有一记可察觉的「顿」）。
     ③ **生灭窗**：uLife 在 12.80→13.60 落到 0、13.60–14.00 全暗，t 回卷（换位置）
        永远发生在这 0.4s 里 —— 接头藏在画外，形上零跳变。
   **两代同场**（相位差半周期 7s）：舞台永不空；而这正是页上
   「同一时刻 · 并行进行 / 持续在听 · 同时在说」两行落点句本人 ——
   任何一刻台上都有两种形态并行，其中每 7s 有一段是「一代在听 · 一代在说」。
   ⇒ **舞台视觉周期 = 7s**（两代互换即回到同一张画），GIF 录 7s 就含
     波→格 与 格→波 两处变形；单代走完 14s。

   高维巧思：**第二道入射波**沿页上那条反馈弧 `_P2ARC` 切进来（3D 里它是一条真的
   audioStream —— 同一种介质，不是装饰线），到达舞台左缘的那一刻，台上的格架在
   **0.56s** 内整片转过 uYaw 让位，其后 **3.10s** 慢慢回正。让位是「转身让路」，
   不是「消失」—— 所以它读得出是两件事在同一个空间里相互避让。

   ── 02 · SAME MOMENT「两制对照」（表达力精进 · 第一波 ① · 2026-09-02）────────
   同一枚场景往下长 238px（相机 setViewOffset，剧场投影一格不动），多出来那一带
   画两排 audioStream —— 与剧场**同介质**（同一枚 lab-kit ⑨ · λ232 · A 档流速）、
   **同分量**（整幅两排，不是 900×58 的灰注脚条）：
     上排 回合制 ✕：一条流 + 一条 gain 剖面 ⇒ 听 / 说是实带，之间落 ghost 档
       （空档 = 真细线，零分支）；「想」不是媒体 ⇒ 一只虚线框；
       说段中一枚事件标，**带子一格不让位**。
     下排 边说边听：听 / 想 / 说三条并行连续带（想走低幅 gain .6），说带从 22% 起；
       在**同一根竖线上**（同一时刻）200px 弧长内落 ghost 让位，随后接回。
   两排的事件必须共用同一个 x —— 不共用，「同一时刻两种反应」这个对照就不成立。
   ═══════════════════════════════════════════════════════════════════════════ */
const MO = K.o;
const _gf = (x) => (+x).toFixed(4);          // GLSL 浮点字面量（几何常量只有 K.o 一份）
/* MO_HEAD —— waveAt / latAt 的**唯一**实现（构建期 _mo_wave/_mo_lat 与它逐行同式）。
   所有几何常量从 K.o 现取现烘：想改形，改 _MO_* 一处，poster 与着色器一起动。 */
const MO_HEAD = [
  'uniform float uT,uRunA,uRunB,uYaw,uLife,uWIn,uWLat,uWOut;',
  'uniform vec4 uA,uF,uPh;',
  'const float TAU = 6.28318530718;',
  'float moS(float th){',
  '  return uA.x*sin(uF.x*th+uPh.x) + uA.y*sin(uF.y*th+uPh.y)',
  '       + uA.z*sin(uF.z*th+uPh.z) + uA.w*sin(uF.w*th+uPh.w);',
  '}',
  // ── 入射 / 出射声波场：等相位线竖直（相位只由 x 决定）──
  'float moWaveX(float u,float o){ return ' + _gf(MO.x0) + ' + o*' + _gf(MO.outdx)
    + ' + (' + _gf(MO.x1) + '-' + _gf(MO.x0) + ')*u; }',
  'vec3 waveAt(float u,float v,float w,float o,float run){',
  '  float x  = moWaveX(u,o);',
  '  float ny = (v-0.5)*2.0, nz = (w-0.5)*2.0;',
  '  float amp = ' + _gf(MO.amp) + '*(1.0-0.62*abs(ny));',
  '  float y = ' + _gf(MO.yc) + ' + ny*' + _gf(MO.hw)
    + ' + amp*moS(TAU*(x-run)/' + _gf(K.as.lam) + ');',
  '  return vec3(x, y, nz*' + _gf(MO.dz * 0.5) + ');',
  '}',
  'float moEnv(float u,float o,float run){',
  '  return 0.5+0.5*moS(TAU*(moWaveX(u,o)-run)/' + _gf(K.as.lam) + ');',
  '}',
  // ── 表征星格：两道正交折叠 + 深度隆起 + 中心往外传的位移涟漪 + 让位偏航 ──
  'vec3 latAt(float u,float v,float w){',
  '  float p = (u-0.5)*' + _gf(MO.lw) + ', q = (v-0.5)*' + _gf(MO.lh)
    + ', r = (w-0.5)*' + _gf(MO.ld) + ';',
  '  float X = p + ' + _gf(MO.f1 * MO.lw * 0.5) + '*sin(TAU*(q/' + _gf(MO.lh) + ')+r*0.012);',
  '  float Y = q + ' + _gf(MO.f2 * MO.lh * 0.5) + '*sin(TAU*1.5*(p/' + _gf(MO.lw) + '));',
  '  float Z = r + ' + _gf(MO.fb) + '*cos(TAU*(p/' + _gf(MO.lw) + '+q/' + _gf(MO.lh) + '));',
  '  float d = length(vec2(X,Y)) + 1e-3;',
  '  float rp = ' + _gf(MO.rip) + '*sin(TAU*(d/' + _gf(MO.rlam) + ' - uT/' + _gf(MO.rper) + '));',
  '  X += rp*X/d; Y += rp*Y/d;',
  '  float cs = cos(uYaw), sn = sin(uYaw);',
  '  return vec3(' + _gf(MO.lcx) + ' + X*cs + Z*sn, ' + _gf(MO.yc) + ' + Y, -X*sn + Z*cs);',
  '}'].join('\n');
const MO_VS = PX_HEAD + '\n' + MO_HEAD + '\n' + [
  'attribute float aU,aV,aW;',
  'varying float vLat,vEn;',
  'void main(){',
  '  vec3 p = waveAt(aU,aV,aW,0.0,uRunA)*uWIn',
  '         + latAt (aU,aV,aW)          *uWLat',
  '         + waveAt(aU,aV,aW,1.0,uRunB)*uWOut;',   // ← 三个解析目标，一次线性插值
  '  vLat = uWLat;',
  '  vEn  = mix(moEnv(aU,0.0,uRunA), moEnv(aU,1.0,uRunB), uWOut);',
  '  vA = aA*uLife; vH = aH;',
  '  vec4 mv = pxCore(vec3(p.x, -p.y, p.z), uSize);',
  '  gl_Position = projectionMatrix*mv;',
  '}'].join('\n');
const MO_PT_FS = [
  'uniform vec3 uColor,uHot; uniform float uOpacity,uBack,uSoft,uLatK,uCrest;',
  'varying float vFade,vA,vH; varying float vLat,vEn;',
  'void main(){',
  '  vec2 c=gl_PointCoord-0.5; float d=dot(c,c);',
  '  if(d>0.25) discard;',
  '  float a=uOpacity*vA*mix(uBack,1.0,vFade)*smoothstep(0.25,uSoft,d);',
  '  a *= mix(1.0, uLatK, vLat);',
  '  a *= 1.0 + uCrest*(1.0-vLat)*(vEn-0.5)*2.0;',      // 波峰亮度增益（格态自动关掉）
  '  if(a<0.004) discard;',
  '  gl_FragColor=vec4(mix(uColor,uHot,clamp(vLat,0.0,1.0)),clamp(a,0.0,1.0));',
  '  #include <colorspace_fragment>',
  '}'].join('\n');
/* 骨架线（两路，同一枚着色器靠 uRib 分档）：
     uRib = 0 **行线**（沿 u）—— 两态都在。波态它是一束**一起起伏的行波线**
            （光靠点云读不出「等相位线竖直」这件事，线一画出来就一眼看见）；
            格态它变成流形的经线，颜色随 vLat 从波色过渡到墨色。
     uRib = 1 **纬筋**（沿 v）—— a ∝ vLat²，只在「格」态长出来：
            格之所以是格，就在于它有第二个方向的支撑。 */
const MO_LN_FS = [
  'uniform vec3 uColor,uHot; uniform float uOpacity,uBack,uWaveK,uRib;',
  'varying float vFade,vA,vH; varying float vLat,vEn;',
  'void main(){',
  '  float k = mix(mix(uWaveK,1.0,vLat), vLat*vLat, uRib);',
  '  float a=uOpacity*vA*mix(uBack,1.0,vFade)*k;',
  '  a *= 1.0 + 0.30*(1.0-vLat)*(vEn-0.5)*2.0;',
  '  if(a<0.004) discard;',
  '  gl_FragColor=vec4(mix(uColor,uHot,clamp(vLat,0.0,1.0)),clamp(a,0.0,1.0));',
  '  #include <colorspace_fragment>',
  '}'].join('\n');

function makeMorph(ctx){
  const Q = K.o, w = ctx.rect[2], h = ctx.rect[3], D = 1400;
  const scene = new THREE.Scene();
  /* 相机按**剧场原高**（Q.h0 = 470）架，再用 setViewOffset 把视锥的下缘拉长到
     整块画布高 —— left/top/width 与 fov 一格不动，只有 height 乘 h/h0 ⇒
     ① 投影中心、横向缩放、上缘全部与从前逐像素相同（剧场不动的机器保证）；
     ② z=0 平面上仍是「1 世界单位 = 1px」，02 的两排带子直接画在局部 y508–708。
     ⚠ 相机的 aspect 必须保持 w/h0（不是 w/h）—— 那正是 setViewOffset 的前提。 */
  const camera = camPx(w, Q.h0, D);
  if(h > Q.h0) camera.setViewOffset(w, Q.h0, 0, 0, w, h);
  const SH = pxShared(D, 120);                 // 雾半程贴着真实 z 范围（±101）收紧 ——
                                              // 松了就等于没有体积（本轮实拍锤过：210 时整幅是平的）
  const NA = Q.na, NB = Q.nb, NC = Q.nc, N = NA*NB*NC;
  /* ── 一批顶点 · 三个解析目标：几何里只有 (u,v,w)，位置全在 VS 里现算 ── */
  const aU = new Float32Array(N), aV = new Float32Array(N), aW = new Float32Array(N);
  const aA = new Float32Array(N), aH = new Float32Array(N);
  const pos = new Float32Array(N*3);           // 占位（VS 不读它，但 three 要 position）
  let n = 0;
  for(let ic = 0; ic < NC; ic++) for(let ib = 0; ib < NB; ib++) for(let ia = 0; ia < NA; ia++){
    aU[n] = ia/(NA-1); aV[n] = ib/(NB-1); aW[n] = ic/(NC-1);
    // 层越深越淡（深度雾之外再压一档：五层点云不压层会糊成一团）
    aA[n] = 0.58 + 0.42*(1.0 - Math.abs(aW[n]-0.5)*2.0);
    aH[n] = 0; n++;
  }
  function moGeo(idx){
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos,3));
    g.setAttribute('aU', new THREE.BufferAttribute(aU,1));
    g.setAttribute('aV', new THREE.BufferAttribute(aV,1));
    g.setAttribute('aW', new THREE.BufferAttribute(aW,1));
    g.setAttribute('aA', new THREE.BufferAttribute(aA,1));
    g.setAttribute('aH', new THREE.BufferAttribute(aH,1));
    if(idx) g.setIndex(idx);
    return g;
  }
  const at = (ia,ib,ic) => (ic*NB + ib)*NA + ia;
  const wRow = [], wRib = [];
  for(let ic = 0; ic < NC; ic += 2) for(let ib = 0; ib < NB; ib++)   // 行线（沿 u · 隔层画）
    for(let ia = 0; ia < NA-1; ia++) wRow.push(at(ia,ib,ic), at(ia+1,ib,ic));
  for(let ic = 0; ic < NC; ic += 2) for(let ia = 0; ia < NA; ia += 4)  // 纬筋（沿 v · 疏）
    for(let ib = 0; ib < NB-1; ib++) wRib.push(at(ia,ib,ic), at(ia,ib+1,ic));
  const AS4 = { uA:{value:new THREE.Vector4(K.as.a[0],K.as.a[1],K.as.a[2],K.as.a[3])},
                uF:{value:new THREE.Vector4(K.as.f[0],K.as.f[1],K.as.f[2],K.as.f[3])},
                uPh:{value:new THREE.Vector4(K.as.ph[0],K.as.ph[1],K.as.ph[2],K.as.ph[3])} };
  function mkGen(){
    const u = Object.assign({ uT:{value:0}, uRunA:{value:0}, uRunB:{value:0},
                              uYaw:{value:0}, uLife:{value:0},
                              uWIn:{value:1}, uWLat:{value:0}, uWOut:{value:0},
                              uLatK:{value:1}, uCrest:{value:Q.crest} }, AS4);
    const mp = mkMat(SH, MO_VS, MO_PT_FS, u);
    const mkLn = (rib) => mkMat(SH, MO_VS, MO_LN_FS, Object.assign({}, u,
      { uSize:{value:1}, uWaveK:{value:.62}, uRib:{value:rib} }));
    const mrow = mkLn(0), mrib = mkLn(1);
    // 三枚材质共用同一批相位 uniform 对象 ⇒ 一处写、三处同步（不可能相位分叉）
    ['uT','uRunA','uRunB','uYaw','uLife','uWIn','uWLat','uWOut'].forEach(k => {
      mrow.uniforms[k] = mp.uniforms[k]; mrib.uniforms[k] = mp.uniforms[k]; });
    const pts = new THREE.Points(moGeo(null), mp); pts.frustumCulled = false;
    const lr = new THREE.LineSegments(moGeo(wRow), mrow); lr.frustumCulled = false;
    const lb = new THREE.LineSegments(moGeo(wRib), mrib); lb.frustumCulled = false;
    scene.add(pts); scene.add(lr); scene.add(lb);
    return { mp, ml: [mrow, mrib], u: mp.uniforms };
  }
  const GEN = [mkGen(), mkGen()];
  /* ── 第二道入射波：沿页上那条弧的一条 audioStream（lab-kit ⑨ · 同一种介质）──
     幅度剖面**只**走 gain 回调：注入窗之外整条落到 ghost 档（细线），
     窗内由弧尾向弧头涨起来 —— 零分支代码。 */
  const arcPts = (() => {
    const p = unpackPoly(Q.arc), c = polyCum(p), t = [0,0], out = [];
    for(let i = 0; i < 150; i++){
      polyAt(p, c, i/149, t);
      out.push([t[0], -t[1], 34]);              // 弧比舞台稍近一档 ⇒ 「切进来」是往前切
    }
    return out;
  })();
  const arc = mkStream(SH, arcPts, { w: Q.arcW, spd: Q.arcSpd, edge: .10 }).add(scene);
  const ARC = Q.arcWin;                         // [起, 到达, 余晖]
  arc.gain((u, clock) => {
    const s = ((clock % Q.gen) + Q.gen) % Q.gen;          // 每 7s 一记（每一代的出生）
    const win = smoother(ARC[0], ARC[1], s) * (1.0 - smoother(ARC[1], ARC[1]+ARC[2], s));
    return win * smoother(0.0, 0.55, u / arc.len);        // 弧头先亮：波是「切进来」的
  });
  /* ═══ 02 · SAME MOMENT「两制对照」（表达力精进 ①）════════════════════════
     一切都画在舞台局部 y = Q.ay + …（= 页 780 起那 200px）。z 恒 0 ⇒
     投影是恒等，poster 的 _p2_env_path 与这里是**同一批坐标**（不是「近似」）。 */
  const AY = Q.ay, SPAN = Q.tx1 - Q.tx0;
  // 一条水平流的采样点：4px 一段（aG 是逐顶点属性，点疏了让位窗口就落不到点上）
  const rowPts = (yc, x0, x1) => {
    const n = Math.max(2, Math.round((x1 - x0) / 4) + 1), o = [];
    for(let i = 0; i < n; i++) o.push([x0 + (x1 - x0)*i/(n-1), -(AY + yc), 0]);
    return o;
  };
  const win2 = (t, a, b, e) => smoother(a-e, a+e, t) * (1 - smoother(b-e, b+e, t));
  /* 上排 · 回合制：一条流 + 一条 gain 剖面（听 / 说实带、其余落 ghost 空档）。
     「其余」里含「想」那一段 —— 想不是媒体，它由下面那只虚线框来说。 */
  const anti = mkStream(SH, rowPts(Q.ry, Q.tx0, Q.tx1),
                        { w: Q.rw, spd: Q.spdb[0], edge: .04 }).add(scene);
  anti.gain((u) => {
    const t = u / SPAN;
    return Math.max(win2(t, Q.seg[0][0], Q.seg[0][1], Q.sege),
                    win2(t, Q.seg[2][0], Q.seg[2][1], Q.sege));
  });
  /* 下排 · 边说边听：听 / 想 / 说三条并行连续带。
     「想」按流质铁律不是媒体 ⇒ 同一枚原语的低幅档（gain .6 + 更窄的基准半宽），
     不另起一套点阵语汇。「说」从 22% 起，并在事件那一刻让位 200px 再接回。 */
  const EVX = Q.tx0 + SPAN*Q.evt;
  const live = [];
  for(let k = 0; k < 3; k++){
    const x0 = Q.tx0 + (k === 2 ? SPAN*Q.spk : 0);
    const s = mkStream(SH, rowPts(Q.ly[k], x0, Q.tx1),
                       { w: Q.lhw[k], spd: Q.spdb[1+k], edge: .04 }).add(scene);
    if(k === 2){
      const c = EVX - x0, hw = Q.duck*0.5, g0 = Q.lg[k];
      s.gain((u) => g0 * (1 - win2(u, c-hw, c+hw, hw*0.30)));
    }else{
      const g0 = Q.lg[k];
      s.gain(() => g0);
    }
    live.push(s);
  }
  /* 「想」的虚线框（不是流）+ 两枚事件竖标（同一根竖线：上排不让位 / 下排让位）。
     虚线段的坐标是**构建期算好的定长表**（K.o.dash）⇒ poster 与这里破折同相。 */
  function segMesh(rows, mat){
    const pos = new Float32Array(rows.length*6), al = new Float32Array(rows.length*2).fill(1);
    rows.forEach((r, i) => {
      pos[i*6]   = r[0]; pos[i*6+1] = -(AY + r[1]); pos[i*6+2] = 0;
      pos[i*6+3] = r[2]; pos[i*6+4] = -(AY + r[3]); pos[i*6+5] = 0;
    });
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos,3));
    g.setAttribute('aA', new THREE.BufferAttribute(al,1));
    g.setAttribute('aH', new THREE.BufferAttribute(new Float32Array(al.length),1));
    const o = new THREE.LineSegments(g, mat); o.frustumCulled = false; scene.add(o);
    return o;
  }
  const dashMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  segMesh(Q.dash, dashMat);
  const evtMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  segMesh([[EVX, Q.ry - Q.evh, EVX, Q.ry + Q.evh],
           [EVX, Q.ly[2] - Q.evh, EVX, Q.ly[2] + Q.evh]], evtMat);
  const evtDotMat = mkMat(SH, PX_PT_VS, PX_PT_FS);
  {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(
      new Float32Array([EVX, -(AY + Q.ry - Q.evh), 0]), 3));
    fillAH(g, 1, 0);
    const o = new THREE.Points(g, evtDotMat); o.frustumCulled = false; scene.add(o);
  }
  /* ── 相位：一代在 t 时刻的三态权重 + 生灭窗 + 让位偏航（与构建期 _mo_phase 同式）── */
  function phase(t){
    const s1 = smoother(Q.ph[0], Q.ph[1], t), s2 = smoother(Q.ph[2], Q.ph[3], t);
    const life = smoother(Q.life[0], Q.life[1], t) * (1 - smoother(Q.life[2], Q.life[3], t));
    const s = t - Q.yaw[0];
    const yaw = smoother(0, Q.yaw[1], s) * (1 - smoother(Q.yaw[1], Q.yaw[1]+Q.yaw[2], s)) * Q.yawA;
    return { wIn: 1-s1, wLat: s1*(1-s2), wOut: s1*s2, life, yaw };
  }
  return {
    scene, camera, intro: 1.2, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      for(let g = 0; g < 2; g++){
        const t = (((clock + g*Q.gen) % Q.cyc) + Q.cyc) % Q.cyc;
        const ph = phase(t), u = GEN[g].u;
        u.uT.value = t;
        u.uRunA.value = Q.spd[0]*clock; u.uRunB.value = Q.spd[1]*clock;
        u.uWIn.value = ph.wIn; u.uWLat.value = ph.wLat; u.uWOut.value = ph.wOut;
        u.uLife.value = ph.life * SH.uIntro.value;
        u.uYaw.value = ph.yaw;
      }
      arc.draw(clock);
      anti.draw(clock);                       // 02「两制对照」：四股与剧场同一个钟
      live.forEach(s => s.draw(clock));
    },
    /* ⑲h 的探针：闸门拿它逐拍复算相位（不截帧、不比像素） */
    state(){
      const out = { cyc: Q.cyc, gen: Q.gen, verts: N, grid: [NA,NB,NC], lam: K.as.lam, g: [] };
      for(let g = 0; g < 2; g++){
        const u = GEN[g].u;
        out.g.push({ t: u.uT.value, wIn: u.uWIn.value, wLat: u.uWLat.value,
                     wOut: u.uWOut.value, life: u.uLife.value, yaw: u.uYaw.value });
      }
      out.run = [GEN[0].u.uRunA.value, GEN[0].u.uRunB.value];
      out.arc = arc.mesh.geometry.attributes.aG.array[0];
      out.flow = arc.mat.uniforms.uOpacity.value;
      /* 02「两制对照」的探针：空档真的落到 ghost（不是「小一点的波」）、
         让位真的到底、其余段真的满幅 —— 三个数就够复算「✕ vs ✓」。 */
      const aG = anti.mesh.geometry.attributes.aG.array;
      const dG = live[2].mesh.geometry.attributes.aG.array;
      out.two = { gapMin: Math.min.apply(null, aG), gapMax: Math.max.apply(null, aG),
                  duckMin: Math.min.apply(null, dG), duckMax: Math.max.apply(null, dG),
                  lanes: live.length, evx: EVX };
      return out;
    },
    applyTheme(){
      const wv = cssColor('--o-wave'), lt = cssColor('--o-lat');
      const wop = cssNum('--o-wave-op', .62), lop = cssNum('--o-lat-op', .55);
      GEN.forEach(gn => {
        gn.mp.uniforms.uColor.value.copy(wv);
        gn.mp.uniforms.uHot.value.copy(lt);
        gn.mp.uniforms.uOpacity.value = wop;
        gn.mp.uniforms.uLatK.value = lop / (wop || 1);
        gn.mp.uniforms.uSize.value = cssNum('--o-dot-size', 3);
        gn.mp.uniforms.uSoft.value = .04;
        gn.mp.uniforms.uBack.value = .26;
        gn.ml.forEach(m => {
          m.uniforms.uColor.value.copy(wv); m.uniforms.uHot.value.copy(lt);
          m.uniforms.uOpacity.value = cssNum('--o-wire-op', .3);
          m.uniforms.uBack.value = .26; setBlend(m, cssNum('--o-add', 0)); });
        setBlend(gn.mp, cssNum('--o-add', 0));
      });
      arc.theme(cssColor('--o-arc'), cssColor('--o-arc-rms'),
                cssNum('--o-arc-op', .70), cssNum('--o-arc-rms-op', .55), .62);
      setBlend(arc.mat, cssNum('--o-add', 0));
      // 02「两制对照」：回合制走灰（note 语域）、边说边听走 accent、事件标走 accent-deep
      const an = cssColor('--o-anti'), lv = cssColor('--o-live'), ev = cssColor('--o-evt');
      anti.theme(an, cssColor('--o-anti-rms'), cssNum('--o-anti-op', .66),
                 cssNum('--o-anti-rms-op', .42), 1);
      live.forEach(s => s.theme(lv, cssColor('--o-live-rms'), cssNum('--o-live-op', .66),
                                cssNum('--o-live-rms-op', .55), 1));
      dashMat.uniforms.uColor.value.copy(an); dashMat.uniforms.uHot.value.copy(an);
      dashMat.uniforms.uOpacity.value = cssNum('--o-anti-op', .66);
      dashMat.uniforms.uBack.value = 1; dashMat.uniforms.uGain.value = 0;
      [evtMat, evtDotMat].forEach(m => {
        m.uniforms.uColor.value.copy(ev); m.uniforms.uHot.value.copy(ev);
        m.uniforms.uOpacity.value = cssNum('--o-evt-op', .92);
        m.uniforms.uBack.value = 1; m.uniforms.uGain.value = 0; });
      evtDotMat.uniforms.uSize.value = 8;
      [anti.mat, dashMat, evtMat, evtDotMat].concat(live.map(s => s.mat))
        .forEach(m => setBlend(m, cssNum('--o-add', 0)));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑨ 双工三通道（P3）
   ───────────────────────────────────────────────────────────────────────────
   三张小图的两列（A / B）分坐**两个深度面**：A 在近、B 在远，两列之间那条
   76px 的空档于是变成一条真正穿越空间的通道 —— A→B 的包一路后退变小，
   B→A 的包一路迎面变大，「哪个方向在走」不用看箭头，看包的远近就知道。
     单工   上行通道有包，下行通道压暗、永远无包（线在，包不来）
     半双工 两条通道都活，占空比 1/3 + 半周期相位差 ⇒ **任何时刻只有一个方向在途**
     全双工 两条通道占空比各 100% ⇒ 永远同框
   相位表逐参照抄页上的 .mo-packet（见 dutyOf/flightU 的注释）：语义闸在 3D 上复算，
   与页面 CSS 是同一套参数、同一条算法 —— 不许分叉。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeLanes(ctx){
  const Q = K.l, w = ctx.rect[2], h = ctx.rect[3], D = 1150;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 120), L0 = mkLock(w, h, D);
  // 卡内 figure 坐标 → 舞台局部坐标（三张卡横排，figure 缩放 Q.s、上边距 Q.dy）
  const P = (k, x, y, z) => L0(k * Q.gap + x * Q.s, y * Q.s + Q.dy, z);
  const ZA = Q.dep, ZB = -Q.dep;
  const slabMat = mkMat(SH, PX_LN_VS, PX_LN_FS);        // 说话块（实）
  const idleMat = mkMat(SH, PX_LN_VS, PX_LN_FS);        // 空块（虚 · 没在说）
  const railMat = mkMat(SH, PX_LN_VS, PX_LN_FS);        // 活通道
  const deadMat = mkMat(SH, PX_LN_VS, PX_LN_FS);        // 静默通道
  const axisMat = mkMat(SH, PX_LN_VS, PX_LN_FS);        // 时间轴
  const gateMat = mkMat(SH, PX_LN_VS, PX_LN_FS);        // 半双工的切换闸（虚线段）
  const lapMat = mkMat(SH, PX_LN_VS, PX_LN_FS);         // 全双工的重叠区高亮
  lapMat.side = THREE.DoubleSide;
  railMat.side = THREE.DoubleSide; deadMat.side = THREE.DoubleSide;
  const on = [], off = [], live = [], dead = [], axis = [], gate = [];
  let lapMesh = null;
  const fillMat = mkMat(SH, PX_LN_VS, PX_LN_FS);        // 「谁在说」那块实心带
  fillMat.side = THREE.DoubleSide;
  const CH = [];                                        // 通道运行表
  for(let k = 0; k < 3; k++){
    const M = Q.modes[k];
    M.bands.forEach((b) => {                            // b = [列(0=A/1=B), y, h, 在说]
      const x = b[0] ? Q.rx : Q.lx, z = b[0] ? ZB : ZA;
      const box = extrudeBack(x, b[1], Q.cw, b[2], z, Q.slab, (a,c,d)=>P(k,a,c,d));
      (b[3] ? on : off).push.apply(b[3] ? on : off, box.segs);
      if(b[3]){                                          // 在说 ⇒ 腔口填实（页上就是实心带）
        const g = quadGeo(box.front.slice(0, 4));
        fillAH(g, 1, 0);
        scene.add(Object.assign(new THREE.Mesh(g, fillMat), { frustumCulled:false }));
      }
    });
    M.ch.forEach((c) => {                               // c = [y, 向, 周期, 相位, 空挡, 段长, 活]
      const a = c[1] > 0 ? [Q.lx + Q.cw, ZA] : [Q.rx, ZB];
      const b = c[1] > 0 ? [Q.rx, ZB] : [Q.lx + Q.cw, ZA];
      const p0 = P(k, a[0], c[0], a[1]), p1 = P(k, b[0], c[0], b[1]);
      (c[6] ? live : dead).push([p0[0],p0[1],p0[2], p1[0],p1[1],p1[2]]);
      /* ④：通道是**带**不是线 —— 沿 y 撑开半宽 Q.chw 的一片四边形。
         线宽在 WebGL 里是 1px 死的（lineWidth 早就不生效），所以「加粗」只能
         靠真几何：一枚 quad 才有宽度，深度雾与遮挡也跟着对。 */
      const qd = quadGeo([P(k, a[0], c[0]-Q.chw, a[1]), P(k, b[0], c[0]-Q.chw, b[1]),
                          P(k, b[0], c[0]+Q.chw, b[1]), P(k, a[0], c[0]+Q.chw, a[1])]);
      fillAH(qd, 1, 0);
      scene.add(Object.assign(new THREE.Mesh(qd, c[6] ? railMat : deadMat),
                              { frustumCulled:false }));
      if(c[6]) CH.push({ k, y: c[0], a, b, T: c[2], off: c[3],
                         duty: dutyOf(c[5], c[4], 14) });
    });
    /* ④ 全双工的**重叠区高亮** —— 这一格的论点本身（同一时刻两边都在说）。
       过去只有 2D 有它，3D 起来就没了；现在照 _P3LAP 画一枚同位的面（z=0，
       正好夹在 A 面 +dep 与 B 面 −dep 之间 ⇒ 两列都从它里面穿过去）。 */
    if(k === 2){                                        // k=2 就是全双工那一张
      const g = quadGeo([P(k, Q.lap[0], Q.lap[1], 0), P(k, Q.lap[0]+Q.lap[2], Q.lap[1], 0),
                         P(k, Q.lap[0]+Q.lap[2], Q.lap[1]+Q.lap[3], 0),
                         P(k, Q.lap[0], Q.lap[1]+Q.lap[3], 0)]);
      fillAH(g, 1, 0);
      lapMesh = Object.assign(new THREE.Mesh(g, lapMat), { frustumCulled:false });
      scene.add(lapMesh);
    }
    /* ④ 半双工的**切换闸** —— 同理：2D 有、3D 过去没有。虚线段表是构建期算好的
       （K.l.gate），页上与这里同一批坐标 ⇒ 破折相位不分叉。 */
    if(k === 1) Q.gate.forEach((gseg) => {
      const p2a = P(k, gseg[0], gseg[1], 0), p2b = P(k, gseg[2], gseg[3], 0);
      gate.push([p2a[0],p2a[1],p2a[2], p2b[0],p2b[1],p2b[2]]);
    });
    for(let t = 0; t < 5; t++){                          // 无字刻度的时间轴
      const yy = [Q.ct, Q.ct+26, Q.ct+52, Q.ct+78, 122][t];
      const q0 = P(k, 9, yy, 0), q1 = P(k, 19, yy, 0);
      axis.push([q0[0],q0[1],q0[2], q1[0],q1[1],q1[2]]);
    }
    const v0 = P(k, 14, Q.ct, 0), v1 = P(k, 14, 122, 0);
    axis.push([v0[0],v0[1],v0[2], v1[0],v1[1],v1[2]]);
  }
  [[on, slabMat], [off, idleMat], [axis, axisMat], [gate, gateMat]]
    .forEach(([segs, m]) => {
      if(!segs.length) return;
      const g = segGeo(segs); fillAH(g, 1, 0);
      scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
    });
  const NPK = CH.length * 3;
  const pg = new THREE.BufferGeometry();
  const ppos = new Float32Array(NPK * 3);
  pg.setAttribute('position', new THREE.BufferAttribute(ppos, 3));
  const pA = fillAH(pg, 0, 0);
  const pktMat = mkMat(SH, PX_PT_VS, PX_PT_FS); pktMat.uniforms.uSoft.value = .03;
  scene.add(Object.assign(new THREE.Points(pg, pktMat), { frustumCulled:false }));
  return {
    scene, camera, intro: 1.0, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      let n = 0;
      CH.forEach((c) => {
        for(let j = 0; j < 3; j++){
          const u = flightU(clock + j * c.T / 3, c.T, c.off, c.duty);
          if(u < 0 || u > 1){ pA.a[n] = 0; ppos[n*3+2] = 0; n++; continue; }
          const x = c.a[0] + (c.b[0] - c.a[0]) * u, z = c.a[1] + (c.b[1] - c.a[1]) * u;
          const q = P(c.k, x, c.y, z);
          ppos[n*3] = q[0]; ppos[n*3+1] = q[1]; ppos[n*3+2] = q[2];
          pA.a[n] = Math.min(1, Math.min(u, 1 - u) * 7 + .25); n++;
        }
      });
      pg.attributes.position.needsUpdate = true; pg.attributes.aA.needsUpdate = true;
    },
    applyTheme(){
      slabMat.uniforms.uColor.value.copy(cssColor('--l-on'));
      slabMat.uniforms.uOpacity.value = cssNum('--l-on-op', .95);
      idleMat.uniforms.uColor.value.copy(cssColor('--l-off'));
      idleMat.uniforms.uOpacity.value = cssNum('--l-off-op', .3);
      railMat.uniforms.uColor.value.copy(cssColor('--l-rail'));
      railMat.uniforms.uOpacity.value = cssNum('--l-rail-op', .85);
      deadMat.uniforms.uColor.value.copy(cssColor('--l-dead'));
      deadMat.uniforms.uOpacity.value = cssNum('--l-dead-op', .3);
      gateMat.uniforms.uColor.value.copy(cssColor('--l-off'));
      gateMat.uniforms.uOpacity.value = cssNum('--l-off-op', .8);
      lapMat.uniforms.uColor.value.copy(cssColor('--l-lap'));
      lapMat.uniforms.uOpacity.value = cssNum('--l-lap-op', .19);
      axisMat.uniforms.uColor.value.copy(cssColor('--l-axis'));
      axisMat.uniforms.uOpacity.value = cssNum('--l-axis-op', .4);
      pktMat.uniforms.uColor.value.copy(cssColor('--l-pkt'));
      pktMat.uniforms.uOpacity.value = cssNum('--l-pkt-op', 1);
      pktMat.uniforms.uSize.value = cssNum('--l-pkt-size', 7);
      fillMat.uniforms.uColor.value.copy(cssColor('--l-on'));
      fillMat.uniforms.uOpacity.value = cssNum('--l-fill-op', .28);
      [slabMat, idleMat, railMat, deadMat, axisMat, pktMat, fillMat,
       gateMat, lapMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0;
        m.uniforms.uBack.value = .62; setBlend(m, cssNum('--l-add', 0));
      });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑩ 实时语音链路（P6 · 650 拆解）
   ───────────────────────────────────────────────────────────────────────────
   四个环节（AI-VAD / ASR / LLM / TTS）成为空间站点序列：链路从麦克风（近）
   往云里探（LLM 最深），再回到喇叭（近）—— 「一趟往返」在深度上直接看得见。
   「端到端 650ms」仍是页上那行 DOM 字。
   分步：step1 = 数字人支路（可选件往**前**弹出主路平面，它不在 650ms 预算里）。

   ── 二轮精修 · 波A：主路 12 枚球（296px/s）→ **横贯全链一条流** ────────────
   终审：「P6 数据点不足以表达媒体流。」这条线上跑的是音频，音频一直在来 ⇒
   它是**介质**，必须是一条带子（接入指南 ⑨）。改成一条流之后：
     · 「进站收窄、出站展开」不再是特效，是一条 gain 回调的自然结果
       （站点盒内 aG 压到 .34 ⇒ 幅度落档且包络平掉 = 进了盒子就收成细带）；
     · 符号行的四段（音频帧 / 增量文本 / token / 音频包）首尾**严丝合缝**接成
       一条流（三处接缝 452 / 752 / 1052 由闸门复算），粒度由 λ 与半宽逐段变粗；
     · **token 段留粒子**（token 本来就离散），但按指南 ⑨ 的交界地带条款做成
       **高密度脉冲串**（每 5 枚一组、头亮尾淡）+ 一条极淡**载流带垫底** ——
       只要看得出「一颗一颗在飞」，这一段就还没做完。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeChain(ctx){
  const Q = K.c, w = ctx.rect[2], h = ctx.rect[3], D = 1500;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 200), L0 = mkLock(w, h, D);
  // 两道平移就在这里接上：LA = 盒链组（translate 0,−46），LB = 增量流带组（0,−34）
  const LA = (x, y, z) => L0(x, y + Q.dyA, z);
  const LB = (x, y, z) => L0(x, y + Q.dyB, z);
  const zAt = (x) => {                                  // 链路深度剖面：两端近、中间深
    const t = Math.max(0, Math.min(1, (x - Q.x0) / (Q.x1 - Q.x0)));
    return Q.zNear - (Q.zNear - Q.zDeep) * Math.sin(Math.PI * t);
  };
  const faceMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const hotMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const shellMat= mkMat(SH, PX_LN_VS, PX_LN_FS);
  const railMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const spanMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const face = [], hotF = [], shell = [], rail = [], span = [];
  Q.st.forEach((s) => {                                  // s = [x,y,w,h,hot]
    const z = zAt(s[0] + s[2] / 2);
    const bb = boxBody(s[0], s[1], s[2], s[3], z, Q.dz, LA);
    (s[4] ? hotF : face).push.apply(s[4] ? hotF : face, bb.front);
    shell.push.apply(shell, bb.shell);
  });
  Q.rings.forEach((c) => {                               // 麦克风 / 喇叭：两枚空间环
    const z = zAt(c[0]);
    for(let i = 0; i < 40; i++){
      const a0 = i / 40 * TAU, a1 = (i + 1) / 40 * TAU;
      const p0 = LA(c[0] + Math.cos(a0) * c[2], c[1] + Math.sin(a0) * c[2], z);
      const p1 = LA(c[0] + Math.cos(a1) * c[2], c[1] + Math.sin(a1) * c[2], z);
      face.push([p0[0],p0[1],p0[2], p1[0],p1[1],p1[2]]);
    }
  });
  Q.link.forEach((s) => {                                // 站点之间的接头（真的在深度里走）
    const p0 = LA(s[0], Q.ly, zAt(s[0])), p1 = LA(s[1], Q.ly, zAt(s[1]));
    rail.push([p0[0],p0[1],p0[2], p1[0],p1[1],p1[2]]);
  });
  { const a = LA(Q.span[0], Q.span[2], zAt(Q.span[0])), b = LA(Q.span[1], Q.span[2], zAt(Q.span[1]));
    span.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
    [[Q.span[0], zAt(Q.span[0])], [Q.span[1], zAt(Q.span[1])]].forEach((e) => {
      const u = LA(e[0], Q.span[2]-10, e[1]), v = LA(e[0], Q.span[2]+10, e[1]);
      span.push([u[0],u[1],u[2], v[0],v[1],v[2]]);
    }); }
  [[face, faceMat], [hotF, hotMat], [shell, shellMat], [rail, railMat], [span, spanMat]]
    .forEach(([segs, m]) => {
      const g = segGeo(segs); fillAH(g, 1, 0);
      scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
    });
  /* ── ① 主路：**一条**横贯全链的连续媒体流（麦克风 → 四站 → 喇叭）────────
     旧版是 12 枚球在同一条线上挪；那讲的是「有几个包」，不是「一直在来」。 */
  const inBox = (x) => {                                 // 站点盒内 ⇒ 进站收窄
    for(let i = 0; i < Q.st.length; i++){
      const b = Q.st[i];
      if(x > b[0] && x < b[0] + b[2]) return 1;
    }
    return 0;
  };
  const mainStr = (function(){
    const NM = 300, pts = [];
    for(let i = 0; i < NM; i++){
      const x = Q.x0 + (Q.x1 - Q.x0) * i / (NM - 1);
      pts.push(LA(x, Q.ly, zAt(x)));
    }
    const st = mkStream(SH, pts, { w: Q.hwMain, spd: Q.spd[0] });
    // 进站收窄 / 出站展开：**一条 gain 回调**，零分支代码（软化边界用 smoothstep）
    st.gain((u) => {
      const x = Q.x0 + u;
      let g = 1;
      for(let i = 0; i < Q.st.length; i++){
        const b = Q.st[i], e = 14;
        g *= 1 - 0.66 * (sstep(b[0]-e, b[0]+e, x) - sstep(b[0]+b[2]-e, b[0]+b[2]+e, x));
      }
      return g;
    });
    return st.add(scene);
  })();
  // ── 增量流带：四条并行细 ribbon，各自贴在自己那一段的深度上（也换成连续流）──
  const bandStr = Q.bands.map((b, i) => {                // b = [x0,x1,y]
    const pts = [];
    for(let j = 0; j < 40; j++){
      const x = b[0] + (b[1] - b[0]) * j / 39;
      pts.push(LB(x, b[2], zAt(x) - Q.bandZ * i));
    }
    return mkStream(SH, pts, { w: Q.bandW, spd: Q.spd[5 + i] }).add(scene);
  });
  // ── 增量流带的主轨（那条 hline 本人）──
  const flowMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  { const a2 = LB(Q.flow[0], Q.flow[2], zAt(Q.flow[0])), b2 = LB(Q.flow[1], Q.flow[2], zAt(Q.flow[1]));
    const g = segGeo([[a2[0],a2[1],a2[2], b2[0],b2[1],b2[2]]]); fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.Line(g, flowMat), { frustumCulled:false })); }
  /* ── ② 符号行：四段首尾严丝合缝接成一条流；只有 token 段留粒子 ──────────
     段界逐个 = 页上四组符号的起始 x（Q.seg），三处接缝由 ⑲(P6) 闸复算。 */
  const segStr = Q.seg.map((sg, i) => {
    const pts = [];
    for(let j = 0; j < 40; j++){
      const x = sg[0] + (sg[1] - sg[0]) * j / 39;
      pts.push(LB(x, Q.flow[2], zAt(x)));
    }
    const isTok = (i === Q.tok);
    // token 段是**载流垫底**：地板抬高、包络压平、极淡 —— 它托着上面那串脉冲
    const st = mkStream(SH, pts, { w: Q.hwSeg[i], spd: Q.spd[1 + i],
                                   floor: isTok ? 0.86 : AS.floor });
    return st.add(scene);          // 不写 gain ⇒ aG 恒 1：这四段是一条不断的流
  });
  /* ── ③ token 段的高密度脉冲串（离散语义 + 成流的形）────────────────────
     每 Q.pulseN 枚一组、组内头亮尾淡；粒距 Q.pulse；整串沿段速漂移。
     没有下面那条载流带垫底，它就退回成「一颗一颗在飞」—— 那就是没做完。 */
  const TOKSEG = Q.seg[Q.tok], TOKL = TOKSEG[1] - TOKSEG[0];
  const TN = Math.round(TOKL / Q.pulse) + Q.pulseN;
  const tg = new THREE.BufferGeometry();
  const tpos = new Float32Array(TN * 3);
  tg.setAttribute('position', new THREE.BufferAttribute(tpos, 3));
  const tA = fillAH(tg, 1, 0);
  const tokMat = mkMat(SH, PX_PT_VS, PX_PT_FS); tokMat.uniforms.uSoft.value = .04;
  scene.add(Object.assign(new THREE.Points(tg, tokMat), { frustumCulled:false }));
  // ── 数字人支路（step1）：往前弹出主路平面 ──
  const forkG = new THREE.Group(); forkG.visible = false; scene.add(forkG);
  const forkMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  { const fs = [], zf = zAt(Q.fork[0]) + Q.forkZ;
    const a = LA(Q.fork[0], Q.fork[1], zAt(Q.fork[0])), b = LA(Q.fork[0], Q.dh[1], zf);
    fs.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
    fs.push.apply(fs, boxBody(Q.dh[0], Q.dh[1], Q.dh[2], Q.dh[3], zf, Q.dz, LA).front);
    const g = segGeo(fs); fillAH(g, 1, 0);
    forkG.add(Object.assign(new THREE.LineSegments(g, forkMat), { frustumCulled:false })); }
  let step = 0;
  return {
    scene, camera, intro: 1.2, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    setStep(n){ step = n; forkG.visible = n >= 1; },
    state(){ return { seam: [Q.seg[0][1], Q.seg[1][1], Q.seg[2][1]],
                      span: [Q.x0, Q.x1], tok: Q.tok,
                      spd: Q.spd.slice(), pulses: TN,
                      run: mainStr.mat.uniforms.uRun.value }; },
    draw(dt, clock){
      SH.uTime.value = clock;
      mainStr.draw(clock);
      bandStr.forEach(st => st.draw(clock));
      segStr.forEach(st => st.draw(clock));
      // 「组」的相位必须**随流一起走**：亮头钉在屏上不动 = 「带子没动只是在闪」，
      // 那正是本波要治的病。用 adv（已推进多少颗）给每一颗一个随流漂移的身份 id。
      const adv = Q.spd[1 + Q.tok] * clock / Q.pulse;
      const base = Math.floor(adv), frac = adv - base;
      for(let i = 0; i < TN; i++){
        const x = TOKSEG[0] + (i + frac - 1) * Q.pulse;
        const q = LB(x, Q.flow[2], zAt(x));
        tpos[i*3] = q[0]; tpos[i*3+1] = q[1]; tpos[i*3+2] = q[2];
        const inSeg = x >= TOKSEG[0] && x <= TOKSEG[1] ? 1 : 0;
        // 每 pulseN 枚一组：组头最亮、组尾最淡 ⇒ 读成一串一串，不是一颗一颗
        const id = i - base, k = ((id % Q.pulseN) + Q.pulseN) % Q.pulseN;
        tA.a[i] = inSeg * (1 - k / Q.pulseN * 0.72);
        tA.h[i] = inSeg * (k === 0 ? 1 : 0);
      }
      tg.attributes.position.needsUpdate = true;
      tg.attributes.aA.needsUpdate = true; tg.attributes.aH.needsUpdate = true;
      hotMat.uniforms.uGain.value = .5 + .5 * Math.sin(clock * TAU / Q.beat);
    },
    applyTheme(){
      const peak = cssColor('--c-stream'), rms = cssColor('--c-rms');
      const pop = cssNum('--c-stream-op', .56), rop = cssNum('--c-rms-op', .58);
      mainStr.theme(peak, rms, pop, rop, .62);
      bandStr.forEach((st, i) => st.theme(cssColor('--c-band'), rms,
        cssNum('--c-band-op', .5) * [1, .82, .64, .5][i], rop * .8, .62));
      segStr.forEach((st, i) => st.theme(peak,
        i === Q.tok ? cssColor('--c-bed') : rms,
        i === Q.tok ? cssNum('--c-bed-op', .2) : pop * .92, rop, .62));
      flowMat.uniforms.uColor.value.copy(cssColor('--c-rail'));
      flowMat.uniforms.uOpacity.value = cssNum('--c-rail-op', .6);
      tokMat.uniforms.uColor.value.copy(cssColor('--c-band'));
      tokMat.uniforms.uHot.value.copy(cssColor('--c-pkt'));
      tokMat.uniforms.uOpacity.value = cssNum('--c-glyph-op', .9);
      tokMat.uniforms.uSize.value = cssNum('--c-pkt-size', 7);
      tokMat.uniforms.uGain.value = .55;
      faceMat.uniforms.uColor.value.copy(cssColor('--c-face'));
      faceMat.uniforms.uOpacity.value = cssNum('--c-face-op', .8);
      hotMat.uniforms.uColor.value.copy(cssColor('--c-hot'));
      hotMat.uniforms.uHot.value.copy(cssColor('--c-hot'));
      hotMat.uniforms.uOpacity.value = cssNum('--c-hot-op', 1);
      shellMat.uniforms.uColor.value.copy(cssColor('--c-shell'));
      shellMat.uniforms.uOpacity.value = cssNum('--c-shell-op', .28);
      railMat.uniforms.uColor.value.copy(cssColor('--c-rail'));
      railMat.uniforms.uOpacity.value = cssNum('--c-rail-op', .6);
      spanMat.uniforms.uColor.value.copy(cssColor('--c-span'));
      spanMat.uniforms.uOpacity.value = cssNum('--c-span-op', .5);
      forkMat.uniforms.uColor.value.copy(cssColor('--c-fork'));
      forkMat.uniforms.uOpacity.value = cssNum('--c-fork-op', .6);
      [faceMat, shellMat, railMat, spanMat, forkMat, flowMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0; });
      [faceMat, hotMat, shellMat, railMat, spanMat, forkMat, flowMat, tokMat]
        .forEach(m => { m.uniforms.uBack.value = .62; setBlend(m, cssNum('--c-add', 0)); });
      [mainStr].concat(bandStr, segStr)
        .forEach(st => setBlend(st.mat, cssNum('--c-add', 0)));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑪ 打断时序 · 两条声轨的让位（P8 · 340 拆解）
   ───────────────────────────────────────────────────────────────────────────
   与 P4「双向声带」分工明确：P4 讲**同时**（两条带永远同框、深度上不相撞），
   本页讲**让位的那一刻**。x = 时间（页上 1px = 1ms），两条声轨在深度里交错。

   ── 二轮精修 · 波A：这一页是「Audition 感」的验收主件 ────────────────────
   终审原话：「P8 想构建声波感但像锯齿，突兀不精致 —— 让它像 Audition 里的声波
   一样动起来，可借鉴播放器音量 / 音效动效。」
     ① 波形换成 lab-kit ⑨ 的 **解析包络**（旧版逐柱采样 _P9HS 再线性插值 ——
        每根柱的边界都是一处斜率突变，那就是锯齿本人）。换掉之后从根上没有角。
     ② 让位窗口从旧版 1040→1100 的 60px 断崖，挪到页上「收声」那段相位括号
        （840→1040，**200px**）：塌陷的语义位置由页上的括号决定，不由手感决定。
     ③ 幅度剖面全部走 **gain 回调**：智能体轨在 duck 窗口里 1→0（aG→0 ⇒ 幅度落
        ghost 档且包络一起平掉 = 真细线），用户轨在插话点前后 0→1。零分支代码。
   340ms 快路径仍是一条真的斜穿深度的线：从用户轨的深度直插智能体轨的深度。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeCutin(ctx){
  const Q = K.u, w = ctx.rect[2], h = ctx.rect[3], D = 1500;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 150), L = mkLock(w, h, D);
  const N = 360;
  const smooth = (a, b, x) => { const t = Math.max(0, Math.min(1, (x-a)/(b-a)));
                                return t*t*(3-2*t); };          // C¹ 的 smoothstep
  /* 一条声轨 = 一条 mkStream。深度剖面照旧（让位的退到远处、插话的推到前面），
     幅度剖面**只**通过 gain 回调表达 —— 见 lab-kit ⑨ 的 aG 双通道。 */
  function track(y, kind){
    const pts = [];
    for(let i = 0; i < N; i++){
      const x = Q.tx0 + (Q.tx1-Q.tx0)*i/(N-1);
      const z = kind === 0
        ? Q.zA    - (Q.zA    - Q.zGhost)*smooth(Q.duck[0], Q.duck[1], x)
        : Q.zBack + (Q.zB    - Q.zBack )*smooth(Q.in - 20, Q.in + 40, x);
      pts.push(L(x, y, z));
    }
    const st = mkStream(SH, pts, { w: Q.hw[kind], spd: Q.spd[kind] });
    // ↓↓ 本页全部的「让位」语义就是这两行回调：一条 gain，零 if 分支 ↓↓
    st.gain(kind === 0
      ? (u) => 1 - smooth(Q.duck[0]-Q.tx0, Q.duck[1]-Q.tx0, u)     // 收声：1 → 0
      : (u) => smooth(Q.in-20-Q.tx0, Q.in+40-Q.tx0, u));           // 插话：0 → 1
    st.add(scene);
    return st;
  }
  const strA = track(Q.yA, 0);
  const strB = track(Q.yB, 1);
  // ── 340ms 快路径：从用户轨的深度斜穿到智能体轨的深度（真的换了一个平面）──
  const fastMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  { const pts = [];
    for(let i = 0; i < 40; i++){
      const t = i / 39;
      const x = Q.in + (Q.cut - Q.in) * t;
      const y = Q.yB - 40 - (Q.yB - 40 - (Q.yA + 46)) * t;
      pts.push(L(x, y, Q.zB + (Q.zA - Q.zB) * t));
    }
    const g = stripGeo(pts); fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.Line(g, fastMat), { frustumCulled:false })); }
  // ── 两根事件竖线（插话 / 收声）：立在时间轴上的门，穿透两条轨的深度 ──
  const cutMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  { const segs = [];
    [[Q.in, Q.zB], [Q.cut, Q.zA]].forEach((e) => {
      for(let s = 0; s < 10; s += 2){
        const y0 = Q.gy0 + (Q.gy1 - Q.gy0) * s / 10, y1 = Q.gy0 + (Q.gy1 - Q.gy0) * (s + 1) / 10;
        const a = L(e[0], y0, e[1]), b = L(e[0], y1, e[1]);
        segs.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
      }
    });
    const g = segGeo(segs); fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.LineSegments(g, cutMat), { frustumCulled:false })); }
  // ── 快路径上的包：那 340ms 本身（**离散事件**，所以它才有资格是粒子）──
  const NP = 5, pg = new THREE.BufferGeometry();
  const ppos = new Float32Array(NP * 3);
  pg.setAttribute('position', new THREE.BufferAttribute(ppos, 3));
  const pA = fillAH(pg, 1, 1);
  const pktMat = mkMat(SH, PX_PT_VS, PX_PT_FS); pktMat.uniforms.uSoft.value = .03;
  scene.add(Object.assign(new THREE.Points(pg, pktMat), { frustumCulled:false }));
  return {
    scene, camera, intro: 1.25, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    // 闸门探针：让位剖面与流速可以在运行时被逐点复算（⑲(P8) 用它）
    state(){
      const at = (x) => 1 - smooth(Q.duck[0], Q.duck[1], x);
      return { duck: Q.duck.slice(), spd: Q.spd.slice(),
               gA: [at(Q.duck[0]-1), at((Q.duck[0]+Q.duck[1])/2), at(Q.duck[1]+1)],
               run: strA.mat.uniforms.uRun.value };
    },
    draw(dt, clock){
      SH.uTime.value = clock;
      strA.draw(clock); strB.draw(clock);
      for(let i = 0; i < NP; i++){
        const t = ((clock / Q.dur) + i / NP) % 1;
        const x = Q.in + (Q.cut - Q.in) * t;
        const y = Q.yB - 40 - (Q.yB - 40 - (Q.yA + 46)) * t;
        const q = L(x, y, Q.zB + (Q.zA - Q.zB) * t);
        ppos[i*3] = q[0]; ppos[i*3+1] = q[1]; ppos[i*3+2] = q[2];
        pA.a[i] = Math.min(1, Math.min(t, 1 - t) * 8);
      }
      pg.attributes.position.needsUpdate = true; pg.attributes.aA.needsUpdate = true;
    },
    applyTheme(){
      strA.theme(cssColor('--u-agent'), cssColor('--u-rms'),
                 cssNum('--u-agent-op', .8), cssNum('--u-rms-op', .9), .62);
      strB.theme(cssColor('--u-user'), cssColor('--u-rms-b'),
                 cssNum('--u-user-op', .6), cssNum('--u-rms-op', .9), .62);
      fastMat.uniforms.uColor.value.copy(cssColor('--u-fast'));
      fastMat.uniforms.uOpacity.value = cssNum('--u-fast-op', .9);
      cutMat.uniforms.uColor.value.copy(cssColor('--u-cut'));
      cutMat.uniforms.uOpacity.value = cssNum('--u-cut-op', .55);
      pktMat.uniforms.uColor.value.copy(cssColor('--u-fast'));
      pktMat.uniforms.uOpacity.value = cssNum('--u-pkt-op', 1);
      pktMat.uniforms.uSize.value = cssNum('--u-pkt-size', 8);
      [fastMat, cutMat, pktMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0;
        m.uniforms.uBack.value = .62; setBlend(m, cssNum('--u-add', 0)); });
      [strA, strB].forEach(st => setBlend(st.mat, cssNum('--u-add', 0)));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑫ 产品大图 · 分层深度化（P10 · **谨慎页**）
   ───────────────────────────────────────────────────────────────────────────
   本页是全 deck 标注密度最高的一张图（三十余处标签 / 角标 / 图例 / 三枚数字锚点）。
   所以这一枚场景的第一条纪律不是「立体」，是「**一格不许挪**」：
     · 每一只盒的**前面**走投影锁 ⇒ 与它替换掉的那只 SVG 盒逐像素重合，
       盒上的名字、盒边的角标、车道上的注，全部照旧对得上；
     · 立体感只从三处来 —— ① 五个带各在自己的深度（上行 / 中枢 / 下行 / 底座 /
       客户控制面），深度雾把它们分开；② 盒沿 −z 背向拉伸，看得见侧壁；
       ③ 层与层之间的连线**真的在深度里走**（编排↔LLM、SOS/EOS、打断快路径、
       底座 ↔ 车道），包沿线穿行时近大远小。
     · **相机不动、层不做视差位移** —— 微视差每移一个像素，就有一处标注开始指空。
       可读性第一：这一页的 3D 是「同一张图有了厚度」，不是「同一张图动起来了」。
   大图几何一格未动：盒表 / 车道 y / 包相位全部读页上那几张常量表。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeBigmap(ctx){
  const Q = K.m, w = ctx.rect[2], h = ctx.rect[3], D = 1600;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 230), L = mkLock(w, h, D);
  const faceM = [], shellM = [];
  const face = [[], [], [], [], []], shell = [[], [], [], [], []];
  Q.box.forEach((b) => {                       // b = [x,y,w,h,层,hot]
    const z = Q.zl[b[4]];
    const bb = boxBody(b[0], b[1], b[2], b[3], z, Q.dz, L);
    face[b[4]].push.apply(face[b[4]], bb.front);
    shell[b[4]].push.apply(shell[b[4]], bb.shell);
  });
  Q.ring.forEach((c) => {                      // MIC / SPK 两枚环
    const z = Q.zl[c[3]], acc = [];
    for(let i = 0; i < 36; i++){
      const a0 = i / 36 * TAU, a1 = (i + 1) / 36 * TAU;
      const p0 = L(c[0] + Math.cos(a0)*c[2], c[1] + Math.sin(a0)*c[2], z);
      const p1 = L(c[0] + Math.cos(a1)*c[2], c[1] + Math.sin(a1)*c[2], z);
      acc.push([p0[0],p0[1],p0[2], p1[0],p1[1],p1[2]]);
    }
    face[c[3]].push.apply(face[c[3]], acc);
  });
  for(let l = 0; l < 5; l++){
    [[face[l], faceM], [shell[l], shellM]].forEach(([segs, bag]) => {
      if(!segs.length) { bag.push(null); return; }
      const g = segGeo(segs); fillAH(g, 1, 0);
      const m = mkMat(SH, PX_LN_VS, PX_LN_FS);
      bag.push(m);
      scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
    });
  }
  // ── 车道 / 层间连线：全部是真的在深度里走的线 ──
  const laneMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const beamMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const lanes = [], beams = [];
  Q.lane.forEach((s) => {                      // s = [x0,x1,y,层]
    const a = L(s[0], s[2], Q.zl[s[3]]), b = L(s[1], s[2], Q.zl[s[3]]);
    lanes.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
  });
  Q.beam.forEach((s) => {                      // s = [x0,y0,层0, x1,y1,层1]
    const a = L(s[0], s[1], Q.zl[s[2]]), b = L(s[3], s[4], Q.zl[s[5]]);
    beams.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
  });
  [[lanes, laneMat], [beams, beamMat]].forEach(([segs, m]) => {
    const g = segGeo(segs); fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
  });
  /* ── 波B 轻手术：介质 → **流带**（lab-kit ⑨），离散事件 → **保持粒子** ──────
     判据逐条写在 _P10LANE / _P10BEAM 的 med 列上（接入指南 ⑨）：
       · 一直在来的（上行 / 下行 / 底座两条车道，实时编排⇄LLM / AEC 参考环 /
         底座两道握手）是介质 ⇒ 一条有厚度、会起伏、波峰自己往前走的带子；
       · 有起点有终点、发生一次就结束的（SOS·EOS 事件线、打断快路径、
         客户控制面）是事件 ⇒ 粒子留着，这三条**不动**。
     带子的中心线**逐点走投影锁**、与它替换掉的那条车道逐像素同位 ⇒ **零位移**。 */
  const flows = [];
  function addFlow(a, b, spd){
    const n = 48, pts = [];
    for(let i = 0; i < n; i++){
      const t = i/(n-1);
      pts.push(L(a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t, a[2] + (b[2]-a[2])*t));
    }
    const st = mkStream(SH, pts, { w: Q.floww, spd, edge: .06 }).add(scene);
    flows.push(st);
  }
  { let k = 0;
    Q.medL.forEach((i) => { const s = Q.lane[i], z = Q.zl[s[3]];
      addFlow([s[0], s[2], z], [s[1], s[2], z], Q.spd[k++]); });
    Q.medB.forEach((i) => { const s = Q.beam[i];
      addFlow([s[0], s[1], Q.zl[s[2]]], [s[3], s[4], Q.zl[s[5]]], Q.spd[k++]); }); }
  // ── 包：只剩**离散事件**那三条（车道与握手已经换成流带）──
  const RUN = Q.lane.filter(s => !s[6])
    .map(s => ({ a:[s[0], s[2], Q.zl[s[3]]], b:[s[1], s[2], Q.zl[s[3]]], T:s[4], n:s[5] }))
    .concat(Q.beam.filter(s => !s[8])
      .map(s => ({ a:[s[0], s[1], Q.zl[s[2]]], b:[s[3], s[4], Q.zl[s[5]]], T:s[6], n:s[7] })));
  const NP = RUN.reduce((n, r) => n + r.n, 0);
  const pg = new THREE.BufferGeometry();
  const ppos = new Float32Array(NP * 3);
  pg.setAttribute('position', new THREE.BufferAttribute(ppos, 3));
  const pA = fillAH(pg, 1, 0);
  const pktMat = mkMat(SH, PX_PT_VS, PX_PT_FS); pktMat.uniforms.uSoft.value = .035;
  scene.add(Object.assign(new THREE.Points(pg, pktMat), { frustumCulled:false }));
  return {
    scene, camera, intro: 1.4, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    // evt 只数**真的有包**的那几条；n=0 的那一条是「端到端 650ms」的尺，不是事件
    state(){ return { flows: flows.length, evt: RUN.filter(r => r.n > 0).length,
                      ruler: RUN.filter(r => r.n === 0).length, drift: 0,
                      spd: flows.map(f => f.spd) }; },
    draw(dt, clock){
      SH.uTime.value = clock;
      let k = 0;
      RUN.forEach((r) => {
        for(let i = 0; i < r.n; i++){
          const u = ((clock / r.T) + i / r.n) % 1;
          const q = L(r.a[0] + (r.b[0]-r.a[0])*u, r.a[1] + (r.b[1]-r.a[1])*u,
                      r.a[2] + (r.b[2]-r.a[2])*u);
          ppos[k*3] = q[0]; ppos[k*3+1] = q[1]; ppos[k*3+2] = q[2];
          pA.a[k] = Math.min(1, Math.min(u, 1-u) * 10); k++;
        }
      });
      pg.attributes.position.needsUpdate = true; pg.attributes.aA.needsUpdate = true;
      flows.forEach(st => st.draw(clock));
      if(faceM[0]) faceM[0].uniforms.uGain.value = .35 + .35 * Math.sin(clock * TAU / Q.beat);
    },
    applyTheme(){
      const fc = cssColor('--m-face'), hc = cssColor('--m-hot'), sc = cssColor('--m-shell');
      faceM.forEach((m, l) => { if(!m) return;
        m.uniforms.uColor.value.copy(fc); m.uniforms.uHot.value.copy(hc);
        m.uniforms.uOpacity.value = cssNum('--m-face-op', .85) * Q.lop[l];
        m.uniforms.uGain.value = 0; });
      shellM.forEach((m, l) => { if(!m) return;
        m.uniforms.uColor.value.copy(sc); m.uniforms.uHot.value.copy(sc);
        m.uniforms.uOpacity.value = cssNum('--m-shell-op', .26) * Q.lop[l];
        m.uniforms.uGain.value = 0; });
      laneMat.uniforms.uColor.value.copy(cssColor('--m-lane'));
      laneMat.uniforms.uOpacity.value = cssNum('--m-lane-op', .8);
      beamMat.uniforms.uColor.value.copy(cssColor('--m-beam'));
      beamMat.uniforms.uOpacity.value = cssNum('--m-beam-op', .6);
      pktMat.uniforms.uColor.value.copy(cssColor('--m-pkt'));
      pktMat.uniforms.uOpacity.value = cssNum('--m-pkt-op', .95);
      pktMat.uniforms.uSize.value = cssNum('--m-pkt-size', 6.5);
      [laneMat, beamMat, pktMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0; });
      faceM.concat(shellM, [laneMat, beamMat, pktMat]).forEach(m => {
        if(m){ m.uniforms.uBack.value = .62; setBlend(m, cssNum('--m-add', 0)); } });
      flows.forEach(st => { st.theme(cssColor('--m-flow'), cssColor('--m-flow-rms'),
        cssNum('--m-flow-op', .34), cssNum('--m-flow-rms-op', .55), .62);
        setBlend(st.mat, cssNum('--m-add', 0)); });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑬ 弱网 AI QoS · 囤着播（P11）
   ───────────────────────────────────────────────────────────────────────────
   本页要证的是一句因果：**网络好的时候多下发的包，够断网的时候继续播**。
   3D 把「囤」画成一个真的堆：
     · 上方是下行 AI 语音包的密集流 —— 一枚枚包从网络带往下落进缓存堆；
       断网段（页上那条既有的暗带）上游**停发**，那一段没有一枚包落下来。
     · 缓存堆 = 页上那条蓄水折线本人（x 是时间轴，一格不许挪）挤出成一堆点：
       正常段堆满、断网段肉眼可见地矮下去、恢复后重新堆起来。
     · 堆底持续往下放包，汇进下方那条**永不中断**的对话带 ——
       上游停了、堆在矮下去，而下游的包流一枚没断。这就是「囤着播」的立体证据。
   两个数字（80% / 3–5s）与所有标注仍是页上的 DOM 字，一个没动、也没新造第三个。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeQos(ctx){
  const Q = K.q, w = ctx.rect[2], h = ctx.rect[3], D = 1300;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 140), L = mkLock(w, h, D);
  const hp = unpackPoly(Q.heap);                 // 蓄水折线（页上那条 polygon 的上沿）
  function topAt(x){                             // 堆顶 y（线性插值：折线是页上的原线）
    const n = hp.length / 2;
    if(x <= hp[0]) return hp[1];
    for(let i = 1; i < n; i++){
      if(x <= hp[i*2]){
        const t = (x - hp[i*2-2]) / ((hp[i*2] - hp[i*2-2]) || 1);
        return hp[i*2-1] + (hp[i*2+1] - hp[i*2-1]) * t;
      }
    }
    return hp[n*2-1];
  }
  const dark = (x) => x >= Q.dark[0] && x <= Q.dark[0] + Q.dark[1];
  // ── 缓存堆：一团按堆顶剖面填出来的点云（x 时间轴 · y 堆高 · z 厚度）──
  const HN = Q.hn, hpos = new Float32Array(HN * 3);
  const hgeo = new THREE.BufferGeometry();
  hgeo.setAttribute('position', new THREE.BufferAttribute(hpos, 3));
  const hA = fillAH(hgeo, 1, 0);
  for(let i = 0; i < HN; i++){
    const x = Q.hx0 + (Q.hx1 - Q.hx0) * h1(i, 12.9898);
    const ty = topAt(x), y = ty + (Q.hbot - ty) * h1(i, 78.233);
    const z = (h1(i, 41.17) - .5) * 2 * Q.hz;
    const q = L(x, y, z);
    hpos[i*3] = q[0]; hpos[i*3+1] = q[1]; hpos[i*3+2] = q[2];
    hA.a[i] = .55 + .45 * (1 - (y - ty) / Math.max(1, Q.hbot - ty));
    hA.h[i] = dark(x) ? 1 : 0;                    // 断网段的存货走 hot 色：正在被吃掉
  }
  hgeo.attributes.aA.needsUpdate = true; hgeo.attributes.aH.needsUpdate = true;
  const heapMat = mkMat(SH, PX_PT_VS, PX_PT_FS); heapMat.uniforms.uSoft.value = .06;
  scene.add(Object.assign(new THREE.Points(hgeo, heapMat), { frustumCulled:false }));
  // ── 上游网络：一排包条（收到的 = 实块 / 丢掉的 = 空框）+ 两块战场 + 两只机制盒 ──
  //    这三件都是页上原来那张图的骨架，3D 不许只画一个堆就算完 ——
  //    「80% 丢包」与「3–5s 断网」两个数字得有各自的图形依据。
  const barMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const lostMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const domMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const mechMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const mechHot = mkMat(SH, PX_LN_VS, PX_LN_FS);
  { const got = [], lost = [], dom = [], mech = [], mhot = [];
    Q.bar.forEach((b2) => {                       // b2 = [x, 收到?]
      const bb = boxBody(b2[0], Q.by, Q.bw, Q.bh, Q.bz, Q.bdz, L);
      (b2[1] ? got : lost).push.apply(b2[1] ? got : lost, bb.front);
      if(b2[1]) got.push.apply(got, bb.shell);
    });
    Q.dom.forEach((d) => {                        // 两块战场：只画竖框（压暗）
      dom.push.apply(dom, segsOfLoop(rectPts(d[0], d[1], d[2], d[3], Q.domz, L)));
    });
    Q.mech.forEach((m2) => {                      // 两只机制盒（AI QoS 那只是 hot）
      const bb = boxBody(m2[0], m2[1], m2[2], m2[3], Q.mz, Q.bdz, L);
      (m2[4] ? mhot : mech).push.apply(m2[4] ? mhot : mech, bb.front);
      mech.push.apply(mech, bb.shell);
    });
    [[got, barMat], [lost, lostMat], [dom, domMat], [mech, mechMat], [mhot, mechHot]]
      .forEach(([segs, m]) => {
        const g = segGeo(segs); fillAH(g, 1, 0);
        scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
      }); }
  // ── 堆的轮廓线（页上那条折线本人）+ 缓存盒的四边 ──
  const wireMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  { const segs = [], n = hp.length / 2;
    for(let i = 0; i < n - 1; i++){
      const a = L(hp[i*2], hp[i*2+1], Q.hz), b = L(hp[i*2+2], hp[i*2+3], Q.hz);
      segs.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
      const c = L(hp[i*2], hp[i*2+1], -Q.hz), d = L(hp[i*2+2], hp[i*2+3], -Q.hz);
      segs.push([c[0],c[1],c[2], d[0],d[1],d[2]]);
    }
    segs.push.apply(segs, boxBody(Q.bin[0], Q.bin[1], Q.bin[2], Q.bin[3], 0, Q.hz*2, L).front);
    const g = segGeo(segs); fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.LineSegments(g, wireMat), { frustumCulled:false })); }
  // ── 上游包雨（断网段没有一枚）+ 下游包流（一枚不断）──
  const RAIN = [], OUTN = Q.outn;
  for(let k = 0; k < Q.rain.length; k++) if(!dark(Q.rain[k])) RAIN.push(Q.rain[k]);
  const NP = RAIN.length + OUTN;
  const pg = new THREE.BufferGeometry();
  const ppos = new Float32Array(NP * 3);
  pg.setAttribute('position', new THREE.BufferAttribute(ppos, 3));
  const pA = fillAH(pg, 1, 0);
  const pktMat = mkMat(SH, PX_PT_VS, PX_PT_FS); pktMat.uniforms.uSoft.value = .03;
  scene.add(Object.assign(new THREE.Points(pg, pktMat), { frustumCulled:false }));
  // ── 下方那条永不中断的对话带（页上那条波浪本人）──
  const outMat = mkMat(SH, PX_RB_VS, PX_RB_FS, { uFlow:{ value: 6 } });
  const wp = unpackPoly(Q.wave), wc = polyCum(wp), tmp = [0,0];
  { const pts = [];
    for(let i = 0; i < 160; i++){ polyAt(wp, wc, i / 159, tmp);
      pts.push(L(tmp[0], tmp[1], Q.wz)); }
    const g = ribbonGeo(pts, () => Q.ww); fillAH(g, 1, 0);
    outMat.side = THREE.DoubleSide;
    scene.add(Object.assign(new THREE.Mesh(g, outMat), { frustumCulled:false })); }
  return {
    scene, camera, intro: 1.3, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      let k = 0;
      RAIN.forEach((x, i) => {                    // 上游：落进堆里（断网段一枚都没有）
        const u = ((clock / Q.rdur) + h1(i, 5.11)) % 1;
        const y = Q.ry0 + (topAt(x) - Q.ry0) * u;
        const q = L(x, y, (h1(i, 9.7) - .5) * Q.hz);
        ppos[k*3] = q[0]; ppos[k*3+1] = q[1]; ppos[k*3+2] = q[2];
        pA.a[k] = Math.min(1, (1 - u) * 4); pA.h[k] = 0; k++;
      });
      for(let i = 0; i < OUTN; i++){               // 下游：从堆底一路放到对话带，永不中断
        const u = ((clock / Q.odur) + i / OUTN) % 1;
        const x = Q.hx0 + (Q.hx1 - Q.hx0) * u;
        const y = Q.hbot + (Q.wy - Q.hbot) * Math.min(1, u * 1.6);
        const q = L(x, y, (h1(i, 3.3) - .5) * Q.hz);
        ppos[k*3] = q[0]; ppos[k*3+1] = q[1]; ppos[k*3+2] = q[2];
        pA.a[k] = 1; pA.h[k] = dark(x) ? 1 : 0; k++;
      }
      pg.attributes.position.needsUpdate = true;
      pg.attributes.aA.needsUpdate = true; pg.attributes.aH.needsUpdate = true;
      mechHot.uniforms.uGain.value = .4 + .4 * Math.sin(clock * TAU / 3.4);
    },
    applyTheme(){
      barMat.uniforms.uColor.value.copy(cssColor('--q-bar'));
      barMat.uniforms.uOpacity.value = cssNum('--q-bar-op', .8);
      lostMat.uniforms.uColor.value.copy(cssColor('--q-lost'));
      lostMat.uniforms.uOpacity.value = cssNum('--q-lost-op', .3);
      domMat.uniforms.uColor.value.copy(cssColor('--q-dom'));
      domMat.uniforms.uOpacity.value = cssNum('--q-dom-op', .22);
      mechMat.uniforms.uColor.value.copy(cssColor('--q-mech'));
      mechMat.uniforms.uOpacity.value = cssNum('--q-mech-op', .55);
      mechHot.uniforms.uColor.value.copy(cssColor('--q-hot2'));
      mechHot.uniforms.uHot.value.copy(cssColor('--q-hot2'));
      mechHot.uniforms.uOpacity.value = cssNum('--q-mechhot-op', 1);
      [barMat, lostMat, domMat, mechMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0; });
      heapMat.uniforms.uColor.value.copy(cssColor('--q-heap'));
      heapMat.uniforms.uHot.value.copy(cssColor('--q-hot'));
      heapMat.uniforms.uOpacity.value = cssNum('--q-heap-op', .7);
      heapMat.uniforms.uSize.value = cssNum('--q-heap-size', 3.4);
      heapMat.uniforms.uGain.value = .5;
      wireMat.uniforms.uColor.value.copy(cssColor('--q-wire'));
      wireMat.uniforms.uHot.value.copy(cssColor('--q-wire'));
      wireMat.uniforms.uOpacity.value = cssNum('--q-wire-op', .5);
      wireMat.uniforms.uGain.value = 0;
      pktMat.uniforms.uColor.value.copy(cssColor('--q-pkt'));
      pktMat.uniforms.uHot.value.copy(cssColor('--q-hot'));
      pktMat.uniforms.uOpacity.value = cssNum('--q-pkt-op', .95);
      pktMat.uniforms.uSize.value = cssNum('--q-pkt-size', 6);
      pktMat.uniforms.uGain.value = .6;
      outMat.uniforms.uColor.value.copy(cssColor('--q-out'));
      outMat.uniforms.uHot.value.copy(cssColor('--q-out'));
      outMat.uniforms.uOpacity.value = cssNum('--q-out-op', .7);
      outMat.uniforms.uGain.value = 0;
      [heapMat, wireMat, pktMat, outMat, barMat, lostMat, domMat, mechMat, mechHot]
        .forEach(m => { m.uniforms.uBack.value = .62; setBlend(m, cssNum('--q-add', 0)); });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑭ 视觉模态 · 相机视锥（P12）
   ───────────────────────────────────────────────────────────────────────────
   页上「智能眼镜 → 看图识景 → 对话引擎」这一路，3D 里长成一只**相机视锥**：
   锥顶落在眼镜 chip 上，锥口张在「看图识景」那只卡上；一枚**画面平面**
   顺着视锥往里推，穿过卡口、进入对话流 —— 「看见的东西真的进了这场对话」。
   右侧「表达 · OUT」那一路保持既有配重（加重的实线通道 + 包），
   底部次级带（声纹锁定 / SIP · 前文已述）**保持弱化**：更暗、更远、无包 ——
   页上把它降权了，3D 不许把它捡回来。数字人 / 眼镜等端点仍是页上的 DOM / poster。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeVision(ctx){
  const Q = K.w, w = ctx.rect[2], h = ctx.rect[3], D = 1400;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 180), L = mkLock(w, h, D);
  const faceMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const hotMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const shellMat= mkMat(SH, PX_LN_VS, PX_LN_FS);
  const coneMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const planeMat= mkMat(SH, PX_LN_VS, PX_LN_FS);
  const weakMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const face = [], hotF = [], shell = [], weak = [];
  Q.box.forEach((b) => {                          // b = [x,y,w,h,z,hot]
    const bb = boxBody(b[0], b[1], b[2], b[3], b[4], Q.dz, L);
    (b[5] ? hotF : face).push.apply(b[5] ? hotF : face, bb.front);
    shell.push.apply(shell, bb.shell);
  });
  Q.weak.forEach((b) => {                          // 次级带：只画前框，压暗、退到最远
    weak.push.apply(weak, segsOfLoop(rectPts(b[0], b[1], b[2], b[3], Q.zWeak, L)));
  });
  Q.wline.forEach((s) => {
    const a = L(s[0], s[1], Q.zWeak), b = L(s[2], s[3], Q.zWeak);
    weak.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
  });
  // ── 相机视锥：锥顶（眼镜）→ 锥口（看图识景卡口），四条棱 + 两圈框 ──
  const cone = [];
  { const ap = L(Q.apex[0], Q.apex[1], Q.zApex);
    const m = Q.mouth;
    [[m[0],m[1]],[m[0]+m[2],m[1]],[m[0]+m[2],m[1]+m[3]],[m[0],m[1]+m[3]]].forEach((c) => {
      const q = L(c[0], c[1], Q.zMouth);
      cone.push([ap[0],ap[1],ap[2], q[0],q[1],q[2]]);
    });
    cone.push.apply(cone, segsOfLoop(rectPts(m[0], m[1], m[2], m[3], Q.zMouth, L)));
    // ⚠ 曾经在半程再套过一圈「壁」——它正好压在「理解图片视频」那行字上，
    //   可读性第一 ⇒ 撤掉。视锥只留四条棱 + 锥口一圈，语义一样完整。
  }
  [[face, faceMat], [hotF, hotMat], [shell, shellMat], [cone, coneMat], [weak, weakMat]]
    .forEach(([segs, m]) => {
      const g = segGeo(segs); fillAH(g, 1, 0);
      scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
    });
  // ── 画面平面：沿视锥轴往里推，进入对话流（一枚会飞的四边形框）──
  const planeGeo = segGeo(segsOfLoop(rectPts(0, 0, 1, 1, 0, (a,b,c)=>[a,-b,c])));
  fillAH(planeGeo, 1, 1);
  const planePos = planeGeo.attributes.position;
  scene.add(Object.assign(new THREE.LineSegments(planeGeo, planeMat), { frustumCulled:false }));
  // ── 通道上的包（左进右出，保持页上的配重）──
  const RUN = Q.run.map(s => ({ a:[s[0], s[1], s[2]], b:[s[3], s[4], s[5]], T:s[6], n:s[7] }));
  const NP = RUN.reduce((n, r) => n + r.n, 0);
  const pg = new THREE.BufferGeometry();
  const ppos = new Float32Array(NP * 3);
  pg.setAttribute('position', new THREE.BufferAttribute(ppos, 3));
  const pA = fillAH(pg, 1, 0);
  const pktMat = mkMat(SH, PX_PT_VS, PX_PT_FS); pktMat.uniforms.uSoft.value = .03;
  scene.add(Object.assign(new THREE.Points(pg, pktMat), { frustumCulled:false }));
  return {
    scene, camera, intro: 1.2, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      // 画面平面：从锥口出发、沿轴推进到引擎里（t 循环）
      const t = (clock / Q.pdur) % 1;
      const m = Q.mouth, hub = Q.hub;
      const ease = t * t * (3 - 2 * t);
      const cx0 = m[0] + m[2]/2, cy0 = m[1] + m[3]/2;
      const cx1 = hub[0] + hub[2]/2, cy1 = hub[1] + hub[3]/2;
      const cx = cx0 + (cx1 - cx0) * ease, cy = cy0 + (cy1 - cy0) * ease;
      const sw = (m[2] * (1 - ease) + hub[3] * .62 * ease) / 2;
      const sh2 = (m[3] * (1 - ease) + hub[3] * .5 * ease) / 2;
      const z = Q.zMouth + (Q.zHub - Q.zMouth) * ease;
      const cs = [[cx-sw, cy-sh2], [cx+sw, cy-sh2], [cx+sw, cy+sh2], [cx-sw, cy+sh2], [cx-sw, cy-sh2]];
      for(let i = 0; i < 4; i++){
        const a = L(cs[i][0], cs[i][1], z), b = L(cs[i+1][0], cs[i+1][1], z);
        planePos.array[i*6] = a[0]; planePos.array[i*6+1] = a[1]; planePos.array[i*6+2] = a[2];
        planePos.array[i*6+3] = b[0]; planePos.array[i*6+4] = b[1]; planePos.array[i*6+5] = b[2];
      }
      planePos.needsUpdate = true;
      // 画面平面走到盒子上方时压暗到三成：卡里的字优先（本页的 3D 不许压任何一行字）
      const overBox = Q.box.some(bx => cx > bx[0] - 10 && cx < bx[0] + bx[2] + 10);
      planeMat.uniforms.uOpacity.value = cssNum('--w-plane-op', .9)
        * Math.min(1, Math.min(t, 1-t) * 6) * (overBox ? .3 : 1);
      let k = 0;
      RUN.forEach((r) => {
        for(let i = 0; i < r.n; i++){
          const u = ((clock / r.T) + i / r.n) % 1;
          const q = L(r.a[0] + (r.b[0]-r.a[0])*u, r.a[1] + (r.b[1]-r.a[1])*u,
                      r.a[2] + (r.b[2]-r.a[2])*u);
          ppos[k*3] = q[0]; ppos[k*3+1] = q[1]; ppos[k*3+2] = q[2];
          pA.a[k] = Math.min(1, Math.min(u, 1-u) * 10); k++;
        }
      });
      pg.attributes.position.needsUpdate = true; pg.attributes.aA.needsUpdate = true;
      hotMat.uniforms.uGain.value = .4 + .4 * Math.sin(clock * TAU / Q.beat);
    },
    applyTheme(){
      faceMat.uniforms.uColor.value.copy(cssColor('--w-face'));
      faceMat.uniforms.uOpacity.value = cssNum('--w-face-op', .8);
      hotMat.uniforms.uColor.value.copy(cssColor('--w-hot'));
      hotMat.uniforms.uHot.value.copy(cssColor('--w-hot'));
      hotMat.uniforms.uOpacity.value = cssNum('--w-hot-op', 1);
      shellMat.uniforms.uColor.value.copy(cssColor('--w-shell'));
      shellMat.uniforms.uOpacity.value = cssNum('--w-shell-op', .26);
      coneMat.uniforms.uColor.value.copy(cssColor('--w-cone'));
      coneMat.uniforms.uOpacity.value = cssNum('--w-cone-op', .45);
      planeMat.uniforms.uColor.value.copy(cssColor('--w-plane'));
      planeMat.uniforms.uHot.value.copy(cssColor('--w-plane'));
      weakMat.uniforms.uColor.value.copy(cssColor('--w-weak'));
      weakMat.uniforms.uOpacity.value = cssNum('--w-weak-op', .22);
      pktMat.uniforms.uColor.value.copy(cssColor('--w-pkt'));
      pktMat.uniforms.uOpacity.value = cssNum('--w-pkt-op', .95);
      pktMat.uniforms.uSize.value = cssNum('--w-pkt-size', 6.5);
      [faceMat, shellMat, coneMat, planeMat, weakMat, pktMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0; });
      [faceMat, hotMat, shellMat, coneMat, planeMat, weakMat, pktMat]
        .forEach(m => { m.uniforms.uBack.value = .62; setBlend(m, cssNum('--w-add', 0)); });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑮ 编排中枢机（P13 · 二轮精修 · 波B · 王冠二）
   ───────────────────────────────────────────────────────────────────────────
   终审：「现在的数据是点状移动，流向表意不清，整体呆板，需要把科技感构建出来，
   每一个模块都可以有小巧思，对整个宏大的叙事更要有感觉。」

   ── 概念：中枢不是一只会呼吸的盒，是**一台活的机器** ──────────────────────
     · **机腔深 150**（= 单元腔深 52 的 2.9 倍）：全页最大的一处尺度对比。
       腔一深，六只槽立刻读成「插在机身上的模块」，而不是「并排的六只盒」。
     · **三道逐层内缩的内肋**（37.5px 一道）：腔壁有结构，深度才是「机器内部」
       而不是「一个黑洞」。
     · **呼吸转子**坐在腔底：三枚**异面**轨道环（三张倾斜平面上的椭圆，出平面分量
       az 正负 / 大小两两不同 ⇒ 真异面；az 随时间走一趟余弦 = 翻滚，近侧远侧互换）
       + 420 点在内圈↔外圈之间迁徙的脉动。
       「实时调试 / 一键发布」不写第二遍字，**写在转子的脉动里**：每 4.4s 一记
       发布脉冲从转子下缘出发，沿页上 vline(840,348,398) 注光进发布槽。

   ── 终审硬伤一：核压字 ⇒ 核**放大到字之外**（2026-09-01 定点修复）────────────
   原来核坐在机腔的几何中心 —— 而「对话引擎 / 实时编排」两行字正坐在那里。
   三枚法向两两正交的异面环里**必有一枚是侧着的**，侧着的圆投影成一条直线段，
   正好从「引擎」两个字里竖着劈过去；420 点是实心球，投影必然盖住中心。
   把它调暗是回避不是修 —— 那等于承认这台机器的心脏画错了地方。
   修法是**换位置不是换亮度**：半径放大到字盒之外，核成为环抱两行字的一台转子，
   读成「引擎的核心里坐着这两行字」，语义比原来更准、量级也没缩水（占满整只机腔）。
   发布脉冲的起点同步从腔心 (840,260) 挪到转子下缘 (840,336)。
   硬指标：转子的任何一处可见几何（环 / 粒子 / 粒径 / 注光路径）与两行墨迹盒
   净空 **≥16px**，墨迹盒与贯通流的 ghost 窗口同源。两道机器证明：
     · 构建期 `_k_orb_clear()` 逐点解析断言（环翻滚一整趟 × 整条粒子带 × 呼吸两档）；
     · 运行时 `state().clr` 把**这一帧真的传上去的那批顶点**投影回舞台像素重量一遍，
       qa ⑲p13 在一整个呼吸 / 翻滚周期上逐帧断言。

   ── 六枚模块各一处小巧思（全部画在槽名两侧 96px 净区内，一个字都不压）──────
     ASR 声波进 / 字节出 ｜ LLM 深部巨核 ｜ TTS 字节进 / 波形出 ｜
     数字人 口型光环 ｜ 视觉理解 扫描线 + 视锥 ｜ 知识库·RAG 检索光脉
   净区是量出来的：模块板内宽 352，槽名居中占中段 ⇒ 左右各留 96px 的空白。
   小巧思只许住在这两格里 —— 「每个模块都有小巧思」不能以压字为代价。

   ── 贯通流：一条 audioStream 走完全程 ────────────────────────────────────
   语音 → ASR → 左总线 → 中枢 → **发布槽**（左端伸出舞台外，右端落在发布槽右缘）。
   它是**介质**（语音一直在来），所以是带子不是包（接入指南 ⑨）。
   穿模块、穿字段的那几段走 **aG ghost**：剖面收成细线 ⇒ 流不断，字读得清。

   ── 终审硬伤二：糊成污迹 + 漏出舞台（2026-09-01 定点修复）────────────────────
   ① 落点：右端原来伸到页上 x1840 —— 越过版心右缘 1800 流向虚空，「流要有落点」
      当场破。改成终结在**发布槽右缘**（页 1180）：到「一键发布」为止就是全部语义；
      两端各 22px 渐隐收口（_AS_EDGE 那条通道）：左端在版心之外就收满 ⇒ 边上那一刀
      是画框，不是笔尖；右端落在发布槽右缘，是真正的收口。
   ② 形态：幅度档相对这条路径的尺度过大（半宽 11 + 地板 .30 ⇒ 最窄也有七成宽）
      ⇒ 读成一朵云不是一条波。**只在本页 opt 里**覆写半宽 8 / 地板 .12 /
      λ = 全长 ÷ 12 ≈ 120px（包络两端的宽度比 3.3× → 8.3×；λ 由「被 ghost 切出来的
      最长一段净跨度 220px」反推 —— 每一段里都要装得下一个半波峰），
      让位档反抬到 .075（8×.075 = 11×.055 ⇒ 细线的绝对粗细一格没变）。
      lab-kit ⑨ 的 `_AS_*` 全局常量一个字没动 —— 别的七页逐像素不变。
   窗口是构建期从页上的墨迹框算出来的弧长区间（K.k.gz），运行时只做一次连乘 ——
   **零分支**。中枢⇄LLM、中枢⇄TTS 两条往返闭环**分居总线 ±8px**，
   一条走左、一条走右，「往返」在图上分得开。

   ── 热切换 = 灵魂帧 ────────────────────────────────────────────────────
   在位机体沿 −z 退到 **−320** 并淡出、候选从景深进坞，走的是**真的 position.z
   位移**（不是重新投影锁）—— 所以近大远小是真的，退场是「退进机器里」。
   一进一出**错峰**（退场吃相位 0→0.58 / 进场吃 0.42→1）：交接的那一段两具机体
   同时在场，读得出「先接上再断开」而不是「闪一下换人」。
   候选的**末程**把色与不透明度收敛成在位机体 ⇒ 轮次交界无缝。

   ⚑ **贯通流不透明度与 swap 相位代码上零耦合**：uOpacity 只在 applyTheme() 里
     被赋值一次（读 --k-flow-op），draw() 一个字都不碰它。这是「模型会换代，
     接口不换人」的机制级证明 —— qa 的 ⑲p13 在整个切换窗口**逐帧**断言
     data-lab-flow 恒 .26(light)/.24(dark)、data-lab-run 恒真。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeSlots(ctx){
  const Q = K.k, w = ctx.rect[2], h = ctx.rect[3], D = 1500;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 200), L = mkLock(w, h, D);
  /* ⚑ 投影锁的代价：它把 (D−z)/D 的预缩放**正好除回去** ⇒ 锁住的件无论多深都
     不会变小。腔底的呼吸核、模块里的「深部巨核」、视锥这几件要的正是「真的退远」，
     所以走 LZ：**按腔口 / 板面预缩放，坐在真实深度上** ⇒ 净缩放 (D−zref)/(D−z) < 1。
     （盒体不需要它 —— extrudeBack 的后面已经天然是这个比例。） */
  const LZ = (x, y, z, zref) => { const q = L(x, y, zref); q[2] = z; return q; };
  const ST = ctx.stage;
  const sockMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const wallMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const hubMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const ribMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const busMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const sock = [], wall = [], hub = [], bus = [], rib = [];
  Q.slot.forEach((s) => {                          // s = [x,y,w,h]
    const bb = boxBody(s[0], s[1], s[2], s[3], Q.zSlot, Q.cav, L);
    sock.push.apply(sock, bb.front);
    wall.push.apply(wall, bb.shell);
  });
  /* ── 机腔：前面锁死在页上那只中枢盒，后面沿 −z 退 150 ── */
  { const bb = boxBody(Q.hub[0], Q.hub[1], Q.hub[2], Q.hub[3], Q.zHub, Q.hubCav, L);
    hub.push.apply(hub, bb.front); wall.push.apply(wall, bb.shell);
    /* ── 三道逐层内缩的内肋：腔壁有结构 ── */
    for(let r = 1; r <= Q.rib; r++){
      const f = r / (Q.rib + 1), ix = 26*r, iy = 11*r;
      rib.push.apply(rib, segsOfLoop(rectPts(Q.hub[0]+ix, Q.hub[1]+iy,
        Q.hub[2]-ix*2, Q.hub[3]-iy*2, Q.zHub - Q.hubCav*f, L)));
    } }
  Q.bus.forEach((s) => {                           // s = [x0,y0,x1,y1]
    const a = L(s[0], s[1], Q.zBus), b = L(s[2], s[3], Q.zBus);
    bus.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
  });
  const pillMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  { const pl = segsOfLoop(rectPts(Q.pill[0], Q.pill[1], Q.pill[2], Q.pill[3], Q.zBus, L));
    Q.brk.forEach((e) => {                        // 四槽的集体括号（可替换 · 可兜底 · 可热切换）
      const a2 = L(e[0], e[1], Q.zBus), b2 = L(e[2], e[3], Q.zBus);
      pl.push([a2[0],a2[1],a2[2], b2[0],b2[1],b2[2]]);
    });
    const g = segGeo(pl); fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.LineSegments(g, pillMat), { frustumCulled:false })); }
  [[sock, sockMat], [wall, wallMat], [hub, hubMat], [bus, busMat], [rib, ribMat]]
    .forEach(([segs, m]) => {
      const g = segGeo(segs); fillAH(g, 1, 0);
      scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
    });

  /* ═══ 呼吸转子：三枚异面轨道环 + 420 点脉动（终审硬伤一的修法）═══════════
     核原来是「腔心的一团」—— 而腔心正是「对话引擎 / 实时编排」两行字的位置：
     三枚异面环里必有一枚侧着，侧着的圆投影成一条**直线段**劈过「引擎」；
     420 点是实心球，投影必然盖住中心。调暗是回避不是修。
     现在把它**放大到字盒之外**：三枚扁而宽的轨道椭圆环抱两行字，420 枚粒子在
     内圈↔外圈之间迁徙 ⇒ 读成「引擎的核心里坐着这两行字」。
     几何上是真的 3D：每一枚轨道是一张**倾斜平面上的椭圆**（出平面分量 az·sinθ
     与面内 ay·sinθ 同相 ⇒ 共面），az 三枚正负 / 大小两两不同 ⇒ 真异面；
     az 还随时间走一趟余弦（翻滚），近侧远侧因此互换，透视缩放是真的。
     净空由构建期逐点断言（_k_orb_clear ≥ K.k.clr），运行时 state().clr 复量。 */
  const CZ = Q.zHub - Q.hubCav*0.82;               // 转子坐在腔底（内肋之后）
  /* 转子中心的**预像**：投影之后正好落在两行墨迹盒并集的中心 */
  const IK = Q.ink, D_ = 1500, HCX = w/2, HCY = h/2;
  const IKX = (Math.min.apply(null, IK.map(b => b[0]))
             + Math.max.apply(null, IK.map(b => b[0]+b[2])))/2;
  const IKY = (Math.min.apply(null, IK.map(b => b[1]))
             + Math.max.apply(null, IK.map(b => b[1]+b[3])))/2;
  const CX = HCX + (IKX - HCX)*(D_-CZ)/(D_-Q.zHub);
  const CY = HCY + (IKY - HCY)*(D_-CZ)/(D_-Q.zHub);
  const coreMat = mkMat(SH, PX_PT_VS, PX_PT_FS); coreMat.uniforms.uSoft.value = .03;
  const ringMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const CN = Q.coreN, OB = Q.orb, coreGeo = new THREE.BufferGeometry();
  const cpos = new Float32Array(CN*3);
  coreGeo.setAttribute('position', new THREE.BufferAttribute(cpos,3));
  const cA = fillAH(coreGeo, 1, 0);
  /* 逐粒子的两枚固定相位：θ₀ 走黄金角（沿轨道铺得均匀、不结块）；
     ν 是「内外迁徙」的相位（与旧版 420 点脉动同一条式子，只是脉动改成**换轨道**）*/
  const cTh = new Float32Array(CN), cNu = new Float32Array(CN), cSp = new Float32Array(CN);
  { const ga = Math.PI*(3-Math.sqrt(5));
    for(let i = 0; i < CN; i++){
      // 角速度**逐粒子恒定**（含正负两向 ⇒ 带子自己剪切）：随 ν 换向会让 θ 跳变
      cTh[i] = i*ga; cNu[i] = i/CN*3;
      cSp[i] = (0.30 + 0.22*((i*7919 % 97)/96)) * (i % 2 ? 1 : -1);
    } }
  scene.add(Object.assign(new THREE.Points(coreGeo, coreMat), { frustumCulled:false }));
  /* 三枚轨道环：一枚 = 一条闭合折线（RSEG 段）。环本身不「自转」（自转在自己的
     平面里看不出来），转的是**翻滚**（az 走余弦）与环上那道**跑动的光弧**。 */
  const RSEG = 96, ringGeo = new THREE.BufferGeometry();
  const rpos = new Float32Array(3*RSEG*2*3);
  ringGeo.setAttribute('position', new THREE.BufferAttribute(rpos,3));
  const rA = fillAH(ringGeo, 1, 0);
  scene.add(Object.assign(new THREE.LineSegments(ringGeo, ringMat), { frustumCulled:false }));
  /* 粒子带 = 三枚环之间的分段线性插值（t=0 内圈 / .5 中圈 / 1 外圈）——
     与构建期 _k_orb_at() 逐字同解，净空断言因此覆盖整条带。 */
  function orbAt(t){
    const s = t <= .5 ? t*2 : (t-.5)*2;
    const a = t <= .5 ? OB[2] : OB[1], b = t <= .5 ? OB[1] : OB[0];
    return [a[0]+(b[0]-a[0])*s, a[1]+(b[1]-a[1])*s, a[2]+(b[2]-a[2])*s];
  }
  /* 轨道上一点 → 世界坐标（LZ 的投影锁 + 真深度）*/
  function orbPt(ax, ay, az, th, rad){
    return LZ(CX + ax*rad*Math.cos(th), CY + ay*rad*Math.sin(th),
              CZ + az*rad*Math.sin(th), Q.zHub);
  }
  /* 一枚世界点投影回舞台像素（camPx + 透视除法的解析解）—— state().clr 用它复量 */
  function toPx(X, Y, Z){
    const s = D_/(D_-Z);
    return [HCX + (X-HCX)*s, HCY + (-Y-HCY)*s];
  }
  function inkClr(X, Y, Z){
    const p = toPx(X, Y, Z); let m = 1e9;
    for(let i = 0; i < IK.length; i++){
      const r = IK[i];
      const dx = Math.max(r[0]-p[0], 0, p[0]-(r[0]+r[2]));
      const dy = Math.max(r[1]-p[1], 0, p[1]-(r[1]+r[3]));
      m = Math.min(m, Math.hypot(dx, dy));
    }
    return m;
  }

  /* ═══ 发布脉冲：从转子下缘出发，沿页上 vline(840,348,398) 注光进发布槽 ═══ */
  const pubPts = Q.pubPath.map((q, i) => i === 0 ? LZ(q[0], q[1], CZ, Q.zHub)
                                                : L(q[0], q[1], Q.zBus));
  const pubMat = mkBeamMat(SH, 30, 0.0);
  { const g = beamGeo(pubPts);
    scene.add(Object.assign(new THREE.Line(g, pubMat), { frustumCulled:false }));
    pubMat.userData = { len: g.userData.len }; }

  /* ═══ 两条往返闭环：分居总线 ±8px ═══════════════════════════════════════ */
  const loops = Q.loop.map((pl) => {
    const pts = pl.map(q => L(q[0], q[1], Q.zBus + 6));
    const m = mkBeamMat(SH, 26, 0.20), g = beamGeo(pts);
    scene.add(Object.assign(new THREE.Line(g, m), { frustumCulled:false }));
    return { m, len: g.userData.len };
  });

  /* ═══ 六枚模块小巧思 —— 全部画在槽名两侧 96px 净区里 ═══════════════════
     每一件都是「这个模块在做什么」的图示，不是装饰：
       0 ASR    左：声波进   右：字节出
       1 LLM    右：深部巨核（往腔里退的一团点 —— 参数在深处）
       2 TTS    左：字节进   右：波形出
       3 数字人 右：口型光环（三道同心环脉动）
       4 视觉   左：扫描线   右：视锥（四条棱收到一点）
       5 RAG    左：书脊架   右：检索光脉（一记横扫）                         */
  const GZW = 96, GZH = 36;
  function zone(s, side){                          // side: 0 左 / 1 右
    const x0 = s[0] + (side ? 262 : 22);
    return { x: x0, y: s[1] + 16, w: GZW, h: GZH, cx: x0 + GZW/2, cy: s[1] + 16 + GZH/2 };
  }
  function giz(i, s){
    const A = zone(s, 0), B = zone(s, 1), P = [], E = [], zp = Q.zPlate;
    // 返回 update(clock) —— 位置逐帧现算（小巧思是「活的」，不是贴纸）
    if(i === 0 || i === 2){                        // 声波 ↔ 字节（ASR / TTS 互为镜像）
      const wv = i === 0 ? A : B, by = i === 0 ? B : A;
      for(let k = 0; k < 26; k++) P.push({ kind:'wave', z:wv, u:k/25 });
      for(let r = 0; r < 3; r++) for(let c = 0; c < 6; c++)
        P.push({ kind:'byte', z:by, u:c/5, v:r/2 });
    } else if(i === 1){                            // 深部巨核
      for(let k = 0; k < 54; k++) P.push({ kind:'core', z:B, u:k/53 });
    } else if(i === 3){                            // 口型光环
      for(let r = 0; r < 3; r++) for(let k = 0; k < 22; k++)
        P.push({ kind:'halo', z:B, u:k/22, v:r });
    } else if(i === 4){                            // 扫描线 + 视锥
      for(let k = 0; k < 18; k++) P.push({ kind:'scan', z:A, u:k/17 });
      E.push({ kind:'cone', z:B });
    } else {                                       // 书脊架 + 检索光脉
      E.push({ kind:'shelf', z:A });
      for(let k = 0; k < 16; k++) P.push({ kind:'seek', z:B, u:k/15 });
    }
    return { P, E, A, B, zp };
  }
  const bodies = Q.slot.map((s, i) => {
    const G = giz(i, s);
    const np = G.P.length;
    const pg = new THREE.BufferGeometry();
    const ppos = new Float32Array(np*3);
    pg.setAttribute('position', new THREE.BufferAttribute(ppos,3));
    const pA = fillAH(pg, 1, 0);
    // 线件：模块板轮廓 + 静态小件（视锥 / 书脊）
    const segs = segsOfLoop(rectPts(s[0]+Q.pad, s[1]+Q.pad2, s[2]-Q.pad*2, s[3]-Q.pad2*2,
                                    Q.zPlate, L));
    G.E.forEach((e) => {
      if(e.kind === 'cone'){                       // 视锥：四条棱收到锥顶
        const z = e.z, ap = LZ(z.cx + 34, z.cy, Q.zPlate + 26, Q.zPlate);
        [[-1,-1],[1,-1],[1,1],[-1,1]].forEach(([sx, sy]) => {
          const c = LZ(z.cx - 20 + sx*16, z.cy + sy*13, Q.zPlate - 16, Q.zPlate);
          segs.push([c[0],c[1],c[2], ap[0],ap[1],ap[2]]);
        });
        const q = [[-1,-1],[1,-1],[1,1],[-1,1],[-1,-1]].map(([sx, sy]) =>
          LZ(z.cx - 20 + sx*16, z.cy + sy*13, Q.zPlate - 16, Q.zPlate));
        segs.push.apply(segs, segsOfLoop(q));
      } else {                                     // 书脊架：五条竖脊 + 一道横板
        const z = e.z;
        for(let k = 0; k < 5; k++){
          const x = z.x + 10 + k*18;
          const a = LZ(x, z.y + 4, Q.zPlate - k*7, Q.zPlate),
                b = LZ(x, z.y + z.h - 4, Q.zPlate - k*7, Q.zPlate);
          segs.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
        }
        const a = L(z.x + 4, z.y + z.h - 3, Q.zPlate), b = L(z.x + z.w - 4, z.y + z.h - 3, Q.zPlate);
        segs.push([a[0],a[1],a[2], b[0],b[1],b[2]]);
      }
    });
    const lg = segGeo(segs); fillAH(lg, 1, 0);
    const mkPair = (lnMat, ptMat) => {
      const gp = new THREE.Group();
      gp.add(Object.assign(new THREE.LineSegments(lg, lnMat), { frustumCulled:false }));
      gp.add(Object.assign(new THREE.Points(pg, ptMat), { frustumCulled:false }));
      scene.add(gp); return gp;
    };
    const lnIn = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ptIn = mkMat(SH, PX_PT_VS, PX_PT_FS); ptIn.uniforms.uSoft.value = .03;
    const lnCd = mkMat(SH, PX_LN_VS, PX_LN_FS);
    const ptCd = mkMat(SH, PX_PT_VS, PX_PT_FS); ptCd.uniforms.uSoft.value = .03;
    const gIn = mkPair(lnIn, ptIn), gCd = mkPair(lnCd, ptCd);
    gCd.visible = false;
    return { G, pg, ppos, pA, gIn, gCd, lnIn, ptIn, lnCd, ptCd, np };
  });
  function drawGiz(b, clock){
    const { G, ppos, pA, np } = b;
    for(let k = 0; k < np; k++){
      const it = G.P[k], z = it.z; let x = z.cx, y = z.cy, zz = G.zp, a = 1;
      if(it.kind === 'wave'){
        x = z.x + 6 + it.u*(z.w - 12);
        y = z.cy + 11*Math.sin(TAU*(it.u*1.8 - clock/1.9));
        a = .55 + .45*(0.5 - 0.5*Math.cos(TAU*(it.u - clock/1.9)));
      } else if(it.kind === 'byte'){
        x = z.x + 12 + it.u*(z.w - 24);
        y = z.y + 6 + ((it.v + clock/1.6 + it.u*0.31) % 1)*(z.h - 12);
        a = .30 + .70*(1 - Math.abs(((it.v + clock/1.6 + it.u*0.31) % 1) - .5)*2);
      } else if(it.kind === 'core'){
        const ga = Math.PI*(3-Math.sqrt(5)), yy = 1 - 2*(it.u*53+0.5)/54;
        const rr = Math.sqrt(Math.max(0,1-yy*yy)), an = it.u*53*ga + clock*0.5;
        const R = 15 + 3*Math.sin(TAU*clock/2.2);
        x = z.cx + Math.cos(an)*rr*R; y = z.cy + yy*R*0.8;
        zz = G.zp - 42 + Math.sin(an)*rr*R;        // 往腔里退 ⇒ 「深部」
        a = .45 + .55*(0.5 + 0.5*Math.sin(an));
      } else if(it.kind === 'halo'){
        const R = (7 + it.v*8) * (1 + .22*Math.sin(TAU*(clock/1.5 - it.v*0.33)));
        x = z.cx + Math.cos(TAU*it.u)*R*1.5; y = z.cy + Math.sin(TAU*it.u)*R;
        a = .32 + .68*(1 - it.v/3);
      } else if(it.kind === 'scan'){
        x = z.x + 8 + it.u*(z.w - 16);
        const sy = (clock/2.4) % 1;
        y = z.y + 5 + sy*(z.h - 10);
        a = .35 + .65*Math.max(0, 1 - Math.abs(it.u - sy)*1.2);
      } else {                                     // 检索光脉
        const sw = (clock/2.0) % 1;
        x = z.x + 6 + it.u*(z.w - 12);
        y = z.cy + 8*Math.sin(TAU*(it.u - sw));
        a = .22 + .78*Math.max(0, 1 - Math.abs(it.u - sw)*2.6);
      }
      const q = LZ(x, y, zz, G.zp);
      ppos[k*3] = q[0]; ppos[k*3+1] = q[1]; ppos[k*3+2] = q[2];
      pA.a[k] = a;
    }
    b.pg.attributes.position.needsUpdate = true;
    b.pg.attributes.aA.needsUpdate = true;
  }

  /* ═══ 贯通流：一条 audioStream 走完全程（穿模块穿字段走 aG ghost）═══════ */
  // 等弧长重采样：aG 是逐顶点属性，点疏了 ghost 窗口就落不到点上（本页 1436px ÷ 299 ≈ 4.8px 一段）
  const FLOWN = 300;
  const flowPts = resamplePoly(Q.flow, FLOWN).map(q => L(q[0], q[1], Q.zBus + 12));
  /* 幅度 / 波长 / 让位档 / 收口**全部在这只 opt 里覆写** —— lab-kit ⑨ 的 AS.* 全局档
     一个字没动（别的七页照旧吃全局值）。为什么要覆写：这条流的路径尺度比别的页短，
     全局那一档（半宽 11 · 地板 .30 · λ232）在这里读成一朵云而不是一条波。 */
  const flow = mkStream(SH, flowPts, {
    w: Q.flowW, spd: Q.flowSpd, lam: Q.flowLam,
    floor: Q.flowFloor, ghost: Q.flowGhost, edge: Q.flowEdge }).add(scene);
  /* 幅度剖面 = ghost 窗口的**连乘**（每只窗口一记 smootherstep 凹槽）—— 零分支。
     窗口本身是构建期从页上的墨迹框算出来的弧长区间：流在哪里收细，由页面决定。 */
  flow.gain((u) => {
    let g = 1;
    for(let i = 0; i < Q.gz.length; i++){
      const a = Q.gz[i][0], b = Q.gz[i][1], f = Q.gzF;
      g *= 1 - smoother(a - f, a, u)*(1 - smoother(b, b + f, u));
    }
    return g;
  });

  /* ── 总线包（离散：一次「插入」= 一枚包，接入指南 ⑨ 的事件档）── */
  const RUN = Q.run.map(s => ({ a:[s[0], s[1]], b:[s[2], s[3]], T:s[4], n:s[5] }));
  const NP = RUN.reduce((n, r) => n + r.n, 0);
  const pg2 = new THREE.BufferGeometry();
  const ppos2 = new Float32Array(NP * 3);
  pg2.setAttribute('position', new THREE.BufferAttribute(ppos2, 3));
  const pA2 = fillAH(pg2, 1, 0);
  const pktMat = mkMat(SH, PX_PT_VS, PX_PT_FS); pktMat.uniforms.uSoft.value = .03;
  scene.add(Object.assign(new THREE.Points(pg2, pktMat), { frustumCulled:false }));

  const plateCol = new THREE.Color(), gizCol = new THREE.Color(), candCol = new THREE.Color();
  let plateOp = .8, gizOp = .9;
  let flowOp = .26;                                // ← 只在 applyTheme 里被写；draw 不碰
  return {
    scene, camera, intro: 1.25, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      /* ── 呼吸转子：呼吸只**向外**涨（内界 = 基准档 ⇒ 净空的最坏情形恒在 rad=1）── */
      const beat = 0.5 - 0.5*Math.cos(TAU*clock/Q.beat);
      const rad = 1 + Q.orbBr*beat;
      // 420 枚粒子：沿轨道跑（θ）+ 在内圈↔外圈之间迁徙（ν —— 旧版 420 点脉动那条式子）
      const azb = Math.cos(TAU*clock/Q.orbRoll[1]);   // 整条带同一趟翻滚（连续 · 无跳变）
      for(let i = 0; i < CN; i++){
        const nu = 0.5 + 0.5*Math.sin(TAU*(cNu[i] - clock/2.4));
        const o = orbAt(nu);
        const q = orbPt(o[0], o[1], o[2]*azb, cTh[i] + clock*cSp[i], rad);
        cpos[i*3] = q[0]; cpos[i*3+1] = q[1]; cpos[i*3+2] = q[2];
        cA.a[i] = .30 + .70*nu;                    // 迁到外圈最亮 ⇒ 脉动看得见
      }
      coreGeo.attributes.position.needsUpdate = true;
      coreGeo.attributes.aA.needsUpdate = true;
      /* 三枚环：翻滚（az 走余弦）+ 一道**跑动的光弧**（环在转，靠它读出来）*/
      let n2 = 0;
      for(let k = 0; k < 3; k++){
        const az = OB[k][2]*Math.cos(TAU*clock/Q.orbRoll[k]);
        const arc = TAU*(clock*Q.orbArc[k]);
        for(let i = 0; i <= RSEG; i++){
          const th = i/RSEG*TAU;
          const p = orbPt(OB[k][0], OB[k][1], az, th, rad);
          // 光弧：一段 cos 亮斑绕着环跑（余晖 .22，弧心 1.0）
          const lit = .22 + .78*Math.pow(Math.max(0, Math.cos(th - arc)), 6);
          if(i > 0){
            rA.a[n2] = lit; rpos[n2*3] = p[0]; rpos[n2*3+1] = p[1]; rpos[n2*3+2] = p[2]; n2++;
          }
          if(i < RSEG){
            rA.a[n2] = lit; rpos[n2*3] = p[0]; rpos[n2*3+1] = p[1]; rpos[n2*3+2] = p[2]; n2++;
          }
        }
      }
      ringGeo.attributes.position.needsUpdate = true;
      ringGeo.attributes.aA.needsUpdate = true;
      /* ── 发布脉冲：4.4s 一记，从转子下缘注光进发布槽 ── */
      const pu = (clock % Q.pub) / Q.pub;
      pubMat.uniforms.uHead.value = sstep(0, .34, pu)*pubMat.userData.len*1.14;
      pubMat.uniforms.uRest.value = 0.06*(1 - sstep(.34, .92, pu));
      /* ── 两条往返闭环：一记脉冲去了又回来 ── */
      loops.forEach((lp2, i) => {
        const t = ((clock/(2.6 + i*0.5)) % 1);
        lp2.m.uniforms.uHead.value = t*lp2.len*1.12;
        lp2.m.uniforms.uRest.value = 0.16;
      });
      /* ── 热切换：整轮 cyc 秒换一只槽，走**真的 position.z 位移** ── */
      const round = clock / Q.cyc, who = Math.floor(round) % Q.slot.length;
      const ph = Math.max(0, Math.min(1, (round % 1) / (Q.sw / Q.cyc)));
      const eOut = smoother(Q.swA[0], Q.swA[1], ph);        // 退场（吃前段相位）
      const eIn  = smoother(Q.swB[0], Q.swB[1], ph);        // 进场（吃后段相位）—— 错峰
      /* 位移错峰、**不透明度在交叠窗口 [0.42,0.58] 里交叉** ⇒ 两具机体的可见度之和恒为 1，
         台面上永远有一具在（不做交叉的话，错峰的中点会出现一记「谁都不在」的空洞）。 */
      const xf = smoother(Q.swB[0], Q.swA[1], ph);
      bodies.forEach((b, i) => {
        drawGiz(b, clock);
        if(i !== who){
          b.gIn.position.z = 0; b.gIn.visible = true;
          b.gCd.visible = false; b.gCd.position.z = Q.swz;
          b.lnIn.uniforms.uOpacity.value = plateOp;
          b.ptIn.uniforms.uOpacity.value = gizOp;
          return;
        }
        b.gIn.position.z = Q.swz*eOut;
        b.lnIn.uniforms.uOpacity.value = plateOp*(1 - xf);
        b.ptIn.uniforms.uOpacity.value = gizOp*(1 - xf);
        b.gIn.visible = xf < 0.999;
        b.gCd.visible = xf > 0.001;
        b.gCd.position.z = Q.swz*(1 - eIn);
        // 候选的**末程**把色与不透明度收敛成在位机体 ⇒ 轮次交界无缝
        const cv = smoother(0.72, 1.0, ph);
        b.lnCd.uniforms.uOpacity.value = plateOp*xf;
        b.ptCd.uniforms.uOpacity.value = gizOp*xf;
        b.lnCd.uniforms.uColor.value.copy(candCol).lerp(plateCol, cv);
        b.ptCd.uniforms.uColor.value.copy(candCol).lerp(gizCol, cv);
      });
      let kk = 0;
      RUN.forEach((r) => {
        for(let i = 0; i < r.n; i++){
          const u = ((clock / r.T) + i / r.n) % 1;
          const q = L(r.a[0] + (r.b[0]-r.a[0])*u, r.a[1] + (r.b[1]-r.a[1])*u, Q.zBus);
          ppos2[kk*3] = q[0]; ppos2[kk*3+1] = q[1]; ppos2[kk*3+2] = q[2];
          pA2.a[kk] = Math.min(1, Math.min(u, 1-u) * 10); kk++;
        }
      });
      pg2.attributes.position.needsUpdate = true; pg2.attributes.aA.needsUpdate = true;
      flow.draw(clock);
      hubMat.uniforms.uGain.value = .4 + .4*beat;
      /* ⚑ 把**运行时**的贯通流不透明度摊到舞台上：⑲p13 逐帧读它，
         整个切换窗口必须是同一个数（与 swap 相位零耦合的机器证明）。 */
      ST.dataset.labFlow = flow.mat.uniforms.uOpacity.value.toFixed(2);
      ST.dataset.labSwapph = (who + ':' + ph.toFixed(3));   // ⚠ 别叫 labSwap：
      //   那个名字是构建期摊上去的换装时长（data-lab-swap），运行时覆盖它闸门会读到 NaN
    },
    state(){
      /* ⚑ 净空闸的量法：不是「代码看起来对」，是**把这一帧真的传上去的那批顶点**
         逐点投影回舞台像素，量到两只墨迹盒的距离。环 / 粒子 / 发布脉冲三样一起量，
         再减掉粒径的一半（点是个圆盘，不是数学点）—— 这才是「可见几何的净空」。 */
      const clrOf = () => {
        let m = 1e9;
        const half = coreMat.uniforms.uSize.value*0.5*(D_/(D_-CZ)) + 0.5;
        for(let i = 0; i < CN; i++)
          m = Math.min(m, inkClr(cpos[i*3], cpos[i*3+1], cpos[i*3+2]) - half);
        const rn = rpos.length/3;
        for(let i = 0; i < rn; i++)
          m = Math.min(m, inkClr(rpos[i*3], rpos[i*3+1], rpos[i*3+2]) - 0.5);
        // 发布脉冲：整条路径都带余光 ⇒ 整条路径都算「可见几何」，逐段密采
        for(let i = 0; i < pubPts.length-1; i++)
          for(let k = 0; k <= 40; k++){
            const t = k/40, a = pubPts[i], b2 = pubPts[i+1];
            m = Math.min(m, inkClr(a[0]+(b2[0]-a[0])*t, a[1]+(b2[1]-a[1])*t,
                                   a[2]+(b2[2]-a[2])*t) - 0.5);
          }
        return m;
      };
      const fe = toPx(flowPts[flowPts.length-1][0], flowPts[flowPts.length-1][1],
                      flowPts[flowPts.length-1][2]);
      return { flowOp: flow.mat.uniforms.uOpacity.value,
               gz: Q.gz.length, flowLen: flow.len, spd: flow.spd,
               clr: clrOf(), orb: OB.length,
               flowEnd: [ctx.rect[0] + fe[0], ctx.rect[1] + fe[1]],
               flowAmp: [flow.mat.uniforms.uW.value*Q.flowW,
                         flow.mat.uniforms.uFloor.value,
                         flow.mat.uniforms.uGhost.value,
                         flow.mat.uniforms.uLam.value],
               core: CN, ribs: Q.rib, hubCav: Q.hubCav, pub: Q.pub,
               swz: Q.swz, zIn: bodies.map(b => b.gIn.position.z),
               zCd: bodies.map(b => b.gCd.position.z),
               vis: bodies.map(b => (b.gIn.visible?1:0) + (b.gCd.visible?2:0)),
               loops: loops.length,
               // 三处探针：流的开头（畅通）/ 第一只 ghost 窗口的正中（细线）/ 窗口之后（畅通）
               gain: (() => {
                 const aT = flow.mesh.geometry.attributes.aT.array;
                 const aG = flow.mesh.geometry.attributes.aG.array;
                 const at = (u) => { let bi = 0, bd = 1e9;
                   for(let i = 0; i < aT.length; i += 2){
                     const d = Math.abs(aT[i]-u); if(d < bd){ bd = d; bi = i; } }
                   return aG[bi]; };
                 const z0 = Q.gz[0];
                 return [at(30), at((z0[0]+z0[1])/2), at(z0[1] + Q.gzF*2.4)];
               })() };
    },
    applyTheme(){
      sockMat.uniforms.uColor.value.copy(cssColor('--k-sock'));
      sockMat.uniforms.uOpacity.value = cssNum('--k-sock-op', .7);
      wallMat.uniforms.uColor.value.copy(cssColor('--k-wall'));
      wallMat.uniforms.uOpacity.value = cssNum('--k-wall-op', .26);
      ribMat.uniforms.uColor.value.copy(cssColor('--k-rib'));
      ribMat.uniforms.uOpacity.value = cssNum('--k-rib-op', .30);
      hubMat.uniforms.uColor.value.copy(cssColor('--k-hub'));
      hubMat.uniforms.uHot.value.copy(cssColor('--k-hub'));
      hubMat.uniforms.uOpacity.value = cssNum('--k-hub-op', 1);
      busMat.uniforms.uColor.value.copy(cssColor('--k-bus'));
      busMat.uniforms.uOpacity.value = cssNum('--k-bus-op', .7);
      plateCol.copy(cssColor('--k-plate')); gizCol.copy(cssColor('--k-giz'));
      candCol.copy(cssColor('--k-cand'));
      plateOp = cssNum('--k-plate-op', .8); gizOp = cssNum('--k-giz-op', .9);
      bodies.forEach((b) => {
        b.lnIn.uniforms.uColor.value.copy(plateCol);
        b.ptIn.uniforms.uColor.value.copy(gizCol);
        b.ptIn.uniforms.uSize.value = cssNum('--k-giz-size', 3.4);
        b.ptCd.uniforms.uSize.value = cssNum('--k-giz-size', 3.4);
        [b.lnIn, b.ptIn, b.lnCd, b.ptCd].forEach(m => {
          m.uniforms.uHot.value.copy(m.uniforms.uColor.value);
          m.uniforms.uGain.value = 0; m.uniforms.uBack.value = .40;
          setBlend(m, cssNum('--k-add', 0)); });
      });
      coreMat.uniforms.uColor.value.copy(cssColor('--k-core'));
      coreMat.uniforms.uHot.value.copy(cssColor('--k-core'));
      coreMat.uniforms.uOpacity.value = cssNum('--k-core-op', .8);
      coreMat.uniforms.uSize.value = cssNum('--k-core-size', 3.2);
      ringMat.uniforms.uColor.value.copy(cssColor('--k-ring'));
      ringMat.uniforms.uOpacity.value = cssNum('--k-ring-op', .55);
      pubMat.uniforms.uColor.value.copy(cssColor('--k-pub'));
      pubMat.uniforms.uHot.value.copy(cssColor('--k-pub'));
      pubMat.uniforms.uOpacity.value = cssNum('--k-pub-op', .9);
      pubMat.uniforms.uGain.value = .8;
      loops.forEach((lp2) => {
        lp2.m.uniforms.uColor.value.copy(cssColor('--k-loop'));
        lp2.m.uniforms.uHot.value.copy(cssColor('--k-pub'));
        lp2.m.uniforms.uOpacity.value = cssNum('--k-loop-op', .55);
        lp2.m.uniforms.uGain.value = .7; });
      pktMat.uniforms.uColor.value.copy(cssColor('--k-pkt'));
      pktMat.uniforms.uOpacity.value = cssNum('--k-pkt-op', .95);
      pktMat.uniforms.uSize.value = cssNum('--k-pkt-size', 6.5);
      pillMat.uniforms.uColor.value.copy(cssColor('--k-bus'));
      pillMat.uniforms.uOpacity.value = cssNum('--k-pill-op', .5);
      /* ⚑ 贯通流的不透明度**只在这里**被赋值一次 —— draw() 一个字都不碰它。
         这就是「模型会换代，接口不换人」在代码上的样子。 */
      flowOp = cssNum('--k-flow-op', .26);
      flow.theme(cssColor('--k-flow'), cssColor('--k-flow-rms'),
                 flowOp, cssNum('--k-flow-rms-op', .55), .55);
      [sockMat, wallMat, busMat, pktMat, pillMat, ribMat, coreMat, ringMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0; });
      [sockMat, wallMat, hubMat, busMat, pktMat, pillMat, ribMat,
       pubMat, flow.mat].concat(loops.map(l => l.m))
        .forEach(m => { m.uniforms.uBack.value = .55; setBlend(m, cssNum('--k-add', 0)); });
      /* 核与环坐在腔底（−203）—— 那已经越过深度雾的远端了。深度线索这里交给
         **几何**（LZ 的真透视缩小）承担，雾底放到 .88，否则核直接被雾吃掉。 */
      [coreMat, ringMat].forEach(m => { m.uniforms.uBack.value = .88;
        setBlend(m, cssNum('--k-add', 0)); });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑯ 接入架构 · 三塔握手（P14）
   ───────────────────────────────────────────────────────────────────────────
   终端设备 / 客户业务服务器 / 声网引擎云三只盒子纵深排布：终端在近、
   服务器居中、引擎云在远 —— 「谁在你手里、谁在你机房、谁在我们云上」
   在深度上直接成立（三只塔的**前面**全部锁死，域底标与盒内清单一格不挪）。
   分步：step0 只有三只塔（讲者先摆清「谁是谁」），step1 三道握手上来。

   ── 二轮精修 · 波A：三个点 → **光束生长**（mkBeamMat · 管腔注光）──────────
   终审：「P14 的流动我不喜欢：太快；三个点不像数据流。」病根不在慢一点：
   三个点没有「到达」这个动作 —— 看得见的只是「有东西在那条线上挪」，
   看不见「它到了对面」。光束生长有头、有尾、**走过留痕**：
     · 一轮 9.24s 由注光速度 400px/s 反推：三段路由 634 / 634 / 1228px
       ÷ 同一档 = 6.24s 生长（三段**等速**，qa 逐段复算）；
     · 三段全亮之后**停驻 2.00s** —— 这是本页真正的重点帧（「①②③ 都通了」）；
     · 再用 1.00s 收掉重来。6.24 + 2.00 + 1.00 = 9.24s。
   握手是**离散事件**（有起点有终点、发生一次就结束），所以它才有资格用光束
   而不是流带（接入指南 ⑨）。楼层灯瀑贴在塔的**右内缘**：不横穿塔身，
   不压任何一行字 —— 塔里那些清单行的可读性优先级高于「机房在呼吸」。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeTowers(ctx){
  const Q = K.y, w = ctx.rect[2], h = ctx.rect[3], D = 1500;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, 220), L = mkLock(w, h, D);
  const faceMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const hotMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const wallMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const face = [], hotF = [], wall = [];
  Q.tower.forEach((t) => {                          // t = [x,y,w,h,层,hot]
    const bb = boxBody(t[0], t[1], t[2], t[3], Q.z[t[4]], Q.dz, L);
    (t[5] ? hotF : face).push.apply(t[5] ? hotF : face, bb.front);
    wall.push.apply(wall, bb.shell);
  });
  Q.inner.forEach((b) => {                          // 塔内小盒：SDK / 四枚模型件
    const bb = boxBody(b[0], b[1], b[2], b[3], Q.z[b[4]] + Q.lift, Q.dz2, L);
    (b[5] ? hotF : face).push.apply(b[5] ? hotF : face, bb.front);
    wall.push.apply(wall, bb.shell);
  });
  [[face, faceMat], [hotF, hotMat], [wall, wallMat]].forEach(([segs, m]) => {
    const g = segGeo(segs); fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.LineSegments(g, m), { frustumCulled:false }));
  });
  /* ── 三道握手光束（step1）：xy 走页上那三条正交路由，z 在两塔之间拱过去 ──
     每条路由的几何带 aT（像素弧长），注光头 uHead 沿 aT 前进 ⇒ 头前余光、
     头后全亮、头本身一枚亮斑。「到达」这个动作因此是画出来的。 */
  const arcG = new THREE.Group(); arcG.visible = false; scene.add(arcG);
  const beams = [];
  Q.arc.forEach((a, i) => {                         // a = [路径串, 起层, 止层, 鼓出]
    const p = unpackPoly(a[0]), c = polyCum(p), tmp = [0,0], pts = [], NN = 160;
    for(let j = 0; j < NN; j++){
      const t = j / (NN - 1);
      polyAt(p, c, t, tmp);
      const z = Q.z[a[1]] + (Q.z[a[2]] - Q.z[a[1]]) * t + Math.sin(Math.PI * t) * a[3];
      pts.push(L(tmp[0], tmp[1], z));
    }
    const g = beamGeo(pts);
    const m = mkBeamMat(SH, Q.feather, Q.rest);
    arcG.add(Object.assign(new THREE.Line(g, m), { frustumCulled:false }));
    beams.push({ m, g, route: Q.route[i], t0: 0 });
  });
  // 三段串行：第 i 段的起跑时刻 = 前面几段的生长时间之和（**同一档速度**）
  { let acc = 0;
    beams.forEach((b) => { b.t0 = acc; acc += b.route / Q.beam; }); }
  /* ── 楼层灯瀑：贴每只塔的**右内缘**一列灯，自上而下一趟一趟地落 ──────────
     不横穿塔身（离右内缘 Q.fl），也不压任何一行字：清单行在盒内左侧。 */
  const FN = Q.tower.length * Q.fln;
  const fg = new THREE.BufferGeometry();
  const fpos = new Float32Array(FN * 3);
  fg.setAttribute('position', new THREE.BufferAttribute(fpos, 3));
  const fA = fillAH(fg, 1, 0);
  const floorMat = mkMat(SH, PX_PT_VS, PX_PT_FS); floorMat.uniforms.uSoft.value = .05;
  scene.add(Object.assign(new THREE.Points(fg, floorMat), { frustumCulled:false }));
  { let k = 0;
    Q.tower.forEach((t) => {
      for(let j = 0; j < Q.fln; j++){
        const y = t[1] + t[3] * (j + 0.5) / Q.fln;
        const q = L(t[0] + t[2] - Q.fl, y, Q.z[t[4]] + Q.lift);
        fpos[k*3] = q[0]; fpos[k*3+1] = q[1]; fpos[k*3+2] = q[2]; k++;
      }
    });
    fg.attributes.position.needsUpdate = true; }
  /* 注光头：每条路由一枚亮斑 + 两枚拖尾 —— 光束要「有头」，
     但它挂在**生长的前沿**上（不是三个自己在线上挪的点，那正是被否掉的那版）。 */
  const HN = beams.length * 3;
  const hg = new THREE.BufferGeometry();
  const hpos = new Float32Array(HN * 3);
  hg.setAttribute('position', new THREE.BufferAttribute(hpos, 3));
  const hA = fillAH(hg, 0, 1);
  const headMat = mkMat(SH, PX_PT_VS, PX_PT_FS); headMat.uniforms.uSoft.value = .03;
  arcG.add(Object.assign(new THREE.Points(hg, headMat), { frustumCulled:false }));
  let step = 0, phase = 0;
  return {
    scene, camera, intro: 1.35, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    setStep(n){ step = n; arcG.visible = n >= 1; },
    // 闸门探针：⑲(P14) 用它验「三段有序 + 全亮停驻」（不必截帧比像素）
    state(){
      return { phase, beam: Q.beam, cyc: Q.cyc, grow: Q.grow, hold: Q.hold,
               route: Q.route.slice(),
               head: beams.map(b => b.m.uniforms.uHead.value),
               done: beams.map(b => b.m.uniforms.uHead.value >= b.route - 1e-6 ? 1 : 0) };
    },
    draw(dt, clock){
      SH.uTime.value = clock;
      const T = clock % Q.cyc;
      phase = T;
      // 收尾段：整轮末 Q.rel 秒把光**抽回去**（不是整体淡出 ——
      // 淡出会让三条路由凭空消失，抽回去才读成「这一轮讲完了，重来」）。
      const rel = T > Q.grow + Q.hold
        ? Math.min(1, (T - Q.grow - Q.hold) / Q.rel) : 0;
      let k = 0;
      beams.forEach((b) => {
        const head = Math.max(0, Math.min(b.route, (T - b.t0) * Q.beam)) * (1 - rel);
        b.m.uniforms.uHead.value = head;
        // 前沿上的亮斑 + 两枚拖尾（只在真的在走的时候亮）
        const live = head > 1 && head < b.route - 1 ? 1 : 0;
        const P = b.g.attributes.position.array, AT = b.g.attributes.aT.array, n = AT.length;
        for(let j = 0; j < 3; j++){
          const d = Math.max(0, head - j * Q.feather * .5);
          let lo = 0; while(lo < n - 2 && AT[lo + 1] < d) lo++;
          const seg = (AT[lo + 1] - AT[lo]) || 1, u = (d - AT[lo]) / seg;
          hpos[k*3]   = P[lo*3]   + (P[lo*3+3] - P[lo*3])   * u;
          hpos[k*3+1] = P[lo*3+1] + (P[lo*3+4] - P[lo*3+1]) * u;
          hpos[k*3+2] = P[lo*3+2] + (P[lo*3+5] - P[lo*3+2]) * u;
          hA.a[k] = live * (1 - j * .34); k++;
        }
      });
      hg.attributes.position.needsUpdate = true; hg.attributes.aA.needsUpdate = true;
      // 楼层灯瀑：一列灯自上而下滚，每只塔错开一档（三只机房不是同一个节拍）
      let fk = 0;
      for(let i = 0; i < Q.tower.length; i++){
        const ph = clock / Q.fld + i * 0.31;
        for(let j = 0; j < Q.fln; j++){
          const u = ((ph - j / Q.fln) % 1 + 1) % 1;
          fA.a[fk] = 0.18 + 0.82 * Math.pow(1 - u, 3); fk++;
        }
      }
      fg.attributes.aA.needsUpdate = true;
      hotMat.uniforms.uGain.value = .4 + .4 * Math.sin(clock * TAU / Q.beat);
    },
    applyTheme(){
      faceMat.uniforms.uColor.value.copy(cssColor('--y-face'));
      faceMat.uniforms.uOpacity.value = cssNum('--y-face-op', .8);
      hotMat.uniforms.uColor.value.copy(cssColor('--y-hot'));
      hotMat.uniforms.uHot.value.copy(cssColor('--y-hot'));
      hotMat.uniforms.uOpacity.value = cssNum('--y-hot-op', 1);
      wallMat.uniforms.uColor.value.copy(cssColor('--y-wall'));
      wallMat.uniforms.uOpacity.value = cssNum('--y-wall-op', .26);
      beams.forEach(b => {
        b.m.uniforms.uColor.value.copy(cssColor('--y-beam'));
        b.m.uniforms.uHot.value.copy(cssColor('--y-head'));
        b.m.uniforms.uOpacity.value = cssNum('--y-beam-op', .86);
        b.m.uniforms.uGain.value = 1.1;
      });
      headMat.uniforms.uColor.value.copy(cssColor('--y-head'));
      headMat.uniforms.uHot.value.copy(cssColor('--y-head'));
      headMat.uniforms.uOpacity.value = cssNum('--y-head-op', 1);
      headMat.uniforms.uSize.value = cssNum('--y-head-size', 7.5);
      headMat.uniforms.uGain.value = 0;
      floorMat.uniforms.uColor.value.copy(cssColor('--y-floor'));
      floorMat.uniforms.uHot.value.copy(cssColor('--y-floor'));
      floorMat.uniforms.uOpacity.value = cssNum('--y-floor-op', .7);
      floorMat.uniforms.uSize.value = cssNum('--y-floor-size', 5.2);
      floorMat.uniforms.uGain.value = 0;
      [faceMat, wallMat, floorMat, headMat].forEach(m => {
        m.uniforms.uHot.value.copy(m.uniforms.uColor.value); m.uniforms.uGain.value = 0; });
      [faceMat, hotMat, wallMat, floorMat, headMat].concat(beams.map(b => b.m))
        .forEach(m => { m.uniforms.uBack.value = .62; setBlend(m, cssNum('--y-add', 0)); });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ㉒ 加法层三页（P5 / P15 / P16 · 三轮「静态页升维」）
   ───────────────────────────────────────────────────────────────────────────
   与另外 17 枚场景的**根本差别**：那 17 枚在替换页上的一张 SVG 图（poster 是它的
   降级层）；这三页页上没有图，3D 是加在既有版面之外的一层**氛围场**，
   降级层就是整页本身。所以它们：
     · 一件 DOM 都不动、一枚 poster 都不挂；
     · 几何一律走**投影锁**（每一点的投影落点 = 它的页坐标）⇒ 深度只影响
       雾与粒径，绝不会把形挪到字上去；
     · 共用下面三只小件把「不压字」变成机器判据：`unlock` 把这一帧真的传上
       GPU 的顶点投影回舞台像素、`inkClr` 量它到页上字形墨迹盒的距离、
       `geoClr` 逐顶点取最小值 —— 与构建期的解析断言是**两条独立算路**。
   ═══════════════════════════════════════════════════════════════════════════ */
function unlock(w, h, D, rect){
  const cx = w/2, cy = h/2;
  return function(X, Y, z){
    const k = (D - z)/D;                       // mkLock 的逆
    return [cx + (X-cx)/k + rect[0], cy + (-Y-cy)/k + rect[1]];
  };
}
function inkClr(p, ink){
  let m = 1e9;
  for(let j = 0; j < ink.length; j++){
    const b = ink[j];
    const dx = Math.max(b[0]-p[0], 0, p[0]-(b[0]+b[2]));
    const dy = Math.max(b[1]-p[1], 0, p[1]-(b[1]+b[3]));
    const d = Math.hypot(dx, dy);
    if(d < m) m = d;
  }
  return m;
}
function geoClr(geo, U, ink, pad){
  const a = geo.attributes.position.array;
  let m = 1e9;
  for(let i = 0; i < a.length; i += 3)
    m = Math.min(m, inkClr(U(a[i], a[i+1], a[i+2]), ink) - (pad || 0));
  return m;
}
/* 一整枚场景的净空：items = [[geometry, pad], …]；pad 扣掉带宽 / 点半径
   （那是几何之外的墨）。⑥ 互动星系与 info 的五枚场景都走这一只。 */
function clrMin(U, ink, items){
  let m = 1e9;
  for(let i = 0; i < items.length; i++)
    m = Math.min(m, geoClr(items[i][0], U, ink, items[i][1] || 0));
  return m;
}
/* 折线复活（与 Python 侧 _pk 同格式："x,y;x,y;…"）—— 加法层四页的几何
   **构建期算一遍，运行时不再算第二遍**，两边不可能是两套解。 */
function unpk(s, z){
  return s.split(';').map(t => { const q = t.split(','); return [+q[0], +q[1], z || 0]; });
}
/* "x,y,z;…" → 世界折线（构建期算好，运行时不重算） */
function unpk3(s){
  return s.split(';').map(t => { const q = t.split(','); return [+q[0], +q[1], +q[2]]; });
}
/* R2 低差异序列（塑性数为底 · Roberts 2018）：铺点均匀且不与螺旋共振 */
const PHI2 = 1.3247179572447460;
function r2(i){ return [(0.5 + i/PHI2) % 1, (0.5 + i/(PHI2*PHI2)) % 1]; }

/* ════════════════════════════════════════════════════════════════════════════
   ⑥ 互动星系（P22 末页 ·「展望」）
   ────────────────────────────────────────────────────────────────────────────
   ⚠ 2026-09-03：这里原来是 `makeQuiet`（㉒-① 余韵星野 · 末页的一层涟漪场）。
     Colin 这一轮的意图是**展望**（使命 / 愿景 / 三种互动）—— 末页不再是「余韵」，
     整枚场景退役（QT_VS / QT_FS / makeQuiet / --e-* / ㉒c 三条克制闸一并拆掉）。
   本枚场景发源于 convoai-info P8，现在旗舰是它的**单一真相**：下面这一段
   JS 只读 `K.gx`，所以它**天然尺度无关** —— lab P22（盘心 (380,400) · s=0.75）
   与 info P8（盘心 (860,278) · s=1.0）跑的是同一份代码，差别全在 K 表里。
   三稿与 P17 五脑区大脑**同一语系**：同一套 K.b 式的点材质（PX_PT / camPx / 深度雾）、
   同一套 tmax/dref 密度剖面、12,000 点、一枚占满舞台的发光体，外面挂标注引线。
     ① 核 · 人与人 · 已经发生：实心体积球核 r≈100，向日葵铺点（零随机源），
        厚度剖面 T(d)=tmax·sin(π/2·(d/dref)^0.62) —— 与 makeBrain 逐字同式；
        热度按到球心的距离给 ⇒ **中心最亮**，一切从这里长出来。
     ② 内环 · 人与智能体 · 正在发生：环带 r200–290 厚 ±22，人（accent）与
        智能体（--gx-in-b 蓝）**按确定性序交错**，各半。
     ③ 外环 · 智能体与智能体 · 即将发生：环带 r360–470 厚 ±30，蓝 / 紫各半。
        **网在长**：每点两枚相位 —— aG 是角度门槛（生长锋按角度扫过去，20s 一周期
        由稀到密再回稀，dens 是余弦 ⇒ C¹ 连续、回卷处零跳变），aQ 是**生灭窗相位**
        （写法照 P2 剧场的 uLife：0.4s 内归零再回卷，接头永远藏在最暗处；
        aQ 走塑性数低差异序列 ⇒ 任一帧只有 2% 的点在灭窗里，整幅亮度不跳）。
   环上 24 条智能体间弧（写法照 P21 地球弧：细弧 + 沿弧跑的一枚亮斑），
   随 aG 那道生长锋一起点亮；14 条核↔内环互动流（一来一回）+ 6 条内环→外环
   径向流，全部 mkStream · A 档 110px/s · λ232 —— 与全家族同一种介质。
   整体绕盘轴 1 圈 / 90s 慢转，另叠 P17 同款 ±6° / 17s 轻摇；三件几何（点云 / 弧 / 流）
   **全部跟着转**，所以它是一个在转的体，不是一张贴着动效的图。
   ⚠ 投影锁做在最后一步（xy 按该点自己的 z 预缩放）⇒ 三环在屏上是三枚正椭圆、
     净空可以纯解析地算；深度只管**雾与点径**——体积感全在那儿（与 P17 同一条路）。
   ⚠ canvas 零文字：三环 / 弧 / 流全是形，字全部在 DOM 里（⑲a 正面断言）。
   ⚠ 净空：整体在转在摇 ⇒ 几何逐帧在变，构建期交的是整族的**扫掠包络**（下界），
     qa 的 ⑳galaxy 按不等式对表（与 P17 大脑同一条路）。
   ════════════════════════════════════════════════════════════════════════════ */
const GX_VS = PX_HEAD + [
  'attribute float aS;',
  'uniform float uSz1;',
  'void main(){ vA=aA; vH=aH;',
  '  vec4 mv=pxCore(position, uSize*(1.0-uSz1+uSz1*aS));',
  '  gl_Position=projectionMatrix*mv; }'].join('\n');
/* 外环专用：生灭窗（每点各自 0.4s 归零再回卷）× 生长锋（角度门槛 vs 全环密度） */
const GXO_VS = PX_HEAD + [
  'attribute float aS; attribute float aQ; attribute float aG;',
  'uniform float uSz1,uC,uW0,uWb,uDens,uGs,uFloor;',
  'void main(){',
  '  float u = fract(uC - aQ);',
  '  float life = smoothstep(0.0,uWb,u)*(1.0-smoothstep(1.0-uW0,1.0,u));',
  '  float gate = smoothstep(aG-uGs, aG+uGs, uDens);',
  '  vA = aA*life*(uFloor + (1.0-uFloor)*gate);',
  '  vH = gate;',
  '  vec4 mv=pxCore(position, uSize*(1.0-uSz1+uSz1*aS));',
  '  gl_Position=projectionMatrix*mv; }'].join('\n');

function makeGalaxy(ctx){
  const Q = K.gx, w = ctx.rect[2], h = ctx.rect[3], D = Q.D;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, Q.half);
  const U = unlock(w, h, D, ctx.rect);
  const TAU2 = 6.2831853, RAD = Math.PI/180;
  const hx = w/2, hy = h/2, CX = Q.c[0], CY = Q.c[1];
  const cT = Math.cos(Q.tilt*RAD), sT = Math.sin(Q.tilt*RAD);
  const GA = Math.PI*(3-Math.sqrt(5));      // 黄金角（与构建期 _GX_GA 逐字同式）
  const PL2 = 0.7548776662;                 // 塑性数的倒数（生灭窗相位）
  let csp = 1, ssp = 0, csw = 1, ssw = 0, introE = 0, densE = 0;

  /* 盘面局部 (cosφ, sinφ, r, w) → 世界：自转 → 倾角 → 轻摇 → 投影锁。
     cos/sin(φ) 预存 ⇒ 每帧零三角函数，12,000 点只有加乘（Python 侧 _gx_page 同式）。*/
  const _o = [0,0,0];
  function place(cp, sp, r, wo, out){
    const c2 = cp*csp - sp*ssp, s2 = sp*csp + cp*ssp;
    const u1 = r*c2, v1 = r*s2;
    const y1 = v1*cT - wo*sT, z1 = v1*sT + wo*cT;
    const X2 = u1*csw + z1*ssw, Z2 = -u1*ssw + z1*csw;
    const k = (D - Z2)/D;
    out[0] = hx + (CX + X2 - hx)*k;
    out[1] = -(hy + (CY + y1 - hy)*k);
    out[2] = Z2;
    return out;
  }

  /* ── 三环 12,000 点：静态参数一次算好，position 每帧重算（GPU 只吃坐标）── */
  function coreT(rho){
    const d = Math.max(0, Q.coreR - rho);
    return Q.coreR*Math.sin(Math.PI/2*Math.pow(d/Q.dref, 0.62));
  }
  function genCore(i, o){
    const rho = Q.coreR*Math.pow((i+0.5)/Q.n0, 0.56), phi = i*GA;
    const T = coreT(rho), surf = Math.pow(h1(i,571.3), 0.40);
    const wv = (h1(i,853.9) < 0.5 ? -1 : 1)*T*surf;
    const r3 = Math.hypot(rho, wv)/Q.coreR;
    o[0]=rho; o[1]=phi; o[2]=wv;
    o[3]=(0.26+0.74*surf)*(0.24+0.76*T/Q.coreR);
    o[4]=Math.pow(Math.max(0,1-r3), 1.1); o[5]=surf; o[6]=0; o[7]=0;
  }
  function bandGen(r0, r1, tk, s0){
    return function(i, o){
      const phi = i*GA;
      const fr = (h1(i,137.9+s0) + h1(i,263.1+s0) + h1(i,389.5+s0))/3;
      const wv = tk*(h1(i,331.7+s0) + h1(i,457.3+s0) - 1);
      const edge = 1 - Math.abs(wv)/tk;
      o[0]=r0+(r1-r0)*fr; o[1]=phi; o[2]=wv; o[3]=0.46+0.54*edge;
      o[4]=0; o[5]=0.55+0.45*edge; o[6]=(i*PL2)%1; o[7]=(phi/TAU2)%1;
    };
  }
  const LAY = [];
  function layer(n, gen, stride, par, mat){
    const cs = new Float32Array(n), sn = new Float32Array(n);
    const rr = new Float32Array(n), wo = new Float32Array(n);
    const aA = new Float32Array(n), aH = new Float32Array(n), aS = new Float32Array(n);
    const aQ = new Float32Array(n), aG = new Float32Array(n);
    const pos = new Float32Array(n*3), o = [0,0,0,0,0,0,0,0];
    for(let j = 0; j < n; j++){
      gen(j*stride + par, o);
      cs[j]=Math.cos(o[1]); sn[j]=Math.sin(o[1]); rr[j]=o[0]; wo[j]=o[2];
      aA[j]=o[3]; aH[j]=o[4]; aS[j]=o[5]; aQ[j]=o[6]; aG[j]=o[7];
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos,3));
    g.setAttribute('aA', new THREE.BufferAttribute(aA,1));
    g.setAttribute('aH', new THREE.BufferAttribute(aH,1));
    g.setAttribute('aS', new THREE.BufferAttribute(aS,1));
    g.setAttribute('aQ', new THREE.BufferAttribute(aQ,1));
    g.setAttribute('aG', new THREE.BufferAttribute(aG,1));
    const p = new THREE.Points(g, mat); p.frustumCulled = false; scene.add(p);
    const L = { g, pos, cs, sn, rr, wo, n };
    LAY.push(L); return L;
  }
  const coreMat = mkMat(SH, GX_VS, PX_PT_FS, { uSz1:{value:.55} });
  const inAMat  = mkMat(SH, GX_VS, PX_PT_FS, { uSz1:{value:.35} });
  const inBMat  = mkMat(SH, GX_VS, PX_PT_FS, { uSz1:{value:.35} });
  const outU = () => ({ uSz1:{value:.35}, uC:{value:0}, uW0:{value:Q.w0},
                        uWb:{value:Q.wb}, uDens:{value:0}, uGs:{value:Q.gs},
                        uFloor:{value:Q.floor} });
  const outAMat = mkMat(SH, GXO_VS, PX_PT_FS, outU());
  const outBMat = mkMat(SH, GXO_VS, PX_PT_FS, outU());
  [coreMat, inAMat, inBMat, outAMat, outBMat].forEach(m => { m.uniforms.uSoft.value = .10; });
  layer(Q.n0, genCore, 1, 0, coreMat);
  const genIn = bandGen(Q.r[1], Q.r[2], Q.t[0], 0.0);
  const genOut = bandGen(Q.r[3], Q.r[4], Q.t[1], 7.0);
  layer(Q.n1>>1, genIn, 2, 0, inAMat);       // 人（accent）
  layer(Q.n1>>1, genIn, 2, 1, inBMat);       // 智能体（蓝）—— 按确定性序交错
  layer(Q.n2>>1, genOut, 2, 0, outAMat);
  layer(Q.n2>>1, genOut, 2, 1, outBMat);

  /* ── 三枚外缘轮廓环（P5 的「给轮廓一根真线」）· 跟着盘一起摇 ──
     没有这三根线，三环在屏上只是三层疏密不同的尘 —— 一稿实拍锤过。 */
  const rimMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const NR = Q.rim.length, RSEG = Q.rimseg;
  const rimG = new THREE.BufferGeometry();
  const rimP = new Float32Array(NR*RSEG*2*3);
  rimG.setAttribute('position', new THREE.BufferAttribute(rimP,3));
  fillAH(rimG, 1, 0);
  scene.add(Object.assign(new THREE.LineSegments(rimG, rimMat), { frustumCulled:false }));
  function placeRims(){
    let n3 = 0;
    for(let k = 0; k < NR; k++){
      let px = 0, py = 0, pz = 0;
      for(let i = 0; i <= RSEG; i++){
        const th = i/RSEG*TAU2;
        place(Math.cos(th), Math.sin(th), Q.rim[k], 0, _o);
        if(i > 0){
          rimP[n3*3]=px; rimP[n3*3+1]=py; rimP[n3*3+2]=pz; n3++;
          rimP[n3*3]=_o[0]; rimP[n3*3+1]=_o[1]; rimP[n3*3+2]=_o[2]; n3++;
        }
        px=_o[0]; py=_o[1]; pz=_o[2];
      }
    }
    rimG.attributes.position.needsUpdate = true;
  }

  /* ── 24 条智能体间弧（细弧 + 沿弧跑的亮斑）· 每帧跟着盘一起转 ── */
  const NA = Q.arc.length, ASEG = Q.aseg;
  const arcMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const arcG = new THREE.BufferGeometry();
  const arcP = new Float32Array(NA*ASEG*2*3);
  arcG.setAttribute('position', new THREE.BufferAttribute(arcP,3));
  const arcA = fillAH(arcG, 1, 0);
  scene.add(Object.assign(new THREE.LineSegments(arcG, arcMat), { frustumCulled:false }));
  const headMat = mkMat(SH, PX_PT_VS, PX_PT_FS); headMat.uniforms.uSoft.value = .04;
  const headG = new THREE.BufferGeometry();
  const headP = new Float32Array(NA*3);
  headG.setAttribute('position', new THREE.BufferAttribute(headP,3));
  const headA = fillAH(headG, 1, 1);
  scene.add(Object.assign(new THREE.Points(headG, headMat), { frustumCulled:false }));
  const arcPt = (a, i, out) => {                 // 弧上第 i 个取样点（局部 → 世界）
    const t = i/ASEG, s = Math.sin(Math.PI*t);
    const phi = a[0] + (a[1]-a[0])*t;
    return place(Math.cos(phi), Math.sin(phi), Q.outr - a[4]*s, a[2]*s*(0.15+0.85*introE), out);
  };
  const gateAt = (g) => {                        // 生长锋在角度 g 处的开合（与外环点同式）
    const x = (g - Q.gs), y = (g + Q.gs);
    const t = Math.max(0, Math.min(1, (densE - x)/((y - x) || 1e-6)));
    return t*t*(3 - 2*t);
  };

  /* ── 20 条流（14 核↔内环 + 6 内环→外环）· 中心线跟着盘转 ⇒ 每帧重织带面 ── */
  const SLOC = Q.sp.map(s => s.split(';').map(t => {
    const q = t.split(','); const phi = +q[1];
    return [+q[0], phi, +q[2], Math.cos(phi), Math.sin(phi)];
  }));
  const flows = Q.s.map((sp, i) =>
    mkStream(SH, unpk3(sp), { w: Q.sw[i], spd: Q.spdv[i], lam: AS.lam }).add(scene));
  const WP = new Float32Array(Q.spts*3);
  function updStreams(){
    for(let i = 0; i < flows.length; i++){
      const lp = SLOC[i], n = lp.length, f = flows[i];
      const pos = f.geo.attributes.position.array, nrm = f.geo.attributes.aN.array;
      for(let j = 0; j < n; j++){
        const p = lp[j];
        place(p[3], p[4], p[0], p[2]*(0.15+0.85*introE), _o);
        WP[j*3]=_o[0]; WP[j*3+1]=_o[1]; WP[j*3+2]=_o[2];
      }
      for(let j = 0; j < n; j++){
        const a = Math.max(0,j-1)*3, b = Math.min(n-1,j+1)*3;
        let tx = WP[b]-WP[a], ty = WP[b+1]-WP[a+1];
        const tl = Math.hypot(tx, ty, WP[b+2]-WP[a+2]) || 1; tx/=tl; ty/=tl;
        let nx = ty, ny = -tx;
        const nl = Math.hypot(nx, ny) || 1; nx/=nl; ny/=nl;
        for(let k2 = 0; k2 < 2; k2++){
          const jj = (j*2+k2)*3;
          pos[jj]=WP[j*3]; pos[jj+1]=WP[j*3+1]; pos[jj+2]=WP[j*3+2];
          nrm[jj]=nx; nrm[jj+1]=ny; nrm[jj+2]=0;
        }
      }
      f.geo.attributes.position.needsUpdate = true;
      f.geo.attributes.aN.needsUpdate = true;
    }
  }

  function placeCloud(){
    const ws = 0.15 + 0.85*introE;               // 入场：体积从盘面里长出来
    for(let L = 0; L < LAY.length; L++){
      const q = LAY[L], p = q.pos;
      for(let i = 0; i < q.n; i++){
        place(q.cs[i], q.sn[i], q.rr[i], q.wo[i]*ws, _o);
        p[i*3]=_o[0]; p[i*3+1]=_o[1]; p[i*3+2]=_o[2];
      }
      q.g.attributes.position.needsUpdate = true;
    }
  }
  function placeArcs(clock){
    let n3 = 0;
    for(let a = 0; a < NA; a++){
      const A = Q.arc[a];
      const lit = Q.arcfloor + (1 - Q.arcfloor)*gateAt(A[3]);
      let px = 0, py = 0, pz = 0;
      for(let i = 0; i <= ASEG; i++){
        arcPt(A, i, _o);
        if(i > 0){
          arcP[n3*3]=px; arcP[n3*3+1]=py; arcP[n3*3+2]=pz; arcA.a[n3]=lit; n3++;
          arcP[n3*3]=_o[0]; arcP[n3*3+1]=_o[1]; arcP[n3*3+2]=_o[2]; arcA.a[n3]=lit; n3++;
        }
        px=_o[0]; py=_o[1]; pz=_o[2];
      }
      // 亮斑：沿弧跑（周期 arcdur · 起相位 = 该弧的角度相位 ⇒ 零随机源）
      let u = (clock/Q.arcdur + A[3]) % 1; if(u < 0) u += 1;
      arcPt(A, Math.round(u*ASEG), _o);
      headP[a*3]=_o[0]; headP[a*3+1]=_o[1]; headP[a*3+2]=_o[2];
      headA.a[a] = lit*Math.min(1, 4*u)*Math.min(1, 4*(1-u));
    }
    arcG.attributes.position.needsUpdate = true; arcG.attributes.aA.needsUpdate = true;
    headG.attributes.position.needsUpdate = true; headG.attributes.aA.needsUpdate = true;
  }

  function step(clock){
    const sp = TAU2*clock/Q.spinP;
    csp = Math.cos(sp); ssp = Math.sin(sp);
    const sy = Q.sway*RAD*Math.sin(TAU2*clock/Q.swayP);
    csw = Math.cos(sy); ssw = Math.sin(sy);
    const c = clock/Q.cyc, cf = c - Math.floor(c);
    densE = 0.5 - 0.5*Math.cos(TAU2*c);
    [outAMat, outBMat].forEach(m => {
      m.uniforms.uC.value = cf; m.uniforms.uDens.value = densE; });
    placeCloud(); placeRims(); placeArcs(clock); updStreams();
  }
  step(0);
  return {
    scene, camera, intro: 1.5, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; introE = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      step(clock);
      for(let i = 0; i < flows.length; i++) flows[i].draw(clock);
    },
    /* 净空：把这一帧真的传上 GPU 的顶点（点云 / 弧 / 亮斑 / 20 条带）投影回舞台像素，
       逐顶点量到墨迹名册。点径 / 带宽的 pad 与构建期是**同一个数**（Q.ptpad / Q.wpx）。*/
    state(){
      const items = LAY.map(L => [L.g, Q.ptpad]);
      for(let i = 0; i < flows.length; i++) items.push([flows[i].geo, Q.wpx[i]]);
      items.push([arcG, 0], [rimG, 0], [headG, Q.ptpad]);
      return { clr: clrMin(U, Q.ink, items) };
    },
    applyTheme(){
      const pair = (m, c, hot, op, gain, sz) => {
        m.uniforms.uColor.value.copy(cssColor(c));
        m.uniforms.uHot.value.copy(cssColor(hot || c));
        m.uniforms.uOpacity.value = op; m.uniforms.uGain.value = gain || 0;
        if(sz !== undefined) m.uniforms.uSize.value = sz; };
      const cz = cssNum('--gx-core-size', 3.1), iz = cssNum('--gx-in-size', 2.9);
      const oz = cssNum('--gx-out-size', 2.7);
      pair(coreMat, '--gx-core',  '--gx-core-hot', cssNum('--gx-core-op', .90),
           cssNum('--gx-core-gain', .55), cz);
      pair(inAMat,  '--gx-in-a',  '--gx-core',  cssNum('--gx-in-a-op', .80), .30, iz);
      pair(inBMat,  '--gx-in-b',  '--gx-in-b',  cssNum('--gx-in-b-op', .84), 0,   iz);
      pair(outAMat, '--gx-out-a', '--gx-spark', cssNum('--gx-out-a-op', .76), .45, oz);
      pair(outBMat, '--gx-out-b', '--gx-out-b', cssNum('--gx-out-b-op', .76), .30, oz);
      pair(arcMat,  '--gx-arc',   '--gx-spark', cssNum('--gx-arc-op', .62), .70);
      pair(rimMat,  '--gx-rim',   '--gx-core',  cssNum('--gx-rim-op', .40), .20);
      pair(headMat, '--gx-spark', '--gx-spark', cssNum('--gx-spark-op', .92), .60,
           cssNum('--gx-spark-size', 5));
      const fc = cssColor('--gx-flow'), fr = cssColor('--gx-rms');
      const rc = cssColor('--gx-rad'),  rr = cssColor('--gx-rad-rms');
      const fo = cssNum('--gx-flow-op', .74), fro = cssNum('--gx-rms-op', .82);
      const ro = cssNum('--gx-rad-op', .66),  rro = cssNum('--gx-rad-rms-op', .72);
      const back = cssNum('--gx-back', .34), add = cssNum('--gx-add', 0);
      for(let i = 0; i < flows.length; i++){
        const rad = Q.sk[i] === 1;
        flows[i].theme(rad ? rc : fc, rad ? rr : fr, rad ? ro : fo, rad ? rro : fro, back);
        setBlend(flows[i].mat, add);
      }
      [coreMat, inAMat, inBMat, outAMat, outBMat, arcMat, rimMat, headMat].forEach(m => {
        m.uniforms.uBack.value = back; setBlend(m, add); });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ㉒-② 章头底场（P5 · 三件极致）
   ───────────────────────────────────────────────────────────────────────────
   三张数字卡是主角，底场是伴奏（墨量 ≤ 卡片的 25%，闸上有）。三条极细的
   语义微线在卡下方跑，各自是那件事的**最小表意**，并且都朝下收尾 ——
   与卡右上角那三枚章内指针（↓P6 / ↓P7–8 / ↓P9）同向：
     650ms 延时 = 接力（介质在跑 + 一道注光走完即到）
     340ms 打断 = 让位（智能体轨跑到一半落 ghost，用户轨接上并带走收尾）
     95%  屏蔽 = 薄盾（三路杂线撞盾消解，目标人声从缺口穿过去）
   幅度剖面**全部走 gain 回调，零分支**（lab-kit ⑨ 的 aG 双通道）。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeThree(ctx){
  const Q = K.x, w = ctx.rect[2], h = ctx.rect[3], D = Q.D;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, Q.half), L = mkLock(w, h, D), U = unlock(w, h, D, ctx.rect);
  const R = ctx.rect;
  const loc = (p, z) => L(p[0]-R[0], p[1]-R[1], z);      // 页坐标 → 本景局部 → 投影锁
  /* ── ⑤ 三条支流 + 一条集流带 ────────────────────────────────────────────
     支流从三张卡底垂下（稍近一档 ⇒ 「垂下来」是往前垂），一记肘拐进集流带；
     集流带向右流，半宽在**每一处汇入点涨一档**（Q.cw[0] → Q.cw[1]）——
     「三件事最后合回一张图」不是画出来的比喻，是带子自己变粗。 */
  const NF = Q.s.length, COL = NF - 1;
  const cwAt = (u) => {                      // 集流带在弧长 u 处的半宽（零分支）
    let g = 0;
    for(let j = 0; j < Q.join.length; j++) g += sstep(Q.join[j]-Q.jw, Q.join[j]+Q.jw, u);
    return Q.cw[0] + (Q.cw[1]-Q.cw[0])*(g/Q.join.length);
  };
  const flows = Q.s.map((s, i) => {
    const z = Q.sz[i], pts = unpk(s).map(p => loc(p, z));
    const hw = i === COL ? ((t, u) => cwAt(u)) : Q.w;
    return mkStream(SH, pts, { w:hw, spd:Q.spd[i], lam:Q.lam }).add(scene);
  });
  // 支流：从卡底「起流」—— 头 18px 由 ghost 涨起来，读作「从卡里淌下来」
  for(let i = 0; i < COL; i++) flows[i].gain((u) => sstep(0, 18, u));
  // ── 收口箭头：`ah_r` 的 3D 版（P5 是加法层页，DOM 一个件都不新增）──
  const arrMat = mkMat(SH, PX_LN_VS, PX_LN_FS); arrMat.side = THREE.DoubleSide;
  { const A0 = Q.arr, ax = A0[0], ay = A0[1], al = A0[2];
    const g = new THREE.BufferGeometry();
    const t0 = loc([ax, ay], 0), t1 = loc([ax-al, ay-al*0.5], 0), t2 = loc([ax-al, ay+al*0.5], 0);
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(
      [t0[0],t0[1],t0[2], t1[0],t1[1],t1[2], t2[0],t2[1],t2[2]]), 3));
    fillAH(g, 1, 0);
    scene.add(Object.assign(new THREE.Mesh(g, arrMat), { frustumCulled:false })); }
  // ── 底场微粒：三条微线共同的那层「地」（R2 铺点 · 确定性）──
  const HN = +Q.hazen, hz = Q.haze;
  const hg = new THREE.BufferGeometry(), hp = new Float32Array(HN*3);
  for(let i = 0; i < HN; i++){
    const uv = r2(i), z = -90 + 130*h1(i, 41.7);
    const q = loc([hz[0] + uv[0]*hz[2], hz[1] + uv[1]*hz[3]], z);
    hp[i*3] = q[0]; hp[i*3+1] = q[1]; hp[i*3+2] = q[2];
  }
  hg.setAttribute('position', new THREE.BufferAttribute(hp,3));
  const hA = fillAH(hg, 1, 0);
  for(let i = 0; i < HN; i++) hA.a[i] = 0.35 + 0.65*h1(i, 63.1);
  hg.attributes.aA.needsUpdate = true;
  const hMat = mkMat(SH, PX_PT_VS, PX_PT_FS); hMat.uniforms.uSoft.value = .05;
  scene.add(Object.assign(new THREE.Points(hg, hMat), { frustumCulled:false }));
  return {
    scene, camera, intro: 1.15, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      flows.forEach(f => f.draw(clock));
    },
    applyTheme(){
      const pk = cssColor('--x-flow'), rms = cssColor('--x-rms');
      const op = cssNum('--x-flow-op', .40), rop = cssNum('--x-rms-op', .55);
      flows.forEach((f, i) => {
        // 集流带比支流亮一档：它是三件事合回来的那一条
        f.theme(pk, rms, i === COL ? op*1.22 : op, rop, .55);
        setBlend(f.mat, cssNum('--x-add', 0));
      });
      arrMat.uniforms.uColor.value.copy(cssColor('--x-beam'));
      arrMat.uniforms.uHot.value.copy(cssColor('--x-beam'));
      arrMat.uniforms.uOpacity.value = cssNum('--x-beam-op', .88);
      arrMat.uniforms.uGain.value = 0;
      hMat.uniforms.uColor.value.copy(cssColor('--x-haze'));
      hMat.uniforms.uHot.value.copy(cssColor('--x-haze'));
      hMat.uniforms.uOpacity.value = cssNum('--x-haze-op', .22);
      hMat.uniforms.uSize.value = cssNum('--x-haze-size', 2.0);
      hMat.uniforms.uGain.value = 0;
      [arrMat, hMat].forEach(m => { m.uniforms.uBack.value = .55;
        setBlend(m, cssNum('--x-add', 0)); });
    },
    state(){
      let clr = geoClr(hg, U, Q.ink, 1.4);
      flows.forEach((f, i) => {
        clr = Math.min(clr, geoClr(f.geo, U, Q.ink, i === COL ? Q.cw[1] : Q.w)); });
      return { clr, flows: flows.length, haze: HN, join: Q.join.slice(),
               cw: Q.cw.slice(), spd: flows.map(f => f.spd), lam:Q.lam };
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ㉒-③ 中心辐射（P15 · 六场景）
   ───────────────────────────────────────────────────────────────────────────
   「一套引擎，支撑多类场景」= **一个核 + 六条支线 + 六簇**。版面给这张图留的路
   正好是六张卡之间那条无字带（row1 的字止于 y478、row2 的字起于 y631）：核坐在
   带心，六条支线**直线**发散到六簇 —— 真辐射。六簇各落在自家卡的下缘留白里，
   卡底是 72% 不透明 ⇒ 簇在卡**背后**透出三成：「中心最亮、六簇微光」这层主次
   是版面本身给的。深度上核在最前、六簇各自退到不同的 z ⇒ 发散是真的在深度里。
   六处身份微动，一处一巧思，全部关在自家 140×34 的簇框里（净空闸逐点量）：
     0 外呼=拨号脉冲串 1 智能硬件=设备点阵亮灭 2 虚拟陪伴=柔和呼吸
     3 口语陪练=一来一回 4 智能客服=排队消解 5 更多场景=景深处待命的微光星丛
   ═══════════════════════════════════════════════════════════════════════════ */
function makeHub(ctx){
  const Q = K.hb, w = ctx.rect[2], h = ctx.rect[3], D = Q.D;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, Q.half), L = mkLock(w, h, D), U = unlock(w, h, D, ctx.rect);
  const R = ctx.rect, CX = Q.core[0], CY = Q.core[1], CR = Q.core[2];
  const loc = (x, y, z) => L(x-R[0], y-R[1], z);
  // ── 六条支线：核（z=+70）→ 簇（各自的深度）——「发散」在深度里是真的 ──
  /* ⑦ 支线：半宽从核端 Q.w01[0] 涨到卡端 Q.w01[1] —— 「从核**流向**卡」这件事
     由带子自己的粗细说，不靠箭头。 */
  const flows = Q.s.map((s, i) => {
    const raw = unpk(s), zc = Q.cl[i][2];
    const pts = raw.map((p, j) => loc(p[0], p[1], Q.cz + (zc-Q.cz)*(j/(raw.length-1))));
    return mkStream(SH, pts, { w:(t) => Q.w01[0] + (Q.w01[1]-Q.w01[0])*t,
                               spd:Q.spd[i], lam:Q.lam }).add(scene);
  });
  /* ── ⑦ 核 = 与 P13 同血统的**迷你转子** ────────────────────────────────
     三枚异面椭圆环（_K_ORB 等比缩小到竖半轴 22px）+ 一条在环之间迁徙的粒子带。
     lockZ：xy 按**核所在的那一层** Q.cz 预缩放、z 用点自己的 —— 于是 z=cz 的点
     投影落在页坐标上一格不差，而环翻滚出平面的那一档产生真视差（与 P13 的 LZ
     同一手法）。旧核是一团点 + 两枚同心细环：屏上只是一小坨白光，读不出引擎。 */
  const OB = Q.orb, CN = +Q.orbN, RAD = Math.PI/180;
  const lockZ = (x, y, z) => { const k = (D - Q.cz)/D, hx = w/2, hy = h/2;
    return [hx + (x-R[0]-hx)*k, -(hy + (y-R[1]-hy)*k), z]; };
  /* 三稿：环由 (rx, r2, tilt°) 定义 —— 环平面绕 x 轴倾 tilt，于是
       y = r2·sinθ·cos(tilt)（投影里的竖半轴）、z = r2·sinθ·sin(tilt)（离面）。
     倾角显式给、且各自只在 ±Q.orbAmp 里摆动**不过零** ⇒ 三枚环任何一帧都不共面。 */
  const orbPt = (rx, r2, tl, th, rad) => {
    const ct = Math.cos(tl*RAD), st = Math.sin(tl*RAD), sn = r2*rad*Math.sin(th);
    return lockZ(CX + rx*rad*Math.cos(th), CY + sn*ct, Q.cz + sn*st);
  };
  function orbAt(t){                        // 粒子带：内圈 → 中圈 → 外圈的分段线性插值
    const a2 = t <= 0.5 ? OB[2] : OB[1], b2 = t <= 0.5 ? OB[1] : OB[0];
    const u2 = t <= 0.5 ? t*2 : (t-0.5)*2;
    return [a2[0]+(b2[0]-a2[0])*u2, a2[1]+(b2[1]-a2[1])*u2, a2[2]+(b2[2]-a2[2])*u2];
  }
  const tiltOf = (k, clock) => OB[k][2] + Q.orbAmp*Math.sin(TAU*clock/Q.orbRoll[k]);
  const cg = new THREE.BufferGeometry(), cp = new Float32Array(CN*3);
  cg.setAttribute('position', new THREE.BufferAttribute(cp,3));
  const cA = fillAH(cg, 1, 0);
  const cTh = new Float32Array(CN), cNu = new Float32Array(CN), cSp = new Float32Array(CN);
  { const ga = Math.PI*(3-Math.sqrt(5));
    for(let i = 0; i < CN; i++){ cTh[i] = i*ga; cNu[i] = i/CN*3;
      cSp[i] = (0.30 + 0.22*((i*7919 % 97)/96)) * (i % 2 ? 1 : -1); } }
  const coreMat = mkMat(SH, PX_PT_VS, PX_PT_FS); coreMat.uniforms.uSoft.value = .03;
  scene.add(Object.assign(new THREE.Points(cg, coreMat), { frustumCulled:false }));
  /* 三稿②：**可见的核** —— r≈7 的发光点坐在转子心。亮度不是常数，是六条支线
     在核端的**包络之和**（与 river 的 meet 同一写法：aH 进 uHot / uGain）⇒
     六路一起涨的那一瞬核最亮，读作「引擎在出力」。带亮度地板 ⇒ 常亮。 */
  const coreDot = new THREE.BufferGeometry();
  { const q = lockZ(CX, CY, Q.cz);
    coreDot.setAttribute('position', new THREE.BufferAttribute(
      new Float32Array([q[0], q[1], q[2]]), 3)); }
  const dotA = fillAH(coreDot, 1, 0);
  const dotMat = mkMat(SH, PX_PT_VS, PX_PT_FS); dotMat.uniforms.uSoft.value = .16;
  scene.add(Object.assign(new THREE.Points(coreDot, dotMat), { frustumCulled:false }));
  // 六条支线在核端的解析包络（lab-kit ⑨ 的 envAt · 同一批 K.as 常量）
  const ASK = K.as, KL = TAU/ASK.lam;
  const envAt = (u) => 0.5 + 0.5*(ASK.a[0]*Math.sin(KL*ASK.f[0]*u + ASK.ph[0])
                                + ASK.a[1]*Math.sin(KL*ASK.f[1]*u + ASK.ph[1])
                                + ASK.a[2]*Math.sin(KL*ASK.f[2]*u + ASK.ph[2])
                                + ASK.a[3]*Math.sin(KL*ASK.f[3]*u + ASK.ph[3]));
  const RSEG = 72, ringGeo = new THREE.BufferGeometry();
  const rpos = new Float32Array(3*RSEG*2*3);
  ringGeo.setAttribute('position', new THREE.BufferAttribute(rpos,3));
  const rA = fillAH(ringGeo, 1, 0);
  const ringMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  scene.add(Object.assign(new THREE.LineSegments(ringGeo, ringMat), { frustumCulled:false }));
  // ── 六簇：一处一巧思，逐帧只改 position / aA（几何件数恒定 ⇒ 没有「突然多一枚」）──
  //   前五簇画在 kg 上，第六簇（更多场景 · 景深星丛）单独走 fg（更暗一档的材质）。
  //   ⚠ kg 只开前五簇的点数：多开的顶点会留在原点 (0,0,0)，而原点投影回舞台
  //     正好落在版心左上角 —— 净空闸会把这枚**根本没画出来的**假顶点算进去
  //     （本轮实测：clr 从 20.5 掉到 16.5，查了半天是它）。
  const LAY = [12, 15, 16, 8, 9, 20];                 // 六簇各自的点数
  const OFF = []; let CT = 0;
  LAY.slice(0, 5).forEach(k => { OFF.push(CT); CT += k; });
  const kg = new THREE.BufferGeometry(), kp = new Float32Array(CT*3);
  kg.setAttribute('position', new THREE.BufferAttribute(kp,3));
  const kA = fillAH(kg, 1, 0);
  const nodeMat = mkMat(SH, PX_PT_VS, PX_PT_FS); nodeMat.uniforms.uSoft.value = .04;
  scene.add(Object.assign(new THREE.Points(kg, nodeMat), { frustumCulled:false }));
  const farMat = mkMat(SH, PX_PT_VS, PX_PT_FS); farMat.uniforms.uSoft.value = .06;
  const fg = new THREE.BufferGeometry(), fp = new Float32Array(LAY[5]*3);
  fg.setAttribute('position', new THREE.BufferAttribute(fp,3));
  const fA = fillAH(fg, 1, 0);
  scene.add(Object.assign(new THREE.Points(fg, farMat), { frustumCulled:false }));
  function put(arr, i, x, y, z){ const q = loc(x, y, z);
    arr[i*3] = q[0]; arr[i*3+1] = q[1]; arr[i*3+2] = q[2]; }
  return {
    scene, camera, intro: 1.2, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      flows.forEach(f => f.draw(clock));
      /* ⑦ 迷你转子：呼吸只**向外**涨（净空的最坏情形恒在 rad=1）+ 粒子在环之间
         迁徙 + 三枚环各自翻滚、各带一道跑动的光弧 —— 与 P13 逐行同解，只是小一号 */
      const beat = 0.5 - 0.5*Math.cos(TAU*clock/5.4);
      const rad = 1 + Q.orbBr*beat;
      // 粒子带按 ν 在三枚环之间迁徙；倾角随所在的那一档环连续插值（不跳变）
      for(let i = 0; i < CN; i++){
        const nu = 0.5 + 0.5*Math.sin(TAU*(cNu[i] - clock/2.4));
        const o2 = orbAt(nu);
        const kf = nu <= 0.5 ? 2 - nu*2 : 1 - (nu-0.5)*2;   // 2 → 1 → 0 的连续档位
        const k0 = Math.min(2, Math.floor(kf)), k1 = Math.min(2, k0+1), fr = kf - k0;
        const tl = tiltOf(k0, clock)*(1-fr) + tiltOf(k1, clock)*fr;
        const q = orbPt(o2[0], o2[1], tl, cTh[i] + clock*cSp[i], rad);
        cp[i*3] = q[0]; cp[i*3+1] = q[1]; cp[i*3+2] = q[2];
        cA.a[i] = .30 + .70*nu;
      }
      cg.attributes.position.needsUpdate = true; cg.attributes.aA.needsUpdate = true;
      // 核：六条支线在核端的包络之和（归一到 0..1）⇒ aH 进 uHot / uGain
      let se = 0;
      for(let i = 0; i < flows.length; i++) se += envAt(-flows[i].spd*clock);
      dotA.h[0] = Math.max(0, Math.min(1, se/flows.length));
      dotA.a[0] = 0.62 + 0.38*dotA.h[0];                 // 地板 .62 ⇒ 核常亮
      coreDot.attributes.aA.needsUpdate = true;
      coreDot.attributes.aH.needsUpdate = true;
      let n3 = 0;
      for(let k = 0; k < 3; k++){
        const tl = tiltOf(k, clock);
        const arc = TAU*(clock*Q.orbArc[k]);
        for(let i = 0; i <= RSEG; i++){
          const th = i/RSEG*TAU, q = orbPt(OB[k][0], OB[k][1], tl, th, rad);
          // 环线的底亮比 P13 高两档（.22 → .55）：迷你尺寸下只靠光弧读不出「三枚环」
          const lit = .55 + .45*Math.pow(Math.max(0, Math.cos(th - arc)), 6);
          if(i > 0){ rA.a[n3] = lit;
            rpos[n3*3] = q[0]; rpos[n3*3+1] = q[1]; rpos[n3*3+2] = q[2]; n3++; }
          if(i < RSEG){ rA.a[n3] = lit;
            rpos[n3*3] = q[0]; rpos[n3*3+1] = q[1]; rpos[n3*3+2] = q[2]; n3++; }
        }
      }
      ringGeo.attributes.position.needsUpdate = true;
      ringGeo.attributes.aA.needsUpdate = true;
      // 六处身份微动
      Q.cl.forEach((c, k) => {
        const x0 = c[0], y0 = c[1], z0 = c[2], o = OFF[k], nk = LAY[k];
        if(k === 0){                       // 外呼：拨号脉冲串（一串一串地打出去）
          const ph = (clock/1.9) % 1, head = ph*1.45 - 0.22;
          for(let i = 0; i < nk; i++){ const u = i/(nk-1);
            put(kp, o+i, x0 - 56 + 112*u, y0, z0);
            kA.a[o+i] = 0.26 + 0.74*Math.exp(-Math.pow((u-head)/0.11, 2)); }
        }else if(k === 1){                 // 智能硬件：设备点阵亮灭
          const lit = ((clock/0.21)|0) % nk;
          for(let i = 0; i < nk; i++){
            put(kp, o+i, x0 - 48 + (i%5)*24, y0 - 12 + ((i/5)|0)*12, z0);
            kA.a[o+i] = i === lit ? 1 : (i === (lit+7)%nk ? .66 : .28); }
        }else if(k === 2){                 // 虚拟陪伴：柔和呼吸
          const rr = 12 + 8*(0.5 + 0.5*Math.sin(clock*TAU/4.6));
          for(let i = 0; i < nk; i++){ const a = (i/nk)*TAU;
            put(kp, o+i, x0 + Math.cos(a)*rr*2.4, y0 + Math.sin(a)*rr*0.68, z0);
            kA.a[o+i] = 0.42 + 0.36*(0.5 + 0.5*Math.sin(clock*TAU/4.6 + a)); }
        }else if(k === 3){                 // 口语陪练：一来一回
          for(let i = 0; i < 6; i++){ put(kp, o+i, x0 - 50 + 20*i, y0, z0);
            kA.a[o+i] = .28; }
          const p = 0.5 - 0.5*Math.cos(clock*TAU/3.0);
          put(kp, o+6, x0 - 50 + 100*p, y0 - 7, z0);      kA.a[o+6] = .95;
          put(kp, o+7, x0 + 50 - 100*p, y0 + 7, z0);      kA.a[o+7] = .95;
        }else if(k === 4){                 // 智能客服：排队消解（队头走一个，队伍前移）
          const t = (clock/0.62) % 1, gone = ((clock/0.62)|0) % nk;
          for(let i = 0; i < nk; i++){
            const idx = (i - gone + nk*2) % nk;
            put(kp, o+i, x0 - 56 + (idx - t)*13.5, y0, z0);
            kA.a[o+i] = idx === 0 ? (1-t)*.95 : .38 + .40*(1 - idx/nk); }
        }else{                             // 更多场景：景深处待命的微光星丛
          for(let i = 0; i < nk; i++){ const uv = r2(i+3);
            put(fp, i, x0 - 62 + uv[0]*124, y0 - 14 + uv[1]*28, z0);
            fA.a[i] = 0.30 + 0.60*(0.5 + 0.5*Math.sin(clock*0.55 + i*1.9)); }
        }
      });
      kg.attributes.position.needsUpdate = true; kg.attributes.aA.needsUpdate = true;
      fg.attributes.position.needsUpdate = true; fg.attributes.aA.needsUpdate = true;
    },
    applyTheme(){
      const pk = cssColor('--h-spoke'), rms = cssColor('--h-rms');
      flows.forEach(f => { f.theme(pk, rms, cssNum('--h-spoke-op', .42),
                                   cssNum('--h-rms-op', .58), .48);
        setBlend(f.mat, cssNum('--h-add', 0)); });
      ringMat.uniforms.uGain.value = 0;
      coreMat.uniforms.uColor.value.copy(cssColor('--h-core'));
      coreMat.uniforms.uHot.value.copy(cssColor('--h-core'));
      coreMat.uniforms.uOpacity.value = cssNum('--h-core-op', .92);
      coreMat.uniforms.uSize.value = cssNum('--h-core-size', 3.0);
      coreMat.uniforms.uGain.value = 0;
      ringMat.uniforms.uColor.value.copy(cssColor('--h-ring'));
      ringMat.uniforms.uHot.value.copy(cssColor('--h-ring'));
      ringMat.uniforms.uOpacity.value = cssNum('--h-ring-op', .66);
      ringMat.uniforms.uGain.value = 0;
      // 核：底色走 --h-core、热色走 --h-dot（与 P13 呼吸核同色档）· uGain 吃 aH
      dotMat.uniforms.uColor.value.copy(cssColor('--h-core'));
      dotMat.uniforms.uHot.value.copy(cssColor('--h-dot'));
      dotMat.uniforms.uOpacity.value = cssNum('--h-dot-op', .95);
      dotMat.uniforms.uSize.value = Q.corer*2;
      dotMat.uniforms.uGain.value = cssNum('--h-dot-gain', .55);
      dotMat.uniforms.uBack.value = 1;
      setBlend(dotMat, cssNum('--h-add', 0));
      nodeMat.uniforms.uColor.value.copy(cssColor('--h-node'));
      nodeMat.uniforms.uHot.value.copy(cssColor('--h-node'));
      nodeMat.uniforms.uOpacity.value = cssNum('--h-node-op', 1);
      nodeMat.uniforms.uSize.value = cssNum('--h-node-size', 4.0);
      nodeMat.uniforms.uGain.value = 0;
      farMat.uniforms.uColor.value.copy(cssColor('--h-far'));
      farMat.uniforms.uHot.value.copy(cssColor('--h-far'));
      farMat.uniforms.uOpacity.value = cssNum('--h-far-op', .90);
      farMat.uniforms.uSize.value = cssNum('--h-far-size', 3.0);
      farMat.uniforms.uGain.value = 0;
      // ⚠ 六簇坐在 --card-bg（72% 不透明）**背后**：屏上只剩三成。
      //   所以 uBack（深度雾的余亮）要按「透过卡之后还读不读得出」定档 ——
      //   核与两枚环在卡间空档里是全亮的，两者的档次因此不一样。
      coreMat.uniforms.uBack.value = .80; ringMat.uniforms.uBack.value = .80;
      nodeMat.uniforms.uBack.value = .74; farMat.uniforms.uBack.value = .70;
      [coreMat, ringMat, nodeMat, farMat].forEach(m => setBlend(m, cssNum('--h-add', 0)));
    },
    state(){
      let clr = 1e9;
      flows.forEach(f => { clr = Math.min(clr, geoClr(f.geo, U, Q.ink, Q.w01[1])); });
      const nsz = nodeMat.uniforms.uSize.value*0.5 + 0.5;
      clr = Math.min(clr, geoClr(kg, U, Q.ink, nsz), geoClr(fg, U, Q.ink, nsz),
                     geoClr(cg, U, Q.ink, coreMat.uniforms.uSize.value*0.5 + 0.5),
                     geoClr(ringGeo, U, Q.ink, 1.0),
                     geoClr(coreDot, U, Q.ink, Q.corer));
      return { clr, spokes: flows.length, nodes: CT, core: CN, orb: OB.length,
               tilt: [0,1,2].map(k => +tiltOf(k, SH.uTime.value).toFixed(2)),
               dot: +dotA.a[0].toFixed(3),
               spd: flows.map(f => f.spd), lam: Q.lam,
               z: Q.cl.map(c => c[2]), cz: Q.cz };
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ㉒-④ 通话流（P16 · Call Agent 成绩单）
   ───────────────────────────────────────────────────────────────────────────
   这一页 3D 语义最弱（数字卡 + 对照表），所以做**克制的证据场**：
   「1,000+ 通 / 天 · 多路并发」= 一束细密的通话流（audioStream 血统），七股并行、
   从左涌入、过了 x624 之后向右铺开 —— 读作「一直在打、并发在跑」。
   先并拢再铺开不是造型：页面左半有「02 · KEY DIFFERENCE」那行小标，铺开就压字；
   右半是空的，扇形正好占住。这条形也顺手把上面的成绩单与下面的对照表缝在一起。
   ⚠ 流是**均质的一束**：不给任何一张卡加权 —— 96.5% 的 hot 是页面既有语义，
     3D 不新造第二处热点。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeCalls(ctx){
  const Q = K.nb, w = ctx.rect[2], h = ctx.rect[3], D = Q.D;
  const scene = new THREE.Scene(), camera = camPx(w, h, D);
  const SH = pxShared(D, Q.half), L = mkLock(w, h, D), U = unlock(w, h, D, ctx.rect);
  const R = ctx.rect;
  /* ⑥ 八条水平细带（4px 一段现铺 —— aG 是逐顶点属性，点疏了通话段就落不到点上）*/
  const NL = +Q.n, X0 = Q.x[0], X1 = Q.x[1], NP = Math.round((X1-X0)/4) + 1;
  const flows = [];
  for(let i = 0; i < NL; i++){
    const pts = [];
    for(let j = 0; j < NP; j++)
      pts.push(L(X0 + (X1-X0)*j/(NP-1) - R[0], Q.y[i] - R[1], Q.sz[i]));
    flows.push(mkStream(SH, pts, { w:Q.w, spd:Q.spd[i], lam:Q.lam }).add(scene));
  }
  /* 通话段：一条**确定性**的方波（起停走 smootherstep，零随机源、零分支）——
     段周期 / 占空 / 起相位八条各不相同 ⇒ 屏上永远有几路在讲、几路刚挂断，
     而八条一起在跑就是「并发」。gain=0 的那一段落到 ghost 档 = 线还在，通话没在。 */
  for(let i = 0; i < NL; i++){
    const T = Q.call[i][0], duty = Q.call[i][1], ph = Q.call[i][2], e = Q.ce;
    flows[i].gain((u) => {
      let q = (u/T + ph) % 1; if(q < 0) q += 1;
      return smoother(0, e, q) * (1 - smoother(duty-e, duty+e, q));
    });
  }
  return {
    scene, camera, intro: 1.1, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){ SH.uTime.value = clock; flows.forEach(f => f.draw(clock)); },
    applyTheme(){
      const pk = cssColor('--n-flow'), rms = cssColor('--n-rms');
      flows.forEach(f => { f.theme(pk, rms, cssNum('--n-flow-op', .70),
                                   cssNum('--n-rms-op', .60), .66);
        setBlend(f.mat, cssNum('--n-add', 0)); });
    },
    state(){
      let clr = 1e9;
      flows.forEach(f => { clr = Math.min(clr, geoClr(f.geo, U, Q.ink, Q.w)); });
      return { clr, lanes: flows.length, spd: flows.map(f => f.spd), lam: Q.lam,
               z: Q.sz.slice() };
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   单渲染器巡游 · TOUR
   ───────────────────────────────────────────────────────────────────────────
   全 deck **一个 WebGLRenderer、一块 canvas**。canvas 平时停在车库（屏外），
   翻到有场景的页就被 appendChild 进那一页的 .lab-stage、按 data-lab-rect 对位、
   热切换到该页的场景；翻到没有场景的页就回车库、canvas 隐身。
   于是：① 浏览器的「同页面 WebGL 上下文上限」从根上不存在（16 个 3D 页也只吃一枚）；
        ② 任一时刻只有一个场景在渲染，22 页里没有任何一页在偷偷空转；
        ③ 加一页 3D 只需要「写一个场景工厂 + 在 LAB_RECTS 里加一行」。

   ⚠ 判活一律**从 DOM 读**（.active / [data-step].on），不读 deck.i ——
     现场翻页（deck.go）与 qa / occlusion-scan / 截图脚本（直接 classList.toggle）
     两条路径共用同一套判据，不会出现「现场在跑、截图里没跑」这种分叉。
   ═══════════════════════════════════════════════════════════════════════════ */
const CANVAS = document.getElementById('labGl');
const GARAGE = document.getElementById('labGarage');
const FACTORY = { voice:makeVoice, globe:makeGlobe, brain:makeBrain,
                  shell:makeShell, spiral:makeSpiral, terrain:makeTerrain, duplex:makeDuplex,
                  /* 第二波（九页套件化 · 终波）*/
                  morph:makeMorph, lanes:makeLanes, chain:makeChain, cutin:makeCutin,
                  bigmap:makeBigmap, qos:makeQos, vision:makeVision, slots:makeSlots,
                  towers:makeTowers,
                  /* ⑥ 互动星系（P22 · 在页 3D）+ 三轮「静态页升维」的三枚加法层 */
                  galaxy:makeGalaxy, three:makeThree, hub:makeHub, calls:makeCalls };
const STAGES = [...document.querySelectorAll('.lab-stage')].map(el=>({
  el, page:+el.dataset.labPage, name:el.dataset.labScene,
  rect:el.dataset.labRect.split(',').map(Number),
  print:el.querySelector('.lab-print'),
  slide:el.closest('.slide'), unit:null,
}));
const TOUR = { page:0, scene:'', mounts:0, leaves:{}, pages:STAGES.map(s=>s.page) };
window.__labTour = TOUR;
document.documentElement.dataset.labScenes = TOUR.pages.join(',');

function markPoster(why){
  const c = CANVAS;
  if(c){ c.dataset.labMode='POSTER'; c.dataset.labRun='0'; }
  document.querySelectorAll('.lab-stage').forEach(s=>s.classList.remove('gl-up'));
  if(c && c.parentNode!==GARAGE && GARAGE) GARAGE.appendChild(c);
  document.documentElement.setAttribute('data-lab-poster','1');
  paintProbe();
  console.info('[convoai-lab] poster 降级：'+why);
}
function paintProbe(){
  const p = document.getElementById('labProbe'); if(!p||!CANVAS) return;
  const d = CANVAS.dataset;
  p.innerHTML = '<span>'+((d.labScene||'—').toUpperCase())+' P'+(d.labPage||'—')+'</span>'
    + '<span class="sep">/</span><span>FPS <b>'+(d.labFps||'—')+'</b></span>'
    + '<span class="sep">/</span><span>DPR '+(d.labDpr||'—')+'</span>'
    + '<span class="sep">/</span><span>THREE r'+K.rev+'</span>'
    + '<span class="sep">/</span><span>'+(d.labMode||'BOOT')+'</span>';
}

let renderer=null, cur=null, raf=0, last=0, clock=0, tIntro=0, paced=0;
let running=false, degraded=false, booted=false;
let frames=0, fpsT=0, startT=0, tot=0;
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

function stageScale(){
  return Math.min(1, Math.min(window.innerWidth/1920, window.innerHeight/1080) || 1);
}
function pixRatio(){
  // DPR 上限 2，再乘舞台缩放：小窗口下不白烧像素（舞台是 transform:scale 的固定 1920 画布）
  return Math.min(window.devicePixelRatio||1, 2) * stageScale();
}
function mount(s){
  const r = s.rect;
  CANVAS.style.left = r[0]+'px'; CANVAS.style.top = r[1]+'px';
  CANVAS.style.width = r[2]+'px'; CANVAS.style.height = r[3]+'px';
  if(CANVAS.parentNode !== s.el) s.el.appendChild(CANVAS);
  CANVAS.classList.toggle('lab-grab', !!s.unit.grab);
  const pr = pixRatio();
  renderer.setPixelRatio(pr);
  renderer.setSize(r[2], r[3], false);
  s.unit.onDPR(pr);
  CANVAS.dataset.labPage = String(s.page);
  CANVAS.dataset.labScene = s.name;
  CANVAS.dataset.labDpr = String(Math.round(pr*100)/100);
  TOUR.page = s.page; TOUR.scene = s.name; TOUR.mounts++;
  cur = s;
}
function unmount(){
  if(cur){
    cur.el.classList.remove('gl-up');
    if(cur.unit.onLeave) cur.unit.onLeave();
    cur.unit.setIntro(0);
    TOUR.leaves[cur.page] = (TOUR.leaves[cur.page]||0)+1;
  }
  CANVAS.classList.remove('lab-grab');
  if(CANVAS.parentNode !== GARAGE) GARAGE.appendChild(CANVAS);
  CANVAS.dataset.labPage='0'; CANVAS.dataset.labScene='';
  TOUR.page = 0; TOUR.scene='';
  cur = null;
}
function applyStep(s){
  if(!s.unit.setStep || !s.slide) return;
  let n = 0;
  s.slide.querySelectorAll('[data-step]').forEach(e=>{
    if(e.classList.contains('on')) n = Math.max(n, +e.dataset.step||0); });
  s.unit.setStep(n);
}
function frame(dt){
  if(!cur) return;
  clock += dt;
  if(tIntro < 1) tIntro = Math.min(1, tIntro + (dt / cur.unit.intro));
  cur.unit.setIntro(easeFlow(tIntro));
  cur.unit.draw(dt, clock);
  renderer.render(cur.unit.scene, cur.unit.camera);
}
function loop(ts){
  raf = requestAnimationFrame(loop);
  if(!startT) startT = ts;
  // 定拍模式：rAF 照跑（每帧都重画 ⇒ 绘制缓冲区始终是新的，截图不会截到空帧），
  // 但**钟不走** —— 钟只在 TOUR.step() 里按 1/fps 前进。
  const dt = paced ? 0 : Math.min(0.05, last ? (ts-last)/1000 : 0.016); last = ts;
  frame(dt); frames++; tot++;
  if(ts-fpsT > 500){ CANVAS.dataset.labFps = String(Math.round(frames*1000/(ts-fpsT)));
    frames=0; fpsT=ts; paintProbe(); }
  // 自动降级：连续 2s 平均 < 20fps ⇒ 退 poster（`?lab=hold` 关掉这一条）
  const el = (ts-startT)/1000;
  if(!FLAGS.hold && !degraded && el >= 2.0 && (tot/el) < 20) degrade();
}
function degrade(){
  degraded = true; stop(); unmount();
  CANVAS.dataset.labMode='POSTER'; CANVAS.dataset.labDegraded='1';
  document.documentElement.setAttribute('data-lab-poster','1');
  paintProbe();
  console.info('[convoai-lab] FPS 连续 2s < 20 ⇒ 自动退 poster');
}
function start(){
  if(degraded || !cur) return;
  if(reduced.matches){            // 尊重系统设置：渲一帧（入场落位）就停帧
    tIntro=1; frame(0);
    cur.el.classList.add('gl-up');
    CANVAS.dataset.labMode='STILL'; CANVAS.dataset.labRun='0'; CANVAS.dataset.labFps='—';
    paintProbe(); return;
  }
  if(raf) return;
  last=0; startT=0; tot=0; frames=0; fpsT=performance.now();
  raf = requestAnimationFrame(loop);
  CANVAS.dataset.labMode='LIVE'; CANVAS.dataset.labRun='1'; paintProbe();
}
function stop(){ if(raf){ cancelAnimationFrame(raf); raf=0; } CANVAS.dataset.labRun='0'; }

function enter(s){
  if(cur === s) return;
  stop(); unmount();
  mount(s);
  // 复位入场参数 ⇒ 回到该页重放。**定拍模式例外**：那时 dt 恒为 0，入场再也走不完，
  // 换页之后整页的「长出来」参数会永远停在 0（带子零宽 = 整层看不见）。
  // 本轮实拍踩过一次：录完 P14 没退定拍就去拍 P18，LOOP 环带整条消失。
  clock=0; tIntro = paced ? 1 : 0;
  applyStep(s);
  if(s.unit.onEnter) s.unit.onEnter();
  frame(0);                                // 先渲一帧，**场景 ready** 之后才让 poster 让位
  s.el.classList.add('gl-up');
}
function leaveAll(){
  stop(); unmount();
  if(CANVAS.dataset.labMode !== 'POSTER') CANVAS.dataset.labMode = 'IDLE';
  paintProbe();
}
function syncActive(){
  if(degraded) return;
  const act = document.querySelector('.slide.active');
  const p = act ? (+act.dataset.p || 0) : 0;
  const s = STAGES.find(x => x.page === p);
  if(!s || document.hidden){
    if(document.hidden && cur){ stop(); if(CANVAS.dataset.labMode==='LIVE') CANVAS.dataset.labMode='IDLE'; paintProbe(); return; }
    running = false; leaveAll(); return;
  }
  running = true;
  enter(s);
  applyStep(s);
  start();
}

/* ── TOUR.pace · **录屏定拍器**（二轮精修 · 波A 的必备件）────────────────
   容器里是软渲染，实测只有 3–4 fps。按真实 dt 录出来的 GIF 名义 12fps、
   实际 3.4fps ⇒ 放出来**快 3.5×**，而本波终审第一位的判据正是「速度是否从容」——
   录快了就没法看，更没法验。定拍之后：
     pace(fps)  停 rAF，改成手动推帧，每帧钟只走 1/fps（录多久就是多久）；
     step(n)    手动推 n 帧并各渲一帧（截图脚本每推一帧截一张）；
     seek(t)    直接跳到第 t 秒并渲一帧（闸门验「某一刻的场上状态」用它）；
     pace(0)    回到 rAF。
   这三件同时是 ⑲ 闸的探针入口 —— 不必截帧比像素就能验时序。 */
TOUR.pace = function(fps){
  if(!fps){ paced = 0; return 0; }
  paced = 1/fps; tIntro = 1;                 // 定拍前入场必须已经走完（否则 dt=0 会把它冻住）
  if(cur && !raf && !reduced.matches) start();
  return paced;
};
TOUR.step = function(n){ clock += (paced || 1/12) * Math.max(1, n|0); return clock; };
TOUR.seek = function(t){ clock = +t || 0; tIntro = 1; frame(0); return clock; };
TOUR.unit = function(){ return cur ? cur.unit : null; };
/* TOUR.shot · **同 tick** 的像素读回（波B 的消闪闸用它）────────────────────
   renderer 没开 preserveDrawingBuffer（常态零显存代价），所以像素只能在
   「渲完这一帧的**同一个任务**里」读回来 —— 隔一个 tick 合成器就把缓冲区清了。
   返回：整幅平均亮度 + bw×bh 分块平均亮度（Rec.601 luma，透明处天然是 0）。
   闸门拿它逐帧做差：亮度**突变**才是「闪」，位移不是。 */
TOUR.shot = function(bw, bh){
  if(!cur || !renderer) return null;
  frame(0);                                        // ← 同 tick：先渲，再读
  const gl = renderer.getContext();
  const W2 = CANVAS.width, H2 = CANVAS.height;
  const buf = new Uint8Array(W2*H2*4);
  gl.readPixels(0, 0, W2, H2, gl.RGBA, gl.UNSIGNED_BYTE, buf);
  const BW = bw||8, BH = bh||8, sum = new Float64Array(BW*BH), cnt = new Float64Array(BW*BH);
  let tot = 0, alp = 0, cov = 0;
  for(let y = 0; y < H2; y++){
    const by = Math.min(BH-1, (y*BH/H2)|0);
    for(let x = 0; x < W2; x++){
      const o = (y*W2+x)*4;
      const l = 0.299*buf[o] + 0.587*buf[o+1] + 0.114*buf[o+2];
      const bi = by*BW + Math.min(BW-1, (x*BW/W2)|0);
      sum[bi] += l; cnt[bi]++; tot += l;
      alp += buf[o+3]; if(buf[o+3] >= 8) cov++;
    }
  }
  const blocks = [];
  for(let i = 0; i < BW*BH; i++) blocks.push(sum[i]/(cnt[i]||1));
  // ink = 平均 alpha（「这一页画了多少墨」）· cov = alpha≥8 的像素占比（「铺了多广」）
  return { mean: tot/(W2*H2), blocks, w: W2, h: H2,
           ink: alp/(W2*H2*255), cov: cov/(W2*H2) };
};
TOUR.clock = function(){ return clock; };

/* ═══ 装配 ═══════════════════════════════════════════════════════════════ */
if(!webglOK()){
  markPoster('no-webgl');
}else{
  try{
    renderer = new THREE.WebGLRenderer({canvas:CANVAS, antialias:true, alpha:true,
                                        powerPreference:'high-performance'});
    renderer.setClearAlpha(0);
    renderer.setSize(16,16,false);
    STAGES.forEach(s=>{
      const f = FACTORY[s.name];
      if(!f) throw new Error('未知场景 '+s.name+'（P'+s.page+'）');
      s.unit = f({ rect:s.rect, canvas:CANVAS, stage:s.el, page:s.page, print:s.print });
      s.unit.applyTheme();
      s.unit.setIntro(0);
      // 预热：在车库里以 16×16 渲一帧，把着色器编译落在启动期（翻到该页不会卡首帧）
      renderer.render(s.unit.scene, s.unit.camera);
      s.el.dataset.labReady = '1';
    });
    booted = true;
    CANVAS.dataset.labMode = 'IDLE';
  }catch(e){
    console.info('[convoai-lab] boot 失败：'+(e&&e.message));
    markPoster('boot-fail');
    booted = false;
  }
}

if(booted){
  /* 页面不可见就把 rAF 掐掉，回来续跑（与非激活 slide 是两道独立的闸，双双 cancel） */
  document.addEventListener('visibilitychange', function(){
    if(document.hidden){ stop(); if(CANVAS.dataset.labMode==='LIVE') CANVAS.dataset.labMode='IDLE'; paintProbe(); }
    else syncActive();
  });
  window.addEventListener('resize', function(){
    if(cur){ const pr=pixRatio(); renderer.setPixelRatio(pr);
      renderer.setSize(cur.rect[2],cur.rect[3],false); cur.unit.onDPR(pr);
      CANVAS.dataset.labDpr=String(Math.round(pr*100)/100); if(!raf) frame(0); }
  });
  /* 打印帧：render-then-read —— 不开 preserveDrawingBuffer（常态零显存代价），
     在 beforeprint 这个**同步**事件里先渲一帧、立刻 toDataURL，绘制缓冲区还没被
     合成器清掉，读到的就是非空帧。纸上 22 页一起铺开，canvas 只在当前那一页里，
     所以其余 3D 页在纸上一律以 poster（= 页上原来那张 SVG）为准。 */
  window.addEventListener('beforeprint', function(){
    try{
      if(!cur) return;
      tIntro = 1; frame(0);
      const url = renderer.domElement.toDataURL('image/png');
      if(url && url.length > 2000 && cur.print) cur.print.setAttribute('src', url);
    }catch(e){}
  });
  /* 主题：**延一个 rAF** 再读 —— 换页交叠时 CSS 变量还没落到新主题上，
     同帧读会读到上一主题的色。七个场景一起热更新（不只当前那个）。 */
  new MutationObserver(function(){
    requestAnimationFrame(function(){
      STAGES.forEach(s=>{ if(s.unit) s.unit.applyTheme(); });
      if(!raf) frame(0);
    });
  }).observe(document.documentElement, {attributes:true, attributeFilter:['data-theme']});
  reduced.addEventListener?.('change', function(){ stop(); if(running) start(); });

  /* 两道保险各管一段（与 P20 视频页同一手法，**不改共享 deck.js**）：
       ① 包 deck.go / deck.applySteps —— 现场翻页走这条；
       ② MutationObserver 盯 .slide 与分步容器的 class —— qa / occlusion-scan /
          截图脚本是直接 classList.toggle 的，只有这一道盯得住。 */
  if(window.deck){
    ['go','applySteps'].forEach(function(m){
      const f = window.deck[m];
      window.deck[m] = function(){ const r = f.apply(this, arguments); syncActive(); return r; };
    });
  }
  let pend=false;
  const mo = new MutationObserver(function(){
    if(pend) return; pend=true;
    requestAnimationFrame(function(){ pend=false; syncActive(); });
  });
  document.querySelectorAll('.slide').forEach(function(sec){
    mo.observe(sec,{attributes:true,attributeFilter:['class']});
  });
  STAGES.forEach(function(s){
    if(!s.slide) return;
    s.slide.querySelectorAll('[data-step]').forEach(function(c){
      mo.observe(c,{attributes:true,attributeFilter:['class']});
    });
  });
  syncActive();
  paintProbe();
  window.__labReady = STAGES.length;
}
"""


# ── 常量表：构建期算好，运行时直接吃 ───────────────────────────────────────
#   poster 与 WebGL 逐字同参的唯一保证；也是「3D 不新造坐标」的唯一保证 ——
#   五枚新场景的几何全部是各页 SVG 路径的展平结果（见上面的 lab-kit 几何预处理）。
#   ⚠ lab_k() 必须在**所有页面定义之后**调用（build() 里调），它要读各页的路径常量。
THREE_REV = (lambda s: (_re2.search(r'(?:const|let|var)\s+\w+\s*=\s*"(\d{3})"[,;]', s)
                        or _re2.search(r'"(\d{3})"', s)).group(1))(
    (ROOT / "public" / "decks" / "assets" / "three" / "three.core.min.js").read_text(encoding="utf-8"))


def _n(x):
    """JS 数字字面量：短、无科学计数法、两边解析结果一致"""
    return ("%.6f" % x).rstrip("0").rstrip(".") if isinstance(x, float) else str(x)


def _arr(xs):
    return "[" + ",".join(_n(float(x)) for x in xs) + "]"


def _sarr(xs):
    return "[" + ",".join('"%s"' % x for x in xs) + "]"


def _obj(d):
    # 键重名当场炸：JS 对象字面量里后写的那个静默胜出，于是「几何常量」会被
    # 另一件东西顶掉，屏上只剩 NaN（本轮踩过一次：02 的 lane 半宽把星格宽度
    # `lw` 顶了，MO_HEAD 整段编译失败）。K 表是全 deck 的几何真相，不许重名。
    ks = [k for k, _v in d]
    assert len(ks) == len(set(ks)), \
        "K 表键重名：%r" % sorted({k for k in ks if ks.count(k) > 1})
    return "{" + ",".join("%s:%s" % (k, v) for k, v in d) + "}"


def lab_k():
    # ── ③ 大脑（P17）：母形 = 页上那条 13 段贝塞尔侧视轮廓 ──────────────────
    bb = _bbox(_BRAIN)
    bc = [(bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0]
    # 突触弧的 z 拱幅度：按弧的 2D 长度给（长弧跨半球跨得深，短弧只是就近搭一把）
    _arcA = [0.42 * a[1] for a in _ARCS]
    _spark = [(k, _sec(a[2]), _sec(a[3])) for k, a in enumerate(_ARCS)] \
           + [(k, _sec(_ARCS[k][2]), _sec(d)) for k, d in _ARC_EXTRA]
    b = _obj([
        ("cont", '"%s"' % _poly(_BRAIN, per=18, tol=1.2)),
        ("zones", "[" + ",".join('"%s"' % _polym(z[0]) for z in _ZONES) + "]"),
        ("sul", "[" + ",".join('"%s"' % _poly(s) for s in (_SUL1, _SUL2, _SUL3)) + "]"),
        # 三条沟的刻槽深度 / 宽度：外侧裂（Sylvian）最深 —— 它是这张侧视图最容易被
        # 读懂的解剖特征，3D 里必须还是一道真沟，不能被厚度剖面填平。
        ("sulD", _arr([0.30, 0.56, 0.34])),
        ("sulW", _arr([22, 27, 20])),
        ("bb", _arr(bb)), ("c", _arr(bc)),
        ("tmax", _n(132.0)), ("dref", _n(108.0)), ("n", "12000"),
        ("arcs", "[" + ",".join('"%s"' % _poly(a[0], per=16, tol=2.0) for a in _ARCS) + "]"),
        ("arcA", _arr(_arcA)),
        ("spark", "[" + ",".join(_arr(s) for s in _spark) + "]"),
        ("zper", _arr([_sec(z[1]) for z in _ZONES])),
        ("zoff", _arr([_sec(z[2]) for z in _ZONES])),
        ("inp", '"%s"' % _poly(_BRAIN_IN, per=16, tol=2.0)),
        ("outX", _n(1088.0)), ("out", _arr([1214, 268])), ("out2", _arr([1386, 268])),
        # 小脑 / 脑干：页上是两枚独立闭合小形，3D 里也各成一团（半厚度小一档，
        # 它们本来就比大脑窄）。aZone=-1 ⇒ 不参与五区放电。
        ("sub", "[" + ",".join('"%s"' % _poly(d, per=16, tol=1.4) for d in (_CEREB, _STEM)) + "]"),
        ("subT", _arr([52, 30])), ("subN", "1500"),
        ("sway", _n(12.0)), ("swayP", _n(17.0)),
    ])
    # ── ④ 双层防御壳（P9）：环心 / 两层半径 / 缺口 / 三路噪声主方向全部抄页上 ──
    _d1 = (613 - _SCX, -(50 - _SCY))
    _d2 = (613 - _SCX, -(196 - _SCY))
    _d3 = (613 - _SCX, -(342 - _SCY))
    def _u3(v):
        m = math.hypot(v[0], v[1]) or 1.0
        return [v[0] / m, v[1] / m, 0.0]
    s = _obj([
        ("c", _arr([_SCX, _SCY])),
        ("r1", _n(float(_SR1))), ("r2", _n(float(_SR2))),
        ("rc", _n(float(_SAG) * 0.46)), ("r0", _n(346.0)),
        # 缺口：页上外环开 ±40/r138、内环开 ±34/r86 —— 3D 里换算成绕 -X 轴的锥角，
        # 并各放宽一档（球面上 17° 的洞在屏上小得看不出「开着」）。
        ("gap2", _n(math.cos(35.0 * math.pi / 180))),
        ("gap1", _n(math.cos(40.0 * math.pi / 180))),
        ("d1", _arr(_u3(_d1))), ("d2", _arr(_u3(_d2))), ("d3", _arr(_u3(_d3))),
        # 二轮精修 · 波A：四股的周期一律由「行程 ÷ 目标流速」反推（_spd_rows(9)）——
        # 旧版噪声 50–69 而目标人声 155–217，同页三倍差把「谁重要」讲成了「谁快」。
        ("dur", _arr([_dur_at(L, sp) for _nm, L, sp in _spd_rows(9)])),
    ])
    # ── ⑤ 复利螺旋（P18）：脊线 = 页上那条成长曲线本人 ────────────────────
    _r18 = _spd_rows(18)
    r = _obj([
        ("spine", '"%s"' % _poly(_CA_CURVE, per=20, tol=1.2)),
        ("r0", _n(_CA_R0)), ("r1", _n(_CA_R1)), ("turns", _n(_CA_TURNS)),
        ("w0", _n(4.0)), ("w1", _n(22.0)), ("n", str(_CA_N)),
        ("days", _arr([_CA_X(x) for x, _nm in _CA_DAYS])),
        ("climb", _n(_dur_at(_r18[0][1], _r18[0][2]))),
        # 二轮精修 · 波A：相机从 D560 换到 D1500（560 档水平视场 112°，环画到边被剪斜），
        # 螺旋用 mkRelock 逐像素还原 —— 拍板过的形不该因为隔壁多了一枚环就变。
        ("D0", _n(560.0)), ("D", _n(1500.0)), ("half", _n(70.0)),
        # 「真人销冠」基准虚线（波A 补回：3D 里原来没画，页上四个字指着空白）
        ("base", _arr([_CA_X(150), 160, _CA_X(1060)])), ("baseDash", _arr([7, 6])),
        # LOOP 环带（投影锁）：环心 / 半径 / 站点 / 站点半径 / 局部右移 / 一圈的秒数
        ("ring", _arr(_CA_RING)), ("rdx", _n(float(_CA_RDX))),
        ("node", "[" + ",".join(_arr((x, y)) for x, y, _nm in _CA_LOOP) + "]"),
        ("nodeR", _n(float(_CA_NODE_R))),
        ("ringTz", _n(0.85)), ("ringW", _n(13.0)),
        ("ringDur", _n(_dur_at(_r18[1][1], _r18[1][2]))), ("ringSpd", _n(_SPD_P18[1])),
        ("ringN", "3"),      # 环上 3 个整波长 ⇒ 基频在闭环上严丝合缝
    ])
    # ── ⑥ 声学地形（P7）：脊线 = 页上那条逐帧概率曲线（局部坐标左移 660）──
    #    波B 消闪：曲线**周期化**成一张定长表（_vad_tables），几何建满两个周期，
    #    每帧只设 scroll.position.x —— 一格顶点都不重算，闪的物理前提就没有了。
    _hp, _gap, _ons = _vad_tables()
    t = _obj([
        ("curve", '"%s"' % _poly(_VADCURVE, per=18, tol=1.2, dx=660.0)),
        ("sem", '"%s"' % _poly(_VADSEM, per=18, tol=1.2, dx=660.0)),
        ("base", _n(132.0)), ("nx", "150"), ("nz", "13"),
        ("x0", _n(_T_X0)), ("x1", _n(_T_X1)), ("zw", _n(68.0)), ("sig", _n(40.0)),
        ("band", _arr([_VTOP, _VBOT])),
        ("pins", _arr([_VSOS - 660, _VEOS - 660])), ("pinTop", _n(26.0)),
        ("semZ", _n(52.0)), ("tilt", _n(-0.17)),
        # 波B：周期化脊线表 / 谷长表 / 起声表（全部对**材料坐标**预计算 · 定长 _T_NT）
        ("hp", _arr(_hp)), ("gap", _arr(_gap)), ("ons", _arr(_ons)),
        ("nt", str(_T_NT)), ("per", _n(_T_X1 - _T_X0)),
        ("spd", _n(_SPD_P7)), ("lap", _n((_T_X1 - _T_X0) / _SPD_P7)),
        ("halo", _arr(_T_HALO)), ("pil", _arr(_T_PIL)),
        ("semW", _n(_T_SEMW)), ("feedW", _n(_T_FEEDW)), ("feedZ", _n(_T_FEEDZ)),
    ])
    # ── ⑦ 全双工双向声带（P4）：截断 x 就是页上三条泳道共用的那根垂线 ─────
    _r4 = _spd_rows(4)
    d = _obj([
        ("x0", _n(_D_X0)), ("x1", _n(_D_X1)), ("yc", _n(_D_YC)),
        ("amp", _n(_D_AMP)), ("dep", _n(_D_DEP)), ("turns", _n(_D_TURNS)),
        ("phase", _n(_D_PHASE)),
        ("lap0", _n(10.0)), ("lap1", _n(64.0)),
        ("cut", _n(float(_XIN))), ("ghost", _n(0.16)),
        ("cy0", _n(60.0)), ("cy1", _n(330.0)), ("n", str(_D_N)),
        ("hw", _n(11.0)),
        # 波A：两条带的周期由各自的弧长 ÷ 目标流速反推（旧：324 / 375px/s）
        ("durA", _n(_dur_at(_r4[0][1], _r4[0][2]))),
        ("durB", _n(_dur_at(_r4[1][1], _r4[1][2]))),
    ])
    # ══ 第二波九枚场景（2026-08-31 · 终波）══════════════════════════════════
    #   几何一律从上面那批名册与页上的 d= 里来；调参一律是深度 / 周期 / 相位。
    _rows = lambda xs: "[" + ",".join(_arr(r) for r in xs) + "]"
    # ⑧ P2 模态转换剧场（波B · 王冠一）—— 三个解析目标的**全部参数**只有这一份，
    #    poster（构建期，见 _mo_poster）与顶点着色器（运行时，见 MO_HEAD）同吃它。
    o = _obj([
        ("arc", '"%s"' % _poly(_P2ARC, per=18, tol=1.2)),
        ("box", _rows(_P2N)), ("hotCol", str(_O_HOTCOL)),
        ("cyc", _n(_MO_CYC)), ("gen", _n(_MO_GEN)),
        ("ph", _arr(_MO_PH)), ("life", _arr(_MO_LIFE)),
        ("yaw", _arr(_MO_YAW)), ("yawA", _n(_MO_YAWA)),
        ("x0", _n(_MO_X0)), ("x1", _n(_MO_X1)), ("outdx", _n(_MO_OUTDX)),
        ("yc", _n(_MO_YC)), ("hw", _n(_MO_HW)), ("amp", _n(_MO_AMP)), ("dz", _n(_MO_DZ)),
        ("na", str(_MO_NA)), ("nb", str(_MO_NB)), ("nc", str(_MO_NC)),
        ("lcx", _n(_MO_LCX)), ("lw", _n(_MO_LW)), ("lh", _n(_MO_LH)), ("ld", _n(_MO_LD)),
        ("f1", _n(_MO_F1)), ("f2", _n(_MO_F2)), ("fb", _n(_MO_FB)),
        ("rip", _n(_MO_RIP)), ("rlam", _n(_MO_RLAM)), ("rper", _n(_MO_RPER)),
        ("crest", _n(_MO_CREST)),
        # 两条波场的波峰速度（A 档 · _spd_rows(2) 是同一份真相）
        ("spd", _arr([sp for _nm, _L, sp in _spd_rows(2)])),
        ("arcW", _n(_MO_ARCW)), ("arcWin", _arr(_MO_ARC)),
        ("arcSpd", _n(_SPD_P2[0])),
        # ── 02「两制对照」（表达力精进 ①）：相机按剧场原高架 + setViewOffset ──
        ("h0", _n(_MO_H0)), ("ay", _n(_P2AY)),
        ("tx0", _n(_P2TX0)), ("tx1", _n(_P2TX1)),
        ("ry", _n(_P2RY)), ("rw", _n(_P2RW)),
        ("seg", _rows(_P2SEG)), ("sege", _n(_P2SEGE)),
        ("evt", _n(_P2EVT)), ("evh", _n(_P2EVH)),
        ("dash", _rows(_P2DASH)),
        ("ly", _arr(_P2LY)), ("lhw", _arr(_P2LW)), ("lg", _arr(_P2LG)),
        ("spk", _n(_P2SPK)), ("duck", _n(_P2DUCK)),
        ("spdb", _arr(_SPD_P2B)),
    ])
    # ⑨ P3 双工三通道（bands / ch 两张表逐条来自页上的 band() 与 pk()）
    _modes = "[" + ",".join(
        _obj([("bands", _rows(_P3BANDS[m])),
              ("ch", _rows([(c[0], c[1], c[2], c[3], c[4], c[5], c[6]) for c in _P3CH[m]]))])
        for m in ("simplex", "half", "full")) + "]"
    l = _obj([
        ("modes", _modes), ("lx", _n(float(_P3LX))), ("rx", _n(float(_P3RX))),
        ("cw", _n(float(_P3CW))), ("ct", _n(float(_P3CT))),
        ("s", _n(P3_FIG_S)), ("dy", _n(P3_FIG_DY)), ("gap", _n(float(P3_FIG_GAP))),
        ("dep", _n(float(_L_DEP))), ("slab", _n(float(_L_SLAB))),
        # ④：通道半宽 + 全双工重叠区 + 半双工切换闸（后两件 3D 过去根本没画）
        ("chw", _n(_P3CHW)), ("lap", _arr(_P3LAP)), ("gate", _rows(_P3GATESEG)),
    ])
    # ⑩ P6 实时语音链路
    c = _obj([
        ("st", _rows(_P6ST)), ("rings", _rows(_P6RING)), ("link", _rows(_P6LINK)),
        ("bands", _rows(_P6BAND)), ("bandZ", "22"), ("bandW", "5"),
        ("fork", _arr(_P6FORK)), ("dh", _arr(_P6DH)), ("forkZ", "96"),
        ("flow", _arr(_P6FLOW)),
        ("x0", _n(float(_P6X0))), ("x1", _n(float(_P6X1))), ("ly", "185"),
        ("span", "[70,1610,400]"),
        # ⚠ P6 的 figure 里有两道 translate（盒链 −46 / 增量流带 −34，见 _pipe_fig 末行）：
        #   上面这些坐标是**页上写的原值**，3D 必须把同一道平移补上，否则整组低 46px、
        #   页上的字就全掉到盒外（本轮实拍实锤）。改那两个 translate 必须同步改这两行。
        ("dyA", "-46"), ("dyB", "-34"),
        ("zNear", _n(float(_C_ZNEAR))), ("zDeep", _n(float(_C_ZDEEP))),
        ("dz", "40"), ("beat", "3.4"),
        # ── 二轮精修 · 波A：主路 12 枚球（296px/s）→ **横贯全链一条流** ──────
        #   终审：「P6 数据点不足以表达媒体流。」链路上跑的是音频，音频一直在来 ⇒
        #   它是介质，必须是一条带子。「进站收窄、出站展开」不再是特效，
        #   是一条 gain 回调的自然结果（零分支）。
        ("seg", _rows(_P6SEG)), ("segNm", _sarr(_P6SEGNM)), ("tok", str(_P6TOKEN)),
        ("spd", _arr([sp for _nm, _L, sp in _spd_rows(6)])),
        ("hwMain", _n(15.0)), ("hwSeg", _arr([9.0, 8.0, 8.0, 10.0])),
        ("pulse", _n(_C_PULSE)), ("pulseN", str(_C_PULSEN)),
        ("bedOp", _n(0.34)),
    ])
    # ⑪ P8 打断时序
    u = _obj([
        ("in", _n(float(_P9IN))), ("cut", _n(float(_P9CUT))),
        ("yA", "120"), ("yB", "270"),
        ("tx0", _n(float(_U_TX0))), ("tx1", _n(float(_U_TX1))),
        ("zA", _n(float(_U_ZA))), ("zB", _n(float(_U_ZB))),
        ("zGhost", _n(float(_U_ZGH))), ("zBack", _n(float(_U_ZBK))),
        ("gy0", "74"), ("gy1", "320"), ("dur", "2.4"),
        # ── 二轮精修 · 波A：逐柱采样包络（_P9HS + 线性插值）→ **解析包络** ──────
        #   旧版每根柱的边界都是一处斜率突变 —— 那就是「像锯齿」的病根本人。
        #   让位窗口同时从 1040→1100 的 60px 断崖，挪到页上「收声」那段括号
        #   （840→1040，200px）：塌陷的语义位置该由页上的相位括号决定。
        ("duck", _arr([_U_DUCK0, _P9CUT])),
        # 基准半宽 34 ≈ 页上波形柱的最高半高（_P9HS 最大 64 ⇒ 32）——
        # poster 交给 canvas 的那一瞬间，带子的包络高度与柱子的天际线是同一档。
        ("spd", _arr(_SPD_P8)), ("hw", _arr([34.0, 34.0])),
    ])
    # ⑫ P10 产品大图（分层深度化 · 相机不动）
    m = _obj([
        ("box", _rows(_P10BOX)), ("ring", _rows(_P10RING)),
        ("lane", _rows(_P10LANE)), ("beam", _rows(_P10BEAM)),
        ("zl", _arr(_M_ZL)), ("lop", _arr(_M_LOP)),
        ("dz", _n(float(_M_DZ))), ("beat", _n(_M_BEAT)),
        # 波B 轻手术：介质名册（下标）+ 流带半宽 + 逐股波峰速度
        ("medL", _arr(_M_MEDL)), ("medB", _arr(_M_MEDB)),
        ("floww", _n(_M_FLOWW)), ("spd", _arr(_SPD_P10)),
    ])
    # ⑬ P11 弱网 AI QoS（囤着播）
    q = _obj([
        ("heap", '"%s"' % _poly(_P11HEAPTOP)), ("bin", _arr(_P11BIN)),
        ("wave", '"%s"' % _poly(_P11WAVE, per=10, tol=1.0)),
        ("hx0", _n(float(_Q_HX0))), ("hx1", _n(float(_Q_HX1))), ("hbot", _n(float(_Q_HBOT))),
        ("hz", _n(float(_Q_HZ))), ("hn", str(_Q_HN)),
        ("dark", _arr(_WN_DARK)), ("rain", _arr(_Q_RAIN)),
        ("ry0", _n(float(_Q_RY0))), ("rdur", _n(_Q_RDUR)),
        ("wy", _n(float(_Q_WY))), ("wz", _n(float(_Q_WZ))), ("ww", _n(float(_Q_WW))),
        ("odur", _n(_Q_ODUR)), ("outn", str(_Q_OUTN)),
        ("bar", _rows(_P11BAR)), ("by", _n(float(_P11BY))), ("bw", _n(float(_P11BW))),
        ("bh", _n(float(_P11BH))), ("bz", _n(float(_Q_BZ))), ("bdz", _n(float(_Q_BDZ))),
        ("dom", _rows(_P11DOM)), ("domz", _n(float(_Q_DOMZ))),
        ("mech", _rows(_P11MECH)), ("mz", _n(float(_Q_MZ))),
    ])
    # ⑭ P12 视觉模态（相机视锥）
    w = _obj([
        ("box", _rows(_P12BOX)), ("weak", _rows(_P12WEAK)), ("wline", _rows(_P12WLINE)),
        ("run", _rows(_P12RUN)), ("apex", _arr(_W_APEX)), ("mouth", _arr(_W_MOUTH)),
        ("hub", _arr(_P12BOX[0][:4])),
        ("zApex", _n(float(_W_ZAPEX))), ("zMouth", _n(float(_W_ZMOUTH))),
        ("zHub", _n(float(_W_ZHUB))), ("zWeak", _n(float(_W_ZWEAK))),
        # 波A：画面平面的周期由「锥口 → 中枢的距离 ÷ 目标流速」反推（旧 77.5px/s）
        ("dz", "30"), ("beat", "3.4"),
        ("pdur", _n(_dur_at(_spd_rows(12)[0][1], _spd_rows(12)[0][2]))),
    ])
    # ⑮ P13 编排中枢机（波B · 王冠二）
    _fl = _plen(_P13FLOW)
    _gz = [g for g in (_box_u(_P13FLOW, b) for b in _P13GHOST) if g]
    k = _obj([
        ("slot", _rows(_P13SLOT)), ("hub", _arr(_P13HUB)),
        ("bus", _rows(_P13BUS)), ("run", _rows(_P13RUN)),
        ("zSlot", _n(float(_K_ZSLOT))), ("zPlate", _n(float(_K_ZSLOT))),
        ("zHub", _n(float(_K_ZHUB))), ("zBus", _n(float(_K_ZBUS))),
        ("cav", _n(float(_K_CAV))), ("dz", "34"), ("pad", "14"), ("pad2", "12"),
        ("cyc", _n(_K_CYC)), ("sw", _n(_K_SW)), ("beat", "3.6"),
        ("pill", _arr(_P13PILL)), ("brk", _rows(_P13BRK)),
        # 机腔 / 内肋 / 呼吸转子 / 发布脉冲
        ("hubCav", _n(_K_HUBCAV)), ("rib", str(_K_RIB)),
        ("coreN", str(_K_CORE_N)), ("pub", _n(_K_PUB)),
        ("pubPath", _rows(_P13PUB)),
        # 转子：三枚轨道环 (ax,ay,az) + 呼吸幅度 + 翻滚周期 + 光弧角速度 + 墨迹盒与净空
        ("orb", _rows(_K_ORB)), ("orbBr", _n(_K_ORB_BR)),
        ("orbRoll", _arr(_K_ORB_ROLL)), ("orbArc", _arr(_K_ORB_ARC)),
        ("ink", _rows(_P13INK)), ("clr", _n(_K_CLR)),
        # 贯通流：折线 + ghost 窗口（弧长区间，px）+ 渐隐半宽 + 波峰速度
        ("flow", _rows(_P13FLOW)), ("flowLen", _n(_fl)),
        ("gz", _rows(_gz)), ("gzF", _n(_K_GZF)), ("flowSpd", _n(_SPD_P13)),
        # 本页覆写的幅度档（lab-kit ⑨ 的 _AS_* 全局常量一个没动）
        ("flowW", _n(_K_FLOWW)), ("flowFloor", _n(_K_FLOWFLOOR)),
        ("flowGhost", _n(_K_FLOWGHOST)), ("flowLam", _f1(_k_flow_lam())),
        ("flowEdge", "%.5f" % _k_flow_edge()),
        # 两条往返闭环（分居总线 ±8px）
        ("loop", "[" + ",".join(_rows(lp2) for lp2 in _P13LOOP) + "]"),
        ("busx", str(_K_BUSX)), ("loopOff", _n(_K_LOOP_OFF)),
        # 热切换：真 position.z 位移 + 一进一出错峰
        ("swz", _n(_K_SWZ)), ("swA", _arr(_K_SWA)), ("swB", _arr(_K_SWB)),
    ])
    # ⑯ P14 接入架构三塔握手
    y = _obj([
        ("tower", _rows(_P14T)), ("inner", _rows(_P14IN)),
        ("arc", "[" + ",".join('["%s",%d,%d,%d]' % (_poly(a[0]), a[1], a[2], a[3])
                               for a in _P14ARC) + "]"),
        ("z", _arr(_Y_Z)), ("lift", "8"), ("dz", "46"), ("dz2", "18"),
        ("cyc", _n(_Y_CYC)), ("rest", _n(_Y_REST)), ("beat", "3.6"),
        # ── 二轮精修 · 波A：三个点 → 光束生长（B 档 · 离散事件才许光束）────────
        #   注光 400px/s；三段路由长逐条 = 页上那三条路由本人；
        #   生长 6.24s → 全亮停驻 2.00s → 收 1.00s = 一轮 9.24s（qa 三段等速复算）。
        ("beam", _n(_Y_BEAM)), ("route", _arr([_plen_d(a[0]) for a in _P14ARC])),
        ("grow", _n(_Y_GROW)), ("hold", _n(_Y_HOLD)), ("rel", _n(_Y_REL)),
        ("feather", _n(26.0)),
        # 楼层灯瀑：贴塔**右内缘**的一列灯（不横穿塔身、不压任何一行字）
        ("fl", _n(float(_Y_FLOOR))), ("fln", str(_Y_FLOORN)), ("fld", _n(_Y_FLOORD)),
    ])
    # ═══ ⑥ 互动星系 + 三轮「静态页升维」· 三枚加法层的常量 ═══════════════
    #   K 键 ↔ CSS 前缀：gx ↔ --gx-（P22 galaxy）· x ↔ --x-（P5 three）
    #                    hb ↔ --h-（P15 hub）· nb ↔ --n-（P16 calls）
    #   （K.h 会与舞台高 K.H 只差大小写，读代码时容易看错 ⇒ 用 hb / nb）
    # ⑥ 互动星系（P22）：K 表条目由 `gx_kobj` 一次算出（半径 / 厚度 / rim / outr /
    #   抬升 / 深度雾半程 / 流的局部串全部按 s 缩放；带宽 / 点径 / 流速 / λ 不缩放）。
    #   makeGalaxy 只读这张表 ⇒ 它天然尺度无关，lab / info 共用同一份 JS。
    gx = gx_kobj(GX22["cx"], GX22["cy"], GX22["s"], GX22["rect"][2], GX22["rect"][3],
                 "[" + ",".join(_arr(b) for b in _P22INK) + "]")
    x5 = _obj([
        # ⑤：三条支流 + 一条集流带的中心线（页坐标 · 已重采样成等弧长点）
        ("s", "[" + ",".join('"%s"' % _pk(_lerp_poly(q, m2)) for q, m2 in
                             [(_x5_drop(k), 24) for k in range(3)]
                             + [(_X5COL, 92)]) + "]"),
        ("sz", _arr([14, 14, 14, 0])),                     # 支流稍近一档 ⇒ 「垂下来」是往前垂
        ("spd", _arr(_SPD_P5)), ("lam", _n(_X5LAM)), ("w", _n(_X5W)),
        # 集流带的半宽剖面：每过一处汇入点涨一档（3.0 → 8.2）
        ("join", _arr(_X5JOIN)), ("cw", _arr([_X5CW0, _X5CW1])), ("jw", _n(46.0)),
        ("arr", _arr([_X5COLX[1], _X5COLY, _X5ARR])),
        ("haze", _arr(_X5HAZE)), ("hazen", str(_X5HAZEN)),
        ("ink", "[" + ",".join(_arr(b) for b in _X5INK) + "]"), ("clr", _n(_ADD_CLR)),
        ("D", _n(1400.0)), ("half", _n(190.0)),
    ])
    h15 = _obj([
        ("core", _arr([_H15CORE[0], _H15CORE[1], _H15CR])), ("cz", _n(_H15CZ)),
        ("cl", "[" + ",".join(_arr(c) for c in _H15CL) + "]"),
        ("box", _arr([_H15CLW, _H15CLH])),
        ("s", "[" + ",".join('"%s"' % _pk(_lerp_poly(_h15_spoke(k), 40))
                             for k in range(6)) + "]"),
        ("spd", _arr(_SPD_P15)), ("lam", _n(_H15LAM)), ("w", _n(_H15W)),
        # ⑦ 迷你转子：三枚**显式倾角**的环 (rx, r2, tilt°) + 摆幅 + 可见的核
        ("orb", _rows(_H15ORB)), ("orbBr", _n(_K_ORB_BR)),
        ("orbRoll", _arr(_K_ORB_ROLL)), ("orbArc", _arr(_K_ORB_ARC)),
        ("orbAmp", _n(_H15ORBAMP)), ("corer", _n(_H15CORER)),
        ("orbN", str(_H15ORBN)), ("w01", _arr([_H15W0, _H15W1])),
        ("ink", "[" + ",".join(_arr(b) for b in _H15INK) + "]"), ("clr", _n(_ADD_CLR)),
        ("D", _n(_H15D)), ("half", _n(300.0)),
    ])
    n16 = _obj([
        # ⑥：八条水平直带 —— 点在 JS 里按 4px 一段现铺（直线不必打包成折线串）
        ("y", _arr([_n16_y(k) for k in range(_N16N)])),
        ("x", _arr([_N16X0, _N16X1])), ("n", str(_N16N)),
        ("sz", _arr([-8 - 7 * k for k in range(_N16N)])),
        ("call", _rows(_N16CALL)), ("ce", _n(_N16CE)),
        ("spd", _arr(_SPD_P16)), ("lam", _n(_N16LAM)), ("w", _n(_N16W)),
        ("ink", "[" + ",".join(_arr(b) for b in _N16INK) + "]"), ("clr", _n(_ADD_CLR)),
        ("D", _n(1400.0)), ("half", _n(220.0)),
    ])
    return "{" + ",".join([
        "W:%d" % LW, "H:%d" % LH, "FPX:%s" % _n(FPX), 'rev:"%s"' % THREE_REV,
        "v:{" + ",".join([
            "cam:" + _arr(VCAM.C),
            "tilt:%s" % _n(VTILT), "spin:%s" % _n(VSPIN), "n:%d" % VN,
            "amp:%s" % _n(VAMP), "w0:%s" % _n(VW0),
            "ha:" + _arr([h[0] for h in VHARM]),
            "hw:" + _arr([h[1] for h in VHARM]),
            "hk:" + _arr([h[2] for h in VHARM]),
            "hp:" + _arr([h[3] for h in VHARM]),
            "hot:" + _arr(VHOT), "introSec:%s" % _n(VINTRO),
        ]) + "}",
        "g:{" + ",".join([
            "cam:" + _arr(GCAM.C),
            "tilt:%s" % _n(GTILT), "y0:%s" % _n(GY0), "spin:%s" % _n(GSPIN),
            "introSec:%s" % _n(GINTRO),
        ]) + "}",
        # lab-kit ⑨ · audioStream 参数表（全 deck 共用一份 —— 一处改，所有流一起动）
        "as:" + _obj([
            ("a", _arr(_AS_A)), ("f", _arr(_AS_F)), ("ph", _arr(_AS_PH)),
            ("lam", _n(_AS_LAM)), ("floor", _n(_AS_FLOOR)), ("ghost", _n(_AS_GHOST)),
            ("grain", _n(_AS_GRAIN)), ("grainL", _n(_AS_GRAINL)),
            ("edge", _n(_AS_EDGE)), ("crest", _n(_AS_CREST)), ("comp", _n(_AS_COMP)),
            ("spd", _n(_SPD_A)),
        ]),
        "b:" + b, "s:" + s, "r:" + r, "t:" + t, "d:" + d,
        # 第二波九枚（终波）
        "o:" + o, "l:" + l, "c:" + c, "u:" + u, "m:" + m,
        "q:" + q, "w:" + w, "k:" + k, "y:" + y,
        # ⑥ 互动星系（P22 · 在页 3D）+ 三轮的三枚加法层
        "gx:" + gx, "x:" + x5, "hb:" + h15, "nb:" + n16,
        'landBits:"%s"' % LAND_BITS, "landN:%d" % LAND_N,
        'nodeTable:"%s"' % NODE_TABLE, 'routeTable:"%s"' % ROUTE_TABLE,
        "arcDur:%s" % ARC_DUR_S, "arcGap:%s" % ARC_GAP_S, "arcOff:%s" % ARC_OFF_S,
    ]) + "}"


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
       # LAB 演绎的唯一一处正文改动：kicker 末段挂上家族名。
       # 主标 / 副题 / accent 短棒 / 页脚 mono 行一个像素不碰 —— 右边那颗球
       # 是加在**留白**上的，不是从字里挤出来的（构图账见 LAB 块的 VGR/VCX/VCY）。
       "AGORA · CONVERSATIONAL AI ENGINE · DEEP DIVE · 深入讲解 · LAB"),
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
]), lab="voice")

# ═══ P2 · 模态转换剧场 ·「对话是一个实时决策的过程」════════════════════════
#   2026-08-20 三轮「图形升维」：4 卡 + 弱双轨 → 一张「决策环」。
#   2026-09-01 二轮精修 · 波B（王冠一）：决策环 → **模态转换剧场**。
#   Colin 亲自给的方向：「我们本质在构建的是拆解对话的本质 —— 听、想、说是第一性
#   原理出发的对话本质，拆解人类在这个过程如何做模态转换。从你的高维去拆解这个理念，
#   不用惧怕人类看不懂，很多情况下我们可以意会，不用拘泥于人类社会的维度来解释对话。」
#   ⇒ 不画「四步接成一个环」（那是流程图语域），画**同一段东西换了三次形态**。
#   三态的定义、周期、相位、生灭窗全部写在文件上方的 _MO_* 常量块里（那是唯一真相，
#   poster 与顶点着色器同吃）。
#
#   ── 版式：**第五处许可分歧**（四卡四角 → 底排四栏）────────────────────────
#   环没了，四张卡就没有「四角」这个位置理由了。改成底排四栏：舞台整幅让给剧场，
#   四栏在底下当**图注**（听 / 理解 / 判断 / 表达 —— 读者一眼知道台上正在演谁）。
#   **文案一个字没改**（_MOVES4 逐字沿用），**发射顺序与母本逐件对齐**
#   （四栏 → 三处接口注 → 弧注两行 → 环心注两行 → 图例），所以「逐字同文 + step
#   集合同源」两道同源闸照绿；分歧只在坐标，登记在 _DIVERGE 的第五行。
#   hot 件仍唯一 = 「判断」那一栏（高一档 + accent 描边 + halo）：全页的因在这里。
_MOVES4 = [   # (台上动作, 序号, 原卡标题, 原卡正文) —— 标题与正文与旧版一字不差
    ("听",   "01", "听清 · 认人 · 懂内容",       "分离目标人声、识别说话人，同时理解在说什么"),
    ("理解", "02", "带入对象、场景与情绪",       "结合上下文理解言外之意，而不只是逐字转写"),
    ("判断", "03", "持续判断：继续听，还是开口", "实时权衡时机，不必等一句话彻底说完"),
    ("表达 · 控制节奏", "04", "边说边听，灵活调整节奏", "表达的同时仍在倾听，随时被打断、随时接上"),
]
# 底排四栏（等宽 396 · 栏距 32 ⇒ 4×396 + 3×32 = 1680 正好铺满版心）；
# 判断那一栏高一档（顶沿上抬 16px），是全页唯一一处「冒头」—— 因在这里。
_P2N = [(0, 338, 396, 126), (428, 338, 396, 126), (856, 322, 396, 142), (1284, 338, 396, 126)]
# ── 第二道入射波的入场弧（本页灵魂：「表达时仍在听」）──────────────────────
#   母本里它是「表达 → 听清」的点线反馈弧。剧场版里它是**同一件事的高维说法**：
#   台上这一代还在「说」，下一代的入射波已经沿这条弧切进来了 —— 3D 里它是一条真的
#   audioStream（lab-kit ⑨），到达舞台左缘的那一刻触发格架让位（_MO_YAW）。
#   坐标随版式分歧一起重锚（母本那串锚在四角卡上，四角没了它就无处可锚）。
_P2ARC = "M300 264 C 208 264, 160 238, 160 158 C 160 78, 208 54, 296 54"


# ── 模态转换剧场的**构建期几何**：poster 与顶点着色器同参 ────────────────────
#   waveAt / latAt 在这里是 Python、在 MO_HEAD 里是 GLSL，两处逐行同式，
#   参数**只有 _MO_* 一份**（运行时经 K.o 拿到同一批数）。
#   poster 取 t* = 12.0：那一刻第 0 代在「说」（出射波场，正倾泻出画）、
#   第 1 代在「想」（表征星格已完全成形）—— 一张静帧里同时有波与格，
#   而且正是页上「同一时刻 · 并行进行」那句话的图。
_MO_POSTER_T = 12.0


def _mo_S(th):
    """四枚谐波叠加的**零均值**版（= 2·(envAt−0.5)）—— 与 lab-kit ⑨ 同一组权重/频率/起相位"""
    return sum(_AS_A[k] * math.sin(_AS_F[k] * th + _AS_PH[k]) for k in range(4))


def _mo_wave(u, v, w, run, out):
    """入射 / 出射声波场：**等相位线竖直**的行波 —— 相位只由 x 决定。
       波长逐字取 _AS_LAM（232px）⇒ 与 lab-kit ⑨ 那条流是同一种介质。"""
    span = _MO_X1 - _MO_X0
    x = _MO_X0 + out * _MO_OUTDX + span * u
    ny = (v - 0.5) * 2.0
    nz = (w - 0.5) * 2.0
    amp = _MO_AMP * (1.0 - 0.62 * abs(ny))
    y = _MO_YC + ny * _MO_HW + amp * _mo_S(2.0 * math.pi * (x - run) / _AS_LAM)
    return (x, y, nz * _MO_DZ * 0.5)


def _mo_lat(u, v, w, t, yaw):
    """表征星格：34×12×5 点阵被**两道折叠函数**揉成一片流形 +
       一道从中心往外传的**位移**涟漪（理解是几何变换，不是黑盒）。"""
    p = (u - 0.5) * _MO_LW
    q = (v - 0.5) * _MO_LH
    r = (w - 0.5) * _MO_LD
    TAU = 2.0 * math.pi
    # 折叠 ①：沿 q 的正弦褶（把平面揉出一道纵向波纹，深度层各错开一点）
    X = p + _MO_F1 * _MO_LW * 0.5 * math.sin(TAU * (q / _MO_LH) + r * 0.012)
    # 折叠 ②：沿 p 的正弦褶 —— 两道折叠方向正交，交出来的才是「流形」不是「波纹纸」
    Y = q + _MO_F2 * _MO_LH * 0.5 * math.sin(TAU * 1.5 * (p / _MO_LW))
    Z = r + _MO_FB * math.cos(TAU * (p / _MO_LW + q / _MO_LH))
    d = math.hypot(X, Y) + 1e-3
    rp = _MO_RIP * math.sin(TAU * (d / _MO_RLAM - t / _MO_RPER))
    X += rp * X / d
    Y += rp * Y / d
    cs, sn = math.cos(yaw), math.sin(yaw)
    return (_MO_LCX + X * cs + Z * sn, _MO_YC + Y, -X * sn + Z * cs)


def _mo_phase(t):
    """一代在 t 时刻的三态权重 (wIn, wLat, wOut) + 生灭窗 uLife + 让位偏航 uYaw。
       四道相位边界全部走 smootherstep；权重和恒为 1（⑲h 逐点复算）。"""
    ph = _MO_PH
    s1 = _smoother(ph[0], ph[1], t)
    s2 = _smoother(ph[2], ph[3], t)
    lf = _MO_LIFE
    life = _smoother(lf[0], lf[1], t) * (1.0 - _smoother(lf[2], lf[3], t))
    s = t - _MO_YAW[0]
    yaw = (_smoother(0.0, _MO_YAW[1], s)
           * (1.0 - _smoother(_MO_YAW[1], _MO_YAW[1] + _MO_YAW[2], s))) * _MO_YAWA
    return (1.0 - s1, s1 * (1.0 - s2), s1 * s2, life, yaw)


def _mo_at(u, v, w, t, clock):
    """三个解析目标按 (wIn,wLat,wOut) **线性插值** —— 顶点着色器里是同一行。"""
    wi, wl, wo, life, yaw = _mo_phase(t)
    a = _mo_wave(u, v, w, _SPD_P2[0] * clock, 0.0)
    b = _mo_lat(u, v, w, t, yaw)
    c = _mo_wave(u, v, w, _SPD_P2[1] * clock, 1.0)
    return ([a[k] * wi + b[k] * wl + c[k] * wo for k in range(3)], life)


# ── 02「两制对照」的构建期几何（poster 与 3D 同吃这一份）────────────────────
def _p2_win(t, a, b, e):
    """一扇 smootherstep 窗（gain 剖面的唯一构件 —— 运行时 win() 逐行同式）"""
    return _smoother(a - e, a + e, t) * (1.0 - _smoother(b - e, b + e, t))


def _p2_anti_gain(a_t):
    """上排回合制的幅度剖面：听 / 说是实带，其余（含「想」那一段）落 ghost 档。
       **零分支** —— 空档不是「不画」，是同一条流的幅度落到细线（lab-kit ⑨ 的 aG）。"""
    t = a_t / (_P2TX1 - _P2TX0)
    return max(_p2_win(t, _P2SEG[0][0], _P2SEG[0][1], _P2SEGE),
               _p2_win(t, _P2SEG[2][0], _P2SEG[2][1], _P2SEGE))


def _p2_env_path(yc, x0, x1, hw, spd, gainf, n=320):
    """一条水平 audioStream 在 t* 那一帧的**静态包络轮廓**（与 AS_VS 逐行同式）：
       en = .5+.5·Σaᵢsin(2π·fᵢ·(aT−run)/λ+φᵢ)；amp = mix(ghost,1,g)；dyn = mix(1,en,g)；
       半高 = hw·(floor + (1−floor)·dyn)·amp。
       ⚠ 两端那一档 uEdge 在着色器里是**alpha** 渐隐，填充路径表达不了 alpha，
         所以 poster 把它折算到高度上（观感更接近；差别只在 WebGL 起不来时看得到）。"""
    run = spd * _MO_POSTER_T
    top, bot = [], []
    for i in range(n + 1):
        t = i / float(n)
        x = x0 + (x1 - x0) * t
        a_t = x - x0                      # 水平流 ⇒ 沿流弧长 = 横向距离
        en = 0.5 + 0.5 * _mo_S(2.0 * math.pi * (a_t - run) / _AS_LAM)
        g = max(0.0, min(1.0, gainf(a_t)))
        amp = _AS_GHOST + (1.0 - _AS_GHOST) * g
        dyn = 1.0 + (en - 1.0) * g
        h = hw * (_AS_FLOOR + (1.0 - _AS_FLOOR) * dyn) * amp
        h *= _smoothstep(0.0, _AS_EDGE, t) * _smoothstep(0.0, _AS_EDGE, 1.0 - t)
        top.append((x, yc - h))
        bot.append((x, yc + h))
    d = "M" + " L".join("%s %s" % (_f1(p[0]), _f1(p[1])) for p in top)
    d += " L" + " L".join("%s %s" % (_f1(p[0]), _f1(p[1])) for p in reversed(bot)) + "Z"
    return d


def _p2_dash_segs(x0, x1, yc, hh, dash=12.0, gap=9.0):
    """「想」不是媒体（流质铁律）—— 它是一只**虚线框**（沿用旧 _P2ANTI 那枚虚线
       chip 的语义）。虚线段在构建期算成定长表，poster 与 3D 用同一批坐标 ⇒
       破折相位不可能分叉（「构建期算一遍、运行时不再算第二遍」）。"""
    pts = [(x0, yc - hh), (x1, yc - hh), (x1, yc + hh), (x0, yc + hh), (x0, yc - hh)]
    segs, s, per = [], 0.0, dash + gap
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        L = math.hypot(bx - ax, by - ay) or 1.0
        while s < L:
            e = min(L, s + dash)
            if e - s > 0.8:
                segs.append((ax + (bx - ax) * s / L, ay + (by - ay) * s / L,
                             ax + (bx - ax) * e / L, ay + (by - ay) * e / L))
            s += per
        s -= L
    return segs


_P11SRCY = 1044                  # 表达力精进 ③：P11 的 SOURCE 自己占一行（详见页上注）
_P2DASH = _p2_dash_segs(_P2DKX[0], _P2DKX[1], _P2RY, _P2DKH)
_P2EVX = _P2TX0 + (_P2TX1 - _P2TX0) * _P2EVT     # 两排共用的那一刻（局部 x）


def _p2_two_fig():
    """02 · SAME MOMENT「两制对照」的 **poster 层**（3D 起来时整幅让给 canvas）：
       两排带子的静态包络轮廓 + 「想」的虚线框 + 两枚事件竖标 —— 字一个不裹。
       字的 DOM 序与旧 _P2ANTI 逐字相同（回合制 / 听完 / 想 / 说 / 听完再回答 ✕），
       所以 ⑳ 的「正文逐字同源」照旧放行 —— 本轮**一个字没新增**。"""
    o = []
    # ① 上排 · 回合制：一条流（听 / 说实带 + ghost 空档）
    o.append('<path class="p2-anti" d="%s"/>'
             % _p2_env_path(_P2RY, _P2TX0, _P2TX1, _P2RW, _SPD_P2B[0], _p2_anti_gain))
    # ② 「想」的虚线框（不是流）
    o.append('<path class="p2-dash" d="%s"/>'
             % "".join("M%s %sL%s %s" % tuple(_f1(v) for v in s) for s in _P2DASH))
    # ③ 下排 · 边说边听：听 / 想 / 说三条并行连续带（说带在 _P2EVT 处让位再接回）
    for k in range(3):
        x0 = _P2TX0 + ((_P2TX1 - _P2TX0) * _P2SPK if k == 2 else 0.0)
        if k == 2:
            hw = _P2DUCK * 0.5
            c = _P2EVX - x0
            gf = (lambda a_t, c=c, hw=hw:
                  _P2LG[2] * (1.0 - _p2_win(a_t, c - hw, c + hw, hw * 0.30)))
        else:
            gf = (lambda a_t, k=k: _P2LG[k])
        o.append('<path class="p2-live" d="%s"/>'
                 % _p2_env_path(_P2LY[k], x0, _P2TX1, _P2LW[k], _SPD_P2B[1 + k], gf))
    # ④ 两枚事件竖标：同一根竖线上，上排不让位、下排让位（✕ / ✓ 的几何含义）
    o.append('<path class="p2-evt" d="%s"/>'
             % "".join("M%s %sV%s" % (_f1(_P2EVX), _f1(yc - _P2EVH), _f1(yc + _P2EVH))
                       for yc in (_P2RY, _P2LY[2])))
    o.append('<circle class="p2-evt-d" cx="%s" cy="%s" r="4"/>'
             % (_f1(_P2EVX), _f1(_P2RY - _P2EVH)))
    out = [lp(*o)]
    # ── 字（全在 poster 之外，任何降级路径下都压在 canvas 之上）──────────────
    #    顺序与旧 _P2ANTI 逐字相同；样式也照抄（note 语域 = 灰、小一号）。
    _G, _B = "var(--ink-3)", int(_P2LBY)
    out.append(txt(2, int(_P2GY), "回合制", "sm", size=14, col=_G, mono=True, ls=".16em"))
    for k, _s in enumerate(["听完", "想", "说"]):
        _cx = _P2TX0 + (_P2TX1 - _P2TX0) * (_P2SEG[k][0] + _P2SEG[k][1]) / 2.0
        out.append(txt(int(round(_cx)), _B, _s, "sm", size=17, anchor="middle", col=_G))
    out.append(txt(1680, _B, "听完再回答 ✕", "sm", size=17, anchor="end", col=_G))
    # ── 下排的字（表达力精进 · 第二波 0 · 终审补）────────────────────────────
    #   三枚 lane 标与「回合制」同一列、同字号（mono 14 · ls .16em），只把色档
    #   换成 accent —— 于是「灰 = 回合制 / accent = 边说边听」这层对仗在字上也成立；
    #   右端判词与上排的「听完再回答 ✕」同一列右对齐、同字号，落在下排之下。
    #   这四枚字串是 build() 末尾同源自证的**白名单例外**（见那一段的断言）。
    for k, _s in enumerate(["听", "想", "说"]):
        out.append(txt(2, int(_P2LGY[k]), _s, "sm", size=14, col=AC, mono=True, ls=".16em"))
    out.append(txt(1680, int(_P2VY), "边说边听 ✓", "sm", size=17, anchor="end", col=AC))
    return "".join(out)


def _mo_poster():
    """P2 的降级层：把 t* 那一帧**逐点算出来**画成 SVG。
       与 WebGL 同参（同一批 _MO_* 常量、同一组公式、同一套行线/纬筋的抽稀规则）
       ⇒ poster 与 canvas 是同一张图，交接时不会「跳一下」。"""
    NA, NB, NC = _MO_NA, _MO_NB, _MO_NC
    dots = {0: [], 1: []}
    rows = {0: [], 1: []}
    ribs = []

    def P(ia, ib, ic, tg):
        pt, _lf = _mo_at(ia / (NA - 1.0), ib / (NB - 1.0), ic / (NC - 1.0),
                         tg, _MO_POSTER_T)
        return _mo_proj(pt)

    def inside(q):
        """poster 必须裁在舞台矩形里。出射波场的右端**本来就越过右缘**（那是
           「倾泻出画」），canvas 会自己裁掉；SVG 不裁，溢出的那 16px 就成了
           pinned 逐像素比对里唯一一处差异（本轮实拍锤过）。"""
        return 0.0 <= q[0] <= 1680.0 and 0.0 <= q[1] <= 470.0

    for g in (0, 1):
        tg = (_MO_POSTER_T + g * _MO_GEN) % _MO_CYC
        _wi, wl, _wo, life, _yaw = _mo_phase(tg)
        if life < 0.02:
            continue
        for ia in range(0, NA, 2):                     # 点：2×2×2 抽稀（2040 → 255/代）
            for ib in range(0, NB, 2):
                for ic in range(0, NC, 2):
                    s2 = P(ia, ib, ic, tg)
                    if inside(s2):
                        dots[g].append("M%s %sh.01" % (_f1(s2[0]), _f1(s2[1])))
        for ic in range(0, NC, 2):                     # 行线：与运行时 wRow 同一套抽稀
            for ib in range(NB):
                d, pen = "", False
                for ia in range(NA):
                    s2 = P(ia, ib, ic, tg)
                    if not inside(s2):
                        pen = False
                        continue
                    d += ("L" if pen else "M") + _f1(s2[0]) + " " + _f1(s2[1])
                    pen = True
                if d:
                    rows[g].append(d)
        if wl > 0.5:                                   # 纬筋：只有成形的「格」才有
            for ic in range(0, NC, 2):
                for ia in range(0, NA, 4):
                    d, pen = "", False
                    for ib in range(NB):
                        s2 = P(ia, ib, ic, tg)
                        if not inside(s2):
                            pen = False
                            continue
                        d += ("L" if pen else "M") + _f1(s2[0]) + " " + _f1(s2[1])
                        pen = True
                    if d:
                        ribs.append(d)
    return ('<path class="p2-row" d="%s"/><path class="p2-wire" d="%s"/>'
            '<path class="p2-wave" d="%s"/><path class="p2-lat" d="%s"/>'
            % ("".join(rows[0]), "".join(rows[1]) + "".join(ribs),
               "".join(dots[0]), "".join(dots[1])))


def _mo_proj(p):
    """构建期的透视投影：与运行时 camPx(w,h,_MO_D) 逐参同解（近大远小是真的）。"""
    k = _MO_D / (_MO_D - p[2])
    return (840.0 + (p[0] - 840.0) * k, 235.0 + (p[1] - 235.0) * k)


def _theatre_fig():
    o = [lp(_mo_poster())]                    # 剧场的降级层：整幅让给它，字全在外面
    for k, (act, no, ttl, body) in enumerate(_MOVES4):
        x, y, w, h = _P2N[k]
        hot = (k == _O_HOTCOL)
        # 运动原语 ④：全页唯一 hot 件（判断栏）呼吸 + 光晕 —— 「因」在这里一直在跳。
        # ⚠ 四栏的框**不入 poster**：它们是底排图注，3D 起来时也要在（剧场在它们上方）。
        o.append("".join(([halo_rect(x, y, w, h, 10, sc="1.05", op=".3", dur="3.6s")] if hot else [])
                         + [box(x, y, w, h, 10, hot=hot, i=k + 1,
                                cls="mo-breathe" if hot else "", sty="--mo-dur:3.6s" if hot else "")]))
        o.append(txt(x + 26, y + (38 if hot else 34), "%s · %s" % (no, act), "sm",
                     size=14, col=AC, mono=True, ls=".14em"))
        o.append(txt(x + 26, y + (80 if hot else 70), ttl, "ttl",
                     size=25 if hot else 23, col=AC if hot else None))
        o.append(txt(x + 26, y + (118 if hot else 104), body, "sm", size=17 if hot else 16))
    # ── 三处接口注（母本那三条环边的注，按新语义重锚）──────────────────────
    #   ① 升维接口（波 → 格）：入射波场把「对象 · 场景 · 情绪」交给星格
    #   ② 格内：判断在格里发生 —— 「何时开口」指着星格本人
    #   ③ 凝聚接口（格 → 波）：星格塌回波场，「开口表达」倾泻出画
    for _ax, _s in ((615, "对象 · 场景 · 情绪"), (930, "何时开口"), (1290, "开口表达")):
        o.append(lp(vline(_ax, 38, 56, AC, 2, 2)))
        o.append(ah_d(_ax, 68, AC))
        o.append(txt(_ax, 30, _s, "sm", size=16, anchor="middle"))
    # ── 第二道入射波的入场弧（本页灵魂）──────────────────────────────────
    o.append(lp(packet(_P2ARC, 400, seg=26, col=AD, w=9, op=".3", dur="4s", i=5, cls="mo-cycle"),
                dline(_P2ARC, AD, 3, 5, dash="3 8"),
                ah_r(308, 54, AD, 7)))
    o.append(txt(0, 152, "表达时仍在听", "ttl", size=18, col=AD, weight=700))
    o.append(txt(0, 178, "随时被打断、随时接上", "sm", size=15, col=AD))
    # ── 剧场落点句：两代同场（相位差半周期）⇒ 台上永远是「同一时刻」──────────
    o.append(txt(840, 282, "同一时刻 · 并行进行", "ttl", size=20, anchor="middle"))
    o.append(txt(840, 306, "持续在听 · 同时在说", "sm", size=15, anchor="middle", mono=True))
    # ── 图例（只列本页用到的两种线型）──
    o.append(legend(0, 30, [("solid", "主数据流"), ("dot", "参考 / 反馈")]))
    return "".join(o)
# 02「两制对照」（表达力精进 · 第一波 ①）：旧版是一条 900×58 的灰色注脚 chip 条
#   —— 与上面那座剧场不对等，读者眼里 01 是论证、02 是脚注。新版与 01 **同介质**
#   （同一枚 audioStream · λ232 · A 档流速）、**同分量**（整幅 1680×200 两排带子），
#   字一个没新增（回合制 / 听完 / 想 / 说 / 听完再回答 ✕ 全是旧条上的原字）。
page("content", "".join([
    head("REAL-TIME DECISION · 边听边说", "对话，是一个<strong>实时决策</strong>的过程。"),
    lab(120, 236, "01 · FOUR MOVES · 同一时刻发生"),
    figbox(120, 272, 1680, 1680, int(_MO_H0), _theatre_fig(), i=1),
    lab(120, 756, "02 · SAME MOMENT · 边说边听", i=6),
    figbox(120, 780, 1680, 1680, int(_P2AH), _p2_two_fig(), i=7),
    # 收口线留在 850：它同时是「两制」的分界（上排回合制在它之上、下排在它之下），
    # 也照旧压着背景板自带的那条 y847–853 accent 细线（见 _P2AY 那一段的注）。
    rule(850),
    land("自然对话不是“听完再回答”，而是边说边听、持续判断——这正是引擎要还原的能力。"),
]), lab="morph")

# ═══ P3 · 双工三模式 ·「一次对话，线路先分三种」════════════════════════════
#   01 三列等宽卡（120 / 700 / 1280 · w520 —— 与 P5「三件极致」同一栅格）：
#      英文小标 + 模式名 + 极简时序小图 + 机理一句 + 实例一句（末列 .card-c.on = 引擎所在）
#   02 table.mini 两行差异（话轮归属 / 能否插话），末列走 accent
_P3LX, _P3RX, _P3CW = 44, 268, 148   # A 列 x / B 列 x / 列宽；列间 76 的空档正好放「切换」二字
_P3CT, _P3CB = 30, 134               # 时间区间（上 / 下）
# ── 三种模式的通道相位表（2026-08-31 第二波：3D 通道与页上的 .mo-packet 逐参同源）──
#   (通道 y, 方向 +1 = A→B / −1 = B→A, 周期 s, 起相位 s, 空挡 ln, 段长 L, 活 = 有没有包)
#   半双工那两行的 (ln=196, L=56, dur=3.3, off=0 / −1.65) 就是页上 pk() 的实参本人：
#   占空比 = (L + seg)/(seg + ln) = (56+14)/(14+196) = 1/3，相位差 = 半周期 ⇒ 严格互斥。
_P3CH = {
    "simplex": [(62, 1, 0.9, 0.0, 56, 56, 1), (102, -1, 0.0, 0.0, 0, 56, 0)],
    # ④：两轮各 44 高（30–74 / 90–134）⇒ 通道跟着挪进各自那一轮的正中
    "half":    [(48, 1, 3.3, 0.0, 196, 56, 1), (116, -1, 3.3, -1.65, 196, 56, 1)],
    "full":    [(74, -1, 0.82, 0.0, 50, 50, 1), (96, 1, 0.9, 0.0, 56, 56, 1)],
}
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
    LX, RX, CW, CT, CB = _P3LX, _P3RX, _P3CW, _P3CT, _P3CB
    # ── 方向通道件（三种模式共用同一套语法，只有「谁活、什么时候活」不同）──
    #   ④：通道从 2.5px 的线加粗成半宽 _P3CHW 的**带**（页上与 3D 同一档）——
    #   「通道」得看得见宽度才是通道；箭头也跟着放大一档。
    _CW2 = _P3CHW * 2
    def ch_r(y, i=3):                       # A → B 活通道：实线 accent + 右箭头
        return hline(194, 250, y, AC, _CW2, i) + ah_r(266, y, AC, 9)
    def ch_l(y, i=3):                       # B → A 活通道：实线 accent + 左箭头
        return hline(266, 210, y, AC, _CW2, i) + ah_l(194, y, AC, 9)
    def ch_dead(y, i=3):                    # 静默通道：压暗虚线 + 灰箭头 —— 线在，包永远不来
        return (dline("M266 %d H206" % y, HS, _CW2, i, dash="7 7", sty="opacity:.42")
                + ah_l(194, y, "var(--ink-3)", 9))
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
        o += [lp(band(LX, CT, CB - CT, True, 1), band(RX, CT, CB - CT, False, 2),
                 ch_r(62), pk(194, 250, 62, 56, "0.9s", "duplex-simplex"),
                 ch_dead(102))]
    elif mode == "half":
        # ④：两个轮次各 **44** 高（旧版三轮 × 24 —— 块太薄，3 米外读不出「谁在说」）：
        #    30–74（A 说） / 闸 82 / 90–134（B 说）。一次完整的轮换就是半双工的定义。
        o += [lp(band(LX, 30, 44, True, 1), band(RX, 30, 44, False, 2),
                 band(LX, 90, 44, False, 3), band(RX, 90, 44, True, 3),
                 # 切换闸：轮次之间必须先让线，才轮到对方（两列之间断开，让出闸名）
                 dline("M%d 82 H%d" % (LX, LX + CW), HS, 2.4, 2, dash="5 5"),
                 dline("M%d 82 H%d" % (RX, RX + CW), HS, 2.4, 2, dash="5 5")),
              txt(230, 87, "切换", "sm", size=14, anchor="middle", col="var(--ink-3)"),
              # 冲突瞬间：A 讲话中途 B 想出声 —— 被闸拦住（明亮一档，它是这一格的论点）
              txt(RX + CW // 2, 61, "✕", "ttl", size=26, anchor="middle", col=AD),
              # ── 严格互斥的两枚包：轮次 1（A 说 · y30–54）走上通道，轮次 2（B 说 · y70–94）
              #    走下通道。占空比 1/3 + 半周期相位差 ⇒ 两段在途区间必不相交
              #    （相位错了等于把半双工讲成全双工，qa-motion 用参数静态复算钉死这一条；
              #    第二波起 3D 通道用同一张 _P3CH 相位表复算，两条路一处真相）。
              lp(ch_r(48), pk(194, 250, 48, 196, "3.3s", "duplex-half"),
                 ch_l(116), pk(266, 210, 116, 196, "3.3s", "duplex-half", delay="-1.65s"))]
    else:
        # A 30–102 / B 62–134：重叠区间 62–102 横贯两列高亮 = 同一时刻两边都在说
        o += [lp('<rect class="pop" style="--i:2;fill:%s;opacity:.19" x="%d" y="%d" width="%d" '
                 'height="%d" rx="5"/>' % ((AD,) + _P3LAP),
                 band(LX, 30, 72, True, 1), band(RX, 62, 72, True, 2),
                 # 插话瞬间：粗 accent-deep 快路径（与 P8 / P9 同 idiom）—— 从 B 横插进 A
                 hline(264, 214, 74, AD, _CW2, 3), ah_l(196, 74, AD, 9),
                 # ── 两个方向同时在途（占空比各 100%，永远同框）：
                 #    B→A 的包直接跑在既有的快路径上（accent-deep，与那支箭头同色同向），
                 #    A→B 另开一条通道落在 y96 —— 仍在重叠区 62–102 之内，且与快路径
                 #    （线宽 5 ⇒ y71.5–76.5）之间留 12px，两枚包（w10 ⇒ ±5）互不相碰。
                 pk(264, 214, 74, 50, "0.82s", "duplex-full", col=AD),
                 ch_r(96), pk(194, 250, 96, 56, "0.9s", "duplex-full"))]
    # 无字刻度的时间轴（竖直向下）
    o.append(lp(vline(14, CT, 122, HS, 1.4, 5),
                ah_d(14, CB, "var(--ink-3)", 7),
                *[hline(9, 19, ty, HS, 1.4, 5) for ty in (CT, CT + 26, CT + 52, CT + 78, 122)]))
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
    # p3-win：3D 起来时在卡背景上开一扇窗（见 LAB_CSS 的 .p3-win 段）——
    # 本 deck 唯一一页「图形区坐在卡里」的 3D 页，卡底 72% 不透明会把 canvas 压成鬼影。
    sh("rise card-c p3-win%s" % (" on" if _on else ""),
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
]), lab="lanes")

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
        # 三条活动带的**几何**入 poster 层（3D 起来时让位给两条对向声带）；
        # 带上的字（用户插话 / 每格一次… / 收声让位）留在外面，压在 canvas 之上。
        if i == 0:      # 听：永不中断的输入波形；_XIN 之后是新出现的用户语音（加重）
            # 运动原语 ①：波形带底下压一列能量包，横贯全程 —— 「听的车道永不关闭」
            o.append(lp(
                packet("M162 %d H1636" % (by + bh // 2), 420, seg=26, w=13, op=".22", dur="2.4s", i=1),
                _bars(162, 54, by + bh // 2, "var(--ink-3)", seed=2, gap=17, w=7, op=".42"),
                _bars(1084, 23, by + bh // 2, AC, seed=6, gap=17, w=8),
                _bars(1480, 9, by + bh // 2, "var(--ink-3)", seed=13, gap=17, w=7, op=".42")))
            o.append(txt(1084, by - 12, "用户插话", "sm", size=15, col=AC, mono=True))
        elif i == 1:    # 想：等距判定刻度，_XIN 那一格是「让位」的那次判断（实心）
            _g = [hline(160, 1636, by + bh // 2, HS, 1.4, 3)]
            for k in range(27):
                x = 160 + k * 56
                hot = abs(x - _XIN) < 28
                _g.append(vline(x, by + 4, by + bh - 4, AD if hot else HS, 3 if hot else 1.4, 3))
            o.append(lp(*_g))
            o.append(txt(1636, by - 12, "每格一次「要不要出声」", "sm", size=15, anchor="end"))
        else:           # 说：TTS 输出块 —— 第二块在 _XIN 被截断，其后让位（空带）
            _g = []
            for bx, bw in [(160, 452), (700, _XIN - 700)]:
                _g.append('<rect class="pop" style="--i:4;fill:%s" x="%d" y="%d" width="%d" '
                          'height="%d" rx="5"/>' % (AC, bx, by, bw, bh))
            _g.append(vline(_XIN, by - 6, by + bh + 6, AD, 4, 5))
            _g.append('<rect class="pop" style="--i:5" x="%d" y="%d" width="%d" height="%d" rx="5" '
                      'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 6"/>'
                      % (_XIN + 10, by, 1626 - _XIN, bh, HS))
            o.append(lp(*_g))
            o.append(txt(_XIN + 22, by - 12, "收声让位", "sm", size=15, col=AD, mono=True))
    # ── 快路径：听见插话 → 判断让位 → 收声，一根 accent-deep 粗线贯穿三带（P8 idiom）──
    o.append(lp(
        vline(_XIN, 106, 268, AD, 5, 6),
        # 运动原语 ③（轻）：快路径节点脉冲 —— 「340ms 那一下」在跳，但不抢波形
        '<circle class="pop mo-pulse" style="--i:6;--mo-lo:.45;--mo-dur:2.8s;fill:%s" '
        'cx="%d" cy="190" r="8"/>' % (AD, _XIN),
        ah_d(_XIN, 280, AD, 8)))
    o.append(txt(_XIN + 20, 248, "340ms", "ttl", size=20, col=AD, weight=700))
    # ── NOW 播放头：一条竖虚线穿过三条活动带 —— 「同一瞬间」三件事都在跑 ──
    # 运动原语 ②：NOW 播放头的 dash 缓慢下爬（刻度不动、播放头在读）
    o.append(lp(dline("M%d 50 V336" % _XNOW, AC, 1.6, 7, dash="4 8", cls="mo-drift",
                      sty="--mo-off:-24;--mo-dur:1.8s")))
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
]), lab="duplex")

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
]), lab="three")

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
    # 圆圈是「形」（3D 里换成两枚空间环）；圆里那两枚象形图标等同标签，留在 canvas 之上。
    o.append(lp('<circle class="pop box" style="--i:0" cx="70" cy="185" r="44" stroke-width="1.4"/>'))
    o.append('<path class="pop" style="--i:0" d="M70 165a10 10 0 0 1 10 10v10a10 10 0 0 1-20 0v-10a10 10 0 0 1 10-10z '
             'M56 183a14 14 0 0 0 28 0 M70 197v9" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % AC)
    o.append(txt(70, 288, "人声输入", "ttl", size=20, anchor="middle"))
    o.append(lp('<circle class="pop box" style="--i:6" cx="1610" cy="185" r="44" stroke-width="1.4"/>'))
    o.append('<path class="pop" style="--i:6" d="M1600 173h-10v24h10l16 13V160z M1624 176a10 10 0 0 1 0 18 '
             'M1631 169a18 18 0 0 1 0 32" fill="none" stroke="%s" stroke-width="2.4" '
             'stroke-linecap="round" stroke-linejoin="round"/>' % AC)
    o.append(txt(1610, 288, "语音输出", "ttl", size=20, anchor="middle"))
    # 四个串行环节
    for i, (n, sub, foot, hot) in enumerate(_PIPE):
        x = _PIPE_X[i]
        cx = x + 110
        # 运动原语 ④：本页唯一 hot 件（AI-VAD）呼吸 + 光晕
        o.append(lp(*(([halo_rect(x, 120, 220, 130, 6, sc="1.07", op=".3", dur="3.4s")] if hot else [])
                      + [box(x, 120, 220, 130, 6, hot=hot, i=i + 1,
                             cls="mo-breathe" if hot else "", sty="--mo-dur:3.4s" if hot else "")])))
        o.append(txt(cx, 178, n, "ttl", size=26, anchor="middle",
                     col=AC if hot else None))
        o.append(txt(cx, 214, sub, "sm", size=17, anchor="middle"))
        o.append(txt(cx, 290, foot, "lbl", size=15, anchor="middle"))
    # 主路连接箭头（末段 TTS → 喇叭，中途在 x1415 分叉）
    # 运动原语 ①：每段接头压一枚能量包，方向与箭头一致，恒速 ≈100 单位/秒
    #（短接头过得快、末段长所以久 —— 速度一致才读成同一股流，而不是五处各自闪）
    _lk = []
    for x1, x2, k in [(118, 180, 0), (400, 470, 1), (690, 760, 2), (980, 1050, 3), (1270, 1566, 4)]:
        _ln = x2 - 12 - x1
        _lk.append(packet("M%d 185 H%d" % (x1, x2 - 12), _ln, seg=18, w=9, op=".3",
                          dur="%.2fs" % ((_ln + 18) / 100.0), i=k))
        _lk.append(hline(x1, x2 - 12, 185, HS, 2, k))
        _lk.append(ah_r(x2, 185, "var(--ink-3)"))
    o.append(lp(*_lk))
    # ── step1：分叉点 + 虚线支路 + 数字人（可选件，不在主路上）──
    #   2026-08-20 四轮微调：支路整组左移 40px 并收窄 30px（290→260），
    #   把「数字人 · 可选」盒的右上角与喇叭下的「语音输出」标签拉开 ≥40px
    #   （原 10px：盒右缘 1560 贴着标签左缘 1570，读成两件东西粘在一起）。
    #   左侧同时验过：TTS 脚注「开口说话」右缘 ≈1198，盒左缘 1245 → 47px，两侧都松。
    #   分叉点 x 随盒心一起移到 1375，仍落在 TTS→喇叭那一段主路上，语义与 650ms 口径不变。
    o.append('<g data-step="1">')
    o.append(lp('<circle class="pop" style="--i:1;fill:%s" cx="1375" cy="185" r="6"/>' % AC,
                dline("M1375 193 V276", HS, 2, 2, dash="6 6", cls="mo-drift",
                      sty="--mo-off:-24;--mo-dur:2.4s"),
                ah_d(1375, 290, "var(--ink-3)", 7),
                box(1245, 292, 260, 70, 6, dashed=True, i=3)))
    o.append(txt(1375, 322, "数字人 · 可选", "ttl", size=21, anchor="middle"))
    o.append(txt(1375, 348, "口型 / 表情 · 与主路并行", "sm", size=14, anchor="middle"))
    o.append('</g>')
    # 端到端跨度标注（文字在线上方，绝不压线）· 只跨主路，数字人支路在线之上、不计入
    o.append(txt(840, 372, "端到端 650ms", "ttl", size=28, anchor="middle", col=AC, weight=700))
    o.append(lp(dline("M70 400 H1610", AC, 1.6, 6, dash="3 8"),
                vline(70, 390, 410, AC, 1.6, 6),
                vline(1610, 390, 410, AC, 1.6, 6)))

    # 盒链 + 分叉 + 650ms 是一组（整组上提 46px，收掉标题与图之间的空档）
    chain = "".join(o)
    o = []
    # ── 2026-08-20 三轮升维：链下加一条「增量流带」──────────────────────────
    #   ① 无字小跨度线（4 条，与上方四个盒左对齐、彼此重叠）：每一环不等上一环说完。
    #      刻意无字、无数字 —— 分环耗时没有已核定口径，全 deck 只有 650ms 一个数字。
    #   ② 增量流带：符号从左到右渐变形态（音频帧 → 增量文本 → token → 音频包），
    #      段落标注只用既有词（P8 里的「增量文本」「增量合成 · 随时可截断」）。
    _g = []
    for k, (sx, ex) in enumerate([(150, 620), (450, 920), (750, 1220), (1050, 1620)]):
        y = 432 + k * 12
        _g.append('<rect class="pop" style="--i:%d;fill:%s;opacity:%s" x="%d" y="%d" width="%d" '
                  'height="4" rx="2"/>' % (k + 2, AC, [".95", ".72", ".52", ".38"][k], sx, y, ex - sx))
    _g.append(packet("M150 518 H1596", 430, seg=26, w=13, op=".2", dur="5s", i=7))
    _g.append(hline(150, 1596, 518, HS, 1.4, 7))
    _g.append(ah_r(1610, 518, "var(--ink-3)", 7))
    # ① 音频帧（AI-VAD 段）：细密竖条
    for k in range(19):
        h = [16, 26, 12, 30, 20][k % 5]
        _g.append('<rect class="pop" style="--i:5;fill:%s" x="%d" y="%d" width="5" height="%d" rx="2"/>'
                  % (AC, 152 + k * 15, 518 - h // 2, h))
    # ② 增量文本（ASR 段）：一截截长出来的文本条
    for k in range(7):
        _g.append('<rect class="pop" style="--i:6;fill:%s;opacity:.9" x="%d" y="510" width="%d" '
                  'height="9" rx="4"/>' % (AC, 452 + k * 40, 12 + k * 3))
    o.append(lp(*_g))
    o.append(txt(452, 492, "增量文本", "sm", size=15, col=AC, mono=True))
    _g = []
    # ③ token（LLM 段）：一颗颗方块
    for k in range(11):
        _g.append('<rect class="pop" style="--i:6;fill:%s;opacity:.85" x="%d" y="509" width="17" '
                  'height="17" rx="4"/>' % (AC, 752 + k * 26, ))
    # ④ 音频包（TTS 段）：越来越密的圆角包，末尾被 accent-deep 截断记号收住
    for k in range(13):
        _g.append('<rect class="pop" style="--i:7;fill:%s;opacity:.9" x="%d" y="505" width="26" '
                  'height="26" rx="7"/>' % (AC, 1052 + k * 34, ))
    o.append(lp(*_g))
    o.append(txt(1052, 492, "增量合成 · 随时可截断", "sm", size=15, col=AC, mono=True))
    o.append(lp(vline(1502, 498, 538, AD, 4, 8)))
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
]), steps=1, lab="chain")

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
# 逐帧概率曲线与语义层：提到模块级 —— lab_k() 要拿它们做 3D 声学地形的**脊线**与前排折脊，
# 于是「地形的天际线」就是页上这条曲线本人（页上改了这一行，地形跟着改）。
_VADCURVE = ("M680 118 C 770 116, 836 102, 880 62 C 922 30, 980 40, 1042 48 "
             "C 1104 56, 1140 40, 1200 50 C 1256 60, 1272 84, 1302 96 "
             "C 1344 112, 1420 118, 1660 116")
_VADSEM = "M1430 78 C 1500 62, 1560 54, 1660 46"
# ── 波B 消闪 ③ 的常量与预计算表 ───────────────────────────────────────────
#   Colin 终审：「色块闪动营造流动感是偷懒的欺骗」——要真流动。
#   本页原来有两处**假流动**：滞回面靠 uFlow=0 的 sin(−uTime) 整片原地明灭、
#   立柱帽子逐帧改 alpha 呼吸。两件都是「同一块像素反复变亮变暗」= 闪。
#   换掉它们的三件（消闪三件）：
#     ① **地形整幅**按 A 档 110px/s 向左平移。要平移就得先**周期化**：
#        页上那条概率曲线两端差 2px（y 118 → 116），把这 2px 沿全幅**线性摊掉**
#        ⇒ 首尾的高度与斜率都接得上（两端本来就近乎水平，摊掉后斜率差 2/980）。
#        几何建满**两个周期**，每帧只设 scroll.position.x ——
#        一格顶点都不重算，闪的物理前提就不存在。一趟 980 ÷ 110 = **8.91s** 无缝。
#     ② 理解光束**驻位**在 SOS / EOS 两枚事件 x 上（滚动的是语音，钉住的是判定 ——
#        SOS/EOS 的 DOM 标签钉死在 x=880/1380，P7 又不在版式分歧名单里，
#        所以只能让地形从两道光束下穿过）。判定晕的半径是 gap / ons 两张
#        **对材料坐标预计算**的表的连续函数：
#          短谷 → 晕涨到一半就收回来；长谷 → 越过判定线，一边收细一边凝成晶柱落地。
#        阈值只在**构建期**（下面这两张表里）出现；运行时是一路连续插值，
#        **零随机、零状态机、零阈值跳变**。
#     ③ 语义层从「一条会飘的虚线」改成**贴着折脊走的连续流带** + 一条前沿馈送带。
_T_X0, _T_X1 = 20.0, 1000.0     # 地形的材料坐标区间（= 一个周期 980px）
_T_NT = 197                     # 预计算表长度（196 段 × 5px）
_T_HALO = (13.0, 26.0, 0.75)    # 判定晕：基半径 / 起声增益 / 长谷收缩系数
_T_PIL = (34.0, 7.0, 0.62)      # 晶柱：满高 / 基半宽 / 长谷收细系数
_T_SEMW, _T_FEEDW, _T_FEEDZ = 5.0, 3.0, 34.0   # 语义流带半宽 / 馈送带半宽 / 馈送带 z


def _vad_p(y):
    """页上纵轴：y=40 是概率 1、y=124 是概率 0（_vad_signal 的刻度本人）"""
    return max(0.0, min(1.0, (124.0 - y) / 84.0))


def _vad_tables():
    """三张对材料坐标预计算的表（长度 _T_NT，覆盖一个周期 [x0, x1]）：
         hp  周期化后的脊线 y（两端 2px 落差沿全幅线性摊掉）
         gap 该点所在静音谷的**长度**（归一到 260px 上限）
         ons 起声强度（概率的正向斜率）
       gap / ons 里可以出现阈值与分段 —— 它们是**构建期**的事。
       运行时只做「按弧长取表 + smoothstep 插值」，一条连续函数，**零阈值跳变**。"""
    pts = _decim(_pathpts(_VADCURVE, 18)[0], 1.2)
    xs = [q[0] - 660.0 for q in pts]
    ys = [q[1] for q in pts]

    def raw(x):
        if x <= xs[0]:
            return ys[0]
        for i in range(1, len(xs)):
            if xs[i] >= x:
                u = (x - xs[i - 1]) / ((xs[i] - xs[i - 1]) or 1.0)
                return ys[i - 1] + (ys[i] - ys[i - 1]) * u
        return ys[-1]

    y0, y1, span = raw(_T_X0), raw(_T_X1), _T_X1 - _T_X0
    step = span / (_T_NT - 1)
    # ① 周期化：把两端落差沿全幅线性摊掉（高度接得上，斜率只差 (y1−y0)/span = 2/980）
    hp = [raw(_T_X0 + i * step) - (y1 - y0) * (i * step) / span for i in range(_T_NT)]
    hp[-1] = hp[0]                                   # 末点钉死等于首点（浮点尾差归零）
    pr = [_vad_p(v) for v in hp]
    # ② 起声：概率的正向斜率（周期环上取差分）→ 高斯平滑 → 归一
    d = [max(0.0, (pr[(i + 1) % (_T_NT - 1)] - pr[(i - 1) % (_T_NT - 1)]) / (2 * step))
         for i in range(_T_NT)]
    ons = _gauss_ring(d, 18.0 / step)
    m = max(ons) or 1.0
    ons = [v / m for v in ons]
    # ③ 谷长：p < .5 的连通段长度 / 260（**阈值只在这里**，运行时看到的是平滑后的表）
    low = [1 if v < 0.5 else 0 for v in pr[:-1]]
    n = len(low)
    gl = [0.0] * n
    i = 0
    while i < n:
        if not low[i]:
            i += 1
            continue
        j = i
        while j < n and low[j]:
            j += 1
        L = (j - i) * step
        for k in range(i, j):
            gl[k] = min(1.0, L / 260.0)
        i = j
    gap = _gauss_ring(gl + [gl[0]], 26.0 / step)
    hp[-1] = hp[0]
    return ([round(v, 3) for v in hp], [round(v, 4) for v in gap], [round(v, 4) for v in ons])


def _gauss_ring(a, sig):
    """环上高斯平滑（首尾相接 ⇒ 表本身也是周期的，滚过接头不会有一记跳）"""
    n = len(a) - 1
    r = max(1, int(sig * 3))
    w = [math.exp(-(k * k) / (2.0 * sig * sig)) for k in range(-r, r + 1)]
    sw = sum(w) or 1.0
    out = []
    for i in range(n):
        out.append(sum(a[(i + k) % n] * w[k + r] for k in range(-r, r + 1)) / sw)
    out.append(out[0])
    return out


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
    # ④ 滞回带：两条点线阈值（参考语域）+ 极淡填充　【以下几何入 poster 层】
    #   3D 起来时这一段让位给 canvas 上的声学地形：概率曲线挤出成山脊、滞回带升成
    #   悬在地形上方的两枚判定面、SOS/EOS 变成地形上的立柱光标。字全部留在外面。
    o.append(lp(
        '<rect class="pop" style="--i:4;fill:%s;opacity:.07" x="680" y="%d" width="980" '
        'height="%d" rx="3"/>' % (AD, _VTOP, _VBOT - _VTOP),
        dline("M680 %d H1660" % _VTOP, AD, 2, 5, dash="2 6", cls="mo-drift",
              sty="--mo-off:-32;--mo-dur:4s"),
        dline("M680 %d H1660" % _VBOT, AD, 2, 5, dash="2 6", cls="mo-drift",
              sty="--mo-off:-32;--mo-dur:4s;--mo-del:-2s")))
    o.append(txt(692, 56, "平滑 / 滞回", "sm", size=13, col=AD, mono=True))
    # ⑤ 逐帧概率曲线（accent 实线）—— 也是 3D 地形的脊线母形（见 lab_k() 的 t.curve）
    o.append(lp('<path class="dw" style="--len:1200;--i:5" d="%s" fill="none" stroke="%s" '
                'stroke-width="3" stroke-linecap="round"/>' % (_VADCURVE, AC)))
    # ⑥ 两枚事件 pin（虚线 = 事件语法）
    for _j, (px, nm) in enumerate([(_VSOS, "SOS"), (_VEOS, "EOS")]):
        _d = "" if _j == 0 else ";--mo-del:-1.2s"
        o.append(lp(
            dline("M%d 32 V126" % px, HS, 2, 6, dash="6 6", cls="mo-drift",
                  sty="--mo-off:-24;--mo-dur:2.4s" + _d),
            '<circle class="pop mo-pulse" style="--i:6;--mo-dur:2.4s%s;fill:%s" cx="%d" cy="%d" r="6"/>'
            % (_d, AC, px, _VTOP if px == _VSOS else 117)))
        o.append(txt(px + 12, 44, nm, "lbl", size=15, col=AC))
    o.append(txt(1180, 18, "SOS / EOS 事件", "sm", size=14, col="var(--ink-3)", mono=True))
    # ⑦ 声学之上再叠一层语义（商业进阶版的差异，用既有词）
    o.append(lp('<path class="pop mo-drift" style="--i:7;--mo-off:-30;--mo-dur:2.8s" '
                'd="%s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 6"/>'
                % (_VADSEM, AD)))
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
]), steps=1, lab="terrain")

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
        # 括号本身是「侦测 / 收声 / 让位」三个字的脚手架（谁管哪一段全靠它），
        # 与图例同一语域 ⇒ 留在 canvas 之上，3D 不接管。
        o.append(hline(x1, x2, 62, AD, 2, 1))
        o.append(vline(x1, 62, 74, AD, 2, 1))
        o.append(vline(x2, 62, 74, AD, 2, 1))
        o.append(txt((x1 + x2) // 2, 46, nm, "sm", size=17, anchor="middle", col=AD, weight=700))
    # ── 智能体轨：说到一半被切断，其后是空带（让位）──
    o.append(txt(10, 128, "智能体", "ttl", size=22, col=AC))
    # 左侧波形的既有词标注：这一大段波形在讲什么，之前完全没说
    o.append(txt(170, 74, "智能体正在说话", "sm", size=17, col=AC))
    # 运动原语 ③ · 第 1 拍：智能体正在说（整条波形轻脉冲，文字在组外不跟着闪）
    o.append(lp('<g class="mo-pulse" style="--mo-lo:.62;--mo-dur:3.6s">%s</g>'
                % _bars(170, 51, 120, AC, hs=_P9HS),
                '<rect class="pop" style="--i:3" x="1055" y="88" width="585" height="64" rx="6" '
                'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 6"/>' % HS,
                _P9QUIET % (3, 1075, 118, 545),       # 让位段：无字静默平线（与用户轨呼应）
                # 第 3 拍：智能体收声（切断竖线；delay 1.4s ⇒ 排在插话之后）
                '<g class="mo-pulse" style="--mo-lo:.34;--mo-dur:3.6s;--mo-del:1.4s">%s</g>'
                % vline(_P9CUT, 82, 158, AD, 4, 3),
                # ── 340ms 快路径：插话 → 收声，粗 accent-deep，两端钉在两条轨之间 ──
                packet("M%d 230 V196 H%d" % (_P9IN, _P9CUT), 374, seg=30, col=AD, w=14, op=".3",
                       dur="2.4s", i=4),
                '<path class="dw" style="--len:374;--i:4" d="M%d 230 V196 H%d" fill="none" '
                'stroke="%s" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
                % (_P9IN, _P9CUT, AD),
                ah_u(_P9CUT, 168, AD, 8)))
    o.append(txt((_P9IN + _P9CUT) // 2, 184, "340ms", "ttl", size=26, anchor="middle",
                 col=AD, weight=700))
    # ── 用户轨：插话前是无字静默平线，从 _P9IN 起一直在说 ──
    o.append(txt(10, 278, "用户", "ttl", size=22, col="var(--ink-2)"))
    o.append(lp(_P9QUIET % (2, 170, 268, 510),
                _bars(_P9IN, 55, 270, "var(--ink-2)", seed=3, hs=_P9HS),
                # ── 两条时刻虚线（事件语域）+ 底部标注 ──
                # 第 2 拍：用户插话（事件时刻线；delay .7s ⇒ 夹在说话与收声之间）
                '<g class="mo-pulse" style="--mo-lo:.34;--mo-dur:3.6s;--mo-del:.7s">%s</g>'
                % dline("M%d 74 V320" % _P9IN, HS, 2, 5, dash="6 6"),
                dline("M%d 74 V320" % _P9CUT, HS, 2, 5, dash="6 6")))
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
]), lab="cutin")

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
    # 两枚环的几何入 poster 层：3D 起来时它们让位给 canvas 上的两层半透明球壳
    # （缺口方位、半径、内外关系全部照抄这两行 —— 见 lab_k() 的 s.r1/r2/gap1/gap2）。
    o.append(lp(
        _ring(_SR2, 40, 3, HS, "9 8", cls="mo-cycle",
              sty="--mo-off:-867;--mo-dur:26s"),          # 外环 r138 周长≈867 = dash「9 8」×51
        _ring(_SR1, 34, 3, AC, "8 7", cls="mo-cycle",
              sty="--mo-off:540;--mo-dur:18s")))          # 内环 r86 周长≈540 = dash「8 7」×36 · 反向
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
    o.append(lp(packet("M96 %d H234" % _SCY, 162, seg=24, dur="1.6s", i=2),
                hline(96, 234, _SCY, AC, 3.5, 2), ah_r(246, _SCY, AC)))
    o.append(txt(140, 170, "声纹锁定 · 只留目标人声", "sm", size=14, anchor="middle", col=AC))
    # ── 智能体（中 · 唯一 hot 件）──
    # 呼吸光晕：压在智能体圆片之下向外扩散再消失（100% 帧 opacity 回 0 ⇒ 静态语域下不留痕）
    o.append(lp(
        '<circle class="mo-halo" cx="%d" cy="%d" r="%d" fill="none" stroke="%s" '
        'stroke-width="2.5" opacity="0"/>' % (_SCX, _SCY, _SAG, AC),
        '<circle class="pop mo-breathe" style="--i:0;fill:var(--card-bg-2);stroke:%s" cx="%d" cy="%d" '
        'r="%d" stroke-width="3"/>' % (AC, _SCX, _SCY, _SAG)))
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
        _g = []
        if stop == _SR1:
            # 穿过外环：在交点上打一个不透明的洞，点线从洞里穿过去 —— 不写字也读得出「过了」
            ox, oy = _SCX - ux * _SR2, _SCY - uy * _SR2
            _g.append('<circle class="pop" style="--i:4;fill:var(--card-bg-2)" cx="%.1f" cy="%.1f" '
                      'r="11"/>' % (ox, oy))
        _g.append(dline("M%.1f %.1f L%.1f %.1f" % (613 + ux * 96, sy + uy * 96,
                                                   px - ux * 12, py - uy * 12), HS, 2.4, 5, dash="2 7",
                        cls="mo-drift", sty=_NSTY[_k]))
        o.append(lp(*_g))
        # ✕ 记号不进 poster 组：它标的是「这一路在哪一层被挡住」，而 3D 里粒子恰好
        # 在同一方向、同一半径上弹开（px 相机在 z=0 平面上 1 世界单位 = 1 像素），
        # 两条路径下它落在同一个点上 —— 留在外面，降级与 3D 都对得准。
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
]), lab="shell")

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
    # 四条样线与它们的标签是**图例**（不是图）⇒ 走 keep，留在 canvas 之上。
    _leg = [hline(0, 40, 649, AC, 2.5, 9), dline("M150 649 H190", HS, 2, 9, dash="6 5"),
            dline("M340 649 H380", AD, 2.2, 9, dash="2 6"), hline(520, 560, 649, AD, 5, 9)]
    o.append(_leg[0]); o.append(txt(50, 654, "音频流", "sm", size=14))
    o.append(_leg[1]); o.append(txt(200, 654, "事件 / 控制", "sm", size=14))
    o.append(_leg[2]); o.append(txt(390, 654, "AEC 参考", "sm", size=14))
    o.append(_leg[3]); o.append(txt(570, 654, "打断快路径", "sm", size=14))

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
    return _lpsplit(o, keep=_leg)

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
]), lab="bigmap")

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
# 下带那条「对话 · 连续不卡顿」的波浪（2026-08-31 第二波：3D 的下游 ribbon 就是它本人，
# 所以从 _weaknet_fig() 里提到模块级 —— 值一个字符没动）。
_P11WAVE = ("M12 426 Q 72 396 132 426 T 252 426 T 372 426 T 492 426 T 612 426 T 732 426 "
            "T 852 426 T 972 426 T 1012 426")
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
    _P11W = _P11WAVE
    o.append(packet(_P11W, 380, seg=30, w=13, op=".26", dur="3s", i=7))
    o.append('<path class="dw" style="--len:1200;--i:7" d="%s" fill="none" '
             'stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (_P11W, AC))
    o.append('<circle class="pop" style="--i:8;fill:%s" cx="1016" cy="426" r="7"/>' % AC)
    o.append(legend(0, 486, [("solid", "音频流 · 语音包"), ("dash", "丢包 / 断网"),
                             ("fill", "本地缓存余量")]))
    return _lpsplit(o)
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
    # 表达力精进 · 第一波 ③：SOURCE 下移一行（1010 → 1044，仍右对齐 1800）。
    #   旧版实测：落点句墨迹排到 x1103.6（.land 的盒是 1000 宽，但 29px 的句子
    #   953px 一行排得下 ⇒ 从 x150 一路排到 1103.6），而 SOURCE 的墨迹从
    #   x1096.5 起 —— 两栏在同一基线上**已经叠了 7px**，「同行两栏」根本没成立。
    #   只动布局：下移一行（+34 = .src 的行高 23.8 + 10 的行距）之后各占一行。
    #   与页脚三件的关系（实测）：底轨 y1045（发丝线 · 两端渐隐）在 SOURCE 墨迹
    #   1046.3–1068.3 之上 1.3px；页码 .sig 在 y44（右上角，另一头）；本页
    #   data-steps=0（没有 BUILD 指示）；页底 1078 那条板上装饰只到 x1010，
    #   与右对齐的 SOURCE 不同栏 —— 三处都不冲突。
    src(_SRC_TYP, y=_P11SRCY, x=1010, w=790, align="right"),
]), lab="qos")

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
    return _lpsplit(o)
page("content", "".join([
    head("BEYOND VOICE · 不止于听清", "看得见、认得人的<strong>多模态对话</strong>。"),
    lab(120, 236, "01 · SEE & SPEAK"),
    figbox(120, 292, 1680, 1680, 450, _io_fig(), i=1),
    rule(850),
    land("同一套引擎，看得见、说得出——让对话，走出屏幕。"),
]), lab="vision")

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
    """插槽：槽框（可虚线）+ 内模块块 + 槽名 + 块上方的 ⇄ 换装小件。

       ── 波B **第六处许可分歧：poster 分组** ────────────────────────────────
       原来这个函数把四件拼成**一整条带字的串**返回。`_lpsplit` 的判据是
       「片段里出现 <text 就整件留在 canvas 之上」—— 于是那块**不透明**的模块板
       （fill:var(--card-bg-2)）跟着字一起留在了 canvas 上面，把 3D 画进单元里的
       每一处小巧思全盖死了。本轮**只改分件方式**：四件各自成片段返回，
       `_lpsplit` 就能把「形」（槽框 / 模块板 / ⇄）收进 poster 组、只把「字」留在外面。
       **DOM 坐标一格没动**（⑳ 名册闸与 pinned 逐像素闸都照绿），
       变的只是 <g class="lab-poster"> 的分组 —— 登记在 _DIVERGE 的第六行。"""
    return [box(x, y, w, h, 8, dashed=dashed, i=i),
            '<rect class="pop" style="--i:%d;fill:var(--card-bg-2)" x="%d" y="%d" width="%d" '
            'height="%d" rx="6" stroke="%s" stroke-width="1.4"/>'
            % (i, x + 14, y + 12, w - 28, h - 24, HS),
            txt(x + w // 2, y + h // 2 + 8, name, "ttl", size=22, anchor="middle"),
            swap_mark(x + w - 46, y - 14, i=i,
                      sty="--mo-lo:.5;--mo-dur:5.4s;--mo-del:-%.1fs" % (0.9 * i))]
def _orch_fig():
    o = [txt(250, 26, "可自由替换 · 模型层", "lbl", size=16, anchor="middle", col=AC),
         txt(1430, 26, "按需叠加 · 高阶能力", "lbl", size=16, anchor="middle", col=AC)]
    # ── 左列：四个模型槽 → 支线汇到 x540 总线 → 一条主干进引擎（唯一一枚箭头落在引擎口）──
    _LY = [60, 168, 276, 384]
    for i, n in enumerate(_MODELS):
        y = _LY[i]
        o += _slot(60, y, 380, 68, n, i=i + 1)
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
        o += _slot(1240, y, 380, 68, n, i=i + 3, dashed=True)
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
    return _lpsplit(o)
page("content", "".join([
    head("OPEN & FLEXIBLE · 灵活扩展", "你的模型自由组合，<strong>引擎负责编排</strong>。"),
    lab(120, 236, "01 · ORCHESTRATION"),
    figbox(120, 272, 1680, 1680, 545, _orch_fig(), i=1),
    rule(850),
    land("快速编排 ASR / LLM / TTS / 数字人与语音体验，实时调试、一键发布智能体。"),
]), lab="slots")

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
    # 两条域分隔虚线是**页级分区件**（三个域底标靠它们站住），与图例同一语域 ⇒ keep。
    _div = [dline("M555 100 V500", HS, 1, 0, dash="3 9"),
            dline("M1125 100 V500", HS, 1, 0, dash="3 9")]
    o += _div
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
    return _lpsplit(o, keep=_div)
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
]), steps=1, lab="towers")

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
]), lab="hub")

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
]), lab="calls")

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
# 输入主通路（耳位波形 → 颞叶下部 01 区）：提到模块级 —— lab_k() 要拿它做 3D 输入声流的路径，
# 3D 与 2D 因此是同一条曲线（页上改了这一行，canvas 里那道声流跟着改）。
_BRAIN_IN = "M206 462 C330 526 452 566 572 566 C662 566 726 532 752 496"
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
    # ── 脑体（= poster 层）：LAB 旗舰版里这一整段是**降级层** ────────────────
    #   3D 起来时它淡出，canvas 上那颗体积点云大脑接管（母形就是下面这条 _BRAIN）；
    #   起不来 / print / 归档时它原样呈现 —— 这一页永远是完整的一页。
    #   区序号 / 引线 / 区名 / INPUT / 输出盒**全部不在这一组里**：它们压在 canvas 之上。
    f = []
    # ── ⑤ 霓虹底层（静态 · 不带动画 ⇒ 不进运动件账本）──
    f.append('<path d="%s" fill="none" stroke="%s" stroke-width="12" opacity=".07" '
             'stroke-linejoin="round"/>' % (_BRAIN, AC))
    # ── 小脑 / 脑干：先画（= 在大脑之后 / 之下），大脑的填色与轮廓随后压过它们的上缘 ──
    for _d in (_CEREB, _STEM):
        f.append('<path d="%s" fill="var(--card-bg-2)" opacity=".95"/>' % _d)
        f.append('<path d="%s" fill="%s" opacity=".045"/>' % (_d, AC))
        f.append('<path class="dw" style="--len:900;--i:2" d="%s" fill="none" '
                 'stroke="var(--ink-2)" stroke-width="2.2" stroke-linejoin="round"/>' % _d)
    # ── ① 五区放电（全部 clip 在轮廓里）──
    f.append('<g clip-path="url(#p17clip)">')
    for _d, _dur, _del in _ZONES:
        f.append('<path class="mo-pulse" style="--mo-hi:.05;--mo-lo:.15;--mo-dur:%s;--mo-del:%s" '
                 'd="%s" fill="%s" fill-rule="evenodd" opacity=".04"/>' % (_dur, _del, _d, AC))
    # 区内脑回纹理
    for _g in _GYRI:
        f.append('<path d="%s" fill="none" stroke="var(--ink-3)" stroke-width=".8" opacity=".42"/>' % _g)
    # 脑沟（分区边界）：比纹理重一档、比主轮廓轻一档
    for _s in (_SUL1, _SUL2, _SUL3):
        f.append('<path class="dw" style="--len:520;--i:3" d="%s" fill="none" '
                 'stroke="var(--ink-2)" stroke-width="2" opacity=".85"/>' % _s)
    # ── ② 突触弧线 + 神经火花（也 clip 在脑内 —— 火花不该跑到脑外去）──
    for _d, _ln, _dur, _del in _ARCS:
        f.append(dline(_d, AD, 1.2, 4, dash="2 7"))
        f.append(packet(_d, _ln, col=AC, w=8, seg=8, dur=_dur, op=".55", i=4,
                        delay=_del, cap="round"))
    for _k, _del in _ARC_EXTRA:
        _d, _ln, _dur, _ = _ARCS[_k]
        f.append(packet(_d, _ln, col=AC, w=8, seg=8, dur=_dur, op=".55", i=4,
                        delay=_del, cap="round"))
    f.append('</g>')
    # ── 主轮廓 + 小脑 + 脑干（画在填色之上 ⇒ 线稿永远压得住色块）──
    f.append('<path class="dw" style="--len:2600;--i:1" d="%s" fill="none" stroke="var(--ink-2)" '
             'stroke-width="2.5" stroke-linejoin="round"/>' % _BRAIN)
    f.append('<path d="M494 382 C534 400 578 412 616 424" fill="none" stroke="var(--ink-3)" '
             'stroke-width=".8" opacity=".5"/>')
    f.append('<path d="M486 418 C526 438 570 452 610 458" fill="none" stroke="var(--ink-3)" '
             'stroke-width=".8" opacity=".5"/>')
    f.append('<path d="M492 448 C528 466 568 476 604 480" fill="none" stroke="var(--ink-3)" '
             'stroke-width=".8" opacity=".5"/>')
    # 04 环形深部小区：补一圈描边，让「深部结构」读得出是一枚独立器件
    f.append('<g clip-path="url(#p17clip)"><path d="%s" fill="none" stroke="%s" '
             'stroke-width="1.8" opacity=".6" fill-rule="evenodd"/></g>' % (_ZONES[4][0], AC))
    o.append(lp(*f))
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
    o.append(lp(
        packet(_BRAIN_IN, 620, col=AC, w=11, seg=22, dur="2.6s", op=".34", i=2),
        '<path class="dw" style="--len:620;--i:2" d="%s" fill="none" stroke="%s" '
        'stroke-width="2.5"/>' % (_BRAIN_IN, AC),
        ah_u(756, 486, AC, 8)))
    # ── ③ 输出：额叶前缘 → hot 盒（粗 accent-deep 快路径 + 1.6s 重拍）──
    o.append(lp('<g class="mo-pulse" style="--mo-lo:.38;--mo-dur:1.6s">%s%s</g>'
                % (hline(1140, 1372, 268, AD, 5, 6), ah_r(1388, 268, AD, 8))))
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
]), lab="brain")

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
# ── 二轮精修 · 波A：双轴坐标整体左移 80px ─────────────────────────────────
#   终审：「排版上两张图偏挤，把双轴坐标左移一些，让 LOOP 不要如此挤压。」
#   两条纪律：
#     ① **改坐标本身，不加 transform**（接入指南 ⑧：P6 那两道 translate 翻过车 ——
#        3D 一旦忘了补同一道平移，整组错位、页上的字全掉到盒外）。这里连
#        _CA_CURVE 本人都是位移后的串，3D 读它即天然对位，没有第二份真相。
#     ② 取 **80**：最左墨迹是「DAY 01」（居中于 x70 ⇒ 页上 190、墨迹左缘 ≈164），
#        仍稳在版心 120 之内 —— 再往左就要啃版心。图例留在 x0 不跟移
#        （它本来就贴着版心左缘，是这一版的左基准）。
_CA_DX = 80
_CA_X = lambda x: x - _CA_DX
_CA_DAYS = [(150, "DAY 01"), (420, "DAY 07"), (700, "DAY 15"), (1060, "DAY 30")]


def _dxp(d, dx):
    """把一条**只含 M / C 绝对指令**的路径整体平移 −dx（改坐标本身，不加 transform）。
       非 M/C 当场抛 —— 这一条只服务 _CA_CURVE，不许悄悄用到别的路径上。"""
    toks = _re2.findall(r"[A-Za-z]|-?\d*\.?\d+", d)
    for t in toks:
        if t.isalpha():
            assert t in "MC", "_dxp 只吃 M / C：%r" % t
    out, k = [], 0
    for t in toks:
        if t.isalpha():
            out.append(t)
            continue
        v = float(t) - (dx if k % 2 == 0 else 0.0)
        out.append("%g" % v)
        k += 1
    return " ".join(out)


_CA_CURVE0 = ("M150 232 C 260 224, 340 214, 420 204 C 520 192, 620 176, 700 160 "
              "C 830 134, 960 108, 1060 70")
_CA_CURVE = _dxp(_CA_CURVE0, _CA_DX)
_CA_R0, _CA_R1, _CA_TURNS, _CA_N = 16.0, 56.0, 3.25, 460   # 复利螺旋：半径 / 圈数 / 采样
def _loopcurve_fig():
    o = []
    # ── 坐标轴（y 轴只画一截 + 一个箭头 = 「越高越好」，不标刻度：这页讲趋势不讲绝对值）──
    o.append(ah_u(_CA_X(110), 28, HS, 6))
    o.append(vline(_CA_X(110), 40, 250, HS, 1.4, 1))
    o.append(txt(_CA_X(126), 44, "转化效果", "sm", size=15, col="var(--ink-3)", mono=True))
    o.append(hline(_CA_X(110), _CA_X(1150), 250, HS, 1.4, 1))
    for _x, _d in _CA_DAYS:
        o.append(vline(_CA_X(_x), 250, 259, HS, 1.4, 1))
        o.append(txt(_CA_X(_x), 280, _d, "lbl", size=14, anchor="middle"))
    # ── 真人销冠平线（基准）──
    # 基准线与成长曲线的几何入 poster 层：3D 起来时曲线成为复利螺旋的**脊线**
    # （半径与带宽随 t 一起长），坐标轴 / 刻度 / 标签全部留在外面。
    # ⚠ 3D 必须把这条基准虚线**画回来**（波A 修的旧漏：3D 里没有它，
    #   页上「真人销冠」四个字就指着一片空白）。
    o.append(lp(dline("M%d 160 H%d" % (_CA_X(150), _CA_X(1060)), HS, 2, 2, dash="7 6",
                      cls="mo-drift", sty="--mo-off:-39;--mo-dur:3.4s")))
    o.append(txt(_CA_X(1075), 166, "真人销冠", "sm", size=17, col="var(--ink-3)"))
    # ── 外呼智能体成长曲线 ──
    o.append(lp(packet(_CA_CURVE, 980, seg=28, w=12, op=".32", dur="2.6s", i=3),
                '<path class="dw" style="--len:1020;--i:3" d="%s" fill="none" stroke="%s" '
                'stroke-width="3.4" stroke-linecap="round"/>' % (_CA_CURVE, AC)))
    o.append(txt(_CA_X(1075), 76, "外呼智能体", "sm", size=17, col=AC, weight=700))
    # ── 穿越点（DAY 15）：标签甩到点的左上，曲线在那一带是从右下往左下走的，不打架 ──
    o.append(lp('<circle class="pop mo-pulse" style="--i:4;--mo-dur:2.2s;--mo-lo:.34;fill:%s" '
                'cx="%d" cy="160" r="9"/>' % (AC, _CA_X(700))))
    o.append(txt(_CA_X(688), 138, "反超", "sm", size=18, anchor="end", col=AD, weight=700))
    # ── 终点（DAY 30）：2 倍位 ──
    o.append(lp(
        '<circle class="mo-halo" style="--mo-sc:2.2;--mo-op:.45;--mo-dur:3.2s" '
        'cx="%d" cy="70" r="10" fill="none" stroke="%s" stroke-width="2.5" opacity="0"/>'
        % (_CA_X(1060), AC),
        '<circle class="pop mo-breathe" style="--i:5;--mo-dur:3.2s;fill:%s" '
        'cx="%d" cy="70" r="10"/>' % (AC, _CA_X(1060))))
    o.append(txt(_CA_X(1060), 42, "2 倍", "ttl", size=26, anchor="middle", col=AC, weight=700))
    o.append(legend(0, 302, [("solid", "外呼智能体"), ("dash", "真人销冠基准")]))
    return "".join(o)
_CA_LOOP = [(190, 59, "复盘"), (286, 155, "定位"), (190, 251, "迭代"), (94, 155, "训练")]
_CA_RING = (190, 155, 96)       # LOOP 环：环心 / 半径（= 页上那枚 circle 本人）
_CA_NODE_R = 40                 # 四枚站点圆的半径
# 右图 figbox 在 x1420、舞台原点在 x120 ⇒ 环带在舞台局部坐标里整体右移这一档
_CA_RDX = 1420 - 120
def _loopring_fig():
    o = []
    # 环只让 dash 绕圈（.mo-cycle），几何不转：四个节点是钉在钟面位置上的，一转就乱套。
    # 周长 2πr = 603.2；dash「8 7」周期 15，--mo-off 取 600（= 40 个整周期）⇒ 100% 帧 = 原图。
    # 二轮精修 · 波A：环与四枚站点圆入 poster 层 —— 3D 起来时它们换成**投影锁空间环带**
    # （环平面一倾、包沿环巡行，四站名一格不挪）。方向标与四个词留在 canvas 之上。
    o.append(lp('<circle class="pop mo-cycle" style="--i:2;--mo-off:-600;--mo-dur:9s" '
                'cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="2.4" '
                'stroke-dasharray="8 7"/>' % (_CA_RING + (AC,))))
    for _deg in (45, 135, 225, 315):            # 四个缺口上的顺时针方向标
        o.append('<g transform="rotate(%d 190 155)">%s</g>' % (_deg, ah_d(286, 155, AC, 7)))
    for _i, (_x, _y, _nm) in enumerate(_CA_LOOP):
        o.append(lp('<circle class="pop" style="--i:%d;fill:var(--card-bg-2)" cx="%d" cy="%d" '
                    'r="%d" stroke="%s" stroke-width="1.6"/>'
                    % (3 + _i, _x, _y, _CA_NODE_R, AC)))
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
]), lab="spiral")
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
# ── LAB 半屏重排（**正文一个字节没动，只换盒子**）──────────────────────────
#   引擎版：四张 KPI 卡一行铺满 1680（g4）。LAB 版右半让给地球，四张卡改 2×2 落在
#   左列 930 宽里 —— 卡里的 tag / 数字 / 说明三行逐字照旧。
#   高度账（改盒宽必须重算这一笔）：
#     卡内容 = padding 24×2 + tag 18 + gap 10 + 数字 80×0.92 + gap 8 + 说明 20×1.45
#            ≈ 187 ⇒ 每行 196 够用（盒 416 − 行距 24，两行各 196）。
#     .lab-kpi 把 .card 的 30/32 padding 收到 24/26、gap 13 → 10：**只收白边，
#     不动任何字号** —— 80px 的数字在半屏里照样是这一页最大的东西。
#   卡宽 (930−24)/2 = 453，减内边距 52 = 401 的行宽：最长的一行说明
#   「稳居第一 · 份额超过第 2–8 位总和」实测 ~330px，单行放得下（改盒宽先量这一条）。
page("content", "".join([
    head("WHY AGORA · 底座实力", "跑在声网<strong>实时互动底座</strong>之上。"),
    sh("", "left:120px;top:264px;width:930px;height:416px",
       '<div class="g2 lab-kpi" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d;justify-content:center"><div class="tag%s">%s</div>'
           '<div class="stat"><span class="v%s" style="font-size:80px">%s</span>'
           '<span class="l">%s</span></div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag,
              "" if _on else " w", _v, _l)
           for _i, (_tag, _v, _l, _on) in enumerate(_WHY)) + '</div>'),
    # 2026-08-20 仲裁 P0：43.4% 这个具体数字未取得公司批准口径，改为「份额超过第 2–8 位
    # 厂商总和」的定性表述并把报告名写全；四张 KPI 卡的数字一个都不动。
    sh("flow", "left:120px;top:706px;width:930px;height:60px;--i:5",
       '<div class="note grey">注：IDC《中国视频云市场报告》音视频通信（RTC）赛道 · '
       '<b>份额超过第 2–8 位厂商总和</b></div>'),
    # top 794 而非 820：content 背景板自带一条 accent 细线在 y848–852（x120–761），
    # land 落在 820 时字形正压在线上 = 划掉的观感；抬到 794 让那条线落到文字下方当收口横线
    land("2014 年成立，全球最受欢迎的实时音视频云服务提供商——语音智能体，"
         "跑在经海量流量锤炼的底座上。", y=794),
    # 本行与 convoai-info P2 逐字同源，两份 deck 不许分叉（四大数与限定语同理）
    src("SOURCE · 声网官网 / IR 公开口径 · IDC 中国视频云市场报告 · 事实截止 2026.08"),
    # ── 地球角注（从 /lab-globe 的页脚原样搬来的那一行）────────────────────
    #   右对齐到版心右缘 1800、与左边的 SOURCE 行共一条页脚横轨 ——
    #   出处在左、图注在右，是一条轨不是两处零件。
    #   top 1017 而不是 1015：.mono-sm 15px 与 .src 17px 的**基线**要对齐，
    #   两枚盒顶差 2px 才是同一条线（改任一枚的字号必须重算）。
    #   这一行是硬要求，不是装饰：228 枚节点是**示意分布**，不标它就等于默认它是
    #   真实 PoP 清单。弧线同理 —— 全页一个延迟数值都不许出现（数字红线）。
    sh("flow mono-sm", "left:1120px;top:1017px;width:680px;height:24px;text-align:right;--i:7",
       "节点分布示意 · 200+ 全球节点 · SD-RTN"),
]), lab="globe")

# ═══ P22 · OpenAI 合作 · 末页（logo 锁定版 + 使命愿景 + 互动星系 · 页号 19→18→21→22）══
#   参照 robot26 #33「A QUIET ENDORSEMENT」，按 Colin 指令泛化两处：
#     ①「实时通信底座」→「对话式 AI 引擎底座」（本 deck 讲的是引擎，不是 RTC 管道）
#     ②「你的消费机器人」→「你的对话式智能体」（本 deck 的听众不限于机器人客户）
#   锚点 mono 行用 convoai-info P8 已核措辞「全球首批合作伙伴」——不写「全球首个」，
#   那是 OpenAI 的事，不是声网的事（info 二轮仲裁 P0 已钉死这一条）。
#   2026-08-21 收束轮 20 → 18：原 P20 收尾页删除，本页升为末页，承接两件事 ——
#     ① OpenAI × Agora logo 锁定版（robot26 双源资产跨引用，lt/dk 双 img CSS 显隐）；
#     ② 从被删收尾页继承的 CTA 行（Fable 裁定：真实入口不能随收尾页一起消失）。
#
#   ── 2026-09-03 改版：居中 → **左右两栏**（Colin：「info 最后一页的视觉复用到 lab 末页」）──
#   右半让给 convoai-info P8 的「互动星系」（三种互动由内向外生长）—— 与 P21 右侧的
#   SD-RTN 地球对仗：**底座 → 愿景**，一头一尾两枚球体收住整份 deck。
#   于是整页对齐方式跟着走：logo 锁定版与大字一起靠左（居中版的因果反过来用一次）。
#   OpenAI 段**一个字不改**，只是换了盒子；新增的只有使命 / 愿景两行 + 三区标注 + 角注。
#   使命 / 愿景两句 SOURCE 口径 = 声网官网 关于我们（与 convoai-info P8 逐字同源）。
P22_MISSION = "帮助人们跨越距离实时互动，如聚一堂。"
P22_VISION = "让实时互动像空气和水一样，无处不在。"
# ── 三区标注（DOM · 与 info P8 / P5 同一套 .ttl / 序号 / 引线样式）─────────────
#   逐字取自 convoai-info P8（那份 deck 的措辞已过仲裁），一个字不新造。
#   引线取端点起手写 d（**首个点 = 落点**）⇒ 端点小圆直接读 d 的第一对数（P17 同法）；
#   落点的盘面局部参数在 `_GX22_LEAD_END`，build() 末尾逐条对表（差 >0.6px 当场炸）。
#   坐标是 figbox 局部（vbw = 盒宽 ⇒ 局部 = 舞台 −(1060,130)）。
P22LEAD = [
    ("01", "人与人", "已经发生", "实时音视频 · 2014 年起",
     20, 66, "start", "M267.5 400 C245 320 180 214 100 148"),
    ("02", "人与智能体", "正在发生", "对话式 AI 引擎 · 企业级智能体 · R1",
     740, 66, "end", "M617 400 C645 322 665 224 692 148"),
    ("03", "智能体与智能体", "即将发生", "智能体之间的实时对话与协作",
     740, 670, "end", "M669.3 561.8 C683 588 696 614 709 640"),
]
#   角注：与左列 mono-sm ② 同一条 y1004 基线（P21「出处在左、图注在右」同一条轨）。
#   它是硬要求不是装饰：三枚环径是**示意**，不标它就等于默认它代表规模。
#   ⚠ 2026-09-03 终审修正：角注**不许出现色名**。原句写「玫红 = 人 · 蓝 = 智能体 ·
#     紫 = 智能体网」，但这三枚 token 是随主题变的（--gx-core 浅底走 accent 玫红、
#     暗底核偏淡紫；--gx-out-b 暗底是 --l-phys 紫蓝）—— 同一句话在暗底下就是错的。
#     改成只讲**结构**（三环由内向外生长），两档主题都成立；三种身份由 01/02/03
#     三区标注自己说，不必在角注里再翻译一遍颜色。
P22_NOTE = "互动星系示意 · 三环由内向外生长 · 环径不代表规模"


def p22_body(sh, figbox, txt, dline, lp):
    """P22 的页面 body —— **两份 deck 共用这一个函数**（引擎母本 import 本模块调它）。
       唯一的差别由 `lp` 参数给：LAB 传 `lp()`（把 poster 裹进 <g class="lab-poster">，
       3D 起来就淡出），引擎母本传恒等函数（poster 是那份 deck 里永久的 2D 正装）。
       ⇒ 两份产物的 P22 除 poster 组的那一对标签之外**逐字节相同**，
         同源自证不需要为这一页开任何白名单。
       sh / figbox / txt / dline 由调用方传入自己那一份同名件（两份 builder 里
       这四只是逐字同源的组装件 —— 另外 20 页的逐字节自证已经把这一条验死了）。"""
    AC = "var(--accent)"
    # 右半舞台：poster（形 · LAB 里会随 WebGL 起来而淡出）+ 三区标注（字与引线 · 常在）
    fig = [lp(gx_poster(GX22["cx"], GX22["cy"], GX22["s"], thin=4))]
    for (_no, _who, _when, _sub, _lx, _ly, _anc, _d) in P22LEAD:
        fig.append(dline(_d, "var(--ink-3)", 1.2, 5, dash="2 5"))
        fig.append('<circle class="pop" style="--i:5;fill:%s" cx="%s" cy="%s" r="3.4"/>'
                   % (AC, _d.split()[0][1:], _d.split()[1]))
        fig.append(txt(_lx, _ly, _no, "sm", size=13, anchor=_anc,
                       col="var(--ink-3)", mono=True))
        fig.append(txt(_lx, _ly + 26,
                       "%s · <tspan style=\"fill:%s\">%s</tspan>" % (_who, AC, _when),
                       "ttl", size=21, anchor=_anc))
        fig.append(txt(_lx, _ly + 54, _sub, "sm", size=14, anchor=_anc,
                       col="var(--ink-2)", mono=True))
    return "".join([
        sh("flow kk", "left:120px;top:128px;width:880px;height:28px",
           "2024.10.01 · A QUIET ENDORSEMENT"),
        # 盒 578×393 = 原片整幅按 0.69 缩；墨迹（= 视觉上的 logo 锁定版）落在
        # x120–520 / y175–428。为什么不按墨迹开盒 —— 见 DECK_CSS 里 .lock 那段；
        # 改盒宽必须按那段的比例重算 left/top（墨迹左偏 .15273×盒宽、上偏 .06283×盒高）。
        sh("spread lock", "left:32px;top:150px;width:578px;height:393px;--i:2",
           '<img class="lt" src="%(A)sopenai-agora-light.png" alt="OpenAI × 声网 Agora 合作标识">'
           '<img class="dk" src="%(A)sopenai-agora.webp" alt="OpenAI × 声网 Agora 合作标识">'
           % {"A": _R26}),
        # 46px / 880 宽：左列里排满三行（3 × 46×1.36 ≈ 188），字号从居中版的 58 收一档 ——
        # 半栏宽度下 58px 会排到五行，大字就不再是大字了。
        sh("ink", "left:120px;top:456px;width:880px;height:200px;"
           "font:700 46px/1.36 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
           # 「寻找」外面这层 nowrap 不是装饰：CJK 允许任意两字之间断行，
           # 一个词被劈成两行读起来像错字。
           "全球最强的 Voice Agent 团队，在为他们的 Realtime API "
           "<span style='white-space:nowrap'>寻找</span>"
           "<strong style='color:var(--accent)'>对话式 AI 引擎底座</strong>时，给出的选择。"),
        sh("spread", "left:120px;top:672px;width:120px;height:4px;background:var(--accent);"
           "border-radius:2px;--i:3", ""),
        sh("flow", "left:120px;top:700px;width:880px;height:42px;"
           "font:400 28px/1.5 var(--f-cn);color:var(--ink-2);--i:4",
           "同样的工程能力，我们用来支撑你的对话式智能体。"),
        # ── 使命 / 愿景两行（与 convoai-info P8 同一段标记 · 逐字同源）──────────
        #   愿景行的字形底落在 y852 之前，title 背景板那条 y≈878 的 hairline
        #   正好落在它下方当收口线（与 P1 封面同一条轨）。
    ] + [
        sh("settle", "left:120px;top:%dpx;width:880px;height:40px;--i:%d"
           % (776 + _i * 44, 5 + _i),
           '<div style="display:flex;align-items:baseline;gap:18px">'
           '<span style="flex:none;width:62px;font:700 15px/1 var(--f-mono);'
           'letter-spacing:.16em;color:var(--accent)">%s</span>'
           '<span style="font:500 24px/1.35 var(--f-cn);color:var(--ink)">%s</span></div>'
           % (_lb, _tx))
        for _i, (_lb, _tx) in enumerate((("使命", P22_MISSION), ("愿景", P22_VISION)))
    ] + [
        sh("flow mono-sm", "left:120px;top:966px;width:880px;height:24px;--i:7",
           "2024 OpenAI Realtime API 发布 · 声网为全球首批合作伙伴"),
        # CTA：纯文本 mono 行，不做假链接样式（没有 <a>，不加下划线/悬停态）
        sh("flow mono-sm", "left:120px;top:1004px;width:880px;height:24px;--i:8",
           "DEMO / 文档 · agora.io › 对话式 AI 引擎 · 联系团队"),
        # ── 右半：互动星系（figbox 与 lab-rect 是**同一只盒** ⇒ 局部原点同一个）──
        figbox(GX22["rect"][0], GX22["rect"][1], GX22["rect"][2],
               GX22["rect"][2], GX22["rect"][3], "".join(fig), i=1),
        sh("flow mono-sm", "left:1120px;top:1004px;width:680px;height:24px;"
           "text-align:right;--i:7", P22_NOTE),
    ])


page("title", p22_body(sh, figbox, txt, dline, lp), lab="galaxy")

# ═══ 组装 ═══════════════════════════════════════════════════════════════════
def build():
    total = len(PAGES)
    secs = []
    for i, (board, steps, body, labk) in enumerate(PAGES, 1):
        sig = '<div class="sig">%d/%d</div>' % (i, total)
        # 3D 舞台夹在背景板与 .pp 之间：两者都是 z-index:0，靠**文档序**分先后。
        # 无场景的页插入空串 ⇒ 这条模板拼出的字节与引擎母本完全相同。
        assert (labk is not None) == (i in LAB_RECTS), "P%d 的 lab= 声明与 LAB_RECTS 不一致" % i
        if labk is not None:
            assert labk == LAB_RECTS[i][0], "P%d 场景名分叉：%s vs %s" % (i, labk, LAB_RECTS[i][0])
        lab = ("  " + lab_stage(i) + "\n") if labk else ""
        secs.append(
            '<section class="slide conf-boarded" data-p="%d" data-steps="%d">\n'
            '  <div class="conf-bg conf-bg-%s" aria-hidden="true"></div>\n%s'
            '  <div class="pp">%s%s</div>\n</section>' % (i, steps, board, lab, sig, body))
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
        '<title>声网 · 对话式 AI 引擎 · 深入讲解 · LAB</title>\n'
        + FONTS
        + "<style>" + css("conf-theme-dual.css") + "</style>"
        + "<style>" + css("stage.css") + "</style>"
        + "<style>" + css("motion.css") + "</style>"
        + "<style>" + css("components.css") + "</style>"
        + "<style>" + css("conf-chrome.css").split("<svg class=\"deck-flow\"")[0] + "</style>"   # 流场退役：只取 CSS
        + BOARDS_CSS + DECK_CSS + LAB_CSS
        + "\n</head>\n<body>\n"
        # data-lab-diverge：版式分歧名册摊到产物上 —— qa 的同源自证复算它
        # （六处一处不多一处不少；构建期已与母本逐页对过几何）
        '<div class="deck-viewport">\n  <div class="deck-stage" id="deckStage" '
        'data-lab-diverge="%s">\n' % ";".join("%d:%s" % (p, k) for p, k, _w in _DIVERGE)
        + chrome + "\n" + "\n".join(secs) + "\n  </div>\n</div>\n"
        # 车库：全 deck 唯一那块 canvas 的常驻位（屏外）。挂在 .deck-viewport 之外 ——
        # 舞台自带 overflow:hidden + transform:scale，canvas 停在里面会被裁 / 被缩。
        + lab_garage() + "\n"
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
        # ── LAB 运行时（前奏 classic + importmap + module 本体）────────────
        + LAB_PRELUDE
        + '<script type="module">\nconst K=' + lab_k() + ';\n' + LAB_MODULE_BODY + '</script>\n'
        + "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")
    assert total == 22, "页数漂移：%d != 22" % total
    assert doc.count("<section") == 22, "section 数漂移：%d" % doc.count("<section")
    boards = {i: b for i, (b, _s, _y, _l) in enumerate(PAGES, 1)}
    assert {i for i, b in boards.items() if b == "title"} == {1, 22}, \
        "title 板页漂移：%r" % sorted(i for i, b in boards.items() if b == "title")
    steps_map = {i: s for i, (_b, s, _y, _l) in enumerate(PAGES, 1) if s}
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
    # 取某一页的 section（**必须带 <section 前缀**：DECK_CSS 里有
    # `.slide[data-p="22"]` 这样的选择器，裸串会先命中 CSS —— 本轮踩过一次）
    def _sec_of(pp):
        return doc.split('<section class="slide conf-boarded" data-p="%d"' % pp,
                         1)[1].split("</section>", 1)[0]

    # ── LAB 断言（构建期就拦住，别等到 qa）────────────────────────────────
    #   _INPAGE = poster 就是页上那张 SVG 的那些页（P1/P21 走专用离线 poster，不在内）
    #   加法层三页（三轮）另有一条**更硬**的自证（见下面的 ㉒ 闸），不走 poster 那条路
    _INPAGE = tuple(sorted(set(LAB_RECTS) - {1, 21} - set(_ADD_PAGES)))
    lab_map = {i: l for i, (_b, _s, _y, l) in enumerate(PAGES, 1) if l}
    _want = {i: v[0] for i, v in LAB_RECTS.items()}
    assert lab_map == _want, "LAB 3D 页漂移：%r != %r" % (lab_map, _want)
    assert sorted(lab_map) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                               17, 18, 21, 22], \
        "场景页码表漂移（七 + 九 + 三轮三枚加法层 + ⑥ 互动星系 = 20）：%r" % sorted(lab_map)
    # 逐页语义审查的留白：只剩 P19（R1 实拍照片页）与 P20（视频页）。
    #   P19 照片就是照片，加 3D 画蛇添足；P20 那支片子本身在动 —— 这是**既定判断**，
    #   两页一个像素不许改（2026-09-01 三轮复核，与 Colin 的「看下全部静态页」并不冲突：
    #   静态页升维指的是「页上没有动效的**图形页**」，实拍与视频不在其内）。
    assert sorted(set(range(1, 23)) - set(lab_map)) == [19, 20], \
        "保持 2D 的两页漂移：%r" % sorted(set(range(1, 23)) - set(lab_map))
    # ── 单渲染器巡游的硬红线：**全文档恰好一枚 canvas**（不是每页一枚）────────
    #   只数 <canvas> 标签：`lab-canvas` 这个串在 CSS 与运行时选择器里也出现。
    assert doc.count("<canvas") == 1, "canvas 件数漂移：%d（单渲染器巡游只准一枚）" % doc.count("<canvas")
    assert doc.count('class="lab-garage"') == 1, "缺 canvas 车库"
    assert doc.count('id="labGl"') == 1, "canvas id 漂移"
    # canvas 必须停在车库里（构建产物的初始态），不在任何一张 slide 里
    _garage = doc.split('<div class="lab-garage"', 1)[1].split("</div>", 1)[0]
    assert "<canvas" in _garage, "canvas 没停在车库里"
    for _sec in doc.split('<section class="slide')[1:]:
        assert "<canvas" not in _sec.split("</section>")[0], "有 slide 里塞了 canvas（应由运行时搬进去）"
    # ── 逐页舞台：矩形声明 / 场景名 / poster 层 / 打印帧位 ────────────────
    for _p, (_kind, _x, _y2, _w, _h) in LAB_RECTS.items():
        _sec = _sec_of(_p)
        assert 'data-lab-scene="%s"' % _kind in _sec, "P%d 舞台缺场景名" % _p
        assert 'data-lab-rect="%d,%d,%d,%d"' % (_x, _y2, _w, _h) in _sec, "P%d 图形区矩形漂移" % _p
        if _p in _ADD_PAGES:
            # 加法层：3D 没有替换任何东西 ⇒ **不许**挂 poster（挂一枚空的只是骗闸门）
            assert 'class="lab-poster"' not in _sec, \
                "㉒ P%d 是加法层页，不该有 poster —— 它的降级层是整页本身" % _p
        else:
            assert 'class="lab-poster"' in _sec, "P%d 缺 poster 降级层" % _p
        assert 'class="lab-print"' in _sec, "P%d 缺打印帧位" % _p
        assert _sec.count('class="lab-stage"') == 1, "P%d 舞台层不是一枚" % _p
        # 矩形必须落在版心内（超出就是对位算错了，别等到截图才发现）
        assert 0 <= _x and 0 <= _y2 and _x + _w <= 1920 and _y2 + _h <= 1080, \
            "P%d 图形区矩形出界：%r" % (_p, (_x, _y2, _w, _h))
    # 十四页的 poster 是**页上原来那张 SVG**：<g class="lab-poster"> 必须在 .pp 里
    #（只有 P1/P21 走构建期离线投影出来的专用 poster，落在舞台里）
    for _p in _INPAGE:
        _sec = _sec_of(_p)
        _pp = _sec.split('<div class="pp">', 1)[1]
        assert '<g class="lab-poster">' in _pp, "P%d 的图形没有裹进 poster 层" % _p
        # poster 组里**一个字也不许有**（字要压在 canvas 之上，任何降级路径下都在位）。
        # 逐组按 <g>/</g> 配对扫（P17 的组里还套着 clip-path 的 <g>，正则数不清层数）。
        _i = 0
        while True:
            _i = _pp.find('<g class="lab-poster">', _i)
            if _i < 0:
                break
            _j, _dep = _i + 22, 1
            while _dep > 0:
                _ng, _ne = _pp.find("<g", _j), _pp.find("</g>", _j)
                if _ne < 0:
                    break
                if 0 <= _ng < _ne:
                    _dep += 1; _j = _ng + 2
                else:
                    _dep -= 1; _j = _ne + 4
            assert "<text" not in _pp[_i:_j], "P%d 的 poster 组里裹进了文字件" % _p
            _i = _j
    # three 零外链：只准指自托管路径
    assert "/decks/assets/three/three.module.min.js" in doc and "cdn" not in doc.lower().split("<body")[0]
    # 材质色红线：LAB 运行时里一个色号都不许写死（#rgb / rgb() / hsl() 一律不许）
    _js = doc.split('<script type="module">', 1)[1]
    # 注释先剥掉再扫：注释里写「归一成 rgb()」是**说明**，不是色号
    _js_code = _js.split("</script>", 1)[0]
    _js_code = _re2.sub(r"/\*.*?\*/", " ", _js_code, flags=_re2.S)
    _js_code = _re2.sub(r"(?m)//.*$", " ", _js_code)
    for _pat in (r"#[0-9a-fA-F]{3,8}\b", r"\brgba?\(", r"\bhsla?\("):
        _hit = [m for m in _re2.findall(_pat, _js_code)]
        assert not _hit, "LAB 运行时写死了色号（%s）：%r —— 材质色只准读 CSS 变量" % (_pat, _hit[:4])
    # ── ⑳ 第二波几何名册 × 产物逐条对表（2026-08-31 终波）────────────────
    #   第二波九枚场景的盒表 / 环表 / 路径串全部**抄自页上**，这一闸把每一条与
    #   产物里真实存在的 <rect> / <circle> / d= 对回去：页面改了图而 3D 没跟上，
    #   构建当场炸（不会静默错位 —— 本轮 P6 那两道 translate 就是这么找出来的）。
    def _svg_of(pp):
        return _sec_of(pp)

    def _rectset(h):
        return {(int(float(a)), int(float(b2)), int(float(c2)), int(float(d2)))
                for a, b2, c2, d2 in _re2.findall(
                    r'<rect[^>]*?\bx="([-\d.]+)"\s+y="([-\d.]+)"\s+width="([-\d.]+)"\s+'
                    r'height="([-\d.]+)"', h)}

    def _circset(h):
        return {(int(float(a)), int(float(b2)), int(float(c2)))
                for a, b2, c2 in _re2.findall(
                    r'<circle[^>]*?\bcx="([-\d.]+)"\s+cy="([-\d.]+)"\s+r="([-\d.]+)"', h)}

    def _onpage(pp, rects=(), circs=(), paths=()):
        _h = _svg_of(pp)
        _R, _C = _rectset(_h), _circset(_h)
        for _r in rects:
            assert tuple(_r[:4]) in _R, "⑳ P%d 的 3D 盒表在页上找不到对应矩形：%r" % (pp, _r[:4])
        for _c in circs:
            assert tuple(_c[:3]) in _C, "⑳ P%d 的 3D 环表在页上找不到对应圆：%r" % (pp, _c[:3])
        for _d in paths:
            assert 'd="%s"' % _d in _h, "⑳ P%d 的 3D 路径在页上找不到：%r" % (pp, _d[:40])

    _onpage(2, rects=_P2N, paths=[_P2ARC])
    _onpage(6, rects=_P6ST + [_P6DH], circs=_P6RING)
    _onpage(10, rects=_P10BOX, circs=_P10RING)
    _onpage(11, rects=[(b[0], _P11BY, _P11BW, _P11BH) for b in _P11BAR]
                      + [m[:4] for m in _P11MECH] + [_P11BIN],
            paths=[_P11WAVE])
    _onpage(12, rects=[b[:4] for b in _P12BOX] + _P12WEAK)
    _onpage(13, rects=_P13SLOT + [_P13HUB])
    _onpage(14, rects=[t[:4] for t in _P14T] + [i[:4] for i in _P14IN],
            paths=[a[0] for a in _P14ARC])
    # P18（波A 新入名册）：LOOP 环与四枚站点圆 —— 3D 里的空间环带就是这几个圆本人
    _onpage(18, circs=[_CA_RING] + [(x, y, _CA_NODE_R) for x, y, _nm in _CA_LOOP])

    # ── lab-kit ⑨ 的三条数学前提（不成立就没有「不可能有锯齿」这句话）────────
    assert abs(sum(_AS_A) - 1.0) < 1e-9, \
        "⑨ 谐波权重未归一（Σa=%r）—— en = .5+.5·Σaᵢsin 就不再恒 ∈[0,1]" % sum(_AS_A)
    assert all(x > 0 for x in _AS_A), "⑨ 谐波权重必须全正"
    for _i in range(len(_AS_F)):
        for _j in range(_i + 1, len(_AS_F)):
            _r = _AS_F[_j] / _AS_F[_i]
            assert abs(_r - round(_r)) > 0.05, \
                "⑨ 谐波 %d/%d 成整数比（%.3f）—— 包络会齐步，起伏变心跳" % (_i, _j, _r)
    assert 0 < _AS_GHOST < _AS_FLOOR, "⑨ ghost 档必须比幅度地板还低（让位 = 细线）"
    # 让位窗口必须**正好**是页上「收声」那段相位括号（840 → 1040，200px）
    assert _U_DUCK0 == 840 and _P9CUT - _U_DUCK0 == 200, \
        "⑨ P8 让位窗口不是页上「收声」那段括号（%d→%d）" % (_U_DUCK0, _P9CUT)
    assert ('%d 62' % _U_DUCK0) in _svg_of(8) or ('H%d' % _U_DUCK0) in _svg_of(8), \
        "⑨ P8 让位窗口的左界在页上找不到对应的相位括号界"
    # 符号行四段严丝合缝（三处接缝）：有缝就不是一条流
    for _i in range(3):
        assert _P6SEG[_i][1] == _P6SEG[_i + 1][0], \
            "⑨ P6 符号行第 %d 处接缝有缝：%r" % (_i + 1, _P6SEG[_i:_i + 2])
    # ── 终审硬伤一：P13 转子净空 ≥16px（构建失败条件，不是手感）─────────────
    #   构建期量的是**几何**（环 / 轨道的中心线），运行时 state().clr 还要再减掉
    #   粒子的半径（--k-core-size 3.4 ⇒ ≈1.7px）与线宽的一半 —— 所以这里预留 2px：
    #   构建期 ≥ 18 才保证「可见几何」在运行时也 ≥ 16。
    assert _K_CLR_MIN >= _K_CLR + 2.0, \
        ("⑮ P13 转子压字：与「对话引擎 / 实时编排」墨迹盒最小净空 %.1fpx < %.0f+2px"
         % (_K_CLR_MIN, _K_CLR))
    _obx = _K_ORB_BOX
    assert (_obx[0] >= _P13HUB[0] + 4 and _obx[2] <= _P13HUB[0] + _P13HUB[2] - 4
            and _obx[1] >= _P13HUB[1] + 4 and _obx[3] <= _P13HUB[1] + _P13HUB[3] - 4), \
        "⑮ P13 转子越出机腔：包围盒 %r vs 机腔 %r" % ([round(v) for v in _obx], _P13HUB)
    # 三枚轨道必须**真异面**（az 两两不同、且不全同号），否则就是三枚同心圆
    assert len({o[2] for o in _K_ORB}) == 3 and min(o[2] for o in _K_ORB) < 0 < max(
        o[2] for o in _K_ORB), "⑮ P13 三枚轨道不是异面（az=%r）" % [o[2] for o in _K_ORB]
    # 发布脉冲的注光路径也不许压字：起点坐在腔底（按转子那一档深度投影），
    # 其余两点走投影锁（页坐标本人）。透视是线性的 ⇒ 投影后逐段仍是直线段。
    _pubpx = [_k_proj(_P13PUB[0][0], _P13PUB[0][1], 0.0)] + [
        (float(q[0]), float(q[1])) for q in _P13PUB[1:]]
    for _i in range(len(_pubpx) - 1):
        _a, _b = _pubpx[_i], _pubpx[_i + 1]
        for _k in range(41):
            _t = _k / 40.0
            _px, _py = (_a[0] + (_b[0] - _a[0]) * _t, _a[1] + (_b[1] - _a[1]) * _t)
            for _r in _P13INK:
                _dx = max(_r[0] - _px, 0.0, _px - (_r[0] + _r[2]))
                _dy = max(_r[1] - _py, 0.0, _py - (_r[1] + _r[3]))
                assert math.hypot(_dx, _dy) >= _K_CLR, \
                    "⑮ P13 发布脉冲注光路径压字：(%.0f,%.0f) 距墨迹盒 %.1fpx" % (
                        _px, _py, math.hypot(_dx, _dy))
    # ── 终审硬伤二：P13 贯通流必须有落点，且不许溢出版心 ─────────────────────
    _fend = (LAB_RECTS[13][1] + _P13FLOW[-1][0], LAB_RECTS[13][2] + _P13FLOW[-1][1])
    _sink = LAB_RECTS[13][1] + _P13PILL[0] + _P13PILL[2]     # 发布槽右缘（页坐标）
    assert _fend[0] <= 1800, "⑨ P13 贯通流溢出版心：终点 x=%d > 1800" % _fend[0]
    assert abs(_fend[0] - _sink) <= 40, \
        "⑨ P13 贯通流没有落点：终点 x=%d 不在发布槽右缘 %d ±40 内" % (_fend[0], _sink)
    assert _P13PILL[1] <= _P13FLOW[-1][1] <= _P13PILL[1] + _P13PILL[3], \
        "⑨ P13 贯通流的终点没落在发布槽的高度区间里（y=%d）" % _P13FLOW[-1][1]
    assert 0 < _K_FLOWGHOST < _K_FLOWFLOOR < _AS_FLOOR and _K_FLOWW < 11.0, \
        "⑨ P13 幅度覆写不成立（ghost %.3f / floor %.3f / w %.1f）" % (
            _K_FLOWGHOST, _K_FLOWFLOOR, _K_FLOWW)
    assert (_AS_LAM, _AS_FLOOR, _AS_GHOST) == (232.0, 0.30, 0.055), \
        "⑨ lab-kit ⑨ 的全局幅度档被动了 —— P13 只准在本页 opt 里覆写"
    # ── ㉒ 三轮「静态页升维」· 加法层三页的构建期硬闸 ─────────────────────────
    #    ① 净空：每一页的 3D 几何与该页**字形墨迹盒**的最小距离 ≥ 16px
    #       （已扣掉带宽 / 粒半径 —— 量的是「屏上真的画出来的边缘」，不是中心线）；
    #    ② 出界：几何必须落在该页声明的 lab-rect 里（越界就是被 canvas 裁掉一半）。
    #    （2026-09-03：原本的第三条「末页克制」随余韵星野一起退役 —— P22 现在是
    #      在页 3D 页，它的机器面在下面那一段 ⑳galaxy。）
    for _p in _ADD_PAGES:
        assert _ADD_CLRMIN[_p] >= _ADD_CLR, \
            "㉒ P%d 的 3D 压字：与字形墨迹盒最小净空 %.1fpx < %.0f" % (
                _p, _ADD_CLRMIN[_p], _ADD_CLR)
        for _b in _ADD_INK[_p]:
            assert 0 <= _b[0] and 0 <= _b[1] and _b[0] + _b[2] <= 1920 \
                and _b[1] + _b[3] <= 1080, "㉒ P%d 的墨迹盒出界：%r" % (_p, _b)
    _addgeo = {
        5: [_x5_drop(k) for k in range(3)] + [_X5COL, _x5_arrow(), _box_pts(*_X5HAZE)],
        15: [_h15_spoke(_k) for _k in range(6)]
            + [_box_pts(_c[0] - _H15CLW, _c[1] - _H15CLH, _H15CLW * 2, _H15CLH * 2)
               for _c in _H15CL]
            + [_box_pts(_H15CORE[0] - _H15CR, _H15CORE[1] - _H15CR, _H15CR * 2, _H15CR * 2)],
        16: [_n16_lane(_k) for _k in range(_N16N)],
    }
    for _p, _gs in _addgeo.items():
        # ⚠ 名册与舞台位表必须是同一份真相：只改一半 ⇒ 几何落在 canvas 之外被裁掉，
        #   而 ㉒ 的出界闸拿的是名册那一份，什么都验不出来（本轮踩过一次）。
        assert tuple(_ADD_RECT[_p]) == tuple(LAB_RECTS[_p][1:]), \
            "㉒ P%d 的 _ADD_RECT 与 LAB_RECTS 分叉：%r vs %r" % (
                _p, _ADD_RECT[_p], LAB_RECTS[_p][1:])
        _rx, _ry, _rw, _rh = _ADD_RECT[_p]
        for _g in _gs:
            for _q in _g:
                assert _rx <= _q[0] <= _rx + _rw and _ry <= _q[1] <= _ry + _rh, \
                    "㉒ P%d 的几何越出 lab-rect：%r ∉ %r" % (_p, (round(_q[0]), round(_q[1])),
                                                        _ADD_RECT[_p])
    # 加法层不许新造文字 / 数字：这三页的 3D 一个字都不画（数字红线的机器面）
    for _p in _ADD_PAGES:
        assert _p in LAB_RECTS and LAB_RECTS[_p][0] in ("three", "hub", "calls")

    # ── ⑳galaxy P22「互动星系」的构建期硬闸（解出来的，不是调出来的）────────────
    #    与 convoai-info P8 的 ⓖ / ⑳galaxy 同一批判据，只是半径全部乘了 s。
    _gs = GX22["s"]
    assert _GX_CORE_N + _GX_IN_N + _GX_OUT_N == _GX_N == 12000, \
        "⑳galaxy 三环点数合计 %d != 12000" % _GX_N
    assert _GX_IN_N % 2 == 0 and _GX_OUT_N % 2 == 0, "⑳galaxy 环带点数不是偶数（交错分不平）"
    _gr = [v * _gs for v in (_GX_CORE_R, _GX_IN_R0, _GX_IN_R1, _GX_OUT_R0, _GX_OUT_R1)]
    assert all(_gr[i] > _gr[i - 1] for i in range(1, 5)), \
        "⑳galaxy 三环半径不是严格递增：%r" % [round(v, 1) for v in _gr]
    assert _gr[1] - _gr[0] >= 60 * _gs and _gr[3] - _gr[2] >= 50 * _gs, \
        "⑳galaxy 环与环之间的净空缝太窄：%r" % [round(v, 1) for v in _gr]
    assert _GX_SN == _GX_SN_IN + _GX_SN_RAD == 20 and _GX_ARCS == 24, \
        "⑳galaxy 流 / 弧的股数漂移：%d 股 / %d 弧" % (_GX_SN, _GX_ARCS)
    # ① 三枚引线落点离环带 ≥16px（构建期扫掠包络实测 —— 机器判据，不是目测）
    for _k, _v in enumerate(_GX22_LEAD):
        assert _v >= _GX_LEADCLR, \
            "⑳galaxy 第 %d 组标注的引线落点离环带只有 %.1fpx（下限 %.0f）" % (
                _k + 1, _v, _GX_LEADCLR)
    # ② 引线 d 的**首个点**必须就是落点的投影（端点小圆直接读这一对数）
    for (_no, _who, _wh, _sub, _lx, _ly, _anc, _d), _end in zip(P22LEAD, _GX22_LEAD_END):
        _q = _gx_page(_end[0], _end[1], _end[2], GX22["cx"], GX22["cy"], _gs)
        _dx = abs(float(_d.split()[0][1:]) - _q[0])
        _dy = abs(float(_d.split()[1]) - _q[1])
        assert max(_dx, _dy) <= 0.6, \
            "⑳galaxy %s 组引线的起手点没落在落点上：d=%s… vs 投影 (%.1f, %.1f)" % (
                _no, _d[:22], _q[0], _q[1])
    # ③ 整个扫掠包络（含点径 / 带宽 pad）必须落在 lab-rect 之内 —— 越界就被裁掉一半
    _grx, _gry, _grw, _grh = GX22["rect"]
    for _px, _py, _pad in _GX22_PROBE:
        assert _grx <= _px - _pad and _px + _pad <= _grx + _grw \
            and _gry <= _py - _pad and _py + _pad <= _gry + _grh, \
            "⑳galaxy 扫掠包络越出 lab-rect：(%.1f, %.1f) ± %.1f ∉ %r" % (
                _px, _py, _pad, GX22["rect"])
    # ④ 星系不出版心右缘 1800（摇摆绕竖轴转 ⇒ u 被混进 z，z 跨 < u 跨，撑不出 470s）
    assert _grx + GX22["cx"] + _gr[4] <= 1800.0, \
        "⑳galaxy 外环外缘越过版心右缘 1800：%.1f" % (_grx + GX22["cx"] + _gr[4])
    # ⑤ 净空：扫掠包络到 P22 字形墨迹盒 ≥16px（运行时 state().clr 复量同一个数）
    assert _P22CLRMIN >= _GX_LEADCLR, \
        "⑳galaxy P22 的 3D 压字：与字形墨迹盒最小净空 %.1fpx < %.0f" % (
            _P22CLRMIN, _GX_LEADCLR)
    for _b in _P22INK:
        assert 0 <= _b[0] and 0 <= _b[1] and _b[0] + _b[2] <= 1920 and _b[1] + _b[3] <= 1080, \
            "⑳galaxy P22 的墨迹盒出界：%r" % (_b,)
    # ⑥ poster **零文字**（字全部在 canvas 之上），角注必须写着「示意」
    _p22 = _sec_of(22)
    _pg22 = _p22.split('<g class="lab-poster">', 1)[1].split("</g>", 1)[0]
    assert "<text" not in _pg22 and "<tspan" not in _pg22, "⑳galaxy P22 的 poster 组里裹进了字"
    assert _pg22.count("gx-p1") == 1 and _pg22.count("gx-rim") == 3 \
        and _pg22.count("gx-arc") == _GX_ARCS and _pg22.count("gx-flow") == _GX_SN, \
        "⑳galaxy P22 poster 件数漂移（核 / 轮廓环 / 弧 / 流）"
    assert P22_NOTE in _p22 and "示意" in P22_NOTE, "⑳galaxy P22 缺角注 —— 环径不许被当成规模"
    # ⑦ 使命 / 愿景两句逐字（SOURCE 口径：声网官网 关于我们）
    for _q2 in (P22_MISSION, P22_VISION):
        assert _q2 in _p22, "P22 缺使命 / 愿景原句：「%s」" % _q2
    for _q2 in ("人与人", "人与智能体", "智能体与智能体", "已经发生", "正在发生", "即将发生"):
        assert _q2 in _p22, "P22 缺三区标注「%s」" % _q2
    # ⑧ OpenAI 段原字（换了盒子，一个字不许动）—— 客户名与「首批」口径的机器面
    for _q2 in ("2024.10.01 · A QUIET ENDORSEMENT", "全球最强的 Voice Agent 团队",
                "对话式 AI 引擎底座", "同样的工程能力，我们用来支撑你的对话式智能体。",
                "声网为全球首批合作伙伴", "agora.io › 对话式 AI 引擎"):
        assert _q2 in _p22, "P22 的 OpenAI 段原字被动了：缺「%s」" % _q2
    assert "全球首个" not in _p22, "P22 出现「全球首个」—— 首批口径已钉死"

    # ── 表达力精进 · 第一波：P2 / P4 的净空闸（借加法层那把 ≥16px 的尺子）────────
    for _p, _m in ((2, _P2CLRMIN), (4, _P4CLRMIN)):
        assert _m >= _CLR[_p], \
            "① P%d 的 3D 压字：与字形墨迹盒最小净空 %.1fpx < %.0f" % (_p, _m, _CLR[_p])
        for _b in _INK[_p]:
            assert 0 <= _b[0] and 0 <= _b[1] and _b[0] + _b[2] <= 1920 \
                and _b[1] + _b[3] <= 1080, "① P%d 的墨迹盒出界：%r" % (_p, _b)
    # ① P2：02 区必须整块落在 lab-rect 里（越界就是被 canvas 裁掉一半），
    #    且与四栏卡底（y735）≥40px、上排 / 下排各自躲开收口线 y850。
    _r2 = LAB_RECTS[2]
    for _g in _p2_geo_boxes():
        assert _r2[1] <= _g[0] and _g[0] + _g[2] <= _r2[1] + _r2[3] + 0.001, \
            "① P2 的 02 几何横向越出 lab-rect：%r" % (_g,)
        assert _r2[2] <= _g[1] and _g[1] + _g[3] <= _r2[2] + _r2[4], \
            "① P2 的 02 几何纵向越出 lab-rect：%r" % (_g,)
    _p2top = min(b[1] for b in _P2INK) + _INKPAD          # 名册留量扣回来 = 实测墨迹顶
    assert _p2top - 735 >= 40, \
        "① P2 的 02 顶（%.0f）与四栏卡底 y735 净空 %.1f < 40px" % (_p2top, _p2top - 735)
    assert 780 + _P2RY + _P2RW < 850 < 780 + _P2LY[0] - _P2LW[0], \
        "① P2 的收口线 y850 横穿了某一排（上排底 %.0f / 下排顶 %.0f）" % (
            780 + _P2RY + _P2RW, 780 + _P2LY[0] - _P2LW[0])
    assert _P2SEG[0][1] < _P2SEG[1][0] < _P2SEG[1][1] < _P2SEG[2][0], \
        "① P2 上排三段没有真空档（串行的全部证据就在这两处空档上）：%r" % (_P2SEG,)
    assert _P2SEG[2][0] < _P2EVT < _P2SEG[2][1] and _P2SPK < _P2EVT, \
        "① P2 的事件不在两排的「说」段之内：%s" % _n(_P2EVT)
    # ② P4：舞台起点必须在三行说明最右墨迹 + 16px 之外（病名 B 的机器面）
    _p4r = max(b[0] + b[2] for b in _P4INK)
    assert LAB_RECTS[4][1] + _D_X0 >= _p4r + _CLR[4], \
        "② P4 舞台起点 %d 没有让开三行说明的最右墨迹 %d + %d" % (
            LAB_RECTS[4][1] + _D_X0, _p4r, _CLR[4])
    # 两次交叉：yA = yB ⇔ cos(θ)+cos(θ+phase) = 0 ⇔ θ = π/2 − phase/2 + kπ
    _cross = [k for k in range(9)
              if 0 <= math.pi / 2 - _D_PHASE / 2 + k * math.pi <= 2 * math.pi * _D_TURNS]
    assert len(_cross) == 2, \
        "② P4 两条声带在新跑道上交叉 %d 次（要两次）：turns=%s" % (len(_cross), _n(_D_TURNS))

    # P14 一轮 = 生长 + 全亮停驻 + 收尾，且生长由三段路由 ÷ 同一档注光速度反推
    _rt = [_plen_d(_a[0]) for _a in _P14ARC]
    assert abs(sum(_rt) / _Y_BEAM - _Y_GROW) < 1e-9, "⑨ P14 生长时长不是三段 ÷ 400px/s"
    assert abs(_Y_CYC - (_Y_GROW + _Y_HOLD + _Y_REL)) < 1e-9, "⑨ P14 一轮 != 生长+停驻+收尾"
    assert _Y_HOLD >= 2.0, "⑨ P14 全亮停驻不足 2s —— 那一帧是本页的重点帧"
    # ── 全局速度品味检查：A 档 30 股全部落在 110 ±30% 内 ─────────────────
    _SPD_ALL = [(_p, nm, sp) for _p in sorted(LAB_RECTS) for nm, _L, sp in _spd_rows(_p)]
    assert len(_SPD_ALL) == _SPD_N, "④ A 档股数漂移：%d（应为 %d）" % (len(_SPD_ALL), _SPD_N)
    _lo, _hi = _SPD_A * (1 - _SPD_TOL), _SPD_A * (1 + _SPD_TOL)
    for _p, _nm, _sp in _SPD_ALL:
        assert _lo <= _sp <= _hi, "④ P%d「%s」流速 %.1f 越出 110±30%%" % (_p, _nm, _sp)
    _spdlo = min(x[2] for x in _SPD_ALL)
    _spdhi = max(x[2] for x in _SPD_ALL)
    # P3 的 band 是逐条现算的矩形（列 x 由 _P3LX/_P3RX 决定）—— 同样逐条对表
    for _m, _bs in _P3BANDS.items():
        for _b in _bs:
            _x = _P3RX if _b[0] else _P3LX
            assert ('x="%d" y="%d" width="%d" height="%d"' % (_x, _b[1], _P3CW, _b[2])) in _svg_of(3), \
                "⑳ P3 的 3D 说话块在页上找不到：%r" % ((_m, _b),)
    # ④ 新入册两件：全双工的重叠区高亮 / 半双工的切换闸（3D 照着它们画）
    assert ('x="%d" y="%d" width="%d" height="%d"' % _P3LAP) in _svg_of(3), \
        "⑳ P3 的重叠区高亮在页上找不到：%r" % (_P3LAP,)
    for _g in _P3GATE:
        assert ('d="M%d %d H%d"' % (_g[0], _g[1], _g[2])) in _svg_of(3), \
            "⑳ P3 的切换闸在页上找不到：%r" % (_g,)
    assert all(_b[2] >= 44 for _bs in _P3BANDS.values() for _b in _bs), \
        "④ P3 的 A/B 块高有低于 44 的：%r" % [_b for _bs in _P3BANDS.values()
                                              for _b in _bs if _b[2] < 44]
    assert _P3CHW >= 4.0, "④ P3 方向通道半宽 %.1f < 4" % _P3CHW
    # ── ⑥ 三稿：八条通话流必须整束落在「卡盒之下、02 小标墨迹之上」──────────
    #    卡盒不是墨迹盒（_N16INK 只登记字形行框），所以这一条另立断言：
    #    卡底是 --card-bg 72% 不透明，车道钻到它底下就会被读成「卡里的毛刺」。
    _n16top = _n16_y(0) - _N16W
    _n16bot = _n16_y(_N16N - 1) + _N16W
    assert _n16top - _N16CARDB >= _ADD_CLR, \
        "⑥ P16 车道钻进卡盒了：束顶 %.1f 距卡盒底 %.0f 只有 %.1fpx（下限 %.0f）" % (
            _n16top, _N16CARDB, _n16top - _N16CARDB, _ADD_CLR)
    assert _n16top - _N16TABB >= _ADD_CLR and _N16LANDT - _n16bot >= _ADD_CLR, \
        "⑥ P16 车道没落在对照表与落点句之间：束 %.1f–%.1f vs [%d, %d]" % (
            _n16top, _n16bot, _N16TABB, _N16LANDT)
    assert _N16RECT[1] <= _n16top and _n16bot <= _N16RECT[1] + _N16RECT[3], \
        "⑥ P16 车道越出 lab-rect：%.1f–%.1f ∉ %r" % (_n16top, _n16bot, _N16RECT)
    # P8 的两根事件 x 与波形表：页上必须真出现（1px = 1ms 的换算靠它们成立）
    assert _P9CUT - _P9IN == 340, "⑳ P8 快路径跨度不是 340px（= 340ms）"
    # 数字红线：弧线不标延迟；示意分布必须挂小注
    _p21 = _sec_of(21)
    assert "节点分布示意" in _p21, "P21 缺「节点分布示意」小注 —— 228 枚节点不许当真实 PoP 清单"
    for _bad in ("ms 抵达", "毫秒抵达", "ms 延迟", "延迟 <", "RTT"):
        assert _bad not in _p21, "P21 弧线标了延迟数值：「%s」" % _bad

    # ── 同源自证：非 3D 的 20 页与引擎母本**逐字节**相同 ────────────────────
    #   这一条是 LAB 演绎的定义本身 ——「只加两页 3D，正文一个字节没动」。
    #   引擎产物不在身边（首次 clone / CI 顺序）时降级成 skip 并打一行警告，
    #   不 assert 挂掉整个构建（那会把 builder 变成对另一份产物的硬依赖）。
    if ENGINE_REF.exists():
        _eng = ENGINE_REF.read_text(encoding="utf-8")
        def _secs_of(h):
            out = {}
            for chunk in h.split('<section class="slide conf-boarded" data-p="')[1:]:
                out[int(chunk.split('"', 1)[0])] = chunk.split("</section>", 1)[0]
            return out
        _E, _L = _secs_of(_eng), _secs_of(doc)
        def _txt(h):
            return _re2.sub(r"\s+", " ", _re2.sub(r"<[^>]+>", " ", h)).strip()
        # ① 非 3D 页：**逐字节**同源（一个字节都没动）
        _same = [p for p in range(1, 23) if p not in LAB_RECTS]
        # ── ㉒ 加法层三页：把 .lab-stage 那一层摘掉之后必须与母本**逐字节**相同 ──
        #    这是全 deck 最硬的一条同源自证：另外 15 页只保证「逐字同文」（几何被裹进
        #    poster 组、片段分组变了），这三页保证**一个字节都没动**——
        #    3D 在这里是加法，加法层拿掉就是原来那一页。
        for _p in _ADD_PAGES:
            _peel = _L[_p].replace("  " + lab_stage(_p) + "\n", "", 1)
            assert _peel == _E[_p], \
                "㉒ P%d 摘掉加法层之后与母本不是逐字节相同 —— 3D 动了这一页的 DOM" % _p
        for _p in _same:
            assert _E[_p] == _L[_p], "LAB 与引擎母本在 P%d 上分叉（非 3D 页必须逐字节同源）" % _p
        # ② 3D 页：**逐字**同文 —— 3D 化只动「形」（几何被裹进 <g class="lab-poster">、
        #    多了一层 .lab-stage），DOM 文案 / kicker / SOURCE / data-step 一个字没改。
        #    这一条是「全量 3D 化」的定义本身：升维不是重写内容。
        # ── P2 白名单例外（表达力精进 · 第二波 0 · 与 P1「· LAB」/ P21 角注同一先例）──
        #   下排三条并行带原本一个标签都没有：读者分不出哪条是听 / 想 / 说，也没有
        #   与上排「听完再回答 ✕」对仗的 ✓。补的是**四枚字串**，一个不多：
        #     「听」「想」「说」（三枚 lane 标）+「边说边听 ✓」（下排判词）。
        #   例外写成断言而不是放行：把两边的文本节点序列逐枚对齐，LAB 多出来的
        #   那几枚必须**恰好等于**这张白名单（顺序也一致），多一个字就炸。
        _P2WL = list(_P2WL_DECL)

        def _toks(h):
            return [t for t in _re2.sub(r"<[^>]+>", "\x00", h).split("\x00")
                    if _re2.sub(r"\s+", " ", t).strip()]

        def _extra_of(_lt, _et):
            """LAB 相对母本多出来的文本节点（逐枚对齐 · 母本一枚都不许少）"""
            _lt = [_re2.sub(r"\s+", " ", t).strip() for t in _lt]
            _et = [_re2.sub(r"\s+", " ", t).strip() for t in _et]
            _i = _j = 0
            _ex = []
            while _i < len(_lt) and _j < len(_et):
                if _lt[_i] == _et[_j]:
                    _i += 1; _j += 1
                else:
                    _ex.append(_lt[_i]); _i += 1
            _ex += _lt[_i:]
            assert _j == len(_et), "母本有文本节点在 LAB 里对不上（第 %d 枚：%r）" % (_j, _et[_j])
            return _ex
        for _p in _INPAGE:
            if _p == 2:
                _ex2 = _extra_of(_toks(_L[2]), _toks(_E[2]))
                assert _ex2 == _P2WL, \
                    "P2 白名单例外被撑开了：多出来的是 %r，只准 %r" % (_ex2, _P2WL)
            else:
                assert _txt(_L[_p]) == _txt(_E[_p]), \
                    "P%d 正文与引擎母本分叉（3D 化只准动图形，不准动一个字）" % _p
            _sE = {m for m in _re2.findall(r'data-step="(\d+)"', _E[_p])}
            _sL = {m for m in _re2.findall(r'data-step="(\d+)"', _L[_p])}
            assert _sE == _sL, "P%d 的 data-step 步进语义分叉：%r vs %r" % (_p, _sL, _sE)
        _e1 = _txt(_E[1]).replace("DEEP DIVE · 深入讲解", "DEEP DIVE · 深入讲解 · LAB", 1)
        assert _txt(_L[1]) == _e1, "P1 正文与引擎母本分叉（只准 kicker 末段加 · LAB）"
        _GN = "节点分布示意 · 200+ 全球节点 · SD-RTN"
        _l21 = _re2.sub(r"\s+", " ", _txt(_L[21]).replace(_GN, "")).strip()
        assert _l21 == _txt(_E[21]), "P21 正文与引擎母本分叉（只准换盒子 + 加角注）"
        # ── 版式分歧名册 × 产物逐页对表（一处不多一处不少）────────────────
        #   几何 token = 页上所有 <rect>/<circle>/<path> 的 x/y/cx/cy/d 序列。
        #   3D 化本身**不改**这个序列（它只是把片段裹进 <g class="lab-poster">），
        #   所以序列一旦与母本不同，就一定是真的动了版式。
        def _geom(h):
            h2 = _re2.sub(r'<g class="lab-poster">|</g>', "", h)
            # ⚠ 必须带左边界：没有它，`id="labStage2"` 会被当成一处 d=（本轮踩过）
            return _re2.findall(r'\s(?:x|y|cx|cy|d)="[^"]*"', h2)
        _geomdiff = {p for p in range(1, 23) if _geom(_E[p]) != _geom(_L[p])}
        _declared = {p for p, k, _w in _DIVERGE if k == "geom"}
        assert _geomdiff == _declared, \
            "版式分歧名册对不上：产物实际分叉 %r，名册声明 %r" % (sorted(_geomdiff), sorted(_declared))
        assert len(_DIVERGE) == 7, "版式分歧应为 7 处，名册里有 %d 处" % len(_DIVERGE)
        # stage 行：P18 的舞台真的横跨了两图（母本那只 figbox 只有 1240 宽）
        assert LAB_RECTS[18][3] > 1240, \
            "版式分歧 stage 行不成立：P18 舞台宽 %d 没有横跨两图" % LAB_RECTS[18][3]
        # poster 行的针对性自证：P13 那块**不透明**模块板必须已经进了 poster 组
        # （母本里它是裸 <rect>；不进 poster 组就会把 3D 画进单元的小巧思全盖死）
        _p13 = _svg_of(13)
        _plate = ('fill:var(--card-bg-2)" x="%d" y="%d" width="%d" height="%d"'
                  % (_P13SLOT[0][0] + 14, _P13SLOT[0][1] + 12,
                     _P13SLOT[0][2] - 28, _P13SLOT[0][3] - 24))
        assert _plate in _p13, "⑥ P13 模块板的几何漂了（poster 分组分歧的对象找不到）"
        _pi = _p13.index(_plate)
        _pg = _p13.rfind('<g class="lab-poster">', 0, _pi)
        assert _pg >= 0 and _p13.find("</g>", _pg) > _pi, \
            "⑥ P13 模块板没有进 lab-poster 组 —— 它会把每一处 3D 小巧思盖死"
        assert _plate in _E[13] and '<g class="lab-poster">' not in _E[13], \
            "⑥ 引擎母本的 P13 不该有 poster 组（分歧的另一半不成立）"
        _twin = ("逐字节同源 %d 页 + 3D %d 页逐字同文（含 data-step 集合同源）· 版式分歧 %d 处"
                 % (len(_same), len(_INPAGE), len(_DIVERGE)))
    else:
        _twin = "⚠ 引擎产物不在身边，同源自证跳过"

    print("convoai-lab.html · %d 页 · %dKB · conf-light 默认 · 分步 %r"
          % (total, len(doc) // 1024, steps_map))
    print("  3D 场景 %d 枚（单渲染器巡游 · 全文档 1 枚 canvas）：%s"
          % (len(lab_map), " / ".join("P%d %s" % kv for kv in sorted(lab_map.items()))))
    print("  poster：声场球 %d 点 / 地球陆地 %d 点 · %d 节点 · %d 弧 · three r%s"
          % (VPOSTER["n"], GPOSTER["nLand"], GPOSTER["nNode"], len(GPOSTER["arcs"]), THREE_REV))
    print("  同源自证：%s" % _twin)
    print("  版式分歧名册：%s" % " / ".join("P%d·%s" % (p, k) for p, k, _w in _DIVERGE))
    print("  波A 速度表：A 档 %d 股 · %.1f–%.1f px/s · 极差 %.2f×（基准 %.0f ±%d%%）"
          % (len(_SPD_ALL), _spdlo, _spdhi, _spdhi / _spdlo, _SPD_A, int(_SPD_TOL * 100)))
    print("  P13 定点修复：转子净空 %.1fpx（下限 %.0f）· 包围盒 %r ⊂ 机腔 %r · "
          "贯通流 %.0fpx → 落点 x%d（发布槽右缘 %d）· 幅度 w%.0f/floor%.2f/ghost%.3f/λ%.0f"
          % (_K_CLR_MIN, _K_CLR, [round(v) for v in _K_ORB_BOX], list(_P13HUB),
             _plen(_P13FLOW), _fend[0], _sink,
             _K_FLOWW, _K_FLOWFLOOR, _K_FLOWGHOST, _k_flow_lam()))
    print("  三轮加法层：P5 底场 / P15 中心辐射 / P16 通话流 · "
          "净空 %s（下限 %.0f）· 摘层即母本（逐字节）"
          % (" / ".join("P%d %.1f" % (p, _ADD_CLRMIN[p]) for p in _ADD_PAGES), _ADD_CLR))
    print("  ⑥ P22 互动星系：三环 %d 点 @ s=%s · 半径 %s · %d 弧 / %d 股（λ%.0f · %dpx/s）· "
          "引线净空 %s（下限 %.0f）· 墨迹净空 %.1fpx · poster 1/%d 抽稀"
          % (_GX_N, _n(GX22["s"]),
             "/".join(_f1(v * GX22["s"]) for v in (_GX_CORE_R, _GX_IN_R1, _GX_OUT_R1)),
             _GX_ARCS, _GX_SN, _AS_LAM, int(_SPD_A),
             " / ".join("%.1f" % v for v in _GX22_LEAD), _GX_LEADCLR, _P22CLRMIN, 4))
    print("  表达力精进 ①②③：P2 舞台 470→%d（setViewOffset，剧场投影不动）· "
          "02 两排 %d 股（上排 %s / 下排 %s 三条 · λ%.0f）· 净空 %.1fpx｜"
          "P4 舞台起点 x%d（三行说明最右墨迹 %d + %d）· %s 圈两次交叉 · 净空 %.1fpx｜"
          "P11 SOURCE %d（land 独占 y988 一行）"
          % (LAB_RECTS[2][4], len(_SPD_P2B), _n(_SPD_P2B[0]),
             "/".join(_n(v) for v in _SPD_P2B[1:]), _AS_LAM, _P2CLRMIN,
             int(LAB_RECTS[4][1] + _D_X0), _p4r, int(_CLR[4]), _n(_D_TURNS), _P4CLRMIN,
             _P11SRCY))
    print("  表达力精进 · 二波 0④⑤⑥⑦：P2 下排补 %d 枚字（白名单 %s）｜"
          "P3 半双工 2 轮×%d 高 · 通道半宽 %s · 重叠区 %r + 闸 %d 段入册｜"
          "P5 三支流→集流带 %s→%s 半宽 · 收口箭头 x%d｜"
          "P16 %d 条并行通话流（间距 %s · 半宽 %s · 8 组确定性通话段）｜"
          "P15 迷你转子 %d 粒 · 外圈 %s×%s · 三环倾角 %s° · 支线半宽 %s→%s"
          % (len(_P2WL_DECL), "/".join(_P2WL_DECL),
             _P3BANDS["half"][0][2], _n(_P3CHW), _P3LAP, len(_P3GATESEG),
             _n(_X5CW0), _n(_X5CW1), int(_X5COLX[1]),
             _N16N, _n(_N16DY), _n(_N16W),
             _H15ORBN, _f1(_H15ORB[0][0]), _f1(_H15ORB[0][1]),
             "/".join(_f1(o[2]) for o in _H15ORB),
             _n(_H15W0), _n(_H15W1)))
    print("  波A 音频流：λ=%.0fpx @ %.0fpx/s ⇒ %.2fs 一次呼吸 · Σa=%.2f · P14 注光 %.0fpx/s "
          "⇒ 一轮 %.2fs（生长 %.2f + 停驻 %.2f + 收 %.2f）"
          % (_AS_LAM, _SPD_A, _AS_LAM / _SPD_A, sum(_AS_A), _Y_BEAM,
             _Y_CYC, _Y_GROW, _Y_HOLD, _Y_REL))

if __name__ == "__main__":
    build()
