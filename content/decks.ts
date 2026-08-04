export type Deck = {
  slug: string;
  title: string;
  slides: number;
  category: "演讲" | "公众号" | "对外演讲";
  num?: string; // 公众号编号 / 演讲编号
  date?: string; // 对外演讲：日期
  venue?: string; // 对外演讲：场合
  dual?: boolean; // true = 单文件双主题（左下角切换）；false = 双文件（-light 路由）
  locked?: boolean; // 首发前锁定：索引页列出但不挂链
};

/** 隐藏 deck 库：不进导航、不进 sitemap、全部 noindex。索引页 /decks 仅自己可知。 */
export const speechDecks: Deck[] = [
  { slug: "cowork", title: "从「被托付」到「双向奔赴 · 共事」· 信任进化 V10", slides: 62, category: "演讲", dual: true },
  { slug: "cowork-conf", title: "从「被托付」到「双向奔赴 · 共事」· 2026 AI 产品大会视觉版", slides: 55, category: "演讲", dual: false, locked: true },
  { slug: "newcollege", title: "带一个新同事上班 · Agent 恒动复利", slides: 92, category: "演讲", dual: false },
  { slug: "3years", title: "当智能体开始行动，人和组织怎样跟上 · 三年母版", slides: 48, category: "演讲", dual: true },
];

/** 对外演讲全集 · 2024–2026 · 14 场（13 为圆桌主持无 deck）。 */
export const talkDecks: Deck[] = [
  { slug: "aiot26", num: "16", date: "2026.08", venue: "2026 AI 产品大会 · 声网 AIoT 专场", title: "当 AI 有了身体：从玩具到伙伴的多模态产品化破局", slides: 40, category: "对外演讲", dual: true, locked: true },
  { slug: "aws26", num: "15", date: "2026.06", venue: "AWS 中国峰会", title: "被记住 · 被托付：对话式智能体的物种分化与同源进化", slides: 38, category: "对外演讲", dual: true },
  { slug: "inspire26", num: "14", date: "2026.06", venue: "INSPIRE 2026", title: "从对话式 AI 到企业级智能体", slides: 24, category: "对外演讲", dual: true },
  { slug: "robot26", num: "12", date: "2026.05", venue: "RTE 春夏巡游 · 深圳", title: "从玩具到伙伴：消费级机器人的「活人感」交互设计", slides: 42, category: "对外演讲", dual: true },
  { slug: "dual26", num: "11", date: "2026.04", venue: "中国网络视听大会", title: "RTE + AI 双引擎驱动视听全域商业增长", slides: 20, category: "对外演讲", dual: true },
  { slug: "vibesota", num: "10", date: "2026.01", venue: "Voice Agent 闭门会", title: "Voice Agent 2026 · Vibe SOTA", slides: 28, category: "对外演讲", dual: true },
  { slug: "vibecheck", num: "09", date: "2026.01", venue: "First Prompt · Singapore", title: "No More Prompts — How Conversation Agents Pass the Vibe Check", slides: 21, category: "对外演讲", dual: true },
  { slug: "pm25", num: "08", date: "2025.12", venue: "人人都是产品经理大会 2025", title: "从「活人感」缺失到体验基准打造", slides: 41, category: "对外演讲", dual: true },
  { slug: "prodready", num: "07", date: "2025.10", venue: "ConvoAI & RTE 2025", title: "Production-Ready 对话式 AI 产品全栈发布", slides: 22, category: "对外演讲", dual: true },
  { slug: "era3", num: "06", date: "2025.10", venue: "ConvoAI & RTE 2025", title: "Agent 交互核心引擎，重塑实时体验的第三纪元", slides: 39, category: "对外演讲", dual: true },
  { slug: "engine25", num: "05", date: "2025.08", venue: "全球产品经理大会", title: "Agent 交互核心引擎，重构人机协同体验革命", slides: 39, category: "对外演讲", dual: true },
  { slug: "audio25", num: "04", date: "2025.03", venue: "中国网络视听大会", title: "对话式 AI 驱动 AI 音频体验革新", slides: 24, category: "对外演讲", dual: true },
  { slug: "convoai", num: "03", date: "2025.03", venue: "ConvoAI 产品发布会", title: "ConvoAI 对话式 AI 引擎 · 正式发布", slides: 27, category: "对外演讲", dual: true },
  { slug: "pm24", num: "02", date: "2024.12", venue: "人人都是产品经理大会 2024", title: "生成式 AI 驱动实时互动的技术变革与体验革新", slides: 32, category: "对外演讲", dual: true },
  { slug: "rte24", num: "01", date: "2024.10", venue: "RTE 2024 · 首次外部主旨", title: "生成式 AI 驱动实时互动的技术变革与体验革新", slides: 31, category: "对外演讲", dual: true },
];

