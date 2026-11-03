#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
method_claude.py

Ekstraktor dokumentasi Moodle 502 (docs.moodle.org) menjadi berkas Markdown.
Alur kerja (pembaruan 2026-09: lolos Cloudflare lewat Chrome CDP, bukan cookie):

  1. Ambil daftar laman via MediaWiki API (list=allpages), BUKAN scrape Special:AllPages.
  2. Loop unduh HTML isi tiap laman via api.php?action=parse&prop=text.
  3. Unduh aset gambar + tulis ulang path-nya jadi lokal (folder images/).
  4. Tulis ulang tautan internal antar-halaman jadi tautan Markdown lokal.
  5. Konversi HTML -> Markdown dengan pandoc.
  6. Lolos Cloudflare: skrip menyambung ke Chrome asli lewat CDP (connect_over_cdp)
     dan mengirim SEMUA permintaan lewat context.request milik browser itu. Cookie
     hasil penyelesaian tantangan (cf_clearance) dan sidik jari TLS browser asli
     terbawa otomatis — tidak ada lagi copy-paste cookie. Tantangan diselesaikan
     sekali secara manual oleh pengguna di jendela Chrome.
  7. Sopan-santun: delay antar-request + berhenti anggun saat tantangan muncul lagi.

Cara pakai:
    python method_claude.py --pages Teacher_quick_guide --limit 5   # uji coba laman tertentu
    python method_claude.py --pages-file for_teacher.txt            # dari berkas daftar judul
    python method_claude.py --cdp-url http://localhost:9233 ...     # sesi Chrome debugging lain
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

# Impor Playwright dijaga try/except: bila pustakanya belum terpasang pada
# environment conda yang dipakai, skrip langsung berhenti dengan petunjuk
# pemasangan alih-alih menampilkan traceback yang tidak jelas.
try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:
    print(f"LINGKUNGAN TIDAK LENGKAP: {exc}", file=sys.stderr)
    print("Pasang dependensi pada environment conda ini dulu, mis.:", file=sys.stderr)
    print("  python -m pip install playwright beautifulsoup4", file=sys.stderr)
    raise SystemExit(2)


# ===================== KONFIGURASI =====================
# Alamat pangkal dan ruang nama dokumentasi. docs.moodle.org adalah wiki farm:
# tiap versi (mis. 502) adalah instalasi MediaWiki terpisah, jadi api.php ada
# di bawah path versi ini, BUKAN di root domain.
BASE_URL = "https://docs.moodle.org"
LANG_PATH = "502/en"
API_URL = f"{BASE_URL}/{LANG_PATH}/api.php"

# Alamat endpoint CDP Chrome yang dijalankan pengguna dengan mode debugging.
# Bisa di-override lewat --cdp-url bila sesi Chrome hidup di port lain.
CDP_URL_DEFAULT = "http://localhost:9222"

# Kesopanan dan batas waktu: jeda antar-request (detik) supaya tidak memicu
# blokir agresif, serta batas waktu tiap request dalam MILIDETIK — satuan
# timeout milik Playwright APIRequestContext, bukan detik seperti requests.
DEFAULT_DELAY = 1.5
REQUEST_TIMEOUT_MS = 30_000

# Berapa kali skrip mencoba ulang satu permintaan yang ditantang Cloudflare.
# Tiap percobaan diawali jeda agar pengguna menyelesaikan tantangan manual.
MAX_CHALLENGE_ATTEMPTS = 3

# Batas waktu menyambung ke Chrome lewat CDP (milidetik) dan batas waktu
# membaca daftar tab lewat /json/list (detik). Endpoint level-browser bisa
# menggantung lama bila Chrome baru restart sambil jendela lama dibiarkan
# hidup; batas ini memaksa skrip segera pindah ke jalur cadangan.
CDP_CONNECT_TIMEOUT_MS = 15_000
CDP_JSON_TIMEOUT_S = 5

# Direktori keluaran, relatif terhadap lokasi skrip ini.
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "moodle_docs"
IMAGES_DIR = OUTPUT_DIR / "images"

# Penanda isi halaman tantangan Cloudflare di dalam body teks (huruf kecil).
# Kalau salah satu frasa ini muncul pada respons yang seharusnya berisi
# JSON/HTML laman, artinya yang diterima adalah halaman "Just a moment...".
CHALLENGE_MARKERS = (
    "just a moment",
    "checking your browser",
    "challenge-platform",
    "cf-challenge",
)


