#!/usr/bin/env python3
"""cowork.html → cowork-conf.html：2026 AI 产品大会视觉版。
   完全对齐大会模板：黑底 + 紫系(#9333EA/#A855F7/#C084FC) + 金黄 #FFC000 +
   阿里巴巴普惠体 2.0 + 页头紫 tab/双 logo + 模板封面 keyart + 章节页/观点页版式。
   内容与 62 页定稿母版逐字一致（内容层已烘焙进母版），仅叠加视觉层与媒体层
   （P3 录音 + 「授权可收回」页后插视频页）+ 演讲压缩层（两轮 -8），共 55 页。
   媒体行为与 PPT 对齐：前进键第一按播放，再按停止并翻页；M 键手动播/停（p 已被「跳上一整页」占用）。

   ── 双输出（2026-08-05）──────────────────────────────────────────────
   本脚本一份源码出两个 deck，靠环境变量 CONF_V2 切换：
     默认（不设）  → 55 页大会版   public/decks/cowork-conf.html   （线上 /cowork-conf，C1–C6）
     CONF_V2=1     → 43 页 R8 聚焦版 public/decks/cowork-confv2.html（预览 /cowork-confv2，+C8）
   C8 的全部变换（删陪伴章、钱×渗透拆回、PART/金句重编号、灰字提亮、+2px、溢出档…）
   一律在 `if V2:` 门内；门外两版逐字一致，唯一共用增量 = FIX_CSS（多行 note clip-path 真 bug）。"""
import os, re, sys
sys.path.insert(0, "/tmp/conf-tpl")
from assets import LOGO, COVER, VENUE

V2 = os.environ.get("CONF_V2") == "1"
OUT = "public/decks/cowork-confv2.html" if V2 else "public/decks/cowork-conf.html"

s = open("public/decks/cowork.html", encoding="utf-8").read()

# ── 1) 单主题：替换 浅底:root + 暗底 两个 token 块 ─────────────
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

# ── 2) 去掉主题引导/切换（单主题） ───────────────────────────
s = s.replace('<html lang="zh-CN" data-theme="dark">', '<html lang="zh-CN">')
s = re.sub(r"<script>try\{if\(localStorage\.getItem\('colin-theme'\)[^<]*</script>", "", s, count=1)
s = re.sub(r'<button class="deck-swap" id="deckSwap">[^<]*</button>\s*<script>\s*\(function\(\)\{\s*var b=document\.getElementById\(\'deckSwap\'\);.*?\}\)\(\);\s*</script>', "", s, flags=re.S, count=1)

# ── 3) 字体：普惠体 2.0 优先（观众机无字体时回落苹方/思源） ──
s = s.replace(
  "--f-cn:-apple-system,'PingFang SC','MiSans','HarmonyOS Sans SC','Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif",
  "--f-cn:'Alibaba PuHuiTi 2.0','阿里巴巴普惠体 2.0',-apple-system,'PingFang SC','Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif")
s = s.replace(
  "--f-en:'Satoshi',-apple-system,'PingFang SC',sans-serif",
  "--f-en:'Alibaba PuHuiTi 2.0','阿里巴巴普惠体 2.0','Calibri',-apple-system,'PingFang SC',sans-serif")

# ── 4) 标题 & meta ───────────────────────────────────────────
s = re.sub(r"<title>[^<]*</title>",
  "<title>从「被托付」到「双向奔赴 · 共事」· 2026 AI 产品大会版</title>", s, count=1)

# ── 5) 封面：模板 keyart 版 ─────────────────────────────────
cover_old_start = s.index('<section class="slide active">\n  <div class="cover">')
cover_old_end = s.index("</section>", cover_old_start) + len("</section>")
NEW_COVER = '''<section class="slide active">
  <div class="confcover">
    <div class="cc-in">
      <div class="cc-kicker flow" style="--i:0">人人都是产品经理 · 2026 AI 产品大会</div>
      <h1 class="cc-title ink" style="--i:1">从「被托付」<br>到「双向奔赴 · 共事」</h1>
      <div class="cc-sub spread" style="--i:3">对话式智能体的信任进化</div>
      <div class="cc-speaker rise" style="--i:5">主讲人：<b>姚光华 Colin</b><span>声网 AI 产品线负责人 · Head of AI Products, Agora</span></div>
    </div>
  </div>
</section>'''
s = s[:cover_old_start] + NEW_COVER + s[cover_old_end:]

# ── 6) 观点页文案：MONEY QUOTE → 观点页 · 嘉宾金句 ───────────
s = re.sub(r"(?i)Money Quote · 0(\d)", r"观点页 · 嘉宾金句 · 0\1", s)

# ──（内容层已于 2026-08-03 定稿烘焙进母版；母版 = /cowork final 定格，自此冻结）──
# ── 6.4-C) 演讲压缩层（2026-08-04 · 仅大会版 · -5 页 → 58 页） ──
# 目标：时长可控。① P7×P8 融合(左钱右渗透,分步展开) ② P10×P11 融合(阶段为主轴,北极星挂下方)
# ③ 删 案例06(十一周)/四条线(进化)/终页 ④ 收束挪到「尺子两面」前——全场以「向外叫 Eval,向内叫内观」收束
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
_en = [s.index('</section>', t) + len('</section>') for t in _st]
_head2, _tail2 = s[:_st[0]], s[_en[-1]:]
_secs = [s[_st[i]:_en[i]] for i in range(len(_st))]
assert len(_secs) == 62, f"母版应 62 页，实际 {len(_secs)}"

# C8 存底：母版原「钱」页 / 原「渗透」页（C1 会把 _secs[6] 覆盖成 F_MONEY 融合页，
# C8 里要原样拆回这两页——存底放在任何改写之前，保证拆回的就是母版原文）
_ORIG6, _ORIG7 = _secs[6], _secs[7]
# C9 存底：母版原 Eval 一/二课两页（C2 会把 _secs[28] 覆盖成 F_EVAL 融合页）、
#          母版原「体验的围栏 / 执行的围栏」两页（C1 会把 _secs[46] 覆盖成 F_FENCE 融合页）。
#          同 C8 手法：存底放在任何改写之前，C9 拆回的就是母版原文。
_ORIG28, _ORIG29 = _secs[28], _secs[29]
_ORIG46, _ORIG47 = _secs[46], _secs[47]

F_MONEY = '''<section class="slide">
  <div class="chrome"><span>PART 1 · 语法变了</span><span>7</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">整个赛道在同时点火，采购已经开动</div>
      <h2 class="ink" style="--i:1">先看<em>钱</em>往哪儿去了，再看<em>渗透</em>到了哪儿</h2>
    </div>
    <div class="body">
      <div class="fx2">
        <div class="fxcol">
          <div class="fxh flow" style="--i:2">钱 · 不是一个垂类在融资</div>
          <div class="fxrow flow" style="--i:3"><span class="fk">ElevenLabs</span><span class="fn">$11B</span><span class="fd">最新估值 · 红杉领投 $500M</span></div>
          <div class="fxrow flow" style="--i:4"><span class="fk">OpenAI</span><span class="fn">$25B</span><span class="fd">年化收入 · 模型方亲自做「在场」</span></div>
          <div class="fxrow flow" style="--i:5"><span class="fk">Cartesia</span><span class="fn">$100M</span><span class="fd">B 轮 · 押延迟，不押音色</span></div>
          <div class="fxrow flow" style="--i:6"><span class="fk">Sierra</span><span class="fn">$150M+</span><span class="fd">ARR · 按「解决」收费</span></div>
          <div class="fxrow flow" style="--i:7"><span class="fk">Fin</span><span class="fn">~$100M</span><span class="fd">ARR · $0.99 per resolution</span></div>
          <div class="fxrow flow" style="--i:8"><span class="fk">Retell</span><span class="fn">$40M</span><span class="fd">ARR · 已盈利 · 3,000+ 企业</span></div>
          <div class="fxnote flow" style="--i:9">国内不看故事看存量：呼叫中心全口径 <b>¥5,850 亿</b>，纯技改空间 <b>&gt;2,000 亿</b>，AI 坐席成本仅人工 <b>15–20%</b>。</div>
        </div>
        <div class="fxcol" data-step="1">
          <div class="fxh flow" style="--i:0">渗透 · 这五个数都已经发生</div>
          <div class="fig" style="margin:0;justify-content:flex-start;">
          <svg viewBox="0 0 790 400" width="790" aria-hidden="true">
            <text class="txt pop" style="--i:1" x="0" y="22">中国银行业 · 已部署智能客服</text>
            <path class="stroke" stroke-width="12" stroke-linecap="round" d="M0 50 H700" opacity=".22"/>
            <path class="stroke-am dw" style="--len:637;--i:1" stroke-width="12" stroke-linecap="round" d="M0 50 H637"/>
            <text class="big pop" style="--i:2" x="790" y="62" text-anchor="end">91%</text>
            <text class="txt pop" style="--i:2" x="0" y="100">AI 语音坐席成本 · 相对人工</text>
            <path class="stroke" stroke-width="12" stroke-linecap="round" d="M0 128 H700" opacity=".22"/>
            <path class="stroke-am dw" style="--len:140;--i:2" stroke-width="12" stroke-linecap="round" d="M0 128 H140"/>
            <text class="big pop" style="--i:3" x="790" y="140" text-anchor="end">15–20%</text>
            <text class="txt pop" style="--i:3" x="0" y="178">美国成年人 · 用过 AI 聊天机器人（两年前 33%）</text>
            <path class="stroke" stroke-width="12" stroke-linecap="round" d="M0 206 H700" opacity=".22"/>
            <path class="stroke-am dw" style="--len:343;--i:3" stroke-width="12" stroke-linecap="round" d="M0 206 H343"/>
            <text class="big pop" style="--i:4" x="790" y="218" text-anchor="end">49%</text>
            <text class="txt pop" style="--i:4" x="0" y="256">美国青少年 · 用过 AI 陪伴类产品</text>
            <path class="stroke" stroke-width="12" stroke-linecap="round" d="M0 284 H700" opacity=".22"/>
            <path class="stroke-am dw" style="--len:504;--i:4" stroke-width="12" stroke-linecap="round" d="M0 284 H504"/>
            <text class="big pop" style="--i:5" x="790" y="296" text-anchor="end">72%</text>
            <text class="txt pop" style="--i:5" x="0" y="334">要紧事宁可先说给 AI 听、不找真人</text>
            <path class="stroke" stroke-width="12" stroke-linecap="round" d="M0 362 H700" opacity=".22"/>
            <path class="stroke-co dw" style="--len:231;--i:5" stroke-width="12" stroke-linecap="round" d="M0 362 H231"/>
            <text class="big fill-co pop" style="--i:6" x="790" y="374" text-anchor="end">33%</text>
          </svg>
          </div>
          <div class="fxnote flow" style="--i:7">预测还在打架（「2027 一半电话 AI 独立处理」vs「一半组织放弃迁移」）——<b>别等预测收敛，看采购。</b>拦住企业的是「出了问题算谁的」，第三、四幕来解。</div>
        </div>
      </div>
      <div class="foot flow rev" style="--i:10">对话式 AI 从技术选项变成预算科目 · 海外 2026 公开信息 · 国内 CC-CMM / 艾媒 / 第一新声 · 消费侧 Pew 2026.06 / Common Sense Media 2025.07</div>
    </div>
  </div>
</section>'''

F_STAGES = _secs[9]
F_STAGES = F_STAGES.replace('<div class="eyebrow flow" style="--i:0">本场承重页 · 被使用 → 被记住 → 被托付 → 双向奔赴 · 共事</div>',
                            '<div class="eyebrow flow" style="--i:0">本场承重页 · 四个阶段 × 四把北极星尺子</div>')
_NSTAR = '''<div class="nstar">
        <div class="ns flow" style="--i:4"><b>任务成功率</b><span>被使用 · 它行不行</span></div>
        <div class="ns" data-step="1"><b>30 天留存率</b><span>被记住 · 它熟不熟</span></div>
        <div class="ns" data-step="2"><b>结果达成率</b><span>被托付 · 它担不担得起</span></div>
        <div class="ns am" data-step="3"><b>名下净业绩</b><span>双向奔赴 · 它算不算一个人头</span></div>
      </div>
      <div class="note"'''
assert F_STAGES.count('<div class="note"') == 1
F_STAGES = F_STAGES.replace('<div class="note"', _NSTAR, 1)
F_STAGES = F_STAGES.replace('这一步才算<b class="am">双向</b>。</span></div>',
                            '这一步才算<b class="am">双向</b>。<br>而拿上一阶段的尺子去管下一阶段——拿成功率验收一个要审批的岗位——是三年里最常见的<b>错位</b>。</span></div>')

