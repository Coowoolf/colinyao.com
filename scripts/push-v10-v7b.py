#!/usr/bin/env python3
"""V10（浅底→暗底注入，/cowork）+ 三年母版 V7B 最新稿（紫→品红重上色 + 双主题，替换 /3years）
   + 全站 deck title 体检：统一为 声网 AI 产品负责人（Head of AI Products, Agora）"""
import re, glob, pathlib

U = pathlib.Path("/mnt/user-data/uploads/Documents/Colin_Knowledge_Vault/07-个人品牌与成长/演讲档案")
OUT = pathlib.Path("public/decks")

CJK = "-apple-system,'PingFang SC','MiSans','HarmonyOS Sans SC','Source Han Sans SC','Noto Sans SC','Microsoft YaHei'"

TITLE_FIXES = [
    ("声网 AI RTE 产品线负责人", "声网 AI 产品负责人"),
    ("AI RTE 产品线负责人", "AI 产品负责人"),
    ("声网 AI 产品线负责人", "声网 AI 产品负责人"),
    ("声网 ConvoAI 产品负责人", "声网 AI 产品负责人"),
]

def fix_titles(s: str) -> tuple[str, int]:
    n = 0
    for a, b in TITLE_FIXES:
        c = s.count(a)
        if c:
            s = s.replace(a, b)
            n += c
    return s, n

# ============ 1. V10 → /cowork（浅底源，套演讲 deck 管线） ============
FONTS = """<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-700.woff2') format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Satoshi';src:url('/fonts/Satoshi-900.woff2') format('woff2');font-weight:900;font-display:swap;}
</style>
"""
DARK = open("scripts/_dark_block.css", encoding="utf-8").read() if pathlib.Path("scripts/_dark_block.css").exists() else """
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
BOOT = "<script>try{if(localStorage.getItem('colin-theme')==='light')document.documentElement.removeAttribute('data-theme')}catch(e){}</script>"
SWAP_LIGHTBASE = """
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

s = (U / "V10_从被托付到共事_浅底.html").read_text(encoding="utf-8")
s = s.replace('<html lang="zh-CN">', '<html lang="zh-CN" data-theme="dark">', 1)
s = s.replace("<head>", "<head>\n<meta name=\"robots\" content=\"noindex, nofollow\">" + BOOT, 1)
s = re.sub(r'<link[^>]*(fonts\.googleapis|fonts\.gstatic|fontshare)[^>]*>\n?', "", s)
s = s.replace("<style>", FONTS + "<style>", 1)
s = re.sub(r"--f-cn:[^;]*;", f"--f-cn:{CJK},sans-serif;", s)
s = re.sub(r"--f-en:[^;]*;", "--f-en:'Satoshi',-apple-system,'PingFang SC',sans-serif;", s)
s = re.sub(r"--f-mono:[^;]*;", "--f-mono:'JetBrains Mono','SF Mono',ui-monospace,'PingFang SC',monospace;", s)
m = re.search(r"(:root\{.*?\n\})", s, re.S)
assert m, "V10 theme root not found"
s = s[: m.end()] + DARK + s[m.end():]
s = s.replace("</body>", SWAP_LIGHTBASE + "</body>", 1)
s, n10 = fix_titles(s)
(OUT / "cowork.html").write_text(s, encoding="utf-8")
print(f"/cowork    {s.count(chr(99)+'lass=' + chr(34) + 'slide')} slides-ish  title-fixes:{n10}  {len(s)//1024}KB")

