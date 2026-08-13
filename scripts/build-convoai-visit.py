#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-visit.py · 《声网对话式 AI · 公司与产品矩阵》初次拜访客户 deck
# CONF 家族 · conf-light 默认 · 单文件双主题 · 背景板节奏 · 三线三色 · hero-art 章视觉
# 结构（方案 A · Colin 2026-08-12 拍板 · 31 页）：
#   序幕(5) → 矩阵(3) → Engine(5) → Agent(5) → PhysicalAI(4) → 案例(4) → 合流(3) → 收尾(2)
# 口径纪律：只用公开可查证数字；Phone Agent 用「Global 率先发布」（不写未来日期）；
#   点名 LiveKit（拍板5）；序幕/图灵/五维/12项 = BPO 喂稿锁定文案逐字口径。
# hero-art：GPT 5.6 交付（2048×1152 RGBA 透明底 ×5 组双主题），contain 不裁切，
#   放在背景板之上、正文之下；T3 左下听筒与 T5 底部半球为有意构图，禁止 cover。
# ═══════════════════════════════════════════════════════════════════════════
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
OUT = ROOT / "public" / "decks" / "convoai.html"
A = "/decks/assets/convoai/"
R26 = "/decks/assets/robot26/"
B = "/decks/assets/conf-boards/"

def css(name):
    return (SRC / name).read_text(encoding="utf-8")

FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>"""

# ── 背景板（六板节奏 · skill 默认组合 + 三章各归各板）────────────────────────
BOARDS_CSS = """<style id="convoai-boards">
.conf-bg{position:absolute;inset:0;z-index:0;pointer-events:none;background-repeat:no-repeat;
  background-position:center;background-size:cover;opacity:var(--conf-bg-opacity,.58);}
.slide.conf-boarded{background:transparent!important;}
.slide.conf-boarded>.pp{z-index:1;}
.conf-bg-title{--conf-bg-opacity:.66;background-image:url('%(B)stitle-02-orbit-light.png');}
.conf-bg-ch-eng{--conf-bg-opacity:.58;background-image:url('%(B)schapter-01-giant-index-light.png');}
.conf-bg-ch-agent{--conf-bg-opacity:.58;background-image:url('%(B)schapter-02-window-light.png');}
.conf-bg-ch-phys{--conf-bg-opacity:.58;background-image:url('%(B)schapter-03-constellation-light.png');}
.conf-bg-quote{--conf-bg-opacity:.46;background-image:url('%(B)squote-02-halo-rings-light.png');}
.conf-bg-content{--conf-bg-opacity:.42;background-image:url('%(B)scontent-01-matrix-light.png');}
html[data-theme="dark"] .conf-bg-title{background-image:url('%(B)stitle-02-orbit-dark.png');}
html[data-theme="dark"] .conf-bg-ch-eng{background-image:url('%(B)schapter-01-giant-index-dark.png');}
html[data-theme="dark"] .conf-bg-ch-agent{background-image:url('%(B)schapter-02-window-dark.png');}
html[data-theme="dark"] .conf-bg-ch-phys{background-image:url('%(B)schapter-03-constellation-dark.png');}
html[data-theme="dark"] .conf-bg-quote{background-image:url('%(B)squote-02-halo-rings-dark.png');}
html[data-theme="dark"] .conf-bg-content{background-image:url('%(B)scontent-01-matrix-dark.png');}
html[data-theme="dark"] .conf-bg{filter:saturate(.92);}
</style>""" % {"B": B}

# ── 本 deck 专属 CSS ─────────────────────────────────────────────────────────
DECK_CSS = """<style id="convoai-deck">
/* 绝对画布 shape 层（robot26 惯例；reference 栈是语义排版系，缺这两行） */
.pp{position:absolute;inset:0;}
.pp .sh{position:absolute;overflow:visible;}
:root{--l-eng:var(--accent);--l-agent:#5b8cff;--l-phys:#7b61ff;
  /* conf 家族 token 表里没有 --on-bg，而 components.css 的 .card.on 靠它上底色：
     变量未定义 → 整条 background 声明作废 → 高亮卡反而丢掉 .card 的 card-bg 变成透明。
     照 inspire26 的 13%→3% / 暗底 9%→2% 补上，颜色走 var()，并把 card-bg 垫在渐变下面。 */
  --on-bg:linear-gradient(180deg,color-mix(in srgb,var(--accent) 13%,transparent),
    color-mix(in srgb,var(--accent) 3%,transparent)),var(--card-bg);
  --warn-bg:linear-gradient(180deg,color-mix(in srgb,var(--coral) 10%,transparent),
    color-mix(in srgb,var(--coral) 2.5%,transparent)),var(--card-bg);}
html[data-theme="dark"]{--l-agent:#6e96ff;--l-phys:#b78cf0;
  --on-bg:linear-gradient(180deg,color-mix(in srgb,var(--accent) 9%,transparent),
    color-mix(in srgb,var(--accent) 2%,transparent)),var(--card-bg);
  --warn-bg:linear-gradient(180deg,color-mix(in srgb,var(--coral) 9%,transparent),
    color-mix(in srgb,var(--coral) 2%,transparent)),var(--card-bg);}
/* .card .tag（0,2,0）压过 .am（0,1,0）——高亮卡的 tag 拿不到琥珀，补一条同特异度的 */
.card .tag.am{color:var(--amber);}
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 15px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--sig-ink);}
/* hero-art：背景板之上、正文之下；contain 不裁切，不加底色（GPT 交接约束） */
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
.kpi,.card-c{background:var(--card-bg);border:1px solid var(--hair);border-radius:20px;}
.kpi{padding:34px 38px;}
.kpi .tag{font:700 15px/1 var(--f-mono);letter-spacing:.18em;color:var(--accent);}
.kpi .num{margin-top:22px;font:900 92px/1 var(--f-cn);letter-spacing:-.03em;color:var(--ink);}
.kpi .num small{font:700 34px/1 var(--f-cn);letter-spacing:0;}
.kpi .cap{margin-top:14px;font:400 20px/1.45 var(--f-cn);color:var(--ink-2);}
/* 矩阵卡 */
.mx{padding:30px 34px;}
.mx .tag{font:700 14px/1 var(--f-mono);letter-spacing:.16em;color:var(--tc,var(--accent));}
.mx h3{margin:14px 0 10px;font:700 32px/1.25 var(--f-cn);color:var(--ink);}
.mx h3 em{font-style:normal;font:500 15px/1 var(--f-mono);color:var(--ink-3);letter-spacing:.06em;margin-left:12px;}
.mx p{font:400 19px/1.5 var(--f-cn);color:var(--ink-2);}
/* 时间轴 */
.tl-line{background:var(--hair);height:3px;}
.tl .date{font:700 17px/1 var(--f-mono);letter-spacing:.06em;color:var(--accent);}
.tl h3{margin:12px 0 8px;font:700 27px/1.3 var(--f-cn);color:var(--ink);}
.tl p{font:400 18px/1.45 var(--f-cn);color:var(--ink-2);}
.tl.hot h3{color:var(--accent);}
.tl-pin{width:20px;height:20px;border-radius:50%;background:var(--accent);
  box-shadow:0 0 0 6px color-mix(in srgb,var(--accent) 20%,transparent);}
/* 版本轴 tick */
.vt{width:3px;background:var(--ink-3);opacity:.55;}
.vt.big{background:var(--accent);opacity:1;width:5px;}
/* 主题词 chip */
.chip{display:inline-block;margin:0 14px 16px 0;padding:12px 20px;border:1px solid var(--hair);
  border-radius:999px;background:var(--card-bg);font:500 20px/1 var(--f-cn);color:var(--ink-2);}
/* 对比条 */
.cmp-name{font:700 26px/1.3 var(--f-cn);color:var(--ink);}
.cmp-dir{font:500 14px/1 var(--f-mono);letter-spacing:.1em;color:var(--ink-3);}
.cbar{height:40px;border-radius:9px;}
.cbar.ours{background:var(--l-eng);}
.cbar.them{background:var(--ink-3);opacity:.42;}
.cval{font:700 24px/40px var(--f-mono);color:var(--ink);}
.cval em{font-style:normal;font-size:16px;color:var(--ink-3);margin-left:8px;}
/* funnel */
.fbar{height:66px;border-radius:12px;background:color-mix(in srgb,var(--l-agent) 82%,transparent);}
.fbar.dim{background:var(--ink-3);opacity:.45;}
.flab{font:500 20px/66px var(--f-cn);color:var(--ink);white-space:nowrap;}
.flab b{font:700 22px/1 var(--f-mono);letter-spacing:.02em;}
/* 五维 */
.five{padding:26px 24px;}
.five .tag{font:700 13px/1 var(--f-mono);letter-spacing:.14em;color:var(--l-agent);}
.five h3{margin:12px 0 6px;font:700 27px/1.25 var(--f-cn);color:var(--ink);}
.five .ans{margin:14px 0 8px;font:900 42px/1 var(--f-cn);letter-spacing:-.02em;color:var(--l-agent);}
.five .ans small{font:700 19px/1.3 var(--f-cn);display:block;margin-top:8px;color:var(--ink);}
.five p{font:400 16.5px/1.45 var(--f-cn);color:var(--ink-2);}
/* 12 宫格 */
.g12{padding:22px 26px;}
.g12 .no{font:700 14px/1 var(--f-mono);color:var(--l-agent);letter-spacing:.08em;}
.g12 h3{margin:10px 0 6px;font:700 23px/1.25 var(--f-cn);color:var(--ink);}
.g12 p{font:400 15.5px/1.4 var(--f-cn);color:var(--ink-2);}
/* 三态卡（活人感） */
.face{padding:26px 30px;border-top:5px solid var(--ink-3);}
.face .en{font:700 14px/1 var(--f-mono);letter-spacing:.2em;color:var(--ink-3);}
.face h3{margin:10px 0 8px;font:700 34px/1.2 var(--f-cn);color:var(--ink);}
.face p{font:400 18.5px/1.5 var(--f-cn);color:var(--ink-2);}
.face.good{border-top-color:var(--l-phys);}
.face.good h3{color:var(--l-phys);}
/* .pp .sh{overflow:visible}（0,2,0）压得过 .strip{...}（0,1,0）——必须同特异度以上才生效，
   否则 height:auto 的位图按原始比例撑出盒外，砸到下一排 .face 卡（遮盖报告 #1–#3）。
   overflow 只裁「画」不裁「盒」，所以第二道同时把 img 的布局盒收进 .sh：
   cover + object-position 顶对齐 = 与 overflow 裁切完全相同的取景（底部烤字带按设计裁掉）。 */
