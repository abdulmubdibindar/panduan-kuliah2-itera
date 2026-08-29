# Panduan Reproduksi & Panduan Agent (GEMINI.md)

Dokumen ini adalah versi adaptasi dari [`cdp-web-scrape/GEMINI.md`](../cdp-web-scrape/GEMINI.md), disesuaikan untuk tujuan **eksplorasi & dokumentasi fitur** `kuliah2.itera.ac.id` (Moodle ITERA), bukan scraping tabel nilai ke Google Sheets.

---

## 1. Arsitektur & Metode Proyek

Proyek ini memakai metode **Chrome DevTools Protocol (CDP)** yang sama dengan `cdp-web-scrape` untuk melewati proteksi SSO/anti-bot `kuliah2.itera.ac.id`, dengan tujuan akhir berbeda: bukan mengekstraksi data tabel, melainkan **membaca dan mencatat fitur** yang tersedia di instance tersebut sebagai bahan penelaahan untuk `Guide/KULIAH2.md`.

### Mengapa CDP, bukan Playwright biasa?
Sama seperti alasan di `cdp-web-scrape/GEMINI.md`: Playwright normal (headless/headed) menyuntikkan `navigator.webdriver` yang memicu deteksi bot/SSO, sedangkan CDP mengendalikan Chrome asli pengguna dengan sesi login aktif dan *fingerprint* manusia.

---

## 2. Persyaratan & Instalasi

Tidak perlu instalasi baru — environment conda `web_scrape` (dipakai bersama `cdp-web-scrape`) sudah punya `playwright` dan `beautifulsoup4`.

```powershell
& "C:\Users\IKHLAS\.conda\envs\web_scrape\python.exe" -m pip list
```

---

## 3. Langkah-Langkah Reproduksi

### Langkah 1: Jalankan Chrome dalam Mode Debugging
Tutup semua jendela Chrome biasa, lalu:
```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug_profile"
```

### Langkah 2: Login Manual
Di jendela Chrome debug tersebut, buka `https://kuliah2.itera.ac.id`, login SSO secara manual, pastikan sesi aktif (mis. bisa membuka kursus "Statistika").

### Langkah 3: Jalankan `explore_kuliah2.py` per Halaman
```powershell
& "C:\Users\IKHLAS\.conda\envs\web_scrape\python.exe" explore_kuliah2.py "https://kuliah2.itera.ac.id/my/"
```
Argumen adalah URL halaman yang ingin dijelajah. Setiap pemanggilan men-dump **satu** halaman ke `dumps/<timestamp>__<slug>.md` dan mencetak path filenya.

### Langkah 4: Baca Dump, Tentukan Halaman Berikutnya
Baca berkas dump yang dihasilkan (berisi judul, konten utama, dan daftar tautan navigasi), lalu ulangi Langkah 3 dengan URL berikutnya yang relevan — dituntun oleh checklist kebutuhan di [`Guide/spec.md`](../../Guide/spec.md) (Kepesertaan, Asesmen, Knowledge & Community Management).

---

## 4. Struktur File Proyek

* `explore_kuliah2.py`: skrip utama, connect via CDP, dump satu halaman per panggilan.
* `dumps/`: hasil dump Markdown per halaman (di-gitignore, berpotensi memuat data pribadi mahasiswa).

---

## 5. Petunjuk untuk Agent AI

Jika suatu saat proyek ini diadaptasi lagi untuk target/tujuan lain, ikuti pola yang sama seperti `cdp-web-scrape/GEMINI.md` §5: analisis struktur HTML target lewat Inspect Element di Chrome debug, lalu sesuaikan fungsi ekstraksi (`extract_page` di `explore_kuliah2.py`) menggunakan BeautifulSoup. Skill `playwright-cdp-scraper` di `.claude/skills/playwright_cdp_scraper/` tetap jadi acuan umum polanya.

<!-- prinsip:mulai -->
### PRINSIP INTERAKSI

Dahulukan ini sebelum [[TONE]]

1. **Jadilah Proaktif (**_**Be Proactive**_**):**

    Jangan hanya menjawab pertanyaan. Antisipasi kebutuhan pengguna berikutnya. Jika pengguna sedang mengerjakan suatu proyek, ajukan pertanyaan lanjutan untuk memperjelas tujuan mereka. Tawarkan bantuan untuk tugas-tugas berikutnya, seperti menyusun draf dokumen, membuat kerangka rencana, merangkum informasi, atau membuat daftar tugas (_to-do list_).

2. **Respons Detail untuk Tugas Kompleks (**_**Detailed Responses for Complex Tasks**_**):**

    Jawab pertanyaan sederhana secara ringkas, tetapi berikan respons yang menyeluruh dan mendalam untuk pertanyaan yang kompleks, terbuka, atau terkait proyek.

3. **Ajukan Pertanyaan Cerdas (**_**Ask Smart Questions**_**):**

    Ajukan satu pertanyaan lanjutan pada satu waktu agar tidak membuat pengguna merasa kewalahan. Gunakan pertanyaan untuk memperdalam pemahaman Anda tentang masalah tersebut dan menawarkan solusi yang lebih terukur.

4. **Berpikir Kritis (**_**Be a Critical Thinker**_**):**

    Evaluasi ide dan informasi yang disampaikan secara kritis. Tunjukkan kelemahan, asumsi yang kurang tepat, atau kurangnya bukti secara sopan. Prioritaskan akurasi dan kebenaran daripada sekadar menyetujui.

5. **Format yang Jelas (**_**Clear Formatting**_**):**

    Gunakan paragraf dan prosa untuk penjelasan dan laporan. Hindari daftar berpoin (_bulleted lists_) kecuali jika pengguna secara eksplisit meminta daftar atau pemeringkatan.

6. **Langsung ke Inti Masalah (**_**Get to the Point**_**):**

    Jangan memulai respons dengan pujian seperti "pertanyaan bagus" atau "ide yang menarik." Jawab langsung permintaan pengguna.
<!-- prinsip:selesai -->
