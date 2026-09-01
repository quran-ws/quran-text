# Cross-riwāyah comparison

Generated 2026-09-01 from the KFGQPC packages in `data/`. 77,434 canonical words across 114 sūrahs and 7 riwāyāt.

Every word carries one ID that means the same word in every riwāyah that has it. Where the riwāyāt disagree, the disagreement is recorded against that ID rather than hidden by it.

## What is being compared

A word is never compared as raw text. Four forms are derived from every spelling, each stripping one more layer of what a scribe added after the codices were written. Two riwāyāt are said to agree *at a level* when their forms at that level are identical.

| form | question it answers | example | and what it drops |
|---|---|---|---|
| `uthmani` | how is it printed? | `ٱلرَّحۡمَٰنِ` | — |
| `folded` | what does it say, ignoring which codepoints the release chose? | `الرَّحْمَٰنِ` | release notation, attached-alef letters, editorial marks |
| `pointed` | which letters, dots and all? | `الرحمان` | vowels, hamza, madd, ṣilah |
| `rasm` | what is on the line in the codex? | `الرحماں` | the dots |

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
| `diacritic_variant` | 36,261 | 46.83% | same letters and same dots — the vowelling differs |
| `dotting_variant` | 338 | 0.44% | one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ |
| `rasm_variant` | 260 | 0.34% | the codices disagree about the letters on the line |
| `word_boundary` | 12 | 0.02% | a source prints the word joined to its neighbour |
| `partial` | 5 | 0.01% | the word is absent from at least one riwāyah |

Each word gets the *strongest* label that applies, tested in this order: rasm, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed to share one rasm across all seven, and an `identical` word is identical after notation folding — the raw spelling of every riwāyah is always kept in `forms`, whatever the label.

## Pairwise agreement

Share of the words two riwāyāt both have, where they agree at each level.

| pair | shared words | same spelling | same reading | same letters | same rasm |
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

Rasm agreement never drops below 99.5%: the seven riwāyāt are one text. Spelling agreement is far lower because the packages were typeset in different years with different conventions — which is what the `folded` and `pointed` columns strip away.

## Where the riwāyāt genuinely disagree

Three things can differ once spelling, vowelling and pointing are set aside: the letters, the word boundaries, and whether a word is there at all. Together they account for 277 of 77,434 words — though 198 of the letter differences are a disagreement between the two typesettings rather than between the codices, and are picked out below.

| kind | count | status | what it means |
|---|---|---|---|
| letters differ | 260 | `rasm_variant` | a letter one codex has on the line and another does not — 198 of them an ā the two hands place differently |
| boundaries differ | 6 events | `word_boundary` | one source prints two words as one |
| word absent | 5 | `partial` | a riwāyah does not have the word at all |

### Letters — rasm disagreements

260 words where the riwāyāt disagree about the letters on the line, after dots, hamza, vowelling and the dagger alif have been set aside. The full list is in [`rasm-variants.md`](rasm-variants.md) and [`conflicts.csv`](conflicts.csv); the first 25 follow.

