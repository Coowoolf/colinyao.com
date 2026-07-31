import type { Metadata } from "next";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import Motif from "@/components/Motifs";
import { rays, dimOrder, bindPin, rulerStats } from "@/content/ruler";
import { boundVolumes, bookStats } from "@/content/book";
import { talks, talkYears, upcoming, } from "@/content/talks";
import { pieceIndex, talkNumToSlug } from "@/content/book";
import { ideas } from "@/content/ideas";

export const metadata: Metadata = {
  title: "总目",
  description:
    "《同一把尺子》× 时空内外 · 总目：按维（四把尺子 41 钉）、按卷（五卷 40 篇）、按时（2024–2026 演讲年表）、按术语（8 条概念）——全站唯一的检索处。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);
const CN = ["一", "二", "三", "四", "五"];

export default function IndexPage() {
  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head">
          <p className="eyebrow flow" style={s(0)}>INDEX <span className="am">·</span> 总目</p>
          <h1 className="h-sec ink" style={s(1)}>四种找法，一页收齐</h1>
          <p className="lead flow" style={s(2)}>
            按维（{rulerStats.pins} 钉）、按卷（{bookStats.pieces} 篇）、按时（15 场）、按术语（{ideas.length} 条）。
            同一批思想，四套坐标。
          </p>
          <div className="term-chips flow" style={s(3)}>
            <a href="#dims" className="term-chip">按维 · 时空内外</a>
            <a href="#vols" className="term-chip">按卷 · 五卷</a>
            <a href="#timeline" className="term-chip">按时 · 年表</a>
            <a href="#terms" className="term-chip">按术语 · 8 条</a>
          </div>
        </Reveal>

        {/* ============ 按维 ============ */}
        <div id="dims" />
        <Reveal className="section-head" style={{ marginTop: 40 }}>
          <h2 className="h-sub ink" style={s(0)}>按维 <span className="dim3">· 时空内外 · {rulerStats.pins} 钉</span></h2>
        </Reveal>
        {dimOrder.map((id) => rays.find((r) => r.id === id)!).map((ray) => (
          <Reveal key={ray.id}>
            <h3 className="talk-year settle" style={s(0)}>
              {ray.zh} · {ray.name}{" "}
              <Link href={{ time: "/time", space: "/space", inw: "/inward", out: "/outward" }[ray.id]} className="am" style={{ fontSize: 13, letterSpacing: ".14em" }}>
                维度页 →
              </Link>
            </h3>
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
          </Reveal>
        ))}

        {/* ============ 按卷 ============ */}
        <div id="vols" />
        <Reveal className="section-head" style={{ marginTop: 72 }}>
          <h2 className="h-sub ink" style={s(0)}>按卷 <span className="dim3">·《同一把尺子》· {bookStats.pieces} 篇 · {bookStats.pages} 页</span></h2>
          <p className="lead flow" style={s(1)}>论证的顺序。从 <Link href="/preface" className="am">序</Link> 读起，或直接入卷。</p>
        </Reveal>
        {boundVolumes.map((v) => (
          <Reveal key={v.id}>
            <h3 className="talk-year settle" style={s(0)}>
              卷{CN[v.no - 1]} · {v.zh}{" "}
              <Link href={`/${v.id}`} className="am" style={{ fontSize: 13, letterSpacing: ".14em" }}>卷页 →</Link>
            </h3>
            {v.bound.map((p, i) =>
              p.locked ? (
                <div key={p.slug} className="rlist-pin locked flow" style={{ ...s(Math.min(i, 8)), paddingLeft: 2 }}>
                  <b>{p.no} · {p.title}</b>
                  <span>{p.lockNote}</span>
                </div>
              ) : (
                <a key={p.slug} href={`/${p.slug}`} className="rlist-pin flow" style={{ ...s(Math.min(i, 8)), paddingLeft: 2 }}>
                  <b>{p.no} · {p.title}</b>
                  <span>第 {p.folio} 页 · {p.slides} 页</span>
                </a>
              )
            )}
          </Reveal>
        ))}

        {/* ============ 按时 ============ */}
        <div id="timeline" />
        <Reveal className="section-head" style={{ marginTop: 72 }}>
          <h2 className="h-sub ink" style={s(0)}>按时 <span className="dim3">· 演讲年表 · 2024–2026</span></h2>
        </Reveal>
        <Reveal>
          <div className="upnext flow" style={s(0)}>
            <div>
              <p className="tag">UP NEXT · 卷五 5.10</p>
              <p className="t">{upcoming.title}</p>
              <p className="d">{upcoming.venue} —— {upcoming.summary}</p>
            </div>
            <div className="when">
              {upcoming.date}
              <small>UPCOMING</small>
            </div>
          </div>
        </Reveal>
        {talkYears.map((year) => (
          <Reveal key={year}>
            <h3 className="talk-year settle" style={s(0)}>{year}</h3>
            {talks
              .filter((t) => t.year === year)
              .map((t, i) => {
                const slug = talkNumToSlug[t.num];
                const piece = slug ? pieceIndex.get(slug) : undefined;
                return (
                  <article key={t.num} className="talk-row flow dn" style={s(i + 1)} id={`t${t.num}`}>
                    <div className="talk-meta">
                      <span className="date">{t.date}</span>
                      <span className="venue">{t.venue}</span>
                      {t.role && <span className="chip">{t.role.toUpperCase()}</span>}
                      {t.lang && <span className="chip">EN</span>}
                    </div>
                    <div className="talk-body">
                      <h4 className="talk-title">
                        {t.title}
                        {t.star && <span className="star">{"★".repeat(t.star)}</span>}
                      </h4>
                      <p className="talk-summary">{t.summary}</p>
                      <div className="talk-foot">
                        <span>NO.{String(t.num).padStart(2, "0")}</span>
                        {t.slides && <span>{t.slides} SLIDES</span>}
                        {piece && !piece.locked && (
                          <a href={`/${slug}`} className="am" style={{ textDecoration: "none" }}>
                            卷{CN[piece.vol - 1]} · {piece.no} · 读此篇 →
                          </a>
                        )}
                        {t.tags?.map((tag) => <span key={tag}>#{tag}</span>)}
                      </div>
                    </div>
                  </article>
                );
              })}
          </Reveal>
        ))}

        {/* ============ 按术语 ============ */}
        <div id="terms" />
        <Reveal className="section-head" style={{ marginTop: 72 }}>
          <h2 className="h-sub ink" style={s(0)}>按术语 <span className="dim3">· {ideas.length} 条 · 引用注明《同一把尺子》colinyao.com</span></h2>
        </Reveal>
        <div className="ideas-grid">
          {ideas.map((idea) => (
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
                出处：
                {idea.refs.map((r, j) => (
                  <span key={j}>
                    {j > 0 && " · "}
                    {r.num ? <a href={`#t${r.num}`}>{r.label}</a> : r.label}
                  </span>
                ))}
              </span>
            </Reveal>
          ))}
        </div>

        <Reveal className="vol-nav">
          <Link href="/">
            <span className="k">← 展开</span>
            <span className="t">时空内外</span>
          </Link>
          <Link href="/book" className="next">
            <span className="k">合上 →</span>
            <span className="t">《同一把尺子》· 书</span>
          </Link>
        </Reveal>
      </div>
    </section>
  );
}