# ============ 2. V7B 最新稿 → /3years（紫→品红 + 双主题 + 属性选择器浅底覆写） ============
v = (U / "草稿/三年母版_deck_V7B.html").read_text(encoding="utf-8")
v = v.replace("<head>", "<head>\n<meta name=\"robots\" content=\"noindex, nofollow\">", 1)
v = re.sub(r'<link[^>]*(fonts\.googleapis|fonts\.gstatic|fontshare)[^>]*>\n?', "", v)
v = v.replace("'Noto Sans SC'", CJK.replace("'Noto Sans SC',", "") and "-apple-system,'PingFang SC','MiSans','HarmonyOS Sans SC','Source Han Sans SC','Noto Sans SC'")
# 紫 → 品红家族（rgba 先行，避免半截替换）
RECOLOR = [
    ("rgba(168,85,247,", "rgba(229,49,112,"),
    ("rgba(255,192,0,", "rgba(255,176,32,"),
    ("#a855f7", "#e53170"),
    ("#c9a6ff", "#f27ba1"),
    ("#7c5fc0", "#be185d"),
    ("#ffc000", "#ffb020"),
]
for a, b in RECOLOR:
    v = v.replace(a, b)

LIGHT_V7B = """
/* LIGHT · V7B 家族浅底：token 取自 colin-deck-light（品红→信号粉 / 暖金→暖橙） */
html[data-theme="light"]{
  --stage-bg:#e2e3e8; --slide-bg:#eff0f3;
  --white:#0d0d0d; --t2:#2a2a2a; --t3:#7a7a83; --t4:#8b8b93;
  --panel:#fffffe; --border:rgba(13,13,13,.16);
  --purple:#d9376e; --purple-light:#b8215a; --purple-deep:#b8215a; --purple-soft:rgba(217,55,110,.10);
  --gold:#ff8e3c; --gold-soft:rgba(255,142,60,.12);
  --link:#2a2a2a;
  --glowP:rgba(217,55,110,.22); --glowG:rgba(255,142,60,.22);
}
/* SVG 演示属性权重为 0：浅底用属性选择器覆写品红/暖金字面量 */
html[data-theme="light"] [fill="#e53170"]{fill:#d9376e;}
html[data-theme="light"] [stroke="#e53170"]{stroke:#d9376e;}
html[data-theme="light"] [fill="#f27ba1"]{fill:#b8215a;}
html[data-theme="light"] [stroke="#f27ba1"]{stroke:#b8215a;}
html[data-theme="light"] [fill="#be185d"]{fill:#b8215a;}
html[data-theme="light"] [stroke="#be185d"]{stroke:#b8215a;}
html[data-theme="light"] [fill="#ffb020"]{fill:#ff8e3c;}
html[data-theme="light"] [stroke="#ffb020"]{stroke:#ff8e3c;}
html[data-theme="light"] [stop-color="#e53170"]{stop-color:#d9376e;}
html[data-theme="light"] [stop-color="#ffb020"]{stop-color:#ff8e3c;}
html[data-theme="light"] [stop-color="#f27ba1"]{stop-color:#b8215a;}
"""
mv = re.search(r"(:root\{.*?\n\})", v, re.S)
assert mv, "V7B root not found"
v = v[: mv.end()] + LIGHT_V7B + v[mv.end():]

SWAP_DARKBASE = SWAP_LIGHTBASE.replace(
    "if(t==='light'){document.documentElement.removeAttribute('data-theme');b.textContent='暗底';}\n    else{document.documentElement.setAttribute('data-theme','dark');b.textContent='浅底';}",
    "if(t==='light'){document.documentElement.dataset.theme='light';b.textContent='暗底';}\n    else{delete document.documentElement.dataset.theme;b.textContent='浅底';}"
).replace("--f-mono", "--f-mono, monospace")
v = v.replace("</body>", SWAP_DARKBASE + "</body>", 1)
v, n7 = fix_titles(v)
(OUT / "3years.html").write_text(v, encoding="utf-8")
print(f"/3years    {v.count('class=' + chr(34) + 'slide')} slides  title-fixes:{n7}  {len(v)//1024}KB  residual-purple:{v.count('#a855f7')+v.count('#c9a6ff')}")

# ============ 3. 全站 deck title 体检 ============
report = {}
for f in sorted(glob.glob("public/decks/*.html")):
    if f.endswith(("cowork.html", "3years.html")):
        continue
    t = open(f, encoding="utf-8").read()
    t2, n = fix_titles(t)
    if n:
        open(f, "w", encoding="utf-8").write(t2)
        report[pathlib.Path(f).stem] = n
print("TITLE FIXES:", report, "total", sum(report.values()))
