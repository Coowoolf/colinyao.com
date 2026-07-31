import Link from "next/link";
import Reveal from "@/components/Reveal";
import RulerFig from "@/components/RulerFig";
import Motif from "@/components/Motifs";
import { site } from "@/content/site";
import { book, boundVolumes, bookStats } from "@/content/book";
import { upcoming } from "@/content/talks";

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

export default function Home() {
  return (
    <>
      {/* ============ 封面 ============ */}
      <Reveal as="section" className="hero">
        <div className="wrap">
          <p className="cover-author flow" style={s(0)}>
            {book.author} 著 <span className="am">·</span> {book.en} <span className="am">·</span> 2024–2026 连载中
          </p>
          <h1 className="h-hero hero-quote">
            <i className="spread" style={s(1)}>{book.title}</i>
          </h1>
          <div className="mq-line" style={s(4)} />
          <p className="cover-sub flow" style={s(5)}>
            向外叫 <span className="am">Eval</span>，向内叫<span className="am">内观</span>。
          </p>
          <p className="hero-sub flow" style={s(6)}>
            一本正在写的书。两年、十五场演讲、二十三篇文章，按<b>论证的顺序</b>重新装订：
            先铸尺，再量向外的两个半球，最后把尺子转向自己。
          </p>
          <div className="hero-ctas">
            <Link href="/preface" className="cta flow" style={s(7)}>从序开始读 →</Link>
            <Link href="/ruler" className="cta flow" style={s(8)}>展开活页 · 时空内外 ↗</Link>
            <a href="#toc" className="cta ghost flow" style={s(9)}>目录 ↓</a>
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
              <span className="l flow" style={s(0)}>VOLUMES</span>
              <span className="n settle" style={s(1)}>{bookStats.volumes}</span>
              <div className="stat-motif flow" style={s(2)}><Motif kind="steps" plain /></div>
              <span className="d flow" style={s(3)}>卷：尺子 · 活人感 · 被托付 · 同源进化 · 内观</span>
            </div>
            <div className="stat">
              <span className="l flow" style={s(2)}>PIECES</span>
              <span className="n settle" style={s(3)}>{bookStats.pieces}</span>
              <div className="stat-motif flow" style={s(4)}><Motif kind="sota" plain /></div>
              <span className="d flow" style={s(5)}>篇：演讲、文章与课程，每一篇都有归卷与页码</span>
            </div>
            <div className="stat">
              <span className="l flow" style={s(4)}>PAGES</span>
              <span className="n settle" style={s(5)}>{bookStats.pages}</span>
              <div className="stat-motif flow" style={s(6)}><Motif kind="tb" plain /></div>
              <span className="d flow" style={s(7)}>页，页边码全书连续——还在往后长</span>
            </div>
          </div>
        </div>
      </Reveal>

      {/* ============ 总目录 ============ */}
      <section className="section" id="toc">
        <div className="wrap">
          <Reveal className="section-head">
            <p className="eyebrow flow" style={s(0)}>CONTENTS <span className="am">·</span> 总目录</p>
            <h2 className="h-sec ink" style={s(1)}>五卷，四十篇</h2>
            <p className="lead flow" style={s(2)}>
              组织原则只有一个：论证的顺序。读者从序进，按卷读；熟客直接翻附录检索。
            </p>
          </Reveal>
          <Reveal className="toc">
            <Link href="/preface" className="toc-row flow" style={s(0)}>
              <span className="no">序</span>
              <span className="name">同一把尺子</span>
              <span className="en">PREFACE</span>
              <span className="toc-leader" />
              <span className="pg">卷首</span>
            </Link>
            <Link href="/ruler" className="toc-row flow" style={s(1)}>
              <span className="no">活页</span>
              <span className="name">时空内外</span>
              <span className="en">TIME · SPACE · IN · OUT</span>
              <span className="badge-serial">四个维度</span>
              <span className="toc-leader" />
              <span className="pg">41 钉 · 滚动展开</span>
            </Link>
            {boundVolumes.map((v, i) => (
              <Link key={v.id} href={`/${v.id}`} className="toc-row flow" style={s(i + 1)}>
                <span className="no">卷{["一", "二", "三", "四", "五"][v.no - 1]}</span>
                <span className="name">{v.zh}</span>
                <span className="en">{v.en}</span>
                {v.id === "vol5" && <span className="badge-serial">连载中</span>}
                <span className="toc-leader" />
                <span className="pg">{v.pieces.length} 篇 · 第 {v.folio} 页</span>
              </Link>
            ))}
            <Link href="/talks" className="toc-row appendix flow" style={s(6)}>
              <span className="no">附 A</span>
              <span className="name">演讲年表</span>
              <span className="en">APPENDIX A</span>
              <span className="toc-leader" />
              <span className="pg">2024–2026</span>
            </Link>
            <Link href="/ideas" className="toc-row appendix flow" style={s(7)}>
              <span className="no">附 B</span>
              <span className="name">术语索引</span>
              <span className="en">APPENDIX B</span>
              <span className="toc-leader" />
              <span className="pg">8 条</span>
            </Link>
          </Reveal>
        </div>
      </section>

      {/* ============ 腰封金句 ============ */}
      <Reveal as="section" className="hairline">
        <div className="wrap mq-block">
          <p className="eyebrow flow" style={s(0)}>腰封 · MONEY QUOTE</p>
          <p className="q spread" style={s(1)}>
            模型决定能力上限，<br />引擎决定体验下限。
          </p>
          <div className="mq-line" style={s(3)} />
          <p className="who pop" style={s(4)}>卷四 · 同源进化 · AWS 中国峰会 2026</p>
        </div>
      </Reveal>

      {/* ============ 正在写的一章 ============ */}
      <Reveal as="section" className="section hairline">
        <div className="wrap">
          <div className="section-head">
            <p className="eyebrow flow" style={s(0)}>NOW WRITING <span className="am">·</span> 正在写的一章</p>
          </div>
          <Link href="/vol5" style={{ textDecoration: "none", color: "inherit", display: "block" }}>
            <div className="upnext flow" style={s(1)}>
              <div>
                <p className="tag">卷五 · 5.10</p>
                <p className="t">{upcoming.title}</p>
                <p className="d">{upcoming.venue} —— {upcoming.summary}</p>
              </div>
              <div className="when">
                {upcoming.date}
                <small>首发后开放</small>
              </div>
            </div>
          </Link>
        </div>
      </Reveal>

      {/* ============ 版权页 CTA ============ */}
      <Reveal as="section" className="section hairline">
        <div className="wrap">
          <div className="section-head">
            <p className="eyebrow flow" style={s(0)}>COLOPHON</p>
            <h2 className="h-sec ink" style={s(1)}>关于作者</h2>
            <p className="lead flow" style={s(2)}>
              姚光华（Colin），{site.role}。这本书写对话式智能体，也写与 AI 共事的人。
            </p>
            <div className="hero-ctas">
              {site.links.map((l, i) => (
                <span key={l.name} className="cta flow" style={s(3 + i)}>{l.name} · {l.value}</span>
              ))}
              <Link href="/about" className="cta ghost flow" style={s(5)}>作者与版权页 →</Link>
            </div>
          </div>
        </div>
      </Reveal>
    </>
  );
}
