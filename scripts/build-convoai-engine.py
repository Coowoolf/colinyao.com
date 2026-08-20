#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-engine.py ·《声网 · 对话式 AI 引擎 · 产品介绍》17 页
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
#   并给 P6 / P7 / P14 各加一步 presenter-controlled build（data-steps + [data-step]）。
#
# 结构（17 页；★ = 2026-08-20 一轮新增，☆ = 二轮新增）：
#   P1  封面（title 板）        P2  实时决策        P3  双工三模式 ★
#   P4  全双工工作原理 ★        P5  三件极致        P6  实时语音链路（build ×1）
#   P7  VAD ★（build ×1）       P8  产品架构大图 ☆  P9  优雅打断
#   P10 SAL 选择性注意力        P11 弱网            P12 多模态
#   P13 开放编排                P14 接入架构（build ×1）
#   P15 典型场景                P16 Why Agora（口径锁）
#   P17 收尾（title 板）
#
# ── P16 数据口径（Colin 2026-08-18 指错，改为 31p 拜访版 P2 的锁定口径，一字对齐）──
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

# ── 背景板（两张：title 给 P1/P13，content 给 P2–P12）────────────────────────
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
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 15px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--sig-ink);}
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

def dline(d, col="var(--hair-strong)", w=2, i=1, dash="7 7"):
    """虚线：不能走 .dw —— motion.css 的 .dw{stroke-dasharray:var(--len)} 会把 dasharray
       属性整条压掉，虚线会渲染成实线。这里改挂 .pop（只动 opacity/transform），破折保留。"""
    return ('<path class="pop" style="--i:%d" d="%s" stroke="%s" stroke-width="%s" '
            'fill="none" stroke-dasharray="%s"/>' % (i, d, col, w, dash))

def box(x, y, w, h, r=4, hot=False, dashed=False, i=0):
    """家族图框：常态走 class="box"（fill card-bg / stroke hair），高亮走 accent 描边"""
    d = ' stroke-dasharray="7 6"' if dashed else ""
    if hot:
        return ('<rect class="pop" style="--i:%d" x="%d" y="%d" width="%d" height="%d" rx="%d" '
                'fill="none" stroke="var(--accent)" stroke-width="2.5"%s/>' % (i, x, y, w, h, r, d))
    return ('<rect class="pop box" style="--i:%d" x="%d" y="%d" width="%d" height="%d" rx="%d" '
            'stroke-width="1.4"%s/>' % (i, x, y, w, h, r, d))

def txt(x, y, s, cls="txt", size=None, anchor=None, col=None, weight=None, i=None,
        mono=False, ls=None):
    st = []
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
_LGK = {"solid": lg_solid, "dash": lg_dash, "dot": lg_dot, "fast": lg_fast}

def step_badge(x, y, n, r=16, i=2):
    """握手序号徽标（P14）：不透明圆片 + accent 序号，压在连线上、线从徽标底下穿过。
       fill 必须是 --card-bg-2（#fffffe / #131320）——  --card-bg 是 72% 透明，
       半透明徽标会让连线从数字里透出来，读成「数字被划掉」。"""
    return ('<circle class="pop" style="--i:%d;fill:var(--card-bg-2)" cx="%d" cy="%d" r="%d" '
            'stroke="%s" stroke-width="2"/>' % (i, x, y, r, AC)
            + txt(x, y + 7, str(n), "ttl", size=20, anchor="middle", col=AC, weight=700))
def legend(x, y, items, i=9, gap=54):
    """图例行：items = [(kind, 标签)] 或 [(kind, 标签, 线宽)]；kind ∈ solid / dash / dot / fast。
       第三项给线宽：图例样线必须与页内真线同粗，否则「粗一档」在图例里读不出来。
       步进按标签字数估宽（CJK 14px/字），够松，不会互相压。"""
    o, cx = [], x
    for it in items:
        kind, label = it[0], it[1]
        w = it[2] if len(it) > 2 else None
        o.append(_LGK[kind](cx, y, i=i) if w is None else _LGK[kind](cx, y, w=w, i=i))
        o.append(txt(cx + 50, y + 5, label, "sm", size=14, i=i))
        cx += 50 + int(len(label) * 13.2) + gap
    return "".join(o)

