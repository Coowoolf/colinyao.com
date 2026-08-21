#!/usr/bin/env python3
"""Bake a deck HTML into a self-contained archive: inline /decks/assets/* and /fonts/* as data URLs."""
import re, base64, sys, pathlib

ROOT = pathlib.Path('/home/claude/colinyao.com/public')
MIME = {'.png':'image/png','.webp':'image/webp','.jpg':'image/jpeg','.jpeg':'image/jpeg',
        '.svg':'image/svg+xml','.woff2':'font/woff2','.woff':'font/woff','.gif':'image/gif'}

def inline_assets(html):
    """把 /decks/assets|/fonts 引用内联为 data URL（bake 与 srcdoc 共用）。"""
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
    left = re.findall(r'/(?:decks/assets|fonts)/[^"\')\s>]+', html)
    ext = re.findall(r'(?:src|href)="https?://[^"]+"', html)
    pathlib.Path(dst).write_text(html, encoding='utf-8')
    print(f'{dst}: {len(refs)-len(miss)} inlined, miss={miss}, left={len(left)}, ext={ext[:5]}, size={pathlib.Path(dst).stat().st_size:,}')

bake(ROOT/'decks/convoai-info.html', '/home/claude/eco-review/convoai-info-速讲版-8p.html')
bake(ROOT/'decks/convoai-visit.html', '/home/claude/eco-review/convoai-初次拜访版-31p.html')
