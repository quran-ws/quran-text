# quran_text for Dart and Flutter

No dependencies. Ḥafṣ is bundled as a package asset; load it once.

```dart
import 'package:flutter/services.dart' show rootBundle;
import 'package:quran_text/quran_text.dart';

final m = await Mushaf.hafs(read: rootBundle.loadString);           // Flutter
final m = await Mushaf.hafs();                                       // Dart VM

m.ayah(2, 255).text;                                              // plain words
m.ayah(2, 255).render(marks: true, ayahMarks: true);            // with waqf marks and ۝٢٥٥
m.page(3).render(marks: true, ayahMarks: true, lines: true);
m.page(3).lines;                                                  // for a page layout
m.surah(112).ayahs;                                                 // [Ayah, …]
m.juz(30).firstAyah!.key;                                         // "78:1"
m.word(1, 4, 1).number;                                           // 11, the same word in every riwāyah
m.sajdat();                                                       // every āyah printed with ۩
m.search('مالك يوم الدين');                                       // [Span]

final w = Mushaf.fromJson(await rootBundle.loadString('assets/warsh.json'));   // another riwāyah, your asset
AyahMap.fromJson(json).convert(2, 255, 'warsh');                  // MappedAyah(2, 253, 'split', 254)
```

The font the text needs is bundled and declared in the package's pubspec, so
`TextStyle(fontFamily: m.font.family, package: 'quran_text')` renders every word.
For another riwāyah add its `.ttf` from `data/fonts/` to your own `fonts:`.

`marks` takes `true` or a set of `MarkKind` (`{MarkKind.waqf}`). Wrong numbers
throw `RangeError`; a layer the file lacks (juz in Bazzī) throws `StateError`
with the reason from the file. The full API is in [`../README.md`](../README.md).

Test: `dart test` in this directory.
