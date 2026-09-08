#!/usr/bin/env python3
"""cowork-confv2.html（46 页母稿）→ irte2026.html：iRTE 2026 实时智能大会 · 产品专场版。

   ── 家族定位 ──────────────────────────────────────────────────────────
   deck 家族第四支「irte」。视觉真源 = 大会模板 `iRTE2026_PPT模板_产品.pptx`
   （拆解规范：/home/claude/eco-review/irte-家族规范-v1.md）：
     · 底 #080C14（深海军蓝）· 主强调绿 #96FF9D · 次强调青 #7FF4FF
     · 标签薰衣草 #B29BFF · 结构件深紫 #5C22A5 · 第四色深青 #004660
     · 思源黑体（Source Han Sans CN，沙箱里 = Noto Sans CJK SC 同源）
     · 签名语法五件：`>` 提示符 / kicker 下深紫短条 81×4.5 / 像素方块 /
       绿是主角 / 星空 + 紫阶梯只出现在非正文页
   **原则：模板给色 / 字 / 标记 / 页型，CONF 家族给字号尺度与版式密度。**
   40 页正文母稿已逐页撑满，不能再改字号重排；所以只换颜色、字重、标记与页型，
   不动 h2 60px / eyebrow 17px mono / 正文 19–22px 这套 CONF 尺度。
   不上 LAB 3D：无 three / 无 canvas / 无 WebGL；运动原语只用母稿已有的
   .flow / .rise / .spread / .settle / .dw / .pop / .ink / .pkt，data-step 一个不动。

   ── 与母稿的差异只有五处 ─────────────────────────────────────────────
     ① P1 封面套模板「专场标题页」（模板 slide 3）
     ② P2 开场换成声网主场叙事（SVG 骨架 / 坐标 / 动效类原样，只换文案）
     ③ P15 / P22 / P31 / P32 四页案例整页留白（待 Colin 填新案例）
     ④ 删母稿 P44（单向门 / 双向门），后两页 chrome 页码 45→44、46→45
     ⑤ 原 P45「一页带走」四句换对象：开发者 / 客户 / 伙伴 / 自己
   其余 40 页逐字不动。

   重建：python3 scripts/build-irte2026.py
   自检：node scripts/qa-irte2026.mjs（BASE=http://127.0.0.1:8899）
"""
import base64, os, re, sys

SRC = "public/decks/cowork-confv2.html"
OUT = "public/decks/irte2026.html"
ASSETS = "scripts/assets/irte2026"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

src_bytes = open(SRC, "rb").read()
s = src_bytes.decode("utf-8")
SRC_MD5_LEN = len(src_bytes)

HITS = []


def rep(hay, old, new, n=1, tag=""):
    """替换 + 命中数断言。"""
    c = hay.count(old)
    assert c == n, f"[{tag}] 期望命中 {n} 次，实际 {c} 次：{old[:70]!r}"
    HITS.append((tag or old[:40], n))
    return hay.replace(old, new)


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode("ascii")


BG_STARS = b64(f"{ASSETS}/bg-stars.png")   # 1920×850 星空 + 紫像素阶梯（模板 L2 版式底）
LOGO = b64(f"{ASSETS}/logo.png")           # 821×297 iRTE2026 / 实时智能大会 页眉 logo

# ══════════════════════════════════════════════════════════════════════
# 0) 像素格数字（模板章节号「01」用的 Z Labs Bitmap 未嵌入，自绘 5×7 点阵）
# ══════════════════════════════════════════════════════════════════════
GLYPHS = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}


def pix(text, cell=21, gap=3, color="#96FF9D"):
    """5×7 点阵像素字 → <svg>。方块 + 留缝（与 KV 里像素字同语法），字间空 1 列。"""
    cols = len(text) * 6 - 1          # 每字 5 列 + 字间 1 列空
    w, h = cols * cell, 7 * cell
    blk = cell - gap
    rects = []
    for gi, ch in enumerate(text):
        rows = GLYPHS[ch]
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "1":
                    x = (gi * 6 + c) * cell
                    y = r * cell
                    rects.append(
                        f'<rect x="{x:.4g}" y="{y:.4g}" width="{blk:.4g}" height="{blk:.4g}"/>')
    return (f'<svg width="{w:.4g}" height="{h:.4g}" viewBox="0 0 {w:.4g} {h:.4g}" '
            f'fill="{color}" shape-rendering="crispEdges" aria-hidden="true">'
            + "".join(rects) + "</svg>")


