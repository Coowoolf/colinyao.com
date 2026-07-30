"use client";

import { useEffect, useRef, useState, type ElementType, type ReactNode } from "react";

/**
 * 流动感触发器：进入视口时给容器加 .visible，
 * 容器内的 .flow / .rise / .spread / .settle / .ink / .dw / .pop 逐层错峰入场。
 */
export default function Reveal({
  as: Tag = "div",
  className = "",
  children,
  threshold = 0.16,
  ...rest
}: {
  as?: ElementType;
  className?: string;
  children: ReactNode;
  threshold?: number;
  [key: string]: unknown;
}) {
  const ref = useRef<HTMLElement | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setVisible(true);
      return;
    }
    // 首屏兜底：布局盒已在视口内就直接触发（双 rAF 保证初态先绘制、动画完整播放）
    const r = el.getBoundingClientRect();
    if (r.top < window.innerHeight * 0.92 && r.bottom > 0) {
      requestAnimationFrame(() => requestAnimationFrame(() => setVisible(true)));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            setVisible(true);
            io.disconnect();
          }
        }
      },
      { threshold, rootMargin: "0px 0px -6% 0px" }
    );
    io.observe(el);
    return () => io.disconnect();
  }, [threshold]);

  return (
    <Tag ref={ref} className={`rv ${visible ? "visible" : ""} ${className}`} {...rest}>
      {children}
    </Tag>
  );
}
