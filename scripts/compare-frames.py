#!/usr/bin/env python3
"""逐像素比对两张同尺寸截图（配 pinned-diff.mjs 用）：报差异像素数与最大通道差。"""
import sys
from PIL import Image, ImageChops
a, b = Image.open(sys.argv[1]).convert('RGB'), Image.open(sys.argv[2]).convert('RGB')
d = ImageChops.difference(a, b)
bbox = d.getbbox()
hist = d.convert('L').histogram()
n = sum(hist[13:])
print('差异像素(>12) %d / %d · bbox %s' % (n, a.width * a.height, bbox))
