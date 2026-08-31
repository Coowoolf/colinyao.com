#!/usr/bin/env node
/* =========================================================================
   /lab-globe · 陆地点云数据生成器（构建期离线，运行时零外部请求）
   -------------------------------------------------------------------------
   输入：npm 包 world-atlas 的 land-50m.json（Natural Earth 1:50m 陆地面，
        TopoJSON）。**只在构建期用**，node_modules 不入库。
        跑之前先： npm i world-atlas topojson-client
   算法：
     ① Fibonacci 球面点阵（黄金角螺旋）取 N 个候选点 —— 等面积、无极点堆积，
        且运行时用 5 行代码即可逐点复现同一序列（所以只需回传一条 land/ocean
        位掩码，不需要回传任何坐标）。
     ② 逐点做 lon/lat 平面 even-odd 射线判定（按纬度分桶加速）。
     ③ 位掩码 → base64 字符串，直接内嵌进 lab-globe.html。
   输出：scripts/assets/lab-globe-land.json  { n, bits(base64), landCount }
   用法： node scripts/build-lab-globe-land.mjs [N]
   ========================================================================= */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const N = Number(process.argv[2] || 52000);

// ── ① 读 TopoJSON → GeoJSON ────────────────────────────────────────────────
let topo, feature;
try {
  topo = require("world-atlas/land-50m.json");
  ({ feature } = require("topojson-client"));
} catch {
  console.error("缺依赖：npm i world-atlas topojson-client");
  process.exit(1);
}
const geo = feature(topo, topo.objects.land);
const polys = [];
const pushPoly = (p) => polys.push(p);
const g = geo.type === "FeatureCollection" ? geo.features.map((f) => f.geometry) : [geo.geometry || geo];
for (const gg of g) {
  if (!gg) continue;
  if (gg.type === "Polygon") pushPoly(gg.coordinates);
  else if (gg.type === "MultiPolygon") gg.coordinates.forEach(pushPoly);
}

// ── 边表 + 纬度分桶 ────────────────────────────────────────────────────────
/** edge = [lon1, lat1, lon2, lat2] */
const edges = [];
for (const rings of polys) for (const ring of rings) {
  for (let i = 0; i < ring.length - 1; i++) {
    const a = ring[i], b = ring[i + 1];
    if (a[1] === b[1]) continue;            // 水平边对 even-odd 无贡献
    edges.push([a[0], a[1], b[0], b[1]]);
  }
}
const BANDS = 180, band = (lat) => Math.min(BANDS - 1, Math.max(0, Math.floor((lat + 90) / 180 * BANDS)));
const buckets = Array.from({ length: BANDS }, () => []);
for (const e of edges) {
  const lo = band(Math.min(e[1], e[3])), hi = band(Math.max(e[1], e[3]));
  for (let b = lo; b <= hi; b++) buckets[b].push(e);
}

/* Natural Earth 的 Antarctica 环最南只到 -85.19（南极点那块由制图闭合边切掉了），
   直接用会在南极开一个洞 —— 球一转就露馅。示意图口径下把 -85 以南整片补成陆地。 */
const SPOLE_CAP = -85.0;

function isLand(lon, lat) {
  if (lat <= SPOLE_CAP) return true;
  const bs = buckets[band(lat)];
  let crossings = 0;
  for (let i = 0; i < bs.length; i++) {
    const [x1, y1, x2, y2] = bs[i];
    if ((y1 > lat) !== (y2 > lat)) {
      const xi = x1 + ((lat - y1) / (y2 - y1)) * (x2 - x1);
      if (xi > lon) crossings++;
    }
  }
  return (crossings & 1) === 1;
}

// ── ② Fibonacci 球面点阵（运行时逐字复现这段） ─────────────────────────────
const GA = Math.PI * (3 - Math.sqrt(5));   // 黄金角
const bytes = new Uint8Array(Math.ceil(N / 8));
let landCount = 0;
for (let i = 0; i < N; i++) {
  const y = 1 - (2 * (i + 0.5)) / N;
  const r = Math.sqrt(Math.max(0, 1 - y * y));
  const th = i * GA;
  const x = Math.cos(th) * r, z = Math.sin(th) * r;
  const lat = (Math.asin(y) * 180) / Math.PI;
  // 经度约定必须与页面的 ll2v 逐字一致：x = cosφ·sinλ, z = cosφ·cosλ ⇒ λ = atan2(x, z)。
  // （写成 atan2(z,x) 会让陆地相对节点表整体转 90° 又镜像 —— 踩过一次。）
  const lon = (Math.atan2(x, z) * 180) / Math.PI;
  if (isLand(lon, lat)) { bytes[i >> 3] |= 1 << (i & 7); landCount++; }
}

// ── ③ 落盘 ────────────────────────────────────────────────────────────────
const b64 = Buffer.from(bytes).toString("base64");
mkdirSync(new URL("./assets/", import.meta.url), { recursive: true });
const out = new URL("./assets/lab-globe-land.json", import.meta.url);
writeFileSync(out, JSON.stringify({ n: N, landCount, bits: b64 }));
console.log(`N=${N}  land=${landCount} (${((landCount / N) * 100).toFixed(1)}%)  base64=${(b64.length / 1024).toFixed(1)}KB`);

// ── ASCII 目检（确认大陆轮廓对得上，不是一团乱码） ──────────────────────────
if (process.env.PREVIEW) {
  const W = 120, H = 44, rows = [];
  for (let r = 0; r < H; r++) {
    let s = "";
    for (let c = 0; c < W; c++) {
      const lon = -180 + (c + 0.5) / W * 360;
      const lat = 90 - (r + 0.5) / H * 180;
      s += isLand(lon, lat) ? "#" : ".";
    }
    rows.push(s);
  }
  console.log(rows.join("\n"));
}
