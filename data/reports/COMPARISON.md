# Cross-riwāyah comparison

Generated 2026-09-08 from the KFGQPC packages in `sources/`. 77,442 canonical words across 114 sūrahs and 16 riwāyāt.

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
| hisham | Hishām | هشام | Ibn ʿĀmir al-Shāmī | `dimashqi` | 6,226 | 77,433 |
| khalaf | Khalaf | خلف | Ḥamzah al-Kūfī | `kufi` | 6,236 | 77,434 |
| khallad | Khallād | خلاد | Ḥamzah al-Kūfī | `kufi` | 6,236 | 77,433 |
| abu-al-harith | Abū al-Ḥārith | أبو الحارث | al-Kisāʾī al-Kūfī | `kufi` | 6,236 | 77,435 |
| ibn-wardan | Ibn Wardān | ابن وردان | Abū Jaʿfar al-Madanī | `madani-first` | 6,214 | 77,410 |
| ibn-jammaz | Ibn Jammāz | ابن جماز | Abū Jaʿfar al-Madanī | `madani-first` | 6,214 | 77,410 |
| ruways | Ruways | رويس | Yaʿqūb al-Ḥaḍramī | `basri` | 6,204 | 77,384 |
| rawh | Rawḥ | روح | Yaʿqūb al-Ḥaḍramī | `basri` | 6,206 | 77,422 |
| ishaq | Isḥāq | إسحاق | Khalaf al-ʿĀshir | `kufi` | 6,236 | 77,434 |

