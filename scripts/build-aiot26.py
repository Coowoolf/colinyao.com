#!/usr/bin/env python3
"""aiot26 · 「当 AI 有了身体」——从玩具到伙伴的 Physical AI 升维版（35 页 · 双主题）。
   底盘：robot26.html（RTE 春夏巡游原版，组件库同源）；
   移植：cowork 定稿的 分水岭(熟人版)/临场感三块动效/半秒页 + .pkt 动效 + 媒体模块(gemini 视频)；
   新写：钩子/双赛道全景/消费读数/端×云五问/破局主张/五幕章节/首尾页。
   场合：2026 AI 产品大会 · 声网 AIoT 专场 · 2026.08.09 北京 · 30 min。"""
import re

R = open("public/decks/robot26.html", encoding="utf-8").read()
C = open("public/decks/cowork.html", encoding="utf-8").read()
SEC = re.compile(r'<section class="slide[^"]*">.*?</section>', re.S)
rs = SEC.findall(R)
cs = SEC.findall(C)
assert len(rs) == 36 and len(cs) == 62

head = R[:R.index('<section class="slide')]
tail = R[R.rindex('</section>') + len('</section>'):]

def one(hay, old, new):
    assert hay.count(old) == 1, "锚点失效: " + old[:50]
    return hay.replace(old, new, 1)

# ═ 移植 CSS（.pkt / prz3 / 媒体） ═
PORT_CSS = """
/* ═ aiot26 移植层：pkt 光点 · 临场感三块 · 页内媒体（token 双主题安全） ═ */
.pkt{stroke-linecap:round;stroke-dasharray:var(--pl,72) 4000;
  stroke-dashoffset:var(--p0,72px);opacity:0;
  animation:pktrun var(--pt,7.2s) linear infinite var(--pd,0s);}
@keyframes pktrun{
  0%  {stroke-dashoffset:var(--p0,72px);opacity:0;}
  6%  {opacity:1;}
  38% {opacity:1;}
  47% {stroke-dashoffset:var(--p1,-940px);opacity:0;}
  100%{stroke-dashoffset:var(--p1,-940px);opacity:0;}
}
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
.dm-ind{position:absolute;right:64px;bottom:56px;width:10px;height:10px;border-radius:50%;background:var(--amber);opacity:0;transition:opacity .4s;z-index:40;}
.slide.dm-playing .dm-ind{opacity:.9;animation:dmpulse 1.1s ease-in-out infinite;}
@keyframes dmpulse{0%,100%{transform:scale(1);opacity:.9;}50%{transform:scale(1.55);opacity:.45;}}
.vslide{position:absolute;inset:0;background:#000;display:flex;align-items:center;justify-content:center;}
.vslide video{width:100%;height:100%;object-fit:contain;background:#000;}
"""
head = head[:head.rindex('</style>')] + PORT_CSS + head[head.rindex('</style>'):]
head = re.sub(r'<title>[^<]*</title>',
  '<title>当 AI 有了身体 · 从玩具到伙伴 · 2026 AI 产品大会 AIoT 专场</title>', head, count=1)

MEDIA_JS = '''<script>
/* deck-media：媒体页按键行为与 PPT 对齐（第一按播，再按停+翻页；M 键手动） */
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
tail = one(tail, '</body>', MEDIA_JS + '\n</body>')

# ═ 新页 ═══════════════════════════════════════════════════════
COVER = '''<section class="slide">
  <div class="cover">
    <div class="kicker flow" style="--i:0">人人都是产品经理 · 2026 AI 产品大会 · 声网 AIoT 专场</div>
    <h1 class="ink" style="--i:1">当 AI，<br>有了身体。</h1>
    <div class="subtitle spread" style="--i:3">从玩具到伙伴 · 多模态交互的产品化破局</div>
    <div class="meta">
      <div class="rise" style="--i:4"><span class="k">场合</span><span class="v">AI 硬件多模态交互的产品化破局 · 声网 AIoT 专场</span></div>
      <div class="rise" style="--i:5"><span class="k">日期</span><span class="v">2026.08.09 · 北京 · 渔阳饭店</span></div>
      <div class="rise" style="--i:6"><span class="k">讲者</span><span class="v">姚光华 Colin · 声网 AI 产品线负责人</span></div>
      <div class="rise" style="--i:7"><span class="k">时长</span><span class="v">30 min · 35 slides</span></div>
    </div>
  </div>
