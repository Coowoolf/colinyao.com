#!/usr/bin/env node
/* ═══════════════════════════════════════════════════════════════════════════
   /lab-globe · SD-RTN 全球实时网络地球（three.js Phase 0 spike）
   ---------------------------------------------------------------------------
   产物： public/decks/lab-globe.html —— 自包含，除 /decks/assets/three/* 三个
         自托管库文件外零外链、零运行时外部请求。
   数据： scripts/assets/lab-globe-land.json（陆地位掩码，由
         scripts/build-lab-globe-land.mjs 离线生成；已入库，重建不需要 npm 依赖）
   跑：   node scripts/build-lab-globe.mjs
   自检： node scripts/shot-lab-globe.mjs

   ── 这一版替 Colin 做的美学判断（Phase 1 进生产 deck 前请先推翻我）─────────
   · 陆地点云 14481 枚（Fibonacci 球面点阵 · ~0.93° 间距 ≈ 103km）。再密就糊成
     实心色块、丢掉「点云」的手工感；再疏东南亚群岛和加勒比就断了。
   · 弧线 5 槽并发（题给的 3–6 取中位偏上）。周期 6.4/8.1/5.5/9.3/7.2 秒两两不整除，
     起相位负偏移错开 —— 任何时刻在飞的是 3–5 条，永远不齐步。
   · 弧是「蛇」不是「烟花」：头进 62%、尾追 38%，一条线自己抽出来又收进去，
     linewidth 恒为 1px（WebGL 本来也画不粗），克制。
   · 自转 60s/圈 = 6°/s，地理正确方向（东向）。拖拽时停转，松手 2.4s 后缓入恢复。
   · 材质：浅底 = 纸面球 + 近黑 fresnel 描边（线稿），暗底 = 近黑球 + accent 霓虹
     limb + 大气辉光。所有颜色 100% 从 CSS 变量读，JS 里没有任何色号。
   ═══════════════════════════════════════════════════════════════════════════ */
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..");

/* ── 陆地位掩码 ─────────────────────────────────────────────────────────── */
const LAND = JSON.parse(readFileSync(join(HERE, "assets/lab-globe-land.json"), "utf8"));

/* 自托管 three 的版本号：直接从落库的那份文件里抠 REVISION，不靠人记 */
const THREE_REV = (() => {
  const s = readFileSync(join(ROOT, "public/decks/assets/three/three.core.min.js"), "utf8");
  const m = s.match(/(?:const|let|var)\s+(\w+)\s*=\s*"(\d{3})"[,;]/) || s.match(/"(\d{3})"/);
  return m ? m[m.length - 1] : "185";
})();

/* ── 相机 / 舞台常量（poster 与 WebGL 必须逐字同参，否则降级层会跳） ────── */
const W = 1920, H = 1080;
const FOV = 30;                       // 垂直视场角
const CAM = [0, 1.05, 4.85];          // |C| = 4.9621
const DX = 370, DY = 0;               // setViewOffset 把球心推到 (1330, 540)
const TILT = -0.30;                   // 地轴倾角（示意，非 23.44°）
const LON0 = 42;                      // 首帧正对经度：非洲—欧洲—中东居中
const Y0 = (-LON0 * Math.PI) / 180;   // spin.rotation.y 初值
const SPIN = 60;                      // 秒 / 圈

const FPX = (H / 2) / Math.tan((FOV * Math.PI) / 360);   // 焦距（像素）= 2015.3
const CD = Math.hypot(...CAM);
const GR = (FPX * 1) / Math.sqrt(CD * CD - 1);           // 球在屏上的半径 ≈ 414.6
const GCX = W / 2 + DX, GCY = H / 2 + DY;

/* ═══ 节点表 ═══════════════════════════════════════════════════════════════
   硬编码城市坐标，**示意分布**：按全球主要网络枢纽加权（亚太最密，其次欧洲 /
   北美，拉美与非洲取主要落地城市）。这不是任何一家的真实 PoP 清单，页面上也
   逐字标了「节点分布示意」。 ─────────────────────────────────────────────── */
