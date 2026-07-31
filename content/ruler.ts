import { allDecks } from "./decks";
import { pieceIndex } from "./book";

/** ============================================================
 *  活页 · 尺子（/ruler）数据层
 *  四条射线从「人」出发：外 Eval / 内 内观 / 时 时间 / 空 关系。
 *  规则：站 = 论证对象所在刻度；读数 = 该篇的签名数字。
 *  尽头都伸进非人的尺度，刻度永远是人读的。
 *  ============================================================ */

export type Pin = {
  slug?: string; // 关联 deck（钉图跳转 /slug）；缺省为特殊 pin
  title?: string; // 特殊 pin（如「本书」）自带标题
  href?: string;
  reading: string; // 签名数字读数
  locked?: boolean;
};

export type Station = {
  id: string;
  label: string; // 站名（刻度名）
  tick: string; // mono 刻度注（英文/数量级）
  pins: Pin[];
};

export type Ray = {
  id: "out" | "inw" | "time" | "space";
  zh: string;
  name: string; // Eval / 内观 / 时间 / 关系
  en: string;
  /** 尽头注：超出最后一格刻度的方向感 */
  beyond: string;
  stations: Station[];
};

export const rulerMeta = {
  title: "时空内外",
  subtitle: "四把尺子",
  sub: "活页 · 展开于《同一把尺子》",
  en: "TIME · SPACE · INWARD · OUTWARD",
  origin: "人",
  originNote: "原点站着人 · 你在这里",
  legend: "合上是同一把，展开是时空内外 · 站 = 论证对象的刻度 · 读数 = 签名数字",
};

/** 展开顺序（scroll 叙事与待机循环共用）：时 → 空 → 内 → 外 */
export const dimOrder: Ray["id"][] = ["time", "space", "inw", "out"];