_secs[6] = F_MONEY
_secs[9] = F_STAGES

# ── C2（2026-08-04 二轮 · -3 → 55 页）─────────────────────────
# ① Eval 一二课合并（题之骗 × 粒度之骗，左右双栏），四课顺位为第二课紧随，三课(方法论)收尾
# ② 类比三把尺子并进自治爬梯（不破坏梯子原展示，交叉验证作末步条带）
# ③ 两道围栏合一页上下两栏（图原样保留缩放，正文砍掉由口播承担）
F_EVAL = '''<section class="slide">
  <div class="chrome"><span>PART 3 · 被托付 · Eval 第一课</span><span>29</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow coral flow" style="--i:0">Eval 第一课 · 题之骗 × 粒度之骗</div>
      <h2 class="ink" style="--i:1">你的 demo 在骗你，你的<span class="co">单轮打分</span>也在骗你</h2>
    </div>
    <div class="body">
      <div class="fx2">
        <div class="fxcol">
          <div class="fxh flow" style="--i:2">题之骗 · demo 的题 ≠ 生产的题</div>
          <div class="fig" style="margin:0;justify-content:flex-start;">
          <svg viewBox="0 0 780 300" width="780" aria-hidden="true">
            <text class="lbl pop" style="--i:3" x="330" y="24" text-anchor="middle">厂商 A</text>
            <text class="lbl pop" style="--i:3" x="420" y="24" text-anchor="middle">B</text>
            <text class="lbl pop" style="--i:3" x="510" y="24" text-anchor="middle">C</text>
            <text class="lbl pop" style="--i:3" x="600" y="24" text-anchor="middle">D</text>
            <text class="lbl pop" style="--i:3" x="690" y="24" text-anchor="middle">E</text>
            <text class="lbl pop" style="--i:3" x="770" y="24" text-anchor="end">F</text>
            <path class="stroke dw" style="--len:780;--i:3" stroke-width="1" d="M0 44 H780" opacity=".5"/>
            <g class="pop" style="--i:4"><text class="ttl" x="0" y="112" style="font-size:23px">生僻哲学词</text></g>
            <text class="sm pop" style="--i:4" x="0" y="142">现象学 · 二律背反 · 祛魅</text>
            <path class="stroke-am dw" style="--len:34;--i:5" stroke-width="2.6" stroke-linecap="round" d="M322 108 L328 115 L339 100"/>
            <path class="stroke-am dw" style="--len:34;--i:5" stroke-width="2.6" stroke-linecap="round" d="M412 108 L418 115 L429 100"/>
            <path class="stroke-am dw" style="--len:34;--i:5" stroke-width="2.6" stroke-linecap="round" d="M502 108 L508 115 L519 100"/>
            <path class="stroke-am dw" style="--len:34;--i:6" stroke-width="2.6" stroke-linecap="round" d="M592 108 L598 115 L609 100"/>
            <path class="stroke-am dw" style="--len:34;--i:6" stroke-width="2.6" stroke-linecap="round" d="M682 108 L688 115 L699 100"/>
            <path class="stroke-am dw" style="--len:34;--i:6" stroke-width="2.6" stroke-linecap="round" d="M752 108 L758 115 L769 100"/>
            <path class="stroke dw" style="--len:780;--i:6" stroke-width="1" d="M0 176 H780" opacity=".3"/>
            <g class="pop" style="--i:7"><text class="ttl fill-co" x="0" y="240" style="font-size:23px">呼号 / 逐位订单号</text></g>
            <text class="sm pop" style="--i:7" x="0" y="270">B 如 Boy · 0086 · 一位一位念</text>
            <path class="stroke-co dw" style="--len:40;--i:8" stroke-width="2.6" stroke-linecap="round" d="M324 226 L338 240 M338 226 L324 240"/>
            <path class="stroke-co dw" style="--len:40;--i:8" stroke-width="2.6" stroke-linecap="round" d="M414 226 L428 240 M428 226 L414 240"/>
            <path class="stroke-co dw" style="--len:40;--i:8" stroke-width="2.6" stroke-linecap="round" d="M504 226 L518 240 M518 226 L504 240"/>
            <path class="stroke-co dw" style="--len:40;--i:9" stroke-width="2.6" stroke-linecap="round" d="M594 226 L608 240 M608 226 L594 240"/>
            <path class="stroke-co dw" style="--len:40;--i:9" stroke-width="2.6" stroke-linecap="round" d="M684 226 L698 240 M698 226 L684 240"/>
            <path class="stroke-co dw" style="--len:40;--i:9" stroke-width="2.6" stroke-linecap="round" d="M754 226 L768 240 M768 226 L754 240"/>
          </svg>
          </div>
          <div class="fxnote flow" style="--i:10">「现象学」全对，「B 如 Boy」全崩——<b>demo 里全是你写的题。</b></div>
        </div>
        <div class="fxcol" data-step="1">
          <div class="fxh flow" style="--i:0">粒度之骗 · 轮轮满分，整段 0 分</div>
          <div class="fig" style="margin:0;justify-content:flex-start;">
          <svg viewBox="0 0 780 210" width="780" aria-hidden="true">
            <text class="lbl fill-am pop" style="--i:1" x="0" y="20">单轮评测 · 每一轮都拿满分</text>
            <rect class="box pop" style="--i:2" x="0" y="38" width="115" height="56" rx="4"/>
            <rect class="box pop" style="--i:2" x="133" y="38" width="115" height="56" rx="4"/>
            <rect class="box pop" style="--i:2" x="266" y="38" width="115" height="56" rx="4"/>
            <rect class="box pop" style="--i:3" x="399" y="38" width="115" height="56" rx="4"/>
            <rect class="box pop" style="--i:3" x="532" y="38" width="115" height="56" rx="4"/>
            <rect class="box pop" style="--i:3" x="665" y="38" width="115" height="56" rx="4"/>
            <text class="lbl fill-am pop" style="--i:3" x="57" y="72" text-anchor="middle">T1 ✓</text>
            <text class="lbl fill-am pop" style="--i:3" x="190" y="72" text-anchor="middle">T2 ✓</text>
            <text class="lbl fill-am pop" style="--i:3" x="323" y="72" text-anchor="middle">T3 ✓</text>
            <text class="lbl fill-am pop" style="--i:4" x="456" y="72" text-anchor="middle">T4 ✓</text>
            <text class="lbl fill-am pop" style="--i:4" x="589" y="72" text-anchor="middle">T5 ✓</text>
            <text class="lbl fill-am pop" style="--i:4" x="722" y="72" text-anchor="middle">T6 ✓</text>
            <path class="stroke-co dw" style="--len:800;--i:5" stroke-width="2" d="M0 128 V150 H780 V128"/>
            <g class="pop" style="--i:6"><text class="ttl fill-co" x="390" y="192" text-anchor="middle" style="font-size:23px">整段 · 客户想改的那个航班，最后没改成</text></g>
          </svg>
          </div>
          <div class="fxrow flow" style="--i:7"><span class="fk">段级 01</span><span class="fn" style="font-size:20px">任务完成率</span><span class="fd">来的时候要什么，走的时候拿到没有</span></div>
          <div class="fxrow flow" style="--i:8"><span class="fk">段级 02</span><span class="fn" style="font-size:20px">转人工原因</span><span class="fd">转出去不丢人，说不清原因才丢人</span></div>
          <div class="fxrow flow" style="--i:9"><span class="fk">段级 03</span><span class="fn" style="font-size:20px">48h 重复来电</span><span class="fd">「解决了」最诚实的反证</span></div>
        </div>
      </div>
      <div class="note flow" data-step="1"><span>单轮指标是给模型看的，段级指标才是给业务看的。<b>你付钱买的是结果，不是六次礼貌的回应。</b></span></div>
    </div>
  </div>
</section>'''
_secs[28] = F_EVAL

# 课四 → Eval 第二课（紧随合并页）；课三保持「第三课」名号收尾
_secs[31] = _secs[31].replace('Eval 第四课', 'Eval 第二课')

# 爬梯页 · 追加交叉验证条带（末步登场，不动原梯子）
# C5 · 断层折点 x 从 960 → 675：与母版梯子 svg 里「最大的一跳 THE BIG JUMP」那条紫色竖虚线
#      （d="M675 40 V450"）同 x。两 svg 同为 width=1680 / viewBox 0 0 1680 …，坐标系一致，
#      故直接取 675；标签 x=675+14=689，两段 sm 居中 x=(340+675)/2≈508 与 (675+1580)/2≈1128。
_STRIP = '''</svg>
      </div>
      <div class="fig" data-step="4" style="margin-top:4px">
        <svg width="1680" viewBox="0 0 1680 178" fill="none">
          <path class="stroke-co pop" style="--i:0" stroke-width="1.4" stroke-dasharray="5 9" d="M675 6 V172"/>
          <text class="lbl fill-co pop" style="--i:1" x="689" y="22">交叉验证 · 两个行业的断层，也卡在同一格</text>
          <g class="pop" style="--i:1"><text class="ttl" x="0" y="56" style="font-size:22px">自动驾驶 L1–L5</text></g>
          <path class="stroke dw" style="--len:1240;--i:2" stroke-width="2" d="M340 50 H675 V26 H1580"/>
          <text class="sm pop" style="--i:3" x="508" y="76" text-anchor="middle">L1–L2 · 辅助驾驶，人不敢离环</text>
          <text class="sm pop" style="--i:3" x="1128" y="70" text-anchor="middle">L3–L5 · 系统担责，卡了十年的一跳</text>
          <g class="pop" style="--i:2"><text class="ttl" x="0" y="136" style="font-size:22px">支付 Agent 五级</text></g>
          <path class="stroke dw" style="--len:1240;--i:3" stroke-width="2" d="M340 130 H675 V106 H1580"/>
          <text class="sm pop" style="--i:4" x="508" y="156" text-anchor="middle">L1–L2 · 行业还在边缘徘徊</text>
          <text class="sm pop" style="--i:4" x="1128" y="150" text-anchor="middle">L3–L5 · 还没人真正到达</text>
          <text class="lbl fill-am pop" style="--i:5" x="1580" y="176" text-anchor="end">第三把尺子，就是上面这架梯子——三把尺子，同一个形状</text>
        </svg>
      </div>
      <div class="note flow" data-step="3"'''
assert _secs[39].count('</svg>\n      </div>\n      <div class="note flow" data-step="3"') == 1
_secs[39] = _secs[39].replace('</svg>\n      </div>\n      <div class="note flow" data-step="3"', _STRIP, 1)
_secs[39] = _secs[39].replace('<div class="eyebrow flow" style="--i:0">自治爬梯 · THE AUTONOMY LADDER</div>',
                              '<div class="eyebrow flow" style="--i:0">自治爬梯 × 交叉验证 · HUMAN IN THE LOOP</div>')

# 两道围栏合一页（图原样保留，按宽缩放；正文口播）
def _svg(sec):
    a = sec.index('<svg'); b = sec.index('</svg>') + 6
    return sec[a:b]
