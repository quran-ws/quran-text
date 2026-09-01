# Method

Four stages: parse each riwayah into ayahs, cut ayahs into kalimahs, reduce each kalimah
to comparable forms, then align the seven kalimah streams into one spine.

## 0. Choosing the release

Six of the seven riwayahs ship two releases: a 2026 `.docx` (v3.0) and a 2022
CSV/HTML package (v2). **Where two files of the same riwayah disagree, the later
release is taken as a correction and is the text.** That assumption is scoped
strictly to a single riwayah — nothing is inferred from one riwayah about
another, and no difference *between* packages is treated as a mistake by either.

This matters most for kalimah boundaries, because KFGQPC revises them on purpose.
The 2026 Ḥafṣ document separates `مَا لِيَ` at 27:20 and 36:22, where Ḥafṣ's own
2022 CSV joins it as the traditional `مَالِيَ`. Neither is an error; the second is
a deliberate change of convention, and the newer convention is the one published
here.

The earlier release is never merged into the text. It is loaded only as a
cross-check, and every difference between the two is counted and reported in
`out/COMPARISON.md` under *Source integrity*.

The rule is asserted rather than assumed: `check_release_policy` fails the build
if a riwayah's text is ever loaded from the older of its two packages. Loading
them the wrong way round would publish a superseded convention while passing
every structural check.

**Dūrī is the exception the rule cannot help.** Both its packages are from 2022,
so "later" does not discriminate, and its three dropped spaces are recorded as
boundary events rather than silently resolved from the other package.

## 1. Parsing

Each `.docx` is read through its XML (`word/document.xml`), walking `<w:t>`
elements rather than regexing the markup — attribute text inside `<w:pPr>`
otherwise leaks into the text, which is how the first attempt acquired a
paragraph of tab-stop definitions.

**Surah boundaries come from resets in the ayah numbering, not from headings.**
The v3.0 Qālūn document is missing the heading for Al-Baqarah, and typed it at
the end of the previous paragraph instead. Heading-driven segmentation
therefore shifted every surah after Al-Fātiḥah by one, silently. Numbering
resets are intrinsic to the text and let the parser assert, at the end, that it
found 114 surahs of contiguous 1..N ayahs.

The basmalah printed above a surah without a number of its own is kept as ayah
`0` rather than discarded, because whether it counts as an ayah is a property of
the counting tradition rather than of the text.

## 2. Tokenising

A kalimah is a whitespace-delimited run of harfs and their marks. Everything else
is peeled off and kept:

- **ayah numbers** (`U+06DD` + digits, or the presentation-form ligatures
  `U+FC00 + n − 1` that the v2 CSVs use) become the kalimah's `ayah` attribute;
- **pause marks** (`ۖ ۗ ۘ ۙ ۚ ۛ`) trail a kalimah with no space; they are recitation
  annotation, not orthography, so they move to a `waqf` field;
- **rub al-hizb** `۞` and **sajdah** `۩` become flags on the neighbouring kalimah.

Nothing is dropped silently: a token with no consonantal content at all is
folded into its predecessor with a note.

## 3. Normalising

Five forms are derived from every kalimah, each answering a different question.

| form | question | example |
|---|---|---|
| `uthmani` | how is it printed? | `ٱلرَّحۡمَٰنِ` |
| `folded` | what does it say, ignoring which codepoints the release used? | `الرَّحْمَٰنِ` |
| `pointed` | which harfs, dots and all, as the kalimah is *read*? | `الرحمان` |
| `rasm` | what is on the line in the mushaf? | `الرحمں` |
| `simple` | how would you type it plainly? | `الرّحمان` |

`pointed` and `rasm` part company over the dagger alif: the ā of `ٱلرَّحۡمَٰنِ` is
read, so `pointed` writes it, and it is not on the line, so `rasm` does not.

**`folded` exists because the packages spell the same qira'ah differently.** It
neutralises three things:

- **release notation** — the 2022 files write the KFGQPC sukūn head `U+06E1` and
  reuse `U+0656/0657/065E` for open tanwīn; the 2026 files write `U+0652` and the
  dedicated `U+08F0–08F2`;
- **the attached-alef harfs** `U+0870–U+0882`, one codepoint for what other
  releases write as an alef plus a vowel, decomposed back again. The mapping was
  not guessed: each codepoint was aligned against the other riwayahs' spelling of
  the same kalimah across the whole corpus, and every entry is the majority
  correspondence with ≥5,800 confirmations;
- **editorial marks** — `U+08CC`, the proofreader's *ṣaḥḥa*, occurs 8,128 times in
  the v3.0 Warsh document and nowhere else. It was the single largest source of
  spurious differences in the corpus, and it is not text.

**`rasm` is the alignment key and the identity of a kalimah.** It is the bare
Uthmani skeleton: undotted, unvowelled, and without hamza.

