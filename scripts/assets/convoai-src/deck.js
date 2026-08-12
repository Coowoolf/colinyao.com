/* ===========================================
   固定舞台演示控制器 —— 1920×1080 整体缩放 + 分步展开
   =========================================== */
class SlidePresentation{
  constructor(){
    this.slides=[...document.querySelectorAll('.slide')];
    this.stage=document.getElementById('deckStage');
    this.progress=document.getElementById('deckProgress');
    this.stepsEl=document.getElementById('deckSteps');
    this.i=0;this.step=0;
    /* 预先算好每页的分步数 */
    this.maxStep=this.slides.map(s=>{
      const els=[...s.querySelectorAll('[data-step]')];
      return els.length?Math.max(...els.map(e=>+e.dataset.step||0)):0;
    });
    this.setupScale();this.setupKeys();this.setupTouch();this.setupWheel();
    this.go(this.readHash(),true);
    window.addEventListener('hashchange',()=>this.go(this.readHash()));
  }
  readHash(){const n=parseInt((location.hash||'').replace('#',''),10);return isNaN(n)?0:n-1;}

  setupScale(){
    const scale=()=>{
      const f=Math.min(window.innerWidth/1920,window.innerHeight/1080);
      const x=(window.innerWidth-1920*f)/2, y=(window.innerHeight-1080*f)/2;
      this.stage.style.transform=`translate(${x}px, ${y}px) scale(${f})`;
    };
    scale();window.addEventListener('resize',scale);
  }
  setupKeys(){
    document.addEventListener('keydown',e=>{
      if(e.target.getAttribute&&e.target.getAttribute('contenteditable'))return;
      if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();this.next();}
      if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();this.prev();}
      if(e.key==='Home'){e.preventDefault();this.go(0);}
      if(e.key==='End'){e.preventDefault();this.go(this.slides.length-1);}
      /* n / p 跳整页，跳过分步 */
      if(e.key==='n'){e.preventDefault();this.go(this.i+1);}
      if(e.key==='p'){e.preventDefault();this.go(this.i-1);}
    });
  }
  setupTouch(){
    let x0=null,y0=null;
    document.addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
    document.addEventListener('touchend',e=>{
      if(x0===null)return;
      const dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0;
      if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)){dx<0?this.next():this.prev();}
      x0=null;y0=null;
    },{passive:true});
  }
  setupWheel(){
    let lock=false;
    document.addEventListener('wheel',e=>{
      if(lock)return;if(Math.abs(e.deltaY)<18)return;
      lock=true;setTimeout(()=>lock=false,700);
      e.deltaY>0?this.next():this.prev();
    },{passive:true});
  }

  /* —— 前进：先把本页的分步走完，再翻页 —— */
  next(){
    if(this.step<this.maxStep[this.i]){this.step++;this.applySteps();return;}
    this.go(this.i+1);
  }
  /* —— 后退：先退分步；退到 0 再回上一页，并展开到那一页的最后一步 —— */
  prev(){
    if(this.step>0){this.step--;this.applySteps();return;}
    this.go(this.i-1,false,true);
  }

  applySteps(){
    const cur=this.slides[this.i];
    cur.querySelectorAll('[data-step]').forEach(el=>{
      el.classList.toggle('on',(+el.dataset.step||0)<=this.step);
    });
    this.renderSteps();
  }
  renderSteps(){
    const max=this.maxStep[this.i];
    if(!max){this.stepsEl.classList.remove('on');this.stepsEl.innerHTML='';return;}
    let h='<b>build</b>';
    for(let k=1;k<=max;k++)h+=`<i class="${k<=this.step?'done':''}"></i>`;
    this.stepsEl.innerHTML=h;
    this.stepsEl.classList.add('on');
  }

  go(n,init,toEnd){
    const target=Math.max(0,Math.min(n,this.slides.length-1));
    this.i=target;
    this.step=toEnd?this.maxStep[target]:0;
    this.slides.forEach((s,k)=>{
      const on=(k===this.i);
      s.classList.toggle('active',on);
      if(!on)s.classList.remove('visible');
    });
    const cur=this.slides[this.i];
    /* 先按当前 step 归位，再触发入场，保证分步元素不会闪一下 */
    cur.querySelectorAll('[data-step]').forEach(el=>{
      el.classList.toggle('on',(+el.dataset.step||0)<=this.step);
    });
    void cur.offsetWidth;
    requestAnimationFrame(()=>requestAnimationFrame(()=>cur.classList.add('visible')));
    this.renderSteps();
    this.progress.style.width=((this.i+1)/this.slides.length*100)+'%';
    history.replaceState(null,'','#'+(this.i+1));
  }
}
const deck=new SlidePresentation();
window.deck=deck;

/* ===========================================
   就地编辑（E 键 / 左上角热区）
   =========================================== */
const editor={
  isActive:false,
  toggle(){
    this.isActive=!this.isActive;
    const btn=document.getElementById('editToggle');
    btn.classList.toggle('active',this.isActive);
    if(this.isActive)btn.classList.add('show');
    document.querySelectorAll('.slide h1,.slide h2,.slide h3,.slide p,.slide .t,.slide .d,.slide .q,.slide .s,.slide .l,.slide .sub,.slide .note,.slide td,.slide th,.slide .ds,.slide .v')
      .forEach(el=>el.setAttribute('contenteditable',this.isActive));
    if(!this.isActive)this.save();
  },
  save(){try{localStorage.setItem('deck-edits',document.getElementById('deckStage').innerHTML);}catch(e){}}
};
const hotzone=document.querySelector('.edit-hotzone');
const editToggle=document.getElementById('editToggle');
let hideT=null;
hotzone.addEventListener('mouseenter',()=>{clearTimeout(hideT);editToggle.classList.add('show');});
hotzone.addEventListener('mouseleave',()=>{hideT=setTimeout(()=>{if(!editor.isActive)editToggle.classList.remove('show');},400);});
editToggle.addEventListener('mouseenter',()=>clearTimeout(hideT));
editToggle.addEventListener('mouseleave',()=>{hideT=setTimeout(()=>{if(!editor.isActive)editToggle.classList.remove('show');},400);});
editToggle.addEventListener('click',()=>editor.toggle());
hotzone.addEventListener('click',()=>editor.toggle());
document.addEventListener('keydown',e=>{
  if((e.key==='e'||e.key==='E')&&!(e.target.getAttribute&&e.target.getAttribute('contenteditable'))){editor.toggle();}
  if(e.key==='s'&&(e.metaKey||e.ctrlKey)&&editor.isActive){e.preventDefault();editor.save();}
});
