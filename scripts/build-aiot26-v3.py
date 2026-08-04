#!/usr/bin/env python3
"""aiot26-v3 · 《AI 有了身体，为什么还是三天进抽屉？》—— 终版（35 页 · 五幕 · 默认浅底）。

  规划来源：Vault《2026-08-09_AI产品大会_AIoT专场_V1V2评审与终版规划》
  一句话：V2 的骨架与诚实度 + V1 的幕结构与金句页 + 三处两版都漏掉的补位。

  底盘：public/decks/aiot26-v2.html（样式 / 控制器 / deck-media / deckRuler / 默认 light）
  留 V2：抽屉曲线 · demo · 身体≠伙伴 · 两种价值逻辑 · 三乘数总图 · 三个乘数拆页 ·
         身体的意义 · 恰好半秒 · 两种延迟 · 北极星 · 多模态时序 · 选择性注意 · 端云 ·
         故障恢复 · 四方责任表 · 标准化接口 · 评测闭环 · 三个动作 · 回到抽屉
  取 V1：幕卡与金句页型 + 3 颗金句（上下半场 / 陌生人 / 生死线）+ 21g 终页
  五幕：01 分辨 / 02 三个乘数 / 03 那半秒 / 04 在房间里 / 05 交出去（开场先给一页路线图）
  新写：P02 续集钩子（挂 2025.12 人人都是 PM 大会，不是 0516）· P07 反共识改写（分组而非泼冷水）
        · P24 AMA 真实提问（两版都删了的一线可信度页）· 路线图 + 五张幕卡（讲述版结构）
  删掉：V2 的 分界线 / 一条真实链路 / 全景独立页 / 独立谢谢页（后两者折进 P27 与 P31）

  场合：2026 AI 产品大会 · 声网 AIoT 专场 · 2026.08.09 北京 · 30 min。
"""
import re

# 幕卡 / 金句页型取自 Fable 那版 35 页 aiot26（已保存为 _src-；
# 现在的 aiot26.html 是重建后的 40 页保底版，页数与索引都不同）
V1 = open("public/decks/_src-aiot26-fable35.html", encoding="utf-8").read()
V2 = open("public/decks/aiot26-v2.html", encoding="utf-8").read()
SEC = re.compile(r'<section class="slide[^"]*">.*?</section>', re.S)
a = SEC.findall(V1)
b = SEC.findall(V2)
assert len(a) == 35 and len(b) == 26, (len(a), len(b))

head = V2[:V2.index('<section class="slide')]
tail = V2[V2.rindex('</section>') + len('</section>'):]


def one(hay, old, new):
    assert hay.count(old) == 1, "锚点失效: " + old[:70]
    return hay.replace(old, new, 1)


# ═══════════════════════════════════════════════════════════════
# 一、底盘：沿用 V2（已是默认 light / swap 隐藏 / noindex），只换标题
# ═══════════════════════════════════════════════════════════════
head = re.sub(r'<title>[^<]*</title>',
              '<title>AI 有了身体，为什么还是三天进抽屉？· 2026 AI 产品大会 AIoT 专场 · 终版</title>',
              head, count=1)

V3_CSS = """
/* ═════════ aiot26-v3 层 ═════════
   幕卡与金句页从 V1 移植回来，需要 .act / .mq 两个页型的节奏参数；
   底盘 V2 已把 --step 收到 58ms，金句页在这个步进下略显急，单独放宽。 */
.mq .q i{--step:96ms;}
.act .cn,.act .en{--step:88ms;}
/* AMA 提问页：who 只放编号，角色落在右栏 src，避免 190px 槽被中文撑破 */
.quotes.ama .r .who{width:110px;}
.quotes.ama .r .src{width:300px;}
.quotes.ama .r .say{font-size:27px;}
</style>"""
_k = head.rindex('</style>')          # 挂在最后一段样式之后，确保覆盖 V2 层
head = head[:_k] + V3_CSS + head[_k + len('</style>'):]


def act(num, en, cn, d):
    return ('<section class="slide">\n  <div class="act">\n'
            '    <div class="num flow" style="--i:0">ACT %s</div>\n'
            '    <div class="en settle" style="--i:1">%s</div>\n'
            '    <div class="cn spread" style="--i:3">%s</div>\n'
            '    <div class="d flow" style="--i:4">%s</div>\n'
            '  </div>\n</section>' % (num, en, cn, d))


