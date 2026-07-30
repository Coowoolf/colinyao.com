/** 首屏图腾：同一把尺子，两个方向。线条自绘（.dw），标注随后浮起（.pop）。 */
export default function RulerFig() {
  return (
    <svg className="hero-ruler" viewBox="0 0 680 130" fill="none" aria-hidden="true">
      {/* 主尺 */}
      <path className="dw" style={{ ["--len" as string]: 660, ["--i" as string]: 4 } as React.CSSProperties}
        d="M30 70 H650" stroke="var(--hair-strong)" strokeWidth="1.5" />
      {/* 持续流动的光：从原点分别流向 Eval 与内观 */}
      <path className="mlive slow" d="M340 70 H650" stroke="var(--coral)" strokeWidth="1.6" opacity=".75" />
      <path className="mlive slow" d="M340 70 H30" stroke="var(--amber)" strokeWidth="1.6" opacity=".75" />
      {/* 刻度（两段错峰） */}
      <path className="dw" style={{ ["--len" as string]: 320, ["--i" as string]: 6 } as React.CSSProperties}
        d="M70 70 v-12 M110 70 v-8 M150 70 v-8 M190 70 v-12 M230 70 v-8 M270 70 v-8 M310 70 v-12"
        stroke="var(--ink-3)" strokeWidth="1.4" />
      <path className="dw" style={{ ["--len" as string]: 320, ["--i" as string]: 7 } as React.CSSProperties}
        d="M370 70 v-12 M410 70 v-8 M450 70 v-8 M490 70 v-12 M530 70 v-8 M570 70 v-8 M610 70 v-12"
        stroke="var(--ink-3)" strokeWidth="1.4" />
      {/* 原点 */}
      <path className="dw" style={{ ["--len" as string]: 40, ["--i" as string]: 8 } as React.CSSProperties}
        d="M340 88 V48" stroke="var(--amber)" strokeWidth="2.2" />
      {/* 两端箭头 */}
      <path className="dw" style={{ ["--len" as string]: 60, ["--i" as string]: 9 } as React.CSSProperties}
        d="M46 58 L30 70 L46 82" stroke="var(--amber)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      <path className="dw" style={{ ["--len" as string]: 60, ["--i" as string]: 9 } as React.CSSProperties}
        d="M634 58 L650 70 L634 82" stroke="var(--coral)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      {/* 标注 */}
      <text className="pop" style={{ ["--i" as string]: 10 } as React.CSSProperties}
        x="30" y="34" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="3">
        EVAL · 向外
      </text>
      <text className="pop" style={{ ["--i" as string]: 10 } as React.CSSProperties}
        x="650" y="34" fill="var(--coral)" fontFamily="var(--mono)" fontSize="12" letterSpacing="3" textAnchor="end">
        内观 · 向内
      </text>
      <text className="pop" style={{ ["--i" as string]: 11 } as React.CSSProperties}
        x="340" y="122" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="10" letterSpacing="4" textAnchor="middle">
        THE SAME RULER
      </text>
    </svg>
  );
}
