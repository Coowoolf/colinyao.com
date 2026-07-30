import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // 隐藏 deck 路由：不进导航、不进 sitemap、不给搜索引擎收录
  async rewrites() {
    return [
      { source: "/newcollege", destination: "/decks/newcollege.html" },
      { source: "/newcollege-light", destination: "/decks/newcollege-light.html" },
      { source: "/3years", destination: "/decks/3years.html" },
      { source: "/trust", destination: "/decks/trust.html" },
      { source: "/trust-light", destination: "/decks/trust-light.html" },
    ];
  },
  async headers() {
    return [
      {
        source: "/(newcollege|newcollege-light|3years|trust|trust-light|decks/:path*)",
        headers: [{ key: "X-Robots-Tag", value: "noindex, nofollow" }],
      },
    ];
  },
};

export default nextConfig;