# ══════════════════════════════════════════════════════════════════════
# 1) token 块：CONF 紫金 → irte 绿青紫（单主题，母稿已无主题切换与 deckSwap）
#    映射依据见规范 §6。--mark-3 不在 §6 表里但母稿 `[fill="var(--ink-3)"]`
#    依赖它（图内灰圆点不跟着文字灰走），照母稿原值保留。
#    --ink-2 / --ink-3 不取规范 §6 的模板正文灰（#B8BEC9 / #8993A5），取母稿 C8「灰字提亮」
#    的档位换成模板的冷灰色相（#DDE1E8 / #C3C9D3）——C8 是 Colin 在大屏上定的可读性决定，
#    优先级高于模板的 PPT 字色（Fable 终审 2026-09-08）。
# ══════════════════════════════════════════════════════════════════════
i = s.index(":root{")
k = s.index("}", s.index("--warn-bg", i)) + 1
IRTE_TOKENS = """:root{
  --stage-bg:#080C14;
  --slide-bg:#080C14;
  --card-bg:#0E1422;
  --card-bg-2:#101829;
  --cardw-bg:#ffffff;
  --cardw-ink:#111111;
  --cardw-ink2:#3c3c46;
  --cardw-tag:#8a8aa0;
  --cardw-am:#5C22A5;
  --cardw-co:#004660;
  --file-bg:#05080E;
  --hair:rgba(137,147,165,.32);
  --hair-soft:rgba(137,147,165,.16);
  --hair-strong:rgba(137,147,165,.55);
  --ink:#FFFFFF;
  --ink-2:#DDE1E8;
  --ink-3:#C3C9D3;
  --mark-3:#A5A5A5;
  --amber:#96FF9D;
  --coral:#7FF4FF;
  --magenta:#B29BFF;
  --mq:#FFFFFF;
  --mq-2:#96FF9D;
  --flow-line:rgba(178,155,255,.28);
  --flow-line-2:rgba(137,147,165,.14);
  --flow-op:.35;
  --on-fill:rgba(92,34,165,.22);
  --on-bg:linear-gradient(180deg,rgba(92,34,165,.34),rgba(92,34,165,.10));
  --warn-bg:linear-gradient(180deg,rgba(127,244,255,.10),rgba(127,244,255,.02));
}"""
assert s[i:k].count("--stage-bg") == 1 and "--amber" in s[i:k], "token 块定位失败"
s = s[:i] + IRTE_TOKENS + s[k:]
HITS.append(("token 块", 1))

# 母稿另有一个「SVG 里不能用渐变变量当 fill」的 :root 补丁块，它会覆盖上面的
# --on-fill（橙残留）。同步换成 irte 深紫 / 青。
s = rep(s,
        "  --on-fill:rgba(255,142,60,.11);\n  --warn-fill:rgba(217,55,110,.09);",
        "  --on-fill:rgba(92,34,165,.22);\n  --warn-fill:rgba(127,244,255,.09);",
        1, "on-fill/warn-fill 实色补丁")

# ══════════════════════════════════════════════════════════════════════
# 2) 字体：普惠体 2.0 → 思源黑体（模板 theme fontScheme「iRTE Source Han Sans CN」）
#    --f-cn / --f-en 同栈（模板全篇一套字，英文也是思源）；--f-mono 不动。
#    母稿两处 :root 都定义了这两个变量（后一处是「字体健壮性」兜底块），都要换。
# ══════════════════════════════════════════════════════════════════════
HAN = ("'Source Han Sans CN','Source Han Sans SC','Noto Sans CJK SC','Noto Sans SC',"
       "'PingFang SC','HarmonyOS Sans SC','Microsoft YaHei',sans-serif")
s = rep(s,
        "  --f-cn:'Alibaba PuHuiTi 2.0','阿里巴巴普惠体 2.0',-apple-system,'PingFang SC',"
        "'Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif;",
        f"  --f-cn:{HAN};", 2, "--f-cn ×2")
s = rep(s,
        "  --f-en:'Alibaba PuHuiTi 2.0','阿里巴巴普惠体 2.0','Calibri',-apple-system,"
        "'PingFang SC',sans-serif;",
        f"  --f-en:{HAN};", 2, "--f-en ×2")
# Satoshi 已无人引用（--f-en 换栈后），两条 @font-face 一并撤掉：
# 家族纪律「站内引用只许 /fonts/JetBrainsMono-*.woff2 与 /media/cowork/p3-call.mp3」。
s = rep(s,
        "@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');"
        "font-weight:700;font-display:swap;}\n"
        "@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');"
        "font-weight:900;font-display:swap;}\n", "", 1, "撤 Satoshi @font-face")
assert "Satoshi" not in s, "Satoshi 残留"

# ══════════════════════════════════════════════════════════════════════
# 3) <title>（noindex meta 原样保留）
# ══════════════════════════════════════════════════════════════════════
s, nt = re.subn(r"<title>[^<]*</title>",
                "<title>从「被托付」到「双向奔赴 · 共事」· iRTE 2026 实时智能大会 · 产品专场</title>",
                s, count=1)
assert nt == 1
HITS.append(("<title>", 1))

# ══════════════════════════════════════════════════════════════════════
# 4) 切 head / sections / tail
# ══════════════════════════════════════════════════════════════════════
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
_en = [s.index("</section>", t) + len("</section>") for t in _st]
head, tail = s[:_st[0]], s[_en[-1]:]
secs = [s[_st[i]:_en[i]] for i in range(len(_st))]
assert len(secs) == 46, f"母稿应 46 页，实际 {len(secs)}"

# ── 4.1 P1 封面 = 模板 slide 3「专场标题页」 ──────────────────────────
COVER = '''<section class="slide active l2 cover-irte">
  <div class="ic">
    <div class="ic-kicker flow" style="--i:0">&gt; iRTE 2026 · 产品专场</div>
    <h1 class="ic-title ink" style="--i:1">从「被托付」<br>到「双向奔赴 · 共事」</h1>
    <div class="ic-sub spread" style="--i:3">对话式智能体的信任进化</div>
    <div class="ic-speaker rise" style="--i:5">姚光华 Colin｜声网 · AI 产品线负责人</div>
    <div class="ic-date rise" style="--i:6">2026.10.23–24 · 北京悠唐皇冠假日酒店</div>
    <div class="ic-logo" aria-hidden="true"></div>
    <div class="ic-px" aria-hidden="true"></div>
  </div>
</section>'''
assert 'class="confcover"' in secs[0], "P1 不是母稿 confcover 封面"
secs[0] = COVER
HITS.append(("P1 封面整段替换", 1))

