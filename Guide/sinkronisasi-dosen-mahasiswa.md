---
type: audit
project: moodle-manual
title: Audit Sinkronisasi Panduan Dosen ↔ Mahasiswa
description: Pemetaan tiap bagian buku dosen ke padanannya di buku mahasiswa, beserta celah yang perlu ditulis.
date: 2026-08-27
tags:
  - itera
  - moodle
  - audit
---

# Audit Sinkronisasi Panduan Dosen ↔ Mahasiswa

Dokumen ini memetakan setiap bagian buku dosen ke padanannya di buku mahasiswa. Tujuannya memastikan setiap tindakan dosen yang berdampak pada layar mahasiswa punya penjelasan di sisi mahasiswa, sehingga kedua pihak memakai `kuliah2.itera.ac.id` dengan pemahaman yang sama.

Status yang dipakai:

| Status        | Arti                                                                            |
| ------------- | ------------------------------------------------------------------------------- |
| **ADA**       | Sudah sinkron; istilah dan alurnya cocok.                                       |
| **KURANG**    | Sudah disinggung tetapi terlalu dangkal, tersebar, atau istilahnya belum cocok. |
| **TIDAK ADA** | Berdampak nyata pada mahasiswa tetapi belum dibahas sama sekali.                |
| **N/A**       | Murni kewenangan dosen; mahasiswa tidak perlu tahu prosedurnya.                 |

Keadaan per 24 Agustus 2026, setelah restrukturisasi bab 1–2 dosen dan pembenahan buku mahasiswa.

## Bab 1 — Masuk dan Mengenali Antarmuka

| Bagian dosen                         | Dampak yang dilihat mahasiswa                              | Counterpart mahasiswa                            | Status  |
| ------------------------------------ | ---------------------------------------------------------- | ------------------------------------------------ | ------- |
| 1.1 Masuk ke New E-Learning ITERA    | Alur SSO yang sama persis                                  | 1.2 Masuk ke Moodle ITERA                        | **ADA** |
| 1.2 Mengenali tampilan antarmuka     | Menu navigasi teratas yang sama, minus Site administration | 1.3 Mengenali tampilan antarmuka                 | **ADA** |
| 1.2.1 My courses                     | Laman pertama setelah login, tanpa tombol Create course    | 1.3.1 My courses                                 | **ADA** |
| 1.2.2 Dashboard                      | Timeline dan Calendar yang sama                            | 1.3.2 Dashboard                                  | **ADA** |
| 1.2.3 Home                           | Beranda situs yang sama                                    | 1.3.x Home (paragraf baru)                       | **ADA** |
| 1.2.4 Site administration            | Menu ini tidak ada pada layar mahasiswa                    | Disebut sebagai perbedaan peran di callout 1.3.3 | **N/A** |
| 1.2.5 Menu akun dan preferensi       | Menu akun identik                                          | 1.3.4 Menu akun dan preferensi                   | **ADA** |
| 1.3 Keluar dari New E-Learning ITERA | Prosedur keluar dan batas waktu sesi yang sama             | 1.4 Keluar dengan aman                           | **ADA** |

## Bab 2 — Membuat dan Membuka Mata Kuliah

| Bagian dosen                                                                                           | Dampak yang dilihat mahasiswa                                      | Counterpart mahasiswa                                                     | Status                                         |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------- | ---------------------------------------------- |
| 2.1 Membuat mata kuliah baru                                                                           | Tidak ada; mahasiswa hanya menerima hasilnya                       | —                                                                         | **N/A**                                        |
| 2.1.1 Pengaturan lanjutan → **Show gradebook to students**                                             | Menu **Grades** bisa tidak muncul sama sekali bagi mahasiswa       | Callout di 4.5 _Melihat nilai dan umpan balik tugas_                      | **ADA**                                        |
| 2.1.1 Pengaturan lanjutan → **Maximum upload size**                                                    | Unggahan tugas ditolak karena berkas terlalu besar                 | Disinggung sebagai gejala di tabel 4.1                                    | **ADA**                                        |
| 2.1.1 Pengaturan lanjutan → **Number of announcements**, **Force language**, **Show activity reports** | Blok pengumuman, bahasa antarmuka, dan laporan aktivitas sendiri   | Callout di 3.1 _Memahami susunan materi_                                  | **ADA**                                        |
| 2.1.1 Pengaturan lanjutan → **Group mode**                                                             | Menentukan apakah mahasiswa melihat anggota kelompok lain          | 2.4 _Memeriksa keanggotaan_, baris "Hanya kelompok sendiri yang terlihat" | **ADA**                                        |
| 2.2 Membuka mata kuliah                                                                                | Halaman mata kuliah, indeks kursus, area utama                     | 1.3.3 Halaman mata kuliah                                                 | **ADA**                                        |
| 2.3 Penjelasan menu-menu mata kuliah                                                                   | Menu mata kuliah versi mahasiswa (tanpa Settings, tanpa Edit mode) | 1.3.3, satu paragraf ringkas + callout perbedaan peran                    | **ADA**                                        |
| 2.3.4 Grades (di dalam mata kuliah)                                                                    | Mahasiswa melihat nilainya sendiri di sini                         | 4.5 Melihat nilai dan umpan balik tugas                                   | **ADA** — sebagian M-07 sudah tertutup di sini |

