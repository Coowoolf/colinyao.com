#!/usr/bin/env python3
"""aiot26-v3 → aiot26-conf.html：2026 AI 产品大会 · 声网 AIoT 专场视觉版（35 页）。

   与 scripts/build-conf.py（cowork → cowork-conf）同一套视觉层做法：
   黑底 + 紫系(#9333EA/#A855F7/#C084FC) + 金黄 #FFC000 + 阿里巴巴普惠体 2.0
   + 页头紫 tab / 右上大会 logo + 模板封面 keyart + 章节页 / 观点页版式。

   内容层一个字不改 —— 全部来自 scripts/build-aiot26-v3.py 的产物（35 页 · 五幕）。
   为保证可再生：本脚本先在临时目录里跑一遍 build-aiot26-v3.py 拿到 V3 全文，
   因此 public/decks/aiot26-v3.html 从仓库删除后，本脚本依然能独立重建
   （V3 的两个输入 _src-aiot26-fable35.html / aiot26-v2.html 仍在仓库里）。

   媒体层沿用 V3：P04 视频页（.vstage + 三帧静帧兜底）+ deck-media 按键行为，
   .dm-ind/.vslide 样式 V3 已自带，本脚本的覆盖层不再重复声明。
"""
import os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, "/tmp/conf-tpl")
from assets import LOGO, COVER, VENUE

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── 0) 先在临时目录里重建 V3（不落地到 public/decks，避免复活已下线的路由） ──
def build_v3() -> str:
    tmp = tempfile.mkdtemp(prefix="aiot26-v3-")
    dst = os.path.join(tmp, "public", "decks")
    os.makedirs(dst)
    for f in ("_src-aiot26-fable35.html", "aiot26-v2.html"):
        shutil.copy(os.path.join(REPO, "public", "decks", f), dst)
    subprocess.run([sys.executable, os.path.join(REPO, "scripts", "build-aiot26-v3.py")],
                   cwd=tmp, check=True)
    out = open(os.path.join(dst, "aiot26-v3.html"), encoding="utf-8").read()
    shutil.rmtree(tmp, ignore_errors=True)
    return out


s = build_v3()

# ── 1) 单主题：替换 浅底:root + 暗底 两个 token 块（整块照抄 build-conf.py） ──
i = s.index(":root{")
j = s.index('html[data-theme="dark"]')
k = s.index("}", s.index("--warn-bg", j)) + 1
CONF = """:root{
  --stage-bg:#000000;
  --slide-bg:#000000;
  --card-bg:#131017;
  --card-bg-2:#1b1622;
  --cardw-bg:#ffffff;
  --cardw-ink:#111111;
  --cardw-ink2:#3c3c46;
  --cardw-tag:#8a8aa0;
  --cardw-am:#7E22CE;
  --cardw-co:#B45309;
  --file-bg:#0a0a0d;
  --hair:rgba(255,255,255,.12);
  --hair-soft:rgba(255,255,255,.06);
  --hair-strong:rgba(255,255,255,.24);
  --ink:#ffffff;
  --ink-2:#c9c9d4;
  --ink-3:#A5A5A5;
  --amber:#A855F7;
  --coral:#FFC000;
  --magenta:#C084FC;
  --mq:#ffffff;
  --mq-2:#FFC000;
  --flow-line:rgba(168,85,247,.30);
  --flow-line-2:rgba(255,255,255,.13);
  --flow-op:.4;
  --on-fill:rgba(147,51,234,.16);
  --on-bg:linear-gradient(180deg,rgba(147,51,234,.15),rgba(147,51,234,.04));
  --warn-bg:linear-gradient(180deg,rgba(255,192,0,.10),rgba(255,192,0,.02));
}"""
s = s[:i] + CONF + s[k:]
s = s.replace("""/* ===========================================
   THEME · colin-deck-light
   浅灰白 #eff0f3 + 近黑 #0d0d0d + 暖橙 #ff8e3c
   =========================================== */""",
              """/* ===========================================
   THEME · 2026 AI 产品大会（单主题）
   黑底 #000 + 紫系 #9333EA/#A855F7/#C084FC + 金黄 #FFC000
   =========================================== */""", 1)

# ── 2) 去掉主题引导 / 切换按钮 / V3 后加的 T 键监听（单主题） ────
s = s.replace('<html lang="zh-CN" data-theme="dark">', '<html lang="zh-CN">')
s = re.sub(r"<script>try\{if\(localStorage\.getItem\('colin-theme'\)[^<]*</script>", "", s, count=1)
s = re.sub(r'<button class="deck-swap" id="deckSwap">[^<]*</button>\s*<script>\s*\(function\(\)\{\s*var b=document\.getElementById\(\'deckSwap\'\);.*?\}\)\(\);\s*</script>',
           "", s, flags=re.S, count=1)
# V3 的 T 键切换与「视频页状态机」同处一个 <script>，只切前半段
_T0 = "/* V2 · 按钮隐藏后仍保留双主题切换：T 键 */"
_T1 = "/* V2 · 视频页状态机"
assert s.count(_T0) == 1 and s.count(_T1) == 1, "T 键 / 视频状态机锚点失效"
s = s[:s.index(_T0)] + s[s.index(_T1):]

