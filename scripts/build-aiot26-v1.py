#!/usr/bin/env python3
"""aiot26 保底版 —— 0516 深圳那一场的「三个月后 · 换场合」迭代（40 页 · 双主题）。

  为什么重建：现有 aiot26 名义上是 0516 的升维版，实际主干是断的——
  0516 的中心论点「角色三件套 + 一个引擎」在里面出现 0 次，
  AMA / 豆豆案例 / 关系容量三级跳 / Robotics 1 / 我们的位置 / 家庭第六成员 也全部为 0。
  它不是三个月迭代，是复用了部分页面的另起炉灶版本。

  本版定位：**保底**。主干严格对齐全量还原后的 robot26（42 页），
  只叠加三个月的内容增量，再做换场合的必要适配。风险最低、可追溯。
  （另有 aiot26-v3 是完整升维版，用三乘数新框架；aiot26-v2 留作过程材料。）

  底盘：aiot26.html（robot26 组件库 + 移植层 PORT_CSS + 媒体模块，同源）
  主干：robot26.html 还原版取 19 页
  增量：Physical AI 两个半场 / 消费侧读数 / 端云边界(工程 #4) / 产品化破局 / 上下半场金句
  适配：封面换场合、钩子改挂 2025-12 人人都是 PM 大会（这批听众看过那场，没看过 0516）
  场合：2026 AI 产品大会 · 声网 AIoT 专场 · 2026.08.09 北京 · 30 min。
"""
import re

# 增量页取自 Fable 那版 35 页 aiot26（保存为 _src-，因为本脚本的输出就是 aiot26.html，
# 直接读自己会在第二次运行时炸掉）
A = open("public/decks/_src-aiot26-fable35.html", encoding="utf-8").read()
R = open("public/decks/robot26.html", encoding="utf-8").read()
SEC = re.compile(r'<section class="slide[^"]*">.*?</section>', re.S)
a_ = SEC.findall(A)
rs = SEC.findall(R)
assert len(a_) == 35, "增量源必须是 Fable 那版 35 页，当前 %d" % len(a_)
assert len(rs) == 42, "robot26 必须是全量还原后的 42 页，当前 %d" % len(rs)

head = A[:A.index('<section class="slide')]
tail = A[A.rindex('</section>') + len('</section>'):]
head = re.sub(r'<title>[^<]*</title>',
              '<title>从玩具到伙伴 · 三个月后 · 2026 AI 产品大会 AIoT 专场 · 保底版</title>',
              head, count=1)


def one(hay, old, new):
    assert hay.count(old) == 1, "锚点失效: " + old[:70]
    return hay.replace(old, new, 1)


def act(num, en, cn, d):
    return ('<section class="slide">\n  <div class="act">\n'
            '    <div class="num flow" style="--i:0">ACT %s</div>\n'
            '    <div class="en settle" style="--i:1">%s</div>\n'
            '    <div class="cn spread" style="--i:3">%s</div>\n'
            '    <div class="d flow" style="--i:4">%s</div>\n'
            '  </div>\n</section>' % (num, en, cn, d))


# ═══════════════════════════════════════════════════════════════
# 封面 · 钩子
# ═══════════════════════════════════════════════════════════════
COVER = one(a_[0], '30 min · 35 slides', '30 min · 40 slides')

# 钩子改挂 2025-12：这批听众（人人都是产品经理大会）看过「活人感」那场，
# 没看过 0516 深圳 RTE 场。现有 aiot26 的「三个月，行业换了一个词」挂错了前作。
HOOK = '''<section class="slide">
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
          <div class="d">那一场讲的是屏幕里的声音：怎么让它说话的节奏、语气和分寸，不像一台机器。</div>
          <div class="d"><b>那时候的题：</b>它说话像不像一个人。</div>
        </div>
        <div class="card on rise" style="--i:3">
          <div class="tag">2026.08 · 今天</div>
          <div class="t">有了身体之后</div>
          <div class="d">它从屏幕里走出来，会看、会转头、会伸手，也会当着一屋子人开口。</div>
          <div class="d"><b>今天的题：</b>像个人，为什么还是留不住。</div>
        </div>
      </div>
      <div class="land flow" style="--i:4">像不像一个人，是上一场的题。<b>值不值得被留下来，是今天这一场的题。</b></div>
      <div class="foot flow" style="--i:5">这套框架我在今年 5 月的 RTE 春夏巡游讲过一轮，今天是三个月后的版本——主干没变，多了三件事。</div>
    </div>
  </div>
</section>'''

