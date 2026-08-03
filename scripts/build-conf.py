#!/usr/bin/env python3
"""cowork.html → cowork-conf.html：2026 AI 产品大会视觉版。
   完全对齐大会模板：黑底 + 紫系(#9333EA/#A855F7/#C084FC) + 金黄 #FFC000 +
   阿里巴巴普惠体 2.0 + 页头紫 tab/双 logo + 模板封面 keyart + 章节页/观点页版式。
   内容与 65 页母版逐字一致，另叠加【仅大会版】内容试验层（2026-08-03 反馈：删两条路页/挪三把尺子与时机页/终幕对象化等）
   与媒体层（P3 录音 + 「授权可收回」页后插视频页），共 65 页。
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

# a) P15 分水岭 · 挪入「九成产品卡在这一格」（原 P16 的卡点标记）
rep1('<circle class="fill-am pop" style="--i:4" cx="840" cy="150" r="9"/>',
     '''<circle class="fill-am pop" style="--i:4" cx="840" cy="150" r="9"/>
          <circle class="stroke-co pop" style="--i:5" cx="840" cy="150" r="17" stroke-width="2"/>
          <text class="lbl fill-co pop" style="--i:5" x="806" y="240" text-anchor="end">九成产品卡在这一格</text>''')

# b) P27 眉题：岔路口页（原 P16）删除后，改指第二幕分水岭
rep1('接上一幕的岔路口 · 我们换到下面那条', '接第二幕的分水岭 · 这次走「替你干活」这条路')

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

# d) P37 · Eval 升维：不止交互质量，是商业化结果的计量基础设施
rep1('<div class="eyebrow flow" style="--i:0">把上面两页接起来</div>',
     '<div class="eyebrow flow" style="--i:0">把上面两页接起来 · EVAL 的身份升级</div>')
rep1('<h2 class="ink" style="--i:1">评测不是质量流程，是计费基础设施</h2>',
     '<h2 class="ink" style="--i:1">评测不再只量交互质量，是<em>商业化结果</em>的计量基础设施</h2>')
rep1('<div class="land flow" style="--i:12">出题权的移交，就是信任的移交。<span class="s">',
     '<div class="land flow" style="--i:12">Eval 已经从「对交互质量的评测」，长成产品经理衡量<b>最终商业化结果</b>的关键基础设施——出题权的移交，就是信任的移交。<span class="s">')

# e) 终幕三个「对象」标记 + 标题切心
rep1('<h2 class="ink" style="--i:1">你交付的不再是一份 PRD，是<em>一套评测</em></h2>',
     '<h2 class="ink" style="--i:1">对产品经理说：你交付的不再是一份 PRD，是<em>一套评测</em></h2>')
rep1('<h2 class="ink" style="--i:1">看过、用过、学过、<em>干过</em></h2>',
     '<h2 class="ink" style="--i:1">对个人说：你站到哪一阶了——看过、用过、学过、<em>干过</em></h2>')
rep1('<h2 class="ink" style="--i:1">转身的第一个动作，是<em>把那条线画出来</em></h2>',
     '<h2 class="ink" style="--i:1">对组织说：先分清哪些是<em>单向门</em>，哪些是<em>双向门</em></h2>')

# f) 结构调整：删 P16；P45(三把尺子)挪到 P42(岗位)后；P50(时机)挪到「语音没有撤回键」前；
#    终幕对调：先对个人(P57,P58)，再对产品经理(P56)
_starts = [m.start() for m in re.finditer(r'<section class="slide', s)]
_ends = [s.index('</section>', st) + len('</section>') for st in _starts]
for _i in range(len(_starts) - 1):
    assert s[_ends[_i]:_starts[_i+1]].strip() == '', "section 之间有非空内容，重排会丢"
_head, _tail = s[:_starts[0]], s[_ends[-1]:]
_secs = [s[_starts[_i]:_ends[_i]] for _i in range(len(_starts))]
assert len(_secs) == 65, f"母版应 65 页，实际 {len(_secs)}"
order = (list(range(0, 15))            # P1–P15
         + list(range(16, 41))         # P17–P41（跳过 P16）
         + [41, 44, 49, 42, 43, 45, 46, 47, 48]   # 岗位→三把尺子→时机→撤回论证→撤回MQ→审批→案例04/05→MQ
         + list(range(50, 55))         # 工牌…章节页
         + [56, 57, 55, 58, 59, 60]    # 个人四阶→High Agency→产品经理evals→第四圆→案例06→组织门
         + list(range(61, 65)))        # 尺子两面…终页
assert sorted(order) == [i for i in range(65) if i != 15]
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
assert len(_vs) == 64, f"试验层后应 64 页，实际 {len(_vs)}"
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
/* 案例02 · 右侧 3.5% 拆解面板（内容试验层） */
.m35{position:absolute;right:120px;top:216px;width:560px;display:flex;flex-direction:column;gap:16px;}
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
assert n == 65, f"大会版应为 65 页，实际 {n}"
print(f"cowork-conf.html written · {n} slides · {len(s)//1024}KB")
assert "deckRuler" in s and "noindex" in s
print("ruler ✓ noindex ✓")
