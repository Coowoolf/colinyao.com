export type Talk = {
  num: number;
  date: string; // 展示用
  year: number;
  venue: string;
  title: string;
  summary: string;
  slides?: number;
  star?: 1 | 2; // 1 = 代表作，2 = 里程碑
  role?: string; // 默认主讲
  lang?: "EN";
  tags?: string[];
};

export const upcoming = {
  date: "2026.08",
  venue: "人人都是产品经理 · AI 产品经理大会",
  title: "对话式智能体的信任进化",
  summary:
    "信任的尺子 × 四次 PM 跃迁。「同一把尺子，向外叫 Eval，向内叫内观」将在这场演讲首次上台——它已经先在这里落了户。",
};

export const talks: Talk[] = [
  {
    num: 15,
    date: "2026.06.23",
    year: 2026,
    venue: "AWS 中国峰会 · 上海世博中心",
    title: "被记住 · 被托付：对话式智能体的物种分化与同源进化",
    summary:
      "「消费级 × 企业级」两个半球第一次合体公开讲：对话式智能体分化为两个物种——像人的被记住，像系统的被托付——却共享同一段 DNA、同一颗引擎。与 AWS 解决方案架构师联合，把世界观缝进云上 Production-Ready 的工程兑现。",
    slides: 40,
    star: 2,
    tags: ["被记住·被托付", "同源进化", "模型上限·引擎下限"],
  },
  {
    num: 14,
    date: "2026.06.06",
    year: 2026,
    venue: "Google Cloud 开发者大会",
    title: "从对话式 AI 到企业级智能体",
    summary:
      "企业级半球的母本：客服是第一个被企业真金白银付费的智能体场景。用真实生产数据立论——96.5% 的用户没有分辨出 AI，营销转化 2× 超越人类销冠；再以「五维金标准」定义什么才算企业级。",
    slides: 19,
    star: 1,
    tags: ["被托付", "96.5%", "五维金标准"],
  },
  {
    num: 13,
    date: "2026.05.17",
    year: 2026,
    venue: "RTE Dev Talk · 直播圆桌",
    title: "Thinking Machines 押注的「交互模型」是什么",
    summary: "圆桌主持：从 Thinking Machines 的押注出发，聊交互模型与实时体验的下一步。",
    role: "主持",
    tags: ["交互模型"],
  },
  {
    num: 12,
    date: "2026.05.16",
    year: 2026,
    venue: "声网 RTE 2026 春夏巡游 · 深圳站 IoT",
    title: "从玩具到伙伴：消费级机器人的「活人感」交互设计",
    summary:
      "消费级半球的母本：玩具与伙伴的分水岭不是智能，是角色。提出「角色三件套（身份/关系/历史）+ 一个实时引擎」工程框架与 QoI 范式，以「21g 灵魂 × 0.29TB 记忆」双峰收尾——从被使用，到被记住。",
    slides: 36,
    star: 1,
    tags: ["活人感", "角色三件套", "0.29 TB", "QoI"],
  },
  {
    num: 11,
    date: "2026.04.15",
    year: 2026,
    venue: "第十三届中国网络视听大会",
    title: "RTE + AI 双引擎驱动视听全域商业增长",
    summary:
      "从体验话题转向商业话题：行业从「试水 AI」走向「靠 AI 赚钱」，双引擎叙事对应这一阶段的增长命题。",
    slides: 16,
    tags: ["商业化"],
  },
  {
    num: 10,
    date: "2026.01.25 / 03.07",
    year: 2026,
    venue: "Voice Agent 闭门会 · 北京 & Voice Agent Camp",
    title: "Voice Agent 2026 · Vibe SOTA",
    summary:
      "面向小圈层的内核版本：把 Vibe Check 升级为 Vibe SOTA——2026 年语音智能体的体验天花板长什么样，怎么达到。",
    slides: 22,
    tags: ["Vibe SOTA"],
  },
  {
    num: 9,
    date: "2026 H1",
    year: 2026,
    venue: "First Prompt · Singapore",
    title: "No More Prompts — How Conversation Agents Pass the Vibe Check",
    summary:
      "首次国际英文舞台：把「活人感」翻译成国际语境的 Vibe Check——对话智能体是否通过氛围检验，才是真实可用的衡量标准。",
    slides: 8,
    lang: "EN",
    tags: ["Vibe Check", "国际"],
  },
  {
    num: 8,
    date: "2025.12.23",
    year: 2025,
    venue: "人人都是产品经理大会 2025",
    title: "从「活人感」缺失到体验基准打造——对话式智能体的进化之路",
    summary:
      "个人辨识度最高的一场：AI 对话产品的根本缺陷不是技术指标，而是「不像活人在跟你聊」的整体感受。首次完整提出「活人感」，并给出把它量化为体验基准的方法。",
    slides: 47,
    star: 1,
    tags: ["活人感", "体验基准"],
  },
  {
    num: 7,
    date: "2025.10.31",
    year: 2025,
    venue: "ConvoAI & RTE 2025",
    title: "Production-Ready 对话式 AI 产品全栈发布",
    summary:
      "ConvoAI 一周年全栈发布：与 Demo-Ready 划清界限——真实生产环境跑通、可商用、可规模化。",
    slides: 18,
    tags: ["Production-Ready"],
  },
  {
    num: 6,
    date: "2025.10.31",
    year: 2025,
    venue: "ConvoAI & RTE 2025",
    title: "对话式 AI：Agent 交互核心引擎，重塑实时体验的第三纪元",
    summary:
      "「Agent 交互核心引擎」× 三阶段论的合体升级，提出「第三纪元」——QoS、QoE 之后，为人和模型共同设计的时代。至今最完整、最被复用的对外主旨叙事。",
    slides: 43,
    star: 1,
    tags: ["第三纪元", "核心引擎"],
  },
  {
    num: 5,
    date: "2025.08.15",
    year: 2025,
    venue: "全球产品经理大会",
    title: "对话式 AI：Agent 交互核心引擎，重构人机协同体验革命",
    summary:
      "首次提出「对话式 AI = Agent 交互核心引擎」：把对话式 AI 从细分产品上拔到 Agent 时代基础设施的位置，给 PM 一个清晰的产品坐标系。",
    slides: 43,
    tags: ["核心引擎"],
  },
  {
    num: 4,
    date: "2025.03.28",
    year: 2025,
    venue: "第十二届中国网络视听大会",
    title: "对话式 AI 驱动 AI 音频体验革新",
    summary:
      "面向网络视听行业的特化版：音频从被动的传输介质，升级为 AI Native 时代体验产品的核心入口。",
    slides: 25,
    tags: ["音频"],
  },
  {
    num: 3,
    date: "2025.03.06",
    year: 2025,
    venue: "ConvoAI 产品发布会",
    title: "ConvoAI 对话式 AI 引擎 · 正式发布",
    summary:
      "从产品定义、能力矩阵、客户案例到定价的完整官宣——ConvoAI 从内部产品走向市场产品的节点。",
    slides: 31,
    tags: ["发布"],
  },
  {
    num: 2,
    date: "2024.12.07",
    year: 2024,
    venue: "人人都是产品经理大会 2024",
    title: "生成式 AI 驱动实时互动的技术变革与体验革新",
    summary:
      "RTE 大会版本面向 PM 受众的转译：更多产品方法论、更少技术细节，沿用三段论与「听得到 → 听得心」四阶段框架。",
    slides: 37,
    tags: ["四阶段"],
  },
  {
    num: 1,
    date: "2024.10.25",
    year: 2024,
    venue: "RTE 2024 · 首次外部独立主旨",
    title: "生成式 AI 驱动实时互动的技术变革与体验革新",
    summary:
      "一切的起点：首次系统提出 QoS → QoE → AI QoE 三阶段框架，发布「自然打断、自如对话」与 HIP 人声意图预测——此后所有对外叙事的根基版本。",
    slides: 33,
    star: 1,
    tags: ["三阶段", "起点"],
  },
];

export const talkYears = [2026, 2025, 2024];
