#!/usr/bin/env python3
"""cowork.html → cowork-conf.html：2026 AI 产品大会视觉版。
   完全对齐大会模板：黑底 + 紫系(#9333EA/#A855F7/#C084FC) + 金黄 #FFC000 +
   阿里巴巴普惠体 2.0 + 页头紫 tab/双 logo + 模板封面 keyart + 章节页/观点页版式。
   内容与 65 页母版逐字一致，另叠加【仅大会版】内容试验层（2026-08-03 反馈：删两条路页/挪三把尺子与时机页/终幕对象化等）
   与媒体层（P3 录音 + 「授权可收回」页后插视频页）。R3 后共 63 页。
   媒体行为与 PPT 对齐：前进键第一按播放，再按停止并翻页；M 键手动播/停（p 已被「跳上一整页」占用）。"""
import re, sys
sys.path.insert(0, "/tmp/conf-tpl")
from assets import LOGO, COVER, VENUE

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

# ── 6.4) 内容试验层（Colin 2026-08-03 反馈 · 仅大会版；敲定后再同步母版） ──
def rep1(old, new):
    global s
    assert s.count(old) == 1, "锚点失效: " + old[:44]
    s = s.replace(old, new, 1)

# a) P15 分水岭 · 上行支加「熟人」进阶节点（工具→熟人→伙伴），九成卡点标在熟人格
rep1('<circle class="fill-am pop" style="--i:4" cx="840" cy="150" r="9"/>',
     '''<circle class="fill-am pop" style="--i:4" cx="840" cy="150" r="9"/>
          <circle class="fill-ink pop" style="--i:5" cx="1005" cy="102" r="9"/>
          <g class="pop" style="--i:5"><text class="ttl" x="1005" y="64" text-anchor="middle" style="font-size:30px">熟人</text></g>
          <text class="txt pop" style="--i:5" x="1005" y="146" text-anchor="middle">记得你是谁</text>
          <circle class="stroke-co pop" style="--i:6" cx="1005" cy="102" r="18" stroke-width="2"/>
          <text class="lbl fill-co pop" style="--i:6" x="1005" y="238" text-anchor="middle">九成产品卡在这一格</text>''')

# b) P27 眉题：分化已画进本页阶梯图，眉题点「同一个起点」
rep1('接上一幕的岔路口 · 我们换到下面那条', '同一个起点 · 上一幕走「陪伴」，这一幕走「干活」')

# c) 案例02 · 96.5% 右侧留白 → 3.5% 拆解（素材：V5 主干 · 九类 AI 感知信号）
rep1('<div class="mark flow" style="--i:0">案例 02 · 真实生产环境 · A PRODUCTION-SCALE TURING TEST</div>',
     '''<div class="mark flow" style="--i:0">案例 02 · 真实生产环境 · A PRODUCTION-SCALE TURING TEST</div>
    <div class="m35">
      <div class="mk flow" style="--i:5">那 3.5%，是怎么露的马脚 · 九类「AI 感知信号」</div>
      <div class="row flow" style="--i:6"><span class="n">60</span><span class="t">情绪重复 / 不耐烦</span><span class="bar" style="--w:100%"></span></div>
      <div class="row flow" style="--i:7"><span class="n">11</span><span class="t">报出品牌或系统身份</span><span class="bar" style="--w:18%"></span></div>
      <div class="row flow" style="--i:7"><span class="n">11</span><span class="t">粗鲁与对抗</span><span class="bar" style="--w:18%"></span></div>
      <div class="row flow" style="--i:8"><span class="n">9</span><span class="t">直接说出「你是机器人」</span><span class="bar" style="--w:15%"></span></div>
      <div class="sx flow" style="--i:9">一通可命中多个标签 · 86 通为去重通数<br><b>机器感先暴露在节奏与情绪，不在音色。</b></div>
    </div>''')

# d) P37 · （R2/R3 的局部补丁已被 R5 全页重做取代，见 6.4-R5）

# e) 终幕三个「对象」标记 + 标题切心
rep1('<h2 class="ink" style="--i:1">你交付的不再是一份 PRD，是<em>一套评测</em></h2>',
     '<h2 class="ink" style="--i:1">对产品经理说：你交付的不再是一份 PRD，是<em>一套评测</em></h2>')
rep1('<h2 class="ink" style="--i:1">看过、用过、学过、<em>干过</em></h2>',
     '<h2 class="ink" style="--i:1">对个人说：你站到哪一阶了——看过、用过、学过、<em>干过</em></h2>')
rep1('<h2 class="ink" style="--i:1">转身的第一个动作，是<em>把那条线画出来</em></h2>',
     '<h2 class="ink" style="--i:1">对组织说：先分清哪些是<em>单向门</em>，哪些是<em>双向门</em></h2>')

# ── 6.4-R3) 第三轮反馈（2026-08-03 晚 · 仅大会版） ──────────
# 1) 四种失败页标题直给
rep1('<h2 class="ink" style="--i:1">「它变了个人」背后的四种失败</h2>',
     '<h2 class="ink" style="--i:1">这四种失败，让它变不成<em>伙伴</em></h2>')