_sv_exp = _svg(_secs[46]).replace('width="1680"', 'width="1360"', 1)
# C5 · 执行的围栏改「左右两栏」重排（母版 _secs[47] 原 svg 是上下堆叠 578 高，缩到 1130 宽后拥挤且左偏）。
#      markup / 类名全部沿用母版，只改坐标：左栏文本通道、右栏语音通道，两栏镜像对称，
#      中间一条极淡竖分隔；底部「事后没有撤回键…」+ 闸门线横贯全宽。
_SV_EXE_LR = '''<svg width="1560" viewBox="0 0 1680 386" fill="none">
          <!-- 两栏中缝：极淡竖分隔 -->
          <path class="stroke pop" style="--i:0" stroke-width="1" opacity=".16" d="M840 8 V238"/>

          <!-- 左栏 · 文本通道 -->
          <text class="lbl pop" style="--i:0" x="0" y="18">文本通道 · TEXT CHANNEL</text>
          <rect class="box pop" style="--i:0" x="0" y="36" width="220" height="72" rx="4"/>
          <g class="pop" style="--i:0"><text class="ttl" x="110" y="80" text-anchor="middle" style="font-size:24px">生成</text></g>
          <path class="stroke dw" style="--len:52;--i:1" stroke-width="1.6" d="M220 72 H272"/>
          <path class="fill-ink pop" style="--i:1" d="M272 64 L286 72 L272 80 Z"/>
          <rect class="box pop" style="--i:1" x="290" y="36" width="220" height="72" rx="4"/>
          <g class="pop" style="--i:1"><text class="ttl" x="400" y="80" text-anchor="middle" style="font-size:24px">人过一眼</text></g>
          <path class="stroke dw" style="--len:52;--i:2" stroke-width="1.6" d="M510 72 H562"/>
          <path class="fill-ink pop" style="--i:2" d="M562 64 L576 72 L562 80 Z"/>
          <rect class="box pop" style="--i:2" x="580" y="36" width="220" height="72" rx="4"/>
          <g class="pop" style="--i:2"><text class="ttl" x="690" y="80" text-anchor="middle" style="font-size:24px">发出</text></g>

          <path class="stroke-am dw" style="--len:700;--i:3" stroke-width="2" d="M690 116 C 690 162, 110 162, 110 116"/>
          <path class="fill-am pop" style="--i:4" d="M101 116 L110 100 L119 116 Z"/>
          <g class="pop" style="--i:4">
            <path class="stroke-am pkt" stroke-width="4"
              style="--pl:70px;--p0:70px;--p1:-700px;--pt:5.6s;--pd:1.6s" d="M690 116 C 690 162, 110 162, 110 116"/>
          </g>
          <text class="txt fill-am pop" style="--i:4" x="400" y="196" text-anchor="middle">可撤回 · 可编辑 · 发错了还能删</text>
          <text class="txt pop" style="--i:5" x="400" y="230" text-anchor="middle">一句越权的承诺，在文本里是一条可以删掉的消息。</text>

          <!-- 右栏 · 语音通道（与左栏同 y，镜像对称） -->
          <text class="lbl pop" style="--i:4" x="880" y="18">语音通道 · VOICE CHANNEL</text>
          <rect class="box pop" style="--i:4" x="880" y="36" width="220" height="72" rx="4"/>
          <g class="pop" style="--i:4"><text class="ttl" x="990" y="80" text-anchor="middle" style="font-size:24px">生成</text></g>
          <path class="stroke dw" style="--len:52;--i:5" stroke-width="1.6" d="M1100 72 H1152"/>
          <path class="fill-ink pop" style="--i:5" d="M1152 64 L1166 72 L1152 80 Z"/>
          <rect class="box pop" style="--i:5" x="1170" y="36" width="220" height="72" rx="4"/>
          <g class="pop" style="--i:5"><text class="ttl" x="1280" y="80" text-anchor="middle" style="font-size:24px">直接进耳朵</text></g>
          <path class="stroke dw" style="--len:52;--i:6" stroke-width="1.6" d="M1390 72 H1442"/>
          <path class="fill-ink pop" style="--i:6" d="M1442 64 L1456 72 L1442 80 Z"/>
          <rect class="box pop" style="--i:6" x="1460" y="36" width="220" height="72" rx="4" stroke="var(--coral)" stroke-width="1.6"/>
          <g class="pop" style="--i:6"><text class="ttl fill-co" x="1570" y="80" text-anchor="middle" style="font-size:24px">说出即生效</text></g>

          <!-- 画不出来的那条弧线：虚线，且永远走不回去 -->
          <g class="pop" style="--i:7">
            <path class="stroke-co" stroke-width="1.4" stroke-dasharray="6 9" opacity=".45" fill="none"
              d="M1570 116 C 1570 162, 990 162, 990 116"/>
          </g>
          <text class="txt fill-co pop" style="--i:8" x="1280" y="196" text-anchor="middle">这条弧线不存在</text>
          <text class="txt pop" style="--i:8" x="1280" y="230" text-anchor="middle">同样一句话，在电话里是一份已经成立的口头承诺。</text>

          <!-- 撤回键没有了，闸门只能整体前移 -->
          <path class="stroke dw" style="--len:1700;--i:9" stroke-width="1" opacity=".45" d="M0 262 H1680"/>
          <text class="lbl pop" style="--i:9" x="0" y="292">事后没有撤回键，那道闸门就只能整体前移到「说出口之前」</text>

          <path class="stroke dw" style="--len:1560;--i:10" stroke-width="1.6" d="M0 362 H1540"/>
          <path class="fill-ink pop" style="--i:10" d="M1540 354 L1556 362 L1540 370 Z"/>
          <path class="stroke-co dw" style="--len:52;--i:10" stroke-width="3.4" d="M375 346 V378M750 346 V378M1125 346 V378"/>
          <g class="pop" style="--i:10">
            <text class="txt fill-co" x="375" y="332" text-anchor="middle">能力边界</text>
            <text class="txt fill-co" x="750" y="332" text-anchor="middle">授权范围</text>
            <text class="txt fill-co" x="1125" y="332" text-anchor="middle">人工审批</text>
            <text class="txt fill-am" x="1680" y="332" text-anchor="end">才允许出声</text>
          </g>
        </svg>'''
_sv_exe = _SV_EXE_LR
assert '这条弧线不存在' in _svg(_secs[47]) and '这条弧线不存在' in _SV_EXE_LR
F_FENCE = ('''<section class="slide">
  <div class="chrome"><span>PART 4 · 双向奔赴 · 两道围栏</span><span>47</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">TWO FENCES · 时机立规矩，动作拦半路</div>
      <h2 class="ink" style="--i:1">两道围栏：交互行为要有<em>规矩</em>，语音动作<span class="co">最难在半路拦住</span></h2>
    </div>
    <div class="body">
      <div class="fxh flow" style="--i:2">体验的围栏 · 恰当的时机，比更快的延迟值钱</div>
      <div class="fig">''' + _sv_exp + '''</div>
      <div class="fxh" data-step="1">执行的围栏 · 文本有撤回弧线，语音那条画不出来</div>
      <div class="fig" data-step="1">''' + _sv_exe + '''</div>
    </div>
  </div>
</section>''')
_secs[46] = F_FENCE

# ── C3（2026-08-04 三轮 · 主标题精调，页数不变）───────────────
# P5 提要页正名 / P7·P8 主副对调(P7 在 F_MONEY 字面量) / P33 商业模式变迁上主标
# P38 证据 → Human in the loop / P50 补 P34 进阶：评测 = 计费口径
def _r1(i, old, new):
    assert _secs[i].count(old) == 1, f"_secs[{i}] 定位失败: {old[:48]}"
    _secs[i] = _secs[i].replace(old, new, 1)

# P5 · 「本场提要」上主标，弧线「活人感 → 双向奔赴」作副标
_r1(4, '<div class="eyebrow flow" style="--i:0">本场提要</div>',
       '<div class="eyebrow flow" style="--i:0">从「活人感」，到「双向奔赴」</div>')
_r1(4, '<h2 class="ink" style="--i:1">去年问「它像不像人」。今年问：谁在替谁说话</h2>',
       '<h2 class="ink" style="--i:1">本场提要</h2>')

# P8 · 主副对调
_r1(8, '<div class="eyebrow flow" style="--i:0">四个互不相干的人，说了同一件事</div>',
       '<div class="eyebrow flow" style="--i:0">所有的路，最后都汇到「对话」这条线上</div>')
_r1(8, '<h2 class="ink" style="--i:1">所有的路，最后都汇到「对话」这条线上</h2>',
       '<h2 class="ink" style="--i:1">四个互不相干的人，说了<em>同一件事</em></h2>')

# P33 · 商业模式变迁上主标，原主标（科目）降副标
_r1(34, '<div class="eyebrow flow" style="--i:0">怎么判断一项技术真的兑现了</div>',
        '<div class="eyebrow flow" style="--i:0">看客户把这笔钱，记在哪个科目上</div>')
_r1(34, '<h2 class="ink" style="--i:1">看客户把这笔钱，记在哪个科目上</h2>',
        '<h2 class="ink" style="--i:1">企业级智能体的商业模式变迁：从技术付费，到<em>结果付费</em></h2>')

# P38 · 隔着的不是技术，是人还在不在环里（同自动驾驶：Human in the loop）
_r1(39, '<h2 class="ink" style="--i:1">每一级之间隔着的不是技术，是<em>证据</em></h2>',
        '<h2 class="ink" style="--i:1">每一级之间隔着的不是技术，是<em>人还在不在环里</em></h2>')

# P50 · 进阶行（P34 的下一步）：评测不止定义产品，直接是计费口径；原 note 并入防重复
# （放 duo 外的紧凑单行——duo 内加带会被 body flex 压缩、overflow:hidden 截断）
_r1(53, '那句「做对了」。</b></div>\n        </div>\n      </div>',
        '''那句「做对了」。</b></div>
        </div>
      </div>
      <div class="adv flow" data-step="2"><span class="ak">进阶 · 它不止定义产品</span><span class="ab">你写的这套评测，就是「按结果收钱」的计费口径</span><span class="ad">对产品量好坏，对商业量钱——商业模式和商业结果，都押在这把尺子上</span></div>''')
_r1(53, '<div class="note" data-step="2"><span class="flow" style="--i:0">这也是为什么<b>「按结果收钱」绕不过评测</b>：计价单位从「用量」换成「结果」的那一刻，你手里得先有一把判得了「成了」的尺子。<b>先有 Evals，才谈得上按结果收钱。</b></span></div>\n      ', '')

# ── C4（2026-08-04 四轮 · P9/P21 主副再调 + 收束页精进 + Kevin Weil 事实修正）──
# P9 · 主标「四个阶段，四颗北极星」，「三个被字」回副标位
_r1(9, '<h2 class="ink" style="--i:1">三个「被」字。今年，主语换了</h2>',
       '<h2 class="ink" style="--i:1">四个阶段，四颗<em>北极星</em></h2>')
_r1(9, '<div class="eyebrow flow" style="--i:0">本场承重页 · 四个阶段 × 四把北极星尺子</div>',
       '<div class="eyebrow flow" style="--i:0">三个「被」字。今年，主语换了</div>')

# P21 · 主标改问句，原主标并入副标（保留反共识记号）
_r1(22, '<h2 class="ink" style="--i:1">有三类对话，今天就不该交给它</h2>',
        '<h2 class="ink" style="--i:1">哪些智能体，<em>不应该</em>被记住？</h2>')
_r1(22, '<div class="eyebrow coral flow" style="--i:0">本场第一处反共识</div>',
        '<div class="eyebrow coral flow" style="--i:0">本场第一处反共识 · 有三类对话，今天就不该交给它</div>')

# P54 · 收束卡精进：机制归组织（放权与决策机制），产品管理者带走新融合岗位的定义
# 四张卡收拢成四个名词：一套评测 · 一个岗位 · 一门生意 · 一套机制
_r1(60, '<span class="no">管的不再是三个职能</span><em>一套机制</em>',
        '<span class="no">管的不再是三个职能</span><em>一个新的融合岗位</em>')
_r1(60, '产品、设计、研发，走进客户现场融合成 FDE——第四个圆不是新部门，是岗位本身的变化。',
        '产品、设计、研发，走进客户现场，融合成 FDE——第四个圆不是新部门，是一个新岗位的定义。')
_r1(60, '<span class="no">要的不是 AI 能力</span><em>放权</em>',
        '<span class="no">要的不是 AI 能力</span><em>一套放权与决策机制</em>')
_r1(60, '组织真正的活，是把权放到这两把梯子够得着的那一格。',
        '组织真正的活，是定一套决策机制：把权放到这两把梯子够得着的那一格。')

# P55 · Kevin Weil 已卸任：OpenAI CPO → 前 CPO
_r1(58, '<div class="by">Kevin Weil · OpenAI CPO</div>',
        '<div class="by">Kevin Weil · OpenAI 前 CPO</div>')

# ── C5（2026-08-04 五轮 · 换序 + 对齐 + 图例对色 + 执行围栏左右排）──
# 上面三处已就地改写：_order 换序（金句02 ↔ 反共识页）、_STRIP 折点 960→675、_SV_EXE_LR 左右两栏。
# P39 · 岗位散点图图例与大会配色对不上：母版写的是浅底母版的色名，
#      在大会版 --amber=#A855F7(紫)、--coral=#FFC000(金黄)，图上根本没有「暖橙」和「粉」。
#      按图上实际颜色改口径：已规模商业化 = 紫，强监管场景 = 金黄。
_r1(40, '圆点大小 = 用量 · 暖橙 = 已规模商业化 · 灰 = 早期 · 粉 = 强监管场景',
        '圆点大小 = 用量 · 紫 = 已规模商业化 · 灰 = 早期 · 金黄 = 强监管场景')

