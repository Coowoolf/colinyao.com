#!/usr/bin/env python3
"""aiot26-v2 · 《AI 有了身体，为什么还是三天进抽屉？》—— 叙事重构版（26 页 · 默认浅底）。

  中心命题：AI 有了身体，不等于关系成立。Physical AI 的产品化，不是把语音、视觉和动作
  并排接上，而是让感知、记忆、判断和行动发生在同一条时间线上。

  底盘：public/decks/aiot26.html（V1 · 保留不动，只取样式 / deck 控制器 / deck-media / deckRuler）
  回收：V1 分水岭·半秒·噪声·端云·PRES 三块动效；cowork 定稿的 角色卡 / 共同历史 / 全景图
  新写：三乘数总图 / 临场闭环 / 两种延迟 / 北极星 / 链路 / 四方责任表 / 三个动作 / 收尾
  改造：默认 light（无 localStorage 时）· deck-swap 按钮隐藏（T 键仍可切）· 动效预算收紧
  场合：2026 AI 产品大会 · 声网 AIoT 专场 · 2026.08.09 北京 · 30 min。
"""
import re

V1 = open("public/decks/aiot26.html", encoding="utf-8").read()
C = open("public/decks/cowork.html", encoding="utf-8").read()
SEC = re.compile(r'<section class="slide[^"]*">.*?</section>', re.S)
v1s = SEC.findall(V1)
cs = SEC.findall(C)
assert len(v1s) == 35 and len(cs) == 62, (len(v1s), len(cs))

head = V1[:V1.index('<section class="slide')]
tail = V1[V1.rindex('</section>') + len('</section>'):]


def one(hay, old, new):
    assert hay.count(old) == 1, "锚点失效: " + old[:60]
    return hay.replace(old, new, 1)


def capi(sec, cap):
    """把回收素材里的 --i 阶梯压进预算（去掉超长 stagger 链）。"""
    return re.sub(r'--i:(\d+)', lambda m: '--i:%d' % min(int(m.group(1)), cap), sec)


# ═══════════════════════════════════════════════════════════════
# 一、底盘改造：默认浅底 + 标题 + V2 样式层
# ═══════════════════════════════════════════════════════════════
head = one(head, '<html lang="zh-CN" data-theme="dark">', '<html lang="zh-CN">')
head = one(head,
    "try{if(localStorage.getItem('colin-theme')==='light')document.documentElement.removeAttribute('data-theme')}catch(e){}",
    "try{if(localStorage.getItem('colin-theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}catch(e){}")
head = re.sub(r'<title>[^<]*</title>',
    '<title>AI 有了身体，为什么还是三天进抽屉？· 2026 AI 产品大会 AIoT 专场</title>', head, count=1)

V2_CSS = """
/* ═════════ aiot26-v2 层 ═════════
   ① 动效预算收紧：标题快落、整页自然落定，去掉超长 stagger
   ② 移植 cowork 组件：.tri 三栏脚注 / .badgecard 角色卡
   ③ 新组件：视频页 .vstage / 四方责任表 .quad / 来源行 .foot.src
   （颜色一律走既有 token，svg 一律包在 .fig / .prz 内） */
:root{--step:58ms;}
.ink{transition:-webkit-mask-position 1.0s var(--ease-flow) calc(var(--i,0)*var(--step)),
                mask-position 1.0s var(--ease-flow) calc(var(--i,0)*var(--step));}
.flow{transition:opacity .64s var(--ease-flow) calc(var(--i,0)*var(--step)),
                 transform .76s var(--ease-flow) calc(var(--i,0)*var(--step)),
                 filter .58s var(--ease-flow) calc(var(--i,0)*var(--step)),
                 clip-path .88s var(--ease-flow) calc(var(--i,0)*var(--step));}
.rise{transition:opacity .62s var(--ease-flow) calc(var(--i,0)*var(--step)),
                 transform .8s var(--ease-flow) calc(var(--i,0)*var(--step)),
                 clip-path .84s var(--ease-flow) calc(var(--i,0)*var(--step));}
.spread{transition:opacity .6s var(--ease-flow) calc(var(--i,0)*var(--step)),
                   transform .8s var(--ease-flow) calc(var(--i,0)*var(--step)),
                   clip-path .9s var(--ease-flow) calc(var(--i,0)*var(--step));}
.settle{transition:opacity .66s var(--ease) calc(var(--i,0)*var(--step)),
                   transform .88s var(--ease-flow) calc(var(--i,0)*var(--step)),
                   filter .66s var(--ease) calc(var(--i,0)*var(--step));}
.dw{transition:stroke-dashoffset 1.22s var(--ease-flow) calc(var(--i,0)*var(--step));}
.pop{transition:opacity .52s var(--ease) calc(var(--i,0)*var(--step)),
                transform .6s var(--ease) calc(var(--i,0)*var(--step));}

/* 封面 kicker 的第二行小字（锚定官方议程题） */
.cover .kicker .ag{display:block;margin-top:13px;font-size:15px;letter-spacing:.14em;
  color:var(--ink-3);text-transform:none;}
.cover .meta.q{gap:64px;}

/* 来源行：结论大，来源小 */
.foot.src{font-family:var(--f-mono);font-size:15px;letter-spacing:.06em;color:var(--ink-3);line-height:1.7;}

/* 移植 · cowork 三栏脚注 */
.tri{display:flex;gap:40px;align-items:flex-start;padding-top:24px;border-top:1px solid var(--hair);}
.tri .col{flex:1;display:flex;flex-direction:column;gap:10px;}
.tri .col .k{font-family:var(--f-mono);font-size:14px;letter-spacing:.16em;text-transform:uppercase;color:var(--amber);}
.tri .col .v{font-size:21px;line-height:1.56;color:var(--ink-2);font-weight:300;}

/* 移植 · cowork 角色卡 */
.badgecard{background:var(--card-bg-2);border:1px solid var(--hair);border-radius:6px;padding:28px 32px;
  display:flex;flex-direction:column;gap:17px;}
.badgecard .hd{display:flex;align-items:baseline;justify-content:space-between;
  border-bottom:1px solid var(--hair);padding-bottom:15px;}
.badgecard .hd .nm{font-size:31px;font-weight:900;color:var(--ink);}
.badgecard .hd .id{font-family:var(--f-mono);font-size:14px;letter-spacing:.16em;color:var(--ink-3);}
.badgecard .row{display:flex;gap:18px;align-items:baseline;}
.badgecard .row .k{font-family:var(--f-mono);font-size:14px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--amber);width:126px;flex:none;}
.badgecard .row .v{font-size:20px;line-height:1.5;color:var(--ink-2);font-weight:300;flex:1;}

/* 四方责任表：产品经理和 CEO 想截图带走的那一页 */
.quad{table-layout:fixed;}
.quad thead th{font-size:16px;padding:0 18px 14px 0;}
.quad thead th:first-child{width:132px;}
.quad tbody td{padding:20px 18px 20px 0;font-size:19px;line-height:1.52;white-space:normal;}
.quad tbody td:first-child{font-family:var(--f-mono);font-size:14px;letter-spacing:.12em;
  color:var(--ink-3);font-weight:400;text-transform:uppercase;}
.quad tbody td b{display:block;font-size:22px;font-weight:700;color:var(--ink);margin-bottom:7px;}
.quad tbody td.am b{color:var(--amber);}

/* 视频页：静态封面帧 · 播放前提示 · 播放后小结 · 抽帧兜底 */
.vstage{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:24px;padding:60px var(--pad-x);}
.vframe{position:relative;width:1280px;height:720px;background:#000;border:1px solid var(--hair);
  border-radius:6px;overflow:hidden;flex:none;}
.vframe video{width:100%;height:100%;object-fit:contain;background:#000;display:block;}
.vstills{position:absolute;inset:0;display:none;grid-template-columns:1fr 1fr 1fr;gap:2px;background:#000;}
.vstills img{width:100%;height:100%;object-fit:cover;display:block;}
.vstills .cap{position:absolute;left:0;right:0;bottom:0;padding:12px 18px;background:rgba(0,0,0,.55);
  font-family:var(--f-mono);font-size:14px;letter-spacing:.12em;color:#fffffe;}
.slide.dm-fail .vstills{display:grid;}
.vcue{font-size:27px;line-height:1.5;color:var(--ink-2);font-weight:300;text-align:center;
  transition:opacity .5s var(--ease);}
.vcue b{color:var(--ink);font-weight:700;}
.slide.dm-live .vcue{opacity:.22;}
.vsum{font-size:27px;line-height:1.5;color:var(--ink-2);font-weight:300;text-align:center;
  opacity:0;transition:opacity .7s var(--ease);}
.vsum b{color:var(--coral);font-weight:700;}
.slide.dm-done .vsum{opacity:1;}
"""
head = head[:head.rindex('</style>')] + V2_CSS + head[head.rindex('</style>'):]

# ═══════════════════════════════════════════════════════════════
# 二、舞台外 chrome：deck-swap 隐藏（保留 T 键切换）+ 视频页状态机
# ═══════════════════════════════════════════════════════════════
tail = one(tail, '.deck-swap{position:fixed;left:26px;bottom:22px;z-index:1000;',
                 '.deck-swap{display:none!important;position:fixed;left:26px;bottom:22px;z-index:1000;')
tail = one(tail, "  var cur='dark';\n  try{cur=localStorage.getItem('colin-theme')||'dark';}catch(e){}",
                 "  var cur='light';\n  try{cur=localStorage.getItem('colin-theme')||'light';}catch(e){}")