# 2) 阶梯页：灰线画回消费分支（工具→熟人→伙伴，纵向对应实习生/外包）
rep1('''<text class="sm" x="180" y="408" text-anchor="middle">同一个起点</text>
            </g>
          </g>''',
     '''<text class="sm" x="180" y="408" text-anchor="middle">同一个起点</text>
            </g>
          </g>
          <g class="pop" style="--i:8">
            <g opacity=".5">
              <path class="stroke" stroke-width="1.8" d="M320 330 C 356 330, 356 384, 392 384 H1200"/>
              <circle class="fill-ink" cx="510" cy="384" r="7"/>
              <text class="sm" x="530" y="391" style="font-size:20px">熟人 · 记得你是谁</text>
              <circle class="fill-ink" cx="840" cy="384" r="7"/>
              <text class="sm" x="860" y="391" style="font-size:20px">伙伴 · 在乎你怎么样</text>
              <text class="lbl" x="1230" y="391" style="font-size:15px">消费级 · 陪伴 —— 上一幕走的那条</text>
              <path class="stroke" stroke-width="1" stroke-dasharray="3 6" d="M510 374 V352" opacity=".55"/>
              <path class="stroke" stroke-width="1" stroke-dasharray="3 6" d="M840 374 V290" opacity=".55"/>
            </g>
          </g>''')

# 3) 96.5% 页加标题句
rep1('A PRODUCTION-SCALE TURING TEST</div>\n    <div class="m35">',
     'A PRODUCTION-SCALE TURING TEST</div>\n    <div class="mh flow" style="--i:0">「活人感」已经被解决了。</div>\n    <div class="m35">')

# 4) MQ：换成面向全场的举手问句
rep1('<div class="q ink" style="--i:2">你凭什么说，<span class="hl">它做对了</span>？</div>',
     '<div class="q ink" style="--i:2">在座的有多少人，<br><span class="hl">亲手写过</span>一份自己产品的评测集？</div>')

# 5) 尺子第N课 → Eval 第N课（chrome + 眉题）
for _a, _b in [('尺子第一课','Eval 第一课'),('尺子第二课','Eval 第二课'),
               ('尺子第三课','Eval 第三课'),('尺子第四课','Eval 第四课')]:
    assert s.count(_a) == 2, f"{_a}: {s.count(_a)}"
    s = s.replace(_a, _b)

# 6) Eval 第四课重讲：AI 质检 100% 通过 vs 人类复检 ≥10% 错判
rep1('''<text class="lbl pop" style="--i:2" x="22" y="58">100 通真实通话</text>
          <path class="stroke dw" style="--len:1468;--i:3" stroke-width="44" stroke-linecap="round" d="M44 112 H1490" opacity=".22"/>
          <path class="stroke-co dw" style="--len:168;--i:4" stroke-width="44" stroke-linecap="round" d="M1512 112 H1658"/>
          <text class="lbl pop" style="--i:4" x="44" y="122">90 通确实通过</text>
          <text class="lbl fill-co pop" style="--i:5" x="1658" y="58" text-anchor="end">10 通真的失败了</text>

          <rect class="box pop" style="--i:6" x="0" y="196" width="580" height="118" rx="5" stroke-dasharray="7 7"/>
          <g class="pop" style="--i:7"><text class="ttl" x="290" y="248" text-anchor="middle" style="font-size:27px">一个永远回答「通过」的裁判</text></g>
          <text class="sm pop" style="--i:7" x="290" y="284" text-anchor="middle">零智能 · 零成本 · 零价值</text>
          <path class="stroke-co pop" style="--i:8" stroke-width="1.6" stroke-dasharray="6 8" d="M580 240 C 860 240, 980 160, 1180 138"/>
          <g class="pop" style="--i:9"><text class="big" x="1658" y="266" text-anchor="end" style="font-size:70px">90%</text></g>
          <text class="lbl pop" style="--i:10" x="1658" y="302" text-anchor="end">与人工标注一致率</text>''',
     '''<text class="lbl pop" style="--i:2" x="22" y="44">第一遍 · AI 质检 —— AI 在检测 AI</text>
          <path class="stroke-am dw" style="--len:1356;--i:3" stroke-width="40" stroke-linecap="round" d="M44 96 H1400"/>
          <g class="pop" style="--i:4"><text class="big fill-am" x="1658" y="112" text-anchor="end" style="font-size:60px">100%</text></g>
          <text class="lbl pop" style="--i:4" x="1658" y="146" text-anchor="end">质检报表 · 全部通过</text>
          <text class="lbl pop" style="--i:5" x="22" y="200">第二遍 · 人类复检 —— 同一批通话，重新听</text>
          <path class="stroke dw" style="--len:1220;--i:6" stroke-width="40" stroke-linecap="round" d="M44 252 H1264" opacity=".22"/>
          <path class="stroke-co dw" style="--len:136;--i:7" stroke-width="40" stroke-linecap="round" d="M1286 252 H1400"/>
          <g class="pop" style="--i:8"><text class="big fill-co" x="1658" y="268" text-anchor="end" style="font-size:60px">≥10%</text></g>
          <text class="lbl fill-co pop" style="--i:8" x="1658" y="302" text-anchor="end">错判 · 实际不通过</text>''')