def mq(mark, l1, l2, s):
    return ('<section class="slide">\n  <div class="mq">\n'
            '    <div class="mark flow" style="--i:0">%s</div>\n'
            '    <div class="q">\n'
            '      <i class="rise" style="--i:1">%s</i>\n'
            '      <i class="rise" style="--i:3">%s</i>\n'
            '    </div>\n    <div class="rule"></div>\n'
            '    <div class="s rise" style="--i:5">%s</div>\n'
            '  </div>\n</section>' % (mark, l1, l2, s))


# ═══════════════════════════════════════════════════════════════
# 二、页面
# ═══════════════════════════════════════════════════════════════

# ── P01 · 封面（V2 封面 + 页数订正） ─────────────────────────────
P01 = one(b[0], '30 min · 26 slides', '30 min · 35 slides')

# ── 路线图（新写）· 开场就把五幕交代清楚 ────────────────────────
#   30 分钟的演讲，听众需要知道自己在哪一步。这一页是「好听」的关键：
#   五个幕名都 ≤4 字，正好压进 .rows .k 的 190px 槽。
ROADMAP = '''<section class="slide">
  <div class="chrome"><span>路线图 · THE ROUTE</span><span>05</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">接下来 30 分钟，我们走五步</div>
      <h2 class="ink" style="--i:1">从「该不该做」，走到「回去做什么」</h2>
    </div>
    <div class="body">
      <div class="rows">
        <div class="r flow" style="--i:2"><span class="n">01</span><span class="k">分辨</span><span class="v">同一批技术，两套评价体系。先确定你的产品该不该被记住——这一步决定后面 25 分钟跟你有没有关系。</span></div>
        <div class="r flow" style="--i:3"><span class="n">02</span><span class="k">三个乘数</span><span class="v">今天唯一需要你带走的框架：伙伴感 = 角色一致性 × 共同历史 × 可控临场。</span></div>
        <div class="r flow" style="--i:4"><span class="n">03</span><span class="k">那半秒</span><span class="v">有了身体，第一个变难的是时间。什么时候开口，比开口说什么更早决定体验。</span></div>
        <div class="r flow" style="--i:4"><span class="n">04</span><span class="k">在房间里</span><span class="v">把设备放进真实的客厅、教室和车里：同时听、同时看、同时动，断了还要能回来。</span></div>
        <div class="r flow" style="--i:5"><span class="n">05</span><span class="k">交出去</span><span class="v">哪些题不该你解，哪些事只有你能做。把破局落成责任边界，和一张能每周重跑的评测。</span></div>
      </div>
      <div class="land flow" style="--i:5">前两步讲判断，中间两步讲工程，最后一步讲交付。<b>你只需要记住第 02 步那一行公式，其余都是它的展开。</b></div>
    </div>
  </div>
</section>'''

# ── P02 · 续集钩子（新写）─────────────────────────────────────
#   两版都做错的地方：V1 把续集挂在 0516 深圳 RTE 场，可这批听众没看过那场；
#   他们看过的是 2025.12 同一个大会的「活人感」。钩子必须挂对前作。
P02 = '''<section class="slide">
  <div class="chrome"><span>接上一场 · THE SEQUEL</span><span>02</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">先说清楚今天和上次的关系</div>
      <h2 class="ink" style="--i:1">去年我在这个台上讲怎么让它像个活人，今天它有了身体</h2>
    </div>
    <div class="body">
      <div class="g2">
        <div class="card rise" style="--i:2">
          <div class="tag">2025.12 · 人人都是产品经理大会</div>
          <div class="t">「活人感」</div>
          <div class="d">那一场讲的是屏幕里的声音：怎么让它说话的节奏、语气和分寸，不像一台机器。结论是把体验拆成可测的基准。</div>
          <div class="d"><b>那时候的题：</b>它说话像不像一个人。</div>
        </div>
        <div class="card on rise" style="--i:3">
          <div class="tag">2026.08 · 今天</div>
          <div class="t">有了身体之后</div>
          <div class="d">它从屏幕里走出来，会看、会转头、会伸手，也会在客厅里当着一屋子人开口。能力清单长了一大截。</div>
          <div class="d"><b>今天的题：</b>像个人，为什么还是留不住。</div>
        </div>
      </div>
      <div class="land flow" style="--i:4">像不像一个人，是上一场的题。<b>值不值得被留下来，是今天这一场的题。</b></div>
      <div class="foot src flow" style="--i:5">前作 · 《从「活人感」缺失到体验基准打造》2025.12 · 同一个大会</div>
    </div>
  </div>
</section>'''