const NODES = [
  // ── 亚太 AP ────────────────────────────────────────────────────────────
  ["Beijing",39.9,116.4,"AP"],["Shanghai",31.2,121.5,"AP"],["Shenzhen",22.5,114.1,"AP"],
  ["Guangzhou",23.1,113.3,"AP"],["Hangzhou",30.3,120.2,"AP"],["Chengdu",30.6,104.1,"AP"],
  ["Chongqing",29.6,106.6,"AP"],["Wuhan",30.6,114.3,"AP"],["Xian",34.3,108.9,"AP"],
  ["Qingdao",36.1,120.4,"AP"],["Tianjin",39.1,117.2,"AP"],["Shenyang",41.8,123.4,"AP"],
  ["Nanjing",32.1,118.8,"AP"],["Xiamen",24.5,118.1,"AP"],["Kunming",25.0,102.7,"AP"],
  ["Urumqi",43.8,87.6,"AP"],["Lhasa",29.7,91.1,"AP"],["Harbin",45.8,126.6,"AP"],
  ["HongKong",22.3,114.2,"AP"],["Taipei",25.0,121.6,"AP"],["Kaohsiung",22.6,120.3,"AP"],
  ["Seoul",37.6,127.0,"AP"],["Busan",35.2,129.1,"AP"],["Tokyo",35.7,139.7,"AP"],
  ["Osaka",34.7,135.5,"AP"],["Nagoya",35.2,137.0,"AP"],["Fukuoka",33.6,130.4,"AP"],
  ["Sapporo",43.1,141.4,"AP"],["Singapore",1.35,103.8,"AP"],["KualaLumpur",3.1,101.7,"AP"],
  ["Penang",5.4,100.3,"AP"],["Jakarta",-6.2,106.8,"AP"],["Surabaya",-7.3,112.7,"AP"],
  ["Medan",3.6,98.7,"AP"],["Denpasar",-8.7,115.2,"AP"],["Bangkok",13.8,100.5,"AP"],
  ["ChiangMai",18.8,99.0,"AP"],["HoChiMinh",10.8,106.7,"AP"],["Hanoi",21.0,105.8,"AP"],
  ["DaNang",16.1,108.2,"AP"],["Manila",14.6,121.0,"AP"],["Cebu",10.3,123.9,"AP"],
  ["PhnomPenh",11.6,104.9,"AP"],["Vientiane",18.0,102.6,"AP"],["Yangon",16.9,96.2,"AP"],
  ["BandarSeriBegawan",4.9,114.9,"AP"],["Mumbai",19.1,72.9,"AP"],["Delhi",28.6,77.2,"AP"],
  ["Bangalore",13.0,77.6,"AP"],["Chennai",13.1,80.3,"AP"],["Hyderabad",17.4,78.5,"AP"],
  ["Kolkata",22.6,88.4,"AP"],["Pune",18.5,73.9,"AP"],["Ahmedabad",23.0,72.6,"AP"],
  ["Colombo",6.9,79.9,"AP"],["Dhaka",23.8,90.4,"AP"],["Karachi",24.9,67.0,"AP"],
  ["Lahore",31.5,74.3,"AP"],["Islamabad",33.7,73.1,"AP"],["Kathmandu",27.7,85.3,"AP"],
  ["Almaty",43.2,76.9,"AP"],["Tashkent",41.3,69.3,"AP"],["Ulaanbaatar",47.9,106.9,"AP"],
  ["Sydney",-33.9,151.2,"AP"],["Melbourne",-37.8,145.0,"AP"],["Brisbane",-27.5,153.0,"AP"],
  ["Perth",-31.95,115.9,"AP"],["Adelaide",-34.9,138.6,"AP"],["Auckland",-36.9,174.8,"AP"],
  ["Wellington",-41.3,174.8,"AP"],["Christchurch",-43.5,172.6,"AP"],["PortMoresby",-9.5,147.2,"AP"],
  ["Suva",-18.1,178.4,"AP"],["Guam",13.5,144.8,"AP"],["Honolulu",21.3,-157.9,"AP"],
  ["Noumea",-22.3,166.5,"AP"],
  // ── 北美 NA ────────────────────────────────────────────────────────────
  ["NewYork",40.7,-74.0,"NA"],["Ashburn",39.0,-77.5,"NA"],["Washington",38.9,-77.0,"NA"],
  ["Boston",42.4,-71.1,"NA"],["Philadelphia",39.95,-75.2,"NA"],["Atlanta",33.75,-84.4,"NA"],
  ["Miami",25.8,-80.2,"NA"],["Tampa",27.95,-82.5,"NA"],["Charlotte",35.2,-80.8,"NA"],
  ["Nashville",36.2,-86.8,"NA"],["Chicago",41.9,-87.6,"NA"],["Detroit",42.3,-83.0,"NA"],
  ["Minneapolis",45.0,-93.3,"NA"],["StLouis",38.6,-90.2,"NA"],["KansasCity",39.1,-94.6,"NA"],
  ["Dallas",32.8,-96.8,"NA"],["Houston",29.8,-95.4,"NA"],["Austin",30.3,-97.7,"NA"],
  ["Denver",39.7,-105.0,"NA"],["SaltLakeCity",40.8,-111.9,"NA"],["Phoenix",33.4,-112.1,"NA"],
  ["LasVegas",36.2,-115.1,"NA"],["LosAngeles",34.05,-118.2,"NA"],["SanJose",37.3,-121.9,"NA"],
  ["SanFrancisco",37.8,-122.4,"NA"],["Seattle",47.6,-122.3,"NA"],["Portland",45.5,-122.7,"NA"],
  ["Toronto",43.7,-79.4,"NA"],["Montreal",45.5,-73.6,"NA"],["Ottawa",45.4,-75.7,"NA"],
  ["Vancouver",49.3,-123.1,"NA"],["Calgary",51.0,-114.1,"NA"],["Winnipeg",49.9,-97.1,"NA"],
  ["Halifax",44.6,-63.6,"NA"],["Anchorage",61.2,-149.9,"NA"],["MexicoCity",19.4,-99.1,"NA"],
  ["Guadalajara",20.7,-103.3,"NA"],["Monterrey",25.7,-100.3,"NA"],["Queretaro",20.6,-100.4,"NA"],
  ["Tijuana",32.5,-117.0,"NA"],
  // ── 拉美 LA ────────────────────────────────────────────────────────────
  ["SaoPaulo",-23.55,-46.6,"LA"],["RioDeJaneiro",-22.9,-43.2,"LA"],["Brasilia",-15.8,-47.9,"LA"],
  ["PortoAlegre",-30.0,-51.2,"LA"],["Fortaleza",-3.7,-38.5,"LA"],["Recife",-8.05,-34.9,"LA"],
  ["BeloHorizonte",-19.9,-43.9,"LA"],["Manaus",-3.1,-60.0,"LA"],["BuenosAires",-34.6,-58.4,"LA"],
  ["Cordoba",-31.4,-64.2,"LA"],["Santiago",-33.45,-70.7,"LA"],["Valparaiso",-33.05,-71.6,"LA"],
  ["Lima",-12.05,-77.05,"LA"],["Bogota",4.7,-74.1,"LA"],["Medellin",6.25,-75.6,"LA"],
  ["Cali",3.45,-76.5,"LA"],["Quito",-0.2,-78.5,"LA"],["Guayaquil",-2.2,-79.9,"LA"],
  ["Caracas",10.5,-66.9,"LA"],["PanamaCity",8.98,-79.5,"LA"],["SanJoseCR",9.9,-84.1,"LA"],
  ["GuatemalaCity",14.6,-90.5,"LA"],["Havana",23.1,-82.4,"LA"],["SantoDomingo",18.5,-69.9,"LA"],
  ["SanJuan",18.5,-66.1,"LA"],["Montevideo",-34.9,-56.2,"LA"],["Asuncion",-25.3,-57.6,"LA"],
  ["LaPaz",-16.5,-68.1,"LA"],
  // ── 欧洲 EU ────────────────────────────────────────────────────────────
  ["London",51.5,-0.13,"EU"],["Manchester",53.5,-2.24,"EU"],["Dublin",53.35,-6.26,"EU"],
  ["Edinburgh",55.95,-3.19,"EU"],["Amsterdam",52.37,4.9,"EU"],["Rotterdam",51.92,4.48,"EU"],
  ["Brussels",50.85,4.35,"EU"],["Paris",48.86,2.35,"EU"],["Marseille",43.3,5.37,"EU"],
  ["Lyon",45.76,4.84,"EU"],["Frankfurt",50.11,8.68,"EU"],["Berlin",52.52,13.4,"EU"],
  ["Munich",48.14,11.58,"EU"],["Hamburg",53.55,10.0,"EU"],["Dusseldorf",51.23,6.78,"EU"],
  ["Zurich",47.37,8.54,"EU"],["Geneva",46.2,6.14,"EU"],["Vienna",48.21,16.37,"EU"],
  ["Prague",50.08,14.44,"EU"],["Warsaw",52.23,21.01,"EU"],["Krakow",50.06,19.94,"EU"],
  ["Budapest",47.5,19.04,"EU"],["Bucharest",44.43,26.1,"EU"],["Sofia",42.7,23.32,"EU"],
  ["Belgrade",44.8,20.46,"EU"],["Zagreb",45.81,15.98,"EU"],["Ljubljana",46.06,14.51,"EU"],
  ["Athens",37.98,23.73,"EU"],["Rome",41.9,12.5,"EU"],["Milan",45.46,9.19,"EU"],
  ["Naples",40.85,14.27,"EU"],["Madrid",40.42,-3.7,"EU"],["Barcelona",41.39,2.17,"EU"],
  ["Lisbon",38.72,-9.14,"EU"],["Copenhagen",55.68,12.57,"EU"],["Stockholm",59.33,18.07,"EU"],
  ["Oslo",59.91,10.75,"EU"],["Helsinki",60.17,24.94,"EU"],["Tallinn",59.44,24.75,"EU"],
  ["Riga",56.95,24.1,"EU"],["Vilnius",54.69,25.28,"EU"],["Moscow",55.75,37.62,"EU"],
  ["StPetersburg",59.93,30.34,"EU"],["Kyiv",50.45,30.52,"EU"],["Istanbul",41.01,28.98,"EU"],
  ["Ankara",39.93,32.86,"EU"],["Reykjavik",64.15,-21.94,"EU"],["Novosibirsk",55.03,82.92,"EU"],
  // ── 中东非洲 MEA ───────────────────────────────────────────────────────
  ["Dubai",25.2,55.27,"MEA"],["AbuDhabi",24.45,54.38,"MEA"],["Doha",25.29,51.53,"MEA"],
  ["Riyadh",24.71,46.68,"MEA"],["Jeddah",21.49,39.19,"MEA"],["KuwaitCity",29.38,47.99,"MEA"],
  ["Manama",26.23,50.59,"MEA"],["Muscat",23.6,58.55,"MEA"],["TelAviv",32.08,34.78,"MEA"],
  ["Amman",31.95,35.93,"MEA"],["Beirut",33.89,35.5,"MEA"],["Baghdad",33.31,44.36,"MEA"],
  ["Tehran",35.69,51.39,"MEA"],["Cairo",30.04,31.24,"MEA"],["Alexandria",31.2,29.92,"MEA"],
  ["Casablanca",33.57,-7.59,"MEA"],["Tunis",36.8,10.18,"MEA"],["Algiers",36.75,3.06,"MEA"],
  ["Tripoli",32.89,13.19,"MEA"],["Lagos",6.52,3.38,"MEA"],["Abuja",9.06,7.49,"MEA"],
  ["Accra",5.6,-0.19,"MEA"],["Abidjan",5.32,-4.03,"MEA"],["Dakar",14.72,-17.47,"MEA"],
  ["Nairobi",-1.29,36.82,"MEA"],["AddisAbaba",9.03,38.74,"MEA"],["Kampala",0.35,32.58,"MEA"],
  ["DarEsSalaam",-6.79,39.28,"MEA"],["Kinshasa",-4.44,15.27,"MEA"],["Luanda",-8.84,13.23,"MEA"],
  ["Johannesburg",-26.2,28.05,"MEA"],["CapeTown",-33.92,18.42,"MEA"],["Durban",-29.86,31.02,"MEA"],
  ["Maputo",-25.97,32.57,"MEA"],["Harare",-17.83,31.05,"MEA"],["Khartoum",15.5,32.56,"MEA"],
];

