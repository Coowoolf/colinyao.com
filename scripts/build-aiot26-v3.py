#!/usr/bin/env python3
"""aiot26-v3 · 《AI 有了身体，为什么还是三天进抽屉？》—— 终版（37 页 · 五幕 · 默认浅底）。

  规划来源：Vault《2026-08-09_AI产品大会_AIoT专场_V1V2评审与终版规划》
  一句话：V2 的骨架与诚实度 + V1 的幕结构与金句页 + 三处两版都漏掉的补位。

  底盘：public/decks/aiot26-v2.html（样式 / 控制器 / deck-media / deckRuler / 默认 light）
  留 V2：抽屉曲线 · demo · 身体≠伙伴 · 两种价值逻辑 · 三乘数总图 · 三个乘数拆页 ·
         身体的意义 · 恰好半秒 · 两种延迟 · 北极星 · 多模态时序 · 选择性注意 · 端云 ·
         故障恢复 · 四方责任表 · 标准化接口 · 评测闭环 · 三个动作 · 回到抽屉
  取 V1：幕卡与金句页型 + 3 颗金句（上下半场 / 陌生人 / 生死线）+ 21g 终页
  五幕：01 分辨 / 02 三个乘数 / 03 那半秒 / 04 在房间里 / 05 交出去（开场先给一页路线图）
  新写：P02 续集钩子（挂 2025.12 人人都是 PM 大会，不是 0516）· P07 反共识改写（分组而非泼冷水）
        · 路线图 + 五张幕卡（讲述版结构）
  删掉：V2 的 分界线 / 一条真实链路 / 全景独立页 / 独立谢谢页（后两者折进 P27 与 P31）

  ── C7 轮（试讲前夜 · 35 → 37 页）───────────────────────────────
  ① P11 三乘数总图：三张卡各加一行「主论坛映射」（身份 ⇒ 角色一致性 /
     关系 × 历史 ⇒ 共同记忆 / 实时引擎 ⇒ 可控临场），卡片加高 40px 整图下沉。
  ② P14 临场：五阶段从一条直线改成正五边形位的闭合环（顺时针 + 弧中点箭头，
     「新的感知 → 感知」加粗跑光点，环心「同一条时间线 · ONE TIMELINE」）。
  ③ P20 北极星：取值换成独家主数 P90 E2E LATENCY ＜ 1.5S（来自与 Tolan
     工程团队的一手交流），原「1 秒心理边界」等公开拆解降级为参照系。
  ④ 视频页从开场 P04 移到 ACT04「同一条时间线」之后，作为现场例证；
     vcue 从「三件事」改为「一件事」聚焦。
  ⑤ ACT04 从知识模块串讲，重构为「问题驱动 · 逐题作答」：五问总览 +
     Q1 延迟 / Q2 听不清 / Q3 端到端（三页：论点 → 例证 → GPT-Live 异步双模型）
     / Q4 端与云 / Q5 出错了，每页页脚给公开来源；MQ 生死线收口。
     原 AMA 四问页升级为五问总览页并移进 ACT04，ACT05 直接从四方责任开场。

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
/* C7 · ACT04 五问总览：提问人落款收成小字，不抢问题原话 */
.rows .r .v .s{color:var(--ink-3);font-size:18px;margin-left:10px;white-space:nowrap;}
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
P01 = one(b[0], '30 min · 26 slides', '30 min · 37 slides')

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
        <div class="r flow" style="--i:4"><span class="n">04</span><span class="k">在房间里</span><span class="v">把设备放进真实的客厅、教室和车里。这一幕不讲知识点，只回答这一年被问得最多的五个问题。</span></div>
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

# ── P03 · 抽屉曲线（V2 原样）────────────────────────────────────
P03 = b[1]

# ── 视频页 · 从开场第 4 页移到 ACT04「同一条时间线」之后 ─────────
#   它不再是「先看个 demo」，而是多模态论点的现场例证：
#   三件事提示 → 一件事聚焦（同一条时间线里边听边想边说边做）。
VIDEO = one(b[2], '<div class="chrome"><span>证据 · THE DEMO</span><span>03</span></div>',
            '<div class="chrome"><span>现场例证 · ONE TIMELINE, LIVE</span><span>26</span></div>')
VIDEO = one(VIDEO,
            '<div class="vcue flow" style="--i:0">接下来只看三件事：<b>它看见了什么</b> · '
            '<b>它想起了什么</b> · <b>它什么时候开口</b></div>',
            '<div class="vcue flow" style="--i:0">接下来只看一件事：它在<b>同一条时间线</b>里，'
            '边听、边想、边说、边做</div>')
VIDEO = one(VIDEO,
            '<div class="vsum">它证明了：<b>会说话，已经不稀缺。</b>它没有证明的是：<b>关系成立。</b></div>',
            '<div class="vsum">它证明了：<b>三条通道确实可以落在同一条时间线上。</b>'
            '它没有证明的是：<b>关系成立。</b></div>')

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
           '把设备放进真实的客厅、教室和车里。这一幕不讲知识点：'
           '这一年被问得最多的五个问题，一题一页，逐题作答。')
ACT5 = act('05', 'THE HANDOFF', '交出去',
           '五个问题答完，剩下的是分工。哪些题不该你解，哪些事只有你能做——'
           '这一幕把破局落成责任边界，和一张能每周重跑的评测。')

# ── P10–P13 · 三乘数总图 + 三个乘数 ────────────────────────────
# 全场拍照页之一：先让公式和三张卡片自己立住，再补「这是乘法不是加法」那一刀。
P10 = one(b[6], '<div class="note flow" style="--i:6">这是乘法，不是加法',
          '<div class="note flow" data-step="1" style="--i:6">这是乘法，不是加法')
# V3 删掉了 V1/V2 的独立「分水岭」页，但「分水岭不是智能，是角色」是 Colin 最有所有权的
# 那句判断，骨架里不能没有。补回这张总图的眉标——它本来就是这句话的展开。
P10 = one(P10, '<div class="eyebrow flow" style="--i:0">今天唯一需要你记住的那张图</div>',
          '<div class="eyebrow flow" style="--i:0">分水岭不是智能，是角色 —— 今天唯一需要你记住的那张图</div>')
# 与主论坛 keynote 对齐（/cowork-conf PART 2「被记住」P15「伙伴感 = 三份产品资产 × 一个实时引擎」）：
# 三个乘数是同一张图换一种切法。C7 起把这层对应关系直接写进三张卡里（tag 级映射行），
# 页脚只留一句挂钩——听过主论坛的人一眼就能对上号，不必等我口头解释。
P10 = one(P10, '<b>接下来三页，一项一项拆。</b></div>',
          '<b>接下来三页，一项一项拆。</b></div>\n'
          '      <div class="foot flow" style="--i:6">卡片里那三行小字，'
          '就是主论坛那张「伙伴感 = 三份产品资产 × 一个实时引擎」换一种切法。</div>')

# C7 · 改动一 —— 三张乘数卡加「主论坛映射行」：身份 ⇒ 角色一致性 /
# 关系 × 历史 ⇒ 共同记忆 / 实时引擎 ⇒ 可控临场。卡片加高 40px，整图下沉重排。
_CARDS = [
    ('0', '34', 'MULTIPLIER 01 · ROLE', '角色一致性',
     '三个月后重放一段对话，', '用户还认得出这是同一个「它」',
     '主论坛 · 身份 ⇒ 角色一致性', '落地形态 · 可版本化的角色卡'),
    ('590', '624', 'MULTIPLIER 02 · HISTORY', '共同历史',
     '它记得的不是聊天记录，', '是你们一起经历过的那些事',
     '主论坛 · 关系 × 历史 ⇒ 共同记忆', '落地形态 · 关系账本'),
    ('1180', '1214', 'MULTIPLIER 03 · PRESENCE', '可控临场',
     '它在该开口的那一刻开口，', '做错了还回得来',
     '主论坛 · 实时引擎，早就在做 ⇒ 可控临场', '落地形态 · 实时引擎'),
]
for _bx, _tx, _k, _t, _d1, _d2, _map, _land in _CARDS:
    P10 = one(P10,
        '<rect class="box" x="%s" y="26" width="500" height="252" rx="6" stroke-width="1"/>' % _bx,
        '<rect class="box" x="%s" y="20" width="500" height="292" rx="6" stroke-width="1"/>' % _bx)
    P10 = one(P10, '<text class="lbl" x="%s" y="80">%s</text>' % (_tx, _k),
                   '<text class="lbl" x="%s" y="70">%s</text>' % (_tx, _k))
    P10 = one(P10,
        '<text class="fill-ink" x="%s" y="152" style="font-size:44px;font-weight:900">%s</text>' % (_tx, _t),
        '<text class="fill-ink" x="%s" y="140" style="font-size:44px;font-weight:900">%s</text>' % (_tx, _t))
    P10 = one(P10, '<text class="txt" x="%s" y="200">%s</text>' % (_tx, _d1),
                   '<text class="txt" x="%s" y="188">%s</text>' % (_tx, _d1))
    P10 = one(P10, '<text class="txt" x="%s" y="232">%s</text>' % (_tx, _d2),
                   '<text class="txt" x="%s" y="220">%s</text>' % (_tx, _d2))
    P10 = one(P10, '<text class="lbl fill-am" x="%s" y="266">%s</text>' % (_tx, _land),
                   '<text class="lbl" x="%s" y="258">%s</text>\n'
                   '            <text class="lbl fill-am" x="%s" y="292">%s</text>' % (_tx, _map, _tx, _land))
for _x in ('545', '1135'):
    P10 = one(P10,
        '<text class="fill-am" x="%s" y="166" text-anchor="middle" style="font-size:48px;font-weight:900">×</text>' % _x,
        '<text class="fill-am" x="%s" y="180" text-anchor="middle" style="font-size:48px;font-weight:900">×</text>' % _x)
P10 = one(P10, '<path class="stroke-am dw" style="--len:52;--i:5" stroke-width="2.4" d="M840 278 V330"/>',
               '<path class="stroke-am dw" style="--len:44;--i:5" stroke-width="2.4" d="M840 312 V352"/>')
P10 = one(P10, '<rect x="380" y="330" width="920" height="92" rx="6" fill="none" stroke="var(--amber)" stroke-width="2"/>',
               '<rect x="380" y="352" width="920" height="92" rx="6" fill="none" stroke="var(--amber)" stroke-width="2"/>')
P10 = one(P10, '<text class="fill-am" x="840" y="388" text-anchor="middle" style="font-size:36px;font-weight:900">',
               '<text class="fill-am" x="840" y="410" text-anchor="middle" style="font-size:36px;font-weight:900">')
P10 = one(P10, '<path d="M0 458 H1680" stroke="var(--hair)" stroke-width="1" stroke-dasharray="4 7"/>',
               '<path d="M0 484 H1680" stroke="var(--hair)" stroke-width="1" stroke-dasharray="4 7"/>')
P10 = one(P10, '<text class="fill-co" x="0" y="506" style="font-size:31px;font-weight:900">',
               '<text class="fill-co" x="0" y="532" style="font-size:31px;font-weight:900">')
P10 = one(P10, 'viewBox="0 0 1680 520"', 'viewBox="0 0 1680 552"')
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
#
# C7 · 改动二 —— 原来五个阶段排成一条直线，看不出是「环」。重做成正五边形位的
# 闭合圆环：cx840 / cy300 / R190，五节点按 72° 均分，从正上方顺时针（感知 → 召回 →
# 判断 → 行动 → 新的感知）；每段弧两端各留 8° 呼吸位，弧中点放一枚箭头示意方向；
# 「新的感知 → 感知」那一段加粗并跑一枚 amber 光点，强调这是闭环而不是终点。
# 环心是「同一条时间线 · ONE TIMELINE」。入场：底环先生长，节点与弧沿环依序 pop。
_RING = '''<div class="fig gfill">
        <svg viewBox="0 0 1680 552" width="1680" aria-hidden="true">
          <path class="dw" style="--len:1310;--i:2" fill="none" stroke="var(--hair)" stroke-width="1.2"
                d="M840 104 A208 208 0 0 1 840 520 A208 208 0 0 1 840 104"/>
          <circle class="pop" style="--i:2" cx="840" cy="312" r="118" fill="none"
                  stroke="var(--hair)" stroke-width="1" stroke-dasharray="2 9"/>
          <g class="pop" style="--i:2">
            <text class="fill-ink" x="840" y="308" text-anchor="middle" style="font-size:30px;font-weight:900">同一条时间线</text>
            <text class="lbl" x="840" y="340" text-anchor="middle">ONE TIMELINE</text>
          </g>

          <path class="stroke-am dw" style="--len:212;--i:3" stroke-width="2.4" fill="none"
                d="M868.95 106.02 A208 208 0 0 1 1026.95 220.82"/>
          <path class="fill-am pop" style="--i:3" d="M969.54 149.01 L961.45 136.33 L954.98 145.23 Z"/>
          <path class="stroke-am dw" style="--len:212;--i:4" stroke-width="2.4" fill="none"
                d="M1044.84 275.88 A208 208 0 0 1 984.50 461.62"/>
          <path class="fill-am pop" style="--i:4" d="M1035.04 384.84 L1044.60 373.23 L1034.13 369.83 Z"/>
          <path class="stroke-am dw" style="--len:212;--i:5" stroke-width="2.4" fill="none"
                d="M937.65 495.65 A208 208 0 0 1 742.35 495.65"/>
          <path class="fill-am pop" style="--i:5" d="M831 520 L845 525.5 L845 514.5 Z"/>
          <path class="stroke-am dw" style="--len:212;--i:6" stroke-width="2.4" fill="none"
                d="M695.50 461.62 A208 208 0 0 1 635.16 275.88"/>
          <path class="fill-am pop" style="--i:6" d="M639.40 367.72 L638.49 382.74 L648.96 379.34 Z"/>
          <path class="stroke-am dw" style="--len:212;--i:7" stroke-width="6" fill="none"
                d="M653.05 220.82 A208 208 0 0 1 811.05 106.02"/>
          <path class="stroke-am pkt" stroke-width="7.4" fill="none"
                style="--pl:40px;--p0:40px;--p1:-218px;--pt:3.4s;--pd:1.5s"
                d="M653.05 220.82 A208 208 0 0 1 811.05 106.02"/>
          <path class="fill-am pop" style="--i:7" d="M725.02 138.43 L710.46 142.21 L716.93 151.11 Z"/>

          <g class="pop" style="--i:2">
            <circle cx="840" cy="104" r="13" class="fill-am"/>
            <circle class="mring" cx="840" cy="104" r="13" fill="none" stroke="var(--coral)" stroke-width="2.4" style="--d:1.9s"/>
            <text class="ttl" x="840" y="44" text-anchor="middle" style="font-size:30px">感知</text>
            <text class="sm" x="840" y="74" text-anchor="middle" style="font-size:19px">麦克风、摄像头、传感器一直醒着</text>
          </g>
          <g class="pop" style="--i:3">
            <circle cx="1037.82" cy="247.72" r="13" class="fill-am"/>
            <text class="ttl" x="1072" y="241" style="font-size:30px">召回</text>
            <text class="sm" x="1072" y="270" style="font-size:19px">此刻该想起哪一条历史</text>
          </g>
          <g class="pop" style="--i:4">
            <circle cx="962.26" cy="480.28" r="13" class="fill-am"/>
            <text class="ttl" x="996" y="474" style="font-size:30px">判断</text>
            <text class="sm" x="996" y="503" style="font-size:19px">要不要开口、说什么、什么时候</text>
          </g>
          <g class="pop" style="--i:5">
            <circle cx="717.74" cy="480.28" r="13" class="fill-am"/>
            <text class="ttl" x="684" y="474" text-anchor="end" style="font-size:30px">行动</text>
            <text class="sm" x="684" y="503" text-anchor="end" style="font-size:19px">语音和动作同时发出去</text>
          </g>
          <g class="pop" style="--i:6">
            <circle cx="642.18" cy="247.72" r="15" class="fill-co"/>
            <text class="ttl fill-co" x="608" y="241" text-anchor="end" style="font-size:30px">新的感知</text>
            <text class="sm" x="608" y="270" text-anchor="end" style="font-size:19px">它刚做的事，立刻改变了现场</text>
          </g>
        </svg>
      </div>'''
P13 = one(b[9],
          '<div class="eyebrow flow" style="--i:0">乘数三 · 可控临场</div>\n'
          '      <h2 class="ink" style="--i:1">感知 → 召回 → 判断 → 行动 → 新的感知，共享同一条时间线</h2>',
          '<div class="eyebrow flow" style="--i:0">乘数三 · 可控临场 —— 主论坛给的金标准，就是这三件事</div>\n'
          '      <h2 class="ink" style="--i:1">临场感 = 实时听见 × 立刻想起 × 当下回应</h2>')
_i0 = P13.index('<div class="fig gfill">')
_i1 = P13.index('</div>', P13.index('</svg>')) + len('</div>')
P13 = P13[:_i0] + _RING + P13[_i1:]
P13 = one(P13,
          '<div class="note flow" style="--i:5">把这个环拆开，就是四个可以分别排期的工程量：'
          '<b>临场 = 实时感知 × 即时召回 × 合时回应 × 可恢复行动。</b>四项里少任何一项，环就断在那里。</div>',
          '<div class="note flow" style="--i:8">这三件事必须发生在<b>同一秒</b>里，才叫「在场」。'
          '有了身体之后它多长出一环——动作发出去就收不回来，所以还要加上<b>可恢复行动</b>：'
          '<b>感知 → 召回 → 判断 → 行动 → 新的感知</b>，五步接回同一条时间线，'
          '少任何一步，环就断在那里。</div>')
P13 = one(P13,
          '<div class="land flow" style="--i:5">落地形态 = 实时引擎。<span class="s">它不生产内容，'
          '它决定内容什么时候、以什么顺序发生——三个乘数到这里合上：角色卡 × 关系账本 × 实时引擎，'
          '就是「三份产品资产 × 一个实时引擎」在硬件上的样子。</span></div>',
          '<div class="land flow" style="--i:8">落地形态 = 实时引擎。<span class="s">它不生产内容，'
          '它决定内容什么时候、以什么顺序发生——三个乘数到这里合上：角色卡 × 关系账本 × 实时引擎。</span></div>')

# ── P14 · MQ 02 ──────────────────────────────────────────────
P14 = mq('MONEY QUOTE · 02',
         '没有共同历史的机器人，',
         '永远是陌生人。',
         '当前大多数消费硬件，卡在「工具」和「熟人」之间。')

# ── P16–P22 · 身体的意义 / 半秒 / 两种延迟 / 北极星 / 时序 / 注意 / 端云 ──
P16 = b[10]   # 身体的意义
P17 = b[11]   # 恰好的那半秒
P18 = b[12]   # 两种延迟
# ── P19（终稿 P20）· 北极星 —— C7 · 改动三 ─────────────────────
#   原来这一页的取值是「压进 1 秒（内部口径 · 设计样例）」，台上没有分量。
#   换成 Colin 独家：P90 E2E LATENCY ＜ 1.5S，口径是「从人说完最后一个字，
#   到人听到 Agent 说出第一个字」，来自与 Tolan 工程团队的一手交流。
#   原有的 1 秒心理边界等公开拆解降级为「参照系」，不再是北极星本身。
P19 = one(b[13],
          '<h2 class="ink" style="--i:1">北极星只有一条：从用户说完，到第一声有意义的回应</h2>',
          '<h2 class="ink" style="--i:1">北极星只有一条：从人说完最后一个字，到人听到它开口</h2>')
P19 = one(P19,
          '<div class="v">P90</div>\n'
          '            <div class="l">端到端 · 从话音落地，到第一声有意义的回应</div>\n'
          '            <div class="u">END OF SPEECH → FIRST MEANINGFUL AUDIO</div>',
          '<div class="v">&lt; 1.5s</div>\n'
          '            <div class="l">从人说完最后一个字，到人听到 Agent 说出第一个字</div>\n'
          '            <div class="u">P90 E2E LATENCY &lt; 1.5S</div>')
P19 = one(P19,
          '<span class="k">取值</span><span class="v">把 P90 压进 1 秒这条对话的心理边界之内'
          '（内部口径 · 设计样例），再在边界内谈表达停顿。</span>',
          '<span class="k">取值</span><span class="v">P90 ＜ 1.5 秒。这不是我推演出来的数字，是'
          '<b>与 Tolan 工程团队一手交流</b>拿到的口径——一条真实在守的线，守住了才轮到谈表达停顿。</span>')
P19 = one(P19,
          '<div class="note flow" style="--i:5">公开拆解口径：1 秒是对话的心理边界；'
          '一次 +500 毫秒的改动，被创始人形容为一场「灾难」；后来在架构层把语音启动时间缩短了 0.7 秒以上。</div>',
          '<div class="note flow" style="--i:5">公开可查的参照系放在旁边看：1 秒是对话的心理边界；'
          '一次 +500 毫秒的改动，被创始人形容为一场「灾难」；后来在架构层把语音启动时间缩短了 0.7 秒以上。'
          '<b>这些是参照，不是北极星本身——北极星就是上面那一条。</b></div>')
P19 = one(P19,
          '<div class="foot src flow" style="--i:5">来源 · Colin《我从 Tolan 身上，'
          '看清了 Voice Agent 的 4 个反直觉真相》公开拆解口径</div>',
          '<div class="foot src flow" style="--i:5">主数来源 · 与 Tolan 工程团队的一手交流（P90 ＜ 1.5s 口径）'
          '｜ 参照 · Colin《我从 Tolan 身上，看清了 Voice Agent 的 4 个反直觉真相》公开拆解</div>')
# ═══════════════════════════════════════════════════════════════
# ACT 04 · C7 重构：从「知识模块串讲」改回「问题驱动 · 逐题作答」
#   页面语法照保底版 /aiot26 的「工程问题 #N」体例：
#   eyebrow 放从业者的问题原话，h2 放 Colin 的答案判断，foot 给公开来源。
#   问题池：AMA / 客户现场 + 2026 公开社区调研（见 16_ACT04_问题调研来源.md）。
# ═══════════════════════════════════════════════════════════════

def foot(sec, txt):
    """在 .body 末尾（落点之后）追加一条来源脚注 —— ACT04 每页都要有。"""
    tail = '\n    </div>\n  </div>\n</section>'
    assert sec.count(tail) == 1, '来源脚注挂载点失效'
    return sec.replace(
        tail, '\n      <div class="foot src flow" style="--i:5">%s</div>%s' % (txt, tail), 1)


# ── Q0 · 五问总览（由原 P24 AMA 页升级：四问 → 五问 · 加公开来源）──
Q0 = '''<section class="slide">
  <div class="chrome"><span>五个问题 · WHAT THEY ACTUALLY ASK</span><span>22</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">这一年在 AMA、客户现场和开发者社区里，被反复问到的就是这五个</div>
      <h2 class="ink" style="--i:1">这一幕不讲知识点，只回答五个问题</h2>
    </div>
    <div class="body">
      <div class="rows">
        <div class="r flow" style="--i:2"><span class="n">Q1</span><span class="k">延迟</span><span class="v">「有办法把接话的延迟感降下来，真的像在跟人说话吗？」<span class="s">—— OEM 产品负责人</span></span></div>
        <div class="r flow" style="--i:3"><span class="n">Q2</span><span class="k">听不清</span><span class="v">「一屋子人还开着电视，它怎么知道是在跟它说话？」<span class="s">—— 智能玩具开发者</span></span></div>
        <div class="r flow hot" style="--i:3"><span class="n">Q3</span><span class="k">端到端</span><span class="v">「GPT-Live 都全双工了，我们这套级联是不是白做了？」<span class="s">—— 模型公司架构师</span></span></div>
        <div class="r flow" style="--i:4"><span class="n">Q4</span><span class="k">端与云</span><span class="v">「什么放端上、什么放云上？断了网它是不是就傻了？」<span class="s">—— 端侧算法工程师</span></span></div>
        <div class="r flow" style="--i:4"><span class="n">Q5</span><span class="k">出错了</span><span class="v">「它要是说错话、做错动作呢——尤其是对着孩子？」<span class="s">—— 品牌方与家长</span></span></div>
      </div>
      <div class="note flow" style="--i:5">请注意这五个问题的共同点：<b>四个问的是临场，第五个问的是后果。没有一个人问角色，也没有一个人问历史。</b>乘数里最难的那两项，恰恰没有人在问。</div>
      <div class="land flow" style="--i:5">所以这一幕我按被问到的顺序答，一题一页。<b>答完你会发现：五个都是工程题，但每一题的分水岭都在产品判断上。</b></div>
      <div class="foot src flow" style="--i:5">问题池 · AMA / 客户现场（Colin 一线观察）+ 公开社区调研：OpenAI Developer Community · Hacker News · 知乎 / V2EX · CES 2026 AI 玩具报道 · 行业媒体（VentureBeat / TechRepublic / 第一财经）</div>
    </div>
  </div>
</section>'''

# ── Q1 · 延迟（短页 · 回指上一幕 + 硬件侧新增量：动作延迟）──────────
Q1 = '''<section class="slide">
  <div class="chrome"><span>Q1 · 延迟 · LATENCY</span><span>23</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">Q1 ·「有办法把接话的延迟感降下来，真的像在跟人说话吗？」</div>
      <h2 class="ink" style="--i:1">上一幕已经给了答案，有了身体只多一件事</h2>
    </div>
    <div class="body">
      <div class="note flow" style="--i:2">这一题我不重讲：<b>系统延迟要消失，表达停顿要被设计</b>——这是上一幕那两页的结论，北极星是 P90 ＜ 1.5 秒。它在屏幕上和在硬件上，是同一条线。</div>
      <div class="rows">
        <div class="r flow" style="--i:3"><span class="n">01</span><span class="k">系统延迟</span><span class="v">要消失。压到 P90 ＜ 1.5 秒，并且能拆开归因：拾音 / 路由 / 检索 / 模型 / 合成 / 网络。</span></div>
        <div class="r flow" style="--i:4"><span class="n">02</span><span class="k">表达停顿</span><span class="v">要被设计。在那条边界之内，恰好的那半秒比快半秒值钱——它是角色的一部分，不是延迟。</span></div>
        <div class="r flow hot" style="--i:4"><span class="n">03</span><span class="k">动作延迟</span><span class="v">有了身体才出现的第三个量。电机转起来才算数，秒级，而且<b>没有撤回键</b>——它必须最早被决定，还要在决定和执行之间留一段可以叫停的窗口。</span></div>
      </div>
      <div class="land flow" style="--i:5">所以硬件上的延迟预算里，第一次出现了一段「不能反悔」的时间。<b>动作要比语音更早被决定，也要更早被允许取消。</b></div>
      <div class="foot src flow" style="--i:5">来源 · AMA / 客户现场 ｜ 公开参照：thepromptbench.com《Latency Budgets for Real-Time Voice》· destilabs.com《2026 AI Voice Agent Benchmark: Latency &amp; Cost per Minute》</div>
    </div>
  </div>
</section>'''

# ── Q2 · 噪声与拒识（原 P24「选择性注意」改造进问答体例）────────────
#   快闸修二保留：.rows .k 只有 190px，27px 字最多 7 个汉字。
Q2 = one(b[14], '<span class="k">非目标人声与多人重叠</span>', '<span class="k">非目标人声</span>')
Q2 = one(Q2, '<div class="chrome"><span>选择性注意 · WHO IS TALKING TO ME</span><span>15</span></div>',
             '<div class="chrome"><span>Q2 · 听不清 · WHO IS TALKING TO ME</span><span>24</span></div>')
Q2 = one(Q2, '<div class="eyebrow coral flow" style="--i:0">把设备放进真实的客厅、教室和车里</div>',
             '<div class="eyebrow coral flow" style="--i:0">Q2 ·「一屋子人还开着电视，它怎么知道是在跟它说话？」</div>')
Q2 = foot(Q2, '来源 · AMA / 客户现场 ｜ 公开高频区：'
              'community.openai.com《Background Noise Interfering with Realtime API Using Phone》/'
              '《Realtime API interrupts too aggressively on filler words》· '
              'cloud.tencent.com《实时说话人分离上线》')

# ── Q3 · 端到端还是级联（答案分三页：论点 → 现场例证 → GPT-Live 分析）──
Q3A = one(b[15], '<div class="chrome"><span>多模态时序 · ONE TIMELINE</span><span>16</span></div>',
                 '<div class="chrome"><span>Q3 · 端到端 · 答案上半</span><span>25</span></div>')
Q3A = one(Q3A, '<div class="eyebrow flow" style="--i:0">多模态不是把三个功能并排接上</div>',
               '<div class="eyebrow flow" style="--i:0">Q3 ·「GPT-Live 都全双工了，我们这套级联是不是白做了？」· 先答一半</div>')
Q3A = foot(Q3A, '来源 · AMA / 客户现场 ｜ 公开讨论区：gradium.ai《Cascaded Voice Agents vs '
                'Speech-to-Speech: Architecture Tradeoffs in 2026》· softcery.com'
                '《Real-Time vs Turn-Based Voice Agents in 2026》')

# Q3B · 答案升级一个大版本 —— 素材来自 Colin 三部曲 #39/#40/#41（口径原样搬运，
# 不重新发明数字）：/async-two-model「他们取消了 turn detector，然后用了两个模型」、
# /warp-public-good（6→2 与 Active Internet-Draft 的精确口径）、/turn-ledger。
Q3B = '''<section class="slide">
  <div class="chrome"><span>Q3 · 端到端 · 答案下半</span><span>27</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">Q3 · 2026 年 8 月，这个问题有了新答案 —— 我自己也改了一个判断</div>
      <h2 class="ink" style="--i:1">不是端到端赢了，是异步双模型：级联没死，是被重构了</h2>
    </div>
    <div class="body">
      <div class="note flow" style="--i:2">OpenAI 在 8 月 3 日的工程博客里做了两件事：把独立的 <b>turn detector 移出音频主路</b>——不再猜「用户说完没有」，而是换掉了这道题本身；然后给新系统起了个名字，叫 <b>two-model architecture</b>。这是官方自己写下的词，不是我的读图结论。</div>
      <div class="g3">
        <div class="card rise" style="--i:3">
          <div class="tag">LAYER 01 · 模态</div>
          <div class="t">这一层确实端到端了</div>
          <div class="d">实时语音主路直接处理和生成音频，不必再经过 transcript 这个瓶颈。语气、停顿、重音，不会在转换时被删掉。</div>
        </div>
        <div class="card rise" style="--i:4">
          <div class="tag">LAYER 02 · 链路</div>
          <div class="t">这一层保持分工</div>
          <div class="d">GPT-Live 留在现场负责听、说、停顿、打断；遇到搜索和深度推理，异步委派给后台的前沿模型，结果以 guidance 回流。</div>
        </div>
        <div class="card warn rise" style="--i:4">
          <div class="tag">LAYER 03 · 时间</div>
          <div class="t">真正被重构的是它</div>
          <div class="d">深度推理从同步关键路径挪到异步旁路。关键不在于有几个模型，而在于<b>第二个模型不挡住第一个模型说话</b>。</div>
        </div>
      </div>
      <div class="land flow" style="--i:5">所以「端到端赢了」和「级联没死」，都只说对了一半。<b>会死的是串行，不会死的是分工。</b><span class="s">边界没有消失，它换了位置——从 STT / LLM / TTS 之间，换到实时主路与异步旁路之间。对做硬件的人来说，接下来要补的不是第三个模型，是不可逆动作的闸门，和两条路径共用的那本账。</span></div>
      <div class="foot src flow" style="--i:5">口径提示 · 同篇博客的传输层 WARP：协议握手 6 RTT → 2 RTT（草案 Abstract 口径；产品体感的 1 RTT 是另一本账）。截至 2026-08-04，WARP 是 Active Internet-Draft，尚未被工作组采纳，不是 IETF 标准。</div>
      <div class="foot src flow" style="--i:5">来源 · OpenAI 工程博客《How we built a realtime system for responsive voice AI in six months》2026-08-03 ｜ venturebeat.com（GPT-Live 发布）· gradium.ai《Cascaded vs Speech-to-Speech 2026》· contextstudios.ai（GPT-Live vs Cascaded）｜ 我的三部曲 #39 / #40 / #41</div>
    </div>
  </div>
</section>'''

# ── Q4 · 端与云（原 P25 端云边界改造进问答体例 · 顺带回答隐私边界）────
Q4 = one(b[16], '<div class="chrome"><span>端云边界 · EDGE × CLOUD</span><span>17</span></div>',
                '<div class="chrome"><span>Q4 · 端与云 · EDGE × CLOUD</span><span>28</span></div>')
Q4 = one(Q4, '<div class="eyebrow flow" style="--i:0">切在哪，第一次成了产品决策，不是硬件预算决策</div>',
             '<div class="eyebrow flow" style="--i:0">Q4 ·「什么放端上、什么放云上？断了网它是不是就傻了？」</div>')
Q4 = one(Q4,
         '<div class="land flow" style="--i:5">切分的标准不是算力，是体验红线：'
         '<b>哪些事慢半秒就出戏，哪些事可以想两秒。</b></div>',
         '<div class="land flow" style="--i:5">切分的标准不是算力，是体验红线：'
         '<b>哪些事慢半秒就出戏，哪些事可以想两秒。</b>'
         '<span class="s">顺带答掉一个跟着来的问题：孩子说的那些话到底存在哪——'
         '这条线画在哪里，隐私边界就在哪里。它是同一个决策，不是两个。</span></div>\n'
         '      <div class="foot src flow" style="--i:5">来源 · AMA / 客户现场 ｜ 公开高频区：'
         'news.ycombinator.com《2026 will be the year of on-device agents》· '
         '知乎 GAIR Live 029《端云协同与记忆革命》· shengwang.cn《2026 Physical AI 行业全景》</div>')

# ── Q5 · 出错了（原 P26 故障与恢复改造：把「多人同时说话」换成 2026 最热的
#      「说了不该说的话」，与 CES 2026 AI 玩具那一轮争议正面对上）────────
Q5 = one(b[17], '<div class="chrome"><span>故障与恢复 · RECOVERABLE ACTION</span><span>18</span></div>',
                '<div class="chrome"><span>Q5 · 出错了 · RECOVERABLE ACTION</span><span>29</span></div>')
Q5 = one(Q5, '<div class="eyebrow coral flow" style="--i:0">真实使用里，这四件事一定会发生</div>',
             '<div class="eyebrow coral flow" style="--i:0">Q5 ·「它要是说错话、做错动作呢——尤其是对着孩子？」</div>')
Q5 = one(Q5,
         '<tr class="flow" style="--i:3"><td>多人同时说话</td><td>谁大声听谁的，或者干脆两个都答</td>'
         '<td>认住此刻的说话人，其余按背景处理，并说明它在跟谁说</td></tr>',
         '<tr class="flow" style="--i:3"><td>说了不该说的话</td><td>当作没发生过，或者从此一刀切、什么都不敢答</td>'
         '<td>当场承认并纠正，把这一次留痕，并让负责的大人看得见</td></tr>')
Q5 = foot(Q5, '来源 · AMA / 客户现场 ｜ 2026 公开争议区：'
              'techrepublic.com《AI Toys Reach Children Before Privacy and Safety Rules Catch Up》· '
              'abc7news.com（CES 2026 AI 陪伴玩具）· safeagentbench.github.io（具身动作安全评测）')

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
    # 开场 · 3 页 —— 冷开场那条曲线，先把问题摆上台（demo 已移进 ACT04）
    P01, P02, P03,
    ROADMAP,
    # ACT 01 · 分辨 —— 你的产品该不该被记住
    ACT1, P05, P06, P07, P08,
    # ACT 02 · 三个乘数 —— 今天唯一要带走的框架
    ACT2, P10, P11, P12, P13, P14,
    # ACT 03 · 那半秒 —— 什么时候开口
    ACT3, P16, P17, P18, P19,
    # ACT 04 · 在房间里 —— 五问总览 → 逐题作答（Q3 三页：论点 / 现场例证 / GPT-Live）→ 生死线
    ACT4, Q0, Q1, Q2, Q3A, VIDEO, Q3B, Q4, Q5, P26,
    # ACT 05 · 交出去 —— 责任边界 → 标准化 → 评测 → 三个动作
    ACT5, P25, P27, P28, P29,
    # 收束 · 回到抽屉 + 21g 钉子
    P30, P31,
]
assert len(S) == 37, len(S)

s = head + '\n'.join(S) + tail

# 页码重排（眉标右侧序号按最终顺序改写）
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
assert len(_st) == 37, len(_st)


def _rn(mm):
    idx = sum(1 for t in _st if t <= mm.start())
    return mm.group(1) + ('%02d' % idx) + mm.group(2)


s = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _rn, s)

open('public/decks/aiot26-v3.html', 'w', encoding='utf-8').write(s)

# ═══════════════════════════════════════════════════════════════
# 三、发布前断言
# ═══════════════════════════════════════════════════════════════
n = len(re.findall(r'<section class="slide', s))
assert n == 37, n

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
    '四个问的是临场，第五个问的是后果。没有一个人问角色，也没有一个人问历史',
    '没有共同历史的机器人，',
    '别听错。别失控。别让人等。',
    '从玩具到伙伴的距离，',
    '如果你在上面这三格里，接下来二十分钟你可以放松地听',
    '三份产品资产 × 一个实时引擎',   # 必须与主论坛 keynote 公式挂钩
    '临场感 = 实时听见 × 立刻想起 × 当下回应',  # 主论坛 P19 金标准，必须先于五步环出现
    '可恢复行动',
    '从「该不该做」，走到「回去做什么」',
    '你只需要记住第 02 步那一行公式，其余都是它的展开',
    # C7 新增 —— 六处改动的落地证据
    '主论坛 · 身份 ⇒ 角色一致性',
    '主论坛 · 关系 × 历史 ⇒ 共同记忆',
    '主论坛 · 实时引擎，早就在做 ⇒ 可控临场',
    '同一条时间线',
    'ONE TIMELINE',
    'P90 E2E LATENCY &lt; 1.5S',
    '从人说完最后一个字，到人听到 Agent 说出第一个字',
    '与 Tolan 工程团队一手交流',
    '接下来只看一件事：它在<b>同一条时间线</b>里，边听、边想、边说、边做',
    '这一幕不讲知识点，只回答五个问题',
    '有办法把接话的延迟感降下来，真的像在跟人说话吗？',
    '一屋子人还开着电视，它怎么知道是在跟它说话？',
    'GPT-Live 都全双工了，我们这套级联是不是白做了？',
    '什么放端上、什么放云上？断了网它是不是就傻了？',
    '它要是说错话、做错动作呢——尤其是对着孩子？',
    '不是端到端赢了，是异步双模型：级联没死，是被重构了',
    'two-model architecture',
    '会死的是串行，不会死的是分工',
    '6 RTT → 2 RTT',
    'Active Internet-Draft',
    '动作延迟',
    '说了不该说的话',
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

# C7 · 改动一/二/三/五 的结构断言
assert s.count('A208 208 0 0 1') == 8, '临场环弧段数不对（5 段 + 底环 2 段 + 闭环光点 1）'
assert len(re.findall(r'<circle cx="[\d.]+" cy="[\d.]+" r="1[35]" class="fill-(?:am|co)"/>', s)) == 5, \
    '临场环节点应为 5 个'
assert '设计样例' not in s[s.index('北极星只有一条'):s.index('北极星只有一条') + 4200], \
    '北极星页仍有「设计样例」'
assert s.count('class="foot src') >= 9, 'ACT04 逐题来源脚注缺失'
for _q in ('Q1</span><span class="k">延迟', 'Q2</span><span class="k">听不清',
           'Q3</span><span class="k">端到端', 'Q4</span><span class="k">端与云',
           'Q5</span><span class="k">出错了'):
    assert _q in s, '五问总览缺题: ' + _q

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
