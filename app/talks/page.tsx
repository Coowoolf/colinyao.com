import type { Metadata } from "next";
import Reveal from "@/components/Reveal";
import { talks, talkYears, upcoming } from "@/content/talks";

export const metadata: Metadata = {
  title: "Talks · 演讲档案",
  description:
    "姚光华（Colin）2024 年以来的公开演讲档案：RTE 大会、AWS 中国峰会、Google Cloud 开发者大会、人人都是产品经理大会、First Prompt Singapore。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

export default function TalksPage() {
  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head">
          <p className="eyebrow flow" style={s(0)}>TALKS <span className="am">·</span> 2024–2026</p>
          <h1 className="h-sec ink" style={s(1)}>演讲档案</h1>
          <p className="lead flow" style={s(2)}>
            15 场公开演讲，按时间倒序。这不是作品集——是一条能看见思想怎么长出来的演进线：
            从三阶段框架，到活人感，到两个半球，到同一把尺子。★ 为代表作。
          </p>
        </Reveal>

        <Reveal>
          <div className="upnext flow" style={s(0)}>
            <div>
              <p className="tag">UP NEXT</p>
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
              .map((t, i) => (
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
                      {t.tags?.map((tag) => <span key={tag}>#{tag}</span>)}
                    </div>
                  </div>
                </article>
              ))}
          </Reveal>
        ))}

        <Reveal className="mq-block">
          <p className="q spread" style={s(0)}>下一场，见。</p>
          <div className="mq-line" style={s(2)} />
          <p className="who pop" style={s(3)}>演讲邀约 · ICOLINYAO@GMAIL.COM</p>
        </Reveal>
      </div>
    </section>
  );
}