rep1('<div class="col flow" style="--i:12"><div class="k">正确的看法 03</div><div class="v">裁判自己也要有回归集。换模型、换 prompt，裁判必须重新验一遍。</div></div>',
     '''<div class="col flow" style="--i:12"><div class="k">正确的看法 03</div><div class="v">裁判自己也要有回归集。换模型、换 prompt，裁判必须重新验一遍。</div></div>
      </div>
      <div class="land flow" style="--i:13">AI 裁判可以雇，但不能依赖。<span class="s">最终裁判权在你自己手里——你的产品，你亲自听。</span></div>
      <div class="tri" style="display:none">''')

# 7) P37 · （R3 局部补丁已被 R5 全页重做取代）

# 8) P40 · 账 → OKR
rep1('<div class="tag">Signal · 自己的账</div>', '<div class="tag">Signal · 自己的 OKR</div>')
rep1('<div class="t">它有自己的账</div>', '<div class="t">它有自己的 OKR</div>')

# 9) Part4 标题与眉题：类比 / 协作 / 双护栏 / Waymo / 护城河金句 / 两道围栏
rep1('<h2 class="ink" style="--i:1">三把互不相识的尺子，量出了<em>同一个形状</em></h2>',
     '<h2 class="ink" style="--i:1">类比自动驾驶与支付智能体：三把尺子，<em>同一个形状</em></h2>')
rep1('<h2 class="ink" style="--i:1">比人准了，还是得<em>人审批</em></h2>',
     '<h2 class="ink" style="--i:1">人和 Agent 共事的协作关系：它决策，<em>人审批</em></h2>')
rep1('<div class="eyebrow flow" style="--i:0">问责 · WHO APPROVES</div>',
     '<div class="eyebrow flow" style="--i:0">产品在其中的角色 · WHO APPROVES</div>')
rep1('<h2 class="ink" style="--i:1">Agent 出事，<span class="co">算谁的</span></h2>',
     '<h2 class="ink" style="--i:1">两道护栏：提示词拦话术，<span class="co">架构拦越权</span></h2>')
rep1('<h2 class="ink" style="--i:1">行人，<em>不在像素里</em></h2>',
     '<h2 class="ink" style="--i:1">这脚刹车，是产品经理写进<em>架构的护栏</em></h2>')
rep1('<i class="rise" style="--i:1">行人不在像素里，</i>',
     '<i class="rise" style="--i:1">提示词只能拦住一些越权，</i>')
rep1('<i class="rise" style="--i:2">承诺不在波形里。</i>',
     '<i class="rise" style="--i:2">架构的护栏，才是产品经理的护城河。</i>')
rep1('<div class="eyebrow flow" style="--i:0">指标的更新 · FROM LATENCY TO TIMING</div>',
     '<div class="eyebrow flow" style="--i:0">体验的围栏 · FROM LATENCY TO TIMING</div>')
rep1('<div class="eyebrow coral flow" style="--i:0">为什么语音这一行的门槛天然更高</div>',
     '<div class="eyebrow coral flow" style="--i:0">执行的围栏 · 为什么语音天然更难拦</div>')

# 10) 终幕：CEO 们说 / 对产品管理者说 / 共事 → 进化
rep1('<h2 class="ink" style="--i:1">High Agency 是发动机，<span class="co">但不是完整答案</span></h2>',
     '<h2 class="ink" style="--i:1">CEO 们说：High Agency 是发动机，<span class="co">但不是完整答案</span></h2>')
rep1('<div class="eyebrow flow" style="--i:0">个人层 · THE HUMAN ENGINE</div>',
     '<div class="eyebrow flow" style="--i:0">来自 CEO 们的同一个判断 · THE HUMAN ENGINE</div>')
rep1('<h2 class="ink" style="--i:1">2024 我画的三个圆，今天长出了<em>第四个</em></h2>',
     '<h2 class="ink" style="--i:1">对产品管理者说：2024 的三个圆，长出了<em>第四个</em></h2>')
rep1('<text class="ttl fill-am" x="1545" y="212" text-anchor="middle" style="font-size:38px">共事</text>',
     '<text class="ttl fill-am" x="1545" y="212" text-anchor="middle" style="font-size:38px">进化</text>')
rep1('<text class="lbl fill-am pop" style="--i:6" x="1545" y="312" text-anchor="middle">COWORK</text>',
     '<text class="lbl fill-am pop" style="--i:6" x="1545" y="312" text-anchor="middle">EVOLUTION</text>')
rep1('<b>共事不是我挑的词，是四条线自己走到的。</b>',
     '<b>进化不是我挑的词，是四条线自己走出来的。</b>')

