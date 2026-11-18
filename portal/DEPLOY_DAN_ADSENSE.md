# Panduan Deploy Online, SEO & Aktivasi Google AdSense (`lombakurasi.info`)

Portal pSEO berada di folder `portal/` dengan hasil build statis di `portal/dist/` (320+ halaman inti terindeks + halaman paginasi `noindex` + `sitemap-index.xml`).

## 1. Mengatur Domain `lombakurasi.info` di Vercel & DNS
1. Tambahkan `lombakurasi.info` dan `www.lombakurasi.info` di **Vercel Dashboard → Settings → Domains**.
2. Jadikan `lombakurasi.info` sebagai **Primary Domain**, dan arahkan `www.lombakurasi.info` serta `lombakurasi.vercel.app` dengan **301 Redirect** ke `https://lombakurasi.info`.
3. Set Environment Variable di Vercel: `SITE_URL=https://lombakurasi.info` lalu redeploy.
4. Pastikan email `redaksi@lombakurasi.info` aktif (mis. via Cloudflare Email Routing atau Zoho Mail).

## 2. Build & Deploy Lokal
```bash
npm run build
npm run preview
```
- **Build command**: `npm run build`
- **Output directory**: `dist`
- **Root directory**: `portal`

## 3. Mengaktifkan Monitoring Trafik Admin
Buka `src/config/site.ts` bagian `analytics` & `seo`:
- `gaMeasurementId`: isi dengan Google Analytics 4 Measurement ID (`"G-..."`) untuk memantau trafik, sumber akuisisi, serta custom event (`click_official_source`, `click_urgent_deadline`, `save_competition`, `directory_filter_used`, `export_csv`).
- `clarityId`: isi dengan Microsoft Clarity Project ID untuk heatmap & scroll depth.
- `enableVercelAnalytics` & `enableVercelSpeedInsights`: ubah ke `true` setelah fitur diaktifkan di Dashboard Vercel.
- Verifikasi domain `lombakurasi.info` di **Google Search Console** (disarankan via TXT record DNS) lalu submit `https://lombakurasi.info/sitemap-index.xml`.

## 4. Cara Mengaktifkan Google AdSense (Setelah Akun Disetujui)
> **Catatan Penting:** `showPlaceholders` di `src/config/site.ts` sengaja diset `false` agar tidak ada kotak iklan kosong tampil sebelum akun AdSense disetujui.

1. Buka `src/config/site.ts` dan isi:
   - `adsenseClient`: isi dengan Publisher ID Anda, misalnya `"ca-pub-1234567890123456"`.
   - `slots`: isi masing-masing slot ID (`topLeaderboard`, `inFeed`, `inArticle`, `sidebarBox`, `sidebarSticky`, `mobileAnchor`).
2. Buka `public/ads.txt`, hapus tanda `#` pada baris template dan ganti `pub-0000000000000000` dengan Publisher ID AdSense Anda.
3. Jalankan ulang `npm run build` lalu deploy ke Vercel.
