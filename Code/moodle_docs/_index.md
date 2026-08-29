# Indeks Direktori moodle_docs

Dokumen indeks yang menjelaskan isi dari direktori `moodle_docs` — hasil ekstraksi Markdown laman-laman [docs.moodle.org/502](https://docs.moodle.org/502/en/Main_page) menggunakan [[method_claude.py]] (sebagian laman pasangan topik 3 diambil manual lewat sesi CDP karena `curl_cffi` masih tertantang Cloudflare — lihat [[HANDOFF-SISA-TUGAS]]), mencakup pengaturan kursus, jenis-jenis resource, enrolment, grading, berbagai jenis aktivitas Moodle, restrict access, serta pengaturan ujian dengan Safe Exam Browser.

## Direktori

- `images`: kumpulan 205 berkas tangkapan layar dan ikon (PNG) yang dirujuk oleh berkas-berkas Markdown di direktori ini

## File

- [[2D_3D_structure_display_short_answer.md]]: Jenis soal Quiz short answer dengan MarvinSketch/MarvinView untuk konten 2D/3D
- [[360-degree_feedback_module.md]]: Plugin aktivitas 360-degree feedback (multi-rater) dari atasan, kolega, dan bawahan
- [[Activities.md]]: Daftar 15 jenis aktivitas standar Moodle beserta ringkasan dan tautan tiap jenis
- [[Activity_completion.md]]: Fitur activity completion — kriteria penyelesaian aktivitas dan dropdown "To do" bagi siswa
- [[Adding_a_new_course.md]]: Cara menambah kursus baru oleh Administrator, Course Creator, atau Manager
- [[Assignment.md]]: Aktivitas Assignment — submit tugas siswa, grading, dan rubrik
- [[Assignment_settings.md]]: Seluruh opsi pengaturan aktivitas Assignment (Allow submissions from, Due date, dll.) serta pengaturan Site administration terkait
- [[Authentication.md]]: Metode autentikasi login Moodle (manual, no login, self-registration, dll.)
- [[Badges.md]]: Fitur badge/lencana pencapaian (site badge dan course badge)
- [[BigBlueButton.md]]: Aktivitas video conference BigBlueButton untuk kelas daring
- [[Block_settings.md]]: Cara menambah blok, mengatur block actions/permissions, dan membuat blok "sticky" di berbagai konteks (situs, kursus, aktivitas)
- [[Blocks.md]]: Blok pada sisi halaman Moodle (block drawer, blok sticky, dll.)
- [[Book.md]]: Resource Book — halaman/bab multi-halaman dengan daftar isi, mendukung multimedia (isi sama dengan [[Book_resource.md]])
- [[Book_resource.md]]: Resource Book — halaman/bab multi-halaman dengan daftar isi, mendukung multimedia (isi sama dengan [[Book.md]])
- [[Building_Quiz.md]]: Menyusun isi kuis — menambah soal, mengatur halaman, bobot, dan urutan acak
- [[Calendar.md]]: Fitur kalender — event situs/kursus/grup/pengguna, termasuk deadline assignment dan quiz
- [[Choice_activity.md]]: Aktivitas Choice — polling/voting dengan pilihan radio button
- [[Course_completion.md]]: Fitur dan laporan penyelesaian kursus (course completion)
- [[Course_formats.md]]: Format tampilan kursus (Single activity, Social, Topics, Weekly, dll.) dan cara memilihnya
- [[Course_homepage.md]]: Bagian-bagian tampilan halaman utama kursus (navigasi, course index, dll.)
- [[Course_settings.md]]: Pengaturan kursus (nama, format, dan opsi umum lainnya)
- [[Database.md]]: Halaman disambiguasi topik "Database" (activity module, autentikasi/enrolment eksternal, skema DB Moodle)
- [[Database_activity.md]]: Aktivitas Database — membangun, menampilkan, dan mencari bank entri record
- [[E-examination_quick_guide.md]]: Panduan cepat ujian daring (sumatif) dengan Quiz + Safe Exam Browser
- [[Enrolment_methods.md]]: Ringkasan metode-metode enrolment yang tersedia dalam kursus (manual, self, guest, dll.)
- [[External_tool.md]]: Halaman LTI External tools — menambah dan mengelola tool eksternal di kursus
- [[Feedback_activity.md]]: Aktivitas Feedback — survei evaluasi kursus atau pengajar
- [[File.md]]: Resource File — mengunggah dan menampilkan berkas apa pun sebagai materi (isi sama dengan [[File_resource.md]])
- [[File_resource.md]]: Resource File — mengunggah dan menampilkan berkas apa pun sebagai materi (isi sama dengan [[File.md]])
- [[Folder.md]]: Resource Folder — menampilkan beberapa berkas sekaligus, bisa unggah individual atau folder zip (isi sama dengan [[Folder_resource.md]])
- [[Folder_resource.md]]: Resource Folder — menampilkan beberapa berkas sekaligus, bisa unggah individual atau folder zip (isi sama dengan [[Folder.md]])
- [[Forum.md]]: Aktivitas Forum — diskusi berbasis thread (isi sama dengan [[Forum_activity.md]])
- [[Forum_activity.md]]: Aktivitas Forum — diskusi berbasis thread (isi sama dengan [[Forum.md]])
- [[Glossary.md]]: Aktivitas Glossary — daftar istilah kolaboratif seperti kamus (isi sama dengan [[Glossary_activity.md]])
- [[Glossary_activity.md]]: Aktivitas Glossary — daftar istilah kolaboratif seperti kamus (isi sama dengan [[Glossary.md]])
- [[Gradebook.md]]: Grader report — kumpulan nilai semua aktivitas yang dinilai dalam kursus
- [[Grades.md]]: Indeks topik terkait nilai (grading guide, grader report, grade settings, dll.)
- [[Grade_export.md]]: Cara mengekspor nilai (Excel, ODS, teks polos, XML, atau publish via URL)
- [[Grade_import.md]]: Cara mengimpor nilai (CSV, XML, atau tempel dari spreadsheet)
- [[Groupings.md]]: Fitur grouping — kumpulan grup dalam kursus untuk mengarahkan tugas ke beberapa grup sekaligus
- [[Groups.md]]: Fitur group — alasan penggunaan dan level-level grup dalam kursus
- [[Guest_access.md]]: Metode enrolment guest access — melihat konten kursus tanpa dapat berpartisipasi
- [[H5P_activity.md]]: Aktivitas H5P — konten interaktif dari Content bank atau h5p.com
- [[IMS_content_package.md]]: Resource IMS content package — memuat materi format standar IMS Content Packaging dari sumber lain
- [[Lesson.md]]: Aktivitas Lesson — halaman bercabang berdasarkan respons siswa (isi sama dengan [[Lesson_activity.md]])
- [[Lesson_activity.md]]: Aktivitas Lesson — halaman bercabang berdasarkan respons siswa (isi sama dengan [[Lesson.md]])
- [[LTI_External_tool_activity.md]]: Cara menambahkan aktivitas LTI External tool ke dalam kursus
- [[Manual_enrolment.md]]: Plugin enrolment manual oleh admin atau guru
- [[Page.md]]: Resource Page — laman teks/media yang dibuat lewat text editor (isi sama dengan [[Page_resource.md]])
- [[Page_resource.md]]: Resource Page — laman teks/media yang dibuat lewat text editor (isi sama dengan [[Page.md]])
- [[Quiz.md]]: Aktivitas Quiz — dari soal pilihan ganda sederhana hingga self-assessment kompleks (isi sama dengan [[Quiz_activity.md]])
- [[Quiz_activity.md]]: Aktivitas Quiz — dari soal pilihan ganda sederhana hingga self-assessment kompleks (isi sama dengan [[Quiz.md]])
- [[Quiz_FAQ.md]]: Tanya-jawab praktis seputar Quiz (guest, uji coba, tampilan hasil, kasus-kasus khusus)
- [[Quiz_reports.md]]: Laporan hasil kuis — grades, responses, statistics, dan manual grading
- [[Quiz_security.md]]: Pengamanan ujian di luar SEB serta batasan yang tidak bisa dilakukan dari sisi server
- [[Quiz_settings.md]]: Seluruh opsi pengaturan aktivitas Quiz, termasuk bagian Safe Exam Browser
- [[Resources.md]]: Ringkasan jenis-jenis resource Moodle (Book, File, Folder, IMS content package, Page, Text and media area, URL)
- [[Restrict_access.md]]: Fitur restrict access — membatasi ketersediaan aktivitas/section berdasarkan kondisi tertentu
- [[Restrict_access_settings.md]]: Seluruh opsi kondisi Restrict access (activity completion, tanggal, nilai, grup, profil pengguna) serta perbedaan ikon mata terbuka/tertutup
- [[Safe_Exam_Browser.md]]: Peramban ujian terkunci (SEB) — fitur, opsi "Require the use of Safe Exam Browser", berkas konfigurasi, dan templat
- [[SCORM_activity.md]]: Aktivitas SCORM — paket konten e-learning standar SCORM/AICC
- [[Self_enrolment.md]]: Metode self enrolment — siswa mendaftar sendiri ke kursus, opsional dengan enrolment key
- [[Teacher_quick_guide.md]]: Panduan cepat fitur-fitur Moodle bagi pengguna dengan peran Teacher
- [[Teacher_role.md]]: Penjelasan hak dan batasan peran Teacher dalam kursus
- [[Text_and_media_area.md]]: Resource Text and media area — menampilkan teks dan multimedia langsung di halaman kursus
- [[URL.md]]: Resource URL — tautan web sebagai resource kursus (isi sama dengan [[URL_resource.md]])
- [[URL_resource.md]]: Resource URL — tautan web sebagai resource kursus (isi sama dengan [[URL.md]])
- [[Using_restrict_access.md]]: Contoh praktis penerapan Restrict access — rangkaian aktivitas kondisional, kondisi ALL/ANY (OR/eitheror)
- [[Wiki_activity.md]]: Aktivitas Wiki — dokumen kolaboratif mirip Wikipedia
- [[Workshop.md]]: Aktivitas Workshop — peer assessment antar siswa (isi sama dengan [[Workshop_activity.md]])
- [[Workshop_activity.md]]: Aktivitas Workshop — peer assessment antar siswa (isi sama dengan [[Workshop.md]])