# ── 4.2 P2 开场 → 声网主场（只换文案，SVG 骨架 / 坐标 / 动效类原样） ──
p2 = secs[1]
assert 'PART 0 · 开场</span><span>2<' in p2
P2_EDITS = [
    ('<div class="eyebrow flow" style="--i:0">回到讲台</div>',
     '<div class="eyebrow flow" style="--i:0">主场 · 从 RTC 到对话式 AI</div>'),
    ('<h2 class="ink" style="--i:1">第三次，站上同一个讲台</h2>',
     '<h2 class="ink" style="--i:1">交出去的东西，一年比一年重</h2>'),
    # 2024
    ('>生成式 AI × 实时互动</text>', '>Realtime API · 全球首批合作伙伴</text>'),
    ('>职能边界开始融合</text>', '>把模型接进实时通道</text>'),
    ('>一段可以改的草稿</text>', '>一条通向模型的实时通道</text>'),
    # 2025
    ('>活人感 → 体验基准</text>', '>引擎 1.0 · R1 GA</text>'),
    ('>可以用实验验证，就不该等待共识</text>', '>活人感成了体验基准</text>'),
    ('>一个可以复核的判断</text>', '>一场听起来像人的对话</text>'),
    # 2026（txt / lbl / sm 三行不动）
    ('>被托付 → 双向奔赴</text>', '>Call Agent 全球版</text>'),
    # note
    ('三个题目，是<b>同一场转身的三层</b>——2024 职能融合，2025 人与组织，'
     '今年轮到<b class="am">我们和它的关系</b>。',
     '三个节点，是<b>同一场转身的三层</b>——2024 通道，2025 体验，'
     '今年轮到<b class="am">我们和它的关系</b>。'),
]
for old, new in P2_EDITS:
    p2 = rep(p2, old, new, 1, "P2 " + re.sub(r"<[^>]+>", "", old)[:22])
secs[1] = p2

# ── 4.3 四张章节页 .act（P6 / P13 / P26 / P39）→ 模板 slide 4 版式 ────
ACTS = {5: ("1", "GRAMMAR"), 12: ("2", "ENTRUSTED"),
        25: ("3", "COWORK"), 38: ("4", "PEOPLE &amp; ORG")}
for idx, (num, en) in ACTS.items():
    sec = secs[idx]
    assert '<div class="act">' in sec, f"S{idx+1} 不是章节页"
    sec = rep(sec, '<section class="slide">', '<section class="slide l2">', 1,
              f"P{idx+1} act l2")
    sec = rep(sec,
              f'<div class="num flow" style="--i:0">PART {num}</div>',
              f'<div class="num flow" style="--i:0">{pix("0" + num, cell=150 / 7)}'
              f'<span class="sr">PART {num}</span></div>',
              1, f"P{idx+1} 像素章节号 0{num}")
    sec = rep(sec,
              f'<div class="en settle" style="--i:1">{en}</div>',
              f'<div class="en settle" style="--i:1">PART {num} · {en}</div>',
              1, f"P{idx+1} .en → PART {num} · {en}")
    secs[idx] = sec

# ── 4.4 五张金句页 .mq 加 L2 星空底（P12 / P21 / P25 / P33 / P36） ────
#     P16 是 .ask（页底纯色，见规范：只有非正文页用 L2；.ask 是正文提问页），
#     P46 结语是普通 .wrap 页。
for idx in (11, 20, 24, 32, 35):
    sec = secs[idx]
    assert '<div class="mq">' in sec, f"S{idx+1} 不是金句页"
    m = re.match(r'<section class="slide ', sec)
    assert m, f"S{idx+1} class 形状意外"
    secs[idx] = sec.replace('<section class="slide ', '<section class="slide l2 ', 1)
    HITS.append((f"P{idx+1} mq l2", 1))

# ── 4.5 四页案例留白（P15 / P22 / P31 / P32 整段替换） ────────────────
PH_TPL = '''<section class="slide ph">
  <div class="chrome"><span>{crumb}</span><span>{no}</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">案例 {cn} · 待定 · CASE TBD</div>
      <h2 class="ink" style="--i:1"><span class="ph-t">案例标题 · 待定</span></h2>
    </div>
    <div class="body">
      <div class="ph-box ph-fig rise" style="--i:2"><span>主图区 · 图 / 曲线 / 录音</span></div>
      <div class="ph-row">
        <div class="ph-box rise" style="--i:3"><span>数据 01</span></div>
        <div class="ph-box rise" style="--i:4"><span>数据 02</span></div>
        <div class="ph-box rise" style="--i:5"><span>数据 03</span></div>
      </div>
      <div class="ph-box ph-land rise" style="--i:6"><span>落点一句 · 待定</span></div>
    </div>
  </div>
</section>'''
for n, (idx, cn) in enumerate([(14, "01"), (21, "02"), (30, "03"), (31, "04")]):
    m = re.search(r'<div class="chrome"><span>(.*?)</span><span>(.*?)</span></div>', secs[idx])
    assert m, f"S{idx+1} 无 chrome"
    crumb, no = m.group(1), m.group(2)
    assert "CASE" in crumb, f"S{idx+1} 不是案例页：{crumb}"
    secs[idx] = PH_TPL.format(crumb=crumb, no=no, cn=cn)
    HITS.append((f"P{idx+1} 案例留白 {cn}", 1))

