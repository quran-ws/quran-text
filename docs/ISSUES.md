# Issues

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

### 1. ~~Sūsī v3.0 splits Al-Mulk 67:9 into two āyāt~~ — not a defect

**This entry was wrong and is kept as a correction.** It claimed Al-Mulk has 30
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

**The qirāʾah does not determine the count.** KFGQPC's own printings of the
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
which also found the qirāʾah→system mapping wrong in the other direction: the
Dūrī muṣḥaf measures onto First Madinan in 113 of 114 sūrahs, not Baṣrī.)*

**What changed here as a result.** The build no longer asserts a total per
tradition. `COUNTING_TOTALS = {"kufi": 6236, "madani": 6214, "basri": 6217}` is
gone: it measured an assumption rather than the data, and produced a false
positive on every run. `out/fawasil.json` is now derived from the packages
themselves and keyed by muṣḥaf, so two riwāyāt are grouped only where their
fawāṣil are actually identical. The `counting` field survives as a display
label with that stated in the code.

**One thing this repository cannot yet reconcile.** The forum write-up reports
that the digital Dūrī muṣḥaf carries **6,218** āyāt, matching the 1429 printing.
Parsing `UthmanicDouri V20.docx` here yields **6,217**. That is a one-āyah gap
between a stated figure and this parse, and it is not resolved — it may be a
different digital package, or a parse defect in this repository. It is recorded
rather than reconciled by adjusting either side.

### 2. Qālūn v3.0 carries the Al-Baqarah heading inside the previous paragraph

`UthmanicQaloun-v-3.0.docx` has 113 sūrah headings in their own paragraphs
instead of 114. The text `سُورَةُ البَقَرَةِ` sits at the **end of the Al-Fātiḥah
paragraph**, after āyah 7's number. This is a fact about the document's
paragraph structure, not about its text — every word of scripture is present
and in order.

Two consequences for anything that parses the file, both handled here:

- heading-driven sūrah segmentation shifts every sūrah after Al-Fātiḥah by one.
  Segmenting on āyah-numbering resets instead removes the dependency entirely,
  and is the more robust rule regardless.
- the stranded heading was landing as two words at the head of Al-Baqarah 2:1.
  Text after the final āyah mark of a paragraph is now stripped when it matches
  the heading pattern. That anchor is deliberately narrow: sūrah 24 opens with
  `سُورَةٌ أَنزَلۡنَٰهَا`, which *is* scripture, and a looser rule would eat it.

### 3. Word boundaries differ between packages

Six word pairs are printed joined in one package and separated in another. The
pipeline re-segments them so the index keeps one column per word, records
`boundary: {"<riwaya>": "joined_in_source"}`, and **does not judge which
spacing is correct**. Left alone, each join would falsely report the following
word absent from that riwāyah.

Three are cases where a riwāyah's two releases disagree with each other:

| āyah | `UthmanicDouri V20.docx` | Dūrī's own 2022 CSV |
|---|---|---|
| 4:90 | `مَارُدُّوٓاْ` | `مَا رُدُّوٓاْ` |
| 10:26 | `قَتَرٞوَلَا` | `قَتَرٞ وَلَا` |
| 11:77 | `كَانُواْيَعۡمَلُونَ` | `كَانُواْ يَعۡمَلُونَ` |

Three are cases where packages differ from each other:

- Bazzī `لَأُاْقۡسِمُ` (75:1) — Ibn Kathīr's reading, written as one word;
- Bazzī and Dūrī `مَالِيَ` / `وَمَالِيَ` (27:20, 36:22) — the traditional muṣḥaf
  spelling. The 2026 Ḥafṣ document moved the other way and separated
  `مَا لِيَ`, where Ḥafṣ's own 2022 CSV joins it: a change of convention
  between releases.

`out/boundaries.csv` carries a `riwayat_agree` column saying whether the riwāyāt
read the run identically once re-segmented. That is a statement about agreement,
not about correctness.

### 4. Characters carrying no textual weight

Stripped because they do not affect the letters or the reading: kashida
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

### The dagger alif was made a letter, and it is not one

