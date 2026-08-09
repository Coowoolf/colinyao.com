#!/usr/bin/env python3
"""演讲Deck 批处理：浅底源文件 → 单文件双主题（默认暗底，跟随全站 colin-theme）。
处理：noindex + 字体本地化 + 注入暗底 token 块（严格取自 colin-deck-dark reference/theme.css）
     + <html data-theme="dark"> 预置 + head 主题引导 + 左下角切换按钮。"""
import re, sys, pathlib

SRC = pathlib.Path("/mnt/user-data/uploads/Documents/Colin_Knowledge_Vault/07-个人品牌与成长/演讲Deck")
OUT = pathlib.Path("/home/claude/colinyao.com/public/decks")

# slug 映射（对应 talks.ts 编号；13 为圆桌主持无 deck）
DECKS = {
    "01-RTE大会-生成式AI驱动实时互动-浅底.html": "rte24",
    "02-人人都是PM-生成式AI驱动实时互动-浅底.html": "pm24",
    "03-ConvoAI产品发布会-浅底.html": "convoai",
    "04-中国网络视听大会-对话式AI驱动音频体验革新-浅底.html": "audio25",
    "05-全球产品经理大会-Agent交互核心引擎-浅底.html": "engine25",
    "06-ConvoAI与RTE-重塑实时体验的第三纪元-浅底.html": "era3",
    "07-ConvoAI与RTE-ProductionReady全栈发布-浅底.html": "prodready",
    "08-人人都是PM2025-活人感与体验基准-浅底.html": "pm25",
    "09-FirstPrompt新加坡-NoMorePrompts-浅底.html": "vibecheck",
    "10-VoiceAgent闭门会-VibeSOTA-浅底.html": "vibesota",
    "11-中国网络视听大会-RTE与AI双引擎-浅底.html": "dual26",
    # robot26 现役 = 北京站 PPT 一比一还原（build-robot26-bj.py 生成），
    # 这条 Vault 源是 0516 深圳浅底稿，落到归档件，避免批处理覆盖现役产物。
    "12-RTE春夏巡游深圳-从玩具到伙伴-浅底.html": "robot26-v0516",
    "14-GoogleCloud开发者大会-从对话式AI到企业级智能体-浅底.html": "gcloud",
    "15-AWS中国峰会-被记住被托付-浅底.html": "aws26",
}

FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>
"""

# 暗底 override —— token 严格取自 colin-deck-dark reference/theme.css
DARK = """
/* DARK · token 严格取自 colin-deck-dark reference/theme.css */
html[data-theme="dark"]{
  --stage-bg:#07070b;
  --slide-bg:#0f0e17;
  --card-bg:#16151f;
  --card-bg-2:#1c1b26;
  --cardw-bg:#fffffe;
  --cardw-ink:#0f0e17;
  --cardw-ink2:#3d3d4e;
  --cardw-tag:#8a8aa0;
  --cardw-am:#c2410c;
  --cardw-co:#d1392a;
  --file-bg:#0a0910;
  --hair:rgba(255,255,254,.10);
  --hair-soft:rgba(255,255,254,.055);
  --hair-strong:rgba(255,255,254,.20);
  --ink:#fffffe;
  --ink-2:#a7a9be;
  --ink-3:#6f7186;
  --amber:#ff8906;
  --coral:#f25f4c;
  --magenta:#e53170;
  --mq:#f25f4c;
  --mq-2:#ff8906;
  --flow-line:rgba(255,137,6,.30);
  --flow-line-2:rgba(255,255,254,.16);
  --flow-op:.42;
  --on-bg:linear-gradient(180deg,rgba(255,137,6,.075),rgba(255,137,6,.02));
  --warn-bg:linear-gradient(180deg,rgba(242,95,76,.075),rgba(242,95,76,.02));
}
"""

BOOT = """<script>try{if(localStorage.getItem('colin-theme')==='light')document.documentElement.removeAttribute('data-theme')}catch(e){}</script>"""

SWAP = """
<style>
.deck-swap{position:fixed;left:26px;bottom:22px;z-index:1000;
  font-family:var(--f-mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-3);border:1px solid var(--hair);border-radius:2px;
  padding:7px 13px;opacity:.5;transition:opacity .3s,color .3s,border-color .3s;
  background:transparent;cursor:pointer;}
