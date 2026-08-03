#!/usr/bin/env python3
"""一次性烘焙（2026-08-03 定稿）：把大会版内容试验层（R2–R6）+ R7 终稿修正固化进母版 cowork.html。
   定稿原则（Colin）：conf 为最终真源，母版/离线/文档全部对齐 conf 内容。
   烘焙后：母版 62 页（= conf 63 页 − 视频页；媒体仍仅大会版），build-conf.py 回归纯视觉+媒体变换。
   本脚本只可运行一次（入口断言母版 65 页，烘焙后自然失效）。"""
import re

F = "public/decks/cowork.html"
s = open(F, encoding="utf-8").read()
assert len(re.findall(r'<section class="slide', s)) == 65, "母版已非 65 页——烘焙只能执行一次"

# ── 复用 build-conf.py 的完整内容层（6.4 段），保证与线上 conf 逐字一致 ──
_src = open("scripts/build-conf.py", encoding="utf-8").read()
_seg = _src[_src.index("# ── 6.4)"):_src.index("# ── 6.5)")]
exec(compile(_seg, "content-layer", "exec"))

# ═ R7 · 终稿修正（GPT review 商定项 · 2026-08-03） ═════════════
# 1) 96.5% 与 P35「披露底线」对齐：撤「图灵测试 / 毫不知情」，立「已披露前提」
rep1('案例 01 · 真实生产环境 · A PRODUCTION-SCALE TURING TEST',
     '案例 01 · 真实生产环境 · A PRODUCTION-SCALE MEASUREMENT')
rep1('2,475 通全量人工标注的真实外呼里，只有 <b>86 通</b> 被对方听出「这是 AI」。',
     '2,475 通全量人工标注的真实外呼里，只有 <b>86 通</b> 出现「机器感」信号。')
rep1('<div class="foot flow" style="--i:4">1950 年，图灵提出那个判别游戏的时候，设想的是一场五分钟的文字对谈。<br>76 年之后，这件事是在一条电话线上、由一个真的要把东西卖给你的人、在毫不知情的状态下完成的。</div>',
     '<div class="foot flow" style="--i:4">图灵设想的考题，是「伪装成人」。真实生产环境里更难的考题是：<br>开场第一句就承认自己是 AI，对方还愿意把这通电话好好聊完——96.5%，是在<b>已披露</b>的前提下拿到的。</div>')
rep1('那 3.5%，是怎么露的马脚 · 九类「AI 感知信号」',
     '那 3.5% 的机器感，从哪来 · 九类「AI 感知信号」')

# 2) 措辞统一：护栏 → 围栏（Colin 语言习惯；护城河不动）
_hl = s.count('护栏')
assert _hl == 8, f"护栏出现 {_hl} 处，预期 8(6正文+2注释)"
s = s.replace('护栏', '围栏')

# 3) P40 · 权责一句：化解「业绩记它名下」与「不可自我审批」的表面冲突
rep1('<b>先有归属，才谈得上追责。</b>',
     '<b>先有归属，才谈得上追责——业绩可以记在它名下，责任必须落在可追责的人身上。</b>')

# 4) 金句编号按新页序重排（原 06/05 倒序）
_mq = [0]
def _mqf(mm):
    _mq[0] += 1
    return 'Money Quote · 0%d' % _mq[0]
s = re.sub(r'Money Quote · 0\d', _mqf, s)
assert _mq[0] == 6, _mq[0]

# ═ 收尾：页码重排 + 封面页数 + 内容层样式移植 ═══════════════
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
assert len(_st) == 62, f"烘焙后应 62 页，实际 {len(_st)}"
def _rn(mm):
    idx = sum(1 for t in _st if t <= mm.start())
    return mm.group(1) + str(idx) + mm.group(2)
s = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _rn, s)

rep1('40 min · 65 slides', '40 min · 62 slides')

BAKE_CSS = """
/* ═ 定稿烘焙 · 内容层样式（2026-08-03 · 与大会版共用，全 token 双主题安全） ═ */
.mega .mh{font-size:46px;font-weight:900;color:var(--ink);letter-spacing:.01em;margin-bottom:-4px;}
.m35{position:absolute;right:120px;top:256px;width:560px;display:flex;flex-direction:column;gap:16px;}
.m35 .mk{font-family:var(--f-mono);font-size:14px;letter-spacing:.2em;color:var(--coral);margin-bottom:6px;}
.m35 .row{display:grid;grid-template-columns:64px 1fr;column-gap:16px;row-gap:7px;align-items:baseline;}
.m35 .row .n{font-family:var(--f-en);font-size:36px;font-weight:900;line-height:1;color:var(--ink);text-align:right;}
.m35 .row .t{font-size:20px;color:var(--ink-2);}
.m35 .row .bar{grid-column:2;height:7px;width:var(--w);background:var(--coral);opacity:.85;border-radius:2px;}
.m35 .sx{font-size:16px;line-height:1.7;color:var(--ink-3);border-top:1px solid var(--hair);padding-top:14px;margin-top:4px;}
.m35 .sx b{color:var(--ink-2);}
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
"""
_li = s.rindex("</style>")
s = s[:_li] + BAKE_CSS + s[_li:]

open(F, "w", encoding="utf-8").write(s)
n = len(re.findall(r'<section class="slide', s))
print(f"母版烘焙完成 · {n} 页 · {len(s)//1024}KB · 金句 {_mq[0]} 条已重排 · 围栏统一 {_hl} 处")
