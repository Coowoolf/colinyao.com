#!/usr/bin/env python3
"""cowork 第二轮重构：删 P36；47/48 升格案例 03/04；P8 加国内存量；
   插入 岗位全景(42)/产品全景(58)/四线汇总(63)；全局重编页码；封面 63→65。
   同一套操作应用于 站内 cowork.html 与 Vault V10 源文件。"""
import re, sys

# ───────────────────────── 新页 1 · 岗位全景（承接自治爬梯） ─────────────────────────
SLIDE_JOBS = '''<section class="slide">
  <div class="chrome"><span>PART 4 · 双向奔赴</span><span>42</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">上一页的梯子，放上真实岗位 · ON THE JOB</div>
      <h2 class="ink" style="--i:1">五年按场景排。<em>今年按岗位排，图就变了</em></h2>
    </div>
    <div class="body">
      <div class="fig flow" style="--i:2">
        <svg width="1640" height="470" viewBox="0 0 1640 470">
          <path class="stroke dw" style="--len:1400;--i:3" d="M190 400 H1590" stroke-width="1"/>
          <path class="stroke dw" style="--len:330;--i:3" d="M190 400 V70" stroke-width="1"/>
          <text class="lbl pop" style="--i:3" x="70" y="96">L4 主动</text>
          <text class="lbl pop" style="--i:3" x="70" y="176">L3 可执行</text>
          <text class="lbl pop" style="--i:3" x="70" y="256">L2 只读应答</text>
          <text class="lbl pop" style="--i:3" x="70" y="336">L0–L1</text>
          <rect class="pop" style="--i:4" x="190" y="150" width="1400" height="120" fill="var(--on-fill)"/>
          <text class="sm pop" style="--i:4" x="1580" y="142" text-anchor="end" fill="var(--amber)">今年整体重心：L2 与 L3 之间</text>
          <g data-step="1">
            <circle class="pop" style="--i:0" cx="290" cy="96" r="26" fill="var(--amber)" opacity=".85"/>
            <text class="txt pop" style="--i:0" x="290" y="440" text-anchor="middle">外呼销售</text>
            <circle class="pop" style="--i:1" cx="480" cy="216" r="21" fill="var(--amber)" opacity=".7"/>
            <text class="txt pop" style="--i:1" x="480" y="440" text-anchor="middle">客服与随访</text>
          </g>
          <g data-step="2">
            <circle class="pop" style="--i:0" cx="670" cy="316" r="24" fill="var(--ink-3)" opacity=".8"/>
            <text class="txt pop" style="--i:0" x="670" y="440" text-anchor="middle">陪伴</text>
            <circle class="pop" style="--i:1" cx="860" cy="256" r="16" fill="var(--ink-3)" opacity=".7"/>
            <text class="txt pop" style="--i:1" x="860" y="440" text-anchor="middle">教练 / 助教</text>
          </g>
          <g data-step="3">
            <circle class="pop" style="--i:0" cx="1050" cy="176" r="13" fill="var(--coral)" opacity=".75"/>
            <text class="txt pop" style="--i:0" x="1050" y="440" text-anchor="middle">调度</text>
            <circle class="pop" style="--i:1" cx="1240" cy="256" r="11" fill="var(--ink-3)" opacity=".65"/>
            <text class="txt pop" style="--i:1" x="1240" y="440" text-anchor="middle">巡检</text>
          </g>
          <g data-step="4">
            <circle class="pop" style="--i:0" cx="1420" cy="296" r="15" fill="var(--ink-3)" opacity=".7"/>
            <text class="txt pop" style="--i:0" x="1420" y="440" text-anchor="middle">翻译</text>
            <circle class="pop" style="--i:1" cx="1560" cy="336" r="10" fill="var(--coral)" opacity=".6"/>
            <text class="txt pop" style="--i:1" x="1560" y="440" text-anchor="middle">护理与助障</text>
          </g>
          <text class="lbl pop" style="--i:5" x="190" y="52">圆点大小 = 用量 · 暖橙 = 已规模商业化 · 灰 = 早期 · 粉 = 强监管场景</text>
        </svg>
      </div>
      <div class="tri" data-step="4">
        <div class="col flow" style="--i:0"><div class="k">读图规则 01</div><div class="v"><b>越靠上不等于越成熟</b>，只等于人退得越远。</div></div>
        <div class="col flow" style="--i:1"><div class="k">读图规则 02</div><div class="v">商业化最快的那一列，<b>未必是自治级别最高的那一列</b>。</div></div>
        <div class="col flow" style="--i:2"><div class="k">读图规则 03</div><div class="v">客户现在不问「这个场景能不能做」，<b>他们问「这个岗位能不能交」</b>。</div></div>
      </div>
      <div class="foot flow rev" style="--i:6" data-step="4">数据来源 · 声网研究院 + RTE 开发者社区 + 客户实测 · 2026</div>
    </div>
  </div>
</section>'''

