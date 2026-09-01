# Cross-riwayah comparison

Generated 2026-09-02 from the KFGQPC packages in `data/`. 77,434 canonical kalimahs across 114 surahs and 7 riwayahs.

Every kalimah carries one ID that means the same kalimah in every riwayah that has it. Where the riwayahs disagree, the disagreement is recorded against that ID rather than hidden by it.

## What is being compared

A kalimah is never compared as raw text. Four forms are derived from every spelling, each stripping one more layer of what a scribe added after the mushafs were written. Two riwayahs are said to agree *at a level* when their forms at that level are identical.

| form | question it answers | example | and what it drops |
|---|---|---|---|
| `uthmani` | how is it printed? | `ٱلرَّحۡمَٰنِ` | — |
| `folded` | what does it say, ignoring which codepoints the release chose? | `الرَّحْمَٰنِ` | release notation, attached-alef harfs, editorial marks |
| `pointed` | which harfs, dots and all? | `الرحمان` | vowels, hamza, madd, ṣilah |
| `rasm` | what is on the line in the mushaf? | `الرحماں` | the dots |

The two skeletons are separate on purpose. `تَعۡمَلُونَ` and `يَعۡمَلُونَ` have different `pointed` forms but one `rasm` — `ٮعملوں` — because the mushafs were written undotted and carry both qira'ahs by design. Calling that a rasm variant would be a category error; calling it vowelling would hide a real qira'ah. It is named **`dotting_variant`**.