.pp .sh.strip{overflow:hidden;border-radius:18px;}
.strip img{width:100%;height:auto;max-width:none;max-height:none;display:block;}
.pp .sh.strip img{height:100%;object-fit:cover;object-position:50% 0;}
/* 移植 inspire26/dual26 版式：.fig 内的 SVG 走 width:100%;height:auto，
   必须解掉 stage.css 的 svg{max-width:100%;max-height:100%}，否则定高 .sh 里会被压扁 */
.fig svg{max-width:none;max-height:none;}
/* 案例卡 */
.case{border-radius:18px;overflow:hidden;border:1px solid var(--hair);
  box-shadow:0 10px 28px rgba(0,0,0,.12);background:var(--card-bg);}
.case img{width:100%;height:100%;object-fit:cover;display:block;}
/* 图框 */
.frame{border-radius:20px;overflow:hidden;border:1px solid var(--hair);
  box-shadow:0 14px 40px rgba(0,0,0,.14);background:#fff;}
.frame img{width:100%;height:100%;object-fit:cover;display:block;}
.callout-chip{background:var(--ink);color:var(--bg,#fff);border-radius:12px;padding:14px 24px;
  font:700 20px/1.4 var(--f-cn);box-shadow:0 8px 24px rgba(0,0,0,.22);}
html[data-theme="dark"] .callout-chip{background:#f5f5f4;color:#111;}
/* 金句页 */
.q-big{font:700 76px/1.35 var(--f-cn);letter-spacing:-.01em;color:var(--ink);text-align:center;}
.q-big strong{color:var(--accent);}
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

# ── 组装件 ──────────────────────────────────────────────────────────────────
def sh(cls, style, body, step=None, sid=None):
    a = ' data-sid="%s"' % sid if sid else ""
    a += ' data-step="%d"' % step if step is not None else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (cls, a, style, body)

def dot(var):
    return '<span class="dot" style="background:var(--%s)"></span>' % var

PAGES = []          # (board, steps, body_html, hero)
def page(board, steps, body, hero=None):
    PAGES.append((board, steps, body, hero))

def case_row(names, top, h):
    """等宽案例卡一排（14 张官方联合案例图 · 530×942 与 840×1493 同为 0.5626 比例）"""
    n = len(names)
    gap = 28
    w = (1680 - (n - 1) * gap) // n
    out = []
    for i, nm in enumerate(names):
        x = 120 + i * (w + gap)
        out.append(sh("rise case", "left:%dpx;top:%dpx;width:%dpx;height:%dpx" % (x, top, w, h),
                      '<img src="%scase-%s.webp" alt="声网联合案例 · %s">' % (A, nm, nm)))
    return "".join(out)

# ═══ 序幕 · 公司信任状（P1–P5）═══════════════════════════════════════════════

# P1 · 封面（T1 hero 右侧盒装 contain，不裁切）
page("title", 0, "".join([
    sh("flow kk", "left:120px;top:200px;width:1400px;height:28px",
       "AGORA · 声网 · CONVERSATIONAL AI"),
    sh("ink", "left:120px;top:266px;width:1100px;height:250px;font:700 96px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "让每一次人机对话，<br>都像<strong style='color:var(--accent)'>真人</strong>一样自然。"),
    sh("flow sub", "left:120px;top:600px;width:1400px;height:44px",
       "声网 · 对话式 AI 产品矩阵 —— 公司与三条产品线"),
    sh("rise", "left:120px;top:700px;width:1500px;height:56px;font:700 26px/1 var(--f-mono);letter-spacing:.06em;color:var(--ink-2)",
       dot("l-eng") + 'ENGINE<span style="margin-left:56px"></span>'
       + dot("l-agent") + 'AGENT<span style="margin-left:56px"></span>'
       + dot("l-phys") + 'PHYSICAL AI'),
    sh("flow mono-sm", "left:120px;top:930px;width:1200px;height:24px",
       "主讲人：姚光华 Colin · 声网 AI 产品线负责人"),
]), hero=("three-engines", "left:860px;top:230px;width:1200px;height:675px"))

# P2 · RTE 领导者（锁定文案 · 官网/IR 口径 · dual26 p06 四卡数字墙）
_RTE = [
    ("市场占有率", "No.1",  "市场占有率稳居第一，份额超过第 2–8 位总和", True),
    ("技术突破",   "50+",   "突破性自主创新技术（全球发明专利）",       False),
    ("开发者生态", "100万+", "全球注册应用数",                         False),
    ("生产规模",   "900亿+", "单月支撑通话分钟数",                     False),
]
page("content", 1, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "序幕 · 声网 RTE · REAL-TIME ENGAGEMENT"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "RTE 行业的<strong>领导者</strong>。"),
    sh("", "left:120px;top:330px;width:1680px;height:268px",
       '<div class="g4">' + "".join(
           '<div class="card%s rise" style="--i:%d"><div class="tag%s">%s</div>'
           '<div class="stat"><span class="v%s">%s</span><span class="l">%s</span></div></div>'
           % (" on" if _on else "", 2 + _i, " am" if _on else "", _tag,
              "" if _on else " w", _v, _l)
           for _i, (_tag, _v, _l, _on) in enumerate(_RTE)) + '</div>'),
    sh("flow", "left:120px;top:700px;width:1680px;height:60px",
       '<div class="note grey">注：根据 IDC 数据，声网在音视频通信（RTC）赛道的市场占有率达 '
       '<b>43.4%</b>——超过第 2–8 位厂商总和。</div>', step=1),
    # top 794 而非 820：content 背景板自带一条 accent 细线在 y848–852（x120–761），
    # land 落在 820 时字形正压在线上 = 划掉的观感；抬 26px 让那条线落到文字下方当收口横线
    sh("flow", "left:120px;top:794px;width:1680px;height:70px",
       '<div class="land">全球最受欢迎的实时音视频云服务提供商。</div>', step=1),
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px", "SOURCE · 声网官网 / IR 口径 · 2026"),
]))

# P3 · 全球开发者首选（锁定文案 P3 · 大数字 + 分账图）
_P3FIG = (
    '<div class="fig"><svg viewBox="0 0 1000 360" style="width:100%;height:auto">'
    '<g class="pop" style="--i:0">'
    '<rect x="60" y="30" width="880" height="62" rx="2" class="box" stroke-width="1"/>'
    '<text class="lbl" x="500" y="67" text-anchor="middle">全球 Top 10,000 Apps（按 MAU）</text></g>'
    '<path class="dw" style="--len:140;--i:1" d="M60 92 L190 142" stroke="var(--hair-strong)" stroke-width="1" fill="none"/>'
    '<path class="dw" style="--len:140;--i:1" d="M940 92 L810 142" stroke="var(--hair-strong)" stroke-width="1" fill="none"/>'
    '<g class="pop" style="--i:2">'
    '<rect x="190" y="142" width="620" height="62" rx="2" class="box" stroke-width="1"/>'
    '<text class="lbl" x="500" y="179" text-anchor="middle">其中集成 RTC 服务的 App</text></g>'
    '<path class="dw" style="--len:54;--i:3" d="M250 204 V258" stroke="var(--hair-strong)" stroke-width="1" fill="none"/>'
    '<path class="dw" style="--len:54;--i:3" d="M750 204 V258" stroke="var(--hair-strong)" stroke-width="1" fill="none"/>'
    '<g class="pop" style="--i:4">'
    '<rect x="190" y="258" width="322" height="72" rx="2" fill="var(--accent)"/>'
    '<rect x="512" y="258" width="298" height="72" rx="2" class="box" stroke-width="1"/>'
    # fill 只是 presentation attribute，压不过 .fig .ttl{fill:var(--ink)}（CSS 一律高于呈现属性），
    # 必须写成内联 style 才生效——否则实心 accent 条上会印出深色字，浅底/暗底都读不出来
    '<text class="ttl" x="351" y="303" text-anchor="middle" style="fill:var(--slide-bg)">使用声网 · 近一半</text>'
    '<text class="txt" x="661" y="302" text-anchor="middle">其他 RTC 供应商合计</text></g>'
    '</svg></div>')
page("content", 1, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "序幕 · 全球开发者首选 · TOP 10000"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px",
       "全球开发者的<strong>共同选择</strong>。"),
    sh("settle", "left:120px;top:392px;width:660px;height:260px",
       '<div class="stat"><div class="v" style="font-size:150px;line-height:1;font-family:var(--f-cn)">近一半</div>'
       '<div class="l" style="margin-top:6px">集成 RTC 的 Top 10,000 App 里，近一半使用声网</div>'
       '<div class="u">NEARLY HALF OF RTC-EMBEDDED APPS EMBED AGORA</div></div>'),
    sh("flow", "left:840px;top:322px;width:960px;height:346px", _P3FIG, step=1),
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px", "SOURCE · 声网官网 / IR 口径 · 2026"),
]))

