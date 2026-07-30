# colinyao.com

姚光华（Colin Yao）的个人网站 —— 思想档案馆。

> 同一把尺子，向外叫 Eval，向内叫内观。

## 技术

- Next.js 15（App Router，全静态预渲染）
- 无 CSS 框架：`app/globals.css` 即全站设计系统（Colin 暗底 editorial 视觉语言 + 五层流动感动效）
- 字体自托管（Satoshi / JetBrains Mono），中文走系统栈（PingFang SC / MiSans / 思源黑体）——国内访问无第三方依赖
- 内容全部数据文件化：`content/talks.ts`（演讲档案）、`content/ideas.ts`(概念库)、`content/site.ts`（站点信息与链接）

## 日常维护

- **新增一场演讲**：在 `content/talks.ts` 的数组头部加一个对象
- **新增一个概念**：在 `content/ideas.ts` 加一张卡
- **改链接 / 头衔**：`content/site.ts`

改完 `git push`，Vercel 自动部署。

## 本地开发

```bash
npm install
npm run dev
```

## 视觉自检

```bash
npm run build && npm start &
CHROMIUM_PATH=<chromium 路径> node scripts/shots.mjs   # 截图到 /tmp/shots
```
