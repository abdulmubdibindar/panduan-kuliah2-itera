<#
.SINOPSIS
    Merender pedoman menjadi laman HTML di docs/ untuk GitHub Pages.

.DESKRIPSI
    Dua langkah utama, dijalankan dari Guide/:

      1. `quarto render --to html --output-dir _book-laman`
         -> hasil sementara di dalam proyek, lalu dicerminkan ke docs/
      2. (opsional, -DenganPdf) `quarto render --to typst`
         -> Guide/_book/Panduan-Moodle-ITERA.pdf (terbitan resmi)

    Render HTML sengaja ditampung lebih dahulu di Guide/_book-laman, bukan
    langsung ke docs/. Bila output-dir menunjuk ke luar direktori proyek,
    Quarto menolak membersihkan berkas basi (mis. site_libs/ dan halaman bab
    yang sudah dihapus), sehingga laman bisa memuat sisa terbitan lama.

    PDF tidak dirender ulang secara bawaan karena PDF adalah terbitan resmi
    yang sudah di-commit; merendernya ulang hanya untuk menerbitkan laman akan
    mengubah berkas itu (paginasi dapat bergeser antar versi Quarto) tanpa ada
    perubahan isi. Pakai -DenganPdf bila isi pedoman memang baru diubah.

    Sesudah dicerminkan, PDF disalin ke docs/ supaya tombol "Unduh versi PDF"
    pada halaman depan bekerja, dan berkas .nojekyll ditulis agar GitHub Pages
    tidak memproses keluaran Quarto dengan Jekyll.

    docs/ adalah artefak render yang ikut di-commit, karena GitHub Pages
    menyajikan laman dari `main` -> `/docs`. Direktori itu dikecualikan dari
    robocopy pada sync-ke-github.ps1 (daftar /XD) supaya tidak terhapus ketika
    vault OneDrive dicerminkan ke repo.

.PARAMETER DenganPdf
    Render ulang PDF (Typst) sebelum menerbitkan laman.

.CONTOH
    powershell -File .\terbitkan-laman.ps1
    powershell -File .\terbitkan-laman.ps1 -DenganPdf
#>
[CmdletBinding()]
param(
    [switch]$DenganPdf
)

$ErrorActionPreference = "Stop"

$Akar  = $PSScriptRoot
$Guide = Join-Path $Akar "Guide"
$Situs = Join-Path $Guide "_book-laman"
$Docs  = Join-Path $Akar "docs"
$Pdf   = Join-Path $Guide "_book\Panduan-Moodle-ITERA.pdf"

if (-not (Get-Command quarto -ErrorAction SilentlyContinue)) {
    Write-Host "Quarto tidak ditemukan pada PATH. Pasang Quarto 1.9 atau lebih baru lebih dahulu." -ForegroundColor Red
    exit 1
}

Push-Location $Guide
try {
    if ($DenganPdf) {
        Write-Host "== Merender PDF (Typst) ==" -ForegroundColor Yellow
        quarto render --to typst
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Render PDF gagal (kode $LASTEXITCODE). docs/ tidak diubah." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "== Memakai PDF yang sudah ada di Guide/_book/ (pakai -DenganPdf untuk merender ulang) ==" -ForegroundColor DarkGray
    }

    Write-Host "`n== Merender laman HTML ==" -ForegroundColor Yellow
    quarto render --to html --output-dir $Situs
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Render HTML gagal (kode $LASTEXITCODE). docs/ tidak diubah." -ForegroundColor Red
        exit 1
    }

    # docs/ dibangun ulang dari nol supaya bab atau aset yang sudah dihapus
    # tidak tertinggal dan ikut terbit.
    Write-Host "`n== Mencerminkan hasil render ke docs/ ==" -ForegroundColor Yellow
    if (Test-Path $Docs) {
        Remove-Item $Docs -Recurse -Force
    }
    Copy-Item $Situs $Docs -Recurse

    if (Test-Path $Pdf) {
        Copy-Item $Pdf (Join-Path $Docs "Panduan-Moodle-ITERA.pdf") -Force
        Write-Host "PDF disalin ke docs/." -ForegroundColor DarkGray
    } else {
        Write-Host "PDF tidak ditemukan di $Pdf; tombol unduh akan menunjuk berkas yang belum ada. Jalankan ulang dengan -DenganPdf." -ForegroundColor Yellow
    }

    New-Item -ItemType File -Path (Join-Path $Docs ".nojekyll") -Force | Out-Null

    Write-Host "`nLaman siap di $Docs" -ForegroundColor Green
    Write-Host "Periksa docs\index.html, lalu commit dan push docs/ agar GitHub Pages membangun ulang." -ForegroundColor Green
} finally {
    Pop-Location
}