# 11) 新页 · 临场感（Part 2 高光 · R4：三块循环动效 SVG——均衡器 / 记忆星图 / 声呐回应）
_EQH = [34,62,96,124,90,142,112,152,98,134,152,106,144,90,122,74,98,48]
_EQ = ''.join(
    f'<rect class="eqb" style="--d:{i*0.075:.2f}s" x="{14+i*25}" y="{196-h}" width="12" height="{h}" rx="2" '
    f'fill="var(--{"coral" if i in (4,11) else "amber"})" opacity="{".95" if i in (4,11) else ".8"}"/>'
    for i, h in enumerate(_EQH))
PRESENCE = '''<section class="slide">
  <div class="chrome"><span>PART 2 · 被记住</span><span>22</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">第二幕的高光 · PRESENCE</div>
      <h2 class="ink" style="--i:1">记忆之上，还有一层：<em>临场感</em></h2>
    </div>
    <div class="body">
      <div class="prz3">
        <div class="prz rise" style="--i:2">
          <div class="pzk">01 · HEAR IT LIVE</div>
          <svg viewBox="0 0 460 240" aria-hidden="true">
            <line x1="10" y1="197" x2="450" y2="197" stroke="var(--hair)" stroke-width="1"/>
            ''' + _EQ + '''
          </svg>
          <div class="pzt">实时<b>听见</b></div>
          <div class="pzs">声音进来的那一刻，它已经在听——不是录完、转写完，再来理解。</div>
        </div>
        <div class="prz rise" style="--i:4">
          <div class="pzk">02 · RECALL AT ONCE</div>
          <svg viewBox="0 0 460 240" aria-hidden="true">
            <g opacity=".28">
              <path class="stroke" stroke-width="1.2" d="M60 196 L150 58"/>
              <path class="stroke" stroke-width="1.2" d="M60 196 L250 96"/>
              <path class="stroke" stroke-width="1.2" d="M60 196 L398 140"/>
              <path class="stroke" stroke-width="1.2" d="M60 196 L296 178"/>
            </g>
            <g opacity=".4">
              <circle class="fill-ink" cx="150" cy="58" r="6"/>
              <circle class="fill-ink" cx="250" cy="96" r="6"/>
              <circle class="fill-ink" cx="398" cy="140" r="6"/>
              <circle class="fill-ink" cx="296" cy="178" r="6"/>
            </g>
            <path class="stroke-am" stroke-width="1.6" opacity=".55" d="M60 196 C 160 150, 260 90, 352 44"/>
            <path class="stroke-am pkt" style="--pl:24px;--p0:24px;--p1:-360px;--pt:2.2s" stroke-width="3.5" d="M60 196 C 160 150, 260 90, 352 44"/>
            <circle class="fill-am" cx="60" cy="196" r="9"/>
            <circle class="fill-co" cx="352" cy="44" r="7"/>
            <circle class="mring" cx="352" cy="44" r="7" fill="none" stroke="var(--coral)" stroke-width="2"/>
            <text class="lbl" x="60" y="228" text-anchor="middle" style="font-size:14px">这句话</text>
            <text class="lbl fill-co" x="352" y="24" text-anchor="middle" style="font-size:14px">上周那件事</text>
          </svg>
          <div class="pzt">立刻<b>想起</b></div>
          <div class="pzs">你提到上周的事，它不用去翻库——那段共同历史，本来就在场。</div>
        </div>
        <div class="prz rise" style="--i:6">
          <div class="pzk">03 · RESPOND IN THE MOMENT</div>
          <svg viewBox="0 0 460 240" aria-hidden="true">
            <path class="stroke" stroke-width="2" opacity=".45" d="M14 120 C 56 96, 88 150, 126 120 C 152 100, 178 140, 212 122"/>
            <circle class="fill-am" cx="234" cy="120" r="9"/>
            <circle class="mring" cx="234" cy="120" r="8" fill="none" stroke="var(--amber)" stroke-width="2"/>
            <circle class="mring" cx="234" cy="120" r="8" fill="none" stroke="var(--amber)" stroke-width="2" style="--d:.7s"/>
            <path class="stroke-am" stroke-width="2" opacity=".7" d="M248 120 H436"/>
            <path class="stroke-am pkt" style="--pl:20px;--p0:20px;--p1:-230px;--pt:1.3s" stroke-width="4.5" d="M248 120 H436"/>
            <text class="lbl" x="80" y="88" style="font-size:14px">话音未落</text>
            <text class="lbl fill-co" x="342" y="98" text-anchor="middle" style="font-size:14px">半秒之内</text>
          </svg>
          <div class="pzt">当下<b>回应</b></div>
          <div class="pzs">在这句话还热着的时候接住它——而不是三秒后给一个正确答案。</div>
        </div>
      </div>
      <div class="land flow rev" style="--i:8">三件事发生在同一秒里，才叫「在场」。<span class="s">记忆是资产，临场是引擎——下一页，讲那半秒。</span></div>
    </div>
  </div>
</section>'''