EXTRA_JS = '''<script>
/* V2 · 按钮隐藏后仍保留双主题切换：T 键 */
document.addEventListener('keydown',function(e){
  if(e.target&&e.target.getAttribute&&e.target.getAttribute('contenteditable'))return;
  if(e.key!=='t'&&e.key!=='T')return;
  var d=document.documentElement,dark=d.getAttribute('data-theme')==='dark',b=document.getElementById('deckSwap');
  if(dark){d.removeAttribute('data-theme');if(b)b.textContent='暗底';}
  else{d.setAttribute('data-theme','dark');if(b)b.textContent='浅底';}
  try{localStorage.setItem('colin-theme',dark?'light':'dark');}catch(err){}
});
/* V2 · 视频页状态机：播放中收起提示，播完亮出小结；失败（或 F 键）落到三帧静帧 */
(function(){
  function init(){
    var v=document.querySelector('video[data-dm]');
    if(!v){return setTimeout(init,150);}
    var sl=v.closest('.slide');
    function fail(){sl.classList.add('dm-fail');sl.classList.remove('dm-live');}
    v.addEventListener('play',function(){sl.classList.add('dm-live');});
    v.addEventListener('ended',function(){sl.classList.add('dm-done');sl.classList.remove('dm-live');});
    v.addEventListener('pause',function(){if(v.currentTime>1)sl.classList.add('dm-done');});
    v.addEventListener('error',fail,true);
    if(v.canPlayType&&v.canPlayType('video/mp4')===''){fail();}
    document.addEventListener('keydown',function(e){
      if(e.target&&e.target.getAttribute&&e.target.getAttribute('contenteditable'))return;
      if(e.key==='f'||e.key==='F'){sl.classList.toggle('dm-fail');sl.classList.add('dm-done');e.preventDefault();}
    });
  }
  init();
})();
</script>'''
tail = one(tail, '</body>', EXTRA_JS + '\n</body>')


# ═══════════════════════════════════════════════════════════════
# 三、26 页
# ═══════════════════════════════════════════════════════════════

P01 = '''<section class="slide">
  <div class="cover">
    <div class="kicker flow" style="--i:0">2026 AI 产品大会 · 声网 AIoT 专场<span class="ag">官方议程题 · AI 硬件多模态交互的产品化破局</span></div>
    <h1 class="ink" style="--i:1">AI 有了身体，<br>为什么还是三天进抽屉？</h1>
    <div class="subtitle spread" style="--i:2">多模态 AI 硬件，从能力堆叠到关系成立</div>
    <div class="meta q">
      <div class="rise" style="--i:3"><span class="k">讲者</span><span class="v">姚光华 Colin · 声网 AI 产品线负责人</span></div>
      <div class="rise" style="--i:4"><span class="k">日期</span><span class="v">2026.08.09 · 北京</span></div>
      <div class="rise" style="--i:5"><span class="k">时长</span><span class="v">30 min · 26 slides</span></div>
    </div>
  </div>
</section>'''

# ── P2 · 视觉高潮① 留存曲线 ──────────────────────────────────
P02 = '''<section class="slide">
  <div class="chrome"><span>冷开场 · THE DRAWER</span><span>02</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow coral flow" style="--i:0">先看一条几乎所有人都跑过的曲线</div>
      <h2 class="ink" style="--i:1">前三天什么都想让它试一遍，第四天它进了抽屉</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 620" width="1680" aria-hidden="true">
          <text class="lbl pop" style="--i:2" x="0" y="22">纵轴 · 今天还会主动把它打开的人</text>
          <path class="dw" style="--len:1580;--i:2" d="M60 520 H1640" stroke="var(--hair)" stroke-width="1" fill="none"/>
          <path class="pop" style="--i:4" fill="var(--amber)" fill-opacity=".13" stroke="none"
                d="M110 62 C 300 78, 400 200, 620 262 C 810 316, 940 380, 1080 414 C 1250 454, 1400 478, 1560 486 L1560 520 L110 520 Z"/>
          <path class="stroke-am dw" style="--len:1160;--i:3" stroke-width="3.4" fill="none"
                d="M110 62 C 300 78, 400 200, 620 262 C 810 316, 940 380, 1080 414"/>
          <path class="stroke-co dw" style="--len:520;--i:4" stroke-width="3.4" fill="none"
                d="M1080 414 C 1250 454, 1400 478, 1560 486"/>
          <g class="pop" style="--i:3" stroke="var(--hair)" stroke-width="1" stroke-dasharray="4 7">
            <path d="M110 62 V520"/><path d="M620 262 V520"/><path d="M1080 414 V520"/>
          </g>
          <path class="stroke-co pop" style="--i:4" stroke-width="1.4" stroke-dasharray="4 7" d="M1560 486 V520"/>
          <circle class="fill-am pop" style="--i:3" cx="110" cy="62" r="9"/>
          <circle class="fill-ink pop" style="--i:3" cx="620" cy="262" r="8"/>
          <circle class="fill-ink pop" style="--i:4" cx="1080" cy="414" r="8"/>
          <circle class="fill-co pop" style="--i:4" cx="1560" cy="486" r="12"/>
          <g class="pop" style="--i:3">
            <text class="lbl" x="140" y="558" text-anchor="middle">DAY 1 · 开箱</text>
            <text class="ttl" x="140" y="596" text-anchor="middle">什么都想让它试一遍</text>
          </g>
          <g class="pop" style="--i:4">
            <text class="lbl" x="640" y="558" text-anchor="middle">DAY 2 · 复述</text>
            <text class="ttl" x="640" y="596" text-anchor="middle">同一个问题，它不记得你问过</text>
          </g>
          <g class="pop" style="--i:4">
            <text class="lbl" x="1080" y="558" text-anchor="middle">DAY 3 · 空转</text>
            <text class="ttl" x="1080" y="596" text-anchor="middle">不知道还能跟它说什么</text>
          </g>
          <g class="pop" style="--i:5">
            <text class="lbl fill-co" x="1520" y="558" text-anchor="middle">第 4 天 · 进抽屉</text>
            <text class="ttl fill-co" x="1520" y="596" text-anchor="middle">没有故障，只是再没想起它</text>
          </g>
        </svg>
      </div>
      <div class="note co"><span class="flow" style="--i:5">它没有坏，也没有惹你，甚至一直很有礼貌。<b>它只是没有变成一个你会主动想起的存在。</b>这条曲线，就是今天这 30 分钟要回答的唯一问题。</span></div>
    </div>
  </div>
</section>'''

# ── P3 · 证据视频（封面帧 / 提示 / 小结 / 抽帧兜底）─────────────
P03 = '''<section class="slide">
  <div class="chrome"><span>证据 · THE DEMO</span><span>03</span></div>
  <div class="vstage">
    <div class="vcue flow" style="--i:0">接下来只看三件事：<b>它看见了什么</b> · <b>它想起了什么</b> · <b>它什么时候开口</b></div>
    <div class="vframe rise" style="--i:1">
      <video data-dm src="/media/cowork/gemini-demo.mp4" poster="/media/aiot26/still-1.jpg" preload="auto" playsinline></video>
      <div class="vstills">
        <img src="/media/aiot26/still-1.jpg" alt="">
        <img src="/media/aiot26/still-2.jpg" alt="">
        <img src="/media/aiot26/still-3.jpg" alt="">
        <div class="cap">静帧备用 · 现场视频不可用时按 F 切换 · 桌面机器人 × 对话式 AI 实拍</div>
      </div>
    </div>
    <div class="vsum">它证明了：<b>会说话，已经不稀缺。</b>它没有证明的是：<b>关系成立。</b></div>
    <div class="dm-ind" aria-hidden="true"></div>
  </div>
</section>'''

# ── P4 · 第一判断 ─────────────────────────────────────────────
P04 = '''<section class="slide">
  <div class="chrome"><span>第一判断 · BODY IS NOT A BOND</span><span>04</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">2026 · Physical AI 从技术分支，进入大众产品叙事</div>
      <h2 class="ink" style="--i:1">身体不等于伙伴：能力出现，不等于关系成立</h2>
    </div>
    <div class="body">
      <div class="duo">
        <div class="flow" style="--i:2">
          <div class="h">今年确实发生了 · 能力侧</div>
          <div class="b">世界模型与端侧 VLA，同时向消费硬件下沉</div>
          <div class="s">NVIDIA 发布新一代 Cosmos 3 世界模型；Google DeepMind 发布可在机器人本体上离线运行的 Gemini Robotics On-Device。看见和动起来的门槛，这一年是真的降下来了。</div>
        </div>
        <div class="flow rev" style="--i:3">
          <div class="h">今年没有发生 · 关系侧</div>
          <div class="b">上一页那条曲线的形状，一天也没变</div>
          <div class="s">我们反复看到：能力清单越来越长，第四天的那个抽屉还在原地。能力是可以采购的，关系不是——它只能被设计出来。</div>
        </div>
      </div>
      <div class="land flow" style="--i:4">今天全场只讲一句话：<b>AI 有了身体，不等于关系成立。</b><span class="s">Physical AI 的产品化，不是把语音、视觉和动作并排接上，而是让感知、记忆、判断和行动，发生在同一条时间线上。</span></div>
      <div class="foot src flow" style="--i:5">来源 · NVIDIA newsroom（Cosmos 3 世界模型）· Google DeepMind blog（Gemini Robotics On-Device）</div>
    </div>
  </div>
</section>'''

# ── P5 · 两种价值逻辑 ─────────────────────────────────────────
P05 = '''<section class="slide">
  <div class="chrome"><span>两种价值逻辑 · TWO LOGICS</span><span>05</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">同一批技术，两套完全不同的评价体系</div>
      <h2 class="ink" style="--i:1">任务价值型，和关系价值型</h2>
    </div>
    <div class="body">
      <div class="g2">
        <div class="card rise" style="--i:2">
          <div class="tag">LOGIC A · 任务价值型</div>
          <div class="t">它替我，把一件事做完了吗</div>
          <div class="d">扫地机、点货机器人、导览终端、工业巡检——用户买的是一个确定的结果，交互只是达成结果的路径。</div>
          <div class="d"><b>它的三把尺子：</b>任务成功率 × 单位时间吞吐 × 安全与合规。</div>
        </div>
        <div class="card on rise" style="--i:3">
          <div class="tag">LOGIC B · 关系价值型</div>
          <div class="t">明天，我还想不想找它</div>
          <div class="d">陪伴机器人、AI 玩具、桌面伙伴、可穿戴助理——用户买的是一段会延续下去的关系，交互本身就是产品。</div>
          <div class="d"><b>它的三把尺子：</b>回访意愿 × 关系连续性 × 信任。</div>
        </div>
      </div>
      <div class="note flow" style="--i:4">市场信号：CES 2026 上，数十家中国 AI 玩具与陪伴硬件品牌集中出现；资本市场也开始用潮玩与 IP 消费的逻辑，来理解 AI 陪伴硬件。<b>关系价值型不是一个概念，它已经是一门生意。</b></div>
      <div class="land flow" style="--i:5">这两套体系没有高下之分，也不比谁更赚钱。<span class="s">真正的错误只有一个：拿其中一把尺子，去量另一类产品——陪伴类硬件的问题，通常不是任务做得不够好，是它一直在被任务尺子考核。</span></div>
      <div class="foot src flow" style="--i:5">口径 · CES 2026 公开报道综合（各家统计口径不一，此处不取单一数字）</div>
    </div>
  </div>
</section>'''