| word id | sūrah:āyah | rasm on each side | as printed |
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
| 2331 | 2:132 | `ووصى` hafs,shuba,bazzi,douri,sousi  ·  `واوصى` qaloun,warsh | **وَوَصَّىٰ** hafs,shuba,bazzi,douri,sousi  ·  **وَأَوْصَىٰ** qaloun  ·  **وَأَوْصٜىٰ** warsh |
| 2824 | 2:158 | `سعاٮر` hafs,shuba,bazzi,douri,sousi  ·  `سعٮر` qaloun,warsh | **شَعَآئِرِ** hafs,shuba,bazzi,douri,sousi  ·  **شَعَٰٓئِرِ** qaloun,warsh |
| 2991 | 2:166 | `الاسٮاٮ` hafs,shuba,bazzi,douri,sousi  ·  `الاسٮٮ` qaloun,warsh | **ٱلۡأَسۡبَابُ** hafs,shuba,bazzi  ·  **ࡲ۬لْأَسْبَٰبُ** qaloun  ·  **ࡲ۬لَاسْبَٰبُ** warsh  ·  **اِ۬لۡأَسۡبَابُ** douri  ·  **ࡵ۬لۡأَسۡبَابُ** sousi |
| 3929 | 2:210 | `العمام` hafs,shuba,bazzi,douri,sousi  ·  `العمم` qaloun,warsh | **ٱلۡغَمَامِ** hafs,shuba,bazzi  ·  **ࡰ۬لْغَمَٰمِ** qaloun,warsh  ·  **اَ۬لۡغَمَامِ** douri  ·  **ࡱ۬لۡغَمَامِ** sousi |
| 3939 | 2:211 | `اسرٮل` hafs,shuba,bazzi,douri,sousi  ·  `اسراٮل` qaloun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shuba,bazzi,douri,sousi  ·  **إِسْرَآءِيلَ** qaloun,warsh |
| 4209 | 2:220 | `اصلاح` hafs,shuba,bazzi,douri,sousi  ·  `اصلح` qaloun,warsh | **إِصۡلَاحࣱ** hafs,shuba,bazzi,sousi  ·  **إِصْلَٰحࣱ** qaloun  ·  **ࡴصْلَٰحࣱ** warsh  ·  **إِصۡلَاحٞ** douri |
| 4399 | 2:229 | `مرٮاں` hafs,shuba,bazzi,douri,sousi  ·  `مرٮں` qaloun,warsh | **مَرَّتَانِ** hafs,shuba,bazzi,douri,sousi  ·  **مَرَّتَٰنِ** qaloun,warsh |
| 4561 | 2:233 | `الرصاعه` hafs,shuba,bazzi,douri,sousi  ·  `الرصعه` qaloun,warsh | **ٱلرَّضَاعَةَ** hafs,shuba,bazzi  ·  **ࡰ۬لرَّضَٰعَةَ** qaloun,warsh  ·  **اَ۬لرَّضَاعَةَ** douri  ·  **ࡱ۬لرَّضَاعَةَ** sousi |
| 4827 | 2:243 | `احٮهم` hafs,shuba,bazzi,douri,sousi  ·  `احٮاهم` qaloun,warsh | **أَحۡيَٰهُمۡ** hafs,shuba,douri,sousi  ·  **أَحۡيَٰهُمُۥ** bazzi  ·  **أَحْيَاهُمْ** qaloun  ·  **أَحْيٜاهُمُۥٓ** warsh |
| 4870 | 2:246 | `اسرٮل` hafs,shuba,bazzi,douri,sousi  ·  `اسراٮل` qaloun,warsh | **إِسۡرَٰٓءِيلَ** hafs,shuba,bazzi,douri,sousi  ·  **إِسْرَآءِيلَ** qaloun,warsh |
| 5366 | 2:259 | `العطام` hafs,shuba,bazzi,douri,sousi  ·  `العطم` qaloun,warsh | **ٱلۡعِظَامِ** hafs,shuba,bazzi  ·  **ࡰ۬لْعِظَٰمِ** qaloun,warsh  ·  **اَ۬لۡعِظَامِ** douri  ·  **ࡱ۬لۡعِظَامِ** sousi |
| 5554 | 2:266 | `واعٮاٮ` hafs,shuba,bazzi,douri,sousi  ·  `واعٮٮ` qaloun,warsh | **وَأَعۡنَابࣲ** hafs,shuba,bazzi,sousi  ·  **وَأَعْنَٰبࣲ** qaloun,warsh  ·  **وَأَعۡنَابٖ** douri |
| 5738 | 2:274 | `وعلاٮٮه` hafs,shuba,bazzi,douri,sousi  ·  `وعلٮٮه` qaloun,warsh | **وَعَلَانِيَةࣰ** hafs,shuba,bazzi,sousi  ·  **وَعَلَٰنِيَةࣰ** qaloun,warsh  ·  **وَعَلَانِيَةٗ** douri |
| 5943 | 2:282 | `وامراٮاں` hafs,shuba,bazzi,douri,sousi  ·  `وامراٮں` qaloun,warsh | **وَٱمۡرَأَتَانِ** hafs,shuba,bazzi  ·  **وَامْرَأَتَٰنِ** qaloun,warsh  ·  **وَاَمۡرَأَتَانِ** douri  ·  **وَࡱمۡرَأَتَانِ** sousi |

