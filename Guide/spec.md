---
type: specification
project: moodle-manual
title: Spesifikasi Pedoman Penggunaan kuliah2.itera.ac.id
description: Ketentuan muatan minimal dan bentuk keluaran pedoman Moodle ITERA.
tags:
  - itera
  - moodle
---

# Spesifikasi Pedoman Penggunaan `kuliah2.itera.ac.id`

## Pengguna Sasaran

Pedoman ditujukan kepada dosen, asisten pengajar, dan mahasiswa ITERA. Pembaca harus dapat menjalankan prosedur tanpa pengetahuan teknis tentang administrasi Moodle.

### Dosen dan Asisten

Pedoman harus menjelaskan perjalanan pengguna berikut. Sistematika penyajian dibebaskan. ID kebutuhan bersifat stabil dan dipakai oleh [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/matriks-pemenuhan|matriks pemenuhan]] serta catatan pengujian.

#### D-01

Masuk ke situs.

#### D-01A

Membuat mata kuliah (kursus) sendiri di Moodle, sebelum mengelola isinya. ID ini semula terlewat dari spec; dikonfirmasi pengguna pada 22 Agustus 2026 bahwa setiap dosen — bukan hanya admin LMS atau pengelola prodi — dapat membuat kursusnya sendiri.

#### D-02

Membuat kelas paralel & membuatkan mahasiswa kelompok *custom* untuk pengerjaan tugas.

#### D-03

Meng-*enroll* mahasiswa baik oleh dosen maupun mahasiswa sendiri.

#### D-04

Menetapkan dosen lain dan asisten sebagai pengajar.

#### D-05

Mengorganisasi tampilan kelas dengan *section*, *subsection* dan *block*, termasuk jenis-jenis fitur yang relevan dan contoh penggunaannya.

#### D-06

Mengunggah bahan ajar, termasuk penjelasan seluruh jenis *resources* dan contoh penggunaannya yang relevan.

#### D-07

Membuat asesmen tugas, termasuk penjelasan seluruh jenis *activities* dan contoh penggunaannya yang relevan.

#### D-08

Membuat asesmen ujian dengan Safe Exam Browser.

#### D-09

Memeriksa kelengkapan pengumpulan tugas.

1. Melihat kapan pengumpulan tugas untuk mengetahui keterlambatan.
2. Saya pernah dapat info bahwa Moodle juga memungkinkan pengajar untuk melihat kapan mahasiswa membuka panduannya. Ini juga perlu dibahas.

#### D-10

Memberi nilai untuk tugas dan ujian.

#### D-11

Mengunduh/menghimpun nilai asesmen tugas & ujian untuk diolah dengan spreadsheet secara mandiri.

#### D-12

Membuat sistem hadiah dengan *Badges*.

#### D-13

Penjelasan fitur-fitur di *More* dan kasus penggunaannya yang relevan.

1. Abaikan jika ada fitur yang sudah dijelaskan pada kegiatan-kegiatan yang diminta di atas.

> [!important]- Penting
> Cari juga bagaimana mengintegrasikan sistem [[_assets/OBE|OBE]] dengan fitur `kuliah2.itera.ac.id`. Tapi fokusnya ini eksperimental, jadi output-nya terpisah dengan pedoman yang asli.

### Asisten

Asisten pada hakikatnya adalah mahasiswa yang diberikan penugasan membantu dosen pada mata kuliah tertentu. Kewenangan asisten dibatasi secara tegas pada:

#### A-01

Mengenali peran dan batasan antarmuka akun asisten (*Non-editing teacher*).

#### A-02

Membantu mengunggah materi modul dan panduan praktikum pada bagian (*section*) yang disiapkan dosen.

#### A-03

Memeriksa hasil pekerjaan peserta pada *Assignment* dan *Quiz*, memberikan nilai (*grading*), dan menuliskan catatan umpan balik (*feedback comments*).

#### A-04

Memantau rekapitulasi buku nilai (*Grades*) serta memeriksa log aktivitas peserta (*Reports → Logs*).

### Mahasiswa

#### M-01

Masuk ke situs.

#### M-02

Bergabung ke kelas paralel.

#### M-03

Membuat kelompok *custom* sendiri untuk pengerjaan tugas.

#### M-04

Mengenal berbagai jenis *resources* dan *activities* dan cara penggunaannya.

#### M-05

Cara mengumpulkan tugas.

#### M-06

Cara mengoperasikan ujian yang menggunakan Safe Exam Browser.

#### M-07

Cara melihat nilai tugas.

## Bentuk Keluaran

- Sumber ditulis sebagai satu proyek Quarto terpadu di `Guide/` dengan fitur `PART` (Bagian I: Dosen, Bagian II: Asisten, Bagian III: Mahasiswa); menghasilkan satu dokumen PDF gabungan.
- Eksperimen OBE/CPMK ditulis terpisah di `eksperimen-obe-cpmk/` dan belum menjadi produk PDF.
- Setiap prosedur yang bergantung pada antarmuka harus dilengkapi tangkapan layar dari `kuliah2.itera.ac.id`.
- Tangkapan layar harus menampilkan area yang relevan, menyamarkan data pribadi jika ada, dan memiliki keterangan yang menjelaskan tindakan pembaca.
- Tipografi mengikuti [[DESIGN]]: Playfair Display untuk judul, Carlito untuk teks isi, dan JetBrains Mono untuk kode atau teks teknis.
- Bahasa mengikuti [[TONE]] dan mengutamakan kalimat Indonesia yang baku, langsung, serta bebas jargon yang tidak diperlukan.
- Dilengkapi lembar pengesahan resmi berformat ITERA dengan nama dan jabatan pejabat pengesah (*placeholder*).

## Kebijakan Sumber

1. Utamakan sumber yang sudah tersimpan dalam [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/moodle_docs/_index\|korpus Moodle lokal]].
2. Jika sumber yang dibutuhkan belum tersedia, ekstrak hanya laman yang relevan dari dokumentasi resmi `docs.moodle.org` melalui MediaWiki API dan simpan ke korpus lokal sebelum dipakai.
3. Jangan menggunakan sumber internet selain dokumentasi resmi `docs.moodle.org`.
4. Gunakan [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/KULIAH2\|KULIAH2]] dan hasil uji kursus sandbox untuk membedakan perilaku generik Moodle dari keadaan situs Moodle ITERA.
5. Jangan menyatakan fitur tersedia pada situs Moodle ITERA jika temuan lokal atau hasil uji sandbox belum membuktikannya.

## Kriteria Selesai

Satu bagian dianggap selesai jika prosedurnya lengkap, sumber lokalnya dapat ditelusuri, tangkapan layarnya cocok dengan langkah, hasil PDF telah diperiksa secara visual, dan pengguna dapat menjalankan prosedurnya tanpa menebak tindakan berikutnya.
