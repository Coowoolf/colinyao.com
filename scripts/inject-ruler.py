#!/usr/bin/env python3
"""deck-ruler：顶线即尺子——整体进度 + hover 刻度齿 + 点击/拖动跳页 + 数字键直达。
   注入全部 deck（talkdecks 索引页除外）；幂等；隐藏旧的底部进度条。"""
import glob, pathlib

MODULE = """
<style>
/* deck-ruler · 顶线即尺子：整体进度 + 跳页（hover 出刻度齿，点击/拖动直达，数字+Enter 跳页） */
.deck-progress,#progress{display:none!important;}
.deck-ruler{position:fixed;top:0;left:0;right:0;height:20px;z-index:1200;cursor:pointer;}
.dr-track{position:absolute;top:0;left:0;right:0;height:2px;background:var(--hair,rgba(128,128,128,.22));transition:height .25s ease;}
.dr-fill{position:absolute;top:0;left:0;height:2px;width:0;background:var(--amber,#ff8906);transition:width .45s cubic-bezier(.22,.9,.24,1),height .25s ease;}
.dr-teeth{position:absolute;top:0;left:0;right:0;height:7px;opacity:0;transition:opacity .25s ease;pointer-events:none;}
.dr-teeth i{position:absolute;top:0;width:1px;height:4px;background:var(--ink-3,#8a8a99);opacity:.55;}
.dr-teeth i.maj{height:7px;opacity:.95;}
.deck-ruler:hover .dr-track,.deck-ruler:hover .dr-fill{height:6px;}
.deck-ruler:hover .dr-teeth{opacity:1;}
.dr-tip{position:absolute;top:13px;left:50%;transform:translateX(-50%);
  font-family:var(--f-mono,monospace);font-size:11px;line-height:1;letter-spacing:.1em;
  color:var(--ink,#fff);background:var(--card-bg-2,var(--panel,#1c1b26));
  border:1px solid var(--hair,rgba(128,128,128,.25));border-radius:2px;padding:5px 8px;
  opacity:0;transition:opacity .2s;white-space:nowrap;pointer-events:none;}
.deck-ruler:hover .dr-tip{opacity:1;}
@media print{.deck-ruler{display:none!important;}}
</style>
<div class="deck-ruler" id="deckRuler" aria-hidden="true"><div class="dr-track"></div><div class="dr-teeth"></div><div class="dr-fill"></div><div class="dr-tip">1</div></div>
<script>
(function(){
  var slides=document.querySelectorAll('.slide');var N=slides.length;if(!N)return;
  var ruler=document.getElementById('deckRuler'),fill=ruler.querySelector('.dr-fill'),
      tip=ruler.querySelector('.dr-tip'),teeth=ruler.querySelector('.dr-teeth');
  /* 刻度齿：页多自动抽稀（≤96 根），每 5 根一长齿 */
  var step=Math.max(1,Math.ceil(N/96));
  for(var i=0;i<N;i+=step){var t=document.createElement('i');
    if((i/step)%5===0)t.className='maj';t.style.left=(((i+0.5)/N)*100)+'%';teeth.appendChild(t);}
  function cur(){for(var i=0;i<N;i++)if(slides[i].classList.contains('active'))return i;return 0;}
  function paint(){fill.style.width=(((cur()+1)/N)*100)+'%';}
  var mo=new MutationObserver(paint);
  slides.forEach(function(s){mo.observe(s,{attributes:true,attributeFilter:['class']});});
  paint();
  function target(e){var r=ruler.getBoundingClientRect();
    var x=(e.touches&&e.touches[0]?e.touches[0].clientX:e.clientX);
    var f=(x-r.left)/r.width;return Math.max(0,Math.min(N-1,Math.floor(f*N)));}
  function jump(n){
    if(window.deck&&typeof window.deck.go==='function'){window.deck.go(n);return;}
    var d=n-cur(),key=d>0?'ArrowRight':'ArrowLeft';
    for(var i=0;i<Math.abs(d);i++)document.dispatchEvent(new KeyboardEvent('keydown',{key:key,bubbles:true}));
  }
  var dragging=false;
  ruler.addEventListener('mousemove',function(e){var n=target(e);
    tip.textContent=(n+1)+' / '+N;tip.style.left=(((n+0.5)/N)*100)+'%';if(dragging)jump(n);});
  ruler.addEventListener('mousedown',function(e){dragging=true;jump(target(e));e.preventDefault();});
  addEventListener('mouseup',function(){dragging=false;});
  ruler.addEventListener('click',function(e){jump(target(e));});
  ruler.addEventListener('touchstart',function(e){jump(target(e));e.preventDefault();},{passive:false});
  ruler.addEventListener('touchmove',function(e){jump(target(e));e.preventDefault();},{passive:false});
  /* 数字键 + Enter 直达 */
  var buf='',bufT=null;
  document.addEventListener('keydown',function(e){
    if(e.target&&e.target.getAttribute&&e.target.getAttribute('contenteditable')==='true')return;
    if(e.key>='0'&&e.key<='9'){buf+=e.key;clearTimeout(bufT);bufT=setTimeout(function(){buf='';tip.style.opacity='';},1600);
      tip.textContent=buf+' / '+N;tip.style.left='50%';tip.style.opacity='1';}
    else if(e.key==='Enter'&&buf){var n=parseInt(buf,10);buf='';tip.style.opacity='';
      if(n>=1&&n<=N)jump(n-1);}
    else if(buf){buf='';tip.style.opacity='';}
  });
})();
</script>
"""

count = 0
for f in sorted(glob.glob("public/decks/*.html")):
    name = pathlib.Path(f).name
    if name == "talkdecks.html":
        continue
    s = open(f, encoding="utf-8").read()
    if "deckRuler" in s:
        continue
    assert "</body>" in s, name
    s = s.replace("</body>", MODULE + "</body>", 1)
    open(f, "w", encoding="utf-8").write(s)
    count += 1
print(f"injected deck-ruler into {count} decks")
