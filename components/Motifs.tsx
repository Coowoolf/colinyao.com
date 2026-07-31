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
    case "evalprd":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <rect className="dw" style={v(300, 2)} x="36" y="30" width="110" height="100" rx="4" stroke="var(--ink-2)" strokeWidth="2" />
          <path className="dw" style={v(160, 3)} d="M54 54 H128 M54 74 H128 M54 94 H108" stroke="var(--ink-3)" strokeWidth="2" />
          <path className="dw" style={v(80, 4)} d="M176 80 H240 M228 68 L242 80 L228 92" stroke="var(--amber)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(180, 5)} d="M268 96 H428" stroke="var(--hair-strong)" strokeWidth="2" />
          <path className="mlive slow" d="M268 96 H428" stroke="var(--amber)" strokeWidth="2" opacity=".8" />
          <path className="dw" style={v(160, 6)} d="M292 96 v-16 M324 96 v-24 M356 96 v-16 M388 96 v-24 M416 96 v-16" stroke="var(--ink-2)" strokeWidth="2.2" />
          <circle className="pop dlive" style={p(7)} cx="428" cy="96" r="5" fill="var(--amber)" />
          {T && <text className="pop" style={p(6)} x="36" y="150" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">PRD</text>}
          {T && <text className="pop" style={p(7)} x="428" y="150" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">EVAL · 可复用的尺子</text>}
        </svg>
      );
    case "turnsx":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(40, 2)} d="M48 62 L60 76 L84 48" stroke="var(--ink-2)" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(40, 3)} d="M128 62 L140 76 L164 48" stroke="var(--ink-2)" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(40, 4)} d="M208 62 L220 76 L244 48" stroke="var(--ink-2)" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(40, 5)} d="M288 62 L300 76 L324 48" stroke="var(--ink-2)" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(420, 6)} d="M40 112 C 140 96, 300 96, 372 108" stroke="var(--hair-strong)" strokeWidth="2" strokeDasharray="5 8" />
          <path className="mlive" d="M40 112 C 140 96, 300 96, 372 108" stroke="var(--coral)" strokeWidth="2" opacity=".7" />
          <path className="dw" style={v(70, 7)} d="M388 94 L424 130 M424 94 L388 130" stroke="var(--coral)" strokeWidth="3.4" strokeLinecap="round" />
          {T && <text className="pop" style={p(7)} x="40" y="30" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">每一轮 · 对</text>}
          {T && <text className="pop" style={p(8)} x="424" y="152" fill="var(--coral)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">整段 · 错</text>}
        </svg>
      );
    case "notmodel":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <circle className="dw" style={v(160, 2)} cx="86" cy="72" r="26" stroke="var(--ink-3)" strokeWidth="2" strokeDasharray="4 7" />
          <path className="dw" style={v(200, 3)} d="M124 72 H180 M180 30 V114 M180 30 H340 M180 114 H340" stroke="var(--ink-2)" strokeWidth="2" />
          <path className="dw" style={v(220, 4)} d="M212 30 V114 M244 30 V114 M276 30 V114 M308 30 V114" stroke="var(--hair-strong)" strokeWidth="1.6" />
          <path className="mlive slow" d="M124 72 H180 M180 72 H424" stroke="var(--magenta)" strokeWidth="2.2" opacity=".85" />
          <path className="dw" style={v(120, 5)} d="M340 30 L388 72 L340 114" stroke="var(--magenta)" strokeWidth="2.4" strokeLinejoin="round" />
          <circle className="pop dlive" style={p(6)} cx="424" cy="72" r="6" fill="var(--magenta)" />
          {T && <text className="pop" style={p(6)} x="86" y="128" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="middle">MODEL</text>}
          {T && <text className="pop" style={p(7)} x="424" y="128" fill="var(--magenta)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">架构 · 流程 · 工程</text>}
        </svg>
      );
    case "gold5":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(360, 2)} d="M230 22 L296 66 L272 134 L188 134 L164 66 Z" stroke="var(--hair-strong)" strokeWidth="1.8" />
          <path className="dw" style={v(300, 3)} d="M230 22 L230 84 M296 66 L230 84 M272 134 L230 84 M188 134 L230 84 M164 66 L230 84" stroke="var(--ink-3)" strokeWidth="1.4" />
          <path className="dw" style={v(300, 4)} d="M230 40 L278 70 L260 122 L200 122 L182 70 Z" stroke="var(--amber)" strokeWidth="2.4" strokeLinejoin="round" />
          <path className="mlive slow" d="M230 40 L278 70 L260 122 L200 122 L182 70 Z" stroke="var(--amber)" strokeWidth="2" opacity=".7" />
          <circle className="pop dlive" style={p(5)} cx="230" cy="40" r="4.5" fill="var(--amber)" />
          <circle className="pop dlive" style={p(6)} cx="278" cy="70" r="4.5" fill="var(--amber)" />
          <circle className="pop dlive" style={p(7)} cx="182" cy="70" r="4.5" fill="var(--amber)" />
          {T && <text className="pop" style={p(6)} x="330" y="60" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">5 BARS</text>}
          {T && <text className="pop" style={p(7)} x="330" y="82" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">一起达标</text>}
        </svg>
      );
    case "settle72":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(420, 2)} d="M28 92 H432" stroke="var(--hair-strong)" strokeWidth="2" />
          <path className="dw" style={v(120, 3)} d="M48 92 C 60 60, 74 60, 86 92 C 98 124, 112 124, 124 92" stroke="var(--ink-2)" strokeWidth="2.2" />
          <path className="dw" style={v(200, 4)} d="M140 92 H360" stroke="var(--ink-3)" strokeWidth="2" strokeDasharray="4 10" />
          <path className="mlive slow" d="M140 92 H396" stroke="var(--amber)" strokeWidth="2" opacity=".75" />
          <path className="dw" style={v(40, 5)} d="M396 78 V106" stroke="var(--amber)" strokeWidth="2.6" />
          <circle className="pop dlive" style={p(6)} cx="396" cy="92" r="7" fill="var(--amber)" />
          {T && <text className="pop" style={p(6)} x="48" y="132" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">对话结束</text>}
          {T && <text className="pop" style={p(7)} x="396" y="60" fill="var(--amber)" fontFamily="var(--mono)" fontSize="13" letterSpacing="2.5" textAnchor="middle">+72H · 结算</text>}
        </svg>
      );
    case "triad":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <circle className="dw" style={v(260, 2)} cx="186" cy="62" r="40" stroke="var(--ink-2)" strokeWidth="2" />
          <circle className="dw" style={v(260, 3)} cx="274" cy="62" r="40" stroke="var(--ink-2)" strokeWidth="2" />
          <circle className="dw" style={v(260, 4)} cx="230" cy="112" r="40" stroke="var(--ink-2)" strokeWidth="2" />
          <circle className="mlive slow" cx="230" cy="112" r="40" stroke="var(--amber)" strokeWidth="2" opacity=".7" />
          <circle className="pop dlive" style={p(5)} cx="230" cy="78" r="7" fill="var(--amber)" />
          {T && <text className="pop" style={p(6)} x="112" y="36" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">身份</text>}
          {T && <text className="pop" style={p(6)} x="348" y="36" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">关系</text>}
          {T && <text className="pop" style={p(7)} x="348" y="140" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">历史 + 实时引擎</text>}
        </svg>
      );
    case "agency":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(380, 2)} d="M60 110 L400 66" stroke="var(--ink-2)" strokeWidth="2.4" />
          <path className="dw" style={v(60, 3)} d="M230 132 L214 152 M230 132 L246 152 M230 88 V132" stroke="var(--ink-3)" strokeWidth="2.2" />
          <circle className="pop" style={p(4)} cx="92" cy="120" r="5" fill="var(--ink-3)" />
          <circle className="pop" style={p(5)} cx="116" cy="122" r="5" fill="var(--ink-3)" />
          <circle className="pop" style={p(6)} cx="140" cy="118" r="5" fill="var(--ink-3)" />
          <circle className="pop dlive" style={p(7)} cx="382" cy="52" r="10" fill="var(--amber)" />
          <path className="mlive slow" d="M60 110 L400 66" stroke="var(--amber)" strokeWidth="1.8" opacity=".6" />
          {T && <text className="pop" style={p(7)} x="60" y="150" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">执行 · 变便宜</text>}
          {T && <text className="pop" style={p(8)} x="400" y="30" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">HIGH AGENCY · 变贵</text>}
        </svg>
      );
    case "compound":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(420, 2)} d="M36 132 H428 M36 132 V28" stroke="var(--hair-strong)" strokeWidth="1.8" />
          <path className="dw" style={v(430, 3)} d="M36 128 C 140 126, 220 120, 280 100 C 340 80, 390 48, 424 26" stroke="var(--amber)" strokeWidth="2.6" strokeLinecap="round" />
          <path className="mlive" d="M36 128 C 140 126, 220 120, 280 100 C 340 80, 390 48, 424 26" stroke="#fffffe" strokeWidth="1.8" opacity=".55" />
          <path className="dw" style={v(120, 5)} d="M120 128 v6 M204 122 v6 M288 98 v6 M372 58 v6" stroke="var(--ink-3)" strokeWidth="2" />
          <circle className="pop dlive" style={p(6)} cx="424" cy="26" r="6" fill="var(--amber)" />
          {T && <text className="pop" style={p(6)} x="36" y="152" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">不下班 · 恒动</text>}
          {T && <text className="pop" style={p(7)} x="424" y="52" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">复利</text>}
        </svg>
      );
    case "timefx":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(90, 2)} d="M60 46 H144" stroke="var(--ink-2)" strokeWidth="6" strokeLinecap="round" />
          <path className="dw" style={v(360, 3)} d="M60 118 H420" stroke="var(--amber)" strokeWidth="6" strokeLinecap="round" />
          <path className="mlive slow" d="M60 118 H420" stroke="#fffffe" strokeWidth="2" opacity=".5" />
          <path className="dw" style={v(160, 4)} d="M64 54 L64 110 M104 54 L232 110 M144 54 L416 110" stroke="var(--hair-strong)" strokeWidth="1.4" strokeDasharray="3 7" />
          <circle className="pop dlive" style={p(6)} cx="420" cy="118" r="6" fill="var(--amber)" />
          {T && <text className="pop" style={p(5)} x="160" y="50" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">人间 · 3 天</text>}
          {T && <text className="pop" style={p(7)} x="420" y="146" fill="var(--amber)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">CLAUDE · 3 年</text>}
        </svg>
      );
    case "cowork":
      return (
        <svg viewBox="0 0 460 160" fill="none" aria-hidden="true">
          <path className="dw" style={v(180, 2)} d="M48 80 H200 M184 64 L204 80 L184 96" stroke="var(--ink-2)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
          <path className="dw" style={v(180, 3)} d="M412 80 H260 M276 64 L256 80 L276 96" stroke="var(--coral)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
          <path className="mlive slow" d="M48 80 H204" stroke="var(--ink-2)" strokeWidth="1.8" opacity=".5" />
          <path className="mlive slow" d="M412 80 H256" stroke="var(--coral)" strokeWidth="1.8" opacity=".7" />
          <circle className="dw" style={v(140, 4)} cx="230" cy="80" r="20" stroke="var(--coral)" strokeWidth="2" strokeDasharray="4 6" />
          <circle className="pop dlive" style={p(5)} cx="230" cy="80" r="5" fill="var(--coral)" />
          {T && <text className="pop" style={p(6)} x="48" y="128" fill="var(--ink-3)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5">被托付 · 单向</text>}
          {T && <text className="pop" style={p(7)} x="412" y="128" fill="var(--coral)" fontFamily="var(--mono)" fontSize="12" letterSpacing="2.5" textAnchor="end">共事 · 双向奔赴 · 2026.08</text>}
        </svg>
      );
    default:
      return null;

  }
}
