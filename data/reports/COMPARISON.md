# Cross-riwāyah comparison

Generated 2026-09-08 from the KFGQPC packages in `sources/`. 77,434 canonical words across 114 sūrahs and 7 riwāyāt.

Every word carries one ID that means the same word in every riwāyah that has it. Where the riwāyāt disagree, the disagreement is recorded against that ID rather than hidden by it.

## What is being compared

A word is never compared as raw text. Four forms are derived from every spelling, each stripping one more layer of what a scribe added after the codices were written. Two riwāyāt are said to agree *at a level* when their forms at that level are identical.

| form | question it answers | example | and what it drops |
|---|---|---|---|
| `rasm_uthmani` | how is it printed? | `ٱلرَّحۡمَٰنِ` | — |
| `folded` | what does it say, ignoring which codepoints the release chose? | `الرَّحْمَٰنِ` | release notation, attached-alef letters, editorial marks |
| `pointed` | which letters, dots and all? | `الرحمان` | vowels, hamzah, madd, ṣilah |
| `rasm` | what is on the line in the codex? | `الرحماں` | the dots |

The two skeletons are separate on purpose. `تَعۡمَلُونَ` and `يَعۡمَلُونَ` have different `pointed` forms but one `rasm` — `ٮعملوں` — because the codices were written undotted and carry both qiraahs by design. Calling that a rasm variant would be a category error; calling it vowelling would hide a real qiraah. It is named **`dotting_variant`**.

