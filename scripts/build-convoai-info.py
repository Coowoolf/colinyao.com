#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# build-convoai-info.py · 《声网对话式 AI · 一页一章 Infograph》拜访速讲版 deck
# CONF 家族 · conf-light 默认 · 单文件双主题 · 三线三色 —— 与 build-convoai-visit.py 同源
# 结构（8 页 · 讲者不翻页、不点击，一页讲透一章）：
#   P1 封面 → P2 公司 → P3 矩阵 → P4 Engine → P5 Agent → P6 PhysicalAI → P7 案例 → P8 合流
# 与 31 页版的差别只有三条：
#   ① 全部 data-steps=0（入场只靠 flow/rise/settle + --i 错峰，没有任何分步）
#   ② 背景板只用两张：P1 title / P2–P8 content（最安静的 matrix .42）
#   ③ hero-art 只留 P1 的 three-engines 盒装
# 口径纪律：所有数字与句子从 build-convoai-visit.py 逐字复制，一个不新造。
# Infograph 版式语言：页内 2–4 个分区，分区间 1px var(--hair) 细线，
#   每分区一个 mono 小节标（「01 · SCALE」14px letter-spacing .18em ink-3）。
# ── 踩过的坑（移植 SVG 必守，见 optim/mining-report.md §6）───────────────────
#   · svg 一律 style="width:100%;height:auto"，且 .sh 高度 = width×viewBoxH/viewBoxW，
#     否则 stage.css 的 svg{max-height:100%} 会把图压扁 / .sh 装不下会被 clip-path 切掉
#   · .dw 的 --len 必须≈路径长度，否则线不出来
#   · SVG 里换色一律写内联 style="fill:…"，呈现属性 fill= 压不过 .fig .lbl/.ttl 的 CSS fill
#   · content 背景板自带一条 accent 细线在 y848–852（x120–761）：那一带不放文字，
#     否则字形正压在线上 = 被划掉的观感
# ═══════════════════════════════════════════════════════════════════════════
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "assets" / "convoai-src"
OUT = ROOT / "public" / "decks" / "convoai-info.html"
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

# ── 背景板（速讲版只用两张：title + content）─────────────────────────────────
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