# ── P6 · 分界线（V1 分水岭升级）────────────────────────────────
P06 = '''<section class="slide">
  <div class="chrome"><span>分界线 · THE REAL DIVIDE</span><span>06</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">把同一颗模型，装进两家不同的产品</div>
      <h2 class="ink" style="--i:1">同一个模型下，拉开体验的是角色，不是 IQ</h2>
    </div>
    <div class="body">
      <div class="fig">
        <svg viewBox="0 0 1680 336" width="1680" fill="none">
          <text class="lbl pop" style="--i:2" x="0" y="20">纵轴 · 用户明天还想不想再打开它</text>
          <path class="stroke dw" style="--len:840;--i:2" stroke-width="2.4" d="M40 250 C 320 250, 560 180, 840 150"/>
          <g class="pop" style="--i:3"><text class="ttl" x="240" y="150" text-anchor="middle" style="font-size:32px">更聪明</text></g>
          <text class="txt pop" style="--i:3" x="240" y="186" text-anchor="middle">这一段，更强的模型确实更好</text>
          <path class="stroke-co pop" style="--i:3" stroke-width="1.4" stroke-dasharray="6 8" d="M840 30 V296"/>
          <text class="lbl fill-co pop" style="--i:3" x="840" y="320" text-anchor="middle">分界线 · THE DIVIDE</text>
          <circle class="fill-am pop" style="--i:4" cx="840" cy="150" r="9"/>
          <circle class="fill-ink pop" style="--i:4" cx="1005" cy="102" r="9"/>
          <text class="lbl fill-co pop" style="--i:5" x="1005" y="238" text-anchor="middle">我们反复看到：绝大多数产品，卡在这一格</text>
          <circle class="stroke-co pop" style="--i:5" cx="1005" cy="102" r="18" stroke-width="2"/>
          <path class="stroke-am dw" style="--len:560;--i:4" stroke-width="3" d="M840 150 C 1060 120, 1180 76, 1360 62"/>
          <g class="pop" style="--i:5">
            <path class="stroke-am pkt" stroke-width="4"
              style="--pl:60px;--p0:60px;--p1:-560px;--pt:5.6s;--pd:1.6s"
              d="M840 150 C 1060 120, 1180 76, 1360 62"/>
          </g>
          <g class="pop" style="--i:5"><text class="ttl fill-am" x="1400" y="56" style="font-size:32px">伙伴</text></g>
          <text class="txt pop" style="--i:5" x="1400" y="92">改用角色打分</text>
          <path class="stroke-co dw" style="--len:560;--i:4" stroke-width="2.4" d="M840 150 C 1060 180, 1180 240, 1360 258"/>
          <g class="pop" style="--i:5"><text class="ttl fill-co" x="1400" y="252" style="font-size:32px">更贵的玩具</text></g>
          <text class="txt pop" style="--i:5" x="1400" y="288">还在用能力打分</text>
          <text class="lbl pop" style="--i:5" x="0" y="326">横轴 · 模型能力一路在涨 →</text>
        </svg>
      </div>
      <div class="duo">
        <div class="flow" style="--i:5">
          <div class="h">拉不开差距的 · 能力尺</div>
          <div class="b">答对率、响应速度、知识覆盖</div>
          <div class="s">这些指标全部提升，用户照样在第四天把它收起来。因为它们回答的是「它行不行」。</div>
        </div>
        <div class="flow rev" style="--i:5">
          <div class="h">真正拉开差距的 · 角色尺</div>
          <div class="b">它是谁、它记不记得、它什么时候开口</div>
          <div class="s">这三件事只要有一件没定义，再强的模型也只是一个更贵的玩具。</div>
        </div>
      </div>
    </div>
  </div>
</section>'''

# ── P7 · 视觉高潮② 三乘数总图 ─────────────────────────────────
P07 = '''<section class="slide">
  <div class="chrome"><span>核心框架 · THE THREE MULTIPLIERS</span><span>07</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">今天唯一需要你记住的那张图</div>
      <h2 class="ink" style="--i:1">伙伴感 = 角色一致性 × 共同历史 × 可控临场</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 520" width="1680" aria-hidden="true">
          <g class="pop" style="--i:2">
            <rect class="box" x="0" y="26" width="500" height="252" rx="6" stroke-width="1"/>
            <text class="lbl" x="34" y="80">MULTIPLIER 01 · ROLE</text>
            <text class="fill-ink" x="34" y="152" style="font-size:44px;font-weight:900">角色一致性</text>
            <text class="txt" x="34" y="200">三个月后重放一段对话，</text>
            <text class="txt" x="34" y="232">用户还认得出这是同一个「它」</text>
            <text class="lbl fill-am" x="34" y="266">落地形态 · 可版本化的角色卡</text>
          </g>
          <g class="pop" style="--i:3"><text class="fill-am" x="545" y="166" text-anchor="middle" style="font-size:48px;font-weight:900">×</text></g>
          <g class="pop" style="--i:3">
            <rect class="box" x="590" y="26" width="500" height="252" rx="6" stroke-width="1"/>
            <text class="lbl" x="624" y="80">MULTIPLIER 02 · HISTORY</text>
            <text class="fill-ink" x="624" y="152" style="font-size:44px;font-weight:900">共同历史</text>
            <text class="txt" x="624" y="200">它记得的不是聊天记录，</text>
            <text class="txt" x="624" y="232">是你们一起经历过的那些事</text>
            <text class="lbl fill-am" x="624" y="266">落地形态 · 关系账本</text>
          </g>
          <g class="pop" style="--i:4"><text class="fill-am" x="1135" y="166" text-anchor="middle" style="font-size:48px;font-weight:900">×</text></g>
          <g class="pop" style="--i:4">
            <rect class="box" x="1180" y="26" width="500" height="252" rx="6" stroke-width="1"/>
            <text class="lbl" x="1214" y="80">MULTIPLIER 03 · PRESENCE</text>
            <text class="fill-ink" x="1214" y="152" style="font-size:44px;font-weight:900">可控临场</text>
            <text class="txt" x="1214" y="200">它在该开口的那一刻开口，</text>
            <text class="txt" x="1214" y="232">做错了还回得来</text>
            <text class="lbl fill-am" x="1214" y="266">落地形态 · 实时引擎</text>
          </g>
          <path class="stroke-am dw" style="--len:52;--i:5" stroke-width="2.4" d="M840 278 V330"/>
          <g class="pop" style="--i:5">
            <rect x="380" y="330" width="920" height="92" rx="6" fill="none" stroke="var(--amber)" stroke-width="2"/>
            <text class="fill-am" x="840" y="388" text-anchor="middle" style="font-size:36px;font-weight:900">伙伴感 · 用户明天还想再打开它</text>
          </g>
          <g class="pop" style="--i:6" data-step="1">
            <path d="M0 458 H1680" stroke="var(--hair)" stroke-width="1" stroke-dasharray="4 7"/>
            <text class="fill-co" x="0" y="506" style="font-size:31px;font-weight:900">任何一项接近零 —— 得到的都只是一个更昂贵、更聪明的玩具。</text>
          </g>
        </svg>
      </div>
      <div class="note flow" style="--i:6">这是乘法，不是加法：三项里只要有一项接近零，前面所有的能力都乘不出关系。<b>接下来三页，一项一项拆。</b></div>
    </div>
  </div>
</section>'''

# ── P8 · 乘数一 角色一致性 ────────────────────────────────────
P08 = '''<section class="slide">
  <div class="chrome"><span>乘数一 · ROLE CONSISTENCY</span><span>08</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">乘数一 · 角色一致性</div>
      <h2 class="ink" style="--i:1">角色不是起个名字，也不是一段 system prompt，是一套稳定的判断方式</h2>
    </div>
    <div class="body g2 gfill">
      <div class="badgecard rise" style="--i:2">
        <div class="hd"><div class="nm">角色卡 · Persona Card</div><div class="id">v3.2 · 设计样例</div></div>
        <div class="row"><div class="k">语调</div><div class="v">短句为主，不用感叹号，很少说「我理解你的感受」</div></div>
        <div class="row"><div class="k">判断方式</div><div class="v">你不高兴时先安静两秒，再问一件具体的事——不给结论</div></div>
        <div class="row"><div class="k">喜恶</div><div class="v">讨厌被叫「助手」；喜欢下雨天；对「加油」这个词过敏</div></div>
        <div class="row"><div class="k">边界</div><div class="v">不劝分不劝和，不给医疗建议，不假装自己是人</div></div>
        <div class="row"><div class="k">回归集</div><div class="v">一组人格锚点用例，每次发版必跑，通过率不达标不上线</div></div>
      </div>
      <div class="mid">
        <div class="note flow" style="--i:3"><b>一句话定义不了角色。</b>「你是一个温柔的陪伴机器人」——换一个模型，这句话的效果就全变了。角色必须是<b>可测的、可回归的、可版本化的</b>。</div>
        <div class="note co flow" style="--i:4"><b>角色漂移是线上事故，不是调优问题。</b>所以角色卡要有版本号、要有 diff、要进发版流程：改角色和改支付逻辑，走同一条评审通道。</div>
        <div class="note flow" style="--i:5"><b>验收标准只有一条：</b>把三个月前的一段对话拿出来重放，用户能不能认出，这还是同一个「它」。</div>
        <div class="foot src flow" style="--i:5">卡面为设计样例，非任何在售产品的真实配置</div>
      </div>
    </div>
  </div>
</section>'''

