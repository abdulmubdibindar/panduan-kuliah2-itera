# Catatan Penelaahan kuliah2.itera.ac.id

> Dokumen ini **bukan** pedoman akhir. Ini adalah catatan hasil eksplorasi langsung ke instance Moodle ITERA (`kuliah2.itera.ac.id`) yang dipakai sebagai bahan mentah saat menulis pedoman akhir sesuai kebutuhan ber-ID stabil di [[spec]]. Judul kategori di bawah adalah pengelompokan temuan, bukan jangkar kebutuhan.

## Ringkasan Eksplorasi

- **Tanggal**: 2026-07-09
- **Akun**: akun dosen milik Pak Abdul (`muhammad.bindar@pwk.itera.ac.id`), login SSO manual
- **Kursus contoh**: **PL25-12001 Statistika Untuk Perencanaan** (kategori PWK / FTIK), `course id=283`, dijadikan acuan konkret untuk sebagian besar temuan di bawah
- **Metode**: Chrome dijalankan dalam mode debugging (`--remote-debugging-port=9222`), Pak Abdul login manual, lalu [`explore_kuliah2.py`](07%20APAPUN%20DICOBA/Moodle%20Docs%20(manual)/Code/kuliah2-explore/explore_kuliah2.py) men-dump tiap halaman untuk dibaca
- **Catatan peran akun**: akun ini punya akses lebih luas dari sekadar dosen pengampu satu mata kuliah — terlihat link "Site administration" di navigasi global, serta akses ke `course/management.php` yang menampilkan **seluruh kategori dan kursus institusi** (bukan cuma milik Pak Abdul). Namun `admin/modules.php` (daftar modul aktivitas) mengembalikan **Access denied**, jadi bukan admin situs penuh — kemungkinan ada peran manajer/pengelola kategori. Eksplorasi ini sengaja **tidak** masuk ke kursus dosen lain demi privasi, hanya mencatat nama-nama kursus yang tampak di listing.
- **Kursus kedua**: Pak Abdul meng-*enroll* diri sendiri (sebagai **Student**) ke kursus **"[ITERA] EC-Council Artificial Intelligence Essentials (AIE)"** (`course id=673`, 72 partisipan) agar ada kursus yang benar-benar terisi untuk dijelajahi. Kursus ini dipakai **hanya untuk membandingkan menu** yang tampil ke peran Student vs Teacher (lihat §Jejak Digital) — bukan untuk menelaah konten materinya, karena Pak Abdul bukan dosen pengampu di sana.

---

## Uji Sandbox 20 Agustus 2026

Pengujian berikut dilakukan hanya pada kursus tersembunyi `course id=917`. Identitas akun dan nilai kunci *enrolment* tidak dicatat di dokumen ini.

- **Pembuatan kursus dan pengaturan awal**: kursus sandbox berhasil dibuat dan dipertahankan dalam keadaan **Hidden** selama penyiapan. Halaman kursus, **Settings**, **Participants**, **Groups**, **Groupings**, metode *enrolment*, dan pengaturan nilai dapat diuji tanpa menyentuh kursus aktif.
- **Kelas paralel dan *grouping***: dua *group* kelas paralel (`Kelas RA` dan `Kelas RB`) serta satu *grouping* berhasil dibuat dan muncul pada halaman pengelolaan masing-masing.
- **Pendaftaran mandiri per kelas**: *self enrolment* dengan kunci kelompok yang berbeda berhasil pada kedua kelas. Setelah formulir dikirim, akun uji memperoleh peran **Student** dan langsung masuk ke *group* RA atau RB yang sesuai. Nilai kuncinya tidak disimpan.
- **Pendaftaran manual belum terbukti**: modal **Enrol users** dapat dibuka, tetapi pencarian akun sasaran belum menghasilkan kecocokan yang dapat dipilih. Karena itu, alur *manual enrolment* belum boleh dinyatakan selesai. Pada modal yang diuji, *group* bawaan terpilih adalah `Kelas RA`; dosen harus memeriksa pilihan ini sebelum mengirim formulir.
- **Pilihan peran pada akun pengelola sandbox**: modal **Enrol users** dan penyunting peran sebaris menampilkan **Teacher**, **Non-editing teacher**, dan **Student**, dengan **Student** sebagai pilihan awal pada modal. Ini adalah temuan dari akun pengelola sandbox, bukan bukti bahwa akun dengan peran **Teacher** murni dapat menetapkan Teacher atau Non-editing teacher.
- **Batas Non-editing teacher**: akun uji dapat membuka **Participants**, **Grades** (termasuk **Grader report**), dan **More → Reports**. Di Reports tersedia **Logs**, **Live logs**, **Activity report**, dan **Course participation**. Akun ini tidak memperoleh **Edit mode**, **Turn editing on**, pengaturan kursus aktif, **Course reuse**, **Enrol users**, **Enrolment methods**, maupun pengelolaan **Groups/Groupings**. Barisnya di Participants menunjukkan hanya peran **Non-editing teacher**, tanpa peran Student dan tanpa keanggotaan kelas.
- **Batas Student**: akun Student ditolak saat mencoba membuka halaman pengelolaan Groups. Dengan konfigurasi sandbox saat ini, mahasiswa tidak dapat membuat atau mengubah *group* sendiri melalui menu inti Moodle; kebutuhan kelompok mandiri masih memerlukan mekanisme lain yang belum terbukti tersedia di ITERA.
- **Auto-create groups**: daftar **Select members from role** yang terlihat adalah **All**, **Manager**, **Course creator**, **Teacher**, **Non-editing teacher**, dan **Student**; pilihan `No roles` tidak tersedia. Pratinjau dengan **Student** menghitung satu pengguna menjadi satu *group* dan hanya menyasar peserta berperan Student. Pratinjau tidak disimpan sebagai perubahan akhir.

