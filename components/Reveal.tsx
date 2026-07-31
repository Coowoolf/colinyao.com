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
    if (r.top < window.innerHeight * 0.92) { // 在露出线以上（含已滚过/恢复滚动位置）即触发
      requestAnimationFrame(() => requestAnimationFrame(() => setVisible(true)));
      return;
    }
    let idleT: ReturnType<typeof setTimeout> | undefined;
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) done();
        }
      },
      { threshold, rootMargin: "0px 0px -6% 0px" }
    );
    // 保险：滚动停稳后复查一次布局盒（防锚点直跳/急速滚动下 IO 偶发漏报）
    const onScroll = () => {
      clearTimeout(idleT);
      idleT = setTimeout(() => {
        const r2 = el.getBoundingClientRect();
        if (r2.top < window.innerHeight * 0.96) done(); // 含已滚过头的元素
      }, 260);
    };
    function done() {
      setVisible(true);
      io.disconnect();
      window.removeEventListener("scroll", onScroll);
      clearTimeout(idleT);
    }
    io.observe(el);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      io.disconnect();
      window.removeEventListener("scroll", onScroll);
      clearTimeout(idleT);
    };
  }, [threshold]);

  return (
    <Tag ref={ref} className={`rv ${visible ? "visible" : ""} ${className}`} {...rest}>
      {children}
    </Tag>
  );
}