This reverses the decision recorded below, which was wrong, and the reasoning
that produced it is worth keeping because it was wrong in an instructive way.

A superscript alef is by definition an alef the scribe did **not** write on the
line. It is the reader's cue for ḥadhf al-alif — the device by which one
skeleton is written so as to carry two readings. `ملك` is what every codex has
at 1:4, written that way so that it can be read both `مَٰلِكِ` and `مَلِكِ`; that
is the point of it, and al-Dānī says so plainly: *كتبوا في جميع المصاحف ملك بغير
ألف*. Promoting the dagger to a letter therefore reported the codices as
disagreeing in exactly the places they had been written to agree.

The scale: **170 of the 232** reported rasm disagreements were this and nothing
else — `مالك`/`ملك`, `يضاعف`/`يضعف`, `كلمات`/`كلمت`, `مساكين`/`مسكين`,
`دفاع`/`دفع`, `الرياح`/`الريح`, `طائرا`/`طيرا`. Every one of them is a
textbook ḥadhf. What survives once the dagger is dropped is 62 words, and that
list is recognisably the received one: `ووصى`/`وأوصى` 2:132, `وسارعوا`/`سارعوا`
3:133, `يرتد`/`يرتدد` 5:54, `كلمت`/`كلمة` 7:137, `والذين`/`الذين` 9:107,
`قال`/`قل` 21:4 and 23:112, `لله`/`الله` 23:87 and 23:89, `عبادِ`/`عبادي` 43:68,
`إذا`/`إذ` 74:33. Converging on the received list from a completely different
direction is the strongest check available here.

A second defect fell out of the same code. The guard that stops `اٰ` from
emitting two alefs tested only for a preceding `ا`, so a dagger riding on a
final `ى` was emitted as an *extra letter*: `عَلَىٰٓ` came out `علٮا` and 34:17
`يُجَٰزَىٰ` came out `ٮحارٮا`, six letters for a four-letter word. **3,071 word
positions** carried an inflated skeleton. 34:17 was consequently filed as a rasm
disagreement when `نُجَٰزِي` and `يُجَٰزَىٰ` are one skeleton pointed two ways.

The ā is not lost. It is read, so `pointed` keeps it, and 1:4 is now a
`dotting_variant`: one rasm, two readings — which is what it is.

### What the old reasoning got right, and what to do with it

The objection below — that the Warsh/Qālūn set prints `هَارُوتَ` where the Kūfī
set prints `هَٰرُوتَ` — is real, and dropping the dagger surfaces 198 words of it.
But it does not argue for folding, because the disagreement runs in **both**
directions: the same Warsh/Qālūn set prints `مُبَٰرَك`, `ٱلۡغَمَٰمِ` and
`يُعَلِّمَٰنِ` where the Kūfī set prints `مُبَارَك`, `ٱلۡغَمَامِ` and `يُعَلِّمَانِ`. Two
hands making opposite choices about ḥadhf al-alif is a difference of typesetting
on its face; whether any of it is also a difference of codex is a question these
sources cannot answer.

So it is neither folded away nor counted as a codex disagreement. `rasm_plene`
spells every ā out, and a word whose skeletons agree once it is applied gets its
own status, `madd_alif` — 198 words, kept, counted and listed separately. The
alternative of merging them would have hidden them; the alternative of calling
them `rasm_variant` would have claimed more than the evidence supports.

Result: 232 → 62 `rasm_variant` + 198 `madd_alif`; 170 false positives removed,
3,071 skeletons corrected, none newly flagged.

### Dropping the dagger alif hid the most famous variant of all

**Superseded by the entry above.** Kept because the argument is a good example
of a headline count moving in a plausible direction for the wrong reason.


The rasm was originally defined as "what is written on the line", which meant
the superscript alif was discarded. That is defensible as history and wrong for
this corpus: KFGQPC's Warsh/Qālūn set writes ā on the line where the Kūfī set
writes a dagger, so the two spellings of one word looked different — 202 false
positives — while `مَٰلِكِ` and `مَلِكِ` at 1:4 collapsed to the same skeleton and
were filed as a mere difference of vowelling.

