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

# ── C10 · R10 删文后的逐页视觉重排（撑满层）·只在 CONF_V2=1 装配 ────────────────
#    与 C9_CSS 同规矩：类名按 45 页版最终页号命名，一页一档，排在 C9_CSS 之后。
#    这一轮八页里有三页是「重构」而不是「删句」——P5 路线图升主体、P37 四坐标接管、
#    P45 纯图收场——所以档位里除了放大，还带版式（.body 分配、图内字号）的重写。
C10_CSS = """
/* ============ C10 · R10 · 八页删改后逐页撑满 ============ */
/* ⚠️ 撑满只有两把真刀：svg 的 viewBox（_ystretch）与字号。
      给 .fig svg 写 width:18xx 是无效的——.fig 是 flex 容器，超过 1680 的
      svg 会被 flex-shrink 压回 1680（母版正文栅格宽），C9 那几条 width 即属此列。 */

/* P5 本场提要：三问卡与 note 撤走，五站路线图升为全页主体（svg 已纵向 ×4.6） */
.r10p5 .wrap{padding-bottom:64px;}
.r10p5 .head{margin-bottom:22px;}
.r10p5 .body{gap:0;justify-content:center;}
.r10p5 .fig .lbl{font-size:30px;letter-spacing:.22em;}
.r10p5 .fig .txt{font-size:76px;font-weight:700;fill:var(--ink);}
.r10p5 .fig .sm{font-size:34px;}

/* P18 Eval 第三课 · 裁判：删三条「正确的看法」，两遍质检对照条放大（svg ×1.5） */
.r10p18 .wrap{padding-bottom:72px;}
.r10p18 .head{margin-bottom:32px;}
.r10p18 .body{gap:44px;}
.r10p18 .fig .lbl{font-size:27px;letter-spacing:.1em;}
.r10p18 .land{font-size:40px;line-height:1.4;}
.r10p18 .land .s{font-size:28px;margin-top:12px;}

/* P22 商业模式变迁：英文判断句 + 中文翻译行（同 land 体系，次一级字号） */
.r10p22 .wrap{padding-bottom:74px;}
.r10p22 .body{gap:46px;}
.r9en .s{font-family:var(--f-cn);font-size:30px;font-weight:400;line-height:1.46;
  letter-spacing:0;color:var(--ink-2);margin-top:16px;}

/* P27 爬梯页：note 与 foot 撤走，梯子图（svg ×1.13）+ 交叉验证条带接管整页。
   字号只小步加——底部条带那两行本来就贴得紧，加大了会撞在一起。 */
.r10p27 .wrap{padding-bottom:56px;}
.r10p27 .head{margin-bottom:30px;}
.r10p27 .body{gap:30px;}
.r10p27 .fig .lbl{font-size:19px;}
.r10p27 .fig .txt{font-size:22px;}
.r10p27 .fig .sm{font-size:18px;}

/* P29 它决策，人审批：英文引文块撤走，三格大数与两条走法图（svg ×1.9）再放大 */
.r10p29 .wrap{padding-bottom:74px;}
.r10p29 .body{gap:56px;}
.r10p29 .stat .v{font-size:132px;}
.r10p29 .stat .l{font-size:29px;}
.r10p29 .stat .u{font-size:19px;}
.r10p29 .fig .lbl{font-size:23px;}
.r10p29 .fig .sm{font-size:23px;}

/* P37 QoT：三卡 + 两段解释撤走，四条工程坐标升为页面主体（四列 · 大字为主）。
   .take.qot4 的特异性必须压过母版 .take .c:nth-child(n) —— 四条是并列关系，
   不是递进关系，所以字号一致、左边框一律走 amber。 */
.r10p37 .wrap{padding-bottom:70px;}
.r10p37 .head{margin-bottom:30px;}
.r10p37 .body{gap:56px;}
.r10p37 .fig .lbl{font-size:19px;}
.r10p37 .fig .sm{font-size:22px;}
.take.qot4{gap:30px;}
.take.qot4 .c{gap:16px;padding:8px 0 8px 28px;border-left:4px solid var(--amber);}
.take.qot4 .c .ord{font-family:var(--f-en);font-size:27px;font-weight:900;color:var(--amber);}
.take.qot4 .c .who{font-size:50px;font-weight:700;line-height:1.16;
  letter-spacing:-.015em;color:var(--ink);}
.take.qot4 .c .lat{font-family:var(--f-mono);font-size:19px;letter-spacing:.16em;
  color:var(--ink-3);}
.take.qot4 .c .s{font-size:27px;font-weight:300;line-height:1.5;color:var(--ink-2);}

/* P39 对个人说：land 撤走，暴露量折线（svg ×1.4）与四阶卡一起放大 */
.r10p39 .wrap{padding-bottom:70px;}
.r10p39 .head{margin-bottom:32px;}
.r10p39 .body{gap:52px;}
.r10p39 .fig .lbl{font-size:22px;}
.r10p39 .fig .txt{font-size:24px;}
.r10p39 .fig .sm{font-size:24px;}
.r10p39 .card.sm{padding:26px 28px;gap:12px;}
.r10p39 .card .n{font-size:44px;}
.r10p39 .card .t{font-size:31px;}
.r10p39 .card .d{font-size:24px;line-height:1.52;}

/* P45 终页：引文卡与结语撤走，向外/向内那把尺子摊开成整页（svg ×1.7）· 纯视觉收场。
   .lbl 保持母版字号 —— 行首那两个 mono 标签（外 · 读 AGENT / 内 · 读自己）
   离第一列正文只有 180 个单位，一加大就骑到正文上。 */
.r10p45 .wrap{padding-bottom:64px;}
.r10p45 .head{margin-bottom:26px;}
.r10p45 .body{gap:0;justify-content:center;}
.r10p45 .fig .txt{font-size:28px;}
"""

# ── C11 · R11 删文/换血后的逐页视觉重排（撑满层）·只在 CONF_V2=1 装配 ────────────
#    同 C9/C10 规矩：类名按 45 页版最终页号命名，一页一档，排在 C10_CSS 之后。
#    仍然记住 C10 顶部那条：撑满只有 viewBox（_ystretch）与字号两把真刀，
#    给 .fig svg 写 width:18xx 无效（.fig 是 flex 容器，超过 1680 会被压回去）。
C11_CSS = """
/* ============ C11 · R11 · 十三页删改与数据换血后逐页撑满 ============ */
/* P3 录音页：两块口播结论撤走，波形（svg ×2）接管上半页，2025/2026 两栏放大 */
.r11p3 .wrap{padding-bottom:64px;}
.r11p3 .head{margin-bottom:30px;}
.r11p3 .body{gap:34px;}
.r11p3 .fig .lbl{font-size:19px;}
.r11p3 .fig .sm{font-size:22px;}
.r11p3 .duo>div{padding:30px 34px;gap:14px;}
.r11p3 .duo .h{font-size:19px;}
.r11p3 .duo .b{font-size:42px;line-height:1.3;}
.r11p3 .quote .en.sm{font-size:27px;line-height:1.5;}
.r11p3 .foot{font-size:24px;}

/* P5 本场提要：路线图四站（站距 ≈487），比五站时多出的横向余量还给字号 */
.r11p5 .fig .txt{font-size:82px;}
.r11p5 .fig .sm{font-size:36px;}
.r11p5 .fig .lbl{font-size:32px;}

/* P8 渗透页：企业侧四条 + 消费侧一条，条目变少，行文与大数一起加大 */
.r11p8 .fig .txt{font-size:25px;}
.r11p8 .fig .lbl{font-size:20px;}
.r11p8 .fig .big{font-size:56px;}
.r11p8 .foot{font-size:19px;line-height:1.6;max-width:1680px;}

/* P9 四个互不相干的人：结论行是这一页的落点，抬到 land 级字重 */
.r11p9 .body{gap:34px;}
.r11p9 .fig .ttl{font-size:31px;}
.r11p9 .fig .sm{font-size:21px;}
.r11p9 .fig .lbl{font-size:18px;}
.r11p9 .note{font-size:29px;line-height:1.55;color:var(--ink);font-weight:400;}

/* P10 四阶段四北极星：边界声明 foot 撤走，折线（svg ×1.08）与四颗星一起放大 */
.r11p10 .body{gap:30px;}
.r11p10 .fig .lbl{font-size:18px;}
.r11p10 .fig .txt{font-size:23px;}
.r11p10 .nstar .ns b{font-size:29px;}
.r11p10 .nstar .ns span{font-size:17px;}

/* P19 Eval 第四课：四步文字并进图内（图 364 → 522），下方四块撤走，图升整页主体 */
.r11p19 .wrap{padding-bottom:60px;}
.r11p19 .head{margin-bottom:28px;}
.r11p19 .body{gap:32px;}
.r11p19 .fig .lbl{font-size:18px;}
.r11p19 .fig .sm{font-size:21px;}
.r11p19 .fig .txt{font-size:26px;}

/* P21 案例 02：3.08% × 1.5% 双大数对比接管页面（三格 + note 撤走）。
   两个数一紫一灰 —— 紫的是 AI，灰的是人工那条谁也压不下去的底线。 */
.r11p21 .body{gap:32px;}
.cmp2{display:grid;grid-template-columns:1fr auto 1fr;gap:56px;align-items:center;}
.cmp2 .c{display:flex;flex-direction:column;gap:10px;}
.cmp2 .c .k{font-family:var(--f-mono);font-size:17px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink-3);}
.cmp2 .c .v{font-family:var(--f-en);font-size:116px;font-weight:900;line-height:.9;
  letter-spacing:-.035em;color:var(--ink-3);}
.cmp2 .c.am .v{color:var(--amber);}
.cmp2 .c .l{font-size:32px;font-weight:700;line-height:1.28;color:var(--ink);}
.cmp2 .c .u{font-size:21px;font-weight:300;line-height:1.5;color:var(--ink-2);}
.cmp2 .vs{font-family:var(--f-mono);font-size:24px;letter-spacing:.24em;color:var(--ink-3);}

/* P22 商业模式变迁：中文行升为主句，英文降为原文补充，末行标出处 */
.r11pay{border-left-color:var(--coral);font-size:36px;line-height:1.4;
  padding-top:14px;padding-bottom:14px;}
.r11pay .en{display:block;font-family:var(--f-mono);font-size:26px;font-weight:700;
  line-height:1.42;letter-spacing:.005em;color:var(--ink-2);margin-top:14px;}
.r11pay .en b{color:var(--coral);font-weight:700;}
.r11pay .src{display:block;font-family:var(--f-mono);font-size:17px;letter-spacing:.08em;
  font-weight:400;color:var(--ink-3);margin-top:10px;}

/* P29 它决策，人审批：版面对调 —— 两条走法图上，三个大数下并缩小 */
.r11p29 .body{gap:60px;}
.r11p29 .stat{gap:11px;}
.r11p29 .stat .v{font-size:88px;}
.r11p29 .stat .l{font-size:24px;}
.r11p29 .stat .u{font-size:16px;}

/* P30 案例 03：图最上并放大（svg ×1.55），事件叙述缩小沉底作注释行 */
.r11p30 .body{gap:24px;}
.r11p30 .fig .lbl{font-size:19px;}
.r11p30 .fig .sm{font-size:23px;}
.r11p30 .old.tail{background:none;border:none;border-top:1px solid var(--hair);
  border-radius:0;padding:14px 0 0;gap:6px;}
.r11p30 .old.tail .yr{font-size:13px;}
.r11p30 .old.tail .tx{font-size:18px;line-height:1.5;font-weight:300;color:var(--ink-3);}

/* P33 体验的围栏：backchannel 那条 note 撤走，波形图与四张卡一起放开 */
.r11p33 .body{gap:32px;}
.r11p33 .card.sm{padding:24px 26px;gap:11px;}

/* P36 五条准入线全景：下方只留一句，四条产品线的能力矩阵放大（svg ×1.18） */
.r11p36 .wrap{padding-bottom:60px;}
.r11p36 .head{margin-bottom:30px;}
.r11p36 .body{gap:30px;}
.r11p36 .fig .lbl{font-size:18px;}
.r11p36 .fig .sm{font-size:19px;}
"""

# ── C12 · R12 新页「AI 投资资金流向 2024→2026」的页级档 ·只在 CONF_V2=1 装配 ─────
#    这一轮不是删文撑满，而是**新增一页**（45 → 46），所以档位里只有新页一档 .r12flow。
#    图是「时间 × 层级」的资金流向带：三条横带（基础模型 / Coding / 对话式 AI），
#    每条带按 2024 / 2025 / 2026 三段给不同 stroke-width —— 带宽是量级示意，
#    真数全部以文字标在带上，口径与来源逐条写进 foot（不造数）。
C12_CSS = """
/* ============ C12 · R12 · 新页「钱的三次落点」（PART 1 数据开场第一页）============ */
/* 大屏可读优先：图内三级字号全部上调；.big 是三条带上的钱数（母版 44px 紫），
   这一页的 .big 要跟着带走灰 / 走 amber 两种色，所以色由 fill-* 类另给。 */
.r12flow .wrap{padding-bottom:56px;}
.r12flow .head{margin-bottom:26px;}
.r12flow .body{gap:26px;}
.r12flow .fig .lbl{font-size:21px;letter-spacing:.16em;}
.r12flow .fig .ttl{font-size:30px;}
.r12flow .fig .txt{font-size:25px;}
.r12flow .fig .sm{font-size:22px;}
.r12flow .fig .big{font-size:40px;fill:var(--ink);}
.r12flow .fig .big.fill-am{fill:var(--amber);}
.r12flow .note{font-size:26px;}
.r12flow .foot{font-size:16px;line-height:1.62;max-width:1680px;}
"""

# ── C13 · R13 七处内容修订的页级档 ·只在 CONF_V2=1 装配 ────────────────────────
#    这一层里只有一处是「回调」（P5 路线图字号从 R10/R11 的 76→82px 收回 46px），
#    其余六处都是内容层动作（补引文 / 补金句 / 改拼读法 / 纠表意 / 换两张金句页），
#    所以档位很薄：一页一档，全部排在 C12_CSS 之后（同名属性后写者胜）。
C13_CSS = """
/* ============ C13 · R13 · 七处内容修订 ============ */
/* P4 一个人都没有：左栏两条引文叠成一摞 —— 2026 的 Bret 与 1876 的贝尔，
   一页之内把「150 年」这件事从文字变成两个可以并排读的时间点。 */
.r13bell .qstack{display:flex;flex-direction:column;gap:24px;align-self:center;}
.r13bell .qstack .quote .en.sm{font-size:23px;line-height:1.46;}
.r13bell .qstack .quote.co .en.sm{font-family:var(--f-mono);font-size:21px;color:var(--ink-2);}
.r13bell .qstack .quote.co .by{margin-top:10px;text-transform:none;letter-spacing:.1em;}

/* P5 本场提要：R10 的 ×4.6 把站名推到 76px、R11 再推到 82px，顶格失了美感。
   R13 回调到「大而清爽」的优雅档 —— 站名 46 / PART 标 24 / 副题 25，
   圆点半径与线宽同步回收，四行在 665 的 viewBox 里居中排开、上下留白各 ≈120。 */
.r13p5 .head{margin-bottom:26px;}
.r13p5 .fig .txt{font-size:46px;}
.r13p5 .fig .sm{font-size:25px;}
.r13p5 .fig .lbl{font-size:24px;letter-spacing:.2em;}

/* P16 灵魂拷问：问句仍是主体（112 → 96px 给第二拍让位），
   Weil 金句作 data-step=1 的第二拍落在下方（英文 mono + 署名行）。 */
.r13ask .ask{gap:56px;}
.r13ask .ask .q{font-size:96px;}
.r13ask .ask .quote{max-width:1420px;border-left-width:4px;padding-left:32px;}
.r13ask .ask .quote .en{font-family:var(--f-mono);font-size:32px;line-height:1.44;
  font-weight:700;letter-spacing:0;color:var(--coral);}
.r13ask .ask .quote .by{font-size:21px;letter-spacing:.16em;margin-top:16px;}

/* P22 案例 02：两个数是同一把尺子（意向转化率），所以两栏加一条等宽底座的条，
   条长比 = 数值比（3.08 : 1.5 ≈ 100% : 49%），Agent 那条走 amber。
   ⚠️ 两条比例条把这一页撑到 108%（超 106 上限），所以大数与栏距同步收一档。 */
.cmp2 .c .bar{height:14px;border-radius:3px;background:var(--hair-soft);
  border:1px solid var(--hair);margin:2px 0 0;}
.cmp2 .c .bar i{display:block;height:100%;border-radius:2px;background:rgba(255,255,255,.38);}
.cmp2 .c.am .bar i{background:var(--amber);}
.r13case .body{gap:26px;}
.r13case .cmp2{gap:48px;}
.r13case .cmp2 .c{gap:8px;}
.r13case .cmp2 .c .v{font-size:104px;}

/* P25 金句 03：换成 Bret Taylor 的英文原句 —— 英文为主（mono）、中文译一行、署名行。 */
.r13mq .mq .q{font-family:var(--f-mono);font-size:52px;font-weight:700;
  line-height:1.36;letter-spacing:0;}
.r13mq .mq .zh{font-size:34px;font-weight:700;line-height:1.5;
  color:var(--mq-2);max-width:1300px;}
.r13mq .mq .s{font-family:var(--f-mono);font-size:22px;letter-spacing:.14em;}
.r13fence .mq .s{max-width:1300px;}
"""

# ── C14 · R14 两处的页级档 ·只在 CONF_V2=1 装配 ────────────────────────────────
#    ① P2「舞台 → 讲台」是纯改字，没有版式档。
#    ② 钱流向页从「三条层带」重做成**真正的双轴时间图**，需要一整套图元档：
#       轴/网格退到 hair 三档（6% / 12% / 24%），数据线是这一页唯一响的东西；
#       量级差（178 vs 3.3）用左右两轴解决，图内另有一行小注防误读。
#    档位全部排在 C12_CSS（.r12flow 那一档）之后 —— 这一页两个类都挂，后写者胜。
C14_CSS = """
/* ============ C14 · R14 · 钱流向页重做成双轴时间图 ============ */
/* 字号：图内五级全部再定一遍（C12 的 .r12flow 档为三条层带调的，双轴图用不上）。 */
.r14money .fig .lbl{font-size:18px;letter-spacing:.14em;}
.r14money .fig .lbl.yr{font-size:24px;letter-spacing:.16em;fill:var(--ink-2);}
.r14money .fig .ttl{font-size:27px;}
.r14money .fig .txt{font-size:22px;}
.r14money .fig .txt.val{font-size:23px;font-weight:500;}
.r14money .fig .sm{font-size:20px;}
.r14money .fig .sm.wing{font-size:19px;}
.r14money .fig .sm.anno{font-size:17px;}
.r14money .fig .big{font-size:38px;}
.r14money .foot{font-size:18px;}
/* 轴与网格：安静。三档 hair token —— 网格 6% / 轴 12% / 基线 24%，一律实线一律 1px。 */
.r14money .fig .gd{stroke:var(--hair-soft);stroke-width:1;}
.r14money .fig .ax{stroke:var(--hair);stroke-width:1;}
.r14money .fig .axb{stroke:var(--hair-strong);stroke-width:1;}
/* 三条数据线：明度 + 粗细双重编码。
   ⚠️ --ink(#fff) 与 --ink-3(#D9D9E3) 直接并排是 ΔE≈11（低于 15 的正常视觉下限，
   两条灰线糊在一起），所以 Coding 那条压到 72% —— 合成 ≈#9C9CA3，
   对 --ink 与 --amber 的 ΔE 都 ≥20（dataviz validator 三项 PASS），线宽补到 3.5 保投影可读。
   明度阶梯同时就是叙事阶梯：amber 主角 > 白（最大头）> 灰（第二波，已收尾）。 */
.r14money .fig .ln{fill:none;stroke-linecap:round;stroke-linejoin:round;}
.r14money .fig .ln.fnd{stroke:var(--ink);stroke-width:6;}
.r14money .fig .ln.cod{stroke:var(--ink-3);stroke-width:3.5;opacity:.72;}
.r14money .fig .ln.cnv{stroke:var(--amber);stroke-width:7;}
/* 节点：底色描边环，压在别的线上也认得出（dataviz 的 surface ring）。 */
.r14money .fig .dot{stroke:var(--slide-bg);stroke-width:3;}
.r14money .fig .dot.fnd{fill:var(--ink);}
.r14money .fig .dot.cod{fill:var(--ink-3);opacity:.72;}
.r14money .fig .dot.cnv{fill:var(--amber);}
/* 终点名牌引线：极细，只做「这条线叫什么」的牵引，不参与读数。 */
.r14money .fig .lead{fill:none;stroke-width:1.4;opacity:.5;}
.r14money .fig .lead.fnd{stroke:var(--ink);}
.r14money .fig .lead.cnv{stroke:var(--amber);}
/* 对话式曲线下的渐变面积：低透明度的一层薄雾，只说「钱正在往这一层灌」。 */
.r14money #r14conv .g0{stop-color:var(--amber);stop-opacity:.22;}
.r14money #r14conv .g1{stop-color:var(--amber);stop-opacity:0;}
"""

