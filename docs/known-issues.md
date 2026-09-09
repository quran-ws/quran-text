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

Four of the seven packages count 67:9. Sūsī is counted here as its **2026**
release has it; its 2022 release does not count the position, and that change is
taken up at the end of this entry. Al-Dānī records this exact position —
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
`data/counting.json` is keyed by system with the editions under each.

**The 6,218 belongs to Sūsī, not to Dūrī.** This entry previously recorded a
one-āyah gap it could not close: a forum write-up gives the digital Dūrī muṣḥaf
**6,218** āyāt, and parsing `UthmanicDouri V20.docx` here yields **6,217**. The
gap was read as either a different package or a parse defect. It is neither —
the figure was attached to the wrong riwāyah.

Dūrī has no v3.0 release, so both of its packages date from 2022, and they
agree: `DouriData_v2-0.csv` has **6,217 rows** and the document parses to
**6,217**, with **no difference in any of the 114 sūrahs**. Nothing in the Dūrī
release carries 6,218.

Sūsī does, and only since 2026:

| Sūsī release | sūrah 67 | total |
|---|---|---|
| `SousiData_v2-0.csv` (2022) | 30 | 6,217 |
| `UthmanicSousi-v-3.0.docx` (2026) | **31** | **6,218** |

Those two differ in exactly one sūrah, and it is sūrah 67 — the 67:9 split this
entry is about. **KFGQPC moved the Sūsī division at 67:9 between its 2022 and
its 2026 release**, which is the same kind of change between printings that §3
records for `مَا لِيَ`, and it is what puts a 6,218 in the packages for a
narrator of Abū ʿAmr. Per the standing rule it is a difference, not a defect.

What is settled is where 6,218 is attested in `sources/`: in Sūsī's 2026 release
and nowhere else. What the forum write-up was itself describing is not settled,
and no figure has been adjusted on either side to make them agree.

### 1b. ~~Bazzī counts 78:40 ﴿قريبًا﴾, and no source yet says the Makkī count does~~ — cited

**This is now closed.** The entry recorded that the Bazzī edition counts an āyah
end after ﴿قريبًا﴾ at 78:40 and totals 6,220 where the classical Makkī total is
6,219, that upstream gave the point to Baṣrī alone, and that no source was known
to place it inside the Makkī count. One does.

**al-Dānī, *al-Bayān*, sūrah 78 (Naba)** puts it in Baṣrī and nowhere else:

> وهي إحدى وأربعون آية في البصري، وأربعون في عدد الباقين.
> اختلافها آية: ﴿عذابًا قريبًا﴾ [٤٠] **عدها البصري ولم يعدها الباقون**.

On its own that leaves the edition unexplained — «الباقون» includes the Makkī.

**al-Qāḍī, *al-Farāʾid al-Ḥisān*, at the same word, records khilāf *within* the
Makkī count:**

> قَرِيبًا الْبَصْرِى **وَخُلْفٌ مَكِّهِمْ**
> … عده البصري **والمكي يُخْلَف عنه** وتركه الباقون

So the edition is not anomalous and is not borrowing from Baṣrī. It is a Makkī
muṣḥaf resolving a documented Makkī khilāf in favour of counting — the same
shape as §1, where Warsh, Qālūn and Bazzī count a position al-Dānī marks
مختلف فيها. Its own numbers say the same thing: measured against the six
systems, Bazzī is **1** āyah end from Makkī and **106** from Baṣrī.

| system | āyah ends that differ from Bazzī |
|---|---|
| **Makkī** | **1** |
| Madanī First | 39 |
| Madanī Last | 48 |
| **Baṣrī** | **106** |

**What changed here.** The point moved from `open-findings.json` to
`khilaf.json`, which is what that file says should happen once a source is
cited, and it now appears under `counting.khilaf` in `data/mushaf/bazzi.json`
rather than `counting.unexplained`. **No edition has an unexplained āyah end
any more.**

