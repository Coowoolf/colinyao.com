#!/usr/bin/env python3
# 终审素材拼版 · convoai-engine「动效全覆盖轮」
#   ① motion-sweep.gif     P8 产品大图动效 GIF（浅色 · ≈2.5s 循环感 · ≤6MB）
#   ② motion-frames.png    P2/P6/P9/P11/P12/P14/P15「双帧同格」拼图
#                          （每格 t=0 与「与 t=0 差异最大」的一帧上下叠 —— 一眼看出真的在动）
#   ③ p13-full-photos.png  P13 修好之后的浅 / 深并置（重点看两块板完整）
#   ④ engine-18p-contact.png  18 × 2（浅/深）全量 contact sheet
# 依赖：/tmp/mo-pNN（shot-motion.mjs 连拍）· /tmp/eng-r22（shot-engine-family.mjs）
# 用法：python3 scripts/eng-motion-sheets.py
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

REV = Path("/home/claude/eco-review"); REV.mkdir(parents=True, exist_ok=True)
SHOTS = Path("/tmp/eng-r22")
TMP = Path("/tmp/eng-r22-cells"); TMP.mkdir(parents=True, exist_ok=True)

FONTS = ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
def font(sz):
    for f in FONTS:
        if Path(f).exists():
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
    return ImageFont.load_default()

BG, INK, SUB, LINE = (22, 22, 26), (240, 240, 245), (150, 150, 160), (64, 64, 72)
PAPER, PINK = (243, 244, 248), (255, 142, 60)


def sheet(cells, cols, cell_w, out, pad=18, lab_h=34, title=None, title_h=0, cell_h=None, fit=False):
    """fit=True：按格宽等比缩放、行高逐行取该行最高的一张（各页裁框长宽比不同，
       统一拉伸会把版面拉变形，统一行高又会留一大片空黑）。"""
    rows = (len(cells) + cols - 1) // cols
    scaled = []
    for p, lab in cells:
        if p is None:
            scaled.append(None); continue
        src = Image.open(p).convert("RGB")
        if fit:
            k = cell_w / src.size[0]
            scaled.append(src.resize((cell_w, max(1, int(src.size[1] * k))), Image.LANCZOS))
        else:
            scaled.append(src.resize((cell_w, cell_h or round(cell_w * 1080 / 1920)), Image.LANCZOS))
    rh = []
    for r in range(rows):
        hs = [im.size[1] for im in scaled[r * cols:(r + 1) * cols] if im is not None]
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
            if scaled[i] is None: continue
            im.paste(scaled[i], (x, y + lab_h))
            d.rectangle([x, y + lab_h, x + cell_w - 1, y + lab_h + scaled[i].size[1] - 1], outline=LINE)
        y += rh[r] + lab_h + pad
    im.save(out); print("·", out, im.size)


# ═══ ① P8 动效 GIF ══════════════════════════════════════════════════════
def p8_gif():
    src = sorted(Path("/tmp/mo-p8").glob("f*.png"))
    box = (120, 268, 1810, 960)                      # 图区（含图例行），去掉页眉与页脚
    ims = []
    for f in src:
        im = Image.open(f).convert("RGB").crop(box)
        w = 900; h = round(w * im.size[1] / im.size[0])
        ims.append(im.resize((w, h), Image.LANCZOS)
                   .quantize(colors=96, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG))
    out = REV / "motion-sweep.gif"
    ims[0].save(out, save_all=True, append_images=ims[1:], duration=95, loop=0, optimize=True)
    print("·", out, "%d 帧 · %.2f MB" % (len(ims), out.stat().st_size / 1e6))


# ═══ ② 双帧同格 ═════════════════════════════════════════════════════════
# 每页裁一块「动效落点最密」的区域：整幅缩进格子里时位移只有几像素，裁紧了才看得出在动。
ROI = {
    2:  ((140, 285, 1600, 745),  "P2 决策环 · 主流 flow-packet 顺时针 / 反馈弧 cycle 反向 / 判断节点 breathe"),
    6:  ((120, 288, 1810, 812),  "P6 实时语音链路 · 盒链接头 flow-packet 左→右（恒速）/ AI-VAD breathe / 支路 dash-drift"),
    9:  ((120, 278, 1810, 652),  "P9 优雅打断 · 因果链 pulse 三连（说话→插话→收声）/ 快路径 flow-packet"),
    11: ((120, 288, 1240, 792),  "P11 弱网 · 语音包雨 dash-drift 下落 / 缓存条蓄放呼吸 / 下带 flow-packet / 断网 ✕ pulse"),
    12: ((120, 290, 1810, 748),  "P12 多模态 · 两条加重主脊 flow-packet（IN 向 hub / OUT 离 hub）/ hub breathe"),
    14: ((120, 272, 1810, 820),  "P14 开放编排 · 左右插入总线 flow-packet 收敛向引擎 / ⇄ 换装极轻 pulse / 引擎 breathe"),
    15: ((120, 264, 1810, 848),  "P15 接入架构 · ①②③ 握手按序 pulse / ③ 媒体流双向 flow-packet"),
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
    w = a.size[0]; h = a.size[1]
    im = Image.new("RGB", (w, h * 2 + 46), PAPER)
    d = ImageDraw.Draw(im)
    im.paste(a, (0, 0)); im.paste(b, (0, h + 46))
    d.rectangle([0, 0, w - 1, h - 1], outline=(200, 202, 212))
    d.rectangle([0, h + 46, w - 1, h * 2 + 45], outline=(200, 202, 212))
    d.rectangle([0, h + 6, w - 1, h + 40], fill=(255, 255, 255))
    d.rectangle([0, h + 6, 6, h + 40], fill=PINK)
    d.text((16, h + 12), "▲ t = 0.00s      ▼ t = %.2fs（差异最大的一帧 · %d 帧连拍中选出）"
           % (bi * 0.13, len(fs)), font=font(22), fill=(60, 62, 72))
    p = TMP / ("pair-p%d.png" % page); im.save(p)
    return p, im.size


# ═══ 出图 ═══════════════════════════════════════════════════════════════
p8_gif()

cells, sizes = [], []
for pg in (2, 6, 9, 11, 12, 14, 15):
    p, sz = pair_cell(pg)
    cells.append((p, ROI[pg][1])); sizes.append(sz)
CW = 900
sheet(cells, 2, CW, REV / "motion-frames.png", title_h=52, fit=True,
      title="convoai-engine · 动效全覆盖轮 · 七页「双帧同格」（同一页两帧上下叠 —— 看得出动了）")

sheet([(SHOTS / "p13-light.png", "P13 · 图左 / 规格右重排 · 浅色 —— 两块板四边完整（4G 天线顶端 + 板底排线全在画内）"),
       (SHOTS / "p13-dark.png",  "P13 · 深色 —— 同一版式，实拍不翻色")],
      1, 1500, REV / "p13-full-photos.png", title_h=52, fit=True,
      title="convoai-engine · P13 产品图完整显示（旧版 620×296 cover 裁切 → 新版 380×510 图窗 · 由高定标）")

cs = []
for i in range(1, 19):
    for th in ("light", "dark"):
        cs.append((SHOTS / ("p%02d-%s.png" % (i, th)), "P%d · %s" % (i, th)))
sheet(cs, 4, 760, REV / "engine-18p-contact.png", title_h=46,
      title="convoai-engine · 18 页 × 浅/深 全量 contact sheet（2026-08-21 动效全覆盖轮后）")
