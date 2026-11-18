export interface SimtComp {
  name: string;
  short: string;
  rating: number;
  score: number | null;
  start: string;
  end: string;
  level: string;
  cluster: string;
  category: string;
  link: string;
  branches: string[];
}

export interface OrganizerItem {
  id: number;
  slug: string;
  org: string;
  orgShort: string;
  orgLink: string;
  country: string;
  rating: number;
  avgScore: number | null;
  branchesCnt: number;
  compsCnt: number;
  topBranches: string[];
  clusters: string[];
  levels: string[];
  sectors: string[];
  latestSimt: string;
  event: string;
  status: string;
  start: string;
  end: string;
  regDeadline: string;
  effectiveSort: string;
  isExactStart: boolean;
  regSort: string;
  jenjang: string;
  jenjangTags: string[];
  modeLokasi: string;
  modeType: string;
  sourceUrl: string;
  notes: string;
  simtComps: SimtComp[];
}

const MONTHS_ID = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"];
const MONTHS_FULL = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];

export function fmtDate(d: string, fullMonth = false): string {
  if (!d || d === "-") return "-";
  const mFull = d.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  const arr = fullMonth ? MONTHS_FULL : MONTHS_ID;
  if (mFull) {
    const mo = parseInt(mFull[2], 10);
    return `${parseInt(mFull[3], 10)} ${arr[mo] || mFull[2]} ${mFull[1]}`;
  }
  const mMon = d.match(/^(\d{4})-(\d{2})$/);
  if (mMon) {
    const mo = parseInt(mMon[2], 10);
    return `${arr[mo] || mMon[2]} ${mMon[1]}`;
  }
  return d;
}

export function daysFromRef(targetDate: string, refDate = "2026-11-15"): number | null {
  if (!targetDate || targetDate === "9999-12-31" || targetDate === "-") return null;
  const a = new Date(refDate + "T00:00:00Z");
  const b = new Date(targetDate + "T00:00:00Z");
  if (Number.isNaN(a.getTime()) || Number.isNaN(b.getTime())) return null;
  return Math.round((b.getTime() - a.getTime()) / 86400000);
}

export function countdownLabel(item: OrganizerItem): { text: string; tone: string } | null {
  if (!item.effectiveSort || item.effectiveSort === "9999-12-31") return null;
  if (item.effectiveSort === "2026-11-15") {
    return { text: "Aktif / Berlangsung", tone: "cd-now" };
  }
  const diff = daysFromRef(item.effectiveSort);
  if (diff === null) return null;
  if (diff >= 0 && diff <= 30) {
    return { text: `${item.isExactStart ? "" : "~"}${diff} hari lagi`, tone: "cd-soon" };
  }
  if (diff > 30 && diff <= 90) {
    return { text: `${item.isExactStart ? "" : "Est. "}${Math.round(diff / 30)} bulan lagi`, tone: "cd-mid" };
  }
  if (diff > 90) {
    return { text: `${item.isExactStart ? "" : "Est. "}${Math.round(diff / 30)} bulan lagi`, tone: "cd-far" };
  }
  return null;
}

export function statusClass(st: string): string {
  const map: Record<string, string> = {
    "Pendaftaran Dibuka": "st-open",
    "Sedang Berlangsung": "st-live",
    "Akan Datang (Terjadwal)": "st-sched",
    "Estimasi Siklus Tahunan": "st-est",
    "Belum Ada Info Terbaru": "st-none",
  };
  return map[st] || "st-none";
}

export function modeClass(mt: string): string {
  const map: Record<string, string> = {
    "Online / Daring": "b-mode-online",
    "Offline / Luring": "b-mode-offline",
    Hybrid: "b-mode-hybrid",
  };
  return map[mt] || "b-mode-unk";
}

export const EXPIRING_SOON_DAYS = 3;
export const ACTIVE_DEADLINE_STATUSES = [
  "Pendaftaran Dibuka",
  "Sedang Berlangsung",
  "Akan Datang (Terjadwal)",
];

export interface DeadlineCandidate {
  slug: string;
  event: string;
  org: string;
  jenjang: string;
  regDeadline: string;
  regSort: string;
  rating: number;
  status: string;
}

export interface UrgentDeadlineEntry extends DeadlineCandidate {
  daysLeft: number | null;
  expiringSoon: boolean;
}

/** Return today's date in YYYY-MM-DD for the given timezone (defaults to WIB / Asia/Jakarta). */
export function getTodayIso(timeZone = "Asia/Jakarta"): string {
  try {
    return new Intl.DateTimeFormat("en-CA", {
      timeZone,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }).format(new Date());
  } catch {
    const now = new Date();
    const pad = (n: number) => String(n).padStart(2, "0");
    return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  }
}

/** Format tooltip message for deadlines expiring within the attention window. */
export function expiringTitle(daysLeft: number | null): string | undefined {
  if (daysLeft === null || daysLeft < 0 || daysLeft > EXPIRING_SOON_DAYS) return undefined;
  return daysLeft === 0
    ? "Batas pendaftaran berakhir hari ini!"
    : `Segera berakhir (${daysLeft} hari lagi)`;
}

/** Filter out deadlines already past todayIso, sort nearest first, and mark entries expiring within EXPIRING_SOON_DAYS. */
export function getUrgentDeadlines(
  items: DeadlineCandidate[],
  todayIso: string,
  limit = 5
): UrgentDeadlineEntry[] {
  return items
    .filter(
      (x) =>
        x.regSort !== "9999-12-31" &&
        x.regSort >= todayIso &&
        ACTIVE_DEADLINE_STATUSES.includes(x.status)
    )
    .sort((a, b) => a.regSort.localeCompare(b.regSort) || b.rating - a.rating)
    .slice(0, limit)
    .map((x) => {
      const daysLeft = daysFromRef(x.regSort, todayIso);
      return {
        ...x,
        daysLeft,
        expiringSoon: daysLeft !== null && daysLeft >= 0 && daysLeft <= EXPIRING_SOON_DAYS,
      };
    });
}

export function starsText(n: number): { full: string; empty: string } {
  const clamped = Math.max(0, Math.min(5, n));
  return {
    full: "★".repeat(clamped),
    empty: "☆".repeat(5 - clamped),
  };
}