# ───────────────────────── 新页 2 · 产品全景（案例 05 之后交个底） ─────────────────────────
SLIDE_MATRIX = '''<section class="slide">
  <div class="chrome"><span>PART 5 · 人与组织 · 交个底</span><span>58</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">上一页的「默认值」，固化在这张图里 · 声网对话式 AI 全景</div>
      <h2 class="ink" style="--i:1">这是一个体系，<em>不是分散的产品点</em></h2>
    </div>
    <div class="body">
      <div class="fig flow" style="--i:2">
        <svg width="1640" height="500" viewBox="0 0 1640 500">
          <text class="lbl pop" style="--i:3" x="60" y="40">能力 →</text>
          <text class="lbl pop" style="--i:3" x="330" y="40" text-anchor="middle">实时感知</text>
          <text class="lbl pop" style="--i:3" x="580" y="40" text-anchor="middle">自然轮次</text>
          <text class="lbl pop" style="--i:3" x="830" y="40" text-anchor="middle">上下文理解</text>
          <text class="lbl pop" style="--i:3" x="1080" y="40" text-anchor="middle">多模态表达</text>
          <text class="lbl pop" style="--i:3" x="1330" y="40" text-anchor="middle">任务执行</text>
          <path class="stroke dw" style="--len:1400;--i:3" d="M200 62 H1460" stroke-width="1"/>
          <path class="stroke dw" style="--len:400;--i:3" d="M200 62 V450" stroke-width="1"/>
          <g data-step="1">
            <text class="ttl pop" style="--i:0" x="60" y="116" style="font-size:26px">Call Agent</text>
            <text class="sm pop" style="--i:0" x="60" y="142">电话智能体</text>
            <circle class="pop" style="--i:0" cx="330" cy="118" r="17" fill="var(--amber)" opacity=".85"/>
            <circle class="pop" style="--i:0" cx="580" cy="118" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="830" cy="118" r="15" fill="var(--amber)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="1080" cy="118" r="10" fill="var(--ink-3)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="1330" cy="118" r="21" fill="var(--amber)"/>
          </g>
          <g data-step="2">
            <text class="ttl pop" style="--i:0" x="60" y="216" style="font-size:26px">Physical AI</text>
            <text class="sm pop" style="--i:0" x="60" y="242">硬件与具身</text>
            <circle class="pop" style="--i:0" cx="330" cy="218" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="580" cy="218" r="15" fill="var(--amber)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="830" cy="218" r="17" fill="var(--amber)" opacity=".85"/>
            <circle class="pop" style="--i:0" cx="1080" cy="218" r="19" fill="var(--amber)" opacity=".9"/>
            <circle class="pop" style="--i:0" cx="1330" cy="218" r="10" fill="var(--ink-3)" opacity=".7"/>
          </g>
          <g data-step="3">
            <text class="ttl pop" style="--i:0" x="60" y="316" style="font-size:26px">STT</text>
            <text class="sm pop" style="--i:0" x="60" y="342">实时转写</text>
            <circle class="pop" style="--i:0" cx="330" cy="318" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="580" cy="318" r="12" fill="var(--ink-3)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="830" cy="318" r="12" fill="var(--ink-3)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="1080" cy="318" r="17" fill="var(--amber)" opacity=".85"/>
            <circle class="pop" style="--i:0" cx="1330" cy="318" r="8" fill="var(--ink-3)" opacity=".6"/>
          </g>
          <g data-step="4">
            <text class="ttl pop" style="--i:0" x="60" y="416" style="font-size:26px">ConvoAI Engine</text>
            <text class="sm pop" style="--i:0" x="60" y="442">通用引擎</text>
            <circle class="pop" style="--i:0" cx="330" cy="418" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="580" cy="418" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="830" cy="418" r="19" fill="var(--amber)" opacity=".9"/>
            <circle class="pop" style="--i:0" cx="1080" cy="418" r="19" fill="var(--amber)" opacity=".9"/>
            <circle class="pop" style="--i:0" cx="1330" cy="418" r="19" fill="var(--amber)" opacity=".9"/>
          </g>
          <text class="lbl pop" style="--i:4" x="1500" y="480" text-anchor="end">圆点大小 = 该产品线在这一格的投入强度</text>
        </svg>
      </div>
      <div class="note flow" style="--i:5" data-step="4">这张图想说的只有一句：<b>四条产品线不是四个赛道，是同一个能力模型的四个切片。</b>任何一格的进步，四条线一起受益 —— 客户现场沉淀的每一个「默认值」，都会长进某一格里。</div>
    </div>
  </div>
</section>'''

