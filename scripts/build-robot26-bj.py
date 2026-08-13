#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""robot26 v2 —— 《RTE春夏巡游北京站-ColinVFinal.pptx》36 页一比一还原。

  取代关系
  ────────
  · 老 robot26.html（0516 深圳 36 页 PPT 手工改编成 colin-deck，再由
    build-robot26-full.py 补到 42 页）已归档为 public/decks/robot26-v0516.html，
    不注册路由，只做 aiot26 家族的重建锚点（build-aiot26.py / build-aiot26-v1.py 指它）。
  · 本脚本产出的 public/decks/robot26.html 是**北京站原稿的还原**，不是改编：
    视觉忠于 PPT 自己的模板（纯黑底 + #D4B7F9 淡紫 + Source Han Sans 气质），
    版面按 PPTX 的绝对坐标 1:1 落位（18288000 EMU / 1920px = 9525 EMU/px，正好等比）；
    机械系统（1920×1080 固定舞台 / 键盘翻页 / data-step 分步 / .flow .rise .dw .pop .settle .ink
    / 顶线尺子 / E 键就地编辑）沿用本站 deck 框架。

  数据来源
  ────────
  · scripts/assets/robot26-bj-model.json —— 由 scripts/extract-pptx-model.py 从解包后的
    PPTX 抽出的版面模型（每个 shape 的坐标 / 填充 / 描边 / 文本 run + <p:timing> 点击分组）。
    重新抽取：cd <解包目录> && python3 <repo>/scripts/extract-pptx-model.py > scripts/assets/robot26-bj-model.json
  · scripts/assets/robot26-bj-icons.json —— 12 枚 ≤4KB 的线性小图标（data URI 内联）。
  · public/decks/assets/robot26/ —— 视频 / 大图 / 场次角标（外链，不内联）。

  动效映射（详见 /mnt/user-data/outputs/robot26-动效动线研究.md）
  ────────
  PPT 全场只有一种入场：Dissolve In（溶解）500ms，59 次单击、218 个「与上一动画同时」，
  零退出、零强调、零路径。分步数逐页照搬（data-step = 第几次单击），
  组内按 PPT 自己的 z-order/落笔顺序给 --i 错峰（PPT 是齐进，本站骨架是错峰，
  这是唯一一处有意的「机械系统本地化」，见研究文档 §4）。
  质感按 shape 角色分配：细长矩形 → SVG `.dw` 画线（--len = 实长）；
  图片/圆形 → `.pop`；大字 → `.settle`；主标题 → `.ink`；卡片 → `.rise`；正文 → `.flow`。

  运行：python3 scripts/build-robot26-bj.py
"""
import json, os, re, math, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = json.load(open(os.path.join(ROOT, "scripts/assets/robot26-bj-model.json"), encoding="utf-8"))
ICONS = json.load(open(os.path.join(ROOT, "scripts/assets/robot26-bj-icons.json"), encoding="utf-8"))
_fitp = os.path.join(ROOT, "scripts/assets/robot26-bj-fit.json")
# 二次自适配表：PowerPoint 的 normAutofit（溢出时缩排）在换字体后需要重算的那一点点缩放。
# 由 scripts/fit-robot26.mjs 在 chromium 里实测溢出后生成，键 = "页码:shapeId"。
FIT = json.load(open(_fitp, encoding="utf-8")) if os.path.exists(_fitp) else {}
OUT = os.path.join(ROOT, "public/decks/robot26.html")
A = "/decks/assets/robot26/"

# ── R22 · 金句：编号校正 + 逐张打磨 ──────────────────────────────────────────
# 原稿两处错：① P24/P25 的「MONEY QUOTE · NN」与右下「钉子 · PIN NN」编号互换；
#            ② 标了 OF 05，全场实际只有 4 张。统一成 01–04 OF 04，MQ 与 PIN 同号。
# 打磨口径（Colin R22 授权 brainstorm）：短、反转、有动作、能脱稿念出来。
#   PIN 01 两句都压缩：去掉「因为 / 的 / 值得」这类缓冲词，把反转顶到句尾。
#   PIN 02「别听错。别失控。别让人等。」已经够金 —— 动不如不动，只改编号。
#   PIN 03「模型决定能力上限。引擎决定体验下限。」结构已对仗 —— 不动，只改编号。
#   PIN 04 用 Colin 自己给的种子：「继承」→「抄」，英文副标同步改成对应的动词句。
# 三张金句页统一断成「铺垫，」/「是 反转。」的对句 —— 反转独占一行才念得响，
# 也顺手治了原稿在窄框里的坏断行（关系/破裂、具身/智能被劈开）。
# 格式：(页, shapeId, 段序) : [(新文本, 借第几个原 run 的字号/字色/字重), ...]；ref=None 表示换行
BR = None
QUOTE_PATCH = {
    (4, "10", 0): [("★ ", 0), ("MONEY QUOTE · 01 OF 03", 1)],   # R24：MQ04 删页，重连号
    (4, "11", 0): [("3 ", 0), ("天扔抽屉，不是 ", 1), ("技术故障", 3), ("，", 4), ("", BR),
                   ("是 ", 5), ("关系破裂", 7), ("。", 8)],
    (4, "13", 0): [("用户买的不是 ", 0), ("更聪明的玩具", 4), ("，", 5), ("", BR),
                   ("是 ", 5), ("更处得来的伙伴", 6), ("。", 7)],
    (24, "10", 0): [("★ ", 0), ("MONEY QUOTE · 02 OF 03", 1)],
    (24, "16", 0): [("钉子 · PIN 02", 0)],
    (25, "4", 0): [("★ ", 0), ("MONEY QUOTE · 03 OF 03", 1)],
    (25, "17", 0): [("钉子 · PIN 03", 0)],
    # P28 右上注脚：原稿把「INFO DENSITY HIGH」和中文说明挤在 250px 里折行，
    # 「给」被甩到行尾成孤字 —— 改成显式断行，标签一行、说明一行。
    (28, "4", 0): [("INFO DENSITY HIGH", 0), ("", BR), ("给一线产品经理看的版本", 0)],
    # R24：老 P33（MQ04）整页删除，原三条 patch 随之退役
}


def apply_quote_patch(model):
    """把 QUOTE_PATCH 落到模型上：新 run 整份克隆参考 run 的字号/字色/字重/字距，只换文本。"""
    hit = 0
    for sl in model["slides"]:
        for sh in sl["shapes"]:
            for pi, p in enumerate(sh.get("paras", [])):
                key = (sl["n"], str(sh["id"]), pi)
                if key not in QUOTE_PATCH:
                    continue
                src = p["runs"]
                p["runs"] = [{"br": True} if ref is None else dict(src[ref], t=txt)
                             for txt, ref in QUOTE_PATCH[key]]
                hit += 1
    assert hit == len(QUOTE_PATCH), "QUOTE_PATCH 有 %d 条没落地" % (len(QUOTE_PATCH) - hit)

# ── R22 · mono 标签裁字：宽度放开表 ──────────────────────────────────────────
# 病灶：PPT 里这些角标本来就靠 normAutofit 缩排硬塞进窄框，换字体后仍然折行，
#       读起来像「被剪裁压缩显示不全」（Colin 点名的 CONSUMER ROBOTS, 2025 就是这张）。
#       字号一律不动（保留原字号体系），只把框往**文字锚点的反方向**放开，
#       视觉位置与原稿逐像素一致，只是不再折行。
# 格式：(页, shapeId) : 放开多少 px（右对齐 → 往左放；左对齐 → 往右放；居中 → 两边各半）
WIDEN = {
    (2, "28"): 180,     # RETENTION SHAPE OF CONSUMER ROBOTS, 2025 —— Colin 点名
    (6, "46"): 270,     # FUNCTIONS BOX VS. CHARACTER BEING
    (23, "31"): 120,    # SD-RTN 10 YEARS OF TIMING（R24 顺延：21→23）
}

PT = 4 / 3.0          # 1pt = 4/3 px（1920px 舞台 = 20 英寸 → 96 dpi）
DEF_SZ = 18.0         # presentation.xml defaultTextStyle lvl1
LH = 1.22             # spcPct 100% → CSS line-height（对 Source Han Sans 量得的换算）
MAX_I = 5             # --i 上限：0.44s + 1.7s(dw) < 2.4s，保证 QA 截图不拍到半截

# ── R22 模板层 ──────────────────────────────────────────────────────────────
# R27：SIG（colinyao.com 落款）与 NO_SIG（满幅页豁免）双双退役——
#      右上角改挂连续页码 n/total，见 build_slide 里的 sig 行；想回滚落款版看 git 历史 a809814。

# ── R23 · 封面背景板：P1/P36 撤峰会满幅 keyart，换 colin-deck 暗色模板层 ──────
# Colin 2026-08-09 拍板：P1/P36 的背景板换成自家 deck 设计（此前是峰会 keyart 风格）。
# 做法：这两页跳过 image5.jpeg 满幅 shape → stage 的底流场/栏线网格/发丝导轨透出，
#       与 P2-P35 同一块背景板；两页黑字 #000000 翻 var(--ink)（淡紫 accent 原样保留，
#       文案/坐标/字号/动效一律不动）。cover-ai.jpg 资产随之清零（会场痕迹清零同一纪律）。
# 浅底变体：不进本 deck（colin-deck 节奏铁律「单场一个主题」，本体纯黑）；
#       预览稿由 build 后另行叠加浅底变量生成，不上线不注册路由。
COVER_BG_DROP = {1, 37}          # R24 起尾页顺延为 P37

# ── R24 · P11 一拆三 + 老 P13 严谨化 + MQ04 删页（Colin 2026-08-09 逐页指令）────
# ① 老 P11 拆成三页：Ilya 引文页（GTC 2023 对谈，10 亿词出处）→ 0.29TB 四步推演页
#    （口径与 #03《我们的一生只有 0.29TB》一致：10 亿词 → 25% → ÷150 词/分 ≈ 3.2 年 → 25kbps ≈ 0.29TB）
#    → FIG 01 关系容量曲线整页（左侧卡原几何不动，右侧补伙伴线读数 + TAKEAWAY）。
# ② 老 P13（新 P14）30 年坐标严谨化：第三段「2024 →」改「2022 →」（ChatGPT 2022.11 为拐点，
#    GPT-4o 2024.05 为演进），「ChatGPT · GPT-4o」改「ChatGPT → GPT-4o」；其余三段交叉验证均成立
#    （1990s 固网→蜂窝→IP ✓ / 2010s Siri 2011·Alexa 2014 指令式 ✓ / NOW 共在 ✓）。
# ③ 删老 P33（MQ04「抄作业」页，Colin：有点没意义）——金句重连号 01–03 OF 03，PIN 04 随页退役。
# 页数 36 → 37；P11 之后全部顺延 +2，老 P33 之后回收 -1（老 P34-36 → 新 P35-37）。
W, ZI, HUI = "#FFFFFF", "#D4B7F9", "var(--ink-3)"   # 白 / 淡紫 / 弱灰（沿用模型字面色 + R23 变量惯例）

def _tx(sid, x, y, w, h, paras, anchor="t"):
    return {"kind": "sp", "id": sid, "name": "R24 " + sid, "x": x, "y": y, "w": w, "h": h,
            "geom": "rect", "body": {"anchor": anchor, "ins": [2.67, 2.67, 2.67, 2.67], "wrap": "square", "af": 1},
            "paras": paras}

def _p(runs, ln=None, algn=None, bef=None):
    p = {"runs": [dict(t=t, sz=sz, c=c, **({"b": 1} if b else {}), **({"spc": spc} if spc else {}))
                  for (t, sz, c, b, spc) in runs]}
    if ln: p["ln"] = ln
    if algn: p["algn"] = algn
    if bef: p["bef"] = bef
    return p

def _slide_a():
    """新 P11 · Ilya 引文页：语境节录（左）+ 两拍对白（右，分步）。引文 verbatim，节略以 … 标示。"""
    ctx1 = ("“So there are two dimensions to multi-modality. … The first reason is that "
            "multi-modality is useful. It is useful for a neural network to see … because the "
            "world is very visual. … There is a second reason … which is that we learn more "
            "about the world by learning from images, in addition to learning from text. … ")
    ctx2 = "For a human being, as human beings, we get to hear about one billion words in our entire life.”"
    shapes = [
        _tx("a2", 120, 144, 1730, 34, [_p([("A NUMBER FROM THE SOURCE · ILYA SUTSKEVER × JENSEN HUANG", 15.0, ZI, 1, 6.4)])]),
        _tx("a3", 120, 192, 1730, 146, [_p([("一生，只听得到「 ", 45.0, W, 1, -0.6), ("10 亿词", 45.0, ZI, 1, -0.6),
                                            (" 」。", 45.0, W, 1, -0.6)], ln=1.18)]),
        _tx("a4", 120, 392, 920, 470, [_p([("ILYA SUTSKEVER · 时任 OPENAI 首席科学家", 12.0, HUI, 1, 3.2)]),
                                       _p([(ctx1, 15.0, HUI, 0, 0), (ctx2, 15.0, W, 1, 0)], ln=1.62, bef=18)]),
        _tx("a5", 1160, 430, 640, 150, [_p([("JENSEN HUANG", 12.0, HUI, 1, 3.2)]),
                                        _p([("“Only one billion words?”", 30.0, W, 1, 0)], ln=1.25, bef=14)]),
        _tx("a6", 1160, 640, 640, 190, [_p([("ILYA", 12.0, HUI, 1, 3.2)]),
                                        _p([("“That’s amazing.", 30.0, ZI, 1, 0)], ln=1.3, bef=14),
                                        _p([("That’s not a lot.”", 30.0, ZI, 1, 0)], ln=1.3)]),
        _tx("a7", 120, 972, 1680, 26, [_p([("SOURCE · NVIDIA GTC SPRING 2023 · FIRESIDE CHAT: AI TODAY AND VISION OF THE FUTURE · 2023.03", 10.5, HUI, 1, 3.36)])]),
    ]
    return {"n": -1, "shapes": shapes, "clicks": [["a5"], ["a6"]]}

def _slide_b():
    """新 P12 · 0.29TB 四步推演：四节点横排分步 → 大数落地。口径同 #03 essay。"""
    nodes = [
        ("b4", 120,  "一生听 10 亿词",   "口径 · ILYA，GTC 2023",            0),
        ("b5", 553,  "→ 只有 25% 值得记", "筛出 2.5 亿词 · 寒暄重复噪声出局", 1),
        ("b6", 986,  "→ 折成 3.2 年音频", "÷ 150 词/分钟 ≈ 167 万分钟",      2),
        ("b7", 1419, "→ 装进 0.29 TB",   "语音 25 KBPS ≈ 295 GB",           3),
    ]
    shapes = [
        _tx("b2", 120, 144, 1730, 34, [_p([("THE BACK-OF-THE-ENVELOPE · 1B WORDS → 0.29 TB", 15.0, ZI, 1, 6.4)])]),
        _tx("b3", 120, 192, 1730, 146, [_p([("一道", 45.0, W, 1, -0.6), ("「 四步 」", 45.0, ZI, 1, -0.6),
                                            ("算术题。", 45.0, W, 1, -0.6)], ln=1.18)]),
    ]
    for sid, x, tt, sub, _ in nodes:
        zi_head = tt.split(" ", 1)[0] if tt.startswith("→") else None
        runs = ([("→ ", 27.0, ZI, 1, 0), (tt[2:], 27.0, W, 1, 0)] if zi_head else [(tt, 27.0, W, 1, 0)])
        shapes.append(_tx(sid, x, 420, 392, 200, [_p(runs, ln=1.3),
                                                  _p([(sub, 11.5, HUI, 1, 2.4)], ln=1.5, bef=16)]))
    shapes += [
        _tx("b8", 120, 660, 1730, 170, [_p([("0.29 ", 105.0, ZI, 1, -5.6), ("TB", 36.0, W, 1, -5.6)], ln=0.9, algn="ctr")]),
        _tx("b9", 120, 852, 1730, 44, [_p([("一个人一生中，真正值得被保存的「生命上下文」——上限就在这里。", 20.0, W, 1, 0)], algn="ctr")]),
        _tx("b10", 120, 972, 1680, 26, [_p([("口径 · 思想实验 · 详见 #03《我们的一生只有 0.29TB》· 均为数量级估算", 10.5, HUI, 1, 3.36)])]),
    ]
    return {"n": -1, "shapes": shapes, "clicks": [["b5"], ["b6"], ["b7", "b8", "b9"]]}

