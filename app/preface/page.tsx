import type { Metadata } from "next";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import Motif from "@/components/Motifs";
import { preface } from "@/content/book";

export const metadata: Metadata = {
  title: "序 · 同一把尺子",
  description: "《同一把尺子》序：向外叫 Eval，向内叫内观。产品和人，进化机制是同一个——更早发现错误，更快修正错误。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

export default function PrefacePage() {
  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head vol-head">
          <span className="voln" aria-hidden="true">序</span>
          <p className="eyebrow flow" style={s(0)}>{preface.en}</p>
          <h1 className="h-sec ink" style={s(1)}>{preface.zh}</h1>
        </Reveal>

        <Reveal className="preface-body">
          {preface.intro.map((p, i) => (
            <p key={i} className={`flow ${i === 0 ? "dropcap" : ""} ${i === preface.intro.length - 1 ? "last" : ""}`} style={s(i + 1)}>
              {p}
            </p>
          ))}
        </Reveal>

        <Reveal>
          <div className="stat-motif flow" style={{ ...s(1), height: 96, marginTop: 48 }}>
            <Motif kind="ruler" plain />
          </div>
        </Reveal>

        <Reveal className="vol-nav">
          <Link href="/">
            <span className="k">← 封面</span>
            <span className="t">总目录</span>
          </Link>
          <Link href="/vol1" className="next">
            <span className="k">开始读 · 卷一 →</span>
            <span className="t">尺子</span>
          </Link>
        </Reveal>
      </div>
    </section>
  );
}