# ── C6（2026-08-04 六轮 · 精调：授权书退场 / 实时悖论 / QoT 口语化 / 收束换资产带）──
# 背景：C1-C2 压缩把《Agent 授权书》整页删掉了，但 P41、P53 两处还在指它；
#       P44 讲「说出即生效、人来不及批」，闸门轴上却写着「人工审批」，自相矛盾。
def _cut1(i, a, b, new=''):
    """把 _secs[i] 里从 a 到 b（含首尾）的一整块换成 new。两个锚点都必须唯一。"""
    assert _secs[i].count(a) == 1, f"_secs[{i}] 起点定位失败: {a[:48]}"
    assert _secs[i].count(b) == 1, f"_secs[{i}] 终点定位失败: {b[:48]}"
    p = _secs[i].index(a)
    q = _secs[i].index(b, p) + len(b)
    _secs[i] = _secs[i][:p] + new + _secs[i][q:]

# ① P41（案例 03 · 两道围栏）教训 03：《Agent 授权书》那页已被删，改说「内核六件事」
_r1(43, '<div class="d">一份写清楚的<b>《Agent 授权书》</b>：替谁做、做什么、到哪里为止、如何披露、错了怎么办、怎么收回。这张表，第五幕交给组织。</div>',
        '<div class="d">授权不能只活在代码里，还要白纸黑字写清六件事：<b>替谁做、做什么、到哪里为止、如何披露、错了怎么办、怎么收回</b>——写不出来，就是还没想清楚。这六件事，第五幕会变成组织的授权语法。</div>')

# ② P44（两道围栏合一 · _secs[46] = F_FENCE）闸门轴的实时悖论：
#    语音「说出即生效」，人不可能逐句审批 —— 人工审批必须前移成「事前授权」（批类别，不批句子）。
_r1(46, '<text class="txt fill-co" x="1125" y="332" text-anchor="middle">人工审批</text>',
        '<text class="txt fill-co" x="1125" y="332" text-anchor="middle">事前授权</text>')
_r1(46, '<text class="lbl pop" style="--i:9" x="0" y="292">事后没有撤回键，那道闸门就只能整体前移到「说出口之前」</text>',
        '<text class="lbl pop" style="--i:9" x="0" y="292">事后没有撤回键，闸门整体前移到「说出口之前」——人工审批也前移：'
        '<tspan class="fill-am">批动作类别，不批每一句话</tspan></text>')

# ③ P47（QoT）三张维度卡换成能念出口的词；工程坐标「授权可收」→「授权可撤销」
_r1(50, '<div class="t">边界遵守 / Boundary Fidelity</div>', '<div class="t">边界 / BOUNDARY</div>')
_r1(50, '<div class="t">结果可追 / Accountability</div>', '<div class="t">结果 / ACCOUNTABILITY</div>')
_r1(50, '<div class="t">托付可收 / Recoverability</div>', '<div class="t">可撤销 / RECOVERABILITY</div>')
_r1(50, '授权可收（随时降级、随时回滚）', '授权可撤销（随时降级、随时回滚）')

# ④ P53（对组织说）：2025 那场的题目补全 + 尾部落点改「把权放给 high agency 的人」
_r1(57, '2025 年这道题我讲给产研团队，名字叫<b>单向门 / 双向门</b>；今年它升级成整个公司的授权语法——',
        '2025 年我把它讲给产研团队，题目叫<b>《人和组织，必须一起转身》</b>——单向门 / 双向门；今年它升级成整个公司的授权语法：')
_r1(57, '<div class="land flow rev" style="--i:12">个人 agency 是能力，<b>组织 agency 是制度许可</b>。<span class="s">流程集中在不可逆风险上，自由留给可逆试验。第四幕那份《Agent 授权书》，已经把「替谁做、做什么、到哪里为止、错了怎么办、怎么收回」写给它了。<b>同一张表，换个抬头，也给人发一张。</b></span></div>',
        '<div class="land flow rev" style="--i:12">转身的落点就一句：<b>把权放给 high agency 的人</b>——他们会带着 Agent，把结果一起做出来。<span class="s">个人 agency 是能力，<b>组织 agency 是制度许可</b>：流程集中在不可逆风险上，自由留给可逆试验。第四幕写给 Agent 的授权六件事，<b>换个抬头，也该给人写一份</b>。</span></div>')

# ⑤ P54（收束页）：撤掉「四路汇聚 + 进化速度=放权速度」那套收口（母版里它接的是被删掉的终页），
#    原位改成四张卡各自带走的那一件资产：评测 · 岗位 · 结果生意 · 放权决策机制。
#    ⚠️ 四组的中心必须落在 .take 的列心 200/627/1053/1480（列宽 (1680-3*26)/4=400.5）。
_TAKEAWAY_BAND = '''<div class="fig" data-step="4">
        <svg width="1680" viewBox="0 0 1680 132" fill="none">
          <!-- ① 评测 · 一把带刻度的尺子 -->
          <g class="pop" style="--i:0"><path class="stroke" stroke-width="1" opacity=".4" d="M122 14 V26 M278 14 V26 M122 20 H278"/></g>
          <path class="stroke dw" style="--len:412;--i:0" stroke-width="1.5" d="M120 34 H280 V78 H120 Z"/>
          <g class="pop" style="--i:1"><path class="stroke" stroke-width="1.4" d="M140 34 V56 M160 34 V46 M180 34 V46 M200 34 V56 M220 34 V46 M240 34 V46 M260 34 V56"/></g>
          <text class="ttl pop" style="--i:1;font-size:23px" x="200" y="118" text-anchor="middle">评测</text>

          <!-- ② 岗位 · 三圆交叠再加第四圆（FDE 那一圈是新的） -->
          <g class="pop" style="--i:1">
            <circle class="stroke" stroke-width="1.4" cx="588" cy="46" r="30"/>
            <circle class="stroke" stroke-width="1.4" cx="614" cy="46" r="30"/>
            <circle class="stroke" stroke-width="1.4" cx="640" cy="46" r="30"/>
          </g>
          <circle class="stroke-am pop" style="--i:2" stroke-width="2.4" cx="666" cy="46" r="30"/>
          <text class="ttl pop" style="--i:2;font-size:23px" x="627" y="118" text-anchor="middle">岗位</text>

          <!-- ③ 结果生意 · 价签上打勾才结算 -->
          <path class="stroke dw" style="--len:320;--i:2" stroke-width="1.5" d="M1026 18 H1104 A8 8 0 0 1 1112 26 V70 A8 8 0 0 1 1104 78 H1026 L994 48 Z"/>
          <circle class="stroke pop" style="--i:2" stroke-width="1.4" cx="1018" cy="48" r="5"/>
          <path class="stroke dw" style="--len:64;--i:3" stroke-width="2.4" stroke-linecap="round" d="M1042 48 L1056 62 L1086 30"/>
          <text class="ttl pop" style="--i:3;font-size:23px" x="1053" y="118" text-anchor="middle">结果生意</text>

          <!-- ④ 放权决策机制 · 左边双向门（进得去回得来），右边单向门（推开就没有回头） -->
          <path class="stroke dw" style="--len:250;--i:3" stroke-width="1.5" d="M1400 18 H1464 V78 H1400 Z"/>
          <path class="stroke dw" style="--len:250;--i:3" stroke-width="1.5" d="M1496 18 H1560 V78 H1496 Z"/>
          <g class="pop" style="--i:4">
            <path class="stroke" stroke-width="1.4" d="M1414 48 H1450"/>
            <path class="fill-ink" d="M1408 48 L1418 42 L1418 54 Z"/>
            <path class="fill-ink" d="M1456 48 L1446 42 L1446 54 Z"/>
            <path class="stroke" stroke-width="1.8" d="M1508 38 V58"/>
            <path class="stroke" stroke-width="1.4" d="M1508 48 H1544"/>
            <path class="fill-ink" d="M1552 48 L1542 42 L1542 54 Z"/>
          </g>
          <text class="ttl pop" style="--i:4;font-size:23px" x="1480" y="118" text-anchor="middle">放权决策机制</text>
        </svg>
      </div>'''
_cut1(60, '<div class="fig" data-step="4">', '一个更贵的玩具</b>。</span></div>', _TAKEAWAY_BAND)

# ══════════════════════════════════════════════════════════════════════════════
# ── C8（2026-08-05 · R8 第一版 · 55 → 43 页 · 聚焦企业级智能体：客服 / 销售）──
# 8.5 试讲评审会结论：
#   ① 删 PART 2「被记住 · 陪伴」整章（陪伴半球下午 AIoT 专场整场拆讲，本场不重复）
#   ② 钱 × 渗透拆回母版原版两页（融合页信息密度过高，评审会要求拆开各讲一页）
#   ③ P9 承重页加分论坛预告，把删掉的半球明确交接出去
#   ④ 暗线页（工具→合伙人）改写：指向下午专场，不再指「上一幕」
#   ⑤ PART 重编号 0/1/2/3/4 + 金句重编号 01–05 + 幕序文字指涉全扫描
#   ⑥ 灰字提亮（--ink-2/--ink-3）+ 次级文字类统一 +2px（视觉第一刀）
# ══════════════════════════════════════════════════════════════════════════════

# ── 真 bug 修复（两版共用）：多行 .note 从第二行起被 clip-path 吃掉 ──
FIX_CSS = """
/* ---- 修复：多行 .note 整段被 clip-path 吃掉第二行起 ----
   .flow 的入场动效结束态是 clip-path:inset(-10px -16px)；内联元素的裁切参考框只取
   第一行行盒，于是换行后的第二、三行永远不显示（母版遗留，P8/P10 两页命中）。
   把 note 的整段包裹层改 inline-block，参考框变成整块，动效不变、全文可见。 */
.note>span.flow,.note>span.flow.rev,.note>.flow{display:inline-block;}
"""

# ── 以下两块只在 CONF_V2=1 时装配（定义本身无副作用，放在门外便于阅读）──

_ROUTE5 = '''<!-- 全场路线：五站一条线。前两站讲「变了什么」，后三站分别回答上面三个问题。 -->
        <svg viewBox="0 0 1680 250" width="1680" fill="none">
          <path class="stroke dw" style="--len:1560;--i:6" stroke-width="1.5" d="M80 118 H1600"/>
          <path class="stroke-am dw" style="--len:800;--i:7" stroke-width="3" d="M840 118 H1600"/>

          <circle class="fill-am pop" style="--i:7" cx="80" cy="118" r="10"/>
          <circle class="pop" style="--i:7" cx="460" cy="118" r="7" fill="var(--ink-3)"/>
          <g class="pop" style="--i:8" fill="var(--slide-bg)" stroke="var(--amber)" stroke-width="3">
            <circle cx="840" cy="118" r="9"/><circle cx="1220" cy="118" r="9"/><circle cx="1600" cy="118" r="9"/>
          </g>

          <text class="lbl fill-am pop" style="--i:7" x="80" y="80" text-anchor="middle">PART 0</text>
          <text class="lbl pop" style="--i:7" x="460" y="80" text-anchor="middle">PART 1</text>
          <text class="lbl fill-am pop" style="--i:8" x="840" y="80" text-anchor="middle">PART 2</text>
          <text class="lbl fill-am pop" style="--i:8" x="1220" y="80" text-anchor="middle">PART 3</text>
          <text class="lbl fill-am pop" style="--i:8" x="1600" y="80" text-anchor="middle">PART 4</text>

          <text class="txt pop" style="--i:9" x="80" y="168" text-anchor="middle">开场</text>
          <text class="txt pop" style="--i:9" x="460" y="168" text-anchor="middle">语法变了</text>
          <text class="txt pop" style="--i:9" x="840" y="168" text-anchor="middle">被托付</text>
          <text class="txt pop" style="--i:9" x="1220" y="168" text-anchor="middle">双向奔赴</text>
          <text class="txt pop" style="--i:9" x="1600" y="168" text-anchor="middle">人与组织</text>

          <text class="sm pop" style="--i:10" x="80" y="206" text-anchor="middle">三年，同一场转身</text>
          <text class="sm pop" style="--i:10" x="460" y="206" text-anchor="middle">从调用到双向奔赴</text>
          <text class="sm fill-am pop" style="--i:10" x="840" y="206" text-anchor="middle">尺子、授权与边界</text>
          <text class="sm fill-am pop" style="--i:10" x="1220" y="206" text-anchor="middle">出事了算谁的</text>
          <text class="sm fill-am pop" style="--i:10" x="1600" y="206" text-anchor="middle">你和团队怎么变</text>
        </svg>'''