`rasm` drops hamzah and every hamzah carrier reduces to its seat, because hamzah is post-ʿUthmānic notation: `يَسۡتَهۡزِئُ` and `يَسْتَهْزِۓُ` are one word. It also drops the dagger alif, which is by definition an alef the scribe did *not* write on the line, so `هَٰرُوتَ` and `هَارُوتَ` do **not** share a rasm: `هروٮ` against `هاروٮ`. That difference is real inside any one muṣḥaf and is kept, but between these two typesettings it is a house style rather than a codex — see [the ā on the line or above it](#the-ā-on-the-line-or-above-it).

## The riwāyāt

| key | riwāyah | الرواية | qāriʾ | counting system | āyāt | words |
|---|---|---|---|---|---|---|
| hafs | Ḥafṣ | حفص | ʿĀṣim al-Kūfī | `kufi` | 6,236 | 77,432 |
| shubah | Shuʿbah | شعبة | ʿĀṣim al-Kūfī | `kufi` | 6,236 | 77,432 |
| warsh | Warsh | ورش | Nāfiʿ al-Madanī | `madani-last` | 6,214 | 77,431 |
| qalun | Qālūn | قالون | Nāfiʿ al-Madanī | `madani-last` | 6,214 | 77,431 |
| duri | Dūrī | الدوري | Abū ʿAmr al-Baṣrī | `madani-first` | 6,217 | 77,431 |
| susi | Sūsī | السوسي | Abū ʿAmr al-Baṣrī | `madani-first` | 6,218 | 77,431 |
| bazzi | Bazzī | البزي | Ibn Kathīr al-Makkī | `makki` | 6,220 | 77,432 |

The āyah totals are not errors and not deducible from the qāriʾ. Many fawāṣil are مختلف فيها, so every printed edition chooses, and the counting system above is **derived** from what this package prints, not assumed from the riwāyah. That is exactly why the index is flat, and why the āyah boundaries are read off each muṣḥaf: see [the fawāṣil](#fawāṣil-where-the-āyāt-end) below.

## How the words compare

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.38% | one qiraah, one spelling, in all seven |
| `diacritic_variant` | 36,261 | 46.83% | same letters and same dots — the vowelling differs |
| `dotting_variant` | 338 | 0.44% | one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ |
| `alif_variant` | 198 | 0.26% | one skeleton, one ā: on the line in one hand, above it in the other |
| `rasm_variant` | 60 | 0.08% | the codices disagree about the letters on the line |
| `word_boundary` | 16 | 0.02% | a source prints the word joined to its neighbour |
| `partial` | 3 | 0.00% | the word is absent from at least one riwāyah |

Each word gets the *strongest* label that applies, tested in this order: rasm, ā, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed to share one rasm across all seven, an `alif_variant` to share one skeleton once every ā is spelled out, and an `identical` word is identical after notation folding — the raw spelling of every riwāyah is always kept in `forms`, whatever the label.

## Pairwise agreement

Share of the words two riwāyāt both have, where they agree at each level.

| pair | shared words | same spelling | same qiraah | same letters | same rasm |
|---|---|---|---|---|---|
| duri–susi | 77,432 | 66.7% | 82.8% | 99.97% | 100.00% |
| warsh–qalun | 77,431 | 85.2% | 87.5% | 99.95% | 99.99% |
| hafs–shubah | 77,433 | 99.2% | 99.2% | 99.86% | 99.99% |
| shubah–duri | 77,432 | 70.9% | 74.1% | 99.75% | 99.98% |
| shubah–susi | 77,432 | 72.1% | 72.9% | 99.72% | 99.97% |
| shubah–bazzi | 77,432 | 84.1% | 84.1% | 99.75% | 99.97% |
| hafs–bazzi | 77,432 | 84.0% | 84.0% | 99.73% | 99.97% |
| hafs–duri | 77,432 | 70.8% | 74.1% | 99.73% | 99.97% |
| duri–bazzi | 77,432 | 57.8% | 61.0% | 99.83% | 99.97% |
| hafs–susi | 77,432 | 72.0% | 72.8% | 99.70% | 99.97% |
| susi–bazzi | 77,432 | 66.6% | 67.4% | 99.80% | 99.97% |
| hafs–warsh | 77,431 | 41.3% | 75.2% | 99.72% | 99.70% |
| shubah–warsh | 77,431 | 41.4% | 75.2% | 99.73% | 99.70% |
| warsh–bazzi | 77,431 | 37.2% | 63.4% | 99.72% | 99.70% |
| warsh–duri | 77,431 | 37.8% | 76.3% | 99.72% | 99.69% |
| warsh–susi | 77,431 | 39.2% | 77.7% | 99.74% | 99.69% |
| hafs–qalun | 77,431 | 40.4% | 76.6% | 99.76% | 99.69% |
| shubah–qalun | 77,431 | 40.5% | 76.6% | 99.77% | 99.69% |
| qalun–bazzi | 77,431 | 41.5% | 70.8% | 99.76% | 99.69% |
| qalun–duri | 77,431 | 36.8% | 78.5% | 99.75% | 99.69% |
| qalun–susi | 77,431 | 42.6% | 84.4% | 99.72% | 99.69% |

Rasm agreement never drops below 99.5%: the seven riwāyāt are one text. Spelling agreement is far lower because the packages were typeset in different years with different conventions — which is what the `folded` and `pointed` columns strip away.

## Where the riwāyāt genuinely disagree

Three things can differ once spelling, vowelling and pointing are set aside: the letters, the word boundaries, and whether a word is there at all. Together they account for 75 of 77,434 words. A fourth kind is listed with them and counted apart: 198 words where the disagreement is only about whether an ā sits on the line or above it.

| kind | count | status | what it means |
|---|---|---|---|
| letters differ | 60 | `rasm_variant` | a letter one codex has on the line and another does not — 56 of them one letter more, 4 one letter for another |
| the ā is placed differently | 198 | `alif_variant` | one skeleton once every ā is spelled out; the two hands disagree about which ā to write on the line |
| boundaries differ | 6 events | `word_boundary` | one source prints two words as one |
| word absent | 3 | `partial` | a riwāyah does not have the word at all |

### Letters — rasm disagreements

60 words where the riwāyāt disagree about the letters on the line, after dots, hamzah, vowelling and the ā have all been set aside. These are the differences the sources can be trusted on: they split the seven riwāyāt 13 different ways — by miṣr, not by publisher — and they are the khilāf the rasm literature names. All 60 are listed below, grouped by what the difference *is*. Machine-readable: [`rasm-variants.md`](rasm-variants.md), [`differences.csv`](../differences.csv).

#### One skeleton, one letter more

56 of the 60. Both sides write the same letters in the same order and one side writes a letter the other does not: `ٮرٮد`/`ٮرٮدد` — يَرۡتَدَّ against يَرۡتَدِدۡ at 5:54 — or `ٮسٮهى`/`ٮسٮهٮه`, تَشۡتَهِي against تَشۡتَهِيهِ at 43:71. Nothing is replaced; the skeletons nest.

| word id | sūrah:āyah | rasm on each side | as printed |
|---|---|---|---|
| 2331 | 2:132 | `ووصى` hafs,shubah,bazzi,duri,susi  ·  `واوصى` qalun,warsh | **وَوَصَّىٰ** hafs,shubah,bazzi,duri,susi  ·  **وَأَوْصَىٰ** qalun  ·  **وَأَوْصٜىٰ** warsh |
| 8353 | 3:133 | `وسارعوا` hafs,shubah,bazzi,duri,susi  ·  `سارعوا` qalun,warsh | **وَسَارِعُوٓاْ** hafs,shubah,duri  ·  **وَسَارِعُواْ** bazzi,susi  ·  **سَارِعُواْ** qalun  ·  **سَارِعُوٓاْ** warsh |
| 8851 | 3:158 | `لالى` hafs,shubah,bazzi,qalun,warsh  ·  `لاالى` duri,susi | **لَإِلَى** hafs,shubah,bazzi,qalun,warsh  ·  **لَإِاْلَى** duri,susi |
| 14726 | 5:53 | `وٮڡول` hafs,shubah,duri,susi  ·  `ٮڡول` bazzi,qalun,warsh | **وَيَقُولُ** hafs,shubah  ·  **يَقُولُ** bazzi,qalun,warsh  ·  **وَيَقُولَ** duri,susi |
| 14745 | 5:54 | `ٮرٮد` hafs,shubah,bazzi,duri,susi  ·  `ٮرٮدد` qalun,warsh | **يَرۡتَدَّ** hafs,shubah,bazzi,duri,susi  ·  **يَّرْتَدِدْ** qalun,warsh |
| 17215 | 6:63 | `اٮحٮٮا` hafs,shubah  ·  `اٮحٮٮٮا` bazzi,qalun,warsh,duri,susi | **أَنجَىٰنَا** hafs,shubah  ·  **أَنجَيۡتَنَا** bazzi,duri,susi  ·  **أَنجَيْتَنَا** qalun  ·  **ࡰنجَيْتَنَا** warsh |
| 18334 | 6:124 | `رسالٮه` hafs,bazzi  ·  `رسلٮه` shubah,qalun,warsh,duri,susi | **رِسَالَتَهُۥ** hafs,bazzi  ·  **رِسَٰلَٰتِهِۦ** shubah,qalun,warsh,duri  ·  **رِّسَٰلَٰتِهِۦ** susi |
| 19696 | 7:34 | `ٮسٮاحروں` hafs,shubah,bazzi,duri,susi  ·  `ٮسٮحروں` qalun,warsh | **يَسۡتَأۡخِرُونَ** hafs,shubah,bazzi,duri  ·  **يَسْتَْٔخِرُونَ** qalun  ·  **يَسْتَٰخِرُونَ** warsh  ·  **يَسۡتَاخِرُونَ** susi |
| 21416 | 7:144 | `ٮرسلٮى` hafs,shubah,duri,susi  ·  `ٮرسالٮى` bazzi,qalun,warsh | **بِرِسَٰلَٰتِي** hafs,shubah,duri,susi  ·  **بِرِسَالَتِي** bazzi  ·  **بِرِسَالَتِے** qalun,warsh |
| 23200 | 8:42 | `حى` hafs,duri,susi  ·  `حٮى` shubah,bazzi,qalun,warsh | **حَيَّ** hafs,duri,susi  ·  **حَِۧيَ** shubah,bazzi  ·  **حَۑِيَ** qalun  ·  **حَيِيَ** warsh |
| 24700 | 9:47 | `ولاوصعوا` hafs,shubah,bazzi,qalun,warsh  ·  `ولااوصعوا` duri,susi | **وَلَأَوۡضَعُواْ** hafs,shubah,bazzi  ·  **وَلَأَوْضَعُواْ** qalun,warsh  ·  **وَلَأَاْوۡضَعُواْ** duri,susi |
| 25793 | 9:107 | `والدٮں` hafs,shubah,bazzi,duri,susi  ·  `الدٮں` qalun,warsh | **وَٱلَّذِينَ** hafs,shubah,bazzi  ·  **ࡴ۬لذِينَ** qalun,warsh  ·  **وَاَلَّذِينَ** duri  ·  **وَࡱلَّذِينَ** susi |
| 31777 | 12:110 | `ڡٮحى` hafs,shubah,bazzi,duri,susi  ·  `ڡٮٮحى` qalun,warsh | **فَنُجِّيَ** hafs,shubah  ·  **فَنُۨجِي** bazzi,duri,susi  ·  **فَنُنجِے** qalun,warsh |
| 37273 | 17:93 | `ڡل` hafs,shubah,qalun,warsh,duri,susi  ·  `ڡال` bazzi | **قُلۡ** hafs,shubah,duri,susi  ·  **قَالَ** bazzi  ·  **قُلْ** qalun,warsh |
| 38135 | 18:36 | `مٮها` hafs,shubah,duri,susi  ·  `مٮهما` bazzi,qalun,warsh | **مِّنۡهَا** hafs,shubah,duri,susi  ·  **مِّنۡهُمَا** bazzi  ·  **مِّنْهُمَا** qalun,warsh |
| 38936 | 18:95 | `مكٮى` hafs,shubah,qalun,warsh,duri,susi  ·  `مكٮٮى` bazzi | **مَكَّنِّي** hafs,shubah,duri,susi  ·  **مَكَّنَنِي** bazzi  ·  **مَكَّنِّے** qalun,warsh |
| 39298 | 19:19 | `لاهٮ` hafs,shubah,bazzi,qalun,warsh,duri  ·  `لاٮهٮ` susi | **لِأَهَبَ** hafs,shubah,bazzi,qalun  ·  **لِاَهَبَ** warsh  ·  **لِاَ۬هَبَ** duri  ·  **لِاَۧهَبَ** susi |
| 41131 | 20:112 | `ٮحاڡ` hafs,shubah,qalun,warsh,duri,susi  ·  `ٮحڡ` bazzi | **يَخَافُ** hafs,shubah,qalun,warsh,duri,susi  ·  **يَخَفۡ** bazzi |
| 41455 | 21:4 | `ڡال` hafs  ·  `ڡل` shubah,bazzi,qalun,warsh,duri,susi | **قَالَ** hafs  ·  **قُل** shubah,bazzi,qalun,warsh,duri,susi |
| 41720 | 21:30 | `اولم` hafs,shubah,qalun,warsh,duri,susi  ·  `الم` bazzi | **أَوَلَمۡ** hafs,shubah,duri,susi  ·  **أَلَمۡ** bazzi  ·  **أَوَلَمْ** qalun,warsh |
| 42341 | 21:88 | `ٮحى` hafs,shubah,bazzi,duri,susi  ·  `ٮٮحى` qalun,warsh | **نُۨجِي** hafs,bazzi,duri,susi  ·  **نُجِّي** shubah  ·  **نُنجِے** qalun,warsh |
| 44635 | 23:87 | `لله` hafs,shubah,bazzi,qalun,warsh  ·  `الله` duri,susi | **لِلَّهِ** hafs,shubah,bazzi  ·  **لِلهِ** qalun,warsh  ·  **اَ۬للَّهُ** duri  ·  **ࡱ۬للَّهُ** susi |
| 44654 | 23:89 | `لله` hafs,shubah,bazzi,qalun,warsh  ·  `الله` duri,susi | **لِلَّهِ** hafs,shubah,bazzi  ·  **لِلهِ** qalun,warsh  ·  **اَ۬للَّهُ** duri  ·  **ࡱ۬للَّهُ** susi |
| 44847 | 23:112 | `ڡل` hafs,shubah,bazzi,duri,susi  ·  `ڡال` qalun,warsh | **قَٰلَ** hafs,shubah,duri,susi  ·  **قُلۡ** bazzi  ·  **قَالَ** qalun,warsh |
| 46555 | 25:25 | `وٮرل` hafs,shubah,qalun,warsh,duri,susi  ·  `وٮٮرل` bazzi | **وَنُزِّلَ** hafs,shubah,qalun,warsh,duri,susi  ·  **وَنُنزِلُ** bazzi |
| 48694 | 27:21 | `لٮاٮٮٮى` hafs,shubah,qalun,warsh,duri,susi  ·  `لٮاٮٮٮٮى` bazzi | **لَيَأۡتِيَنِّي** hafs,shubah,duri  ·  **لَيَأۡتِيَنَّنِي** bazzi  ·  **لَيَأْتِيَنِّے** qalun  ·  **لَيَاتِيَنِّے** warsh  ·  **لَيَاتِيَنِّي** susi |
| 48852 | 27:36 | `اٮٮں` hafs,shubah,bazzi,duri,susi  ·  `اٮٮٮى` qalun,warsh | **ءَاتَىٰنِۦَ** hafs,duri,susi  ·  **ءَاتَىٰنِ** shubah,bazzi  ·  **ءَاتَيٰنِࣉَ** qalun  ·  **ءَاتٜيٰنِࣉَ** warsh |
| 50187 | 28:37 | `وڡال` hafs,shubah,qalun,warsh,duri,susi  ·  `ڡال` bazzi | **وَقَالَ** hafs,shubah,qalun,warsh,duri,susi  ·  **قَالَ** bazzi |
| 50378 | 28:48 | `سحراں` hafs,shubah,bazzi,duri,susi  ·  `سحرں` qalun,warsh | **سِحۡرَانِ** hafs,shubah  ·  **سَٰحِرَانِ** bazzi,duri,susi  ·  **سَٰحِرَٰنِ** qalun,warsh |
| 52070 | 30:8 | `ٮلڡاى` hafs,shubah,bazzi,duri,susi  ·  `ٮلڡا` qalun,warsh | **بِلِقَآيِٕ** hafs,shubah,bazzi,duri,susi  ·  **بِلِقَآءِ** qalun,warsh |
| 52159 | 30:16 | `ولڡاى` hafs,shubah,bazzi,duri,susi  ·  `ولڡا` qalun,warsh | **وَلِقَآيِٕ** hafs,shubah,bazzi,duri,susi  ·  **وَلِقَآءِ** qalun,warsh |
| 53776 | 33:4 | `الى` hafs,shubah,bazzi,warsh,duri,susi  ·  `الٮى` qalun | **ٱلَِّٰٓٔي** hafs,shubah  ·  **ٱلَّٰٓيۡ** bazzi  ·  **ࡲ۬لَّٰٓئِے** qalun  ·  **ࡲ۬لٜےْ** warsh  ·  **اُ۬لَّٰٓيۡ** duri  ·  **ࡲ۬لَّٰٓيۡ** susi |
| 56602 | 35:43 | `السٮى` hafs,shubah,bazzi,warsh,duri,susi  ·  `السٮٮى` qalun | **ٱلسَّيِّيِٕ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّيِّئِے** qalun  ·  **ࡰ۬لسَّيِّےِٕ** warsh  ·  **اَ۬لسَّيِّيِٕ** duri  ·  **ࡱ۬لسَّيِّيِٕ** susi |
| 56964 | 36:35 | `عملٮه` hafs,bazzi,qalun,warsh,duri,susi  ·  `عملٮ` shubah | **عَمِلَتۡهُ** hafs,duri,susi  ·  **عَمِلَتۡ** shubah  ·  **عَمِلَتۡهُۥ** bazzi  ·  **عَمِلَتْهُ** qalun,warsh |
| 57749 | 37:68 | `لالى` hafs,shubah,bazzi,qalun,warsh  ·  `لاالى` duri,susi | **لَإِلَى** hafs,shubah,bazzi,qalun,warsh  ·  **لَإِاْلَى** duri,susi |
| 59548 | 39:34 | `حرا` hafs,shubah,bazzi,duri,susi  ·  `حروا` qalun,warsh | **جَزَآءُ** hafs,shubah,bazzi,duri,susi  ·  **جَزَٰٓؤُاْ** qalun,warsh |
| 60056 | 39:69 | `وحاى` hafs,shubah,bazzi,duri,susi  ·  `وحى` qalun,warsh | **وَجِاْيٓءَ** hafs,shubah,bazzi,duri,susi  ·  **وَجِےٓءَ** qalun,warsh |
| 60523 | 40:26 | `اں` hafs,shubah  ·  `واں` bazzi,qalun,warsh,duri,susi | **أَن** hafs,shubah  ·  **وَأَن** bazzi,duri,susi  ·  **وَأَنْ** qalun,warsh |
| 62695 | 42:30 | `ڡٮما` hafs,shubah,bazzi,duri,susi  ·  `ٮما` qalun,warsh | **فَبِمَا** hafs,shubah,bazzi,duri,susi  ·  **بِمَا** qalun,warsh |
| 63696 | 43:68 | `ٮعٮاد` hafs,bazzi  ·  `ٮعٮادى` shubah,qalun,warsh,duri,susi | **يَٰعِبَادِ** hafs,bazzi  ·  **يَٰعِبَادِيَ** shubah  ·  **يَٰعِبَادِے** qalun,warsh  ·  **يَٰعِبَادِي** duri,susi |
| 63722 | 43:71 | `ٮسٮهٮه` hafs,qalun,warsh  ·  `ٮسٮهى` shubah,bazzi,duri,susi | **تَشۡتَهِيهِ** hafs  ·  **تَشۡتَهِي** shubah,bazzi,duri,susi  ·  **تَشْتَهِيهِ** qalun,warsh |
| 64932 | 46:15 | `احسٮا` hafs,shubah  ·  `حسٮا` bazzi,qalun,warsh,duri,susi | **إِحۡسَٰنًا** hafs,shubah  ·  **حُسۡنًا** bazzi,duri,susi  ·  **حُسْناً** qalun,warsh |
| 68622 | 55:22 | `اللولو` hafs,shubah,bazzi,duri,susi  ·  `اللولوا` qalun,warsh | **ٱللُّؤۡلُؤُ** hafs,bazzi  ·  **ٱللُّولُؤُ** shubah  ·  **ࡰ۬للُّؤْلُؤُاْ** qalun,warsh  ·  **اَ۬للُّؤۡلُؤُ** duri  ·  **ࡱ۬للُّولُؤُ** susi |
| 69876 | 58:2 | `الى` hafs,shubah,bazzi,warsh,duri,susi  ·  `الٮى` qalun | **ٱلَِّٰٓٔي** hafs,shubah  ·  **ٱلَّٰٓيۡ** bazzi  ·  **ࡰ۬لَّٰٓئِے** qalun  ·  **ࡰ۬لٜےْ** warsh  ·  **اَ۬لَّٰٓيۡ** duri  ·  **ࡱ۬لَّٰٓيۡ** susi |
| 70587 | 59:13 | `لاٮٮم` hafs,shubah,bazzi,qalun,warsh  ·  `لااٮٮم` duri,susi | **لَأَنتُمۡ** hafs,shubah  ·  **لَأَنتُمُۥ** bazzi  ·  **لَأَنتُمْ** qalun  ·  **لَأَنتُمُۥٓ** warsh  ·  **لَأَاْنتُمۡ** duri,susi |
| 71302 | 61:14 | `اٮصار` hafs,shubah  ·  `اٮصارا` bazzi,qalun,warsh,duri,susi | **أَنصَارَ** hafs,shubah  ·  **أَنصَارࣰا** bazzi,susi  ·  **أَنصَاراࣰ** qalun,warsh  ·  **أَنصَارٗا** duri |
| 71303 | 61:14 | `الله` hafs,shubah  ·  `لله` bazzi,qalun,warsh,duri,susi | **ٱللَّهِ** hafs,shubah  ·  **لِّلَّهِ** bazzi,duri,susi  ·  **لِّلهِ** qalun,warsh |
| 72021 | 65:4 | `والى` hafs,shubah,bazzi,warsh,duri,susi  ·  `والٮى` qalun | **وَٱلَِّٰٓٔي** hafs,shubah  ·  **وَٱلَّٰٓيۡ** bazzi  ·  **وَالَّٰٓئِے** qalun  ·  **وَالٜےْ** warsh  ·  **وَاَلَّٰٓيۡ** duri  ·  **وَࡱلَّٰٓيۡ** susi |
| 72032 | 65:4 | `والى` hafs,shubah,bazzi,warsh,duri,susi  ·  `والٮى` qalun | **وَٱلَِّٰٓٔي** hafs,shubah  ·  **وَٱلَّٰٓيۡ** bazzi  ·  **وَالَّٰٓئِے** qalun  ·  **وَالٜےْ** warsh  ·  **وَاَلَّٰٓيۡ** duri  ·  **وَࡱلَّٰٓيۡ** susi |
| 73986 | 72:20 | `ڡل` hafs,shubah  ·  `ڡال` bazzi,qalun,warsh,duri,susi | **قُلۡ** hafs,shubah  ·  **قَالَ** bazzi,qalun,warsh,duri,susi |
| 74439 | 74:33 | `اد` hafs,qalun,warsh  ·  `ادا` shubah,bazzi,duri,susi | **إِذۡ** hafs  ·  **إِذَا** shubah,bazzi,duri,susi  ·  **إِذْ** qalun  ·  **إِذَ** warsh |
| 74440 | 74:33 | `ادٮر` hafs,qalun,warsh  ·  `دٮر` shubah,bazzi,duri,susi | **أَدۡبَرَ** hafs  ·  **دَبَرَ** shubah,bazzi,duri,susi  ·  **أَدْبَرَ** qalun  ·  **ࡰدْبَرَ** warsh |
| 75690 | 81:24 | `ٮصٮٮں` hafs,shubah,qalun,warsh  ·  `ٮصطٮٮں` bazzi,duri,susi | **بِضَنِينࣲ** hafs,shubah,qalun,warsh  ·  **بِضظَنِينࣲ** bazzi  ·  **بِضظَنِينٖ** duri  ·  **بِّضظَنِينࣲ** susi |
| 76508 | 89:23 | `وحاى` hafs,shubah,bazzi,duri,susi  ·  `وحى` qalun,warsh | **وَجِاْيٓءَ** hafs,shubah,bazzi,duri,susi  ·  **وَجِےٓءَ** qalun,warsh |
| 76592 | 90:14 | `اطعم` hafs,shubah,bazzi,duri,susi  ·  `اطعام` qalun,warsh | **إِطۡعَٰمࣱ** hafs,shubah  ·  **أَطۡعَمَ** bazzi,duri,susi  ·  **إِطْعَامࣱ** qalun  ·  **ࡴطْعَامࣱ** warsh |
| 77259 | 106:2 | `الڡهم` hafs,shubah,bazzi,duri,susi  ·  `اٮلڡهم` qalun,warsh | **إِۦلَٰفِهِمۡ** hafs,shubah,duri,susi  ·  **إِۦلَٰفِهِمُۥ** bazzi  ·  **إِيلَٰفِهِمْ** qalun  ·  **ࡴيلَٰفِهِمْ** warsh |

#### One letter for another

4 of the 60, where a letter is not added but exchanged — `ولا`/`ڡلا` (وَلَا against فَلَا, 91:15), `كلمٮ`/`كلمه` (the open against the tied tāʾ, 7:137).

| word id | sūrah:āyah | rasm on each side | as printed |
|---|---|---|---|
| 21269 | 7:137 | `كلمٮ` hafs,shubah,bazzi,duri,susi  ·  `كلمه` qalun,warsh | **كَلِمَتُ** hafs,shubah,bazzi,duri,susi  ·  **كَلِمَةُ** qalun,warsh |
| 48378 | 26:217 | `وٮوكل` hafs,shubah,bazzi,duri,susi  ·  `ڡٮوكل` qalun,warsh | **وَتَوَكَّلۡ** hafs,shubah,bazzi,duri,susi  ·  **فَتَوَكَّلْ** qalun,warsh |
| 68790 | 55:54 | `وحٮى` hafs,shubah,bazzi,duri,susi  ·  `وحٮا` qalun,warsh | **وَجَنَى** hafs,shubah,bazzi,duri,susi  ·  **وَجَنَا** qalun,warsh |
| 76676 | 91:15 | `ولا` hafs,shubah,bazzi,duri,susi  ·  `ڡلا` qalun,warsh | **وَلَا** hafs,shubah,bazzi,duri,susi  ·  **فَلَا** qalun,warsh |

### The ā on the line or above it

198 words whose skeletons agree once every ā is spelled out, and differ only because one hand wrote that ā on the line and the other wrote it above: the Warsh/Qālūn set prints `هَارُوتَ` and `مُبَٰرَك` where the Kūfī set prints `هَٰرُوتَ` and `مُبَارَك`.

They are not counted as the codices disagreeing, and the reason is in the data rather than in a judgement about it. **All 198 split the seven riwāyāt along exactly one line — `bazzi,duri,hafs,shubah,susi` against `qalun,warsh` — in both directions and without one exception.** The 60 real letter differences split them 13 different ways. Ḥadhf and ithbāt al-alif do vary between the codices of the amṣār, but they do not put Makkah with Madinah 198 times out of 198 and never once apart; a publisher's house style does. Bazzī goes its own way 7 times among the 60 and not once among these.

The distinction is still kept in `rasm`, because inside any one muṣḥaf it is that muṣḥaf's own ḥadhf, carried consistently: Ḥafṣ writes قال plene 412 times and defective 4, سبحان defective 12 and plene once, and 175 of these 198 words show the identical split at *every* occurrence of the word in the corpus. What the sources cannot answer is which of the two hands is the codex's. A sample:

| word id | sūrah:āyah | rasm on each side | as printed |
|---|---|---|---|
| 425 | 2:28 | `ڡاحٮكم` hafs,shubah,bazzi,duri,susi  ·  `ڡاحٮاكم` qalun,warsh | **فَأَحۡيَٰكُمۡ** hafs,shubah,duri,susi  ·  **فَأَحۡيَٰكُمُۥ** bazzi  ·  **فَأَحْيَاكُمْ** qalun  ·  **فَأَحْيٜاكُمْ** warsh |
| 618 | 2:40 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh |
| 690 | 2:47 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh |
| 823 | 2:57 | `العمام` hafs,shubah,bazzi,duri,susi  ·  `العمم` qalun,warsh | **ٱلۡغَمَامَ** hafs,shubah,bazzi  ·  **ࡲ۬لْغَمَٰمَ** qalun,warsh  ·  **اُ۬لۡغَمَامَ** duri  ·  **ࡲ۬لۡغَمَامَ** susi |
| 1333 | 2:83 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri  ·  **إِسْرَآءِيلَ** qalun,warsh  ·  **إِسۡرَٰٓءِيل** susi |
| 1339 | 2:83 | `احساٮا` hafs,shubah,bazzi,duri,susi  ·  `احسٮا` qalun,warsh | **إِحۡسَانࣰا** hafs,shubah,bazzi,susi  ·  **إِحْسَٰناࣰ** qalun,warsh  ·  **إِحۡسَانٗا** duri |
| 1738 | 2:102 | `هروٮ` hafs,shubah,bazzi,duri,susi  ·  `هاروٮ` qalun,warsh | **هَٰرُوتَ** hafs,shubah,bazzi,duri,susi  ·  **هَارُوتَ** qalun,warsh |
| 1739 | 2:102 | `ومروٮ` hafs,shubah,bazzi,duri,susi  ·  `وماروٮ` qalun,warsh | **وَمَٰرُوتَ** hafs,shubah,bazzi,duri,susi  ·  **وَمَارُوتَ** qalun,warsh |
| 1741 | 2:102 | `ٮعلماں` hafs,shubah,bazzi,duri,susi  ·  `ٮعلمں` qalun,warsh | **يُعَلِّمَانِ** hafs,shubah,bazzi,duri,susi  ·  **يُعَلِّمَٰنِ** qalun,warsh |
| 2147 | 2:121 | `ٮلاوٮه` hafs,shubah,bazzi,duri,susi  ·  `ٮلوٮه` qalun,warsh | **تِلَاوَتِهِۦٓ** hafs,shubah,duri  ·  **تِلَاوَتِهِۦ** bazzi,susi  ·  **تِلَٰوَتِهِۦ** qalun  ·  **تِلَٰوَتِهِۦٓ** warsh |
| 2158 | 2:122 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh |
| 2824 | 2:158 | `سعاٮر` hafs,shubah,bazzi,duri,susi  ·  `سعٮر` qalun,warsh | **شَعَآئِرِ** hafs,shubah,bazzi,duri,susi  ·  **شَعَٰٓئِرِ** qalun,warsh |
| 2991 | 2:166 | `الاسٮاٮ` hafs,shubah,bazzi,duri,susi  ·  `الاسٮٮ` qalun,warsh | **ٱلۡأَسۡبَابُ** hafs,shubah,bazzi  ·  **ࡲ۬لْأَسْبَٰبُ** qalun  ·  **ࡲ۬لَاسْبَٰبُ** warsh  ·  **اِ۬لۡأَسۡبَابُ** duri  ·  **ࡵ۬لۡأَسۡبَابُ** susi |
| 3929 | 2:210 | `العمام` hafs,shubah,bazzi,duri,susi  ·  `العمم` qalun,warsh | **ٱلۡغَمَامِ** hafs,shubah,bazzi  ·  **ࡰ۬لْغَمَٰمِ** qalun,warsh  ·  **اَ۬لۡغَمَامِ** duri  ·  **ࡱ۬لۡغَمَامِ** susi |
| 3939 | 2:211 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh |

### Pointing — one rasm, two qiraahs

338 words share a rasm but are pointed differently. These are real differences in qiraah, not in the codex: an undotted skeleton carries them all. A sample:

| word id | sūrah:āyah | shared rasm | pointed as |
|---|---|---|---|
| 11 | 1:4 | `ملك` | **مالك** hafs,shubah  ·  **ملك** bazzi,qalun,warsh,duri,susi |
| 105 | 2:9 | `ٮحدعوں` | **يخدعون** hafs,shubah  ·  **يخادعون** bazzi,qalun,warsh,duri,susi |
| 709 | 2:48 | `ٮڡٮل` | **يقبل** hafs,shubah,qalun,warsh  ·  **تقبل** bazzi,duri,susi |
| 748 | 2:51 | `وعدٮا` | **واعدنا** hafs,shubah,bazzi,qalun,warsh  ·  **وعدنا** duri,susi |
| 854 | 2:58 | `ٮعڡر` | **نغفر** hafs,shubah,bazzi,duri,susi  ·  **يغفر** qalun,warsh |
| 1142 | 2:72 | `ڡادرٮم` | **فاداراتم** hafs,shubah,bazzi,qalun,duri,susi  ·  **فادارتم** warsh |
| 1196 | 2:74 | `ٮعملوں` | **تعملون** hafs,shubah,qalun,warsh,duri,susi  ·  **يعملون** bazzi |
| 1312 | 2:81 | `حطٮٮه` | **خطيته** hafs,shubah,bazzi,duri,susi  ·  **خطياته** qalun,warsh |
| 1335 | 2:83 | `ٮعٮدوں` | **تعبدون** hafs,shubah,qalun,warsh,duri,susi  ·  **يعبدون** bazzi |
| 1390 | 2:85 | `ٮڡدوهم` | **تفادوهم** hafs,shubah,qalun,warsh  ·  **تفدوهم** bazzi,duri,susi |
| 1421 | 2:85 | `ٮعملوں` | **تعملون** hafs,duri,susi  ·  **يعملون** shubah,bazzi,qalun,warsh |
| 1670 | 2:98 | `ومٮكٮل` | **وميكيال** hafs,duri,susi  ·  **وميكايل** shubah,bazzi,qalun,warsh |
| 2479 | 2:140 | `ٮڡولوں` | **تقولون** hafs  ·  **يقولون** shubah,bazzi,qalun,warsh,duri,susi |
| 2711 | 2:149 | `ٮعملوں` | **تعملون** hafs,shubah,bazzi,qalun,warsh  ·  **يعملون** duri,susi |
| 2966 | 2:165 | `ٮرى` | **يري** hafs,shubah,bazzi,duri,susi  ·  **تري** qalun,warsh |

### Boundaries — where the space falls

A boundary disagreement is never about one word; it is about the space between two. Each event below shows the whole run, exactly as each riwāyah prints it. The last column is the one that matters: **agree** means every riwāyah reads the run identically once it is re-segmented, so the flag is a *source* that lost a space, not a muṣḥaf that really prints the words joined.

**4:91** — word ids 11634, 11635 · joined in `duri`, `qalun` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | مَا رُدُّوٓاْ |
| `bazzi,qalun,susi` | مَا رُدُّواْ |

**10:26** — word ids 26811, 26812 · joined in `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,qalun,warsh,susi` | قَتَرࣱ وَلَا |
| `duri` | قَتَرٞ وَلَا |

**11:78** — word ids 29368, 29369 · joined in `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi` | كَانُواْ يَعۡمَلُونَ |
| `qalun,warsh` | كَانُواْ يَعْمَلُونَ |

**27:20** — word ids 48679, 48680 · joined in `bazzi`, `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi` | مَا لِيَ |
| `qalun,warsh` | مَا لِے |
| `duri,susi` | مَا لِي |

**36:22** — word ids 56845, 56846 · joined in `bazzi`, `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,qalun,warsh,duri,susi` | وَمَا لِيَ |

**75:1** — word ids 74539, 74540 · joined in `bazzi` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَآ أُقۡسِمُ |
| `bazzi` | لَأُ اْقۡسِمُ |
| `qalun` | لَا أُقْسِمُ |
| `warsh` | لَآ أُقْسِمُ |
| `susi` | لَا أُقۡسِم |

Machine-readable: [`resegmentation.csv`](resegmentation.csv).

### Absence — words not every riwāyah has

Each is well attested: Ibn Kathīr's `مِن` at 9:101; Nāfiʿ reciting `فإن الله الغني` at 57:24 where the others read `فإن الله هو الغني`; and `أَوۡ` at 40:26, where Ḥafṣ and Shuʿbah read *aw* and the other five read *wa* — a different word, so the number of `أَوۡ` is absent from them and their `وَأَنْ` takes the number of `أَن`.

| number | sūrah:āyah | rasm | present in | absent from | as printed |
|---|---|---|---|---|---|
| 25685 | 9:101 | `مں` | bazzi | hafs, shubah, warsh, qalun, duri, susi | **مِن** bazzi |
| 60522 | 40:26 | `او` | hafs, shubah | warsh, qalun, duri, susi, bazzi | **أَوۡ** hafs,shubah |
| 69720 | 57:24 | `هو` | hafs, shubah, duri, susi, bazzi | warsh, qalun | **هُوَ** hafs,shubah,bazzi,duri  ·  **هُّوَ** susi |

### Written joined — two words some muṣḥafs print as one

Nothing is added and nothing is dropped: the nūn assimilates into the letter after it and is not written, so the same two words are printed as one. The numbering counts the finest division, so both words keep a number and the joined word *covers* both — recorded in each muṣḥaf's `numbering.written_joined`, never as a missing word. Declared in `sources/alignment/written-joined.json`.

| number | sūrah:āyah | rasm | written joined by | as printed |
|---|---|---|---|---|
| 73950 | 72:16 | `واں` | hafs, shubah, bazzi | **وَأَلَّوِ** hafs,shubah,bazzi  ·  **وَأَن** qalun,warsh,duri,susi |
| 73951 | 72:16 | `لو` | hafs, shubah, bazzi | **وَأَلَّوِ** hafs,shubah,bazzi  ·  **لَّوِ** qalun,warsh,duri,susi |
| 74226 | 73:20 | `اں` | duri, susi | **أَن** hafs,shubah,bazzi,qalun,warsh  ·  **أَلَّن** duri,susi |
| 74227 | 73:20 | `لں` | duri, susi | **لَّن** hafs,shubah,bazzi,qalun,warsh  ·  **أَلَّن** duri,susi |

## Fawāṣil: where the āyāt end

The āyah boundaries are a layer *over* the word index, not a property of it, and **the count belongs to the printed edition, not to the riwāyah**. An edition follows one of the six classical counting systems, and at the points where the system's own authorities disagree it follows one of them: al-Dānī records Mulk 67:9 «قد جاءنا نذير» as counted by Shayba and not by Abū Jaʿfar inside the First Madani, and KFGQPC's own Dūrī printings all state they follow المدني الأول and still total 6,218 (1429 AH), 6,217 (1436) and 6,214 (1443).

Each edition's system is **derived** by comparing its own āyah ends to every system's boundaries (from [qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map), vendored under `sources/counting/`), then the points of khilāf inside the system are named with the authority the edition follows. Whatever is left is `unexplained` and is an open finding. Machine-readable: [`counting.json`](../counting.json).

| muṣḥaf | system |  | āyāt | basmalah counted | khilāf inside the system | unexplained |
|---|---|---|---|---|---|---|
| hafs | `kufi` | الكوفي | 6,236 | yes | — | — |
| shubah | `kufi` | الكوفي | 6,236 | yes | — | — |
| warsh | `madani-last` | المدني الأخير | 6,214 | no | — | — |
| qalun | `madani-last` | المدني الأخير | 6,214 | no | — | — |
| duri | `madani-first` | المدني الأول | 6,217 | no | 3:92 counted (shayba); 3:97 not counted (shayba); 37:167 counted (shayba); 67:9 not counted (abu-jafar); 80:24 counted (shayba); 81:26 counted (shayba) | — |
| susi | `madani-first` | المدني الأول | 6,218 | no | 3:92 counted (shayba); 3:97 not counted (shayba); 37:167 counted (shayba); 67:9 counted (shayba); 80:24 counted (shayba); 81:26 counted (shayba) | — |
| bazzi | `makki` | المكي | 6,220 | yes | 78:40 counted () | — |

| edition | `hafs` | `shubah` | `warsh` | `qalun` | `duri` | `susi` | `bazzi` |
|---|---|---|---|---|---|---|---|
| `hafs` | — | 0 | 140 | 140 | 133 | 134 | 150 |
| `shubah` | 0 | — | 140 | 140 | 133 | 134 | 150 |
| `warsh` | 140 | 140 | — | 0 | 57 | 56 | 48 |
| `qalun` | 140 | 140 | 0 | — | 57 | 56 | 48 |
| `duri` | 133 | 133 | 57 | 57 | — | 1 | 39 |
| `susi` | 134 | 134 | 56 | 56 | 1 | — | 38 |
| `bazzi` | 150 | 150 | 48 | 48 | 39 | 38 | — |

Āyah ends where two editions differ. Dūrī and Sūsī, both First Madani, part company at exactly one place — 67:9 — which is the whole of the 6,217/6,218 difference between them: Dūrī follows Abū Jaʿfar there and Sūsī follows Shayba. Bazzī counts 78:40, which no source yet gives to the Makkī count; it is reported as an open finding, not corrected.

## Source integrity

Six riwāyāt ship two releases. Comparing them is the sharpest available check on each, since the publisher is the same.

**Where the two releases disagree, the later one is the text.** KFGQPC revises these documents deliberately: the 2026 Ḥafṣ separates `مَا لِيَ` where Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`. That is a change of convention, not a defect, and the newer convention is the one published here. The earlier release is never merged into the text — it is only compared against it, below. The rule cannot discriminate for Dūrī, whose two packages are both from 2022; its three dropped spaces are recorded as boundary events instead.

| riwāyah | āyāt compared | byte-identical | notation only | marks/vowels only | rasm differs |
|---|---|---|---|---|---|
| hafs | 6,236 | 2,715 | 700 | 2,819 | 2 |
| shubah | 6,236 | 2,715 | 697 | 2,822 | 2 |
| warsh | 6,214 | 160 | 410 | 5,635 | 9 |
| qalun | 6,214 | 733 | 2,319 | 3,154 | 8 |
| duri | 6,217 | 6,214 | 0 | 0 | 3 |
| susi | 6,217 | 508 | 1,916 | 3,768 | 25 |

`notation only` is dominated by the 2026 files adopting the Arabic Extended-B alif letters (`U+0870`–`U+0882`), which fold an alef and its vowel into one codepoint where the 2022 files used an alef plus combining marks. The `folded` form decomposes them again, so none of it reaches the word index.

### Checks

All checks pass.

## Per sūrah

| sūrah | name | words | identical | diacritic | dotting | ā | rasm | boundary/absent | per 1000 |
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
| 72 | Al-Jinn | 286 | 138 | 144 | 1 | 0 | 1 | 2 | 10.5 |
| 73 | Al-Muzzammil | 199 | 99 | 98 | 0 | 0 | 0 | 2 | 10.1 |
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