# ── 6.4-R4) 第四轮反馈（仅大会版） ──────────────────────────
# 2) 反共识页 · 三卡改行业案例（电商投诉 / 金融 / 导购）
rep1('''<div class="n">01</div>
          <div class="tag">高情绪 · 投诉升级</div>
          <div class="t">人要的不是方案<br>是有人认账</div>
          <div class="d">这种时候，一个「完全理解您的心情」的机器，是在火上浇油。</div>''',
     '''<div class="n">01</div>
          <div class="tag">电商 · 大促投诉升级</div>
          <div class="t">投诉的人要的不是方案<br>是有人认账</div>
          <div class="d">大促售后炸线的那晚，一句「完全理解您的心情」的机器话术，是在火上浇油。</div>''')
rep1('''<div class="n">02</div>
          <div class="tag">高不可逆 · 涉钱涉命</div>
          <div class="t">退款、退保<br>用药建议</div>
          <div class="d">错一次赔不起。不可逆的动作，永远要有一个人按下最后那一下。</div>''',
     '''<div class="n">02</div>
          <div class="tag">金融 · 涉钱不可逆</div>
          <div class="t">退保、赎回、调额<br>错一次赔不起</div>
          <div class="d">资金动作不可逆，也是监管红线——永远要有一个人按下最后那一下。</div>''')
rep1('''<div class="n">03</div>
          <div class="tag">高模糊 · 需求没想清</div>
          <div class="t">用户自己<br>都不知道要什么</div>
          <div class="d">这时候 Agent 只会把他越绕越远——它太会顺着说了。</div>''',
     '''<div class="n">03</div>
          <div class="tag">导购 · 高客单高模糊</div>
          <div class="t">客户自己<br>都没想清要买什么</div>
          <div class="d">大额消费的犹豫期，Agent 太会顺着说——只会把他越绕越远，最后谁都不下单。</div>''')

# 3) 灵魂拷问页 · 删左下角重复 cue（主问句已升为大标题）
rep1('''
    <div class="cue flow" style="--i:7">在座有多少人，亲手写过一份自己产品的评测集？</div>''', '')

# 4) 对组织说 · 标题突出「放权」（链式：作用于 R2 改后的标题）
rep1('<h2 class="ink" style="--i:1">对组织说：先分清哪些是<em>单向门</em>，哪些是<em>双向门</em></h2>',
     '<h2 class="ink" style="--i:1">对组织说：<em>放权</em>，从分清单向门与双向门开始</h2>')

# 5) 收束页 · 组织要的是放权，不是进化
rep1('<span class="no">要的不是 AI 能力</span><em>进化</em>',
     '<span class="no">要的不是 AI 能力</span><em>放权</em>')
rep1('<div class="s">Agent 有 L0–L4，人有看过·用过·学过·干过。组织真正的活，是让这两把梯子同步往上。</div>',
     '<div class="s">Agent 有 L0–L4，人有看过·用过·学过·干过——组织真正的活，是把权放到这两把梯子够得着的那一格。</div>')

# ── 6.4-R5) 第五轮反馈（仅大会版） ──────────────────────────
# 1) P37 全页重做：Eval 贯穿产品全生命周期的闭环主轴
rep1('<div class="eyebrow flow" style="--i:0">把上面两页接起来</div>',
     '<div class="eyebrow flow" style="--i:0">把上面两页接起来 · EVAL 贯穿全生命周期</div>')
rep1('<h2 class="ink" style="--i:1">评测不是质量流程，是计费基础设施</h2>',
     '<h2 class="ink" style="--i:1">同一把 Eval：对产品量<em>好坏</em>，对商业量<em>钱</em></h2>')
