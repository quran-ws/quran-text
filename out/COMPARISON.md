# Cross-riwāyah comparison

Generated 2026-09-01 from the KFGQPC packages in `data/`. 77,434 canonical words across 114 sūrahs and 7 riwāyāt.

Every word carries one ID that means the same word in every riwāyah that has it. Where the riwāyāt disagree, the disagreement is recorded against that ID rather than hidden by it.

## What is being compared

A word is never compared as raw text. Four forms are derived from every spelling, each stripping one more layer of what a scribe added after the codices were written. Two riwāyāt are said to agree *at a level* when their forms at that level are identical.

| form | question it answers | example | and what it drops |
|---|---|---|---|
| `uthmani` | how is it printed? | `مَٰلِكِ` | — |
| `folded` | what does it say, ignoring which codepoints the release chose? | `مَٰلِكِ` | release notation, attached-alef letters, editorial marks |
| `pointed` | which letters, dots and all? | `مالك` | vowels, hamza, madd, ṣilah |
| `rasm` | what is on the line in the codex? | `مالك` | the dots |

The two skeletons are separate on purpose. `تَعۡمَلُونَ` and `يَعۡمَلُونَ` have different `pointed` forms but one `rasm` — `ٮعملوں` — because the codices were written undotted and carry both readings by design. Calling that a rasm variant would be a category error; calling it vowelling would hide a real reading. It is named **`dotting_variant`**.

`rasm` drops hamza and every hamza carrier reduces to its seat, because hamza is post-ʿUthmānic notation: `يَسۡتَهۡزِئُ` and `يَسْتَهْزِۓُ` are one word. Dagger alif and written alef are also one ā — `هَٰرُوتَ` and `هَارُوتَ` — since the packages differ only in where the publisher put it.

## The riwāyāt

| key | riwāyah | الرواية | qāriʾ | counting | āyāt | words |
|---|---|---|---|---|---|---|
| hafs | Ḥafṣ | حفص | ʿĀṣim al-Kūfī | kufi | 6,236 | 77,432 |
| shuba | Shuʿbah | شعبة | ʿĀṣim al-Kūfī | kufi | 6,236 | 77,432 |
| warsh | Warsh | ورش | Nāfiʿ al-Madanī | madani | 6,214 | 77,431 |
| qaloun | Qālūn | قالون | Nāfiʿ al-Madanī | madani | 6,214 | 77,431 |
| douri | Dūrī | الدوري | Abū ʿAmr al-Baṣrī | basri | 6,217 | 77,431 |
| sousi | Sūsī | السوسي | Abū ʿAmr al-Baṣrī | basri | 6,218 | 77,431 |
| bazzi | Bazzī | البزي | Ibn Kathīr al-Makkī | makki | 6,220 | 77,432 |

