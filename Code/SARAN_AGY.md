# Saran & Usulan Pendekatan Proyek Ekstraksi Moodle Docs

Dokumen ini berisi saran dan usulan pendekatan dari Antigravity untuk mengatasi kendala ekstraksi dokumen Moodle Docs (versi 5.2/502) dan mengoptimalkannya untuk panduan e-learning ITERA.

## 1. Mengatasi Proteksi Cloudflare ("Moodle challenge")
Playwright atau crawler headless standar sering kali diblokir oleh Cloudflare karena tanda tangan browser otomatis (*headless browser fingerprint*) terdeteksi.

**Usulan Solusi: Remote Debugging (Chrome DevTools Protocol / CDP)**
*   **Konsep:** Dibanding mencoba meretas deteksi bot Cloudflare (yang selalu berubah), kita dapat memanfaatkan peramban Chrome asli yang sedang berjalan di komputer pengguna.
*   **Cara Menjalankan:**
    1. Jalankan Chrome dari terminal dengan port debugging aktif:
       ```bash
       chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome-profile"
       ```
    2. Buka `https://docs.moodle.org/502/en/Main_page` di jendela Chrome tersebut, selesaikan tantangan Cloudflare (jika muncul) secara manual.
    3. Skrip otomatisasi (Python/Node.js) akan terhubung ke port `9222` menggunakan pustaka Playwright/Puppeteer (`connect_over_cdp`).
    4. Skrip melakukan navigasi dan pengambilan data dengan aman karena menggunakan kuki (*cookies*) dan sesi yang sah dari Chrome asli Anda.

---

## 2. Pemanfaatan MediaWiki API untuk Konten Bersih
Dibanding mengunduh DOM HTML lengkap dari halaman web biasa (yang akan menyertakan sidebar, header, footer, dan menu navigasi), gunakan API internal MediaWiki dari Moodle Docs.

*   **Endpoint API:** `https://docs.moodle.org/502/en/api.php`
*   **Mendapatkan Daftar Halaman:**
    Gunakan modul `query` dengan parameter `list=allpages` untuk mendata seluruh judul halaman yang ada:
    ```
    api.php?action=query&list=allpages&format=json&aplimit=500
    ```
*   **Mendapatkan Konten Utama:**
    Gunakan modul `parse` dengan parameter `prop=text` untuk mengambil HTML konten artikel saja (tanpa elemen navigasi situs):
    ```
    api.php?action=parse&prop=text&page=NAMA_HALAMAN&format=json
    ```
*   **Konversi ke Markdown:**
    HTML bersih tersebut dikonversi menjadi Markdown menggunakan utilitas **Pandoc** (versi 3.8.2.1 sudah terinstal lokal) agar menghasilkan format Markdown yang standar dan rapi.

---

## 3. Pembatasan Cakupan Scraping (Targeted Scope)
Moodle Docs memiliki ribuan halaman yang mencakup panduan developer, admin server, dan fitur yang sangat teknis. Untuk panduan dosen ITERA, sebaiknya cakupan dibatasi.

**Rekomendasi Pendekatan:**
1.  **Ekstraksi Berdasarkan Kategori:** Hanya mengunduh halaman yang tergolong dalam kategori peran pengajar (*Teacher role* atau *Category:Teacher*).
2.  **Ekstraksi Berdasarkan Halaman Induk:** Memulai dari halaman indeks utama seperti `Teacher_quick_guide`, memindai semua tautan internal di dalamnya secara rekursif hingga kedalaman tertentu (misal kedalaman 2 atau 3), dan hanya mengunduh halaman-halaman tersebut.

---

## 4. Optimalisasi untuk Obsidian
Karena proyek ini dijalankan di dalam folder Obsidian (terdapat direktori `.obsidian`), hasil Markdown sebaiknya disesuaikan dengan fitur Obsidian:

*   **Tautan Internal (WikiLinks):** Konversi tautan internal antarhalaman Moodle Docs menjadi format `[[Nama Halaman]]` agar peta koneksi dokumen terbentuk otomatis di Obsidian.
*   **Penyimpanan Gambar Offline:** Unduh semua gambar pendukung dari halaman dokumentasi ke folder lokal (misalnya `attachments/` atau `images/`) dan perbarui tautan gambar di Markdown menjadi path lokal agar panduan dapat dibaca secara penuh tanpa koneksi internet.
*   **Metadata (Frontmatter):** Tambahkan YAML Frontmatter di awal setiap berkas Markdown untuk menyimpan data penunjang seperti:
    ```yaml
    ---
    title: "Nama Halaman"
    source_url: "URL Asli Moodle Docs"
    downloaded_at: 2026-07-07
    moodle_version: "5.2"
    ---
    ```

---

## Rencana Aksi Awal (Proof of Concept)
Sebagai langkah awal, kita sebaiknya membuat sebuah skrip uji coba (**PoC**) sederhana untuk:
1.  Menghubungkan ke port remote debugging Chrome.
2.  Mengunduh konten halaman `Teacher_quick_guide` via MediaWiki API.
3.  Mengonversi isi HTML-nya menjadi berkas Markdown menggunakan Pandoc.
4.  Mengunduh gambar pendukung ke folder lokal dan memperbarui tautannya.
5.  Menyimpannya ke direktori kerja untuk dievaluasi tampilannya di Obsidian.
