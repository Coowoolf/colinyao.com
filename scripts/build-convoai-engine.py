#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-engine.py ·《声网 · 对话式 AI 引擎 · 产品介绍》13 页
# CONF 家族 · conf-light 默认 · 单文件双主题 —— 以 build-convoai-info.py 为母版克隆
#   （同一套 DECK_CSS token / conf-light·dark 背景板 / deck.js 运行时 / noindex / 双主题）
#
# 这份 deck 是 convoai-info P4「引擎产品详解」抽屉的内容（iframe 载入）。
# 2026-08-18 重建：旧版是 Apple 风格 13 页横滚（git 历史里可回溯），
# 内容 1:1 移植、版式用家族语法重绘，只有 P12 的数字口径按 Colin 指错做了修正。
#
# 结构（13 页 · 全部 data-steps=0，讲者不分步）：
#   P1  封面（title 板）        P2  实时决策        P3  三件极致
#   P4  实时语音链路            P5  优雅打断        P6  SAL 选择性注意力
#   P7  弱网                    P8  多模态          P9  开放编排
#   P10 接入架构                P11 典型场景        P12 Why Agora（数据修正）
#   P13 收尾（title 板）
#
# ── P12 数据口径（Colin 2026-08-18 指错，改为 31p 拜访版 P2 的锁定口径，一字对齐）──
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

def lab(x, y, txt, w=680, col=None, i=0):
    """mono 小节标：「01 · SIGNAL PATH」"""
    c = ";color:%s" % col if col else ""
    return sh("flow seclab", "left:%dpx;top:%dpx;width:%dpx;height:20px;--i:%d%s" % (x, y, w, i, c), txt)

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

def txt(x, y, s, cls="txt", size=None, anchor=None, col=None, weight=None, i=None):
    st = []
    if size:   st.append("font-size:%dpx" % size)
    if col:    st.append("fill:%s" % col)
    if weight: st.append("font-weight:%d" % weight)
    a = ' text-anchor="%s"' % anchor if anchor else ""
    g = ' class="%s"' % cls if cls else ""
    sty = ' style="%s"' % ";".join(st) if st else ""
    return '<text%s x="%d" y="%d"%s%s>%s</text>' % (g, x, y, a, sty, s)

PAGES = []          # (board, body_html)
def page(board, body):
    PAGES.append((board, body))

AC = "var(--accent)"
AD = "var(--accent-deep)"
HS = "var(--hair-strong)"

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
#   01 FOUR MOVES 四步卡 / 02 SAME MOMENT 边听边说双轨图 / land
_MOVES4 = [
    ("01", "听清 · 认人 · 懂内容",       "分离目标人声、识别说话人，同时理解在说什么"),
    ("02", "带入对象、场景与情绪",       "结合上下文理解言外之意，而不只是逐字转写"),
    ("03", "持续判断：继续听，还是开口", "实时权衡时机，不必等一句话彻底说完"),
    ("04", "边说边听，灵活调整节奏",     "表达的同时仍在倾听，随时被打断、随时接上"),
]
# 双轨图：上轨「持续在听」向右汇入判断框，下轨「同时在说」从判断框流回 —— 同一时刻两件事
_P2FIG = "".join([
    txt(10, 70, "持续在听", "ttl", size=21, col=AC),
    txt(10, 158, "同时在说", "ttl", size=21, col="var(--ink-2)"),
    hline(210, 1382, 62, AC, 2, 1), ah_r(1390, 62, AC),
    txt(430, 40, "听清 · 认人", "sm", size=17, anchor="middle"),
    txt(900, 40, "对象 · 场景 · 情绪", "sm", size=17, anchor="middle"),
    hline(1382, 210, 150, HS, 2, 2), ah_l(202, 150, "var(--ink-3)"),
    txt(430, 182, "开口表达", "sm", size=17, anchor="middle"),
    txt(900, 182, "控制节奏", "sm", size=17, anchor="middle"),
    box(1418, 30, 252, 152, 8, hot=True, i=3),
    txt(1544, 92, "判断", "ttl", size=24, anchor="middle", col=AC),
    txt(1544, 130, "何时开口", "sm", size=18, anchor="middle"),
])
page("content", "".join([
    head("REAL-TIME DECISION · 边听边说", "对话，是一个<strong>实时决策</strong>的过程。"),
    lab(120, 236, "01 · FOUR MOVES · 同一时刻发生"),
    sh("", "left:120px;top:272px;width:1680px;height:250px",
       '<div class="g4" style="height:100%">' + "".join(
           '<div class="card rise" style="--i:%d;justify-content:center">'
           '<div class="n" style="font-size:34px">%s</div>'
           '<div class="t" style="font-size:24px">%s</div>'
           '<div class="d" style="font-size:18px">%s</div></div>'
           % (2 + _i, _no, _n, _d)
           for _i, (_no, _n, _d) in enumerate(_MOVES4)) + '</div>'),
    lab(120, 588, "02 · SAME MOMENT · 边说边听"),
    figbox(120, 620, 1680, 1680, 200, _P2FIG, i=3),
    rule(850),
    land("自然对话不是“听完再回答”，而是边说边听、持续判断——这正是引擎要还原的能力。"),
]))

