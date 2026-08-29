#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
method_claude.py

Ekstraktor dokumentasi Moodle 502 (docs.moodle.org) menjadi berkas Markdown.
Implementasi alur kerja dari SARAN_CLAUDE.md:

  1. Ambil daftar laman via MediaWiki API (list=allpages), BUKAN scrape Special:AllPages.
  2. Loop unduh HTML isi tiap laman via api.php?action=parse&prop=text (memakai cookie cf_clearance).
  3. Unduh aset gambar + tulis ulang path-nya jadi lokal (folder images/).
  4. Tulis ulang tautan internal antar-halaman jadi tautan Markdown lokal.
  5. Konversi HTML -> Markdown dengan pandoc.
  6. Lolos Cloudflare: sesi HTTP memakai curl_cffi dengan impersonate Chrome (meniru TLS/JA3
     fingerprint browser asli) — lihat 2026-07-07-result.md, Opsi A.
  7. Sopan-santun: delay antar-request + berhenti anggun saat 403.

Cara pakai:
    python method_claude.py --cookie "cf_clearance=XXXX" --limit 5      # uji coba 5 laman
    python method_claude.py --cookie-file cookie.txt                    # semua laman
    python method_claude.py --pages Teacher_quick_guide --cookie "..."  # laman tertentu (PoC)
    python method_claude.py --pages-file for_teacher.txt --cookie-file cookie.txt  # dari berkas daftar judul
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

from curl_cffi import requests
from bs4 import BeautifulSoup


# ===================== KONFIGURASI =====================
BASE_URL = "https://docs.moodle.org"
LANG_PATH = "502/en"  # ruang nama versi + bahasa dokumentasi
# docs.moodle.org adalah wiki farm: tiap versi (mis. 502) adalah instalasi MediaWiki
# terpisah, jadi api.php ada di bawah path versi ini, BUKAN di root domain.
API_URL = f"{BASE_URL}/{LANG_PATH}/api.php"

# Target impersonate curl_cffi (Opsi A, lihat 2026-07-07-result.md): meniru TLS/JA3
# fingerprint browser asli supaya lolos Cloudflare Bot Management. "chrome" otomatis
# memilih versi Chrome terbaru yang didukung curl_cffi yang terpasang; bisa juga
# dispesifikkan, mis. "chrome124"/"chrome131".
#
# Catatan trade-off: UA identifikatif ala sopan-santun (SARAN_CLAUDE #5) sengaja tidak
# lagi dipakai sebagai default, karena UA harus konsisten dengan fingerprint Chrome +
# dengan UA browser yang memperoleh cf_clearance. Kalau perlu UA persis, berikan lewat
# --user-agent.
IMPERSONATE_TARGET = "chrome"
DEFAULT_DELAY = 1.5      # jeda antar-request (detik) agar tidak memicu blokir agresif
REQUEST_TIMEOUT = 30     # batas waktu tiap request (detik)

# Direktori keluaran, relatif terhadap lokasi skrip ini.
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "moodle_docs"
IMAGES_DIR = OUTPUT_DIR / "images"


# ===================== KELAS PENGECUALIAN =====================
class ChallengeError(Exception):
    """Diangkat saat server membalas 403 (cookie cf_clearance kedaluwarsa/batal)."""


# ===================== SESI HTTP =====================
def build_session(
    cookie: str | None,
    user_agent: str | None = None,
    impersonate: str = IMPERSONATE_TARGET,
) -> requests.Session:
    """Bangun sesi curl_cffi yang meniru TLS fingerprint Chrome + pasang cookie cf_clearance.

    Sesi memakai `impersonate` curl_cffi sehingga TLS/JA3 handshake tampak seperti Chrome
    asli (bukan python-requests) — ini yang membedakan Opsi A dari `requests` biasa. User-Agent
    dibiarkan mengikuti bawaan impersonate agar konsisten dengan fingerprint-nya; hanya
    di-override kalau `user_agent` diberikan eksplisit (mis. UA persis browser yang memperoleh
    cf_clearance).
    """
    session = requests.Session(impersonate=impersonate)
    if user_agent:
        session.headers.update({"User-Agent": user_agent})
    if cookie:
        # Cookie bisa berupa "cf_clearance=xxx" atau "cf_clearance=xxx; other=yyy".
        for pair in cookie.split(";"):
            pair = pair.strip()
            if "=" in pair:
                name, value = pair.split("=", 1)
                session.cookies.set(name.strip(), value.strip(), domain="docs.moodle.org")
        if not session.cookies:
            print(
                "PERINGATAN: string cookie diberikan tapi tidak ada pasangan 'nama=nilai' "
                "yang terbaca (tidak ditemukan tanda '='). Pastikan formatnya "
                "'cf_clearance=<nilai>', bukan hanya nilainya saja.",
                file=sys.stderr,
            )
    return session