# ── C8-⑨ 次级文字类统一 +2px（现值基准显式覆盖；卡片行高同步收紧防挤）──
C8_CSS = """
/* ============ C8 · R8 第一版 · 次级文字 +2px（大屏可读性） ============ */
/* 正文 / 说明类：现值 +2px */
.note{font-size:24px;line-height:1.56;}
.mega .foot{font-size:24px;line-height:1.6;}
.land .s{font-size:24px;line-height:1.55;}
.ask .hint .v{font-size:24px;line-height:1.52;}
.ask .cue{font-size:23px;}
.rows .r .v{font-size:23px;line-height:1.46;}
.tri .col .v{font-size:23px;line-height:1.5;}
.vs .line{font-size:23px;line-height:1.52;}
.wall .v .t{font-size:23px;line-height:1.48;}
.card .d{font-size:22px;line-height:1.5;}
.card-w .d{font-size:22px;line-height:1.5;}
.duo .s{font-size:22px;line-height:1.52;}
.dutyrow .b{font-size:22px;line-height:1.5;}
.layer .ds{font-size:22px;line-height:1.44;}
.stat .l{font-size:22px;line-height:1.38;}
.steps .s{font-size:22px;}
.take .c .say .no{font-size:22px;line-height:1.38;}
.m35 .row .t{font-size:22px;}
.badgecard .row .v{font-size:22px;line-height:1.44;}
.card.sm .d{font-size:20px;line-height:1.44;}
.card .kv .vv{font-size:21px;line-height:1.44;}
.steps .s .d{font-size:21px;line-height:1.48;}
.take .c .s{font-size:21px;line-height:1.5;}
.thanks .ft{font-size:21px;}
.quotes .r .src{font-size:20px;}
.pzs{font-size:20px;line-height:1.62;}
.m35 .sx{font-size:18px;line-height:1.62;}
.mq .s{font-size:26px;line-height:1.55;}
/* 表格 */
table{font-size:23px;}
table.big tbody td{font-size:24px;}
table.tight tbody td{font-size:22px;}
table.mini tbody td{font-size:20px;line-height:1.4;}
table.mini thead th{font-size:16px;}
thead th{font-size:19px;}
/* mono 标签 / 脚注类：现值 +2px */
.foot{font-size:16px;line-height:1.62;}
.card .tag,.card-w .tag{font-size:17px;}
.card.sm .tag{font-size:15px;}
.card .kv .kk{font-size:15px;}
.steps .s .i{font-size:17px;}
.duo .h{font-size:17px;}
.dutyrow .s{font-size:17px;}
.dutyrow .h span{font-size:15px;}
.vs .col .h{font-size:17px;}
.vs .line .num{font-size:18px;}
.quotes .r .who{font-size:17px;}
.tri .col .k{font-size:16px;}
.stat .u{font-size:16px;}
.layer .fr{font-size:17px;}
.lv{font-size:17px;}
.pill{font-size:16px;}
.old .yr{font-size:16px;}
.m35 .mk{font-size:16px;}
.quote .by{font-size:16px;}
.wall .v .by{font-size:15px;}
.badgecard .row .k,.badgecard .hd .id{font-size:16px;}
.badgecard .sig .ln .k{font-size:15px;}
.ask .hint .k{font-size:16px;}
.act .rail span{font-size:18px;}
/* 图内文字（svg）：现值 +2px */
.fig .txt{font-size:21px;}
.fig .sm{font-size:18px;}
.fig .lbl{font-size:17px;}
/* conf 层自有的次级类 */
.fxrow .fk{font-size:17px;}
.fxrow .fd{font-size:18px;}
.fxnote{font-size:18px;line-height:1.6;}
.fx2 svg .txt{font-size:19px;}
.nstar .ns span{font-size:17px;}
.adv .ak{font-size:17px;}
.adv .ad{font-size:19px;line-height:1.45;}
/* 图内灰圆点不跟着提亮（P27「灰 = 早期」、P34 投入强度图例要保住三色可辨） */
[fill="var(--ink-3)"]{fill:var(--mark-3);}
/* ---- 加大后的溢出页逐页微调：只收留白 / 间距 / 内边距，字号一律不回缩 ---- */
.t8 .wrap{padding-bottom:56px;}
.t8 .head{margin-bottom:26px;}
.t8 .body{gap:20px;}
.t8b .wrap{padding-bottom:40px;}
.t8b .head{margin-bottom:18px;}
.t8b .body{gap:15px;}
.t8b .card{padding:22px 26px;}
.t8b .card.sm{padding:16px 18px;gap:7px;}
.t8b .g3{gap:18px;}
.t8b .g4{gap:16px;}
.t8b .duo>div{padding:20px 28px;gap:9px;}
.t8b .steps .s{padding:18px 22px 18px 0;}
.t8b .steps .s+.s{padding-left:22px;}
.t8b .land{padding-top:4px;padding-bottom:4px;}
.t8b .rows .r{padding:9px 0;}
"""

# ── C9 · R9 删文后的逐页视觉重排（撑满层）·只在 CONF_V2=1 装配 ─────────────────
#    删文的代价是掏空的半页；这一层把每张动刀页保留下来的元素放大、间距放开，
#    让页面重新长满 1920×1080。类名按 R9 完成后的最终页号命名，一页一档。
C9_CSS = """
/* ============ C9 · R9 · 删文后逐页撑满 ============ */
/* P14 案例01 · 96.5%：大数与九类信号图接管整页 */
.r9p14 .mega{gap:40px;}
.r9p14 .mega .mark{font-size:17px;margin-bottom:26px;}
.r9p14 .mega .mh{font-size:60px;}
.r9p14 .mega .num{font-size:336px;}
.r9p14 .mega .cap{font-size:38px;line-height:1.46;max-width:1000px;}
.r9p14 .mega .foot{font-size:26px;line-height:1.62;max-width:1010px;}
.r9p14 .m35{top:206px;width:640px;gap:36px;}
.r9p14 .m35 .mk{font-size:19px;margin-bottom:12px;}
.r9p14 .m35 .row{grid-template-columns:100px 1fr;column-gap:22px;row-gap:16px;}
.r9p14 .m35 .row .n{font-size:58px;}
.r9p14 .m35 .row .t{font-size:28px;}
.r9p14 .m35 .row .bar{height:12px;}
.r9p14 .m35 .sx{font-size:23px;line-height:1.66;padding-top:24px;}

/* P15 灵魂拷问：只剩一问，做成全页级大字 */
.r9p15 .ask{gap:64px;}
.r9p15 .ask .badge{font-size:21px;letter-spacing:.34em;}
.r9p15 .ask .badge::before{width:80px;}
.r9p15 .ask .q{font-size:112px;line-height:1.28;max-width:1680px;}

/* P22 商业模式变迁：图放大 + 英文判断句大字收底 */
.r9p22 .fig svg{width:1840px;}
.r9p22 .head{margin-bottom:30px;}
.r9p22 .body{gap:36px;}
.r9en{font-family:var(--f-mono);font-size:40px;font-weight:700;line-height:1.4;
  letter-spacing:.005em;border-left-color:var(--coral);padding-top:16px;padding-bottom:16px;}
.r9en b{color:var(--coral);font-weight:700;}

/* P23 同一把 Eval：全生命周期长图放大（.t8 的收紧在这里放回来） */
.r9p23 .wrap{padding-bottom:78px;}
.r9p23 .head{margin-bottom:34px;}
.r9p23 .body{gap:38px;}
.r9p23 .fig svg{width:1860px;}
.r9p23 .land{font-size:34px;}
.r9p23 .land .s{font-size:26px;}

/* P28 真实岗位上梯子：散点图放大撑满 */
.r9p28 .fig svg{width:1860px;height:auto;}
.r9p28 .head{margin-bottom:30px;}
.r9p28 .body{gap:32px;}
.r9p28 .foot{font-size:19px;}

/* P29 它决策，人审批：三格大数 + 两条走法图同时放大 */
.r9p29 .wrap{padding-bottom:76px;}
.r9p29 .head{margin-bottom:34px;}
.r9p29 .body{gap:40px;}
.r9p29 .stat .v{font-size:118px;}
.r9p29 .stat .l{font-size:26px;}
.r9p29 .stat .u{font-size:18px;}
.r9p29 .fig svg{width:1840px;}
.r9p29 .quote .en.sm{font-size:28px;line-height:1.44;}

/* P31 Waymo：图是主体，口播讲故事 */
.r9p31 .wrap{padding-bottom:64px;}
.r9p31 .head{margin-bottom:30px;}
.r9p31 .fig svg{width:1880px;}
.r9p31 .body{gap:32px;}
.r9p31 .land{font-size:33px;padding-top:10px;padding-bottom:10px;}
.r9p31 .land .s{font-size:25px;}

/* P43 对组织说：两扇门放大成整页主体 + 一句话收底 */
.r9p43 .wrap{padding-bottom:64px;}
.r9p43 .head{margin-bottom:30px;}
.r9p43 .fig svg{width:1780px;}
.r9p43 .body{gap:40px;}
.r9p43 .land{font-size:38px;line-height:1.44;padding-top:10px;padding-bottom:10px;}

/* P45 终页：尺子两面图放大居中 + 一句收场 */
.r9p45 .wrap{padding-bottom:80px;}
.r9p45 .head{margin-bottom:34px;}
.r9p45 .fig svg{width:1840px;}
.r9p45 .body{gap:40px;}
.r9p45 .quote .en{font-size:34px;line-height:1.4;}
.r9p45 .quote .by{font-size:19px;}
.r9p45 .land{font-size:42px;line-height:1.4;padding-top:8px;padding-bottom:8px;}
"""