# ── P03/P04 · 抽屉曲线 + demo（V2 原样）──────────────────────────
P03, P04 = b[1], b[2]

# ── P05/P06 · 身体≠伙伴 / 两种价值逻辑 ──────────────────────────
#   事实订正：V2 把 Gemini Robotics On-Device（2025.06）放进「今年确实发生了」，差了一年。
#   换成 2026.07.30 的 Gemini Robotics 2 / On-Device 2——离这场只有十天，台上更硬。
P05 = one(b[3],
          'NVIDIA 发布新一代 Cosmos 3 世界模型；Google DeepMind 发布可在机器人本体上离线运行的 '
          'Gemini Robotics On-Device。看见和动起来的门槛，这一年是真的降下来了。',
          'NVIDIA 在 6 月发布 Cosmos 3 世界模型；Google DeepMind 在 7 月底发布 Gemini Robotics 2，'
          '连同可在机器人本体上离线运行的 On-Device 2。看见和动起来的门槛，这一年是真的降下来了。')
P05 = one(P05,
          '来源 · NVIDIA newsroom（Cosmos 3 世界模型）· Google DeepMind blog（Gemini Robotics On-Device）',
          '来源 · NVIDIA newsroom · Cosmos 3（2026.06.01）｜ Google DeepMind · Gemini Robotics 2 / '
          'On-Device 2（2026.07.30）')
P06 = b[4]

# ── P07 · 反共识改写（新写）───────────────────────────────────
#   0516 与 V1 的反共识是「泼冷水」；对 PM 听众更有用的是「分组」——
#   让每个人在这一页对号入座，后面每一页才与他有关。
P07 = '''<section class="slide">
  <div class="chrome"><span>先分组 · A COUNTER-CONSENSUS</span><span>07</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">在往下讲之前，请先给自己的产品选一边</div>
      <h2 class="ink" style="--i:1">不是所有硬件都该做成伙伴，有三类做了反而是负担</h2>
    </div>
    <div class="body">
      <div class="g3">
        <div class="card rise" style="--i:2">
          <div class="tag">CASE 01 · 工具属性极强</div>
          <div class="t">扫地机 · 智能门锁 · 安防摄像头</div>
          <div class="d">用户要的是一个每次都靠得住的工具。给它加人格，只会让人觉得吵。</div>
        </div>
        <div class="card rise" style="--i:3">
          <div class="tag">CASE 02 · 一次性服务</div>
          <div class="t">展会接待 · 临时导游 · 酒店前台</div>
          <div class="d">用户根本不打算跟它建立关系。它只需要在这五分钟里把事办明白。</div>
        </div>
        <div class="card warn rise" style="--i:4">
          <div class="tag">CASE 03 · 隐私敏感</div>
          <div class="t">医疗设备 · 银行 KIOSK · 政务服务</div>
          <div class="d">这里的伙伴感会直接触发不信任——它越像懂你，你越不想让它记住你。</div>
        </div>
      </div>
      <div class="note flow" style="--i:5">所以这一页不是泼冷水，是分组：<b>如果你在上面这三格里，接下来二十分钟你可以放松地听；如果你不在，那接下来每一页都是你的事。</b></div>
      <div class="land flow" style="--i:5">真正的产品判断，从来不是「我能不能做成伙伴」。<b>是「我的产品，值不值得被记住」。</b></div>
    </div>
  </div>
</section>'''

# ── P08 · MQ 01（V1 最好的原创金句）────────────────────────────
P08 = mq('MONEY QUOTE · 01',
         '上半场，造能干活的身体；',
         '下半场，造值得被记住的存在。',
         '两个半场共用技术，不共用尺子。')