# ── C15 · R15 终轮的页级档 ·只在 CONF_V2=1 装配 ───────────────────────────────
#    R15 是「改完全部内容」的收官轮，十项里六项是纯删/纯改字（无版式档），
#    需要档位的只有四处：北极星逐列对齐后的撑满、两页删段后的撑满、
#    灵魂拷问页撤掉第二拍后回到纯问句、新 Weil 金句页的英文体例。
#    全部排在 C14_CSS 之后 —— 与 C13 同名选择器（.r13ask / .r13mq 那两条）靠后写者胜。
C15_CSS = """
/* ============ C15 · R15 终轮 ============ */
/* 北极星页：note 整段删掉之后，body 只剩「阶梯图 + 四颗北极星」两块。
   图按 nstar 的四列几何重画（tread 与列等宽等位），所以这里只负责把两块撑开：
   图放大到 1.06、四栏字号上一档、栏间距跟着 grid 的 26px 走（不改 grid，改了就错位）。 */
.r15nstar .head{margin-bottom:30px;}
.r15nstar .body{gap:34px;}
.r15nstar .fig{align-items:stretch;}
.r15nstar .fig svg{width:100%;height:auto;}
.r15nstar .fig .ttl{font-size:44px;}
.r15nstar .fig .txt{font-size:23px;}
.r15nstar .fig .lbl{font-size:19px;letter-spacing:.16em;}
.r15nstar .nstar{margin-top:6px;}
.r15nstar .nstar .ns{padding-top:16px;}
.r15nstar .nstar .ns b{font-size:30px;}
.r15nstar .nstar .ns span{font-size:19px;}

/* 分水岭页：land 整段删掉之后，图与四张卡各自吃掉一半空档。 */
.r15ladder .head{margin-bottom:30px;}
.r15ladder .body{gap:34px;}
.r15ladder .fig svg{width:100%;height:auto;}
.r15ladder .g4 .card.sm .hd .n{font-size:23px;}
.r15ladder .g4 .card.sm .hd .t{font-size:29px;}
.r15ladder .g4 .card.sm .d{font-size:21px;line-height:1.62;}
.r15ladder .g4 .card.sm .tag{font-size:17px;}

/* Eval 第一课：foot 那句「给产品经理的动作」删掉之后，题面矩阵撑满，note 上一档。 */
.r15eval1 .head{margin-bottom:32px;}
.r15eval1 .body{gap:40px;}
.r15eval1 .fig svg{width:100%;height:auto;}
.r15eval1 .note{font-size:27px;line-height:1.6;}

/* 灵魂拷问页：Weil 第二拍撤回金句页，这一页回到纯问句全页大字（= R9 的 .r9p15 档）。
   C13 那三条 .r13ask 选择器已随 class 一并摘除，这里只留一条兜底，防止将来回挂。 */
.r13ask .ask .q{font-size:112px;}

/* 终检 · 全场收束页（四条一行）：R15 视觉终审逐张过图时抓到的唯一一处留白失衡 ——
   四栏 + 图标带只占 body 的 62%，上下各空一大条。这一页是全场最后的落点，
   字应该是全场最大的一档。四栏整体上调一档 + 间距放开，撑到 ~80%。 */
.r15end .body{gap:72px;}
.r15end .take{gap:30px;}
.r15end .take .c{gap:18px;}
.r15end .take .c .ord{font-size:26px;}
.r15end .take .c .who{font-size:36px;}
.r15end .take .c .say .no{font-size:25px;line-height:1.42;}
.r15end .take .c:nth-child(1) .say em{font-size:30px;}
.r15end .take .c:nth-child(2) .say em{font-size:33px;}
.r15end .take .c:nth-child(3) .say em{font-size:37px;}
.r15end .take .c:nth-child(4) .say em{font-size:41px;}
.r15end .take .c .s{font-size:24px;line-height:1.66;}

/* 金句 02 · Kevin Weil：英文原句为主（mono）+ 中文一行 + 署名行，与 .r13mq 同体例。 */
.r15mq .mq .q{font-family:var(--f-mono);font-size:54px;font-weight:700;
  line-height:1.36;letter-spacing:0;}
.r15mq .mq .zh{font-size:34px;font-weight:700;line-height:1.5;
  color:var(--mq-2);max-width:1300px;}
.r15mq .mq .s{font-family:var(--f-mono);font-size:22px;letter-spacing:.14em;}
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
        # R10 补账：纵轴拉长到 409，--len 还停在 330 —— .dw 的 dasharray 只画到 --len
        #           为止，L4 那一格旁边的轴线在 R9 里是断的
        ('style="--len:330;--i:3" d="M190 400 V70"', 'style="--len:420;--i:3" d="M190 496 V87"'),
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

# ══════════════════════════════════════════════════════════════════════════════
# ── C10（2026-08-05 · R10 · 八页删改 · 页数不变 45）─────────────────────────────
# 评审结论同 R9：解释性文字交回口播，页面只留观众要看的东西；这一轮里有三页不只是
#   删句，而是把「配角」提成主体（重构）：
#   ① P5  本场提要 · 删三问卡整组 + note，五站路线图升为全页主体（纵向 ×4.6 + 大字）
#   ② P18 Eval 第三课 · 删「正确的看法 01/02/03」，两遍质检对照条放大（纵向 ×1.5）
#   ③ P22 商业模式变迁 · 英文判断句下补中文翻译行（同 land 体系）+ 删 36 亿 foot
#   ④ P27 爬梯页 · 删 note + foot，梯子图与交叉验证条带一起放大撑满
#   ⑤ P29 它决策人审批 · 删英文引文块，三格大数与两条走法图再放大
#   ⑥ P37 QoT · 删三卡 + 两段解释，四条工程坐标升为页面主体（四列 .take.qot4）
#   ⑦ P39 对个人说 · 删 land，暴露量折线与四阶卡放大
#   ⑧ P45 终页 · 删 Kevin Weil 引文卡 + 结语，那把尺子摊开成整页，纯视觉收场
# 页码均按 45 页版；_secs 下标仍是母版 62 页的原始下标（P5→4 / P18→31 / P22→34 /
#   P27→39 / P29→42 / P37→50 / P39→52 / P45→58）。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    # ── C10-① P5 本场提要 · 三问卡整组 + note 撤走，路线图升主体 ───────────────
    _cut1(4, '\n      <div class="g3">', '↓ PART 4 · 人与组织</div></div>\n      </div>')
    _cut1(4, '\n      <div class="note flow" style="--i:11">这三个问题不是哲学问题',
             '「这事出了问题，算谁的」</b>。</div>')
    #    站点圆点 / 线宽随图一起放大（半径与 stroke-width 不在纵拉伸的作用域内）
    _r1(4, '<circle class="fill-am pop" style="--i:7" cx="80" cy="118" r="10"/>',
           '<circle class="fill-am pop" style="--i:7" cx="80" cy="118" r="19"/>')
    _r1(4, '<circle class="pop" style="--i:7" cx="460" cy="118" r="7" fill="var(--ink-3)"/>',
           '<circle class="pop" style="--i:7" cx="460" cy="118" r="14" fill="var(--ink-3)"/>')
    _r1(4, '<g class="pop" style="--i:8" fill="var(--slide-bg)" stroke="var(--amber)" stroke-width="3">\n'
           '            <circle cx="840" cy="118" r="9"/><circle cx="1220" cy="118" r="9"/>'
           '<circle cx="1600" cy="118" r="9"/>',
           '<g class="pop" style="--i:8" fill="var(--slide-bg)" stroke="var(--amber)" stroke-width="6">\n'
           '            <circle cx="840" cy="118" r="17"/><circle cx="1220" cy="118" r="17"/>'
           '<circle cx="1600" cy="118" r="17"/>')
    #    纵向 ×4.6：一条扁线长成整页的五站路线；viewBox 顺手裁掉拉伸出来的上下空白
    _ystretch(4, 4.6, ('viewBox="0 0 1680 250"', 'viewBox="0 320 1680 665"'), paths=(
        ('<path class="stroke dw" style="--len:1560;--i:6" stroke-width="1.5" d="M80 118 H1600"/>',
         '<path class="stroke dw" style="--len:1560;--i:6" stroke-width="3" d="M80 543 H1600"/>'),
        ('<path class="stroke-am dw" style="--len:800;--i:7" stroke-width="3" d="M840 118 H1600"/>',
         '<path class="stroke-am dw" style="--len:800;--i:7" stroke-width="6" d="M840 543 H1600"/>')))
    _cls(4, 'r10p5')

    # ── C10-② P18 Eval 第三课 · 裁判 · 删三条「正确的看法」──────────────────────
    _cut1(31, '\n      <div class="tri">', '裁判必须重新验一遍。</div></div>\n      </div>')
    _ystretch(31, 1.5, ('viewBox="0 0 1680 330"', 'viewBox="0 0 1680 495"'), paths=(
        ('stroke-width="40" stroke-linecap="round" d="M44 96 H1400"',
         'stroke-width="58" stroke-linecap="round" d="M44 144 H1400"'),
        ('stroke-width="40" stroke-linecap="round" d="M44 252 H1264"',
         'stroke-width="58" stroke-linecap="round" d="M44 378 H1264"'),
        ('stroke-width="40" stroke-linecap="round" d="M1286 252 H1400"',
         'stroke-width="58" stroke-linecap="round" d="M1286 378 H1400"'),
        ('style="font-size:60px">100%', 'style="font-size:86px">100%'),
        ('style="font-size:60px">≥10%', 'style="font-size:86px">≥10%')))
    _cls(31, 'r10p18')

    # ── C10-③ P22 商业模式变迁 · 英文判断句补中文翻译行 + 删 36 亿 foot ──────────
    #    英文原句保留原样，中文走 land 体系的 .s（次一级字号），不另起一块
    _r1(34, 'you pay for <b>business outcomes delivered</b>.</div>',
            'you pay for <b>business outcomes delivered</b>.'
            '<span class="s">你付的不是 token 的钱——是被交付出来的业务结果的钱。</span></div>')
    _cut1(34, '\n      <div class="foot flow rev" style="--i:10">同一赛道的参照',
              '付了一个软件公司拿不到的价</div>')
    _cls(34, 'r10p22')

    # ── C10-④ P27 爬梯页 · 删 note + foot，梯子图（含交叉验证条带）放大撑满 ────────
    _cut1(39, '\n      <div class="note flow" data-step="3" style="--i:6">一个只能升级',
              '收权难——收权才是工程。</b></div>')
    _cut1(39, '\n      <div class="foot flow rev" data-step="4">给产品团队的动作',
              '就是你现在真实的位置</div>')
    #    梯子纵向 ×1.13（_ystretch 只作用于第一张 svg，底部交叉验证条带原样保留）
    _ystretch(39, 1.13, ('viewBox="0 0 1680 460"', 'viewBox="0 0 1680 520"'), paths=(
        ('d="M40 400 H340"', 'd="M40 452 H340"'),
        ('style="--len:368;--i:4" stroke-width="2" d="M340 400 V332 H640"',
         'style="--len:380;--i:4" stroke-width="2" d="M340 452 V375 H640"'),
        ('d="M675 40 V450"', 'd="M675 45 V509"'),
        ('style="--len:100;--i:1" stroke-width="3" d="M640 332 L710 264"',
         'style="--len:106;--i:1" stroke-width="3" d="M640 375 L710 298"'),
        ('d="M710 264 H1010"', 'd="M710 298 H1010"'),
        ('style="--len:368;--i:2" stroke-width="2" d="M1010 264 V196 H1310"',
         'style="--len:380;--i:2" stroke-width="2" d="M1010 298 V221 H1310"'),
        ('style="--len:398;--i:4" stroke-width="3" d="M1310 196 V128 H1640"',
         'style="--len:410;--i:4" stroke-width="3" d="M1310 221 V145 H1640"'),
        ('d="M1600 150 V424"', 'd="M1600 170 V481"'),
        # 向下电梯的箭头保持原大小，只整体下移到新的线尾
        ('d="M1591 424 L1600 442 L1609 424 Z"', 'd="M1591 481 L1600 499 L1609 481 Z"')))
    #    交叉验证条带里「第三把尺子」那行原本贴着上一行（母版 26 单位）；本页字号加大后
    #    只剩 7px，往下让 12 个单位把行距还回去（viewBox 同步加高）
    _r1(39, '<text class="lbl fill-am pop" style="--i:5" x="1580" y="176"',
            '<text class="lbl fill-am pop" style="--i:5" x="1580" y="188"')
    _r1(39, '<svg width="1680" viewBox="0 0 1680 178" fill="none">',
            '<svg width="1680" viewBox="0 0 1680 192" fill="none">')
    _cls(39, 'r10p27')

    # ── C10-⑤ P29 它决策，人审批 · 删英文引文块 ────────────────────────────────
    _cut1(42, '\n      <div class="quote flow" style="--i:8">',
              '<div class="by">某企业支付平台 CEO 与访谈者 · 2026</div>\n      </div>')
    #    引文块腾出的 200px 全给两条走法：纵向 ×1.9，节点圆点与线宽同步加粗
    for _o, _n in (('<circle cx="300" cy="64" r="7"/><circle cx="720" cy="64" r="7"/>'
                    '<circle cx="1140" cy="64" r="7"/>',
                    '<circle cx="300" cy="64" r="12"/><circle cx="720" cy="64" r="12"/>'
                    '<circle cx="1140" cy="64" r="12"/>'),
                   ('<circle cx="300" cy="186" r="7"/><circle cx="1140" cy="186" r="7"/>',
                    '<circle cx="300" cy="186" r="12"/><circle cx="1140" cy="186" r="12"/>'),
                   ('cx="720" cy="186" r="13" fill="var(--slide-bg)" stroke="var(--amber)" stroke-width="3.4"',
                    'cx="720" cy="186" r="20" fill="var(--slide-bg)" stroke="var(--amber)" stroke-width="4.6"')):
        _r1(42, _o, _n)
    assert _secs[42].count('text-anchor="middle" style="font-size:24px"') == 6
    _secs[42] = _secs[42].replace('text-anchor="middle" style="font-size:24px"',
                                  'text-anchor="middle" style="font-size:32px"')
    #    ✗ / ✓ 两个记号不跟着纵向拉伸变形，只整体平移到新的线心（64→122 / 186→353）
    _ystretch(42, 1.9, ('viewBox="0 0 1680 250"', 'viewBox="0 24 1680 412"'), paths=(
        ('stroke-width="2.8" d="M76 50 L104 78 M104 50 L76 78"',
         'stroke-width="4" d="M76 108 L104 136 M104 108 L76 136"'),
        ('stroke-width="2.8" d="M76 186 L88 198 L106 172"',
         'stroke-width="4" d="M76 353 L88 365 L106 339"'),
        ('stroke-width="2" d="M180 64 H1240"', 'stroke-width="3" d="M180 122 H1240"'),
        ('stroke-width="3" d="M180 186 H1240"', 'stroke-width="4.5" d="M180 353 H1240"'),
        ('--pd:1.4s" d="M180 186 H1240"', '--pd:1.4s" d="M180 353 H1240"')))
    _cls(42, 'r10p29')

    # ── C10-⑥ P37 QoT · 三卡 + 两段解释 → 四条工程坐标接管页面 ───────────────────
    #    QoS-QoE-QoI-QoT 顶部条保留；下半页换成四列（.take 体系，大字为主）。
    _QOT4 = '''
      <div class="take qot4" data-step="4">
        <div class="c rise" style="--i:0"><div class="ord">01</div><div class="who">身份可验</div><div class="lat">VERIFIABLE</div><div class="s">「它是谁、代表谁」</div></div>
        <div class="c rise" style="--i:1"><div class="ord">02</div><div class="who">行为可拦</div><div class="lat">INTERCEPTABLE</div><div class="s">「越界那句话，必须在说完之前被拦下」</div></div>
        <div class="c rise" style="--i:2"><div class="ord">03</div><div class="who">结果可追</div><div class="lat">ACCOUNTABLE</div><div class="s">「每一轮留痕、可归因」</div></div>
        <div class="c rise" style="--i:3"><div class="ord">04</div><div class="who">授权可撤销</div><div class="lat">REVOCABLE</div><div class="s">「随时降级、随时回滚」</div></div>
      </div>'''
    _cut1(50, '\n      <div class="g3" data-step="4">', '随时降级、随时回滚）。</span></div>', _QOT4)
    #    顶部四格条纵向 ×1.35（格子本身要跟着长高，height 不在 y 正则的作用域里）
    for _o, _n in (('style="font-size:32px">QoS', 'style="font-size:42px">QoS'),
                   ('style="font-size:32px">QoE', 'style="font-size:42px">QoE'),
                   ('style="font-size:32px">QoI', 'style="font-size:42px">QoI'),
                   ('style="font-size:32px">QoT', 'style="font-size:42px">QoT')):
        _r1(50, _o, _n)
    _ystretch(50, 1.35, ('viewBox="0 0 1680 250"', 'viewBox="0 0 1680 338"'), paths=(
        ('width="380" height="120"', 'width="380" height="162"'),
        ('d="M388 100 H418"', 'd="M388 135 H418"'),
        ('d="M821 100 H851"', 'd="M821 135 H851"'),
        ('d="M1254 100 H1284"', 'd="M1254 135 H1284"'),
        ('d="M1489 174 V210 H0 V186"', 'd="M1489 235 V284 H0 V251"')))
    _cls(50, 'r10p37')

    # ── C10-⑦ P39 对个人说 · 删 land ──────────────────────────────────────────
    _cut1(52, '\n      <div class="land flow" style="--i:12">四阶不是学历',
              '你敢把重活交给它的前提。</span></div>')
    #    四阶折线纵向 ×1.4：台阶落差拉开，最难跨的那一段才看得出「难」
    for _o, _n in (('style="font-size:28px">看过', 'style="font-size:34px">看过'),
                   ('style="font-size:28px">用过', 'style="font-size:34px">用过'),
                   ('style="font-size:28px">学过', 'style="font-size:34px">学过'),
                   ('style="font-size:28px">干过', 'style="font-size:34px">干过')):
        _r1(52, _o, _n)
    _ystretch(52, 1.4, ('viewBox="0 0 1680 300"', 'viewBox="0 -14 1680 452"'), paths=(
        ('style="--len:260;--i:2" stroke-width="1.5" d="M90 280 V30"',
         'style="--len:360;--i:2" stroke-width="1.5" d="M90 392 V42"'),
        ('d="M90 24 l-7 12 l14 0 z"', 'd="M90 38 l-7 12 l14 0 z"'),   # 箭头保持原大小
        ('d="M140 264 H1580"', 'd="M140 370 H1580"'),
        ('d="M140 236 H440 L510 178 H810 L880 120 H1180 L1250 58 H1580"',
         'd="M140 330 H440 L510 249 H810 L880 168 H1180 L1250 81 H1580"'),
        ('d="M810 178 L880 120"', 'd="M810 249 L880 168"')))
    _cls(52, 'r10p39')

    # ── C10-⑧ P45 终页 · 删 Kevin Weil 引文卡 + 结语，纯图收场 ────────────────────
    _cut1(58, '\n      <div class="quote flow" style="--i:10">',
              '也不忘<b>理解自己</b>。</div>')
    #    图内 ttl 是 inline font-size（压过 class），先就地加大，再整体纵向 ×1.7
    for _o, _n in (('style="font-size:26px">同一把尺子', 'style="font-size:46px">同一把尺子'),
                   ('style="font-size:28px">向外 · Eval', 'style="font-size:48px">向外 · Eval'),
                   ('style="font-size:28px">向内 · 内观', 'style="font-size:48px">向内 · 内观')):
        _r1(58, _o, _n)
    _ystretch(58, 1.7, ('viewBox="0 -104 1680 380"', 'viewBox="0 -177 1680 646"'), paths=(
        ('d="M0 -44 H1680"', 'd="M0 -75 H1680"'),
        ('style="--len:20;--i:8" stroke-width="2.2" d="M190 -52 V-36M560 -52 V-36M930 -52 V-36M1300 -52 V-36"',
         'style="--len:34;--i:8" stroke-width="2.6" d="M190 -88 V-61M560 -88 V-61M930 -88 V-61M1300 -88 V-61"'),
        ('width="80" height="176"', 'width="80" height="299"'),
        ('d="M800 82 H832 M800 116 H822 M800 150 H832 M800 184 H822"',
         'd="M800 139 H832 M800 197 H822 M800 255 H832 M800 313 H822"'),
        ('d="M900 134 H1300"', 'd="M900 228 H1300"'),
        ('d="M1300 125 L1318 134 L1300 143 Z"', 'd="M1300 213 L1318 228 L1300 243 Z"'),
        ('d="M780 134 H380"', 'd="M780 228 H380"'),
        ('d="M380 125 L362 134 L380 143 Z"', 'd="M380 213 L362 228 L380 243 Z"')))
    _cls(58, 'r10p45')

# ══════════════════════════════════════════════════════════════════════════════
# ── C11（2026-08-05 · R11 · 十三页删改与数据换血 · 页数不变 45）─────────────────
# 沿用 C9/C10 的四把工具（_r1 / _cut1 / _cls / _ystretch）。这一轮里除了「删句 + 撑满」，
# 还有三类新动作：**数据换血**（P8 企业侧导向）、**结论重写**（P9）、**版面对调**（P29/P30）。
#   ① P3  录音页 · 删两块口播讲的结论文字，波形纵向 ×2 接管上半页
#   ② P4  一个人都没有 · OPENAPI → A2A；PSTN「跑了 100 年」→「150 年」（贝尔 1876 → 今年）
#   ③ P5  本场提要 · 路线图删「PART 0 开场」站，四站重排（站距 / 高亮段起点同步）
#   ④ P8  渗透页 · 数据换血：消费侧五取一，企业侧补两条 2026 一手采购硬数，SOURCE 逐条标源
#   ⑤ P9  四个互不相干的人 · 结论行重写为「企业服务侧已到规模化应用阶段·硬性基础全部具备」
#   ⑥ P10 四阶段四北极星 · 删「边界声明」foot
#   ⑦ P19 Eval 第四课 · STEP 01-04 四块文字并进图内成节点标注，下方四块删除，图升主体
#   ⑧ P21 案例 02 · 页面核心换成 3.08% 被识破率 × 1.5% 人工基线的双大数对比，删三格 + note
#   ⑨ P22 商业模式变迁 · 中文行升主，英文降为原文补充 + 出处行（Sierra 官方博客已核到）
#   ⑩ P29 它决策人审批 · 版面对调：两条走法图上，三个大数下并缩小
#   ⑪ P30 案例 03 沙箱逃逸 · 版面对调：图最上并放大，事件叙述缩小沉到最底部作注释行
#   ⑫ P33 体验的围栏 · 删 backchannel 抱怨那条 note
#   ⑬ P36 五条准入线全景 · 下方文字只留「四条产品线…四个切片」一句，图放大
# 页码按 45 页版；_secs 下标是母版 62 页原始下标（P3→2 / P4→3 / P5→4 / P8→7 / P9→8 /
#   P10→9 / P19→30 / P21→33 / P22→34 / P29→42 / P30→43 / P33→46 / P36→49）。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    def _rn(i, old, new, n):
        """定量替换：_secs[i] 里 old 必须出现 n 次，全部换成 new（_r1 的复数版）。"""
        assert _secs[i].count(old) == n, f'_secs[{i}] 定量替换失败（应 {n} 次）：{old[:48]}'
        _secs[i] = _secs[i].replace(old, new)

    # ── C11-① P3 一年后我又听了那段录音 · 删两块口播结论，波形纵向 ×2 ────────────
    _cut1(2, '\n          <div class="s">当时我的结论是', '把它做得更像人</b>。</div>')
    _cut1(2, '\n          <div class="s">他真正的愤怒不是', '能替谁审批</b>。</div>')
    #    波形是这一页唯一的视觉，删完两段之后纵向 ×2 接管上半页。
    #    两条正弦与走带光点共用同一条 d（三处），一次替换全中；--len:2200 原本就盖得住
    #    拉伸后的实长（1715 → 1813），不用补账。
    _ystretch(2, 2.0, ('viewBox="0 0 1680 196"', 'viewBox="0 0 1680 392"'), paths=(
        ('d="M0 74 C 120 32, 240 116, 360 74 S 600 32, 720 74 S 960 116, 1080 74 '
         'S 1320 32, 1440 74 S 1620 110, 1680 74"',
         'd="M0 148 C 120 64, 240 232, 360 148 S 600 64, 720 148 S 960 232, 1080 148 '
         'S 1320 64, 1440 148 S 1620 220, 1680 148"'),
        ('d="M0 74 C 120 110, 240 38, 360 74 S 600 114, 720 74 S 960 36, 1080 74 '
         'S 1320 112, 1440 74 S 1620 40, 1680 74"',
         'd="M0 148 C 120 220, 240 76, 360 148 S 600 228, 720 148 S 960 72, 1080 148 '
         'S 1320 224, 1440 148 S 1620 80, 1680 148"'),
        ('width="286" height="120"', 'width="286" height="240"'),
        ('d="M1004 14 V134 M1290 14 V134"', 'd="M1004 28 V268 M1290 28 V268"')))
    _cls(2, 'r11p3')

    # ── C11-② P4 今年这段通话里一个人都没有 · A2A + PSTN 150 年 ──────────────────
    #    ⓐ 四个「本来以为会用上」的协议里，OPENAPI 换成 A2A（今年真正在谈的那条 agent 互操作协议）
    _r1(3, '<text class="lbl" x="560" y="-66" text-anchor="middle">OPENAPI</text>',
           '<text class="lbl" x="560" y="-66" text-anchor="middle">A2A</text>')
    #    ⓑ 贝尔 1876 年打出人类第一通电话 —— 到今年（2026）整 150 周年，图上与说明行一起改
    _r1(3, '>PSTN · 一张跑了 100 年的电话网<', '>PSTN · 一张跑了 150 年的电话网<')
    _r1(3, '是语音，加一张一百年的旧网。',
           '是语音，加一张<b>一百五十年</b>的旧网'
           '（贝尔 1876 年打出人类第一通电话，今年整 150 周年）。')

    # ── C11-③ P5 本场提要 · 路线图删「PART 0 · 开场」站，四站重排 ─────────────────
    #    站位 80/460/840/1220/1600（等距 380 · 五站）→ 140/627/1113/1600（等距 ≈487 · 四站）；
    #    高亮段起点从 PART 2 的旧 x=840 同步挪到新 x=627，--len 800 → 1010（1600-627=973）。
    _cut1(4, '<!-- 全场路线', '</svg>', '''<!-- 全场路线：四站一条线。第一站讲「变了什么」，后三站分别回答托付时代的三个问题。 -->
        <svg viewBox="0 320 1680 665" width="1680" fill="none">
          <path class="stroke dw" style="--len:1500;--i:6" stroke-width="3" d="M140 543 H1600"/>
          <path class="stroke-am dw" style="--len:1010;--i:7" stroke-width="6" d="M627 543 H1600"/>

          <circle class="fill-am pop" style="--i:7" cx="140" cy="543" r="19"/>
          <g class="pop" style="--i:8" fill="var(--slide-bg)" stroke="var(--amber)" stroke-width="6">
            <circle cx="627" cy="543" r="17"/><circle cx="1113" cy="543" r="17"/><circle cx="1600" cy="543" r="17"/>
          </g>

          <text class="lbl fill-am pop" style="--i:7" x="140" y="368" text-anchor="middle">PART 1</text>
          <text class="lbl fill-am pop" style="--i:8" x="627" y="368" text-anchor="middle">PART 2</text>
          <text class="lbl fill-am pop" style="--i:8" x="1113" y="368" text-anchor="middle">PART 3</text>
          <text class="lbl fill-am pop" style="--i:8" x="1600" y="368" text-anchor="middle">PART 4</text>

          <text class="txt pop" style="--i:9" x="140" y="773" text-anchor="middle">语法变了</text>
          <text class="txt pop" style="--i:9" x="627" y="773" text-anchor="middle">被托付</text>
          <text class="txt pop" style="--i:9" x="1113" y="773" text-anchor="middle">双向奔赴</text>
          <text class="txt pop" style="--i:9" x="1600" y="773" text-anchor="middle">人与组织</text>

          <text class="sm pop" style="--i:10" x="140" y="948" text-anchor="middle">从调用到双向奔赴</text>
          <text class="sm fill-am pop" style="--i:10" x="627" y="948" text-anchor="middle">尺子、授权与边界</text>
          <text class="sm fill-am pop" style="--i:10" x="1113" y="948" text-anchor="middle">出事了算谁的</text>
          <text class="sm fill-am pop" style="--i:10" x="1600" y="948" text-anchor="middle">你和团队怎么变</text>
        </svg>''')
    _cls(4, 'r11p5')

    # ── C11-④ P8 预测还在打架，采购已经开动 · 数据换血（企业侧导向）─────────────
    #    消费侧五条压成一条（49% 那条最有力：两年 33% → 49%，需求端的底盘）；
    #    企业侧补两条 2026 年一手采购硬数（Salesforce《State of Service: AI Agents Edition》，
    #    n=3,075，2026-03-09~04-04 实地）；91% 与 15–20% 原样保留。SOURCE 逐条标源与年份。
    #    bar 换算沿用母版比例尺 14.4px/%（91%→1310 / 20%→288 / 49%→706）。
    _cut1(7, '<svg viewBox="0 0 1680 492"', '</svg>', '''<svg viewBox="0 0 1680 496" width="1680" aria-hidden="true">
          <!-- ── 企业侧：四个数，全部是已经发生的采购与部署 ───────────── -->
          <text class="lbl fill-am pop" style="--i:2" x="0" y="12">企业侧 · 这四个数都已经发生</text>

          <text class="txt pop" style="--i:3" x="0" y="54">全球企业客服组织里，已经在用 AI 智能体的（一年前还是 39%）</text>
          <path class="stroke" stroke-width="14" stroke-linecap="round" d="M0 88 H1440" opacity=".22"/>
          <path class="stroke-am dw" style="--len:950;--i:3" stroke-width="14" stroke-linecap="round" d="M0 88 H950"/>
          <text class="big pop" style="--i:4" x="1680" y="103" text-anchor="end">66%</text>

          <text class="txt pop" style="--i:4" x="0" y="136">中国银行业里，已经部署智能客服的比例</text>
          <path class="stroke" stroke-width="14" stroke-linecap="round" d="M0 170 H1440" opacity=".22"/>
          <path class="stroke-am dw" style="--len:1310;--i:4" stroke-width="14" stroke-linecap="round" d="M0 170 H1310"/>
          <text class="big pop" style="--i:5" x="1680" y="185" text-anchor="end">91%</text>

          <text class="txt pop" style="--i:5" x="0" y="218">已经上线的组织里，60 天内就看到可量化收益的</text>
          <path class="stroke" stroke-width="14" stroke-linecap="round" d="M0 252 H1440" opacity=".22"/>
          <path class="stroke-am dw" style="--len:1010;--i:5" stroke-width="14" stroke-linecap="round" d="M0 252 H1008"/>
          <text class="big pop" style="--i:6" x="1680" y="267" text-anchor="end">70%</text>

          <text class="txt pop" style="--i:6" x="0" y="300">AI 语音坐席的综合成本，只有人工坐席的</text>
          <path class="stroke" stroke-width="14" stroke-linecap="round" d="M0 334 H1440" opacity=".22"/>
          <path class="stroke-am dw" style="--len:288;--i:6" stroke-width="14" stroke-linecap="round" d="M0 334 H288"/>
          <text class="big pop" style="--i:7" x="1680" y="349" text-anchor="end">15–20%</text>

          <!-- ── 消费侧：只留一条，需求那一端早就到位 ───────────────────── -->
          <text class="lbl fill-co pop" style="--i:7" x="0" y="392">消费侧 · 只留一条对照</text>

          <text class="txt pop" style="--i:8" x="0" y="434">美国成年人里，用过 AI 聊天机器人的（两年前还是 33%）</text>
          <path class="stroke" stroke-width="14" stroke-linecap="round" d="M0 468 H1440" opacity=".22"/>
          <path class="stroke-co dw" style="--len:710;--i:8" stroke-width="14" stroke-linecap="round" d="M0 468 H706"/>
          <text class="big fill-co pop" style="--i:9" x="1680" y="483" text-anchor="end">49%</text>
        </svg>''')
    _r1(7, '<div class="foot flow rev" style="--i:11">SOURCE · 国内：CC-CMM · 艾媒咨询 · 第一新声 2025 · '
           '消费侧：Pew Research 2026.06（n=5,119）· Common Sense Media 2025.07（n=1,060）· '
           'Similarweb 2026 年中 · 预测对照：Gartner 2025–2026</div>',
           '<div class="foot flow rev" style="--i:11">SOURCE · 66% 与 70%：Salesforce《State of Service: '
           'AI Agents Edition》2026-05（n=3,075 · 2026 年 3–4 月实地）· 91% 与 15–20%：CC-CMM · 艾媒咨询 · '
           '第一新声 2025 · 49%：Pew Research 2026-06（n=5,119）· 预测对照：Gartner 2025–2026</div>')
    _cls(7, 'r11p8')

    # ── C11-⑤ P9 四个互不相干的人 · 结论行重写 ──────────────────────────────────
    #    四条引言不动，只把结论行的口径抬高一级：不再停在「模型不再是瓶颈」，
    #    直接落到「企业服务侧已经到了规模化应用的阶段——硬性基础全部具备」。
    _r1(8, '<div class="note"><span class="flow" style="--i:12">四个方向的人得出了同一个结论：'
           '<b>模型不再是瓶颈</b>。瓶颈换成了产品——权限怎么给、结果怎么算、出错怎么收。</span></div>',
           '<div class="note"><span class="flow" style="--i:12">四个方向的人，指向同一个判断：'
           '<b class="am">对话式智能体在企业服务侧，已经到了规模化应用的阶段</b>——'
           '智能够用、部署可做、扩散周期已经开始、周边那圈软件也补齐了，'
           '<b>硬性基础全部具备</b>。</span></div>')
    _cls(8, 'r11p9')

    # ── C11-⑥ P10 四个阶段四颗北极星 · 删「边界声明」foot ────────────────────────
    _cut1(9, '\n      <div class="foot flow rev" data-step="4" style="--i:0">边界声明',
             '结果记在哪里 · 出错由谁负责</div>')
    #    腾出的一行还给四级折线：纵向 ×1.08（阶梯落差拉开一点，字号同步小步加大）
    _ystretch(9, 1.08, ('viewBox="0 0 1680 480"', 'viewBox="0 0 1680 520"'), paths=(
        ('style="font-size:34px"', 'style="font-size:40px"'),
        ('d="M20 410 H420"', 'd="M20 443 H420"'),
        ('style="--len:480;--i:0" stroke-width="2" d="M420 410 V330 H820"',
         'style="--len:500;--i:0" stroke-width="2" d="M420 443 V356 H820"'),
        ('style="--len:480;--i:0" stroke-width="2" d="M820 330 V250 H1220"',
         'style="--len:500;--i:0" stroke-width="2" d="M820 356 V270 H1220"'),
        ('d="M1200 40 V450"', 'd="M1200 43 V486"'),
        ('style="--len:520;--i:1" stroke-width="3" d="M1220 250 V170 H1660"',
         'style="--len:540;--i:1" stroke-width="3" d="M1220 270 V184 H1660"')))
    _cls(9, 'r11p10')

    # ── C11-⑦ P19 Eval 第四课 · STEP 01-04 并进图内，下方四块删除 ────────────────
    #    四步本来就是图上四个节点的做法说明，分成两处看是重复；并进去之后图升为整页主体。
    _STEPS_IN = '''<text class="lbl fill-am pop" style="--i:5" x="1520" y="205" text-anchor="middle">每次发版必跑</text>

          <!-- 四步做法：本来在图下方另起四块，R11 并成图上四个节点各自的标注 -->
          <text class="lbl fill-am pop" style="--i:6" x="180" y="256" text-anchor="middle">STEP 01</text>
          <g class="pop" style="--i:6"><text class="ttl" x="180" y="298" text-anchor="middle" style="font-size:31px">全量捞，不抽样</text></g>
          <text class="sm pop" style="--i:7" x="180" y="330" text-anchor="middle">抽样会先把长尾抽没，</text>
          <text class="sm pop" style="--i:7" x="180" y="356" text-anchor="middle">而长尾正是它翻车的地方</text>

          <text class="lbl fill-am pop" style="--i:6" x="660" y="256" text-anchor="middle">STEP 02</text>
          <g class="pop" style="--i:6"><text class="ttl" x="660" y="298" text-anchor="middle" style="font-size:31px">人耳听，不看文本</text></g>
          <text class="sm pop" style="--i:7" x="660" y="330" text-anchor="middle">停顿、抢话、气口，</text>
          <text class="sm pop" style="--i:7" x="660" y="356" text-anchor="middle">转成文字之后全没了</text>

          <text class="lbl fill-am pop" style="--i:7" x="1120" y="256" text-anchor="middle">STEP 03</text>
          <g class="pop" style="--i:7"><text class="ttl" x="1120" y="298" text-anchor="middle" style="font-size:31px">归类，不打分</text></g>
          <text class="sm pop" style="--i:8" x="1120" y="330" text-anchor="middle">先说清「错在哪一类」，</text>
          <text class="sm pop" style="--i:8" x="1120" y="356" text-anchor="middle">再谈错得多严重</text>

          <text class="lbl fill-am pop" style="--i:7" x="1520" y="256" text-anchor="middle">STEP 04</text>
          <g class="pop" style="--i:7"><text class="ttl fill-am" x="1520" y="298" text-anchor="middle" style="font-size:31px">固化成回归集</text></g>
          <text class="sm pop" style="--i:8" x="1520" y="330" text-anchor="middle">每一条失败都变成一道题，</text>
          <text class="sm pop" style="--i:8" x="1520" y="356" text-anchor="middle">从此不许再错第二遍</text>'''
    _r1(30, '<text class="lbl fill-am pop" style="--i:5" x="1520" y="205" text-anchor="middle">每次发版必跑</text>',
            _STEPS_IN)
    #    图下半（九类信号带）整体下移 156，给四步标注让位
    _r1(30, '<path class="stroke dw" style="--len:1700;--i:6" stroke-width="1" opacity=".45" d="M0 250 H1680"/>',
            '<path class="stroke dw" style="--len:1700;--i:9" stroke-width="1" opacity=".45" d="M0 406 H1680"/>')
    _r1(30, '<text class="lbl pop" style="--i:6" x="0" y="282">那九类，就是这九类 —— 每一类都能单独出题、单独回归</text>',
            '<text class="lbl pop" style="--i:9" x="0" y="438">那九类，就是这九类 —— 每一类都能单独出题、单独回归</text>')
    _r1(30, '<path class="stroke dw" style="--len:1520;--i:6" stroke-width="1.2" opacity=".5" d="M88 302 H1592"/>',
            '<path class="stroke dw" style="--len:1520;--i:9" stroke-width="1.2" opacity=".5" d="M88 458 H1592"/>')
    _rn(30, 'cy="302" r="5"', 'cy="458" r="5"', 9)
    _rn(30, 'y="334" text-anchor="middle"', 'y="490" text-anchor="middle"', 9)
    _rn(30, 'y="358" text-anchor="middle"', 'y="514" text-anchor="middle"', 9)
    _r1(30, '<svg viewBox="0 0 1680 364" width="1680" aria-hidden="true">',
            '<svg viewBox="0 0 1680 522" width="1680" aria-hidden="true">')
    _cut1(30, '\n      <div class="steps">', '不许再错第二遍。</div></div>\n      </div>')
    #    下方四块腾出的一整条还给图：整张纵向 ×1.15（522 → 600），节点标题同步加大
    _ystretch(30, 1.15, ('viewBox="0 0 1680 522"', 'viewBox="0 0 1680 600"'), paths=(
        ('style="font-size:28px"', 'style="font-size:32px"'),
        ('d="M80 125 H1600"', 'd="M80 144 H1600"'),
        ('d="M0 406 H1680"', 'd="M0 467 H1680"'),
        ('d="M88 458 H1592"', 'd="M88 527 H1592"')))
    _cls(30, 'r11p19')

    # ── C11-⑧ P21 案例 02 · 3.08% × 1.5% 双大数对比接管页面 ──────────────────────
    #    Colin 口径：被识破率 3.08%（现文 96.5% 反推出的 3.5% 一律以 3.08% 为准），
    #    对照人工坐席自己被投诉「不像人」的 1.5% 基线 —— 含义是「已经逼近人工极限」。
    _cut1(33, '\n      <div class="g4">', '就是案例 01 那个数字的现场。</span></div>', '''
      <div class="cmp2">
        <div class="c am rise" style="--i:8">
          <div class="k">AI 坐席 · 本案例全量标注</div>
          <div class="v">3.08%</div>
          <div class="l">被识破率</div>
          <div class="u">通话结束前，被对方听出「这是 AI」的比例</div>
        </div>
        <div class="vs pop" style="--i:9">VS</div>
        <div class="c rise" style="--i:10">
          <div class="k">人工坐席 · 上线前人工基线 · 内部口径</div>
          <div class="v">1.5%</div>
          <div class="l">被投诉「不像人」基线</div>
          <div class="u">真人坐席被客户抱怨「像机器人」的比例</div>
        </div>
      </div>
      <div class="land flow" style="--i:11">两个数之间只剩 <b>1.58 个百分点</b>——<b class="am">它已经贴到人工坐席自己的极限上了。</b></div>''')
    _cls(33, 'r11p21')

    # ── C11-⑨ P22 商业模式变迁 · 中文升主 / 英文降为原文补充 + 出处行 ─────────────
    #    出处已核到一手：Sierra 官方博客《The next Horizon in agents》（Bret Taylor & Clay Bavor,
    #    2026-07-16）原文 "And with Horizon, you don't pay for tokens, you pay for business
    #    outcomes delivered." —— 不是转述，是原话。
    _r1(34, '<div class="land r9en flow" style="--i:9">You don’t pay for tokens, you pay for '
            '<b>business outcomes delivered</b>.<span class="s">你付的不是 token 的钱——'
            '是被交付出来的业务结果的钱。</span></div>',
            '<div class="land r11pay flow" style="--i:9">你付的不是 token 的钱——是被交付出来的业务结果的钱。'
            '<span class="en">“You don’t pay for tokens, you pay for '
            '<b>business outcomes delivered</b>.”</span>'
            '<span class="src">Bret Taylor &amp; Clay Bavor · Sierra 官方博客《The next Horizon in agents》· 2026-07</span></div>')

    # ── C11-⑩ P29 它决策，人审批 · 版面对调（图上 / 三个大数下并缩小）────────────
    _a29 = _secs[42].index('\n      <div class="g3">')
    _b29 = _secs[42].index('\n      <div class="fig">')
    _c29 = _secs[42].index('</svg>\n      </div>', _b29) + len('</svg>\n      </div>')
    _secs[42] = _secs[42][:_a29] + _secs[42][_b29:_c29] + _secs[42][_a29:_b29] + _secs[42][_c29:]
    assert _secs[42].index('<div class="fig">') < _secs[42].index('<div class="g3">'), 'C11 · P29 对调失败'
    _cls(42, 'r11p29')

    # ── C11-⑪ P30 案例 03 · 版面对调（图最上并放大 / 事件叙述缩小沉底作注释行）────
    _a30 = _secs[43].index('\n      <div class="old rise"')
    _b30 = _secs[43].index('\n      <div class="fig">')
    _old30 = _secs[43][_a30:_b30].replace('class="old rise"', 'class="old tail rise"')
    _secs[43] = _secs[43][:_a30] + _secs[43][_b30:]
    _e30 = _secs[43].rindex('\n    </div>\n  </div>\n</section>')
    _secs[43] = _secs[43][:_e30] + _old30 + _secs[43][_e30:]
    assert _secs[43].index('<div class="fig">') < _secs[43].index('<div class="g3">') \
        < _secs[43].index('class="note co') < _secs[43].index('class="old tail'), 'C11 · P30 对调失败'
    #    链路图升为页面第一视觉：纵向 ×1.55（168 → 260），节点标题 23 → 30px
    _ystretch(43, 1.55, ('viewBox="0 0 1680 168"', 'viewBox="0 0 1680 260"'), paths=(
        ('style="font-size:23px"', 'style="font-size:30px"'),
        ('d="M100 82 H1560"', 'd="M100 127 H1560"'),
        ('d="M300 14 V150"', 'd="M300 22 V233"')))
    _cls(43, 'r11p30')

    # ── C11-⑫ P33 体验的围栏 · 删 backchannel 抱怨那条 note ──────────────────────
    _cut1(46, '\n      <div class="note flow" style="--i:10">客户现场最大的抱怨',
              '叫 backchannel。</b></div>')
    _cls(46, 'r11p33')

    # ── C11-⑬ P36 五条准入线全景 · 下方只留一句，图放大 ─────────────────────────
    _cut1(49, '</b>任何一格的进步，四条线一起受益', '固化在这张图的某一格里。</div>', '</b></div>')
    _ystretch(49, 1.18, ('viewBox="0 0 1640 500"', 'viewBox="0 0 1640 590"'), paths=(
        ('height="500"', 'height="590"'),
        ('font-size:26px', 'font-size:31px'),
        ('d="M200 62 H1460"', 'd="M200 73 H1460"'),
        ('style="--len:400;--i:3" d="M200 62 V450"', 'style="--len:480;--i:3" d="M200 73 V531"')))
    _cls(49, 'r11p36')

# ══════════════════════════════════════════════════════════════════════════════
# ── C12（2026-08-05 · R12 · PART 1 幕卡后新增一页 · 45 → 46 页）─────────────────
# 前十一层都在「删 / 改 / 重排」，这一层第一次**加页**。母版 62 页仍然只读：
#   新页作为第 63 个元素 append 进 _secs，再把它的下标插进 _order 的第 6 位
#   （幕卡 _secs[5] 之后、钱页 _secs[6] 之前），页码由现成的 _renum 统一重排。
#
# 为什么加这一页：PART 1 现在的数据开场是「钱（P7）→ 采购（P8）」，一上来就已经在
#   对话式 AI 内部了，缺一张「先看全图」。R12 补上这张全图，三连变成——
#     新 P7  近三年 AI 的钱先后涌进哪里（本页 · 全图）
#     现 P8  对话式 AI 内部的钱分布在哪（ElevenLabs / OpenAI / Sierra 那页）
#     现 P9  采购已经开始发生
#   主张：2024 起最大头一直是基础模型，第二波是 Coding，现在钱正在涌向对话式 AI；
#   对话式 AI 是大泛类，消费声音侧（ElevenLabs）与企业智能体侧（Sierra）都算。
#
# 数据纪律（与 R11 的 P8 换血同一条）：图上每个数都能在 foot 的 SOURCE 行找到来源与
#   年份；拿不到全类别口径的层，用「代表性大轮次之和」并在 sm 行与 foot 里如实写明，
#   **带宽只是量级示意、非等比**这一句也写进 foot，不拿图形冒充等比坐标。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    # 时间 × 层级的资金流向图：x 轴三格年份（2024 / 2025 / 2026 至今），
    # 三条横带按层级排开，每条带三段各给一个 stroke-width（粗细 = 量级）。
    # 坐标账：带轨 x 300→1620，年份格心 520 / 960 / 1400；
    #   带 A 心 y=124（段宽 20/40/64）· 带 B 心 y=272（10/22/24）· 带 C 心 y=412（8/18/44）。
    #   每段长 440，.dw 一律 --len:460 盖得住；带 C 另挂一条 pkt 走带光点（1320 长 → --p1:-1480px）。
    F_FLOW = '''<section class="slide r12flow">
  <div class="chrome"><span>PART 1 · 语法变了</span><span>7</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走</div>
      <h2 class="ink" style="--i:1">近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em></h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 530" width="1680" fill="none">
          <!-- 年份格 -->
          <g class="pop" style="--i:2">
            <path class="stroke" stroke-width="1" opacity=".22" d="M300 34 V478 M740 34 V478 M1180 34 V478 M1620 34 V478"/>
            <text class="lbl" x="520" y="18" text-anchor="middle">2024</text>
            <text class="lbl" x="960" y="18" text-anchor="middle">2025</text>
            <text class="lbl" x="1400" y="18" text-anchor="middle">2026 至今</text>
          </g>

          <!-- 带 A · 基础模型：一路最粗，三年都是最大头 -->
          <text class="ttl pop" style="--i:3" x="0" y="116">基础模型</text>
          <text class="lbl pop" style="--i:3" x="0" y="148">FOUNDATION MODELS</text>
          <path class="stroke dw" style="--len:460;--i:3" stroke-width="20" d="M300 124 H740"/>
          <path class="stroke dw" style="--len:460;--i:4" stroke-width="40" d="M740 124 H1180"/>
          <path class="stroke dw" style="--len:460;--i:5" stroke-width="64" d="M1180 124 H1620"/>
          <text class="big pop" style="--i:3" x="520" y="72" text-anchor="middle">$31.4B</text>
          <text class="big pop" style="--i:4" x="960" y="72" text-anchor="middle">$88.9B</text>
          <text class="big pop" style="--i:5" x="1400" y="72" text-anchor="middle">$178B</text>
          <text class="sm pop" style="--i:5" x="300" y="182">三个数都是当年全年融资额（2026 只到 Q1）· 2025 年全部 AI 融资的 41% 进了这一层，OpenAI · Anthropic · xAI 三家就占 38%</text>

          <!-- 带 B · Coding：第二波，2025 翻倍，2026 开始兑现成收入 -->
          <text class="ttl pop" style="--i:6" x="0" y="264">AI 写代码</text>
          <text class="lbl pop" style="--i:6" x="0" y="296">CODING</text>
          <path class="stroke dw" style="--len:460;--i:6" stroke-width="10" d="M300 272 H740"/>
          <path class="stroke dw" style="--len:460;--i:7" stroke-width="22" d="M740 272 H1180"/>
          <path class="stroke dw" style="--len:460;--i:8" stroke-width="24" d="M1180 272 H1620"/>
          <text class="big pop" style="--i:6" x="520" y="232" text-anchor="middle">$1.6B</text>
          <text class="big pop" style="--i:7" x="960" y="232" text-anchor="middle">$3.3B</text>
          <text class="big pop" style="--i:8" x="1400" y="232" text-anchor="middle">$2B ARR</text>
          <text class="sm pop" style="--i:8" x="300" y="316">前两格是全年融资额，一年翻一倍；第三格换了口径 —— Cursor 的年化收入，第二波已经开始兑现</text>

          <!-- 带 C · 对话式 AI：由细变粗，正在发生（整组挂 data-step=1，讲到这里才出现） -->
          <g data-step="1">
            <text class="ttl fill-am pop" style="--i:0" x="0" y="404">对话式 AI</text>
            <text class="lbl pop" style="--i:0" x="0" y="436">CONVERSATIONAL AI</text>
            <path class="stroke-am dw" style="--len:460;--i:0" stroke-width="8" d="M300 412 H740"/>
            <path class="stroke-am dw" style="--len:460;--i:1" stroke-width="18" d="M740 412 H1180"/>
            <path class="stroke-am dw" style="--len:460;--i:2" stroke-width="44" d="M1180 412 H1620"/>
            <path class="stroke-am pkt" stroke-width="10"
              style="--pl:140px;--p0:140px;--p1:-1480px;--pt:6.4s;--pd:1.2s" d="M300 412 H1620"/>
            <text class="big fill-am pop" style="--i:0" x="520" y="368" text-anchor="middle">$2.1B</text>
            <text class="big fill-am pop" style="--i:1" x="960" y="368" text-anchor="middle">≈$0.7B</text>
            <text class="big fill-am pop" style="--i:2" x="1400" y="368" text-anchor="middle">≈$2.2B</text>

            <!-- 大泛类的两翼：一边消费声音，一边企业智能体，花的是同一笔钱 -->
            <path class="stroke-am pop" style="--i:3" stroke-width="1.4" opacity=".55" d="M760 423 V452 M1320 436 V452"/>
            <text class="lbl fill-am pop" style="--i:3" x="300" y="478">同一层的两翼</text>
            <text class="txt pop" style="--i:3" x="760" y="478" text-anchor="middle">ElevenLabs $500M @ $11B</text>
            <text class="sm pop" style="--i:3" x="760" y="508" text-anchor="middle">消费声音侧</text>
            <text class="txt pop" style="--i:3" x="1320" y="478" text-anchor="middle">Sierra $950M @ $15B</text>
            <text class="sm pop" style="--i:3" x="1320" y="508" text-anchor="middle">企业智能体侧</text>
          </g>
        </svg>
      </div>
      <div class="note" data-step="2"><span class="flow" style="--i:0">2024 全年，整个语音 AI 一共拿到 $2.1B；2026 光是上半年这五笔，加起来就已经顶得上那一整年。<b>对话式 AI 是个大泛类：消费侧的声音和企业侧的智能体，花的是同一笔钱。这笔钱在这一层内部又分给了谁——下一页拆开看。</b></span></div>
      <div class="foot flow rev" style="--i:9">SOURCE · 基础模型层三个数＝当年全年融资额（2026 为 Q1 单季）：Crunchbase 2026-04；「41%」与「三家占 38%」：CB Insights《State of AI 2025》2026-01（2025 年私有 AI 融资 $225.8B）· Coding 层 2024 / 2025＝pure-play 编码工具全年融资额：New Market Pitch 2026-07（2025 的 $3.3B 里 Cursor 一家占 $3.2B）；$2B 年化收入：TechCrunch 2026-04 · 对话式层 2024 $2.1B＝语音 AI 全年融资、8× 于 2023：CB Insights，转引 PYMNTS 2025-06；2025 ≈$0.7B＝Sierra $350M ＋ Sesame $250M（TechCrunch 2025-10）＋ Cartesia $100M；2026 ≈$2.2B＝ElevenLabs $500M（CNBC 2026-02）＋ Sierra $950M（SiliconANGLE 2026-05，同源回溯 2025-09 的 $350M 前轮）＋ Parloa $350M（TechCrunch 2026-01）＋ Decagon $250M（Bloomberg 2026-01）＋ Deepgram $130M（Newcomer 2026-02）—— 后两格是代表性大轮之和、本页自算，不是全类别口径 · 带宽为量级示意，非等比</div>
    </div>
  </div>
</section>'''
    _secs.append(F_FLOW)
    _I_FLOW = len(_secs) - 1
    assert _I_FLOW == 62, f'C12 · 新页应是第 63 个元素，实际下标 {_I_FLOW}'

    # ── C12-② 现 P7（钱页）eyebrow 改成衔接句 ────────────────────────────────
    #    「先看钱往哪儿去了」这句话已经由新页整页承担了，原位换成「再往里看一层」的承接。
    _r1(6, '<div class="eyebrow flow" style="--i:0">先看钱往哪儿去了</div>',
           '<div class="eyebrow flow" style="--i:0">钱到了对话式 AI，再往里看一层：它分给了谁</div>')

# ══════════════════════════════════════════════════════════════════════════════
# ── C13（2026-08-05 · R13 · 七处内容修订 · 页数不变 46）─────────────────────────
# Colin 的反馈横跨 45/46 两个页码版，所以这一层**一律用内容锚定**（_r1/_cut1 的
#   字符串锚点都是页上的原话），不信页码。_secs 下标仍是母版 62 页的原始下标。
#   ① P4  一个人都没有  _secs[3]  · 补贝尔 1876 的人类第一通电话原话（左栏两条引文叠一摞）
#   ② P5  本场提要      _secs[4]  · 路线图字号回调（R10/R11 放大过猛，站名 82 → 46px）
#   ③ P16 灵魂拷问      _secs[27] · 补 Kevin Weil 金句作 data-step=1 的第二拍（问→答）
#   ④ P17 Eval 第一课   _secs[28] · 「B 如 Boy」→ 英语习惯拼读法「A as in Apple · B as in Boy」
#   ⑤ P22 案例 02       _secs[33] · 3.08% 表意纠正：两个数都是**意向转化率**，Agent 已强过人
#   ⑥ P25 金句 03       _secs[36] · 换 Bret Taylor「perfect human」原句（换下「能被计量的同事」）
#   ⑦ P33 金句 04       _secs[45] · 围栏 Part 点睛重写（换下「架构的围栏…护城河」）
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    # ── C13-① P4 今年这段通话里一个人都没有 · 把人类第一通电话写进「150 年」──────
    #    R11 已经把 PSTN 改成「跑了 150 年」并在灰 note 里注了贝尔 1876。R13 再进一步：
    #    左栏做成两条引文的一摞 —— 上面是 2026 的 Bret（英语跑在电话网上），
    #    下面是 1876 的贝尔（人类第一通电话）。同一条线的两端，一页读完 150 年。
    #    .g-38 是两列栅格，直接并排两个 .quote 会把第二条挤到第二行，所以套一层 .qstack。
    _r1(3, '''      <div class="g-38">
        <div class="quote flow" style="--i:11">
          <div class="en sm">&#8220;You have all these fancy MCP things, and we&#8217;re doing English over PSTN.&#8221;</div>
          <div class="by">Bret Taylor · CEO of Sierra / Chairman of OpenAI · 2026-03 公开访谈</div>
        </div>
        <div class="mid">''',
           '''      <div class="g-38">
        <div class="qstack">
          <div class="quote flow" style="--i:11">
            <div class="en sm">&#8220;You have all these fancy MCP things, and we&#8217;re doing English over PSTN.&#8221;</div>
            <div class="by">Bret Taylor · CEO of Sierra / Chairman of OpenAI · 2026-03 公开访谈</div>
          </div>
          <div class="quote co flow" style="--i:12">
            <div class="en sm">&#8220;Mr. Watson — come here — I want to see you.&#8221;</div>
            <div class="by">贝尔 · 1876 · 人类第一通电话，今年整 150 年</div>
          </div>
        </div>
        <div class="mid">''')
    _cls(3, 'r13bell')

    # ── C13-② P5 本场提要 · 路线图字号回调到优雅档 ────────────────────────────
    #    R10-① 把这张图纵向 ×4.6 并把站名推到 76px，R11-③ 删站之后又推到 82px ——
    #    Colin：大到顶格，美感没了。R13 回调：站名 46 / PART 标 24 / 副题 25（CSS 档），
    #    圆点半径 19/17 → 11/10、线宽 3/6 → 2/4（图内属性），四行 y 同步收拢并居中：
    #      PART 标 368 → 468 · 线与圆点 543 → 580 · 站名 773 → 746 · 副题 948 → 856
    #    viewBox 仍是 0 320 1680 665（不动，.body 填充率与 C10/C11 的既有断言一并保住），
    #    上下留白各 ≈120 —— 这就是「大而清爽」而不是「大到顶格」。
    _cut1(4, '<!-- 全场路线', '</svg>', '''<!-- 全场路线：四站一条线。第一站讲「变了什么」，后三站分别回答托付时代的三个问题。
             R13 字号回调：站名 46px，圆点/线宽同步回收，四行在 viewBox 内垂直居中。 -->
        <svg viewBox="0 320 1680 665" width="1680" fill="none">
          <path class="stroke dw" style="--len:1500;--i:6" stroke-width="2" d="M140 580 H1600"/>
          <path class="stroke-am dw" style="--len:1010;--i:7" stroke-width="4" d="M627 580 H1600"/>

          <circle class="fill-am pop" style="--i:7" cx="140" cy="580" r="11"/>
          <g class="pop" style="--i:8" fill="var(--slide-bg)" stroke="var(--amber)" stroke-width="3.5">
            <circle cx="627" cy="580" r="10"/><circle cx="1113" cy="580" r="10"/><circle cx="1600" cy="580" r="10"/>
          </g>

          <text class="lbl fill-am pop" style="--i:7" x="140" y="468" text-anchor="middle">PART 1</text>
          <text class="lbl fill-am pop" style="--i:8" x="627" y="468" text-anchor="middle">PART 2</text>
          <text class="lbl fill-am pop" style="--i:8" x="1113" y="468" text-anchor="middle">PART 3</text>
          <text class="lbl fill-am pop" style="--i:8" x="1600" y="468" text-anchor="middle">PART 4</text>

          <text class="txt pop" style="--i:9" x="140" y="746" text-anchor="middle">语法变了</text>
          <text class="txt pop" style="--i:9" x="627" y="746" text-anchor="middle">被托付</text>
          <text class="txt pop" style="--i:9" x="1113" y="746" text-anchor="middle">双向奔赴</text>
          <text class="txt pop" style="--i:9" x="1600" y="746" text-anchor="middle">人与组织</text>

          <text class="sm pop" style="--i:10" x="140" y="856" text-anchor="middle">从调用到双向奔赴</text>
          <text class="sm fill-am pop" style="--i:10" x="627" y="856" text-anchor="middle">尺子、授权与边界</text>
          <text class="sm fill-am pop" style="--i:10" x="1113" y="856" text-anchor="middle">出事了算谁的</text>
          <text class="sm fill-am pop" style="--i:10" x="1600" y="856" text-anchor="middle">你和团队怎么变</text>
        </svg>''')
    _cls(4, 'r13p5')

    # ── C13-③ 灵魂拷问页 · 加 Kevin Weil 金句作第二拍 ──────────────────────────
    #    R10-⑧ 把这句从终页删掉了（终页改成纯图收场）；它真正的位置在这里 ——
    #    全页大字问句先砸下来，data-step=1 再揭金句，问 → 答两拍。
    _r1(27, '<div class="q ink" style="--i:2">在座的有多少人，<br>'
            '<span class="hl">亲手写过</span>一份自己产品的评测集？</div>',
            '<div class="q ink" style="--i:2">在座的有多少人，<br>'
            '<span class="hl">亲手写过</span>一份自己产品的评测集？</div>\n'
            '    <div class="quote co flow" data-step="1" style="--i:0">\n'
            '      <div class="en">&#8220;Writing evals is the most important thing '
            'a PM can do in the AI era.&#8221;</div>\n'
            '      <div class="by">Kevin Weil · OpenAI 前 CPO</div>\n'
            '    </div>')
    _cls(27, 'r13ask')

    # ── C13-④ Eval 第一课 · 题之骗 ·「B 如 Boy」→ 英语习惯拼读法 ────────────────
    #    真实通话里对方念的是 "A as in Apple, B as in Boy"，不是中式直译的「B 如 Boy」。
    #    svg 那行加了前半句之后仍在 x=0→≈420 之内，离最左一列打叉（x=489）还有余量。
    _r1(28, '<text class="sm pop" style="--i:7" x="0" y="306">B 如 Boy · 0086 · 一位一位念</text>',
            '<text class="sm pop" style="--i:7" x="0" y="306">'
            'A as in Apple · B as in Boy · 0086 · 一位一位念</text>')
    _r1(28, '在「B 如 Boy、0086」上<b>全崩</b>', '在「A as in Apple、0086」上<b>全崩</b>')

    # ── C13-⑤ 案例 02 · 3.08% 表意纠正（R11-⑧ 误标成「被识破率」）───────────────
    #    Colin 定：3.08% 与 1.5% 是**同一把尺子** —— 都是意向转化率。
    #    所以这一页的结论不是「它已经贴到人的极限」，而是「它已经强过人」：
    #    3.08% ≈ 人工基线 1.5% 的两倍。两栏加一条等宽底座的比例条（100% : 49%），
    #    Agent 那条更长并走 amber，视觉方向与主句一致。1.5% 的口径标注原样保留。
    _cut1(33, '\n      <div class="cmp2">', '它已经贴到人工坐席自己的极限上了。</b></div>', '''
      <div class="cmp2">
        <div class="c am rise" style="--i:8">
          <div class="k">AI 坐席 · 本案例全量标注</div>
          <div class="v">3.08%</div>
          <div class="bar"><i style="width:100%"></i></div>
          <div class="l">意向转化率</div>
          <div class="u">一通电话打完，客户留下明确意向的比例</div>
        </div>
        <div class="vs pop" style="--i:9">VS</div>
        <div class="c rise" style="--i:10">
          <div class="k">人工坐席 · 上线前人工基线 · 内部口径</div>
          <div class="v">1.5%</div>
          <div class="bar"><i style="width:49%"></i></div>
          <div class="l">意向转化率</div>
          <div class="u">同一条产线、同一批名单，上线前人工坐席的水平</div>
        </div>
      </div>
      <div class="land flow" style="--i:11">它不是在<b>逼近</b>人的水平——<b class="am">3.08% 对 1.5%，它已经把人工基线翻了一倍。</b></div>''')
    _cls(33, 'r13case')

    # ── C13-⑥ 金句 03 · 换成 Bret Taylor 的「perfect human」原句 ────────────────
    #    被换下的是「一个能被计量的同事，才是真的同事。」（全 deck 仅此一处，别页正文无）。
    #    ⚠️ 出处：本仓库 csagent.html / outcome.html 里都没有这句的逐字原文（已 grep），
    #       所以署名口径按 csagent / 3years 一致的那行写「Bret Taylor · Sierra CEO /
    #       OpenAI 董事长」，不替他补一个没核到的播客集数。
    _cut1(36, '\n    <div class="q">', '是为了敢把事交给它。</div>', '''
    <div class="q">
      <i class="rise" style="--i:1">&#8220;One of the biggest fallacies in AI</i>
      <i class="rise" style="--i:2">is people compare it with this perfect human</i>
      <i class="rise" style="--i:3">that does not exist.&#8221;</i>
    </div>
    <div class="rule"></div>
    <div class="zh rise" style="--i:4">AI 最大的谬误之一，是人们总把它跟一个并不存在的完美的人相比。</div>
    <div class="s rise" style="--i:5">Bret Taylor · Sierra CEO / OpenAI 董事长</div>''')
    _cls(36, 'r13mq')

    # ── C13-⑦ 金句 04 · 围栏 Part 的点睛重写 ───────────────────────────────────
    #    被换下的是「提示词只能拦住一些越权，架构的围栏，才是产品经理的护城河。」——
    #    Colin 判定它像 Waymo 那一案的总结，不是整个 PART 3 的点睛。
    #    钉死的内核：双向奔赴的内核 = 围栏。有了围栏（提示词 + 产品架构），
    #    才有能担起责任、扛得起 OKR 的 Agent，执行流从此摆脱人的辅助。
    _cut1(45, '\n    <div class="q">', '只有你先表示出来的那些东西。</div>', '''
    <div class="q">
      <i class="rise" style="--i:1">围栏不是拦住它，</i>
      <i class="rise" style="--i:2">是放出它。</i>
    </div>
    <div class="rule"></div>
    <div class="s rise" style="--i:4">提示词 + 产品架构，围出一条不用人扶的执行流——围栏有多硬，敢交给它的 OKR 就有多重。</div>''')
    _cls(45, 'r13fence')

# ══════════════════════════════════════════════════════════════════════════════
# ── C14（2026-08-05 · R14 · 两处 · 页数不变 46）────────────────────────────────
# 一律内容锚定取页（Colin 的反馈横跨多个页码版，不信页号）：
#   ① P2 开场「第三次，站上同一个舞台」→「讲台」（全页 grep 逐处改，eyebrow 早就是「回到讲台」）
#   ② R12 新增的钱流向页：三条层带 → **真正的双轴时间图** + foot 来源瘦身成一行
#      （被撤下的详细口径全文留档在设计文档 R14 段，页面上不再背这一大坨）
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    # ── C14-① P2 舞台 → 讲台 ────────────────────────────────────────────────
    #    这一页只有 h2 里一处「舞台」（eyebrow 本来就写「回到讲台」），但按 Colin 的话
    #    做成「全页逐处替换」，以后正文再冒出「舞台」也会一并跟着改，不用回来补。
    _I_P2 = [_i for _i, _x in enumerate(_secs) if '第三次，站上同一个舞台' in _x]
    assert len(_I_P2) == 1, f'C14-① P2 锚点不唯一：{_I_P2}'
    _I_P2 = _I_P2[0]
    assert _secs[_I_P2].count('舞台') >= 1, 'C14-① P2 没找到「舞台」'
    _secs[_I_P2] = _secs[_I_P2].replace('舞台', '讲台')
    assert '舞台' not in _secs[_I_P2] and '第三次，站上同一个讲台' in _secs[_I_P2], 'C14-① 改字未落地'

    # ── C14-② 钱流向页 · 视觉重做成双轴时间图 + 来源瘦身 ──────────────────────
    #    R12 的三条横带（带宽 = 量级示意）表达不清：带宽既不是等比坐标，也读不出「涨没涨」。
    #    R14 换成真正的双轴时间图 —— x 是三个年份刻度，y 是钱，涨落一眼看得见。
    #
    #    坐标账（viewBox 0 40 1680 530）：
    #      年份格心 x = 300 / 720 / 1140；绘图区 x 230→1200，y 120（顶）→470（基线）。
    #      左轴（基础模型）0–200：y = 470 − 1.75v → 31.4→415 · 88.9→314 · 178→158
    #      右轴（Coding / 对话式）0–4：y = 470 − 87.5v → 1.6→330 · 3.3→181
    #                                                   2.1→286 · 0.7→409 · 2.2→278
    #      两套刻度恰好落在同五条网格线上（120 / 207.5 / 295 / 382.5 / 470）——
    #      双轴最怕的「两套网格打架」在这里被数值本身消掉了，只画一套网格。
    #      右轴刻度数字 x=1218，终点名牌 x=1262 起（右留白 418px 够挂两翼小标）。
    #
    #    dataviz 纪律：
    #      · 轴/网格退到 hair 三档（6%/12%/24%）、实线、1px，数据线是唯一响的东西；
    #      · 无 3D 无阴影无装饰，面积只有一层 ≤22% 的渐变薄雾；
    #      · 三条线颜色 + 粗细双重编码；节点带底色描边环（surface ring）；
    #      · 值标只在起点/拐点/终点，终点走名牌，不是每点都挂数字；
    #      · 量级差用双轴解决，图内另加一行小注「左右两轴量级不同」防误读。
    #    ⚠️ Coding 那条：2026 没有可比的融资口径，所以**线到 2025 为止**，
    #       第三点不画、也不画虚线补到第三点 —— Cursor 的 $2B 是 ARR，
    #       把它画进融资轴就是造假，只以一行小注挂在线的末端。
    _I14 = [_i for _i, _x in enumerate(_secs) if '近三年，钱的三次落点' in _x]
    assert len(_I14) == 1, f'C14-② 钱流向页锚点不唯一：{_I14}'
    _I14 = _I14[0]
    _cut1(_I14, '        <svg viewBox="0 0 1680 530"', '        </svg>', '''        <svg viewBox="0 40 1680 530" width="1680" fill="none">
          <defs>
            <linearGradient id="r14conv" gradientUnits="userSpaceOnUse" x1="0" y1="270" x2="0" y2="470">
              <stop class="g0" offset="0"/><stop class="g1" offset="1"/>
            </linearGradient>
          </defs>

          <!-- ① 双轴与网格：五条刻度线两轴共用（左 0/50/100/150/200 · 右 0/1/2/3/4），淡到只做参考 -->
          <g class="pop" style="--i:1">
            <path class="gd" d="M230 120 H1200 M230 207.5 H1200 M230 295 H1200 M230 382.5 H1200"/>
            <path class="ax" d="M230 120 V470 M1200 120 V470"/>
            <path class="axb" d="M230 470 H1200"/>
            <text class="lbl" x="212" y="96" text-anchor="end">基础模型 $B</text>
            <text class="lbl" x="212" y="127" text-anchor="end">200</text>
            <text class="lbl" x="212" y="214" text-anchor="end">150</text>
            <text class="lbl" x="212" y="302" text-anchor="end">100</text>
            <text class="lbl" x="212" y="389" text-anchor="end">50</text>
            <text class="lbl" x="212" y="477" text-anchor="end">0</text>
            <text class="lbl" x="1218" y="96">Coding / 对话式 $B</text>
            <text class="lbl" x="1218" y="127">4</text>
            <text class="lbl" x="1218" y="214">3</text>
            <text class="lbl" x="1218" y="302">2</text>
            <text class="lbl" x="1218" y="389">1</text>
            <text class="lbl" x="1218" y="477">0</text>
          </g>

          <!-- ② X 轴：三刻度，2026 标「至今」；量级小注防双轴误读 -->
          <g class="pop" style="--i:2">
            <text class="lbl yr" x="300" y="508" text-anchor="middle">2024</text>
            <text class="lbl yr" x="720" y="508" text-anchor="middle">2025</text>
            <text class="lbl yr" x="1140" y="508" text-anchor="middle">2026</text>
            <text class="lbl" x="1140" y="538" text-anchor="middle">至今</text>
            <text class="lbl" x="230" y="538">左右两轴量级不同 · 左轴 0–200，右轴 0–4（$B）</text>
          </g>

          <!-- ③ 基础模型（左轴）：31.4 → 88.9 → 178，白粗线，三年都是最大头 -->
          <path class="ln fnd dw" style="--len:950;--i:3" d="M300 415 C 440 406 580 331 720 314 C 860 297 1000 234 1140 158"/>
          <circle class="dot fnd pop" style="--i:4" cx="300" cy="415" r="5.5"/>
          <circle class="dot fnd pop" style="--i:4" cx="720" cy="314" r="5.5"/>
          <circle class="dot fnd pop" style="--i:5" cx="1140" cy="158" r="7.5"/>
          <text class="txt val pop" style="--i:4" x="322" y="448">$31.4B</text>
          <text class="txt val pop" style="--i:4" x="742" y="344">$88.9B</text>
          <path class="lead fnd pop" style="--i:5" d="M1156 158 H1250"/>
          <text class="ttl pop" style="--i:5" x="1262" y="150">基础模型</text>
          <text class="big pop" style="--i:5" x="1262" y="196">$178B</text>

          <!-- ④ AI 写代码（右轴）：1.6 → 3.3；2026 无可比融资口径，线到 2025 为止，
               第三点不画、虚线也不补 —— Cursor 的 $2B 是 ARR，不进融资轴，只作末端小注 -->
          <path class="ln cod dw" style="--len:490;--i:6" d="M300 330 C 440 322 580 210 720 181"/>
          <circle class="dot cod pop" style="--i:6" cx="300" cy="330" r="5.5"/>
          <circle class="dot cod pop" style="--i:7" cx="720" cy="181" r="7.5"/>
          <text class="txt val pop" style="--i:6" x="322" y="362">$1.6B</text>
          <text class="ttl pop" style="--i:7" x="750" y="154">AI 写代码</text>
          <text class="big pop" style="--i:7" x="891" y="154">$3.3B</text>
          <text class="sm anno pop" style="--i:8" x="750" y="190">2026 转向收入兑现 · Cursor ARR $2B</text>

          <!-- ⑤ 对话式 AI（右轴）：2.1 → 0.7 → 2.2+，amber 粗线 + 末段上勾 + 走线光点，
               曲线下压一层渐变薄雾 —— 钱正在往这一层灌。整组 data-step=1，讲到这里才出现 -->
          <g data-step="1">
            <path fill="url(#r14conv)" stroke="none" d="M300 286 C 440 302 580 400 720 409 C 908 425 1060 400 1140 278 L1140 470 L300 470 Z"/>
            <path class="ln cnv dw" style="--len:960;--i:0" d="M300 286 C 440 302 580 400 720 409 C 908 425 1060 400 1140 278"/>
            <path class="stroke-am pkt" stroke-width="9"
              style="--pl:120px;--p0:120px;--p1:-1040px;--pt:6.4s;--pd:1.2s" d="M300 286 C 440 302 580 400 720 409 C 908 425 1060 400 1140 278"/>
            <circle class="dot cnv pop" style="--i:0" cx="300" cy="286" r="5.5"/>
            <circle class="dot cnv pop" style="--i:1" cx="720" cy="409" r="5.5"/>
            <circle class="dot cnv pop" style="--i:2" cx="1140" cy="278" r="8"/>
            <text class="txt val fill-am pop" style="--i:0" x="322" y="264">$2.1B</text>
            <text class="txt val fill-am pop" style="--i:1" x="742" y="452">&#8776;$0.7B</text>
            <path class="lead cnv pop" style="--i:2" d="M1156 278 H1250"/>
            <text class="ttl fill-am pop" style="--i:2" x="1262" y="270">对话式 AI</text>
            <text class="big fill-am pop" style="--i:2" x="1262" y="316">$2.2B+</text>
            <text class="sm wing pop" style="--i:3" x="1262" y="352">消费声音侧 · ElevenLabs $500M @ $11B</text>
            <text class="sm wing pop" style="--i:3" x="1262" y="382">企业智能体侧 · Sierra $950M @ $15B</text>
          </g>
        </svg>''')
    #    foot 瘦身成一行：只留来源名，详细口径（每层的年份/口径/自算说明）移入设计文档 R14 段留档。
    _cut1(_I14, '<div class="foot flow rev" style="--i:9">SOURCE', '带宽为量级示意，非等比</div>',
          '<div class="foot flow rev" style="--i:9">Source · Crunchbase · CB Insights《State of AI 2025》'
          '· TechCrunch · Bloomberg · CNBC</div>')
    _cls(_I14, 'r14money')

# ══════════════════════════════════════════════════════════════════════════════
# ── C15（2026-08-05 · R15 终轮 · 十项 · 页数不变 46）──────────────────────────
# Colin：「至此改完全部内容」。这一层是收官轮，十项：
#   ① 三个主标题（钱分布 / 渗透采购 / 四方观点），eyebrow 与新 h2 语义重复的顺手精简
#   ② 四方观点页中心块英文标 Conversational AI → CONVOAI AGENT
#   ③ 北极星页：nstar 四栏与阶梯四级**逐列对齐** + note 整段删（删后撑满）
#   ④ PART 2 被托付幕卡换金句（Agent＝代理人的双关反转）
#   ⑤ 分水岭页 land 整段删（删后撑满）
#   ⑥ Eval 第一课 foot 整句删（删后撑满）
#   ⑦ 金句 02 换成 Kevin Weil；灵魂拷问页撤掉 R13 加的第二拍（全场 Weil 仅一处）
#   ⑧ 自治爬梯页 L 记号重编 L0-L4 → L1-L5（BIG JUMP 位置不动 → 天然 = L2→L3）
#   ⑨ 全 deck L 记号连坐（岗位散点页 / 案例 02 / 执行的围栏 / 全场收束）
#   ⑩ 终检：R14 留下的「这五笔」→「这几笔」+ 悬空引用终扫
# 取页一律**内容锚定**（_ix 按正文找 _secs 下标），不信页号；母版 62 页仍然只读。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    def _ix(needle):
        """按正文在母版 62 页里找唯一那一节（R15 起全部改动都走这个入口，不写死页号）"""
        _h = [_i for _i, _x in enumerate(_secs) if needle in _x]
        assert len(_h) == 1, f'C15 · 锚点不唯一/未命中「{needle[:30]}」：{_h}'
        return _h[0]

    # ── C15-① 三个主标题 ────────────────────────────────────────────────────
    # a) 钱分布页（ElevenLabs / OpenAI / Sierra 六张卡）——「这不是一个垂类」是一句
    #    反驳式的话，台下没听过反面观点就接不住；换成一句直说的题。
    #    eyebrow 原文「钱到了对话式 AI，再往里看一层：它分给了谁」与新 h2 是近义重复，
    #    只留承接功能，精简成六个字。
    _I_M8 = _ix('这不是一个垂类，是整个对话式 AI 在同时点火')
    _r1(_I_M8, '<h2 class="ink" style="--i:1">这不是一个垂类，是整个对话式 AI 在同时点火</h2>',
                '<h2 class="ink" style="--i:1">对话式 AI 的钱，<em>流向了哪里</em></h2>')
    _r1(_I_M8, '<div class="eyebrow flow" style="--i:0">钱到了对话式 AI，再往里看一层：它分给了谁</div>',
                '<div class="eyebrow flow" style="--i:0">承上页，再往里看一层</div>')

    # b) 渗透采购页 —— 「预测还在打架」的对照仍在 note 里（「至于预测？…还在打架」），
    #    所以主标不再背它，直接说结论：采购正在悄然发生。
    _I_BUY = _ix('<em>采购已经开动</em>')
    _r1(_I_BUY, '<h2 class="ink" style="--i:1">预测还在打架，<em>采购已经开动</em></h2>',
                 '<h2 class="ink" style="--i:1">对话式智能体的采购，<em>正在悄然发生</em></h2>')

    # c) 四方观点页 —— 原 h2「四个互不相干的人，说了同一件事」降回 eyebrow
    #    （C3 当年正是把它从 eyebrow 提上来的，这一步是原路退回），
    #    h2 换成 note 里那句真正的判断；note 去掉被提上去的那一句，其余保留现文。
    _I_FOUR = _ix('四个互不相干的人，说了<em>同一件事</em>')
    _r1(_I_FOUR, '<div class="eyebrow flow" style="--i:0">所有的路，最后都汇到「对话」这条线上</div>',
                  '<div class="eyebrow flow" style="--i:0">四个互不相干的人，说了同一件事</div>')
    _r1(_I_FOUR, '<h2 class="ink" style="--i:1">四个互不相干的人，说了<em>同一件事</em></h2>',
                  '<h2 class="ink" style="--i:1">对话式智能体在企业服务侧，<em>已经到了规模化应用的阶段</em></h2>')
    _r1(_I_FOUR, '四个方向的人，指向同一个判断：<b class="am">对话式智能体在企业服务侧，'
                 '已经到了规模化应用的阶段</b>——智能够用、部署可做、',
                 '四个方向的人，指向同一个判断：智能够用、部署可做、')

    # ── C15-② 四方观点页中心块英文标 ────────────────────────────────────────
    #    「对话式智能体」下面那行英文是全场唯一一处对这个词的英文表述，
    #    统一成产品线口径 CONVOAI AGENT（与 P37 全景页的 ConvoAI Engine 同宗）。
    _r1(_I_FOUR, '>Conversational AI</text>', '>CONVOAI AGENT</text>')

    # ── C15-③ 北极星页：逐列对齐 + note 整段删 ──────────────────────────────
    #    a) 对齐账（实测 body 宽 1680px，svg viewBox 0 0 1680 520 → 1 单位 = 1px）：
    #       .nstar 是 `1fr×4 + gap:26`，四列 x = [0,400.5] [426.5,827] [853,1253.5] [1279.5,1680]。
    #       原阶梯四级是 [20,420] [420,820] [820,1220] [1220,1660]，与列位差 20–40px，
    #       四栏读起来「差一点点」最难受。改法：**每一级的水平段 = 对应那一列的完整跨度**，
    #       级与级之间的竖梁改走 26px 空档里的斜梁（几乎垂直，看着仍是阶梯）。
    #       文字 x 同步落到列左沿 —— 于是 svg 文字与下方 nstar 文字共用一条左边线。
    #       --len 逐条配套：斜梁 √(26²+87²)≈91，加 400.5 的水平段 ≈491 → 一律给 500。
    _I_NS = _ix('四个阶段，四颗<em>北极星</em>')
    for _o, _n in (
        ('d="M20 443 H420"', 'd="M0 443 H400.5"'),
        ('style="--len:400;--i:0" stroke-width="2" d="M0 443 H400.5"',
         'style="--len:410;--i:0" stroke-width="2" d="M0 443 H400.5"'),
        ('d="M420 443 V356 H820"', 'd="M400.5 443 L426.5 356 H827"'),
        ('d="M820 356 V270 H1220"', 'd="M827 356 L853 270 H1253.5"'),
        ('d="M1220 270 V184 H1660"', 'd="M1253.5 270 L1279.5 184 H1680"'),
        ('style="--len:540;--i:1" stroke-width="3" d="M1253.5 270 L1279.5 184 H1680"',
         'style="--len:500;--i:1" stroke-width="3" d="M1253.5 270 L1279.5 184 H1680"'),
        ('x="54" y="339"', 'x="0" y="339"'), ('x="54" y="384"', 'x="0" y="384"'),
        ('x="54" y="421"', 'x="0" y="421"'),
        ('x="454" y="253"', 'x="426.5" y="253"'), ('x="454" y="298"', 'x="426.5" y="298"'),
        ('x="454" y="335"', 'x="426.5" y="335"'),
        ('x="854" y="166"', 'x="853" y="166"'), ('x="854" y="212"', 'x="853" y="212"'),
        ('x="854" y="248"', 'x="853" y="248"'),
        ('x="1254" y="80"', 'x="1279.5" y="80"'), ('x="1254" y="125"', 'x="1279.5" y="125"'),
        ('x="1254" y="162"', 'x="1279.5" y="162"'),
        # 主语易位那条虚线：落到第三、四列中间那道 26px 空档的正中；标注贴第四列左沿
        ('d="M1200 43 V486"', 'd="M1266.5 43 V486"'),
        ('x="1216" y="480"', 'x="1279.5" y="480"'),
    ):
        _r1(_I_NS, _o, _n)
    #    b) note 整段删：三句话（「叫了三年 Agent…才算双向」/「错位」/「陪伴那半球…直接从被托付进」）
    #       —— 第一句打磨后上了 PART 2 幕卡（C15-④），「下午专场」的交接在分水岭页
    #       eyebrow 与图注里各留一处，不会因此悬空。
    _cut1(_I_NS, '<div class="note" data-step="3">', '「被托付」</b>进。</span></div>', '')
    assert '错位' not in _secs[_I_NS] and '下午 AIoT 专场整场拆开讲' not in _secs[_I_NS]
    _cls(_I_NS, 'r15nstar')

    # ── C15-④ PART 2 被托付幕卡 · 换金句 ────────────────────────────────────
    #    Colin 底稿：「我们叫了它三年 Agent（代理人），今天它终于变成了 Agent（代理人）」。
    #    定稿取「叫了三年 / 今天终于」的反转 + 名词→动词的双关落点：把第二个「代理人」
    #    从名词打成动词（「开始代理了」），一句话就说清 PART 2 要讲什么。
    #    第二行「这一幕只讲一件事：那把尺子怎么造」是本幕导航，保留不动。
    _I_ACT2 = _ix('<div class="cn spread" style="--i:3">被托付</div>')
    _r1(_I_ACT2, '<div class="d flow" style="--i:4">被记住，靠的是一致性。被托付，靠的是可验证。<br>'
                 '这一幕只讲一件事：那把尺子怎么造。</div>',
                 '<div class="d flow" style="--i:4">我们叫了它三年 Agent（代理人）——今天，它终于开始代理了。<br>'
                 '这一幕只讲一件事：那把尺子怎么造。</div>')

    # ── C15-⑤ 分水岭页 land 整段删 ──────────────────────────────────────────
    #    「你交出去的东西」这层意思，图上四级的副题（交出去「一步」/「一段」/「一个判断」/
    #    「一个结果」）已经把它说完了，land 是重复讲一遍。
    _I_LAD = _ix('工具 → 实习生 → 外包 → 专家 → <em>合伙人</em>')
    _cut1(_I_LAD, '<div class="land flow rev" style="--i:12">这四级换的不是它的能力',
                  '这一幕，讲的就是那把越来越硬的尺子。</span></div>', '')
    #    删后撑满：这张阶梯图「宽而扁」（1680×372），只放大宽度没用 —— 走 C9 的纵拉伸，
    #    y 整体 ×1.3（字号/半径不变），viewBox 同步加高；四级上行因此更陡，读起来更像「爬」。
    #    ⚠️ --len 与走线光点的行程必须配套：路径长 1438 → 1501，所以 1520→1560、-1560→-1620。
    _ystretch(_I_LAD, 1.3, ('viewBox="0 56 1680 372"', 'viewBox="0 73 1680 484"'), paths=(
        ('d="M40 330 H320"', 'd="M40 429 H320"'),
        ('d="M320 330 C 356 330, 356 384, 392 384 H1200"',
         'd="M320 429 C 356 429, 356 499, 392 499 H1200"'),
        ('d="M510 374 V352"', 'd="M510 486 V458"'),
        ('d="M840 374 V290"', 'd="M840 486 V377"'),
        ('d="M320 330 L370 268 H650 L700 206 H980 L1030 144 H1310 L1360 82 H1640"',
         'd="M320 429 L370 348 H650 L700 268 H980 L1030 187 H1310 L1360 107 H1640"'),
        ('d="M650 268 L700 206"', 'd="M650 348 L700 268"'),
        ('d="M702 202 L720 172"', 'd="M702 263 L720 224"'),
        ('--len:1520;--i:2', '--len:1560;--i:2'),
        ('--pl:110px;--p0:110px;--p1:-1560px', '--pl:110px;--p0:110px;--p1:-1620px'),
    ))
    _cls(_I_LAD, 'r15ladder')

    # ── C15-⑥ Eval 第一课 foot 整句删 ───────────────────────────────────────
    #    note 那两句（「六家主流方案…全崩」「你的 demo 里全是前一种题」）就是落点，
    #    foot 的「动作项」是第三次说同一件事。
    _I_EV1 = _ix('你的 demo 在骗你')
    _cut1(_I_EV1, '<div class="foot flow rev" style="--i:12">给产品经理的动作',
                  '换成客户上周真正打进来的那三通</div>', '')
    _cls(_I_EV1, 'r15eval1')

    # ── C15-⑦ 金句页调换：Weil 从拷问页搬到金句 02 ──────────────────────────
    #    R13-③ 把 Weil 加成拷问页的第二拍，Colin 复看后判定：拷问页就该是纯问句全页大字，
    #    Weil 该占一整张金句页。于是——
    #    a) 拷问页撤回第二拍（连 .r13ask 档位类一并摘掉，回到 R9 的 .r9p15 纯问句档）；
    #    b) 金句 02 换血：被换下的「你以为在选模型，其实在选评测。」全场仅此一处，
    #       换掉即全场清零（评测=资产这层意思由 P41「Evals are the new PRD」承接）。
    _I_ASK = _ix('亲手写过</span>一份自己产品的评测集？')
    _cut1(_I_ASK, '\n    <div class="quote co flow" data-step="1"', 'OpenAI 前 CPO</div>\n    </div>', '')
    _secs[_I_ASK] = _secs[_I_ASK].replace(' r13ask', '', 1)
    assert 'Kevin Weil' not in _secs[_I_ASK] and 'r13ask' not in _secs[_I_ASK]

    _I_MQ2 = _ix('你以为在选模型，')
    _cut1(_I_MQ2, '\n    <div class="q">', '真正的资产是后者。</div>', '''
    <div class="q">
      <i class="rise" style="--i:1">&#8220;Writing evals is the most important</i>
      <i class="rise" style="--i:2">thing a PM can do in the AI era.&#8221;</i>
    </div>
    <div class="rule"></div>
    <div class="zh rise" style="--i:4">写评测，是 AI 时代一个产品经理能做的最重要的事。</div>
    <div class="s rise" style="--i:5">Kevin Weil · OpenAI 前 CPO</div>''')
    _cls(_I_MQ2, 'r15mq')

    # ── C15-⑧ 自治爬梯页 · L 记号重编 L0-L4 → L1-L5 ─────────────────────────
    #    五阶一个不删，只把编号整体 +1，理由是与自动驾驶的 L1–L5 对齐：
    #    THE BIG JUMP（撤掉「人」这张安全网）夹在「起草」与「只读应答」之间，位置不动，
    #    重编后天然 = L2→L3 —— 正好是自动驾驶「L2 辅助驾驶 → L3 系统担责」那一跳。
    #    交叉验证条带上的 L1–L2 / L3–L5 分段标注因此不用改一个字就自洽。
    #    ⚠️ 从高到低替换，避免「改完 L0→L1 又被 L1→L2 二次命中」。
    _I_LDR = _ix('每一级之间隔着的不是技术，是<em>人还在不在环里</em>')
    for _o, _n in (('L4 · 主动外呼', 'L5 · 主动外呼'), ('L3 · 可执行', 'L4 · 可执行'),
                   ('L2 · 只读应答', 'L3 · 只读应答'), ('L1 · 起草', 'L2 · 起草'),
                   ('L0 · 旁听', 'L1 · 旁听'),
                   ('<!-- L2 / L3 / L4 -->', '<!-- L3 / L4 / L5 -->'),
                   ('<!-- L0 / L1 -->', '<!-- L1 / L2 -->')):
        _r1(_I_LDR, _o, _n)
    assert 'L0' not in _secs[_I_LDR], 'C15-⑧ 梯子上不该再有 L0'
    for _mk in ('自动驾驶 L1–L5', 'L1–L2 · 辅助驾驶，人不敢离环', 'L3–L5 · 系统担责，卡了十年的一跳',
                'L1–L2 · 行业还在边缘徘徊', 'L3–L5 · 还没人真正到达', '撤掉「人」这张安全网'):
        assert _mk in _secs[_I_LDR], f'C15-⑧ 交叉验证条带/BIG JUMP 不该被动到：{_mk}'

    # ── C15-⑨ 全 deck L 记号连坐 ────────────────────────────────────────────
    #    a) 岗位散点页：h2 重心 + 纵轴四档刻度 + 重心带标注（图上重心带 rect 罩住的
    #       正是「可执行 / 只读应答」两行，重编后 = L3 与 L4 之间，与新 h2 互证）
    _I_JOB = _ix('真实岗位放上梯子：今年的重心，压在 <em>L2 与 L3 之间</em>')
    for _o, _n in (('压在 <em>L2 与 L3 之间</em>', '压在 <em>L3 与 L4 之间</em>'),
                   ('>L4 主动<', '>L5 主动<'), ('>L3 可执行<', '>L4 可执行<'),
                   ('>L2 只读应答<', '>L3 只读应答<'), ('>L0–L1<', '>L1–L2<'),
                   ('今年整体重心：L2 与 L3 之间', '今年整体重心：L3 与 L4 之间')):
        _r1(_I_JOB, _o, _n)
    #    b) 案例 02 外呼销售：图上它的点就落在最高一档（主动外呼），重编后 = L5
    _I_C2 = _ix('一个 Agent 的入职三十天')
    _r1(_I_C2, '<span class="lv">Autonomy L4</span>', '<span class="lv">Autonomy L5</span>')
    #    c) 执行的围栏：「语音场景的 L2 门槛」指的是「直接对客户说话」那一级 → L3
    _I_FNC = _ix('执行的围栏：语音的动作，')
    _r1(_I_FNC, '语音场景的 L2 门槛，比文本高一级', '语音场景的 L3 门槛，比文本高一级')
    #    d) 全场收束 · 04 组织：两把梯子并列那句
    _I_END = _ix('一套放权与决策机制')
    _r1(_I_END, 'Agent 有 L0–L4，人有看过·用过·学过·干过', 'Agent 有 L1–L5，人有看过·用过·学过·干过')
    #       ⑩c 视觉终审顺手修：这一页四栏 + 图标带只填到 body 的 62%（全场最低），
    #       是唯一一处明显的留白失衡。整体上调一档撑到 ~80%（正文在位断言见下面 C15 段）。
    _cls(_I_END, 'r15end')

    # ── C15-⑩ 终检 · R14 留下的悬空计数词 ───────────────────────────────────
    #    R14 把 foot 从「逐个点名五轮」瘦身成一行来源名之后，note 里的「这五笔」
    #    在页面上再也数不出五笔（图上只挂了两翼那两笔）→ 改成「这几笔」。
    _r1(_I14, '2026 光是上半年这五笔', '2026 光是上半年这几笔')

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
    # ── C12 新页入列（承上面 C12 层）：PART 1 幕卡 _secs[5] 之后、钱页 _secs[6] 之前 ──
    #    45 → 46 页。插在这里而不是插在 C12 层里，是因为 _order 到这一行才装配完。
    assert _order[:7] == [0, 1, 2, 3, 4, 5, 6], f'C12 入列定位失败：{_order[:7]}'
    _order.insert(6, _I_FLOW)
s = _head2 + '\n'.join(_secs[o] for o in _order) + _tail2
_n_cut = 46 if V2 else 54
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
    CONF_CSS += C10_CSS     # C10 · R10 八页删改后逐页撑满（必须排在 C9 之后）
    CONF_CSS += C11_CSS     # C11 · R11 十三页删改与数据换血后逐页撑满（必须排在 C10 之后）
    CONF_CSS += C12_CSS     # C12 · R12 新页「钱的三次落点」页级档（必须排在 C11 之后）
    CONF_CSS += C13_CSS     # C13 · R13 七处内容修订页级档（必须排在 C12 之后：P5 字号回调靠后写者胜）
    CONF_CSS += C14_CSS     # C14 · R14 钱流向页双轴图页级档（必须排在 C12 之后：同页两个类，后写者胜）
    CONF_CSS += C15_CSS     # C15 · R15 终轮页级档（必须排在 C13 之后：.r13ask 那条要靠后写者胜盖回去）
# 插到最后一个 </style> 前（主样式表尾部）
li = s.rindex("</style>")
s = s[:li] + CONF_CSS + s[li:]

open(OUT, "w", encoding="utf-8").write(s)
n = len(re.findall(r'<section class="slide', s))
_n_out = 46 if V2 else 55
assert n == _n_out, f"{'R12 聚焦版' if V2 else '大会版'}应为 {_n_out} 页，实际 {n}"
print(f"{OUT.split('/')[-1]} written · {n} slides · {len(s)//1024}KB")
assert "deckRuler" in s and "noindex" in s
# 两版共用：多行 note clip-path 真 bug 修复必须在位
assert ".note>span.flow,.note>span.flow.rev,.note>.flow{display:inline-block;}" in s, "FIX_CSS 未装配"
# C2/C3 内容在位（防「定义了未装配」）
_MK = ["HUMAN IN THE LOOP", "Eval 第二课", "交叉验证 · 两个行业的断层",
       "本场提要</h2>", "四个互不相干的人，说了", "商业模式变迁", "人还在不在环里</em></h2>", "就是「按结果收钱」的计费口径",
       "四个阶段，四颗", "一个新的融合岗位", "一套放权与决策机制",
       "紫 = 已规模商业化", "金黄 = 强监管场景", "这条弧线不存在", "文本通道 · TEXT CHANNEL", "语音通道 · VOICE CHANNEL",
       'd="M675 6 V172"']
if not V2:
    # 陪伴章内容 + C1/C2 两张融合页（V2 已被 C8/C9 拆回母版原页，融合页定义保留但不装配）
    # + C10 · R10 在 V2 里删掉的两处：P45 Kevin Weil 引文卡署名
    _MK += ["不应该</em>被记住", "题之骗 × 粒度之骗", "单轮打分", "TWO FENCES", "OpenAI 前 CPO"]
for _mk in _MK:
    assert _mk in s, f"C2/C3/C4/C5 内容缺失：{_mk}"
assert ("Eval 第四课" in s) == V2, "课序：V2 应有第四课（听失败），55 页版不应有"
assert "暖橙 = 已规模商业化" not in s and "粉 = 强监管场景" not in s
# C6 内容在位 / 悬空引用清零
_MK6 = ["事前授权", "批动作类别，不批每一句话",
        "这六件事，第四幕会变成组织的授权语法" if V2 else "这六件事，第五幕会变成组织的授权语法",
        "把权放给 high agency 的人"]
if not V2:
    _MK6.append("《人和组织，必须一起转身》")   # C9 · R9 把 P43 的 2025 承接段整段删掉
    # C6 给 QoT 三卡起的短名 —— C10 · R10 在 V2 里把三卡换成了四条工程坐标
    _MK6 += ["边界 / BOUNDARY", "结果 / ACCOUNTABILITY", "可撤销 / RECOVERABILITY",
             "授权可撤销（随时降级、随时回滚）"]
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
    # ⚠️ R15 回归账（改动累计 15 轮后的第四次挪账）：C15-③ 把北极星页 note 整段删了，
    #    「下午 AIoT 专场整场拆开讲」「直接从「被托付」进」两句随之下台 —— 下午专场的交接
    #    改由分水岭页 eyebrow 与图注承担（下面两条），所以这两句从正向名单里摘出。
    #    C15-① 换了两张主标题，「这不是一个垂类」「预测还在打架」同理换成新主标题的锚点。
    for _mk in ("陪伴那条线走「熟人 → 伙伴」（下午专场）", "消费级 · 陪伴 —— 下午 AIoT 专场那条",
                "PART 2 · 被托付", "PART 3 · 双向奔赴", "PART 4 · 人与组织",
                "对话式 AI 的钱，<em>流向了哪里</em>", "<em>正在悄然发生</em>",
                "观点页 · 嘉宾金句 · 05", "前面三幕讲的是",
                "这道题第二、三幕来解",
                "--ink-3:#D9D9E3;", "--ink-2:#E8E8F0;", ".note{font-size:24px"):
        assert _mk in s, f"C8 内容缺失：{_mk}"
    for _mk in ("PART 5", "PART 2 · 被记住", "观点页 · 嘉宾金句 · 06", "恰好的那半秒", "gemini-demo.mp4",
                "class=\"vslide\"><", "值得被记住的存在", "本场第一处反共识", "第五幕", "上一幕",
                "--ink-3:#A5A5A5", "--ink-2:#c9c9d4"):
        assert _mk not in s, f"C8 残留未清：{_mk}"
    # 幕卡 rail 四站 / P5 路线四站（C8 删「被记住」六→五，C11 再删「PART 0 开场」五→四）
    assert s.count('<span>02 被托付</span>') + s.count('<span class="cur">02 被托付</span>') == 4
    assert '>02 被记住<' not in s, "C8：幕卡 rail 不应再有「02 被记住」站"
    #    y 值：C10-① 纵向 ×4.6 后是 368（原 y="80"），C13-② 字号回调时收拢到 468
    assert s.count('y="468" text-anchor="middle">PART') == 4, "C11 · P5 路线应为四站"
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
                # （R9 的 P33「这个坑有名字，叫 backchannel」note 已由 C11-⑫ 删掉）
                "You don’t pay for tokens", "business outcomes delivered",
                # （R9 的 P45 收场句「愿我们在理解 Agent 的同时」已由 C10-⑧ 撤成纯图收场）
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

    # ── C10 · R10 八页删改 ────────────────────────────────────────────────
    #    ⓐ 逐页负向断言：每张动刀页抽一句被删原文，必须查无此句
    for _mk in ("问题一 · 授权边界",                            # P5 · 三问卡整组
                "问题二 · 问责归属", "问题三 · 撤销机制",
                "它能替你做什么，到哪里为止", "收不回来的授权不叫授权",
                "这三个问题不是哲学问题",                       # P5 · note
                "整体一致率是被多数类稀释过的假象",              # P18 · 正确的看法 01
                "人抽检<b>理由</b>而不是结论",                   # P18 · 正确的看法 02
                "裁判自己也要有回归集",                          # P18 · 正确的看法 03
                "一笔约 36 亿美元的收购",                        # P22 · foot
                "不是成熟，只是乐观",                            # P27 · note
                "给产品团队的动作 · 先别问",                     # P27 · foot
                "separation of duties",                          # P29 · 英文引文块
                "某企业支付平台 CEO 与访谈者",
                "越权拒答率 · 策略遵守率",                       # P37 · 01 边界卡
                "审计覆盖率 · 决策可归因率",                     # P37 · 02 结果卡
                "撤销生效延迟 · 回滚成功率",                     # P37 · 03 可撤销卡
                "信任是被验证过的行动空间",                      # P37 · land
                "这三个维度对应四条工程坐标",                    # P37 · 坐标行文字版
                "四阶不是学历",                                  # P39 · land
                "愿我们在理解"):                                 # P45 · 结语
        # ⚠️ R13-③ 起「Writing evals…」不再列在这里：那句从 P45 撤走之后，
        #    R13 把它放回灵魂拷问页作第二拍（正向账在 C13 段里）。
        assert _mk not in s, f"C10 · R10 该删未删：{_mk}"
    #    终页仍必须是纯图收场：Weil 引文卡不许回到那一页（内容锚定，不点页号）
    assert 'Writing evals' not in s[s.index('尺子的两面'):], "C10 · 终页应仍是纯图收场"
    #    ⓑ 正向断言：三处重构与一处新增必须在位
    for _mk in ("身份可验", "VERIFIABLE", "行为可拦", "INTERCEPTABLE",
                "结果可追", "ACCOUNTABLE", "授权可撤销", "REVOCABLE",
                "「越界那句话，必须在说完之前被拦下」", "「随时降级、随时回滚」",
                '<div class="take qot4" data-step="4">', ".take.qot4 .c .who{font-size:50px",
                "你付的不是 token 的钱——是被交付出来的业务结果的钱。",
                'viewBox="0 320 1680 665"',        # P5 路线图纵向 ×4.6
                'viewBox="0 -177 1680 646"',       # P45 尺子纵向 ×1.7
                'viewBox="0 0 1680 495"',          # P18 两遍质检条纵向 ×1.5
                ".r10p5 .fig .txt{font-size:76px", ".r10p45 .fig .txt{font-size:28px"):
        assert _mk in s, f"C10 · R10 内容缺失：{_mk}"
    #    ⓒ 页级档位类必须全部挂上（八页一页一档）
    #    （R11 起同一页可能同时挂 C10 与 C11 两个档位类，所以按词边界找，不再比结尾的引号）
    for _c in ('r10p5', 'r10p18', 'r10p22', 'r10p27', 'r10p29', 'r10p37', 'r10p39', 'r10p45'):
        assert len(re.findall(rf'class="slide[^"]*\b{_c}\b', s)) == 1 and f'.{_c} ' in s, \
            f"C10 · 档位类未挂/未定义：{_c}"
    #    ⓓ QoS-QoE-QoI-QoT 顶部条必须原样留在页上（P5 路线图交给 C11 的四站断言）
    assert all(f'>{_q}</text>' in s for _q in ('QoS', 'QoE', 'QoI', 'QoT')), "C10 · QoT 顶部条缺失"

    # ── C11 · R11 十三页删改与数据换血 ─────────────────────────────────────
    #    ⓐ 逐页负向断言：每张动刀页抽一句被删原文，必须查无此句
    for _mk in ("当时我的结论是：活人感缺失",                     # P3 · 2025 那一栏结论
                "把它做得更像人",
                "他真正的愤怒不是「你不像人」",                   # P3 · 2026 那一栏结论
                "让它说清楚自己是谁、能替谁审批",
                ">OPENAPI</text>",                              # P4 · 协议名换 A2A
                "一张跑了 100 年的电话网", "加一张一百年的旧网",   # P4 · PSTN 年数
                'x="80" y="368" text-anchor="middle">PART 0',    # P5 · 开场站
                '>开场</text>',
                "美国青少年里，用过 AI 陪伴类产品的",             # P8 · 消费侧压缩
                "而遇到要紧事，宁可先说给 AI 听",
                "单次停留 14分17秒", "Common Sense Media",
                "四个方向的人得出了同一个结论",                   # P9 · 旧结论行
                "模型不再是瓶颈",
                "边界声明 · 本场不讨论意识",                      # P10 · foot
                "谁先行动 · 谁代表谁",
                '<div class="steps">',                           # P19 · 下方四块
                '<div class="i">STEP 01</div>', '<div class="i">STEP 04</div>',
                "抽样会先把长尾抽没，而长尾正是它翻车的地方。",
                "每一条失败都变成一道题，从此不许再错第二遍。",
                "96.5%</div><div class=\"l\">未被识破率",         # P21 · 三格
                "同等时间的有效工作量", "同等产出的用人成本",
                "这 2,475 通，是真实生产通话的自然测量",           # P21 · note
                # ⚠️「意向转化率」R11 时是负向断言（三格被删）；R13-⑤ 纠正表意之后，
                #    它是这一页两个大数共同的度量名，正向账在 C13 段里。
                "这个坑有名字，叫 backchannel",                   # P33 · note
                "它在我只说了一个",
                "任何一格的进步，四条线一起受益"):                 # P36 · note 长尾
        assert _mk not in s, f"C11 · R11 该删未删：{_mk}"
    #    ⓑ 正向断言：换血 / 重写 / 重构 / 对调必须在位
    for _mk in ('viewBox="0 0 1680 392"',                    # P3 波形纵向 ×2
                '>A2A</text>', '一张跑了 150 年的电话网',      # P4
                '贝尔 1876 年打出人类第一通电话，今年整 150 周年',
                # （四站首站的坐标账；y 由 C13-② 字号回调时 368 → 468）
                '<text class="lbl fill-am pop" style="--i:7" x="140" y="468" text-anchor="middle">PART 1</text>',
                # P8 · 企业侧新数据（每条都必须能在 SOURCE 行找到出处与年份）
                '>66%</text>', '>70%</text>', '>91%</text>', '>15–20%</text>', '>49%</text>',
                'Salesforce《State of Service: AI Agents Edition》2026-05（n=3,075',
                'Pew Research 2026-06（n=5,119）',
                'CC-CMM · 艾媒咨询 · 第一新声 2025',
                # P9 · 新结论（R15-① 把这句从 note 提上主标题，中间多了一层 <em>）
                '对话式智能体在企业服务侧，<em>已经到了规模化应用的阶段</em>', '硬性基础全部具备',
                # P19 · 四步并进图内
                '>STEP 01</text>', '>STEP 02</text>', '>STEP 03</text>', '>STEP 04</text>',
                '>全量捞，不抽样</text>', '>人耳听，不看文本</text>',
                '>归类，不打分</text>', '>固化成回归集</text>',
                'viewBox="0 0 1680 600"',
                # P21 · 双大数对比 + 基线口径标注（度量名与结论句由 R13-⑤ 纠正，见 C13 段）
                '<div class="cmp2">', '<div class="v">3.08%</div>', '<div class="v">1.5%</div>',
                '上线前人工基线 · 内部口径',
                # P22 · 出处行（一手：Sierra 官方博客）
                'Bret Taylor &amp; Clay Bavor · Sierra 官方博客《The next Horizon in agents》· 2026-07',
                '<div class="land r11pay flow"', '.r11pay .src{display:block',
                # P30 · 事件叙述沉底作注释行
                'class="old tail rise"', 'viewBox="0 0 1680 260"',
                # P36 · 只留一句
                '<b>四条产品线不是四个赛道，是同一个能力模型的四个切片。</b></div>'):
        assert _mk in s, f"C11 · R11 内容缺失：{_mk}"
    #    ⓒ P5 路线图 = 四站（PART 1-4），「PART 0 · 开场」整站撤走
    _p5b = s[s.index('<!-- 全场路线'):]; _p5b = _p5b[:_p5b.index('</svg>')]
    assert all(_t in _p5b for _t in ('语法变了', '被托付', '双向奔赴', '人与组织')), \
        "C11 · P5 路线图四站应完整保留"
    assert _p5b.count('text-anchor="middle">PART') == 4 and 'PART 0' not in _p5b, \
        "C11 · P5 路线应恰好四站且无 PART 0"
    #    （起点 x=627 与 --len:1010 是 C11 的账；y 由 C13-② 字号回调时 543 → 580）
    assert 'd="M627 580 H1600"' in _p5b and '--len:1010' in _p5b, "C11 · P5 高亮段起点/长度未同步"
    #    ⓓ P29 / P30 版面对调：图必须排在大数（P29）与三卡（P30）之前
    _p29 = s[s.index('人和 Agent 共事的协作关系'):]; _p29 = _p29[:_p29.index('</section>')]
    assert _p29.index('<div class="fig">') < _p29.index('<div class="g3">'), "C11 · P29 未对调"
    _p30 = s[s.index('两道围栏：提示词拦话术'):]; _p30 = _p30[:_p30.index('</section>')]
    assert _p30.index('<div class="fig">') < _p30.index('class="old tail'), "C11 · P30 未对调"
    assert _p30.rindex('class="old tail') > _p30.index('class="note co'), "C11 · P30 叙述未沉到最底部"
    #    ⓔ 页级档位类必须全部挂上（十三页里十二页一页一档；P22 走 .r11pay 共享档）
    for _c in ('r11p3', 'r11p5', 'r11p8', 'r11p9', 'r11p10', 'r11p19', 'r11p21',
               'r11p29', 'r11p30', 'r11p33', 'r11p36'):
        assert len(re.findall(rf'class="slide[^"]*\b{_c}\b', s)) == 1 and f'.{_c} ' in s, \
            f"C11 · 档位类未挂/未定义：{_c}"

    # ── C12 · R12 新页「钱的三次落点」在位 ─────────────────────────────────
    #    ⓐ 页级档挂上 + CSS 有定义；整页恰好一份
    assert len(re.findall(r'class="slide[^"]*\br12flow\b', s)) == 1 and '.r12flow ' in s, \
        "C12 · 新页档位类未挂/未定义：r12flow"
    _pf = s[re.search(r'class="slide[^"]*\br12flow\b', s).start():]; _pf = _pf[:_pf.index('</section>')]
    #    ⓑ eyebrow 必须是 Colin 那句原话（逐字）
    assert '产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走' in _pf, "C12 · eyebrow 原话缺失"
    assert '近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>' in _pf, "C12 · h2 缺失"
    #    ⓒ 三条线的名与数齐全（C14 已把三条层带重做成双轴时间图：$2B ARR 下轴、≈$2.2B 改 $2.2B+，
    #       英文层名与「带宽示意」的说法一并撤掉 —— 逐条正向账搬到下面的 C14 段）
    for _b in ('>基础模型</text>', '>AI 写代码</text>', '>对话式 AI</text>',
               '>$31.4B</text>', '>$88.9B</text>', '>$178B</text>',
               '>$1.6B</text>', '>$3.3B</text>',
               '>$2.1B</text>', '>&#8776;$0.7B</text>', '>$2.2B+</text>'):
        assert _pf.count(_b) == 1, f"C12 · 页上层名/数缺失或重复：{_b}"
    assert _pf.count('class="stroke-am pkt"') == 1, "C12 · 对话式那条的走线光点缺失"
    #    ⓓ 大泛类两翼（消费声音 / 企业智能体）点名在页上
    for _w in ('ElevenLabs $500M @ $11B', '消费声音侧', 'Sierra $950M @ $15B', '企业智能体侧'):
        assert _w in _pf, f"C12 · 两翼标注缺失：{_w}"
    #    ⓔ 来源行在位（C14 已瘦身成一行，逐条来源账见下面的 C14 段）
    assert '<div class="foot flow rev" style="--i:9">Source · ' in _pf, "C12 · 来源行缺失"
    #    ⓕ data-step ≤ 2
    _st12 = set(re.findall(r'data-step="(\d+)"', _pf))
    assert _st12 <= {'1', '2'}, f"C12 · data-step 应 ≤2，实际 {_st12}"
    #    ⓖ 新页必须紧跟 PART 1 幕卡、排在钱页之前；钱页 eyebrow 已换成衔接句
    _i_act1 = s.index('<div class="cn spread" style="--i:3">语法变了</div>')
    _i_flow = re.search(r'class="slide[^"]*\br12flow\b', s).start()
    # （锚点随 C15-① 改主标题一并换成新 h2；eyebrow 也在 R15 精简过，断言同步改判）
    _i_money = s.index('对话式 AI 的钱，<em>流向了哪里</em>')
    assert _i_act1 < _i_flow < _i_money, "C12 · 新页应排在 PART 1 幕卡之后、钱页之前"
    assert '先看钱往哪儿去了' not in s, "C12 · 钱页 eyebrow 未换成衔接句"
    assert '<div class="eyebrow flow" style="--i:0">承上页，再往里看一层</div>' in s, "C12 · 钱页新 eyebrow 缺失"

    # ── C13 · R13 七处内容修订 ─────────────────────────────────────────────
    #    全部用内容锚定取页（Colin 的反馈横跨 45/46 两个页码版，不信页号）
    def _sec_of(anchor):
        """按页上一句原话取出它所在的整个 <section>（锚点必须唯一）。"""
        assert s.count(anchor) == 1, f"C13 · 取页锚点不唯一：{anchor[:40]}"
        _a = s.rindex('<section class="slide', 0, s.index(anchor))
        return s[_a:s.index('</section>', _a) + len('</section>')]
    #    ⓐ 负向：被换下 / 被改写的六句必须查无此句
    for _mk in ('B 如 Boy',                                        # ④ 中式直译拼读法
                '<div class="l">被识破率</div>',                    # ⑤ R11 的误标
                '被投诉「不像人」基线', '通话结束前，被对方听出「这是 AI」的比例',
                '它已经贴到人工坐席自己的极限上了。',                 # ⑤ 旧结论（「逼近人」向）
                '一个能被计量的同事，', '计量不是为了管住它，是为了敢把事交给它。',   # ⑥ 被换下的金句
                '提示词只能拦住一些越权，', '架构的围栏，才是产品经理的护城河。',     # ⑦ 被换下的金句
                '你能拦住的，只有你先表示出来的那些东西。'):
        assert _mk not in s, f"C13 · R13 该改未改：{_mk}"

    #    ⓑ ① 贝尔第一通电话：原话 + 出处行必须挂在 P4 那一页（内容锚定取页）
    _p4 = _sec_of('今年这段通话里，一个人都没有')
    for _mk in ('&#8220;Mr. Watson — come here — I want to see you.&#8221;',
                '贝尔 · 1876 · 人类第一通电话，今年整 150 年',
                '<div class="qstack">', 'PSTN · 一张跑了 150 年的电话网'):
        assert _mk in _p4, f"C13-① 贝尔引文缺失：{_mk}"
    assert _p4.count('<div class="quote') == 2, "C13-① P4 左栏应是两条引文的一摞"

    #    ⓒ ② 路线图字号回调：档位类在位 + 四组回调值 + 圆点/线宽同步回收
    for _mk in ('.r13p5 .fig .txt{font-size:46px;}', '.r13p5 .fig .lbl{font-size:24px',
                '.r13p5 .fig .sm{font-size:25px;}'):
        assert _mk in s, f"C13-② 路线图回调值缺失：{_mk}"
    assert '.r11p5 .fig .txt{font-size:82px' in s and s.index('.r11p5 .fig .txt') < s.index('.r13p5 .fig .txt'), \
        "C13-② 回调档必须排在 C11 的 82px 之后（后写者胜）"
    _p5c = s[s.index('<!-- 全场路线'):]; _p5c = _p5c[:_p5c.index('</svg>')]
    assert 'r="11"' in _p5c and _p5c.count('r="10"') == 3 and 'stroke-width="3.5"' in _p5c, \
        "C13-② 圆点半径未回收"
    assert 'stroke-width="2" d="M140 580 H1600"' in _p5c and 'stroke-width="4" d="M627 580 H1600"' in _p5c, \
        "C13-② 线宽未回收"
    assert _p5c.count('y="746"') == 4 and _p5c.count('y="856"') == 4, "C13-② 四行 y 未收拢"

    #    ⓓ ③ Weil 金句 —— ⚠️ R15-⑦ 改判：C13 把它加成灵魂拷问页的第二拍，
    #       C15 把它整张搬到金句 02，拷问页回到纯问句全页大字。这里只守「全场仅一处」，
    #       落点的正向账搬到下面的 C15 段。
    _pask = _sec_of('亲手写过')
    assert 'Writing evals' not in _pask and 'Kevin Weil' not in _pask, \
        "C15-⑦ 灵魂拷问页应已撤回 Weil 第二拍"
    assert 'data-step' not in _pask, "C15-⑦ 灵魂拷问页应是纯问句全页大字（无第二拍）"
    assert s.count('Writing evals is the most important') == 1, "C13-③ Weil 金句应全场只此一处"

    #    ⓔ ④ 英语习惯拼读法：svg 与 note 两处都改到
    _pev = _sec_of('你的 demo 在骗你</h2>')
    assert 'A as in Apple · B as in Boy · 0086 · 一位一位念' in _pev, "C13-④ svg 行未改"
    assert '在「A as in Apple、0086」上<b>全崩</b>' in _pev, "C13-④ 关联句未同步"

    #    ⓕ ⑤ 3.08% 表意纠正：两个数同为意向转化率，主句转向「已经强过人」
    _pc2 = _sec_of('一个 Agent 的入职三十天')
    assert _pc2.count('<div class="l">意向转化率</div>') == 2, "C13-⑤ 两个数的度量名应同为意向转化率"
    assert '<div class="v">3.08%</div>' in _pc2 and '<div class="v">1.5%</div>' in _pc2
    assert '上线前人工基线 · 内部口径' in _pc2, "C13-⑤ 1.5% 的口径标注应保留"
    assert '它已经把人工基线翻了一倍。' in _pc2, "C13-⑤ 新主句缺失"
    #       视觉方向：Agent 那条更长（100%）且走 amber，人工那条 49%
    assert '<div class="bar"><i style="width:100%"></i></div>' in _pc2 \
       and '<div class="bar"><i style="width:49%"></i></div>' in _pc2, "C13-⑤ 比例条缺失"
    assert _pc2.index('width:100%') < _pc2.index('width:49%'), "C13-⑤ Agent 条应排在人工条之前（更长）"
    assert '.cmp2 .c.am .bar i{background:var(--amber);}' in s, "C13-⑤ Agent 条 amber 强调未定义"

    #    ⓖ ⑥ Bret Taylor「perfect human」金句页：英文为主 + 中文一行 + 署名行
    _pmq = _sec_of('One of the biggest fallacies in AI')
    for _mk in ('is people compare it with this perfect human', 'that does not exist.&#8221;',
                'AI 最大的谬误之一，是人们总把它跟一个并不存在的完美的人相比。',
                'Bret Taylor · Sierra CEO / OpenAI 董事长'):
        assert _mk in _pmq, f"C13-⑥ 金句页元素缺失：{_mk}"
    assert '观点页 · 嘉宾金句 · 03' in _pmq, "C13-⑥ 金句编号应仍是 03（页数与编号都不变）"

    #    ⓗ ⑦ 围栏 Part 点睛：新金句在位，且仍挂在金句 04 上
    _pfc = _sec_of('围栏不是拦住它，')
    for _mk in ('是放出它。</i>',
                '提示词 + 产品架构，围出一条不用人扶的执行流——围栏有多硬，敢交给它的 OKR 就有多重。'):
        assert _mk in _pfc, f"C13-⑦ 新金句元素缺失：{_mk}"
    assert '观点页 · 嘉宾金句 · 04' in _pfc, "C13-⑦ 应仍是金句 04"

    #    ⓘ 页级档位类必须全部挂上且 CSS 有定义（r13ask 已随 C15-⑦ 撤回第二拍一并摘掉）
    assert 'class="slide' in s and not re.search(r'class="slide[^"]*\br13ask\b', s), \
        "C15-⑦ r13ask 档位类应已随第二拍一并摘除"
    for _c in ('r13bell', 'r13p5', 'r13case', 'r13mq', 'r13fence'):
        assert len(re.findall(rf'class="slide[^"]*\b{_c}\b', s)) == 1 and f'.{_c} ' in s, \
            f"C13 · 档位类未挂/未定义：{_c}"
    #    ⓙ 页数不变 46（最终页数断言在写盘处，这里只守金句编号 01–05 不变）
    assert s.count('观点页 · 嘉宾金句 · 05') == 1 and '观点页 · 嘉宾金句 · 06' not in s, \
        "C13 · 金句编号应仍是 01–05"

    # ── C14 · R14 两处 ─────────────────────────────────────────────────────
    #    ① P2 讲台在 / 舞台零（正文范围内；母版的 CSS 注释「固定舞台」不在页里，不受影响）
    _pp2 = _sec_of('第三次，站上同一个讲台')
    assert '舞台' not in _pp2, "C14-① P2 仍有「舞台」残留"
    assert '回到讲台' in _pp2, "C14-① P2 eyebrow「回到讲台」丢了"
    assert '第三次，站上同一个舞台' not in s, "C14-① 全场不应再有「站上同一个舞台」"
    _n_slide_stage = sum(1 for _x in re.findall(r'<section class="slide.*?</section>', s, re.S) if '舞台' in _x)
    assert _n_slide_stage == 0, f"C14-① 仍有 {_n_slide_stage} 页正文含「舞台」"

    #    ② 钱流向页 · 双轴时间图
    _pm = _sec_of('近三年，钱的三次落点')
    assert len(re.findall(r'class="slide[^"]*\br14money\b', s)) == 1 and '.r14money ' in s, \
        "C14-② 档位类未挂/未定义：r14money"
    #       ⓐ 双轴骨架：两条轴 + 一套共用网格 + 基线；左右轴标 mono 小字
    assert 'd="M230 120 V470 M1200 120 V470"' in _pm, "C14-② 左右两条轴缺失"
    assert _pm.count('class="gd"') == 1 and _pm.count('class="axb"') == 1, "C14-② 网格/基线缺失"
    assert '>基础模型 $B</text>' in _pm, "C14-② 左轴标缺失"
    assert '>Coding / 对话式 $B</text>' in _pm, "C14-② 右轴标缺失"
    #       ⓑ 左轴刻度 0/50/100/150/200 · 右轴刻度 0/1/2/3/4（两套落在同五条网格线上）
    for _t in ('x="212" y="127" text-anchor="end">200<', 'x="212" y="477" text-anchor="end">0<',
               'x="1218" y="127">4<', 'x="1218" y="477">0<'):
        assert _t in _pm, f"C14-② 轴刻度缺失：{_t}"
    #       ⓒ X 轴三刻度 + 2026「至今」+ 双轴量级小注
    for _t in ('class="lbl yr" x="300" y="508"', 'class="lbl yr" x="720" y="508"',
               'class="lbl yr" x="1140" y="508"', 'x="1140" y="538" text-anchor="middle">至今</text>',
               '左右两轴量级不同 · 左轴 0–200，右轴 0–4（$B）'):
        assert _t in _pm, f"C14-② X 轴/小注缺失：{_t}"
    #       ⓓ 三条数据线各一条：基础模型（白粗）· Coding（灰细）· 对话式（amber 粗 + 光点）
    assert _pm.count('class="ln fnd dw"') == 1 and _pm.count('class="ln cod dw"') == 1 \
       and _pm.count('class="ln cnv dw"') == 1, "C14-② 三条曲线应各一条"
    assert _pm.count('class="stroke-am pkt"') == 1, "C14-② 对话式曲线的走线光点缺失"
    #          Coding 那条只到 2025（第三点不画、虚线也不补），ARR 绝不上融资轴
    assert _pm.count('class="ln cod dw" style="--len:490;--i:6" d="M300 330 C 440 322 580 210 720 181"') == 1, \
        "C14-② Coding 曲线必须止于 2025（x=720）"
    assert 'stroke-dasharray' not in _pm, "C14-② 不许有虚线（ARR 不能被画成第三个融资点）"
    assert '$2B ARR' not in _pm and '2026 转向收入兑现 · Cursor ARR $2B' in _pm, \
        "C14-② Cursor ARR 只能作末端小注，不能当轴上的数"
    #       ⓔ 面积：对话式曲线下的 amber 低透明度渐变（强调「正在灌进来」）
    assert 'fill="url(#r14conv)"' in _pm and 'id="r14conv"' in _pm, "C14-② 对话式曲线下的渐变面积缺失"
    assert '.r14money #r14conv .g0{stop-color:var(--amber);stop-opacity:.22;}' in s, "C14-② 渐变档未定义"
    #       ⓕ 三条曲线各自终点挂名牌（+ 两条引线）；两翼小标挂在 2026 点旁
    for _t in ('x="1262" y="150">基础模型</text>', 'x="1262" y="196">$178B</text>',
               'x="750" y="154">AI 写代码</text>', 'x="891" y="154">$3.3B</text>',
               'x="1262" y="270">对话式 AI</text>', 'x="1262" y="316">$2.2B+</text>'):
        assert _t in _pm, f"C14-② 终点名牌缺失：{_t}"
    assert _pm.count('class="lead fnd pop"') == 1 and _pm.count('class="lead cnv pop"') == 1, \
        "C14-② 名牌引线缺失"
    assert _pm.count('class="sm wing pop"') == 2, "C14-② 2026 点旁应挂两翼小标"
    #       ⓖ 值标只在起点/拐点/终点（终点走名牌），不是每点都挂数字：图内值标恰好五个
    _n_val = _pm.count('class="txt val')
    assert _n_val == 5, f"C14-② 值标应恰好五个（三条线的非终点值），实际 {_n_val}"
    #       ⓗ 三条层带的旧图元必须清零（英文层名 / 三段带 / 带宽示意）
    for _old in ('>FOUNDATION MODELS</text>', '>CODING</text>', '>CONVERSATIONAL AI</text>',
                 'class="stroke dw"', 'class="stroke-am dw"', '>$2B ARR</text>', '>&#8776;$2.2B</text>',
                 '同一层的两翼'):
        assert _old not in _pm, f"C14-② 三条层带旧图元未清：{_old}"
    #       ⓘ foot 瘦身成一行；旧的长口径行全文清零（已移入设计文档 R14 段留档）
    assert '<div class="foot flow rev" style="--i:9">Source · Crunchbase · CB Insights《State of AI 2025》' \
           '· TechCrunch · Bloomberg · CNBC</div>' in _pm, "C14-② 新 foot 一行未落地"
    for _old in ('New Market Pitch 2026-07', 'PYMNTS 2025-06', 'SiliconANGLE 2026-05',
                 'Newcomer 2026-02', 'Crunchbase 2026-04', 'CB Insights《State of AI 2025》2026-01',
                 '本页自算，不是全类别口径', '带宽为量级示意，非等比', 'Cartesia $100M', 'Parloa $350M'):
        assert _old not in s, f"C14-② 旧长 foot 口径未撤下：{_old}"
    #       ⓙ eyebrow / h2 / note 三样原样保留
    for _keep in ('产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走',
                  '近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>',
                  '这笔钱在这一层内部又分给了谁——下一页拆开看。'):
        assert _keep in _pm, f"C14-② 该保留的没保住：{_keep}"
    #       ⓚ data-step 仍 ≤2（对话式整组第二拍，note 第三拍）
    assert set(re.findall(r'data-step="(\d+)"', _pm)) <= {'1', '2'}, "C14-② data-step 应 ≤2"

    # ── C15 · R15 终轮十项 ─────────────────────────────────────────────────
    #    ⓐ 负向：被换下 / 被删掉的整段必须查无此句
    for _mk in ('这不是一个垂类',                                   # ①a 旧 h2
                '钱到了对话式 AI，再往里看一层：它分给了谁',           # ①a 旧 eyebrow
                '预测还在打架',                                     # ①b 旧 h2
                '四个互不相干的人，说了<em>同一件事</em>',            # ①c 旧 h2（降回 eyebrow，无 em）
                '所有的路，最后都汇到「对话」这条线上',               # ①c 旧 eyebrow
                '>Conversational AI</text>',                        # ② 旧英文标
                '可这三年里，一直是我们单方面朝它走',                 # ③b 北极星页 note 第一句
                '是三年里最常见的<b>错位</b>',                       # ③b note 第二句
                '下午 AIoT 专场整场拆开讲',                          # ③b note 第三句
                '被记住，靠的是一致性。被托付，靠的是可验证。',        # ④ 旧幕卡金句
                '这四级换的不是它的能力',                            # ⑤ 分水岭 land
                '那把越来越硬的尺子',
                '给产品经理的动作 · 把你 demo 里最得意的那三条',       # ⑥ Eval 一课 foot
                '你以为在选模型，', '其实在选评测。',                  # ⑦ 被换下的金句 02
                '模型半年换一次，评测集用三年',
                'L0 · 旁听', 'L1 · 起草', 'L2 · 只读应答', 'L3 · 可执行', 'L4 · 主动外呼',  # ⑧ 旧梯级
                '压在 <em>L2 与 L3 之间</em>', '今年整体重心：L2 与 L3 之间',              # ⑨a 旧重心
                '>L4 主动<', '>L0–L1<', 'Autonomy L4',                                   # ⑨a/b
                '语音场景的 L2 门槛', 'Agent 有 L0–L4',                                   # ⑨c/d
                '2026 光是上半年这五笔'):                            # ⑩a 悬空计数词
        assert _mk not in s, f"C15 · R15 该删/该改未落地：{_mk}"

    #    ⓑ ① 三个新主标题在位（各自那一页里）
    _p8n = _sec_of('对话式 AI 的钱，<em>流向了哪里</em>')
    assert '承上页，再往里看一层' in _p8n and 'ElevenLabs · 语音合成' in _p8n, "C15-①a 钱分布页错位"
    _p9n = _sec_of('对话式智能体的采购，<em>正在悄然发生</em>')
    assert '企业侧 · 这四个数都已经发生' in _p9n and '至于预测？同一年的两份报告还在打架' in _p9n, \
        "C15-①b 渗透页错位（「预测打架」的对照仍须留在 note 里）"
    _p10n = _sec_of('对话式智能体在企业服务侧，<em>已经到了规模化应用的阶段</em>')
    assert '<div class="eyebrow flow" style="--i:0">四个互不相干的人，说了同一件事</div>' in _p10n, \
        "C15-①c 原 h2 应降回 eyebrow"
    assert '四个方向的人，指向同一个判断：智能够用、部署可做、扩散周期已经开始、' \
           '周边那圈软件也补齐了，<b>硬性基础全部具备</b>。' in _p10n, "C15-①c 结论行未按现文保留"
    #    ⓒ ② 中心块英文标
    assert '>CONVOAI AGENT</text>' in _p10n and s.count('>CONVOAI AGENT</text>') == 1, "C15-② 英文标未落地"

    #    ⓓ ③ 北极星逐列对齐 + note 清零
    _pns = _sec_of('四个阶段，四颗<em>北极星</em>')
    assert '<div class="note"' not in _pns and '<div class="nstar">' in _pns, "C15-③b note 未整段删"
    #       四级的水平段 = .nstar 四列的完整跨度（1fr×4 + gap:26 @ body 1680 → 列宽 400.5）
    for _t in ('d="M0 443 H400.5"', 'd="M400.5 443 L426.5 356 H827"',
               'd="M827 356 L853 270 H1253.5"', 'd="M1253.5 270 L1279.5 184 H1680"'):
        assert _t in _pns, f"C15-③a 阶梯未落到列位：{_t}"
    #       文字 x 落在列左沿（svg 文字与下方 nstar 文字共用一条左边线）
    for _x in ('x="0" y="384"', 'x="426.5" y="298"', 'x="853" y="212"', 'x="1279.5" y="125"'):
        assert _x in _pns, f"C15-③a 级名未落到列左沿：{_x}"
    #       --len 配套（斜梁 ≈91 + 水平段 400.5 ≈ 491 → 500；首级 400.5 → 410）
    assert '--len:410;--i:0' in _pns and _pns.count('--len:500') == 3, "C15-③a --len 未配套"
    assert 'd="M1266.5 43 V486"' in _pns, "C15-③a 主语易位虚线未落到三/四列之间的空档正中"
    assert len(re.findall(r'class="slide[^"]*\br15nstar\b', s)) == 1 and '.r15nstar ' in s, \
        "C15-③ 档位类未挂/未定义：r15nstar"

    #    ⓔ ④ PART 2 幕卡新金句（Agent＝代理人的双关反转）+ 本幕导航保留
    _pa2 = _sec_of('<div class="cn spread" style="--i:3">被托付</div>')
    assert '我们叫了它三年 Agent（代理人）——今天，它终于开始代理了。' in _pa2, "C15-④ 幕卡金句未落地"
    assert '这一幕只讲一件事：那把尺子怎么造。' in _pa2, "C15-④ 本幕导航不该被动"

    #    ⓕ ⑤⑥ 两处删段 + 档位类
    _pld = _sec_of('工具 → 实习生 → 外包 → 专家 → <em>合伙人</em>')
    assert '<div class="land' not in _pld and '<div class="g4">' in _pld, "C15-⑤ land 未整段删"
    _pe1 = _sec_of('你的 demo 在骗你</h2>')
    assert '<div class="foot' not in _pe1 and '你的 demo 里全是前一种题' in _pe1, "C15-⑥ foot 未整句删"
    for _c in ('r15ladder', 'r15eval1'):
        assert len(re.findall(rf'class="slide[^"]*\b{_c}\b', s)) == 1 and f'.{_c} ' in s, \
            f"C15 · 档位类未挂/未定义：{_c}"

    #    ⓖ ⑦ Weil 只在金句 02（体例：英文两行 + 中文一行 + 署名行）
    _pw = _sec_of('Writing evals is the most important')
    for _mk in ('观点页 · 嘉宾金句 · 02', 'thing a PM can do in the AI era.&#8221;',
                '写评测，是 AI 时代一个产品经理能做的最重要的事。', 'Kevin Weil · OpenAI 前 CPO'):
        assert _mk in _pw, f"C15-⑦ 金句 02 元素缺失：{_mk}"
    #       「全场仅一处」只数正文（C15_CSS 里那行档位注释也写了 Kevin Weil，不算页内容）
    _slides_txt = ''.join(re.findall(r'<section class="slide.*?</section>', s, re.S))
    assert _slides_txt.count('Kevin Weil') == 1, "C15-⑦ 全场 Weil 应仅金句页一处"
    assert len(re.findall(r'class="slide[^"]*\br15mq\b', s)) == 1 and '.r15mq ' in s, \
        "C15-⑦ 档位类未挂/未定义：r15mq"

    #    ⓗ ⑧⑨ L 记号全 deck 一致性自检（三处互证）
    _pl = _sec_of('每一级之间隔着的不是技术，是<em>人还在不在环里</em>')
    for _t in ('L1 · 旁听', 'L2 · 起草', 'L3 · 只读应答', 'L4 · 可执行', 'L5 · 主动外呼'):
        assert _t in _pl, f"C15-⑧ 新梯级缺失：{_t}"
    #       BIG JUMP 不动位置：竖虚线 x=675 仍夹在「起草」(340–640) 与「只读应答」(710–1010) 之间
    #       → 重编后天然 = L2→L3，与自动驾驶「L2 辅助驾驶 → L3 系统担责」完全对齐
    assert 'd="M675 45 V509"' in _pl and '撤掉「人」这张安全网' in _pl, "C15-⑧ BIG JUMP 位置被动了"
    assert _pl.index('L2 · 起草') < _pl.index('撤掉「人」这张安全网') < _pl.index('L3 · 只读应答'), \
        "C15-⑧ BIG JUMP 应仍夹在 L2 与 L3 之间"
    #       交叉验证条带一个字不用改就自洽（自动驾驶 / 支付 Agent 两行的分段标注）
    for _t in ('自动驾驶 L1–L5', 'L1–L2 · 辅助驾驶，人不敢离环', 'L3–L5 · 系统担责，卡了十年的一跳',
               '支付 Agent 五级', 'L1–L2 · 行业还在边缘徘徊', 'L3–L5 · 还没人真正到达'):
        assert _t in _pl, f"C15-⑧ 交叉验证条带被误伤：{_t}"
    #       岗位散点页：h2 重心 = L3 与 L4 之间，纵轴四档同步，重心带标注同步
    _pj = _sec_of('真实岗位放上梯子')
    for _t in ('压在 <em>L3 与 L4 之间</em>', '>L5 主动<', '>L4 可执行<', '>L3 只读应答<', '>L1–L2<',
               '今年整体重心：L3 与 L4 之间'):
        assert _t in _pj, f"C15-⑨a 岗位散点页 L 记号未同步：{_t}"
    #       其余三处
    assert 'Autonomy L5' in _sec_of('一个 Agent 的入职三十天'), "C15-⑨b 案例 02 未同步"
    assert '语音场景的 L3 门槛，比文本高一级' in _sec_of('执行的围栏：语音的动作，'), "C15-⑨c 执行围栏未同步"
    assert 'Agent 有 L1–L5，人有看过·用过·学过·干过' in _sec_of('一套放权与决策机制'), "C15-⑨d 收束页未同步"
    #       全 deck 语义自检：正文里再无 L0，且梯子/重心/BIG JUMP 三处互证
    assert 'L0' not in _slides_txt, "C15-⑨ 全 deck 正文不应再有 L0"

    #    ⓘ ⑩ 终检：悬空计数词改判 + 幕序/课序/金句序仍自洽
    assert '2026 光是上半年这几笔' in _pm, "C15-⑩a「这几笔」未落地"
    assert s.count('观点页 · 嘉宾金句 · 0') == 5, "C15-⑩b 金句仍应是 01–05 五张"
    for _c in '一二三四':
        assert f'>Eval 第{_c}课</div>' in s, f"C15-⑩b 课序缺失：第{_c}课"

    print("ruler ✓ noindex ✓ C2/C3 content ✓ C8 R8v1 ✓ C9 R9 45p ✓ C10 R10 八页 ✓ "
          "C11 R11 十三页 ✓ C12 R12 新页 46p ✓ C13 R13 七处 ✓ C14 R14 讲台+双轴图 ✓ "
          "C15 R15 终轮十项 ✓")
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
