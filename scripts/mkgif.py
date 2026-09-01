#!/usr/bin/env python3
"""PNG 序列 → GIF（PIL · 自适应调色板）。用法：mkgif.py <帧目录> <输出> [fps] [scale]"""
import sys, pathlib
from PIL import Image
src, dst = pathlib.Path(sys.argv[1]), sys.argv[2]
fps = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0
sc = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
fs = sorted(src.glob("f*.png"))
assert fs, "没有帧"
ims = []
for f in fs:
    im = Image.open(f).convert("RGB")
    if sc != 1.0:
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    ims.append(im.quantize(colors=128, method=Image.FASTOCTREE))
ims[0].save(dst, save_all=True, append_images=ims[1:], duration=int(round(1000 / fps)),
            loop=0, optimize=True, disposal=2)
print("%s · %d 帧 @ %.0ffps · %dx%d · %.1fKB" %
      (dst, len(ims), fps, ims[0].width, ims[0].height, pathlib.Path(dst).stat().st_size / 1024))