</section>'''

HOOK = '''<section class="slide">
  <div class="chrome"><span>三个月 · THEN AND NOW</span><span>02</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">上一场与这一场之间</div>
      <h2 class="ink" style="--i:1">三个月，行业换了一个词</h2>
    </div>
    <div class="body">
      <div class="fig flow" style="--i:2">
        <svg viewBox="0 0 1620 300" width="1620" height="300">
          <path class="dw" style="--len:1520;--i:0" d="M50 150 H1570" stroke="var(--hair)" stroke-width="1" fill="none"/>
          <path class="stroke-am pkt" style="--pl:26px;--p0:26px;--p1:-1520px;--pt:6s" stroke-width="4" d="M50 150 H1570"/>
          <g class="pop" style="--i:1">
            <circle cx="240" cy="150" r="8" class="fill-ink"/>
            <text class="lbl" x="240" y="72" text-anchor="middle">2026.05.16 · 深圳</text>
            <text class="ttl" x="240" y="116" text-anchor="middle">从玩具到伙伴</text>
            <text class="sm" x="240" y="200" text-anchor="middle">RTE 春夏巡游 · 活人感交互</text>
          </g>
          <g class="pop" style="--i:3">
            <circle cx="810" cy="150" r="8" class="fill-ink"/>
            <text class="lbl" x="810" y="72" text-anchor="middle">这三个月</text>
            <text class="ttl" x="810" y="116" text-anchor="middle">Physical AI 成了行业词</text>
            <text class="sm" x="810" y="200" text-anchor="middle">世界模型迭代 · VLA 上端侧 · 陪伴硬件集体出海</text>
          </g>
          <g class="pop" style="--i:5">
            <circle cx="1400" cy="150" r="11" class="fill-am"/>
            <text class="lbl" x="1400" y="72" text-anchor="middle" fill="var(--amber)">2026.08.09 · 北京</text>
            <text class="ttl" x="1400" y="116" text-anchor="middle" fill="var(--amber)">当 AI 有了身体</text>
            <text class="sm" x="1400" y="200" text-anchor="middle" fill="var(--amber)">多模态交互的产品化破局</text>
          </g>
        </svg>
      </div>
      <div class="land flow" style="--i:7">词换了，题没换——<b>分水岭还是角色，不是参数量。</b><span class="s">今天把三个月前那条路，用 Physical AI 的坐标重走一遍，再多走三步：看见、行动、破局。</span></div>
    </div>
  </div>
</section>'''

def act(num, en, cn, d):
    return f'''<section class="slide">
  <div class="act">
    <div class="num flow" style="--i:0">{num}</div>
    <div class="en settle" style="--i:1">{en}</div>
    <div class="cn spread" style="--i:3">{cn}</div>
    <div class="d flow" style="--i:4">{d}</div>
  </div>
