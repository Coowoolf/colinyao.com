#!/usr/bin/env python3
"""Bake a deck HTML into a self-contained archive: inline /decks/assets/* and /fonts/* as data URLs."""
import re, base64, sys, pathlib

ROOT = pathlib.Path('/home/claude/colinyao.com/public')
MIME = {'.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.jpeg':'image/jpeg',
        '.svg':'image/svg+xml','.woff2':'font/woff2','.woff':'font/woff','.gif':'image/gif'}

# ── 大体积媒体：不内联，换成线上绝对地址（robot26 归档同款处理）───────────────
#   convoai-engine P20 的无人机秀是 3.1MB 的 mp4，base64 之后 4.2MB，
#   塞进归档等于把一份「发给客户的单文件」撑到 6MB 以上，还只为了离线播一支片子。
#   归档里改成绝对地址：在线打开照播，离线打开退回**已内联的 poster**（整幅静帧，不是空洞）。
#   实现走「先打码、最后还原」而不是直接替换 —— 直接替换的话，
#   https://colinyao.com/decks/assets/... 的尾巴仍然匹配资产内联的正则，
#   会被当成本地资产再内联一次，拼出 https://colinyao.com + dataURL 的鬼东西。
#   2026-08-31 LAB 家族：three.js 三件（合计 750KB）同理走这条路 ——
#   base64 之后 1MB，塞进归档只为了离线转几颗球，不值。归档里改绝对地址。
#   ── 归档态的准确口径（这一条写进归档头注释，别让人以为「离线 = 残页」）──
#     在线打开：七枚 WebGL 场景照常起（P1 声场球 / P4 双向声带 / P7 声学地形 /
#       P9 双层防御壳 / P17 五脑区大脑 / P18 复利螺旋 / P21 SD-RTN 地球）。
#     离线打开：three 拉不到 ⇒ 前奏里的 6s 看门狗把七页钉死在 poster 上，
#       而这七页的 poster **就是页上原来那张 SVG**（P1/P21 是构建期离线投影出的
#       专用静帧，另五页是各页图形原地留用）—— 于是离线归档 = **完整的 2D 版 22 页**，
#       一个字、一张图都不少。不是「缺了 3D 的残页」，是「这份 deck 的 2D 形态」。
#   ⚠ three.core.min.js 不出现在 HTML 里（是 three.module.min.js 自己 import 的），
#     列在这儿只为备案；masking 找不到就跳过，不影响 miss=[]。
#   ⚠ importmap 里**不许**出现 `three/addons/` → `/decks/assets/three/` 这种目录映射：
#     裸目录路径会被资产内联正则当成一枚资产去找，suffix 为空 ⇒ 稳报一条 miss。
#     OrbitControls 一律写全路径（builder 已经这么写了）。
MEDIA_ABS = ['/decks/assets/robot26/demo.mp4',
             '/decks/assets/three/three.module.min.js',
             '/decks/assets/three/three.core.min.js',
             '/decks/assets/three/OrbitControls.js']
SITE = 'https://colinyao.com'
def mask_media(html):
    for k, ref in enumerate(MEDIA_ABS):
        html = html.replace(ref, '@@MEDIA%d@@' % k)     # 占位符不含 & 与 " ⇒ 过得了 srcdoc 转义
    return html
def unmask_media(html):
    for k, ref in enumerate(MEDIA_ABS):
        html = html.replace('@@MEDIA%d@@' % k, SITE + ref)
    return html

def inline_assets(html):
    """把 /decks/assets|/fonts 引用内联为 data URL（bake 与 srcdoc 共用）。"""
    html = mask_media(html)          # 大体积媒体先打码，别让它进内联清单
    for ref in sorted(set(re.findall(r'/(?:decks/assets|fonts)/[^"\'\)\s>]+', html)), key=len, reverse=True):
        p = ROOT / ref.lstrip('/')
        mime = MIME.get(p.suffix.lower())
        if p.exists() and mime:
            html = html.replace(ref, 'data:%s;base64,%s' % (mime, base64.b64encode(p.read_bytes()).decode()))
    return html

def inline_engine_iframe(html):
    """convoai-info 的引擎抽屉：归档态把 iframe 改 srcdoc 内联（srcdoc 继承父源，
    离线可展开且 Esc 键路由照常；drawer JS 已有无 data-src 守卫）。
    注意顺序：引擎文档必须**先内联资产、再转义**——先转义会把 src="…" 变成
    &quot; 包裹，外层资产内联正则识别不到（2026-08-21 P14 案例图漏内联实锤）。"""
    marker = 'data-src="/decks/convoai-engine.html"'
    if marker not in html:
        return html
    eng = (ROOT / 'decks/convoai-engine.html').read_text(encoding='utf-8')
    eng = inline_assets(eng)
    esc = eng.replace('&', '&amp;').replace('"', '&quot;')
    return html.replace(marker, 'srcdoc="%s"' % esc)

