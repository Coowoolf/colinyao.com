import Link from "next/link";
import Reveal from "@/components/Reveal";
import { boundVolumes, type BoundVolume } from "@/content/book";
import { ideas } from "@/content/ideas";

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);
const CN = ["一", "二", "三", "四", "五"];

/** 卷尾翻页目标：卷一的上一页是序，卷五的下一页是附录 A */
function neighbors(v: BoundVolume) {
  const prev =
    v.no === 1
      ? { href: "/preface", k: "上一页 · 序", t: "同一把尺子" }
      : { href: `/vol${v.no - 1}`, k: `上一卷 · 卷${CN[v.no - 2]}`, t: boundVolumes[v.no - 2].zh };
  const next =
    v.no === 5
      ? { href: "/talks", k: "接下来 · 附录 A", t: "演讲年表" }
      : { href: `/vol${v.no + 1}`, k: `下一卷 · 卷${CN[v.no]}`, t: boundVolumes[v.no].zh };
  return { prev, next };
}

export default function VolumePage({ no }: { no: number }) {
  const v = boundVolumes[no - 1];
  const { prev, next } = neighbors(v);
  const terms = v.concepts
    .map((id) => ideas.find((i) => i.id === id))
    .filter(Boolean) as typeof ideas;

  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head vol-head">
          <span className="voln" aria-hidden="true">{v.hanzi}</span>
          <p className="eyebrow flow" style={s(0)}>
            卷{CN[v.no - 1]} <span className="am">·</span> VOL.{v.no} <span className="am">·</span> {v.en}
          </p>
          <h1 className="h-sec ink" style={s(1)}>
            {v.zh}
            {v.id === "vol5" && <span className="badge-serial" style={{ marginLeft: 18, verticalAlign: "middle" }}>连载中</span>}
          </h1>
          <p className="vol-intro dropcap flow" style={s(2)}>{v.intro}</p>
          {terms.length > 0 && (
            <div className="term-chips flow" style={s(3)}>
              <span className="k">本卷术语</span>
              {terms.map((t) => (
                <Link key={t.id} href={`/ideas#${t.id}`} className="term-chip">{t.zh}</Link>
              ))}
            </div>
          )}
        </Reveal>

        <Reveal className="piece-list">
          {v.bound.map((p, i) =>
            p.locked ? (
              <div key={p.slug} className="piece-row locked flow" style={s(Math.min(i, 9))}>
                <span className="piece-no">
                  {p.no}
                  <small>第 {p.folio} 页</small>
                </span>
                <span>
                  <span className="piece-title">
                    {p.title}
                    <span className="piece-lock">{p.lockNote}</span>
                  </span>
                  <span className="piece-src">{p.source}</span>
                </span>
                <span className="piece-pg">{p.slides} 页</span>
              </div>
            ) : (
              <a key={p.slug} href={`/${p.slug}`} className="piece-row flow" style={s(Math.min(i, 9))}>
                <span className="piece-no">
                  {p.no}
                  <small>第 {p.folio} 页</small>
                </span>
                <span>
                  <span className="piece-title">{p.title}</span>
                  <span className="piece-src">{p.source}</span>
                </span>
                <span className="piece-pg">{p.slides} 页</span>
              </a>
            )
          )}
        </Reveal>

        <Reveal className="vol-nav">
          <Link href={prev.href}>
            <span className="k">← {prev.k}</span>
            <span className="t">{prev.t}</span>
          </Link>
          <Link href={next.href} className="next">
            <span className="k">{next.k} →</span>
            <span className="t">{next.t}</span>
          </Link>
        </Reveal>
      </div>
    </section>
  );
}
