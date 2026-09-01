# Method

Four stages: parse each riwāyah into āyāt, cut āyāt into words, reduce each word
to comparable forms, then align the seven word streams into one spine.

## 0. Choosing the release

Six of the seven riwāyāt ship two releases: a 2026 `.docx` (v3.0) and a 2022
CSV/HTML package (v2). **Where they disagree, the later release is the text.**

This matters most for word boundaries, because KFGQPC revises them on purpose.
The 2026 Ḥafṣ document separates `مَا لِيَ` at 27:20 and 36:22, where Ḥafṣ's own
2022 CSV joins it as the traditional `مَالِيَ`. Neither is an error; the second is
a deliberate change of convention, and the newer convention is the one published
here.

The earlier release is never merged into the text. It is loaded only as a
cross-check, and every difference between the two is counted and reported in
`out/COMPARISON.md` under *Source integrity* — which is how the Sūsī and Dūrī
defects in `docs/ISSUES.md` were found in the first place.

The rule is asserted rather than assumed: `check_release_policy` fails the build
if a riwāyah's text is ever loaded from the older of its two packages. Loading
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

**Sūrah boundaries come from resets in the āyah numbering, not from headings.**
The v3.0 Qālūn document is missing the heading for Al-Baqarah, and typed it at
the end of the previous paragraph instead. Heading-driven segmentation
therefore shifted every sūrah after Al-Fātiḥah by one, silently. Numbering
resets are intrinsic to the text and let the parser assert, at the end, that it
found 114 sūrahs of contiguous 1..N āyāt.

The basmalah printed above a sūrah without a number of its own is kept as āyah
`0` rather than discarded, because whether it counts as an āyah is a property of
the counting tradition rather than of the text.

## 2. Tokenising

A word is a whitespace-delimited run of letters and their marks. Everything else
is peeled off and kept:

- **āyah numbers** (`U+06DD` + digits, or the presentation-form ligatures
  `U+FC00 + n − 1` that the v2 CSVs use) become the word's `aya` attribute;
- **pause marks** (`ۖ ۗ ۘ ۙ ۚ ۛ`) trail a word with no space; they are recitation
  annotation, not orthography, so they move to a `waqf` field;
- **rub-el-ḥizb** `۞` and **sajdah** `۩` become flags on the neighbouring word.

Nothing is dropped silently: a token with no consonantal content at all is
folded into its predecessor with a note.

## 3. Normalising

Five forms are derived from every word, each answering a different question.

| form | question | example |
|---|---|---|
| `uthmani` | how is it printed? | `مَٰلِكِ` |
| `folded` | what does it say, ignoring which codepoints the release used? | `مَٰلِكِ` |
| `pointed` | which letters, dots and all? | `مالك` |
| `rasm` | what is on the line in the codex? | `مالك` |
| `simple` | how would you type it plainly? | `مالك` |

**`folded` exists because the packages spell the same reading differently.** It
neutralises three things:

- **release notation** — the 2022 files write the KFGQPC sukūn head `U+06E1` and
  reuse `U+0656/0657/065E` for open tanwīn; the 2026 files write `U+0652` and the
  dedicated `U+08F0–08F2`;
- **the attached-alef letters** `U+0870–U+0882`, one codepoint for what other
  releases write as an alef plus a vowel, decomposed back again. The mapping was
  not guessed: each codepoint was aligned against the other riwāyāt's spelling of
  the same word across the whole corpus, and every entry is the majority
  correspondence with ≥5,800 confirmations;
- **editorial marks** — `U+08CC`, the proofreader's *ṣaḥḥa*, occurs 8,128 times in
  the v3.0 Warsh document and nowhere else. It was the single largest source of
  spurious differences in the corpus, and it is not text.

**`rasm` is the alignment key and the identity of a word.** It is the bare
ʿUthmānic skeleton: undotted, unvowelled, and without hamza.

That is not a convenience. The codices were written that way, and a skeleton
that keeps what was added later is not a rasm:

- **hamza** was devised by al-Khalīl in the 8th century, two centuries after the
  codices. It is dropped, and every carrier reduces to its seat — which is what
  makes `يَسۡتَهۡزِئُ` and `يَسْتَهْزِۓُ` one word, and `هَٰٓؤُلَآءِ` and `هَٰؤُلَآࢇ` one word.