# ── 3) 字体：普惠体 2.0 优先（观众机无字体时回落苹方/思源） ──
s = s.replace(
  "--f-cn:-apple-system,'PingFang SC','MiSans','HarmonyOS Sans SC','Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif",
  "--f-cn:'Alibaba PuHuiTi 2.0','阿里巴巴普惠体 2.0',-apple-system,'PingFang SC','Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif")
s = s.replace(
  "--f-en:'Satoshi',-apple-system,'PingFang SC',sans-serif",
  "--f-en:'Alibaba PuHuiTi 2.0','阿里巴巴普惠体 2.0','Calibri',-apple-system,'PingFang SC',sans-serif")

# ── 4) 标题 ──────────────────────────────────────────────────
s = re.sub(r"<title>[^<]*</title>",
  "<title>AI 有了身体，为什么还是三天进抽屉？· 2026 AI 产品大会版</title>", s, count=1)

# ── 5) 封面：模板 keyart 版（结构同 cowork-conf，文案换本场） ──
cover_old_start = s.index('<section class="slide">\n  <div class="cover">')
cover_old_end = s.index("</section>", cover_old_start) + len("</section>")
NEW_COVER = '''<section class="slide">
  <div class="confcover">
    <div class="cc-in">
      <div class="cc-kicker flow" style="--i:0">人人都是产品经理 · 2026 AI 产品大会 · 声网 AIoT 专场</div>
      <h1 class="cc-title ink" style="--i:1">AI 有了身体，<br>为什么还是三天进抽屉？</h1>
      <div class="cc-sub spread" style="--i:3">多模态 AI 硬件，从能力堆叠到关系成立</div>
      <div class="cc-speaker rise" style="--i:5">主讲人：<b>姚光华 Colin</b><span>声网 AI 产品线负责人 · Head of AI Products, Agora</span></div>
    </div>
  </div>
</section>'''
s = s[:cover_old_start] + NEW_COVER + s[cover_old_end:]

# ── 6) 观点页文案：MONEY QUOTE → 观点页 · 嘉宾金句 ───────────
s = re.sub(r"(?i)Money Quote · 0(\d)", r"观点页 · 嘉宾金句 · 0\1", s)