# ===================== KELAS PENGECUALIAN =====================
class ChallengeError(Exception):
    """Diangkat saat Cloudflare masih menantang setelah semua percobaan ulang."""


# ===================== KESOPANAN KONSOL =====================
# Konsol Windows default-nya cp1252; rekonfigurasi ke utf-8 supaya judul
# laman dan teks non-ASCII yang dicetak ke terminal tidak rusak.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# ===================== PENGECEKAN LINGKUNGAN SEBELUM MULAI =====================
def cek_lingkungan() -> None:
    """Uji interpreter dan keutuhan Playwright pada environment conda aktif.

    Kegagalan Playwright yang paling menjebak bukan pada `import` (yang hampir
    selalu berhasil), melainkan pada *driver*-nya yang tidak lengkap — pernah
    terjadi pada environment `web_scrape` yang memasang playwright lewat
    conda-forge tanpa driver node: import lancar, tetapi mesin Playwright
    tidak bisa dibuka. Karena itu uji di sini dijalankan sungguhan: memanggil
    CLI driver (`node.exe cli.js --version`), supaya kerusakan langsung
    terlihat di awal dengan petunjuk perbaikan, bukan di tengah ekstraksi.
    """
    # Nama environment conda aktif: variabel CONDA_DEFAULT_ENV hanya terisi
    # bila interpreter benar-benar berjalan di dalam env conda; bila tidak,
    # tampilkan nama folder prefix sebagai pengganti informasi yang berguna.
    nama_env = os.environ.get("CONDA_DEFAULT_ENV") or Path(sys.prefix).name
    print(f"[cek lingkungan] Python {sys.version.split()[0]} | environment conda: {nama_env}")

    # Locate dua berkas inti driver lewat fungsi resmi bawaan Playwright;
    # bila pustaka berubah bentuk, kegagalan di sini juga ditangkap.
    try:
        from playwright._impl._driver import compute_driver_executable
        driver_exe, driver_entry = compute_driver_executable()
    except Exception as exc:
        print(f"\nPLAYWRIGHT TIDAK DAPAT DIUJI: {exc}", file=sys.stderr)
        raise SystemExit(2)

    # Berkas wajib ada lebih dulu; kalau hilang (kasus conda-forge tanpa
    # driver), hentikan tanpa menunggu mesin Playwright gagal dibuka.
    hilang = [p for p in (driver_exe, driver_entry) if not os.path.exists(p)]
    if hilang:
        print(f"\nPLAYWRIGHT RUSAK PADA ENVIRONMENT '{nama_env}':", file=sys.stderr)
        for p in hilang:
            print(f"  driver tidak ditemukan: {p}", file=sys.stderr)
        print("Ini lazim terjadi bila playwright dari conda-forge kehilangan driver node.", file=sys.stderr)
        print("Perbaikannya, jalankan pada environment yang sama:", file=sys.stderr)
        print("  python -m pip install --force-reinstall --no-deps playwright", file=sys.stderr)
        raise SystemExit(2)

    # Uji fungsional sungguhan: panggil CLI driver untuk mencetak versi.
    # Keluarannya sengaja dibuang — yang penting kode keluarnya 0.
    hasil = subprocess.run(
        [driver_exe, driver_entry, "--version"],
        capture_output=True, text=True, timeout=60,
    )
    if hasil.returncode != 0:
        print(f"\nPLAYWRIGHT RUSAK PADA ENVIRONMENT '{nama_env}':", file=sys.stderr)
        print(f"  driver CLI gagal dijalankan: {hasil.stderr.strip()[:300]}", file=sys.stderr)
        print("Perbaikannya, jalankan pada environment yang sama:", file=sys.stderr)
        print("  python -m pip install --force-reinstall --no-deps playwright", file=sys.stderr)
        raise SystemExit(2)

    print(f"[cek lingkungan] playwright siap (driver {hasil.stdout.strip()}).")


# ===================== DETEKSI TANTANGAN CLOUDFLARE =====================
def looks_like_challenge(status: int, headers: dict, body: str | None) -> bool:
    """Periksa apakah satu respons adalah halaman tantangan Cloudflare.

    Tiga sinyal diperiksa berurutan: status 403 (tolakan khas Cloudflare),
    header `cf-mitigated: challenge` (bukti permintaan sedang ditantang),
    lalu — hanya untuk respons teks — frasa penanda halaman tantangan pada
    awal body. `body=None` dipakai untuk respons biner (gambar) supaya tidak
    ada byte gambar yang dipaksa di-decode menjadi teks.
    """
    if status == 403:
        return True
    headers_lower = {key.lower(): value for key, value in headers.items()}
    if headers_lower.get("cf-mitigated") == "challenge":
        return True
    if body is not None:
        head = body[:2000].lower()
        return any(marker in head for marker in CHALLENGE_MARKERS)
    return False


