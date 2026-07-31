"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { rays, rulerMeta, bindPin, type Ray, type Station, type BoundPin } from "@/content/ruler";

/** ============================================================
 *  活页 · 尺子 —— 四向星盘
 *  主线导览（沿主线走）+ 自由游走（悬停读数 / 点击入篇 / 缩放拖拽）
 *  几何：中心「人」，外(左) 时(上) 空(下) 内(右) 四条对数刻度射线 + 格环
 *  ============================================================ */

const VB = { w: 1680, h: 1240 };
const C = { x: VB.w / 2, y: VB.h / 2 };

const RADII: Record<Ray["id"], number[]> = {
  out: [170, 278, 386, 494, 602],
  inw: [170, 278, 386, 494, 602],
  time: [130, 195, 260, 325, 390, 455],
  space: [135, 215, 295, 375, 455],
};
const DIR: Record<Ray["id"], [number, number]> = {
  out: [-1, 0],
  inw: [1, 0],
  time: [0, -1],
  space: [0, 1],
};

type Stop =
  | { type: "origin" }
  | { type: "station"; ray: Ray; st: Station; x: number; y: number }
  | { type: "finale" };

function stationXY(rayId: Ray["id"], idx: number) {
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

export default function RulerMap() {
  const [mode, setMode] = useState<"free" | "tour">("free");
  const [stopIdx, setStopIdx] = useState(0);
  const [view, setView] = useState({ scale: 1, tx: 0, ty: 0 });
  const [tip, setTip] = useState<{ x: number; y: number; pin: BoundPin; ray: Ray; st: Station } | null>(null);
  const [live, setLive] = useState(false);
  const drag = useRef<{ on: boolean; x: number; y: number; tx: number; ty: number }>({ on: false, x: 0, y: 0, tx: 0, ty: 0 });
  const wrapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const t = setTimeout(() => setLive(true), 60);
    return () => clearTimeout(t);
  }, []);

  /** 主线：原点 → 外 → 时 → 空 → 内（尺子最后转向自己）→ 收束 */
  const stops = useMemo<Stop[]>(() => {
    const order: Ray["id"][] = ["out", "time", "space", "inw"];
    const s: Stop[] = [{ type: "origin" }];
    for (const id of order) {
      const ray = rays.find((r) => r.id === id)!;
      ray.stations.forEach((st, i) => s.push({ type: "station", ray, st, ...stationXY(id, i) }));
    }
    s.push({ type: "finale" });
    return s;
  }, []);

  const applyCamera = useCallback((stop: Stop) => {
    if (stop.type !== "station") {
      setView({ scale: 1, tx: 0, ty: 0 });
      return;
    }
    const scale = 1.6;
    // 目标站映射到画面偏左（右侧留给站卡）
    const fx = VB.w * 0.38, fy = VB.h * 0.46;
    setView({ scale, tx: fx - stop.x * scale, ty: fy - stop.y * scale });
  }, []);

  const goto = useCallback(
    (i: number) => {
      const n = Math.max(0, Math.min(i, stops.length - 1));
      setStopIdx(n);
      applyCamera(stops[n]);
      setTip(null);
    },
    [stops, applyCamera]
  );

  const startTour = useCallback(() => {
    setMode("tour");
    goto(0);
  }, [goto]);
  const exitTour = useCallback(() => {
    setMode("free");
    setView({ scale: 1, tx: 0, ty: 0 });
    setTip(null);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (mode === "tour") {
        if (e.key === "ArrowRight" || e.key === "Enter" || e.key === " ") { e.preventDefault(); goto(stopIdx + 1); }
        else if (e.key === "ArrowLeft") { e.preventDefault(); goto(stopIdx - 1); }
        else if (e.key === "Escape") exitTour();
      } else if (e.key === "Enter") startTour();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [mode, stopIdx, goto, exitTour, startTour]);

  /* ---- 自由模式：缩放 / 拖拽 ---- */
  const onWheel = (e: React.WheelEvent) => {
    if (mode !== "free") return;
    const next = Math.min(2.4, Math.max(0.7, view.scale * Math.pow(1.0016, -e.deltaY)));
    setView((v) => ({ ...v, scale: next }));
  };
  const onPointerDown = (e: React.PointerEvent) => {
    if (mode !== "free") return;
    drag.current = { on: true, x: e.clientX, y: e.clientY, tx: view.tx, ty: view.ty };
  };
  const onPointerMove = (e: React.PointerEvent) => {
    if (!drag.current.on) return;
    setView((v) => ({ ...v, tx: drag.current.tx + (e.clientX - drag.current.x), ty: drag.current.ty + (e.clientY - drag.current.y) }));
  };
  const onPointerUp = () => (drag.current.on = false);

  const showTip = (e: React.MouseEvent, pin: BoundPin, ray: Ray, st: Station) => {
    const host = wrapRef.current?.getBoundingClientRect();
    if (!host) return;
    setTip({ x: e.clientX - host.left, y: e.clientY - host.top, pin, ray, st });
  };

  const cur = stops[stopIdx];
  const stationNo = stops.filter((s) => s.type === "station").length;
  const curStationNo = stops.slice(0, stopIdx + 1).filter((s) => s.type === "station").length;

  const readout =
    mode === "tour"
      ? cur.type === "station"
        ? `${cur.ray.zh} · ${cur.ray.name} — ${cur.st.label} · ${cur.st.tick}`
        : cur.type === "origin"
          ? `原点 · ${rulerMeta.origin} — ${rulerMeta.originNote}`
          : "尺子最后转向自己"
      : rulerMeta.legend;

  return (
    <div className={`ruler-wrap ${live ? "live" : ""}`} ref={wrapRef}>
      {/* 顶部操作 */}
      <div className="ruler-topbar">
        {mode === "free" ? (
          <button className="rbtn primary" onClick={startTour}>沿主线走 ↵</button>
        ) : (
          <>
            <button className="rbtn" onClick={() => goto(stopIdx - 1)} disabled={stopIdx === 0}>← 上一站</button>
            <button className="rbtn primary" onClick={() => goto(stopIdx + 1)} disabled={stopIdx === stops.length - 1}>下一站 →</button>
            <button className="rbtn ghost" onClick={exitTour}>✕ 自由游走</button>
          </>
        )}
      </div>

      {/* 星盘 */}
      <div
        className={`ruler-stage ${mode}`}
        onWheel={onWheel}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerLeave={onPointerUp}
      >
        <svg viewBox={`0 0 ${VB.w} ${VB.h}`} role="img" aria-label="活页 · 尺子：四向星盘">
          <g
            className="ruler-cam"
            style={{ transform: `translate(${view.tx}px, ${view.ty}px) scale(${view.scale})` }}
          >
            {/* 格环 */}
            {[0, 1, 2, 3, 4].map((k) => (
              <path key={k} d={ringPath(k)} className="ring" style={{ ["--k" as string]: k }} />
            ))}

            {/* 射线 */}
            {rays.map((ray) => {
              const [dx, dy] = DIR[ray.id];
              const horiz = dy === 0;
              const last = RADII[ray.id][RADII[ray.id].length - 1];
              const end = { x: C.x + dx * (last + (horiz ? 46 : 36)), y: C.y + dy * (last + (horiz ? 46 : 36)) };
              const far = { x: C.x + dx * (last + (horiz ? 128 : 84)), y: C.y + dy * (last + (horiz ? 128 : 84)) };
              // 标注锚点：横射线 → 大字在轴上方尽头处，尽头注在轴下方；竖射线 → 大字在箭头旁侧，尽头注在另一侧
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
                <g key={ray.id} className={`ray ray-${ray.id}`}>
                  <line className="ray-line" x1={C.x + dx * 56} y1={C.y + dy * 56} x2={end.x} y2={end.y} />
                  <line className="ray-beyond" x1={end.x} y1={end.y} x2={far.x} y2={far.y} />
                  <text className="ray-zh" x={zh.x} y={zh.y} textAnchor={zh.anchor}>{ray.zh}</text>
                  <text className="ray-name" x={nm.x} y={nm.y} textAnchor={nm.anchor}>{ray.name} · {ray.en}</text>
                  <text className="ray-far" x={fr.x} y={fr.y} textAnchor={fr.anchor}>{ray.beyond} →</text>

                  {/* 刻度站 */}
                  {ray.stations.map((st, i) => {
                    const p = stationXY(ray.id, i);
                    const horiz = dy === 0;
                    const boundPins = st.pins.map(bindPin);
                    return (
                      <g key={st.id} className="station" style={{ ["--i" as string]: i }}>
                        <line
                          className="tickmark"
                          x1={horiz ? p.x : p.x - 9}
                          y1={horiz ? p.y - 9 : p.y}
                          x2={horiz ? p.x : p.x + 9}
                          y2={horiz ? p.y + 9 : p.y}
                        />
                        <text className="st-label" x={horiz ? p.x : p.x - 18} y={horiz ? p.y + 34 : p.y - 6}
                          textAnchor={horiz ? "middle" : "end"}>
                          {st.label}
                        </text>
                        <text className="st-tick" x={horiz ? p.x : p.x - 18} y={horiz ? p.y + 54 : p.y + 12}
                          textAnchor={horiz ? "middle" : "end"}>
                          {st.tick}
                        </text>
                        {/* 钉图 pins */}
                        {boundPins.map((pin, j) => {
                          const off = 26 + j * 27;
                          const px = horiz ? p.x : p.x + off;
                          const py = horiz ? p.y - off : p.y;
                          const dot = (
                            <g key={pin.slug ?? pin.title}>
                              <line className="pin-leader" x1={horiz ? p.x : p.x + 11} y1={horiz ? p.y - 11 : p.y} x2={px} y2={py} />
                              <circle
                                className={`pin ${pin.locked ? "locked" : ""}`}
                                cx={px}
                                cy={py}
                                r={5.6}
                                style={{ ["--pc" as string]: pin.locked ? "var(--ink-3)" : PIN_COLOR[pin.kind] }}
                                onMouseEnter={(e) => showTip(e, pin, ray, st)}
                                onMouseMove={(e) => showTip(e, pin, ray, st)}
                                onMouseLeave={() => setTip(null)}
                                onClick={() => { if (pin.href) window.location.href = pin.href; }}
                              />
                            </g>
                          );
                          return dot;
                        })}
                      </g>
                    );
                  })}
                </g>
              );
            })}

            {/* 原点 · 人 */}
            <g className="origin">
              <circle className="origin-ring" cx={C.x} cy={C.y} r={40} />
              <circle className="origin-core" cx={C.x} cy={C.y} r={3} />
              <text className="origin-zh" x={C.x} y={C.y + 9}>{rulerMeta.origin}</text>
              <text className="origin-note" x={C.x} y={C.y + 66}>{rulerMeta.originNote}</text>
            </g>
          </g>
        </svg>

        {/* 悬停读数卡 */}
        {tip && (
          <div className="ruler-tip" style={{ left: tip.x + 16, top: tip.y - 12 }}>
            <span className="k">{tip.ray.zh} · {tip.st.label}{tip.pin.vol ? ` · ${tip.pin.vol}` : ""}</span>
            <span className="t">{tip.pin.title}</span>
            <span className="r">{tip.pin.reading}</span>
            <span className="a">{tip.pin.locked ? "连载中 · 2026.08 首发后开放" : tip.pin.href ? "点击展开这一篇 →" : ""}</span>
          </div>
        )}

        {/* 导览站卡 */}
        {mode === "tour" && (
          <aside className="tour-card">
            {cur.type === "origin" && (
              <>
                <p className="tc-k">主线 · 起点</p>
                <h2 className="tc-t">{rulerMeta.origin} · 原点</h2>
                <p className="tc-d">
                  同一把尺子，从人出发。向外量系统，向内量自己；面向时间，从毫秒到纪元；
                  面向空间，从一场对话到全人类。四条射线的尽头都伸进非人的尺度——但刻度，永远是人读的。
                </p>
                <p className="tc-hint">→ 或 Enter 出发 · 共 {stationNo} 站</p>
              </>
            )}
            {cur.type === "station" && (
              <>
                <p className="tc-k">{cur.ray.zh} · {cur.ray.name} — 第 {curStationNo} / {stationNo} 站</p>
                <h2 className="tc-t">{cur.st.label} <small>{cur.st.tick}</small></h2>
                <ul className="tc-pins">
                  {cur.st.pins.map(bindPin).map((pin) => (
                    <li key={pin.slug ?? pin.title}>
                      {pin.href ? (
                        <a href={pin.href}>
                          <b>{pin.title}</b>
                          <span>{pin.reading}{pin.vol ? ` · 卷${["一","二","三","四","五"][+pin.vol.split(".")[0] - 1]} · ${pin.vol}` : ""}</span>
                        </a>
                      ) : (
                        <div className={pin.locked ? "locked" : ""}>
                          <b>{pin.title}</b>
                          <span>{pin.reading}{pin.locked ? " · 连载中" : ""}</span>
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              </>
            )}
            {cur.type === "finale" && (
              <>
                <p className="tc-k">主线 · 终点</p>
                <h2 className="tc-t">尺子最后转向自己</h2>
                <p className="tc-d">
                  走完外、时、空，最后一条射线向内——这也是《同一把尺子》整本书的走法。
                  地图到此为止，书从这里开始。
                </p>
                <div className="tc-ctas">
                  <a className="cta" href="/preface">从序开始读 →</a>
                  <a className="cta ghost" href="/vol5">直接去卷五 · 内观 →</a>
                </div>
              </>
            )}
          </aside>
        )}

        {/* 自由模式缩放控件 */}
        {mode === "free" && (
          <div className="ruler-zoom">
            <button className="rbtn" onClick={() => setView((v) => ({ ...v, scale: Math.min(2.4, v.scale * 1.2) }))}>＋</button>
            <button className="rbtn" onClick={() => setView((v) => ({ ...v, scale: Math.max(0.7, v.scale / 1.2) }))}>－</button>
            <button className="rbtn" onClick={() => setView({ scale: 1, tx: 0, ty: 0 })}>⟲</button>
          </div>
        )}
      </div>

      {/* 仪器读数栏 */}
      <div className="ruler-readout">
        <span className="dot" aria-hidden="true" />
        {readout}
      </div>
    </div>
  );
}
