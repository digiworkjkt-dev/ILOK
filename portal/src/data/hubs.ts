import type { OrganizerItem } from "../utils/format";

export interface HubDefinition {
  slug: string;
  title: string;
  shortTitle: string;
  metaDescription: string;
  group: "Status & Prioritas" | "Klaster Bidang" | "Jenjang Sasaran" | "Tingkat" | "Periode Waktu";
  intro: string;
  tips: string[];
  filterFn: (item: OrganizerItem) => boolean;
}

export const HUBS: HubDefinition[] = [
  {
    slug: "pendaftaran-dibuka",
    title: "Lomba Terkurasi yang Pendaftarannya Sedang Dibuka",
    shortTitle: "Pendaftaran Dibuka",
    metaDescription:
      "Daftar lomba terkurasi bintang 3 sampai 5 yang pendaftarannya sedang dibuka per November 2026 lengkap dengan batas pendaftaran.",
    group: "Status & Prioritas",
    intro:
      "Halaman ini menghimpun penyelenggara lomba terkurasi bintang 3★ ke atas yang status pendaftarannya aktif dibuka per 15 November 2026. Gunakan filter di bawah untuk menyaring jenjang SD, SMP, SMA/SMK, hingga mahasiswa.",
    tips: [
      "Periksa batas pendaftaran (deadline) karena beberapa kompetisi menutup registrasi bertahap (early bird hingga reguler).",
      "Pastikan cabang lomba yang dipilih sesuai dengan daftar cabang terkurasi pada halaman detail penyelenggara.",
    ],
    filterFn: (x) => x.status === "Pendaftaran Dibuka",
  },
  {
    slug: "bintang-4-dan-5",
    title: "Lomba Terkurasi Bintang 4★ dan 5★ Terbaik",
    shortTitle: "Kurasi 4★ & 5★",
    metaDescription:
      "Kumpulan penyelenggara ajang talenta dengan peringkat kurasi tertinggi (Bintang 4 dan Bintang 5) beserta jadwal pelaksanaan terdekat 2026–2027.",
    group: "Status & Prioritas",
    intro:
      "Kurasi Bintang 4★ dan 5★ merupakan peringkat tertinggi dalam direktori kompetisi kami yang mencerminkan kualitas tata kelola, cakupan peserta, dan kredibilitas penyelenggara.",
    tips: [
      "Prioritaskan ajang Bintang 4★–5★ untuk memperkuat portofolio seleksi masuk sekolah/kampus jalur prestasi dan beasiswa.",
      "Banyak ajang 5★ seperti NDO, ISFO, Gita Bahana Nusantara, dan Indonesia Inventors Day memiliki seleksi berjenjang yang dimulai beberapa bulan sebelum final.",
    ],
    filterFn: (x) => x.rating >= 4,
  },
  {
    slug: "riset-dan-inovasi",
    title: "Lomba Riset dan Inovasi Terkurasi (Bintang 3★–5★)",
    shortTitle: "Riset & Inovasi",
    metaDescription:
      "Jadwal terbaru olimpiade sains, karya tulis ilmiah, robotik, teknologi, dan inovasi terkurasi bintang 3 ke atas.",
    group: "Klaster Bidang",
    intro:
      "Klaster Riset dan Inovasi mencakup olimpiade sains (matematika, fisika, kimia, biologi, informatika), kompetisi penelitian belia, karya tulis ilmiah, hingga pameran invensi dan robotik.",
    tips: [
      "Untuk kompetisi berbasis makalah/proyek riset, siapkan abstrak dan logbook penelitian minimal 1–2 bulan sebelum batas submit.",
      "Cek apakah babak penyisihan dilaksanakan daring dan babak final luring agar sekolah dapat menyiapkan anggaran perjalanan lebih awal.",
    ],
    filterFn: (x) => x.clusters.includes("Riset dan Inovasi"),
  },
  {
    slug: "olahraga",
    title: "Kejuaraan Olahraga Terkurasi (Bintang 3★–5★)",
    shortTitle: "Olahraga",
    metaDescription:
      "Daftar kejuaraan nasional, provinsi, dan internasional cabang olahraga terkurasi bintang 3 ke atas beserta jadwal terdekat 2026–2027.",
    group: "Klaster Bidang",
    intro:
      "Klaster Olahraga berisi kejuaraan resmi dari induk organisasi olahraga (PB PERCASI, PB PASI, PP PBVSI, PB PERBAKIN, PB TI, Indonesia Archery, dll.) serta turnamen pelajar dan mahasiswa terkurasi bintang 3★–5★.",
    tips: [
      "Pastikan atlet terdaftar pada klub/pengcab resmi jika kejuaraan mensyaratkan rekomendasi Pengprov atau kartu anggota induk cabor.",
      "Perhatikan kategori kelompok umur (KU / U-15 / U-17 / U-19) pada juknis resmi masing-masing kejuaraan.",
    ],
    filterFn: (x) => x.clusters.includes("Olahraga"),
  },
  {
    slug: "seni-budaya",
    title: "Lomba Seni Budaya dan Bahasa Terkurasi (Bintang 3★–5★)",
    shortTitle: "Seni Budaya",
    metaDescription:
      "Jadwal lomba paduan suara, tari, musik, sastra, debat, dan olimpiade bahasa asing terkurasi bintang 3 ke atas.",
    group: "Klaster Bidang",
    intro:
      "Klaster Seni Budaya menghimpun festival paduan suara, seni pertunjukan, musik, desain, hingga olimpiade bahasa asing (seperti Nationale Deutscholympiade Goethe-Institut) yang terkurasi bintang 3★ ke atas.",
    tips: [
      "Siapkan portofolio video rekaman berkualitas baik untuk tahap audisi daring maupun seleksi daerah.",
      "Periksa ketentuan karya orisinal atau repertoar wajib yang ditetapkan panitia sejak jauh hari.",
    ],
    filterFn: (x) => x.clusters.includes("Seni Budaya"),
  },
  {
    slug: "sd-mi",
    title: "Daftar Lomba Terkurasi untuk Siswa SD / MI",
    shortTitle: "Jenjang SD/MI",
    metaDescription:
      "Kumpulan kompetisi dan olimpiade jenjang SD/MI terkurasi bintang 3 ke atas lengkap dengan jadwal pelaksanaan terdekat.",
    group: "Jenjang Sasaran",
    intro:
      "Direktori penyelenggara lomba terkurasi bintang 3★–5★ yang membuka kategori peserta untuk jenjang Sekolah Dasar (SD/MI/sederajat).",
    tips: [
      "Untuk siswa SD, pilih kompetisi yang formatnya ramah usia (daring terawasi atau kategori Junior/Elementary) serta juknis pendampingan orang tua yang jelas.",
    ],
    filterFn: (x) => x.jenjangTags.includes("SD/MI"),
  },
  {
    slug: "smp-mts",
    title: "Daftar Lomba Terkurasi untuk Siswa SMP / MTs",
    shortTitle: "Jenjang SMP/MTs",
    metaDescription:
      "Jadwal lomba dan olimpiade SMP/MTs terkurasi bintang 3 ke atas untuk persiapan jalur prestasi.",
    group: "Jenjang Sasaran",
    intro:
      "Kumpulan ajang talenta terkurasi bintang 3★–5★ untuk pelajar SMP/MTs/sederajat di bidang riset, sains, olahraga, dan seni budaya. Sangat relevan untuk persiapan masuk SMA favorit jalur prestasi.",
    tips: [
      "Mulai kumpulkan sertifikat sejak kelas 7 dan 8 agar bobot prestasi sudah terkumpul sebelum pendaftaran SMA kelas 9.",
    ],
    filterFn: (x) => x.jenjangTags.includes("SMP/MTs"),
  },
  {
    slug: "sma-smk-ma",
    title: "Daftar Lomba Terkurasi untuk Siswa SMA / SMK / MA",
    shortTitle: "Jenjang SMA/SMK/MA",
    metaDescription:
      "Kalender lomba SMA, SMK, dan MA terkurasi bintang 3 sampai 5 sebagai penguat portofolio jalur prestasi dan beasiswa.",
    group: "Jenjang Sasaran",
    intro:
      "Halaman khusus pelajar SMA/SMK/MA/sederajat berisi lomba-lomba terkurasi bintang 3★–5★ yang sertifikatnya bernilai tinggi untuk penguatan portofolio seleksi masuk perguruan tinggi jalur prestasi maupun beasiswa.",
    tips: [
      "Sesuaikan bidang lomba dengan program studi impian Anda (misal klaster Riset/Informatika untuk prodi teknik/sains, atau Ekonomi/Bisnis).",
    ],
    filterFn: (x) => x.jenjangTags.includes("SMA/SMK/MA"),
  },
  {
    slug: "mahasiswa-dikti",
    title: "Daftar Lomba Terkurasi untuk Mahasiswa / Perguruan Tinggi",
    shortTitle: "Mahasiswa / DIKTI",
    metaDescription:
      "Kumpulan kompetisi nasional dan internasional untuk mahasiswa (DIKTI) terkurasi bintang 3 ke atas.",
    group: "Jenjang Sasaran",
    intro:
      "Daftar penyelenggara ajang talenta bintang 3★–5★ yang membuka kategori Mahasiswa / Perguruan Tinggi (D3/D4/S1), termasuk kompetisi vokasi, inovasi ilmiah, bisnis, dan olahraga mahasiswa.",
    tips: [
      "Konsultasikan keikutsertaan dengan bagian kemahasiswaan kampus untuk dukungan pendanaan delegasi dan pengakuan SKPI.",
    ],
    filterFn: (x) => x.jenjangTags.includes("Mahasiswa/DIKTI"),
  },
  {
    slug: "internasional",
    title: "Lomba Tingkat Internasional Terkurasi (Bintang 3★–5★)",
    shortTitle: "Tingkat Internasional",
    metaDescription:
      "Daftar kompetisi dan olimpiade berskala internasional yang terkurasi bintang 3 ke atas beserta jadwal terbaru.",
    group: "Tingkat",
    intro:
      "Menghimpun penyelenggara kompetisi bertaraf internasional (baik yang digelar di Indonesia maupun di luar negeri secara luring/daring) yang tercatat terkurasi bintang 3★–5★.",
    tips: [
      "Siapkan abstrak/presentasi berbahasa Inggris dan periksa kebijakan biaya registrasi atau jalur undangan delegasi nasional.",
    ],
    filterFn: (x) => x.levels.includes("Internasional"),
  },
  {
    slug: "nasional",
    title: "Lomba Tingkat Nasional Terkurasi (Bintang 3★–5★)",
    shortTitle: "Tingkat Nasional",
    metaDescription:
      "Jadwal lengkap lomba tingkat nasional terkurasi bintang 3 ke atas untuk seluruh jenjang.",
    group: "Tingkat",
    intro:
      "Daftar penyelenggara ajang talenta tingkat nasional dengan hasil kurasi bintang 3★ ke atas di seluruh klaster Riset dan Inovasi, Olahraga, maupun Seni Budaya.",
    tips: [
      "Pastikan sertifikat mencantumkan tingkat kompetisi (Nasional), nama cabang lomba, dan nama resmi penyelenggara secara jelas.",
    ],
    filterFn: (x) => x.levels.includes("Nasional"),
  },
  {
    slug: "jadwal-akhir-2026",
    title: "Kalender Lomba Terkurasi Akhir 2026 (November – Desember 2026)",
    shortTitle: "Akhir 2026 (Nov–Des)",
    metaDescription:
      "Jadwal pelaksanaan lomba terkurasi terdekat pada akhir November dan Desember 2026.",
    group: "Periode Waktu",
    intro:
      "Rekap lomba terkurasi bintang 3★–5★ yang berlangsung atau dijadwalkan pada rentang 15 November hingga 31 Desember 2026.",
    tips: [
      "Fokus pada lomba dengan status Pendaftaran Dibuka agar Anda masih sempat mendaftar sebelum penutupan akhir tahun.",
    ],
    filterFn: (x) => x.effectiveSort >= "2026-11-15" && x.effectiveSort <= "2026-12-31",
  },
  {
    slug: "jadwal-2027",
    title: "Kalender Lomba Terkurasi Tahun 2027 (Terjadwal & Estimasi Siklus)",
    shortTitle: "Jadwal 2027",
    metaDescription:
      "Daftar lomba terkurasi bintang 3 ke atas yang dijadwalkan maupun diproyeksikan berlangsung sepanjang tahun 2027.",
    group: "Periode Waktu",
    intro:
      "Perencanaan jangka menengah untuk tahun 2027, mencakup lomba-lomba yang sudah merilis jadwal 2027 (seperti AISEEF, ASCIENCO XII, dan Kejurnas) maupun estimasi siklus tahunan berdasarkan pelaksanaan 2026.",
    tips: [
      "Tandai lomba yang Anda incar (Simpan Lomba) dan pantau situs penyelenggara 2–3 bulan sebelum bulan pelaksanaan.",
    ],
    filterFn: (x) => x.effectiveSort >= "2027-01-01" && x.effectiveSort <= "2027-12-31",
  },
];

export function getHubBySlug(slug: string): HubDefinition | undefined {
  return HUBS.find((h) => h.slug === slug);
}
