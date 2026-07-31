"use client";

import { useState, useRef } from "react";
import { rays, rulerMeta, bindPin, type Ray, type Station, type BoundPin } from "@/content/ruler";

/** ============================================================
 *  时空内外 · 四把尺子 —— 星盘渲染器
 *  度盘环（双层反向慢转）/ 真刻度齿 / 射线渐变 + 流光 /
 *  辉光钉图 / 原点涟漪 / 幽灵大字
 *  状态由外层通过 data-dim / data-fold 驱动，CSS 过渡负责流动。
 *  ============================================================ */

export const VB = { w: 1680, h: 1240 };
export const C = { x: VB.w / 2, y: VB.h / 2 };

export const RADII: Record<Ray["id"], number[]> = {
  out: [170, 278, 386, 494, 602],
  inw: [170, 278, 386, 494, 602],
  time: [130, 195, 260, 325, 390, 455],
  space: [135, 215, 295, 375, 455],
};
export const DIR: Record<Ray["id"], [number, number]> = {
  out: [-1, 0],
  inw: [1, 0],
  time: [0, -1],
  space: [0, 1],
};

export function stationXY(rayId: Ray["id"], idx: number) {
  const r = RADII[rayId][idx];
  const [dx, dy] = DIR[rayId];
  return { x: C.x + dx * r, y: C.y + dy * r };
}

/** 格环：过四条射线第 k 站的圆角菱环 */
function ringPath(k: number) {
  const L = { x: C.x - RADII.out[k], y: C.y };
  const R = { x: C.x + RADII.inw[k], y: C.y };
  const T = { x: C.x, y: C.y - RADII.time[k] };
  const B = { x: C.x, y: C.y + RADII.space[k] };
  const f = 0.552;
  const rt = RADII.time[k] * f, rs = RADII.space[k] * f, ro = RADII.out[k] * f, ri = RADII.inw[k] * f;
  return [
    `M ${T.x} ${T.y}`,
    `C ${T.x + ri} ${T.y}, ${R.x} ${R.y - rt}, ${R.x} ${R.y}`,
    `C ${R.x} ${R.y + rs}, ${B.x + ri} ${B.y}, ${B.x} ${B.y}`,
    `C ${B.x - ro} ${B.y}, ${L.x} ${L.y + rs}, ${L.x} ${L.y}`,
    `C ${L.x} ${L.y - rt}, ${T.x - ro} ${T.y}, ${T.x} ${T.y} Z`,
  ].join(" ");
}

const PIN_COLOR: Record<BoundPin["kind"], string> = {
  talk: "var(--coral)",
  essay: "var(--amber)",
  course: "var(--ink-2)",
  book: "var(--magenta)",
};

/** 度盘齿：半径 r，count 根，majorEvery 根一长齿 */
function BezelTicks({ r, count, majorEvery, len, majorLen }: { r: number; count: number; majorEvery: number; len: number; majorLen: number }) {
  const ticks = [];
  for (let i = 0; i < count; i++) {
    const a = (i / count) * Math.PI * 2;
    const major = i % majorEvery === 0;
    const l = major ? majorLen : len;
    const x1 = C.x + Math.cos(a) * r, y1 = C.y + Math.sin(a) * r;
    const x2 = C.x + Math.cos(a) * (r - l), y2 = C.y + Math.sin(a) * (r - l);
    ticks.push(<line key={i} x1={x1} y1={y1} x2={x2} y2={y2} className={major ? "bz-major" : "bz-minor"} />);
  }
  return <>{ticks}</>;
}

/** 尺身细齿：沿射线从 r0 到 r1，每 step 一根，长齿间隔 majorEvery */
function RulerTeeth({ rayId, r0, r1 }: { rayId: Ray["id"]; r0: number; r1: number }) {
  const [dx, dy] = DIR[rayId];
  const horiz = dy === 0;
  const teeth = [];
  let n = 0;
  for (let r = r0; r <= r1; r += 13, n++) {
    const isMed = n % 5 === 0;
    const l = isMed ? 9 : 5;
    const x = C.x + dx * r, y = C.y + dy * r;
    teeth.push(
      <line
        key={r}
        className={isMed ? "tooth med" : "tooth"}
        x1={horiz ? x : x - l}
        y1={horiz ? y - l : y}
        x2={horiz ? x : x + l}
        y2={horiz ? y + l : y}
      />
    );
  }
  return <>{teeth}</>;
}

