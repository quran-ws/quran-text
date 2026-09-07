# Known issues: what the sources contain

Two kinds: things **the KFGQPC packages do** that the pipeline has to handle,
and mistakes made **in building this** that are worth recording because they
were not obvious.

## A standing rule about the sources

**The KFGQPC packages are the authority. Nothing in them is called an error
here.**

Where a package differs from another package, from an earlier printing of
itself, or from what a counting tradition would lead you to expect, that is
recorded as a difference and left alone. It is not corrected, and it is not
labelled a defect. The publisher makes editorial choices — among fawāṣil that
are مختلف فيها, among orthographic conventions, between its own releases — and
does not always document them. An apparent mistake is far more often a choice
whose reasoning has not been published.

This rule was learned the hard way; entry 1 below is the correction that
prompted it, and it had been wired into the build as a check that failed on
every run.

---

## What the sources contain

### 1. ~~Sūsī v3.0 splits Mulk 67:9 into two āyāt~~ — not a defect

**This entry was wrong and is kept as a correction.** It claimed Mulk has 30
āyāt "in every counting tradition" and reported Sūsī's 31 as an error. Both
halves are false, and the second was refutable from this repository's own
output:

| | āyāt in sūrah 67 |
|---|---|
| Ḥafṣ, Shuʿbah, Dūrī | 30 |
| **Warsh, Qālūn, Sūsī, Bazzī** | **31** |

Four of the seven packages count 67:9. Al-Dānī records this exact position —
«قد جاءنا نذير» — as **مختلف فيها**: *عدها المدني الأخير والمكي ولم يعدها
الباقون، وعدها شيبة ولم يعدها أبو جعفر*. The Madanī (Warsh, Qālūn) and Makkī
(Bazzī) packages counting it is precisely what that says should happen.

**The riwāyah does not determine the count.** KFGQPC's own printings of the
Dūrī muṣḥaf settle it — all three state they follow **المدني الأول**, and all
three disagree:

| printing | āyāt |
|---|---|
| 1429 AH | 6,218 |
| 1436 AH | 6,217 |
| 1443 AH | 6,214 |

The 1429 colophon states 6,214 *«مَا عَدَا الآيَاتِ المُخْتَلَفَ فِيهَا بَيْنَ أَبِي
جَعْفَرٍ وَشَيْبَةَ»* without saying where those positions are or how many; there
are four, which is how that printing reaches 6,218. None of the three explains
the editorial choices behind its division.

