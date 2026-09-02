# Limitations

What this does not do, and where its output should not be trusted without
further work.

## Warsh, Qālūn and Sūsī will look blank in most viewers

Their v3.0 documents use **Arabic Extended-B** codepoints that Unicode only
added in 2021 (`U+0870`–`U+0882`, the alef-with-attached-vowel letters) and the
open-tanwīn marks `U+08F0`–`U+08F2`. Almost no font ships glyphs for them, so
GitHub's JSON viewer, most editors and most terminals render them as blank
boxes or as nothing at all:

| riwāyah | words containing at least one such codepoint |
|---|---|
| Warsh | 19,431 |
| Sūsī | 19,183 |
| Qālūn | 17,527 |
| Bazzī | 6,766 |
| Shuʿbah | 6,649 |
| Ḥafṣ | 6,643 |

**The text is not missing and not corrupt** — `len()` and a codepoint dump both
show it. It is a font-coverage problem at the point of display. Two ways round
it: read the `folded` comparison instead, which decomposes those letters back
into an alef plus a combining vowel that any Arabic font can draw, or install a
font with Extended-B coverage. KFGQPC's own v3.0 fonts are the reference; among
freely available faces, recent Scheherazade New and Noto Naskh Arabic cover the
most of the range.

## The rasm is reconstructed, not transcribed from a manuscript

The `rasm` field is derived by normalising KFGQPC's vowelled text — dropping
dots, hamza, vowels and the dagger alif. It is **not** a transcription of any
ʿUthmānic codex. Where the packages themselves disagree about a letter, the
disagreement is reported; where they agree, the result is only as good as the
reconstruction.

Two normalisation decisions are judgement calls that a different project could
reasonably make differently:

- **Plene against defective alif is reported, not resolved.** ḥadhf vs ithbāt
  al-alif is a real difference between the regional codices, and it is the one
  place where these sources cannot be taken at their word: the two typesettings
  disagree about it in *both* directions, the Warsh/Qālūn set printing `هَارُوتَ`
  where the Kūfī set prints `هَٰرُوتَ` and `مُبَٰرَك` where it prints `مُبَارَك`.
  198 words are affected, and they get their own status, `alif_variant`, rather
  than being counted among the letters the codices disagree about — because all
  198 divide the seven riwāyāt along one line, Warsh+Qālūn against the rest,
  where the 62 real letter differences divide them fourteen ways. That is enough
  to say the class tracks the publisher; it is **not** enough to say which of
  the two hands is the codex's, or that no genuine ḥadhf khilāf is hiding inside
  the class. Deciding that needs a manuscript, not a font, and a project working
  from manuscripts should take these case by case.
- **Hamza is dropped entirely.** Correct for a rasm, but it means `النبي` and
  `النبيء` compare equal at the rasm level. The reading difference survives in
  `pointed` and in `forms`, but not in the word's identity.

## Coverage

**Seven riwāyāt, not ten qirāʾāt.** `data/` provides Ḥafṣ and Shuʿbah (ʿĀṣim),
Warsh and Qālūn (Nāfiʿ), Dūrī and Sūsī (Abū ʿAmr), and Bazzī (Ibn Kathīr). That
is four of the seven canonical qāriʾs, and Ibn Kathīr is represented by only one
of his two riwāyāt — **Qunbul is absent**. Ibn ʿĀmir, Ḥamzah and al-Kisāʾī are
absent entirely, as are the three completing the ten. Nothing here can be
described as a complete qirāʾāt comparison; it is a complete comparison *of the
provided material*.

## Word boundaries follow the latest release, and that is a choice

Where a riwāyah ships two releases that disagree about a word boundary, this
build takes the later one. The 2026 Ḥafṣ separates `مَا لِيَ` at 27:20 and 36:22;
Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`, which is the traditional muṣḥaf
spelling. Publishing the newer convention is defensible — it is the publisher's
own latest word — but it is **not** a claim that the older spelling is wrong,
and a reader who wants the traditional joined form will not find it here. Both
spellings are visible in the *Source integrity* section of `out/COMPARISON.md`.

The assumption is narrow on purpose: it applies only *within* one riwāyah, where
a later file can reasonably be read as correcting an earlier one. Nothing is
assumed across riwāyāt, and no difference between packages is treated as a
mistake by either. It also cannot discriminate for Dūrī, whose two packages are
both from 2022; there the differing spacing at 4:90, 10:26 and 11:77 is recorded
and left alone, because choosing between them would be an editorial judgement
rather than a build step.

## The word index is derived, not authoritative

No source shipped word boundaries. They come from the whitespace in KFGQPC's
own typesetting, which is a good authority but not a doctrinal one, and it is
demonstrably inconsistent between releases of the same riwāyah (`مَالِيَ` joined
in the 2022 Ḥafṣ CSV, separated in the 2026 Ḥafṣ document). Twelve words are
re-segmented by this build. Any downstream use that depends on exact word
boundaries should read `out/COMPARISON.md` first.

## IDs are stable across rebuilds, not across releases

`id` is a position. If KFGQPC ships a release that adds or removes a word, every
`id` after it shifts. Use **`key`** (`sūrah:rasm#occurrence`) as the join key for
anything long-lived — it is derived from content, not position, and survives
insertions elsewhere in the sūrah. Neither identifier is a KFGQPC identifier;
they exist only in this repository.

