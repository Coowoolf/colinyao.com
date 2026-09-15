import type { Metadata } from "next";
import Gate from "@/components/Gate";

// 口令门页：middleware 把没带 cookie 的 /bema、/bema-irte 等 rewrite 到这里（地址栏不变）
export const metadata: Metadata = {
  title: "口令",
  robots: { index: false, follow: false, nocache: true },
};
export const dynamic = "force-dynamic";

const OK_NEXT = /^\/[A-Za-z0-9_\-./]*$/;

export default async function GatePage({ searchParams }: { searchParams: Promise<{ next?: string | string[] }> }) {
  const sp = await searchParams;
  const raw = Array.isArray(sp.next) ? sp.next[0] : sp.next;
  const next = raw && OK_NEXT.test(raw) && !raw.startsWith("//") ? raw : "/";
  return <Gate next={next} />;
}