</section>'''

ACT1 = act('ACT 01', 'THE WAVE', '风口重估', '上半场在造能干活的身体，下半场在造值得被记住的存在。先看清你在哪半场。')
ACT2 = act('ACT 02', 'THE DIVIDE', '分水岭没动', '三个月过去，3 天扔抽屉的曲线一点没变。分水岭还是角色，不是参数量。')
ACT3 = act('ACT 03', 'PRESENCE', '临场感', '多模态不是四个功能并列，是「在场」的四个器官。这一幕讲它怎么落地成体验。')
ACT4 = act('ACT 04', 'FIVE PROBLEMS', '工程五问', '来自真实产线的五个问题——前四个三个月前就在，第五个是这三个月新长出来的。')
ACT5 = act('ACT 05', 'THE HANDOFF', '产品化破局', '这条工程路我们替你走过一遍：3-6 个月的链路调试，应该被封装成一层接口。')

PANORAMA = '''<section class="slide">
  <div class="chrome"><span>Physical AI 全景 · TWO HALVES</span><span>04</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">2026 · 同一个词，两个半场</div>
      <h2 class="ink" style="--i:1">上半场造「能干活的身体」，下半场造「值得被记住的存在」</h2>
    </div>
    <div class="body">
      <div class="fig flow" style="--i:2">
        <svg viewBox="0 0 1620 330" width="1620" height="330">
          <text class="lbl" x="810" y="26" text-anchor="middle">PHYSICAL AI · 感知 → 理解 → 行动 · 同一套底层</text>
          <path class="dw" style="--len:220;--i:1" d="M810 40 V260" stroke="var(--hair)" stroke-width="1" stroke-dasharray="6 8" fill="none"/>
          <g class="pop" style="--i:2">
            <rect x="60" y="70" width="660" height="190" rx="4" class="box" stroke-width="1"/>
            <text class="ttl" x="390" y="116" text-anchor="middle">上半场 · 工业与人形</text>
            <text class="sm" x="390" y="156" text-anchor="middle">世界模型（Cosmos 3）· VLA 基础模型（GR00T / π / Gemini Robotics）</text>
            <text class="sm" x="390" y="188" text-anchor="middle">人形本体量产 · 任务泛化 · 数据飞轮</text>
            <text class="lbl" x="390" y="234" text-anchor="middle">尺子：任务完成率 · 每小时产出</text>
          </g>
          <g class="pop" style="--i:4">
            <rect x="900" y="70" width="660" height="190" rx="4" fill="none" stroke="var(--amber)" stroke-width="2"/>
            <text class="ttl" x="1230" y="116" text-anchor="middle" fill="var(--amber)">下半场 · 消费与陪伴</text>
            <text class="sm" x="1230" y="156" text-anchor="middle" fill="var(--amber)">AI 玩具 · 陪伴机器人 · 桌面机器人 · AI 眼镜 · 教育硬件</text>
            <text class="sm" x="1230" y="188" text-anchor="middle" fill="var(--amber)">多模态交互 · 情感体验 · 角色与关系</text>
            <text class="lbl" x="1230" y="234" text-anchor="middle" fill="var(--amber)">尺子：明天还想不想跟它待着</text>
          </g>
          <text class="sm" x="810" y="304" text-anchor="middle">两个半场共用技术栈，不共用尺子——今天这场，讲下半场。</text>
        </svg>
      </div>
      <div class="land flow" style="--i:6">下半场离钱更近，也离关系更近——<b>它不考「搬得动多少」，考「有没有人愿意再按亮它」。</b></div>
    </div>
  </div>
</section>'''

READOUT = '''<section class="slide">
  <div class="chrome"><span>消费侧读数 · THE SIGNALS</span><span>05</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">这三个月，下半场发生了什么</div>
      <h2 class="ink" style="--i:1">钱和人都到齐了，缺的是产品方法</h2>
    </div>
    <div class="body">
      <div class="g4">
        <div class="card sm rise" style="--i:2"><div class="hd"><div class="n">01</div><div class="t">集体登场</div></div><div class="d">CES 2026 上，<b>超 30 家</b>国产 AI 玩具 / 陪伴机器人集中亮相——从玩具展区走进主展馆。</div><div class="tag">供给侧 · 拥挤起来了</div></div>
        <div class="card sm rise" style="--i:3"><div class="hd"><div class="n">02</div><div class="t">资本定调</div></div><div class="d">头部陪伴玩具完成<b>亿元级融资</b>启动全球化；红杉把 AI 玩具类比成「AI 界的泡泡玛特」。</div><div class="tag">资本侧 · 叙事成立</div></div>
        <div class="card sm rise" style="--i:4"><div class="hd"><div class="n">03</div><div class="t">模型下沉</div></div><div class="d">VLA 出现<b>端侧版本</b>，世界模型走到全模态——「大脑」开始装进小设备。</div><div class="tag">技术侧 · 门槛在降</div></div>
        <div class="card sm rise" style="--i:5"><div class="hd"><div class="n">04</div><div class="t">留存没变</div></div><div class="d">爆款接连出圈，但复购与长期留存依然是全行业的暗伤——<b>3 天曲线还在</b>。</div><div class="tag">需求侧 · 老题未解</div></div>
      </div>
      <div class="note flow" style="--i:6">口径说明：以上为公开报道（CES 2026 行业盘点 / 融资公告 / 厂商发布），非声网数据。</div>
      <div class="land flow" style="--i:7">三个月前我说：消费机器人今天解的题，就是具身明天直接继承的能力。<span class="s">上面这一排新闻，就是这句话正在被验证的样子。</span></div>
    </div>
  </div>
