# quran-text for JavaScript

ESM, no dependencies, TypeScript declarations included, Ḥafṣ bundled. Works
in Node, the browser and React Native.

```js
import { Mushaf, AyahMap } from "@quran.ws/text";

const m = await Mushaf.hafs();                                 // bundled Ḥafṣ

m.ayah(2, 255).text                                            // plain words
m.ayah(2, 255).render({ marks: true, ayahMarks: true })      // with waqf marks and ۝٢٥٥
m.page(3).render({ marks: true, ayahMarks: true, lines: true })
m.surah(112).ayahs                                               // [Ayah, …]
m.juz(30).firstAyah.key                                        // "78:1"
m.word(1, 4, 1).number                                         // 11, the same word in every riwāyah
m.sajdat()                                                     // every āyah printed with ۩
m.search("مالك يوم الدين")                                     // [Span]

const w = await Mushaf.load("data/mushaf/warsh.json");          // another riwāyah, Node
const w = Mushaf.fromJson(await (await fetch(url)).json());    // another riwāyah, browser / React Native
(await AyahMap.load("data/ayah-map.json")).convert(2, 255, "warsh")   // { surah: 2, ayah: 253, ayahLast: 254, relation: "split" }
```

The font the text needs is bundled too: add `m.fontFace()` to a stylesheet and
use `m.font.family`. For another riwāyah pass its `data/fonts/` URL to `fontFace(url)`.

Wrong numbers throw `RangeError`; a layer the file lacks (juz in Bazzī) throws
with the reason from the file. The full API is in [`../README.md`](../README.md).

Test: `node --test` in this directory.
