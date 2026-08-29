# Saran Claude terhadap RINGKASAN.md

Dokumen ini berisi tanggapan dan saran terhadap [`RINGKASAN.md`](./RINGKASAN.md) untuk proyek ekstraksi dokumentasi Moodle 502 menjadi Markdown (panduan Moodle ITERA).

## Yang sudah bagus

- **Diagnosis akar masalah tepat.** Membedakan "Captcha mustahil" vs "headless terdeteksi" itu penting dan menjawab langsung kebingungan di [`CONTEXT.md`](./CONTEXT.md) ("Anda kok bisa?").
- **Insight kunci** — docs.moodle.org itu MediaWiki, jadi tak perlu scrape DOM penuh — adalah pergeseran strategi yang benar dan menghemat banyak kerja refactor.
- **Tabel endpoint** ringkas dan langsung dapat ditindaklanjuti.

## Saran perbaikan (paling penting dulu)

### 1. Asumsi cookie `cf_clearance` "sekali tembus" terlalu optimistis
Langkah 1 di "Usulan Alur Kerja" menyiratkan challenge cukup ditembus sekali lalu aman. Kenyataannya `cf_clearance`:
- terikat pada **IP + User-Agent** — jika salah satu berubah, cookie batal;
- **kedaluwarsa** (biasanya menit–jam, bukan permanen).

**Saran:** tulis eksplisit bahwa cookie punya masa berlaku, dan skrip loop harus **berhenti anggun + minta refresh cookie** kalau tiba-tiba dapat 403 di tengah jalan. Ini mencegah loop panjang gagal senyap.

### 2. Ada celah besar: gambar belum disebut sama sekali
Panduan Moodle penuh screenshot antarmuka. `api.php?action=parse&prop=text` mengembalikan HTML dengan `<img src="/...">` relatif. Kalau tidak diunduh, panduan jadi teks tanpa gambar.

**Saran:** tambahkan satu langkah di alur kerja — **unduh aset gambar + tulis ulang path-nya jadi lokal** (mis. ke folder `attachments/` atau `images/`). Ini keputusan arsitektur, bukan detail teknis, jadi layak masuk ringkasan.

### 3. Tautan internal antar-halaman juga perlu ditulis ulang
HTML hasil parse berisi link `/502/en/Nama_Halaman`. Setelah jadi kumpulan Markdown lokal, link itu akan mati.

**Saran:** perlu langkah normalisasi link → path Markdown relatif (atau format wiki-link `[[Nama Halaman]]` kalau memang dibaca di Obsidian — folder ini punya `.obsidian`, layak dipertimbangkan). Sebutkan minimal sebagai to-do.

### 4. Untuk daftar halaman, pakai API, jangan scrape `Special:AllPages`
Baris tabel menyandingkan keduanya seolah setara. `Special:AllPages` adalah halaman HTML (kena challenge, perlu paginasi manual). Lebih bersih:
```
api.php?action=query&list=allpages&aplimit=500&format=json
```
lalu lanjut via parameter `apcontinue`. Rekomendasikan yang API secara tegas.

### 5. Tambahkan catatan sopan-santun (rate limiting)
Loop unduh ratusan halaman tanpa jeda bisa memicu blokir lebih agresif. Cukup satu kalimat: beri **delay antar-request** + set **User-Agent identifikatif**.

## Saran redaksional

- **Judul "Temuan Uji" beri tanggal versi** — sudah ada (2026-07-06), bagus; pertahankan pola ini kalau ada uji lanjutan.
- **"Pertanyaan Terbuka" poin 2 (cakupan)** adalah keputusan paling menentukan effort. Naikkan jadi keputusan pertama yang diminta ke Abdul, karena menentukan apakah butuh loop penuh atau cukup ekstraksi terarah (mis. mulai dari halaman indeks peran pengajar lalu telusuri link sedalam 2–3 level). Cakupan "seluruh 502" itu ribuan halaman teknis yang tak relevan untuk dosen.

## Rekomendasi atas pertanyaan terbuka

- **Sumber konten:** HTML terender via `pandoc` (poin #1 di tabel) — lebih baik daripada wikitext mentah, karena tabel & struktur langsung rapi tanpa harus membersihkan sintaks template `{{...}}`.
- **Uji coba dulu:** Ya. PoC 1 halaman (mis. `Teacher_quick_guide`) menembus challenge lewat browser asli → unduh via API → pandoc → cek hasil, **termasuk uji unduh 1 gambar**, sebelum bangun skrip penuh.