# ═══════════════════════════════════════════════════════════════
# 三个月增量（从现有 aiot26 取，已建好的页）
# ═══════════════════════════════════════════════════════════════
PANORAMA = a_[3]     # Physical AI 全景 · 两个半场
READOUT = a_[4]      # 消费侧读数 · CES / 资本 / 模型下沉 / 留存没变
MQ_HALVES = a_[6]    # 金句 · 上半场造能干活的身体，下半场造值得被记住的存在
EDGECLOUD = a_[26]   # 工程问题 #4 · 端云边界（三个月新长出来的问题）
BREAKTHROUGH = a_[30]  # 产品化破局（对上大会官方议程题）

# 与主论坛 keynote 对齐（/cowork-conf P20「恰好的那半秒，比快半秒值钱」）：
#   这一页内容本来就是 0ms vs +0.5s 的对照，只是沿用了 0516 的旧标题。
#   改成主论坛那句高光，分论坛就读得出是同一条线的展开。
HALFSEC = one(rs[20],
              '<div class="chrome"><span>同一句话，两种反应</span>',
              '<div class="chrome"><span>恰好的那半秒 · THE RIGHT HALF-SECOND</span>')
HALFSEC = one(HALFSEC,
              '<h2 class="ink" style="--i:1">内容可以一样，反应完全不同。</h2>',
              '<h2 class="ink" style="--i:1">恰好的那半秒，比快半秒值钱。</h2>')

# 与主论坛 keynote 对齐（/cowork-conf PART 2「被记住」P15）：
#   主论坛把这张图写成「伙伴感 = 三份产品资产 × 一个实时引擎」。
#   分论坛是它的展开，中心论点页必须显式挂钩，否则听过主论坛的人会觉得公式变了。
CENTER = one(rs[21],
             '<div class="land flow" style="--i:8">这是一道二选一都不行的题。</div>',
             '<div class="land flow" style="--i:8">这是一道二选一都不行的题。</div>\n'
             '      <div class="foot flow" style="--i:8">主论坛上我把这张图写成'
             '<b>「伙伴感 = 三份产品资产 × 一个实时引擎」</b>——身份、关系、历史就是那三份资产，'
             '临场就是那个引擎。今天这一场，是把它在消费硬件上完整展开一遍。</div>')

# 原 robot26 的「工程问题 #4 架构」在本版顺延为 #5
PROB5 = rs[27].replace('工程问题 #4', '工程问题 #5').replace('ENGINEERING PROBLEM #4', 'ENGINEERING PROBLEM #5')

# 终页：21g 钉子 + 场合信息（robot26 的 rs[40] 是 21g 金句页）
FINALE = one(rs[40],
             '<div class="s rise" style="--i:5">',
             '<div class="s rise" style="--i:5">谢谢 · 姚光华 Colin · 声网 AI 产品线负责人 · '
             '2026 AI 产品大会 · 声网 AIoT 专场 · 北京<br>')