# ───────────────────────── 新页 3 · 四线汇总（收束之前） ─────────────────────────
SLIDE_FOUR = '''<section class="slide">
  <div class="chrome"><span>PART 5 · 人与组织 · 全场回看</span><span>63</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">全场回看 · FOUR LINES, ONE WORD</div>
      <h2 class="ink" style="--i:1">四条线，走到了<em>同一个词</em></h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 520" width="1680" aria-hidden="true">
          <!-- 线一 · 我的主题 -->
          <g>
            <text class="lbl pop" style="--i:0" x="0" y="58">线一 · 我讲的主题</text>
            <path class="stroke dw" style="--len:1140;--i:1" stroke-width="1.4" d="M130 88 H1270"/>
            <circle class="fill-ink pop" style="--i:2" cx="320" cy="88" r="7"/>
            <text class="txt pop" style="--i:2" x="320" y="66" text-anchor="middle">生成式 AI × 实时互动</text>
            <text class="lbl pop" style="--i:2" x="320" y="122" text-anchor="middle">2024</text>
            <circle class="fill-ink pop" style="--i:3" cx="720" cy="88" r="7"/>
            <text class="txt pop" style="--i:3" x="720" y="66" text-anchor="middle">活人感 → 体验基准</text>
            <text class="lbl pop" style="--i:3" x="720" y="122" text-anchor="middle">2025</text>
            <circle class="fill-am pop" style="--i:4" cx="1120" cy="88" r="8"/>
            <text class="txt pop" style="--i:4" x="1120" y="66" text-anchor="middle">被托付 → 双向奔赴</text>
            <text class="lbl pop" style="--i:4" x="1120" y="122" text-anchor="middle">2026</text>
          </g>
          <!-- 线二 · 给产品经理的话 -->
          <g data-step="1">
            <text class="lbl pop" style="--i:0" x="0" y="174">线二 · 给产品经理的话</text>
            <path class="stroke dw" style="--len:1140;--i:0" stroke-width="1.4" d="M130 204 H1270"/>
            <circle class="fill-ink pop" style="--i:1" cx="320" cy="204" r="7"/>
            <text class="txt pop" style="--i:1" x="320" y="182" text-anchor="middle">职能边界开始融合</text>
            <circle class="fill-ink pop" style="--i:2" cx="720" cy="204" r="7"/>
            <text class="txt pop" style="--i:2" x="720" y="182" text-anchor="middle">能实验，就不等共识</text>
            <circle class="fill-am pop" style="--i:3" cx="1120" cy="204" r="8"/>
            <text class="txt pop" style="--i:3" x="1120" y="182" text-anchor="middle">交一套能跑通的评测</text>
          </g>
          <!-- 线三 · 我们的产品 -->
          <g data-step="2">
            <text class="lbl pop" style="--i:0" x="0" y="290">线三 · 我们的引擎</text>
            <path class="stroke dw" style="--len:1140;--i:0" stroke-width="1.4" d="M130 320 H1270"/>
            <circle class="fill-ink pop" style="--i:1" cx="320" cy="320" r="7"/>
            <text class="txt pop" style="--i:1" x="320" y="298" text-anchor="middle">1.0 能对话</text>
            <text class="lbl pop" style="--i:1" x="320" y="354" text-anchor="middle">2025.03</text>
            <circle class="fill-ink pop" style="--i:2" cx="720" cy="320" r="7"/>
            <text class="txt pop" style="--i:2" x="720" y="298" text-anchor="middle">2.0 能上岗 · 电话接入</text>
            <text class="lbl pop" style="--i:2" x="720" y="354" text-anchor="middle">2025.10</text>
            <circle class="fill-am pop" style="--i:3" cx="1120" cy="320" r="8"/>
            <text class="txt pop" style="--i:3" x="1120" y="298" text-anchor="middle">2.x 会用工具 · 打断解耦</text>
            <text class="lbl pop" style="--i:3" x="1120" y="354" text-anchor="middle">2026</text>
          </g>
          <!-- 线四 · 对话式智能体 -->
          <g data-step="3">
            <text class="lbl pop" style="--i:0" x="0" y="406">线四 · 对话式智能体</text>
            <path class="stroke dw" style="--len:1140;--i:0" stroke-width="1.4" d="M130 436 H1270"/>
            <circle class="fill-ink pop" style="--i:1" cx="320" cy="436" r="7"/>
            <text class="txt pop" style="--i:1" x="320" y="414" text-anchor="middle">被使用 · QoS</text>
            <circle class="fill-ink pop" style="--i:2" cx="720" cy="436" r="7"/>
            <text class="txt pop" style="--i:2" x="720" y="414" text-anchor="middle">被记住 · QoE</text>
            <circle class="fill-am pop" style="--i:3" cx="1120" cy="436" r="8"/>
            <text class="txt pop" style="--i:3" x="1120" y="414" text-anchor="middle">被托付 · QoI</text>
          </g>
          <!-- 汇合 · 共事 -->
          <g data-step="4">
            <path class="stroke-am dw" style="--len:420;--i:0" stroke-width="1.6" d="M1270 88 C 1400 88, 1440 210, 1508 246"/>
            <path class="stroke-am dw" style="--len:360;--i:1" stroke-width="1.6" d="M1270 204 C 1390 204, 1440 232, 1508 252"/>
            <path class="stroke-am dw" style="--len:360;--i:2" stroke-width="1.6" d="M1270 320 C 1390 320, 1440 282, 1508 262"/>
            <path class="stroke-am dw" style="--len:420;--i:3" stroke-width="1.6" d="M1270 436 C 1400 436, 1440 300, 1508 268"/>
            <circle class="fill-am pop" style="--i:4" cx="1545" cy="256" r="15"/>
            <g class="pop" style="--i:5"><text class="ttl fill-am" x="1545" y="212" text-anchor="middle" style="font-size:38px">共事</text></g>
            <text class="lbl fill-am pop" style="--i:6" x="1545" y="312" text-anchor="middle">COWORK · QoT</text>
          </g>
        </svg>
      </div>
      <div class="note" data-step="4"><span class="flow" style="--i:7">主题在走，话在变，产品在迭代，智能体在爬梯 —— 四条线互不商量，却在同一年、同一个词上会合。<b>共事不是我挑的词，是四条线自己走到的。</b></span></div>
      <div class="foot flow rev" style="--i:8" data-step="4">第一条线是我讲的 · 第二条是给你的 · 第三条是我们做的 · 第四条是它自己走的 —— 带走这一页，就带走了整场</div>
    </div>
  </div>
</section>'''