def bake(src, dst):
    html = pathlib.Path(src).read_text(encoding='utf-8')
    html = inline_engine_iframe(html)
    html = mask_media(html)
    refs = sorted(set(re.findall(r'/(?:decks/assets|fonts)/[^"\')\s>]+', html)), key=len, reverse=True)
    miss = []
    for ref in refs:
        p = ROOT / ref.lstrip('/')
        if not p.exists():
            miss.append(ref); continue
        mime = MIME.get(p.suffix.lower())
        if not mime:
            miss.append(ref+' (mime?)'); continue
        data = 'data:%s;base64,%s' % (mime, base64.b64encode(p.read_bytes()).decode())
        html = html.replace(ref, data)
    html = unmask_media(html)
    # left 的正则要放过已绝对化的媒体（它的尾巴长得跟本地资产一模一样）
    left = re.findall(r'(?<!colinyao\.com)/(?:decks/assets|fonts)/[^"\')\s>]+', html)
    ext = re.findall(r'(?:src|href)="https?://[^"]+"', html)
    media_out = [m for m in MEDIA_ABS if (SITE + m) in html]
    pathlib.Path(dst).write_text(html, encoding='utf-8')
    print(f'{dst}: {len(refs)-len(miss)} inlined, miss={miss}, left={len(left)}, '
          f'ext={ext[:5]}, media→线上={media_out}, size={pathlib.Path(dst).stat().st_size:,}')

bake(ROOT/'decks/convoai-info.html', '/home/claude/eco-review/convoai-info-速讲版-8p.html')
# 2026-08-21 Colin：31 页初次拜访版退役下线，本清单只剩速讲版一行（终版归档已在 Vault）。
# 2026-08-24：新增 ELI5 版。它只引一张 R1 实拍 webp（34KB）与四张字体，没有大体积媒体、
#   没有 iframe 抽屉 —— 一次直白的内联，miss=[] / left=0 就是它的验收线。
bake(ROOT/'decks/convoai-eli5.html', '/home/claude/eco-review/convoai-eli5-讲给五岁的你-11p.html')
# 2026-08-30：贷后催收方案 deck（私享 /convoai-postloan）。全 SVG 作图、零位图资产 ——
#   只引四张字体与两组背景板 PNG，没有大体积媒体、没有 iframe 抽屉。
#   miss=[] / left=0 就是它的验收线（这份归档要能离线发给金融机构，一格图都不能掉）。
bake(ROOT/'decks/convoai-postloan.html', '/home/claude/eco-review/convoai-postloan-贷后催收方案-15p.html')
# 2026-08-30：同一份 deck 的东南亚英文版（私享 /convoai-postloan-en）。资产口径与中文版
#   一模一样（四张字体 + 两组背景板 PNG，全 SVG 作图、零位图、无 iframe 抽屉），
#   miss=[] / left=0 同样是它的验收线 —— 这份要能离线发给越南的银行，一格图都不能掉。
#   ⚠ 归档态里左下角那枚语言钮点了会指向 /decks/convoai-postloan.html：
#     单文件离线打开时对方 deck 不在身边，跳转必然落空。这是「单文件归档」的固有边界，
#     不是 bug —— 在线版（colinyao.com/convoai-postloan-en）互跳照常。
bake(ROOT/'decks/convoai-postloan-en.html', '/home/claude/eco-review/convoai-postloan-EN-SEA-15p.html')
# 2026-08-31：LAB 家族生产首秀（私享 /convoai-lab）。引擎 22 页的 LAB 演绎 ——
#   两枚 WebGL 主视觉页（P1 声场球 / P21 SD-RTN 地球）+ 其余 20 页与引擎逐字节同源。
#   资产口径：四张字体 + 两组背景板 PNG + 跨引用 robot26 的两张 R1 实拍与 OpenAI 双源 logo
#   （P20 的 demo.mp4 与 three 三件走 MEDIA_ABS）。
#   验收线：miss=[] / left=0 / media→线上 里同时出现 demo.mp4 与 three 两件。
#   ⚠ 归档离线打开时 P1/P21 是 **poster 静帧**（three 拉不到 ⇒ 6s 看门狗钉死 poster），
#     其余 20 页完整。这是「单文件归档 + 750KB 库」的固有边界，不是 bug；
#     在线打开（colinyao.com/convoai-lab）两颗球照转。
bake(ROOT/'decks/convoai-lab.html', '/home/claude/eco-review/convoai-lab-引擎深入讲解-LAB-22p.html')
