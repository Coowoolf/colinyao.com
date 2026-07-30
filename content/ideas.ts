export type Idea = {
  id: string;
  index: string; // IDEA 01
  zh: string;
  en: string;
  def: string;
  refs: { label: string; num?: number }[];
  accent?: "coral" | "magenta";
  motif: "ruler" | "wave" | "hemis" | "bounds" | "sota" | "qoi" | "steps" | "tb";
  since: string;
};

export const ideas: Idea[] = [
  {
    id: "ruler",
    index: "IDEA 01",
    zh: "同一把尺子",
    en: "One Ruler, Two Directions",
    def: "向外，是 Eval——看见系统哪里偏了，把争论变成实验；向内，是内观——看见自己的判断哪里偏了，允许自己改错。真正的专业，不是永远判断正确，而是有一套更早发现错误、更快修正错误的机制。",
    refs: [{ label: "2026.08 信任进化（首发于本站）" }],
    accent: "coral",
    motif: "ruler",
    since: "2026",
  },
  {
    id: "aliveness",
    index: "IDEA 02",
    zh: "活人感",
    en: "The Feeling of Aliveness",
    def: "对话式智能体的第一体验门槛，不在参数和榜单里——在「像不像一个活人在跟你说话」：响应的节奏、打断的从容、情绪的呼应、记得你是谁。缺了它，再聪明也是玩具。",
    refs: [
      { label: "人人都是PM 2025", num: 8 },
      { label: "First Prompt SG", num: 9 },
      { label: "RTE 春夏巡游", num: 12 },
    ],
    motif: "wave",
    since: "2025",
  },
  {
    id: "hemispheres",
    index: "IDEA 03",
    zh: "被记住 · 被托付",
    en: "Remembered · Entrusted",
    def: "对话式智能体分化成两个物种：消费级让 AI 像人，终局是被记住；企业级让 AI 像系统，终局是被托付。物种分化，同源进化——底层是同一段 DNA、同一颗引擎。",
    refs: [
      { label: "AWS 中国峰会", num: 15 },
      { label: "Google Cloud", num: 14 },
      { label: "RTE 春夏巡游", num: 12 },
    ],
    motif: "hemis",
    since: "2026",
  },
  {
    id: "bounds",
    index: "IDEA 04",
    zh: "模型上限 · 引擎下限",
    en: "Ceiling & Floor",
    def: "模型决定能力上限，引擎决定体验下限。所有人都在卷上限，但用户流失发生在下限——一次没接住的打断、一秒尴尬的沉默，比答错一道题伤得更重。",
    refs: [
      { label: "AWS 中国峰会", num: 15 },
      { label: "第三纪元", num: 6 },
    ],
    accent: "magenta",
    motif: "bounds",
    since: "2025",
  },
  {
    id: "vibe-sota",
    index: "IDEA 05",
    zh: "Vibe SOTA",
    en: "State of the Art, by Vibe",
    def: "语音智能体的 SOTA 不在 benchmark 榜单上，在 vibe 里。把「感觉对了」从一句玄学，变成可测量、可优化、可比较的体验基准——这是产品经理的手艺。",
    refs: [
      { label: "Voice Agent 闭门会", num: 10 },
      { label: "First Prompt SG", num: 9 },
    ],
    motif: "sota",
    since: "2026",
  },
  {
    id: "qoi",
    index: "IDEA 06",
    zh: "QoI · 第三纪元",
    en: "Quality of Interaction",
    def: "QoS 为传输设计，QoE 为人设计，QoI 为人模共演设计。实时体验的测量对象完成第三次迁移——从网络质量，到人的感受，到人与模型之间互动本身的质量。",
    refs: [
      { label: "RTE 春夏巡游", num: 12 },
      { label: "第三纪元", num: 6 },
      { label: "RTE 2024", num: 1 },
    ],
    motif: "qoi",
    since: "2024–2026",
  },
  {
    id: "four-steps",
    index: "IDEA 07",
    zh: "听得到 → 听得清 → 听得懂 → 听得心",
    en: "Four Stages of Listening",
    def: "对话体验的四阶段进化：从信号可达，到声音干净，到语义理解，到听出情绪与言外之意。每往上一阶，技术栈换一层，体验标准也换一把尺。",
    refs: [
      { label: "RTE 2024", num: 1 },
      { label: "人人都是PM 2024", num: 2 },
      { label: "第三纪元", num: 6 },
    ],
    motif: "steps",
    since: "2024",
  },
  {
    id: "tb",
    index: "IDEA 08",
    zh: "0.29 TB",
    en: "The Physics of Companionship",
    def: "一生说 10 亿个词，25% 值得记住，折合 3.2 年音频——0.29 TB，是一个人「生命上下文」的物理上限，也是机器人成为伙伴的记忆配额。21g 灵魂 × 0.29TB 记忆。",
    refs: [
      { label: "RTE 春夏巡游", num: 12 },
      { label: "AWS 中国峰会", num: 15 },
    ],
    motif: "tb",
    since: "2026",
  },
];