# ───────────────────────── 页内文本编辑 ─────────────────────────
INLINE = [
 # 47 → 案例 03（补 CASE 链路）
 ('<div class="chrome"><span>PART 4 · 双向奔赴</span><span>47</span></div>\n  <div class="wrap">\n    <div class="head">\n      <div class="eyebrow coral flow" style="--i:0">案例 04 · 今年这一行第一次被迫公开讨论的问题</div>',
  '<div class="chrome"><span>PART 4 · 双向奔赴 · CASE</span><span>47</span></div>\n  <div class="wrap">\n    <div class="head">\n      <div class="eyebrow coral flow" style="--i:0">案例 03 · 今年这一行第一次被迫公开讨论的问题</div>'),
 # 48 → 案例 04
 ('<div class="chrome"><span>PART 4 · 双向奔赴</span><span>48</span></div>',
  '<div class="chrome"><span>PART 4 · 双向奔赴 · CASE</span><span>48</span></div>'),
 ('<div class="eyebrow flow" style="--i:0">技术前提 · THE REPRESENTATION LAYER · 一次有惊无险的刹车</div>',
  '<div class="eyebrow flow" style="--i:0">案例 04 · THE REPRESENTATION LAYER · 一次有惊无险的刹车</div>'),
 # P8 · 国内存量一拍（加在卡片和 foot 之间）
 ('<div class="foot flow rev" style="--i:8">整个 conversational AI，从一个技术选项，变成了预算科目 · 数据截至 2026 年公开信息</div>',
  '<div class="note flow" style="--i:8">这还只是海外。国内不用看故事，看存量：中国呼叫中心全口径投资盘 <b>¥5,850 亿</b>，其中 <b>&gt;2,000 亿</b>是纯技术改造空间，而 AI 语音坐席的综合成本只有人工的 <b>15–20%</b> —— 钱不在风口上，早就趴在预算科目里。</div>\n      <div class="foot flow rev" style="--i:9">整个 conversational AI，从一个技术选项，变成了预算科目 · 海外数据截至 2026 公开信息 · 国内存量口径：CC-CMM / 艾媒咨询</div>'),
 # 封面页数
 ('40 min · 63 slides', '40 min · 65 slides'),
]