The āyah totals are not errors and not deducible from the qāriʾ. Many fawāṣil are مختلف فيها, so every printed muṣḥaf chooses, and the `counting` column above is a conventional label rather than a claim about this package. That is exactly why the index is flat, and why the āyah boundaries are read off each muṣḥaf rather than assumed: see [the fawāṣil](#fawāṣil-where-the-āyāt-end) below.

## How the words compare

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 40,558 | 52.38% | one reading, one spelling, in all seven |
| `diacritic_variant` | 36,459 | 47.08% | same letters and same dots — the vowelling differs |
| `dotting_variant` | 168 | 0.22% | one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ |
| `rasm_variant` | 232 | 0.30% | the codices disagree about the letters on the line |
| `word_boundary` | 12 | 0.02% | a source prints the word joined to its neighbour |
| `partial` | 5 | 0.01% | the word is absent from at least one riwāyah |

Each word gets the *strongest* label that applies, tested in this order: rasm, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed to share one rasm across all seven, and an `identical` word is identical after notation folding — the raw spelling of every riwāyah is always kept in `forms`, whatever the label.

## Pairwise agreement

Share of the words two riwāyāt both have, where they agree at each level.

| pair | shared words | same spelling | same reading | same letters | same rasm |
|---|---|---|---|---|---|
| douri–sousi | 77,431 | 66.7% | 82.8% | 99.97% | 99.97% |
| warsh–qaloun | 77,431 | 85.2% | 87.5% | 99.95% | 99.95% |
| hafs–shuba | 77,432 | 99.2% | 99.2% | 99.86% | 99.94% |
| douri–bazzi | 77,430 | 57.8% | 61.0% | 99.84% | 99.91% |
| sousi–bazzi | 77,430 | 66.6% | 67.4% | 99.81% | 99.88% |
| qaloun–douri | 77,430 | 36.8% | 78.5% | 99.75% | 99.87% |
| shuba–douri | 77,430 | 70.9% | 74.1% | 99.76% | 99.87% |
| shuba–bazzi | 77,431 | 84.1% | 84.1% | 99.75% | 99.87% |
| hafs–douri | 77,430 | 70.8% | 74.1% | 99.74% | 99.87% |
| shuba–qaloun | 77,430 | 40.5% | 76.6% | 99.77% | 99.87% |
| warsh–sousi | 77,430 | 39.2% | 77.7% | 99.74% | 99.86% |
| qaloun–bazzi | 77,430 | 41.5% | 70.8% | 99.76% | 99.86% |
| hafs–qaloun | 77,430 | 40.4% | 76.6% | 99.76% | 99.86% |
| hafs–bazzi | 77,431 | 84.0% | 84.0% | 99.73% | 99.86% |
| qaloun–sousi | 77,430 | 42.6% | 84.4% | 99.72% | 99.85% |
| shuba–sousi | 77,430 | 72.1% | 72.9% | 99.73% | 99.84% |
| warsh–douri | 77,430 | 37.8% | 76.3% | 99.72% | 99.84% |
| hafs–sousi | 77,430 | 72.0% | 72.8% | 99.71% | 99.84% |
| warsh–bazzi | 77,430 | 37.2% | 63.4% | 99.73% | 99.83% |
| shuba–warsh | 77,430 | 41.4% | 75.2% | 99.73% | 99.83% |
| hafs–warsh | 77,430 | 41.3% | 75.2% | 99.72% | 99.82% |

Rasm agreement never drops below 99.5%: the seven riwāyāt are one text. Spelling agreement is far lower because the packages were typeset in different years with different conventions — which is what the `folded` and `pointed` columns strip away.

## Where the riwāyāt genuinely disagree

Three things can differ once spelling, vowelling and pointing are set aside: the letters, the word boundaries, and whether a word is there at all. Together they account for 249 of 77,434 words.

| kind | count | status | what it means |
|---|---|---|---|
| letters differ | 232 | `rasm_variant` | the codices are pointed from different exemplars |
| boundaries differ | 6 events | `word_boundary` | one source prints two words as one |
| word absent | 5 | `partial` | a riwāyah does not have the word at all |

### Letters — rasm disagreements

232 words where the riwāyāt disagree about the letters on the line, after dots, hamza and vowelling have been set aside. The full list is in [`rasm-variants.md`](rasm-variants.md) and [`conflicts.csv`](conflicts.csv); the first 25 follow.

| word id | sūrah:āyah | rasm on each side | as printed |
|---|---|---|---|
| 11 | 1:4 | `مالك` hafs,shuba  ·  `ملك` bazzi,qaloun,warsh,douri,sousi | **مَٰلِكِ** hafs,shuba  ·  **مَلِكِ** bazzi,qaloun,warsh,douri  ·  **مَّلِكِ** sousi |
| 105 | 2:9 | `ٮحدعوں` hafs,shuba  ·  `ٮحادعوں` bazzi,qaloun,warsh,douri,sousi | **يَخۡدَعُونَ** hafs,shuba  ·  **يُخَٰدِعُونَ** bazzi,qaloun,warsh,douri,sousi |
| 748 | 2:51 | `واعدٮا` hafs,shuba,bazzi,qaloun,warsh  ·  `وعدٮا` douri,sousi | **وَٰعَدۡنَا** hafs,shuba,bazzi  ·  **وَٰعَدْنَا** qaloun,warsh  ·  **وَعَدۡنَا** douri,sousi |
| 1142 | 2:72 | `ڡاداراٮم` hafs,shuba,bazzi,qaloun,douri,sousi  ·  `ڡادارٮم` warsh | **فَٱدَّٰرَٰءۡتُمۡ** hafs,shuba  ·  **فَٱدَّٰرَٰءۡتُمُۥ** bazzi  ·  **فَادَّٰرَٰءْتُمْ** qaloun  ·  **فَادَّٰرْٔتُمْ** warsh  ·  **فَاَدَّٰرَٰءۡتُمۡ** douri  ·  **فَاَدَّٰرَٰتُمۡ** sousi |
| 1312 | 2:81 | `حطٮٮه` hafs,shuba,bazzi,douri,sousi  ·  `حطٮاٮه` qaloun,warsh | **خَطِيَٓٔتُهُۥ** hafs,shuba,bazzi,douri,sousi  ·  **خَطِيَٰٓٔتُهُۥ** qaloun,warsh |
| 1390 | 2:85 | `ٮڡادوهم` hafs,shuba,qaloun,warsh  ·  `ٮڡدوهم` bazzi,douri,sousi | **تُفَٰدُوهُمۡ** hafs,shuba  ·  **تَفۡدُوهُمُۥ** bazzi  ·  **تُفَٰدُوهُمْ** qaloun,warsh  ·  **تَفۡدُوهُمۡ** douri,sousi |
| 1670 | 2:98 | `ومٮكٮال` hafs,douri,sousi  ·  `ومٮكاٮل` shuba,bazzi,qaloun,warsh | **وَمِيكَىٰلَ** hafs,douri,sousi  ·  **وَمِيكَِٰٓٔيلَ** shuba,bazzi  ·  **وَمِيكَٰٓئِلَ** qaloun,warsh |
| 2331 | 2:132 | `ووصٮا` hafs,shuba,bazzi,douri,sousi  ·  `واوصٮا` qaloun,warsh | **وَوَصَّىٰ** hafs,shuba,bazzi,douri,sousi  ·  **وَأَوْصَىٰ** qaloun  ·  **وَأَوْصٜىٰ** warsh |
| 3349 | 2:184 | `مسكٮں` hafs,shuba,bazzi,douri,sousi  ·  `مساكٮں` qaloun,warsh | **مِسۡكِينࣲ** hafs,shuba,bazzi  ·  **مَسَٰكِينَ** qaloun,warsh  ·  **مِسۡكِينٖ** douri  ·  **مِّسۡكِينࣲ** sousi |
| 4855 | 2:245 | `ڡٮصاعڡه` hafs,shuba,qaloun,warsh,douri,sousi  ·  `ڡٮصعڡه` bazzi | **فَيُضَٰعِفَهُۥ** hafs,shuba  ·  **فَيُضَعِّفُهُۥ** bazzi  ·  **فَيُضَٰعِفُهُۥ** qaloun,warsh,douri,sousi |
| 5080 | 2:251 | `دڡع` hafs,shuba,bazzi,douri,sousi  ·  `دڡاع` qaloun,warsh | **دَفۡعُ** hafs,shuba,bazzi,douri,sousi  ·  **دِفَٰعُ** qaloun,warsh |
| 5440 | 2:261 | `ٮصاعڡ` hafs,shuba,qaloun,warsh,douri,sousi  ·  `ٮصعڡ` bazzi | **يُضَٰعِفُ** hafs,shuba,qaloun,warsh,douri,sousi  ·  **يُضَعِّفُ** bazzi |
| 6018 | 2:283 | `ڡرهاں` hafs,shuba,qaloun,warsh  ·  `ڡرهں` bazzi,douri,sousi | **فَرِهَٰنࣱ** hafs,shuba,qaloun,warsh  ·  **فَرُهُنࣱ** bazzi,sousi  ·  **فَرُهُنٞ** douri |
| 6990 | 3:49 | `طٮرا` hafs,shuba,bazzi,douri,sousi  ·  `طاٮرا` qaloun,warsh | **طَيۡرَۢا** hafs,shuba,bazzi,douri,sousi  ·  **طَٰٓئِراَۢ** qaloun,warsh |
| 7534 | 3:81 | `اٮٮٮكم` hafs,shuba,bazzi,douri,sousi  ·  `اٮٮٮاكم` qaloun,warsh | **ءَاتَيۡتُكُم** hafs,shuba,douri,sousi  ·  **ءَاتَيۡتُكُمُۥ** bazzi  ·  **ءَاتَيْنَٰكُم** qaloun,warsh |
| 8338 | 3:130 | `مصاعڡه` hafs,shuba,qaloun,warsh,douri,sousi  ·  `مصعڡه` bazzi | **مُّضَٰعَفَةࣰ** hafs,shuba,qaloun,warsh,sousi  ·  **مُّضَعَّفَةࣰ** bazzi  ·  **مُّضَٰعَفَةٗ** douri |
| 8353 | 3:133 | `وسارعوا` hafs,shuba,bazzi,douri,sousi  ·  `سارعوا` qaloun,warsh | **وَسَارِعُوٓاْ** hafs,shuba,douri  ·  **وَسَارِعُواْ** bazzi,sousi  ·  **سَارِعُواْ** qaloun  ·  **سَارِعُوٓاْ** warsh |
| 8552 | 3:146 | `ڡاٮل` hafs,shuba  ·  `ڡٮل` bazzi,qaloun,warsh,douri,sousi | **قَٰتَلَ** hafs,shuba  ·  **قُتِلَ** bazzi,qaloun,warsh,douri,sousi |
| 8851 | 3:158 | `لالى` hafs,shuba,bazzi,qaloun,warsh  ·  `لاالى` douri,sousi | **لَإِلَى** hafs,shuba,bazzi,qaloun,warsh  ·  **لَإِاْلَى** douri,sousi |
| 9722 | 4:5 | `ڡٮاما` hafs,shuba,bazzi,douri,sousi  ·  `ڡٮما` qaloun,warsh | **قِيَٰمࣰا** hafs,shuba,bazzi,sousi  ·  **قِيَماࣰ** qaloun,warsh  ·  **قِيَٰمٗا** douri |
| 9878 | 4:11 | `ٮوصى` hafs,qaloun,warsh,douri,sousi  ·  `ٮوصٮا` shuba,bazzi | **يُوصِي** hafs,douri,sousi  ·  **يُوصَىٰ** shuba,bazzi  ·  **يُوصِے** qaloun,warsh |
| 9974 | 4:12 | `ٮوصٮا` hafs,shuba,bazzi  ·  `ٮوصى` qaloun,warsh,douri,sousi | **يُوصَىٰ** hafs,shuba,bazzi  ·  **يُوصِے** qaloun,warsh  ·  **يُوصِي** douri,sousi |
| 10017 | 4:15 | `والاٮى` hafs,shuba,bazzi,qaloun,douri,sousi  ·  `والٮى` warsh | **وَٱلَّٰتِي** hafs,shuba,bazzi  ·  **وَالَّٰتِے** qaloun  ·  **وَالتِے** warsh  ·  **وَاَلَّٰتِي** douri  ·  **وَࡱلَّٰتِي** sousi |
| 10188 | 4:23 | `الاٮى` hafs,shuba,bazzi,qaloun,douri,sousi  ·  `الٮى` warsh | **ٱلَّٰتِيٓ** hafs,shuba  ·  **ٱلَّٰتِي** bazzi  ·  **ࡲ۬لَّٰتِے** qaloun  ·  **ࡲ۬لتِےٓ** warsh  ·  **اُ۬لَّٰتِيٓ** douri  ·  **ࡲ۬لَّٰتِي** sousi |
| 10196 | 4:23 | `الاٮى` hafs,shuba,bazzi,qaloun,douri,sousi  ·  `الٮى` warsh | **ٱلَّٰتِي** hafs,shuba,bazzi  ·  **ࡲ۬لَّٰتِے** qaloun  ·  **ࡲ۬لتِے** warsh  ·  **اُ۬لَّٰتِي** douri  ·  **ࡲ۬لَّٰتِي** sousi |

### Pointing — one rasm, two readings

168 words share a rasm but are pointed differently. These are real differences in reading, not in the codex: an undotted skeleton carries them all. A sample:

| word id | sūrah:āyah | shared rasm | pointed as |
|---|---|---|---|
| 709 | 2:48 | `ٮڡٮل` | **يقبل** hafs,shuba,qaloun,warsh  ·  **تقبل** bazzi,douri,sousi |
| 854 | 2:58 | `ٮعڡر` | **نغفر** hafs,shuba,bazzi,douri,sousi  ·  **يغفر** qaloun,warsh |
| 1196 | 2:74 | `ٮعملوں` | **تعملون** hafs,shuba,qaloun,warsh,douri,sousi  ·  **يعملون** bazzi |
| 1335 | 2:83 | `ٮعٮدوں` | **تعبدون** hafs,shuba,qaloun,warsh,douri,sousi  ·  **يعبدون** bazzi |
| 1421 | 2:85 | `ٮعملوں` | **تعملون** hafs,douri,sousi  ·  **يعملون** shuba,bazzi,qaloun,warsh |
| 2479 | 2:140 | `ٮڡولوں` | **تقولون** hafs  ·  **يقولون** shuba,bazzi,qaloun,warsh,douri,sousi |
| 2711 | 2:149 | `ٮعملوں` | **تعملون** hafs,shuba,bazzi,qaloun,warsh  ·  **يعملون** douri,sousi |
| 2966 | 2:165 | `ٮرى` | **يري** hafs,shuba,bazzi,douri,sousi  ·  **تري** qaloun,warsh |
| 5368 | 2:259 | `ٮٮسرها` | **ننشزها** hafs,shuba  ·  **ننشرها** bazzi,qaloun,warsh,douri,sousi |
| 5666 | 2:271 | `وٮكڡر` | **ويكفر** hafs  ·  **ونكفر** shuba,bazzi,qaloun,warsh,douri,sousi |
| 6335 | 3:13 | `ٮروٮهم` | **يرونهم** hafs,shuba,bazzi,douri,sousi  ·  **ترونهم** qaloun,warsh |
| 6965 | 3:48 | `وٮعلمه` | **ويعلمه** hafs,shuba,qaloun,warsh  ·  **ونعلمه** bazzi,douri,sousi |
| 7125 | 3:57 | `ڡٮوڡٮهم` | **فيوفيهم** hafs  ·  **فنوفيهم** shuba,bazzi,qaloun,warsh,douri,sousi |
| 7571 | 3:83 | `ٮٮعوں` | **يبغون** hafs,douri,sousi  ·  **تبغون** shuba,bazzi,qaloun,warsh |
| 7581 | 3:83 | `ٮرحعوں` | **يرجعون** hafs  ·  **ترجعون** shuba,bazzi,qaloun,warsh,douri,sousi |

### Boundaries — where the space falls

A boundary disagreement is never about one word; it is about the space between two. Each event below shows the whole run, exactly as each riwāyah prints it. The last column is the one that matters: **agree** means every riwāyah reads the run identically once it is re-segmented, so the flag is a *source* that lost a space, not a muṣḥaf that really prints the words joined.

**4:91** — word ids 11634, 11635 · joined in `douri`, `qaloun` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shuba,warsh,douri` | مَا رُدُّوٓاْ |
| `bazzi,qaloun,sousi` | مَا رُدُّواْ |

**10:26** — word ids 26811, 26812 · joined in `douri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shuba,bazzi,qaloun,warsh,sousi` | قَتَرࣱ وَلَا |
| `douri` | قَتَرٞ وَلَا |

**11:78** — word ids 29368, 29369 · joined in `douri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shuba,bazzi,douri,sousi` | كَانُواْ يَعۡمَلُونَ |
| `qaloun,warsh` | كَانُواْ يَعْمَلُونَ |

**27:20** — word ids 48679, 48680 · joined in `bazzi`, `douri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shuba,bazzi` | مَا لِيَ |
| `qaloun,warsh` | مَا لِے |
| `douri,sousi` | مَا لِي |

**36:22** — word ids 56845, 56846 · joined in `bazzi`, `douri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shuba,bazzi,qaloun,warsh,douri,sousi` | وَمَا لِيَ |

**75:1** — word ids 74539, 74540 · joined in `bazzi` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shuba,douri` | لَآ أُقۡسِمُ |
| `bazzi` | لَأُ اْقۡسِمُ |
| `qaloun` | لَا أُقْسِمُ |
| `warsh` | لَآ أُقْسِمُ |
| `sousi` | لَا أُقۡسِم |

Machine-readable: [`boundaries.csv`](boundaries.csv).

### Absence — words not every riwāyah has

Each is well attested: Ibn Kathīr's `مِن` at 9:100, and Nāfiʿ reading `فإن الله الغني` at 57:24 where the others read `فإن الله هو الغني`. The rest are words one riwāyah writes joined to its neighbour and another writes separately, so the count of words genuinely differs.

| word id | sūrah:āyah | rasm | present in | absent from | as printed |
|---|---|---|---|---|---|
| 25685 | 9:101 | `مں` | bazzi | hafs, shuba, warsh, qaloun, douri, sousi | **مِن** bazzi |
| 60523 | 40:26 | `اں` | hafs, shuba | warsh, qaloun, douri, sousi, bazzi | **أَن** hafs,shuba |
| 69720 | 57:24 | `هو` | hafs, shuba, douri, sousi, bazzi | warsh, qaloun | **هُوَ** hafs,shuba,bazzi,douri  ·  **هُّوَ** sousi |
| 73951 | 72:16 | `لو` | warsh, qaloun, douri, sousi | hafs, shuba, bazzi | **لَّوِ** qaloun,warsh,douri,sousi |
| 74227 | 73:20 | `لں` | hafs, shuba, warsh, qaloun, bazzi | douri, sousi | **لَّن** hafs,shuba,bazzi,qaloun,warsh |

## Fawāṣil: where the āyāt end

The āyah boundaries are a layer *over* the word index, not a property of it, and **they belong to the printed muṣḥaf rather than to the qirāʾah**. Many fawāṣil are مختلف فيها: al-Dānī records Al-Mulk 67:9 «قد جاءنا نذير» as counted by المدني الأخير والمكي and by Shayba and not by the rest, and four of the seven packages here count it. An edition has to choose, and editions of the same riwāyah choose differently — KFGQPC's own Dūrī printings all state they follow المدني الأول and still total 6,218 (1429 AH), 6,217 (1436) and 6,214 (1443).

So the systems below are not counting traditions and are not derived from any. They are read off the packages, and two riwāyāt are grouped only where their fawāṣil are identical. Machine-readable: [`fawasil.json`](fawasil.json).

| system | muṣḥaf | āyāt |
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

Positions where two systems put a fāṣilah differently. Dūrī and Sūsī are both conventionally labelled Baṣrī and part company at exactly one place — 67:9 — which is the whole of the 6,217/6,218 difference between them, and is a documented خلافي point rather than a mistake by either.

## Source integrity

Six riwāyāt ship two releases. Comparing them is the sharpest available check on each, since the publisher is the same.

**Where the two releases disagree, the later one is the text.** KFGQPC revises these documents deliberately: the 2026 Ḥafṣ separates `مَا لِيَ` where Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`. That is a change of convention, not a defect, and the newer convention is the one published here. The earlier release is never merged into the text — it is only compared against it, below. The rule cannot discriminate for Dūrī, whose two packages are both from 2022; its three dropped spaces are recorded as boundary events instead.

| riwāyah | āyāt compared | byte-identical | notation only | marks/vowels only | rasm differs |
|---|---|---|---|---|---|
| hafs | 6,236 | 2,715 | 700 | 2,819 | 2 |
| shuba | 6,236 | 2,715 | 697 | 2,822 | 2 |
| warsh | 6,214 | 160 | 410 | 5,634 | 10 |
| qaloun | 6,214 | 733 | 2,319 | 3,138 | 24 |
| douri | 6,217 | 6,214 | 0 | 0 | 3 |
| sousi | 6,217 | 508 | 1,916 | 3,768 | 25 |

`notation only` is dominated by the 2026 files adopting the Arabic Extended-B alif letters (`U+0870`–`U+0882`), which fold an alef and its vowel into one codepoint where the 2022 files used an alef plus combining marks. The `folded` form decomposes them again, so none of it reaches the word index.

### Checks

All checks pass.

## Per sūrah

| sūrah | name | words | identical | diacritic | dotting | rasm | boundary/absent | per 1000 |
|---|---|---|---|---|---|---|---|---|
| 1 | Al-Fātiḥah | 29 | 11 | 17 | 0 | 1 | 0 | 34.5 |
| 2 | Al-Baqarah | 6,117 | 3181 | 2914 | 10 | 12 | 0 | 2.0 |
| 3 | Āl-‘Imrān | 3,481 | 1767 | 1694 | 14 | 6 | 0 | 1.7 |
| 4 | An-Nisā’ | 3,747 | 1842 | 1884 | 6 | 13 | 2 | 4.0 |
| 5 | Al-Mā’idah | 2,804 | 1362 | 1437 | 0 | 5 | 0 | 1.8 |
| 6 | Al-An‘ām | 3,050 | 1645 | 1387 | 11 | 7 | 0 | 2.3 |
| 7 | Al-A‘rāf | 3,320 | 1779 | 1525 | 7 | 9 | 0 | 2.7 |
| 8 | Al-Anfāl | 1,234 | 592 | 635 | 4 | 3 | 0 | 2.4 |
| 9 | At-Taubah | 2,499 | 1207 | 1279 | 3 | 9 | 1 | 4.0 |
| 10 | Yūnus | 1,833 | 1011 | 813 | 3 | 4 | 2 | 3.3 |
| 11 | Hūd | 1,917 | 1091 | 820 | 1 | 3 | 2 | 2.6 |
| 12 | Yūsuf | 1,777 | 965 | 795 | 4 | 13 | 0 | 7.3 |
| 13 | Ar-Ra‘d | 854 | 454 | 396 | 3 | 1 | 0 | 1.2 |
| 14 | Ibrāhīm | 830 | 429 | 400 | 0 | 1 | 0 | 1.2 |
| 15 | Al-Ḥijr | 654 | 400 | 251 | 1 | 2 | 0 | 3.1 |
| 16 | An-Naḥl | 1,844 | 958 | 878 | 5 | 3 | 0 | 1.6 |
| 17 | Al-Isrā’ | 1,556 | 818 | 728 | 8 | 2 | 0 | 1.3 |
| 18 | Al-Kahf | 1,579 | 809 | 765 | 1 | 4 | 0 | 2.5 |
| 19 | Maryam | 961 | 485 | 473 | 2 | 1 | 0 | 1.0 |
| 20 | Ṭā-Hā | 1,335 | 717 | 610 | 2 | 6 | 0 | 4.5 |
| 21 | Al-Anbiyā’ | 1,169 | 644 | 516 | 1 | 8 | 0 | 6.8 |
| 22 | Al-Ḥajj | 1,274 | 657 | 611 | 2 | 4 | 0 | 3.1 |
| 23 | Al-Mu’minūn | 1,050 | 580 | 463 | 0 | 7 | 0 | 6.7 |
| 24 | An-Nūr | 1,316 | 639 | 669 | 1 | 7 | 0 | 5.3 |
| 25 | Al-Furqān | 893 | 456 | 430 | 3 | 4 | 0 | 4.5 |
| 26 | Ash-Shu‘arā’ | 1,318 | 733 | 582 | 0 | 3 | 0 | 2.3 |
| 27 | An-Naml | 1,151 | 639 | 498 | 8 | 4 | 2 | 5.2 |
| 28 | Al-Qaṣaṣ | 1,430 | 809 | 615 | 2 | 4 | 0 | 2.8 |
| 29 | Al-‘Ankabūt | 976 | 497 | 474 | 4 | 1 | 0 | 1.0 |
| 30 | Ar-Rūm | 817 | 421 | 388 | 4 | 4 | 0 | 4.9 |
| 31 | Luqmān | 546 | 293 | 251 | 1 | 1 | 0 | 1.8 |
| 32 | As-Sajdah | 372 | 208 | 164 | 0 | 0 | 0 | 0.0 |
| 33 | Al-Aḥzāb | 1,287 | 616 | 659 | 5 | 7 | 0 | 5.4 |
| 34 | Saba’ | 883 | 490 | 385 | 2 | 6 | 0 | 6.8 |
| 35 | Fāṭir | 775 | 421 | 350 | 0 | 4 | 0 | 5.2 |
| 36 | Yā-Sīn | 725 | 362 | 356 | 2 | 3 | 2 | 6.9 |
| 37 | Aṣ-Ṣāffāt | 861 | 484 | 376 | 0 | 1 | 0 | 1.2 |
| 38 | Ṣād | 733 | 422 | 309 | 1 | 1 | 0 | 1.4 |
| 39 | Az-Zumar | 1,172 | 625 | 542 | 0 | 5 | 0 | 4.3 |
| 40 | Ghāfir | 1,219 | 632 | 581 | 3 | 2 | 1 | 2.5 |
| 41 | Fuṣṣilat | 794 | 414 | 378 | 1 | 1 | 0 | 1.3 |
| 42 | Ash-Shūra | 860 | 430 | 424 | 3 | 3 | 0 | 3.5 |
| 43 | Az-Zukhruf | 830 | 447 | 375 | 2 | 6 | 0 | 7.2 |
| 44 | Ad-Dukhān | 346 | 198 | 147 | 1 | 0 | 0 | 0.0 |
| 45 | Al-Jāthiyah | 488 | 266 | 221 | 1 | 0 | 0 | 0.0 |
| 46 | Al-Aḥqāf | 643 | 344 | 293 | 5 | 1 | 0 | 1.6 |
| 47 | Muḥammad | 539 | 241 | 293 | 3 | 2 | 0 | 3.7 |
| 48 | Al-Fatḥ | 560 | 267 | 285 | 8 | 0 | 0 | 0.0 |
| 49 | Al-Ḥujurāt | 347 | 165 | 180 | 1 | 1 | 0 | 2.9 |
| 50 | Qāf | 373 | 236 | 135 | 2 | 0 | 0 | 0.0 |
| 51 | Adh-Dhāriyāt | 360 | 187 | 173 | 0 | 0 | 0 | 0.0 |
| 52 | Aṭ-Ṭūr | 312 | 177 | 132 | 0 | 3 | 0 | 9.6 |
| 53 | An-Najm | 360 | 173 | 187 | 0 | 0 | 0 | 0.0 |
| 54 | Al-Qamar | 342 | 190 | 151 | 0 | 1 | 0 | 2.9 |
| 55 | Ar-Raḥmān | 351 | 240 | 109 | 0 | 2 | 0 | 5.7 |
| 56 | Al-Wāqi‘ah | 379 | 212 | 167 | 0 | 0 | 0 | 0.0 |
| 57 | Al-Ḥadīd | 574 | 273 | 298 | 0 | 2 | 1 | 5.2 |
| 58 | Al-Mujādilah | 472 | 243 | 225 | 0 | 4 | 0 | 8.5 |
| 59 | Al-Ḥashr | 445 | 203 | 240 | 0 | 2 | 0 | 4.5 |
| 60 | Al-Mumtaḥanah | 348 | 158 | 190 | 0 | 0 | 0 | 0.0 |
| 61 | Aṣ-Ṣaff | 221 | 110 | 109 | 0 | 2 | 0 | 9.0 |
| 62 | Al-Jumu‘ah | 175 | 79 | 96 | 0 | 0 | 0 | 0.0 |
| 63 | Al-Munāfiqūn | 180 | 87 | 92 | 1 | 0 | 0 | 0.0 |
| 64 | At-Taghābun | 241 | 116 | 122 | 2 | 1 | 0 | 4.1 |
| 65 | Aṭ-Ṭalāq | 287 | 153 | 131 | 1 | 2 | 0 | 7.0 |
| 66 | At-Taḥrīm | 249 | 126 | 122 | 0 | 1 | 0 | 4.0 |
| 67 | Al-Mulk | 333 | 160 | 173 | 0 | 0 | 0 | 0.0 |
| 68 | Al-Qalam | 300 | 190 | 110 | 0 | 0 | 0 | 0.0 |
| 69 | Al-Ḥāqqah | 258 | 153 | 103 | 2 | 0 | 0 | 0.0 |
| 70 | Al-Ma‘ārij | 217 | 109 | 106 | 0 | 2 | 0 | 9.2 |
| 71 | Nūḥ | 226 | 107 | 118 | 0 | 1 | 0 | 4.4 |
| 72 | Al-Jinn | 286 | 138 | 144 | 1 | 2 | 1 | 10.5 |
| 73 | Al-Muzzammil | 199 | 99 | 98 | 0 | 1 | 1 | 10.1 |
| 74 | Al-Muddaththir | 255 | 146 | 106 | 1 | 2 | 0 | 7.8 |
| 75 | Al-Qiyāmah | 164 | 87 | 72 | 3 | 0 | 2 | 12.2 |
| 76 | Al-Insān | 243 | 123 | 119 | 1 | 0 | 0 | 0.0 |
| 77 | Al-Mursalāt | 181 | 107 | 73 | 0 | 1 | 0 | 5.5 |
| 78 | An-Naba’ | 173 | 87 | 86 | 0 | 0 | 0 | 0.0 |
| 79 | An-Nāzi‘āt | 179 | 90 | 88 | 0 | 1 | 0 | 5.6 |
| 80 | ‘Abasa | 133 | 73 | 60 | 0 | 0 | 0 | 0.0 |
| 81 | At-Takwīr | 104 | 60 | 43 | 0 | 1 | 0 | 9.6 |
| 82 | Al-Infiṭār | 80 | 47 | 33 | 0 | 0 | 0 | 0.0 |
| 83 | Al-Muṭaffifīn | 169 | 94 | 74 | 0 | 1 | 0 | 5.9 |
| 84 | Al-Inshiqāq | 107 | 65 | 42 | 0 | 0 | 0 | 0.0 |
| 85 | Al-Burūj | 109 | 53 | 56 | 0 | 0 | 0 | 0.0 |
| 86 | Aṭ-Ṭāriq | 61 | 35 | 26 | 0 | 0 | 0 | 0.0 |
| 87 | Al-A‘lā | 72 | 36 | 35 | 1 | 0 | 0 | 0.0 |
| 88 | Al-Ghāshiyah | 92 | 54 | 37 | 1 | 0 | 0 | 0.0 |
| 89 | Al-Fajr | 137 | 69 | 63 | 3 | 2 | 0 | 14.6 |
| 90 | Al-Balad | 82 | 48 | 33 | 0 | 1 | 0 | 12.2 |
| 91 | Ash-Shams | 54 | 20 | 33 | 0 | 1 | 0 | 18.5 |
| 92 | Al-Lail | 71 | 33 | 38 | 0 | 0 | 0 | 0.0 |
| 93 | Aḍ-Ḍuḥā | 40 | 23 | 17 | 0 | 0 | 0 | 0.0 |
| 94 | Ash-Sharḥ | 27 | 21 | 6 | 0 | 0 | 0 | 0.0 |
| 95 | At-Tīn | 34 | 22 | 12 | 0 | 0 | 0 | 0.0 |
| 96 | Al-‘Alaq | 72 | 41 | 31 | 0 | 0 | 0 | 0.0 |
| 97 | Al-Qadr | 30 | 14 | 16 | 0 | 0 | 0 | 0.0 |
| 98 | Al-Bayyinah | 94 | 50 | 44 | 0 | 0 | 0 | 0.0 |
| 99 | Az-Zalzalah | 36 | 22 | 14 | 0 | 0 | 0 | 0.0 |
| 100 | Al-‘Ādiyāt | 40 | 23 | 17 | 0 | 0 | 0 | 0.0 |
| 101 | Al-Qāri‘ah | 36 | 19 | 17 | 0 | 0 | 0 | 0.0 |
| 102 | At-Takāthur | 28 | 21 | 7 | 0 | 0 | 0 | 0.0 |
| 103 | Al-‘Aṣr | 14 | 10 | 4 | 0 | 0 | 0 | 0.0 |
| 104 | Al-Humazah | 33 | 14 | 19 | 0 | 0 | 0 | 0.0 |
| 105 | Al-Fīl | 23 | 14 | 9 | 0 | 0 | 0 | 0.0 |
| 106 | Quraish | 17 | 5 | 11 | 0 | 1 | 0 | 58.8 |
| 107 | Al-Mā‘ūn | 25 | 11 | 14 | 0 | 0 | 0 | 0.0 |
| 108 | Al-Kauthar | 10 | 6 | 4 | 0 | 0 | 0 | 0.0 |
| 109 | Al-Kāfirūn | 26 | 10 | 16 | 0 | 0 | 0 | 0.0 |
| 110 | An-Naṣr | 19 | 12 | 7 | 0 | 0 | 0 | 0.0 |
| 111 | Al-Masad | 23 | 12 | 11 | 0 | 0 | 0 | 0.0 |
| 112 | Al-Ikhlāṣ | 15 | 10 | 5 | 0 | 0 | 0 | 0.0 |
| 113 | Al-Falaq | 23 | 19 | 4 | 0 | 0 | 0 | 0.0 |
| 114 | An-Nās | 20 | 10 | 10 | 0 | 0 | 0 | 0.0 |
