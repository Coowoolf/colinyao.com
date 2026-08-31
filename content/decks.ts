export type Deck = {
  slug: string;
  title: string;
  slides: number;
  category: "演讲" | "公众号" | "对外演讲" | "情报";
  num?: string; // 公众号编号 / 演讲编号
  date?: string; // 对外演讲：日期
  venue?: string; // 对外演讲：场合
  dual?: boolean; // true = 单文件双主题（左下角切换）；false = 双文件（-light 路由）
  locked?: boolean; // 首发前锁定：索引页列出但不挂链
};

/** 隐藏 deck 库：不进导航、不进 sitemap、全部 noindex。索引页 /decks 仅自己可知。 */
export const speechDecks: Deck[] = [
  // convoai = 初次拜访客户工作 deck（非讲次档案）：公司信任状 + 对话式 AI 矩阵 + 三条产品线。
  // CONF 家族 · conf-light 默认 · 单文件双主题 · 背景板节奏（title/chapter×3/quote/content）
  // + GPT 5.6 hero-art 章视觉层（5 组双主题透明 PNG，contain 不裁切）。
  // 口径纪律：只用公开可查证数字（BPO 喂稿锁定文案 + 官网/发版说明），Phone Agent 用「Global 率先发布」。
  // 2026-08-13 Colin：/convoai 换装引擎产品介绍；31p 拜访版迁出独立路由保持可达（已于 2026-08-21 退役，见下）。
  // 2026-08-20：13 → 16 页（补三张机理页）→ 17 页（VAD 之后插入产品架构大图）。
  // 2026-08-21：17 → 20 页 —— P10 SAL 重做（三种噪声 · 三层方案）/ P11 弱网补 AI QoS 断网续播 /
  //   P12 多模态聚焦视觉模态；新增 P13 Physical AI · R1 开发套件、P14 Physical AI 案例墙、
  //   P19 OpenAI 合作（title 板 quote）；原 P13 编排 → P15 并做「箭头语义修」。
  // 2026-08-21 收束轮 20 → 18：删 P14 案例墙（案例是 convoai-info 的活儿）、删原 P20 收尾页
  //   （末页金句与封面同义，重复收尾等于没收尾），其唯一不可替代的 CTA 行继承到新末页页脚；
  //   P13 R1 改带实拍图（跨引用 robot26 资产）、P18 OpenAI 合作升为末页并加双源 logo 锁定版；
  //   deckSwap 主题键从「hover 才呼出」改为常显 chip（对外发链接的 deck 不能藏切换键）。
  // 2026-08-21（Call Agent 章）18 → 21 页，两件事：
  //   ① 新增 Call Agent 三页：P16 登场 · 成绩单（96.5% / 1,000+ / 1/3 + 真人 vs 智能体三行）、
  //      P17 五个大脑 · Agent Harness（架构页 · 走 P8 大图语言 · 五带并行汇聚 hot 盒）、
  //      P18 Loop Engineering · 成长飞轮（DAY 1→30 曲线穿越平线 + 复盘/定位/迭代/训练小环）。
  //      文案是 Call Agent 官网定稿逐字使用；红线：不出价格、不出 staging URL、不出智能体人名，
  //      96.5% 必须带「盲测 32,000 名真实客户」口径（与 convoai-info P5 的 2,475 通生产口径是
  //      两个不同数据集，不许混写）——build() 里已有构建期红线断言。
  //   ② 页序按 Colin 指令重排：**场景之后接 Call Agent，Call Agent 之后接 R1**。
  //      位移（正文逐字节未动，只换位置）：原 14 编排→13 / 原 15 接入→14 / 原 16 场景→15 /
  //      原 13 R1→19 / 原 17 Why Agora→20 / 原 18 OpenAI→21。
  //      连带：分步页 [6,7,15] → [6,7,14]、口径锁页 17 → 20、title 板 {1,18} → {1,21}。
  // 2026-08-21（视频页）21 → 22：Colin 指令「R1 之后再插一页 robot26 #24 同款全屏视频页」——
  //   新 P20 = 无人机秀 demo 纯全屏片子（跨引用 robot26 的 demo.mp4 + demo-poster.jpg，不复制文件），
  //   Why Agora → P21、OpenAI 末页 → P22。机制整套复刻 robot26 #24：不带 controls 属性
  //   （Blink 控制条在 .deck-stage 的 transform:scale 下错位，Colin 截图实锤）、悬停才呼出、
  //   preload=none、muted+playsinline、data-play-step 步进开播；播放挂钩写在 builder 的内联脚本里，
  //   **不改共享 deck.js**（那份 runtime 是 convoai / info / visit 三份 deck 共用的）。
  //   归档口径：bake-archive 把 demo.mp4 换成 https://colinyao.com/... 绝对地址（3.1MB 不进 base64），
  //   poster 照常内联 —— 在线可播、离线退回整幅静帧。
  // 重建：python3 scripts/build-convoai-engine.py（双生同写 /decks/convoai-engine.html 别名，抽屉 iframe 指它）
  // 自检：node scripts/qa-convoai-engine.mjs（THEME=dark 二跑，含双生一致闸 + P21 口径锁 + P10 大图闸
  //   + P19 实拍图闸 + P22 双源 logo 显隐闸 + deckSwap 常显闸 + 已删两页的内容回流闸
  //   + Call Agent 三页内容闸与价格 / staging 反向闸 + P20 视频页闸）
  // 2026-08-23 Colin：封面换「对话即交互」（kicker 改 DEEP DIVE · 深入讲解），定位从产品介绍
  //   升为**深入讲解版**；同轮 P3 双工三模式入运动件名册（三种双工的运动模式就是它们的定义），
  //   并把三数章重排为 P5 三件极致 → P6 拆 650 → P7 拆 340 前提 → P8 拆 340 → P9 拆 95% →
  //   P10 大图收束（只在 6–10 区间轮转，页数与 P11 起的页序全部不变）。
  { slug: "convoai", title: "声网 · 对话式 AI 引擎 · 深入讲解", slides: 22, category: "演讲", dual: true },
  // 2026-08-21 Colin：拜访版退役下线，终版单文件已归档 Vault。
  //   31 页初次拜访版（builder / 产物 / 专属 QA 三件一并删除）的文案 canon 仍活在两处：
  //   引擎 deck 的 R1 页（双源 canon 溯源注释）与本速讲版 8 页 —— 内容不随路由消失。
  // convoai 的速讲变体：8 页 Infograph，讲者不翻页；重建 build-convoai-info.py · 自检 qa-convoai-info.mjs。
  { slug: "convoai-info", title: "声网对话式 AI · 一页一章 Infograph（拜访速讲版）", slides: 8, category: "演讲", dual: true },
  // 2026-08-24 Colin：社区 /eli5 skill 的方法论（「讲给完全不懂的人：大图、少字」）
  //   × colin-deck 家族语言 = 引擎 22 页深入讲解版的 ELI5 版本。
  //   口吻拍板为**大人也爱看的五岁版**：科普大白话 + 生活类比，客户高管和朋友圈都能秒懂转发，
  //   不是幼儿童话腔。默认浅底（转发场景，链接一打开就得是亮的）。
  //   三条硬闸（写进 qa-convoai-eli5.mjs，是这份 deck 存在的理由）：
  //     ① 每页 = 一句人话大标题 + 一张大图（带动效）+ 至多一行小注；
  //     ② 大图统一 1680×744 = 舞台的 60.28%，十一页同尺寸同位置（余量 0.28pp，缩图必触闸）；
  //     ③ 每页可见正文（眉标 / 标题 / 页码 / SOURCE 之外，含图内标签）≤ 40 个汉字。
  //   数字纪律：只用既有 canon（650ms / 340ms / 95% / 200+ 节点），
  //     人话大字 + 原数小标**同屏并存**（不到一秒 / 650ms · 端到端），禁止新造数字 ——
  //     QA 里有一条数字白名单反向闸，出现表外数字当场触闸。
  //   红线：客户名一个不进（科普 deck 不上案例）· Call Agent 不进（只讲引擎故事）·
  //     a[href]=0（「大人版」指路走纯文本 colinyao.com/convoai）· 价格 / staging / 盲测 / 32,000 全不入。
  //   末页「对话即交互」与引擎深入讲解版封面同句 —— 两份 deck 在这里合上，家族闭环。
  //   重建：python3 scripts/build-convoai-eli5.py（单产物，无 twin 别名）
  //   自检：node scripts/qa-convoai-eli5.mjs（THEME=dark 二跑）+ DECK=eli5 node scripts/qa-motion.mjs
  { slug: "convoai-eli5", title: "声网 · 对话式 AI · 讲给五岁的你", slides: 11, category: "演讲", dual: true },
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
  // robot26 v2 = 《RTE春夏巡游北京站-ColinVFinal.pptx》36 页**一比一还原**（不是改编）：
  // 视觉忠于 PPT 自己的模板（纯黑底 + #D4B7F9 淡紫），因此是**单一视觉**、没有深浅切换按钮
  //（dual 在这里读作「无 -light 双文件」，与 aiot26-conf 单主题同例）。
  // 老的 0516 深圳改编版（42 页 colin-deck 视觉）归档在 public/decks/robot26-v0516.html，不注册路由。
  // R22（2026.08）换模板：会场双 logo 条 + 场次角标全删，底色体系换成 Colin 暗色 deck 的
  //   做法（黑底 + 底流场 + 栏线网格 + 右上 colinyao.com 落款），排版/图片/动效/字号一律不动。
  //   下面的 venue 是**讲次档案**（这场在哪儿讲的），不是 deck 里的 chrome —— deck 内已零场次痕迹。
  // 重建：python3 scripts/build-robot26-bj.py（数据 scripts/assets/robot26-bj-*.json）
  // 自检：node scripts/qa-robot26.mjs（含 R22 段：痕迹清零 / 模板 token / 金句连号 / mono 裁字）
  { slug: "robot26", num: "12", date: "2026.05", venue: "RTE 春夏巡游 · 北京（PPT 原稿还原）", title: "从玩具到伙伴：消费级机器人的「活人感」交互设计", slides: 37, category: "对外演讲", dual: true },
  { slug: "dual26", num: "11", date: "2026.04", venue: "中国网络视听大会", title: "RTE + AI 双引擎驱动视听全域商业增长", slides: 20, category: "对外演讲", dual: true },
  { slug: "vibesota", num: "10", date: "2026.01", venue: "Voice Agent 闭门会", title: "Voice Agent 2026 · Vibe SOTA", slides: 28, category: "对外演讲", dual: true },
  { slug: "vibecheck", num: "09", date: "2026.01", venue: "First Prompt · Singapore", title: "No More Prompts — How Conversation Agents Pass the Vibe Check", slides: 21, category: "对外演讲", dual: true },
  { slug: "pm25", num: "08", date: "2025.12", venue: "人人都是产品经理大会 2025", title: "从「活人感」缺失到体验基准打造", slides: 41, category: "对外演讲", dual: true },
  { slug: "prodready", num: "07", date: "2025.10", venue: "ConvoAI & RTE 2025", title: "Production-Ready 对话式 AI 产品全栈发布", slides: 22, category: "对外演讲", dual: true },
  { slug: "era3", num: "06", date: "2025.10", venue: "ConvoAI & RTE 2025", title: "Agent 交互核心引擎，重塑实时体验的第三纪元", slides: 39, category: "对外演讲", dual: true },
  { slug: "engine25", num: "05", date: "2025.08", venue: "全球产品经理大会", title: "Agent 交互核心引擎，重构人机协同体验革命", slides: 39, category: "对外演讲", dual: true },
  { slug: "audio25", num: "04", date: "2025.03", venue: "中国网络视听大会", title: "对话式 AI 驱动 AI 音频体验革新", slides: 24, category: "对外演讲", dual: true },
  // R29 勘误：本条原 slug 也是 "convoai"，2026-08-12 拜访 deck 立项时文件被覆盖、slug 撞车。
  // 档案版从 git 恢复后迁至 /convoai25（旧 /convoai 现为拜访 deck，索引/年表/尺子回链已随迁）。
  { slug: "convoai25", num: "03", date: "2025.03", venue: "ConvoAI 产品发布会", title: "ConvoAI 对话式 AI 引擎 · 正式发布", slides: 27, category: "对外演讲", dual: true },
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
  { slug: "gptlive", num: "15", title: "「端到端」正在被泛化成一个营销标签——拆解 GPT-Live", slides: 40, category: "公众号", dual: true },
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

// 情报页（内参 · 不进 /decks 索引渲染，仅 allDecks 参与路由与 noindex 头）
// 2026-08-31 Colin：敌情月度洞察按留档上线规程发布，locked 私享直链；索引页三数组不含本组。
export const intelDecks: Deck[] = [
  { slug: "intel-2026-08", title: "2026-08 敌情月度洞察 · 盯发货，别盯发布会", slides: 9, category: "情报", dual: true, locked: true },
];

export const allDecks = [...speechDecks, ...talkDecks, ...essayDecks, ...intelDecks];

/** 供 next.config 生成 rewrites/headers 的路由清单 */
export const deckRoutes: { source: string; file: string }[] = [
  ...allDecks.map((d) => ({ source: `/${d.slug}`, file: `/decks/${d.slug}.html` })),
  { source: "/newcollege-light", file: "/decks/newcollege-light.html" },
  // aiot26 叙事重构版（26 页 · 默认浅底）· 预览路由，Colin 定稿前不进 talkDecks 索引
  { source: "/aiot26-v2", file: "/decks/aiot26-v2.html" },
  // cowork-conf R21 终稿（46 页 · 删陪伴整章 + 逐页删文 + 两页拆分 + 八页删改 + 十三页删改与数据换血
  // + PART 1 幕卡后新增「AI 投资资金流向 2024→2026」一页 + R13 七处内容修订
  // + R14 P2 讲台 / 资金流向页重做成双轴时间图
  // + R15 终轮十项（三张主标题 / CONVOAI AGENT / 北极星逐列对齐 / PART 2 幕卡金句 / 三处删段
  //   / Weil 归金句页 / 自治爬梯 L0-L4 → L1-L5 全 deck 连坐 / 终检）
  // + R16 五处（金句 01 换血「叫了三年 Agent」/ PART 2 幕卡首行还原 / 金句 02·03 中上英下
  //   / 金句 03 出处改正为 Des Traynor · Cheeky Pint #11 / P7 资金流向图数据重查 + 弃双轴改三格小倍数）
  // + R17 熵减十二处（P27/P31/P46/P8/P9/P7/P15/P24 八页删文撑满 + 四张 PART 幕卡开头小字全删
  //   / P31 案例 03 事件主体实名为 OpenAI × Hugging Face / P45 收束页标题对调
  //   / P4 出处精化为 Cheeky Pint #27）
  // + R18 一处（P44 那两个 SVG 门 → Colin 用 GPT-image 生成的单张门图，
  //   scripts/assets/r18-doors.webp 78KB 内联成 data URI · mix-blend-mode:screen 融底）
  // + R19 五处（P7 三格小倍数 → 单轴对数三线图「带时间轴的曲线」，数据一个不动、不回双轴
  //   / 五张金句页 eyebrow 全删 / 金句 02 署名 ex CPO / P31 三段教训正文删 + 教训 03 改题
  //   / P44 删 CEO 那行 + 门图 1380 → 1180）
  // + R20 **终稿**五处（P7 对数轴 → 分段断轴 $0–$4B / $30–$180B 两段线性 + 写代码线换金黄
  //   / P28 交叉验证条带只留自动驾驶一列 / P40「有人用了三年还停在这条线上」归位到「最难跨的一段」
  //   / P43 删「但只讲个人是不公平的。」；P30 点名待 Colin 定夺，本轮未动）
  // + R21 **终稿收口**一页三处（P30 署名实名化为 Eric Glyman · Ramp 联合创始人 · Cheeky Pint 2026-02
  //   / 左侧「10 万+」补 Glyman 逐字原话 [00:06:30] / 右侧「自我认证」补 John Collison
  //   逐字原话 [00:08:09] + 署名 —— 数是 Ramp 的、「不能自我认证」是 Stripe 的，两家各归各）
  // · 大会 conf 视觉）· 预览路由，
  // Colin 定稿前不进 speechDecks 索引；线上 /cowork-conf 仍是 55 页原版。
  // 同源同脚本：CONF_V2=1 python3 scripts/build-conf.py
  { source: "/cowork-confv2", file: "/decks/cowork-confv2.html" },
  // aiot26 正讲版（37 页 · 大会 conf 视觉 · 8.9 正讲版）= V3 内容层 + 大会黑紫金视觉层（单主题）
  // ACT04 为「问题驱动 · 逐题作答」五问结构；页数无独立字段，仅此注释登记
  { source: "/aiot26-conf", file: "/decks/aiot26-conf.html" },
  // 私人页（非 deck）：卧推 100kg 训练计划（2026.8.31–11.11 · 11 周周期化）。
  // 只走私享链接 /bench100，不进任何索引/导航/sitemap；noindex 走 meta + /decks/* 头双重。
  { source: "/bench100", file: "/decks/bench100.html" },
  // 2026-08-30 Colin：贷后催收方案 deck · 私享不进索引。
  //《AI 驱动的智能贷后催收解决方案》15 页 —— 面向银行 / 消费金融 / 互金平台的贷后、
  // 风控、合规、技术负责人，销售方案汇报场景。内容蓝本是 Vault 的
  // ai-debt-collection-ppt-outline.md（14 页大纲 + 第 4 节建议的试点 KPI 页，
  // 按 Colin 指令插在落地场景之后 ⇒ 15 页）。CONF 家族语言、conf-light 默认、
  // 单文件双主题、零分步、五运动原语逐字复用（P5 八环闭环是标杆动效页，
  // P11 中枢 + 八模块是第二动效重点）。
  // 口径纪律两条（改数之前先读 builder 文件头）：
  //   ① 行业侧数字逐字用大纲的，每个都带来源机构名 + 时点，一个不新造、不外推；
  //   ② Agora 侧硬数只用司内 canon（650ms / 340ms / 95% / 900亿+ 单月分钟数 /
  //      200+ 全球节点 SD-RTN），**大纲里「800 亿分钟 · 200+ 国家和地区」是英文官网
  //      旧口径，已仲裁不用** —— 同一家公司两份材料给两个数量级的分钟数，客户当场就问。
  // 表达红线（构建期断言 + qa 反向闸双保险）：催债 / 施压催收 / 逼迫还款 / 强催 /
  //   轰炸外呼 / 暴力催收 六词全文 0；「回收率」不与百分比同句（不承诺提升比例）；
  //   客户名 0（含在谈的「光潽」）；Call Agent / 价格 / staging / 盲测 / 32,000 全不入；
  //   a[href] = 0。
  // 2026-08-30 修订（GPT 5.6 review 仲裁采纳集 + Colin 四项输入）：
  //   · 封面 kicker 补版本标 CHINA EDITION（与 SEA EDITION · VIETNAM ANCHOR 区分）；
  //   · P2 / P8 / P10 三张**趋势断言**页各挂一枚判断标（行业判断 · AGORA VIEW），
  //     标题主句不动 —— 销售叙事保留，标注即诚实；P9 交叉参考卡挂「全球品类代理指标 ·
  //     非可服务市场规模」。.vtag 全 deck 只许这四枚（qa 有枚数上限闸）。
  //   · 口径行 .scope（新件，与 SOURCE ledger 分工：ledger 答「哪来的」，口径行答
  //     「能推什么、不能推什么」）：P3 商业银行法人口径、P4 卡量期末存量、
  //     P7《办法》适用主体 = 持牌消金 + GB/T = 推荐性国标、P12 vendor 生态。
  //   · P12 补 17+ 家 TTS 供应商名单（出处 docs.agora.io）；该节点挂 data-nogate="vendor"，
  //     qa 的**客户名反向闸**整枝跳过它（名单里是供应商不是客户案例，豁免只放这一枚）。
  //   · P13 / P15 落一枚脱敏 proof point（日均呼叫量 100 万通）⇒ **P13 入 SOURCE ledger
  //     名单，全 deck 六行**；P11 加治理要求带（措辞是验收口径，不是功能声明）。
  // 重建：python3 scripts/build-convoai-postloan.py
  // 自检：node scripts/qa-convoai-postloan.mjs（THEME=dark 二跑）
  //      + DECK=postloan node scripts/qa-motion.mjs
  { source: "/convoai-postloan", file: "/decks/convoai-postloan.html" },
  // 2026-08-30 Colin：东南亚英文版 · 私享不进索引 · 同链语言切换。
  //《AI-Powered Post-Loan Collections & Overdue Asset Management》SEA EDITION 15 页 ——
  // 面向东南亚金融机构（银行 / 消费金融 / fintech 平台）的贷后、风控、合规、技术负责人，
  // 首场越南，后续新加坡 / 印尼 / 泰国 / 菲律宾 / 日本 / 韩国。
  // **不是中文版的直译，是市场重铸**：版式、图形、动效系统与中文版逐格同构，
  //   行业侧内容整层换血 —— P3 中国三大数 → e-Conomy SEA 2025 定性引用（不写贷款余额数字）、
  //   P4 卡量两点时序 → **越南 2021 禁令锚点页**（《投资法》61/2020/QH14 把 debt collection
  //   services 列为禁止投资经营业务 ⇒ 外包这条路被法律关掉，唯一路径是自建 + 技术化）、
  //   P7 中国部门规章 / 国标 → **SBV Circular 18/2019/TT-NHNN 监管规格卡**
  //   （≤5 次/日 · 07:00–21:00 · 不得向无还款义务的第三方催告 · 措施须合法）+ 区域条
  //   （OJK / BSP / BOT / MAS 只列机构名，不写各国具体条款 —— 未核）。
  //   P9 市场三层与 P12 Agora canon 天然全球口径，逐条英译沿用。
  // 口径纪律（改数之前先读 builder 文件头）：
  //   ① 行业侧只用 Colin 核过的一手来源，每条带机构名 + 时点，一个不新造、不外推；
  //   ② Agora 侧只用司内 canon（650ms / 340ms / 95% / 90B+ minutes monthly /
  //      200+ global nodes · SD-RTN）；
  //      **IDC 中国市占 No.1 不进英文版** —— 中国市场信任状对 SEA 听众无效且要解释成本。
  //   ③ 2026-08-30 · **仅英文版**：OpenAI 口径改为「named an integration partner at the
  //      2024 OpenAI Realtime API launch」（贴官方发布文可验）；旧转译
  //      "global first-batch partner" 进 qa 的 STALE 名单，回归即 fail。
  //      **中文版的家族 canon 本轮不动** —— 家族级口径变更待 Colin 拍板。
  // 表达红线（构建期断言 + qa 反向闸双保险）：debt chasing / chase debtors /
  //   pressure tactics / aggressive collection / harass / intimidat 六串全文 0；
  //   `threaten` 只准出现 1 次且必须落在 P7 引述监管禁令的 [data-nogate] 节点里；
  //   整份 deck 只准两个百分数（95% / 9.72%），不承诺任何提升比例；客户名 0；
  //   Call Agent / 价格 / staging / 32,000 全不入；a[href] = 0；
  //   **除左下角语言钮的「中文」二字外全页零 CJK**（QA 纯度闸）。
  // 同链路语言切换：两份 deck 各挂一枚常显 pill（左下角、摞在主题钮之上），
  //   中文版「EN」→ /convoai-postloan-en，英文版「中文」→ /convoai-postloan。
  //   ⚠ 必须 <button> + JS 跳转，**不能用 <a>**（两份 deck 的 a[href]=0 闸都还在）。
  // 2026-08-30 修订（与中文版同一轮，英文版另有五条）：
  //   · 封面 kicker → SEA EDITION · VIETNAM ANCHOR（事实骨架全是越南一手来源）；
  //   · P4 措辞弱化：「THE ONLY PATH」→「WHAT REMAINS · IN-HOUSE」，论证句改成
  //     「法律禁的是催收服务这条业务线；贷款机构保留合规自催责任 —— 技术是把它做到规模的
  //     方式，不是法定义务」。禁令三段式结构一格不动。
  //   · P7 精度三件：kicker → VIETNAM · FINANCE-COMPANY GUARDRAILS（适用范围收紧）、
  //     补 Circular 18/2019 的适用范围小注、「No third-party contact」→
  //     「No contact with non-obligor third parties」、区域条标题写明 REGULATOR NAMES ONLY。
  //   · P3 加「ALREADY AT SCALE ON AGORA」证据带，用 info 家族 P2 的两枚 canon
  //     （Top 10,000 RTC App 近一半 / 1M+ 注册应用）——**刻意避开 P12 已用的两枚**，
  //     qa 有「两页不许撞数」的反向闸。
  //   · **全文美式拼写**（-ise/-isation → -ize/-ization、fulfilment → fulfillment、
  //     judgement → judgment、ageing → aging、instalment → installment、behaviour → behavior
  //     …逐词替换，不用裸正则）；qa 加拼写闸，命中即 fail。
  //   其余（版本标 / 判断标 / 口径行 / vendor 生态 / proof point 双落位 + P13 入 ledger /
  //   治理要求带 / 试点第五条 / KPI 口径字典）与中文版逐条同源。
  // 重建：python3 scripts/build-convoai-postloan-en.py
  // 自检：node scripts/qa-convoai-postloan-en.mjs（THEME=dark 二跑，含 CJK 纯度闸 +
  //      美式拼写闸 + 语言钮闸 + 两版互跳 round-trip 实测）
  //      + DECK=postloan-en node scripts/qa-motion.mjs
  { source: "/convoai-postloan-en", file: "/decks/convoai-postloan-en.html" },
  // 2026-08-31 Colin：three.js Phase 0 spike · 私享实验路由 · 不进任何索引数组。
  // /lab-globe = SD-RTN 全球实时网络地球原型，验证 WebGL 能不能进生产 deck：
  // 陆地点云（14.5k 点 · 构建期离线栅格化 · 位掩码内嵌 8.5KB）+ 228 枚示意节点 +
  // 五槽并发大圆弧飞包 + 双主题实时换色（材质色全部 getComputedStyle 读 --g-* CSS
  // 变量，three 代码里零色号）+ poster SVG 降级层（与 WebGL 逐字同参的相机矩阵
  // 离线投影，WebGL 起不来就常驻）+ reduced-motion 停帧 / print 藏 canvas /
  // document.hidden 掐 rAF / DPR ≤ 2。three r185 自托管在
  // public/decks/assets/three/（three.module.min.js + three.core.min.js +
  // OrbitControls.js），页面走 importmap 指自托管路径，**零外链**。
  // 数字红线：全页只许出现「200+」与「毫秒级」，弧线一律不标延迟数值。
  // 重建：node scripts/build-lab-globe.mjs
  //      （陆地数据重生成才需要 node scripts/build-lab-globe-land.mjs，
  //        依赖 npm i world-atlas topojson-client，仅构建期）
  // 自检：node scripts/shot-lab-globe.mjs（lab 级：双主题静置 + 拖拽 + 禁 WebGL
  //      降级 + reduced-motion + pageerror=0 + 双主题 GIF + FPS 记录）
  { source: "/lab-globe", file: "/decks/lab-globe.html" },
];
