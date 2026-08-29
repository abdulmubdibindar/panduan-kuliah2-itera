# Laporan Sukses (2026-07-08): Ekstraksi End-to-End Pertama

Setelah dua hari bergulat dengan Cloudflare dan seluk-beluk MediaWiki, [[method_claude.py]] akhirnya berhasil mengambil satu laman dokumentasi Moodle secara utuh: unduh HTML lewat API, unduh gambar, tulis ulang tautan, sampai konversi ke Markdown yang bersih. Laman uji: `Teacher_quick_guide`.

## Tiga Masalah yang Ditemukan dan Diperbaiki

### 1. Cloudflare menolak lewat sidik jari TLS, bukan sekadar cookie

Sejak [[2026-07-07-result.md]], sudah dicurigai bahwa 403 yang terus muncul bukan cuma soal cookie `cf_clearance` yang salah format, melainkan Cloudflare Bot Management yang mengenali "sidik jari" TLS/JA3 dari `requests` standar Python (header `Cf-Mitigated: challenge` jadi buktinya). Solusinya: **Opsi A** — ganti `requests.Session()` biasa dengan `curl_cffi.requests.Session(impersonate=...)`, yang membuat jabat tangan TLS terlihat persis seperti Chrome asli.

Detail penting yang baru ketahuan saat uji coba langsung:

- `cf_clearance` terikat ke kombinasi IP + User-Agent + fingerprint TLS. Kalau salah satu berubah (atau cookie-nya sudah kedaluwarsa), 403 muncul lagi walau `curl_cffi` sudah dipakai. Solusinya: ambil cookie segar dari sesi browser yang benar-benar aktif.
- User-Agent yang dikirim skrip harus **sama persis** dengan User-Agent browser yang memperoleh cookie tadi (dalam kasus ini Edge, bukan Chrome) — meskipun profil `--impersonate` yang dipakai tetap boleh profil Chromium, karena Edge dan Chrome berbagi mesin TLS yang sama.
- Profil `--impersonate` yang tersedia di `curl_cffi` **selalu tertinggal** dari nomor versi browser asli. Versi `curl_cffi` yang terpasang (0.15.0) baru mendukung sampai `chrome146`, walau browser pengguna sudah Edge 150 — dan itu tidak masalah, karena yang ditiru adalah lapisan TLS, bukan nomor versi persis.

### 2. `api.php` 404 karena docs.moodle.org adalah *wiki farm*

Setelah TLS beres, muncul masalah baru: `api.php` di root domain (`https://docs.moodle.org/api.php`) mengembalikan 404 sungguhan (bukan halaman tantangan Cloudflare — ini justru pertanda baik, artinya permintaan sudah lolos Cloudflare dan benar-benar sampai ke server Moodle).

Penyebabnya: `docs.moodle.org` bukan satu wiki, melainkan *wiki farm* — setiap versi Moodle (mis. `502`) adalah instalasi MediaWiki terpisah dengan `api.php` sendiri di bawah path versi tersebut, bukan di root. Dikonfirmasi lewat uji beberapa kandidat path sekaligus:

| Path                | Hasil                                   |
| ------------------- | ---------------------------------------- |
| `/api.php`          | 404 (tidak ada di root)                  |
| `/502/api.php`      | 200, tapi laman HTML biasa, bukan JSON API |
| `/502/en/api.php`   | 200, JSON API valid ✅                    |
| `/en/api.php`       | 200, JSON API valid (alias)               |
| `/w/api.php`        | 404                                       |

Perbaikan: `API_URL` di [[method_claude.py]] diubah dari `f"{BASE_URL}/api.php"` menjadi `f"{BASE_URL}/{LANG_PATH}/api.php"` (yakni `https://docs.moodle.org/502/en/api.php`).

### 3. Markdown keluaran masih penuh tag HTML mentah

Begitu unduhan berhasil, `Teacher_quick_guide.md` ternyata masih dipenuhi `<div>`, `<span>`, dan `<figure>` mentah. Ini bukan bug pandoc, melainkan keterbatasan wajar: pandoc tidak punya padanan Markdown untuk elemen pembungkus generik semacam itu, jadi dibiarkan apa adanya sebagai HTML mentah.

Solusinya ada di fungsi baru `clean_soup()`, dijalankan atas hasil parse BeautifulSoup **sebelum** dikirim ke pandoc:

- Buang elemen navigasi bawaan MediaWiki yang bukan konten asli laman: `div.navtrail` (breadcrumb), `div.sideblock` (kotak menu "Managing a Moodle course" di setiap laman), `div#toc` (daftar isi otomatis), `span.mw-editsection` (tautan "edit"/"edit source").
- Sederhanakan `<figure><a><img></a><figcaption>...</figcaption></figure>` menjadi `<img>` polos + teks caption, supaya pandoc menghasilkan sintaks gambar Markdown asli (`![alt](src)`).
- Lepas (bukan hapus) semua sisa `<div>`/`<span>` generik yang tidak masuk kategori di atas (mis. `mw-parser-output`, `mw-headline`, `mw-selflink`) — isi/teks di dalamnya tetap dipertahankan, hanya tag pembungkusnya yang dilucuti.

## Hasil Akhir

Perintah yang berhasil:

```powershell
python method_claude.py --pages Teacher_quick_guide --cookie-file cookie.txt --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0" --impersonate chrome146
```

Keluaran: `Code/moodle_docs/Teacher_quick_guide.md` (Markdown bersih, tanpa tag HTML mentah) dan lima gambar di `Code/moodle_docs/images/`.

## Catatan untuk Nanti

- Masih ada spasi/baris kosong berlebih di Markdown hasil konversi — belum dirapikan, jadi kandidat perbaikan lanjutan.
- Perbaikan ini baru diuji pada satu laman (`Teacher_quick_guide`). Uji skala penuh (semua laman via `list_all_pages`) belum dilakukan.