# ===================== JEDA PEMENUHAN TANTANGAN =====================
def prompt_user_solve_challenge(url: str) -> None:
    """Cetak instruksi lalu tunggu pengguna menyelesaikan tantangan di jendela Chrome.

    Skrip tidak pernah mencoba menyelesaikan tantangan sendiri (itulah gunanya
    meminjam browser asli): tugasnya hanya memberi tahu laman yang ditolak,
    lalu berhenti menunggu sampai pengguna menekan Enter di terminal.
    """
    print()
    print("=" * 64)
    print("  CLOUDFLARE MENANTANG PERMINTAAN")
    print(f"  Laman yang diminta: {url}")
    print("=" * 64)
    print("  1. Pindah ke jendela Chrome yang terhubung (mode debugging).")
    print("  2. Buka laman di atas di jendela itu, selesaikan tantangannya")
    print("     (tunggu pemeriksaan selesai) sampai halaman normal terbuka.")
    print("  3. Kembali ke terminal ini, lalu tekan Enter untuk mencoba lagi.")
    input()


# ===================== SESI PERMINTAAN LEWAT BROWSER =====================
def browser_get(request_ctx, url: str, *, params: dict | None = None,
                text_mode: bool = True):
    """GET satu URL lewat context.request milik browser, dengan pengulangan saat ditantang.

    `request_ctx` adalah `BrowserContext.request` dari Playwright — permintaan
    lewat pintu ini dikirim oleh browser asli yang terhubung CDP: cookie
    (termasuk cf_clearance hasil penyelesaian manual pengguna) dan sidik jari
    TLS browser terbawa otomatis, sehingga tidak ada cookie yang disalin skrip.
    Bila respons terdeteksi sebagai tantangan (lihat looks_like_challenge),
    skrip meminta pengguna menyelesaikannya lalu mengulang permintaan, maksimal
    MAX_CHALLENGE_ATTEMPTS kali sebelum mengangkat ChallengeError.
    """
    for attempt in range(1, MAX_CHALLENGE_ATTEMPTS + 1):
        resp = request_ctx.get(url, params=params, timeout=REQUEST_TIMEOUT_MS)
        body = resp.text() if text_mode else None
        if not looks_like_challenge(resp.status, resp.headers, body):
            return resp
        print(
            f"    [tantangan] Cloudflare menantang permintaan "
            f"(percobaan {attempt}/{MAX_CHALLENGE_ATTEMPTS}).",
            file=sys.stderr,
        )
        if attempt == MAX_CHALLENGE_ATTEMPTS:
            raise ChallengeError(
                "Cloudflare masih menantang setelah beberapa kali percobaan. "
                "Selesaikan tantangan di jendela Chrome, lalu jalankan ulang skrip."
            )
        prompt_user_solve_challenge(url)


def api_get(request_ctx, params: dict) -> dict:
    """Panggil MediaWiki API dan kembalikan JSON. Tantangan ditangani browser_get."""
    params = {**params, "format": "json"}
    resp = browser_get(request_ctx, API_URL, params=params)
    if resp.status != 200:
        raise RuntimeError(f"API membalas status {resp.status} untuk {params}")
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"API membalas bukan JSON untuk {params}: {resp.text()[:200]!r}")


# ===================== DAFTAR LAMAN (API, bukan scrape) =====================
def list_all_pages(request_ctx) -> list[str]:
    """Ambil semua judul laman via list=allpages + paginasi apcontinue."""
    titles: list[str] = []
    apcontinue: str | None = None
    while True:
        # Parameter kueri: hanya ruang nama artikel utama (0), maksimal 500
        # judul per panggilan; `apcontinue` dipakai untuk halaman lanjutan.
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": "500",
            "apnamespace": "0",
        }
        if apcontinue:
            params["apcontinue"] = apcontinue
        data = api_get(request_ctx, params)
        for page in data.get("query", {}).get("allpages", []):
            titles.append(page["title"])
        # MediaWiki memberi kunci `continue` bila masih ada halaman berikutnya;
        # bila tidak ada, seluruh daftar sudah terambil.
        cont = data.get("continue")
        if not cont:
            break
        apcontinue = cont["apcontinue"]
        time.sleep(DEFAULT_DELAY)
    return titles


