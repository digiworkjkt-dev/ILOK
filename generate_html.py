import json
import os
import re
from datetime import date

DATA_DIR = r"D:\AI_LAB\Office\AJWA\lombakurasi\data"
OUT_HTML = r"D:\AI_LAB\Office\AJWA\lombakurasi\index.html"
TODAY = date(2026, 11, 15)
TODAY_STR = "2026-11-15"

with open(os.path.join(DATA_DIR, "merged_lomba_kurasi.json"), encoding="utf-8") as f:
    raw_data = json.load(f)


def sanitize_url(u):
    if not u or not isinstance(u, str):
        return ""
    u = u.strip()
    if u.lower().startswith("http://") or u.lower().startswith("https://"):
        if u.startswith("HTTP://"):
            return "http://" + u[7:]
        if u.startswith("HTTPS://"):
            return "https://" + u[8:]
        return u
    return ""


def parse_end_cmp(dstr):
    if not dstr or dstr == "-":
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", dstr.strip())
    if m:
        return dstr.strip()
    m2 = re.match(r"^(\d{4})-(\d{2})$", dstr.strip())
    if m2:
        return f"{m2.group(1)}-{m2.group(2)}-28"
    return None


records = []
total_simt_comps = 0
total_simt_branches = 0

for idx, item in enumerate(raw_data, start=1):
    total_simt_comps += item.get("competitions_count", 0)
    total_simt_branches += item.get("entries_count", 0)

    s_raw = (item.get("nearest_start_date") or "-").strip()
    e_raw = (item.get("nearest_end_date") or "-").strip()
    reg_raw = (item.get("registration_deadline") or "-").strip()

    sort_date = item.get("sort_date") or "9999-12-31"
    end_cmp = parse_end_cmp(e_raw)
    effective_sort = sort_date
    if sort_date != "9999-12-31" and sort_date < TODAY_STR:
        if end_cmp and end_cmp >= TODAY_STR:
            effective_sort = TODAY_STR
        elif item.get("schedule_status") in ("Pendaftaran Dibuka", "Sedang Berlangsung"):
            effective_sort = TODAY_STR

    is_exact_start = bool(re.match(r"^\d{4}-\d{2}-\d{2}$", s_raw))

    # Deadline sort key
    reg_sort = "9999-12-31"
    if re.match(r"^\d{4}-\d{2}-\d{2}$", reg_raw):
        reg_sort = reg_raw
    elif re.match(r"^\d{4}-\d{2}$", reg_raw):
        reg_sort = reg_raw + "-28"

    # Compact SIMT competitions list for modal
    simt_list = []
    for c in item.get("simt_competitions", []):
        simt_list.append({
            "n": c.get("name", ""),
            "sh": c.get("short") or "",
            "r": c.get("rating") or 0,
            "sc": c.get("score"),
            "st": c.get("start") or "-",
            "en": c.get("end") or "-",
            "lv": c.get("level") or "-",
            "cl": c.get("cluster") or "-",
            "ct": c.get("category") or "-",
            "lk": sanitize_url(c.get("link") or ""),
            "br": c.get("branches") or [],
        })

    records.append({
        "id": idx,
        "org": item.get("organizer", ""),
        "org_short": item.get("short_name") or "",
        "org_link": sanitize_url(item.get("organizer_link") or ""),
        "country": item.get("country") or "Indonesia",
        "rating": item.get("max_rating") or 3,
        "avg_score": item.get("avg_score"),
        "branches_cnt": item.get("entries_count") or 0,
        "comps_cnt": item.get("competitions_count") or 0,
        "clusters": item.get("clusters") or [],
        "levels": item.get("levels") or [],
        "sectors": item.get("sectors") or [],
        "latest_simt": item.get("latest_simt_start") or "-",
        "event": item.get("nearest_event_name") or "-",
        "status": item.get("schedule_status") or "Belum Ada Info Terbaru",
        "start": s_raw,
        "end": e_raw,
        "reg_deadline": reg_raw,
        "effective_sort": effective_sort,
        "is_exact_start": is_exact_start,
        "reg_sort": reg_sort,
        "jenjang": item.get("target_jenjang") or "-",
        "jenjang_tags": item.get("jenjang_tags") or ["Lainnya"],
        "mode_lokasi": item.get("mode_lokasi") or "-",
        "mode_type": item.get("mode_type") or "Belum Ditentukan",
        "source_url": sanitize_url(item.get("source_url") or "") or sanitize_url(item.get("organizer_link") or ""),
        "notes": item.get("notes") or "",
        "simt_comps": simt_list,
    })

