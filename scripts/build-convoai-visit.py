#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-visit.py · 《声网对话式 AI · 公司与产品矩阵》初次拜访客户 deck
# CONF 家族 · conf-light 默认 · 单文件双主题 · 背景板节奏 · 三线三色
# 结构（方案 A · Colin 2026-08-12 拍板）：
#   序幕(5) → 矩阵(3) → Engine(5) → Agent(5) → PhysicalAI(4) → 案例(4) → 合流(3) → 收尾(2)
# 口径纪律：只用公开可查证数字；Phone Agent 用「Global 率先发布」；点名 LiveKit。
# ═══════════════════════════════════════════════════════════════════════════
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
OUT = ROOT / "public" / "decks" / "convoai.html"
A = "/decks/assets/convoai/"
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

# ── 本 deck 专属 CSS（三线三色 + 页型件）────────────────────────────────────
DECK_CSS = """<style id="convoai-deck">
/* 绝对画布 shape 层（robot26 惯例；reference 栈是语义排版系，缺这两行） */
.pp{position:absolute;inset:0;}
.pp .sh{position:absolute;overflow:visible;}
:root{--l-eng:var(--accent);--l-agent:#5b8cff;--l-phys:#7b61ff;}
html[data-theme="dark"]{--l-agent:#6e96ff;--l-phys:#b78cf0;}
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 15px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--sig-ink);}
.kk{font:700 20px/1 var(--f-mono);letter-spacing:.28em;color:var(--accent);}
.kk .dot{display:inline-block;width:12px;height:12px;border-radius:3px;margin:0 10px -1px 0;}
.hh{font:700 68px/1.16 var(--f-cn);letter-spacing:-.02em;color:var(--ink);}
.hh strong{color:var(--accent);}
.sub{font:400 26px/1.55 var(--f-cn);color:var(--ink-2);}
.mono-sm{font:500 15px/1.4 var(--f-mono);letter-spacing:.08em;color:var(--ink-3);}
.kpi{background:var(--card-bg);border:1px solid var(--hair);border-radius:20px;padding:34px 38px;}
.kpi .tag{font:700 15px/1 var(--f-mono);letter-spacing:.18em;color:var(--accent);}
.kpi .num{margin-top:22px;font:900 92px/1 var(--f-cn);letter-spacing:-.03em;color:var(--ink);}
.kpi .num small{font:700 34px/1 var(--f-cn);letter-spacing:0;}
.kpi .cap{margin-top:14px;font:400 20px/1.45 var(--f-cn);color:var(--ink-2);}
.line-eng{--lc:var(--l-eng)}.line-agent{--lc:var(--l-agent)}.line-phys{--lc:var(--l-phys)}
</style>"""

# ── 组装件 ──────────────────────────────────────────────────────────────────
def sh(cls, style, body, step=None, sid=None):
    a = ' data-sid="%s"' % sid if sid else ""
    a += ' data-step="%d"' % step if step is not None else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (cls, a, style, body)

PAGES = []          # (board, steps, body_html)
def page(board, steps, body):
    PAGES.append((board, steps, body))

# ═══ 序幕 · 公司信任状 ═══════════════════════════════════════════════════════

# P1 · 封面
page("title", 0, "".join([
    sh("flow kk", "left:120px;top:200px;width:1400px;height:28px",
       "AGORA · 声网 · CONVERSATIONAL AI"),
    sh("ink", "left:120px;top:266px;width:1560px;height:250px;font:700 96px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "让每一次人机对话，<br>都像<strong style='color:var(--accent)'>真人</strong>一样自然。"),
    sh("flow sub", "left:120px;top:600px;width:1400px;height:44px",
       "声网 · 对话式 AI 产品矩阵 —— 公司与三条产品线"),
    sh("rise", "left:120px;top:700px;width:1500px;height:56px;font:700 26px/1 var(--f-mono);letter-spacing:.06em;color:var(--ink-2)",
       '<span class="dot" style="display:inline-block;width:14px;height:14px;border-radius:4px;background:var(--l-eng);margin-right:12px"></span>ENGINE'
       '<span class="dot" style="display:inline-block;width:14px;height:14px;border-radius:4px;background:var(--l-agent);margin:0 12px 0 56px"></span>AGENT'
       '<span class="dot" style="display:inline-block;width:14px;height:14px;border-radius:4px;background:var(--l-phys);margin:0 12px 0 56px"></span>PHYSICAL AI'),
    sh("flow mono-sm", "left:120px;top:930px;width:1200px;height:24px",
       "主讲人：姚光华 Colin · 声网 AI 产品线负责人"),
]))

# P2 · RTE 领导者（锁定文案 · 官网/IR 口径）
page("content", 0, "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "序幕 · 声网 RTE · REAL-TIME ENGAGEMENT"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:100px", "RTE 行业的<strong>领导者</strong>。"),
    sh("rise kpi", "left:120px;top:330px;width:396px;height:340px",
       '<div class="tag">市场占有率</div><div class="num">No.1</div><div class="cap">市场占有率稳居第一，份额超过第 2–8 位总和</div>'),
    sh("rise kpi", "left:548px;top:330px;width:396px;height:340px",
       '<div class="tag">技术突破</div><div class="num">50<small>+</small></div><div class="cap">突破性自主创新技术（全球发明专利）</div>'),
    sh("rise kpi", "left:976px;top:330px;width:396px;height:340px",
       '<div class="tag">开发者生态</div><div class="num">100<small>万+</small></div><div class="cap">全球注册应用数</div>'),
    sh("rise kpi", "left:1404px;top:330px;width:396px;height:340px",
       '<div class="tag">生产规模</div><div class="num">900<small>亿+</small></div><div class="cap">单月支撑通话分钟数</div>'),
    sh("flow mono-sm", "left:120px;top:1015px;width:1680px;height:24px", "SOURCE · 声网官网 / IR 口径 · 2026"),
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
        '<button class="deck-swap" id="deckSwap">暗底</button>\n'
        '<style>.deck-swap{position:fixed;left:26px;bottom:24px;z-index:1100;font-family:var(--f-mono,monospace);'
        'font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);'
        'border-radius:3px;padding:7px 12px;opacity:.5;transition:opacity .3s;background:transparent;cursor:pointer;}'
        '.deck-swap:hover{opacity:1;color:var(--accent);border-color:var(--accent);}'
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
    print("convoai.html · %d 页 · %dKB（骨架 · conf-light 默认）" % (total, len(doc) // 1024))

if __name__ == "__main__":
    build()
