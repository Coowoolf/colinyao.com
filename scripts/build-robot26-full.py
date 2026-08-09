#!/usr/bin/env python3
"""【已退役 · 2026-08-09】本脚本的产物已归档为 public/decks/robot26-v0516.html。
  robot26 现役版本改由 scripts/build-robot26-bj.py 生成（北京站 PPT 36 页一比一还原），
  两者互不相干：本脚本处理的是 0516 深圳那份改编稿。若要复跑，先把 SRC 指向归档件。

robot26 全量还原 —— 把 0516 深圳 RTE 春夏巡游原稿（36 张 PPTX）的信息补齐。

  背景：现有 robot26.html 是当初从 PPTX 手工改编成 colin-deck 的版本，
  36 页里有 6 页是 colin-deck 新增的结构件（1 张全场主线 + 5 张幕卡），
  也就是说原稿 35 张内容页被压进了 30 页——按实质中文内容加权，还原率约 72%。

  四张整页完全丢失：
    · 原 P28 ConvoAI Engine 2.0 · 9 项核心能力（"声纹"二字全文不存在）
    · 原 P30 Robotics 1 开发套件（参数被压成「我们的位置」页的一行 note，无 SPEC 对比表）
    · 原 P31 A QUIET ENDORSEMENT · OpenAI 背书
    · 原 P34 A NEW FORM OF COMPANIONSHIP · 家庭第六成员
  四处实质压缩：
    · 原 P11 关系容量三级跳（工具 → 熟人 → 伙伴）整个递进结构没了
    · 原 P10 豆豆案例 Day 1 / Day 30 / Day 365 的具体叙事被压成一张 SVG
    · 原 P15 Mehrabian 只剩数字，缺「对话从来都不止语言」与「本来就有机会承担那 55%」
    · 原 P8 四症状缺 ①②③④ 主线声明与临场的空间/时间双维度

  本脚本：36 → 44 页。展示形式一律沿用 colin-deck（幕卡 / 金句 / 组件类不变）。
"""
import re

SRC = "public/decks/robot26-v0516.html"   # 退役后源锚改指归档件
s = open(SRC, encoding="utf-8").read()
SEC = re.compile(r'<section class="slide[^"]*">.*?</section>', re.S)
secs = SEC.findall(s)
assert len(secs) == 36, len(secs)
head = s[:s.index('<section class="slide')]
tail = s[s.rindex('</section>') + len('</section>'):]


def one(hay, old, new):
    assert hay.count(old) == 1, "锚点失效: " + old[:70]
    return hay.replace(old, new, 1)


# ═══════════════════════════════════════════════════════════════
# 一、就地补足被压缩的页
# ═══════════════════════════════════════════════════════════════

# 原 P8 四症状 —— 补回「4 组件主线」声明与临场的空间/时间双维度
i10 = 9   # robot26 P10 · 四个非伙伴症状
secs[i10] = one(
    secs[i10],
    '</div>\n  </div>\n</section>',
    '  <div class="land flow" style="--i:7">4 个症状，对应 4 个组件的失败：'
    '<b>① 身份 ② 关系 ③ 历史 ④ 临场（空间 + 时间）。</b>'
    '<span class="s">临场有两个维度——空间上「你在客厅，它的注意力在卧室」，'
    '时间上「你说一半它抢话，你问完它愣 2 秒」。这 4 个组件，就是今天这场演讲的主线。</span></div>\n'
    '    </div>\n  </div>\n</section>')

# 原 P15 Mehrabian —— 数字与「本来就有机会承担那 55%」都在，只差一句铺垫论点
#   （注：这里是 0516 的忠实档案，7/38/55 照原样保留；新一场 aiot26 不再用它，
#     因为该规则只适用于「言辞与非言辞不一致的情感态度沟通」，泛用是可信度风险。）
i_meh = next(k for k, x in enumerate(secs) if 'Mehrabian' in x)
secs[i_meh] = one(
    secs[i_meh],
    '<div class="note flow" style="--i:5">Mehrabian 1971：',
    '<div class="note flow" style="--i:5"><b>对话，从来都不止「语言」。</b>'
    '在语音对话里，AI 的「活人感」缺失比文字对话时更明显——Mehrabian 1971：')

