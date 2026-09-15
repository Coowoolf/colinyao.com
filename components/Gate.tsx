"use client";

import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

// 口令门 · 纸墨 × 砖印（与 /bema 品牌书同一套语汇：墨底 #161412 · 宣纸 #FCFBF8 · 陶土 #D8612B · 两块砖的印）
// 状态机：idle → checking → wrong（抖一下，再来）/ ok（砖叠上去 · 陶土幕布从左扫过 · reload 进 deck）
type Phase = "idle" | "checking" | "wrong" | "ok";

export default function Gate({ next }: { next: string }) {
  const [pass, setPass] = useState("");
  const [phase, setPhase] = useState<Phase>("idle");
  const [tries, setTries] = useState(0);
  const [mounted, setMounted] = useState(false);   // 挂到 body 上：站点 main 有自己的 stacking context，nav 的 z-index 会压过来
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setMounted(true);
    const t = setTimeout(() => inputRef.current?.focus(), 650);
    return () => clearTimeout(t);
  }, []);

  async function submit() {
    if (phase === "checking" || phase === "ok") return;
    const p = pass.trim();
    if (!p) { inputRef.current?.focus(); return; }
    setPhase("checking");
    try {
      const r = await fetch("/api/gate", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ pass: p }) });
      if (r.ok) {
        setPhase("ok");
        setTimeout(() => {
          const target = next && next.startsWith("/") ? next : "/";
          if (location.pathname === target) location.reload(); else location.assign(target);
        }, 1250);
        return;
      }
    } catch { /* 网络错也当作不对 */ }
    setTries((n) => n + 1);
    setPhase("wrong");
    setPass("");
    setTimeout(() => { setPhase("idle"); inputRef.current?.focus(); }, 900);
  }

  const status =
    phase === "checking" ? "……" :
    phase === "wrong" ? (tries >= 3 ? "还是不对。口令找 Colin 要。" : "不对。再来一次。") :
    phase === "ok" ? "好，上前一步。" :
    "输入口令 · 回车进入";

  const node = (
    <div className={`gate gate--${phase}`} role="dialog" aria-modal="true" aria-labelledby="gate-title">
      <style>{CSS}</style>
      <div className="gate-paper" aria-hidden="true" />
      <svg className="gate-flow" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <path className="l s1" d="M-100 720 C 300 640, 520 820, 900 730 S 1500 600, 2020 690" />
        <path className="l s2" d="M-100 300 C 260 240, 700 380, 1100 300 S 1700 220, 2020 280" />
        <path className="l s3" d="M-100 900 C 400 860, 800 960, 1300 900 S 1800 850, 2020 880" />
        <path className="l s4" d="M-100 140 C 500 200, 900 90, 1400 150 S 1800 190, 2020 130" />
      </svg>

      <div className="gate-chrome gate-in" style={{ animationDelay: ".15s" }}>
        <span>iRTE 2026 · 内部预览 · PRIVATE PREVIEW</span>
        <span>AN AGORA MODEL</span>
      </div>

      <form
        className="gate-card"
        onSubmit={(e) => { e.preventDefault(); void submit(); }}
        autoComplete="off"
      >
        <span className="gate-in" style={{ animationDelay: ".25s" }}><span className="gate-mk" aria-hidden="true"><i /><i /></span></span>
        <h1 id="gate-title" className="gate-wm gate-in" style={{ animationDelay: ".35s" }}>bema</h1>
        <p className="gate-line gate-in" style={{ animationDelay: ".55s" }}>上前一步，开口。</p>

        <div className="gate-in gate-fieldwrap" style={{ animationDelay: ".7s" }}>
        <label className="gate-field">
          <span className="gate-label">口令 · PASSPHRASE</span>
          <input
            ref={inputRef}
            type="password"
            name="pass"
            inputMode="text"
            autoCapitalize="off"
            autoCorrect="off"
            spellCheck={false}
            value={pass}
            disabled={phase === "ok"}
            onChange={(e) => setPass(e.target.value)}
            aria-describedby="gate-status"
            placeholder="········"
          />
          <button type="submit" className="gate-enter" aria-label="进入">
            <span>进入</span><b>↵</b>
          </button>
        </label>
        </div>
        <p id="gate-status" className="gate-status gate-in" style={{ animationDelay: ".85s" }} aria-live="polite">{status}</p>
      </form>

      <div className="gate-foot gate-in" style={{ animationDelay: ".15s" }}>
        <span>In the Agora, one steps up to speak.</span>
        <span>2026.10.24 · 北京</span>
      </div>

      <div className="gate-curtain" aria-hidden="true" />
    </div>
  );
  return mounted ? createPortal(node, document.body) : node;
}

