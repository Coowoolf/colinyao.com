import type { CSSProperties } from "react";

const v = (n: number, i: number) => ({ ["--len" as string]: n, ["--i" as string]: i } as CSSProperties);
const p = (i: number) => ({ ["--i" as string]: i } as CSSProperties);

/** Idea 卡片母题图（一图胜千言：线条自绘 + 图元浮起） */
export default function Motif({ kind }: { kind: string }) {
  switch (kind) {
    case "ruler":
      return (
        <svg viewBox="0 0 220 64" fill="none" aria-hidden="true">
          <path className="dw" style={v(200, 2)} d="M12 36 H208" stroke="var(--hair-strong)" strokeWidth="1.4" />
          <path className="dw" style={v(140, 3)} d="M40 36 v-8 M68 36 v-5 M96 36 v-8 M124 36 v-5 M152 36 v-8 M180 36 v-5" stroke="var(--ink-3)" strokeWidth="1.2" />
          <path className="dw" style={v(24, 4)} d="M110 46 V22" stroke="var(--coral)" strokeWidth="2" />
          <path className="dw" style={v(30, 5)} d="M20 29 L12 36 L20 43" stroke="var(--amber)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(30, 5)} d="M200 29 L208 36 L200 43" stroke="var(--coral)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    case "wave":
      return (
        <svg viewBox="0 0 220 64" fill="none" aria-hidden="true">
          <path className="dw" style={v(90, 2)} d="M8 32 H84" stroke="var(--ink-3)" strokeWidth="1.4" strokeDasharray="3 6" />
          <path className="dw" style={v(220, 3)}
            d="M84 32 C 90 32, 92 18, 98 18 S 106 44, 112 44 S 120 10, 126 10 S 134 50, 140 50 S 148 22, 154 22 S 160 36, 166 32"
            stroke="var(--amber)" strokeWidth="1.8" strokeLinecap="round" />
          <path className="dw" style={v(50, 5)} d="M166 32 H212" stroke="var(--amber)" strokeWidth="1.8" strokeLinecap="round" />
          <circle className="pop" style={p(6)} cx="212" cy="32" r="3.5" fill="var(--amber)" />
        </svg>
      );
    case "hemis":
      return (
        <svg viewBox="0 0 220 64" fill="none" aria-hidden="true">
          <circle className="dw" style={v(140, 2)} cx="62" cy="30" r="21" stroke="var(--ink-2)" strokeWidth="1.4" />
          <circle className="dw" style={v(140, 3)} cx="158" cy="30" r="21" stroke="var(--ink-2)" strokeWidth="1.4" />
          <path className="dw" style={v(40, 4)} d="M83 30 H137" stroke="var(--hair-strong)" strokeWidth="1.2" />
          <circle className="pop" style={p(5)} cx="110" cy="30" r="4.5" fill="var(--amber)" />
          <text className="pop" style={p(6)} x="62" y="62" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="8.5" letterSpacing="1.5" textAnchor="middle">像人</text>
          <text className="pop" style={p(6)} x="158" y="62" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="8.5" letterSpacing="1.5" textAnchor="middle">像系统</text>
        </svg>
      );
    case "bounds":
      return (
        <svg viewBox="0 0 220 64" fill="none" aria-hidden="true">
          <path className="dw" style={v(200, 2)} d="M12 14 H208" stroke="var(--ink-3)" strokeWidth="1.3" strokeDasharray="6 6" />
          <path className="dw" style={v(200, 3)} d="M12 50 H208" stroke="var(--magenta)" strokeWidth="2" />
          <path className="dw" style={v(40, 5)} d="M110 22 V42 M104 36 L110 42 L116 36" stroke="var(--ink-2)" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
          <text className="pop" style={p(6)} x="14" y="28" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="8.5" letterSpacing="1.5">CEILING · 模型</text>
          <text className="pop" style={p(7)} x="208" y="44" fill="var(--magenta)" fontFamily="var(--mono)" fontSize="8.5" letterSpacing="1.5" textAnchor="end">FLOOR · 引擎</text>
        </svg>
      );
    case "sota":
      return (
        <svg viewBox="0 0 220 64" fill="none" aria-hidden="true">
          <path className="dw" style={v(30, 2)} d="M30 54 V40" stroke="var(--ink-3)" strokeWidth="7" />
          <path className="dw" style={v(40, 3)} d="M66 54 V32" stroke="var(--ink-3)" strokeWidth="7" />
          <path className="dw" style={v(50, 4)} d="M102 54 V24" stroke="var(--ink-2)" strokeWidth="7" />
          <path className="dw" style={v(60, 5)} d="M138 54 V14" stroke="var(--amber)" strokeWidth="7" />
          <path className="dw" style={v(60, 7)} d="M160 24 L200 24" stroke="var(--hair-strong)" strokeWidth="1.2" strokeDasharray="3 5" />
          <text className="pop" style={p(8)} x="200" y="16" fill="var(--amber)" fontFamily="var(--mono)" fontSize="9" letterSpacing="2" textAnchor="end">SOTA</text>
        </svg>
      );
    case "qoi":
      return (
        <svg viewBox="0 0 220 64" fill="none" aria-hidden="true">
          <path className="dw" style={v(260, 2)} d="M12 54 H70 V38 H140 V20 H208" stroke="var(--ink-2)" strokeWidth="1.6" />
          <text className="pop" style={p(4)} x="40" y="48" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="9" letterSpacing="1" textAnchor="middle">QoS</text>
          <text className="pop" style={p(5)} x="105" y="32" fill="var(--ink-2)" fontFamily="var(--mono)" fontSize="9" letterSpacing="1" textAnchor="middle">QoE</text>
          <text className="pop" style={p(6)} x="174" y="14" fill="var(--amber)" fontFamily="var(--mono)" fontSize="10" letterSpacing="1" textAnchor="middle">QoI</text>
        </svg>
      );
    case "steps":
      return (
        <svg viewBox="0 0 220 64" fill="none" aria-hidden="true">
          <path className="dw" style={v(220, 2)} d="M14 52 C 60 50, 120 40, 206 14" stroke="var(--hair-strong)" strokeWidth="1.2" />
          <circle className="pop" style={p(3)} cx="14" cy="52" r="3" fill="var(--ink-3)" />
          <circle className="pop" style={p(4)} cx="78" cy="47" r="3" fill="var(--ink-3)" />
          <circle className="pop" style={p(5)} cx="142" cy="36" r="3" fill="var(--ink-2)" />
          <circle className="pop" style={p(6)} cx="206" cy="14" r="5" fill="var(--amber)" />
          <text className="pop" style={p(7)} x="206" y="34" fill="var(--amber)" fontFamily="var(--mono)" fontSize="8.5" letterSpacing="1.5" textAnchor="end">得心</text>
        </svg>
      );
    case "tb":
      return <div className="big settle" style={p(2)}>0.29 TB</div>;
    default:
      return null;
  }
}
