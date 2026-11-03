# Kontribusi dan Konvensi Commit

Berkas ini berlaku untuk repo `panduan-kuliah2-itera` dan mengikat manusia maupun agen yang membuat commit di dalamnya.

Sumber kebenaran proyek adalah vault OneDrive `Moodle Docs (manual)`; repo GitHub hanya cerminnya. Suntingan selalu lahir di vault, lalu dicerminkan ke repo. Skrip pencermin `sync-ke-github.ps1` tidak diterbitkan (lihat `.gitignore`), dan panduan penggunaannya ada di `sync-ke-github.md` pada mesin penyusun.

## Alur kerja

1. Sunting berkas di vault OneDrive.
2. Cerminkan ke repo — jalankan `sync-ke-github.ps1 -Coba` lebih dahulu bila ingin melihat dampaknya sebelum menyalin.
3. Stage dan commit **per maksud** di repo; jangan memakai `git add -A` untuk pekerjaan yang bercampur.
4. Dorong dengan `git push` biasa.

Jangan menambah berkas yang hanya ada di repo: robocopy `/MIR` akan menghapusnya pada sinkronisasi berikutnya. Atas alasan yang sama, jangan menyunting salinan di repo untuk isi yang juga hidup di vault — suntingan itu akan tertimpa.

## Format pesan

```
<tipe>(<lingkup>): <ringkasan imperatif, maks 72 kolom>

Mengapa perubahan ini ada — konteks yang tidak terbaca dari diff.

Dampak/rujukan: berkas, keluaran, atau isu terkait.
```

| Tipe | Dipakai untuk |
| --- | --- |
| `feat` | Kemampuan atau isi baru pada pedoman |
| `fix` | Koreksi isi, langkah, atau hasil render yang salah |
| `docs` | Naskah, kontrak kerja, katalog, dan dokumentasi |
| `chore` | Kebersihan repo: `.gitignore`, pelacakan berkas, berkas perkakas |
| `refactor` | Penataan ulang tanpa mengubah hasil |
| `build` | Konfigurasi Quarto, templat Typst, dan hasil render |
| `revert` | Pembatalan commit sebelumnya |

| Lingkup | Wilayah |
| --- | --- |
| `guide`, `guide/dosen`, `guide/mahasiswa` | Naskah pedoman |
| `code`, `ekstraktor` | Perkakas dan korpus di `Code/` |
| `git` | Kebijakan penerbitan, `.gitignore`, konvensi |
| `arsip`, `akar` | `_archive/`, `_assets/`, dan berkas akar |

## Delapan aturan commit

1. **Satu commit satu maksud.** Bila subjek memerlukan kata "dan" untuk menjelaskan, pecah menjadi dua commit.
2. **Subjek imperatif**, maksimum 72 kolom, tanpa titik akhir: `tambahkan`, bukan `menambahkan` atau `sudah ditambahkan`.
3. **Badan menjelaskan mengapa**, bukan apa. Diff sudah menjelaskan apa yang berubah.
4. **Jangan mencampur perubahan mekanis dengan perubahan makna.** Render ulang, pemformatan, dan penggantian nama berdiri sendiri, atau menempel pada commit yang menghasilkannya.
5. **Artefak bangunan ikut commit sumbernya.** PDF di `Guide/_book/` di-commit bersama perubahan `.qmd` yang menghasilkannya agar keduanya tidak pernah berbeda versi.
6. **Penyaringan dan pelepasan pelacakan satu paket.** Menambahkan pola `.gitignore` untuk berkas yang sudah terlacak wajib disertai `git rm --cached` pada commit yang sama; tanpa itu repo berhenti dalam keadaan setengah jalan.
7. **Setiap commit dapat di-`revert` sendirian** tanpa merusak perubahan lain.
8. **Bahasa Indonesia**, istilah teknis boleh tetap Inggris. Riwayat commit menggantikan berkas `_log.md`, jadi tulislah untuk pembaca enam bulan kemudian.

## Contoh

Benar:

```
docs(guide): tambahkan subbagian Group overrides pada Assignment

Tenggat berbeda antar kelas paralel sebelumnya dijelaskan sebagai
Grant extension, padahal mekanismenya berbeda. Subbagian baru
memisahkan keduanya dan menautkan ulang bagian Grant extension.

Dampak: Guide/dosen/04-organisasi-materi-dan-asesmen.qmd,
Guide/_book/Panduan-Moodle-ITERA.pdf
```

Salah:

```
update

- banyak perubahan
- tambah gambar
- hapus berkas
```
