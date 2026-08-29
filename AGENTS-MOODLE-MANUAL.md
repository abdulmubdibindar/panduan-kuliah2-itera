---
type: agent-profile
project: moodle-manual
title: AGENTS-MOODLE-MANUAL
description: Berkas entri, perutean, dan kontrak kerja proyek pedoman Moodle ITERA.
tags:
  - itera
  - icm
  - moodle
---

# Proyek Pedoman Moodle ITERA

Subproyek ini mengolah dokumentasi Moodle dan temuan dari `kuliah2.itera.ac.id` menjadi pedoman penggunaan Moodle untuk dosen, asisten, dan mahasiswa di ITERA. Struktur folder membawa konteks; berkas ini menjadi kontrak kerja tingkat akar, sedangkan `CONTEXT.md` di tiap wilayah menjadi kontrak wilayahnya.

Satu pekerjaan utama: menghasilkan pedoman PDF yang menjelaskan penggunaan `kuliah2.itera.ac.id` berdasarkan kebutuhan lokal ITERA, temuan pada situs yang digunakan, dan dokumentasi resmi Moodle yang sudah tersimpan secara lokal.

## Perutean

| Ketika mengerjakan... | Baca dahulu | Bakuan yang wajib dipakai |
| --- | --- | --- |
| Memahami alur dan status proyek | Berkas ini, bagian [Bentuk Ruang Kerja](#bentuk-ruang-kerja) dan [Status](#status) | `icm-architecture` untuk perubahan arsitektur ruang kerja |
| Mengekstraksi atau memperbaiki sumber Moodle | [Code/CONTEXT.md](Code/CONTEXT.md) | [[aturan-pemrograman]]; `penulisan-prosedur` untuk instruksi yang dijalankan pengguna |
| Menulis atau merevisi pedoman | [Guide/CONTEXT.md](Guide/CONTEXT.md) dan [Guide/spec.md](Guide/spec.md) | `penulisan-quarto`; `penulisan-prosedur`; `playwright-cli` untuk tangkapan layar |
| Menavigasi bahan akademik lokal | [_assets/_index.md](_assets/_index.md) | Muat hanya rujukan yang disebut kontrak tahap |
| Menavigasi isi proyek | [_index.md](_index.md) | *Jump, Don't Crawl* |

## Bentuk Ruang Kerja

Ruang kerja ini merupakan alur pengetahuan dengan dua wilayah yang saling menyerahkan hasil kerja:

1. `Code` memperoleh dan merawat korpus referensi Moodle.
2. `Guide` menelaah kebutuhan, menyusun naskah, mengambil tangkapan layar, dan merender pedoman.

Kedua wilayah tidak diberi nomor karena ekstraksi tidak harus diulang setiap kali satu bagian pedoman direvisi. Urutan kerja ditentukan oleh kesiapan masukan pada kontrak masing-masing, bukan oleh asumsi bahwa seluruh ekstraksi selalu dimulai dari awal.

## Masukan Bersama

- Referensi lokal Moodle: `Code/moodle_docs/`
- Temuan situs Moodle ITERA: [Guide/KULIAH2.md](Guide/KULIAH2.md)
- Kebutuhan keluaran: [Guide/spec.md](Guide/spec.md)
- Konteks akademik: `_assets/`
- Gaya bahasa dan desain: [[TONE]] serta [[DESIGN]]

## Keluaran Utama

- Sumber Quarto: `Guide/`
- Hasil render: `Guide/_book/Panduan-Moodle-ITERA.pdf`

## Status

Tentukan status dengan memeriksa artefak di `Guide/` dan hasil render di `Guide/_book/`. Permukaan status yang aktif adalah [Guide/matriks-pemenuhan.md](Guide/matriks-pemenuhan.md); keadaan berkas yang sebenarnya tetap menjadi sumber status utama.

## Pemeriksaan Pengguna

Pengguna memeriksa struktur, ketepatan langkah, dan kecocokan tangkapan layar pada satu bagian pedoman sebelum bagian tersebut dianggap selesai atau dipakai sebagai dasar bagian berikutnya.

## Aturan yang Berlaku

- Ikuti [[TONE]] untuk komunikasi dan [[DESIGN]] untuk identitas visual.
- Setiap dokumen baru mengikuti ketentuan format dari [[AGENTS]] akar ITERA.
- Jangan memuat seluruh korpus `Code/moodle_docs`; buka indeksnya, lalu baca hanya laman yang relevan dengan bagian yang sedang ditulis.
- Jangan melanjutkan ke tahap berikutnya sebelum pengguna memeriksa keluaran tahap aktif.
- `_index.md` adalah katalog struktur, bukan tempat menyimpan uraian kerja.
- **Jangan membuat atau memperbarui berkas `_log.md`.** Riwayat perubahan proyek ini dipegang riwayat commit git; gunakan `git log` untuk menelusurinya.

## Debugging Kolaboratif

Jika pengguna mengatakan *libatkan saya*, *biarkan saya ikut menangani*, atau *saya ingin nyemplung*, ikuti siklus debugging pada [[aturan-pemrograman]]: jelaskan diagnosis, berikan satu tindakan yang dapat dicoba pengguna, lalu periksa hasilnya setelah pengguna berkata "sudah, lalu?".
