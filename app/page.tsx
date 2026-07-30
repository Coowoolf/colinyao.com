import Link from "next/link";
import Reveal from "@/components/Reveal";
import RulerFig from "@/components/RulerFig";
import { site } from "@/content/site";
import { ideas } from "@/content/ideas";
import { talks, upcoming } from "@/content/talks";

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

/** 卡片摘要：在 90 字以内的最后一个句读处截断 */
function preview(def: string) {
  if (def.length <= 90) return def;
  const head = def.slice(0, 90);
  const cut = Math.max(head.lastIndexOf("。"), head.lastIndexOf("；"), head.lastIndexOf("——"));
  return cut > 30 ? head.slice(0, cut + 1) : head + "……";
}

export default function Home() {
  const featured = ideas.slice(0, 4);
  const latest = talks.slice(0, 3);

  return (
    <>
      {/* ============ HERO · 钉子句 ============ */}
      <Reveal as="section" className="hero">
        <div className="wrap">
          <p className="eyebrow flow" style={s(0)}>
            COLINYAO.COM <span className="am">·</span> {site.ruler.en}
          </p>
          <h1 className="h-hero hero-quote">
            <i className="spread" style={s(1)}>{site.ruler.zh[0]}</i>
            <i className="spread" style={s(3)}>{site.ruler.zh[1]}</i>
            <i className="spread" style={s(5)}>{site.ruler.zh[2]}</i>
          </h1>
          <div className="mq-line" style={s(6)} />
          <p className="hero-sub flow" style={s(7)}>
            我是<b>姚光华（Colin）</b>，{site.role}。做对话式智能体：让它有<b>活人感</b>、
            被记住、被托付；也把「感觉对了」这件事，做成可测量的尺子。
          </p>
          <div className="hero-ctas">
            <Link href="/talks" className="cta flow" style={s(8)}>15 场公开演讲 →</Link>
            <Link href="/ideas" className="cta ghost flow" style={s(9)}>概念库 →</Link>
          </div>
          <RulerFig />
        </div>
        <div className="hero-scroll" aria-hidden="true">SCROLL</div>
      </Reveal>

      {/* ============ 数字带 ============ */}
      <Reveal as="section">
        <div className="wrap">
          <div className="stats">
            <div className="stat">
              <span className="l flow" style={s(0)}>TALKS · SINCE 2024</span>
              <span className="n settle" style={s(1)}>15<em>+</em></span>
              <span className="d flow" style={s(2)}>场公开演讲，从 RTE 大会到 AWS 中国峰会</span>
            </div>
            <div className="stat">
              <span className="l flow" style={s(2)}>HEMISPHERES</span>
              <span className="n settle" style={s(3)}>2</span>
              <span className="d flow" style={s(4)}>个半球：被记住的消费级 × 被托付的企业级</span>
            </div>
            <div className="stat">
              <span className="l flow" style={s(4)}>RULER</span>
              <span className="n settle" style={s(5)}>1</span>
              <span className="d flow" style={s(6)}>把尺子：向外叫 Eval，向内叫内观</span>
            </div>
          </div>
        </div>
      </Reveal>

      {/* ============ IDEAS 精选 ============ */}
      <section className="section">
        <div className="wrap">
          <Reveal className="section-head">
            <p className="eyebrow flow" style={s(0)}>IDEAS <span className="am">·</span> 概念库</p>
            <h2 className="h-sec ink" style={s(1)}>用命名过的概念思考</h2>
            <p className="lead flow" style={s(2)}>
              这些词是在 15 场演讲里一点点磨出来的。每个概念都有出处、有定义、有下文——这里是它们的官方档案。
            </p>
          </Reveal>
          <Reveal className="ideas-grid">
            {featured.map((idea, i) => (
              <Link key={idea.id} href={`/ideas#${idea.id}`} className={`idea-card flow ${idea.accent ?? ""}`} style={s(i * 2)}>
                <span className="idx"><span>{idea.index}</span><span>{idea.since}</span></span>
                <span className="zh">{idea.zh}</span>
                <span className="en">{idea.en}</span>
                <span className="def">{preview(idea.def)}</span>
              </Link>
            ))}
          </Reveal>
          <Reveal className="end-cta">
            <Link href="/ideas" className="cta flow" style={s(1)}>全部 {ideas.length} 个概念 →</Link>
          </Reveal>
        </div>
      </section>

      {/* ============ 金句区块 ============ */}
      <Reveal as="section" className="hairline">
        <div className="wrap mq-block">
          <p className="eyebrow flow" style={s(0)}>MONEY QUOTE</p>
          <p className="q spread" style={s(1)}>
            模型决定能力上限，<br />引擎决定体验下限。
          </p>
          <div className="mq-line" style={s(3)} />
          <p className="who pop" style={s(4)}>AWS 中国峰会 · 2026.06 · SLIDE 34</p>
        </div>
      </Reveal>

      {/* ============ TALKS 最新 ============ */}
      <section className="section hairline">
        <div className="wrap">
          <Reveal className="section-head">
            <p className="eyebrow flow" style={s(0)}>TALKS <span className="am">·</span> 演讲档案</p>
            <h2 className="h-sec ink" style={s(1)}>两年，十五场，一条思想演进线</h2>
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
          <Reveal>
            {latest.map((t, i) => (
              <article key={t.num} className="talk-row flow dn" style={s(i * 2 + 2)}>
                <div className="talk-meta">
                  <span className="date">{t.date}</span>
                  <span className="venue">{t.venue}</span>
                </div>
                <div className="talk-body">
                  <h3 className="talk-title">
                    {t.title}
                    {t.star && <span className="star">{"★".repeat(t.star)}</span>}
                  </h3>
                  <p className="talk-summary">{t.summary}</p>
                </div>
              </article>
            ))}
          </Reveal>
          <Reveal className="end-cta">
            <Link href="/talks" className="cta flow" style={s(1)}>完整档案 · 2024–2026 →</Link>
          </Reveal>
        </div>
      </section>

      {/* ============ 收尾 ============ */}
      <Reveal as="section" className="section hairline">
        <div className="wrap">
          <div className="section-head">
            <p className="eyebrow flow" style={s(0)}>FIND ME</p>
            <h2 className="h-sec ink" style={s(1)}>聊聊对话式智能体</h2>
            <p className="lead flow" style={s(2)}>
              Voice Agent 的 vibe、活人感的工程、AI 产品的手艺——这些话题永远聊得动。
            </p>
            <div className="hero-ctas">
              {site.links.map((l, i) => (
                <span key={l.name} className="cta flow" style={s(3 + i)}>{l.name} · {l.value}</span>
              ))}
              <Link href="/about" className="cta ghost flow" style={s(5)}>关于我 →</Link>
            </div>
          </div>
        </div>
      </Reveal>
    </>
  );
}
