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
MEDIA_ABS = ['/decks/assets/robot26/demo.mp4']
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
