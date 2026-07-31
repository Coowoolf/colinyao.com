import type { NextConfig } from "next";
import { deckRoutes } from "./content/decks";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // 隐藏 deck 路由：不进导航、不进 sitemap、不给搜索引擎收录（清单见 content/decks.ts）
  async rewrites() {
    return deckRoutes.map((r) => ({ source: r.source, destination: r.file }));
  },
  async redirects() {
    return [
      { source: "/ruler", destination: "/", permanent: true },
      { source: "/talks", destination: "/#timeline", permanent: true },
      { source: "/ideas", destination: "/#terms", permanent: true },
      { source: "/index", destination: "/", permanent: true },
      { source: "/toc", destination: "/", permanent: true },
      { source: "/book", destination: "/", permanent: true },
      { source: "/about", destination: "/#about", permanent: true },
    ];
  },
  async headers() {
    const noindex = [{ key: "X-Robots-Tag", value: "noindex, nofollow" }];
    return [
      ...deckRoutes.map((r) => ({ source: r.source, headers: noindex })),
      { source: "/decks", headers: noindex },
      { source: "/decks/:path*", headers: noindex },
    ];
  },
};

export default nextConfig;
