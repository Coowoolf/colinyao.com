#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-info.py · 《声网对话式 AI · 一页一章 Infograph》拜访速讲版 deck
# CONF 家族 · conf-light 默认 · 单文件双主题 · 三线三色
#
# 2026-08-21 v2 重建（Colin 拍板「8 页全部按引擎 deck 家族语言重建，页数保持 8」）：
#   参考实现 = build-convoai-engine.py（家族当前最高标准，22 页）。本文件从它逐条继承
#   五运动原语 / 图形语言 / 版式纪律，**文案与数字一个不新造**——版式重构 ≠ 文案重写。
#   两处例外（Colin 指定）：
#     ① P2 四大数与来源标注改为与引擎 P21（Why Agora 口径锁页）逐字同源；
#     ② 各页新增「流的什么 / 为什么」短线标与图注（不引入新数字 / 新客户名 / 新产品声明）。
#
# 2026-08-23 精修轮（GPT 5.6 review 采纳项 · 已仲裁定案 · 本文件占 A/B/C/D/G 五项）：
#   A 抽屉主题**双向**同步：宿主补 storage 监听（iframe 写 localStorage → 宿主跟随），
#     引擎 builder 此项零改动。见 ENGINE_DRAWER_JS 里那一段注释。
#   B P5「96.5%」大数正下方补一行 cohort 标注「生产外呼 · n=2,475 · 未出现明确 AI 识别信号」
#     ——三段全部是本页既有词与数的重组，**漏斗与其余内容一格未动**。
#   C SOURCE ledger 统一成四段：`SOURCE · 来源 · 样本或时间窗 · 事实截止 2026.08`。
#     P2 原样（本来就是这个形状）；P4/P5/P6/P7/P8 各补一行，**只重排页内既有事实，
#     不新增任何来源 / 样本 / 定义细节**；缺的段就少写，缺口记进交付报告等 Colin 补。
#     P1 封面与 P3 矩阵没有事实声明 ⇒ 规格上就不带 SOURCE 行。
#   D P7 浅色生态图对比度再提 ~17%（只调滤镜数值；不加卡片 / 不加 blur / 不加遮罩，深色不动）。
#   G 投影小字提一档：.sig 与新类 .src 字号 15 → 17、色阶各上一格（与引擎 builder 逐字同源）。
#
# 结构（8 页 · 一页讲透一章；P4/P5/P7 各 1 步 presenter-controlled build）：
#   P1 封面 → P2 公司 → P3 矩阵 → P4 Engine → P5 Agent → P6 PhysicalAI → P7 案例 → P8 合流
#
# ── 家族语言硬指标（逐条继承自引擎 deck，改本文件之前先读完）───────────────
#   · 五运动原语（flow-packet / dash-drift / pulse / breathe+halo / cycle）逐字复用，
#     **不新造 keyframe 名**（qa-motion 有拼写闸）；相位接力用 animation-delay 组合完成。
#   · 动效纪律四条：动效件不携带文字 / 非当前页 animation-play-state:paused /
#     prefers-reduced-motion + print 全关 / 100% 帧 = 静态原图（pinned-diff 逐像素自证）。
#   · P8 质量语言六条：类型化线 + 真线样迷你图例 / 每页唯一 hot 件 / 每条线带
#     「流的什么·为什么」标注 / 闭环·分叉·旁路优先 / 已核定数字带时序标 / 细虚线域分带。
#   · packet 只在盒间接头跑且相位对齐；环形几何不 transform 旋转，用 dash 绕圈。
#   · **任何常显容器不挂 data-step**（引擎 P20 空页事故根因：motion.css 的裸容器兜底
#     规则会把它在 step0 摁成 opacity:0 = 白页）。步进用真正的步进件承载。
#
# ── 踩过的坑（移植 SVG 必守）─────────────────────────────────────────────────
#   · svg 一律 style="width:100%;height:auto"，且 .sh 高度 = width×viewBoxH/viewBoxW，
#     否则 stage.css 的 svg{max-height:100%} 会把图压扁 / .sh 装不下会被 clip-path 切掉
#   · .dw 的 --len 必须≈路径长度，否则线不出来；虚线不能走 .dw（dasharray 会被压掉）
#   · SVG 里换色一律写内联 style="fill:…"，呈现属性 fill= 压不过 .fig .lbl/.ttl 的 CSS fill
#   · components.css 的 b,strong{color:var(--ink)} 会压继承色，深色面板里的 b 要 color:inherit
#   · img{max-width:100%;max-height:100%}（stage.css）会咬放大图 —— 图窗一律 object-fit
#   · .pp .sh{overflow:visible}（0,2,0）：需要裁切时写 .pp .sh.CLASS{overflow:hidden}
#   · content 背景板自带一条 accent 细线在 y848–852（x120–761）：那一带不放文字，
#     rule(850) 正好压住它当收口线；收口线之下是页脚带（引擎 P19 先例）
#
# ── 口径红线（build() 里有构建期反向断言，别等到 qa）─────────────────────────
#   · 不出价格（8,500 / 2,999 / 5,501）· 不出 staging URL
#   · 「盲测」「32,000」不得出现：那是引擎 P16 的 Call Agent 盲测口径，
#     本 deck P5 的 96.5% 是 2,475 通**生产**口径 —— 两个数据集严禁混写
#   · 案例墙 14 家客户名逐字（qa-convoai-info.mjs 有硬编码名单闸）
#
# 重建：python3 scripts/build-convoai-info.py
# 自检：node scripts/qa-convoai-info.mjs（THEME=dark 二跑）
#       DECK=info node scripts/qa-motion.mjs
#       DECK_URL=…/convoai-info.html node scripts/occlusion-scan.mjs
# ═══════════════════════════════════════════════════════════════════════════
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
OUT = ROOT / "public" / "decks" / "convoai-info.html"
A = "/decks/assets/convoai/"
B = "/decks/assets/conf-boards/"
R26 = "/decks/assets/robot26/"

# ── P1 封面主视觉：**声场球 orb（默认）** 与 AI-art 位图二选一 ────────────────
#   两者占的是同一块地（art 盒 left720..1920 / top220..895 与球的极值轮廓
#   x1322–1788 / y345–811 完全重叠），而 3D 舞台在文档序上压在 hero-art 之上 ——
#   同时开只会把位图糊掉。所以这是一枚**互斥**开关，不是叠加：
#     INFO_P1=orb（默认）3D 声场球 · 无 .hero-art
#     INFO_P1=art        AI-art 位图 · P1 不入场景表（终审对比版）
#   两版的其余 7 页逐字节相同。
P1_MODE = os.environ.get("INFO_P1", "orb")
assert P1_MODE in ("orb", "art"), "INFO_P1 只认 orb / art：%r" % P1_MODE
HERO_ART = (P1_MODE == "art")

# ── P6「让对话，走出屏幕。」加法层开关（第二波 · 必须可一键关闭）────────────────
#   本 deck 前六枚场景全是**替换**（3D 坐在页上那张 SVG 原来的位置上）；这一枚是
#   全 deck 唯一的**加法层**：标题右侧那条空带上本来什么都没有，3D 是标题的插图。
#   加法层的净空走 lab 的 16px 规则（不走「不许比 2D 更近」的平手规则）。
#     INFO_P6=exit（默认）上场景 · P6 进 LAB_RECTS · 页上多一枚无字的 poster figbox
#     INFO_P6=off        不进 LAB_RECTS · P6 与 a053ebc 逐字节相同
INFO_P6 = os.environ.get("INFO_P6", "exit")
assert INFO_P6 in ("exit", "off"), "INFO_P6 只认 exit / off：%r" % INFO_P6
P6_EXIT = (INFO_P6 == "exit")

AC = "var(--accent)"
AD = "var(--accent-deep)"
HS = "var(--hair-strong)"
LE = "var(--l-eng)"
LA = "var(--l-agent)"
LP = "var(--l-phys)"


def css(name):
    return (SRC / name).read_text(encoding="utf-8")


FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>"""

# ── 背景板（速讲版只用两张：title 给 P1 / content 给其余）─────────────────────
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

# ═══════════════════════════════════════════════════════════════════════════
# LAB 层 · three.js 语义 3D 升维（2026-09-01 · convoai-info 整体重构）
# ───────────────────────────────────────────────────────────────────────────
#   Colin：「按一样的逻辑去整体重构一下 convoai-info。」
#   —— 把 convoai-lab 那一整套 LAB 工艺（语义 3D / 单渲染器巡游 / 流质铁律 /
#      降级链 / 四条验收红线）搬到速讲版上。**基建一行都不重写**：
#      lab-kit、单渲染器巡游 TOUR、降级链、poster 分件刀 `_lpsplit` 全部
#      从 `scripts/build-convoai-lab.py` **现取**（见 `_LAB` / `_cutmod`）——
#      单一真相在旗舰那边，这里只写本 deck 的语义几何。
#
# ── info 与 lab 的身份差别（本层每一处取舍的理由）─────────────────────────
#   ① **浅色默认**：`colin-theme` 无值时是浅底（速讲 / 微信转发场景）。
#      浅底走正常混合（--x-add:0）、暗底走加色混合（--x-add:1） ⇒ 浅色中间调
#      天然容易塌。本层的浅色档参数按 lab 波B 的教训**预先校足**，
#      并由 qa 的 ⑳ink 闸逐页量「浅/暗墨量比 ≥0.9」。
#   ② **降级链是生命线**：客户会在各种设备上打开（禁 WebGL / reduced-motion /
#      print / 离线归档四条路），8 页必须完整可读。所以每一枚场景都**替换**
#      页上原有的一张 SVG 图 —— poster 就是那张图本人，起不来就是原来的 2D 版。
#      本 deck **没有加法层**（lab 的 P5/P15/P16/P22 那一类）：速讲版页面本就密，
#      版面之外没有可加场的空档（P2 的实测见 lab_data 的注）。
#   ③ **抽屉不动**：引擎抽屉仍指 `convoai-engine`（2D 正装）——速讲现场展开要
#      秒开，不该等 750KB three.js。这是既定判断，见本轮 commit message。
#
# ── 逐页语义审查（8 页 · 一页一判）───────────────────────────────────────
#   P1 封面        → 声场球（lab P1 血统：谐波行波驱动点云球面呼吸 · 波峰上色）
#   P2 公司        → 发布时间线**活动带**（audioStream 沿时间轴 · 5 个里程碑为节点脉冲）
#                    ⚠ 地球：**停手**。P2 上最大的一块无字矩形是 820×96（03 右下），
#                      放得下的球直径 96px —— 比同页「No.1」的字还小，那是装饰不是语义。
#                      要地球就得动 DOM 坐标，本轮纪律不许。见交付报告。
#   P3 矩阵        → 空间生长（底座 = 纵深基面 · 三条产品线从底座抽出向上 · 辅件入景深）
#   P4 ENGINE      → 发版活动带（audioStream 沿时间轴 · 17 次发版为带上的节点脉冲）
#   P5 AGENT       → Agent 骨架（四件能力模块环绕运行时核 · 安全是包住全部的虚线域）
#   P6 PHYSICAL AI → **维持 2D**（R1 实拍照片页 —— 照片就是照片，与 lab P19 同一判断）
#   P7 案例        → **维持 2D · 停手**。eco 五层主视觉是定稿资产，而且它是 .pp 里的
#                    一枚 <img>；3D 舞台按家族层序坐在 .pp **之下**，canvas 会被底图
#                    整幅盖住 —— 要让流看得见就只能把 canvas 抬进 .pp 压在定稿底图之上，
#                    那正是历史指令明令禁止的。结构性冲突，不是口味问题。见交付报告。
#   P8 合流        → 三条空间支流汇入 ONE NET 主河道（本 deck 的标杆页 · 投入最高）
# ═══════════════════════════════════════════════════════════════════════════
import importlib.util as _ilu
import re as _re2

# ── 从旗舰 builder 现取地基（**不改它一个字节**）──────────────────────────
_LAB_SPEC = _ilu.spec_from_file_location("_convoai_lab", ROOT / "scripts" / "build-convoai-lab.py")
_LAB = _ilu.module_from_spec(_LAB_SPEC)
_LAB_SPEC.loader.exec_module(_LAB)


def _cutmod(a, b=None, head=True):
    """按锚点从 lab 的运行时里切一段出来（锚点缺失 = 旗舰改了结构 ⇒ 当场炸，
       绝不静默分叉）。head=True 时把锚点**之前**那一段 `/* ═` 大注释一起带走 ——
       注释是这套地基的一部分，照抄就连注释一起抄。"""
    src = _LAB.LAB_MODULE_BODY
    i = src.index(a)
    if head:
        j = src.rfind("\n/* ═", 0, i)
        assert j > 0, "lab 运行时里 %r 前面没有大注释块 —— 旗舰改了结构" % a
        i = j
    if b is None:
        return src[i:]
    k = src.index(b)
    if head:
        k2 = src.rfind("\n/* ═", 0, k)
        assert k2 > 0, "lab 运行时里 %r 前面没有大注释块" % b
        k = k2
    assert k > i, "切片区间反了：%r … %r" % (a, b)
    return src[i:k]


# lab-kit ①②③④（主题色桥 / 缓动 / 折线工具 / px 场景材质）——「场景 registry」之前的全部
_K_BASE = _cutmod("import * as THREE from 'three';", "function makeVoice(ctx){", head=False)
_K_BASE = _K_BASE[:_K_BASE.rfind("\n/* ═")]        # 尾巴那段大注释归 _K_VOICE，不许重复一遍
# v3：P2 换成 SD-RTN 地球 ⇒ OrbitControls 那枚外链**留着**（makeGlobe 现取，它要用）。
# 全路径外链，不进 importmap（旗舰同写法）。
assert "import { OrbitControls } from '/decks/assets/three/OrbitControls.js';" in _K_BASE
_K_VOICE = _cutmod("function makeVoice(ctx){", "function makeGlobe(ctx){")
_K_GLOBE = _cutmod("function makeGlobe(ctx){", "function makeBrain(ctx){")   # ② SD-RTN 地球
_K_BRAIN = _cutmod("function makeBrain(ctx){", "function makeShell(ctx){")  # ③ 五脑区大脑（P5）
_K_DUPLEX = _cutmod("function makeDuplex(ctx){", "function mkLock(w, h, D){")  # ⑦ 双向声带（P4）
_K_LOCK = _cutmod("function mkLock(w, h, D){", "const AS = K.as;")          # ⑤ 投影锁套件
_K_AS = _cutmod("const AS = K.as;", "const MO = K.o;")                      # ⑨ audioStream
_K_CLR = _cutmod("function unlock(w, h, D, rect){", "const QT_VS = [")      # ㉒ 净空三小件
_K_TOUR = _cutmod("const CANVAS = document.getElementById('labGl');")       # 单渲染器巡游
for _need, _in in (("function mkStream(SH, pts, opt)", _K_AS),
                   ("function mkLock(w, h, D)", _K_LOCK),
                   ("function extrudeBack(", _K_LOCK),
                   ("function geoClr(geo, U, ink, pad)", _K_CLR),
                   ("function camPx(w,h,D)", _K_BASE),
                   ("function camSphere(w,h,C)", _K_BASE),
                   ("const controls = new OrbitControls(camera, ctx.canvas);", _K_GLOBE),
                   ("function ribbonGeo(pts, halfW, uv, dirs)", _K_BASE),
                   ("grp.rotation.y = SWAY*Math.sin(TAU*clock/B.swayP);", _K_BRAIN),
                   ("const A = lane( 1, 0), B = lane(-1, Q.phase);", _K_DUPLEX),
                   ("TOUR.pace = function(fps)", _K_TOUR)):
    assert _need in _in, "lab 地基件缺失：%s" % _need
# 地球的 K 表常量（位掩码陆地 / 示意节点 / 取道表 / 三组弧相位）—— 模块常量现取，
# 一个数都不在本文件里重写；poster 也直接用旗舰算好的那一份 `_LAB.GPOSTER`。
_G_KEYS = ("LAND_BITS", "LAND_N", "NODE_TABLE", "ROUTE_TABLE",
           "ARC_DUR_S", "ARC_GAP_S", "ARC_OFF_S", "GPOSTER", "GCAM",
           "GGR", "GCX", "GCY", "GTILT", "GY0", "GSPIN", "GINTRO")
# 波B：双向声带（P4）/ 五脑区大脑（P5）的图形与常量同样**整块现取**——
# 2D 图（`_duplex_lanes` / `_brain_fig`）、几何常量、K 表构造式全部来自旗舰，
# 本文件只提供矩形与版式。矩形与 lab 逐字同参 ⇒ K 表连重算都不用。
_B_KEYS = ("_duplex_lanes", "_brain_fig", "_LANES", "_XIN", "_XNOW",
           "_D_X0", "_D_X1", "_D_YC", "_D_AMP", "_D_DEP", "_D_TURNS", "_D_PHASE", "_D_N",
           "_SPD_P4", "_d_lane", "_plen", "_dur_at", "_P4INK",
           "_BRAIN", "_ZONES", "_LEADS", "_ARCS", "_ARC_EXTRA", "_BRAIN_IN",
           "_CEREB", "_STEM", "_SUL1", "_SUL2", "_SUL3", "_EXTREMES",
           "_obj", "_arr", "_n", "_poly", "_polym", "_bbox", "_sec", "legend")
for _k in _G_KEYS + _B_KEYS:
    assert hasattr(_LAB, _k), "lab 常量 / 组装件缺失：%s" % _k

# ── ⑦ 走出屏幕（P6 · 加法层）· 几何全部是新写的（页上本来没有图）──────────────
#   语义：标题「让对话，走出屏幕。」的**图解**，不是装饰。
#     · 一只**锁在版面上的屏幕**：外框（bezel）+ 内屏框 + 一块微亮的屏面 ——
#       三件一起才读成「屏幕」；只画一圈细线框会读成一扇门 / 一枚手机图标（一稿的病）。
#       前框 z=0、后框 −60 且内缩 4，lockBox 写法同 P5 ⇒ 屏上落点由构建期定死，
#       深度只管雾与遮挡。
#     · 一条 audioStream 从**屏面里**（z=−140）出发，横穿整只屏、过框右缘，
#       一路朝观众爬到 z=+36，半宽 3.6 → 9 ⇒「越走越近、越走越宽」。
#       介质与全家族同一种（λ=232、屏上 110px/s）。
#     · 框内那一段用 gain 压到 .50（屏幕里的声音是闷的 —— 但**必须看得见**：
#       一稿压到 .35 且只有 26px×半宽2.5，帧上等于没有，故事只剩「框边冒出一条流」），
#       过了框右缘用 smoothstep 在 60px 弧长里放开到 1.0。
#   坐标账（figure = 舞台像素，vb 与盒同宽 ⇒ ×1；局部坐标 = 舞台 − (740,140)）：
#     外框 局部 (52,8,56,84) = 舞台 (792,148)–(848,232)
#       距 kicker 字形行底 y115（.sh 盒底 y120）33px · 距 R1 卡顶 y268 36px ·
#       距主标右缘 x719.7 72.3px —— 加法层的 16px 规则三面都过。
#     内屏框 = 外框内缩 5（rx 6）= 舞台 (797,153)–(843,227)；屏面填色同此范围。
#     流 局部 (60,50,−140) →(108,50,−30) →(1020,50,+36) = 舞台 x800→848→1760、y190
#       框内可见段 48px（其中 ~40px 在渐隐之后满不透明），峰值半宽 9px ⇒
#       带边 181–199，仍在矩形 y140–240 之内。
_EX_RECT = (740, 140, 1060, 100)
_EX_D, _EX_HALF = 1200.0, 300.0
_EX_BOX = (52.0, 8.0, 56.0, 84.0)         # 屏幕外框 / bezel（局部坐标）
_EX_R = 8.0                               # 外框 rx（poster 与 3D 同一个数）
_EX_R2 = 6.0                              # 内屏框 rx
_EX_ZBOX, _EX_DZBOX, _EX_INS = 0.0, 60.0, 4.0
_EX_INS2 = 5.0                            # 内屏框 / 屏面相对外框的内缩
_EX_P0 = (60.0, 50.0, -140.0)             # 源头：屏面里（舞台 x800，内屏框之内 3px）
_EX_P1 = (108.0, 50.0, -30.0)             # 外框右缘（舞台 x848）—— uFrame 的取样处
_EX_P2 = (1020.0, 50.0, 36.0)             # 末端：朝观众来到 +36
_EX_N0, _EX_N1 = 16, 105                  # 两段折线的取样数（合成后 120 点）
_EX_W0, _EX_W1 = 3.6, 9.0                 # 半宽：源头 → 末端（探针 / pad 保守取 9.0）
_EX_FLOOR = _LAB._AS_FLOOR                # .30（媒体流永不掐断 —— 全局档，不分叉）
# 接头渐隐：全局档 .055 在这条流上等于 55px **世界**弧长，而「框内那一段」的世界弧长
# 只有 92px —— 渐隐会把屏里的流吃掉大半。收到 .03（30px 世界弧长 ⇒ 页上 x800→808）：
# 屏里剩下 40px 满不透明的**闷带**，出框那一刻才放开。
# 末端同样只收 30px，正好收在页上那枚 ah_r 箭头之前。
_EX_EDGE = 0.03
_EX_G0, _EX_GSPAN = 0.50, 60.0            # 框内幅度 / 出框之后放开的弧长
_EX_XFRAME = _EX_BOX[0] + _EX_BOX[2]      # 框右缘 x=108（局部）⇒ uFrame 的取样处
_EX_DOT = (_EX_XFRAME, 50.0, 0.0)         # 出口那一枚点（meet 写法：aH = 该处包络）

# ── 舞台位表（每个 3D 页的图形区矩形 · 舞台坐标 1920×1080）─────────────────
#   矩形 = 该页 2D 图形所占的那块地，**不是整屏** ⇒ 3D 形与它替换掉的 SVG 形
#   逐像素同位，页上其余的字全部压在 canvas 之上（canvas 坐在 .pp 之下）。
#   ⚠ 本 deck 的 figbox 有两处 vbw ≠ 盒宽（P2 1620/1680、P5 840/820），
#     所以 figure 坐标 → 舞台像素**有缩放**（见各页的 _S2 / _S5）。
LAB_RECTS = {
    1: ("voice",  1305,  328,  500,  500),   # 球心 (1555,578) 居中 —— 与 lab P1 逐字同参
    # v3：P2 换成 **SD-RTN 地球**（lab P21 的矩形逐字同参：球心 (1470,500) 居中，
    # 弧顶 1.243r=310.75 仍在 320 半宽之内）。左栏四大数占 x120–1050，与球留 100px。
    2: ("globe",  1150,  180,  640,  640),
    3: ("grow",    120,  272, 1680,  600),   # v3 全舞台 = figbox(120,272,1680, vb1680×600)
    # v3 波B：P4 / P5 换成 lab 的双向声带与五脑区大脑，**矩形与 lab 逐字同参** ⇒
    # K 表 / 净空账 / 流速账连重算都不用（图也是 `_duplex_lanes` / `_brain_fig` 现取）。
    4: ("duplex",  120,  268, 1680,  352),   # = lab P4 · figbox(120,268,1680, vb1680×352)
    5: ("brain",   120,  282, 1680,  580),   # = lab P17 · figbox(120,282,1680, vb1680×580)
    # ⑦ 加法层（第二波）：标题右侧那条空带 —— 页上本来没有图，vb 与盒同宽 ⇒ ×1
    6: ("exit",    740,  140, 1060,  100),
    # v3 波C：P7 换成 **14 家 3D 星座墙**（新场景）· figbox(120,272,1680, vb1680×560)
    7: ("wall",    120,  272, 1680,  560),
    8: ("river",   120,  272, 1680,  420),   # v3 全舞台 = figbox(120,272,1680, vb1680×420)
}
if P1_MODE == "art":                       # 对比版：封面让给位图，P1 不入场景表
    del LAB_RECTS[1]
if not P6_EXIT:                            # INFO_P6=off：P6 回到 a053ebc 的样子
    del LAB_RECTS[6]
LAB_PAGES = sorted(LAB_RECTS)
# v3 波C 起：八页里七页有场景（P7 的五层生态图搬进细节层，主图换成 3D 星座墙 ——
# 「底图是 .pp 里的 <img>、舞台会被整幅盖住」那条结构性冲突随之消失：
# 星座墙自己就是主图，eco 图退到面板里）。P6 的实拍照片仍然是照片 ——
# 加法层不碰它，3D 落在**标题右侧的空带**上，与两张卡一格不相干。
FLAT_PAGES = [] if P6_EXIT else [6]

# ── poster 分件刀：形进 <g class="lab-poster">，字原位留在 DOM ──────────────
#   `lp` / `_lpsplit` 逐字取自旗舰（判据两条：片段里出现 `<text` ⇒ 带字的；
#   `<polygon` ⇒ 箭头头，它是方向标注，留在 canvas 之上正好钉住每条 3D 线的流向）。
#   `_LP_TRACE` 记下每一次包装的净荷 —— build() 末尾的同源自证要用它。
_LP_TRACE = []


def lp(*parts):
    body = "".join(parts)
    _LP_TRACE.append(body)
    return '<g class="lab-poster">%s</g>' % body


def _unwrap_poly(html):
    """借来的旗舰图（`_duplex_lanes` / `_brain_fig`）里，箭头头是**裹在**
       `<g class="lab-poster">` 之内的 —— 旗舰的闸门只管「poster 里没有字」。
       本 deck 的规矩更严一档：箭头头是**方向标注**，必须留在 canvas 之上钉住流向
       （⑲a 正面断言 poster 组里零 polygon）。所以这里过一道刀：把每个 poster 组里的
       `<polygon …/>` 提出来、原样接在该组之后 —— 画面一格不变（同一份 SVG 绘制序），
       只是它不再随 poster 一起淡出。
       `</g>` 要配对着找：旗舰的 poster 组里有 `<g clip-path=…>` 嵌套（P5 的脑）。"""
    out, i, tag = [], 0, '<g class="lab-poster">'
    while True:
        j = html.find(tag, i)
        if j < 0:
            out.append(html[i:])
            break
        out.append(html[i:j])
        k, depth = j + len(tag), 1
        while depth:
            a = html.find("<g", k)
            b = html.find("</g>", k)
            assert b >= 0, "poster 组没有闭合"
            if 0 <= a < b:
                depth += 1
                k = a + 2
            else:
                depth -= 1
                k = b + 4
        body = html[j + len(tag):k - 4]
        polys = _re2.findall(r"<polygon\b[^>]*/>", body)
        for q in polys:
            body = body.replace(q, "", 1)
        out.append(tag + body + "</g>" + "".join(polys))
        i = k
    return "".join(out)


def _lpsplit(items, keep=()):
    out, buf = [], []
    for it in items:
        if it in keep or "<text" in it or "<polygon" in it:
            if buf:
                out.append(lp(*buf))
                buf = []
            out.append(it)
        else:
            buf.append(it)
    if buf:
        out.append(lp(*buf))
    return "".join(out)


def lab_garage():
    """车库：单枚 canvas 的常驻位（页面上唯一一块 WebGL 画布 · 屏外零成本）"""
    return ('<div class="lab-garage" id="labGarage" aria-hidden="true">'
            '<canvas class="lab-canvas" id="labGl" width="16" height="16"'
            ' data-lab-canvas="1" data-lab-mode="BOOT" data-lab-run="0"'
            ' data-lab-page="0" data-lab-scene="" aria-hidden="true"></canvas></div>')


LAB_PRELUDE = _LAB.LAB_PRELUDE          # ① classic 前奏 + FPS 探针位 + importmap

# ═══ LAB CSS ═══════════════════════════════════════════════════════════════
#   变量段是本 deck 自己的（六枚前缀），**舞台 / poster / 降级语域那一段逐字取自
#   旗舰**（`/* ── 舞台层` 起到文件末尾）—— 层序、poster 淡出规则、print 与
#   reduced-motion 四条降级路，一个字都不重写。
#
#   ── 浅色档的定标法（lab 波B 的教训，写在这里免得下轮又踩）───────────────
#   暗底走加色混合：一层压一层越叠越亮，所以不透明度可以给得低。
#   浅底走正常混合：同样的不透明度叠在纸白上只会越叠越**灰**，中间调直接塌掉。
#   ⇒ 浅色档一律：① 主色改用 --ink / --accent-deep（纸面上的墨，不是荧光）；
#                 ② 不透明度整体上抬 1.3–1.6×；③ 点径 / 带宽略粗一档。
#   出稿前由 qa 的 ⑳ink 闸逐页实测 `TOUR.shot().ink` 的浅/暗比，目标 ≥0.90。
_LAB_TAIL = _LAB.LAB_CSS[_LAB.LAB_CSS.index("/* ── 舞台层"):]
assert _LAB_TAIL.endswith("</style>")
# 星座墙 poster 的卡框（本 deck 自己的一枚 —— 旗舰没有贴图场景，没有对应的画法）
_LAB_TAIL = _LAB_TAIL.replace(
    "</style>",
    ".w-rim{fill:none;stroke:var(--w-rim);stroke-width:1.2;"
    "opacity:var(--w-poster-rim,.42);}\n</style>")


def _lab_gvars(a, b, need=()):
    """借来的场景，材质 token 也**从旗舰现取**（一处改两处一起动）：从 lab 的
       :root / dark 两段里按注释锚点切下那一小块，一个数都不在本文件里重抄。"""
    s = _LAB.LAB_CSS
    i = s.index(a)
    j = s.index(b, i)
    out = s[i:j]
    for k in need:
        assert k in out, "lab 的 token 块改结构了：切不到 %s" % k
    return out


_G_LIGHT = _lab_gvars("  /* ── 地球 · 浅底", "  /* ── ③ 大脑点云", ("--g-ocean", "--g-poster-node"))
_G_DARK = _lab_gvars("  /* ── 地球 · 暗底", "  /* ── 大脑 · 暗底", ("--g-ocean", "--g-poster-node"))
# 波B：大脑（--b-*）与双向声带（--d-*）两块 token 同样从旗舰整块切取
_B_LIGHT = _lab_gvars("  /* ── ③ 大脑点云", "  /* ── ④ 双层防御壳", ("--b-ink", "--b-atmo-int"))
_B_DARK = _lab_gvars("  /* ── 大脑 · 暗底", "  /* ── 防御壳 · 暗底", ("--b-ink", "--b-atmo-int"))
_D_LIGHT = _lab_gvars("  /* ── ⑦ 全双工双向声带（P4）· 浅底", "  /* ══ 第二波 · 九枚场景", ("--d-up", "--d-add"))
_D_DARK = _lab_gvars("  /* ── 双向声带 · 暗底", "  /* ══ 第二波 · 九枚场景 · 暗底", ("--d-up", "--d-add"))

LAB_CSS = """<style id="convoai-info-3d">
:root{
  /* ── ① 声场球（P1 封面）· 浅底 ──
     几何 / 谐波 / 自转与 lab P1 **逐字同参**（球心 / 半径 / VHARM / VSPIN 全部现取）；
     **浅色墨量档 info 专属**：lab 暗底默认、浅色是副档，info 正好相反 —— 速讲版默认
     浅底，黑点一多就把波峰的粉压没了。所以这一档按「点少一档、粉重一档」重新定标：
     dot-op .94→.82 · dot-size .0138→.0128（墨量下来）/ hot-gain .40→.55 ·
     hot1 .70→.78（波峰上去）。暗档一个字不动。⑳ink 浅/暗比目标 1.20–1.40。 */
  --v-ink:var(--ink);      --v-dot-op:.82;  --v-dot-size:.0128; --v-dot-min:1.1;
  --v-hot:var(--accent);   --v-hot0:.18;    --v-hot1:.78;  --v-hot-gain:.55;
  --v-wire:var(--ink);     --v-wire-op:.40;
  --v-back:.46;            --v-add:0;
  --v-atmo:var(--accent);  --v-atmo-int:.06;
  --v-poster-dot:2.8;
""" + _G_LIGHT + """  /* ── ③ 空间生长（P3）· 浅底 ── */
  --gw-base:var(--accent);      --gw-base-op:.90;
  --gw-deck:var(--accent-deep); --gw-deck-op:.46;
  --gw-rib:var(--ink-3);        --gw-rib-op:.52;
  --gw-box:var(--ink-2);        --gw-box-op:.72;
  --gw-aux:var(--ink-3);        --gw-aux-op:.50;
  --gw-e:var(--l-eng);          --gw-a:var(--l-agent);  --gw-p:var(--l-phys);
  /* 三股主干的 RMS 实芯**各自本色**（浅底上三条一律 accent-deep = 三条都读成粉，
     「三条产品线」当场丢失）—— 与 P8 支流同一病同治，见 --rv-*-rms。 */
  --gw-e-rms:var(--accent-deep); --gw-a-rms:#3b6ae6;    --gw-p-rms:#5a41e6;
  --gw-flow-op:.70;             --gw-rms-op:.76;
  --gw-add:0;
""" + _D_LIGHT + _B_LIGHT + """
  /* ── ⑥ 三条支流一条河（P8 · 标杆）· 浅底 ── */
  --rv-main:var(--accent);      --rv-main-op:.72;
  --rv-rms:var(--accent-deep);  --rv-rms-op:.78;
  --rv-e:var(--l-eng);          --rv-a:var(--l-agent);  --rv-p:var(--l-phys);
  /* 三条支流的 RMS 实芯**各自本色** —— 原来三条一律 accent-deep，浅底上
     Agent（蓝）/ Physical AI（紫）两条从源头起就读成粉，「三条」当场丢失。
     2D 版的 packet 本来就是各自本色（packet(…, col=col)），3D 不许比 2D 退。
     主河道不动（粉 = ONE NET，它才是那一条）。 */
  --rv-e-rms:var(--accent-deep); --rv-a-rms:#3b6ae6;    --rv-p-rms:#5a41e6;
  --rv-trib-op:.78;             --rv-trib-rms-op:.80;
  --rv-bed:var(--accent);       --rv-bed-op:.34;
  --rv-rail:var(--accent);      --rv-rail-op:.88;
  --rv-meet:var(--accent);      --rv-meet-op:1;   --rv-meet-size:14;
  --rv-src:var(--ink-2);        --rv-src-op:.92;  --rv-src-size:20;
  --rv-add:0;
  /* ── ⑦ 走出屏幕（P6 · 全 deck 唯一的加法层）· 浅底 ──
     媒介与全家族同一种（audioStream · λ232 · 110px/s）；峰值色取 Physical AI 页的
     紫（--l-phys），RMS 实芯浅底给一档更深的紫（纸面上要有墨，不能是荧光）。
     屏幕框是版面上的一只**锁**（--ink-3）：它不参与流，只被穿过。 */
  --ex-frame:var(--ink-3);      --ex-frame-op:.85;
  --ex-inner-op:.55;                              /* 内屏框：比外框退一档 */
  --ex-screen:var(--l-phys);    --ex-screen-op:.07;   /* 屏面：微亮，不是一块色 */
  --ex-flow:var(--l-phys);      --ex-flow-op:.70;
  --ex-rms:#5a41e6;             --ex-rms-op:.74;
  --ex-dot:var(--ink-2);        --ex-dot-op:.92;  --ex-dot-size:8;
  --ex-add:0;
  /* ── ⑧ 14 家星座墙（P7）· 浅底 ──
     卡是**贴图**不是线稿：主色不参与，只有「多亮」与「多远退多少」两档。
     深度雾走不透明度（clearAlpha=0 ⇒ 退下去就是让纸面透出来），
     后排最深的一张退到 .97×(1−.26) = .72 —— 看得清是哪一家，又明显在后面。 */
  --w-card-op:.97;   --w-fog:.26;
  --w-rim:var(--ink-3);  --w-rim-op:.55;
  --w-poster-rim:.42;
}
html[data-theme="dark"]{
  --v-ink:var(--ink-2);    --v-dot-op:.84;  --v-dot-size:.0120; --v-dot-min:1.1;
  --v-hot:var(--accent);   --v-hot0:.16;    --v-hot1:.66;  --v-hot-gain:.80;
  --v-wire:var(--ink);     --v-wire-op:.22;
  --v-back:.26;            --v-add:1;
  --v-atmo:var(--accent);  --v-atmo-int:.17;
  --v-poster-dot:2.6;
""" + _G_DARK + """  --gw-base:var(--accent);      --gw-base-op:.92;
  --gw-deck:var(--accent-deep); --gw-deck-op:.26;
  --gw-rib:var(--ink-3);        --gw-rib-op:.36;
  --gw-box:var(--ink-3);        --gw-box-op:.62;
  --gw-aux:var(--ink-3);        --gw-aux-op:.34;
  --gw-e:var(--l-eng);          --gw-a:var(--l-agent);  --gw-p:var(--l-phys);
  /* 暗底实芯本来就是白芯 —— 身份由**峰值色**承担（uColor = --gw-e/a/p），保持 */
  --gw-e-rms:var(--ink);        --gw-a-rms:var(--ink);  --gw-p-rms:var(--ink);
  --gw-flow-op:.50;             --gw-rms-op:.55;
  --gw-add:1;
""" + _D_DARK + _B_DARK + """
  --rv-main:var(--accent);      --rv-main-op:.62;
  --rv-rms:var(--ink);          --rv-rms-op:.58;
  --rv-e:var(--l-eng);          --rv-a:var(--l-agent);  --rv-p:var(--l-phys);
  /* 暗底实芯本来就是白芯 —— 身份由**峰值色**承担（uColor = --rv-e/a/p），保持 */
  --rv-e-rms:var(--ink);        --rv-a-rms:var(--ink);  --rv-p-rms:var(--ink);
  --rv-trib-op:.56;             --rv-trib-rms-op:.55;
  --rv-bed:var(--accent);       --rv-bed-op:.22;
  --rv-rail:var(--accent);      --rv-rail-op:.90;
  --rv-meet:var(--accent);      --rv-meet-op:1;   --rv-meet-size:14;
  --rv-src:var(--ink-2);        --rv-src-op:.92;  --rv-src-size:20;
  --rv-add:1;
  /* 暗底实芯本来就是白芯 —— 身份由峰值色（--l-phys）承担，与 P3/P8 同一档 */
  --ex-frame:var(--ink-3);      --ex-frame-op:.62;
  --ex-inner-op:.40;
  --ex-screen:var(--l-phys);    --ex-screen-op:.10;
  --ex-flow:var(--l-phys);      --ex-flow-op:.54;
  --ex-rms:var(--ink);          --ex-rms-op:.55;
  --ex-dot:var(--ink-2);        --ex-dot-op:.92;  --ex-dot-size:8;
  --ex-add:1;
  /* 星座墙 · 暗底：卡再亮一点点会晃眼（原片本来就是深底棚拍），
     雾反而要重一档 —— 深空里「远」就是「暗」。 */
  --w-card-op:.94;   --w-fog:.46;
  --w-rim:var(--ink-3);  --w-rim-op:.40;
  --w-poster-rim:.30;
}
""" + _LAB_TAIL


# ═══ 本 deck 专属 CSS ═══════════════════════════════════════════════════════
#   顶部是 deck 级运动原语（与 build-convoai-engine.py 的 DECK_CSS 顶部逐字同源，
#   连纪律注释一起搬过来 —— 两份 deck 的运动语言必须是同一套，不许各写各的）。
DECK_CSS = """<style id="convoai-info-deck">
/* ═══ deck 级运动语言 · 五个原语（与引擎 deck 逐字同源 · 不新造 keyframe 名）═════
   ① .mo-packet  能量包 —— 宽 stroke 低透明 dash 段沿路径漂移。只挂实线主数据流，
      方向必须与箭头一致（路径按流向写 d，--mo-off 取负 = 顺路径跑）。它是**新增
      的纯装饰件**，不属于页面几何 ⇒ 静态语域直接 display:none。
   ② .mo-drift   虚线漂移 —— 事件 / 控制 / 参考线 / 域分带的 dash 慢爬，比包慢一档。
      载体是页面真线 ⇒ 静态语域只 animation:none，线本身照画。
   ③ .mo-pulse   脉冲 —— 命中 / 事件标 opacity 明暗，错峰 delay。
      --mo-hi / --mo-lo 可调：载体自带 opacity 时必须把 --mo-hi 设成它的静态值。
   ④ .mo-breathe hot 件呼吸 —— scale ≤1.03，**每页至多一处**，落在该页唯一 hot 件上；
      伴件 .mo-halo 是向外扩散的光晕（100% 帧 opacity:0 ⇒ 静态语域零痕迹）。
      .mo-halo 同时用于 DOM hot 件（transform-box:fill-box 在 HTML 元素上退化为内容盒，
      行为等价）—— 见 .hot-ring。
   ⑤ .mo-cycle   闭环绕行 —— 环 / 回路上的 dash 永续绕圈。
   纪律（硬红线，四条）：
     · 每条 keyframes 的 100% 帧 = 静态原图：dash 位移走完整周期、scale 回 1、
       opacity 回静态值、halo 回 0。遮挡扫描器与 qa 都注入 animation-duration:0s
       + animation-delay:0s 把元素钉在 100% 帧上 —— 「动效关掉 = 原图逐像素」。
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
/* DOM hot 件的光晕环：静态 opacity:0（纸面零痕迹），只在现场脉动一圈。
   放在 hot 文本件内部当兄弟层 —— 环本身不携带任何文字（qa-motion ② 闸）。 */
