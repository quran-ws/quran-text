# QuranText for Swift

Swift Package, Foundation only, Ḥafṣ bundled. iOS 13+, macOS 10.15+.

```swift
import QuranText

let m = try Mushaf.hafs()                                        // bundled Ḥafṣ

m.ayah(2, 255).text                                              // plain words
m.ayah(2, 255).render(marks: .all, ayahMarks: true)            // with waqf marks and ۝٢٥٥
m.page(3).render(marks: [.waqf], ayahMarks: true, lines: true)
m.page(3).lines                                                  // for a page layout
m.surah(112).ayahs                                                 // [Ayah]
m.juz(30)?.firstAyah?.key                                        // "78:1"
m.word(1, 4, 1).number                                           // 11, the same word in every riwāyah
m.sajdat()                                                       // every āyah printed with ۩
m.search("مالك يوم الدين")                                       // [Span]

let w = try Mushaf.load(Bundle.main.url(forResource: "warsh", withExtension: "json")!)   // another riwāyah
try AyahMap.load(url).convert(2, 255, to: "warsh")               // MappedAyah(surah: 2, ayah: 253, relation: "split", ayahLast: 254)
```

The font the text needs is bundled too: register `m.font.url` with
`CTFontManagerRegisterFontsForURL` and use `Font.custom(m.font.family, size:)`.
For another riwāyah add its `.ttf` from `data/fonts/` to your app.

Lookups by number are checked with `precondition`, like array subscripts.
Layers a file may lack come back as `nil`: `bazzi.juz(1)` is `nil` and
`whyAbsent("juz")` says why. Waqf marks are combining characters, so inspect
`unicodeScalars` rather than `Character`s when you need to find one in rendered
text. The full API is in [`../README.md`](../README.md).

Test: `swift test` in this directory.
