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
positive on every run.

**And then changed again.** The `counting` string that survived as a "display
label" was itself wrong for two of the seven: Dūrī and Sūsī were labelled
`basri`, and Baṣrī is 6,204 — no printed Abū ʿAmr muṣḥaf follows it. Comparing
each edition's āyah ends against the six systems' boundaries from
[qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map) puts both on
**First Madinan** at distance zero once al-Dānī's six Abū Jaʿfar/Shayba points
are set aside, differing from each other only at 67:9. So `mushaf.counting` is
now a block that names the *derived* system and what the edition does at every
point of khilāf inside it (`docs/MUSHAF-FORMAT.md`, *Counting*), and
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

`out/reports/resegmentation.csv` carries a `riwayat_agree` column saying whether the riwāyāt
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

### 8. Pause-mark conventions are not comparable between muṣḥafs

Warsh and Qālūn print one general pause sign 9,948 times. Ḥafṣ, Dūrī and Sūsī
print seven distinct ones — ۖ ۗ ۘ ۚ ۛ ۜ and ۩ — totalling far fewer. A consumer
diffing the `waqf` layers of Ḥafṣ and Warsh is comparing publishing conventions,
not readings.

Nothing here normalises them. There is no mapping in the sources from Warsh's
general sign to the Ḥafṣ set, and any mapping this project supplied would be its
own claim about where a reciter may stop.

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

`Column` is a mutable dataclass shared between alignment positions. With the default
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

So it is not folded away. An alef on the line is part of the bare rasm whichever
hand wrote it, so all 198 are counted as `rasm_variant` — but `rasm_plene`
spells every ā out, which makes the sub-class exactly identifiable: it is the
words whose skeletons agree once it is applied. The report lists them under
their own heading so that a reader can see what the 260 is made of, and
`docs/LIMITATIONS.md` says plainly that separating codex from typesetter here
needs a manuscript.

Result: 232 → 260 `rasm_variant`, of which 62 are a letter one codex simply
lacks and 198 are the plene/defective class; 170 false positives removed, 3,071
skeletons corrected, none newly flagged.

**Revised by the entry below**, which asked the corpus a question this reasoning
never put to it.

### "These sources cannot answer it" — they could, and the answer was in the split

The entry above settled for a shrug: two hands disagree about the ā in both
directions, so how much is codex and how much is typesetter is unanswerable
here, and all 198 stay `rasm_variant`. Both halves of that are wrong. The
directions were counted — 134 one way, 64 the other — but *who* was on each side
was never counted at all, and that is the whole question.

**All 198 split the seven riwāyāt along exactly one line: `qaloun,warsh` against
the other five. One partition, 198 words, no exception. The 62 real letter
differences split them 14 ways** — Bazzī alone 7 times, Ḥafṣ+Shuʿbah alone 6,
Qālūn alone 5, Sūsī alone once, and eight more shapes besides.

That settles it. Ḥadhf and ithbāt al-alif do vary between the codices of the
amṣār — it is a whole bāb in al-Dānī's المقنع — but a khilāf of the amṣār has no
reason to put Makkah with Madinah every single time and never once apart, and
Bazzī is Makkī. What does partition perfectly by publisher is the publisher.
Note the shape of the evidence: it is not that folding is convenient or that the
number looks better, it is that the variable which explains all 198 is the file
they were typeset in, and the variable which explains the 62 is the miṣr.

So the 198 became `alif_variant` — reported, listed in full, counted apart from
the letters the codices actually disagree about. The bare `rasm` still keeps the
distinction, because within any one muṣḥaf it is that muṣḥaf's own ḥadhf and it
is carried faithfully: Ḥafṣ writes قال plene 412 times and defective 4, سبحان
defective 12 and plene once, and 175 of the 198 words show the identical split
at *every* occurrence in the corpus. Each book is self-consistent. It is only
between the two typesettings that the choice stops tracking anything textual.

The one-partition fact is now a check rather than a paragraph
(`validate.check_alif_splits`), because it is the ground the status stands on:
if a future package ever splits one of these words Makkah-from-Madinah, the
classification has lost its warrant and the report says so.

Result: 260 → 62 `rasm_variant` + 198 `alif_variant`. Nothing dropped, nothing
folded, one number replaced by two that mean different things.

### A letter added read as a letter exchanged

Grouping the 62 by what the difference *is* — one skeleton with a letter more,
against one letter swapped for another — put `ٮسٮهى`/`ٮسٮهٮه`
(تَشۡتَهِي/تَشۡتَهِيهِ, 43:71) in the wrong group. The rasm keeps the final letter
shapes because the codices did: a yāʾ ending a word is `ى`, medially it is `ٮ`.
Appending the hāʾ therefore moves the yāʾ off the end and changes its shape, so
a character diff sees a substitution *and* an insertion where there is only an
added hāʾ. `normalize.unpositioned` folds the final shapes back into their class
for that comparison and nothing else — position is not identity. Two words moved
groups: 54/8 became 56/6.

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
is decided first now, and `reports/resegmentation.csv` carries a `riwayat_agree` column so
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

### Pairing a different word by position

When a `replace` block's letters did not agree, the old aligner paired tokens
left to right and let the surplus fall off the end. At 40:26 that put Warsh's
`وَأَنْ` against Ḥafṣ's `أَوۡ` — two words sharing one letter — and reported the
`أَن` beside it, which shares every letter, as the word Warsh does not read. The
index said Warsh lacks *an* when Warsh reads *wa-an*. Pairing now maximises
shared letters, order-preserving, and `أَوۡ` is the absent word.

### A joined word reported as a missing one

The old numbering reported Ḥafṣ as not reading `لَّوِ` at 72:16 and Dūrī as not
reading `أَن` at 73:20, because each writes the two words as one and the union
numbering had a number for the second word that the joined muṣḥaf's one token
could not take. Both statements were false: the words are read, inside
`وَأَلَّوِ` and `أَلَّن`. A printed word may now cover a run of two numbers
(`numbering.written_joined`), and "missing" means one thing only — the muṣḥaf
does not read the word.

### Round-trip by word count

The first round-trip check compared word counts per riwāyah and reported three
"failures" that were the re-segmentation working correctly. Comparing the
concatenated **rasm** instead is indifferent to word boundaries while still
catching a genuinely lost or duplicated letter. It passes clean for all seven.