# ═══ P3 · 三件极致 ·「把三件事，做到极致」══════════════════════════════════
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
    rail("END-TO-END 650MS · BARGE-IN 340MS · NOISE SHIELD 95%"),
]))

# ═══ P4 · 实时语音链路 ·「一条深度优化的端到端链路」════════════════════════
_PIPE = [
    # hot 落 AI-VAD：链路里唯一声网自研差异化环节；LLM 是可替换第三方件，高亮它=错误的强调声明
    ("AI-VAD", "智能人声检测", "判断谁在说", True,  False),
    ("ASR",    "语音转写",     "听清说什么", False, False),
    ("LLM",    "大模型理解",   "想怎么答",   False, False),
    ("TTS",    "语音合成",     "开口说话",   False, False),
    ("数字人", "口型 / 表情",  "可选",       False, True),
]
def _p4():
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
    # 五个环节
    for i, (n, sub, foot, hot, dashed) in enumerate(_PIPE):
        x = 180 + i * 266
        cx = x + 110
        o.append(box(x, 120, 220, 130, 6, hot=hot, dashed=dashed, i=i + 1))
        o.append(txt(cx, 178, n, "ttl", size=26, anchor="middle",
                     col=AC if hot else None))
        o.append(txt(cx, 214, sub, "sm", size=17, anchor="middle"))
        o.append(txt(cx, 290, foot, "lbl", size=15, anchor="middle"))
    # 连接箭头
    for x1, x2, k in [(118, 172, 0), (406, 440, 1), (672, 706, 2), (938, 972, 3),
                      (1204, 1238, 4), (1470, 1558, 5)]:
        o.append(hline(x1, x2 - 9, 185, HS, 2, k))
        o.append(ah_r(x2, 185, "var(--ink-3)"))
    # 端到端跨度标注（文字在线上方，绝不压线）
    o.append(txt(840, 372, "端到端 650ms", "ttl", size=28, anchor="middle", col=AC, weight=700))
    o.append(dline("M70 400 H1610", AC, 1.6, 6, dash="3 8"))
    o.append(vline(70, 390, 410, AC, 1.6, 6))
    o.append(vline(1610, 390, 410, AC, 1.6, 6))
    return "".join(o)
page("content", "".join([
    head("PIPELINE · 实时语音链路", "一条深度优化的<strong>端到端链路</strong>。"),
    lab(120, 236, "01 · SIGNAL PATH"),
    figbox(120, 290, 1680, 1680, 430, _p4(), i=1),
    rule(850),
    land("AI-VAD、ASR、LLM、TTS 逐环节协同优化——用户体感是一句接一句，几乎无等待。"),
]))