def api_get(session: requests.Session, params: dict) -> dict:
    """Panggil MediaWiki API dan kembalikan JSON. Deteksi 403 sebagai ChallengeError."""
    params = {**params, "format": "json"}
    resp = session.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
    if resp.status_code == 403:
        debug_headers = {
            k: v for k, v in resp.headers.items()
            if k.lower() in ("cf-ray", "cf-mitigated", "server", "content-type")
        }
        print(f"    [debug] header respons 403: {debug_headers}", file=sys.stderr)
        print(f"    [debug] cuplikan body: {resp.text[:300]!r}", file=sys.stderr)
        raise ChallengeError(
            "403 dari server. Cookie cf_clearance kemungkinan kedaluwarsa/batal "
            "(terikat IP + User-Agent). Perbarui cookie lalu jalankan ulang."
        )
    resp.raise_for_status()
    return resp.json()


# ===================== DAFTAR LAMAN (API, bukan scrape) =====================
def list_all_pages(session: requests.Session) -> list[str]:
    """Ambil semua judul laman via list=allpages + paginasi apcontinue (SARAN_CLAUDE poin #4)."""
    titles: list[str] = []
    apcontinue: str | None = None
    while True:
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": "500",
            "apnamespace": "0",   # hanya ruang nama artikel utama
        }
        if apcontinue:
            params["apcontinue"] = apcontinue
        data = api_get(session, params)
        for page in data.get("query", {}).get("allpages", []):
            titles.append(page["title"])
        cont = data.get("continue")
        if not cont:
            break
        apcontinue = cont["apcontinue"]
        time.sleep(DEFAULT_DELAY)
    return titles


# ===================== UNDUH ISI LAMAN =====================
def fetch_page_html(session: requests.Session, title: str) -> str:
    """Unduh HTML isi laman (tanpa navbar/sidebar) via action=parse&prop=text."""
    data = api_get(
        session,
        {"action": "parse", "page": title, "prop": "text", "redirects": "1"},
    )
    if "error" in data:
        raise RuntimeError(f"API error untuk '{title}': {data['error'].get('info')}")
    return data["parse"]["text"]["*"]


# ===================== PENGOLAHAN GAMBAR =====================
def safe_filename(name: str) -> str:
    """Ubah string apa pun jadi nama berkas yang aman lintas-OS."""
    name = urllib.parse.unquote(name)
    name = re.sub(r"[^\w.\-]+", "_", name)
    return name.strip("_") or "untitled"


