export type Deck = {
  slug: string;
  title: string;
  slides: number;
  category: "演讲" | "公众号";
  num?: string; // 公众号编号
  dual?: boolean; // true = 单文件双主题（左下角切换）；false = 双文件（-light 路由）
};

/** 隐藏 deck 库：不进导航、不进 sitemap、全部 noindex。索引页 /decks 仅自己可知。 */
export const speechDecks: Deck[] = [
  { slug: "newcollege", title: "带一个新同事上班 · Agent 恒动复利", slides: 92, category: "演讲", dual: false },
  { slug: "3years", title: "当智能体开始行动，人和组织怎样跟上 · 三年母版", slides: 48, category: "演讲", dual: true },
  { slug: "trust", title: "对话式智能体的信任进化 · V9.1", slides: 50, category: "演讲", dual: false },
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
];

export const allDecks = [...speechDecks, ...essayDecks];

/** 供 next.config 生成 rewrites/headers 的路由清单 */
export const deckRoutes: { source: string; file: string }[] = [
  ...allDecks.map((d) => ({ source: `/${d.slug}`, file: `/decks/${d.slug}.html` })),
  { source: "/newcollege-light", file: "/decks/newcollege-light.html" },
  { source: "/trust-light", file: "/decks/trust-light.html" },
];
