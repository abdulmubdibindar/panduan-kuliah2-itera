---
type: documentation
title: Catatan Pembelajaran Berbasis Proyek Web Programming
---

Catatan ini disusun berjenjang — dari nol pengetahuan _web programming_ sampai cukup untuk membaca dan memahami **seluruh** yang terjadi di [[method_claude.py]]. Tiap tingkat mengandalkan tingkat sebelumnya, jadi urutannya sengaja dibuat naik, bukan acak per topik.

> [!NOTE] Pembaruan September 2026
> Narasi di bawah menceritakan alur **lama** — meminjam cookie `cf_clearance` lewat `curl_cffi` (Tingkat 3–5). Sejak September 2026, [[method_claude.py]] tidak lagi memakai cookie itu: skrip menyambung ke Chrome asli lewat CDP (`connect_over_cdp`) dan mengirim semua permintaan lewat `context.request` milik browser, sehingga cookie hasil penyelesaian captcha dan sidik jari TLS **browser asli** terbawa otomatis — pengguna menyelesaikan captcha sekali, mesin mengerjakan sisanya. Konsep-konsep di sini tetap bahan belajar yang sah: cookie, status 403, `Session`, dan _TLS fingerprint_ tetap dipakai untuk menjelaskan **kenapa** alur CDP dipilih (alur lama ditolak justru karena sidik jarinya buatan, bukan karena cookie-nya salah). Keterangan alur baru ada di [[method_claude.md]].

## Peta Belajar

| Tingkat | Isi | Pertanyaan yang terjawab |
|---|---|---|
| 0 | Cara internet bekerja | Apa itu "server", "request", "response"? |
| 1 | Anatomi satu permintaan HTTP | Apa itu endpoint, status code, header, cookie? |
| 2 | Dua cara ambil data dari situs | Apa beda API dengan scraping? |
| 3 | Kenapa Moodle Docs "melawan" | Kenapa Playwright gagal, kenapa `User-Agent` saja tak cukup (_TLS fingerprint_), kenapa perlu sopan-santun? |
| 4 | Bekal Python untuk baca skrip ini | `sum()` vs `.sum()`, `Session()`, `Path(...)`, exception |
| 5 | Menyatukan semua | Bagaimana [[method_claude.py]] jalan dari ujung ke ujung |

---

## Tingkat 0 — Bagaimana Internet Bekerja

### Client & Server

Setiap kali Anda membuka situs, sebenarnya ada dua pihak yang bicara: **client** (peramban/browser Anda, atau skrip Python di proyek ini) dan **server** (komputer di tempat lain yang menyimpan data situs, di sini: komputer yang melayani `docs.moodle.org`). Client selalu yang **memulai** percakapan; server hanya **membalas**.

### Request & Response

Satu "putaran bicara" itu punya dua bagian:

- **Request** — permintaan yang dikirim client, isinya "saya mau apa" (mis. "tolong kirimkan laman `Teacher_quick_guide`").
- **Response** — balasan dari server, isinya data yang diminta (atau pesan error kalau permintaannya ditolak).

Ini pola yang berulang di seluruh [[method_claude.py]] — setiap `session.get(...)` adalah satu request, dan variabel `resp`/`data` yang menampungnya adalah response.

### URL sebagai Alamat

URL (`https://docs.moodle.org/502/en/Main_page`) adalah "alamat" yang memberi tahu dua hal: **server mana** yang dituju (`docs.moodle.org`) dan **apa** yang diminta darinya (`502/en/Main_page`).

---

## Tingkat 1 — Anatomi Satu Permintaan HTTP

### Endpoint

Wajar kalau istilah ini terdengar abstrak — "endpoint" cuma nama keren untuk "alamat URL spesifik yang melayani satu fungsi tertentu di server". Satu server bisa punya banyak endpoint, masing-masing untuk tugas berbeda.

Bandingkan dua skenario di proyek ini:

- **Tanpa endpoint API** (scrape DOM penuh): Anda mengetuk "pintu depan" situs dan harus menggeledah seluruh ruangan (HTML lengkap: navbar, sidebar, iklan) untuk menemukan satu barang yang dicari.
- **Dengan endpoint API**: Anda mengetuk "loket khusus" (`docs.moodle.org/api.php`) yang memang dirancang melayani permintaan terstruktur, lalu bilang mau apa lewat parameter (`action=parse&page=...`). Yang dikembalikan sudah rapi (JSON), tanpa perlu menggeledah apa pun.

Di [[method_claude.py]], `API_URL = f"{BASE_URL}/api.php"` (lihat [[method_claude.md#KONFIGURASI|bagian KONFIGURASI]]) adalah endpoint tunggal itu — parameter `action` (`query`, `parse`, dst.) yang menentukan "loket" mana yang dituju di baliknya.

### Status Code

Setiap response membawa kode angka pendek yang meringkas hasilnya — Anda tidak perlu membaca seluruh isi balasan untuk tahu apakah permintaan berhasil. Yang paling relevan di proyek ini:

- **200** — sukses, ini yang isinya data yang diminta.
- **403** — ditolak ("Forbidden"). Di [[method_claude.py]], kode inilah yang dijadikan sinyal bahwa cookie `cf_clearance` sudah kedaluwarsa (lihat `api_get()` di [[method_claude.md#SESI HTTP|bagian SESI HTTP]]).

### Header

Header adalah "catatan tempel" yang menyertai request/response, berisi info tentang percakapan itu sendiri (bukan isi datanya). Satu header yang dipakai proyek ini: `User-Agent` — semacam kartu identitas yang memberi tahu server "siapa yang meminta ini" (browser apa, atau dalam kasus ini, skrip apa). Lihat konstanta `USER_AGENT` di [[method_claude.py]].

### Cookie

Cookie adalah secarik data kecil yang **disimpan client**, lalu dikirim ulang ke server di setiap request berikutnya sebagai "bukti pernah datang sebelumnya". Server yang mengeluarkan cookie di respons pertama, lalu client wajib menyertakannya lagi di request-request selanjutnya. Di proyek ini, cookie `cf_clearance` adalah "tiket masuk" yang didapat setelah menyelesaikan tantangan Cloudflare secara manual lewat browser asli — dibahas lebih dalam di [[#Tingkat 3 — Kenapa Moodle Docs "Melawan"|Tingkat 3]].

---

## Tingkat 2 — Dua Cara Mengambil Data dari Situs

### HTML & DOM (Apa yang Dilihat Browser)

HTML adalah teks berformat yang mendeskripsikan **tampilan** sebuah laman — judul, paragraf, gambar, tombol, semuanya ditulis sebagai "tag" (`<p>`, `<img>`, dst). Browser membaca HTML itu lalu merendernya jadi tampilan visual yang Anda lihat. HTML ini dirancang untuk **dibaca manusia lewat mata**, bukan untuk dipahami program secara langsung.

### Scraping

Scraping berarti mengunduh HTML yang dirancang untuk manusia itu, lalu **menebak-nebak** di mana letak data yang dicari di dalam struktur tag-tag tersebut (mis. "data ada di `<div>` ketiga di dalam `<table>` kedua"). Masalahnya: HTML itu penuh elemen yang tak relevan (navbar, sidebar, iklan), dan kalau situs mengubah desainnya sedikit saja, tebakan itu bisa langsung meleset.

### API & JSON

API (di proyek ini: **MediaWiki API** milik `docs.moodle.org`) adalah endpoint resmi yang memang disediakan situs untuk diakses **program**, bukan mata manusia. Hasilnya biasanya JSON — format data terstruktur (mirip kombinasi dictionary dan list di Python) yang sudah rapi, tanpa bungkus tampilan visual sama sekali.

### API vs Scraping — Dampaknya di Proyek Ini

Perbedaan ini terlihat jelas di `list_all_pages()` dalam [[method_claude.py]]: fungsi itu memakai `action=query&list=allpages` (API) untuk mendapat daftar semua judul laman, **bukan** men-scrape halaman `Special:AllPages` yang dirancang untuk dibaca manusia di browser. Hasilnya: lebih ringan (tak perlu mengunduh HTML tampilan yang tak dipakai), lebih stabil (tak bergantung struktur visual yang bisa berubah), dan sudah terstruktur rapi (list judul, bukan teks bebas yang harus di-parse).

---

## Tingkat 3 — Kenapa Moodle Docs "Melawan"

### Proteksi Bot ala Cloudflare

Banyak situs memasang lapisan pertahanan yang mendeteksi apakah pengunjungnya manusia asli atau program otomatis (bot) — inilah yang tercatat di [[RINGKASAN.md]] sebagai "Moodle challenge". Ciri khasnya: setiap request polos (`curl`, atau skrip tanpa "bukti" sebagai manusia) dibalas 403.

### Kenapa Playwright Gagal, tapi Browser Asli/`WebFetch` Lolos

Ini bukan soal Captcha yang "tidak bisa dipecahkan" — masalahnya adalah **peramban otomatis (headless browser) punya ciri-ciri yang bisa dideteksi** (disebut _fingerprint_), berbeda dari peramban yang benar-benar dijalankan manusia. Cloudflare mendeteksi ciri itu lalu memblokirnya, meskipun secara teknis Playwright "membuka" situsnya dengan benar. Browser asli (atau server pengambil tepercaya seperti `WebFetch`) tidak punya ciri mencurigakan itu, jadi tantangannya bisa diselesaikan secara normal.

_Fingerprint_ ini bukan cuma milik Playwright — skrip Python biasa (`requests`) pun punya sidik jarinya sendiri, dan salah satu yang paling sulit disembunyikan dibahas di bagian berikutnya.

### Sidik Jari yang Tak Bisa Dipalsukan: _TLS Fingerprint_

Jujur, istilah **_TLS fingerprint_** memang terdengar seperti sesuatu dari film mata-mata. Tapi intinya sederhana: **sebelum satu byte pun data HTTP dikirim, client dan server "berjabat tangan" dulu untuk menyepakati cara mengenkripsi percakapan — dan cara tiap program melakukan jabat tangan ini punya pola khas yang bisa dikenali, persis seperti sidik jari.** Pola itu diberi nama teknis JA3/JA4.

Kenapa ini penting? Ingat konsep **Header** `User-Agent` dari [[#Tingkat 1 — Anatomi Satu Permintaan HTTP|Tingkat 1]]: itu cuma **klaim** — secarik teks yang bisa Anda tulis apa saja, termasuk berbohong "saya Chrome". Nah, _TLS fingerprint_ adalah **ciri fisik** yang keluar otomatis dari pustaka yang Anda pakai, dan hampir tidak bisa Anda karang sendiri.

Mari kita bandingkan:

- **Skenario "menyamar" (dan gagal)**: skrip Python `requests` menyalin `User-Agent` Chrome persis huruf demi huruf. Di lapisan HTTP, ia tampak seperti Chrome. Tapi begitu server melihat **lebih dalam** ke jabat tangan TLS-nya, pola urutan _cipher_ dan _extension_ yang dipakai `requests` berteriak "ini OpenSSL/Python, bukan Chrome". Kartu identitasnya bilang Chrome, tapi sidik jarinya bilang Python — ketidakcocokan inilah yang justru mencurigakan.
- **Skenario jujur (yang dipakai proyek ini)**: skrip **tidak berusaha menyamar jadi browser sama sekali**. Ia hanya **meminjam** cookie `cf_clearance` yang sudah diperoleh browser asli, lalu membawanya lewat `requests.Session` (lihat [[#Tingkat 4 — Bekal Python untuk Membaca Skrip Ini|Tingkat 4]]). Server mempercayai tiket itu, bukan sidik jari TLS si skrip.

**Dampak sistemnya krusial dan menjelaskan keputusan desain seluruh proyek ini:** inilah alasan mendasar kenapa `method_claude.py` **tidak bisa menyelesaikan tantangan Cloudflare sendirian**, sehebat apa pun kita memoles `User-Agent`-nya. Sidik jari TLS Python tidak lolos, jadi satu-satunya jalan waras adalah "menumpang" tiket dari browser yang sidik jarinya memang tepercaya — bukan melawan sistem deteksi, melainkan menghindarinya.

Bukti konkretnya sudah kita temui saat _debugging_: server sempat membalas dengan header `Cf-Mitigated: challenge` (tercatat di [[2026-07-07-result.md]]), sinyal khas bahwa yang menolak bukan cookie yang salah, melainkan **sidik jari TLS** yang dikenali sebagai non-browser. Kalau suatu saat Anda benar-benar perlu skrip yang jabat tangannya menyerupai browser, pustaka seperti `curl_cffi` memang dirancang untuk meniru _TLS fingerprint_ Chrome — tapi untuk proyek ini, meminjam `cf_clearance` sudah cukup dan jauh lebih sederhana.

### Cookie `cf_clearance`: Tiket yang Bisa Basi

Setelah tantangan Cloudflare diselesaikan sekali lewat browser asli, server memberi cookie `cf_clearance` sebagai "tiket masuk" yang bisa dipakai ulang — inilah alasan skrip ini tidak perlu membuka browser tiap kali. Tapi tiket ini **tidak abadi**:

- terikat pada kombinasi **IP + User-Agent** tertentu — kalau salah satunya berubah, tiket batal;
- **kedaluwarsa** setelah beberapa waktu (menit–jam), bukan permanen.

Karena itulah [[method_claude.py]] tidak boleh berasumsi tiketnya selalu valid — lihat bagaimana `ChallengeError` menangani ini di bagian berikutnya.

### Sopan Santun dalam Mengambil Data

Jujur, terdengar aneh menyebut skrip Python "sopan" — tapi maksudnya sederhana: **jangan bersikap ke server orang lain seperti robot yang tidak peduli beban yang ditimbulkan**.

Bandingkan:

- **Skenario tidak sopan**: skrip menembak ratusan request per detik tanpa jeda, memakai User-Agent generik/samaran, dan begitu server membalas 403 skrip tetap ngotot mencoba lagi berulang-ulang.
- **Skenario sopan** (diterapkan di [[method_claude.py]]): ada jeda `DEFAULT_DELAY` antar-request, `USER_AGENT` yang jujur menyebut tujuan proyek dan kontak email, serta begitu menerima 403 skrip **berhenti anggun** alih-alih memaksa terus.

Alasan teknisnya konkret: pola trafik agresif membuat server mendeteksinya sebagai serangan lalu memblokir IP Anda — bukan cuma untuk skrip ini, tapi berdampak ke akses normal Anda juga. Dengan bersikap sopan, kalau pun server menolak, Anda akan melihat pesan jelas di terminal ("BERHENTI ANGGUN: 403 dari server...") alih-alih program macet tanpa penjelasan.

---

## Tingkat 4 — Bekal Python untuk Membaca Skrip Ini

### "Perintah", *Keyword*, Fungsi, dan *Method* — Apa Bedanya?

Wajar kalau ketiganya terasa tertukar, karena sehari-hari kita sama-sama menyebutnya "perintah". Python membedakan ketiganya secara ketat:

- ***Keyword*** (kata kunci): kata yang sudah "dikunci" jadi bagian tata bahasa Python — contoh `def`, `if`, `for`, `return`, `import`. Tidak bisa dipakai jadi nama variabel, dan tidak dipanggil pakai tanda kurung seperti fungsi.
- **Fungsi bawaan** (*built-in function*): blok kode siap pakai yang **berdiri sendiri**, dipanggil pakai nama + kurung, datanya diberikan sebagai argumen **di dalam** kurung itu. Contoh: `print()`, `sum()`, `len()`.
- **Method**: fungsi yang **menempel pada objek tertentu**, dipanggil dengan titik setelah objeknya (`objek.method()`). Objeknya sendiri jadi bagian dari pemanggilan, bukan cuma argumen di dalam kurung.

Contoh kontras — **`sum()` vs `.sum()`**:

```python
sum([1, 2, 3])        # fungsi bawaan: iterable diberikan SEBAGAI ARGUMEN di dalam kurung -> 6

import pandas as pd
s = pd.Series([1, 2, 3])
s.sum()                # method: dipanggil DI ATAS objek s lewat titik, tanpa argumen -> 6
```

`sum()` tidak tahu apa-apa sampai Anda kasih iterable-nya secara eksplisit. `.sum()` sudah "tahu" objek mana yang mau dijumlahkan karena dipanggil langsung dari objek itu — disebut method terikat (*bound method*).

Contoh nyata dari [[method_claude.py]] yang memakai keduanya sekaligus:

```python
href[len(prefix):].split("#")[0].split("?")[0]
```

- `len(prefix)` → **fungsi bawaan**, `prefix` diberikan sebagai argumen.
- `.split("#")` dan `.split("?")` → **method** milik objek string, dipanggil langsung dari string yang bersangkutan.

### `requests.Session()`

Bayangkan tiap kali mau kirim request baru, Anda harus mengetik ulang semua header (`User-Agent`) dan menyerahkan ulang semua cookie dari awal — itu skenario **tanpa** Session: repetitif dan rawan lupa.

`requests.Session()` adalah objek yang **mengingat** hal-hal itu untuk Anda di seluruh request yang lewat objek yang sama — mirip satu tab browser yang tetap terbuka, bukan membuka tab baru dari nol tiap klik tautan.

Di [[method_claude.py]], `build_session()` (lihat [[method_claude.md#SESI HTTP|bagian SESI HTTP]]) membuat satu `session`, memasang header `User-Agent` sekali, lalu menyetel cookie `cf_clearance` sekali. Setelahnya, setiap `session.get(...)` di `api_get()` maupun `download_images()` otomatis membawa User-Agent dan cookie yang sama — inilah bagaimana konsep Header dan Cookie dari [[#Tingkat 1 — Anatomi Satu Permintaan HTTP|Tingkat 1]] benar-benar dipakai di kode.

### Exception & Kelas Pengecualian Kustom

*Exception* adalah cara Python "berteriak" ketika sesuatu di luar kondisi normal terjadi saat program berjalan, lalu menghentikan alur normal supaya bisa ditangkap dan ditangani secara khusus (bukan dibiarkan program crash tanpa penjelasan).

Di [[method_claude.py]], `class ChallengeError(Exception)` (lihat [[method_claude.md#KELAS PENGECUALIAN|bagian KELAS PENGECUALIAN]]) adalah exception **buatan sendiri**, khusus dipakai untuk menandai "403 diterima, cookie kemungkinan kedaluwarsa" — beda dari error bawaan Python biasa. Fungsi `api_get()` mengangkat (`raise`) exception ini begitu mendeteksi status 403, lalu di `main()` exception itu ditangkap (`except ChallengeError as exc`) supaya loop bisa **berhenti anggun** dengan pesan jelas, alih-alih ikut pola "sopan santun" yang sudah dibahas di Tingkat 3.

### Membaca `Path(__file__).resolve().parent`

Baris ini di [[method_claude.py]] (variabel `SCRIPT_DIR`) padat, tapi kalau dibaca sebagai rantai langkah dari kiri ke kanan, jadi jelas — tiap `.` adalah satu langkah lanjutan dari hasil langkah sebelumnya:

1. `__file__` — variabel khusus berisi lokasi (path) skrip yang sedang berjalan, dalam bentuk teks.
2. `Path(__file__)` — membungkus teks itu jadi objek `Path` dari modul `pathlib`, supaya bisa dimanipulasi sebagai path (bukan sekadar teks).
3. `.resolve()` — method milik `Path`, mengubahnya jadi path **absolut** (alamat lengkap dari akar drive), sekaligus merapikan hal seperti `..`.
4. `.parent` — mengambil folder **induk** dari path tersebut, bukan berkasnya sendiri.

Gunanya: `OUTPUT_DIR = SCRIPT_DIR / "moodle_docs"` jadi selalu benar **di mana pun** skrip dijalankan, karena tidak bergantung folder kerja aktif saat `python method_claude.py` dipanggil.

### Argumen Baris Perintah (`argparse`) Sekilas

Skrip ini bisa dijalankan dengan opsi tambahan, mis. `python method_claude.py --limit 5`. `argparse` (lihat `parse_args()` di [[method_claude.md#MAIN|bagian MAIN]]) adalah modul bawaan Python yang membaca teks setelah nama skrip di terminal (`--cookie`, `--limit`, dst.), lalu mengubahnya jadi nilai yang bisa dipakai di dalam kode (`args.cookie`, `args.limit`) — tanpa ini, tiap opsi harus di-hardcode manual di dalam skrip.

---

## Tingkat 5 — Menyatukan Semua: Alur [[method_claude.py]] dari Ujung ke Ujung

Dengan bekal Tingkat 0–4, diagram alir di [[method_claude.md#Ringkasan|Ringkasan method_claude]] seharusnya sudah terbaca penuh. Ringkasnya, tiap tahap memakai konsep yang sudah dipelajari:

1. **Bangun sesi** (`build_session`) → `requests.Session` (Tingkat 4) yang membawa header `User-Agent` (Tingkat 1) dan cookie `cf_clearance` (Tingkat 1 & 3). Sesi ini sengaja **meminjam** tiket dari browser asli, bukan menyamar jadi browser — karena _TLS fingerprint_ Python tak akan lolos deteksi Cloudflare (Tingkat 3).
2. **Ambil daftar laman** (`list_all_pages`) → lewat **endpoint** API `list=allpages` (Tingkat 1 & 2), bukan scrape, dengan jeda antar-request sebagai bentuk **sopan santun** (Tingkat 3).
3. **Unduh isi tiap laman** (`fetch_page_html`) → **request** ke endpoint `action=parse` (Tingkat 0 & 1), hasilnya HTML isi murni (Tingkat 2).
4. **Olah gambar & tautan** (`download_images`, `rewrite_internal_links`) → tiap `<img>`/`<a>` dalam HTML (Tingkat 2) diunduh ulang atau ditulis ulang jadi path lokal, memakai **method** string (`.split()`, dst — Tingkat 4).
5. **Konversi ke Markdown** (`html_to_markdown`) → memanggil `pandoc` lewat `subprocess`, di luar cakupan konsep web tapi tetap bagian dari pipa.
6. **Simpan hasil** → memakai `Path` (Tingkat 4) supaya lokasi keluaran (`OUTPUT_DIR`) selalu benar di mana pun skrip dijalankan.
7. **Penanganan 403 di tengah loop** (`main`) → **status code** 403 (Tingkat 1) ditangkap sebagai `ChallengeError` (Tingkat 4), lalu program **berhenti anggun** (Tingkat 3) dengan pesan yang jelas, bukan macet diam-diam.

Kalau ada satu baris di [[method_claude.py]] yang masih terasa asing setelah membaca semua tingkat di atas, itu pertanda bagus untuk ditambahkan sebagai entri baru di sini.
