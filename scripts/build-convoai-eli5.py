#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-eli5.py ·《声网 · 对话式 AI · 讲给五岁的你》11 页
# CONF 家族 · conf-light 默认 · 单文件双主题 —— 以 build-convoai-engine.py 为母版克隆
#   （同一套 DECK_CSS token / conf-light·dark 背景板 / 共享 deck.js / noindex /
#     五个运动原语 keyframes **逐字复用**）。单产物，无 twin 别名。
#
# 2026-08-24 立项（Colin 拿来社区 skill /eli5）：
#   /eli5 的方法论只有一句 ——「讲给完全不懂的人：大图、少字」。
#   把它 × colin-deck 家族语言，做成引擎 deck（22 页深入讲解版）的 ELI5 版本。
#   口吻已拍板：**大人也爱看的五岁版** —— 科普大白话 + 生活类比，
#   客户高管和朋友圈都能秒懂转发；不是幼儿童话腔，也不是简版产品手册。
#
# ── 本 deck 的灵魂 · ELI5 纪律（硬闸，qa-convoai-eli5.mjs 逐页断言）─────────
#   ① 每页 = 一句人话大标题 + 一张大图（带动效）+ 至多一行小注。
#   ② 大图占版面 ≥ 60%：全 deck 统一 1680×744 的图盒 = 1,249,920px²
#      = 1920×1080 舞台的 60.28%。十一页一个尺寸、一个位置 —— 翻页时图框不跳，
#      这本身就是 ELI5 的节奏（每一页都在同一块黑板上画）。
#   ③ 每页可见正文（.kk 眉标 / .hh 标题 / .sig 页码 / .src SOURCE 行之外）
#      ≤ 40 个汉字。图里的标签也算 —— 这条闸逼着图自己把话说完。
#   ④ 图必须扛住「把字全遮住还能看懂」：形状、位置、方向本身就是论证。
#      （这一条机器验不了，是画图时的自律；每页图注里写了它靠什么形状说话。）
#
# ── 数字纪律（第二条硬红线）────────────────────────────────────────────────
#   · 只许用既有 canon 数字：650ms / 340ms / 95% / 200+ 节点。**禁止新造任何数字**。
#   · 人话大字 + **原数小标**并存，同屏出现：大字「不到一秒」、小标「650ms · 端到端」。
#     人话翻译永不顶替事实 —— 转发的人看大字，较真的人看小标，两边都不骗。
#   · 允许的安全换算只有一类：单位改写与百分比读法
#     （650ms → 不到一秒 / 340ms → 不到半秒 / 95% → 十句挡九句半、九成半 /
#      200+ → 两百多个）。
#   · **禁止**「眨眼 X 次」「比 X 快 Y 倍」这类无法核实的类比量词 —— 那是新造数字。
#   · P6 的「1 秒」尺子是**单位刻度**不是指标：尺子全长 200px = 1 秒，
#     缝隙填色 130px = 650ms，比例是真的。改尺子长度必须同步改填色长度。
#
# ── 红线反向闸（照搬引擎 QA 的名单，构建期就拦）──────────────────────────────
#   价格（¥8,500 / ¥2,999 / ¥5,501）· staging URL · 盲测 · 32,000 —— 全不入。
#   **客户名一个不进**：这是科普 deck，不上案例（引擎 deck 的收束轮已经判过这条例）。
#   **Call Agent 不进**：本 deck 只讲引擎故事，外呼智能体是另一条产品线的活儿。
#   **a[href] = 0**：转发场景里 deck 是一张图，不是一个网站。
#   「大人版」指路走纯文本「colinyao.com/convoai」，读者自己敲 —— 不挂链。
#
# ── 家族基建继承清单（与引擎 deck 逐条对齐，改这份先对表）─────────────────
#   · DECK_CSS 五运动原语（moFlow / moPulse / moBreathe / moHalo + 六个类）逐字复用
#   · 双主题（**浅色默认** —— 本 deck 是转发场景，链接一打开就得是亮的）
#   · deckSwap 主题键常显 chip（.62 → hover 1）
#   · noindex / nofollow
#   · 共享 deck.js（scripts/assets/convoai-src/deck.js）—— 一个字节不改
#   · .slide:not(.active) animation-play-state:paused
#   · reduced-motion / print 全关（装饰件 display:none、真几何件 animation:none）
#   · **常显容器不挂 data-step**：本 deck 全 11 页 steps=0，页内零 [data-step]
#     —— 引擎 P19「多出一个空页面」的根因就是把 data-step 挂回了常显 .sh，
#     这里从源头上不给它机会。
#
# 结构（11 页 · ★ = 带 canon 原数小标）：
#   P1  封面（title 板）               P2  轮流说 vs 同时说（对讲机 / 打电话）
#   P3  它怎么知道你说完了（VAD）      P4  你一开口它就闭嘴 ★340ms
#   P5  吵闹里只听你 ★95%             P6  快到像接话 ★650ms
#   P7  网断了它还在说（AI QoS）       P8  它还长了眼睛（视觉 + 数字人）
#   P9  它住进了玩具里（R1 实拍）      P10 全世界修好的路 ★200+
#   P11 收尾（title 板 · 与深入讲解版封面同句「对话即交互」= 家族闭环）
#
# ── 踩过的坑（与母版同一份，移植 SVG 必守）─────────────────────────────────
#   · svg 一律 style="width:100%;height:auto"，.sh 高度 = width×viewBoxH/viewBoxW
#   · SVG 里换色一律写内联 style="fill:…"，呈现属性 fill= 压不过 .fig 的 CSS fill
#   · 虚线不能走 .dw（motion.css 的 stroke-dasharray:var(--len) 会把破折压掉），走 .pop
#   · .pp .sh{overflow:visible}：要裁切写 .pp .sh.CLASS{overflow:hidden}（P9 实拍卡）
#   · <img> 必须 width/height 100% + object-fit —— 放大逼近墨迹会让 rect 冲出 .sh 盒，
#     occlusion-scan 的 TEXT-x-SPILL 只读 rect、不读 overflow:hidden ⇒ 稳报假命中
#   · .mo-cycle / .mo-drift 的 --mo-off **必须是 dasharray 周期的整数倍**，
#     否则 100% 帧 ≠ 0% 帧，pinned-diff SELFPIN 当场报差异（cyc() 帮你算）
#   · .mo-pulse 的载体自带 opacity 时必须把 --mo-hi 设成那个值，
#     否则动画会把它顶成 1（animation 压过 inline style）
# ═══════════════════════════════════════════════════════════════════════════
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
OUT = ROOT / "public" / "decks" / "convoai-eli5.html"
B = "/decks/assets/conf-boards/"
R26 = "/decks/assets/robot26/"

def css(name):
    return (SRC / name).read_text(encoding="utf-8")

FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>"""

# ── 背景板（两张：title 给 P1/P11，content 给其余）──────────────────────────
#   content 板的 opacity 从引擎的 .42 降到 .22：本 deck 每页压着一张 1680×744 的大图，
#   矩阵纹理留在 .42 会从图的空隙里透上来跟图抢注意力。ELI5 的规矩是「图说话」，
#   底纹退到只剩「这是同一个家族」的暗示就够了。
#   ⚠ 板子自带一条 accent 细线在页坐标 y848–852（x120–761）——换算到图 viewBox 是
#     y602–606 / x0–641。引擎 deck 用 rule(850) 把它压成收口线；本 deck 的图占满整页，
#     压不了也躲不开，纪律改成 **那一带不放文字**（大字被它划一道就成了「被划掉」的观感）。
#     每张图的排版都按这条让过：P3 判定标移到波形上方 / P5 数字块移到左上 /
#     P6 尺子落在 626 以下 / P7 说话带落在 610 以下 / P8 标签落在 628 以下。
BOARDS_CSS = """<style id="eli5-boards">
.conf-bg{position:absolute;inset:0;z-index:0;pointer-events:none;background-repeat:no-repeat;
  background-position:center;background-size:cover;opacity:var(--conf-bg-opacity,.58);}
.slide.conf-boarded{background:transparent!important;}
.slide.conf-boarded>.pp{z-index:1;}
.conf-bg-title{--conf-bg-opacity:.60;background-image:url('%(B)stitle-02-orbit-light.png');}
.conf-bg-content{--conf-bg-opacity:.22;background-image:url('%(B)scontent-01-matrix-light.png');}
html[data-theme="dark"] .conf-bg-title{background-image:url('%(B)stitle-02-orbit-dark.png');}
html[data-theme="dark"] .conf-bg-content{background-image:url('%(B)scontent-01-matrix-dark.png');}
html[data-theme="dark"] .conf-bg{filter:saturate(.92);}
</style>""" % {"B": B}

# ── 本 deck 专属 CSS ────────────────────────────────────────────────────────
DECK_CSS = """<style id="convoai-eli5-deck">
/* 绝对画布 shape 层（robot26 惯例） */
.pp{position:absolute;inset:0;}
.pp .sh{position:absolute;overflow:visible;}
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 15px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--sig-ink);}
/* 版式件（与引擎 / info 同源，只有 .hh 加大） */
.kk{font:700 20px/1 var(--f-mono);letter-spacing:.24em;color:var(--accent);}
/* ELI5 的标题比家族默认（68px）大一档：这一句人话是整页的主角，
   图是它的证据。76×1.12 = 85.1px 行盒，落在 96 高的 .sh 里还余 11。
   十一句标题全部单行 —— 最长的 P2 十四个字 ×76 = 1064 < 1680，不会折行。 */