def restructure(path):
    s = open(path, encoding="utf-8").read()
    for i, (old, new) in enumerate(INLINE):
        assert s.count(old) == 1, f"{path}: inline {i} not unique: {old[:60]!r}"
        s = s.replace(old, new)
    # 切片
    spans = [(m.start(), m.end()) for m in re.finditer(r'<section class="slide[^"]*"[^>]*>.*?</section>', s, re.S)]
    assert len(spans) == 63, f"{path}: {len(spans)} slides"
    slides = [s[a:b] for a, b in spans]
    prefix, suffix = s[:spans[0][0]], s[spans[-1][1]:]
    assert '案例 03 · 同一年' in slides[35]  # 要删的那页
    del slides[35]                                  # 删旧 36
    slides.insert(41, SLIDE_JOBS)                   # 自治爬梯(41) 之后 → 42
    slides.insert(57, SLIDE_MATRIX)                 # 案例 05(57) 之后 → 58
    slides.insert(62, SLIDE_FOUR)                   # 尺子两面(62) 之后 → 63
    assert len(slides) == 65
    # 全局重编 chrome 页码
    out = []
    for i, sl in enumerate(slides, 1):
        sl2, n = re.subn(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)',
                         lambda m: m.group(1) + str(i) + m.group(2), sl, count=1)
        out.append(sl2)
    body = "\n".join(out)
    open(path, "w", encoding="utf-8").write(prefix + body + suffix)
    # 校验：案例编号连续
    got = re.findall(r'案例 0(\d)', prefix + body + suffix)
    print(path.split("/")[-1], "→ 65 slides · 案例序:", sorted(set(got)))

restructure("public/decks/cowork.html")
restructure("/mnt/user-data/outputs/V10_从被托付到共事_浅底.html")
print("OK")
