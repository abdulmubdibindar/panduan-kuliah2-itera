# Arsip Cookie cf_clearance (Alur Lama)

Berkas-berkas di folder ini adalah sisa alur ekstraksi Moodle Docs yang lama — memperoleh cookie `cf_clearance` dari browser asli lalu membawanya lewat `curl_cffi`. Alur itu ditinggalkan pada September 2026: [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/method_claude.py|method_claude.py]] kini meminjam sesi Chrome CDP langsung (pengguna menyelesaikan captcha sekali di jendela Chrome; cookie dan sidik jari TLS browser terbawa otomatis), sehingga kedua berkas ini tidak dipakai lagi.

## Isi

- `cookie.txt`: nilai cookie `cf_clearance` terakhir — **rahasia basi**, tetap disaring `.gitignore` dan robocopy `sync-ke-github.ps1` (pola `/XF cookie.txt` menyaring berdasar nama berkas, jadi tetap tertangkap di lokasi baru ini).
- `navigator.userAgent.txt`: catatan waktu pengambilan dan nilai `navigator.userAgent` yang dulu dipakai argumen `--user-agent`.

## Kenapa tidak dihapus

Keduanya adalah bukti sesi debugging 403 yang tercatat di [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/2026-07-07-result|2026-07-07-result]] dan [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/2026-07-08-success-report|2026-07-08-success-report]]; tautan `[[cookie.txt]]` di kedua laporan sejarah itu sengaja dibiarkan menunjuk ke lokasi lama sebagai catatan sejarah.

## Alur penggantinya

Lihat bagian "Cara Menjalankan" pada [[07 APAPUN DICOBA/Moodle Docs (manual)/Code/method_claude.md|method_claude.md]].