.hh{font:700 76px/1.12 var(--f-cn);letter-spacing:-.025em;color:var(--ink);}
.hh strong{color:var(--accent);}
.sub{font:400 27px/1.55 var(--f-cn);color:var(--ink-2);}
.mono-sm{font:500 15px/1.4 var(--f-mono);letter-spacing:.08em;color:var(--ink-3);}
/* 一行小注：走家族 .note（3px accent 左框 · 22px · ink-2），比 .land 收敛一档 ——
   ELI5 页上真正大声说话的是标题和图，小注只是补一句「所以呢」。 */
.note{font-size:23px;}
/* 移植 inspire26/dual26 版式：解掉 stage.css 的 svg{max-width/height:100%} */
.fig svg{max-width:none;max-height:none;}
.fig{align-items:flex-start;}
.on-dark b,.on-dark strong{color:inherit;}
/* ══ deck 级运动语言 · 五个运动原语（自 build-convoai-engine.py **逐字复用**）════
   原语与语义一一对应，本 deck 与引擎 deck 共用同一张对照表：
     ① .mo-packet  能量包 —— 宽 stroke 低透明 dash 段沿路径漂移，只挂主数据流，
        方向与箭头一致。纯装饰件 ⇒ 静态语域 display:none。
     ② .mo-drift   虚线漂移 —— 事件 / 控制 / 参考线的 dash 慢爬，比包慢一档。
     ③ .mo-pulse   脉冲 —— 命中 / 事件标 / 波形条明暗，错峰 delay。
        --mo-hi 必须等于载体的静态 opacity，否则动画把它顶成 1。
     ④ .mo-breathe hot 件呼吸（scale ≤1.03），每页至多一处；伴件 .mo-halo 向外扩散。
     ⑤ .mo-cycle   闭环绕行 —— 环 / 回路上的 dash 永续绕圈。
   纪律（硬红线，四条，与引擎 deck 同一份）：
     · 每条 keyframes 的 100% 帧 = 静态原图（dash 位移走完整周期 / scale 回 1 /
       opacity 回静态值 / halo 回 0）—— 自证工具 scripts/pinned-diff.mjs SELFPIN。
     · 动效元素不携带文字。
     · prefers-reduced-motion 与 print 全关。
     · 非当前页一律 animation-play-state:paused。
   ⚠ P5 的两道防御环 **不做 transform 旋转**，只让 dash 爬（引擎 P10 的页级硬约束）：
     环左侧的缺口就是「只有目标人声进得来」这句话的图形依据，几何一转缺口就甩走了。*/
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
/* ── P9 · R1 实拍卡（跨 deck 引用 robot26 的 1000×750 原片）───────────────
   图窗定死 992×744 —— 992/1000 = 744/750 = .992，cover 由宽高**同时**定标，
   整张 4:3 原片一格不裁地落进窗里（引擎 P19 的「图片展示不全」踩过一次，
   那次是窗口比例与原片不符、cover 由单边定标切掉了板底排线）。
   **改窗宽必须同步改窗高，比例锁死 4:3。**
   左栏 688 = 1680 − 992，放「它 → 住进去」的记号图。 */
.pp .sh.eli-card{overflow:hidden;}
/* 卡底走 --card-bg-2（**不透明**）而不是 --card-bg（72% 透明）：
   背景板那条 accent 细线正好从卡的下半身横穿过去，半透明卡压不住它，
   看上去就是「卡里多了一条不知道哪来的线」。 */
.eli-card{display:flex;flex-direction:row;background:var(--card-bg-2);
  border:1px solid var(--hair);border-radius:24px;}
.eli-side{flex:none;width:688px;align-self:stretch;display:flex;align-items:center;}
.eli-side .fig{width:100%;}
.eli-shot{position:relative;flex:none;width:992px;align-self:stretch;overflow:hidden;
  background:#0a0c14;border-left:1px solid var(--hair);border-radius:0 23px 23px 0;}
.eli-shot img{width:100%;height:100%;display:block;object-fit:cover;object-position:center;}
/* 浅色主题下的「暗媒体卡」惯例：深底实拍直接压在浅版面上会掉进洞里，
   给一圈发丝内描边把图从纸面上拎起来（实拍不翻色，只压一档饱和度免得抢主色）。 */
html:not([data-theme="dark"]) .eli-shot{box-shadow:inset 0 0 0 1px rgba(17,17,17,.12);}
html:not([data-theme="dark"]) .eli-shot img{filter:saturate(.92) contrast(1.03);}
@media print{.eli-shot{box-shadow:none;}}
/* SOURCE 行（口径出处）—— 与小注同一条基线的右半区，走 40 字闸的豁免类 .src */
.src{text-align:right;}
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

# ── 版式栅格（十一页共用，改一个数就得重算整列）─────────────────────────────
#   kicker  y92  h28   → 120
#   标题     y138 h96   → 234        （封面 / 收尾页 y132，下面留副题）
#   大图     y246 h744  → 990        1680×744 = 舞台的 60.28%（ELI5 纪律 ②）
#   小注     y1002 h48  → 1050       28px 底边距
FX, FY, FW, FH = 120, 246, 1680, 744      # 图盒（页坐标）
VBW, VBH = 1680, 744                       # 图 viewBox = 图盒像素，1:1，坐标不用换算

AC = "var(--accent)"
AD = "var(--accent-deep)"
HS = "var(--hair-strong)"
I3 = "var(--ink-3)"
INK = "var(--ink)"

# ── 组装件（与母版同签名）────────────────────────────────────────────────────
def sh(cls, style, body):
    return '<div class="sh %s" style="%s">%s</div>' % (cls, style, body)

def head(kicker, title, ty=138):
    return (sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", kicker)
            + sh("ink hh", "left:120px;top:%dpx;width:1680px;height:96px" % ty, title))

def sub(txt, y=234):
    return sh("flow", "left:120px;top:%dpx;width:1500px;height:46px;--i:3" % y,
              '<div class="sub">%s</div>' % txt)

def bigfig(inner, y=FY, i=1):
    """全 deck 唯一的图盒：1680×744，位置与尺寸十一页不变（ELI5 纪律 ②）。"""
    return sh("spread eli-fig", "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (FX, y, FW, FH, i),
              '<div class="fig"><svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg></div>'
              % (VBW, VBH, inner))

def note(txt, w=1000, i=6):
    return sh("flow", "left:120px;top:1002px;width:%dpx;height:48px;--i:%d" % (w, i),
              '<div class="note">%s</div>' % txt)

SRC_LINE = "SOURCE · 声网官网 · 引擎发版说明 公开口径 · 事实截止 2026.08"
def source(txt=SRC_LINE, i=7):
    """口径出处：与小注同一条基线的右半区（引擎 P11 / P19 同款两栏页脚）。
       .src 是 40 字闸的豁免类 —— 出处不是正文，不占 ELI5 的字数预算。"""
    return sh("flow mono-sm src", "left:1140px;top:1016px;width:660px;height:24px;--i:%d" % i, txt)

# ── SVG 小件 ────────────────────────────────────────────────────────────────
def ah_r(x, y, col, s=10):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x - s - 2, y - 7, x - s - 2, y + 7)
def ah_l(x, y, col, s=10):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x + s + 2, y - 7, x + s + 2, y + 7)
def ah_d(x, y, col, s=10):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x - 7, y - s - 2, x + 7, y - s - 2)
def ah_u(x, y, col, s=10):
    return '<polygon class="pop" style="--i:2;fill:%s" points="%d,%d %d,%d %d,%d"/>' % (
        col, x, y, x - 7, y + s + 2, x + 7, y + s + 2)

def hline(x1, x2, y, col=HS, w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d H%d" stroke="%s" '
            'stroke-width="%s" fill="none"/>' % (abs(x2 - x1), i, x1, y, x2, col, w))
def vline(x, y1, y2, col=HS, w=2, i=1):
    return ('<path class="dw" style="--len:%d;--i:%d" d="M%d %d V%d" stroke="%s" '
            'stroke-width="%s" fill="none"/>' % (abs(y2 - y1), i, x, y1, y2, col, w))

def dline(d, col=HS, w=2, i=1, dash="7 7", cls="", sty=""):
    """虚线：不能走 .dw（motion.css 的 stroke-dasharray:var(--len) 会把破折整条压掉，
       虚线会渲染成实线）。挂 .pop（只动 opacity/transform），破折保留。"""
    return ('<path class="pop%s" style="--i:%d%s" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-dasharray="%s"/>'
            % ((" " + cls) if cls else "", i, (";" + sty) if sty else "", d, col, w, dash))

def txt(x, y, s, cls="txt", size=None, anchor=None, col=None, weight=None, i=None,
        mono=False, ls=None):
    st = []
    if size:   st.append("font-size:%dpx" % size)
    if col:    st.append("fill:%s" % col)
    if weight: st.append("font-weight:%d" % weight)
    if mono:   st.append("font-family:var(--f-mono)")
    if ls is not None: st.append("letter-spacing:%s" % ls)
    if i is not None:  st.append("--i:%d" % i)
    a = ' text-anchor="%s"' % anchor if anchor else ""
    return '<text class="%s" x="%d" y="%d"%s%s>%s</text>' % (
        cls, x, y, a, (' style="%s"' % ";".join(st)) if st else "", s)