## Bab 3 — Kepesertaan, Kelas Paralel, dan Peran

| Bagian dosen                                    | Dampak yang dilihat mahasiswa                                          | Counterpart mahasiswa                                  | Status  |
| ----------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------ | ------- |
| 3.1 Menetapkan dosen lain dan asisten           | Muncul nama asisten di Participants; asisten dapat melihat pengumpulan | —                                                      | **N/A** |
| 3.2.1 Membuat kelas paralel dengan Groups       | Mahasiswa masuk `Kelas RA`/`RB`                                        | 2.4 Memeriksa keanggotaan kelas paralel atau kelompok  | **ADA** |
| 3.2.2 Mengizinkan mahasiswa mendaftar sendiri   | Mahasiswa memakai _enrolment key_                                      | 2.2 Bergabung melalui pendaftaran mandiri              | **ADA** |
| 3.2.3 Membuat kelompok tugas secara otomatis    | Mahasiswa tiba-tiba berada di kelompok yang tidak ia pilih             | 2.5 Membentuk kelompok tugas secara mandiri            | **ADA** |
| 3.2.4 Mendaftarkan mahasiswa secara manual      | Mahasiswa terdaftar tanpa pernah memasukkan kunci apa pun              | Callout di 2.2 _Bergabung melalui pendaftaran mandiri_ | **ADA** |
| 3.3 Menggabungkan beberapa group dalam Grouping | Kegiatan tertentu hanya terbuka bagi _grouping_ tertentu               | Tabel istilah 2.1 + paragraf penutup 2.4               | **ADA** |

## Bab 4 — Organisasi Mata Kuliah, Bahan Ajar, dan Asesmen

| Bagian dosen                                  | Dampak yang dilihat mahasiswa                                | Counterpart mahasiswa                                     | Status                                               |
| --------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------- | ---------------------------------------------------- |
| 4.1.1 Section dan Subsection                  | Susunan halaman mata kuliah                                  | 3.1 Memahami susunan materi dan jenis sumber belajar      | **ADA**                                              |
| 4.1.2 Blocks                                  | Blok yang muncul di sisi halaman mata kuliah mahasiswa       | Paragraf baru di 3.1 _Memahami susunan materi_            | **ADA**                                              |
| 4.2.1 Taksonomi lengkap activities            | Mahasiswa menghadapi Forum, Quiz, Choice, Workshop, H5P, dll | 3.2 Mengenal jenis kegiatan (_Activities_)                | **ADA**                                              |
| 4.2.2 Memilih activities untuk bahan ajar     | Jenis bahan yang ditemui mahasiswa                           | Tabel jenis bahan ajar di 3.1                             | **ADA**                                              |
| 4.2.3 Memilih activities untuk asesmen        | Mahasiswa mengerjakan asesmen selain Assignment              | 3.2, kolom "Yang diharapkan dari Anda"                    | **ADA**                                              |
| 4.2.4 Membuat Quiz dan mengisi bank soal      | Mahasiswa mengerjakan kuis berisi soal dari bank soal        | 4.4 Mengerjakan kuis dan ujian daring (_Quiz_)            | **ADA**                                              |
| 4.2.5 Mengatur Safe Exam Browser untuk ujian  | Mahasiswa harus meluncurkan SEB untuk ujian                  | 4.4 Mengerjakan kuis dan ujian daring (_Quiz_)            | **ADA** — ditulis pada P5, 24 Agustus 2026           |
| 4.3 Mengatur visibilitas dan pembatasan akses | Materi kelabu dengan keterangan `Not available unless: ...`  | Gejala + tindakan dipindahkan ke tabel dan callout di 3.1 | **ADA** — sengaja diringkas atas permintaan pengguna |