# ═══════════════════════════════════════════════════════════════
# 总装 · 40 页 · 五幕 —— 主干顺序严格照 robot26
# ═══════════════════════════════════════════════════════════════
S = [
    # 开场：抽屉曲线先摆问题（robot26 主干开场）
    COVER, HOOK, rs[3], rs[4],
    # ACT 01 · 风口重估 —— 三个月增量集中在这一幕
    act('01', 'THE WAVE', '风口重估',
        '三个月里，能力侧发生了很多事，关系侧一件也没发生。先看清你在哪半场。'),
    PANORAMA, READOUT, MQ_HALVES,
    # ACT 02 · 分水岭 —— robot26 主干
    act('02', 'THE DIVIDE', '分水岭',
        '不是所有机器人都该做成伙伴。该做的那些，卡住它们的也不是智能，是角色。'),
    rs[6], rs[8], rs[9], rs[5],
    # ACT 03 · 角色三件套 + 一个引擎 —— 0516 的中心论点，现有版本整段缺失
    act('03', '3 ROLES + 1 ENGINE', '角色三件套',
        '身份、关系、历史是你的责任，临场是引擎的责任。这一幕是全场的中心论点。'),
    rs[10], rs[11], rs[12], rs[13], rs[14], rs[17], rs[19], HALFSEC, CENTER, rs[15],
    # ACT 04 · 工程五问 —— robot26 四问 + 端云增量
    act('04', 'FIVE PROBLEMS', '工程五问',
        '来自真实产线的五个问题——前四个 5 月就在，第五个是这三个月新长出来的。'),
    rs[23], rs[24], rs[25], rs[26], EDGECLOUD, PROB5, rs[28],
    # ACT 05 · 交给你 —— 破局 + 背书 + 带走
    act('05', 'THE HANDOFF', '交给你',
        '这条工程路我们替你走过一遍了。剩下的，是只有你能做的那部分。'),
    BREAKTHROUGH, rs[31], rs[34], rs[35], rs[37], rs[38], FINALE,
]
assert len(S) == 40, len(S)

s = head + '\n'.join(S) + tail

# 页码重排
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
assert len(_st) == 40, len(_st)


def _rn(mm):
    return mm.group(1) + ('%02d' % sum(1 for t in _st if t <= mm.start())) + mm.group(2)


s = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _rn, s)
open('public/decks/aiot26.html', 'w', encoding='utf-8').write(s)

# ═══════════════════════════════════════════════════════════════
# 断言：主干必须真的对齐 robot26
# ═══════════════════════════════════════════════════════════════
TXT = re.sub(r'<[^>]+>', ' ', s)
TRUNK = [
    '角色三件套',            # 0516 中心论点 —— 旧版缺失
    '豆豆',                  # 共同历史怎么长出来 —— 旧版缺失
    '关系容量的三级跳',       # 工具 → 熟人 → 伙伴 —— 旧版缺失
    'AMA',                   # 一线提问页 —— 旧版缺失
    'Robotics 1',            # 硬件背书 —— 旧版缺失
    '第六个成员',            # 收束页 —— 旧版缺失
    '声网在这一层',          # 我们的位置 —— 旧版缺失
    '不是所有机器人都该做成伙伴',
    '分水岭', '0.29', '别让人等', '5 个节点',
]
for x in TRUNK:
    assert x in TXT, '主干缺失: ' + x
INCREMENT = ['上半场', '下半场', '端侧', '云端', '破局']
for x in INCREMENT:
    assert x in TXT, '三个月增量缺失: ' + x
assert '三个月，行业换了一个词' not in TXT, '旧钩子（挂错前作）还在'
assert '人人都是产品经理大会' in TXT, '新钩子（挂 2025-12）没生效'
assert len(re.findall(r'<div class="act">', s)) == 5, '幕卡数不对'
assert '工程问题 #5' in TXT and '工程问题 #4' in TXT, '工程问题编号未顺延'
assert '三份产品资产 × 一个实时引擎' in TXT, '未与主论坛 keynote 公式挂钩'
assert '恰好的那半秒' in TXT, '未与主论坛 P20 标题对齐'
for _g in ('实时听见','立刻想起','当下回应'):
    assert _g in TXT, '主论坛临场感金标准缺失: ' + _g

print('aiot26.html · %d 页（保底版）· %dKB' % (len(_st), len(s) // 1024))
print('主干 20 页取自 robot26 还原版 · 增量 5 页 · 幕卡 5 · 钩子改挂 2025-12')
print('主干断言 %d 条 ✓  增量断言 %d 条 ✓' % (len(TRUNK), len(INCREMENT)))
