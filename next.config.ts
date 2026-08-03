import type { NextConfig } from "next";
import { deckRoutes } from "./content/decks";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // 隐藏 deck 路由：不进导航、不进 sitemap、不给搜索引擎收录（清单见 content/decks.ts）
  async rewrites() {
    return deckRoutes.map((r) => ({ source: r.source, destination: r.file }));
  },
  async headers() {
    const noindex = [{ key: "X-Robots-Tag", value: "noindex, nofollow" }];
    return [
      ...deckRoutes.map((r) => ({ source: r.source, headers: noindex })),
      { source: "/decks", headers: noindex },
      { source: "/decks/:path*", headers: noindex },
      { source: "/media/:path*", headers: noindex },
    ];
  },
};

export default nextConfig;