## Bab 5 — Pemantauan Pengumpulan dan Jejak Aktivitas

| Bagian dosen                                             | Dampak yang dilihat mahasiswa                                                  | Counterpart mahasiswa                                         | Status  |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------- | ------- |
| 5.1 Memeriksa status dan kelengkapan pengumpulan         | Tidak terlihat mahasiswa                                                       | —                                                             | **N/A** |
| 5.2 Memantau tabel pengumpulan dan penanda keterlambatan | Penanda `late`/`early` yang juga dilihat mahasiswa                             | 4.2 Memahami tabel status penyerahan tugas                    | **ADA** |
| 5.3 Mengatur perpanjangan waktu (_Grant Extension_)      | Mahasiswa melihat `Extension granted until ...` dan tenggat pribadinya berubah | Callout di 4.2 _Memahami tabel status penyerahan tugas_       | **ADA** |
| 5.4 Melacak riwayat pembukaan materi (_Reports & Logs_)  | Seluruh aktivitas mahasiswa tercatat dan dapat dibaca dosen                    | Callout "Aktivitas Anda tercatat beserta cap waktunya" di 3.2 | **ADA** |

## Rekapitulasi

Keadaan setelah prioritas 1, 2, P5, dan celah prioritas 3 ditutup pada 27 Agustus 2026:

| Status    | Jumlah |
| --------- | -----: |
| ADA       |     28 |
| KURANG    |      0 |
| TIDAK ADA |      0 |
| N/A       |      4 |

## Celah yang sudah ditutup

Prioritas 1 dan 2 sudah ditulis seluruhnya:

| Celah                                           | Tempatnya sekarang                                                                                                          |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Grant extension                                 | Callout di `pengumpulan-tugas.qmd` §Memahami tabel status penyerahan tugas                                                  |
| Reports & Logs                                  | Callout di `materi-dan-aktivitas.qmd` §Mengenal jenis kegiatan                                                              |
| Grades mata kuliah + Show gradebook to students | Bagian baru `pengumpulan-tugas.qmd` §Melihat nilai dan umpan balik tugas, dengan tangkapan layar `nilai/01-user-report.png` |
| Jenis Activities                                | Bagian baru `materi-dan-aktivitas.qmd` §Mengenal jenis kegiatan, tabel sembilan jenis                                       |
| Didaftarkan secara manual                       | Callout di `bergabung-dan-kelompok.qmd` §Bergabung melalui pendaftaran mandiri                                              |
| Grouping                                        | Paragraf penutup `bergabung-dan-kelompok.qmd` §Memeriksa keanggotaan                                                        |

Prioritas 3 ditutup pada 27 Agustus 2026:

| Celah                                                                             | Tempatnya sekarang                                                                              |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Home** (dari 1.2.3)                                                             | Heading baru `### Home` di `login-dan-orientasi.qmd` + baris tabel yang merujuk ke sana         |
| **Blocks** (dari 4.1.2)                                                           | Paragraf baru tentang blok di `materi-dan-aktivitas.qmd` §Memahami susunan materi               |
| **Number of announcements / Force language / Show activity reports** (dari 2.1.1) | Callout `tip` di `materi-dan-aktivitas.qmd` §Memahami susunan materi                            |
| **Peringatan batas waktu sesi**                                                   | Callout `warning` di `login-dan-orientasi.qmd` §Keluar dengan aman (diadaptasi dari buku dosen) |

Catatan untuk pekerjaan M-07 nanti: bagian §Melihat nilai dan umpan balik tugas sudah menutup pembacaan **User report** dan pengaturan **Show gradebook to students**. Kalau M-07 dikerjakan sebagai topik penuh, perluas bagian itu — jangan menulis ulang dari nol.

## Celah yang masih terbuka

Tidak ada lagi bagian berstatus **KURANG** atau **TIDAK ADA**. Seluruh celah sinkronisasi sudah tertutup.