data_json = json.dumps(records, ensure_ascii=False, separators=(",", ":"))

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kumpulan Lomba Terkurasi SIMT Bintang 3+ | Jadwal Terdekat (Nov 2026 - 2027)</title>
  <style>
    :root {
      --bg: #f4f7fb;
      --surface: #ffffff;
      --surface-2: #f8fafc;
      --border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #475569;
      --text-soft: #64748b;
      --primary: #104186;
      --primary-light: #eff6ff;
      --accent: #2563eb;
      --green-bg: #dcfce7;
      --green-fg: #166534;
      --blue-bg: #dbeafe;
      --blue-fg: #1e40af;
      --indigo-bg: #e0e7ff;
      --indigo-fg: #3730a3;
      --amber-bg: #fef3c7;
      --amber-fg: #92400e;
      --gray-bg: #f1f5f9;
      --gray-fg: #475569;
      --star: #f59e0b;
      --radius: 12px;
      --shadow: 0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.04);
      --shadow-lg: 0 20px 45px rgba(15, 23, 42, 0.18);
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      font-size: 14px;
    }

    .container {
      max-width: 1520px;
      margin: 0 auto;
      padding: 20px 24px 48px;
    }

    /* Hero Header */
    .hero {
      background: linear-gradient(135deg, #0c2d5e 0%, #104186 55%, #1d4ed8 100%);
      color: #fff;
      border-radius: 18px;
      padding: 26px 30px;
      box-shadow: var(--shadow);
      margin-bottom: 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 18px;
    }
    .hero h1 {
      margin: 0 0 6px;
      font-size: 23px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }
    .hero p {
      margin: 0;
      color: #dbeafe;
      font-size: 13.5px;
      max-width: 820px;
    }
    .hero-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }
    .hero-badge {
      background: rgba(255, 255, 255, 0.14);
      border: 1px solid rgba(255, 255, 255, 0.22);
      color: #fff;
      padding: 4px 11px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 500;
    }
    .hero-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 9px 15px;
      border-radius: 9px;
      border: 1px solid transparent;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      text-decoration: none;
      background: var(--surface);
      color: var(--text);
    }
    .btn-primary {
      background: #ffffff;
      color: var(--primary);
    }
    .btn-primary:hover { background: #eff6ff; }
    .btn-outline {
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.3);
      color: #fff;
    }
    .btn-outline:hover { background: rgba(255, 255, 255, 0.22); }
    .btn-sm {
      padding: 6px 11px;
      font-size: 12px;
      border-radius: 7px;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
    }
    .btn-sm:hover { background: var(--surface-2); border-color: #cbd5e1; }
    .btn-accent {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }
    .btn-accent:hover { background: #1d4ed8; }

    /* KPI Strip */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }
    .kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px 16px;
      box-shadow: var(--shadow);
      cursor: pointer;
      transition: transform 0.12s ease, border-color 0.12s ease;
      text-align: left;
    }
    .kpi-card:hover { transform: translateY(-1px); border-color: #93c5fd; }
    .kpi-card.active { border: 2px solid var(--accent); background: #f8fbff; }
    .kpi-label { font-size: 12px; color: var(--text-soft); font-weight: 600; margin-bottom: 4px; }
    .kpi-value { font-size: 24px; font-weight: 700; color: var(--text); line-height: 1.2; }
    .kpi-sub { font-size: 11.5px; color: var(--text-muted); margin-top: 3px; }

    /* Filter Panel */
    .filter-panel {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 18px;
      box-shadow: var(--shadow);
      margin-bottom: 16px;
    }
    .filter-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 10px;
    }
    .filter-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .filter-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(195px, 1fr));
      gap: 10px 12px;
    }
    .filter-item.span-2 {
      grid-column: span 2;
    }
    @media (max-width: 720px) {
      .filter-item.span-2 { grid-column: span 1; }
    }
    .filter-item label {
      display: block;
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 4px;
    }
    .filter-item input,
    .filter-item select {
      width: 100%;
      padding: 8px 10px;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      font-size: 13px;
      background: #fff;
      color: var(--text);
      outline: none;
    }
    .filter-item input:focus,
    .filter-item select:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
    }

    /* Toolbar */
    .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 10px;
    }
    .result-meta {
      font-size: 13px;
      color: var(--text-muted);
    }
    .result-meta strong { color: var(--text); }
    .toolbar-right {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    /* Table */
    .table-wrap {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 1180px;
    }
    thead th {
      background: #f8fafc;
      border-bottom: 2px solid var(--border);
      padding: 11px 12px;
      text-align: left;
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.03em;
      white-space: nowrap;
      user-select: none;
    }
    thead th.sortable { cursor: pointer; }
    thead th.sortable:hover { background: #eff6ff; color: var(--primary); }
    thead th .sort-ind { margin-left: 4px; font-size: 11px; color: #94a3b8; }
    thead th.sorted-asc .sort-ind,
    thead th.sorted-desc .sort-ind { color: var(--accent); }

    tbody tr {
      border-bottom: 1px solid var(--border);
      transition: background 0.1s ease;
    }
    tbody tr:hover { background: #f8fbff; }
    tbody td {
      padding: 12px 12px;
      vertical-align: top;
      font-size: 13px;
    }

    .col-no { width: 44px; color: var(--text-soft); font-weight: 600; text-align: center; }
    .col-rating { width: 125px; }
    .col-org { width: 220px; }
    .col-event { min-width: 280px; max-width: 380px; }
    .col-status { width: 150px; }
    .col-date { width: 165px; }
    .col-reg { width: 120px; }
    .col-jenjang { width: 185px; }
    .col-link { width: 105px; }

    .stars { color: var(--star); font-size: 14px; letter-spacing: 1px; white-space: nowrap; }
    .stars .dim { color: #cbd5e1; }
    .score-pill {
      display: inline-block;
      margin-top: 4px;
      padding: 2px 7px;
      border-radius: 6px;
      background: #f1f5f9;
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 600;
    }
    .org-name { font-weight: 700; color: var(--text); margin-bottom: 3px; }
    .org-sub { font-size: 11.5px; color: var(--text-soft); }
    .event-title { font-weight: 700; color: #0f172a; margin-bottom: 4px; }
    .event-notes {
      font-size: 12px;
      color: var(--text-muted);
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
      margin-bottom: 6px;
    }
    .badge-row { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
    .badge {
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 600;
      line-height: 1.4;
      white-space: nowrap;
    }
    .st-open { background: var(--green-bg); color: var(--green-fg); }
    .st-live { background: var(--blue-bg); color: var(--blue-fg); }
    .st-sched { background: var(--indigo-bg); color: var(--indigo-fg); }
    .st-est { background: var(--amber-bg); color: var(--amber-fg); }
    .st-none { background: var(--gray-bg); color: var(--gray-fg); }

    .b-cluster { background: #f1f5f9; color: #334155; }
    .b-level { background: #eff6ff; color: #1d4ed8; }
    .b-mode-online { background: #ecfeff; color: #0e7490; }
    .b-mode-offline { background: #fef2f2; color: #991b1b; }
    .b-mode-hybrid { background: #f5f3ff; color: #5b21b6; }
    .b-mode-unk { background: #f1f5f9; color: #64748b; }

    .date-main { font-weight: 700; color: var(--text); }
    .date-sub { font-size: 11.5px; color: var(--text-soft); margin-top: 2px; }
    .countdown-pill {
      display: inline-block;
      margin-top: 4px;
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }
    .cd-now { background: #dbeafe; color: #1e40af; }
    .cd-soon { background: #dcfce7; color: #166534; }
    .cd-mid { background: #fef3c7; color: #92400e; }
    .cd-far { background: #f1f5f9; color: #475569; }

    .link-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      color: var(--accent);
      text-decoration: none;
      font-weight: 600;
      font-size: 12px;
      margin-bottom: 4px;
    }
    .link-btn:hover { text-decoration: underline; }
    .detail-trigger {
      background: #eff6ff;
      color: #1d4ed8;
      border: 1px solid #bfdbfe;
      padding: 3px 9px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
    }
    .detail-trigger:hover { background: #dbeafe; }

    /* Pagination */
    .pagination {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      padding: 14px 16px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: none;
      border-radius: 0 0 var(--radius) var(--radius);
    }
    .page-btns { display: flex; gap: 5px; flex-wrap: wrap; }
    .page-btn {
      padding: 6px 11px;
      border-radius: 7px;
      border: 1px solid var(--border);
      background: #fff;
      cursor: pointer;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-muted);
    }
    .page-btn:hover:not(:disabled) { background: var(--surface-2); border-color: #94a3b8; }
    .page-btn.active { background: var(--primary); color: #fff; border-color: var(--primary); }
    .page-btn:disabled { opacity: 0.45; cursor: not-allowed; }

    /* Modal */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.55);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 18px;
      z-index: 1000;
    }
    .modal-backdrop.open { display: flex; }
    .modal {
      background: #fff;
      border-radius: 16px;
      max-width: 860px;
      width: 100%;
      max-height: 88vh;
      overflow-y: auto;
      box-shadow: var(--shadow-lg);
      padding: 24px 26px;
      position: relative;
    }
    .modal-close {
      position: sticky;
      top: 0;
      float: right;
      background: #f1f5f9;
      border: none;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      font-size: 18px;
      cursor: pointer;
      color: var(--text);
    }
    .modal-close:hover { background: #e2e8f0; }
    .modal h2 { margin: 0 0 6px; font-size: 19px; color: var(--primary); padding-right: 36px; }
    .modal-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      margin: 14px 0;
      background: var(--surface-2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 14px;
    }
    .mg-label { font-size: 11px; font-weight: 700; color: var(--text-soft); text-transform: uppercase; }
    .mg-val { font-size: 13px; font-weight: 600; color: var(--text); margin-top: 2px; }
    .simt-item {
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 11px 14px;
      margin-bottom: 8px;
      background: #fff;
    }
    .simt-item-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 10px;
      font-weight: 700;
      margin-bottom: 4px;
    }
    .branches-list {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 6px;
    }
    .empty-state {
      text-align: center;
      padding: 48px 20px;
      color: var(--text-soft);
    }
    .footer-note {
      margin-top: 18px;
      font-size: 12px;
      color: var(--text-soft);
      text-align: center;
    }
    @media print {
      .filter-panel, .hero-actions, .pagination, .detail-trigger { display: none !important; }
      body { background: #fff; }
      .table-wrap { border: none; box-shadow: none; }
    }
  </style>
</head>
<body>
<div class="container">
  <header class="hero">
    <div>
      <h1>Kumpulan Lomba Terkurasi SIMT (Bintang 3★ ke Atas)</h1>
      <p>
        Hasil scraping <strong>SIMT Kemendikdasmen</strong> (1.284 cabang &amp; 682 ajang terkurasi bintang 3–5 dari 292 penyelenggara)
        yang dilengkapi <strong>deep search</strong> jadwal pelaksanaan lomba terdekat berdasarkan waktu acuan <strong>15 November 2026</strong>.
      </p>
      <div class="hero-badges">
        <span class="hero-badge">📅 Acuan Waktu: 15 November 2026</span>
        <span class="hero-badge">⭐ Kriteria: Kurasi SIMT ≥ 3★</span>
        <span class="hero-badge">🏛️ 292 Penyelenggara Terkurasi</span>
        <span class="hero-badge">🏆 682 Ajang &amp; 1.284 Cabang</span>
      </div>
    </div>
    <div class="hero-actions">
      <a class="btn btn-outline" href="https://simt.kemendikdasmen.go.id/kurasi/advanced-search" target="_blank" rel="noopener">🔗 Buka SIMT Asli</a>
      <button class="btn btn-primary" onclick="exportCSV()">⬇️ Export CSV (Terfilter)</button>
    </div>
  </header>

  <section class="kpi-grid" id="kpiGrid"></section>

  <section class="filter-panel">
    <div class="filter-header">
      <div class="filter-title">🔍 Filter &amp; Sorting Data Lomba Terdekat</div>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="btn-sm" onclick="quickFilterUpcoming()">⚡ Hanya Yang Pasti &amp; Aktif (Nov 2026 – 2027)</button>
        <button class="btn-sm" onclick="resetFilters()">↺ Reset Semua Filter</button>
      </div>
    </div>
    <div class="filter-grid">
      <div class="filter-item span-2">
        <label for="fSearch">Cari Nama Lomba, Penyelenggara, Cabang SIMT, atau Catatan</label>
        <input id="fSearch" type="text" placeholder="Contoh: olimpiade matematika, robotik, IYSA, debat, basket..." oninput="applyFilters(true)" />
      </div>
      <div class="filter-item">
        <label for="fStatus">Status Jadwal</label>
        <select id="fStatus" onchange="applyFilters(true)">
          <option value="ALL">Semua Status</option>
          <option value="CONFIRMED_ACTIVE">Pasti &amp; Aktif (Dibuka + Berlangsung + Terjadwal)</option>
          <option value="Pendaftaran Dibuka">Pendaftaran Dibuka</option>
          <option value="Sedang Berlangsung">Sedang Berlangsung</option>
          <option value="Akan Datang (Terjadwal)">Akan Datang (Terjadwal)</option>
          <option value="Estimasi Siklus Tahunan">Estimasi Siklus Tahunan</option>
          <option value="Belum Ada Info Terbaru">Belum Ada Info Terbaru</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fTimeWindow">Rentang Waktu Terdekat</label>
        <select id="fTimeWindow" onchange="applyFilters(true)">
          <option value="ALL">Semua Waktu</option>
          <option value="ACTIVE_NOV">Aktif / Nov 2026</option>
          <option value="DEC_2026">Desember 2026</option>
          <option value="LATE_2026">Akhir 2026 (Nov – Des 2026)</option>
          <option value="Q1_2027">Kuartal 1 2027 (Jan – Mar 2027)</option>
          <option value="Q2_2027">Kuartal 2 2027 (Apr – Jun 2027)</option>
          <option value="H2_2027">Semester 2 2027 (Jul – Des 2027)</option>
          <option value="HAS_DEADLINE">Memiliki Batas Pendaftaran (Deadline)</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fRating">Hasil Kurasi SIMT (Bintang)</label>
        <select id="fRating" onchange="applyFilters(true)">
          <option value="ALL">Semua Bintang 3★ ke Atas (3★–5★)</option>
          <option value="5">5★ (Bintang 5 Saja)</option>
          <option value="4PLUS">4★ ke Atas (4★ &amp; 5★)</option>
          <option value="4">4★ Saja</option>
          <option value="3">3★ Saja</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fCluster">Klaster SIMT</label>
        <select id="fCluster" onchange="applyFilters(true)">
          <option value="ALL">Semua Klaster</option>
          <option value="Riset dan Inovasi">Riset dan Inovasi</option>
          <option value="Olahraga">Olahraga</option>
          <option value="Seni Budaya">Seni Budaya</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fLevel">Tingkat / Level</label>
        <select id="fLevel" onchange="applyFilters(true)">
          <option value="ALL">Semua Tingkat</option>
          <option value="Internasional">Internasional</option>
          <option value="Nasional">Nasional</option>
          <option value="Provinsi">Provinsi</option>
          <option value="Kabupaten/Kota">Kabupaten/Kota</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fJenjang">Jenjang Sasaran</label>
        <select id="fJenjang" onchange="applyFilters(true)">
          <option value="ALL">Semua Jenjang</option>
          <option value="SD/MI">SD / MI</option>
          <option value="SMP/MTs">SMP / MTs</option>
          <option value="SMA/SMK/MA">SMA / SMK / MA</option>
          <option value="Mahasiswa/DIKTI">Mahasiswa / DIKTI</option>
          <option value="Guru/Tendik">Guru / Tendik</option>
          <option value="Umum/Atlet">Umum / Atlet / Junior</option>
          <option value="PAUD/TK">PAUD / TK</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fMode">Mode Pelaksanaan</label>
        <select id="fMode" onchange="applyFilters(true)">
          <option value="ALL">Semua Mode</option>
          <option value="Online / Daring">Online / Daring</option>
          <option value="Offline / Luring">Offline / Luring</option>
          <option value="Hybrid">Hybrid (Daring + Luring)</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fCountry">Negara Penyelenggara</label>
        <select id="fCountry" onchange="applyFilters(true)">
          <option value="ALL">Semua Negara</option>
          <option value="ID">Indonesia</option>
          <option value="INTL">Luar Negeri</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="fSort">Urutkan Berdasarkan</label>
        <select id="fSort" onchange="applyFilters(true)">
          <option value="nearest_asc">Pelaksanaan Terdekat (Nov 2026 → 2027)</option>
          <option value="deadline_asc">Batas Pendaftaran Terdekat</option>
          <option value="rating_desc">Rating Tertinggi (5★ → 3★), lalu Terdekat</option>
          <option value="score_desc">Skor Kurasi SIMT Tertinggi</option>
          <option value="branches_desc">Cabang Terkurasi Terbanyak</option>
          <option value="org_asc">Nama Penyelenggara (A–Z)</option>
          <option value="event_asc">Nama Lomba Terdekat (A–Z)</option>
        </select>
      </div>
    </div>
  </section>

  <div class="toolbar">
    <div class="result-meta" id="resultMeta">Memuat data...</div>
    <div class="toolbar-right">
      <label for="fPerPage" style="font-size:12px;color:var(--text-muted);font-weight:600;">Tampilkan:</label>
      <select id="fPerPage" class="btn-sm" onchange="changePerPage()">
        <option value="25" selected>25 baris</option>
        <option value="50">50 baris</option>
        <option value="100">100 baris</option>
        <option value="9999">Semua</option>
      </select>
    </div>
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th class="col-no">No</th>
          <th class="col-rating sortable" data-sort="rating" onclick="toggleColSort('rating')">Kurasi SIMT <span class="sort-ind">⇅</span></th>
          <th class="col-org sortable" data-sort="org" onclick="toggleColSort('org')">Penyelenggara <span class="sort-ind">⇅</span></th>
          <th class="col-event sortable" data-sort="event" onclick="toggleColSort('event')">Lomba Terdekat &amp; Ringkasan <span class="sort-ind">⇅</span></th>
          <th class="col-status sortable" data-sort="status" onclick="toggleColSort('status')">Status Jadwal <span class="sort-ind">⇅</span></th>
          <th class="col-date sortable" data-sort="nearest" onclick="toggleColSort('nearest')">Pelaksanaan Terdekat <span class="sort-ind">▲</span></th>
          <th class="col-reg sortable" data-sort="deadline" onclick="toggleColSort('deadline')">Batas Daftar <span class="sort-ind">⇅</span></th>
          <th class="col-jenjang">Jenjang &amp; Mode</th>
          <th class="col-link">Tautan</th>
        </tr>
      </thead>
      <tbody id="tableBody"></tbody>
    </table>
  </div>
  <div class="pagination" id="paginationBar"></div>

  <p class="footer-note">
    Data sumber utama diambil dari API resmi SIMT Kemendikdasmen (<code>simt.kemendikdasmen.go.id/api/v2/list-kurasi</code>) dengan filter kurasi 3★–5★,
    kemudian diperkaya melalui crawling website penyelenggara dan deep search jadwal per 15 November 2026. Klik tombol <strong>Detail SIMT</strong> pada baris lomba untuk melihat seluruh daftar ajang dan cabang terkurasi milik penyelenggara tersebut.
  </p>
</div>

<!-- Detail Modal -->
<div class="modal-backdrop" id="detailModal" onclick="if(event.target===this) closeModal()">
  <div class="modal">
    <button class="modal-close" onclick="closeModal()" aria-label="Tutup">×</button>
    <div id="modalContent"></div>
  </div>
</div>

<script>
const TODAY_STR = "2026-11-15";
const DATA = __DATA_JSON__;

let filtered = [];
let currentPage = 1;
let perPage = 25;
let colSortState = { key: "nearest", dir: "asc" };

const MONTHS_ID = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"];

function esc(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function fmtDate(d) {
  if (!d || d === "-") return "-";
  const mFull = d.match(/^(\\d{4})-(\\d{2})-(\\d{2})$/);
  if (mFull) {
    const mo = parseInt(mFull[2], 10);
    return `${parseInt(mFull[3], 10)} ${MONTHS_ID[mo] || mFull[2]} ${mFull[1]}`;
  }
  const mMon = d.match(/^(\\d{4})-(\\d{2})$/);
  if (mMon) {
    const mo = parseInt(mMon[2], 10);
    return `${MONTHS_ID[mo] || mMon[2]} ${mMon[1]}`;
  }
  return d;
}

function daysBetween(aStr, bStr) {
  const a = new Date(aStr + "T00:00:00");
  const b = new Date(bStr + "T00:00:00");
  return Math.round((b - a) / 86400000);
}

function countdownBadge(r) {
  if (!r.effective_sort || r.effective_sort === "9999-12-31") return "";
  if (r.effective_sort === TODAY_STR) {
    return `<span class="countdown-pill cd-now">Aktif / Berlangsung</span>`;
  }
  const diff = daysBetween(TODAY_STR, r.effective_sort);
  if (diff >= 0 && diff <= 30) {
    return `<span class="countdown-pill cd-soon">${r.is_exact_start ? "" : "~"}${diff} hari lagi</span>`;
  }
  if (diff > 30 && diff <= 90) {
    return `<span class="countdown-pill cd-mid">${r.is_exact_start ? "" : "Est. "}${Math.round(diff/30)} bulan lagi</span>`;
  }
  if (diff > 90) {
    return `<span class="countdown-pill cd-far">${r.is_exact_start ? "" : "Est. "}${Math.round(diff/30)} bulan lagi</span>`;
  }
  return "";
}

function statusBadge(st) {
  const map = {
    "Pendaftaran Dibuka": "st-open",
    "Sedang Berlangsung": "st-live",
    "Akan Datang (Terjadwal)": "st-sched",
    "Estimasi Siklus Tahunan": "st-est",
    "Belum Ada Info Terbaru": "st-none"
  };
  return `<span class="badge ${map[st] || 'st-none'}">${esc(st)}</span>`;
}

function modeBadge(mt) {
  const map = {
    "Online / Daring": "b-mode-online",
    "Offline / Luring": "b-mode-offline",
    "Hybrid": "b-mode-hybrid"
  };
  return `<span class="badge ${map[mt] || 'b-mode-unk'}">${esc(mt)}</span>`;
}

function renderStars(n) {
  const full = "★".repeat(Math.max(0, Math.min(5, n)));
  const empty = "☆".repeat(Math.max(0, 5 - n));
  return `<span class="stars" title="Kurasi SIMT Bintang ${n}">${full}<span class="dim">${empty}</span></span>`;
}

function renderKPIs() {
  const total = DATA.length;
  const openCnt = DATA.filter(x => x.status === "Pendaftaran Dibuka").length;
  const liveCnt = DATA.filter(x => x.status === "Sedang Berlangsung").length;
  const schedCnt = DATA.filter(x => x.status === "Akan Datang (Terjadwal)").length;
  const estCnt = DATA.filter(x => x.status === "Estimasi Siklus Tahunan").length;
  const star45Cnt = DATA.filter(x => x.rating >= 4).length;

  const cards = [
    { id: "ALL", label: "Total Penyelenggara 3★+", val: total, sub: "__TOTAL_COMPS__ ajang • __TOTAL_BRANCHES__ cabang", action: "kpiFilter('ALL')" },
    { id: "OPEN", label: "Pendaftaran Dibuka", val: openCnt, sub: "Siap daftar per 15 Nov 2026", action: "kpiFilter('Pendaftaran Dibuka')" },
    { id: "LIVE", label: "Sedang Berlangsung", val: liveCnt, sub: "Aktif berjalan saat ini", action: "kpiFilter('Sedang Berlangsung')" },
    { id: "SCHED", label: "Akan Datang (Terjadwal)", val: schedCnt, sub: "Jadwal resmi telah rilis", action: "kpiFilter('Akan Datang (Terjadwal)')" },
    { id: "EST", label: "Estimasi Siklus Tahunan", val: estCnt, sub: "Berdasarkan pola edisi 2026", action: "kpiFilter('Estimasi Siklus Tahunan')" },
    { id: "STAR45", label: "Kurasi 4★ & 5★", val: star45Cnt, sub: "Peringkat kurasi tertinggi", action: "kpiFilterRating45()" },
  ];

  const curStatus = document.getElementById("fStatus").value;
  const curRating = document.getElementById("fRating").value;
  document.getElementById("kpiGrid").innerHTML = cards.map(c => {
    let active = false;
    if (c.id === "ALL" && curStatus === "ALL" && curRating === "ALL") active = true;
    if (c.id === "OPEN" && curStatus === "Pendaftaran Dibuka") active = true;
    if (c.id === "LIVE" && curStatus === "Sedang Berlangsung") active = true;
    if (c.id === "SCHED" && curStatus === "Akan Datang (Terjadwal)") active = true;
    if (c.id === "EST" && curStatus === "Estimasi Siklus Tahunan") active = true;
    if (c.id === "STAR45" && curRating === "4PLUS") active = true;
    return `
      <button class="kpi-card ${active ? 'active' : ''}" onclick="${c.action}">
        <div class="kpi-label">${c.label}</div>
        <div class="kpi-value">${c.val}</div>
        <div class="kpi-sub">${c.sub}</div>
      </button>
    `;
  }).join("");
}

function kpiFilter(st) {
  document.getElementById("fStatus").value = st;
  if (st === "ALL") document.getElementById("fRating").value = "ALL";
  applyFilters(true);
}

function kpiFilterRating45() {
  document.getElementById("fRating").value = "4PLUS";
  document.getElementById("fStatus").value = "ALL";
  applyFilters(true);
}

function quickFilterUpcoming() {
  document.getElementById("fStatus").value = "CONFIRMED_ACTIVE";
  document.getElementById("fSort").value = "nearest_asc";
  applyFilters(true);
}

function resetFilters() {
  document.getElementById("fSearch").value = "";
  document.getElementById("fStatus").value = "ALL";
  document.getElementById("fTimeWindow").value = "ALL";
  document.getElementById("fRating").value = "ALL";
  document.getElementById("fCluster").value = "ALL";
  document.getElementById("fLevel").value = "ALL";
  document.getElementById("fJenjang").value = "ALL";
  document.getElementById("fMode").value = "ALL";
  document.getElementById("fCountry").value = "ALL";
  document.getElementById("fSort").value = "nearest_asc";
  colSortState = { key: "nearest", dir: "asc" };
  applyFilters(true);
}

function matchTimeWindow(r, tw) {
  if (tw === "ALL") return true;
  if (tw === "HAS_DEADLINE") return r.reg_deadline && r.reg_deadline !== "-";
  const es = r.effective_sort || "9999-12-31";
  const st = r.start || "-";
  if (tw === "ACTIVE_NOV") return es >= "2026-11-15" && es <= "2026-11-30";
  if (tw === "DEC_2026") return st.startsWith("2026-12") || (es >= "2026-12-01" && es <= "2026-12-31");
  if (tw === "LATE_2026") return es >= "2026-11-15" && es <= "2026-12-31";
  if (tw === "Q1_2027") return es >= "2027-01-01" && es <= "2027-03-31";
  if (tw === "Q2_2027") return es >= "2027-04-01" && es <= "2027-06-30";
  if (tw === "H2_2027") return es >= "2027-07-01" && es <= "2027-12-31";
  return true;
}

const STATUS_PRIORITY = {
  "Pendaftaran Dibuka": 1,
  "Sedang Berlangsung": 2,
  "Akan Datang (Terjadwal)": 3,
  "Estimasi Siklus Tahunan": 4,
  "Belum Ada Info Terbaru": 5
};

function sortFiltered(sortKey) {
  filtered.sort((a, b) => {
    if (sortKey === "nearest_asc") {
      if (a.effective_sort !== b.effective_sort) return a.effective_sort.localeCompare(b.effective_sort);
      const pa = STATUS_PRIORITY[a.status] || 9;
      const pb = STATUS_PRIORITY[b.status] || 9;
      if (pa !== pb) return pa - pb;
      if (b.rating !== a.rating) return b.rating - a.rating;
      return (b.avg_score || 0) - (a.avg_score || 0);
    }
    if (sortKey === "nearest_desc") {
      if (a.effective_sort === "9999-12-31") return 1;
      if (b.effective_sort === "9999-12-31") return -1;
      return b.effective_sort.localeCompare(a.effective_sort);
    }
    if (sortKey === "deadline_asc") {
      if (a.reg_sort !== b.reg_sort) return a.reg_sort.localeCompare(b.reg_sort);
      return a.effective_sort.localeCompare(b.effective_sort);
    }
    if (sortKey === "deadline_desc") {
      if (a.reg_sort === "9999-12-31") return 1;
      if (b.reg_sort === "9999-12-31") return -1;
      return b.reg_sort.localeCompare(a.reg_sort);
    }
    if (sortKey === "rating_desc") {
      if (b.rating !== a.rating) return b.rating - a.rating;
      if (a.effective_sort !== b.effective_sort) return a.effective_sort.localeCompare(b.effective_sort);
      return (b.avg_score || 0) - (a.avg_score || 0);
    }
    if (sortKey === "rating_asc") {
      if (a.rating !== b.rating) return a.rating - b.rating;
      return (a.avg_score || 0) - (b.avg_score || 0);
    }
    if (sortKey === "score_desc") {
      return (b.avg_score || 0) - (a.avg_score || 0);
    }
    if (sortKey === "branches_desc") {
      return b.branches_cnt - a.branches_cnt;
    }
    if (sortKey === "org_asc") {
      return a.org.localeCompare(b.org, "id");
    }
    if (sortKey === "org_desc") {
      return b.org.localeCompare(a.org, "id");
    }
    if (sortKey === "event_asc") {
      return a.event.localeCompare(b.event, "id");
    }
    if (sortKey === "event_desc") {
      return b.event.localeCompare(a.event, "id");
    }
    if (sortKey === "status_asc") {
      return (STATUS_PRIORITY[a.status] || 9) - (STATUS_PRIORITY[b.status] || 9);
    }
    if (sortKey === "status_desc") {
      return (STATUS_PRIORITY[b.status] || 9) - (STATUS_PRIORITY[a.status] || 9);
    }
    return 0;
  });
}

function toggleColSort(key) {
  if (colSortState.key === key) {
    colSortState.dir = colSortState.dir === "asc" ? "desc" : "asc";
  } else {
    colSortState.key = key;
    colSortState.dir = (key === "rating") ? "desc" : "asc";
  }
  const map = {
    "nearest": colSortState.dir === "asc" ? "nearest_asc" : "nearest_desc",
    "deadline": colSortState.dir === "asc" ? "deadline_asc" : "deadline_desc",
    "rating": colSortState.dir === "desc" ? "rating_desc" : "rating_asc",
    "org": colSortState.dir === "asc" ? "org_asc" : "org_desc",
    "event": colSortState.dir === "asc" ? "event_asc" : "event_desc",
    "status": colSortState.dir === "asc" ? "status_asc" : "status_desc",
  };
  const sel = document.getElementById("fSort");
  if ([...sel.options].some(o => o.value === map[key])) {
    sel.value = map[key];
  }
  updateHeaderIndicators();
  sortFiltered(map[key]);
  currentPage = 1;
  renderTable();
}

function updateHeaderIndicators() {
  document.querySelectorAll("thead th.sortable").forEach(th => {
    th.classList.remove("sorted-asc", "sorted-desc");
    const ind = th.querySelector(".sort-ind");
    if (th.dataset.sort === colSortState.key) {
      th.classList.add(colSortState.dir === "asc" ? "sorted-asc" : "sorted-desc");
      ind.textContent = colSortState.dir === "asc" ? "▲" : "▼";
    } else {
      ind.textContent = "⇅";
    }
  });
}

function applyFilters(resetPage) {
  if (resetPage) currentPage = 1;
  const q = document.getElementById("fSearch").value.trim().toLowerCase();
  const st = document.getElementById("fStatus").value;
  const tw = document.getElementById("fTimeWindow").value;
  const rt = document.getElementById("fRating").value;
  const cl = document.getElementById("fCluster").value;
  const lv = document.getElementById("fLevel").value;
  const jj = document.getElementById("fJenjang").value;
  const md = document.getElementById("fMode").value;
  const cn = document.getElementById("fCountry").value;
  const sk = document.getElementById("fSort").value;

  filtered = DATA.filter(r => {
    if (st === "CONFIRMED_ACTIVE") {
      if (!["Pendaftaran Dibuka", "Sedang Berlangsung", "Akan Datang (Terjadwal)"].includes(r.status)) return false;
    } else if (st !== "ALL" && r.status !== st) {
      return false;
    }
    if (!matchTimeWindow(r, tw)) return false;

    if (rt === "5" && r.rating !== 5) return false;
    if (rt === "4PLUS" && r.rating < 4) return false;
    if (rt === "4" && r.rating !== 4) return false;
    if (rt === "3" && r.rating !== 3) return false;

    if (cl !== "ALL" && !r.clusters.includes(cl)) return false;
    if (lv !== "ALL" && !r.levels.includes(lv)) return false;
    if (jj !== "ALL" && !r.jenjang_tags.includes(jj)) return false;
    if (md !== "ALL" && r.mode_type !== md) return false;

    if (cn === "ID" && r.country !== "Indonesia") return false;
    if (cn === "INTL" && r.country === "Indonesia") return false;

    if (q) {
      const hay = [
        r.org, r.org_short, r.event, r.notes, r.jenjang, r.mode_lokasi,
        ...r.clusters, ...r.levels, ...r.sectors,
        ...r.simt_comps.map(c => c.n + " " + c.sh + " " + c.br.join(" "))
      ].join(" ").toLowerCase();
      const tokens = q.split(/\\s+/).filter(Boolean);
      for (const tok of tokens) {
        if (!hay.includes(tok)) return false;
      }
    }
    return true;
  });

  sortFiltered(sk);
  renderKPIs();
  renderTable();
}

function changePerPage() {
  perPage = parseInt(document.getElementById("fPerPage").value, 10) || 25;
  currentPage = 1;
  renderTable();
}

function renderTable() {
  const tbody = document.getElementById("tableBody");
  const total = filtered.length;
  const totalPages = Math.max(1, Math.ceil(total / perPage));
  if (currentPage > totalPages) currentPage = totalPages;

  const startIdx = (currentPage - 1) * perPage;
  const pageRows = filtered.slice(startIdx, startIdx + perPage);

  document.getElementById("resultMeta").innerHTML =
    total === 0
      ? "Tidak ada data yang cocok dengan filter saat ini."
      : `Menampilkan <strong>${startIdx + 1}–${Math.min(startIdx + perPage, total)}</strong> dari <strong>${total}</strong> penyelenggara terkurasi (total 292 penyelenggara).`;

  if (pageRows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-state">Tidak ditemukan lomba yang sesuai kriteria filter. Coba klik <strong>Reset Semua Filter</strong>.</td></tr>`;
    document.getElementById("paginationBar").innerHTML = "";
    return;
  }

  tbody.innerHTML = pageRows.map((r, i) => {
    const no = startIdx + i + 1;
    const dateDisp = r.start === "-"
      ? `<span class="date-main">-</span>`
      : `<span class="date-main">${r.is_exact_start ? "" : "Est. "}${esc(fmtDate(r.start))}</span>`
        + (r.end && r.end !== "-" && r.end !== r.start ? `<div class="date-sub">s.d. ${esc(fmtDate(r.end))}</div>` : "");

    const deadlineDisp = r.reg_deadline && r.reg_deadline !== "-"
      ? `<span class="date-main" style="color:#b91c1c;">${esc(fmtDate(r.reg_deadline))}</span>`
      : `<span class="date-sub">-</span>`;

    const clustersHtml = r.clusters.map(c => `<span class="badge b-cluster">${esc(c)}</span>`).join("");
    const levelsHtml = r.levels.map(l => `<span class="badge b-level">${esc(l)}</span>`).join("");

    return `
      <tr>
        <td class="col-no">${no}</td>
        <td class="col-rating">
          ${renderStars(r.rating)}
          <div class="score-pill">${r.avg_score !== null ? "Skor " + r.avg_score : r.rating + "★"} • ${r.branches_cnt} cbg</div>
          <div class="org-sub" style="margin-top:3px;">${r.comps_cnt} ajang SIMT</div>
        </td>
        <td class="col-org">
          <div class="org-name">${esc(r.org)}</div>
          <div class="org-sub">${r.org_short ? esc(r.org_short) + " • " : ""}${esc(r.country)}</div>
          ${r.org_link ? `<a class="link-btn" style="margin-top:4px;" href="${esc(r.org_link)}" target="_blank" rel="noopener">🌐 Web Penyelenggara</a>` : ""}
        </td>
        <td class="col-event">
          <div class="event-title">${esc(r.event)}</div>
          <div class="event-notes" title="${esc(r.notes)}">${esc(r.notes)}</div>
          <div class="badge-row">${clustersHtml}${levelsHtml}</div>
          <div style="margin-top:6px;">
            <button class="detail-trigger" onclick="openModal(${r.id})">📋 Detail &amp; ${r.comps_cnt} Ajang SIMT</button>
          </div>
        </td>
        <td class="col-status">
          ${statusBadge(r.status)}
          <div class="date-sub" style="margin-top:5px;">SIMT terakhir: ${esc(r.latest_simt)}</div>
        </td>
        <td class="col-date">
          ${dateDisp}
          <div>${countdownBadge(r)}</div>
        </td>
        <td class="col-reg">${deadlineDisp}</td>
        <td class="col-jenjang">
          <div style="margin-bottom:4px;">${modeBadge(r.mode_type)}</div>
          <div class="org-sub" style="margin-bottom:3px;"><strong>Jenjang:</strong> ${esc(r.jenjang)}</div>
          <div class="org-sub"><strong>Lokasi:</strong> ${esc(r.mode_lokasi)}</div>
        </td>
        <td class="col-link">
          ${r.source_url ? `<a class="link-btn" href="${esc(r.source_url)}" target="_blank" rel="noopener">🔗 Info Jadwal</a>` : "-"}
        </td>
      </tr>
    `;
  }).join("");

  renderPagination(total, totalPages);
}

function renderPagination(total, totalPages) {
  const bar = document.getElementById("paginationBar");
  if (totalPages <= 1) {
    bar.innerHTML = `<div class="result-meta">Total ${total} penyelenggara ditampilkan.</div><div></div>`;
    return;
  }
  let btns = [];
  btns.push(`<button class="page-btn" ${currentPage===1?'disabled':''} onclick="goPage(1)">«</button>`);
  btns.push(`<button class="page-btn" ${currentPage===1?'disabled':''} onclick="goPage(${currentPage-1})">‹ Prev</button>`);

  let startP = Math.max(1, currentPage - 2);
  let endP = Math.min(totalPages, currentPage + 2);
  for (let p = startP; p <= endP; p++) {
    btns.push(`<button class="page-btn ${p===currentPage?'active':''}" onclick="goPage(${p})">${p}</button>`);
  }
  btns.push(`<button class="page-btn" ${currentPage===totalPages?'disabled':''} onclick="goPage(${currentPage+1})">Next ›</button>`);
  btns.push(`<button class="page-btn" ${currentPage===totalPages?'disabled':''} onclick="goPage(${totalPages})">»</button>`);

  bar.innerHTML = `
    <div class="result-meta">Halaman <strong>${currentPage}</strong> dari <strong>${totalPages}</strong></div>
    <div class="page-btns">${btns.join("")}</div>
  `;
}

function goPage(p) {
  currentPage = p;
  renderTable();
  window.scrollTo({ top: 220, behavior: "smooth" });
}

function openModal(id) {
  const r = DATA.find(x => x.id === id);
  if (!r) return;
  const simtHtml = r.simt_comps.map(c => `
    <div class="simt-item">
      <div class="simt-item-head">
        <div>${esc(c.n)} ${c.sh ? `(${esc(c.sh)})` : ""}</div>
        <div>${renderStars(c.r)} <span class="score-pill">${c.sc !== null ? c.sc : ""}</span></div>
      </div>
      <div class="org-sub">
        Klaster: <strong>${esc(c.cl)}</strong> • Level: <strong>${esc(c.lv)}</strong> • Kategori: ${esc(c.ct)} • Jadwal SIMT: <strong>${esc(c.st)} s.d. ${esc(c.en)}</strong>
        ${c.lk ? ` • <a href="${esc(c.lk)}" target="_blank" rel="noopener">Link Ajang</a>` : ""}
      </div>
      <div class="branches-list"><strong>Cabang (${c.br.length}):</strong> ${esc(c.br.join(", "))}</div>
    </div>
  `).join("");

  document.getElementById("modalContent").innerHTML = `
    <h2>${esc(r.event !== "-" ? r.event : r.org)}</h2>
    <div class="org-sub" style="font-size:13px; margin-bottom:10px;">
      Penyelenggara: <strong>${esc(r.org)}</strong> (${esc(r.country)}) • Kurasi Maks: ${renderStars(r.rating)}
    </div>
    <div class="modal-grid">
      <div><div class="mg-label">Status Jadwal</div><div class="mg-val">${statusBadge(r.status)}</div></div>
      <div><div class="mg-label">Pelaksanaan Terdekat</div><div class="mg-val">${esc(fmtDate(r.start))} s.d. ${esc(fmtDate(r.end))}</div></div>
      <div><div class="mg-label">Batas Pendaftaran</div><div class="mg-val">${esc(fmtDate(r.reg_deadline))}</div></div>
      <div><div class="mg-label">Jenjang Sasaran</div><div class="mg-val">${esc(r.jenjang)}</div></div>
      <div><div class="mg-label">Mode &amp; Lokasi</div><div class="mg-val">${esc(r.mode_lokasi)}</div></div>
      <div><div class="mg-label">Sumber Deep Search</div><div class="mg-val">${r.source_url ? `<a href="${esc(r.source_url)}" target="_blank" rel="noopener">${esc(r.source_url)}</a>` : "-"}</div></div>
    </div>
    <div style="margin-bottom:16px;">
      <div class="mg-label" style="margin-bottom:4px;">Catatan Hasil Deep Search</div>
      <div style="font-size:13.5px; color:#1e293b; background:#f8fafc; padding:10px 12px; border-radius:8px; border:1px solid var(--border);">${esc(r.notes)}</div>
    </div>
    <div>
      <div class="mg-label" style="margin-bottom:8px;">Daftar Ajang Terkurasi di SIMT (${r.simt_comps.length} Ajang, ${r.branches_cnt} Cabang)</div>
      ${simtHtml}
    </div>
  `;
  document.getElementById("detailModal").classList.add("open");
}

function closeModal() {
  document.getElementById("detailModal").classList.remove("open");
}

document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeModal();
});

function exportCSV() {
  const headers = [
    "No", "Penyelenggara", "Singkatan", "Negara", "Rating Maks SIMT", "Skor Rata-rata",
    "Jumlah Ajang SIMT", "Jumlah Cabang SIMT", "Klaster", "Level",
    "Lomba Terdekat", "Status Jadwal", "Tanggal Mulai", "Tanggal Selesai",
    "Batas Pendaftaran", "Jenjang Sasaran", "Mode", "Lokasi/Mode Detail",
    "Website Penyelenggara", "Sumber Jadwal", "Catatan"
  ];
  const csvEsc = v => '"' + String(v ?? "").replace(/"/g, '""') + '"';
  const rows = filtered.map((r, i) => [
    i + 1, r.org, r.org_short, r.country, r.rating, r.avg_score ?? "",
    r.comps_cnt, r.branches_cnt, r.clusters.join("; "), r.levels.join("; "),
    r.event, r.status, r.start, r.end, r.reg_deadline, r.jenjang,
    r.mode_type, r.mode_lokasi, r.org_link, r.source_url, r.notes
  ].map(csvEsc).join(","));

  const bom = "\\uFEFF";
  const blob = new Blob([bom + headers.map(csvEsc).join(",") + "\\n" + rows.join("\\n")], { type: "text/csv;charset=utf-8;" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "lomba_kurasi_simt_bintang3plus_2026_2027.csv";
  a.click();
}

updateHeaderIndicators();
applyFilters(true);
</script>
</body>
</html>
"""

html_out = (
    HTML_TEMPLATE
    .replace("__DATA_JSON__", data_json)
    .replace("__TOTAL_COMPS__", str(total_simt_comps))
    .replace("__TOTAL_BRANCHES__", f"{total_simt_branches:,}".replace(",", "."))
)

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"Generated {OUT_HTML} ({len(html_out):,} bytes) for {len(records)} organizers.")