### Of those, the ā on the line or above it

198 of the 260 are words whose skeletons differ only by an alef that one hand prints on the line and the other prints as a dagger above it. A written alef is part of the bare rasm whichever hand wrote it, so they are counted as rasm disagreements — but the two KFGQPC typesettings disagree in **both** directions, the Warsh/Qālūn set printing `هَارُوتَ` where the Kūfī set prints `هَٰرُوتَ` and `مُبَٰرَك` where it prints `مُبَارَك`, so how much of this is ḥadhf vs ithbāt al-alif in the codices and how much is the hand of the typesetter is a question these sources cannot answer. A sample:

| word id | sūrah:āyah | rasm on each side | as printed |
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

### Pointing — one rasm, two readings

338 words share a rasm but are pointed differently. These are real differences in reading, not in the codex: an undotted skeleton carries them all. A sample:

| word id | sūrah:āyah | shared rasm | pointed as |
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
| warsh | 6,214 | 160 | 410 | 5,635 | 9 |
| qaloun | 6,214 | 733 | 2,319 | 3,154 | 8 |
| douri | 6,217 | 6,214 | 0 | 0 | 3 |
| sousi | 6,217 | 508 | 1,916 | 3,768 | 25 |

`notation only` is dominated by the 2026 files adopting the Arabic Extended-B alif letters (`U+0870`–`U+0882`), which fold an alef and its vowel into one codepoint where the 2022 files used an alef plus combining marks. The `folded` form decomposes them again, so none of it reaches the word index.

### Checks

All checks pass.

## Per sūrah

