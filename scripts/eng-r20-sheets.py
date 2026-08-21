#!/usr/bin/env python3
# 终审素材拼版 · convoai-engine「大内容轮 17 → 20 页」
#   ① r20-newpages.png        六页（P10/P11/P12/P13/P14/P19）浅色 全尺寸 2×3 带标签
#   ② r20-dark.png            同六页 深色 2×3
#   ③ p15-arrows-fix.png      P15 编排页 BEFORE / AFTER 并置（箭头语义修）
#   ④ engine-20p-contact.png  20 × 2（浅/深）全量 contact sheet
#
# BEFORE 取 git HEAD 的产物（本轮开工前 17 页版的 P13 编排页 = 现在的 P15），
# 开工第一件事就拍在 /tmp/eng-r20/p13-orch-BEFORE.png。
# 用法：python3 scripts/eng-r20-sheets.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REV = Path("/home/claude/eco-review")
REV.mkdir(parents=True, exist_ok=True)
SHOTS = Path("/tmp/eng-r20-full")          # 20×2 全量（shot-engine-family.mjs 产出）
BEFORE15 = Path("/tmp/eng-r20/p13-orch-BEFORE.png")

NEW = [
    (10, "SAL 重做 · 三种噪声 / 三层方案 + 双层防御环"),
    (11, "弱网重做 · 补 AI QoS 断网续播机理"),
    (12, "多模态改造 · 聚焦视觉模态（重点 / 次级配重）"),
    (13, "新增 · Physical AI · R1 开发套件"),
    (14, "新增 · Physical AI · 已经上岗（案例墙）"),
    (19, "新增 · OpenAI 合作（title 板 quote 语域）"),
]

FONTS = ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
         "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
def font(sz):
    for f in FONTS:
        if Path(f).exists():
            try:
                return ImageFont.truetype(f, sz)
            except Exception:
                pass
    return ImageFont.load_default()

BG, INK, SUB = (22, 22, 26), (240, 240, 245), (150, 150, 160)


def sheet(cells, cols, cell_w, out, pad=18, lab_h=34, title=None, title_h=0):
    """cells = [(png_path|None, 标签)]，按行优先铺"""
    cell_h = round(cell_w * 1080 / 1920)
    rows = (len(cells) + cols - 1) // cols
    W = pad + cols * (cell_w + pad)
    H = pad + title_h + rows * (lab_h + cell_h + pad)
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    if title:
        d.text((pad + 2, pad + 4), title, font=font(26), fill=INK)
    for i, (p, lab) in enumerate(cells):
        r, c = divmod(i, cols)
        x = pad + c * (cell_w + pad)
        y = pad + title_h + r * (lab_h + cell_h + pad)
        d.text((x + 2, y + 6), lab, font=font(19), fill=SUB if "BEFORE" in lab else INK)
        if p is None:
            continue
        im.paste(Image.open(p).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS),
                 (x, y + lab_h))
        d.rectangle([x, y + lab_h, x + cell_w - 1, y + lab_h + cell_h - 1], outline=(64, 64, 72))
    im.save(out)
    print("·", out, im.size)


# ① / ② 六页 × 浅 / 深
for th, fn, cn in (("light", "r20-newpages.png", "浅色"), ("dark", "r20-dark.png", "深色")):
    sheet([(SHOTS / ("p%02d-%s.png" % (p, th)), "P%d · %s" % (p, t)) for p, t in NEW],
          2, 1400, REV / fn, title_h=46,
          title="convoai-engine · 17→20 页大内容轮 · 新 / 重做六页（%s 全尺寸）" % cn)

# ③ P15 编排页 BEFORE / AFTER（箭头语义修）
sheet([(BEFORE15, "BEFORE · 旧 P13 —— 同屏三种箭头语义、左右两列同向（进 / 出相反）"),
       (SHOTS / "p15-light.png", "AFTER · 新 P15 —— 只保留「插入 = 指向引擎」一种阅读方向；换装件降为块上方小号灰注记")],
      1, 1560, REV / "p15-arrows-fix.png", title_h=46,
      title="convoai-engine · P15 编排页 · 箭头语义修（BEFORE / AFTER）")

# ④ 20 × 2 全量 contact sheet
cs = []
for i in range(1, 21):
    for th in ("light", "dark"):
        cs.append((SHOTS / ("p%02d-%s.png" % (i, th)), "P%d · %s" % (i, th)))
sheet(cs, 4, 760, REV / "engine-20p-contact.png", title_h=46,
      title="convoai-engine · 20 页 × 浅/深 全量 contact sheet（2026-08-21 大内容轮后）")