# P4 · OpenAI 背书（锁定文案 P4 · 金句板）
page("quote", 1, "".join([
    sh("flow kk nt", "left:120px;top:170px;width:1680px;height:28px;text-align:center",
       "国际背书 · INTERNATIONAL ENDORSEMENT"),
    sh("settle", "left:120px;top:250px;width:1680px;height:60px;text-align:center;font:700 44px/1 var(--f-mono);letter-spacing:.1em;color:var(--accent)",
       "2024.10.01"),
    sh("ink", "left:120px;top:370px;width:1680px;height:220px;text-align:center;font:700 76px/1.4 var(--f-cn);letter-spacing:-.01em;color:var(--ink)",
       "OpenAI Realtime API<br>Agora <strong style='color:var(--accent)'>全球首批合作伙伴</strong>"),
    sh("flow sub", "left:120px;top:650px;width:1680px;height:44px;text-align:center",
       "OpenAI 选择声网 RTE 网络，承载实时语音 API 全球落地。"),
    sh("rise", "left:120px;top:760px;width:1680px;height:56px;text-align:center;font:700 34px/1.4 var(--f-cn);color:var(--accent)",
       "同样的工程能力，今天用来支撑你的对话式 AI 业务。", step=1),
    sh("flow mono-sm", "left:120px;top:880px;width:1680px;height:24px;text-align:center",
       "THE SAME ENGINE THAT POWERS OPENAI'S REALTIME API — NOW POWERS YOURS."),
]))

# P5 · 18 个月 5 里程碑（锁定文案 P5 · dual26 p12 卡片式时间轴）
#   轴 M10 60 H1590 + 5 圆点 r5 + 5 张 300×200 卡；末节点 amber 描边 + amber 字
_MILE = [
    (  10, "2024.10.01", ["全球首个", "Realtime API"],  ["OpenAI + Agora", "首批合作伙伴"],       False),
    ( 330, "2024.10.24", ["国内首个", "Realtime API"],  ["声网 × MiniMax"],                      False),
    ( 650, "2025.03.06", ["引擎 1.0 + R1 GA"],          ["行业首个对话式 AI 引擎", "与硬件开发套件"], False),
    ( 970, "2025.10.31", ["产品全栈发布"],              ["Studio 1.0 + Engine 2.0", "+ Benchmark 3.0"], False),
    (1290, "2026.03.10", ["Call Agent 全球版"],         ["电话客服", "企业级智能体"],              True),
]
def _mile(x, date, tt, sm, hot, i):
    # 高亮色走内联 style（fill 属性会被 .fig .lbl/.ttl 的 CSS fill 覆盖，形同没写）
    cx, am = x + 150, (' style="fill:var(--amber)"' if hot else "")
    box = ('<rect x="%d" y="90" width="300" height="200" rx="3" fill="none" stroke="var(--amber)" stroke-width="2"/>' % x
           if hot else '<rect x="%d" y="90" width="300" height="200" rx="3" class="box" stroke-width="1"/>' % x)
    ty = [186] if len(tt) == 1 else [170, 202]
    o = ['<g class="pop" style="--i:%d">' % i,
         '<circle cx="%d" cy="60" r="5" class="%s"/>' % (cx, "fill-am" if hot else "fill-ink"), box,
         '<text class="lbl" x="%d" y="126" text-anchor="middle"%s>%s</text>' % (cx, am, date)]
    o += ['<text class="ttl" x="%d" y="%d" text-anchor="middle"%s>%s</text>' % (cx, ty[k], am, t)
          for k, t in enumerate(tt)]
    o += ['<text class="sm" x="%d" y="%d" text-anchor="middle">%s</text>' % (cx, 240 + k * 26, s)
          for k, s in enumerate(sm)]
    return "".join(o) + "</g>"
_p5fig = ('<div class="fig"><svg viewBox="0 0 1620 340" style="width:100%;height:auto">'
          '<path class="dw" style="--len:1580;--i:0" d="M10 60 H1590" stroke="var(--hair)" stroke-width="1" fill="none"/>'
          '<g data-step="1">' + "".join(_mile(*m, i=k) for k, m in enumerate(_MILE[:3])) + '</g>'
          '<g data-step="2">' + "".join(_mile(*m, i=k) for k, m in enumerate(_MILE[3:])) + '</g>'
          '</svg></div>')
page("content", 2, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "序幕 · CONVOAI · 18 个月 · 5 个公开里程碑"),
    sh("ink hh", "left:120px;top:148px;width:1200px;height:100px", "18 个月，我们做了 <strong>5 件事</strong>。"),
    sh("flow sub", "left:120px;top:252px;width:1200px;height:40px", "从全球首个 Realtime API 到 Call Agent 全球版"),
    sh("flow", "left:120px;top:330px;width:1680px;height:353px", _p5fig),
    sh("flow", "left:120px;top:760px;width:1680px;height:80px",
       '<div class="land">18 个月 · 5 个对外里程碑——每一步都基于'
       '<strong style="color:var(--accent)">真实的市场和客户反馈</strong>。</div>', step=2),
]))

# ═══ 矩阵 · 一张大图（P6–P8）═════════════════════════════════════════════════

# P6 · 产品矩阵总览（官网分层方案口径 · 六件 · inspire26 p20 架构分层图）
#   六框 250×130 gap 20（10→1610，与底座 rect 1600@x10 右端齐平）→ 竖线 → 实时互动平台底座
_MX = [
    ("对话式 AI 引擎",  "闭源 · 已上线",       True),
    ("TEN 开源工具库",  "开源",               False),
    ("电话客服 Agent",  "Global 率先发布",     False),
    ("AI 模型评测平台", "已上线",             False),
    ("实时转录翻译",    "已上线",             False),
    ("开发套件",        "Physical AI · 已上线", False),
]
def _mxbox(i, name, form, hot):
    x = 10 + i * 270
    cx = x + 125
    am = "fill:var(--amber);" if hot else ""      # 内联 style，见 _mile 注释
    box = ('<rect x="%d" y="40" width="250" height="130" rx="3" fill="none" stroke="var(--amber)" stroke-width="2"/>' % x
           if hot else '<rect x="%d" y="40" width="250" height="130" rx="3" class="box" stroke-width="1"/>' % x)
    return ('<g class="pop" style="--i:%d">%s'
            '<text class="ttl" x="%d" y="96" text-anchor="middle" style="%sfont-size:22px">%s</text>'
            '<text class="sm" x="%d" y="130" text-anchor="middle">%s</text></g>'
            % (i, box, cx, am, name, cx, form))
_p6fig = ('<div class="fig"><svg viewBox="0 0 1620 430" style="width:100%;height:auto">'
          + "".join(_mxbox(i, n, f, h) for i, (n, f, h) in enumerate(_MX))
          + '<g data-step="1">'
          + "".join('<path class="dw" style="--len:55;--i:0" d="M%d 170 V225" '
                    'stroke="var(--hair-strong)" stroke-width="1.5" fill="none"/>' % (135 + i * 270)
                    for i in range(6))
          + '<g class="pop" style="--i:1">'
            '<rect x="10" y="235" width="1600" height="110" rx="3" class="box" stroke-width="1"/>'
            '<text class="lbl" x="42" y="278">实时互动平台 · REAL-TIME ENGAGEMENT</text>'
            '<text class="txt" x="42" y="316">SD-RTN 全球实时网络——当下基本盘，托举全部对话式 AI 产品线</text>'
            '</g></g></svg></div>')
page("content", 2, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "矩阵 · 对话式 AI 产品线 · PRODUCT MATRIX"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "对话式 AI · <strong>产品矩阵</strong>总览。"),
    sh("flow", "left:120px;top:300px;width:1680px;height:446px", _p6fig),
    sh("flow", "left:120px;top:800px;width:1680px;height:56px",
       '<div class="note">与实时互动平台并列的<strong style="color:var(--accent)">两大产品引擎</strong>'
       '——未来增长曲线 + 当下基本盘。</div>', step=2),
    sh("flow", "left:120px;top:890px;width:1680px;height:70px",
       '<div class="land">六件产品，一张底网——这就是对话式 AI 的完整矩阵。</div>', step=2),
]))

