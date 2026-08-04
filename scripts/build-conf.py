#!/usr/bin/env python3
"""cowork.html → cowork-conf.html：2026 AI 产品大会视觉版。
   完全对齐大会模板：黑底 + 紫系(#9333EA/#A855F7/#C084FC) + 金黄 #FFC000 +
   阿里巴巴普惠体 2.0 + 页头紫 tab/双 logo + 模板封面 keyart + 章节页/观点页版式。
   内容与 62 页定稿母版逐字一致（内容层已烘焙进母版），仅叠加视觉层与媒体层
   （P3 录音 + 「授权可收回」页后插视频页）+ 演讲压缩层（两轮 -8），共 55 页。
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

# ──（内容层已于 2026-08-03 定稿烘焙进母版；母版 = /cowork final 定格，自此冻结）──
# ── 6.4-C) 演讲压缩层（2026-08-04 · 仅大会版 · -5 页 → 58 页） ──
# 目标：时长可控。① P7×P8 融合(左钱右渗透,分步展开) ② P10×P11 融合(阶段为主轴,北极星挂下方)
# ③ 删 案例06(十一周)/四条线(进化)/终页 ④ 收束挪到「尺子两面」前——全场以「向外叫 Eval,向内叫内观」收束
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
_en = [s.index('</section>', t) + len('</section>') for t in _st]
_head2, _tail2 = s[:_st[0]], s[_en[-1]:]
_secs = [s[_st[i]:_en[i]] for i in range(len(_st))]
assert len(_secs) == 62, f"母版应 62 页，实际 {len(_secs)}"

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

_order = ([0, 1, 2, 3, 4, 5, 6, 8, 9]          # P1-6 · 融合钱×渗透 · 四方观点 · 融合阶段×北极星
          + list(range(11, 22)) + [23, 22] + list(range(24, 28))
          # ↑ C5：金句02(23) 与 反共识页(22) 换序 —— 恰好半秒 → 视频 → 金句02 → 反共识 → PART 3
          #        反共识页后移，承上启下直接引出 PART 3（元素数仍 17）
          + [28, 31, 30]                         # Eval 第一课(一二合并) → 第二课(裁判,原四) → 第三课(听失败,方法论收尾)
          + list(range(32, 39))                  # MQ选评测 … 章节双向奔赴
          + [39, 40]                             # 爬梯×交叉验证(类比已并入) · 岗位
          + list(range(42, 46))                  # 协作审批 · 双围栏案例 · Waymo · MQ护城河
          + [46]                                 # 两道围栏合一(体验+执行,黑页撤回键随后)
          + list(range(48, 55))                  # MQ撤回键 … 对产品管理者
          + [56, 57]                             # 对 CEO 说 · 对组织说
          + [60, 58])                            # 收束 → 尺子两面收全场
s = _head2 + '\n'.join(_secs[o] for o in _order) + _tail2
assert len(re.findall(r'<section class="slide', s)) == 54, "压缩后应 54 页"

# ── 6.5) 媒体层（仅大会版；母版/线上 /cowork 保持无媒体） ────
# a) P3 页内录音（真实外呼片段，完美嵌入，无需解说文字）
CHROME3 = '<div class="chrome"><span>PART 0 · 开场</span><span>3</span></div>'
assert s.count(CHROME3) == 1, "P3 chrome 定位失败"
AUDIO = (CHROME3 + '\n  <audio data-dm src="/media/cowork/p3-call.mp3" preload="auto"></audio>'
         '\n  <div class="dm-ind" aria-hidden="true"></div>')
s = s.replace(CHROME3, AUDIO, 1)

# b) 插入全幅视频页（陪伴类智能体 · 多模态交互 demo，无文字）
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
# 插到最后一个 </style> 前（主样式表尾部）
li = s.rindex("</style>")
s = s[:li] + CONF_CSS + s[li:]

open("public/decks/cowork-conf.html", "w", encoding="utf-8").write(s)
n = len(re.findall(r'<section class="slide', s))
assert n == 55, f"大会版应为 55 页，实际 {n}"
print(f"cowork-conf.html written · {n} slides · {len(s)//1024}KB")
assert "deckRuler" in s and "noindex" in s
# C2/C3 内容在位（防「定义了未装配」）
for _mk in ("题之骗 × 粒度之骗", "HUMAN IN THE LOOP", "TWO FENCES", "Eval 第二课", "交叉验证 · 两个行业的断层",
            "本场提要</h2>", "四个互不相干的人，说了", "商业模式变迁", "人还在不在环里</em></h2>", "就是「按结果收钱」的计费口径",
            "四个阶段，四颗", "不应该</em>被记住", "单轮打分", "一个新的融合岗位", "一套放权与决策机制", "OpenAI 前 CPO",
            "紫 = 已规模商业化", "金黄 = 强监管场景", "这条弧线不存在", "文本通道 · TEXT CHANNEL", "语音通道 · VOICE CHANNEL",
            'd="M675 6 V172"'):
    assert _mk in s, f"C2/C3/C4/C5 内容缺失：{_mk}"
assert "Eval 第四课" not in s
assert "暖橙 = 已规模商业化" not in s and "粉 = 强监管场景" not in s
# C5 换序：视频页在「恰好的那半秒」之后、金句02 之前；反共识页排在金句02 之后
_i_half, _i_video = s.index('恰好的那半秒'), s.index('gemini-demo.mp4')
_i_mq02, _i_anti = s.index('值得被记住的存在'), s.index('本场第一处反共识')
assert _i_half < _i_video < _i_mq02 < _i_anti, "C5 换序失败：恰好半秒 → 视频 → 金句02 → 反共识"
print("ruler ✓ noindex ✓ C2/C3 content ✓")
