#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
method_claude_quarto.py

Ekstraktor dokumentasi Quarto (quarto.org/docs/guide/) menjadi berkas Markdown,
ditulis langsung ke direktori `how-to-quarto/` (menggantikan isi lama).

Beda mendasar dari method_claude.py (Moodle):
  - quarto.org BUKAN MediaWiki dan TIDAK ada proteksi Cloudflare (terverifikasi:
    curl polos dengan UA generik langsung dapat HTTP 200). Karena itu skrip ini
    memakai `requests` biasa -- tidak ada cookie/curl_cffi/impersonate sama sekali.
  - Tidak ada API daftar laman. Sumber discovery adalah elemen <nav id="quarto-sidebar">
    di laman seed (docs/guide/index.html), yang memuat seluruh tautan bagian Guide.
  - Konten utama tiap laman ada di <main id="quarto-document-content">.
  - Struktur keluaran mirror path URL asli (docs/authoring/x.html -> authoring/x.md),
    BUKAN flat safe_filename() ala Moodle, karena banyak index.html di folder berbeda
    yang akan bertabrakan nama kalau di-flatten.

Cara pakai:
    python method_claude_quarto.py --limit 5      # uji coba 5 laman pertama
    python method_claude_quarto.py                # ekstraksi penuh (~180 laman)