*al-Farāʾid al-Ḥisān attests the khilāf without naming who holds each side, so
the entry carries an empty `authorities` map and the emitted point says
`"authorities_named": false`. `follows` and `against` stay present and empty:
the shape does not vary, and the flag says why they are empty rather than
letting an absent attribution read as an absent disagreement.*

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

`data/reports/resegmentation.csv` carries a `riwayahs_agree` column saying whether the riwāyāt
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

### 5b. `U+06E4` is not a maddah — it is the sajdah line

`ARABIC SMALL HIGH MADDA` is the codepoint the releases use for خط السجدة, the
horizontal line drawn over the words that make the sajdah due. Nothing in the
codepoint says so; the corpus does. In Ḥafṣ it occurs **26 times and nowhere
else**, is the last character of its word in all 26, and the 26 words are the
sajdah phrases of all 15 sajdah places — ﴾يَسۡجُدُونَ﴿, ﴾خَرُّواْ سُجَّدࣰا﴿,
﴾وَلِلَّهِ يَسۡجُدُ﴿ — and nothing else. Shuʿbah, Bazzī, Dūrī and Sūsī carry the same
26; Warsh and Qālūn, whose typesetting draws no such line, carry none. A maddah
would not distribute that way, and would not sit after a final nūn that already
carries its fatḥah.

It was published inside the word until it was classified, where it read as a
maddah those 26 words do not have. It is now peeled off like a waqf mark and
published as the mark kind `sajdah_line` (`docs/format.md`, *Marks*). Where a
word carries both it and ۩ — 7:206 and 84:21 — the release writes the line
inside the sign, and the marks are emitted in that order so that re-attaching
them reproduces the printed token.

---

### 6. Printed lines are not encoded in any release, and were reconstructed wrong

The `.docx` releases mark their **page** turns explicitly — 603
`<w:br w:type="page"/>` elements, giving 604 pages — so a word's page is read
from the file. Its **line** is not there. What the document has is line breaks,
paragraph boundaries and headings, from which the printed line is inferred.

For a long time that inference sat at about **98%**, and this entry recorded the
2% as something the documents could not express. It was a defect here:

| edition | before | after |
|---|---|---|
| **Ḥafṣ** | 6,131 / 6,236 | **6,236 / 6,236** |
| **Shuʿbah** | 6,131 / 6,236 | **6,236 / 6,236** |
| Warsh | 6,106 / 6,214 | 6,210 / 6,214 |
| Qālūn | 6,102 / 6,214 | 6,210 / 6,214 |
| Dūrī | 6,108 / 6,217 | 6,212 / 6,217 |
| Sūsī | 6,089 / 6,217 | 6,193 / 6,217 |

**What was wrong.** A sūrah heading was charged **two** lines: once by the rule
that every paragraph begins a new line, and once again by a `HEADING_LINES = 1`
added on top. The double count stayed invisible because these releases put the
page break *inside* the heading paragraph, so the break's "first paragraph on
this page" flag suppressed the *next* paragraph's increment — two errors
cancelling. That cancellation only covers a page's **first** heading. Every
heading after the first on the same page pushed the rest of that page down one
line, which is exactly why only multi-sūrah pages ever disagreed: 85 pages with
one sūrah start were all correct, and all 12 pages with two or three were not.

**How it was found.** By reading a printed page against the CSV rather than
reasoning about the document. Page 587 sets سُورَةُ الانفِطَارِ, its basmalah,
nine lines of text, سُورَةُ المُطَفِّفِينَ, its basmalah, and two more lines —
**15 rows, with the heading and the basmalah each taking a ruled line of their
own**. The CSV agrees exactly (82:1 on line 3, 83:1 on line 14, and no line
anywhere in the file above 15); the reconstruction said 15 and 16, and a 16th
line on a fifteen-line page is impossible.