.hot-ring{position:absolute;pointer-events:none;display:block;}

/* ═══ 绝对画布 shape 层（robot26 惯例；reference 栈是语义排版系，缺这两行）═════ */
.pp{position:absolute;inset:0;}
.pp .sh{position:absolute;overflow:visible;}
:root{--l-eng:var(--accent);--l-agent:#5b8cff;--l-phys:#7b61ff;
  /* conf 家族 token 表里没有 --on-bg，components.css 的 .card.on 靠它上底色 */
  --on-bg:linear-gradient(180deg,color-mix(in srgb,var(--accent) 13%,transparent),
    color-mix(in srgb,var(--accent) 3%,transparent)),var(--card-bg);
  --warn-bg:linear-gradient(180deg,color-mix(in srgb,var(--coral) 10%,transparent),
    color-mix(in srgb,var(--coral) 2.5%,transparent)),var(--card-bg);}
html[data-theme="dark"]{--l-agent:#6e96ff;--l-phys:#b78cf0;
  --on-bg:linear-gradient(180deg,color-mix(in srgb,var(--accent) 9%,transparent),
    color-mix(in srgb,var(--accent) 2%,transparent)),var(--card-bg);
  --warn-bg:linear-gradient(180deg,color-mix(in srgb,var(--coral) 9%,transparent),
    color-mix(in srgb,var(--coral) 2%,transparent)),var(--card-bg);}
.card .tag.am{color:var(--amber);}
/* ── 投影可读性（2026-08-23 · GPT 5.6 review 采纳项 G · 两份 deck 逐字同源）────
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
/* hero-art：背景板之上、正文之下；contain 不裁切（GPT 交接约束）*/
.hero-art{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;
  z-index:0;pointer-events:none;}
.hero-art.dk{display:none;}
html[data-theme="dark"] .hero-art.lt{display:none;}
html[data-theme="dark"] .hero-art.dk{display:block;}
.slide.visible .hero-art{animation:heroIn 1.2s cubic-bezier(.22,.61,.36,1) both;}
@keyframes heroIn{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:none;}}
/* 版式件 */
.kk{font:700 20px/1 var(--f-mono);letter-spacing:.28em;color:var(--accent);}
.kk.ag{color:var(--l-agent);}.kk.ph{color:var(--l-phys);}.kk.nt{color:var(--ink-3);}
.hh{font:700 68px/1.16 var(--f-cn);letter-spacing:-.02em;color:var(--ink);}
.hh strong{color:var(--accent);}
.hh strong.ag{color:var(--l-agent);}.hh strong.ph{color:var(--l-phys);}
.sub{font:400 26px/1.55 var(--f-cn);color:var(--ink-2);}
.mono-sm{font:500 15px/1.4 var(--f-mono);letter-spacing:.08em;color:var(--ink-3);}
.dot{display:inline-block;width:14px;height:14px;border-radius:4px;margin:0 12px -1px 0;}
.card-c{background:var(--card-bg);border:1px solid var(--hair);border-radius:20px;}
/* Infograph 分区件：mono 小节标 + 1px 分隔细线 */
.seclab{font:500 14px/20px var(--f-mono);letter-spacing:.18em;color:var(--ink-3);}
.seclab b{font-weight:700;color:var(--ink-3);}
.hair-rule{background:var(--hair);}
/* 主题词 chip */
.chip{display:inline-block;margin:0 12px 12px 0;padding:11px 18px;border:1px solid var(--hair);
  border-radius:999px;background:var(--card-bg);font:500 18px/1 var(--f-cn);color:var(--ink-2);}
/* 能力宫格（P5 · 6×2）*/
.cap{border:1px solid var(--hair);border-radius:999px;background:var(--card-bg);
  font:500 16px/1 var(--f-cn);color:var(--ink-2);padding:10px 8px;text-align:center;}
.cap.on{border-color:color-mix(in srgb,var(--l-agent) 55%,transparent);
  background:color-mix(in srgb,var(--l-agent) 10%,var(--card-bg));color:var(--ink);}
/* 三态卡（活人感 · P6）*/
.face{padding:16px 22px;border-top:5px solid var(--ink-3);}
.face .en{font:700 13px/1 var(--f-mono);letter-spacing:.2em;color:var(--ink-3);}
.face h3{margin:8px 0 6px;font:700 26px/1.2 var(--f-cn);color:var(--ink);}
.face p{font:400 15px/1.5 var(--f-cn);color:var(--ink-2);}
.face.good{border-top-color:var(--l-phys);}
.face.good h3{color:var(--l-phys);}
/* .fig 内的 SVG 走 width:100%;height:auto，必须解掉 stage.css 的
   svg{max-width:100%;max-height:100%}，否则定高 .sh 里会被压扁 */
.fig svg{max-width:none;max-height:none;}

/* ═══ P7 · 五层生态主视觉（polish-v4 · Colin 与 GPT 仲裁定稿，层结构原样保留）══
   2026-08-21 v2 重建纪律：**不加卡片、不加 blur、不加遮罩**，只做家族容器化
   + 轻动效（四条域分带 dash-drift + 声网所在层的 hot 标记）+ 深浅稳态复核。 */
:root{--eco-surface:#f8f9fc;}
html[data-theme="dark"]{--eco-surface:#10111c;}
.eco-visual{position:relative;border:1px solid var(--hair);border-radius:20px;
  background:var(--eco-surface);box-shadow:0 18px 44px rgba(11,14,28,.10);}
/* `.pp .sh{overflow:visible}`（0,2,0）压过 `.eco-visual{overflow:hidden}`（0,1,0）→
   底图四角会戳出 20px 圆角边框。同特异度以上把裁切拿回来。 */
.pp .sh.eco-visual{overflow:hidden;}
/* .eco-art 与 .hero-art 同机制：双源 + CSS 控可见性（deckSwap 的 JS 只管 .strip） */
.eco-art{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  display:none;pointer-events:none;}
.eco-art.lt{display:block;opacity:1;}
html[data-theme="dark"] .eco-art.lt{display:none;}
html[data-theme="dark"] .eco-art.dk{display:block;}
/* 动效叠层：绝对定位的 SVG，只画域分带与 hot 标记，一个字都不画 */
.eco-mo{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:2;}
.eco-kicker{position:absolute;left:28px;top:22px;font:600 12px/1 var(--f-mono);
  letter-spacing:.2em;color:var(--ink-3);text-shadow:0 0 7px var(--eco-surface),0 0 3px var(--eco-surface);}
.eco-layer{position:absolute;left:24px;right:24px;height:67px;padding:12px 18px;
  display:grid;grid-template-columns:58px 230px 1fr;align-items:center;gap:12px;
  border:1px solid color-mix(in srgb,var(--ink-3) 22%,transparent);border-radius:12px;
  background:color-mix(in srgb,var(--card-bg) 88%,transparent);backdrop-filter:none;}
.eco-layer .eco-code{font:600 13px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);}
.eco-layer b{font:700 22px/1 var(--f-cn);color:var(--ink);}
.eco-layer small{font:400 13px/1.35 var(--f-cn);color:var(--ink-2);text-align:right;}
.eco-layer.l2,.eco-layer.l1,.eco-layer.l0{border-color:color-mix(in srgb,var(--accent) 55%,transparent);}
.eco-layer.l2 .eco-code,.eco-layer.l2 b,.eco-layer.l1 .eco-code,.eco-layer.l1 b,
.eco-layer.l0 .eco-code,.eco-layer.l0 b{color:var(--accent);}
.eco-layer.l4{top:54px;}.eco-layer.l3{top:137px;}.eco-layer.l2{top:220px;}
.eco-layer.l1{top:303px;}.eco-layer.l0{top:386px;}
html[data-theme="dark"] .eco-layer{background:rgba(10,12,24,.86);}
/* 案例墙 v2：3 张精选大卡 + 11 张证据小卡；客户名走 DOM 文本，不靠海报正文缩略。
   案例墙**不上动效**（文字件不动）—— 一整墙缩略图动起来就是噪声。 */
.case-wall-v2{height:100%;border:1px solid var(--hair);border-radius:20px;padding:20px 18px 16px;
  background:color-mix(in srgb,var(--card-bg) 74%,transparent);box-shadow:0 18px 44px rgba(11,14,28,.10);}
.case-wall-head{display:flex;align-items:baseline;gap:12px;height:38px;color:var(--ink-3);
  font:600 12px/1 var(--f-mono);letter-spacing:.16em;}
.case-wall-head b{margin-left:auto;font:900 42px/.8 var(--f-en);letter-spacing:-.04em;color:var(--accent);}
.case-wall-head small{font:400 12px/1.3 var(--f-cn);letter-spacing:0;color:var(--ink-2);}
.case-feature-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:2px;}
.case-feature{position:relative;height:238px;border:1px solid var(--hair);border-radius:14px;
  overflow:hidden;background:#151727;}
.case-feature img{width:100%;height:100%;display:block;object-fit:cover;object-position:center 68%;
  filter:saturate(.86) contrast(1.04);}
/* 底部压幕：海报自己烧录的品牌名与 DOM caption 在同一位置，中间色标把最后 ~20%
   压到 .93，海报文字变淡影、白字浮出来。 */
.case-feature:after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 38%,rgba(10,12,24,.5) 68%,rgba(10,12,24,.93) 100%);}
.case-feature-caption{position:absolute;left:12px;right:10px;bottom:10px;z-index:1;color:#fff;}
/* components.css 的 `b,strong{color:var(--ink)}`（0,0,1）直接命中这个 b，压过 caption 的
   继承白 —— 浅底主题下客户名会被染成近黑、压在深色幕布上隐形。 */
.case-feature-caption b{display:block;font:700 16px/1.15 var(--f-cn);color:inherit;}
.case-feature-caption span{display:block;margin-top:4px;font:500 10px/1 var(--f-mono);
  letter-spacing:.1em;color:rgba(255,255,255,.7);}
.case-index{display:flex;align-items:center;gap:10px;margin:17px 0 9px;
  font:500 11px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);}