export const rays: Ray[] = [
  {
    id: "out",
    zh: "外",
    name: "Eval",
    en: "OUTWARD",
    beyond: "下一把行业的尺子",
    stations: [
      {
        id: "turn",
        label: "一轮",
        tick: "TURN",
        pins: [
          { slug: "turns", reading: "四种死法 · 逐轮皆对整段却错" },
          { slug: "interrupted", reading: "真实噪声下的误报打断" },
        ],
      },
      {
        id: "session",
        label: "一段对话",
        tick: "SESSION",
        pins: [
          { slug: "demolies", reading: "6 家 STT 横评" },
          { slug: "voiceeval", reading: "重做外呼 Benchmark" },
        ],
      },
      {
        id: "after72",
        label: "会话之后",
        tick: "+72 H",
        pins: [{ slug: "outcome", reading: "72 小时后才结算" }],
      },
      {
        id: "benchmark",
        label: "一个基准",
        tick: "BENCHMARK",
        pins: [
          { slug: "evalprd", reading: "评测即 PRD" },
          { slug: "pm25", reading: "活人感 → 体验基准" },
          { slug: "vibecheck", reading: "Vibe Check · EN 首秀" },
          { slug: "pm24", reading: "听得到 → 听得心" },
        ],
      },
      {
        id: "standard",
        label: "行业标准",
        tick: "STANDARD",
        pins: [
          { slug: "vibesota", reading: "Vibe SOTA 2026" },
          { slug: "gcloud", reading: "五维金标准" },
          { slug: "prodready", reading: "Production-Ready 分界线" },
        ],
      },
    ],
  },
  {
    id: "time",
    zh: "时",
    name: "时间",
    en: "TIME",
    beyond: "下一个纪元",
    stations: [
      {
        id: "ms",
        label: "毫秒",
        tick: "10⁻¹ S",
        pins: [
          { slug: "arch", reading: "级联的胜负手 · 延迟" },
          { slug: "rte24", reading: "自然打断 · 2024 起点" },
        ],
      },
      {
        id: "days",
        label: "三天",
        tick: "10⁵ S",
        pins: [
          { slug: "3days", reading: "CLI → Platform · 3 天" },
          { slug: "systemcard", reading: "人间 3 天 · Claude 3 年" },
        ],
      },
      {
        id: "years",
        label: "两年",
        tick: "10⁷·⁸ S",
        pins: [{ title: "《同一把尺子》本书", href: "/preface", reading: "15 场 · 40 篇 · 1347 页" }],
      },
      {
        id: "decades",
        label: "二十年",
        tick: "10⁸·⁸ S",
        pins: [{ slug: "bottleneck", reading: "模型停更 · 产业忙二十年" }],
      },
      {
        id: "life",
        label: "一生",
        tick: "0.29 TB",
        pins: [{ slug: "029tb", reading: "3.2 年音频 · 生命上下文上限" }],
      },
      {
        id: "epoch",
        label: "纪元",
        tick: "EPOCHS",
        pins: [{ slug: "era3", reading: "QoS → QoE → QoI 第三纪元" }],
      },
    ],
  },
  {
    id: "space",
    zh: "空",
    name: "关系",
    en: "RELATIONS",
    beyond: "物种与文明",
    stations: [
      {
        id: "agent",
        label: "人 ↔ Agent",
        tick: "1 : 1",
        pins: [
          { slug: "tolan", reading: "4 个反直觉真相" },
          { slug: "robot26", reading: "从玩具到伙伴 · 21g 灵魂" },
          { slug: "newcollege", reading: "带一个 AI 新同事上班" },
          { slug: "engine25", reading: "Agent 交互核心引擎" },
          { slug: "audio25", reading: "音频 · AI Native 入口" },
        ],
      },
      {
        id: "human",
        label: "人 ↔ 人",
        tick: "PRESENCE",
        pins: [{ slug: "presence", reading: "买不到的产品 · 必须上门的人" }],
      },
      {
        id: "org",
        label: "人 ↔ 组织",
        tick: "1 : 10³",
        pins: [
          { slug: "csagent", reading: "第一个真金白银的场景" },
          { slug: "convoai", reading: "引擎从内部走向市场" },
          { slug: "elys", reading: "推荐退位 · 分身上桌" },
        ],
      },
      {
        id: "orgs",
        label: "组织 ↔ 组织",
        tick: "10³ : 10³",
        pins: [
          { slug: "awsfde", reading: "10 亿美元 · 送进现场" },
          { slug: "34days", reading: "34 天 · 36 亿美元" },
          { slug: "dual26", reading: "双引擎 · 全域增长" },
        ],
      },
      {
        id: "civ",
        label: "社会 ↔ 全人类",
        tick: "10⁹",
        pins: [
          { slug: "staas", reading: "地位即服务" },
          { slug: "aws26", reading: "两个物种 · 同一颗引擎" },
        ],
      },
    ],
  },
  {
    id: "inw",
    zh: "内",
    name: "内观",
    en: "INWARD",
    beyond: "21g 灵魂",
    stations: [
      {
        id: "retro",
        label: "一次复盘",
        tick: "A RETRO",
        pins: [
          { slug: "4mtokens", reading: "17 小时 · 150 轮 · 4M tokens" },
          { slug: "openclaw", reading: "随出去的份子钱" },
        ],
      },
      {
        id: "project",
        label: "一个项目",
        tick: "A PROJECT",
        pins: [
          { slug: "77days", reading: "77 天 · 种子与森林" },
          { slug: "paperhunt", reading: "重新定义论文阅读" },
        ],
      },
      {
        id: "leap",
        label: "一次跃迁",
        tick: "A LEAP",
        pins: [{ slug: "highagency", reading: "执行变便宜 · 人变贵" }],
      },
      {
        id: "threeyears",
        label: "三年",
        tick: "4 LEAPS",
        pins: [{ slug: "3years", reading: "四次跃迁 · 三年母版" }],
      },
      {
        id: "trustlife",
        label: "信任",
        tick: "A LIFE",
        pins: [{ slug: "trust", reading: "信任进化 · 2026.08 首发", locked: true }],
      },
    ],
  },
];

/* ---------- 解析：pin 补全标题/链接/归卷 ---------- */

const deckMap = new Map(allDecks.map((d) => [d.slug, d]));

export type BoundPin = Pin & {
  title: string;
  href?: string;
  vol?: string; // 归卷篇号，如 1.6
  kind: "talk" | "essay" | "course" | "book";
};

export function bindPin(p: Pin): BoundPin {
  if (!p.slug) return { ...p, title: p.title ?? "", kind: "book" };
  const d = deckMap.get(p.slug);
  const piece = pieceIndex.get(p.slug);
  const kind = d?.category === "公众号" ? "essay" : d?.category === "对外演讲" ? "talk" : "course";
  return {
    ...p,
    title: d?.title ?? p.slug,
    href: p.locked ? undefined : `/${p.slug}`,
    vol: piece?.no,
    kind,
  };
}

export const rulerStats = {
  rays: rays.length,
  stations: rays.reduce((n, r) => n + r.stations.length, 0),
  pins: rays.reduce((n, r) => n + r.stations.reduce((m, s) => m + s.pins.length, 0), 0),
};