# ── 7) 大会版式覆盖层（追加在最后一段样式之后，级联取胜） ─────
#   与 build-conf.py 的 CONF_CSS 同源。不适用于本 deck 的选择器（.fx2/.nstar/.adv）
#   无害保留；deck-media（.dm-ind/.vslide）V3 已自带同名同值声明，此处去重不再重复。
CONF_CSS = """
/* ============ 2026 AI 产品大会 · 版式覆盖层 ============ */
/* 页头：紫方块 tab + 面包屑 · 右上双 logo（模板规范） */
.chrome{align-items:center;}
.chrome span:first-child{position:relative;padding-left:18px;color:var(--ink);letter-spacing:.18em;}
.chrome span:first-child::before{content:"";position:absolute;left:0;top:50%;transform:translateY(-50%);
  width:9px;height:22px;background:#9333EA;}
.chrome span:last-child{margin-right:212px;color:var(--ink-3);}
.chrome::after{content:"";position:absolute;right:56px;top:34px;width:190px;height:22px;
  background:url(__LOGO__) right center/contain no-repeat;opacity:.92;}
/* 封面：模板 keyart 全幅 + 深色标题（对齐模板 slide 1） */
.confcover{position:absolute;inset:0;background:#eef0f4 url(__COVER__) center/cover no-repeat;
  display:flex;align-items:center;}
.confcover::after{content:"";position:absolute;right:56px;top:34px;width:190px;height:22px;
  background:url(__LOGO__) right center/contain no-repeat;filter:invert(1) brightness(.2);opacity:.85;}
.cc-in{padding:0 0 40px 120px;max-width:1220px;}
.cc-kicker{font-family:var(--f-mono);font-size:15px;letter-spacing:.3em;color:#7E22CE;margin-bottom:34px;}
.cc-title{font-size:90px;font-weight:900;line-height:1.22;color:#111;letter-spacing:.01em;padding-right:.08em;}
.cc-sub{font-size:30px;color:#3c3c46;margin-top:26px;letter-spacing:.06em;}
.cc-speaker{margin-top:64px;font-size:24px;color:#111;}
.cc-speaker b{color:#111;}
.cc-kicker,.cc-sub,.cc-title{text-shadow:0 0 22px rgba(255,255,255,.55);}
.cc-speaker b{font-weight:900;font-size:28px;}
.cc-speaker span{display:block;margin-top:10px;font-size:15px;color:#6b6b76;font-family:var(--f-mono);letter-spacing:.06em;}
/* 章节页：对齐模板「01 章节标题」语法 */
.act .num{font-family:var(--f-mono);font-size:15px;letter-spacing:.3em;color:#C084FC;}
.act .en{font-size:56px;letter-spacing:.14em;color:rgba(255,255,255,.34);-webkit-mask-image:none;mask-image:none;}
.act .cn{font-size:88px;font-weight:900;color:#fff;}
.act .cn::before{content:"";display:inline-block;width:14px;height:44px;background:#9333EA;margin-right:26px;}
.act .d{color:var(--ink-3);}
/* 观点页（金句）：大会现场照片底 + 暗化（对齐模板观点页） */
.mq{background:linear-gradient(rgba(0,0,0,.952),rgba(0,0,0,.968)),url(__VENUE__) center/cover no-repeat;}
.mq .mark{color:#FFC000;}
.mq .q i{color:#fff;}
.mq .rule{background:#FFC000;}
/* 压缩层 · 左右双栏与北极星挂载 */
.fx2{display:grid;grid-template-columns:1fr 1fr;gap:52px;align-items:start;}
.fxh{font-family:var(--f-mono);font-size:14px;letter-spacing:.2em;color:var(--amber);margin-bottom:14px;}
.fxrow{display:grid;grid-template-columns:150px 130px 1fr;column-gap:16px;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--hair-soft);}
.fxrow .fk{font-family:var(--f-mono);font-size:15px;letter-spacing:.04em;color:var(--ink-2);}
.fxrow .fn{font-family:var(--f-en);font-size:27px;font-weight:900;color:var(--ink);text-align:right;}
.fxrow .fd{font-size:16px;color:var(--ink-3);}
.fxnote{font-size:16px;line-height:1.65;color:var(--ink-3);margin-top:14px;}
.fxnote b{color:var(--ink-2);}
.fx2 svg .txt{font-size:17px;}
.fx2 svg .big{font-size:40px;}
.nstar{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:26px;margin-top:18px;}
.nstar .ns{border-top:2px solid var(--hair-strong);padding-top:12px;}
.nstar .ns b{display:block;font-size:24px;font-weight:900;color:var(--ink);}
.nstar .ns span{display:block;margin-top:5px;font-size:15px;font-family:var(--f-mono);letter-spacing:.06em;color:var(--ink-3);}
.nstar .ns.am{border-top-color:var(--amber);}
.nstar .ns.am b{color:var(--amber);}
/* C3 · P50 进阶行（评测=计费口径） */
.adv{display:flex;gap:20px;align-items:baseline;border-top:1px solid var(--hair);padding-top:16px;}
.adv .ak{font-family:var(--f-mono);font-size:15px;letter-spacing:.12em;color:var(--amber);white-space:nowrap;flex:none;}
.adv .ab{font-size:23px;font-weight:700;color:var(--ink);white-space:nowrap;flex:none;}
.adv .ad{font-size:17px;color:var(--ink-3);line-height:1.5;}
/* 结尾页照常黑底 */
@media print{.chrome::after,.confcover::after{opacity:1;}}
"""
CONF_CSS = CONF_CSS.replace("__LOGO__", LOGO).replace("__COVER__", COVER).replace("__VENUE__", VENUE)
li = s.rindex("</style>")
s = s[:li] + CONF_CSS + s[li:]

open(os.path.join(REPO, "public", "decks", "aiot26-conf.html"), "w", encoding="utf-8").write(s)

# ── 8) 发布前断言 ────────────────────────────────────────────
n = len(re.findall(r'<section class="slide', s))
assert n == 35, f"大会版应为 35 页，实际 {n}"
assert "noindex" in s and "deckRuler" in s, "noindex / deckRuler 缺失"
assert s.count("观点页 · 嘉宾金句") >= 1, "观点页文案未生效"
assert "MONEY QUOTE" not in s, "仍有未替换的 MONEY QUOTE"
assert 'class="confcover"' in s and 'class="cc-title ink"' in s, "confcover 未装配"
assert "data-theme" not in s, "单主题化失败：仍有 data-theme"
assert "deckSwap" not in s and "colin-theme" not in s, "单主题化失败：仍有 deckSwap / colin-theme"
assert "e.key!=='t'" not in s, "单主题化失败：T 键监听仍在"
assert "PuHuiTi" in s, "普惠体字体栈未生效"
assert "--amber:#A855F7" in s and "--coral:#FFC000" in s, "大会 token 块未生效"
# 内容层（V3 资产）必须原样在位
for _mk in ("伙伴感 = 角色一致性 × 共同历史 × 可控临场", "临场感 = 实时听见 × 立刻想起 × 当下回应",
            "别听错。别失控。别让人等。", "从玩具到伙伴的距离，", "四方责任",
            "gemini-demo.mp4", 'poster="/media/aiot26/still-1.jpg"'):
    assert _mk in s, f"V3 内容缺失：{_mk}"
assert len(re.findall(r'<div class="act">', s)) == 5, "五张幕卡缺失"
assert len(re.findall(r'<div class="mq">', s)) == 4, "金句页 / 终页数量不对"
print(f"aiot26-conf.html written · {n} slides · {len(s)//1024}KB")
print("单主题 ✓  普惠体 ✓  confcover ✓  观点页 ✓  noindex ✓  ruler ✓  媒体 ✓")