# ── 4.5b P29 图例色名跟色板走（母稿按颜色名指代圆点：紫 / 金黄 ⇒ 绿 / 青） ──
# 全 deck 唯一一处用颜色名指代 token 色的正文；不改就是错话（Fable 终审 2026-09-08）。
p29 = secs[28]
assert "真实岗位放上梯子" in p29, "S29 不是岗位梯子页"
p29 = rep(p29, "紫 = 已规模商业化", "绿 = 已规模商业化", 1, "P29 图例色名 紫→绿")
p29 = rep(p29, "金黄 = 强监管场景", "青 = 强监管场景", 1, "P29 图例色名 金黄→青")
secs[28] = p29

# ── 4.5c P23 「为结果付费」实心块：绿 100% 在投影上太冲 ⇒ 绿 .28 底 + 绿 2px 描边 ──
# （母稿是实心紫，等量替换后饱和度高一档；判断：块的语义是「实心 = 落点」，描边保住实心感）
p23 = secs[22]
assert "为结果付费" in p23, "S23 不是商业模式页"
p23 = rep(p23, '<rect class="fill-am pop" style="--i:6" x="1260" y="60" width="300" height="240"/>',
          '<rect class="fill-am pop" style="--i:6" x="1260" y="60" width="300" height="240" '
          'fill-opacity=".28" stroke="var(--amber)" stroke-width="2"/>', 1, "P23 结果付费块降饱和")
secs[22] = p23

# ── 4.6 删 P44（单向门 / 双向门） ─────────────────────────────────────
assert "单向门" in secs[43] and "image/webp" in secs[43], "S44 不是门页"
del secs[43]
HITS.append(("删 P44 单向门/双向门", 1))

# ── 4.7 原 P45「一页带走」→ 新 P44：四句换对象 ───────────────────────
tk = secs[43]
assert 'class="take"' in tk and "全场收束" in tk, "S45 不是一页带走页"
TAKE_EDITS = [
    ('<div class="eyebrow flow" style="--i:0">ONE LINE EACH · 越往上，答案越短，也越重</div>',
     '<div class="eyebrow flow" style="--i:0">ONE LINE EACH · 从外到内，答案越短，也越重</div>'),
    # 01 开发者
    ('<div class="who">产品经理</div>', '<div class="who">开发者</div>'),
    ('<span class="no">交的不再是一份 PRD</span>', '<span class="no">交的不再是一个 demo</span>'),
    # 02 客户
    ('<div class="who">产品管理者</div>', '<div class="who">客户</div>'),
    ('<span class="no">管的不再是三个职能</span><em>一个新的融合岗位</em>',
     '<span class="no">买的不再是调用量</span><em>一个岗位的结果</em>'),
    ('<div class="s">产品、设计、研发，走进客户现场，融合成 FDE——第四个圆不是新部门，'
     '是一个新岗位的定义。</div>',
     '<div class="s">计价单位从「用了多少」换成「岗位交付了什么」。验收方式一变，'
     '交付方式、成本科目跟着全变。</div>'),
    # 03 伙伴
    ('<div class="who">CEO</div>', '<div class="who">伙伴</div>'),
    ('<span class="no">卖的不再是调用量</span><em>一门结果生意</em>',
     '<span class="no">拼的不再是各自的参数</span><em>同一把尺子上的那一格</em>'),
    ('<div class="s">计价单位从「用了多少」换成「岗位交付了什么」。定价一变，'
     '产品形态、交付方式、成本科目跟着全变。</div>',
     '<div class="s">全景图上那五条线，不是声网一家的门槛，是整条链路的共同验收——'
     '模型、语音、集成商各自站上去，客户才敢托付。</div>'),
    # 04 自己
    ('<div class="who">组织</div>', '<div class="who">自己</div>'),
    ('<span class="no">要的不是 AI 能力</span><em>一套放权与决策机制</em>',
     '<span class="no">问的不再是它能不能</span><em>我敢不敢放权</em>'),
    ('<div class="s">Agent 有 L1–L5，人有看过·用过·学过·干过——组织真正的活，'
     '是定一套决策机制：把权放到这两把梯子够得着的那一格。</div>',
     '<div class="s">Agent 有 L1–L5，人有看过·用过·学过·干过——'
     '把权放到自己够得着的那一格，然后往上爬一格。</div>'),
]
for old, new in TAKE_EDITS:
    tk = rep(tk, old, new, 1, "P44 " + re.sub(r"<[^>]+>", "", old)[:20])