_ea = s.index('出题权 = 定价权')
assert s.count('出题权 = 定价权') == 1
_sv0 = s.rindex('<svg', 0, _ea)
_sv1 = s.index('</svg>', _ea) + len('</svg>')
EVAL_SVG = '''<svg viewBox="0 0 1680 330" width="1680" aria-hidden="true">
          <defs><linearGradient id="evsp" gradientUnits="userSpaceOnUse" x1="130" y1="0" x2="1530" y2="0">
            <stop offset="0" style="stop-color:var(--amber)"/><stop offset=".56" style="stop-color:var(--amber)"/>
            <stop offset=".68" style="stop-color:var(--coral)"/><stop offset="1" style="stop-color:var(--coral)"/>
          </linearGradient></defs>
          <path class="stroke dw" style="--len:1560;--i:8" stroke-width="1.4" stroke-dasharray="6 9" opacity=".6" d="M1530 148 C 1530 44, 130 44, 130 148"/>
          <path class="stroke-am pkt" style="--pl:26px;--p0:26px;--p1:-1560px;--pt:7s;--pd:2.6s" stroke-width="3" d="M1530 148 C 1530 44, 130 44, 130 148"/>
          <text class="lbl pop" style="--i:9" x="830" y="34" text-anchor="middle">闭环 · 商业结果，回灌下一轮产品规划</text>
          <path class="dw" style="--len:1400;--i:1" stroke="url(#evsp)" stroke-width="5" fill="none" d="M130 170 H1530"/>
          <path class="pkt" style="--pl:30px;--p0:30px;--p1:-1400px;--pt:5s" stroke="url(#evsp)" stroke-width="7" fill="none" d="M130 170 H1530"/>
          <g class="pop" style="--i:2">
            <circle class="fill-am" cx="130" cy="170" r="10"/>
            <text class="ttl" x="130" y="136" text-anchor="middle" style="font-size:26px">产品规划</text>
            <text class="sm" x="130" y="212" text-anchor="middle">评测即 PRD · 先定义「做对」</text>
          </g>
          <g class="pop" style="--i:3">
            <circle class="fill-am" cx="480" cy="170" r="10"/>
            <text class="ttl" x="480" y="136" text-anchor="middle" style="font-size:26px">产品打磨</text>
            <text class="sm" x="480" y="212" text-anchor="middle">交互质量 · 量产品好坏</text>
          </g>
          <g class="pop" style="--i:4">
            <circle class="fill-am" cx="830" cy="170" r="10"/>
            <text class="ttl" x="830" y="136" text-anchor="middle" style="font-size:26px">上线验收</text>
            <text class="sm" x="830" y="212" text-anchor="middle">模拟考核 · 敢不敢让它上岗</text>
          </g>
          <g class="pop" style="--i:5">
            <circle class="fill-co" cx="1180" cy="170" r="10"/>
            <text class="ttl" x="1180" y="136" text-anchor="middle" style="font-size:26px">计量计费</text>
            <text class="sm" x="1180" y="212" text-anchor="middle">判「解决」才收钱</text>
          </g>
          <g class="pop" style="--i:6">
            <circle class="fill-co" cx="1530" cy="170" r="13"/>
            <text class="ttl fill-co" x="1530" y="136" text-anchor="middle" style="font-size:26px">商业结果</text>
            <text class="sm" x="1530" y="212" text-anchor="middle">这个月的钱 · 结果生意</text>
          </g>
          <path class="stroke-co pop" style="--i:7" stroke-width="1.4" stroke-dasharray="5 7" d="M1005 120 V220"/>
          <text class="lbl fill-co pop" style="--i:7" x="1005" y="106" text-anchor="middle">出题权 = 定价权</text>
          <text class="lbl pop" style="--i:7" x="60" y="292">面向产品 · Eval 量的是「好不好」</text>
          <text class="lbl fill-co pop" style="--i:7" x="1620" y="292" text-anchor="end">面向商业 · Eval 量的是「钱」</text>
        </svg>'''
s = s[:_sv0] + EVAL_SVG + s[_sv1:]
rep1('<div class="land flow" style="--i:12">出题权的移交，就是信任的移交。<span class="s">',
     '<div class="land flow" style="--i:12">Eval 贯穿全生命周期：规划期它是 PRD，打磨期它量好坏，上线期它当考官，商业化它就是计费器——<b>从规划到回款，出题权一路没换过手。</b><span class="s">')

# 2) P42 标题：去掉 RTE Keynote 用词，直给读图结果
rep1('<h2 class="ink" style="--i:1">五年按场景排。<em>今年按岗位排，图就变了</em></h2>',
     '<h2 class="ink" style="--i:1">真实岗位放上梯子：今年的重心，压在 <em>L2 与 L3 之间</em></h2>')

# 3) 两道围栏页：围栏升为主标题，一读就懂；撤回键金句只留给黑页
rep1('<h2 class="ink" style="--i:1">延迟做到某个数之后，剩下的问题不是快，是<em>时机</em></h2>',
     '<h2 class="ink" style="--i:1">体验的围栏：交互行为，要有<em>规矩</em></h2>')
rep1('<div class="eyebrow flow" style="--i:0">体验的围栏 · FROM LATENCY TO TIMING</div>',
     '<div class="eyebrow flow" style="--i:0">FROM LATENCY TO TIMING · 延迟之后，剩下的问题是时机</div>')
rep1('<h2 class="ink" style="--i:1">文本有「撤回」。语音，<span class="co">没有撤回键</span></h2>',
     '<h2 class="ink" style="--i:1">执行的围栏：语音的动作，<span class="co">最难在半路拦住</span></h2>')
rep1('<div class="eyebrow coral flow" style="--i:0">执行的围栏 · 为什么语音天然更难拦</div>',
     '<div class="eyebrow coral flow" style="--i:0">ON EXECUTION · 为什么语音这一行门槛天然更高</div>')

# 4) 全景页：准入线固化句升为主标题，体系句降为副标题
rep1('<div class="eyebrow flow" style="--i:0">上一页的五条准入线，固化在这张图里 · 声网对话式 AI 全景</div>',
     '<div class="eyebrow flow" style="--i:0">交个底 · 这是一个体系，不是分散的产品点</div>')
rep1('<h2 class="ink" style="--i:1">这是一个体系，<em>不是分散的产品点</em></h2>',
     '<h2 class="ink" style="--i:1">五条准入线，固化在这张图里：<em>声网对话式 AI 全景</em></h2>')

