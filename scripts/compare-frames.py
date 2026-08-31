#!/usr/bin/env python3
"""逐像素比对两张同尺寸截图（配 pinned-diff.mjs 用）：报差异像素数与最大通道差。

MASK 环境变量（2026-08-31 · LAB 家族第一波「全量 3D 化」新增）：
    MASK="x,y,w,h;x,y,w,h;…"  —— 比对前把这些矩形涂平（两张都涂）。
    给 3D 页的 canvas 区域用：那一块是 WebGL 实时帧，两次渲染本来就不可能逐像素相同
    （它也不该相同 —— 它是活的）。矩形一律取该页的 data-lab-rect，**逐页豁免**，
    不是整页放行：canvas 之外的每一个像素照旧逐点比对。
    取值：python3 - <<'X' 之类的手抄很容易漂 —— 直接从产物里读：
      grep -o 'data-lab-rect="[^"]*"' public/decks/convoai-lab.html
用法：
    python3 scripts/compare-frames.py a.png b.png
    MASK="120,282,1680,580" python3 scripts/compare-frames.py a.png b.png
"""
import os
import sys
from PIL import Image, ImageChops, ImageDraw

a, b = Image.open(sys.argv[1]).convert('RGB'), Image.open(sys.argv[2]).convert('RGB')
masks = [tuple(int(float(v)) for v in r.split(',')) for r in os.environ.get('MASK', '').split(';') if r.strip()]
for im in (a, b):
    d = ImageDraw.Draw(im)
    for (x, y, w, h) in masks:
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(0, 0, 0))
d = ImageChops.difference(a, b)
bbox = d.getbbox()
hist = d.convert('L').histogram()
n = sum(hist[13:])
print('差异像素(>12) %d / %d · bbox %s%s'
      % (n, a.width * a.height, bbox, (' · 已豁免 %d 块 canvas 区' % len(masks)) if masks else ''))