# 底部图标行：① 评测（尺子）不动；② 原第三槽价签打勾整组平移到第二槽（dx=-426，x 中心 627）；
# ③ 第三槽新画「尺子上的那一格」；④ 第四槽新画「梯子」。
# --i 节拍按槽位保留原节奏（槽 1→4 = 0/1 · 1/2 · 2/3 · 3/4），动画包络与母稿一致。
OLD_SLOT2 = '''          <!-- ② 岗位 · 三圆交叠再加第四圆（FDE 那一圈是新的） -->
          <g class="pop" style="--i:1">
            <circle class="stroke" stroke-width="1.4" cx="588" cy="46" r="30"/>
            <circle class="stroke" stroke-width="1.4" cx="614" cy="46" r="30"/>
            <circle class="stroke" stroke-width="1.4" cx="640" cy="46" r="30"/>
          </g>
          <circle class="stroke-am pop" style="--i:2" stroke-width="2.4" cx="666" cy="46" r="30"/>
          <text class="ttl pop" style="--i:2;font-size:23px" x="627" y="118" text-anchor="middle">岗位</text>

          <!-- ③ 结果生意 · 价签上打勾才结算 -->
          <path class="stroke dw" style="--len:320;--i:2" stroke-width="1.5" d="M1026 18 H1104 A8 8 0 0 1 1112 26 V70 A8 8 0 0 1 1104 78 H1026 L994 48 Z"/>
          <circle class="stroke pop" style="--i:2" stroke-width="1.4" cx="1018" cy="48" r="5"/>
          <path class="stroke dw" style="--len:64;--i:3" stroke-width="2.4" stroke-linecap="round" d="M1042 48 L1056 62 L1086 30"/>
          <text class="ttl pop" style="--i:3;font-size:23px" x="1053" y="118" text-anchor="middle">结果生意</text>

          <!-- ④ 放权决策机制 · 左边双向门（进得去回得来），右边单向门（推开就没有回头） -->
          <path class="stroke dw" style="--len:250;--i:3" stroke-width="1.5" d="M1400 18 H1464 V78 H1400 Z"/>
          <path class="stroke dw" style="--len:250;--i:3" stroke-width="1.5" d="M1496 18 H1560 V78 H1496 Z"/>
          <g class="pop" style="--i:4">
            <path class="stroke" stroke-width="1.4" d="M1414 48 H1450"/>
            <path class="fill-ink" d="M1408 48 L1418 42 L1418 54 Z"/>
            <path class="fill-ink" d="M1456 48 L1446 42 L1446 54 Z"/>
            <path class="stroke" stroke-width="1.8" d="M1508 38 V58"/>
            <path class="stroke" stroke-width="1.4" d="M1508 48 H1544"/>
            <path class="fill-ink" d="M1552 48 L1542 42 L1542 54 Z"/>
          </g>
          <text class="ttl pop" style="--i:4;font-size:23px" x="1480" y="118" text-anchor="middle">放权决策机制</text>'''
NEW_SLOT2 = '''          <!-- ② 结果 · 价签上打勾才结算（原第三槽整组左移 426 到 x 中心 627） -->
          <path class="stroke dw" style="--len:320;--i:1" stroke-width="1.5" d="M600 18 H678 A8 8 0 0 1 686 26 V70 A8 8 0 0 1 678 78 H600 L568 48 Z"/>
          <circle class="stroke pop" style="--i:1" stroke-width="1.4" cx="592" cy="48" r="5"/>
          <path class="stroke dw" style="--len:64;--i:2" stroke-width="2.4" stroke-linecap="round" d="M616 48 L630 62 L660 30"/>
          <text class="ttl pop" style="--i:2;font-size:23px" x="627" y="118" text-anchor="middle">结果</text>

          <!-- ③ 那一格 · 尺子上被点名的第四格 -->
          <path class="stroke dw" style="--len:144;--i:2" stroke-width="1.5" d="M981 66 H1125"/>
          <g class="pop" style="--i:2"><path class="stroke" stroke-width="1.4" d="M989 40 V66 M1021 40 V66 M1053 40 V66 M1085 40 V66 M1117 40 V66"/></g>
          <circle class="fill-am pop" style="--i:3" cx="1085" cy="34" r="6"/>
          <text class="ttl pop" style="--i:3;font-size:23px" x="1053" y="118" text-anchor="middle">那一格</text>

          <!-- ④ 放权 · 梯子（往上爬一格） -->
          <path class="stroke dw" style="--len:136;--i:3" stroke-width="1.5" d="M1448 16 V80 M1512 16 V80"/>
          <g class="pop" style="--i:3"><path class="stroke" stroke-width="1.4" d="M1448 22 H1512 M1448 35 H1512 M1448 61 H1512 M1448 74 H1512"/></g>
          <path class="stroke-am pop" style="--i:4" stroke-width="2.4" d="M1448 48 H1512"/>
          <text class="ttl pop" style="--i:4;font-size:23px" x="1480" y="118" text-anchor="middle">放权</text>'''
tk = rep(tk, OLD_SLOT2, NEW_SLOT2, 1, "P44 图标行 ②③④ 重画")
secs[43] = tk

# ── 4.8 Q&A 尾卡（新 P46 = 模板 slide 17） ───────────────────────────
QA = '''<section class="slide l2 qa-irte">
  <div class="qa">
    <div class="qa-big settle" style="--i:0">Q&amp;A</div>
    <div class="qa-line flow" style="--i:2">&gt; 有什么想一起继续讨论？</div>
    <div class="qa-me rise" style="--i:4">姚光华 Colin · colinyao.com</div>
    <div class="ic-px" aria-hidden="true"></div>
  </div>
</section>'''
secs.append(QA)
HITS.append(("Q&A 尾卡", 1))
assert len(secs) == 46, f"输出应 46 页，实际 {len(secs)}"

# ── 4.9 chrome 页码重排（删 P44 后：原 45→44、原 46→45） ─────────────
def _set_no(sec, no):
    return re.sub(r'(<div class="chrome"><span>.*?</span><span>)\d+(</span></div>)',
                  lambda m: m.group(1) + str(no) + m.group(2), sec, count=1)


renum = 0
for i2, sec in enumerate(secs):
    m = re.search(r'<div class="chrome"><span>.*?</span><span>(\d+)</span></div>', sec)
    if not m:
        continue
    want = i2 + 1
    if int(m.group(1)) != want:
        secs[i2] = _set_no(sec, want)
        renum += 1
