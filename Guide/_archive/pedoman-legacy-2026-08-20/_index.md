# Indeks Direktori Guide/pedoman

Proyek Quarto book berisi naskah panduan akhir penggunaan Moodle ITERA. Susunan satu proyek book membuat referensi silang otomatis (`@sec-...`) antar-bab memperoleh nomor bab yang benar dalam PDF akhir; keputusan awalnya tersimpan dalam [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/pedoman/_log|arsip log]]. Sumber kontennya adalah [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/KULIAH2|KULIAH2]] sebagai temuan situs Moodle ITERA dan `Code/moodle_docs` sebagai dokumentasi generik Moodle, sesuai [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/spec|spec]].

## Direktori

- `images`: Gambar tangkapan layar tiap bab, termasuk *placeholder* yang dibuat otomatis untuk tiap referensi gambar di berkas `.qmd` selama tangkapan layar asli belum tersedia (path mengikuti pola `images/<nama-bab>/<nama-file>.png`)
- `_book`: Direktori keluaran hasil `quarto render` (PDF, dsb.) — dihasilkan otomatis, jangan diedit manual, aman dihapus dan di-render ulang kapan saja

## File

- `@_quarto.yml`: konfigurasi proyek Quarto book yang menetapkan urutan bab, bahasa Indonesia, format tanggal, Playfair Display untuk judul, Carlito untuk teks isi, JetBrains Mono untuk teks teknis, serta keluaran PDF
- `@index.qmd`: Bab Pendahuluan (`.unnumbered`) yang menjelaskan cara membaca panduan, dasar penyusunan, dan konvensi *placeholder* tangkapan layar
- `@01-kepesertaan.qmd`: Bab **Kepesertaan** yang sudah berisi prosedur utama pengelolaan peserta, grup, dosen, dan asisten
- `@02-knowledge-community.qmd`: Bab **Knowledge & Community Management** yang masih berupa kerangka
- `@03-asesmen.qmd`: Bab **Asesmen** yang masih berupa kerangka
- `@04-jejak-digital.qmd`: Bab **Jejak Digital**; bagian menjaga jejak mahasiswa yang lulus atau keluar sudah terisi, sedangkan bagian aktivitas peserta masih berupa kerangka
- `@05-obe-cpmk.qmd`: Bab **OBE/CPMK** yang masih berupa kerangka
- [[07 APAPUN DICOBA/Moodle Docs (manual)/Guide/pedoman/_index|_index]]: katalog struktur direktori `Guide/pedoman`
