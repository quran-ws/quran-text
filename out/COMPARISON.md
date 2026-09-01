# Cross-riwāyah comparison

Generated 2026-09-01 from the KFGQPC packages in `data/`. 77,434 canonical words across 114 sūrahs and 7 riwāyāt.

Every word carries one ID that means the same word in every riwāyah that has it. Where the riwāyāt disagree, the disagreement is recorded against that ID rather than hidden by it.

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

The āyah totals are not errors: the riwāyāt follow different counting traditions (Kūfī 6236, Madanī 6214, Baṣrī 6217, and the Makkī count KFGQPC uses for Bazzī, 6220). This is exactly why the index is flat — the riwāyāt disagree about where āyāt end far more than about words.

## What the words look like across riwāyāt

| status | words | share | meaning |
|---|---|---|---|
| identical | 32,704 | 42.23% | same reading and same spelling in all seven |
| diacritic_variant | 43,745 | 56.49% | same consonantal skeleton, different vowelling or marks |
| rasm_variant | 968 | 1.25% | the riwāyāt disagree about the letters themselves |
| word_boundary | 12 | 0.02% | at least one source prints the word joined to its neighbour |
| partial | 5 | 0.01% | the word is absent from at least one riwāyah |

`identical` compares after folding release notation — the 2022 and 2026 packages spell the same sukūn and tanwīn with different codepoints (`U+06E1`/`U+0652`, `U+0657`/`U+08F1`), which is a typographic difference, not a textual one. The raw spelling of each riwāyah is always kept in `forms`.

## Pairwise agreement

Share of shared words where two riwāyāt agree, at three levels: exact stored spelling, the same reading once notation is folded, and the consonantal skeleton.

| pair | shared words | same spelling | same reading | same rasm |
|---|---|---|---|---|
| douri–sousi | 77,431 | 66.7% | 69.0% | 99.99% |
| hafs–shuba | 77,432 | 99.2% | 99.2% | 99.87% |
| douri–bazzi | 77,430 | 57.8% | 60.2% | 99.75% |
| sousi–bazzi | 77,430 | 66.6% | 66.6% | 99.74% |
| shuba–douri | 77,430 | 70.9% | 73.2% | 99.74% |
| shuba–sousi | 77,430 | 72.1% | 72.1% | 99.73% |
| warsh–qaloun | 77,431 | 74.4% | 74.4% | 99.69% |
| hafs–douri | 77,430 | 70.8% | 73.1% | 99.69% |
| hafs–sousi | 77,430 | 72.0% | 72.0% | 99.68% |
| shuba–bazzi | 77,431 | 84.1% | 84.1% | 99.61% |
| hafs–bazzi | 77,431 | 84.0% | 84.0% | 99.60% |
| qaloun–douri | 77,430 | 36.8% | 64.4% | 99.34% |
| qaloun–sousi | 77,430 | 42.6% | 70.0% | 99.33% |
| qaloun–bazzi | 77,430 | 41.5% | 61.2% | 99.30% |
| shuba–qaloun | 77,430 | 40.5% | 67.2% | 99.28% |
| hafs–qaloun | 77,430 | 40.4% | 67.2% | 99.27% |
| shuba–warsh | 77,430 | 38.1% | 57.5% | 99.12% |
| hafs–warsh | 77,430 | 38.1% | 57.6% | 99.11% |
| warsh–douri | 77,430 | 35.6% | 55.4% | 99.06% |
| warsh–sousi | 77,430 | 35.6% | 54.8% | 99.05% |
| warsh–bazzi | 77,430 | 34.1% | 47.8% | 99.03% |

Rasm agreement never drops below 98%: the seven riwāyāt are one text. Spelling agreement is far lower because the packages were typeset in different years with different conventions.

## Rasm variants

968 words where the riwāyāt disagree about the letters. The full list is in [`rasm-variants.md`](rasm-variants.md) and [`conflicts.csv`](conflicts.csv); a sample follows.