"""

import argparse
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# ===================== KONFIGURASI =====================
BASE_URL = "https://quarto.org"
DEFAULT_SEED_URL = f"{BASE_URL}/docs/guide/index.html"
DEFAULT_USER_AGENT = "MoodleDocsExtractor-Quarto/1.0 (+dokumentasi pribadi, non-komersial)"
DEFAULT_DELAY = 0.5      # jeda antar-request (detik) -- sekadar etiket, bukan menghindari blokir
REQUEST_TIMEOUT = 30

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = SCRIPT_DIR.parent / "how-to-quarto"
ASSETS_FALLBACK_DIRNAME = "_assets"

SIDEBAR_SELECTOR = "nav#quarto-sidebar"
SIDEBAR_LINK_SELECTOR = "a.sidebar-link"
MAIN_CONTENT_SELECTOR = "main#quarto-document-content"
TITLE_HEADER_SELECTOR = "header#title-block-header"


# ===================== SESI HTTP =====================
def build_session(user_agent: str = DEFAULT_USER_AGENT) -> requests.Session:
    """Bangun sesi requests polos. Tidak perlu cookie/impersonate -- quarto.org
    tidak memakai proteksi Cloudflare seperti docs.moodle.org."""
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})
    return session


def fetch_page(session: requests.Session, url: str) -> str:
    """Unduh HTML mentah satu laman. Gagal (4xx/5xx/jaringan) dilempar sebagai
    requests.RequestException biasa -- dipanggil dari process_page yang menangani
    kegagalan per-laman tanpa menghentikan seluruh loop."""
    resp = session.get(url, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.text


# ===================== PEMETAAN URL -> PATH LOKAL =====================
def safe_filename(name: str) -> str:
    """Ubah satu segmen nama jadi aman lintas-OS (dipakai per-segmen path, bukan
    seluruh string, supaya '/' tetap jadi pemisah folder)."""
    name = urllib.parse.unquote(name)
    name = re.sub(r"[^\w.\-]+", "_", name)
    return name.strip("_") or "untitled"


def page_output_path(abs_url: str, output_dir: Path) -> Path | None:
    """Petakan URL laman docs Quarto ke path Markdown lokal, mirroring struktur
    folder URL asli. Hanya URL quarto.org di bawah /docs/ yang berakhiran .html
    yang dianggap "laman" -- ini sengaja mengecualikan aset non-HTML (gambar,
    dsb.) yang kebetulan juga berada di bawah /docs/ (mis. docs/authoring/elephant.png
    dirujuk lewat tautan lightbox <a href="elephant.png">), supaya tidak salah
    dikira laman dan ditulis ulang jadi tautan .md yang rusak.
    """
    if not urllib.parse.urlparse(abs_url).path.endswith(".html"):
        return None
    base = asset_output_path(abs_url, output_dir)
    if base is None:
        return None
    return base.with_suffix(".md")


def asset_output_path(abs_url: str, output_dir: Path) -> Path | None:
    """Sama seperti page_output_path() tapi untuk aset apa pun (gambar, dsb.) --
    tidak mensyaratkan '.html' dan tidak mengubah ekstensi. Dipakai supaya lokasi
    unduh gambar dihitung dari URL absolut (bukan aritmetika path relatif '../'
    terhadap folder keluaran yang sudah "docs/"-nya dibuang), sehingga tetap
    benar untuk folder gambar bersama lintas-subfolder (mis. docs/tools/images/
    dipakai bareng oleh docs/tools/positron/ dan docs/tools/vscode/).
    """
    parsed = urllib.parse.urlparse(abs_url)
    if parsed.netloc != "quarto.org":
        return None
    if not parsed.path.startswith("/docs/"):
        return None
    rel = parsed.path[len("/docs/"):]
    segments = [safe_filename(s) for s in rel.split("/") if s]
    if not segments:
        return None
    return output_dir.joinpath(*segments)


# ===================== DISCOVERY LEWAT SIDEBAR =====================
def discover_guide_pages(session: requests.Session, seed_url: str, output_dir: Path) -> list[str]:
    """Ambil seluruh URL laman Guide dari <nav id="quarto-sidebar"> di laman seed.
    Pengganti list_all_pages() (MediaWiki API) versi Moodle -- di sini tidak ada
    API, jadi sidebar laman seed itu sendiri yang jadi sumber daftar laman.
    """
    html = fetch_page(session, seed_url)
    soup = BeautifulSoup(html, "html.parser")
    sidebar = soup.select_one(SIDEBAR_SELECTOR)
    if sidebar is None:
        raise RuntimeError(
            f"Selektor '{SIDEBAR_SELECTOR}' tidak ditemukan di {seed_url}. "
            "Markup situs mungkin berubah -- periksa ulang."
        )

    urls: list[str] = []
    seen: set[str] = set()
    for a in sidebar.select(SIDEBAR_LINK_SELECTOR):
        href = a.get("href")
        if not href:
            continue
        abs_url = urllib.parse.urljoin(seed_url, href).split("#")[0]
        if page_output_path(abs_url, output_dir) is None:
            continue  # buang tautan eksternal (github.com, shinyapps.io, dll.)
        if abs_url in seen:
            continue  # dedup: beberapa href tampil dua kali (judul section + item pertama)
        seen.add(abs_url)
        urls.append(abs_url)
    return urls


# ===================== EKSTRAKSI KONTEN =====================
def extract_main_content(soup: BeautifulSoup) -> tuple[str, "BeautifulSoup"]:
    """Ambil elemen <main id="quarto-document-content">, lalu pisahkan judul H1
    dari header#title-block-header (yang juga memuat breadcrumb) sebelum header
    itu dibuang -- supaya kita punya judul untuk header berkas Markdown sendiri
    tanpa duplikasi H1 di isi.
    """
    main = soup.select_one(MAIN_CONTENT_SELECTOR)
    if main is None:
        raise RuntimeError(
            f"Selektor '{MAIN_CONTENT_SELECTOR}' tidak ditemukan. "
            "Markup situs mungkin berubah -- periksa ulang."
        )
    title = "Untitled"
    header = main.select_one(TITLE_HEADER_SELECTOR)
    if header is not None:
        h1 = header.select_one("h1.title") or header.find("h1")
        if h1:
            title = re.sub(r"\s+", " ", h1.get_text(" ", strip=True))
        header.decompose()
    return title, main


def simplify_figures(soup: "BeautifulSoup", main: "BeautifulSoup") -> None:
    """Sederhanakan <figure><a><img></a><figcaption>...</figcaption></figure>
    (dan variasi tanpa <a> pembungkus) jadi <img> polos + teks caption, supaya
    pandoc menghasilkan sintaks gambar Markdown asli. Reuse ide dari clean_soup()
    versi Moodle. Tag baru harus dibuat lewat `soup.new_tag()` (objek parse tree
    utuh) -- `Tag.new_tag` di bs4 4.12 adalah `None`, bukan method."""
    for figure in main.find_all("figure"):
        img = figure.find("img")
        if not img:
            figure.decompose()
            continue
        caption_tag = figure.find("figcaption")
        caption = re.sub(r"\s+", " ", caption_tag.get_text(" ", strip=True)) if caption_tag else ""
        new_img = soup.new_tag("img", src=img.get("src", ""), alt=img.get("alt", caption))
        contents = [new_img]
        if caption:
            em = soup.new_tag("em")
            em.string = caption
            contents.append(soup.new_string("\n"))
            contents.append(em)
        figure.replace_with(*contents)


def clean_quarto_soup(soup: "BeautifulSoup", main: "BeautifulSoup") -> None:
    """Sederhanakan figure lalu lepas wrapper <div>/<span> generik sebelum pandoc.

    Batasan yang perlu diketahui: callout (.callout-note/.callout-tip/dst.) dan
    panel-tabset Quarto tidak punya padanan Markdown native di pandoc, sehingga
    setelah unwrap div generik ini kontennya akan collapse jadi paragraf/teks
    berurutan tanpa pemisah visual. Laman yang memakainya (terutama di tools/)
    kemungkinan perlu dipecah manual belakangan.
    """
    simplify_figures(soup, main)
    # "section" wajib diikutkan: pandoc membaca <section> HTML5 sebagai blok Div
    # (class "section level-N") lalu menuliskannya sebagai <div> mentah di gfm
    # karena gfm tak punya padanan container generik -- kalau tak diunwrap di sini,
    # tiap section heading akan bocor jadi HTML mentah di Markdown hasil.
    for tag in main.find_all(["div", "span", "section"]):
        tag.unwrap()


# ===================== PENGOLAHAN GAMBAR =====================
def resolve_and_download_images(
    session: requests.Session, main: "BeautifulSoup", page_url: str,
    page_out_path: Path, output_dir: Path,
) -> None:
    """Unduh tiap <img>, memetakan URL absolut gambar ke path lokal lewat
    asset_output_path() (mirroring path URL asli di bawah /docs/, prefix "docs/"
    dibuang) -- BUKAN aritmetika '../' terhadap folder keluaran, karena folder
    keluaran py itu sendiri sudah kehilangan satu level ("docs/") dibanding
    struktur URL asli, sehingga path relatif dengan '../' yang menuju folder
    gambar bersama lintas-subfolder (mis. docs/tools/images/ dipakai bareng oleh
    docs/tools/positron/ dan docs/tools/vscode/) akan salah hitung kalau
    dikerjakan relatif terhadap folder keluaran. Aset di luar /docs/ (mis. logo
    situs) jatuh ke folder fallback _assets/.
    """
    page_out_dir = page_out_path.parent
    for img in main.find_all("img"):
        src = img.get("src")
        if not src or src.startswith(("http://", "https://", "data:")):
            continue
        abs_url = urllib.parse.urljoin(page_url, src)
        dest = asset_output_path(abs_url, output_dir)
        if dest is None:
            fname = safe_filename(Path(urllib.parse.urlparse(abs_url).path).name)
            dest = output_dir / ASSETS_FALLBACK_DIRNAME / fname
        img["src"] = os.path.relpath(dest, start=page_out_dir).replace("\\", "/")

        if not dest.exists():
            try:
                r = session.get(abs_url, timeout=REQUEST_TIMEOUT)
                r.raise_for_status()
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(r.content)
                time.sleep(DEFAULT_DELAY)
            except Exception as exc:
                print(f"    ! gagal unduh gambar {abs_url}: {exc}", file=sys.stderr)


# ===================== PENGOLAHAN TAUTAN INTERNAL =====================
def resolve_and_rewrite_links(main: "BeautifulSoup", page_url: str, page_out_path: Path, output_dir: Path) -> None:
    """Tulis ulang <a href> yang menunjuk ke laman docs Quarto lain (dalam cakupan
    Guide) jadi tautan Markdown lokal relatif. Tautan di luar cakupan (Reference,
    laman quarto.org lain, aset non-HTML, atau eksternal) dibiarkan apa adanya.
    """
    page_out_dir = page_out_path.parent
    for a in main.find_all("a", href=True):
        href = a["href"]
        abs_url = urllib.parse.urljoin(page_url, href)
        anchor = urllib.parse.urlparse(abs_url).fragment
        target = page_output_path(abs_url.split("#")[0], output_dir)
        if target is None:
            continue
        rel = os.path.relpath(target, start=page_out_dir).replace("\\", "/")
        a["href"] = rel + (f"#{anchor}" if anchor else "")


# ===================== KONVERSI HTML -> MARKDOWN =====================
def html_to_markdown(html: str) -> str:
    """Konversi HTML menjadi Markdown GitHub-flavored memakai pandoc (reuse persis
    dari method_claude.py -- generik, tidak spesifik Moodle)."""
    import subprocess
    result = subprocess.run(
        ["pandoc", "--from=html", "--to=gfm", "--wrap=none"],
        input=html.encode("utf-8"),
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc gagal: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout.decode("utf-8")


def tidy_markdown(markdown: str) -> str:
    """Rapikan spasi berlebih akibat artefak HTML (reuse persis dari method_claude.py)."""
    lines = markdown.split("\n")
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        lines[i] = re.sub(r"[ \t]+([.,;:?]|!(?!\[))", r"\1", line)
    return "\n".join(lines)


# ===================== PIPA PER-LAMAN =====================
def process_page(session: requests.Session, url: str, output_dir: Path) -> tuple[str, Path]:
    """Unduh -> ekstrak main -> olah gambar -> olah tautan -> bersihkan -> konversi
    -> simpan satu laman. Mengembalikan (judul, path_relatif) untuk dipakai
    generate_root_index()."""
    out_path = page_output_path(url, output_dir)
    if out_path is None:
        raise RuntimeError(f"URL di luar cakupan /docs/: {url}")
    print(f"  -> {url}")

    html = fetch_page(session, url)
    soup = BeautifulSoup(html, "html.parser")
    title, main = extract_main_content(soup)
    resolve_and_download_images(session, main, url, out_path, output_dir)
    resolve_and_rewrite_links(main, url, out_path, output_dir)
    clean_quarto_soup(soup, main)
    # decode_contents() (bukan str(main)) supaya tag <main> itu sendiri tidak ikut
    # dikirim ke pandoc -- kalau ikut, pandoc akan membungkusnya jadi <div role="main">
    # mentah di gfm dengan alasan yang sama seperti <section> di clean_quarto_soup.
    markdown = tidy_markdown(html_to_markdown(main.decode_contents()))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    header = f"# {title}\n\n> Sumber: {url}\n\n"
    out_path.write_text(header + markdown, encoding="utf-8")
    return title, out_path.relative_to(output_dir)


# ===================== INDEKS ROOT =====================
EXCLUDED_TOP_DIRS = {"_arsip-manual-lama", "_assets"}


def generate_root_index(output_dir: Path) -> None:
    """Buat SATU `_index.md` di root output_dir yang mengindeks turun sampai
    level subdirektori (bukan `_index.md` terpisah di tiap subfolder) -- ini
    pengecualian sengaja dari konvensi baku AGENTS.md untuk direktori ini,
    dikonfirmasi Abdul karena skala ~180 laman tidak realistis diindeks manual
    per folder.

    Memindai ulang seluruh *.md di output_dir (bukan cuma laman yang diproses
    di run saat ini) supaya index tetap lengkap & benar walau dipanggil setelah
    run parsial (mis. --limit atau --pages untuk uji coba).
    """
    by_dir: dict[Path, list[tuple[str, Path]]] = {}
    for md_path in output_dir.rglob("*.md"):
        rel_path = md_path.relative_to(output_dir)
        if rel_path.name == "_index.md" or rel_path.parts[0] in EXCLUDED_TOP_DIRS:
            continue
        first_line = md_path.read_text(encoding="utf-8").splitlines()[0]
        title = first_line.lstrip("#").strip() or rel_path.stem
        by_dir.setdefault(rel_path.parent, []).append((title, rel_path))

    top_dirs = sorted({p.parts[0] for p in by_dir if p.parts})

    lines = [
        "# Indeks Direktori how-to-quarto",
        "",
        "Dokumen indeks tunggal (dibuat otomatis oleh "
        "[[method_claude_quarto.py]]) yang mengindeks seluruh isi `how-to-quarto/` "
        "sampai level subdirektori -- pengecualian sengaja dari konvensi `_index.md` "
        "per-level di `AGENTS.md`, karena skala laman terlalu besar untuk diindeks "
        "manual per folder. Konten adalah hasil ekstraksi mentah dari "
        "https://quarto.org/docs/guide/, menggantikan dokumentasi manual versi lama "
        "yang kini ada di `_arsip-manual-lama/`.",
        "",
    ]
    for top in top_dirs:
        lines.append(f"## `{top}/`")
        lines.append("")
        sub_dirs = sorted(d for d in by_dir if d.parts and d.parts[0] == top)
        for d in sub_dirs:
            for title, rel_path in sorted(by_dir[d], key=lambda t: str(t[1])):
                lines.append(f"- [[{rel_path.as_posix()}|{title}]]")
        lines.append("")

    (output_dir / "_index.md").write_text("\n".join(lines), encoding="utf-8")


# ===================== MAIN =====================
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ekstraktor dokumentasi Quarto (docs/guide) -> Markdown.")
    p.add_argument("--seed-url", default=DEFAULT_SEED_URL, help="Laman sumber sidebar untuk discovery.")
    p.add_argument("--limit", type=int, help="Batasi jumlah laman (untuk uji coba).")
    p.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="Jeda antar-request (detik).")
    p.add_argument("--pages", nargs="+", help="URL laman tertentu (lewati discovery sidebar).")
    p.add_argument(
        "--pages-file",
        help="Berkas teks berisi URL laman, satu per baris (baris kosong/'#' diabaikan).",
    )
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Direktori keluaran.")
    p.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="Override User-Agent.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    global DEFAULT_DELAY
    DEFAULT_DELAY = args.delay

    output_dir = Path(args.output_dir).resolve()
    session = build_session(user_agent=args.user_agent)

    urls_from_args: list[str] = list(args.pages) if args.pages else []
    if args.pages_file:
        for line in Path(args.pages_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls_from_args.append(line)

    if urls_from_args:
        urls = urls_from_args
    else:
        print("Mengambil daftar laman via sidebar Guide ...")
        urls = discover_guide_pages(session, args.seed_url, output_dir)
        print(f"Ditemukan {len(urls)} laman.")

    if args.limit:
        urls = urls[: args.limit]

    ok, failed = 0, 0
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}]", end=" ")
        try:
            process_page(session, url, output_dir)
            ok += 1
        except Exception as exc:
            print(f"    ! gagal: {exc}", file=sys.stderr)
            failed += 1
        time.sleep(DEFAULT_DELAY)

    generate_root_index(output_dir)
    print(f"\nSelesai. Sukses: {ok}, Gagal: {failed}. Keluaran: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