assert renum == 2, f"应重排 2 个页码，实际 {renum}"
HITS.append(("chrome 页码重排 45→44 / 46→45", renum))

# 页码序列自检：有 chrome 的页，页码 = 其页序，无重复无跳号
nums = []
for i2, sec in enumerate(secs):
    m = re.search(r'<div class="chrome"><span>.*?</span><span>(\d+)</span></div>', sec)
    if m:
        nums.append((i2 + 1, int(m.group(1))))
assert all(a == b for a, b in nums), f"页码错位：{[x for x in nums if x[0] != x[1]]}"
assert len({b for _, b in nums}) == len(nums), "页码有重复"

# ══════════════════════════════════════════════════════════════════════
# 5) tail：删 conf 视觉层 / 门图 CSS，写 irte 模板视觉层
# ══════════════════════════════════════════════════════════════════════
CONF_HEAD = "/* ============ 2026 AI 产品大会 · 版式覆盖层 ============ */"
NEXT_HEAD = "/* 压缩层 · 左右双栏与北极星挂载 */"
a = tail.index(CONF_HEAD)
b = tail.index(NEXT_HEAD)
assert tail.count(CONF_HEAD) == 1 and a < b
conf_block = tail[a:b]
assert conf_block.count("image/jpeg") == 2 and conf_block.count("image/png") == 2

