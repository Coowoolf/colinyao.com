import type { Metadata } from "next";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import RulerScroll from "@/components/RulerScroll";
import { rays, rulerStats, bindPin } from "@/content/ruler";

export const metadata: Metadata = {
  title: "时空内外 · 四把尺子",
  description:
    "《同一把尺子》的活页：时空内外，四把尺子。时 · 从毫秒到纪元，空 · 从一场对话到全人类，内 · 内观的纵深，外 · Eval 的粒度——41 枚思想钉在各自的刻度上。合上是同一把，展开是时空内外。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

export default function RulerPage() {
  return (
    <>
      {/* 首焦即星盘：不滚自转循环，滚动逐把展开，滚完全图可点 */}
      <RulerScroll />

      {/* 读法 · 逐格清单（移动端主视图 / 无 JS 降级 / 检索） */}
      <section className="section hairline" id="list">
        <div className="wrap">
          <Reveal className="section-head">
            <p className="eyebrow flow" style={s(0)}>READINGS <span className="am">·</span> 逐格读数</p>
            <h2 className="h-sec ink" style={s(1)}>四把尺子，{rulerStats.stations} 格刻度</h2>
            <p className="lead flow" style={s(2)}>
              站 = 论证对象所在的刻度；读数 = 那一篇的签名数字。每一枚钉都可展开成一份 deck。
            </p>
          </Reveal>
          {rays.map((ray) => (
            <Reveal key={ray.id}>
              <h3 className="talk-year settle" style={s(0)}>
                {ray.zh} · {ray.name} <span className="dim3" style={{ fontSize: 13, letterSpacing: ".18em" }}>{ray.en}</span>
              </h3>
              {ray.stations.map((st, i) => (
                <div key={st.id} className="rlist-station flow" style={s(Math.min(i + 1, 8))}>
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
          ))}

          <Reveal className="vol-nav">
            <Link href="/">
              <span className="k">← 封面</span>
              <span className="t">《同一把尺子》</span>
            </Link>
            <Link href="/preface" className="next">
              <span className="k">合上活页 · 回到正文 →</span>
              <span className="t">序 · 同一把尺子</span>
            </Link>
          </Reveal>
        </div>
      </section>
    </>
  );
}