export default function RulerCompass({
  interactive = false,
  idPrefix = "cp",
}: {
  interactive?: boolean;
  idPrefix?: string;
}) {
  const [tip, setTip] = useState<{ x: number; y: number; pin: BoundPin; ray: Ray; st: Station } | null>(null);
  const hostRef = useRef<HTMLDivElement>(null);

  const showTip = (e: React.MouseEvent, pin: BoundPin, ray: Ray, st: Station) => {
    if (!interactive) return;
    const host = hostRef.current?.getBoundingClientRect();
    if (!host) return;
    setTip({ x: e.clientX - host.left, y: e.clientY - host.top, pin, ray, st });
  };

  return (
    <div className="compass-host" ref={hostRef}>
      <svg viewBox={`0 0 ${VB.w} ${VB.h}`} role="img" aria-label="时空内外 · 四把尺子">
        <defs>
          {/* 四向射线渐变（沿方向 amber 渐隐） */}
          <linearGradient id={`${idPrefix}-g-out`} gradientUnits="userSpaceOnUse" x1={C.x} y1={C.y} x2={C.x - 660} y2={C.y}>
            <stop offset="0" stopColor="var(--amber)" stopOpacity=".75" />
            <stop offset="1" stopColor="var(--amber)" stopOpacity=".08" />
          </linearGradient>
          <linearGradient id={`${idPrefix}-g-inw`} gradientUnits="userSpaceOnUse" x1={C.x} y1={C.y} x2={C.x + 660} y2={C.y}>
            <stop offset="0" stopColor="var(--amber)" stopOpacity=".75" />
            <stop offset="1" stopColor="var(--amber)" stopOpacity=".08" />
          </linearGradient>
          <linearGradient id={`${idPrefix}-g-time`} gradientUnits="userSpaceOnUse" x1={C.x} y1={C.y} x2={C.x} y2={C.y - 520}>
            <stop offset="0" stopColor="var(--amber)" stopOpacity=".75" />
            <stop offset="1" stopColor="var(--amber)" stopOpacity=".08" />
          </linearGradient>
          <linearGradient id={`${idPrefix}-g-space`} gradientUnits="userSpaceOnUse" x1={C.x} y1={C.y} x2={C.x} y2={C.y + 520}>
            <stop offset="0" stopColor="var(--amber)" stopOpacity=".75" />
            <stop offset="1" stopColor="var(--amber)" stopOpacity=".08" />
          </linearGradient>
          <filter id={`${idPrefix}-glow`} x="-120%" y="-120%" width="340%" height="340%">
            <feGaussianBlur stdDeviation="5" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <radialGradient id={`${idPrefix}-corona`} cx="50%" cy="50%" r="50%">
            <stop offset="0" stopColor="var(--amber)" stopOpacity=".2" />
            <stop offset=".55" stopColor="var(--amber)" stopOpacity=".05" />
            <stop offset="1" stopColor="var(--amber)" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* ---- 幽灵大字（当前维度的汉字底纹） ---- */}
        {rays.map((ray) => (
          <text key={`gh-${ray.id}`} className={`gzh gzh-${ray.id}`} x={C.x} y={C.y + 150}>
            {ray.zh}
          </text>
        ))}

        {/* ---- 度盘：四个维度四个环，由内而外 = 时 · 空 · 内 · 外 ---- */}
        <g className="bezel bezel-1 bz-dim-time">
          <circle cx={C.x} cy={C.y} r={424} className="bz-ring" />
          <BezelTicks r={424} count={96} majorEvery={8} len={6} majorLen={13} />
        </g>
        <g className="bezel bezel-2 bz-dim-space">
          <circle cx={C.x} cy={C.y} r={458} className="bz-ring dashed" />
          <BezelTicks r={458} count={120} majorEvery={10} len={6} majorLen={14} />
        </g>
        <g className="bezel bezel-3 bz-dim-inw">
          <circle cx={C.x} cy={C.y} r={492} className="bz-ring" />
          <BezelTicks r={492} count={72} majorEvery={6} len={7} majorLen={15} />
        </g>
        <g className="bezel bezel-4 bz-dim-out">
          <circle cx={C.x} cy={C.y} r={526} className="bz-ring dashed" />
          <BezelTicks r={526} count={144} majorEvery={12} len={8} majorLen={18} />
        </g>

        {/* ---- 格环 ---- */}
        {[0, 1, 2, 3, 4].map((k) => (
          <path key={k} d={ringPath(k)} className="ring" style={{ ["--k" as string]: k }} />
        ))}

        {/* ---- 四把尺子 ---- */}
        {rays.map((ray) => {
          const [dx, dy] = DIR[ray.id];
          const horiz = dy === 0;
          const last = RADII[ray.id][RADII[ray.id].length - 1];
          const end = { x: C.x + dx * (last + (horiz ? 46 : 36)), y: C.y + dy * (last + (horiz ? 46 : 36)) };
          const far = { x: C.x + dx * (last + (horiz ? 128 : 84)), y: C.y + dy * (last + (horiz ? 128 : 84)) };
          const zh = horiz
            ? { x: C.x + dx * (last + 118), y: C.y - 48, anchor: "middle" as const }
            : { x: C.x + 56, y: far.y + (dy < 0 ? 6 : 2), anchor: "start" as const };
          const nm = horiz
            ? { x: zh.x, y: C.y - 22, anchor: "middle" as const }
            : { x: C.x + 56, y: zh.y + 22, anchor: "start" as const };
          const fr = horiz
            ? { x: zh.x, y: C.y + 34, anchor: "middle" as const }
            : { x: C.x - 56, y: far.y + (dy < 0 ? 12 : 8), anchor: "end" as const };
          return (
            <g key={ray.id} className={`cray cray-${ray.id}`}>
              {/* 尺身：渐变主线 + 细齿 + 流光 */}
              <line className="cray-line" x1={C.x + dx * 56} y1={C.y + dy * 56} x2={end.x} y2={end.y}
                stroke={`url(#${idPrefix}-g-${ray.id})`} />
              <g className="cray-teeth"><RulerTeeth rayId={ray.id} r0={70} r1={last + 26} /></g>
              <line className="cray-flow" x1={C.x + dx * 60} y1={C.y + dy * 60} x2={end.x} y2={end.y} />
              <line className="cray-beyond" x1={end.x} y1={end.y} x2={far.x} y2={far.y} />

              <text className="cray-zh" x={zh.x} y={zh.y} textAnchor={zh.anchor}>{ray.zh}</text>
              <text className="cray-name" x={nm.x} y={nm.y} textAnchor={nm.anchor}>{ray.name} · {ray.en}</text>
              <text className="cray-far" x={fr.x} y={fr.y} textAnchor={fr.anchor}>{ray.beyond} →</text>

              {/* 刻度站 + 钉图 */}
              {ray.stations.map((st, i) => {
                const p = stationXY(ray.id, i);
                const boundPins = st.pins.map(bindPin);
                return (
                  <g key={st.id} className="cst" style={{ ["--i" as string]: i }}>
                    <line className="cst-tick"
                      x1={horiz ? p.x : p.x - 13} y1={horiz ? p.y - 13 : p.y}
                      x2={horiz ? p.x : p.x + 13} y2={horiz ? p.y + 13 : p.y} />
                    <text className="cst-label" x={horiz ? p.x : p.x - 22} y={horiz ? p.y + 38 : p.y - 6}
                      textAnchor={horiz ? "middle" : "end"}>{st.label}</text>
                    <text className="cst-sub" x={horiz ? p.x : p.x - 22} y={horiz ? p.y + 58 : p.y + 12}
                      textAnchor={horiz ? "middle" : "end"}>{st.tick}</text>
                    {boundPins.map((pin, j) => {
                      const off = 30 + j * 29;
                      const px = horiz ? p.x : p.x + off;
                      const py = horiz ? p.y - off : p.y;
                      return (
                        <g key={pin.slug ?? pin.title} className={`cpin ${pin.locked ? "locked" : ""}`} style={{ ["--j" as string]: j }}>
                          <line className="cpin-leader" x1={horiz ? p.x : p.x + 15} y1={horiz ? p.y - 15 : p.y} x2={px} y2={py} />
                          <circle className="cpin-halo" cx={px} cy={py} r={11} style={{ ["--pc" as string]: pin.locked ? "var(--ink-3)" : PIN_COLOR[pin.kind] }} />
                          <circle
                            className="cpin-dot"
                            cx={px} cy={py} r={5.4}
                            filter={`url(#${idPrefix}-glow)`}
                            style={{ ["--pc" as string]: pin.locked ? "var(--ink-3)" : PIN_COLOR[pin.kind] }}
                          />
                          {/* 命中圈：装饰层不接事件，交互都在这枚透明圈上 */}
                          <circle
                            className="cpin-hit"
                            cx={px} cy={py} r={14}
                            onMouseEnter={(e) => showTip(e, pin, ray, st)}
                            onMouseMove={(e) => showTip(e, pin, ray, st)}
                            onMouseLeave={() => setTip(null)}
                            onClick={() => { if (interactive && pin.href) window.location.href = pin.href; }}
                          />
                        </g>
                      );
                    })}
                  </g>
                );
              })}
            </g>
          );
        })}

        {/* ---- 原点 · 人（辉光 + 涟漪） ---- */}
        <g className="corigin">
          <circle cx={C.x} cy={C.y} r={130} fill={`url(#${idPrefix}-corona)`} className="corona" />
          <circle className="ripple r1" cx={C.x} cy={C.y} r={44} />
          <circle className="ripple r2" cx={C.x} cy={C.y} r={44} />
          <circle className="corigin-ring" cx={C.x} cy={C.y} r={40} filter={`url(#${idPrefix}-glow)`} />
          <text className="corigin-zh" x={C.x} y={C.y + 10}>{rulerMeta.origin}</text>
          <text className="corigin-note" x={C.x} y={C.y + 68}>{rulerMeta.originNote}</text>
        </g>
      </svg>

      {interactive && tip && (
        <div className="ruler-tip" style={{ left: tip.x + 16, top: tip.y - 12 }}>
          <span className="k">{tip.ray.zh} · {tip.st.label}{tip.pin.vol ? ` · ${tip.pin.vol}` : ""}</span>
          <span className="t">{tip.pin.title}</span>
          <span className="r">{tip.pin.reading}</span>
          <span className="a">{tip.pin.locked ? "连载中 · 2026.08 首发后开放" : tip.pin.href ? "点击展开这一篇 →" : ""}</span>
        </div>
      )}
    </div>
  );
}