# P7 · 一底座三引擎（T1 hero 全幅作图 · 分流标注三步）
page("content", 3, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "矩阵 · 一底座，三台引擎 · ONE RIVER, THREE STREAMS"),
    sh("ink hh", "left:120px;top:148px;width:1400px;height:100px", "一个实时底座，<strong>三台引擎</strong>。"),
    sh("flow mono-sm", "left:150px;top:668px;width:340px;height:24px", "SD-RTN · 实时底座"),
    sh("rise", "left:1200px;top:400px;width:560px;height:110px", (
        '<div style="font:700 30px/1 var(--f-cn);color:var(--l-eng)">ENGINE · 对话式 AI 引擎</div>'
        '<div style="margin-top:10px;font:400 20px/1.4 var(--f-cn);color:var(--ink-2)">提供能力——把「会说话」做到极致</div>'), step=1),
    sh("rise", "left:1200px;top:586px;width:560px;height:110px", (
        '<div style="font:700 30px/1 var(--f-cn);color:var(--l-agent)">AGENT · 电话客服智能体</div>'
        '<div style="margin-top:10px;font:400 20px/1.4 var(--f-cn);color:var(--ink-2)">交付结果——替你把任务做完</div>'), step=2),
    sh("rise", "left:1200px;top:772px;width:560px;height:110px", (
        '<div style="font:700 30px/1 var(--f-cn);color:var(--l-phys)">PHYSICAL AI · 硬件与具身</div>'
        '<div style="margin-top:10px;font:400 20px/1.4 var(--f-cn);color:var(--ink-2)">打开入口——让对话走出屏幕</div>'), step=3),
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px",
       "现场按你的业务，任选一条支流深入。"),
]), hero=("three-engines", None))

# P8 · MQ01（金句板）
page("quote", 1, "".join([
    sh("ink q-big", "left:120px;top:420px;width:1680px;height:220px",
       "「一个平台，<strong>三台引擎</strong>。」"),
    sh("rise", "left:120px;top:720px;width:1680px;height:56px;text-align:center;font:500 28px/1.6 var(--f-cn);color:var(--ink-2)",
       dot("l-eng") + "Engine 提供能力　" + dot("l-agent") + "Agent 交付结果　" + dot("l-phys") + "Physical AI 走进物理世界",
       step=1),
]))

# ═══ 支流一 · ENGINE（P9–P13 · 玫红）════════════════════════════════════════

# P9 · Engine 章首（chapter-01 Giant Index + T2 hero 右侧）
page("ch-eng", 0, "".join([
    sh("flow kk", "left:120px;top:330px;width:900px;height:28px", "支流一 · ENGINE · 对话式 AI 引擎"),
    sh("ink", "left:120px;top:392px;width:940px;height:330px;font:700 84px/1.3 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "超低延迟、可打断、<br><strong style='color:var(--l-eng)'>高自然度</strong>的<br>语音智能体运行时。"),
    sh("flow sub", "left:120px;top:770px;width:860px;height:80px",
       "从 v1.0 公测到 v2.11——18 个月 17 个公开版本，跑在真实生产里。"),
    sh("flow mono-sm", "left:120px;top:930px;width:800px;height:24px", "ENGINE · 闭源商业产品 · 已上线"),
]), hero=("engine-core", None))

# P10 · 18 个月 17 版（发版说明口径）
_p10 = [
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "ENGINE · 版本节奏 · SHIPPING VELOCITY"),
    sh("ink hh", "left:120px;top:148px;width:1150px;height:100px", "迭代速度，就是<strong>产品力</strong>。"),
    sh("settle", "left:1420px;top:120px;width:380px;height:170px;text-align:right;font:900 170px/1 var(--f-cn);letter-spacing:-.04em;color:var(--l-eng)", "17"),
    sh("flow mono-sm", "left:1420px;top:296px;width:380px;height:24px;text-align:right", "PUBLIC RELEASES · 18 MONTHS"),
    sh("flow tl-line", "left:180px;top:470px;width:1560px;height:3px", ""),
    sh("rise tl", "left:180px;top:520px;width:420px;height:110px",
       '<div class="date">2025.02.18</div><h3>v1.0 公测</h3><p>行业首个对话式 AI 引擎公测</p>'),
    sh("rise tl hot", "left:1330px;top:520px;width:410px;height:110px",
       '<div class="date">2026.08.11</div><h3>v2.11 · 最新</h3><p>发版说明持续更新中</p>'),
]
for _i in range(17):
    _x = 180 + round(_i * 1560 / 16)
    _big = _i in (0, 16)
    _p10.append(sh("pop vt" + (" big" if _big else ""), "left:%dpx;top:%dpx;width:%dpx;height:%dpx"
                   % (_x, 446 if _big else 452, 5 if _big else 3, 50 if _big else 38), ""))
_p10.append(sh("rise", "left:120px;top:700px;width:1680px;height:200px", (
    '<div class="mono-sm" style="margin-bottom:18px">一条时间轴 · 十一个能力主题</div>'
    + "".join('<span class="chip">%s</span>' % t for t in
              ["优雅打断", "三态人声", "暂停意图", "打断架构重构", "有感 / 无感声纹", "短期记忆",
               "MCP 工具接入", "数字人", "ASR / TTS 多供应商", "媒体加密", "热词"])), step=1))
_p10.append(sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px",
               "SOURCE · doc.shengwang.cn · 对话式 AI 引擎发版说明 · 截至 2026.08.11（v2.11）"))
page("content", 1, "".join(_p10))

# P11 · 对 LiveKit 四项（评测报告口径 · 拍板5 点名）
_CMP = [
    ("打断成功率", "越高越好", 900, 464, "33%", "17%"),
    ("词错率 WER", "理想条件 · 越低越好", 605, 900, "9.25%", "13.77%"),
    ("误响应率", "50dB 人声噪声 · 越低越好", 63, 900, "7%", "100%"),
    ("多语种", "开箱默认 · 中/西/法/俄/阿/日", 900, 150, "6/6", "仅英文"),
]
_p11 = [
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "ENGINE · 评测口径 · AGORA VS LIVEKIT AGENTS"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "同题评测，<strong>四项全胜</strong>。"),
]
for _i, (_n, _dir, _wo, _wt, _vo, _vt) in enumerate(_CMP):
    _y = 320 + _i * 150
    _p11 += [
        sh("flow", "left:120px;top:%dpx;width:360px;height:110px" % _y,
           '<div class="cmp-name">%s</div><div class="cmp-dir" style="margin-top:8px">%s</div>' % (_n, _dir)),
        sh("spread cbar ours", "left:520px;top:%dpx;width:%dpx;height:40px" % (_y, _wo), ""),
        sh("flow cval", "left:%dpx;top:%dpx;width:200px;height:40px" % (540 + _wo, _y), "%s<em>声网</em>" % _vo),
        sh("spread cbar them", "left:520px;top:%dpx;width:%dpx;height:40px" % (_y + 56, max(_wt, 10)), ""),
        sh("flow cval", "left:%dpx;top:%dpx;width:220px;height:40px" % (540 + max(_wt, 10), _y + 56), "%s<em>LiveKit</em>" % _vt),
    ]
_p11.append(sh("rise card-c", "left:120px;top:930px;width:1680px;height:110px",
               '<div style="padding:30px 46px;border-left:6px solid var(--l-eng);font:700 28px/1.4 var(--f-cn);color:var(--ink)">'
               '打断更稳 · 听得更准 · 噪声更扛 · 多语种开箱即用——这是引擎的「体验分」。</div>', step=1))
_p11.append(sh("flow mono-sm", "left:120px;top:1052px;width:1680px;height:22px",
               "SOURCE · 声网同题评测 · 2026-03 Web Demo · LiveKit=Deepgram Nova-3+GPT-4.1-mini · TTS 同用 11Labs ｜ 打断/语种为当期默认配置，LiveKit TD v1.0（2026-06）后待复测"))
page("content", 1, "".join(_p11))

# P12 · 三件绝活（卡顶各一张 mini .fig · 线宽 2 · 主色 l-eng）
_FIG_CUT = (           # ① 优雅打断：hair 波连续 / accent 波中段截断 + 竖向缺口 + pop 圆点
    '<path class="stroke" style="stroke-width:2" d="M14 70 q28 -44 56 0 t56 0 t56 0 t56 0 t56 0 t56 0 t56 0"/>'
    '<path fill="none" stroke="var(--l-eng)" stroke-width="2" d="M14 52 q28 44 56 0 t56 0 t56 0"/>'
    '<path fill="none" stroke="var(--l-eng)" stroke-width="2" d="M238 52 q28 44 56 0 t56 0 t56 0"/>'
    '<path d="M210 18 V104" stroke="var(--hair-strong)" stroke-width="2" stroke-dasharray="4 6" fill="none"/>'
    '<circle class="pop fill-am" cx="210" cy="61" r="6"/>')
_FIG_VP = (            # ② 声纹：两组同心弧错位，左组 accent
    '<g fill="none" stroke="var(--l-eng)" stroke-width="2">'
    '<path d="M120 32 A18 18 0 0 1 120 68"/><path d="M120 20 A30 30 0 0 1 120 80"/>'
    '<path d="M120 8 A42 42 0 0 1 120 92"/></g><circle class="fill-am" cx="120" cy="50" r="5"/>'
    '<g class="stroke" style="stroke-width:2">'
    '<path d="M300 52 A18 18 0 0 0 300 88"/><path d="M300 40 A30 30 0 0 0 300 100"/>'
    '<path d="M300 28 A42 42 0 0 0 300 112"/></g>'
    '<circle cx="300" cy="70" r="5" fill="var(--ink-3)"/>')
