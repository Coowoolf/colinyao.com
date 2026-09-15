import { NextResponse, type NextRequest } from "next/server";
import { COOKIE, GATED, gateToken, tokenOk } from "@/lib/gate";

// 口令门：GATED 里的路径没有有效 cookie → rewrite 到 /gate（地址栏仍是原路径，输对口令后 reload 即进）
export const config = { matcher: ["/bema", "/bema-irte", "/decks/bema.html", "/decks/bema-irte.html"] };

export async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;
  if (!GATED.includes(path)) return NextResponse.next();
  const token = await gateToken();
  if (tokenOk(req.cookies.get(COOKIE)?.value, token)) return NextResponse.next();
  const url = req.nextUrl.clone();
  url.pathname = "/gate";
  url.search = "";
  url.searchParams.set("next", path);
  const res = NextResponse.rewrite(url);
  res.headers.set("X-Robots-Tag", "noindex, nofollow");
  res.headers.set("Cache-Control", "no-store");
  return res;
}
