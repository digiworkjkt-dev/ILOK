# Kumpulan Lomba Terkurasi SIMT Kemendikdasmen (Bintang 3★ ke Atas)

Proyek hasil riset, scraping data kurasi SIMT Kemendikdasmen, dan deep search jadwal pelaksanaan lomba terdekat per penyelenggara berdasarkan waktu acuan **15 November 2026**.

## Output Utama
- `index.html` — Halaman HTML mandiri (*standalone*, tidak membutuhkan server maupun koneksi internet untuk membuka datanya) berisi tabel interaktif 292 penyelenggara terkurasi (mencakup 682 judul ajang & 1.284 cabang lomba bintang 3★–5★), lengkap dengan:
  - KPI ringkasan interaktif (Pendaftaran Dibuka, Sedang Berlangsung, Akan Datang/Terjadwal, Estimasi Siklus Tahunan, Kurasi 4★ & 5★).
  - Filter multi-kriteria: pencarian teks bebas, status jadwal, rentang waktu terdekat (Nov 2026, Des 2026, Q1 2027, Q2 2027, H2 2027, memiliki deadline), rating bintang SIMT, klaster, tingkat/level, jenjang sasaran, mode pelaksanaan (Online/Offline/Hybrid), dan negara.
  - Sorting multi-opsi & klik header kolom (pelaksanaan terdekat, batas pendaftaran terdekat, rating tertinggi, skor SIMT, jumlah cabang, A–Z).
  - Modal **Detail & Ajang SIMT** per penyelenggara untuk melihat catatan jadwal hasil deep search beserta seluruh daftar ajang dan cabang terkurasi di SIMT.
  - Ekspor hasil filter ke file `.csv`.

## Ringkasan Data (Per 15 November 2026)
- **Sumber SIMT**: `https://simt.kemendikdasmen.go.id/kurasi/advanced-search` (`/api/v2/list-kurasi` dengan `rate_kurasi` 3, 4, 5)
- **Total Data Terkurasi ≥ 3★**: 1.284 entri cabang (5★: 7, 4★: 197, 3★: 1.080) dari 682 ajang dan **292 penyelenggara unik** (5★: 6, 4★: 86, 3★: 200).
- **Status Jadwal Terdekat Hasil Deep Search (292 Penyelenggara)**:
  - Pendaftaran Dibuka: 47
  - Sedang Berlangsung: 12
  - Akan Datang (Terjadwal): 40
  - Estimasi Siklus Tahunan: 174
  - Belum Ada Info Terbaru: 19

## Struktur Folder
- `index.html` — Output HTML interaktif utama
- `data/simt_kurasi_star3plus.json` — Data mentah hasil scraping SIMT (1.284 baris)
- `data/organizers_master.json` — Pengelompokan 292 penyelenggara beserta daftar ajang & cabang SIMT
- `data/merged_lomba_kurasi.json` — Dataset gabungan SIMT + hasil deep search 292 penyelenggara
- `scrape_simt.py`, `build_organizer_master.py`, `crawl_organizers.py`, `merge_and_validate.py`, `generate_html.py` — Skrip pipeline pengolahan data