_FIG_MEM = (           # ③ 记忆：5 节点由 .dw 线串联，末节点 accent
    '<path class="dw stroke" style="--len:340;stroke-width:2" d="M40 60 H380"/>'
    + "".join('<circle cx="%d" cy="60" r="8" class="box" stroke-width="1.5"/>' % x
              for x in (40, 125, 210, 295))
    + '<circle class="fill-am" cx="380" cy="60" r="8"/>')
_MOVES = [
    ("01", "优雅打断 2.0", "CAN + 语义 + 声学三路融合。从「能打断」到「打断得体」：三态人声、暂停意图、误打断防抖。", _FIG_CUT),
    ("02", "声纹识别", "有感 / 无感双模式。多人同场分得清说话人，客服反欺诈直接可用。", _FIG_VP),
    ("03", "短期记忆", "会话内毫秒级上下文。转人工、转 Agent 不丢线索，多轮任务不断链。", _FIG_MEM),
]
page("content", 0, "".join(
    [sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "ENGINE · 三件绝活 · SIGNATURE MOVES"),
     sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "打断、声纹、记忆——<strong>三件绝活</strong>。")]
    + [sh("rise card-c", "left:%dpx;top:330px;width:536px;height:560px" % (120 + _i * 572),
          '<div style="padding:40px 42px">'
          '<div class="fig" style="margin-bottom:24px"><svg viewBox="0 0 420 120" style="width:100%%;height:auto">%s</svg></div>'
          '<div style="font:700 64px/1 var(--f-mono);color:var(--l-eng);opacity:.55">%s</div>'
          '<h3 style="margin:22px 0 16px;font:700 42px/1.2 var(--f-cn);color:var(--ink)">%s</h3>'
          '<p style="font:400 22px/1.65 var(--f-cn);color:var(--ink-2)">%s</p></div>' % (_f, _no, _n, _d))
       for _i, (_no, _n, _d, _f) in enumerate(_MOVES)]
    + [sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px",
          "均已在 v2.x 公开版本发布 · 见发版说明")]))

# P13 · 开放性（hub-spoke：左列可替换三件套 ↔ 引擎 → 右列开放栈三件）
def _arw(x, y, ang):
    """尖端落在 (x,y)、指向 ang 度的小三角"""
    return ('<polygon class="fill-ink" points="-13,-6.5 0,0 -13,6.5" '
            'transform="translate(%s %s) rotate(%s)"/>' % (x, y, ang))
def _spoke(x, y, w=300, h=96, name=""):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="3" class="box" stroke-width="1"/>'
            '<text class="ttl" x="%d" y="%d" text-anchor="middle" style="font-size:22px">%s</text>'
            % (x, y, w, h, x + w // 2, y + h // 2 + 8, name))
_LN = 'stroke="var(--hair-strong)" stroke-width="1.5" fill="none"'
_p13fig = ('<div class="fig"><svg viewBox="0 0 1620 520" style="width:100%;height:auto">'
           # 中心 · 引擎
           '<g class="pop" style="--i:0">'
           '<rect x="630" y="190" width="360" height="140" rx="3" '
           'style="fill:var(--card-bg);stroke:var(--l-eng);stroke-width:2"/>'
           '<text class="ttl" x="810" y="268" text-anchor="middle" style="font-size:28px">对话式 AI 引擎</text></g>'
           # 左列 · 可替换三件套（双向）
           + "".join('<g class="pop" style="--i:%d">%s</g>' % (i + 1, _spoke(60, y, name=n))
                     for i, (y, n) in enumerate([(40, "ASR"), (212, "LLM"), (384, "TTS")]))
           + '<path class="dw" style="--len:301;--i:1" d="M360 88 L630 220" %s/>' % _LN
           + '<path class="dw" style="--len:270;--i:2" d="M360 260 H630" %s/>' % _LN
           + '<path class="dw" style="--len:301;--i:3" d="M360 432 L630 300" %s/>' % _LN
           + '<g class="pop" style="--i:4">'
           + _arw(630, 220, 26.06) + _arw(360, 88, 206.06)
           + _arw(630, 260, 0) + _arw(360, 260, 180)
           + _arw(630, 300, -26.06) + _arw(360, 432, 153.94) + '</g>'
           + '<text class="sm" x="495" y="246" text-anchor="middle">可替换 · 可兜底 · 可热切换</text>'
           # 右列 · 开放栈三件（单向）
           + '<g data-step="1">'
           + "".join('<g class="pop" style="--i:%d">%s</g>' % (i, _spoke(1260, y, name=n))
                     for i, (y, n) in enumerate([(40, "MCP + Function Call"), (212, "数字人"), (384, "TEN 开源生态")]))
           + '<path class="dw" style="--len:301;--i:0" d="M990 220 L1260 88" %s/>' % _LN
           + '<path class="dw" style="--len:270;--i:1" d="M990 260 H1260" %s/>' % _LN
           + '<path class="dw" style="--len:301;--i:2" d="M990 300 L1260 432" %s/>' % _LN
           + '<g class="pop" style="--i:3">'
           + _arw(1260, 88, -26.06) + _arw(1260, 260, 0) + _arw(1260, 432, 26.06) + '</g>'
           + '</g></svg></div>')
page("content", 1, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "ENGINE · 开放与中立 · OPEN BY DESIGN"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "不锁死任何一家<strong>模型</strong>。"),
    sh("flow", "left:120px;top:290px;width:1680px;height:539px", _p13fig),
    sh("flow", "left:120px;top:890px;width:1680px;height:70px",
       '<div class="land">模型会换代，接口不换人——'
       '<strong style="color:var(--l-eng)">引擎替你消化供应商变化</strong>。</div>', step=1),
]))

# ═══ 支流二 · AGENT（P14–P18 · 蓝）══════════════════════════════════════════