# ── 6.4-R6) 终检修复（全篇 review 扫出的断链与不一致） ──────
# 1) 案例重编号：案例01(自问自答)已删，02–06 顺移为 01–05
for _a, _b in [('案例 02 · 真实生产环境', '案例 01 · 真实生产环境'),
               ('案例 03 · 岗位 01 · 外呼销售', '案例 02 · 岗位 01 · 外呼销售'),
               ('案例 04 · 今年这一行第一次被迫公开讨论的问题', '案例 03 · 今年这一行第一次被迫公开讨论的问题'),
               ('案例 05 · THE REPRESENTATION LAYER', '案例 04 · THE REPRESENTATION LAYER'),
               ('案例 06 · ELEVEN WEEKS ON SITE', '案例 05 · ELEVEN WEEKS ON SITE')]:
    assert s.count(_a) == 1, _a
    s = s.replace(_a, _b, 1)

# 2) 护栏案例页教训03：「下一页就发」指向已删的工牌页 → 改为第五幕交给组织
rep1('：替谁做、做什么、到哪里为止、如何披露、错了怎么办、怎么收回。下一页就发。',
     '：替谁做、做什么、到哪里为止、如何披露、错了怎么办、怎么收回。这张表，第五幕交给组织。')

# 3) 对组织说页：工牌悬空引用 → 接住第四幕的《Agent 授权书》
rep1('你已经给 Agent 发过工牌了——替谁做、做什么、到哪里为止、错了怎么办、怎么收回。',
     '第四幕那份《Agent 授权书》，已经把「替谁做、做什么、到哪里为止、错了怎么办、怎么收回」写给它了。')

# 4) 收束卡02 称谓统一（与「对产品管理者说」一致）
rep1('<div class="who">产品负责人</div>', '<div class="who">产品管理者</div>')

# 5) 收束页 land 重写：命中全篇（进化速度 = 放权速度，底气 = 亲手写的尺子）
rep1('<div class="land ctr flow" data-step="4" style="--i:4">四句话，其实是<em>同一张审批单</em> —— 要批的从来不是它能不能上岗，是<b>我们愿不愿意变</b>。<span class="s">批下来，团队名单上多一个<b>同事</b>；批不下来，再大的模型也只是<b>一个更贵的玩具</b>。</span></div>',
     '<div class="land ctr flow" data-step="4" style="--i:4">四句话，说的是同一件事：<em>它的进化速度，等于我们的放权速度</em>——而放权的底气，来自<b>亲手写的那把尺子</b>。<span class="s">尺子递得出去，名单上就多一个<b>同事</b>；递不出去，再大的模型也只是<b>一个更贵的玩具</b>。</span></div>')

# f) 结构调整：删 P16；P45(三把尺子)挪到 P42(岗位)后；P50(时机)挪到「语音没有撤回键」前；
#    终幕对调：先对个人(P57,P58)，再对产品经理(P56)
_starts = [m.start() for m in re.finditer(r'<section class="slide', s)]
_ends = [s.index('</section>', st) + len('</section>') for st in _starts]
for _i in range(len(_starts) - 1):
    assert s[_ends[_i]:_starts[_i+1]].strip() == '', "section 之间有非空内容，重排会丢"
_head, _tail = s[:_starts[0]], s[_ends[-1]:]
_secs = [s[_starts[_i]:_ends[_i]] for _i in range(len(_starts))]
assert len(_secs) == 65, f"母版应 65 页，实际 {len(_secs)}"
_secs.append(PRESENCE)                         # index 65 · 临场感新页
order = (list(range(0, 15))                    # P1–P15
         + [16]                                # 四种失败（P17 案例01 删）
         + [18, 19, 20, 21]                    # 伙伴感 · 身份 · 历史 · 档位遗忘
         + [65]                                # ★ 临场感（Part2 高光 · 新）
         + [22, 23, 24]                        # 那半秒 · 反共识 · MQ（视频页由媒体层锚定插入）
         + list(range(25, 38))                 # 第三幕全段
         + [38, 39, 40, 41]                    # 章节 · OKR · 爬梯 · 岗位
         + [44, 45, 46, 47, 48]                # 类比 → 协作审批 → 双护栏 → Waymo → 护城河MQ
         + [49, 42, 43]                        # 体验围栏(时机) → 执行围栏(撤回) → 撤回MQ
         + [52, 53]                            # 全景 · QoT（工牌/准入线删）
         + [54, 56, 55, 58, 59, 57, 60]        # 章节 · 对个人 · 对产品经理 · 对管理者 · 案例06 · CEO们 · 对组织
         + list(range(61, 65)))                # 尺子两面 · 回看(进化) · 收束 · 终页
assert sorted(order) == sorted([i for i in range(66) if i not in (15, 17, 50, 51)]), len(order)
s = _head + '\n'.join(_secs[o] for o in order) + _tail

# ── 6.5) 媒体层（仅大会版；母版/线上 /cowork 保持无媒体） ────
# a) P3 页内录音（真实外呼片段，完美嵌入，无需解说文字）
CHROME3 = '<div class="chrome"><span>PART 0 · 开场</span><span>3</span></div>'
assert s.count(CHROME3) == 1, "P3 chrome 定位失败"
AUDIO = (CHROME3 + '\n  <audio data-dm src="/media/cowork/p3-call.mp3" preload="auto"></audio>'
         '\n  <div class="dm-ind" aria-hidden="true"></div>')
s = s.replace(CHROME3, AUDIO, 1)

