// 隐藏 deck 的口令门（2026-09-15 Colin：「给 bema 和 bema-irte 加上访问密码」）
// - 门在 middleware.ts：命中 GATED 的路径，没有有效 cookie 就被 rewrite 到 /gate（地址栏不变）
// - 口令校验在 app/api/gate/route.ts：对了就下发 30 天的签名 cookie
// - 真正的秘密请放 Vercel 环境变量：DECK_GATE_PASS（口令）· DECK_GATE_SECRET（cookie 签名密钥）
//   仓库是公开的，下面的兜底常量只挡「拿到链接就能看」，挡不住认真读仓库的人。

export const GATED = ["/bema", "/bema-irte", "/decks/bema.html", "/decks/bema-irte.html"];
export const COOKIE = "deck_gate";
export const COOKIE_DAYS = 30;

// 兜底：SHA-256("colinyao-deck-gate:" + 口令) 的 hex —— 改口令时用 scripts/gate-hash.mjs 重算
const PASS_SALT = "colinyao-deck-gate:";
const PASS_HASH_FALLBACK = "b92963e2d2b17008b9c3438eb176dac75402c0455b73ac78cbe2f731e8eb84cc";
const SECRET_FALLBACK = "bema-irte-2026-10-24-in-the-agora-one-steps-up-to-speak";

const enc = new TextEncoder();
function hex(buf: ArrayBuffer) {
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
function same(a: string, b: string) {
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

export async function checkPass(pass: string): Promise<boolean> {
  const p = (pass || "").trim();
  if (!p || p.length > 128) return false;
  const envPass = process.env.DECK_GATE_PASS;
  if (envPass) return same(p, envPass);
  const h = hex(await crypto.subtle.digest("SHA-256", enc.encode(PASS_SALT + p)));
  return same(h, PASS_HASH_FALLBACK);
}

export async function gateToken(): Promise<string> {
  const secret = process.env.DECK_GATE_SECRET || SECRET_FALLBACK;
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", key, enc.encode("deck-gate:v1")));
}

export function tokenOk(cookie: string | undefined, token: string) {
  return !!cookie && same(cookie, token);
}
