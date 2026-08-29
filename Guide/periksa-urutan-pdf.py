"""Periksa urutan halaman depan dan entri Bagian pada PDF pedoman Moodle ITERA.

Dijalankan dari direktori `Guide`:

    python periksa-urutan-pdf.py

Skrip ini hanya membaca; ia tidak pernah menulis atau mengubah PDF.
"""

from pathlib import Path
import re
import sys

import fitz  # PyMuPDF

PDF = Path(__file__).parent / "_book" / "Panduan-Moodle-ITERA.pdf"
PENANDA = ["Lembar Pengesahan", "Prakata", "Daftar Isi", "Tentang Panduan Ini"]


def ringkas(teks, batas=90):
    satu_baris = " ".join(teks.split())
    return satu_baris[:batas] if satu_baris else "(halaman kosong)"


def main():
    if not PDF.exists():
        sys.exit(f"PDF belum ada: {PDF}\nJalankan 'quarto render' lebih dahulu.")

    doc = fitz.open(PDF)
    print(f"Berkas  : {PDF}")
    print(f"Halaman : {doc.page_count}")

    print("\n== Isi 12 halaman pertama ==")
    for i in range(min(12, doc.page_count)):
        print(f"[fisik {i + 1:>2}] {ringkas(doc[i].get_text())}")

    print("\n== Nomor halaman yang tercetak di kaki halaman ==")
    for i in range(min(12, doc.page_count)):
        halaman = doc[i]
        kaki = fitz.Rect(0, halaman.rect.height - 60, halaman.rect.width, halaman.rect.height)
        angka = [t for t in halaman.get_text(clip=kaki).split() if re.fullmatch(r"\d+", t)]
        print(f"[fisik {i + 1:>2}] tercetak: {angka[-1] if angka else '(tanpa nomor)'}")

    print("\n== Entri 'Bagian' pada bookmark PDF ==")
    daftar = doc.get_toc()
    bagian = [baris for baris in daftar if baris[1].strip().startswith("Bagian")]
    if not bagian:
        print("  TIDAK ADA — judul Bagian belum terbaca sebagai heading.")
    for level, judul, halaman in bagian:
        print(f"  level {level} | hlm fisik {halaman} | {judul}")

    print("\n== Letak penanda utama ==")
    for nama in PENANDA:
        ada = [i + 1 for i in range(doc.page_count) if doc[i].search_for(nama)]
        print(f"  {nama:<22}: halaman fisik {ada[:5] if ada else 'TIDAK DITEMUKAN'}")

    doc.close()


if __name__ == "__main__":
    main()