# ── P9 · 乘数二 共同历史 ──────────────────────────────────────
P09 = '''<section class="slide">
  <div class="chrome"><span>乘数二 · SHARED HISTORY</span><span>09</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">乘数二 · 共同历史</div>
      <h2 class="ink" style="--i:1">关系，是从<em>共同历史</em>里长出来的</h2>
    </div>
    <div class="body">
      <div class="fig flow" style="--i:2">
        <svg viewBox="0 0 1680 372" width="1680" height="372">
          <path class="dw" style="--len:1520;--i:2" d="M120 312 H1620" stroke="var(--hair)" stroke-width="1" fill="none"/>
          <path class="dw" style="--len:280;--i:2" d="M120 40 V312" stroke="var(--hair)" stroke-width="1" fill="none"/>
          <path class="dw" style="--len:1480;--i:3" d="M120 70 H1600" stroke="var(--coral)" stroke-width="1.5" stroke-dasharray="6 10" fill="none"/>
          <text class="lbl fill-co pop" style="--i:3" x="1600" y="54" text-anchor="end">0.29 TB · 思想实验的边界</text>
          <path class="dw" style="--len:1800;--i:4" d="M130 302 C 430 296, 630 200, 880 128 S 1300 80, 1580 74" stroke="var(--amber)" stroke-width="3" fill="none"/>
          <g class="pop" style="--i:4">
            <circle cx="320" cy="296" r="7" class="fill-ink"/>
            <text class="txt" x="320" y="274" text-anchor="middle">陌生人</text>
            <text class="sm" x="320" y="346" text-anchor="middle">「你叫醒我」—— 一次性指令</text>
          </g>
          <g class="pop" style="--i:5">
            <circle cx="860" cy="140" r="7" class="fill-ink"/>
            <text class="txt" x="860" y="118" text-anchor="middle">熟人</text>
            <text class="sm" x="860" y="346" text-anchor="middle">记得几个偏好，会主动问一句</text>
          </g>
          <g class="pop" style="--i:5">
            <circle cx="1380" cy="78" r="9" class="fill-am"/>
            <text class="txt" x="1380" y="120" text-anchor="middle" fill="var(--amber)">伙伴</text>
            <text class="sm" x="1380" y="346" text-anchor="middle" fill="var(--amber)">一年后，它还接得住去年那件事</text>
          </g>
          <text class="lbl pop" style="--i:5" x="120" y="30">关系深度</text>
          <text class="lbl pop" style="--i:5" x="1620" y="340" text-anchor="end">共同经历 →</text>
        </svg>
      </div>
      <div class="note flow" style="--i:5">0.29 TB，是我做过的一个思想实验：把一个人一生中值得被记住的相处<b>全部存下来</b>，大概是这个量级。它不是任何产品的容量指标，只是用来说明一件事——存得下，从来不是难点。</div>
      <div class="land flow" style="--i:5">真正的问题不是记住一切，<b>而是此刻应该想起什么。</b><span class="s">落地形态 = 关系账本：事实 / 偏好 / 事件 / 边界四类分开存，四类的读写权限和召回策略都不一样。</span></div>
      <div class="foot src flow" style="--i:5">来源 · Colin《我们的一生只有 0.29TB》思想实验，非产品参数</div>
    </div>
  </div>
</section>'''

# ── P10 · 乘数三 可控临场 · 闭环 ──────────────────────────────
P10 = '''<section class="slide">
  <div class="chrome"><span>乘数三 · THE PRESENCE LOOP</span><span>10</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">乘数三 · 可控临场</div>
      <h2 class="ink" style="--i:1">感知 → 召回 → 判断 → 行动 → 新的感知，共享同一条时间线</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 372" width="1680" aria-hidden="true">
          <path class="dw" style="--len:1400;--i:2" d="M120 150 H1560" stroke="var(--hair)" stroke-width="1.4" fill="none"/>
          <path class="stroke-am dw" style="--len:1440;--i:3" stroke-width="2.4" fill="none" d="M120 150 H1560"/>
          <path class="stroke-am dw" style="--len:1900;--i:4" stroke-width="2" fill="none" stroke-dasharray="7 9"
                d="M1560 150 C 1660 150, 1670 300, 1500 300 H180 C 20 300, 20 150, 120 150"/>
          <g class="pop" style="--i:5">
            <path class="stroke-am pkt" stroke-width="4.5" fill="none"
              style="--pl:70px;--p0:70px;--p1:-1440px;--pt:5.4s;--pd:1.2s" d="M120 150 H1560"/>
          </g>
          <text class="lbl fill-am pop" style="--i:5" x="840" y="332" text-anchor="middle">同一条时间线 · 上一次行动，就是下一轮的输入</text>
          <g class="pop" style="--i:3">
            <circle cx="120" cy="150" r="12" class="fill-am"/>
            <text class="ttl" x="120" y="106" text-anchor="middle" style="font-size:30px">感知</text>
            <text class="sm" x="120" y="200" text-anchor="middle" style="font-size:19px">麦克风、摄像头、</text>
            <text class="sm" x="120" y="226" text-anchor="middle" style="font-size:19px">传感器一直醒着</text>
          </g>
          <g class="pop" style="--i:4">
            <circle cx="480" cy="150" r="12" class="fill-am"/>
            <text class="ttl" x="480" y="106" text-anchor="middle" style="font-size:30px">召回</text>
            <text class="sm" x="480" y="200" text-anchor="middle" style="font-size:19px">此刻该想起</text>
            <text class="sm" x="480" y="226" text-anchor="middle" style="font-size:19px">哪一条历史</text>
          </g>
          <g class="pop" style="--i:4">
            <circle cx="840" cy="150" r="12" class="fill-am"/>
            <text class="ttl" x="840" y="106" text-anchor="middle" style="font-size:30px">判断</text>
            <text class="sm" x="840" y="200" text-anchor="middle" style="font-size:19px">要不要开口、</text>
            <text class="sm" x="840" y="226" text-anchor="middle" style="font-size:19px">说什么、什么时候</text>
          </g>
          <g class="pop" style="--i:5">
            <circle cx="1200" cy="150" r="12" class="fill-am"/>
            <text class="ttl" x="1200" y="106" text-anchor="middle" style="font-size:30px">行动</text>
            <text class="sm" x="1200" y="200" text-anchor="middle" style="font-size:19px">语音和动作</text>
            <text class="sm" x="1200" y="226" text-anchor="middle" style="font-size:19px">同时发出去</text>
          </g>
          <g class="pop" style="--i:5">
            <circle cx="1560" cy="150" r="14" class="fill-co"/>
            <text class="ttl fill-co" x="1560" y="106" text-anchor="middle" style="font-size:30px">新的感知</text>
            <text class="sm" x="1560" y="200" text-anchor="middle" style="font-size:19px">它刚做的事，</text>
            <text class="sm" x="1560" y="226" text-anchor="middle" style="font-size:19px">立刻改变了现场</text>
          </g>
        </svg>
      </div>
      <div class="note flow" style="--i:5">把这个环拆开，就是四个可以分别排期的工程量：<b>临场 = 实时感知 × 即时召回 × 合时回应 × 可恢复行动。</b>四项里少任何一项，环就断在那里。</div>
      <div class="land flow" style="--i:5">落地形态 = 实时引擎。<span class="s">它不生产内容，它决定内容什么时候、以什么顺序发生——三个乘数到这里合上：角色卡 × 关系账本 × 实时引擎，就是「三份产品资产 × 一个实时引擎」在硬件上的样子。</span></div>
    </div>
  </div>
</section>'''

# ── P11 · 身体的意义 ──────────────────────────────────────────
P11 = '''<section class="slide">
  <div class="chrome"><span>身体的意义 · CONSEQUENCE</span><span>11</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">为什么有身体，这件事真的不一样</div>
      <h2 class="ink" style="--i:1">身体让一次回答，变成一次会产生后果的行动</h2>
    </div>
    <div class="body">
      <div class="duo">
        <div class="flow" style="--i:2">
          <div class="h">在屏幕上 · A REPLY</div>
          <div class="b">一次回答</div>
          <div class="s">答错了可以重问一次，代价是几秒钟的尴尬。上一句话还留在屏幕上，随时可以往回翻。</div>
        </div>
        <div class="flow rev" style="--i:3">
          <div class="h">有了身体 · AN ACTION</div>
          <div class="b">一次行动</div>
          <div class="s">它已经转过头、已经伸出手、已经在客厅里说出了那句话。代价是信任，有时候是安全。</div>
        </div>
      </div>
      <div class="rows">
        <div class="r flow" style="--i:4"><span class="n">01</span><span class="k">不可撤回</span><span class="v">语音和动作都没有撤回键——发出去的那一刻，就是既成事实。</span></div>
        <div class="r flow" style="--i:4"><span class="n">02</span><span class="k">有物理后果</span><span class="v">一次误判，可能是碰倒一个杯子，也可能是在不该说话的时候开了口。</span></div>
        <div class="r flow" style="--i:5"><span class="n">03</span><span class="k">有旁观者</span><span class="v">屋里通常还有别人。它的每一次行动，都是公开发生的。</span></div>
      </div>
      <div class="land flow" style="--i:5">所以从这一页开始，<b>安全与恢复不再是工程指标，而是产品设计问题。</b></div>
    </div>
  </div>
</section>'''