# ── 本 deck 专属 CSS（与 convoai.html 同源，删掉速讲版用不到的件）────────────
DECK_CSS = """<style id="convoai-info-deck">
/* 绝对画布 shape 层（robot26 惯例；reference 栈是语义排版系，缺这两行） */
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
.sig{position:absolute;right:120px;top:47px;z-index:2;font:500 15px/1 var(--f-mono);
  letter-spacing:.12em;color:var(--sig-ink);}
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
/* 版本轴 tick（P4）*/
.vt{width:3px;background:var(--ink-3);opacity:.55;}
.vt.big{background:var(--l-eng);opacity:1;width:5px;}
.tl-line{background:var(--hair);height:3px;}
/* 主题词 chip */
.chip{display:inline-block;margin:0 12px 12px 0;padding:11px 18px;border:1px solid var(--hair);
  border-radius:999px;background:var(--card-bg);font:500 18px/1 var(--f-cn);color:var(--ink-2);}
/* 能力宫格（P5 · 6×2）*/
.cap{border:1px solid var(--hair);border-radius:999px;background:var(--card-bg);
  font:500 16px/1 var(--f-cn);color:var(--ink-2);padding:10px 8px;text-align:center;}
.cap.on{border-color:color-mix(in srgb,var(--l-agent) 55%,transparent);
  background:color-mix(in srgb,var(--l-agent) 10%,var(--card-bg));color:var(--ink);}
/* 三态卡（活人感 · P6）*/
.face{padding:22px 24px;border-top:5px solid var(--ink-3);}
.face .en{font:700 13px/1 var(--f-mono);letter-spacing:.2em;color:var(--ink-3);}
.face h3{margin:10px 0 8px;font:700 30px/1.2 var(--f-cn);color:var(--ink);}
.face p{font:400 17px/1.5 var(--f-cn);color:var(--ink-2);}
.face.good{border-top-color:var(--l-phys);}
.face.good h3{color:var(--l-phys);}
/* 移植 inspire26/dual26 版式：.fig 内的 SVG 走 width:100%;height:auto，
   必须解掉 stage.css 的 svg{max-width:100%;max-height:100%}，否则定高 .sh 里会被压扁 */
.fig svg{max-width:none;max-height:none;}
/* ═══ 视觉升级 R1（GPT 5.6 · 合入 2026-08-13）· P7 生态全景 + 案例墙 ═══════
   生态图回到位图，但和 2026-08-12 退役的那张 eco-2026.webp 有三点不同：
     ① 浅/深两张同构双源，走 .hero-art 的同一套 CSS 主题切换（不是烧死主题的单图）；
     ② 图本身不承载小字：五层 L4–L0 的中英文全部是 DOM 叠层，字号可控、可维护；
     ③ 只做远景底纹，正文对比度由 .eco-layer 的半透明卡背 + backdrop-blur 兜。 */
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
/* polish-v4：.94 是全景底纹时代的柔化（图只当远景纹理，压低免得抢字）。
   换成专门生成的五层生态主视觉后，图本身就是这一列的主角，必须全锐度出图。 */
.eco-art.lt{display:block;opacity:1;}
html[data-theme="dark"] .eco-art.lt{display:none;}
html[data-theme="dark"] .eco-art.dk{display:block;}
/* kicker 的尾巴正落在全景图那排设备剪影上（文字压图不算遮盖，但会掉对比度）：
   给一圈和面板底色同色的柔光，两主题下都把字从图里拎出来。 */
.eco-kicker{position:absolute;left:28px;top:22px;font:600 12px/1 var(--f-mono);
  letter-spacing:.2em;color:var(--ink-3);text-shadow:0 0 7px var(--eco-surface),0 0 3px var(--eco-surface);}
.eco-layer{position:absolute;left:24px;right:24px;height:67px;padding:12px 18px;
  display:grid;grid-template-columns:58px 230px 1fr;align-items:center;gap:12px;
  border:1px solid color-mix(in srgb,var(--ink-3) 22%,transparent);border-radius:12px;
  /* 玻璃模糊会把生态底图磨成不可读的雾；改用不透明层，保留底图锐度与层级。（该规则实际已被下方 P7 override 全透明化，留作兜底） */
  background:color-mix(in srgb,var(--card-bg) 88%,transparent);backdrop-filter:none;}
.eco-layer .eco-code{font:600 13px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);}
.eco-layer b{font:700 22px/1 var(--f-cn);color:var(--ink);}
.eco-layer small{font:400 13px/1.35 var(--f-cn);color:var(--ink-2);text-align:right;}
.eco-layer.l2,.eco-layer.l1,.eco-layer.l0{border-color:color-mix(in srgb,var(--accent) 55%,transparent);}
.eco-layer.l2 .eco-code,.eco-layer.l2 b,.eco-layer.l1 .eco-code,.eco-layer.l1 b,
.eco-layer.l0 .eco-code,.eco-layer.l0 b{color:var(--accent);}
/* 行距 83 = 带高 67 + 16 净空：行间、与 kicker（top22 · 12px）之间都不许互压 */
.eco-layer.l4{top:54px;}.eco-layer.l3{top:137px;}.eco-layer.l2{top:220px;}
.eco-layer.l1{top:303px;}.eco-layer.l0{top:386px;}
html[data-theme="dark"] .eco-layer{background:rgba(10,12,24,.86);}
/* 案例墙 v2：3 张精选大卡 + 11 张证据小卡；客户名走 DOM 文本，不靠海报正文缩略 */
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
/* 底部压幕：升级版原式（transparent 42%→.84）在 caption 那一带只压到 .58，
   海报自己烧录的品牌名正好在同一位置，和 DOM caption 叠成重影。加一段中间色标，
   把最后 ~20% 压到 .93，海报文字变淡影、白字浮出来。 */
.case-feature:after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 38%,rgba(10,12,24,.5) 68%,rgba(10,12,24,.93) 100%);}
.case-feature-caption{position:absolute;left:12px;right:10px;bottom:10px;z-index:1;color:#fff;}
/* components.css 的 `b,strong{color:var(--ink)}`（0,0,1）直接命中这个 b，压过 caption 的
   继承白 —— 浅底主题下客户名会被染成近黑，正好压在深色幕布上隐形（.callout-chip 同一个坑）。*/
.case-feature-caption b{display:block;font:700 16px/1.15 var(--f-cn);color:inherit;}
.case-feature-caption span{display:block;margin-top:4px;font:500 10px/1 var(--f-mono);
  letter-spacing:.1em;color:rgba(255,255,255,.7);}
.case-index{display:flex;align-items:center;gap:10px;margin:17px 0 9px;
  font:500 11px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);}
.case-index:after{content:"";height:1px;flex:1;background:var(--hair);}
/* 4 列 × 3 行（升级版是 6×2 · 94×83）：11 张卡在 644 宽的墙里排 6 列时，
   墙底会空出 217px 的白洞，而且 9px 的客户名在讲台上读不出来。
   改 4 列 145×124 后墙高正好落在 977（= 左列脚注底 = 我版基线），名字提到 11px。 */
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
/* 案例卡（旧 5 列缩略图网格，随 R1 案例墙退役；.case 保留给回滚基线） */
.case{border-radius:14px;overflow:hidden;border:1px solid var(--hair);
  box-shadow:0 8px 22px rgba(0,0,0,.12);background:var(--card-bg);}
.case img{width:100%;height:100%;object-fit:cover;display:block;}
/* .frame（白底图框）随 P7 位图生态图一起退役，2026-08-12 */
.callout-chip{background:var(--ink);color:var(--bg,#fff);border-radius:12px;padding:13px 22px;
  font:700 19px/1.4 var(--f-cn);box-shadow:0 8px 24px rgba(0,0,0,.22);}
html[data-theme="dark"] .callout-chip{background:#f5f5f4;color:#111;}
/* components.css 的 `b,strong{color:var(--ink)}`（0,0,1）压过 .callout-chip 的继承色 →
   深底 chip 里的 <b> 会被染成 --ink（近黑）而在近黑底上隐形（原 convoai P23 就是这个哑火）。
   同特异度以上把它拉回继承。 */
.callout-chip b,.callout-chip strong{color:inherit;}
/* 编辑热区（deck.js 依赖） */
.edit-hotzone{position:fixed;top:0;left:0;width:120px;height:80px;z-index:10000;}
.edit-toggle{position:fixed;top:18px;left:18px;z-index:10001;opacity:0;pointer-events:none;
  font:500 12px/1 var(--f-mono);letter-spacing:.14em;color:var(--ink-3);
  border:1px solid var(--hair);border-radius:3px;padding:7px 12px;background:transparent;cursor:pointer;
  transition:opacity .3s;}
.edit-toggle.show,.edit-toggle.active{opacity:1;pointer-events:auto;}
.edit-toggle.active{border-color:var(--accent);color:var(--accent);}
@media print{.edit-toggle,.edit-hotzone,.deck-progress,.deck-steps,.deck-swap{display:none!important;}}
/* polish-v3：仅提升投影距离下的 P5 可读性，不改内容/数据/布局 */
[data-p="5"] .seclab{color:var(--ink-2);font-weight:600;}
[data-p="5"] .fig .lbl{fill:var(--ink-2);font-weight:600;}
[data-p="5"] .fig .sm,[data-p="5"] .fig .txt,[data-p="5"] .rows .r .v{font-weight:400;}
[data-p="5"] .fig .box{fill:color-mix(in srgb,var(--card-bg) 90%,var(--ink) 10%);stroke:color-mix(in srgb,var(--ink) 26%,transparent);}
/* polish-v4 · P7：完整五层生态主视觉 + 左右留白 DOM 标注，不再用五条高不透明卡片遮图。
   仲裁适配：v4 原稿用 background-image 承载底图，此处改回 .eco-art 双源 img（保 QA ⑩ 缺图断言与 P1 hero 同机制），视觉等价。 */
[data-p="7"] .eco-visual{
  border:1px solid color-mix(in srgb,var(--ink) 16%,transparent);
  background-color:#f8f9fc;
  box-shadow:0 18px 44px rgba(11,14,28,.08);}
html[data-theme="dark"] [data-p="7"] .eco-visual{
  background-color:#050713;}
/* token 清账：五行文字的柔光 text-shadow 用 --eco-surface，深色下旧值 #10111c 是全景图时代的
   面板底；v4 面板底改 #050713 后在 P7 范围内对齐，避免字周柔光比底亮一档。 */
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
html[data-theme="dark"] [data-p="7"] .callout-chip{
  background:transparent;color:var(--ink);}
[data-p="7"] .callout-chip b{color:var(--accent);}
/* ═══ 引擎详解抽屉（2026-08-18）· P4 「04 · OPEN」行的第 5 个 chip + 视口级 overlay ═══ */
/* 触发 chip：形制与 .chip 家族一字不差，只把描边/文字换成 accent，把「可点」说清楚。
   全部走 token（--accent / --card-bg），浅深两主题同一套规则各自成立。 */
.chip-expand{border-color:color-mix(in srgb,var(--accent) 52%,transparent);
  color:var(--accent);cursor:pointer;-webkit-user-select:none;user-select:none;
  transition:background .15s ease,border-color .15s ease;}
.chip-expand:hover,.chip-expand:focus-visible{
  background:color-mix(in srgb,var(--accent) 14%,var(--card-bg));
  border-color:color-mix(in srgb,var(--accent) 80%,transparent);}
/* 引擎详解抽屉：视口级 overlay（避开舞台 transform，原生控件/iframe 都不吃缩放坐标系的亏） */
/* z 必须盖过 .deck-progress(1000)/.deck-swap(1100)/.edit-hotzone(10001)——
   抽屉开着时进度条不上浮、编辑热区不可误触（Opus 自查发现，Fable 裁定收） */
#engineOverlay{position:fixed;inset:0;z-index:10002;}
#engineOverlay[hidden]{display:none;}
.eo-scrim{position:absolute;inset:0;background:rgba(6,8,18,.78);}
.eo-sheet{position:absolute;inset:26px;border-radius:18px;overflow:hidden;
  border:1px solid rgba(255,255,255,.16);box-shadow:0 30px 90px rgba(0,0,0,.5);background:#e6e6eb;}
.eo-sheet iframe{display:block;width:100%;height:100%;border:0;}
.eo-close{position:absolute;top:14px;right:16px;font:600 12px/1 var(--f-mono);letter-spacing:.14em;
  color:#f5f5f7;background:rgba(10,10,15,.55);border:1px solid rgba(255,255,255,.22);
  border-radius:999px;padding:9px 14px;cursor:pointer;}
.eo-close:hover{background:rgba(10,10,15,.8);}
</style>"""

# ── 组装件 ──────────────────────────────────────────────────────────────────
def sh(cls, style, body, step=None, sid=None):
    a = ' data-sid="%s"' % sid if sid else ""
    a += ' data-step="%d"' % step if step is not None else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (cls, a, style, body)

def dot(var):
    return '<span class="dot" style="background:var(--%s)"></span>' % var

def rule(y, x=120, w=1680, i=1):
    """分区之间的 1px 细线（高度 1px → 扫描器不当它是覆盖块）"""
    return sh("spread hair-rule", "left:%dpx;top:%dpx;width:%dpx;height:1px;--i:%d" % (x, y, w, i), "")