if V2:
    # ── C8-① 钱 × 渗透拆回母版原版两页（撤销 C1 的 _secs[6] = F_MONEY 融合）────
    #    F_MONEY 定义保留（不装配），便于以后回退到融合版
    _secs[6], _secs[7] = _ORIG6, _ORIG7
    assert '这不是一个垂类' in _secs[6] and '预测还在打架' in _secs[7]

    # ── C8-② P9 承重页：末尾追加分论坛预告（陪伴半球交接给下午 AIoT 专场）────
    _r1(9, '是三年里最常见的<b>错位</b>。</span></div>',
           '是三年里最常见的<b>错位</b>。<br>陪伴那半球——从「被使用」到「被记住」——'
           '下午 AIoT 专场整场拆开讲；今天这场，直接从<b class="am">「被托付」</b>进。</span></div>')

    # ── C8-③ 暗线页（工具 → 实习生 → 外包 → 专家 → 合伙人）改写 ────────────
    #    原文三处指向已删的「上一幕」，全部改指下午专场
    _r1(25, '<div class="eyebrow flow" style="--i:0">同一个起点 · 上一幕走「陪伴」，这一幕走「干活」</div>',
            '<div class="eyebrow flow" style="--i:0">同一个起点 · 陪伴那条线走「熟人 → 伙伴」（下午专场），这条线走「干活」</div>')
    _r1(25, '<text class="lbl" x="1230" y="391" style="font-size:15px">消费级 · 陪伴 —— 上一幕走的那条</text>',
            '<text class="lbl" x="1230" y="391" style="font-size:15px">消费级 · 陪伴 —— 下午 AIoT 专场那条</text>')
    _r1(25, '<!-- 共同的根（上一幕那个工具） -->', '<!-- 共同的根（同一个工具起点） -->')

    # ── C8-④ PART 重编号：3→2 被托付 / 4→3 双向奔赴 / 5→4 人与组织 ──────────
    #    带幕名整串替换，顺序从大到小，避免链式误伤（chrome / 幕卡 / P5 三问卡片一次到位）
    for _a, _b in (('PART 5 · 人与组织', 'PART 4 · 人与组织'),
                   ('PART 4 · 双向奔赴', 'PART 3 · 双向奔赴'),
                   ('PART 3 · 被托付',   'PART 2 · 被托付')):
        _secs[:] = [x.replace(_a, _b) for x in _secs]

    # 幕卡上的大编号
    for _i, _o, _n in ((24, 'PART 3', 'PART 2'), (37, 'PART 4', 'PART 3'), (51, 'PART 5', 'PART 4')):
        _r1(_i, f'<div class="num flow" style="--i:0">{_o}</div>',
                f'<div class="num flow" style="--i:0">{_n}</div>')

    # 幕卡底部 rail：五站 → 四站（「02 被记住」整条撤掉）
    _RAIL = ('01 语法变了', '02 被托付', '03 双向奔赴', '04 人与组织')
    for _i, _cur in ((5, 0), (24, 1), (37, 2), (51, 3)):
        _m = re.search(r'<div class="rail">.*?</div>\n', _secs[_i], re.S)
        assert _m, f'_secs[{_i}] rail 定位失败'
        _new = ('<div class="rail">\n'
                + ''.join('      <span%s>%s</span>\n' % (' class="cur"' if _k == _cur else '', _t)
                          for _k, _t in enumerate(_RAIL))
                + '    </div>\n')
        _secs[_i] = _secs[_i].replace(_m.group(0), _new, 1)

    # ── C8-⑤ P5 提要页：全场路线 六站 → 五站（删「被记住」站，站间距重排）────
    #    x 由 80/388/696/1004/1312/1600 改为 80/460/840/1220/1600（等距 380）
    _cut1(4, '<!-- 全场路线', '</svg>', _ROUTE5)

    # ── C8-⑥ 幕序文字指涉全扫描修正（删章后整体前移一位）────────────────
    _r1(7, '这道题第三、四幕来解', '这道题第二、三幕来解')   # 渗透页（拆回后重新入场）
    _r1(43, '这六件事，第五幕会变成组织的授权语法', '这六件事，第四幕会变成组织的授权语法')
    _r1(57, '第四幕写给 Agent 的授权六件事', '第三幕写给 Agent 的授权六件事')
    _r1(51, '前面四幕讲的是「怎么造那把尺子」。', '前面三幕讲的是「怎么造那把尺子」。')
    # （_secs[50] QoT 页「第一幕留下的那格空白」指 PART 1 语法变了，编号未变，保留）

    # ── C8-⑦ 观点页 · 嘉宾金句重编号：删掉的 02 之后整体前移 ────────────────
    for _i, _o, _n in ((32, '03', '02'), (36, '04', '03'), (45, '05', '04'), (48, '06', '05')):
        _r1(_i, f'观点页 · 嘉宾金句 · {_o}', f'观点页 · 嘉宾金句 · {_n}')

    # ── C8-⑧ 灰字提亮（token 层：次级灰 → 近白，大屏可读性第一刀）──────────
    #    --mark-3 = 原次级灰：提亮只给「字」，图内灰圆点（紫/灰/金黄三分图例）仍按原灰
    for _o, _n in (('--ink-2:#c9c9d4;', '--ink-2:#E8E8F0;'),
                   ('--ink-3:#A5A5A5;', '--ink-3:#D9D9E3;\n  --mark-3:#A5A5A5;')):
        assert _head2.count(_o) == 1, f'C8 token 定位失败：{_o}'
        _head2 = _head2.replace(_o, _n, 1)

    # ── C8-⑩ 溢出页逐页微调：给需要的页挂 .t8 / .t8b（字号不回缩）───────────
    #    档位来自 43 页实测「.body 自然高 − 可用高」缺口：>40px 用 t8b，1–40px 用 t8
    _TIGHT = {6: 't8', 7: 't8', 25: 't8', 31: 't8', 35: 't8', 38: 't8b', 39: 't8b',
              42: 't8', 43: 't8b', 44: 't8b', 46: 't8', 53: 't8b', 54: 't8b',
              57: 't8b', 58: 't8'}
    for _i, _c in _TIGHT.items():
        assert _secs[_i].startswith('<section class="slide">'), f'_secs[{_i}] 起始标签异常'
        _secs[_i] = _secs[_i].replace('<section class="slide">', f'<section class="slide {_c}">', 1)

# ══════════════════════════════════════════════════════════════════════════════
# ── C9（2026-08-05 · R9 · 43 → 45 页 · Colin 逐页点名的大幅删文 + 两页拆分）────
# 评审结论：解释性文字整段交回口播，页面只留「他讲这一段时观众要看的东西」；
#   删完必须视觉重排撑满（放大保留元素 / 图表、调间距），不许出现掏空的半页。
#   ① P14 案例01 · 删三栏解读，大数与九类信号图放大
#   ② P15 灵魂拷问 · 删三栏证据，拷问做成全页级大字
#   ③ P16 Eval 融合页 · 拆回母版原两页（第一课 题之骗 / 第二课 整段），课序全链重排
#   ④ P22 商业模式变迁 · note 换英文判断句大字   ⑤ P23 同一把 Eval · 删三条件
#   ⑥ P28 真实岗位上梯子 · 删读图规则           ⑦ P29 它决策人审批 · 删三栏
#   ⑧ P31 Waymo · 删三栏，图放大成视觉主体
#   ⑨ P33 两道围栏合页 · 拆回母版原两页（C6 的「事前授权」修正移植进母版执行页）
#   ⑩ P43 对组织说 · 大清削（门下例子 / 01-04 四卡 / 2025 承接段 / land 只留一句）
#   ⑪ P45 终页 · 删解释性 note，land 压到一句收场
# 页码均按 R9 完成后的 45 页版；_secs 下标是母版 62 页的原始下标。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    def _cls(i, c):
        """给 _secs[i] 的 section 追加一个 class（保留 C8 已挂的 .t8/.t8b 档位）"""
        _m = re.match(r'<section class="slide([^"]*)">', _secs[i])
        assert _m, f'_secs[{i}] section 标签定位失败'
        _secs[i] = _secs[i].replace(_m.group(0), f'<section class="slide{_m.group(1)} {c}">', 1)

    def _ystretch(i, k, vb, paths=()):
        """把 _secs[i] 那张 svg 的纵向坐标整体拉伸 k 倍（字号 / 半径不变），viewBox 同步加高。
           删掉图下方那排文字之后，「宽而扁」的图靠这一手把整页撑满——比只放大宽度有效得多。
           y=/cy= 属性走正则；路径 d= 里的纵坐标必须逐条显式给出（paths），改漏了断言会炸。"""
        _a = _secs[i].index('<svg'); _b = _secs[i].index('</svg>') + 6
        _sv = _secs[i][_a:_b]
        for _o, _n in paths:
            assert _o in _sv, f'_secs[{i}] svg 纵拉伸 · 定位失败：{_o}'
            _sv = _sv.replace(_o, _n)
        _sv = re.sub(r'\b(c?y)="(-?\d+)"', lambda m: f'{m.group(1)}="{round(int(m.group(2)) * k)}"', _sv)
        assert _sv.count(vb[0]) == 1, f'_secs[{i}] svg 纵拉伸 · viewBox 定位失败'
        _sv = _sv.replace(vb[0], vb[1], 1)
        assert ' y="' not in _secs[i][:_a], f'_secs[{i}] svg 之外不应有 y 属性'
        _secs[i] = _secs[i][:_a] + _sv + _secs[i][_b:]

    # ── C9-① P14 案例 01 · 96.5% ───────────────────────────────────────────
    #    删「这个数字说明了什么 / 它没有说明什么 / 所以这一幕要讲」三栏；
    #    撑满：大数 236→330px、主句 46→60px、cap/foot 加大，九类信号图右移放大。
    _cut1(26, '\n    <div class="tri">', '剩下的全部难题都叫「凭什么信」。</div></div>\n    </div>')
    _cls(26, 'r9p14')

    # ── C9-② P15 灵魂拷问 ──────────────────────────────────────────────────
    #    删「不算数的证据 / 算数的证据 / 为什么这很重要」三栏；只剩拷问主句，
    #    撑满：拷问升到 .mq 级大字（104px），badge 放大，全页只此一问。
    _cut1(27, '\n    <div class="hint">', '一个审批权——不是换一个赞。</div></div>\n    </div>')
    _cls(27, 'r9p15')

    # ── C9-③ P16 Eval 第一课融合页 → 拆回母版原两页 ─────────────────────────
    #    C2 的 F_EVAL 在 V2 路径下不装配（定义保留，便于回退）；用 C8 同样的存底手法
    #    把 _secs[28]（你的 demo 在骗你 · 题之骗）/ _secs[29]（每一轮都对，整段却错了）
    #    原样拆回，再补 C8 的 PART 重编号（母版是 PART 3）。
    _secs[28], _secs[29] = _ORIG28, _ORIG29
    for _i in (28, 29):
        assert 'PART 3 · 被托付' in _secs[_i]
        _secs[_i] = _secs[_i].replace('PART 3 · 被托付', 'PART 2 · 被托付')
    assert '你的 demo 在骗你</h2>' in _secs[28] and '每一轮都对，整段却错了</h2>' in _secs[29]
    #    课序全链重排：融合页退场后，原第二课（裁判）→第三课、原第三课（听失败）→第四课
    for _i, _o, _n in ((30, 'Eval 第三课', 'Eval 第四课'), (31, 'Eval 第二课', 'Eval 第三课')):
        assert _secs[_i].count(_o) == 2, f'_secs[{_i}] 课序标记应为 chrome+eyebrow 两处'
        _secs[_i] = _secs[_i].replace(_o, _n)

    # ── C9-④ P22 商业模式变迁 · note → 英文判断句大字 ────────────────────────
    _r1(34, '<div class="note"><span class="flow" style="--i:9">最右边那一格，才是「被托付」在财务报表上的样子。'
            '<b>只有当供应商敢按结果收钱，客户才是真的把事交出去了。</b></span></div>',
            '<div class="land r9en flow" style="--i:9">You don’t pay for tokens, '
            'you pay for <b>business outcomes delivered</b>.</div>')
    _cls(34, 'r9p22')

    # ── C9-⑤ P23 同一把 Eval · 删「可判定 / 可归因 / 可控」三条件 ─────────────
    #    腾出来的 160px 交给全生命周期长图：纵坐标 ×1.45，图从一条细线长成整页主视觉
    _cut1(35, '\n      <div class="tri">', '改完能证明这一类不会再犯。</div></div>\n      </div>')
    _ystretch(35, 1.45, ('viewBox="0 0 1680 330"', 'viewBox="0 0 1680 479"'), paths=(
        ('d="M1530 148 C 1530 44, 130 44, 130 148"', 'd="M1530 215 C 1530 64, 130 64, 130 215"'),
        ('d="M130 170 H1530"', 'd="M130 247 H1530"'),
        ('d="M1005 120 V220"', 'd="M1005 174 V319"')))
    _cls(35, 'r9p23')

    # ── C9-⑥ P28 真实岗位上梯子 · 删三条读图规则，散点图放大撑满 ──────────────
    #    纵坐标 ×1.24：四条自治级别的行距拉开，散点图接管整页
    _cut1(40, '\n      <div class="tri" data-step="4">', '他们问「这个岗位能不能交」</b>。</div></div>\n      </div>')
    _ystretch(40, 1.24, ('width="1640" height="470" viewBox="0 0 1640 470"',
                         'width="1640" height="583" viewBox="0 0 1640 583"'), paths=(
        ('d="M190 400 H1590"', 'd="M190 496 H1590"'),
        ('d="M190 400 V70"', 'd="M190 496 V87"'),
        ('width="1400" height="120"', 'width="1400" height="149"')))
    _cls(40, 'r9p28')

    # ── C9-⑦ P29 它决策，人审批 · 删三栏解读 ─────────────────────────────────
    _cut1(42, '\n      <div class="tri">', '是<b>权责结构</b>。</div></div>\n      </div>')
    _cls(42, 'r9p29')

    # ── C9-⑧ P31 Waymo · 删三栏（现场 / 需求 / 落到语音），只留标题 + 图 + 一句收底 ──
    _cut1(44, '\n      <div class="tri">', '一个能被拦下来的对象</b>——和那双脚一样。</div></div>\n      </div>')
    _cls(44, 'r9p31')

    # ── C9-⑨ P33 两道围栏合页 → 拆回母版原两页 ──────────────────────────────
    #    C1 的 F_FENCE / C5 的 _SV_EXE_LR 在 V2 路径下不装配（定义保留）。
    #    母版执行页的闸门轴仍是旧文，C6 的两处修正在这里原样移植过来。
    _secs[46], _secs[47] = _ORIG46, _ORIG47
    for _i in (46, 47):
        assert 'PART 4 · 双向奔赴' in _secs[_i]
        _secs[_i] = _secs[_i].replace('PART 4 · 双向奔赴', 'PART 3 · 双向奔赴')
    assert '体验的围栏：交互行为，要有<em>规矩</em>' in _secs[46]
    assert '执行的围栏：语音的动作，<span class="co">最难在半路拦住</span>' in _secs[47]
    #    C6-② 移植：闸门轴第三节点「人工审批」→「事前授权」，引导行加「人工审批也前移」
    _r1(47, '<text class="txt fill-co" x="1240" y="526" text-anchor="middle">人工审批</text>',
            '<text class="txt fill-co" x="1240" y="526" text-anchor="middle">事前授权</text>')
    _r1(47, '<text class="lbl pop" style="--i:11" x="0" y="476">事后没有撤回键，那道闸门就只能整体前移到「说出口之前」</text>',
            '<text class="lbl pop" style="--i:11" x="0" y="476">事后没有撤回键，闸门整体前移到「说出口之前」——人工审批也前移：'
            '<tspan class="fill-am">批动作类别，不批每一句话</tspan></text>')
    #    幕序悬空清账：母版体验页 note 指的「第二幕」是已删的陪伴章
    _r1(46, '——这就是第二幕留下的那个坑，它的名字叫 backchannel。',
            '——<b>这个坑有名字，叫 backchannel。</b>')
    _cls(46, 'r9p33')
    _cls(47, 'r9p34')

    # ── C9-⑩ P43 对组织说 · 大清削 ──────────────────────────────────────────
    #    ⓐ 门下四行例子清单 ⓑ 01–04 四张卡 ⓒ 2025 承接段 ⓓ land 只留落点那一句
    #    ⓐ 连同整张图一起重画：例子清单撤掉，两扇门本身放大成整页主体
    #      （门的画法沿用 C6 收束页四资产带里那对门的写法：双向门来回箭头 / 单向门一堵挡回墙）
    _R9_DOORS = '''<svg width="1680" viewBox="0 0 1680 600" fill="none">
          <text class="lbl fill-co pop" style="--i:2" x="840" y="34" text-anchor="middle">这条线画在哪 —— 是 CEO 的活，不是 AI 负责人的活</text>

          <!-- 左区 · 可逆 · 双向门：推得开，也回得来 -->
          <rect class="pop" style="--i:3" x="60" y="96" width="880" height="430" rx="6" fill="var(--on-fill)" stroke="var(--amber)" stroke-width="2.4"/>
          <g class="pop" style="--i:4">
            <rect class="stroke-am" x="350" y="160" width="300" height="250" rx="5" stroke-width="3"/>
            <path class="stroke-am" stroke-width="2" opacity=".5" d="M500 160 V410"/>
          </g>
          <g class="pop" style="--i:5">
            <path class="stroke-am" stroke-width="3" d="M392 285 H608"/>
            <path class="fill-am" d="M348 285 L392 265 L392 305 Z"/>
            <path class="fill-am" d="M652 285 L608 265 L608 305 Z"/>
            <path class="stroke-am pkt" stroke-width="4"
              style="--pl:60px;--p0:60px;--p1:-216px;--pt:4.4s;--pd:1.2s" d="M392 285 H608"/>
          </g>
          <g class="pop" style="--i:5"><text class="ttl fill-am" x="500" y="474" text-anchor="middle" style="font-size:42px">可逆 · 双向门 · 放手做，不用批</text></g>

          <!-- 右区 · 不可逆 · 单向门：推开就没有回头 -->
          <rect class="pop" style="--i:6" x="940" y="96" width="680" height="430" rx="6" stroke="var(--coral)" stroke-width="2.4"/>
          <g class="pop" style="--i:6">
            <rect class="stroke-co" x="1130" y="160" width="300" height="250" rx="5" stroke-width="3"/>
            <path class="stroke-co" stroke-width="2" opacity=".5" d="M1280 160 V410"/>
          </g>
          <g class="pop" style="--i:7">
            <path class="stroke-co" stroke-width="5" d="M1150 205 V365"/>
            <path class="stroke-co" stroke-width="3" d="M1150 285 H1408"/>
            <path class="fill-co" d="M1452 285 L1408 265 L1408 305 Z"/>
          </g>
          <g class="pop" style="--i:7"><text class="ttl fill-co" x="1280" y="474" text-anchor="middle" style="font-size:42px">不可逆 · 单向门 · 先升级</text></g>

          <!-- 那条线 -->
          <path class="stroke-co dw" style="--len:520;--i:8" stroke-width="5" d="M940 70 V552"/>
        </svg>'''
    _cut1(57, '<svg width="1680" viewBox="0 0 1680 270" fill="none">', '</svg>', _R9_DOORS)
    _cut1(57, '\n      <div class="g4">', '退出标准 · 谁来喊停</div></div>\n      </div>')
    _cut1(57, '\n      <div class="note co flow" style="--i:12">2025 年我把它讲给产研团队',
              '一路跑到撞上一扇单向门。</div>')
    _r1(57, '<div class="land flow rev" style="--i:12">转身的落点就一句：<b>把权放给 high agency 的人</b>'
            '——他们会带着 Agent，把结果一起做出来。<span class="s">个人 agency 是能力，'
            '<b>组织 agency 是制度许可</b>：流程集中在不可逆风险上，自由留给可逆试验。'
            '第三幕写给 Agent 的授权六件事，<b>换个抬头，也该给人写一份</b>。</span></div>',
            '<div class="land flow rev" style="--i:8"><b>把权放给 high agency 的人</b>'
            '——他们会带着 Agent，把结果一起做出来。</div>')
    _cls(57, 'r9p43')

    # ── C9-⑪ P45 终页 · 删解释性 note，land 压到一句收场 ──────────────────────
    _cut1(58, '\n      <div class="note flow" style="--i:11">Weil 说的是向外那一面。',
              '是不敢定义「什么算做成」。</b></div>')
    _r1(58, '<div class="land flow" style="--i:12">去年结语我说：<b>AI 会重塑世界，而内观会重塑我们</b>。'
            '今年这句话长成了一把可以量的尺子——向外量它，叫 Eval；向内量自己，叫内观。'
            '<span class="s">一个决定产品能不能进化，一个决定我们自己能不能进化——'
            '愿我们在理解 Agent 的同时，也不忘理解自己。</span></div>',
            '<div class="land flow" style="--i:11">愿我们在理解 <b>Agent</b> 的同时，也不忘<b>理解自己</b>。</div>')
    _cls(58, 'r9p45')