# ── P12 · 视觉高潮③ 上 · 恰好的半秒（V1 强页保留升级）──────────
P12 = '''<section class="slide">
  <div class="chrome"><span>恰好的那半秒 · THE RIGHT HALF-SECOND</span><span>12</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">先看一个反直觉的现象</div>
      <h2 class="ink" style="--i:1">恰好的那半秒，比快半秒值钱</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 310" width="1680" aria-hidden="true">
          <path class="stroke-co pop" style="--i:2" stroke-width="1.2" stroke-dasharray="5 7" d="M700 46 V286"/>
          <text class="lbl pop" style="--i:2" x="700" y="30" text-anchor="middle">用户说完：「最近压力好大。」</text>
          <text class="lbl fill-co pop" style="--i:3" x="0" y="76">A · 零延迟接话</text>
          <path class="stroke dw" style="--len:640;--i:3" stroke-width="13" stroke-linecap="round" d="M60 118 H700" opacity=".34"/>
          <path class="stroke-co dw" style="--len:480;--i:4" stroke-width="13" stroke-linecap="round" d="M700 118 H1180"/>
          <text class="txt pop" style="--i:4" x="1220" y="126">听起来像抢答</text>
          <text class="lbl fill-am pop" style="--i:4" x="0" y="212">B · 停半秒再接</text>
          <path class="stroke dw" style="--len:640;--i:4" stroke-width="13" stroke-linecap="round" d="M60 254 H700" opacity=".34"/>
          <path class="stroke-am pop" style="--i:5" stroke-width="1.6" stroke-dasharray="5 7" d="M700 254 H860"/>
          <path class="stroke-am dw" style="--len:480;--i:5" stroke-width="13" stroke-linecap="round" d="M860 254 H1340"/>
          <text class="lbl fill-am pop" style="--i:5" x="780" y="232" text-anchor="middle">+500ms</text>
          <text class="txt pop" style="--i:5" x="1380" y="262">听起来像在想你的事</text>
        </svg>
      </div>
      <div class="quotes">
        <div class="r flow" style="--i:5"><div class="who">A · 零延迟</div><div class="say">「您可以尝试以下减压方法：深呼吸、散步、听音乐、找朋友聊聊……」</div><div class="src">信息正确 · 节奏机械 · 情绪缺席 —— 它在回答问题，没在听人</div></div>
        <div class="r flow rev" style="--i:5"><div class="who">B · +0.5 秒</div><div class="say">「听起来挺累的，今天发生什么了吗？」</div><div class="src">节奏对了 · 语气对了 —— 那半秒的停顿，本身就是「我在想你的事」</div></div>
      </div>
      <div class="note"><span class="flow" style="--i:5">工程直觉是「延迟越低越好」。产品事实是：<b>0 毫秒的接话，反而让人觉得自己没被听见</b>——因为真人不会在你话音落地的同一帧开口。</span></div>
    </div>
  </div>
</section>'''

# ── P13 · 视觉高潮③ 下 · 两种延迟（修 V1 自相矛盾）─────────────
P13 = '''<section class="slide">
  <div class="chrome"><span>两种延迟 · TWO CLOCKS</span><span>13</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">上一页那半秒，其实是两个不同的量</div>
      <h2 class="ink" style="--i:1">系统延迟要消失，表达停顿要被设计</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 344" width="1680" aria-hidden="true">
          <path class="stroke-co pop" style="--i:2" stroke-width="1.2" stroke-dasharray="5 7" d="M560 42 V176"/>
          <text class="lbl pop" style="--i:2" x="560" y="30" text-anchor="middle">话音落地 · END OF SPEECH</text>
          <path class="stroke dw" style="--len:500;--i:2" stroke-width="26" stroke-linecap="round" d="M60 116 H560" opacity=".3"/>
          <text class="lbl pop" style="--i:2" x="70" y="80">用户在说</text>
          <path class="stroke-am dw" style="--len:300;--i:3" stroke-width="26" stroke-linecap="round" d="M560 116 H860"/>
          <text class="lbl fill-am pop" style="--i:3" x="710" y="80" text-anchor="middle">系统延迟</text>
          <path class="stroke-co dw" style="--len:320;--i:4" stroke-width="26" stroke-linecap="round" d="M880 116 H1200"/>
          <text class="lbl fill-co pop" style="--i:4" x="1040" y="80" text-anchor="middle">表达停顿</text>
          <circle class="fill-ink pop" style="--i:5" cx="1220" cy="116" r="10"/>
          <text class="txt pop" style="--i:5" x="1250" y="124">第一声有意义的回应</text>
          <path d="M0 214 H1680" stroke="var(--hair)" stroke-width="1"/>
          <text class="lbl fill-am pop" style="--i:5" x="0" y="256">系统延迟 · SYSTEM LATENCY</text>
          <text class="txt pop" style="--i:5" x="420" y="256">从话音落地，到第一声有意义的回应。<tspan class="fill-ink" style="font-weight:700">越低越稳越好，目标是让人根本察觉不到它。</tspan></text>
          <path d="M0 288 H1680" stroke="var(--hair-soft)" stroke-width="1"/>
          <text class="lbl fill-co pop" style="--i:5" x="0" y="330">表达停顿 · EXPRESSIVE PAUSE</text>
          <text class="txt pop" style="--i:5" x="420" y="330">它决定「什么时候开口」。<tspan class="fill-ink" style="font-weight:700">这是有意设计的沉默，有目标区间，不是越短越好。</tspan></text>
        </svg>
      </div>
      <div class="note co flow" style="--i:5">所以「每多 200 毫秒都在消耗伙伴感」和「停半秒更像在想你的事」不矛盾——它们说的根本不是同一个量：<b>前一句说的是系统延迟，后一句说的是表达停顿。</b>把两者混成一个指标，就会一边压延迟，一边把角色压没。</div>
      <div class="land flow" style="--i:5">快，是基础设施问题；<b>什么时候开口，是产品问题。</b></div>
    </div>
  </div>
</section>'''

# ── P14 · 北极星 ──────────────────────────────────────────────
P14 = '''<section class="slide">
  <div class="chrome"><span>北极星 · THE NORTH STAR</span><span>14</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">既然要压，先把它定义清楚</div>
      <h2 class="ink" style="--i:1">北极星只有一条：从用户说完，到第一声有意义的回应</h2>
    </div>
    <div class="body">
      <div class="g-38 gfill">
        <div class="mid">
          <div class="stat flow" style="--i:2">
            <div class="v">P90</div>
            <div class="l">端到端 · 从话音落地，到第一声有意义的回应</div>
            <div class="u">END OF SPEECH → FIRST MEANINGFUL AUDIO</div>
          </div>
          <div class="note flow" style="--i:3">不取平均值。<b>伙伴感是被最差的那几次打碎的</b>，不是被平均值打碎的。</div>
        </div>
        <div class="mid">
          <div class="rows">
            <div class="r flow" style="--i:3"><span class="n">01</span><span class="k">口径</span><span class="v">只认这条链路的两端。不是首包、不是模型首 token、不是 TTS 首帧——那三个都是中间量。</span></div>
            <div class="r flow" style="--i:4"><span class="n">02</span><span class="k">归因</span><span class="v">这一条必须能拆开：拾音 / 路由 / 检索 / 模型 / 合成 / 网络，每一段都要能单独看见。</span></div>
            <div class="r flow" style="--i:4"><span class="n">03</span><span class="k">取值</span><span class="v">把 P90 压进 1 秒这条对话的心理边界之内（内部口径 · 设计样例），再在边界内谈表达停顿。</span></div>
          </div>
          <div class="note flow" style="--i:5">公开拆解口径：1 秒是对话的心理边界；一次 +500 毫秒的改动，被创始人形容为一场「灾难」；后来在架构层把语音启动时间缩短了 0.7 秒以上。</div>
          <div class="foot src flow" style="--i:5">来源 · Colin《我从 Tolan 身上，看清了 Voice Agent 的 4 个反直觉真相》公开拆解口径</div>
        </div>
      </div>
    </div>
  </div>
</section>'''

# ── P15 · 噪声与选择性注意 ────────────────────────────────────
P15 = '''<section class="slide">
  <div class="chrome"><span>选择性注意 · WHO IS TALKING TO ME</span><span>15</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow coral flow" style="--i:0">把设备放进真实的客厅、教室和车里</div>
      <h2 class="ink" style="--i:1">难点不是听见所有声音，是知道谁在和我说话</h2>
    </div>
    <div class="body">
      <div class="note flow" style="--i:2">「嘈杂环境」不是一个问题，是三个难度完全不同的问题。把它们混在一起谈，就会得到一个永远调不完的需求。</div>
      <div class="rows">
        <div class="r flow" style="--i:3"><span class="n">01</span><span class="k">稳态背景噪声</span><span class="v">STATIONARY · 空调、风扇、路噪、机械持续运行 —— 相对成熟，工程上已有稳定手段。</span></div>
        <div class="r flow" style="--i:4"><span class="n">02</span><span class="k">瞬态突发</span><span class="v">TRANSIENT · 关门、犬吠、碰撞、掉落 —— 部分可控，代价通常是牺牲一点响应速度。</span></div>
        <div class="r flow hot" style="--i:4"><span class="n">03</span><span class="k">非目标人声与多人重叠</span><span class="v">NON-TARGET SPEECH · 电视里的人声、家人在旁边聊天、几个人同时说话 —— 仍然最难。</span></div>
      </div>
      <div class="land flow" style="--i:5">前两类是信号问题，第三类是<b>产品判断问题</b>：谁是此刻的说话人，其余的都按背景处理。<span class="s">选择性注意不是一个降噪档位，它是一个需要产品来定义的策略——在孩子的房间里和在客服台前，答案并不一样。</span></div>
    </div>
  </div>
</section>'''