def box(x, y, w, h, r=4, hot=False, dashed=False, i=0, cls="", sty=""):
    d = ' stroke-dasharray="8 7"' if dashed else ""
    c = (" " + cls) if cls else ""
    v = (";" + sty) if sty else ""
    if hot:
        return ('<rect class="pop%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
                'fill="none" stroke="%s" stroke-width="3"%s/>' % (c, i, v, x, y, w, h, r, AC, d))
    return ('<rect class="pop box%s" style="--i:%d%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'stroke-width="1.6"%s/>' % (c, i, v, x, y, w, h, r, d))

# ── 运动原语 ① 能量包 ───────────────────────────────────────────────────────
#   压在实线之下的一段粗软 stroke，沿路径漂移。dasharray =「包长 seg + 间隔 ln」，
#   --mo-off 走完一个整周期 ⇒ 100% 帧与 0% 帧逐像素相同。
#   ln 传路径长度：ln = L ⇒ 路上永远有一枚包（连续流）；
#                  ln = 2L ⇒ 包只在半个周期里出现在路上（**相位互斥**用，见 P2 左栏）。
def packet(d, ln, col=None, w=13, seg=26, dur="1.8s", op=".32", i=2, rev=False, delay=None, cap="round"):
    per = seg + int(ln)
    v = "--mo-off:%d;--mo-dur:%s" % (per if rev else -per, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<path class="pop mo-packet" style="--i:%d;%s" d="%s" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-opacity="%s" stroke-linecap="%s" stroke-dasharray="%d %d"/>'
            % (i, v, d, col or AC, w, op, cap, seg, int(ln)))

def drift(d, col=HS, w=2, dash=(8, 7), dur="3.4s", i=2, rev=False, delay=None, k=None, ln=None):
    """运动原语 ② 虚线漂移。--mo-off 必须是 dash 周期的整数倍 ⇒ 100% 帧 = 0% 帧。
       k 直给周期数；不给就按 ln（路径长度）算一个最接近的整数。"""
    per = dash[0] + dash[1]
    if k is None:
        k = max(1, round((ln or per * 12) / per))
    off = per * k * (1 if rev else -1)
    sty = "--mo-off:%d;--mo-dur:%s" % (off, dur)
    if delay: sty += ";--mo-del:%s" % delay
    return dline(d, col, w, i, dash="%d %d" % dash, cls="mo-drift", sty=sty)

def cyc(d, perim, col=None, w=2.4, dash=(9, 8), dur="22s", i=2, rev=False, delay=None):
    """运动原语 ⑤ 闭环绕行：dash 沿环爬，**不做 transform 旋转**。
       周期数 k = round(周长 / dash 周期)，offset = 周期 × k ⇒ 100% 帧 = 0% 帧。"""
    per = dash[0] + dash[1]
    k = max(1, round(perim / per))
    off = per * k * (1 if rev else -1)
    sty = "--mo-off:%d;--mo-dur:%s" % (off, dur)
    if delay: sty += ";--mo-del:%s" % delay
    return dline(d, col or HS, w, i, dash="%d %d" % dash, cls="mo-cycle", sty=sty)

def halo_c(cx, cy, r, col=None, sc="1.5", op=".34", dur="3.6s", delay=None):
    v = "--mo-sc:%s;--mo-op:%s;--mo-dur:%s" % (sc, op, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<circle class="mo-halo" style="%s" cx="%d" cy="%d" r="%d" fill="none" '
            'stroke="%s" stroke-width="3" opacity="0"/>' % (v, cx, cy, r, col or AC))

def halo_rect(x, y, w, h, r=8, col=None, sc="1.28", op=".34", dur="3.6s", delay=None):
    v = "--mo-sc:%s;--mo-op:%s;--mo-dur:%s" % (sc, op, dur)
    if delay: v += ";--mo-del:%s" % delay
    return ('<rect class="mo-halo" style="%s" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'fill="none" stroke="%s" stroke-width="3" opacity="0"/>' % (v, x, y, w, h, r, col or AC))

# ── 波形条（全 deck 的「声音」通用件）────────────────────────────────────────
#   高度表写死（禁止 random / Date —— 两次构建必须逐字节一致）。
#   groups > 0：条按组分批各挂一枚 <g class="mo-pulse">、错峰 delay ⇒ 一段亮度在条上流动。
#   **分组而不是逐条挂**：逐条挂 30 根就把 qa-motion 的 30 件配额一页吃光。
_HA = [46, 88, 30, 110, 64, 38, 96, 56, 76, 32, 84, 44, 68, 26, 102, 50, 72, 34, 92, 60]
_HB = [64, 34, 92, 50, 74, 28, 104, 58, 40, 86, 48, 70, 30, 98, 54, 80, 36, 66, 44, 88]

def bars(x0, n, cy, col, hs=None, gap=24, w=10, seed=0, groups=0, dur=2.6, lo=".40", op=None, sc=1.0):
    hs = hs or _HA
    rs = []
    for k in range(n):
        h = max(8, int(hs[(k + seed) % len(hs)] * sc))
        rs.append('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" style="fill:%s"/>'
                  % (x0 + k * gap, cy - h // 2, w, h, w // 2, col))
    if not groups:
        return '<g class="pop" style="--i:2%s">%s</g>' % ((";opacity:%s" % op) if op else "", "".join(rs))
    out = []
    for g in range(groups):
        body = "".join(rs[k] for k in range(g, n, groups))
        # 载体带 opacity 时 --mo-hi 必须跟着写，否则 moPulse 的 100% 帧把它顶成 1
        oj = (";opacity:%s;--mo-hi:%s" % (op, op)) if op else ""
        out.append('<g class="mo-pulse" style="--mo-dur:%ss;--mo-del:%.2fs;--mo-lo:%s%s">%s</g>'
                   % (dur, g * dur / groups, lo, oj, body))
    return '<g class="pop" style="--i:2">%s</g>' % "".join(out)

# ── 人物 / AI 记号（全 deck 复用同两枚形状：「你」是人，「它」是会说话的方块）──
def person(cx, cy, s=1.0, col=None):
    c = col or INK
    hr = 30 * s
    return ('<circle class="pop" style="--i:2" cx="%d" cy="%d" r="%d" fill="none" stroke="%s" '
            'stroke-width="%.1f"/>' % (cx, cy - 46 * s, hr, c, 3.4 * s)
            + '<path class="pop" style="--i:2" d="M%d %d a%d %d 0 0 1 %d 0" fill="none" '
              'stroke="%s" stroke-width="%.1f"/>'
              % (cx - 52 * s, cy + 46 * s, 52 * s, 52 * s, 104 * s, c, 3.4 * s))

def aimark(cx, cy, s=1.0, hot=True):
    """「它」：圆角方块 + 里面三根短波 —— 一个会说话的小机器。"""
    w = 92 * s
    o = ['<rect class="pop" style="--i:2" x="%d" y="%d" width="%d" height="%d" rx="%d" '
         'fill="%s" stroke="%s" stroke-width="%.1f"/>'
         % (cx - w / 2, cy - w / 2, w, w, 24 * s,
            "color-mix(in srgb,var(--accent) 14%,transparent)" if hot else "none", AC, 3.2 * s)]
    for k, h in enumerate((26, 44, 30)):
        o.append('<rect class="pop" style="--i:3;fill:%s" x="%d" y="%d" width="%d" height="%d" rx="%d"/>'
                 % (AC, cx - 20 * s + k * 18 * s, cy - h * s / 2, 9 * s, h * s, 5 * s))
    return "".join(o)

def bubble(x, y, w, h, r, hot=False, tail="bl", i=2):
    """说话气泡：圆角矩形 + 一支尾巴。ELI5 全 deck 的「一句话」就是这个形状。"""
    fill = "color-mix(in srgb,var(--accent) 12%,transparent)" if hot else "var(--card-bg-2)"
    st = AC if hot else HS
    o = ['<rect class="pop" style="--i:%d" x="%d" y="%d" width="%d" height="%d" rx="%d" '
         'fill="%s" stroke="%s" stroke-width="2.6"/>' % (i, x, y, w, h, r, fill, st)]
    if tail == "bl":
        o.append('<path class="pop" style="--i:%d" d="M%d %d L%d %d L%d %d Z" fill="%s" stroke="%s" '
                 'stroke-width="2.6" stroke-linejoin="round"/>'
                 % (i, x + 70, y + h - 2, x + 34, y + h + 62, x + 152, y + h - 2, fill, st))
    elif tail == "br":
        o.append('<path class="pop" style="--i:%d" d="M%d %d L%d %d L%d %d Z" fill="%s" stroke="%s" '
                 'stroke-width="2.6" stroke-linejoin="round"/>'
                 % (i, x + w - 70, y + h - 2, x + w - 34, y + h + 62, x + w - 152, y + h - 2, fill, st))
    return "".join(o)

def snd(cx, cy, n=3, r0=22, gap=17, col=None, w=3.4, i=3, cls="", sty=""):
    """声音记号：n 道向右张开的弧（噪声源 / 数字人的嘴都用它）。"""
    o = []
    for k in range(n):
        r = r0 + k * gap
        o.append('<path class="pop%s" style="--i:%d%s" d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f" '
                 'fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
                 % ((" " + cls) if cls else "", i, (";" + sty) if sty else "",
                    cx + r * 0.5, cy - r * 0.866, r, r, cx + r * 0.5, cy + r * 0.866,
                    col or I3, w))
    return "".join(o)

def cross(cx, cy, s=17, col=None, w=5):
    """✕ 命中标：画真线，不用字符 ✕（动效元素不许携带文字，字符版会被 qa-motion 拦下）。"""
    c = col or AD
    return ('<path d="M%d %d L%d %d M%d %d L%d %d" stroke="%s" stroke-width="%d" '
            'stroke-linecap="round" fill="none"/>' % (cx - s, cy - s, cx + s, cy + s,
                                                      cx + s, cy - s, cx - s, cy + s, c, w))

def check(cx, cy, s=18, col="var(--card-bg-2)", w=5):
    return ('<path d="M%d %d L%d %d L%d %d" stroke="%s" stroke-width="%d" stroke-linecap="round" '
            'stroke-linejoin="round" fill="none"/>'
            % (cx - s, cy, cx - s // 4, cy + s * 3 // 4, cx + s, cy - s * 3 // 4, col, w))

PAGES = []          # (board, body_html)
def page(board, body):
    PAGES.append((board, body))

def pt(cx, cy, r, deg):
    """极坐标 → 画布坐标（角度按数学正向，y 轴已翻转：0° 在右，90° 在上）。"""
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy - r * math.sin(a))

# ═══ P1 · 封面（title 板）══════════════════════════════════════════════════
#   图靠什么说话：两只说话气泡，左边是人的、右边是它的，中间两条道**同时**在跑包
#   —— 一上来就把「会聊天」画成「两边同时有来有回」，为 P2 的第一记重拳埋雷管。
#   零标签：把字全遮住，两只气泡 + 双向流动本身就是「对话」。
def _p1():
    up = "M750 290 C810 290 870 340 930 340"
    dn = "M930 500 C870 500 810 450 750 450"
    return "".join([
        bubble(90, 120, 660, 340, 60, hot=False, tail="bl", i=1),
        bars(150, 11, 290, I3, _HA, gap=48, w=18, groups=3, dur=2.8, lo=".38"),
        bubble(930, 250, 660, 340, 60, hot=True, tail="br", i=2),
        bars(990, 11, 420, AC, _HB, gap=48, w=18, seed=3, groups=3, dur=2.8, lo=".42"),
        halo_rect(930, 250, 660, 340, 60, dur="5.2s"),
        '<path class="dw" style="--len:200;--i:3" d="%s" stroke="%s" stroke-width="3" fill="none"/>' % (up, HS),
        packet(up, 200, col=AC, dur="2.2s"), ah_r(932, 340, AC),
        '<path class="dw" style="--len:200;--i:3" d="%s" stroke="%s" stroke-width="3" fill="none"/>' % (dn, HS),
        packet(dn, 200, col=AC, dur="2.2s", delay="-1.1s"), ah_l(748, 450, AC),
    ])
page("title", "".join([
    head("AGORA · CONVOAI · ELI5 · 讲给五岁的你",
         "讲给五岁的你：<strong>会聊天的 AI</strong>。", ty=132),
    sub("不用懂技术。看完这 11 页，你就懂了。"),
    bigfig(_p1(), y=288),
]))

# ═══ P2 · 轮流说 vs 同时说 ·「全 deck 的第一记重拳」═══════════════════════
#   语义直接复用引擎 P3 的双工三模式，只留最能打的两极、图放大、字减到四个词。
#   图靠什么说话：左右两块板，上面各摆一件人人认得的东西（对讲机 / 电话听筒），
#   下面是同一套「谁在什么时候说」的时间条 ——
#     左：两条块**错开**（时间上不重叠）+ 一道切换闸 + 一个被挡住的 ✕
#     右：两条块**重叠**（同一段时间两边都在说）+ 重叠区高亮 + 一支插话的快箭头
#   动效是这一页的论证本身（**相位互斥 vs 同时**）：
#     左栏两条道的包用 ln = 2L 的 dasharray ⇒ 包只在半个周期出现在道上，
#     再给下面那条 −½ 周期的负 delay ⇒ 两条道**轮流**有包，永不同时。
#     右栏两条道用 ln = L ⇒ 两条道永远同时有包。
#   把字全遮住：错开 vs 重叠、挡住 vs 插进去 —— 图自己说得完。
def _p2_walkie(cx, top):
    o = [box(cx - 62, top + 44, 124, 196, r=18, i=1),
         '<path class="dw" style="--len:70;--i:2" d="M%d %d L%d %d" stroke="%s" stroke-width="6" '
         'fill="none" stroke-linecap="round"/>' % (cx + 40, top + 44, cx + 60, top - 18, HS),
         '<circle class="pop" style="--i:2;fill:%s" cx="%d" cy="%d" r="8"/>' % (HS, cx + 60, top - 24)]
    for k in range(3):
        o.append(hline(cx - 36, cx + 36, top + 78 + k * 18, HS, 4, 2))
    o.append('<rect class="pop" style="--i:3;fill:%s" x="%d" y="%d" width="30" height="40" rx="9"/>'
             % (AC, cx - 15, top + 148))
    return "".join(o)

def _p2_phone(cx, cy):
    """经典听筒：一条粗弧 + 两端听筒/话筒圆头。"""
    return ('<path class="pop" style="--i:1" d="M%d %d Q%d %d %d %d" fill="none" stroke="%s" '
            'stroke-width="30" stroke-linecap="round"/>' % (cx - 92, cy + 34, cx, cy - 108, cx + 92, cy + 34, HS)
            + '<circle class="pop" style="--i:2;fill:%s" cx="%d" cy="%d" r="30"/>' % (HS, cx - 92, cy + 34)
            + '<circle class="pop" style="--i:2;fill:%s" cx="%d" cy="%d" r="30"/>' % (HS, cx + 92, cy + 34)
            + '<circle class="pop" style="--i:3;fill:%s" cx="%d" cy="%d" r="13"/>' % (AC, cx - 92, cy + 34)
            + '<circle class="pop" style="--i:3;fill:%s" cx="%d" cy="%d" r="13"/>' % (AC, cx + 92, cy + 34))

def _p2_panel(px, kind):
    L1, L2 = 470, 610                     # 两条时间道
    o = [box(px, 0, 790, 744, r=28, i=1)]
    cx = px + 395
    if kind == "half":
        o.append(_p2_walkie(cx, 60))
        o += [txt(cx, 322, "对讲机", "ttl", size=42, anchor="middle", col=INK, i=3),
              txt(cx, 362, "HALF-DUPLEX", "lbl", size=15, anchor="middle", i=3)]
    else:
        o.append(_p2_phone(cx, 168))
        o += [txt(cx, 322, "打电话", "ttl", size=42, anchor="middle", col=AC, i=3),
              txt(cx, 362, "FULL-DUPLEX", "lbl", size=15, anchor="middle", col=AC, i=3)]
    # 两条道的底轨 + 谁是谁
    for cy in (L1, L2):
        o.append(dline("M%d %d H%d" % (px + 78, cy, px + 716), HS, 1.6, 4, dash="5 8"))
    o += [txt(px + 44, L1 + 9, "你", "ttl", size=26, anchor="middle", col=INK, i=4),
          txt(px + 44, L2 + 9, "它", "ttl", size=26, anchor="middle", col=AC, i=4)]
    if kind == "half":
        a0, a1, b0, b1 = px + 94, px + 364, px + 424, px + 704
        o += [  # 你说（块 1）／ 它说（块 2）：x 上完全错开 = 时间上轮流
            '<rect class="pop" style="--i:5;fill:%s;opacity:.80" x="%d" y="%d" width="%d" height="58" rx="12"/>'
            % (INK, a0, L1 - 29, a1 - a0),
            '<rect class="pop" style="--i:6;fill:%s" x="%d" y="%d" width="%d" height="58" rx="12"/>'
            % (AC, b0, L2 - 29, b1 - b0),
            # 它说话的那段时间，你想说的话只剩一只空壳 —— ✕ 才有东西可否定
            '<rect class="pop" style="--i:6" x="%d" y="%d" width="%d" height="58" rx="12" fill="none" '
            'stroke="%s" stroke-width="2" stroke-dasharray="8 7"/>' % (b0, L1 - 29, b1 - b0, HS),
            # 切换闸：轮次之间必须先让线，才轮到对方
            dline("M%d 424 V656" % (px + 394), HS, 2.6, 6, dash="7 7"),
            # 它说话的中途你想插话 —— 被闸挡住（✕ 是画的线，不是字符）
            '<g class="mo-pulse" style="--mo-dur:2.2s;--mo-lo:.22">%s</g>' % cross(px + 564, L1, 21),
            packet("M%d %d H%d" % (a0 + 14, L1, a1 - 14), 2 * (a1 - a0 - 28), col="var(--card-bg-2)",
                   dur="3.4s", op=".55", w=15),
            packet("M%d %d H%d" % (b0 + 14, L2, b1 - 14), 2 * (b1 - b0 - 28), col="var(--card-bg-2)",
                   dur="3.4s", delay="-1.7s", op=".55", w=15),
        ]
    else:
        a0, a1, b0, b1 = px + 94, px + 520, px + 300, px + 704
        mid = (b0 + a1) // 2
        o += [  # 重叠区：同一段时间，两边都在说（220 宽，一眼就看得出「叠上了」）
            '<rect class="pop" style="--i:5;fill:%s;opacity:.16" x="%d" y="424" width="%d" height="232" rx="14"/>'
            % (AD, b0, a1 - b0),
            halo_rect(b0, 424, a1 - b0, 232, 14, col=AD, sc="1.12", op=".28", dur="4.4s"),
            '<rect class="pop" style="--i:5;fill:%s;opacity:.80" x="%d" y="%d" width="%d" height="58" rx="12"/>'
            % (INK, a0, L1 - 29, a1 - a0),
            '<rect class="pop" style="--i:6;fill:%s" x="%d" y="%d" width="%d" height="58" rx="12"/>'
            % (AC, b0, L2 - 29, b1 - b0),
            # 重叠区中间一支双头连杆：这一刻上下两条都在响（不是「谁插谁」，是同时）
            '<path class="dw" style="--len:70;--i:7" d="M%d 508 V572" stroke="%s" stroke-width="6" '
            'fill="none"/>' % (mid, AD),
            ah_u(mid, 502, AD, 8), ah_d(mid, 578, AD, 8),
            packet("M%d %d H%d" % (a0 + 14, L1, a1 - 14), a1 - a0 - 28, col="var(--card-bg-2)",
                   dur="2.6s", op=".55", w=15),
            packet("M%d %d H%d" % (b0 + 14, L2, b1 - 14), b1 - b0 - 28, col="var(--card-bg-2)",
                   dur="2.6s", delay="-.6s", op=".55", w=15),
        ]
    return "".join(o)

page("content", "".join([
    head("TAKE TURNS / BOTH AT ONCE · 轮流说 vs 同时说",
         "对讲机<strong>轮流说</strong>，打电话<strong>同时说</strong>。"),
    bigfig(_p2_panel(0, "half") + _p2_panel(890, "full")),
    note("以前的语音助手是对讲机，它是打电话。"),
]))

# ═══ P3 · 它怎么知道你说完了（VAD 的人话版）═══════════════════════════════
#   图靠什么说话：上面一条你的声音，中间断两次 ——
#     第一次断得短（你在想词）：往下的虚线撞上一个 ✕，它**没有**开口；
#     第二次断得长（你说完了）：往下的粗快路径直通它的声音，它开口了。
#   两次停顿长短不同、两条下行线一条被挡一条通了 —— 字全遮住也读得出来。
#   ⚠ 两段停顿的宽度是本页唯一的论据：短停 90 / 长停 204，**长的必须明显长于短的**。
#     改波形条数必须重算这两段，否则「停一下 vs 说完了」在图上分不出来。
#   判定标（停一下 / 说完了）钉在波形**上方** —— 下方 602–606 是背景板自带 accent 线的
#   走廊（见 BOARDS_CSS 的告警），大字压上去就是「被划掉」。
def _p3():
    UY, DY = 240, 566
    GX1, GX2 = 603, 1218                  # 短停中点 / 长停中点
    fast = "M1218 364 C1218 468 1252 544 1348 556"
    o = [txt(44, UY + 10, "你", "ttl", size=28, anchor="middle", col=INK, i=1),
         txt(44, DY + 10, "它", "ttl", size=28, anchor="middle", col=AC, i=1),
         dline("M90 %d H1620" % UY, HS, 1.4, 1, dash="5 9"),
         dline("M90 %d H1620" % DY, HS, 1.4, 1, dash="5 9"),
         # 你的一句话：说一段（90–558）→ 停 90 → 再说一段（648–1116）→ 停 204 → 说完了
         bars(90, 18, UY, INK, _HA, gap=26, w=11, groups=3, dur=2.4, lo=".34"),
         bars(648, 18, UY, INK, _HB, gap=26, w=11, seed=5, groups=3, dur=2.4, lo=".34"),
         txt(GX1, 148, "停一下", "ttl", size=32, anchor="middle", col=I3, i=5),
         txt(GX2, 148, "说完了", "ttl", size=32, anchor="middle", col=AC, i=5),
         # 停顿一：短。虚线下探，被 ✕ 拦住 —— 它没有抢话
         dline("M%d 176 V300" % GX1, HS, 2.4, 3, dash="8 8"),
         dline("M%d 364 V498" % GX1, HS, 2.4, 3, dash="8 8"),
         '<circle class="pop" style="--i:3;fill:var(--card-bg-2)" cx="%d" cy="330" r="32" stroke="%s" '
         'stroke-width="2.6" stroke-dasharray="6 6"/>' % (GX1, HS),
         txt(GX1, 342, "?", "ttl", size=34, anchor="middle", col=I3, i=4),
         '<g class="mo-pulse" style="--mo-dur:2.4s;--mo-lo:.2">%s</g>' % cross(GX1, 520, 19),
         # 停顿二：长。粗快路径直通它的声音 —— 它开口了
         '<path class="dw" style="--len:130;--i:4" d="M%d 176 V296" stroke="%s" stroke-width="3" '
         'fill="none"/>' % (GX2, AC),
         '<circle class="pop" style="--i:4;fill:%s" cx="%d" cy="330" r="32"/>' % (AC, GX2),
         check(GX2, 330),
         halo_c(GX2, 330, 32, dur="2.8s"),
         '<path class="dw" style="--len:230;--i:5" d="%s" stroke="%s" stroke-width="7" fill="none"/>'
         % (fast, AD),
         packet(fast, 230, col=AD, dur="1.5s", w=15),
         ah_r(1368, 557, AD),
         # 它的回答
         bars(1392, 9, DY, AC, _HB, gap=26, w=11, seed=2, groups=3, dur=2.2, lo=".42"),
    ]
    return "".join(o)
page("content", "".join([
    head("WHEN DID YOU FINISH · 它怎么知道你说完了",
         "你是<strong>停一下</strong>，还是<strong>说完了</strong>？"),
    bigfig(_p3()),
    note("你想词的时候它安静等着，你真说完了它才开口。"),
]))

# ═══ P4 · 你一开口，它就闭嘴（打断 · canon 340ms）════════════════════════
#   图靠什么说话：它的话是一条长条，在你开口之后**很快就被剪断**，
#   断口右边留着一条虚线的空壳 —— 那是「它本来还要说的话，不说了」。
#   剪断处和你开口处之间夹着一段极窄的括号，人话大字 + 原数小标就钉在括号下面。
def _p4():
    UY, DY = 170, 400
    X0, X1 = 780, 880                     # 你开口 / 它收声
    o = [txt(44, UY + 10, "你", "ttl", size=28, anchor="middle", col=INK, i=1),
         txt(44, DY + 10, "它", "ttl", size=28, anchor="middle", col=AC, i=1),
         # 它正说着的一长条
         '<rect class="pop" style="--i:2;fill:%s" x="90" y="%d" width="790" height="68" rx="14"/>'
         % (AC, DY - 34),
         # 断口右边的空壳：本来还要说的部分
         '<rect class="pop" style="--i:4" x="880" y="%d" width="720" height="68" rx="14" fill="none" '
         'stroke="%s" stroke-width="2.2" stroke-dasharray="9 8"/>' % (DY - 34, HS),
         # 你开口
         bars(X0, 31, UY, INK, _HA, gap=26, w=11, groups=3, dur=2.4, lo=".34"),
         drift("M%d 104 V520" % X0, AD, 2.4, (8, 8), "4.2s", 3, ln=416),
         drift("M%d 104 V520" % X1, AD, 2.4, (8, 8), "4.2s", 3, ln=416, delay="-2.1s"),
         # 你一开口 → 它收声：一条又粗又短的快路径
         '<path class="dw" style="--len:190;--i:4" d="M782 240 C800 292 838 322 876 350" '
         'stroke="%s" stroke-width="8" fill="none"/>' % AD,
         packet("M782 240 C800 292 838 322 876 350", 190, col=AD, dur="1.1s", w=16),
         ah_d(880, 360, AD),
         halo_c(880, 400, 38, col=AD, dur="2.6s"),
         # 极窄的括号 + 人话大字 + 原数小标（两者同屏，永不拆开）
         '<path class="dw" style="--len:144;--i:5" d="M%d 468 V492 H%d V468" stroke="%s" '
         'stroke-width="2.6" fill="none"/>' % (X0, X1, AD),
         txt(830, 582, "不到半秒", "ttl", size=66, anchor="middle", col=AC, weight=700, i=6),
         txt(830, 630, "340ms · 打断收声", "lbl", size=19, anchor="middle", i=6),
    ]
    return "".join(o)
page("content", "".join([
    head("YOU SPEAK, IT STOPS · 你一开口，它就闭嘴",
         "你一开口，它<strong>马上闭嘴</strong>。"),
    bigfig(_p4()),
    note("不到半秒，它就安静下来听你说。"),
    source(),
]))

# ═══ P5 · 吵闹的派对里只听你（SAL · canon 95%）═══════════════════════════
#   图靠什么说话：中间是它，外面套两道有缺口的环 —— 缺口只朝左边、朝着你。
#   四面八方的噪声撞在环上碎成 ✕，只有从缺口进来的那一条直通中心。
#   ⚠ 两道环 **不做 transform 旋转**，只让 dash 爬（引擎 P10 的页级硬约束）：
#     缺口就是「只有目标人声进得来」这句话的图形依据，几何一转缺口就甩走了。
def _p5():
    CX, CY = 960, 372
    R1, R2 = 170, 240
    def gap_ring(r, dur, rev=False):
        # 缺口 40°（160°–200°，正对左边的你）；弧长 = 2πr × 320/360。
        # ⚠ sweep-flag 必须是 **0**：两个端点都在环的左侧、对 y 轴对称，
        #   过这两点的半径 r 的圆有两个（圆心在 CX 或 CX−1.88r）。
        #   large-arc=1 + sweep=1 会选中**另一个**圆心 —— 两道环各自偏心、不再同心
        #   （2026-08-24 实测：外环偏到 x=509、内环偏到 x=640，整页论证当场垮掉）。
        x1, y1 = pt(CX, CY, r, 200)
        x2, y2 = pt(CX, CY, r, 160)
        d = "M%.1f %.1f A%d %d 0 1 0 %.1f %.1f" % (x1, y1, r, r, x2, y2)
        return cyc(d, 2 * math.pi * r * 320 / 360.0, col=AC if r == R1 else HS,
                   w=3 if r == R1 else 2.6, dash=(9, 8), dur=dur, i=2, rev=rev)
    o = [gap_ring(R2, "26s"), gap_ring(R1, "18s", rev=True),
         aimark(CX, CY, 1.5),
         '<g class="mo-breathe" style="--mo-dur:3.6s;--mo-sc:1.04">'
         '<circle cx="%d" cy="%d" r="86" fill="none" stroke="%s" stroke-width="2.4" opacity=".5"/></g>'
         % (CX, CY, AC),
         halo_c(CX, CY, 86, dur="4.2s")]
    # 六路噪声：撞环碎成 ✕
    xs = []
    for k, deg in enumerate((250, 300, 350, 40, 90, 130)):
        sx, sy = pt(CX, CY, 330, deg)
        ax, ay = pt(CX, CY, 300, deg)
        bx, by = pt(CX, CY, 256, deg)
        cxp, cyp = pt(CX, CY, R2, deg)
        o.append(snd(sx, sy, 3, 20, 15, col=I3, w=3.2, i=3))
        o.append(drift("M%.1f %.1f L%.1f %.1f" % (ax, ay, bx, by), HS, 2.2, (7, 7), "3.6s", 3,
                       ln=44, delay="-%.1fs" % (k * 0.5)))
        xs.append((cxp, cyp))
    for g in range(2):
        body = "".join(cross(x, y, 15, AD, 4.6) for j, (x, y) in enumerate(xs) if j % 2 == g)
        o.append('<g class="mo-pulse" style="--mo-dur:2.6s;--mo-del:%.1fs;--mo-lo:.18">%s</g>' % (g * 1.3, body))
    # 你：从缺口直通中心的那一条
    lane = "M182 %d H862" % CY
    o += [person(110, CY, 1.0),
          '<path class="dw" style="--len:680;--i:4" d="%s" stroke="%s" stroke-width="4" fill="none"/>'
          % (lane, AC),
          packet(lane, 680, col=AC, dur="2.4s", w=16), ah_r(882, CY, AC),
          txt(110, CY + 96, "你", "ttl", size=28, anchor="middle", col=INK, i=4),
          txt(1213, 104, "噪音", "ttl", size=28, anchor="middle", col=I3, i=4),
          # 数字块钉在左上：左下（y602–606 那条走廊）会被背景板的 accent 线横穿大字
          txt(60, 132, "九成半", "ttl", size=66, col=AC, weight=700, i=6),
          txt(60, 180, "95% · 环境干扰屏蔽", "lbl", size=19, i=6)]
    return "".join(o)
page("content", "".join([
    head("ONLY YOU IN A NOISY ROOM · 吵闹里只听你",
         "十句噪音，它<strong>挡住九句半</strong>。"),
    bigfig(_p5()),
    note("派对再吵，它只把你的声音放进来。"),
    source(),
]))

# ═══ P6 · 快到像接话（延时 · canon 650ms）═══════════════════════════════
#   图靠什么说话：你的声音停在一根竖线上，它的声音从另一根竖线起来，
#   两根线之间夹着一段极短的缝。下面那把尺子把这段缝**放大**量给你看 ——
#   **尺子全长 800px = 1 秒，缝隙填色 520px = 650ms**，比例是真的，不是画着玩的。
#   改尺子长度必须同步改填色长度（RW / RF 保持 800 : 520 = 1000ms : 650ms）。
#   两支斜拉的引线把上面那道窄缝拉到下面这把尺子上 = 「放大看」，不是另起一件事。
def _p6():
    UY, DY = 180, 360
    X0, X1 = 700, 830                     # 你话音落 / 它开口
    RX, RW, RF = 380, 800, 520            # 尺子起点 / 全长 = 1 秒 / 填色 = 650ms
    fast = "M%d 246 C%d 280 %d 310 %d 338" % (X0, X0 + 42, X1 - 42, X1)
    o = [txt(44, UY + 10, "你", "ttl", size=28, anchor="middle", col=INK, i=1),
         txt(44, DY + 10, "它", "ttl", size=28, anchor="middle", col=AC, i=1),
         bars(90, 24, UY, INK, _HA, gap=25, w=11, groups=3, dur=2.4, lo=".34"),
         bars(845, 30, DY, AC, _HB, gap=25, w=11, seed=4, groups=3, dur=2.2, lo=".42"),
         drift("M%d 100 V470" % X0, HS, 2.4, (8, 8), "4.4s", 3, ln=370),
         drift("M%d 100 V470" % X1, AC, 2.4, (8, 8), "4.4s", 3, ln=370, delay="-2.2s"),
         # 接力：话音落点 → 开口点，一段又粗又短的快路径
         '<path class="dw" style="--len:170;--i:4" d="%s" stroke="%s" stroke-width="8" fill="none"/>'
         % (fast, AD),
         packet(fast, 170, col=AD, dur="1.0s", w=16), ah_r(X1 + 4, 340, AD),
         # 引线：把那道窄缝拉到尺子上（细虚线，只是「放大镜的两条边」）
         dline("M%d 470 L%d 616" % (X0, RX), HS, 1.8, 5, dash="6 7"),
         dline("M%d 470 L%d 616" % (X1, RX + RF), HS, 1.8, 5, dash="6 7"),
         # 尺子：整条 = 1 秒，填色 = 这段缝
         '<rect class="pop" style="--i:5" x="%d" y="626" width="%d" height="26" rx="13" fill="none" '
         'stroke="%s" stroke-width="2"/>' % (RX, RW, HS),
         '<rect class="pop" style="--i:6;fill:%s" x="%d" y="626" width="%d" height="26" rx="13"/>'
         % (AC, RX, RF),
         halo_rect(RX, 626, RF, 26, 13, sc="1.06", op=".3", dur="3.4s"),
         vline(RX, 612, 666, HS, 2, 5), vline(RX + RW, 612, 666, HS, 2, 5),
         txt(RX + RW + 18, 652, "1 秒", "ttl", size=28, col=I3, i=6),
         txt(1348, 662, "不到一秒", "ttl", size=62, col=AC, weight=700, i=6),
         txt(1348, 710, "650ms · 端到端", "lbl", size=19, i=6),
    ]
    return "".join(o)
page("content", "".join([
    head("FAST ENOUGH TO REPLY · 快到像接话",
         "你话音刚落，它<strong>就接上</strong>。"),
    bigfig(_p6()),
    note("这条缝比你说一句「你好」还短。"),
    source(),
]))

# ═══ P7 · 网断了它还在说（AI QoS —— **不是** FEC）═══════════════════════
#   Colin 的 AI QoS canon：网络好的时候多带一点（先囤进缓冲），
#   路上断掉的那一段照常往外说。**别写成 FEC**（那是另一套机制，本 deck 不讲）。
#   图靠什么说话：上面一条路，中间缺了一段；路边一个装满的罐子；
#   下面它说的话从头到尾**一根不断**，直直穿过路断掉的那一段。
def _p7():
    # 说话带**故意**压在 604（= 板子那条 accent 线所在的走廊）：密排的条把它整段盖住，
    # 等于引擎 rule(850)「把它压成收口线」的同一手法 —— 躲不开就吃掉它。
    RY, SY = 168, 604                     # 路 / 它说的话
    G0, G1 = 760, 1080                    # 路断掉的那一段
    o = [txt(90, 96, "NETWORK", "lbl", size=15, i=1),
         # 断网带：整条竖着的一片，图上所有件都从它身上穿过去
         '<rect class="pop" style="--i:1;fill:%s;opacity:.07" x="%d" y="40" width="%d" height="680" rx="16"/>'
         % (AD, G0, G1 - G0),
         drift("M%d 40 V720" % G0, AD, 2.2, (8, 8), "4.6s", 2, ln=680),
         drift("M%d 40 V720" % G1, AD, 2.2, (8, 8), "4.6s", 2, ln=680, delay="-2.3s"),
         txt((G0 + G1) // 2, 178, "断了", "ttl", size=34, anchor="middle", col=AD, i=3)]
    # 路：两条边 + 中间的虚线，断掉的一段整个没有
    for seg in ((90, G0), (G1, 1600)):
        o += [hline(seg[0], seg[1], RY - 40, HS, 2.4, 1), hline(seg[0], seg[1], RY + 40, HS, 2.4, 1),
              drift("M%d %d H%d" % (seg[0], RY, seg[1]), HS, 2, (10, 12), "5.2s", 2,
                    ln=seg[1] - seg[0])]
    # 网好的时候：包一路跑进罐子
    road = "M100 %d H%d" % (RY, G0 - 16)
    o += [packet(road, G0 - 116, col=AC, dur="2.0s", w=16),
          packet(road, G0 - 116, col=AC, dur="2.0s", delay="-1.0s", w=16),
          # 罐子：装了七成，正在呼吸
          box(560, 300, 180, 200, r=18, i=3),
          '<g class="mo-breathe" style="--mo-dur:3.8s;--mo-sc:1.03">'
          '<rect x="568" y="358" width="164" height="134" rx="12" style="fill:%s;opacity:.30"/></g>' % AC,
          halo_rect(560, 300, 180, 200, 18, sc="1.16", op=".3", dur="4.2s"),
          # 标签落在罐子**左边**：压在罐顶会被进料管从字上穿过去（2026-08-24 实测）
          txt(538, 412, "多带一点", "ttl", size=30, anchor="end", col=INK, i=4),
          '<path class="dw" style="--len:96;--i:4" d="M700 212 C700 254 662 268 652 292" stroke="%s" '
          'stroke-width="5" fill="none"/>' % AC,
          packet("M700 212 C700 254 662 268 652 292", 96, col=AC, dur="1.4s", w=13),
          ah_d(650, 300, AC),
          '<path class="dw" style="--len:56;--i:5" d="M650 500 V556" stroke="%s" stroke-width="5" '
          'fill="none"/>' % AC, ah_d(650, 566, AC),
          # 它说的话：一根不断，直穿断网带
          bars(90, 58, SY, AC, _HB, gap=26, w=11, groups=4, dur=2.8, lo=".42", sc=0.75),
          txt(90, 706, "它一直在说", "ttl", size=30, col=AC, i=6)]
    return "".join(o)
page("content", "".join([
    head("THE ROAD BREAKS, IT DOESN'T · 网断了它还在说",
         "路上断了，它<strong>照样说完</strong>。"),
    bigfig(_p7()),
    note("网好的时候先囤着，断了照样讲下去。"),
]))

# ═══ P8 · 它还长了眼睛（视觉模态 + 数字人）══════════════════════════════
#   图靠什么说话：左边一张画面 → 中间一只大眼睛 → 右边一张会说话的脸。
#   三件东西一字排开、包沿着两条道从左往右跑，读的方向就是「看见 → 说出来」。
def _p8():
    EX, EY = 720, 372
    L1 = "M392 %d H464" % EY
    L2 = "M974 %d H1188" % EY
    o = [  # 一张画面：山 + 太阳
        box(50, 230, 330, 260, r=22, i=1),
        '<path class="pop" style="--i:2;fill:%s;opacity:.34" d="M94 452 L200 300 L306 452 Z"/>' % HS,
        '<circle class="pop" style="--i:2;fill:%s;opacity:.62" cx="300" cy="312" r="30"/>' % AC,
        hline(74, 356, 456, HS, 2.2, 2),
        '<path class="dw" style="--len:72;--i:3" d="%s" stroke="%s" stroke-width="4" fill="none"/>' % (L1, AC),
        packet(L1, 72, col=AC, dur="1.6s", w=14), ah_r(468, EY, AC),
        # 眼睛
        '<path class="pop" style="--i:2" d="M480 %d Q720 172 960 %d Q720 572 480 %d Z" fill="var(--card-bg-2)" '
        'stroke="%s" stroke-width="3.6"/>' % (EY, EY, EY, HS),
        '<g class="mo-breathe" style="--mo-dur:3.6s;--mo-sc:1.05">'
        '<circle cx="%d" cy="%d" r="108" style="fill:%s;opacity:.20" stroke="%s" stroke-width="3"/></g>'
        % (EX, EY, AC, AC),
        '<circle class="pop" style="--i:4;fill:%s" cx="%d" cy="%d" r="50"/>' % (AC, EX, EY),
        '<circle class="pop" style="--i:5;fill:var(--card-bg-2)" cx="%d" cy="%d" r="18"/>' % (EX - 32, EY - 36),
        halo_c(EX, EY, 108, dur="4.0s"),
        txt(EX, 664, "看得见", "ttl", size=34, anchor="middle", col=INK, i=5),
        '<path class="dw" style="--len:214;--i:5" d="%s" stroke="%s" stroke-width="4" fill="none"/>' % (L2, AC),
        packet(L2, 214, col=AC, dur="2.0s", w=14), ah_r(1192, EY, AC),
        # 数字人：一张会说话的脸
        '<circle class="pop" style="--i:5" cx="1350" cy="%d" r="138" fill="var(--card-bg-2)" stroke="%s" '
        'stroke-width="3.2"/>' % (EY, HS),
        '<circle class="pop" style="--i:6;fill:%s" cx="1305" cy="%d" r="14"/>' % (INK, EY - 40),
        '<circle class="pop" style="--i:6;fill:%s" cx="1395" cy="%d" r="14"/>' % (INK, EY - 40),
        '<g class="mo-breathe" style="--mo-dur:2.4s;--mo-sc:1.10">'
        '<ellipse cx="1350" cy="%d" rx="42" ry="28" style="fill:%s;opacity:.55" stroke="%s" '
        'stroke-width="2.4"/></g>' % (EY + 52, AC, AC),
        '<g class="mo-pulse" style="--mo-dur:2.2s;--mo-lo:.24">%s</g>'
        % snd(1512, EY, 3, 28, 22, col=AC, w=4.2),
        txt(1390, 664, "说得出", "ttl", size=34, anchor="middle", col=AC, i=6),
    ]
    return "".join(o)
page("content", "".join([
    head("IT HAS EYES · 它还长了眼睛", "它还<strong>长了眼睛</strong>。"),
    bigfig(_p8()),
    note("它不只会听，还看得见你给它的画面。"),
]))

# ═══ P9 · 它住进了玩具里（R1 实拍 · 跨 deck 引用 robot26 原片）══════════
#   图靠什么说话：左边是前八页那只会聊天的记号，一支粗箭头把它送进右边的实物板子里。
#   右边那张不是画的，是真东西 —— ELI5 讲到这里必须落到一件摸得着的硬件上。
#   ⚠ img 全局规则的坑：图窗 992×744 与原片 1000×750 同为 4:3，cover 一格不裁；
#     img 必须 width/height 100% + object-fit（放大逼近墨迹会让 rect 冲出 .sh 盒，
#     occlusion-scan 的 TEXT-x-SPILL 只读 rect、不读 overflow:hidden ⇒ 稳报假命中）。
def _p9_side():
    up = "M330 216 C368 216 396 240 428 262"
    o = [bubble(60, 130, 250, 130, 34, hot=False, tail="bl", i=1),
         bars(96, 6, 195, I3, _HA, gap=32, w=13, groups=2, dur=2.8, lo=".38"),
         bubble(390, 208, 250, 130, 34, hot=True, tail="br", i=2),
         bars(426, 6, 273, AC, _HB, gap=32, w=13, seed=3, groups=2, dur=2.8, lo=".42"),
         '<path class="dw" style="--len:110;--i:3" d="%s" stroke="%s" stroke-width="3" fill="none"/>' % (up, HS),
         packet(up, 110, col=AC, dur="1.8s", w=12),
         # 送进去：一支又粗又肯定的箭头，箭尖顶到卡的分栏线（右边就是那块真板子）
         '<path class="dw" style="--len:400;--i:4" d="M200 468 C320 556 440 592 634 600" stroke="%s" '
         'stroke-width="9" fill="none"/>' % AD,
         packet("M200 468 C320 556 440 592 634 600", 400, col=AD, dur="1.9s", w=18),
         ah_r(660, 601, AD),
         txt(320, 706, "住进去", "ttl", size=34, anchor="middle", col=AD, i=5)]
    return "".join(o)
page("content", "".join([
    head("WHERE IT LIVES · 它住进了玩具里", "这是它的<strong>家</strong>。"),
    sh("spread eli-fig eli-card", "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:1" % (FX, FY, FW, FH),
       '<div class="eli-side"><div class="fig">'
       '<svg viewBox="0 0 688 744" style="width:100%%;height:auto">%s</svg></div></div>'
       '<div class="eli-shot"><img src="%sr1-wifi.webp" alt="声网 R1 开发套件实拍"></div>'
       % (_p9_side(), R26)),
    note("这套本事，装得进一块小板子里。"),
    sh("flow mono-sm src", "left:1140px;top:1016px;width:660px;height:24px;--i:7",
       "R1 开发套件 · 声网 · 公开发布信息"),
]))

# ═══ P10 · 全世界修好的路（SD-RTN · canon 200+ 节点）════════════════════
#   图靠什么说话：一条地球的弧，弧上一串站点，你的话从左边上路、一站一站跳到右边的它。
#   旁边还有几条灰虚线的备用路 —— 路不止一条，哪条通就走哪条。
def _p10():
    CXE, CYE, RE = 840, 1700, 1420        # 地球弧的圆心与半径（apex y = 280）
    def arc_y(x):
        return CYE - math.sqrt(RE * RE - (x - CXE) ** 2)
    y_end = arc_y(40)
    earth = "M40 %.1f A%d %d 0 0 1 1640 %.1f" % (y_end, RE, RE, y_end)
    RN = 1520                              # 外面那圈网络层
    yn = CYE - math.sqrt(RN * RN - 800 ** 2)
    net = "M40 %.1f A%d %d 0 0 1 1640 %.1f" % (yn, RN, RN, yn)
    net_len = 2 * math.asin(800.0 / RN) * RN
    NX = [120, 300, 480, 660, 840, 1020, 1200, 1380, 1560]
    NP = [(x, arc_y(x)) for x in NX]
    o = ['<path class="pop" style="--i:1;fill:%s;opacity:.06" d="%s L1640 744 L40 744 Z"/>' % (AC, earth),
         '<path class="dw" style="--len:1700;--i:1" d="%s" stroke="%s" stroke-width="3" fill="none"/>'
         % (earth, HS),
         cyc(net, net_len, col=HS, w=2, dash=(9, 8), dur="30s", i=2)]
    # 备用路：站点之间的灰虚线，**向外拱起**跨过地球弧（贴着弧画就跟弧本身重合、白画）。
    # 「路不止一条，哪条通就走哪条」靠的正是这几条拱出来的备用弧。
    for k, (a, c, lift) in enumerate(((1, 3, 120), (5, 7, 120), (2, 6, 210))):
        mx = (NP[a][0] + NP[c][0]) / 2.0
        my = (NP[a][1] + NP[c][1]) / 2.0 - lift
        d = "M%d %.1f Q%.1f %.1f %d %.1f" % (NP[a][0], NP[a][1], mx, my, NP[c][0], NP[c][1])
        o.append(drift(d, HS, 2, (7, 7), "5.0s", 3, ln=700, delay="-%.1fs" % (k * 1.4)))
    # 主路：你 → 四站 → 它
    lane = ("M150 620 L%d %.1f L%d %.1f L%d %.1f L%d %.1f L1530 620"
            % (NP[1][0], NP[1][1], NP[3][0], NP[3][1], NP[5][0], NP[5][1], NP[7][0], NP[7][1]))
    ln = 0.0
    pts = [(150, 620), NP[1], NP[3], NP[5], NP[7], (1530, 620)]
    for a, bq in zip(pts, pts[1:]):
        ln += math.hypot(bq[0] - a[0], bq[1] - a[1])
    o += ['<path class="dw" style="--len:%d;--i:4" d="%s" stroke="%s" stroke-width="4" fill="none"/>'
          % (int(ln), lane, AC),
          packet(lane, ln, col=AC, dur="3.4s", w=16),
          packet(lane, ln, col=AC, dur="3.4s", delay="-1.7s", w=16)]
    # 站点
    for g in range(2):
        body = "".join('<circle cx="%d" cy="%.1f" r="12" style="fill:%s" stroke="var(--card-bg-2)" '
                       'stroke-width="3"/>' % (x, y, AC) for j, (x, y) in enumerate(NP) if j % 2 == g)
        o.append('<g class="mo-pulse" style="--mo-dur:3.0s;--mo-del:%.1fs;--mo-lo:.30">%s</g>' % (g * 1.5, body))
    o += [person(100, 620, 0.92), txt(100, 716, "你", "ttl", size=26, anchor="middle", col=INK, i=5),
          aimark(1580, 620, 1.0), txt(1580, 716, "它", "ttl", size=26, anchor="middle", col=AC, i=5),
          txt(60, 140, "两百多个驿站", "ttl", size=58, col=AC, weight=700, i=6),
          txt(60, 186, "200+ 节点 · SD-RTN", "lbl", size=19, i=6)]
    return "".join(o)
page("content", "".join([
    head("ROADS BUILT WORLDWIDE · 全世界修好的路",
         "你的话，走<strong>修好的路</strong>。"),
    bigfig(_p10()),
    note("全球两百多个驿站，替你的话挑最快的一条。"),
    source(),
]))

# ═══ P11 · 收尾（title 板 · 与深入讲解版封面同句 = 家族闭环）═════════════
#   图靠什么说话：P1 的两只气泡长成了一个不断的环 —— 话在环上一直走，走完又回来。
#   「对话即交互」这一句是引擎 22 页深入讲解版封面的原句，两份 deck 在这里合上。
def _p11():
    loop = "M140 372 A700 300 0 1 1 1540 372 A700 300 0 1 1 140 372"
    # Ramanujan 近似周长：a=700 b=300 → 3269
    perim = math.pi * (700 + 300) * (1 + 3 * 0.16 / (10 + math.sqrt(4 - 3 * 0.16)))
    return "".join([
        cyc(loop, perim, col=HS, w=2.6, dash=(10, 9), dur="24s", i=1),
        packet(loop, perim, col=AC, dur="9s", w=16, op=".30"),
        packet(loop, perim, col=AC, dur="9s", delay="-4.5s", w=16, op=".30"),
        bubble(330, 200, 480, 260, 52, hot=False, tail="bl", i=2),
        bars(376, 8, 330, I3, _HA, gap=48, w=17, groups=2, dur=3.0, lo=".38"),
        bubble(880, 290, 480, 260, 52, hot=True, tail="br", i=3),
        bars(926, 8, 420, AC, _HB, gap=48, w=17, seed=3, groups=2, dur=3.0, lo=".42"),
        halo_rect(880, 290, 480, 260, 52, dur="5.4s"),
    ])
page("title", "".join([
    head("CONVERSATION IS THE INTERFACE · 对话即交互", "<strong>对话即交互</strong>。"),
    bigfig(_p11()),
    note("让陪伴自然，让生意成单。", w=940),
    sh("flow mono-sm src", "left:1140px;top:1016px;width:660px;height:24px;--i:7",
       "大人版 · colinyao.com/convoai"),
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
        # 主题初始化：与引擎 / info 同一个 localStorage 键（家族一致，别改键名）
        '<script>try{if(localStorage.getItem("colin-theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}</script>\n'
        '<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>声网 · 对话式 AI · 讲给五岁的你</title>\n'
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
        # deckSwap 常显 chip（与引擎 / info 同一套）：本 deck 是**转发场景**，
        # 链接被直接甩进群里，藏起来的切换键等于没有键。
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
        'window.__setTheme=apply;'
        'b.addEventListener("click",function(){b.blur();'
        'var now=document.documentElement.getAttribute("data-theme")==="dark"?"dark":"light";'
        'var nxt=(now==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",nxt);}catch(e){}apply(nxt);});})();</script>\n'
        "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")

    # ── 构建期闸门（别等到 qa）──────────────────────────────────────────────
    assert total == 11, "页数漂移：%d != 11" % total
    assert doc.count("<section") == 11, "section 数漂移：%d" % doc.count("<section")
    boards = {i: b for i, (b, _y) in enumerate(PAGES, 1)}
    assert {i for i, b in boards.items() if b == "title"} == {1, 11}, \
        "title 板页漂移：%r" % sorted(i for i, b in boards.items() if b == "title")
    # 常显容器不挂 data-step：全 deck 零分步（引擎 P19「多出一个空页面」的根因）。
    # 只扫 <section> 正文 —— 共享 motion.css 的注释里写着 [data-step="N"] 的说明文字，
    # 扫整份文档会被那行注释误伤。
    _pages_html = "\n".join(secs)
    assert 'data-step="' not in _pages_html, "本 deck 不该有任何 [data-step]（全 11 页 steps=0）"
    assert doc.count('data-steps="0"') == 11, "分步声明漂移"
    # 红线反向闸：价格 / staging / 盲测 / 32,000 / Call Agent / 客户名 / 外链
    for _bad in ("¥8,500", "¥2,999", "¥5,501", "8,500", "2,999", "5,501",
                 "staging", "盲测", "32,000", "Call Agent", "外呼"):
        assert _bad not in doc, "红线：全 deck 不许出现「%s」" % _bad
    # 客户名一个不进（名单与 qa-convoai-info.mjs 的 CASES 逐字同源）
    for _c in ("集贤科技", "Robopoet", "luwu", "Pophie", "商汤", "MiniMax", "智谱清言",
               "星野", "灵机一动", "LOOKTECH", "HeyCyan", "LOOKEE", "莲偶科技", "豆神 AI"):
        assert _c not in doc, "红线：科普 deck 不上案例，客户名「%s」不许入页" % _c
    body = doc.split("<body>")[1]
    assert "<a " not in body and "href=" not in body, "红线：a[href] 必须为 0（指路走纯文本）"
    # canon 三数 + 200+ 必须各自在场（人话大字永不顶替原数）
    for _n in ("340ms", "95%", "650ms", "200+"):
        assert _n in doc, "canon 原数缺席：%s" % _n
    print("convoai-eli5.html · %d 页 · %dKB · conf-light 默认 · 分步 0 · 大图 %d×%d（舞台的 %.1f%%）"
          % (total, len(doc) // 1024, FW, FH, FW * FH / (1920 * 1080) * 100))

if __name__ == "__main__":
    build()