# 原 P29 我们的位置 —— 硬件参数从这里挪走（改由独立的 Robotics 1 页承载），补回 RTE 底座
i_sit = next(k for k, x in enumerate(secs) if 'WHERE WE SIT' in x)
secs[i_sit] = one(
    secs[i_sit],
    'ConvoAI Engine 2.6 · 16 次迭代 · 14 个月 · Production-Ready<br>'
    'Robotics 1 消费机器人开发套件：R1 Wi-Fi（2025.03.20 · BK7258）／ '
    'R1 4G（2025.09.26 · UNISOC 8910 Cat.1 一体化）',
    'ConvoAI Engine 2.6 · 16 次迭代 · 14 个月 · Production-Ready<br>'
    'Robotics 1 消费机器人开发套件（下一页详解）· '
    'SD-RTN + Last-Mile + 30000+ 机型适配 = RTE 全域通信底座')


# ═══════════════════════════════════════════════════════════════
# 二、补回丢失的整页
# ═══════════════════════════════════════════════════════════════

# 原 P11 · 关系容量三级跳 ────────────────────────────────────────
LEAPS = '''<section class="slide">
  <div class="chrome"><span>关系容量三级跳 · THREE LEAPS</span><span>00</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">RELATIONSHIP CAPACITY · THREE LEAPS</div>
      <h2 class="ink" style="--i:1">关系容量的三级跳。</h2>
    </div>
    <div class="body">
      <div class="g3">
        <div class="card rise" style="--i:2">
          <div class="tag">LEVEL 01 · 工具</div>
          <div class="t">智能音箱</div>
          <div class="d">「你叫醒我」。一次性指令，用完即走，没有任何需要被记住的东西。</div>
        </div>
        <div class="card rise" style="--i:3">
          <div class="tag">LEVEL 02 · 熟人</div>
          <div class="t">记得几个偏好的 AI 玩具</div>
          <div class="d">它知道你喜欢什么颜色、常问什么问题。有一点记忆，但撑不起关系。</div>
        </div>
        <div class="card on rise" style="--i:4">
          <div class="tag am">LEVEL 03 · 伙伴</div>
          <div class="t">填满生命上下文配额的伙伴形态</div>
          <div class="d">它和你之间有一段只有你们两个知道的历史，换一台就得从头再来。</div>
        </div>
      </div>
      <div class="note flow" style="--i:5">当前 9 成消费机器人，卡在<b>工具和熟人之间</b>——它们有记忆，但没有共同历史。</div>
      <div class="land flow" style="--i:6">那么真正的伙伴感，能不能用一个数字量化？<span class="s">下一页，我们给它一个物理上限。</span></div>
    </div>
  </div>
</section>'''

# 原 P10 · 豆豆案例三段（Day 1 / Day 30 / Day 365）──────────────
DOUDOU = '''<section class="slide">
  <div class="chrome"><span>共同历史怎么长出来 · DAY 1 → DAY 365</span><span>00</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">③ HISTORY · 历史不是录音，是从录音里长出来的对你的理解</div>
      <h2 class="ink" style="--i:1">一只叫「豆豆」的猫，怎么变成不可替代。</h2>
    </div>
    <div class="body">
      <div class="rows">
        <div class="r flow" style="--i:2"><span class="n">01</span><span class="k">DAY 1 · 浅</span><span class="v">你告诉它，你养的猫叫「豆豆」。——这只是第一次对话里的一个事实。</span></div>
        <div class="r flow" style="--i:3"><span class="n">02</span><span class="k">DAY 30 · 中</span><span class="v">它主动问你「豆豆最近怎么样？」——主动召回，这时候才开始有「关系」。</span></div>
        <div class="r flow hot" style="--i:4"><span class="n">03</span><span class="k">DAY 365 · 深</span><span class="v">它知道豆豆爱吃哪个牌子、生病过几次。——长期共同历史 = 不可替代。</span></div>
      </div>
      <div class="note flow" style="--i:5">对应三层存储：<b>短期</b>本次对话上下文（context window）· <b>中期</b>本周／本月主题汇聚（RAG / summary）· <b>长期</b>画像／关键事件／偏好（结构化存储 + 检索）。</div>
      <div class="land flow" style="--i:6">没有共同历史的机器人，永远是陌生人。<span class="s">音频是耗材，语义才是资产。</span></div>
    </div>
  </div>
</section>'''