| word id | sūrah:āyah | rasm | forms |
|---|---|---|---|
| 176 | 2:15 | يستهزي | **يَسۡتَهۡزِئُ** hafs,shuba,douri,sousi,bazzi  ·  **يَسْتَهْزِۓُ** warsh,qaloun |
| 425 | 2:28 | فاحيكم | **فَأَحۡيَٰكُمۡ** hafs,shuba,douri,sousi  ·  **فَأَحْيٜاكُمْ** warsh  ·  **فَأَحْيَاكُمْ** qaloun  ·  **فَأَحۡيَٰكُمُۥ** bazzi |
| 491 | 2:31 | هولا | **هَٰٓؤُلَآءِ** hafs,shuba,warsh  ·  **هَٰؤُلَآࢇ** qaloun,bazzi  ·  **هَٰٓؤُلَآ** douri  ·  **هَٰؤُلَا** sousi |
| 618 | 2:40 | اسرءيل | **إِسۡرَٰٓءِيلَ** hafs,shuba,douri,sousi,bazzi  ·  **إِسْرَآءِيلَ** warsh,qaloun |
| 690 | 2:47 | اسرءيل | **إِسۡرَٰٓءِيلَ** hafs,shuba,douri,sousi,bazzi  ·  **إِسْرَآءِيلَ** warsh,qaloun |
| 709 | 2:48 | يقبل | **يُقۡبَلُ** hafs,shuba  ·  **يُقْبَلُ** warsh,qaloun  ·  **تُقۡبَلُ** douri,sousi,bazzi |
| 722 | 2:49 | ءال | **ءَالِ** hafs,shuba,qaloun,douri,sousi,bazzi  ·  **اٰلِ** warsh |
| 768 | 2:53 | ءاتينا | **ءَاتَيۡنَا** hafs,shuba,douri,sousi,bazzi  ·  **اٰتَيْنَا** warsh  ·  **ءَاتَيْنَا** qaloun |
| 823 | 2:57 | الغمام | **ٱلۡغَمَامَ** hafs,shuba,bazzi  ·  **ࡲ۬لْغَمَٰمَ** warsh,qaloun  ·  **اُ۬لۡغَمَامَ** douri  ·  **ࡲ۬لۡغَمَامَ** sousi |
| 854 | 2:58 | نغفر | **نَّغۡفِرۡ** hafs,shuba,bazzi  ·  **يُغْفَرْ** warsh,qaloun  ·  **نَّغۡفِر** douri,sousi |
| 956 | 2:61 | النبين | **ٱلنَّبِيِّۧنَ** hafs,shuba,bazzi  ·  **ࡰ۬لنَّبِيِٕٓۑنَ** warsh,qaloun  ·  **اَ۬لنَّبِيِّۧنَ** douri  ·  **ࡱ۬لنَّبِيِّۧنَ** sousi |
| 972 | 2:62 | ءامن | **ءَامَنَ** hafs,shuba,qaloun,douri,sousi,bazzi  ·  **اٰمَنَ** warsh |
| 1132 | 2:71 | الن | **ٱلَٰۡٔنَ** hafs,shuba,bazzi  ·  **ࡲ۬لَٰنَ** warsh  ·  **ࡲ۬ءَلْٰنَ** qaloun  ·  **اُ۬لَٰۡٔنَ** douri  ·  **ࡲ۬لَٰۡٔنَ** sousi |
| 1142 | 2:72 | فادرءتم | **فَٱدَّٰرَٰءۡتُمۡ** hafs,shuba  ·  **فَادَّٰرْٔتُمْ** warsh  ·  **فَادَّٰرَٰءْتُمْ** qaloun  ·  **فَاَدَّٰرَٰءۡتُمۡ** douri  ·  **فَاَدَّٰرَٰتُمۡ** sousi  ·  **فَٱدَّٰرَٰءۡتُمُۥ** bazzi |
| 1196 | 2:74 | تعملون | **تَعۡمَلُونَ** hafs,shuba,douri,sousi  ·  **تَعْمَلُونَ࣌** warsh  ·  **تَعْمَلُونَ** qaloun  ·  **يَعۡمَلُونَ** bazzi |
| 1333 | 2:83 | اسرءيل | **إِسۡرَٰٓءِيلَ** hafs,shuba,douri,bazzi  ·  **إِسْرَآءِيلَ** warsh,qaloun  ·  **إِسۡرَٰٓءِيل** sousi |
| 1335 | 2:83 | تعبدون | **تَعۡبُدُونَ** hafs,shuba,douri,sousi  ·  **تَعْبُدُونَ** warsh,qaloun  ·  **يَعۡبُدُونَ** bazzi |
| 1339 | 2:83 | احسانا | **إِحۡسَانࣰا** hafs,shuba,sousi,bazzi  ·  **إِحْسَٰناࣰ** warsh,qaloun  ·  **إِحۡسَانٗا** douri |
| 1421 | 2:85 | يعملون | **تَعۡمَلُونَ** hafs,douri,sousi  ·  **يَعۡمَلُونَ** shuba,bazzi  ·  **يَعْمَلُونَ࣌** warsh  ·  **يَعْمَلُونَ** qaloun |
| 1436 | 2:87 | ءاتينا | **ءَاتَيۡنَا** hafs,shuba,douri,sousi,bazzi  ·  **اٰتَيْنَا** warsh  ·  **ءَاتَيْنَا** qaloun |
| 1738 | 2:102 | هروت | **هَٰرُوتَ** hafs,shuba,douri,sousi,bazzi  ·  **هَارُوتَ** warsh,qaloun |
| 1739 | 2:102 | ومروت | **وَمَٰرُوتَ** hafs,shuba,douri,sousi,bazzi  ·  **وَمَارُوتَ࣌** warsh  ·  **وَمَارُوتَ** qaloun |
| 1741 | 2:102 | يعلمان | **يُعَلِّمَانِ** hafs,shuba,douri,sousi,bazzi  ·  **يُعَلِّمَٰنِ** warsh,qaloun |
| 1843 | 2:106 | ءايه | **ءَايَةٍ** hafs,shuba,qaloun,douri,sousi,bazzi  ·  **اٰيَةٍ** warsh |
| 2147 | 2:121 | تلاوته | **تِلَاوَتِهِۦٓ** hafs,shuba,douri  ·  **تِلَٰوَتِهِۦٓ** warsh  ·  **تِلَٰوَتِهِۦ** qaloun  ·  **تِلَاوَتِهِۦ** sousi,bazzi |

