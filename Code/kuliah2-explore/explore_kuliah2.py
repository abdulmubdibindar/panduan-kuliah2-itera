"""
explore_kuliah2.py - Dump satu halaman kuliah2.itera.ac.id (Moodle ITERA) ke Markdown

Dipakai untuk menjelajahi instance Moodle ITERA lewat sesi Chrome yang sudah
login SSO secara manual, lalu mencatat judul + konten utama + tautan navigasi
sebagai bahan penelaahan fitur (bukan scraping tabel data).

Cara pakai:
  1. Jalankan Chrome dalam mode debugging (lihat README.md), login manual.
  2. python explore_kuliah2.py [URL]
     Tanpa argumen URL, default ke beranda kuliah2.itera.ac.id.
  3. Path berkas dump dicetak ke stdout untuk dibaca berikutnya.

Setiap pemanggilan men-dump SATU halaman. Browser Chrome milik pengguna
TIDAK pernah ditutup oleh skrip ini.
"""

import re
import sys
import time

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeout

# ─── KONFIGURASI ──────────────────────────────────────────────────────────────

DEFAULT_URL = "https://kuliah2.itera.ac.id/"

SCRIPT_DIR = Path(__file__).parent
DUMPS_DIR = SCRIPT_DIR / "dumps"

# Selector konten utama Moodle (Boost theme & varian umum), dicoba berurutan
MAIN_CONTENT_SELECTORS = ["#region-main", "[role='main']", "#page-content", "body"]

# Selector elemen navigasi yang ditelusuri untuk daftar tautan
NAV_SELECTORS = [
    "#nav-drawer", ".navbar", ".breadcrumb", ".secondary-navigation",
    "#page-navbar", "nav", ".block_navigation", ".block_settings",
]


# ─── FUNGSI UTILITAS ──────────────────────────────────────────────────────────

def is_login_page(page: Page) -> bool:
    url = page.url.lower()
    title = page.title().lower()
    return "login" in url or "masuk" in url or "sso" in url or "auth" in url or "username" in title


def slugify(url: str) -> str:
    parsed = urlparse(url)
    raw = f"{parsed.path}_{parsed.query}".strip("/_") or "root"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", raw).strip("-").lower()
    return slug[:80] or "root"


def extract_main_text(soup: BeautifulSoup) -> str:
    for selector in MAIN_CONTENT_SELECTORS:
        node = soup.select_one(selector)
        if node is not None:
            text = node.get_text("\n", strip=True)
            if text:
                return re.sub(r"\n{3,}", "\n\n", text)
    return ""


def extract_nav_links(soup: BeautifulSoup, base_url: str) -> list[tuple[str, str]]:
    seen = set()
    links = []
    for selector in NAV_SELECTORS:
        for node in soup.select(selector):
            for a in node.find_all("a", href=True):
                text = a.get_text(" ", strip=True)
                href = urljoin(base_url, a["href"])
                if not text or href.startswith("javascript:"):
                    continue
                key = (text, href)
                if key in seen:
                    continue
                seen.add(key)
                links.append(key)
    return links


def dump_page(page: Page, url: str) -> Path:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except PlaywrightTimeout:
        print(f"  [!] Timeout saat membuka halaman: {url}")
        raise

    time.sleep(1.5)  # beri waktu render elemen dinamis

    if is_login_page(page):
        print("\n⚠️  Sesi tampaknya tidak aktif (mendarat di halaman login/SSO).")
        print("   Silakan login ulang secara manual di jendela Chrome, lalu tekan Enter di sini...")
        input()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(1.5)
        if is_login_page(page):
            print("  [!] Masih di halaman login. Dump dibatalkan untuk URL ini.")
            raise RuntimeError("Sesi belum aktif setelah login ulang")

    title = page.title()
    final_url = page.url
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    main_text = extract_main_text(soup)
    nav_links = extract_nav_links(soup, final_url)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = slugify(final_url)
    DUMPS_DIR.mkdir(exist_ok=True)
    out_path = DUMPS_DIR / f"{timestamp}__{slug}.md"

    lines = [
        f"# {title}",
        "",
        f"URL: {final_url}",
        "",
        "## Konten Utama",
        "",
        main_text or "_(konten utama tidak ditemukan / kosong)_",
        "",
        "## Tautan Navigasi",
        "",
    ]
    if nav_links:
        lines += [f"- [{text}]({href})" for text, href in nav_links]
    else:
        lines.append("_(tidak ada tautan navigasi terdeteksi)_")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    print("=" * 60)
    print("  Eksplorasi kuliah2.itera.ac.id (CDP dump)")
    print(f"  Target: {url}")
    print("=" * 60)

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect_over_cdp("http://localhost:9222")
        except Exception:
            print("\n❌ Gagal menyambung ke Chrome. Pastikan Chrome sudah berjalan dengan:")
            print('   --remote-debugging-port=9222 --user-data-dir="C:\\chrome_debug_profile"')
            sys.exit(1)

        context = browser.contexts[0]
        # Pakai tab yang sudah ada (sesi login) alih-alih membuka tab baru tiap kali
        page = context.pages[0] if context.pages else context.new_page()

        try:
            out_path = dump_page(page, url)
        except (PlaywrightTimeout, RuntimeError):
            sys.exit(1)

        print(f"\n[✓] Dump tersimpan: {out_path}")
        # Sengaja TIDAK memanggil browser.close()/page.close() — biarkan Chrome
        # milik pengguna tetap terbuka untuk pemanggilan berikutnya.


if __name__ == "__main__":
    main()
