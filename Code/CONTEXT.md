---
type: context
project: moodle-manual
stage: source-acquisition
title: Kontrak Pengadaan Sumber Moodle
description: Kontrak untuk memperoleh, membersihkan, mendokumentasikan, dan memeriksa sumber Moodle lokal.
tags:
  - itera
  - icm
  - moodle
---

# Kontrak Pengadaan Sumber Moodle

Satu pekerjaan: memperoleh atau memperbaiki sumber lokal yang diperlukan oleh penulis pedoman. Jangan mengekstraksi ulang korpus jika laman yang dibutuhkan sudah tersedia dan masih memadai.

## Asal korpus `moodle_docs`

Direktori ini lahir dari keterbatasan pengetahuan saat penyusunannya. Ketika korpus mulai dikumpulkan (Juli 2026), penyusun belum tahu bahwa ada cara kerja bernama *browsing agent*: otomasi browser yang bekerja bersama manusia, memakai sesi Chrome sungguhan, sehingga tantangan Cloudflare cukup diselesaikan sekali secara manual lalu laman diekstrak langsung. Yang terbayang saat itu hanyalah API resmi plus nilai cookie `cf_clearance` yang harus diperbarui berkala, dan itulah jalur yang dipakai (arsipnya di [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/_archive/cookie-cf-clearance/_index|arsip alur lama]]).

Sejak September 2026 alur itu ditinggalkan: `method_claude.py` meminjam sesi Chrome lewat CDP, penyusun menyelesaikan captcha sekali, lalu laman diekstrak langsung. Korpus di direktori ini karena itu bukan lagi jalur utama — ia dipertahankan sebagai rujukan yang sudah terperiksa dan sebagai jejak bagaimana pedoman ini disusun, serta tidak diterbitkan ke GitHub (lihat `.gitignore`).

## Masukan

- Kerja: daftar laman pada `@for_teacher.txt`, `@assignments.txt`, atau `@quiz_seb.txt`, sesuai tugas aktif.
- Kerja: skrip ekstraksi yang disebut oleh [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/_index\|Code/_index]].
- Rujukan: [[aturan-pemrograman]].
- Rujukan: dokumentasi skrip yang namanya sama dengan skrip dan berekstensi `.md`.

Jangan muat: seluruh `moodle_docs/`, seluruh proyek `cdp-web-scrape/`, atau berkas arsip cookie dan identitas browser jika tugas tidak memerlukannya.

## Proses

1. Periksa [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/moodle_docs/_index\|indeks korpus Moodle]] untuk memastikan sumber belum tersedia.
2. Pilih jalur akuisisi yang paling sempit: MediaWiki API lewat sesi Chrome CDP untuk dokumentasi Moodle (pengguna menyelesaikan captcha Cloudflare sekali di jendela Chrome; skrip meminjam sesi browser itu) atau CDP untuk eksplorasi situs Moodle ITERA yang sudah memiliki sesi masuk.
3. Simpan hasil sebagai berkas Markdown dan aset gambar yang dapat diperiksa manusia.
4. Perbarui dokumentasi skrip jika perilaku kode berubah.
5. Perbarui `_index.md` hanya jika struktur atau daftar artefak penting pada tingkat tersebut berubah.

## Keluaran

- Dokumentasi Moodle generik → `moodle_docs/`
- Temuan situs Moodle ITERA → [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/KULIAH2|KULIAH2]]
- Dokumentasi kode → berkas `.md` di samping skrip terkait
- Catatan pembelajaran pemrograman web → [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/LEARN|LEARN]]

## Pemeriksaan Manusia

Pengguna membuka satu hasil Markdown dan aset gambarnya, lalu memastikan isi dapat dibaca, tautan lokal bekerja, dan sumber tersebut memang menjawab kebutuhan bagian pedoman sebelum hasil diteruskan ke `Guide`.
