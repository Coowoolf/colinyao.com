import { allDecks, type Deck } from "./decks";

/** ============================================================
 *  《同一把尺子》· 成书数据层
 *  组织原则：论证的顺序，不是时间的顺序。
 *  加一篇新内容 = decks.ts 加一行 + 在对应卷的 pieces 里插一个 slug。
 *  目录、篇号、页边码全部由此文件推导，零手工维护。
 *  ============================================================ */

export const book = {
  title: "同一把尺子",
  en: "THE SAME RULER",
  subtitle: "向外叫 Eval，向内叫内观。",
  author: "姚光华 Colin",
  edition: "初版 2026 · 连载中",
};

export type Piece = {
  slug: string;
  /** 连载中：目录列出但不挂链接（如 /trust 首发前防剧透） */
  locked?: boolean;
  lockNote?: string;
};

export type Volume = {
  id: string; // vol1…vol5
  no: number;
  hanzi: string; // 壹—伍（卷号大字）
  zh: string;
  en: string;
  /** 目录里的一行小注 */
  sub: string;
  /** 卷首语（约 250 字，首字下沉） */
  intro: string;
  /** 本卷术语（/ideas 概念 id） */
  concepts: string[];
  pieces: Piece[];
};

/** 序（不计页码，位于 /preface） */
export const preface = {
  zh: "同一把尺子",
  en: "PREFACE · THE SAME RULER",
  intro: [
    "两年，十五场演讲，二十三篇文章。它们看起来讲的是对话式智能体——活人感、被记住、被托付——但把它们摊开在同一张桌面上，我才看清自己一直在做的只有一件事：铸一把尺子。",
    "向外，它叫 Eval：看见系统哪里偏了，把争论变成实验。向内，它叫内观：看见自己的判断哪里偏了，允许自己改错。产品和人，进化机制是同一个——更早发现错误，更快修正错误。",
    "这本书按论证的顺序重新装订了这两年：先铸尺（卷一），再量向外的两个半球——被记住的消费级（卷二）与被托付的企业级（卷三），然后发现它们共享同一颗引擎（卷四），最后把尺子转向自己（卷五）。",
    "它还在写。",
  ],
};

export const volumes: Volume[] = [
  {
    id: "vol1",
    no: 1,
    hanzi: "壹",
    zh: "尺子",
    en: "THE RULER",
    sub: "怎么测量「感觉对了」",
    intro:
      "所有人都在谈体验，没有人敢给体验一个刻度。二〇二四年十月，我在 RTE 大会上画下第一把尺子：QoS、QoE、AI QoE——网络的质量、人的感受、智能的分寸，三段刻度，一条直线。此后两年我做的所有事，不过是把这把尺子越磨越细：把「感觉对了」翻译成可以跑的评测，把 demo 的谎言摊在横评的日光下，把一整段对话的死法逐轮验尸。评测即 PRD——在 AI 时代，产品经理交付的不再是功能清单，而是一把别人可以复用的尺子。这一卷讲的就是铸尺的过程。",
    concepts: ["four-steps", "vibe-sota", "eval-prd", "turns-wrong"],
    pieces: [
      { slug: "rte24" },
      { slug: "pm24" },
      { slug: "evalprd" },
      { slug: "demolies" },
      { slug: "voiceeval" },
      { slug: "turns" },
      { slug: "interrupted" },
      { slug: "vibecheck" },
      { slug: "vibesota" },
    ],
  },
  {
    id: "vol2",
    no: 2,
    hanzi: "貳",
    zh: "活人感",
    en: "ALIVENESS",
    sub: "被记住的消费级半球",
    intro:
      "消费级的终局不是更聪明，是被记住。AI 对话产品的根本缺陷从来不在参数和榜单里，在「不像一个活人在跟你说话」：响应的节奏、打断的从容、情绪的呼应、记得你是谁。这一卷从「活人感」的命名开始，到角色三件套的工程框架，到 0.29TB——一个人生命上下文的物理上限，也是机器人成为伙伴的记忆配额。玩具与伙伴的分水岭不是智能，是角色；从被使用，到被记住。",
    concepts: ["aliveness", "qoi", "tb", "role-triad"],
    pieces: [
      { slug: "pm25" },
      { slug: "tolan" },
      { slug: "robot26" },
      { slug: "029tb" },
      { slug: "audio25" },
      { slug: "presence" },
      { slug: "elys" },
      { slug: "staas" },
    ],
  },
  {
    id: "vol3",
    no: 3,
    hanzi: "叁",
    zh: "被托付",
    en: "ENTRUSTED",
    sub: "被信任的企业级半球",
    intro:
      "企业不为「像人」付费，企业为「可托付」付费。客服是第一个被真金白银验证的智能体场景：96.5% 的用户没有分辨出 AI，营销转化超过人类销冠——但数字只是入场券。真正的门槛是五维金标准，是一通电话结束 72 小时后才敢结算的 outcome，是把工程师送进客户现场的最后一公里。这一卷讲企业级半球：先让 AI 像系统一样可靠，然后才配像同事一样被托付。",
    concepts: ["gold-standard", "settle-72h", "not-the-model"],
    pieces: [
      { slug: "inspire26" },
      { slug: "csagent" },
      { slug: "outcome" },
      { slug: "prodready" },
      { slug: "awsfde" },
      { slug: "34days" },
    ],
  },
  {
    id: "vol4",
    no: 4,
    hanzi: "肆",
    zh: "同源进化",
    en: "ONE ENGINE",
    sub: "两个物种，同一颗引擎",
    intro:
      "两个半球看起来在分道扬镳：消费级越来越像人，企业级越来越像系统。但拆开看，它们共享同一段 DNA——同一颗实时引擎、同一套打断与轮次、同一条「模型决定能力上限，引擎决定体验下限」的物理定律。所有人都在卷上限，用户流失却发生在下限：一次没接住的打断，比答错一道题伤得更重。这一卷是合体——物种分化，同源进化；QoS、QoE 之后，为人和模型共同设计的第三纪元。",
    concepts: ["hemispheres", "bounds"],
    pieces: [
      { slug: "engine25" },
      { slug: "era3" },
      { slug: "convoai" },
      { slug: "arch" },
      { slug: "bottleneck" },
      { slug: "dual26" },
      { slug: "aws26" },
    ],
  },
  {
    id: "vol5",
    no: 5,
    hanzi: "伍",
    zh: "内观",
    en: "INWARD",
    sub: "向内的那把尺子 · 连载中",
    intro:
      "写到这里，尺子转了个方向。带一个 AI 新同事上班，17 小时 150 轮对话，一个 side project 的 77 天——AI 让执行变便宜，high agency 让人变贵，而比 high agency 更稀缺的，是把自己也放上评测台的勇气。向外我用 Eval 度量系统，向内我用内观度量自己：四次跃迁，每一次都是先承认上一版的自己错了。这一卷还没写完——信任进化，八月上台。",
    concepts: ["ruler", "agency-price", "compounding", "time-fx", "cowork-next"],
    pieces: [
      { slug: "highagency" },
      { slug: "newcollege" },
      { slug: "4mtokens" },
      { slug: "3days" },
      { slug: "systemcard" },
      { slug: "openclaw" },
      { slug: "paperhunt" },
      { slug: "77days" },
      { slug: "3years" },
      { slug: "cowork", locked: true, lockNote: "连载中 · 2026.08 首发后开放" },
    ],
  },
];