.case-index:after{content:"";height:1px;flex:1;background:var(--hair);}
.case-mini-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;}
.case-mini{position:relative;height:124px;border:1px solid var(--hair);border-radius:10px;
  overflow:hidden;background:#171928;}
.case-mini img{width:100%;height:100%;display:block;object-fit:cover;object-position:center 38%;
  filter:saturate(.58) contrast(1.02) brightness(.82);}
.case-mini:after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 34%,rgba(10,12,24,.5) 66%,rgba(10,12,24,.88) 100%);}
.case-mini span{position:absolute;left:9px;right:7px;bottom:8px;z-index:1;color:#fff;
  font:700 13px/1.35 var(--f-mono);letter-spacing:.035em;text-shadow:0 1px 6px rgba(0,0,0,.9);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
@media print{.eco-visual,.case-wall-v2{box-shadow:none;}}
.callout-chip{background:var(--ink);color:var(--bg,#fff);border-radius:12px;padding:13px 22px;
  font:700 19px/1.4 var(--f-cn);box-shadow:0 8px 24px rgba(0,0,0,.22);}
html[data-theme="dark"] .callout-chip{background:#f5f5f4;color:#111;}
.callout-chip b,.callout-chip strong{color:inherit;}
/* polish-v4 · P7：完整五层生态主视觉 + 左右留白 DOM 标注，不用高不透明卡片遮图 */
[data-p="7"] .eco-visual{
  border:1px solid color-mix(in srgb,var(--ink) 16%,transparent);
  background-color:#f8f9fc;
  box-shadow:0 18px 44px rgba(11,14,28,.08);}
html[data-theme="dark"] [data-p="7"] .eco-visual{background-color:#050713;}
/* token 清账：五行文字的柔光 text-shadow 用 --eco-surface，深色下对齐 v4 面板底 */
html[data-theme="dark"] [data-p="7"]{--eco-surface:#050713;}
[data-p="7"] .eco-visual::after{
  content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(90deg,
    rgba(248,249,252,.99) 0%,rgba(248,249,252,.90) 18%,rgba(248,249,252,.18) 34%,
    rgba(248,249,252,.08) 66%,rgba(248,249,252,.88) 82%,rgba(248,249,252,.99) 100%);}
html[data-theme="dark"] [data-p="7"] .eco-visual::after{
  background:linear-gradient(90deg,
    rgba(5,7,19,.99) 0%,rgba(5,7,19,.90) 18%,rgba(5,7,19,.16) 34%,
    rgba(5,7,19,.08) 66%,rgba(5,7,19,.88) 82%,rgba(5,7,19,.99) 100%);}
[data-p="7"] .eco-kicker{
  z-index:3;left:24px;top:20px;font-size:12px;letter-spacing:.18em;
  color:var(--ink-3);text-shadow:none;}
[data-p="7"] .eco-layer{
  z-index:3;left:24px;right:24px;height:64px;padding:0;
  grid-template-columns:42px 205px minmax(0,1fr);gap:0;
  border:0;border-radius:0;background:transparent;backdrop-filter:none;}
html[data-theme="dark"] [data-p="7"] .eco-layer{background:transparent;}
[data-p="7"] .eco-layer .eco-code{
  font:700 13px/1 var(--f-mono);letter-spacing:.12em;
  color:var(--ink-3);text-shadow:0 0 12px var(--eco-surface);}
[data-p="7"] .eco-layer b{
  font:700 23px/1.12 var(--f-cn);color:var(--ink);
  text-shadow:0 0 14px var(--eco-surface),0 0 5px var(--eco-surface);}
[data-p="7"] .eco-layer small{
  justify-self:end;max-width:360px;font:500 15px/1.3 var(--f-cn);
  color:var(--ink-2);text-align:right;
  text-shadow:0 0 14px var(--eco-surface),0 0 5px var(--eco-surface);}
[data-p="7"] .eco-layer.l2 .eco-code,[data-p="7"] .eco-layer.l2 b,
[data-p="7"] .eco-layer.l1 .eco-code,[data-p="7"] .eco-layer.l1 b,
[data-p="7"] .eco-layer.l0 .eco-code,[data-p="7"] .eco-layer.l0 b{color:var(--accent);}
[data-p="7"] .eco-layer.l4{top:50px;}
[data-p="7"] .eco-layer.l3{top:157px;}
[data-p="7"] .eco-layer.l2{top:264px;}
[data-p="7"] .eco-layer.l1{top:361px;}
[data-p="7"] .eco-layer.l0{top:449px;}
[data-p="7"] .callout-chip{
  padding:7px 0 7px 20px;border-radius:0;border-left:3px solid var(--accent);
  background:transparent;color:var(--ink);box-shadow:none;}
html[data-theme="dark"] [data-p="7"] .callout-chip{background:transparent;color:var(--ink);}
[data-p="7"] .callout-chip b{color:var(--accent);}
/* polish · P7 浅色生态图对比度（2026-08-23 采纳项 D · 只调滤镜数值）────────────
   原值 contrast 1.14 / saturate 1.06 在会议室投影下仍然偏灰：主干与节点是原片里最细的
   一层墨，浅底 + 投影两道洗，网状节点几乎读不出来。本轮把对比再提约 15–20%
   （1.14 → 1.34 ≈ +17%；饱和 1.06 → 1.24 让三色节点各自站住），并补一档
   brightness(.97) 把整体白场压回来 —— 光提 contrast 会把浅灰底一起推成纯白，
   反而更平。**Colin 定稿红线不动：不加卡片、不加 blur、不加遮罩。深色零改动。** */
html:not([data-theme="dark"]) [data-p="7"] .eco-art.lt{
  filter:contrast(1.34) saturate(1.24) brightness(.97);}

/* ═══ P6 · R1 实拍图卡（图左 / 规格右 · 引擎 P19 同款机制，窗宽按本页 300 高重算）══
   图窗 280×300 对 1000×750（4:3）原片做 cover ⇒ 由**高**定标（scale = 300/750 = .40），
   整张原片的 750 行全在窗内，只裁左右：横向可见原片宽 = 280/.40 = 700px（居中 ⇒ 原片
   x150–849），两块板的实测墨迹在 x278–719 内，左右各余 58px 以上。**改窗宽必须重算这条。** */
.pp .sh.r1-card{overflow:hidden;}
.r1-card{display:flex;flex-direction:row;}
.r1-shot{position:relative;flex:none;width:280px;align-self:stretch;overflow:hidden;
  background:#0a0c14;border-right:1px solid var(--hair);}
/* 图必须 width/height 100% + object-fit —— 放大 img 去逼近墨迹会让它的 rect 冲出卡底，
   qa 的 cardspill（只读 rect、不读 overflow:hidden）稳报一条假命中。 */
.r1-shot img{width:100%;height:100%;display:block;object-fit:cover;object-position:center;}
.r1-body{flex:1;display:flex;flex-direction:column;padding:24px 26px 20px;}
.r1-main{flex:1;display:flex;flex-direction:column;justify-content:center;}
.r1-cap{flex:none;padding-top:12px;border-top:1px solid var(--hair);}
.r1-cap .cap{font:400 13px/1.5 var(--f-cn);color:var(--ink-3);}
/* 浅色主题下的「暗媒体卡」惯例：深底实拍图直接压在浅版面上会掉进洞里 ——
   给一圈发丝内描边把图从纸面上拎起来（实拍不翻色，只压一档饱和度）。 */
html:not([data-theme="dark"]) .r1-shot{box-shadow:inset 0 0 0 1px rgba(17,17,17,.12);}
html:not([data-theme="dark"]) .r1-shot img{filter:saturate(.92) contrast(1.03);}
@media print{.r1-shot{box-shadow:none;}}

/* ═══ P2 · 半屏 KPI 卡（四大数 2×2 · 逐字取自 lab P21 的 .lab-kpi）════════════
   四张卡从「一行四张 × 1680 宽」改成「2×2 × 930 宽」之后卡内高度成了瓶颈：
   家族 .card 的 30/32 padding + gap 13 在 196px 的行高里差 7px。这里把它收到
   24/26 + gap 10（**只动白边**），80px 的数字与 20px 的说明一个像素不改。 */
.lab-kpi .card{padding:24px 26px;gap:10px;}

/* ═══ 细节层 ·「密的东西进抽屉」（v3 新机制 · 每页至多一枚）═══════════════════
   .detail 面板 = 该页的 data-step="1"：默认收起，按 → / 空格 / chip 展开（BUILD
   指示器自然显示 1 步），Esc / ← 收回。展开态是一块从右侧滑入的卡（宽 ≤760 ·
   高 ≤640 · --card-bg 92% 不透明），盖在主图右半之上；3D 照跑 —— canvas 坐在 .pp
   之下，面板在 .pp 里，天然压在它之上。
   ⚠ 收起态**只走 opacity / clip-path**（motion.css 的 .flow.rev 那一路），不写
     display:none —— 写了就把「滑入」与「离线归档照常可按键展开」一起弄没了。
     收起态 pointer-events:none：面板压在图上，收起时不许吃走点击。
   ⚠ 面板内容仍在该 slide 的 DOM 里 ⇒ ⑫⑭⑮ 的字串闸门照过。
   ⚠ ⑳clr 的墨迹名册**不登记面板内的字**：面板压在 canvas 之上，3D 压不到它；
     qa 的 ⑳clr-a 文字遍历同步跳过 .detail 子树（两头一把尺，见 qa 里的注）。
   ⚠ @media print：面板 display:none —— 按需内容不上纸。 */
.detail{background:color-mix(in srgb,var(--card-bg-2) 92%,transparent);
  border:1px solid var(--hair);border-radius:18px;padding:24px 30px 22px;
  box-shadow:0 26px 64px rgba(11,14,28,.16);}
html[data-theme="dark"] .detail{box-shadow:0 26px 64px rgba(0,0,0,.46);}
/* `.pp .sh{overflow:visible}`（0,2,0）压过 `.detail{overflow:hidden}`（0,1,0） */
.pp .sh.detail{overflow:hidden;}
.detail:not(.on){pointer-events:none;}
.d-head{display:flex;align-items:baseline;gap:14px;margin-bottom:6px;}
.d-head .esc{margin-left:auto;font:500 12px/1 var(--f-mono);letter-spacing:.14em;
  color:var(--ink-3);}
.d-sec{margin-top:12px;}
@media print{.detail{display:none!important;}}

/* ═══ 引擎详解抽屉（P4 / P5 / P6 三个入口 · 视口级 overlay）═════════════════
   触发 chip：形制与 .chip 家族一字不差，只把描边/文字换成 accent。
   position:relative 是给 .hot-ring 用的（P4 的 hot 件 = 抽屉 chip）。 */
.chip-expand{position:relative;border-color:color-mix(in srgb,var(--accent) 52%,transparent);
  color:var(--accent);cursor:pointer;-webkit-user-select:none;user-select:none;
  transition:background .15s ease,border-color .15s ease;}
.chip-expand:hover,.chip-expand:focus-visible{
  background:color-mix(in srgb,var(--accent) 14%,var(--card-bg));
  border-color:color-mix(in srgb,var(--accent) 80%,transparent);}
.chip-expand.ag{border-color:color-mix(in srgb,var(--l-agent) 52%,transparent);color:var(--l-agent);}
.chip-expand.ag:hover,.chip-expand.ag:focus-visible{
  background:color-mix(in srgb,var(--l-agent) 14%,var(--card-bg));
  border-color:color-mix(in srgb,var(--l-agent) 80%,transparent);}
.chip-expand.ph{border-color:color-mix(in srgb,var(--l-phys) 52%,transparent);color:var(--l-phys);}
.chip-expand.ph:hover,.chip-expand.ph:focus-visible{
  background:color-mix(in srgb,var(--l-phys) 14%,var(--card-bg));
  border-color:color-mix(in srgb,var(--l-phys) 80%,transparent);}
/* 视口级 overlay（避开舞台 transform，原生控件/iframe 都不吃缩放坐标系的亏）。
   z 必须盖过 .deck-progress(1000)/.deck-swap(1100)/.edit-hotzone(10000)。 */
#engineOverlay{position:fixed;inset:0;z-index:10002;}
#engineOverlay[hidden]{display:none;}
.eo-scrim{position:absolute;inset:0;background:rgba(6,8,18,.78);}
.eo-sheet{position:absolute;inset:26px;border-radius:18px;overflow:hidden;
  border:1px solid rgba(255,255,255,.16);box-shadow:0 30px 90px rgba(0,0,0,.5);background:#e6e6eb;}
.eo-sheet iframe{display:block;width:100%;height:100%;border:0;}
/* 收回按钮挪到左上：iframe 内的引擎 deck 右上角是页码 sig，ESC 胶囊压在右上会叠在一起。 */
.eo-close{position:absolute;top:14px;left:16px;font:600 12px/1 var(--f-mono);letter-spacing:.14em;
  color:#f5f5f7;background:rgba(10,10,15,.55);border:1px solid rgba(255,255,255,.22);
  border-radius:999px;padding:9px 14px;cursor:pointer;}
.eo-close:hover{background:rgba(10,10,15,.8);}
.eo-close:focus:not(:focus-visible){outline:none;box-shadow:none;}
@media print{#engineOverlay,.deck-swap{display:none!important;}}
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


# ═══ 组装件（与引擎 deck 同签名 —— 两份 deck 的图形语法必须可互抄）══════════
def sh(cls, style, body, step=None, sid=None):
    a = ' data-sid="%s"' % sid if sid else ""
    a += ' data-step="%d"' % step if step is not None else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (cls, a, style, body)


def dot(var):
    return '<span class="dot" style="background:var(--%s)"></span>' % var


def rule(y, x=120, w=1680, i=1):
    """分区之间的 1px 细线（高度 1px → 扫描器不当它是覆盖块）"""
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:%dpx;height:1px;--i:%d" % (x, y, w, i), "")


def lab(x, y, txt, w=620, col=None, i=0, step=None):
    """mono 小节标：「01 · SCALE」"""
    c = ";color:%s" % col if col else ""
    return sh("flow seclab", "left:%dpx;top:%dpx;width:%dpx;height:20px;--i:%d%s" % (x, y, w, i, c),
              txt, step=step)


def figbox(x, y, w, vbw, vbh, inner, cls="flow", i=0, step=None):
    """SVG 装盒：.sh 高度按 viewBox 等比算死，svg 一律 width:100%;height:auto"""
    h = round(w * vbh / vbw)
    return sh(cls, "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (x, y, w, h, i),
              '<div class="fig"><svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg></div>'
              % (vbw, vbh, inner), step=step)


def head(kicker, title, kk="kk"):
    """每页统一的页眉：kicker y92 / 标题 y148 起（家族版式纪律）"""
    return (sh("flow " + kk, "left:120px;top:92px;width:1680px;height:28px", kicker)
            + sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", title))


def land(txt, y=988, x=120, w=1680, i=6):
    return sh("flow", "left:%dpx;top:%dpx;width:%dpx;height:70px;--i:%d" % (x, y, w, i),
              '<div class="land">%s</div>' % txt)


def rail(txt, y=1010, x=120, w=1680, i=7, align=None):
    a = ";text-align:%s" % align if align else ""
    return sh("flow mono-sm", "left:%dpx;top:%dpx;width:%dpx;height:24px;--i:%d%s" % (x, y, w, i, a), txt)


_DETAIL_X, _DETAIL_Y, _DETAIL_W, _DETAIL_HMAX = 1060, 250, 740, 640
DETAIL_PAGES = [2, 3, 4, 5, 6, 7]  # 有细节层的页（P1 封面 / P8 合流按规格不带）


def detail(title, body, h=640, y=_DETAIL_Y, i=2):
    """细节层面板（该页的 data-step=1 · 从右侧滑入 · Esc / ← 收回）。
       几何锁死：x 1060（右缘 1800 = 版心右缘 · 左缘让开 P2 左栏卡的 x1050）·
       顶 250（页码 sig 底 y64 之下）·
       底 ≤890（land y988 之上）⇒ 展开态压不到 land / SOURCE / 页码。
       走 `.flow.rev`：motion.css 的收起态是 translate3d(30px,·) + inset(0 0 0 100%)
       ——「从右侧滑入」这四个字就是这条规则本人，不新造 keyframe。"""
    assert h <= _DETAIL_HMAX, "细节层面板高 %d > 上限 %d" % (h, _DETAIL_HMAX)
    assert y + h <= 900, "细节层面板底 %d 压到 land 带了" % (y + h)
    return sh("flow rev detail", "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d"
              % (_DETAIL_X, y, _DETAIL_W, h, i),
              '<div class="d-head"><span class="seclab">%s</span>'
              '<span class="esc">ESC · 收回</span></div>%s' % (title, body), step=1)


def detail_chip(x=1500, y=986, w=300, i=6):
    """细节层入口 chip（mono · 与引擎抽屉 chip 同款 · 放在 land 行右侧）。
       它不是另一套开关：按下 = 走 deck 的第 1 步，与 → / 空格完全同一条路。"""
    return sh("flow", "left:%dpx;top:%dpx;width:%dpx;height:50px;text-align:right;--i:%d"
              % (x, y, w, i),
              '<span class="chip chip-expand chip-detail" role="button" tabindex="0" '
              'data-detail="1" style="margin-right:0">⤢ 细节 · ⏎</span>')


def src(txt, y=1010, x=120, w=1680, i=7, align=None):
    """SOURCE ledger 行（2026-08-23 采纳项 C）。全家族统一四段：
         SOURCE · <来源> · <样本或时间窗> · 事实截止 2026.08
       缺哪段就少哪段（不编），缺口记在交付报告里等 Colin 补。
       与 rail() 分成两枚类：.src 是「出处」，.mono-sm 是页内普通元信息行 ——
       G 轮只提 .src 与 .sig 这两枚投影小字的字号/色阶，别再把它们混用。"""
    a = ";text-align:%s" % align if align else ""
    return sh("flow src", "left:%dpx;top:%dpx;width:%dpx;height:24px;--i:%d%s" % (x, y, w, i, a), txt)


# ── SVG 小件（引擎 deck 同源）───────────────────────────────────────────────
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


def hline(x1, x2, y, col=HS, w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d H%d" '
            'stroke="%s" stroke-width="%s" fill="none"/>' % (abs(x2 - x1), i, x1, y, x2, col, w))


def vline(x, y1, y2, col=HS, w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d V%d" '
            'stroke="%s" stroke-width="%s" fill="none"/>' % (abs(y2 - y1), i, x, y1, y2, col, w))


def dline(d, col=HS, w=2, i=1, dash="7 7", cls="", sty=""):
    """虚线：不能走 .dw —— motion.css 的 .dw{stroke-dasharray:var(--len)} 会把 dasharray
       整条压掉，虚线会渲染成实线。改挂 .pop（只动 opacity/transform），破折保留。
       cls / sty：额外类与额外内联变量（挂运动原语用：.mo-drift + --mo-off/--mo-dur）。"""
    return ('<path class="pop%s" style="--i:%d%s" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-dasharray="%s"/>'
            % ((" " + cls) if cls else "", i, (";" + sty) if sty else "", d, col, w, dash))


def curve(d, col, w=2.5, i=1):
    """实线主干（贝塞尔）：走 .dw 自绘入场，--len 用采样长度算，不许瞎填。"""
    return ('<path class="dw" style="--len:%d;--i:%d" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-linecap="round"/>' % (round(path_len(d)) + 8, i, d, col, w))


def box(x, y, w, h, r=4, hot=False, dashed=False, i=0, cls="", sty="", col=None):
    """家族图框：常态 class="box"（fill card-bg / stroke hair），高亮走 accent 描边。"""
    d = ' stroke-dasharray="7 6"' if dashed else ""
    c = (" " + cls) if cls else ""
    v = (";" + sty) if sty else ""
    if hot:
        return ('<rect class="pop%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
                'fill="none" stroke="%s" stroke-width="2.5"%s/>'
                % (c, i, v, x, y, w, h, r, col or AC, d))
    return ('<rect class="pop box%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'stroke-width="1.4"%s/>' % (c, i, v, x, y, w, h, r, d))


def halo_rect(x, y, w, h, r=8, col=None, sc="1.06", op=".34", dur="3.6s", delay=None):
    """呼吸光晕（原语 ④ 的伴件 · 矩形版）：贴着 hot 盒向外扩散再消失。
       100% 帧 opacity:0 ⇒ 静态语域零痕迹（纸面上不会留一枚谜之边框）。"""
    v = "--mo-sc:%s;--mo-op:%s;--mo-dur:%s" % (sc, op, dur)
    if delay:
        v += ";--mo-del:%s" % delay
    return ('<rect class="mo-halo" style="%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'fill="none" stroke="%s" stroke-width="2.5" opacity="0"/>' % (v, x, y, w, h, r, col or AC))


def halo_div(style, col=None, sc="1.16", op=".38", dur="3.4s", delay=None, radius="14px", bw="2.5px"):
    """DOM hot 件的光晕环：空 <i>，不携带任何文字（qa-motion ② 闸）。
       静态 opacity:0 ⇒ 截图 / 纸面上零痕迹，只在现场脉动。"""
    v = "--mo-sc:%s;--mo-op:%s;--mo-dur:%s" % (sc, op, dur)
    if delay:
        v += ";--mo-del:%s" % delay
    return ('<i class="mo-halo hot-ring" aria-hidden="true" style="%s;%s;'
            'border:%s solid %s;border-radius:%s"></i>' % (style, v, bw, col or AC, radius))


def txt(x, y, s, cls="txt", size=None, anchor=None, col=None, weight=None,
        mono=False, ls=None, sty=None):
    st = []
    if sty:
        st.append(sty)
    if size:
        st.append("font-size:%dpx" % size)
    if col:
        st.append("fill:%s" % col)
    if weight:
        st.append("font-weight:%d" % weight)
    # mono：.lbl 是唯一自带 mono 的类，但它带 text-transform:uppercase（会把「Token 签名」
    # 烧成「TOKEN 签名」）。要 mono 又要保留大小写时走这一路。
    if mono:
        st.append("font-family:var(--f-mono)")
    if ls is not None:
        st.append("letter-spacing:%s" % ls)
    a = ' text-anchor="%s"' % anchor if anchor else ""
    g = ' class="%s"' % cls if cls else ""
    style = ' style="%s"' % ";".join(st) if st else ""
    return '<text%s x="%d" y="%d"%s%s>%s</text>' % (g, x, y, a, style, s)


# ── 运动原语 ① 能量包（deck 级）────────────────────────────────────────────
#   压在实线之下的一段粗软 stroke，沿路径漂移。dasharray =「包长 seg + 间隔 per-seg」，
#   --mo-off 恰好走完一个整周期 per ⇒ 100% 帧与 0% 帧逐像素相同（静态原图纪律）。
#   per = 包距（两枚包之间的路径距离）；速度 v = per / dur，全图统一 v 才能「同速接力」。
def packet(d, per, dur, delay=None, col=None, w=12, seg=22, op=".32", i=2, cap="round", cls=""):
    v = "--mo-off:%d;--mo-dur:%s" % (-per, dur)
    if delay is not None:
        v += ";--mo-del:%s" % delay
    return ('<path class="pop mo-packet%s" style="--i:%d;%s" d="%s" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-opacity="%s" stroke-linecap="%s" stroke-dasharray="%d %d"/>'
            % ((" " + cls) if cls else "", i, v, d, col or AC, w, op, cap, seg, per - seg))


# ── 线型系统 + 真线样迷你图例（P8 质量语言第一条）────────────────────────────
def lg_solid(x, y, col=AC, w=2.5, i=9):
    return hline(x, x + 40, y, col, w, i)


def lg_dash(x, y, col=HS, w=1.6, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="6 5")


def lg_dot(x, y, col=AD, w=2.4, i=9):
    return dline("M%d %d H%d" % (x, y, x + 40), col, w, i, dash="2 6")


def lg_fast(x, y, col=AC, w=6, i=9):
    return hline(x, x + 40, y, col, w, i)


_LGK = {"solid": lg_solid, "dash": lg_dash, "dot": lg_dot, "fast": lg_fast}


def legend(x, y, items, i=9, gap=48, size=14):
    """图例行：items = [(kind, 标签)] / [(kind, 标签, 线宽)] / [(kind, 标签, 线宽, 颜色)]。
       样线必须与页内真线同粗同色，否则「粗一档 / 弱一档」在图例里读不出来。"""
    o, cx = [], x
    for it in items:
        kind, label = it[0], it[1]
        w = it[2] if len(it) > 2 else None
        col = it[3] if len(it) > 3 else None
        kw = {"i": i}
        if w is not None:
            kw["w"] = w
        if col is not None:
            kw["col"] = col
        o.append(_LGK[kind](cx, y, **kw))
        o.append(txt(cx + 50, y + 5, label, "sm", size=size))
        cx += 50 + int(len(label) * 13.2) + gap
    return "".join(o)


# ── 贝塞尔路径长度（P8 合流的相位账必须按真实弧长算，不许目测）──────────────
def _cub(p0, p1, p2, p3, t):
    u = 1 - t
    return (u * u * u * p0 + 3 * u * u * t * p1 + 3 * u * t * t * p2 + t * t * t * p3)


def bez_len(p0, p1, p2, p3, n=240):
    """三次贝塞尔弧长（折线采样，n=240 的误差 < 0.05%，对相位来说远够）"""
    last, s = p0, 0.0
    for k in range(1, n + 1):
        t = k / n
        cur = (_cub(p0[0], p1[0], p2[0], p3[0], t), _cub(p0[1], p1[1], p2[1], p3[1], t))
        s += math.hypot(cur[0] - last[0], cur[1] - last[1])
        last = cur
    return s


def path_len(d):
    """只认本 deck 用到的三种 d：M…C… 三次贝塞尔 / M…L… 直线 / M…H|V… 轴向线。
       先把命令字母与数字拆开（'M30 90' 这种紧挨着写法在本文件里到处都是）。"""
    s = d.replace(",", " ")
    for c in "MCLHV":
        s = s.replace(c, " " + c + " ")
    tok = s.split()
    if "C" in tok:
        i = tok.index("C")
        p0 = (float(tok[1]), float(tok[2]))
        p1 = (float(tok[i + 1]), float(tok[i + 2]))
        p2 = (float(tok[i + 3]), float(tok[i + 4]))
        p3 = (float(tok[i + 5]), float(tok[i + 6]))
        return bez_len(p0, p1, p2, p3)
    if "L" in tok:
        i = tok.index("L")
        return math.hypot(float(tok[i + 1]) - float(tok[1]), float(tok[i + 2]) - float(tok[2]))
    if "H" in tok:
        return abs(float(tok[tok.index("H") + 1]) - float(tok[1]))
    if "V" in tok:
        return abs(float(tok[tok.index("V") + 1]) - float(tok[2]))
    return 0.0


def _n3(x):
    """短数字（最多 4 位小数 · 去掉尾零）—— 构建期摊 data-* 与写 SVG 坐标都用它。
       定义提到页之前：P7 的星座墙 poster 在页里就要用（它是构建期离线投影出来的）。"""
    return ("%.4f" % float(x)).rstrip("0").rstrip(".") or "0"


PAGES = []          # (board, steps, body_html, hero)


def page(board, body, hero=None, steps=0, lab=None):
    PAGES.append((board, steps, body, hero, lab))


# ═══ P1 · 封面（title 板 · 家族封面骨架）═══════════════════════════════════
#   气质对齐引擎 P1：kicker y200 / 96px 主标 y266 / accent 短棒 / sub / 页脚 mono。
#   主标与三产品线 chips 逐字保留（Fable 裁定 #1 之后就没再动过）。
#   AI-art 主视觉：新图 2048×1152 透明底、右重心，实际墨迹从图内 x669 起（= 屏幕 x1112），
#   主标两行各 9 个全角字、右缘 x≈967 —— 中间还剩 145px 净空，宽标题与图不相撞。
#   盒 left720+width1200=1920 正好齐右缘（原 860+1200=2060 会被舞台裁掉 140px）。
#   **本页不入运动件名册**：封面是静的（引擎 P1 同例），一张会动的封面只会抢主标。
page("title", "".join([
    sh("flow kk", "left:120px;top:200px;width:1400px;height:28px",
       "AGORA · 声网 · CONVERSATIONAL AI · INFOGRAPH"),
    sh("ink", "left:120px;top:266px;width:1100px;height:250px;"
       "font:700 96px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "让陪伴自然，<br>让生意<strong style='color:var(--accent)'>成单</strong>。"),
    sh("spread", "left:120px;top:552px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow sub", "left:120px;top:600px;width:1400px;height:44px;--i:4",
       "声网 · 对话式 AI —— 一页一章 · 拜访速讲版"),
    sh("rise", "left:120px;top:700px;width:1500px;height:56px;"
       "font:700 26px/1 var(--f-mono);letter-spacing:.06em;color:var(--ink-2);--i:5",
       dot("l-eng") + 'ENGINE<span style="margin-left:56px"></span>'
       + dot("l-agent") + 'AGENT<span style="margin-left:56px"></span>'
       + dot("l-phys") + 'PHYSICAL AI'),
    sh("flow mono-sm", "left:120px;top:930px;width:1200px;height:24px;--i:6",
       "主讲人：姚光华 Colin · 声网 AI 产品线负责人"),
]), hero=("info-v2/hero-cover-v2", "left:720px;top:220px;width:1200px;height:675px"),
     lab=("voice" if P1_MODE == "orb" else None))

# ═══ P2 · 公司 · Why Agora（v3「一页一讲」重建）═════════════════════════════
#   主图 = **SD-RTN 地球**（lab P21 的场景与矩形逐字同参 · 现取 makeGlobe）。
#   页上留的：左栏四大数 2×2 + IDC 注（与引擎 P21 / lab P21 逐字同源）+ 一句落点。
#   密材料（03 OpenAI 首批两行 · 使用声网/其他 RTC 条 · 04 五里程碑）全部进**细节层**。
#
#   ── 口径锁（2026-08-21 Colin：「四大数与来源标注改为与引擎 P21 逐字同源」）──
#   禁止回归的旧错误：93万 / 700亿 /「对话式 AI 引擎市场占有率」/「200+ 覆盖场景 · 20+ 行业」。
#   ⚠ 43.4% 这个具体数字**不写**：引擎 P21 的仲裁 P0 已把它换成「份额超过第 2–8 位厂商
#     总和」的定性表述（理由：未取得公司批准口径）。「拷贝原句」= 拷贝改过之后的那一句。
#   200+ 不进四卡（引擎 P21：「四卡足够，不补第五个数字」）；它在本页的正确落点是
#   地球的**角注**（节点分布示意 · 200+ 全球节点 · SD-RTN）。
#
#   ── 版式账（改任一个数就得把这一段一起改）──────────────────────────────
#     左栏 x120–1050（930 宽）：seclab y236 · 四卡 2×2 y272–688 · IDC 注 y706–766。
#     地球矩形 (1150,180,640,640)：球心 (1470,500) · 屏上半径 250 ⇒ 限界 x1220–1720 /
#       y250–750，弧的外包络半径 312 ⇒ x1158–1782 / y188–812，全在矩形之内。
#       离左栏右缘 100px、离版心右缘 18px（1782 vs 1800）。
#     rule(850) 压住 content 背景板自带的那条 accent 细线（y848–852 · x120–761）。
#     角注 y872–896（右对齐到 1800）· land y940 · SOURCE y1022。
_WHY = [
    ("市场占有率", "No.1",   "稳居第一 · 份额超过第 2–8 位总和", True),
    ("技术突破",   "50+",    "突破性自主创新技术（全球发明专利）", False),
    ("开发者生态", "100万+", "全球注册应用数",                   False),
    ("生产规模",   "900亿+", "单月支撑通话分钟数",               False),
]
# 五节点里程碑（内容逐字未改）—— v3 里它从「页脚横带」搬进细节层，改**竖排**：
# 760 宽的面板里横排 5 段名称只能缩到 8px，那是装饰不是信息。
_MILE = [
    # 2026-08-20 仲裁 P0：「全球首个 Realtime API」是 OpenAI 的事，不是声网的事，
    # 且与同页 03 · ENDORSEMENT 的「全球首批合作伙伴」自相矛盾。改为首批口径。
    ("2024.10.01", "全球首批 Realtime API", False),
    ("2024.10.24", "国内首个 Realtime API", False),
    ("2025.03.06", "引擎 1.0 + R1 GA",      False),
    ("2025.10.31", "产品全栈发布",           False),
    ("2026.03.10", "Call Agent 全球版",      True),
]
_P2_Q, _P2_T = 110, "1.1s"          # 里程碑竖轴的包距与周期（v = 100 单位/秒 · 全 deck 同速）


def _p2mile():
    """04 · MILESTONES 竖排时间线（viewBox 700×250 · 细节层内）
       线型只有一种（时间轴），所以不上图例；「流的什么 / 为什么」写在 seclab 那一行。
       ⚠ 它在**细节层**里，不是 poster ⇒ 不走 _lpsplit（本页的 poster 是地球）。"""
    o = []
    ax, y0, y1 = 26, 18, 232
    o.append(vline(ax, y0, y1, "var(--hair)", 1.5, 0))
    # 能量包：一枚包从最早的里程碑跑向最新的（方向 = 时间方向 · 自上而下）
    o.append(packet("M%d %d V%d" % (ax, y0, y1), _P2_Q, _P2_T, col=AC, w=8, seg=30, op=".20", i=1))
    o.append(ah_d(ax, y1 + 14, "var(--ink-3)", 7))
    step = (y1 - y0) / (len(_MILE) - 1)
    for k, (date, name, hot) in enumerate(_MILE):
        cy = round(y0 + k * step)
        if hot:
            o.append('<circle class="mo-halo" style="--mo-sc:3.2;--mo-op:.5;--mo-dur:3.2s" '
                     'cx="%d" cy="%d" r="7" fill="none" stroke="%s" stroke-width="2" opacity="0"/>'
                     % (ax, cy, AC))
            o.append('<circle class="pop" style="--i:%d;fill:%s" cx="%d" cy="%d" r="8"/>' % (2 + k, AC, ax, cy))
        else:
            o.append('<circle class="pop box" style="--i:%d" cx="%d" cy="%d" r="7" stroke-width="1.6"/>'
                     % (2 + k, ax, cy))
        o.append(txt(52, cy + 6, date, "sm", size=17, mono=True,
                     col=AC if hot else "var(--ink-3)", ls=".04em"))
        o.append(txt(186, cy + 7, name, "ttl", size=19, col=AC if hot else None))
    return "".join(o)


def _p2detail():
    """细节层内容：03 ENDORSEMENT 两行 + 使用声网/其他 RTC 条 + 04 MILESTONES 竖排。
       字串**逐字同源**（与 v2 的 03 / 02 两区、_MILE 表一字不差）。"""
    return "".join([
        '<div style="font:700 26px/1 var(--f-mono);letter-spacing:.1em;color:var(--accent);'
        'margin-top:6px">2024.10.01</div>',
        '<div style="margin-top:14px;font:700 27px/1.36 var(--f-cn);color:var(--ink)">'
        "OpenAI Realtime API · Agora <strong style='color:var(--accent)'>全球首批合作伙伴</strong>"
        '</div>',
        '<div style="margin-top:12px;font:500 18px/1.5 var(--f-cn);color:var(--accent)">'
        '同样的工程能力，今天用来支撑你的对话式 AI 业务。</div>',
        # 02 · ADOPTION 的那两条（逐字同源）：使用声网 / 其他 RTC
        '<div class="d-sec" style="display:flex;gap:10px">'
        '<div style="flex:0 0 344px;height:38px;background:var(--accent);border-radius:6px;'
        'font:700 17px/38px var(--f-cn);color:var(--slide-bg);text-align:center">使用声网</div>'
        '<div style="flex:1;height:38px;background:var(--card-bg);border:1px solid var(--hair);'
        'border-radius:6px;font:500 17px/36px var(--f-cn);color:var(--ink-2);text-align:center">'
        '其他 RTC</div></div>',
        '<div class="d-sec seclab">04 · MILESTONES · 18 个月 · 5 个公开里程碑</div>',
        '<div class="fig" style="margin-top:8px">'
        '<svg viewBox="0 0 700 250" style="width:100%%;height:auto">%s</svg></div>' % _p2mile(),
    ])


page("content", "".join([
    head("公司 · 声网 RTE · ONE-PAGE BRIEF",
         "RTE 行业领导者，<strong>一页讲完</strong>。"),
    # 区 01 · SCALE（四大数 2×2 · 引擎 P21 口径锁）· hot = No.1
    lab(120, 236, "01 · SCALE", w=930),
    sh("", "left:120px;top:272px;width:930px;height:416px",
       '<div class="g2 lab-kpi" style="height:100%">' + "".join(
           '<div class="card%s rise" style="--i:%d;justify-content:center">'
           '<div class="tag%s">%s</div>'
           '<div class="stat"><span class="v%s" style="font-size:80px">%s</span>'
           '<span class="l">%s</span></div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag,
              "" if _on else " w", _v, _l)
           for _i, (_tag, _v, _l, _on) in enumerate(_WHY)) + '</div>'),
    # hot 光晕环：贴着 No.1 那一格（g2 单格宽 = (930−24)/2 = 453 ⇒ 第一格 x120..573）。
    # sc 1.05 ⇒ 峰值只涨 ~11px，右缘 584 仍在第二格起点 597 之内。
    sh("", "left:116px;top:268px;width:461px;height:200px;pointer-events:none",
       halo_div("position:absolute;inset:0", sc="1.05", op=".22", dur="3.4s", radius="16px")),
    # 引擎 P21 的 note 逐字：43.4% 已被仲裁换成定性表述，这里不许回填
    sh("flow", "left:120px;top:706px;width:930px;height:60px;--i:5",
       '<div class="note grey">注：IDC《中国视频云市场报告》音视频通信（RTC）赛道 · '
       '<b>份额超过第 2–8 位厂商总和</b></div>'),
    rule(850),
    # ── 地球角注（从 lab P21 原样搬来的那一行）───────────────────────────────
    #   这一行是**硬要求**，不是装饰：228 枚节点是示意分布，不标它就等于默认它是
    #   真实 PoP 清单。弧线同理 —— 全页一个延迟数值都不许出现（数字红线）。
    sh("flow mono-sm", "left:1150px;top:872px;width:650px;height:24px;text-align:right;--i:6",
       "节点分布示意 · 200+ 全球节点 · SD-RTN"),
    # 落点句（含「近一半」逐字）
    land("集成 RTC 的 Top 10,000（MAU）App 里，<strong>近一半</strong>使用声网。",
         y=940, w=1200),
    detail_chip(x=1400, y=938, w=400),
    # 细节层：03 OpenAI 首批 + 使用声网/其他 RTC 条 + 04 五里程碑（竖排）
    #   高 600 而不是上限 640：底 850 让开地球角注（y872）那一行。
    detail("03 · ENDORSEMENT", _p2detail(), h=600),
    # SOURCE ledger（四段制）· 本行与引擎 P21 逐字同源，两份 deck 不许分叉
    src("SOURCE · 声网官网 / IR 公开口径 · IDC 中国视频云市场报告 · 事实截止 2026.08",
        y=1022, x=940, w=860, align="right"),
]), steps=1, lab="globe")

# ═══ P3 · 矩阵 ·「一个实时底座，三条产品线」（v3 · 空间生长放大到全舞台）═══════
#   2026-08-20 仲裁 P0 的分类学在图里：底座（SD-RTN / RTE）→ 三条产品线
#   （Engine / Agent / Physical AI）→ Engine 的两种交付形态（闭源引擎 / 开源 TEN）；
#   评测平台、实时转录翻译是「配套能力 · 工具」，旁挂、不与产品线并列 —— 图里用
#   「细虚线 + 弱化 + 不占主干」把这层级差画出来，不靠标签自说自话。
#   六个 chip 的内容逐字进图（名称 + 形态标签一字未改）。
#   hot 件 = SD-RTN 底座（这页的论点：托举一切的是那一条）。
#
#   ── v3 放大账（矩形 480 → 600 · 图形区吃满全舞台）────────────────────────
#     产品线盒 300×112 → **380×140**（规格下限 360×140）：盒里三行字（mono 名在盒外、
#       标题 25px、形态标签 15px）从「挤在 112 里」变成「有呼吸」。
#     主干 base_y 370→450 / trunk_top 172→200 ⇒ 生长段 196→248px（长了 27%）。
#     辅件盒 74→84 高、下沉到 y290–374（与主干注解 y245 留 45px）。
#     底座 rect 76→96 高（两行字 y486 / y520）。
#     纵深基面栅格整片坐在 fig y402–448 那条**无字空带**里（上方 aux 盒文字止于 y354，
#       下方底座顶沿 y450），横向止于 fig x1450（右边 y426 那行域分带注记从 x1460 起）。
_MX_LINES = [
    # (trunk_x, 色, mono 名, 盒内标题, 盒内形态标签, 主干注解 = _ENG3 的描述逐字)
    (300,  LE, "ENGINE",      "对话式 AI 引擎", "产品线 · Engine · 闭源", "提供能力——把「会说话」做到极致"),
    (840,  LA, "AGENT",       "企业级智能体",   "产品线 · Agent",         "交付结果——替你把任务做完"),
    (1380, LP, "PHYSICAL AI", "开发套件",       "产品线 · Physical AI",   "打开入口——让对话走出屏幕"),
]
_MX_AUX = [
    # (x, w, 名称, 形态标签, 挂法)  · 挂法 "trunk" = 挂在 Engine 主干上；"base" = 挂在底座上
    # ⚠ 右缘必须**停在主干之前**（三条主干在 fig x 300 / 840 / 1380）：
    #   盒宽一放到 300 就被主干从盒里穿过去（本轮实拍锤过）。260 宽留 30–40px 让路。
    (10,   260, "TEN 开源工具库",  "Engine 交付形态 · 开源", "trunk"),
    (540,  260, "AI 模型评测平台", "配套能力 · 工具",        "base"),
    (1080, 260, "实时转录翻译",    "配套能力 · 工具",        "base"),
]
_MX_BW, _MX_BH = 380, 140                 # 产品线盒（规格下限 360×140）
_MX_BOXY = 40                             # 盒顶（fig）
_MX_AUXY, _MX_AUXH = 290, 84              # 辅件盒
_MX_SEP = 432                             # 细虚线域分带的 y
# 底座顶沿 / 高 / 主干终点 —— **2D 与 3D 共用这三个数**（LAB 层的 makeGrow 直接引用，
# 不许两处各写一个字面量：v2 就是这么埋雷的）。
# 高 86 而不是 96：底座底沿 fig 536 与图例（fig 556）留 20px，而图例又必须收在
# content 背景板那条 accent 细线之前（stage y848–852 = fig 576–580）。
_GW_BASEY, _GW_BASEH, _GW_TOP = 450, 86, 200


def _p3fig():
    o = []
    base_y, trunk_top = _GW_BASEY, _GW_TOP
    # ── 细虚线域分带：上方是产品线与配套，下方是实时底座 ──
    o.append(dline("M0 %d H1668" % _MX_SEP, HS, 1, 0, dash="3 9",
                   cls="mo-drift", sty="--mo-off:-24;--mo-dur:4.2s"))
    o.append(txt(1660, _MX_SEP - 6, "↑ 产品线与配套　↓ 实时底座", "sm", size=14, anchor="end",
                 col="var(--ink-3)", mono=True))
    # ── 三条主干（实线三色 · 由底座向上生长）+ 能量包（同速 v=100 单位/秒）──
    for k, (tx, col, mono, title, form, why) in enumerate(_MX_LINES):
        o.append(box(tx - _MX_BW // 2, _MX_BOXY, _MX_BW, _MX_BH, 6, i=1 + k))
        o.append(txt(tx, 25, mono, "lbl", size=15, anchor="middle", col=col))
        o.append(txt(tx, _MX_BOXY + 62, title, "ttl", size=28, anchor="middle"))
        o.append(txt(tx, _MX_BOXY + 100, form, "sm", size=16, anchor="middle"))
        d = "M%d %d V%d" % (tx, base_y - 2, trunk_top)
        o.append(packet(d, 248, "2.48s", delay="%.2fs" % (-0.62 * k), col=col,
                        w=16, seg=26, op=".34", i=2 + k))
        o.append('<path class="dw" style="--len:248;--i:%d" d="%s" stroke="%s" stroke-width="2.5" '
                 'fill="none"/>' % (2 + k, d, col))
        o.append(ah_u(tx, trunk_top - 12, col, 8))
        o.append(txt(tx + 18, 245, why, "sm", size=17, col="var(--ink-2)"))
    # ── 配套 / 交付形态：细虚线旁挂，**无箭头**（它是附属说明，不是第三种流向）──
    for x, w, name, form, how in _MX_AUX:
        o.append(box(x, _MX_AUXY, w, _MX_AUXH, 5, dashed=True, i=5))
        o.append(txt(x + w // 2, _MX_AUXY + 36, name, "ttl", size=21, anchor="middle", col="var(--ink-2)"))
        o.append(txt(x + w // 2, _MX_AUXY + 64, form, "sm", size=15, anchor="middle", col="var(--ink-3)"))
        if how == "trunk":
            o.append(dline("M%d %d H300" % (x + w + 4, _MX_AUXY + 42), HS, 1.4, 6, dash="5 6",
                           cls="mo-drift", sty="--mo-off:-33;--mo-dur:3.8s"))
        else:
            o.append(dline("M%d %d V%d" % (x + w // 2, _MX_AUXY + _MX_AUXH, base_y), HS, 1.4, 6,
                           dash="5 6", cls="mo-drift", sty="--mo-off:-33;--mo-dur:3.8s"))
    # ── 底座（hot）：accent 描边 + 光晕；条内两枚反向包 = 端 ↔ 云 一直在跑 ──
    o.append(halo_rect(0, base_y, 1668, _GW_BASEH, 8, sc="1.03", op=".26", dur="3.8s"))
    o.append('<rect class="pop" style="--i:7;fill:var(--card-bg-2)" x="0" y="%d" width="1668" '
             'height="%d" rx="8" stroke="none"/>' % (base_y, _GW_BASEH))
    o.append(box(0, base_y, 1668, _GW_BASEH, 8, hot=True, i=7))
    o.append(txt(30, base_y + 34, "实时底座 · RTE · REAL-TIME ENGAGEMENT", "lbl", size=16, col=AC))
    o.append(txt(30, base_y + 68, "SD-RTN 全球实时网络——一个实时底座，托举上面三条产品线与全部配套能力",
                 "txt", size=21))
    o.append(packet("M1180 %d H1640" % (base_y + 52), 260, "2.6s", col=AC, w=9, seg=18, op=".22", i=8))
    o.append(packet("M1640 %d H1180" % (base_y + 52), 260, "3.0s", col=AC, w=9, seg=18, op=".22", i=8))
    # ── 迷你图例（真线样 · 只列本页真正用到的线型）──
    # 图例 y556（stage 828）而不是 580：content 背景板自带一条 accent 细线在
    # stage y848–852（fig 576–580），图例落在 580 会被那条线从字里穿过去。
    o.append(legend(10, 556, [("solid", "Engine 主干", 2.5, LE), ("solid", "Agent 主干", 2.5, LA),
                              ("solid", "Physical AI 主干", 2.5, LP),
                              ("dash", "配套 / 交付形态 · 旁挂", 1.4, HS)]))
    return _lpsplit(o)


page("content", "".join([
    head("矩阵 · 对话式 AI 产品线 · PRODUCT MATRIX",
         "一个实时底座，<strong>三条产品线</strong>。"),
    lab(120, 236, "01 · ARCHITECTURE · 一个底座 · 三条主干 · 配套旁挂"),
    figbox(120, 272, 1680, 1680, 600, _p3fig(), i=1),
    rule(850),
    land(dot("l-eng") + "Engine 提供能力　" + dot("l-agent") + "Agent 交付结果　"
         + dot("l-phys") + "Physical AI 走进物理世界。", y=940, w=1200),
    detail_chip(x=1400, y=938, w=400),
    # 细节层：02 · ENGINE DELIVERY FORMS（一句 + 两枚 chip）
    detail("02 · ENGINE DELIVERY FORMS", "".join([
        '<div style="margin-top:10px" class="note">Engine 的'
        '<strong style="color:var(--accent)">两种交付形态</strong>：闭源引擎 · 开源 TEN。</div>',
        '<div class="d-sec">'
        '<span class="chip">闭源 · 已上线　对话式 AI 引擎</span>'
        '<span class="chip">开源　TEN 开源工具库</span></div>',
    ]), h=260, y=300),
]), steps=1, lab="grow")

# ═══ P4 · Engine ·「超低延迟、可打断、高自然度」（v3 波B · 主图 = 双向声带）══════
#   主图 = lab P4 的**全双工双向声带**：`_duplex_lanes()`（2D 泳道 / poster）现取 +
#   `makeDuplex`（两条对向 3D ribbon）现取，矩形与 lab 逐字同参 (120,268,1680,352)。
#   三条 lane 标题 听 / 想 / 说 与三行说明**逐字照 lab P4**（`_LAB._LANES`）。
#   舞台起点 x = 页 900（局部 780）≥ 三行说明最右墨迹 874 + 16 —— 构建期断言，
#   两条声带交叉恰 2 次的解析断言一并照抄（见 build() 的 ⓗ）。
#   页上留的数 = 三件极致一行三格（口径逐字取 lab P5 的 `_EXTREMES`）。
#   密材料（17 次发版 / VS LIVEKIT / SIGNATURE MOVES / OPEN）全部进**细节层**。
#   hot 件 = 抽屉 chip（本页唯一「可以按下去」的东西）· 常显，不进分步。
_CMP = [
    ("打断成功率",   "越高越好",             "33%",   "17%"),
    ("词错率 WER",   "理想条件 · 越低越好",   "9.25%", "13.77%"),
    ("误响应率",     "50dB 人声噪声 · 越低越好", "7%",  "100%"),
    ("多语种",       "开箱默认 · 中西法俄阿日", "6/6", "仅英文"),
]
_MOVES = [
    ("01", "优雅打断 2.0", "CAN + 语义 + 声学三路融合。从「能打断」到「打断得体」。"),
    ("02", "声纹识别",     "有感 / 无感双模式。多人同场分得清说话人。"),
    ("03", "短期记忆",     "会话内毫秒级上下文。转人工、转 Agent 不丢线索。"),
]
_OPEN = ["ASR / LLM / TTS 可替换 · 可兜底 · 可热切换", "MCP + Function Call",
         "数字人", "TEN 开源生态"]
_P4_REL = 17                       # 18 个月 17 次公开发版（口径与 v2 逐字同源）


def _p4band_sm():
    """细节层里的**发版活动带**（viewBox 700×86 · 缩排版）。
       原 `_p4band` 是 1440 宽的横带，塞进 740 的面板里字号只剩 8px ——
       这里按面板宽度重画同一张图：一根轴 + 17 格 + 一枚能量包，
       两端日期 13px、轴下线标 12px（**字号 ≥12 是这一格的硬要求**）。
       文案与格数一个都没改。"""
    o, x0, x1, ay = [], 14, 686, 40
    o.append(hline(x0, x1, ay, "var(--hair)", 1.5, 0))
    # 包距 224（v=100 ⇒ 2.24s 一枚）：672 长的轴上同时 3 枚，密了会读成虚线装饰
    o.append(packet("M%d %d H%d" % (x0, ay, x1), 224, "2.24s", col=LE, w=8, seg=20, op=".24", i=1))
    for k in range(_P4_REL):
        x = x0 + round(k * (x1 - x0) / (_P4_REL - 1))
        big = k in (0, _P4_REL - 1)
        o.append('<rect class="pop" style="--i:%d;fill:%s%s" x="%d" y="%d" width="%d" height="%d" rx="2"/>'
                 % (1 + k // 6, LE if big else "var(--ink-3)", "" if big else ";opacity:.55",
                    x - (2 if big else 1), ay - (13 if big else 9), 4 if big else 3,
                    26 if big else 18))
    o.append(txt(x0, 18, "2025.02.18 · v1.0 公测", "sm", size=13, mono=True, col="var(--ink-3)"))
    o.append(txt(x1, 18, "2026.08.11 · v2.11 最新", "sm", size=13, anchor="end", mono=True, col=LE))
    o.append(txt(x0, 70, "RELEASE FLOW · 每一格 = 一次公开发版 · 包在跑 = 版本一直在出",
                 "sm", size=12, mono=True, col="var(--ink-3)"))
    return "".join(o)


def _p4detail():
    """细节层：01 十七次发版 + 02 VS LIVEKIT 四行 + 03 SIGNATURE MOVES + 04 OPEN。
       字串**逐字同源**（与 v2 的 01/02/03/04 四区一字不差）。"""
    return "".join([
        '<div style="display:flex;align-items:baseline;gap:14px;margin-top:2px">'
        '<span style="font:900 40px/1 var(--f-en);letter-spacing:-.03em;color:var(--l-eng)">17</span>'
        '<span class="mono-sm">PUBLIC RELEASES · 18 MONTHS</span></div>',
        '<div class="fig" style="margin-top:2px">'
        '<svg viewBox="0 0 700 74" style="width:100%%;height:auto">%s</svg></div>' % _p4band_sm(),
        '<div class="d-sec seclab">02 · VS LIVEKIT · 2026-03 同题评测 · 默认配置口径</div>',
        '<div style="margin-top:6px;display:grid;grid-template-columns:1fr 92px 92px;'
        'gap:0 10px;align-items:center">'
        '<div></div>'
        '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.1em;color:var(--l-eng);'
        'text-align:right">声网</div>'
        '<div style="font:500 12px/1 var(--f-mono);letter-spacing:.1em;color:var(--ink-3);'
        'text-align:right">LIVEKIT</div>'
        + "".join(
            '<div style="padding:4px 0;border-top:1px solid var(--hair)">'
            '<span style="font:700 16px/1.3 var(--f-cn);color:var(--ink)">%s</span>'
            '<span style="margin-left:10px;font:400 12px/1 var(--f-cn);color:var(--ink-3)">%s</span></div>'
            '<div style="padding:4px 0;border-top:1px solid var(--hair);text-align:right;'
            'font:700 16px/1.3 var(--f-mono);color:var(--ink)">%s</div>'
            '<div style="padding:4px 0;border-top:1px solid var(--hair);text-align:right;'
            'font:500 16px/1.3 var(--f-mono);color:var(--ink-3)">%s</div>'
            % (_n, _d, _vo, _vt) for _n, _d, _vo, _vt in _CMP)
        + '</div>',
        '<div class="d-sec seclab">03 · SIGNATURE MOVES</div>',
        "".join('<div style="margin-top:6px">'
                '<span style="font:700 13px/1 var(--f-mono);color:var(--l-eng);'
                'margin-right:10px">%s</span>'
                '<span style="font:700 17px/1.3 var(--f-cn);color:var(--ink)">%s</span>'
                '<div style="margin-top:2px;font:400 14px/1.45 var(--f-cn);color:var(--ink-2)">%s</div>'
                '</div>' % (_no, _n, _d) for _no, _n, _d in _MOVES),
        '<div class="d-sec seclab">04 · OPEN</div>',
        '<div style="margin-top:6px">'
        + "".join('<span class="chip" style="margin:0 7px 7px 0;padding:6px 12px;font-size:13px">'
                  '%s</span>' % _t for _t in _OPEN) + '</div>',
    ])


page("content", "".join([
    head("ENGINE · 一页讲透 · SHIPPING VELOCITY", "超低延迟、可打断、<strong>高自然度</strong>。"),
    lab(120, 236, "01 · THREE LANES · 同时在跑"),
    # 主图：lab P4 的三条泳道（2D = poster）+ 双向声带（3D）· 图与矩形逐字同参
    figbox(120, 268, 1680, 1680, 352, _unwrap_poly(_LAB._duplex_lanes()), i=1),
    figbox(1080, 630, 720, 720, 28,
           legend(0, 14, [("solid", "音频流"), ("dash", "事件 / 控制"), ("fast", "快路径")]), i=4),
    # 区 02 · THREE EXTREMES（一行三格 · 口径逐字取 lab P5 的三张数字卡）
    lab(120, 636, "02 · THREE EXTREMES · 三件极致"),
    ] + [
    sh("flow", "left:%dpx;top:676px;width:540px;height:170px;--i:%d" % (120 + _i * 580, 2 + _i),
       '<div class="stat"><span class="u">%s</span>'
       '<span class="v" style="font-size:64px;color:var(--l-eng)">%s'
       '<span style="font-size:.38em;letter-spacing:0">%s</span></span>'
       '<span class="l" style="font-size:19px;color:var(--ink);font-weight:700">%s</span></div>'
       '<div style="margin-top:8px;font:400 15px/1.5 var(--f-cn);color:var(--ink-2)">%s</div>'
       % (_tag, _v, _u, _n, _d))
    for _i, (_tag, _v, _u, _n, _d, _ptr) in enumerate(_LAB._EXTREMES)
    ] + [
    rule(850),
    land("模型会换代，接口不换人。", y=940, w=620),
    # 引擎详解抽屉的触发件（P4 上按 Enter 或点击 → 视口级 overlay）· **常显**：
    # 细节层占了 data-step=1，本页唯一的 action 不能再藏在分步里。
    # hot 光晕环塞在 chip 内部当兄弟层：环是空 <i>，不携带文字（qa-motion ② 闸）。
    sh("flow", "left:820px;top:938px;width:600px;height:50px;text-align:right;--i:5",
       '<span class="chip chip-expand" id="engineExpand" role="button" tabindex="0" '
       'data-eng-hash="1" style="margin-right:0">'
       + halo_div("left:-5px;top:-5px;right:-5px;bottom:-5px", sc="1.10", op=".42",
                  dur="3.0s", radius="999px", bw="2px")
       + '⤢ 引擎产品详解 · 22 页 · ⏎</span>'),
    detail_chip(x=1460, y=938, w=340),
    detail("01 · VELOCITY · 18 个月 17 次公开发版", _p4detail(), h=640),
    # SOURCE ledger：两块数据各出各的来源与时间窗 —— 发版轴（18 个月 17 次）与同题评测。
    # 「2026-03 时点」是 LiveKit 对比的口径限定，必须在页脚也留一份。
    src("SOURCE · 引擎公开发版 / 同题评测 默认配置口径 · "
        "18 个月 17 次发版 / 2026-03 时点 · 事实截止 2026.08",
        y=1022, x=700, w=1100, align="right"),
]), steps=1, lab="duplex")

# ═══ P5 · Agent ·「已经超越真人的企业级智能体」（v3 波B · 主图 = 五个大脑）══════
#   主图 = lab P17 的**五脑区大脑**：`_brain_fig()`（2D 侧视线稿 / poster）现取 +
#   `makeBrain`（母形 → 体积点云）现取，矩形与 lab 逐字同参 (120,282,1680,580)。
#   五区标注 / INPUT 客户语音 /「输出 · 最佳回复」逐字照 lab P17。
#   ⚠ **不带** lab P17 的那行「为什么 96.5%…答案在这五层」脚注 —— 那是一句因果断言；
#     本 deck 的 96.5% 是 2,475 通**生产**口径，与引擎 P16 的「盲测 32,000」是两个
#     数据集，全篇不许出现「盲测 / 32,000」（build() 有反向断言）。
#   页上留的数 = 96.5% 与 2.05× 两格，落在标题行右半那块空地上（主标 14 字止于 x1072）。
#   密材料（漏斗四行 / 五件事 / 十二项能力）全部进**细节层**。
#   hot 件 = 96.5% 大数（DOM 光晕环）。
_FUN = [
    ("接听",      "2,475 · 100.0%", 1.000, None),
    ("真人接听",   "2,180 · 88.1%",  0.881, None),
    ("有效对话",   "1,170 · 47.3%",  0.473, "var(--l-agent)"),
    ("感知为 AI",  "86 · 3.5%",      0.035, "var(--coral)"),
]
# 五进阶（内容逐字未改 —— v2 的 03 · FIVE 那五行）
_FIVE = [
    ("01", "运行时", "全球 SD-RTN 200+ 节点"),
    ("02", "记忆",   "毫秒级分层记忆 RAG 端到端"),
    # 2026-08-20 仲裁 P0：混合 chip 拆成三段各自成立的表述。
    # SOC 2 保持原措辞（builder 里查不到「Type II」的既有依据，不擅自升格）。
    ("03", "安全",   "99.99% SLA · SOC 2 · 支持 GDPR 合规"),
    ("04", "工具",   "MCP + Function Call 开放栈"),
    ("05", "弹性",   "900 亿分钟 RTE 月均支撑"),
]
_G12 = ["SIP / PSTN 全打通", "Warm Transfer", "WhatsApp 接入", "LATAM SIP", "海外多供应商",
        "静态填充词", "Campaign A/B", "时区 · 号码前缀", "音色复刻", "优雅打断 2.0",
        "声纹识别", "实时情绪识别"]


def _p5detail():
    """细节层：漏斗四行 + 03 五件事 + 04 十二项能力 chips（字串逐字同源）。"""
    return "".join([
        '<div style="margin-top:4px">'
        + "".join(
            '<div style="display:flex;align-items:center;gap:12px;margin-top:5px">'
            '<span style="flex:none;width:78px;font:500 13px/1 var(--f-mono);'
            'letter-spacing:.1em;color:var(--ink-3);text-align:right">%s</span>'
            '<span style="flex:none;height:24px;width:%dpx;border-radius:3px;'
            'border:2px solid %s;background:%s"></span>'
            '<span style="font:500 14px/1 var(--f-mono);color:%s">%s</span></div>'
            % (_lb, max(round(_r * 300), 8), _col or "var(--hair-strong)",
               "transparent", _col or "var(--ink-2)", _v)
            for _lb, _v, _r, _col in _FUN)
        + '</div>',
        '<div style="margin-top:8px;font:400 15px/1.5 var(--f-cn);color:var(--ink-2)">'
        '仅 3.5%（86 通）被用户明显感知为 AI。</div>',
        # 02 · CONVERSION 的原句（v2 逐字）：页上只留 2.05× 与一行短标，
        # 「1.5% 行业天花板 / 3.08% 真实生产数据」这两段密材料落在这里。
        '<div class="d-sec seclab">02 · CONVERSION</div>',
        '<div style="margin-top:6px;font:400 15px/1.6 var(--f-cn);color:var(--ink-2)">'
        '行业最佳人工 1.5% —— 行业天花板　·　ConvoAI 3.08% —— 真实生产数据</div>',
        '<div style="margin-top:4px;font:500 14px/1 var(--f-mono);letter-spacing:.06em;'
        'color:var(--l-agent)">AI ÷ 人 = 2.05 倍 · 日均营销转化率</div>',
        '<div class="d-sec seclab">03 · FIVE · 企业级智能体必须做的 5 件事</div>',
        "".join('<div style="display:flex;align-items:baseline;gap:12px;margin-top:5px">'
                '<span style="flex:none;width:88px;font:500 13px/1 var(--f-mono);'
                'color:var(--l-agent)">%s · %s</span>'
                '<span style="font:400 15px/1.35 var(--f-cn);color:var(--ink-2)">%s</span></div>'
                % (_no, _n, _v) for _no, _n, _v in _FIVE),
        '<div class="d-sec seclab">04 · CAPABILITIES · 企业级智能体 12 项能力</div>',
        '<div style="margin-top:6px;display:grid;grid-template-columns:repeat(3,1fr);gap:6px">'
        + "".join('<div class="cap%s" style="font-size:13px;padding:7px 4px">%s</div>'
                  % (" on" if _i == 9 else "", _t) for _i, _t in enumerate(_G12))
        + '</div>',
    ])


page("content", "".join([
    head("AGENT · 企业级智能体 · REAL PRODUCTION DATA",
         '已经超越<strong class="ag">真人</strong>的企业级智能体。', kk="kk ag"),
    # ── 页上留的两个数（标题行右半的空地：主标 14 字 68px 止于 x1072）──────────
    #   hot = 96.5%（DOM 光晕环）。两格底 y252，与主图顶 y282 留 30px。
    sh("settle", "left:1100px;top:132px;width:380px;height:120px;--i:2",
       '<div class="stat"><div class="v" style="font-size:60px;color:var(--l-agent)">96.5%</div>'
       '<div class="l" style="font-size:16px">通话未出现用户明确识别 AI 的信号</div></div>'),
    # 2026-08-23 采纳项 B ·「96.5% 口径明示」：大数下方那行 cohort 标注，三段全部是
    # 本页已有的词与数重组（副句 + 漏斗首级 2,475 + 页眉 REAL PRODUCTION DATA）。
    sh("flow src", "left:1100px;top:230px;width:700px;height:20px;--i:2",
       "生产外呼 · n=2,475 · 未出现明确 AI 识别信号"),
    sh("", "left:1094px;top:128px;width:250px;height:88px;pointer-events:none",
       halo_div("position:absolute;inset:0", col=LA, sc="1.08", op=".24", dur="3.2s", radius="16px")),
    sh("settle", "left:1520px;top:132px;width:280px;height:120px;--i:3",
       '<div class="stat"><div class="v" style="font-size:60px;color:var(--l-agent)">2.05×</div>'
       '<div class="l" style="font-size:16px">AI ÷ 人 · 日均营销转化率</div></div>'),
    lab(120, 246, "01 · FIVE BRAIN REGIONS · 同时放电", w=900),
    # 图例挪到页眉行右半区（lab P17 同款破例）—— 主图是一颗满幅的脑，底下留不出图例带。
    # 本页把它放在主图之下的空带里（y866），与 lab 的位置不同、内容逐字相同。
    figbox(120, 282, 1680, 1680, 580, _unwrap_poly(_LAB._brain_fig()), i=1),
    figbox(120, 866, 720, 720, 30,
           _LAB.legend(0, 16, [("solid", "输入 · 主通路"), ("fast", "合成输出"),
                               ("dot", "突触弧线"), ("dot", "标注引线", 1.2, "var(--ink-3)")]),
           i=5),
    land("不再是「AI 能否替代人工」——是「人工能否追上 AI」。", y=940, w=760),
    # 深链入口：跳引擎 deck 的 Call Agent 章（#16）· 常显
    sh("flow", "left:920px;top:938px;width:500px;height:50px;text-align:right;--i:5",
       '<span class="chip chip-expand ag" id="agentExpand" role="button" tabindex="0" '
       'data-eng-hash="16" style="margin-right:0">⤢ Call Agent 详解 · ⏎</span>'),
    detail_chip(x=1460, y=938, w=340),
    detail("02 · TURING FUNNEL · 生产外呼 n=2,475", _p5detail(), h=640),
    # SOURCE ledger：本页两个数据块（96.5% 漏斗 / 2.05× 转化）同属一份生产外呼数据集
    src("SOURCE · 真实生产数据 · 生产外呼 n=2,475 · 事实截止 2026.08",
        y=1022, x=1120, w=680, align="right"),
]), steps=1, lab="brain")

# ═══ P6 · PhysicalAI ·「让对话，走出屏幕」（v3 波B · 版式照 lab P19）══════════
#   01 R1 KIT 两张大图卡（**带实拍图**，跨 deck 引用 robot26 原片，不复制文件）——
#   版式照 lab P19（两张 820 宽的大卡 + 规格行），卡文案逐字取现版 P6。
#   「走出屏幕」加法层保留在标题右侧那条空带（exit 场景 + poster 原样）。
#   02 ROBOTICS 1 三数一行三格；密材料（活人感三态）进**细节层**。
#   hot 件 = 实拍图组（两枚图窗各一圈光晕，同相 —— 一个 hot 概念）。
#   深链 chip → 抽屉跳引擎 #19（R1 开发套件页）· 常显。
#   ⚠ 图窗几何账（改卡高必须重算这一条 · 见 DECK_CSS 的 .r1-shot 段）：
#     窗 280×340 对 1000×750（4:3）原片做 cover ⇒ 由**高**定标（scale = 340/750 = .4533），
#     整张原片的 750 行全在窗内，只裁左右：横向可见原片宽 = 280/.4533 = 617.6px
#     （居中 ⇒ 原片 x191–809），两块板的实测墨迹在 x278–719 内，左右各余 87px 以上。
_R1KIT = [
    ("R1 · WI-FI · 2025.03.20 发布", "R1-WiFi",
     "面向家居与室内场景——音箱、桌宠、陪伴机器人。",
     "· 连接　Wi-Fi　　· 场景　家居 / 室内　　· 形态　音箱 · 桌宠 · 陪伴机器人",
     "r1-wifi.webp"),
    ("R1 · 4G · 2025.09.26 发布", "R1-4G",
     "走出 Wi-Fi 覆盖——户外、随身、车载与出海设备。",
     "· 连接　4G 全移动　　· 场景　户外 / 随身 / 车载　　· 形态　出海设备 · 随身伴侣",
     "r1-4g.webp"),
]
_FACES = [
    ("",      "TOO DRY",    "太木", "正确，但没有关系温度。用户不想再开口。"),
    (" good", "JUST RIGHT", "恰好", "自然、可持续相处。下次还想跟它说话。"),
    ("",      "TOO CLINGY", "太腻", "伪装成朋友的销售感。三句之后想拔电源。"),
]
_ROB = [
    ("200+",   "",                        "全球节点 · SD-RTN 软件定义实时网"),
    ("毫秒级",  "font-family:var(--f-cn);", "端到端往返 · 弱网最后一公里对抗"),
    ("30000+", "",                        "芯片与整机适配 · 你的形态大概率已支持"),
]


def _p6exit():
    """⑦ 加法层的 **poster**（降级链是生命线 · 构建期离线投影 · 一个字都没有）。
       投影是**恒等**的 —— 屏幕的三枚框都过投影锁，落点就是它们的页坐标；
       所以这里画的与 WebGL 那一帧是同一张图，交接时不会跳。
       件序与 3D 一致：屏面填色 → 后框 + 四条棱 → 内屏框 → 外框 → 中心线。
       字一个都没有；箭头头（方向标注）按家族纪律**留在 poster 组之外**，
       压在 canvas 之上钉住流向（qa 的 ⑲a 正面断言 poster 组里零 polygon）。"""
    x, y, w, h = _EX_BOX
    ins, ins2, r, r2 = _EX_INS, _EX_INS2, _EX_R, _EX_R2
    # 屏面：不透明度走 CSS 变量 ⇒ poster 与 3D 两档主题同源（浅 .07 / 暗 .10）
    screen = ('<rect class="pop" style="--i:1;opacity:var(--ex-screen-op,.07)" x="%g" y="%g" '
              'width="%g" height="%g" rx="%g" fill="var(--ex-screen,var(--l-phys))"/>'
              % (x + ins2, y + ins2, w - 2 * ins2, h - 2 * ins2, r2))
    back = ('<rect class="pop" style="--i:1;opacity:.5" x="%g" y="%g" width="%g" height="%g" '
            'rx="%g" fill="none" stroke="var(--ink-3)" stroke-width="1.2"/>'
            % (x + ins, y + ins, w - 2 * ins, h - 2 * ins, max(2.0, r - ins / 2.0)))
    edge = "".join("M%g %g L%g %g" % (a[0], a[1], b[0], b[1])
                   for a, b in (((x + r * .3, y + r * .3), (x + ins + r * .3, y + ins + r * .3)),
                                ((x + w - r * .3, y + r * .3), (x + w - ins - r * .3, y + ins + r * .3)),
                                ((x + w - r * .3, y + h - r * .3), (x + w - ins - r * .3, y + h - ins - r * .3)),
                                ((x + r * .3, y + h - r * .3), (x + ins + r * .3, y + h - ins - r * .3))))
    edges = ('<path class="pop" style="--i:1;opacity:.4" d="%s" stroke="var(--ink-3)" '
             'stroke-width="1" fill="none"/>' % edge)
    inner = ('<rect class="pop" style="--i:1;opacity:.62" x="%g" y="%g" width="%g" height="%g" '
             'rx="%g" fill="none" stroke="var(--ink-3)" stroke-width="1.2"/>'
             % (x + ins2, y + ins2, w - 2 * ins2, h - 2 * ins2, r2))
    front = ('<rect class="pop" style="--i:1" x="%g" y="%g" width="%g" height="%g" rx="%g" '
             'fill="none" stroke="var(--ink-3)" stroke-width="1.5"/>' % (x, y, w, h, r))
    mid = hline(round(x + w), round(_EX_P2[0]), round(_EX_P2[1]), "var(--hair)", 1.5, 0)
    return (lp(screen, back, edges, inner, front, mid)
            + ah_r(round(_EX_P2[0]) + 12, round(_EX_P2[1]), LP, 9))


page("content", "".join([
    head("PHYSICAL AI · 对话式 AI 开发套件 · GLOBAL FIRST",
         '让对话，<strong class="ph">走出屏幕</strong>。', kk="kk ph"),
    ] + ([
    # ⑦ 加法层的降级层：标题右侧那条空带上的 poster（无字 · 见 _p6exit()）
    figbox(_EX_RECT[0], _EX_RECT[1], _EX_RECT[2], _EX_RECT[2], _EX_RECT[3], _p6exit(), i=1),
    ] if P6_EXIT else []) + [
    lab(120, 236, "01 · R1 KIT · 两种形态"),
    ] + [
    sh("rise card-c r1-card", "left:%dpx;top:268px;width:820px;height:340px;--i:%d" % (120 + _i * 860, 2 + _i),
       '<div class="r1-shot"><img src="%s%s" alt="声网 R1 开发套件 · %s 实拍">%s</div>'
       '<div class="r1-body"><div class="r1-main">'
       '<div class="mono-sm" style="color:var(--l-phys)">%s</div>'
       '<h3 style="margin:10px 0 0;font:700 38px/1.15 var(--f-cn);color:var(--ink)">%s</h3>'
       '<div style="margin-top:16px;font:400 19px/1.55 var(--f-cn);color:var(--ink-2)">%s</div>'
       '</div><div class="r1-cap"><span class="cap">%s</span></div></div>'
       % (R26, _img, _nm,
          halo_div("left:14px;top:14px;right:14px;bottom:14px", col=LP, sc="1.05", op=".34",
                   dur="3.6s", delay="%.1fs" % (-0.9 * _i), radius="6px", bw="2px"),
          _tag, _nm, _p, _spec))
    for _i, (_tag, _nm, _p, _spec, _img) in enumerate(_R1KIT)
    ] + [
    # 区 02 · ROBOTICS 1（一行三格 · 逐字取现版 03 · ROBOTICS 1）
    lab(120, 640, "02 · ROBOTICS 1 · 机器人的临场引擎"),
    ] + [
    sh("flow", "left:%dpx;top:676px;width:540px;height:120px;--i:%d" % (120 + _i * 580, 2 + _i),
       '<div style="font:900 56px/1.1 var(--f-en);%sletter-spacing:-.02em;color:var(--l-phys)">%s</div>'
       '<div style="margin-top:10px;font:400 17px/1.5 var(--f-cn);color:var(--ink-2)">%s</div>'
       % (_ff, _v, _l))
    for _i, (_v, _ff, _l) in enumerate(_ROB)
    ] + [
    rule(850),
    sh("flow", "left:120px;top:876px;width:1000px;height:44px;font:500 24px/1.4 var(--f-cn);"
       "color:var(--l-phys);--i:6", "全球率先发布的对话式 AI 硬件开发套件。"),
    land("你做产品与角色，我们做<strong style='color:var(--l-phys)'>临场与连接</strong>。",
         y=940, w=760),
    # 深链入口：跳引擎 deck 的 R1 页（#19）· 常显
    sh("flow", "left:920px;top:938px;width:500px;height:50px;text-align:right;--i:5",
       '<span class="chip chip-expand ph" id="physExpand" role="button" tabindex="0" '
       'data-eng-hash="19" style="margin-right:0">⤢ R1 开发套件详解 · ⏎</span>'),
    detail_chip(x=1460, y=938, w=340),
    # 细节层：02 · LIFELIKE 活人感三态 + 收口一句（字串逐字同源）
    detail("02 · LIFELIKE ·「活人感」三态", "".join([
        "".join('<div class="face%s" style="border-top-width:4px;padding:10px 0 8px;'
                'margin-top:10px">'
                '<div class="en">%s</div><h3 style="margin:6px 0 4px;font-size:22px">%s</h3>'
                '<p style="font-size:14px">%s</p></div>' % (_cls, _en, _cn, _d)
                for _cls, _en, _cn, _d in _FACES),
        '<div class="d-sec"><div class="note">活人感 = '
        '<strong style="color:var(--l-phys)">角色立得住 + 临场撑得住</strong>。</div></div>',
    ]), h=470),
    # SOURCE ledger：来源段与引擎 P19（同一套 R1 事实）同源；时间窗取本页两张卡的发布日
    src("SOURCE · 声网官网 / R1 公开发布信息 · 2025.03.20 / 2025.09.26 发布 · 事实截止 2026.08",
        y=1022, x=820, w=980, align="right"),
]), steps=1, lab=("exit" if P6_EXIT else None))

# ═══ P7 · 案例 ·「对话式 AI，已经上岗」（v3 波C · 主图 = 14 家 3D 星座墙）═══════
#   主图 = 新场景 `wall`：14 张公开案例卡图做成**带厚度的贴图卡片**，两排弧形排在
#   纵深里 —— 前排三家头部（luwu / Robopoet / 集贤科技 · 大一档）、后排 11 家；
#   整墙绕竖轴极缓摆动 ±6°（周期 20s · 零随机源），各卡按自己的相位轻微前后浮动 ±10。
#   **零文字进 canvas**：卡上只有图，客户名一律在 DOM 的名册行里（⑮ 闸认那一行）。
#   细节层 = 01 ECOSYSTEM 五层地壳（现版 eco 图双源 + L4–L0 五行 + 两句逐字）。
#
#   ── 2026-08-21 v2 定稿里不许再动的东西（Colin 与 GPT 仲裁）─────────────────
#     · eco 五层主视觉与层结构原样保留：不加卡片、不加 blur、不加遮罩；
#       浅色对比滤镜（contrast 1.34 / saturate 1.24 / brightness .97）原样迁移。
#     · 客户名逐字对照公开卡片上烧录的品牌（客户当面的 deck 一字不能错）：
#       集贤科技 / luwu / 商汤 / 智谱清言 / HeyCyan / 莲偶科技 —— qa 有硬编码名单闸。
_ECO = [
    ("l4", "L4", "入口与设备",   "通用助手 · 工作入口 · 可穿戴 · 机器人"),
    ("l3", "L3", "应用与结果",   "CX · 销售 · 医疗 · 教育 · 陪伴 · 翻译"),
    ("l2", "L2", "Agent 运行时", "声网对话式 AI 引擎 · TEN"),
    ("l1", "L1", "模型与感知",   "声网 Agora · 感知与 VAD"),
    ("l0", "L0", "实时基础设施", "声网 Agora · SD-RTN"),
]
# 14 家已公开联合案例（名册顺序 = 现版逐字：三家头部在前，其余 11 家照原序）
_FEATURE = [
    ("jixian",   "集贤科技",   "AI 玩具"),
    ("robopoet", "Robopoet",   "AI 陪伴机器人"),
    ("luwu",     "luwu",       "桌面级情感陪伴机器人"),
]
_MINI = [
    ("pophie", "Pophie"), ("sensetime", "商汤"), ("minimax", "MiniMax"),
    ("zhipu", "智谱清言"), ("xingye", "星野"), ("lingji", "灵机一动"),
    ("looktech", "LOOKTECH"), ("heycyan", "HeyCyan"), ("lookee", "LOOKEE"),
    ("lianou", "莲偶科技"), ("doushen", "豆神 AI"),
]
_CASES = [(n, "%sinfo-v2/case-feature-%s.webp" % (A, f), 512, 640) for f, n, _k in _FEATURE] \
    + [(n, "%sinfo-v2/case-mini-%s.webp" % (A, f), 176, 176) for f, n in _MINI]

# ── 星座墙的几何账（局部画布 1680×560 · 画布中心 (840,280) = 投影中心）──────────
#   前排：三家头部，卡 260×325（**与原片 512×640 同比 0.8 ⇒ 零裁切**），y 心 330，
#         x 420 / 840 / 1260，z = 30 − dx²/12000（极缓弧，中间最近）。
#         顺序照任务书：luwu / Robopoet / 集贤科技（左→右）。
#   后排：11 家，卡 136×136（**与原片 176×176 同比 1.0 ⇒ 零裁切**），y 心 115，
#         x = 40 + 160k（k=0…10），z = −180 − dx²/8000 ⇒ 最深 −260（合规格区间）。
#         投影后单卡 117–122px、间距 ~140px ⇒ **互不遮挡**（这是「11 张都认得出」
#         与「200×126」之间唯一能两全的一组数：200 宽在 z≈−250 上投影 173px，
#         11 张要 1900px，装不进 1680 的舞台 ⇒ 卡宽按舞台反推）。
#   摆动：绕过 (cx=840, cz=−120) 的竖轴 ±6°，周期 20s（≥18s）· 零随机源。
#   浮动：z 上叠 ±10 的正弦，周期 11s，相位 k·2π/14 —— 十四张各走各的。
_W_D = 1600.0                       # camPx 深度
_W_CX, _W_CY, _W_CZ = 840.0, 280.0, -120.0
_W_SWAY, _W_CYC = 6.0, 20.0         # 摆动幅度（度）/ 周期（秒）
_W_FAMP, _W_FPER = 10.0, 11.0       # 浮动幅度 / 周期（秒）
_W_DZ, _W_INS = 11.0, 3.0           # 卡的体厚 / 后框内缩
_W_FRONT = (260.0, 325.0, 330.0, 30.0, 12000.0)   # (w, h, y, z0, R)
_W_BACK = (136.0, 136.0, 115.0, -180.0, 8000.0)


def _w_cards():
    """14 张卡的静置几何：[(name, url, x, y, z0, cw, ch, 相位)]。
       前排三家的名册序是 集贤/Robopoet/luwu，**摆位**按任务书 luwu/Robopoet/集贤 左→右。"""
    o = []
    fw, fh, fy, fz, fR = _W_FRONT
    order = [2, 1, 0]                       # luwu · Robopoet · 集贤科技
    for k, idx in enumerate(order):
        x = 420.0 + k * 420.0
        dx = x - _W_CX
        o.append((_CASES[idx][0], _CASES[idx][1], x, fy, fz - dx * dx / fR, fw, fh, idx))
    bw, bh, by, bz, bR = _W_BACK
    for k in range(11):
        x = 40.0 + k * 160.0
        dx = x - _W_CX
        o.append((_CASES[3 + k][0], _CASES[3 + k][1], x, by, bz - dx * dx / bR, bw, bh, 3 + k))
    return o


_W_CARDS = _w_cards()


def _w_proj(x, y, z):
    """卡上一点 → 屏上（局部画布像素）· camPx 的透视除法。摆动为 0 时的静置投影。"""
    k = (_W_D - z) / _W_D
    return (_W_CX + (x - _W_CX) / k, _W_CY + (y - _W_CY) / k)


def _p7wall_poster():
    """星座墙的 **poster**（构建期离线投影 · 一个字都没有）。
       14 枚 <image> 放在各自的静置投影位（摆动 0 / 浮动取各自的 t=0 相位），
       每枚配一圈 <rect> 卡框 —— 框既是「带厚度的卡」的前缘，也让降级层里
       有真几何件（⑲c 数的是 path/rect/circle/… ，<image> 不算）。
       preserveAspectRatio="xMidYMid slice" 与 3D 的 UV 裁切**同一条规则**（居中 cover）；
       两种卡的长宽比都与原片一致 ⇒ 实际零裁切，poster 与 WebGL 是同一张图。"""
    o = []
    for nm, url, x, y, z0, cw, ch, ph in _W_CARDS:
        z = z0 + _W_FAMP * math.sin(2 * math.pi * ph / 14.0)
        a = _w_proj(x - cw / 2.0, y - ch / 2.0, z)
        b = _w_proj(x + cw / 2.0, y + ch / 2.0, z)
        o.append('<image href="%s" x="%s" y="%s" width="%s" height="%s" '
                 'preserveAspectRatio="xMidYMid slice"/>'
                 % (url, _n3(a[0]), _n3(a[1]), _n3(b[0] - a[0]), _n3(b[1] - a[1])))
        o.append('<rect class="w-rim" x="%s" y="%s" width="%s" height="%s" rx="3"/>'
                 % (_n3(a[0]), _n3(a[1]), _n3(b[0] - a[0]), _n3(b[1] - a[1])))
    return lp(*o)


def _p7detail():
    """细节层：01 ECOSYSTEM 五层地壳（eco 图双源 + L4–L0 五行 + 两句逐字）。
       ⚠ eco 图是 v2 的定稿资产，双源与 object-fit:cover 一格不动（⑩ 闸认这两条）；
         **盒按原片长宽比给**（620×349 ≈ 980/552 = 1.775）⇒ cover 实际零裁切，
         五层地壳一层都不掉（面板里 680 宽的盒配 326 高会把最底两层裁掉，实拍锤过）。
         v2 里那五枚绝对定位的层标是按 980×552 调的，面板里放不下 ⇒ 图归图、
         五行归五行（内容逐字未改），不做拉伸变形的叠标。"""
    return "".join([
        '<div class="eco-visual" style="position:relative;width:620px;height:349px;'
        'margin:4px auto 0">'
        '<img class="eco-art lt" src="%(A)sinfo-v2/ecosystem-stack-v4-light.webp" alt="">'
        '<img class="eco-art dk" src="%(A)sinfo-v2/ecosystem-stack-v4-dark.webp" alt="">'
        '<div class="eco-kicker">REAL-TIME INTELLIGENCE ECOSYSTEM</div></div>' % {"A": A},
        '<div style="margin-top:10px">'
        + "".join('<div style="display:flex;align-items:baseline;gap:14px;margin-top:4px">'
                  '<span style="flex:none;width:30px;font:700 13px/1 var(--f-mono);'
                  'letter-spacing:.1em;color:%s">%s</span>'
                  '<span style="flex:none;width:150px;font:700 16px/1.3 var(--f-cn);color:%s">%s</span>'
                  '<span style="font:400 14px/1.35 var(--f-cn);color:var(--ink-2)">%s</span></div>'
                  % (AC if _c in ("L2", "L1", "L0") else "var(--ink-3)", _c,
                     AC if _c in ("L2", "L1", "L0") else "var(--ink)", _n, _d)
                  for _cls, _c, _n, _d in _ECO)
        + '</div>',
        '<div class="d-sec"><div class="callout-chip">L0 连接 · L1 感知 · L2 运行时——'
        '<b>三层都有声网</b></div></div>',
        '<div style="margin-top:6px" class="mono-sm">'
        '从 SD‑RTN 到设备，每一层都由声网托住 · 事实截止 2026.08</div>',
    ])


page("content", "".join([
    head("案例 · 已经上岗的对话式 AI · IN PRODUCTION",
         "对话式 AI，<strong>已经上岗</strong>。", kk="kk nt"),
    # 右上大数：14 · 声网联合案例 · 均已公开（沿用现版 .case-wall-head 的字样）
    sh("settle", "left:1360px;top:140px;width:440px;height:110px;text-align:right;--i:2",
       '<div style="font:900 96px/.85 var(--f-en);letter-spacing:-.04em;color:var(--accent)">14</div>'
       '<div style="margin-top:12px;font:400 18px/1.4 var(--f-cn);color:var(--ink-2)">'
       '声网联合案例 · 均已公开</div>'),
    lab(120, 236, "01 · CASE WALL · 14 家已公开的联合案例", w=980),
    figbox(120, 272, 1680, 1680, 560, _p7wall_poster(), i=1),
    rule(850),
    # 名册行：14 家客户名逐字、顺序照现版（⑮ 闸认这一行）
    sh("flow mono-sm", "left:120px;top:876px;width:1680px;height:26px;font-size:17px;--i:5",
       " · ".join(c[0] for c in _CASES)),
    land("声网官方联合案例 · 均已公开——你的场景，多半能对上号。", y=940, w=1100),
    detail_chip(x=1460, y=938, w=340),
    detail("01 · ECOSYSTEM · 五层价值地壳，我们在哪", _p7detail(), h=620),
    # SOURCE ledger：案例墙的出处。**五层生态图没有外部来源**（Colin 自绘的价值分层），
    # 这一条是交付报告里记着的缺口 —— 细节层里那行「从 SD‑RTN 到设备…」是生态图
    # 自己的脚注，原样保留，不当 SOURCE 用。
    src("SOURCE · 声网官方联合案例 · 14 例 均已公开 · 事实截止 2026.08",
        y=1022, x=1120, w=680, align="right"),
]), steps=1, lab="wall")

# ═══ P8 · 合流 ·「三条支流，一条河」（v3 · 河放大到全舞台 · 本 deck 标杆动效页）═══
#   主图：三色支流从左侧三源头以贝塞尔曲线汇入 ONE NET 主河道，铺满 (120,272,1680,420)。
#   其下：02 三不（三行）与 03 三步（三 chip）并排；再下是两句落点 / DEMO / SOURCE / 署名。
#   hot 件 = 合流点 + ONE NET 主河道（accent 描边 + 光晕 + 合流点脉冲）。
#
#   ── v3 放大账（1.6× · 只放大「形」，介质与相位规则一格不动）─────────────────
#     图形区 820×560（vb×1）→ **1680×420**（vb×1）：河从「左半的一张图」变成
#       「横贯全舞台的一条河」——「一条河」这三个字第一次在版面上是字面意思。
#     线宽 / 盒 / 半宽全部 ×1.6（宽度是这张图的语义：河比支流宽 = 能量守恒）：
#       支流 2D packet w13→21（半宽 6.5→10.4）· 主河道 hline w4→6.4 / packet w15→24；
#       3D 支流半宽 4.0–6.5 → **6.4–10.4**，主河道 13→**20.8**、河口涌起 15→**24**，
#       涌起作用半径 80→128，河床纵深 90→144。
#     ONE NET 河道盒 350×52 rx26 → **560×84 rx42**（峰值 ±24 仍在盒内）。
#     包距同步 ×1.6：主河道 Qm 90→144（Tm .9→1.44s）、支流 Qt 270→432（Tt 2.7→4.32s）；
#       Qt = 3·Qm 的关系不动 ⇒「三条支流各占一格、轮流接力」照旧。
#     **λ 不变**（lab-kit ⑨ 的 232px —— 全家族同一种介质，放大的是形不是声）。
#     接力相位 off_k = −Lw_k + k·λ/3 由 builder 按**新的**世界弧长重算（qa ⑳rv 复算）。
#
#   ── 相位账（「同速同相接力」不是感觉，是算出来的）─────────────────────────
#   全图统一速度 v = 100 单位/秒。主河道包距 Qm = 144（dur 1.44s）；支流包距 Qt = 432（4.32s）。
#   支流 i 的负 delay：del_i = ((i×1.44 − L_i/100) mod 4.32) − 4.32，L_i = 该支流贝塞尔的采样弧长。
#   ⚠ 改任何一条曲线的控制点、或改 Qm / Qt / v，这三条 delay 必须重算（builder 会自动算，
#     但别把 L_i 写成常量）。
_NEU = [
    ("01", "不做 C 端 App",   "不和你的产品竞争用户——你的用户永远是你的。"),
    ("02", "不做自有硬件品牌", "R1 是开发套件，不是消费品——我们停在你需要的那一层。"),
    ("03", "不训基座大模型",   "多供应商开放，谁好用接谁——模型进步全部归你享受。"),
]
_STEP = [
    ("STEP 1 · 今天",     "注册即用",   "免费额度，当天就能听到第一句回话"),
    ("STEP 2 · 两周",     "PoC 共建",   "工程团队陪跑，把你的第一个真实场景跑通"),
    # 2026-08-20 仲裁 P1：「一个季度规模化上线」是承诺口吻，补限定词降成典型节奏
    ("STEP 3 · 一个季度", "规模化上线",
     "SLA、全球部署、多供应商兜底（典型节奏，视场景与合规而定）"),
]
_TRIB = [
    # (源头 y, 色, 支流标注 = ONE NET 那一行的原句逐字拆到各自的支流上)
    ( 68, LE, "Engine 的每一次打断"),
    (218, LA, "Agent 的每一次交付"),
    (368, LP, "Physical AI 的每一次唤醒"),
]
_P8_SX = 48                        # 三个源头的 x
_P8_CX, _P8_CY = 700, 225          # 合流点
_P8_MX1 = 1600                     # 主河道末端
_P8_BOX = (700, 183, 900, 84, 42)  # ONE NET 河道盒（x, y, w, h, rx）· 铺满整条主河道
_P8_QM, _P8_TM = 144, 1.44         # 主河道包距 / 周期（= v2 的 90 / 0.9 × 1.6）
_P8_QT, _P8_TT = 432, 4.32         # 支流包距 / 周期（Qt = 3·Qm 不动）
_P8_SEPX = 640                     # 细虚线域分带的 x（左「三条产品线」／右「一张实时网」）


def _p8trib_d(k, y):
    """三条支流的贝塞尔：控制点让曲线在源头端水平出发、在汇合点端水平进入（河口不折角）。"""
    c1 = 400 if k != 1 else 380
    return "M%d %d C %d %d, 520 %d, %d %d" % (_P8_SX, y, c1, y, _P8_CY, _P8_CX, _P8_CY)


def _p8fig():
    o = []
    bx, by, bw, bh, br = _P8_BOX
    # ── 细虚线域分带：左「三条产品线」／右「一张实时网」──
    o.append(dline("M%d 46 V396" % _P8_SEPX, HS, 1, 0, dash="3 9",
                   cls="mo-drift", sty="--mo-off:-24;--mo-dur:4.4s"))
    o.append(txt(330, 34, "三条产品线", "sm", size=16, anchor="middle", col="var(--ink-3)", mono=True))
    o.append(txt(1000, 34, "一张实时网", "sm", size=16, anchor="middle", col="var(--ink-3)", mono=True))
    # ── 主河道（hot）：低透明 accent 底 + accent 描边 + 光晕 ──
    o.append(halo_rect(bx, by, bw, bh, br, sc="1.05", op=".30", dur="3.6s"))
    o.append('<rect class="pop" style="--i:5;fill:%s;opacity:.12" x="%d" y="%d" width="%d" '
             'height="%d" rx="%d"/>' % (AC, bx, by, bw, bh, br))
    o.append(box(bx, by, bw, bh, br, hot=True, i=5))
    # ── 三条支流：实线三色 + 能量包（相位按弧长算，见页头推导）──
    for k, (y, col, label) in enumerate(_TRIB):
        d = _p8trib_d(k, y)
        ln = path_len(d)
        delay = ((k * _P8_TM - ln / 100.0) % _P8_TT) - _P8_TT
        o.append(packet(d, _P8_QT, "%.2fs" % _P8_TT, delay="%.3fs" % delay, col=col,
                        w=21, seg=38, op=".34", i=2 + k))
        o.append(curve(d, col, 4, 2 + k))
        o.append('<circle class="pop" style="--i:%d;fill:%s" cx="%d" cy="%d" r="10"/>'
                 % (2 + k, col, _P8_SX, y))
        o.append(txt(_P8_SX, y - 28, label, "sm", size=17, col="var(--ink-2)"))
    # ── 主河道能量包：包距 144 ⇒ 三条支流各占一格，轮流接力（同速 v=100）──
    o.append(packet("M%d %d H%d" % (_P8_CX, _P8_CY, _P8_MX1), _P8_QM, "%.2fs" % _P8_TM,
                    delay="0s", col=AC, w=24, seg=32, op=".38", i=6))
    o.append(hline(_P8_CX, _P8_MX1, _P8_CY, AC, 6.4, 6))    # 主河道比支流粗一档
    o.append(ah_r(_P8_MX1 + 20, _P8_CY, AC, 14))
    # ── 合流点：脉冲事件标（原语 ③）──
    o.append('<circle class="mo-halo" style="--mo-sc:2.6;--mo-op:.45;--mo-dur:3.0s" cx="%d" cy="%d" '
             'r="14" fill="none" stroke="%s" stroke-width="2" opacity="0"/>' % (_P8_CX, _P8_CY, AC))
    o.append('<circle class="pop mo-pulse" style="--i:6;fill:%s;--mo-hi:1;--mo-lo:.45;--mo-dur:2.4s" '
             'cx="%d" cy="%d" r="14"/>' % (AC, _P8_CX, _P8_CY))
    o.append(txt(_P8_CX, 162, "合流点", "sm", size=16, anchor="middle", col=AC, mono=True))
    # ── 主河道题注（河道自己不携带文字）──
    o.append(txt(bx + 16, 306, "ONE NET", "lbl", size=16, col=AC))
    o.append(txt(bx + 16, 342, "SD-RTN 软件定义实时网络", "ttl", size=26, col=AC))
    o.append(txt(bx + 16, 374, "全球 200+ 节点 · 端到端毫秒级", "sm", size=18))
    # ── 迷你图例（真线样）──
    o.append(legend(14, 400, [("solid", "Engine", 4, LE), ("solid", "Agent", 4, LA),
                              ("solid", "Physical AI", 4, LP),
                              ("fast", "ONE NET 主河道", 6.4, AC)], gap=40, size=14))
    return _lpsplit(o)


page("content", "".join([
    head("合流 · 为什么是声网 · 怎么开始 · ONE NET", "三条支流，<strong>一条河</strong>。"),
    # 区 01 · ONE NET（全舞台合流大图）
    lab(120, 236, "01 · ONE NET · 三条支流汇入一条河"),
    figbox(120, 272, 1680, 1680, 420, _p8fig(), i=1),
    # 区 02 · NEUTRALITY（左）/ 03 · START（右）—— 并排，收口线 rule(850) 之上
    lab(120, 708, "02 · NEUTRALITY", w=760),
    # 行高账：padding 5×2 + 20px/1.3 的键行 26 + 1px 分隔 = 37/行 ⇒ 三行 110px，
    # 734+110 = 844 —— 收在 content 背景板那条 accent 细线（stage y848–852）之前。
    sh("", "left:120px;top:734px;width:760px;height:112px",
       '<div class="rows">' + "".join(
           '<div class="r flow" style="--i:%d;padding:5px 0;gap:18px">'
           '<span class="n" style="width:44px;font-size:21px">%s</span>'
           '<span class="k" style="width:200px;font-size:20px;line-height:1.3">%s</span>'
           '<span class="v" style="font-size:16px">%s</span></div>' % (2 + _i, _no, _n, _d)
           for _i, (_no, _n, _d) in enumerate(_NEU)) + '</div>'),
    lab(960, 708, "03 · START", w=840),
    ] + [
    sh("rise", "left:960px;top:%dpx;width:840px;height:38px;--i:%d" % (734 + _i * 38, 2 + _i),
       '<div class="chip" style="display:flex;align-items:center;gap:14px;width:100%%;'
       'margin:0 0 4px 0;padding:6px 20px;box-sizing:border-box">'
       '<span style="font:500 13px/1 var(--f-mono);letter-spacing:.1em;color:var(--accent);'
       'width:150px;flex:none">%s</span>'
       '<span style="font:700 19px/1.2 var(--f-cn);color:var(--ink);width:118px;flex:none">%s</span>'
       '<span style="font:400 14px/1.4 var(--f-cn);color:var(--ink-2);flex:1">%s</span></div>'
       % (_t, _n, _d))
    for _i, (_t, _n, _d) in enumerate(_STEP)
    ] + [
    rule(850),
    # 落点一：合流大图的收口句（逐字）
    sh("flow", "left:120px;top:876px;width:900px;height:52px;font:400 24px/1.6 var(--f-cn);"
       "color:var(--ink);--i:6",
       "都跑在同一张 <strong style='color:var(--accent)'>SD-RTN 软件定义实时网络</strong>上"
       "——全球 200+ 节点，端到端毫秒级。"),
    # 2026-08-20 仲裁 P0：「OpenAI 选择我们」是不可核实的因果叙述，改为可核实的事实陈述
    sh("flow", "left:1000px;top:876px;width:800px;height:32px;font:500 20px/1.5 var(--f-cn);"
       "color:var(--accent);text-align:right;--i:5",
       "2024 OpenAI Realtime API 发布 · 声网为全球首批合作伙伴。"),
    # CTA（纯 mono 文本，不做假链接样式）
    sh("flow mono-sm", "left:1000px;top:920px;width:800px;height:24px;text-align:right;--i:6",
       "DEMO / 文档 · agora.io › 对话式 AI · 联系团队"),
    # 落点二 + 页脚同一基线三栏：land（左） · SOURCE ledger（中） · 署名 rail（右）
    land("让陪伴自然，让生意<strong>成单</strong>。", w=460),
    # P8 的数字（200+ 节点 / 毫秒级 / OpenAI 首批）都是 P2 那份口径的回指 ⇒ 来源同 P2；
    # 本页没有自己的样本或时间窗 ⇒ 该段留空（缺口已记入交付报告）。
    src("SOURCE · 声网官网 / IR 公开口径 · 事实截止 2026.08", x=560, w=580, align="right"),
    rail("姚光华 COLIN · SHENGWANG.CN · COLINYAO.COM", x=1200, w=600, align="right"),
]), lab="river")



# ═══════════════════════════════════════════════════════════════════════════
# LAB 层 · 场景几何（五枚 · 每一个坐标都取自上面各页自己的常量，一个不新造）
# ───────────────────────────────────────────────────────────────────────────
#   投影锁（lab-kit ⑤ mkLock）是本层的地基：页上的 2D 点 (x,y) 抬到深度 z 之后
#   先按 (D−z)/D 预缩放，透视除法正好把这一档除回去 ⇒ **投影落点与 2D 逐像素相同**。
#   于是「有真深度」与「标签一格不挪」不再互斥 —— 本 deck 五页的图上全是标签，
#   这条不成立的话，3D 一起来页上的字就全指空了。
#
#   ⚠ 流速账（A 档 110px/s 是**屏上**的速度，不是世界坐标里的）：投影锁把
#     页坐标按 k=(D−z)/D 放大进世界，所以世界弧长 = ∫k·ds_page。
#     `_lock_len()` 把两个长度都算出来，`spd_world = 110 × Lw/Lp` ⇒
#     波峰在**屏上**走满 Lp 恰好用 Lp/110 秒。data-lab-spd 摊的是屏上速度。
_SPD_A = 110.0                     # A 档基准（px/s · 与旗舰同一个数）
_SPD_TOL = 0.30                    # ±30%
_CLR_PAD = 0.5                     # 构建期声明与运行时实测允许的误差


def _lockpt(x, y, z, w, h, D):
    """mkLock 的 Python 同解（世界坐标 · y 取负，与 three 同）"""
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


def _spd_world(pts, w, h, D, spd=_SPD_A):
    Lp, Lw = _lock_len(pts, w, h, D)
    return spd * Lw / (Lp or 1.0), Lp


def _pk3(pts):
    """世界折线打包成 "x,y,z;…"（构建期算一遍，运行时不再算第二遍）"""
    return ";".join("%s,%s,%s" % (_n3(p[0]), _n3(p[1]), _n3(p[2])) for p in pts)


def _arr3(xs):
    return "[" + ",".join(_n3(v) for v in xs) + "]"


def _lerp_line(a, b, n):
    return [(a[0] + (b[0] - a[0]) * i / (n - 1.0), a[1] + (b[1] - a[1]) * i / (n - 1.0),
             a[2] + (b[2] - a[2]) * i / (n - 1.0)) for i in range(n)]


# ── ① 声场球（P1）：与 lab P1 **逐字同参** —— 球心 / 半径 / 谐波 / 自转全部现取 ──
#    构图账（lab 的原注）：球心 (1555,578) · 屏上半径 218 ⇒ 极值轮廓
#    x1322–1788 / y345–811。本页墨迹右缘是 kicker 的 x875（y197–223），
#    主标右缘 x684 —— 球离最近的一处字 447px，封面构图上它坐在右侧留白正中。
_V_POSTER = _LAB._voice_poster()

# ── ② SD-RTN 地球（P2）· 与 lab P21 **逐字同参**（构图 / 相机 / poster 全部现取）──
#    球心 (1470,500) · 屏上半径 250 ⇒ 限界 x1220–1720 / y250–750；
#    弧的外包络（1.243r，见 lab 的 buildArc lift）投影半径 312 ⇒ x1158–1782 / y188–812，
#    整片仍在矩形 (1150,180,640,640) 之内。
#    ⚠ 地球是**球面场景**（camSphere），不是 px 投影锁场景 ⇒ 它不进 ⑳clr 的
#      「两条算路对表」通道（与 P1 声场球同例，也与旗舰 lab 的 ㉒ 闸同例）。
#      它自己的净空由 ⑳globe 单验：把外包络圆与页上字形行框逐处量，下限 16px。
_G_POSTER = _LAB.GPOSTER
_G_R = _LAB.GGR
_G_CX, _G_CY = _LAB.GCX, _LAB.GCY
_G_LIFT = 1.243                            # 弧的最大抬升倍率（= lab buildArc 的 0.028+0.215）
# 球面半径 R 的限界在屏上的投影半径：FPX·R / sqrt(|C|²−R²)
_G_ENV = _LAB.FPX * _G_LIFT / math.sqrt(_LAB.GCAM.CD ** 2 - _G_LIFT ** 2)
_G_CLR = 16.0                              # 地球净空下限（加法层 16px 规则）


# ── ③ 空间生长（P3）· 几何逐条抄 _p3fig() ─────────────────────────────────
#   _GW_BASEY / _GW_TOP 在 P3 页那一段就定死了（2D 与 3D **共用同两个数**）。
_GW_D, _GW_HALF = 1500.0, 480.0           # v3：矩形高 480→600，雾的半程跟着放一档
_GW_BOXDZ = 52.0                          # 三只产品线盒的体厚（盒 300×112→380×140，体厚跟一档）
_GW_AUXZ = -150.0                         # 辅件（TEN / 评测 / 转录）退到景深里
_GW_AUXDZ = 26.0
_GW_ZTOP = 8.0                            # 主干抵达产品线盒时的深度（贴着版面）
# 三股主干的半宽是**沿程函数**：基面深处 4.0 → 盒底 8.0（= 2D packet 的半宽 8.0，
# 页上 packet w 从 13 放到 16 ⇒「不许比 2D 更近」仍是平手）。透视本来就把深处收窄
# （D/(D−z)），叠加后近 2× 生长 ——「从底座抽出来向上生长」因此在帧上读得出，
# 而不是一根等粗的棍。
# 净空探针与运行时 pad 一律**保守取最大 8.0**（两条算路同一个数 ⇒ 不会各算各的）。
_GW_W0, _GW_W1 = 4.0, 8.0
_GW_WMAX = _GW_W1
_GW_N = 90
# ── 底座 = **纵深基面**（不是一只盒）· 几何账 ──────────────────────────────
#   页上那只 rect(0,450,1668,86) 里坐着两行字（fig y468–488 / 500–524）——
#   任何「向后拉伸」的框都会绕画布中心缩进去、正好压在那两行上（v2 实拍锤过：
#   deck=210 时后框底边落在字上，净空 0）。所以底座**不做体**：
#     · 前框锁死在页上那只 rect 上（hot · 一个像素不动）；
#     · 纵深由它**身后**的一片透视栅格承担 —— 栅格整片坐在
#       fig y402–448 那条**无字空带**里（上方 aux 盒文字止于 y354，
#       下方底座顶沿 y450），横向止于 fig x1450（右边 y426 那行域分带注记从
#       x1460 起）。
#   栅格是真的地平面：screen = 消失点 + (近边 − 消失点)·d0/(d+d0)，
#   d 是 0..1 的深度参数，z = −_GW_ZFAR·d ⇒ 深度雾把远端自然压弱。
_GW_GN, _GW_GM = 8, 15                    # 栅格：8 道横 / 15 道竖
_GW_GY0, _GW_GY1 = 448.0, 388.0           # 近边 y / 消失点 y（fig）
_GW_GX0, _GW_GX1 = 10.0, 1450.0           # 近边左右缘（fig）
_GW_GXV = 840.0                           # 消失点 x（fig · 画布中线）
_GW_GD0 = 0.3043                          # 透视常数：d=1 时落在 fig y402（= 近边到消失点的 23.3%）
_GW_ZFAR = 760.0                          # 栅格最远处的深度


def _gw_grid_pt(xj, d):
    """基面上一点（fig 坐标 + 深度）—— 真地平面的解析式，不是手调出来的"""
    f = _GW_GD0 / (d + _GW_GD0)
    return (_GW_GXV + (xj - _GW_GXV) * f, _GW_GY1 + (_GW_GY0 - _GW_GY1) * f, -_GW_ZFAR * d)


def _gw_grid():
    """8 道横 + 15 道竖 —— 每一道都是一条独立折线（世界坐标里各自成线）"""
    rows, cols = [], []
    for i in range(_GW_GN):
        d = i / (_GW_GN - 1.0)
        rows.append([_gw_grid_pt(_GW_GX0 + (_GW_GX1 - _GW_GX0) * j / 40.0, d) for j in range(41)])
    for j in range(_GW_GM):
        xj = _GW_GX0 + (_GW_GX1 - _GW_GX0) * j / (_GW_GM - 1.0)
        cols.append([_gw_grid_pt(xj, i / 24.0) for i in range(25)])
    return rows + cols


def _gw_trunk(tx):
    """主干：从基面深处抽出来，一路生长到产品线盒 —— 投影锁 ⇒ 屏上仍是页上那条竖线"""
    return _lerp_line((tx, _GW_BASEY - 2.0, -_GW_ZFAR * 0.55), (tx, _GW_TOP, _GW_ZTOP), _GW_N)


# ── ④ 双向声带（P4）· 几何与常量**整块现取自旗舰** ─────────────────────────
#    矩形与 lab P4 逐字同参 (120,268,1680,352) ⇒ `_d_lane` / `_D_*` / `_SPD_P4`
#    直接就是本页的真相，一个数都不在这里重算。净空名册同理（`_LAB._P4INK`）。
_D_D = 1400.0                             # makeDuplex 的 camPx 深度（旗舰写死的那一个）
_D_HW = 11.0                              # 声带半宽（= lab_k 的 d.hw）

# ── ⑤ 五脑区大脑（P5）· 几何与常量**整块现取自旗舰** ────────────────────────
#    矩形与 lab P17 逐字同参 (120,282,1680,580) ⇒ `_brain_fig()` 与 K.b 原样可用。
#    ⚠ 大脑绕竖轴 ±12° 摇摆（周期 17s）⇒ 它的屏上限界是**随时间变的**；
#      净空因此不走「两条算路对表」，走 ⑳swept：构建期算出**扫掠包络**
#      （轮廓 × 摇摆区间 × 厚度透视），运行时定拍到 seek(6) 复核。
_B_D = 1350.0                             # makeBrain 的 camPx 深度
_B_TMAX = 132.0                           # 半厚度上界（= lab_k 的 b.tmax）
_B_SWAY = 12.0                            # 摇摆幅度（度）
_B_SWAYP = 17.0                           # 摇摆周期（秒）


def _lockbox(x, y, w, h, z0, dz, ins, W, H, D):
    """锁住的盒体：前框 = 页上那只 rect@z0；后框 = 同一只 rect 内缩 ins @(z0−dz)。
       两枚都过投影锁 ⇒ 屏上落点由这四个数决定，深度只影响雾与遮挡。
       （P6 加法层的屏幕框在用；波B 之前 P5 的能力盒也走这一路。）"""
    f = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    b = [(x + ins, y + ins), (x + w - ins, y + ins), (x + w - ins, y + h - ins),
         (x + ins, y + h - ins), (x + ins, y + ins)]
    return (_lock_path([(q[0], q[1], z0) for q in f], W, H, D),
            _lock_path([(q[0], q[1], z0 - dz) for q in b], W, H, D),
            f, b)


# ── ⑥ 三条支流一条河（P8 · 标杆）· 几何逐条抄 _p8fig() ────────────────────
#   v3：所有宽度 ×1.6（形放大 1.6×，介质不变 —— λ 仍是 lab-kit ⑨ 的 232px）。
_RV_D, _RV_HALF = 1200.0, 330.0
_RV_ZSRC = -270.0                         # 三条支流的源头深度（在纵深里）
_RV_ZMEET = 0.0                           # 汇合点 = 版面平面（主河道就在眼前）
# ── 能量守恒：河**比支流宽**（否则「一条河 = 三条之和」在帧上读不出来）──────
#   支流半宽 = 沿程函数 6.4（源头）→ 10.4（河口）：透视本来就把源头收窄
#   （D/(D−z) = 1200/1470 = .816），叠加后源头→河口约 2× 生长，正是「越近越宽」。
#   10.4 = 页上 2D packet 的半宽（stroke 21）⇒「不许比 2D 更近」不破。
#   主河道半宽 20.8（河道盒 rx42 · 高 84 ⇒ 峰值 ±24 仍在盒内），且 floor 抬到 .55 ——
#   河是稳定的，脉动归支流。河口 128px 内再抬到 24（三条流交出去的那一处要看得见「合」）。
#   净空探针与运行时 pad：支流保守取最大 10.4、主河道取最大 24（两条算路同一个数）。
_RV_WT0, _RV_WT1 = 6.4, 10.4              # 支流半宽：源头 → 河口（= v2 的 4.0 / 6.5 ×1.6）
_RV_WT = _RV_WT1                          # 探针 / pad 的保守上界
_RV_WM = 20.8                             # 主河道基准半宽（= 13 ×1.6）
_RV_WMOUTH = 24.0                         # 河口涌起的峰值半宽（= 15 ×1.6）
_RV_WACC = 128.0                          # 涌起的作用半径（沿主河道弧长 px · = 80 ×1.6）
_RV_WMAX = _RV_WMOUTH                     # 探针 / pad 的保守上界
_RV_MFLOOR = 0.55                         # 主河道幅度地板（全局档 0.30 ⇒ 河更稳）
_RV_N = 140
_RV_LAM = _LAB._AS_LAM                    # 波长逐字取 lab-kit ⑨ ⇒ 与全家族同一种介质


def _rv_trib(k, y):
    """一条支流的空间中心线：页上那条贝塞尔 + 从源头到汇合点的深度爬升。
       xy 逐点取自 _p8trib_d(k, y)（同一串控制点），z 按弧长比例线性收到 0。"""
    d = _p8trib_d(k, y)
    s = d.replace(",", " ")
    for c in "MC":
        s = s.replace(c, " " + c + " ")
    t2 = s.split()
    i = t2.index("C")
    p0 = (float(t2[1]), float(t2[2]))
    p1 = (float(t2[i + 1]), float(t2[i + 2]))
    p2 = (float(t2[i + 3]), float(t2[i + 4]))
    p3 = (float(t2[i + 5]), float(t2[i + 6]))
    o = []
    for j in range(_RV_N):
        t = j / (_RV_N - 1.0)
        o.append((_cub(p0[0], p1[0], p2[0], p3[0], t),
                  _cub(p0[1], p1[1], p2[1], p3[1], t),
                  _RV_ZSRC + (_RV_ZMEET - _RV_ZSRC) * (t * t * (3 - 2 * t))))
    return o


def _rv_main():
    return _lerp_line((float(_P8_CX), float(_P8_CY), _RV_ZMEET),
                      (float(_P8_MX1), float(_P8_CY), _RV_ZMEET), 60)


def _rrect(x, y, w, h, r, per=9):
    """圆角矩形 → 闭合折线（页上那只 rx42 的 ONE NET 河道盒本人）"""
    o = []
    for cx, cy, a0 in ((x + w - r, y + r, -90.0), (x + w - r, y + h - r, 0.0),
                       (x + r, y + h - r, 90.0), (x + r, y + r, 180.0)):
        for i in range(per + 1):
            a = (a0 + 90.0 * i / per) * math.pi / 180.0
            o.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    o.append(o[0])
    return o


# ── ⑦ 走出屏幕（P6）· 声流中心线（几何常量表在 LAB_RECTS 之前 · 那里要用）──────
def _ex_path():
    """声流的中心线（局部像素 · 含 z）—— 两段折线合成一条序列"""
    return _lerp_line(_EX_P0, _EX_P1, _EX_N0)[:-1] + _lerp_line(_EX_P1, _EX_P2, _EX_N1)


# ── 墨迹名册（每页 3D 矩形之内的**字形行框** · Range.getClientRects 实测）──────
#   这张表是「不压字」从纪律变成机器判据的地方：qa 的 ⑳clr-a 闸拿活 DOM 逐处对表，
#   改了文案而没同步这张表 ⇒ 当场报。坐标是舞台坐标（1920×1080）。
_INK = {
    # ② 地球（P2）：矩形 (1150,180,640,640) 里**没有一处页上的字**（左栏止于 x1050、
    #   角注在 y872、land 在 y940）。登记的是它的四个真实对手 —— 四卡右列的说明行 /
    #   IDC 注末行 / 地球角注 / 页码 8/8 ——⑳globe 拿它们量 16px。
    #   ⚠ 细节层（.detail）里的字**不登记**：面板压在 canvas 之上，3D 压不到它。
    2: [(1759.2, 44, 36.7, 22), (669.3, 149, 266.6, 76), (935.9, 149, 66.6, 76),
        (624, 415.3, 340, 22), (624, 536.7, 284.1, 100), (733.3, 717, 268.9, 25),
        (1464.6, 872, 335.4, 20), (802, 955, 145, 32), (1691.6, 949, 89.4, 20),
        (1033, 1022, 767, 22)],
    # ③ 空间生长（P3）：全舞台 (120,272,1680,600) 内的字形行框（构建后实测填表）
    3: [(386.7, 282, 66.6, 20), (328.2, 349, 183.6, 31), (340.9, 398, 158.3, 17),
        (438, 502, 272, 19), (932.2, 282, 55.5, 20), (876, 349, 168, 31),
        (908, 398, 104, 17), (978, 502, 221, 19), (1438.9, 282, 122.1, 20),
        (1444, 349, 112, 31), (1429.8, 398, 140.5, 17), (1518, 502, 221, 19),
        (183.6, 579, 152.8, 23), (182.9, 612, 154.2, 17),
        (713.6, 579, 152.8, 23), (738.3, 612, 103.3, 17),
        (1267, 579, 126, 23), (1278.3, 612, 103.3, 17),
        (150, 740, 416.3, 21), (150, 771, 735.8, 23),
        (180, 820, 75.5, 16), (396, 820, 68.5, 16), (599, 820, 100.4, 16),
        (881, 820, 136.1, 16), (1592.4, 684, 187.6, 18)],
    # ④ 双向声带（P4）：矩形 (120,268,1680,352) 内的字形行框（构建后实测填表）——
    #   三条 lane 的序号圈 / 听想说 / LISTEN THINK SPEAK / 三行说明，
    #   加上带上的四处注记（用户插话 / 每格一次「要不要出声」/ 收声让位 / 340ms / NOW）。
    4: [(139, 291, 10, 20), (174, 283, 28, 31), (174, 321, 57.7, 17),
        (272, 288, 602.2, 25), (1204, 295, 60, 20),
        (139, 405, 10, 20), (174, 397, 28, 31), (174, 435, 48.1, 17),
        (272, 402, 459.6, 25), (1591, 410, 165, 17),
        (139, 519, 10, 20), (174, 511, 28, 31), (174, 549, 48.1, 17),
        (272, 516, 265.2, 25), (1222, 523, 60, 20),
        (1220, 498, 62.3, 22), (964.5, 296, 31.1, 18)],
    # ⑤ 五脑区大脑（P5）：矩形 (120,282,1680,580) 内的字形行框 —— 五枚区序号 +
    #   五组「区名 + 序号」引线标 + INPUT / 客户语音 + 输出 · 最佳回复 + 每 0.8 秒。
    5: [(971, 723, 18, 20), (881, 659, 18, 20), (721, 489, 18, 20),
        (911, 523, 18, 20), (1151, 479, 18, 20),
        (360, 385, 126, 23), (470.4, 365, 15.6, 17),
        (339, 561, 147, 23), (470.4, 541, 15.6, 17),
        (1280, 417, 168, 23), (1280, 397, 15.6, 17),
        (1280, 711, 168, 23), (1280, 691, 15.6, 17),
        (1280, 783, 189, 23), (1280, 763, 15.6, 17),
        (199.9, 661, 48.1, 17), (192, 760, 64, 17),
        (1568.3, 538, 165.3, 27), (1526, 456, 70, 18)],
    # ⑦ 加法层的四邻（Range.getClientRects 实测 · 舞台坐标）：kicker 行 /
    #   主标末字行（页上主标的右缘就在这一行里）/「01 · R1 KIT」小节标 / 页码 6/8。
    #   与另外五页不同 —— 这四只盒**没有一只落在 3D 矩形之内**（矩形 740,140,1060,100
    #   本来就是标题右侧那条空带）。登记它们不是为了「盖住矩形内的字」，
    #   而是为了让 ⑳clr 有四个真实的对手去量 16px。
    6: [(120.0, 89.0, 760.0, 26.0), (653.1, 149.0, 66.6, 76.0),
        (120.0, 236.0, 122.6, 20.0), (1759.2, 47.0, 40.8, 17.0)],
    # ⑧ 星座墙（P7）：矩形 (120,272,1680,560) 里**没有一处页上的字**（大数在 y140–250、
    #   名册在 y876、land 在 y940）。登记的是它的四邻 —— ⑳clr 拿它们量 16px。
    7: [(120, 89, 643.2, 26), (120, 149, 349.4, 76), (469.4, 149, 266.6, 76),
        (735.9, 149, 66.6, 76), (1702.6, 120, 97.4, 120), (1604, 235.6, 196, 20),
        (120, 237, 367.1, 18), (120, 876, 1421.2, 22), (150, 955, 779.8, 32),
        (1691.6, 949, 89.4, 20), (1175.8, 1022, 624.3, 22)],
    8: [(410, 290, 80, 21), (1080, 290, 80, 21),
        (168, 297, 159.7, 19), (168, 447, 151.2, 19), (168, 597, 189.9, 19),
        (796, 418, 48, 21), (836, 562, 82.9, 21), (836, 590, 313.4, 30),
        (836, 630, 246.5, 20), (184, 664, 43.6, 16), (353, 664, 36.6, 16),
        (509, 664, 68.5, 16), (744, 664, 107.9, 16)],
}
# ── 已知穿越名册（P8 · 三行支流标注）──────────────────────────────────────
#   `txt(_P8_SX, y−28, label)` 把标注钉在源头点正上方 28px，而支流曲线从源头就往
#   右上爬 ⇒ **页上那条 2D 曲线本来就从这三行字底下穿过**（2D 半宽 10.4px）。
#   3D 的流带在同一处更窄（透视把深处的带子收窄了）⇒ 比 2D 还让出一点。
#   这不是「3D 压字」，是页面既有的图文叠压关系；把它写成名册**正面登记**，
#   而不是把它混进净空名册去把下限拖成负数。qa 的 ⑳clr-a 闸认这张表。
_INK_SKIP = {
    # ④ P4（借来的旗舰几何）：上行声带在 fig x1104 处**擦到**「收声让位」行的左下角
    #   （ribbon 顶点落在盒内 1.7px）。几何是旗舰 P4 本人（`_D_*` 现取，一个数没改），
    #   字也是旗舰本人 —— 这层叠压关系随图一起继承（旗舰自己的 `_P4INK` 只登记三行
    #   说明）。带子在字**之下**（canvas 坐在 .pp 之下），15px mono 的可读性不受影响。
    #   **正面登记**，而不是把它混进净空名册去把下限拖成负数。
    4: [(1222, 523, 60, 20)],
    # ⑤ P5：五枚区序号本来就**印在脑体之内**（2D 的 `_brain_fig` 也是这么画的）——
    #   它们是「这一块是哪个区」的贴标，不是被 3D 压到的字。
    5: [(971, 723, 18, 20), (881, 659, 18, 20), (721, 489, 18, 20),
        (911, 523, 18, 20), (1151, 479, 18, 20)],
    8: [(168, 597, 189.9, 19)],
}
for _p8, _bs in _INK_SKIP.items():
    _INK[_p8] = [b for b in _INK[_p8] if tuple(b) not in {tuple(x) for x in _bs}]

# ── 净空下限：**「3D 不许比它替换掉的 2D 更近」**─────────────────────────────
#   加法层（lab 的 P5/P15/P16/P22）可以要求 16px，因为它们画在版面之外的空档里。
#   本 deck 五枚全是**替换**：3D 落在页上那张图原来的位置上，而那张图本来就是
#   贴着标签画的。所以下限逐页取「页上 2D 与同一批字形的既有净空」，
#   每一条都记下**证人**（哪两只盒），qa 的 ⑳clr 闸两头对表。
#   每一条都记下**证人**（哪一处几何 vs 哪一只字盒）与页上 2D 的同处净空，
#   报告里逐条摆出来 —— 这一闸真正管的是「不许比 2D 更近」。
_CLR = {
    # ② 地球：页上这块地本来没有图（左栏四大数占 x120–1050）⇒ 走**加法层 16px 规则**，
    #   不走「不许比 2D 更近」的平手规则。对手见 _INK[2] 的四邻。
    2: (_G_CLR, "加法层 · 16px 规则 · 证人 = 弧外包络圆（R=%.1f · 心 1470,500）"
                "vs 左栏四大数说明行 / IDC 注 / 地球角注 / 页码" % _G_ENV),
    3: (8.0,  "产品线盒顶 y312（fig y40）vs 其上 mono 名（ENGINE 行底 stage y302）"
              "；2D 盒画在同一处 ⇒ 平手"),
    # ④ 双向声带：两条带没过投影锁 ⇒ 探针自己做透视除法（见 _d_build 的注）。
    #   两条算路因此**逐位对得上**（解析 13.60 / 运行时 13.60）。
    #   另有一条**更硬**的正面断言（ⓗ）：舞台起点 x900 ≥ 三行说明最右墨迹 874 + 16。
    4: (13.5, "3D 截断竖线上端（fig y60 · 页 x1200）vs「用户插话」行 (1204,295,60,20)"
              " ⇒ 13.60px；页上那根 2D 竖线只画到 fig y106，3D 往上多探 46px（旗舰几何）"),
    # ⑤ 大脑：外包络只比母形轮廓外扩 ~2.4px（厚度最大处离轮廓最远，两件事互相抵消），
    #   最近的一处是输入声流末端 vs「客户语音」行 —— 9.24px。
    5: (9.0,  "输入声流（_BRAIN_IN · 摇摆 ±12° 的最外缘）vs「客户语音」行 (192,760)"
              " ⇒ 9.24px；页上那条 2D 曲线在同一处更远 ⇒ 3D 没有比 2D 更近"),
    7: (16.0, "加法层 · 16px 规则 · 证人 = 卡片投影包络（摆动 ±6° × 浮动 ±10 扫掠）"
              "vs 右上大数 14 / 名册行 / land / 页码"),
    8: (13.5, "支流带在源头处（保守 pad = 河口峰值半宽 10.4）vs 其上 28px 的支流标注行"
              "：24−10.4 = 13.6px；页上 2D packet 的半宽也正是 10.4 ⇒ 逐像素平手。"
              "真实屏上半宽在源头只有 8.49（透视收窄 1200/1470）⇒ 3D 实际还让出 1.9px"),
}
if P6_EXIT:
    # 加法层走 **16px 规则**（版面之外的空档，不走「不许比 2D 更近」的平手规则）。
    # 证人 = kicker 行底 y115（.sh 盒底 y120）vs 屏幕框顶 y154 ⇒ 39.0px。
    _CLR[6] = (16.0, "加法层 · 16px 规则 · 证人 = kicker 行底 y115（盒底 y120）"
                     "vs 屏幕外框顶 y148 ⇒ 33.0px")
else:
    del _INK[6]
# P4 的 hot 是抽屉 chip（本页唯一「可以按下去」的东西）：它绝不许被 3D 压。
# v3 波B：chip 从 04 · OPEN 那行（step1）搬到 land 行右侧并**常显** ——
# 细节层占了 data-step=1，本页唯一的 action 不能再藏在分步里。
# chip 实测盒 (1161.6,938,258.4,42)，而 P4 的 3D 矩形是 (120,268,1680,352) ⇒ 相距 318px。
_P4_CHIP = (1161.6, 938.0, 258.4, 42.0)
_P4_CHIP_CLR = 16.0


# ═══════════════════════════════════════════════════════════════════════════
# LAB 层 · 五枚场景的运行时（只写语义几何 —— 地基件全部来自旗舰的 lab-kit）
# ═══════════════════════════════════════════════════════════════════════════
INFO_SCENES = r"""
/* ═══ info 场景共用小件（五行胶水 · 基建一件不重写）════════════════════════ */
const AS_K = 6.2831853 / AS.lam;
function asEnv(u){                      /* lab-kit ⑨ 解析包络的 JS 同解（与 AS_VS 逐行同式） */
  return 0.5 + 0.5*( AS.a[0]*Math.sin(AS_K*AS.f[0]*u+AS.ph[0])
                   + AS.a[1]*Math.sin(AS_K*AS.f[1]*u+AS.ph[1])
                   + AS.a[2]*Math.sin(AS_K*AS.f[2]*u+AS.ph[2])
                   + AS.a[3]*Math.sin(AS_K*AS.f[3]*u+AS.ph[3]) );
}
function unpk3(s){                      /* "x,y,z;…" → 世界折线（构建期算好，运行时不重算） */
  return s.split(';').map(t => { const q = t.split(','); return [+q[0], +q[1], +q[2]]; });
}
function iLine(pts, mat){ const g = stripGeo(pts); fillAH(g,1,0);
  const o = new THREE.Line(g, mat); o.frustumCulled = false; return o; }
function iSegs(segs, mat){ const g = segGeo(segs); fillAH(g,1,0);
  const o = new THREE.LineSegments(g, mat); o.frustumCulled = false; return o; }
function iPts(pts, mat){ const g = stripGeo(pts); fillAH(g,1,0);
  const o = new THREE.Points(g, mat); o.frustumCulled = false; return o; }
/* 闭合折线 → 虚线段表：3D 里的「虚线域」，dash/gap 逐字取页上的 stroke-dasharray */
function dashSegs(pts, dash, gap){
  const out = []; let on = true, rem = dash;
  for(let i = 0; i < pts.length-1; i++){
    const a = pts[i], b = pts[i+1];
    const L = Math.hypot(b[0]-a[0], b[1]-a[1], b[2]-a[2]);
    let t0 = 0;
    while(L - t0 > 1e-6){
      const step = Math.min(rem, L - t0), t1 = t0 + step;
      if(on){
        const P = (t) => [a[0]+(b[0]-a[0])*t/L, a[1]+(b[1]-a[1])*t/L, a[2]+(b[2]-a[2])*t/L];
        const p0 = P(t0), p1 = P(t1);
        out.push([p0[0],p0[1],p0[2], p1[0],p1[1],p1[2]]);
      }
      rem -= step; t0 = t1;
      if(rem <= 1e-6){ on = !on; rem = on ? dash : gap; }
    }
  }
  return out;
}
/* 段加密：`geoClr` 逐**顶点**量净空 —— 一只只有四个角的框会把「边中段离字最近」
   这件事整个漏掉（本轮实测：P3 的盒框运行时报 12.25px，构建期解析是 8.0px）。
   把每一段切成 ≤step 的小段，渲出来一模一样，而顶点密到足以代表整条边。 */
function denseSegs(segs, step){
  const out = [], st = step || 12;
  for(let i = 0; i < segs.length; i++){
    const s = segs[i];
    const L = Math.hypot(s[3]-s[0], s[4]-s[1], s[5]-s[2]);
    const n = Math.max(1, Math.ceil(L / st));
    for(let k = 0; k < n; k++){
      const a = k/n, b = (k+1)/n;
      out.push([s[0]+(s[3]-s[0])*a, s[1]+(s[4]-s[1])*a, s[2]+(s[5]-s[2])*a,
                s[0]+(s[3]-s[0])*b, s[1]+(s[4]-s[1])*b, s[2]+(s[5]-s[2])*b]);
    }
  }
  return out;
}
/* 锁住的盒体：前后两枚框都过投影锁 ⇒ 屏上落点由构建期定死，深度只影响雾与遮挡。
   （P5 的画布中心落在四只能力盒围出来的中庭里，extrudeBack 的后框一缩就压字。） */
function lockBox(f, b){
  const e = [];
  for(let i = 0; i < 4; i++) e.push([f[i][0],f[i][1],f[i][2], b[i][0],b[i][1],b[i][2]]);
  return { front: segsOfLoop(f), shell: segsOfLoop(b).concat(e), f: f, b: b, edges: e };
}
/* 净空：把这一帧真的传上 GPU 的几何投影回舞台像素，量到页上字形墨迹盒的最小距离。
   items = [[geometry, pad], …]；pad 扣掉带宽 / 点半径（那是几何之外的墨）。 */
function clrMin(U, ink, items){
  let m = 1e9;
  for(let i = 0; i < items.length; i++)
    m = Math.min(m, geoClr(items[i][0], U, ink, items[i][1] || 0));
  return m;
}

/* ═══════════════════════════════════════════════════════════════════════════
   ② SD-RTN 地球（P2 公司 · 主图）—— **makeGlobe 现取自旗舰**，不在这里重写
   ───────────────────────────────────────────────────────────────────────────
   实现整体是 lab P21 那一枚（位掩码陆地 / 示意节点 / 五槽并发大圆弧 / 双主题材质 /
   OrbitControls 可拖不可缩）。本 deck 只提供矩形与 K 表 —— 场景代码一个字节没改。
   弧**不标任何延迟数值**（数字红线）；节点是示意分布，页上那行角注写死了这一条。
   ⚠ 它是球面场景（camSphere），没有 px 投影锁 ⇒ 不交 state().clr，
     净空由 ⑳globe 单验（弧外包络圆 vs 页上字形行框，下限 16px）。
   ═══════════════════════════════════════════════════════════════════════════ */

/* ═══════════════════════════════════════════════════════════════════════════
   ③ 空间生长（P3 矩阵 ·「一个实时底座，三条产品线」）
   ───────────────────────────────────────────────────────────────────────────
   页上是一张平面架构图：底座横贯、三条主干向上、配套虚线旁挂。升维之后，
   这三层关系变成**三层空间**：
     · 底座 = 一块有厚度的**纵深基面**（前框锁死在页上那只 rect，向 −z 拉 210，
       15 道横肋把纵深读出来）—— 它托举一切，所以它是全页最厚的一件，也是 hot；
     · 三条产品线 = 三股从基面内部**抽出来向上生长**的流（audioStream）：
       起点在基面深处、终点贴着版面平面 ⇒ 越往上越近、越亮、越宽；
     · 辅件（TEN / 评测 / 转录）退到 z=−150 的**景深处**：投影锁保证它们仍然
       落在页上那三只虚线盒的位置上，但深度雾把它们压弱一档 —— 层级差不再靠
       标签自说自话，靠的是它们真的在后面。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeGrow(ctx){
  const G = K.gw, w = ctx.rect[2], h = ctx.rect[3], D = G.D;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, G.half);
  const L = mkLock(w, h, D), U = unlock(w, h, D, ctx.rect);
  const baseMat = mkMat(SH, PX_LN_VS, PX_LN_FS);   /* 底座前框（hot） */
  const deckMat = mkMat(SH, PX_LN_VS, PX_LN_FS);   /* 底座的后框与棱 */
  const ribMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);   /* 备用（盒壳与栅格分色时用） */
  const boxMat  = [0,1,2].map(() => mkMat(SH, PX_LN_VS, PX_LN_FS));
  const shellMat = mkMat(SH, PX_LN_VS, PX_LN_FS);  /* 三只盒的体壳 */
  const auxMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);   /* 景深处的辅件 + 旁挂虚线 */
  /* 底座：**只有前框**（锁死在页上那只 rect 上）—— 它是 hot，一个像素不动 */
  const baseO = iSegs(denseSegs(segsOfLoop(G.base)), baseMat); scene.add(baseO);
  /* 纵深基面：底座身后那片真地平面（8 道横 + 15 道竖 · 各自成线） */
  const gridO = G.grid.map((s2) => { const o = iLine(unpk3(s2), deckMat);
                                     scene.add(o); return o; });
  const ribO = gridO[0];                 /* 净空取样时的代表（下面统一遍历 gridO） */
  /* 主干半宽**沿程生长**：基面深处 3.5 → 盒底 6.5（透视再叠一道 ⇒ 近 2× 生长）。
     「从底座抽出来向上长」因此是几何上真的在长，不是靠标签自说自话。 */
  const flows = G.trunk.map((s, k) =>
    mkStream(SH, unpk3(s), { w: (t) => G.w0 + (G.w1 - G.w0)*t,
                             spd: G.spd[k], lam: AS.lam }).add(scene));
  const boxO = G.box.map((b, k) => {
    const bd = boxBody(b[0], b[1], b[2], b[3], 0, G.boxdz, L);
    const f = iSegs(denseSegs(bd.front), boxMat[k]); scene.add(f);
    const s = iSegs(denseSegs(bd.shell), shellMat); scene.add(s);
    return [f, s];
  });
  const auxSegs = [];
  G.aux.forEach((b) => {
    const bd = boxBody(b[0], b[1], b[2], b[3], G.auxz, G.auxdz, L);
    bd.front.forEach(e => auxSegs.push(e)); bd.shell.forEach(e => auxSegs.push(e));
  });
  G.link.forEach(p => dashSegs(unpk3(p), 5, 6).forEach(e => auxSegs.push(e)));
  const auxO = iSegs(denseSegs(auxSegs), auxMat); scene.add(auxO);
  return {
    scene, camera, intro: 1.1, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){ SH.uTime.value = clock; flows.forEach(f => f.draw(clock)); },
    state(){ return { clr: clrMin(U, G.ink,
      flows.map(f => [f.geo, G.wpx]).concat(
        [[baseO.geometry, 0], [auxO.geometry, 0]],
        gridO.map(o => [o.geometry, 0]),
        boxO.map(o => [o[0].geometry, 0]), boxO.map(o => [o[1].geometry, 0]))) }; },
    applyTheme(){
      const pair = (m, c, hot, op, gain) => {
        m.uniforms.uColor.value.copy(cssColor(c));
        m.uniforms.uHot.value.copy(cssColor(hot || c));
        m.uniforms.uOpacity.value = op; m.uniforms.uGain.value = gain || 0; };
      pair(baseMat, '--gw-base', '--gw-base', cssNum('--gw-base-op', .9));
      pair(deckMat, '--gw-deck', '--gw-deck', cssNum('--gw-deck-op', .3));
      pair(ribMat,  '--gw-rib',  '--gw-rib',  cssNum('--gw-rib-op', .5));
      pair(shellMat,'--gw-rib',  '--gw-rib',  cssNum('--gw-rib-op', .5) * .8);
      pair(auxMat,  '--gw-aux',  '--gw-aux',  cssNum('--gw-aux-op', .5));
      /* RMS 实芯**各自本色**（浅底上原来三条一律 accent-deep = 三条都读成粉）*/
      const GW_RMS = ['--gw-e-rms','--gw-a-rms','--gw-p-rms'];
      ['--gw-e','--gw-a','--gw-p'].forEach((v, k) => {
        pair(boxMat[k], v, v, cssNum('--gw-box-op', .7));
        flows[k].theme(cssColor(v), cssColor(GW_RMS[k]),
                       cssNum('--gw-flow-op', .55), cssNum('--gw-rms-op', .7), .40);
        setBlend(flows[k].mat, cssNum('--gw-add', 0));
      });
      [baseMat, deckMat, ribMat, shellMat, auxMat].concat(boxMat).forEach(m => {
        m.uniforms.uBack.value = .40; setBlend(m, cssNum('--gw-add', 0)); });
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ④ 双向声带（P4 ENGINE）· ⑤ 五脑区大脑（P5 AGENT）
   ───────────────────────────────────────────────────────────────────────────
   两枚场景**整体现取自旗舰**（makeDuplex / makeBrain），本文件一个字节没改。
   它们原本不交 `state()`（旗舰的 ㉒ 闸只覆盖四枚加法层），而 info 的 ⑳clr 要一个
   运行时数 —— 所以这里加一层**只读的**外壳 `withClr`：不碰场景内部，只在它交出来
   的对象上补一个 `state()`，把**这一帧真的挂在 scene 上的几何**用 `unlock` 投影回
   舞台像素，逐顶点量到墨迹名册。
   ⚠ `unlock` 是 camPx 场景的**通用**逆投影（不只对 mkLock 过的几何成立）：
     屏上 x = cx + (X−cx)·D/(D−z)，正是 unlock 的那一行式子。
   ⚠ 量的时候把点径 / 带宽的 pad 一并扣掉（geoClr 的 pad 形参）。
   ═══════════════════════════════════════════════════════════════════════════ */
function withClr(make, D, ink, pad){
  return function(ctx){
    const u = make(ctx);
    if(u.state) return u;
    const U = unlock(ctx.rect[2], ctx.rect[3], D, ctx.rect);
    u.state = function(){
      let m = 1e9;
      u.scene.traverse(function(o){
        const g = o.geometry;
        if(!g || !g.attributes || !g.attributes.position) return;
        m = Math.min(m, geoClr(g, U, ink, pad));
      });
      return { clr: m };
    };
    return u;
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑧ 14 家星座墙（P7 案例）· 全 deck 唯一一枚**贴图**场景
   ───────────────────────────────────────────────────────────────────────────
   语义：14 个已公开的联合案例不是一张缩略图网格，是**一面站在纵深里的墙**——
   三家头部站在前排（大一档、几乎贴着版面），另外 11 家沿一道极缓的弧退进景深。
   墙整体绕竖轴摆动 ±6°（周期 20s · 零随机源）：一动，前后关系就读出来了；
   各卡再按自己的相位在 z 上浮动 ±10 —— 十四张各走各的，墙才是活的不是一块板。
   ⚠ **零文字进 canvas**：卡上只有原片，客户名一律在 DOM 的名册行里（⑮ 闸认那一行）。
   ⚠ 深度雾走**不透明度**：clearAlpha=0 ⇒ 退下去就是让纸面透出来，浅底暗底同一条路。
   ⚠ 贴图 sRGB + ClampToEdge；两种卡的长宽比都与原片一致 ⇒ UV 不裁切，
     poster 的 `preserveAspectRatio="xMidYMid slice"` 与它逐像素同解。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeWall(ctx){
  const W = K.w, w = ctx.rect[2], h = ctx.rect[3], D = W.D;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const grp = new THREE.Group();
  grp.position.set(W.cx, -W.cy, W.cz);        // 摆动轴 = 墙心的竖轴
  scene.add(grp);
  const loader = new THREE.TextureLoader();
  const SWAY = W.sway*Math.PI/180;
  const cards = W.card.map(function(c, i){
    /* c = [x, y, z0, cw, ch, phase] —— 全部是构建期算好的舞台像素 */
    const tex = loader.load(W.url[i]);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = tex.wrapT = THREE.ClampToEdgeWrapping;
    const mat = new THREE.MeshBasicMaterial({ map:tex, transparent:true, opacity:1,
                                              depthWrite:false, side:THREE.DoubleSide });
    const m = new THREE.Mesh(new THREE.PlaneGeometry(c[3], c[4]), mat);
    m.position.set(c[0]-W.cx, -(c[1]-W.cy), c[2]-W.cz);
    grp.add(m);
    /* 卡的**厚度**：前缘 + 后缘（内缩 ins · 退 dz）+ 四条棱 —— 三件一起才读成
       「一张有厚度的卡」，只画一圈框会读成一张贴纸。 */
    const hw = c[3]/2, hh = c[4]/2, ins = W.ins, dz = W.dz;
    const f = [[-hw,-hh,0],[hw,-hh,0],[hw,hh,0],[-hw,hh,0]];
    const b = [[-hw+ins,-hh+ins,-dz],[hw-ins,-hh+ins,-dz],[hw-ins,hh-ins,-dz],[-hw+ins,hh-ins,-dz]];
    const seg = [];
    for(let k=0;k<4;k++){
      const a1=f[k], a2=f[(k+1)%4], b1=b[k], b2=b[(k+1)%4];
      seg.push([a1[0],a1[1],a1[2], a2[0],a2[1],a2[2]]);
      seg.push([b1[0],b1[1],b1[2], b2[0],b2[1],b2[2]]);
      seg.push([a1[0],a1[1],a1[2], b1[0],b1[1],b1[2]]);
    }
    const rimMat = new THREE.LineBasicMaterial({ transparent:true, depthWrite:false });
    const rg = new THREE.BufferGeometry();
    const arr = new Float32Array(seg.length*6);
    seg.forEach(function(q,j){ arr.set(q, j*6); });
    rg.setAttribute('position', new THREE.BufferAttribute(arr,3));
    const rim = new THREE.LineSegments(rg, rimMat);
    rim.position.copy(m.position); rim.frustumCulled=false; grp.add(rim);
    return { m:m, rim:rim, mat:mat, rimMat:rimMat, x:c[0], y:c[1], z0:c[2],
             cw:c[3], ch:c[4], ph:c[5] };
  });
  const U = unlock(w, h, D, ctx.rect);
  let clockRef = 0, intro = 1;
  function place(clock){
    for(let i=0;i<cards.length;i++){
      const c = cards[i];
      const z = c.z0 + W.famp*Math.sin(6.2831853*clock/W.fper + c.ph);
      c.m.position.z = z - W.cz; c.rim.position.z = z - W.cz;
    }
    grp.rotation.y = SWAY*Math.sin(6.2831853*clock/W.cyc);
  }
  place(0);
  return {
    scene, camera, intro:1.2, grab:false,
    onDPR(pr){},
    setIntro(e){ intro = e; grp.scale.setScalar(Math.max(1e-3, 0.94 + 0.06*e));
                 cards.forEach(function(c){ c.mat.opacity = c.baseOp*e; c.rimMat.opacity = c.baseRim*e; }); },
    draw(dt, clock){ clockRef = clock; place(clock); },
    /* 净空：把这一帧真的挂在 scene 上的**卡四角**（含摆动与浮动）投影回舞台像素，
       量到墨迹名册。卡是贴图面，四角就是它的全部外缘（框在四角之内）。 */
    state(){
      const th = grp.rotation.y, ct = Math.cos(th), st = Math.sin(th);
      let m = 1e9;
      for(let i=0;i<cards.length;i++){
        const c = cards[i];
        const z = c.z0 + W.famp*Math.sin(6.2831853*clockRef/W.fper + c.ph);
        for(let sx=-1; sx<=1; sx+=2) for(let sy=-1; sy<=1; sy+=2){
          const lx = (c.x - W.cx) + sx*c.cw/2, ly = (c.y - W.cy) + sy*c.ch/2, lz = (z - W.cz);
          const X = W.cx + lx*ct + lz*st, Z = W.cz - lx*st + lz*ct;
          m = Math.min(m, inkClr(U(X, -(W.cy + ly), Z), W.ink));
        }
      }
      return { clr: m };
    },
    applyTheme(){
      const op = cssNum('--w-card-op', .96), fog = cssNum('--w-fog', .34);
      const rimC = cssColor('--w-rim'), rimO = cssNum('--w-rim-op', .5);
      for(let i=0;i<cards.length;i++){
        const c = cards[i];
        const t = Math.max(0, Math.min(1, (W.zmax - c.z0)/(W.zmax - W.zmin || 1)));
        c.baseOp = op*(1 - fog*t); c.baseRim = rimO*(1 - fog*t);
        c.mat.opacity = c.baseOp*intro; c.rimMat.opacity = c.baseRim*intro;
        c.rimMat.color.copy(rimC);
      }
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑥ 三条支流，一条河（P8 合流 · 本 deck 的标杆页）
   ───────────────────────────────────────────────────────────────────────────
   这一页天生就是 3D 语义：三条支流在**纵深**里各自成流（源头 z=−270），
   一路爬升汇入版面平面上的 ONE NET 主河道（z=0）。
   ── 接力的相位账（「同速同相」不是感觉，是解出来的）──────────────────────
   四条流**共用同一个世界速度** v（= 主河道的 110px/s；主河道 z 恒 0 ⇒ 世界即屏幕）。
   支流 k 的世界弧长 Lw_k，相位偏移 off_k = −Lw_k + k·λ/3：
     u_支流末 = Lw_k − v·t + off_k = −v·t + k·λ/3 = u_主河道首 + k·λ/3
   ⇒ ① 支流末端与主河道首端的波**严丝合缝**（不瞬移、不叠影）；
      ② 三条支流的波峰各差 λ/3 到达汇合点 ⇒ 读起来就是**轮流接力进主河道**。
   支流在纵深里的屏上速度天然比主河道慢（透视，越远越慢）—— 那是对的：
   它是真的在远处。qa 的 ⑳rv 闸拿 data-lab-rvphase 逐条复算这三个偏移。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeRiver(ctx){
  const R = K.rv, w = ctx.rect[2], h = ctx.rect[3], D = R.D;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, R.half);
  const L = mkLock(w, h, D), U = unlock(w, h, D, ctx.rect);
  const bedMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const railMat = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const srcMat  = mkMat(SH, PX_PT_VS, PX_PT_FS);
  const meetMat = mkMat(SH, PX_PT_VS, PX_PT_FS);
  /* ── 能量守恒：河**比支流宽** ───────────────────────────────────────────
     支流半宽沿程 4.0（源头）→ 6.5（河口），透视再把源头收窄一道（1200/1470）——
     叠加后源头到河口约 2× 生长，正是「越近越宽」。
     主河道 13.0 且 floor .55（河是稳定的，脉动归支流），河口 80px 内再抬到 15：
     三条流交出去的那一处要看得见「合」。峰值 ±15 仍在 rx26·高 52 的河道盒内。 */
  const trib = R.trib.map((s, k) =>
    mkStream(SH, unpk3(s), { w: (t) => R.wt0 + (R.wt1 - R.wt0)*t,
                             spd: R.spd, lam: AS.lam }).add(scene));
  const main = mkStream(SH, unpk3(R.main), {
    w: (t, acc) => { const q = acc/R.wacc; return R.wm + (R.wmouth - R.wm)*Math.exp(-q*q); },
    spd: R.spd, lam: AS.lam, floor: R.mfloor }).add(scene);
  /* ONE NET 主河道：页上那只 rx26 的圆角盒 —— 前框锁死、向后拉出河床 */
  const rail = unpk3(R.rail), bed = unpk3(R.bed);
  const railO = iSegs(denseSegs(segsOfLoop(rail)), railMat); scene.add(railO);
  const bedSegs = segsOfLoop(bed);
  for(let i = 0; i < rail.length; i += 4)
    bedSegs.push([rail[i][0],rail[i][1],rail[i][2], bed[i][0],bed[i][1],bed[i][2]]);
  const bedO = iSegs(denseSegs(bedSegs), bedMat); scene.add(bedO);
  const srcO = iPts(unpk3(R.src), srcMat); scene.add(srcO);
  const meetO = iPts(unpk3(R.meet), meetMat); scene.add(meetO);
  const mA = meetO.geometry.attributes.aH, sA = srcO.geometry.attributes.aH;
  return {
    scene, camera, intro: 1.25, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      const run = R.spd * clock;
      main.draw(clock);
      trib.forEach((f, k) => { f.draw(clock); f.mat.uniforms.uRun.value = run - R.off[k]; });
      /* 汇合点：三条支流在此刻交出去的包络之和 —— 「三条流轮流接力」看得见的那一处 */
      let s = 0;
      for(let k = 0; k < R.off.length; k++) s += asEnv(-run + R.off[k] + R.tlen[k]);
      mA.array[0] = Math.max(0, Math.min(1, (s / R.off.length - 0.35) / 0.5));
      mA.needsUpdate = true;
      for(let k = 0; k < R.off.length; k++) sA.array[k] = asEnv(R.off[k] - run) * .8;
      sA.needsUpdate = true;
    },
    state(){ return { clr: clrMin(U, R.ink,
      trib.map(f => [f.geo, R.wtpx]).concat([
        [main.geo, R.wmpx], [railO.geometry, 0], [bedO.geometry, 0],
        [srcO.geometry, cssNum('--rv-src-size',6)/2],
        [meetO.geometry, cssNum('--rv-meet-size',9)/2]])) }; },
    applyTheme(){
      const pair = (m, c, hot, op, gain, sz) => {
        m.uniforms.uColor.value.copy(cssColor(c));
        m.uniforms.uHot.value.copy(cssColor(hot || c));
        m.uniforms.uOpacity.value = op; m.uniforms.uGain.value = gain || 0;
        if(sz !== undefined) m.uniforms.uSize.value = sz; };
      pair(railMat, '--rv-rail', '--rv-rail', cssNum('--rv-rail-op', .88));
      pair(bedMat,  '--rv-bed',  '--rv-bed',  cssNum('--rv-bed-op', .3));
      pair(srcMat,  '--rv-src',  '--rv-main', cssNum('--rv-src-op', .8), .9,
           cssNum('--rv-src-size', 6.4));
      pair(meetMat, '--rv-meet', '--rv-meet', cssNum('--rv-meet-op', 1), .8,
           cssNum('--rv-meet-size', 9));
      main.theme(cssColor('--rv-main'), cssColor('--rv-rms'),
                 cssNum('--rv-main-op', .7), cssNum('--rv-rms-op', .78), .38);
      /* 三条支流的 RMS 实芯**各自本色**（原来三条一律 accent-deep ⇒ 浅底上
         Agent / Physical AI 两条从源头起就读成粉，「三条」当场丢失）。
         主河道的实芯不动 —— 粉 = ONE NET，它才是那一条。 */
      const RV_RMS = ['--rv-e-rms','--rv-a-rms','--rv-p-rms'];
      ['--rv-e','--rv-a','--rv-p'].forEach((v, k) =>
        trib[k].theme(cssColor(v), cssColor(RV_RMS[k]),
                      cssNum('--rv-trib-op', .6), cssNum('--rv-trib-rms-op', .7), .38));
      [railMat, bedMat, srcMat, meetMat].forEach(m => {
        m.uniforms.uBack.value = .38; setBlend(m, cssNum('--rv-add', 0)); });
      [main].concat(trib).forEach(f => setBlend(f.mat, cssNum('--rv-add', 0)));
    },
  };
}

/* ═══════════════════════════════════════════════════════════════════════════
   ⑦ 走出屏幕（P6 PHYSICAL AI ·「让对话，走出屏幕。」）· 全 deck 唯一的加法层
   ───────────────────────────────────────────────────────────────────────────
   另外六枚场景都在**替换**页上的一张 SVG；这一枚不替换任何东西 —— 它是标题的
   **图解**，坐在标题右侧那条本来就空着的带子上（舞台 740,140,1060,100）。
   两件东西，一句话：
     · 一只**锁在版面上的屏幕**：外框（bezel · 56×84 rx8）+ 内屏框（内缩 5 · rx6）
       + 一块微亮的**屏面**（quadGeo 实心面，op 浅 .07 / 暗 .10）。三件一起才读成
       「屏幕」—— 只画一圈细线框会读成一扇门或一枚手机图标（一稿的病，二稿改掉）。
       前框 z=0、后框 z=−60 内缩 4（lockBox 写法同 P5：两枚都过投影锁 ⇒ 屏上落点
       由构建期定死，深度只管雾与遮挡）。它不参与流，只被穿过：屏幕是**边界**。
     · 一条 audioStream 从**屏面里**（z=−140）起，横穿整只屏、过框右缘，一路朝观众
       爬到 z=+36，半宽 3.6 → 9。介质与全家族同一种（λ=232px、110px/s ⇒ 2.11s 一次呼吸）。
   「走出屏幕」在这里是**几何上真的走出去**，不是隐喻：
     幅度剖面 g(u) = .50 → 1.0（在框右缘之后 60px 弧长里 smoothstep 放开）——
     屏幕里的声音是闷的**但看得见**（一稿压到 .35 且只有 26px×半宽2.5，帧上等于没有，
     故事只剩「框边冒出一条流」）；框右缘那一枚点的 aH = 该处包络 ⇒
     **波峰穿框的那一刻它亮一下**，「穿过去」有了一个看得见的瞬间。
   ⚠ 加法层的净空走 16px 规则（版面之外的空档），不走「不许比 2D 更近」——
     页上这块地本来没有图，没有 2D 可比。⑳clr 的对手是四邻的字形行框。
   ═══════════════════════════════════════════════════════════════════════════ */
function makeExit(ctx){
  const X = K.ex, w = ctx.rect[2], h = ctx.rect[3], D = X.D;
  const scene = new THREE.Scene();
  const camera = camPx(w, h, D);
  const SH = pxShared(D, X.half);
  const U = unlock(w, h, D, ctx.rect);
  const frameMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const innerMat  = mkMat(SH, PX_LN_VS, PX_LN_FS);
  const screenMat = mkMat(SH, PX_LN_VS, PX_LN_FS);   /* 实心面照用 PX_LN 那对着色器 */
  const dotMat    = mkMat(SH, PX_PT_VS, PX_PT_FS);
  /* 屏面：一块微亮的实心面（quadGeo 逐字取自 lab-kit ⑤）—— 它坐在最里层，
     内屏框与外框压在它之上；「屏幕」这三件的层序与 poster 完全一致。 */
  const screenG = quadGeo(unpk3(X.quad)); fillAH(screenG, 1, 0);
  const screenO = new THREE.Mesh(screenG, screenMat);
  screenMat.side = THREE.DoubleSide; screenO.frustumCulled = false; scene.add(screenO);
  /* 屏幕框：外框前框 + 后框 + 四条棱（denseSegs 加密到 ≤12px —— 净空是逐顶点量的） */
  const LB = lockBox(unpk3(X.lb[0]), unpk3(X.lb[1]));
  const frameO = iSegs(denseSegs(LB.front.concat(LB.shell)), frameMat); scene.add(frameO);
  const innerO = iSegs(denseSegs(segsOfLoop(unpk3(X.inner))), innerMat); scene.add(innerO);
  const path = unpk3(X.path);
  /* 幅度剖面：出框之前恒 g0（闷），出框之后 smoothstep 在 gspan 弧长里放开到 1。
     fn 只吃 u ⇒ mkStream 认作静态剖面，整段只算一次，不进每帧开销。 */
  const flow = mkStream(SH, path, { w: (t) => X.w0 + (X.w1 - X.w0)*t,
                                    spd: X.spd, lam: AS.lam,
                                    floor: X.floor, edge: X.edge })
    .gain((u) => {
      const q = Math.max(0, Math.min(1, (u - X.uframe) / X.gspan));
      return X.g0 + (1 - X.g0)*q*q*(3 - 2*q);
    }).add(scene);
  const dotO = iPts(unpk3(X.dot), dotMat); scene.add(dotO);
  const dA = dotO.geometry.attributes.aH;
  return {
    scene, camera, intro: 1.15, grab: false,
    onDPR(pr){ SH.uPx.value = pr; },
    setIntro(e){ SH.uIntro.value = e; },
    draw(dt, clock){
      SH.uTime.value = clock;
      flow.draw(clock);
      /* 出口那一枚点：aH = 框右缘处此刻的包络（与 river 的 meet 同一写法）——
         波峰穿框时它亮，波谷时它退回一枚安静的点。 */
      dA.array[0] = asEnv(X.uframe - X.spd*clock);
      dA.needsUpdate = true;
    },
    state(){ return { clr: clrMin(U, X.ink, [
      [flow.geo, X.wpx], [frameO.geometry, 0], [innerO.geometry, 0], [screenG, 0],
      [dotO.geometry, cssNum('--ex-dot-size', 8)/2] ]) }; },
    applyTheme(){
      frameMat.uniforms.uColor.value.copy(cssColor('--ex-frame'));
      frameMat.uniforms.uHot.value.copy(cssColor('--ex-frame'));
      frameMat.uniforms.uOpacity.value = cssNum('--ex-frame-op', .85);
      frameMat.uniforms.uGain.value = 0;
      innerMat.uniforms.uColor.value.copy(cssColor('--ex-frame'));
      innerMat.uniforms.uHot.value.copy(cssColor('--ex-frame'));
      innerMat.uniforms.uOpacity.value = cssNum('--ex-inner-op', .55);
      innerMat.uniforms.uGain.value = 0;
      screenMat.uniforms.uColor.value.copy(cssColor('--ex-screen'));
      screenMat.uniforms.uHot.value.copy(cssColor('--ex-screen'));
      screenMat.uniforms.uOpacity.value = cssNum('--ex-screen-op', .07);
      screenMat.uniforms.uGain.value = 0;
      dotMat.uniforms.uColor.value.copy(cssColor('--ex-dot'));
      dotMat.uniforms.uHot.value.copy(cssColor('--ex-flow'));
      dotMat.uniforms.uOpacity.value = cssNum('--ex-dot-op', .92);
      dotMat.uniforms.uSize.value = cssNum('--ex-dot-size', 8);
      dotMat.uniforms.uGain.value = .9;
      flow.theme(cssColor('--ex-flow'), cssColor('--ex-rms'),
                 cssNum('--ex-flow-op', .70), cssNum('--ex-rms-op', .74), .46);
      [frameMat, innerMat, screenMat, dotMat].forEach(m => {
        m.uniforms.uBack.value = .46; setBlend(m, cssNum('--ex-add', 0)); });
      setBlend(flow.mat, cssNum('--ex-add', 0));
    },
  };
}
"""


# ═══════════════════════════════════════════════════════════════════════════
# LAB 层 · 构建期常量表（运行时直接吃）+ 净空的**解析算路**
# ───────────────────────────────────────────────────────────────────────────
#   净空有两条独立算路，两边必须给出同一个数（qa 的 ⑳clr 闸对表）：
#     ① 构建期（这里）：投影锁 ⇒ 锁住的点投影落点 = 它的页坐标；
#        向后拉伸的框投影 = 页矩形绕**画布中心**按 s=(D−z0)/(D−z0+dz) 缩一档。
#        于是净空可以纯解析地算出来，不需要跑浏览器。
#     ② 运行时（scene.state().clr）：把这一帧真的传上 GPU 的顶点用 `unlock`
#        投影回舞台像素，逐顶点量。
#   两条算路从几何到代码都不共用，对得上才算真的没压字。
# ═══════════════════════════════════════════════════════════════════════════
def _cssmax(name):
    """从 LAB_CSS 里现取某个尺寸变量的**最大值**（浅 / 暗两档取大的那一档）——
       净空探针的 pad 因此与页面上真正画出来的点径同源，不会两处各写一个数。"""
    v = [float(x) for x in _re2.findall(r"%s\s*:\s*([0-9.]+)" % _re2.escape(name), LAB_CSS)]
    assert v, "LAB_CSS 里找不到 %s" % name
    return max(v)


def _back_s(z0, dz, D):
    """向后拉伸 dz 之后，后框在屏上相对**画布中心**的缩放"""
    return (D - z0) / (D - z0 + dz)


def _probe_lock(pts, rect, pad=0.0):
    """锁住的几何：投影落点 = 页坐标（pts 是画布局部坐标）"""
    return [(rect[0] + p[0], rect[1] + p[1], pad) for p in pts]


def _probe_back(pts, z0, dz, D, rect, pad=0.0):
    """向后拉伸出来的框 / 棱：绕画布中心缩 s 之后落在哪儿"""
    cx, cy = rect[2] / 2.0, rect[3] / 2.0
    s = _back_s(z0, dz, D)
    return [(rect[0] + cx + (p[0] - cx) * s, rect[1] + cy + (p[1] - cy) * s, pad) for p in pts]


def _probe_rect(x, y, w, h, per=26):
    o = []
    for i in range(per):
        t = i / float(per)
        o += [(x + w * t, y), (x + w * t, y + h), (x, y + h * t), (x + w, y + h * t)]
    return o


def _wpx(w0, pts, D):
    """一条流带在**屏上**的最大半宽：世界半宽 w0 经透视放大 D/(D−z)，取路径上的最大值。
       净空的 pad 用它 —— 与 `_probe_stream` 同一条式子，构建期与运行时不会各算各的。"""
    return w0 * max(D / (D - q[2]) for q in pts)


def _probe_stream(pts, rect, w0, D):
    """连续流带：中心线锁住 ⇒ 落点 = 页坐标；屏上半宽 = w0 / k（k=(D−z)/D）"""
    return [(rect[0] + p[0], rect[1] + p[1], w0 / ((D - p[2]) / D)) for p in pts]


def _dist_box(px, py, b):
    dx = max(b[0] - px, 0.0, px - (b[0] + b[2]))
    dy = max(b[1] - py, 0.0, py - (b[1] + b[3]))
    return math.hypot(dx, dy)


def _clr_of(probe, ink):
    m = 1e9
    for px, py, pad in probe:
        for b in ink:
            d = _dist_box(px, py, b) - pad
            if d < m:
                m = d
    return m


def _cum_world(pagepts, w, h, D):
    wp = _lock_path(pagepts, w, h, D)
    cum = [0.0]
    for i in range(1, len(wp)):
        cum.append(cum[-1] + math.hypot(wp[i][0] - wp[i - 1][0], wp[i][1] - wp[i - 1][1]))
    return wp, cum


def _u_at_x(pagepts, cum, x):
    for i in range(len(pagepts) - 1):
        a, b = pagepts[i][0], pagepts[i + 1][0]
        if min(a, b) - 1e-6 <= x <= max(a, b) + 1e-6:
            t = 0.0 if b == a else (x - a) / (b - a)
            return cum[i] + (cum[i + 1] - cum[i]) * t
    return cum[-1]


# ── ② P2 SD-RTN 地球 ───────────────────────────────────────────────────────
def _g_build():
    """地球没有 px 投影锁的几何 —— 它的净空探针就是**弧的外包络圆**：
       半径 _G_ENV（球面 1.243r 的限界投影）绕球心一圈，逐点量到页上字形行框。
       这与运行时 ⑳globe 那一闸量的是同一个圆（qa 从 data-lab-genv 现取）。"""
    probe = []
    for i in range(360):
        a2 = i * math.pi / 180.0
        probe.append((_G_CX + _G_ENV * math.cos(a2), _G_CY + _G_ENV * math.sin(a2), 0.0))
    return dict(env=_G_ENV, probe=probe)


# ── ③ P3 空间生长 ─────────────────────────────────────────────────────────
def _gw_build():
    r = LAB_RECTS[3]
    w, h = r[3], r[4]
    # 盒 / 辅件 / 旁挂虚线的坐标**逐条取自 _p3fig() 的那批常量**（不许两处各写一个数）
    box = [(tx - _MX_BW // 2, _MX_BOXY, _MX_BW, _MX_BH) for tx, _c, _m, _t, _f, _y in _MX_LINES]
    aux = [(x, _MX_AUXY, bw, _MX_AUXH) for x, bw, _n2, _f, _how in _MX_AUX]
    link = []
    for x, bw, _n2, _f, how in _MX_AUX:
        if how == "trunk":
            link.append([(x + bw + 4, _MX_AUXY + 42, _GW_AUXZ), (300, _MX_AUXY + 42, _GW_AUXZ)])
        else:
            link.append([(x + bw // 2, _MX_AUXY + _MX_AUXH, _GW_AUXZ),
                         (x + bw // 2, _GW_BASEY, _GW_AUXZ)])
    grid = _gw_grid()
    trunk, spd, probe = [], [], []
    for tx, _c, _m, _t, _f, _y in _MX_LINES:
        pts = _gw_trunk(tx)
        _wp, cum = _cum_world(pts, w, h, _GW_D)
        Lp = _xylen([(p[0], p[1]) for p in pts])
        trunk.append(pts)
        spd.append(_SPD_A * cum[-1] / Lp)
        probe += _probe_stream(pts, r[1:], _GW_WMAX, _GW_D)
    # 底座：**只有前框**（锁死在页上那只 rect 上）+ 身后那片透视基面栅格
    probe += _probe_lock(_probe_rect(0, _GW_BASEY, 1668, _GW_BASEH), r[1:])
    for g in grid:
        probe += _probe_lock([(q[0], q[1]) for q in g], r[1:])
    for b in box:
        pr = _probe_rect(*b)
        probe += _probe_lock(pr, r[1:]) + _probe_back(pr, 0.0, _GW_BOXDZ, _GW_D, r[1:])
    for b in aux:
        pr = _probe_rect(*b)
        probe += _probe_lock(pr, r[1:]) + _probe_back(pr, _GW_AUXZ, _GW_AUXDZ, _GW_D, r[1:])
    for ln2 in link:
        probe += _probe_lock([(p[0], p[1]) for p in _lerp_line(ln2[0], ln2[1], 24)], r[1:])
    return dict(w=w, h=h, box=box, aux=aux, link=link, grid=grid,
                trunk=trunk, spd=spd, probe=probe)


# ── ④ P4 双向声带 · ⑤ P5 五脑区大脑（净空探针）────────────────────────────
#   两枚都是「借来的场景」：3D 的顶点在运行时才生成（ribbon 网格 / 12000 点的体积
#   点云），构建期没法逐点复现。所以它们的构建期算路用的是**外包络**：
#     P4：两条声带的中心线（`_d_lane`，与 makeDuplex 的 lane() 逐点同解）+
#         半宽 hw 经透视放大 ⇒ 与运行时的 ribbon 顶点是同一批点（exact）。
#     P5：页上那条母形轮廓 `_BRAIN` + 突触弧 + 输入通路，**扫掠**摇摆区间
#         ±12° 并按半厚度 tmax 做透视外扩 ⇒ 一枚**必然包住**点云的壳。
#   两条算路的关系因此是：解析 ≤ 运行时（下界），qa 按这条不等式对表。
def _d_build():
    """双向声带的净空探针。**注意：这两条带没有过投影锁**（makeDuplex 的 lane() 直接
       写世界坐标）⇒ 屏上落点不是页坐标本人，得自己做一次透视除法：
         sx = rect.x + cx + (x−cx)·D/(D−z)，pad = hw·D/(D−z)。
       —— 这是与 grow / river 那一路（锁死中心线）最本质的差别，别照抄那边的
       `_probe_stream`（本轮实拍锤过：照抄会把净空算小 14px）。
       下行那条带的半宽是 hw×0.86（旗舰 band(B, Q.hw*0.86, true)）。"""
    r = LAB_RECTS[4]
    w, h = r[3], r[4]
    cx, cy = w / 2.0, h / 2.0
    probe, lanes = [], []
    for sgn, ph, hw in ((1, 0.0, _D_HW), (-1, _LAB._D_PHASE, _D_HW * 0.86)):
        pts = []
        for i in range(_LAB._D_N):
            u = i / (_LAB._D_N - 1.0)
            th = 2 * math.pi * _LAB._D_TURNS * u + ph
            pts.append((_LAB._D_X0 + (_LAB._D_X1 - _LAB._D_X0) * u,
                        _LAB._D_YC - sgn * _LAB._D_AMP * math.cos(th),
                        sgn * _LAB._D_DEP * math.sin(th)))
        lanes.append(pts)
        # ribbonGeo 的 Python 同解：顶点 = 中心线 ± hw·n̂，n̂ = 切线在 XY 面内的法向。
        # **不是**「中心线 ± 半径的圆盘」——圆盘在盒角处会把净空算小（本轮实拍锤过：
        # 圆盘算 −1.9px，真顶点是 +2.6px）。逐顶点算，两条算路才对得上。
        n = len(pts)
        for i in range(n):
            a2, b2 = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
            tx, ty = b2[0] - a2[0], b2[1] - a2[1]
            tl = math.hypot(tx, ty, b2[2] - a2[2]) or 1.0
            nx, ny = ty / tl, -tx / tl
            nl = math.hypot(nx, ny) or 1.0
            nx, ny = nx / nl, ny / nl
            px, py, pz = pts[i]
            k = (_D_D - pz) / _D_D
            for sg in (1.0, -1.0):
                vx, vy = px + sg * hw * nx, py + sg * hw * ny
                probe.append((r[1] + cx + (vx - cx) / k, r[2] + cy + (vy - cy) / k, 0.0))
    # 截断竖线（x=_XIN · z=0 ⇒ 透视是恒等，落点就是页坐标）
    probe += _probe_lock([(float(_LAB._XIN), 60.0 + (330.0 - 60.0) * i / 24.0)
                          for i in range(25)], r[1:])
    return dict(w=w, h=h, lanes=lanes, probe=probe)


def _b_build():
    """大脑的净空外包络（构建期解析算路）。
       点云不是随手撒的：厚度剖面 T(d) = tmax·sin(π/2·(d/dref)^0.62)，d 是到母形
       轮廓的距离 ⇒ **轮廓上 T=0**（正视限界就是那条轮廓本人），越往里越厚。
       所以「3D 会不会比 2D 更胖」是一道解析题：沿轮廓向内走 d，点在 z=±T(d) 上，
       透视把它按 1/k 推出去（k=(D−T)/D），再叠一层 ±12° 摇摆的 x 位移 ——
       取整族的最大外缘即是包络。实测只比 2D 轮廓外扩 ~2.4px（不是 tmax 那一档的 35px：
       最胖的点在深处，而深处离轮廓远，两件事互相抵消）。
       运行时（withClr）量的是真点云 ⇒ 解析必然是它的**下界**，qa 按不等式对表。"""
    r = LAB_RECTS[5]
    w, h = r[3], r[4]
    dref = 108.0
    polys = [_LAB._pathpts(_LAB._BRAIN, 26)[0], _LAB._pathpts(_LAB._CEREB, 20)[0],
             _LAB._pathpts(_LAB._STEM, 20)[0], _LAB._pathpts(_LAB._BRAIN_IN, 20)[0]]
    for a2 in _LAB._ARCS:
        polys.append(_LAB._pathpts(a2[0], 16)[0])
    # 形心：向内走的方向（母形是团状 ⇒ 朝形心走 d 与「离轮廓 d」足够接近）
    allp = [q for pts in polys[:1] for q in pts]
    ccx = sum(q[0] for q in allp) / len(allp)
    ccy = sum(q[1] for q in allp) / len(allp)
    bb = _LAB._bbox(_LAB._BRAIN)
    bcx = (bb[0] + bb[2]) / 2.0
    sw = _B_SWAY * math.pi / 180.0
    DEP = [0.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 50.0, 80.0]
    probe = []
    for pi, pts in enumerate(polys):
        inner = (pi == 0)          # 只有母形才有「向内变厚」；其余是线状件（贴表面走）
        for px, py in pts:
            for d in (DEP if inner else [0.0]):
                if inner and d > 0:
                    vx, vy = ccx - px, ccy - py
                    nl = math.hypot(vx, vy) or 1.0
                    qx, qy = px + vx / nl * d, py + vy / nl * d
                else:
                    qx, qy = px, py
                t = min(1.0, d / dref)
                T = _B_TMAX * math.sin(math.pi / 2 * (t ** 0.62)) if inner else _B_TMAX * 0.25
                for z0 in ((-T, T) if T else (0.0,)):
                    for th in (-sw, 0.0, sw):
                        dx = qx - bcx
                        X = bcx + dx * math.cos(th) + z0 * math.sin(th)
                        Z = -dx * math.sin(th) + z0 * math.cos(th)
                        k = (_B_D - Z) / _B_D
                        probe.append((r[1] + w / 2.0 + (X - w / 2.0) / k,
                                      r[2] + h / 2.0 + (qy - h / 2.0) / k, 0.0))
    return dict(w=w, h=h, probe=probe)


# ── ⑧ P7 星座墙 ─────────────────────────────────────────────────────────────
def _w_build():
    """星座墙的净空探针 = **扫掠包络**：十四张卡的四角 × 摆动区间 {−6°,0,+6°}
       × 浮动区间 {−famp,0,+famp}，逐点做透视除法投影回舞台像素。
       卡在摆动 / 浮动里走的就是这个族，运行时 state() 量的是族里的**某一帧** ⇒
       解析必然是它的下界，qa 按不等式对表（与 P5 大脑同一条路）。"""
    r = LAB_RECTS[7]
    w, h = r[3], r[4]
    sw = _W_SWAY * math.pi / 180.0
    probe = []
    for nm, url, x, y, z0, cw, ch, ph in _W_CARDS:
        for dz in (-_W_FAMP, 0.0, _W_FAMP):
            for sx in (-1, 1):
                for sy in (-1, 1):
                    lx = (x - _W_CX) + sx * cw / 2.0
                    ly = (y - _W_CY) + sy * ch / 2.0
                    lz = (z0 + dz) - _W_CZ
                    for th in (-sw, 0.0, sw):
                        X = _W_CX + lx * math.cos(th) + lz * math.sin(th)
                        Z = _W_CZ - lx * math.sin(th) + lz * math.cos(th)
                        k = (_W_D - Z) / _W_D
                        probe.append((r[1] + _W_CX + (X - _W_CX) / k,
                                      r[2] + _W_CY + ly / k, 0.0))
    return dict(w=w, h=h, probe=probe)


# ── ⑥ P8 三条支流一条河 ───────────────────────────────────────────────────
_RV_BED = 144.0                           # 河床纵深（= 90 ×1.6）


def _rv_build():
    r = LAB_RECTS[8]
    w, h = r[3], r[4]
    trib, tlen, off, spdrow, probe = [], [], [], [], []
    for k, (y, _c, _lb) in enumerate(_TRIB):
        pts = _rv_trib(k, y)
        _wp, cum = _cum_world(pts, w, h, _RV_D)
        Lp = _xylen([(p[0], p[1]) for p in pts])
        trib.append(pts)
        tlen.append(cum[-1])
        # 接力：off_k = −Lw_k + k·λ/3 ⇒ 支流末端与主河道首端严丝合缝，且三条差 λ/3
        off.append(-cum[-1] + k * _RV_LAM / 3.0)
        spdrow.append(("支流%d" % (k + 1), Lp, _SPD_A * Lp / cum[-1]))
        probe += _probe_stream(pts, r[1:], _RV_WT, _RV_D)
    main = _rv_main()
    _mw, mcum = _cum_world(main, w, h, _RV_D)
    spdrow.append(("ONE NET 主河道", _xylen([(p[0], p[1]) for p in main]), _SPD_A))
    probe += _probe_stream(main, r[1:], _RV_WMAX, _RV_D)
    rail = [(p[0], p[1], 0.0) for p in _rrect(_P8_BOX[0], _P8_BOX[1], _P8_BOX[2],
                                              _P8_BOX[3], _P8_BOX[4])]
    probe += _probe_lock([(p[0], p[1]) for p in rail], r[1:])
    probe += _probe_back([(p[0], p[1]) for p in rail], 0.0, _RV_BED, _RV_D, r[1:])
    # ⚠ 页上那条域分带 `M640 46 V396`**不进 3D**：它要说的那件事，3D 里已经由
    #   **深度**说了 —— 支流在纵深、主河道在版面平面。两枚域标注（三条产品线 /
    #   一张实时网）是文字件，照常留在 DOM 里。
    src = [(float(_P8_SX), float(y), _RV_ZSRC) for y, _c, _lb in _TRIB]
    probe += [(r[1] + p[0], r[2] + p[1], _cssmax("--rv-src-size") / 2.0) for p in src]
    meet = [(float(_P8_CX), float(_P8_CY), 0.0)]
    probe += [(r[1] + p[0], r[2] + p[1], _cssmax("--rv-meet-size") / 2.0) for p in meet]
    return dict(w=w, h=h, trib=trib, tlen=tlen, off=off, main=main, rail=rail,
                src=src, meet=meet, spd=spdrow, probe=probe)


# ── ⑦ P6 走出屏幕（加法层）───────────────────────────────────────────────
def _ex_build():
    r = _EX_RECT
    w, h = r[2], r[3]
    page = _ex_path()
    wp, cum = _cum_world(page, w, h, _EX_D)
    Lp = _xylen([(p[0], p[1]) for p in page])
    spd = _SPD_A * cum[-1] / Lp
    uframe = _u_at_x(page, cum, _EX_XFRAME)      # 框右缘处的**世界弧长** = 放开的起点
    bx, by, bw2, bh2 = _EX_BOX
    wf, wb, pf, pb = _lockbox(bx, by, bw2, bh2, _EX_ZBOX, _EX_DZBOX, _EX_INS, w, h, _EX_D)
    # 内屏框 / 屏面：外框内缩 _EX_INS2，z=0（同样过投影锁 ⇒ 落点 = 页坐标）
    ix, iy = bx + _EX_INS2, by + _EX_INS2
    iw, ih = bw2 - 2 * _EX_INS2, bh2 - 2 * _EX_INS2
    inner = _lock_path([(ix, iy, 0.0), (ix + iw, iy, 0.0), (ix + iw, iy + ih, 0.0),
                        (ix, iy + ih, 0.0), (ix, iy, 0.0)], w, h, _EX_D)
    quad = _lock_path([(ix, iy, 0.0), (ix + iw, iy, 0.0),
                       (ix + iw, iy + ih, 0.0), (ix, iy + ih, 0.0)], w, h, _EX_D)
    # 净空探针：流（中心线锁住 · pad 保守取最大半宽 9.0）+ 外框前后两枚 + 四条棱
    #           + 内屏框（屏面与它同范围 ⇒ 同一批点）+ 出口点
    probe = _probe_stream(page, r, _EX_W1, _EX_D)
    probe += _probe_lock(_probe_rect(bx, by, bw2, bh2), r)
    probe += _probe_lock(_probe_rect(bx + _EX_INS, by + _EX_INS,
                                     bw2 - 2 * _EX_INS, bh2 - 2 * _EX_INS), r)
    probe += _probe_lock(_probe_rect(ix, iy, iw, ih), r)
    for a, b in zip(pf[:4], pb[:4]):
        probe += _probe_lock([(q[0], q[1]) for q in _lerp_line((a[0], a[1], 0),
                                                              (b[0], b[1], 0), 6)], r)
    probe += [(r[0] + _EX_DOT[0], r[1] + _EX_DOT[1], _cssmax("--ex-dot-size") / 2.0)]
    return dict(w=w, h=h, page=page, spd=spd, Lp=Lp, uframe=uframe,
                lb=(wf, wb), inner=inner, quad=quad, probe=probe)


_G = _g_build()
_GW = _gw_build()
_D = _d_build()
_B = _b_build()
_W = _w_build()
_RV = _rv_build()
_EX = _ex_build()
_PROBE = {2: _G["probe"], 3: _GW["probe"], 4: _D["probe"], 5: _B["probe"],
          7: _W["probe"], 8: _RV["probe"]}
if P6_EXIT:
    _PROBE[6] = _EX["probe"]
_CLR_MIN = {p: _clr_of(_PROBE[p], _INK[p]) for p in _PROBE}


def _spd_rows(p):
    """逐股**屏上**流速（px/s）—— A 档 110 ±30%，qa 的 ⑳spd 闸逐股复算"""
    if p == 2:
        return []          # 地球不是「介质流」——它没有 audioStream，不进 A 档流速表
    if p == 3:
        return [("%s 主干" % m[2], _xylen([(q[0], q[1]) for q in _GW["trunk"][k]]), _SPD_A)
                for k, m in enumerate(_MX_LINES)]
    if p == 4:
        # 两条声带 —— 名字 / 弧长 / 速度**逐条现取自旗舰**的 `_spd_rows(4)`
        return list(_LAB._spd_rows(4))
    if p == 5:
        return []          # 大脑不是「介质流」：突触火花是离散事件（B 档），不进 A 档表
    if p == 6:
        return [("走出屏幕声流", _EX["Lp"], _SPD_A)]
    if p == 8:
        return _RV["spd"]
    return []


_SPD_N = sum(len(_spd_rows(p)) for p in LAB_PAGES)


def _spd_attr(p):
    r = _spd_rows(p)
    return [("spd", ";".join("%s,%s" % (nm, _n3(round(s, 1))) for nm, _L, s in r))] if r else []


def _lw(pts, p):
    return _n3(_xylen([(q[0], q[1]) for q in pts]))


def lab_data(p):
    """把该页场景的周期 / 相位 / 关键几何 / 墨迹名册摊到舞台的 data-* 上。
       闸门因此可以**静态复算**，不必去读着色器、也不必截图比对。"""
    a = []
    if p == 1:
        a += [("spin", _LAB.VSPIN), ("intro", _LAB.VINTRO), ("pts", _LAB.VN),
              ("amp", _LAB.VAMP), ("w0", _LAB.VW0),
              ("harm", ";".join(",".join(str(x) for x in hh) for hh in _LAB.VHARM)),
              ("hot", "%s,%s" % _LAB.VHOT)]
    elif p == 2:
        # 地球：自转周期 / 入场 / 节点数 / 取道数 / 三组弧相位全部**现取自旗舰**；
        # globe = 球心与屏上半径，genv = 弧外包络的投影半径（⑳globe 拿它复算净空）。
        a += [("spin", _LAB.GSPIN), ("intro", _LAB.GINTRO),
              ("nodes", len(_LAB._NODES_LL)), ("routes", len(_LAB._ROUTES)),
              ("arc-dur", _LAB.ARC_DUR_S.strip("[]")),
              ("arc-gap", _LAB.ARC_GAP_S.strip("[]")),
              ("arc-off", _LAB.ARC_OFF_S.strip("[]")),
              ("globe", "%s,%s,%s" % (_n3(_G_CX), _n3(_G_CY), _n3(_G_R))),
              ("genv", _n3(round(_G_ENV, 2)))]
    elif p == 3:
        a += [("trunks", len(_MX_LINES)), ("aux", len(_MX_AUX)),
              ("trunkx", ",".join(str(m[0]) for m in _MX_LINES)),
              ("grid", "%d,%d" % (_GW_GN, _GW_GM)), ("zfar", _n3(_GW_ZFAR)),
              ("z", "%s,%s,%s" % (_n3(-_GW_ZFAR), _n3(_GW_AUXZ), _n3(_GW_ZTOP))),
              ("base", "%d,%d" % (_GW_BASEY, _GW_TOP)),
              ("w", "%s-%s" % (_n3(_GW_W0), _n3(_GW_W1)))]
    elif p == 4:
        # 双向声带：跑道 / 圈数 / 相位 / 截断线 / NOW —— 全部现取自旗舰的常量
        a += [("span", "%s,%s" % (_n3(_LAB._D_X0), _n3(_LAB._D_X1))),
              ("turns", _n3(_LAB._D_TURNS)), ("phase", _n3(_LAB._D_PHASE)),
              ("amp", _n3(_LAB._D_AMP)), ("dep", _n3(_LAB._D_DEP)),
              ("hw", _n3(_D_HW)), ("cut", str(_LAB._XIN)), ("now", str(_LAB._XNOW)),
              ("cross", "2"),
              ("chip", "%s,%s,%s,%s" % tuple(_n3(v) for v in _P4_CHIP)),
              ("chipclr", _n3(_P4_CHIP_CLR))]
    elif p == 5:
        # 大脑：五区周期 / 相位 / 突触弧数 / 摇摆 —— 与旗舰 lab_data(17) 逐字同源
        a += [("zper", ",".join(str(_LAB._sec(z[1])) for z in _LAB._ZONES)),
              ("zoff", ",".join(str(_LAB._sec(z[2])) for z in _LAB._ZONES)),
              ("arcs", len(_LAB._ARCS)),
              ("sparks", len(_LAB._ARCS) + len(_LAB._ARC_EXTRA)),
              ("sway", _n3(_B_SWAY)), ("sway-p", _n3(_B_SWAYP)),
              ("tmax", _n3(_B_TMAX))]
    elif p == 6:
        a += [("lam", _n3(_LAB._AS_LAM)),
              ("z", "%s,%s,%s" % (_n3(_EX_P0[2]), _n3(_EX_P2[2]), _n3(-_EX_DZBOX))),
              ("frame", "%s,%s,%s,%s" % tuple(_n3(v) for v in _EX_BOX)),
              ("inset", "%s,%s" % (_n3(_EX_INS), _n3(_EX_INS2))),
              ("uframe", _n3(_EX["uframe"])), ("gain", "%s,%s" % (_n3(_EX_G0), _n3(_EX_GSPAN))),
              ("w", "%s-%s" % (_n3(_EX_W0), _n3(_EX_W1)))]
    elif p == 7:
        # 星座墙：卡数 / 摆动周期（⑳flick 用 cyc）/ 浮动 / 体厚 / 深度区间
        a += [("cards", len(_W_CARDS)), ("front", 3),
              ("sway", _n3(_W_SWAY)), ("cyc", _n3(_W_CYC)),
              ("famp", _n3(_W_FAMP)), ("fper", _n3(_W_FPER)),
              ("dz", _n3(_W_DZ)),
              ("z", "%s,%s" % (_n3(min(c[4] for c in _W_CARDS)),
                               _n3(max(c[4] for c in _W_CARDS))))]
    elif p == 8:
        a += [("trib", len(_TRIB)), ("lam", _n3(_RV_LAM)),
              ("tlen", ",".join(_n3(v) for v in _RV["tlen"])),
              ("rvphase", ",".join(_n3(v) for v in _RV["off"])),
              ("zsrc", _n3(_RV_ZSRC)), ("bed", _n3(_RV_BED)),
              ("meet", "%d,%d" % (_P8_CX, _P8_CY)),
              # 支流「源头-河口」/ 主河道「基准-河口涌起」——qa 的 ⑳rv 只透传不判
              ("w", "%s-%s,%s-%s" % (_n3(_RV_WT0), _n3(_RV_WT1),
                                     _n3(_RV_WM), _n3(_RV_WMOUTH)))]
    if p in _INK:
        a += [("ink", ";".join("%s,%s,%s,%s" % tuple(_n3(v) for v in b) for b in _INK[p])),
              ("clr", _n3(_CLR[p][0])), ("clr-min", _n3(round(_CLR_MIN[p], 2)))]
    return "".join(' data-lab-%s="%s"' % kv for kv in a + _spd_attr(p))


def lab_stage(p):
    """一页的 3D 舞台层：辉光（仅声场球）+ poster（仅 P1 有专用 svg）+ 打印帧位。
       **canvas 不在这里** —— 全 deck 只有一枚，常驻车库，翻页时搬进来。"""
    kind, rx, ry, rw, rh = LAB_RECTS[p]
    atmo = poster = ""
    if kind == "voice":
        aw = _LAB.VGR * 2 * 1.35
        atmo = ('<div class="lab-atmo" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;'
                'background:radial-gradient(circle closest-side,transparent 62%%,var(--v-atmo) 74%%,'
                'transparent 87%%);opacity:var(--v-atmo-int)"></div>'
                % (_LAB.VCX - aw / 2, _LAB.VCY - aw / 2, aw, aw))
        poster = ('<svg class="lab-poster" id="labPoster1" viewBox="0 0 1920 1080" aria-hidden="true">'
                  '<path class="v-wire-b" d="%s"/><path class="v-dot-b" d="%s"/>'
                  '<path class="v-wire" d="%s"/><path class="v-dot" d="%s"/>'
                  '<path class="v-dot-h" d="%s"/></svg>'
                  % (_V_POSTER["wireB"], _V_POSTER["back"], _V_POSTER["wire"],
                     _V_POSTER["front"], _V_POSTER["hot"]))
    elif kind == "globe":
        # 辉光 + poster 都**现取自旗舰**（`_LAB.GPOSTER` 是构建期用与运行时逐字同参的
        # 相机矩阵离线投影出来的那一份）⇒ poster 与 WebGL 是同一张图，交接不跳。
        aw = _G_R * 2 * 1.35
        atmo = ('<div class="lab-atmo" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;'
                'background:radial-gradient(circle closest-side,transparent 62%%,var(--g-atmo) 74%%,'
                'transparent 87%%);opacity:var(--g-atmo-int)"></div>'
                % (_G_CX - aw / 2, _G_CY - aw / 2, aw, aw))
        poster = ('<svg class="lab-poster" id="labPoster2" viewBox="0 0 1920 1080" aria-hidden="true">'
                  '<circle class="g-ocean" cx="%s" cy="%s" r="%s"/>'
                  '<path class="g-grat" d="%s"/><path class="g-land" d="%s"/>%s'
                  '<path class="g-node" d="%s"/>'
                  '<circle class="g-rim" cx="%s" cy="%s" r="%s"/></svg>'
                  % (_n3(_G_CX), _n3(_G_CY), _n3(_G_R), _G_POSTER["grat"], _G_POSTER["land"],
                     "".join('<path class="g-arc" d="%s"/>' % d for d in _G_POSTER["arcs"]),
                     _G_POSTER["nodes"], _n3(_G_CX), _n3(_G_CY), _n3(_G_R)))
    pr = ('<img class="lab-print" id="labPrint%d" alt="" aria-hidden="true" '
          'style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (p, rx, ry, rw, rh))
    return ('<div class="lab-stage" id="labStage%d" data-lab-page="%d" data-lab-scene="%s" '
            'data-lab-rect="%d,%d,%d,%d"%s aria-hidden="true">%s%s%s</div>'
            % (p, p, kind, rx, ry, rw, rh, lab_data(p), atmo, poster, pr))


def info_k():
    """常量表：构建期算好，运行时直接吃 —— 也是「3D 不新造坐标」的唯一保证。"""
    def O(d):
        return "{" + ",".join("%s:%s" % (k, v) for k, v in d) + "}"

    def PL(pts, w, h, D):
        return '"%s"' % _pk3(_lock_path(pts, w, h, D))

    def PA(pts, w, h, D):
        return "[" + ",".join(_arr3(q) for q in _lock_path(pts, w, h, D)) + "]"

    def INK(p):
        return "[" + ",".join(_arr3(b) for b in _INK[p]) + "]"

    gw = O([("D", _n3(_GW_D)), ("half", _n3(_GW_HALF)),
            ("basey", str(_GW_BASEY)),
            ("grid", "[" + ",".join(PL(g, _GW["w"], _GW["h"], _GW_D)
                                    for g in _GW["grid"]) + "]"),
            ("boxdz", _n3(_GW_BOXDZ)), ("auxz", _n3(_GW_AUXZ)), ("auxdz", _n3(_GW_AUXDZ)),
            ("box", "[" + ",".join(_arr3(b) for b in _GW["box"]) + "]"),
            ("aux", "[" + ",".join(_arr3(b) for b in _GW["aux"]) + "]"),
            ("link", "[" + ",".join(
                PL(_lerp_line(a, b, 24), _GW["w"], _GW["h"], _GW_D)
                for a, b in _GW["link"]) + "]"),
            ("base", "[" + ",".join(_arr3(q) for q in
                     _lock_path([(0, _GW_BASEY, 0), (1668, _GW_BASEY, 0),
                                 (1668, _GW_BASEY + _GW_BASEH, 0),
                                 (0, _GW_BASEY + _GW_BASEH, 0),
                                 (0, _GW_BASEY, 0)], _GW["w"], _GW["h"], _GW_D)) + "]"),
            ("trunk", "[" + ",".join(PL(q, _GW["w"], _GW["h"], _GW_D)
                                     for q in _GW["trunk"]) + "]"),
            ("spd", "[" + ",".join(_n3(v) for v in _GW["spd"]) + "]"),
            ("w0", _n3(_GW_W0)), ("w1", _n3(_GW_W1)),
            ("wpx", _n3(max(_wpx(_GW_WMAX, q, _GW_D) for q in _GW["trunk"]))),
            ("ink", INK(3))])
    # ── ④ 双向声带（P4）· K 表**逐条现取自旗舰的 lab_k()**（同一批模块常量、
    #    同一条 `_spd_rows(4)` 反推周期）；本文件只补 D / pad / ink 三项供 withClr 用。
    _r4 = _LAB._spd_rows(4)
    d = _LAB._obj([
        ("x0", _LAB._n(_LAB._D_X0)), ("x1", _LAB._n(_LAB._D_X1)),
        ("yc", _LAB._n(_LAB._D_YC)),
        ("amp", _LAB._n(_LAB._D_AMP)), ("dep", _LAB._n(_LAB._D_DEP)),
        ("turns", _LAB._n(_LAB._D_TURNS)), ("phase", _LAB._n(_LAB._D_PHASE)),
        ("lap0", _LAB._n(10.0)), ("lap1", _LAB._n(64.0)),
        ("cut", _LAB._n(float(_LAB._XIN))), ("ghost", _LAB._n(0.16)),
        ("cy0", _LAB._n(60.0)), ("cy1", _LAB._n(330.0)), ("n", str(_LAB._D_N)),
        ("hw", _LAB._n(_D_HW)),
        ("durA", _LAB._n(_LAB._dur_at(_r4[0][1], _r4[0][2]))),
        ("durB", _LAB._n(_LAB._dur_at(_r4[1][1], _r4[1][2]))),
        # info 专属三项（旗舰不需要）：withClr 的逆投影深度 / 净空 pad / 墨迹名册
        ("D", _n3(_D_D)), ("pad", _n3(0.0)), ("ink", INK(4)),
    ])
    # ── ⑤ 五脑区大脑（P5）· 同上，整块现取（母形 / 五区 / 脑沟 / 突触弧 / 输入通路）
    _bb = _LAB._bbox(_LAB._BRAIN)
    _bc = [(_bb[0] + _bb[2]) / 2.0, (_bb[1] + _bb[3]) / 2.0]
    _arcA = [0.42 * a2[1] for a2 in _LAB._ARCS]
    _spark = [(k, _LAB._sec(a2[2]), _LAB._sec(a2[3])) for k, a2 in enumerate(_LAB._ARCS)] \
        + [(k, _LAB._sec(_LAB._ARCS[k][2]), _LAB._sec(dl)) for k, dl in _LAB._ARC_EXTRA]
    b = _LAB._obj([
        ("cont", '"%s"' % _LAB._poly(_LAB._BRAIN, per=18, tol=1.2)),
        ("zones", "[" + ",".join('"%s"' % _LAB._polym(z[0]) for z in _LAB._ZONES) + "]"),
        ("sul", "[" + ",".join('"%s"' % _LAB._poly(q)
                               for q in (_LAB._SUL1, _LAB._SUL2, _LAB._SUL3)) + "]"),
        ("sulD", _LAB._arr([0.30, 0.56, 0.34])),
        ("sulW", _LAB._arr([22, 27, 20])),
        ("bb", _LAB._arr(_bb)), ("c", _LAB._arr(_bc)),
        ("tmax", _LAB._n(_B_TMAX)), ("dref", _LAB._n(108.0)), ("n", "12000"),
        ("arcs", "[" + ",".join('"%s"' % _LAB._poly(a2[0], per=16, tol=2.0)
                                for a2 in _LAB._ARCS) + "]"),
        ("arcA", _LAB._arr(_arcA)),
        ("spark", "[" + ",".join(_LAB._arr(q) for q in _spark) + "]"),
        ("zper", _LAB._arr([_LAB._sec(z[1]) for z in _LAB._ZONES])),
        ("zoff", _LAB._arr([_LAB._sec(z[2]) for z in _LAB._ZONES])),
        ("inp", '"%s"' % _LAB._poly(_LAB._BRAIN_IN, per=16, tol=2.0)),
        ("outX", _LAB._n(1088.0)), ("out", _LAB._arr([1214, 268])),
        ("out2", _LAB._arr([1386, 268])),
        ("sub", "[" + ",".join('"%s"' % _LAB._poly(q, per=16, tol=1.4)
                               for q in (_LAB._CEREB, _LAB._STEM)) + "]"),
        ("subT", _LAB._arr([52, 30])), ("subN", "1500"),
        ("sway", _LAB._n(_B_SWAY)), ("swayP", _LAB._n(_B_SWAYP)),
        # info 专属三项：pad 取暗档火花点径的一半（5.2/2 = 2.6，两档取大）
        ("D", _n3(_B_D)), ("pad", _n3(_cssmax("--b-spark-size") / 2.0)), ("ink", INK(5)),
    ])
    # ── ⑧ 星座墙（P7）：十四张卡的舞台像素几何 + 贴图地址 + 摆动 / 浮动参数
    w7 = O([("D", _n3(_W_D)),
            ("cx", _n3(_W_CX)), ("cy", _n3(_W_CY)), ("cz", _n3(_W_CZ)),
            ("sway", _n3(_W_SWAY)), ("cyc", _n3(_W_CYC)),
            ("famp", _n3(_W_FAMP)), ("fper", _n3(_W_FPER)),
            ("dz", _n3(_W_DZ)), ("ins", _n3(_W_INS)),
            ("zmin", _n3(min(c[4] for c in _W_CARDS))),
            ("zmax", _n3(max(c[4] for c in _W_CARDS))),
            ("card", "[" + ",".join(
                "[%s,%s,%s,%s,%s,%s]"
                % (_n3(c[2]), _n3(c[3]), _n3(c[4]), _n3(c[5]), _n3(c[6]),
                   _n3(2 * math.pi * c[7] / 14.0))
                for c in _W_CARDS) + "]"),
            ("url", "[" + ",".join('"%s"' % c[1] for c in _W_CARDS) + "]"),
            ("ink", INK(7))])
    rv = O([("D", _n3(_RV_D)), ("half", _n3(_RV_HALF)),
            ("trib", "[" + ",".join(PL(q, _RV["w"], _RV["h"], _RV_D)
                                    for q in _RV["trib"]) + "]"),
            ("main", PL(_RV["main"], _RV["w"], _RV["h"], _RV_D)),
            ("rail", PL(_RV["rail"], _RV["w"], _RV["h"], _RV_D)),
            ("bed", PL([(q[0], q[1], -_RV_BED) for q in _RV["rail"]],
                       _RV["w"], _RV["h"], _RV_D)),
            ("src", PL(_RV["src"], _RV["w"], _RV["h"], _RV_D)),
            ("meet", PL(_RV["meet"], _RV["w"], _RV["h"], _RV_D)),
            ("off", "[" + ",".join(_n3(v) for v in _RV["off"]) + "]"),
            ("tlen", "[" + ",".join(_n3(v) for v in _RV["tlen"]) + "]"),
            ("spd", _n3(_SPD_A)),
            ("wt0", _n3(_RV_WT0)), ("wt1", _n3(_RV_WT1)),
            ("wm", _n3(_RV_WM)), ("wmouth", _n3(_RV_WMOUTH)),
            ("wacc", _n3(_RV_WACC)), ("mfloor", _n3(_RV_MFLOOR)),
            ("wtpx", _n3(max(_wpx(_RV_WT, q, _RV_D) for q in _RV["trib"]))),
            ("wmpx", _n3(_wpx(_RV_WMAX, _RV["main"], _RV_D))),
            ("ink", INK(8))])
    ex = O([("D", _n3(_EX_D)), ("half", _n3(_EX_HALF)),
            ("path", PL(_EX["page"], _EX["w"], _EX["h"], _EX_D)),
            ("lb", '["%s","%s"]' % (_pk3(_EX["lb"][0]), _pk3(_EX["lb"][1]))),
            ("inner", '"%s"' % _pk3(_EX["inner"])), ("quad", '"%s"' % _pk3(_EX["quad"])),
            ("dot", PL([_EX_DOT], _EX["w"], _EX["h"], _EX_D)),
            ("spd", _n3(_EX["spd"])), ("uframe", _n3(_EX["uframe"])),
            ("g0", _n3(_EX_G0)), ("gspan", _n3(_EX_GSPAN)),
            ("floor", _n3(_EX_FLOOR)), ("edge", _n3(_EX_EDGE)),
            ("w0", _n3(_EX_W0)), ("w1", _n3(_EX_W1)),
            ("wpx", _n3(_wpx(_EX_W1, _EX["page"], _EX_D))),
            ("ink", INK(6) if P6_EXIT else "[]")])
    return "{" + ",".join([
        "W:1920", "H:1080", "FPX:%s" % _n3(_LAB.FPX), 'rev:"%s"' % _LAB.THREE_REV,
        # ① 声场球：与 lab P1 **逐字同参**（球心 / 半径 / 谐波 / 自转 / 入场全部现取）
        "v:{" + ",".join([
            "cam:" + _arr3(_LAB.VCAM.C), "tilt:%s" % _n3(_LAB.VTILT),
            "spin:%s" % _n3(_LAB.VSPIN), "n:%d" % _LAB.VN, "amp:%s" % _n3(_LAB.VAMP),
            "w0:%s" % _n3(_LAB.VW0),
            "ha:" + _arr3([hh[0] for hh in _LAB.VHARM]),
            "hw:" + _arr3([hh[1] for hh in _LAB.VHARM]),
            "hk:" + _arr3([hh[2] for hh in _LAB.VHARM]),
            "hp:" + _arr3([hh[3] for hh in _LAB.VHARM]),
            "hot:" + _arr3(_LAB.VHOT), "introSec:%s" % _n3(_LAB.VINTRO)]) + "}",
        # lab-kit ⑨ · audioStream 参数表（与旗舰同一份 —— 全家族同一种介质）
        "as:" + O([("a", _arr3(_LAB._AS_A)), ("f", _arr3(_LAB._AS_F)),
                   ("ph", _arr3(_LAB._AS_PH)), ("lam", _n3(_LAB._AS_LAM)),
                   ("floor", _n3(_LAB._AS_FLOOR)), ("ghost", _n3(_LAB._AS_GHOST)),
                   ("grain", _n3(_LAB._AS_GRAIN)), ("grainL", _n3(_LAB._AS_GRAINL)),
                   ("edge", _n3(_LAB._AS_EDGE)), ("crest", _n3(_LAB._AS_CREST)),
                   ("comp", _n3(_LAB._AS_COMP)), ("spd", _n3(_SPD_A))]),
        # ② SD-RTN 地球：构图 / 相机 / 位掩码陆地 / 示意节点 / 取道表 / 三组弧相位
        #    **全部现取自旗舰**（一个数都不在本文件里重写）
        "g:" + O([("cam", _arr3(_LAB.GCAM.C)), ("tilt", _n3(_LAB.GTILT)),
                  ("y0", _n3(_LAB.GY0)), ("spin", _n3(_LAB.GSPIN)),
                  ("introSec", _n3(_LAB.GINTRO))]),
        'landBits:"%s"' % _LAB.LAND_BITS, "landN:%d" % _LAB.LAND_N,
        'nodeTable:"%s"' % _LAB.NODE_TABLE, 'routeTable:"%s"' % _LAB.ROUTE_TABLE,
        "arcDur:%s" % _LAB.ARC_DUR_S, "arcGap:%s" % _LAB.ARC_GAP_S,
        "arcOff:%s" % _LAB.ARC_OFF_S,
        "gw:" + gw, "d:" + d, "b:" + b, "w:" + w7, "rv:" + rv, "ex:" + ex,
    ]) + "}"


# ── 运行时装配：地基（旗舰现取）+ 本 deck 五枚场景 + 单渲染器巡游 ──────────
_FACTORY_JS = ("const FACTORY = { voice:makeVoice, globe:makeGlobe, grow:makeGrow,\n"
               "                  duplex:withClr(makeDuplex, K.d.D, K.d.ink, K.d.pad),\n"
               "                  brain:withClr(makeBrain, K.b.D, K.b.ink, K.b.pad),\n"
               "                  wall:makeWall, river:makeRiver, exit:makeExit };")
_TOUR_JS = _re2.sub(r"const FACTORY = \{[\s\S]*?\};", lambda _m: _FACTORY_JS, _K_TOUR, count=1)
assert "makeGlobe" in _TOUR_JS and "withClr(makeBrain" in _TOUR_JS, "FACTORY 替换失败"
INFO_MODULE_BODY = (_K_BASE + _K_VOICE + _K_GLOBE + _K_BRAIN + _K_LOCK + _K_AS + _K_CLR
                    + _K_DUPLEX + INFO_SCENES + _TOUR_JS)

# ═══ 引擎详解抽屉 + 深链的行为层（独立 <script>，不碰共享的 deck.js）═══════════
#   入口三处（chip 点击 与 该页 Enter 同效）：
#     P4 · #engineExpand → 引擎 #1  （引擎产品详解，全篇）
#     P5 · #agentExpand  → 引擎 #16 （Call Agent 章）
#     P6 · #physExpand   → 引擎 #19 （R1 开发套件）
#   收回：Esc（父窗口或 iframe 内都认）、点 scrim、点 ESC 按钮。
#   键盘纪律：window 的 capture 阶段拦一层 —— 抽屉开着时除 Esc 外全部吞掉，
#             免得按键漏进 deck.js 把底下的 deck 翻页。E 键归就地编辑器，不许占用。
#   深链实现：iframe 未加载 ⇒ 首次 src 直接带 #N（引擎 deck.js 的 constructor 读 hash）；
#             已加载 ⇒ 改 contentWindow.location.hash（引擎 deck.js 有 hashchange 监听，
#             实测同源可写），同 hash 不写、避免无事件空转；取不到 contentWindow 时
#             重设 src 强制带 hash 重载（可接受的降级）。**引擎 deck 零改动。**
#   归档 srcdoc 模式：无 data-src ⇒ 懒加载守卫静默，深链降级为普通展开。
ENGINE_DRAWER_JS = """<script>(function(){
var ov=document.getElementById("engineOverlay"),
    fr=document.getElementById("engineFrame");
if(!ov||!fr)return;
var chips=[].slice.call(document.querySelectorAll(".chip-expand[data-eng-hash]"));
var scrim=ov.querySelector(".eo-scrim"),btn=ov.querySelector(".eo-close"),loaded=false;
/* 页 → 引擎章号：P4 全篇 / P5 Call Agent / P6 R1。改页序必须同步改这张表。 */
var PAGE_HASH={"4":"1","5":"16","6":"19"};
function isOpen(){return !ov.hidden;}
/* ── 主题实时联动 ────────────────────────────────────────────────────────
   iframe 首帧靠 <head> 里读 localStorage("colin-theme") 自跟随；但抽屉开着时
   宿主再点 deckSwap，iframe 已经加载完、不会二次读 localStorage —— 底下是深色、
   抽屉里还是浅色。这里用 MutationObserver 盯宿主 html[data-theme]，
   一变就把 iframe 的 documentElement 与它自己的 localStorage 一起对齐。
   引擎 deck 暴露了 window.__setTheme（同时管 data-theme 与按钮文案），优先走它。 */
function hostTheme(){return document.documentElement.getAttribute("data-theme")==="dark"?"dark":"light";}
function syncTheme(){
  var t=hostTheme(),w=null;
  try{w=fr.contentWindow;}catch(e){}
  if(!w||!w.document||!w.document.documentElement)return;
  try{w.localStorage.setItem("colin-theme",t);}catch(e){}
  if(typeof w.__setTheme==="function"){try{w.__setTheme(t);return;}catch(e){}}
  if(t==="dark")w.document.documentElement.setAttribute("data-theme","dark");
  else w.document.documentElement.removeAttribute("data-theme");
}
try{new MutationObserver(function(){if(loaded)syncTheme();})
      .observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});}catch(e){}
/* ── 反向：iframe → 宿主（2026-08-23 采纳项 A · 把单向同步补成双向）──────────
   上面那只 observer 只管「宿主变了推给 iframe」。抽屉开着时讲者顺手点的往往是
   **iframe 里那枚 deckSwap**（它就在抽屉左下角、比宿主那枚更顺手）——
   引擎 deck 的按钮写 localStorage("colin-theme") 再 apply，宿主此前完全不知情：
   收回抽屉，底下 8 页还是旧主题。
   同源 iframe（含归档 srcdoc 态）写 localStorage 会在**宿主窗口**触发 storage 事件
   （同一个 window 自己写不触发 ⇒ 宿主点自己的 deckSwap 不会回环，天然无死循环）。
   这里只认 colin-theme 这一个键，先判不同再落属性（免得无谓抖动）；
   宿主属性一变，上面那只 observer 会再把同一个值推回 iframe —— 幂等，无害。
   优先走宿主自己的 __setTheme：它同时管 data-theme 与 deckSwap 的按钮文案。 */
window.addEventListener("storage",function(e){
  if(!e||e.key!=="colin-theme")return;
  var t=(e.newValue==="dark")?"dark":"light";
  if(hostTheme()===t)return;
  if(typeof window.__setTheme==="function"){try{window.__setTheme(t);return;}catch(err){}}
  if(t==="dark")document.documentElement.setAttribute("data-theme","dark");
  else document.documentElement.removeAttribute("data-theme");
});
function bindInner(){
  var w=null;try{w=fr.contentWindow;}catch(e){}
  if(!w||w.__engineEscBound)return;   /* 标志位挂在内层 window 上：每次 load 换新 window 自动失效 */
  w.__engineEscBound=true;
  w.addEventListener("keydown",function(e){
    if(e.key==="Escape"){e.preventDefault();closeDrawer();}
  });
}
function focusInner(){try{fr.contentWindow.focus();}catch(e){}bindInner();}
function goHash(h){
  if(!h)return;
  var w=null;try{w=fr.contentWindow;}catch(e){}
  if(w&&w.location){
    try{
      if(String(w.location.hash)!=="#"+h)w.location.hash="#"+h;   /* 引擎 deck.js 有 hashchange 监听 */
      return;
    }catch(e){}
  }
  if(fr.dataset.src){loaded=false;fr.setAttribute("src",fr.dataset.src+"#"+h);}   /* 兜底：带 hash 重载 */
}
fr.addEventListener("load",function(){loaded=true;syncTheme();if(isOpen())focusInner();});
function openDrawer(h){
  if(!fr.getAttribute("src")){
    /* 懒加载：首次展开才拉 22 页，并直接带上目标章号。
       归档 srcdoc 态无 data-src ⇒ 此处静默（srcdoc 已内联，深链降级为普通展开）。 */
    if(fr.dataset.src)fr.setAttribute("src",fr.dataset.src+(h?"#"+h:""));
  }else if(h){goHash(h);}
  ov.hidden=false;
  if(loaded){syncTheme();focusInner();}                 /* 每次展开都以宿主当前主题为准重新对齐 */
}
function closeDrawer(){ov.hidden=true;window.focus();}
chips.forEach(function(c){
  var h=c.getAttribute("data-eng-hash");
  c.addEventListener("click",function(){c.blur();openDrawer(h);});
  c.addEventListener("keydown",function(e){
    if(e.key==="Enter"||e.key===" "){e.preventDefault();e.stopPropagation();openDrawer(h);}
  });
});
scrim.addEventListener("click",closeDrawer);
btn.addEventListener("click",function(){btn.blur();closeDrawer();});   /* 点完就摘焦点，不留 ring */
window.addEventListener("keydown",function(e){
  if(isOpen()){
    if(e.key==="Escape"){e.preventDefault();e.stopImmediatePropagation();closeDrawer();return;}
    e.stopImmediatePropagation();return;   /* 抽屉开着：其余按键一律不许漏进 deck.js */
  }
  if(e.key!=="Enter")return;
  var t=e.target;
  if(t&&t.getAttribute&&t.getAttribute("contenteditable"))return;   /* 就地编辑态不抢 Enter */
  if(t&&t.id==="deckSwap")return;                                   /* 主题按钮的 Enter 归它自己 */
  if(t&&t.classList&&t.classList.contains("chip-expand"))return;    /* chip 聚焦态的 Enter 归它自己 */
  var cur=document.querySelector(".slide.active");
  var p=cur&&cur.dataset?cur.dataset.p:null;
  if(!p||!PAGE_HASH[p])return;                                      /* 只在 P4 / P5 / P6 认 Enter */
  e.preventDefault();e.stopImmediatePropagation();openDrawer(PAGE_HASH[p]);
},true);
})();</script>
"""

# ═══ 细节层的行为层（v3 · 独立 <script>，同样不碰共享的 deck.js）═══════════════
#   面板本身**没有自己的状态**：它就是该页的 data-step=1。所以这里只做两件小事 ——
#     ① chip「细节 ⏎」：点击 / Enter / 空格 ⇒ 走 deck 的第 1 步（与 → 完全同一条路）；
#     ② Esc ⇒ 退回第 0 步（← 由 deck.js 的 prev() 天然管着，这里不重复实现）。
#   键盘纪律：Esc 走 capture 阶段，但**排在引擎抽屉之后**注册 ——
#     抽屉开着时它的 stopImmediatePropagation 先吞掉 Esc（Esc 归抽屉），
#     抽屉收起后 Esc 才落到面板上。两层互不打架，靠的是注册顺序，不是标志位。
DETAIL_JS = """<script>(function(){
var chips=[].slice.call(document.querySelectorAll(".chip-detail"));
function step(n){
  var d=window.deck; if(!d)return;
  if(d.step===n)return;
  d.step=n; d.applySteps();
}
function hasPanel(){
  var cur=document.querySelector(".slide.active");
  return !!(cur&&cur.querySelector(".detail"));
}
chips.forEach(function(c){
  c.addEventListener("click",function(){c.blur();step(1);});
  c.addEventListener("keydown",function(e){
    if(e.key==="Enter"||e.key===" "){e.preventDefault();e.stopPropagation();c.blur();step(1);}
  });
});
window.addEventListener("keydown",function(e){
  if(e.key!=="Escape")return;
  var ov=document.getElementById("engineOverlay");
  if(ov&&!ov.hidden)return;                 /* 抽屉开着：Esc 归抽屉 */
  if(!hasPanel())return;
  var d=window.deck; if(!d||d.step===0)return;
  e.preventDefault();e.stopImmediatePropagation();step(0);
},true);
})();</script>
"""


# ═══ 组装 ═══════════════════════════════════════════════════════════════════
def build():
    total = len(PAGES)
    secs = []
    for i, (board, steps, body, hero, labk) in enumerate(PAGES, 1):
        sig = '<div class="sig">%d/%d</div>' % (i, total)
        # 3D 舞台夹在背景板与 .pp 之间：两者都是 z-index:0，靠**文档序**分先后。
        # 无场景的页插入空串 ⇒ 这条模板拼出的字节与改造之前完全相同。
        assert (labk is not None) == (i in LAB_RECTS), "P%d 的 lab= 声明与 LAB_RECTS 不一致" % i
        if labk is not None:
            assert labk == LAB_RECTS[i][0], "P%d 场景名分叉：%s vs %s" % (i, labk, LAB_RECTS[i][0])
        labh = ("  " + lab_stage(i) + "\n") if labk else ""
        hero_html = ""
        if hero and HERO_ART:
            name, style = hero
            st = ' style="%s"' % style if style else ""
            # name = 资产 basename（不含 -light/-dark 与扩展名），相对 /decks/assets/convoai/
            hero_html = ('<img class="hero-art lt" src="%s%s-light.png" alt=""%s>'
                         '<img class="hero-art dk" src="%s%s-dark.png" alt=""%s>'
                         % (A, name, st, A, name, st))
        secs.append(
            '<section class="slide conf-boarded" data-p="%d" data-steps="%d">\n'
            '  <div class="conf-bg conf-bg-%s" aria-hidden="true"></div>%s\n%s'
            '  <div class="pp">%s%s</div>\n</section>'
            % (i, steps, board, hero_html, labh, sig, body))
    chrome = ('<div class="deck-grid" aria-hidden="true"></div>'
              '<div class="deck-rail t" aria-hidden="true"></div>'
              '<div class="deck-rail b" aria-hidden="true"></div>')
    doc = (
        '<!DOCTYPE html>\n<html lang="zh-CN"><head>\n'
        # 主题初始化：**无值时默认浅色**（Colin 拍板：速讲 / 微信转发场景以浅底为准）。
        # 键名与引擎 deck 同一个 —— 同源 iframe 里引擎自动跟随宿主主题，别改键名。
        '<script>try{if(localStorage.getItem("colin-theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}</script>\n'
        '<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>声网对话式 AI · 一页一章 Infograph · 姚光华 Colin</title>\n'
        + FONTS
        + "<style>" + css("conf-theme-dual.css") + "</style>"
        + "<style>" + css("stage.css") + "</style>"
        + "<style>" + css("motion.css") + "</style>"
        + "<style>" + css("components.css") + "</style>"
        + "<style>" + css("conf-chrome.css").split("<svg class=\"deck-flow\"")[0] + "</style>"   # 流场退役：只取 CSS
        + BOARDS_CSS + DECK_CSS + LAB_CSS
        + "\n</head>\n<body>\n"
        '<div class="deck-viewport">\n  <div class="deck-stage" id="deckStage">\n'
        + chrome + "\n" + "\n".join(secs) + "\n  </div>\n</div>\n"
        # 车库：全 deck 唯一那块 canvas 的常驻位（屏外）。挂在 .deck-viewport 之外 ——
        # 舞台自带 overflow:hidden + transform:scale，canvas 停在里面会被裁 / 被缩。
        + lab_garage() + "\n"
        # 引擎详解抽屉：必须与 .deck-viewport 平级 —— 塞进 .deck-stage 就会吃到舞台的
        # translate+scale，iframe 内的原生滚动/点击坐标系全歪。
        '<div id="engineOverlay" hidden>\n'
        '  <div class="eo-scrim"></div>\n'
        '  <div class="eo-sheet">\n'
        '    <iframe id="engineFrame" data-src="/decks/convoai-engine.html" '
        # 2026-08-23 引擎 deck 封面换「对话即交互」后定位升为深入讲解版，decks.ts 的标题行
        # 已同步；抽屉 iframe 的 title 是这条改名唯一漏掉的落点（屏幕阅读器 / 悬停提示读它）。
        'title="声网 · 对话式 AI 引擎 · 深入讲解"></iframe>\n'
        '    <button class="eo-close" type="button">ESC · 收回</button>\n'
        '  </div>\n</div>\n'
        '<div class="deck-progress" id="deckProgress"></div>\n'
        '<div class="deck-steps" id="deckSteps"></div>\n'
        '<div class="edit-hotzone" aria-hidden="true"></div>\n'
        '<button class="edit-toggle" id="editToggle">EDIT</button>\n'
        '<button class="deck-swap" id="deckSwap">暗底</button>\n'
        # 2026-08-21 Colin：deckSwap 与引擎 deck 对齐为**常显 chip**（.62 → hover 1）。
        # 这份 deck 同样会被直接发链接，「默认隐身 · hover 呼出」等于键不存在。
        # 实底 --card-bg-2 而不是 transparent —— 左下角坐着 content 板的矩阵纹理，
        # 透明底会让 12px mono 掉进纹理里。只有 @media print 隐藏。
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
        'else{document.documentElement.removeAttribute("data-theme");b.textContent="暗底";}'
        'document.querySelectorAll(".strip img.lt").forEach(function(el){el.style.display=(t==="dark")?"none":"block";});'
        'document.querySelectorAll(".strip img.dk").forEach(function(el){el.style.display=(t==="dark")?"block":"none";});}'
        'var cur="light";try{cur=localStorage.getItem("colin-theme")||"light";}catch(e){}apply(cur);'
        # 点击时从 DOM 现场读当前态（不吃闭包变量的陈旧值）：宿主抽屉会从外部改这份文档的
        # data-theme，闭包里的 cur 会过期，再点就把主题切反。
        'window.__setTheme=apply;'
        'b.addEventListener("click",function(){b.blur();'
        'var now=document.documentElement.getAttribute("data-theme")==="dark"?"dark":"light";'
        'var nxt=(now==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",nxt);}catch(e){}apply(nxt);});})();</script>\n'
        + ENGINE_DRAWER_JS
        + DETAIL_JS
        # ── LAB 运行时（前奏 classic + importmap + module 本体）────────────
        #   放在抽屉之后：抽屉是速讲现场的 action，它的键路由必须先装上；
        #   three 是 module（defer 语义），本来就排在最后跑。
        + LAB_PRELUDE
        + '<script type="module">\nconst K=' + info_k() + ';\n' + INFO_MODULE_BODY + '</script>\n'
        + "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")

    # ── 构建期断言（别等到 qa）──────────────────────────────────────────────
    assert total == 8, "页数漂移：%d != 8" % total
    assert doc.count("<section") == 8, "section 数漂移：%d" % doc.count("<section")
    assert 'name="robots" content="noindex' in doc, "缺 noindex"
    boards = {i: b for i, (b, _s, _y, _h, _l) in enumerate(PAGES, 1)}
    assert {i for i, b in boards.items() if b == "title"} == {1}, \
        "title 板页漂移：%r" % sorted(i for i, b in boards.items() if b == "title")
    steps_map = {i: s for i, (_b, s, _y, _h, _l) in enumerate(PAGES, 1) if s}
    # v3 波A/波B：P2–P7 每页一枚**细节层**（该页的 data-step=1）⇒ 六页分步
    assert steps_map == {2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, "分步页漂移：%r" % steps_map
    # 细节层：每页至多一枚，且必须挂在 data-step="1" 上（P2–P7 六枚）
    assert doc.count('class="sh flow rev detail"') == len(DETAIL_PAGES), \
        "细节层面板数漂移：%d != %d" % (doc.count('class="sh flow rev detail"'), len(DETAIL_PAGES))
    assert doc.count('chip chip-expand chip-detail') == len(DETAIL_PAGES), \
        "细节层入口 chip 数漂移"
    # 常显容器不许挂 data-step（引擎 P20 空页事故根因：裸容器兜底规则会把它摁成白页）
    assert 'class="sh vid"' not in doc, "本 deck 无视频页"
    # ── 红线 / 口径断言一律走**页上可见文本**，不走整份产物 ─────────────────
    #   LAB 层把一大批几何常量（逗号分隔的数组）烘进了 <script>，
    #   「8,500」这种串会在数字数组里偶然出现 —— 那不是页上的价格，是坐标。
    #   红线管的本来就是「客户看得见的字」，所以判据落在 section 的文本上
    #   （与 qa 的 ⑭ 闸读 deckStage.textContent 是同一把尺）。
    import re as _re
    _VIS = _re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", " ",
                   "".join(_re.findall(r"<section class=\"slide.*?</section>", doc, _re.S))))
    for _bad in ("8,500", "2,999", "5,501", "staging", "盲测", "32,000"):
        assert _bad not in _VIS, "红线：8 页可见文本不许出现「%s」" % _bad
    # 正向口径断言：本 deck 自己的两个数据集锚点必须在
    for _must in ("96.5%", "2,475", "近一半", "No.1", "900亿+", "100万+", "50+"):
        assert _must in _VIS, "口径丢失：「%s」" % _must
    # 深链契约：三处入口的 hash 表必须齐
    for _h in ('data-eng-hash="1"', 'data-eng-hash="16"', 'data-eng-hash="19"'):
        assert _h in doc, "深链入口缺失：%s" % _h
    # SOURCE ledger（采纳项 C）：六页各一行、四段制、结尾一律「事实截止 2026.08」。
    # P1 封面与 P3 矩阵没有事实声明 ⇒ 不带 SOURCE 行（这是规格，不是遗漏）。
    _srcs = _re.findall(r'<div class="sh flow src"[^>]*>(SOURCE[^<]*)</div>', doc)
    assert len(_srcs) == 6, "SOURCE ledger 行数漂移：%d != 6（%r）" % (len(_srcs), _srcs)
    for _s in _srcs:
        assert _s.startswith("SOURCE · "), "SOURCE 行不以「SOURCE · 」起手：%r" % _s
        assert _s.endswith(" · 事实截止 2026.08"), "SOURCE 行未以事实截止收尾：%r" % _s
        assert _s.count(" · ") >= 2, "SOURCE 行不足两段：%r" % _s
    # 双向主题同步（采纳项 A）：宿主必须挂 storage 监听，且只认 colin-theme 这一个键
    assert 'window.addEventListener("storage"' in doc, "缺 iframe→宿主 的 storage 反向同步"
    assert 'e.key!=="colin-theme"' in doc, "storage 监听未限定 colin-theme 键"
    # 96.5% cohort 标注（采纳项 B）：三段口径一个都不许掉
    assert "生产外呼 · n=2,475 · 未出现明确 AI 识别信号" in doc, "P5 96.5% cohort 标注缺失"
    # ═══ LAB 层的构建期自证（六道 · 别等到 qa）═══════════════════════════════
    # ⓐ **与改造前逐字同文**：8 页可见文本的摘要 + data-step 集合逐页钉死。
    #    基线取自 LAB 化之前那一版产物（f04f7b2 的 convoai-info.html）——
    #    LAB 层只做两件事：section 里插一层 .lab-stage（无字）、SVG 里把「形」
    #    裹进 <g class="lab-poster">（无字）⇒ 文本流一个字节都不该动。
    #    改一个字、挪一处 data-step，这一闸当场炸。两种 P1 模式共用同一批摘要
    #    （hero 位图与 poster 都不带字）。
    #    v3 三波：P2/P3/P8（波A）· P4/P5/P6（波B）· P7（波C）全部重排 ⇒ 摘要必然分叉。
    #    这一闸因此收成只钉 **P1 封面** —— 全程一格没动，摘要与 v2（cf3fd73 之后的
    #    LAB 版）逐字节相同，改一个字当场炸。data-step 集合仍是八页全钉。
    _BASE = {1: ("6a266af55cce4643", [])}
    _STEPS = [[], [1], [1], [1], [1], [1], [1], []]
    import hashlib as _hl
    _secs = _re.findall(r'<section class="slide.*?</section>', doc, _re.S)
    assert len(_secs) == 8, "section 切分失败：%d" % len(_secs)
    for _i, _sec in enumerate(_secs):
        _pn = _i + 1
        _t = _re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", " ", _sec)).strip()
        _d = _hl.sha1(_t.encode()).hexdigest()[:16]
        _st = sorted(set(int(x) for x in _re.findall(r'data-step="(\d+)"', _sec)))
        if _pn in _BASE:
            assert _d == _BASE[_pn][0], ("ⓐ P%d 文本与 v2 分叉（%s != %s）—— "
                                         "波 A 不许动这四页" % (_pn, _d, _BASE[_pn][0]))
        assert _st == _STEPS[_i], "ⓐ P%d data-step 集合分叉：%r != %r" % (_pn, _st, _STEPS[_i])
    # ⓑ poster 分件：裹进去的**只有形** —— 一个 <text>、一枚 <polygon> 都不许进
    assert _LP_TRACE, "ⓑ 一个 poster 组都没有 —— _lpsplit 没接上"
    for _q in _LP_TRACE:
        assert "<text" not in _q, "ⓑ poster 组里裹进了文字件（字必须压在 canvas 之上）"
        assert "<polygon" not in _q, "ⓑ poster 组里裹进了箭头头（它是方向标注，留在 DOM）"
    for _pp in LAB_PAGES:
        assert 'class="lab-poster"' in _secs[_pp - 1], "ⓑ P%d 缺 poster 降级层" % _pp
    # P1 声场球 / P2 地球走**构建期离线投影**出来的全屏专用 poster（在舞台里，不在 .pp）；
    # 其余四页的 poster 就是页上那张 SVG 本人（原地留用）。
    for _pp in LAB_PAGES:
        if LAB_RECTS[_pp][0] in ("voice", "globe"):
            continue
        assert '<g class="lab-poster">' in _secs[_pp - 1], \
            "ⓑ P%d 的图形没有原地留作 poster 层" % _pp
    # ⓒ 单渲染器巡游：全文档恰一枚 canvas + 车库在位 + 舞台数与场景表同源
    assert doc.count("<canvas") == 1, "ⓒ WebGL canvas %d 枚 —— 单渲染器巡游只准 1 枚" % doc.count("<canvas")
    assert doc.count('class="lab-garage"') == 1, "ⓒ 缺 canvas 车库"
    assert doc.count('class="lab-stage"') == len(LAB_PAGES), \
        "ⓒ .lab-stage %d 枚 != 场景表 %d 页" % (doc.count('class="lab-stage"'), len(LAB_PAGES))
    for _pp in FLAT_PAGES:
        assert _pp not in LAB_RECTS, "ⓒ P%d 是既定的 2D 页，不该有场景" % _pp
    # ⓓ 净空：构建期解析算路 ≥ 该页的下限（下限 = 它替换掉的那张 2D 图的既有净空）
    for _pp, (_lo, _why) in _CLR.items():
        assert _pp in _CLR_MIN, "ⓓ P%d 没有净空实测" % _pp
        assert _CLR_MIN[_pp] >= _lo - 1e-6, \
            "ⓓ P%d 的 3D 压字：解析净空 %.2fpx < 下限 %.1fpx（%s）" % (_pp, _CLR_MIN[_pp], _lo, _why)
    # ⓓ' P4 的 hot 是抽屉 chip —— 它绝不许被 3D 压（这一条是正面断言，不是顺带）
    _chipclr = _clr_of(_PROBE[4], [_P4_CHIP])
    assert _chipclr >= _P4_CHIP_CLR, \
        "ⓓ' P4 抽屉 chip 被 3D 压到 %.1fpx（下限 %.0f）" % (_chipclr, _P4_CHIP_CLR)
    # ⓔ 流速：A 档 110 ±30%，且任一页内极差 ≤ 1.35×（同页快慢会被读成主次）
    _lo2, _hi2 = _SPD_A * (1 - _SPD_TOL), _SPD_A * (1 + _SPD_TOL)
    for _pp in LAB_PAGES:
        _rows = _spd_rows(_pp)
        for _nm, _L2, _v in _rows:
            assert _lo2 - 1e-6 <= _v <= _hi2 + 1e-6, \
                "ⓔ P%d「%s」%.1fpx/s 越出 A 档 %.0f–%.0f" % (_pp, _nm, _v, _lo2, _hi2)
        if len(_rows) > 1:
            _vs = [r[2] for r in _rows]
            assert max(_vs) / min(_vs) <= 1.35, "ⓔ P%d 页内极差 %.2f×" % (_pp, max(_vs) / min(_vs))
    # ⓕ audioStream 参数表（与旗舰同一份 · 解析包络的两条数学前提）
    assert abs(sum(_LAB._AS_A) - 1.0) < 1e-9, "ⓕ 谐波权重和 != 1 —— 包络会出现尖角"
    for _i2 in range(4):
        for _j2 in range(_i2 + 1, 4):
            _r2v = _LAB._AS_F[_j2] / _LAB._AS_F[_i2]
            assert abs(_r2v - round(_r2v)) > 1e-3, "ⓕ 谐波频率整除 —— 包络会逐拍重复"
    # ⓗ 借来的两枚场景 · 旗舰自己的两条正面断言，原样照抄 ─────────────────────
    #   ① P4 舞台起点必须在三行说明最右墨迹 + 16px 之外（旗舰「病名 B」的机器面）；
    #   ② 两条声带在这条跑道上交叉恰 2 次（yA=yB ⇔ θ = π/2 − phase/2 + kπ）。
    _p4r = max(b[0] + b[2] for b in _LAB._P4INK)
    assert LAB_RECTS[4][1] + _LAB._D_X0 >= _p4r + 16.0, \
        "ⓗ P4 舞台起点 %d 没有让开三行说明的最右墨迹 %d + 16" % (
            LAB_RECTS[4][1] + _LAB._D_X0, _p4r)
    _cross = [_k2 for _k2 in range(9)
              if 0 <= math.pi / 2 - _LAB._D_PHASE / 2 + _k2 * math.pi
              <= 2 * math.pi * _LAB._D_TURNS]
    assert len(_cross) == 2, "ⓗ P4 两条声带交叉 %d 次（要两次）" % len(_cross)
    # ⓖ P8 接力的相位账：off_k + Lw_k − k·λ/3 必须恰好归零（不瞬移 / 不叠影）
    for _k2, _o2 in enumerate(_RV["off"]):
        _res = _o2 + _RV["tlen"][_k2] - _k2 * _RV_LAM / 3.0
        assert abs(_res) < 1e-6, "ⓖ P8 支流%d 的接力相位没对齐（余 %.6f）" % (_k2 + 1, _res)
    print("convoai-info.html · %d 页 · %dKB · conf-light 默认 · 分步 %r · hero-art=%s"
          % (total, len(doc) // 1024, steps_map, "on" if HERO_ART else "off"))


if __name__ == "__main__":
    build()
