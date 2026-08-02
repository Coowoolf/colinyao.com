// 按物 · WORKS —— 作品集数据层。
// 策展原则：每件作品用四阶语法量一遍（被使用 → 被记住 → 被托付 → 双向奔赴），
// 尺子先量自己；公司作品只走公开口径（官网 / 发布会 / 大会 deck 已讲的）。
export type Work = {
  id: string;
  name: string;
  en: string;
  kind: "个人出品" | "声网 · 产品线" | "声网 · 工具与评测";
  tagline: string;
  role: string;
  stage: 1 | 2 | 3 | 4; // 走到四阶的第几格
  stageNote: string;
  milestones: string[];
  links: { label: string; href: string }[];
  featured?: boolean;
};

export const stageNames = ["被使用", "被记住", "被托付", "双向奔赴"];

export const works: Work[] = [
  {
    id: "comma",
    name: "Comma",
    en: "VOICE AS A KEYBOARD",
    kind: "个人出品",
    tagline: "按住说话，松手上屏——macOS 语音输入工具，在任何应用里用声音代替键盘。",
    role: "独立出品 · 0 → 1（产品定义 · macOS 客户端 · 自造硬件）",
    stage: 2,
    stageNote: "内测用户日常高频在用——回来，比夸它更真",
    milestones: [
      "macOS 菜单栏应用：fn 一按即说，AI 润色、去口头语、实时中英互译",
      "Comma Mic 自造硬件：ESP32-S3 · BLE · Opus 流式——讲拾音的人自己造了一只麦克风",
      "Comma CLI：把「语音即输入」延伸进终端与 Agent 工作流",
    ],
    links: [],
    featured: true,
  },
  {
    id: "convoai-engine",
    name: "ConvoAI Engine",
    en: "CONVERSATIONAL AI ENGINE",
    kind: "声网 · 产品线",
    tagline: "让 Agent 像人一样接得住对话的实时引擎——两行代码接入，15 分钟上线。",
    role: "产品负责人 · 1.0 → 2.x · 16 次迭代",
    stage: 3,
    stageNote: "岗位级交付：同一套引擎在营销外呼、售后客服等真实岗位承担业务结果",
    milestones: [
      "2024.10 国内首个 Realtime API（声网 × MiniMax），五个节点 19 个月",
      "1.0 能对话（2025.03）→ 2.0 电话接入（2025.10）→ 2.x 会用工具 · 打断解耦 · 四态轮次判定",
      "选择性注意力锁定 / 优雅打断 2.0 / 全链路轮次追踪——把「听清、接住、不失控」做成引擎能力",
    ],
    links: [
      { label: "官网", href: "https://www.shengwang.cn/blog/blogdetail/conversational-ai/" },
    ],
    featured: true,
  },
  {
    id: "call-agent",
    name: "Call Agent",
    en: "AGENT ON THE PHONE LINE",
    kind: "声网 · 产品线",
    tagline: "把 Agent 放上电话线的岗位化产品——按岗位交付，不按功能交付。",
    role: "产品负责人 · 岗位化交付模式的定义者",
    stage: 3,
    stageNote: "外呼销售岗已有自己的业绩单——第一批走向「双向奔赴」的岗位",
    milestones: [
      "外呼销售岗：入职 30 天反超人工平均约 2 倍（3.08% 转化率）",
      "96.5% 未被识别为 AI —— 2,475 通全量人工标注的真实外呼",
      "岗位工牌机制：红线 · 审批权限 · 升级路径，把「托付」写成制度",
    ],
    links: [],
  },
  {
    id: "stt",
    name: "STT 实时转写",
    en: "REALTIME SPEECH-TO-TEXT",
    kind: "声网 · 产品线",
    tagline: "从「引擎的一个模块」长成一条独立产品线——为轮次判定提供毫秒级素材的那一层。",
    role: "产品负责人 · 模块 → 产品线的升格操盘",
    stage: 1,
    stageNote: "最不性感的一层，今年增长最快——被使用，是它唯一要赢的尺子",
    milestones: [
      "Realtime 2.0：流式 · 低延迟 · 热词 · 多语种",
      "独立入口：从模块变成一条可以自己被搜索到的产品线",
      "自研 ASR 模型：这一层的单位成本，决定整条链的报价空间",
    ],
    links: [],
  },
  {
    id: "agent-studio",
    name: "Agent Studio · 模型评测平台",
    en: "BUILD & EVAL TOOLING",
    kind: "声网 · 工具与评测",
    tagline: "从「一小时搭出来」到「能上线」——编排、模拟考核与评测的那一层。",
    role: "产品负责人 · 评测即 PRD 的产品化落点",
    stage: 1,
    stageNote: "上线前那一段（模拟考核 · 合规通过率 · 失败归因）正在变成默认动作",
    milestones: [
      "零代码编排 · 场景化模板 · 插件化集成（电话 / 模型 / 数字人）",
      "上线前新增一段：模拟考核、合规通过率、权限分层、失败案例归因",
      "模型评测平台：仪表盘 · 竞技场 · 工作流——让选型有依据，让报价有底气",
    ],
    links: [],
  },
];
