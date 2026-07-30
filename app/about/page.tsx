import type { Metadata } from "next";
import Link from "next/link";
import Reveal from "@/components/Reveal";
import { site } from "@/content/site";

export const metadata: Metadata = {
  title: "About · 关于",
  description: "姚光华（Colin Yao），声网 AI 产品线负责人。做对话式智能体：活人感、被记住·被托付、Vibe SOTA。",
};

const s = (i: number) => ({ ["--i" as string]: i } as React.CSSProperties);

export default function AboutPage() {
  return (
    <section className="section" style={{ paddingTop: "clamp(120px,16vh,180px)" }}>
      <div className="wrap">
        <Reveal className="section-head">
          <p className="eyebrow flow" style={s(0)}>ABOUT <span className="am">·</span> 关于</p>
          <h1 className="h-sec ink" style={s(1)}>姚光华 · Colin Yao</h1>
        </Reveal>

        <div className="about-grid">
          <Reveal className="about-body">
            <p className="flow" style={s(0)}>
              我是<b>姚光华（Colin）</b>，<b>{site.role}</b>，负责对话式 AI 引擎 ConvoAI。
              一句话说清我在做的事：<b>让对话式智能体从 Demo 走到 Production，从玩具走到伙伴</b>——
              消费级让 AI 像人、<span className="am">被记住</span>；企业级让 AI 像系统、<span className="am">被托付</span>。
            </p>
            <p className="flow" style={s(1)}>
              2024 年至今讲了 15 场公开演讲：RTE 大会、AWS 中国峰会、Google Cloud 开发者大会、
              全球产品经理大会、人人都是产品经理大会、First Prompt Singapore。
              一路磨出了一套自己的概念工具：<b>活人感</b>、<b>体验基准</b>、<b>Vibe SOTA</b>、<b>QoI</b>、
              「模型决定能力上限，引擎决定体验下限」。它们都收在<Link href="/ideas" className="am">概念库</Link>里。
            </p>
            <p className="flow" style={s(2)}>
              这个网站叫「同一把尺子」：向外，用 Eval 度量系统哪里偏了；向内，用内观看见自己的判断哪里偏了。
              产品和人，进化机制是同一个——<b>更早发现错误，更快修正错误</b>。
            </p>
            <p className="flow" style={s(3)}>
              演讲邀约、产品切磋、或者只是想聊聊 Voice Agent 的 vibe——写信给我。
            </p>
          </Reveal>

          <Reveal className="about-aside">
            <div className="aside-block">
              <span className="k flow" style={s(0)}>CONTACT</span>
              {site.links.map((l, i) => (
                <a key={l.name} href={l.href} className="link-row flow" style={s(i + 1)}
                  target={l.href.startsWith("http") ? "_blank" : undefined} rel="noreferrer">
                  <span className="n">{l.name}</span>
                  <span className="v">{l.value}</span>
                </a>
              ))}
            </div>
            <div className="aside-block">
              <span className="k flow" style={s(2)}>NOW · 2026</span>
              <div className="link-row flow" style={s(3)}>
                <span className="n">在做</span>
                <span className="v">ConvoAI · 对话式 AI 引擎</span>
              </div>
              <div className="link-row flow" style={s(4)}>
                <span className="n">在讲</span>
                <span className="v">对话式智能体的信任进化</span>
              </div>
              <div className="link-row flow" style={s(5)}>
                <span className="n">在想</span>
                <span className="v">Eval 与内观</span>
              </div>
            </div>
            <div className="aside-block">
              <span className="k flow" style={s(4)}>ELSEWHERE</span>
              <Link href="/talks" className="link-row flow" style={s(5)}>
                <span className="n">演讲档案</span>
                <span className="v">15 TALKS →</span>
              </Link>
              <Link href="/ideas" className="link-row flow" style={s(6)}>
                <span className="n">概念库</span>
                <span className="v">8 IDEAS →</span>
              </Link>
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
  );
}
