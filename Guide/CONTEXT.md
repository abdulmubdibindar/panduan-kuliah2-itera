---
type: context
project: moodle-manual
stage: guide-authoring
title: Kontrak Pembangunan Ulang Pedoman Moodle ITERA
description: Kontrak untuk mengembangkan dua buku secara paralel, menjaga keterlacakan, menguji sandbox, dan memeriksa PDF per pasangan topik.
tags:
  - itera
  - icm
  - moodle
---

# Kontrak Pembangunan Ulang Pedoman Moodle ITERA

Satu pekerjaan: mengubah kebutuhan dan sumber lokal menjadi satu buku pedoman terpadu yang dapat dijalankan tanpa menebak langkahnya—terbagi menjadi tiga bagian (Dosen, Asisten, dan Mahasiswa). Eksperimen OBE/CPMK tetap terpisah dan ditunda sampai pengujian Gradebook selesai.

## Masukan

- Kerja: [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/spec\|spec]].
- Kerja: [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/KULIAH2\|KULIAH2]].
- Status: [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/matriks-pemenuhan\|matriks pemenuhan]].
- Rujukan: [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/moodle_docs/_index\|indeks korpus Moodle]].
- Rujukan sesuai topik: [[07 APAPUN DICOBA/Moodle Docs (manual)/_assets/_index\|indeks bahan akademik]].
- Rujukan bahasa dan visual: [[TONE]] dan [[DESIGN]].

Jangan muat: seluruh korpus Moodle atau seluruh `_assets/`. Mulailah dari indeks, lalu buka hanya sumber yang menjawab bagian yang sedang ditulis.

## Proses dan Gerbang

1. Pilih satu pasangan topik sesuai urutan pada [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/matriks-pemenuhan#Gerbang Pasangan Topik\|gerbang pasangan topik]]. Jangan membuka pasangan berikutnya sebelum pengguna menyetujui pasangan aktif.
2. Mulai dari indeks korpus. Jika sumber belum tersedia, ekstrak hanya laman yang relevan dari `docs.moodle.org` melalui MediaWiki API lewat sesi Chrome CDP (lihat [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/method_claude.md\|method_claude]]); jangan memakai domain internet lain.
3. Cocokkan dokumentasi generik dengan temuan `KULIAH2` dan uji tiga peran di kursus sandbox. Semua perubahan situs dibatasi pada sandbox; kursus aktif hanya boleh dibaca.
4. Tulis bagian dosen, asisten, dan mahasiswa secara konsisten. Setiap prosedur memuat prasyarat, jalur menu, langkah bernomor, hasil yang terlihat, cabang ketika hasil berbeda, batas kewenangan, dan tindakan berikutnya.
5. Ambil tangkapan layar lokal pada ukuran konsisten, pangkas ke area tindakan, samarkan data pribadi, beri label stabil, dan rujuk secara eksplisit dari teks.
6. Perbarui matriks pemenuhan berdasarkan artefak yang benar-benar ada. Fitur yang belum terbukti tetap ditandai belum terverifikasi.
7. Bangkitkan satu dokumen PDF gabungan, serahkan kepada pengguna untuk diperiksa dan disetujui.

## Keluaran

- Proyek Quarto terpadu → `Guide/_quarto.yml`
- Naskah Bagian I (Dosen) → `dosen/`
- Naskah Bagian II (Asisten) → `asisten/`
- Naskah Bagian III (Mahasiswa) → `mahasiswa/`
- PDF terpadu → `_book/Panduan-Moodle-ITERA.pdf`
- Catatan eksperimen, tanpa PDF → `eksperimen-obe-cpmk/`
- Aset bersama nonprosedural → `_shared/` dan `assets/`

## Pemeriksaan Manusia

Untuk setiap pasangan topik, pengguna menjalankan sekurang-kurangnya satu prosedur dosen/asisten dan satu prosedur mahasiswa sambil membandingkannya dengan tangkapan layar. Persetujuan atau koreksinya dicatat pada matriks sebelum bagian dianggap selesai.