def apply_r24(model):
    sls = model["slides"]
    assert sls[10]["n"] == 11 and sls[32]["n"] == 33, "R24 前置页序不对"
    p11 = sls[10]
    keep = {str(s["id"]): s for s in p11["shapes"]}
    # 新 P13 = FIG 01 整页：左侧卡原几何（4/5/6），右侧伙伴线读数（c7）+ TAKEAWAY（11/12/13 右移）
    c7 = _tx("c7", 1160, 430, 640, 200, [_p([("一台机器人能成为「伙伴」的", 24.0, W, 1, 0)], ln=1.5),
                                         _p([("记忆配额上限 —— 也是 ", 24.0, W, 1, 0), ("0.29 TB", 24.0, ZI, 1, 0),
                                             ("。", 24.0, W, 1, 0)], ln=1.5)])
    for sid, dx, dy in (("11", 31, -184), ("12", 31, -184), ("13", 31, -184)):  # 原块在 x≈1129，右移 31 上提 184
        sh = keep[sid]
        sh["x"] += dx
        sh["y"] += dy
    slide_c = {"n": -1,
               "shapes": [keep["2"], keep["3"], keep["4"], keep["5"], keep["6"], c7, keep["11"], keep["12"], keep["13"]],
               "clicks": [["4", "5", "6"], ["c7"], ["13", "12", "11"]]}
    # 老 P13 严谨化（此时仍是原编号 13 → 列表下标 12）
    for sh in sls[12]["shapes"]:
        for p in sh.get("paras", []):
            for r in p.get("runs", []):
                if r.get("t") == "2024 →":
                    r["t"] = "2022 →"
                if r.get("t") == "ChatGPT · GPT-4o":
                    r["t"] = "ChatGPT → GPT-4o"
    # 重组：P11 → A/B/C；删老 P33
    new = sls[:10] + [_slide_a(), _slide_b(), slide_c] + sls[11:32] + sls[33:]
    for i, sl in enumerate(new, 1):
        sl["n"] = i
    assert len(new) == 37, "R24 后应为 37 页，实际 %d" % len(new)
    model["slides"] = new
# 底流场：8 条横贯画面的贝塞尔曲线，分 3 组各自 sway；与 cowork-confv2 同一实现
FLOW_SVG = """<svg class="deck-flow" viewBox="0 0 1920 1080" preserveAspectRatio="none" aria-hidden="true">
  <g>
    <path class="l1 s1" stroke-width="1.6" d="M-200 250 C 260 120, 520 400, 900 260 S 1560 90, 2120 240"/>
    <path class="l2 s2" stroke-width="1.2" d="M-200 340 C 300 220, 620 500, 980 350 S 1600 200, 2120 330"/>
    <path class="l2 s3" stroke-width="1"   d="M-200 160 C 340 60, 700 300, 1060 150 S 1660 20, 2120 140"/>
  </g>
  <g>
    <path class="l1 s2" stroke-width="1.4" d="M-200 700 C 300 580, 640 860, 1020 720 S 1640 560, 2120 690"/>
    <path class="l2 s4" stroke-width="1.1" d="M-200 800 C 260 700, 600 960, 1000 820 S 1620 670, 2120 790"/>
    <path class="l2 s1" stroke-width="1"   d="M-200 610 C 380 500, 720 780, 1100 620 S 1700 470, 2120 600"/>
  </g>
  <g>
    <path class="l2 s3" stroke-width=".9"  d="M-200 980 C 320 880, 680 1120, 1080 980 S 1680 840, 2120 960"/>
    <path class="l1 s4" stroke-width="1.1" d="M-200 470 C 340 380, 660 640, 1040 500 S 1660 360, 2120 470"/>
  </g>
</svg>"""

# R28：栏线网格 + 上下导轨从 FLOW_SVG 常量拆出——skill 新规只退役流场曲线，这三件照挂
STAGE_CHROME = """<div class="deck-grid" aria-hidden="true"></div>
<div class="deck-rail t" aria-hidden="true"></div>
<div class="deck-rail b" aria-hidden="true"></div>"""

# ── 资产映射 ────────────────────────────────────────────────────────────────
ASSET = {
    # R22 已删：image3.png（RTE 2026 春夏巡游角标）/ image4.png（人人都是产品经理 + 起点课堂双 logo 条）
    #          —— 两个资产文件同步从 public/decks/assets/robot26/ 移除，全场零残留。
    # R23 已删：image5.jpeg（cover-ai.jpg 峰会 keyart 满幅背景）—— P1/P36 换 colin-deck 背景板，
    #          shape 在 build_slide 里跳过，资产文件同步移除。
    "image10.png": A + "robot-face.webp",
    "image11.png": A + "cat-day30.webp",
    "image12.png": A + "cat-day1.webp",
    "image13.png": A + "cat-day365.webp",
    "image15.jpeg": A + "first-principles.jpg",
    "image17.png": A + "era-now.webp",
    "image18.png": A + "era-2024.webp",
    "image19.png": A + "era-2010s.webp",
    "image20.png": A + "era-1990s.webp",
    "image24.png": A + "comfort-faces.webp",
    "image27.png": A + "demo-poster.jpg",
    "image38.png": A + "r1-wifi.webp",
    "image39.png": A + "r1-4g.webp",
    "image40.png": A + "openai-agora.webp",
    "image41.png": A + "living-room.webp",
    "image42.jpeg": A + "qr-wechat.jpg",
    "image43.jpeg": A + "qr-xiaohongshu.jpg",   # R27.1b：查明实为 Colin 小红书名片卡（原名 qr-rte 是误标）
}
SKIP_IMG = {"image16.png"}   # 整张 alpha=0 的空图，PowerPoint 里也是不可见的

# ── R26 · 浅色资产映射（交付包 robot26-light-optimized · 2026-08-11）─────────
# 11 张黑底线稿的浅色版：透明底 + #0d0d0d 深线 + #f45b8c 玫红强调；
# P33 合作图为完整重建（两个 wordmark 转深色，无黑色画布）。像素级翻色，尺寸与原图逐对一致。
ASSET_LIGHT = {
    "image10.png": A + "robot-face-light.png",
    "image11.png": A + "cat-day30-light.png",
    "image12.png": A + "cat-day1-light.png",
    "image13.png": A + "cat-day365-light.png",
    "image17.png": A + "era-now-light.png",
    "image18.png": A + "era-2024-light.png",
    "image19.png": A + "era-2010s-light.png",
    "image20.png": A + "era-1990s-light.png",
    "image24.png": A + "comfort-faces-light.png",
    "image40.png": A + "openai-agora-light.png",
    "image41.png": A + "living-room-light.png",
}

# ── 图表重画（原生 SVG，零截图）─────────────────────────────────────────────
# 环形图：(边长, 内半径, 外半径, 轨道色, 弧色, 百分比)
DONUT = {
    "image6.png":  (960, 360, 464, "#101010", "#D4B7F9", 0.21),
    "image7.png":  (960, 360, 465, "#101010", "#D4B7F9", 0.45),
    "image21.png": (560, 210, 271, "#E6EFEC", "#944AF0", 0.07),
    "image22.png": (760, 285, 368, "#E6EFEC", "#D4B7F9", 0.38),
    "image23.png": (960, 360, 465, "#E6EFEC", "#D4B7F9", 0.55),
}
SPARK = {   # 迷你留存曲线：(viewBox, path, 颜色)
    "image8.png": ("0 0 160 72", "M2 7.5 H40 V63.5 H158", "#999999"),
    "image9.png": ("0 0 160 72",
                   "M2 59.5 C 20 52, 34 34, 55 26.5 S 88 30, 109 31 S 140 20, 158 11.5", "#D3B7F9"),
}
ARROW = {   # 小箭头：(viewBox, path, 颜色, 线宽, 实测路径长)
    "image25.png": ("0 0 80 44", "M40 40 V8 M28 20 L40 7 L52 20", "#B78CF0", 5, 68),
    "image26.png": ("0 0 160 80", "M6 40 H150 M132 24 L152 40 L132 56", "#D4B7F9", 5, 196),
}


def donut_svg(name, w, h, cls, i, step):
    side, r0, r1, track, arc, pct = DONUT[name]
    r = (r0 + r1) / 2.0
    sw = r1 - r0
    c = 2 * math.pi * r
    dash = c * pct
    return (
        f'<svg viewBox="0 0 {side} {side}" width="{w:.1f}" height="{h:.1f}" aria-hidden="true">'
        f'<circle cx="{side/2}" cy="{side/2}" r="{r:.1f}" fill="none" stroke="{track}" stroke-width="{sw:.1f}"/>'
        f'<circle class="dwa" style="--len:{dash:.1f};--rest:{c:.1f};--i:{i}" cx="{side/2}" cy="{side/2}" r="{r:.1f}"'
        f' fill="none" stroke="{arc}" stroke-width="{sw:.1f}" stroke-linecap="butt"'
        f' transform="rotate(-90 {side/2} {side/2})"/></svg>')


def spark_svg(name, w, h, i):
    vb, d, col = SPARK[name]
    ln = 212 if name == "image8.png" else 172       # 实测 getTotalLength()
    return (f'<svg viewBox="{vb}" width="{w:.1f}" height="{h:.1f}" aria-hidden="true">'
            f'<path class="dw" style="--len:{ln};--i:{i}" d="{d}" fill="none" stroke="{col}"'
            f' stroke-width="4.5" stroke-linecap="square" stroke-linejoin="miter"/></svg>')


