#!/usr/bin/env python3
"""八页联览：4×2 网格 + 页码角标。用法：montage-info.py <theme> <out>"""
import sys, pathlib
from PIL import Image, ImageDraw
th, out = sys.argv[1], sys.argv[2]
SRC = pathlib.Path("/home/claude/eco-review")
COLS, W = 4, 900                      # 单页缩到 900 宽
ims = [Image.open(SRC / f"info-p{i}-{th}.png").convert("RGB") for i in range(1, 9)]
sw, sh = W, round(W * ims[0].height / ims[0].width)
pad, top = 14, 0
bg = (245, 245, 247) if th == "light" else (10, 10, 12)
fg = (30, 30, 34) if th == "light" else (215, 215, 220)
sheet = Image.new("RGB", (COLS * sw + (COLS + 1) * pad, 2 * sh + 3 * pad + top), bg)
d = ImageDraw.Draw(sheet)
for k, im in enumerate(ims):
    x = pad + (k % COLS) * (sw + pad)
    y = pad + top + (k // COLS) * (sh + pad)
    sheet.paste(im.resize((sw, sh), Image.LANCZOS), (x, y))
    d.rectangle([x, y, x + sw - 1, y + sh - 1], outline=(190, 190, 196) if th == "light" else (54, 54, 60))
    d.text((x + 8, y + 6), "P%d" % (k + 1), fill=fg)
sheet.save(out)
print("%s · %dx%d · %.0fKB" % (out, sheet.width, sheet.height, pathlib.Path(out).stat().st_size / 1024))