def download_images(session: requests.Session, soup: BeautifulSoup) -> None:
    """Unduh tiap <img> ke folder images/ lalu tulis ulang src jadi lokal (SARAN_CLAUDE poin #2)."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        abs_url = urllib.parse.urljoin(BASE_URL, src)      # ubah path relatif jadi absolut
        fname = safe_filename(os.path.basename(urllib.parse.urlparse(abs_url).path))
        dest = IMAGES_DIR / fname
        if not dest.exists():
            try:
                r = session.get(abs_url, timeout=REQUEST_TIMEOUT)
                if r.status_code == 403:
                    raise ChallengeError("403 saat mengunduh gambar; cookie perlu di-refresh.")
                r.raise_for_status()
                dest.write_bytes(r.content)
                time.sleep(DEFAULT_DELAY)
            except ChallengeError:
                raise
            except Exception as exc:  # gambar rusak/hilang tak boleh menggagalkan seluruh laman
                print(f"    ! gagal unduh gambar {abs_url}: {exc}", file=sys.stderr)
                continue
        img["src"] = f"images/{fname}"   # arahkan ke berkas lokal


# ===================== PENGOLAHAN TAUTAN INTERNAL =====================
def rewrite_internal_links(soup: BeautifulSoup) -> None:
    """Ubah tautan /502/en/Nama_Halaman jadi tautan Markdown lokal (SARAN_CLAUDE poin #3)."""
    prefix = f"/{LANG_PATH}/"
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(prefix):
            page = href[len(prefix):].split("#")[0].split("?")[0]
            if page:
                anchor = href.split("#", 1)[1] if "#" in href else ""
                target = f"{safe_filename(page)}.md" + (f"#{anchor}" if anchor else "")
                a["href"] = target


# ===================== PEMBERSIHAN HTML SISA MEDIAWIKI =====================
def clean_soup(soup: BeautifulSoup) -> None:
    """Buang elemen non-konten & lepas wrapper div/span generik sebelum dikirim ke pandoc.

    Pandoc tidak punya padanan Markdown untuk <div>/<span>/<figure> generik, jadi kalau
    dibiarkan apa adanya elemen-elemen ini keluar sebagai HTML mentah di berkas .md (bukan
    dikonversi). Fungsi ini membersihkannya dulu di level HTML.
    """
    # Elemen navigasi bawaan MediaWiki yang bukan konten asli laman (menu breadcrumb,
    # kotak navigasi sisi, daftar isi otomatis, link "edit"/"edit source").
    for selector in ("div.navtrail", "div.sideblock", "div#toc"):
        for tag in soup.select(selector):
            tag.decompose()
    for tag in soup.find_all("span", class_="mw-editsection"):
        tag.decompose()

    # Sederhanakan <figure><a><img></a><figcaption>...</figcaption></figure> jadi <img>
    # polos + teks caption, supaya pandoc menghasilkan sintaks gambar Markdown asli
    # (![alt](src)) alih-alih membiarkan seluruh blok sebagai HTML mentah.
    for figure in soup.find_all("figure"):
        img = figure.find("img")
        if not img:
            figure.decompose()
            continue
        caption_tag = figure.find("figcaption")
        # Pakai separator " " karena get_text() tanpa separator menggabungkan teks
        # lintas-tag tanpa spasi (mis. "using the" + "Boost theme" -> "using theBoost theme").
        caption = re.sub(r"\s+", " ", caption_tag.get_text(" ", strip=True)) if caption_tag else ""
        new_img = soup.new_tag("img", src=img.get("src", ""), alt=caption)
        contents = [new_img]
        if caption:
            em = soup.new_tag("em")
            em.string = caption
            contents.append(soup.new_string("\n"))
            contents.append(em)
        figure.replace_with(*contents)

    # Lepas sisa wrapper <div>/<span> generik (mis. mw-parser-output, mw-headline,
    # mw-selflink) -- tag dibuang, isi/teks di dalamnya tetap dipertahankan.
    for tag in soup.find_all(["div", "span"]):
        tag.unwrap()


# ===================== KONVERSI HTML -> MARKDOWN =====================
def html_to_markdown(html: str) -> str:
    """Konversi HTML menjadi Markdown GitHub-flavored memakai pandoc."""
    result = subprocess.run(
        ["pandoc", "--from=html", "--to=gfm", "--wrap=none"],
        input=html.encode("utf-8"),
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc gagal: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout.decode("utf-8")


# ===================== PEMBERSIHAN SPASI EKSTRA =====================
def tidy_markdown(markdown: str) -> str:
    """Rapikan spasi berlebih akibat artefak HTML MediaWiki, mis. ' .' atau ' ,' sisa
    dari teks yang terpisah tag (contoh nyata: '</a> .' pada Teacher_quick_guide).
    Dilewati di dalam blok kode berpagar (```) supaya indentasi/format kode tak ikut kena.
    """
    lines = markdown.split("\n")
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # (?!\[) mencegah "spasi + !" sebelum sintaks gambar Markdown ![alt](src) ikut
        # kehapus (itu bukan artefak, tapi pemisah sengaja antar dua gambar berurutan).
        lines[i] = re.sub(r"[ \t]+([.,;:?]|!(?!\[))", r"\1", line)
    return "\n".join(lines)


# ===================== PIPA PER-LAMAN =====================
def process_page(session: requests.Session, title: str) -> None:
    """Unduh -> olah gambar -> olah tautan -> konversi -> simpan satu laman."""
    print(f"  -> {title}")
    html = fetch_page_html(session, title)
    soup = BeautifulSoup(html, "html.parser")
    download_images(session, soup)
    rewrite_internal_links(soup)
    clean_soup(soup)
    markdown = tidy_markdown(html_to_markdown(str(soup)))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{safe_filename(title)}.md"
    header = f"# {title}\n\n> Sumber: {BASE_URL}/{LANG_PATH}/{urllib.parse.quote(title)}\n\n"
    out_path.write_text(header + markdown, encoding="utf-8")


# ===================== MAIN =====================
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ekstraktor dokumentasi Moodle 502 -> Markdown.")
    p.add_argument("--cookie", help="Nilai cookie, mis. 'cf_clearance=XXXX'.")
    p.add_argument("--cookie-file", help="Berkas berisi string cookie (alternatif --cookie).")
    p.add_argument("--pages", nargs="+", help="Judul laman tertentu (lewati pengambilan daftar).")
    p.add_argument(
        "--pages-file",
        help=(
            "Berkas teks berisi judul laman, satu judul per baris (alternatif/tambahan "
            "--pages). Baris kosong dan baris berawalan '#' diabaikan."
        ),
    )
    p.add_argument("--limit", type=int, help="Batasi jumlah laman (untuk uji coba).")
    p.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="Jeda antar-request (detik).")
    p.add_argument(
        "--user-agent",
        help=(
            "Override User-Agent (mis. hasil navigator.userAgent dari browser yang "
            "dipakai memperoleh cf_clearance). Default: UA Chrome bawaan impersonate "
            "curl_cffi supaya konsisten dengan TLS fingerprint-nya."
        ),
    )
    p.add_argument(
        "--impersonate",
        default=IMPERSONATE_TARGET,
        help=(
            "Profil browser yang ditiru curl_cffi di lapisan TLS/JA3, mis. 'chrome', "
            f"'chrome124', 'chrome131'. Default: '{IMPERSONATE_TARGET}'."
        ),
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    global DEFAULT_DELAY
    DEFAULT_DELAY = args.delay

    cookie = args.cookie
    if args.cookie_file:
        cookie = Path(args.cookie_file).read_text(encoding="utf-8").strip()
    if not cookie:
        print("PERINGATAN: tidak ada cookie cf_clearance; kemungkinan besar kena 403.",
              file=sys.stderr)

    session = build_session(cookie, user_agent=args.user_agent, impersonate=args.impersonate)

    # Tentukan daftar laman: dari argumen --pages/--pages-file, atau via API.
    titles_from_args: list[str] = list(args.pages) if args.pages else []
    if args.pages_file:
        for line in Path(args.pages_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                titles_from_args.append(line)

    if titles_from_args:
        titles = titles_from_args
    else:
        print("Mengambil daftar laman via MediaWiki API ...")
        try:
            titles = list_all_pages(session)
        except ChallengeError as exc:
            print(f"BERHENTI: {exc}", file=sys.stderr)
            return 2
        print(f"Ditemukan {len(titles)} laman.")

    if args.limit:
        titles = titles[: args.limit]

    # Loop unduh dengan berhenti anggun saat cookie kedaluwarsa (SARAN_CLAUDE poin #1).
    ok, failed = 0, 0
    for i, title in enumerate(titles, 1):
        print(f"[{i}/{len(titles)}]", end=" ")
        try:
            process_page(session, title)
            ok += 1
        except ChallengeError as exc:
            print(f"\nBERHENTI ANGGUN: {exc}", file=sys.stderr)
            print(f"Selesai sebagian: {ok} sukses sebelum cookie batal.", file=sys.stderr)
            return 2
        except Exception as exc:
            print(f"    ! gagal: {exc}", file=sys.stderr)
            failed += 1
        time.sleep(DEFAULT_DELAY)

    print(f"\nSelesai. Sukses: {ok}, Gagal: {failed}. Keluaran: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
