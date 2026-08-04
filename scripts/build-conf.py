#!/usr/bin/env python3
"""cowork.html → cowork-conf.html：2026 AI 产品大会视觉版。
   完全对齐大会模板：黑底 + 紫系(#9333EA/#A855F7/#C084FC) + 金黄 #FFC000 +
   阿里巴巴普惠体 2.0 + 页头紫 tab/双 logo + 模板封面 keyart + 章节页/观点页版式。
   内容与 62 页定稿母版逐字一致（内容层已烘焙进母版），仅叠加视觉层与媒体层
   （P3 录音 + 「授权可收回」页后插视频页）+ 演讲压缩层（-5），共 58 页。
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
      <div class="eyebrow flow" style="--i:0">先看钱往哪儿去了 · 再看渗透到了哪儿</div>
      <h2 class="ink" style="--i:1">整个赛道在同时点火，<em>采购已经开动</em></h2>
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
_order = ([0, 1, 2, 3, 4, 5, 6, 8, 9]          # P1-6 · 融合钱×渗透 · 四方观点 · 融合阶段×北极星
          + list(range(11, 55))                  # MQ12 起至 对产品管理者(m55) —— 案例06(m56)删
          + [56, 57]                             # 对 CEO 说 · 对组织说 —— 进化(m60)删
          + [60, 58])                            # 收束(越往上答案越短) → 尺子两面(向外Eval向内内观)收全场 —— 终页(m62)删
s = _head2 + '\n'.join(_secs[o] for o in _order) + _tail2
assert len(re.findall(r'<section class="slide', s)) == 57, "压缩后应 57 页"

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
assert len(_vs) == 57, f"压缩层后应 57 页，实际 {len(_vs)}"
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
assert n == 58, f"大会版应为 58 页，实际 {n}"
print(f"cowork-conf.html written · {n} slides · {len(s)//1024}KB")
assert "deckRuler" in s and "noindex" in s
print("ruler ✓ noindex ✓")