if V2:
    _order = ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   # P1-10 · 开场四页 · PART1 幕卡 · 钱 · 渗透 · 四方观点 · 承重页
              + [11] + list(range(24, 28)))
    # ↑ C8：金句01 之后直接进 PART 2（原 PART 3）被托付 ——
    #        原 PART 2 陪伴整章（12 节：幕卡+9 内容页+金句02+反共识页）整章删除
else:
    _order = ([0, 1, 2, 3, 4, 5, 6, 8, 9]      # P1-6 · 融合钱×渗透 · 四方观点 · 融合阶段×北极星
              + list(range(11, 22)) + [23, 22] + list(range(24, 28)))
    # ↑ C5：金句02(23) 与 反共识页(22) 换序 —— 恰好半秒 → 视频 → 金句02 → 反共识 → PART 3
    #        反共识页后移，承上启下直接引出 PART 3（元素数仍 17）
_order += ([28, 31, 30]                        # Eval 第一课(一二合并) → 第二课(裁判,原四) → 第三课(听失败,方法论收尾)
          + list(range(32, 39))                  # MQ选评测 … 章节双向奔赴
          + [39, 40]                             # 爬梯×交叉验证(类比已并入) · 岗位
          + list(range(42, 46))                  # 协作审批 · 双围栏案例 · Waymo · MQ护城河
          + [46]                                 # 两道围栏合一(体验+执行,黑页撤回键随后)
          + list(range(48, 55))                  # MQ撤回键 … 对产品管理者
          + [56, 57]                             # 对 CEO 说 · 对组织说
          + [60, 58])                            # 收束 → 尺子两面收全场
if V2:
    # ── C9-③/⑨ 拆页入列（承上面 C9 层）：融合页退场，母版原两页各自成页 ──────
    #    Eval：第一课(题之骗) → 第二课(整段) → 第三课(裁判,原四) → 第四课(听失败)
    #    围栏：体验的围栏 → 执行的围栏
    for _a, _b in ((28, 29), (46, 47)):
        assert _order.count(_a) == 1 and _b not in _order, f'C9 拆页入列定位失败：{_a}/{_b}'
        _order.insert(_order.index(_a) + 1, _b)
s = _head2 + '\n'.join(_secs[o] for o in _order) + _tail2
_n_cut = 45 if V2 else 54
assert len(re.findall(r'<section class="slide', s)) == _n_cut, f"压缩后应 {_n_cut} 页"

# ── 6.5) 媒体层（仅大会版；母版/线上 /cowork 保持无媒体） ────
# a) P3 页内录音（真实外呼片段，完美嵌入，无需解说文字）
CHROME3 = '<div class="chrome"><span>PART 0 · 开场</span><span>3</span></div>'
assert s.count(CHROME3) == 1, "P3 chrome 定位失败"
AUDIO = (CHROME3 + '\n  <audio data-dm src="/media/cowork/p3-call.mp3" preload="auto"></audio>'
         '\n  <div class="dm-ind" aria-hidden="true"></div>')
s = s.replace(CHROME3, AUDIO, 1)

# b) 全幅视频页（陪伴类智能体 · 多模态交互 demo，无文字）
if V2:
    # C8：视频页随 PART 2 陪伴整章一并撤除 —— 锚点「恰好的那半秒」页已不在本场，
    #     视频改由下午 AIoT 专场承载。
    assert '恰好的那半秒' not in s, "C8：陪伴章已删，视频锚点不应仍在"
    assert 'gemini-demo.mp4' not in s, "C8：视频页应已随陪伴章撤除"
else:
    VIDEO = '''<section class="slide">
  <div class="vslide">
    <video data-dm src="/media/cowork/gemini-demo.mp4" preload="auto" playsinline></video>
    <div class="dm-ind" aria-hidden="true"></div>
  </div>
</section>
'''
    # 内容锚定（C5 改挂）：插在「恰好的那半秒」页之后 —— 反共识页已后移到金句02 之后，
    # 视频不再跟着它走；锚点用该页 h2 全串（跟随内容移动，不吃页码位移）
    _vs = [m.start() for m in re.finditer(r'<section class="slide', s)]
    assert len(_vs) == 54, f"压缩层后应 54 页，实际 {len(_vs)}"
    _ANCHOR = '<h2 class="ink" style="--i:1">恰好的那半秒，比快半秒值钱</h2>'
    assert s.count(_ANCHOR) == 1, "视频锚点定位失败"
    _ai = s.index(_ANCHOR)
    _ae = s.index('</section>', _ai) + len('</section>')
    s = s[:_ae] + '\n' + VIDEO.rstrip('\n') + s[_ae:]

# c) 页码重排：每个 chrome 第二个 span = 所属 slide 的 1-based 序号
starts = [m.start() for m in re.finditer(r'<section class="slide', s)]
def _renum(mm):
    idx = sum(1 for st in starts if st <= mm.start())
    return mm.group(1) + str(idx) + mm.group(2)
s = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _renum, s)

# d) 媒体行为脚本：包装 deck 控制器（第一按播，再按停+翻页；M 键手动）
MEDIA_JS = '''<script>
/* deck-media：媒体页按键行为与 PPT 对齐 */
(function(){
  function init(){
    var d=window.deck; if(!d||!d.slides){return setTimeout(init,120);}
    var played={};
    function m(i){var sl=d.slides[i];return sl?sl.querySelector('[data-dm]'):null;}
    function stop(i){var x=m(i);if(x){x.pause();try{x.currentTime=0;}catch(e){}d.slides[i].classList.remove('dm-playing');}}
    var oN=d.next.bind(d), oP=d.prev.bind(d), oG=d.go.bind(d);
    d.next=function(){
      var i=d.i, x=m(i);
      if(x && !played[i]){
        played[i]=1;d.slides[i].classList.add('dm-playing');
        try{x.currentTime=0;}catch(e){}
        var p=x.play(); if(p&&p.catch)p.catch(function(){});
        x.onended=function(){d.slides[i].classList.remove('dm-playing');};
        return;
      }
      if(x){stop(i);}
      oN();
    };
    d.prev=function(){stop(d.i);played[d.i]=0;oP();};
    d.go=function(n,a,b){if(typeof n==='number'&&n!==d.i){stop(d.i);played[d.i]=0;}return oG(n,a,b);};
    document.addEventListener('keydown',function(e){
      if(e.target&&e.target.getAttribute&&e.target.getAttribute('contenteditable'))return;
      if(e.key==='m'||e.key==='M'){
        var x=m(d.i); if(!x)return;
        if(x.paused){played[d.i]=1;d.slides[d.i].classList.add('dm-playing');var p=x.play();if(p&&p.catch)p.catch(function(){});}
        else{x.pause();d.slides[d.i].classList.remove('dm-playing');}
        e.preventDefault();
      }
    });
  }
  init();
})();
</script>'''
bi = s.rindex('</body>')
s = s[:bi] + MEDIA_JS + '\n' + s[bi:]

