# Method

Four stages: parse each riwāyah into āyāt, cut āyāt into words, reduce each word
to comparable forms, then align the seven word streams into one spine.

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

Four forms are derived from every word, each answering a different question.

| form | question | example |
|---|---|---|
| `uthmani` | how is it printed? | `مَٰلِكِ` |
| `folded` | what does it say, ignoring which codepoints the release used? | `مَٰلِكِ` |
| `rasm` | which letters are on the line? | `ملك` |
| `simple` | how would you type it plainly? | `مالك` |

**`folded` exists because the 2022 and 2026 releases spell the same reading
differently.** The 2022 files write the KFGQPC sukūn head `U+06E1` and reuse
`U+0656/0657/065E` for open tanwīn; the 2026 files write `U+0652` and the
dedicated `U+08F0–08F2`. Without folding, Dūrī — the one riwāyah still on a
2022 document — would report thousands of differences against everything else
that are purely typographic.

**`rasm` is the alignment key**, and the boundary between "same word, read
differently" and "different word". It folds every alif spelling (`ا أ إ آ ٱ`
and the Arabic Extended-B attached-alif letters `U+0870–U+0879` that the 2026
Warsh/Qālūn/Sūsī files introduce) to a bare alif, folds `ؤ ئ ى ة ے ۑ` to their
base letters, and drops all marks.

Superscript letters — the ṣilah waw and yeh `ۥ ۦ`, the small high yeh `ۧ` — are
marks, not letters: they stand for a vowel that is pronounced but not written on
the line. That is what lets Bazzī's `عَلَيۡهِمُۥ` align with `عَلَيۡهِمۡ` as one word
read two ways rather than splitting into two unrelated words.

## 4. Aligning

The riwāyāt share a rasm that is identical 99 %+ of the time, so a progressive
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
- **`key`** — `sūrah:rasm#occurrence`, e.g. `1:ملك#1`. This is rebuild-stable
  and does not shift if a future release adds or removes a word earlier in the
  sūrah, so it is the safer join key for long-lived references.

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

Plus 16 unit tests over the normalisation, splitting and alignment primitives.