# ── P16 · 多模态时序（V1 PRES 动效重构）───────────────────────
P16 = '''<section class="slide">
  <div class="chrome"><span>多模态时序 · ONE TIMELINE</span><span>16</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">多模态不是把三个功能并排接上</div>
      <h2 class="ink" style="--i:1">语音、视觉、动作，必须落在同一条时间线上</h2>
    </div>
    <div class="body">
      <div class="prz3">
        <div class="prz rise" style="--i:2">
          <div class="pzk">01 · HEAR · 连续流</div>
          <svg viewBox="0 0 460 240" aria-hidden="true">
            <line x1="10" y1="197" x2="450" y2="197" stroke="var(--hair)" stroke-width="1"/>
            <rect class="eqb" style="--d:0.00s" x="14" y="162" width="12" height="34" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.07s" x="39" y="134" width="12" height="62" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.15s" x="64" y="100" width="12" height="96" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.22s" x="89" y="72" width="12" height="124" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.30s" x="114" y="106" width="12" height="90" rx="2" fill="var(--coral)" opacity=".95"/><rect class="eqb" style="--d:0.38s" x="139" y="54" width="12" height="142" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.45s" x="164" y="84" width="12" height="112" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.53s" x="189" y="44" width="12" height="152" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.60s" x="214" y="98" width="12" height="98" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.67s" x="239" y="62" width="12" height="134" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.75s" x="264" y="44" width="12" height="152" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.82s" x="289" y="90" width="12" height="106" rx="2" fill="var(--coral)" opacity=".95"/><rect class="eqb" style="--d:0.90s" x="314" y="52" width="12" height="144" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:0.97s" x="339" y="106" width="12" height="90" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:1.05s" x="364" y="74" width="12" height="122" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:1.12s" x="389" y="122" width="12" height="74" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:1.20s" x="414" y="98" width="12" height="98" rx="2" fill="var(--amber)" opacity=".8"/><rect class="eqb" style="--d:1.27s" x="439" y="148" width="12" height="48" rx="2" fill="var(--amber)" opacity=".8"/>
          </svg>
          <div class="pzt">语音<b>·毫秒</b></div>
          <div class="pzs">边说边理解，是一条不间断的流。打断和让步，都发生在这条流上。</div>
        </div>
        <div class="prz rise" style="--i:3">
          <div class="pzk">02 · SEE · 帧序列</div>
          <svg viewBox="0 0 460 240" aria-hidden="true">
            <rect x="24" y="34" width="412" height="164" rx="6" class="stroke" stroke-width="1.4"/>
            <g opacity=".5">
              <path class="stroke" stroke-width="1" d="M24 76 H436"/>
              <path class="stroke" stroke-width="1" d="M24 116 H436"/>
              <path class="stroke" stroke-width="1" d="M24 156 H436"/>
            </g>
            <path class="stroke-am pkt" style="--pl:150px;--p0:150px;--p1:-170px;--pt:2.6s" stroke-width="2.5" d="M40 34 V198"/>
            <rect x="252" y="86" width="96" height="76" rx="4" class="stroke-am" stroke-width="2.4"/>
            <circle class="fill-co" cx="300" cy="124" r="7"/>
            <circle class="mring" cx="300" cy="124" r="7" fill="none" stroke="var(--coral)" stroke-width="2"/>
            <text class="lbl" x="24" y="224" style="font-size:14px">一帧 · 一帧 · 一帧</text>
            <text class="lbl fill-co" x="436" y="224" text-anchor="end" style="font-size:14px">看见「你抬头了」</text>
          </svg>
          <div class="pzt">视觉<b>·百毫秒</b></div>
          <div class="pzs">画面是一帧一帧到的，天然比语音慢一拍。慢多少，决定了它抬头的时机对不对。</div>
        </div>
        <div class="prz rise" style="--i:4">
          <div class="pzk">03 · ACT · 物理量</div>
          <svg viewBox="0 0 460 240" aria-hidden="true">
            <path class="stroke" stroke-width="2" opacity=".45" d="M14 120 C 56 96, 88 150, 126 120 C 152 100, 178 140, 212 122"/>
            <circle class="fill-am" cx="234" cy="120" r="9"/>
            <circle class="mring" cx="234" cy="120" r="8" fill="none" stroke="var(--amber)" stroke-width="2"/>
            <circle class="mring" cx="234" cy="120" r="8" fill="none" stroke="var(--amber)" stroke-width="2" style="--d:.7s"/>
            <path class="stroke-am" stroke-width="2" opacity=".7" d="M248 120 H436"/>
            <path class="stroke-am pkt" style="--pl:20px;--p0:20px;--p1:-230px;--pt:1.4s" stroke-width="4.5" d="M248 120 H436"/>
            <text class="lbl" x="24" y="88" style="font-size:14px">决定要动</text>
            <text class="lbl fill-co" x="436" y="98" text-anchor="end" style="font-size:14px">发出去就收不回</text>
          </svg>
          <div class="pzt">动作<b>·秒级</b></div>
          <div class="pzs">电机要转起来才算数，最慢，而且没有撤回键——它必须最早被决定。</div>
        </div>
      </div>
      <div class="land flow rev" style="--i:5">三条通道的时间粒度根本不一样。<b>谁来把它们对齐到同一条时间线上，谁就决定了体验。</b><span class="s">并排接上三个模型，只会得到三条各走各的时间轴——那不是多模态，那是三个功能。</span></div>
    </div>
  </div>
</section>'''

# ── P17 · 视觉高潮④ 上 · 端云责任边界 ─────────────────────────
P17 = '''<section class="slide">
  <div class="chrome"><span>端云边界 · EDGE × CLOUD</span><span>17</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">切在哪，第一次成了产品决策，不是硬件预算决策</div>
      <h2 class="ink" style="--i:1">反应在端，理解在云，断网不失态</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 424" width="1680" aria-hidden="true">
          <path class="dw" style="--len:300;--i:2" d="M840 16 V316" stroke="var(--hair-strong)" stroke-width="1.2" stroke-dasharray="6 9" fill="none"/>
          <g class="pop" style="--i:2">
            <rect x="0" y="40" width="790" height="252" rx="6" fill="none" stroke="var(--amber)" stroke-width="2"/>
            <text class="lbl fill-am" x="34" y="86">端侧 · 反应在端</text>
            <text class="fill-ink" x="34" y="140" style="font-size:32px;font-weight:900">半秒之内必须发生的事</text>
            <text class="txt" x="34" y="192">唤醒与拾音 · 打断与让步 · 表情与转头 · 避障与急停</text>
            <text class="sm" x="34" y="236">判据不是算力够不够，是慢半秒会不会出戏。</text>
            <text class="sm" x="34" y="266">一个来回的公网往返，在这里就已经太久了。</text>
          </g>
          <g class="pop" style="--i:3">
            <rect class="box" x="890" y="40" width="790" height="252" rx="6" stroke-width="1"/>
            <text class="lbl" x="924" y="86">云端 · 理解在云</text>
            <text class="fill-ink" x="924" y="140" style="font-size:32px;font-weight:900">要随关系一起变厚的事</text>
            <text class="txt" x="924" y="192">复杂推理 · 长期记忆与召回 · 角色一致性校验 · 内容生成</text>
            <text class="sm" x="924" y="236">这些东西会随着相处越长越大，</text>
            <text class="sm" x="924" y="266">不该被一颗 SoC 的规格封顶。</text>
          </g>
          <g class="pop" style="--i:4">
            <rect x="0" y="330" width="1680" height="82" rx="6" fill="none" stroke="var(--coral)" stroke-width="2"/>
            <text class="lbl fill-co" x="34" y="366">断网时 · GRACEFUL DEGRADE</text>
            <text class="txt" x="34" y="398">端侧先接管，说一句它自己的话，再排队等云端回来——宁可慢，也不许定住三秒。失态一次，角色就碎一次。</text>
          </g>
        </svg>
      </div>
      <div class="land flow" style="--i:5">切分的标准不是算力，是体验红线：<b>哪些事慢半秒就出戏，哪些事可以想两秒。</b></div>
    </div>
  </div>
</section>'''

# ── P18 · 故障与恢复 ──────────────────────────────────────────
P18 = '''<section class="slide">
  <div class="chrome"><span>故障与恢复 · RECOVERABLE ACTION</span><span>18</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow coral flow" style="--i:0">真实使用里，这四件事一定会发生</div>
      <h2 class="ink" style="--i:1">伙伴感不会死于一次错误，只会死于错误之后的沉默</h2>
    </div>
    <div class="body">
      <table class="tight">
        <thead><tr><th>断裂场景</th><th>会击穿伙伴感的处理</th><th>可恢复的处理</th></tr></thead>
        <tbody>
          <tr class="flow" style="--i:2"><td>断网</td><td>定住三秒，回来之后从头开始，像什么都没发生过</td><td>端侧先应一声，回来后接着上一句往下讲</td></tr>
          <tr class="flow" style="--i:3"><td>误唤醒</td><td>突然自说自话，把屋里的人吓一跳</td><td>先低声确认一次，没人应答就安静退回待机</td></tr>
          <tr class="flow" style="--i:3"><td>多人同时说话</td><td>谁大声听谁的，或者干脆两个都答</td><td>认住此刻的说话人，其余按背景处理，并说明它在跟谁说</td></tr>
          <tr class="flow" style="--i:4"><td>动作失败</td><td>反复重试，或者假装已经做到了</td><td>说出它做不到，给出下一步，并把这次失败记进关系账本</td></tr>
        </tbody>
      </table>
      <div class="land flow" style="--i:5">这就是「可恢复行动」的工程含义：<b>每一个动作都要有取消点，每一次失败都要有说明点。</b><span class="s">用户能原谅一个会犯错的伙伴，不会原谅一个犯了错还当没发生的机器。</span></div>
    </div>
  </div>
</section>'''