# ===================== UNDUH ISI LAMAN =====================
def fetch_page_html(request_ctx, title: str) -> str:
    """Unduh HTML isi laman (tanpa navbar/sidebar) via action=parse&prop=text."""
    data = api_get(
        request_ctx,
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


def download_images(request_ctx, soup: BeautifulSoup) -> None:
    """Unduh tiap <img> ke folder images/ lalu tulis ulang src jadi lokal."""
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
                # text_mode=False: respons biner, deteksi tantangan cukup lewat
                # status/header tanpa memaksa decode isi gambar jadi teks.
                resp = browser_get(request_ctx, abs_url, text_mode=False)
                if resp.status != 200:
                    raise RuntimeError(f"status {resp.status}")
                dest.write_bytes(resp.body())
                time.sleep(DEFAULT_DELAY)
            except ChallengeError:
                raise
            except Exception as exc:  # gambar rusak/hilang tak boleh menggagalkan seluruh laman
                print(f"    ! gagal unduh gambar {abs_url}: {exc}", file=sys.stderr)
                continue
        img["src"] = f"images/{fname}"   # arahkan ke berkas lokal


# ===================== PENGOLAHAN TAUTAN INTERNAL =====================
def rewrite_internal_links(soup: BeautifulSoup) -> None:
    """Ubah tautan /502/en/Nama_Halaman jadi tautan Markdown lokal."""
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
def process_page(request_ctx, title: str) -> None:
    """Unduh -> olah gambar -> olah tautan -> konversi -> simpan satu laman."""
    print(f"  -> {title}")
    html = fetch_page_html(request_ctx, title)
    soup = BeautifulSoup(html, "html.parser")
    download_images(request_ctx, soup)
    rewrite_internal_links(soup)
    clean_soup(soup)
    markdown = tidy_markdown(html_to_markdown(str(soup)))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{safe_filename(title)}.md"
    header = f"# {title}\n\n> Sumber: {BASE_URL}/{LANG_PATH}/{urllib.parse.quote(title)}\n\n"
    out_path.write_text(header + markdown, encoding="utf-8")


# ===================== PENYAMBUNGAN KE CHROME (DENGAN JALUR CADANGAN) =====================
def fetch_cdp_page_ws(cdp_url: str) -> str | None:
    """Ambil alamat websocket salah satu tab laman Chrome via /json/list.

    Jalur cadangan dipakai bila endpoint level-browser menggantung (bisa
    terjadi setelah Chrome di-restart sementara jendela sesi lama dibiarkan
    hidup): alih-alih menyambung ke /devtools/browser, skrip melampirkan
    diri ke ws sebuah tab yang sudah terbuka. Pintu `context.request` tetap
    tersedia dan tetap berbagi cookie dengan profil browser itu.
    """
    # /json/list memuat daftar seluruh target debug (tab, pekerja latar,
    # dan lain-lain). Dibaca lewat urllib supaya tidak bergantung pada
    # koneksi Playwright yang justru sedang bermasalah.
    try:
        with urllib.request.urlopen(f"{cdp_url}/json/list", timeout=CDP_JSON_TIMEOUT_S) as resp:
            targets = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    # Urutkan kandidat: tab laman web biasa (http/https) lebih disukai,
    # dan di antaranya laman docs.moodle.org paling disukai karena cookie
    # hasil penyelesaian tantangan menempel pada sesi laman itu.
    pages = [t for t in targets if t.get("type") == "page"]
    web_pages = [p for p in pages if (p.get("url") or "").startswith("http")]
    moodle_pages = [p for p in web_pages if "docs.moodle.org" in p.get("url", "")]
    kandidat = moodle_pages or web_pages or pages
    if not kandidat:
        return None
    return kandidat[0].get("webSocketDebuggerUrl")


def connect_to_chrome(pw, cdp_url: str):
    """Sambungkan ke Chrome lewat CDP; jatuh ke ws tab bila endpoint browser menggantung.

    Jalur utama menyambung ke endpoint level-browser (yang mencakup seluruh
    konteks). Bila sambungan itu gagal atau menggantung melewati
    CDP_CONNECT_TIMEOUT_MS, skrip melampirkan diri ke websocket salah satu
    tab yang sudah ada. Kedua jalur memberi pintu yang sama persis:
    `context.request` berbagi cookie profil browser asli.
    """
    # Jalur utama: endpoint level-browser (http://host:port). Batas waktu
    # pendek mencegah skrip menunggu tanpa akhir pada endpoint macet.
    try:
        return pw.chromium.connect_over_cdp(cdp_url, timeout=CDP_CONNECT_TIMEOUT_MS)
    except Exception as exc:
        print(f"    [catatan] endpoint browser tidak merespons ({type(exc).__name__});",
              file=sys.stderr)
        print("              mencoba jalur cadangan: melampirkan diri ke tab yang sudah terbuka ...",
              file=sys.stderr)

    # Jalur cadangan: lampirkan diri ke ws tab laman yang sudah ada.
    ws_url = fetch_cdp_page_ws(cdp_url)
    if not ws_url:
        raise RuntimeError("Tidak ada tab yang bisa dilampiri lewat /json/list.")
    return pw.chromium.connect_over_cdp(ws_url, timeout=CDP_CONNECT_TIMEOUT_MS)


# ===================== MAIN =====================
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Ekstraktor dokumentasi Moodle 502 -> Markdown lewat Chrome CDP."
    )
    p.add_argument(
        "--cdp-url",
        default=CDP_URL_DEFAULT,
        help=(
            "Alamat endpoint CDP Chrome yang berjalan mode debugging, mis. "
            f"'http://localhost:9222'. Default: '{CDP_URL_DEFAULT}'."
        ),
    )
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
    return p.parse_args()


