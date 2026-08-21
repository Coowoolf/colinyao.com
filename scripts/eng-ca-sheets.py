#!/usr/bin/env python3
# 终审素材拼版 · convoai-engine「Call Agent 章 + 视频页 18 → 21 → 22 页」
#   ① callagent-motion.png     P17 / P18 两页「双帧同格」（t=0 与差异最大的一帧上下叠）
#   ② engine-22p-contact.png   22 × 2（浅/深）全量 contact sheet
# 浅/深三页全尺寸竖排（callagent-3pages.png / callagent-dark.png）走 scripts/compose-review.py，
# 不在本文件里 —— 那两张要的是 1:1 像素，不缩放。
# 依赖：/tmp/eng-ca（shot-engine-family.mjs）· /tmp/mo-p17 · /tmp/mo-p18（shot-motion.mjs）
# 用法：python3 scripts/eng-ca-sheets.py
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

REV = Path("/home/claude/eco-review"); REV.mkdir(parents=True, exist_ok=True)
SHOTS = Path("/tmp/eng-ca")
TMP = Path("/tmp/eng-ca-cells"); TMP.mkdir(parents=True, exist_ok=True)

FONTS = ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
def font(sz):
    for f in FONTS:
        if Path(f).exists():
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
    return ImageFont.load_default()

BG, INK, LINE = (22, 22, 26), (240, 240, 245), (64, 64, 72)
PAPER, PINK = (243, 244, 248), (255, 142, 60)


def sheet(cells, cols, cell_w, out, pad=18, lab_h=34, title=None, title_h=0, cell_h=None, fit=False):
    rows = (len(cells) + cols - 1) // cols
    scaled = []
    for p, _lab in cells:
        src = Image.open(p).convert("RGB")
        if fit:
            k = cell_w / src.size[0]
            scaled.append(src.resize((cell_w, max(1, int(src.size[1] * k))), Image.LANCZOS))
        else:
            scaled.append(src.resize((cell_w, cell_h or round(cell_w * 1080 / 1920)), Image.LANCZOS))
    rh = []
    for r in range(rows):
        hs = [im.size[1] for im in scaled[r * cols:(r + 1) * cols]]
        rh.append(max(hs) if hs else (cell_h or round(cell_w * 1080 / 1920)))
    im = Image.new("RGB", (pad + cols * (cell_w + pad),
                           pad + title_h + sum(rh) + rows * (lab_h + pad)), BG)
    d = ImageDraw.Draw(im)
    if title:
        d.text((pad + 2, pad + 4), title, font=font(26), fill=INK)
    y = pad + title_h
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            if i >= len(cells): break
            x = pad + c * (cell_w + pad)
            d.text((x + 2, y + 6), cells[i][1], font=font(19), fill=INK)
            im.paste(scaled[i], (x, y + lab_h))
            d.rectangle([x, y + lab_h, x + cell_w - 1, y + lab_h + scaled[i].size[1] - 1], outline=LINE)
        y += rh[r] + lab_h + pad
    im.save(out); print("·", out, im.size)


# ═══ ① 双帧同格（P17 / P18）════════════════════════════════════════════════
# 裁「动效落点最密」的图区：整幅缩进格子里位移只有几像素，裁紧了才看得出在动。
ROI = {
    17: ((120, 282, 1810, 866),
         "P17 五个大脑 · 五条车道 flow-packet 各自速度（2.0/2.3/2.6/2.9/3.2s）= 并行不同步 · "
         "汇聚点 pulse · hot 盒 breathe + halo"),
    18: ((120, 276, 1810, 600),
         "P18 成长飞轮 · 曲线 flow-packet 顺着长 · 基准平线 dash-drift · 反超点 pulse · "
         "2 倍终点 breathe + halo · 右侧四节点 Loop cycle 绕行"),
}
def pair_cell(page):
    box, _ = ROI[page]
    fs = sorted(Path("/tmp/mo-p%d" % page).glob("f*.png"))
    a = Image.open(fs[0]).convert("RGB").crop(box)
    best, bi = -1, 1
    for i, f in enumerate(fs[1:], 1):
        b = Image.open(f).convert("RGB").crop(box)
        n = sum(ImageChops.difference(a, b).convert("L").histogram()[10:])
        if n > best: best, bi = n, i
    b = Image.open(fs[bi]).convert("RGB").crop(box)
    w, h = a.size
    im = Image.new("RGB", (w, h * 2 + 46), PAPER)
    d = ImageDraw.Draw(im)
    im.paste(a, (0, 0)); im.paste(b, (0, h + 46))
    d.rectangle([0, 0, w - 1, h - 1], outline=(200, 202, 212))
    d.rectangle([0, h + 46, w - 1, h * 2 + 45], outline=(200, 202, 212))
    d.rectangle([0, h + 6, w - 1, h + 40], fill=(255, 255, 255))
    d.rectangle([0, h + 6, 6, h + 40], fill=PINK)
    d.text((16, h + 12), "▲ t = 0.00s      ▼ t ≈ %.2fs（差异最大的一帧 · %d 帧连拍中选出）"
           % (bi * 0.13, len(fs)), font=font(22), fill=(60, 62, 72))
    p = TMP / ("pair-p%d.png" % page); im.save(p)
    return p


sheet([(pair_cell(pg), ROI[pg][1]) for pg in (17, 18)], 1, 1500,
      REV / "callagent-motion.png", title_h=52, fit=True,
      title="convoai-engine · Call Agent 章 · P17 / P18 双帧同格（同一页两帧上下叠 —— 看得出动了）")

# ═══ ② 21 页全量 contact sheet ════════════════════════════════════════════
cs = []
for i in range(1, 23):
    for th in ("light", "dark"):
        cs.append((SHOTS / ("p%02d-%s.png" % (i, th)), "P%d · %s" % (i, th)))
sheet(cs, 4, 760, REV / "engine-22p-contact.png", title_h=46,
      title="convoai-engine · 22 页 × 浅/深 全量 contact sheet（2026-08-21 Call Agent 章 + 视频页后 · "
            "新增 P16–P18 ■ 与 P20 ▶ · 场景 → Call Agent → R1 → 无人机秀 DEMO）")
