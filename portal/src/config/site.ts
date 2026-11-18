export const SITE = {
  name: "InfoLombaKurasi",
  domain: "lombakurasi.info",
  url: "https://lombakurasi.info",
  tagline: "Kalender Lomba Terkurasi Nasional & Internasional (Bintang 3★–5★)",
  description:
    "Direktori jadwal pelaksanaan lomba terdekat berstandar kurasi bintang 3 ke atas. Dilengkapi filter jenjang, status pendaftaran, batas waktu, dan panduan kompetisi.",
  referenceDate: "2026-11-15",
  referenceDateLabel: "15 November 2026",
  lastUpdatedLabel: "18 November 2026",
  contactEmail: "redaksi@lombakurasi.info",
  perPage: 20,
  seo: {
    defaultOgImage: "/og-default.png",
    // Isi dengan kode verifikasi Google Search Console / Bing Webmaster jika tidak memakai verifikasi DNS TXT
    googleSiteVerification: "",
    bingSiteVerification: "",
  },
  analytics: {
    // Isi dengan Google Analytics 4 Measurement ID, contoh: "G-XXXXXXXXXX"
    gaMeasurementId: "",
    // Isi dengan Microsoft Clarity Project ID, contoh: "abcd1234ef"
    clarityId: "",
    // Ubah ke true setelah mengaktifkan Web Analytics / Speed Insights di Dashboard Vercel
    enableVercelAnalytics: false,
    enableVercelSpeedInsights: false,
  },
  ads: {
    // Isi dengan Publisher ID Google AdSense Anda, contoh: "ca-pub-1234567890123456"
    adsenseClient: "",
    // Tetap false sebelum AdSense disetujui agar tidak menampilkan kotak iklan kosong saat proses review.
    showPlaceholders: false,
    slots: {
      topLeaderboard: "",
      inFeed: "",
      inArticle: "",
      sidebarBox: "",
      sidebarSticky: "",
      mobileAnchor: "",
    },
  },
};