`rasm` drops hamza and every hamza carrier reduces to its seat, because hamza is post-Uthmani notation: `يَسۡتَهۡزِئُ` and `يَسْتَهْزِۓُ` are one kalimah. It also drops the dagger alif, which is by definition an alef the scribe did *not* write on the line, so `هَٰرُوتَ` and `هَارُوتَ` do **not** share a rasm: `هروٮ` against `هاروٮ`. That difference is real inside any one mushaf and is kept, but between these two typesettings it is a house style rather than a mushaf — see [the ā on the line or above it](#the-ā-on-the-line-or-above-it).

## The riwayahs

| key | riwayah | الرواية | qari | counting | ayahs | kalimahs |
|---|---|---|---|---|---|---|
| hafs | Ḥafṣ | حفص | ʿĀṣim al-Kūfī | kufi | 6,236 | 77,432 |
| shuba | Shuʿbah | شعبة | ʿĀṣim al-Kūfī | kufi | 6,236 | 77,432 |
| warsh | Warsh | ورش | Nāfiʿ al-Madanī | madani | 6,214 | 77,431 |
| qaloun | Qālūn | قالون | Nāfiʿ al-Madanī | madani | 6,214 | 77,431 |
| douri | Dūrī | الدوري | Abū ʿAmr al-Baṣrī | basri | 6,217 | 77,431 |
| sousi | Sūsī | السوسي | Abū ʿAmr al-Baṣrī | basri | 6,218 | 77,431 |
| bazzi | Bazzī | البزي | Ibn Kathīr al-Makkī | makki | 6,220 | 77,432 |

The ayah totals are not errors and not deducible from the qari. Many fasilahs are مختلف فيها, so every printed mushaf chooses, and the `counting` column above is a conventional label rather than a claim about this package. That is exactly why the index is flat, and why the ayah boundaries are read off each mushaf rather than assumed: see [the fasilahs](#fasilahs-where-the-ayahs-end) below.

## How the kalimahs compare

| status | kalimahs | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.38% | one qira'ah, one spelling, in all seven |
| `diacritic_variant` | 36,261 | 46.83% | same harfs and same dots — the vowelling differs |
| `dotting_variant` | 338 | 0.44% | one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ |
| `alif_variant` | 198 | 0.26% | one skeleton, one ā: on the line in one hand, above it in the other |
| `rasm_variant` | 62 | 0.08% | the mushafs disagree about the harfs on the line |
| `kalimah_boundary` | 12 | 0.02% | a source prints the kalimah joined to its neighbour |
| `partial` | 5 | 0.01% | the kalimah is absent from at least one riwayah |

Each kalimah gets the *strongest* label that applies, tested in this order: rasm, ā, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed to share one rasm across all seven, an `alif_variant` to share one skeleton once every ā is spelled out, and an `identical` kalimah is identical after notation folding — the raw spelling of every riwayah is always kept in `forms`, whatever the label.

## Pairwise agreement

Share of the kalimahs two riwayahs both have, where they agree at each level.

| pair | shared kalimahs | same spelling | same qira'ah | same harfs | same rasm |
|---|---|---|---|---|---|
| douri–sousi | 77,431 | 66.7% | 82.8% | 99.97% | 100.00% |
| warsh–qaloun | 77,431 | 85.2% | 87.5% | 99.95% | 99.99% |
| hafs–shuba | 77,432 | 99.2% | 99.2% | 99.86% | 99.99% |
| shuba–douri | 77,430 | 70.9% | 74.1% | 99.76% | 99.98% |
| shuba–sousi | 77,430 | 72.1% | 72.9% | 99.73% | 99.98% |
| shuba–bazzi | 77,431 | 84.1% | 84.1% | 99.75% | 99.97% |
| hafs–douri | 77,430 | 70.8% | 74.1% | 99.74% | 99.97% |
| douri–bazzi | 77,430 | 57.8% | 61.0% | 99.84% | 99.97% |
| hafs–bazzi | 77,431 | 84.0% | 84.0% | 99.73% | 99.97% |
| hafs–sousi | 77,430 | 72.0% | 72.8% | 99.71% | 99.97% |
| sousi–bazzi | 77,430 | 66.6% | 67.4% | 99.81% | 99.97% |
| hafs–warsh | 77,430 | 41.3% | 75.2% | 99.72% | 99.70% |
| shuba–warsh | 77,430 | 41.4% | 75.2% | 99.73% | 99.70% |
| warsh–bazzi | 77,430 | 37.2% | 63.4% | 99.73% | 99.70% |
| warsh–douri | 77,430 | 37.8% | 76.3% | 99.72% | 99.70% |
| warsh–sousi | 77,430 | 39.2% | 77.7% | 99.74% | 99.69% |
| hafs–qaloun | 77,430 | 40.4% | 76.6% | 99.76% | 99.69% |
| shuba–qaloun | 77,430 | 40.5% | 76.6% | 99.77% | 99.69% |
| qaloun–bazzi | 77,430 | 41.5% | 70.8% | 99.76% | 99.69% |
| qaloun–douri | 77,430 | 36.8% | 78.5% | 99.75% | 99.69% |
| qaloun–sousi | 77,430 | 42.6% | 84.4% | 99.72% | 99.69% |

Rasm agreement never drops below 99.5%: the seven riwayahs are one text. Spelling agreement is far lower because the packages were typeset in different years with different conventions — which is what the `folded` and `pointed` columns strip away.

## Where the riwayahs genuinely disagree

Three things can differ once spelling, vowelling and pointing are set aside: the harfs, the kalimah boundaries, and whether a kalimah is there at all. Together they account for 79 of 77,434 kalimahs. A fourth kind is listed with them and counted apart: 198 kalimahs where the disagreement is only about whether an ā sits on the line or above it.

| kind | count | status | what it means |
|---|---|---|---|
| harfs differ | 62 | `rasm_variant` | a harf one mushaf has on the line and another does not — 56 of them one harf more, 6 one harf for another |
| the ā is placed differently | 198 | `alif_variant` | one skeleton once every ā is spelled out; the two hands disagree about which ā to write on the line |
| boundaries differ | 6 events | `kalimah_boundary` | one source prints two kalimahs as one |
| kalimah absent | 5 | `partial` | a riwayah does not have the kalimah at all |

### Harfs — rasm disagreements

62 kalimahs where the riwayahs disagree about the harfs on the line, after dots, hamza, vowelling and the ā have all been set aside. These are the differences the sources can be trusted on: they split the seven riwayahs 14 different ways — by miṣr, not by publisher — and they are the khilāf the rasm literature names. All 62 are listed below, grouped by what the difference *is*. Machine-readable: [`rasm-variants.md`](rasm-variants.md), [`conflicts.csv`](conflicts.csv).

#### One skeleton, one harf more

56 of the 62. Both sides write the same harfs in the same order and one side writes a harf the other does not: `ٮرٮد`/`ٮرٮدد` — يَرۡتَدَّ against يَرۡتَدِدۡ at 5:54 — or `ٮسٮهى`/`ٮسٮهٮه`, تَشۡتَهِي against تَشۡتَهِيهِ at 43:71. Nothing is replaced; the skeletons nest.

| kalimah id | surah:ayah | rasm on each side | as printed |
|---|---|---|---|
| 2331 | 2:132 | `ووصى` hafs,shuba,bazzi,douri,sousi  ·  `واوصى` qaloun,warsh | **وَوَصَّىٰ** hafs,shuba,bazzi,douri,sousi  ·  **وَأَوْصَىٰ** qaloun  ·  **وَأَوْصٜىٰ** warsh |
| 8353 | 3:133 | `وسارعوا` hafs,shuba,bazzi,douri,sousi  ·  `سارعوا` qaloun,warsh | **وَسَارِعُوٓاْ** hafs,shuba,douri  ·  **وَسَارِعُواْ** bazzi,sousi  ·  **سَارِعُواْ** qaloun  ·  **سَارِعُوٓاْ** warsh |
| 8851 | 3:158 | `لالى` hafs,shuba,bazzi,qaloun,warsh  ·  `لاالى` douri,sousi | **لَإِلَى** hafs,shuba,bazzi,qaloun,warsh  ·  **لَإِاْلَى** douri,sousi |
| 14726 | 5:53 | `وٮڡول` hafs,shuba,douri,sousi  ·  `ٮڡول` bazzi,qaloun,warsh | **وَيَقُولُ** hafs,shuba  ·  **يَقُولُ** bazzi,qaloun,warsh  ·  **وَيَقُولَ** douri,sousi |
| 14745 | 5:54 | `ٮرٮد` hafs,shuba,bazzi,douri,sousi  ·  `ٮرٮدد` qaloun,warsh | **يَرۡتَدَّ** hafs,shuba,bazzi,douri,sousi  ·  **يَّرْتَدِدْ** qaloun,warsh |
| 17215 | 6:63 | `اٮحٮٮا` hafs,shuba  ·  `اٮحٮٮٮا` bazzi,qaloun,warsh,douri,sousi | **أَنجَىٰنَا** hafs,shuba  ·  **أَنجَيۡتَنَا** bazzi,douri,sousi  ·  **أَنجَيْتَنَا** qaloun  ·  **ࡰنجَيْتَنَا** warsh |
| 18334 | 6:124 | `رسالٮه` hafs,bazzi  ·  `رسلٮه` shuba,qaloun,warsh,douri,sousi | **رِسَالَتَهُۥ** hafs,bazzi  ·  **رِسَٰلَٰتِهِۦ** shuba,qaloun,warsh,douri  ·  **رِّسَٰلَٰتِهِۦ** sousi |
| 19696 | 7:34 | `ٮسٮاحروں` hafs,shuba,bazzi,douri,sousi  ·  `ٮسٮحروں` qaloun,warsh | **يَسۡتَأۡخِرُونَ** hafs,shuba,bazzi,douri  ·  **يَسْتَْٔخِرُونَ** qaloun  ·  **يَسْتَٰخِرُونَ** warsh  ·  **يَسۡتَاخِرُونَ** sousi |
| 21416 | 7:144 | `ٮرسلٮى` hafs,shuba,douri,sousi  ·  `ٮرسالٮى` bazzi,qaloun,warsh | **بِرِسَٰلَٰتِي** hafs,shuba,douri,sousi  ·  **بِرِسَالَتِي** bazzi  ·  **بِرِسَالَتِے** qaloun,warsh |
| 23200 | 8:42 | `حى` hafs,douri,sousi  ·  `حٮى` shuba,bazzi,qaloun,warsh | **حَيَّ** hafs,douri,sousi  ·  **حَِۧيَ** shuba,bazzi  ·  **حَۑِيَ** qaloun  ·  **حَيِيَ** warsh |
| 24700 | 9:47 | `ولاوصعوا` hafs,shuba,bazzi,qaloun,warsh  ·  `ولااوصعوا` douri,sousi | **وَلَأَوۡضَعُواْ** hafs,shuba,bazzi  ·  **وَلَأَوْضَعُواْ** qaloun,warsh  ·  **وَلَأَاْوۡضَعُواْ** douri,sousi |
| 25793 | 9:107 | `والدٮں` hafs,shuba,bazzi,douri,sousi  ·  `الدٮں` qaloun,warsh | **وَٱلَّذِينَ** hafs,shuba,bazzi  ·  **ࡴ۬لذِينَ** qaloun,warsh  ·  **وَاَلَّذِينَ** douri  ·  **وَࡱلَّذِينَ** sousi |
| 31777 | 12:110 | `ڡٮحى` hafs,shuba,bazzi,douri,sousi  ·  `ڡٮٮحى` qaloun,warsh | **فَنُجِّيَ** hafs,shuba  ·  **فَنُۨجِي** bazzi,douri,sousi  ·  **فَنُنجِے** qaloun,warsh |
| 37273 | 17:93 | `ڡل` hafs,shuba,qaloun,warsh,douri,sousi  ·  `ڡال` bazzi | **قُلۡ** hafs,shuba,douri,sousi  ·  **قَالَ** bazzi  ·  **قُلْ** qaloun,warsh |
| 38135 | 18:36 | `مٮها` hafs,shuba,douri,sousi  ·  `مٮهما` bazzi,qaloun,warsh | **مِّنۡهَا** hafs,shuba,douri,sousi  ·  **مِّنۡهُمَا** bazzi  ·  **مِّنْهُمَا** qaloun,warsh |
| 38936 | 18:95 | `مكٮى` hafs,shuba,qaloun,warsh,douri,sousi  ·  `مكٮٮى` bazzi | **مَكَّنِّي** hafs,shuba,douri,sousi  ·  **مَكَّنَنِي** bazzi  ·  **مَكَّنِّے** qaloun,warsh |
| 39298 | 19:19 | `لاهٮ` hafs,shuba,bazzi,qaloun,warsh,douri  ·  `لاٮهٮ` sousi | **لِأَهَبَ** hafs,shuba,bazzi,qaloun  ·  **لِاَهَبَ** warsh  ·  **لِاَ۬هَبَ** douri  ·  **لِاَۧهَبَ** sousi |
| 41131 | 20:112 | `ٮحاڡ` hafs,shuba,qaloun,warsh,douri,sousi  ·  `ٮحڡ` bazzi | **يَخَافُ** hafs,shuba,qaloun,warsh,douri,sousi  ·  **يَخَفۡ** bazzi |
| 41455 | 21:4 | `ڡال` hafs  ·  `ڡل` shuba,bazzi,qaloun,warsh,douri,sousi | **قَالَ** hafs  ·  **قُل** shuba,bazzi,qaloun,warsh,douri,sousi |
| 41720 | 21:30 | `اولم` hafs,shuba,qaloun,warsh,douri,sousi  ·  `الم` bazzi | **أَوَلَمۡ** hafs,shuba,douri,sousi  ·  **أَلَمۡ** bazzi  ·  **أَوَلَمْ** qaloun,warsh |
| 42341 | 21:88 | `ٮحى` hafs,shuba,bazzi,douri,sousi  ·  `ٮٮحى` qaloun,warsh | **نُۨجِي** hafs,bazzi,douri,sousi  ·  **نُجِّي** shuba  ·  **نُنجِے** qaloun,warsh |
| 44635 | 23:87 | `لله` hafs,shuba,bazzi,qaloun,warsh  ·  `الله` douri,sousi | **لِلَّهِ** hafs,shuba,bazzi  ·  **لِلهِ** qaloun,warsh  ·  **اَ۬للَّهُ** douri  ·  **ࡱ۬للَّهُ** sousi |
| 44654 | 23:89 | `لله` hafs,shuba,bazzi,qaloun,warsh  ·  `الله` douri,sousi | **لِلَّهِ** hafs,shuba,bazzi  ·  **لِلهِ** qaloun,warsh  ·  **اَ۬للَّهُ** douri  ·  **ࡱ۬للَّهُ** sousi |
| 44847 | 23:112 | `ڡل` hafs,shuba,bazzi,douri,sousi  ·  `ڡال` qaloun,warsh | **قَٰلَ** hafs,shuba,douri,sousi  ·  **قُلۡ** bazzi  ·  **قَالَ** qaloun,warsh |
| 46555 | 25:25 | `وٮرل` hafs,shuba,qaloun,warsh,douri,sousi  ·  `وٮٮرل` bazzi | **وَنُزِّلَ** hafs,shuba,qaloun,warsh,douri,sousi  ·  **وَنُنزِلُ** bazzi |
| 48694 | 27:21 | `لٮاٮٮٮى` hafs,shuba,qaloun,warsh,douri,sousi  ·  `لٮاٮٮٮٮى` bazzi | **لَيَأۡتِيَنِّي** hafs,shuba,douri  ·  **لَيَأۡتِيَنَّنِي** bazzi  ·  **لَيَأْتِيَنِّے** qaloun  ·  **لَيَاتِيَنِّے** warsh  ·  **لَيَاتِيَنِّي** sousi |
| 48852 | 27:36 | `اٮٮں` hafs,shuba,bazzi,douri,sousi  ·  `اٮٮٮى` qaloun,warsh | **ءَاتَىٰنِۦَ** hafs,douri,sousi  ·  **ءَاتَىٰنِ** shuba,bazzi  ·  **ءَاتَيٰنِࣉَ** qaloun  ·  **ءَاتٜيٰنِࣉَ** warsh |
| 50187 | 28:37 | `وڡال` hafs,shuba,qaloun,warsh,douri,sousi  ·  `ڡال` bazzi | **وَقَالَ** hafs,shuba,qaloun,warsh,douri,sousi  ·  **قَالَ** bazzi |
| 50378 | 28:48 | `سحراں` hafs,shuba,bazzi,douri,sousi  ·  `سحرں` qaloun,warsh | **سِحۡرَانِ** hafs,shuba  ·  **سَٰحِرَانِ** bazzi,douri,sousi  ·  **سَٰحِرَٰنِ** qaloun,warsh |
| 52070 | 30:8 | `ٮلڡاى` hafs,shuba,bazzi,douri,sousi  ·  `ٮلڡا` qaloun,warsh | **بِلِقَآيِٕ** hafs,shuba,bazzi,douri,sousi  ·  **بِلِقَآءِ** qaloun,warsh |
| 52159 | 30:16 | `ولڡاى` hafs,shuba,bazzi,douri,sousi  ·  `ولڡا` qaloun,warsh | **وَلِقَآيِٕ** hafs,shuba,bazzi,douri,sousi  ·  **وَلِقَآءِ** qaloun,warsh |
| 53776 | 33:4 | `الى` hafs,shuba,bazzi,warsh,douri,sousi  ·  `الٮى` qaloun | **ٱلَِّٰٓٔي** hafs,shuba  ·  **ٱلَّٰٓيۡ** bazzi  ·  **ࡲ۬لَّٰٓئِے** qaloun  ·  **ࡲ۬لٜےْ** warsh  ·  **اُ۬لَّٰٓيۡ** douri  ·  **ࡲ۬لَّٰٓيۡ** sousi |
| 56602 | 35:43 | `السٮى` hafs,shuba,bazzi,warsh,douri,sousi  ·  `السٮٮى` qaloun | **ٱلسَّيِّيِٕ** hafs,shuba,bazzi  ·  **ࡰ۬لسَّيِّئِے** qaloun  ·  **ࡰ۬لسَّيِّےِٕ** warsh  ·  **اَ۬لسَّيِّيِٕ** douri  ·  **ࡱ۬لسَّيِّيِٕ** sousi |
| 56964 | 36:35 | `عملٮه` hafs,bazzi,qaloun,warsh,douri,sousi  ·  `عملٮ` shuba | **عَمِلَتۡهُ** hafs,douri,sousi  ·  **عَمِلَتۡ** shuba  ·  **عَمِلَتۡهُۥ** bazzi  ·  **عَمِلَتْهُ** qaloun,warsh |
| 57749 | 37:68 | `لالى` hafs,shuba,bazzi,qaloun,warsh  ·  `لاالى` douri,sousi | **لَإِلَى** hafs,shuba,bazzi,qaloun,warsh  ·  **لَإِاْلَى** douri,sousi |
| 59548 | 39:34 | `حرا` hafs,shuba,bazzi,douri,sousi  ·  `حروا` qaloun,warsh | **جَزَآءُ** hafs,shuba,bazzi,douri,sousi  ·  **جَزَٰٓؤُاْ** qaloun,warsh |
| 60056 | 39:69 | `وحاى` hafs,shuba,bazzi,douri,sousi  ·  `وحى` qaloun,warsh | **وَجِاْيٓءَ** hafs,shuba,bazzi,douri,sousi  ·  **وَجِےٓءَ** qaloun,warsh |
| 62695 | 42:30 | `ڡٮما` hafs,shuba,bazzi,douri,sousi  ·  `ٮما` qaloun,warsh | **فَبِمَا** hafs,shuba,bazzi,douri,sousi  ·  **بِمَا** qaloun,warsh |
| 63696 | 43:68 | `ٮعٮاد` hafs,bazzi  ·  `ٮعٮادى` shuba,qaloun,warsh,douri,sousi | **يَٰعِبَادِ** hafs,bazzi  ·  **يَٰعِبَادِيَ** shuba  ·  **يَٰعِبَادِے** qaloun,warsh  ·  **يَٰعِبَادِي** douri,sousi |
| 63722 | 43:71 | `ٮسٮهٮه` hafs,qaloun,warsh  ·  `ٮسٮهى` shuba,bazzi,douri,sousi | **تَشۡتَهِيهِ** hafs  ·  **تَشۡتَهِي** shuba,bazzi,douri,sousi  ·  **تَشْتَهِيهِ** qaloun,warsh |
| 64932 | 46:15 | `احسٮا` hafs,shuba  ·  `حسٮا` bazzi,qaloun,warsh,douri,sousi | **إِحۡسَٰنًا** hafs,shuba  ·  **حُسۡنًا** bazzi,douri,sousi  ·  **حُسْناً** qaloun,warsh |
| 68622 | 55:22 | `اللولو` hafs,shuba,bazzi,douri,sousi  ·  `اللولوا` qaloun,warsh | **ٱللُّؤۡلُؤُ** hafs,bazzi  ·  **ٱللُّولُؤُ** shuba  ·  **ࡰ۬للُّؤْلُؤُاْ** qaloun,warsh  ·  **اَ۬للُّؤۡلُؤُ** douri  ·  **ࡱ۬للُّولُؤُ** sousi |
| 69876 | 58:2 | `الى` hafs,shuba,bazzi,warsh,douri,sousi  ·  `الٮى` qaloun | **ٱلَِّٰٓٔي** hafs,shuba  ·  **ٱلَّٰٓيۡ** bazzi  ·  **ࡰ۬لَّٰٓئِے** qaloun  ·  **ࡰ۬لٜےْ** warsh  ·  **اَ۬لَّٰٓيۡ** douri  ·  **ࡱ۬لَّٰٓيۡ** sousi |
| 70587 | 59:13 | `لاٮٮم` hafs,shuba,bazzi,qaloun,warsh  ·  `لااٮٮم` douri,sousi | **لَأَنتُمۡ** hafs,shuba  ·  **لَأَنتُمُۥ** bazzi  ·  **لَأَنتُمْ** qaloun  ·  **لَأَنتُمُۥٓ** warsh  ·  **لَأَاْنتُمۡ** douri,sousi |
| 71302 | 61:14 | `اٮصار` hafs,shuba  ·  `اٮصارا` bazzi,qaloun,warsh,douri,sousi | **أَنصَارَ** hafs,shuba  ·  **أَنصَارࣰا** bazzi,sousi  ·  **أَنصَاراࣰ** qaloun,warsh  ·  **أَنصَارٗا** douri |
| 71303 | 61:14 | `الله` hafs,shuba  ·  `لله` bazzi,qaloun,warsh,douri,sousi | **ٱللَّهِ** hafs,shuba  ·  **لِّلَّهِ** bazzi,douri,sousi  ·  **لِّلهِ** qaloun,warsh |
| 72021 | 65:4 | `والى` hafs,shuba,bazzi,warsh,douri,sousi  ·  `والٮى` qaloun | **وَٱلَِّٰٓٔي** hafs,shuba  ·  **وَٱلَّٰٓيۡ** bazzi  ·  **وَالَّٰٓئِے** qaloun  ·  **وَالٜےْ** warsh  ·  **وَاَلَّٰٓيۡ** douri  ·  **وَࡱلَّٰٓيۡ** sousi |
| 72032 | 65:4 | `والى` hafs,shuba,bazzi,warsh,douri,sousi  ·  `والٮى` qaloun | **وَٱلَِّٰٓٔي** hafs,shuba  ·  **وَٱلَّٰٓيۡ** bazzi  ·  **وَالَّٰٓئِے** qaloun  ·  **وَالٜےْ** warsh  ·  **وَاَلَّٰٓيۡ** douri  ·  **وَࡱلَّٰٓيۡ** sousi |
| 73986 | 72:20 | `ڡل` hafs,shuba  ·  `ڡال` bazzi,qaloun,warsh,douri,sousi | **قُلۡ** hafs,shuba  ·  **قَالَ** bazzi,qaloun,warsh,douri,sousi |
| 74226 | 73:20 | `اں` hafs,shuba,bazzi,qaloun,warsh  ·  `الں` douri,sousi | **أَن** hafs,shuba,bazzi,qaloun,warsh  ·  **أَلَّن** douri,sousi |
| 74439 | 74:33 | `اد` hafs,qaloun,warsh  ·  `ادا` shuba,bazzi,douri,sousi | **إِذۡ** hafs  ·  **إِذَا** shuba,bazzi,douri,sousi  ·  **إِذْ** qaloun  ·  **إِذَ** warsh |
| 74440 | 74:33 | `ادٮر` hafs,qaloun,warsh  ·  `دٮر` shuba,bazzi,douri,sousi | **أَدۡبَرَ** hafs  ·  **دَبَرَ** shuba,bazzi,douri,sousi  ·  **أَدْبَرَ** qaloun  ·  **ࡰدْبَرَ** warsh |
| 75690 | 81:24 | `ٮصٮٮں` hafs,shuba,qaloun,warsh  ·  `ٮصطٮٮں` bazzi,douri,sousi | **بِضَنِينࣲ** hafs,shuba,qaloun,warsh  ·  **بِضظَنِينࣲ** bazzi  ·  **بِضظَنِينٖ** douri  ·  **بِّضظَنِينࣲ** sousi |
| 76508 | 89:23 | `وحاى` hafs,shuba,bazzi,douri,sousi  ·  `وحى` qaloun,warsh | **وَجِاْيٓءَ** hafs,shuba,bazzi,douri,sousi  ·  **وَجِےٓءَ** qaloun,warsh |
| 76592 | 90:14 | `اطعم` hafs,shuba,bazzi,douri,sousi  ·  `اطعام` qaloun,warsh | **إِطۡعَٰمࣱ** hafs,shuba  ·  **أَطۡعَمَ** bazzi,douri,sousi  ·  **إِطْعَامࣱ** qaloun  ·  **ࡴطْعَامࣱ** warsh |
| 77259 | 106:2 | `الڡهم` hafs,shuba,bazzi,douri,sousi  ·  `اٮلڡهم` qaloun,warsh | **إِۦلَٰفِهِمۡ** hafs,shuba,douri,sousi  ·  **إِۦلَٰفِهِمُۥ** bazzi  ·  **إِيلَٰفِهِمْ** qaloun  ·  **ࡴيلَٰفِهِمْ** warsh |

#### One harf for another

6 of the 62, where a harf is not added but exchanged — `ولا`/`ڡلا` (وَلَا against فَلَا, 91:15), `كلمٮ`/`كلمه` (the open against the tied tāʾ, 7:137).

| kalimah id | surah:ayah | rasm on each side | as printed |
|---|---|---|---|
| 21269 | 7:137 | `كلمٮ` hafs,shuba,bazzi,douri,sousi  ·  `كلمه` qaloun,warsh | **كَلِمَتُ** hafs,shuba,bazzi,douri,sousi  ·  **كَلِمَةُ** qaloun,warsh |
| 48378 | 26:217 | `وٮوكل` hafs,shuba,bazzi,douri,sousi  ·  `ڡٮوكل` qaloun,warsh | **وَتَوَكَّلۡ** hafs,shuba,bazzi,douri,sousi  ·  **فَتَوَكَّلْ** qaloun,warsh |
| 60522 | 40:26 | `او` hafs,shuba  ·  `واں` bazzi,qaloun,warsh,douri,sousi | **أَوۡ** hafs,shuba  ·  **وَأَن** bazzi,douri,sousi  ·  **وَأَنْ** qaloun,warsh |
| 68790 | 55:54 | `وحٮى` hafs,shuba,bazzi,douri,sousi  ·  `وحٮا` qaloun,warsh | **وَجَنَى** hafs,shuba,bazzi,douri,sousi  ·  **وَجَنَا** qaloun,warsh |
| 73950 | 72:16 | `والو` hafs,shuba,bazzi  ·  `واں` qaloun,warsh,douri,sousi | **وَأَلَّوِ** hafs,shuba,bazzi  ·  **وَأَن** qaloun,warsh,douri,sousi |
| 76676 | 91:15 | `ولا` hafs,shuba,bazzi,douri,sousi  ·  `ڡلا` qaloun,warsh | **وَلَا** hafs,shuba,bazzi,douri,sousi  ·  **فَلَا** qaloun,warsh |

### The ā on the line or above it

198 kalimahs whose skeletons agree once every ā is spelled out, and differ only because one hand wrote that ā on the line and the other wrote it above: the Warsh/Qālūn set prints `هَارُوتَ` and `مُبَٰرَك` where the Kūfī set prints `هَٰرُوتَ` and `مُبَارَك`.

They are not counted as the mushafs disagreeing, and the reason is in the data rather than in a judgement about it. **All 198 split the seven riwayahs along exactly one line — `bazzi,douri,hafs,shuba,sousi` against `qaloun,warsh` — in both directions and without one exception.** The 62 real harf differences split them 14 different ways. Ḥadhf and ithbāt al-alif do vary between the mushafs of the amṣār, but they do not put Makkah with Madinah 198 times out of 198 and never once apart; a publisher's house style does. Bazzī goes its own way 7 times among the 62 and not once among these.

The distinction is still kept in `rasm`, because inside any one mushaf it is that mushaf's own ḥadhf, carried consistently: Ḥafṣ writes قال plene 412 times and defective 4, سبحان defective 12 and plene once, and 175 of these 198 kalimahs show the identical split at *every* occurrence of the kalimah in the corpus. What the sources cannot answer is which of the two hands is the mushaf's. A sample:

| kalimah id | surah:ayah | rasm on each side | as printed |
|---|---|---|---|
| 425 | 2:28 | `ڡاحٮكم` hafs,shuba,bazzi,douri,sousi  ·  `ڡاحٮاكم` qaloun,warsh | **فَأَحۡيَٰكُمۡ** hafs,shuba,douri,sousi  ·  **فَأَحۡيَٰكُمُۥ** bazzi  ·  **فَأَحْيَاكُمْ** qaloun  ·  **فَأَحْيٜاكُمْ** warsh |
| 618 | 2:40 | `اسرٮل` hafs,shuba,bazzi,douri,sousi  ·  `اسراٮل` qaloun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shuba,bazzi,douri,sousi  ·  **إِسْرَآءِيلَ** qaloun,warsh |
| 690 | 2:47 | `اسرٮل` hafs,shuba,bazzi,douri,sousi  ·  `اسراٮل` qaloun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shuba,bazzi,douri,sousi  ·  **إِسْرَآءِيلَ** qaloun,warsh |
| 823 | 2:57 | `العمام` hafs,shuba,bazzi,douri,sousi  ·  `العمم` qaloun,warsh | **ٱلۡغَمَامَ** hafs,shuba,bazzi  ·  **ࡲ۬لْغَمَٰمَ** qaloun,warsh  ·  **اُ۬لۡغَمَامَ** douri  ·  **ࡲ۬لۡغَمَامَ** sousi |
| 1333 | 2:83 | `اسرٮل` hafs,shuba,bazzi,douri,sousi  ·  `اسراٮل` qaloun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shuba,bazzi,douri  ·  **إِسْرَآءِيلَ** qaloun,warsh  ·  **إِسۡرَٰٓءِيل** sousi |
| 1339 | 2:83 | `احساٮا` hafs,shuba,bazzi,douri,sousi  ·  `احسٮا` qaloun,warsh | **إِحۡسَانࣰا** hafs,shuba,bazzi,sousi  ·  **إِحْسَٰناࣰ** qaloun,warsh  ·  **إِحۡسَانٗا** douri |
| 1738 | 2:102 | `هروٮ` hafs,shuba,bazzi,douri,sousi  ·  `هاروٮ` qaloun,warsh | **هَٰرُوتَ** hafs,shuba,bazzi,douri,sousi  ·  **هَارُوتَ** qaloun,warsh |
| 1739 | 2:102 | `ومروٮ` hafs,shuba,bazzi,douri,sousi  ·  `وماروٮ` qaloun,warsh | **وَمَٰرُوتَ** hafs,shuba,bazzi,douri,sousi  ·  **وَمَارُوتَ** qaloun,warsh |
| 1741 | 2:102 | `ٮعلماں` hafs,shuba,bazzi,douri,sousi  ·  `ٮعلمں` qaloun,warsh | **يُعَلِّمَانِ** hafs,shuba,bazzi,douri,sousi  ·  **يُعَلِّمَٰنِ** qaloun,warsh |
| 2147 | 2:121 | `ٮلاوٮه` hafs,shuba,bazzi,douri,sousi  ·  `ٮلوٮه` qaloun,warsh | **تِلَاوَتِهِۦٓ** hafs,shuba,douri  ·  **تِلَاوَتِهِۦ** bazzi,sousi  ·  **تِلَٰوَتِهِۦ** qaloun  ·  **تِلَٰوَتِهِۦٓ** warsh |
| 2158 | 2:122 | `اسرٮل` hafs,shuba,bazzi,douri,sousi  ·  `اسراٮل` qaloun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shuba,bazzi,douri,sousi  ·  **إِسْرَآءِيلَ** qaloun,warsh |
| 2824 | 2:158 | `سعاٮر` hafs,shuba,bazzi,douri,sousi  ·  `سعٮر` qaloun,warsh | **شَعَآئِرِ** hafs,shuba,bazzi,douri,sousi  ·  **شَعَٰٓئِرِ** qaloun,warsh |
| 2991 | 2:166 | `الاسٮاٮ` hafs,shuba,bazzi,douri,sousi  ·  `الاسٮٮ` qaloun,warsh | **ٱلۡأَسۡبَابُ** hafs,shuba,bazzi  ·  **ࡲ۬لْأَسْبَٰبُ** qaloun  ·  **ࡲ۬لَاسْبَٰبُ** warsh  ·  **اِ۬لۡأَسۡبَابُ** douri  ·  **ࡵ۬لۡأَسۡبَابُ** sousi |
| 3929 | 2:210 | `العمام` hafs,shuba,bazzi,douri,sousi  ·  `العمم` qaloun,warsh | **ٱلۡغَمَامِ** hafs,shuba,bazzi  ·  **ࡰ۬لْغَمَٰمِ** qaloun,warsh  ·  **اَ۬لۡغَمَامِ** douri  ·  **ࡱ۬لۡغَمَامِ** sousi |
| 3939 | 2:211 | `اسرٮل` hafs,shuba,bazzi,douri,sousi  ·  `اسراٮل` qaloun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shuba,bazzi,douri,sousi  ·  **إِسْرَآءِيلَ** qaloun,warsh |

### Pointing — one rasm, two qira'ahs

338 kalimahs share a rasm but are pointed differently. These are real differences in qira'ah, not in the mushaf: an undotted skeleton carries them all. A sample:

| kalimah id | surah:ayah | shared rasm | pointed as |
|---|---|---|---|
| 11 | 1:4 | `ملك` | **مالك** hafs,shuba  ·  **ملك** bazzi,qaloun,warsh,douri,sousi |
| 105 | 2:9 | `ٮحدعوں` | **يخدعون** hafs,shuba  ·  **يخادعون** bazzi,qaloun,warsh,douri,sousi |
| 709 | 2:48 | `ٮڡٮل` | **يقبل** hafs,shuba,qaloun,warsh  ·  **تقبل** bazzi,douri,sousi |
| 748 | 2:51 | `وعدٮا` | **واعدنا** hafs,shuba,bazzi,qaloun,warsh  ·  **وعدنا** douri,sousi |
| 854 | 2:58 | `ٮعڡر` | **نغفر** hafs,shuba,bazzi,douri,sousi  ·  **يغفر** qaloun,warsh |
| 1142 | 2:72 | `ڡادرٮم` | **فاداراتم** hafs,shuba,bazzi,qaloun,douri,sousi  ·  **فادارتم** warsh |
| 1196 | 2:74 | `ٮعملوں` | **تعملون** hafs,shuba,qaloun,warsh,douri,sousi  ·  **يعملون** bazzi |
| 1312 | 2:81 | `حطٮٮه` | **خطيته** hafs,shuba,bazzi,douri,sousi  ·  **خطياته** qaloun,warsh |
| 1335 | 2:83 | `ٮعٮدوں` | **تعبدون** hafs,shuba,qaloun,warsh,douri,sousi  ·  **يعبدون** bazzi |
| 1390 | 2:85 | `ٮڡدوهم` | **تفادوهم** hafs,shuba,qaloun,warsh  ·  **تفدوهم** bazzi,douri,sousi |
| 1421 | 2:85 | `ٮعملوں` | **تعملون** hafs,douri,sousi  ·  **يعملون** shuba,bazzi,qaloun,warsh |
| 1670 | 2:98 | `ومٮكٮل` | **وميكيال** hafs,douri,sousi  ·  **وميكايل** shuba,bazzi,qaloun,warsh |
| 2479 | 2:140 | `ٮڡولوں` | **تقولون** hafs  ·  **يقولون** shuba,bazzi,qaloun,warsh,douri,sousi |
| 2711 | 2:149 | `ٮعملوں` | **تعملون** hafs,shuba,bazzi,qaloun,warsh  ·  **يعملون** douri,sousi |
| 2966 | 2:165 | `ٮرى` | **يري** hafs,shuba,bazzi,douri,sousi  ·  **تري** qaloun,warsh |

### Boundaries — where the space falls

A boundary disagreement is never about one kalimah; it is about the space between two. Each event below shows the whole run, exactly as each riwayah prints it. The last column is the one that matters: **agree** means every riwayah reads the run identically once it is re-segmented, so the flag is a *source* that lost a space, not a mushaf that really prints the kalimahs joined.

**4:91** — kalimah ids 11634, 11635 · joined in `douri`, `qaloun` · **all riwayahs agree** (a dropped space in the source)

| riwayahs | as printed |
|---|---|
| `hafs,shuba,warsh,douri` | مَا رُدُّوٓاْ |
| `bazzi,qaloun,sousi` | مَا رُدُّواْ |

**10:26** — kalimah ids 26811, 26812 · joined in `douri` · **all riwayahs agree** (a dropped space in the source)

| riwayahs | as printed |
|---|---|
| `hafs,shuba,bazzi,qaloun,warsh,sousi` | قَتَرࣱ وَلَا |
| `douri` | قَتَرٞ وَلَا |

**11:78** — kalimah ids 29368, 29369 · joined in `douri` · **all riwayahs agree** (a dropped space in the source)

| riwayahs | as printed |
|---|---|
| `hafs,shuba,bazzi,douri,sousi` | كَانُواْ يَعۡمَلُونَ |
| `qaloun,warsh` | كَانُواْ يَعْمَلُونَ |

**27:20** — kalimah ids 48679, 48680 · joined in `bazzi`, `douri` · **all riwayahs agree** (a dropped space in the source)

| riwayahs | as printed |
|---|---|
| `hafs,shuba,bazzi` | مَا لِيَ |
| `qaloun,warsh` | مَا لِے |
| `douri,sousi` | مَا لِي |

**36:22** — kalimah ids 56845, 56846 · joined in `bazzi`, `douri` · **all riwayahs agree** (a dropped space in the source)

| riwayahs | as printed |
|---|---|
| `hafs,shuba,bazzi,qaloun,warsh,douri,sousi` | وَمَا لِيَ |

**75:1** — kalimah ids 74539, 74540 · joined in `bazzi` · **all riwayahs agree** (a dropped space in the source)

| riwayahs | as printed |
|---|---|
| `hafs,shuba,douri` | لَآ أُقۡسِمُ |
| `bazzi` | لَأُ اْقۡسِمُ |
| `qaloun` | لَا أُقْسِمُ |
| `warsh` | لَآ أُقْسِمُ |
| `sousi` | لَا أُقۡسِم |

Machine-readable: [`boundaries.csv`](boundaries.csv).

### Absence — kalimahs not every riwayah has

Each is well attested: Ibn Kathīr's `مِن` at 9:100, and Nāfiʿ reading `فإن الله الغني` at 57:24 where the others read `فإن الله هو الغني`. The rest are kalimahs one riwayah writes joined to its neighbour and another writes separately, so the count of kalimahs genuinely differs.

| kalimah id | surah:ayah | rasm | present in | absent from | as printed |
|---|---|---|---|---|---|
| 25685 | 9:101 | `مں` | bazzi | hafs, shuba, warsh, qaloun, douri, sousi | **مِن** bazzi |
| 60523 | 40:26 | `اں` | hafs, shuba | warsh, qaloun, douri, sousi, bazzi | **أَن** hafs,shuba |
| 69720 | 57:24 | `هو` | hafs, shuba, douri, sousi, bazzi | warsh, qaloun | **هُوَ** hafs,shuba,bazzi,douri  ·  **هُّوَ** sousi |
| 73951 | 72:16 | `لو` | warsh, qaloun, douri, sousi | hafs, shuba, bazzi | **لَّوِ** qaloun,warsh,douri,sousi |
| 74227 | 73:20 | `لں` | hafs, shuba, warsh, qaloun, bazzi | douri, sousi | **لَّن** hafs,shuba,bazzi,qaloun,warsh |

## Fasilahs: where the ayahs end

The ayah boundaries are a layer *over* the kalimah index, not a property of it, and **they belong to the printed mushaf rather than to the qira'ah**. Many fasilahs are مختلف فيها: al-Dānī records Al-Mulk 67:9 «قد جاءنا نذير» as counted by المدني الأخير والمكي and by Shayba and not by the rest, and four of the seven packages here count it. An edition has to choose, and editions of the same riwayah choose differently — KFGQPC's own Dūrī printings all state they follow المدني الأول and still total 6,218 (1429 AH), 6,217 (1436) and 6,214 (1443).

So the systems below are not counting traditions and are not derived from any. They are read off the packages, and two riwayahs are grouped only where their fasilahs are identical. Machine-readable: [`fasilahs.json`](fasilahs.json).

| system | mushaf | ayahs |
|---|---|---|
| `hafs+shuba` | hafs, shuba | 6,236 |
| `bazzi` | bazzi | 6,220 |
| `qaloun+warsh` | qaloun, warsh | 6,214 |
| `douri` | douri | 6,217 |
| `sousi` | sousi | 6,218 |

| system | `hafs+shuba` | `bazzi` | `qaloun+warsh` | `douri` | `sousi` |
|---|---|---|---|---|---|
| `hafs+shuba` | — | 150 | 140 | 133 | 134 |
| `bazzi` | 150 | — | 48 | 39 | 38 |
| `qaloun+warsh` | 140 | 48 | — | 57 | 56 |
| `douri` | 133 | 39 | 57 | — | 1 |
| `sousi` | 134 | 38 | 56 | 1 | — |

Positions where two systems put a fasilah differently. Dūrī and Sūsī are both conventionally labelled Baṣrī and part company at exactly one place — 67:9 — which is the whole of the 6,217/6,218 difference between them, and is a documented خلافي point rather than a mistake by either.

## Source integrity

Six riwayahs ship two releases. Comparing them is the sharpest available check on each, since the publisher is the same.

**Where the two releases disagree, the later one is the text.** KFGQPC revises these documents deliberately: the 2026 Ḥafṣ separates `مَا لِيَ` where Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`. That is a change of convention, not a defect, and the newer convention is the one published here. The earlier release is never merged into the text — it is only compared against it, below. The rule cannot discriminate for Dūrī, whose two packages are both from 2022; its three dropped spaces are recorded as boundary events instead.

| riwayah | ayahs compared | byte-identical | notation only | marks/vowels only | rasm differs |
|---|---|---|---|---|---|
| hafs | 6,236 | 2,715 | 700 | 2,819 | 2 |
| shuba | 6,236 | 2,715 | 697 | 2,822 | 2 |
| warsh | 6,214 | 160 | 410 | 5,635 | 9 |
| qaloun | 6,214 | 733 | 2,319 | 3,154 | 8 |
| douri | 6,217 | 6,214 | 0 | 0 | 3 |
| sousi | 6,217 | 508 | 1,916 | 3,768 | 25 |

`notation only` is dominated by the 2026 files adopting the Arabic Extended-B alif harfs (`U+0870`–`U+0882`), which fold an alef and its vowel into one codepoint where the 2022 files used an alef plus combining marks. The `folded` form decomposes them again, so none of it reaches the kalimah index.

### Checks

All checks pass.

## Per surah

| surah | name | kalimahs | identical | diacritic | dotting | ā | rasm | boundary/absent | per 1000 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Al-Fātiḥah | 29 | 11 | 17 | 1 | 0 | 0 | 0 | 0.0 |
| 2 | Al-Baqarah | 6,117 | 3181 | 2890 | 21 | 24 | 1 | 0 | 0.2 |
| 3 | Āl-‘Imrān | 3,481 | 1767 | 1685 | 18 | 9 | 2 | 0 | 0.6 |
| 4 | An-Nisā’ | 3,747 | 1842 | 1876 | 19 | 8 | 0 | 2 | 0.5 |
| 5 | Al-Mā’idah | 2,804 | 1362 | 1418 | 3 | 19 | 2 | 0 | 0.7 |
| 6 | Al-An‘ām | 3,050 | 1645 | 1382 | 16 | 5 | 2 | 0 | 0.7 |
| 7 | Al-A‘rāf | 3,320 | 1779 | 1518 | 13 | 7 | 3 | 0 | 0.9 |
| 8 | Al-Anfāl | 1,234 | 592 | 632 | 6 | 3 | 1 | 0 | 0.8 |
| 9 | At-Taubah | 2,499 | 1207 | 1279 | 10 | 0 | 2 | 1 | 1.2 |
| 10 | Yūnus | 1,833 | 1011 | 809 | 7 | 4 | 0 | 2 | 1.1 |
| 11 | Hūd | 1,917 | 1091 | 817 | 4 | 3 | 0 | 2 | 1.0 |
| 12 | Yūsuf | 1,777 | 965 | 791 | 16 | 4 | 1 | 0 | 0.6 |
| 13 | Ar-Ra‘d | 854 | 454 | 394 | 4 | 2 | 0 | 0 | 0.0 |
| 14 | Ibrāhīm | 830 | 429 | 399 | 1 | 1 | 0 | 0 | 0.0 |
| 15 | Al-Ḥijr | 654 | 400 | 251 | 3 | 0 | 0 | 0 | 0.0 |
| 16 | An-Naḥl | 1,844 | 958 | 877 | 8 | 1 | 0 | 0 | 0.0 |
| 17 | Al-Isrā’ | 1,556 | 818 | 722 | 9 | 6 | 1 | 0 | 0.6 |
| 18 | Al-Kahf | 1,579 | 809 | 760 | 3 | 5 | 2 | 0 | 1.3 |
| 19 | Maryam | 961 | 485 | 471 | 2 | 2 | 1 | 0 | 1.0 |
| 20 | Ṭā-Hā | 1,335 | 717 | 603 | 7 | 7 | 1 | 0 | 0.7 |
| 21 | Al-Anbiyā’ | 1,169 | 644 | 513 | 6 | 3 | 3 | 0 | 2.6 |
| 22 | Al-Ḥajj | 1,274 | 657 | 608 | 6 | 3 | 0 | 0 | 0.0 |
| 23 | Al-Mu’minūn | 1,050 | 580 | 460 | 4 | 3 | 3 | 0 | 2.9 |
| 24 | An-Nūr | 1,316 | 639 | 669 | 8 | 0 | 0 | 0 | 0.0 |
| 25 | Al-Furqān | 893 | 456 | 426 | 6 | 4 | 1 | 0 | 1.1 |
| 26 | Ash-Shu‘arā’ | 1,318 | 733 | 577 | 2 | 5 | 1 | 0 | 0.8 |
| 27 | An-Naml | 1,151 | 639 | 495 | 10 | 3 | 2 | 2 | 3.5 |
| 28 | Al-Qaṣaṣ | 1,430 | 809 | 606 | 4 | 9 | 2 | 0 | 1.4 |
| 29 | Al-‘Ankabūt | 976 | 497 | 471 | 5 | 3 | 0 | 0 | 0.0 |
| 30 | Ar-Rūm | 817 | 421 | 388 | 6 | 0 | 2 | 0 | 2.4 |
| 31 | Luqmān | 546 | 293 | 250 | 2 | 1 | 0 | 0 | 0.0 |
| 32 | As-Sajdah | 372 | 208 | 163 | 0 | 1 | 0 | 0 | 0.0 |
| 33 | Al-Aḥzāb | 1,287 | 616 | 659 | 11 | 0 | 1 | 0 | 0.8 |
| 34 | Saba’ | 883 | 490 | 383 | 8 | 2 | 0 | 0 | 0.0 |
| 35 | Fāṭir | 775 | 421 | 348 | 3 | 2 | 1 | 0 | 1.3 |
| 36 | Yā-Sīn | 725 | 362 | 356 | 4 | 0 | 1 | 2 | 4.1 |
| 37 | Aṣ-Ṣāffāt | 861 | 484 | 375 | 0 | 1 | 1 | 0 | 1.2 |
| 38 | Ṣād | 733 | 422 | 308 | 2 | 1 | 0 | 0 | 0.0 |
| 39 | Az-Zumar | 1,172 | 625 | 541 | 3 | 1 | 2 | 0 | 1.7 |
| 40 | Ghāfir | 1,219 | 632 | 574 | 4 | 7 | 1 | 1 | 1.6 |
| 41 | Fuṣṣilat | 794 | 414 | 377 | 2 | 1 | 0 | 0 | 0.0 |
| 42 | Ash-Shūra | 860 | 430 | 424 | 5 | 0 | 1 | 0 | 1.2 |
| 43 | Az-Zukhruf | 830 | 447 | 373 | 6 | 2 | 2 | 0 | 2.4 |
| 44 | Ad-Dukhān | 346 | 198 | 146 | 1 | 1 | 0 | 0 | 0.0 |
| 45 | Al-Jāthiyah | 488 | 266 | 220 | 1 | 1 | 0 | 0 | 0.0 |
| 46 | Al-Aḥqāf | 643 | 344 | 290 | 5 | 3 | 1 | 0 | 1.6 |
| 47 | Muḥammad | 539 | 241 | 293 | 5 | 0 | 0 | 0 | 0.0 |
| 48 | Al-Fatḥ | 560 | 267 | 285 | 8 | 0 | 0 | 0 | 0.0 |
| 49 | Al-Ḥujurāt | 347 | 165 | 179 | 2 | 1 | 0 | 0 | 0.0 |
| 50 | Qāf | 373 | 236 | 133 | 2 | 2 | 0 | 0 | 0.0 |
| 51 | Adh-Dhāriyāt | 360 | 187 | 173 | 0 | 0 | 0 | 0 | 0.0 |
| 52 | Aṭ-Ṭūr | 312 | 177 | 132 | 3 | 0 | 0 | 0 | 0.0 |
| 53 | An-Najm | 360 | 173 | 186 | 0 | 1 | 0 | 0 | 0.0 |
| 54 | Al-Qamar | 342 | 190 | 150 | 1 | 1 | 0 | 0 | 0.0 |
| 55 | Ar-Raḥmān | 351 | 240 | 96 | 0 | 13 | 2 | 0 | 5.7 |
| 56 | Al-Wāqi‘ah | 379 | 212 | 166 | 0 | 1 | 0 | 0 | 0.0 |
| 57 | Al-Ḥadīd | 574 | 273 | 298 | 2 | 0 | 0 | 1 | 1.7 |
| 58 | Al-Mujādilah | 472 | 243 | 225 | 3 | 0 | 1 | 0 | 2.1 |
| 59 | Al-Ḥashr | 445 | 203 | 239 | 1 | 1 | 1 | 0 | 2.2 |
| 60 | Al-Mumtaḥanah | 348 | 158 | 190 | 0 | 0 | 0 | 0 | 0.0 |
| 61 | Aṣ-Ṣaff | 221 | 110 | 107 | 0 | 2 | 2 | 0 | 9.0 |
| 62 | Al-Jumu‘ah | 175 | 79 | 96 | 0 | 0 | 0 | 0 | 0.0 |
| 63 | Al-Munāfiqūn | 180 | 87 | 92 | 1 | 0 | 0 | 0 | 0.0 |
| 64 | At-Taghābun | 241 | 116 | 122 | 3 | 0 | 0 | 0 | 0.0 |
| 65 | Aṭ-Ṭalāq | 287 | 153 | 131 | 1 | 0 | 2 | 0 | 7.0 |
| 66 | At-Taḥrīm | 249 | 126 | 119 | 1 | 3 | 0 | 0 | 0.0 |
| 67 | Al-Mulk | 333 | 160 | 173 | 0 | 0 | 0 | 0 | 0.0 |
| 68 | Al-Qalam | 300 | 190 | 108 | 0 | 2 | 0 | 0 | 0.0 |
| 69 | Al-Ḥāqqah | 258 | 153 | 103 | 2 | 0 | 0 | 0 | 0.0 |
| 70 | Al-Ma‘ārij | 217 | 109 | 106 | 2 | 0 | 0 | 0 | 0.0 |
| 71 | Nūḥ | 226 | 107 | 118 | 1 | 0 | 0 | 0 | 0.0 |
| 72 | Al-Jinn | 286 | 138 | 144 | 1 | 0 | 2 | 1 | 10.5 |
| 73 | Al-Muzzammil | 199 | 99 | 98 | 0 | 0 | 1 | 1 | 10.1 |
| 74 | Al-Muddaththir | 255 | 146 | 106 | 1 | 0 | 2 | 0 | 7.8 |
| 75 | Al-Qiyāmah | 164 | 87 | 72 | 3 | 0 | 0 | 2 | 12.2 |
| 76 | Al-Insān | 243 | 123 | 119 | 1 | 0 | 0 | 0 | 0.0 |
| 77 | Al-Mursalāt | 181 | 107 | 73 | 1 | 0 | 0 | 0 | 0.0 |
| 78 | An-Naba’ | 173 | 87 | 84 | 0 | 2 | 0 | 0 | 0.0 |
| 79 | An-Nāzi‘āt | 179 | 90 | 88 | 1 | 0 | 0 | 0 | 0.0 |
| 80 | ‘Abasa | 133 | 73 | 60 | 0 | 0 | 0 | 0 | 0.0 |
| 81 | At-Takwīr | 104 | 60 | 42 | 0 | 1 | 1 | 0 | 9.6 |
| 82 | Al-Infiṭār | 80 | 47 | 33 | 0 | 0 | 0 | 0 | 0.0 |
| 83 | Al-Muṭaffifīn | 169 | 94 | 74 | 1 | 0 | 0 | 0 | 0.0 |
| 84 | Al-Inshiqāq | 107 | 65 | 42 | 0 | 0 | 0 | 0 | 0.0 |
| 85 | Al-Burūj | 109 | 53 | 56 | 0 | 0 | 0 | 0 | 0.0 |
| 86 | Aṭ-Ṭāriq | 61 | 35 | 26 | 0 | 0 | 0 | 0 | 0.0 |
| 87 | Al-A‘lā | 72 | 36 | 35 | 1 | 0 | 0 | 0 | 0.0 |
| 88 | Al-Ghāshiyah | 92 | 54 | 37 | 1 | 0 | 0 | 0 | 0.0 |
| 89 | Al-Fajr | 137 | 69 | 63 | 4 | 0 | 1 | 0 | 7.3 |
| 90 | Al-Balad | 82 | 48 | 33 | 0 | 0 | 1 | 0 | 12.2 |
| 91 | Ash-Shams | 54 | 20 | 32 | 0 | 1 | 1 | 0 | 18.5 |
| 92 | Al-Lail | 71 | 33 | 38 | 0 | 0 | 0 | 0 | 0.0 |
| 93 | Aḍ-Ḍuḥā | 40 | 23 | 17 | 0 | 0 | 0 | 0 | 0.0 |
| 94 | Ash-Sharḥ | 27 | 21 | 6 | 0 | 0 | 0 | 0 | 0.0 |
| 95 | At-Tīn | 34 | 22 | 12 | 0 | 0 | 0 | 0 | 0.0 |
| 96 | Al-‘Alaq | 72 | 41 | 31 | 0 | 0 | 0 | 0 | 0.0 |
| 97 | Al-Qadr | 30 | 14 | 16 | 0 | 0 | 0 | 0 | 0.0 |
| 98 | Al-Bayyinah | 94 | 50 | 44 | 0 | 0 | 0 | 0 | 0.0 |
| 99 | Az-Zalzalah | 36 | 22 | 14 | 0 | 0 | 0 | 0 | 0.0 |
| 100 | Al-‘Ādiyāt | 40 | 23 | 17 | 0 | 0 | 0 | 0 | 0.0 |
| 101 | Al-Qāri‘ah | 36 | 19 | 17 | 0 | 0 | 0 | 0 | 0.0 |
| 102 | At-Takāthur | 28 | 21 | 7 | 0 | 0 | 0 | 0 | 0.0 |
| 103 | Al-‘Aṣr | 14 | 10 | 4 | 0 | 0 | 0 | 0 | 0.0 |
| 104 | Al-Humazah | 33 | 14 | 19 | 0 | 0 | 0 | 0 | 0.0 |
| 105 | Al-Fīl | 23 | 14 | 9 | 0 | 0 | 0 | 0 | 0.0 |
| 106 | Quraish | 17 | 5 | 11 | 0 | 0 | 1 | 0 | 58.8 |
| 107 | Al-Mā‘ūn | 25 | 11 | 14 | 0 | 0 | 0 | 0 | 0.0 |
| 108 | Al-Kauthar | 10 | 6 | 4 | 0 | 0 | 0 | 0 | 0.0 |
| 109 | Al-Kāfirūn | 26 | 10 | 16 | 0 | 0 | 0 | 0 | 0.0 |
| 110 | An-Naṣr | 19 | 12 | 7 | 0 | 0 | 0 | 0 | 0.0 |
| 111 | Al-Masad | 23 | 12 | 11 | 0 | 0 | 0 | 0 | 0.0 |
| 112 | Al-Ikhlāṣ | 15 | 10 | 5 | 0 | 0 | 0 | 0 | 0.0 |
| 113 | Al-Falaq | 23 | 19 | 4 | 0 | 0 | 0 | 0 | 0.0 |
| 114 | An-Nās | 20 | 10 | 10 | 0 | 0 | 0 | 0 | 0.0 |