# 原 P28 · ConvoAI Engine 2.0 九项核心能力 ──────────────────────
NINE = '''<section class="slide">
  <div class="chrome"><span>CONVOAI ENGINE 2.0 · 9 项核心能力</span><span>00</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">INFO DENSITY HIGH · 给一线产品经理看的版本</div>
      <h2 class="ink" style="--i:1">9 项核心能力，直接对应你做消费机器人的真实需求。</h2>
    </div>
    <div class="body">
      <div class="g3">
        <div class="card sm rise" style="--i:2"><div class="tag">01 · 低延迟</div><div class="t">E2E &lt; 1s</div><div class="d">端到端小于 1 秒的实时对话。</div></div>
        <div class="card sm rise" style="--i:2"><div class="tag">02 · 懂打断</div><div class="t">优雅打断 2.0</div><div class="d">智能识别该让还是该抢。</div></div>
        <div class="card sm rise" style="--i:3"><div class="tag">03 · 多语种 &amp; 音色</div><div class="t">全球语音生态</div><div class="d">主流 ASR / TTS 供应商全打通。</div></div>
        <div class="card sm rise" style="--i:3"><div class="tag">04 · 形象</div><div class="t">AI 数字人</div><div class="d">给它一张可以被看见的脸。</div></div>
        <div class="card sm rise" style="--i:4"><div class="tag">05 · 眼睛</div><div class="t">视觉理解</div><div class="d">看图 / 看人 / 看场景。</div></div>
        <div class="card sm on rise" style="--i:4"><div class="tag am">06 · 专注</div><div class="t">声纹锁定</div><div class="d">选择性注意力——只听该听的那个人。</div></div>
        <div class="card sm rise" style="--i:5"><div class="tag">07 · 能分辨</div><div class="t">声纹识别</div><div class="d">听得出这屋里谁是谁。</div></div>
        <div class="card sm rise" style="--i:5"><div class="tag">08 · 懂节奏</div><div class="t">何时说 / 停 / 跟</div><div class="d">开口时机、沉默时长、跟话策略。</div></div>
        <div class="card sm rise" style="--i:6"><div class="tag">09 · 能落地</div><div class="t">SIP / PSTN 全打通</div><div class="d">从设备一路通到电话网。</div></div>
      </div>
      <div class="land flow" style="--i:7">这 9 项不是功能清单，是把「角色三件套」实时托住所需要的最小能力集。</div>
    </div>
  </div>
</section>'''

# 原 P30 · Robotics 1 开发套件 ──────────────────────────────────
R1 = '''<section class="slide">
  <div class="chrome"><span>开发套件 · CONSUMER ROBOT DEV KIT</span><span>00</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">PLUG · CONNECT · SHIP</div>
      <h2 class="ink" style="--i:1">声网 Robotics 1：赋予硬件「数字灵魂」。</h2>
    </div>
    <div class="body">
      <div class="g2">
        <div class="card rise" style="--i:2">
          <div class="tag">R1 · WI-FI ｜ 2025.03.20 发布</div>
          <div class="t">带「灵动眼睛」PCB</div>
          <div class="d">主控 BK7258 · Wi-Fi 联网。面向<b>家庭与桌面玩具</b>。</div>
        </div>
        <div class="card on rise" style="--i:3">
          <div class="tag am">R1 · 4G ｜ 2025.09.26 发布</div>
          <div class="t">带 4G 天线 · 一体化</div>
          <div class="d">UNISOC 8910 · Cat.1 一体化。面向<b>户外 / 出行陪伴</b>。</div>
        </div>
      </div>
      <div class="rows">
        <div class="r flow" style="--i:4"><span class="n">—</span><span class="k">对话式 AI</span><span class="v">Wi-Fi ● ｜ 4G ●　　　视觉理解　Wi-Fi ● ｜ 4G ●　　　本地唤醒　Wi-Fi ● ｜ 4G ●</span></div>
        <div class="r flow" style="--i:5"><span class="n">—</span><span class="k">传感扩展</span><span class="v">陀螺仪 / NFC / 振动马达，两版一致；差别只在联网方式与整机形态。</span></div>
      </div>
      <div class="note flow" style="--i:6">★ <b>R1 4G 的单芯片一体化是关键卖点</b>：省掉一颗模组，整机成本和体积一起降下来。</div>
      <div class="land flow" style="--i:7">临场引擎 + 硬件参考设计 = 拿来即用的伙伴感地基。</div>
    </div>
  </div>
</section>'''

# 原 P31 · OpenAI 背书 ─────────────────────────────────────────
ENDORSE = '''<section class="slide">
  <div class="mq">
    <div class="mark flow" style="--i:0">A QUIET ENDORSEMENT · 2024.10.01</div>
    <div class="q">
      <i class="rise" style="--i:1">全球最强的 Voice Agent 团队，</i>
      <i class="rise" style="--i:3">在为 Realtime API 找实时通信底座时，选了我们。</i>
    </div>
    <div class="rule"></div>
    <div class="s rise" style="--i:5">同样的工程能力，我们用来支撑你的消费机器人。</div>
  </div>
</section>'''