# P14 · Agent 章首（chapter-02 Window + T3 hero 左侧）
page("ch-agent", 0, "".join([
    sh("flow kk ag", "left:960px;top:330px;width:840px;height:28px", "支流二 · AGENT · 电话客服智能体"),
    sh("ink", "left:960px;top:392px;width:840px;height:330px;font:700 84px/1.3 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "从引擎到<strong style='color:var(--l-agent)'>商品</strong>：<br>替你把任务<br>做完。"),
    sh("flow sub", "left:960px;top:770px;width:820px;height:80px",
       "Agora Phone Agent · Global 率先发布——呼入 / 外呼开箱即用。"),
    sh("flow mono-sm", "left:960px;top:930px;width:800px;height:24px", "CALL AGENT · 企业级 · 用生产数据说话"),
]), hero=("agent-call", None))

# P15 · 图灵测试 96.5%（锁定文案 · inspire26 p12 版式：左大数字 + 右四级 funnel）
#   比例尺 7px / 百分点：700 / 617 / 331 / 26；前两级实心 .box，后两级空心（l-agent → coral 降级）
_FUN = [
    ( 20, 700, "接听",      "2,475 · 100.0%", 272, None),
    ( 92, 617, "真人接听",   "2,180 · 88.1%",  272, None),
    (164, 331, "有效对话",   "1,170 · 47.3%",  272, "var(--l-agent)"),
    (236,  26, "感知为 AI",  "86 · 3.5%",      296, "var(--coral)"),
]
def _fun(i, y, w, lab, val, vx, col):
    bar = ('<rect x="250" y="%d" width="%d" height="52" rx="2" fill="none" stroke="%s" stroke-width="2"/>' % (y, w, col)
           if col else '<rect x="250" y="%d" width="%d" height="52" rx="2" class="box" stroke-width="1"/>' % (y, w))
    return ('<g class="pop" style="--i:%d">%s'
            '<text class="lbl" x="230" y="%d" text-anchor="end">%s</text>'
            '<text class="sm" x="%d" y="%d"%s>%s</text></g>'
            % (i, bar, y + 32, lab, vx, y + 33,
               (' style="fill:%s"' % col) if col else "", val))   # 内联 style，见 _mile 注释
_p15fig = ('<div class="fig"><svg viewBox="0 0 1000 300" style="width:100%;height:auto">'
           + "".join(_fun(i, *f) for i, f in enumerate(_FUN)) + '</svg></div>')
page("content", 1, "".join([
    sh("flow kk ag", "left:120px;top:92px;width:1680px;height:28px", "AGENT · 图灵测试 · REAL PRODUCTION DATA"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px",
       '<strong class="ag">96.5%</strong> 的用户，以为在跟真人说话。'),
    sh("flow", "left:120px;top:372px;width:560px;height:200px",
       '<div class="stat"><div class="v" style="color:var(--l-agent)">96.5%</div>'
       '<div class="l">基于 1,170 通真实有效对话——仅 3.5%（86 通）被用户明显感知为 AI</div>'
       '<div class="u">CONVOAI 真实生产数据 · 非实验室盲测</div></div>'),
    sh("flow rev", "left:740px;top:330px;width:1060px;height:318px", _p15fig),
    sh("flow", "left:120px;top:690px;width:1680px;height:90px",
       '<div class="note">86 通「明显感知」的九维信号拆解里，情绪 / 重复 / 不耐烦一项就占 60 通——'
       '其余 A–I 各维不超过 11 通。<br>≥1 句真实用户发言才计入有效对话。</div>'),
    sh("flow tl-line", "left:180px;top:830px;width:1560px;height:3px", "", step=1),
    sh("pop tl-pin", "left:170px;top:821px;width:20px;height:20px;background:var(--l-agent);box-shadow:0 0 0 6px color-mix(in srgb,var(--l-agent) 20%,transparent)", "", step=1),
    sh("pop tl-pin", "left:1730px;top:821px;width:20px;height:20px;background:var(--l-agent);box-shadow:0 0 0 6px color-mix(in srgb,var(--l-agent) 20%,transparent)", "", step=1),
    sh("rise", "left:120px;top:870px;width:1680px;height:120px;text-align:center;font:400 26px/1.7 var(--f-cn);color:var(--ink)",
       '<b style="font-family:var(--f-mono)">1950</b> 图灵设想机器能否骗过人类 ——76 年—— '
       '<b style="font-family:var(--f-mono)">2026</b> <strong style="color:var(--l-agent)">96.5% 的用户已经分辨不出</strong>。', step=1),
]))

# P16 · 3.08% vs 1.5%（inspire26 p14 横向双条 · 比例尺 266.6px/百分点：400 / 821）
_p16fig = ('<div class="fig"><svg viewBox="0 0 1620 300" style="width:100%;height:auto">'
           '<g class="pop" style="--i:0">'
           '<rect x="320" y="46" width="400" height="64" rx="2" class="box" stroke-width="1"/>'
           '<text class="lbl" x="300" y="84" text-anchor="end">行业最佳人工</text>'
           '<text class="txt" x="744" y="86">1.5% —— 受过良好培训与管理的一线销冠，行业天花板</text></g>'
           '<g data-step="1">'
           '<g class="pop" style="--i:0">'
           '<rect x="320" y="150" width="821" height="64" rx="2" fill="none" stroke="var(--l-agent)" stroke-width="2"/>'
           # Agent 章图形主色 = l-agent；一律内联 style（fill 属性压不过 .fig .lbl/.txt/.big 的 CSS fill）
           '<text class="lbl" x="300" y="188" text-anchor="end" style="fill:var(--l-agent)">ConvoAI</text>'
           '<text class="txt" x="1165" y="190" style="fill:var(--l-agent)">3.08% —— 真实生产数据</text></g>'
           '<path class="dw" style="--len:120;--i:1" d="M1180 78 V182" stroke="var(--hair-strong)" '
           'stroke-width="1" stroke-dasharray="4 8" fill="none"/>'
           '<text class="big pop" style="--i:2;fill:var(--l-agent)" x="1230" y="146">2.05×</text>'
           '</g>'
           '<g data-step="2"><text class="lbl pop" style="--i:0" x="320" y="270">'
           'AI ÷ 人 = 2.05 倍 · 日均营销转化率 · CONVOAI 电话智能体生产数据</text></g>'
           '</svg></div>')
page("content", 2, "".join([
    sh("flow kk ag", "left:120px;top:92px;width:1680px;height:28px", "AGENT · 日均营销转化率 · OUTPERFORMING HUMANS"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "已经超越<strong class='ag'>真人销冠</strong>。"),
    sh("flow sub", "left:120px;top:252px;width:1200px;height:40px", "真实生产数据 · 同场景同口径对比"),
    sh("flow", "left:120px;top:360px;width:1680px;height:311px", _p16fig),
    sh("flow", "left:120px;top:840px;width:1680px;height:110px",
       '<div class="land">不再是「AI 能否替代人工」的问题。<br>是「人工能否追上 AI」的问题了。</div>', step=2),
]))

# P17 · 五维金标准（锁定文案 · inspire26 p17 五行 .rows 逐字）
#   读法：不做会出什么事故 → 我们用什么兜底；03 安全为全页唯一的红（coral）
_FIVE = [
    ("01", "运行时", "数据串租户 / 突增拖垮邻居 / 海外扩容等几周 → 全球 SD-RTN 200+ 节点 · RTE 30000+ 终端适配", False),
    ("02", "记忆",   "5 轮就忘订单号 / 检索 1–2 秒节奏崩 / 知识更新慢念旧政策 → 毫秒级分层记忆 RAG 端到端", False),
    ("03", "安全",   "法务风控签不了字 / 监管要审计日志拿不出 / 海外数据驻留违规 → 99.99% · SOC 2 / GDPR · SLA 赔付", True),
    ("04", "工具",   "说了「改地址」其实啥也没改 / 出错无法回滚 / 协议私有接一个重写一次 → MCP + Function Call 开放栈", False),
    ("05", "弹性",   "双 11 / 春节直接挂 / 单供应商挂服务全挂 / 没 SLA 赔付损失不赔 → 900 亿分钟 RTE 月均支撑", False),
]
page("content", 1, "".join([
    sh("flow kk ag", "left:120px;top:92px;width:1680px;height:28px",
       "AGENT · 五维金标准 · 不做会出什么事故 → 我们用什么兜底"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "企业级智能体，必须做的 <strong class='ag'>5 件事</strong>。"),
    sh("", "left:120px;top:345px;width:1680px;height:410px",
       '<div class="rows">' + "".join(
           '<div class="r flow%s" style="--i:%d;padding:24px 0">'
           '<span class="n" style="color:var(--%s)">%s</span>'
           '<span class="k" style="color:var(--%s)">%s</span><span class="v">%s</span></div>'
           % (" hot" if _hot else "", 2 + _i, "coral" if _hot else "l-agent", _no,
              "coral" if _hot else "l-agent", _n, _v)
           for _i, (_no, _n, _v, _hot) in enumerate(_FIVE)) + '</div>'),
    sh("flow", "left:120px;top:850px;width:1680px;height:70px",
       '<div class="land">5 件事少做一件——'
       '<strong style="color:var(--l-agent)">智能体就不算企业级</strong>。</div>', step=1),
]))

# P18 · Call Agent 12 项能力（锁定文案）
_G12 = [
    ("01", "SIP / PSTN 全打通", "国内主流运营商 + 海外接入"),
    ("02", "Warm Transfer", "无缝转人工 · 上下文同步"),
    ("03", "WhatsApp 接入", "语音 + 文本一体"),
    ("04", "LATAM SIP", "拉美出海首选"),
    ("05", "海外多供应商", "ASR / LLM / TTS 全链路兜底"),
    ("06", "静态填充词", "思考间隙更自然"),
    ("07", "Campaign A/B", "生产级 A/B Test"),
    ("08", "时区 · 号码前缀", "全球部署即开即用"),
    ("09", "音色复刻", "品牌音色一致性"),
    ("10", "优雅打断 2.0", "CAN + 语义 + 声学融合"),
    ("11", "声纹识别", "说话人区分 / 反欺诈"),
    ("12", "实时情绪识别", "响应策略动态调整"),
]
page("content", 1, "".join(
    [sh("flow kk ag", "left:120px;top:92px;width:1680px;height:28px", "AGENT · CALL AGENT · 产品能力全景"),
     sh("ink hh", "left:120px;top:148px;width:1300px;height:100px", "12 项能力，<strong class='ag'>一体化</strong>交付。"),
     sh("flow mono-sm", "left:1440px;top:190px;width:360px;height:24px;text-align:right", "客服 + 外呼 + 全球部署")]
    # 12 卡 .rise 成对错峰（--i 2,2,3,3…7,7）从左上向右下推波；第 10 张「优雅打断 2.0」高亮
    + [sh("rise card-c g12", "left:%dpx;top:%dpx;width:396px;height:178px;--i:%d%s"
          % (120 + (_i % 4) * 428, 310 + (_i // 4) * 206, 2 + _i // 2,
             ";border-color:color-mix(in srgb,var(--l-agent) 45%,transparent);"
             "background:color-mix(in srgb,var(--l-agent) 9%,var(--card-bg))" if _i == 9 else ""),
          '<div class="no">%s</div><h3>%s</h3><p>%s</p>' % (_no, _n, _d))
       for _i, (_no, _n, _d) in enumerate(_G12)]
    + [sh("rise", "left:120px;top:958px;width:1680px;height:56px;font:700 30px/1.4 var(--f-cn);color:var(--ink)",
          "这不是能力清单——是<strong style='color:var(--l-agent)'>已经跑在客服一线的产品</strong>。", step=1)]))

# ═══ 支流三 · PHYSICAL AI（P19–P22 · 紫）═══════════════════════════════════

# P19 · PhysicalAI 章首（chapter-03 Constellation + T4 hero 底部家族）
page("ch-phys", 0, "".join([
    sh("flow kk ph", "left:120px;top:150px;width:1680px;height:28px;text-align:center", "支流三 · PHYSICAL AI · 对话式 AI 开发套件"),
    sh("ink", "left:120px;top:212px;width:1680px;height:120px;text-align:center;font:700 88px/1.2 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "让对话，<strong style='color:var(--l-phys)'>走出屏幕</strong>。"),
    sh("flow sub", "left:120px;top:892px;width:1680px;height:44px;text-align:center",
       "音箱、眼镜、桌面机器人、毛绒玩具——同一颗「临场引擎」。"),
    sh("flow mono-sm", "left:120px;top:966px;width:1680px;height:24px;text-align:center",
       "官网定位 · 面向具身智能与物理世界交互的实时智能方案"),
]), hero=("physical-family", None))

# P20 · 活人感（robot26 P17 一页化 · 叙事顺序为 Colin 拍板件：太木→太腻→恰好+图）
page("content", 4, "".join([
    sh("flow kk ph", "left:120px;top:80px;width:1680px;height:28px", "PHYSICAL AI · 「活人感」 · DEFINITION"),
    sh("ink hh", "left:120px;top:134px;width:1680px;height:90px;font-size:60px",
       "不是越像人越好，<strong class='ph'>是双方都能舒适</strong>。"),
    sh("settle strip", "left:360px;top:252px;width:1200px;height:432px",
       '<img class="lt" src="%scomfort-faces-light.png" alt="活人感三态">'
       '<img class="dk" src="%scomfort-faces.webp" alt="活人感三态" style="display:none">' % (R26, R26), step=3),
    sh("rise card-c face", "left:120px;top:716px;width:520px;height:186px",
       '<div class="en">TOO DRY</div><h3>太木</h3><p>正确，但没有关系温度。用户不想再开口。</p>', step=1),
    sh("rise card-c face good", "left:700px;top:716px;width:520px;height:186px",
       '<div class="en">JUST RIGHT</div><h3>恰好</h3><p>自然、可持续相处。下次还想跟它说话。</p>', step=3),
    sh("rise card-c face", "left:1280px;top:716px;width:520px;height:186px",
       '<div class="en">TOO CLINGY</div><h3>太腻</h3><p>伪装成朋友的销售感。三句之后想拔电源。</p>', step=2),
    sh("flow", "left:120px;top:940px;width:1680px;height:48px;text-align:center;font:400 26px/1.5 var(--f-cn);color:var(--ink)",
       "消费级机器人语境下：<strong style='color:var(--l-phys)'>活人感 = 角色立得住 + 临场撑得住</strong>。", step=4),
]))

# P21 · R1 开发套件（Global 率先发布 · 双形态 · 卡内 3 行 mono spec）
_SPEC = ('<div style="margin-top:24px;font:500 15px/1.95 var(--f-mono);letter-spacing:.06em;color:var(--ink-3)">'
         '%s</div>')
page("content", 1, "".join([
    sh("flow kk ph", "left:120px;top:92px;width:1680px;height:28px", "PHYSICAL AI · R1 开发套件 · GLOBAL FIRST"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px",
       "全球率先发布的<strong class='ph'>对话式 AI 硬件开发套件</strong>。"),
    sh("rise card-c", "left:120px;top:330px;width:816px;height:420px",
       '<div style="padding:44px 48px">'
       '<div class="mono-sm" style="color:var(--l-phys)">R1 · WI-FI · 2025.03.20 发布</div>'
       '<h3 style="margin:22px 0 16px;font:700 46px/1.2 var(--f-cn);color:var(--ink)">R1-WiFi</h3>'
       '<p style="font:400 22px/1.65 var(--f-cn);color:var(--ink-2)">面向家居与室内场景——音箱、桌宠、陪伴机器人，'
       '插上即获得可打断、低延迟的对话能力。</p>'
       + _SPEC % ('· 连接　Wi-Fi<br>· 场景　家居 / 室内<br>· 形态　音箱 · 桌宠 · 陪伴机器人') + '</div>'),
    sh("rise card-c", "left:984px;top:330px;width:816px;height:420px",
       '<div style="padding:44px 48px">'
       '<div class="mono-sm" style="color:var(--l-phys)">R1 · 4G · 2025.09.26 发布</div>'
       '<h3 style="margin:22px 0 16px;font:700 46px/1.2 var(--f-cn);color:var(--ink)">R1-4G</h3>'
       '<p style="font:400 22px/1.65 var(--f-cn);color:var(--ink-2)">走出 Wi-Fi 覆盖——户外、随身、车载与出海设备，'
       '4G 全移动场景同样的临场体验。</p>'
       + _SPEC % ('· 连接　4G 全移动<br>· 场景　户外 / 随身 / 车载<br>· 形态　出海设备 · 随身伴侣') + '</div>'),
    # 800 而非 820：避开背景板 y848–852 的 accent 细线（见 P2 注释）
    sh("rise", "left:120px;top:800px;width:1680px;height:60px;font:700 30px/1.4 var(--f-cn);color:var(--ink)",
       "从 Demo 到量产——R1 把「接入对话式 AI」变成<strong class='ph' style='color:var(--l-phys)'>开箱即用</strong>。", step=1),
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px", "SOURCE · 声网官网 · R1 公开发布信息"),
]))

# P22 · Robotics 1 · 机器人的临场引擎（.g3 三数字证据行）
_R1 = [
    ("200+",   "",                     "全球节点 · SD-RTN 软件定义实时网", "SD-RTN"),
    ("毫秒级",  "font-family:var(--f-cn);", "端到端往返 · 弱网最后一公里对抗", "LAST-MILE"),
    ("30000+", "",                     "芯片与整机适配 · 你的形态大概率已支持", "DEVICE ECOSYSTEM"),
]
page("content", 1, "".join([
    sh("flow kk ph", "left:120px;top:92px;width:1680px;height:28px", "PHYSICAL AI · ROBOTICS 1 · 机器人的临场引擎"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "临场感，是硬件的<strong class='ph'>生命线</strong>。"),
    sh("", "left:120px;top:380px;width:1680px;height:200px",
       '<div class="g3">' + "".join(
           '<div class="stat flow" style="--i:%d"><div class="v" style="%scolor:var(--l-phys)">%s</div>'
           '<div class="l">%s</div><div class="u">%s</div></div>' % (2 + _i, _ff, _v, _l, _u)
           for _i, (_v, _ff, _l, _u) in enumerate(_R1)) + '</div>'),
    sh("flow", "left:120px;top:700px;width:1680px;height:60px",
       '<div class="note">电梯、地库、户外弱网——临场不掉线，机器人才「接得上话」。</div>', step=1),
    # 794 而非 820：避开背景板 y848–852 的 accent 细线（见 P2 注释）
    sh("flow", "left:120px;top:794px;width:1680px;height:70px",
       '<div class="land">你做产品与角色，我们做<strong style="color:var(--l-phys)">临场与连接</strong>。</div>', step=1),
]))

# ═══ 案例 · 生态与客户（P23–P26）════════════════════════════════════════════

# P23 · 2026 生态全景（v1.2 修复版）
page("content", 1, "".join([
    sh("flow kk nt", "left:120px;top:80px;width:1680px;height:28px", "案例 · 2026 对话式 AI 生态全景 · LANDSCAPE"),
    sh("ink hh", "left:120px;top:134px;width:1680px;height:90px;font-size:60px", "我们在生态的<strong>哪一层</strong>？"),
    sh("settle frame", "left:280px;top:250px;width:1360px;height:765px",
       '<img src="%seco-2026.webp" alt="2026 对话式 AI 生态全景">' % A),
    sh("pop callout-chip", "left:320px;top:920px;width:auto;height:auto",
       "L0 连接 · L1 感知 · L2 运行时——<b>三层都有声网</b>", step=1),
    sh("flow mono-sm", "left:280px;top:1032px;width:1360px;height:22px",
       "五层价值地壳 · 代表性生态 · 事实截止 2026.08 · 研究口径见 colinyao.com 知识库"),
]))

# P24 · 案例 · 陪伴与情感
page("content", 0, "".join([
    sh("flow kk nt", "left:120px;top:92px;width:1680px;height:28px", "案例 · 陪伴与情感 · COMPANIONS IN PRODUCTION"),
    sh("ink hh", "left:120px;top:146px;width:1680px;height:90px;font-size:60px", "从毛绒到桌宠，<strong>陪伴先上岗</strong>。"),
    case_row(["jixian", "robopoet", "luwu", "pophie"], 280, 714),
    sh("flow mono-sm", "left:120px;top:1024px;width:1680px;height:22px", "声网官方联合案例 · 均已公开发布"),
]))

# P25 · 案例 · 助手与创作
page("content", 0, "".join([
    sh("flow kk nt", "left:120px;top:92px;width:1680px;height:28px", "案例 · 助手与创作 · IN-APP AGENTS"),
    sh("ink hh", "left:120px;top:146px;width:1680px;height:90px;font-size:60px", "App 里的对话式 AI，<strong>正在标配化</strong>。"),
    case_row(["sensetime", "minimax", "zhipu", "xingye", "lingji"], 280, 604),
    sh("flow mono-sm", "left:120px;top:1024px;width:1680px;height:22px", "声网官方联合案例 · 均已公开发布"),
]))

# P26 · 案例 · 眼镜、外教与新硬件
page("content", 0, "".join([
    sh("flow kk nt", "left:120px;top:92px;width:1680px;height:28px", "案例 · 眼镜、外教与新硬件 · NEW DEVICES"),
    sh("ink hh", "left:120px;top:146px;width:1680px;height:90px;font-size:60px", "下一个入口，<strong>已经量产</strong>。"),
    case_row(["looktech", "heycyan", "lookee", "lianou", "doushen"], 280, 604),
    sh("flow mono-sm", "left:120px;top:1024px;width:1680px;height:22px", "声网官方联合案例 · 均已公开发布"),
]))

# ═══ 合流 · 为什么是声网（P27–P29）══════════════════════════════════════════

# P27 · 同一个底座（T5 hero 半球在底部 · 有意贴边构图，不裁切）
page("content", 1, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "合流 · 同一个底座 · SD-RTN"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "三条支流，<strong>一条河</strong>。"),
    sh("rise", "left:120px;top:300px;width:1680px;height:56px;font:700 26px/1.5 var(--f-cn);color:var(--ink-2)",
       dot("l-eng") + "Engine 的每一次打断　" + dot("l-agent") + "Agent 的每一通电话　" + dot("l-phys") + "Physical AI 的每一次唤醒"),
    sh("flow", "left:120px;top:392px;width:1680px;height:60px;font:400 26px/1.6 var(--f-cn);color:var(--ink)",
       "都跑在同一张 <strong style='color:var(--accent)'>SD-RTN 软件定义实时网络</strong>上——全球 200+ 节点，端到端毫秒级。"),
    sh("pop callout-chip", "left:710px;top:610px;width:auto;height:auto", "一张网 · 三条产品线 · 同一个临场标准", step=1),
]), hero=("network-globe", None))

