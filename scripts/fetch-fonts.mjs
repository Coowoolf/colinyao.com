// 构建兜底：public/fonts 缺字体时自动下载（本仓库已内置字体，此脚本通常直接跳过）。
// 用于「无二进制文件」的部署环境（如 Vercel MCP 直传源码）。下载失败不阻塞构建。
import { existsSync, mkdirSync, writeFileSync } from "node:fs";

const DIR = "public/fonts";
const JBM = (w) =>
  `https://cdn.jsdelivr.net/npm/@fontsource/jetbrains-mono@5.2.5/files/jetbrains-mono-latin-${w}-normal.woff2`;

const wanted = {
  "Satoshi-500.woff2": null,
  "Satoshi-700.woff2": null,
  "Satoshi-900.woff2": null,
  "JetBrainsMono-400.woff2": JBM(400),
  "JetBrainsMono-500.woff2": JBM(500),
};

const missing = Object.keys(wanted).filter((f) => !existsSync(`${DIR}/${f}`));
if (missing.length === 0) {
  console.log("[fonts] all present, skip");
  process.exit(0);
}

mkdirSync(DIR, { recursive: true });

try {
  if (missing.some((f) => f.startsWith("Satoshi"))) {
    const css = await (await fetch("https://api.fontshare.com/v2/css?f[]=satoshi@500,700,900&display=swap")).text();
    for (const block of css.match(/@font-face\s*{[^}]+}/g) ?? []) {
      const w = block.match(/font-weight:\s*(\d+)/)?.[1];
      const u = block.match(/url\('(\/\/cdn[^']+?\.woff2)'\)/)?.[1];
      if (w && u) wanted[`Satoshi-${w}.woff2`] = "https:" + u;
    }
  }
  for (const f of missing) {
    const url = wanted[f];
    if (!url) continue;
    const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
    writeFileSync(`${DIR}/${f}`, buf);
    console.log(`[fonts] fetched ${f} (${buf.length}B)`);
  }
} catch (e) {
  console.warn("[fonts] fetch failed, system fallback will be used:", e.message);
}