- **the dots** came later still. One skeleton carries several readings by design:
  `تَعۡمَلُونَ` and `يَعۡمَلُونَ` are `ٮعملوں` twice over. Letters merge only where
  their shapes merge, which depends on position — `ب ت ث ن ي` share one tooth
  medially but part company at the end of a word, where `ب ت ث` keep the bowl,
  `ن` takes its own curve and `ي` its own tail.
- **the dagger alif** is a written alef by another name: KFGQPC's Warsh/Qālūn set
  prints `هَارُوتَ` where the Kūfī set prints `هَٰرُوتَ`. Folding them is not merely
  tidy — keeping them apart *hides* real variants, because the same fold is what
  separates `مَٰلِكِ` from `مَلِكِ`, `دِفَٰعُ` from `دَفۡعُ`, and `ٱلرِّيَٰحُ` from `ٱلرِّيحُ`.
  `مالك`/`ملك` at 1:4 — the best-known variant in the Qurʾān — was previously
  filed as a mere difference of vowelling.

`pointed` keeps the dots and is otherwise the same. The gap between the two is
itself a category of variation, and it gets its own status, `dotting_variant`.

The ṣilah waw and yeh `ۥ ۦ` are *not* folded to letters: they stand for a vowel
that is pronounced but never written, which is what lets Bazzī's `عَلَيۡهِمُۥ` align
with `عَلَيۡهِمۡ` as one word read two ways. The small high yeh `ۧ` is the opposite
case and *is* a letter — the second yāʾ of `ٱلنَّبِيِّۧنَ`, which Warsh prints on the
line as `ۑ`.

## 4. Aligning

The riwāyāt share a rasm that is identical 99.5 %+ of the time, so a progressive
alignment suffices. Ḥafṣ becomes the initial spine; each remaining riwāyah is
folded in with a `difflib` diff over rasm sequences, per sūrah.

Each diff opcode has one meaning:

- `equal` — the riwāyah joins the existing columns;
- `insert` — the riwāyah has a word the spine lacks, so a new column is created
  (this is how Bazzī's `مِن` at 9:101 gets an ID that the others simply do not use);
- `delete` — the riwāyah has no word at that column;
- `replace` — the same slot, spelled differently.

`replace` blocks of unequal length are the interesting case, and are almost
always a **word-boundary disagreement** rather than a different reading. When
the letters on both sides agree, the block is re-segmented: a word one source
printed joined (`كَانُواْيَعۡمَلُونَ`) is split back apart at the right offset, with
marks staying on the letter they sit on. Without this, the next word is falsely
reported absent from that riwāyah.

The result is one `Column` per canonical word, holding at most one token from
each riwāyah. Its position is the word's ID.

## Identifiers

- **`id`** — a running integer over the whole corpus, `1 … 77434`.
- **`i`** — the word's 1-based position within its sūrah.
- **`key`** — `sūrah:pointed#occurrence`, e.g. `1:مالك#1`. This is rebuild-stable
  and does not shift if a future release adds or removes a word earlier in the
  sūrah, so it is the safer join key for long-lived references. It is built from
  the *pointed* skeleton rather than the bare rasm because `1:مالك#1` is legible
  where `1:مالك#1`'s undotted counterpart would not be, and one canonical
  spelling makes it just as stable.

## 5. Fawāṣil

The āyah boundaries are a layer *over* the word index, in `out/fawasil.json`.
Each system lists the ID of the last word of every āyah; the riwāyāt sharing a
system agree on all of them. There are five, not four: Dūrī and Sūsī are both
Baṣrī but part company at exactly one fāṣilah, which is the whole of the
6217/6218 difference between them.

## Verification

`python3 build.py` runs three families of check and prints what it finds.

1. **Structural** — IDs contiguous, `key` unique, `i` contiguous per sūrah.
2. **Round-trip** — for each riwāyah, the concatenated rasm of every form in the
   index must equal the concatenated rasm of tokenising that riwāyah's source
   directly. Comparing letters rather than word counts makes the check
   indifferent to re-segmentation while still catching a genuinely lost or
   duplicated word. This passes for all seven.
3. **External** — parsed āyah totals against the classical counting traditions,
   which is how the Sūsī defect in `docs/ISSUES.md` surfaced.

Plus 24 unit tests over the normalisation, splitting and alignment primitives.