## Word-boundary disagreements

One source prints as a single word what the others print as two. Some are the source's own orthography (Bazzī's `لَأُاْقۡسِمُ`, the traditional `مَالِ`), and some are dropped spaces — Dūrī's `كَانُواْيَعۡمَلُونَ` at 11:77 is written with the space in that riwāyah's own 2022 release. Both are re-segmented so the index keeps one column per word, and both are recorded here rather than judged.

| word id | sūrah:āyah | rasm | absent from | forms |
|---|---|---|---|---|
| 11634 | 4:91 | ما | — | **مَا** hafs,shuba,warsh,qaloun,douri,sousi,bazzi |
| 11635 | 4:91 | ردوا | — | **رُدُّوٓاْ** hafs,shuba,warsh,douri  ·  **رُدُّواْ** qaloun,sousi,bazzi |
| 26811 | 10:26 | قتر | — | **قَتَرࣱ** hafs,shuba,warsh,qaloun,sousi,bazzi  ·  **قَتَرٞ** douri |
| 26812 | 10:26 | ولا | — | **وَلَا** hafs,shuba,warsh,qaloun,douri,sousi,bazzi |
| 29368 | 11:78 | كانوا | — | **كَانُواْ** hafs,shuba,warsh,qaloun,douri,sousi,bazzi |
| 29369 | 11:78 | يعملون | — | **يَعۡمَلُونَ** hafs,shuba,douri,sousi,bazzi  ·  **يَعْمَلُونَ** warsh,qaloun |
| 48679 | 27:20 | ما | — | **مَا** hafs,shuba,warsh,qaloun,douri,sousi,bazzi |
| 48680 | 27:20 | لي | — | **لِيَ** hafs,shuba,bazzi  ·  **لِے** warsh,qaloun  ·  **لِي** douri,sousi |
| 56845 | 36:22 | وما | — | **وَمَا** hafs,shuba,warsh,qaloun,douri,sousi,bazzi |
| 56846 | 36:22 | لي | — | **لِيَ** hafs,shuba,warsh,qaloun,douri,sousi,bazzi |
| 74539 | 75:1 | لا | — | **لَآ** hafs,shuba,warsh,douri  ·  **لَا** qaloun,sousi  ·  **لَأُ** bazzi |
| 74540 | 75:1 | اقسم | — | **أُقۡسِمُ** hafs,shuba,douri  ·  **أُقْسِمُ** warsh,qaloun  ·  **أُقۡسِم** sousi  ·  **اْقۡسِمُ** bazzi |

