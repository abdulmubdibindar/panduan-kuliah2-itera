// Penyesuaian bersama buku Pedoman Moodle ITERA.
// Berlaku untuk Quarto 1.9.38 dan Typst 0.14.2.

#show figure: set block(breakable: true)
#show heading: set text(font: "Playfair Display", fill: rgb("#003b59"))
#show link: set text(fill: rgb("#003b59"))
#show raw: set text(features: ("liga": 0, "calt": 0))

// Callout memakai definisi bawaan Quarto. Edisi pertama menjaga isi setiap
// callout tetap pendek; fungsi pengganti dari Quarto 1.9.38 tidak disalin
// karena gagal dikompilasi sebagai header mandiri pada Typst 0.14.2.

// State untuk membedakan bagian depan (romawi) dan isi utama (angka arab)
#let in-mainmatter = state("in-mainmatter", false)
#let bag-counter = counter("bag-counter")

// Judul Bagian (part) ditulis sebagai heading tingkat 1 tanpa nomor supaya ikut
// terbaca oleh mesin `#outline` dan muncul sebagai entri "Bagian ..." di Daftar
// Isi. Penandanya adalah `supplement: [Bagian]` — bukan label — karena field
// `supplement` selalu dapat dibaca di dalam show rule dan tidak menimbulkan
// label kembar ketika buku memuat lebih dari satu Bagian. Tampilan kartu satu
// halaman penuhnya diatur oleh `show heading` di `_shared/typst/typst-template.typ`.
#let part(title) = {
  pagebreak(weak: true)
  bag-counter.step()
  context {
    // Hanya saat Bagian I dipanggil pertama kali: aktifkan mainmatter & reset halaman ke 1
    if bag-counter.get().first() == 1 {
      in-mainmatter.update(true)
      counter(page).update(1)
    }
  }
  counter(heading).update(0)
  v(35%)
  heading(level: 1, numbering: none, outlined: true, supplement: [Part])[#title]
  v(1fr)
  pagebreak()
}
