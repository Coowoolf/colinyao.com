import type { Metadata } from "next";
import Reveal from "@/components/Reveal";
import { talks, talkYears, upcoming } from "@/content/talks";
import { pieceIndex, talkNumToSlug } from "@/content/book";

export const metadata: Metadata = {
  title: "附录 A · 演讲年表",
  description:
    "《同一把尺子》附录 A：姚光华（Colin）2024 年以来的公开演讲年表。正文按论证归卷，此处按时间检索：RTE 大会、AWS 中国峰会、Google Cloud 开发者大会、人人都是产品经理大会、First Prompt Singapore。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);
const CN = ["一", "二", "三", "四", "五"];

export default function TalksPage() {
  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head">
          <p className="eyebrow flow" style={s(0)}>附录 A <span className="am">·</span> APPENDIX A · 2024–2026</p>
          <h1 className="h-sec ink" style={s(1)}>演讲年表</h1>
          <p className="lead flow" style={s(2)}>
            正文按论证归卷，年表按时间检索——15 场公开演讲倒序排列，每场标注了它在书中的篇号。
            ★ 为代表作。
          </p>
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
            <h2 className="talk-year settle" style={s(0)}>{year}</h2>
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
                      <h3 className="talk-title">
                        {t.title}
                        {t.star && <span className="star">{"★".repeat(t.star)}</span>}
                      </h3>
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

        <Reveal className="mq-block">
          <p className="q spread" style={s(0)}>下一场，见。</p>
          <div className="mq-line" style={s(2)} />
          <p className="who pop" style={s(3)}>小红书 / 公众号 · 姚光华 COLIN</p>
        </Reveal>
      </div>
    </section>
  );
}
