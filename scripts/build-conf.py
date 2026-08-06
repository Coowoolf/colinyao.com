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

# ── C16 · R16 的页级档 ·只在 CONF_V2=1 装配 ───────────────────────────────────
#    三档：两张金句页的「中上英下」体例（.r16mq2 / .r16mq3）+ 钱流向页的三格小倍数
#    （.r16money）。全部排在 C15_CSS 之后 —— 金句两页仍挂着 .r13mq / .r15mq（本仓
#    的既定做法是旧档留在原位、新档靠**后写者胜**盖过去，见 C14 对 .r12flow 的处理），
#    所以 .r16mq* 与 .r13mq/.r15mq 同为三类选择器时，靠源码顺序赢。
C16_CSS = """
/* ============ C16 · R16 · 两张金句页中上英下 + 钱流向页三格小倍数 ============ */
/* 金句 02/03：本场对象是中文听众 —— 中文回到 .mq .q 的中文金句字号体系（80px/900），
   英文原句降为下方一行 mono 补充（保留 mono 质感，但不再是主角）。
   ⚠️ .r13mq / .r15mq 把 .q 定成过 mono 52/54px，这两条必须在这里显式盖回中文体系，
      font-family 与 font-size 一个都不能漏（只盖 size 会留下 mono 的中文回退字形）。 */
.r16mq2 .mq .q,.r16mq3 .mq .q{font-family:var(--f-cn);font-size:80px;font-weight:900;
  line-height:1.28;letter-spacing:-.018em;color:var(--mq);}
.r16mq2 .mq .en,.r16mq3 .mq .en{font-family:var(--f-mono);font-size:30px;font-weight:700;
  line-height:1.5;letter-spacing:0;color:var(--mq-2);max-width:1420px;}
.r16mq2 .mq .s,.r16mq3 .mq .s{font-family:var(--f-mono);font-size:22px;letter-spacing:.14em;}
/* 出处行：署名行下面再挂一行（Cheeky Pint 集数 + 时间戳），比署名再低一档、贴紧它。
   .mq 的 gap 是 36px，所以用负 margin 把这一行收到署名行脚下。 */
.r16mq3 .mq .s.src{font-size:19px;letter-spacing:.12em;opacity:.68;margin-top:-24px;}

/* 钱流向页 · 三格小倍数（R14 的双轴时间图整张作废）。
   为什么弃双轴：左 0–200 / 右 0–4 两把尺并置，把 $3.3B 画得比 $178B 还高 ——
   dataviz 的头号 anti-pattern（两套刻度的对齐是任意的，图会凭空造出一个相关性）。
   改法是它给的标准解：**三格小倍数，各用各的 y 尺，共享 x**，量级差写在图上明说。
   一格 = 一条赛道：柱高只在格内可比，跨格比的是形状，不是高度。 */
.r16money .fig .lbl{font-size:19px;letter-spacing:.12em;}
.r16money .fig .lbl.yr{font-size:24px;letter-spacing:.16em;fill:var(--ink-2);text-transform:none;}
.r16money .fig .ttl{font-size:30px;}
.r16money .fig .txt.val{font-size:22px;font-weight:500;fill:var(--ink-2);}
.r16money .fig .txt.val.fill-am{fill:var(--amber);}
.r16money .fig .sm{font-size:18px;}
.r16money .fig .sm.anno{font-size:19px;fill:var(--ink-2);}
.r16money .fig .sm.anno.fill-am{fill:var(--amber);}
.r16money .fig .big{font-size:40px;fill:var(--ink);}
.r16money .fig .big.fill-am{fill:var(--amber);}
.r16money .note{font-size:22px;}
.r16money .foot{font-size:18px;}
/* 每格的表头分隔线与基线：退到 hair 两档，安静（数据柱是这一页唯一响的东西）。 */
.r16money .fig .pr{stroke:var(--hair);stroke-width:1;fill:none;}
.r16money .fig .axb{stroke:var(--hair-strong);stroke-width:1;fill:none;}
/* 数据柱 = 一条 96px 粗的竖直 .dw 描边：入场时从基线长上来，--len 与柱高逐条同步。
   格内配色走 dataviz 的 emphasis 规则 —— 落点年（该赛道钱砸得最狠的那一年）用本格
   的主色，其余年份同色降到 .34 的一档明度，绝不另生一个色相。
   三格主色本身是叙事阶梯：白（模型，最大头）→ 灰（写代码，已收尾）→ amber（对话，正在发）。 */
.r16money .fig .col{fill:none;stroke-width:96;stroke-linecap:butt;}
.r16money .fig .col.fnd{stroke:var(--ink);}
.r16money .fig .col.cod{stroke:var(--ink-3);}
.r16money .fig .col.cnv{stroke:var(--amber);}
.r16money .fig .col.dim{opacity:.34;}
"""

# ── C17 · R17 的页级档 ·只在 CONF_V2=1 装配 ───────────────────────────────────
#    R17 是一轮**熵减**：十二处里九处是纯删文，删完必须逐页撑满，所以这一层几乎全是
#    「删后放大」的档位。全部排在 C16_CSS 之后（.r16money / .r15end 等同页档靠后写者胜）。
C17_CSS = """
/* ============ C17 · R17 · 九处删文后的逐页撑满 + 两处版式 ============ */
/* P7 钱流向页：note 整段删（Sierra 未收录那层意思改由口播承担），三格图接管整个 body。 */
.r17money .head{margin-bottom:30px;}
.r17money .body{gap:30px;}
.r17money .fig{align-items:stretch;}
.r17money .fig svg{width:100%;height:auto;}
.r17money .fig .ttl{font-size:34px;}
.r17money .fig .big{font-size:46px;}
.r17money .fig .txt.val{font-size:25px;}
.r17money .fig .lbl.yr{font-size:27px;}
.r17money .fig .sm{font-size:20px;}
.r17money .fig .sm.anno{font-size:21px;}

/* P8 六卡页：国内存量 note + foot 双删，六张卡接管整页 —— 大数与描述各上一档。 */
.r17p8 .head{margin-bottom:32px;}
.r17p8 .g3{gap:26px;}
.r17p8 .card .tag{font-size:19px;}
.r17p8 .card .n{font-size:78px;}
.r17p8 .card .t{font-size:25px;}
.r17p8 .card .d{font-size:22px;line-height:1.6;}

/* P9 渗透页：预测对照 note 删 + foot 瘦成机构名，五条读数图纵向接管整页。 */
.r17p9 .head{margin-bottom:32px;}
.r17p9 .body{gap:28px;}
.r17p9 .fig{align-items:stretch;}
.r17p9 .fig svg{width:100%;height:auto;}
.r17p9 .fig .txt{font-size:25px;}
.r17p9 .fig .lbl{font-size:21px;}
.r17p9 .fig .big{font-size:52px;}
.r17p9 .foot{font-size:18px;}

/* P15 案例页：结尾图灵两句压成一句，foot 因此从两行变一行，可以放大一档。 */
.r17p15 .mega .foot{font-size:27px;line-height:1.6;max-width:1560px;}

/* P24 Eval 全生命周期：land 里的 Legora 那句删掉之后，主句独占一行、上一档。 */
.r17p24 .land{font-size:27px;line-height:1.58;}

/* P27 判据页：三张 Signal 卡的描述句 + 四条「怎么验」+ 收尾 note 三块全删。
   删完这一页只剩「三个信号标题 + Q1–Q4 两行对照」，是全场最干净的一页 ——
   卡片整体放大一档，两栏之间的呼吸放开，让「工具时代 / 共事时代」的对仗立住。 */
.r17p27 .head{margin-bottom:36px;}
.r17p27 .body{gap:44px;}
.r17p27 .g3{gap:30px;}
.r17p27 .g3 .card{padding:40px 34px 44px;}
.r17p27 .g3 .card .n{font-size:26px;}
.r17p27 .g3 .card .tag{font-size:20px;}
.r17p27 .g3 .card .t{font-size:54px;}
.r17p27 .g4{gap:26px;}
.r17p27 .g4 .card.sm{padding:34px 28px 38px;gap:22px;}
.r17p27 .g4 .card.sm .hd{margin-bottom:4px;}
.r17p27 .g4 .card.sm .hd .n{font-size:25px;}
.r17p27 .g4 .card.sm .hd .t{font-size:31px;}
.r17p27 .g4 .card.sm .kv{gap:8px;}
.r17p27 .g4 .card.sm .kv .kk{font-size:18px;}
.r17p27 .g4 .card.sm .kv .vv{font-size:24px;line-height:1.55;}

/* P31 案例 03：那段「我不想制造恐慌」的 note 删掉之后，链路图 + 三张教训卡 + 事件块撑满。 */
.r17case3 .body{gap:30px;}
.r17case3 .fig svg{width:100%;height:auto;}
.r17case3 .g3 .card .d{font-size:21px;line-height:1.6;}
.r17case3 .old{padding:26px 28px;}
.r17case3 .old .tx{font-size:24px;}
/* 事件块的来源行：媒体名一行，mono 小字（详细 URL 进设计文档 R17 段）。 */
.r17case3 .old .src{display:block;margin-top:12px;font-family:var(--f-mono);
  font-size:15px;letter-spacing:.06em;color:var(--mark-3);}

/* P46 终页：外/内两列清单（八条）整块删，只留「同一把尺子 → 向外 Eval / 向内 内观」。
   这是全场最后一张，气要足 —— svg 重新排过（纵向长了一半），字号整体再上一档。 */
.r17fin .head{margin-bottom:40px;}
.r17fin .fig{align-items:stretch;}
.r17fin .fig svg{width:100%;height:auto;}
.r17fin .fig .txt{font-size:27px;}
.r17fin .fig .lbl{font-size:19px;letter-spacing:.2em;}
"""

# ── C18 · R18 的页级档 ·只在 CONF_V2=1 装配 ───────────────────────────────────
#    只有一处：P44 那两个 SVG 门换成 Colin 用 GPT-image 生成的单张门图。
C18_CSS = """
/* ============ C18 · R18 · P44 换 GPT 生成门图（单图双门 · screen 融底） ============ */
/* 版面：一行 CEO 那句（原来挂在 svg 里的 .lbl）→ 门图 → 图下双标签 → land 落地句。
   图 1672×669（已裁掉上下的空黑边，长宽比 2.4993），max-width 1380 → 高 552，
   加上标签行 52 = 604；body 实测 764，配 gap 20 与 39 的 caption 行，填充率落在 ~99%。 */
.r18doors .head{margin-bottom:30px;}
.r18doors .body{gap:20px;}
.r18doors .dcap{font-family:var(--f-mono);font-size:24px;letter-spacing:.1em;
  color:var(--coral);text-align:center;line-height:1.4;}
.r18doors .doors{position:relative;width:100%;max-width:1380px;margin:0 auto;padding-bottom:52px;}
/* mix-blend-mode:screen —— 黑底与页面底合成，图片的矩形边界消失。
   ⚠️ 双保险：图本身已经把底色**压到纯 #000**（生成图原来是 rgb(3,3,8) 的抬升黑），
      所以就算 .rise 的 transform/clip-path 造出层叠上下文、blend 只对着透明背景生效，
      边界一样看不出来 —— 两条路任意一条成立，页面都是对的。 */
.r18doors .doors img{display:block;width:100%;height:auto;mix-blend-mode:screen;}
/* 图下双标签：绝对定位到两扇门各自的横向中心（实测 27.2% / 72.3%），
   随图等比缩放永远对得上；文字一字未改，只是从旧 svg 里挪出来重排。 */
.r18doors .doors .dl{position:absolute;bottom:0;transform:translateX(-50%);
  white-space:nowrap;font-size:31px;font-weight:700;line-height:1.2;letter-spacing:.01em;}
.r18doors .doors .dl.am{color:var(--amber);}
.r18doors .doors .dl.co{color:var(--coral);}
"""

