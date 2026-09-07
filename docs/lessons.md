# Lessons: mistakes made building this

Recorded because each cost real time and each would recur.

### Word counts hid a sūrah-level shift

The first Qālūn parse produced 6,214 āyāt — the correct Madanī total — while
being wrong about which sūrah every āyah belonged to. **A correct total is not
a correct parse.** The check that caught it was structural: 113 sūrahs, not 114.
Asserting an invariant the data must satisfy found in one line what comparing
totals would never have found.

### Regexing XML

`re.findall(r'<w:t[^>]*>(.*?)</w:t>')` over `document.xml` looked fine on Ḥafṣ
and returned a paragraph of `<w:tab w:val="left" w:position="4377"/>` tab-stop
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
skeleton is written so as to carry two qiraahs. `ملك` is what every codex has
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

A second defect fell out of the same code. The guard that keeps `اٰ` from
emitting two alefs tested only for a preceding `ا`, so a dagger riding on a
final `ى` was emitted as an *extra letter*: `عَلَىٰٓ` came out `علٮا` and 34:17
`يُجَٰزَىٰ` came out `ٮحارٮا`, six letters for a four-letter word. **3,071 word
positions** carried an inflated skeleton. 34:17 was consequently filed as a rasm
disagreement when `نُجَٰزِي` and `يُجَٰزَىٰ` are one skeleton pointed two ways.

The ā is not lost. It is read, so `pointed` keeps it, and 1:4 is now a
`dotting_variant`: one rasm, two qiraahs — which is what it is.

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
`docs/limitations.md` says plainly that separating codex from typesetter here
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

**All 198 split the seven riwāyāt along exactly one line: `qalun,warsh` against
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
between the two typesettings that the choice no longer tracks anything textual.

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
is decided first now, and `reports/resegmentation.csv` carries a `riwayahs_agree` column so
the two cases are told apart rather than conflated.

### "No local rule can separate these" — there was one

34 words of the `أَرَءَيۡتَ` family were shipped as a known residual, reported as
`rasm_variant` when the codices agree. Warsh writes `ࡰرَٰٓيْتَ`, spelling the
tashīl'd hamzah as a dagger alif; Ḥafṣ writes `أَرَءَيۡتَ` with a hamzah. Dropping
hamzah and folding the dagger to an alef made Ḥafṣ lose a letter and Warsh gain
one.

Three rules were tried and rejected, and the conclusion drawn was that no rule
looking at the glyphs and their neighbours could work, because `إِسۡرَٰٓءِيلَ`
needs the opposite treatment with the same local context. That conclusion was
wrong: the context is not the same, it just extends one character further than
was being looked at.

`ٰٓ` is a madd **over** something. What it is over is what decides:

| after the `ٰٓ` | example | the dagger is |
|---|---|---|
| a hamzah | `إِسۡرَٰٓءِيلَ`, `هَٰٓؤُلَآءِ`, `مَلَٰٓئِكَةِ` | a written ā |
| a doubled letter | `تَتَّبِعَٰٓنِّ`, `فَذَٰٓنِّكَ` | a written ā (madd lāzim) |
| nothing — end of word | `عَلَىٰٓ` | a written ā |
| a plain undoubled letter | `ࡰرَٰٓيْتَ` | **the suppressed hamzah** |

The first attempt at this rule handled only the first and third rows and
introduced two new false positives at 10:89 and 28:32 — caught by diffing the
flagged-ID set against the previous build rather than by trusting the headline
count, which had moved in the right direction while being wrong. Qālūn writes
the same madd with `U+06EC` instead of a maddah, which was a second miss.

Result: 266 → 232 rasm disagreements, 34 resolved, none newly flagged.

The generalisable part is not about hamzah. It is that "no rule can distinguish
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

The old numbering reported Ḥafṣ as not reciting `لَّوِ` at 72:16 and Dūrī as not
reciting `أَن` at 73:20, because each writes the two words as one and the union
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
