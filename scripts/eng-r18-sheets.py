#!/usr/bin/env python3
# 终审素材拼版 · convoai-engine「收束轮 20 → 18 页」
#   ① r18-review.png          2×3 带标签：P13 浅/深 · P18 浅/深 · P10 动效双帧 · deckSwap 常显特写
#   ② p10-motion.gif          P10 常驻动效循环（浅色 · ≤6MB）
#   ③ engine-18p-contact.png  18 × 2（浅/深）全量 contact sheet
# 依赖：/tmp/eng-r18-full（shot-engine-family.mjs）· /tmp/p10-gif（shot-p10-motion.mjs）
# 用法：python3 scripts/eng-r18-sheets.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REV = Path("/home/claude/eco-review"); REV.mkdir(parents=True, exist_ok=True)
SHOTS = Path("/tmp/eng-r18-full")
GIFSRC = Path("/tmp/p10-gif")
TMP = Path("/tmp/eng-r18-cells"); TMP.mkdir(parents=True, exist_ok=True)

FONTS = ["/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
         "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
def font(sz):
    for f in FONTS:
        if Path(f).exists():
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
    return ImageFont.load_default()

BG, INK, SUB, LINE = (22, 22, 26), (240, 240, 245), (150, 150, 160), (64, 64, 72)

def sheet(cells, cols, cell_w, out, pad=18, lab_h=34, title=None, title_h=0):
    cell_h = round(cell_w * 1080 / 1920)
    rows = (len(cells) + cols - 1) // cols
    im = Image.new("RGB", (pad + cols * (cell_w + pad),
                           pad + title_h + rows * (lab_h + cell_h + pad)), BG)
    d = ImageDraw.Draw(im)
    if title:
        d.text((pad + 2, pad + 4), title, font=font(26), fill=INK)
    for i, (p, lab) in enumerate(cells):
        r, c = divmod(i, cols)
        x = pad + c * (cell_w + pad); y = pad + title_h + r * (lab_h + cell_h + pad)
        d.text((x + 2, y + 6), lab, font=font(19), fill=INK)
        if p is None: continue
        im.paste(Image.open(p).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS), (x, y + lab_h))
        d.rectangle([x, y + lab_h, x + cell_w - 1, y + lab_h + cell_h - 1], outline=LINE)
    im.save(out); print("·", out, im.size)

# ── ① 之一：P10 动效双帧拼一格（间隔 ~0.5s，肉眼可比：dash 位移 / ✕ 明暗 / 光晕半径）──
def p10_pair():
    # 只裁「双层防御环」那一坨（fig viewBox 与像素 1:1，环心 300,196 / 外环 r138）：
    # 整幅缩到格子里时动效差异只有几像素，裁紧了才看得出「真的在动」。
    box = (60, 20, 500, 420)
    a = Image.open(GIFSRC / "f00.png").convert("RGB").crop(box)
    b = Image.open(GIFSRC / "f06.png").convert("RGB").crop(box)   # 相隔 0.42s，逐帧差最大的一对
    cw = 820; ch = round(cw * a.size[1] / a.size[0])
    im = Image.new("RGB", (1920, 1080), (243, 244, 248))
    d = ImageDraw.Draw(im)
    for k, (src, lab) in enumerate(((a, "t = 0.00s"), (b, "t = 0.42s"))):
        x = 120 + k * (cw + 40); y = (1080 - ch) // 2 + 40
        im.paste(src.resize((cw, ch), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + cw - 1, y + ch - 1], outline=(196, 198, 208))
        d.text((x + 4, y - 34), lab, font=font(26), fill=(90, 92, 104))
    d.text((30, 34), "P10 双层防御环 · 常驻动效（同一页相隔 ~0.5s 的两帧）",
           font=font(30), fill=(40, 42, 52))
    d.text((30, 78), "环上 dash 绕圈爬 · 干扰点线错峰漂移 · ✕ 脉冲 · 目标人声能量包奔向中心 · 智能体呼吸光晕",
           font=font(24), fill=(110, 112, 124))
    p = TMP / "p10-pair.png"; im.save(p); return p

# ── ① 之二：deckSwap 常显 chip 特写（浅 / 深 左下角 1:1 放大）──
def swap_chip():
    im = Image.new("RGB", (1920, 1080), BG); d = ImageDraw.Draw(im)
    d.text((40, 40), "deckSwap 主题键 · 默认可见（opacity .62 · hover/focus 1）",
           font=font(34), fill=INK)
    d.text((40, 92), "Colin：「没有浅色切换的键」——本 deck 常被直接发链接，切换键不能藏在 hover 里",
           font=font(24), fill=SUB)
    for k, th in enumerate(("light", "dark")):
        crop = Image.open(SHOTS / ("p01-%s.png" % th)).convert("RGB").crop((0, 1004, 220, 1078))
        big = crop.resize((crop.size[0] * 4, crop.size[1] * 4), Image.LANCZOS)
        x, y = 80 + k * (big.size[0] + 120), 260
        im.paste(big, (x, y))
        d.rectangle([x, y, x + big.size[0] - 1, y + big.size[1] - 1], outline=LINE)
        d.text((x, y + big.size[1] + 16), "P1 左下角 · %s（4× 放大）" % th, font=font(26), fill=SUB)
    p = TMP / "swap-chip.png"; im.save(p); return p

sheet([
    (SHOTS / "p13-light.png", "P13 · R1 带实拍图重排 · 浅色（robot26 资产跨引用 · 图在上/规格在下）"),
    (SHOTS / "p13-dark.png",  "P13 · 深色（浅色下走「暗媒体卡」发丝内描边，深色直接融进卡面）"),
    (SHOTS / "p18-light.png", "P18 · OpenAI 合作 · 末页 · 浅色（logo 锁定版 + 继承 CTA 行）"),
    (SHOTS / "p18-dark.png",  "P18 · 深色（lt/dk 双 img CSS 显隐 · 白色 wordmark 版）"),
    (p10_pair(),              "P10 · 常驻动效双帧对比 · 浅色"),
    (swap_chip(),             "主题切换键 · 常显 chip（浅 / 深）"),
], 2, 1400, REV / "r18-review.png", title_h=46,
   title="convoai-engine · 收束轮 20→18 · 终审四件（P13 带图重排 / P18 末页 logo / P10 动效 / deckSwap 显形）")

# ── ② P10 动效 GIF ──
frames = sorted(GIFSRC.glob("f*.png"))
ims = [Image.open(f).convert("RGB").resize((600, 392), Image.LANCZOS)
       .quantize(colors=128, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG) for f in frames]
gif = REV / "p10-motion.gif"
ims[0].save(gif, save_all=True, append_images=ims[1:], duration=70, loop=0, optimize=True)
print("·", gif, "%d 帧 · %.2f MB" % (len(ims), gif.stat().st_size / 1e6))

# ── ③ 18 × 2 全量 contact sheet ──
cs = []
for i in range(1, 19):
    for th in ("light", "dark"):
        cs.append((SHOTS / ("p%02d-%s.png" % (i, th)), "P%d · %s" % (i, th)))
sheet(cs, 4, 760, REV / "engine-18p-contact.png", title_h=46,
      title="convoai-engine · 18 页 × 浅/深 全量 contact sheet（2026-08-21 收束轮后）")