</section>'''

MQ_HALVES = '''<section class="slide">
  <div class="mq">
    <div class="mark flow" style="--i:0">MONEY QUOTE · 01</div>
    <div class="q">
      <i class="rise" style="--i:1">上半场，造能干活的身体；</i>
      <i class="rise" style="--i:3">下半场，造值得被记住的存在。</i>
    </div>
    <div class="rule"></div>
    <div class="s rise" style="--i:5">两个半场共用技术，不共用尺子。</div>
  </div>
</section>'''

VIDEO = '''<section class="slide">
  <div class="vslide">
    <video data-dm src="/media/cowork/gemini-demo.mp4" preload="auto" playsinline></video>
    <div class="dm-ind" aria-hidden="true"></div>
  </div>
</section>'''

EDGECLOUD = '''<section class="slide">
  <div class="chrome"><span>工程问题 #4 · EDGE × CLOUD</span><span>27</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow coral flow" style="--i:0">这三个月新长出来的问题</div>
      <h2 class="ink" style="--i:1">端侧醒着，云端想着——切错了，临场感就没了</h2>
    </div>
    <div class="body">
      <div class="g3">
        <div class="card rise" style="--i:2">
          <div class="n">原则 01</div>
          <div class="tag">反应在端</div>
          <div class="t">临场不许排队</div>
          <div class="d">唤醒、打断、表情、避障——半秒内必须有反应的事，一个来回云端都嫌多。</div>
        </div>
        <div class="card rise" style="--i:3">
          <div class="n">原则 02</div>
          <div class="tag">理解在云</div>
          <div class="t">人格和记忆要长大</div>
          <div class="d">角色、共同历史、复杂推理放云端——它们要随关系变厚，不能被一颗 SoC 封顶。</div>
        </div>
        <div class="card rise" style="--i:4">
          <div class="n">原则 03</div>
          <div class="tag">断网不失态</div>
          <div class="t">降级也要像个伙伴</div>
          <div class="d">网络抖动时宁可说「我想想」，也不能定住三秒——失态一次，角色就碎一次。</div>
        </div>
      </div>
      <div class="note flow" style="--i:5">行业信号：VLA 已有端侧版本、世界模型走向全模态——「切在哪」第一次成了产品决策，不是硬件预算决策。</div>
      <div class="land flow" style="--i:6">切分的标准不是算力，是体验红线：<b>哪些事慢半秒就出戏，哪些事可以想两秒。</b></div>
    </div>
  </div>
</section>'''

BREAKTHROUGH = '''<section class="slide">
  <div class="chrome"><span>产品化破局 · THE BREAKTHROUGH</span><span>31</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">大会主题词，给一个工程答案</div>
      <h2 class="ink" style="--i:1">把 3-6 个月的链路调试，封装成一层接口</h2>
    </div>
    <div class="body">
      <div class="duo">
        <div class="flow" style="--i:2">
          <div class="h">自己拼</div>
          <div class="b">ASR + LLM + TTS + 视觉 + RTC，五条链自己焊</div>
          <div class="s">让一台硬件「同时听得清、看得懂、反应快」，行业平均要调 3-6 个月——精力全花在抠通信链路上。</div>
        </div>
        <div class="flow rev" style="--i:4">
          <div class="h">接一层</div>
          <div class="b">声网对话式 AI 开发套件 · 多模态实时交互标准化接口</div>
          <div class="s">低延迟、高稳定、易集成；AI 教育、陪伴机器人、智能穿戴、智能家居已规模化落地。精力回到角色、关系和体验。</div>
        </div>
      </div>
      <div class="note flow" style="--i:6"><b>模型决定能力上限，引擎决定体验下限</b>——上限交给大模型的进化，下限用工程锁死。</div>
      <div class="land flow" style="--i:7">破局点不是再多一个功能，是<b>把不该你解的题外包，把只有你能做的角色做穿。</b></div>
    </div>
  </div>