def lab(x, y, txt, w=620, col=None, i=0):
    """mono 小节标：「01 · SCALE」"""
    c = ";color:%s" % col if col else ""
    return sh("flow seclab", "left:%dpx;top:%dpx;width:%dpx;height:20px;--i:%d%s" % (x, y, w, i, c), txt)

def figbox(x, y, w, vbw, vbh, inner, cls="flow", i=0):
    """SVG 装盒：.sh 高度按 viewBox 等比算死，svg 一律 width:100%;height:auto"""
    h = round(w * vbh / vbw)
    return sh(cls, "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d" % (x, y, w, h, i),
              '<div class="fig"><svg viewBox="0 0 %d %d" style="width:100%%;height:auto">%s</svg></div>'
              % (vbw, vbh, inner))

PAGES = []          # (board, steps, body_html, hero)
def page(board, body, hero=None):
    PAGES.append((board, 0, body, hero))     # 速讲版：全部 data-steps=0

# ═══ P1 · 封面（title 板 + hero 盒；照抄 convoai P1，只改 kk 尾巴与 sub）═════
page("title", "".join([
    sh("flow kk", "left:120px;top:200px;width:1400px;height:28px",
       "AGORA · 声网 · CONVERSATIONAL AI · INFOGRAPH"),
    sh("ink", "left:120px;top:266px;width:1100px;height:250px;font:700 96px/1.22 var(--f-cn);letter-spacing:-.02em;color:var(--ink)",
       "让陪伴自然，<br>让生意<strong style='color:var(--accent)'>成单</strong>。"),
    sh("flow sub", "left:120px;top:600px;width:1400px;height:44px",
       "声网 · 对话式 AI —— 一页一章 · 拜访速讲版"),
    sh("rise", "left:120px;top:700px;width:1500px;height:56px;font:700 26px/1 var(--f-mono);letter-spacing:.06em;color:var(--ink-2)",
       dot("l-eng") + 'ENGINE<span style="margin-left:56px"></span>'
       + dot("l-agent") + 'AGENT<span style="margin-left:56px"></span>'
       + dot("l-phys") + 'PHYSICAL AI'),
    sh("flow mono-sm", "left:120px;top:930px;width:1200px;height:24px",
       "主讲人：姚光华 Colin · 声网 AI 产品线负责人"),
]), hero=("info-v2/hero-cover-v2", "left:720px;top:220px;width:1200px;height:675px"))
# ── P1 hero 盒（视觉升级 R1）─────────────────────────────────────────────────
#   原盒 left860+width1200=2060 出画布 140px，右侧被舞台裁掉 → 收到 720+1200=1920 正好齐右缘。
#   主标保持原句（Fable 裁定 #1）：升级版改的「让陪伴自然，让生意成单。」是未申报的内容改动，
#   且和 P8 收尾回收的同一句断裂，不采。
#   新图 2048×1152 透明底、右重心：实际墨迹从图内 x669 起（= 屏幕 x1112），
#   主标两行各 9 个全角字、右缘 x≈967 —— 中间还剩 145px 净空，宽标题与图不相撞。

# ═══ P2 · 公司 ·「RTE 领导者」（accent）════════════════════════════════════
#   01 SCALE 四数字 / 02 ADOPTION 近一半 + 分账条 / 03 ENDORSEMENT OpenAI / 04 MILESTONES 五节点
_RTE = [
    ("No.1",   "市场占有率稳居第一，份额超过第 2–8 位总和", True),
    ("50+",    "突破性自主创新技术（全球发明专利）",       False),
    ("100万+", "全球注册应用数",                          False),
    ("900亿+", "单月支撑通话分钟数",                      False),
]
# 五节点卡片时间轴 mini：P5 原图 viewBox 1620×340 / 框 300×200 太高，
# 按 spec 重排成 viewBox 1620×170 / 框 300×100，文字两行（日期 + 名称），细节行删
_MILE = [
    (  10, "2024.10.01", "全球首个 Realtime API", False),
    ( 330, "2024.10.24", "国内首个 Realtime API", False),
    ( 650, "2025.03.06", "引擎 1.0 + R1 GA",      False),
    ( 970, "2025.10.31", "产品全栈发布",           False),
    (1290, "2026.03.10", "Call Agent 全球版",      True),
]
def _mile(x, date, name, hot, i):
    # 高亮色走内联 style（fill 属性会被 .fig .lbl/.ttl 的 CSS fill 覆盖，形同没写）
    cx, am = x + 150, (' style="fill:var(--accent)"' if hot else "")
    box = ('<rect x="%d" y="56" width="300" height="100" rx="3" fill="none" stroke="var(--accent)" stroke-width="2"/>' % x
           if hot else '<rect x="%d" y="56" width="300" height="100" rx="3" class="box" stroke-width="1"/>' % x)
    return ('<g class="pop" style="--i:%d">'
            '<circle cx="%d" cy="30" r="5" class="%s"/>%s'
            '<text class="lbl" x="%d" y="92" text-anchor="middle"%s>%s</text>'
            '<text class="ttl" x="%d" y="130" text-anchor="middle" style="font-size:20px%s">%s</text></g>'
            % (i, cx, "fill-am" if hot else "fill-ink", box,
               cx, am, date, cx, ";fill:var(--accent)" if hot else "", name))
_p2mile = ('<path class="dw" style="--len:1580;--i:0" d="M10 30 H1590" stroke="var(--hair)" stroke-width="1" fill="none"/>'
           + "".join(_mile(*m, i=k + 1) for k, m in enumerate(_MILE)))

page("content", "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "公司 · 声网 RTE · ONE-PAGE BRIEF"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:80px;font-size:56px",
       "RTE 行业领导者，<strong>一页讲完</strong>。"),
    # 区 01 · SCALE
    lab(120, 236, "01 · SCALE"),
    sh("", "left:120px;top:272px;width:1680px;height:140px",
       '<div class="g4">' + "".join(
           '<div class="stat flow" style="--i:%d">'
           '<span class="v%s" style="font-size:64px">%s</span>'
           '<span class="l" style="font-size:14px">%s</span></div>'
           % (2 + _i, "" if _on else " w", _v, _l)
           for _i, (_v, _l, _on) in enumerate(_RTE)) + '</div>'),
    rule(420),
    # 区 02 · ADOPTION（左半）
    lab(120, 452, "02 · ADOPTION"),
    sh("settle", "left:120px;top:488px;width:780px;height:150px",
       '<div class="stat"><div class="v" style="font-size:96px;font-family:var(--f-cn)">近一半</div>'
       '<div class="l">集成 RTC 的 Top 10,000（MAU）App 里，近一半使用声网</div></div>'),
    sh("spread", "left:120px;top:660px;width:406px;height:40px;background:var(--accent);border-radius:6px;"
       "font:700 17px/40px var(--f-cn);color:var(--slide-bg);text-align:center;--i:3", "使用声网"),
    sh("spread", "left:526px;top:660px;width:374px;height:40px;background:var(--card-bg);border:1px solid var(--hair);"
       "border-radius:6px;font:500 17px/38px var(--f-cn);color:var(--ink-2);text-align:center;--i:4", "其他 RTC"),
    # 区 03 · ENDORSEMENT（右半）
    lab(980, 452, "03 · ENDORSEMENT"),
    sh("settle", "left:980px;top:488px;width:820px;height:44px;font:700 28px/1 var(--f-mono);letter-spacing:.1em;color:var(--accent);--i:2",
       "2024.10.01"),
    sh("flow", "left:980px;top:548px;width:820px;height:90px;font:700 30px/1.4 var(--f-cn);color:var(--ink);--i:3",
       "OpenAI Realtime API · Agora <strong style='color:var(--accent)'>全球首批合作伙伴</strong>"),
    sh("flow", "left:980px;top:654px;width:820px;height:50px;font:500 20px/1.5 var(--f-cn);color:var(--accent);--i:4",
       "同样的工程能力，今天用来支撑你的对话式 AI 业务。"),
    rule(744),
    # 区 04 · MILESTONES（五节点卡片时间轴 mini · 末框 accent 描边）
    lab(120, 766, "04 · MILESTONES · 18 个月 · 5 个公开里程碑"),
    figbox(120, 800, 1680, 1620, 170, _p2mile, i=2),
    sh("flow", "left:120px;top:988px;width:1680px;height:70px;--i:5",
       '<div class="land">全球最受欢迎的实时音视频云服务提供商。</div>'),
]))

