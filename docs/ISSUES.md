# Issues

Two kinds: defects found **in the KFGQPC sources**, and mistakes made **in
building this** that are worth recording because they were not obvious.

---

## Defects in the sources

### 1. Sūsī v3.0 splits Al-Mulk 67:9 into two āyāt

`UthmanicSousi-v-3.0.docx` numbers 31 āyāt in sūrah 67. Al-Mulk has **30** in
every counting tradition, and Sūsī's own 2022 release (`SousiData_v2-0.csv`)
has 30. The document ends an āyah after `قَالُواْ بَلَىٰ قَد جَّآءَنَا نَذِيرࣱ` and starts
a new one at `فَكَذَّبۡنَا وَقُلۡنَا…`, so every āyah from 9 to 30 is shifted by one and
the riwāyah totals 6,218 instead of 6,217.

**Impact: none on the word index.** This is purely an āyah-boundary error; the
word sequence is untouched. It is the clearest vindication of the flat model —
had words been nested under āyāt, this single defect would have misaligned
2,000+ words for one riwāyah. As it is, only the `aya` attribute of the affected
Sūsī words is off by one.

**Not silently corrected.** `build.py` reports it on every run:

```
checks: 1 finding(s)
  - [counting_total] sousi the basri tradition totals 6217 āyāt; this release has 6218
```

Correcting it means asserting which side of the split is wrong, which is an
editorial call for someone with the printed muṣḥaf in hand, not a build step.

### 2. Qālūn v3.0 is missing the heading for Al-Baqarah

`UthmanicQaloun-v-3.0.docx` has 113 sūrah headings instead of 114. The text
`سُورَةُ البَقَرَةِ` was typed at the **end of the Al-Fātiḥah paragraph**, after
āyah 7's number, rather than in its own paragraph.

Two consequences, both handled:

- heading-driven sūrah segmentation shifts every sūrah after Al-Fātiḥah by one.
  Segmenting on āyah-numbering resets instead removes the dependency entirely.
- the stranded heading was landing as two words at the head of Al-Baqarah 2:1.
  Text after the final āyah mark of a paragraph is now stripped when it matches
  the heading pattern. That anchor is deliberately narrow: sūrah 24 opens with
  `سُورَةٌ أَنزَلۡنَٰهَا`, which *is* scripture, and a looser rule would eat it.

### 3. Dūrī v3.0 drops three spaces between words

`UthmanicDouri V20.docx` prints three word pairs joined. Dūrī's own 2022 CSV
prints all three with the space, which makes these unambiguous typographic
defects rather than orthographic choices:

| āyah | document | the same riwāyah's CSV |
|---|---|---|
| 4:90 | `مَارُدُّوٓاْ` | `مَا رُدُّوٓاْ` |
| 10:26 | `قَتَرٞوَلَا` | `قَتَرٞ وَلَا` |
| 11:77 | `كَانُواْيَعۡمَلُونَ` | `كَانُواْ يَعۡمَلُونَ` |

The words are re-segmented so the index keeps one column per word, and the join
is recorded as `boundary: {"douri": "joined_in_source"}`. Left alone, each of
these would falsely report the following word absent from Dūrī.

### 4. Word joins that are *not* defects

The same mechanism catches joins that are genuine orthography, and the pipeline
deliberately does **not** try to tell them apart — it records the join and lets
a reader judge:

- Bazzī `لَأُاْقۡسِمُ` (75:1) — Ibn Kathīr's reading, written as one word;
- Bazzī and Dūrī `مَالِيَ` / `وَمَالِيَ` (27:20, 36:22) — the traditional muṣḥaf
  spelling. Here the *2026 Ḥafṣ document* moved the other way and separated
  `مَا لِيَ`, where Ḥafṣ's own 2022 CSV joins it. A deliberate change of
  convention between releases, not an error.

All 12 are listed in `out/COMPARISON.md`.

### 5. Stray characters

Present across the sources and stripped as meaningless: kashida `U+0640` (6,838
occurrences — KFGQPC's own changelogs record removing these), zero-width joiner,
and right-to-left marks. One dotless beh `U+066E` in Bazzī and one small low
seen `U+06E3` in Ḥafṣ v3.0 appear exactly once each and are probably typos, but
neither affects the rasm.

---

## Mistakes made building this

Recorded because each cost real time and each would recur.

### Word counts hid a sūrah-level shift

The first Qālūn parse produced 6,214 āyāt — the correct Madanī total — while
being wrong about which sūrah every āyah belonged to. **A correct total is not
a correct parse.** The check that caught it was structural: 113 sūrahs, not 114.
Asserting an invariant the data must satisfy found in one line what comparing
totals would never have found.

### Regexing XML

`re.findall(r'<w:t[^>]*>(.*?)</w:t>')` over `document.xml` looked fine on Ḥafṣ
and returned a paragraph of `<w:tab w:val="left" w:pos="4377"/>` tab-stop
definitions on Qālūn. Walking the element tree is barely more code and cannot
do this.

### Sequence identity vs value identity

`Column` is a mutable dataclass shared between spine positions. With the default
generated `__eq__`, a `col not in out` membership test compared *contents*,
which was both quadratic and wrong once two columns held equal tokens. Columns
are now `@dataclass(eq=False)`.

### Dead entries in the fold tables

`ۥ` and `ۦ` were listed in both the marks set and the rasm-fold map. Since marks
are dropped first, the fold entries were unreachable — the tables *looked* like
they folded ṣilah into `و`/`ي`, and did not. A unit test written against the
apparent behaviour failed, which is how it was found. The unreachable entries
are gone and the decision — superscript letters are vowels, not rasm — is now
stated where it is made.

### Round-trip by word count

The first round-trip check compared word counts per riwāyah and reported three
"failures" that were the re-segmentation working correctly. Comparing the
concatenated **rasm** instead is indifferent to word boundaries while still
catching a genuinely lost or duplicated letter. It passes clean for all seven.
