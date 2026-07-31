import type { Metadata } from "next";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import RulerScroll from "@/components/RulerScroll";

export const metadata: Metadata = {
  title: { absolute: "时空内外 ·《同一把尺子》· 姚光华 Colin" },
  description:
    "时空内外——姚光华（Colin）的思想星盘。时 · 从毫秒到纪元，空 · 从一场对话到全人类，内 · 内观的纵深，外 · Eval 的粒度；41 枚思想钉在四个维度的刻度上。展开是时空内外，合上是《同一把尺子》。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

export default function Home() {
  return (
    <>
      {/* 首页即星盘：不滚自转循环，滚动逐维展开，滚完全图可点 */}
      <RulerScroll />

      {/* 尾部：开合的两个去处 */}
      <section className="section hairline">
        <div className="wrap">
          <Reveal className="section-head">
            <p className="eyebrow flow" style={s(0)}>NEXT <span className="am">·</span> 从这里去</p>
            <h2 className="h-sec ink" style={s(1)}>展开看过了，合上再读一遍</h2>
            <p className="lead flow" style={s(2)}>
              四个维度各有一页目录（导航上的<b>时 · 空 · 内 · 外</b>）；要找某一篇，去总目；
              要按论证的顺序读，合上——它是一本书。
            </p>
          </Reveal>
          <Reveal className="vol-nav">
            <Link href="/toc">
              <span className="k">总目 · INDEX</span>
              <span className="t">按维 · 按卷 · 按时 · 按术语</span>
            </Link>
            <Link href="/book" className="next">
              <span className="k">合上是同一把尺子 →</span>
              <span className="t">《同一把尺子》· 书</span>
            </Link>
          </Reveal>
        </div>
      </section>
    </>
  );
}
