# Indeks Direktori Code

Dokumen indeks yang menjelaskan isi dari direktori `Code` yang digunakan untuk menyimpan skrip otomasi dan dokumen pendukung alur kerja.

## Direktori

- `contoh-learn`: Contoh kode latihan pemrograman (menghitung rata-rata list) yang dipisahkan dari [[LEARN.md]], berisi `rata-rata.py` dan dokumentasinya `rata-rata.md`
- `moodle_docs`: Hasil ekstraksi Markdown dari [[method_claude.py]] — kumpulan laman docs.moodle.org (pengaturan kursus, enrolment, grading, aktivitas kuis/forum/wiki/dll., serta pengaturan ujian dengan Safe Exam Browser) beserta subdirektori `images` untuk berkas tangkapan layar pendukung, dijelaskan dalam [[Code/moodle_docs/_index]]
- `cdp-web-scrape`: Proyek/eksperimen terpisah (repositori git sendiri) untuk scraping berbasis Chrome DevTools Protocol (CDP) + Google Sheets pada portal SIAKAD ITERA; independen dari alur kerja ekstraksi Moodle Docs dan mengikuti konvensi dokumentasinya sendiri (`README.md`, `CLAUDE.md`)
- `cdp-kuliah2-explore`: Hasil penggandaan `cdp-web-scrape`, diadaptasi untuk menjelajahi `kuliah2.itera.ac.id` (instance Moodle ITERA) lewat sesi Chrome CDP yang sudah login SSO manual — bukan scraping tabel, melainkan dump satu halaman per panggilan ([[07 APAPUN DICOBA/Moodle Docs (manual)/Code/kuliah2-explore/explore_kuliah2.py|explore_kuliah2.py]]) sebagai bahan penelaahan untuk `Guide/KULIAH2.md`; mengikuti konvensi dokumentasinya sendiri (`README.md`, `CLAUDE.md`, `GEMINI.md`)

## File

- [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/CONTEXT]]: kontrak pengadaan sumber yang menetapkan kapan ekstraksi diperlukan, masukan yang boleh dimuat, keluaran, dan pemeriksaan manusia
- [[LEARN.md]]: Catatan pembelajaran berjenjang (Tingkat 0-5) dari nol pengetahuan web programming sampai memahami seluruh [[method_claude.py]] — dasar internet & HTTP, API vs scraping, proteksi Cloudflare (_fingerprint_ & _TLS fingerprint_), bekal Python, dan rangkuman alur ujung ke ujung
- [[RINGKASAN.md]]: Ringkasan temuan uji coba (2026-07-06) mengenai proteksi Cloudflare dan usulan pemanfaatan MediaWiki API
- [[SARAN_AGY.md]]: Saran pendekatan proyek dari Antigravity, mencakup bypass Cloudflare via remote debugging, MediaWiki API, dan optimalisasi Obsidian
- [[SARAN_CLAUDE.md]]: Ulasan dan tanggapan asisten Claude terhadap berkas [[RINGKASAN.md]]
- [[method_claude.py]]: Skrip Python ekstraktor dokumentasi Moodle 502 (MediaWiki API → unduh gambar → tulis ulang tautan → konversi pandoc → Markdown), implementasi dari [[SARAN_CLAUDE.md]]
- [[method_claude.md]]: Dokumentasi kode untuk [[method_claude.py]] (Ringkasan + diagram mermaid + penjelasan baris-per-baris)
- [[method_claude_quarto.py]]: Skrip Python ekstraktor dokumentasi Quarto (quarto.org/docs/guide/, discovery via sidebar → unduh gambar → tulis ulang tautan → konversi pandoc → Markdown), keluarannya ditulis langsung ke `how-to-quarto/` di root repo (menggantikan dokumentasi manual versi lama, kini di `how-to-quarto/_arsip-manual-lama/`)
- [[method_claude_quarto.md]]: Dokumentasi kode untuk [[method_claude_quarto.py]] (Ringkasan + diagram mermaid + penjelasan baris-per-baris + cara menjalankan)
- [[for_teacher.txt]]: Daftar judul laman docs.moodle.org terkait pengorganisasian kelas oleh dosen (course setup, enrolment, grading, tracking, restrict access), untuk dipakai dengan `--pages-file` di [[method_claude.py]]
- [[assignments.txt]]: Daftar judul laman docs.moodle.org untuk jenis-jenis aktivitas Moodle (BigBlueButton, Choice, Database, Feedback, Forum, Glossary, H5P, Lesson, LTI, SCORM, Wiki, Workshop), untuk dipakai dengan `--pages-file` di [[method_claude.py]]
- [[quiz_seb.txt]]: Daftar judul laman docs.moodle.org terkait pengaturan ujian dengan Safe Exam Browser beserta rumpun Quiz pendukungnya (Quiz settings, Quiz security, E-examination quick guide, Quiz FAQ, Building Quiz, Quiz reports), untuk dipakai dengan `--pages-file` di [[method_claude.py]]
- [[pedoman_rebuild_sources.txt]]: Daftar sempit 19 judul kandidat docs.moodle.org yang belum tersedia dalam korpus lokal dan diperlukan untuk pembangunan ulang pedoman—resources, Assignment settings, peran, kalender/laporan, kelompok mandiri, dan prosedur badges—untuk dipakai dengan `--pages-file` di [[method_claude.py]]; judul yang belum didukung tautan silang lokal harus diverifikasi oleh API saat ekstraksi
- [[cookie.txt]]: Nilai cookie `cf_clearance` (Cloudflare) yang diperlukan `build_session()` di [[method_claude.py]] agar lolos proteksi bot; diperbarui berkala saat kedaluwarsa
- [[navigator.userAgent.txt]]: Catatan waktu pengambilan dan nilai `navigator.userAgent` browser, dipakai sebagai argumen `--user-agent` di [[method_claude.py]] agar cocok dengan [[cookie.txt]]
- [[coba mermaid script.md]]: Draf uji coba sintaks diagram mermaid, cikal bakal diagram yang dipakai di `contoh-learn/rata-rata.md`
- [[2026-07-07-result.md]]: Ringkasan sesi debugging 403 (bug format `cookie.txt`, temuan `Cf-Mitigated: challenge` yang mengindikasikan fingerprint TLS, opsi lanjutan `curl_cffi` vs remote debugging Chrome/CDP)
- [[2026-07-08-success-report.md]]: Laporan sukses ekstraksi end-to-end pertama (implementasi `curl_cffi` Opsi A, perbaikan `API_URL` wiki farm, pembersihan HTML sisa MediaWiki via `clean_soup()`)
- [[convert_to_markdown.py]]: Skrip Python ekstraktor laman Google Cloud Learn (`cloud.google.com/learn`) menjadi berkas Markdown utuh lengkap dengan metadata, struktur judul, daftar, tabel, tautan, dan gambar
- [[convert_to_markdown.md]]: Dokumentasi kode untuk [[convert_to_markdown.py]] (Ringkasan + diagram mermaid + penjelasan baris-per-baris)
- [[what-is-artificial-intelligence.md]]: Hasil ekstraksi Markdown utuh dari laman `https://cloud.google.com/learn/what-is-artificial-intelligence?hl=id`
- [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/_index|_index]]: katalog struktur direktori `Code`