# b) P24 之后插入全幅视频页（陪伴类智能体 · 多模态交互 demo，无文字）
VIDEO = '''<section class="slide">
  <div class="vslide">
    <video data-dm src="/media/cowork/gemini-demo.mp4" preload="auto" playsinline></video>
    <div class="dm-ind" aria-hidden="true"></div>
  </div>
</section>
'''
# 内容锚定：插在「授权可以被收回」反共识页之后（跟随内容移动，不吃页码位移）
_vs = [m.start() for m in re.finditer(r'<section class="slide', s)]
assert len(_vs) == 62, f"试验层后应 62 页，实际 {len(_vs)}"
_ai = s.index('授权可以被收回——这不是失败')
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
/* 结尾页照常黑底 */
@media print{.chrome::after,.confcover::after{opacity:1;}}
/* 96.5% 页标题句 + 临场感高光页（内容试验层） */
.mega .mh{font-size:46px;font-weight:900;color:var(--ink);letter-spacing:.01em;margin-bottom:-4px;}
.prz3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:34px;margin-top:6px;}
.prz{border:1px solid var(--hair);border-radius:10px;padding:24px 26px 22px;background:var(--card-bg);display:flex;flex-direction:column;gap:12px;}
.prz svg{width:100%;height:auto;display:block;}
.pzk{font-family:var(--f-mono);font-size:13px;letter-spacing:.22em;color:var(--ink-3);}
.pzt{font-size:42px;font-weight:900;color:var(--ink);letter-spacing:.02em;}
.pzt b{color:var(--amber);}
.pzs{font-size:18px;line-height:1.7;color:var(--ink-2);font-weight:300;}
.prz svg .lbl{font-family:var(--f-mono);letter-spacing:.12em;fill:var(--ink-3);}
.prz svg .lbl.fill-co{fill:var(--coral);}
.prz svg .fill-am{fill:var(--amber);}
.prz svg .fill-co{fill:var(--coral);}
.prz svg .fill-ink{fill:var(--ink);}
.prz svg .stroke{stroke:var(--ink-2);fill:none;}
.prz svg .stroke-am{stroke:var(--amber);fill:none;}
@keyframes przeq{0%,100%{transform:scaleY(.16)}50%{transform:scaleY(1)}}
.eqb{transform-box:fill-box;transform-origin:50% 100%;animation:przeq 1.25s cubic-bezier(.45,0,.55,1) infinite;animation-delay:var(--d,0s);}
@keyframes przring{0%{r:8px;opacity:.9}75%{r:36px;opacity:0}100%{r:36px;opacity:0}}
.mring{animation:przring 2.1s ease-out infinite;animation-delay:var(--d,0s);}
/* 案例02 · 右侧 3.5% 拆解面板（内容试验层） */
.m35{position:absolute;right:120px;top:256px;width:560px;display:flex;flex-direction:column;gap:16px;}
.m35 .mk{font-family:var(--f-mono);font-size:14px;letter-spacing:.2em;color:var(--coral);margin-bottom:6px;}
.m35 .row{display:grid;grid-template-columns:64px 1fr;column-gap:16px;row-gap:7px;align-items:baseline;}
.m35 .row .n{font-family:var(--f-en);font-size:36px;font-weight:900;line-height:1;color:var(--ink);text-align:right;}
.m35 .row .t{font-size:20px;color:var(--ink-2);}
.m35 .row .bar{grid-column:2;height:7px;width:var(--w);background:var(--coral);opacity:.85;border-radius:2px;}
.m35 .sx{font-size:16px;line-height:1.7;color:var(--ink-3);border-top:1px solid var(--hair);padding-top:14px;margin-top:4px;}
.m35 .sx b{color:var(--ink-2);}
/* deck-media · 页内音视频（PPT 对齐：前进键先播，再按翻页） */
.dm-ind{position:absolute;right:64px;bottom:56px;width:10px;height:10px;border-radius:50%;background:var(--amber);opacity:0;transition:opacity .4s;z-index:40;}
.slide.dm-playing .dm-ind{opacity:.9;animation:dmpulse 1.1s ease-in-out infinite;}
@keyframes dmpulse{0%,100%{transform:scale(1);opacity:.9;}50%{transform:scale(1.55);opacity:.45;}}
.vslide{position:absolute;inset:0;background:#000;display:flex;align-items:center;justify-content:center;}
.vslide video{width:100%;height:100%;object-fit:contain;background:#000;}
"""
CONF_CSS = CONF_CSS.replace("__LOGO__", LOGO).replace("__COVER__", COVER).replace("__VENUE__", VENUE)
# 插到最后一个 </style> 前（主样式表尾部）
li = s.rindex("</style>")
s = s[:li] + CONF_CSS + s[li:]

open("public/decks/cowork-conf.html", "w", encoding="utf-8").write(s)
n = len(re.findall(r'<section class="slide', s))
assert n == 63, f"大会版应为 63 页，实际 {n}"
print(f"cowork-conf.html written · {n} slides · {len(s)//1024}KB")
assert "deckRuler" in s and "noindex" in s
print("ruler ✓ noindex ✓")
