// 重算口令门的兜底哈希：node scripts/gate-hash.mjs <口令> → 粘到 lib/gate.ts 的 PASS_HASH_FALLBACK（口令本身不进仓库）
import { createHash } from "node:crypto";
const pass = process.argv[2];
if (!pass) { console.error("usage: node scripts/gate-hash.mjs <pass>"); process.exit(1); }
console.log(createHash("sha256").update("colinyao-deck-gate:" + pass).digest("hex"));