.deck-swap:hover{opacity:1;color:var(--amber);border-color:var(--amber);}
@media print{.deck-swap{display:none!important;}}
</style>
<button class="deck-swap" id="deckSwap">浅底</button>
<script>
(function(){
  var b=document.getElementById('deckSwap');
  function apply(t){
    if(t==='light'){document.documentElement.removeAttribute('data-theme');b.textContent='暗底';}
    else{document.documentElement.setAttribute('data-theme','dark');b.textContent='浅底';}
  }
  var cur='dark';
  try{cur=localStorage.getItem('colin-theme')||'dark';}catch(e){}
  apply(cur);
  b.addEventListener('click',function(){
    cur=(cur==='dark')?'light':'dark';
    try{localStorage.setItem('colin-theme',cur);}catch(e){}
    apply(cur);
  });
})();
</script>
"""

F_CN = "-apple-system,'PingFang SC','MiSans','HarmonyOS Sans SC','Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif"
F_EN = "'Satoshi',-apple-system,'PingFang SC',sans-serif"
F_MONO = "'JetBrains Mono','SF Mono',ui-monospace,'PingFang SC',monospace"

def process(src: pathlib.Path, hrefmap=None) -> str:
    s = src.read_text(encoding="utf-8")
    # 1. html 标签预置暗底（无闪烁）
    s = s.replace('<html lang="zh-CN">', '<html lang="zh-CN" data-theme="dark">', 1)
    # 2. head: noindex + 主题引导（偏好浅底则立即摘掉 data-theme）
    s = s.replace("<head>", "<head>\n<meta name=\"robots\" content=\"noindex, nofollow\">" + BOOT, 1)
    # 3. 剥掉全部外部字体请求（preconnect + googleapis + fontshare）
    s = re.sub(r'<link[^>]*(fonts\.googleapis|fonts\.gstatic|fontshare)[^>]*>\n?', "", s)
    # 4. 本地字体块放在第一个 <style> 前
    s = s.replace("<style>", FONTS + "<style>", 1)
    # 5. 字体栈替换为系统栈 + 自托管
    s = re.sub(r"--f-cn:[^;]*;", f"--f-cn:{F_CN};", s)
    s = re.sub(r"--f-en:[^;]*;", f"--f-en:{F_EN};", s)
    s = re.sub(r"--f-mono:[^;]*;", f"--f-mono:{F_MONO};", s)
    # 6. 第一个 :root{...}（THEME 浅底块）后注入暗底 override
    m = re.search(r"(:root\{.*?\n\})", s, re.S)
    assert m, f"{src.name}: theme :root not found"
    s = s[: m.end()] + DARK + s[m.end():]
    # 7. 索引页改写卡片链接
    if hrefmap:
        for fname, slug in hrefmap.items():
            s = s.replace(f'href="{fname}"', f'href="/{slug}"')
    # 8. 尾部切换按钮
    s = s.replace("</body>", SWAP + "</body>", 1)
    return s

report = []
for fname, slug in DECKS.items():
    out = OUT / f"{slug}.html"
    html = process(SRC / fname)
    n = html.count('class="slide')
    out.write_text(html, encoding="utf-8")
    report.append((slug, fname, n, len(html)))

# 合集索引页 → talkdecks.html（卡片链接改写为 /slug 路由）
idx = process(SRC / "index.html", hrefmap=DECKS)
idx = idx.replace('<span class="date"></span>', '<span class="date">2026 H1</span>')  # 09 补日期
(OUT / "talkdecks.html").write_text(idx, encoding="utf-8")

for slug, fname, n, size in report:
    print(f"/{slug:<10} {n:>2} slides  {size//1024}KB  ← {fname}")
print(f"/talkdecks  index  {len(idx)//1024}KB")

# 校验：每个产物 dark 块存在、无外部字体、noindex、swap 齐备
bad = []
for f in list(OUT.glob("*.html")):
    t = f.read_text(encoding="utf-8")
    if f.stem in [s for s, *_ in report] or f.stem == "talkdecks":
        checks = {
            "dark-block": 'html[data-theme="dark"]' in t,
            "no-ext-fonts": "googleapis" not in t and "fontshare" not in t,
            "noindex": 'name="robots"' in t,
            "swap": 'id="deckSwap"' in t,
            "boot": "colin-theme" in t.split("</head>")[0],
        }
        fails = [k for k, v in checks.items() if not v]
        if fails:
            bad.append((f.name, fails))
print("VERIFY:", "ALL OK" if not bad else bad)
