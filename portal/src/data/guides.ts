export interface GuideArticle {
  slug: string;
  title: string;
  category: string;
  readMinutes: number;
  publishedAt: string;
  updatedAt: string;
  excerpt: string;
  relatedHubs: { label: string; href: string }[];
  sections: { heading: string; paragraphs: string[]; bullets?: string[] }[];
  faqs: { q: string; a: string }[];
}

export const GUIDES: GuideArticle[] = [
  {
    slug: "arti-bintang-kurasi-lomba-untuk-jalur-prestasi",
    title: "Arti Peringkat Bintang 3 hingga 5 pada Lomba Terkurasi dan Manfaatnya untuk Jalur Prestasi",
    category: "Panduan Kurasi",
    readMinutes: 6,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Memahami cara kerja peringkat bintang kurasi ajang talenta dan mengapa lomba bintang 3 ke atas menjadi patokan penting untuk portofolio akademik maupun seleksi jalur prestasi.",
    relatedHubs: [
      { label: "Lihat Lomba Bintang 4★ & 5★", href: "/kategori/bintang-4-dan-5/" },
      { label: "Lomba SMA/SMK/MA", href: "/kategori/sma-smk-ma/" },
    ],
    sections: [
      {
        heading: "Apa Itu Penilaian Kurasi Ajang Talenta?",
        paragraphs: [
          "Kurasi ajang talenta adalah proses peninjauan kualitas suatu kompetisi berdasarkan rekam jejak penyelenggara, kejelasan pedoman teknis (juknis), objektivitas penjurian, cakupan wilayah peserta, serta konsistensi pelaksanaan.",
          "Setiap penyelenggara — baik lembaga riset, perguruan tinggi, induk organisasi olahraga, yayasan, maupun penyelenggara independen — dievaluasi berdasarkan standar tata kelola kompetisi yang terukur.",
        ],
      },
      {
        heading: "Mengapa Memilih Lomba Bintang 3★ ke Atas?",
        paragraphs: [
          "Dalam direktori ini, kami hanya menampilkan ajang dan cabang kompetisi yang telah memenuhi kriteria kurasi Bintang 3★, 4★, dan 5★ untuk membantu peserta menghindari lomba berisiko rendah kredibilitas.",
        ],
        bullets: [
          "Bintang 5★: Peringkat tertinggi dengan skor kurasi sangat kuat, tata kelola mapan, serta rekam jejak penyelenggaraan yang konsisten (contoh: Indonesia Inventors Day, NDO Goethe-Institut, ISFO OJK, Gita Bahana Nusantara, Kejurnas PERCASI, Kejuaraan PB ABTI).",
          "Bintang 4★: Kredibilitas penyelenggara tinggi dengan cakupan peserta luas di tingkat nasional maupun internasional.",
          "Bintang 3★: Sudah memenuhi standar kurasi yang diakui dan layak dijadikan portofolio prestasi resmi sesuai jenjang dan tingkatnya.",
        ],
      },
      {
        heading: "Tips Memanfaatkan Sertifikat Lomba untuk Jalur Prestasi",
        paragraphs: [
          "Sertifikat dari lomba terkurasi memudahkan sekolah, perguruan tinggi, maupun panitia beasiswa memverifikasi keabsahan dan bobot ajang yang diikuti siswa. Pastikan nama penyelenggara, nama ajang, serta cabang lomba pada sertifikat Anda tercantum lengkap dan sesuai.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah semua lomba berbayar berarti tidak berkualitas?",
        a: "Tidak. Banyak penyelenggara independen maupun yayasan yang mengenakan biaya pendaftaran tetap meraih peringkat kurasi bintang 3 atau 4 apabila tata kelola, sistem penjurian, dan integritas lombanya memenuhi standar penilaian.",
      },
      {
        q: "Apakah data jadwal di direktori ini selalu resmi dari panitia?",
        a: "Kami menelusuri tautan resmi masing-masing penyelenggara dan memisahkan secara tegas antara jadwal terkonfirmasi dengan estimasi siklus tahunan. Selalu lakukan verifikasi akhir pada situs resmi penyelenggara sebelum mendaftar.",
      },
    ],
  },
  {
    slug: "cara-memeriksa-kelayakan-dan-status-kurasi-lomba",
    title: "Panduan Memeriksa Kelayakan dan Status Kurasi Lomba bagi Siswa, Sekolah, dan Penyelenggara",
    category: "Panduan Kurasi",
    readMinutes: 5,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Langkah praktis memeriksa rekam jejak kurasi lomba incaran Anda serta hal-hal penting yang wajib dicek sebelum mendaftar.",
    relatedHubs: [
      { label: "Lomba Pendaftaran Dibuka", href: "/kategori/pendaftaran-dibuka/" },
      { label: "Lomba Nasional", href: "/kategori/nasional/" },
    ],
    sections: [
      {
        heading: "1. Cek Rekam Jejak Kurasi Sebelum Mendaftar Lomba",
        paragraphs: [
          "Kesalahan paling sering terjadi adalah siswa mengikuti lomba terlebih dahulu tanpa memeriksa kredibilitas penyelenggaranya, lalu baru menyadari sertifikatnya kurang berbobot saat hendak dilampirkan untuk seleksi sekolah, kampus, atau beasiswa.",
          "Gunakan fitur pencarian di direktori ini untuk memastikan penyelenggara dan cabang lomba yang diikuti minimal memiliki peringkat bintang 3★.",
        ],
      },
      {
        heading: "2. Periksa Kecocokan Cabang dan Tahun Penyelenggaraan",
        paragraphs: [
          "Penilaian kurasi melekat pada kombinasi penyelenggara, nama ajang, dan cabang lomba (misalnya cabang Matematika, Biologi, Catur, atau Karya Ilmiah). Satu ajang bisa memiliki puluhan cabang dengan skor penilaian yang berbeda.",
        ],
        bullets: [
          "Simpan tautan resmi juknis dan halaman pengumuman pemenang sebagai bukti pendukung.",
          "Pastikan nama lengkap peserta, jenjang (SD/SMP/SMA/DIKTI), dan tanggal pelaksanaan tercantum jelas pada sertifikat.",
        ],
      },
    ],
    faqs: [
      {
        q: "Mengapa beberapa lomba belum memiliki tanggal pasti untuk tahun berikutnya?",
        a: "Banyak kompetisi tahunan baru merilis tanggal resmi 2–4 bulan sebelum pendaftaran dibuka. Pada kasus tersebut, kami menampilkan proyeksi bulan pelaksanaan berdasarkan siklus edisi sebelumnya.",
      },
    ],
  },
  {
    slug: "strategi-lomba-riset-dan-inovasi-bintang-4-dan-5",
    title: "Strategi Memilih Lomba Riset dan Inovasi Terkurasi Bintang 4–5 untuk Pelajar",
    category: "Riset & Inovasi",
    readMinutes: 6,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Klaster Riset dan Inovasi mendominasi lebih dari separuh data lomba terkurasi bintang 3+. Simak cara memilih antara olimpiade sains tertulis dan kompetisi proyek penelitian.",
    relatedHubs: [
      { label: "Klaster Riset & Inovasi", href: "/kategori/riset-dan-inovasi/" },
      { label: "Kurasi 4★ & 5★", href: "/kategori/bintang-4-dan-5/" },
    ],
    sections: [
      {
        heading: "Dua Jalur Utama di Klaster Riset dan Inovasi",
        paragraphs: [
          "Dari 1.284 cabang lomba bintang 3★ ke atas di direktori kami, sebanyak 839 entri berada di klaster Riset dan Inovasi. Secara umum, ajang di klaster ini terbagi menjadi dua format: olimpiade berbasis ujian (CBT/tertulis) dan kompetisi berbasis proyek/karya ilmiah.",
        ],
        bullets: [
          "Kompetisi Proyek & Invensi: Contohnya Indonesia Inventors Day (INNOPA), Lomba Peneliti Belia (CYS), maupun ajang IYSA seperti AISEEF dan GYIIF. Sangat kuat untuk melatih riset tim, poster ilmiah, dan presentasi bahasa Inggris.",
          "Olimpiade Sains Berbasis Tes: Cocok untuk siswa yang kuat di pemecahan soal Matematika, Fisika, Kimia, Biologi, Ekonomi, dan Informatika secara individu.",
        ],
      },
      {
        heading: "Kapan Waktu Terbaik Memulai Persiapan?",
        paragraphs: [
          "Lomba proyek penelitian membutuhkan waktu persiapan minimal 2 hingga 4 bulan untuk perumusan masalah, eksperimen atau pembuatan prototipe, dan penulisan makalah. Karena itu, pantau estimasi siklus tahunan sejak awal semester agar tidak terburu-buru.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah siswa SMP boleh mengikuti kompetisi inovasi internasional?",
        a: "Banyak ajang riset internasional membuka kategori terpisah untuk Elementary (SD), Junior High (SMP), Senior High (SMA), hingga University. Periksa kolom Jenjang Sasaran sebelum mendaftar.",
      },
    ],
  },
  {
    slug: "kalender-persiapan-lomba-sma-jalur-prestasi-2027",
    title: "Kalender Persiapan Lomba Siswa SMA/SMK/MA Tahun Ajaran 2026–2027 untuk Portofolio Prestasi",
    category: "Strategi Siswa",
    readMinutes: 5,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Menyusun timeline keikutsertaan lomba terkurasi dari November 2026 hingga akhir 2027 agar selaras dengan jadwal akademik sekolah dan target studi lanjut.",
    relatedHubs: [
      { label: "Lomba SMA/SMK/MA", href: "/kategori/sma-smk-ma/" },
      { label: "Jadwal Akhir 2026", href: "/kategori/jadwal-akhir-2026/" },
      { label: "Jadwal 2027", href: "/kategori/jadwal-2027/" },
    ],
    sections: [
      {
        heading: "Pembagian Kuartal Persiapan Lomba",
        paragraphs: [
          "Siswa kelas 10 dan 11 memiliki waktu paling ideal untuk mengumpulkan portofolio prestasi terkurasi tanpa mengganggu persiapan ujian akhir kelas 12.",
        ],
        bullets: [
          "November – Desember 2026: Ikuti ajang akhir tahun yang pendaftarannya masih dibuka serta persiapkan naskah untuk lomba kuartal pertama 2027.",
          "Januari – Maret 2027 (Q1): Musim padat olimpiade sains daring/luring dan seleksi awal pameran inovasi (seperti AISEEF, NDO final, dan kompetisi universitas).",
          "April – Juni 2027 (Q2): Puncak audisi seni budaya (seperti Gita Bahana Nusantara), kompetisi bisnis/vokasi, dan kejuaraan olahraga pelajar.",
          "Juli – Oktober 2027 (H2): Puncak musim kompetisi nasional berbagai lembaga dan kementerian (seperti ISFO, Kejurnas, dan Indonesia Inventors Day).",
        ],
      },
    ],
    faqs: [
      {
        q: "Berapa jumlah sertifikat lomba yang ideal untuk portofolio prestasi masuk kampus?",
        a: "Kualitas, linearitas dengan program studi tujuan, tingkat kompetisi (Nasional/Internasional), serta peringkat kurasi bintang 3–5 jauh lebih menentukan daripada sekadar kuantitas sertifikat.",
      },
    ],
  },
  {
    slug: "panduan-ajang-olahraga-terkurasi-induk-cabor",
    title: "Mengenal Kejuaraan Olahraga Terkurasi Bintang 3–5 dari Induk Organisasi Resmi",
    category: "Olahraga",
    readMinutes: 5,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Dari catur, atletik, panahan, bola voli, menembak, hingga taekwondo: panduan memahami jalur kejuaraan olahraga terkurasi resmi.",
    relatedHubs: [
      { label: "Klaster Olahraga", href: "/kategori/olahraga/" },
      { label: "Lomba Nasional", href: "/kategori/nasional/" },
    ],
    sections: [
      {
        heading: "Peran Induk Organisasi Cabang Olahraga (PB/PP)",
        paragraphs: [
          "Dalam data terkurasi bintang 3★–5★, tercatat 247 entri di klaster Olahraga. Sebagian besar kejuaraan bereputasi tinggi diselenggarakan oleh induk organisasi resmi seperti PB PERCASI (Catur), PB PASI (Atletik), PP PBVSI (Bola Voli), PB PERBAKIN (Menembak), PB ABTI (Bola Tangan), PB TI (Taekwondo), PB PORSEROSI (Sepatu Roda), dan PB PERPANI (Panahan).",
        ],
      },
      {
        heading: "Syarat Administrasi yang Sering Ditanyakan",
        paragraphs: [
          "Berbeda dengan olimpiade akademik yang pendaftarannya bisa dilakukan mandiri oleh siswa, kejuaraan olahraga resmi umumnya mensyaratkan keanggotaan klub, surat rekomendasi Pengkab/Pengprov, atau hasil kualifikasi daerah terlebih dahulu.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah turnamen olahraga antar-sekolah swasta juga ada yang masuk daftar kurasi?",
        a: "Ya, selain Kejurnas induk cabor, liga pelajar populer dan kejuaraan terbuka yang dikelola profesional (seperti DBL Indonesia dan berbagai open tournament karate/pencak silat/renang) juga tercatat pada kategori bintang 3–4.",
      },
    ],
  },
  {
    slug: "panduan-lomba-seni-budaya-dan-bahasa-terkurasi",
    title: "Peluang Lomba Seni Budaya, Paduan Suara, dan Olimpiade Bahasa Terkurasi",
    category: "Seni Budaya",
    readMinutes: 5,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Menjelajahi 198 cabang seni budaya dan bahasa berperingkat bintang 3 ke atas, mulai dari olimpiade bahasa Jerman NDO, paduan suara internasional, hingga festival budaya.",
    relatedHubs: [
      { label: "Klaster Seni Budaya", href: "/kategori/seni-budaya/" },
      { label: "Tingkat Internasional", href: "/kategori/internasional/" },
    ],
    sections: [
      {
        heading: "Cakupan Klaster Seni Budaya",
        paragraphs: [
          "Klaster Seni Budaya tidak hanya memuat lomba tari, musik, lukis, atau paduan suara, tetapi juga mencakup sejumlah kompetisi bahasa asing dan sastra—misalnya Nationale Deutscholympiade (NDO) dari Goethe-Institut Indonesien yang meraih peringkat kurasi Bintang 5★.",
        ],
      },
      {
        heading: "Persiapan Portofolio dan Hak Cipta Karya",
        paragraphs: [
          "Pastikan karya seni, video audisi, maupun naskah sastra/dongeng merupakan karya asli peserta sesuai ketentuan juknis. Untuk lomba paduan suara dan musik orkestra, perhatikan jadwal audisi daerah yang kerap dibuka pada semester pertama setiap tahun.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah lomba bahasa Inggris dan bahasa Arab masuk klaster Seni Budaya?",
        a: "Pada pengelompokan klaster kami, cabang bahasa dan sastra umumnya masuk ke klaster Seni Budaya, sedangkan beberapa kompetisi literasi atau debat tematik bisa tersebar sesuai kategori penyelenggaranya. Gunakan kotak pencarian di Beranda untuk mencari kata kunci bahasa tertentu.",
      },
    ],
  },
  {
    slug: "olimpiade-online-vs-offline-terkurasi",
    title: "Lomba Online vs Offline vs Hybrid Terkurasi: Cara Memilih yang Paling Tepat",
    category: "Strategi Siswa",
    readMinutes: 4,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Memahami kelebihan, tantangan teknis, dan efisiensi biaya antara lomba daring (CBT/Zoom), luring, dan hybrid yang terkurasi bintang 3–5.",
    relatedHubs: [
      { label: "Pendaftaran Dibuka", href: "/kategori/pendaftaran-dibuka/" },
      { label: "Jadwal 2027", href: "/kategori/jadwal-2027/" },
    ],
    sections: [
      {
        heading: "Kapan Memilih Mode Online / Daring?",
        paragraphs: [
          "Lomba daring sangat menghemat biaya transportasi dan akomodasi, terutama bagi siswa di luar Pulau Jawa. Pastikan koneksi internet stabil dan ikuti simulasi teknis (try out sistem CBT atau kamera pengawas) sebelum hari-H.",
        ],
      },
      {
        heading: "Keunggulan Model Hybrid dan Offline",
        paragraphs: [
          "Banyak kompetisi unggulan (seperti ISFO, OKN UGM, LOGIKA UI, hingga ajang riset IYSA dan CYS) memakai format Hybrid: penyisihan daring agar menjangkau seluruh Indonesia, lalu babak semifinal/final secara luring di kampus atau pusat konvensi untuk menjamin objektivitas penjurian.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah sertifikat lomba online tetap bernilai jika terkurasi?",
        a: "Ya, selama ajang dan penyelenggaranya memiliki rekam jejak kurasi yang jelas, mode pelaksanaan daring, luring, maupun hybrid tetap diakui sesuai tingkat dan peringkat kurasinya.",
      },
    ],
  },
  {
    slug: "cara-verifikasi-keaslian-penyelenggara-lomba",
    title: "5 Langkah Memverifikasi Keaslian Penyelenggara Lomba Sebelum Membayar Registrasi",
    category: "Keamanan Peserta",
    readMinutes: 4,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Lindungi siswa dan sekolah dari penipuan lomba berkedok kurasi dengan memeriksa domain resmi, skor penilaian, dan jejak penyelenggaraan sebelumnya.",
    relatedHubs: [
      { label: "Kurasi 4★ & 5★", href: "/kategori/bintang-4-dan-5/" },
      { label: "Lomba Nasional", href: "/kategori/nasional/" },
    ],
    sections: [
      {
        heading: "Checklist Verifikasi Cepat",
        paragraphs: [
          "Maraknya promosi lomba di media sosial membuat peserta perlu cermat membedakan kompetisi bereputasi dari lomba instan yang minim standar penjurian.",
        ],
        bullets: [
          "Cocokkan nama resmi badan hukum/lembaga penyelenggara dengan profil terverifikasi (bukan hanya nama singkat atau logo acara).",
          "Pastikan tautan pendaftaran berasal dari domain resmi penyelenggara yang tercantum di halaman detail.",
          "Periksa riwayat pelaksanaan edisi tahun sebelumnya (dokumentasi pemenang, berita kampus/media, atau laporan kegiatan).",
          "Waspadai penyelenggara yang menjanjikan medali pasti atau sertifikat instan tanpa proses ujian/penjurian yang wajar.",
        ],
      },
    ],
    faqs: [
      {
        q: "Bagaimana jika menemukan tautan lama penyelenggara sudah tidak aktif?",
        a: "Beberapa penyelenggara mengganti domain atau berpindah ke kanal resmi terbaru. Pada direktori ini kami melengkapi kolom Sumber Jadwal dari hasil penelusuran web terkini untuk membantu menemukan situs aktifnya.",
      },
    ],
  },
  {
    slug: "panduan-lomba-sd-dan-smp-untuk-jalur-prestasi",
    title: "Panduan Orang Tua: Memilih Lomba Terkurasi SD dan SMP untuk Jalur Prestasi Sekolah",
    category: "Orang Tua & Sekolah",
    readMinutes: 5,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Tips mendampingi anak jenjang SD dan SMP mengikuti lomba terkurasi bintang 3–5 tanpa membebani psikologis belajar.",
    relatedHubs: [
      { label: "Lomba SD/MI", href: "/kategori/sd-mi/" },
      { label: "Lomba SMP/MTs", href: "/kategori/smp-mts/" },
    ],
    sections: [
      {
        heading: "Fokus pada Minat Alami dan Ketahanan Mental",
        paragraphs: [
          "Pada jenjang SD dan SMP, tujuan utama mengikuti kompetisi bukan sekadar berburu sertifikat untuk seleksi jalur prestasi, melainkan membangun rasa percaya diri, sportivitas, dan kebiasaan berpikir terstruktur.",
        ],
        bullets: [
          "Pilih 1–2 bidang minat utama anak (misalnya Matematika, Bahasa, Renang, Catur, atau Peneliti Belia) daripada mendaftarkan ke terlalu banyak cabang sekaligus.",
          "Manfaatkan fitur Simpan Lomba di portal ini untuk merencanakan maksimal 2–4 ajang terkurasi per semester.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah sertifikat lomba tingkat kabupaten/kota atau provinsi tetap berguna untuk seleksi sekolah?",
        a: "Ya. Dalam aturan jalur prestasi daerah, sertifikat berjenjang dari tingkat Kabupaten/Kota hingga Nasional dan Internasional memiliki bobot poin masing-masing sesuai ketentuan dinas pendidikan setempat.",
      },
    ],
  },
  {
    slug: "peluang-kompetisi-mahasiswa-dan-vokasi-terkurasi",
    title: "Peluang Kompetisi Nasional dan Vokasi Terkurasi untuk Mahasiswa (DIKTI)",
    category: "Mahasiswa & Vokasi",
    readMinutes: 5,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Mengulas ajang terkurasi untuk mahasiswa S1 maupun pendidikan vokasi (D3/D4), termasuk kompetisi himpunan mahasiswa UI, UGM, UNY, Undip, IPB, hingga Forum Vokasi.",
    relatedHubs: [
      { label: "Lomba Mahasiswa/DIKTI", href: "/kategori/mahasiswa-dikti/" },
      { label: "Klaster Riset & Inovasi", href: "/kategori/riset-dan-inovasi/" },
    ],
    sections: [
      {
        heading: "Mengapa Mahasiswa Tetap Perlu Memantau Standar Kurasi?",
        paragraphs: [
          "Banyak ajang bergengsi tingkat perguruan tinggi — baik yang digelar kementerian, organisasi mahasiswa (seperti HMJ/BEM FMIPA UI, UGM, UNY, Undip, IPB), maupun Forum Pendidikan Tinggi Vokasi Indonesia — tercatat dalam daftar kurasi bintang 3–4 dan memberi nilai tambah kuat pada SKPI (Surat Keterangan Pendamping Ijazah) serta seleksi mahasiswa berprestasi.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah lomba antar-universitas yang diadakan himpunan mahasiswa diakui?",
        a: "Sejumlah olimpiade dan kompetisi nasional yang diselenggarakan oleh fakultas maupun himpunan mahasiswa universitas ternama telah lolos penilaian kurasi bintang 3–4 dan masuk dalam direktori ini.",
      },
    ],
  },
  {
    slug: "checklist-dokumen-dan-juknis-sebelum-daftar-lomba",
    title: "Checklist Dokumen dan Poin Penting Juknis yang Wajib Dibaca Sebelum Mendaftar Lomba",
    category: "Tips Teknis",
    readMinutes: 4,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Jangan sampai gugur karena masalah administrasi: cek poin-poin krusial dalam buku panduan/juknis lomba sebelum hari penutupan pendaftaran.",
    relatedHubs: [
      { label: "Pendaftaran Dibuka", href: "/kategori/pendaftaran-dibuka/" },
      { label: "Jadwal Akhir 2026", href: "/kategori/jadwal-akhir-2026/" },
    ],
    sections: [
      {
        heading: "Poin Krusial di Setiap Juknis Lomba",
        paragraphs: [
          "Banyak peserta gagal lolos ke babak selanjutnya bukan karena kemampuan akademik, melainkan kelalaian administratif saat mengunggah berkas.",
        ],
        bullets: [
          "Batas usia atau tingkat kelas aktif pada tahun ajaran berjalan (perhatikan status siswa kelas akhir).",
          "Status kepesertaan: Individu atau Tim (serta apakah anggota tim boleh lintas sekolah/lintas angkatan).",
          "Format penamaan file, ukuran maksimal PDF/video, dan batas waktu unggah berdasarkan zona waktu (WIB/WITA/WIT).",
          "Persyaratan surat tugas/rekomendasi kepala sekolah atau pembina jika diwajibkan.",
          "Aturan plagiarisme, penggunaan AI, atau orisinalitas karya.",
        ],
      },
    ],
    faqs: [
      {
        q: "Kapan sebaiknya mengunggah berkas pendaftaran lomba?",
        a: "Usahakan mengunggah berkas minimal 2–3 hari sebelum batas akhir (deadline) untuk menghindari gangguan server penuh pada jam-jam terakhir penutupan.",
      },
    ],
  },
  {
    slug: "panduan-guru-pembina-menyusun-peta-jalan-lomba-sekolah",
    title: "Panduan Guru Pembina Ekskul: Menyusun Peta Jalan Lomba Terkurasi Sekolah Setahun Penuh",
    category: "Orang Tua & Sekolah",
    readMinutes: 5,
    publishedAt: "2026-11-15",
    updatedAt: "2026-11-15",
    excerpt:
      "Cara praktis bagi Wakasek Kesiswaan dan pembina tim olimpiade memetakan agenda lomba terkurasi bintang 3–5 agar pembinaan siswa lebih terarah dan hemat anggaran.",
    relatedHubs: [
      { label: "Kurasi 4★ & 5★", href: "/kategori/bintang-4-dan-5/" },
      { label: "Jadwal 2027", href: "/kategori/jadwal-2027/" },
    ],
    sections: [
      {
        heading: "Mengelompokkan Target Lomba Berdasarkan Klaster & Siklus",
        paragraphs: [
          "Dengan 292 penyelenggara yang sudah dikelompokkan ke dalam klaster Riset dan Inovasi, Olahraga, serta Seni Budaya beserta estimasi bulan pelaksanaannya, sekolah dapat menyusun kalender pembinaan tahunan sebelum tahun anggaran berjalan.",
        ],
        bullets: [
          "Tetapkan ajang Bintang 4★–5★ sebagai target utama tim inti sekolah.",
          "Gunakan ajang Bintang 3★ daring sebagai ajang pemanasan dan uji mental bertanding sebelum menghadapi kompetisi utama.",
          "Ekspor daftar hasil filter dari direktori ini ke format CSV untuk rapat koordinasi guru pembina dan komite sekolah.",
        ],
      },
    ],
    faqs: [
      {
        q: "Apakah data dari direktori ini bisa diekspor untuk keperluan rapat sekolah?",
        a: "Ya, di halaman Beranda tersedia tombol Export CSV yang mengunduh seluruh daftar lomba sesuai filter jenjang atau klaster yang sedang Anda pilih.",
      },
    ],
  },
];

export function getGuideBySlug(slug: string): GuideArticle | undefined {
  return GUIDES.find((g) => g.slug === slug);
}