/* ============================================================
 *  推导：篇号 / 页边码 / 出处
 * ============================================================ */

const deckMap = new Map<string, Deck>(allDecks.map((d) => [d.slug, d]));

export type BoundPiece = {
  slug: string;
  no: string; // "1.3"
  folio: number; // 起始页边码（全书连续）
  title: string;
  slides: number;
  source: string; // 出处体例：演讲 · 场合 · 日期 ／ 公众号 NO.xx ／ 课程 · 母版
  locked?: boolean;
  lockNote?: string;
};

export type BoundVolume = Volume & {
  bound: BoundPiece[];
  folio: number; // 本卷起始页
  pages: number; // 本卷页数
};

function sourceOf(d: Deck): string {
  if (d.category === "公众号") return `公众号 NO.${d.num}`;
  if (d.category === "对外演讲") return `演讲 · ${d.venue} · ${d.date}`;
  if (d.slug === "newcollege") return "课程 · 内部公开课";
  if (d.slug === "3years") return "母版 · 三年";
  if (d.slug === "cowork") return "演讲 · 2026.08 首发";
  return "演讲";
}

/** 全书装订：一次计算所有卷的篇号与连续页边码 */
export function bindBook(): BoundVolume[] {
  let folio = 1;
  return volumes.map((v) => {
    const start = folio;
    const bound = v.pieces.map((p, i) => {
      const d = deckMap.get(p.slug);
      if (!d) throw new Error(`book.ts: 未在 decks.ts 找到篇目 ${p.slug}`);
      const bp: BoundPiece = {
        slug: p.slug,
        no: `${v.no}.${i + 1}`,
        folio,
        title: d.title,
        slides: d.slides,
        source: sourceOf(d),
        locked: p.locked,
        lockNote: p.lockNote,
      };
      folio += d.slides;
      return bp;
    });
    return { ...v, bound, folio: start, pages: folio - start };
  });
}

export const boundVolumes = bindBook();
export const bookStats = {
  volumes: volumes.length,
  pieces: volumes.reduce((n, v) => n + v.pieces.length, 0),
  pages: boundVolumes.reduce((n, v) => n + v.pages, 0),
};

/** slug → 篇号（附录年表回链用），如 aws26 → { vol: 4, no: "4.7" } */
export const pieceIndex = new Map<string, { vol: number; volZh: string; no: string; locked?: boolean }>(
  boundVolumes.flatMap((v) => v.bound.map((p) => [p.slug, { vol: v.no, volZh: v.zh, no: p.no, locked: p.locked }]))
);

/** talks.ts num → deck slug（附录 A 年表回链） */
export const talkNumToSlug: Record<number, string> = {
  1: "rte24", 2: "pm24", 3: "convoai", 4: "audio25", 5: "engine25", 6: "era3",
  7: "prodready", 8: "pm25", 9: "vibecheck", 10: "vibesota", 11: "dual26",
  12: "robot26", 14: "inspire26", 15: "aws26",
};
