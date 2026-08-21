#!/usr/bin/env python3
"""终审素材拼图器：把若干张截图按「标签 + 图」拼成一张对照图（PIL，无外部依赖）。

用法：
  python3 scripts/compose-review.py OUT.png "标签A::/path/a.png" "标签B::/path/b.png" [--cols 1|2]
说明：
  · 每格上方是一条 56px 的标签带（wqy-zenhei，中文能出）
  · --cols 2 时左右并置，否则上下叠
  · 图不缩放（保持像素级可读），格宽取各图最大宽
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
BAR, PAD, GAP = 56, 18, 18
BG, FG, SUB = (245, 245, 247), (17, 17, 17), (255, 142, 60)


def main():
    out = sys.argv[1]
    cols = 1
    args = []
    it = iter(sys.argv[2:])
    for a in it:
        if a == "--cols":
            cols = int(next(it))
        else:
            args.append(a)
    items = []
    for a in args:
        label, path = a.split("::", 1)
        items.append((label, Image.open(path).convert("RGB")))
    f = ImageFont.truetype(FONT, 30)
    cw = max(im.width for _, im in items)
    rows = (len(items) + cols - 1) // cols
    rh = [0] * rows
    for k, (_, im) in enumerate(items):
        r = k // cols
        rh[r] = max(rh[r], im.height + BAR)
    W = PAD * 2 + cols * cw + (cols - 1) * GAP
    H = PAD * 2 + sum(rh) + (rows - 1) * GAP
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)
    y = PAD
    for r in range(rows):
        x = PAD
        for c in range(cols):
            k = r * cols + c
            if k >= len(items):
                break
            label, im = items[k]
            d.rectangle([x, y, x + cw, y + BAR - 6], fill=(255, 255, 255))
            d.rectangle([x, y, x + 6, y + BAR - 6], fill=SUB)
            d.text((x + 20, y + 11), label, font=f, fill=FG)
            canvas.paste(im, (x, y + BAR))
            x += cw + GAP
        y += rh[r] + GAP
    canvas.save(out)
    print("· %s  %dx%d" % (out, W, H))


main()