---

## Kepesertaan

Merujuk kebutuhan [[spec#D-02|D-02]], [[spec#D-03|D-03]], [[spec#D-04|D-04]], [[spec#M-02|M-02]], dan [[spec#M-03|M-03]].

### 1. Membuat mata kuliah
- **Update 22 Agustus 2026 (sandbox, akun dosen port 9233)**: jalur yang benar-benar dipakai dosen bukan lewat Site administration, melainkan tombol **"Create course"** yang tampil langsung di blok **Course overview** pada halaman **My courses** (`/my/courses.php`) — tidak perlu masuk ke Site administration sama sekali. Tombol ini membuka form yang sama, `/course/edit.php?category=0`.
- **Konfirmasi peran**: halaman Participants kursus sandbox (`id=917`) menunjukkan akun dosen uji berperan **"Teacher, Course creator"**, dan dua akun dosen tamu lain di kursus yang sama berperan **"Non-editing teacher, Course creator"**. Setiap akun dosen yang teramati membawa peran **Course creator** berdampingan dengan peran pengajarnya — bukan cuma akun dengan privilese tambahan seperti Pak Abdul. Ini menguatkan konfirmasi pengguna (22 Agustus 2026) bahwa **seluruh dosen ITERA dapat membuat kursusnya sendiri**, jadi ditambahkan sebagai [[spec#D-01A|D-01A]] yang semula terlewat dari spec.
- Field form **Add a new course**, dikonfirmasi lewat tangkapan layar sandbox: **Course full name**, **Course short name** (format `PRODI##-#####` mis. `PL25-12001`), **Course category** (kategori bawaan berlabel **"Silahkan pilih category PRODI"** — placeholder wajib diganti lewat kotak pencarian, bukan kategori sungguhan), **Course visibility** (Hide/Show), **Course start date**, **Course end date**, **Course ID number**, lalu bagian **Description**.
- Kursus dikelompokkan dalam struktur kategori dua level: **Fakultas → Program Studi** (contoh: `FTIK / PWK`, `FS / Matematika`, dst.), plus kategori khusus seperti `Tahap Persiapan Bersama` dan `MKWI (Mata Kuliah Wajib Institusi)`. Jalur lama lewat **Site administration → Courses → Manage courses and categories** (`/course/management.php`) tetap ada dan tetap berfungsi (breadcrumb form di atas tetap melewatinya), tetapi bukan jalur yang perlu diajarkan ke dosen karena tombol **Create course** lebih langsung.
- Referensi generik: [[Code/moodle_docs/Adding_a_new_course|Adding_a_new_course]], [[Code/moodle_docs/Course_settings|Course_settings]]

### 2. Meng-enroll mahasiswa jadi peserta per kelas
- Di kuliah2 ITERA, **satu mata kuliah = satu kursus Moodle**, dan pembagian per kelas paralel (mis. Kelas RA vs RB) dilakukan lewat fitur **Groups**, bukan kursus terpisah. Ditemukan grup `Kelas RA LDP 2025` dan `Kelas RB LDP 2025` di kursus Statistika.
- Metode enrolment yang aktif di kursus ini: **Self enrolment (Mahasiswa)** dan **Manual enrolments** (Guest access juga ada tapi tidak dipakai). Menu: **Participants → Enrolment methods** (`/enrol/instances.php?id=<course>`).
- Referensi generik: [[Code/moodle_docs/Enrolment_methods|Enrolment_methods]], [[Code/moodle_docs/Manual_enrolment|Manual_enrolment]], [[Code/moodle_docs/Self_enrolment|Self_enrolment]], [[Code/moodle_docs/Guest_access|Guest_access]], [[Code/moodle_docs/Groups|Groups]], [[Code/moodle_docs/Groupings|Groupings]]

### 3. Meng-assign dosen dan asisten
- Daftar peran yang tersedia di level kursus (halaman **Participants**): **No roles**, **Dosen Pengembang MK (Course creator)**, **Dosen (Teacher)**, **Dosen tamu (Non-editing teacher)**, **Mahasiswa (Student)** — label Indonesia dipetakan ke peran standar Moodle.
- Uji sandbox 20 Agustus 2026 mengonfirmasi bahwa **Non-editing teacher** dapat membuka Gradebook dan laporan, tetapi tidak dapat mengubah kursus, mengelola *enrolment*, atau mengelola Groups/Groupings. Kemampuan menilai *submission* Assignment dan *attempt* Quiz tetap perlu diuji setelah aktivitas tersebut tersedia.
- Assign peran dilakukan lewat halaman Participants → tombol enrol/assign role per pengguna.
- Referensi generik: [[Code/moodle_docs/Teacher_role|Teacher_role]]

### 4. Manajemen mahasiswa lulus vs mahasiswa baru
- **Tidak teramati langsung** (kursus contoh baru berisi 1 partisipan yaitu Pak Abdul sendiri, belum ada siklus kelulusan yang terjadi). Mekanisme umum yang tersedia di UI: filter status **Active/Inactive** di halaman Participants, aksi massal **"Edit selected user enrolments"** dan **"Delete selected user enrolments"**, serta kolom **"Status"** per peserta.
- **Keterbatasan**: belum bisa dipastikan apakah ITERA punya proses otomatis (mis. sinkronisasi dari SIAKAD) untuk unenrol mahasiswa lulus / enrol mahasiswa baru per semester, atau murni manual oleh dosen/admin prodi.

---

## Asesmen

Merujuk kebutuhan [[spec#D-07|D-07]], [[spec#D-08|D-08]], [[spec#D-09|D-09]], [[spec#D-10|D-10]], [[spec#D-11|D-11]], [[spec#M-05|M-05]], [[spec#M-06|M-06]], dan [[spec#M-07|M-07]].

### 1. Membuat asesmen — jenis Activity yang tersedia
- **Keterbatasan penting**: section **"Tugas dan Penilaian"** di kursus Statistika masih **kosong** (belum ada assignment/quiz/aktivitas apa pun ditambahkan), jadi tidak ada contoh hidup untuk diamati langsung. Kursus ini secara umum baru berisi 1 resource jenis **URL** ("Modul Statistika Untuk Perencanaan") di section "Materi Ajar".
- Percobaan mengecek daftar lengkap modul aktivitas lewat **Site administration → Plugins → Activity modules** (`/admin/modules.php`) mengembalikan **Access denied** — akun ini tidak punya akses admin situs penuh untuk melihat daftar modul terpasang.
- Percobaan mencoba menyalakan mode edit kursus (untuk membuka dialog "Add an activity or resource") **sengaja tidak dilanjutkan** — itu adalah aksi yang mengubah state kursus produksi sungguhan, di luar izin "cuma melihat-lihat" yang diberikan.
- **Yang tersedia di kursus level**: link **Question bank** (`/question/edit.php?courseid=283`) dan **Content bank** (`/contentbank/index.php`) sudah ada di menu administrasi kursus, menandakan fitur bank soal & bank konten aktif di instance ini.
- Referensi generik (perlu diverifikasi mana yang benar-benar aktif di instance ITERA saat kursus sudah berisi aktivitas): [[Code/moodle_docs/Activities|Activities]], [[Code/moodle_docs/Assignment|Assignment]], [[Code/moodle_docs/Quiz|Quiz]], [[Code/moodle_docs/Workshop|Workshop]], [[Code/moodle_docs/Workshop_activity|Workshop_activity]]

### 2. Safe Exam Browser
- **Status terverifikasi (24 Agustus 2026): SEB AKTIF.** Pengujian langsung pada sandbox course 917 (Quiz `Kuis 1: Konsep Dasar Perencanaan Wilayah`, cmid 6768) menunjukkan formulir pengaturan Quiz memuat fieldset **Safe Exam Browser** dengan pemilih **Require the use of Safe Exam Browser** bernilai `No`, `Yes – Configure manually`, `Yes – Upload my own config`, dan `Yes – Use SEB client config`, beserta sub-pengaturan lengkap (`Show Safe Exam Browser download button`, `Enable quitting of SEB`, `Quit password`, `Show SEB task bar`, `Enable URL filtering`, dan seterusnya).
- Catatan lama bahwa pencarian "safe exam browser" di **Site administration search** tidak menemukan hasil **tetap benar**, tetapi kesimpulan turunannya (SEB kemungkinan tidak aktif) **sudah terbantah**: pengaturan SEB memang tidak muncul di pencarian Site administration karena letaknya di dalam formulir Quiz, bukan sebagai menu tersendiri.
- Dari sisi mahasiswa, kuis dengan SEB aktif tidak lagi menampilkan tombol **Attempt quiz**; yang muncul adalah keterangan bahwa kuis hanya dapat dikerjakan lewat Safe Exam Browser beserta tombol **Download Safe Exam Browser**, **Launch Safe Exam Browser**, dan **Download configuration**.
- **Batas pengujian**: aplikasi SEB itu sendiri tidak dipasang dan tidak dijalankan, sehingga perilaku penguncian layar di dalam aplikasi belum diamati langsung. Yang terverifikasi adalah ketersediaan dan efek pengaturannya di Moodle.
- **Rujukan generik**: [[Code/moodle_docs/Safe_Exam_Browser|Safe_Exam_Browser]], [[Code/moodle_docs/Quiz_settings|Quiz_settings]], [[Code/moodle_docs/Quiz_security|Quiz_security]], dan [[Code/moodle_docs/E-examination_quick_guide|E-examination_quick_guide]].

### 3. Memeriksa & memberi nilai asesmen
- **Tidak ada contoh hidup** (belum ada assignment/quiz di kursus ini untuk dinilai). Antarmuka grading assignment/quiz beserta fitur efisiensi (mis. "quick grading", isi nilai sama untuk beberapa siswa) **perlu diverifikasi terpisah** begitu ada aktivitas nyata.

### 4. Menarik rekapitulasi nilai
- Menu **Grades → Export** (`/grade/export/ods/index.php?id=<course>` dan variannya) menyediakan ekspor ke: **OpenDocument spreadsheet, Plain text, Excel spreadsheet, XML**.
- Opsi ekspor: filter per grup (mis. per kelas RA/RB), pilih item nilai yang disertakan, sertakan feedback atau tidak, kecualikan pengguna suspended, format tampilan nilai (**Real / Percentage / Letter**), dan jumlah desimal.
- Grader report (`/grade/report/index.php?id=<course>`) juga punya menu Setup → Gradebook setup, Course grade settings, Scales, Grade letters, Import.
- Referensi generik: [[Code/moodle_docs/Gradebook|Gradebook]], [[Code/moodle_docs/Grades|Grades]], [[Code/moodle_docs/Grade_export|Grade_export]], [[Code/moodle_docs/Grade_import|Grade_import]]

---

## Knowledge & Community Management

Merujuk kebutuhan [[spec#D-05|D-05]], [[spec#D-06|D-06]], [[spec#M-04|M-04]], serta bagian kalender yang mendukung perjalanan pengguna kedua buku.

### 1. Pemakaian block
- Block yang teramati aktif di **Dashboard**: **Timeline** (daftar aktivitas jatuh tempo) dan **Calendar**.
- Menambah block baru butuh mode edit kursus/dashboard, yang **tidak dicoba** (lihat catatan di bagian Asesmen soal alasan tidak menyalakan edit mode).
- Referensi generik: [[Code/moodle_docs/Blocks|Blocks]]

### 2. Materi untuk berbagai media
- Kursus Statistika saat ini baru punya 1 resource jenis **URL** (link keluar ke modul ajar). Jenis resource/aktivitas lain untuk materi (File, Page, video ter-embed, H5P) **belum teramati langsung** di kursus ini — perlu dicek begitu materi lain ditambahkan atau lewat kursus contoh lain yang sudah lebih terisi.
- Fitur **Content bank** aktif di level kursus (`/contentbank/index.php`) — bisa jadi wadah aset materi yang dipakai ulang lintas aktivitas.

### 3. Organisasi tampilan kursus
- **Format kursus** yang tersedia (Site administration → pengaturan kursus): **Custom sections**, **Weekly sections**, **Single activity**, **Social**. Kursus Statistika memakai **Custom sections** dengan nama section custom: *Kontrak kuliah*, *Materi Ajar*, *Praktikum*, *Tugas dan Penilaian* — bukan format mingguan standar.
- **Hidden sections**: bisa diatur "shown as not available" (terlihat tapi terkunci) atau "completely invisible".
- **Course layout**: satu halaman penuh vs satu section per halaman.
- Toggle lain yang relevan ke UX mahasiswa: **Show gradebook to students** (Ya/Tidak), **Show activity reports**, **Show activity dates**, **Completion tracking** (aktifkan pelacakan penyelesaian aktivitas + tampilkan kondisi penyelesaian ke mahasiswa), **Group mode** (No groups / Separate / Visible).
- Referensi generik: [[Code/moodle_docs/Course_homepage|Course_homepage]], [[Code/moodle_docs/Course_settings|Course_settings]], [[Code/moodle_docs/Activity_completion|Activity_completion]], [[Code/moodle_docs/Course_completion|Course_completion]], [[Code/moodle_docs/Restrict_access|Restrict_access]], [[Code/moodle_docs/Course_formats|Course_formats]]

#### Uji Sandbox 21 Agustus 2026 (course 917, Edit mode)

- **Rename section berhasil**: section default "New section" pada format Custom sections berhasil diubah namanya lewat klik langsung pada judul section (bukan lewat menu Edit) — kotak isian inline muncul dengan petunjuk "Escape to cancel, Enter when finished". Diuji dengan mengganti dua section menjadi `Materi Ajar` dan `Tugas dan Penilaian`.
- **Tombol "+" pada tiap section** membuka menu cepat berisi dua pilihan: **Activity or resource** (membuka dialog penuh) dan **Subsection** (tautan langsung, tanpa dialog). Ini mengonfirmasi subsection adalah warga kelas satu di sisi UI Moodle 5.02 pada instance ini, bukan cuma fitur di dokumentasi generik.
- **Klik "Subsection" belum terbukti berhasil membuat subsection** pada sesi ini — permintaan AJAX pendukungnya (`core_get_string` untuk komponen `subsection`) sempat gagal dengan `ERR_CONNECTION_TIMED_OUT`, memunculkan dialog exception Moodle yang memblokir interaksi lanjutan, dan sesudah itu situs `kuliah2.itera.ac.id` sendiri tidak lagi bisa dijangkau (timeout penuh, bukan 403/error halaman) sementara `docs.moodle.org` dan domain lain tetap normal — mengindikasikan gangguan sisi ITERA yang terpisah dari gangguan Cloudflare `docs.moodle.org`. **Perlu diulang** begitu konektivitas pulih, sebelum menuliskan langkah "Add subsection" sebagai prosedur teruji ke buku.
- **Inventaris nyata "Add an activity or resource" (tab All), tertangkap lewat dialog penuh sebelum gangguan** — ini daftar definitif yang menggantikan status "perlu inventaris" sebelumnya: **Assignment, Book, Choice, Custom certificate, Database, Feedback, File, Folder, Forum, Glossary, H5P, IMS content package, Lesson, Page, Quiz, SCORM package, Text and media area, URL, Virtual programming lab, Wiki, Workshop**. Catatan:
  - **Text and media area** menggantikan **Label** lama (dikonfirmasi juga oleh laman docs.moodle.org yang baru diekstrak, lihat [[Code/moodle_docs/Text_and_media_area|Text_and_media_area]]) — jangan menulis "Label" di buku, pakai nama tampilan ini.
  - **Custom certificate** dan **Virtual programming lab** adalah plugin tambahan khas instance ITERA, tidak ada di korpus `moodle_docs` generik — sebut sebagai "tersedia di kuliah2.itera.ac.id" tanpa merujuk halaman docs.moodle.org untuk keduanya.
  - **LTI External tool** dan **Chat** **tidak muncul** pada daftar ini — jangan menuliskannya sebagai tersedia di instance ITERA.
  - **Quiz** ada di daftar tetapi sengaja tidak dibangun mendalam pada pasangan topik ini (lihat [[spec#D-08|D-08]], pasangan topik 5).
- **Tema gelap/terang**: instance ini punya toggle tema sendiri di navbar (elemen `#toggle-darkmode-input`, kelas `moove-darkmode` pada `<body>`), terpisah dari `prefers-color-scheme` OS/browser — `page.emulateMedia` tidak berpengaruh, harus mengklik togel ini secara eksplisit. Sesi peramban bisa "mewarisi" keadaan gelap dari sesi sebelumnya; periksa kelas `moove-darkmode` pada `<body>` sebelum menangkap layar dan matikan togel bila aktif.

### 4. Integrasi Google Calendar untuk reminder tugas
- **Memungkinkan**, lewat mekanisme standar Moodle: **Calendar → Export calendar** (`/calendar/export.php`) menghasilkan URL feed iCal dinamis (bukan tautan statis) yang otomatis ter-update — bisa dipakai untuk **subscribe** dari Google Calendar ("Add by URL"), bukan integrasi native khusus Google.
- Opsi export: cakupan event (semua / per kategori / per kursus / per grup / event pribadi) dan rentang waktu (minggu ini, bulan ini, 60 hari, atau rentang custom).
- Ada juga **Calendar → Import or export calendars** (`/calendar/managesubscriptions.php`) untuk mengelola langganan kalender eksternal (arahnya kebalikan: mengimpor kalender lain ke Moodle). Saat dicek, belum ada langganan aktif di akun ini.
- Referensi: tidak ada halaman `moodle_docs` spesifik kalender yang sudah diekstrak — perlu ekstraksi tambahan dari docs.moodle.org bila ingin rujukan resmi.

---

## OBE / CPMK

Merujuk kebutuhan eksperimen terpisah setelah [[spec#D-11|D-11]] diuji, serta konteks di [[OBE]], [[CPL-CPMK]], dan [[Penilaian]]. Catatan eksperimennya berada di `eksperimen-obe-cpmk/` dan bukan bagian dari dua PDF pedoman.

**Pertanyaan**: Adakah fitur untuk mengukur CPMK di Moodle kuliah2.itera.ac.id?

**Jawaban singkat: fiturnya ada secara teknis (plugin Competencies bawaan Moodle), tapi belum dipakai/dikonfigurasi sama sekali di instance ITERA.** Ditemukan dua jalur berbeda yang relevan:

### 1. Plugin Competencies (`tool_lp`) — cocok secara struktur, tapi belum dipakai
- Kursus Statistika punya menu **Competencies** di administrasi kursus (`/admin/tool/lp/coursecompetencies.php?courseid=283`), dengan teks bawaan Moodle "Competency ratings in this course are updated immediately in learning plans" — tapi statusnya: **"No competencies have been linked to this course."**
- Dicek di level situs (**Site administration → Competencies frameworks**, `/admin/tool/lp/competencyframeworks.php`): **"No competency frameworks have been created yet."** — jadi bukan cuma kursus Statistika yang belum diisi, **belum ada satupun framework kompetensi dibuat di seluruh instance kuliah2.itera.ac.id**.
- Secara struktur, plugin Competencies Moodle sebenarnya cocok untuk memodelkan CPL→CPMK: framework kompetensi mendukung hierarki induk-anak (persis pola [[CPL-CPMK]]) dan tiap kompetensi bisa ditautkan ke aktivitas/kursus untuk dinilai (rating scale, bukan skor numerik).
- **Keterbatasan plugin ini** untuk kebutuhan ITERA: penilaian Competencies berbasis *rating scale* (mis. skala penguasaan), **bukan pembobotan persentase** seperti model di [[_assets/Penilaian|Penilaian]] (tiap bentuk penilaian per CPMK punya bobot % yang dijumlah 100%). Jadi meski framework CPL/CPMK dibuat di sini, agregasi nilai akhir tetap perlu dihitung lewat Gradebook (lihat poin 2), bukan lewat plugin Competencies itu sendiri.
- Untuk benar-benar memakainya, perlu langkah admin situs: membuat competency framework (kemungkinan oleh admin LMS pusat/prodi, bukan dosen per mata kuliah), lalu tiap dosen menautkan CPMK relevan ke kursusnya.

### 2. Grade categories di Gradebook — jalur praktis yang sudah bisa dipakai dosen sendiri
- Halaman **Gradebook setup** (`/grade/edit/tree/index.php?id=283`) mengonfirmasi Gradebook Moodle mendukung **"Add category"** dengan kolom **Weights** dan pilihan **Aggregation** (kursus Statistika saat ini masih default "Natural", belum ada kategori/item dibuat).
- Ini artinya dosen **bisa** membuat satu grade category per CPMK (mis. `CPMK-a-1`, `CPMK-b-1`, `CPMK-b-2` sesuai kodifikasi di [[CPL-CPMK]]), memasukkan tiap bentuk penilaian ([[Penilaian#Bentuk Penilaian|Bentuk Penilaian]]) sebagai grade item di dalamnya, lalu mengatur **Aggregation** ke *Weighted mean of grades* dan bobot per item — meniru persis tabel bobot di [[Penilaian#Kolom Penilaian dalam Materi Per Pekan|Penilaian]] (`a + b + c = 100`).
- Jalur ini **tidak butuh setup admin situs** — sepenuhnya bisa dilakukan dosen sendiri lewat Gradebook setup kursusnya, jadi lebih praktis untuk direkomendasikan di pedoman dibanding menunggu framework Competencies dibuat.

### Rekomendasi untuk pedoman akhir
Sarankan dua opsi ke pembaca pedoman: (a) **jalur cepat/praktis** — pakai grade category per CPMK dengan aggregation berbobot di Gradebook, bisa langsung dikerjakan sendiri; (b) **jalur ideal jangka panjang** — usulkan ke admin LMS ITERA agar dibuatkan competency framework CPL/CPMK resmi di level situs, supaya pelacakan CPMK across-kursus (bukan cuma dalam satu mata kuliah) bisa memakai fitur Competencies/Learning Plans bawaan Moodle.

---

## Jejak Digital

Merujuk kebutuhan [[spec#D-09|D-09]] dan [[spec#D-13|D-13]].

### 1. Melihat aktivitas peserta kelas (sudut pandang dosen)
- **Konfirmasi role-gating**: menu **Reports** (course administration) muncul di navigasi kursus Statistika (Pak Abdul = Teacher di sana), tapi **tidak muncul sama sekali** di navigasi kursus AIE (`id=673`) tempat Pak Abdul berperan sebagai **Student**. Jadi menu di bawah ini murni sudut pandang dosen/pengajar, bukan mahasiswa.
- Isi menu **Reports** (`/report/view.php?courseid=<id>`): **Competency breakdown**, **Logs**, **Live logs**, **Activity report**, **Course participation**, **Activity completion**, **Statistics**.
- **Logs** (`/report/log/index.php?id=<id>`): form filter dengan pilihan **Select a course**, **Select a group**, **Select a user** (untuk kursus Statistika saat ini cuma berisi "All participants", Pak Abdul sendiri, dan "Guest user" — karena memang baru dia satu-satunya peserta), **Date** (per hari), **Activities**, **Actions**. Ini jalur paling spesifik untuk menjawab "siapa membuka apa, kapan" — termasuk kebutuhan pemeriksaan pada [[spec#D-09|D-09]], asalkan difilter ke aktivitas dan rentang tanggal yang tepat.
- **Live logs**: versi sama tapi real-time (aktivitas 1 jam terakhir).
- **Course participation**: laporan per-aktivitas siapa yang sudah/belum berpartisipasi (submit/view) — cocok untuk cek massal "siapa yang belum buka materi/tugas X", bukan cuma satu-per-satu lewat Logs.
- **Keterbatasan**: karena kursus contoh nyaris kosong (cuma 1 partisipan, tanpa aktivitas asesmen sungguhan), tampilan **hasil** laporan (baris log/partisipasi sungguhan) belum bisa diverifikasi langsung — baru menu, opsi filter, dan struktur formulirnya yang terkonfirmasi hidup di instance ini.

### 2. Log aktivitas bertahan setelah unenrol? (kekhawatiran dari sistem lama)
Ditemukan tiga fakta yang saling melengkapi soal ini:

1. **Status enrolment punya dua mode, bukan cuma enrolled/unenrolled**: filter "Status" di halaman Participants (`/user/index.php?id=<id>`) punya opsi **Active** dan **Inactive** — ini mode *suspend* bawaan Moodle (menonaktifkan akses tanpa menghapus keanggotaan), terpisah dari **Unenrol** (menghapus total).
2. **Unenrol memang destruktif terhadap data kursus**: [[Code/moodle_docs/Manual_enrolment|Manual_enrolment]] (dokumentasi resmi yang sudah diekstrak) secara eksplisit menyebutkan opsi aksi expiry "*Unenrol user from course* **purges grades, group memberships, preferences and other user related data from the courses**" — ini mengonfirmasi keluhan dosen di sistem lama bukan bug, tapi memang perilaku standar Moodle.
3. **Dropdown "Select a user" di Logs diisi dari daftar partisipan yang sedang aktif**, bukan dari riwayat log independen — dicek langsung di kursus Statistika, dropdown itu cuma berisi peserta yang *sedang* terdaftar. Artinya begitu seorang mahasiswa di-*unenrol* penuh, kemungkinan besar dia juga hilang dari dropdown ini, sehingga log lamanya jadi sulit dicari lewat menu kursus meski datanya mungkin masih tersimpan di database.

**Rekomendasi (belum diuji ujung-ke-ujung — perlu konfirmasi Pak Abdul/admin LMS di kursus yang benar-benar berpenghuni)**: untuk mahasiswa yang lulus/keluar tapi jejak aktivitasnya masih ingin dilacak, pakai **Suspend** (ubah Status jadi Inactive) alih-alih **Unenrol** penuh. Suspend mempertahankan keanggotaan di Participants (bisa disaring lewat filter Status supaya tidak mengganggu tampilan harian) sekaligus memblokir akses masuk mahasiswa tsb — dan karena berbagi sumber data yang sama dengan filter Logs/Course participation, semestinya mahasiswa itu tetap bisa dipilih & ditelusuri di laporan-laporan tersebut. Unenrol penuh sebaiknya disimpan untuk kondisi butuh "bersih-bersih" data (mis. akhir siklus akreditasi), bukan sebagai langkah rutin akhir semester.

---

## Kekhususan Instance ITERA vs `docs.moodle.org` Generik

- Tema/branding: judul situs "**New E-Learning Institut Teknologi Sumatera**", ada elemen kustom seperti course image/banner per kursus.
- Label peran diterjemahkan & disesuaikan konteks lokal: "Dosen Pengembang MK (Course creator)", "Dosen (Teacher)", "Dosen tamu (Non-editing teacher)", "Mahasiswa (Student)" — bukan label default Moodle berbahasa Inggris.
- Struktur kategori kursus mengikuti struktur akademik ITERA (Fakultas → Program Studi, plus kategori administratif seperti "Tahap Persiapan Bersama" dan "MKWI").
- Fitur **Report builder** / **Custom reports** (`/reportbuilder/`) muncul di navigasi global — ini fitur Moodle 4.4+ yang tidak selalu aktif di semua instance, dan belum ada dokumentasi generiknya di `moodle_docs`.
- Kode mata kuliah memakai format `[PRODI][TAHUN]-[NOMOR]` (contoh: `PL25-12001`).

## Keterbatasan Eksplorasi

- Kursus contoh (Statistika) masih **hampir kosong** — belum ada quiz/assignment/forum sungguhan, sehingga banyak detail Asesmen (jenis Activity aktual, pengaturan SEB, alur grading) **belum bisa diverifikasi langsung** dan perlu eksplorasi susulan begitu kursus sudah lebih terisi, atau eksplorasi ke kursus lain milik Pak Abdul yang sudah aktif dipakai.
- Tidak mencoba menyalakan mode edit kursus (untuk melihat dialog "Add an activity or resource" atau menambah block) karena itu aksi yang mengubah state produksi, di luar izin sesi ini.
- `admin/modules.php` (daftar modul aktivitas terpasang) tidak bisa diakses — akun ini bukan admin situs penuh.
- Tidak masuk ke kursus dosen lain yang terlihat di `course/management.php`, meski secara teknis akun ini punya visibilitas ke sana — di luar cakupan izin ("mata kuliah statistika" saja) dan demi privasi dosen lain.
- Mekanisme manajemen mahasiswa lulus/mahasiswa baru per semester belum teramati (kursus contoh cuma punya 1 partisipan).
