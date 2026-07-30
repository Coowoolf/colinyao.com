import type { Metadata } from "next";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import Motif from "@/components/Motifs";
import { ideas } from "@/content/ideas";
import { volumes } from "@/content/book";

export const metadata: Metadata = {
  title: "附录 B · 术语索引",
  description:
    "《同一把尺子》附录 B · 术语索引：同一把尺子、活人感、被记住·被托付、模型上限·引擎下限、Vibe SOTA、QoI、听得到→听得心、0.29TB。每条术语标注定义、出处与归卷。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);
const CN = ["一", "二", "三", "四", "五"];

/** 概念 id → 归卷（ruler 特例归序） */
const homeVol = new Map<string, { label: string; href: string }>();
volumes.forEach((v) => v.concepts.forEach((c) => homeVol.set(c, { label: `卷${CN[v.no - 1]} · ${v.zh}`, href: `/${v.id}` })));
homeVol.set("ruler", { label: "序 / 卷五 · 内观", href: "/preface" });

export default function IdeasPage() {
  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head">
          <p className="eyebrow flow" style={s(0)}>附录 B <span className="am">·</span> APPENDIX B · 术语索引</p>
          <h1 className="h-sec ink" style={s(1)}>用命名过的概念思考</h1>
          <p className="lead flow" style={s(2)}>
            没被命名的直觉留不下来。这 {ideas.length} 条术语是两年 15 场演讲淘出来的思考工具——
            每一条都有定义、有出处、有归卷。引用随意，注明《同一把尺子》colinyao.com 即可。
          </p>
        </Reveal>

        <div className="ideas-grid">
          {ideas.map((idea) => {
            const vol = homeVol.get(idea.id);
            return (
              <Reveal key={idea.id} id={idea.id} className={`idea-card ${idea.accent ?? ""}`} threshold={0.12}>
                <span className="idx flow" style={s(0)}>
                  <span>{idea.index}</span>
                  <span>{idea.since}</span>
                </span>
                <div className="idea-motif">
                  <Motif kind={idea.motif} />
                </div>
                <span className="zh ink" style={s(1)}>{idea.zh}</span>
                <span className="en flow" style={s(2)}>{idea.en}</span>
                <span className="def flow" style={s(3)}>{idea.def}</span>
                <span className="refs flow" style={s(4)}>
                  {vol && (
                    <>
                      归卷：<Link href={vol.href}>{vol.label}</Link>
                      <br />
                    </>
                  )}
                  出处：
                  {idea.refs.map((r, j) => (
                    <span key={j}>
                      {j > 0 && " · "}
                      {r.num ? <Link href={`/talks#t${r.num}`}>{r.label}</Link> : r.label}
                    </span>
                  ))}
                </span>
              </Reveal>
            );
          })}
        </div>

        <Reveal className="mq-block">
          <p className="q spread" style={s(0)}>
            真正的专业，是有一套<br />更早发现错误、更快修正错误的机制。
          </p>
          <div className="mq-line" style={s(2)} />
          <p className="who pop" style={s(3)}>《同一把尺子》· 2026</p>
        </Reveal>
      </div>
    </section>
  );
}