IRTE_CSS = """/* ============ iRTE 2026 · 模板视觉层 ============ */
/* 视觉真源 = iRTE2026_PPT模板_产品.pptx（规范 v1）。
   模板给色 / 字 / 标记 / 页型，CONF 给字号尺度与版式密度 —— 所以这一段只换
   颜色、字重、标记与页型，不动 h2 60px / eyebrow 17px mono / 正文 19–22px。 */

/* 页底：正文页纯 #080C14；L2（星空 1920×850 + 紫像素阶梯，左右各裁 10.648%
   ⇒ background-size 2440×1080 居中）+ 一层 dk2 34.9% 蒙版，只给封面 / 四张章节页 /
   五张金句页 / Q&A 尾卡。.l2 写成 .slide.l2 是为了避开 .deck-flow 里同名的 path.l2。 */
.slide{background:#080C14;}
.slide.l2{background:#080C14 url(data:image/png;base64,__BG__) center/2440px 1080px no-repeat;}
.slide.l2::before{content:'';position:absolute;inset:0;background:rgba(8,12,20,.349);z-index:0;}

/* 页眉：深紫小方块 + 面包屑；右上角模板 logo 落在页面坐标 (1660.8, 39.2) 222.7×80.6。
   .chrome 是 left/right 120 · top 44 的绝对定位条 ⇒ left 1540.8 / top -4.8。
   页码右缘 = 1920-120-190 = 1610 ≤ 1630，不进 logo 盒。 */
.chrome{align-items:center;}
.chrome span:first-child{position:relative;padding-left:18px;color:var(--ink-3);letter-spacing:.18em;}
.chrome span:first-child::before{content:"";position:absolute;left:0;top:50%;transform:translateY(-50%);
  width:10px;height:10px;background:#5C22A5;}
.chrome span:last-child{margin-right:190px;color:var(--ink-3);}
.chrome::after{content:'';position:absolute;left:1540.8px;top:-4.8px;width:222.7px;height:80.6px;
  background:url(data:image/png;base64,__LOGO__) center/contain no-repeat;opacity:.95;}

/* eyebrow = 模板 kicker：`>` 提示符 + 薰衣草字 + 底下深紫短条 81×4.5。
   padding-bottom 10 + margin-bottom 12 = 母稿的 22 ⇒ h2 位置 Δ0，40 页正文不重排。 */
.eyebrow{color:#B29BFF;padding-bottom:10px;
  background:linear-gradient(#5C22A5,#5C22A5) left bottom/81px 4.5px no-repeat;}
.eyebrow::before{content:'>';width:auto;height:auto;background:none;font-family:var(--f-mono);
  font-weight:700;font-size:19px;line-height:1;color:#B29BFF;}
/* 母稿的 .eyebrow.coral::before / .grey::before 只改 background（原来是一根实心小横条），
   权重比 .eyebrow::before 高 —— 不显式清掉，`>` 会被涂成一块实心色块。 */
.eyebrow.coral::before{background:none;color:var(--coral);}
.eyebrow.grey{background-image:linear-gradient(var(--ink-3),var(--ink-3));}
.eyebrow.grey::before{background:none;color:var(--ink-3);}
.head .eyebrow{margin-bottom:12px;}

/* .mega .mark / .ask .badge 同法：`>` 前缀 + 薰衣草 */
.mega .mark{color:#B29BFF;display:flex;align-items:center;gap:16px;}
.mega .mark::before{content:'>';flex:none;font-family:var(--f-mono);font-weight:700;
  font-size:19px;line-height:1;color:#B29BFF;}
.ask .badge{color:#B29BFF;}
.ask .badge::before{content:'>';width:auto;height:auto;background:none;font-family:var(--f-mono);
  font-weight:700;font-size:19px;line-height:1;color:#B29BFF;}
.ask .hl{color:#96FF9D;}

/* 章节页 .act = 模板 slide 4：像素章节号 / 白色章节主题 / 绿竖条小标题 / 右下 > NEXT。
   母稿 .act 的 flex 与四个子件的 flow/settle/spread 动效保留；改成绝对定位后 flex 不再起作用。 */
.act .num{position:absolute;left:108px;top:130px;height:150px;}
.act .num svg{display:block;height:150px;width:auto;}
.act .cn{position:absolute;left:108px;top:374px;font-size:88px;font-weight:700;color:#fff;
  letter-spacing:.01em;padding-right:0;line-height:1.15;}
.act .en{position:absolute;left:108px;top:665px;border-left:6px solid #96FF9D;padding:6px 0 6px 30px;
  font-family:var(--f-mono);font-size:22px;font-weight:500;line-height:1;letter-spacing:.2em;
  color:var(--ink-2);-webkit-mask-image:none;mask-image:none;}
.act .rail{position:absolute;left:auto;right:189px;top:auto;bottom:131px;transform:none;
  align-items:flex-end;gap:10px;}
.act .rail span{color:rgba(255,255,255,.62);}   /* 落在紫阶梯上：灰蓝在紫上读不出，改半透明白 */
.act .rail span.cur{color:#7FF4FF;}
.act .rail span.cur::before{content:'> ';}
.act .rail span.cur::after{content:none;}
.act::after{content:'';position:absolute;right:36.5px;top:39.2px;width:222.7px;height:80.6px;
  background:url(data:image/png;base64,__LOGO__) center/contain no-repeat;opacity:.95;}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0;}

/* 金句页 .mq：白字 + 绿尺，不放 logo（模板无此页型，判断：金句页要空） */
.mq .q i{color:#fff;}
.mq .rule{background:#96FF9D;}
.mq .s{color:var(--ink-3);}
.mq .en{color:#B8BEC9;}

/* 一页带走：两条橙残留边框跟主强调走（绿） */
.take .c:nth-child(2){border-left-color:rgba(150,255,157,.34);}
.take .c:nth-child(3){border-left-color:rgba(150,255,157,.64);}

/* 案例留白页 .ph：虚线占位框，等 Colin 填新案例 */
.ph-t{color:var(--ink-3);}
.ph-box{border:1.5px dashed var(--hair-strong);border-radius:4px;display:flex;
  align-items:center;justify-content:center;font-family:var(--f-mono);font-size:15px;
  letter-spacing:.22em;color:var(--ink-3);}
.ph-fig{height:400px;}
.ph-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;margin-top:24px;}
.ph-row .ph-box{height:150px;}
.ph-land{height:74px;margin-top:24px;}

/* 封面 = 模板 slide 3「专场标题页」：绝对坐标上对齐，不是 flex 居中 */
.ic{position:absolute;inset:0;}
.ic-kicker{position:absolute;left:108px;top:136.6px;margin:0;font-size:37px;font-weight:700;
  color:#B29BFF;letter-spacing:.02em;line-height:1.2;}
.ic-title{position:absolute;left:108px;top:238px;width:1424px;margin:0;font-size:72px;
  font-weight:700;line-height:1.22;color:#fff;letter-spacing:.01em;padding-right:.08em;}
/* 238 + 2 行 ×(72×1.22) + 26 = 439.7 —— 标题写死两行（<br>），所以直接落数 */
.ic-sub{position:absolute;left:108px;top:439.7px;margin:0;font-size:30px;color:#B8BEC9;
  letter-spacing:.06em;line-height:1.4;}
.ic-speaker{position:absolute;left:108px;top:644.8px;margin:0;font-size:37px;font-weight:700;
  color:#96FF9D;letter-spacing:.02em;line-height:1.2;}
.ic-date{position:absolute;left:108px;top:743px;margin:0;font-family:var(--f-mono);font-size:17px;
  letter-spacing:.1em;color:#8993A5;line-height:1.2;}
.ic-logo{position:absolute;left:1572.3px;top:483.7px;width:320.4px;height:115.9px;
  background:url(data:image/png;base64,__LOGO__) center/contain no-repeat;}
/* 四色像素块：绿 / 青 / 薰衣草 / 深青，13×11.5 @ (168,851) 间距 27（一枚元素 + box-shadow） */
.ic-px{position:absolute;left:168px;top:851px;width:13px;height:11.5px;background:#96FF9D;
  box-shadow:27px 0 0 #7FF4FF,54px 0 0 #B29BFF,81px 0 0 #004660;}

/* Q&A 尾卡 = 模板 slide 17（Q&A 用思源黑体 Bold，不是像素字） */
.qa{position:absolute;inset:0;}
.qa-big{position:absolute;left:108px;top:174.4px;margin:0;font-size:170px;font-weight:700;
  line-height:1;color:#96FF9D;letter-spacing:-.01em;}
.qa-line{position:absolute;left:108px;top:532.9px;margin:0;font-size:32px;font-weight:700;
  color:#fff;line-height:1.3;}
.qa-me{position:absolute;left:108px;top:600px;margin:0;font-family:var(--f-mono);font-size:17px;
  letter-spacing:.1em;color:#8993A5;line-height:1.2;}
.qa::after{content:'';position:absolute;right:36.5px;top:39.2px;width:222.7px;height:80.6px;
  background:url(data:image/png;base64,__LOGO__) center/contain no-repeat;opacity:.95;}

"""
IRTE_CSS = IRTE_CSS.replace("__BG__", BG_STARS).replace("__LOGO__", LOGO)
tail = tail[:a] + IRTE_CSS + tail[b:]
HITS.append((".confcover / conf 版式覆盖层整段替换", 1))

# @media print 里给 conf logo 的补丁
tail = rep(tail, "@media print{.chrome::after,.confcover::after{opacity:1;}}\n",
           "@media print{.chrome::after,.act::after,.qa::after{opacity:1;}}\n",
           1, "@media print logo 补丁")