An earlier attempt had rejected the right answer for the wrong reason: treating
a heading at the top of a page as sitting in an ornamental band "fixed the 105
and broke 1,001". It broke them because page-top headings were the one case
already coming out right.

**`first` now means "nothing has been printed on this page yet"** and is cleared
when a glyph is placed rather than when a paragraph opens, and `HEADING_LINES`
is `0`.

**What is left is not reconstruction error.** Ḥafṣ and Shuʿbah are exact. The
rest divide into two kinds:

- **five to seven āyāt per edition** that begin on the last ruled line of a page
  and run onto the next. The reconstruction records where the āyah *begins*; the
  CSV records where it *continues*. The packages' own read.me notes they mark
  two-page āyāt with a `–` in the `page` column. Bookkeeping, not typesetting.
- **seventeen more in Sūsī, all inside sūrah 67.** Its 2026 document counts 67:9
  and its 2022 CSV does not (§1), so from that point the two number the sūrah's
  āyāt differently and the comparison is misaligned rather than wrong.

**The editions check each other.** Mapped through the shared numbering, `pg` is
identical for all 77,432 words in all seven editions, and `ln` splits into two
layout families, identical within each:

| family | editions | same line as each other |
|---|---|---|
| A | Ḥafṣ, Shuʿbah, Dūrī, Sūsī, Bazzī | 100.00% |
| B | Warsh, Qālūn | 100.00% |

Across the two families it is 96.66% — Warsh and Qālūn distribute words over the
lines of a page differently, on the same pages.

`ln` is still declared under `layers.derived` and still scored against the
release that states it, and `line_disagreements` still lists every āyah that
differs. **Bazzī has no v2 release to score against, but it is not therefore
unknown**: its lines are identical, word for word, to Ḥafṣ's, which are now
exact. Its file still says `"validated": false`, which understates what the
other six establish about it.

Per the standing rule, nothing here is a defect in the packages. The releases
were not made to answer this question; the defect was in reading them.

### 7. ۞ marks two different divisions, and the releases carry no marginal apparatus at all

| release | ۞ | division marked | markable | not printed |
|---|---|---|---|---|
| Ḥafṣ, Shuʿbah, Bazzī | 199 | 240 rubu_al_hizbs | 239 | 40 |
| Dūrī, Sūsī | 433 | 480 thumns | 479 | 46 |
| Warsh | 435 | 480 thumns | 479 | 44 |
| Qālūn | 437 | 480 thumns | 479 | 42 |

This entry used to say only that "the conventional division is 240 rubu_al_hizbs, and no
release prints that many", and left it unreconciled. Every part of that needed
work.

**There are two conventions, not four.** Ḥafṣ, Shuʿbah and Bazzī mark the 240
**rubu_al_hizbs** — and at the same 199 words, identically. The other four mark the 480
**thumns** (60 ḥizb × 8), at exactly double the density: median gap 164–166
words against 334.

**One division is never markable.** The Qurʾān opens at 1:1, the start of the
first rubu_al_hizb, ḥizb and juz, and no release prints a ۞ there. So the markable
positions are 239 and 479. Ḥafṣ's first mark stands at 2:26, one full rubu_al_hizb in;
its last at 100:9, one rubu_al_hizb before the end.

**The rest are not absent from the muṣḥaf — they are marked in the margin.**
The printed muṣḥaf carries a medallion in the outer margin at **every one of the
240 rubu_al_hizbs**, reading «الحِزْبُ N» at a ḥizb start and «رُبْعُ / نِصْفُ /
ثَلَاثَةُ أَرْبَاعِ الحِزْبِ N» at the quarters between. Where a sūrah heading
occupies the place the inline symbol would take, the medallion alone states the
division. At **7:1** the print shows «الحِزْبُ ١٦» in the margin and no ۞.