That is not a convenience. The mushafs were written that way, and a skeleton
that keeps what was added later is not a rasm:

- **hamza** was devised by al-Khalīl in the 8th century, two centuries after the
  mushafs. It is dropped, and every carrier reduces to its seat — which is what
  makes `يَسۡتَهۡزِئُ` and `يَسْتَهْزِۓُ` one kalimah, and `هَٰٓؤُلَآءِ` and `هَٰؤُلَآࢇ` one kalimah.
- **the dots** came later still. One skeleton carries several qira'ahs by design:
  `تَعۡمَلُونَ` and `يَعۡمَلُونَ` are `ٮعملوں` twice over. Harfs merge only where
  their shapes merge, which depends on position — `ب ت ث ن ي` share one tooth
  medially but part company at the end of a kalimah, where `ب ت ث` keep the bowl,
  `ن` takes its own curve and `ي` its own tail.
- **the dagger alif** is, by definition, an alef the scribe did *not* write on
  the line. It is the reader's cue for ḥadhf al-alif, and it is the mechanism by
  which one skeleton carries two qira'ahs: `ملك` is what every mushaf has at 1:4,
  and it is written that way so as to be read both `مَٰلِكِ` and `مَلِكِ`. The same
  goes for `دفع` (`دِفَٰعُ`/`دَفۡعُ`), `الريح` (`ٱلرِّيَٰحَ`/`ٱلرِّيحَ`), `كلمٮ`
  (`كَلِمَٰتُ`/`كَلِمَتُ`) and `طٮرا` (`طَٰٓئِراً`/`طَيۡرًا`). Counting the dagger as a
  harf reports all of those as disagreements between mushafs that agree, and
  it is what the build used to do: 170 of the 232 rasm disagreements it reported
  were this and nothing else. The ā is not lost — it is read, so `pointed` keeps
  it, and 1:4 is a `dotting_variant`: one rasm, two qira'ahs.

  A dagger riding on a final `ى` was also emitted as a *second* harf, so
  `عَلَىٰٓ` came out `علٮا` and 34:17 `يُجَٰزَىٰ` came out six harfs long. 3,071
  kalimah positions carried an inflated skeleton for this reason.

  `pointed` still counts the dagger, since it spells the qira'ah, and there it
  needs the one rule that looks further than a character and its neighbour: `ٰٓ`
  is a madd *over* something, and what it is over decides. Over a hamza
  (`إِسۡرَٰٓءِيلَ`), over a doubled harf (`تَتَّبِعَٰٓنِّ`, madd lāzim), or at the end
  of a kalimah (`عَلَىٰٓ`), the dagger is a real ā. Over a plain undoubled harf
  there is no hamza for the madd to be over, because the qira'ah suppressed it —
  Warsh's `ࡰرَٰٓيْتَ` against Ḥafṣ's `أَرَءَيۡتَ` — so the dagger *is* the hamza, and
  hamza is not part of the qira'ah's harfs either.

An alef that *is* on the line stays, whichever hand wrote it, so a difference in
one is a difference in the rasm — 260 kalimahs. But **the bare rasm cannot settle
on its own which ā a mushaf put there**, because the two typesettings disagree
about that in both directions: the Warsh/Qālūn set prints `هَارُوتَ` where the
Kūfī set prints `هَٰرُوتَ`, and `مُبَٰرَك` where it prints `مُبَارَك`. A sixth form,
`rasm_plene`, spells every ā out and so makes the two hands comparable. The 198
kalimahs whose skeletons agree once it is applied get their own status,
`alif_variant`; the 62 that remain are `rasm_variant`.

That split is drawn by the corpus, not chosen. **All 198 plene/defective kalimahs
divide the seven riwayahs along exactly one line — Warsh+Qālūn against the other
five — in both directions and without a single exception. The 62 divide them
fourteen different ways**: Bazzī alone seven times, Ḥafṣ+Shuʿbah alone six,
Qālūn alone five, Sūsī alone once. Ḥadhf and ithbāt al-alif genuinely do vary
between the mushafs of the amṣār — but a khilāf of the amṣār would sometimes put
Makkah with Madinah, and this one never does, 198 times out of 198. What
partitions by publisher is the publisher's hand. `validate.check_alif_splits`
asserts the one-partition fact so that a future package cannot quietly break the
ground the status stands on.

The bare `rasm` keeps the distinction all the same, because inside one mushaf it
is that mushaf's own ḥadhf and it is kept faithfully: Ḥafṣ writes قال plene 412
times and defective 4, سبحان defective 12 and plene once, and 175 of the 198
kalimahs show the identical split at every occurrence in the corpus. Each book is
consistent with itself. What no font can say is which of the two hands is the
mushaf's.

