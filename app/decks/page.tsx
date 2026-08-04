import type { Metadata } from "next";
import Reveal from "@/components/Reveal";
import { speechDecks, talkDecks, essayDecks } from "@/content/decks";

export const metadata: Metadata = {
  title: "Deck Index",
  robots: { index: false, follow: false },
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

export default function DecksIndex() {
  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head">
          <p className="eyebrow flow" style={s(0)}>DECK INDEX <span className="am">·</span> 私享库</p>
          <h1 className="h-sec ink" style={s(1)}>Deck 索引</h1>
          <p className="lead flow" style={s(2)}>
            此页无入口、不收录，地址只有你知道。所有 deck 深浅双主题：
            左下角切换，或跟随全站主题偏好。← / → 翻页。
          </p>
        </Reveal>

        <Reveal>
          <h2 className="talk-year settle" style={s(0)}>演讲 · 课程</h2>
          {speechDecks.map((d, i) =>
            d.locked ? (
              <div key={d.slug} className="talk-row flow dn" style={{ ...s(i + 1), opacity: 0.55 }}>
                <div className="talk-meta">
                  <span className="date">/{d.slug}</span>
                  <span className="venue">{d.slides} SLIDES · 连载中</span>
                </div>
                <div className="talk-body">
                  <h3 className="talk-title" style={{ fontSize: "clamp(17px,1.8vw,21px)" }}>{d.title}</h3>
                </div>
              </div>
            ) : (
              <a key={d.slug} href={`/${d.slug}`} className="talk-row flow dn" style={s(i + 1)}>
                <div className="talk-meta">
                  <span className="date">/{d.slug}</span>
                  <span className="venue">{d.slides} SLIDES</span>
                </div>
                <div className="talk-body">
                  <h3 className="talk-title" style={{ fontSize: "clamp(17px,1.8vw,21px)" }}>{d.title}</h3>
                </div>
              </a>
            )
          )}
        </Reveal>

        <Reveal>
          <h2 className="talk-year settle" style={s(0)}>对外演讲全集 · 2024–2026</h2>
          {talkDecks.map((d, i) => (
            <a key={d.slug} href={`/${d.slug}`} className="talk-row flow dn" style={s(Math.min(i + 2, 10))}>
              <div className="talk-meta">
                <span className="date">/{d.slug}</span>
                <span className="venue">{d.date} · {d.slides} SLIDES</span>
              </div>
              <div className="talk-body">
                <h3 className="talk-title" style={{ fontSize: "clamp(17px,1.8vw,21px)" }}>{d.title}</h3>
                <p className="talk-summary">{d.venue}</p>
              </div>
            </a>
          ))}
        </Reveal>

        <Reveal>
          <h2 className="talk-year settle" style={s(0)}>公众号 · 文章 Deck</h2>
          {essayDecks.map((d, i) =>
            d.locked ? (
              <div key={d.slug} className="talk-row flow dn" style={{ ...s(Math.min(i + 1, 10)), opacity: 0.55 }}>
                <div className="talk-meta">
                  <span className="date">/{d.slug}</span>
                  <span className="venue">NO.{d.num} · {d.slides} SLIDES · 连载中</span>
                </div>
                <div className="talk-body">
                  <h3 className="talk-title" style={{ fontSize: "clamp(17px,1.8vw,21px)" }}>{d.title}</h3>
                </div>
              </div>
            ) : (
              <a key={d.slug} href={`/${d.slug}`} className="talk-row flow dn" style={s(Math.min(i + 1, 10))}>
                <div className="talk-meta">
                  <span className="date">/{d.slug}</span>
                  <span className="venue">NO.{d.num} · {d.slides} SLIDES</span>
                </div>
                <div className="talk-body">
                  <h3 className="talk-title" style={{ fontSize: "clamp(17px,1.8vw,21px)" }}>{d.title}</h3>
                </div>
              </a>
            )
          )}
        </Reveal>

        <Reveal className="mq-block">
          <p className="q spread" style={s(0)}>先在现场做十遍，<br />再给第十一次起一个产品名。</p>
          <div className="mq-line" style={s(2)} />
          <p className="who pop" style={s(3)}>{speechDecks.length + talkDecks.length + essayDecks.length} DECKS · ALL DUAL-THEME</p>
        </Reveal>
      </div>
    </section>
  );
}