# ═══ P1 · 封面（title 板）══════════════════════════════════════════════════
page("title", "".join([
    sh("flow kk", "left:120px;top:200px;width:1500px;height:28px",
       "AGORA · CONVERSATIONAL AI ENGINE · 产品介绍"),
    sh("ink", "left:120px;top:266px;width:1500px;height:250px;"
       "font:700 96px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "<strong style='color:var(--accent)'>2 行代码</strong>，<br>构建自然流畅的对话体验。"),
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
        o.append(box(x, y, w, h, 10, hot=hot, i=k + 1))
        o.append(txt(x + 26, y + (38 if hot else 34), "%s · %s" % (no, act), "sm",
                     size=14, col=AC, mono=True, ls=".14em"))
        o.append(txt(x + 26, y + (80 if hot else 70), ttl, "ttl",
                     size=25 if hot else 23, col=AC if hot else None))
        o.append(txt(x + 26, y + (118 if hot else 104), body, "sm", size=17 if hot else 16))
    # ── 三条实线主流程边（环的正向）：每条都带标注，说清「这一步交出去的是什么」──
    o.append(hline(780, 988, 87, AC, 2.5, 2)); o.append(ah_r(1000, 87, AC))
    o.append(txt(890, 69, "对象 · 场景 · 情绪", "sm", size=16, anchor="middle"))
    o.append(vline(1200, 154, 238, AC, 2.5, 3)); o.append(ah_d(1200, 250, AC))
    o.append(txt(1222, 208, "何时开口", "sm", size=16))
    o.append(hline(980, 792, 327, AC, 2.5, 4)); o.append(ah_l(780, 327, AC))
    o.append(txt(880, 309, "开口表达", "sm", size=16, anchor="middle"))
    # ── 闭环关键边：点线反馈弧，从「表达」绕回「听清」——本页的灵魂 ──
    #   3px（比实线细一档但看得见）+ 标签压在弯道肘部右侧的月牙里，读者一眼知道它注解谁
    o.append(dline("M376 327 C 240 327, 170 300, 170 207 C 170 114, 240 87, 360 87", AD, 3, 5,
                   dash="3 8"))
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
    """双轨活动图（vb 460×116）· 2026-08-20 三轮升维：
       三张小图共用同一套时间轴语法 —— A 方 / B 方两条横向活动带，时间从左到右，
       实心带 = 正在占线，虚线空带 = 没在说。形态差异即模式差异，不靠文字解释：
         单工   A 带满格连续 / B 带全空 / 一支单向箭头
         半双工 A、B 交替出现，轮次之间是「切换闸」竖标记与空档；
                B 在 A 讲话中途尝试出声 → 被闸拦住的 ✕
         全双工 A、B 有重叠区间（同时活动），重叠处高亮，插话瞬间画快路径粗线
       末行是无字刻度：本页没有已核定的时间数字，只给节奏感，绝不发明数字。"""
    AY, BY, BH = 14, 72, 26
    def band(x, w, y, on, i=1, col=AC, op=None):
        if on:
            return ('<rect class="pop" style="--i:%d;fill:%s%s" x="%d" y="%d" width="%d" '
                    'height="%d" rx="4"/>' % (i, col, (";opacity:%s" % op) if op else "", x, y, w, BH))
        return ('<rect class="pop" style="--i:%d" x="%d" y="%d" width="%d" height="%d" rx="4" '
                'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 5"/>'
                % (i, x, y, w, BH, HS))
    o = [txt(0, 34, "A", "ttl", size=20), txt(0, 92, "B", "ttl", size=20)]
    if mode == "simplex":
        o += [band(40, 412, AY, True, 1), band(40, 412, BY, False, 2),
              vline(246, 46, 60, AC, 2.5, 3), ah_d(246, 70, AC, 7)]
    elif mode == "half":
        o += [band(40, 112, AY, True, 1), band(188, 112, BY, True, 2),
              band(336, 116, AY, True, 3),
              band(188, 112, AY, False, 2), band(336, 116, BY, False, 3),
              # 两道切换闸：轮次之间必须先让线，才轮到对方（首闸在两带之间断开，让出闸名）
              dline("M170 6 V48", HS, 2, 2, dash="5 5"),
              dline("M170 70 V104", HS, 2, 2, dash="5 5"),
              txt(170, 66, "切换", "sm", size=14, anchor="middle", col="var(--ink-3)"),
              dline("M318 6 V104", HS, 2, 3, dash="5 5"),
              # 冲突瞬间：A 讲话中途 B 想出声 —— 被拦住
              band(64, 66, BY, False, 2),
              txt(97, 94, "✕", "ttl", size=22, anchor="middle", col=AD)]
    else:
        o += ['<rect class="pop" style="--i:2;fill:%s;opacity:.13" x="228" y="6" width="64" '
              'height="100" rx="4"/>' % AD,
              band(40, 252, AY, True, 1), band(228, 224, BY, True, 2),
              # 插话瞬间：粗 accent 快路径（与 P8 / P9 同 idiom）
              vline(260, 98, 50, AD, 5, 3), ah_u(260, 44, AD, 7)]
    # 无字刻度的时间轴
    o.append(hline(40, 440, 110, HS, 1.4, 5))
    o.append(ah_r(452, 110, "var(--ink-3)", 7))
    o += [vline(tx, 104, 110, HS, 1.4, 5) for tx in (40, 140, 240, 340, 440)]
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
       '<div style="padding:26px 30px;height:100%%;display:flex;flex-direction:column">'
       '<div style="font:500 14px/1 var(--f-mono);letter-spacing:.18em;color:%s">%s</div>'
       '<div style="margin-top:12px;font:700 38px/1.15 var(--f-cn);color:var(--ink)">%s</div>'
       '<div class="fig" style="margin-top:16px">'
       '<svg viewBox="0 0 460 116" style="width:100%%;height:auto">%s</svg></div>'
       '<div style="margin-top:16px;font:400 19px/1.55 var(--f-cn);color:var(--ink-2)">%s</div>'
       '<div style="margin-top:auto;padding-top:14px;border-top:1px solid var(--hair);'
       'font:400 17px/1.5 var(--f-cn);color:var(--ink-3)">%s</div></div>'
       % (AC if _on else "var(--ink-3)", _tag, _name, _duplex_fig(_k), _mech, _ex))
    for _i, (_tag, _name, _k, _mech, _ex, _on) in enumerate(_DUPLEX)
    ] + [
    # 页级迷你图例（三张小图共用一套线型语法，图例只出一次，压在 lab 02 同一基线的右侧）
    figbox(1080, 664, 720, 720, 28,
           legend(0, 14, [("solid", "主数据流"), ("dash", "事件 / 控制"), ("fast", "快路径")]),
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
    o.append('<circle class="pop" style="--i:6;fill:%s" cx="%d" cy="190" r="8"/>' % (AD, _XIN))
    o.append(ah_d(_XIN, 280, AD, 8))
    o.append(txt(_XIN + 20, 248, "340ms", "ttl", size=20, col=AD, weight=700))
    # ── NOW 播放头：一条竖虚线穿过三条活动带 —— 「同一瞬间」三件事都在跑 ──
    o.append(dline("M%d 50 V336" % _XNOW, AC, 1.6, 7, dash="4 8"))
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

# ═══ P5 · 三件极致 ·「把三件事，做到极致」══════════════════════════════════
_EXTREMES = [
    ("01 · LATENCY",  "650", "ms", "端到端响应延时", "从说完话到智能体开口，全链路深度优化，低至 650ms。"),
    ("02 · BARGE-IN", "340", "ms", "极速打断响应",   "随时插话即时收声，模拟真人对话节奏。"),
    ("03 · SHIELD",   "95",  "%",  "环境干扰屏蔽",   "选择性注意力锁定，嘈杂环境也能精准听清对话人声。"),
]
page("content", "".join([
    head("REAL-TIME VOICE · 极致实时语音体验", "把三件事，<strong>做到极致</strong>。"),
    lab(120, 236, "01 · THREE EXTREMES"),
    ] + [
    sh("rise card-c", "left:%dpx;top:300px;width:520px;height:500px;--i:%d" % (120 + _i * 580, 2 + _i),
       '<div style="padding:44px 40px;height:100%%;display:flex;flex-direction:column;justify-content:center">'
       '<div style="font:500 14px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-3)">%s</div>'
       '<div style="margin-top:28px;font:900 132px/.92 var(--f-en);letter-spacing:-.035em;color:var(--accent)">'
       '%s<span style="font-size:.38em;letter-spacing:0">%s</span></div>'
       '<div style="margin-top:28px;font:700 32px/1.25 var(--f-cn);color:var(--ink)">%s</div>'
       '<div style="margin-top:14px;font:400 20px/1.65 var(--f-cn);color:var(--ink-2)">%s</div></div>'
       % (_tag, _v, _u, _n, _d))
    for _i, (_tag, _v, _u, _n, _d) in enumerate(_EXTREMES)
    ] + [
    rule(850),
    # 原 rail（纯英文口号）替换为 SOURCE 行：三个数字是全 deck 被引用最多的口径，
    # 必须自带出处与「典型值」限定（2026-08-20 仲裁 P0）。
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px;--i:7",
       "SOURCE · 声网官网 · 引擎发版说明 公开口径 · 典型值 · 事实截止 2026.08"),
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
        o.append(box(x, 120, 220, 130, 6, hot=hot, i=i + 1))
        o.append(txt(cx, 178, n, "ttl", size=26, anchor="middle",
                     col=AC if hot else None))
        o.append(txt(cx, 214, sub, "sm", size=17, anchor="middle"))
        o.append(txt(cx, 290, foot, "lbl", size=15, anchor="middle"))
    # 主路连接箭头（末段 TTS → 喇叭，中途在 x1415 分叉）
    for x1, x2, k in [(118, 180, 0), (400, 470, 1), (690, 760, 2), (980, 1050, 3), (1270, 1566, 4)]:
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
    o.append(dline("M1375 193 V276", HS, 2, 2, dash="6 6"))
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
    head("PIPELINE · 实时语音链路", "一条深度优化的<strong>实时语音</strong>链路。"),
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
    o.append(dline("M680 %d H1660" % _VTOP, AD, 2, 5, dash="2 6"))
    o.append(dline("M680 %d H1660" % _VBOT, AD, 2, 5, dash="2 6"))
    o.append(txt(692, 56, "平滑 / 滞回", "sm", size=13, col=AD, mono=True))
    # ⑤ 逐帧概率曲线（accent 实线）
    o.append('<path class="dw" style="--len:1200;--i:5" d="M680 118 C 770 116, 836 102, 880 62 '
             'C 922 30, 980 40, 1042 48 C 1104 56, 1140 40, 1200 50 C 1256 60, 1272 84, 1302 96 '
             'C 1344 112, 1420 118, 1660 116" fill="none" stroke="%s" stroke-width="3" '
             'stroke-linecap="round"/>' % AC)
    # ⑥ 两枚事件 pin（虚线 = 事件语法）
    for px, nm in [(_VSOS, "SOS"), (_VEOS, "EOS")]:
        o.append(dline("M%d 32 V126" % px, HS, 2, 6, dash="6 6"))
        o.append('<circle class="pop" style="--i:6;fill:%s" cx="%d" cy="%d" r="6"/>'
                 % (AC, px, _VTOP if px == _VSOS else 117))
        o.append(txt(px + 12, 44, nm, "lbl", size=15, col=AC))
    o.append(txt(1180, 18, "SOS / EOS 事件", "sm", size=14, col="var(--ink-3)", mono=True))
    # ⑦ 声学之上再叠一层语义（商业进阶版的差异，用既有词）
    o.append('<path class="pop" style="--i:7" d="M1430 78 C 1500 62, 1560 54, 1660 46" fill="none" '
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
    head("VOICE ACTIVITY DETECTION · 从能量检测到语义判停",
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
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px;--i:9",
       "SOURCE · GITHUB.COM/TEN-FRAMEWORK/TEN-VAD · TEN ECOSYSTEM · "
       "引擎发版说明 · SOS/EOS 判停重构自 V2.6"),
]), steps=1)

# ═══ P8 · 产品架构大图 ·「一张图，看懂全双工引擎」（2026-08-20 新增）═════════
#   全 deck 唯一一张「大图页」：静置全量、不分步 —— 一张图就要一眼全。
#   viewBox 1680×660 与 .sh 同尺寸 ⇒ 1 svg 单位 = 1 屏幕像素，所有坐标可直接对表。
#   三秒可读性的四个锚点（验收标准）：
#     ① 上行 / 下行两条 accent 车道同时贯穿 → 两件事同时在跑
#     ② AI-VAD 是最大的一只 hot 盒，坐在上行车道正中 → 它是路口
#     ③ accent-deep 粗线从 AI-VAD 垂直插进「语音输出」，旁注「不经过 LLM」→ 打断是快路径
#     ④ 点线从下行车道弯回 AEC，标「参考信号」→ 所以听不见自己
#   版式雷区：content 背景板自带 accent 细线在屏幕 y848–852（= svg y566–570），
#   底部 SD-RTN 条从 y566 起，正好把它压在条内，不会横穿任何文字。
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
    o.append(box(634, 116, 430, 128, 8, hot=True, i=4))
    o.append(txt(849, 158, "AI-VAD 进阶判停", "ttl", size=30, anchor="middle", col=AC))
    o.append(txt(849, 192, "TEN VAD 声学内核 · 帧级 10/16ms · 开源", "sm", size=16, anchor="middle"))
    o.append(txt(849, 220, "+ 语义判停 · CAN 三路融合 · 商业进阶", "sm", size=16, anchor="middle", col=AC))
    # 角标压在盒的左上角（而不是右上角）：右上角紧邻「→ ASR」那支箭头，读者会把它当箭头的注解
    o.append(txt(640, 106, "帧级 10/16ms", "sm", size=14, col=AC, mono=True))
    o.append(box(1106, 132, 180, 88, 6, i=5))
    o.append(txt(1196, 172, "流式 ASR", "ttl", size=21, anchor="middle"))
    o.append(txt(1196, 198, "增量文本", "sm", size=15, anchor="middle"))
    for x1, x2, k in [(110, 150, 1), (340, 382, 2), (592, 634, 3), (1064, 1106, 4), (1286, 1328, 5)]:
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
    o.append(dline("M1030 250 C 1120 316, 1330 316, 1420 258", HS, 2, 5, dash="7 6"))
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
    o.append(hline(1328, 1300, 368, AC, 2.5, 5))
    o.append(ah_l(1286, 368, AC))
    o.append(hline(1106, 844, 368, AC, 2.5, 6))
    o.append(ah_l(830, 368, AC))
    o.append(hline(620, 122, 368, AC, 2.5, 7))
    o.append(ah_l(108, 368, AC))
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
    o.append(dline("M560 362 C 470 320, 360 280, 300 234", AD, 3, 7, dash="3 8"))
    o.append(ah_u(300, 222, AD, 7))
    o.append(txt(372, 252, "参考信号——所以听不见自己", "sm", size=15, col=AD))
    # (b) 打断快路径：accent 粗线，从 AI-VAD 垂直直插「语音输出」，不经过 LLM
    o.append(vline(700, 248, 314, AD, 5, 6))
    o.append(ah_d(700, 324, AD, 8))
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
    return "".join(o)

page("content", "".join([
    head("PRODUCT ARCHITECTURE · FULL-DUPLEX × AI-VAD · DATA FLOW",
         "<strong>一张图</strong>，看懂全双工引擎。"),
    lab(120, 246, "01 · ONE PICTURE · 上行 / 中枢 / 下行 · 两条闭环"),
    figbox(120, 282, 1680, 1680, 660, _bigmap(), i=1),
    land("听的车道永不关闭，说的车道随时让行——中间站着 AI-VAD。", y=944),
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px;--i:9",
       "SOURCE · 引擎发版说明 · TEN ECOSYSTEM · 打断/延时口径见 P5"),
]))

# ═══ P9 · 优雅打断 ·「想插话就插话，340ms 即时收声」════════════════════════
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
    o.append(_bars(170, 51, 120, AC, hs=_P9HS))
    o.append('<rect class="pop" style="--i:3" x="1055" y="88" width="585" height="64" rx="6" '
             'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 6"/>' % HS)
    o.append(_P9QUIET % (3, 1075, 118, 545))       # 让位段：无字静默平线（与用户轨呼应）
    o.append(vline(_P9CUT, 82, 158, AD, 4, 3))
    # ── 340ms 快路径：插话 → 收声，粗 accent-deep，两端钉在两条轨之间 ──
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
    o.append(dline("M%d 74 V320" % _P9IN, HS, 2, 5, dash="6 6"))
    o.append(dline("M%d 74 V320" % _P9CUT, HS, 2, 5, dash="6 6"))
    o.append(txt(_P9IN, 346, "用户插话", "sm", size=18, anchor="middle", col=AD, weight=700))
    o.append(txt(_P9CUT, 346, "智能体收声", "sm", size=18, anchor="middle", col=AC, weight=700))
    # 图例从 y378 提到 y340，与两枚事件标同一条基线：左 = 图例（x0–442），右 = 事件标（x664 起），
    # 中间还留 220px。这一并到一行，图底那条「左边整片空、右边两个字」的空带就没有了，
    # viewBox 也从 396 收到 372，页面重心跟着往上收一档。
    o.append(legend(0, 340, [("solid", "音频流"), ("dash", "事件 / 控制"), ("fast", "打断快路径")]))
    return "".join(o)
page("content", "".join([
    head("INTERRUPTION · 优雅打断", "想插话就插话，<strong>340ms 即时收声</strong>。"),
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

# ═══ P10 · SAL ·「嘈杂环境里，只听该听的人」═══════════════════════════════
# 2026-08-20 三轮升维：一排「干扰 → 竖墙」改成一个真正的空间场景 ——
#   中心是智能体（唯一 hot 件），左侧一条实线波束从目标人声直达中心（屏蔽环在这一侧留缺口），
#   右侧三路干扰用点线波束射向中心，全部撞在屏蔽环上打 ✕。
#   屏蔽环 = 本页的闭环感：它把「只听该听的人」画成一个可以指着讲的东西。
_NOISE = [("旁人交谈", 40), ("环境噪声", 240), ("背景音乐", 440)]
_SCX, _SCY, _SR = 760, 240, 190      # 场景中心 / 屏蔽环半径
def _sal_fig():
    o = []
    # ── 屏蔽环：左侧 ±8° 留缺口，正好让目标人声的波束穿进来 ──
    o.append('<path class="pop" style="--i:3" d="M%d %d A %d %d 0 1 1 %d %d" fill="none" '
             'stroke="%s" stroke-width="2.5" stroke-dasharray="10 9"/>'
             % (_SCX - 188, _SCY - 26, _SR, _SR, _SCX - 188, _SCY + 26, AC))
    # ── 目标人声（左）──
    o.append('<circle class="pop box" style="--i:1" cx="150" cy="240" r="62" stroke-width="2"/>')
    o.append('<path class="pop" style="--i:1" d="M150 214a11 11 0 0 1 11 11v9a11 11 0 0 1-22 0v-9a11 11 0 0 1 11-11z '
             'M134 234a16 16 0 0 0 32 0 M150 250v10" fill="none" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % AC)
    o.append(txt(150, 346, "目标人声", "ttl", size=22, anchor="middle", col=AC))
    o.append(txt(150, 378, "锁定 · 精准识别", "sm", size=17, anchor="middle"))
    o.append(hline(212, 628, 240, AC, 3.5, 2)); o.append(ah_r(640, 240, AC))
    o.append(txt(420, 216, "声纹锁定 · 只留目标人声", "sm", size=17, anchor="middle", col=AC))
    # ── 智能体（中 · 唯一 hot 件）──
    o.append('<circle class="pop" style="--i:0;fill:var(--card-bg-2);stroke:%s" cx="%d" cy="%d" '
             'r="110" stroke-width="3"/>' % (AC, _SCX, _SCY))
    o.append(txt(_SCX, 232, "智能体", "ttl", size=28, anchor="middle"))
    o.append(txt(_SCX, 270, "声纹锁定", "sm", size=18, anchor="middle", col=AC))
    # ── 三路干扰：点线波束 → 撞在屏蔽环上 ✕ ──
    for n, sy in _NOISE:
        dx, dy = 1520 - _SCX, sy - _SCY
        ln = (dx * dx + dy * dy) ** .5
        ux, uy = dx / ln, dy / ln
        ex, ey = 1520 - ux * 48, sy - uy * 48                  # 干扰源圆边
        rx, ry = _SCX + ux * _SR, _SCY + uy * _SR              # 屏蔽环交点
        o.append('<circle class="pop box" style="--i:4" cx="1520" cy="%d" r="48" stroke-width="1.4"/>' % sy)
        o.append(txt(1520, sy + 8, n, "sm", size=17, anchor="middle"))
        o.append(dline("M%d %d L%d %d" % (ex, ey, rx + ux * 14, ry + uy * 14), HS, 2.4, 5, dash="2 7"))
        o.append(txt(rx, ry + 10, "✕", "ttl", size=28, anchor="middle", col=AD))
    # ── 屏蔽环的名牌：压在环底，不透明底把弧线遮住，读者知道这一圈叫什么 ──
    o.append('<rect class="pop" style="--i:6;fill:var(--card-bg-2)" x="%d" y="%d" width="360" '
             'height="60" rx="30" stroke="%s" stroke-width="2.5"/>' % (_SCX - 180, _SCY + 172, AC))
    o.append(txt(_SCX, _SCY + 210, "屏蔽 95% 干扰", "ttl", size=26, anchor="middle", col=AC, weight=700))
    o.append(legend(0, 486, [("solid", "目标人声"), ("dot", "干扰 · 被屏蔽")]))
    return "".join(o)
page("content", "".join([
    head("SELECTIVE ATTENTION (SAL) · 选择性注意力锁定", "嘈杂环境里，<strong>只听该听的人</strong>。"),
    lab(120, 236, "01 · LOCK ON"),
    figbox(120, 285, 1680, 1680, 500, _sal_fig(), i=1),
    rule(850),
    rail("SELECTIVE ATTENTION LOCK · 95% INTERFERENCE SHIELDED"),
]))

# ═══ P11 · 弱网 ·「网络在抖，对话不断」══════════════════════════════════════
# 2026-08-20 三轮升维：一条丢包条 + 一条波浪 → 上下两条对齐的时间带。
#   上带 = 网络状况（正常 → 80% 丢包高密段 → 3–5s 瞬时断网空洞段 → 恢复），
#   下带 = 对话连续性（一条永不中断的音频带，在上带最恶劣区间下方依然连续），
#   两带之间坐着唯一 hot 件「抗丢包引擎」：上面吸收锯齿，下面吐出平滑。
#   数字只用现有两枚 stat（80% / 3–5s），不发明第三个。
_WN_SEGS = [(0, 9, 1), (256, 10, 8), (536, 6, 6), (716, 12, 1)]   # (x0, 包数, 丢包数)
def _weaknet_fig():
    o = [txt(0, 24, "网络 · 大量丢包 + 瞬时断网", "lbl", size=15)]
    # 最恶劣区间的竖向对照带：上带最烂的地方，正对着下带最平的地方
    o.append('<rect class="pop" style="--i:1;fill:%s;opacity:.06" x="252" y="36" width="428" '
             'height="330" rx="6"/>' % AD)
    for x0, n, lost in _WN_SEGS:
        for k in range(n):
            x = x0 + k * 28
            if k < n - lost:
                o.append('<rect class="pop" style="--i:%d;fill:%s" x="%d" y="44" width="22" '
                         'height="60" rx="5"/>' % (1 + k % 3, AC, x))
            else:
                o.append('<rect class="pop" style="--i:%d" x="%d" y="44" width="22" height="60" '
                         'rx="5" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 4"/>'
                         % (1 + k % 3, x, HS))
    o.append(txt(382, 128, "80% 丢包", "ttl", size=20, anchor="middle", col=AD, weight=700))
    o.append(txt(606, 128, "3–5s 瞬时断网", "ttl", size=20, anchor="middle", col=AD, weight=700))
    o.append(txt(606, 84, "✕ 断网", "ttl", size=20, anchor="middle", col=AD))
    # ── 吸收：整段坏区收进来（点线漏斗）+ 一段锯齿 = 网络给的是什么样的东西 ──
    for k in range(7):
        x = 400 + k * 42
        o.append(dline("M%d 142 L%d 164" % (x, 540 + (x - 526) // 5), AD, 1.6, 2, dash="3 5"))
    _saw = " ".join("L%d %d" % (470 + k * 10, 168 if k % 2 == 0 else 184) for k in range(16))
    o.append('<path class="pop" style="--i:2" d="M462 176 %s" fill="none" stroke="%s" '
             'stroke-width="2" stroke-linejoin="round"/>' % (_saw, AD))
    o.append(box(370, 194, 340, 76, 10, hot=True, i=3))
    o.append(txt(540, 242, "抗丢包引擎", "ttl", size=26, anchor="middle", col=AC))
    # ── 输出：一段平滑波 = 引擎吐出来的是什么样的东西 ──
    o.append('<path class="pop" style="--i:4" d="M460 292 Q 480 280 500 292 T 540 292 T 580 292 '
             'T 620 292" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % AC)
    o.append(vline(540, 302, 334, AC, 2.5, 4))
    o.append(ah_d(540, 348, AC))
    # ── 下带：一条连续不断的音频带，横贯全程 ──
    o.append(txt(0, 344, "对话 · 连续不卡顿", "ttl", size=21, col=AC))
    o.append('<rect class="pop" style="--i:5;fill:%s;opacity:.14" x="0" y="358" width="1060" '
             'height="56" rx="8"/>' % AC)
    o.append('<path class="dw" style="--len:1200;--i:5" d="M12 386 Q 72 356 132 386 T 252 386 '
             'T 372 386 T 492 386 T 612 386 T 732 386 T 852 386 T 972 386 T 1044 386" fill="none" '
             'stroke="%s" stroke-width="4" stroke-linecap="round"/>' % AC)
    o.append('<circle class="pop" style="--i:6;fill:%s" cx="1048" cy="386" r="7"/>' % AC)
    o.append(legend(0, 442, [("solid", "对话音频流"), ("dash", "丢包 / 断网")]))
    return "".join(o)
_P7STAT = [("80", "%", "丢包率下稳定对话"), ("3–5", "s", "瞬时断网自如响应")]
page("content", "".join([
    head("WEAK NETWORK · 弱网也能聊", "网络在抖，<strong>对话不断</strong>。"),
    lab(120, 236, "01 · PACKET LOSS"),
    figbox(120, 280, 1080, 1080, 470, _weaknet_fig(), i=1),
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
    sh("flow mono-sm", "left:1150px;top:1010px;width:650px;height:24px;text-align:right;--i:7",
       "SOURCE · 声网官网 · 引擎发版说明 公开口径 · 典型值 · 事实截止 2026.08"),
]))

# ═══ P12 · 多模态 ·「看得见、认得人的多模态对话」════════════════════════════
_CAPS = [
    ("VOICEPRINT", "声纹锁定", "认准说话人"),
    ("VISION",     "看图识景", "理解图片视频"),
    ("AVATAR",     "数字人",   "口型表情同步"),
    ("SIP",        "SIP 电话", "接呼叫中心"),
]
# 2026-08-20 三轮升维：hub + 四张并排卡 → 一个有方向的 IO 辐条图。
#   四张能力卡文案一字不改，只是从「一排卡」变成「辐条端点卡」，并按 IO 方向分域：
#     左 = 感知 · IN（箭头指向 hub）／右 = 表达 · OUT（箭头离开 hub）／底 = 接入通道（双向）
#   这是视觉分组，不改任何产品分类文案。hot 件唯一 = 中心 hub。
def _p12_card(x, y, w, h, tag, name, desc, i=2):
    o = [box(x, y, w, h, 10, i=i)]
    if tag:
        o.append(txt(x + 26, y + 34, tag, "lbl", size=13))
    o.append(txt(x + 26, y + (72 if tag else 50), name, "ttl", size=26))
    if desc:
        o.append(txt(x + 26, y + 106, desc, "sm", size=18))
    return "".join(o)
def _io_fig():
    o = []
    # ── 中心 hub（hot）──
    o.append(box(630, 180, 420, 140, 14, hot=True, i=1))
    o.append(txt(840, 240, "对话引擎", "ttl", size=38, anchor="middle"))
    o.append(txt(840, 282, "一套接入", "sm", size=18, anchor="middle", col=AC, mono=True, ls=".16em"))
    # ── 左：感知 · IN ──
    o.append(txt(40, 34, "感知 · IN", "sm", size=15, col=AC, mono=True, ls=".18em"))
    o.append(_p12_card(40, 60, 390, 130, *_CAPS[0], i=2))
    o.append(_p12_card(40, 230, 390, 130, *_CAPS[1], i=3))
    for cy, hy in [(125, 205), (295, 275)]:
        o.append('<path class="dw" style="--len:300;--i:3" d="M430 %d H540 V%d H606" fill="none" '
                 'stroke="%s" stroke-width="2.5"/>' % (cy, hy, AC))
        o.append(ah_r(618, hy, AC))
    # ── 右：表达 · OUT ──
    o.append(txt(1640, 34, "表达 · OUT", "sm", size=15, col=AC, anchor="end", mono=True, ls=".18em"))
    o.append(_p12_card(1250, 82, 390, 86, "", "语音", "", i=2))
    o.append(_p12_card(1250, 230, 390, 130, *_CAPS[2], i=3))
    for cy, hy in [(125, 205), (295, 275)]:
        o.append('<path class="dw" style="--len:300;--i:4" d="M1050 %d H1160 V%d H1238" '
                 'fill="none" stroke="%s" stroke-width="2.5"/>' % (hy, cy, AC))
        o.append(ah_r(1250, cy, AC))
    # ── 底：接入通道（双向）──
    o.append(_p12_card(630, 400, 420, 130, *_CAPS[3], i=5))
    o.append(txt(1080, 462, "接入通道", "sm", size=15, col=AC, mono=True, ls=".18em"))
    o.append(vline(840, 334, 386, AC, 2.5, 5))
    o.append(ah_d(840, 398, AC)); o.append(ah_u(840, 322, AC))
    o.append(legend(0, 548, [("solid", "主数据流 · 单向 / 双向")]))
    return "".join(o)
page("content", "".join([
    head("BEYOND VOICE · 不止于听清", "看得见、认得人的<strong>多模态对话</strong>。"),
    lab(120, 236, "01 · ONE ENGINE, FOUR SENSES"),
    figbox(120, 276, 1680, 1680, 560, _io_fig(), i=1),
    rule(850),
    land("同一套引擎，语音、视觉、声纹、电话一并接入——对话不再只是“听和说”。"),
]))

# ═══ P13 · 开放编排 ·「你的模型自由组合，引擎负责编排」══════════════════════
_MODELS = ["ASR 语音识别", "LLM 大模型", "TTS 语音合成", "数字人"]
_ADDONS = ["视觉理解", "知识库 · RAG"]   # 产品口径：知识库 RAG 是一项能力，不拆
# 2026-08-20 三轮升维：两列盒子 + 曲线 → 一台「插槽机」。
#   每个模型不再是一只盒子，而是「槽框 + 可拔出的模块块 + ⇄ 换装箭头」——一眼看出可插拔；
#   槽列下方一道集体括号标「可替换 · 可兜底 · 可热切换」（convoai-info P4 既有 chip 原文）；
#   右列两个高阶能力走虚线槽框 = 按需叠加；底部一条小流程带收在「实时调试 → 一键发布」。
def _slot(x, y, w, h, name, i=1, dashed=False):
    """插槽：外槽框（可虚线）+ 内模块块 + 右侧 ⇄ 换装箭头"""
    o = [box(x, y, w, h, 8, dashed=dashed, i=i)]
    o.append('<rect class="pop" style="--i:%d;fill:var(--card-bg-2)" x="%d" y="%d" width="%d" '
             'height="%d" rx="6" stroke="%s" stroke-width="1.4"/>'
             % (i, x + 14, y + 12, w - 80, h - 24, HS))
    o.append(txt(x + 14 + (w - 80) // 2, y + h // 2 + 8, name, "ttl", size=22, anchor="middle"))
    sx, cy = x + w - 58, y + h // 2
    o.append(hline(sx, sx + 22, cy - 8, AC, 1.6, i)); o.append(ah_r(sx + 30, cy - 8, AC, 6))
    o.append(hline(sx + 30, sx + 8, cy + 8, AC, 1.6, i)); o.append(ah_l(sx, cy + 8, AC, 6))
    return "".join(o)
def _orch_fig():
    o = [txt(250, 26, "可自由替换 · 模型层", "lbl", size=16, anchor="middle", col=AC),
         txt(1430, 26, "按需叠加 · 高阶能力", "lbl", size=16, anchor="middle", col=AC)]
    for i, n in enumerate(_MODELS):
        y = 56 + i * 112
        o.append(_slot(60, y, 380, 72, n, i=i + 1))
        o.append('<path class="dw" style="--len:230;--i:%d" d="M452 %d C 540 %d, 540 260, 604 260" '
                 'fill="none" stroke="%s" stroke-width="2" opacity=".55"/>' % (i + 2, y + 36, y + 36, AC))
    o.append(ah_r(616, 260, AC))
    # 集体括号：四个槽共享的一条产品承诺
    o.append(hline(60, 440, 480, AC, 2, 6))
    o.append(vline(60, 468, 480, AC, 2, 6)); o.append(vline(440, 468, 480, AC, 2, 6))
    o.append(txt(250, 508, "可替换 · 可兜底 · 可热切换", "sm", size=18, anchor="middle", col=AC,
                 weight=700))
    # 中枢（唯一 hot 件）
    o.append(box(620, 180, 440, 160, 16, hot=True, i=0))
    o.append(txt(840, 250, "对话引擎", "ttl", size=36, anchor="middle", col=AC))
    o.append(txt(840, 296, "实时编排", "txt", size=21, anchor="middle"))
    for i, n in enumerate(_ADDONS):
        y = 168 + i * 128
        o.append(_slot(1240, y, 380, 72, n, i=i + 3, dashed=True))
        o.append('<path class="dw" style="--len:230;--i:%d" d="M1060 260 C 1140 260, 1140 %d, 1228 %d" '
                 'fill="none" stroke="%s" stroke-width="2" opacity=".55"/>' % (i + 3, y + 36, y + 36, AC))
        o.append(ah_r(1240, y + 36, AC))
    # 底部小流程带
    o.append(vline(840, 348, 384, AC, 2, 6)); o.append(ah_d(840, 396, AC))
    o.append('<rect class="pop" style="--i:7;fill:var(--card-bg-2)" x="620" y="400" width="440" '
             'height="60" rx="30" stroke="%s" stroke-width="1.4"/>' % HS)
    o.append(txt(840, 438, "实时调试 &#8594; 一键发布", "ttl", size=22, anchor="middle"))
    o.append(legend(0, 530, [("solid", "主数据流"), ("dash", "按需叠加")]))
    return "".join(o)
page("content", "".join([
    head("OPEN & FLEXIBLE · 灵活扩展", "你的模型自由组合，<strong>引擎负责编排</strong>。"),
    lab(120, 236, "01 · ORCHESTRATION"),
    figbox(120, 272, 1680, 1680, 545, _orch_fig(), i=1),
    rule(850),
    land("快速编排 ASR / LLM / TTS / 数字人与语音体验，实时调试、一键发布智能体。"),
]))

# ═══ P14 · 接入架构 ·「2 行代码，三方协同即可上线」═════════════════════════
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
    o.append(step_badge(530, 58, 1, i=2))
    # ② 创建 / 控制智能体（客户服务器 → 引擎 · 虚线 REST 控制面）
    #   起点 x890 与 ① 的落点 x790 同在服务器盒顶：一收一发，服务器是这一步的枢纽
    o.append(dline("M890 120 V58 H1410 V110", HS, 2, 3, dash="6 6"))
    o.append(ah_d(1410, 118, "var(--ink-3)", 6))
    o.append(txt(1150, 32, "创建 / 控制智能体", "sm", size=18, anchor="middle"))
    o.append(step_badge(1150, 58, 2, i=3))
    # ③ 实时音视频流（终端 ⇄ 引擎 · 实线双向 · 粗一档）—— 建立在 ①② 之后，所以走盒底
    o.append('<path class="dw" style="--len:1228;--i:4" d="M270 434 V478 H1410 V434" '
             'fill="none" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/>' % AC)
    o.append(ah_u(270, 424, AC))
    o.append(ah_u(1410, 424, AC))
    o.append(txt(840, 452, "实时音视频流", "ttl", size=19, anchor="middle", col=AC, weight=700))
    o.append(step_badge(840, 478, 3, i=5))
    o.append('</g>')
    return "".join(o)
page("content", "".join([
    head("ARCHITECTURE · 接入架构", "<strong>2 行代码</strong>，三方协同即可上线。"),
    lab(120, 236, "01 · THREE PARTIES"),
    # viewBox 556→578、盒顶 280→266：③ 的盒底跑道要在「三盒底缘 / 域底标 / 图例」之间
    # 各留出 10px 以上的呼吸（原 556 里只剩 6px，徽标贴着域底标）。
    # 盒底 266+578=844，仍压在 rule(850) 之上，不碰收口线。
    figbox(120, 266, 1680, 1680, 578, _arch_fig(), i=1),
    rule(850),
    land("终端只管采集与播放，密钥与业务逻辑留在你的服务器——2 行代码、15 分钟即可跑通，安全可控、上线快。"),
]), steps=1)

# ═══ P15 · 典型场景 ·「一套引擎，支撑多类场景」════════════════════════════
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

# ═══ P16 · Why Agora ·「跑在声网实时互动底座之上」═════════════════════════
#   数据修正页：四数字与 note / SOURCE 全部与 31 页拜访版 P2 一字对齐。
#   2026-08-20 扩页时整块原样搬运（页号 12 → 15），内容一字未动。
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
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px;--i:7",
       "SOURCE · 声网官网 / IR 公开口径 · IDC 中国视频云市场报告 · 事实截止 2026.08"),
]))

# ═══ P17 · 收尾（title 板）═══════════════════════════════════════════════
page("title", "".join([
    sh("ink", "left:120px;top:320px;width:1560px;height:250px;"
       "font:700 96px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "最好的对话式 AI，<br>让人<strong style='color:var(--accent)'>忘了它是 AI</strong>。"),
    sh("spread", "left:120px;top:626px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow sub", "left:120px;top:678px;width:1500px;height:48px;--i:4",
       "低延时、可打断、听得清、看得见——把技术藏进体验里。"),
    # CTA：纯文本 mono 行，不做假链接样式（没有 <a>，不加下划线/悬停态）
    sh("flow mono-sm", "left:120px;top:790px;width:1500px;height:24px;--i:5",
       "DEMO / 文档 · agora.io › 对话式 AI 引擎 · 联系团队"),
    sh("flow mono-sm", "left:120px;top:930px;width:1400px;height:24px;--i:6",
       "仅供方案交流参考"),
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
        '<title>声网 · 对话式 AI 引擎 · 产品介绍</title>\n'
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
        '<style>.deck-swap{position:fixed;left:26px;bottom:24px;z-index:1100;font-family:var(--f-mono,monospace);'
        'font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);'
        'border-radius:3px;padding:7px 12px;opacity:0;transition:opacity .3s;background:transparent;cursor:pointer;}'
        '.deck-swap:hover,.deck-swap:focus-visible{opacity:.9;color:var(--accent);border-color:var(--accent);}'
        '.deck-swap:focus:not(:focus-visible){outline:none;box-shadow:none;}'
        '@media (hover:none){.deck-swap{opacity:.4;}}'
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
        "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")
    OUT_ALIAS.write_text(doc, encoding="utf-8")
    assert total == 17, "页数漂移：%d != 17" % total
    assert doc.count("<section") == 17, "section 数漂移：%d" % doc.count("<section")
    steps_map = {i: s for i, (_b, s, _y) in enumerate(PAGES, 1) if s}
    assert steps_map == {6: 1, 7: 1, 14: 1}, "分步页漂移：%r" % steps_map
    print("convoai.html + convoai-engine.html（双生） · %d 页 · %dKB · conf-light 默认 · 分步 %r"
          % (total, len(doc) // 1024, steps_map))

if __name__ == "__main__":
    build()
