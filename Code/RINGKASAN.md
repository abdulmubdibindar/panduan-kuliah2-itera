# Ringkasan Temuan & Usulan Alur Kerja

## Konteks
Tujuan: mengekstraksi laman [dokumentasi Moodle 5.02](https://docs.moodle.org/502/en/Main_page) menjadi berkas Markdown untuk panduan penggunaan Moodle ITERA.

## Temuan Uji (2026-07-06)
1. **Bukan Captcha biasa.** Situs dilindungi proteksi bot ala Cloudflare ("Moodle challenge").
2. **Setiap HTTP polos (`curl`) → 403 "Moodle challenge".** Inilah yang menjebak Playwright kemarin.
3. **Playwright gagal karena terdeteksi otomatis/headless**, bukan karena Captcha mustahil dipecahkan.
4. **`WebFetch` tembus** hanya karena lewat server pengambil tepercaya — bukan "memecahkan" Captcha.
5. **docs.moodle.org adalah situs MediaWiki** → ada endpoint konten murni, tak perlu scrape DOM penuh.

## Endpoint MediaWiki yang Tersedia
| Endpoint | Hasil | Catatan |
|---|---|---|
| `?action=raw` | wikitext mentah | ringkas, tapi ada sintaks template |
| `api.php?action=parse&prop=text` | HTML isi saja (tanpa navbar/sidebar) | → `pandoc`, paling rapi |
| `Special:AllPages` / kategori | daftar semua laman | untuk otomasi loop |

## Usulan Alur Kerja Revisi
1. **Sekali di awal:** buka 1 laman lewat browser asli (claude-in-chrome / profil Chrome) → dapatkan cookie `cf_clearance`.
2. **Ambil daftar laman** dari `Special:AllPages`.
3. **Loop unduh** tiap laman via `api.php?action=parse&prop=text` + cookie tadi.
4. **Konversi HTML → Markdown** dengan `pandoc`.

> Keuntungan: challenge cukup ditembus **sekali**; hasil Markdown jauh lebih bersih daripada refactor DOM manual.

## Pertanyaan Terbuka (menunggu tanggapan Abdul)
1. **Sumber konten:** HTML terender (`pandoc`, mirip tampilan asli + tabel) **atau** wikitext mentah (ringkas, perlu bersihkan template)?
2. **Cakupan:** seluruh dokumentasi 502 atau kategori tertentu saja (mis. hanya yang relevan untuk dosen)?
3. **Uji coba dulu?** Coba tembus challenge lewat claude-in-chrome untuk 1 laman sebagai bukti konsep sebelum bangun skrip penuh?
