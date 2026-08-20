#!/usr/bin/env python3
# 终审素材拼版 · convoai-engine「三页收尾精修」（P14 握手时序 / P9 构图再平衡 / P6 微调）
#   ① ultimate-final3.png        三页 浅色 BEFORE / AFTER 并置（2 列 × 3 行，带标签）
#   ② engine-ultimate-contact.png 17 × 2（浅/深）全量 contact sheet · 重出
#
# BEFORE 取「本轮开工前的工作树快照」而不是 git HEAD：HEAD 落后两轮
# （上一轮 10 张图页升维尚未 commit），拿 HEAD 当 before 会把上一轮的成果算进这一轮，
# 三页的 delta 就读不准了。快照见 /tmp/final3-before（本轮开工第一件事拍的）。
# 用法：python3 scripts/eng-final3-sheets.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REV = Path("/home/claude/eco-review")
BEFORE, AFTER = Path("/tmp/final3-before"), Path("/tmp/final3-after")
SHOTS = Path("/tmp/eng-full")          # 17×2 全量（shot-engine-family.mjs 产出）
PAGES = [14, 9, 6]
TITLES = {14: "接入架构 · 握手时序 ①②③", 9: "优雅打断 · 构图再平衡", 6: "实时语音链路 · 支路让位"}

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


# ① 三页 before / after 并置：2 列 × 3 行
cells = []
for p in PAGES:
    cells.append((BEFORE / ("p%02d-light.png" % p), "P%d BEFORE · 本轮前（= 上一轮产物）" % p))
    cells.append((AFTER / ("p%02d-light.png" % p), "P%d AFTER · %s" % (p, TITLES[p])))
sheet(cells, 2, 1120, REV / "ultimate-final3.png", title_h=44,
      title="convoai-engine · 三页收尾精修 · 浅色 BEFORE / AFTER 并置（P14 / P9 / P6）")

# ② 17 × 2 全量 contact sheet（重出）
cs = []
for i in range(1, 18):
    for th in ("light", "dark"):
        cs.append((SHOTS / ("p%02d-%s.png" % (i, th)), "P%d · %s" % (i, th)))
sheet(cs, 4, 760, REV / "engine-ultimate-contact.png", title_h=44,
      title="convoai-engine · 17 页 × 浅/深 全量 contact sheet（三页收尾精修后）")