# ── P19 · E2E 链路 ────────────────────────────────────────────
P19 = '''<section class="slide">
  <div class="chrome"><span>一条真实链路 · THE E2E PATH</span><span>19</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">把上面这些话，落到一条能画出来的路径上</div>
      <h2 class="ink" style="--i:1">一次交互经过六段，每一段都有延迟，也都有失败点</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 400" width="1680" aria-hidden="true">
          <text class="lbl pop" style="--i:2" x="0" y="20">用户话音落地</text>
          <text class="lbl fill-am pop" style="--i:2" x="1680" y="20" text-anchor="end">第一声回应 · 第一个动作</text>
          <path class="dw" style="--len:260;--i:2" d="M240 152 H288 M528 152 H576 M816 152 H864 M1104 152 H1152 M1392 152 H1440" stroke="var(--hair-strong)" stroke-width="1.6" fill="none"/>
          <g class="pop" style="--i:3">
            <rect class="box" x="0" y="96" width="240" height="112" rx="4" stroke-width="1"/>
            <text class="ttl" x="24" y="140" style="font-size:23px">① 感知</text>
            <text class="sm" x="24" y="176">拾音 · VAD · 选择性注意</text>
            <text class="lbl fill-am" x="24" y="72">数十 ms</text>
            <text class="lbl fill-co" x="24" y="248">误唤醒 / 漏拾</text>
          </g>
          <g class="pop" style="--i:3">
            <rect class="box" x="288" y="96" width="240" height="112" rx="4" stroke-width="1"/>
            <text class="ttl" x="312" y="140" style="font-size:23px">② 路由</text>
            <text class="sm" x="312" y="176">接入 · 鉴权 · 编排</text>
            <text class="lbl fill-am" x="312" y="72">数十 ms</text>
            <text class="lbl fill-co" x="312" y="248">超时 / 网络抖动</text>
          </g>
          <g class="pop" style="--i:4">
            <rect class="box" x="576" y="96" width="240" height="112" rx="4" stroke-width="1"/>
            <text class="ttl" x="600" y="140" style="font-size:23px">③ 检索</text>
            <text class="sm" x="600" y="176">关系账本召回</text>
            <text class="lbl fill-am" x="600" y="72">数十～百 ms</text>
            <text class="lbl fill-co" x="600" y="248">召回了不相干的事</text>
          </g>
          <g class="pop" style="--i:4">
            <rect x="864" y="96" width="240" height="112" rx="4" fill="none" stroke="var(--amber)" stroke-width="2"/>
            <text class="ttl fill-am" x="888" y="140" style="font-size:23px">④ 模型</text>
            <text class="sm" x="888" y="176">理解 · 推理 · 生成</text>
            <text class="lbl fill-am" x="888" y="72">首 token 百 ms 级</text>
            <text class="lbl fill-co" x="888" y="248">首包抖动 / 跑题</text>
          </g>
          <g class="pop" style="--i:5">
            <rect class="box" x="1152" y="96" width="240" height="112" rx="4" stroke-width="1"/>
            <text class="ttl" x="1176" y="140" style="font-size:23px">⑤ 合成</text>
            <text class="sm" x="1176" y="176">TTS 首帧 · 韵律</text>
            <text class="lbl fill-am" x="1176" y="72">百 ms 级</text>
            <text class="lbl fill-co" x="1176" y="248">音频卡顿 / 情绪不对</text>
          </g>
          <g class="pop" style="--i:5">
            <rect x="1440" y="96" width="240" height="112" rx="4" fill="none" stroke="var(--coral)" stroke-width="2"/>
            <text class="ttl fill-co" x="1464" y="140" style="font-size:23px">⑥ 动作</text>
            <text class="sm" x="1464" y="176">下发 · 执行 · 回报</text>
            <text class="lbl fill-am" x="1464" y="72">百 ms 级</text>
            <text class="lbl fill-co" x="1464" y="248">被挡住 / 没有回报</text>
          </g>
          <g class="pop" style="--i:5">
            <path class="stroke-am pkt" stroke-width="4" fill="none"
              style="--pl:26px;--p0:26px;--p1:-280px;--pt:4.4s;--pd:1s" d="M240 152 H288 M528 152 H576 M816 152 H864 M1104 152 H1152 M1392 152 H1440"/>
          </g>
          <path d="M0 300 H1680" stroke="var(--hair)" stroke-width="1"/>
          <text class="txt pop" style="--i:5" x="0" y="342">上面一行是延迟贡献，下面一行是失败点。<tspan class="fill-ink" style="font-weight:700">产品经理要做的第一件事，是把这两行填满，并在每一格上写下责任方。</tspan></text>
          <text class="lbl pop" style="--i:5" x="0" y="386">口径 · 链路为声网对话式 AI 引擎生产架构；时间为数量级，内部口径，非任何客户的实测值</text>
        </svg>
      </div>
    </div>
  </div>
</section>'''

# ── P20 · 视觉高潮④ 主体 · 四方责任划分 ───────────────────────
P20 = '''<section class="slide">
  <div class="chrome"><span>责任边界 · WHO OWNS WHAT</span><span>20</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">这一页，是我今天最想让你拍下来的一页</div>
      <h2 class="ink" style="--i:1">四方各自负责什么，先划清楚，再谈破局</h2>
    </div>
    <div class="body">
      <table class="quad">
        <thead><tr><th></th><th>产品团队</th><th>模型</th><th>实时引擎</th><th>设备</th></tr></thead>
        <tbody>
          <tr class="flow" style="--i:2">
            <td>负责</td>
            <td class="am"><b>角色</b>关系目标 · 体验标准与评测</td>
            <td><b>理解</b>推理 · 内容生成</td>
            <td><b>时序</b>编排 · 打断 · 恢复与稳定性</td>
            <td><b>感知</b>动作 · 端侧安全与物理边界</td>
          </tr>
          <tr class="flow" style="--i:3">
            <td>交付物</td>
            <td>角色卡 · 关系账本设计 · 评测集</td>
            <td>能力与成本曲线</td>
            <td>时序与稳定性的可承诺指标</td>
            <td>传感与执行规格 · 安全边界</td>
          </tr>
          <tr class="flow" style="--i:4">
            <td>缺位时</td>
            <td>一个更聪明、也更贵的玩具</td>
            <td>答得不对、不像那个它</td>
            <td>抢话、卡顿、断了回不来</td>
            <td>看不见、动不了、不安全</td>
          </tr>
        </tbody>
      </table>
      <div class="land flow" style="--i:5">产品化破局不是多接一个模型，而是重新划清责任边界：<b>实时系统标准化，角色资产私有化，体验标准数据化。</b></div>
    </div>
  </div>
</section>'''

# ── P21 · 产品证据（cowork 全景图回收）────────────────────────
P21 = '''<section class="slide">
  <div class="chrome"><span>产品证据 · THE PANORAMA</span><span>21</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">交个底 · 上面那条实时引擎，具体是什么</div>
      <h2 class="ink" style="--i:1">不是四个赛道，是同一个能力模型的四个切片</h2>
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
            <text class="ttl pop" style="--i:0;font-size:26px" x="60" y="116">Call Agent</text>
            <text class="sm pop" style="--i:0" x="60" y="142">电话智能体</text>
            <circle class="pop" style="--i:0" cx="330" cy="118" r="17" fill="var(--amber)" opacity=".85"/>
            <circle class="pop" style="--i:0" cx="580" cy="118" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="830" cy="118" r="15" fill="var(--amber)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="1080" cy="118" r="10" fill="var(--ink-3)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="1330" cy="118" r="21" fill="var(--amber)"/>
          </g>
          <g data-step="1">
            <text class="ttl pop" style="--i:0;font-size:26px" x="60" y="216">Physical AI</text>
            <text class="sm pop" style="--i:0" x="60" y="242">硬件与具身 · 今天这一场</text>
            <circle class="pop" style="--i:0" cx="330" cy="218" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="580" cy="218" r="15" fill="var(--amber)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="830" cy="218" r="17" fill="var(--amber)" opacity=".85"/>
            <circle class="pop" style="--i:0" cx="1080" cy="218" r="19" fill="var(--amber)" opacity=".9"/>
            <circle class="pop" style="--i:0" cx="1330" cy="218" r="10" fill="var(--ink-3)" opacity=".7"/>
          </g>
          <g data-step="2">
            <text class="ttl pop" style="--i:0;font-size:26px" x="60" y="316">STT</text>
            <text class="sm pop" style="--i:0" x="60" y="342">实时转写与翻译</text>
            <circle class="pop" style="--i:0" cx="330" cy="318" r="21" fill="var(--amber)"/>
            <circle class="pop" style="--i:0" cx="580" cy="318" r="12" fill="var(--ink-3)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="830" cy="318" r="12" fill="var(--ink-3)" opacity=".7"/>
            <circle class="pop" style="--i:0" cx="1080" cy="318" r="17" fill="var(--amber)" opacity=".85"/>
            <circle class="pop" style="--i:0" cx="1330" cy="318" r="8" fill="var(--ink-3)" opacity=".6"/>
          </g>
          <g data-step="2">
            <text class="ttl pop" style="--i:0;font-size:26px" x="60" y="416">ConvoAI Engine</text>
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
      <div class="note flow" style="--i:5" data-step="2">四条产品线共用同一套时序、编排、打断与恢复能力——<b>任何一格的进步，四条线一起受益。</b>今天讲的这类硬件，就是图上「Physical AI」那一行。</div>
      <div class="foot src flow" style="--i:5">口径 · 投入强度为内部口径的相对表示，非市场份额、非客户数据</div>
    </div>
  </div>
</section>'''

# ── P22 · 标准化接口 ──────────────────────────────────────────
P22 = '''<section class="slide">
  <div class="chrome"><span>标准化接口 · WHAT TO OUTSOURCE</span><span>22</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">同一件事，第二十家公司再做一遍，不会更好</div>
      <h2 class="ink" style="--i:1">哪些能力应该沉成基础设施，哪些必须你自己拥有</h2>
    </div>
    <div class="body">
      <div class="duo">
        <div class="flow" style="--i:2">
          <div class="h">沉成基础设施 · 引擎侧</div>
          <div class="b">每家都要做一遍，做出来也不构成差异</div>
          <div class="s">时序对齐、打断与让步、回声消除、选择性注意、端云切换、断网降级、可观测与归因。<br>它们决定体验的下限，而下限应该用工程锁死，不该用产品团队的时间去反复兑换。</div>
        </div>
        <div class="flow rev" style="--i:3">
          <div class="h">必须自己拥有 · 产品侧</div>
          <div class="b">外包出去，你的产品就没有了自己</div>
          <div class="s">角色卡、关系账本、体验标准与评测集。<br>它们决定体验的上限，也是唯一会随时间增值的东西——模型可以换，引擎可以换，这三样换不了。</div>
        </div>
      </div>
      <div class="note flow" style="--i:4">在我们接触的典型项目中，让一台硬件同时做到「听得清、看得懂、反应快、断了还回得来」，把这条链路完整接通仍需数月。<b>这几个月花在哪，基本决定了产品最后长什么样。</b></div>
      <div class="land flow" style="--i:5">把不该你解的题标准化，<b>把只有你能做的事私有化。</b></div>
    </div>
  </div>
</section>'''

# ── P23 · 评测闭环 ────────────────────────────────────────────
P23 = '''<section class="slide">
  <div class="chrome"><span>评测闭环 · MAKE IT REGRESSABLE</span><span>23</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">说不清的东西，就管不住</div>
      <h2 class="ink" style="--i:1">把关系体验，变成可以每周重跑一次的评测</h2>
    </div>
    <div class="body">
      <div class="rows">
        <div class="r flow" style="--i:2"><span class="n">01</span><span class="k">角色是否一致</span><span class="v">换上下文、换时间、换情绪，它的判断方式还是不是同一个。回归集里放人格锚点用例，任何一次角色改动都要重跑。</span></div>
        <div class="r flow" style="--i:3"><span class="n">02</span><span class="k">该想起的想起了没有</span><span class="v">不是「记住多少」，是「此刻该不该提」。既要测召回的准确，也要测克制——不合时宜地翻旧账，比忘掉更伤关系。</span></div>
        <div class="r flow" style="--i:4"><span class="n">03</span><span class="k">时机对不对</span><span class="v">开口时机、打断与让步、沉默时长、动作与语音的先后。这一组只能在真实音频和真实动作上跑，文本测不出来。</span></div>
      </div>
      <div class="note flow" style="--i:5">节奏：每周一次回归，通过率不达标不发版——改角色和改支付逻辑，走同一条评审通道。这一条不是流程洁癖，是因为<b>角色漂移在线上是一次事故，不是一次调优。</b></div>
      <div class="land flow" style="--i:5">产品经理的交付物变了：<b>你写下的这套评测，就是这个角色的定义。</b></div>
    </div>
  </div>
</section>'''

