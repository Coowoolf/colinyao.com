#!/usr/bin/env python3
# 终审素材拼版 · convoai-engine「极致版」图形升维
#   ① ultimate-before-after.png  改动页 浅色 before/after 并置（4 列 = before/after/before/after）
#   ② ultimate-dark.png          改动页 深色 after（2 列）
#   ③ engine-ultimate-contact.png 17 × 2（浅/深）全量 contact sheet
# 用法：python3 scripts/eng-ultimate-sheets.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REV = Path("/home/claude/eco-review")
BEFORE, AFTER = REV / "eng-before", REV / "eng-after"
SHOTS = Path("/tmp/eng-full")          # 17×2 全量（shot-engine-family.mjs 产出）
PAGES = [2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 14]
TITLES = {2: "实时决策 · 决策环", 3: "双工三模式 · 双轨时序", 4: "全双工原理 · 活动带泳道",
          6: "实时语音链路 · 增量流带", 7: "VAD · 信号图", 9: "优雅打断 · 相位标注",
          10: "SAL · 场景图", 11: "弱网 · 双带时间轴", 12: "多模态 · IO 辐条",
          13: "编排 · 插槽机", 14: "接入架构 · P8 一致性"}

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


# ① before / after 并置：4 列 = before, after, before, after
cells = []
for p in PAGES:
    cells.append((BEFORE / ("p%02d-light.png" % p), "P%d BEFORE" % p))
    cells.append((AFTER / ("p%02d-light.png" % p), "P%d AFTER · %s" % (p, TITLES[p])))
while len(cells) % 4:
    cells.append((None, ""))
sheet(cells, 4, 880, REV / "ultimate-before-after.png", title_h=44,
      title="convoai-engine · 图形升维 · 浅色 BEFORE / AFTER 并置（11 张改动页）")

# ② 深色 after
sheet([(AFTER / ("p%02d-dark.png" % p), "P%d · %s" % (p, TITLES[p])) for p in PAGES],
      2, 1120, REV / "ultimate-dark.png", title_h=44,
      title="convoai-engine · 图形升维 · 深色 AFTER（11 张改动页）")

# ③ 17 × 2 全量 contact sheet
cs = []
for i in range(1, 18):
    for th in ("light", "dark"):
        cs.append((SHOTS / ("p%02d-%s.png" % (i, th)), "P%d · %s" % (i, th)))
sheet(cs, 4, 760, REV / "engine-ultimate-contact.png", title_h=44,
      title="convoai-engine · 17 页 × 浅/深 全量 contact sheet")