# ── 五张幕卡 · 每张都回答「这一幕要解决什么」──────────────────
ACT1 = act('01', 'THE DIVIDE', '分辨',
           '同一批技术，两套完全不同的评价体系。先确定你的产品该不该被记住——'
           '这一步决定后面 25 分钟跟你有没有关系。')
ACT2 = act('02', 'THE MULTIPLIERS', '三个乘数',
           '关系不是加出来的，是乘出来的。接下来四页，是今天唯一需要你带走的框架。')
ACT3 = act('03', 'THE HALF-SECOND', '那半秒',
           '有了身体，第一个变难的是时间。什么时候开口，比开口说什么更早决定体验。')
ACT4 = act('04', 'IN THE ROOM', '在房间里',
           '把设备放进真实的客厅、教室和车里：同时听、同时看、同时动，断了还要能回来。')
ACT5 = act('05', 'THE HANDOFF', '交出去',
           '哪些题不该你解，哪些事只有你能做。这一幕把破局落成责任边界，和一张能每周重跑的评测。')

# ── P10–P13 · 三乘数总图 + 三个乘数 ────────────────────────────
# 全场拍照页之一：先让公式和三张卡片自己立住，再补「这是乘法不是加法」那一刀。
P10 = one(b[6], '<div class="note flow" style="--i:6">这是乘法，不是加法',
          '<div class="note flow" data-step="1" style="--i:6">这是乘法，不是加法')
# 与主论坛 keynote 对齐（/cowork-conf PART 2「被记住」P15「伙伴感 = 三份产品资产 × 一个实时引擎」）：
# 三个乘数是同一张图换一种切法——角色一致性=身份那份资产，共同历史=关系+历史两份，
# 可控临场=那个引擎。不挂钩的话，听过主论坛的人会以为公式换了。
P10 = one(P10, '<b>接下来三页，一项一项拆。</b></div>',
          '<b>接下来三页，一项一项拆。</b></div>\n'
          '      <div class="foot flow" style="--i:6">这就是主论坛那张'
          '「伙伴感 = 三份产品资产 × 一个实时引擎」换一种切法：'
          '角色一致性是身份那份资产，共同历史是关系与历史两份，可控临场就是那个引擎。</div>')
# 快闸修一：V2 这条 h2 满宽溢出（60px × 需 1876px > 可用 1680px），
# 且 .ink 的 mask 会啃掉末字。把 system prompt 那半句降到眉标。
P11 = one(b[7],
          '<div class="eyebrow flow" style="--i:0">乘数一 · 角色一致性</div>\n'
          '      <h2 class="ink" style="--i:1">角色不是起个名字，也不是一段 system prompt，是一套稳定的判断方式</h2>',
          '<div class="eyebrow flow" style="--i:0">乘数一 · 角色一致性 —— 也不是一段 system prompt</div>\n'
          '      <h2 class="ink" style="--i:1">角色不是起个名字，是一套稳定的判断方式</h2>')
P12 = b[8]
# 乘数三 · 可控临场 —— 主论坛 P19 的「实时听见 × 立刻想起 × 当下回应」是金标准，
# 必须先出现；五步环降级为它的展开（有了身体多一环：行动收不回来 → 可恢复行动）。
P13 = one(b[9],
          '<div class="eyebrow flow" style="--i:0">乘数三 · 可控临场</div>\n'
          '      <h2 class="ink" style="--i:1">感知 → 召回 → 判断 → 行动 → 新的感知，共享同一条时间线</h2>',
          '<div class="eyebrow flow" style="--i:0">乘数三 · 可控临场 —— 主论坛给的金标准，就是这三件事</div>\n'
          '      <h2 class="ink" style="--i:1">临场感 = 实时听见 × 立刻想起 × 当下回应</h2>')