# ═══ P5 · 优雅打断 ·「想插话就插话，340ms 即时收声」════════════════════════
def _bars(x0, n, cy, col, seed=0, gap=17, w=8, op=None):
    hs = [30, 54, 16, 66, 38, 22, 58, 34, 46, 18, 50, 26, 40, 14, 62, 30, 44, 20, 56, 36]
    o = []
    for i in range(n):
        h = hs[(i + seed) % len(hs)]
        o.append('<rect class="pop" style="--i:%d;fill:%s%s" x="%d" y="%d" width="%d" height="%d" rx="%d"/>'
                 % (1 + i % 4, col, (";opacity:%s" % op) if op else "", x0 + i * gap, cy - h // 2, w, h, w // 2))
    return "".join(o)
_P5FIG = "".join([
    txt(10, 118, "智能体", "ttl", size=22, col=AC),
    txt(10, 318, "用户", "ttl", size=22, col="var(--ink-2)"),
    _bars(170, 34, 110, AC),
    _bars(820, 7, 110, "var(--ink-3)", seed=11, op=".45"),
    dline("M800 40 V350", AD, 2, 1, dash="6 6"),
    txt(812, 32, "用户插话", "sm", size=18, col=AD, weight=700),
    dline("M960 40 V350", AC, 2, 2, dash="6 6"),
    txt(972, 32, "智能体收声", "sm", size=18, col=AC, weight=700),
    _bars(990, 38, 310, "var(--ink-2)", seed=3),
    # 340ms 跨度：文字在括线上方
    txt(880, 358, "340ms", "ttl", size=24, anchor="middle", col=AC, weight=700),
    hline(800, 960, 380, AC, 2, 3),
    vline(800, 372, 388, AC, 2, 3),
    vline(960, 372, 388, AC, 2, 3),
])
page("content", "".join([
    head("INTERRUPTION · 优雅打断", "想插话就插话，<strong>340ms 即时收声</strong>。"),
    lab(120, 236, "01 · TIMELINE"),
    figbox(120, 285, 1680, 1680, 420, _P5FIG, i=1),
    lab(120, 742, "02 · WHAT HAPPENS"),
    sh("rise", "left:120px;top:774px;width:1680px;height:54px;--i:4",
       "".join('<span class="chip">%s</span>' % t for t in
               ["智能体正在说话", "用户随时可插话", "340ms 内即时收声、转为倾听"])),
    rule(850),
    land("对话像真人一样你来我往。"),
]))

# ═══ P6 · SAL ·「嘈杂环境里，只听该听的人」═══════════════════════════════
_NOISE = [("旁人交谈", 90), ("环境噪声", 210), ("背景音乐", 330)]
_P6FIG = "".join(
    # 目标人声（左）
    ['<circle class="pop box" style="--i:1" cx="180" cy="210" r="72" stroke-width="2"/>',
     '<path class="pop" style="--i:1" d="M180 182a12 12 0 0 1 12 12v10a12 12 0 0 1-24 0v-10a12 12 0 0 1 12-12z '
     'M163 204a17 17 0 0 0 34 0 M180 221v11" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % AC,
     txt(180, 330, "目标人声", "ttl", size=22, anchor="middle", col=AC),
     txt(180, 362, "锁定 · 精准识别", "sm", size=17, anchor="middle"),
     hline(258, 660, 210, AC, 3, 2), ah_r(672, 210, AC),
     # 引擎（中）
     '<circle class="pop" style="--i:0;fill:var(--card-bg-2);stroke:%s" cx="780" cy="210" r="100" stroke-width="3"/>' % AC,
     txt(780, 202, "智能体", "ttl", size=28, anchor="middle"),
     txt(780, 240, "声纹锁定", "sm", size=18, anchor="middle", col=AC),
     # 屏蔽墙
     dline("M978 60 V360", AC, 2.5, 3, dash="10 9"),
     ] + [
    # 三路干扰
    x for n, cy in _NOISE for x in (
        '<circle class="pop box" style="--i:4" cx="1400" cy="%d" r="52" stroke-width="1.4"/>' % cy,
        txt(1400, cy + 10, "✕", "ttl", size=30, anchor="middle", col="var(--ink-3)"),
        txt(1478, cy + 8, n, "sm", size=19),
        dline("M1346 %d H990" % cy, HS, 2, 5),
    )] + [
    # 结论徽标
    box(600, 402, 360, 62, 31, hot=True, i=6),
    txt(780, 442, "屏蔽 95% 干扰", "ttl", size=26, anchor="middle", col=AC, weight=700),
])
page("content", "".join([
    head("SELECTIVE ATTENTION (SAL) · 选择性注意力锁定", "嘈杂环境里，<strong>只听该听的人</strong>。"),
    lab(120, 236, "01 · LOCK ON"),
    figbox(120, 285, 1680, 1680, 500, _P6FIG, i=1),
    rule(850),
    rail("SELECTIVE ATTENTION LOCK · 95% INTERFERENCE SHIELDED"),
]))

# ═══ P7 · 弱网 ·「网络在抖，对话不断」══════════════════════════════════════
def _p7():
    o = [txt(10, 40, "网络 · 大量丢包 + 瞬时断网", "lbl", size=15)]
    got = {0, 6, 12, 16}
    for i in range(20):
        x = 20 + i * 52
        if i in got:
            o.append('<rect class="pop" style="--i:%d;fill:%s" x="%d" y="64" width="34" height="44" rx="6"/>'
                     % (1 + i % 3, AC, x))
        else:
            o.append('<rect class="pop" style="--i:%d" x="%d" y="64" width="34" height="44" rx="6" '
                     'fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 4"/>' % (1 + i % 3, x, HS))
    o += [
        txt(540, 146, "✕ 断网", "sm", size=17, anchor="middle", col=AD, weight=700),
        vline(540, 166, 196, AC, 2, 2), ah_d(540, 206, AC),
        box(370, 216, 340, 76, 10, hot=True, i=3),
        txt(540, 264, "抗丢包引擎", "ttl", size=26, anchor="middle", col=AC),
        vline(540, 300, 330, AC, 2, 4), ah_d(540, 340, AC),
        txt(10, 386, "对话 · 连续不卡顿", "ttl", size=21, col=AC),
        '<path class="dw" style="--len:1100;--i:5" d="M20 428 Q 80 392 140 428 T 260 428 T 380 428 T 500 428 '
        'T 620 428 T 740 428 T 860 428 T 980 428 T 1040 428" fill="none" stroke="%s" stroke-width="4" '
        'stroke-linecap="round"/>' % AC,
        '<circle class="pop" style="--i:6;fill:%s" cx="1044" cy="428" r="7"/>' % AC,
    ]
    return "".join(o)
_P7STAT = [("80", "%", "丢包率下稳定对话"), ("3–5", "s", "瞬时断网自如响应")]
page("content", "".join([
    head("WEAK NETWORK · 弱网也能聊", "网络在抖，<strong>对话不断</strong>。"),
    lab(120, 236, "01 · PACKET LOSS"),
    figbox(120, 280, 1080, 1080, 470, _p7(), i=1),
    lab(1280, 236, "02 · RESILIENCE"),
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
    land("极端弱网、瞬时断网也不掉线——移动、车载、户外场景，对话依旧顺畅。"),
]))

# ═══ P8 · 多模态 ·「看得见、认得人的多模态对话」════════════════════════════
_CAPS = [
    ("VOICEPRINT", "声纹锁定", "认准说话人"),
    ("VISION",     "看图识景", "理解图片视频"),
    ("AVATAR",     "数字人",   "口型表情同步"),
    ("SIP",        "SIP 电话", "接呼叫中心"),
]
# 从中心 hub 扇出到四列卡片的正交母线（比贝塞尔曲线更 editorial，也更好读）
_P8CX = [202, 627, 1052, 1477]
_P8FAN = "".join(
    [vline(840, 0, 42, AC, 2, 1), hline(_P8CX[0], _P8CX[-1], 42, AC, 2, 2)]
    + [vline(cx, 42, 88, AC, 2, 3) for cx in _P8CX]
    + [ah_d(cx, 96, AC, 7) for cx in _P8CX])
page("content", "".join([
    head("BEYOND VOICE · 不止于听清", "看得见、认得人的<strong>多模态对话</strong>。"),
    lab(120, 236, "01 · ONE ENGINE, FOUR SENSES"),
    sh("rise card-c on", "left:660px;top:284px;width:600px;height:130px;--i:1",
       '<div style="height:100%;display:flex;align-items:center;justify-content:center;gap:24px">'
       '<div style="font:700 38px/1.2 var(--f-cn);color:var(--ink)">对话引擎</div>'
       '<div style="width:1px;height:38px;background:var(--hair)"></div>'
       '<div style="font:500 18px/1 var(--f-mono);letter-spacing:.16em;color:var(--accent)">一套接入</div></div>'),
    figbox(120, 424, 1680, 1680, 100, _P8FAN, i=2),
    sh("", "left:120px;top:534px;width:1680px;height:250px",
       '<div class="g4" style="height:100%">' + "".join(
           '<div class="card rise" style="--i:%d;justify-content:center"><div class="tag">%s</div>'
           '<div class="t" style="font-size:26px">%s</div>'
           '<div class="d" style="font-size:18px">%s</div></div>'
           % (3 + _i, _t, _n, _d)
           for _i, (_t, _n, _d) in enumerate(_CAPS)) + '</div>'),
    rule(850),
    land("同一套引擎，语音、视觉、声纹、电话一并接入——对话不再只是“听和说”。"),
]))

# ═══ P9 · 开放编排 ·「你的模型自由组合，引擎负责编排」══════════════════════
_MODELS = ["ASR 语音识别", "LLM 大模型", "TTS 语音合成", "数字人"]
_ADDONS = ["视觉理解", "知识库 · RAG"]   # 产品口径：知识库 RAG 是一项能力，不拆
def _p9():
    o = [txt(230, 32, "可自由替换 · 模型层", "lbl", size=16, anchor="middle", col=AC),
         txt(1450, 32, "按需叠加 · 高阶能力", "lbl", size=16, anchor="middle", col=AC)]
    for i, n in enumerate(_MODELS):
        y = 70 + i * 98
        o.append(box(40, y, 380, 70, 8, i=i + 1))
        o.append(txt(230, y + 44, n, "ttl", size=22, anchor="middle"))
        o.append('<path class="dw" style="--len:230;--i:%d" d="M420 %d C 530 %d, 530 240, 620 240" '
                 'fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % (i + 2, y + 35, y + 35, AC))
    o.append(box(620, 140, 440, 200, 16, hot=True, i=0))
    o.append(txt(840, 218, "对话引擎", "ttl", size=36, anchor="middle", col=AC))
    o.append(txt(840, 262, "实时编排", "txt", size=21, anchor="middle"))
    o.append(txt(840, 300, "调试 · 一键发布", "sm", size=18, anchor="middle"))
    for i, n in enumerate(_ADDONS):
        y = 120 + i * 98
        o.append(box(1260, y, 380, 70, 8, i=i + 3))
        o.append(txt(1450, y + 44, n, "ttl", size=22, anchor="middle"))
        o.append('<path class="dw" style="--len:230;--i:%d" d="M1060 240 C 1150 240, 1150 %d, 1260 %d" '
                 'fill="none" stroke="%s" stroke-width="2" opacity=".5"/>' % (i + 3, y + 35, y + 35, AC))
    return "".join(o)
page("content", "".join([
    head("OPEN & FLEXIBLE · 灵活扩展", "你的模型自由组合，<strong>引擎负责编排</strong>。"),
    lab(120, 236, "01 · ORCHESTRATION"),
    figbox(120, 290, 1680, 1680, 480, _p9(), i=1),
    rule(850),
    land("快速编排 ASR / LLM / TTS / 数字人与语音体验，实时调试、一键发布智能体。"),
]))

# ═══ P10 · 接入架构 ·「2 行代码，三方协同即可上线」═════════════════════════
def _p10():
    o = []
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
    # 连线：终端 ⇄ 引擎（实时音视频流，走顶弧）
    o.append(txt(840, 46, "实时音视频流", "sm", size=19, anchor="middle", col=AC, weight=700))
    o.append('<path class="dw" style="--len:1500;--i:2" d="M512 180 C 600 180, 620 68, 840 68 '
             'C 1060 68, 1080 180, 1168 180" fill="none" stroke="%s" stroke-width="2.5"/>' % AC)
    o.append(ah_r(1176, 180, AC))
    o.append(ah_l(504, 180, AC))
    # 连线：终端 ⇄ 服务器（取 Token）· 不能用 .lbl —— 它带 text-transform:uppercase，
    # 会把「取 Token」烧成「取 TOKEN」，与原稿不符
    o.append(txt(555, 258, "取 Token", "sm", size=15, anchor="middle", col="var(--ink-3)"))
    o.append(hline(514, 596, 286, HS, 2, 3))
    o.append(ah_r(606, 286, "var(--ink-3)"))
    o.append(ah_l(504, 286, "var(--ink-3)"))
    # 连线：服务器 → 引擎（服务端签名 · 创建智能体）
    o.append(txt(1320, 446, "服务端签名 · 创建智能体", "sm", size=17, anchor="middle"))
    o.append(hline(1070, 1548, 470, AC, 2, 4))
    o.append(ah_r(1560, 470, AC))
    return "".join(o)
page("content", "".join([
    head("ARCHITECTURE · 接入架构", "<strong>2 行代码</strong>，三方协同即可上线。"),
    lab(120, 236, "01 · THREE PARTIES"),
    figbox(120, 285, 1680, 1680, 500, _p10(), i=1),
    rule(850),
    land("终端只管采集与播放，密钥与业务逻辑留在你的服务器——2 行代码、15 分钟即可跑通，安全可控、上线快。"),
]))

# ═══ P11 · 典型场景 ·「一套引擎，支撑多类场景」════════════════════════════
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

# ═══ P12 · Why Agora ·「跑在声网实时互动底座之上」═════════════════════════
#   数据修正页：四数字与 note / SOURCE 全部与 31 页拜访版 P2 一字对齐。
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
    sh("flow", "left:120px;top:650px;width:1680px;height:60px;--i:5",
       '<div class="note grey">注：根据 IDC 数据，声网在音视频通信（RTC）赛道的市场占有率达 '
       '<b>43.4%</b>——超过第 2–8 位厂商总和。</div>'),
    # top 794 而非 820：content 背景板自带一条 accent 细线在 y848–852（x120–761），
    # land 落在 820 时字形正压在线上 = 划掉的观感；抬到 794 让那条线落到文字下方当收口横线
    land("2014 年成立，全球最受欢迎的实时音视频云服务提供商——语音智能体，"
         "跑在经海量流量锤炼的底座上。", y=794),
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px;--i:7",
       "SOURCE · 声网官网 / IR 公开口径 · IDC"),
]))