def main() -> int:
    args = parse_args()
    global DEFAULT_DELAY
    DEFAULT_DELAY = args.delay

    # Pengecekan pra-terbang: pastikan environment conda yang dipakai
    # sungguh punya Playwright yang utuh sebelum menyambung ke Chrome.
    cek_lingkungan()

    # Tentukan daftar laman dari argumen --pages/--pages-file lebih dulu;
    # kalau keduanya kosong, daftar penuh diambil lewat API di bawah.
    titles_from_args: list[str] = list(args.pages) if args.pages else []
    if args.pages_file:
        for line in Path(args.pages_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                titles_from_args.append(line)

    with sync_playwright() as pw:
        # Sambungkan ke Chrome asli pengguna lewat CDP — jalur utama ke
        # endpoint browser, dengan jalur cadangan ke tab yang sudah terbuka
        # bila endpoint itu menggantung (lihat connect_to_chrome). Gagal
        # pada kedua jalur biasanya berarti Chrome debugging belum dijalankan
        # sama sekali: instruksikan cara membukanya, lalu berhenti (kode 2).
        try:
            browser = connect_to_chrome(pw, args.cdp_url)
        except Exception:
            print("\nGAGAL MENYAMBUNG KE CHROME.", file=sys.stderr)
            print(f"Pastikan Chrome berjalan dengan remote debugging di {args.cdp_url}:", file=sys.stderr)
            print('  & "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\chrome_debug_profile"', file=sys.stderr)
            print("Lalu buka https://docs.moodle.org/502/en/Main_page di jendela itu", file=sys.stderr)
            print("dan selesaikan tantangan Cloudflare bila muncul.", file=sys.stderr)
            return 2

        # Pakai konteks browser pertama (profil yang sedang dipakai pengguna)
        # dan pintu permintaan miliknya untuk semua GET berikutnya.
        context = browser.contexts[0]
        request_ctx = context.request

        if titles_from_args:
            titles = titles_from_args
        else:
            print("Mengambil daftar laman via MediaWiki API (lewat Chrome CDP) ...")
            try:
                titles = list_all_pages(request_ctx)
            except ChallengeError as exc:
                print(f"BERHENTI: {exc}", file=sys.stderr)
                return 2
            print(f"Ditemukan {len(titles)} laman.")

        if args.limit:
            titles = titles[: args.limit]

        # Loop unduh dengan berhenti anggun saat tantangan tak kunjung selesai.
        ok, failed = 0, 0
        for i, title in enumerate(titles, 1):
            print(f"[{i}/{len(titles)}]", end=" ")
            try:
                process_page(request_ctx, title)
                ok += 1
            except ChallengeError as exc:
                print(f"\nBERHENTI ANGGUN: {exc}", file=sys.stderr)
                print(f"Selesai sebagian: {ok} sukses sebelum tantangan muncul lagi.", file=sys.stderr)
                return 2
            except Exception as exc:
                print(f"    ! gagal: {exc}", file=sys.stderr)
                failed += 1
            time.sleep(DEFAULT_DELAY)

        # Browser pengguna sengaja TIDAK ditutup: sesi debugging dibiarkan
        # hidup supaya pemanggilan berikutnya bisa langsung tersambung lagi.
        print(f"\nSelesai. Sukses: {ok}, Gagal: {failed}. Keluaran: {OUTPUT_DIR}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