| sūrah | name | words | identical | diacritic | dotting | rasm | boundary/absent | per 1000 |
|---|---|---|---|---|---|---|---|---|
| 1 | Al-Fātiḥah | 29 | 11 | 17 | 1 | 0 | 0 | 0.0 |
| 2 | Al-Baqarah | 6,117 | 3181 | 2890 | 21 | 25 | 0 | 4.1 |
| 3 | Āl-‘Imrān | 3,481 | 1767 | 1685 | 18 | 11 | 0 | 3.2 |
| 4 | An-Nisā’ | 3,747 | 1842 | 1876 | 19 | 8 | 2 | 2.7 |
| 5 | Al-Mā’idah | 2,804 | 1362 | 1418 | 3 | 21 | 0 | 7.5 |
| 6 | Al-An‘ām | 3,050 | 1645 | 1382 | 16 | 7 | 0 | 2.3 |
| 7 | Al-A‘rāf | 3,320 | 1779 | 1518 | 13 | 10 | 0 | 3.0 |
| 8 | Al-Anfāl | 1,234 | 592 | 632 | 6 | 4 | 0 | 3.2 |
| 9 | At-Taubah | 2,499 | 1207 | 1279 | 10 | 2 | 1 | 1.2 |
| 10 | Yūnus | 1,833 | 1011 | 809 | 7 | 4 | 2 | 3.3 |
| 11 | Hūd | 1,917 | 1091 | 817 | 4 | 3 | 2 | 2.6 |
| 12 | Yūsuf | 1,777 | 965 | 791 | 16 | 5 | 0 | 2.8 |
| 13 | Ar-Ra‘d | 854 | 454 | 394 | 4 | 2 | 0 | 2.3 |
| 14 | Ibrāhīm | 830 | 429 | 399 | 1 | 1 | 0 | 1.2 |
| 15 | Al-Ḥijr | 654 | 400 | 251 | 3 | 0 | 0 | 0.0 |
| 16 | An-Naḥl | 1,844 | 958 | 877 | 8 | 1 | 0 | 0.5 |
| 17 | Al-Isrā’ | 1,556 | 818 | 722 | 9 | 7 | 0 | 4.5 |
| 18 | Al-Kahf | 1,579 | 809 | 760 | 3 | 7 | 0 | 4.4 |
| 19 | Maryam | 961 | 485 | 471 | 2 | 3 | 0 | 3.1 |
| 20 | Ṭā-Hā | 1,335 | 717 | 603 | 7 | 8 | 0 | 6.0 |
| 21 | Al-Anbiyā’ | 1,169 | 644 | 513 | 6 | 6 | 0 | 5.1 |
| 22 | Al-Ḥajj | 1,274 | 657 | 608 | 6 | 3 | 0 | 2.4 |
| 23 | Al-Mu’minūn | 1,050 | 580 | 460 | 4 | 6 | 0 | 5.7 |
| 24 | An-Nūr | 1,316 | 639 | 669 | 8 | 0 | 0 | 0.0 |
| 25 | Al-Furqān | 893 | 456 | 426 | 6 | 5 | 0 | 5.6 |
| 26 | Ash-Shu‘arā’ | 1,318 | 733 | 577 | 2 | 6 | 0 | 4.6 |
| 27 | An-Naml | 1,151 | 639 | 495 | 10 | 5 | 2 | 6.1 |
| 28 | Al-Qaṣaṣ | 1,430 | 809 | 606 | 4 | 11 | 0 | 7.7 |
| 29 | Al-‘Ankabūt | 976 | 497 | 471 | 5 | 3 | 0 | 3.1 |
| 30 | Ar-Rūm | 817 | 421 | 388 | 6 | 2 | 0 | 2.4 |
| 31 | Luqmān | 546 | 293 | 250 | 2 | 1 | 0 | 1.8 |
| 32 | As-Sajdah | 372 | 208 | 163 | 0 | 1 | 0 | 2.7 |
| 33 | Al-Aḥzāb | 1,287 | 616 | 659 | 11 | 1 | 0 | 0.8 |
| 34 | Saba’ | 883 | 490 | 383 | 8 | 2 | 0 | 2.3 |
| 35 | Fāṭir | 775 | 421 | 348 | 3 | 3 | 0 | 3.9 |
| 36 | Yā-Sīn | 725 | 362 | 356 | 4 | 1 | 2 | 4.1 |
| 37 | Aṣ-Ṣāffāt | 861 | 484 | 375 | 0 | 2 | 0 | 2.3 |
| 38 | Ṣād | 733 | 422 | 308 | 2 | 1 | 0 | 1.4 |
| 39 | Az-Zumar | 1,172 | 625 | 541 | 3 | 3 | 0 | 2.6 |
| 40 | Ghāfir | 1,219 | 632 | 574 | 4 | 8 | 1 | 7.4 |
| 41 | Fuṣṣilat | 794 | 414 | 377 | 2 | 1 | 0 | 1.3 |
| 42 | Ash-Shūra | 860 | 430 | 424 | 5 | 1 | 0 | 1.2 |
| 43 | Az-Zukhruf | 830 | 447 | 373 | 6 | 4 | 0 | 4.8 |
| 44 | Ad-Dukhān | 346 | 198 | 146 | 1 | 1 | 0 | 2.9 |
| 45 | Al-Jāthiyah | 488 | 266 | 220 | 1 | 1 | 0 | 2.0 |
| 46 | Al-Aḥqāf | 643 | 344 | 290 | 5 | 4 | 0 | 6.2 |
| 47 | Muḥammad | 539 | 241 | 293 | 5 | 0 | 0 | 0.0 |
| 48 | Al-Fatḥ | 560 | 267 | 285 | 8 | 0 | 0 | 0.0 |
| 49 | Al-Ḥujurāt | 347 | 165 | 179 | 2 | 1 | 0 | 2.9 |
| 50 | Qāf | 373 | 236 | 133 | 2 | 2 | 0 | 5.4 |
| 51 | Adh-Dhāriyāt | 360 | 187 | 173 | 0 | 0 | 0 | 0.0 |
| 52 | Aṭ-Ṭūr | 312 | 177 | 132 | 3 | 0 | 0 | 0.0 |
| 53 | An-Najm | 360 | 173 | 186 | 0 | 1 | 0 | 2.8 |
| 54 | Al-Qamar | 342 | 190 | 150 | 1 | 1 | 0 | 2.9 |
| 55 | Ar-Raḥmān | 351 | 240 | 96 | 0 | 15 | 0 | 42.7 |
| 56 | Al-Wāqi‘ah | 379 | 212 | 166 | 0 | 1 | 0 | 2.6 |
| 57 | Al-Ḥadīd | 574 | 273 | 298 | 2 | 0 | 1 | 1.7 |
| 58 | Al-Mujādilah | 472 | 243 | 225 | 3 | 1 | 0 | 2.1 |
| 59 | Al-Ḥashr | 445 | 203 | 239 | 1 | 2 | 0 | 4.5 |
| 60 | Al-Mumtaḥanah | 348 | 158 | 190 | 0 | 0 | 0 | 0.0 |
| 61 | Aṣ-Ṣaff | 221 | 110 | 107 | 0 | 4 | 0 | 18.1 |
| 62 | Al-Jumu‘ah | 175 | 79 | 96 | 0 | 0 | 0 | 0.0 |
| 63 | Al-Munāfiqūn | 180 | 87 | 92 | 1 | 0 | 0 | 0.0 |
| 64 | At-Taghābun | 241 | 116 | 122 | 3 | 0 | 0 | 0.0 |
| 65 | Aṭ-Ṭalāq | 287 | 153 | 131 | 1 | 2 | 0 | 7.0 |
| 66 | At-Taḥrīm | 249 | 126 | 119 | 1 | 3 | 0 | 12.0 |
| 67 | Al-Mulk | 333 | 160 | 173 | 0 | 0 | 0 | 0.0 |
| 68 | Al-Qalam | 300 | 190 | 108 | 0 | 2 | 0 | 6.7 |
| 69 | Al-Ḥāqqah | 258 | 153 | 103 | 2 | 0 | 0 | 0.0 |
| 70 | Al-Ma‘ārij | 217 | 109 | 106 | 2 | 0 | 0 | 0.0 |
| 71 | Nūḥ | 226 | 107 | 118 | 1 | 0 | 0 | 0.0 |
| 72 | Al-Jinn | 286 | 138 | 144 | 1 | 2 | 1 | 10.5 |
| 73 | Al-Muzzammil | 199 | 99 | 98 | 0 | 1 | 1 | 10.1 |
| 74 | Al-Muddaththir | 255 | 146 | 106 | 1 | 2 | 0 | 7.8 |
| 75 | Al-Qiyāmah | 164 | 87 | 72 | 3 | 0 | 2 | 12.2 |
| 76 | Al-Insān | 243 | 123 | 119 | 1 | 0 | 0 | 0.0 |
| 77 | Al-Mursalāt | 181 | 107 | 73 | 1 | 0 | 0 | 0.0 |
| 78 | An-Naba’ | 173 | 87 | 84 | 0 | 2 | 0 | 11.6 |
| 79 | An-Nāzi‘āt | 179 | 90 | 88 | 1 | 0 | 0 | 0.0 |
| 80 | ‘Abasa | 133 | 73 | 60 | 0 | 0 | 0 | 0.0 |
| 81 | At-Takwīr | 104 | 60 | 42 | 0 | 2 | 0 | 19.2 |
| 82 | Al-Infiṭār | 80 | 47 | 33 | 0 | 0 | 0 | 0.0 |
| 83 | Al-Muṭaffifīn | 169 | 94 | 74 | 1 | 0 | 0 | 0.0 |
| 84 | Al-Inshiqāq | 107 | 65 | 42 | 0 | 0 | 0 | 0.0 |
| 85 | Al-Burūj | 109 | 53 | 56 | 0 | 0 | 0 | 0.0 |
| 86 | Aṭ-Ṭāriq | 61 | 35 | 26 | 0 | 0 | 0 | 0.0 |
| 87 | Al-A‘lā | 72 | 36 | 35 | 1 | 0 | 0 | 0.0 |
| 88 | Al-Ghāshiyah | 92 | 54 | 37 | 1 | 0 | 0 | 0.0 |
| 89 | Al-Fajr | 137 | 69 | 63 | 4 | 1 | 0 | 7.3 |
| 90 | Al-Balad | 82 | 48 | 33 | 0 | 1 | 0 | 12.2 |
| 91 | Ash-Shams | 54 | 20 | 32 | 0 | 2 | 0 | 37.0 |
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