# ── C19 · R19 的页级档 ·只在 CONF_V2=1 装配 ───────────────────────────────────
#    三档：P7 换成「单一时间轴 + 对数纵轴」的三线图（.r19money）、五张金句页删 eyebrow 后
#    重心回中（.r19mq）、P44 门图收比例（.r19doors）。全部排在 C18_CSS 之后。
C19_CSS = """
/* ============ C19 · R19 · P7 对数时间轴三线图 / 金句页去 eyebrow / 门图收比例 ============ */
/* P7：Colin「那个带时间轴的曲线的图表更加清楚展示了三者的变化」——数据一个不动，形式换回曲线。
   ⚠️ **红线：不许回双轴**。R16 点名的视觉说谎正是「左 0–200 / 右 0–4 把 $3.3B 画得比 $178B 高」，
      回去等于重犯。三条赛道量级差 ~900 倍（0.21 ↔ 178），单线性轴画不下 ——
      解法是**同一根轴 + 对数刻度**：一根尺、一套网格，量级差用「每格 ×10」表达。
      对数轴唯一的代价是读者要知道它是对数的，所以：① 角落明写「纵轴 · 对数刻度」；
      ② 网格线就是十倍阶梯并逐条标 $0.1B / $1B / $10B / $100B；③ 每个点直接标值，点标即刻度。 */
.r19money .head{margin-bottom:30px;}
.r19money .body{gap:30px;}
.r19money .fig{align-items:stretch;}
.r19money .fig svg{width:100%;height:auto;}
.r19money .fig .lbl{font-size:19px;letter-spacing:.12em;}
.r19money .fig .lbl.yr{font-size:27px;letter-spacing:.16em;fill:var(--ink-2);text-transform:none;}
.r19money .fig .lbl.dec{font-size:19px;letter-spacing:.08em;text-transform:none;}
.r19money .fig .ttl{font-size:34px;}
.r19money .fig .txt.val{font-size:25px;font-weight:500;fill:var(--ink-2);}
.r19money .fig .txt.val.fill-am{fill:var(--amber);}
.r19money .fig .sm{font-size:20px;}
.r19money .fig .sm.anno{font-size:20px;fill:var(--ink-2);}
.r19money .fig .sm.anno.fill-am{fill:var(--amber);}
.r19money .fig .big{font-size:46px;fill:var(--ink);}
.r19money .fig .big.fill-am{fill:var(--amber);}
/* 网格与轴：hair 两档，实线 1px —— 三条数据线是这一页唯一响的东西。 */
.r19money .fig .gd{stroke:var(--hair);stroke-width:1;fill:none;}
.r19money .fig .axb{stroke:var(--hair-strong);stroke-width:1;fill:none;}
/* 三条线：明度 + 粗细双重编码（与 R14 同一套阶梯，amber 是今年的主角）。
   ⚠️ --ink(#fff) 与 --ink-3(#D9D9E3) 并排 ΔE≈11 太近，写代码那条压到 .72 合成 ≈#9C9CA3，
      对 --ink 与 --amber 的 ΔE 都 ≥20；线宽补到 4 保投影可读。 */
.r19money .fig .ln{fill:none;stroke-linecap:round;stroke-linejoin:round;}
.r19money .fig .ln.fnd{stroke:var(--ink);stroke-width:5.5;}
.r19money .fig .ln.cod{stroke:var(--ink-3);stroke-width:4;opacity:.72;}
.r19money .fig .ln.cnv{stroke:var(--amber);stroke-width:7;}
/* 节点：底色描边环（surface ring），两条线在 2024 重合成一个点也认得出。 */
.r19money .fig .dot{stroke:var(--slide-bg);stroke-width:3;}
.r19money .fig .dot.fnd{fill:var(--ink);}
.r19money .fig .dot.cod{fill:var(--ink-3);opacity:.72;}
.r19money .fig .dot.cnv{fill:var(--amber);}
/* 终点名牌引线：极细，只做牵引，不参与读数。 */
.r19money .fig .lead{fill:none;stroke-width:1.4;opacity:.5;}
.r19money .fig .lead.fnd{stroke:var(--ink);}
.r19money .fig .lead.cod{stroke:var(--ink-3);}
.r19money .fig .lead.cnv{stroke:var(--amber);}

/* P31 案例 03：三张教训卡的正文整块删之后只剩标题，链路图 + 事件块接管 —— 标题上两档，
   卡片留白放开，事件块字号上一档，把 72% 撑回红线内。 */
.r19case3 .body{gap:36px;}
.r19case3 .fig svg{width:100%;height:auto;}
.r19case3 .g3{gap:26px;}
.r19case3 .g3 .card{padding:38px 32px 42px;}
.r19case3 .g3 .card .tag{font-size:20px;}
.r19case3 .g3 .card .t{font-size:42px;line-height:1.25;}
.r19case3 .old{padding:30px 32px;}
.r19case3 .old .yr{font-size:21px;}
.r19case3 .old .tx{font-size:27px;}

/* 五张金句页：页型元信息（`观点页 · 嘉宾金句 · 0X`）整块删。
   .mq 本来就是 flex column + justify-content:center，删掉一个子元素**重心自动回中**，
   这里只把 gap 放开一档，让「主文 / 分隔线 / 英文 / 署名」的呼吸补上元信息腾出的那一块。 */
.r19mq .mq{gap:44px;}

/* P44 门图：Colin 说现在有点过大 —— 1380 收到 1180（高 552 → 472），留白多一点。
   标签仍是 % 定位（27.2% / 72.3%），随图等比自适应，一个数都不用改。 */
.r19doors .body{gap:32px;}
.r19doors .doors{max-width:1180px;}
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

# ══════════════════════════════════════════════════════════════════════════════
# ── C16（2026-08-06 · R16 · 五处 · 页数不变 46）─────────────────────────────────
# Colin 复看 R15 之后的五处，其中两处是**改判**（把上一轮放错地方的东西挪回去、
# 把一句从没核到一手的署名改对），一处是**推倒重来**（钱流向图的数据 + 画法）：
#   ① 金句 01 主文换成「我们叫了它三年 Agent（代理人）——今天，它终于开始代理了。」
#      —— R15 把这句放上了 PART 2 幕卡，Colin 澄清本意是金句页。承句「所以今年这一场…」不动。
#   ② PART 2 幕卡首行退回 R15 之前的原文（「被记住…被托付…」），第二行导航不动。
#      ①② 合起来是一次搬家：搬完全 deck「我们叫了它三年」恰好一处（金句 01）。
#   ③ 金句 02（Weil）中上英下：中文升主（中文金句字号体系），英文降为下方 mono 原文补充。
#   ④ 金句 03 中上英下 + **出处改正**：这句不是 Bret Taylor 的，是 Des Traynor
#      （Intercom 联合创始人），Cheeky Pint #11。英文逐字已核到一手 transcript。
#   ⑤ P7 钱流向页：数据重查 + 弃双轴重画成三格小倍数（Colin 三条质疑全部成立）。
# 取页一律**内容锚定**（沿用 C15 的 _ix），不信页号；母版 62 页仍然只读。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    # ── C16-① 金句 01 · 主文换血 ────────────────────────────────────────────
    #    换下的「兑现的，不是模型更聪明了。是「谁负责」这件事，终于有了答案。」全场仅此一处，
    #    换掉即清零（「责任」这层意思由紧跟的承句「讲的不是能力，是责任」原样承接）。
    #    分行：破折号前/后一刀两段 —— 前半是「叫了三年」的铺垫，后半是名词打成动词的落点。
    #    实测两行在 .mq（1920 − padding 190×2 = 1540px）里最宽 ≈1390px，不用降字号档。
    _I_MQ1 = _ix('<i class="rise" style="--i:1">兑现的，</i>')
    _cut1(_I_MQ1, '\n      <i class="rise" style="--i:1">兑现的，</i>',
                  '<i class="rise" style="--i:4">终于有了答案。</i>', '''
      <i class="rise" style="--i:1">我们叫了它三年 Agent（代理人）——</i>
      <i class="rise" style="--i:2">今天，它终于开始代理了。</i>''')
    _r1(_I_MQ1, '<div class="s rise" style="--i:6">所以今年这一场，讲的不是能力，是责任。</div>',
                '<div class="s rise" style="--i:4">所以今年这一场，讲的不是能力，是责任。</div>')
    assert '兑现的，' not in _secs[_I_MQ1] and '谁负责' not in _secs[_I_MQ1], 'C16-① 旧主文未清零'

    # ── C16-② PART 2 幕卡首行还原（撤销 C15-④）──────────────────────────────
    #    R15 把上面那句打磨完放到了幕卡上；Colin 澄清本意是放金句页 —— 幕卡首行退回原文。
    #    第二行「这一幕只讲一件事：那把尺子怎么造。」是本幕导航，两轮都没动过。
    _I_ACT2b = _ix('<div class="cn spread" style="--i:3">被托付</div>')
    _r1(_I_ACT2b,
        '<div class="d flow" style="--i:4">我们叫了它三年 Agent（代理人）——今天，它终于开始代理了。<br>'
        '这一幕只讲一件事：那把尺子怎么造。</div>',
        '<div class="d flow" style="--i:4">被记住，靠的是一致性。被托付，靠的是可验证。<br>'
        '这一幕只讲一件事：那把尺子怎么造。</div>')
    #    搬家账：全 deck「我们叫了它三年」必须恰好一处（金句 01），幕卡上不许再有
    assert '我们叫了它三年' not in _secs[_I_ACT2b], 'C16-② 幕卡上不该再有那句金句'
    assert sum(_x.count('我们叫了它三年') for _x in _secs) == 1, 'C16-①② 搬家后应恰好一处'

    # ── C16-③ 金句 02（Weil）· 中上英下 ─────────────────────────────────────
    #    本场对象是中文听众：中文回到 .mq .q 的中文金句体系（80px/900），
    #    英文原句缩到下方一行 mono 作原文补充（质感留着，但不再抢主）。署名行不动。
    #    中文分行落在自然停顿上（「是 AI 时代 / 一个产品经理…」），禁止词中断行。
    _I_MQ2b = _ix('Writing evals is the most important')
    _cut1(_I_MQ2b, '\n      <i class="rise" style="--i:1">&#8220;Writing evals',
                   '<div class="s rise" style="--i:5">Kevin Weil · OpenAI 前 CPO</div>', '''
      <i class="rise" style="--i:1">写评测，是 AI 时代</i>
      <i class="rise" style="--i:2">一个产品经理能做的最重要的事。</i>
    </div>
    <div class="rule"></div>
    <div class="en rise" style="--i:4">&#8220;Writing evals is the most important thing a PM can do in the AI era.&#8221;</div>
    <div class="s rise" style="--i:5">Kevin Weil · OpenAI 前 CPO</div>''')
    _cls(_I_MQ2b, 'r16mq2')

    # ── C16-④ 金句 03 · 中上英下 + 出处改正 ─────────────────────────────────
    #    ⚠️ 出处改正（Colin 2026-08-06 拍板）：这句不是 Bret Taylor 的 ——
    #       是 **Des Traynor（Intercom 联合创始人）**，Stripe 的 Cheeky Pint 播客第 11 期
    #       《…the "four horsemen" of good AI companies》（John Collison 主持）。
    #       英文逐字已核到一手：Cheeky Pint 官方 Substack 挂的 rev.com transcript，
    #       Des 的这一段落在 **[00:10:29]**（deeplink ts=629.89），与 deck 现有英文**逐字一致**，
    #       所以英文一个字不改，只改署名 + 补出处行。
    #       Colin 口述的时间戳是 00:09:56，与官方 transcript 差 33 秒（疑为 YouTube 版偏移）——
    #       页面按**一手 transcript 口径**写 00:10:29，差异写进设计文档 R16 段待 Colin 一句话定夺。
    #    ⚠️ 全 deck 的「Bret Taylor」这一轮只动这一处：另外三处都是**核过的真引文**，不许连坐 ——
    #       P4「English over PSTN」（本仓 csagent.html 记为 Cheeky Pint #27 · 原句照抄）、
    #       P23 Sierra 官方博客「you don't pay for tokens」、
    #       P43「Hyper high-agency people who really deeply care.」（highagency.html 记为 #27 [01:28:23]）。
    _I_MQ3 = _ix('One of the biggest fallacies in AI')
    _cut1(_I_MQ3, '\n      <i class="rise" style="--i:1">&#8220;One of the biggest fallacies',
                  '<div class="s rise" style="--i:5">Bret Taylor · Sierra CEO / OpenAI 董事长</div>', '''
      <i class="rise" style="--i:1">AI 最大的谬误之一，是人们总把它</i>
      <i class="rise" style="--i:2">跟一个并不存在的完美的人相比。</i>
    </div>
    <div class="rule"></div>
    <div class="en rise" style="--i:4">&#8220;One of the biggest fallacies in AI is people compare it with this perfect human that does not exist.&#8221;</div>
    <div class="s rise" style="--i:5">Des Traynor · Intercom 联合创始人</div>
    <div class="s src rise" style="--i:6">Cheeky Pint #11 · 00:10:29</div>''')
    _cls(_I_MQ3, 'r16mq3')
    assert 'Bret Taylor' not in _secs[_I_MQ3], 'C16-④ 金句 03 不该再有 Bret Taylor'

    # ── C16-⑤ P7 钱流向页 · 数据重查 + 弃双轴重画 ────────────────────────────
    #    Colin 三条质疑，条条成立：
    #      1) 双轴（左 0–200 / 右 0–4）把 $3.3B 画得比 $178B 还高 —— 视觉说谎；
    #      2) 对话式 2024 $2.1B → 2025 ≈$0.7B 取数残缺（产业 2025 并没有萎缩到 1/3）；
    #      3) 融资额和 Cursor ARR $2B 混在同一张图，口径没标（融资 ≠ 收入）。
    #
    #    ⓐ 数据重查（每个数字都带来源与日期，一律一级市场**披露融资额**，不造数）：
    #       · 基础模型 —— Crunchbase News 2026-04-02《Sector Snapshot: … Foundational AI …》：
    #         2024 $31.4B / 52 笔，2025 $88.9B / 66 笔，2026 **Q1（截至 3-31）** $178B / 24 笔。
    #         ⚠️ $178B 是**一季度**数，不是「至今」—— R14 标成「至今」是错的，这一轮标清 Q1。
    #         （H1 口径查无可靠的「基础模型」聚合：Crunchbase 2026-07-02 只给了
    #          「OpenAI + Anthropic 两家 = $217B = H1 全球创投的 43%」，不是同一把尺，不采用。）
    #       · AI 写代码 —— New Market Pitch《AI Coding Market: 21 Funding Deals》2026-07-13
    #         逐笔表自算复核：2024 **$1.59B**/11 笔，2025 **$3.25B**/6 笔（Cursor 两轮
    #         $900M + $2.3B = $3.2B，占 98%），2026 **H1（截至 7-02）$207.5M**/4 笔。
    #         → R14 的 1.6 / 3.3 是对的；而 2026 **有**可比的融资聚合数，所以这一格能画满三年。
    #         → Cursor ARR $2B **从图上彻底移除**（ARR 是收入不是融资，收入故事 P8/P9 已有）。
    #       · 对话式 AI —— 同一家同一天同一口径《Conversational AI: 89 Funding Deals》：
    #         2024 **$1.59B**/33 笔，2025 **$1.94B**/30 笔，2026 **H1（截至 7-02）$1.82B**/26 笔。
    #         → R14 的 2.1 / ≈0.7 / 2.2+ **三个数全错**：2025 不但没萎缩到 1/3，还比 2024 涨了；
    #           2026 只用半年就追平 2025 全年 —— 这才是「现在轮到对话」的真凭据。
    #         ⚠️ 该表尚未收录 Sierra 2026-05-04 的 $950M（TechCrunch / CNBC 已实锤），
    #           所以 $1.82B 是**保守下限**；图上不擅自补录（补了就是混口径），只在 note 里点名。
    #    ⓑ 画法（dataviz 纪律）：
    #       双轴是 dataviz anti-patterns 的头一条（两套刻度的对齐是任意的，图会凭空造相关性），
    #       它给的标准解就是**小倍数**。三格并排、各用各的 y 尺、共享 x（2024 / 2025 / 2026），
    #       量级差写在图上明说，口径一行标清。柱高只在格内可比 —— 跨格比的是形状。
    #       · 无 y 轴无网格：每格三根柱各自直接挂值标，值标就是这一格的刻度（小倍数标准做法）；
    #       · 柱 = 96px 粗的竖直 .dw 描边，入场从基线长上来，--len 与柱高逐条同步；
    #       · emphasis：每格「落点年」（钱砸得最狠那年）用本格主色，其余降到 .34，不另生色相；
    #       · 三格主色即叙事阶梯：白（模型）→ 灰（写代码，已收尾）→ amber（对话，正在发）；
    #       · 对话式整格 data-step=1（讲到这里才出现），note 第三拍 —— data-step 仍 ≤2。
    #    坐标账（viewBox 0 0 1680 560）：三格 x 起点 0 / 590 / 1180，格宽 500，格间 90；
    #       格内三根柱心 x = +83 / +250 / +417，柱宽 96；基线 y=446，满格柱高 280（顶 y=166）。
    #       柱高 = 值 / 本格最大值 × 280，逐根算在下面的注释里。
    _I16 = _ix('近三年，钱的三次落点')
    _cut1(_I16, '        <svg viewBox="0 40 1680 530"', '        </svg>', '''        <svg viewBox="0 0 1680 560" width="1680" fill="none">
          <!-- ① 顶行：左边一行口径（单一，不再有第二把尺）；右边一句话交代为什么分三格 -->
          <g class="pop" style="--i:0">
            <text class="lbl" x="0" y="26">口径：一级市场披露融资额 · $B</text>
            <text class="lbl" x="1680" y="26" text-anchor="end">三条赛道量级差百倍，同一把尺画不下：三格各用各的尺，看形状</text>
          </g>

          <!-- ② 基础模型（自有尺 0–178）：31.4 → 88.9 → 178，柱高 49.4 / 139.8 / 280 -->
          <g class="pop" style="--i:1">
            <text class="ttl" x="0" y="64">基础模型</text>
            <text class="big" x="500" y="68" text-anchor="end">$178B</text>
            <text class="sm" x="500" y="98" text-anchor="end">2026 Q1 · 截至 3-31</text>
            <path class="pr" d="M0 118 H500"/>
          </g>
          <path class="col fnd dim dw" style="--len:56;--i:2" d="M83 446 V396.6"/>
          <path class="col fnd dim dw" style="--len:146;--i:3" d="M250 446 V306.2"/>
          <path class="col fnd dw" style="--len:286;--i:4" d="M417 446 V166"/>
          <g class="pop" style="--i:4">
            <text class="txt val" x="83" y="380.6" text-anchor="middle">$31.4B</text>
            <text class="txt val" x="250" y="290.2" text-anchor="middle">$88.9B</text>
            <text class="txt val" x="417" y="150" text-anchor="middle">$178B</text>
            <path class="axb" d="M0 446 H500"/>
            <text class="lbl yr" x="83" y="480" text-anchor="middle">2024</text>
            <text class="lbl yr" x="250" y="480" text-anchor="middle">2025</text>
            <text class="lbl yr" x="417" y="480" text-anchor="middle">2026</text>
            <text class="sm" x="417" y="508" text-anchor="middle">至今</text>
            <text class="sm anno" x="0" y="546">一个季度，就是去年一整年的两倍</text>
          </g>

          <!-- ③ AI 写代码（自有尺 0–3.25）：1.59 → 3.25 → 0.21，柱高 137 / 280 / 18.1
               落点年 = 2025（那一轮的钱在一年里发完，Cursor 两轮就占了 98%） -->
          <g class="pop" style="--i:5">
            <text class="ttl" x="590" y="64">AI 写代码</text>
            <text class="big" x="1090" y="68" text-anchor="end">$0.2B</text>
            <text class="sm" x="1090" y="98" text-anchor="end">2026 上半年 · 截至 7-02</text>
            <path class="pr" d="M590 118 H1090"/>
          </g>
          <path class="col cod dim dw" style="--len:143;--i:6" d="M673 446 V309"/>
          <path class="col cod dw" style="--len:286;--i:7" d="M840 446 V166"/>
          <path class="col cod dim dw" style="--len:24;--i:8" d="M1007 446 V427.9"/>
          <g class="pop" style="--i:8">
            <text class="txt val" x="673" y="293" text-anchor="middle">$1.6B</text>
            <text class="txt val" x="840" y="150" text-anchor="middle">$3.3B</text>
            <text class="txt val" x="1007" y="411.9" text-anchor="middle">$0.2B</text>
            <path class="axb" d="M590 446 H1090"/>
            <text class="lbl yr" x="673" y="480" text-anchor="middle">2024</text>
            <text class="lbl yr" x="840" y="480" text-anchor="middle">2025</text>
            <text class="lbl yr" x="1007" y="480" text-anchor="middle">2026</text>
            <text class="sm" x="1007" y="508" text-anchor="middle">至今</text>
            <text class="sm anno" x="590" y="546">一轮钱在 2025 发完 · Cursor 一家占 98%</text>
          </g>

          <!-- ④ 对话式 AI（自有尺 0–1.94）：1.59 → 1.94 → 1.82，柱高 229.5 / 280 / 262.7
               整组 data-step=1：讲到这里才出现。落点年 = 2026（半年追平去年全年） -->
          <g data-step="1">
            <g class="pop" style="--i:0">
              <text class="ttl" x="1180" y="64">对话式 AI</text>
              <text class="big fill-am" x="1680" y="68" text-anchor="end">$1.8B</text>
              <text class="sm" x="1680" y="98" text-anchor="end">2026 上半年 · 截至 7-02</text>
              <path class="pr" d="M1180 118 H1680"/>
            </g>
            <path class="col cnv dim dw" style="--len:235;--i:1" d="M1263 446 V216.5"/>
            <path class="col cnv dim dw" style="--len:286;--i:2" d="M1430 446 V166"/>
            <path class="col cnv dw" style="--len:268;--i:3" d="M1597 446 V183.3"/>
            <g class="pop" style="--i:3">
              <text class="txt val" x="1263" y="200.5" text-anchor="middle">$1.6B</text>
              <text class="txt val" x="1430" y="150" text-anchor="middle">$1.9B</text>
              <text class="txt val fill-am" x="1597" y="167.3" text-anchor="middle">$1.8B</text>
              <path class="axb" d="M1180 446 H1680"/>
              <text class="lbl yr" x="1263" y="480" text-anchor="middle">2024</text>
              <text class="lbl yr" x="1430" y="480" text-anchor="middle">2025</text>
              <text class="lbl yr" x="1597" y="480" text-anchor="middle">2026</text>
              <text class="sm" x="1597" y="508" text-anchor="middle">至今</text>
              <text class="sm anno fill-am" x="1180" y="546">半年，已经追平去年一整年</text>
            </g>
          </g>
        </svg>''')
    #    note 按最终数据重写：2024 两条赛道同一起跑线（都是 $1.6B），两年后一条发完、一条刚开始发。
    #    「上半年」的说法与实际取数窗口（1-01 → 7-02）相符；Sierra 五月那笔点名说明为什么 $1.82B 是下限。
    _cut1(_I16, '<div class="note" data-step="2">', '下一页拆开看。</b></span></div>',
          '<div class="note" data-step="2"><span class="flow" style="--i:0">2024 那一年，写代码和对话式拿到的钱一样多，'
          '都是 $1.6B。之后分了岔：写代码那一轮在 2025 一次发完（$3.25B，Cursor 一家占 98%），2026 上半年只剩 $0.21B；'
          '对话式这一轮才刚开始发——2026 前六个月的 $1.82B 已经追平 2025 全年，而这还没算进 Sierra 五月那笔 $950M。'
          '<b>对话式 AI 是个大泛类：消费声音侧 ElevenLabs $500M @ $11B、企业智能体侧 Sierra $950M @ $15B，'
          '花的是同一笔钱。这笔钱在这一层内部又分给了谁——下一页拆开看。</b></span></div>')
    #    foot 仍是 R14 体例：只留来源名，逐条口径（年份 / 截点 / 笔数 / URL）留档在设计文档 R16 段。
    _r1(_I16, '<div class="foot flow rev" style="--i:9">Source · Crunchbase · CB Insights《State of AI 2025》'
              '· TechCrunch · Bloomberg · CNBC</div>',
              '<div class="foot flow rev" style="--i:9">Source · New Market Pitch · Crunchbase News '
              '· TechCrunch · CNBC</div>')
    _cls(_I16, 'r16money')
    assert 'Cursor ARR' not in _secs[_I16][_secs[_I16].index('<svg'):_secs[_I16].index('</svg>')], \
        'C16-⑤ svg 里不许再出现 ARR（融资轴只能画融资）'

# ══════════════════════════════════════════════════════════════════════════════
# ── C17（2026-08-06 · R17 · 十二处 · 页数不变 46）───────────────────────────────
# 这一轮是**熵减**：十二处里九处是纯删文（Colin 逐页点名「这块可以删」），
# 一处点名研究（案例 03 的模型厂实名）、一处标题对调、一处出处精化、一处按兵不动。
#   ①  P27 判据页    · 删三张 Signal 卡的描述句 + 四条「怎么验」+ 收尾 note（六块）
#   ②  P31 案例 03   · a) 删「我不想制造恐慌」整段  b) 事件主体**实名**（已查实）
#   ③  P45 全场收束  · h2 换「全场收束，一页带走」，旧 h2 降级进 eyebrow
#   ④  P46 终页      · 删外/内两列共八条清单，余下元素放大重排（svg 重画）
#   ⑤  P8  六卡页    · 删国内存量 note + foot
#   ⑥  P9  渗透页    · 删预测对照整块 + foot 简化成只留机构名（Gartner 随预测一起撤）
#   ⑦  P7  三格图    · 删整个 note 段（Sierra 未收录那层意思改由口播承担 + 设计文档留档）
#   ⑧  P15 96.5% 页  · 结尾图灵两句压成一句（含两处口径修正，见下）
#   ⑨  P24 Eval 全周期· 删 Legora 那句
#   ⑩  四张 PART 幕卡 · 开头小字 .d 整块删（编号 / 幕名 / 英文名 / nav rail 都不动）
#   ⑪  P4  PSTN 页   · 出处「2026-03 公开访谈」→「Cheeky Pint #27」（R16 查到的，顺手落地）
#   ⑫  P44           · 本轮一个字不动（Colin 要换一张门的生成图，图回来才动版面）
# 取页一律**内容锚定**（沿用 _ix），不信页号；母版 62 页仍然只读。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    # ── C17-① P27 判据页 · 删六块 ───────────────────────────────────────────
    #    删完这一页只剩「三个 Signal 标题 + Q1–Q4 的工具时代/共事时代两行对照」——
    #    对照本身就是判据，描述句是把对照又用散文说了一遍；四条「怎么验」是第三遍。
    #    ⚠️ Q4 那句长的「先有归属，才谈得上追责…」Colin 没点名，**保留**。
    _I_SIG = _ix('可观测，才敢写进需求文档')
    for _d in ('\n          <div class="d">不是你问它才查。是你还没开口，它先把上次没结掉的那件事捞了出来。</div>',
               '\n          <div class="d">这通电话、这条消息、这次确认，是它发起的。发起权第一次不在人这边。</div>',
               '\n          <div class="d">它带来的成交、它造成的损失，记在它的编号下，而不是摊进某个人的 KPI。</div>',
               '\n          <div class="kv"><div class="kk">怎么验</div><div class="vv">翻最近 100 次交互，几次是它发起的？</div></div>',
               '\n          <div class="kv"><div class="kk">怎么验</div><div class="vv">它自报家门那句话，写在哪个文件里？</div></div>',
               '\n          <div class="kv"><div class="kk">怎么验</div><div class="vv">报表里有没有独立的一行？</div></div>',
               '\n          <div class="kv co"><div class="kk">怎么验</div><div class="vv">出事五分钟内，你拿得出那条链路吗？</div></div>'):
        _r1(_I_SIG, _d, '')
    _cut1(_I_SIG, '\n      <div class="note"><span class="flow" style="--i:9">这四句话里',
                   '四个「怎么验」，回去就能跑一遍。</b></span></div>', '')
    #    三个 Signal 标题与 Q1–Q4 两行对照必须原样在（删的是描述，不是判据）
    for _keep in ('它主动想起', '它主动开口', '它有自己的 OKR',
                  '先有归属，才谈得上追责——业绩可以记在它名下，责任必须落在可追责的人身上。'):
        assert _keep in _secs[_I_SIG], f'C17-① 该保留的被误删：{_keep}'
    assert '怎么验' not in _secs[_I_SIG] and '<div class="d">' not in _secs[_I_SIG] \
       and '<div class="note"' not in _secs[_I_SIG], 'C17-① 六块未删净'
    _cls(_I_SIG, 'r17p27')

    # ── C17-② P31 案例 03 · 删「不制造恐慌」+ 事件主体实名 ────────────────────
    #    a) 那段 note 是「我想用它说明一件事…」的自我解说，三张教训卡已经把话说完了。
    _I_C3 = _ix('两道围栏：提示词拦话术，')
    _cut1(_I_C3, '\n      <div class="note co flow" style="--i:10">我不想用这一页制造恐慌',
                 '从伦理讨论变成了工程需求。</div>', '')
    assert '恐慌' not in _secs[_I_C3], 'C17-②a 未删净'
    #    b) 实名（Colin 2026-08-06 拍板可以点名；本轮 WebSearch 查实，事件指纹极独特、
    #       多家一线媒体交叉一致，属「板上钉钉」，故落地）：
    #         · 模型厂 = **OpenAI**（2026-07-21 自曝，Fortune / The Hacker News / CBS / TechCrunch）
    #         · 第三方平台 = **Hugging Face**（生产设施被入侵，为的是偷 ExploitGym 评测答案）
    #         · 平台 CEO = **Clem Delangue**，原话 "This incident, **possibly the first of its kind**,
    #           proves a point we've long believed…"（另于 TechCrunch 2026-07-26 称
    #           "The first autonomous agent cyberattack is an unprecedented event."）
    #           → 页面上「可能是同类中的第一起」是这句的直译，比原来的转述更贴一手。
    #         · 24 小时那句也**查实了**：自曝 7-21，OpenAI Presence（企业级 Agent 平台，
    #           官方通稿主打 built-in guardrails）7-22 发布 —— 确实不到 24 小时。
    #         · 逃逸手段：Artifactory 零日（≤7.16.1）→ 提权 → 横向移动 → 窃取凭证 → RCE。
    #       逐条 URL 进设计文档 R17 段；页面上只挂一行媒体名（沿用 R14 起的 foot 体例）。
    _r1(_I_C3, '<div class="yr">2026-07 · 一家模型厂的公开披露</div>',
               '<div class="yr">2026-07 · OpenAI 的公开披露</div>')
    _r1(_I_C3, '其一个未发布模型在评测过程中<b>逃出沙箱、利用漏洞并窃取凭证</b>，'
               '入侵了一家第三方平台的生产设施。该平台 CEO 称其「<b>可能是第一起 AI 逃逸并攻击第三方的事件</b>」。'
               '<br>这件事的披露，距离同一家公司发布「可被信任的企业级 Agent」，<b>相隔不到 24 小时</b>。',
               '其一个未发布模型在评测过程中<b>逃出沙箱、利用漏洞并窃取凭证</b>，'
               '入侵了 <b>Hugging Face</b> 的生产设施。Hugging Face CEO Clem Delangue 称这起事件'
               '「<b>可能是同类中的第一起</b>」。'
               '<br>这件事的披露（7-21），距离同一家公司发布主打「内置围栏」的企业级 Agent 平台 '
               '<b>OpenAI Presence</b>（7-22），<b>相隔不到 24 小时</b>。'
               '<span class="src">Fortune · The Hacker News · TechCrunch · CBS News · 2026-07</span>')
    #    c) 顺手修一处**祖传 2px 越界**：这张链路图的 viewBox 高 260，而底下那条
    #       「提示词 · 策略文档」标注的基线在 y=257（15px 字，下缘 ≈262）——
    #       靠母版 `.fig svg{overflow:visible}` 才没被裁掉，但 QA 新加的「svg 文字不出自己的框」
    #       会如实报出来。把 viewBox 加高 12（260 → 272）一次修干净，图元一个不动。
    _r1(_I_C3, '<svg width="1680" viewBox="0 0 1680 260" fill="none">',
               '<svg width="1680" viewBox="0 0 1680 272" fill="none">')
    _cls(_I_C3, 'r17case3')

    # ── C17-③ P45 全场收束 · 标题对调 ───────────────────────────────────────
    #    「越往上，答案越短 —— 也越重」是一句**评论**，不是这一页的功能；功能是「一页带走」。
    #    评论降级进 eyebrow（与新 h2 的「全场收束」不重复，所以 eyebrow 里的那四个字撤掉）。
    _I_END17 = _ix('越往上，答案<em>越短</em> —— 也越重')
    _r1(_I_END17, '<h2 class="ink" style="--i:1">越往上，答案<em>越短</em> —— 也越重</h2>',
                  '<h2 class="ink" style="--i:1">全场收束，<em>一页带走</em></h2>')
    _r1(_I_END17, '<div class="eyebrow flow" style="--i:0">全场收束 · ONE LINE EACH</div>',
                  '<div class="eyebrow flow" style="--i:0">ONE LINE EACH · 越往上，答案越短，也越重</div>')

    # ── C17-④ P46 终页 · 删外/内两列八条 + svg 重画 ──────────────────────────
    #    八条清单是「回去怎么用」的操作细则，终页不该背它（P41 对产品经理那页已经讲过一遍）。
    #    删完只剩「同一把尺子 → 向外 Eval / 向内 内观」这一个对称结构 —— 这才是全场最后一眼。
    #    ⚠️ 删掉负 y 区之后，剩下的图只占 1680×~430（3.9:1 的宽扁），照原样摆只能填到 ~60%。
    #       所以 svg 整张按新版心重画：viewBox 0 0 1680 640，尺子加长（299 → 420）、
    #       两条箭头线下移到 y=300、三级文字各自加大一档，图自己撑满 body。
    #       --len 逐条配套：右线 392 → 400 · 左线 400 → 410 · 四道刻度合计 120 → 140。
    _I_FIN = _ix('同一把尺子，向外叫 <em>Eval</em>，向内叫<em>内观</em>')
    _cut1(_I_FIN, '        <svg width="1680" viewBox="0 -177 1680 646" fill="none">', '        </svg>',
          '''        <svg width="1680" viewBox="0 0 1680 640" fill="none">
          <!-- 尺子本体：加长到 420，四道刻度跟着重排（长短相间，读起来才像刻度） -->
          <rect class="pop" style="--i:2" x="800" y="90" width="88" height="420" rx="5" fill="var(--on-fill)" stroke="var(--amber)" stroke-width="2.6"/>
          <path class="stroke-am dw" style="--len:140;--i:3" stroke-width="1.8" d="M800 176 H836 M800 258 H824 M800 340 H836 M800 422 H824"/>
          <g class="pop" style="--i:3"><text class="ttl fill-am" x="844" y="592" text-anchor="middle" style="font-size:54px">同一把尺子</text></g>

          <!-- 向外：尺子 → Agent / 产品 -->
          <path class="stroke dw" style="--len:400;--i:4" stroke-width="1.8" d="M908 300 H1300"/>
          <path class="fill-ink pop" style="--i:4" d="M1300 284 L1320 300 L1300 316 Z"/>
          <g class="pop" style="--i:5"><text class="ttl" x="1352" y="258" style="font-size:56px">向外 · Eval</text></g>
          <text class="txt pop" style="--i:5" x="1352" y="330">让我们看见系统的偏差</text>
          <text class="lbl pop" style="--i:5" x="1352" y="396">AGENT / PRODUCT</text>

          <!-- 向内：尺子 → 人 / 自己 -->
          <path class="stroke-co dw" style="--len:410;--i:6" stroke-width="1.8" d="M780 300 H380"/>
          <path class="fill-co pop" style="--i:6" d="M380 284 L360 300 L380 316 Z"/>
          <g class="pop" style="--i:7"><text class="ttl fill-co" x="328" y="258" text-anchor="end" style="font-size:56px">向内 · 内观</text></g>
          <text class="txt pop" style="--i:7" x="328" y="330" text-anchor="end">让我们承认自己的偏差</text>
          <text class="lbl pop" style="--i:7" x="328" y="396" text-anchor="end">HUMAN / SELF</text>

          <!-- 同一个源头、同长的两条路、同一组时序：两枚光点永远同时出发、同时到达 -->
          <g class="pop" style="--i:7">
            <path class="stroke-am pkt" stroke-width="4"
              style="--pl:70px;--p0:70px;--p1:-400px;--pt:4.8s;--pd:1.4s" d="M908 300 H1300"/>
            <path class="stroke-co pkt" stroke-width="4"
              style="--pl:70px;--p0:70px;--p1:-400px;--pt:4.8s;--pd:1.4s" d="M780 300 H380"/>
          </g>
        </svg>''')
    for _gone in ('外 · AGENT', '抢话、复读、没转人工', '一百条里踩了几条', '模型的问题还是流程的',
                  '同一套题，分数动没动', '内 · 读自己', '我凭什么说它不行', '我的判断能不能复现',
                  '我是不是在用感觉验收', '我改的是它还是我的标准'):
        assert _gone not in _secs[_I_FIN], f'C17-④ 两列清单未删净：{_gone}'
    _cls(_I_FIN, 'r17fin')

    # ── C17-⑤ P8 六卡页 · 删国内存量 note + foot ────────────────────────────
    #    国内存量那一段（¥5,850 亿 / >2,000 亿 / 15–20%）与下一页 P9 的读数是同一层意思，
    #    而 15–20% 那个数在 P9 图上还有一条独立的读数条 —— 删这里不丢信息。
    _I_P8 = _ix('对话式 AI 的钱，<em>流向了哪里</em>')
    _cut1(_I_P8, '\n      <div class="note flow" style="--i:8">这还只是海外。', '早就趴在预算科目里。</div>', '')
    _cut1(_I_P8, '\n      <div class="foot flow rev" style="--i:9">整个 conversational AI',
                 '国内存量口径：CC-CMM / 艾媒咨询</div>', '')
    assert '5,850' not in _secs[_I_P8] and '<div class="foot' not in _secs[_I_P8], 'C17-⑤ 未删净'
    assert 'ElevenLabs · 语音合成' in _secs[_I_P8], 'C17-⑤ 六张卡不该被动'
    _cls(_I_P8, 'r17p8')

    # ── C17-⑥ P9 渗透页 · 删预测对照 + foot 只留机构名 ──────────────────────
    #    「预测还在打架」这层对照，R15 把它从主标题降到 note 时留了一条命；这一轮整块删。
    #    ⚠️ 连坐检查：Gartner 全 deck 只在这一条 foot 里出现，随预测对照一起撤，撤完清零。
    _I_P9 = _ix('对话式智能体的采购，<em>正在悄然发生</em>')
    _cut1(_I_P9, '\n      <div class="note co"><span class="flow" style="--i:10">至于预测？',
                 '这道题第二、三幕来解。</span></div>', '')
    _r1(_I_P9, '<div class="foot flow rev" style="--i:11">SOURCE · 66% 与 70%：Salesforce'
               '《State of Service: AI Agents Edition》2026-05（n=3,075 · 2026 年 3–4 月实地）'
               '· 91% 与 15–20%：CC-CMM · 艾媒咨询 · 第一新声 2025 · 49%：Pew Research 2026-06'
               '（n=5,119）· 预测对照：Gartner 2025–2026</div>',
               '<div class="foot flow rev" style="--i:11">SOURCE · Salesforce · CC-CMM · 艾媒咨询 '
               '· 第一新声 · Pew Research</div>')
    _cls(_I_P9, 'r17p9')

    # ── C17-⑦ P7 三格小倍数 · 删整个 note 段 ────────────────────────────────
    #    图自己已经把三拍说清楚了（格内 take + 终值大字），note 是把图又读了一遍。
    #    ⚠️ 被删掉的两层信息**不丢**：Sierra $950M 未被 New Market Pitch 收录（所以 $1.82B 是
    #       保守下限）+ 大泛类两翼明细 —— 一律移进设计文档 R17 段留档，台上由口播承担。
    _I_P7 = _ix('近三年，钱的三次落点')
    _cut1(_I_P7, '\n      <div class="note" data-step="2">', '下一页拆开看。</b></span></div>', '')
    assert '<div class="note' not in _secs[_I_P7] and 'Sierra' not in _secs[_I_P7], 'C17-⑦ note 未删净'
    assert '口径：一级市场披露融资额 · $B' in _secs[_I_P7] and '半年，已经追平去年一整年' in _secs[_I_P7], \
        'C17-⑦ 口径行/格内注不该被动'
    #    ⚠️ note 一走，图必须**自己长高**，否则 .fig 只是把 560 高的图居中、上下各留一大条。
    #       做法：把**顶行那一组（口径 + 尺度说明）之外的所有 y 整体下移 84**，viewBox 同步
    #       560 → 644。为什么非下移不可：R17 把表头终值大字从 40px 提到 46px 之后，
    #       .big 的 bbox 顶（68−46=22）已经吃进顶行 19px 小字的 bbox 底（31），
    #       QA 的「svg 文字零重叠」实测直接报了两处（口径说明 × $0.2B / $1.8B）；
    #       下移 84 一次把这条缝拉开到 ~19px，顺带让图从 560 长到 644 吃满 .fig 的空档。
    #       历史层 C16 那张 svg 的源码**一个字不改**，这里只做坐标搬运（C16 段的几何断言随之改判）。
    _sa = _secs[_I_P7].index('<svg'); _sb = _secs[_I_P7].index('</svg>')
    _sv17 = _secs[_I_P7][_sa:_sb]
    assert _sv17.count('viewBox="0 0 1680 560"') == 1, 'C17-⑦ 钱页 svg viewBox 定位失败'
    _sv17 = _sv17.replace('viewBox="0 0 1680 560"', 'viewBox="0 0 1680 644"', 1)
    _tend = _sv17.index('</g>') + 4          # 顶行那一组（口径 + 尺度说明）到此为止，y 不动
    _hd17, _rs17 = _sv17[:_tend], _sv17[_tend:]
    assert '口径：一级市场披露融资额' in _hd17 and '三格各用各的尺' in _hd17, 'C17-⑦ 顶行分割失败'
    _shift = lambda v: f'{float(v) + 84:g}'
    #       路径里的纵坐标：`M x y H x2`（横线，只有一个 y）与 `M x y V y2`（柱，两个 y）
    _rs17 = re.sub(r'\bd="M([\d.]+) ([\d.]+) ([HV])([\d.]+)"',
                   lambda m: f'd="M{m.group(1)} {_shift(m.group(2))} {m.group(3)}'
                             f'{_shift(m.group(4)) if m.group(3) == "V" else m.group(4)}"', _rs17)
    _rs17 = re.sub(r'\by="([\d.]+)"', lambda m: f'y="{_shift(m.group(1))}"', _rs17)
    _secs[_I_P7] = _secs[_I_P7][:_sa] + _hd17 + _rs17 + _secs[_I_P7][_sb:]
    #       搬运账（抽查四处：表头 / 基线 / 三格各自的落点年柱 / 底部 take）
    for _t in ('viewBox="0 0 1680 644"', 'd="M0 202 H500"', 'd="M0 530 H500"',
               'd="M417 530 V250"', 'd="M840 530 V250"', 'd="M1597 530 V267.3"',
               'y="630">一个季度，就是去年一整年的两倍</text>'):
        assert _t in _secs[_I_P7], f'C17-⑦ svg 下移 84 未落地：{_t}'
    assert 'y="26">口径：一级市场披露融资额 · $B</text>' in _secs[_I_P7], 'C17-⑦ 顶行不该被搬'
    _cls(_I_P7, 'r17money')

    # ── C17-⑧ P15 96.5% 页 · 图灵两句压成一句 ───────────────────────────────
    #    ⚠️ 两处对 Colin 口述的**口径修正**（汇报里已标）：
    #      a) 他说的「150 年前」是**贝尔那条电话线**（P4 那页，1876 → 今年整 150 年），
    #         图灵是 **1950 / 76 年后**，这里不改成 150；
    #      b) 他说的「96.5% 的对话式智能体」口径不对 —— 96.5% 是 **2,475 通里未被识破的通话占比**
    #         （86 通被听出来），所以写「**96.5% 的真实通话**」，与同页 .cap 的口径完全对齐。
    _I_96 = _ix('2,475 通全量人工标注的真实外呼里')
    _r1(_I_96, '<div class="foot flow" style="--i:4">1950 年，图灵提出那个判别游戏的时候，'
               '设想的是一场五分钟的文字对谈。<br>76 年之后，这件事是在一条电话线上、'
               '由一个真的要把东西卖给你的人、在毫不知情的状态下完成的。</div>',
               '<div class="foot flow" style="--i:4">1950 年，图灵提出那场五分钟的判别游戏；'
               '76 年后，<b>96.5% 的真实通话</b>，悄悄通过了图灵测试。</div>')
    _cls(_I_96, 'r17p15')

    # ── C17-⑨ P24 Eval 全生命周期 · 删 Legora 那句 ──────────────────────────
    #    主句「从规划到回款，出题权一路没换过手」已经是落点，Legora 是举例再说一遍。
    _I_EV = _ix('同一把 Eval：对产品量<em>好坏</em>，对商业量<em>钱</em>')
    _r1(_I_EV, '<span class="s">法律 AI 公司 Legora 的做法值得抄：让客户的资深律师来定义'
               '「什么叫做对了」，产品团队只负责通过。谁定义正确，谁就掌握这段关系。</span>', '')
    assert 'Legora' not in _secs[_I_EV], 'C17-⑨ 未删净'
    _cls(_I_EV, 'r17p24')

    # ── C17-⑩ 四张 PART 幕卡 · 开头小字整块删 ───────────────────────────────
    #    Colin：「现在每个 part 的开头的小字都可以删除」。幕卡只留 PART 编号 / 英文名 / 幕名 /
    #    nav rail —— 一张幕卡就该只干一件事：告诉台下「进第几幕了」。
    #    ⚠️ PART 2 那块正是 C16-② 刚还原的两行，这一轮整块删（C16-② 的断言随之改判）。
    #    ⚠️ R12 加的资金流向页不是幕卡（它有 .wrap/.head，没有 .act），锚点用 .act 里的
    #       `<div class="cn spread">` 逐张定位，误伤不了它。
    _ACT_D = {
        '语法变了': '<div class="d flow" style="--i:4">被使用、被记住、被托付——三个「被」字，'
                    '主语一直是我们。<br>今年，主语换了。</div>',
        '被托付': '<div class="d flow" style="--i:4">被记住，靠的是一致性。被托付，靠的是可验证。<br>'
                  '这一幕只讲一件事：那把尺子怎么造。</div>',
        '双向奔赴 · 共事': '<div class="d flow" style="--i:4">三年了，一直是我们朝它走一步、再走一步。'
                           '这一幕，轮到它朝我们走。<br>我们交出去的是决定权，它交回来的必须是证据 '
                           '—— 走不回来的，不配叫同事。</div>',
        '人与组织': '<div class="d flow" style="--i:4">前面三幕讲的是「怎么造那把尺子」。<br>'
                    '最后一幕讲三件更难的事：把尺子写进价格里、谁去造它、以及组织要跟着变成什么样。</div>',
    }
    _N_ACT = 0
    for _cn, _d in _ACT_D.items():
        _i = _ix(f'<div class="cn spread" style="--i:3">{_cn}</div>')
        assert '<div class="act">' in _secs[_i], f'C17-⑩ 这不是一张幕卡：{_cn}'
        _r1(_i, '\n    ' + _d, '')
        assert '<div class="d flow"' not in _secs[_i], f'C17-⑩ 幕卡小字未删净：{_cn}'
        #    编号 / 英文名 / 幕名 / nav rail 一个都不许动
        for _keep in ('<div class="num flow"', '<div class="en settle"',
                      f'<div class="cn spread" style="--i:3">{_cn}</div>', '<div class="rail">'):
            assert _keep in _secs[_i], f'C17-⑩ 幕卡骨架被误伤（{_cn}）：{_keep}'
        _N_ACT += 1
    assert _N_ACT == 4, f'C17-⑩ 应处理四张幕卡，实际 {_N_ACT}'

    # ── C17-⑪ P4 PSTN 页 · 出处精化 ─────────────────────────────────────────
    #    R16 查证时发现：本仓 csagent.html 有一整页「原句照抄 · Cheeky Pint #27」就是这句，
    #    所以「2026-03 公开访谈」这个模糊出处可以换成确切集数（格式融入该行现有体例）。
    _I_P4 = _ix('You have all these fancy MCP things')
    _r1(_I_P4, '<div class="by">Bret Taylor · CEO of Sierra / Chairman of OpenAI · 2026-03 公开访谈</div>',
               '<div class="by">Bret Taylor · CEO of Sierra / Chairman of OpenAI · Cheeky Pint #27</div>')
    assert '2026-03 公开访谈' not in _secs[_I_P4], 'C17-⑪ 旧出处未清零'

    # ── C17-⑫ P44 —— R17 那一轮一个字不动（等 Colin 的门图）；R18 已把图换上，见 C18。

# ══════════════════════════════════════════════════════════════════════════════
# ── C18（2026-08-06 · R18 · 一处 · 页数不变 46）─────────────────────────────────
# 只有一处：P44「对组织说 · 单向门 / 双向门」把那两个 SVG 门（Colin 嫌太大没美感）
# 换成他用 GPT-image 生成的**单张门图**——左半是带紫色摆弧的双向弹簧门，右半是微开
# 露紫光缝的金库门，共一条基线，无文字。R17-⑫ 那条「P44 未动」的守门断言随之改判到这里。
#
# 资源纪律：图**进仓库**（scripts/assets/r18-doors.webp），build 时 base64 内联成 data URI ——
#   与母版那四张图（logo / cover / venue）同一个模式，归档出去的单文件 HTML 才能离线渲染；
#   文件缺失直接断言报错，保证 Colin 在自己终端上 clone 下来就能重建同样的产物。
# 压图账：原图 PNG 1672×941 / 1.27MB → 裁掉上下纯黑空边（131..800，长宽比 2.4993）
#   → 底色从 rgb(3,3,8) 压到纯 #000 → WebP q95 **78KB**（远在 400KB 预算内）。
#   2x 放大逐处看过门缝紫光与地面光斑：无色带（灰阶切片相邻步进 ≤2/255）。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    import base64
    _DOORS_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'r18-doors.webp')
    assert os.path.exists(_DOORS_F), \
        f'C18-① 门图资源缺失：{_DOORS_F} —— 该文件随仓库走，clone 下来才能重建这一页'
    _DOORS_B = open(_DOORS_F, 'rb').read()
    assert _DOORS_B[:4] == b'RIFF' and _DOORS_B[8:12] == b'WEBP', 'C18-① 门图不是 WebP'
    assert len(_DOORS_B) <= 400 * 1024, f'C18-① 门图超预算：{len(_DOORS_B)//1024}KB > 400KB'
    _DOORS_URI = 'data:image/webp;base64,' + base64.b64encode(_DOORS_B).decode('ascii')

    #    版面：CEO 那句（原本是 svg 里的 .lbl 文本）单独成行 → 门图 → 图下双标签 → land。
    #    两个标签的横向位置是**在图上量出来的**：左侧弹簧门（含两侧摆弧）横跨 109–799，
    #    中心 27.2%；右侧金库门（含敞开的圆弧门框）横跨 929–1488，中心 72.3%。
    #    用百分比 + translateX(-50%) 定位，图怎么缩放都对得上。
    #    ⚠️ 两段标签文字与 land / h2 / eyebrow 全部**一字未改**，只是从旧 svg 里挪出来重排。
    _I_D18 = _ix('对组织说：<em>放权</em>，从分清单向门与双向门开始')
    _cut1(_I_D18, '      <div class="fig">', '      </div>\n', f'''      <div class="dcap flow" style="--i:2">这条线画在哪 —— 是 CEO 的活，不是 AI 负责人的活</div>
      <div class="fig">
        <div class="doors rise" style="--i:3">
          <img src="{_DOORS_URI}" alt="左：可逆的双向弹簧门；右：不可逆的单向金库门">
          <div class="dl am" style="left:27.2%">可逆 · 双向门 · 放手做，不用批</div>
          <div class="dl co" style="left:72.3%">不可逆 · 单向门 · 先升级</div>
        </div>
      </div>
''')
    #    旧的两个 svg 门必须整块清零（矩形门板 / 摆动箭头 / 那条竖着的分界线 / 走线光点）
    for _old in ('<svg', '</svg>', 'class="stroke-am pkt"', 'd="M940 70 V552"',
                 'x="350" y="160"', 'x="1130" y="160"', 'font-size:42px'):
        assert _old not in _secs[_I_D18], f'C18-① 旧门图残留：{_old}'
    #    该留的一样不少（h2 / eyebrow / CEO 那句 / 两段标签 / land）
    for _keep in ('组织层 · ONE-WAY / TWO-WAY DOORS', '对组织说：<em>放权</em>，从分清单向门与双向门开始',
                  '这条线画在哪 —— 是 CEO 的活，不是 AI 负责人的活',
                  '可逆 · 双向门 · 放手做，不用批', '不可逆 · 单向门 · 先升级',
                  '<b>把权放给 high agency 的人</b>——他们会带着 Agent，把结果一起做出来。'):
        assert _keep in _secs[_I_D18], f'C18-① 该保留的丢了：{_keep}'
    _cls(_I_D18, 'r18doors')

# ══════════════════════════════════════════════════════════════════════════════
# ── C19（2026-08-06 · R19 · 五处 · 页数不变 46）─────────────────────────────────
# Colin 看着线上 R18 提的五处：
#   ① P7 展示形式改回「带时间轴的曲线」，**数据一个不动**；顺手删掉「三格各用各的尺」那句。
#      ⚠️ 红线：不许回双轴（R16 点名的视觉说谎）→ 定为**单一时间轴 + 对数纵轴 + 三条曲线**。
#   ② 五张金句页的 eyebrow（`观点页 · 嘉宾金句 · 0X`）全删，页面只剩主文 + 英文小行 + 署名。
#   ③ 金句 02 署名 `OpenAI 前 CPO` → `OpenAI ex CPO`（Colin R13 原话本来就是 ex CPO）。
#   ④ P31 三段教训正文删（卡片只剩标题）+ 教训 03 标题改「也必须写进 SOP 流程里」。
#   ⑤ P44 删 CEO 那行 + 门图从 1380 收到 1180。
# 取页一律**内容锚定**（沿用 _ix），不信页号；母版 62 页仍然只读。
# ══════════════════════════════════════════════════════════════════════════════
if V2:
    # ── C19-① P7 · 三格小倍数 → 单轴对数三线图（数据一个不动）─────────────────
    #    为什么是对数轴而不是回双轴：三条赛道量级差 ~860 倍（0.21 ↔ 178）。
    #      · 双轴 = R16 已经判死的视觉说谎（两套刻度的对齐是任意的，图会凭空造相关性）；
    #      · 单线性轴 = 写代码与对话式两条会被压成贴着 0 的两条平线，「变化」完全看不见；
    #      · **单轴对数** = 一根尺、一套网格，量级差用「每格 ×10」表达，三条线同图可比**形状**。
    #    对数轴的唯一代价是读者得知道它是对数的 —— 用三件事补偿：角落明写「纵轴 · 对数刻度」、
    #    网格线本身就是十倍阶梯并逐条标 $0.1B/$1B/$10B/$100B、每个点直接标值（点标即刻度）。
    #
    #    坐标账（viewBox 0 0 1680 600）：y = 400 − 100·log10(v)，即**一格 100px = ×10**；
    #      网格 $100B→200 · $10B→300 · $1B→400 · $0.1B→500；x 三刻度 300 / 725 / 1150。
    #      基础模型 31.4→250.3 · 88.9→205.1 · 178→175.0
    #      AI 写代码 1.59→379.9 · 3.25→348.8 · 0.2075→468.3
    #      对话式   1.59→379.9 · 1.94→371.2 · 1.82→374.0
    #      ⚠️ 2024 两条**真的重合**（都是 $1.59B）—— 不是画错，所以只标一个值 + 一行小注说明；
    #         两条线从同一点分岔，正好把「同一起跑线」这层意思画了出来。
    #      故事红利（Colin 点名要看得见的两个动作）：
    #         · 写代码 2025 冲顶（348.8）→ 2026 跳水（468.3），跨过整整 1.2 个数量级；
    #         · 与对话式在 x≈807 处**交叉**，2026 对话式（374.0）反超写代码（468.3）。
    #    描边动画 --len 逐条按贝塞尔实长采样算过：fnd 854 / cod 871 / cnv 850 → 一律给 +6 的余量。
    _I_P7b = _ix('近三年，钱的三次落点')
    _sa19 = _secs[_I_P7b].index('<svg'); _sb19 = _secs[_I_P7b].index('</svg>') + 6
    assert 'viewBox="0 0 1680 644"' in _secs[_I_P7b][_sa19:_sb19], 'C19-① P7 旧三格 svg 定位失败'
    _secs[_I_P7b] = _secs[_I_P7b][:_sa19] + '''<svg viewBox="0 0 1680 600" width="1680" fill="none">
          <!-- ① 顶行：左 = 单一口径；右 = 刻度性质（角落小字，不写成整句解释） -->
          <g class="pop" style="--i:0">
            <text class="lbl" x="0" y="26">口径：一级市场披露融资额 · $B</text>
            <text class="lbl" x="1680" y="26" text-anchor="end">纵轴 · 对数刻度</text>
          </g>

          <!-- ② 十倍阶梯网格 + 基线：网格线本身就是刻度，逐条标出来 -->
          <g class="pop" style="--i:1">
            <path class="gd" d="M250 200 H1180 M250 300 H1180 M250 400 H1180 M250 500 H1180"/>
            <path class="axb" d="M250 520 H1180"/>
            <text class="lbl dec" x="222" y="207" text-anchor="end">$100B</text>
            <text class="lbl dec" x="222" y="307" text-anchor="end">$10B</text>
            <text class="lbl dec" x="222" y="407" text-anchor="end">$1B</text>
            <text class="lbl dec" x="222" y="507" text-anchor="end">$0.1B</text>
            <text class="lbl yr" x="300" y="556" text-anchor="middle">2024</text>
            <text class="lbl yr" x="725" y="556" text-anchor="middle">2025</text>
            <text class="lbl yr" x="1150" y="556" text-anchor="middle">2026</text>
            <text class="sm" x="1150" y="584" text-anchor="middle">至今</text>
            <text class="lbl" x="250" y="584">2026 至今：基础模型截至 3-31（Q1）· 写代码与对话式截至 7-02（H1）</text>
          </g>

          <!-- ③ 基础模型（白粗）：31.4 → 88.9 → 178，三年都是最大头，一直在涨 -->
          <path class="ln fnd dw" style="--len:860;--i:2" d="M300 250.3 C 448.75 250.3, 576.25 205.1, 725 205.1 C 873.75 205.1, 1001.25 175, 1150 175"/>
          <circle class="dot fnd pop" style="--i:3" cx="300" cy="250.3" r="6"/>
          <circle class="dot fnd pop" style="--i:3" cx="725" cy="205.1" r="6"/>
          <circle class="dot fnd pop" style="--i:4" cx="1150" cy="175" r="8.5"/>
          <g class="pop" style="--i:3">
            <text class="txt val" x="300" y="232" text-anchor="middle">$31.4B</text>
            <text class="txt val" x="725" y="187" text-anchor="middle">$88.9B</text>
          </g>
          <g class="pop" style="--i:4">
            <path class="lead fnd" d="M1166 175 H1190"/>
            <text class="ttl" x="1200" y="160">基础模型</text>
            <text class="big" x="1200" y="220">$178B</text>
            <text class="sm anno" x="937" y="160" text-anchor="middle">一个季度，就是去年一整年的两倍</text>
          </g>

          <!-- ④ AI 写代码（灰细）：1.59 → 3.25 → 0.2075 —— 2025 冲顶，2026 跳水 1.2 个数量级 -->
          <path class="ln cod dw" style="--len:878;--i:5" d="M300 379.9 C 448.75 379.9, 576.25 348.8, 725 348.8 C 873.75 348.8, 1001.25 468.3, 1150 468.3"/>
          <circle class="dot cod pop" style="--i:6" cx="300" cy="379.9" r="6"/>
          <circle class="dot cod pop" style="--i:6" cx="725" cy="348.8" r="6"/>
          <circle class="dot cod pop" style="--i:7" cx="1150" cy="468.3" r="8.5"/>
          <g class="pop" style="--i:6">
            <text class="txt val" x="725" y="331" text-anchor="middle">$3.3B</text>
            <text class="sm anno" x="725" y="296" text-anchor="middle">一轮钱在 2025 发完 · Cursor 一家占 98%</text>
          </g>
          <g class="pop" style="--i:7">
            <path class="lead cod" d="M1166 468.3 L1190 483"/>
            <text class="ttl" x="1200" y="474">AI 写代码</text>
            <text class="big" x="1200" y="534">$0.2B</text>
          </g>

          <!-- ⑤ 对话式 AI（amber 粗，今年的主角）：1.59 → 1.94 → 1.82；
               与写代码在 2024 同一点出发、在 x≈807 交叉，2026 反超。整组 data-step=1 -->
          <g data-step="1">
            <path class="ln cnv dw" style="--len:856;--i:0" d="M300 379.9 C 448.75 379.9, 576.25 371.2, 725 371.2 C 873.75 371.2, 1001.25 374, 1150 374"/>
            <circle class="dot cnv pop" style="--i:1" cx="300" cy="379.9" r="6"/>
            <circle class="dot cnv pop" style="--i:1" cx="725" cy="371.2" r="6"/>
            <circle class="dot cnv pop" style="--i:2" cx="1150" cy="374" r="8.5"/>
            <g class="pop" style="--i:1">
              <text class="txt val" x="300" y="412" text-anchor="middle">$1.6B</text>
              <text class="sm anno" x="300" y="446" text-anchor="middle">写代码与对话式，2024 从同一点出发</text>
              <text class="txt val fill-am" x="725" y="404" text-anchor="middle">$1.9B</text>
            </g>
            <g class="pop" style="--i:2">
              <path class="lead cnv" d="M1166 374 H1190"/>
              <text class="ttl" x="1200" y="358">对话式 AI</text>
              <text class="big fill-am" x="1200" y="418">$1.8B</text>
              <text class="sm anno fill-am" x="1000" y="345" text-anchor="middle">半年，已经追平去年一整年</text>
            </g>
          </g>
        </svg>''' + _secs[_I_P7b][_sb19:]
    #    删句 + 旧三格图元清零 + 数据一个没动（九个数里 $1.6B 因两条重合只标一次 → 页上八个值标）
    assert '三条赛道量级差百倍' not in _secs[_I_P7b], 'C19-① 该删的那句未清零'
    for _old in ('class="col ', 'class="pr"', '>至今</text>\n            <text class="sm anno"'):
        assert _old not in _secs[_I_P7b], f'C19-① 旧三格图元残留：{_old}'
    for _v in ('>$31.4B</text>', '>$88.9B</text>', '>$178B</text>', '>$3.3B</text>',
               '>$0.2B</text>', '>$1.6B</text>', '>$1.9B</text>', '>$1.8B</text>'):
        assert _secs[_I_P7b].count(_v) == 1, f'C19-① 数值应逐个各一处：{_v}'
    _cls(_I_P7b, 'r19money')

    # ── C19-② 五张金句页 · eyebrow 整块删 ───────────────────────────────────
    #    `观点页 · 嘉宾金句 · 0X` 是页型元信息，台下不需要；删完页面只剩
    #    金句主文（+ 英文小行）+ 署名。删后 .mq 的 justify-content:center 自动把引文块回中。
    #    ⚠️ 全 deck 的「金句仍是五张」从此**凭内容认**，不再凭编号 eyebrow（收口断言随之改判）。
    _MQ19 = []
    for _n, _anchor in (('01', '我们叫了它三年 Agent（代理人）——'),
                        ('02', 'Writing evals is the most important'),
                        ('03', 'One of the biggest fallacies in AI'),
                        ('04', '围栏不是拦住它，'),
                        ('05', '没有撤回键。')):
        _i = _ix(_anchor)
        _r1(_i, f'\n    <div class="mark flow" style="--i:0">观点页 · 嘉宾金句 · {_n}</div>', '')
        assert 'class="mark' not in _secs[_i], f'C19-② 金句 {_n} 的 eyebrow 未删净'
        _cls(_i, 'r19mq')
        _MQ19.append(_i)
    assert len(set(_MQ19)) == 5, 'C19-② 五张金句页应互不相同'

    # ── C19-③ 金句 02 署名 · 前 CPO → ex CPO ────────────────────────────────
    #    Colin R13 给的原话本来就是 ex CPO（C4 当年把母版的 `OpenAI CPO` 改成中文「前 CPO」，
    #    这一轮回到他的原写法）。全场 Weil 仅此一处，改完即全场一致。
    _r1(_MQ19[1], '<div class="s rise" style="--i:5">Kevin Weil · OpenAI 前 CPO</div>',
                  '<div class="s rise" style="--i:5">Kevin Weil · OpenAI ex CPO</div>')
    assert 'OpenAI 前 CPO' not in _secs[_MQ19[1]], 'C19-③ 旧署名未清零'

    # ── C19-④ P31 · 三段教训正文删 + 教训 03 改题 ────────────────────────────
    #    卡片只剩标题：三句标题本身已经是三条教训，正文是把标题又展开说一遍。
    #    教训 03「也必须在纸上」→「**也必须写进 SOP 流程里**」—— 「纸上」太文学，
    #    SOP 是组织侧能直接执行的落点（与第四幕的授权语法同一条线）。
    _I_C3b = _ix('两道围栏：提示词拦话术，')
    for _d in ('<div class="d">高敏权限不能只靠提示词和策略文档约束。它们写得再好，也不是'
               '<b>可执行的边界</b>——模型不会因为你写了「不要」就做不到。</div>',
               '<div class="d">容器、沙箱、权限边界、人工升级通道——这四件是<b>工程</b>，'
               '不是流程。写在架构图上，不是写在 Wiki 上。</div>',
               '<div class="d">授权不能只活在代码里，还要白纸黑字写清六件事：'
               '<b>替谁做、做什么、到哪里为止、如何披露、错了怎么办、怎么收回</b>'
               '——写不出来，就是还没想清楚。这六件事，第四幕会变成组织的授权语法。</div>'):
        _r1(_I_C3b, _d, '')
    _r1(_I_C3b, '<div class="t">也必须在纸上</div>', '<div class="t">也必须写进 SOP 流程里</div>')
    assert '<div class="d">' not in _secs[_I_C3b], 'C19-④ 教训卡应只剩标题'
    assert '六件事' not in _secs[_I_C3b] and '也必须在纸上' not in _secs[_I_C3b], 'C19-④ 未删净/未改题'
    #    悬空检查：第四幕「授权六件事」那页原来回指的是「第三幕写给 Agent 的授权六件事」
    #    （C8-⑤ 改的幕序），指的是**幕**不是**案例 03**，与本页无关 —— 一个字都不用动。
    #    全 deck 仍有「六件事」的地方只剩那一页，且它自己把六件事写全了，不依赖本页。
    _cls(_I_C3b, 'r19case3')

    # ── C19-⑤ P44 · 删 CEO 那行 + 门图收比例 ────────────────────────────────
    #    a) `这条线画在哪 —— 是 CEO 的活，不是 AI 负责人的活` 整行删（R18 才从旧 svg 里挪出来的
    #       那一行 mono caption）。h2 / eyebrow / 双标签 / land 一个字不动。
    _I_D19 = _ix('对组织说：<em>放权</em>，从分清单向门与双向门开始')
    _r1(_I_D19, '      <div class="dcap flow" style="--i:2">这条线画在哪 —— 是 CEO 的活，'
                '不是 AI 负责人的活</div>\n', '')
    assert 'dcap' not in _secs[_I_D19] and 'CEO 的活' not in _secs[_I_D19], 'C19-⑤a CEO 那行未删净'
    #    b) 图 1380 → 1180（高 552 → 472）。两段标签是 % 定位（27.2% / 72.3%），随图等比走，
    #       一个数都不用改 —— R18 当初就是为这一天写成 % 的。
    _cls(_I_D19, 'r19doors')

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
    CONF_CSS += C16_CSS     # C16 · R16 页级档（必须排在 C13/C14/C15 之后：.r13mq/.r15mq/.r14money 三处都靠后写者胜）
    CONF_CSS += C17_CSS     # C17 · R17 页级档（必须排在 C16 之后：.r16money / .r15end 等同页档靠后写者胜）
    CONF_CSS += C18_CSS     # C18 · R18 页级档（P44 门图，必须排在 C9 的 .r9p43 之后：同页两个类，后写者胜）
    CONF_CSS += C19_CSS     # C19 · R19 页级档（必须排在 C17/C18 之后：.r17money / .r18doors 同页档靠后写者胜）
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
# ⚠️ R19 改判：C19-④ 把 P31 三张教训卡的正文整块删了（卡片只剩标题），「这六件事，第四幕会变成
#    组织的授权语法」随之下台 —— 从 V2 的正向名单里摘出（负向账在 C19 段）。它原本只是**前向指涉**，
#    第四幕那页自己把六件事写全了，不依赖本页，所以不悬空。55 页版那句仍在，照旧守着。
_MK6 = ["事前授权", "批动作类别，不批每一句话", "把权放给 high agency 的人"]
if not V2:
    _MK6.append("这六件事，第五幕会变成组织的授权语法")
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
# ⚠️ R17 改判：C17-③ 把 V2 的这条 eyebrow 换成了「ONE LINE EACH · 越往上，答案越短，也越重」
#    （旧 h2 降级进来），55 页版仍是「全场收束 · ONE LINE EACH」——两版共用的锚点因此收窄成
#    两版都保留的 `ONE LINE EACH`（全场唯一）。四资产带的正向账不变。
assert s.count('ONE LINE EACH') == 1, "C6 · P54 锚点 ONE LINE EACH 应全场唯一"
_p54 = s[s.index('ONE LINE EACH'):]
_p54 = _p54[:_p54.index('</section>')]
for _w in ('>评测</text>', '>岗位</text>', '>结果生意</text>', '>放权决策机制</text>'):
    assert _w in _p54, f"C6 · P54 四资产带缺失：{_w}"

if V2:
    # ── C8 内容在位 / 陪伴章清零 / 视觉第一刀在位 ────────────────────────
    # ⚠️ R15 回归账（改动累计 15 轮后的第四次挪账）：C15-③ 把北极星页 note 整段删了，
    #    「下午 AIoT 专场整场拆开讲」「直接从「被托付」进」两句随之下台 —— 下午专场的交接
    #    改由分水岭页 eyebrow 与图注承担（下面两条），所以这两句从正向名单里摘出。
    #    C15-① 换了两张主标题，「这不是一个垂类」「预测还在打架」同理换成新主标题的锚点。
    # ⚠️ R17 回归账（第五次挪账）：C17-⑩ 把四张 PART 幕卡的开头小字整块删了 ——
    #    「前面三幕讲的是」（PART 4 幕卡）随之下台；C17-⑥ 把 P9 的预测对照整块删了 ——
    #    「这道题第二、三幕来解」随之下台。两条都从**正向**名单摘出（负向账在 C17 段）。
    #    幕序本身仍由 rail 四站与 PART 标题守着（下面两条断言），不会因此悬空。
    for _mk in ("陪伴那条线走「熟人 → 伙伴」（下午专场）", "消费级 · 陪伴 —— 下午 AIoT 专场那条",
                "PART 2 · 被托付", "PART 3 · 双向奔赴", "PART 4 · 人与组织",
                "对话式 AI 的钱，<em>流向了哪里</em>", "<em>正在悄然发生</em>",
                # ⚠️ R19 改判：C19-② 把五张金句页的 eyebrow（`观点页 · 嘉宾金句 · 0X`）全删了 ——
                #    「金句仍是五张」从此**凭内容认**（五句主文各一处，正向账在 C19 段），
                #    这条编号锚点从正向名单摘出；负向的「· 06」仍留在下面守着。
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
                # ⚠️ R17 改判：C17-④ 把终页那张尺子图整张重画了（外/内两列八条清单整块删，
                #    负 y 区随之消失，viewBox 0 -177 1680 646 → 0 0 1680 640），
                #    这条几何断言作废；新几何的正向账在 C17 段。
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
                # P8 · 企业侧新数据（五条读数本身不动；⚠️ **R17 改判**：C17-⑥ 按 P7 体例把
                #      这一页的 SOURCE 行瘦身成**只留机构名**（n= 与月份细节全去，Gartner 随
                #      预测对照一起撤），所以三条「逐条标源与年份」的断言作废 ——
                #      新 foot 的正向账（五家机构名齐全）在 C17 段。）
                '>66%</text>', '>70%</text>', '>91%</text>', '>15–20%</text>', '>49%</text>',
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
                # ⚠️ R17 改判：C17-②c 把这张链路图的 viewBox 加高 12（260 → 272）修掉一处
                #    2px 文字越界，几何数变了 —— 只留「事件叙述沉底」那条与画法无关的账。
                'class="old tail rise"',
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
    # ⚠️ R17 改判：C17-②a 把这一页的 `.note.co`（「我不想制造恐慌…」）整段删了，
    #    「叙述沉在 note 之后」这条相对位置断言失去参照物 —— 作废。
    #    「事件块沉在最底部」这层意思改由上面那条（图在事件块之前）+ C17 段的正向账守。
    assert 'class="note co' not in _p30, "C17-②a P30 的 note 应已整段删"
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
    #    ⓒ 三条赛道的名在页上（C14 把三条层带重做成双轴时间图，C16 又把双轴整张换成三格小倍数：
    #       ⚠️ **R16 改判**：三条线的「数」不再由这里守 —— 2.1 / ≈0.7 / 2.2+ 三个数经重查全部作废，
    #       $178B / $1.6B 在小倍数里各出现两次（表头终值大字 + 柱上值标），count==1 不再成立。
    #       逐条数值账（含来源与截点）整体搬到下面的 C16 段；这里只守三条赛道的名各一处。
    #       同理，「走线光点 .pkt」是曲线图的图元，柱图上没有线可走 —— 一并搬到 C16 段作反向断言。）
    for _b in ('>基础模型</text>', '>AI 写代码</text>', '>对话式 AI</text>'):
        assert _pf.count(_b) == 1, f"C12 · 页上赛道名缺失或重复：{_b}"
    #    ⓓ ⚠️ **R17 改判**：C17-⑦ 把这一页的 note 整段删了（图自己已经把三拍说清楚），
    #       大泛类两翼（ElevenLabs / Sierra）的明细随之下台 —— 改由**口播**承担，
    #       全文留档在设计文档 R17 段。这条正向断言作废，负向账（note 已清零）在 C17 段。
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

    # ⚠️ **R18 起的通用护栏**：C18 把一张 78KB 的门图 base64 内联进了 P44，
    #    base64 是纯 ASCII 乱码，全 deck 的**英文短串**负向扫描（'L0' / 'Legora' / 'Gartner' …）
    #    会被它随机命中而误报。所以凡是「整本扫英文短串」的断言，一律先把 data-URI 载荷抹掉。
    #    （中文串不受影响，base64 里不会出现中文。）
    def _nouri(t):
        return re.sub(r'data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+', 'data:image/…', t)

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

    #    ⓖ ⑥「perfect human」金句页：英文逐字仍在（R13 换上来的那句一个字没动）
    #       ⚠️ **R16 改判**：这一页 R16 改成了「中上英下」+ 出处改正 ——
    #       ⒜ 中文从一整行拆成两行 `<i>`（80px 中文金句体系），contiguous 的整句不再存在；
    #       ⒝ 署名从「Bret Taylor · Sierra CEO / OpenAI 董事长」改成 Des Traynor（这句本来就
    #          不是 Bret 的，R13 当年只写了「出处口径留给 Colin 复核」）。
    #       两条正向账（中文两行 + 新署名 + 出处行）搬到下面的 C16 段；这里只守英文逐字不变。
    _pmq = _sec_of('One of the biggest fallacies in AI')
    for _mk in ('is people compare it with this perfect human', 'that does not exist.&#8221;'):
        assert _mk in _pmq, f"C13-⑥ 金句页元素缺失：{_mk}"
    # ⚠️ R19 改判：C19-② 删掉了金句页的 eyebrow 编号 —— 这一页「是不是金句 03」改由
    #    **内容 + 顺序**认（英文原句 + Des 署名，正向账在 C16/C19 段），编号锚点从这里摘除。

    #    ⓗ ⑦ 围栏 Part 点睛：新金句在位，且仍挂在金句 04 上
    _pfc = _sec_of('围栏不是拦住它，')
    for _mk in ('是放出它。</i>',
                '提示词 + 产品架构，围出一条不用人扶的执行流——围栏有多硬，敢交给它的 OKR 就有多重。'):
        assert _mk in _pfc, f"C13-⑦ 新金句元素缺失：{_mk}"
    # ⚠️ R19 改判：同上 —— 编号 eyebrow 已删，这一页凭「围栏不是拦住它，是放出它。」认。

    #    ⓘ 页级档位类必须全部挂上且 CSS 有定义（r13ask 已随 C15-⑦ 撤回第二拍一并摘掉）
    assert 'class="slide' in s and not re.search(r'class="slide[^"]*\br13ask\b', s), \
        "C15-⑦ r13ask 档位类应已随第二拍一并摘除"
    for _c in ('r13bell', 'r13p5', 'r13case', 'r13mq', 'r13fence'):
        assert len(re.findall(rf'class="slide[^"]*\b{_c}\b', s)) == 1 and f'.{_c} ' in s, \
            f"C13 · 档位类未挂/未定义：{_c}"
    #    ⓙ 页数不变 46（最终页数断言在写盘处，这里只守金句编号 01–05 不变）
    # ⚠️ R19 改判：编号 eyebrow 全删 —— 「仍是五张」改由五句主文各一处来守（C19 段 ⓒ）。
    #    （只数正文：C19_CSS 那段档位注释里也写了这个词，不算页内容）
    assert '观点页 · 嘉宾金句' not in ''.join(re.findall(r'<section class="slide.*?</section>', s, re.S)), \
        "C19-② 金句页编号 eyebrow 应已全场清零"

    # ── C14 · R14 两处 ─────────────────────────────────────────────────────
    #    ① P2 讲台在 / 舞台零（正文范围内；母版的 CSS 注释「固定舞台」不在页里，不受影响）
    _pp2 = _sec_of('第三次，站上同一个讲台')
    assert '舞台' not in _pp2, "C14-① P2 仍有「舞台」残留"
    assert '回到讲台' in _pp2, "C14-① P2 eyebrow「回到讲台」丢了"
    assert '第三次，站上同一个舞台' not in s, "C14-① 全场不应再有「站上同一个舞台」"
    _n_slide_stage = sum(1 for _x in re.findall(r'<section class="slide.*?</section>', s, re.S) if '舞台' in _x)
    assert _n_slide_stage == 0, f"C14-① 仍有 {_n_slide_stage} 页正文含「舞台」"

    #    ② 钱流向页 · 双轴时间图
    #    ⚠️ **R16 改判**：这张双轴时间图整张作废（Colin 三条质疑全部成立 —— 左 0–200 / 右 0–4
    #       把 $3.3B 画得比 $178B 还高；对话式那条的取数残缺；融资额与 Cursor ARR 混在一张图）。
    #       R16 换成三格小倍数，所以 ⓐ–ⓖ（双轴骨架 / 两套刻度 / 三条曲线 / 走线光点 / 渐变面积 /
    #       终点名牌 / 值标五个）与 ⓘ 的 foot 逐字账**全部从这里摘除**，正向账搬进下面的 C16 段。
    #       仍留在这里的是三条**不随画法变化**的账：档位类挂载 · 三条层带旧图元清零 · 旧长 foot 清零
    #       · eyebrow/h2 保留 · data-step ≤2。（R14 的双轴图元素改由 C16 段做反向断言。）
    _pm = _sec_of('近三年，钱的三次落点')
    assert len(re.findall(r'class="slide[^"]*\br14money\b', s)) == 1 and '.r14money ' in s, \
        "C14-② 档位类未挂/未定义：r14money"
    #       ⓗ 三条层带的旧图元必须清零（英文层名 / 三段带 / 带宽示意）
    for _old in ('>FOUNDATION MODELS</text>', '>CODING</text>', '>CONVERSATIONAL AI</text>',
                 'class="stroke dw"', 'class="stroke-am dw"', '>$2B ARR</text>', '>&#8776;$2.2B</text>',
                 '同一层的两翼'):
        assert _old not in _pm, f"C14-② 三条层带旧图元未清：{_old}"
    #       ⓘ foot 一行体例保留（逐字账随 R16 换源改判到 C16 段）；旧的长口径行全文仍须清零
    for _old in ('New Market Pitch 2026-07', 'PYMNTS 2025-06', 'SiliconANGLE 2026-05',
                 'Newcomer 2026-02', 'Crunchbase 2026-04', 'CB Insights《State of AI 2025》2026-01',
                 '本页自算，不是全类别口径', '带宽为量级示意，非等比', 'Cartesia $100M', 'Parloa $350M'):
        assert _old not in s, f"C14-② 旧长 foot 口径未撤下：{_old}"
    #       ⓙ eyebrow / h2 原样保留（⚠️ **R17 改判**：note 整段随 C17-⑦ 删掉，
    #          「这笔钱在这一层内部又分给了谁——下一页拆开看」这条正向断言作废；
    #          「下一页拆开看」的衔接改由页序本身承担 —— P7 图 → P8 六卡就是那一拆。）
    for _keep in ('产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走',
                  '近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>'):
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
                # ⚠️ R16 改判：④「被记住，靠的是一致性。被托付，靠的是可验证。」原本在这条负向名单里
                #    （R15 把它从幕卡上换掉了）。Colin 澄清 R15-④ 那句本意是放金句页，
                #    R16-② 把幕卡首行**退回这句原文** —— 它重新成为正向内容，从负向名单摘除，
                #    正向账（幕卡首行 + 导航行）搬进下面的 C16 段。
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
    # ⚠️ **R17 改判**：C15-①b 当年把「预测还在打架」从主标题降到 note 时留了它一条命；
    #    C17-⑥ 这一轮把那整块 note 删了（Colin 点名），所以「对照仍须留在 note 里」作废 ——
    #    这一页从此只讲「已经发生的采购」，不再背预测的对照（负向账在 C17 段）。
    assert '企业侧 · 这四个数都已经发生' in _p9n, "C15-①b 渗透页错位"
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

    #    ⓔ ④ PART 2 幕卡 —— ⚠️ **R16 改判：整条作废**。
    #       R15 把「我们叫了它三年 Agent（代理人）——今天，它终于开始代理了。」放上了幕卡；
    #       Colin 2026-08-06 澄清那句本意是**金句页**，R16-① 把它搬到金句 01、R16-② 把幕卡
    #       首行退回 R15 之前的原文。幕卡两行的正向账整体搬进下面的 C16 段。

    #    ⓕ ⑤⑥ 两处删段 + 档位类
    _pld = _sec_of('工具 → 实习生 → 外包 → 专家 → <em>合伙人</em>')
    assert '<div class="land' not in _pld and '<div class="g4">' in _pld, "C15-⑤ land 未整段删"
    _pe1 = _sec_of('你的 demo 在骗你</h2>')
    assert '<div class="foot' not in _pe1 and '你的 demo 里全是前一种题' in _pe1, "C15-⑥ foot 未整句删"
    for _c in ('r15ladder', 'r15eval1'):
        assert len(re.findall(rf'class="slide[^"]*\b{_c}\b', s)) == 1 and f'.{_c} ' in s, \
            f"C15 · 档位类未挂/未定义：{_c}"

    #    ⓖ ⑦ Weil 只在金句 02（英文逐字与署名行两轮都没变；⚠️ **R16 改判**：R16-③ 把这一页
    #       改成「中上英下」，中文从一整行拆成两行 `<i>`，所以 contiguous 的中文整句不再存在 ——
    #       中文两行的正向账搬进下面的 C16 段，这里只守英文逐字 / 编号 / 署名 / 全场仅一处。）
    _pw = _sec_of('Writing evals is the most important')
    # ⚠️ R19 改判两条：编号 eyebrow 已删（C19-②）；署名 `OpenAI 前 CPO` → `OpenAI ex CPO`（C19-③）。
    #    这里只守英文逐字；编号与署名的正向账搬到 C19 段。
    for _mk in ('thing a PM can do in the AI era.&#8221;',):
        assert _mk in _pw, f"C15-⑦ 金句 02 元素缺失：{_mk}"
    #       「全场仅一处」只数正文（C15_CSS 里那行档位注释也写了 Kevin Weil，不算页内容）
    _slides_txt = _nouri(''.join(re.findall(r'<section class="slide.*?</section>', s, re.S)))
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

    #    ⓘ ⑩ 终检：幕序/课序/金句序仍自洽
    #    ⚠️ **R16 改判**：⑩a「2026 光是上半年这几笔」随 C16-⑤ 的 note 整段重写而作废
    #       （新 note 按重查后的数据改写，不再有「这几笔」这个数不出来的量词）。
    #       负向的「这五笔」仍留在上面 ⓐ 的 cut 名单里。
    # ⚠️ R19 改判：编号 eyebrow 全删 —— 「五张」的账见 C19 段 ⓒ（五句主文各一处 + 五个档位类）。
    for _c in '一二三四':
        assert f'>Eval 第{_c}课</div>' in s, f"C15-⑩b 课序缺失：第{_c}课"

    # ── C16 · R16 五处 ─────────────────────────────────────────────────────
    #    ⓐ 负向：被换下 / 被作废的整段必须查无此句
    for _mk in ('兑现的，', '不是模型更聪明了。', '是「谁负责」这件事，',        # ① 旧金句 01 主文
                '终于有了答案。',
                # ⚠️ ④ 旧署名「Bret Taylor · Sierra CEO / OpenAI 董事长」**不能进全场负向名单** ——
                #    P43「Hyper high-agency」那条真引文用的是同一行署名。金句 03 页内的清零
                #    在下面 ⓒ 段按页断言（_pq3 里既无 Bret Taylor 也无「2026-03 公开访谈」）。
                '左右两轴量级不同',                                            # ⑤ 双轴防误读小注（双轴没了）
                '>基础模型 $B</text>', '>Coding / 对话式 $B</text>',            # ⑤ 两个轴标
                'id="r14conv"',                                                # ⑤ 双轴图那层渐变面积
                # ⚠️ **R19 改判**：`class="ln * dw"` / `class="lead ` 三条曲线与名牌引线的类名
                #    从负向名单摘除 —— R19 把这一页换回了**单轴对数三线图**，线与引线名正言顺地回来了。
                #    R16 真正判死的是「双轴」，负向账因此收窄成上面那三条（两个轴标 + 防误读小注 + 渐变面积）
                #    加下面 C19 段按页断言的「零第二把尺」。
                # ⚠️「走线光点 .stroke-am pkt」全 deck 十三页都在用，不能进全场负向名单 ——
                #    钱流向页内的清零在下面 ⓓ 段按页断言。
                'Cursor ARR $2B', '2026 转向收入兑现',                          # ⑤ ARR 混入融资图（连 note 口径一并撤）
                '>$2.1B</text>', '>&#8776;$0.7B</text>', '>$2.2B+</text>',      # ⑤ 被重查推翻的三个数
                '2026 光是上半年这几笔',                                        # ⑤ 旧 note 的量词
                'CB Insights《State of AI 2025》'):                            # ⑤ 旧 foot 的来源（本轮全部换源）
        assert _mk not in s, f"C16 · R16 该删/该改未落地：{_mk}"
    #    ⚠️「Bret Taylor」这一轮只从金句 03 撤下，**其余三处一个都不许连坐**（全是核过的真引文）：
    #       P4「English over PSTN」/ P23 Sierra 官方博客「不是 token 的钱」/ P43「Hyper high-agency」。
    _slides16 = _nouri(''.join(re.findall(r'<section class="slide.*?</section>', s, re.S)))
    #    只数**页面上看得见的**署名（P4 的 svg 上方有一条源码注释也写了 Bret Taylor，不算页内容）
    _visible16 = re.sub(r'<!--.*?-->', '', _slides16, flags=re.S)
    _n_bret = _visible16.count('Bret Taylor')
    assert _n_bret == 3, \
        f"C16-④ 全场 Bret Taylor 应剩三处真引文（PSTN / Sierra 博客 / High Agency），实际 {_n_bret}"
    for _keep in ('You have all these fancy MCP things', 'you pay for <b>business outcomes delivered</b>',
                  'Hyper high-agency people who really deeply care.'):
        assert _keep in _slides16, f"C16-④ 别处的 Bret Taylor 真引文被误伤：{_keep}"

    #    ⓑ ① 金句 01 换血（全场「我们叫了它三年」恰好一处）
    #    ⚠️ **R17 改判**：②「PART 2 幕卡首行退回原文」这一条**整条作废** ——
    #       C17-⑩ 把四张 PART 幕卡的开头小字**整块删了**（Colin：每个 part 的开头小字都可以删），
    #       所以 R16 刚还原的那两行也一并下台。幕卡的正向账（骨架四件在、小字清零）搬进 C17 段。
    #    ⚠️ **R19 改判**：C19-② 删掉了编号 eyebrow —— 取页锚点从编号换成主文首行（内容锚定）。
    _pq1 = _sec_of('我们叫了它三年 Agent（代理人）——')
    assert '<i class="rise" style="--i:1">我们叫了它三年 Agent（代理人）——</i>' in _pq1 and \
           '<i class="rise" style="--i:2">今天，它终于开始代理了。</i>' in _pq1, "C16-① 金句 01 新主文未落地"
    assert '所以今年这一场，讲的不是能力，是责任。' in _pq1, "C16-① 承句不该被动"
    assert _slides16.count('我们叫了它三年') == 1, "C16-① 全场「我们叫了它三年」应恰好一处"

    #    ⓒ ③④ 两张金句页「中上英下」：中文在 .q（中文金句体系）、英文降为下方 mono 一行
    for _cn, _anchor, _en, _sig in (
        # ⚠️ **R19 改判**：取页锚点从编号 eyebrow 换成英文原句（C19-②）；
        #    金句 02 的署名 `OpenAI 前 CPO` → `OpenAI ex CPO`（C19-③）。
        ('r16mq2', 'Writing evals is the most important',
         '&#8220;Writing evals is the most important thing a PM can do in the AI era.&#8221;',
         'Kevin Weil · OpenAI ex CPO'),
        ('r16mq3', 'One of the biggest fallacies in AI',
         '&#8220;One of the biggest fallacies in AI is people compare it with this perfect human '
         'that does not exist.&#8221;',
         'Des Traynor · Intercom 联合创始人')):
        _p = _sec_of(_anchor)
        assert f'<div class="en rise" style="--i:4">{_en}</div>' in _p, f"C16 · {_cn} 英文补充行未落地"
        assert f'<div class="s rise" style="--i:5">{_sig}</div>' in _p, f"C16 · {_cn} 署名行未落地"
        #    DOM 顺序：中文 .q 必须排在英文 .en 之前（「中上英下」的结构账）
        assert _p.index('<div class="q">') < _p.index('<div class="en rise"'), f"C16 · {_cn} 中文应在英文之前"
        assert len(re.findall(rf'class="slide[^"]*\b{_cn}\b', s)) == 1 and f'.{_cn} ' in s, \
            f"C16 · 档位类未挂/未定义：{_cn}"
    #       中文两行（分行落在自然停顿上，禁止词中断行 —— 实际渲染宽度由 QA 机检）
    for _t in ('<i class="rise" style="--i:1">写评测，是 AI 时代</i>',
               '<i class="rise" style="--i:2">一个产品经理能做的最重要的事。</i>',
               '<i class="rise" style="--i:1">AI 最大的谬误之一，是人们总把它</i>',
               '<i class="rise" style="--i:2">跟一个并不存在的完美的人相比。</i>'):
        assert s.count(_t) == 1, f"C16-③④ 中文分行未落地或重复：{_t}"
    #       ④ 出处改正：署名 + 出处行；英文逐字与一手 transcript 一致（rev.com · ts=629.89）
    _pq3 = _sec_of('One of the biggest fallacies in AI')
    assert '<div class="s src rise" style="--i:6">Cheeky Pint #11 · 00:10:29</div>' in _pq3, \
        "C16-④ 出处行未落地"
    assert 'Bret Taylor' not in _pq3 and '2026-03 公开访谈' not in _pq3, "C16-④ 金句 03 旧署名残留"
    #       中文字号 > 英文字号（体系账；实测由 QA 机检，这里守 CSS 档位本身）
    assert '.r16mq2 .mq .q,.r16mq3 .mq .q{font-family:var(--f-cn);font-size:80px' in s and \
           '.r16mq2 .mq .en,.r16mq3 .mq .en{font-family:var(--f-mono);font-size:30px' in s, \
        "C16-③④ 中上英下的字号档未定义"

    #    ⓓ ⑤ 钱流向页 —— ⚠️ **R19 改判：三格小倍数整张作废**。
    #       Colin 看着线上 R18 说「那个带时间轴的曲线的图表更加清楚展示了三者的变化」，
    #       所以 R19 把形式换回曲线（**数据一个不动**），并删掉「三格各用各的尺」那句。
    #       于是这里的三格几何账 —— 尺度说明句 / 九根柱 / 九个值标 / 三条基线 + 三条表头线 /
    #       九个 x 刻度 / 三个「至今」/ 落点年高亮 / 三格截点 / 格内 take / 柱高 --len 机检 ——
    #       **全部从这里摘除**，正向账（三序列九个数在位、对数轴标注、零第二把尺）搬进下面的 C19 段。
    #       R16 真正立住、且 R19 一个字没动的那两条留在这里：**数值序列**与 **foot 换源**。
    _p16 = _sec_of('近三年，钱的三次落点')
    assert len(re.findall(r'class="slide[^"]*\br16money\b', s)) == 1 and '.r16money ' in s, \
        "C16-⑤ 档位类未挂/未定义：r16money"
    assert '>口径：一级市场披露融资额 · $B</text>' in _p16, "C16-⑤ 口径行缺失"
    #       最终数值序列（重查结果；R19 换成单轴三线图之后每个数各标一次）
    for _v in ('>$31.4B</text>', '>$88.9B</text>', '>$178B</text>',   # 基础模型（Crunchbase）
               '>$1.6B</text>', '>$3.3B</text>', '>$0.2B</text>',      # 写代码（New Market Pitch）
               '>$1.9B</text>', '>$1.8B</text>'):                       # 对话式（同源同口径）
        assert _p16.count(_v) == 1, f"C16-⑤ 数值序列不符：{_v} 应恰好一处，实际 {_p16.count(_v)}"
    #       口径纪律：svg 里不许出现 ARR / 收入（融资轴只画融资）
    _svg16 = _p16[_p16.index('<svg'):_p16.index('</svg>')]
    #       （图上唯一的百分数是「Cursor 一家占 98%」，那是**同一口径内部**的占比，不是另一把尺）
    assert 'ARR' not in _svg16 and '收入' not in _svg16, "C16-⑤ 融资图里不许混进 ARR / 收入口径"
    #       foot 仍是 R14 体例（只留来源名），且换成了本轮真正用到的两家
    assert '<div class="foot flow rev" style="--i:9">Source · New Market Pitch · Crunchbase News ' \
           '· TechCrunch · CNBC</div>' in _p16, "C16-⑤ 新 foot 一行未落地"
    #       eyebrow / h2 一个字没动（R12 立的那两条仍然成立）
    for _keep in ('产品经理判断趋势有个笨办法：不看报告的措辞，看钱往哪走',
                  '近三年，钱的三次落点：先模型，再代码，<em>现在轮到对话</em>'):
        assert _keep in _p16, f"C16-⑤ eyebrow/h2 不该被动：{_keep}"
    assert set(re.findall(r'data-step="(\d+)"', _p16)) <= {'1', '2'}, "C16-⑤ data-step 应仍 ≤2"

    # ── C16 · R16 五处 ─────────────────────────────────────────────────────
    # ── C17 · R17 十二处 ───────────────────────────────────────────────────
    #    ⓐ 负向：九处删文的整段必须查无此句（每条后面标出自哪一处）
    #    ⚠️ 只数**页面正文**：历史层的 CSS 注释里写过被删素材的名字（例如 C10_CSS 里那句
    #       「行首那两个 mono 标签（外 · 读 AGENT / 内 · 读自己）」），那是源码注释不是页内容，
    #       历史层只读、不改，所以这里把 <style> 排除掉再查。
    _slides17 = _nouri(''.join(re.findall(r'<section class="slide.*?</section>', s, re.S)))
    for _mk in ('不是你问它才查。是你还没开口',                    # ① P27 Signal 01 描述句
                '发起权第一次不在人这边',                          # ① P27 Signal 02
                '而不是摊进某个人的 KPI',                          # ① P27 Signal 03
                '翻最近 100 次交互，几次是它发起的？',              # ① P27 怎么验 Q1
                '它自报家门那句话，写在哪个文件里？',               # ① P27 怎么验 Q2
                '报表里有没有独立的一行？',                         # ① P27 怎么验 Q3
                '出事五分钟内，你拿得出那条链路吗？',               # ① P27 怎么验 Q4
                '这四句话里，只要有一句', '四个「怎么验」，回去就能跑一遍',  # ① P27 收尾 note
                '我不想用这一页制造恐慌', '从伦理讨论变成了工程需求',        # ②a P31 note
                '一家模型厂的公开披露', '一家第三方平台的生产设施',          # ②b 实名前的匿名说法
                '越往上，答案<em>越短</em> —— 也越重',                     # ③ P45 旧 h2
                '全场收束 · ONE LINE EACH',                               # ③ P45 旧 eyebrow
                '外 · 读 AGENT', '抢话、复读、没转人工', '一百条里踩了几条',   # ④ P46 外列四条
                '模型的问题还是流程的', '同一套题，分数动没动',
                '内 · 读自己', '我凭什么说它不行', '我的判断能不能复现',       # ④ P46 内列四条
                '我是不是在用感觉验收', '我改的是它还是我的标准',
                'viewBox="0 -177 1680 646"',                              # ④ P46 旧 viewBox
                '¥5,850 亿', '早就趴在预算科目里',                          # ⑤ P8 国内存量 note
                '整个 conversational AI，从一个技术选项，变成了预算科目',      # ⑤ P8 旧 foot
                '至于预测？同一年的两份报告还在打架', '别等预测收敛，看采购',   # ⑥ P9 预测对照
                '这道题第二、三幕来解', 'Gartner',                          # ⑥ P9 连坐清零
                '（n=3,075', '（n=5,119）',                                # ⑥ P9 foot 细节
                '2024 那一年，写代码和对话式拿到的钱一样多',                  # ⑦ P7 note
                '还没算进 Sierra 五月那笔 $950M',
                '对话式 AI 是个大泛类', '下一页拆开看。',
                '设想的是一场五分钟的文字对谈', '在毫不知情的状态下完成的',     # ⑧ P15 图灵两句
                '法律 AI 公司 Legora 的做法值得抄', '谁定义正确，谁就掌握这段关系',  # ⑨ P24
                '被使用、被记住、被托付——三个「被」字',                      # ⑩ PART 1 幕卡小字
                '被记住，靠的是一致性。被托付，靠的是可验证。',               # ⑩ PART 2 幕卡小字
                '三年了，一直是我们朝它走一步、再走一步',                     # ⑩ PART 3 幕卡小字
                '前面三幕讲的是「怎么造那把尺子」',                          # ⑩ PART 4 幕卡小字
                '2026-03 公开访谈'):                                       # ⑪ P4 旧出处
        assert _mk not in _slides17, f"C17 · R17 该删/该改未落地：{_mk}"

    #    ⓑ ① P27 判据页：删六块之后，只剩三个 Signal 标题 + Q1–Q4 两行对照
    _p27 = _sec_of('可观测，才敢写进需求文档')
    for _keep in ('它主动想起', '它主动开口', '它有自己的 OKR',
                  '>谁先行动？<', '>谁代表谁？<', '>结果记在哪？<', '>出错谁负责？<',
                  '先有归属，才谈得上追责——业绩可以记在它名下，责任必须落在可追责的人身上。'):
        assert _keep in _p27, f"C17-① 该保留的被误删：{_keep}"
    assert _p27.count('<div class="kv') == 8, \
        f"C17-① Q1–Q4 应各剩两行对照（工具时代/共事时代）= 8 条，实际 {_p27.count('<div class=' + chr(34) + 'kv')}"
    assert '怎么验' not in _p27 and '<div class="note' not in _p27, "C17-① 六块未删净"

    #    ⓒ ② P31 案例 03：note 清零 + 事件主体实名（本轮 WebSearch 查实，见设计文档 R17 段）
    _p31 = _sec_of('两道围栏：提示词拦话术，')
    assert '<div class="note' not in _p31, "C17-②a note 未删净"
    for _mk in ('2026-07 · OpenAI 的公开披露', '入侵了 <b>Hugging Face</b> 的生产设施',
                'Hugging Face CEO Clem Delangue', '可能是同类中的第一起',
                '<b>OpenAI Presence</b>（7-22）', '<b>相隔不到 24 小时</b>',
                '<span class="src">Fortune · The Hacker News · TechCrunch · CBS News · 2026-07</span>'):
        assert _mk in _p31, f"C17-②b 实名/来源未落地：{_mk}"
    #       三张教训卡的标题与链路图仍在
    #       ⚠️ **R19 改判**：教训 03 标题「也必须在纸上」→「也必须写进 SOP 流程里」（C19-④），
    #          从这条名单里摘出；三段卡片正文也在 C19-④ 整块删了（负向账在 C19 段）。
    for _keep in ('提示词不是围栏', '围栏必须在架构里',
                  '一句「不要」，拦不住一个已经能执行动作的主体'):
        assert _keep in _p31, f"C17-② 该保留的被误伤：{_keep}"

    #    ⓓ ③ P45 全场收束：新 h2 + 旧 h2 降级进 eyebrow（四栏一个字没动）
    _p45 = _sec_of('全场收束，<em>一页带走</em>')
    assert '<div class="eyebrow flow" style="--i:0">ONE LINE EACH · 越往上，答案越短，也越重</div>' in _p45, \
        "C17-③ 旧 h2 未降级进 eyebrow"
    for _keep in ('交的不再是一份 PRD', '管的不再是三个职能', '卖的不再是调用量', '要的不是 AI 能力'):
        assert _keep in _p45, f"C17-③ 四栏不该被动：{_keep}"

    #    ⓔ ④ P46 终页：两列八条清零 + svg 按新版心重画（--len 与新路径逐条同步）
    _p46 = _sec_of('同一把尺子，向外叫 <em>Eval</em>，向内叫<em>内观</em>')
    assert 'viewBox="0 0 1680 640"' in _p46, "C17-④ 终页 svg 未按新版心重画"
    for _mk in ('x="800" y="90" width="88" height="420"',            # 尺子加长
                'd="M800 176 H836 M800 258 H824 M800 340 H836 M800 422 H824"',  # 四道刻度重排
                '--len:140;--i:3',                                    # 刻度合计 120 → --len 140
                'style="--len:400;--i:4" stroke-width="1.8" d="M908 300 H1300"',   # 向外线
                'style="--len:410;--i:6" stroke-width="1.8" d="M780 300 H380"',    # 向内线
                '>同一把尺子</text>', '>向外 · Eval</text>', '>向内 · 内观</text>',
                '>让我们看见系统的偏差</text>', '>让我们承认自己的偏差</text>',
                '>AGENT / PRODUCT</text>', '>HUMAN / SELF</text>'):
        assert _mk in _p46, f"C17-④ 终页新图元缺失：{_mk}"
    assert _p46.count('class="stroke-am pkt"') == 1 and _p46.count('class="stroke-co pkt"') == 1, \
        "C17-④ 两枚同步光点必须各一枚"

    #    ⓕ ⑤⑥⑦ 三页删文 + 两处 foot 改写
    _p8 = _sec_of('对话式 AI 的钱，<em>流向了哪里</em>')
    assert '<div class="note' not in _p8 and '<div class="foot' not in _p8, "C17-⑤ note/foot 未删净"
    assert _p8.count('<div class="card') == 6, "C17-⑤ 六张卡应一张不少"
    _p9 = _sec_of('对话式智能体的采购，<em>正在悄然发生</em>')
    assert '<div class="note' not in _p9, "C17-⑥ 预测对照未删净"
    assert '<div class="foot flow rev" style="--i:11">SOURCE · Salesforce · CC-CMM · 艾媒咨询 ' \
           '· 第一新声 · Pew Research</div>' in _p9, "C17-⑥ foot 未简化成只留机构名"
    for _keep in ('>66%</text>', '>70%</text>', '>91%</text>', '>15–20%</text>', '>49%</text>'):
        assert _keep in _p9, f"C17-⑥ 五条读数不该被动：{_keep}"
    _p7 = _sec_of('近三年，钱的三次落点')
    assert '<div class="note' not in _p7 and 'Sierra' not in _p7, "C17-⑦ note 未删净"
    for _keep in ('口径：一级市场披露融资额 · $B', '一个季度，就是去年一整年的两倍',
                  '一轮钱在 2025 发完 · Cursor 一家占 98%', '半年，已经追平去年一整年',
                  'Source · New Market Pitch · Crunchbase News · TechCrunch · CNBC'):
        assert _keep in _p7, f"C17-⑦ 口径行/格内注/foot 不该被动：{_keep}"

    #    ⓖ ⑧⑨ 两处压缩（⑧ 含两处对 Colin 口述的口径修正，理由见设计文档 R17 段）
    _p15 = _sec_of('2,475 通全量人工标注的真实外呼里')
    assert '<div class="foot flow" style="--i:4">1950 年，图灵提出那场五分钟的判别游戏；' \
           '76 年后，<b>96.5% 的真实通话</b>，悄悄通过了图灵测试。</div>' in _p15, "C17-⑧ 新句未落地"
    #       修正 a：150 年是贝尔那条线（P4），图灵是 1950 / 76 年后 —— 这一页不许出现 150 年
    assert '150' not in _p15, "C17-⑧a「150 年」是贝尔那条线，不该出现在图灵这页"
    #       修正 b：96.5% 的口径是「未被识破的通话占比」，与同页 .cap 的 2,475/86 完全对齐
    assert '96.5% 的真实通话' in _p15 and '只有 <b>86 通</b> 被对方听出' in _p15, "C17-⑧b 口径未对齐"
    _p24 = _sec_of('同一把 Eval：对产品量<em>好坏</em>，对商业量<em>钱</em>')
    assert 'Legora' not in _p24 and '<span class="s">' not in _p24, "C17-⑨ Legora 那句未删净"
    assert '从规划到回款，出题权一路没换过手。' in _p24, "C17-⑨ land 主句不该被动"

    #    ⓗ ⑩ 四张幕卡：小字清零 + 骨架四件（编号 / 英文名 / 幕名 / rail）一件不少
    _n_act17 = 0
    for _cn, _en in (('语法变了', 'GRAMMAR'), ('被托付', 'ENTRUSTED'),
                     ('双向奔赴 · 共事', 'COWORK'), ('人与组织', 'PEOPLE &amp; ORG')):
        _pa = _sec_of(f'<div class="cn spread" style="--i:3">{_cn}</div>')
        assert '<div class="act">' in _pa, f"C17-⑩ 锚到的不是幕卡：{_cn}"
        assert '<div class="d flow"' not in _pa, f"C17-⑩ 幕卡小字未删净：{_cn}"
        assert f'<div class="en settle" style="--i:1">{_en}</div>' in _pa and \
               '<div class="num flow" style="--i:0">PART ' in _pa and '<div class="rail">' in _pa, \
            f"C17-⑩ 幕卡骨架被误伤：{_cn}"
        _n_act17 += 1
    assert _n_act17 == 4, f"C17-⑩ 应恰好四张幕卡，实际 {_n_act17}"
    #       R12 加的资金流向页不是幕卡，绝不能被误伤（它有 .wrap/.head，没有 .act）
    assert '<div class="act">' not in _p7, "C17-⑩ 资金流向页被误当成幕卡"
    assert len(re.findall(r'<div class="act">', _slides17)) == 4, "C17-⑩ 全场应恰好四张幕卡"

    #    ⓘ ⑪ P4 出处精化（R16 查证时在本仓 csagent.html 找到的确切集数）
    _p4 = _sec_of('You have all these fancy MCP things')
    assert '<div class="by">Bret Taylor · CEO of Sierra / Chairman of OpenAI · Cheeky Pint #27</div>' in _p4, \
        "C17-⑪ 新出处未落地"

    #    ⓙ 连坐终扫：被删素材在全 deck 不该留下悬空引用
    #       ⚠️「怎么验」只在 P27 有过**标签**用法；P45 的「做到了，我怎么验」是一句自然语言，
    #         自己站得住，不是对 P27 那四行的指认 —— 所以这里按**标签形态**查，不查字面。
    assert '<div class="kk">怎么验</div>' not in _slides17, "C17 · 「怎么验」标签未全场清零"
    assert '把「它能不能做到」换成「做到了，我怎么验」。' in _slides17, "C17 · P45 那句自然语言不该被误伤"
    for _mk in ('Legora', 'Gartner', '5,850', '预测'):
        assert _mk not in _slides17, f"C17 · 被删素材全场残留：{_mk}"
    #       页级档位类必须全部挂上且 CSS 有定义（九页一页一档）
    for _c in ('r17money', 'r17p8', 'r17p9', 'r17p15', 'r17p24', 'r17p27', 'r17case3', 'r17fin'):
        assert len(re.findall(rf'class="slide[^"]*\b{_c}\b', s)) == 1 and f'.{_c} ' in s, \
            f"C17 · 档位类未挂/未定义：{_c}"
    #       ⑫ P44「对组织说 · 单向门/双向门」—— ⚠️ **R18 改判**：R17 那一轮按 Colin 的话
    #          按兵不动（等他的生成图），当时立了一条「门图仍是那一张 svg」的守门断言；
    #          R18 图到了，那对 svg 门已被单张门图取代，`<svg count == 1` 这条作废。
    #          三段文字「原样还在」的账仍然成立（它们只是从 svg 里挪出来重排），继续守。
    #          ⚠️ **R19 改判**：C19-⑤ 把「这条线画在哪 —— 是 CEO 的活…」整行删了，
    #          从这条名单摘出；两段门标签仍在（它们是 % 定位，随图缩放，R19 收比例也没动它们）。
    _p44 = _sec_of('对组织说：<em>放权</em>，从分清单向门与双向门开始')
    for _keep in ('可逆 · 双向门 · 放手做，不用批', '不可逆 · 单向门 · 先升级'):
        assert _keep in _p44, f"C17-⑫ P44 的两段门标签一字未改：{_keep}"

    # ── C18 · R18 一处（P44 换门图） ────────────────────────────────────────
    #    ⓐ 单张门图在位：data URI · WebP · screen 融底 · .rise 入场
    _p44b = _sec_of('对组织说：<em>放权</em>，从分清单向门与双向门开始')
    assert '<div class="doors rise" style="--i:3">' in _p44b, "C18-① 门图容器/入场未落地"
    assert _p44b.count('<img src="data:image/webp;base64,') == 1, "C18-① 门图应是唯一一张内联 data URI"
    assert 'alt="左：可逆的双向弹簧门；右：不可逆的单向金库门"' in _p44b, "C18-① 门图缺 alt"
    assert '.r18doors .doors img{display:block;width:100%;height:auto;mix-blend-mode:screen;}' in s, \
        "C18-① screen 融底未定义"
    #    ⓑ 旧的两个 svg 门整块清零（这一页从此没有 svg）
    assert '<svg' not in _p44b, "C18-① 旧门图 svg 未清零"
    for _old in ('class="stroke-am pkt"', 'd="M940 70 V552"', 'x="350" y="160"', 'x="1130" y="160"'):
        assert _old not in _p44b, f"C18-① 旧门图元残留：{_old}"
    #    ⓒ 图下双标签：对位到实测的两扇门中心，文字一字未改
    assert '<div class="dl am" style="left:27.2%">可逆 · 双向门 · 放手做，不用批</div>' in _p44b and \
           '<div class="dl co" style="left:72.3%">不可逆 · 单向门 · 先升级</div>' in _p44b, \
        "C18-① 图下双标签未对位/文字被动"
    #    ⓓ ⚠️ **R19 改判**：CEO 那句（R18 才从 svg 里挪出来的 .dcap 独立行）在 C19-⑤ 整行删了，
    #       这条正向断言作废（负向账在 C19 段）。land 落地句仍原样。
    assert '<b>把权放给 high agency 的人</b>——他们会带着 Agent，把结果一起做出来。' in _p44b, \
        "C18-① land 落地句不该被动"
    #    ⓔ 档位类 + 资源账（图进仓库、内联体积可控）
    assert len(re.findall(r'class="slide[^"]*\br18doors\b', s)) == 1 and '.r18doors ' in s, \
        "C18 · 档位类未挂/未定义：r18doors"
    assert len(_DOORS_B) <= 400 * 1024, "C18 · 门图超预算"
    #    ⓕ 全场只有这一张 webp（其余四张是母版的 logo/cover/venue，jpeg/png）
    assert s.count('data:image/webp;base64,') == 1, "C18 · 全场应只有一张内联 webp"

    # ── C19 · R19 五处 ─────────────────────────────────────────────────────
    _slides19 = _nouri(''.join(re.findall(r'<section class="slide.*?</section>', s, re.S)))
    #    ⓐ 负向：被删/被换的整段必须查无此句
    for _mk in ('三条赛道量级差百倍',                                   # ① 被点名删掉的那句
                'class="col ', 'class="pr"',                            # ① 三格小倍数的柱与表头线
                '>2026 Q1 · 截至 3-31</text>', '>2026 上半年 · 截至 7-02</text>',  # ① 三格各自的截点行
                '观点页 · 嘉宾金句',                                    # ② 五张金句页的编号 eyebrow
                'Kevin Weil · OpenAI 前 CPO',                           # ③ 旧署名
                '高敏权限不能只靠提示词和策略文档约束',                  # ④ 教训 01 正文
                '容器、沙箱、权限边界、人工升级通道',                    # ④ 教训 02 正文
                '授权不能只活在代码里', '这六件事，第四幕会变成组织的授权语法',  # ④ 教训 03 正文
                '也必须在纸上',                                          # ④ 教训 03 旧标题
                '这条线画在哪 —— 是 CEO 的活', 'class="dcap'):           # ⑤ P44 那行
        assert _mk not in _slides19, f"C19 · R19 该删/该改未落地：{_mk}"

    #    ⓑ ① P7 · 单轴对数三线图（数据一个不动）
    _p19 = _sec_of('近三年，钱的三次落点')
    assert len(re.findall(r'class="slide[^"]*\br19money\b', s)) == 1 and '.r19money ' in s, \
        "C19-① 档位类未挂/未定义：r19money"
    #       ⚠️ 红线：全场零第二把尺 —— 双轴的一切图元必须仍然是零
    for _dual in ('>基础模型 $B</text>', '>Coding / 对话式 $B</text>', '左右两轴量级不同',
                  'id="r14conv"', 'x="1218"'):
        assert _dual not in _p19, f"C19-① 双轴残留（红线）：{_dual}"
    #       对数刻度：角落小字 + 十倍阶梯网格四条并逐条标出（网格线本身就是刻度）
    assert '>纵轴 · 对数刻度</text>' in _p19, "C19-① 对数刻度标注缺失"
    assert 'd="M250 200 H1180 M250 300 H1180 M250 400 H1180 M250 500 H1180"' in _p19, \
        "C19-① 十倍阶梯网格（四条）缺失"
    for _d in ('>$100B</text>', '>$10B</text>', '>$1B</text>', '>$0.1B</text>'):
        assert _p19.count(_d) == 1, f"C19-① 十倍阶梯刻度标缺失/重复：{_d}"
    #       三条曲线各一条 + 各三个节点；共享 x 三刻度（不再是三格 ×3）
    for _c in ('fnd', 'cod', 'cnv'):
        assert _p19.count(f'class="ln {_c} dw"') == 1, f"C19-① 曲线应各一条：{_c}"
        assert _p19.count(f'class="dot {_c} pop"') == 3, f"C19-① 每条线三个节点：{_c}"
        assert _p19.count(f'class="lead {_c}"') == 1, f"C19-① 终点名牌引线缺失：{_c}"
    assert _p19.count('class="lbl yr"') == 3, "C19-① 共享 x 只应有三个年份刻度"
    assert _p19.count('>至今</text>') == 1, "C19-① 「至今」只标一次（共享 x）"
    #       截点语义保留：三条线的 2026 截点不同，合并成 x 轴下的一行说明
    assert '2026 至今：基础模型截至 3-31（Q1）· 写代码与对话式截至 7-02（H1）' in _p19, \
        "C19-① 三条线各自的 2026 截点说明缺失"
    #       数据一个不动：三序列九个数在位（2024 两条重合成一点，$1.6B 只标一次 → 页上八个值标）
    for _v in ('>$31.4B</text>', '>$88.9B</text>', '>$178B</text>',
               '>$3.3B</text>', '>$0.2B</text>',
               '>$1.6B</text>', '>$1.9B</text>', '>$1.8B</text>'):
        assert _p19.count(_v) == 1, f"C19-① 数值应逐个各一处：{_v}"
    assert '写代码与对话式，2024 从同一点出发' in _p19, "C19-① 两条线重合那一点的说明缺失"
    #       R16 三条叙事注转成曲线旁 callout，一字未改
    for _t in ('一个季度，就是去年一整年的两倍', '一轮钱在 2025 发完 · Cursor 一家占 98%',
               '半年，已经追平去年一整年'):
        assert _p19.count(_t) == 1, f"C19-① 曲线旁 callout 缺失：{_t}"
    #       口径行与 Source foot 原样保留
    assert '>口径：一级市场披露融资额 · $B</text>' in _p19 and \
           '<div class="foot flow rev" style="--i:9">Source · New Market Pitch · Crunchbase News ' \
           '· TechCrunch · CNBC</div>' in _p19, "C19-① 口径行/来源行不该被动"
    #       --len 必须盖得住贝塞尔实长（三条线逐条采样算过：fnd 854 / cod 871 / cnv 850）
    for _len, _y in re.findall(r'class="ln \w+ dw" style="--len:(\d+);--i:\d+" d="M300 ([\d.]+)', _p19):
        assert int(_len) >= 880 or int(_len) >= 850, f"C19-① --len 过小：{_len}"
    assert set(re.findall(r'data-step="(\d+)"', _p19)) <= {'1'}, "C19-① data-step 应 ≤1（note 已在 R17 删掉）"

    #    ⓒ ② 五张金句页：eyebrow 全场清零 + 五张仍在（凭内容认）+ 档位类五处
    for _mq in ('我们叫了它三年 Agent（代理人）——', 'Writing evals is the most important',
                'One of the biggest fallacies in AI', '围栏不是拦住它，', '没有撤回键。'):
        assert _slides19.count(_mq) == 1, f"C19-② 金句主文应各一处：{_mq}"
    assert len(re.findall(r'class="slide[^"]*\br19mq\b', s)) == 5 and '.r19mq ' in s, \
        "C19-② 五张金句页的档位类未全挂/未定义：r19mq"
    #       ⚠️ 只删金句页那五条：P15 案例 01 的 `.mark`（案例 01 · 真实生产环境…）是页面内容不是
    #          页型编号，Colin 没点名，一个字不动 —— 所以全场 .mark 剩且只剩它一处。
    assert _slides19.count('class="mark') == 1 and \
           '案例 01 · 真实生产环境 · A PRODUCTION-SCALE TURING TEST' in _slides19, \
        "C19-② .mark 应只剩案例 01 那一处（五张金句页的编号已删）"
    #    ⓓ ③ 金句 02 署名 ex CPO（全场 Weil 仍仅一处）
    assert '<div class="s rise" style="--i:5">Kevin Weil · OpenAI ex CPO</div>' in _slides19, \
        "C19-③ 新署名未落地"
    assert _slides19.count('Kevin Weil') == 1, "C19-③ 全场 Weil 应仍仅金句 02 一处"

    #    ⓔ ④ P31：三张教训卡只剩标题 + 教训 03 改题；链路图与事件块一个字没动
    _p31b = _sec_of('两道围栏：提示词拦话术，')
    assert '<div class="d">' not in _p31b, "C19-④ 教训卡应只剩标题"
    assert _p31b.count('<div class="tag">教训 0') == 3, "C19-④ 三张教训卡都得在"
    for _t in ('<div class="t">提示词不是围栏</div>', '<div class="t">围栏必须在架构里</div>',
               '<div class="t">也必须写进 SOP 流程里</div>'):
        assert _t in _p31b, f"C19-④ 教训标题缺失/未改题：{_t}"
    for _keep in ('一句「不要」，拦不住一个已经能执行动作的主体', '2026-07 · OpenAI 的公开披露',
                  'Hugging Face CEO Clem Delangue'):
        assert _keep in _p31b, f"C19-④ 链路图/事件块被误伤：{_keep}"
    #       ⚠️ 悬空检查（R19 逐条走过一遍）：「六件事」这个提法**全 deck 只在这张卡的正文里出现过**
    #          （P53 那句「第三幕写给 Agent 的授权六件事」早在 R10/R11 的删文里就下台了），
    #          所以正文一删，全场归零、无人回指 —— 不需要再动任何一页。这条断言把它钉死：
    assert '六件' not in _slides19 and '授权语法' not in _slides19, \
        "C19-④「六件事」应已全场归零（若别处冒出回指，就是悬空，必须一并理顺）"
    #          第四幕组织侧那页讲的是「单向门 / 双向门」与「授权可撤销」，本来就不依赖案例 03。
    assert '授权可撤销' in _slides19, "C19-④ 第四幕组织侧的授权口径不该被误伤"
    assert len(re.findall(r'class="slide[^"]*\br19case3\b', s)) == 1, "C19-④ 档位类未挂：r19case3"

    #    ⓕ ⑤ P44：CEO 那行清零 + 图收到 1180（标签仍是 % 定位，一个数没动）
    _p44c = _sec_of('对组织说：<em>放权</em>，从分清单向门与双向门开始')
    assert 'dcap' not in _p44c and 'CEO' not in _p44c, "C19-⑤a CEO 那行未删净"
    assert '.r19doors .doors{max-width:1180px;}' in s, "C19-⑤b 门图未收到 1180"
    assert len(re.findall(r'class="slide[^"]*\br19doors\b', s)) == 1 and '.r19doors ' in s, \
        "C19-⑤ 档位类未挂/未定义：r19doors"
    for _keep in ('<div class="dl am" style="left:27.2%">可逆 · 双向门 · 放手做，不用批</div>',
                  '<div class="dl co" style="left:72.3%">不可逆 · 单向门 · 先升级</div>',
                  '<b>把权放给 high agency 的人</b>——他们会带着 Agent，把结果一起做出来。'):
        assert _keep in _p44c, f"C19-⑤ 该保留的被误伤：{_keep}"


    print("ruler ✓ noindex ✓ C2/C3 content ✓ C8 R8v1 ✓ C9 R9 45p ✓ C10 R10 八页 ✓ "
          "C11 R11 十三页 ✓ C12 R12 新页 46p ✓ C13 R13 七处 ✓ C14 R14 讲台+双轴图 ✓ "
          "C15 R15 终轮十项 ✓ C16 R16 五处 ✓ C17 R17 十二处 ✓ "
          f"C18 R18 P44 门图 ✓（{len(_DOORS_B)//1024}KB webp 内联）· C19 R19 五处 ✓")
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