/* ── 骨干取道表（示意）：跨区长途优先，弧线才有「取道」的读法 ────────────── */
const ROUTE_NAMES = [
  ["Singapore","SanJose"],["Tokyo","LosAngeles"],["Frankfurt","Mumbai"],["London","NewYork"],
  ["HongKong","Sydney"],["SaoPaulo","Madrid"],["Dubai","Singapore"],["Seoul","Seattle"],
  ["Jakarta","Tokyo"],["Amsterdam","Ashburn"],["Mumbai","Singapore"],["Nairobi","Dubai"],
  ["Lagos","London"],["Santiago","Miami"],["Sydney","LosAngeles"],["Paris","Casablanca"],
  ["Moscow","Frankfurt"],["Bangkok","HongKong"],["HoChiMinh","Singapore"],["Johannesburg","Frankfurt"],
  ["Toronto","London"],["MexicoCity","Dallas"],["Istanbul","Frankfurt"],["TelAviv","Amsterdam"],
  ["Auckland","Sydney"],["Shanghai","Singapore"],["Bogota","Miami"],["Riyadh","Mumbai"],
  ["Manila","HongKong"],["Stockholm","Frankfurt"],
];
const idxOf = (n) => { const i = NODES.findIndex((x) => x[0] === n); if (i < 0) throw new Error("未知节点 " + n); return i; };
const ROUTES = ROUTE_NAMES.map(([a, b]) => [idxOf(a), idxOf(b)]);

/* ═══ 几何工具（poster 侧；与运行时逐字同算法） ══════════════════════════ */
const D2R = Math.PI / 180;
function ll2v(lat, lon, r = 1) {
  const p = lat * D2R, l = lon * D2R, c = Math.cos(p);
  return [c * Math.sin(l) * r, Math.sin(p) * r, c * Math.cos(l) * r];
}
function rotY(v, a) { const s = Math.sin(a), c = Math.cos(a); return [v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c]; }
function rotZ(v, a) { const s = Math.sin(a), c = Math.cos(a); return [v[0] * c - v[1] * s, v[0] * s + v[1] * c, v[2]]; }
const world = (v) => rotZ(rotY(v, Y0), TILT);

// 相机基（与 three lookAt 同构）
const nz = (v) => { const m = Math.hypot(...v); return [v[0] / m, v[1] / m, v[2] / m]; };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const ZA = nz(CAM), XA = nz(cross([0, 1, 0], ZA)), YA = cross(ZA, XA);
const CHAT = nz(CAM);

function project(p) {                       // 世界坐标 → 画布像素
  const d = [p[0] - CAM[0], p[1] - CAM[1], p[2] - CAM[2]];
  const vz = dot(d, ZA); if (vz > -0.05) return null;
  return [GCX + (FPX * dot(d, XA)) / -vz, GCY - (FPX * dot(d, YA)) / -vz];
}
const visible = (p) => dot(nz(p), CHAT) > 1 / CD;    // 球面点是否在朝前半球
const f1 = (n) => (Math.round(n * 10) / 10).toString();

/* ── poster：陆地点（抽稀）─────────────────────────────────────────────────
   抽稀必须用**确定性随机弃取**，不能用固定步长 —— 黄金角螺旋按固定 stride 取样
   会跟螺旋自己共振，屏幕上直接变成一片斜条纹摩尔纹（踩过一次，见 git 历史）。 */
function landPositions(keep) {
  const bin = Buffer.from(LAND.bits, "base64");
  const N = LAND.n, GA = Math.PI * (3 - Math.sqrt(5)), JIT = 0.35 * Math.sqrt((4 * Math.PI) / N);
  const out = [];
  for (let i = 0; i < N; i++) {
    if (!(bin[i >> 3] & (1 << (i & 7)))) continue;
    const hk = Math.sin((i + 7) * 127.1) * 43758.5453;
    if (hk - Math.floor(hk) >= keep) continue;
    const y = 1 - (2 * (i + 0.5)) / N, r = Math.sqrt(Math.max(0, 1 - y * y)), th = i * GA;
    let p = [Math.cos(th) * r, y, Math.sin(th) * r];
    // 确定性抖动：打散黄金角螺旋的摩尔纹（运行时逐字同式）
    const h1 = Math.sin((i + 1) * 12.9898) * 43758.5453, j1 = h1 - Math.floor(h1) - 0.5;
    const h2 = Math.sin((i + 1) * 78.233) * 24634.6345, j2 = h2 - Math.floor(h2) - 0.5;
    const ax = Math.abs(p[1]) > 0.95 ? [1, 0, 0] : [0, 1, 0];
    const t1 = nz(cross(p, ax)), t2 = cross(p, t1);
    p = nz([p[0] + JIT * (j1 * t1[0] + j2 * t2[0]), p[1] + JIT * (j1 * t1[1] + j2 * t2[1]), p[2] + JIT * (j1 * t1[2] + j2 * t2[2])]);
    out.push(p);
  }
  return out;
}

function dotsPath(pts, r) {
  let d = "";
  for (const p of pts) {
    const w = world([p[0] * r, p[1] * r, p[2] * r]);
    if (!visible(w)) continue;
    const s = project(w); if (!s) continue;
    d += `M${f1(s[0])} ${f1(s[1])}h.01`;
  }
  return d;
}

/* ── poster：经纬网 ─────────────────────────────────────────────────────── */
function graticulePath() {
  let d = "";
  const push = (pts) => {          // 只画可见段，遇到背面就断笔
    let open = false;
    for (const w of pts) {
      if (!visible(w)) { open = false; continue; }
      const s = project(w); if (!s) { open = false; continue; }
      d += (open ? "L" : "M") + f1(s[0]) + " " + f1(s[1]);
      open = true;
    }
  };
  for (let lon = -180; lon < 180; lon += 30) {
    const a = []; for (let lat = -88; lat <= 88; lat += 2) a.push(world(ll2v(lat, lon, 1.001)));
    push(a);
  }
  for (let lat = -60; lat <= 60; lat += 30) {
    const a = []; for (let lon = -180; lon <= 180; lon += 2) a.push(world(ll2v(lat, lon, 1.001)));
    push(a);
  }
  return d;
}

/* ── poster：节点 + 三条弧 ──────────────────────────────────────────────── */
function nodesPath() {
  let d = "";
  for (const [, lat, lon] of NODES) {
    const w = world(ll2v(lat, lon, 1.012));
    if (!visible(w)) continue;
    const s = project(w); if (!s) continue;
    d += `M${f1(s[0])} ${f1(s[1])}h.01`;
  }
  return d;
}
function arcPts(ia, ib, segs = 72) {
  const a = nz(ll2v(NODES[ia][1], NODES[ia][2])), b = nz(ll2v(NODES[ib][1], NODES[ib][2]));
  const om = Math.acos(Math.max(-1, Math.min(1, dot(a, b)))), so = Math.sin(om);
  const lift = 0.028 + 0.215 * (om / Math.PI);
  const out = [];
  for (let i = 0; i <= segs; i++) {
    const t = i / segs;
    let p = so < 1e-6 ? a.slice() : [0, 1, 2].map((k) => (a[k] * Math.sin((1 - t) * om) + b[k] * Math.sin(t * om)) / so);
    p = nz(p); const s = 1 + lift * Math.sin(Math.PI * t);
    out.push(world([p[0] * s, p[1] * s, p[2] * s]));
  }
  return out;
}
function posterArcs() {
  const picks = [];
  for (const [ia, ib] of ROUTES) {
    const wa = world(ll2v(NODES[ia][1], NODES[ia][2])), wb = world(ll2v(NODES[ib][1], NODES[ib][2]));
    if (visible(wa) && visible(wb)) picks.push([ia, ib]);
  }
  const chosen = [picks[0], picks[Math.floor(picks.length / 2)], picks[picks.length - 1]].filter(Boolean);
  return chosen.map(([ia, ib]) => {
    let d = "", open = false;
    for (const w of arcPts(ia, ib)) {
      if (!visible(w)) { open = false; continue; }
      const s = project(w); if (!s) { open = false; continue; }
      d += (open ? "L" : "M") + f1(s[0]) + " " + f1(s[1]); open = true;
    }
    return d;
  }).filter((d) => d.length > 24);
}