Folding the dagger to a written alef removes those 202 and surfaces 206 real
variants that were invisible: `مالك`/`ملك`, `يخدعون`/`يخادعون`, `دفع`/`دفاع`,
`الريح`/`الرياح`, `مسكين`/`مساكين`. Only 99 words are in both lists — the old
definition and the correct one barely overlap, so this was never a tuning knob.

Two rules were tried and rejected on the way. Collapsing every run of alefs
afterwards welds Bazzī's `لَأُاْقۡسِمُ` into one alef and breaks the re-segmentation
of 75:1. Treating a dagger on an existing `ا`/`ى` seat as a vowel looks right —
it drops the count from 262 to 242 — but it hides `عَلَىٰٓ`/`عَلَيَّ` and
`يُوصِي`/`يُوصَىٰ`, and tightening it to check the raw seat character explodes to
1,195, because the packages do not agree on which glyph the seat is: Dūrī writes
`مُوسۭيٰ` with `U+064A` where the others write `مُوسَىٰ` with `U+0649`.

### A hard-coded skeleton in the basmalah detector

`_is_bare_basmalah` compared against a literal `"بسماللهالرحمنالرحيم"`. When the
rasm became undotted the needle stopped matching, and 113 sūrahs silently
absorbed their opening basmalah into āyah 1 — 448 extra words, with every
structural check still passing, because the index was internally consistent
about the wrong thing. The needle is now derived from a reference spelling
through the same normalisation, so it cannot drift again.

### Word-boundary status outranked the comparison

`classify` returned `word_boundary` before comparing the words at all, on the
reasoning that a join *causes* an apparent absence. It does — but it also meant
five of the six boundary events were reported as disagreements when all seven
riwāyāt read them identically and one source had merely lost a space. Content
is decided first now, and `boundaries.csv` carries a `riwayat_agree` column so
the two cases are told apart rather than conflated.

### "No local rule can separate these" — there was one

34 words of the `أَرَءَيۡتَ` family were shipped as a known residual, reported as
`rasm_variant` when the codices agree. Warsh writes `ࡰرَٰٓيْتَ`, spelling the
tashīl'd hamza as a dagger alif; Ḥafṣ writes `أَرَءَيۡتَ` with a hamza. Dropping
hamza and folding the dagger to an alef made Ḥafṣ lose a letter and Warsh gain
one.

Three rules were tried and rejected, and the conclusion drawn was that no rule
looking at the glyphs and their neighbours could work, because `إِسۡرَٰٓءِيلَ`
needs the opposite treatment with the same local context. That conclusion was
wrong: the context is not the same, it just extends one character further than
was being looked at.

`ٰٓ` is a madd **over** something. What it is over is what decides:

| after the `ٰٓ` | example | the dagger is |
|---|---|---|
| a hamza | `إِسۡرَٰٓءِيلَ`, `هَٰٓؤُلَآءِ`, `مَلَٰٓئِكَةِ` | a written ā |
| a doubled letter | `تَتَّبِعَٰٓنِّ`, `فَذَٰٓنِّكَ` | a written ā (madd lāzim) |
| nothing — end of word | `عَلَىٰٓ` | a written ā |
| a plain undoubled letter | `ࡰرَٰٓيْتَ` | **the suppressed hamza** |

The first attempt at this rule handled only the first and third rows and
introduced two new false positives at 10:89 and 28:32 — caught by diffing the
flagged-ID set against the previous build rather than by trusting the headline
count, which had moved in the right direction while being wrong. Qālūn writes
the same madd with `U+06EC` instead of a maddah, which was a second miss.

Result: 266 → 232 rasm disagreements, 34 resolved, none newly flagged.

The generalisable part is not about hamza. It is that "no rule can distinguish
these" is a claim about the rules tried, and it was stated in the docs as
though it were a claim about the data.

### Round-trip by word count

The first round-trip check compared word counts per riwāyah and reported three
"failures" that were the re-segmentation working correctly. Comparing the
concatenated **rasm** instead is indifferent to word boundaries while still
catching a genuinely lost or duplicated letter. It passes clean for all seven.