</section>'''

FINALE = '''<section class="slide">
  <div class="cover">
    <div class="kicker flow" style="--i:0">谢谢</div>
    <h1 class="ink" style="--i:1">模型给它大脑，<br>引擎给它临场，<br>角色给它名字。</h1>
    <div class="subtitle spread" style="--i:3">三者都有，才叫伙伴 · 姚光华 Colin</div>
    <div class="meta">
      <div class="rise" style="--i:4"><span class="k">场合</span><span class="v">2026 AI 产品大会 · 声网 AIoT 专场</span></div>
      <div class="rise" style="--i:5"><span class="k">日期</span><span class="v">2026.08.09 · 北京</span></div>
      <div class="rise" style="--i:6"><span class="k">系列</span><span class="v">从玩具到伙伴 · Physical AI 升维版（前作 · RTE 春夏巡游 2026.05）</span></div>
      <div class="rise" style="--i:7"><span class="k">讲者</span><span class="v">姚光华 Colin · 声网 AI 产品线负责人</span></div>
    </div>
  </div>
</section>'''

# ═ 移植与改造 ═════════════════════════════════════════════════
def w1620(sec):  # cowork 图幅 1680 → 底盘 1620 等比缩放
    return sec.replace('width="1680"', 'width="1620"')

# 分水岭 · 熟人版（cowork idx14）
DIVIDE = cs[14]
DIVIDE = one(DIVIDE, '<div class="chrome"><span>PART 2 · 被记住</span><span>15</span></div>',
             '<div class="chrome"><span>真正的分水岭 · THE REAL DIVIDE</span><span>11</span></div>')
DIVIDE = one(DIVIDE, '这一页是整个第二幕的判断依据', '三个月过去，这一页还是判断依据')
DIVIDE = w1620(DIVIDE)

# 临场感三块动效（cowork idx20）→ 多模态版
PRES = cs[20]
PRES = one(PRES, '<div class="chrome"><span>PART 2 · 被记住</span><span>21</span></div>',
           '<div class="chrome"><span>临场感 · PRESENCE</span><span>18</span></div>')
PRES = one(PRES, '<div class="eyebrow flow" style="--i:0">第二幕的高光 · PRESENCE</div>',
           '<div class="eyebrow flow" style="--i:0">多模态的正确打开方式 · 三个器官一秒同频</div>')
PRES = one(PRES, '01 · HEAR IT LIVE', '01 · SEE &amp; HEAR IT LIVE')
PRES = one(PRES, '<div class="pzt">实时<b>听见</b></div>', '<div class="pzt">实时<b>感知</b></div>')
PRES = one(PRES, '声音进来的那一刻，它已经在听——不是录完、转写完，再来理解。',
           '声音和画面进来的那一刻，它已经在理解——不是录完、转写完，再来分析。')
PRES = one(PRES, '在这句话还热着的时候接住它——而不是三秒后给一个正确答案。',
           '在这句话还热着的时候接住它——用语气回应，也用一个抬头回应。')
PRES = w1620(PRES)

# 恰好的那半秒（cowork idx21）
HALF = cs[21]
HALF = one(HALF, '<div class="chrome"><span>PART 2 · 被记住</span><span>22</span></div>',
           '<div class="chrome"><span>恰好的那半秒 · THE RIGHT HALF-SECOND</span><span>19</span></div>')
HALF = w1620(HALF)

# 坐标：30 年换五次（robot26 idx16 · 整图重画）
COORD = rs[16]
COORD = one(COORD, '交互的坐标，30 年换了四次。', '交互的坐标，30 年换了五次。')
_c0 = COORD.index('<svg viewBox="0 0 1620 300"')
_c1 = COORD.index('</svg>') + len('</svg>')
COORD = COORD[:_c0] + '''<svg viewBox="0 0 1620 300" width="1620" height="300">
          <path class="dw" style="--len:1520;--i:0" d="M50 180 H1570" stroke="var(--hair)" stroke-width="1" fill="none"/>
          <g class="pop" style="--i:1">
            <circle cx="160" cy="180" r="7" class="fill-ink"/>
            <text class="lbl" x="160" y="80" text-anchor="middle">1990s</text>
            <text class="ttl" x="160" y="124" text-anchor="middle">人 ↔ 人</text>
            <text class="sm" x="160" y="230" text-anchor="middle">电话 / 视频</text>
          </g>
          <g class="pop" style="--i:2">
            <circle cx="480" cy="180" r="7" class="fill-ink"/>
            <text class="lbl" x="480" y="80" text-anchor="middle">2010s</text>
            <text class="ttl" x="480" y="124" text-anchor="middle">人 ↔ 机</text>
            <text class="sm" x="480" y="230" text-anchor="middle">IVR · Alexa · 指令式</text>
          </g>
          <g class="pop" style="--i:3">
            <circle cx="800" cy="180" r="7" class="fill-ink"/>
            <text class="lbl" x="800" y="80" text-anchor="middle">2024</text>
            <text class="ttl" x="800" y="124" text-anchor="middle">人 ↔ 模</text>
            <text class="sm" x="800" y="230" text-anchor="middle">ChatGPT · 对话式</text>
          </g>
          <g class="pop" style="--i:4">
            <circle cx="1120" cy="180" r="7" class="fill-ink"/>
            <text class="lbl" x="1120" y="80" text-anchor="middle">2025</text>
            <text class="ttl" x="1120" y="124" text-anchor="middle">人 + 模 + 人</text>
            <text class="sm" x="1120" y="230" text-anchor="middle">消费机器人 / AI 眼镜 · 共在</text>
          </g>
          <g class="pop" style="--i:5">
            <circle cx="1460" cy="180" r="10" class="fill-am"/>
            <text class="lbl" x="1460" y="80" text-anchor="middle" fill="var(--amber)">2026</text>
            <text class="ttl" x="1460" y="124" text-anchor="middle" fill="var(--amber)">模，有了身体</text>
            <text class="sm" x="1460" y="230" text-anchor="middle" fill="var(--amber)">Physical AI · 在场即交互</text>
          </g>
        </svg>''' + COORD[_c1:]

# 工程问题 #4 → #5（robot26 idx25 · 敢商用）
PROB5 = rs[25]
PROB5 = PROB5.replace('工程问题 #4', '工程问题 #5').replace('ENGINEERING PROBLEM #4', 'ENGINEERING PROBLEM #5')

# ═ 总装（35 页） ═
S = [COVER, HOOK, ACT1, PANORAMA, READOUT, rs[6], MQ_HALVES,
     ACT2, rs[3], rs[5], DIVIDE, rs[9], rs[10], rs[12], rs[13],
     ACT3, COORD, PRES, HALF, rs[18], rs[17], VIDEO,
     ACT4, rs[22], rs[23], rs[24], EDGECLOUD, PROB5, rs[26],
     ACT5, BREAKTHROUGH, rs[29], rs[32], rs[34], FINALE]
assert len(S) == 35, len(S)

s = head + '\n'.join(S) + tail

# 金句编号按序重排
_mq = [0]
def _mqf(mm):
    _mq[0] += 1
    return 'MONEY QUOTE · 0%d' % _mq[0]
s = re.sub(r'(?i)Money Quote · 0\d', _mqf, s)

# 页码重排
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
assert len(_st) == 35
def _rn(mm):
    idx = sum(1 for t in _st if t <= mm.start())
    return mm.group(1) + str(idx) + mm.group(2)
s = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _rn, s)

open('public/decks/aiot26.html', 'w', encoding='utf-8').write(s)
print(f"aiot26.html · {len(_st)} 页 · {len(s)//1024}KB · 金句 {_mq[0]} 条")
assert 'deckRuler' in s and 'noindex' in s and 'data-dm' in s
print("ruler ✓ noindex ✓ media ✓")