P13 = one(P13,
          '<div class="note flow" style="--i:5">把这个环拆开，就是四个可以分别排期的工程量：'
          '<b>临场 = 实时感知 × 即时召回 × 合时回应 × 可恢复行动。</b>四项里少任何一项，环就断在那里。</div>',
          '<div class="note flow" style="--i:5">这三件事必须发生在<b>同一秒</b>里，才叫「在场」。'
          '有了身体之后它多长出一环——动作发出去就收不回来，所以还要加上<b>可恢复行动</b>。</div>\n'
          '      <div class="note flow" style="--i:5">展开成可以分别排期的工程量，就是上面这个闭环：'
          '<b>实时感知 × 即时召回 × 合时回应 × 可恢复行动</b>，'
          '接成「感知 → 召回 → 判断 → 行动 → 新的感知」。四项里少任何一项，环就断在那里。</div>')

# ── P14 · MQ 02 ──────────────────────────────────────────────
P14 = mq('MONEY QUOTE · 02',
         '没有共同历史的机器人，',
         '永远是陌生人。',
         '当前大多数消费硬件，卡在「工具」和「熟人」之间。')

# ── P16–P22 · 身体的意义 / 半秒 / 两种延迟 / 北极星 / 时序 / 注意 / 端云 ──
P16 = b[10]   # 身体的意义
P17 = b[11]   # 恰好的那半秒
P18 = b[12]   # 两种延迟
P19 = b[13]   # 北极星
P20 = b[15]   # 多模态时序（先讲对齐，再讲听谁的）
# 快闸修二：.rows .k 只有 190px，27px 字最多 7 个汉字；V2 这一格 10 个字会折成两行。
# 「多人重叠」在右栏正文里已经说到了，键名只留分类词。
P21 = one(b[14], '<span class="k">非目标人声与多人重叠</span>', '<span class="k">非目标人声</span>')
P22 = b[16]   # 端云边界

# ── P23 · 故障与恢复（V2 原样）─────────────────────────────────
P23 = b[17]

# ── P24 · AMA 真实提问（新写 · 两版都删掉的一线可信度页）──────────
#   四个问题是 0516 那场 AMA 收到的原话，不是编的。
#   这一页真正的价值在落点：他们问的全是临场，没有一个人问角色和历史。
P24 = '''<section class="slide">
  <div class="chrome"><span>来自一线 · WHAT THEY ACTUALLY ASK</span><span>24</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">这一年我在 AMA 和客户现场，被反复问到的四个问题</div>
      <h2 class="ink" style="--i:1">真实产线上的问题，长这个样子</h2>
    </div>
    <div class="body">
      <div class="quotes ama">
        <div class="r flow" style="--i:2"><div class="who">Q · 01</div><div class="say">有办法让延迟感降到，真的像是在跟人说话吗？</div><div class="src">— OEM 产品负责人</div></div>
        <div class="r flow" style="--i:3"><div class="who">Q · 02</div><div class="say">怎么提高在嘈杂环境里的识别准确率？</div><div class="src">— 端侧算法工程师</div></div>
        <div class="r flow" style="--i:4"><div class="who">Q · 03</div><div class="say">怎么拒识？周围有人说话，或者使用者在跟别人说话。</div><div class="src">— 智能玩具开发者</div></div>
        <div class="r flow" style="--i:5"><div class="who">Q · 04</div><div class="say">主流 voice agent 到底该用 S2S，还是 STT-LLM-TTS？</div><div class="src">— 模型公司架构师</div></div>
      </div>
      <div class="note flow" style="--i:6">这四个问题都很好，也都很真实——但请注意它们的共同点：<b>四个问题问的全是临场，没有一个人问角色，也没有一个人问历史。</b></div>
      <div class="land flow" style="--i:6">乘数里最难的那两项，恰恰没有人在问。<b>下一页，把这四个问题分给该答的人。</b></div>
    </div>
  </div>
</section>'''

# ── P25 · 四方责任表（全场拍照页 · 补分步：大表格一行一步）────────
#   SKILL 明确要求大表格逐行揭示；V2 这一页是一次铺开的。
#   先亮「负责」，再亮「交付物」，最后「缺位时」+ 落点一起砸下来。
P25 = one(b[19], '<tr class="flow" style="--i:3">\n            <td>交付物</td>',
          '<tr class="flow" data-step="1" style="--i:3">\n            <td>交付物</td>')
P25 = one(P25, '<tr class="flow" style="--i:4">\n            <td>缺位时</td>',
          '<tr class="flow" data-step="2" style="--i:4">\n            <td>缺位时</td>')