# ═══ P3 · 矩阵 ·「一个平台，三台引擎」（accent）════════════════════════════
#   01 ARCHITECTURE 分层图 / 02 THREE ENGINES 三行三色 / 03 DUAL FORM 双形态
_MX = [
    ("对话式 AI 引擎",  "闭源 · 已上线",        True),
    ("TEN 开源工具库",  "开源",                False),
    ("企业级智能体",  "Call Agent · Global 率先发布", False),
    ("AI 模型评测平台", "已上线",              False),
    ("实时转录翻译",    "已上线",              False),
    ("开发套件",        "Physical AI · 已上线", False),
]
def _mxbox(i, name, form, hot):
    # 原图 viewBox 1620×430；按 spec 把底座条与框间距收 30px、整体压到 1620×320
    x = 10 + i * 270
    cx = x + 125
    am = "fill:var(--accent);" if hot else ""      # 内联 style，见文件头注释
    box = ('<rect x="%d" y="10" width="250" height="130" rx="3" fill="none" stroke="var(--accent)" stroke-width="2"/>' % x
           if hot else '<rect x="%d" y="10" width="250" height="130" rx="3" class="box" stroke-width="1"/>' % x)
    return ('<g class="pop" style="--i:%d">%s'
            '<text class="ttl" x="%d" y="66" text-anchor="middle" style="%sfont-size:22px">%s</text>'
            '<text class="sm" x="%d" y="100" text-anchor="middle">%s</text></g>'
            % (i, box, cx, am, name, cx, form))
_p3fig = ("".join(_mxbox(i, n, f, h) for i, (n, f, h) in enumerate(_MX))
          + "".join('<path class="dw" style="--len:40;--i:%d" d="M%d 140 V180" '
                    'stroke="var(--hair-strong)" stroke-width="1.5" fill="none"/>' % (6 + i, 135 + i * 270)
                    for i in range(6))
          + '<g class="pop" style="--i:7">'
            '<rect x="10" y="180" width="1600" height="110" rx="3" class="box" stroke-width="1"/>'
            '<text class="lbl" x="42" y="223">实时互动平台 · REAL-TIME ENGAGEMENT</text>'
            '<text class="txt" x="42" y="261">SD-RTN 全球实时网络——当下基本盘，托举全部对话式 AI 产品线</text>'
            '</g>')
_ENG3 = [
    ("l-eng",   "ENGINE",      "提供能力——把「会说话」做到极致"),
    ("l-agent", "AGENT",       "交付结果——替你把任务做完"),
    ("l-phys",  "PHYSICAL AI", "打开入口——让对话走出屏幕"),
]
page("content", "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "矩阵 · 对话式 AI 产品线 · PRODUCT MATRIX"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", "一个平台，<strong>三台引擎</strong>。"),
    # 区 01 · ARCHITECTURE（分区标 y=236 = 全 deck 首分区标统一栏位）
    lab(120, 236, "01 · ARCHITECTURE"),
    figbox(120, 276, 1680, 1620, 320, _p3fig, i=1),
    rule(628),
    # 区 02 · THREE ENGINES（左 2/3）
    lab(120, 636, "02 · THREE ENGINES"),
    sh("", "left:120px;top:668px;width:1080px;height:170px",
       '<div class="rows">' + "".join(
           '<div class="r flow" style="--i:%d;padding:12px 0">'
           '<span class="n" style="width:40px">%s</span>'
           '<span class="k" style="width:210px;color:var(--%s);font-family:var(--f-mono);font-size:24px">%s</span>'
           '<span class="v" style="font-size:21px">%s</span></div>'
           % (2 + _i, dot(_c), _c, _n, _d)
           for _i, (_c, _n, _d) in enumerate(_ENG3)) + '</div>'),
    # 区 03 · DUAL FORM（右 1/3）
    lab(1240, 636, "03 · DUAL FORM"),
    sh("rise card-c", "left:1240px;top:668px;width:560px;height:104px;--i:3",
       '<div style="padding:20px 26px">'
       '<div class="mono-sm" style="color:var(--accent)">闭源 · 已上线</div>'
       '<div style="margin-top:12px;font:700 30px/1.2 var(--f-cn);color:var(--ink)">对话式 AI 引擎</div></div>'),
    sh("rise card-c", "left:1240px;top:792px;width:560px;height:104px;--i:4",
       '<div style="padding:20px 26px">'
       '<div class="mono-sm">开源</div>'
       '<div style="margin-top:12px;font:700 30px/1.2 var(--f-cn);color:var(--ink)">TEN 开源工具库</div></div>'),
    # 底行：land（左）与 note（右）文字基线对齐 —— .note 文心 = y+23.6，.land 文心 = y+31.75，
    # 所以 note 顶比 land 顶高 8px 才是真齐（原来 914/920 差 6，实际差 14px 没对上）
    sh("flow", "left:1240px;top:996px;width:560px;height:60px;--i:5",
       '<div class="note">与实时互动平台并列的<strong style="color:var(--accent)">两大产品引擎</strong>。</div>'),
    sh("flow", "left:120px;top:988px;width:1080px;height:70px;--i:6",
       '<div class="land">' + dot("l-eng") + "Engine 提供能力　" + dot("l-agent") + "Agent 交付结果　"
       + dot("l-phys") + "Physical AI 走进物理世界。</div>"),
]))