# ── 7) 大会版式覆盖层（追加在主 CSS 之后，级联取胜） ─────────
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
/* deck-media · 页内音视频（PPT 对齐：前进键先播，再按翻页） */
.dm-ind{position:absolute;right:64px;bottom:56px;width:10px;height:10px;border-radius:50%;background:var(--amber);opacity:0;transition:opacity .4s;z-index:40;}
.slide.dm-playing .dm-ind{opacity:.9;animation:dmpulse 1.1s ease-in-out infinite;}
@keyframes dmpulse{0%,100%{transform:scale(1);opacity:.9;}50%{transform:scale(1.55);opacity:.45;}}
.vslide{position:absolute;inset:0;background:#000;display:flex;align-items:center;justify-content:center;}
.vslide video{width:100%;height:100%;object-fit:contain;background:#000;}
"""
CONF_CSS = CONF_CSS.replace("__LOGO__", LOGO).replace("__COVER__", COVER).replace("__VENUE__", VENUE)
CONF_CSS += FIX_CSS         # 两版共用 · 多行 note clip-path 真 bug 修复
if V2:
    CONF_CSS += C8_CSS      # C8 · 次级文字 +2px 覆盖层（必须排在 conf 版式层之后）
    CONF_CSS += C9_CSS      # C9 · R9 删文后逐页撑满（必须排在 C8 +2px 之后）
# 插到最后一个 </style> 前（主样式表尾部）
li = s.rindex("</style>")
s = s[:li] + CONF_CSS + s[li:]

open(OUT, "w", encoding="utf-8").write(s)
n = len(re.findall(r'<section class="slide', s))
_n_out = 45 if V2 else 55
assert n == _n_out, f"{'R9 聚焦版' if V2 else '大会版'}应为 {_n_out} 页，实际 {n}"
print(f"{OUT.split('/')[-1]} written · {n} slides · {len(s)//1024}KB")
assert "deckRuler" in s and "noindex" in s
# 两版共用：多行 note clip-path 真 bug 修复必须在位
assert ".note>span.flow,.note>span.flow.rev,.note>.flow{display:inline-block;}" in s, "FIX_CSS 未装配"
# C2/C3 内容在位（防「定义了未装配」）
_MK = ["HUMAN IN THE LOOP", "Eval 第二课", "交叉验证 · 两个行业的断层",
       "本场提要</h2>", "四个互不相干的人，说了", "商业模式变迁", "人还在不在环里</em></h2>", "就是「按结果收钱」的计费口径",
       "四个阶段，四颗", "一个新的融合岗位", "一套放权与决策机制", "OpenAI 前 CPO",
       "紫 = 已规模商业化", "金黄 = 强监管场景", "这条弧线不存在", "文本通道 · TEXT CHANNEL", "语音通道 · VOICE CHANNEL",
       'd="M675 6 V172"']
if not V2:
    # 陪伴章内容 + C1/C2 两张融合页（V2 已被 C8/C9 拆回母版原页，融合页定义保留但不装配）
    _MK += ["不应该</em>被记住", "题之骗 × 粒度之骗", "单轮打分", "TWO FENCES"]
for _mk in _MK:
    assert _mk in s, f"C2/C3/C4/C5 内容缺失：{_mk}"
assert ("Eval 第四课" in s) == V2, "课序：V2 应有第四课（听失败），55 页版不应有"
assert "暖橙 = 已规模商业化" not in s and "粉 = 强监管场景" not in s
# C6 内容在位 / 悬空引用清零
_MK6 = ["事前授权", "批动作类别，不批每一句话",
        "这六件事，第四幕会变成组织的授权语法" if V2 else "这六件事，第五幕会变成组织的授权语法",
        "边界 / BOUNDARY", "结果 / ACCOUNTABILITY", "可撤销 / RECOVERABILITY",
        "授权可撤销（随时降级、随时回滚）", "把权放给 high agency 的人"]
if not V2:
    _MK6.append("《人和组织，必须一起转身》")   # C9 · R9 把 P43 的 2025 承接段整段删掉
for _mk in _MK6:
    assert _mk in s, f"C6 内容缺失：{_mk}"
assert "授权书" not in s, "C6：《Agent 授权书》已删页，正文不应再出现该字样"
assert "进化速度，等于我们的放权速度" not in s, "C6：收束页 land 应已随汇聚箭头一并撤掉"
assert 'text-anchor="middle">人工审批</text>' not in s, "C6：闸门轴第三节点应已从「人工审批」改成「事前授权」"
_p54 = s[s.index('全场收束 · ONE LINE EACH'):]
_p54 = _p54[:_p54.index('</section>')]
for _w in ('>评测</text>', '>岗位</text>', '>结果生意</text>', '>放权决策机制</text>'):
    assert _w in _p54, f"C6 · P54 四资产带缺失：{_w}"

if V2:
    # ── C8 内容在位 / 陪伴章清零 / 视觉第一刀在位 ────────────────────────
    for _mk in ("下午 AIoT 专场整场拆开讲", "直接从<b class=\"am\">「被托付」</b>进",
                "陪伴那条线走「熟人 → 伙伴」（下午专场）", "消费级 · 陪伴 —— 下午 AIoT 专场那条",
                "PART 2 · 被托付", "PART 3 · 双向奔赴", "PART 4 · 人与组织",
                "这不是一个垂类", "预测还在打架",
                "观点页 · 嘉宾金句 · 05", "前面三幕讲的是",
                "这道题第二、三幕来解",
                "--ink-3:#D9D9E3;", "--ink-2:#E8E8F0;", ".note{font-size:24px"):
        assert _mk in s, f"C8 内容缺失：{_mk}"
    for _mk in ("PART 5", "PART 2 · 被记住", "观点页 · 嘉宾金句 · 06", "恰好的那半秒", "gemini-demo.mp4",
                "class=\"vslide\"><", "值得被记住的存在", "本场第一处反共识", "第五幕", "上一幕",
                "--ink-3:#A5A5A5", "--ink-2:#c9c9d4"):
        assert _mk not in s, f"C8 残留未清：{_mk}"
    # 幕卡 rail 四站 / P5 路线五站
    assert s.count('<span>02 被托付</span>') + s.count('<span class="cur">02 被托付</span>') == 4
    assert '>02 被记住<' not in s, "C8：幕卡 rail 不应再有「02 被记住」站"
    assert s.count('y="80" text-anchor="middle">PART') == 5, "C8 · P5 路线应为五站"
    _p5 = s[s.index('<!-- 全场路线'):]; _p5 = _p5[:_p5.index('</svg>')]
    assert '被记住' not in _p5, "C8 · P5 路线应已删「被记住」站"

    # ── C9 · R9 删文到位 / 拆页到位 / 撑满层在位 ──────────────────────────
    #    ⓐ 逐页负向断言：每张动刀页抽一句被删原文，必须查无此句
    for _mk in ("工程上已经基本解完了",                  # P14 · 这个数字说明了什么
                "两把完全不同的尺子",                      # P14 · 它没有说明什么
                "剩下的全部难题都叫「凭什么信」",           # P14 · 所以这一幕要讲
                "大模型评分 4.6 分",                       # P15 · 不算数的证据
                "失败样本能追到具体哪一步的",               # P15 · 算数的证据
                "不是换一个赞",                            # P15 · 为什么这很重要
                "最右边那一格，才是「被托付」在财务报表上的样子",  # P22 · 原 note
                "两个人分别判，结论一样",                   # P23 · 条件 01
                "识别、检索、决策，还是话术",               # P23 · 条件 02
                "改完能证明这一类不会再犯",                 # P23 · 条件 03
                "只等于人退得越远",                        # P28 · 读图规则 01
                "未必是自治级别最高的那一列",               # P28 · 读图规则 02
                "这个岗位能不能交",                        # P28 · 读图规则 03
                "责任必须落在一个能被追责的主体上",         # P29 · 审批不是为了审得更准
                "准确率和问责，是两件事",                   # P29 · 给企业组织的提醒
                "它约束的从来不是能力",                     # P29 · 这一条不会过时
                "捞回一双正在移动的脚",                     # P31 · 现场 · 有惊无险
                "中间隔着一条被写下来的需求",               # P31 · 刹得住是因为有人写过
                "和那双脚一样",                            # P31 · 落到语音上
                "找十个客户聊聊", "改一版提示词",           # P43 · 双向门例子
                "改一条红线", "换掉一条业务规则",           # P43 · 单向门例子
                "没有名字的授权，是一句好听的话",           # P43 · 01 结果归谁
                "就是上面那条线", "拿不到，就等于没授",     # P43 · 02 / 03
                "没有退出标准的授权，最后都会烂尾",         # P43 · 04 什么时候停
                "2025 年我把它讲给产研团队",               # P43 · 2025 承接段
                "组织 agency 是制度许可",                   # P43 · 原 land 长尾
                "Weil 说的是向外那一面",                    # P45 · 解释性 note
                "去年结语我说"):                            # P45 · 原 land 长尾
        assert _mk not in s, f"C9 · R9 该删未删：{_mk}"
    #    ⓑ 拆页与课序：Eval 四课全在、母版原两页在位；两道围栏各自成页
    for _mk in ("你的 demo 在骗你</h2>", "每一轮都对，整段却错了</h2>",
                "Eval 第一课", "Eval 第二课", "Eval 第三课", "Eval 第四课",
                "体验的围栏：交互行为，要有<em>规矩</em>",
                "执行的围栏：语音的动作，<span class=\"co\">最难在半路拦住</span>",
                "这个坑有名字，叫 backchannel",
                "You don’t pay for tokens", "business outcomes delivered",
                "愿我们在理解 <b>Agent</b> 的同时",
                "可逆 · 双向门 · 放手做，不用批", "不可逆 · 单向门 · 先升级",
                ".r9p14 .mega .num{font-size:336px;}", ".r9en{font-family:var(--f-mono)"):
        assert _mk in s, f"C9 · R9 内容缺失：{_mk}"
    #    ⓒ 课序链：第一课 → 第二课 → 第三课(裁判) → 第四课(听失败)，正序出现
    _ke = [s.index(f'>Eval 第{_c}课</div>') for _c in '一二三四']
    assert _ke == sorted(_ke), f"C9 · Eval 课序错位：{_ke}"
    assert '裁判' in s[_ke[2]:_ke[3]] and '一百条真实的失败' in s[_ke[3]:], "C9 · 第三/四课内容与课号错配"
    #    ⓓ 事前授权必须落在「执行的围栏」那一页（而不是别处）
    _pfe = s[s.index('执行的围栏：语音的动作'):]
    _pfe = _pfe[:_pfe.index('</section>')]
    assert '事前授权' in _pfe and '批动作类别，不批每一句话' in _pfe, "C9 · 事前授权未落在执行围栏页"
    print("ruler ✓ noindex ✓ C2/C3 content ✓ C8 R8v1 ✓ C9 R9 45p ✓")
else:
    # ── C5 换序：视频页在「恰好的那半秒」之后、金句02 之前；反共识页排在金句02 之后
    _i_half, _i_video = s.index('恰好的那半秒'), s.index('gemini-demo.mp4')
    _i_mq02, _i_anti = s.index('值得被记住的存在'), s.index('本场第一处反共识')
    assert _i_half < _i_video < _i_mq02 < _i_anti, "C5 换序失败：恰好半秒 → 视频 → 金句02 → 反共识"
    # ── 55 页线上版：C8 的一切都不应出现（陪伴章 / 五幕编号 / 金句06 / 原 token / 溢出档）
    for _mk in ("PART 2 · 被记住", "PART 5 · 人与组织", "观点页 · 嘉宾金句 · 06",
                "--ink-3:#A5A5A5;", "--ink-2:#c9c9d4;", 'class="vslide"'):
        assert _mk in s, f"55 页版内容缺失：{_mk}"
    for _mk in ("下午 AIoT 专场", "--ink-3:#D9D9E3", "--mark-3:", ".note{font-size:24px",
                '<section class="slide t8', "PART 4 · 人与组织"):
        assert _mk not in s, f"55 页版不应含 C8 产物：{_mk}"
    print("ruler ✓ noindex ✓ C2/C3 content ✓")
