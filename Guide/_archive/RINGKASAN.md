---
type: historical-summary
project: moodle-manual
status: archived
as-of: 2026-07-09
---

# Arsip Ringkasan dan Daftar Pekerjaan 9 Juli 2026

> [!IMPORTANT]
> Berkas ini mempertahankan keadaan proyek pada 9 Juli 2026 dan bukan sumber status aktif. Keputusan tentang font Abadi, Carlito untuk judul, dan kewajiban memperbarui `_log.md` di bawah sudah digantikan. Baca [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/CONTEXT|Guide/CONTEXT]] dan periksa artefak di `pedoman/` untuk mengetahui keadaan terbaru.

## Ringkasan Pekerjaan (2026-07-09)

1. **Struktur naskah disepakati**: panduan akhir ditulis sebagai satu proyek **Quarto book** di [[pedoman/_index|pedoman]] (bukan dokumen `.qmd` terpisah), supaya referensi silang otomatis `@sec-...` antarbab bisa bekerja dan bernomor benar. Alur kerja disepakati satu bab dulu untuk direview sebelum lanjut, dan tautan referensi di naskah akhir memakai URL internet (`docs.moodle.org`), bukan path file lokal.
2. **Bab 1 Kepesertaan ditulis penuh**: membuat mata kuliah, meng-*enroll* mahasiswa per kelas (manual/self enrolment + Groups/Groupings), meng-*assign* dosen dan asisten, serta manajemen mahasiswa lulus/baru. Bab 2–5 (Knowledge & Community Management, Asesmen, Jejak Digital, OBE/CPMK) masih kerangka judul dengan label `#sec-...` final.
3. **Gambar placeholder** dibuat otomatis (Python + Pillow) untuk tiap referensi `![...](images/...)` supaya render PDF (LaTeX) tidak gagal karena file gambar belum ada — menunggu diganti tangkapan layar asli oleh Pak Abdul.
4. **Disesuaikan ulang ke [[spec.md]]**: ditemukan ketentuan font (heading **Abadi**, body **Carlito**, monospace **JetBrains Mono**) belum diterapkan. Carlito & JetBrains Mono terpasang di sistem dan sudah dikonfigurasi; **font Abadi tidak ditemukan** di sistem ini sama sekali — untuk sementara `sansfont` (heading) memakai Carlito juga, tinggal diganti satu baris di `_quarto.yml` begitu Abadi terpasang.
5. **Reorganisasi bab**: konten "Suspend vs Unenrol" yang tadinya ditulis penuh di Bab 1 dipindah jadi isi utuh di Bab 4 Jejak Digital (`@sec-suspend-vs-unenrol`) supaya tidak berulang; urutan Bab 2 dan 3 ditukar (Knowledge & Community Management sebelum Asesmen) mengikuti alur semester materi-dulu-baru-dinilai.
6. PDF berhasil dirender ulang di tiap tahap, referensi silang terverifikasi benar (tidak ada tanda `??`) lewat `pdftotext`, dan font terverifikasi ter-*embed* lewat `pdffonts`.

Rincian lengkap tiap langkah ada di [[pedoman/_log|pedoman/_log]].

## To-Do List

### Menunggu Pak Abdul pada 9 Juli 2026
- [ ] Review isi & gaya Bab 1 **Kepesertaan** ([[pedoman/01-kepesertaan.qmd|01-kepesertaan]]) sebelum bab-bab lain ditulis penuh.
- [ ] Pasang font **Abadi** (biasanya dari instalasi Microsoft Office/365) di sistem, supaya `sansfont` di [[pedoman/_quarto.yml|_quarto.yml]] bisa diganti dari Carlito ke Abadi.
- [ ] Ganti gambar *placeholder* di `pedoman/images/**/*.png` dengan tangkapan layar asli dari kuliah2.itera.ac.id — nama file sudah disiapkan mengikuti isi teks, tidak perlu ubah naskah lagi.

### Menunggu giliran ditulis pada 9 Juli 2026
- [ ] Tulis penuh Bab 2 **Knowledge & Community Management** ([[pedoman/02-knowledge-community.qmd|02-knowledge-community]]).
- [ ] Tulis penuh Bab 3 **Asesmen** ([[pedoman/03-asesmen.qmd|03-asesmen]]) — termasuk panduan semua jenis Activity, Safe Exam Browser, tips efisiensi grading, dan rekapitulasi nilai.
- [ ] Tulis penuh sisa Bab 4 **Jejak Digital** bagian "Melihat Aktivitas Peserta Kelas" ([[pedoman/04-jejak-digital.qmd|04-jejak-digital]]) — menu Reports/Logs/Live logs/Course participation. Bagian Suspend vs Unenrol sudah selesai.
- [ ] Tulis penuh Bab 5 **OBE / CPMK** ([[pedoman/05-obe-cpmk.qmd|05-obe-cpmk]]) — plugin Competencies vs grade categories berbobot.

### Prosedur berulang yang berlaku pada 9 Juli 2026
- [ ] Render ulang PDF (`quarto render --to pdf` di `Guide/pedoman`) dan verifikasi referensi silang lewat `pdftotext` (tidak ada tanda `??`).
- [ ] Perbarui [[pedoman/_index|pedoman/_index]] dan [[pedoman/_log|pedoman/_log]] sesuai [[07 APAPUN DICOBA/Moodle Docs (manual)/AGENTS-MOODLE-MANUAL|AGENTS-MOODLE-MANUAL]].
