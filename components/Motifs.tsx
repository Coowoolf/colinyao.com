import type { CSSProperties } from "react";

const v = (n: number, i: number) => ({ ["--len" as string]: n, ["--i" as string]: i } as CSSProperties);
const p = (i: number) => ({ ["--i" as string]: i } as CSSProperties);

/**
 * Idea 卡片母题图 · 460×160 大图版（卡片的视觉主角，不是装饰条）
 * 线条自绘入场（.dw）+ 标注浮起（.pop）+ 持续流动光（.mlive）/ 呼吸点（.dlive）
 * plain 模式：隐藏文字标注（用于数字带等缩小场景，避免文字糊成噪点）
 */
export default function Motif({ kind, plain = false }: { kind: string; plain?: boolean }) {
  const T = !plain; // 是否渲染文字标注
  switch (kind) {
    case "ruler":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(420, 2)} d="M28 84 H432" stroke="var(--hair-strong)" strokeWidth="2" />
          <path className="mlive slow" d="M230 84 H432" stroke="var(--coral)" strokeWidth="2" opacity=".8" />
          <path className="mlive slow" d="M230 84 H28" stroke="var(--amber)" strokeWidth="2" opacity=".8" />
          <path className="dw" style={v(300, 3)} d="M76 84 v-20 M124 84 v-12 M172 84 v-20 M220 84 v-12" stroke="var(--ink-3)" strokeWidth="2" />
          <path className="dw" style={v(300, 4)} d="M268 84 v-12 M316 84 v-20 M364 84 v-12 M412 84 v-20" stroke="var(--ink-3)" strokeWidth="2" />
          <path className="dw" style={v(60, 5)} d="M230 108 V50" stroke="var(--coral)" strokeWidth="3" />
          <circle className="pop dlive" style={p(7)} cx="230" cy="42" r="5" fill="var(--coral)" />
          <path className="dw" style={v(50, 6)} d="M42 70 L26 84 L42 98" stroke="var(--amber)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(50, 6)} d="M418 70 L434 84 L418 98" stroke="var(--coral)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
          {T && <text className="pop" style={p(7)} x="28" y="132" fill="var(--amber)" fontFamily="var(--mono)" fontSize="13" letterSpacing="3">EVAL · 向外</text>}
          {T && <text className="pop" style={p(7)} x="432" y="132" fill="var(--coral)" fontFamily="var(--mono)" fontSize="13" letterSpacing="3" textAnchor="end">内观 · 向内</text>}
        </svg>
      );
    case "wave":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(130, 2)} d="M24 80 H140" stroke="var(--ink-3)" strokeWidth="2" strokeDasharray="4 9" />
          <path className="dw" style={v(200, 6)} d="M150 96 C 168 96, 174 118, 190 118 S 214 74, 228 74 S 250 120, 264 118 S 288 82, 300 86"
            stroke="var(--ink-3)" strokeWidth="1.6" opacity=".35" />
          <path className="dw" style={v(340, 3)}
            d="M140 80 C 156 80, 162 36, 178 36 S 200 124, 214 124 S 234 20, 248 20 S 270 136, 284 136 S 306 52, 320 52 S 336 88, 350 80"
            stroke="var(--amber)" strokeWidth="2.6" strokeLinecap="round" />
          <path className="mlive" d="M140 80 C 156 80, 162 36, 178 36 S 200 124, 214 124 S 234 20, 248 20 S 270 136, 284 136 S 306 52, 320 52 S 336 88, 350 80 H436"
            stroke="#fffffe" strokeWidth="2" opacity=".65" />
          <path className="dw" style={v(100, 5)} d="M350 80 H436" stroke="var(--amber)" strokeWidth="2.6" strokeLinecap="round" />
          <circle className="pop dlive" style={p(6)} cx="436" cy="80" r="6" fill="var(--amber)" />
          {T && <text className="pop" style={p(7)} x="24" y="132" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">SIGNAL</text>}
          {T && <text className="pop" style={p(7)} x="436" y="132" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">ALIVE</text>}
        </svg>
      );
    case "hemis":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <circle className="dw" style={v(340, 2)} cx="140" cy="72" r="52" stroke="var(--ink-2)" strokeWidth="2" />
          <circle className="dw" style={v(340, 3)} cx="320" cy="72" r="52" stroke="var(--ink-2)" strokeWidth="2" />
          <circle className="mlive slow" cx="140" cy="72" r="52" stroke="var(--amber)" strokeWidth="2.2" opacity=".9" />
          <circle className="mlive slow" cx="320" cy="72" r="52" stroke="var(--coral)" strokeWidth="2.2" opacity=".9" />
          <path className="dw" style={v(100, 4)} d="M192 72 H268" stroke="var(--hair-strong)" strokeWidth="1.8" />
          <circle className="pop dlive" style={p(5)} cx="230" cy="72" r="8" fill="var(--amber)" />
          <path className="dw" style={v(260, 6)} d="M110 128 C 160 150, 300 150, 350 128" stroke="var(--hair-strong)" strokeWidth="1.4" strokeDasharray="3 8" />
          {T && <text className="pop" style={p(6)} x="140" y="150" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="middle">像人 · 被记住</text>}
          {T && <text className="pop" style={p(6)} x="320" y="150" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="middle">像系统 · 被托付</text>}
        </svg>
      );
    case "bounds":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(420, 2)} d="M24 36 H436" stroke="var(--ink-3)" strokeWidth="2" strokeDasharray="9 9" />
          <path className="dw" style={v(420, 3)} d="M24 118 H436" stroke="var(--magenta)" strokeWidth="3" />
          <path className="mlive" d="M24 118 H436" stroke="#fffffe" strokeWidth="2" opacity=".55" />
          <path className="dw" style={v(90, 5)} d="M230 48 V104 M218 92 L230 106 L242 92" stroke="var(--ink-2)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
          <circle className="pop dlive" style={p(7)} cx="352" cy="118" r="5" fill="var(--magenta)" />
          {T && <text className="pop" style={p(6)} x="24" y="22" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">CEILING · 模型 · 大家都在卷</text>}
          {T && <text className="pop" style={p(7)} x="436" y="144" fill="var(--magenta)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">FLOOR · 引擎 · 流失发生地</text>}
        </svg>
      );
    case "sota":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(50, 2)} d="M56 132 V102" stroke="var(--ink-3)" strokeWidth="15" />
          <path className="dw" style={v(70, 3)} d="M124 132 V84" stroke="var(--ink-3)" strokeWidth="15" />
          <path className="dw" style={v(90, 4)} d="M192 132 V62" stroke="var(--ink-2)" strokeWidth="15" />
          <path className="dw" style={v(110, 5)} d="M260 132 V40" stroke="var(--ink-2)" strokeWidth="15" />
          <path className="dw dlive" style={v(130, 6)} d="M328 132 V22" stroke="var(--amber)" strokeWidth="15" />
          <path className="dw" style={v(110, 8)} d="M352 22 H436" stroke="var(--hair-strong)" strokeWidth="1.6" strokeDasharray="4 7" />
          {T && <text className="pop" style={p(9)} x="436" y="46" fill="var(--amber)" fontFamily="var(--mono)" fontSize="14" letterSpacing="3" textAnchor="end">SOTA</text>}
          {T && <text className="pop" style={p(9)} x="56" y="152" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="middle">BENCH</text>}
          {T && <text className="pop" style={p(10)} x="328" y="152" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="middle">VIBE</text>}
        </svg>
      );
    case "qoi":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(560, 2)} d="M24 132 H140 V88 H280 V40 H436" stroke="var(--ink-2)" strokeWidth="2.4" />
          <path className="mlive" d="M24 132 H140 V88 H280 V40 H436" stroke="var(--amber)" strokeWidth="2.6" opacity=".9" />
          <circle className="pop dlive" style={p(7)} cx="436" cy="40" r="6" fill="var(--amber)" />
          {T && <text className="pop" style={p(4)} x="82" y="118" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="14" letterSpacing="2" textAnchor="middle">QoS</text>}
          {T && <text className="pop" style={p(5)} x="210" y="74" fill="var(--ink-2)" fontFamily="var(--mono)" fontSize="14" letterSpacing="2" textAnchor="middle">QoE</text>}
          {T && <text className="pop" style={p(6)} x="352" y="26" fill="var(--amber)" fontFamily="var(--mono)" fontSize="15" letterSpacing="2" textAnchor="middle">QoI</text>}
          {T && <text className="pop" style={p(8)} x="82" y="152" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="11" letterSpacing="2" textAnchor="middle">为传输</text>}
          {T && <text className="pop" style={p(8)} x="210" y="152" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="11" letterSpacing="2" textAnchor="middle">为人</text>}
          {T && <text className="pop" style={p(9)} x="352" y="152" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="11" letterSpacing="2" textAnchor="middle">为人模共演</text>}
        </svg>
      );
    case "steps":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(460, 2)} d="M24 128 C 120 124, 250 96, 436 28" stroke="var(--hair-strong)" strokeWidth="1.8" />
          <path className="mlive" d="M24 128 C 120 124, 250 96, 436 28" stroke="var(--amber)" strokeWidth="2.2" opacity=".85" />
          <circle className="pop" style={p(3)} cx="24" cy="128" r="6" fill="var(--ink-3)" />
          <circle className="pop" style={p(4)} cx="160" cy="118" r="6" fill="var(--ink-3)" />
          <circle className="pop" style={p(5)} cx="296" cy="88" r="6" fill="var(--ink-2)" />
          <circle className="pop dlive" style={p(6)} cx="436" cy="28" r="9" fill="var(--amber)" />
          {T && <text className="pop" style={p(4)} x="24" y="152" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2" textAnchor="middle">听得到</text>}
          {T && <text className="pop" style={p(5)} x="160" y="146" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2" textAnchor="middle">听得清</text>}
          {T && <text className="pop" style={p(6)} x="296" y="116" fill="var(--ink-2)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2" textAnchor="middle">听得懂</text>}
          {T && <text className="pop" style={p(7)} x="424" y="60" fill="var(--amber)" fontFamily="var(--mono)" fontSize="13" letterSpacing="2" textAnchor="end">听得心</text>}
        </svg>
      );
    case "tb":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <circle className="dw" style={v(360, 2)} cx="96" cy="80" r="54" stroke="var(--amber)" strokeWidth="2.2" />
          <circle className="dw" style={v(240, 3)} cx="96" cy="80" r="38" stroke="var(--hair-strong)" strokeWidth="1.4" strokeDasharray="4 8" />
          <circle className="mlive slow" cx="96" cy="80" r="54" stroke="#fffffe" strokeWidth="2" opacity=".65" />
          <circle className="pop dlive" style={p(5)} cx="96" cy="80" r="7" fill="var(--amber)" />
          {T && <text className="pop" style={p(4)} x="180" y="96" fill="var(--amber)" fontFamily="var(--mono)" fontSize="52" fontWeight="700" letterSpacing="-1">0.29 TB</text>}
          {!T && <text className="pop" style={p(4)} x="180" y="100" fill="var(--amber)" fontFamily="var(--mono)" fontSize="56" fontWeight="700">0.29</text>}
          {T && <text className="pop" style={p(6)} x="182" y="128" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">一生的生命上下文 · 21G 灵魂</text>}
        </svg>
      );
    default:
      return null;
  }
}