# ═══ P13 · 收尾（title 板）═══════════════════════════════════════════════
page("title", "".join([
    sh("ink", "left:120px;top:320px;width:1560px;height:250px;"
       "font:700 96px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "最好的对话式 AI，<br>让人<strong style='color:var(--accent)'>忘了它是 AI</strong>。"),
    sh("spread", "left:120px;top:626px;width:120px;height:4px;background:var(--accent);"
       "border-radius:2px;--i:3", ""),
    sh("flow sub", "left:120px;top:678px;width:1500px;height:48px;--i:4",
       "低延时、可打断、听得清、看得见——把技术藏进体验里。"),
    sh("flow mono-sm", "left:120px;top:930px;width:1400px;height:24px;--i:6",
       "仅供方案交流参考"),
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
        'b.addEventListener("click",function(){cur=(cur==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",cur);}catch(e){}apply(cur);});})();</script>\n'
        "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")
    OUT_ALIAS.write_text(doc, encoding="utf-8")
    assert total == 13, "页数漂移：%d != 13" % total
    assert doc.count("<section") == 13, "section 数漂移：%d" % doc.count("<section")
    print("convoai.html + convoai-engine.html（双生） · %d 页 · %dKB · conf-light 默认 · 全页 data-steps=0" % (total, len(doc) // 1024))

if __name__ == "__main__":
    build()