The 62 `rasm_variant` kalimahs are the received list, and the report tables them by
what the difference is. 56 are one skeleton with one harf more —
`ووصى`/`وأوصى` at 2:132, `ٮرٮد`/`ٮرٮدد` (يَرۡتَدَّ/يَرۡتَدِدۡ) at 5:54,
`ٮسٮهى`/`ٮسٮهٮه` (تَشۡتَهِي/تَشۡتَهِيهِ) at 43:71, `قال`/`قل` at 21:4 and 23:112,
`لله`/`الله` at 23:87. 6 are one harf exchanged for another:
`كلمت`/`كلمة` at 7:137, `ولا`/`فلا` at 91:15.

Telling those two apart needs one more fold. The rasm keeps the final harf
shapes, because the mushafs did — a nūn ending a kalimah has its own curve, `ں`,
where medially it is a tooth, `ٮ` — so appending a hāʾ to `ٮسٮهى` moves the yāʾ
off the end of the kalimah and changes its shape too, and a plain character diff
reads the added harf as a substitution as well. `normalize.unpositioned` folds
the final shapes back into their class for the comparison, and only for it.

`pointed` keeps the dots and is otherwise the same. The gap between the two is
itself a category of variation, and it gets its own status, `dotting_variant`.

The ṣilah waw and yeh `ۥ ۦ` are *not* folded to harfs: they stand for a vowel
that is pronounced but never written, which is what lets Bazzī's `عَلَيۡهِمُۥ` align
with `عَلَيۡهِمۡ` as one kalimah read two ways. The small high yeh `ۧ` is the opposite
case and *is* a harf — the second yāʾ of `ٱلنَّبِيِّۧنَ`, which Warsh prints on the
line as `ۑ`.

## 4. Aligning

The riwayahs share a rasm that is identical 99.5 %+ of the time, so a progressive
alignment suffices. Ḥafṣ becomes the initial spine; each remaining riwayah is
folded in with a `difflib` diff over rasm sequences, per surah.

Each diff opcode has one meaning:

- `equal` — the riwayah joins the existing columns;
- `insert` — the riwayah has a kalimah the spine lacks, so a new column is created
  (this is how Bazzī's `مِن` at 9:101 gets an ID that the others simply do not use);
- `delete` — the riwayah has no kalimah at that column;
- `replace` — the same slot, spelled differently.

`replace` blocks of unequal length are the interesting case, and are almost
always a **kalimah-boundary disagreement** rather than a different qira'ah. When
the harfs on both sides agree, the block is re-segmented: a kalimah one source
printed joined (`كَانُواْيَعۡمَلُونَ`) is split back apart at the right offset, with
marks staying on the harf they sit on. Without this, the next kalimah is falsely
reported absent from that riwayah.

The result is one `Column` per canonical kalimah, holding at most one token from
each riwayah. Its position is the kalimah's ID.

## Identifiers

- **`id`** — a running integer over the whole corpus, `1 … 77434`.
- **`i`** — the kalimah's 1-based position within its surah.
- **`key`** — `surah:pointed#occurrence`, e.g. `1:مالك#1`. This is rebuild-stable
  and does not shift if a future release adds or removes a kalimah earlier in the
  surah, so it is the safer join key for long-lived references. It is built from
  the *pointed* skeleton rather than the bare rasm because `1:مالك#1` is legible
  where `1:مالك#1`'s undotted counterpart would not be, and one canonical
  spelling makes it just as stable.

## 5. Fasilahs

The ayah boundaries are a layer *over* the kalimah index, in `out/fasilahs.json`.
Each system lists the ID of the last kalimah of every ayah; the riwayahs sharing a
system agree on all of them. There are five, not four: Dūrī and Sūsī are both
Baṣrī but part company at exactly one fasilah, which is the whole of the
6217/6218 difference between them.

## Verification

`python3 build.py` runs three families of check and prints what it finds.

1. **Structural** — IDs contiguous, `key` unique, `i` contiguous per surah.
2. **Round-trip** — for each riwayah, the concatenated rasm of every form in the
   index must equal the concatenated rasm of tokenising that riwayah's source
   directly. Comparing harfs rather than kalimah counts makes the check
   indifferent to re-segmentation while still catching a genuinely lost or
   duplicated kalimah. This passes for all seven.
3. **Release policy** — the text of each riwayah must come from its latest
   package, since that is the only correction this pipeline assumes.

There is deliberately **no** check of ayah totals against the counting
traditions. An earlier version had one, and it was measuring an assumption: the
qira'ah does not determine the count, many fasilahs are مختلف فيها, and KFGQPC's
own Dūrī printings total 6,218, 6,217 and 6,214 while all three state they
follow المدني الأول. See `docs/ISSUES.md`.

Plus 24 unit tests over the normalisation, splitting and alignment primitives.