# ── P24 · 三个动作 ────────────────────────────────────────────
P24 = '''<section class="slide">
  <div class="chrome"><span>带走 · THREE MOVES</span><span>24</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">不需要立项，本周就能做</div>
      <h2 class="ink" style="--i:1">回去以后的三个动作</h2>
    </div>
    <div class="body">
      <div class="g3">
        <div class="card rise" style="--i:2">
          <div class="n">1</div>
          <div class="tag">回扣 · 临场</div>
          <div class="t">画一条真实的时间线</div>
          <div class="d">从用户开口，到设备做出动作。把每一段延迟、每一个失败点、每一格的责任方，都写在同一张纸上。</div>
          <div class="d"><b>做完你会发现：</b>大多数团队从来没有把这条线完整画出来过。</div>
        </div>
        <div class="card on rise" style="--i:3">
          <div class="n">2</div>
          <div class="tag">回扣 · 三乘数</div>
          <div class="t">定义三个关系评测</div>
          <div class="d">角色是否一致、是否想起了正确的历史、是否在合适的时机回应。每一项先写十条用例就够。</div>
          <div class="d"><b>做完你会发现：</b>你的看板上，可能一个这样的指标都没有。</div>
        </div>
        <div class="card rise" style="--i:4">
          <div class="n">3</div>
          <div class="tag">回扣 · 责任边界</div>
          <div class="t">做一次断裂测试</div>
          <div class="d">断网、误唤醒、多人同时说话、动作失败——四种情况各来一遍，看它能不能优雅地回来。</div>
          <div class="d"><b>做完你会发现：</b>体验的差距，几乎全在这四个瞬间里。</div>
        </div>
      </div>
      <div class="land flow" style="--i:5">这三件事的顺序不能换：<b>先看清时间线，再定义标准，最后才去压断裂。</b></div>
    </div>
  </div>
</section>'''

# ── P25 · 回收 ────────────────────────────────────────────────
P25 = '''<section class="slide">
  <div class="chrome"><span>回收 · BACK TO THE DRAWER</span><span>25</span></div>
  <div class="wrap">
    <div class="head">
      <div class="eyebrow flow" style="--i:0">回到开场那条曲线</div>
      <h2 class="ink" style="--i:1">第四天进抽屉，是因为三个乘数里，有一个归了零</h2>
    </div>
    <div class="body">
      <div class="fig gfill">
        <svg viewBox="0 0 1680 336" width="1680" aria-hidden="true">
          <g class="pop" style="--i:2">
            <rect class="box" x="0" y="20" width="500" height="196" rx="6" stroke-width="1"/>
            <text class="lbl" x="34" y="66">角色一致性 → 0</text>
            <text class="fill-ink" x="34" y="124" style="font-size:34px;font-weight:900">它每天像换了一个人</text>
            <text class="sm" x="34" y="168">上午像客服，下午像哥们，</text>
            <text class="sm" x="34" y="196">晚上像心理医生——你没法跟一个人设不稳的东西建立关系。</text>
          </g>
          <g class="pop" style="--i:3">
            <rect class="box" x="590" y="20" width="500" height="196" rx="6" stroke-width="1"/>
            <text class="lbl" x="624" y="66">共同历史 → 0</text>
            <text class="fill-ink" x="624" y="124" style="font-size:34px;font-weight:900">它永远第一次见你</text>
            <text class="sm" x="624" y="168">你昨天说的事，今天要从头讲一遍。</text>
            <text class="sm" x="624" y="196">聊天记录都在，可它什么也没想起来。</text>
          </g>
          <g class="pop" style="--i:4">
            <rect class="box" x="1180" y="20" width="500" height="196" rx="6" stroke-width="1"/>
            <text class="lbl" x="1214" y="66">可控临场 → 0</text>
            <text class="fill-ink" x="1214" y="124" style="font-size:34px;font-weight:900">它总在你走开之后开口</text>
            <text class="sm" x="1214" y="168">该接话的时候在加载，该安静的时候在说话，</text>
            <text class="sm" x="1214" y="196">断一次网就再也回不到刚才。</text>
          </g>
          <path class="dw" style="--len:1680;--i:5" d="M0 262 H1680" stroke="var(--coral)" stroke-width="1.5" stroke-dasharray="5 8" fill="none"/>
          <text class="fill-co pop" style="--i:5" x="0" y="316" font-size="30" font-weight="900">这三条里只要有一条归零，前面所有的能力，都乘不出关系。</text>
        </svg>
      </div>
      <div class="land flow" style="--i:5">所以那个抽屉，从来不是因为它不够聪明。<span class="s">是因为三个乘数里的某一项，从第一天起就没有人负责。</span></div>
    </div>
  </div>
</section>'''

# ── P26 · 收尾 ────────────────────────────────────────────────
P26 = '''<section class="slide">
  <div class="cover">
    <div class="kicker flow" style="--i:0">谢谢</div>
    <h1 class="ink" style="--i:1;font-size:74px">模型让它会回答，<br>角色让它保持一致，<br>历史让关系得以继续，<br>临场让这一切发生在此刻。</h1>
    <div class="subtitle spread" style="--i:3">从「被使用」，到「被记住」。</div>
    <div class="meta q">
      <div class="rise" style="--i:4"><span class="k">讲者</span><span class="v">姚光华 Colin</span></div>
      <div class="rise" style="--i:4"><span class="k">职务</span><span class="v">声网 AI 产品线负责人</span></div>
      <div class="rise" style="--i:5"><span class="k">场合</span><span class="v">2026 AI 产品大会 · 声网 AIoT 专场 · 北京</span></div>
    </div>
  </div>
</section>'''

S = [P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13,
     P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26]
assert len(S) == 26, len(S)
S = [capi(x, 7) for x in S]

s = head + '\n'.join(S) + tail

# 页码重排
_st = [m.start() for m in re.finditer(r'<section class="slide', s)]
assert len(_st) == 26, len(_st)


def _rn(mm):
    idx = sum(1 for t in _st if t <= mm.start())
    return mm.group(1) + ('%02d' % idx) + mm.group(2)


s = re.sub(r'(<div class="chrome"><span>[^<]*</span><span>)[^<]*(</span></div>)', _rn, s)

open('public/decks/aiot26-v2.html', 'w', encoding='utf-8').write(s)

# ═══════════════════════════════════════════════════════════════
# 四、发布前断言
# ═══════════════════════════════════════════════════════════════
n = len(re.findall(r'<section class="slide', s))
assert n == 26, n

# 三个可引用资产在位
ASSETS = [
    '伙伴感 = 角色一致性 × 共同历史 × 可控临场',
    '任何一项接近零 —— 得到的都只是一个更昂贵、更聪明的玩具。',
    '感知 → 召回 → 判断 → 行动 → 新的感知',
    '临场 = 实时感知 × 即时召回 × 合时回应 × 可恢复行动',
    '实时系统标准化，角色资产私有化，体验标准数据化',
    '产品化破局不是多接一个模型，而是重新划清责任边界',
    '身体让一次回答，变成一次会产生后果的行动',
    '系统延迟要消失，表达停顿要被设计',
    '快，是基础设施问题；<b>什么时候开口，是产品问题。</b>',
    '从「被使用」，到「被记住」。',
]
for a in ASSETS:
    assert a in s, '资产缺失: ' + a

# 事实红线：只查屏上文字（不含 CSS / JS，避免 38% 54% 这类样式数值误伤）
TXT = re.sub(r'<[^>]+>', ' ', '\n'.join(S))
BAN = ['OPENAI TOLAN', 'SOTA', '物理上限', '上半场', '下半场', '泡泡玛特', '红杉',
       '角色给它名字', '九成', '3-6 个月', '3—6 个月', '走进第 4 段', '已解决', '致命',
       'Mehrabian', '超 30 家', '亿元级融资']
for b in BAN:
    assert b not in TXT, '红线词命中: ' + b
assert not ('7%' in TXT and '38%' in TXT and '55%' in TXT), 'Mehrabian 7/38/55 组合命中'

# 默认浅色 + 隐藏 swap + noindex + 底盘件齐全
assert '<html lang="zh-CN">' in s and 'data-theme="dark"><head>' not in s, '默认主题不是 light'
assert "localStorage.getItem('colin-theme')==='dark'" in s, 'light-first 引导脚本缺失'
assert "cur='light'" in s and "colin-theme')||'light'" in s, 'swap 默认值未改'
assert '.deck-swap{display:none!important;' in s, 'deck-swap 未隐藏'
assert 'noindex' in s and 'deckRuler' in s and 'data-dm' in s, '底盘件缺失'
assert 'poster="/media/aiot26/still-1.jpg"' in s and 'vstills' in s, '视频封面帧 / 兜底行缺失'

# svg 必须在类作用域容器内（.fig 或 .prz）
for m in re.finditer(r'<svg', s):
    seg = s[max(0, m.start() - 900):m.start()]
    assert ('class="fig' in seg or 'class="prz' in seg or 'deck-flow' in s[m.start():m.start() + 80]), \
        'svg 未包在 .fig/.prz 内 @%d' % m.start()

steps = re.findall(r'data-step="(\d+)"', s)
print('aiot26-v2.html · %d 页 · %dKB · data-step 揭示点 %d 处（最大档 %s）'
      % (n, len(s) // 1024, len(steps), max(steps) if steps else '-'))
print('资产 ✓  红线 ✓  默认 light ✓  swap 隐藏 ✓  noindex ✓  媒体 ✓  fig 作用域 ✓')