The āyah totals are not errors and not deducible from the qāriʾ. Many fawāṣil are مختلف فيها, so every printed edition chooses, and the counting system above is **derived** from what this package prints, not assumed from the riwāyah. That is exactly why the index is flat, and why the āyah boundaries are read off each muṣḥaf: see [the fawāṣil](#fawāṣil-where-the-āyāt-end) below.

## How the words compare

| status | words | share | meaning |
|---|---|---|---|
| `identical` | 34,251 | 44.23% | one qiraah, one spelling, in every riwāyah |
| `diacritic_variant` | 40,996 | 52.94% | same letters and same dots — the vowelling differs |
| `dotting_variant` | 919 | 1.19% | one rasm, pointed differently: تَعۡمَلُونَ against يَعۡمَلُونَ |
| `alif_variant` | 197 | 0.25% | one skeleton, one ā: on the line in one hand, above it in the other |
| `rasm_variant` | 842 | 1.09% | the codices disagree about the letters on the line |
| `word_boundary` | 155 | 0.20% | a source prints the word joined to its neighbour |
| `partial` | 82 | 0.11% | the word is absent from at least one riwāyah |

Each word gets the *strongest* label that applies, tested in this order: rasm, ā, absence, boundary, dotting, vowelling. So a `dotting_variant` is guaranteed to share one rasm across all riwāyāt, an `alif_variant` to share one skeleton once every ā is spelled out, and an `identical` word is identical after notation folding — the raw spelling of every riwāyah is always kept in `forms`, whatever the label.

## Pairwise agreement

Share of the words two riwāyāt both have, where they agree at each level.

| pair | shared words | same spelling | same qiraah | same letters | same rasm |
|---|---|---|---|---|---|
| ibn-wardan–ibn-jammaz | 77,410 | 100.0% | 100.0% | 100.00% | 100.00% |
| duri–susi | 77,432 | 66.7% | 82.8% | 99.97% | 100.00% |
| hafs–shubah | 77,433 | 99.2% | 99.2% | 99.86% | 99.99% |
| khalaf–ishaq | 77,434 | 94.6% | 94.7% | 99.92% | 99.98% |
| abu-al-harith–ishaq | 77,435 | 98.7% | 98.7% | 99.92% | 99.98% |
| warsh–qalun | 77,431 | 85.2% | 87.5% | 99.93% | 99.98% |
| shubah–duri | 77,432 | 70.8% | 74.1% | 99.75% | 99.97% |
| shubah–bazzi | 77,432 | 84.1% | 84.1% | 99.75% | 99.97% |
| shubah–susi | 77,432 | 72.1% | 72.9% | 99.72% | 99.97% |
| hafs–bazzi | 77,432 | 84.0% | 84.0% | 99.73% | 99.97% |
| khallad–ishaq | 77,434 | 98.7% | 98.8% | 99.90% | 99.97% |
| hafs–duri | 77,432 | 70.8% | 74.1% | 99.73% | 99.97% |
| duri–bazzi | 77,432 | 57.8% | 61.0% | 99.83% | 99.97% |
| khalaf–abu-al-harith | 77,435 | 93.9% | 93.9% | 99.90% | 99.97% |
| hafs–susi | 77,432 | 72.0% | 72.8% | 99.70% | 99.97% |
| susi–bazzi | 77,432 | 66.6% | 67.4% | 99.80% | 99.97% |
| khalaf–khallad | 77,433 | 95.4% | 95.4% | 99.95% | 99.96% |
| khallad–abu-al-harith | 77,434 | 97.9% | 98.0% | 99.87% | 99.95% |
| ruways–rawh | 77,385 | 99.2% | 99.2% | 99.86% | 99.90% |
| hisham–abu-al-harith | 77,432 | 95.9% | 95.9% | 99.51% | 99.87% |
| hisham–khallad | 77,432 | 95.5% | 95.5% | 99.49% | 99.87% |
| hisham–ishaq | 77,432 | 96.0% | 96.0% | 99.53% | 99.86% |
| hisham–khalaf | 77,431 | 91.4% | 91.4% | 99.48% | 99.86% |
| khallad–rawh | 77,423 | 85.7% | 85.7% | 99.36% | 99.79% |
| abu-al-harith–rawh | 77,423 | 85.4% | 85.4% | 99.37% | 99.78% |
| rawh–ishaq | 77,423 | 85.8% | 85.8% | 99.40% | 99.78% |
| khalaf–rawh | 77,422 | 81.9% | 81.9% | 99.34% | 99.77% |
| hisham–rawh | 77,421 | 87.1% | 87.1% | 99.43% | 99.71% |
| khallad–ruways | 77,385 | 85.2% | 85.2% | 99.26% | 99.70% |
| abu-al-harith–ruways | 77,385 | 85.0% | 85.0% | 99.28% | 99.70% |
| ruways–ishaq | 77,385 | 85.3% | 85.3% | 99.30% | 99.69% |
| hafs–qalun | 77,431 | 40.4% | 77.0% | 99.76% | 99.69% |
| shubah–qalun | 77,431 | 40.5% | 77.0% | 99.77% | 99.69% |
| qalun–bazzi | 77,431 | 41.5% | 71.2% | 99.76% | 99.69% |
| qalun–duri | 77,431 | 36.8% | 78.6% | 99.75% | 99.69% |
| khalaf–ruways | 77,384 | 81.3% | 81.4% | 99.24% | 99.69% |
| qalun–susi | 77,431 | 42.6% | 84.8% | 99.72% | 99.68% |
| hafs–warsh | 77,431 | 41.3% | 75.6% | 99.70% | 99.68% |
| shubah–warsh | 77,431 | 41.4% | 75.6% | 99.71% | 99.68% |
| warsh–bazzi | 77,431 | 37.2% | 63.9% | 99.71% | 99.68% |
| hisham–ruways | 77,383 | 86.8% | 86.8% | 99.38% | 99.68% |
| warsh–duri | 77,431 | 37.8% | 76.4% | 99.70% | 99.67% |
| warsh–susi | 77,431 | 39.2% | 78.2% | 99.72% | 99.67% |
| shubah–abu-al-harith | 77,433 | 31.5% | 83.6% | 98.84% | 99.50% |
| hafs–khallad | 77,433 | 31.8% | 83.5% | 98.82% | 99.50% |
| hafs–abu-al-harith | 77,433 | 31.4% | 83.6% | 98.85% | 99.50% |
| shubah–khallad | 77,433 | 31.9% | 83.5% | 98.81% | 99.49% |
| hafs–ishaq | 77,433 | 31.8% | 84.1% | 98.87% | 99.49% |
| shubah–ishaq | 77,433 | 31.9% | 84.1% | 98.86% | 99.49% |
| hafs–khalaf | 77,432 | 30.3% | 79.7% | 98.81% | 99.49% |
| shubah–khalaf | 77,432 | 30.3% | 79.7% | 98.80% | 99.48% |
| duri–abu-al-harith | 77,432 | 27.3% | 66.4% | 98.73% | 99.48% |
| bazzi–abu-al-harith | 77,432 | 29.7% | 71.8% | 98.74% | 99.48% |
| susi–abu-al-harith | 77,432 | 29.5% | 66.2% | 98.70% | 99.47% |
| shubah–hisham | 77,431 | 32.1% | 85.2% | 98.87% | 99.47% |
| duri–khallad | 77,432 | 27.3% | 65.6% | 98.70% | 99.47% |
| bazzi–khallad | 77,432 | 29.9% | 71.8% | 98.71% | 99.47% |
| hafs–hisham | 77,431 | 32.1% | 85.2% | 98.85% | 99.47% |
| susi–khallad | 77,432 | 29.5% | 65.3% | 98.67% | 99.47% |
| duri–ishaq | 77,432 | 27.4% | 66.1% | 98.75% | 99.47% |
| bazzi–ishaq | 77,432 | 30.1% | 72.1% | 98.75% | 99.47% |
| bazzi–hisham | 77,431 | 30.3% | 73.2% | 98.86% | 99.47% |
| susi–ishaq | 77,432 | 29.5% | 65.8% | 98.72% | 99.46% |
| duri–hisham | 77,431 | 27.5% | 66.6% | 98.82% | 99.46% |
| duri–khalaf | 77,431 | 26.1% | 62.4% | 98.69% | 99.46% |
| bazzi–khalaf | 77,431 | 28.5% | 68.3% | 98.70% | 99.46% |
| susi–hisham | 77,431 | 29.5% | 66.1% | 98.79% | 99.46% |
| susi–khalaf | 77,431 | 28.0% | 62.0% | 98.66% | 99.46% |
| hisham–ibn-wardan | 77,407 | 76.8% | 76.8% | 99.38% | 99.43% |
| hisham–ibn-jammaz | 77,407 | 76.8% | 76.9% | 99.37% | 99.43% |
| abu-al-harith–ibn-wardan | 77,407 | 75.4% | 75.4% | 99.16% | 99.41% |
| abu-al-harith–ibn-jammaz | 77,407 | 75.4% | 75.5% | 99.16% | 99.41% |
| khallad–ibn-wardan | 77,407 | 74.8% | 74.9% | 99.14% | 99.41% |
| khallad–ibn-jammaz | 77,407 | 74.8% | 74.9% | 99.14% | 99.41% |
| ibn-wardan–ishaq | 77,407 | 75.2% | 75.2% | 99.17% | 99.40% |
| ibn-jammaz–ishaq | 77,407 | 75.2% | 75.2% | 99.17% | 99.40% |
| khalaf–ibn-wardan | 77,406 | 71.5% | 71.5% | 99.12% | 99.40% |
| khalaf–ibn-jammaz | 77,406 | 71.5% | 71.5% | 99.12% | 99.40% |
| hafs–rawh | 77,422 | 31.7% | 83.5% | 98.72% | 99.34% |
| shubah–rawh | 77,422 | 31.6% | 83.5% | 98.69% | 99.34% |
| ibn-wardan–rawh | 77,396 | 86.4% | 86.4% | 99.31% | 99.34% |
| ibn-jammaz–rawh | 77,396 | 86.4% | 86.4% | 99.31% | 99.34% |
| qalun–ibn-wardan | 77,406 | 45.9% | 65.6% | 98.72% | 99.33% |
| qalun–ibn-jammaz | 77,406 | 45.9% | 65.6% | 98.72% | 99.33% |
| duri–rawh | 77,421 | 27.0% | 64.0% | 98.72% | 99.33% |
| susi–rawh | 77,421 | 31.5% | 69.0% | 98.69% | 99.33% |
| bazzi–rawh | 77,421 | 32.6% | 78.3% | 98.69% | 99.33% |
| warsh–ibn-wardan | 77,406 | 40.7% | 60.4% | 98.72% | 99.32% |
| warsh–ibn-jammaz | 77,406 | 40.7% | 60.4% | 98.72% | 99.32% |
| qalun–hisham | 77,431 | 49.0% | 69.5% | 98.92% | 99.31% |
| ibn-wardan–ruways | 77,359 | 86.2% | 86.2% | 99.27% | 99.31% |
| ibn-jammaz–ruways | 77,359 | 86.2% | 86.2% | 99.28% | 99.31% |
| qalun–khallad | 77,431 | 47.9% | 67.9% | 98.71% | 99.30% |
| warsh–hisham | 77,431 | 45.1% | 67.7% | 98.86% | 99.30% |
| hafs–ruways | 77,384 | 31.4% | 83.0% | 98.67% | 99.30% |
| qalun–abu-al-harith | 77,431 | 48.5% | 68.9% | 98.74% | 99.30% |
| shubah–ruways | 77,384 | 31.4% | 82.9% | 98.65% | 99.30% |
| qalun–ishaq | 77,431 | 48.4% | 68.7% | 98.76% | 99.30% |
| warsh–khallad | 77,431 | 44.6% | 66.8% | 98.66% | 99.29% |
| duri–ruways | 77,383 | 26.9% | 63.7% | 98.68% | 99.29% |
| susi–ruways | 77,383 | 31.4% | 68.8% | 98.65% | 99.29% |
| warsh–abu-al-harith | 77,431 | 44.5% | 67.1% | 98.69% | 99.29% |
| qalun–khalaf | 77,430 | 46.0% | 66.0% | 98.70% | 99.29% |
| bazzi–ruways | 77,383 | 32.4% | 77.9% | 98.65% | 99.29% |
| warsh–ishaq | 77,431 | 45.0% | 67.5% | 98.71% | 99.29% |
| warsh–khalaf | 77,430 | 42.7% | 64.9% | 98.64% | 99.28% |
| qalun–rawh | 77,420 | 51.5% | 73.3% | 98.71% | 99.16% |
| warsh–rawh | 77,420 | 44.4% | 65.8% | 98.66% | 99.15% |
| qalun–ruways | 77,382 | 51.2% | 72.9% | 98.66% | 99.12% |
| warsh–ruways | 77,382 | 44.3% | 65.6% | 98.61% | 99.11% |
| shubah–ibn-wardan | 77,406 | 30.4% | 74.0% | 98.58% | 99.06% |
| shubah–ibn-jammaz | 77,406 | 30.4% | 74.1% | 98.58% | 99.06% |
| hafs–ibn-wardan | 77,406 | 30.5% | 74.1% | 98.57% | 99.05% |
| hafs–ibn-jammaz | 77,406 | 30.5% | 74.1% | 98.57% | 99.05% |
| bazzi–ibn-wardan | 77,406 | 32.9% | 77.5% | 98.59% | 99.05% |
| bazzi–ibn-jammaz | 77,406 | 32.9% | 77.5% | 98.59% | 99.05% |
| duri–ibn-wardan | 77,406 | 26.2% | 55.7% | 98.56% | 99.05% |
| duri–ibn-jammaz | 77,406 | 26.2% | 55.7% | 98.56% | 99.05% |
| susi–ibn-wardan | 77,406 | 31.4% | 62.6% | 98.58% | 99.05% |
| susi–ibn-jammaz | 77,406 | 31.5% | 62.6% | 98.59% | 99.05% |

Rasm agreement never drops below 99.5%: the riwāyāt are one text. Spelling agreement is far lower because the packages were typeset in different years with different conventions — which is what the `folded` and `pointed` columns strip away.

## Where the riwāyāt genuinely disagree

Three things can differ once spelling, vowelling and pointing are set aside: the letters, the word boundaries, and whether a word is there at all. Together they account for 1,090 of 77,442 words. A fourth kind is listed with them and counted apart: 197 words where the disagreement is only about whether an ā sits on the line or above it.

| kind | count | status | what it means |
|---|---|---|---|
| letters differ | 842 | `rasm_variant` | a letter one codex has on the line and another does not — 820 of them one letter more, 22 one letter for another |
| the ā is placed differently | 197 | `alif_variant` | one skeleton once every ā is spelled out; the two hands disagree about which ā to write on the line |
| boundaries differ | 76 events | `word_boundary` | one source prints two words as one |
| word absent | 82 | `partial` | a riwāyah does not have the word at all |

### Letters — rasm disagreements

842 words where the riwāyāt disagree about the letters on the line, after dots, hamzah, vowelling and the ā have all been set aside. These are the differences the sources can be trusted on: they split the riwāyāt 62 different ways — by miṣr, not by publisher — and they are the khilāf the rasm literature names. All 842 are listed below, grouped by what the difference *is*. Machine-readable: [`rasm-variants.md`](rasm-variants.md), [`differences.csv`](../differences.csv).

#### One skeleton, one letter more

820 of the 842. Both sides write the same letters in the same order and one side writes a letter the other does not: `ٮرٮد`/`ٮرٮدد` — يَرۡتَدَّ against يَرۡتَدِدۡ at 5:54 — or `ٮسٮهى`/`ٮسٮهٮه`, تَشۡتَهِي against تَشۡتَهِيهِ at 43:71. Nothing is replaced; the skeletons nest.

| word id | sūrah:āyah | rasm on each side | as printed |
|---|---|---|---|
| 19 | 1:6 | `الصرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الرط` ruways | **ٱلصِّرَٰطَ** hafs,shubah,bazzi  ·  **ࡰ۬لصِّرَٰطَ** qalun,warsh  ·  **اَ۬لصِّرَٰطَ** duri  ·  **ࡱ۬لصِّرَٰطَ** susi  ·  **ٱلصِّرَٰطَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ٱلۜرَٰطَ** ruways |
| 21 | 1:7 | `صرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `رط` ruways | **صِرَٰطَ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ۜرَٰطَ** ruways |
| 219 | 2:19 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 274 | 2:22 | `الارص` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `االارص` khallad | **ٱلۡأَرۡضَ** hafs,shubah,bazzi  ·  **ࡲ۬لْأَرْضَ** qalun  ·  **ࡲ۬لَارْضَ** warsh  ·  **اُ۬لۡأَرۡضَ** duri  ·  **ࡲ۬لۡأَرۡضَ** susi  ·  **ٱلْأَرْضَ** hisham,khalaf,abu-al-harith,ishaq  ·  **االْأَرْضَ** khallad  ·  **ٱلأَْرْضَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 280 | 2:22 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 416 | 2:27 | `الارص` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `االارص` khallad | **ٱلۡأَرۡضِ** hafs,shubah,bazzi  ·  **ࡴ۬لْأَرْضِ** qalun  ·  **ࡴ۬لَارْضِ** warsh  ·  **اِ۬لۡأَرۡضِ** duri  ·  **ࡵ۬لۡأَرۡضِ** susi  ·  **ٱلْأَرْضِ** hisham,khalaf,abu-al-harith,ishaq  ·  **االْأَرْضِ** khallad  ·  **ٱلأَْرْضِ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 444 | 2:29 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 490 | 2:31 | `ٮاسما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮاسماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِأَسۡمَآءِ** hafs,shubah,bazzi,duri,susi  ·  **بِأَسْمَآءِ** qalun,warsh  ·  **بِأَسْمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 491 | 2:31 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  `هولااں` ibn-wardan,ibn-jammaz,ruways | **هَٰٓؤُلَآءِ** hafs,shubah,warsh  ·  **هَٰؤُلَآࢇ** bazzi,qalun  ·  **هَٰٓؤُلَآ** duri  ·  **هَٰؤُلَا** susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **هَٰؤُلَآآءِن** ibn-wardan,ibn-jammaz,ruways |
| 579 | 2:37 | `ڡٮلڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡٮلڡٮى` ibn-wardan,ibn-jammaz | **فَتَلَقَّىٰٓ** hafs,shubah,duri  ·  **فَتَلَقَّىٰ** bazzi,qalun,susi  ·  **فَتَلَقّٜىٰٓ** warsh  ·  **فَتَلَقَّىٰٓ** hisham  ·  **فَتَلَقّٜ۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **فَتَلَقَّيى** ibn-wardan,ibn-jammaz  ·  **فَتَلَقَّيٰ** ruways,rawh |
| 749 | 2:51 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `موسٮى` ibn-wardan,ibn-jammaz | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ibn-wardan,ibn-jammaz |
| 873 | 2:59 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 956 | 2:61 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 1375 | 2:85 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 1456 | 2:87 | `ٮهوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮهوٮى` ibn-wardan,ibn-jammaz | **تَهۡوَىٰٓ** hafs,shubah,duri  ·  **تَهۡوَىٰ** bazzi,susi  ·  **تَهْوَىٰ** qalun,ruways,rawh  ·  **تَهْوٜىٰٓ** warsh  ·  **تَهْوَىٰٓ** hisham  ·  **تَهْو۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَهْوَىى** ibn-wardan,ibn-jammaz |
| 1757 | 2:102 | `المر` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `المرا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡمَرۡءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَرْءِ** qalun,warsh  ·  **اَ۬لۡمَرۡءِ** duri  ·  **ࡱ۬لۡمَرۡءِ** susi  ·  **ٱلْمَرْآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 2052 | 2:116 | `وڡالوا` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ڡالوا` hisham | **وَقَالُواْ** hafs,shubah,bazzi,qalun,warsh,duri,susi,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **قَالُواْ** hisham  ·  **وَّقَالُواْ** khalaf |
| 2070 | 2:117 | `ڡصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡصٮى` ibn-wardan,ibn-jammaz | **قَضَىٰٓ** hafs,shubah,duri,hisham  ·  **قَضَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **قَضٜىٰٓ** warsh  ·  **قَض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **قَضَيى** ibn-wardan,ibn-jammaz |
| 2187 | 2:124 | `اٮٮلى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اٮٮلٮى` ibn-wardan,ibn-jammaz | **ٱبۡتَلَىٰٓ** hafs,shubah  ·  **ٱبۡتَلَىٰ** bazzi  ·  **ࡴٜبْتَلَىٰ** qalun  ·  **ࡴٜبْتَلٜىٰٓ** warsh  ·  **اِ۪بۡتَلَىٰٓ** duri  ·  **ࡵٜبۡتَلَىٰ** susi  ·  **ٱبْتَلَيٰٓ** hisham  ·  **ٱبْتَل۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱبْتَلَيى** ibn-wardan,ibn-jammaz  ·  **ٱبْتَلَىٰ** ruways,rawh |
| 2188 | 2:124 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهِـيمَ** warsh  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2214 | 2:125 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبۡرَٰهِـۧم** susi  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2217 | 2:125 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 2218 | 2:125 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2229 | 2:126 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمُ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمُ** bazzi  ·  **إِبْرَٰهِيمُ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمُ** hisham  ·  **إِبْرَٰهِـمُ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2259 | 2:127 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمُ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمُ** bazzi  ·  **إِبْرَٰهِيمُ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمُ** hisham  ·  **إِبْرَٰهِـمُ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2308 | 2:130 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2331 | 2:132 | `ووصى` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `واوصى` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **وَوَصَّىٰ** hafs,shubah,bazzi,duri,susi  ·  **وَأَوْصَىٰ** qalun,hisham,ibn-wardan,ibn-jammaz  ·  **وَأَوْصٜىٰ** warsh  ·  **وَوَصّٜ۪ىٰ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَوَصَّىٰ** ruways,rawh |
| 2333 | 2:132 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمُ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمُ** bazzi  ·  **إِبْرَٰهِيمُ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمُ** hisham  ·  **إِبْرَٰهِـمُ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2350 | 2:133 | `اد` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  `د` ibn-wardan,ibn-jammaz,ruways | **إِذۡ** hafs,shubah  ·  **ࡹذۡ** bazzi,susi  ·  **ࡹذْ** qalun,warsh  ·  **ا۪ذۡ** duri  ·  **إِذْ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ذْ** ibn-wardan,ibn-jammaz,ruways |
| 2366 | 2:133 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2398 | 2:135 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2412 | 2:136 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 2413 | 2:136 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2481 | 2:140 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2491 | 2:140 | `اٮٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااٮٮم` hisham | **ءَأَنتُمۡ** hafs,shubah  ·  **ءَࡶنتُمُۥ** bazzi  ·  **ءَٰࡶنتُمْ** qalun  ·  **آٓنتُمُۥٓ** warsh  ·  **ءَٰا۬نتُمۡ** duri  ·  **ءَٰࡶنتُمۡ** susi  ·  **ءَاانتُمْ** hisham  ·  **ءَأَنتُمْ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءٱنتُمۥُ** ibn-wardan,ibn-jammaz  ·  **ءَٱنتُمْ** ruways |
| 2540 | 2:142 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮسالى` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,duri,susi  ·  **يَّشَآءُ** qalun,warsh  ·  **يَشَآءُ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَّشَآءُ** khalaf  ·  **يَشَآءُِلَىٰ** ibn-wardan,ibn-jammaz |
| 2541 | 2:142 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,rawh  ·  **ࡹِلَىٰ** bazzi,qalun,warsh,susi  ·  **اِ۪لَىٰ** duri  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلَىٰۜرَٰطࣲ** ruways |
| 2926 | 2:164 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 2944 | 2:164 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 3033 | 2:169 | `ٮالسو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالسوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلسُّوٓءِ** hafs,shubah,bazzi  ·  **بِالسُّوٓءِ** qalun,warsh,duri,susi  ·  **بِالسُّوٓآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 3034 | 2:169 | `والڡحسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والڡحساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلۡفَحۡشَآءِ** hafs,shubah,bazzi  ·  **وَالْفَحْشَآءِ** qalun,warsh  ·  **وَاَلۡفَحۡشَآءِ** duri  ·  **وَࡱلۡفَحۡشَآءِ** susi  ·  **وَٱلْفَحْشَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 3114 | 2:173 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡا` ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَلاَ** ibn-wardan,ibn-jammaz  ·  **فَا** ruways,rawh |
| 3182 | 2:177 | `والمعرٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `المعرٮ` hisham | **وَٱلۡمَغۡرِبِ** hafs,shubah,bazzi  ·  **وَالْمَغْرِبِ** qalun,warsh  ·  **وَاَلۡمَغۡرِبِ** duri  ·  **وَࡱلۡمَغۡرِبِ** susi  ·  **ٱلْمَغْرِبِ** hisham  ·  **وَٱلْمَغْرِبِ** khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 3192 | 2:177 | `والٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **وَالنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **وَاَلنَّبِيِّـۧنَ** duri  ·  **وَࡱلنَّبِيِّـۧنَ** susi  ·  **وَٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 3216 | 2:177 | `الٮاسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮاساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡبَأۡسَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لْبَأْسَآءِ** qalun,warsh  ·  **اِ۬لۡبَأۡسَآءِ** duri  ·  **ࡵ۬لۡبَاسَآءِ** susi  ·  **ٱلْبَأْسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْبَاسَآآءِ** ibn-wardan,ibn-jammaz |
| 3217 | 2:177 | `والصرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والصراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلضَّرَّآءِ** hafs,shubah,bazzi  ·  **وَالضَّرَّآءِ** qalun,warsh  ·  **وَاَلضَّرَّآءِ** duri  ·  **وَࡱلضَّرَّآءِ** susi  ·  **وَٱلضَّرَّآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 3310 | 2:182 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡا` ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَلاَ** ibn-wardan,ibn-jammaz  ·  **فَا** ruways,rawh |
| 3823 | 2:203 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡا` ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَلاَ** ibn-wardan,ibn-jammaz  ·  **فا** ruways,rawh |
| 3828 | 2:203 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡا` ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَلاَ** ibn-wardan,ibn-jammaz  ·  **فَا** ruways,rawh |
| 3983 | 2:213 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡲ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اُ۬لنَّبِيِّـۧنَ** duri  ·  **ࡲ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 4023 | 2:213 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,rawh  ·  **ࡹِلَىٰ** bazzi,qalun,warsh,susi  ·  **اِ۪لَىٰ** duri  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلَىٰۜرَٰطࣲ** ruways |
| 4084 | 2:216 | `وعسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وعسٮى` ibn-wardan,ibn-jammaz | **وَعَسَىٰٓ** hafs,shubah,duri,hisham  ·  **وَعَسَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **وَعَسٜىٰٓ** warsh  ·  **وَعَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَعَسَىى** ibn-wardan,ibn-jammaz |
| 4091 | 2:216 | `وعسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وعسٮى` ibn-wardan,ibn-jammaz | **وَعَسَىٰٓ** hafs,shubah,duri,hisham  ·  **وَعَسَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **وَعَسٜىٰٓ** warsh  ·  **وَعَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَعَسَىى** ibn-wardan,ibn-jammaz |
| 4318 | 2:224 | `وٮصلحوا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `و` khalaf,abu-al-harith,ishaq | **وَتُصۡلِحُواْ** hafs,shubah,bazzi,duri,susi  ·  **وَتُصْلِحُواْ** qalun,warsh,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **وَ** khalaf,abu-al-harith,ishaq |
| 4650 | 2:235 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لنِّسَآءِ** qalun,warsh  ·  **اِ۬لنِّسَآءِ** duri  ·  **ࡵ۬لنِّسَآءِ** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 4874 | 2:246 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `موسٮى` ibn-wardan,ibn-jammaz | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ibn-wardan,ibn-jammaz |
| 5279 | 2:258 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمَ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمَ** bazzi  ·  **إِبْرَٰهِيمَ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمَ** hisham  ·  **إِبْرَٰهِـمَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 5288 | 2:258 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمُ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمُ** bazzi  ·  **إِبْرَٰهِيمُ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمُ** hisham  ·  **إِبْرَٰهِـمُ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 5298 | 2:258 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمُ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمُ** bazzi  ·  **إِبْرَٰهِيمُ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمُ** hisham  ·  **إِبْرَٰهِـمُ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 5377 | 2:259 | `اعلم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااعلم` khallad | **أَعۡلَمُ** hafs,shubah,bazzi,duri,susi  ·  **أَعْلَمُ** qalun,warsh,hisham,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **ٱعْلَمْ** khalaf,abu-al-harith  ·  **ااعْلَمْ** khallad |
| 5386 | 2:260 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `اٮرهم` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **إِبۡرَٰهِـۧمُ** hafs,shubah,duri,susi  ·  **إِبۡرَٰهِيمُ** bazzi  ·  **إِبْرَٰهِيمُ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **إِبْرَٰهَٰمُ** hisham  ·  **إِبْرَٰهِـمُ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 5703 | 2:273 | `للڡڡرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `للڡڡراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **لِلۡفُقَرَآءِ** hafs,shubah,bazzi,duri,susi  ·  **لِلْفُقَرَآءِ** qalun,warsh  ·  **لِلْفُقَرَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 5780 | 2:275 | `ڡاٮٮهى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ڡاٮٮهٮى` khalaf,abu-al-harith,ishaq | **فَٱنتَهَىٰ** hafs,shubah,bazzi  ·  **فَانتَهَىٰ** qalun,hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **فَانتَهٜىٰ** warsh  ·  **فَاَنتَهَىٰ** duri,susi  ·  **فَانتَه۪يى** khalaf,abu-al-harith,ishaq  ·  **فَانتَه۪ىٰ** khallad |
| 5834 | 2:278 | `الرٮوا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الرٮوٮا` ibn-wardan,ibn-jammaz | **ٱلرِّبَوٰٓاْ** hafs,shubah  ·  **ٱلرِّبَوٰاْ** bazzi  ·  **ࡰ۬لرِّبَوٰاْ** qalun  ·  **ࡰ۬لرِّبَوٰٓاْ** warsh  ·  **اَ۬لرِّبَوٰٓاْ** duri  ·  **ࡱ۬لرِّبَوٰاْ** susi  ·  **ٱلرِّٜبَوٰٓاْ** hisham  ·  **ٱلرِّٜب۪وٰٓاْ** khalaf,abu-al-harith,ishaq  ·  **ٱلرِّٜبوٰ۪ٓاْ** khallad  ·  **ٱلرِّٜبَوىاْ** ibn-wardan,ibn-jammaz  ·  **ٱلرِّٜبَوٰاْ** ruways,rawh |
| 5890 | 2:282 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **ࡴلَىٰٓ** warsh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 5948 | 2:282 | `السهدا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السهداا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلشُّهَدَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لشُّهَدَآءِ** qalun,warsh  ·  **اَ۬لشُّهَدَآءِ** duri  ·  **ࡱ۬لشُّهَدَآءِ** susi  ·  **ٱلشُّهَدَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 5957 | 2:282 | `السهدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `السهدادا` ibn-wardan,ibn-jammaz | **ٱلشُّهَدَآءُ** hafs,shubah,bazzi  ·  **ࡰ۬لشُّهَدَآءُ** qalun,warsh  ·  **اَ۬لشُّهَدَآءُ** duri  ·  **ࡱ۬لشُّهَدَآءُ** susi  ·  **ٱلشُّهَدَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلشُّهَدَآءُِذَا** ibn-wardan,ibn-jammaz |
| 5968 | 2:282 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **ࡴلَىٰٓ** warsh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 5976 | 2:282 | `وادٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وادٮٮى` ibn-wardan,ibn-jammaz | **وَأَدۡنَىٰٓ** hafs,shubah,duri  ·  **وَأَدۡنَىٰ** bazzi,susi  ·  **وَأَدْنَىٰ** qalun,ruways,rawh  ·  **وَأَدْنٜىٰٓ** warsh  ·  **وَأَدْنَيٰٓ** hisham  ·  **وَأَدْن۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَأَدْنَيى** ibn-wardan,ibn-jammaz |
| 6195 | 3:5 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 6344 | 3:13 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساں` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,duri,susi  ·  **يَّشَآءُ** qalun,warsh  ·  **يَشَآءُ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَّشَآءُ** khalaf  ·  **يَشَآءُِنَّ** ibn-wardan,ibn-jammaz |
| 6356 | 3:14 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لنِّسَآءِ** qalun,warsh  ·  **اَ۬لنِّسَآءِ** duri  ·  **ࡱ۬لنِّسَآءِ** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 6472 | 3:20 | `والامٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والامٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلۡأُمِّيِّـۧنَ** hafs,shubah,bazzi  ·  **وَالْأُمِّيِّۑنَ** qalun  ·  **وَالُامِّيِّۑنَ** warsh  ·  **وَاَلۡأُمِّيِّـۧنَ** duri  ·  **وَࡱلۡأُمِّيِّـۧنَ** susi  ·  **وَٱلأُْمِّٜيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 6473 | 3:20 | `اسلمٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااسلمٮم` hisham | **ءَأَسۡلَمۡتُمۡ** hafs,shubah  ·  **ءَࡶسۡلَمۡتُمُۥ** bazzi  ·  **ءَٰࡶسْلَمْتُمْ** qalun  ·  **ءَآسْلَمْتُمْ** warsh  ·  **ءَٰا۬سۡلَمۡتُمۡ** duri  ·  **ءَٰࡶسۡلَمۡتُمۡ** susi  ·  **ءَااسْلَمْتُمْ** hisham  ·  **ءَأَسْلَمْتُمْ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءٱسْلَمْتُمۥُ** ibn-wardan,ibn-jammaz  ·  **ءَٱسْلَمْتُمْ** ruways |
| 6492 | 3:21 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 6601 | 3:27 | `المٮٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `المٮٮٮ` hisham | **ٱلۡمَيِّتِ** hafs  ·  **ٱلۡمَيۡتِ** shubah,bazzi  ·  **ࡰ۬لْمَيِّتِ** qalun,warsh  ·  **اَ۬لۡمَيۡتِ** duri  ·  **ࡱ۬لۡمَيۡتِ** susi  ·  **ٱلْمَيْيتِ** hisham  ·  **ٱلْمَيِّٜتِ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْمَيِّتِ** ibn-wardan,ibn-jammaz |
| 6603 | 3:27 | `المٮٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `المٮٮٮ` hisham | **ٱلۡمَيِّتَ** hafs  ·  **ٱلۡمَيۡتَ** shubah,bazzi  ·  **ࡲ۬لْمَيِّتَ** qalun,warsh  ·  **اُ۬لۡمَيۡتَ** duri  ·  **ࡲ۬لۡمَيۡتَ** susi  ·  **ٱلْمَيْيتَ** hisham  ·  **ٱلْمَيِّٜتَ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْمَيِّتَ** ibn-wardan,ibn-jammaz |
| 6779 | 3:37 | `ركرٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ركرٮاا` ruways,rawh | **زَكَرِيَّا** hafs  ·  **زَكَرِيَّآءَ** shubah  ·  **زَكَرِيَّآءُ** bazzi,qalun,warsh,duri,susi  ·  **زَكَرِيَّاءُ** hisham  ·  **زَكَرِيَّا** khalaf,khallad,abu-al-harith,ishaq  ·  **زَكَرِيَّآءُ** ibn-wardan,ibn-jammaz  ·  **زَكَرِيَّااءُ** ruways,rawh |
| 6783 | 3:37 | `ركرٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ركرٮاا` ruways,rawh | **زَكَرِيَّا** hafs  ·  **زَكَرِيَّآءُ** shubah,bazzi,qalun,warsh,duri,susi  ·  **زَكَرِيَّاءُ** hisham  ·  **زَكَرِيَّا** khalaf,khallad,abu-al-harith,ishaq  ·  **زَكَرِيَّآءُ** ibn-wardan,ibn-jammaz  ·  **زَكَرِيَّااءُ** ruways,rawh |
| 6807 | 3:38 | `ركرٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ركرٮاا` ruways,rawh | **زَكَرِيَّا** hafs  ·  **زَكَرِيَّآءُ** shubah,bazzi,qalun,warsh,duri,susi  ·  **زَكَرِيَّاءُ** hisham  ·  **زَكَرِيَّا** khalaf,khallad,abu-al-harith,ishaq  ·  **زَكَرِيَّآءُ** ibn-wardan,ibn-jammaz  ·  **زَكَرِيَّااءُ** ruways,rawh |
| 6819 | 3:38 | `الدعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الدعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلدُّعَآءِ** hafs,shubah,bazzi  ·  **ࡲ۬لدُّعَآءِ** qalun,warsh,susi  ·  **اُ۬لدُّعَآءِ** duri  ·  **ٱلدُّعَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 6887 | 3:42 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **نِسَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **نِسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 6898 | 3:44 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَنۢبَآءِ** hafs,shubah,bazzi,qalun,duri,susi  ·  **ࡰنۢبَآءِ** warsh  ·  **أَنۢبَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 6959 | 3:47 | `ڡصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡصٮى` ibn-wardan,ibn-jammaz | **قَضَىٰٓ** hafs,shubah,duri,hisham  ·  **قَضَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **قَضٜىٰٓ** warsh  ·  **قَض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **قَضَيى** ibn-wardan,ibn-jammaz |
| 7040 | 3:51 | `هدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `هدارط` ruways | **هَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **هَّٰذَا** susi  ·  **هَٰذَاۜرَٰطࣱ** ruways |
| 7081 | 3:55 | `ٮعٮسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮعٮسٮى` ibn-wardan,ibn-jammaz | **يَٰعِيسَىٰٓ** hafs,shubah,hisham  ·  **يَٰعِيسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰعِيسٜىٰٓ** warsh  ·  **يَٰعِيسۭيٰٓ** duri  ·  **يَٰعِيس۪ىٰ** susi  ·  **يَٰعِيس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰعِيسَىى** ibn-wardan,ibn-jammaz |
| 7254 | 3:66 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 7415 | 3:75 | `الامٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الامٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡأُمِّيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡴ۬لْأُمِّيِّۑنَ** qalun  ·  **ࡴ۬لُامِّيِّۑنَ** warsh  ·  **اِ۬لۡأُمِّيِّـۧنَ** duri  ·  **ࡵ۬لۡأُمِّيِّـۧنَ** susi  ·  **ٱلأُْمِّٜيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 7508 | 3:79 | `رٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `رٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **رَبَّٰنِيِّـۧنَ** hafs,shubah,bazzi,duri,susi  ·  **رَبَّٰنِيِّۑنَ** qalun,warsh  ·  **رَبَّٰنِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 7521 | 3:80 | `والٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **وَالنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **وَاَلنَّبِيِّـۧنَ** duri  ·  **وَࡱلنَّبِيِّـۧنَ** susi  ·  **وَٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 7533 | 3:81 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 7549 | 3:81 | `اڡررٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااڡررٮم` hisham | **ءَأَقۡرَرۡتُمۡ** hafs,shubah  ·  **ءَࡶقۡرَرۡتُمُۥ** bazzi  ·  **ءَٰࡶقْرَرْتُمْ** qalun  ·  **ءَآقْرَرْتُمْ** warsh  ·  **ءَٰا۬قۡرَرۡتُمۡ** duri  ·  **ءَٰࡶقۡرَرۡتُمۡ** susi  ·  **ءَااقْرَرْتُمْ** hisham  ·  **ءَأَقْرَرْتُمْ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءٱقْرَرْتُمۥُ** ibn-wardan,ibn-jammaz  ·  **ءَٱقْرَرْتُمْ** ruways |
| 7591 | 3:84 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 7865 | 3:101 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 8170 | 3:119 | `اولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أُوْلَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **أُوْلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 8263 | 3:125 | `ٮلى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮلٮى` ibn-wardan,ibn-jammaz | **بَلَىٰٓ** hafs,shubah,duri  ·  **بَلَىٰ** bazzi,qalun,susi  ·  **بَلٜىٰٓ** warsh  ·  **بَلَيٰٓ** hisham  ·  **بَل۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **بَلَيى** ibn-wardan,ibn-jammaz  ·  **بَلَيٰ** ruways,rawh |
| 8337 | 3:130 | `الرٮوا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الرٮوٮا` ibn-wardan,ibn-jammaz | **ٱلرِّبَوٰٓاْ** hafs,shubah  ·  **ٱلرِّبَوٰاْ** bazzi  ·  **ࡲ۬لرِّبَوٰاْ** qalun,susi  ·  **ࡲ۬لرِّبَوٰٓاْ** warsh  ·  **اُ۬لرِّبَوٰٓاْ** duri  ·  **ٱلرِّٜبَوٰٓاْ** hisham  ·  **ٱلرِّٜب۪وٰٓاْ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلرِّٜبَوىاْ** ibn-wardan,ibn-jammaz  ·  **ٱلرِّٜبَوٰاْ** ruways,rawh |
| 8354 | 3:133 | `وسارعوا` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `سارعوا` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **وَسَارِعُوٓاْ** hafs,shubah,duri,khalaf,khallad,abu-al-harith,ishaq  ·  **وَسَارِعُواْ** bazzi,susi,ruways,rawh  ·  **سَارِعُواْ** qalun,ibn-wardan,ibn-jammaz  ·  **سَارِعُوٓاْ** warsh,hisham |
| 8368 | 3:134 | `السرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّرَّآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّرَّآءِ** qalun,warsh  ·  **اِ۬لسَّرَّآءِ** duri  ·  **ࡵ۬لسَّرَّآءِ** susi  ·  **ٱلسَّرَّآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 8369 | 3:134 | `والصرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والصراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلضَّرَّآءِ** hafs,shubah,bazzi  ·  **وَالضَّرَّآءِ** qalun,warsh  ·  **وَاَلضَّرَّآءِ** duri  ·  **وَࡱلضَّرَّآءِ** susi  ·  **وَٱلضَّرَّآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 8513 | 3:144 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 8608 | 3:149 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 8644 | 3:152 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّيٰ** ruways,rawh |
| 8681 | 3:153 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 8847 | 3:157 | `ٮحمعوں` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮاحمعوں` ruways,rawh | **يَجۡمَعُونَ** hafs  ·  **تَجۡمَعُونَ** shubah,bazzi,duri,susi  ·  **تَجْمَعُونَ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **تأجْمَعُونَ** ruways,rawh |
| 8852 | 3:158 | `لالى` hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `لاالى` duri,susi | **لَإِلَى** hafs,shubah,bazzi,qalun,warsh  ·  **لَإِاْلَى** duri,susi  ·  **لإَُلَي** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لإَٓلَي** ibn-wardan,ibn-jammaz,ruways,rawh |
| 9334 | 3:184 | `والرٮر` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `وٮالرٮر` hisham | **وَٱلزُّبُرِ** hafs,shubah,bazzi  ·  **وَالزُّبُرِ** qalun,warsh  ·  **وَاَلزُّبُرِ** duri  ·  **وَࡱلزُّبُرِ** susi  ·  **وَبِالزُّبُرِ** hisham  ·  **وَٱلزُّبُرِ** khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 9335 | 3:184 | `والكٮٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `وٮالكٮٮ` hisham | **وَٱلۡكِتَٰبِ** hafs,shubah,bazzi  ·  **وَالْكِتَٰبِ** qalun,warsh  ·  **وَاَلۡكِتَٰبِ** duri  ·  **وَࡱلۡكِتَٰبِ** susi  ·  **وَبِالْكِتَٰبِ** hisham  ·  **وَٱلْكِتَٰبِ** khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 9516 | 3:195 | `اصٮع` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اٮٮلااصٮع` ruways,rawh | **أُضِيعُ** hafs,shubah,bazzi,qalun,warsh,duri,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **أُضِيع** susi  ·  **أَنِّٜيلَاأُضِيعُ** ruways,rawh |
| 9684 | 4:3 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لنِّسَآءِ** qalun,warsh  ·  **اَ۬لنِّسَآءِ** duri  ·  **ࡱ۬لنِّسَآءِ** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 9774 | 4:7 | `وللٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وللٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَلِلنِّسَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وَلِلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 9792 | 4:8 | `والٮٮمى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `الٮٮمى` khalaf | **وَٱلۡيَتَٰمَىٰ** hafs,shubah,bazzi  ·  **وَالْيَتَٰمَىٰ** qalun  ·  **وَالْيَتَٰمٜىٰ** warsh  ·  **وَاَلۡيَتَٰمَىٰ** duri  ·  **وَࡱلۡيَتَٰمَىٰ** susi  ·  **وَٱلْيَتَٰمَيٰ** hisham  ·  **ٱلْيَتَٰم۪يٰ** khalaf  ·  **وَٱلْيَتَٰم۪يٰ** khallad,ishaq  ·  **وَٱلْيَتَٰم۪ىٰ** abu-al-harith  ·  **وَٱلْيَتَٰمَىٰ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 9868 | 4:11 | `ڡلامه` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ڡلالالامه` abu-al-harith | **فَلِأُمِّهِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **فَلأُِمِّٜهِ** hisham,ishaq  ·  **فَلإمِّٜهِ** khalaf  ·  **فَِلإِمِّٜهِ** khallad  ·  **فَلإِلإلإمِّٜهِ** abu-al-harith  ·  **فَلأ۠مِّٜهِ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 9874 | 4:11 | `ڡلامه` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ڡلالالامه` abu-al-harith | **فَلِأُمِّهِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **فَلأُِمِّٜهِ** hisham,ishaq  ·  **فَلإمِّٜهِ** khalaf  ·  **فَِلإِمِّٜهِ** khallad  ·  **فَلإِلإلإمِّٜهِ** abu-al-harith  ·  **فَلأ۠مِّٜهِ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 10166 | 4:22 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah  ·  **ٱلنِّسَآࢇ** bazzi  ·  **ࡰ۬لنِّسَآࢇ** qalun  ·  **ࡰ۬لنِّسَآءِ** warsh  ·  **اَ۬لنِّسَآ** duri  ·  **ࡱ۬لنِّسَا** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 10167 | 4:22 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لا` ibn-wardan,ibn-jammaz | **إِلَّا** hafs,shubah,bazzi,qalun,duri,susi  ·  **الَّا** warsh  ·  **إِلَّا** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **لَّا** ibn-wardan,ibn-jammaz  ·  **ٱلَّا** ruways |
| 10233 | 4:24 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah  ·  **ٱلنِّسَآࢇ** bazzi  ·  **ࡰ۬لنِّسَآࢇ** qalun  ·  **ࡰ۬لنِّسَآءِ** warsh  ·  **اَ۬لنِّسَآ** duri  ·  **ࡱ۬لنِّسَا** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 10234 | 4:24 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لا` ibn-wardan,ibn-jammaz | **إِلَّا** hafs,shubah,bazzi,qalun,duri,susi  ·  **الَّا** warsh  ·  **إِلَّا** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **لَّا** ibn-wardan,ibn-jammaz  ·  **ٱلَّا** ruways |
| 10241 | 4:24 | `واحل` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `واحدل` hisham | **وَأُحِلَّ** hafs  ·  **وَأَحَلَّ** shubah,bazzi,qalun,warsh,duri,susi  ·  **وَأَحدلَّ** hisham  ·  **وَأُحِلَّ** khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **وَأَحَلَّ** ruways,rawh |
| 10427 | 4:32 | `وللٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وللٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَلِلنِّسَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وَلِلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 10463 | 4:34 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لنِّسَآءِ** qalun,warsh  ·  **اَ۬لنِّسَآءِ** duri  ·  **ࡱ۬لنِّسَآءِ** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 10627 | 4:41 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 10664 | 4:43 | `مرصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `مرصٮى` ibn-wardan,ibn-jammaz | **مَّرۡضَىٰٓ** hafs,shubah  ·  **مَرۡضَىٰ** bazzi  ·  **مَّرْضَىٰ** qalun  ·  **مَّرْضٜىٰٓ** warsh  ·  **مَّرۡضۭيٰٓ** duri  ·  **مَّرۡض۪ىٰ** susi  ·  **مَّرْضَىٰٓ** hisham  ·  **مَّرْض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مَرْضَيى** ibn-wardan,ibn-jammaz  ·  **مَّرْضَىٰ** ruways,rawh |
| 10768 | 4:47 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 10797 | 4:48 | `اڡٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اڡٮرٮى` ibn-wardan,ibn-jammaz | **ٱفۡتَرَىٰٓ** hafs,shubah  ·  **ٱفۡتَرَىٰ** bazzi  ·  **ࡴٜفْتَرَىٰ** qalun  ·  **ࡴٜفْتَرٜىٰٓ** warsh  ·  **اِ۪فۡتَر۪يٰٓ** duri  ·  **ࡵٜفۡتَرٜىٰ** susi  ·  **ٱفْتَرَىٰٓ** hisham  ·  **ٱفْتر۪ىٰٓ** khalaf,abu-al-harith,ishaq  ·  **ٱفْتَر۪ىٰٓ** khallad  ·  **ٱفْتَرَىى** ibn-wardan,ibn-jammaz  ·  **ٱفْتَرَىٰ** ruways,rawh |
| 10838 | 4:51 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 10940 | 4:58 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 11120 | 4:66 | `ڡلٮل` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ڡلٮلا` hisham | **قَلِيلࣱ** hafs,shubah,bazzi,qalun,warsh,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **قَلِيلٞ** duri  ·  **قَلِيلاࣰ** hisham |
| 11139 | 4:68 | `ولهدٮٮهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `ولهدٮٮهمرطا` ruways | **وَلَهَدَيۡنَٰهُمۡ** hafs,shubah,duri,susi  ·  **وَلَهَدَيۡنَٰهُمُۥ** bazzi  ·  **وَلَهَدَيْنَٰهُمْ** qalun,warsh,hisham,khallad,abu-al-harith,rawh,ishaq  ·  **وَّلَهَدَيْنَٰهُمْ** khalaf  ·  **وَلَهَدَيْنَٰهُمۥُ** ibn-wardan,ibn-jammaz  ·  **وَلَهَدَيْنَٰهُمْۜرَٰطࣰا** ruways |
| 11153 | 4:69 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 11155 | 4:69 | `والسهدا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والسهداا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلشُّهَدَآءِ** hafs,shubah,bazzi  ·  **وَالشُّهَدَآءِ** qalun,warsh  ·  **وَاَلشُّهَدَآءِ** duri  ·  **وَࡱلشُّهَدَآءِ** susi  ·  **وَٱلشُّهَدَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 11243 | 4:75 | `والٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **وَالنِّسَآءِ** qalun,warsh  ·  **وَاَلنِّسَآءِ** duri  ·  **وَࡱلنِّسَآءِ** susi  ·  **وَٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 11318 | 4:77 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 11362 | 4:78 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 11448 | 4:83 | `والى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `والٮى` ibn-wardan,ibn-jammaz | **وَإِلَىٰٓ** hafs,shubah,warsh,duri,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **وَإِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **وَإِلَىى** ibn-wardan,ibn-jammaz |
| 11676 | 4:92 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **ࡴلَىٰٓ** warsh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 11701 | 4:92 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **ࡴلَىٰٓ** warsh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 11747 | 4:94 | `الڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الڡٮى` ibn-wardan,ibn-jammaz | **أَلۡقَىٰٓ** hafs,shubah,duri  ·  **أَلۡقَىٰ** bazzi,susi  ·  **أَلْقَىٰ** qalun,ruways,rawh  ·  **ࡰلْقٜىٰٓ** warsh  ·  **أَلْقَيٰٓ** hisham  ·  **أَلْق۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أَلْقَيى** ibn-wardan,ibn-jammaz |
| 11846 | 4:98 | `والٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **وَالنِّسَآءِ** qalun,warsh  ·  **وَاَلنِّسَآءِ** duri  ·  **وَࡱلنِّسَآءِ** susi  ·  **وَٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 11968 | 4:102 | `مرصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `مرصٮى` ibn-wardan,ibn-jammaz | **مَّرۡضَىٰٓ** hafs,shubah  ·  **مَرۡضَىٰ** bazzi  ·  **مَّرْضَىٰ** qalun  ·  **مَّرْضٜىٰٓ** warsh  ·  **مَّرۡضۭيٰٓ** duri  ·  **مَّرۡض۪ىٰ** susi  ·  **مَّرْضَىٰٓ** hisham  ·  **مَّرْض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مَرْضَيى** ibn-wardan,ibn-jammaz  ·  **مَّرْضَىٰ** ruways,rawh |
| 12003 | 4:104 | `اٮٮعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱبۡتِغَآءِ** hafs,shubah,bazzi  ·  **ࡴٜبْتِغَآءِ** qalun,warsh  ·  **اِ۪بۡتِغَآءِ** duri  ·  **ࡵٜبۡتِغَآءِ** susi  ·  **ٱبْتِغَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 12080 | 4:109 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 12388 | 4:127 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لنِّسَآءِ** qalun,warsh  ·  **اَ۬لنِّسَآءِ** duri  ·  **ࡱ۬لنِّسَآءِ** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 12448 | 4:129 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لنِّسَآءِ** qalun,warsh  ·  **اَ۬لنِّسَآءِ** duri  ·  **ࡱ۬لنِّسَآءِ** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 12553 | 4:135 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 12568 | 4:135 | `الهوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الهوٮى` ibn-wardan,ibn-jammaz | **ٱلۡهَوَىٰٓ** hafs,shubah  ·  **ٱلۡهَوَىٰ** bazzi  ·  **ࡲ۬لْهَوَىٰ** qalun  ·  **ࡲ۬لْهَوٜىٰٓ** warsh  ·  **اُ۬لۡهَوَىٰٓ** duri  ·  **ࡲ۬لۡهَوَىٰ** susi  ·  **ٱلْهَوَىٰٓ** hisham  ·  **ٱلْهَو۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْهَوَىى** ibn-wardan,ibn-jammaz  ·  **ٱلْهَوَىٰ** ruways,rawh |
| 12739 | 4:143 | `دلك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `دلكلاالى` ruways,rawh | **ذَٰلِكَ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **ذَٰلِكَلَاإِلَىٰ** ruways,rawh |
| 12742 | 4:143 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 12743 | 4:143 | `ولا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ولاالى` ruways,rawh | **وَلَآ** hafs,shubah,warsh,duri  ·  **وَلَا** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **وَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **وَلَاإِلَىٰ** ruways,rawh |
| 12773 | 4:145 | `الدرك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الدررك` ibn-wardan,ibn-jammaz,ruways,rawh | **ٱلدَّرۡكِ** hafs,shubah  ·  **ٱلدَّرَكِ** bazzi  ·  **ࡴ۬لدَّرَكِ** qalun,warsh  ·  **اِ۬لدَّرَكِ** duri  ·  **ࡵ۬لدَّرَكِ** susi  ·  **ٱلدَّرَكِ** hisham  ·  **ٱلدَّرْكِ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلدَّرركِ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 12814 | 4:148 | `ٮالسو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالسوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلسُّوٓءِ** hafs,shubah,bazzi  ·  **بِالسُّوٓءِ** qalun,warsh,duri,susi  ·  **بِالسُّوٓآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 12896 | 4:153 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `موسٮى` ibn-wardan,ibn-jammaz | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ibn-wardan,ibn-jammaz |
| 13086 | 4:163 | `والٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **وَالنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **وَاَلنَّبِيِّـۧنَ** duri  ·  **وَࡱلنَّبِيِّـۧنَ** susi  ·  **وَٱلنَّبِيِّٜـنَ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّٱلنَّبِيِّٜـنَ** khalaf |
| 13090 | 4:163 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 13323 | 4:175 | `الٮه` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮهرطا` ruways | **إِلَيۡهِ** hafs,shubah,duri,susi  ·  **إِلَيۡهِۦ** bazzi  ·  **إِلَيْهِ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **إِلَيْهِۜرَٰطࣰا** ruways |
| 13609 | 5:6 | `مرصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `مرصٮى` ibn-wardan,ibn-jammaz | **مَّرۡضَىٰٓ** hafs,shubah  ·  **مَرۡضَىٰ** bazzi  ·  **مَّرْضَىٰ** qalun  ·  **مَّرْضٜىٰٓ** warsh  ·  **مَّرۡضۭيٰٓ** duri  ·  **مَّرۡض۪ىٰ** susi  ·  **مَّرْضَىٰٓ** hisham  ·  **مَّرْض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مَرْضَيى** ibn-wardan,ibn-jammaz  ·  **مَّرْضَىٰ** ruways,rawh |
| 13678 | 5:8 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 13813 | 5:14 | `ٮصرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮصرٮى` ibn-wardan,ibn-jammaz | **نَصَٰرَىٰٓ** hafs,shubah,hisham  ·  **نَصَٰرَىٰ** bazzi,qalun,ruways,rawh  ·  **نَصَٰرٜىٰٓ** warsh  ·  **نَصَٰر۪يٰٓ** duri  ·  **نَصَٰرٜىٰ** susi  ·  **نَصَٰر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **نَصَٰرَىى** ibn-wardan,ibn-jammaz |
| 13825 | 5:14 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لى` ibn-wardan,ibn-jammaz | **إِلَىٰ** hafs,shubah,rawh  ·  **ࡹلَىٰ** bazzi,qalun,warsh,susi  ·  **ا۪لَىٰ** duri  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلَىٰ** ruways |
| 13872 | 5:16 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 14007 | 5:21 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 14012 | 5:22 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 14050 | 5:24 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 14061 | 5:24 | `ڡڡٮلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡڡٮا` ruways,rawh | **فَقَٰتِلَآ** hafs,shubah,warsh,duri  ·  **فَقَٰتِلَا** bazzi,qalun,susi  ·  **فَقَٰتِلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَقَٰتِلاَ** ibn-wardan,ibn-jammaz  ·  **فَقَٰتِا** ruways,rawh |
| 14069 | 5:25 | `املك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اٮٮلااملك` ruways,rawh | **أَمۡلِكُ** hafs,shubah,bazzi,duri,susi  ·  **أَمْلِكُ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **إِنِّٜيلَاأَمْلِكُ** ruways,rawh |
| 14166 | 5:31 | `ٮوٮلٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮوٮلٮٮى` ibn-wardan,ibn-jammaz | **يَٰوَيۡلَتَىٰٓ** hafs,shubah  ·  **يَٰوَيۡلَتَىٰ** bazzi,susi  ·  **يَٰوَيْلَتَىٰ** qalun,ruways,rawh  ·  **يَٰوَيْلَتٜىٰٓ** warsh  ·  **يَٰوَيۡلَتۭيٰٓ** duri  ·  **يَٰوَيْلَتَىٰٓ** hisham  ·  **يَٰوَيْلَت۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰوَيْلَتَيى** ibn-wardan,ibn-jammaz |
| 14542 | 5:46 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 14683 | 5:51 | `والٮصرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `والٮصرٮى` ibn-wardan,ibn-jammaz | **وَٱلنَّصَٰرَىٰٓ** hafs,shubah  ·  **وَٱلنَّصَٰرَىٰ** bazzi  ·  **وَالنَّصَٰرَىٰ** qalun  ·  **وَالنَّصَٰرٜىٰٓ** warsh  ·  **وَاَلنَّصَٰر۪يٰٓ** duri  ·  **وَࡱلنَّصَٰرٜىٰ** susi  ·  **وَٱلنَّصَٰرَىٰٓ** hisham  ·  **وَٱلنَّصَٰر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَٱلنَّصَٰرَىى** ibn-wardan,ibn-jammaz  ·  **وَٱلنَّصَٰرَىٰ** ruways,rawh |
| 14707 | 5:52 | `ٮحسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮحسٮى` ibn-wardan,ibn-jammaz | **نَخۡشَىٰٓ** hafs,shubah,duri  ·  **نَخۡشَىٰ** bazzi  ·  **نَخْشَىٰ** qalun,ruways,rawh  ·  **نَخْشٜىٰٓ** warsh  ·  **نَّخۡشَىٰ** susi  ·  **نَخْشَىٰٓ** hisham  ·  **نَخْش۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **نَخْشَيى** ibn-wardan,ibn-jammaz |
| 14727 | 5:53 | `وٮڡول` hafs,shubah,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮڡول` bazzi,qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **وَيَقُولُ** hafs,shubah,khalaf,khallad,abu-al-harith,ishaq  ·  **يَقُولُ** bazzi,qalun,warsh,hisham,ibn-wardan,ibn-jammaz  ·  **وَيَقُولَ** duri,susi,ruways,rawh |
| 14730 | 5:53 | `اهولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اهولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَهَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **أَهَٰؤُلَآءِ** bazzi,qalun,susi  ·  **أَهَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 14746 | 5:54 | `ٮرٮد` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرٮدد` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **يَرۡتَدَّ** hafs,shubah,bazzi,duri,susi  ·  **يَّرْتَدِدْ** qalun,warsh  ·  **يَرْتَدِدْ** hisham,ibn-wardan,ibn-jammaz  ·  **يَّرْتَدَّ** khalaf  ·  **يَرْتَدَّ** khallad,abu-al-harith,ruways,rawh,ishaq |
| 14883 | 5:60 | `سوا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سواا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **سَوَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **سَوَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 14957 | 5:64 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لى` ibn-wardan,ibn-jammaz | **إِلَىٰ** hafs,shubah,rawh  ·  **ࡹلَىٰ** bazzi,qalun,warsh,susi  ·  **ا۪لَىٰ** duri  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلَىٰ** ruways |
| 15097 | 5:70 | `ٮهوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮهوٮى` ibn-wardan,ibn-jammaz | **تَهۡوَىٰٓ** hafs,shubah,duri  ·  **تَهۡوَىٰ** bazzi,susi  ·  **تَهْوَىٰ** qalun,ruways,rawh  ·  **تَهْوٜىٰٓ** warsh  ·  **تَهْوَىٰٓ** hisham  ·  **تَهْو۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَهْوَىى** ibn-wardan,ibn-jammaz |
| 15250 | 5:77 | `سوا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سواا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **سَوَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **سَوَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 15345 | 5:83 | `ٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرٮى` ibn-wardan,ibn-jammaz | **تَرَىٰٓ** hafs,shubah,hisham  ·  **تَرَىٰ** bazzi,qalun,ruways,rawh  ·  **تَرٜىٰٓ** warsh  ·  **تَر۪يٰٓ** duri  ·  **تَرٜىٰ** susi  ·  **تَر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَرَىى** ibn-wardan,ibn-jammaz |
| 15704 | 5:101 | `اسٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اسٮاں` ibn-wardan,ibn-jammaz | **أَشۡيَآءَ** hafs,shubah,bazzi,duri,susi  ·  **أَشْيَآءَ** qalun  ·  **ࡰشْيَآءَ** warsh  ·  **أَشْيَآءَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **أَشْيَآءَن** ibn-wardan,ibn-jammaz |
| 15849 | 5:107 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 15874 | 5:108 | `ادٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ادٮٮى` ibn-wardan,ibn-jammaz | **أَدۡنَىٰٓ** hafs,shubah,duri  ·  **أَدۡنَىٰ** bazzi,susi  ·  **أَدْنَىٰ** qalun,ruways,rawh  ·  **أَدْنٜىٰٓ** warsh  ·  **أَدْنَيٰٓ** hisham  ·  **أَدْن۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أَدْنَيى** ibn-wardan,ibn-jammaz |
| 15976 | 5:111 | `الحوارٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الحوارٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡحَوَارِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لْحَوَارِيِّۑنَ** qalun,warsh  ·  **اَ۬لۡحَوَارِيِّـۧنَ** duri  ·  **ࡱ۬لۡحَوَارِيِّـۧنَ** susi  ·  **ٱلْحَوَارِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 16032 | 5:114 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 16200 | 6:2 | `ڡصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡصٮى` ibn-wardan,ibn-jammaz | **قَضَىٰٓ** hafs,shubah,duri,hisham  ·  **قَضَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **قَضٜىٰٓ** warsh  ·  **قَض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **قَضَيى** ibn-wardan,ibn-jammaz |
| 16526 | 6:24 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 16577 | 6:27 | `ٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرٮى` ibn-wardan,ibn-jammaz | **تَرَىٰٓ** hafs,shubah,hisham  ·  **تَرَىٰ** bazzi,qalun,ruways,rawh  ·  **تَرٜىٰٓ** warsh  ·  **تَر۪يٰٓ** duri  ·  **تَرٜىٰ** susi  ·  **تَر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَرَىى** ibn-wardan,ibn-jammaz |
| 16618 | 6:30 | `ٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرٮى` ibn-wardan,ibn-jammaz | **تَرَىٰٓ** hafs,shubah,hisham  ·  **تَرَىٰ** bazzi,qalun,ruways,rawh  ·  **تَرٜىٰٓ** warsh  ·  **تَر۪يٰٓ** duri  ·  **تَرٜىٰ** susi  ·  **تَر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَرَىى** ibn-wardan,ibn-jammaz |
| 16640 | 6:31 | `ٮلڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮلڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِلِقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِلِقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 16668 | 6:32 | `وللدار` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ولدار` hisham | **وَلَلدَّارُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وَلَدَارُ** hisham  ·  **وَّلَلدَّارُ** khalaf  ·  **وَلَلدَّارُ** khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 16699 | 6:34 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 16726 | 6:35 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 16760 | 6:37 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 16804 | 6:39 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `علٮرط` ruways | **عَلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **عَلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَىٰۜرَٰطࣲ** ruways |
| 16836 | 6:42 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 16841 | 6:42 | `ٮالٮاسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالٮاساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلۡبَأۡسَآءِ** hafs,shubah,bazzi  ·  **بِالْبَأْسَآءِ** qalun,warsh  ·  **بِالۡبَأۡسَآءِ** duri  ·  **بِالۡبَاسَآءِ** susi  ·  **بِالْبَأْسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **بِالْبَاسَآآءِ** ibn-wardan,ibn-jammaz |
| 16842 | 6:42 | `والصرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والصراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلضَّرَّآءِ** hafs,shubah,bazzi  ·  **وَالضَّرَّآءِ** qalun,warsh  ·  **وَاَلضَّرَّآءِ** duri  ·  **وَࡱلضَّرَّآءِ** susi  ·  **وَٱلضَّرَّآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 16869 | 6:44 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 16967 | 6:50 | `ٮوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮوحٮى` ibn-wardan,ibn-jammaz | **يُوحَىٰٓ** hafs,shubah,duri,hisham  ·  **يُوحَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **يُوحٜىٰٓ** warsh  ·  **يُوح۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يُوحَيى** ibn-wardan,ibn-jammaz |
| 17023 | 6:53 | `اهولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اهولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَهَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **أَهَٰؤُلَآءِ** bazzi,qalun,susi  ·  **أَهَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 17165 | 6:60 | `لٮڡصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لٮڡصٮى` ibn-wardan,ibn-jammaz | **لِيُقۡضَىٰٓ** hafs,shubah,duri  ·  **لِيُقۡضَىٰ** bazzi,susi  ·  **لِيُقْضَىٰ** qalun,ruways,rawh  ·  **لِيُقْضٜىٰٓ** warsh  ·  **لِيُقْضَىٰٓ** hisham  ·  **لِيُقْض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **لِيُقْضَيى** ibn-wardan,ibn-jammaz |
| 17216 | 6:63 | `اٮحٮٮا` hafs,shubah,khalaf,khallad,abu-al-harith,ishaq  ·  `اٮحٮٮٮا` bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh | **أَنجَىٰنَا** hafs,shubah  ·  **أَنجَيۡتَنَا** bazzi,duri,susi  ·  **أَنجَيْتَنَا** qalun,hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **ࡰنجَيْتَنَا** warsh  ·  **أَنج۪ينَا** khalaf,khallad,abu-al-harith,ishaq |
| 17576 | 6:83 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساں` ibn-wardan,ibn-jammaz | **نَّشَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **نَّشَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **نَّشَآءُِنَّ** ibn-wardan,ibn-jammaz |
| 17602 | 6:85 | `وركرٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `وركرٮاا` ruways,rawh | **وَزَكَرِيَّا** hafs  ·  **وَزَكَرِيَّآءَ** shubah,bazzi,qalun,warsh,duri,susi  ·  **وَزَكَرِيَّاءَ** hisham  ·  **وَزَكَرِيَّا** khalaf,khallad,abu-al-harith,ishaq  ·  **وَزَكَرِيَّآءَ** ibn-wardan,ibn-jammaz  ·  **وَزَكَرِيَّااءَ** ruways,rawh |
| 17623 | 6:87 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 17651 | 6:89 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 17881 | 6:99 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 18335 | 6:124 | `رسالٮه` hafs,bazzi  ·  `رسلٮه` shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **رِسَالَتَهُۥ** hafs,bazzi  ·  **رِسَٰلَٰتِهِۦ** shubah,qalun,warsh,duri,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **رِّسَٰلَٰتِهِۦ** susi  ·  **رِسََٰلَتِهِۦ** khalaf,abu-al-harith,ishaq |
| 18375 | 6:126 | `وهدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `وهدارط` ruways | **وَهَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **وَهَٰذَاۜرَٰطُ** ruways |
| 18734 | 6:144 | `اد` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `د` ibn-wardan,ibn-jammaz | **إِذۡ** hafs,shubah  ·  **ࡹذۡ** bazzi,susi  ·  **ࡹذْ** qalun,warsh  ·  **ا۪ذۡ** duri  ·  **إِذْ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ذْ** ibn-wardan,ibn-jammaz  ·  **ٱذْ** ruways |
| 18985 | 6:153 | `هدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `هدارطى` ruways | **هَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **هَٰذَاۜرَٰطِي** ruways |
| 19015 | 6:154 | `ٮلڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮلڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِلِقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِلِقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 19151 | 6:161 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 19257 | 7:3 | `ٮدكروں` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮٮدكروں` hisham | **تَذَكَّرُونَ** hafs  ·  **تَذَّكَّرُونَ** shubah,bazzi,qalun,warsh,duri,susi  ·  **يَتَذَكَّرُونَ** hisham  ·  **تَذَكَّرُونَ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَذَّكَّرُونَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 19382 | 7:16 | `لهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `لهمرطك` ruways | **لَهُمۡ** hafs,shubah,duri,susi  ·  **لَهُمُۥ** bazzi  ·  **لَهُمْ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **لَهُمۥُ** ibn-wardan,ibn-jammaz  ·  **لَهُمْۜرَٰطَكَ** ruways |
| 19527 | 7:26 | `الٮڡوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `االٮڡوى` abu-al-harith | **ٱلتَّقۡوَىٰ** hafs,shubah,bazzi  ·  **ࡰ۬لتَّقْوَىٰ** qalun  ·  **ࡰ۬لتَّقْوٜىٰ** warsh  ·  **اُ۬لتَّقۡوۭيٰ** duri  ·  **ࡲ۬لتَّقۡو۪ىٰ** susi  ·  **ٱلتَّقْوَىٰ** hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **ٱلتَّقْو۪ىٰ** khalaf,khallad,ishaq  ·  **ٱٱلتَّقْو۪ىٰ** abu-al-harith |
| 19697 | 7:34 | `ٮسٮاحروں` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮسٮحروں` qalun,warsh,ibn-wardan,ibn-jammaz | **يَسۡتَأۡخِرُونَ** hafs,shubah,bazzi,duri  ·  **يَسْتَـْٔخِرُونَ** qalun  ·  **يَسْتَٰخِرُونَ** warsh,ibn-wardan,ibn-jammaz  ·  **يَسۡتَاخِرُونَ** susi  ·  **يَسْتَأْخِرُونَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 19745 | 7:37 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 19762 | 7:37 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 19785 | 7:38 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 19794 | 7:38 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 19831 | 7:40 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡲ۬لسَّمَآءِ** qalun,warsh,susi  ·  **اُ۬لسَّمَآءِ** duri  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 19885 | 7:43 | `وما` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ما` hisham | **وَمَا** hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **مَا** hisham |
| 19905 | 7:44 | `وٮادى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وٮادٮى` ibn-wardan,ibn-jammaz | **وَنَادَىٰٓ** hafs,shubah,duri,hisham  ·  **وَنَادَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **وَنَادٜىٰٓ** warsh  ·  **وَنَاد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَنَادَىى** ibn-wardan,ibn-jammaz |
| 19948 | 7:46 | `ٮعرڡوں` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮعرڡوٮلا` khalaf | **يَعۡرِفُونَ** hafs,shubah,bazzi,duri,susi  ·  **يَعْرِفُونَ** qalun,warsh,hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّعْرِفُونَُلا** khalaf |
| 19974 | 7:48 | `وٮادى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وٮادٮى` ibn-wardan,ibn-jammaz | **وَنَادَىٰٓ** hafs,shubah,duri,hisham  ·  **وَنَادَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **وَنَادٜىٰٓ** warsh  ·  **وَنَاد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَنَادَىى** ibn-wardan,ibn-jammaz |
| 19988 | 7:49 | `اهولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اهولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَهَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **أَهَٰؤُلَآءِ** bazzi,qalun,susi  ·  **أَهَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 20003 | 7:50 | `وٮادى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وٮادٮى` ibn-wardan,ibn-jammaz | **وَنَادَىٰٓ** hafs,shubah,duri,hisham  ·  **وَنَادَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **وَنَادٜىٰٓ** warsh  ·  **وَنَاد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَنَادَىى** ibn-wardan,ibn-jammaz |
| 20012 | 7:50 | `الما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَآءِ** qalun,warsh  ·  **اَ۬لۡمَآءِ** duri  ·  **ࡱ۬لۡمَآءِ** susi  ·  **ٱلْمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 20153 | 7:57 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 20455 | 7:75 | `ڡال` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `وڡال` hisham | **قَالَ** hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَقَالَ** hisham |
| 20534 | 7:81 | `اٮكم` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,ruways  ·  `ااٮٮكم` hisham  ·  `ااٮكم` khalaf,khallad,abu-al-harith,rawh,ishaq | **إِنَّكُمۡ** hafs  ·  **أَءِنَّكُمۡ** shubah  ·  **أَࢇنَّكُمُۥ** bazzi  ·  **إِنَّكُمْ** qalun,warsh  ·  **أَٰ۟نَّكُمۡ** duri  ·  **أَٰࢇنَّكُمۡ** susi  ·  **أَٰآءِىنَّكُمْ** hisham  ·  **أَآءِنَّكُمْ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **إِنَّكُمۥُ** ibn-wardan,ibn-jammaz  ·  **أَءنَّكُمْ** ruways |
| 20612 | 7:86 | `ٮكل` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `ٮكلرط` ruways | **بِكُلِّ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِكُلِّ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **بِكُلِّۜرَٰطࣲ** ruways |
| 20771 | 7:94 | `ٮالٮاسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالٮاساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلۡبَأۡسَآءِ** hafs,shubah,bazzi  ·  **بِالْبَأْسَآءِ** qalun,warsh  ·  **بِالۡبَأۡسَآءِ** duri  ·  **بِالۡبَاسَآءِ** susi  ·  **بِالْبَأْسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **بِالْبَاسَآآءِ** ibn-wardan,ibn-jammaz |
| 20772 | 7:94 | `والصرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والصراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلضَّرَّآءِ** hafs,shubah,bazzi  ·  **وَالضَّرَّآءِ** qalun,warsh  ·  **وَاَلضَّرَّآءِ** duri  ·  **وَࡱلضَّرَّآءِ** susi  ·  **وَٱلضَّرَّآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 20796 | 7:96 | `الڡرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الڡرٮى` ibn-wardan,ibn-jammaz | **ٱلۡقُرَىٰٓ** hafs,shubah  ·  **ٱلۡقُرَىٰ** bazzi  ·  **ࡰ۬لْقُرَىٰ** qalun  ·  **ࡰ۬لْقُرٜىٰٓ** warsh  ·  **اَ۬لۡقُر۪يٰٓ** duri  ·  **ࡱ۬لۡقُرٜىٰ** susi  ·  **ٱلْقُرَىٰٓ** hisham  ·  **ٱلْقُر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْقُرَىى** ibn-wardan,ibn-jammaz  ·  **ٱلْقُرَىٰ** ruways,rawh |
| 20803 | 7:96 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 20813 | 7:97 | `الڡرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الڡرٮى` ibn-wardan,ibn-jammaz | **ٱلۡقُرَىٰٓ** hafs,shubah  ·  **ٱلۡقُرَىٰ** bazzi  ·  **ࡲ۬لْقُرَىٰ** qalun  ·  **ࡲ۬لْقُرٜىٰٓ** warsh  ·  **اُ۬لۡقُر۪يٰٓ** duri  ·  **ࡲ۬لۡقُرٜىٰ** susi  ·  **ٱلْقُرَىٰٓ** hisham  ·  **ٱلْقُر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْقُرَىى** ibn-wardan,ibn-jammaz  ·  **ٱلْقُرَىٰ** ruways,rawh |
| 20820 | 7:98 | `اوامں` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `او` ibn-wardan,ibn-jammaz | **أَوَأَمِنَ** hafs,shubah,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **أَوۡأَمِنَ** bazzi  ·  **أَوْأَمِنَ** qalun,hisham  ·  **أَوَࡰمِنَ** warsh  ·  **أَوْ** ibn-wardan,ibn-jammaz |
| 20823 | 7:98 | `الڡرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الڡرٮى` ibn-wardan,ibn-jammaz | **ٱلۡقُرَىٰٓ** hafs,shubah  ·  **ٱلۡقُرَىٰ** bazzi  ·  **ࡲ۬لْقُرَىٰ** qalun  ·  **ࡲ۬لْقُرٜىٰٓ** warsh  ·  **اُ۬لۡقُر۪يٰٓ** duri  ·  **ࡲ۬لۡقُرٜىٰ** susi  ·  **ٱلْقُرَىٰٓ** hisham  ·  **ٱلْقُر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْقُرَىى** ibn-wardan,ibn-jammaz  ·  **ٱلْقُرَىٰ** ruways,rawh |
| 20987 | 7:113 | `اں` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,ruways  ·  `ااٮں` hisham  ·  `ااں` khalaf,khallad,abu-al-harith,rawh,ishaq | **إِنَّ** hafs,bazzi,qalun,warsh  ·  **أَءِنَّ** shubah  ·  **أَٰ۟نَّ** duri  ·  **أَٰࢇنَّ** susi  ·  **أَٰآءِىنَّ** hisham  ·  **أَآءِنَّ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **إِنَّ** ibn-wardan,ibn-jammaz  ·  **أَءنَّ** ruways |
| 21000 | 7:115 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 21022 | 7:117 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `موسٮى` ibn-wardan,ibn-jammaz | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ibn-wardan,ibn-jammaz |
| 21312 | 7:139 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 21399 | 7:143 | `دكا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `دكاا` khallad | **دَكࣰّا** hafs,shubah,bazzi,susi  ·  **دَكّاࣰ** qalun,warsh  ·  **دَكّٗا** duri  ·  **دَكࣰّا** hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **دَكَّاءَ** khalaf,abu-al-harith,ishaq  ·  **دَكَّااءَ** khallad |
| 21418 | 7:144 | `ٮرسلٮى` hafs,shubah,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,ishaq  ·  `ٮرسالٮى` bazzi,qalun,warsh,ibn-wardan,ibn-jammaz,rawh | **بِرِسَٰلَٰتِي** hafs,shubah,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,ishaq  ·  **بِرِسَالَتِي** bazzi,ibn-wardan,ibn-jammaz,rawh  ·  **بِرِسَالَتِے** qalun,warsh |
| 21485 | 7:147 | `ولڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ولڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَلِقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وَلِقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 21840 | 7:161 | `ٮعڡر` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮعڡدر` hisham | **نَّغۡفِرۡ** hafs,shubah,bazzi  ·  **تُغْفَرْ** qalun,warsh,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **نَّغۡفِر** duri,susi  ·  **تُغْفدرْ** hisham  ·  **نَّغْفِرْ** khalaf,khallad,abu-al-harith,ishaq |
| 21858 | 7:162 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 21917 | 7:165 | `السو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسُّوٓءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسُّوٓءِ** qalun,warsh  ·  **اِ۬لسُّوٓءِ** duri  ·  **ࡵ۬لسُّوٓءِ** susi  ·  **ٱلسُّوٓآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 22311 | 7:188 | `السو` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `السوں` ibn-wardan,ibn-jammaz | **ٱلسُّوٓءُ** hafs,shubah,bazzi  ·  **ࡰ۬لسُّوٓءُ** qalun,warsh  ·  **اَ۬لسُّوٓءُ** duri  ·  **ࡱ۬لسُّوٓءُ** susi  ·  **ٱلسُّوٓءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلسُّوٓءُِنْ** ibn-wardan,ibn-jammaz |
| 22427 | 7:196 | `ولٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ولى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَلِـِّۧيَ** hafs,shubah,bazzi,duri,susi  ·  **وَلِيِّيَ** qalun,warsh  ·  **وَلِـِّٜيَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 22693 | 8:11 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 22886 | 8:24 | `المر` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `المرا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡمَرۡءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَرْءِ** qalun,warsh  ·  **اَ۬لۡمَرۡءِ** duri  ·  **ࡱ۬لۡمَرۡءِ** susi  ·  **ٱلْمَرْآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 23009 | 8:32 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 23202 | 8:42 | `حى` hafs,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `حٮى` shubah,bazzi,qalun,warsh | **حَيَّ** hafs,duri,susi  ·  **حَـِۧيَ** shubah,bazzi  ·  **حَـۑِيَ** qalun  ·  **حَيِيَ** warsh  ·  **حَىَّ** hisham,khalaf,khallad,abu-al-harith  ·  **حَـِيَ** ibn-wardan,ibn-jammaz,ruways,rawh  ·  **حَـِىَ** ishaq |
| 23334 | 8:49 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 23549 | 8:64 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّٰأَيُّهَا** khalaf |
| 23557 | 8:65 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 23650 | 8:70 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّٰأَيُّهَا** khalaf |
| 24171 | 9:23 | `اولٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اولٮاں` ibn-wardan,ibn-jammaz | **أَوۡلِيَآءَ** hafs,shubah,bazzi,duri,susi  ·  **أَوْلِيَآءَ** qalun,warsh  ·  **أَوْلِيَآءَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **أَوْلِيَآءَنِ** ibn-wardan,ibn-jammaz |
| 24292 | 9:28 | `اں` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ں` ibn-wardan,ibn-jammaz | **إِنَّ** hafs,shubah  ·  **ࡹنَّ** bazzi,qalun,warsh,susi  ·  **ا۪نَّ** duri  ·  **إِنَّ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **نَّ** ibn-wardan,ibn-jammaz  ·  **ٱنَّ** ruways |
| 24702 | 9:47 | `ولاوصعوا` hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ولااوصعوا` duri,susi | **وَلَأَوۡضَعُواْ** hafs,shubah,bazzi  ·  **وَلَأَوْضَعُواْ** qalun,warsh,hisham,khallad,abu-al-harith,ishaq  ·  **وَلَأَاْوۡضَعُواْ** duri,susi  ·  **وَّلَأَوْضَعُواْ** khalaf  ·  **وَلأََوْضَعُواْ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 24904 | 9:60 | `للڡڡرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `للڡڡراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **لِلۡفُقَرَآءِ** hafs,shubah,bazzi,duri,susi  ·  **لِلْفُقَرَآءِ** qalun,warsh  ·  **لِلْفُقَرَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 25165 | 9:73 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 25483 | 9:91 | `الصعڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الصعڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلضُّعَفَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لضُّعَفَآءِ** qalun,warsh  ·  **اَ۬لضُّعَفَآءِ** duri  ·  **ࡱ۬لضُّعَفَآءِ** susi  ·  **ٱلضُّعَفَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 25795 | 9:107 | `والدٮں` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الدٮں` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **وَٱلَّذِينَ** hafs,shubah,bazzi  ·  **ࡴ۬لذِينَ** qalun,warsh  ·  **وَاَلَّذِينَ** duri  ·  **وَࡱلَّذِينَ** susi  ·  **ٱلَّذِينَ** hisham,ibn-wardan,ibn-jammaz  ·  **وَّٱلَّذِينَ** khalaf  ·  **وَٱلَّذِينَ** khallad,abu-al-harith,ruways,rawh,ishaq |
| 26466 | 10:11 | `لڡصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `لڡصٮى` ruways,rawh | **لَقُضِيَ** hafs,shubah,bazzi,qalun,warsh,duri,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **لَّقُضِيَ** susi  ·  **لَقَضَىٰٓ** hisham  ·  **لَقَضَيى** ruways,rawh |
| 26612 | 10:18 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 26688 | 10:22 | `ٮسٮركم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮٮسركم` hisham,ibn-wardan,ibn-jammaz | **يُسَيِّرُكُمۡ** hafs,shubah,duri,susi  ·  **يُسَيِّرُكُمُۥ** bazzi  ·  **يُسَيِّرُكُمْ** qalun,warsh  ·  **يَنشُرُكُمْ** hisham  ·  **يُسَيِّٜرُكُمْ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَنشُرُكُمۥُ** ibn-wardan,ibn-jammaz |
| 26759 | 10:24 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 26802 | 10:25 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮسالى` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,duri,susi  ·  **يَّشَآءُ** qalun,warsh  ·  **يَشَآءُ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَّشَآءُ** khalaf  ·  **يَشَآءُِلَىٰ** ibn-wardan,ibn-jammaz |
| 26803 | 10:25 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,rawh  ·  **ࡹِلَىٰ** bazzi,qalun,warsh,susi  ·  **اِ۪لَىٰ** duri  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلَىٰۜرَٰطࣲ** ruways |
| 26897 | 10:31 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 26979 | 10:35 | `ٮهدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ٮهدٮى` khalaf,abu-al-harith,ishaq | **يَهِدِّيٓ** hafs  ·  **يِهِدِّيٓ** shubah  ·  **يَهَدِّي** bazzi  ·  **يَه۬دِّے** qalun  ·  **يَهَدِّےٓ** warsh  ·  **يَه۬دِّيٓ** duri  ·  **يَه۬دِّي** susi  ·  **يَهَدِّٜىٓ** hisham  ·  **يَهْدِىي** khalaf,abu-al-harith,ishaq  ·  **يَهْدِىٓ** khallad  ·  **يَهْدِّٜى** ibn-wardan,ibn-jammaz  ·  **يَهِدِّٜى** ruways,rawh |
| 27135 | 10:45 | `ٮلڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮلڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِلِقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِلِقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 27379 | 10:61 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 27445 | 10:66 | `سركا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `سركاں` ibn-wardan,ibn-jammaz | **شُرَكَآءَ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **شُرَكَآءَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **شُرَكَآءَن** ibn-wardan,ibn-jammaz |
| 27556 | 10:72 | `احرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `احرٮى` khalaf,abu-al-harith,ishaq | **أَجۡرِيَ** hafs,duri,susi  ·  **أَجۡرِيٓ** shubah  ·  **أَجۡرِي** bazzi  ·  **أَجْرِيَ** qalun  ·  **ࡰجْرِيَ** warsh  ·  **أَجْرِىَ** hisham,ibn-wardan,ibn-jammaz  ·  **أَجْرِىي** khalaf,abu-al-harith,ishaq  ·  **أَجْرِىٓ** khallad  ·  **أَجْرِى** ruways,rawh |
| 28007 | 10:103 | `ٮٮح` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮٮٮح` ibn-wardan,ibn-jammaz | **نُنجِ** hafs,abu-al-harith,ruways,rawh  ·  **نُنَجِّ** shubah,bazzi,qalun,warsh,duri,susi  ·  **نُنَجِّٜ** hisham,khalaf,khallad,ishaq  ·  **نُننجِّٜ** ibn-wardan,ibn-jammaz |
| 28018 | 10:104 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡا` ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَلا** ibn-wardan,ibn-jammaz  ·  **فَا** ruways,rawh |
| 28038 | 10:105 | `للدٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `للد` khalaf,abu-al-harith | **لِلدِّينِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **لِلدِّينِ** hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **لِلد** khalaf,abu-al-harith |
| 28146 | 11:3 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **ࡴلَىٰٓ** warsh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 28216 | 11:7 | `الما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَآءِ** qalun,warsh  ·  **اَ۬لۡمَآءِ** duri  ·  **ࡱ۬لۡمَآءِ** susi  ·  **ٱلْمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 28240 | 11:8 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 28435 | 11:18 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 28595 | 11:29 | `احرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `احرٮى` abu-al-harith,ishaq | **أَجۡرِيَ** hafs,duri,susi  ·  **أَجۡرِيٓ** shubah  ·  **أَجۡرِي** bazzi  ·  **أَجْرِيَ** qalun  ·  **ࡰجْرِيَ** warsh  ·  **أَجْرِىَ** hisham,ibn-wardan,ibn-jammaz  ·  **أَجْرِىٓ** khalaf,khallad  ·  **أَجْرِىي** abu-al-harith,ishaq  ·  **أَجْرِى** ruways,rawh |
| 28934 | 11:49 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَنۢبَآءِ** hafs,shubah,bazzi,qalun,duri,susi  ·  **ࡰنۢبَآءِ** warsh  ·  **أَنۢبَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 28974 | 11:51 | `احرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `احرٮى` khalaf,abu-al-harith,ishaq | **أَجۡرِيَ** hafs,duri,susi  ·  **أَجۡرِيٓ** shubah  ·  **أَجۡرِي** bazzi  ·  **أَجْرِيَ** qalun,hisham,ibn-wardan,ibn-jammaz  ·  **ࡰجْرِيَ** warsh  ·  **أَجْرِيي** khalaf,abu-al-harith,ishaq  ·  **أَجْرِيٓ** khallad  ·  **أَجْرِي** ruways,rawh |
| 29051 | 11:56 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `علٮرط` ruways | **عَلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **عَلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَىٰۜرَٰطࣲ** ruways |
| 29293 | 11:71 | `ورا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَرَآءِ** hafs,shubah  ·  **وَرَآࢇ** bazzi  ·  **وَّرَآࢇ** qalun  ·  **وَّرَآءِ** warsh  ·  **وَرَآ** duri  ·  **وَرَا** susi  ·  **وَرَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّرَآآءِ** khalaf |
| 29294 | 11:71 | `اسحٯ` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `سحٯ` ibn-wardan,ibn-jammaz | **إِسۡحَٰقَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْحَٰقَ** qalun,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **اسْحَٰقَ** warsh  ·  **سْحَٰقَ** ibn-wardan,ibn-jammaz  ·  **ٱسْحَٰقَ** ruways |
| 29298 | 11:72 | `الد` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `االد` hisham | **ءَأَلِدُ** hafs,shubah,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءَࡶلِدُ** bazzi  ·  **ءَٰࡶلِدُ** qalun,susi  ·  **ءَالِدُ** warsh  ·  **ءَٰا۬لِدُ** duri  ·  **ءَاالِدُ** hisham  ·  **ءٱلِدُ** ibn-wardan,ibn-jammaz  ·  **ءَٱلِدُ** ruways |
| 29376 | 11:78 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 29423 | 11:81 | `ڡاسر` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡااسر` ibn-wardan,ibn-jammaz | **فَأَسۡرِ** hafs,shubah,duri,susi  ·  **فَٱسۡرِ** bazzi  ·  **فَاسْرِ** qalun,warsh  ·  **فَأَسْرِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **فَااسْرِ** ibn-wardan,ibn-jammaz |
| 29530 | 11:87 | `ٮسوا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮسواٮك` ibn-wardan,ibn-jammaz | **نَشَٰٓؤُاْ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **نَشَٰؤُاْ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **نَشَٰؤُاِْنَّكَ** ibn-wardan,ibn-jammaz |
| 29717 | 11:100 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَنۢبَآءِ** hafs,shubah,bazzi,qalun,duri,susi  ·  **ࡰنۢبَآءِ** warsh  ·  **أَنۢبَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 29994 | 11:120 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَنۢبَآءِ** hafs,shubah,bazzi,qalun,duri,susi  ·  **ࡰنۢبَآءِ** warsh  ·  **أَنۢبَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 30371 | 12:24 | `اٮه` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮه` ibn-wardan,ibn-jammaz | **إِنَّهُۥ** hafs,shubah  ·  **ࡹنَّهُۥ** bazzi,qalun,warsh,susi  ·  **ا۪نَّهُۥ** duri  ·  **إِنَّهُۥ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **نَّهُۥ** ibn-wardan,ibn-jammaz  ·  **ٱنَّهُۥ** ruways |
| 30612 | 12:38 | `اٮاى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَابَآءِيٓ** hafs,shubah  ·  **ءَابَآءِيَ** bazzi,qalun,warsh,duri,susi  ·  **ءَابَآآءِىَ** hisham,ibn-wardan,ibn-jammaz  ·  **ءَابَآآءِىٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ءَابَآآءِى** ruways,rawh |
| 30636 | 12:39 | `ٮصحٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮصٮحٮى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **يَٰصَٰحِبَيِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **يَٰصَيحِبَيِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 30677 | 12:41 | `ٮصحٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮصٮحٮى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **يَٰصَٰحِبَيِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **يَٰصَيحِبَيِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 30783 | 12:47 | `داٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `دااٮا` khalaf,abu-al-harith,ishaq | **دَأَبࣰا** hafs  ·  **دَأۡبࣰا** shubah,bazzi  ·  **دَأْباࣰ** qalun,warsh  ·  **دَأۡبٗا** duri  ·  **دَابࣰا** susi,ibn-wardan,ibn-jammaz  ·  **دَأْبࣰا** hisham,ruways,rawh  ·  **دَاْأبࣰا** khalaf,abu-al-harith,ishaq  ·  **دَاْبࣰا** khallad |
| 30888 | 12:53 | `ٮالسو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالسوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلسُّوٓءِ** hafs,shubah  ·  **بِٱلسُّوِّ** bazzi  ·  **بِالسُّوِّ** qalun  ·  **بِالسُّوٓءِ** warsh  ·  **بِالسُّوٓ** duri  ·  **بِالسُّو** susi  ·  **بِالسُّوٓآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 30944 | 12:58 | `احوه` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حوه` ibn-wardan,ibn-jammaz | **إِخۡوَةُ** hafs,shubah  ·  **ࡹخۡوَةُ** bazzi,susi  ·  **ࡹخْوَةُ** qalun,warsh  ·  **ا۪خۡوَةُ** duri  ·  **إِخْوَةُ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **خْوَةُ** ibn-wardan,ibn-jammaz  ·  **ٱخْوَةُ** ruways |
| 31218 | 12:76 | `وعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وِعَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وِعَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 31223 | 12:76 | `وعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وِعَآءِ** hafs,shubah,bazzi,duri,susi  ·  **وِّعَآءِ** qalun,warsh  ·  **وِعَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وِّٜعَآآءِ** khalaf |
| 31472 | 12:90 | `اٮك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `ااٮك` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِنَّكَ** hafs,shubah  ·  **إِنَّكَ** bazzi  ·  **أَٰࢇنَّكَ** qalun,susi  ·  **أَࢇنَّكَ** warsh  ·  **أَٰ۟نَّكَ** duri  ·  **أَٰءِٰٰنَّكَ** hisham  ·  **أَآءِنَّكَ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **إِنَّكَ** ibn-wardan,ibn-jammaz  ·  **أَءنَّكَ** ruways |
| 31636 | 12:100 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساٮه` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **يَشَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَشَآءُِنَّهُۥ** ibn-wardan,ibn-jammaz |
| 31664 | 12:102 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَنۢبَآءِ** hafs,shubah,bazzi,qalun,duri,susi  ·  **ࡰنۢبَآءِ** warsh  ·  **أَنۢبَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 31780 | 12:110 | `ڡٮحى` hafs,shubah,bazzi,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ڡٮٮحى` qalun,warsh,khallad | **فَنُجِّيَ** hafs,shubah  ·  **فَنُـۨجِي** bazzi,duri,susi  ·  **فَنُنجِے** qalun,warsh  ·  **فَنُجِّٜيَ** hisham,ruways,rawh  ·  **فَنُۨجِي** khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **فَنُنجِي** khallad |
| 31850 | 13:2 | `ٮلڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮلڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِلِقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِلِقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 31908 | 13:5 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi,warsh  ·  **أَٰࢇذَا** qalun,susi  ·  **أَٰ۟ذَا** duri  ·  **إِذَا** hisham,ibn-wardan,ibn-jammaz  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَءذَا** ruways |
| 31911 | 13:5 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun  ·  **ࡴنَّا** warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَٰءِٰٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ruways,rawh  ·  **أَٰءنَّا** ibn-wardan,ibn-jammaz |
| 32076 | 13:14 | `الما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَآءِ** qalun,warsh  ·  **اَ۬لۡمَآءِ** duri  ·  **ࡱ۬لۡمَآءِ** susi  ·  **ٱلْمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 32146 | 13:17 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 32387 | 13:30 | `اله` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `رٮٮلااله` ruways,rawh | **إِلَٰهَ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **رَبِّٜيلَاإِلَٰهَ** ruways,rawh |
| 32678 | 14:1 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطِ** ruways |
| 33122 | 14:24 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33222 | 14:32 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33266 | 14:35 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اٮرهم` hisham | **إِبۡرَٰهِيمُ** hafs,shubah,bazzi,duri,susi  ·  **إِبْرَٰهِيمُ** qalun,warsh,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **إِبْرَٰهَٰٰمُ** hisham |
| 33335 | 14:38 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33348 | 14:39 | `الدعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الدعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلدُّعَآءِ** hafs,shubah,bazzi  ·  **ࡲ۬لدُّعَآءِ** qalun,warsh,susi  ·  **اُ۬لدُّعَآءِ** duri  ·  **ٱلدُّعَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33357 | 14:40 | `دعا` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `دعاا` hisham,abu-al-harith,ishaq | **دُعَآءِ** hafs,shubah,qalun  ·  **دُعَآءِۦ** bazzi,warsh,duri,susi  ·  **دُعَآآءِ** hisham,abu-al-harith,ishaq  ·  **دُعَآءِۦ** khalaf,khallad,ibn-wardan,ibn-jammaz,ruways,rawh |
| 33539 | 15:7 | `لوما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `لو` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **لَّوۡمَا** hafs,shubah,bazzi,duri,susi  ·  **لَّوْمَا** qalun,warsh  ·  **لَّوْ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33595 | 15:14 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33610 | 15:16 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33661 | 15:22 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33794 | 15:41 | `هدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `هدارط` ruways | **هَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **هَٰذَاۜرَٰطٌ** ruways |
| 33944 | 15:65 | `ڡاسر` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡااسر` ibn-wardan,ibn-jammaz | **فَأَسۡرِ** hafs,shubah,duri,susi  ·  **فَٱسۡرِ** bazzi  ·  **فَاسْرِ** qalun,warsh  ·  **فَأَسْرِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **فَااسْرِ** ibn-wardan,ibn-jammaz |
| 33964 | 15:66 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33973 | 15:68 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33987 | 15:71 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 34124 | 15:95 | `المسٮهرٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  `المسٮهراٮں` hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **ٱلۡمُسۡتَهۡزِءِينَ** hafs,shubah,bazzi  ·  **ࡰ۬لْمُسْتَهْزِءِينَ** qalun,warsh  ·  **اَ۬لۡمُسۡتَهۡزِءِينَ** duri  ·  **ࡱ۬لۡمُسۡتَهۡزِءِينَ** susi  ·  **ٱلْمُسْتَهْزِآءِينَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْمُسْتَهْزِينَ** ibn-wardan,ibn-jammaz |
| 34151 | 16:1 | `اٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اٮٮى` ruways,rawh | **أَتَىٰٓ** hafs,shubah,duri  ·  **أَتَىٰ** bazzi,qalun,susi  ·  **أَتٜىٰٓ** warsh  ·  **أَتَيٰٓ** hisham  ·  **أَت۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أَتَي** ibn-wardan,ibn-jammaz  ·  **أَتَيى** ruways,rawh |
| 34245 | 16:10 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 34277 | 16:12 | `مسحرٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `مسحرٮه` khallad | **مُسَخَّرَٰتُۢ** hafs  ·  **مُسَخَّرَٰتِۭ** shubah,bazzi  ·  **مُسَخَّرَٰتِۢ** qalun,warsh,duri  ·  **مُّسَخَّرَٰتِۭ** susi  ·  **مُسَخَّرَٰتُۢ** hisham  ·  **مُسَخَّرَٰتِۭ** khalaf,abu-al-harith,ishaq  ·  **مُسَخَّرَٰتةِ** khallad  ·  **مُسَخَّرَٰتَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 34449 | 16:27 | `سركاى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سركااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **شُرَكَآءِيَ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **شُرَكَآآءِيَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 34476 | 16:28 | `ٮلى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮلٮى` ruways,rawh | **بَلَىٰٓ** hafs,shubah,duri  ·  **بَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **بَلٜىٰٓ** warsh  ·  **بَلَيٰٓ** hisham  ·  **بَل۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **بَلَيى** ruways,rawh |
| 34637 | 16:37 | `ٮهدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮهدٮى` hisham,ibn-wardan,ibn-jammaz | **يَهۡدِي** hafs,shubah  ·  **يُهۡدَيٰ** bazzi  ·  **يُهْدَىٰ** qalun,ruways,rawh  ·  **يُهْدٜىٰ** warsh  ·  **يُهۡدَىٰ** duri,susi  ·  **يُهْدَىى** hisham,ibn-wardan,ibn-jammaz  ·  **يَهْدِى** khalaf,khallad,abu-al-harith,ishaq |
| 34712 | 16:43 | `ٮوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮوحٮى` ibn-wardan,ibn-jammaz | **نُّوحِيٓ** hafs  ·  **يُوحَىٰٓ** shubah,duri,hisham  ·  **يُوحَيٰ** bazzi  ·  **يُوحَىٰ** qalun,susi,ruways,rawh  ·  **يُوحٜىٰٓ** warsh  ·  **يُّوح۪ىٰٓ** khalaf  ·  **يُوح۪ىٰٓ** khallad,abu-al-harith,ishaq  ·  **يُوحَيى** ibn-wardan,ibn-jammaz |
| 34885 | 16:59 | `سو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **سُوٓءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **سُوٓآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 34924 | 16:61 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَي** ibn-wardan,ibn-jammaz  ·  **إِلَيى** ruways,rawh |
| 34955 | 16:63 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 34986 | 16:65 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 35075 | 16:70 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 35209 | 16:76 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `علٮرط` ruways | **عَلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **عَلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَىٰۜرَٰطࣲ** ruways |
| 35253 | 16:79 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 35359 | 16:86 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 35428 | 16:90 | `الڡحسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الڡحساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡفَحۡشَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لْفَحْشَآءِ** qalun,warsh  ·  **اِ۬لۡفَحۡشَآءِ** duri  ·  **ࡵ۬لۡفَحۡشَآءِ** susi  ·  **ٱلْفَحْشَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 35898 | 16:121 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 36268 | 17:20 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 36269 | 17:20 | `وهولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وهولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَهَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **وَهَٰؤُلَآءِ** bazzi,qalun,susi  ·  **وَهَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 36271 | 17:20 | `عطا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `عطاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **عَطَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **عَطَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 36418 | 17:32 | `الرٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الرٮٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **ٱلزِّنَىٰٓ** hafs,shubah  ·  **ٱلزِّنَىٰ** bazzi  ·  **ࡲ۬لزِّنَىٰ** qalun,susi  ·  **ࡲ۬لزِّنٜىٰٓ** warsh  ·  **اُ۬لزِّنَىٰٓ** duri  ·  **ٱلزِّٜنَيٰٓ** hisham  ·  **ٱلزِّٜن۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلزِّٜنَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 36512 | 17:39 | `اوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `اوحٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **أَوۡحَىٰٓ** hafs,shubah,duri  ·  **أَوۡحَىٰ** bazzi,susi  ·  **أَوْحَىٰ** qalun  ·  **أَوْحٜىٰٓ** warsh  ·  **أَوْحَىٰٓ** hisham  ·  **أَوْح۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أَوْحَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 36617 | 17:46 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 36630 | 17:47 | `ٮحوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ٮحوٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **نَجۡوَىٰٓ** hafs,shubah  ·  **نَجۡوَىٰ** bazzi  ·  **نَجْوَىٰ** qalun  ·  **نَجْوٜىٰٓ** warsh  ·  **نَجۡوۭيٰٓ** duri  ·  **نَجۡو۪ىٰ** susi  ·  **نَجْوَىٰٓ** hisham  ·  **نَجْو۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **نَجْوَىى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 36649 | 17:49 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi,warsh  ·  **أَٰࢇذَا** qalun,susi  ·  **أَٰ۟ذَا** duri  ·  **إِذَا** hisham,ibn-wardan,ibn-jammaz  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَءذَا** ruways |
| 36653 | 17:49 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun  ·  **ࡴنَّا** warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَٰءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ruways,rawh  ·  **أَٰءنَّا** ibn-wardan,ibn-jammaz |
| 36683 | 17:51 | `عسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `عسٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **عَسَىٰٓ** hafs,shubah,duri,hisham  ·  **عَسَىٰ** bazzi,qalun,susi  ·  **عَسٜىٰٓ** warsh  ·  **عَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **عَسَىى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 36735 | 17:55 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 37037 | 17:75 | `لادڡٮك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `لاادڡٮك` khalaf | **لَّأَذَقۡنَٰكَ** hafs,shubah,bazzi,duri,susi  ·  **لَّأَذَقْنَٰكَ** qalun,warsh  ·  **لَّأَذَقْنَٰكَ** hisham,khallad,abu-al-harith,ishaq  ·  **لَّاَأذَقْنَٰكَ** khalaf  ·  **لأََّذَقْنَٰكَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 37092 | 17:79 | `عسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `عسٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **عَسَىٰٓ** hafs,shubah,duri,hisham  ·  **عَسَىٰ** bazzi,qalun,susi  ·  **عَسٜىٰٓ** warsh  ·  **عَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **عَسَىى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 37198 | 17:88 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 37221 | 17:89 | `ڡاٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡاٮٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **فَأَبَىٰٓ** hafs,shubah,duri  ·  **فَأَبَىٰ** bazzi,qalun,susi  ·  **فَأَبٜىٰٓ** warsh  ·  **فَأَبَيٰٓ** hisham  ·  **فَأَب۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **فَأَبَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 37268 | 17:93 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 37277 | 17:93 | `ڡل` hafs,shubah,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ڡال` bazzi,hisham | **قُلۡ** hafs,shubah,duri,susi  ·  **قَالَ** bazzi,hisham  ·  **قُلْ** qalun,warsh,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 37292 | 17:94 | `الهدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الهدٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **ٱلۡهُدَىٰٓ** hafs,shubah  ·  **ٱلۡهُدَىٰ** bazzi  ·  **ࡲ۬لْهُدَىٰ** qalun  ·  **ࡲ۬لْهُدٜىٰٓ** warsh  ·  **اُ۬لۡهُدَىٰٓ** duri  ·  **ࡲ۬لۡهُدَىٰ** susi  ·  **ٱلْهُدَىٰٓ** hisham  ·  **ٱلْهُد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْهُدَىى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 37311 | 17:95 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 37358 | 17:98 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi,warsh  ·  **أَٰࢇذَا** qalun,susi  ·  **أَٰ۟ذَا** duri  ·  **إِذَا** hisham,ibn-wardan,ibn-jammaz  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَءذَا** ruways |
| 37362 | 17:98 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun  ·  **ࡴنَّا** warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَٰءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ruways,rawh  ·  **أَٰءنَّا** ibn-wardan,ibn-jammaz |
| 37375 | 17:99 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 37397 | 17:100 | `لامسكٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لاامسكٮم` khalaf,ibn-wardan,ibn-jammaz | **لَّأَمۡسَكۡتُمۡ** hafs,shubah,duri,susi  ·  **لَّأَمۡسَكۡتُمُۥ** bazzi  ·  **لَّأَمْسَكْتُمْ** qalun,warsh  ·  **لَّأَمْسَكْتُمْ** hisham,khallad,abu-al-harith,ishaq  ·  **لَّاَأمْسَكْتُمْ** khalaf  ·  **لَّاَأمْسَكْتُمۥُ** ibn-wardan,ibn-jammaz  ·  **لأََّمْسَكْتُمْ** ruways,rawh |
| 37426 | 17:102 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh  ·  **هَٰؤُلَآࢇ** bazzi,qalun  ·  **هَٰٓؤُلَآ** duri  ·  **هَٰؤُلَا** susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 37605 | 18:6 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 37657 | 18:11 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 37702 | 18:15 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 37873 | 18:21 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 37893 | 18:22 | `رٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `رٮٮى` ibn-wardan,ibn-jammaz | **رَّبِّيٓ** hafs,shubah  ·  **رَّبِّيَ** bazzi,qalun,warsh,duri,susi  ·  **رَّبِّٜيٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **رَّبِّٜيي** ibn-wardan,ibn-jammaz  ·  **رَّبِّٜي** ruways,rawh |
| 37927 | 18:24 | `عسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `عسٮى` ibn-wardan,ibn-jammaz | **عَسَىٰٓ** hafs,shubah,duri,hisham  ·  **عَسَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَسٜىٰٓ** warsh  ·  **عَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **عَسَىى** ibn-wardan,ibn-jammaz |
| 38139 | 18:36 | `مٮها` hafs,shubah,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `مٮهما` bazzi,qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **مِّنۡهَا** hafs,shubah,duri,susi  ·  **مِّنۡهُمَا** bazzi  ·  **مِّنْهُمَا** qalun,warsh  ·  **مِّٜنْهُمَا** hisham,ibn-wardan,ibn-jammaz  ·  **مِّٜنْهَا** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 38163 | 18:38 | `ٮرٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرٮٮى` ibn-wardan,ibn-jammaz | **بِرَبِّيٓ** hafs,shubah  ·  **بِرَبِّيَ** bazzi,qalun,warsh,duri,susi  ·  **بِرَبِّٜيٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **بِرَبِّٜيي** ibn-wardan,ibn-jammaz  ·  **بِرَبِّٜي** ruways,rawh |
| 38185 | 18:40 | `رٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `رٮٮى` ibn-wardan,ibn-jammaz | **رَبِّيٓ** hafs,shubah  ·  **رَبِّيَ** bazzi,qalun,warsh,duri,susi  ·  **رَبِّٜيٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **رَبِّٜيي** ibn-wardan,ibn-jammaz  ·  **رَبِّٜي** ruways,rawh |
| 38195 | 18:40 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 38224 | 18:42 | `ٮرٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرٮٮى` ibn-wardan,ibn-jammaz | **بِرَبِّيٓ** hafs,shubah  ·  **بِرَبِّيَ** bazzi,qalun,warsh,duri,susi  ·  **بِرَبِّٜيٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **بِرَبِّٜيي** ibn-wardan,ibn-jammaz  ·  **بِرَبِّٜي** ruways,rawh |
| 38254 | 18:45 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 38378 | 18:52 | `سركاى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سركااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **شُرَكَآءِيَ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **شُرَكَآآءِىَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 38448 | 18:56 | `هروا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `هرا` ibn-wardan,ibn-jammaz | **هُزُوࣰا** hafs  ·  **هُزُؤࣰا** shubah,bazzi,susi,hisham,abu-al-harith,ruways,rawh  ·  **هُزُؤاࣰ** qalun,warsh  ·  **هُزُؤٗا** duri  ·  **هُزْؤࣰا** khalaf,khallad,ishaq  ·  **هُزࣰُٔا** ibn-wardan,ibn-jammaz |
| 38827 | 18:85 | `ڡاٮٮع` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡااٮٮع` ibn-wardan,ibn-jammaz,ruways,rawh | **فَأَتۡبَعَ** hafs,shubah  ·  **فَٱتَّبَعَ** bazzi  ·  **فَاتَّبَعَ** qalun,warsh  ·  **فَاَتَّبَعَ** duri,susi  ·  **فَأَتْبَعَ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَااتَّبَعَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 38880 | 18:89 | `اٮٮع` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ااٮٮع` ibn-wardan,ibn-jammaz,ruways,rawh | **أَتۡبَعَ** hafs,shubah  ·  **ٱتَّبَعَ** bazzi  ·  **ࡰٜتَّبَعَ** qalun,warsh  ·  **اَ۪تَّبَعَ** duri  ·  **ࡱٜتَّبَعَ** susi  ·  **أَتْبَعَ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ااتَّبَعَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 38904 | 18:92 | `اٮٮع` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ااٮٮع` ibn-wardan,ibn-jammaz,ruways,rawh | **أَتۡبَعَ** hafs,shubah  ·  **ٱتَّبَعَ** bazzi  ·  **ࡰٜتَّبَعَ** qalun,warsh  ·  **اَ۪تَّبَعَ** duri  ·  **ࡱٜتَّبَعَ** susi  ·  **أَتْبَعَ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ااتَّبَعَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 38940 | 18:95 | `مكٮى` hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `مكٮٮى` bazzi | **مَكَّنِّي** hafs,shubah,duri,susi  ·  **مَكَّنَنِي** bazzi  ·  **مَكَّنِّے** qalun,warsh  ·  **مَكَّنِّٜي** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 38965 | 18:96 | `اٮوٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اٮٮوٮى` khalaf  ·  `ااٮٮوٮى` khallad | **ءَاتُونِيٓ** hafs,duri,hisham,abu-al-harith,ishaq  ·  **ٱءۡتُونِيٓ** shubah  ·  **ءَاتُونِي** bazzi,susi,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **ءَاتُونِے** qalun  ·  **ءَاتُونِےٓ** warsh  ·  **ٱئْتُونِي** khalaf  ·  **اائْتُونِيٓ** khallad |
| 39028 | 18:102 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮا` ibn-wardan,ibn-jammaz | **إِنَّآ** hafs,shubah  ·  **ࡹنَّا** bazzi,qalun,susi  ·  **ࡹنَّآ** warsh  ·  **ا۪نَّآ** duri  ·  **إِنَّآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **نَّا** ibn-wardan,ibn-jammaz  ·  **ٱنَّا** ruways  ·  **إِنَّا** rawh |
| 39135 | 19:2 | `ركرٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ركرٮاا` ibn-wardan,ibn-jammaz,ruways,rawh | **زَكَرِيَّآ** hafs  ·  **زَكَرِيَّآءَ** shubah,bazzi,qalun,warsh,duri,susi  ·  **زَكَرِيَّاءَ** hisham  ·  **زَكَرِيَّآ** khalaf,khallad,abu-al-harith,ishaq  ·  **زَكَرِيَّااءَ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 39136 | 19:3 | `اد` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `د` ibn-wardan,ibn-jammaz | **إِذۡ** hafs,shubah  ·  **ࡹذۡ** bazzi,susi  ·  **ࡹذْ** qalun,warsh  ·  **ا۪ذۡ** duri  ·  **إِذْ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ذْ** ibn-wardan,ibn-jammaz  ·  **ٱذْ** ruways |
| 39159 | 19:5 | `وراى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ورااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَرَآءِي** hafs,shubah,duri,susi  ·  **وَرَآءِيَ** bazzi  ·  **وَّرَآءِے** qalun,warsh  ·  **وَرَآآءِى** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّرَآآءِى** khalaf |
| 39176 | 19:7 | `ٮركرٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮركرٮاا` ruways,rawh | **يَٰزَكَرِيَّآ** hafs  ·  **يَٰزَكَرِيَّآءُ** shubah,bazzi,qalun,warsh,duri,susi  ·  **يَٰزَكَرِيَّاءُ** hisham  ·  **يَّٰزَكَرِيَّآ** khalaf  ·  **يَٰزَكَرِيَّآ** khallad,abu-al-harith,ishaq  ·  **يَٰزَكَرِيَّا** ibn-wardan,ibn-jammaz  ·  **يَٰزَكَرِيَّااءُ** ruways,rawh |
| 39234 | 19:11 | `ڡاوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡاوحٮى` ruways,rawh | **فَأَوۡحَىٰٓ** hafs,shubah,duri  ·  **فَأَوۡحَىٰ** bazzi,susi  ·  **فَأَوْحَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **فَأَوْحٜىٰٓ** warsh  ·  **فَأَوْحَىٰٓ** hisham  ·  **فَأَوْحىٰٓ** khalaf,abu-al-harith,ishaq  ·  **فَأَوْح۪ىٰٓ** khallad  ·  **فَأَوْحَيى** ruways,rawh |
| 39302 | 19:19 | `لاهٮ` hafs,shubah,bazzi,qalun,warsh,duri,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `لاٮهٮ` susi | **لِأَهَبَ** hafs,shubah,bazzi,qalun,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **لِاَهَبَ** warsh  ·  **لِاَ۬هَبَ** duri  ·  **لِاَۧهَبَ** susi  ·  **لاهَبَ** ruways,rawh |
| 39469 | 19:35 | `ڡصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡصٮى` ruways,rawh | **قَضَىٰٓ** hafs,shubah,duri,hisham  ·  **قَضَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **قَضٜىٰٓ** warsh  ·  **قَض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **قَضَيى** ruways,rawh |
| 39476 | 19:36 | `واں` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `وااں` ruways | **وَإِنَّ** hafs,shubah  ·  **وَأَنَّ** bazzi,qalun,warsh,duri,susi  ·  **وَإِنَّ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **وأَنَّ** ibn-wardan,ibn-jammaz  ·  **وَأأنَّ** ruways |
| 39481 | 19:36 | `هدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `هدارط` ruways | **هَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **هَّٰذَا** susi  ·  **هَٰذَاۜرَٰطࣱ** ruways |
| 39559 | 19:43 | `اهدك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `اهدكرطا` ruways | **أَهۡدِكَ** hafs,shubah,bazzi,duri,susi  ·  **أَهْدِكَ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **أَهْدِكَۜرَٰطࣰا** ruways |
| 39612 | 19:48 | `عسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `عسٮى` ruways,rawh | **عَسَىٰٓ** hafs,shubah,duri,hisham  ·  **عَسَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَسٜىٰٓ** warsh  ·  **عَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **عَسَىى** ruways,rawh |
| 39615 | 19:48 | `ٮدعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮدعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِدُعَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِدُعَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 39644 | 19:51 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah  ·  **مُوسَىٰ** bazzi,qalun  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوسَيٰٓ** hisham  ·  **مُوس۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيٰ** ibn-wardan,ibn-jammaz  ·  **مُوسَيى** ruways,rawh |
| 39702 | 19:58 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 39811 | 19:66 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi,warsh  ·  **أَٰࢇذَا** qalun,susi  ·  **أَٰ۟ذَا** duri  ·  **أَءِٰذَا** hisham  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءذَا** ibn-wardan,ibn-jammaz  ·  **أَءذَا** ruways |
| 39904 | 19:75 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `حٮٮى` ruways,rawh | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّىٰ** ibn-wardan,ibn-jammaz  ·  **حَتَّيى** ruways,rawh |
| 40096 | 20:2 | `لٮسڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `لٮسڡٮى` ruways,rawh | **لِتَشۡقَىٰٓ** hafs,shubah  ·  **لِتَشۡقَىٰ** bazzi  ·  **لِتَشْقَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **لِتَشْقٜىٰٓ** warsh  ·  **لِتَشۡقۭيٰٓ** duri  ·  **لِتَشۡق۪ىٰ** susi  ·  **لِتَشْقَيٰٓ** hisham  ·  **لِتَشْق۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **لِتَشْقَيى** ruways,rawh |
| 40141 | 20:9 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ruways,rawh |
| 40163 | 20:11 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮموسٮى` ruways,rawh | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَّٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ruways,rawh |
| 40172 | 20:12 | `طوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `طوٮى` ruways,rawh | **طُوࣰى** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **طُوَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **طُوٜىٰ** warsh  ·  **طُوۭيٰ** duri  ·  **طُو۪ىٰ** susi  ·  **طُوَىى** ruways,rawh |
| 40174 | 20:13 | `احٮرٮك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `احٮرٮٮك` khallad | **ٱخۡتَرۡتُكَ** hafs,shubah,bazzi  ·  **ࡰٜخْتَرْتُكَ** qalun,warsh  ·  **اَ۪خۡتَرۡتُكَ** duri  ·  **ࡱٜخۡتَرۡتُكَ** susi  ·  **ٱخْتَرْتُكَ** hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **ٱخْتَرْنَٰٰكَ** khalaf  ·  **ٱخْتَرْننٰكَ** khallad |
| 40177 | 20:13 | `ٮوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮوحٮى` ruways,rawh | **يُوحَىٰٓ** hafs,shubah,hisham  ·  **يُوحَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **يُوحٜىٰٓ** warsh  ·  **يُوحۭيٰٓ** duri  ·  **يُوح۪ىٰ** susi  ·  **يُوح۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يُوحَيى** ruways,rawh |
| 40306 | 20:37 | `احرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `احرٮى` ruways,rawh | **أُخۡرَىٰٓ** hafs,shubah  ·  **أُخۡرَىٰ** bazzi  ·  **أُخْرَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **ࡳخْرٜىٰٓ** warsh  ·  **أُخۡر۪يٰٓ** duri  ·  **أُخۡرٜىٰ** susi  ·  **أُخْرَىٰٓ** hisham  ·  **أُخْر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أُخْرَىى** ruways,rawh |
| 40309 | 20:38 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 40312 | 20:38 | `ٮوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮوحٮى` ruways,rawh | **يُوحَىٰٓ** hafs,shubah,hisham  ·  **يُوحَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **يُوحٜىٰٓ** warsh  ·  **يُوحۭيٰٓ** duri  ·  **يُوح۪ىٰ** susi  ·  **يُوح۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يُوحَيى** ruways,rawh |
| 40345 | 20:40 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 40429 | 20:47 | `الهدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الهدٮى` ruways,rawh | **ٱلۡهُدَىٰٓ** hafs,shubah  ·  **ٱلۡهُدَىٰ** bazzi  ·  **ࡰ۬لْهُدَىٰ** qalun  ·  **ࡰ۬لْهُدٜىٰٓ** warsh  ·  **اَ۬لۡهُدۭيٰٓ** duri  ·  **ࡱ۬لۡهُد۪ىٰ** susi  ·  **ٱلْهُدَىٰٓ** hisham  ·  **ٱلْهُد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْهُدَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلْهُدَىى** ruways,rawh |
| 40480 | 20:53 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 40590 | 20:65 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮموسٮى` ruways,rawh | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ruways,rawh |
| 40705 | 20:73 | `واٮڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `واٮڡٮى` ruways,rawh | **وَأَبۡقَىٰٓ** hafs,shubah  ·  **وَأَبۡقَىٰ** bazzi  ·  **وَأَبْقَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **وَأَبْقٜىٰٓ** warsh  ·  **وَأَبۡقۭيٰٓ** duri  ·  **وَأَبۡق۪ىٰ** susi  ·  **وَأَبْقَيٰٓ** hisham  ·  **وَّأَبْق۪يٰٓ** khalaf  ·  **وَأَبْق۪يٰٓ** khallad,abu-al-harith,ishaq  ·  **وَأَبْقَيى** ruways,rawh |
| 40744 | 20:77 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ruways,rawh |
| 40746 | 20:77 | `اسر` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ااسر` ibn-wardan,ibn-jammaz | **أَسۡرِ** hafs,shubah,duri,susi  ·  **ٱسۡرِ** bazzi  ·  **ࡴٜسْرِ** qalun,warsh  ·  **أَسْرِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ااسْرِ** ibn-wardan,ibn-jammaz |
| 40819 | 20:84 | `اولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أُوْلَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **أُوْلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 40820 | 20:84 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 40836 | 20:86 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ruways,rawh |
| 40991 | 20:97 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **ࡴلَىٰٓ** warsh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 41019 | 20:99 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَنۢبَآءِ** hafs,shubah,bazzi,qalun,duri,susi  ·  **ࡰنۢبَآءِ** warsh  ·  **أَنۢبَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 41136 | 20:112 | `ٮحاڡ` hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮحڡ` bazzi | **يَخَافُ** hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَخَفۡ** bazzi |
| 41164 | 20:114 | `ٮڡصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اٮڡصى` ruways,rawh | **يُقۡضَىٰٓ** hafs,shubah,duri  ·  **يُقۡضَىٰ** bazzi,susi  ·  **يُّقْضَىٰ** qalun  ·  **يُّقْضٜىٰٓ** warsh  ·  **يُقْضَىٰٓ** hisham  ·  **يُّقْض۪ىٰٓ** khalaf  ·  **يُقْض۪ىٰٓ** khallad,abu-al-harith,ishaq  ·  **يُقْضَىٰ** ibn-wardan,ibn-jammaz  ·  **أَنَّقْضِي** ruways,rawh |
| 41173 | 20:115 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 41202 | 20:117 | `ڡٮسڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡٮسڡٮى` ruways,rawh | **فَتَشۡقَىٰٓ** hafs,shubah  ·  **فَتَشۡقَىٰ** bazzi  ·  **فَتَشْقَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **فَتَشْقٜىٰٓ** warsh  ·  **فَتَشۡقۭيٰٓ** duri  ·  **فَتَشۡق۪ىٰ** susi  ·  **فَتَشْقَيٰٓ** hisham  ·  **فَتَشْق۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **فَتَشْقَيى** ruways,rawh |
| 41240 | 20:121 | `وعصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `وعصٮى` ruways,rawh | **وَعَصَىٰٓ** hafs,shubah,duri,hisham  ·  **وَعَصَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **وَعَصٜىٰٓ** warsh  ·  **وَعَص۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَعَصَيى** ruways,rawh |
| 41307 | 20:127 | `واٮڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `واٮڡٮى` ruways,rawh | **وَأَبۡقَىٰٓ** hafs,shubah  ·  **وَأَبۡقَىٰ** bazzi  ·  **وَأَبْقَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **وَأَبْقٜىٰٓ** warsh  ·  **وَأَبۡقۭيٰٓ** duri  ·  **وَأَبۡق۪ىٰ** susi  ·  **وَأَبْقَيٰٓ** hisham  ·  **وَأَبْق۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَأَبْقَيى** ruways,rawh |
| 41423 | 20:135 | `الصرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الرط` ruways | **ٱلصِّرَٰطِ** hafs,shubah,bazzi  ·  **ࡲ۬لصِّرَٰطِ** qalun,warsh,susi  ·  **اُ۬لصِّرَٰطِ** duri  ·  **ٱلصِّرَٰطِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ٱلۜرَٰطِ** ruways |
| 41460 | 21:4 | `ڡال` hafs,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡل` shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh | **قَالَ** hafs,khalaf,khallad,abu-al-harith,ishaq  ·  **قُل** shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh |
| 41465 | 21:4 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 41725 | 21:30 | `اولم` hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `الم` bazzi | **أَوَلَمۡ** hafs,shubah,duri,susi  ·  **أَلَمۡ** bazzi  ·  **أَوَلَمْ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 41737 | 21:30 | `الما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَآءِ** qalun,warsh  ·  **اَ۬لۡمَآءِ** duri  ·  **ࡱ۬لۡمَآءِ** susi  ·  **ٱلْمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 41895 | 21:44 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 41919 | 21:45 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `دا` ibn-wardan,ibn-jammaz | **إِذَا** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹذَا** bazzi,qalun,warsh,susi  ·  **ا۪ذَا** duri  ·  **ذَا** ibn-wardan,ibn-jammaz  ·  **ٱذَا** ruways |
| 42068 | 21:62 | `اٮٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااٮٮ` hisham | **ءَأَنتَ** hafs,shubah,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءَࡶنتَ** bazzi  ·  **ءَٰࡶنتَ** qalun,susi  ·  **ءَآنتَ** warsh  ·  **ءَٰا۬نتَ** duri  ·  **ءَاانتَ** hisham  ·  **ءٱنتَ** ibn-wardan,ibn-jammaz  ·  **ءَٱنتَ** ruways |
| 42096 | 21:65 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 42346 | 21:88 | `ٮحى` hafs,shubah,bazzi,duri,susi,hisham,khalaf  ·  `ٮٮحى` qalun,warsh,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **نُـۨجِي** hafs,bazzi,duri,susi  ·  **نُجِّي** shubah  ·  **نُنجِے** qalun,warsh  ·  **نُجِّٜي** hisham  ·  **نُۨجِي** khalaf  ·  **نُنجِي** khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 42348 | 21:89 | `وركرٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `وركرٮاا` ruways,rawh | **وَزَكَرِيَّآ** hafs  ·  **وَزَكَرِيَّآءَ** shubah,bazzi,qalun,warsh,duri,susi  ·  **وَزَكَرِيَّاءَ** hisham  ·  **وَزَكَرِيَّآ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَزَكَرِيَّآءَ** ibn-wardan,ibn-jammaz  ·  **وَزَكَرِيَّااءَ** ruways,rawh |
| 42349 | 21:89 | `اد` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `د` ibn-wardan,ibn-jammaz | **إِذۡ** hafs,shubah  ·  **ࡹذۡ** bazzi,susi  ·  **ࡹذْ** qalun,warsh  ·  **ا۪ذۡ** duri  ·  **إِذْ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ذْ** ibn-wardan,ibn-jammaz  ·  **ٱذْ** ruways |
| 42464 | 21:99 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 42680 | 22:5 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮسالى` ibn-wardan,ibn-jammaz | **نَشَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **نَشَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **نَشَآءُِلَىٰ** ibn-wardan,ibn-jammaz |
| 42681 | 22:5 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah  ·  **ࡹِلَىٰ** bazzi,qalun,susi  ·  **ࡹِلَىٰٓ** warsh  ·  **اِ۪لَىٰٓ** duri  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلَيى** ruways  ·  **إِلَيى** rawh |
| 42696 | 22:5 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 42860 | 22:15 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 43004 | 22:24 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطِ** ruways |
| 43125 | 22:31 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 43147 | 22:33 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 43432 | 22:52 | `ٮمٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮمٮٮى` ruways,rawh | **تَمَنَّىٰٓ** hafs,shubah,duri  ·  **تَمَنَّىٰ** bazzi,qalun,susi  ·  **تَمَنّٜىٰٓ** warsh  ·  **تَمَنَّىٰٓ** hisham  ·  **تَمَنّٜ۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَمَنَّىٰ** ibn-wardan,ibn-jammaz  ·  **تَمَنَّيى** ruways,rawh |
| 43483 | 22:54 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 43601 | 22:63 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 43699 | 22:70 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 43983 | 23:18 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 44181 | 23:33 | `ٮلڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮلڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِلِقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِلِقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 44524 | 23:73 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 44533 | 23:74 | `الصرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الرط` ruways | **ٱلصِّرَٰطِ** hafs,shubah,bazzi  ·  **ࡴ۬لصِّرَٰطِ** qalun,warsh  ·  **اِ۬لصِّرَٰطِ** duri  ·  **ࡵ۬لصِّرَٰطِ** susi  ·  **ٱلصِّرَٰطِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ٱلۜرَٰطِ** ruways |
| 44600 | 23:82 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi,warsh  ·  **أَٰࢇذَا** qalun,susi  ·  **أَٰ۟ذَا** duri  ·  **إِذَا** hisham,ibn-wardan,ibn-jammaz  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَءذَا** ruways |
| 44605 | 23:82 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun  ·  **ࡴنَّا** warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَٰءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ruways,rawh  ·  **أَٰءنَّا** ibn-wardan,ibn-jammaz |
| 44641 | 23:87 | `لله` hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الله` duri,susi  ·  `االله` ruways,rawh | **لِلَّهِ** hafs,shubah,bazzi  ·  **لِلهِ** qalun,warsh  ·  **اَ۬للَّهُ** duri  ·  **ࡱ۬للَّهُ** susi  ·  **لَِِّله** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لِِله** ibn-wardan,ibn-jammaz  ·  **االَّلُه** ruways,rawh |
| 44660 | 23:89 | `لله` hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الله` duri,susi  ·  `االله` ruways,rawh | **لِلَّهِ** hafs,shubah,bazzi  ·  **لِلهِ** qalun,warsh  ·  **اَ۬للَّهُ** duri  ·  **ࡱ۬للَّهُ** susi  ·  **لَِِّله** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لِِله** ibn-wardan,ibn-jammaz  ·  **االَّلُه** ruways,rawh |
| 44712 | 23:95 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 44739 | 23:99 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 44747 | 23:100 | `لعلى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لعلٮى` ibn-wardan,ibn-jammaz | **لَعَلِّيٓ** hafs,shubah  ·  **لَعَلِّيَ** bazzi,qalun,warsh,duri,susi  ·  **لَعَلِّٜيَ** hisham  ·  **لَعَلِّٜيٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **لَعَلِّٜيي** ibn-wardan,ibn-jammaz  ·  **لَعَلِّٜي** ruways,rawh |
| 44853 | 23:112 | `ڡل` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡال` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **قَٰلَ** hafs,shubah,duri,susi,ruways,rawh,ishaq  ·  **قُلۡ** bazzi  ·  **قَالَ** qalun,warsh,hisham,ibn-wardan,ibn-jammaz  ·  **قُلْ** khalaf,khallad,abu-al-harith |
| 44868 | 23:114 | `ڡل` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡال` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **قَٰلَ** hafs,shubah,bazzi,duri,susi,ruways,rawh,ishaq  ·  **قَالَ** qalun,warsh,hisham,ibn-wardan,ibn-jammaz  ·  **قُلْ** khalaf,khallad,abu-al-harith |
| 45010 | 24:6 | `سهدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `سهدالا` ibn-wardan,ibn-jammaz | **شُهَدَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **شُهَدَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **شُهَدَآءُِلا** ibn-wardan,ibn-jammaz |
| 45107 | 24:13 | `ٮالسهدا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالسهداا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلشُّهَدَآءِ** hafs,shubah,bazzi  ·  **بِالشُّهَدَآءِ** qalun,warsh,duri,susi  ·  **بِالشُّهَدَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 45216 | 24:21 | `ٮالڡحسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالڡحساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلۡفَحۡشَآءِ** hafs,shubah,bazzi  ·  **بِالْفَحْشَآءِ** qalun,warsh  ·  **بِالۡفَحۡشَآءِ** duri,susi  ·  **بِالْفَحْشَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 45410 | 24:31 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَابَآءِ** hafs,shubah,bazzi,qalun,duri,susi  ·  **اٰبَآءِ** warsh  ·  **ءَابَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 45415 | 24:31 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَبۡنَآءِ** hafs,shubah,bazzi,duri,susi  ·  **أَبْنَآءِ** qalun  ·  **ࡰبْنَآءِ** warsh  ·  **أَبْنَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 45510 | 24:33 | `الٮعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡبِغَآءِ** hafs,shubah  ·  **ٱلۡبِغَآࢇ** bazzi  ·  **ࡰ۬لْبِغَآࢇ** qalun  ·  **ࡰ۬لْبِغَآءِ** warsh  ·  **اَ۬لۡبِغَآ** duri  ·  **ࡱ۬لۡبِغَا** susi  ·  **ٱلْبِغَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 45613 | 24:37 | `واٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `واٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَإِيتَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وَإِيتَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 45737 | 24:43 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 45790 | 24:45 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساں` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **يَشَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَشَآءُنَّ** ibn-wardan,ibn-jammaz |
| 45805 | 24:46 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  `لى` ibn-wardan,ibn-jammaz  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,rawh  ·  **ࡹِلَىٰ** bazzi,qalun,warsh,susi  ·  **اِ۪لَىٰ** duri  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلَىٰۜرَٰطࣲ** ruways |
| 46052 | 24:60 | `الٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنِّسَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لنِّسَآءِ** qalun,warsh  ·  **اَ۬لنِّسَآءِ** duri  ·  **ࡱ۬لنِّسَآءِ** susi  ·  **ٱلنِّٜسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 46193 | 24:63 | `كدعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `كدعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **كَدُعَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **كَدُعَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 46451 | 25:17 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 46507 | 25:20 | `ڡٮٮه` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لٮعڡٮٮه` ibn-wardan,ibn-jammaz | **فِتۡنَةً** hafs,shubah,bazzi,duri,susi  ·  **فِتْنَةً** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **لِبَعࣲْفِتْنَةً** ibn-wardan,ibn-jammaz |
| 46561 | 25:25 | `وٮرل` hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `وٮٮرل` bazzi | **وَنُزِّلَ** hafs,shubah,qalun,warsh,duri,susi  ·  **وَنُنزِلُ** bazzi  ·  **وَنُزِّٜلَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 46811 | 25:48 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 46814 | 25:49 | `لٮحٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `لٮحى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **لِّنُحۡـِۧيَ** hafs,shubah,bazzi,duri,susi  ·  **لِّنُحْـۑِيَ** qalun  ·  **لِّنُحْۑِيَ** warsh  ·  **لِّٜنُحْـِيَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 46866 | 25:54 | `الما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَآءِ** qalun,warsh  ·  **اَ۬لۡمَآءِ** duri  ·  **ࡱ۬لۡمَآءِ** susi  ·  **ٱلْمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 46954 | 25:61 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 47146 | 26:4 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 47198 | 26:10 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ruways,rawh |
| 47408 | 26:41 | `اٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اٮٮں` hisham | **أَئِنَّ** hafs,shubah,warsh  ·  **أَىٜنَّ** bazzi  ·  **أَٰئِنَّ** qalun  ·  **أَٰى۪نَّ** duri  ·  **أَٰىٜنَّ** susi  ·  **أَئِىنَّ** hisham  ·  **أَئِنَّ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰئنَّ** ibn-wardan,ibn-jammaz  ·  **أَئنَّ** ruways |
| 47423 | 26:43 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُّوسَىٰٓ** hafs,shubah  ·  **مُوسَىٰ** bazzi,ibn-wardan,ibn-jammaz  ·  **مُّوسَىٰ** qalun  ·  **مُّوسٜىٰٓ** warsh  ·  **مُّوسۭيٰٓ** duri  ·  **مُّوس۪ىٰ** susi  ·  **مُّوسَىٰٓ** hisham  ·  **مُّوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُّوسَيى** ruways,rawh |
| 47468 | 26:49 | `ٮعلموں` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮعلموٮد` ruways,rawh | **تَعۡلَمُونَ** hafs,shubah,bazzi,duri,susi  ·  **تَعْلَمُونَ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **تَعْلَمُوند** ruways,rawh |
| 47496 | 26:52 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ruways,rawh |
| 47498 | 26:52 | `اسر` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ااسر` ibn-wardan,ibn-jammaz | **أَسۡرِ** hafs,shubah,duri,susi  ·  **ٱسۡرِ** bazzi  ·  **ࡴٜسْرِ** qalun,warsh  ·  **أَسْرِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ااسْرِ** ibn-wardan,ibn-jammaz |
| 47508 | 26:54 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 47535 | 26:61 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ruways,rawh |
| 47546 | 26:63 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `موسٮى` ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ruways,rawh |
| 47584 | 26:69 | `اٮرهٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرهٮم` ibn-wardan,ibn-jammaz | **إِبۡرَٰهِيمَ** hafs,shubah  ·  **ࡹبۡرَٰهِيمَ** bazzi,susi  ·  **ࡹبْرَٰهِيمَ** qalun,warsh  ·  **ا۪بۡرَٰهِيمَ** duri  ·  **إِبْرَٰهِيمَ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **بْرَٰهِيمَ** ibn-wardan,ibn-jammaz  ·  **ٱبْرَٰهِيمَ** ruways |
| 48224 | 26:187 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah  ·  **ٱلسَّمَآࢇ** bazzi  ·  **ࡰ۬لسَّمَآࢇ** qalun  ·  **ࡰ۬لسَّمَآءِ** warsh  ·  **اَ۬لسَّمَآ** duri  ·  **ࡱ۬لسَّمَا** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 48448 | 27:1 | `طس` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `طسى` khalaf,abu-al-harith,ishaq | **طسٓ** hafs,bazzi,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **طٜسٓ** shubah  ·  **طَسِٓ** qalun,warsh  ·  **ط۪سي** khalaf,abu-al-harith,ishaq  ·  **ط۪سٓ** khallad |
| 48523 | 27:9 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 48639 | 27:18 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 48700 | 27:21 | `لٮاٮٮٮى` hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `لٮاٮٮٮٮى` bazzi | **لَيَأۡتِيَنِّي** hafs,shubah,duri  ·  **لَيَأۡتِيَنَّنِي** bazzi  ·  **لَيَأْتِيَنِّے** qalun  ·  **لَيَاتِيَنِّے** warsh  ·  **لَيَاتِيَنِّي** susi  ·  **لَيَأْتِيَنِّٜي** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **لَيَاتِيَنِّٜي** ibn-wardan,ibn-jammaz |
| 48787 | 27:29 | `الملوا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الملواٮى` ibn-wardan,ibn-jammaz | **ٱلۡمَلَؤُاْ** hafs,shubah,bazzi  ·  **ࡰ۬لْمَلَؤُاْ** qalun,warsh  ·  **اَ۬لۡمَلَؤُاْ** duri  ·  **ࡱ۬لۡمَلَؤُاْ** susi  ·  **ٱلْمَلَؤُاْ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْمَلَؤُاِْنِّٜيَ** ibn-wardan,ibn-jammaz |
| 48847 | 27:35 | `ڡٮاطره` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡٮطره` qalun,warsh,ibn-wardan,ibn-jammaz | **فَنَاظِرَةُۢ** hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَنَٰظِرَةُۢ** qalun,warsh  ·  **فَنَٰظِرَةٰ** ibn-wardan,ibn-jammaz  ·  **فَنَاظِرَةٰ** ruways,rawh |
| 48858 | 27:36 | `اٮٮں` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اٮٮٮى` qalun,warsh | **ءَاتَىٰنِۦَ** hafs,duri,susi  ·  **ءَاتَىٰنِ** shubah,bazzi  ·  **ءَاتَيٰنِࣉَ** qalun  ·  **ءَاتٜيٰنِࣉَ** warsh  ·  **ءَاتَينِ** hisham,khalaf,khallad,rawh,ishaq  ·  **ءَات۪ينِ** abu-al-harith  ·  **ءَاتَينَِۦ** ibn-wardan,ibn-jammaz,ruways |
| 49170 | 27:60 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 49183 | 27:60 | `اله` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `االه` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِلَٰهࣱ** hafs,shubah  ·  **أَࢇلَٰهࣱ** bazzi,warsh  ·  **أَٰࢇلَٰهࣱ** qalun,susi  ·  **أَٰ۟لَٰهٞ** duri  ·  **أَءِٰٰلَٰهࣱ** hisham  ·  **أَآءِلَٰهࣱ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءلَٰهࣱ** ibn-wardan,ibn-jammaz  ·  **أَءلَٰهࣱ** ruways |
| 49204 | 27:61 | `اله` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `االه` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِلَٰهࣱ** hafs,shubah  ·  **أَࢇلَٰهࣱ** bazzi  ·  **أَٰࢇلَٰهࣱ** qalun,susi  ·  **ࡰࢇلَٰهࣱ** warsh  ·  **أَٰ۟لَٰهٞ** duri  ·  **أَءِٰٰلَٰهࣱ** hisham  ·  **أَآءِلَٰهࣱ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءلَٰهࣱ** ibn-wardan,ibn-jammaz  ·  **أَءلَٰهࣱ** ruways |
| 49221 | 27:62 | `اله` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `االه` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِلَٰهࣱ** hafs,shubah  ·  **أَࢇلَٰهࣱ** bazzi,warsh  ·  **أَٰࢇلَٰهࣱ** qalun,susi  ·  **أَٰ۟لَٰهٞ** duri  ·  **أَءِٰٰلَٰهࣱ** hisham  ·  **أَآءِلَٰهࣱ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءلَٰهࣱ** ibn-wardan,ibn-jammaz  ·  **أَءلَٰهࣱ** ruways |
| 49240 | 27:63 | `اله` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `االه` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِلَٰهࣱ** hafs,shubah  ·  **أَࢇلَٰهࣱ** bazzi,warsh  ·  **أَٰࢇلَٰهࣱ** qalun,susi  ·  **أَٰ۟لَٰهٞ** duri  ·  **أَءِٰٰلَٰهࣱ** hisham  ·  **أَآءِلَٰهࣱ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءلَٰهࣱ** ibn-wardan,ibn-jammaz  ·  **أَءلَٰهࣱ** ruways |
| 49255 | 27:64 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 49257 | 27:64 | `اله` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `االه` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِلَٰهࣱ** hafs,shubah  ·  **أَࢇلَٰهࣱ** bazzi,warsh  ·  **أَٰࢇلَٰهࣱ** qalun,susi  ·  **أَٰ۟لَٰهٞ** duri  ·  **أَءِٰٰلَٰهࣱ** hisham  ·  **أَآءِلَٰهࣱ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءلَٰهࣱ** ibn-wardan,ibn-jammaz  ·  **أَءلَٰهࣱ** ruways |
| 49281 | 27:66 | `ادرك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اادرك` ruways,rawh | **ٱدَّٰرَكَ** hafs,shubah  ·  **أَدۡرَكَ** bazzi,duri,susi  ·  **ࡴٜدَّٰرَكَ** qalun,warsh  ·  **ٱدَّٰرَكَ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **أَدْرَكَ** ibn-wardan,ibn-jammaz  ·  **أأدْرَكَ** ruways,rawh |
| 49297 | 27:67 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi  ·  **إِذَا** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **أَٰ۟ذَا** duri  ·  **أَٰࢇذَا** susi  ·  **أَءِٰٰذَا** hisham  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَءذَا** ruways |
| 49301 | 27:67 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `ااٮٮا` ruways | **أَئِنَّا** hafs,shubah,warsh  ·  **أَىٜنَّا** bazzi  ·  **أَٰئِنَّا** qalun  ·  **أَٰى۪نَّا** duri  ·  **أَٰىٜنَّا** susi  ·  **إِنَّنَا** hisham,abu-al-harith  ·  **أَئِنَّا** khalaf,khallad,rawh,ishaq  ·  **أَٰئنَّا** ibn-wardan,ibn-jammaz  ·  **أأئنَّا** ruways |
| 49371 | 27:75 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 49416 | 27:80 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `دا` ibn-wardan,ibn-jammaz | **إِذَا** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹذَا** bazzi,qalun,warsh,susi  ·  **ا۪ذَا** duri  ·  **ذَا** ibn-wardan,ibn-jammaz  ·  **ٱذَا** ruways |
| 49648 | 28:6 | `وٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `وٮرٮى` khalaf,abu-al-harith,ishaq | **وَنُرِيَ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وَنُرِىَ** hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **وَيَر۪ىى** khalaf,abu-al-harith,ishaq  ·  **وَيَر۪ىٰ** khallad |
| 49700 | 28:9 | `عسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `عسٮى` ibn-wardan,ibn-jammaz | **عَسَىٰٓ** hafs,shubah,duri,hisham  ·  **عَسَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَسٜىٰٓ** warsh  ·  **عَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **عَسَىى** ibn-wardan,ibn-jammaz |
| 49744 | 28:12 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 49753 | 28:13 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 49772 | 28:14 | `واسٮوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `واسٮوٮى` ibn-wardan,ibn-jammaz | **وَٱسۡتَوَىٰٓ** hafs,shubah  ·  **وَٱسۡتَوَىٰ** bazzi  ·  **وَاسْتَوَىٰ** qalun  ·  **وَاسْتَوٜىٰٓ** warsh  ·  **وَاَسۡتَوَىٰٓ** duri  ·  **وَࡱسۡتَوَىٰ** susi  ·  **وَٱسْتَوَىٰٓ** hisham  ·  **وَٱسْتَو۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَٱسْتَوَىى** ibn-wardan,ibn-jammaz  ·  **وَٱسْتَوَىٰ** ruways,rawh |
| 49851 | 28:18 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `موسٮى` ibn-wardan,ibn-jammaz | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ibn-wardan,ibn-jammaz |
| 49865 | 28:19 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 49894 | 28:20 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 49956 | 28:24 | `ٮولى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮولٮى` ibn-wardan,ibn-jammaz | **تَوَلَّىٰٓ** hafs,shubah,duri  ·  **تَوَلَّىٰ** bazzi,qalun,susi  ·  **تَوَلّٜىٰٓ** warsh  ·  **تَوَلَّيٰٓ** hisham  ·  **تَوَلّٜ۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَوَلَّيى** ibn-wardan,ibn-jammaz  ·  **تَوَلَّىٰ** ruways,rawh |
| 50012 | 28:27 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 50088 | 28:30 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,ruways,rawh  ·  **يَّٰمُوسَىٰ** qalun  ·  **يَّٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَّٰمُوس۪ىٰٓ** khalaf  ·  **يَٰمُوس۪ىٰٓ** khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 50106 | 28:31 | `ٮموسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮموسٮى` ibn-wardan,ibn-jammaz | **يَٰمُوسَىٰٓ** hafs,shubah,hisham  ·  **يَٰمُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **يَٰمُوسٜىٰٓ** warsh  ·  **يَٰمُوسۭيٰٓ** duri  ·  **يَٰمُوس۪ىٰ** susi  ·  **يَٰمُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَٰمُوسَيى** ibn-wardan,ibn-jammaz |
| 50193 | 28:37 | `وڡال` hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ڡال` bazzi | **وَقَالَ** hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **قَالَ** bazzi |
| 50231 | 28:38 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 50375 | 28:48 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `موسٮى` ibn-wardan,ibn-jammaz | **مُوسَىٰٓ** hafs,shubah  ·  **مُوسَىٰ** bazzi,qalun,ruways,rawh  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوسَيٰٓ** hisham  ·  **مُوس۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ibn-wardan,ibn-jammaz |
| 50384 | 28:48 | `سحراں` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `سحرں` qalun,warsh,ibn-wardan,ibn-jammaz | **سِحۡرَانِ** hafs,shubah  ·  **سَٰحِرَانِ** bazzi,duri,susi,hisham,ruways,rawh  ·  **سَٰحِرَٰنِ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **سِحْرَانِ** khalaf,khallad,abu-al-harith,ishaq |
| 50508 | 28:57 | `ٮحٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮحٮٮى` ibn-wardan,ibn-jammaz | **يُجۡبَىٰٓ** hafs,shubah,duri  ·  **يُجۡبَىٰ** bazzi,susi  ·  **تُجْبَىٰ** qalun,ruways  ·  **تُجْبٜىٰٓ** warsh  ·  **يُجْبَىٰٓ** hisham  ·  **يُّجْب۪ىٰٓ** khalaf  ·  **يُجْب۪ىٰٓ** khallad,abu-al-harith,ishaq  ·  **تُجْبَيى** ibn-wardan,ibn-jammaz  ·  **يُجْبَىٰ** rawh |
| 50553 | 28:59 | `الڡرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الڡرٮى` ibn-wardan,ibn-jammaz | **ٱلۡقُرَىٰٓ** hafs,shubah  ·  **ٱلۡقُرَىٰ** bazzi  ·  **ࡴ۬لْقُرَىٰ** qalun  ·  **ࡴ۬لْقُرٜىٰٓ** warsh  ·  **اِ۬لۡقُر۪يٰٓ** duri  ·  **ࡵ۬لۡقُرٜىٰ** susi  ·  **ٱلْقُرَيٰٓ** hisham  ·  **ٱلْقُر۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْقُرَيى** ibn-wardan,ibn-jammaz  ·  **ٱلْقُرَيٰ** ruways  ·  **ٱلْقُرَىٰ** rawh |
| 50569 | 28:60 | `واٮڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `واٮڡٮى` ibn-wardan,ibn-jammaz | **وَأَبۡقَىٰٓ** hafs,shubah,duri  ·  **وَأَبۡقَىٰ** bazzi,susi  ·  **وَأَبْقَىٰ** qalun  ·  **وَأَبْقٜىٰٓ** warsh  ·  **وَأَبْقَيٰٓ** hisham  ·  **وَّأَبْق۪يٰٓ** khalaf  ·  **وَأَبْق۪يٰٓ** khallad,abu-al-harith,ishaq  ·  **وَأَبْقَيى** ibn-wardan,ibn-jammaz  ·  **وَأَبْقَيٰ** ruways,rawh |
| 50593 | 28:62 | `سركاى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سركااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **شُرَكَآءِيَ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **شُرَكَآآءِىَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 50603 | 28:63 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 50647 | 28:67 | `ڡعسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡعسٮى` ibn-wardan,ibn-jammaz | **فَعَسَىٰٓ** hafs,shubah,duri,hisham  ·  **فَعَسَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **فَعَسٜىٰٓ** warsh  ·  **فَعَس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **فَعَسَىى** ibn-wardan,ibn-jammaz |
| 50745 | 28:74 | `سركاى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سركااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **شُرَكَآءِيَ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **شُرَكَآآءِىَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 50983 | 28:86 | `ٮلڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮلڡٮى` ibn-wardan,ibn-jammaz | **يُلۡقَىٰٓ** hafs,shubah,duri  ·  **يُلۡقَىٰ** bazzi,susi  ·  **يُّلْقَىٰ** qalun  ·  **يُّلْقٜىٰٓ** warsh  ·  **يُلْقَيٰٓ** hisham  ·  **يُّلْق۪يٰٓ** khalaf  ·  **يُلْق۪يٰٓ** khallad,abu-al-harith,ishaq  ·  **يُلْقَيى** ibn-wardan,ibn-jammaz  ·  **يُلْقَىٰ** ruways,rawh |
| 51415 | 29:28 | `اٮكم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮكم` khalaf,abu-al-harith,ishaq | **إِنَّكُمۡ** hafs  ·  **أَءِنَّكُمۡ** shubah  ·  **إِنَّكُمُۥ** bazzi  ·  **إِنَّكُمْ** qalun,warsh  ·  **أَٰ۟نَّكُمۡ** duri  ·  **أَٰࢇنَّكُمۡ** susi  ·  **إِنَّكُمْ** hisham,ruways,rawh  ·  **أَآءِنَّكُمْ** khalaf,abu-al-harith,ishaq  ·  **أَءِنَّكُمْ** khallad  ·  **إِنَّكُمُۥ** ibn-wardan,ibn-jammaz |
| 51510 | 29:34 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 51516 | 29:34 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 51668 | 29:45 | `الڡحسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الڡحساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡفَحۡشَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لْفَحْشَآءِ** qalun,warsh  ·  **اِ۬لۡفَحۡشَآءِ** duri  ·  **ࡵ۬لۡفَحۡشَآءِ** susi  ·  **ٱلْفَحْشَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 51712 | 29:47 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 51910 | 29:63 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 52116 | 30:10 | `السواى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `السواٮى` ibn-wardan,ibn-jammaz | **ٱلسُّوٓأَىٰٓ** hafs,shubah  ·  **ٱلسُّوٓأَىٰ** bazzi  ·  **ࡲ۬لسُّوٓأَىٰ** qalun  ·  **ࡲ۬لسُّوٓأٜىٰٓ** warsh  ·  **اُ۬لسُّوٓأۭيٰٓ** duri  ·  **ࡲ۬لسُّوٓأ۪ىٰ** susi  ·  **ٱلسُّوٓأَىٰٓ** hisham  ·  **ٱلسُّوٓأ۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلسُّوٓأَىى** ibn-wardan,ibn-jammaz  ·  **ٱلسُّوٓأَىٰ** ruways,rawh |
| 52265 | 30:24 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 52637 | 30:48 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 52668 | 30:50 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **ࡴلَىٰٓ** warsh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 52703 | 30:52 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `دا` ibn-wardan,ibn-jammaz | **إِذَا** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹذَا** bazzi,qalun,warsh,susi  ·  **ا۪ذَا** duri  ·  **ذَا** ibn-wardan,ibn-jammaz  ·  **ٱذَا** ruways |
| 52916 | 31:10 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 53099 | 31:20 | `طهره` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮعمطهره` ruways,rawh | **ظَٰهِرَةࣰ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **ظَٰهِرَةٗ** duri  ·  **نِعْمࣰَظَٰهِرَةࣰ** ruways,rawh |
| 53422 | 32:5 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah  ·  **ٱلسَّمَآࢇ** bazzi  ·  **ࡰ۬لسَّمَآࢇ** qalun  ·  **ࡰ۬لسَّمَآءِ** warsh  ·  **اَ۬لسَّمَآ** duri  ·  **ࡱ۬لسَّمَا** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 53475 | 32:10 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi,warsh  ·  **أَٰࢇذَا** qalun,susi  ·  **أَٰ۟ذَا** duri  ·  **إِذَا** hisham,ibn-wardan,ibn-jammaz  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَءذَا** ruways |
| 53479 | 32:10 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun,warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَٰءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ruways,rawh  ·  **أَٰءنَّا** ibn-wardan,ibn-jammaz |
| 53485 | 32:10 | `ٮلڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮلڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِلِقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **بِلِقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 53500 | 32:12 | `ٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮرٮى` ibn-wardan,ibn-jammaz | **تَرَىٰٓ** hafs,shubah,hisham  ·  **تَرَىٰ** bazzi,qalun,ruways,rawh  ·  **تَرٜىٰٓ** warsh  ·  **تَر۪يٰٓ** duri  ·  **تَرٜىٰ** susi  ·  **تَر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَرَىى** ibn-wardan,ibn-jammaz |
| 53705 | 32:27 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لى` ibn-wardan,ibn-jammaz | **إِلَى** hafs,shubah  ·  **ࡹلَى** bazzi,qalun,warsh,susi  ·  **ا۪لَى** duri  ·  **إِلَي** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **لَي** ibn-wardan,ibn-jammaz  ·  **ٱلَي** ruways |
| 53740 | 33:1 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 53755 | 33:2 | `ٮوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ٮوحٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **يُوحَىٰٓ** hafs,shubah,duri,hisham  ·  **يُوحَىٰ** bazzi,qalun,susi  ·  **يُوحٜىٰٓ** warsh  ·  **يُوح۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يُوحَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 53782 | 33:4 | `الى` hafs,shubah,bazzi,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` qalun,ruways,rawh | **ٱلَّٰٓـِٔي** hafs,shubah  ·  **ٱلَّـٰٓيۡ** bazzi  ·  **ࡲ۬لَّٰٓئِے** qalun  ·  **ࡲ۬لٜےْ** warsh  ·  **اُ۬لَّٰٓيۡ** duri  ·  **ࡲ۬لَّٰٓيۡ** susi  ·  **ٱلَِّٰٔي** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلَّٰٓي** ibn-wardan,ibn-jammaz  ·  **ٱلَّٰئيِ** ruways,rawh |
| 53848 | 33:6 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 53859 | 33:7 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 54214 | 33:28 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّٰأَيُّهَا** khalaf |
| 54479 | 33:40 | `الٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡰ۬لنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **اَ۬لنَّبِيِّـۧنَ** duri  ·  **ࡱ۬لنَّبِيِّـۧنَ** susi  ·  **ٱلنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 54571 | 33:50 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّٰأَيُّهَا** khalaf |
| 54605 | 33:50 | `اراد` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اراد‏` warsh | **أَرَادَ** hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **ࡰرَادَ‏** warsh |
| 54648 | 33:51 | `ادٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ادٮٮى` ruways,rawh | **أَدۡنَىٰٓ** hafs,shubah,duri  ·  **أَدۡنَىٰ** bazzi,susi  ·  **أَدْنَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **أَدْنٜىٰٓ** warsh  ·  **أَدْنَيٰٓ** hisham  ·  **أَدْن۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أَدْنَيى** ruways,rawh |
| 54668 | 33:52 | `ٮحل` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮاحل` ruways,rawh | **يَحِلُّ** hafs,shubah,bazzi,qalun,warsh  ·  **تَحِلُّ** duri,susi  ·  **يَحِلُّ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **تأحِلُّ** ruways,rawh |
| 54735 | 33:53 | `ورا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَرَآءِ** hafs,shubah,bazzi,duri,susi  ·  **وَّرَآءِ** qalun,warsh  ·  **وَرَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّرَآآءِ** khalaf |
| 54782 | 33:55 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَبۡنَآءِ** hafs,shubah  ·  **أَبۡنَآࢇ** bazzi  ·  **أَبْنَآࢇ** qalun  ·  **أَبْنَآءِ** warsh  ·  **أَبۡنَآ** duri  ·  **أَبۡنَا** susi  ·  **أَبْنَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 54785 | 33:55 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَبۡنَآءِ** hafs,shubah,bazzi,duri,susi  ·  **أَبْنَآءِ** qalun,warsh  ·  **أَبْنَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 54841 | 33:59 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّٰأَيُّهَا** khalaf |
| 54846 | 33:59 | `وٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وٮساا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَنِسَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **وَنِسَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 54853 | 33:59 | `ادٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ادٮٮى` ruways,rawh | **أَدۡنَىٰٓ** hafs,shubah,duri  ·  **أَدۡنَىٰ** bazzi,susi  ·  **أَدْنَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **أَدْنٜىٰٓ** warsh  ·  **أَدْنَيٰٓ** hisham  ·  **أَدْن۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أَدْنَيى** ruways,rawh |
| 55055 | 34:2 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 55127 | 34:6 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطِ** ruways |
| 55172 | 34:9 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 55700 | 34:40 | `اهولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اهولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **أَهَٰٓؤُلَآءِ** hafs,shubah,warsh  ·  **أَهَٰؤُلَآࢇ** bazzi,qalun  ·  **أَهَٰٓؤُلَآ** duri  ·  **أَهَٰؤُلَا** susi  ·  **أَهَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 55881 | 34:52 | `الٮٮاوس` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `الٮٮااوس` khalaf,khallad,abu-al-harith,ishaq | **ٱلتَّنَاوُشُ** hafs,bazzi  ·  **ٱلتَّنَآؤُشُ** shubah  ·  **ࡲ۬لتَّنَاوُشُ** qalun,warsh  ·  **اُ۬لتَّنَآؤُشُ** duri  ·  **ࡲ۬لتَّنَآؤُشُ** susi  ·  **ٱلتَّنَاوُشُ** hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **ٱلتَّنَااؤُشُ** khalaf,khallad,abu-al-harith,ishaq |
| 55927 | 35:1 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساں` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **يَشَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَشَآءُِنَّ** ibn-wardan,ibn-jammaz |
| 55966 | 35:3 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 56202 | 35:15 | `الڡڡرا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الڡڡرالى` ibn-wardan,ibn-jammaz | **ٱلۡفُقَرَآءُ** hafs,shubah,bazzi  ·  **ࡲ۬لْفُقَرَآءُ** qalun,warsh  ·  **اُ۬لۡفُقَرَآءُ** duri  ·  **ࡲ۬لۡفُقَرَآءُ** susi  ·  **ٱلْفُقَرَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْفُقَرَآءُِلَي** ibn-wardan,ibn-jammaz |
| 56324 | 35:27 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 56352 | 35:28 | `العلموا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `العلمواں` ibn-wardan,ibn-jammaz | **ٱلۡعُلَمَٰٓؤُاْ** hafs,shubah,bazzi  ·  **ࡴ۬لْعُلَمَٰٓؤُاْ** qalun,warsh  ·  **اِ۬لۡعُلَمَٰٓؤُاْ** duri  ·  **ࡵ۬لۡعُلَمَٰٓؤُاْ** susi  ·  **ٱلْعُلَمَٰؤُاْ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْعُلَمَٰؤُاِْنَّ** ibn-wardan,ibn-jammaz |
| 56608 | 35:43 | `السٮى` hafs,shubah,bazzi,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `السٮٮى` qalun | **ٱلسَّيِّيِٕ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّيِّئِے** qalun  ·  **ࡰ۬لسَّيِّےِٕ** warsh  ·  **اَ۬لسَّيِّيِٕ** duri  ·  **ࡱ۬لسَّيِّيِٕ** susi  ·  **ٱلسَّيِّٜيِ** hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **ٱلسَّيِّٜئْ** khalaf,khallad |
| 56612 | 35:43 | `السٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `السٮٮلا` ibn-wardan,ibn-jammaz | **ٱلسَّيِّئُ** hafs  ·  **ٱلسَّيِّئُ** shubah,bazzi  ·  **ࡲ۬لسَّيِّۓُ** qalun,warsh  ·  **اُ۬لسَّيِّئُ** duri  ·  **ࡲ۬لسَّيِّئُ** susi  ·  **ٱلسَّيِّٜئُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلسَّيِّٜئُِلَّا** ibn-wardan,ibn-jammaz |
| 56674 | 35:45 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 56691 | 36:4 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `علٮرط` ruways | **عَلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **عَلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَىٰۜرَٰطࣲ** ruways |
| 56707 | 36:7 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 56736 | 36:10 | `اٮدرٮهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااٮدرٮهم` hisham | **ءَأَنذَرۡتَهُمۡ** hafs,shubah  ·  **ءَࡶنذَرۡتَهُمُۥ** bazzi  ·  **ءَٰࡶنذَرْتَهُمْ** qalun  ·  **ءَآنذَرْتَهُمُۥٓ** warsh  ·  **ءَٰا۬نذَرۡتَهُمۡ** duri  ·  **ءَٰࡶنذَرۡتَهُمۡ** susi  ·  **ءَاانذَرْتَهُمْ** hisham  ·  **ءَأَنذَرْتَهُمْ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءٱنذَرْتَهُمۥُ** ibn-wardan,ibn-jammaz  ·  **ءَٱنذَرْتَهُمْ** ruways |
| 56828 | 36:19 | `اٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اٮٮں` hisham | **أَئِن** hafs,shubah,warsh,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَىٜن** bazzi  ·  **أَٰئِن** qalun  ·  **أَٰى۪ن** duri  ·  **أَٰىٜن** susi  ·  **أَئِىن** hisham  ·  **ءَٰٱيْن** ibn-wardan,ibn-jammaz  ·  **أَئن** ruways |
| 56859 | 36:23 | `اٮحد` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااٮحد` hisham | **ءَأَتَّخِذُ** hafs,shubah  ·  **ءَࡶتَّخِذُ** bazzi  ·  **ءَٰࡶتَّخِذُ** qalun,susi  ·  **ءَآتَّخِذُ** warsh  ·  **ءَٰا۬تَّخِذُ** duri  ·  **ءَااتَّخِذُ** hisham  ·  **ءَأَتَّخِذُ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءٱتَّخِذُ** ibn-wardan,ibn-jammaz  ·  **ءَٱتَّخِذُ** ruways |
| 56906 | 36:28 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 56970 | 36:35 | `عملٮه` hafs,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `عملٮ` shubah,khalaf,khallad,abu-al-harith,ishaq | **عَمِلَتۡهُ** hafs,duri,susi  ·  **عَمِلَتۡ** shubah  ·  **عَمِلَتۡهُۥ** bazzi  ·  **عَمِلَتْهُ** qalun,warsh,hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **عَمِلَتْ** khalaf,khallad,abu-al-harith,ishaq |
| 57210 | 36:61 | `هدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `هدارط` ruways | **هَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **هَٰذَاۜرَٰطࣱ** ruways |
| 57248 | 36:66 | `الصرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الرط` ruways | **ٱلصِّرَٰطَ** hafs,shubah,bazzi  ·  **ࡲ۬لصِّرَٰطَ** qalun,warsh,susi  ·  **اُ۬لصِّرَٰطَ** duri  ·  **ٱلصِّرَٰطَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ٱلۜرَٰطَ** ruways |
| 57486 | 37:16 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi  ·  **أَٰࢇذَا** qalun,susi  ·  **ࡰࢇذَا** warsh  ·  **أَٰ۟ذَا** duri  ·  **إِذَا** hisham  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءذَا** ibn-wardan,ibn-jammaz  ·  **أَءذَا** ruways |
| 57491 | 37:16 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun  ·  **ࡴنَّا** warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَٰءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh |
| 57493 | 37:17 | `اواٮاوٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `او` hisham | **أَوَءَابَآؤُنَا** hafs,shubah,bazzi,warsh,duri,susi  ·  **أَوْءَابَآؤُنَا** qalun  ·  **أَوْ** hisham  ·  **أَوَءَابَآؤُنَا** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **أَوْءَابَآؤُنَا** ibn-wardan,ibn-jammaz |
| 57530 | 37:23 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطِ** ruways |
| 57672 | 37:52 | `اٮك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `ااٮك` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِنَّكَ** hafs,shubah  ·  **أَࢇنَّكَ** bazzi,warsh  ·  **أَٰࢇنَّكَ** qalun,susi  ·  **أَٰ۟نَّكَ** duri  ·  **أَٰءِٰنَّكَ** hisham  ·  **أَآءِنَّكَ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءنَّكَ** ibn-wardan,ibn-jammaz  ·  **أَءنَّكَ** ruways |
| 57675 | 37:53 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi,warsh  ·  **أَٰࢇذَا** qalun,susi  ·  **أَٰ۟ذَا** duri  ·  **إِذَا** hisham,ibn-wardan,ibn-jammaz  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَءذَا** ruways |
| 57680 | 37:53 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun  ·  **ࡴنَّا** warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَٰءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ruways,rawh  ·  **أَٰءنَّا** ibn-wardan,ibn-jammaz |
| 57689 | 37:55 | `سوا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سواا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **سَوَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **سَوَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 57756 | 37:68 | `لالى` hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `لاالى` duri,susi | **لَإِلَى** hafs,shubah,bazzi,qalun,warsh  ·  **لَإِاْلَى** duri,susi  ·  **لإَُلَي** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لإَٓلَي** ibn-wardan,ibn-jammaz,ruways,rawh |
| 57763 | 37:70 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 57853 | 37:91 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz |
| 57956 | 37:109 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 57972 | 37:113 | `وعلى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وعلٮى` ibn-wardan,ibn-jammaz | **وَعَلَىٰٓ** hafs,shubah,warsh,duri  ·  **وَعَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **وَعَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **وَعَلَيى** ibn-wardan,ibn-jammaz |
| 57998 | 37:118 | `الصرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الرط` ruways | **ٱلصِّرَٰطَ** hafs,shubah,bazzi  ·  **ࡰ۬لصِّرَٰطَ** qalun,warsh  ·  **اَ۬لصِّرَٰطَ** duri  ·  **ࡱ۬لصِّرَٰطَ** susi  ·  **ٱلصِّرَٰطَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ٱلۜرَٰطَ** ruways |
| 58109 | 37:145 | `ٮالعرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالعراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلۡعَرَآءِ** hafs,shubah,bazzi  ·  **بِالْعَرَآءِ** qalun,warsh  ·  **بِالۡعَرَآءِ** duri,susi  ·  **بِالْعَرَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 58316 | 38:6 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 58394 | 38:15 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi,rawh  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh  ·  **هَٰؤُلَآࢇ** bazzi,qalun  ·  **هَٰٓؤُلَآ** duri  ·  **هَٰؤُلَا** susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,ishaq  ·  **هَٰؤُلَآءَِّ** rawh |
| 58467 | 38:22 | `سوا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سواا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **سَوَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **سَوَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 58468 | 38:22 | `الصرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الرط` ruways | **ٱلصِّرَٰطِ** hafs,shubah,bazzi  ·  **ࡴ۬لصِّرَٰطِ** qalun,warsh  ·  **اِ۬لصِّرَٰطِ** duri  ·  **ࡵ۬لصِّرَٰطِ** susi  ·  **ٱلصِّرَٰطِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ٱلۜرَٰطِ** ruways |
| 58494 | 38:24 | `الحلطا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الحلطاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡخُلَطَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْخُلَطَآءِ** qalun,warsh  ·  **اَ۬لۡخُلَطَآءِ** duri  ·  **ࡱ۬لۡخُلَطَآءِ** susi  ·  **ٱلْخُلَطَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 58836 | 38:63 | `اٮحدٮهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ااٮحدٮهم` khallad,ruways,rawh | **أَتَّخَذۡنَٰهُمۡ** hafs,shubah  ·  **أَتَّخَذۡنَٰهُمُۥ** bazzi  ·  **أَتَّخَذْنَٰهُمْ** qalun,warsh  ·  **اِ۪تَّخَذۡنَٰهُمۡ** duri  ·  **ࡵٜتَّخَذۡنَٰهُمۡ** susi  ·  **أَتَّخَذْنَٰهُمْ** hisham  ·  **ٱتَّخَذْنَٰهُمْ** khalaf,abu-al-harith,ishaq  ·  **ااتَّخَذْنَٰهُمْ** khallad,ruways,rawh  ·  **أَتَّخَذْنَٰهُمۥُ** ibn-wardan,ibn-jammaz |
| 58879 | 38:69 | `الاعلى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الاعلٮى` ibn-wardan,ibn-jammaz | **ٱلۡأَعۡلَىٰٓ** hafs,shubah  ·  **ٱلۡأَعۡلَىٰ** bazzi  ·  **ࡴ۬لْأَعْلَىٰ** qalun  ·  **ࡴ۬لَاعْلٜىٰٓ** warsh  ·  **اِ۬لۡأَعۡلَىٰٓ** duri  ·  **ࡵ۬لۡأَعۡلَىٰ** susi  ·  **ٱلْأَعْلَيٰٓ** hisham  ·  **ٱلْأَعْل۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلأَْعْلَيى** ibn-wardan,ibn-jammaz  ·  **ٱلأَْعْلَىٰ** ruways,rawh |
| 58883 | 38:70 | `ٮوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮوحٮى` ibn-wardan,ibn-jammaz | **يُوحَىٰٓ** hafs,shubah,duri,hisham  ·  **يُوحَىٰ** bazzi,susi,ruways,rawh  ·  **يُّوحَىٰ** qalun  ·  **يُّوحٜىٰٓ** warsh  ·  **يُّوح۪ىٰٓ** khalaf  ·  **يُوح۪ىٰٓ** khallad,abu-al-harith,ishaq  ·  **يُوحَيى** ibn-wardan,ibn-jammaz |
| 59036 | 39:3 | `رلڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `رلڡٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **زُلۡفَىٰٓ** hafs,shubah  ·  **زُلۡفَىٰ** bazzi  ·  **زُلْفَىٰ** qalun  ·  **زُلْفٜىٰٓ** warsh  ·  **زُلۡفۭيٰٓ** duri  ·  **زُلۡف۪ىٰ** susi  ·  **زُلْفَيٰٓ** hisham  ·  **زُلْف۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **زُلْفَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 59364 | 39:21 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 59555 | 39:34 | `حرا` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حروا` qalun,warsh,ibn-wardan,ibn-jammaz | **جَزَآءُ** hafs,shubah,bazzi,duri,susi  ·  **جَزَٰٓؤُاْ** qalun,warsh  ·  **جَزَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **جَزَٰٓؤاْ** ibn-wardan,ibn-jammaz |
| 59683 | 39:42 | `الاحرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الاحرٮى` ruways,rawh | **ٱلۡأُخۡرَىٰٓ** hafs,shubah  ·  **ٱلۡأُخۡرَىٰ** bazzi  ·  **ࡲ۬لْأُخْرَىٰ** qalun  ·  **ࡲ۬لُاخْرٜىٰٓ** warsh  ·  **اُ۬لۡأُخۡر۪يٰٓ** duri  ·  **ࡲ۬لۡأُخۡرٜىٰ** susi  ·  **ٱلأُْخْرَىٰٓ** hisham  ·  **ٱلأُْخْر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلأُْخْرَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلأُْخْرَىى** ruways,rawh |
| 59684 | 39:42 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 59766 | 39:47 | `سو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **سُوٓءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **سُوٓآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 59829 | 39:51 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 59856 | 39:53 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 59964 | 39:61 | `ٮمڡارٮهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ٮمڡاردٮهم` khalaf,abu-al-harith,ishaq | **بِمَفَازَتِهِمۡ** hafs,duri,susi  ·  **بِمَفَازَٰتِهِمۡ** shubah  ·  **بِمَفَازَتِهِمُۥ** bazzi  ·  **بِمَفَازَتِهِمْ** qalun,warsh,hisham,ruways,rawh  ·  **بِمَفَازدءتِهِمْ** khalaf,abu-al-harith,ishaq  ·  **بِمَفَازءَتِهِمْ** khallad  ·  **بِمَفَازَتِهِمۥُ** ibn-wardan,ibn-jammaz |
| 59994 | 39:64 | `ٮامروٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮامروٮٮى` hisham | **تَأۡمُرُوٓنِّيٓ** hafs,shubah,duri  ·  **تَأۡمُرُوٓنِّيَ** bazzi  ·  **تَأْمُرُونِيَ** qalun  ·  **تَامُرُونِيَ** warsh,ibn-wardan,ibn-jammaz  ·  **تَامُرُوٓنِّي** susi  ·  **تَأْمُرُونَنِيٓ** hisham  ·  **تَأْمُرُوٓنِّٜيٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَأْمُرُوٓنِّٜي** ruways,rawh |
| 60063 | 39:69 | `وحاى` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وحى` qalun,warsh,ibn-wardan,ibn-jammaz | **وَجِاْيٓءَ** hafs,shubah,bazzi,duri,susi  ·  **وَجِےٓءَ** qalun,warsh  ·  **وَجاْىٓءَ** hisham,abu-al-harith  ·  **وَجِاْىٓءَ** khalaf,khallad,rawh,ishaq  ·  **وَجِيٓءَ** ibn-wardan,ibn-jammaz  ·  **وَجاىٓءَ** ruways |
| 60064 | 39:69 | `ٮالٮٮٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالٮٮٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلنَّبِيِّـۧنَ** hafs,shubah,bazzi  ·  **بِالنَّبِيٓـِٕۑنَ** qalun,warsh  ·  **بِالنَّبِيِّـۧنَ** duri,susi  ·  **بِالنَّبِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 60065 | 39:69 | `والسهدا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والسهداا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلشُّهَدَآءِ** hafs,shubah,bazzi  ·  **وَالشُّهَدَآءِ** qalun,warsh  ·  **وَاَلشُّهَدَآءِ** duri  ·  **وَࡱلشُّهَدَآءِ** susi  ·  **وَٱلشُّهَدَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 60087 | 39:71 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `حٮٮى` ruways,rawh | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّىٰ** ibn-wardan,ibn-jammaz  ·  **حَتَّيى** ruways,rawh |
| 60131 | 39:73 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `حٮٮى` ruways,rawh | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّىٰ** ibn-wardan,ibn-jammaz  ·  **حَتَّيى** ruways,rawh |
| 60220 | 40:5 | `امه` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `امهه` khalaf,abu-al-harith,ishaq | **أُمَّةِۭ** hafs,shubah,bazzi,susi  ·  **أُمَّةِۢ** qalun,warsh,duri  ·  **أُمَّةِۭ** hisham,khallad  ·  **أُمَّةِة** khalaf,abu-al-harith,ishaq  ·  **أُمَّةِۢ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 60347 | 40:13 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 60530 | 40:26 | `اں` hafs,shubah,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `واں` bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz | **أَن** hafs,shubah,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَأَن** bazzi,duri,susi,hisham,ibn-wardan,ibn-jammaz  ·  **وَأَنْ** qalun,warsh |
| 61495 | 41:11 | `اسٮوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اسٮوٮى` ruways,rawh | **ٱسۡتَوَىٰٓ** hafs,shubah  ·  **ٱسۡتَوَىٰ** bazzi  ·  **ࡰٜسْتَوَىٰ** qalun  ·  **ࡰٜسْتَوٜىٰٓ** warsh  ·  **اَ۪سۡتَوَىٰٓ** duri  ·  **ࡱٜسۡتَوَىٰ** susi  ·  **ٱسْتَوَىٰٓ** hisham  ·  **ٱسْتَو۪ىٰٓ** khalaf,khallad,abu-al-harith  ·  **ٱسْتَوَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱسْتَوَىى** ruways,rawh  ·  **ٱسْتَو۪يٰٓ** ishaq |
| 61497 | 41:11 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 61750 | 41:28 | `اعدا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `اعداا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,ishaq  ·  `ااعداا` rawh | **أَعۡدَآءِ** hafs,shubah  ·  **ࡶَعۡدَآءِ** bazzi,susi  ·  **ࡶَعْدَآءِ** qalun,warsh  ·  **اَ۬عۡدَآءِ** duri  ·  **أَعْدَآآءِ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱعْدَآآءِ** ibn-wardan,ibn-jammaz,ruways  ·  **أأعْدَآآءِ** rawh |
| 61916 | 41:39 | `الموٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الموٮٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **ٱلۡمَوۡتَىٰٓ** hafs,shubah  ·  **ٱلۡمَوۡتَىٰ** bazzi  ·  **ࡴ۬لْمَوْتَىٰ** qalun  ·  **ࡴ۬لْمَوْتٜىٰٓ** warsh  ·  **اِ۬لۡمَوۡتۭيٰٓ** duri  ·  **ࡵ۬لۡمَوۡت۪ىٰ** susi  ·  **ٱلْمَوْتَيٰٓ** hisham  ·  **ٱلْمَوْت۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْمَوْتَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 61995 | 41:44 | `اعحمى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,ishaq  ·  `ااعحمى` rawh | **ءَا۬عۡجَمِيࣱّ** hafs  ·  **ءَأَعۡجَمِيࣱّ** shubah  ·  **ءَࡶعۡجَمِيࣱّ** bazzi  ·  **ءَٰࡶعْجَمِيࣱّ** qalun  ·  **ءَآعْجَمِيࣱّ** warsh  ·  **ءَٰا۬عۡجَمِيّٞ** duri  ·  **ءَٰࡶعۡجَمِيࣱّ** susi  ·  **أَعْجَمِيࣱّ** hisham  ·  **ءَأَعْجَمِيࣱّ** khalaf,khallad,abu-al-harith,ishaq  ·  **ءٱعْجَمِيࣱّ** ibn-wardan,ibn-jammaz  ·  **ءَاعْجَمِيࣱّ** ruways  ·  **ءَأأعْجَمِيࣱّ** rawh |
| 62067 | 41:47 | `سركاى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سركااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **شُرَكَآءِي** hafs,shubah,duri,susi  ·  **شُرَكَآءِيَ** bazzi  ·  **شُرَكَآءِے** qalun,warsh  ·  **شُرَكَآآءِى** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 62090 | 41:49 | `دعا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `دعاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **دُعَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **دُعَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 62183 | 41:54 | `لڡا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `لڡاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **لِّقَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **لِّٜقَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 62462 | 42:16 | `وعلٮهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `علٮهم` khalaf | **وَعَلَيۡهِمۡ** hafs,shubah,duri,susi  ·  **وَعَلَيۡهِمُۥ** bazzi  ·  **وَعَلَيْهِمْ** qalun,warsh,hisham,abu-al-harith,ishaq  ·  **عَلَيْهُمْ** khalaf  ·  **وَعَلَيْهُمْ** khallad,ruways,rawh  ·  **وَعَلَيْهِمۥُ** ibn-wardan,ibn-jammaz |
| 62664 | 42:27 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساٮه` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **يَشَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَشَآءُِنَّهُۥ** ibn-wardan,ibn-jammaz |
| 62702 | 42:30 | `ڡٮما` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮما` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **فَبِمَا** hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **بِمَا** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **بِِۭمَا** hisham |
| 62970 | 42:49 | `اٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساٮٮا` ibn-wardan,ibn-jammaz | **إِنَٰثࣰا** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹِنَٰثࣰا** bazzi,susi  ·  **ࡹِنَٰثاࣰ** qalun,warsh  ·  **اِ۪نَٰثٗا** duri  ·  **يَشَآءُِنَٰثࣰا** ibn-wardan,ibn-jammaz  ·  **ٱنَٰثࣰا** ruways |
| 63004 | 42:51 | `ٮسا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮساٮه` ibn-wardan,ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **يَشَآءُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَشَآءُِنَّهُۥ** ibn-wardan,ibn-jammaz |
| 63032 | 42:52 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `الٮرط` ruways | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَىٰۜرَٰطࣲ** ruways |
| 63035 | 42:53 | `صرط` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `رط` ruways | **صِرَٰطِ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **ۜرَٰطِ** ruways |
| 63119 | 43:11 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 63311 | 43:29 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 63414 | 43:38 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `حٮٮى` ibn-wardan,ibn-jammaz | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّيى** ibn-wardan,ibn-jammaz  ·  **حَتَّىٰ** ruways,rawh |
| 63463 | 43:43 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `علٮرط` ruways | **عَلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **عَلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَىٰۜرَٰطࣲ** ruways |
| 63639 | 43:61 | `هدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `هدارط` ruways | **هَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **هَٰذَاۜرَٰطࣱ** ruways |
| 63672 | 43:64 | `هدا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `هدارط` ruways | **هَٰذَا** hafs,shubah,bazzi,qalun,warsh,duri,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **هَّٰذَا** susi  ·  **هَٰذَاۜرَٰطࣱ** ruways |
| 63703 | 43:68 | `ٮعٮاد` hafs,bazzi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮعٮادى` shubah,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz | **يَٰعِبَادِ** hafs,bazzi,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **يَٰعِبَادِيَ** shubah  ·  **يَٰعِبَادِے** qalun,warsh  ·  **يَٰعِبَادِي** duri,susi  ·  **يَٰعِبَادِى** hisham,ibn-wardan,ibn-jammaz  ·  **يَٰعِبَادِۦ** ruways |
| 63729 | 43:71 | `ٮسٮهٮه` hafs,qalun,warsh,hisham,ibn-wardan,ibn-jammaz  ·  `ٮسٮهى` shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq | **تَشۡتَهِيهِ** hafs  ·  **تَشۡتَهِي** shubah,bazzi,duri,susi  ·  **تَشْتَهِيهِ** qalun,warsh,hisham,ibn-wardan,ibn-jammaz  ·  **تَشْتَهِي** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 63825 | 43:84 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah  ·  **ٱلسَّمَآࢇ** bazzi  ·  **ࡴ۬لسَّمَآࢇ** qalun  ·  **ࡴ۬لسَّمَآءِ** warsh  ·  **اِ۬لسَّمَآ** duri  ·  **ࡵ۬لسَّمَا** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 63870 | 43:88 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 63971 | 44:16 | `الكٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الكٮرٮى` ibn-wardan,ibn-jammaz | **ٱلۡكُبۡرَىٰٓ** hafs,shubah  ·  **ٱلۡكُبۡرَىٰ** bazzi  ·  **ࡰ۬لْكُبْرَىٰ** qalun  ·  **ࡰ۬لْكُبْرٜىٰٓ** warsh  ·  **اَ۬لۡكُبۡر۪يٰٓ** duri  ·  **ࡱ۬لۡكُبۡرٜىٰ** susi  ·  **ٱلْكُبْرَىٰٓ** hisham  ·  **ٱلْكُبْر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْكُبْرَىى** ibn-wardan,ibn-jammaz  ·  **ٱلْكُبْرَىٰ** ruways,rawh |
| 63996 | 44:19 | `اٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اٮٮى` ibn-wardan,ibn-jammaz | **إِنِّيٓ** hafs,shubah  ·  **إِنِّيَ** bazzi,qalun,warsh,duri,susi  ·  **إِنِّٜيٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِنِّٜيي** ibn-wardan,ibn-jammaz  ·  **إِنِّٜي** ruways,rawh |
| 64014 | 44:22 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 64017 | 44:23 | `ڡاسر` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡااسر` ibn-wardan,ibn-jammaz | **فَأَسۡرِ** hafs,shubah,duri,susi  ·  **فَٱسۡرِ** bazzi  ·  **فَاسْرِ** qalun,warsh  ·  **فَأَسْرِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **فَااسْرِ** ibn-wardan,ibn-jammaz |
| 64080 | 44:34 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 64159 | 44:47 | `سوا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `سواا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **سَوَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **سَوَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 64255 | 45:5 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 64939 | 46:15 | `احسٮا` hafs,shubah,khalaf,khallad,abu-al-harith,ishaq  ·  `حسٮا` bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh | **إِحۡسَٰنًا** hafs,shubah  ·  **حُسۡنًا** bazzi,duri,susi  ·  **حُسْناً** qalun,warsh  ·  **حُسْنًا** hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **إِحْسَٰنًا** khalaf,khallad,abu-al-harith,ishaq |
| 65059 | 46:20 | `ادهٮٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,ishaq  ·  `اادهٮٮم` rawh | **أَذۡهَبۡتُمۡ** hafs,shubah,duri,susi  ·  **ءَࡶذۡهَبۡتُمُۥ** bazzi  ·  **أَذْهَبْتُمْ** qalun,warsh,khalaf,khallad,abu-al-harith,ishaq  ·  **ءَاذْهَبْتُمْ** hisham  ·  **ءٱذْهَبْتُمۥُ** ibn-wardan,ibn-jammaz  ·  **ءَٱذْهَبْتُمْ** ruways  ·  **ءَأأذْهَبْتُمْ** rawh |
| 65304 | 46:33 | `ٮحٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮحى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **يُحۡـِۧيَ** hafs,shubah,bazzi,duri,susi  ·  **يُّحْـۑِيَ** qalun  ·  **يُّحْۑِيَ** warsh  ·  **يُحْـِيَ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يُّحْـِيَ** khalaf |
| 65868 | 47:38 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 65913 | 48:2 | `وٮهدٮك` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `وٮهدٮكرطا` ruways | **وَيَهۡدِيَكَ** hafs,shubah,bazzi,duri,susi  ·  **وَيَهْدِيَكَ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **وَيَهْدِيَكَۜرَٰطࣰا** ruways |
| 66078 | 48:12 | `السو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّوۡءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّوْءِ** qalun,warsh  ·  **اَ۬لسَّوۡءِ** duri  ·  **ࡱ۬لسَّوۡءِ** susi  ·  **ٱلسَّوْآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 66232 | 48:20 | `وٮهدٮكم` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `وٮهدٮكمرطا` ruways | **وَيَهۡدِيَكُمۡ** hafs,shubah,duri,susi  ·  **وَيَهۡدِيَكُمُۥ** bazzi  ·  **وَيَهْدِيَكُمْ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **وَيَهْدِيَكُمُۥ** ibn-wardan,ibn-jammaz  ·  **وَيَهْدِيَكُمْۜرَٰطࣰا** ruways |
| 66514 | 49:4 | `ورا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَرَآءِ** hafs,shubah,bazzi,duri,susi  ·  **وَّرَآءِ** qalun,warsh  ·  **وَرَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّرَآآءِ** khalaf |
| 66600 | 49:9 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  `لى` ibn-wardan,ibn-jammaz,ruways | **إِلَىٰٓ** hafs,shubah  ·  **ࡹلَىٰ** bazzi,qalun,susi  ·  **ࡹلَىٰٓ** warsh  ·  **ا۪لَىٰٓ** duri  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لَىٰ** ibn-wardan,ibn-jammaz,ruways  ·  **إِلَىٰ** rawh |
| 66817 | 50:3 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways  ·  `اادا` khalaf,khallad,abu-al-harith,rawh,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi  ·  **أَٰࢇذَا** qalun,susi  ·  **ࡰࢇذَا** warsh  ·  **أَٰ۟ذَا** duri  ·  **أَءِٰذَا** hisham  ·  **أَآءِذَا** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **أَٰءذَا** ibn-wardan,ibn-jammaz  ·  **أَءذَا** ruways |
| 66845 | 50:6 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 66872 | 50:9 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 67042 | 50:30 | `امٮلاٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `امٮلٮلٮ` ibn-wardan,ibn-jammaz | **ٱمۡتَلَأۡتِ** hafs,shubah,bazzi  ·  **ࡴٜمْتَلَأْتِ** qalun,warsh  ·  **اِ۪مۡتَلَأۡتِ** duri  ·  **ࡵٜمۡتَلَاتِ** susi  ·  **ٱمْتَلأَتِ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱمْتَليلتِ** ibn-wardan,ibn-jammaz  ·  **ٱمْتَلأَُّتِ** ruways,rawh |
| 67190 | 51:7 | `والسما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والسماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **وَالسَّمَآءِ** qalun,warsh  ·  **وَاَلسَّمَآءِ** duri  ·  **وَࡱلسَّمَآءِ** susi  ·  **وَٱلسَّمَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّٱلسَّمَآآءِ** khalaf |
| 67261 | 51:22 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 67266 | 51:23 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 67290 | 51:26 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `الٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 67367 | 51:38 | `موسى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `موسٮى` ibn-wardan,ibn-jammaz,ruways,rawh | **مُوسَىٰٓ** hafs,shubah,hisham  ·  **مُوسَىٰ** bazzi,qalun  ·  **مُوسٜىٰٓ** warsh  ·  **مُوسۭيٰٓ** duri  ·  **مُوس۪ىٰ** susi  ·  **مُوس۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **مُوسَيى** ibn-wardan,ibn-jammaz,ruways,rawh |
| 67802 | 52:44 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 67859 | 53:3 | `الهوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الهوٮى` ruways,rawh | **ٱلۡهَوَىٰٓ** hafs,shubah  ·  **ٱلۡهَوَىٰ** bazzi  ·  **ࡴ۬لْهَوَىٰ** qalun  ·  **ࡴ۬لْهَوٜىٰٓ** warsh  ·  **اِ۬لۡهَوۭيٰٓ** duri  ·  **ࡵ۬لۡهَو۪ىٰ** susi  ·  **ٱلْهَوَىٰٓ** hisham  ·  **ٱلْهَو۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْهَوَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلْهَوَىى** ruways,rawh |
| 67882 | 53:10 | `ڡاوحى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡاوحٮى` ruways,rawh | **فَأَوۡحَىٰٓ** hafs,shubah,duri  ·  **فَأَوۡحَىٰ** bazzi,susi  ·  **فَأَوْحَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **فَأَوْحٜىٰٓ** warsh  ·  **فَأَوْحَىٰٓ** hisham  ·  **فَأَوْح۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **فَأَوْحَيى** ruways,rawh |
| 67891 | 53:11 | `راى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `راٮى` ruways,rawh | **رَأَىٰٓ** hafs,hisham  ·  **رٜأٜىٰٓ** shubah,warsh  ·  **رَأَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **رَأ۪يٰٓ** duri  ·  **رَأٜىٰ** susi  ·  **ر۪أ۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **رَأَىى** ruways,rawh |
| 67905 | 53:15 | `الماوى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الماوٮى` ruways,rawh | **ٱلۡمَأۡوَىٰٓ** hafs,shubah  ·  **ٱلۡمَأۡوَىٰ** bazzi  ·  **ࡲ۬لْمَأْوَىٰ** qalun  ·  **ࡲ۬لْمَأْوٜىٰٓ** warsh  ·  **اُ۬لۡمَأۡوۭيٰٓ** duri  ·  **ࡲ۬لۡمَاو۪ىٰ** susi  ·  **ٱلْمَأْوَىٰٓ** hisham  ·  **ٱلْمَأْو۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْمَاوَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلْمَأْوَىى** ruways,rawh |
| 67921 | 53:18 | `الكٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الكٮرٮى` ruways,rawh | **ٱلۡكُبۡرَىٰٓ** hafs,shubah  ·  **ٱلۡكُبۡرَىٰ** bazzi  ·  **ࡴ۬لْكُبْرَىٰ** qalun  ·  **ࡴ۬لْكُبْرٜىٰٓ** warsh  ·  **اِ۬لۡكُبۡر۪يٰٓ** duri  ·  **ࡵ۬لۡكُبۡرٜىٰ** susi  ·  **ٱلْكُبْرَىٰٓ** hisham  ·  **ٱلْكُبْر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْكُبْرَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلْكُبْرَىى** ruways,rawh |
| 67927 | 53:20 | `الاحرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الاحرٮى` ruways,rawh | **ٱلۡأُخۡرَىٰٓ** hafs,shubah  ·  **ٱلۡأُخۡرَىٰ** bazzi  ·  **ࡰ۬لْأُخْرَىٰ** qalun  ·  **ࡰ۬لُاخْرٜىٰٓ** warsh  ·  **اَ۬لۡأُخۡر۪يٰٓ** duri  ·  **ࡱ۬لۡأُخۡرٜىٰ** susi  ·  **ٱلأُْخْرَىٰٓ** hisham  ·  **ٱلأُْخْر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلأُْخْرَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلأُْخْرَىى** ruways,rawh |
| 67935 | 53:22 | `صٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `صٮرٮى` ruways,rawh | **ضِيزَىٰٓ** hafs,shubah,hisham  ·  **ضِئۡزَىٰ** bazzi  ·  **ضِيزَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **ضِيزٜىٰٓ** warsh  ·  **ضِيزۭيٰٓ** duri  ·  **ضِيز۪ىٰ** susi  ·  **ضِيز۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ضِيزَىى** ruways,rawh |
| 67960 | 53:23 | `الهدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الهدٮى` ruways,rawh | **ٱلۡهُدَىٰٓ** hafs,shubah  ·  **ٱلۡهُدَىٰ** bazzi  ·  **ࡲ۬لْهُدَىٰ** qalun  ·  **ࡲ۬لْهُدٜىٰٓ** warsh  ·  **اِ۬لۡهُدۭيٰٓ** duri  ·  **ࡵ۬لۡهُد۪ىٰ** susi  ·  **ٱلْهُدَىٰٓ** hisham  ·  **ٱلْهُد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْهُدَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلْهُدَىى** ruways,rawh |
| 67985 | 53:26 | `وٮرصى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `وٮرصٮى` ruways,rawh | **وَيَرۡضَىٰٓ** hafs,shubah  ·  **وَيَرۡضَىٰ** bazzi  ·  **وَيَرْضَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **وَيَرْضٜىٰٓ** warsh  ·  **وَيَرۡضۭيٰٓ** duri  ·  **وَيَرۡض۪ىٰ** susi  ·  **وَيَرْضَىٰٓ** hisham  ·  **وَيَرْض۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَيَرْضَيى** ruways,rawh |
| 68084 | 53:32 | `اٮڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اٮڡٮى` ruways,rawh | **ٱتَّقَىٰٓ** hafs,shubah  ·  **ٱتَّقَىٰ** bazzi  ·  **ࡴٜتَّقَىٰ** qalun  ·  **ࡴٜتَّقٜىٰٓ** warsh  ·  **اِ۪تَّقۭيٰٓ** duri  ·  **ࡵٜتَّق۪ىٰ** susi  ·  **ٱتَّقَيٰٓ** hisham  ·  **ٱتَّق۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱتَّقَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱتَّقَيى** ruways,rawh |
| 68090 | 53:34 | `واكدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `واكدٮى` ruways,rawh | **وَأَكۡدَىٰٓ** hafs,shubah  ·  **وَأَكۡدَىٰ** bazzi  ·  **وَأَكْدَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **وَأَكْدٜىٰٓ** warsh  ·  **وَأَكۡدۭيٰٓ** duri  ·  **وَأَكۡد۪ىٰ** susi  ·  **وَأَكْدَىٰٓ** hisham  ·  **وَّأَكْد۪ىٰٓ** khalaf  ·  **وَأَكْد۪ىٰٓ** khallad,abu-al-harith,ishaq  ·  **وَأَكْدَىى** ruways,rawh |
| 68095 | 53:35 | `ٮرى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮرٮى` ruways,rawh | **يَرَىٰٓ** hafs,shubah,hisham  ·  **يَرَىٰ** bazzi,qalun,ibn-wardan,ibn-jammaz  ·  **يَرٜىٰٓ** warsh  ·  **يَر۪يٰٓ** duri  ·  **يَرٜىٰ** susi  ·  **يَر۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يَرَىى** ruways,rawh |
| 68105 | 53:37 | `وڡى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `وڡٮى` ruways,rawh | **وَفَّىٰٓ** hafs,shubah  ·  **وَفَّىٰ** bazzi,qalun  ·  **وَفّٜىٰٓ** warsh  ·  **وَفّۭيٰٓ** duri  ·  **وَفّ۪ىٰ** susi  ·  **وَفَّيٰٓ** hisham  ·  **وَفّٜ۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَفَّىٰ** ibn-wardan,ibn-jammaz  ·  **وَفَّيى** ruways,rawh |
| 68180 | 53:55 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68187 | 53:56 | `الاولى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الاولٮى` ruways,rawh | **ٱلۡأُولَىٰٓ** hafs,shubah  ·  **ٱلۡأُولَىٰ** bazzi  ·  **ࡴ۬لْأُولَىٰ** qalun  ·  **ࡴ۬لُاولٜىٰٓ** warsh  ·  **اِ۬لۡأُولۭيٰٓ** duri  ·  **ࡵ۬لۡأُول۪ىٰ** susi  ·  **ٱلأُْولَيٰٓ** hisham  ·  **ٱلأُْول۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلأُْولَىٰ** ibn-wardan,ibn-jammaz  ·  **ٱلأُْولَيى** ruways,rawh |
| 68228 | 54:4 | `الاٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡأَنۢبَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْأَنۢبَآءِ** qalun  ·  **ࡰ۬لَانۢبَآءِ** warsh  ·  **اَ۬لۡأَنۢبَآءِ** duri  ·  **ࡱ۬لۡأَنۢبَآءِ** susi  ·  **ٱلْأَنۢبَآآءِ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلأَْنۢبَآآءِ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 68277 | 54:11 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68590 | 55:13 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68605 | 55:16 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68613 | 55:18 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68624 | 55:21 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68629 | 55:22 | `اللولو` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اللولوا` qalun,warsh,ibn-wardan,ibn-jammaz | **ٱللُّؤۡلُؤُ** hafs,bazzi  ·  **ٱللُّولُؤُ** shubah  ·  **ࡰ۬للُّؤْلُؤُاْ** qalun,warsh  ·  **اَ۬للُّؤۡلُؤُ** duri  ·  **ࡱ۬للُّولُؤُ** susi  ·  **ٱللُّؤْلُؤُ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱللُّولُؤُاْ** ibn-wardan,ibn-jammaz |
| 68632 | 55:23 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68642 | 55:25 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68656 | 55:28 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68670 | 55:30 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68678 | 55:32 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68698 | 55:34 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68710 | 55:36 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68720 | 55:38 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68732 | 55:40 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68742 | 55:42 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68757 | 55:45 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68766 | 55:47 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68772 | 55:49 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68779 | 55:51 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68788 | 55:53 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68801 | 55:55 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68814 | 55:57 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68821 | 55:59 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68830 | 55:61 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68837 | 55:63 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68842 | 55:65 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68849 | 55:67 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68857 | 55:69 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68864 | 55:71 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68872 | 55:73 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68882 | 55:75 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 68892 | 55:77 | `الا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ءَالَآءِ** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **ءَالَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 69060 | 56:47 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi  ·  **إِنَّا** qalun  ·  **ࡴنَّا** warsh  ·  **أَٰ۟نَّا** duri  ·  **أَٰࢇنَّا** susi  ·  **أَءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,ishaq  ·  **إِنَّا** abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh |
| 69062 | 56:48 | `اواٮاوٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `او` hisham | **أَوَءَابَآؤُنَا** hafs,shubah,bazzi,warsh,duri,susi  ·  **أَوْءَابَآؤُنَا** qalun  ·  **أَوْ** hisham  ·  **أَوَءَابَآؤُنَا** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **أَوْءَابَآؤُنَا** ibn-wardan,ibn-jammaz |
| 69117 | 56:61 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 69333 | 57:4 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 69442 | 57:10 | `وكلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `وكل` hisham | **وَكُلࣰّا** hafs,shubah,bazzi,susi  ·  **وَكُلّاࣰ** qalun,warsh  ·  **وَكُلّٗا** duri  ·  **وَكُلࣱّ** hisham  ·  **وَكُلࣰّا** khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 69666 | 57:21 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 69775 | 57:27 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 69884 | 58:2 | `الى` hafs,shubah,bazzi,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الٮى` qalun  ·  `الاى` ibn-wardan,ibn-jammaz | **ٱلَّٰٓـِٔي** hafs,shubah  ·  **ٱلَّٰٓيۡ** bazzi  ·  **ࡰ۬لَّٰٓئِے** qalun  ·  **ࡰ۬لٜےْ** warsh  ·  **اَ۬لَّٰٓيۡ** duri  ·  **ࡱ۬لَّٰٓيۡ** susi  ·  **ٱلَِّٰٔي** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلَّٱي** ibn-wardan,ibn-jammaz  ·  **ٱلَّٰيِ** ruways,rawh |
| 70149 | 58:13 | `اسڡڡٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ااسڡڡٮم` hisham | **ءَأَشۡفَقۡتُمۡ** hafs,shubah  ·  **ءَࡶشۡفَقۡتُمُۥ** bazzi  ·  **ءَٰࡶشْفَقْتُمْ** qalun  ·  **آٓشْفَقْتُمُۥٓ** warsh  ·  **ءَٰا۬شۡفَقۡتُمۡ** duri  ·  **ءَٰࡶشۡفَقۡتُمۡ** susi  ·  **ءَااشْفَقْتُمْ** hisham  ·  **ءَأَشْفَقْتُمْ** khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءٱشْفَقْتُمۥُ** ibn-wardan,ibn-jammaz  ·  **ءَٱشْفَقْتُمْ** ruways |
| 70463 | 59:7 | `الاعٮٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الاعٮٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡأَغۡنِيَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لْأَغْنِيَآءِ** qalun  ·  **ࡰ۬لَاغْنِيَآءِ** warsh  ·  **اَ۬لۡأَغۡنِيَآءِ** duri  ·  **ࡱ۬لۡأَغۡنِيَآءِ** susi  ·  **ٱلْأَغْنِيَآآءِ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلأَْغْنِيَآآءِ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 70479 | 59:8 | `للڡڡرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `للڡڡراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **لِلۡفُقَرَآءِ** hafs,shubah,bazzi,duri,susi  ·  **لِلْفُقَرَآءِ** qalun,warsh  ·  **لِلْفُقَرَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 70595 | 59:13 | `لاٮٮم` hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `لااٮٮم` duri,susi | **لَأَنتُمۡ** hafs,shubah  ·  **لَأَنتُمُۥ** bazzi  ·  **لَأَنتُمْ** qalun,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **لَأَنتُمُۥٓ** warsh  ·  **لَأَاْنتُمۡ** duri,susi  ·  **لأََنتُمۥُ** ibn-wardan,ibn-jammaz  ·  **لأََنتُمْ** ruways,rawh |
| 70616 | 59:14 | `ورا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `وراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَرَآءِ** hafs,shubah,bazzi,duri,susi  ·  **وَّرَآءِ** qalun,warsh  ·  **وَرَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّرَآآءِ** khalaf |
| 70829 | 60:2 | `ٮالسو` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالسوا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلسُّوٓءِ** hafs,shubah,bazzi  ·  **بِالسُّوٓءِ** qalun,warsh,duri,susi  ·  **بِالسُّوٓآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 70978 | 60:9 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 71063 | 60:12 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 71069 | 60:12 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `علٮى` ibn-wardan,ibn-jammaz | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ruways,rawh  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ibn-wardan,ibn-jammaz |
| 71221 | 61:7 | `ٮدعى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮدعٮى` ibn-wardan,ibn-jammaz | **يُدۡعَىٰٓ** hafs,shubah,duri  ·  **يُدۡعَىٰ** bazzi,susi  ·  **يُدْعَىٰ** qalun,ruways,rawh  ·  **يُدْعٜىٰٓ** warsh  ·  **يُدْعَىٰٓ** hisham  ·  **يُدْع۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **يُدْعَيى** ibn-wardan,ibn-jammaz |
| 71236 | 61:8 | `ٮوره` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮوردهد` hisham | **نُورِهِۦ** hafs,bazzi,khalaf,khallad,abu-al-harith,ishaq  ·  **نُّورَهُۥ** shubah,qalun,warsh,duri,susi  ·  **نُّوردهدۥ** hisham  ·  **نُّورَهُۥ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 71310 | 61:14 | `اٮصار` hafs,shubah,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اٮصارا` bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz | **أَنصَارَ** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **أَنصَارࣰا** bazzi,susi,ibn-wardan,ibn-jammaz  ·  **أَنصَاراࣰ** qalun,warsh  ·  **أَنصَارٗا** duri |
| 71311 | 61:14 | `الله` hafs,shubah,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `لله` bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz | **ٱللَّهِ** hafs,shubah  ·  **لِّلَّهِ** bazzi,duri,susi  ·  **لِّلهِ** qalun,warsh  ·  **ٱللهَِّ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **للهَِّ** ibn-wardan,ibn-jammaz  ·  **ٱللَّهِ** ruways,rawh |
| 71317 | 61:14 | `للحوارٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `للحوارٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **لِلۡحَوَارِيِّـۧنَ** hafs,shubah,bazzi,duri,susi  ·  **لِلْحَوَارِيِّـۑنَ** qalun  ·  **لِلْحَوَارِيِّۑنَ** warsh  ·  **لِلْحَوَارِيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 71357 | 62:2 | `الامٮٮں` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `الامٮں` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلۡأُمِّيِّـۧنَ** hafs,shubah,bazzi  ·  **ࡴ۬لْأُمِّيِّـۑنَ** qalun  ·  **ࡴ۬لُامِّيِّۑنَ** warsh  ·  **اِ۬لۡأُمِّيِّـۧنَ** duri  ·  **ࡵ۬لۡأُمِّيِّـۧنَ** susi  ·  **ٱلأُْمِّٜيِّٜـنَ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 71937 | 65:1 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 72022 | 65:3 | `امره` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `امردهد` hisham | **أَمۡرِهِۦ** hafs  ·  **أَمۡرَهُۥ** shubah,bazzi,duri,susi  ·  **أَمْرَهُۥ** qalun,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **ࡰمْرَهُۥ** warsh  ·  **أَمْردهدۥ** hisham |
| 72029 | 65:4 | `والى` hafs,shubah,bazzi,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `والٮى` qalun  ·  `والاى` ibn-wardan,ibn-jammaz | **وَٱلَّٰٓـِٔي** hafs,shubah  ·  **وَٱلَّٰٓيۡ** bazzi  ·  **وَالَّٰٓئِے** qalun  ·  **وَالٜےْ** warsh  ·  **وَاَلَّٰٓيۡ** duri  ·  **وَࡱلَّٰٓيۡ** susi  ·  **وَٱلَِّٰٔي** hisham,khallad,abu-al-harith,ishaq  ·  **وَّٱلَِّٰٔي** khalaf  ·  **وَٱلَّٱي** ibn-wardan,ibn-jammaz  ·  **وَٱلَّٰيِ** ruways,rawh |
| 72040 | 65:4 | `والى` hafs,shubah,bazzi,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `والٮى` qalun  ·  `والاى` ibn-wardan,ibn-jammaz | **وَٱلَّٰٓـِٔي** hafs,shubah  ·  **وَٱلَّٰٓيۡ** bazzi  ·  **وَالَّٰٓئِے** qalun  ·  **وَالٜےْ** warsh  ·  **وَاَلَّٰٓيۡ** duri  ·  **وَࡱلَّٰٓيۡ** susi  ·  **وَٱلَِّٰٔي** hisham,khallad,abu-al-harith,ishaq  ·  **وَّٱلَِّٰٔي** khalaf  ·  **وَٱلَّٱي** ibn-wardan,ibn-jammaz  ·  **وَٱلَّٰيِ** ruways,rawh |
| 72224 | 66:1 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّٰأَيُّهَا** khalaf |
| 72250 | 66:3 | `اسر` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اسر‏` warsh | **أَسَرَّ** hafs,shubah,bazzi,qalun,duri,susi  ·  **ࡰسَرَّ‏** warsh  ·  **أَسَرَّ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 72394 | 66:9 | `ٮاٮها` hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮاٮها‏` warsh | **يَٰٓأَيُّهَا** hafs,shubah,duri  ·  **يَٰأَيُّهَا** bazzi,qalun,susi  ·  **يَٰٓأَيُّهَا‏** warsh  ·  **يَٰأَيُّهَا** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يَّٰأَيُّهَا** khalaf |
| 72469 | 66:12 | `وكٮٮه` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `وكٮدٮه` hisham | **وَكُتُبِهِۦ** hafs,duri,susi,ruways,rawh  ·  **وَكِتَٰبِهِۦ** shubah,bazzi,qalun,warsh,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **وَكِتدٰبِهِۦ** hisham |
| 72634 | 67:16 | `امٮٮم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اامٮٮم` hisham | **ءَأَمِنتُم** hafs,shubah,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ءَࡶمِنتُمُۥ** bazzi  ·  **ءَٰࡶمِنتُم** qalun,susi  ·  **ءَامِنتُم** warsh  ·  **ءَٰا۬مِنتُم** duri  ·  **ءَاامِنتُم** hisham  ·  **ءَٰٱمِنتُمۥُ** ibn-wardan,ibn-jammaz  ·  **ءَٱمِنتُم** ruways |
| 72637 | 67:16 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 72649 | 67:17 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡴ۬لسَّمَآءِ** qalun,warsh  ·  **اِ۬لسَّمَآءِ** duri  ·  **ࡵ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 72712 | 67:22 | `اهدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `اهدٮى` ruways,rawh | **أَهۡدَىٰٓ** hafs,shubah,duri  ·  **أَهۡدَىٰ** bazzi,susi  ·  **أَهْدَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **أَهْدٜىٰٓ** warsh  ·  **أَهْدَىٰٓ** hisham  ·  **أَهْد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **أَهْدَىى** ruways,rawh |
| 72716 | 67:22 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `علٮرط` ruways | **عَلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz,rawh  ·  **عَلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَىٰۜرَٰطࣲ** ruways |
| 72758 | 67:27 | `سٮٮ` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `سلٮٮ` ibn-wardan,ibn-jammaz | **سِيٓـَٔتۡ** hafs,shubah,bazzi,duri,susi  ·  **س۬يٓـَٔتْ** qalun,warsh  ·  **سيَٓٔتْ** hisham,abu-al-harith,ruways  ·  **سِيَٓٔتْ** khalaf,khallad,rawh,ishaq  ·  **سليَٓٔتْ** ibn-wardan,ibn-jammaz |
| 73081 | 68:49 | `ٮالعرا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮالعراا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **بِٱلۡعَرَآءِ** hafs,shubah,bazzi  ·  **بِالْعَرَآءِ** qalun,warsh  ·  **بِالۡعَرَآءِ** duri,susi  ·  **بِالْعَرَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 73193 | 69:17 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 73436 | 70:18 | `ڡاوعى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡاوعٮى` ruways,rawh | **فَأَوۡعَىٰٓ** hafs,shubah  ·  **فَأَوۡعَىٰ** bazzi  ·  **فَأَوْعَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **فَأَوْعٜىٰٓ** warsh  ·  **فَأَوۡعۭيٰٓ** duri  ·  **فَأَوۡع۪ىٰ** susi  ·  **فَأَوْعَىٰٓ** hisham  ·  **فَأَوْع۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **فَأَوْعَيى** ruways,rawh |
| 73483 | 70:30 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 73547 | 70:41 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 73611 | 71:4 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 73633 | 71:6 | `دعاى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `دعااى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **دُعَآءِيٓ** hafs,shubah  ·  **دُعَآءِيَ** bazzi,qalun,warsh,duri,susi  ·  **دُعَآآءِىَ** hisham,ibn-wardan,ibn-jammaz  ·  **دُعَآآءِىٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **دُعَآآءِي** ruways  ·  **دُعَآآءِى** rawh |
| 73932 | 72:13 | `الهدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الهدٮى` ruways,rawh | **ٱلۡهُدَىٰٓ** hafs,shubah  ·  **ٱلۡهُدَىٰ** bazzi  ·  **ࡰ۬لْهُدَىٰ** qalun  ·  **ࡰ۬لْهُدٜىٰٓ** warsh  ·  **اَ۬لۡهُدَىٰٓ** duri  ·  **ࡱ۬لۡهُدَىٰ** susi  ·  **ٱلْهُدَىٰٓ** hisham  ·  **ٱلْهُد۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلْهُدَيٰ** ibn-wardan,ibn-jammaz  ·  **ٱلْهُدَىى** ruways,rawh |
| 73994 | 72:20 | `ڡل` hafs,shubah,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡال` bazzi,qalun,warsh,duri,susi,ruways,rawh | **قُلۡ** hafs,shubah  ·  **قَالَ** bazzi,qalun,warsh,duri,susi,ruways,rawh  ·  **قَٰلَ** hisham,abu-al-harith,ishaq  ·  **قُلْ** khalaf,khallad,ibn-wardan,ibn-jammaz |
| 74038 | 72:24 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `حٮٮى` ruways,rawh | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّىٰ** ibn-wardan,ibn-jammaz  ·  **حَتَّيى** ruways,rawh |
| 74120 | 73:6 | `وطا` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `وطاا` hisham | **وَطۡـࣰٔا** hafs,shubah,bazzi  ·  **وَطْـٔاࣰ** qalun,warsh  ·  **وِطَآءٗ** duri  ·  **وِطَآءࣰ** susi  ·  **وِطَااءࣰ** hisham  ·  **وَطࣰْٔا** khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 74447 | 74:33 | `اد` hafs,qalun,warsh,khalaf,khallad,ruways,rawh,ishaq  ·  `ادا` shubah,bazzi,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz | **إِذۡ** hafs  ·  **إِذَا** shubah,bazzi,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz  ·  **إِذْ** qalun,khalaf,khallad,ruways,rawh,ishaq  ·  **إِذَ** warsh |
| 74448 | 74:33 | `ادٮر` hafs,qalun,warsh,khalaf,khallad,ruways,rawh,ishaq  ·  `دٮر` shubah,bazzi,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz | **أَدۡبَرَ** hafs  ·  **دَبَرَ** shubah,bazzi,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz  ·  **أَدْبَرَ** qalun,khalaf,khallad,ruways,rawh,ishaq  ·  **ࡰدْبَرَ** warsh |
| 74498 | 74:47 | `حٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `حٮٮى` ruways,rawh | **حَتَّىٰٓ** hafs,shubah,warsh,duri  ·  **حَتَّىٰ** bazzi,qalun,susi  ·  **حَتَّىٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **حَتَّىٰ** ibn-wardan,ibn-jammaz  ·  **حَتَّيى** ruways,rawh |
| 74562 | 75:4 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 74673 | 75:33 | `الى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `الٮى` ruways,rawh | **إِلَىٰٓ** hafs,shubah,warsh,duri  ·  **إِلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **إِلَيى** ruways,rawh |
| 74682 | 75:35 | `ڡاولى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ڡاولٮى` ruways,rawh | **فَأَوۡلَىٰٓ** hafs,shubah  ·  **فَأَوۡلَىٰ** bazzi  ·  **فَأَوْلَىٰ** qalun,ibn-wardan,ibn-jammaz  ·  **فَأَوْلٜىٰٓ** warsh  ·  **فَأَوۡلۭيٰٓ** duri  ·  **فَأَوۡل۪ىٰ** susi  ·  **فَأَوْلَيٰٓ** hisham  ·  **فَأَوْل۪يٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **فَأَوْلَيى** ruways,rawh |
| 74703 | 75:39 | `والاٮٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `والاٮٮٮى` ruways,rawh | **وَٱلۡأُنثَىٰٓ** hafs,shubah  ·  **وَٱلۡأُنثَىٰ** bazzi  ·  **وَالْأُنثَىٰ** qalun  ·  **وَالُانثٜىٰٓ** warsh  ·  **وَاَلۡأُنثۭيٰٓ** duri  ·  **وَࡱلۡأُنث۪ىٰ** susi  ·  **وَٱلأُْنثَىٰٓ** hisham  ·  **وَٱلأُْنث۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **وَٱلأُْنثَىٰ** ibn-wardan,ibn-jammaz  ·  **وَٱلأُْنثَيى** ruways,rawh |
| 74707 | 75:40 | `على` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `علٮى` ruways,rawh | **عَلَىٰٓ** hafs,shubah,warsh,duri  ·  **عَلَىٰ** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **عَلَيٰٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عَلَيى** ruways,rawh |
| 74709 | 75:40 | `ٮحٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `ٮحى` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **يُحۡـِۧيَ** hafs,shubah,bazzi,duri,susi  ·  **يُّحْـۑِيَ** qalun  ·  **يُّحْۑِيَ** warsh  ·  **يُحْـِيَ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يُّحْـِيَ** khalaf |
| 74908 | 76:27 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 75329 | 79:10 | `اٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `ااٮا` khalaf,khallad,abu-al-harith,ishaq | **أَءِنَّا** hafs,shubah  ·  **أَࢇنَّا** bazzi,warsh  ·  **أَٰࢇنَّا** qalun,susi  ·  **أَٰ۟نَّا** duri  ·  **أَٰءِٰنَّا** hisham  ·  **أَآءِنَّا** khalaf,khallad,abu-al-harith,ishaq  ·  **إِنَّا** ibn-wardan,ibn-jammaz  ·  **أَءنَّا** ruways  ·  **أَءِنَّا** rawh |
| 75333 | 79:11 | `ادا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  `اادا` khalaf,khallad,ishaq | **أَءِذَا** hafs,shubah  ·  **أَࢇذَا** bazzi  ·  **إِذَا** qalun,warsh,hisham,abu-al-harith,ruways,rawh  ·  **أَٰ۟ذَا** duri  ·  **أَٰࢇذَا** susi  ·  **أَآءِذَا** khalaf,khallad,ishaq  ·  **أَٰءذَا** ibn-wardan,ibn-jammaz |
| 75336 | 79:11 | `ٮحره` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮره` khallad | **نَّخِرَةࣰ** hafs,bazzi,qalun,warsh,susi  ·  **نَّٰخِرَةࣰ** shubah  ·  **نَّخِرَةٗ** duri  ·  **نَّخِرَةࣰ** hisham,ibn-wardan,ibn-jammaz,rawh  ·  **نَّٰخِرَةࣰ** khalaf,abu-al-harith,ruways,ishaq  ·  **نَِّٰٰرَةࣰ** khallad |
| 75952 | 83:32 | `هولا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `هولاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **هَٰٓؤُلَآءِ** hafs,shubah,warsh,duri  ·  **هَٰؤُلَآءِ** bazzi,qalun,susi  ·  **هَٰؤُلَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 76019 | 84:12 | `وٮصلى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وٮصصلى` ibn-wardan,ibn-jammaz | **وَيَصۡلَىٰ** hafs,shubah,duri,susi  ·  **وَيُصَلَّيٰ** bazzi  ·  **وَيُصَلَّىٰ** qalun,warsh  ·  **وَيُصَلَّيٰ** hisham  ·  **وَّيَصْل۪يٰ** khalaf  ·  **وَيَصْل۪يٰ** khallad,ishaq  ·  **وَيُصَلّٜ۪يٰ** abu-al-harith  ·  **وَيصصْلَىٰ** ibn-wardan,ibn-jammaz  ·  **وَيَصْلَىٰ** ruways,rawh |
| 76080 | 85:1 | `والسما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والسماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **وَالسَّمَآءِ** qalun,warsh  ·  **وَاَلسَّمَآءِ** duri  ·  **وَࡱلسَّمَآءِ** susi  ·  **وَٱلسَّمَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّٱلسَّمَآآءِ** khalaf |
| 76189 | 86:1 | `والسما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والسماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **وَالسَّمَآءِ** qalun,warsh  ·  **وَاَلسَّمَآءِ** duri  ·  **وَࡱلسَّمَآءِ** susi  ·  **وَٱلسَّمَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّٱلسَّمَآآءِ** khalaf |
| 76229 | 86:11 | `والسما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والسماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **وَالسَّمَآءِ** qalun,warsh  ·  **وَاَلسَّمَآءِ** duri  ·  **وَࡱلسَّمَآءِ** susi  ·  **وَٱلسَّمَآآءِ** hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **وَّٱلسَّمَآآءِ** khalaf |
| 76381 | 88:18 | `السما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لسَّمَآءِ** qalun,warsh  ·  **اَ۬لسَّمَآءِ** duri  ·  **ࡱ۬لسَّمَآءِ** susi  ·  **ٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 76485 | 89:16 | `رٮى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `رٮٮى` ibn-wardan,ibn-jammaz | **رَبِّيٓ** hafs,shubah  ·  **رَبِّيَ** bazzi,qalun,warsh,duri  ·  **رَّبِّيَ** susi  ·  **رَبِّٜيٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **رَبِّٜيي** ibn-wardan,ibn-jammaz  ·  **رَبِّٜي** ruways,rawh |
| 76516 | 89:23 | `وحاى` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وحى` qalun,warsh,ibn-wardan,ibn-jammaz | **وَجِاْيٓءَ** hafs,shubah,bazzi,duri,susi  ·  **وَجِےٓءَ** qalun,warsh  ·  **وَجاْىٓءَ** hisham,abu-al-harith,ruways  ·  **وَّجِاْىٓءَ** khalaf  ·  **وَجِاْىٓءَ** khallad,rawh,ishaq  ·  **وَجِيٓءَ** ibn-wardan,ibn-jammaz |
| 76600 | 90:14 | `اطعم` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `اطعام` qalun,warsh,ibn-wardan,ibn-jammaz | **إِطۡعَٰمࣱ** hafs,shubah  ·  **أَطۡعَمَ** bazzi,duri,susi  ·  **إِطْعَامࣱ** qalun,ibn-wardan,ibn-jammaz  ·  **ࡴطْعَامࣱ** warsh  ·  **إِطْعَٰمࣱ** hisham,khalaf,khallad,ruways,rawh,ishaq  ·  **أَطْعَمَ** abu-al-harith |
| 76644 | 91:5 | `والسما` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `والسماا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **وَٱلسَّمَآءِ** hafs,shubah,bazzi  ·  **وَالسَّمَآءِ** qalun,warsh  ·  **وَاَلسَّمَآءِ** duri  ·  **وَࡱلسَّمَآءِ** susi  ·  **وَٱلسَّمَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 76721 | 92:11 | `ٮردى` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  `ٮردٮى` ruways,rawh | **تَرَدَّىٰٓ** hafs,shubah  ·  **تَرَدَّىٰ** bazzi,qalun  ·  **تَرَدّٜىٰٓ** warsh  ·  **تَرَدّۭيٰٓ** duri  ·  **تَرَدّ۪ىٰ** susi  ·  **تَرَدَّىٰٓ** hisham  ·  **تَرَدّٜ۪ىٰٓ** khalaf,khallad,abu-al-harith,ishaq  ·  **تَرَدَّىٰ** ibn-wardan,ibn-jammaz  ·  **تَرَدَّىى** ruways,rawh |
| 77267 | 106:2 | `الڡهم` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اٮلڡهم` qalun,warsh | **إِۦلَٰفِهِمۡ** hafs,shubah,duri,susi  ·  **إِۦلَٰفِهِمُۥ** bazzi  ·  **إِيلَٰفِهِمْ** qalun  ·  **ࡴيلَٰفِهِمْ** warsh  ·  **إِۦلَٰفِهِمْ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **إِلَٰفِهِمۥُ** ibn-wardan,ibn-jammaz |
| 77269 | 106:2 | `السٮا` hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  `السٮاا` hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **ٱلشِّتَآءِ** hafs,shubah,bazzi  ·  **ࡰ۬لشِّتَآءِ** qalun,warsh  ·  **اَ۬لشِّتَآءِ** duri  ·  **ࡱ۬لشِّتَآءِ** susi  ·  **ٱلشِّتَآآءِ** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |

#### One letter for another

22 of the 842, where a letter is not added but exchanged — `ولا`/`ڡلا` (وَلَا against فَلَا, 91:15), `كلمٮ`/`كلمه` (the open against the tied tāʾ, 7:137).

| word id | sūrah:āyah | rasm on each side | as printed |
|---|---|---|---|
| 14124 | 5:28 | `ٮدى` hafs,shubah,bazzi,qalun,warsh,duri,susi,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `ٮدٮا` hisham  ·  `ٮدٮى` khalaf | **يَدِيَ** hafs,qalun,warsh,duri,susi  ·  **يَدِيٓ** shubah  ·  **يَدِي** bazzi  ·  **يَدِىا** hisham  ·  **يَّدِىي** khalaf  ·  **يَدِىٓ** khallad,abu-al-harith,ishaq  ·  **يَدِىَ** ibn-wardan,ibn-jammaz  ·  **يَدِى** ruways,rawh |
| 18564 | 6:137 | `سركاوهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `سركاٮهم` hisham | **شُرَكَآؤُهُمۡ** hafs,shubah,duri,susi  ·  **شُرَكَآؤُهُمُۥ** bazzi  ·  **شُرَكَآؤُهُمْ** qalun,warsh  ·  **شُرَكَآئِهِمْ** hisham  ·  **شُرَكَآؤُهُمْ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **شُرَكَآؤُهُمۥُ** ibn-wardan,ibn-jammaz |
| 21271 | 7:137 | `كلمٮ` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `كلمه` qalun,warsh,ibn-wardan,ibn-jammaz | **كَلِمَتُ** hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **كَلِمَةُ** qalun,warsh,ibn-wardan,ibn-jammaz |
| 21331 | 7:141 | `اٮحٮٮكم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `اٮحاكم` hisham | **أَنجَيۡنَٰكُم** hafs,shubah,duri,susi  ·  **أَنجَيۡنَٰكُمُۥ** bazzi  ·  **أَنجَيْنَٰكُم** qalun,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ࡰنجَيْنَٰكُم** warsh  ·  **أَنجَاكُم** hisham  ·  **أَنجَيْنَٰكُمۥُ** ibn-wardan,ibn-jammaz |
| 36089 | 17:7 | `لٮسوا` hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `لٮس‍وا` duri,susi  ·  `لٮسووا` ibn-wardan,ibn-jammaz,ruways,rawh | **لِيَسُـُٔواْ** hafs,bazzi,qalun,warsh  ·  **لِيَسُوٓأَ** shubah,hisham,khalaf,khallad,ishaq  ·  **لِيَسُ‍ُٔواْ** duri,susi  ·  **لِنَسُوٓأَ** abu-al-harith  ·  **لِيَسُوُٓٔواْ** ibn-wardan,ibn-jammaz,ruways,rawh |
| 44767 | 23:101 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡلٮل` ibn-wardan,ibn-jammaz,ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَليل** ibn-wardan,ibn-jammaz,ruways,rawh |
| 48384 | 26:217 | `وٮوكل` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡٮوكل` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **وَتَوَكَّلۡ** hafs,shubah,bazzi,duri,susi  ·  **فَتَوَكَّلْ** qalun,warsh  ·  **فَتَوَكَّلْ** hisham,ibn-wardan,ibn-jammaz  ·  **وَتَوَكَّلْ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 52076 | 30:8 | `ٮلڡاى` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮلڡا` qalun,warsh  ·  `ٮلڡاا` ibn-wardan,ibn-jammaz | **بِلِقَآيِٕ** hafs,shubah,bazzi,duri,susi  ·  **بِلِقَآءِ** qalun,warsh  ·  **بِلِقَآءِيْ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **بِلِقَآآءِ** ibn-wardan,ibn-jammaz |
| 52165 | 30:16 | `ولڡاى` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ولڡا` qalun,warsh  ·  `ولڡاا` ibn-wardan,ibn-jammaz | **وَلِقَآيِٕ** hafs,shubah,bazzi,duri,susi  ·  **وَلِقَآءِ** qalun,warsh  ·  **وَلِقَآءِيْ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَلِقَآآءِ** ibn-wardan,ibn-jammaz |
| 54947 | 33:67 | `السٮٮلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `السٮٮلٮل` ibn-wardan,ibn-jammaz | **ٱلسَّبِيلَا۠** hafs,bazzi  ·  **ٱلسَّبِيلَا** shubah  ·  **ࡰ۬لسَّبِيلَا** qalun,warsh  ·  **اَ۬لسَّبِيلَاْ** duri  ·  **ࡱ۬لسَّبِيلَاْ** susi  ·  **ٱلسَّبِيلاَ** hisham  ·  **ٱلسَّبِيلَاْ** khalaf  ·  **ٱلسَّبِيلا۠** khallad,ishaq  ·  **ٱلسَّبِيل۠اَ** abu-al-harith  ·  **ٱلسَّبِيليل** ibn-wardan,ibn-jammaz  ·  **ٱلسَّبِيلّاَ** ruways,rawh |
| 60457 | 40:21 | `مٮهم` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `مٮكم` hisham | **مِنۡهُمۡ** hafs,shubah,duri,susi  ·  **مِنۡهُمُۥ** bazzi  ·  **مِنْهُمْ** qalun,warsh,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **مِنكُمْ** hisham  ·  **مِنْهُمۥُ** ibn-wardan,ibn-jammaz |
| 68586 | 55:12 | `دو` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `دا` hisham | **ذُو** hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **ذَا** hisham |
| 68797 | 55:54 | `وحٮى` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وحٮا` qalun,warsh,ibn-wardan,ibn-jammaz | **وَجَنَى** hafs,shubah,bazzi,duri,susi  ·  **وَجَنَا** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **وَجَنَي** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَّجَنَي** khalaf |
| 68898 | 55:78 | `دى` hafs,shubah,bazzi,qalun,warsh,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  `دو` hisham | **ذِي** hafs,shubah,bazzi,duri,susi,ibn-wardan,ibn-jammaz  ·  **ذِے** qalun,warsh  ·  **ذُو** hisham  ·  **ذِى** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 69187 | 56:75 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡلٮل` ibn-wardan,ibn-jammaz,ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَليل** ibn-wardan,ibn-jammaz,ruways,rawh |
| 73299 | 69:38 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡلٮل` ibn-wardan,ibn-jammaz,ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَليل** ibn-wardan,ibn-jammaz,ruways,rawh |
| 73540 | 70:40 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡلٮل` ibn-wardan,ibn-jammaz,ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَليل** ibn-wardan,ibn-jammaz,ruways,rawh |
| 73958 | 72:16 | `والو` hafs,shubah,bazzi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `واں` qalun,warsh,duri,susi  ·  `واٮلو` ibn-wardan,ibn-jammaz | **وَأَلَّوِ** hafs,shubah,bazzi  ·  **وَأَن** qalun,warsh,duri,susi  ·  **وَأَلَّوِ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَّأَلَّوِ** khalaf  ·  **وَأَنلَّوِ** ibn-wardan,ibn-jammaz |
| 75663 | 81:15 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡلٮل` ibn-wardan,ibn-jammaz,ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَليل** ibn-wardan,ibn-jammaz,ruways,rawh |
| 75698 | 81:24 | `ٮصٮٮں` hafs,shubah,qalun,warsh,hisham,khalaf,khallad,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  `ٮصطٮٮں` bazzi,duri,susi  ·  `ٮطٮٮں` abu-al-harith,ruways | **بِضَنِينࣲ** hafs,shubah,qalun,warsh,hisham,khalaf,khallad,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **بِضظَنِينࣲ** bazzi  ·  **بِضظَنِينٖ** duri  ·  **بِّضظَنِينࣲ** susi  ·  **بِظنِينࣲ** abu-al-harith,ruways |
| 76037 | 84:16 | `ڡلا` hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  `ڡلٮل` ibn-wardan,ibn-jammaz,ruways,rawh | **فَلَآ** hafs,shubah,warsh,duri  ·  **فَلَا** bazzi,qalun,susi  ·  **فَلَآ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **فَليلَ** ibn-wardan,ibn-jammaz  ·  **فَليل** ruways,rawh |
| 76684 | 91:15 | `ولا` hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡلا` qalun,warsh,hisham,ibn-wardan,ibn-jammaz | **وَلَا** hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **فَلَا** qalun,warsh,hisham  ·  **فَلاَ** ibn-wardan,ibn-jammaz |

### The ā on the line or above it

197 words whose skeletons agree once every ā is spelled out, and differ only because one hand wrote that ā on the line and the other wrote it above: the Warsh/Qālūn set prints `هَارُوتَ` and `مُبَٰرَك` where the Kūfī set prints `هَٰرُوتَ` and `مُبَارَك`.

They are not counted as the codices disagreeing, and the reason is in the data rather than in a judgement about it. **All 197 split the riwāyāt 5 different ways.** The 842 real letter differences split them 62 different ways. Ḥadhf and ithbāt al-alif do vary between the codices of the amṣār, but they do not put Makkah with Madinah 197 times out of 197 and never once apart; a publisher's house style does. Bazzī goes its own way 6 times among the 842 and not once among these.

The distinction is still kept in `rasm`, because inside any one muṣḥaf it is that muṣḥaf's own ḥadhf, carried consistently: Ḥafṣ writes قال plene 412 times and defective 4, سبحان defective 12 and plene once, and 173 of these 197 words show the identical split at *every* occurrence of the word in the corpus. What the sources cannot answer is which of the two hands is the codex's. A sample:

| word id | sūrah:āyah | rasm on each side | as printed |
|---|---|---|---|
| 425 | 2:28 | `ڡاحٮكم` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ڡاحٮاكم` qalun,warsh,ibn-wardan,ibn-jammaz | **فَأَحۡيَٰكُمۡ** hafs,shubah,duri,susi  ·  **فَأَحۡيَٰكُمُۥ** bazzi  ·  **فَأَحْيَاكُمْ** qalun  ·  **فَأَحْيٜاكُمْ** warsh  ·  **فَأَحْيَٰكُمْ** hisham,khalaf,khallad,ruways,rawh,ishaq  ·  **فَأَحْيٰ۪كُمْ** abu-al-harith  ·  **فَأَحْيَاكُمۥُ** ibn-wardan,ibn-jammaz |
| 618 | 2:40 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh  ·  **إِسْرَٰٓآءِيلَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **إِسْرَايلَ** ibn-wardan,ibn-jammaz |
| 690 | 2:47 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh  ·  **إِسْرَٰٓآءِيلَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **إِسْرَايلَ** ibn-wardan,ibn-jammaz |
| 823 | 2:57 | `العمام` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `العمم` qalun,warsh,ibn-wardan,ibn-jammaz | **ٱلۡغَمَامَ** hafs,shubah,bazzi  ·  **ࡲ۬لْغَمَٰمَ** qalun,warsh  ·  **اُ۬لۡغَمَامَ** duri  ·  **ࡲ۬لۡغَمَامَ** susi  ·  **ٱلْغَمَامَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْغَمَٰمَ** ibn-wardan,ibn-jammaz |
| 1333 | 2:83 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri  ·  **إِسْرَآءِيلَ** qalun,warsh  ·  **إِسۡرَٰٓءِيل** susi  ·  **إِسْرَٰٓآءِيلَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **إِسْرَايلَ** ibn-wardan,ibn-jammaz |
| 1339 | 2:83 | `احساٮا` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `احسٮا` qalun,warsh,ibn-wardan,ibn-jammaz | **إِحۡسَانࣰا** hafs,shubah,bazzi,susi  ·  **إِحْسَٰناࣰ** qalun,warsh  ·  **إِحۡسَانٗا** duri  ·  **إِحْسَانࣰا** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **إِحْسَٰنࣰا** ibn-wardan,ibn-jammaz |
| 1738 | 2:102 | `هروٮ` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `هاروٮ` qalun,warsh,ibn-wardan,ibn-jammaz | **هَٰرُوتَ** hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **هَارُوتَ** qalun,warsh,ibn-wardan,ibn-jammaz |
| 1739 | 2:102 | `ومروٮ` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `وماروٮ` qalun,warsh,ibn-wardan,ibn-jammaz | **وَمَٰرُوتَ** hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَمَارُوتَ** qalun,warsh,ibn-wardan,ibn-jammaz |
| 1741 | 2:102 | `ٮعلماں` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮعلمں` qalun,warsh,ibn-wardan,ibn-jammaz | **يُعَلِّمَانِ** hafs,shubah,bazzi,duri,susi  ·  **يُعَلِّمَٰنِ** qalun,warsh  ·  **يُعَلِّمَانِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يُعَلِّمَٰنِ** ibn-wardan,ibn-jammaz |
| 2147 | 2:121 | `ٮلاوٮه` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `ٮلوٮه` qalun,warsh,ibn-wardan,ibn-jammaz | **تِلَاوَتِهِۦٓ** hafs,shubah,duri,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **تِلَاوَتِهِۦ** bazzi,susi  ·  **تِلَٰوَتِهِۦ** qalun,ibn-wardan,ibn-jammaz  ·  **تِلَٰوَتِهِۦٓ** warsh  ·  **تِلاَوَتِهِۦ** ruways,rawh |
| 2158 | 2:122 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh  ·  **إِسْرَٰٓآءِيلَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **إِسْرَايلَ** ibn-wardan,ibn-jammaz |
| 2824 | 2:158 | `سعاٮر` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `سعٮر` qalun,warsh,ibn-wardan,ibn-jammaz | **شَعَآئِرِ** hafs,shubah,bazzi,duri,susi  ·  **شَعَٰٓئِرِ** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **شَعَآئِرِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 2991 | 2:166 | `الاسٮاٮ` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `الاسٮٮ` qalun,warsh,ibn-wardan,ibn-jammaz | **ٱلۡأَسۡبَابُ** hafs,shubah,bazzi  ·  **ࡲ۬لْأَسْبَٰبُ** qalun  ·  **ࡲ۬لَاسْبَٰبُ** warsh  ·  **اِ۬لۡأَسۡبَابُ** duri  ·  **ࡵ۬لۡأَسۡبَابُ** susi  ·  **ٱلْأَسْبَابُ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلأَْسْبَٰبُ** ibn-wardan,ibn-jammaz  ·  **ٱلأَْسْبَابُ** ruways,rawh |
| 3929 | 2:210 | `العمام` hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  `العمم` qalun,warsh,ibn-wardan,ibn-jammaz | **ٱلۡغَمَامِ** hafs,shubah,bazzi  ·  **ࡰ۬لْغَمَٰمِ** qalun,warsh  ·  **اَ۬لۡغَمَامِ** duri  ·  **ࡱ۬لۡغَمَامِ** susi  ·  **ٱلْغَمَامِ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **ٱلْغَمَٰمِ** ibn-wardan,ibn-jammaz |
| 3939 | 2:211 | `اسرٮل` hafs,shubah,bazzi,duri,susi  ·  `اسراٮل` qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq | **إِسۡرَٰٓءِيلَ** hafs,shubah,bazzi,duri,susi  ·  **إِسْرَآءِيلَ** qalun,warsh  ·  **إِسْرَٰٓآءِيلَ** hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **إِسْرَايلَ** ibn-wardan,ibn-jammaz |

### Pointing — one rasm, two qiraahs

919 words share a rasm but are pointed differently. These are real differences in qiraah, not in the codex: an undotted skeleton carries them all. A sample:

| word id | sūrah:āyah | shared rasm | pointed as |
|---|---|---|---|
| 11 | 1:4 | `ملك` | **مالك** hafs,shubah,abu-al-harith,ruways,rawh,ishaq  ·  **ملك** bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,ibn-wardan,ibn-jammaz |
| 105 | 2:9 | `ٮحدعوں` | **يخدعون** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يخادعون** bazzi,qalun,warsh,duri,susi |
| 233 | 2:19 | `محٮط` | **محيط** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **محيطا** ibn-wardan,ibn-jammaz,ruways,rawh |
| 445 | 2:29 | `ڡسوٮهں` | **فسوياهن** hafs,shubah,bazzi,qalun,warsh,duri,susi  ·  **فسويهن** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 560 | 2:36 | `ڡارلهما` | **فازلهما** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **فازالهما** khalaf,khallad |
| 709 | 2:48 | `ٮڡٮل` | **يقبل** hafs,shubah,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **تقبل** bazzi,duri,susi,ruways,rawh |
| 748 | 2:51 | `وعدٮا` | **واعدنا** hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **وعدنا** duri,susi,ibn-wardan,ibn-jammaz,ruways,rawh |
| 854 | 2:58 | `ٮعڡر` | **نغفر** hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يغفر** qalun,warsh,ibn-wardan,ibn-jammaz  ·  **تغفر** hisham |
| 1074 | 2:68 | `عواں` | **عوان** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **عوانا** ibn-wardan,ibn-jammaz,ruways,rawh |
| 1142 | 2:72 | `ڡادرٮم` | **فاداراتم** hafs,shubah,bazzi,qalun,duri,susi  ·  **فادارتم** warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 1196 | 2:74 | `ٮعملوں` | **تعملون** hafs,shubah,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يعملون** bazzi |
| 1312 | 2:81 | `حطٮٮه` | **خطيته** hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **خطياته** qalun,warsh,ibn-wardan,ibn-jammaz |
| 1335 | 2:83 | `ٮعٮدوں` | **تعبدون** hafs,shubah,qalun,warsh,duri,susi,hisham,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **يعبدون** bazzi,khalaf,khallad,abu-al-harith |
| 1389 | 2:85 | `اسرى` | **اساريا** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **اسريا** khalaf,khallad |
| 1390 | 2:85 | `ٮڡدوهم` | **تفادوهم** hafs,shubah,qalun,warsh,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh  ·  **تفدوهم** bazzi,duri,susi,hisham,khalaf,khallad,ishaq |

### Boundaries — where the space falls

A boundary disagreement is never about one word; it is about the space between two. Each event below shows the whole run, exactly as each riwāyah prints it. The last column is the one that matters: **agree** means every riwāyah reads the run identically once it is re-segmented, so the flag is a *source* that lost a space, not a muṣḥaf that really prints the words joined.

**2:12** — word ids 133, 134 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | أَلَآ إِنَّهُمۡ |
| `bazzi` | أَلَا إِنَّهُمُۥ |
| `qalun` | أَلَا إِنَّهُمْ |
| `warsh` | أَلَآ إِنَّهُمْ |
| `susi` | أَلَا إِنَّهُمۡ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّهُمْ |
| `ibn-wardan,ibn-jammaz` | أَلَا إِنَّهُمۥُ |
| `ruways,rawh` | أَلَا إِنَّهُمْ |

**2:13** — word ids 152, 153 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | أَلَآ إِنَّهُمۡ |
| `bazzi` | ࡶَلَا إِنَّهُمُۥ |
| `qalun` | ࡶَلَا إِنَّهُمْ |
| `warsh` | ࡶَلَآ إِنَّهُمْ |
| `duri` | اَ۬لَآ إِنَّهُمۡ |
| `susi` | ࡶَلَا إِنَّهُمۡ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّهُمْ |
| `ibn-wardan,ibn-jammaz` | ٱلَا إِنَّهُمۥُ |
| `ruways` | ٱلَا إِنَّهُمْ |
| `rawh` | أَلَا إِنَّهُمْ |

**2:102** — word ids 1745, 1746 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | يَقُولَآ إِنَّمَا |
| `bazzi,qalun,susi` | يَقُولَا إِنَّمَا |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | يَقُولَآ إِنَّمَا |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | يَقُولَا إِنَّمَا |

**2:114** — word ids 2031, 2032 · joined in `rawh` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri,susi` | لَهُمۡ فِي |
| `bazzi` | لَهُمُۥ فِي |
| `qalun,warsh` | لَهُمْ فِے |
| `hisham,khalaf,khallad,abu-al-harith,ruways,ishaq` | لَهُمْ فِي |
| `ibn-wardan,ibn-jammaz` | لَهُمۥُ فِي |
| `rawh` | لَهُم فِْي |

**2:181** — word ids 3289, 3290 · joined in `abu-al-harith`, `hisham`, `ibn-jammaz`, `ibn-wardan`, `ishaq`, `khalaf`, `khallad`, `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi` | بَعۡدَ مَا |
| `qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq` | بَعْدَ مَا |

**2:214** — word ids 4051, 4052 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَلَآ إِنَّ |
| `bazzi,qalun,susi` | أَلَا إِنَّ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّ |
| `ibn-wardan,ibn-jammaz` | أَلاَ إِنَّ |
| `ruways,rawh` | أَلَا إِنَّ |

**2:224** — word ids 4318, 4319 · joined in `khalaf` · **the riwāyāt differ** (a real difference)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi` | وَتُصۡلِحُواْ |
| `qalun,warsh,hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh` | وَتُصْلِحُواْ |
| `khalaf,abu-al-harith,ishaq` | وَ تُصْلِحُواْ |

**2:255** — word ids 5176, 5177, 5178 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | ٱللَّهُ لَآ إِلَٰهَ |
| `bazzi` | ٱللَّهُ لَا إِلَٰهَ |
| `qalun` | ࡰ۬للَّهُ لَا إِلَٰهَ |
| `warsh` | ࡰ۬للَّهُ لَآ إِلَٰهَ |
| `duri` | اَ۬للَّهُ لَآ إِلَٰهَ |
| `susi` | ࡱ۬للَّهُ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | ٱلله لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | ٱللَّهُ لَا إِلَٰهَ |

**2:256** — word ids 5226, 5227 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَآ إِكۡرَاهَ |
| `bazzi,susi` | لَا إِكۡرَاهَ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَا إِكْرَاهَ |
| `warsh` | لَآ إِكْرَاهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَآ إِكْرَاهَ |

**2:262** — word ids 5459, 5460 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | وَلَآ أَذࣰى |
| `bazzi,susi,ibn-wardan,ibn-jammaz,ruways,rawh` | وَلَا أَذࣰى |
| `qalun` | وَلَا أَذىࣰ |
| `warsh` | وَلَآ أَذىࣰ |
| `duri` | وَلَآ أَذٗى |
| `hisham,khallad,abu-al-harith,ishaq` | وَلَآ أَذࣰىِۢ |
| `khalaf` | وَّلَآ أَذࣰىِۢ |

**3:2** — word ids 6149, 6150, 6151 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | ٱللَّهُ لَآ إِلَٰهَ |
| `bazzi` | ٱللَّهُ لَا إِلَٰهَ |
| `qalun` | ࡰ۬للَّهُ لَا إِلَٰهَ |
| `warsh` | ࡰ۬للَّهُ لَآ إِلَٰهَ |
| `duri` | اَ۬للَّهُ لَآ إِلَٰهَ |
| `susi` | ࡱ۬للَّهُ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | ٱلله لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz` | ٱللَّهُ لاَ إِلَٰهَ |
| `ruways,rawh` | ٱللَّهُ لَا إِلَٰهَ |

**3:6** — word ids 6202, 6203, 6204 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | يَشَآءُ لَآ إِلَٰهَ |
| `bazzi,qalun,susi` | يَشَآءُ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | يَشَآءُ لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz` | يَشَآءُ لاَ إِلَٰهَ |
| `ruways,rawh` | يَشَآءُ لَا إِلَٰهَ |

**3:10** — word ids 6290, 6291 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَوۡلَٰدُهُم |
| `bazzi` | وَلَا أَوۡلَٰدُهُمُۥ |
| `qalun,ruways,rawh` | وَلَا أَوْلَٰدُهُم |
| `warsh` | وَلَآ أَوْلَٰدُهُم |
| `susi` | وَلَا أَوۡلَٰدُهُم |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَوْلَٰدُهُم |
| `ibn-wardan,ibn-jammaz` | وَلَا أَوْلَٰدُهُمۥُ |

**3:18** — word ids 6418, 6419, 6420 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَنَّهُۥ لَآ إِلَٰهَ |
| `bazzi,qalun,susi` | أَنَّهُۥ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَنَّهُۥ لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَنَّهُۥ لَا إِلَٰهَ |

**3:18** — word ids 6427, 6428, 6429 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | بِٱلۡقِسۡطِ لَآ إِلَٰهَ |
| `bazzi` | بِٱلۡقِسۡطِ لَا إِلَٰهَ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | بِالْقِسْطِ لَا إِلَٰهَ |
| `warsh` | بِالْقِسْطِ لَآ إِلَٰهَ |
| `duri` | بِالۡقِسۡطِ لَآ إِلَٰهَ |
| `susi` | بِالۡقِسۡطِ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | بِالْقِسْطِ لَآ إِلَٰهَ |

**3:116** — word ids 8105, 8106 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَوۡلَٰدُهُم |
| `bazzi` | وَلَا أَوۡلَٰدُهُمُۥ |
| `qalun,ruways,rawh` | وَلَا أَوْلَٰدُهُم |
| `warsh` | وَلَآ أَوْلَٰدُهُم |
| `susi` | وَلَا أَوۡلَٰدُهُم |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَوْلَٰدُهُم |
| `ibn-wardan,ibn-jammaz` | ولَا أَوْلَٰدُهُمۥُ |

**3:183** — word ids 9312, 9313 · joined in `abu-al-harith` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | قَدۡ جَآءَكُمۡ |
| `bazzi` | قَدۡ جَآءَكُمُۥ |
| `qalun,warsh` | قَدْ جَآءَكُمْ |
| `duri,susi` | قَد جَّآءَكُمۡ |
| `hisham,abu-al-harith` | قَد جَّآءَكُمْ |
| `khalaf,khallad,ishaq` | قَد جّٜ۪آءَكُمْ |
| `ibn-wardan,ibn-jammaz` | قَدْ جَآءَكُمۥُ |
| `ruways,rawh` | قَدْ جَآءَكُمْ |

**3:188** — word ids 9405, 9406 · joined in `hisham` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | لَا تَحۡسَبَنَّ |
| `bazzi,duri,susi` | لَا يَحۡسِبَنَّ |
| `qalun,warsh` | لَا يَحْسِبَنَّ |
| `hisham,ibn-wardan,ibn-jammaz` | لَا يَحْسَبَنَّ |
| `khalaf,khallad` | لَا تَحْسَبَنَّ |
| `abu-al-harith,ruways,rawh,ishaq` | لَا تَحْسِبَنَّ |

**4:77** — word ids 11316, 11317 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أَخَّرۡتَنَآ |
| `bazzi` | لَوۡلَا أَخَّرۡتَنَا |
| `qalun` | لَوْلَا أَخَّرْتَنَا |
| `warsh` | لَوْلَآ أَخَّرْتَنَآ |
| `susi` | لَّوۡلَا أَخَّرۡتَنَا |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أَخَّرْتَنَآ |
| `ibn-wardan,ibn-jammaz` | لَولَا أَخَّرْتَنَا |
| `ruways,rawh` | لَوْلَا أَخَّرْتَنَا |

**4:87** — word ids 11524, 11525, 11526 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | ٱللَّهُ لَآ إِلَٰهَ |
| `bazzi` | ٱللَّهُ لَا إِلَٰهَ |
| `qalun` | ࡴ۬للَّهُ لَا إِلَٰهَ |
| `warsh` | ࡴ۬للَّهُ لَآ إِلَٰهَ |
| `duri` | اِ۬للَّهُ لَآ إِلَٰهَ |
| `susi` | ࡵ۬للَّهُ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | ٱلله لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | ٱللَّهُ لَا إِلَٰهَ |

**4:91** — word ids 11635, 11636 · joined in `duri`, `qalun` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | مَا رُدُّوٓاْ |
| `bazzi,qalun,susi` | مَا رُدُّواْ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | مَا رُدُّوٓاْ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | مَا رُدُّواْ |

**4:123** — word ids 12311, 12312 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | وَلَآ أَمَانِيِّ |
| `bazzi,qalun,susi` | وَلَا أَمَانِيِّ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَمَانِيِّٜ |
| `ibn-wardan,ibn-jammaz` | وَلَا أَمَانِي |
| `ruways,rawh` | وَلَا أَمَانِيِّٜ |

**4:174** — word ids 13302, 13303 · joined in `hisham` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | قَدۡ جَآءَكُم |
| `bazzi` | قَدۡ جَآءَكُمُۥ |
| `qalun,warsh` | قَدْ جَآءَكُم |
| `duri,susi` | قَد جَّآءَكُم |
| `hisham,abu-al-harith` | قَد جَّآءَكُم |
| `khalaf,ishaq` | قَد جّٜ۪آءَكُم |
| `khallad` | قَد جَّ۪آءَكُم |
| `ibn-wardan,ibn-jammaz` | قَدْ جَآءَكُمۥُ |
| `ruways,rawh` | قَدْ جَآءَكُم |

**5:2** — word ids 13413, 13414 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | وَلَآ ءَآمِّينَ |
| `bazzi,qalun,susi` | وَلَا ءَآمِّينَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ ءَآمِّٜينَ |
| `ibn-wardan,ibn-jammaz` | وَلَا ءَآمِّٜينَ |
| `ruways,rawh` | وَلَاءَ آمِّٜينَ |

**5:116** — word ids 16096, 16097 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَعۡلَمُ |
| `bazzi` | وَلَا أَعۡلَمُ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | وَلَا أَعْلَمُ |
| `warsh` | وَلَآ أَعْلَمُ |
| `susi` | وَلَا أَعۡلَم |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَعْلَمُ |

**6:8** — word ids 16291, 16292 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أُنزِلَ |
| `bazzi,susi` | لَوۡلَا أُنزِلَ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَوْلَا أُنزِلَ |
| `warsh` | لَوْلَآ أُنزِلَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أُنزِلَ |

**6:43** — word ids 16845, 16846 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | فَلَوۡلَآ إِذۡ |
| `bazzi` | فَلَوۡلَا إِذۡ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | فَلَوْلَا إِذْ |
| `warsh` | فَلَوْلَآ إِذْ |
| `duri` | فَلَوۡلَآ إِذ |
| `susi` | فَلَوۡلَا إِذ |
| `hisham` | فَلَوْلَآ إِذ |
| `khalaf,khallad,abu-al-harith,ishaq` | فَلَوْلَآ إِذْ |

**6:50** — word ids 16958, 16959 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | وَلَآ أَقُولُ |
| `bazzi,qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | وَلَا أَقُولُ |
| `susi` | وَلَا أَقُول |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَقُولُ |

**6:76** — word ids 17458, 17459, 17460 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | قَالَ لَآ أُحِبُّ |
| `bazzi,qalun` | قَالَ لَا أُحِبُّ |
| `susi` | قَال لَّا أُحِبُّ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | قَالَ لَآ أُحِبُّ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | قَالَ لَا أُحِبُّ |

**6:80** — word ids 17517, 17518 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | وَلَآ أَخَافُ |
| `bazzi,qalun,susi,ibn-wardan,ibn-jammaz,ruways,rawh` | وَلَا أَخَافُ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَخَافُ |

**6:91** — word ids 17710, 17711 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ ءَابَآؤُكُمۡ |
| `bazzi` | وَلَا ءَابَآؤُكُمُۥ |
| `qalun` | وَلَا ءَابَآؤُكُمْ |
| `warsh` | وَلَآ ءَابَآؤُكُمْ |
| `susi` | وَلَا ءَابَآؤُكُمۡ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ ءَابَآؤُكُمْ |
| `ibn-wardan,ibn-jammaz` | وَلَا ءَابَآؤُكُمۥُ |
| `ruways,rawh` | وَلَاءَ ابَآؤُكُمْ |

**6:102** — word ids 17956, 17957, 17958 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | رَبُّكُمۡ لَآ إِلَٰهَ |
| `bazzi` | رَبُّكُمُۥ لَا إِلَٰهَ |
| `qalun` | رَبُّكُمْ لَا إِلَٰهَ |
| `warsh` | رَبُّكُمْ لَآ إِلَٰهَ |
| `susi` | رَبُّكُمۡ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | رَبُّكُمْ لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz` | رَبُّكُمۥُ لَا إِلَٰهَ |
| `ruways,rawh` | رَبُّكُمْ لَا إِلَٰهَ |

**6:106** — word ids 18007, 18008, 18009 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | رَّبِّكَ لَآ إِلَٰهَ |
| `bazzi,qalun,susi` | رَّبِّكَ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | رَّبِّٜكَ لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | رَّبِّٜكَ لَا إِلَٰهَ |

**6:148** — word ids 18843, 18844 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | وَلَآ ءَابَآؤُنَا |
| `bazzi,qalun,susi` | وَلَا ءَابَآؤُنَا |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ ءَابَآؤُنَا |
| `ibn-wardan,ibn-jammaz` | وَلَا ءَابَآؤُنَا |
| `ruways,rawh` | وَلَاءَ ابَآؤُنَا |

**7:43** — word ids 19888, 19889 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أَنۡ |
| `bazzi,susi` | لَوۡلَا أَنۡ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَوْلَا أَنْ |
| `warsh` | لَوْلَآ أَنْ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أَنْ |

**7:49** — word ids 20000, 20001 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَنتُمۡ |
| `bazzi` | وَلَا أَنتُمُۥ |
| `qalun,ruways,rawh` | وَلَا أَنتُمْ |
| `warsh` | وَلَآ أَنتُمْ |
| `susi` | وَلَا أَنتُمۡ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَنتُمْ |
| `ibn-wardan,ibn-jammaz` | وَلَا أَنتُمۥُ |

**7:98** — word ids 20820, 20821 · joined in `ibn-wardan` · **the riwāyāt differ** (a real difference)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri,susi,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq` | أَوَأَمِنَ |
| `bazzi` | أَوۡأَمِنَ |
| `qalun,hisham` | أَوْأَمِنَ |
| `warsh` | أَوَࡰمِنَ |
| `ibn-wardan,ibn-jammaz` | أَوْ أَمِنَ |

**7:131** — word ids 21181, 21182 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَلَآ إِنَّمَا |
| `bazzi,qalun,susi` | أَلَا إِنَّمَا |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّمَا |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَلَا إِنَّمَا |

**7:158** — word ids 21755, 21756, 21757 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | وَٱلۡأَرۡضِ لَآ إِلَٰهَ |
| `bazzi` | وَٱلۡأَرۡضِ لَا إِلَٰهَ |
| `qalun` | وَالْأَرْضِ لَا إِلَٰهَ |
| `warsh` | وَالَارْضِ لَآ إِلَٰهَ |
| `duri` | وَاَلۡأَرۡضِ لَآ إِلَٰهَ |
| `susi` | وَࡱلۡأَرۡضِ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَٱلْأَرْضِ لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | وَٱلأَْرْضِ لَا إِلَٰهَ |

**7:192** — word ids 22371, 22372 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَنفُسَهُمۡ |
| `bazzi` | وَلَا أَنفُسَهُمُۥ |
| `qalun,ruways,rawh` | وَلَا أَنفُسَهُمْ |
| `warsh` | وَلَآ أَنفُسَهُمْ |
| `susi` | وَلَا أَنفُسَهُمۡ |
| `hisham,khallad,abu-al-harith,ishaq` | وَلَآ أَنفُسَهُمْ |
| `khalaf` | وَّلَآ أَنفُسَهُمْ |
| `ibn-wardan,ibn-jammaz` | وَلَا أَنفُسَهُمۥُ |

**7:197** — word ids 22442, 22443 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَنفُسَهُمۡ |
| `bazzi` | وَلَا أَنفُسَهُمُۥ |
| `qalun,ruways,rawh` | وَلَا أَنفُسَهُمْ |
| `warsh` | وَلَآ أَنفُسَهُمْ |
| `susi` | وَلَا أَنفُسَهُمۡ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَنفُسَهُمْ |
| `ibn-wardan,ibn-jammaz` | وَلَا أَنفُسَهُمۥُ |

**9:12** — word ids 23993, 23994, 23995 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | إِنَّهُمۡ لَآ أَيۡمَٰنَ |
| `bazzi` | إِنَّهُمُۥ لَا أَيۡمَٰنَ |
| `qalun` | إِنَّهُمْ لَا أَيْمَٰنَ |
| `warsh` | إِنَّهُمْ لَآ أَيْمَٰنَ |
| `susi` | إِنَّهُمۡ لَا أَيۡمَٰنَ |
| `hisham` | إِنَّهُمْ لَآ إِيمَٰنَ |
| `khalaf,khallad,abu-al-harith,ishaq` | إِنَّهُمْ لَآ أَيْمَٰنَ |
| `ibn-wardan,ibn-jammaz` | إِنَّهُمۥُ لَا أَيْمَٰنَ |
| `ruways,rawh` | إِنَّهُمْ لَا أَيْمَٰنَ |

**9:55** — word ids 24832, 24833 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَوۡلَٰدُهُمۡ |
| `bazzi` | وَلَا أَوۡلَٰدُهُمُۥ |
| `qalun,ruways,rawh` | وَلَا أَوْلَٰدُهُمْ |
| `warsh` | وَلَآ أَوْلَٰدُهُمُۥٓ |
| `susi` | وَلَا أَوۡلَٰدُهُمۡ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَوْلَٰدُهُمْ |
| `ibn-wardan,ibn-jammaz` | وَلَا أَوْلَٰدُهُمۥُ |

**9:92** — word ids 25514, 25515, 25516 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | قُلۡتَ لَآ أَجِدُ |
| `bazzi,susi` | قُلۡتَ لَا أَجِدُ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | قُلْتَ لَا أَجِدُ |
| `warsh` | قُلْتَ لَآ أَجِدُ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | قُلْتَ لَآ أَجِدُ |

**9:99** — word ids 25658, 25659 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَلَآ إِنَّهَا |
| `bazzi,qalun,susi` | أَلَا إِنَّهَا |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّهَا |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَلَا إِنَّهَا |

**9:110** — word ids 25877, 25878 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | إِلَّآ أَن |
| `bazzi,qalun,susi` | إِلَّا أَن |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | إِلاِْ أَن |
| `ibn-wardan,ibn-jammaz` | إِلا أَن |
| `ruways,rawh` | إِلَا أَن |

**9:129** — word ids 26273, 26274, 26275 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah` | ٱللَّهُ لَآ إِلَٰهَ |
| `bazzi` | ٱللَّهُ لَا إِلَٰهَ |
| `qalun` | ࡰ۬للَّهُ لَا إِلَٰهَ |
| `warsh` | ࡰ۬للَّهُ لَآ إِلَٰهَ |
| `duri` | اَ۬للَّهُ لَآ إِلَٰهَ |
| `susi` | ࡱ۬للَّهُ لَا إِلَٰهَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | ٱلله لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | ٱللَّهُ لَا إِلَٰهَ |

**10:16** — word ids 26577, 26578 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs` | وَلَآ أَدۡرَىٰكُم |
| `shubah` | وَلَآ أَدۡرٜىٰكُم |
| `bazzi` | وَلَأَ اْدۡرَىٰكُمُۥ |
| `qalun` | وَلَا أَدْرَيٰكُم |
| `warsh` | وَلَآ أَدْرٜيٰكُم |
| `duri` | وَلَآ أَدۡر۪ىٰكُم |
| `susi` | وَلَا أَدۡرٜىٰكُم |
| `hisham` | وَلَآ أَدْرَىكُم |
| `khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أَدْر۪ىكُم |
| `ibn-wardan,ibn-jammaz` | وَلَا أَدْرَىكُمۥُ |
| `ruways,rawh` | وَلَا أَدْرَىكُم |

**10:20** — word ids 26649, 26650 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أُنزِلَ |
| `bazzi,susi` | لَوۡلَا أُنزِلَ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَوْلَا أُنزِلَ |
| `warsh` | لَوْلَآ أُنزِلَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أُنزِلَ |

**10:26** — word ids 26813, 26814 · joined in `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,qalun,warsh,susi,hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq` | قَتَرࣱ وَلَا |
| `duri` | قَتَرٞ وَلَا |
| `khalaf` | قَتَرࣱ وَّلَا |

**10:55** — word ids 27264, 27265 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَلَآ إِنَّ |
| `bazzi,qalun,susi` | أَلَا إِنَّ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَلَا إِنَّ |

**10:55** — word ids 27271, 27272 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَلَآ إِنَّ |
| `bazzi,qalun,susi` | أَلَا إِنَّ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَلَا إِنَّ |

**10:61** — word ids 27384, 27385 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أَكۡبَرَ |
| `bazzi,susi` | وَلَا أَكۡبَرَ |
| `qalun,ibn-wardan,ibn-jammaz` | وَلَا أَكْبَرَ |
| `warsh` | وَلَآ أَكْبَرَ |
| `hisham,abu-al-harith` | وَلَآ أَكْبَرَ |
| `khalaf,khallad,ishaq` | وَلَآ أَكْبَرُ |
| `ruways,rawh` | وَلَا أَكْبَرُ |

**10:62** — word ids 27390, 27391 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | أَلَآ إِنَّ |
| `bazzi,qalun,susi` | أَلَا إِنَّ |
| `warsh` | ࡰلَآ إِنَّ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَلَا إِنَّ |

**10:66** — word ids 27429, 27430 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَلَآ إِنَّ |
| `bazzi,qalun,susi` | أَلَا إِنَّ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | أَلَآ إِنَّ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَلَا إِنَّ |

**10:90** — word ids 27815, 27816, 27817 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,warsh,duri` | أَنَّهُۥ لَآ إِلَٰهَ |
| `bazzi,qalun,susi` | أَنَّهُۥ لَا إِلَٰهَ |
| `hisham` | أَنَّهُۥ لَآ إِلَٰهَ |
| `khalaf,khallad,abu-al-harith,ishaq` | إِنَّهُۥ لَآ إِلَٰهَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | أَنَّهُۥ لَا إِلَٰهَ |

**10:105** — word ids 28038, 28039 · joined in `khalaf` · **the riwāyāt differ** (a real difference)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,qalun,warsh,duri,susi` | لِلدِّينِ |
| `hisham,khallad,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq` | لِلدِّينِ |
| `khalaf,abu-al-harith` | لِلد يِّنِ |

**11:78** — word ids 29371, 29372 · joined in `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi` | كَانُواْ يَعۡمَلُونَ |
| `qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq` | كَانُواْ يَعْمَلُونَ |

**12:24** — word ids 30361, 30362 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أَن |
| `bazzi,susi` | لَوۡلَا أَن |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَوْلَا أَن |
| `warsh` | لَوْلَآ أَن |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أَن |

**12:94** — word ids 31535, 31536 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أَن |
| `bazzi,susi` | لَوۡلَا أَن |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَوْلَا أَن |
| `warsh` | لَوْلَآ أَن |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أَن |

**13:7** — word ids 31952, 31953 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أُنزِلَ |
| `bazzi,susi` | لَوۡلَا أُنزِلَ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَوْلَا أُنزِلَ |
| `warsh` | لَوْلَآ أُنزِلَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أُنزِلَ |

**13:27** — word ids 32331, 32332 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَوۡلَآ أُنزِلَ |
| `bazzi,susi` | لَوۡلَا أُنزِلَ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَوْلَا أُنزِلَ |
| `warsh` | لَوْلَآ أُنزِلَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَوْلَآ أُنزِلَ |

**13:36** — word ids 32548, 32549 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | وَلَآ أُشۡرِكَ |
| `bazzi,susi` | وَلَا أُشۡرِكَ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | وَلَا أُشْرِكَ |
| `warsh` | وَلَآ أُشْرِكَ |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | وَلَآ أُشْرِكَ |

**13:37** — word ids 32562, 32563 · joined in `abu-al-harith`, `hisham`, `ibn-jammaz`, `ibn-wardan`, `ishaq`, `khalaf`, `khallad`, `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi` | بَعۡدَ مَا |
| `qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq` | بَعْدَ مَا |

**15:7** — word ids 33539, 33540 · joined in `hisham` · **the riwāyāt differ** (a real difference)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi` | لَّوۡمَا |
| `qalun,warsh` | لَّوْمَا |
| `hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq` | لَّوْ مَا |

**19:7** — word ids 39176, 39177 · joined in `ibn-jammaz`, `ibn-wardan` · **the riwāyāt differ** (a real difference)

| riwāyāt | as printed |
|---|---|
| `hafs` | يَٰزَكَرِيَّآ إِنَّا |
| `shubah` | يَٰزَكَرِيَّآءُ إِنَّا |
| `bazzi,qalun,warsh,susi` | يَٰزَكَرِيَّآءُ ࡹِنَّا |
| `duri` | يَٰزَكَرِيَّآءُ اِ۪نَّا |
| `hisham` | يَٰزَكَرِيَّاءُ إِنَّا |
| `khalaf` | يَّٰزَكَرِيَّآ إِنَّا |
| `khallad,abu-al-harith,ishaq` | يَٰزَكَرِيَّآ إِنَّا |
| `ibn-wardan,ibn-jammaz` | يَٰزَكَرِيَّا اءُِنَّا |
| `ruways` | يَٰزَكَرِيَّااءُ ٱنَّا |
| `rawh` | يَٰزَكَرِيَّااءُ إِنَّا |

**27:20** — word ids 48685, 48686 · joined in `bazzi`, `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi` | مَا لِيَ |
| `qalun,warsh` | مَا لِے |
| `duri,susi,ruways,rawh` | مَا لِي |
| `hisham,abu-al-harith` | مَا لِىَ |
| `khalaf,khallad,ibn-wardan,ibn-jammaz,ishaq` | مَا لِى |

**30:1** — word ids 52005, 52006 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq` | الٓمٓ غُلِبَتِ |
| `qalun,warsh` | أَلَٓمِّٓ غُلِبَتِ |
| `ruways,rawh` | الٓمٓۚ غُلِبَتِ |

**36:22** — word ids 56851, 56852 · joined in `bazzi`, `duri` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,abu-al-harith,ibn-wardan,ibn-jammaz` | وَمَا لِيَ |
| `khalaf,khallad,ruways,rawh,ishaq` | وَمَا لِي |

**37:17** — word ids 57493, 57494 · joined in `hisham` · **the riwāyāt differ** (a real difference)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,warsh,duri,susi` | أَوَءَابَآؤُنَا |
| `qalun` | أَوْءَابَآؤُنَا |
| `hisham` | أَوْ ءَابَآؤُنَا |
| `khalaf,khallad,abu-al-harith,ruways,rawh,ishaq` | أَوَءَابَآؤُنَا |
| `ibn-wardan,ibn-jammaz` | أَوْءَابَآؤُنَا |

**39:59** — word ids 59937, 59938 · joined in `abu-al-harith`, `khalaf` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi` | قَدۡ جَآءَتۡكَ |
| `qalun,warsh` | قَدْ جَآءَتْكَ |
| `duri,susi` | قَد جَّآءَتۡكَ |
| `hisham,abu-al-harith` | قَد جَّآءَتْكَ |
| `khalaf,khallad` | قَد جّٜ۪آءَتْكَ |
| `ibn-wardan,ibn-jammaz,ruways,rawh` | قَدْ جَآءَتْكَ |
| `ishaq` | قَد جَّٜآءَتْكَ |

**43:68** — word ids 63704, 63705 · joined in `hisham` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,duri,susi` | لَا خَوۡفٌ |
| `qalun,warsh,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq` | لَا خَوْفٌ |
| `hisham` | لا خَوْفٌ |
| `ruways,rawh` | لَا خَوْفَ |

**56:48** — word ids 69062, 69063 · joined in `hisham` · **the riwāyāt differ** (a real difference)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,warsh,duri,susi` | أَوَءَابَآؤُنَا |
| `qalun` | أَوْءَابَآؤُنَا |
| `hisham` | أَوْ ءَابَآؤُنَا |
| `khalaf,khallad,abu-al-harith,ruways,rawh,ishaq` | أَوَءَابَآؤُنَا |
| `ibn-wardan,ibn-jammaz` | أَوْءَابَآؤُنَا |

**65:2** — word ids 72007, 72008 · joined in `rawh`, `ruways` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,susi` | مَخۡرَجࣰا وَيَرۡزُقۡهُ |
| `bazzi` | مَخۡرَجࣰا وَيَرۡزُقۡهُۥ |
| `qalun,warsh` | مَخْرَجاࣰ وَيَرْزُقْهُ |
| `duri` | مَخۡرَجٗا وَيَرۡزُقۡهُ |
| `hisham,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq` | مَخْرَجࣰا وَيَرْزُقْهُ |
| `khalaf` | مَخْرَجࣰا وَّيَرْزُقْهُ |
| `ruways,rawh` | مَخْرَجࣰاۚ وَيَرْزُقْهُ |

**71:23** — word ids 73746, 73747 · joined in `ibn-jammaz`, `ibn-wardan` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,bazzi,susi,hisham,khallad,abu-al-harith,ruways,rawh,ishaq` | وَلَا سُوَاعࣰا |
| `qalun,warsh` | وَلَا سُوَاعاࣰ |
| `duri` | وَلَا سُوَاعٗا |
| `khalaf` | وَّلَا سُوَاعࣰا |
| `ibn-wardan,ibn-jammaz` | وَلا سُوَاعࣰاَ |

**75:1** — word ids 74547, 74548 · joined in `bazzi` · **all riwāyāt agree** (a dropped space in the source)

| riwāyāt | as printed |
|---|---|
| `hafs,shubah,duri` | لَآ أُقۡسِمُ |
| `bazzi` | لَأُ اْقۡسِمُ |
| `qalun,ibn-wardan,ibn-jammaz,ruways,rawh` | لَا أُقْسِمُ |
| `warsh` | لَآ أُقْسِمُ |
| `susi` | لَا أُقۡسِم |
| `hisham,khalaf,khallad,abu-al-harith,ishaq` | لَآ أُقْسِمُ |

Machine-readable: [`resegmentation.csv`](resegmentation.csv).

### Absence — words not every riwāyah has

Each is well attested: Ibn Kathīr's `مِن` at 9:101; Nāfiʿ reciting `فإن الله الغني` at 57:24 where the others read `فإن الله هو الغني`; and `أَوۡ` at 40:26, where Ḥafṣ and Shuʿbah read *aw* and the other five read *wa* — a different word, so the number of `أَوۡ` is absent from them and their `وَأَنْ` takes the number of `أَن`.

| number | sūrah:āyah | rasm | present in | absent from | as printed |
|---|---|---|---|---|---|
| 492 | 2:31 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, rawh, ishaq | ibn-wardan, ibn-jammaz, ruways | **إِن** hafs,shubah,bazzi,qalun,duri,susi,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ان** warsh |
| 2542 | 2:142 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 4024 | 2:213 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 4319 | 2:224 | `ٮصلحوا` | khalaf, abu-al-harith, ishaq | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khallad, ibn-wardan, ibn-jammaz, ruways, rawh | **تُصْلِحُواْ** khalaf,abu-al-harith,ishaq |
| 5958 | 2:282 | `ادا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِذَا** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹِذَا** bazzi,qalun,warsh,susi  ·  **اِ۪ذَا** duri  ·  **ٱذَا** ruways |
| 6345 | 3:13 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّ** hafs,shubah  ·  **ࡹِنَّ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّ** duri  ·  **إِنَّ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّ** ruways |
| 7041 | 3:51 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣱ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٞ** duri |
| 7866 | 3:101 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 9514 | 3:195 | `اٮى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **أَنِّي** hafs,shubah,bazzi,duri,susi  ·  **أَنِّے** qalun,warsh  ·  **أَنِّٜي** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq |
| 9515 | 3:195 | `لا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **لَآ** hafs,shubah,warsh,duri  ·  **لَا** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **لَآ** hisham,khalaf,khallad,abu-al-harith,ishaq |
| 11140 | 4:68 | `صرطا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣰا** hafs,shubah,bazzi,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطاࣰ** qalun,warsh  ·  **صِرَٰطٗا** duri |
| 12740 | 4:143 | `لا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **لَآ** hafs,shubah,warsh,duri  ·  **لَا** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **لَآ** hisham,khalaf,khallad,abu-al-harith,ishaq |
| 12741 | 4:143 | `الى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq |
| 12744 | 4:143 | `الى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **إِلَىٰ** hafs,shubah,bazzi,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  **إِلَيٰ** hisham,khalaf,khallad,abu-al-harith,ishaq |
| 13324 | 4:175 | `صرطا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣰا** hafs,shubah,bazzi,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطاࣰ** qalun,warsh  ·  **صِرَٰطٗا** duri |
| 13873 | 5:16 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 14067 | 5:25 | `اٮى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **إِنِّي** hafs,shubah,bazzi,duri,susi  ·  **إِنِّے** qalun,warsh  ·  **إِنِّٜي** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq |
| 14068 | 5:25 | `لا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **لَآ** hafs,shubah,warsh,duri  ·  **لَا** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **لَآ** hisham,khalaf,khallad,abu-al-harith,ishaq |
| 15705 | 5:101 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِن** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹن** bazzi,qalun,warsh,susi  ·  **ا۪ن** duri  ·  **ٱن** ruways |
| 16805 | 6:39 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 17577 | 6:83 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّ** hafs,shubah  ·  **ࡹِنَّ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّ** duri  ·  **إِنَّ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّ** ruways |
| 17624 | 6:87 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 18376 | 6:126 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطُ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq |
| 18986 | 6:153 | `صرطى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطِي** hafs,shubah,bazzi,duri,susi,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطِے** qalun,warsh  ·  **صِرَٰطِيَ** hisham |
| 19152 | 6:161 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 19383 | 7:16 | `صرطك` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطَكَ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq |
| 19949 | 7:46 | `كلا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ruways, rawh, ishaq | khalaf | **كُلَّۢا** hafs,shubah,bazzi,duri,susi  ·  **كُلّاَۢ** qalun,warsh  ·  **كُلَآ** hisham,khallad,abu-al-harith,ishaq  ·  **كُلا** ibn-wardan,ibn-jammaz  ·  **كُلاࣱّ** ruways,rawh |
| 20613 | 7:86 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 20821 | 7:97 | `امں` | ibn-wardan, ibn-jammaz | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | **أَمِنَ** ibn-wardan,ibn-jammaz |
| 22312 | 7:188 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنۡ** hafs,shubah  ·  **ࡹِنۡ** bazzi,susi  ·  **ࡹِنْ** qalun  ·  **ࡹِنَ** warsh  ·  **اِ۪نۡ** duri  ·  **إِنْ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنْ** ruways |
| 24172 | 9:23 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنِ** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹنِ** bazzi,qalun,warsh,susi  ·  **ا۪نِ** duri  ·  **ٱنِ** ruways |
| 25687 | 9:101 | `مں` | bazzi | hafs, shubah, warsh, qalun, duri, susi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ruways, rawh, ishaq | **مِن** bazzi |
| 26804 | 10:25 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 27446 | 10:66 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِن** hafs,shubah,hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ࡹن** bazzi,susi  ·  **ࡹنْ** qalun,warsh  ·  **ا۪ن** duri  ·  **ٱن** ruways |
| 28039 | 10:105 | `ٮں` | khalaf, abu-al-harith | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khallad, ibn-wardan, ibn-jammaz, ruways, rawh, ishaq | **يِّنِ** khalaf,abu-al-harith |
| 29052 | 11:56 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 29531 | 11:87 | `اٮك` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّكَ** hafs,shubah  ·  **ࡹِنَّكَ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّكَ** duri  ·  **إِنَّكَ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّكَ** ruways |
| 31637 | 12:100 | `اٮه` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّهُۥ** hafs,shubah  ·  **ࡹِنَّهُۥ** bazzi,qalun,warsh  ·  **اِ۪نَّهُۥ** duri  ·  **ࡹِنَّه** susi  ·  **إِنَّهُۥ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّهُۥ** ruways |
| 32385 | 13:30 | `رٮى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **رَبِّي** hafs,shubah,bazzi,duri,susi  ·  **رَبِّے** qalun,warsh  ·  **رَبِّٜي** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq |
| 32386 | 13:30 | `لا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **لَآ** hafs,shubah,warsh,duri  ·  **لَا** bazzi,qalun,susi,ibn-wardan,ibn-jammaz  ·  **لَآ** hisham,khalaf,khallad,abu-al-harith,ishaq |
| 32679 | 14:1 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطِ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq |
| 33540 | 15:7 | `ما` | hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ruways, rawh, ishaq | hafs, shubah, warsh, qalun, duri, susi, bazzi | **مَا** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |
| 33795 | 15:41 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطٌ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq |
| 35210 | 16:76 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 35899 | 16:121 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 39482 | 19:36 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣱ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٞ** duri |
| 39560 | 19:43 | `صرطا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣰا** hafs,shubah,bazzi,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطاࣰ** qalun,warsh  ·  **صِرَٰطٗا** duri |
| 40887 | 20:87 | `ى` | ibn-wardan, ibn-jammaz | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | **ى** ibn-wardan,ibn-jammaz |
| 41163 | 20:114 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **أَن** hafs,shubah,bazzi,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ishaq  ·  **أَنْ** qalun,warsh |
| 43005 | 22:24 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطِ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq |
| 43484 | 22:54 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 44296 | 23:45 | `ر` | ibn-wardan, ibn-jammaz | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | **ر** ibn-wardan,ibn-jammaz |
| 44525 | 23:73 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 45011 | 24:6 | `الا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِلَّآ** hafs,shubah  ·  **ࡹِلَّا** bazzi,qalun,susi  ·  **ࡹِلَّآ** warsh  ·  **اِ۪لَّآ** duri  ·  **إِلاِْ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱلا** ruways  ·  **إِلا** rawh |
| 45791 | 24:45 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّ** hafs,shubah  ·  **ࡹِنَّ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّ** duri  ·  **إِنَّ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّ** ruways |
| 45806 | 24:46 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 46506 | 25:20 | `لٮعص` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **لِبَعۡضࣲ** hafs,shubah,bazzi,susi  ·  **لِبَعْضࣲ** qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **لِبَعۡضٖ** duri |
| 48788 | 27:29 | `اٮى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنِّيٓ** hafs,shubah  ·  **ࡹِنِّي** bazzi,susi  ·  **ࡹِنِّيَ** qalun,warsh  ·  **اِ۪نِّيٓ** duri  ·  **إِنِّٜيٓ** hisham,khalaf,khallad,abu-al-harith,ishaq  ·  **ٱنِّٜي** ruways  ·  **إِنِّٜي** rawh |
| 53098 | 31:20 | `ٮعمه` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ishaq | ruways, rawh | **نِعَمَهُۥ** hafs,qalun,warsh,duri,susi,ibn-wardan,ibn-jammaz  ·  **نِعۡمَةࣰ** shubah,bazzi  ·  **نِعْمَةࣰ** hisham,khalaf,khallad,abu-al-harith,ishaq |
| 55128 | 34:6 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطِ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq |
| 55928 | 35:1 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّ** hafs,shubah  ·  **ࡹِنَّ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّ** duri  ·  **إِنَّ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّ** ruways |
| 56203 | 35:15 | `الى` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِلَى** hafs,shubah  ·  **ࡹِلَى** bazzi,qalun,warsh,susi  ·  **اِ۪لَى** duri  ·  **إِلَي** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱلَي** ruways |
| 56353 | 35:28 | `اں` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّ** hafs,shubah  ·  **ࡹِنَّ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّ** duri  ·  **إِنَّ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّ** ruways |
| 56613 | 35:43 | `الا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِلَّا** hafs,shubah  ·  **ࡹِلَّا** bazzi,qalun,warsh,susi  ·  **اِ۪لَّا** duri  ·  **إِلَّا** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱلَّا** ruways |
| 56692 | 36:4 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 57211 | 36:61 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣱ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٞ** duri |
| 57494 | 37:17 | `اٮاوٮا` | hisham | hafs, shubah, warsh, qalun, duri, susi, bazzi, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ruways, rawh, ishaq | **ءَابَآؤُنَا** hisham |
| 57531 | 37:23 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطِ** hafs,shubah,bazzi,qalun,warsh,duri,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq |
| 60529 | 40:26 | `او` | hafs, shubah, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | warsh, qalun, duri, susi, bazzi, hisham, ibn-wardan, ibn-jammaz | **أَوۡ** hafs,shubah  ·  **أَوْ** khalaf,khallad,abu-al-harith,ruways,rawh,ishaq |
| 62665 | 42:27 | `اٮه` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّهُۥ** hafs,shubah  ·  **ࡹِنَّهُۥ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّهُۥ** duri  ·  **إِنَّهُۥ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّهُۥ** ruways |
| 62969 | 42:49 | `ٮسا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **يَشَآءُ** hafs,shubah,bazzi,duri,susi  ·  **يَّشَآءُ** qalun,warsh  ·  **يَشَآءُ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **يَّشَآءُ** khalaf |
| 63005 | 42:51 | `اٮه` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **إِنَّهُۥ** hafs,shubah  ·  **ࡹِنَّهُۥ** bazzi,qalun,warsh,susi  ·  **اِ۪نَّهُۥ** duri  ·  **إِنَّهُۥ** hisham,khalaf,khallad,abu-al-harith,rawh,ishaq  ·  **ٱنَّهُۥ** ruways |
| 63033 | 42:52 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 63464 | 43:43 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 63640 | 43:61 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣱ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٞ** duri |
| 63673 | 43:64 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣱ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٞ** duri |
| 65914 | 48:2 | `صرطا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣰا** hafs,shubah,bazzi,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطاࣰ** qalun,warsh  ·  **صِرَٰطٗا** duri |
| 66233 | 48:20 | `صرطا` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣰا** hafs,shubah,bazzi,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطاࣰ** qalun,warsh  ·  **صِرَٰطٗا** duri |
| 69063 | 56:50 | `اٮاوٮا` | hisham | hafs, shubah, warsh, qalun, duri, susi, bazzi, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, ruways, rawh, ishaq | **ءَابَآؤُنَا** hisham |
| 69728 | 57:24 | `هو` | hafs, shubah, duri, susi, bazzi, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | warsh, qalun, hisham, ibn-wardan, ibn-jammaz | **هُوَ** hafs,shubah,bazzi,duri,khalaf,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **هُّوَ** susi |
| 72717 | 67:22 | `صرط` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ibn-wardan, ibn-jammaz, rawh, ishaq | ruways | **صِرَٰطࣲ** hafs,shubah,bazzi,qalun,warsh,susi,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,rawh,ishaq  ·  **صِرَٰطٖ** duri |
| 73959 | 72:16 | `لو` | hafs, shubah, warsh, qalun, duri, susi, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | ibn-wardan, ibn-jammaz | **وَأَلَّوِ** hafs,shubah,bazzi  ·  **لَّوِ** qalun,warsh,duri,susi  ·  **وَأَلَّوِ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَّأَلَّوِ** khalaf |

### Written joined — two words some muṣḥafs print as one

Nothing is added and nothing is dropped: the nūn assimilates into the letter after it and is not written, so the same two words are printed as one. The numbering counts the finest division, so both words keep a number and the joined word *covers* both — recorded in each muṣḥaf's `numbering.written_joined`, never as a missing word. Declared in `sources/alignment/written-joined.json`.

| number | sūrah:āyah | rasm | written joined by | as printed |
|---|---|---|---|---|
| 73958 | 72:16 | `واں` | hafs, shubah, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | **وَأَلَّوِ** hafs,shubah,bazzi  ·  **وَأَن** qalun,warsh,duri,susi  ·  **وَأَلَّوِ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَّأَلَّوِ** khalaf  ·  **وَأَنلَّوِ** ibn-wardan,ibn-jammaz |
| 73959 | 72:16 | `لو` | hafs, shubah, bazzi, hisham, khalaf, khallad, abu-al-harith, ruways, rawh, ishaq | **وَأَلَّوِ** hafs,shubah,bazzi  ·  **لَّوِ** qalun,warsh,duri,susi  ·  **وَأَلَّوِ** hisham,khallad,abu-al-harith,ruways,rawh,ishaq  ·  **وَّأَلَّوِ** khalaf |
| 74234 | 73:20 | `اں` | duri, susi | **أَن** hafs,shubah,bazzi,qalun,warsh,hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq  ·  **أَلَّن** duri,susi |
| 74235 | 73:20 | `لں` | duri, susi | **لَّن** hafs,shubah,bazzi,qalun,warsh  ·  **أَلَّن** duri,susi  ·  **لَّن** hisham,khalaf,khallad,abu-al-harith,ibn-wardan,ibn-jammaz,ruways,rawh,ishaq |

## Fawāṣil: where the āyāt end

The āyah boundaries are a layer *over* the word index, not a property of it, and **the count belongs to the printed edition, not to the riwāyah**. An edition follows one of the six classical counting systems, and at the points where the system's own authorities disagree it follows one of them: al-Dānī records Mulk 67:9 «قد جاءنا نذير» as counted by Shayba and not by Abū Jaʿfar inside the First Madani, and KFGQPC's own Dūrī printings all state they follow المدني الأول and still total 6,218 (1429 AH), 6,217 (1436) and 6,214 (1443).

Each edition's system is **derived** by comparing its own āyah ends to every system's boundaries (from [qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map), vendored under `sources/counting/`), then the points of khilāf inside the system are named with the authority the edition follows. Whatever is left is `unexplained` and is an open finding. Machine-readable: [`counting.json`](../counting.json).

That derived system is what the edition **prints**. It is not the count the **qāriʾ** is associated with — Abū ʿAmr is Baṣrī, and both of his printed muṣḥafs measure onto First Madani — so both are published, as `system` and `system_associated_with_qari`, with `differs_from_association` where they part.

| muṣḥaf | system printed |  | qāriʾ associated with | āyāt | basmalah counted | khilāf inside the system | unexplained |
|---|---|---|---|---|---|---|---|
| hafs | `kufi` | الكوفي | `kufi` | 6,236 | yes | — | — |
| shubah | `kufi` | الكوفي | `kufi` | 6,236 | yes | — | — |
| warsh | `madani-last` | المدني الأخير | `madani-last` | 6,214 | no | — | — |
| qalun | `madani-last` | المدني الأخير | `madani-last` | 6,214 | no | — | — |
| duri | `madani-first` | المدني الأول | `basri` **≠** | 6,217 | no | 3:92 counted (shayba); 3:97 not counted (shayba); 37:167 counted (shayba); 67:9 not counted (abu-jafar); 80:24 counted (shayba); 81:26 counted (shayba) | — |
| susi | `madani-first` | المدني الأول | `basri` **≠** | 6,218 | no | 3:92 counted (shayba); 3:97 not counted (shayba); 37:167 counted (shayba); 67:9 counted (shayba); 80:24 counted (shayba); 81:26 counted (shayba) | — |
| bazzi | `makki` | المكي | `makki` | 6,220 | yes | 78:40 counted () | — |
| hisham | `dimashqi` | الدمشقي | `dimashqi` | 6,226 | no | — | — |
| khalaf | `kufi` | الكوفي | `kufi` | 6,236 | yes | — | None not counted; None counted |
| khallad | `kufi` | الكوفي | `kufi` | 6,236 | yes | — | — |
| abu-al-harith | `kufi` | الكوفي | `kufi` | 6,236 | yes | — | — |
| ibn-wardan | `madani-first` | المدني الأول | `madani-first` | 6,214 | no | 3:92 not counted (abu-jafar); 3:97 counted (abu-jafar); 37:167 not counted (abu-jafar); 67:9 not counted (abu-jafar); 80:24 not counted (abu-jafar); 81:26 not counted (abu-jafar) | 20:88 not counted; None counted; 23:45 not counted; None counted |
| ibn-jammaz | `madani-first` | المدني الأول | `madani-first` | 6,214 | no | 3:92 not counted (abu-jafar); 3:97 counted (abu-jafar); 37:167 not counted (abu-jafar); 67:9 not counted (abu-jafar); 80:24 not counted (abu-jafar); 81:26 not counted (abu-jafar) | 20:88 not counted; None counted; 23:45 not counted; None counted |
| ruways | `basri` | البصري | `basri` | 6,204 | no | — | — |
| rawh | `basri` | البصري | `basri` | 6,206 | no | — | 84:7 counted; 84:10 counted |
| ishaq | `kufi` | الكوفي | `kufi` | 6,236 | yes | — | — |

| edition | `hafs` | `shubah` | `warsh` | `qalun` | `duri` | `susi` | `bazzi` | `hisham` | `khalaf` | `khallad` | `abu-al-harith` | `ibn-wardan` | `ibn-jammaz` | `ruways` | `rawh` | `ishaq` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `hafs` | — | 0 | 140 | 140 | 133 | 134 | 150 | 140 | 2 | 0 | 0 | 136 | 136 | 128 | 126 | 0 |
| `shubah` | 0 | — | 140 | 140 | 133 | 134 | 150 | 140 | 2 | 0 | 0 | 136 | 136 | 128 | 126 | 0 |
| `warsh` | 140 | 140 | — | 0 | 57 | 56 | 48 | 108 | 142 | 140 | 140 | 64 | 64 | 100 | 98 | 140 |
| `qalun` | 140 | 140 | 0 | — | 57 | 56 | 48 | 108 | 142 | 140 | 140 | 64 | 64 | 100 | 98 | 140 |
| `duri` | 133 | 133 | 57 | 57 | — | 1 | 39 | 107 | 135 | 133 | 133 | 9 | 9 | 97 | 95 | 133 |
| `susi` | 134 | 134 | 56 | 56 | 1 | — | 38 | 108 | 136 | 134 | 134 | 10 | 10 | 98 | 96 | 134 |
| `bazzi` | 150 | 150 | 48 | 48 | 39 | 38 | — | 118 | 152 | 150 | 150 | 48 | 48 | 106 | 104 | 150 |
| `hisham` | 140 | 140 | 108 | 108 | 107 | 108 | 118 | — | 142 | 140 | 140 | 112 | 112 | 84 | 86 | 140 |
| `khalaf` | 2 | 2 | 142 | 142 | 135 | 136 | 152 | 142 | — | 2 | 2 | 138 | 138 | 130 | 128 | 2 |
| `khallad` | 0 | 0 | 140 | 140 | 133 | 134 | 150 | 140 | 2 | — | 0 | 136 | 136 | 128 | 126 | 0 |
| `abu-al-harith` | 0 | 0 | 140 | 140 | 133 | 134 | 150 | 140 | 2 | 0 | — | 136 | 136 | 128 | 126 | 0 |
| `ibn-wardan` | 136 | 136 | 64 | 64 | 9 | 10 | 48 | 112 | 138 | 136 | 136 | — | 0 | 102 | 100 | 136 |
| `ibn-jammaz` | 136 | 136 | 64 | 64 | 9 | 10 | 48 | 112 | 138 | 136 | 136 | 0 | — | 102 | 100 | 136 |
| `ruways` | 128 | 128 | 100 | 100 | 97 | 98 | 106 | 84 | 130 | 128 | 128 | 102 | 102 | — | 2 | 128 |
| `rawh` | 126 | 126 | 98 | 98 | 95 | 96 | 104 | 86 | 128 | 126 | 126 | 100 | 100 | 2 | — | 126 |
| `ishaq` | 0 | 0 | 140 | 140 | 133 | 134 | 150 | 140 | 2 | 0 | 0 | 136 | 136 | 128 | 126 | — |

Āyah ends where two editions differ. Dūrī and Sūsī, both First Madani, part company at exactly one place — 67:9 — which is the whole of the 6,217/6,218 difference between them: Dūrī follows Abū Jaʿfar there and Sūsī follows Shayba. Bazzī counts 78:40, which no source yet gives to the Makkī count; it is reported as an open finding, not corrected.

## Source integrity

Six riwāyāt ship two releases. Comparing them is the sharpest available check on each, since the publisher is the same.

**Where the two releases disagree, the later one is the text.** KFGQPC revises these documents deliberately: the 2026 Ḥafṣ separates `مَا لِيَ` where Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`. That is a change of convention, not a defect, and the newer convention is the one published here. The earlier release is never merged into the text — it is only compared against it, below. The rule cannot discriminate for Dūrī, whose two packages are both from 2022; its three dropped spaces are recorded as boundary events instead.

| riwāyah | āyāt compared | byte-identical | notation only | marks/vowels only | rasm differs |
|---|---|---|---|---|---|
| hafs | 6,236 | 2,715 | 700 | 2,819 | 2 |
| shubah | 6,236 | 2,715 | 697 | 2,822 | 2 |
| warsh | 6,214 | 156 | 414 | 5,635 | 9 |
| qalun | 6,214 | 717 | 2,333 | 3,143 | 21 |
| duri | 6,217 | 6,214 | 0 | 0 | 3 |
| susi | 6,217 | 508 | 1,916 | 3,768 | 25 |

`notation only` is dominated by the 2026 files adopting the Arabic Extended-B alif letters (`U+0870`–`U+0882`), which fold an alef and its vowel into one codepoint where the 2022 files used an alef plus combining marks. The `folded` form decomposes them again, so none of it reaches the word index.

### Checks

All checks pass.

## Per sūrah

| sūrah | name | words | identical | diacritic | dotting | ā | rasm | boundary/absent | per 1000 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Al-Fātiḥah | 29 | 9 | 17 | 1 | 0 | 2 | 0 | 69.0 |
| 2 | Al-Baqarah | 6,118 | 2701 | 3246 | 56 | 24 | 67 | 24 | 14.9 |
| 3 | Āl-‘Imrān | 3,481 | 1514 | 1846 | 47 | 9 | 40 | 25 | 18.7 |
| 4 | An-Nisā’ | 3,747 | 1549 | 2092 | 36 | 8 | 46 | 16 | 16.5 |
| 5 | Al-Mā’idah | 2,804 | 1170 | 1557 | 22 | 19 | 28 | 8 | 12.8 |
| 6 | Al-An‘ām | 3,050 | 1390 | 1551 | 47 | 5 | 30 | 27 | 18.7 |
| 7 | Al-A‘rāf | 3,321 | 1535 | 1673 | 47 | 7 | 41 | 18 | 17.8 |
| 8 | Al-Anfāl | 1,234 | 515 | 695 | 13 | 3 | 8 | 0 | 6.5 |
| 9 | At-Taubah | 2,499 | 1035 | 1413 | 27 | 0 | 7 | 17 | 9.6 |
| 10 | Yūnus | 1,834 | 852 | 917 | 24 | 4 | 15 | 22 | 20.2 |
| 11 | Hūd | 1,917 | 898 | 973 | 23 | 3 | 16 | 4 | 10.4 |
| 12 | Yūsuf | 1,777 | 841 | 879 | 35 | 4 | 13 | 5 | 10.1 |
| 13 | Ar-Ra‘d | 854 | 375 | 454 | 7 | 2 | 6 | 10 | 18.7 |
| 14 | Ibrāhīm | 830 | 353 | 461 | 7 | 1 | 7 | 1 | 9.6 |
| 15 | Al-Ḥijr | 655 | 345 | 294 | 4 | 0 | 10 | 2 | 18.3 |
| 16 | An-Naḥl | 1,844 | 814 | 987 | 23 | 1 | 17 | 2 | 10.3 |
| 17 | Al-Isrā’ | 1,556 | 671 | 834 | 20 | 6 | 25 | 0 | 16.1 |
| 18 | Al-Kahf | 1,579 | 657 | 878 | 19 | 5 | 20 | 0 | 12.7 |
| 19 | Maryam | 961 | 410 | 522 | 8 | 2 | 16 | 3 | 19.8 |
| 20 | Ṭā-Hā | 1,336 | 603 | 675 | 21 | 7 | 28 | 2 | 22.5 |
| 21 | Al-Anbiyā’ | 1,169 | 567 | 573 | 14 | 3 | 12 | 0 | 10.3 |
| 22 | Al-Ḥajj | 1,274 | 552 | 691 | 15 | 3 | 11 | 2 | 10.2 |
| 23 | Al-Mu’minūn | 1,051 | 497 | 527 | 9 | 2 | 14 | 2 | 15.2 |
| 24 | An-Nūr | 1,316 | 537 | 748 | 16 | 0 | 12 | 3 | 11.4 |
| 25 | Al-Furqān | 893 | 369 | 500 | 12 | 4 | 7 | 1 | 9.0 |
| 26 | Ash-Shu‘arā’ | 1,318 | 632 | 663 | 5 | 5 | 13 | 0 | 9.9 |
| 27 | An-Naml | 1,151 | 552 | 560 | 15 | 2 | 19 | 3 | 19.1 |
| 28 | Al-Qaṣaṣ | 1,430 | 695 | 689 | 12 | 10 | 24 | 0 | 16.8 |
| 29 | Al-‘Ankabūt | 976 | 435 | 520 | 12 | 3 | 6 | 0 | 6.1 |
| 30 | Ar-Rūm | 817 | 365 | 432 | 11 | 0 | 7 | 2 | 11.0 |
| 31 | Luqmān | 546 | 246 | 293 | 3 | 1 | 2 | 1 | 5.5 |
| 32 | As-Sajdah | 372 | 177 | 182 | 6 | 1 | 6 | 0 | 16.1 |
| 33 | Al-Aḥzāb | 1,287 | 520 | 731 | 18 | 0 | 18 | 0 | 14.0 |
| 34 | Saba’ | 883 | 406 | 454 | 15 | 2 | 5 | 1 | 6.8 |
| 35 | Fāṭir | 775 | 358 | 399 | 4 | 2 | 8 | 4 | 15.5 |
| 36 | Yā-Sīn | 725 | 308 | 397 | 7 | 0 | 9 | 4 | 17.9 |
| 37 | Aṣ-Ṣāffāt | 862 | 408 | 429 | 7 | 1 | 15 | 2 | 19.7 |
| 38 | Ṣād | 733 | 360 | 359 | 5 | 1 | 8 | 0 | 10.9 |
| 39 | Az-Zumar | 1,172 | 535 | 609 | 10 | 1 | 15 | 2 | 14.5 |
| 40 | Ghāfir | 1,219 | 552 | 648 | 7 | 7 | 4 | 1 | 4.1 |
| 41 | Fuṣṣilat | 794 | 361 | 417 | 7 | 1 | 8 | 0 | 10.1 |
| 42 | Ash-Shūra | 860 | 372 | 469 | 8 | 0 | 7 | 4 | 12.8 |
| 43 | Az-Zukhruf | 830 | 375 | 427 | 11 | 2 | 10 | 5 | 18.1 |
| 44 | Ad-Dukhān | 346 | 168 | 168 | 3 | 1 | 6 | 0 | 17.3 |
| 45 | Al-Jāthiyah | 488 | 214 | 265 | 7 | 1 | 1 | 0 | 2.0 |
| 46 | Al-Aḥqāf | 643 | 296 | 331 | 10 | 3 | 3 | 0 | 4.7 |
| 47 | Muḥammad | 539 | 210 | 319 | 9 | 0 | 1 | 0 | 1.9 |
| 48 | Al-Fatḥ | 560 | 223 | 320 | 12 | 0 | 3 | 2 | 8.9 |
| 49 | Al-Ḥujurāt | 347 | 146 | 191 | 7 | 1 | 2 | 0 | 5.8 |
| 50 | Qāf | 373 | 206 | 158 | 3 | 2 | 4 | 0 | 10.7 |
| 51 | Adh-Dhāriyāt | 360 | 158 | 192 | 5 | 0 | 5 | 0 | 13.9 |
| 52 | Aṭ-Ṭūr | 312 | 148 | 155 | 8 | 0 | 1 | 0 | 3.2 |
| 53 | An-Najm | 360 | 149 | 190 | 5 | 1 | 15 | 0 | 41.7 |
| 54 | Al-Qamar | 342 | 165 | 170 | 4 | 1 | 2 | 0 | 5.8 |
| 55 | Ar-Raḥmān | 351 | 89 | 213 | 1 | 13 | 35 | 0 | 99.7 |
| 56 | Al-Wāqi‘ah | 380 | 171 | 201 | 2 | 1 | 4 | 1 | 13.2 |
| 57 | Al-Ḥadīd | 574 | 228 | 332 | 9 | 0 | 4 | 1 | 8.7 |
| 58 | Al-Mujādilah | 472 | 206 | 254 | 10 | 0 | 2 | 0 | 4.2 |
| 59 | Al-Ḥashr | 445 | 176 | 257 | 7 | 1 | 4 | 0 | 9.0 |
| 60 | Al-Mumtaḥanah | 348 | 136 | 206 | 2 | 0 | 4 | 0 | 11.5 |
| 61 | Aṣ-Ṣaff | 221 | 89 | 123 | 2 | 2 | 5 | 0 | 22.6 |
| 62 | Al-Jumu‘ah | 175 | 73 | 100 | 1 | 0 | 1 | 0 | 5.7 |
| 63 | Al-Munāfiqūn | 180 | 81 | 98 | 1 | 0 | 0 | 0 | 0.0 |
| 64 | At-Taghābun | 241 | 99 | 138 | 4 | 0 | 0 | 0 | 0.0 |
| 65 | Aṭ-Ṭalāq | 287 | 130 | 148 | 3 | 0 | 4 | 2 | 20.9 |
| 66 | At-Taḥrīm | 249 | 108 | 131 | 3 | 3 | 4 | 0 | 16.1 |
| 67 | Al-Mulk | 333 | 142 | 182 | 2 | 0 | 6 | 1 | 21.0 |
| 68 | Al-Qalam | 300 | 156 | 141 | 0 | 2 | 1 | 0 | 3.3 |
| 69 | Al-Ḥāqqah | 258 | 127 | 125 | 4 | 0 | 2 | 0 | 7.8 |
| 70 | Al-Ma‘ārij | 217 | 92 | 116 | 5 | 0 | 4 | 0 | 18.4 |
| 71 | Nūḥ | 226 | 83 | 138 | 1 | 0 | 2 | 2 | 17.7 |
| 72 | Al-Jinn | 286 | 109 | 171 | 1 | 0 | 4 | 1 | 17.5 |
| 73 | Al-Muzzammil | 199 | 80 | 116 | 0 | 0 | 1 | 2 | 15.1 |
| 74 | Al-Muddaththir | 255 | 125 | 124 | 3 | 0 | 3 | 0 | 11.8 |
| 75 | Al-Qiyāmah | 164 | 69 | 84 | 3 | 0 | 6 | 2 | 48.8 |
| 76 | Al-Insān | 243 | 92 | 145 | 5 | 0 | 1 | 0 | 4.1 |
| 77 | Al-Mursalāt | 181 | 73 | 105 | 3 | 0 | 0 | 0 | 0.0 |
| 78 | An-Naba’ | 173 | 60 | 110 | 1 | 2 | 0 | 0 | 0.0 |
| 79 | An-Nāzi‘āt | 179 | 73 | 89 | 14 | 0 | 3 | 0 | 16.8 |
| 80 | ‘Abasa | 133 | 58 | 75 | 0 | 0 | 0 | 0 | 0.0 |
| 81 | At-Takwīr | 104 | 48 | 53 | 0 | 1 | 2 | 0 | 19.2 |
| 82 | Al-Infiṭār | 80 | 38 | 38 | 4 | 0 | 0 | 0 | 0.0 |
| 83 | Al-Muṭaffifīn | 169 | 74 | 90 | 4 | 0 | 1 | 0 | 5.9 |
| 84 | Al-Inshiqāq | 107 | 58 | 47 | 0 | 0 | 2 | 0 | 18.7 |
| 85 | Al-Burūj | 109 | 45 | 61 | 2 | 0 | 1 | 0 | 9.2 |
| 86 | Aṭ-Ṭāriq | 61 | 27 | 31 | 1 | 0 | 2 | 0 | 32.8 |
| 87 | Al-A‘lā | 72 | 28 | 43 | 1 | 0 | 0 | 0 | 0.0 |
| 88 | Al-Ghāshiyah | 92 | 41 | 48 | 2 | 0 | 1 | 0 | 10.9 |
| 89 | Al-Fajr | 137 | 57 | 71 | 7 | 0 | 2 | 0 | 14.6 |
| 90 | Al-Balad | 82 | 41 | 38 | 2 | 0 | 1 | 0 | 12.2 |
| 91 | Ash-Shams | 54 | 18 | 20 | 13 | 1 | 2 | 0 | 37.0 |
| 92 | Al-Lail | 71 | 29 | 40 | 1 | 0 | 1 | 0 | 14.1 |
| 93 | Aḍ-Ḍuḥā | 40 | 20 | 20 | 0 | 0 | 0 | 0 | 0.0 |
| 94 | Ash-Sharḥ | 27 | 18 | 9 | 0 | 0 | 0 | 0 | 0.0 |
| 95 | At-Tīn | 34 | 20 | 14 | 0 | 0 | 0 | 0 | 0.0 |
| 96 | Al-‘Alaq | 72 | 33 | 39 | 0 | 0 | 0 | 0 | 0.0 |
| 97 | Al-Qadr | 30 | 13 | 16 | 1 | 0 | 0 | 0 | 0.0 |
| 98 | Al-Bayyinah | 94 | 42 | 52 | 0 | 0 | 0 | 0 | 0.0 |
| 99 | Az-Zalzalah | 36 | 17 | 19 | 0 | 0 | 0 | 0 | 0.0 |
| 100 | Al-‘Ādiyāt | 40 | 18 | 22 | 0 | 0 | 0 | 0 | 0.0 |
| 101 | Al-Qāri‘ah | 36 | 16 | 17 | 3 | 0 | 0 | 0 | 0.0 |
| 102 | At-Takāthur | 28 | 17 | 10 | 1 | 0 | 0 | 0 | 0.0 |
| 103 | Al-‘Aṣr | 14 | 9 | 5 | 0 | 0 | 0 | 0 | 0.0 |
| 104 | Al-Humazah | 33 | 11 | 21 | 1 | 0 | 0 | 0 | 0.0 |
| 105 | Al-Fīl | 23 | 11 | 12 | 0 | 0 | 0 | 0 | 0.0 |
| 106 | Quraish | 17 | 5 | 10 | 0 | 0 | 2 | 0 | 117.6 |
| 107 | Al-Mā‘ūn | 25 | 9 | 16 | 0 | 0 | 0 | 0 | 0.0 |
| 108 | Al-Kauthar | 10 | 4 | 6 | 0 | 0 | 0 | 0 | 0.0 |
| 109 | Al-Kāfirūn | 26 | 7 | 19 | 0 | 0 | 0 | 0 | 0.0 |
| 110 | An-Naṣr | 19 | 10 | 9 | 0 | 0 | 0 | 0 | 0.0 |
| 111 | Al-Masad | 23 | 9 | 14 | 0 | 0 | 0 | 0 | 0.0 |
| 112 | Al-Ikhlāṣ | 15 | 10 | 5 | 0 | 0 | 0 | 0 | 0.0 |
| 113 | Al-Falaq | 23 | 15 | 8 | 0 | 0 | 0 | 0 | 0.0 |
| 114 | An-Nās | 20 | 9 | 11 | 0 | 0 | 0 | 0 | 0.0 |
