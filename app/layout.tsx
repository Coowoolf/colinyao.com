import type { Metadata, Viewport } from "next";
import "./globals.css";
import FlowField from "@/components/FlowField";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import { site } from "@/content/site";

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: site.title,
    template: "%s · Colin Yao",
  },
  description: site.description,
  keywords: ["姚光华", "Colin Yao", "对话式AI", "Voice Agent", "活人感", "ConvoAI", "Eval", "对话式智能体"],
  openGraph: {
    title: site.title,
    description: site.description,
    url: site.url,
    siteName: "colinyao.com",
    locale: "zh_CN",
    type: "website",
    images: [{ url: "/og.png", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    title: site.title,
    description: site.description,
    images: ["/og.png"],
  },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  themeColor: "#0f0e17",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <head>
        {/* 首帧主题引导（防闪烁）+ 有 JS 才启用入场初态；
            兜底：2.6s 内动效系统未唤醒（弱网 hydration 慢）则强制显示全部内容 */}
        <script
          dangerouslySetInnerHTML={{
            __html:
              "try{if(localStorage.getItem('colin-theme')==='light')document.documentElement.dataset.theme='light'}catch(e){}document.documentElement.classList.add('js');setTimeout(function(){if(!document.querySelector('.rv.visible'))document.documentElement.classList.add('anim-fallback')},2600);",
          }}
        />
      </head>
      <body>
        <FlowField />
        <Nav />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