## What "identical" means

`status: identical` means identical **after notation folding** — the fold that
makes the 2022 sukūn `U+06E1` equal the 2026 `U+0652`. It is a claim about the
reading, not about bytes. The raw spelling of each riwāyah is always in `forms`;
compare those if you need byte equality.

The folding table itself is a judgement. It covers the mappings that could be
established with confidence by comparing two releases of the *same* riwāyah. It
deliberately does **not** attempt to equate the Arabic Extended-B attached-alif
letters (`U+0870–U+0879`, new in the 2026 Warsh/Qālūn/Sūsī files) with the
2022 spelling of alif-plus-marks, because doing so correctly needs KFGQPC's
specification for those codepoints, which is not in `data/`. Consequence: those
differences are reported as `diacritic_variant` rather than `identical`, which
inflates the diacritic bucket and deflates the identical one. The rasm — and so
the alignment and the ID — is unaffected.

## The alignment is progressive, not optimal

Riwāyāt are folded into the spine one at a time, Ḥafṣ first. A true multiple
sequence alignment could in principle place a disputed word better than this
does. At the observed level of agreement (99.0 %–99.99 % rasm identity, 17 words
total in the boundary and partial buckets) the difference is unlikely to matter,
but the order of `ORDER` in `src/quranidx/build.py` is a parameter of the result
rather than a neutral choice.

`ORDER[0]` carries more weight than the rest of the list: it is the muṣḥaf the
IDs count, so *added* and *lacking* are said with respect to Ḥafṣ. That is
deliberate — Ḥafṣ is what most word-level datasets are built on, and it is the
one muṣḥaf whose IDs come out `1 … n` with no repeat and no gap — but it is a
choice, and a project that wanted a riwāyah-neutral spine would make it
differently. It does not affect which words the riwāyāt are found to share, only
how the five places they differ are labelled and numbered.

## Where a contraction is recorded is a convention, not a claim

Three places in the corpus write as one word what the other muṣḥafs write as
two, and the two are not the same letters — the nūn is assimilated and drops off
the line:

| | fewer words | more words |
|---|---|---|
| 40:26 | `وَأَن` — five | `أَوْ` `أَن` — Ḥafṣ, Shuʿbah |
| 72:16 | `وَأَلَّوِ` — Ḥafṣ, Shuʿbah, Bazzī | `وَأَن` `لَّوِ` — the other four |
| 73:20 | `أَلَّن` — Dūrī, Sūsī | `أَن` `لَّن` — the other five |

The single word has to be recorded against one of the two spine words, and at
72:16 and 73:20 it genuinely contains both: `أَلَّن` begins with the `أن` and ends
with the `لن`. The build decides by longest shared run of letters and prefers
the earlier word on a tie, which is deterministic and reproducible — but it is a
rule for breaking a tie, not a finding about the text. Do not read the choice as
a claim that the contracted form corresponds to that spine word rather than the
other. Compare the pair together.

40:26 is not a contraction and is not ambiguous in the same way: `أَوْ` is *aw*
and `وَ` is *wa*, different words with different meanings. There `أَن` pairs with
the `أن` inside `وَأَن`, and `أَوْ` is a word Ḥafṣ and Shuʿbah have that the other
five do not.

## Not linguistically annotated

There is no root, lemma, part of speech, morphology or translation here, and no
tajwīd analysis. Pause marks are preserved per riwāyah but not interpreted.
`simple` is a mechanical de-vowelling for search and diffing, not a
transliteration or a standard imlāʾī orthography — the Ḥafṣ v2 CSV ships a real
`aya_text_emlaey` column, which is loaded as metadata but not reconciled to the
word level.

## Verification is internal

The checks prove the index is faithful to the packages in `data/` — round-trip
of every letter of every riwāyah, contiguous IDs, āyah totals against the
classical counting traditions. They do **not** prove the packages are faithful
to a printed muṣḥaf. The 260 letter-level variants in `out/rasm-variants.md` —
62 `rasm_variant` and 198 `alif_variant` — have not been checked against the
qirāʾāt literature one by one; spot checks against
well-known variants (9:101 Ibn Kathīr's `مِن`, 57:23 the Madanī rasm omitting
`هُوَ`, `مَٰلِكِ`/`مَلِكِ`, Bazzī's ṣilat al-mīm) all came out right, which is
evidence but not an audit.

**Before any use where correctness of the sacred text matters, this needs review
by someone qualified in qirāʾāt against printed maṣāḥif.**
