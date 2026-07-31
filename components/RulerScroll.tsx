"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import RulerCompass from "@/components/RulerCompass";
import { rays, rulerMeta, dimOrder, bindPin, type Ray } from "@/content/ruler";

/** ============================================================
 *  时空内外 · 四把尺子 —— scroll 叙事驱动器
 *  唯一交互 = 滚动：合上 → 时 → 空 → 内 → 外 → 全图（可点击）
 *  不滚时（首焦）：自动走「展开-闭合」循环，页面自己流动
 *  ============================================================ */

type Dim = Ray["id"] | "all" | null; // null = 合上

const ATTRACT: { dim: Dim; ms: number }[] = [
  { dim: "time", ms: 4300 },
  { dim: "space", ms: 4300 },
  { dim: "inw", ms: 4300 },
  { dim: "out", ms: 4300 },
  { dim: "all", ms: 3400 },
  { dim: null, ms: 1400 },
];

const CN: Record<string, string> = { time: "时", space: "空", inw: "内", out: "外" };

export default function RulerScroll() {
  const [dim, setDim] = useState<Dim>("all"); // SSR/无 JS：全图打开
  const [p, setP] = useState(0);
  const wrapRef = useRef<HTMLDivElement>(null);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const attractIdx = useRef(0);
  const inAttract = useRef(false);

  const stopAttract = useCallback(() => {
    inAttract.current = false;
    if (timer.current) { clearTimeout(timer.current); timer.current = null; }
  }, []);

  const attractStep = useCallback(() => {
    const cur = ATTRACT[attractIdx.current % ATTRACT.length];
    setDim(cur.dim);
    timer.current = setTimeout(() => {
      attractIdx.current += 1;
      if (inAttract.current) attractStep();
    }, cur.ms);
  }, []);

  const startAttract = useCallback(() => {
    if (inAttract.current) return;
    inAttract.current = true;
    attractStep();
  }, [attractStep]);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setDim("all");
      return;
    }
    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = wrapRef.current;
        if (!el) return;
        const vh = window.innerHeight;
        const r = el.getBoundingClientRect();
        const prog = Math.max(0, Math.min(1, -r.top / (r.height - vh)));
        setP(prog);
        if (prog <= 0.012) {
          startAttract(); // 回到顶部 → 恢复自转循环
          return;
        }
        stopAttract();
        if (prog < 0.05) setDim(null); // 一旦开始滚：先合上
        else if (prog < 0.86) {
          const k = Math.min(3, Math.floor(((prog - 0.05) / (0.86 - 0.05)) * 4));
          setDim(dimOrder[k]); // 再按时空内外逐把展开
        } else setDim("all"); // 走完回到大图 · 可点击
      });
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    return () => {
      stopAttract();
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, [startAttract, stopAttract]);

  const activeRay = dim && dim !== "all" ? rays.find((r) => r.id === dim) : null;
  const atTop = p <= 0.012;
  const isAll = dim === "all";

  const readout = activeRay
    ? `${activeRay.zh} · ${activeRay.name} — ${activeRay.stations[0].label} → ${activeRay.stations[activeRay.stations.length - 1].label} · ${activeRay.beyond}`
    : isAll
      ? rulerMeta.legend
      : "合上是同一把尺子";

  return (
    <div className="ruler-scrollwrap" ref={wrapRef}>
      <div className="rstage" data-dim={dim ?? ""} data-fold={dim === null ? 1 : 0}>
        <RulerCompass interactive={isAll} />

        {/* 首焦标题（待机时可见） */}
        <div className={`rs-head ${atTop ? "on" : ""}`}>
          <p className="eyebrow">活页 <span className="am">·</span> {rulerMeta.en}</p>
          <h1 className="rs-title">{rulerMeta.title}</h1>
          <p className="rs-sub">
            <b>时</b>，从毫秒到纪元；<b>空</b>，从一场对话到全人类；<b>内</b>，内观的纵深；<b>外</b>，Eval 的粒度。
            四个维度，合上是同一把尺子。
          </p>
          <p className="rs-hint">↓ 向下滚动 · 逐维展开</p>
        </div>

        {/* 维度卡（叙事段可见，钉可点） */}
        {activeRay && !atTop && (
          <aside className="dim-card" key={activeRay.id}>
            <p className="dc-k">第 {["一", "二", "三", "四"][dimOrder.indexOf(activeRay.id)]} 维 · {activeRay.name} · {activeRay.en}</p>
            <h2 className="dc-t">{CN[activeRay.id]}</h2>
            <ul className="dc-pins">
              {activeRay.stations.map((st) => (
                <li key={st.id}>
                  <span className="dc-st">{st.label} <i>{st.tick}</i></span>
                  {st.pins.map(bindPin).map((pin) =>
                    pin.href ? (
                      <a key={pin.slug ?? pin.title} href={pin.href}>
                        <b>{pin.title}</b>
                        <span>{pin.reading}</span>
                      </a>
                    ) : (
                      <div key={pin.slug ?? pin.title} className={pin.locked ? "locked" : ""}>
                        <b>{pin.title}</b>
                        <span>{pin.reading}{pin.locked ? " · 连载中" : ""}</span>
                      </div>
                    )
                  )}
                </li>
              ))}
            </ul>
          </aside>
        )}

        {/* 全图提示（叙事终段） */}
        {isAll && !atTop && (
          <div className="rs-allhint">全图 · 悬停读数 · 点击入篇 · 继续下滑看逐格清单 ↓</div>
        )}

        {/* 进度侧轨：时空内外（全图态 = 四字齐亮变大） */}
        <div className={`rs-rail ${isAll ? "all" : ""}`} aria-hidden="true">
          {dimOrder.map((id) => (
            <span key={id} className={dim === id ? "on" : ""}>{CN[id]}</span>
          ))}
        </div>

        {/* 仪器读数栏 */}
        <div className="rs-readout">
          <span className="dot" aria-hidden="true" />
          {readout}
        </div>
      </div>
    </div>
  );
}
