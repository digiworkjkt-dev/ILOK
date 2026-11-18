import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const portalRoot = path.resolve(__dirname, "..");
const srcPath = path.resolve(portalRoot, "..", "data", "merged_lomba_kurasi.json");
const outDir = path.join(portalRoot, "src", "data");
const outPath = path.join(outDir, "lomba.json");

fs.mkdirSync(outDir, { recursive: true });

const raw = JSON.parse(fs.readFileSync(srcPath, "utf-8"));
const TODAY_STR = "2026-11-15";

function slugify(str) {
  return String(str || "penyelenggara")
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 72) || "penyelenggara";
}

function sanitizeUrl(u) {
  if (!u || typeof u !== "string") return "";
  const s = u.trim();
  if (/^https?:\/\//i.test(s)) {
    return s.replace(/^HTTP:\/\//, "http://").replace(/^HTTPS:\/\//, "https://");
  }
  return "";
}

function parseEndCmp(dstr) {
  if (!dstr || dstr === "-") return null;
  if (/^\d{4}-\d{2}-\d{2}$/.test(dstr.trim())) return dstr.trim();
  const m = dstr.trim().match(/^(\d{4})-(\d{2})$/);
  if (m) return `${m[1]}-${m[2]}-28`;
  return null;
}

const usedSlugs = new Set();
const STATUS_PRIORITY = {
  "Pendaftaran Dibuka": 1,
  "Sedang Berlangsung": 2,
  "Akan Datang (Terjadwal)": 3,
  "Estimasi Siklus Tahunan": 4,
  "Belum Ada Info Terbaru": 5,
};

function sanitizeNotes(txt) {
  if (!txt) return "";
  return txt
    .replace(/\bLembaga terdaftar di SIMT Kemendikdasmen\s*\/\s*Puspresnas\.?/gi, "Penyelenggara terverifikasi dalam daftar kurasi resmi.")
    .replace(/\bLembaga terdaftar di SIMT Puspresnas\.?/gi, "Penyelenggara terverifikasi dalam daftar kurasi resmi.")
    .replace(/\bterdaftar dan terkurasi SIMT Puspresnas/gi, "terkurasi secara resmi")
    .replace(/\bterkurasi di SIMT Puspresnas/gi, "terkurasi secara resmi")
    .replace(/\bterkurasi SIMT Puspresnas/gi, "terkurasi secara resmi")
    .replace(/\bterkurasi SIMT/gi, "terkurasi")
    .replace(/\bterkurasi Puspresnas/gi, "terkurasi resmi")
    .replace(/\bdalam kurasi Puspresnas/gi, "dalam daftar kurasi resmi")
    .replace(/\bBerdasarkan data SIMT,/gi, "Berdasarkan arsip kurasi sebelumnya,")
    .replace(/\bEdisi SIMT terakhir/gi, "Edisi terkurasi terakhir")
    .replace(/\btersertifikasi resmi Puspresnas Kemendikdasmen/gi, "tersertifikasi resmi")
    .replace(/\bbersama Puspresnas Kemendikdasmen/gi, "bersama mitra resmi")
    .replace(/\bPuspresnas Kemendikdasmen/gi, "lembaga kurasi resmi")
    .replace(/\bSIMT Puspresnas/gi, "daftar kurasi resmi")
    .replace(/\bSIMT\b/gi, "daftar kurasi")
    .replace(/\bPuspresnas\b/gi, "lembaga kurasi resmi")
    .replace(/\s{2,}/g, " ")
    .trim();
}

const items = raw.map((item, idx) => {
  let baseSlug = slugify(item.organizer);
  let slug = baseSlug;
  let counter = 2;
  while (usedSlugs.has(slug)) {
    slug = `${baseSlug}-${counter++}`;
  }
  usedSlugs.add(slug);

  const sRaw = (item.nearest_start_date || "-").trim();
  const eRaw = (item.nearest_end_date || "-").trim();
  const regRaw = (item.registration_deadline || "-").trim();

  const sortDate = item.sort_date || "9999-12-31";
  const endCmp = parseEndCmp(eRaw);
  let effectiveSort = sortDate;
  if (sortDate !== "9999-12-31" && sortDate < TODAY_STR) {
    if ((endCmp && endCmp >= TODAY_STR) || ["Pendaftaran Dibuka", "Sedang Berlangsung"].includes(item.schedule_status)) {
      effectiveSort = TODAY_STR;
    }
  }

  let regSort = "9999-12-31";
  if (/^\d{4}-\d{2}-\d{2}$/.test(regRaw)) regSort = regRaw;
  else if (/^\d{4}-\d{2}$/.test(regRaw)) {
    const [y, m] = regRaw.split("-").map(Number);
    const lastDay = String(new Date(Date.UTC(y, m, 0)).getUTCDate()).padStart(2, "0");
    regSort = `${regRaw}-${lastDay}`;
  }

  const simtComps = (item.simt_competitions || []).map((c) => ({
    name: c.name || "",
    short: c.short || "",
    rating: c.rating || 0,
    score: c.score ?? null,
    start: c.start || "-",
    end: c.end || "-",
    level: c.level || "-",
    cluster: c.cluster || "-",
    category: c.category || "-",
    link: sanitizeUrl(c.link || ""),
    branches: c.branches || [],
  }));

  const branchSet = [];
  for (const c of simtComps) {
    for (const b of c.branches) {
      if (b && !branchSet.includes(b)) branchSet.push(b);
      if (branchSet.length >= 6) break;
    }
    if (branchSet.length >= 6) break;
  }

  return {
    id: idx + 1,
    slug,
    org: item.organizer || "",
    orgShort: item.short_name || "",
    orgLink: sanitizeUrl(item.organizer_link || ""),
    country: item.country || "Indonesia",
    rating: item.max_rating || 3,
    avgScore: item.avg_score ?? null,
    branchesCnt: item.entries_count || 0,
    compsCnt: item.competitions_count || 0,
    topBranches: branchSet.slice(0, 4),
    clusters: item.clusters || [],
    levels: item.levels || [],
    sectors: item.sectors || [],
    latestSimt: item.latest_simt_start || "-",
    event: item.nearest_event_name || "-",
    status: item.schedule_status || "Belum Ada Info Terbaru",
    start: sRaw,
    end: eRaw,
    regDeadline: regRaw,
    effectiveSort,
    isExactStart: /^\d{4}-\d{2}-\d{2}$/.test(sRaw),
    regSort,
    jenjang: item.target_jenjang || "-",
    jenjangTags: item.jenjang_tags || ["Lainnya"],
    modeLokasi: item.mode_lokasi || "-",
    modeType: item.mode_type || "Belum Ditentukan",
    sourceUrl: sanitizeUrl(item.source_url || "") || sanitizeUrl(item.organizer_link || ""),
    notes: sanitizeNotes(item.notes || ""),
    simtComps,
  };
});

// Default sort: nearest execution date, then status priority, then rating desc
items.sort((a, b) => {
  if (a.effectiveSort !== b.effectiveSort) return a.effectiveSort.localeCompare(b.effectiveSort);
  const pa = STATUS_PRIORITY[a.status] || 9;
  const pb = STATUS_PRIORITY[b.status] || 9;
  if (pa !== pb) return pa - pb;
  if (b.rating !== a.rating) return b.rating - a.rating;
  return (b.avgScore || 0) - (a.avgScore || 0);
});

fs.writeFileSync(outPath, JSON.stringify(items, null, 2), "utf-8");
console.log(`Prepared ${items.length} organizers -> ${outPath}`);
