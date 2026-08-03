# 新会话交接包 · colinyao.com / cowork

> 旧云端会话的设备桥绑定在服务端损坏（诊断结论：仅剩 get_device_info 且报设备未绑定，
> 重启/重连文件夹/退出重登均无效）。本包让新会话零上下文损失接管。

## 当前状态
- 站点与 /cowork（65 页 V10）最新版已上线；**完整变更史 = 本仓库 git log**（每条 commit 摘要即 changelog）。
- colin-deck skill（账户级）四条硬要求照常：双主题单文件 / 流动感动效 / 三道闸门 / Vault+站点双落点。
- 纪律：deck 路由永远 noindex；锁定 deck（/cowork 2026.08 首发前）不挂公链；内部 roadmap 不上站。

## 待办 1 · Vault 写回（桥恢复后第一件事）
1. 用 `_handover/V10_从被托付到共事_浅底.html` 覆盖
   `Vault/07-个人品牌与成长/演讲档案/V10_从被托付到共事_浅底.html`
2. `Vault/11-Side Projects/colinyao.com/colinyao.com-设计文档.md`：
   按本仓库最近 6 条 commit 的摘要补记 changelog（2026-08-01 起），或请 Colin 把旧会话里
   已交付的设计文档文件直接给你。

## 待办 2 · 2026 AI 产品大会模板版
- 模板：`Vault/+Inbox/` 内的 PPT 模板（文件名以实际为准）。
- 流程：pptx 解包（主题色/字体/母版版式/logo/封面页脚规范）→ 输出对齐清单 →
  以 `public/decks/cowork.html`（65 页）为内容底，整体换装出大会视觉版
  `public/decks/cowork-conf.html` → 登记 content/decks.ts（noindex，不进导航，locked 同 /cowork）→
  三道闸门 QA → push 上线 → 大会版 HTML 留档 `Vault/07-个人品牌与成长/演讲档案/`。

## 待办 3 · 杂项
- Comma 作品卡（首页 #works）缺链接：等 Colin 指定可公开的仓库/落地页。
- GitHub PAT 临近到期（约一周周期），推送失败时提醒 Colin 换新。
