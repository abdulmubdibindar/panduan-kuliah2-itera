<div align="center">

**[Bahasa Indonesia](#panduan-penggunaan-platform-new-e-learning-itera)** · [English](#new-e-learning-itera-user-guide)

</div>

## Panduan Penggunaan Platform *New E-Learning* ITERA

Pedoman penggunaan platform *New E-Learning* ITERA (`kuliah2.itera.ac.id`) untuk dosen, asisten, dan mahasiswa. Disusun dari korpus dokumentasi resmi Moodle dan pengujian langsung pada kursus sandbox, diterbitkan sebagai satu dokumen PDF gabungan yang dibangun dengan Quarto dan Typst.

### Penyusun

- Dr. Ir. Harry Yuliansyah, S.T., M.Eng
- Muhammad Abdul Mubdi Bindar, S.T., M.T.
- Misfallah Nurhayati, M.T.
- Dr. Husna Tiara Putri, S.T., M.T.
- Vivian Alvianti, S.P.W.K., M.P.W.K.

### Stack dan Kebutuhan

| Kebutuhan | Keterangan |
| --- | --- |
| Quarto ≥ 1.9 | Diuji pada versi 1.9.38 |
| Typst | Sudah menyatu dengan Quarto sejak versi di atas — tidak perlu instalasi terpisah |
| Fonta (Carlito, Playfair Display, JetBrains Mono) | Sudah dibundel di `Guide/_shared/fonts/`, tidak perlu dipasang ke sistem |
| Python 3 | Hanya diperlukan bila ingin menjalankan ulang pengekstrak dokumentasi di `Code/` |

### Pemetaan Direktori

| Direktori | Isi |
| --- | --- |
| `Guide/` | Sumber Quarto (`.qmd`), konfigurasi (`_quarto.yml`), dan hasil render (`_book/`) |
| `Guide/_shared/` | Fonta, templat Typst, dan aset bersama nonprosedural |
| `Guide/eksperimen-obe-cpmk/` | Eksperimen integrasi OBE/CPMK — belum menjadi produk PDF, ditunda sampai pengujian Gradebook selesai |
| `Guide/_archive/` | Naskah pedoman versi lama (legacy) yang sudah digantikan |
| `Code/` | Pengekstrak dokumentasi dan korpus lokal 72 laman `docs.moodle.org` — korpusnya tidak ikut diterbitkan ke repo |
| `_assets/` | Rujukan akademik OBE/CPMK dan bahan pendukung lain yang dikutip lintas naskah |
| `AGENTS-MOODLE-MANUAL.md`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.md` | Berkas kontrak ICM — titik masuk agen AI yang bekerja di repo ini |

### Cara Menjalankan Quarto

Dijalankan dari direktori `Guide/` pada repo hasil kloning:

```bash
cd Guide
quarto render
```

Quarto mencetak proses render tiap bab satu per satu, diakhiri baris `Output created: _book/Panduan-Moodle-ITERA.pdf`. Berkas PDF-nya ada di `Guide/_book/Panduan-Moodle-ITERA.pdf`.

Format keluaran proyek ini hanya `typst` (lihat `Guide/_quarto.yml`), jadi `quarto preview` tidak berlaku di sini — gunakan `quarto render` lalu buka PDF-nya secara manual.

Bila Quarto berhenti dengan galat fonta tidak ditemukan, periksa apakah pengaturan `font-paths` di `Guide/_quarto.yml` masih menunjuk ke `_shared/fonts` dan kesepuluh berkas fonta di dalamnya benar-benar ikut terkloning (`git ls-files "Guide/_shared/fonts/*"`).

### Dapat Dijalankan Agent Harness

Repo ini disusun dengan kerangka **ICM (*Interpretable Context Methodology*)** dari **Jake Van Clief**: struktur folder yang membawa konteks, `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` sebagai titik masuk yang merutekan ke `AGENTS-MOODLE-MANUAL.md`, dan `CONTEXT.md` sebagai kontrak kerja di tiap wilayah (`Code/`, `Guide/`). Agen yang membaca berkas entri akan menemukan sendiri rute kerjanya tanpa merayapi seluruh pohon.

Sitasi makalahnya:

> Van Clief, J., & McDermott, D. (2026). *Interpretable Context Methodology: Folder Structure as Agent Architecture*. arXiv:2603.16021v2. <https://arxiv.org/html/2603.16021v2>

Makalah ini berlisensi **CC BY 4.0**, dan implementasi acuannya berlisensi MIT di <https://github.com/RinDig/Interpretable-Context-Methodology-ICM->. Kedua lisensi itu mengizinkan penggunaan ulang dengan atribusi; penyebutan ini sekaligus memenuhi syarat atribusinya.

### Sinkronisasi Dua Mesin

Repo ini disinkronkan dari vault OneDrive (sumber kebenaran tunggal) memakai `sync-ke-github.ps1`, yang tersimpan di akar sumber tetapi **tidak diterbitkan** ke GitHub (lihat `.gitignore`). Skrip itu menjalankan `git pull --ff-only`, mencerminkan berkas dengan robocopy, lalu commit dan push. Panduan penggunaan lengkap dan alur pikir rancangannya ada di `sync-ke-github.md`, berkas pendamping yang juga tidak diterbitkan — keduanya hanya hidup di mesin-mesin penyusun lewat sinkronisasi OneDrive.

### Konvensi Commit

Setiap commit mencatat satu maksud. Format pesan, tipe, lingkup, dan delapan aturannya ada di [CONTRIBUTING.md](CONTRIBUTING.md); kerangka pesannya tersedia di `.gitmessage` dan dapat diaktifkan sekali per klon dengan `git config commit.template .gitmessage`. Riwayat commit menggantikan berkas `_log.md`, jadi pesan yang menjelaskan *mengapa* adalah bagian dari dokumentasi proyek.

### Sumber dan Atribusi

Korpus dokumentasi generik di `Code/moodle_docs/` diekstrak dari [docs.moodle.org](https://docs.moodle.org), didistribusikan Moodle Pty Ltd di bawah lisensi [GNU GPL](https://docs.moodle.org/en/License). Korpus itu hanya tersimpan di mesin penyusun dan tidak ikut diterbitkan; yang diterbitkan adalah pengekstraknya, `Code/method_claude.py`.

---

## New E-Learning ITERA User Guide

A user guide for the *New E-Learning* ITERA platform (`kuliah2.itera.ac.id`), written for lecturers, teaching assistants, and students. Compiled from official Moodle documentation and hands-on testing on a sandbox course, published as a single combined PDF built with Quarto and Typst.

### Authors

- Dr. Ir. Harry Yuliansyah, S.T., M.Eng
- Muhammad Abdul Mubdi Bindar, S.T., M.T.
- Misfallah Nurhayati, M.T.
- Dr. Husna Tiara Putri, S.T., M.T.
- Vivian Alvianti, S.P.W.K., M.P.W.K.

### Stack and Requirements

| Requirement | Note |
| --- | --- |
| Quarto >= 1.9 | Tested on version 1.9.38 |
| Typst | Bundled with Quarto since the version above — no separate install needed |
| Fonts (Carlito, Playfair Display, JetBrains Mono) | Already bundled under `Guide/_shared/fonts/`, no system install needed |
| Python 3 | Only needed to re-run the documentation extractor in `Code/` |

### Directory Map

| Directory | Contents |
| --- | --- |
| `Guide/` | Quarto sources (`.qmd`), configuration (`_quarto.yml`), and render output (`_book/`) |
| `Guide/_shared/` | Fonts, Typst templates, and shared non-procedural assets |
| `Guide/eksperimen-obe-cpmk/` | OBE/CPMK integration experiment — not yet a PDF deliverable, on hold until Gradebook testing is complete |
| `Guide/_archive/` | Superseded legacy drafts of the guide |
| `Code/` | Documentation extractor and a local corpus of 72 `docs.moodle.org` pages — the corpus itself is not published |
| `_assets/` | Academic references for OBE/CPMK and other supporting material cited across the manuscript |
| `AGENTS-MOODLE-MANUAL.md`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.md` | ICM contract files — entry points for AI agents working in this repo |

### Running Quarto

Run from the `Guide/` directory of the cloned repo:

```bash
cd Guide
quarto render
```

Quarto prints the render progress for each chapter in turn, ending with `Output created: _book/Panduan-Moodle-ITERA.pdf`. The PDF lands at `Guide/_book/Panduan-Moodle-ITERA.pdf`.

This project's only output format is `typst` (see `Guide/_quarto.yml`), so `quarto preview` does not apply here — use `quarto render` and open the PDF manually.

If Quarto stops with a font-not-found error, check that `font-paths` in `Guide/_quarto.yml` still points to `_shared/fonts` and that all ten font files inside it were actually cloned (`git ls-files "Guide/_shared/fonts/*"`).

### Runs Under an Agent Harness

This repository is organized using **ICM (*Interpretable Context Methodology*)** by **Jake Van Clief**: a folder structure that carries context, `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` as entry points that route to `AGENTS-MOODLE-MANUAL.md`, and `CONTEXT.md` as the working contract for each area (`Code/`, `Guide/`). An agent reading the entry file finds its own working route without crawling the whole tree.

Paper citation:

> Van Clief, J., & McDermott, D. (2026). *Interpretable Context Methodology: Folder Structure as Agent Architecture*. arXiv:2603.16021v2. <https://arxiv.org/html/2603.16021v2>

The paper is licensed **CC BY 4.0**, and its reference implementation is MIT-licensed at <https://github.com/RinDig/Interpretable-Context-Methodology-ICM->. Both licenses permit reuse with attribution; this mention also satisfies that attribution requirement.

### Two-Machine Sync

This repo is synced from the OneDrive vault (the single source of truth) using `sync-ke-github.ps1`, which lives in the source root but is **not published** to GitHub (see `.gitignore`). The script runs `git pull --ff-only`, mirrors files with robocopy, then commits and pushes. The full usage guide and design rationale live in `sync-ke-github.md`, a companion file that is likewise not published — both files exist only on the authors' machines via their own OneDrive sync.

### Commit Convention

Each commit records a single intent. The message format, types, scopes, and the eight rules live in [CONTRIBUTING.md](CONTRIBUTING.md); a message skeleton is provided in `.gitmessage` and can be enabled once per clone with `git config commit.template .gitmessage`. Commit history replaces a `_log.md` file, so messages that explain *why* are part of the project documentation.

### Sources and Attribution

The generic documentation corpus under `Code/moodle_docs/` was extracted from [docs.moodle.org](https://docs.moodle.org), distributed by Moodle Pty Ltd under the [GNU GPL](https://docs.moodle.org/en/License). The corpus stays on the authors' machines and is not published; what is published is the extractor, `Code/method_claude.py`.