## Words absent from some riwāyāt

Genuine textual differences, each well attested.

| word id | sūrah:āyah | rasm | absent from | forms |
|---|---|---|---|---|
| 25685 | 9:101 | من | hafs, shuba, warsh, qaloun, douri, sousi | **مِن** bazzi |
| 60523 | 40:26 | ان | warsh, qaloun, douri, sousi, bazzi | **أَن** hafs,shuba |
| 69720 | 57:24 | هو | warsh, qaloun | **هُوَ** hafs,shuba,douri,bazzi  ·  **هُّوَ** sousi |
| 73951 | 72:16 | لو | hafs, shuba, bazzi | **لَّوِ** warsh,qaloun,douri,sousi |
| 74227 | 73:20 | لن | douri, sousi | **لَّن** hafs,shuba,warsh,qaloun,bazzi |

## Source integrity

Six riwāyāt ship two releases. Comparing them is the sharpest available check on each, since the publisher is the same.

| riwāyah | āyāt compared | byte-identical | notation only | marks/vowels only | rasm differs |
|---|---|---|---|---|---|
| hafs | 6,236 | 2,715 | 663 | 2,856 | 2 |
| shuba | 6,236 | 2,715 | 662 | 2,857 | 2 |
| warsh | 6,214 | 160 | 73 | 5,949 | 32 |
| qaloun | 6,214 | 733 | 250 | 5,199 | 32 |
| douri | 6,217 | 6,214 | 0 | 0 | 3 |
| sousi | 6,217 | 508 | 195 | 5,490 | 24 |

The `marks/vowels only` column is dominated by the 2026 files adopting the Arabic Extended-B alif letters (`U+0870`–`U+0879`), which fold an alif and its vowel into one codepoint where the 2022 files used an alif plus combining marks. The rasm is untouched, so none of it reaches the word index.

### Checks

| check | riwāyah | detail |
|---|---|---|
| counting_total | sousi | the basri tradition totals 6217 āyāt; this release has 6218 |

## Per sūrah