# P28 · 中立性（.rows 三行）
_NEU = [
    ("01", "不做 C 端 App",     "不和你的产品竞争用户——你的用户永远是你的。"),
    ("02", "不做自有硬件品牌",   "R1 是开发套件，不是消费品——我们停在你需要的那一层。"),
    ("03", "不训基座大模型",     "多供应商开放，谁好用接谁——模型进步全部归你享受。"),
]
page("content", 1, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "合流 · 为什么是声网 · NEUTRALITY"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "我们<strong>不抢</strong>客户的生意。"),
    sh("", "left:120px;top:360px;width:1680px;height:300px",
       '<div class="rows">' + "".join(
           '<div class="r flow" style="--i:%d;padding:32px 0"><span class="n">%s</span>'
           '<span class="k" style="width:300px">%s</span>'
           '<span class="v" style="font-size:23px">%s</span></div>' % (2 + _i, _no, _n, _d)
           for _i, (_no, _n, _d) in enumerate(_NEU)) + '</div>'),
    sh("flow", "left:120px;top:800px;width:1680px;height:80px",
       '<div class="land">中立，是基础设施的第一美德——'
       '<strong style="color:var(--accent)">OpenAI 选择我们，也是这个原因</strong>。</div>', step=1),
]))

# P29 · 收束金句（回收封面句）
page("quote", 1, "".join([
    sh("ink q-big", "left:120px;top:380px;width:1680px;height:300px",
       "让每一次人机对话，<br>都像<strong>真人</strong>一样自然。"),
    sh("rise", "left:120px;top:780px;width:1680px;height:56px;text-align:center;font:500 28px/1.6 var(--f-cn);color:var(--ink-2)",
       "这句话，三条产品线各自兑现一遍——" + dot("l-eng") + "能力　" + dot("l-agent") + "结果　" + dot("l-phys") + "入口",
       step=1),
]))