const CSS = `
@font-face{font-family:'Urbanist';src:url('/fonts/Urbanist-700-bema.woff2') format('woff2');font-weight:700;font-display:swap;}
html:has(.gate) .nav,html:has(.gate) .footer,html:has(.gate) main>*:not(.gate){visibility:hidden;}
html:has(.gate){overflow:hidden;}
.gate{position:fixed;inset:0;z-index:10000;background:#161412;color:#F1ECE3;overflow:hidden;
  --paper:#FCFBF8;--clay:#D8612B;--clay-2:#F07A44;--ink-2:#CFC6BA;--ink-3:#8C8177;--hair:rgba(241,236,227,.14);--hair-strong:rgba(241,236,227,.30);
  --mono:'JetBrains Mono','SF Mono',ui-monospace,'PingFang SC',monospace;
  --cn:'Inter Tight',-apple-system,'PingFang SC','HarmonyOS Sans SC','Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif;
  --ease-flow:cubic-bezier(.22,.9,.24,1);
  font-family:var(--cn);-webkit-font-smoothing:antialiased;}
.gate-paper{position:absolute;inset:0;pointer-events:none;opacity:.55;mix-blend-mode:screen;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='360' height='360'><filter id='g'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .95 0 0 0 0 .93 0 0 0 0 .89 0 0 0 .07 0'/></filter><rect width='100%' height='100%' filter='url(%23g)'/></svg>");}
.gate-flow{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:.5;}
.gate-flow .l{fill:none;stroke:var(--hair-strong);stroke-width:1.2;stroke-linecap:round;stroke-dasharray:220 180;animation:gate-drift linear infinite;}
.gate-flow .s1{animation-duration:38s;stroke:rgba(216,97,43,.40);} .gate-flow .s2{animation-duration:52s;} .gate-flow .s3{animation-duration:64s;} .gate-flow .s4{animation-duration:46s;stroke:rgba(216,97,43,.28);}
@keyframes gate-drift{to{stroke-dashoffset:-1600;}}

.gate-chrome,.gate-foot{position:absolute;left:clamp(20px,4vw,72px);right:clamp(20px,4vw,72px);display:flex;justify-content:space-between;gap:16px;
  font:500 12px/1 var(--mono);letter-spacing:.22em;text-transform:uppercase;color:var(--ink-3);}
.gate-chrome{top:clamp(20px,3.6vw,44px);} .gate-foot{bottom:clamp(20px,3.6vw,44px);text-transform:none;letter-spacing:.12em;}
@media (max-width:640px){.gate-chrome span:last-child,.gate-foot span:last-child{display:none;}}

.gate-card{position:absolute;left:50%;top:50%;transform:translate(-50%,-52%);width:min(560px,88vw);display:flex;flex-direction:column;align-items:flex-start;}
.gate-in{animation:gate-in .95s var(--ease-flow) both;}
.gate-fieldwrap{width:100%;}
.gate-mk{display:flex;align-items:flex-end;gap:0;height:44px;margin-bottom:26px;}
.gate-mk i{display:block;width:64px;height:16px;background:var(--clay);transition:transform .7s var(--ease-flow);}
.gate-mk i:first-child{transform:translateY(0);} .gate-mk i:last-child{transform:translate(-30px,-16px);}
.gate--ok .gate-mk i:last-child{transform:translate(0,-17px);}
.gate--wrong .gate-mk{animation:gate-shake .5s var(--ease-flow) both;}
.gate-wm{margin:0;font:700 clamp(96px,16vw,168px)/.86 'Urbanist','Inter Tight',sans-serif;letter-spacing:-.035em;color:var(--paper);font-feature-settings:"kern" 1;}
.gate-line{margin:22px 0 40px;font:400 clamp(18px,2.2vw,22px)/1.5 var(--cn);color:var(--ink-2);letter-spacing:.02em;}
.gate-field{position:relative;display:flex;align-items:flex-end;gap:14px;width:100%;padding:14px 0 12px;border-bottom:1px solid var(--hair-strong);transition:border-color .35s;}
.gate-field:focus-within{border-bottom-color:var(--clay);}
.gate--wrong .gate-field{border-bottom-color:var(--clay);animation:gate-shake .5s var(--ease-flow) both;}
.gate-label{position:absolute;left:0;top:-12px;font:700 11px/1 var(--mono);letter-spacing:.26em;text-transform:uppercase;color:var(--clay-2);}
.gate-field input{flex:1;min-width:0;background:transparent;border:0;outline:0;color:var(--paper);caret-color:var(--clay);
  font:500 clamp(24px,3.4vw,30px)/1.2 var(--mono);letter-spacing:.24em;padding:6px 0 2px;}
.gate-field input::placeholder{color:var(--ink-3);opacity:.7;letter-spacing:.3em;}
.gate-field input:disabled{opacity:.5;}
.gate-enter{flex:none;display:inline-flex;align-items:center;gap:10px;background:transparent;border:0;cursor:pointer;padding:6px 0 4px;
  font:700 12px/1 var(--mono);letter-spacing:.22em;text-transform:uppercase;color:var(--ink-3);transition:color .3s;}
.gate-enter b{font:700 18px/1 var(--mono);color:var(--clay);transition:transform .35s var(--ease-flow);}
.gate-enter:hover,.gate-field:focus-within .gate-enter{color:var(--paper);} .gate-enter:hover b{transform:translateX(3px);}
.gate-status{margin:16px 0 0;min-height:18px;font:500 12px/1.5 var(--mono);letter-spacing:.14em;color:var(--ink-3);transition:color .3s;}
.gate--wrong .gate-status{color:var(--clay-2);}
.gate--ok .gate-status{color:var(--paper);}
.gate--checking .gate-status{color:var(--ink-2);}

.gate-curtain{position:absolute;inset:0;background:var(--clay);transform:translateX(-101%);pointer-events:none;
  transition:transform .95s var(--ease-flow);}
.gate--ok .gate-curtain{transform:translateX(0);transition-delay:.35s;}
.gate--ok .gate-card{transition:opacity .5s var(--ease-flow) .25s,transform .9s var(--ease-flow) .25s;opacity:0;transform:translate(-50%,-58%);}

@keyframes gate-in{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:none;}}
@keyframes gate-shake{0%,100%{transform:translateX(0);}18%{transform:translateX(-9px);}36%{transform:translateX(8px);}54%{transform:translateX(-5px);}72%{transform:translateX(3px);}}
@media (prefers-reduced-motion:reduce){.gate *{animation-duration:.01ms!important;transition-duration:.2s!important;}.gate-flow{display:none;}}
`;