| sūrah | name | words | identical | diacritic | rasm | boundary/absent | variants per 1000 |
|---|---|---|---|---|---|---|---|
| 1 | Al-Fātiḥah | 29 | 10 | 19 | 0 | 0 | 0.0 |
| 2 | Al-Baqarah | 6,117 | 2607 | 3431 | 79 | 0 | 12.9 |
| 3 | Āl-‘Imrān | 3,481 | 1448 | 1986 | 47 | 0 | 13.5 |
| 4 | An-Nisā’ | 3,747 | 1501 | 2217 | 27 | 2 | 7.7 |
| 5 | Al-Mā’idah | 2,804 | 1124 | 1649 | 31 | 0 | 11.1 |
| 6 | Al-An‘ām | 3,050 | 1294 | 1717 | 39 | 0 | 12.8 |
| 7 | Al-A‘rāf | 3,320 | 1432 | 1850 | 38 | 0 | 11.4 |
| 8 | Al-Anfāl | 1,234 | 497 | 724 | 13 | 0 | 10.5 |
| 9 | At-Taubah | 2,499 | 975 | 1506 | 17 | 1 | 7.2 |
| 10 | Yūnus | 1,833 | 797 | 1015 | 19 | 2 | 11.5 |
| 11 | Hūd | 1,917 | 858 | 1037 | 20 | 2 | 11.5 |
| 12 | Yūsuf | 1,777 | 774 | 978 | 25 | 0 | 14.1 |
| 13 | Ar-Ra‘d | 854 | 368 | 475 | 11 | 0 | 12.9 |
| 14 | Ibrāhīm | 830 | 351 | 477 | 2 | 0 | 2.4 |
| 15 | Al-Ḥijr | 654 | 316 | 326 | 12 | 0 | 18.3 |
| 16 | An-Naḥl | 1,844 | 756 | 1075 | 13 | 0 | 7.0 |
| 17 | Al-Isrā’ | 1,556 | 676 | 840 | 40 | 0 | 25.7 |
| 18 | Al-Kahf | 1,579 | 675 | 885 | 19 | 0 | 12.0 |
| 19 | Maryam | 961 | 402 | 547 | 12 | 0 | 12.5 |
| 20 | Ṭā-Hā | 1,335 | 607 | 710 | 18 | 0 | 13.5 |
| 21 | Al-Anbiyā’ | 1,169 | 489 | 661 | 19 | 0 | 16.3 |
| 22 | Al-Ḥajj | 1,274 | 540 | 724 | 10 | 0 | 7.8 |
| 23 | Al-Mu’minūn | 1,050 | 443 | 590 | 17 | 0 | 16.2 |
| 24 | An-Nūr | 1,316 | 517 | 793 | 6 | 0 | 4.6 |
| 25 | Al-Furqān | 893 | 375 | 500 | 18 | 0 | 20.2 |
| 26 | Ash-Shu‘arā’ | 1,318 | 583 | 722 | 13 | 0 | 9.9 |
| 27 | An-Naml | 1,151 | 499 | 623 | 27 | 2 | 25.2 |
| 28 | Al-Qaṣaṣ | 1,430 | 647 | 761 | 22 | 0 | 15.4 |
| 29 | Al-‘Ankabūt | 976 | 391 | 572 | 13 | 0 | 13.3 |
| 30 | Ar-Rūm | 817 | 336 | 465 | 16 | 0 | 19.6 |
| 31 | Luqmān | 546 | 225 | 317 | 4 | 0 | 7.3 |
| 32 | As-Sajdah | 372 | 163 | 204 | 5 | 0 | 13.4 |
| 33 | Al-Aḥzāb | 1,287 | 507 | 752 | 28 | 0 | 21.8 |
| 34 | Saba’ | 883 | 387 | 484 | 12 | 0 | 13.6 |
| 35 | Fāṭir | 775 | 327 | 440 | 8 | 0 | 10.3 |
| 36 | Yā-Sīn | 725 | 279 | 437 | 7 | 2 | 12.4 |
| 37 | Aṣ-Ṣāffāt | 861 | 389 | 460 | 12 | 0 | 13.9 |
| 38 | Ṣād | 733 | 337 | 390 | 6 | 0 | 8.2 |
| 39 | Az-Zumar | 1,172 | 491 | 673 | 8 | 0 | 6.8 |
| 40 | Ghāfir | 1,219 | 513 | 690 | 15 | 1 | 13.1 |
| 41 | Fuṣṣilat | 794 | 325 | 458 | 11 | 0 | 13.9 |
| 42 | Ash-Shūra | 860 | 331 | 520 | 9 | 0 | 10.5 |
| 43 | Az-Zukhruf | 830 | 340 | 476 | 14 | 0 | 16.9 |
| 44 | Ad-Dukhān | 346 | 151 | 191 | 4 | 0 | 11.6 |
| 45 | Al-Jāthiyah | 488 | 217 | 263 | 8 | 0 | 16.4 |
| 46 | Al-Aḥqāf | 643 | 271 | 355 | 17 | 0 | 26.4 |
| 47 | Muḥammad | 539 | 222 | 311 | 6 | 0 | 11.1 |
| 48 | Al-Fatḥ | 560 | 213 | 338 | 9 | 0 | 16.1 |
| 49 | Al-Ḥujurāt | 347 | 135 | 209 | 3 | 0 | 8.6 |
| 50 | Qāf | 373 | 193 | 172 | 8 | 0 | 21.4 |
| 51 | Adh-Dhāriyāt | 360 | 137 | 221 | 2 | 0 | 5.6 |
| 52 | Aṭ-Ṭūr | 312 | 143 | 168 | 1 | 0 | 3.2 |
| 53 | An-Najm | 360 | 154 | 200 | 6 | 0 | 16.7 |
| 54 | Al-Qamar | 342 | 142 | 191 | 9 | 0 | 26.3 |
| 55 | Ar-Raḥmān | 351 | 198 | 136 | 17 | 0 | 48.4 |
| 56 | Al-Wāqi‘ah | 379 | 179 | 191 | 9 | 0 | 23.7 |
| 57 | Al-Ḥadīd | 574 | 226 | 343 | 4 | 1 | 8.7 |
| 58 | Al-Mujādilah | 472 | 197 | 273 | 2 | 0 | 4.2 |
| 59 | Al-Ḥashr | 445 | 162 | 278 | 5 | 0 | 11.2 |
| 60 | Al-Mumtaḥanah | 348 | 132 | 215 | 1 | 0 | 2.9 |
| 61 | Aṣ-Ṣaff | 221 | 91 | 125 | 5 | 0 | 22.6 |
| 62 | Al-Jumu‘ah | 175 | 65 | 109 | 1 | 0 | 5.7 |
| 63 | Al-Munāfiqūn | 180 | 77 | 101 | 2 | 0 | 11.1 |
| 64 | At-Taghābun | 241 | 93 | 146 | 2 | 0 | 8.3 |
| 65 | Aṭ-Ṭalāq | 287 | 121 | 162 | 4 | 0 | 13.9 |
| 66 | At-Taḥrīm | 249 | 108 | 134 | 7 | 0 | 28.1 |
| 67 | Al-Mulk | 333 | 119 | 212 | 2 | 0 | 6.0 |
| 68 | Al-Qalam | 300 | 156 | 141 | 3 | 0 | 10.0 |
| 69 | Al-Ḥāqqah | 258 | 117 | 139 | 2 | 0 | 7.8 |
| 70 | Al-Ma‘ārij | 217 | 88 | 129 | 0 | 0 | 0.0 |
| 71 | Nūḥ | 226 | 91 | 134 | 1 | 0 | 4.4 |
| 72 | Al-Jinn | 286 | 117 | 164 | 4 | 1 | 17.5 |
| 73 | Al-Muzzammil | 199 | 70 | 124 | 4 | 1 | 25.1 |
| 74 | Al-Muddaththir | 255 | 124 | 128 | 3 | 0 | 11.8 |
| 75 | Al-Qiyāmah | 164 | 75 | 81 | 6 | 2 | 48.8 |
| 76 | Al-Insān | 243 | 92 | 149 | 2 | 0 | 8.2 |
| 77 | Al-Mursalāt | 181 | 77 | 104 | 0 | 0 | 0.0 |
| 78 | An-Naba’ | 173 | 70 | 101 | 2 | 0 | 11.6 |
| 79 | An-Nāzi‘āt | 179 | 81 | 96 | 2 | 0 | 11.2 |
| 80 | ‘Abasa | 133 | 61 | 71 | 1 | 0 | 7.5 |
| 81 | At-Takwīr | 104 | 53 | 49 | 2 | 0 | 19.2 |
| 82 | Al-Infiṭār | 80 | 40 | 40 | 0 | 0 | 0.0 |
| 83 | Al-Muṭaffifīn | 169 | 82 | 87 | 0 | 0 | 0.0 |
| 84 | Al-Inshiqāq | 107 | 50 | 55 | 2 | 0 | 18.7 |
| 85 | Al-Burūj | 109 | 41 | 66 | 2 | 0 | 18.3 |
| 86 | Aṭ-Ṭāriq | 61 | 32 | 29 | 0 | 0 | 0.0 |
| 87 | Al-A‘lā | 72 | 33 | 38 | 1 | 0 | 13.9 |
| 88 | Al-Ghāshiyah | 92 | 44 | 46 | 2 | 0 | 21.7 |
| 89 | Al-Fajr | 137 | 52 | 80 | 5 | 0 | 36.5 |
| 90 | Al-Balad | 82 | 37 | 44 | 1 | 0 | 12.2 |
| 91 | Ash-Shams | 54 | 19 | 33 | 2 | 0 | 37.0 |
| 92 | Al-Lail | 71 | 32 | 39 | 0 | 0 | 0.0 |
| 93 | Aḍ-Ḍuḥā | 40 | 21 | 19 | 0 | 0 | 0.0 |
| 94 | Ash-Sharḥ | 27 | 17 | 10 | 0 | 0 | 0.0 |
| 95 | At-Tīn | 34 | 20 | 14 | 0 | 0 | 0.0 |
| 96 | Al-‘Alaq | 72 | 31 | 38 | 3 | 0 | 41.7 |
| 97 | Al-Qadr | 30 | 10 | 20 | 0 | 0 | 0.0 |
| 98 | Al-Bayyinah | 94 | 46 | 48 | 0 | 0 | 0.0 |
| 99 | Az-Zalzalah | 36 | 19 | 17 | 0 | 0 | 0.0 |
| 100 | Al-‘Ādiyāt | 40 | 18 | 22 | 0 | 0 | 0.0 |
| 101 | Al-Qāri‘ah | 36 | 16 | 20 | 0 | 0 | 0.0 |
| 102 | At-Takāthur | 28 | 20 | 8 | 0 | 0 | 0.0 |
| 103 | Al-‘Aṣr | 14 | 6 | 8 | 0 | 0 | 0.0 |
| 104 | Al-Humazah | 33 | 11 | 22 | 0 | 0 | 0.0 |
| 105 | Al-Fīl | 23 | 10 | 13 | 0 | 0 | 0.0 |
| 106 | Quraish | 17 | 5 | 11 | 1 | 0 | 58.8 |
| 107 | Al-Mā‘ūn | 25 | 11 | 13 | 1 | 0 | 40.0 |
| 108 | Al-Kauthar | 10 | 5 | 5 | 0 | 0 | 0.0 |
| 109 | Al-Kāfirūn | 26 | 7 | 19 | 0 | 0 | 0.0 |
| 110 | An-Naṣr | 19 | 11 | 8 | 0 | 0 | 0.0 |
| 111 | Al-Masad | 23 | 8 | 15 | 0 | 0 | 0.0 |
| 112 | Al-Ikhlāṣ | 15 | 8 | 7 | 0 | 0 | 0.0 |
| 113 | Al-Falaq | 23 | 14 | 9 | 0 | 0 | 0.0 |
| 114 | An-Nās | 20 | 8 | 12 | 0 | 0 | 0.0 |