**The releases encode none of it.** `الحزب`, `حزب`, `الجزء`, `جزء` and `ربع`
appear **nowhere** in any part of the `.docx` — not in `document.xml`, not in
the headers or footers, and there are no text boxes. The releases carry the
inline symbol and nothing else. So a division can be plainly marked in the
printed muṣḥaf and wholly absent from these files, and `marks` is **not a
complete record of the muṣḥaf's divisions**: it is a complete record of its
inline ۞.

**The full division can nonetheless be recovered, and closes exactly.** Each juz
holds 8 rubu_al_hizbs, so the grid is countable rather than estimated. For Ḥafṣ:

| source | positions |
|---|---|
| printed ۞ | 199 |
| juz starts from the v2 CSV (less the two its own marks contradict — §11) | 28 |
| sūrah openings in a juz that is short, each medallion-confirmed | 19 |
| medallions read from the printed muṣḥaf | 13 |
| **total** | **240**, and every juz holds exactly 8 |

**The assembled 240 are recorded** in `sources/divisions/hafs-rubu-al-hizb.json`, each with the source that fixes it — a printed ۞, a juz start, a count that leaves one candidate, or a margin medallion read from the print. It is evidence, not a published layer: `data/` still carries no `rubu_al_hizb_starts`.

The absences concentrate where sūrahs are short: juz 28 is missing 4 of 8, juz
29 5, and juz 30 prints **one** mark for its eight divisions.

**Checked against the print at both ends of the claim:**

| page | the print | this repository |
|---|---|---|
| 413 | a ۞ at 31:22 | the same ۞ at 31:22 |
| 151 | سورة الأعراف opens; «الحِزْبُ ١٦» in the margin, no ۞ | no ۞ — and juz 8 is one short, at 7:1 |

A medallion marks *every* rubu_al_hizb, including the 199 that also carry a ۞, so a
medallion on a page does not by itself mean the division sits at that page's
sūrah opening. Two readings had to be corrected on exactly that point: p554's
«رُبْعُ الحِزْبِ ٥٦» is the ۞ at 63:4, not 63:1, and p575's «رُبْعُ الحِزْبِ
٥٨» is the ۞ at 73:20, not 74:1.

**Nothing is added and nothing is lost.** Every ۞ in every document is emitted —
199, 199, 199, 433, 433, 435, 437 — matching each `.docx` exactly, so no mark is
dropped in parsing. Per the standing rule, a publisher that shows a division in
the margin rather than beside a heading has made a typographic choice, not an
error — but a consumer who reads `marks` as "every division in this muṣḥaf" will
be wrong, and that is what this entry exists to say.

*A naming note: `mark_types` calls the ۞ kind `hizb`. The symbol is the
**rubu_al_hizb** sign, and the ḥizb proper is the marginal label these files do
not carry. The name is imprecise and predates this entry.*

### 8. Waqf-mark conventions are not comparable between muṣḥafs

Warsh and Qālūn print one general waqf sign 9,948 times. Ḥafṣ, Dūrī and Sūsī
print seven distinct ones — ۖ ۗ ۘ ۚ ۛ ۜ and ۩ — totalling far fewer. A consumer
diffing the `waqf` layers of Ḥafṣ and Warsh is comparing publishing conventions,
not qiraahs.

Nothing here normalises them. There is no mapping in the sources from Warsh's
general sign to the Ḥafṣ set, and any mapping this project supplied would be its
own claim about where a reciter may make waqf.

### 9. Bazzī has no v2 release, so it has no juz layer

`sources/` has `UthmanicBazzi-v-3.0.zip` and no `BazziData` package. The juz number
comes from the v2 CSVs, so Bazzī has none, and its file names the absence in
`layers.absent` rather than emitting nulls. Its **pages are unaffected** — those
come from the `.docx`, which every muṣḥaf has. The Bazzī document names no juz
anywhere: it contains no occurrence of جزء, حزب or ربع.

**How much of it is nonetheless determined.** Two independent things narrow the
gap to a single position, and both are readings of the sources rather than
inferences of this project's own:

- **26 of the 30 starts are the same word in all six editions that have juz.**
  The raw CSVs appear to disagree far more widely than that, but most of the
  difference is āyah-*numbering*, not division: mapped through the shared word
  numbering it resolves to four genuine disagreements — juz 4, 7, 11 and 26.
- **The majority is clear at three of those four.** At juz 7 and 26 the only
  dissenters are Dūrī and Sūsī, both rāwīs of Abū ʿAmr; at juz 4 Shuʿbah stands
  alone and at juz 11 Ḥafṣ does. Bazzī is Ibn Kathīr's, so on each point it sits
  with the majority.

**Juz 26 is the one that is not determined.** Neither edition family agrees and
no mark is printed there, since 46:1 is a sūrah opening:

| | juz 26 begins at |
|---|---|
| Ḥafṣ, Shuʿbah, Warsh, Qālūn | 46:1 |
| Dūrī, Sūsī | 45:32 |
| top of page 502, where 28 of 30 juz begin | 45:32 |

The layout argument and the majority of the editions point opposite ways, so it
is left open rather than decided here. See `docs/verify-in-print.md`, Q2.

**The ۞ marks do not decide this.** A ۞ marks the rubu_al_hizb, not the juz, and
a juz start landing on one is the rubu_al_hizb falling there. Of the four disputed juz
only juz 7 has a mark standing on the boundary; at juz 4 and 11 the nearest are
15 and 19 words away — neighbouring rubu_al_hizbs — and at juz 26 no edition prints one
at all, since 46:1 is a sūrah opening and §7 shows marks are never printed
there.

### 10. Imlāʾī exists for one release only

Only `hafsData_v2-0.csv` carries an `aya_text_emlaey` column. Warsh, Qālūn, Dūrī
and Sūsī all have a v2 release and none of them has the column, so having a v2
package is not the test — having something in the column is.

Bringing it down from the āyah to the word is new work, and it does not fully
close: 77,356 of Ḥafṣ's 77,432 words are mapped, 4 āyāt cannot be paired and 2
cannot be aligned to the word index. Those words get a `null` entry. An absent
spelling is recoverable; a guessed one is not.

### 11. The Ḥafṣ v2 CSV's juz column disagrees with the muṣḥaf's own printed marks

Two of the thirty juz starts in `hafsData_v2-0.csv` do not fall where the
printed Ḥafṣ muṣḥaf puts its ۞:

| juz | the CSV's `jozz` column | the printed ۞ | the other editions |
|---|---|---|---|
| **4** | 3:92 | **3:93** | Shuʿbah 3:93; Warsh, Qālūn, Dūrī, Sūsī 3:91 |
| **11** | 9:94 | **9:93** | Shuʿbah, Warsh, Qālūn 9:93; Dūrī, Sūsī 9:91 |

At both points the printed mark agrees with other editions and the CSV stands
alone. These are also two of the four juz where the seven editions disagree at
all (§9), so the conflict is not incidental — it is the reason two of those four
looked unresolved.

**How it surfaced.** Not by comparing editions, but by counting. Every juz holds
exactly 8 rubu_al_hizbs, so once the 240 rubu_al_hizb positions are assembled the total must be
240 and every juz must hold 8. Taking the CSV's juz starts gives **242**, with
juz 4 and juz 10 holding 9 apiece — because the CSV's juz start and the muṣḥaf's
own mark, 15 and 19 words apart, were being counted as two divisions rather than
one. Taking the printed mark instead closes both: **240, every juz exactly 8.**

**Nothing is corrected.** `juz_starts` is still read from the CSV, because that
is what the package states and the standing rule holds. This entry records that
at these two positions the same publisher's document and data file disagree, and
that the document is the one consistent with the division it prints. A consumer
computing rubu_al_hizbs from `juz_starts` will be one out in juz 4 and juz 11; one
reading `marks` will not.

*The two are recorded here rather than in `open-findings.json`, which holds
disagreements about **āyah** counting. This is a disagreement about division.*

---