# ═══ 收尾（P30–P31）═════════════════════════════════════════════════════════

# P30 · 合作路径
page("content", 0, "".join(
    [sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "收尾 · 合作路径 · NEXT STEPS"),
     sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "三步，从今天到<strong>上线</strong>。")]
    + [sh("rise card-c", "left:%dpx;top:330px;width:536px;height:480px" % (120 + _i * 572),
          '<div style="padding:40px 42px">'
          '<div class="mono-sm" style="color:var(--accent)">%s</div>'
          '<h3 style="margin:20px 0 16px;font:700 40px/1.2 var(--f-cn);color:var(--ink)">%s</h3>'
          '<p style="font:400 22px/1.65 var(--f-cn);color:var(--ink-2)">%s</p></div>' % (_t, _n, _d))
       for _i, (_t, _n, _d) in enumerate([
           ("STEP 1 · 今天", "注册即用", "Console 开通对话式 AI 引擎——免费额度，当天就能听到第一句回话。"),
           ("STEP 2 · 两周", "PoC 共建", "工程团队陪跑，把你的第一个真实场景跑通——不是 Demo，是可上线雏形。"),
           ("STEP 3 · 一个季度", "规模化上线", "SLA、全球部署、多供应商兜底——从 PoC 进入生产，随业务弹性扩展。"),
       ])]
    # 卡间 36px 空隙里的连接箭头（656–692 / 1228–1264），y 居卡中
    + [sh("flow", "left:%dpx;top:560px;width:36px;height:24px" % _x,
          '<div class="fig"><svg viewBox="0 0 60 24" style="width:100%;height:auto">'
          '<path class="dw" style="--len:40" d="M4 12 H44" stroke="var(--hair-strong)" stroke-width="1.5" fill="none"/>'
          '<polygon class="fill-ink" points="44,5 58,12 44,19"/></svg></div>')
       for _x in (656, 1228)]
    + [sh("flow mono-sm", "left:120px;top:900px;width:1680px;height:24px",
          "任何一步遇到问题——直接找我。")]))

# P31 · 谢谢（title 板收尾）
page("title", 0, "".join([
    sh("ink", "left:120px;top:380px;width:1680px;height:200px;text-align:center;font:700 130px/1.15 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "谢谢。"),
    sh("rise", "left:120px;top:640px;width:1680px;height:40px;text-align:center;font:700 24px/1 var(--f-mono);letter-spacing:.08em;color:var(--ink-2)",
       dot("l-eng") + "ENGINE　" + dot("l-agent") + "AGENT　" + dot("l-phys") + "PHYSICAL AI"),
    sh("flow sub", "left:120px;top:750px;width:1680px;height:44px;text-align:center",
       "姚光华 Colin · 声网 AI 产品线负责人"),
    sh("flow mono-sm", "left:120px;top:830px;width:1680px;height:24px;text-align:center",
       "SHENGWANG.CN · COLINYAO.COM"),
]))

# ═══ 组装 ═══════════════════════════════════════════════════════════════════
def build():
    total = len(PAGES)
    secs = []
    for i, (board, steps, body, hero) in enumerate(PAGES, 1):
        sig = '<div class="sig">%d/%d</div>' % (i, total)
        hero_html = ""
        if hero:
            name, style = hero
            st = ' style="%s"' % style if style else ""
            hero_html = ('<img class="hero-art lt" src="%shero/hero-%s-light.png" alt=""%s>'
                         '<img class="hero-art dk" src="%shero/hero-%s-dark.png" alt=""%s>'
                         % (A, name, st, A, name, st))
        secs.append(
            '<section class="slide conf-boarded" data-p="%d" data-steps="%d">\n'
            '  <div class="conf-bg conf-bg-%s" aria-hidden="true"></div>%s\n'
            '  <div class="pp">%s%s</div>\n</section>' % (i, steps, board, hero_html, sig, body))
    chrome = ('<div class="deck-grid" aria-hidden="true"></div>'
              '<div class="deck-rail t" aria-hidden="true"></div>'
              '<div class="deck-rail b" aria-hidden="true"></div>')
    doc = (
        '<!DOCTYPE html>\n<html lang="zh-CN"><head>\n'
        '<script>try{if(localStorage.getItem("colin-theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}</script>\n'
        '<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>声网对话式 AI · 公司与产品矩阵 · 姚光华 Colin</title>\n'
        + FONTS
        + "<style>" + css("conf-theme-dual.css") + "</style>"
        + "<style>" + css("stage.css") + "</style>"
        + "<style>" + css("motion.css") + "</style>"
        + "<style>" + css("components.css") + "</style>"
        + "<style>" + css("conf-chrome.css").split("<svg class=\"deck-flow\"")[0] + "</style>"   # 流场退役：只取 CSS，不取流场 SVG
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
        'border-radius:3px;padding:7px 12px;opacity:.5;transition:opacity .3s;background:transparent;cursor:pointer;}'
        '.deck-swap:hover{opacity:1;color:var(--accent);border-color:var(--accent);}'
        '@media print{.deck-swap{display:none!important;}}</style>\n'
        "<script>" + (SRC / "deck.js").read_text(encoding="utf-8") + "</script>\n"
        '<script>(function(){var b=document.getElementById("deckSwap");'
        'function apply(t){if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");b.textContent="浅底";}'
        'else{document.documentElement.removeAttribute("data-theme");b.textContent="暗底";}'
        'document.querySelectorAll(".strip img.lt").forEach(function(el){el.style.display=(t==="dark")?"none":"block";});'
        'document.querySelectorAll(".strip img.dk").forEach(function(el){el.style.display=(t==="dark")?"block":"none";});}'
        'var cur="light";try{cur=localStorage.getItem("colin-theme")||"light";}catch(e){}apply(cur);'
        'b.addEventListener("click",function(){cur=(cur==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",cur);}catch(e){}apply(cur);});})();</script>\n'
        "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")
    assert total == 31, "页数漂移：%d != 31" % total
    print("convoai.html · %d 页 · %dKB · conf-light 默认" % (total, len(doc) // 1024))

if __name__ == "__main__":
    build()