*(Evidence assembled by @quranpedia in
[qiraat-ayah-map#10](https://github.com/quranpedia/qiraat-ayah-map/pull/10),
which also found the riwāyah→system mapping wrong in the other direction: the
Dūrī muṣḥaf measures onto First Madani in 113 of 114 sūrahs, not Baṣrī.)*

**What changed here as a result.** The build no longer asserts a total per
tradition. `COUNTING_TOTALS = {"kufi": 6236, "madani": 6214, "basri": 6217}` is
gone: it measured an assumption rather than the data, and produced a false
positive on every run.

**And then changed again.** The `counting` string that survived as a "display
label" was itself wrong for two of the seven: Dūrī and Sūsī were labelled
`basri`, and Baṣrī is 6,204 — no printed Abū ʿAmr muṣḥaf follows it. Comparing
each edition's āyah ends against the six systems' boundaries from
[qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map) puts both on
**First Madani** at distance zero once al-Dānī's six Abū Jaʿfar/Shayba points
are set aside, differing from each other only at 67:9. So `mushaf.counting` is
now a block that names the *derived* system and what the edition does at every
point of khilāf inside it (`docs/format.md`, *Counting*), and
`out/counting.json` is keyed by system with the editions under each.

**One thing this repository cannot yet reconcile.** The forum write-up reports
that the digital Dūrī muṣḥaf carries **6,218** āyāt, matching the 1429 printing.
Parsing `UthmanicDouri V20.docx` here yields **6,217**. That is a one-āyah gap
between a stated figure and this parse, and it is not resolved — it may be a
different digital package, or a parse defect in this repository. It is recorded
rather than reconciled by adjusting either side.

### 1b. Bazzī counts 78:40 ﴿قريبًا﴾, and no source yet says the Makkī count does

Derived against qiraat-ayah-map, the Bazzī edition matches Makkī at every
point but one: it counts an āyah end after ﴿قريبًا﴾ at 78:40 and totals 6,220
where the classical Makkī total is 6,219. Upstream gives that point to Baṣrī
alone, and its attestation notes record al-Dānī reporting it for Baṣrī, not
Makkī; nquran.com lists it for Makkī too. Two independent sources putting a
Makkī boundary there looks like a khilāf inside the Makkī transmission rather
than a printing slip, but it is uncited, so the file reports it under
`counting.unexplained`, it is listed in `data/counting/open-findings.json`, and
it has been reported to qiraat-ayah-map. It is **not** corrected on either side.

### 2. Qālūn v3.0 carries the Baqarah heading inside the previous paragraph

`UthmanicQaloun-v-3.0.docx` has 113 sūrah headings in their own paragraphs
instead of 114. The text `سُورَةُ البَقَرَةِ` sits at the **end of the Al-Fātiḥah
paragraph**, after āyah 7's number. This is a fact about the document's
paragraph structure, not about its text — every word of scripture is present
and in order.

Two consequences for anything that parses the file, both handled here:

- heading-driven sūrah segmentation shifts every sūrah after Al-Fātiḥah by one.
  Segmenting on āyah-numbering resets instead removes the dependency entirely,
  and is the more robust rule regardless.
- the stranded heading was landing as two words at the head of Baqarah 2:1.
  Text after the final āyah mark of a paragraph is now stripped when it matches
  the heading pattern. That anchor is deliberately narrow: sūrah 24 opens with
  `سُورَةٌ أَنزَلۡنَٰهَا`, which *is* scripture, and a looser rule would eat it.

### 3. Word boundaries differ between packages

Six word pairs are printed joined in one package and separated in another. The
pipeline re-segments them so the index keeps one column per word, records
`boundary: {"<riwayah>": "joined_in_source"}`, and **does not judge which
spacing is correct**. Left alone, each join would falsely report the following
word absent from that riwāyah.

Three are cases where a riwāyah's two releases disagree with each other:

| āyah | `UthmanicDouri V20.docx` | Dūrī's own 2022 CSV |
|---|---|---|
| 4:90 | `مَارُدُّوٓاْ` | `مَا رُدُّوٓاْ` |
| 10:26 | `قَتَرٞوَلَا` | `قَتَرٞ وَلَا` |
| 11:77 | `كَانُواْيَعۡمَلُونَ` | `كَانُواْ يَعۡمَلُونَ` |

Three are cases where packages differ from each other:

- Bazzī `لَأُاْقۡسِمُ` (75:1) — Ibn Kathīr's qiraah, written as one word;
- Bazzī and Dūrī `مَالِيَ` / `وَمَالِيَ` (27:20, 36:22) — the traditional muṣḥaf
  spelling. The 2026 Ḥafṣ document moved the other way and separated
  `مَا لِيَ`, where Ḥafṣ's own 2022 CSV joins it: a change of convention
  between releases.

`out/reports/resegmentation.csv` carries a `riwayahs_agree` column saying whether the riwāyāt
read the run identically once re-segmented. That is a statement about agreement,
not about correctness.

### 4. Characters carrying no textual weight

Stripped because they do not affect the letters or the qiraah: kashida
`U+0640` (6,838 occurrences — KFGQPC's own changelogs record removing these),
zero-width joiner, and right-to-left marks. One dotless beh `U+066E` in Bazzī
and one small low seen `U+06E3` in Ḥafṣ v3.0 occur exactly once each; both are
recorded and neither affects the rasm.

### 5. `U+08CC` — an editorial mark in the text

`ARABIC SMALL HIGH WORD SAH`, the proofreader's *ṣaḥḥa* ("correct as written"),
occurs **8,128 times** in the v3.0 Warsh document and essentially nowhere else.
It is not pronounced, not written by any other release, and not part of the
word. Until it was classified it was the single largest source of spurious
differences in the corpus — larger than every genuine variant combined. It is
now stripped with the structural symbols.

---

### 6. Printed lines are not encoded in any release

The `.docx` releases mark their **page** turns explicitly — 603
`<w:br w:type="page"/>` elements, giving 604 pages — so a word's page is read
from the file. Its **line** is not there. What the document has is line breaks,
paragraph boundaries and headings, from which the printed line can be inferred
but not read.

The inference reaches about **98.3%**:

| method | āyāt whose line matches the v2 CSV |
|---|---|
| line breaks alone | 5,079 / 6,236 |
| + paragraph boundaries and headings | **6,131 / 6,236** ← shipped |

The residual overshoots by one or two on pages the publisher sets specially,
Al-Fātiḥah above all, whose decorative frame the document flow does not
describe. One further rule was tried and rejected: treating a heading at the top
of a page as sitting in the page's ornamental band rather than on a ruled line.
It fixed the 105 and broke 1,001, so headings at a page top evidently do take a
line in most pages and the exception is narrower than that.

This is a **reconstruction, and the format says so**: `ln` is declared under
`layers.derived`, scored against the release that states it, and every
disagreeing āyah is listed in `line_disagreements` so a consumer can exclude
them rather than discover them. Bazzī has no v2 release, so its lines cannot be
checked at all and its file says `"validated": false` rather than implying the
same confidence as the rest.

Per the standing rule above, none of this is called a defect in the packages.
Typesetting software has no reason to record a line number; the releases were
not made to answer this question.

### 7. The ۞ symbol is printed a different number of times in each release

| release | ۞ |
|---|---|
| Ḥafṣ, Shuʿbah, Bazzī | 199 |
| Dūrī, Sūsī | 433 |
| Warsh | 435 |
| Qālūn | 437 |

The conventional division is 240 arbāʿ, and no release prints that many. The
symbol is emitted here exactly as each release prints it and **is not
reconciled**, because 240 is not a number any package in `data/` states, and
inventing the missing marks would be this project adding data its sources do not
carry.

### 8. Waqf-mark conventions are not comparable between muṣḥafs

Warsh and Qālūn print one general waqf sign 9,948 times. Ḥafṣ, Dūrī and Sūsī
print seven distinct ones — ۖ ۗ ۘ ۚ ۛ ۜ and ۩ — totalling far fewer. A consumer
diffing the `waqf` layers of Ḥafṣ and Warsh is comparing publishing conventions,
not qiraahs.

Nothing here normalises them. There is no mapping in the sources from Warsh's
general sign to the Ḥafṣ set, and any mapping this project supplied would be its
own claim about where a reciter may make waqf.

### 9. Bazzī has no v2 release, so it has no juz layer

`data/` has `UthmanicBazzi-v-3.0.zip` and no `BazziData` package. The juz number
comes from the v2 CSVs, so Bazzī has none, and its file names the absence in
`layers.absent` rather than emitting nulls. Its **pages are unaffected** — those
come from the `.docx`, which every muṣḥaf has.

### 10. Imlāʾī exists for one release only

Only `hafsData_v2-0.csv` carries an `aya_text_emlaey` column. Warsh, Qālūn, Dūrī
and Sūsī all have a v2 release and none of them has the column, so having a v2
package is not the test — having something in the column is.

Bringing it down from the āyah to the word is new work, and it does not fully
close: 77,356 of Ḥafṣ's 77,432 words are mapped, 4 āyāt cannot be paired and 2
cannot be aligned to the word index. Those words get a `null` entry. An absent
spelling is recoverable; a guessed one is not.

---