P25 = one(P25, '<div class="land flow" style="--i:5">产品化破局不是多接一个模型',
          '<div class="land flow" data-step="2" style="--i:5">产品化破局不是多接一个模型')

# ── P26 · MQ 03 · 生死线 ─────────────────────────────────────
P26 = mq('MONEY QUOTE · 03 · 生死线',
         '别听错。别失控。别让人等。',
         '剩下的，才轮到聪明。',
         "Don't mishear. Don't break. Don't make people wait.")

# ── P27 · 标准化接口（V2 + 折进被删的全景页一句）─────────────────
P27 = one(b[21],
          '<div class="land flow" style="--i:5">把不该你解的题标准化，',
          '<div class="note flow" style="--i:4">左边这一栏并不是为消费硬件单独做的：同一套时序、编排、打断与恢复能力，'
          '在电话客服、企业智能体、Physical AI 上是同一份底座——<b>任何一格的进步，几条线一起受益。</b></div>\n'
          '      <div class="land flow" style="--i:5">把不该你解的题标准化，')

# ── P28 · 评测闭环（快闸修三：同上，键名压进 190px 槽，并与第三行「时机对不对」对仗）──
P28 = one(b[22], '<span class="k">该想起的想起了没有</span>', '<span class="k">想起得对不对</span>')

# ── P29 · 三个动作（V2 + 补一句可带走的自查表）───────────────────
P29 = one(b[23],
          '<div class="land flow" style="--i:5">这三件事的顺序不能换：',
          '<div class="note flow" style="--i:5">这三件事合起来，就是一张能贴在工位上的自查表：'
          '<b>一条时间线 · 三组关系评测 · 四种断裂场景。</b>不需要立项，本周就能做完第一轮。</div>\n'
          '      <div class="land flow" style="--i:5">这三件事的顺序不能换：')

# ── P30 · 回到抽屉（V2 原样 · 闭环）───────────────────────────
P30 = b[24]

# ── P31 · 终页（V1 的 21g 钉子 + V2 的场合信息）──────────────────
#   V2 把 21g 那页丢了，那是 0516 全场最高光、也是 Colin 个人品牌的钉子。
P31 = '''<section class="slide">
  <div class="mq">
    <div class="mark flow" style="--i:0">灵魂 21 G · 记忆 0.29 TB</div>
    <div class="q">
      <i class="rise" style="--i:1">从玩具到伙伴的距离，</i>
      <i class="rise" style="--i:3">就是从被使用到被记住的距离。</i>
    </div>
    <div class="rule"></div>
    <div class="s rise" style="--i:5">谢谢 · 姚光华 Colin · 声网 AI 产品线负责人 · 2026 AI 产品大会 · 声网 AIoT 专场 · 北京</div>
  </div>
</section>'''

S = [
    # 开场 · 4 页 —— 冷开场那条曲线 + demo，先把问题摆上台
    P01, P02, P03, P04,
    ROADMAP,
    # ACT 01 · 分辨 —— 你的产品该不该被记住
    ACT1, P05, P06, P07, P08,
    # ACT 02 · 三个乘数 —— 今天唯一要带走的框架
    ACT2, P10, P11, P12, P13, P14,
    # ACT 03 · 那半秒 —— 什么时候开口
    ACT3, P16, P17, P18, P19,
    # ACT 04 · 在房间里 —— 真实环境里的四件事，收在生死线
    ACT4, P20, P21, P22, P23, P26,
    # ACT 05 · 交出去 —— 一线提问 → 责任边界 → 标准化 → 评测 → 三个动作
    ACT5, P24, P25, P27, P28, P29,
    # 收束 · 回到抽屉 + 21g 钉子
    P30, P31,
]
assert len(S) == 35, len(S)

s = head + '\n'.join(S) + tail

# 页码重排（眉标右侧序号按最终顺序改写）
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
assert len(_st) == 35, len(_st)


def _rn(mm):
    idx = sum(1 for t in _st if t <= mm.start())
    return mm.group(1) + ('%02d' % idx) + mm.group(2)


s = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _rn, s)

open('public/decks/aiot26-v3.html', 'w', encoding='utf-8').write(s)

