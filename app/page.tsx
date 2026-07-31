import type { Metadata } from "next";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import RulerScroll from "@/components/RulerScroll";
import Motif from "@/components/Motifs";
import { rays, dimOrder, bindPin, rulerStats } from "@/content/ruler";
import { boundVolumes, bookStats, pieceIndex, talkNumToSlug } from "@/content/book";
import { talks, talkYears, upcoming } from "@/content/talks";
import { ideas } from "@/content/ideas";
import { site } from "@/content/site";

export const metadata: Metadata = {
  title: { absolute: "时空内外 ·《同一把尺子》· 姚光华 Colin" },
  description:
    "时空内外——姚光华（Colin）的思想星盘。时 · 从毫秒到纪元，空 · 从一场对话到全人类，内 · 内观的纵深，外 · Eval 的粒度；41 枚思想钉在四个维度的刻度上。展开是时空内外，合上是《同一把尺子》。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);
const CN = ["一", "二", "三", "四", "五"];

export default function Home() {
  return (
    <>
      {/* ============ 首焦：时空内外星盘 ============ */}
      <RulerScroll />

      {/* ============ 总目 · 四种找法 ============ */}
      <section className="section hairline" id="index">
        <div className="wrap">
          <Reveal className="section-head">
            <p className="eyebrow flow" style={s(0)}>INDEX <span className="am">·</span> 总目</p>
            <h2 className="h-sec ink" style={s(1)}>四种找法，一页收齐</h2>
            <p className="lead flow" style={s(2)}>
              按维（{rulerStats.pins} 钉）、按卷（{bookStats.pieces} 篇）、按时（15 场）、按术语（{ideas.length} 条）。
              同一批思想，四套坐标。
            </p>
            <div className="term-chips flow" style={s(3)}>
              <a href="#dims" className="term-chip">按维 · 时空内外</a>
              <a href="#vols" className="term-chip">按卷 · 五卷</a>
              <a href="#timeline" className="term-chip">按时 · 年表</a>
              <a href="#terms" className="term-chip">按术语 · {ideas.length} 条</a>
            </div>
          </Reveal>

          {/* ---- 按维 ---- */}
          <div id="dims" />
          <Reveal className="section-head" style={{ marginTop: 40 }}>
            <h3 className="h-sub ink" style={s(0)}>按维 <span className="dim3">· 时空内外 · {rulerStats.pins} 钉</span></h3>
          </Reveal>
          {dimOrder.map((id) => rays.find((r) => r.id === id)!).map((ray) => (
            <Reveal key={ray.id}>
              <h4 className="talk-year settle" style={s(0)}>
                {ray.zh} · {ray.name}{" "}
                <Link href={{ time: "/time", space: "/space", inw: "/inward", out: "/outward" }[ray.id]} className="am" style={{ fontSize: 13, letterSpacing: ".14em" }}>
                  维度页 →
                </Link>
              </h4>
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

          {/* ---- 按卷 ---- */}
          <div id="vols" />
          <Reveal className="section-head" style={{ marginTop: 72 }}>
            <h3 className="h-sub ink" style={s(0)}>按卷 <span className="dim3">·《同一把尺子》· {bookStats.pieces} 篇 · {bookStats.pages} 页</span></h3>
            <p className="lead flow" style={s(1)}>论证的顺序。从 <Link href="/preface" className="am">序</Link> 读起，或直接入卷。</p>
          </Reveal>
          {boundVolumes.map((v) => (
            <Reveal key={v.id}>
              <h4 className="talk-year settle" style={s(0)}>
                卷{CN[v.no - 1]} · {v.zh}{" "}
                <Link href={`/${v.id}`} className="am" style={{ fontSize: 13, letterSpacing: ".14em" }}>卷页 →</Link>
              </h4>
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

          {/* ---- 按时 ---- */}
          <div id="timeline" />
          <Reveal className="section-head" style={{ marginTop: 72 }}>
            <h3 className="h-sub ink" style={s(0)}>按时 <span className="dim3">· 演讲年表 · 2024–2026</span></h3>
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
              <h4 className="talk-year settle" style={s(0)}>{year}</h4>
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
                        <h5 className="talk-title">
                          {t.title}
                          {t.star && <span className="star">{"★".repeat(t.star)}</span>}
                        </h5>
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

          {/* ---- 按术语 ---- */}
          <div id="terms" />
          <Reveal className="section-head" style={{ marginTop: 72 }}>
            <h3 className="h-sub ink" style={s(0)}>按术语 <span className="dim3">· {ideas.length} 条 · 引用注明《同一把尺子》colinyao.com</span></h3>
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
            <a href="#top" onClick={undefined}>
              <span className="k">← 回到星盘</span>
              <span className="t">时空内外</span>
            </a>
            <Link href="/preface" className="next">
              <span className="k">合上是同一把尺子 →</span>
              <span className="t">从序开始读</span>
            </Link>
          </Reveal>
        </div>
      </section>

      {/* ============ 关于 · 作者与版权页 ============ */}
      <section className="section hairline" id="about">
        <div className="wrap">
          <Reveal className="section-head">
            <p className="eyebrow flow" style={s(0)}>COLOPHON <span className="am">·</span> 作者与版权页</p>
            <h2 className="h-sec ink" style={s(1)}>姚光华 · Colin Yao</h2>
          </Reveal>

          <div className="about-grid">
            <Reveal className="about-body">
              <p className="flow" style={s(0)}>
                我是<b>姚光华（Colin）</b>，<b>{site.role}</b>。
                一句话说清我在做的事：<b>让对话式智能体从 Demo 走到 Production，从玩具走到伙伴</b>——
                消费级让 AI 像人、<span className="am">被记住</span>；企业级让 AI 像系统、<span className="am">被托付</span>。
              </p>
              <p className="flow" style={s(1)}>
                2024 年至今讲了 15 场公开演讲：RTE 大会、AWS 中国峰会、Google Cloud 开发者大会、
                全球产品经理大会、人人都是产品经理大会、First Prompt Singapore。
                一路磨出了一套自己的概念工具：<b>活人感</b>、<b>体验基准</b>、<b>Vibe SOTA</b>、<b>QoI</b>、
                「模型决定能力上限，引擎决定体验下限」。它们都收在<a href="#terms" className="am">术语总目</a>里。
              </p>
              <p className="flow" style={s(2)}>
                这个网站，展开是<b>时空内外</b>——四把尺子丈量万物；合上是一本正在写的书：
                <b>《同一把尺子》</b>——向外，用 Eval 度量系统哪里偏了；向内，用内观看见自己的判断哪里偏了。
                产品和人，进化机制是同一个——<b>更早发现错误，更快修正错误</b>。
                五卷四十篇，从<Link href="/preface" className="am">序</Link>读起。
              </p>
              <p className="flow" style={s(3)}>
                想找我聊——小红书 / 微信公众号搜「<b>姚光华 Colin</b>」。
              </p>
            </Reveal>

            <Reveal className="about-aside">
              <div className="aside-block">
                <span className="k flow" style={s(0)}>FIND ME</span>
                <div className="link-row flow" style={s(1)}>
                  <span className="n">小红书 / 公众号</span>
                  <span className="v">姚光华 Colin</span>
                </div>
              </div>
              <div className="aside-block">
                <span className="k flow" style={s(2)}>NOW · 2026</span>
                <div className="link-row flow" style={s(3)}>
                  <span className="n">在做</span>
                  <span className="v">声网 AI 产品线 · ConvoAI</span>
                </div>
                <div className="link-row flow" style={s(4)}>
                  <span className="n">在讲</span>
                  <span className="v">从「被托付」到「共事」</span>
                </div>
                <div className="link-row flow" style={s(5)}>
                  <span className="n">在想</span>
                  <span className="v">Eval 与内观</span>
                </div>
              </div>
              <div className="aside-block">
                <span className="k flow" style={s(4)}>本书</span>
                <Link href="/preface" className="link-row flow" style={s(5)}>
                  <span className="n">序</span>
                  <span className="v">同一把尺子 →</span>
                </Link>
                <a href="#vols" className="link-row flow" style={s(6)}>
                  <span className="n">总目</span>
                  <span className="v">5 卷 · 40 篇 →</span>
                </a>
              </div>
            </Reveal>
          </div>

          <Reveal className="mq-block">
            <p className="q spread" style={s(0)}>AI 会重塑世界，<br />而内观会重塑我们。</p>
            <div className="mq-line" style={s(2)} />
            <p className="who pop" style={s(3)}>人人都是产品经理大会 · 2025 · 最后一页</p>
          </Reveal>
        </div>
      </section>
    </>
  );
}