# ═══ P4 · Engine ·「对话式 AI 引擎 · 体验分」（l-eng 玫红）═════════════════
#   01 VELOCITY 17 版轴 / 02 VS LIVEKIT 四项 / 03 SIGNATURE MOVES 三绝活 / 04 OPEN chips
_CMP = [
    ("打断成功率",   "越高越好",             900, 464, "33%",   "17%"),
    ("词错率 WER",   "理想条件 · 越低越好",   605, 900, "9.25%", "13.77%"),
    ("误响应率",     "50dB 人声噪声 · 越低越好", 63, 900, "7%",  "100%"),
    ("多语种",       "开箱默认 · 中西法俄阿日", 900, 150, "6/6", "仅英文"),
]
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
    ("01", "优雅打断 2.0", "CAN + 语义 + 声学三路融合。从「能打断」到「打断得体」。", _FIG_CUT),
    ("02", "声纹识别",     "有感 / 无感双模式。多人同场分得清说话人。",              _FIG_VP),
    ("03", "短期记忆",     "会话内毫秒级上下文。转人工、转 Agent 不丢线索。",         _FIG_MEM),
]
_p4 = [
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "ENGINE · 一页讲透 · SHIPPING VELOCITY"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", "超低延迟、可打断、<strong>高自然度</strong>。"),
    # 区 01 · VELOCITY（17 版 mini 轴）· 分区标 y=236 统一栏位，整段内容随之上移 10
    lab(120, 236, "01 · VELOCITY"),
    sh("flow tl-line", "left:180px;top:296px;width:1280px;height:3px;--i:1", ""),
    sh("flow mono-sm", "left:180px;top:330px;width:460px;height:24px;--i:3", "2025.02.18 · v1.0 公测"),
    sh("flow mono-sm", "left:1000px;top:330px;width:460px;height:24px;text-align:right;--i:3",
       "2026.08.11 · v2.11 最新"),
    sh("settle", "left:1560px;top:248px;width:240px;height:76px;text-align:right;"
       "font:900 56px/1 var(--f-cn);letter-spacing:-.03em;color:var(--l-eng);--i:2", "17"),
    sh("flow mono-sm", "left:1440px;top:330px;width:360px;height:22px;text-align:right;--i:3",
       "PUBLIC RELEASES · 18 MONTHS"),
]
for _i in range(17):
    _x = 180 + round(_i * 1280 / 16)
    _big = _i in (0, 16)
    _p4.append(sh("pop vt" + (" big" if _big else ""),
                  "left:%dpx;top:%dpx;width:%dpx;height:%dpx;--i:%d"
                  % (_x, 282 if _big else 287, 5 if _big else 3, 32 if _big else 22, 1 + _i // 6), ""))
_p4.append(rule(384))
# 区 02 · VS LIVEKIT（左半 · 每项一行：名称 + 双条 + 两值）
_p4.append(lab(120, 404, "02 · VS LIVEKIT · 2026-03 同题评测 · 默认配置口径"))
for _i, (_n, _dir, _wo, _wt, _vo, _vt) in enumerate(_CMP):
    _y = 444 + _i * 96
    _so, _st = max(round(_wo * 460 / 900), 6), max(round(_wt * 460 / 900), 6)
    _p4 += [
        sh("flow", "left:120px;top:%dpx;width:200px;height:46px;--i:%d" % (_y, 2 + _i),
           '<div style="font:700 20px/1.25 var(--f-cn);color:var(--ink)">%s</div>'
           '<div style="margin-top:6px;font:500 13px/1 var(--f-mono);letter-spacing:.1em;color:var(--ink-3)">%s</div>'
           % (_n, _dir)),
        sh("spread", "left:328px;top:%dpx;width:%dpx;height:14px;background:var(--l-eng);border-radius:4px;--i:%d"
           % (_y + 2, _so, 2 + _i), ""),
        sh("flow", "left:800px;top:%dpx;width:150px;height:24px;--i:%d" % (_y - 4, 2 + _i),
           '<span style="font:700 18px/24px var(--f-mono);color:var(--ink)">%s</span>'
           '<span style="font:400 13px/24px var(--f-cn);color:var(--ink-3);margin-left:8px">声网</span>' % _vo),
        sh("spread", "left:328px;top:%dpx;width:%dpx;height:14px;background:var(--ink-3);opacity:.42;border-radius:4px;--i:%d"
           % (_y + 30, _st, 2 + _i), ""),
        sh("flow", "left:800px;top:%dpx;width:150px;height:24px;--i:%d" % (_y + 24, 2 + _i),
           '<span style="font:700 18px/24px var(--f-mono);color:var(--ink-2)">%s</span>'
           '<span style="font:400 13px/24px var(--f-cn);color:var(--ink-3);margin-left:8px">LiveKit</span>' % _vt),
    ]
# 区 03 · SIGNATURE MOVES（右半 · 三张 mini 卡）
_p4.append(lab(980, 404, "03 · SIGNATURE MOVES"))
_p4 += [sh("rise card-c", "left:980px;top:%dpx;width:820px;height:128px;--i:%d" % (440 + _i * 134, 3 + _i),
           '<div style="padding:0 30px;height:100%%;display:flex;align-items:center;gap:26px">'
           '<div class="fig" style="width:200px;flex:none">'
           '<svg viewBox="0 0 420 120" style="width:100%%;height:auto">%s</svg></div>'
           '<div style="flex:1">'
           '<div style="font:700 24px/1.2 var(--f-cn);color:var(--ink)">'
           '<span style="font:700 15px/1 var(--f-mono);color:var(--l-eng);margin-right:12px">%s</span>%s</div>'
           '<div style="margin-top:10px;font:400 15px/1.5 var(--f-cn);color:var(--ink-2)">%s</div>'
           '</div></div>' % (_f, _no, _n, _d))
        for _i, (_no, _n, _d, _f) in enumerate(_MOVES)]
# 区 04 · OPEN（chips 一行）· 底分隔线统一 850（与 P5/P8 同栏位，压住背景板 y848–852 的 accent 细线）
_p4.append(rule(850))
_p4.append(lab(120, 874, "04 · OPEN"))
_p4.append(sh("rise", "left:120px;top:902px;width:1680px;height:54px;--i:4",
              "".join('<span class="chip">%s</span>' % t for t in
                      ["ASR / LLM / TTS 可替换 · 可兜底 · 可热切换", "MCP + Function Call",
                       "数字人", "TEN 开源生态"])
              # 第 5 个 chip = 「引擎产品详解」抽屉的触发件（Enter 或点击 → 视口级 overlay）
              + '<span class="chip chip-expand" id="engineExpand" role="button" tabindex="0">'
                '⤢ 引擎产品详解 · 13 页 · ⏎</span>'))
_p4.append(sh("flow", "left:120px;top:988px;width:1680px;height:70px;--i:6",
              '<div class="land">模型会换代，接口不换人。</div>'))
page("content", "".join(_p4))

# ═══ P5 · Agent ·「企业级智能体 · 生产数据」（l-agent 蓝）══════════════════
#   01 TURING 96.5% + funnel / 02 CONVERSION 2.05× / 03 FIVE 五维 / 04 CAPABILITIES 12 项
_FUN = [
    ( 20, 700, "接听",      "2,475 · 100.0%", 272, None),
    ( 92, 617, "真人接听",   "2,180 · 88.1%",  272, None),
    (164, 331, "有效对话",   "1,170 · 47.3%",  272, "var(--l-agent)"),
    (236,  26, "感知为 AI",  "86 · 3.5%",      296, "var(--coral)"),
]
def _fun(i, y, w, lb, val, vx, col):
    bar = ('<rect x="250" y="%d" width="%d" height="52" rx="2" fill="none" stroke="%s" stroke-width="2"/>' % (y, w, col)
           if col else '<rect x="250" y="%d" width="%d" height="52" rx="2" class="box" stroke-width="1"/>' % (y, w))
    return ('<g class="pop" style="--i:%d">%s'
            '<text class="lbl" x="230" y="%d" text-anchor="end">%s</text>'
            '<text class="sm" x="%d" y="%d"%s>%s</text></g>'
            % (i, bar, y + 32, lb, vx, y + 33,
               (' style="fill:%s"' % col) if col else "", val))   # 内联 style，见文件头注释
_p5fun = "".join(_fun(i, *f) for i, f in enumerate(_FUN))
# 横向双条 mini：P16 原图 viewBox 1620×300 塞进 840 宽会把 15px 字压到 7.8px，
# 所以按 1:1 重排成 viewBox 840×200（几何比例与数据一模一样：1.5% : 3.08% = 196 : 402）
_p5conv = ('<g class="pop" style="--i:0">'
           '<rect x="150" y="26" width="196" height="46" rx="2" class="box" stroke-width="1"/>'
           '<text class="lbl" x="134" y="56" text-anchor="end">行业最佳人工</text>'
           '<text class="txt" x="362" y="57">1.5% —— 行业天花板</text></g>'
           '<g class="pop" style="--i:1">'
           '<rect x="150" y="104" width="402" height="46" rx="2" fill="none" stroke="var(--l-agent)" stroke-width="2"/>'
           # Agent 章图形主色 = l-agent；一律内联 style（fill 属性压不过 .fig .lbl/.txt/.big 的 CSS fill）
           '<text class="lbl" x="134" y="134" text-anchor="end" style="fill:var(--l-agent)">ConvoAI</text>'
           '<text class="txt" x="568" y="135" style="fill:var(--l-agent)">3.08% —— 真实生产数据</text></g>'
           '<text class="big pop" style="--i:3;fill:var(--l-agent)" x="700" y="100" text-anchor="middle">2.05×</text>'
           '<text class="lbl pop" style="--i:4" x="150" y="188">AI ÷ 人 = 2.05 倍 · 日均营销转化率</text>')
_FIVE = [
    ("01", "运行时", "全球 SD-RTN 200+ 节点",     False),
    ("02", "记忆",   "毫秒级分层记忆 RAG 端到端",  False),
    ("03", "安全",   "99.99% · SOC 2 / GDPR",     True),
    ("04", "工具",   "MCP + Function Call 开放栈", False),
    ("05", "弹性",   "900 亿分钟 RTE 月均支撑",   False),
]
_G12 = ["SIP / PSTN 全打通", "Warm Transfer", "WhatsApp 接入", "LATAM SIP", "海外多供应商",
        "静态填充词", "Campaign A/B", "时区 · 号码前缀", "音色复刻", "优雅打断 2.0",
        "声纹识别", "实时情绪识别"]
page("content", "".join([
    sh("flow kk ag", "left:120px;top:92px;width:1680px;height:28px", "AGENT · 企业级智能体 · REAL PRODUCTION DATA"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:90px",
       '已经超越<strong class="ag">真人</strong>的企业级智能体。'),
    # 区 01 · TURING（左半）
    lab(120, 236, "01 · TURING"),
    sh("settle", "left:120px;top:268px;width:760px;height:130px",
       '<div class="stat"><div class="v" style="font-size:88px;color:var(--l-agent)">96.5%</div>'
       '<div class="l">用户以为在跟真人说话</div></div>'),
    figbox(120, 400, 800, 1000, 300, _p5fun, i=2),
    sh("flow", "left:120px;top:660px;width:800px;height:44px;font:400 20px/1.4 var(--f-cn);color:var(--ink-2);--i:4",
       "仅 3.5%（86 通）被用户明显感知为 AI。"),
    # 区 02 · CONVERSION（右半上）· 右列起点统一到 x980（P2/P4/P6/P8 同栏位），宽 820 → 右缘仍是 1800
    lab(980, 236, "02 · CONVERSION"),
    figbox(980, 268, 820, 840, 200, _p5conv, i=2),
    # 区 03 · FIVE（右半下）
    lab(980, 496, "03 · FIVE · 企业级智能体必须做的 5 件事"),
    sh("", "left:980px;top:528px;width:820px;height:300px",
       '<div class="rows">' + "".join(
           '<div class="r flow%s" style="--i:%d;padding:15px 0">'
           '<span class="n" style="color:var(--%s);font-size:22px">%s</span>'
           '<span class="k" style="width:130px;font-size:22px;color:var(--%s)">%s</span>'
           '<span class="v" style="font-size:19px">%s</span></div>'
           % (" hot" if _hot else "", 2 + _i, "coral" if _hot else "l-agent", _no,
              "coral" if _hot else "l-agent", _n, _v)
           for _i, (_no, _n, _v, _hot) in enumerate(_FIVE)) + '</div>'),
    rule(850),
    # 区 04 · CAPABILITIES（12 项 6×2）
    lab(120, 866, "04 · CAPABILITIES · 企业级智能体 12 项能力"),
    sh("rise", "left:120px;top:890px;width:1680px;height:94px;--i:3",
       '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:14px">'
       + "".join('<div class="cap%s">%s</div>' % (" on" if _i == 9 else "", _t)
                 for _i, _t in enumerate(_G12)) + '</div>'),
    sh("flow", "left:120px;top:988px;width:1680px;height:70px;--i:5",
       '<div class="land">不再是「AI 能否替代人工」——是「人工能否追上 AI」。</div>'),
]))

# ═══ P6 · PhysicalAI ·「让对话走出屏幕」（l-phys 紫）══════════════════════
#   01 R1 KIT 双形态 / 02 LIFELIKE 活人感三态 / 03 ROBOTICS 1 三数字
_R1KIT = [
    ("R1 · WI-FI · 2025.03.20 发布", "R1-WiFi",
     "面向家居与室内场景——音箱、桌宠、陪伴机器人。",
     "· 连接　Wi-Fi　　· 场景　家居 / 室内　　· 形态　音箱 · 桌宠 · 陪伴机器人"),
    ("R1 · 4G · 2025.09.26 发布", "R1-4G",
     "走出 Wi-Fi 覆盖——户外、随身、车载与出海设备。",
     "· 连接　4G 全移动　　· 场景　户外 / 随身 / 车载　　· 形态　出海设备 · 随身伴侣"),
]
_FACES = [
    ("",     "TOO DRY",    "太木", "正确，但没有关系温度。用户不想再开口。"),
    (" good", "JUST RIGHT", "恰好", "自然、可持续相处。下次还想跟它说话。"),
    ("",     "TOO CLINGY", "太腻", "伪装成朋友的销售感。三句之后想拔电源。"),
]
_ROB = [
    ("200+",   "",                        "全球节点 · SD-RTN 软件定义实时网"),
    ("毫秒级",  "font-family:var(--f-cn);", "端到端往返 · 弱网最后一公里对抗"),
    ("30000+", "",                        "芯片与整机适配 · 你的形态大概率已支持"),
]
page("content", "".join([
    sh("flow kk ph", "left:120px;top:92px;width:1680px;height:28px", "PHYSICAL AI · 对话式 AI 开发套件 · GLOBAL FIRST"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:90px",
       '让对话，<strong class="ph">走出屏幕</strong>。'),
    # 区 01 · R1 KIT（左半）
    lab(120, 236, "01 · R1 KIT"),
    ] + [
    sh("rise card-c", "left:120px;top:%dpx;width:800px;height:176px;--i:%d" % (266 + _i * 192, 2 + _i),
       '<div style="padding:22px 30px">'
       '<div class="mono-sm" style="color:var(--l-phys)">%s</div>'
       '<h3 style="margin:12px 0 8px;font:700 34px/1.2 var(--f-cn);color:var(--ink)">%s</h3>'
       '<div style="font:400 18px/1.5 var(--f-cn);color:var(--ink-2)">%s</div>'
       '<div style="margin-top:12px;font:500 13px/1 var(--f-mono);letter-spacing:.06em;color:var(--ink-3)">%s</div>'
       '</div>' % (_tag, _nm, _p, _spec))
    for _i, (_tag, _nm, _p, _spec) in enumerate(_R1KIT)
    ] + [
    sh("flow", "left:120px;top:652px;width:800px;height:44px;font:500 22px/1.4 var(--f-cn);color:var(--l-phys);--i:4",
       "全球率先发布的对话式 AI 硬件开发套件。"),
    # 区 02 · LIFELIKE（右半）
    lab(980, 236, "02 · LIFELIKE · 「活人感」三态"),
    ] + [
    sh("rise card-c face%s" % _cls, "left:%dpx;top:266px;width:260px;height:236px;--i:%d" % (980 + _i * 280, 2 + _i),
       '<div class="en">%s</div><h3>%s</h3><p>%s</p>' % (_en, _cn, _d))
    for _i, (_cls, _en, _cn, _d) in enumerate(_FACES)
    ] + [
    sh("flow", "left:980px;top:520px;width:820px;height:60px;--i:5",
       '<div class="note">活人感 = <strong style="color:var(--l-phys)">角色立得住 + 临场撑得住</strong>。</div>'),
    rule(706),
    # 区 03 · ROBOTICS 1（全宽三数字；.v 落在 y776–842，正好躲开背景板 y848 的 accent 细线）
    lab(120, 728, "03 · ROBOTICS 1 · 机器人的临场引擎"),
    sh("", "left:120px;top:776px;width:1680px;height:140px",
       '<div class="g3">' + "".join(
           '<div class="stat flow" style="--i:%d">'
           '<div class="v" style="font-size:72px;%scolor:var(--l-phys)">%s</div>'
           '<div class="l">%s</div></div>' % (2 + _i, _ff, _v, _l)
           for _i, (_v, _ff, _l) in enumerate(_ROB)) + '</div>'),
    sh("flow", "left:120px;top:988px;width:1680px;height:70px;--i:5",
       '<div class="land">你做产品与角色，我们做<strong style="color:var(--l-phys)">临场与连接</strong>。</div>'),
]))

# ═══ P7 · 案例 ·「已经上岗的对话式 AI」（accent）═══════════════════════════
#   左 01 ECOSYSTEM 五层实时智能生态（双源全景底图 + DOM 五层叠标）
#   右 02 CASES 案例墙 v2（3 张精选大卡 + 11 张证据小卡 = 14 例）
# ── 视觉升级 R1（GPT 5.6 · 合入 2026-08-13）─────────────────────────────────
#   2026-08-12 把 eco-2026.webp 换成原生 SVG，是因为那张 4K 全景压进 980px 后小字全糊、
#   而且白底在暗主题里是块外来物。R1 把位图请回来，但三条病根都治了：
#     ① 浅/深同构双源，走 .hero-art 的同一套 CSS 主题切换；
#     ② 图只做远景底纹，L4–L0 的字全部是 DOM（.eco-layer），字号可控；
#     ③ 半透明卡背 + backdrop-blur 保证两主题下标签都压得住底图。
#   完整 4K 全景仍在 /convoai 第 23 页，脚注指路（裁定 #3 合并两版为一行）。
_ECO = [
    ("l4", "L4", "入口与设备",   "通用助手 · 工作入口 · 可穿戴 · 机器人"),
    ("l3", "L3", "应用与结果",   "CX · 销售 · 医疗 · 教育 · 陪伴 · 翻译"),
    ("l2", "L2", "Agent 运行时", "声网对话式 AI 引擎 · TEN"),
    ("l1", "L1", "模型与感知",   "声网 Agora · 感知与 VAD"),
    ("l0", "L0", "实时基础设施", "声网 Agora · SD-RTN"),
]
_p7eco = ('<img class="eco-art lt" src="%(A)sinfo-v2/ecosystem-stack-v4-light.webp" alt="">'
          '<img class="eco-art dk" src="%(A)sinfo-v2/ecosystem-stack-v4-dark.webp" alt="">'
          '<div class="eco-kicker">REAL-TIME INTELLIGENCE ECOSYSTEM</div>' % {"A": A}
          + "".join('<div class="eco-layer %s"><span class="eco-code">%s</span>'
                    '<b>%s</b><small>%s</small></div>' % _l for _l in _ECO))

# ── 裁定 #2 · 客户名逐字对照公开卡片上烧录的品牌（客户当面的 deck 一字不能错）──
#   升级版写错四处，此处修正：极限→集贤科技 / LUWUU→luwu / SenseTime→商汤 /
#   智谱→智谱清言 / Heycyan→HeyCyan / 联欧→莲偶科技。案例事实与数量（14）不变。
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
_p7wall = (
    '<div class="case-wall-v2">'
    '<div class="case-wall-head"><span>02 · CASES · OFFICIAL PUBLIC CASES</span>'
    '<b>14</b><small>声网联合案例 · 均已公开</small></div>'
    '<div class="case-feature-row">'
    + "".join('<div class="case-feature"><img src="%sinfo-v2/case-feature-%s.webp" alt="声网联合案例 · %s">'
              '<div class="case-feature-caption"><b>%s</b><span>%s</span></div></div>'
              % (A, _f, _n, _n, _k) for _f, _n, _k in _FEATURE)
    + '</div><div class="case-index">+ 11 个公开联合案例</div><div class="case-mini-grid">'
    + "".join('<div class="case-mini"><img src="%sinfo-v2/case-mini-%s.webp" alt="声网联合案例 · %s">'
              '<span>%s</span></div>' % (A, _f, _n, _n) for _f, _n in _MINI)
    + '</div></div>')

_p7 = [
    sh("flow kk nt", "left:120px;top:92px;width:1680px;height:28px", "案例 · 已经上岗的对话式 AI · IN PRODUCTION"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", "对话式 AI，<strong>已经上岗</strong>。"),
    # 区 01 · ECOSYSTEM（左列 · 全景底图 + 五层 DOM 叠标；顶 292 / 底 844 与我版逐像素同）
    lab(120, 236, "01 · ECOSYSTEM · 五层价值地壳，我们在哪", w=980),
    sh("flow eco-visual", "left:120px;top:292px;width:980px;height:552px;--i:1", _p7eco),
    sh("pop callout-chip", "left:120px;top:872px;width:auto;height:auto;--i:4",
       "L0 连接 · L1 感知 · L2 运行时——<b>三层都有声网</b>"),
    # 裁定 #3：合并我版「完整 4K 全景见 /convoai P23」与升级版「每一层都由声网托住」为一行
    sh("flow mono-sm", "left:120px;top:953px;width:980px;height:24px;--i:5",
       "从 SD‑RTN 到设备，每一层都由声网托住 · 完整 4K 全景见 /convoai P23 · 事实截止 2026.08"),
    # 区 02 · CASES（右列 · 案例墙 v2；顶 236 与左列 seclab 齐，底 977 与左列脚注底齐）
    sh("flow", "left:1156px;top:236px;width:644px;height:741px;--i:2", _p7wall),
    sh("flow", "left:120px;top:988px;width:1680px;height:70px;--i:6",
       '<div class="land">声网官方联合案例 · 均已公开——你的场景，多半能对上号。</div>'),
]
page("content", "".join(_p7))

# ═══ P8 · 合流 ·「为什么是声网 · 怎么开始」（accent）═══════════════════════
#   01 ONE NET 一张网 / 02 NEUTRALITY 中立三条 / 03 START 三步 / 底 land + credit
_NEU = [
    ("01", "不做 C 端 App",   "不和你的产品竞争用户——你的用户永远是你的。"),
    ("02", "不做自有硬件品牌", "R1 是开发套件，不是消费品——我们停在你需要的那一层。"),
    ("03", "不训基座大模型",   "多供应商开放，谁好用接谁——模型进步全部归你享受。"),
]
_STEP = [
    ("STEP 1 · 今天",     "注册即用",   "免费额度，当天就能听到第一句回话"),
    ("STEP 2 · 两周",     "PoC 共建",   "工程团队陪跑，把你的第一个真实场景跑通"),
    ("STEP 3 · 一个季度", "规模化上线", "SLA、全球部署、多供应商兜底"),
]
_ARROW = ('<div class="fig"><svg viewBox="0 0 20 36" style="width:100%;height:auto">'
          '<path class="dw" style="--len:22" d="M10 2 V24" stroke="var(--hair-strong)" stroke-width="1.5" fill="none"/>'
          '<polygon class="fill-ink" points="4,24 16,24 10,34"/></svg></div>')
page("content", "".join([
    sh("flow kk", "left:120px;top:92px;width:1680px;height:28px", "合流 · 为什么是声网 · 怎么开始 · ONE NET"),
    sh("ink hh", "left:120px;top:148px;width:1680px;height:90px", "三条支流，<strong>一条河</strong>。"),
    # 区 01 · ONE NET（分区标 y=236 统一栏位）
    lab(120, 236, "01 · ONE NET"),
    sh("rise", "left:120px;top:274px;width:1680px;height:44px;font:700 26px/1.5 var(--f-cn);color:var(--ink-2);--i:2",
       dot("l-eng") + "Engine 的每一次打断　" + dot("l-agent") + "Agent 的每一次交付　"
       + dot("l-phys") + "Physical AI 的每一次唤醒"),
    sh("flow", "left:120px;top:330px;width:1680px;height:50px;font:400 24px/1.6 var(--f-cn);color:var(--ink);--i:3",
       "都跑在同一张 <strong style='color:var(--accent)'>SD-RTN 软件定义实时网络</strong>上——全球 200+ 节点，端到端毫秒级。"),
    rule(404),
    # 区 02 · NEUTRALITY（左半）
    lab(120, 426, "02 · NEUTRALITY"),
    sh("", "left:120px;top:460px;width:840px;height:186px",
       '<div class="rows">' + "".join(
           '<div class="r flow" style="--i:%d;padding:16px 0"><span class="n">%s</span>'
           '<span class="k" style="width:230px;font-size:24px">%s</span>'
           '<span class="v" style="font-size:18px">%s</span></div>' % (2 + _i, _no, _n, _d)
           for _i, (_no, _n, _d) in enumerate(_NEU)) + '</div>'),
    sh("flow", "left:120px;top:676px;width:840px;height:50px;font:500 24px/1.5 var(--f-cn);color:var(--accent);--i:5",
       "OpenAI 选择我们，也是这个原因。"),
    # 区 03 · START（右半 · 三步竖排，箭头连接）
    lab(980, 426, "03 · START"),
    ] + [
    sh("rise card-c", "left:980px;top:%dpx;width:820px;height:76px;--i:%d" % (460 + _i * 120, 2 + _i),
       '<div style="padding:0 30px;height:100%%;display:flex;align-items:center;gap:24px">'
       '<div style="font:500 15px/1 var(--f-mono);letter-spacing:.12em;color:var(--accent);width:180px;flex:none">%s</div>'
       '<div style="font:700 30px/1.2 var(--f-cn);color:var(--ink);width:172px;flex:none">%s</div>'
       '<div style="font:400 17px/1.4 var(--f-cn);color:var(--ink-2);flex:1">%s</div></div>' % (_t, _n, _d))
    for _i, (_t, _n, _d) in enumerate(_STEP)
    ] + [
    sh("flow", "left:1380px;top:542px;width:20px;height:36px;--i:3", _ARROW),
    sh("flow", "left:1380px;top:662px;width:20px;height:36px;--i:4", _ARROW),
    rule(850),
    # 底 · land + credit 同一行：land 左（y988 = 全 deck land 统一基线），credit 右对齐、
    # 顶 1010 让 mono 文心（1010+10.5）压住 land 文心（988+31.75），两边真齐平。
    # 原来 land 在 880、credit 在 1004 各占一行 —— land 比其他 7 页高 108px，翻页时那根
    # accent 竖条会跳，正是 Colin 说的「看起来没对齐」。
    sh("flow", "left:120px;top:988px;width:1060px;height:70px;--i:6",
       '<div class="land">让陪伴自然，让生意<strong>成单</strong>。</div>'),
    sh("flow mono-sm", "left:1200px;top:1010px;width:600px;height:24px;text-align:right;--i:7",
       "姚光华 COLIN · SHENGWANG.CN · COLINYAO.COM"),
]))

# ═══ 引擎详解抽屉的行为层（独立 <script>，不碰共享的 deck.js）═════════════════
#   触发：P4 上按 Enter，或点击 / Enter 聚焦态的 #engineExpand chip
#   收回：Esc（父窗口或 iframe 内都认）、点 scrim、点 ESC 按钮
#   键盘纪律：window 的 capture 阶段拦一层 —— 抽屉开着时除 Esc 外全部吞掉，
#             免得按键漏进 deck.js 把底下的 deck 翻页（点过 ESC 按钮、焦点
#             回到父窗口之后，这层是唯一的兜底）。
#   iframe 懒加载，关闭不清 src：二次展开接着上次的位置，Q&A 现场友好。
ENGINE_DRAWER_JS = """<script>(function(){
var ov=document.getElementById("engineOverlay"),
    fr=document.getElementById("engineFrame"),
    chip=document.getElementById("engineExpand");
if(!ov||!fr||!chip)return;
var scrim=ov.querySelector(".eo-scrim"),btn=ov.querySelector(".eo-close"),loaded=false;
function isOpen(){return !ov.hidden;}
function bindInner(){
  var w=null;try{w=fr.contentWindow;}catch(e){}
  if(!w||w.__engineEscBound)return;   /* 标志位挂在内层 window 上：每次 load 换新 window 自动失效 */
  w.__engineEscBound=true;
  w.addEventListener("keydown",function(e){
    if(e.key==="Escape"){e.preventDefault();closeDrawer();}
  });
}
function focusInner(){try{fr.contentWindow.focus();}catch(e){}bindInner();}
fr.addEventListener("load",function(){loaded=true;if(isOpen())focusInner();});
function openDrawer(){
  if(!fr.getAttribute("src")&&fr.dataset.src)fr.setAttribute("src",fr.dataset.src);   /* 懒加载：首次展开才拉 13 页；归档态用 srcdoc、无 data-src，此守卫防误导航 */
  ov.hidden=false;
  if(loaded)focusInner();
}
function closeDrawer(){ov.hidden=true;window.focus();}
chip.addEventListener("click",openDrawer);
chip.addEventListener("keydown",function(e){
  if(e.key==="Enter"||e.key===" "){e.preventDefault();openDrawer();}
});
scrim.addEventListener("click",closeDrawer);
btn.addEventListener("click",closeDrawer);
window.addEventListener("keydown",function(e){
  if(isOpen()){
    if(e.key==="Escape"){e.preventDefault();e.stopImmediatePropagation();closeDrawer();return;}
    e.stopImmediatePropagation();return;   /* 抽屉开着：其余按键一律不许漏进 deck.js */
  }
  if(e.key!=="Enter")return;
  var t=e.target;
  if(t&&t.getAttribute&&t.getAttribute("contenteditable"))return;   /* 就地编辑态不抢 Enter */
  if(t&&t.id==="deckSwap")return;                                   /* 主题按钮的 Enter 归它自己 */
  var cur=document.querySelector(".slide.active");
  if(!cur||cur.dataset.p!=="4")return;                              /* 只在 P4 认 Enter */
  e.preventDefault();e.stopImmediatePropagation();openDrawer();
},true);
})();</script>
"""

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
            # name = 资产 basename（不含 -light/-dark 与扩展名），相对 /decks/assets/convoai/
            hero_html = ('<img class="hero-art lt" src="%s%s-light.png" alt=""%s>'
                         '<img class="hero-art dk" src="%s%s-dark.png" alt=""%s>'
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
        '<title>声网对话式 AI · 一页一章 Infograph · 姚光华 Colin</title>\n'
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
        # 引擎详解抽屉：必须与 .deck-viewport 平级 —— 塞进 .deck-stage 就会吃到舞台的
        # translate+scale，iframe 内的原生滚动/点击坐标系全歪。
        '<div id="engineOverlay" hidden>\n'
        '  <div class="eo-scrim"></div>\n'
        '  <div class="eo-sheet">\n'
        '    <iframe id="engineFrame" data-src="/decks/convoai-engine.html" '
        'title="声网 · 对话式 AI 引擎 · 产品介绍"></iframe>\n'
        '    <button class="eo-close" type="button">ESC · 收回</button>\n'
        '  </div>\n</div>\n'
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
        'else{document.documentElement.removeAttribute("data-theme");b.textContent="暗底";}'
        'document.querySelectorAll(".strip img.lt").forEach(function(el){el.style.display=(t==="dark")?"none":"block";});'
        'document.querySelectorAll(".strip img.dk").forEach(function(el){el.style.display=(t==="dark")?"block":"none";});}'
        'var cur="light";try{cur=localStorage.getItem("colin-theme")||"light";}catch(e){}apply(cur);'
        'b.addEventListener("click",function(){cur=(cur==="dark")?"light":"dark";'
        'try{localStorage.setItem("colin-theme",cur);}catch(e){}apply(cur);});})();</script>\n'
        + ENGINE_DRAWER_JS +
        "</body></html>\n")
    OUT.write_text(doc, encoding="utf-8")
    assert total == 8, "页数漂移：%d != 8" % total
    print("convoai-info.html · %d 页 · %dKB · conf-light 默认 · 全页 data-steps=0" % (total, len(doc) // 1024))

if __name__ == "__main__":
    build()
