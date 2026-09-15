import { NextResponse } from "next/server";
import { COOKIE, COOKIE_DAYS, checkPass, gateToken } from "@/lib/gate";

export const runtime = "edge";
export const dynamic = "force-dynamic";

// POST {pass} → 对：下发签名 cookie（30 天）· 错：401（拖 500ms，别让人拿脚本试）
export async function POST(req: Request) {
  let pass = "";
  try {
    const body = (await req.json()) as { pass?: unknown };
    pass = typeof body?.pass === "string" ? body.pass : "";
  } catch {
    pass = "";
  }
  const ok = await checkPass(pass);
  if (!ok) {
    await new Promise((r) => setTimeout(r, 500));
    return NextResponse.json({ ok: false }, { status: 401, headers: { "Cache-Control": "no-store" } });
  }
  const res = NextResponse.json({ ok: true }, { headers: { "Cache-Control": "no-store" } });
  res.cookies.set(COOKIE, await gateToken(), {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 24 * COOKIE_DAYS,
  });
  return res;
}
