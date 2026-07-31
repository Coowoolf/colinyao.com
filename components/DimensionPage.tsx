import Link from "next/link";
import Reveal from "@/components/Reveal";
import RulerCompass from "@/components/RulerCompass";
import { rays, dimOrder, bindPin, type Ray } from "@/content/ruler";
import { ideas } from "@/content/ideas";

/** 维度页：该维的目录——单尺活图（锁定本维 · 钉可点）+ 逐站钉列表 + 本维术语 + 翻页 */

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);
const CN: Record<string, string> = { time: "时", space: "空", inw: "内", out: "外" };
const ROUTE: Record<string, string> = { time: "/time", space: "/space", inw: "/inward", out: "/outward" };

export default function DimensionPage({ id }: { id: Ray["id"] }) {
  const ray = rays.find((r) => r.id === id)!;
  const k = dimOrder.indexOf(id);
  const prev =
    k === 0
      ? { href: "/", k: "← 回到星盘", t: "时空内外" }
      : { href: ROUTE[dimOrder[k - 1]], k: `← 上一维 · ${CN[dimOrder[k - 1]]}`, t: rays.find((r) => r.id === dimOrder[k - 1])!.name };
  const next =
    k === 3
      ? { href: "/book", k: "合上是同一把尺子 →", t: "《同一把尺子》· 书" }
      : { href: ROUTE[dimOrder[k + 1]], k: `下一维 · ${CN[dimOrder[k + 1]]} →`, t: rays.find((r) => r.id === dimOrder[k + 1])!.name };
  const terms = ray.terms.map((t) => ideas.find((i) => i.id === t)).filter(Boolean) as typeof ideas;

  return (
    <>
      {/* 单尺活图：星盘锁定本维，常驻流动，钉可点 */}
      <div className="dimpage">
        <div className="rstage" data-dim={id} data-fold={0}>
          <RulerCompass interactive idPrefix={`dp-${id}`} />
          <div className="dim-head">
            <p className="eyebrow">第{["一", "二", "三", "四"][k]}维 <span className="am">·</span> {ray.name} <span className="am">·</span> {ray.en}</p>
            <h1 className="dim-title">{ray.zh}</h1>
          </div>
        </div>
      </div>

      <section className="section" style={{ paddingTop: "clamp(40px,6vh,72px)" }}>
        <div className="wrap">
          <Reveal className="section-head" style={{ marginBottom: 20 }}>
            <p className="vol-intro dropcap flow" style={s(0)}>{ray.intro}</p>
            {terms.length > 0 && (
              <div className="term-chips flow" style={s(1)}>
                <span className="k">本维术语</span>
                {terms.map((t) => (
                  <Link key={t.id} href={`/toc#${t.id}`} className="term-chip">{t.zh}</Link>
                ))}
              </div>
            )}
          </Reveal>

          <Reveal>
            {ray.stations.map((st, i) => (
              <div key={st.id} className="rlist-station flow" style={s(Math.min(i, 8))}>
                <div className="rlist-head">
                  <span className="lab">{st.label}</span>
                  <span className="tick">{st.tick}</span>
                </div>
                <div className="rlist-pins">
                  {st.pins.map(bindPin).map((pin) =>
                    pin.href ? (
                      <a key={pin.slug ?? pin.title} href={pin.href} className="rlist-pin">
                        <b>{pin.title}</b>
                        <span>{pin.reading}{pin.vol ? ` · ${pin.vol}` : ""}</span>
                      </a>
                    ) : (
                      <div key={pin.slug ?? pin.title} className="rlist-pin locked">
                        <b>{pin.title}</b>
                        <span>{pin.reading} · 连载中 2026.08</span>
                      </div>
                    )
                  )}
                </div>
              </div>
            ))}
            <p className="rlist-beyond flow" style={s(9)}>刻度之外：{ray.beyond} →</p>
          </Reveal>

          <Reveal className="vol-nav">
            <Link href={prev.href}>
              <span className="k">{prev.k}</span>
              <span className="t">{prev.t}</span>
            </Link>
            <Link href={next.href} className="next">
              <span className="k">{next.k}</span>
              <span className="t">{next.t}</span>
            </Link>
          </Reveal>
        </div>
      </section>
    </>
  );
}
