# quran-text for Kotlin

Android and JVM, Ḥafṣ bundled. Depends on `org.json` only, which Android ships.

```kotlin
import org.quranpedia.qurantext.*

val m = Mushaf.hafs()                                                // bundled Ḥafṣ

m.ayah(2, 255).text                                                  // plain words
m.ayah(2, 255).render(marks = MarkKind.all, ayahMarks = true)      // with waqf marks and ۝٢٥٥
m.page(3).render(marks = setOf(MarkKind.waqf), ayahMarks = true, lines = true)
m.page(3).lines                                                      // for a page layout
m.surah(112).ayahs                                                     // List<Ayah>
m.juz(30).firstAyah?.key                                             // "78:1"
m.word(1, 4, 1).number                                               // 11, the same word in every riwāyah
m.sajdat()                                                           // every āyah printed with ۩
m.search("مالك يوم الدين")                                           // List<Span>

val w = Mushaf.fromJson(assets.open("warsh.json").bufferedReader().readText())   // another riwāyah, Android
val w = Mushaf.load(File("out/mushaf/warsh.json"))                              // another riwāyah, JVM
AyahMap.load(File("out/ayah-map.json")).convert(2, 255, "warsh")     // MappedAyah(2, 253, "split", 254)
```

The font the text needs is bundled too: `m.font.family` names it and
`m.font.open()` streams the `.ttf` (copy it to a file for `Typeface.createFromFile`).
For another riwāyah put its `.ttf` from `out/fonts/` in `assets/`.

Wrong numbers throw `IllegalArgumentException`; a layer the file lacks (juz in
Bazzī) throws `IllegalStateException` with the reason from the file. The full
API is in [`../README.md`](../README.md).

Test: `gradle test` in this directory (`-Dquran.out=…` to point at another `out/`).