# ═══════════════════════════════════════════════════════════════
# 三、发布前断言
# ═══════════════════════════════════════════════════════════════
n = len(re.findall(r'<section class="slide', s))
assert n == 35, n

# 三个可引用资产 + 本版新增的四处必须在位
ASSETS = [
    '伙伴感 = 角色一致性 × 共同历史 × 可控临场',
    '感知 → 召回 → 判断 → 行动 → 新的感知',
    '实时系统标准化，角色资产私有化，体验标准数据化',
    '系统延迟要消失，表达停顿要被设计',
    '身体让一次回答，变成一次会产生后果的行动',
    # v3 新增
    '像不像一个人，是上一场的题',
    '上半场，造能干活的身体；',
    '四个问题问的全是临场，没有一个人问角色，也没有一个人问历史',
    '没有共同历史的机器人，',
    '别听错。别失控。别让人等。',
    '从玩具到伙伴的距离，',
    '如果你在上面这三格里，接下来二十分钟你可以放松地听',
    '三份产品资产 × 一个实时引擎',   # 必须与主论坛 keynote 公式挂钩
    '临场感 = 实时听见 × 立刻想起 × 当下回应',  # 主论坛 P19 金标准，必须先于五步环出现
    '可恢复行动',
    '从「该不该做」，走到「回去做什么」',
    '你只需要记住第 02 步那一行公式，其余都是它的展开',
]
for x in ASSETS:
    assert x in s, '资产缺失: ' + x

# 事实红线：只查屏上文字（不含 CSS / JS）
TXT = re.sub(r'<[^>]+>', ' ', '\n'.join(S))
BAN = ['Mehrabian', '物理上限', '泡泡玛特', '红杉', '超 30 家', '亿元级融资',
       'SOTA', 'OPENAI TOLAN', '九成', '3-6 个月', '已解决', '致命']
for x in BAN:
    assert x not in TXT, '红线词命中: ' + x
assert not ('7%' in TXT and '38%' in TXT and '55%' in TXT), 'Mehrabian 7/38/55 组合命中'
# 0.29TB 必须仍带思想实验标注，不得退回「物理上限」讲法
assert '思想实验' in TXT, '0.29TB 的思想实验标注丢了'

# 底盘件（继承自 V2，不许在组装中掉）
assert '<html lang="zh-CN">' in s, '默认主题不是 light'
assert "localStorage.getItem('colin-theme')==='dark'" in s, 'light-first 引导脚本缺失'
assert '.deck-swap{display:none!important;' in s, 'deck-swap 未隐藏'
assert 'noindex' in s and 'deckRuler' in s and 'data-dm' in s, '底盘件缺失'
assert 'poster="/media/aiot26/still-1.jpg"' in s and 'vstills' in s, '视频封面帧 / 兜底行缺失'

# 结构：2 张幕卡 + 3 颗金句 + 1 张终页金句
assert len(re.findall(r'<div class="act">', s)) == 5, 'act 幕卡数不对（五幕）'
# 五幕名与路线图必须一致，否则听众对不上号
for _a in ('分辨','三个乘数','那半秒','在房间里','交出去'):
    assert s.count(_a) >= 2, '幕名与路线图不一致: ' + _a
assert len(re.findall(r'<div class="mq">', s)) == 4, 'mq 页数不对（3 金句 + 1 终页）'

# svg 必须在类作用域容器内（.fig 或 .prz）
for m in re.finditer(r'<svg', s):
    seg = s[max(0, m.start() - 900):m.start()]
    assert ('class="fig' in seg or 'class="prz' in seg
            or 'deck-flow' in s[m.start():m.start() + 80]), 'svg 未包在 .fig/.prz 内 @%d' % m.start()

steps = re.findall(r'data-step="(\d+)"', s)
print('aiot26-v3.html · %d 页 · %dKB · data-step 揭示点 %d 处（最大档 %s）'
      % (n, len(s) // 1024, len(steps), max(steps) if steps else '-'))
print('资产 ✓  红线 ✓  默认 light ✓  swap 隐藏 ✓  noindex ✓  媒体 ✓  幕卡%d 金句%d ✓  fig 作用域 ✓'
      % (len(re.findall(r'<div class="act">', s)), len(re.findall(r'<div class="mq">', s))))