const POSTER = {
  land: dotsPath(landPositions(0.20), 1.004),
  grat: graticulePath(),
  nodes: nodesPath(),
  arcs: posterArcs(),
};

/* ═══ 页面 ═════════════════════════════════════════════════════════════════ */
const NODE_TABLE = NODES.map(([, lat, lon]) => `${lat},${lon}`).join(";");
const ROUTE_TABLE = ROUTES.map(([a, b]) => `${a},${b}`).join(";");

const HTML = `<!DOCTYPE html>
<html lang="zh-CN"><head>
<script>try{if(localStorage.getItem("colin-theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}<\/script>
<meta name="robots" content="noindex, nofollow"><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="/icon.svg">
<title>LAB · SD-RTN 全球实时网络地球</title>
<!-- three.js r${THREE_REV} · 自托管于 /decks/assets/three/ · 零外链
     构建： node scripts/build-lab-globe.mjs   自检： node scripts/shot-lab-globe.mjs -->
<style>
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-400.woff2') format('woff2');font-weight:400;font-display:swap;}
@font-face{font-family:'JetBrains Mono';src:url('/fonts/JetBrainsMono-500.woff2') format('woff2');font-weight:500;font-display:swap;}
</style>
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   THEME · colin-deck DUAL（base 家族取值 · 单文件双主题）
   :root = 浅底（默认） · html[data-theme="dark"] = 暗底
   --g-* 是这一页的地球材质层：**three.js 里一个色号都不写**，全部
   getComputedStyle 读这里；换主题时 MutationObserver 重读并热更新 uniform。
   ═══════════════════════════════════════════════════════════════════════════ */
:root{
  --stage-bg:#e2e3e8; --slide-bg:#eff0f3; --card-bg-2:#fffffe;
  --ink:#0d0d0d; --ink-2:#2a2a2a; --ink-3:#7a7a83;
  --accent:#ff8e3c; --accent-deep:#d9376e;
  --amber:var(--accent); --coral:var(--accent-deep);
  --hair:rgba(13,13,13,.16); --hair-soft:rgba(13,13,13,.075); --hair-strong:rgba(13,13,13,.30);
  --grid-line:rgba(13,13,13,.05);

  /* ── 地球 · 浅底 = 近黑线稿 + accent 节点（editorial）── */
  --g-ocean:#f6f6f9;   --g-shade:.22;
  --g-rim:var(--ink);  --g-rim-int:1;    --g-rim-pow:4.2;
  --g-land:var(--ink); --g-land-op:.92;  --g-land-size:.0048; --g-land-lit:.14;
  --g-grat:var(--ink); --g-grat-op:.13;
  --g-node:var(--accent);      --g-node-op:1;   --g-node-size:.0112;
  --g-halo:var(--accent);      --g-halo-op:.30; --g-halo-size:.030; --g-halo-add:0;
  --g-arc:var(--accent-deep);  --g-arc-op:.85;
  --g-head:var(--accent-deep); --g-head-op:.95; --g-head-size:.0128; --g-head-add:0;
  --g-atmo:var(--accent);      --g-atmo-int:.11;
  --g-poster-ocean:#f4f4f7;    --g-poster-op:1;
}
html[data-theme="dark"]{
  --stage-bg:#07070b; --slide-bg:#0f0e17; --card-bg-2:#16151f;
  --ink:#fffffe; --ink-2:#a7a9be; --ink-3:#6f7186;
  --accent:#ff8906; --accent-deep:#f25f4c;
  --hair:rgba(255,255,254,.10); --hair-soft:rgba(255,255,254,.055); --hair-strong:rgba(255,255,254,.20);
  --grid-line:rgba(255,255,254,.042);

  /* ── 地球 · 暗底 = 深空霓虹 ── */
  --g-ocean:#08070f;   --g-shade:.62;
  --g-rim:var(--accent); --g-rim-int:1;   --g-rim-pow:8.0;
  --g-land:var(--ink-3); --g-land-op:.92; --g-land-size:.0046; --g-land-lit:.58;
  --g-grat:var(--ink);   --g-grat-op:.075;
  --g-node:var(--accent);      --g-node-op:1;   --g-node-size:.0110;
  --g-halo:var(--accent);      --g-halo-op:.38; --g-halo-size:.038; --g-halo-add:1;
  --g-arc:var(--accent-deep);  --g-arc-op:.88;
  --g-head:var(--ink);         --g-head-op:1;   --g-head-size:.0130; --g-head-add:1;
  --g-atmo:var(--accent);      --g-atmo-int:.30;
  --g-poster-ocean:#08070f;    --g-poster-op:1;
}

*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:100%;height:100%;overflow:hidden;background:var(--stage-bg);}
:root{
  --f-cn:-apple-system,'Helvetica Neue',Arial,'PingFang SC','Noto Sans CJK SC','Source Han Sans SC','MiSans','HarmonyOS Sans SC','Microsoft YaHei',sans-serif;
  --f-mono:'JetBrains Mono','SF Mono',ui-monospace,'PingFang SC',monospace;
  --pad-x:120px; --pad-y:88px;
  --ease-flow:cubic-bezier(.22,.9,.24,1);
}

/* ── 固定 16:9 舞台（viewport-base 口径）───────────────────────────────── */
.deck-viewport{position:fixed;inset:0;overflow:hidden;background:var(--stage-bg);}
.deck-stage{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;
  transform-origin:0 0;background:var(--slide-bg);}
.slide{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;
  font-family:var(--f-cn);color:var(--ink);-webkit-font-smoothing:antialiased;}

/* 家族栏格：竖发丝线 */
.colgrid{position:absolute;inset:0;pointer-events:none;z-index:0;
  background-image:linear-gradient(90deg,var(--grid-line) 1px,transparent 1px);
  background-size:240px 100%;background-position:120px 0;}

/* ── 地球层 ─────────────────────────────────────────────────────────────── */
.globe-wrap{position:absolute;inset:0;z-index:1;}
/* 外辉光：垫在 poster / canvas 之下 —— 球体自己（不透明）挡掉内圈，只露出限界外那一圈。
   WebGL 路与 poster 路共用同一层，所以两条路的辉光逐像素一致；软渲染也省了一整屏片元。 */
.globe-atmo{position:absolute;border-radius:50%;pointer-events:none;
  left:${f1(GCX - GR * 1.35)}px; top:${f1(GCY - GR * 1.35)}px;
  width:${f1(GR * 2.7)}px; height:${f1(GR * 2.7)}px;
  background:radial-gradient(circle closest-side,transparent 62%,var(--g-atmo) 74%,transparent 87%);
  opacity:var(--g-atmo-int);}
.globe-canvas{position:absolute;left:0;top:0;width:1920px;height:1080px;display:block;
  opacity:0;transition:opacity .9s var(--ease-flow);}
.globe-canvas.up{opacity:1;}
.globe-poster{position:absolute;left:0;top:0;width:1920px;height:1080px;display:block;
  opacity:var(--g-poster-op);transition:opacity 1.1s var(--ease-flow);}
.globe-poster.down{opacity:0;}
.p-ocean{fill:var(--g-poster-ocean);}
.p-rim{fill:none;stroke:var(--g-rim);stroke-width:1.1;opacity:calc(var(--g-rim-int)*.55);}
.p-grat{fill:none;stroke:var(--g-grat);stroke-width:1;opacity:calc(var(--g-grat-op)*1.6);}
.p-land{fill:none;stroke:var(--g-land);stroke-width:2.6;stroke-linecap:round;opacity:calc(var(--g-land-op)*.9);}
.p-node{fill:none;stroke:var(--g-node);stroke-width:6;stroke-linecap:round;opacity:.92;}
.p-arc{fill:none;stroke:var(--g-arc);stroke-width:1.5;opacity:calc(var(--g-arc-op)*.85);}

/* ── 文字层 ─────────────────────────────────────────────────────────────── */
.copy{position:absolute;left:var(--pad-x);top:250px;width:760px;z-index:3;}
.kicker{font-family:var(--f-mono);font-size:17px;font-weight:500;letter-spacing:.28em;
  text-transform:uppercase;color:var(--accent);margin-bottom:34px;}
.tt{font-size:88px;font-weight:700;line-height:1.22;letter-spacing:-.022em;color:var(--ink);}
.dek{margin-top:36px;font-size:22px;line-height:1.92;font-weight:300;color:var(--ink-2);max-width:690px;}
.dek em{font-style:normal;color:var(--ink);font-weight:500;
  box-shadow:inset 0 -.52em 0 color-mix(in srgb,var(--accent) 26%,transparent);}
.legend{margin-top:52px;display:flex;gap:44px;align-items:center;}
.legend .it{display:flex;align-items:center;gap:12px;font-family:var(--f-mono);font-size:13px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3);}
.legend .sw{width:11px;height:11px;border-radius:50%;background:var(--accent);
  box-shadow:0 0 0 5px color-mix(in srgb,var(--accent) 20%,transparent);flex:none;}
.legend .ln{width:30px;height:0;border-top:1.6px solid var(--accent-deep);flex:none;}
.hairline{position:absolute;left:var(--pad-x);top:172px;width:760px;height:1px;
  background:var(--hair);z-index:3;}
.brand{position:absolute;left:var(--pad-x);top:var(--pad-y);z-index:3;font-family:var(--f-mono);
  font-size:14px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-3);}
.brand b{color:var(--ink);font-weight:500;}
.foot{position:absolute;right:var(--pad-x);bottom:var(--pad-y);z-index:3;text-align:right;
  font-family:var(--f-mono);font-size:14px;letter-spacing:.14em;color:var(--ink-3);}
.gnote{position:absolute;right:var(--pad-x);bottom:calc(var(--pad-y) + 34px);z-index:4;
  font-family:var(--f-mono);font-size:13px;letter-spacing:.12em;color:var(--accent-deep);text-align:right;}
.gnote[hidden]{display:none;}

/* ── lab chrome：FPS 探针 + 主题钮（都在舞台之外，跟着 viewport）────────── */
.lab-probe{position:fixed;left:26px;top:22px;z-index:1100;font-family:var(--f-mono);
  font-size:11px;letter-spacing:.13em;color:var(--ink-3);opacity:.62;
  display:flex;gap:9px;align-items:center;pointer-events:none;
  text-shadow:0 0 6px var(--stage-bg);}
.lab-probe .sep{opacity:.4;}
.lab-probe b{font-weight:500;color:var(--accent);}
.deck-swap{position:fixed;left:26px;bottom:24px;z-index:1100;font-family:var(--f-mono);font-size:12px;
  letter-spacing:.14em;color:var(--ink-3);border:1px solid var(--hair);border-radius:3px;padding:7px 12px;
  opacity:.62;transition:opacity .3s,color .3s,border-color .3s;background:var(--card-bg-2);cursor:pointer;}
.deck-swap:hover,.deck-swap:focus-visible{opacity:1;color:var(--accent);border-color:var(--accent);}
.deck-swap:focus:not(:focus-visible){outline:none;}

/* ── 降级 ───────────────────────────────────────────────────────────────── */
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
    transition-duration:.2s!important;}
}
@media print{
  html,body{width:1920px;height:auto;overflow:visible;background:#fff;}
  .deck-viewport{position:static;overflow:visible;background:#fff;}
  .deck-stage{position:static;transform:none!important;}
  .slide{position:relative;}
  .globe-canvas{display:none!important;}
  /* transition 也要掐掉：打印时机切过来还在做 1.1s 淡入，纸上就印了一张半透明的球 */
  .globe-poster{opacity:1!important;transition:none!important;}
  .lab-probe,.deck-swap{display:none!important;}
}
</style>
</head>
<body>
<div class="deck-viewport">
  <div class="deck-stage" id="stage">
    <div class="slide">
      <div class="colgrid"></div>

      <div class="globe-wrap">
        <div class="globe-atmo"></div>
        <!-- 降级层：静态 SVG 地球（同构图简化版，构建期用与 WebGL 逐字同参的
             相机矩阵离线投影而成 —— WebGL 起来前 / 起不来时它就是这一页的画面） -->
        <svg class="globe-poster" id="poster" viewBox="0 0 1920 1080" aria-hidden="true">
          <circle class="p-ocean" cx="${f1(GCX)}" cy="${f1(GCY)}" r="${f1(GR)}"/>
          <path class="p-grat" d="${POSTER.grat}"/>
          <path class="p-land" d="${POSTER.land}"/>
${POSTER.arcs.map((d) => `          <path class="p-arc" d="${d}"/>`).join("\n")}
          <path class="p-node" d="${POSTER.nodes}"/>
          <circle class="p-rim" cx="${f1(GCX)}" cy="${f1(GCY)}" r="${f1(GR)}"/>
        </svg>
        <canvas class="globe-canvas" id="gl" width="1920" height="1080"></canvas>
      </div>

      <div class="brand"><b>COLIN YAO</b> · LAB</div>
      <div class="hairline"></div>
      <div class="copy">
        <div class="kicker">LAB · THREE.JS SPIKE · SD-RTN GLOBE</div>
        <h1 class="tt">一张实时网络，<br>包住地球。</h1>
        <p class="dek">软件定义实时网：就近接入、动态选路、<em>毫秒级</em>抵达。
          屏幕上这颗球是示意图 —— 亮点是节点，弧是一次取道。</p>
        <div class="legend">
          <div class="it"><span class="sw"></span>节点 NODE</div>
          <div class="it"><span class="ln"></span>取道 ROUTE</div>
        </div>
      </div>
      <div class="foot">节点分布示意 · 200+ 全球节点 · SD-RTN</div>
      <div class="gnote" id="gnote" hidden>WEBGL 不可用 · 已回落到静态示意图</div>
    </div>
  </div>
</div>

<div class="lab-probe" id="probe">
  <span id="pFps">FPS <b>—</b></span><span class="sep">/</span>
  <span id="pDpr">DPR —</span><span class="sep">/</span>
  <span>THREE r${THREE_REV}</span><span class="sep">/</span>
  <span id="pMode">BOOT</span>
</div>
<button class="deck-swap" id="deckSwap">暗底</button>

<script>
/* 舞台等比适配 + 主题三段 + WebGL 看门狗（classic script，模块挂了也照跑） */
(function(){
  var stage=document.getElementById('stage');
  window.__stageScale=1;
  function fit(){
    var f=Math.min(window.innerWidth/1920,window.innerHeight/1080);
    var x=(window.innerWidth-1920*f)/2,y=(window.innerHeight-1080*f)/2;
    stage.style.transform='translate('+x+'px, '+y+'px) scale('+f+')';
    window.__stageScale=f;
    if(window.__onStageFit)window.__onStageFit(f);
  }
  fit();window.addEventListener('resize',fit);

  var b=document.getElementById('deckSwap');
  function apply(t){
    if(t==='dark'){document.documentElement.setAttribute('data-theme','dark');b.textContent='\\u6d45\\u5e95';}
    else{document.documentElement.removeAttribute('data-theme');b.textContent='\\u6697\\u5e95';}
  }
  var cur='light';try{cur=localStorage.getItem('colin-theme')||'light';}catch(e){}
  apply(cur);window.__setTheme=apply;
  b.addEventListener('click',function(){
    b.blur();
    var now=document.documentElement.getAttribute('data-theme')==='dark'?'dark':'light';
    var nxt=now==='dark'?'light':'dark';
    try{localStorage.setItem('colin-theme',nxt);}catch(e){}
    apply(nxt);
  });

  // 看门狗：6s 内 WebGL 没起来 ⇒ poster 常驻 + 一行小字
  setTimeout(function(){
    if(window.__globeUp)return;
    document.getElementById('gnote').hidden=false;
    var m=document.getElementById('pMode');if(m)m.textContent='POSTER';
    var f=document.getElementById('pFps');if(f)f.innerHTML='FPS <b>—</b>';
  },6000);
})();
<\/script>

<script type="importmap">
{"imports":{"three":"/decks/assets/three/three.module.min.js","three/addons/":"/decks/assets/three/"}}
<\/script>

<script type="module">
import * as THREE from 'three';
import { OrbitControls } from '/decks/assets/three/OrbitControls.js';

/* ═════════ 常量（与 build-lab-globe.mjs 的 poster 投影逐字同参） ═════════ */
const W=${W}, H=${H}, FOV=${FOV}, DX=${DX}, DY=${DY};
const CAM=[${CAM.join(",")}], TILT=${TILT}, Y0=${Y0.toFixed(6)}, SPIN=${SPIN};
const LAND_N=${LAND.n};
const LAND_BITS="${LAND.bits}";
const NODE_TABLE="${NODE_TABLE}";
const ROUTE_TABLE="${ROUTE_TABLE}";
/* 五槽弧：周期两两不整除 + 负起相位 ⇒ 任意时刻 3–5 条在飞，永不齐步 */
const ARC_DUR=[6.4,8.1,5.5,9.3,7.2,6.9], ARC_GAP=[1.9,1.2,2.6,1.5,2.1,1.7], ARC_OFF=[0,-2.3,-4.7,-1.1,-6.2,-3.6];
const SEG=128;                       // 每条弧的采样段数
const canvas=document.getElementById('gl');
const poster=document.getElementById('poster');
const gnote=document.getElementById('gnote');
const pFps=document.getElementById('pFps'), pDpr=document.getElementById('pDpr'), pMode=document.getElementById('pMode');

/* ═════════ 主题色：**JS 里一个色号都不写**，全部读 CSS 变量 ═════════════ */
const probe=document.createElement('span');
probe.style.cssText='position:absolute;left:-9999px;top:0';
document.body.appendChild(probe);
const _c=new THREE.Color();
function cssColor(name){
  // 让浏览器自己把 var() / color-mix() / 具名色归一成 rgb()，再进 three。
  // 变量取不到时不兜色号（这一页禁止写死色号）—— 留空即继承 body 的 --ink。
  probe.style.color='';
  const v=getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  if(v) probe.style.color=v;
  const m=getComputedStyle(probe).color.match(/[\\d.]+/g)||[128,128,128];
  return _c.setRGB(m[0]/255,m[1]/255,m[2]/255,THREE.SRGBColorSpace).clone();
}
function cssNum(name,dflt){
  const v=parseFloat(getComputedStyle(document.documentElement).getPropertyValue(name));
  return isFinite(v)?v:dflt;
}

/* ═════════ WebGL 能力检测 ═══════════════════════════════════════════════ */
function webglOK(){
  try{
    const c=document.createElement('canvas');
    return !!(c.getContext('webgl2')||c.getContext('webgl')||c.getContext('experimental-webgl'));
  }catch(e){return false;}
}
if(!webglOK()){ fallback('no-webgl'); }
else { try{ boot(); }catch(e){ console.warn('[lab-globe]',e); fallback('boot-fail'); } }

function fallback(why){
  gnote.hidden=false; pMode.textContent='POSTER';
  window.__globeUp=false;
  console.info('[lab-globe] poster 降级：'+why);
}

/* ═════════ 主流程 ═══════════════════════════════════════════════════════ */
function boot(){
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'high-performance'});
  renderer.setSize(W,H,false);
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(FOV,W/H,0.1,100);
  camera.position.set(CAM[0],CAM[1],CAM[2]);
  camera.lookAt(0,0,0);
  // 球心不在画面正中：setViewOffset 平移视锥 —— 纯平移，球的轮廓仍是正圆
  camera.setViewOffset(W,H,-DX,-DY,W,H);

  /* ── 共享 uniform ─────────────────────────────────────────────────── */
  const U={ uScale:{value:1}, uTime:{value:0} };

  /* DPR 上限 2；再乘舞台缩放，小窗口下不白烧像素 */
  function applyDPR(){
    const s=Math.min(1,window.__stageScale||1);
    const pr=Math.min(window.devicePixelRatio||1,2)*s;
    renderer.setPixelRatio(pr);
    renderer.setSize(W,H,false);
    U.uScale.value=(H*pr)/(2*Math.tan(FOV*Math.PI/360));
    pDpr.textContent='DPR '+(Math.round(pr*100)/100);
    return pr;
  }

  /* ── 层级：pivot(地轴倾角) → spin(自转) → 内容 ────────────────────── */
  const pivot=new THREE.Group(); pivot.rotation.z=TILT; scene.add(pivot);
  const spin=new THREE.Group(); spin.rotation.y=Y0; pivot.add(spin);

  /* ── ① 海球（遮挡体 + fresnel 塑形）────────────────────────────────── */
  const oceanU={
    uBase:{value:new THREE.Color()}, uRim:{value:new THREE.Color()},
    uRimInt:{value:.5}, uRimPow:{value:3}, uShade:{value:.3},
  };
  const ocean=new THREE.Mesh(
    new THREE.SphereGeometry(0.995,72,48),
    new THREE.ShaderMaterial({
      uniforms:oceanU,
      vertexShader:\`varying vec3 vN; varying vec3 vP;
        void main(){ vN=normalize(normalMatrix*normal);
          vec4 mv=modelViewMatrix*vec4(position,1.0); vP=mv.xyz;
          gl_Position=projectionMatrix*mv; }\`,
      fragmentShader:\`uniform vec3 uBase; uniform vec3 uRim;
        uniform float uRimInt; uniform float uRimPow; uniform float uShade;
        varying vec3 vN; varying vec3 vP;
        const vec3 L=vec3(-0.42,0.50,0.76);   // 视空间定光：球转、光不转，晨昏线不飘
        void main(){
          vec3 n=normalize(vN), v=normalize(-vP);
          float f=pow(clamp(1.0-max(dot(n,v),0.0),0.0,1.0),uRimPow);
          float d=max(dot(n,normalize(L)),0.0);
          vec3 c=uBase*(1.0-uShade+uShade*(0.30+0.70*d));
          c+=uRim*(f*uRimInt);
          gl_FragColor=vec4(c,1.0);
          #include <colorspace_fragment>
        }\`,
    })
  );
  spin.add(ocean);

  /* ── ③ 经纬网（30° 一格，很淡，只做「这是地图」的暗示）─────────────── */
  const gratU={ uColor:{value:new THREE.Color()}, uOpacity:{value:.1} };
  const gratMat=new THREE.LineBasicMaterial({transparent:true,depthWrite:false});
  const gratPts=[];
  const ll2v=(lat,lon,r)=>{const p=lat*Math.PI/180,l=lon*Math.PI/180,c=Math.cos(p);
    return new THREE.Vector3(c*Math.sin(l)*r,Math.sin(p)*r,c*Math.cos(l)*r);};
  for(let lon=-180;lon<180;lon+=30){
    let prev=null;
    for(let lat=-88;lat<=88;lat+=4){const v=ll2v(lat,lon,1.001);if(prev){gratPts.push(prev,v);}prev=v;}
  }
  for(let lat=-60;lat<=60;lat+=30){
    let prev=null;
    for(let lon=-180;lon<=180;lon+=4){const v=ll2v(lat,lon,1.001);if(prev){gratPts.push(prev,v);}prev=v;}
  }
  const grat=new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(gratPts),gratMat);
  spin.add(grat);

  /* ── ④ 陆地点云 ───────────────────────────────────────────────────── */
  // Fibonacci 球面点阵逐点复现（与 build-lab-globe-land.mjs 同式），
  // 位掩码只回答第 i 个候选点「是不是陆地」—— 所以数据里没有一个坐标。
  const bin=atob(LAND_BITS);
  const GA=Math.PI*(3-Math.sqrt(5));
  const JIT=0.35*Math.sqrt(4*Math.PI/LAND_N);
  const lp=[];
  const _p=new THREE.Vector3(),_t1=new THREE.Vector3(),_t2=new THREE.Vector3(),_ax=new THREE.Vector3();
  for(let i=0;i<LAND_N;i++){
    if(!(bin.charCodeAt(i>>3)&(1<<(i&7))))continue;
    const y=1-(2*(i+0.5))/LAND_N, r=Math.sqrt(Math.max(0,1-y*y)), th=i*GA;
    _p.set(Math.cos(th)*r,y,Math.sin(th)*r);
    const h1=Math.sin((i+1)*12.9898)*43758.5453, j1=h1-Math.floor(h1)-0.5;
    const h2=Math.sin((i+1)*78.233)*24634.6345,  j2=h2-Math.floor(h2)-0.5;
    _ax.set(0,1,0); if(Math.abs(_p.y)>0.95)_ax.set(1,0,0);
    _t1.crossVectors(_p,_ax).normalize(); _t2.crossVectors(_p,_t1);
    _p.addScaledVector(_t1,JIT*j1).addScaledVector(_t2,JIT*j2).normalize().multiplyScalar(1.004);
    lp.push(_p.x,_p.y,_p.z);
  }
  const LAND_COUNT=lp.length/3;

  /* 共用的「球面发光点」着色器：圆点 + 边缘淡出 + 受光 + 逐点相位脉冲 */
  const POINT_VS=\`
    uniform float uScale; uniform float uSize; uniform float uMinPx;
    uniform float uTime; uniform float uPulse; uniform float uLit;
    attribute float aPhase; attribute float aAlpha;
    varying float vFade; varying float vA;
    const vec3 L=vec3(-0.42,0.50,0.76);
    void main(){
      vec4 mv=modelViewMatrix*vec4(position,1.0);
      vec3 n=normalize(mat3(modelViewMatrix)*normalize(position));
      vec3 v=normalize(-mv.xyz);
      float facing=max(dot(n,v),0.0);
      float lit=mix(1.0-uLit,1.0,max(dot(n,normalize(L)),0.0));
      float pulse=1.0+uPulse*sin(uTime*1.7+aPhase);
      vFade=smoothstep(0.0,0.34,facing)*lit;
      vA=aAlpha;
      gl_Position=projectionMatrix*mv;
      gl_PointSize=max(uSize*pulse*uScale/max(-mv.z,0.001),uMinPx);
    }\`;
  const POINT_FS=\`
    uniform vec3 uColor; uniform float uOpacity; uniform float uSoft;
    varying float vFade; varying float vA;
    void main(){
      vec2 c=gl_PointCoord-0.5; float d=dot(c,c);
      if(d>0.25) discard;
      float a=uOpacity*vFade*vA*smoothstep(0.25,uSoft,d);
      if(a<0.004) discard;
      gl_FragColor=vec4(uColor,a);
      #include <colorspace_fragment>
    }\`;
  function pointMat(minPx,soft,blend){
    return new THREE.ShaderMaterial({
      uniforms:{ uScale:U.uScale, uTime:U.uTime,
        uSize:{value:.004}, uMinPx:{value:minPx}, uColor:{value:new THREE.Color()},
        uOpacity:{value:1}, uSoft:{value:soft}, uPulse:{value:0}, uLit:{value:0} },
      vertexShader:POINT_VS, fragmentShader:POINT_FS,
      transparent:true, depthWrite:false, blending:blend||THREE.NormalBlending,
    });
  }
  function attachAttrs(geo,count,phased){
    const ph=new Float32Array(count), al=new Float32Array(count);
    for(let i=0;i<count;i++){ ph[i]=phased?(i*2.399963)%6.2831853:0; al[i]=1; }
    geo.setAttribute('aPhase',new THREE.BufferAttribute(ph,1));
    geo.setAttribute('aAlpha',new THREE.BufferAttribute(al,1));
    return al;
  }

  const landGeo=new THREE.BufferGeometry();
  landGeo.setAttribute('position',new THREE.BufferAttribute(new Float32Array(lp),3));
  attachAttrs(landGeo,LAND_COUNT,false);
  const landMat=pointMat(1.05,.13);
  spin.add(new THREE.Points(landGeo,landMat));

  /* ── ⑤ 节点（~200 枚，示意分布）+ 光晕 ─────────────────────────────── */
  const nodeLL=NODE_TABLE.split(';').map(s=>s.split(',').map(Number));
  const NODE_COUNT=nodeLL.length;
  const npos=new Float32Array(NODE_COUNT*3);
  const nvec=[];
  nodeLL.forEach((ll,i)=>{ const v=ll2v(ll[0],ll[1],1.013);
    npos[i*3]=v.x;npos[i*3+1]=v.y;npos[i*3+2]=v.z; nvec.push(ll2v(ll[0],ll[1],1)); });
  const nodeGeo=new THREE.BufferGeometry();
  nodeGeo.setAttribute('position',new THREE.BufferAttribute(npos,3));
  const nodeAlpha=attachAttrs(nodeGeo,NODE_COUNT,true);
  const nodeMat=pointMat(1.7,.14);
  const haloGeo=new THREE.BufferGeometry();
  haloGeo.setAttribute('position',new THREE.BufferAttribute(npos,3));
  const haloAlpha=attachAttrs(haloGeo,NODE_COUNT,true);
  const haloMat=pointMat(3,.0,THREE.AdditiveBlending);
  spin.add(new THREE.Points(haloGeo,haloMat));
  spin.add(new THREE.Points(nodeGeo,nodeMat));

  /* ── ⑥ 飞包：五条并发大圆弧 + 沿弧飞行的小光点 ─────────────────────── */
  const routes=ROUTE_TABLE.split(';').map(s=>s.split(',').map(Number));
  const arcMat=new THREE.LineBasicMaterial({transparent:true,depthWrite:false});
  const slots=[];
  for(let s=0;s<ARC_DUR.length;s++){
    const g=new THREE.BufferGeometry();
    g.setAttribute('position',new THREE.BufferAttribute(new Float32Array((SEG+1)*3),3));
    const m=arcMat.clone();
    const line=new THREE.Line(g,m);
    line.frustumCulled=false;
    spin.add(line);
    slots.push({g,m,line,route:s%routes.length,pts:new Float32Array((SEG+1)*3),cycle:-1});
  }
  const headGeo=new THREE.BufferGeometry();
  headGeo.setAttribute('position',new THREE.BufferAttribute(new Float32Array(slots.length*3),3));
  const headAlpha=attachAttrs(headGeo,slots.length,false);
  const headMat=pointMat(2.2,.05,THREE.AdditiveBlending);
  const heads=new THREE.Points(headGeo,headMat);
  heads.frustumCulled=false;
  spin.add(heads);

  const _a=new THREE.Vector3(),_b=new THREE.Vector3(),_q=new THREE.Vector3();
  function buildArc(slot){
    const [ia,ib]=routes[slot.route];
    _a.copy(nvec[ia]); _b.copy(nvec[ib]);
    const om=Math.acos(Math.max(-1,Math.min(1,_a.dot(_b)))), so=Math.sin(om);
    const lift=0.028+0.215*(om/Math.PI);
    for(let i=0;i<=SEG;i++){
      const t=i/SEG;
      if(so<1e-6) _q.copy(_a);
      else _q.set(0,0,0).addScaledVector(_a,Math.sin((1-t)*om)/so).addScaledVector(_b,Math.sin(t*om)/so);
      _q.normalize().multiplyScalar(1+lift*Math.sin(Math.PI*t));
      slot.pts[i*3]=_q.x; slot.pts[i*3+1]=_q.y; slot.pts[i*3+2]=_q.z;
    }
    slot.g.attributes.position.array.set(slot.pts);
    slot.g.attributes.position.needsUpdate=true;
    slot.g.computeBoundingSphere();
    slot.dest=ib;
  }
  slots.forEach(buildArc);

  /* 节点抵达脉冲：光点飞到就给终点节点一记，衰减回去 */
  const pulseAmt=new Float32Array(NODE_COUNT);

  /* ═════════ 主题应用（启动 + 每次 data-theme 变化） ═════════════════ */
  let themeDark=false;
  const setBlend=(m,add)=>{
    const b=add>=.5?THREE.AdditiveBlending:THREE.NormalBlending;
    if(m.blending!==b){ m.blending=b; m.needsUpdate=true; }
  };
  function applyTheme(){
    themeDark=document.documentElement.getAttribute('data-theme')==='dark';
    oceanU.uBase.value.copy(cssColor('--g-ocean'));
    oceanU.uRim.value.copy(cssColor('--g-rim'));
    oceanU.uRimInt.value=cssNum('--g-rim-int',.5);
    oceanU.uRimPow.value=cssNum('--g-rim-pow',3);
    oceanU.uShade.value=cssNum('--g-shade',.3);

    gratMat.color.copy(cssColor('--g-grat'));
    gratMat.opacity=cssNum('--g-grat-op',.1);

    landMat.uniforms.uColor.value.copy(cssColor('--g-land'));
    landMat.uniforms.uOpacity.value=cssNum('--g-land-op',.8);
    landMat.uniforms.uSize.value=cssNum('--g-land-size',.004);
    landMat.uniforms.uLit.value=cssNum('--g-land-lit',.2);

    nodeMat.uniforms.uColor.value.copy(cssColor('--g-node'));
    nodeMat.uniforms.uOpacity.value=cssNum('--g-node-op',1);
    nodeMat.uniforms.uSize.value=cssNum('--g-node-size',.0105);
    nodeMat.uniforms.uPulse.value=.16;
    nodeMat.uniforms.uLit.value=.10;

    haloMat.uniforms.uColor.value.copy(cssColor('--g-halo'));
    haloMat.uniforms.uOpacity.value=cssNum('--g-halo-op',.24);
    haloMat.uniforms.uSize.value=cssNum('--g-halo-size',.032);
    haloMat.uniforms.uPulse.value=.22;
    setBlend(haloMat,cssNum('--g-halo-add',1));

    headMat.uniforms.uColor.value.copy(cssColor('--g-head'));
    headMat.uniforms.uOpacity.value=cssNum('--g-head-op',1);
    headMat.uniforms.uSize.value=cssNum('--g-head-size',.013);
    setBlend(headMat,cssNum('--g-head-add',1));

    const ac=cssColor('--g-arc'), ao=cssNum('--g-arc-op',.7);
    slots.forEach(s=>{ s.m.color.copy(ac); s.baseOp=ao; });
  }
  applyTheme();
  new MutationObserver(()=>{ applyTheme(); if(paused) draw(0); })
    .observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});

  /* ═════════ 交互 ═════════════════════════════════════════════════════ */
  const controls=new OrbitControls(camera,canvas);
  controls.enableDamping=true; controls.dampingFactor=.065;
  controls.enablePan=false; controls.rotateSpeed=.42;
  controls.enableZoom=true; controls.zoomSpeed=.5;
  controls.minDistance=3.6; controls.maxDistance=6.6;   // 永远进不到球里
  controls.minPolarAngle=.16; controls.maxPolarAngle=Math.PI-.16;
  let dragT=-1e9;
  controls.addEventListener('start',()=>{dragT=1e9;});
  controls.addEventListener('end',()=>{dragT=clock;});
  controls.addEventListener('change',()=>{ if(paused) draw(0); });

  /* ═════════ 循环 ═════════════════════════════════════════════════════ */
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused=false, raf=0, clock=0, last=0, frames=0, fpsT=0;
  const SPIN_W=(Math.PI*2)/SPIN;

  function step(slot,i,t){
    const period=ARC_DUR[i]+ARC_GAP[i];
    let tl=(t-ARC_OFF[i])%period; if(tl<0)tl+=period;
    const cyc=Math.floor((t-ARC_OFF[i])/period);
    if(cyc!==slot.cycle){                       // 换一条取道
      slot.cycle=cyc;
      slot.route=(((cyc*slots.length+i)%routes.length)+routes.length)%routes.length;
      buildArc(slot);
      slot.pinged=false;
    }
    if(tl>=ARC_DUR[i]){ slot.line.visible=false; headAlpha[i]=0; return; }
    const u=tl/ARC_DUR[i];
    const head=Math.min(1,u/0.62), tail=Math.max(0,(u-0.38)/0.62);
    const i0=Math.floor(tail*SEG), i1=Math.ceil(head*SEG);
    const cnt=Math.max(2,i1-i0+1);
    slot.line.visible=true;
    slot.g.setDrawRange(i0,Math.min(cnt,SEG+1-i0));
    const env=Math.min(1,u/0.06)*Math.min(1,(1-u)/0.12);
    slot.m.opacity=slot.baseOp*env;
    if(head<1){
      const hi=Math.min(SEG,Math.round(head*SEG));
      const hp=headGeo.attributes.position.array;
      hp[i*3]=slot.pts[hi*3]; hp[i*3+1]=slot.pts[hi*3+1]; hp[i*3+2]=slot.pts[hi*3+2];
      headAlpha[i]=env;
    }else{
      headAlpha[i]=0;
      if(!slot.pinged){ slot.pinged=true; pulseAmt[slot.dest]=1; }
    }
  }

  function draw(dt){
    clock+=dt;
    U.uTime.value=clock;
    // 拖拽时停转，松手 2.4s 后缓入恢复（不跟用户抢方向盘）
    let spinK=1;
    const since=clock-dragT;
    if(since<0) spinK=0;
    else if(since<2.4) spinK=0;
    else if(since<4.0) spinK=(since-2.4)/1.6;
    spin.rotation.y+=dt*SPIN_W*spinK;

    slots.forEach((s,i)=>step(s,i,clock));
    headGeo.attributes.position.needsUpdate=true;
    headGeo.attributes.aAlpha.needsUpdate=true;

    // 抵达脉冲衰减
    let any=false;
    for(let i=0;i<NODE_COUNT;i++){
      if(pulseAmt[i]>0.001){ pulseAmt[i]*=Math.pow(0.12,dt); any=true; }
      else pulseAmt[i]=0;
      nodeAlpha[i]=1+pulseAmt[i]*1.6;
      haloAlpha[i]=1+pulseAmt[i]*3.2;
    }
    if(any||clock<0.1){ nodeGeo.attributes.aAlpha.needsUpdate=true; haloGeo.attributes.aAlpha.needsUpdate=true; }

    controls.update();
    renderer.render(scene,camera);
  }

  function loop(ts){
    raf=requestAnimationFrame(loop);
    const dt=Math.min(0.05,last?(ts-last)/1000:0.016); last=ts;
    draw(dt);
    frames++;
    if(ts-fpsT>500){ pFps.innerHTML='FPS <b>'+Math.round(frames*1000/(ts-fpsT))+'</b>'; frames=0; fpsT=ts; }
  }
  function start(){
    if(reduced.matches){                        // 尊重系统设置：渲一帧就停帧
      paused=true; draw(0);
      pMode.textContent='STILL'; pFps.innerHTML='FPS <b>—</b>';
      return;
    }
    paused=false; last=0; fpsT=performance.now(); frames=0;
    if(!raf) raf=requestAnimationFrame(loop);
    pMode.textContent='LIVE';
  }
  function stop(){ if(raf){cancelAnimationFrame(raf); raf=0;} }
  reduced.addEventListener?.('change',()=>{ stop(); start(); });

  // 页面不可见就把 rAF 掐掉，回来续跑（时钟不跳）
  document.addEventListener('visibilitychange',()=>{
    if(document.hidden){ stop(); pMode.textContent='IDLE'; }
    else if(!paused){ last=0; start(); }
  });

  window.__onStageFit=()=>{ applyDPR(); if(paused) draw(0); };
  applyDPR();
  draw(0);                                       // 首帧：t=0，确定性
  requestAnimationFrame(()=>{
    canvas.classList.add('up');
    poster.classList.add('down');
    window.__globeUp=true;
    start();
  });
}
<\/script>
</body></html>
`;

const OUT = join(ROOT, "public/decks/lab-globe.html");
writeFileSync(OUT, HTML);
const kb = (n) => (n / 1024).toFixed(1) + "KB";
console.log(`写出 ${OUT}`);
console.log(`  整页            ${kb(Buffer.byteLength(HTML))}   （不含 /decks/assets/three/*）`);
console.log(`  陆地位掩码      ${kb(LAND.bits.length)}  land=${LAND.landCount}/${LAND.n}`);
console.log(`  poster SVG      ${kb(POSTER.land.length + POSTER.grat.length + POSTER.nodes.length + POSTER.arcs.join("").length)}`);
console.log(`  节点表          ${kb(NODE_TABLE.length)}  nodes=${NODES.length}  routes=${ROUTES.length}`);
console.log(`  球心/半径       (${f1(GCX)}, ${f1(GCY)})  R=${f1(GR)}`);