def arrow_svg(name, w, h, i):
    vb, d, col, sw, ln = ARROW[name]
    return (f'<svg viewBox="{vb}" width="{w:.1f}" height="{h:.1f}" aria-hidden="true">'
            f'<path class="dw" style="--len:{ln};--i:{i}" d="{d}" fill="none" stroke="{col}"'
            f' stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def fig01_svg(w, h, i):
    """P11 · FIG 01 · RELATIONSHIP DEPTH × MEMORY CAPACITY —— 原生重画，不贴图。
       Y：工具 / 熟人 / 朋友 / 伙伴；X：对数轴，四个锚点 0.000 / 0.001 / 0.01 / 0.29TB。"""
    L, R, T, B = 190, 1430, 88, 772          # 绘图区（viewBox 1782×1025 下的坐标）
    ys = {"工具": 757, "熟人": 601, "朋友": 429, "伙伴": 257}
    s = [f'<svg viewBox="0 0 1782 1025" width="{w:.1f}" height="{h:.1f}" aria-hidden="true" class="fig01">']
    # 网格
    for k, y in ys.items():
        if k != "工具":
            s.append(f'<line x1="{L}" y1="{y}" x2="{R}" y2="{y}" stroke="#E4E4E8" stroke-width="2" stroke-dasharray="7 9"/>')
        s.append(f'<text x="{L-32}" y="{y+16}" text-anchor="end" class="ax">{k}</text>')
    # 轴
    s.append(f'<path class="dw" style="--len:1954;--i:{i}" d="M{L} {T} V{B} H{R+30}" fill="none" stroke="#2E2E33" stroke-width="4"/>')
    s.append(f'<text x="{R+42}" y="{B+8}" class="axm">log</text>')
    # 曲线
    d = f"M282 {B-5} C 420 748, 560 726, 700 694 S 940 596, 1070 470 S 1210 296, 1232 {ys['伙伴']-2}"
    s.append(f'<path class="dw" style="--len:1135;--i:{i+1}" d="{d}" fill="none" stroke="#D4B7F9" stroke-width="9" stroke-linecap="round"/>')
    # 数据点
    for cx, cy, col, r in [(282, B - 5, "#7C7C82", 15), (452, 738, "#7C7C82", 15), (730, 688, "#0D0D0D", 17)]:
        s.append(f'<circle class="pop" style="--i:{i+2}" cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>')
    # 伙伴线 + 目标点
    s.append(f'<line class="dw" style="--len:660;--i:{i+3}" x1="1232" y1="112" x2="1232" y2="{B}" stroke="#944AF0" stroke-width="4" stroke-dasharray="12 10"/>')
    s.append(f'<text x="1256" y="130" class="axp">伙伴线</text>')
    s.append(f'<g class="pop" style="--i:{i+4}"><circle cx="1232" cy="{ys["伙伴"]-2}" r="52" fill="#D4B7F9" opacity=".16"/>'
             f'<circle cx="1232" cy="{ys["伙伴"]-2}" r="38" fill="none" stroke="#D4B7F9" stroke-width="2" opacity=".55"/>'
             f'<circle cx="1232" cy="{ys["伙伴"]-2}" r="26" fill="#C9A9F7"/></g>')
    # X 轴刻度文字
    # R24：前两枚刻度文字原稿互压（280/452 中锚半径重叠），左右各让 28px 错开
    for x, t, cls in [(252, "Siri · 0.000", "axm"), (490, "普通玩具 · 0.001", "axm"),
                      (730, "主流 AI 玩具 · 0.01", "axm"), (1232, "目标 · 0.29 TB", "axp2")]:
        s.append(f'<text x="{x}" y="{B+75}" text-anchor="middle" class="{cls}">{t}</text>')
    s.append("</svg>")
    return "".join(s)


# ── 文本 ────────────────────────────────────────────────────────────────────
def bold_of(run):
    if run.get("b"):
        return True
    f = run.get("f") or ""
    return "Bold" in f or "Heavy" in f or "Black" in f


CJK = re.compile(r"[⺀-鿿豈-﫿＀-｠￠-￦]")
MONO_PARA = re.compile(r"^\s*钉子\s*·\s*PIN")   # 角标：PPT 里 P33 是 Courier、其余是 Arial，不齐


# 来源行 / 出处角标 —— 纯拉丁的小字注脚，PPT 里写成 Arial，收进 mono 与 eyebrow 同族。
# （Colin R22 点名的「CONSUMER ROBOTS, 2025」就是第一条）
MONO_SID = {(2, "28"), (3, "10"), (6, "46"), (7, "4"), (19, "5"), (23, "31"), (32, "49"),
            (11, "a7"), (12, "b10")}  # R24 顺延 + 新增两条来源行（Ilya 引文页 / 0.29TB 口径行）


def fam_of(run, sz_px, para_txt="", key=None):
    """R22 · mono 统一 —— 只收 chrome 那一族，正文与大标题一律不碰。
       PPT 原稿把角标/注脚一半写成 Courier New（P33/P35），一半写成 Arial（其余 30 页），
       同一族标签两种字，是原稿自己的不一致；统一收进 --f-mono，
       顺带把 eyebrow 对齐 Colin 家 deck 的 chrome 语言。
       三条判据：① 原稿就是 Courier ② 字距 ≥ 5.5px 的拉字距标签（eyebrow / MQ / PIN）
                ③ MONO_SID 点名的来源行。"""
    f = run.get("f") or ""
    if "Courier" in f:
        return "var(--f-mono)"
    t = run.get("t") or ""
    if not t.strip():
        return None
    if MONO_PARA.match(para_txt):
        return "var(--f-mono)"
    if CJK.search(t):
        return None
    if key in MONO_SID:
        return "var(--f-mono)"
    if (run.get("spc") or 0) >= 5.5 and sz_px <= 24.5:
        return "var(--f-mono)"
    return None    # 默认继承 --f-cn


def esc(t):
    return html.escape(t).replace("  ", " &#160;")


def render_text(sh, scale, key=None):
    """把 shape 的段落/run 渲染成 HTML。scale = normAutofit fontScale。"""
    body = sh.get("body") or {}
    lsr = body.get("lsr", 0.0)
    out = []
    for p in sh.get("paras", []):
        st = []
        algn = p.get("algn")
        if algn in ("ctr", "r", "just"):
            st.append("text-align:" + {"ctr": "center", "r": "right", "just": "justify"}[algn])
        ln = p.get("ln")
        if ln:
            st.append("line-height:%.3f" % max(0.7, (ln - lsr) * LH))
        elif lsr:
            st.append("line-height:%.3f" % max(0.7, (1 - lsr) * LH))
        if p.get("bef"):
            st.append("margin-top:%.1fpx" % p["bef"])
        if p.get("aft"):
            st.append("margin-bottom:%.1fpx" % p["aft"])
        if p.get("marL"):
            st.append("padding-left:%.1fpx" % p["marL"])
        ptxt = "".join(r.get("t", "") for r in p.get("runs", []))
        runs = [r for r in p.get("runs", []) if r.get("br") or (r.get("t", "") != "")]
        inner = []
        for ri, r in enumerate(runs):
            if r.get("br"):
                inner.append("<br>")
                continue
            t = r.get("t", "")
            cs = []
            sz = (r.get("sz") or DEF_SZ) * PT * scale
            cs.append("font-size:%.1fpx" % sz)
            cs.append("font-weight:%d" % (700 if bold_of(r) else 400))
            cs.append("color:" + (r.get("c") or "#000000"))
            if r.get("i"):
                cs.append("font-style:italic")
            deco = []
            if r.get("u"):
                deco.append("underline")
            if r.get("s"):
                deco.append("line-through")
            if deco:
                cs.append("text-decoration:" + " ".join(deco))
            if r.get("spc"):
                spc = r["spc"] * scale
                cs.append("letter-spacing:%.2fpx" % spc)
                # R22 · 尾字距回收（conf 家族当年的 padding-right:.06em 同一个病）：
                # CSS 的 letter-spacing 会在**最后一个字之后**也补一个字距，这一格空白
                # 计进行盒宽度 —— 于是「刚好放得下」的标签被挤到换行、居中的标签左偏半格。
                # 行尾 run 用等量负 margin 把它收回来，字形不动、位置不动，只还回那一格。
                if ri == len(runs) - 1 and not t.endswith(" "):
                    cs.append("margin-right:%.2fpx" % (-spc))
            fam = fam_of(r, sz, ptxt, key)
            if fam:
                cs.append("font-family:" + fam)
            inner.append('<span style="%s">%s</span>' % (";".join(cs), esc(t)))
        if not inner:
            inner.append("<br>")
        out.append('<p%s>%s</p>' % ((' style="%s"' % ";".join(st)) if st else "", "".join(inner)))
    return "".join(out)


def maxsz(sh):
    m = 0
    for p in sh.get("paras", []):
        for r in p.get("runs", []):
            m = max(m, r.get("sz") or DEF_SZ)
    return m


def has_text(sh):
    for p in sh.get("paras", []):
        for r in p.get("runs", []):
            if (r.get("t") or "").strip():
                return True
    return False


def is_rule(sh):
    """PPT 里当分隔线 / 下划线 / 强调条用的细长矩形 → 映射成 SVG 画线。"""
    if sh["kind"] != "sp" or has_text(sh):
        return False
    if sh.get("geom") not in ("rect", None):
        return False
    f = sh.get("fill")
    if not isinstance(f, str):
        return False
    w, h = sh.get("w", 0), sh.get("h", 0)
    return (h <= 8 and w >= 40) or (w <= 8 and h >= 40)


def role_of(sh):
    if is_rule(sh):
        return "rule"
    if sh["kind"] == "pic":
        return "pop"
    fill = sh.get("fill")
    txt = has_text(sh)
    w, h = sh.get("w", 0), sh.get("h", 0)
    if sh.get("geom") == "ellipse":
        return "pop"
    if fill is not None and w >= 200 and h >= 80:
        return "rise"
    if not txt:
        return "pop"
    ms = maxsz(sh)
    if ms >= 78:
        return "settle"
    if ms >= 40 and w >= 640:
        return "ink"
    if ms >= 40:
        return "settle"
    return "flow"


# ── shape → HTML ────────────────────────────────────────────────────────────
def geom_css(sh):
    css = []
    g = sh.get("geom")
    if g == "ellipse":
        css.append("border-radius:50%")
    elif g == "roundRect":
        css.append("border-radius:%.1fpx" % (min(sh.get("w", 0), sh.get("h", 0)) * 0.16))
    f = sh.get("fill")
    if isinstance(f, str):
        css.append("background:" + f)
    elif isinstance(f, dict) and f.get("grad"):
        stops = ",".join("%s %.1f%%" % (c, p) for p, c in f["grad"])
        css.append("background:linear-gradient(%.0fdeg,%s)" % (f.get("ang", 0) + 90, stops))
    l = sh.get("line")
    if l:
        css.append("border:%.2fpx %s %s" % (max(0.75, l["w"]), l.get("dash", "solid") and
                                            ("dashed" if l.get("dash", "").startswith("dash") else "solid"), l["c"]))
    if sh.get("rot"):
        css.append("transform:rotate(%.2fdeg)" % sh["rot"])
    return css


def shape_html(sh, step, i, sn):
    w, h = sh.get("w", 0), sh.get("h", 0)
    x, y = sh.get("x", 0), sh.get("y", 0)
    role = role_of(sh)
    # R22 · 裁字修复：只放宽框，不动字号；按段落对齐方向反向放开，视觉锚点保持原位
    d = WIDEN.get((sn, str(sh["id"])))
    if d:
        algn = (sh.get("paras") or [{}])[0].get("algn")
        if algn == "r":
            x, w = x - d, w + d
        elif algn == "ctr":
            x, w = x - d / 2.0, w + d
        else:
            w = w + d
    base = ["left:%.1fpx" % x, "top:%.1fpx" % y, "width:%.1fpx" % w, "height:%.1fpx" % h]
    attr = ""
    if step:
        attr += ' data-step="%d"' % step

    # ① 细长矩形 → SVG 画线
    if role == "rule":
        col = sh["fill"]
        if w >= h:
            d, ln, sw = "M0 %.2f H%.2f" % (h / 2, w), w, h
        else:
            d, ln, sw = "M%.2f 0 V%.2f" % (w / 2, h), h, w
        svg = ('<svg width="%.1f" height="%.1f" viewBox="0 0 %.2f %.2f" aria-hidden="true">'
               '<path class="dw" style="--len:%.1f;--i:%d" d="%s" stroke="%s" stroke-width="%.2f" fill="none"/></svg>'
               % (w, h, w, h, ln, i, d, col, sw))
        return '<div class="sh rule"%s style="%s">%s</div>' % (attr, ";".join(base), svg)

    # ② 图片
    if sh["kind"] == "pic":
        img = sh.get("img")
        if img in SKIP_IMG:
            return ""
        cls = "sh pop"
        if img in DONUT:
            return '<div class="sh"%s style="%s">%s</div>' % (attr, ";".join(base), donut_svg(img, w, h, cls, i, step))
        if img in SPARK:
            return '<div class="sh"%s style="%s">%s</div>' % (attr, ";".join(base), spark_svg(img, w, h, i))
        if img in ARROW:
            return '<div class="sh"%s style="%s">%s</div>' % (attr, ";".join(base), arrow_svg(img, w, h, i))
        if img == "image14.png":
            return '<div class="sh"%s style="%s">%s</div>' % (attr, ";".join(base), fig01_svg(w, h, i))
        if img in ICONS:
            return ('<div class="%s"%s style="%s;--i:%d"><img src="%s" alt=""></div>'
                    % (cls, attr, ";".join(base), i, ICONS[img]))
        src = ASSET.get(img)
        if not src:
            return ""
        # 视频页（老 P22 → R24 起 P24）：PPT 里这张图就是 media1.mp4 的封面帧，单击播放
        if sn == 24:
            return ('<div class="sh vid"%s style="%s;--i:%d">'
                    '<video data-play-step="1" src="%sdemo.mp4" poster="%s" preload="none" playsinline'
                    ' muted controls></video></div>' % (attr, ";".join(base), i, A, src))
        # R26：浅色资产双源（默认 src=暗版；主题切换脚本按 data-*-src 同步）
        light_src = ASSET_LIGHT.get(img)
        theme_attr = (' data-dark-src="%s" data-light-src="%s"' % (src, light_src)) if light_src else ""
        return '<div class="%s"%s style="%s;--i:%d"><img src="%s"%s alt=""></div>' % (cls, attr, ";".join(base), i, src, theme_attr)

    # ③ 普通形状 / 文本框
    css = base + geom_css(sh)
    body = sh.get("body") or {}
    if has_text(sh):
        ins = body.get("ins", [2.67, 2.67, 2.67, 2.67])
        css.append("padding:%.2fpx %.2fpx %.2fpx %.2fpx" % (ins[1], ins[2], ins[3], ins[0]))
        anc = body.get("anchor", "t")
        css.append("justify-content:" + {"t": "flex-start", "ctr": "center", "b": "flex-end"}.get(anc, "flex-start"))
        if body.get("wrap") == "none":
            css.append("white-space:nowrap")
        k = body.get("fs", 1.0) * float(FIT.get("%d:%s" % (sn, sh["id"]), 1.0))
        inner = render_text(sh, k, (sn, str(sh["id"])))
        cls = "sh tx " + role
    else:
        inner = ""
        cls = "sh " + role
    af = ' data-af="1"' if (body.get("af") and has_text(sh)) else ""
    return '<div class="%s" data-sid="%s"%s%s style="%s;--i:%d">%s</div>' % (
        cls, sh["id"], af, attr, ";".join(css), i, inner)


# ── 每页组装 ────────────────────────────────────────────────────────────────
def stagger(n):
    """组内 n 个元素 → --i 序列，压到 0..MAX_I，保证 2.4s 内全部落位。"""
    if n <= 1:
        return [0]
    k = min(1.0, float(MAX_I) / (n - 1))
    return [int(round(j * k)) for j in range(n)]


def build_slide(sl):
    n = sl["n"]
    # R23：封面两页跳过峰会满幅 keyart（背景板交给 stage 模板层）
    shapes = [s for s in sl["shapes"]
              if not (n in COVER_BG_DROP and s.get("img") == "image5.jpeg")]
    groups = [g for g in sl["clicks"] if g]
    step_of, idx_of = {}, {}
    for gi, ids in enumerate(groups, 1):
        st = stagger(len(ids))
        for j, sid in enumerate(ids):
            step_of[sid] = gi
            idx_of[sid] = st[j]
    # 无动画的 shape：按 z-order 错峰，随页面入场
    free = [s["id"] for s in shapes if s["id"] not in step_of]
    fst = stagger(len(free))
    for j, sid in enumerate(free):
        idx_of[sid] = fst[j]

    parts = []
    for sh in shapes:
        parts.append(shape_html(sh, step_of.get(sh["id"], 0), idx_of.get(sh["id"], 0), n))
    # R22：版式角标（会场双 logo 条 34 页 + P22 的 RTE 巡游角标）整条撤掉。
    #      R27：右上角落款（colinyao.com）退役，全 37 页改挂连续页码；
    #      总数由 slide count 派生，不硬写；NO_SIG 满幅页豁免惯例随之退役
    #      （.sig 自带 z-index:2，压得住 P24 满幅视频与封面元素）。
    parts.insert(0, '<div class="sig">%d/%d</div>' % (n, len(MODEL["slides"])))
    maxstep = len(groups) + (1 if n == 24 else 0)  # R24：视频页顺延 22→24
    # R28：每页挂一张 CONF 背景板（.pp 之前 · z0；.pp z1 压其上）
    html = ('<section class="slide conf-boarded" data-p="%d" data-steps="%d">\n'
            '  <div class="conf-bg conf-bg-%s" aria-hidden="true"></div>\n'
            '  <div class="pp">%s</div>\n</section>'
            % (n, maxstep, _conf_board(n), "".join(p for p in parts if p)))
    if n in COVER_BG_DROP:
        # R23：黑底上黑字不可读，两页 #000000 全部翻主题变量（其余颜色原样，淡紫 accent 留任）
        html = html.replace("color:#000000", "color:var(--ink)")
    return html


# ── 骨架 ────────────────────────────────────────────────────────────────────
FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>"""

CSS = r"""<style>
/* ===========================================================
   robot26 · 北京站原稿还原 · R22 换 Colin 暗色模板
   排版 / 字号 / 配色 token 仍取自 PPT 自己的稿子（一比一）：
   近黑 #000000 底 · 淡紫 #D4B7F9 主强调 · 深紫 #944AF0 次强调
   · 卡片白 #FFFFFE / 深卡 #1F1D2B / 分隔 #2A2A2A / 灰阶 #D9D9D9 #A6A6A6 #5B5B5B
   —— R22 只换「模板层」（页面 chrome + 底色质感），排版 / 图片 / 动效 / 字号一律不动：
   ① 会场双 logo 条（34 页）与 P22 的巡游场次角标整条撤掉（QA 全场 grep 零残留）
   ② 底色体系换成 colin-deck-dark 的做法：黑底 + 底流场（8 条贝塞尔漂移）
      + 240px 极细栏线网格 + 上下发丝导轨；slide 背景改 transparent 让流场透出来
      （底色数值仍是纯黑 —— 全部 PPT 位图都带烘死的黑底，抬亮底色会露出矩形接缝）
   ③ 右上角原 logo 槽换成 Colin 自己的 mono 落款
   =========================================================== */
:root{
  /* PPT 原稿是「Calibri/Arial 拉丁 + Source Han Sans CN 中文」的混排；
     这里按同一分工映射到自托管/系统栈：拉丁走 SF/Helvetica/Arial，中文走 PingFang/思源。
     R22：小号带字距的拉丁标签（eyebrow / 角标 / PIN / 来源行）统一收进 mono ——
     PPT 原稿里这一族一半 Courier 一半 Arial，本来就不齐，顺手对齐 Colin 家的 chrome 语言 */
  --f-cn:-apple-system,'Helvetica Neue',Arial,'PingFang SC','Noto Sans CJK SC','Source Han Sans SC','MiSans','HarmonyOS Sans SC','Microsoft YaHei',sans-serif;
  --f-mono:'JetBrains Mono','SF Mono',ui-monospace,'PingFang SC',monospace;
  /* R25 · conf 家族双主题：:root = conf-light（玫红系），html[data-theme="dark"] = conf-dark（淡紫系）。
     默认暗（deck 血统），左下角可切换；变量口径 = colin-deck conf-theme-dual.css。 */
  --stage-bg:#e2e3e8; --slide-bg:#eff0f3;
  --ink:#111111; --ink-3:#8e8e93; --amber:#f45b8c; --hair:rgba(17,17,17,.16);
  --card-bg-2:#fffffe;
  --ink-m:#6e6e73; --ink-soft:#7a7a83; --ink-2x:#3a3a3f;
  --acc-deep:#d8366a; --acc-2:#7b61ff; --amber-soft:#f9a8c6;
  --rule-line:#d8d8dc; --sig-ink:rgba(17,17,17,.30); --rail-line:rgba(17,17,17,.10);
  --void-0:#fffffe; --void-1:#fffffe; --void-2:#fffffe;   /* 黑页隐形垫板 → 浅底白卡 */
  --flow-line:rgba(244,91,140,.30);
  --flow-line-2:rgba(17,17,17,.13);
  --flow-op:.40;
  --grid-line:rgba(17,17,17,.05);
  --ease:cubic-bezier(.16,1,.3,1);
  --ease-flow:cubic-bezier(.22,.9,.24,1);
  --step:88ms;
}
html[data-theme="dark"]{
  --stage-bg:#000000; --slide-bg:#000000;
  --ink:#FFFFFF; --ink-3:#6f7186; --amber:#D4B7F9; --hair:rgba(255,255,255,.14);
  --card-bg-2:#131320;
  --ink-m:#A6A6A6; --ink-soft:#A7A9BE; --ink-2x:#D9D9D9;
  --acc-deep:#944AF0; --acc-2:#B78CF0; --amber-soft:#C9A9F7;
  --rule-line:#2A2A2A; --sig-ink:rgba(255,255,255,.30); --rail-line:rgba(255,255,255,.10);
  --void-0:#000000; --void-1:#0D0D0D; --void-2:#0A0A0A;   /* 暗底保持原稿近黑三档 */
  --flow-line:rgba(212,183,249,.30);
  --flow-line-2:rgba(255,255,255,.11);
  --flow-op:.42;
  --grid-line:rgba(255,255,255,.042);
}
/* R25 · svg 属性色跟主题（presentation attr 优先级低于 CSS，可直接覆写）*/
[stroke="#D4B7F9"]{stroke:var(--amber);} [fill="#D4B7F9"]{fill:var(--amber);}
[stroke="#D3B7F9"]{stroke:var(--amber);} [fill="#D3B7F9"]{fill:var(--amber);}
[stroke="#C9A9F7"]{stroke:var(--amber-soft);} [fill="#C9A9F7"]{fill:var(--amber-soft);}
[stroke="#944AF0"]{stroke:var(--acc-deep);} [fill="#944AF0"]{fill:var(--acc-deep);}
[stroke="#B78CF0"]{stroke:var(--acc-2);} [fill="#B78CF0"]{fill:var(--acc-2);}
[stroke="#2A2A2A"]{stroke:var(--rule-line);}
/* R25 · 浅底位图媒体卡：黑底烘死的位图在浅底上收成「暗媒体卡」——圆角 + 发丝描边，接缝变画框 */
html:not([data-theme="dark"]) .pp .sh>img{border-radius:10px;outline:1px solid var(--hair);outline-offset:-1px;}
html:not([data-theme="dark"]) .pp video{border-radius:10px;outline:1px solid var(--hair);outline-offset:-1px;}
/* R26 · 浅色资产：透明 PNG 不需要媒体卡画框；P24 视频影院卡
   （R26 的 P17 sid 级对比度修正随 R27 整页重排退役——新卡色在 .r27-face-card 里定死） */
html:not([data-theme="dark"]) .pp img[data-light-src]{border-radius:0!important;outline:0!important;background:transparent!important;}
/* 2026-08-13 Colin：P24 视频改全屏。两处修复：
   ① 根因——通用填充规则写的是 `.pp video`，robot26 段落是 .slide，从未命中，
     视频一直按素材原生 1280×720 裸渲染（≈2/3 舞台宽）；此处补命中的 P24 规则，
     16:9 同比 cover 满幅无裁切。
   ② R26 的浅色 1760×990 影院内框 + 18px 圆角随「全屏」指令退役（要回滚恢复上两行即可，见 git）。 */
section[data-p="24"] .sh.vid{left:0!important;top:0!important;width:1920px!important;height:1080px!important;}
section[data-p="24"] video{display:block;width:100%;height:100%;object-fit:cover;background:#000;border-radius:0;outline:0;}
html:not([data-theme="dark"]) section[data-p="24"] video{border-radius:0!important;outline:0!important;}
*{margin:0;padding:0;box-sizing:border-box;}

/* ---- 固定舞台（viewport-base，与全站 deck 同源）---- */
html,body{width:100%;height:100%;margin:0;overflow:hidden;background:var(--stage-bg);}
.deck-viewport{position:fixed;inset:0;overflow:hidden;background:var(--stage-bg);}
.deck-stage{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;transform-origin:0 0;background:var(--slide-bg);}
.slide{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;display:block;
  visibility:hidden;opacity:0;pointer-events:none;background:transparent;
  font-family:var(--f-cn);color:var(--ink);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;}
.slide.active,.slide.visible{visibility:visible;opacity:1;pointer-events:auto;z-index:1;}
img,video,canvas,svg{max-width:100%;max-height:100%;}

/* ---- R22 模板层 · 底流场（colin-deck-dark 同源实现）---- */
.deck-flow{position:absolute;inset:0;z-index:0;pointer-events:none;opacity:var(--flow-op);}
.deck-flow path{fill:none;stroke-linecap:round;stroke-dasharray:220 180;animation:drift linear infinite;}
.deck-flow .l1{stroke:var(--flow-line);}
.deck-flow .l2{stroke:var(--flow-line-2);}
.deck-flow .s1{animation-duration:38s;}
.deck-flow .s2{animation-duration:52s;}
.deck-flow .s3{animation-duration:64s;}
.deck-flow .s4{animation-duration:46s;}
.deck-flow g{animation:sway 26s ease-in-out infinite;}
.deck-flow g:nth-child(2){animation-duration:34s;animation-direction:reverse;}
.deck-flow g:nth-child(3){animation-duration:41s;}
@keyframes drift{0%{stroke-dashoffset:0;}100%{stroke-dashoffset:-1600;}}
@keyframes sway{0%,100%{transform:translate3d(0,0,0);}50%{transform:translate3d(-34px,14px,0);}}
/* ---- R22 模板层 · 240px 极细栏线网格 + 上下发丝导轨 ---- */
.deck-grid{position:absolute;inset:0;z-index:0;pointer-events:none;
  background:repeating-linear-gradient(90deg,transparent 0 120px,var(--grid-line) 120px 121px,transparent 121px 360px);
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 14%,#000 86%,transparent 100%);
          mask-image:linear-gradient(180deg,transparent 0,#000 14%,#000 86%,transparent 100%);}
.deck-rail{position:absolute;left:120px;right:120px;height:1px;z-index:0;pointer-events:none;
  background:linear-gradient(90deg,transparent,var(--rail-line) 18%,var(--rail-line) 82%,transparent);}
.deck-rail.t{top:32px;} .deck-rail.b{bottom:32px;}
/* ---- R22 模板层 · 右上角落款（原会场 logo 槽）---- */
.sig{position:absolute;right:120px;top:47px;z-index:2;
  font-family:var(--f-mono);font-size:15px;font-weight:400;line-height:1;
  letter-spacing:.24em;padding-right:.24em;color:var(--sig-ink);
  text-transform:uppercase;white-space:nowrap;pointer-events:none;}
@media print{
  .deck-flow,.deck-grid,.deck-rail{display:none!important;}
  html,body{width:1920px;height:auto;overflow:visible;background:#000;}
  .deck-viewport{position:static;overflow:visible;}
  .deck-stage{position:static;width:auto;height:auto;transform:none!important;}
  .slide{position:relative;display:block!important;visibility:visible!important;opacity:1!important;
    pointer-events:auto!important;width:1920px;height:1080px;break-after:page;page-break-after:always;filter:none!important;}
  .slide:last-child{break-after:auto;page-break-after:auto;}
  .deck-steps,.deck-progress,.deck-ruler,.edit-toggle,.edit-hotzone{display:none!important;}
  .flow,.rise,.spread,.settle,.pop,.ink,.dw,[data-step]{opacity:1!important;transform:none!important;
    filter:none!important;clip-path:none!important;-webkit-mask-image:none!important;mask-image:none!important;
    stroke-dashoffset:0!important;}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.2s!important;}
}

/* ---- PPT 绝对版面层 ---- */
.pp{position:absolute;inset:0;}
.pp .sh{position:absolute;overflow:visible;}
.pp .tx{display:flex;flex-direction:column;}
.pp .tx p{font-size:24px;line-height:1.22;color:#000;font-weight:400;letter-spacing:0;}
.pp img{display:block;width:100%;height:100%;object-fit:fill;}
.pp video{display:block;width:100%;height:100%;object-fit:cover;background:#000;}
.pp .mark{opacity:.92;}
.pp svg{overflow:visible;display:block;}
.fig01 .ax{font-family:var(--f-cn);font-size:36px;font-weight:700;fill:#3A3A40;}
.fig01 .axm{font-family:var(--f-mono);font-size:27px;fill:#5B5B5B;}
.fig01 .axp{font-family:var(--f-cn);font-size:30px;font-weight:700;fill:#944AF0;}
.fig01 .axp2{font-family:var(--f-mono);font-size:27px;font-weight:500;fill:#B78CF0;}

/* ---- 入场动效（站内 motion.css 同源；PPT 的 Dissolve In 按角色分配质感）---- */
.flow{opacity:0;transform:translate3d(-26px,10px,0);filter:blur(7px);clip-path:inset(0 100% 0 0);
  transition:opacity .82s var(--ease-flow) calc(var(--i,0)*var(--step)),
             transform .98s var(--ease-flow) calc(var(--i,0)*var(--step)),
             filter .74s var(--ease-flow) calc(var(--i,0)*var(--step)),
             clip-path 1.1s var(--ease-flow) calc(var(--i,0)*var(--step));}
.slide.visible .flow{opacity:1;transform:translate3d(0,0,0);filter:blur(0);clip-path:inset(-14px -20px);}
.rise{opacity:0;transform:translate3d(0,34px,0);clip-path:inset(100% 0 0 0);
  transition:opacity .8s var(--ease-flow) calc(var(--i,0)*var(--step)),
             transform 1.02s var(--ease-flow) calc(var(--i,0)*var(--step)),
             clip-path 1.06s var(--ease-flow) calc(var(--i,0)*var(--step));}
.slide.visible .rise{opacity:1;transform:translate3d(0,0,0);clip-path:inset(-14px -20px);}
.settle{opacity:0;transform:scale(1.09);filter:blur(16px);
  transition:opacity .82s var(--ease) calc(var(--i,0)*var(--step)),
             transform 1.1s var(--ease-flow) calc(var(--i,0)*var(--step)),
             filter .82s var(--ease) calc(var(--i,0)*var(--step));}
.slide.visible .settle{opacity:1;transform:scale(1);filter:blur(0);}
.ink{-webkit-mask-image:linear-gradient(96deg,#000 0%,#000 38%,rgba(0,0,0,.42) 54%,rgba(0,0,0,0) 74%);
  mask-image:linear-gradient(96deg,#000 0%,#000 38%,rgba(0,0,0,.42) 54%,rgba(0,0,0,0) 74%);
  -webkit-mask-size:300% 100%;mask-size:300% 100%;
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-position:128% 0;mask-position:128% 0;
  transition:-webkit-mask-position 1.35s var(--ease-flow) calc(var(--i,0)*var(--step)),
             mask-position 1.35s var(--ease-flow) calc(var(--i,0)*var(--step));}
.slide.visible .ink{-webkit-mask-position:0% 0;mask-position:0% 0;}
.pop{opacity:0;transform:translateY(12px) scale(.95);transform-origin:center;
  transition:opacity .66s var(--ease) calc(var(--i,0)*var(--step)),transform .76s var(--ease) calc(var(--i,0)*var(--step));}
.slide.visible .pop{opacity:1;transform:translateY(0) scale(1);}
.dw{stroke-dasharray:var(--len,1200);stroke-dashoffset:var(--len,1200);
  transition:stroke-dashoffset 1.6s var(--ease-flow) calc(var(--i,0)*var(--step));}
.slide.visible .dw{stroke-dashoffset:0;}
/* .dwa —— 环形弧「填进去」：dash = 弧长，gap = 整周长，保证起始态完全隐藏 */
.dwa{stroke-dasharray:var(--len,100) var(--rest,1000);stroke-dashoffset:var(--len,100);
  transition:stroke-dashoffset 1.6s var(--ease-flow) calc(var(--i,0)*var(--step));}
.slide.visible .dwa{stroke-dashoffset:0;}
/* 换页交叠 */
.slide{transition:opacity .5s var(--ease),filter .5s var(--ease),visibility 0s linear .5s;}
.slide.visible{transition:opacity .48s var(--ease),filter .48s var(--ease),visibility 0s;filter:none;}
.slide:not(.visible){filter:blur(14px);}

/* ---- 分步展开（data-step，与站内 build 机制同源）---- */
.slide.visible [data-step]:not(.on) .flow,.slide.visible .flow[data-step]:not(.on){
  opacity:0;transform:translate3d(-26px,10px,0);filter:blur(7px);clip-path:inset(0 100% 0 0);}
.slide.visible [data-step]:not(.on) .rise,.slide.visible .rise[data-step]:not(.on){
  opacity:0;transform:translate3d(0,34px,0);clip-path:inset(100% 0 0 0);}
.slide.visible [data-step]:not(.on) .settle,.slide.visible .settle[data-step]:not(.on){
  opacity:0;transform:scale(1.09);filter:blur(16px);}
.slide.visible [data-step]:not(.on) .pop,.slide.visible .pop[data-step]:not(.on){
  opacity:0;transform:translateY(12px) scale(.95);}
.slide.visible [data-step]:not(.on) .dw,.slide.visible .dw[data-step]:not(.on){stroke-dashoffset:var(--len,1200);}
.slide.visible [data-step]:not(.on) .dwa,.slide.visible .dwa[data-step]:not(.on){stroke-dashoffset:var(--len,100);}
.slide.visible [data-step]:not(.on) .ink,.slide.visible .ink[data-step]:not(.on){
  -webkit-mask-position:128% 0;mask-position:128% 0;}
.slide.visible [data-step]:not(.on):not(.flow):not(.rise):not(.settle):not(.pop):not(.dw):not(.ink){
  opacity:0;transition:opacity .66s var(--ease-flow);}
.slide.visible [data-step].on{opacity:1;}
/* 画线容器本身不参与整体淡入，只让线自己画 */
.slide.visible .sh.rule[data-step]:not(.on){opacity:1;}

/* ---- 舞台外 chrome ---- */
.deck-steps{position:fixed;right:26px;bottom:22px;z-index:1000;display:flex;gap:9px;align-items:center;opacity:0;transition:opacity .3s;}
.deck-steps.on{opacity:1;}
.deck-steps i{width:8px;height:8px;border-radius:50%;border:1px solid var(--ink-3);display:block;transition:all .3s var(--ease);}
.deck-steps i.done{background:var(--amber);border-color:var(--amber);}
.deck-steps b{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;color:var(--ink-3);
  text-transform:uppercase;font-weight:400;margin-right:4px;}
.deck-progress{position:fixed;left:0;bottom:0;height:2px;background:var(--amber);z-index:1000;transition:width .45s var(--ease);}
.edit-hotzone{position:fixed;top:0;left:0;width:80px;height:80px;z-index:10000;cursor:pointer;}
.edit-toggle{position:fixed;top:18px;left:18px;z-index:10001;opacity:0;pointer-events:none;
  transition:opacity .3s ease;background:var(--card-bg-2);color:var(--ink);border:1px solid var(--hair);
  border-radius:3px;padding:8px 12px;font-family:var(--f-mono);font-size:13px;cursor:pointer;}
.deck-swap{position:fixed;left:26px;bottom:24px;z-index:1100;font-family:var(--f-mono);font-size:12px;letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);border-radius:3px;padding:7px 12px;opacity:.5;transition:opacity .3s,color .3s,border-color .3s;background:transparent;cursor:pointer;}
.deck-swap:hover{opacity:1;color:var(--amber);border-color:var(--amber);}
@media print{.deck-swap{display:none!important;}}
.edit-toggle.show,.edit-toggle.active{opacity:1;pointer-events:auto;}
.edit-toggle.active{border-color:var(--amber);color:var(--amber);}
[contenteditable="true"]{outline:1px dashed rgba(212,183,249,.55);outline-offset:4px;}
</style>"""

RULER = r"""<style>
/* deck-ruler · 顶线即尺子（与全站 deck 同源） */
.deck-progress,#progress{display:none!important;}
.deck-ruler{position:fixed;top:0;left:0;right:0;height:20px;z-index:1200;cursor:pointer;}
.dr-track{position:absolute;top:0;left:0;right:0;height:2px;background:var(--hair);transition:height .25s ease;}
.dr-fill{position:absolute;top:0;left:0;height:2px;width:0;background:var(--amber);transition:width .45s cubic-bezier(.22,.9,.24,1),height .25s ease;}
.dr-teeth{position:absolute;top:0;left:0;right:0;height:7px;opacity:0;transition:opacity .25s ease;pointer-events:none;}
.dr-teeth i{position:absolute;top:0;width:1px;height:4px;background:var(--ink-3);opacity:.55;}
.dr-teeth i.maj{height:7px;opacity:.95;}
.deck-ruler:hover .dr-track,.deck-ruler:hover .dr-fill{height:6px;}
.deck-ruler:hover .dr-teeth{opacity:1;}
.dr-tip{position:absolute;top:13px;left:50%;transform:translateX(-50%);
  font-family:var(--f-mono);font-size:11px;line-height:1;letter-spacing:.1em;
  color:var(--ink);background:var(--card-bg-2);border:1px solid var(--hair);border-radius:2px;padding:5px 8px;
  opacity:0;transition:opacity .2s;white-space:nowrap;pointer-events:none;}
.deck-ruler:hover .dr-tip{opacity:1;}
@media print{.deck-ruler{display:none!important;}}
</style>
<div class="deck-ruler" id="deckRuler" aria-hidden="true"><div class="dr-track"></div><div class="dr-teeth"></div><div class="dr-fill"></div><div class="dr-tip">1</div></div>
<script>
(function(){
  var slides=document.querySelectorAll('.slide');var N=slides.length;if(!N)return;
  var ruler=document.getElementById('deckRuler'),fill=ruler.querySelector('.dr-fill'),
      tip=ruler.querySelector('.dr-tip'),teeth=ruler.querySelector('.dr-teeth');
  var step=Math.max(1,Math.ceil(N/96));
  for(var i=0;i<N;i+=step){var t=document.createElement('i');
    if((i/step)%5===0)t.className='maj';t.style.left=(((i+0.5)/N)*100)+'%';teeth.appendChild(t);}
  function cur(){for(var i=0;i<N;i++)if(slides[i].classList.contains('active'))return i;return 0;}
  function paint(){fill.style.width=(((cur()+1)/N)*100)+'%';}
  var mo=new MutationObserver(paint);
  slides.forEach(function(s){mo.observe(s,{attributes:true,attributeFilter:['class']});});
  paint();
  function target(e){var r=ruler.getBoundingClientRect();
    var x=(e.touches&&e.touches[0]?e.touches[0].clientX:e.clientX);
    var f=(x-r.left)/r.width;return Math.max(0,Math.min(N-1,Math.floor(f*N)));}
  function jump(n){
    if(window.deck&&typeof window.deck.go==='function'){window.deck.go(n);return;}
    var d=n-cur(),key=d>0?'ArrowRight':'ArrowLeft';
    for(var i=0;i<Math.abs(d);i++)document.dispatchEvent(new KeyboardEvent('keydown',{key:key,bubbles:true}));
  }
  var dragging=false;
  ruler.addEventListener('mousemove',function(e){var n=target(e);
    tip.textContent=(n+1)+' / '+N;tip.style.left=(((n+0.5)/N)*100)+'%';if(dragging)jump(n);});
  ruler.addEventListener('mousedown',function(e){dragging=true;jump(target(e));e.preventDefault();});
  addEventListener('mouseup',function(){dragging=false;});
  ruler.addEventListener('click',function(e){jump(target(e));});
  ruler.addEventListener('touchstart',function(e){jump(target(e));e.preventDefault();},{passive:false});
  ruler.addEventListener('touchmove',function(e){jump(target(e));e.preventDefault();},{passive:false});
  var buf='',bufT=null;
  document.addEventListener('keydown',function(e){
    if(e.target&&e.target.getAttribute&&e.target.getAttribute('contenteditable')==='true')return;
    if(e.key>='0'&&e.key<='9'){buf+=e.key;clearTimeout(bufT);bufT=setTimeout(function(){buf='';tip.style.opacity='';},1600);
      tip.textContent=buf+' / '+N;tip.style.left='50%';tip.style.opacity='1';}
    else if(e.key==='Enter'&&buf){var n=parseInt(buf,10);buf='';tip.style.opacity='';
      if(n>=1&&n<=N)jump(n-1);}
    else if(buf){buf='';tip.style.opacity='';}
  });
})();
</script>"""

JS = r"""<script>
/* ===========================================
   固定舞台演示控制器 —— 与全站 deck 同源（1920×1080 整体缩放 + 分步展开）
   =========================================== */
class SlidePresentation{
  constructor(){
    this.slides=[...document.querySelectorAll('.slide')];
    this.stage=document.getElementById('deckStage');
    this.progress=document.getElementById('deckProgress');
    this.stepsEl=document.getElementById('deckSteps');
    this.i=0;this.step=0;
    /* 分步数：优先取 data-steps（照搬 PPT 的单击次数），否则数 [data-step] */
    this.maxStep=this.slides.map(s=>{
      if(s.dataset.steps)return +s.dataset.steps;
      const els=[...s.querySelectorAll('[data-step]')];
      return els.length?Math.max(...els.map(e=>+e.dataset.step||0)):0;
    });
    this.setupScale();this.setupKeys();this.setupTouch();this.setupWheel();
    this.go(this.readHash(),true);
    window.addEventListener('hashchange',()=>this.go(this.readHash()));
  }
  readHash(){const n=parseInt((location.hash||'').replace('#',''),10);return isNaN(n)?0:n-1;}
  setupScale(){
    const scale=()=>{
      const f=Math.min(window.innerWidth/1920,window.innerHeight/1080);
      const x=(window.innerWidth-1920*f)/2, y=(window.innerHeight-1080*f)/2;
      this.stage.style.transform=`translate(${x}px, ${y}px) scale(${f})`;
    };
    scale();window.addEventListener('resize',scale);
  }
  setupKeys(){
    document.addEventListener('keydown',e=>{
      if(e.target.getAttribute&&e.target.getAttribute('contenteditable'))return;
      if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();this.next();}
      if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();this.prev();}
      if(e.key==='Home'){e.preventDefault();this.go(0);}
      if(e.key==='End'){e.preventDefault();this.go(this.slides.length-1);}
      if(e.key==='n'){e.preventDefault();this.go(this.i+1);}
      if(e.key==='p'){e.preventDefault();this.go(this.i-1);}
    });
  }
  setupTouch(){
    let x0=null,y0=null;
    document.addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
    document.addEventListener('touchend',e=>{
      if(x0===null)return;
      const dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0;
      if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)){dx<0?this.next():this.prev();}
      x0=null;y0=null;
    },{passive:true});
  }
  setupWheel(){
    let lock=false;
    document.addEventListener('wheel',e=>{
      if(lock)return;if(Math.abs(e.deltaY)<18)return;
      lock=true;setTimeout(()=>lock=false,700);
      e.deltaY>0?this.next():this.prev();
    },{passive:true});
  }
  next(){
    if(this.step<this.maxStep[this.i]){this.step++;this.applySteps();return;}
    this.go(this.i+1);
  }
  prev(){
    if(this.step>0){this.step--;this.applySteps();return;}
    this.go(this.i-1,false,true);
  }
  applySteps(){
    const cur=this.slides[this.i];
    cur.querySelectorAll('[data-step]').forEach(el=>{
      el.classList.toggle('on',(+el.dataset.step||0)<=this.step);
    });
    this.renderSteps();this.syncMedia();
  }
  renderSteps(){
    const max=this.maxStep[this.i];
    if(!max){this.stepsEl.classList.remove('on');this.stepsEl.innerHTML='';return;}
    let h='<b>build</b>';
    for(let k=1;k<=max;k++)h+=`<i class="${k<=this.step?'done':''}"></i>`;
    this.stepsEl.innerHTML=h;
    this.stepsEl.classList.add('on');
  }
  /* PPT 的 mediacall：P22 单击一次 = playFrom(0)；离页即停并归零 */
  syncMedia(){
    document.querySelectorAll('video[data-play-step]').forEach(v=>{
      const sec=v.closest('.slide');
      const live=sec.classList.contains('active')&&this.step>=(+v.dataset.playStep||1);
      if(live){const p=v.play();if(p&&p.catch)p.catch(()=>{});}
      else{try{v.pause();v.currentTime=0;}catch(e){}}
    });
  }
  go(n,init,toEnd){
    const target=Math.max(0,Math.min(n,this.slides.length-1));
    this.i=target;
    this.step=toEnd?this.maxStep[target]:0;
    this.slides.forEach((s,k)=>{
      const on=(k===this.i);
      s.classList.toggle('active',on);
      if(!on)s.classList.remove('visible');
    });
    const cur=this.slides[this.i];
    cur.querySelectorAll('[data-step]').forEach(el=>{
      el.classList.toggle('on',(+el.dataset.step||0)<=this.step);
    });
    void cur.offsetWidth;
    requestAnimationFrame(()=>requestAnimationFrame(()=>cur.classList.add('visible')));
    this.renderSteps();this.syncMedia();
    this.progress.style.width=((this.i+1)/this.slides.length*100)+'%';
    history.replaceState(null,'','#'+(this.i+1));
  }
}
const deck=new SlidePresentation();
window.deck=deck;

/* 就地编辑（E 键 / 左上角热区） */
const editor={
  isActive:false,
  toggle(){
    this.isActive=!this.isActive;
    const btn=document.getElementById('editToggle');
    btn.classList.toggle('active',this.isActive);
    if(this.isActive)btn.classList.add('show');
    document.querySelectorAll('.pp .tx p span').forEach(el=>el.setAttribute('contenteditable',this.isActive));
    if(!this.isActive)this.save();
  },
  save(){try{localStorage.setItem('deck-edits',document.getElementById('deckStage').innerHTML);}catch(e){}}
};
const hotzone=document.querySelector('.edit-hotzone');
const editToggle=document.getElementById('editToggle');
let hideT=null;
hotzone.addEventListener('mouseenter',()=>{clearTimeout(hideT);editToggle.classList.add('show');});
hotzone.addEventListener('mouseleave',()=>{hideT=setTimeout(()=>{if(!editor.isActive)editToggle.classList.remove('show');},400);});
editToggle.addEventListener('mouseenter',()=>clearTimeout(hideT));
editToggle.addEventListener('mouseleave',()=>{hideT=setTimeout(()=>{if(!editor.isActive)editToggle.classList.remove('show');},400);});
editToggle.addEventListener('click',()=>editor.toggle());
hotzone.addEventListener('click',()=>editor.toggle());
document.addEventListener('keydown',e=>{
  if((e.key==='e'||e.key==='E')&&!(e.target.getAttribute&&e.target.getAttribute('contenteditable'))){editor.toggle();}
  if(e.key==='s'&&(e.metaKey||e.ctrlKey)&&editor.isActive){e.preventDefault();editor.save();}
});

/* R25 · 深浅切换（colin-theme 全站共享偏好键） */
(function(){var b=document.getElementById('deckSwap');
  function apply(t){if(t==='light'){document.documentElement.removeAttribute('data-theme');b.textContent='暗底';}
    else{document.documentElement.setAttribute('data-theme','dark');b.textContent='浅底';}
    document.querySelectorAll('img[data-dark-src][data-light-src]').forEach(function(im){
      im.src = t==='light' ? im.dataset.lightSrc : im.dataset.darkSrc;});}
  var cur='dark';try{cur=localStorage.getItem('colin-theme')||'dark';}catch(e){}
  apply(cur);
  b.addEventListener('click',function(){cur=(cur==='dark')?'light':'dark';
    try{localStorage.setItem('colin-theme',cur);}catch(e){}apply(cur);});
})();
</script>"""


# ═══════════════════════════════════════════════════════════════════════════
# R27 · GPT 5.6 整体视觉优化合入（交付包 robot26-light-optimized/FABLE-R27-HANDOFF.md · 2026-08-11）
# 变换层原则不变：模型 json 保持 PPT 原样，本层在 build_slide 产物上整页替换 + 精确补丁。
# 与交付包 build-r27-preview.py 的差异（Fable review 修正，证据链见设计文档 R27 条目）：
#   · P11 speaker 归属改回官方口径——Jensen 问「Only one billion words?」，
#     「That's amazing. That's not a lot.」是 Ilya 自己的感叹（lifearchitect.ai 逐字稿
#     与现行 R24 版一致；NVIDIA 官方博客亦无 Jensen 说 That's amazing 的记载；
#     ytscribe ASR 无说话人标注，不构成反证）。交付包声称的「纠正」不成立，予以驳回。
#   · P11 删去无法核验的「38:22–38:36」时间码，改挂可核验的 on-demand 会话号
#   · P12 第 4 节点单位间距规范化：≈ 313 GB ≈ 0.29 TiB（交接文档自己的写法）
#   · P3 双环 --rest 改回 .dwa 惯例（--rest=整周长；交付包写成了余弧，机检 ④ 会拦）
#   · 资产一律走仓库相对路径（A 前缀）；浅色双源复用 R26 ASSET_LIGHT/apply(t)，
#     不移植交付包的 wire_light_assets / R27_JS / R26 重复 CSS（禁止重复造）
#   · 单行 mono 元素挂 data-sid（r3k/r4p/…），让 QA ⑪ 裁字机检继续覆盖新页
# ═══════════════════════════════════════════════════════════════════════════

R27_CSS = r"""<style id="robot26-r27">
/* R27 · full-deck dual-theme polish */
.sig{letter-spacing:.12em;padding-right:0;font-weight:500;color:var(--sig-ink);}
.r27-kicker{font:700 20px/1 var(--f-mono);letter-spacing:.28em;color:var(--amber);}
.r27-headline{font:700 68px/1.16 var(--f-cn);letter-spacing:-.02em;color:var(--ink);}
.r27-headline strong{color:var(--amber);}
.r27-card{background:var(--card-bg-2);border:1px solid var(--hair);border-radius:20px;}
.r27-label{font:700 17px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-m);}
.r27-note{font:400 22px/1.55 var(--f-cn);color:var(--ink-m);}
.r27-source{font:500 15px/1.35 var(--f-mono);letter-spacing:.08em;color:var(--ink-3);}
.r27-accent{color:var(--amber);}
.r27-hair{background:var(--hair);}

/* P24 · 影院视频面上的页码取反色（浅色主题的暗 ink 会沉进黑视频帧；Fable review 增补） */
html:not([data-theme="dark"]) section[data-p="24"] .sig{color:rgba(255,255,255,.42);}

/* Global light-theme cleanup: black PPT outlines become native conf-light hairlines. */
html:not([data-theme="dark"]) .pp .sh[style*="border:1.00px solid #0D0D0D"],
html:not([data-theme="dark"]) .pp .sh[style*="border:1.00px solid #000000"]{
  border-color:var(--hair)!important;
}
html:not([data-theme="dark"]) .pp [stroke="#101010"],
html:not([data-theme="dark"]) .pp [stroke="#0D0D0D"],
html:not([data-theme="dark"]) .pp [stroke="#000000"]{stroke:var(--hair)!important;}

/* P5 · soften the three cases and remove the heavy bottom slab. */
section[data-p="5"] :is([data-sid="4"],[data-sid="12"],[data-sid="20"]){
  border:1px solid var(--hair)!important;border-radius:18px!important;background:var(--card-bg-2)!important;
}
section[data-p="5"] [data-sid="28"]{
  border:0!important;border-left:5px solid var(--amber)!important;border-radius:0 14px 14px 0!important;
  background:color-mix(in srgb,var(--card-bg-2) 88%,var(--amber) 12%)!important;
}
section[data-p="5"] .sh.rule path{stroke:var(--hair)!important;stroke-width:1!important;}

/* P14 · GPT R27.1 增量（2026-08-12 交接）：④ 能力从突兀 amber 大方块改为带顶线的 thesis surface。
   （同批 P17 的 build0+contain 提案与 Colin 现场拍板的「太木→太腻→恰好+图同拍」冲突，未采纳） */
section[data-p="14"] [data-sid="11"]{
  background:transparent!important;border:0!important;border-top:2px solid var(--amber)!important;
  border-radius:0!important;height:110px!important;
}
section[data-p="14"] [data-sid="12"]{color:var(--ink-m)!important;}
section[data-p="14"] [data-sid="13"]{color:var(--amber)!important;}
/* R27.4（Colin）：落点句「临场感的落点：交互」移到 thesis 顶线上方压轴（原位 1000,852 右下角） */
section[data-p="14"] [data-sid="26"]{left:240px!important;top:600px!important;}

/* P10 · R27.3（Colin）：「智能音箱 你叫醒我」标签框 116×58 贴字宽极限，
   Mac PingFang 渲染下尾字被裁；加宽加高保持圆心对位（机检 ⑪ 未点名的盲区，防御性放宽） */
section[data-p="10"] [data-sid="7"]{left:270.8px!important;width:160px!important;height:66px!important;}

/* P15 · remove the isolated lower-left box; keep one continuous thesis line. */
section[data-p="15"] [data-sid="21"]{
  background:transparent!important;border:0!important;border-top:1px solid var(--hair)!important;border-radius:0!important;
  top:806px!important;height:170px!important;
}
section[data-p="15"] [data-sid="22"]{left:120px!important;top:832px!important;width:820px!important;height:122px!important;}

/* P19/P20 · bottom questions must never be clipped or covered. */
section[data-p="19"] [data-step="3"][data-sid="2"]{
  left:120px!important;top:918px!important;width:1680px!important;height:86px!important;z-index:20!important;
}
section[data-p="19"] [data-step="3"][data-sid="2"] span{font-size:35px!important;line-height:1.35!important;}
section[data-p="19"] :is([data-sid="18"],[data-sid="19"],[data-sid="20"]) span{color:#fffffe!important;}
section[data-p="20"] [data-sid="21"]{top:896px!important;height:150px!important;border-radius:14px!important;}
section[data-p="20"] [data-sid="22"]{
  left:164px!important;top:924px!important;width:1588px!important;height:92px!important;z-index:20!important;
}
section[data-p="20"] [data-sid="22"] span{font-size:30px!important;line-height:1.42!important;}

/* P29 · accent-on-accent copy gets a fixed ink color. */
section[data-p="29"] [data-sid="29"]{border-radius:16px!important;}
section[data-p="29"] [data-sid="31"]{left:160px!important;width:1580px!important;height:88px!important;}
section[data-p="29"] [data-sid="31"] span{color:#0d0d0d!important;}

/* Custom R27 pages */
.r27-metric{border-radius:28px;background:color-mix(in srgb,var(--card-bg-2) 92%,var(--amber) 8%);border:1px solid var(--hair);}
.r27-metric svg{position:absolute;left:54px;top:42px;width:350px;height:350px;}
.r27-metric .track{fill:none;stroke:var(--hair);stroke-width:30;}
.r27-metric .arc{fill:none;stroke:var(--amber);stroke-width:30;stroke-linecap:round;}
.r27-metric .num{position:absolute;left:0;top:145px;width:458px;text-align:center;font:900 118px/1 var(--f-cn);color:var(--ink);}
.r27-metric .num b{font-size:48px;color:var(--amber);}
.r27-metric .caption{position:absolute;left:42px;right:42px;bottom:38px;text-align:center;font:700 27px/1.35 var(--f-cn);color:var(--ink);}
.r27-metric .caption small{display:block;margin-top:8px;font:400 18px/1.4 var(--f-cn);color:var(--ink-m);}

.r27-quote-row{border-left:6px solid var(--amber);padding:16px 0 16px 44px;}
.r27-quote-row .main{font:700 65px/1.32 var(--f-cn);letter-spacing:-.02em;color:var(--ink);}
.r27-quote-row .main em{font-style:normal;color:var(--amber);}
.r27-quote-row .sub{margin-top:14px;font:500 20px/1.45 var(--f-mono);letter-spacing:.08em;color:var(--ink-m);}

.r27-dialogue{border-radius:18px;padding:28px 32px;background:var(--card-bg-2);border:1px solid var(--hair);}
.r27-dialogue.accent{background:color-mix(in srgb,var(--card-bg-2) 82%,var(--amber) 18%);border-color:color-mix(in srgb,var(--amber) 48%,transparent);}
.r27-dialogue .who{font:700 16px/1 var(--f-mono);letter-spacing:.16em;color:var(--amber);}
.r27-dialogue .say{margin-top:16px;font:700 39px/1.25 var(--f-cn);color:var(--ink);}
.r27-quote-card{padding:42px 48px;border-radius:24px;background:var(--card-bg-2);border:1px solid var(--hair);}
.r27-quote-card .speaker{font:700 17px/1 var(--f-mono);letter-spacing:.15em;color:var(--amber);}
.r27-quote-card blockquote{margin-top:30px;font:700 52px/1.32 var(--f-cn);letter-spacing:-.015em;color:var(--ink);}
.r27-quote-card .time{margin-top:28px;font:500 16px/1 var(--f-mono);letter-spacing:.12em;color:var(--ink-3);}

.r27-calc-line{height:4px;border-radius:999px;background:var(--hair);}
.r27-calc-node{padding:28px 28px 24px;border-radius:18px;background:var(--card-bg-2);border:1px solid var(--hair);}
.r27-calc-node .n{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:var(--amber);color:#0d0d0d;font:800 18px/1 var(--f-mono);}
.r27-calc-node h3{margin-top:22px;font:700 34px/1.25 var(--f-cn);color:var(--ink);}
.r27-calc-node p{margin-top:14px;font:400 19px/1.45 var(--f-cn);color:var(--ink-m);}
.r27-result{font:900 128px/.9 var(--f-cn);letter-spacing:-.05em;color:var(--amber);}
.r27-result small{font:700 42px/1 var(--f-mono);letter-spacing:0;color:var(--ink);}

.r27-chart{border-radius:22px;background:var(--card-bg-2);border:1px solid var(--hair);}
.r27-chart text{font-family:var(--f-cn);fill:var(--ink-m);}
.r27-chart .axis{stroke:var(--hair);stroke-width:2;}
.r27-chart .curve{fill:none;stroke:var(--amber);stroke-width:7;stroke-linecap:round;}
.r27-chart .dot{fill:var(--slide-bg);stroke:var(--amber);stroke-width:6;}
.r27-chart .goal{fill:var(--amber);stroke:var(--amber);}
.r27-chart .grid{stroke:var(--hair);stroke-width:1;stroke-dasharray:5 8;}

/* R27.4 采纳 GPT 裁法：素材 1500×750，插画占上部 ~540px，底部两百多像素烘着与
   HTML 卡片重复的文案带——原生宽度顶对齐，只裁掉重复行，人物头肩上身完整 */
.pp .sh.r27-face-strip{overflow:hidden;border-radius:18px;background:transparent;}
/* ↑ 提级到 .pp .sh 同权重之上：基础层 .pp .sh{overflow:visible} 会盖掉单类选择器——
   GPT 预览同病（其母版里重复文案带实际没裁掉），此处按交接意图修正 */
.r27-face-strip img{width:100%!important;height:auto!important;max-width:none!important;
  max-height:none!important;object-fit:unset!important;display:block!important;}
/* ↑ max-height:none 是关键：全局 reset img{max-height:100%} 会把图钳回盒高压扁（GPT 预览同病） */
.r27-face-card{padding:26px 30px;border-radius:16px;border:1px solid var(--hair);background:var(--card-bg-2);}
.r27-face-card.mid{background:var(--amber);border-color:var(--amber);}
.r27-face-card.deep{background:var(--acc-deep);border-color:var(--acc-deep);}
.r27-face-card .en{font:700 14px/1 var(--f-mono);letter-spacing:.18em;color:var(--ink-m);}
.r27-face-card.mid :is(.en,h3,p){color:#0d0d0d;}
.r27-face-card.deep :is(.en,h3,p){color:#fffffe;}
.r27-face-card h3{margin-top:12px;font:700 52px/1 var(--f-cn);color:var(--ink);}
.r27-face-card p{margin-top:12px;font:400 19px/1.42 var(--f-cn);color:var(--ink-m);}

.r27-timeline-line{height:4px;border-radius:999px;background:linear-gradient(90deg,var(--hair),var(--amber));}
.r27-milestone{padding:24px 22px;border-radius:16px;background:var(--card-bg-2);border:1px solid var(--hair);}
.r27-milestone.active{background:var(--amber);border-color:var(--amber);}
.r27-milestone .date{font:700 16px/1 var(--f-mono);letter-spacing:.11em;color:var(--amber);}
.r27-milestone.active .date{color:#0d0d0d;}
.r27-milestone h3{margin-top:14px;font:700 25px/1.25 var(--f-cn);color:var(--ink);}
.r27-milestone.active h3{color:#0d0d0d;}
.r27-milestone p{margin-top:10px;font:400 17px/1.38 var(--f-cn);color:var(--ink-m);}
.r27-milestone.active p{color:rgba(13,13,13,.72);}
.r27-pin{width:22px;height:22px;border-radius:50%;background:var(--slide-bg);border:5px solid var(--amber);}

/* R27.1c：P37 名片图回归 R26 原几何裸图呈现，.r27-qr-card 白卡包装退役（越包越小） */
.r27-qr-card h3{margin-top:18px;font:700 25px/1.2 var(--f-cn);color:var(--ink);}
.r27-qr-card p{margin-top:8px;font:400 16px/1.4 var(--f-cn);color:var(--ink-m);}
</style>"""


# ── R28 · CONF 背景板（2026-08-12 skill 新规：FLOW_SVG 流场退出 CONF，静态远景板上岗）──
# 默认组合四板成节奏（skill 铁律：一页一张 · 未采用候选不入仓 · 板为静态层，内容动效照旧）
def _conf_board(n):
    """页型 → 背景板类名后缀。R28.1（Colin）：内容板按幕轮换，换板即换章——
    全场 5 板，落在 skill「一场 4–6 张」区间内；同幕之内不换图。
    R29（2026-08-12 Colin）：side-rail 退役——竖杠元素与 P15/16 图形页冲突，
    二幕回归 matrix；三幕保留 axis-map，25/28 边界仍换板"""
    if n in (1, 37):
        return "title-02"        # 封面 / 致谢 · Orbit 轨道
    if n in (4, 26, 27):
        return "quote-02"        # 金句 MQ 01–03 · Halo Rings 光环
    if n == 14:
        return "chapter-03"      # ④ THE ENGINE 章节开篇 · Constellation 星座
    if n <= 25:
        return "content-01"      # 一、二幕 · 问题角色 + 临场引擎 · Matrix 结构网格
    return "content-03"          # 第三幕 · 声网产品落地段 · Axis Map 轴线图


R28_CSS = r"""<style id="robot26-r28-conf-boards">
/* R28 · CONF 背景板库（4 板 · 双主题成对 · 透明度梯度内置） */
.conf-bg{position:absolute;inset:0;z-index:0;pointer-events:none;background-repeat:no-repeat;
  background-position:center;background-size:cover;opacity:var(--conf-bg-opacity,.58);}
.slide.conf-boarded{background:transparent!important;}
.slide.conf-boarded>.pp{z-index:1;}
.conf-bg-title-02{--conf-bg-opacity:.66;background-image:url('/decks/assets/conf-boards/title-02-orbit-light.png');}
.conf-bg-chapter-03{--conf-bg-opacity:.58;background-image:url('/decks/assets/conf-boards/chapter-03-constellation-light.png');}
.conf-bg-quote-02{--conf-bg-opacity:.46;background-image:url('/decks/assets/conf-boards/quote-02-halo-rings-light.png');}
.conf-bg-content-01{--conf-bg-opacity:.42;background-image:url('/decks/assets/conf-boards/content-01-matrix-light.png');}
.conf-bg-content-02{--conf-bg-opacity:.42;background-image:url('/decks/assets/conf-boards/content-02-side-rail-light.png');}
.conf-bg-content-03{--conf-bg-opacity:.42;background-image:url('/decks/assets/conf-boards/content-03-axis-map-light.png');}
html[data-theme="dark"] .conf-bg-title-02{background-image:url('/decks/assets/conf-boards/title-02-orbit-dark.png');}
html[data-theme="dark"] .conf-bg-chapter-03{background-image:url('/decks/assets/conf-boards/chapter-03-constellation-dark.png');}
html[data-theme="dark"] .conf-bg-quote-02{background-image:url('/decks/assets/conf-boards/quote-02-halo-rings-dark.png');}
html[data-theme="dark"] .conf-bg-content-01{background-image:url('/decks/assets/conf-boards/content-01-matrix-dark.png');}
html[data-theme="dark"] .conf-bg-content-02{background-image:url('/decks/assets/conf-boards/content-02-side-rail-dark.png');}
html[data-theme="dark"] .conf-bg-content-03{background-image:url('/decks/assets/conf-boards/content-03-axis-map-dark.png');}
html[data-theme="dark"] .conf-bg{filter:saturate(.92);}
</style>"""


def _r27_sh(classes, style, body, step=None, sid=None):
    a = ' data-sid="%s"' % sid if sid else ""
    a += ' data-step="%d"' % step if step is not None else ""
    return '<div class="sh %s"%s style="%s">%s</div>' % (classes, a, style, body)


def _r27_section(page, steps, body):
    sig = '<div class="sig">%d/%d</div>' % (page, len(MODEL["slides"]))
    return ('<section class="slide conf-boarded" data-p="%d" data-steps="%d">\n'
            '  <div class="conf-bg conf-bg-%s" aria-hidden="true"></div>\n'
            '  <div class="pp">%s%s</div>\n</section>'
            % (page, steps, _conf_board(page), sig, body))


def _r27_p3():
    # 2026 Clutch 口径（press release 2026-06-25 · N=422，Fable 已逐句核对原文）
    C = 2 * math.pi * 150          # .dwa 惯例：--len=弧长 · --rest=整周长（机检 ④）
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:120px;top:92px;width:1680px;height:28px',
                "THE NUMBERS DON'T LIE", sid="r3k"),
        _r27_sh('ink r27-headline', 'left:120px;top:148px;width:1680px;height:154px',
                'AI 已经普及，<strong>糟糕体验仍在直接伤害留存。</strong>'),
        _r27_sh('settle r27-metric', 'left:230px;top:350px;width:458px;height:500px',
                '<svg viewBox="0 0 400 400"><circle class="track" cx="200" cy="200" r="150"/>'
                '<circle class="arc dwa" style="--len:%.1f;--rest:%.1f;--i:1" cx="200" cy="200" r="150" transform="rotate(-90 200 200)"/></svg>'
                '<div class="num">87<b>%%</b></div><div class="caption">经常接触 AI 智能体<small>采用已经发生，体验标准没有降低</small></div>' % (C * .87, C)),
        _r27_sh('settle r27-metric', 'left:1232px;top:350px;width:458px;height:500px',
                '<svg viewBox="0 0 400 400"><circle class="track" cx="200" cy="200" r="150"/>'
                '<circle class="arc dwa" style="--len:%.1f;--rest:%.1f;--i:3" cx="200" cy="200" r="150" transform="rotate(-90 200 200)"/></svg>'
                '<div class="num">67<b>%%</b></div><div class="caption">差体验后不想继续使用<small>问题不是 AI 身份，而是关系被破坏</small></div>' % (C * .67, C)),
        _r27_sh('flow r27-note', 'left:630px;top:905px;width:660px;height:62px;text-align:center;font-weight:700;color:var(--ink)',
                '用户不是拒绝 AI；用户拒绝的是<strong class="r27-accent">无法建立信任的 AI</strong>。'),
        _r27_sh('flow r27-source', 'left:120px;top:1020px;width:1680px;height:24px',
                'SOURCE · CLUTCH CONSUMER AI SUPPORT STUDY · 2026.06 · N=422', sid="r3s"),
    ])
    return _r27_section(3, 0, body)


def _r27_p4():
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:120px;top:84px;width:1680px;height:28px',
                'MONEY QUOTE · 01 OF 03', sid="r4k"),
        _r27_sh('ink r27-quote-row', 'left:255px;top:250px;width:1410px;height:250px',
                '<div class="main">3 天扔抽屉，不是技术故障，<br>是<em>关系破裂</em>。</div>'
                '<div class="sub">WHEN NOVELTY ENDS, RELATIONSHIP HAS TO BEGIN.</div>'),
        _r27_sh('flow r27-hair', 'left:255px;top:545px;width:1410px;height:1px', ''),
        _r27_sh('ink r27-quote-row', 'left:255px;top:605px;width:1410px;height:250px',
                '<div class="main">用户买的不是更聪明的玩具，<br>是<em>更处得来的伙伴</em>。</div>'
                '<div class="sub">INTELLIGENCE EARNS ATTENTION. COMPANIONSHIP EARNS RETURN.</div>'),
        _r27_sh('flow r27-label', 'left:1480px;top:995px;width:320px;height:24px;text-align:right',
                '<span>钉子 · PIN 01</span>', sid="r4p"),
    ])
    return _r27_section(4, 0, body)


def _r27_p11():
    # 归属按官方口径（见模块头注释）：Jensen 的台词是追问，感叹两句都是 Ilya 的
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:120px;top:96px;width:1680px;height:28px',
                'A NUMBER FROM THE SOURCE · NVIDIA GTC 2023', sid="r11k"),
        _r27_sh('ink r27-headline', 'left:120px;top:150px;width:1680px;height:150px',
                '一生，只听得到「<strong>10 亿词</strong>」。'),
        _r27_sh('rise r27-quote-card', 'left:120px;top:360px;width:1020px;height:470px',
                '<div class="speaker" data-sid="r11sp">ILYA SUTSKEVER · OPENAI CO-FOUNDER &amp; CHIEF SCIENTIST (2023)</div>'
                '<blockquote>“As human beings, we get to hear about <span class="r27-accent">one billion words</span> in our entire life.”</blockquote>'
                '<div class="time" data-sid="r11t">NVIDIA ON-DEMAND · GTCSPRING23-S52092</div>'),
        _r27_sh('flow r27-dialogue', 'left:1210px;top:400px;width:590px;height:170px',
                '<div class="who">JENSEN HUANG</div><div class="say">“Only one billion words?”</div>', step=1),
        _r27_sh('flow r27-dialogue accent', 'left:1210px;top:620px;width:590px;height:210px',
                '<div class="who">ILYA SUTSKEVER</div><div class="say">“That’s amazing. That’s not a lot.”</div>', step=2),
        _r27_sh('flow r27-note', 'left:120px;top:875px;width:1680px;height:60px',
                '有限的输入，意味着<strong class="r27-accent">值得保留的上下文必须被选择</strong>。'),
        _r27_sh('flow r27-source', 'left:120px;top:1015px;width:1680px;height:24px',
                'SOURCE · NVIDIA GTC SPRING 2023 · FIRESIDE CHAT: AI TODAY AND VISION OF THE FUTURE · 2023.03', sid="r11s"),
    ])
    return _r27_section(11, 2, body)


def _r27_p12():
    nodes = [
        (120, None, '1', '10 亿词', '一生听到的语言输入', 'ILYA · GTC 2023'),
        (545, 1, '2', '× 25%', '只保留值得记住的部分', '思想实验筛选率'),
        (970, 2, '3', '÷ 150', '换算为约 167 万分钟', '词 / 分钟'),
        # R27.3（Colin）：kbps 反算落到 0.29 TB，不做 313GB→TiB 的单位跳变
        #   （0.29 TB ÷ 167 万分钟 ≈ 2.9e11B / 1.0e8s ≈ 23 kbps；23kbps×167万分钟=0.2875TB≈0.29 ✓）
        (1395, 3, '4', '× 23 kbps', '≈ 0.29 TB', '长期语音存储'),
    ]
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:120px;top:96px;width:1680px;height:28px',
                'FROM WORDS TO MEMORY · A BACK-OF-THE-ENVELOPE MODEL', sid="r12k"),
        _r27_sh('ink r27-headline', 'left:120px;top:150px;width:1680px;height:150px',
                '把「10 亿词」折成一条<strong>可计算的记忆链</strong>。'),
        _r27_sh('flow r27-calc-line', 'left:200px;top:455px;width:1515px;height:4px', ''),
    ])
    for x, step, num, title, desc, foot in nodes:
        body += _r27_sh('rise r27-calc-node', 'left:%dpx;top:345px;width:365px;height:300px' % x,
                        '<div class="n">%s</div><h3>%s</h3><p>%s<br><small>%s</small></p>' % (num, title, desc, foot),
                        step=step)
    body += ''.join([
        _r27_sh('settle r27-result', 'left:120px;top:720px;width:820px;height:150px',
                '0.29 <small>TB 级</small>', step=3),
        _r27_sh('flow r27-note', 'left:960px;top:740px;width:840px;height:120px',
                '这不是精确的人生配额，而是一个产品判断：<br><strong class="r27-accent">记忆不是无限堆积，而是持续筛选。</strong>', step=3),
        _r27_sh('flow r27-source', 'left:120px;top:1015px;width:1680px;height:24px',
                'ASSUMPTION · 25% RETENTION · 150 WORDS/MIN · 23 KBPS · ORDER-OF-MAGNITUDE MODEL', sid="r12s"),
    ])
    return _r27_section(12, 3, body)


def _r27_p13():
    chart = ('<svg viewBox="0 0 1030 520" width="1030" height="520" aria-label="关系深度与记忆容量概念曲线">'
             '<line class="axis" x1="90" y1="440" x2="970" y2="440"/><line class="axis" x1="90" y1="440" x2="90" y2="60"/>'
             '<line class="grid" x1="90" y1="330" x2="970" y2="330"/><line class="grid" x1="90" y1="220" x2="970" y2="220"/><line class="grid" x1="90" y1="110" x2="970" y2="110"/>'
             '<path class="curve" d="M120 420 C310 408 470 370 610 300 C735 238 820 145 925 82"/>'
             '<circle class="dot" cx="250" cy="397" r="13"/><circle class="dot" cx="470" cy="350" r="13"/><circle class="dot" cx="690" cy="252" r="13"/><circle class="dot goal" cx="925" cy="82" r="16"/>'
             '<text x="215" y="475" font-size="24">Siri</text><text x="415" y="475" font-size="24">普通玩具</text><text x="615" y="475" font-size="24">主流 AI 玩具</text><text x="855" y="475" font-size="24">伙伴目标</text>'
             '<text x="22" y="280" font-size="21" transform="rotate(-90 22 280)">RELATIONSHIP DEPTH</text><text x="410" y="515" font-size="21">MEMORY CAPACITY · LOG SCALE</text>'
             '<text x="850" y="58" font-size="25" font-weight="700" style="fill:var(--amber)">0.29 TB 级</text>'
             '</svg>')
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:120px;top:96px;width:1680px;height:28px',
                'RELATIONSHIP CAPACITY · CONCEPTUAL MODEL', sid="r13k"),
        _r27_sh('ink r27-headline', 'left:120px;top:150px;width:1680px;height:150px',
                '记忆容量决定了<strong>关系能走多深</strong>。'),
        _r27_sh('rise r27-chart', 'left:120px;top:330px;width:1080px;height:590px;padding:28px 24px', chart, step=1),
        _r27_sh('flow r27-card', 'left:1260px;top:365px;width:540px;height:250px;padding:40px',
                '<div class="r27-label">THE PARTNER LINE</div>'
                '<div style="margin-top:26px;font:700 43px/1.28 var(--f-cn);color:var(--ink)">伙伴不是"记得更多"，<br>而是<strong class="r27-accent">记得更对</strong>。</div>', step=2),
        _r27_sh('flow r27-card', 'left:1260px;top:665px;width:540px;height:205px;padding:36px 40px;border-left:6px solid var(--amber)',
                '<div class="r27-label">TAKEAWAY</div>'
                '<div style="margin-top:22px;font:700 31px/1.38 var(--f-cn);color:var(--ink)">音频是原料，<br><span class="r27-accent">可检索的共同历史</span>才是资产。</div>', step=3),
        _r27_sh('flow r27-source', 'left:120px;top:1015px;width:1680px;height:24px',
                'NOTE · CONCEPTUAL MODEL, NOT AN EMPIRICAL RETENTION CURVE', sid="r13s"),
    ])
    return _r27_section(13, 3, body)


def _r27_p17():
    img = ASSET["image24.png"]                       # comfort-faces.webp
    light = ASSET_LIGHT["image24.png"]               # comfort-faces-light.png（R26 资产复用）
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:80px;top:66px;width:1760px;height:28px', 'DEFINITION', sid="r17k"),
        _r27_sh('ink r27-headline', 'left:80px;top:118px;width:1760px;height:130px',
                '「活人感」不是越像人越好，<strong>是双方都能舒适。</strong>'),
        # R27.1（Colin 现场反馈）：叙事先立两种失败态（太木→太腻），恰好最后收，
        #        人物 strip 与「恰好」同拍出现（时序为 Colin 拍板件，GPT 的 build0 提案不采）
        # R27.4（GPT 裁法采纳）：strip 原生 1500 宽顶对齐、盒高 540 裁掉底部重复文案带
        _r27_sh('settle r27-face-strip', 'left:210px;top:210px;width:1500px;height:540px',
                '<img src="%s" data-dark-src="%s" data-light-src="%s" alt="活人感舒适度三种状态">' % (img, img, light), step=3),
        _r27_sh('rise r27-face-card', 'left:80px;top:755px;width:550px;height:195px',
                '<div class="en">TOO DRY</div><h3>太木</h3><p>正确，但没有关系温度。<br>用户不想再开口。</p>', step=1),
        _r27_sh('rise r27-face-card mid', 'left:685px;top:755px;width:550px;height:195px',
                '<div class="en">JUST RIGHT</div><h3>恰好</h3><p>自然、可持续相处。<br>下次还想跟它说话。</p>', step=3),
        _r27_sh('rise r27-face-card deep', 'left:1290px;top:755px;width:550px;height:195px',
                '<div class="en">TOO CLINGY</div><h3>太腻</h3><p>伪装成朋友的销售感。<br>三句之后想拔电源。</p>', step=2),
        _r27_sh('flow r27-note', 'left:80px;top:985px;width:1760px;height:48px;text-align:center;font-size:25px;color:var(--ink)',
                '消费级机器人语境下：<strong class="r27-accent">活人感 = 角色立得住 + 临场撑得住</strong>。', step=4),
    ])
    return _r27_section(17, 4, body)


def _r27_p28():
    # 五节点与「19 个月」均为老 P28（模型 n=26）原口径，内容锚定不变，只换版式
    milestones = [
        (120, '2024.10', 'OpenAI × Agora', 'Realtime API · RTC partner', False),
        (458, '2024.10.24', '声网 × MiniMax', '国内 Realtime', False),
        (796, '2025.03.06', 'ConvoAI Engine 1.0', '引擎正式发布', False),
        (1134, '2025.10.31', '全栈能力', 'Studio + Engine 2.0 + Eval 3.0', True),
        (1472, '2026.03.10', 'Agora Phone Agent', '电话客服智能体 · Global', False),
    ]
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:120px;top:96px;width:1680px;height:28px',
                'CONVERSATIONAL AI MILESTONES', sid="r28k"),
        _r27_sh('ink r27-headline', 'left:120px;top:150px;width:1680px;height:150px',
                '19 个月，走完<strong>从 API 到全栈产品</strong>。'),
        _r27_sh('flow r27-timeline-line', 'left:180px;top:560px;width:1560px;height:4px', ''),
    ])
    for i, (x, date, title, desc, active) in enumerate(milestones):
        body += _r27_sh('rise r27-milestone' + (' active' if active else ''),
                        'left:%dpx;top:350px;width:300px;height:170px' % x,
                        '<div class="date">%s</div><h3>%s</h3><p>%s</p>' % (date, title, desc))
        body += _r27_sh('pop r27-pin', 'left:%dpx;top:551px;width:22px;height:22px' % (x + 139), '')
        body += _r27_sh('flow r27-note', 'left:%dpx;top:610px;width:300px;height:80px;text-align:center;font-size:18px' % x,
                        '0%d / 05' % (i + 1))
    body += _r27_sh('flow r27-card', 'left:120px;top:770px;width:1680px;height:150px;padding:34px 42px;border-left:6px solid var(--amber)',
                    '<div class="r27-label">FROM INFRASTRUCTURE TO PRODUCT</div>'
                    '<div style="margin-top:20px;font:700 35px/1.25 var(--f-cn);color:var(--ink)">我们已经替你把工程化的路走过一遍——接下来，轮到<strong class="r27-accent">产品体验</strong>。</div>')
    return _r27_section(28, 0, body)


def _r27_p37():
    body = ''.join([
        _r27_sh('flow r27-kicker', 'left:120px;top:110px;width:850px;height:28px', 'THANK YOU', sid="r37k"),
        _r27_sh('settle r27-headline', 'left:120px;top:190px;width:900px;height:155px', '谢谢。'),
        _r27_sh('flow', 'left:120px;top:390px;width:700px;height:150px;font:700 43px/1.38 var(--f-cn);color:var(--ink)',
                '让我们一起，把消费机器人<br>从<strong class="r27-accent">玩具</strong>做成<strong class="r27-accent">伙伴</strong>。'),
        _r27_sh('flow r27-note', 'left:120px;top:600px;width:700px;height:150px',
                '<strong style="color:var(--ink)">Colin · 姚光华</strong><br>声网 AI 产品线负责人<br>ConvoAI · Robotics 1 开发套件'),
        _r27_sh('flow r27-card', 'left:120px;top:830px;width:700px;height:170px;padding:34px 40px;border-left:6px solid var(--amber)',
                '<div class="r27-label">KEEP THE CONVERSATION GOING</div>'
                '<div style="margin-top:20px;font:700 28px/1.35 var(--f-cn);color:var(--ink)">把现场的问题带走，<br><span class="r27-accent">把下一次对话做得更像伙伴。</span></div>'),
        # R27.1c（Colin：找回之前的版本）：两张名片图按 R26 原几何一比一还原——
        #   不套白卡、不加标签、原始比例大图（微信 474.8×604.7 / 小红书 443.1×604.7）。
        #   第二张的正名不变：内容是 Colin 小红书名片卡（R27.1b 查明，原 qr-rte 是误标），
        #   仓库同时保留 qr-rte.jpg 同内容副本，喂缓存里的旧 HTML，防「图裂」。
        _r27_sh('pop', 'left:878.7px;top:276.6px;width:474.8px;height:604.7px',
                '<img src="%sqr-wechat.jpg" alt="Colin 微信二维码" style="width:100%%;height:100%%;object-fit:contain">' % A),
        _r27_sh('pop', 'left:1426.0px;top:276.7px;width:443.1px;height:604.7px',
                '<img src="%sqr-xiaohongshu.jpg" alt="Colin 小红书名片（含二维码）" style="width:100%%;height:100%%;object-fit:contain">' % A),
    ])
    return _r27_section(37, 0, body)


def apply_r27(secs):
    """R27 · 整页替换 + 精确补丁。补丁断言命中次数：builder 输出格式一变，构建期就报错。"""
    def patch(idx, old, new):
        hits = secs[idx].count(old)
        assert hits == 1, "R27 补丁未命中（%d 处）@P%d: %s…" % (hits, idx + 1, old[:56])
        secs[idx] = secs[idx].replace(old, new)
    # P2 · 眉标年份 2025 → 2026
    patch(1, 'RETENTION SHAPE OF CONSUMER ROBOTS, 2025',
             'RETENTION SHAPE OF CONSUMER ROBOTS, 2026')
    # P5 · 总结底栏延后到 build 4（不再从 step 0 起压一块空白重底）
    patch(4, '<div class="sh rise" data-sid="28" style="left:120.0px;top:802.5px',
             '<div class="sh rise" data-sid="28" data-step="4" style="left:120.0px;top:802.5px')
    # P6 · 结论面 + 英文小标一起延后到 build 5，build 0–4 干净结束在对比表
    patch(5, '<div class="sh rise" data-sid="44" style="left:120.0px;top:899.9px',
             '<div class="sh rise" data-sid="44" data-step="5" style="left:120.0px;top:899.9px')
    patch(5, '<div class="sh tx flow" data-sid="46" data-af="1" data-step="4" style="left:1260.0px;top:936.0px',
             '<div class="sh tx flow" data-sid="46" data-af="1" data-step="5" style="left:1260.0px;top:936.0px')
    # P14 · 章节眉标+标题 build 0 常驻（入页不再是纯空白帧；原 5 步保留）
    patch(13, ' data-sid="2" data-af="1" data-step="2" style="left:120.0px;top:156.1px',
              ' data-sid="2" data-af="1" style="left:120.0px;top:156.1px')
    patch(13, ' data-sid="3" data-af="1" data-step="2" style="left:120.0px;top:210.1px',
              ' data-sid="3" data-af="1" style="left:120.0px;top:210.1px')
    # 整页重排（build_slide 产物整段替换；页码 sig 由 _r27_section 自带）
    for page, maker in ((3, _r27_p3), (4, _r27_p4), (11, _r27_p11), (12, _r27_p12),
                        (13, _r27_p13), (17, _r27_p17), (28, _r27_p28), (37, _r27_p37)):
        secs[page - 1] = maker()
    return secs


def main():
    apply_quote_patch(MODEL)
    apply_r24(MODEL)
    secs = [build_slide(sl) for sl in MODEL["slides"]]
    # R25 · 字面色 → 主题变量（黑字/白卡内深灰字/chip 上黑字保持字面：两主题都在浅面上）
    def _apply_map(t, mp):
        for a, b in mp:
            t = t.replace(a, b)
        return t
    R25_MAP = [
        ("color:#FFFFFF", "color:var(--ink)"),
        ("color:#FFFFFE", "color:var(--ink)"),
        ("color:#D4B7F9", "color:var(--amber)"),
        ("color:#944AF0", "color:var(--acc-deep)"),
        ("color:#A6A6A6", "color:var(--ink-m)"),
        ("color:#A7A9BE", "color:var(--ink-soft)"),
        ("color:#D9D9D9", "color:var(--ink-2x)"),
        ("background:#D4B7F9", "background:var(--amber)"),
        ("background:#000000", "background:var(--void-0)"),
        ("background:#0D0D0D", "background:var(--void-1)"),
        ("background:#0A0A0A", "background:var(--void-2)"),
        ("background:#1F1D2B", "background:var(--card-bg-2)"),
        ("background:#944AF0", "background:var(--acc-deep)"),
    ]
    secs = [_apply_map(x, R25_MAP) for x in secs]
    # R27 · 整页替换 + 精确补丁（在 R25 变量化之后跑：R27 手排页生来就是变量色）
    secs = apply_r27(secs)
    doc = (
        '<!DOCTYPE html>\n<html lang="zh-CN" data-theme="dark"><head>\n'
        '<script>try{if(localStorage.getItem("colin-theme")==="light")document.documentElement.removeAttribute("data-theme")}catch(e){}</script>\n'
        '<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>从玩具到伙伴 · 消费级机器人的「活人感」交互设计 · 姚光华 Colin</title>\n'
        + FONTS + "\n" + CSS + "\n" + R27_CSS + "\n" + R28_CSS + "\n</head>\n<body>\n"
        '<div class="deck-viewport">\n  <div class="deck-stage" id="deckStage">\n'
        # R28：FLOW_SVG 流场退出 CONF 装配（skill 2026-08-12 新规；流场是 base 站内签名，
        #      conf 换每页静态背景板。FLOW_SVG 常量与 .deck-flow CSS 保留便于回滚）
        + STAGE_CHROME + "\n"
        + "\n".join(secs) +
        "\n  </div>\n</div>\n"
        '<div class="deck-progress" id="deckProgress"></div>\n'
        '<div class="deck-steps" id="deckSteps"></div>\n'
        '<div class="edit-hotzone"></div>\n'
        '<button class="edit-toggle" id="editToggle">EDIT</button>\n'
        '<button class="deck-swap" id="deckSwap">浅底</button>\n'
        + JS + "\n" + RULER + "\n</body></html>\n"
    )
    open(OUT, "w", encoding="utf-8").write(doc)
    steps = [len([g for g in s["clicks"] if g]) + (1 if s["n"] == 24 else 0) for s in MODEL["slides"]]
    print("robot26.html · %d 页 · %dKB" % (len(secs), len(doc) // 1024))
    print("分步数逐页：" + " ".join(str(x) for x in steps) + "  （合计 %d 次单击）" % sum(steps))


if __name__ == "__main__":
    main()
