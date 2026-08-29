#let warna-utama = rgb("#003b59")
#let warna-sekunder = rgb("#d66b1f")
#let warna-latar = rgb("#e8f0f3")

#let in-mainmatter = state("in-mainmatter", false)
#let bag-counter = counter("bag-counter")

#let part(title) = {
  pagebreak(weak: true)
  bag-counter.step()
  context {
    let b = bag-counter.get().first()
    if b == 1 [
      #in-mainmatter.update(true)
      #counter(page).update(1)
    ]
  }
  counter(heading).update(0)
  v(35%)
  heading(level: 1, numbering: none, outlined: true, supplement: [Part])[#title]
  v(1fr)
  pagebreak()
}

#let pedoman(
  title: none,
  subtitle: none,
  authors: none,
  date: none,
  lang: "id",
  region: "ID",
  fontsize: 11pt,
  sectionnumbering: none,
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  mainfont: "Carlito",
  sansfont: "Playfair Display",
  monofont: "JetBrains Mono",
  doc,
) = {
  set document(title: title)
  set document(
    author: authors.map(author => content-to-string(author.name)).join(", ", last: " & "),
  ) if authors != none and authors != ()

  // Bagian depan (sampul, pengesahan, prakata, daftar isi) tidak bernomor.
  // Penomoran halaman dinyalakan kembali di `tentang-panduan.qmd`, tempat
  // halaman 1 buku ini dimulai.
  // Tambahan: pengaturan halaman; Romawi kecil sebelum Bagian 1, Angka Arab mulai Bagian 1
  set page(
    paper: "a4",
    margin: (x: 25mm, y: 25mm),
    footer: context {
      let is-main = in-mainmatter.get()
      let p = counter(page).get().first()
      align(center)[
        #if is-main {
          numbering("1", p) // Angka Arab: 1, 2, 3...
        } else {
          numbering("i", p) // Romawi kecil: i, ii, iii...
        }
      ]
    },
  )
  set text(font: (mainfont,), lang: lang, region: region, size: fontsize)
  set par(justify: true, leading: 0.72em)
  // Nomori bab, bagian, dan subbagian substantif (tiga tingkat). Tingkat
  // keempat ke bawah dipakai untuk daftar taksonomi seperti kelompok jenis
  // activities, dan sengaja dibiarkan tanpa nomor.
  set heading(numbering: (..nums) => {
    let values = nums.pos()
    if values.len() == 1 {
      numbering("1", ..values)
    } else if values.len() == 2 {
      numbering("1.1", ..values)
    } else if values.len() == 3 {
      numbering("1.1.1", ..values)
    } else {
      none
    }
  }) if sectionnumbering != none

  show heading: it => {
    // Judul Bagian ditandai `supplement: [Part]` oleh fungsi `#part` di
    // `_shared/typst-header.typ`; tampilannya kartu satu halaman penuh, bukan
    // kotak judul bab. Pemenggalan halamannya sudah diurus `#part`.
    let bagian = it.supplement == [Part]

    set text(
      font: (sansfont,),
      weight: "bold",
      fill: warna-utama,
      size: if bagian { 24pt }
        else if it.level == 1 { 22pt }
        else if it.level == 2 { 18.5pt }
        else if it.level == 3 { 16.5pt } // 1.5x dari ukuran teks normal (11pt)
        else if it.level == 4 { 13pt }
        else { 11pt },
    )

    if bagian {
      set par(justify: false)
      align(center)[
        #block(
          width: 100%,
          fill: warna-latar,
          stroke: (left: 4pt + warna-sekunder),
          inset: (x: 18pt, y: 24pt),
          radius: (right: 6pt),
          it,
        )
      ]
    } else if it.level == 1 {
      pagebreak(weak: true)
      block(
        width: 100%,
        above: 0pt,
        below: 1.4em,
        inset: (x: 10pt, y: 8pt),
        stroke: (left: 1.2pt + warna-utama, top: 1.2pt + warna-utama, bottom: 1.2pt + warna-utama),
        radius: (left: 8pt),
        it,
      )
    } else {
      let sp-above = if it.level == 2 { 2.4em }
        else if it.level == 3 { 2.0em }
        else { 1.6em }
      block(above: sp-above, below: 0.7em, sticky: true, it)
    }
  }

  // Daftar Isi: penomoran halaman dinamis (romawi untuk bagian depan, arab untuk isi utama)
  show outline.entry: it => {
    let loc = it.element.location()
    let is-main = in-mainmatter.at(loc)
    let p = counter(page).at(loc).first()
    let formatted-page = if is-main {
      numbering("1", p)
    } else {
      numbering("i", p)
    }
    let is-part = it.element.func() == heading and it.element.supplement == [Part]

    let num = if it.element.numbering != none {
      let nums = counter(heading).at(loc)
      let fn = it.element.numbering
      if type(fn) == function {
        fn(..nums)
      } else if type(fn) == str {
        numbering(fn, ..nums)
      } else {
        none
      }
    } else {
      none
    }

    let entry-content = [
      #if num != none and num != "" [#num #h(0.5em)]#it.element.body
      #box(width: 1fr, it.fill)
      #formatted-page
    ]

    if is-part {
      v(1.1em, weak: true)
      block(width: 100%, above: 0.8em, below: 0.4em)[
        #strong(link(loc, entry-content))
      ]
    } else {
      let indent = (it.level - 1) * toc_indent
      block(width: 100%, above: 0.4em, below: 0.4em)[
        #h(indent)
        #link(loc, entry-content)
      ]
    }
  }

  show raw: set text(font: (monofont,), features: ("liga": 0, "calt": 0))
  show link: set text(fill: warna-utama)

  // Sampul
  page(footer: none, margin: 0mm)[
    #align(center)[
      #v(16mm)
      #image("assets/images/logo-itera.png", width: 30mm)
      #v(30mm)
      #block(
        width: 150mm,
        fill: warna-latar,
        stroke: (left: 2pt + warna-sekunder),
        inset: (x: 15mm, y: 14mm),
      )[
        #set text(font: (sansfont,), fill: warna-utama)
        #set par(justify: false)
        #align(center)[
          #text(size: 22pt, weight: "bold")[#title]
        ]
        #if subtitle != none {
          v(7mm)
          align(center, text(size: 15pt, weight: "bold")[#subtitle])
        }
        #if authors != none and authors != () {
          v(12mm)
          set text(font: (mainfont,), fill: black, size: 11pt)
          align(center)[
            #for author in authors [
              #author.name \
            ]
          ]
        }
      ]
      #v(1fr)
      #v(15mm)
    ]
  ]
  counter(page).update(1) // Memulai nomor i dari Lembar Pengesahan

  // Daftar Isi tidak lagi dicetak di sini. Penempatannya mengikuti urutan
  // naskah: `#outline(...)` dipanggil dari `prakata.qmd`, sesudah Prakata.
  // Parameter `toc*` dibiarkan ada demi kecocokan dengan `typst-show.typ`.
  doc
}

#set table(inset: 6pt, stroke: none)