export const essayDecks: Deck[] = [
  { slug: "tolan", num: "01", title: "我从 Tolan 身上，看清了 Voice Agent 的 4 个反直觉真相", slides: 22, category: "公众号", dual: true },
  { slug: "paperhunt", num: "02", title: "PaperHunt：我是如何用一个 Side Project 重新定义「论文阅读」的", slides: 22, category: "公众号", dual: true },
  { slug: "029tb", num: "03", title: "我们的一生只有 0.29TB：从第一性原理看 AI 录音的价值上限", slides: 28, category: "公众号", dual: true },
  { slug: "voiceeval", num: "04", title: "VoiceAgentEval：为什么我们必须重做 AI 外呼的 Benchmark", slides: 24, category: "公众号", dual: true },
  { slug: "openclaw", num: "05", title: "为了赶时髦的「中登」，给 OpenClaw 随了多少份子钱", slides: 23, category: "公众号", dual: true },
  { slug: "elys", num: "06", title: "Elys 给字节和小红书的一把剑：推荐算法退位，分身上桌", slides: 24, category: "公众号", dual: true },
  { slug: "staas", num: "07", title: "旧文新读：地位即服务", slides: 26, category: "公众号", dual: true },
  { slug: "4mtokens", num: "08", title: "17 小时，150 轮对话，4M Tokens：一个产品经理用 Claude Code 造了什么", slides: 36, category: "公众号", dual: true },
  { slug: "3days", num: "09", title: "一个产品的三天，从 CLI 长成 Developer Platform", slides: 39, category: "公众号", dual: true },
  { slug: "systemcard", num: "10", title: "Claude 3 天人间 3 年，Anthropic 243 页 System Card 读后感", slides: 34, category: "公众号", dual: true },
  { slug: "77days", num: "11", title: "种子与森林：一个 Side Project 的 77 天", slides: 30, category: "公众号", dual: true },
  { slug: "csagent", num: "12", title: "客服 Agent 的胜负手，不在模型——从 Bret Taylor 和 Sierra 身上验证的 6 件事", slides: 39, category: "公众号", dual: true },
  { slug: "arch", num: "13", title: "胜负手不在模型，在架构——最懂端到端的 ElevenLabs，为什么押注「级联」", slides: 34, category: "公众号", dual: true },
  { slug: "demolies", num: "17", title: "你的 demo 在骗你——一场 6 家 STT 的横评", slides: 35, category: "公众号", dual: true },
  { slug: "turns", num: "18", title: "每一轮都对，整段却错了——客服 Agent 的四种死法", slides: 34, category: "公众号", dual: true },
  { slug: "evalprd", num: "19", title: "评测即 PRD——AI 时代，产品经理的交付物变了", slides: 39, category: "公众号", dual: true },
  { slug: "interrupted", num: "20", title: "它不停以为自己被打断——现成语音方案扛不住真实噪声", slides: 36, category: "公众号", dual: true },
  { slug: "presence", num: "20.5", title: "OpenAI 发了一个买不到的产品——Presence 最稀缺的是必须上门的人", slides: 40, category: "公众号", dual: true },
  { slug: "bottleneck", num: "21", title: "OpenAI COO 说：即使模型今天停更，也够产业忙二十年", slides: 25, category: "公众号", dual: true },
  { slug: "outcome", num: "23", title: "一通客服结束 72 小时后，AI 才决定这笔钱能不能收", slides: 34, category: "公众号", dual: true },
  { slug: "highagency", num: "27", title: "AI 让执行变便宜，high agency 让人变贵", slides: 51, category: "公众号", dual: true },
  { slug: "awsfde", num: "28", title: "AWS 砸 10 亿美元把工程师送进客户现场——但他们什么时候离开", slides: 30, category: "公众号", dual: true },
  { slug: "34days", num: "32", title: "改名 34 天后，它以 36 亿美元卖给 Salesforce", slides: 30, category: "公众号", dual: true },
  { slug: "warp-public-good", num: "39", title: "OpenAI 把「更快」写进 IETF 草案，声网的护城河要换地方了", slides: 30, category: "公众号", dual: true, locked: true },
  { slug: "turn-ledger", num: "40", title: "你按「一通电话解决了没有」收费，可「一轮」是猜出来的", slides: 30, category: "公众号", dual: true, locked: true },
  { slug: "async-two-model", num: "41", title: "他们取消了 turn detector，然后用了两个模型", slides: 32, category: "公众号", dual: true, locked: true },
];

export const allDecks = [...speechDecks, ...talkDecks, ...essayDecks];

/** 供 next.config 生成 rewrites/headers 的路由清单 */
export const deckRoutes: { source: string; file: string }[] = [
  ...allDecks.map((d) => ({ source: `/${d.slug}`, file: `/decks/${d.slug}.html` })),
  { source: "/newcollege-light", file: "/decks/newcollege-light.html" },
  // aiot26 叙事重构版（26 页 · 默认浅底）· 预览路由，Colin 定稿前不进 talkDecks 索引
  { source: "/aiot26-v2", file: "/decks/aiot26-v2.html" },
  // aiot26 正讲版（35 页 · 大会 conf 视觉 · 8.9 正讲版）= V3 内容层 + 大会黑紫金视觉层（单主题）
  { source: "/aiot26-conf", file: "/decks/aiot26-conf.html" },
];