# 原 P34 · 家庭第六成员 ────────────────────────────────────────
SIXTH = '''<section class="slide">
  <div class="chrome"><span>新的伙伴形态 · A NEW FORM OF COMPANIONSHIP</span><span>00</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">LIVING ROOM · 2030</div>
      <h2 class="ink" style="--i:1">消费级机器人，不是更聪明的玩具，是新的伙伴形态。</h2>
    </div>
    <div class="body">
      <div class="note flow" style="--i:2">一个会<b>持续陪伴你、记得你、感知你、理解你</b>的存在。</div>
      <div class="g2">
        <div class="card rise" style="--i:3">
          <div class="tag">NEXT 5 YEARS</div>
          <div class="t">家庭的第六个成员</div>
          <div class="d">伙伴形态的消费机器人，会像宠物一样进入家庭结构——只不过它记得的事更多。</div>
        </div>
        <div class="card on rise" style="--i:4">
          <div class="tag am">今天在座的每一位</div>
          <div class="t">塑造这个新成员的人</div>
          <div class="d">这个成员长成什么性格、记得什么、在什么时候开口，是你们现在正在写的需求文档决定的。</div>
        </div>
      </div>
      <div class="land flow" style="--i:5">在座的每一位，都有机会成为塑造这个新成员的人。</div>
    </div>
  </div>
</section>'''


# ═══════════════════════════════════════════════════════════════
# 三、装配：把补回的页插进原有顺序
# ═══════════════════════════════════════════════════════════════
def idx(pat):
    return next(k for k, x in enumerate(secs) if pat in x)


out = []
for k, sec in enumerate(secs):
    out.append(sec)
    if 'CAPACITY CURVE' in sec:                 # 容量曲线之前先讲三级跳 → 插在其前
        out.insert(len(out) - 1, LEAPS)
    if '② 关系 · ③ 历史' in sec:                 # 关系/历史之后补豆豆案例
        out.append(DOUDOU)
    if 'FOUR THREADS' in sec:                    # 四部曲之后补 9 项能力
        out.append(NINE)
    if 'WHERE WE SIT' in sec:                    # 我们的位置之后补硬件 + 背书
        out.append(R1)
        out.append(ENDORSE)
    if 'THREE ASKS' in sec:                      # 三条建议之后、终局金句之前补第六成员
        out.append(SIXTH)

s2 = head + '\n'.join(out) + tail

# 页码重排
_st = [m.start() for m in re.finditer(r'<section class="slide', s2)]
n = len(_st)


def _rn(mm):
    return mm.group(1) + ('%02d' % sum(1 for t in _st if t <= mm.start())) + mm.group(2)


s2 = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _rn, s2)
open(SRC, 'w', encoding='utf-8').write(s2)

# ═══════════════════════════════════════════════════════════════
# 四、还原断言：原稿里这些实质内容必须在
# ═══════════════════════════════════════════════════════════════
TXT = re.sub(r'<[^>]+>', ' ', s2)
MUST = [
    '关系容量的三级跳', '填满生命上下文配额的伙伴形态', '卡在', '工具和熟人之间',
    '豆豆', '主动召回', '长期共同历史', '结构化存储',
    '9 项核心能力', '声纹锁定', '声纹识别', 'SIP / PSTN', '优雅打断 2.0', '视觉理解',
    'Robotics 1', 'BK7258', 'UNISOC 8910', '灵动眼睛', '陀螺仪', '单芯片一体化',
    '全球最强的 Voice Agent 团队', '实时通信底座',
    '新的伙伴形态', '第六个成员', '塑造这个新成员',
    '① 身份 ② 关系 ③ 历史 ④ 临场', 'RTE 全域通信底座',
]
for m in MUST:
    assert m in TXT, '还原缺失: ' + m

print('robot26-v0516.html · %d 页（原 36 → 补回 %d 页）· %dKB' % (n, n - 36, len(s2) // 1024))
print('补回：三级跳 / 豆豆案例 / Engine 2.0 九项能力 / Robotics 1 / OpenAI 背书 / 家庭第六成员')
print('就地补足：四症状主线声明 + 临场空间时间双维度 / RTE 全域通信底座')
print('还原断言 %d 条 ✓' % len(MUST))
