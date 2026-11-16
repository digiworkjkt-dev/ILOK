# Panduan Deploy Online & Aktivasi Google AdSense

Portal pSEO multi-halaman berada di folder `portal/` dengan hasil build statis siap upload di `portal/dist/` (**418 halaman HTML statis** + `sitemap-index.xml`).

## 1. Mengatur Domain Website
1. Ubah domain default di `astro.config.mjs` (atau set environment variable `SITE_URL=https://domainanda.com` saat build).
2. Perbarui baris `Sitemap:` di `public/robots.txt` agar mengarah ke `https://domainanda.com/sitemap-index.xml`.
3. Perbarui `contactEmail` dan `name` di `src/config/site.ts`.

## 2. Build & Deploy ke Hosting Statis (Gratis / Murah & Kencang)
Portal ini 100% statis (*zero backend server*), sehingga dapat di-deploy langsung ke **Cloudflare Pages**, **Vercel**, **Netlify**, atau **cPanel/Nginx**:
- **Build command**: `npm run build`
- **Output directory**: `dist`
- **Root directory**: `portal`

Atau jalankan di lokal terlebih dahulu:
```bash
npm run build
npm run preview
```

## 3. Cara Mengaktifkan Google AdSense (Setelah Akun Disetujui)
Seluruh penempatan iklan sudah dirancang dengan tinggi tercadang (*reserved height*) untuk menjaga skor **CLS (Cumulative Layout Shift)** tetap rendah.

1. Buka `src/config/site.ts` dan isi:
   - `adsenseClient`: isi dengan Publisher ID Anda, misalnya `"ca-pub-1234567890123456"`.
   - `slots`: isi masing-masing slot ID (`topLeaderboard`, `inFeed`, `inArticle`, `sidebarBox`, `sidebarSticky`, `mobileAnchor`).
   - Ubah `showPlaceholders: false` jika Anda hanya ingin menampilkan unit iklan yang aktif.
2. Buka `public/ads.txt`, hapus tanda `#` pada baris template dan ganti `pub-0000000000000000` dengan Publisher ID AdSense Anda.
3. Jalankan ulang `npm run build` lalu deploy folder `dist/`.