# ── 5.1 三条「压缩层比 irte 覆盖层更靠后、按层叠会赢」的规则，就地拨回 ───────
# irte 覆盖层写在 conf 覆盖层原位（C7 之前），后面的 C9–C21 压缩层同名或更高
# 权重的规则会盖过它，所以这三条只能在原地改：
#   ① .r9p15 .ask .badge::before —— 母稿把 56×1 的线加宽到 80px；现在 ::before 是
#      一个「>」字符，80px 固定宽会在 > 和文字之间撑出一个 60px 的空洞。
#   ② .act .rail span —— 压缩层把 16px 顶到 18px；任务书章节页规格是 16px mono 灰。
#   ③ .r16mq2/.r16mq3 .mq .en —— 英文句用 var(--mq-2)（现在 = 绿），压过 irte 的
#      .mq .en{color:#B8BEC9}；按任务书金句页规格改回模板正文灰。
tail = rep(tail, ".r9p15 .ask .badge::before{width:80px;}",
           ".r9p15 .ask .badge::before{width:auto;}", 1, "P16 badge::before 宽度拨回 auto")
tail = rep(tail, "\n.act .rail span{font-size:18px;}", "\n.act .rail span{font-size:16px;}",
           1, "章节页 rail 字号 18→16")
tail = rep(tail,
           ".r16mq2 .mq .en,.r16mq3 .mq .en{font-family:var(--f-mono);font-size:30px;"
           "font-weight:700;\n  line-height:1.5;letter-spacing:0;color:var(--mq-2);max-width:1420px;}",
           ".r16mq2 .mq .en,.r16mq3 .mq .en{font-family:var(--f-mono);font-size:30px;"
           "font-weight:700;\n  line-height:1.5;letter-spacing:0;color:#B8BEC9;max-width:1420px;}",
           1, "金句页英文行 → 模板正文灰 #B8BEC9")

# C18 门图 CSS 段（.r18doors）——整段删到 C19 段头之前
C18 = "/* ============ C18 · R18 · P44 换 GPT 生成门图（单图双门 · screen 融底） ============ */"
C19 = "/* ============ C19 · R19 · P7 对数时间轴三线图 / 金句页去 eyebrow / 门图收比例 ============ */"
c18a, c19a = tail.index(C18), tail.index(C19)
assert c18a < c19a and tail[c18a:c19a].count(".r18doors") >= 6
tail = tail[:c18a] + tail[c19a:]
HITS.append(("删 C18 .r18doors CSS 段", 1))

# C19 段里的 .r19doors 两条
tail = rep(tail,
           "/* P44 门图：Colin 说现在有点过大 —— 1380 收到 1180（高 552 → 472），留白多一点。\n"
           "   标签仍是 % 定位（27.2% / 72.3%），随图等比自适应，一个数都不用改。 */\n"
           ".r19doors .body{gap:32px;}\n.r19doors .doors{max-width:1180px;}\n\n",
           "", 1, "删 .r19doors CSS")
assert "r18doors" not in tail and "r19doors" not in tail

out = head + "\n".join(secs) + tail

# ══════════════════════════════════════════════════════════════════════
# 6) 构建期断言
# ══════════════════════════════════════════════════════════════════════
n_sec = len(re.findall(r'<section class="slide', out))
assert n_sec == 46, f"输出 section 数 {n_sec} ≠ 46"

for bad in ("image/jpeg", "image/webp", "#9333EA", "#A855F7", "#C084FC", "#FFC000",
            "#7E22CE", "#B45309", "人人都是产品经理", "AI 产品大会", "Alibaba PuHuiTi",
            "普惠体", "单向门", "双向门", "three.js", "WebGL", "<canvas"):
    assert bad not in out, f"输出残留禁词 / 禁色：{bad}"
for must in ("#96FF9D", "#7FF4FF", "#B29BFF", "#5C22A5", "#080C14", "Source Han Sans CN",
             '<meta name="robots" content="noindex, nofollow">'):
    assert must in out, f"输出缺少：{must}"
# 站内引用只许两处
refs = sorted({u for pair in re.findall(
    r'''(?:src|href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)''', out)
    for u in pair if u.startswith("/")})
assert refs == ["/fonts/JetBrainsMono-400.woff2", "/fonts/JetBrainsMono-500.woff2",
                "/media/cowork/p3-call.mp3"], f"站内引用异常：{refs}"
# 案例留白页不许残留母稿案例数据（正文 DOM 口径；tail 里 C9/C11 撑满段的**注释**还
# 写着旧页的 96.5% / 3.08%，那几条选择器已随页面一起失效，是死规则不是页面内容，
# 且与别页共用的撑满规则同段，动它风险大于收益 —— 故断言只走 section 正文）
_dom = "\n".join(secs)
for kw in ("96.5%", "2,475", "3.08%", "入职三十天", "Hugging Face", "刹车"):
    assert kw not in _dom, f"案例留白未清干净：{kw}"

open(OUT, "w", encoding="utf-8").write(out)
size = os.path.getsize(OUT)
assert size < 500 * 1024, f"文件 {size} B ≥ 500 KB"

print(f"母稿 {SRC} {SRC_MD5_LEN:,} B / 46 页")
for tag, n in HITS:
    print(f"  · {tag}  ×{n}")
print(f"→ {OUT}  {size:,} B  {n_sec} 页  （断言全过）")
