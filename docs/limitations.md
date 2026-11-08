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
show it. It is a font-coverage problem at the point of display. The fix is the
font KFGQPC ships with each text: every muṣḥaf file names it in its `font`
block and the build copies it to `data/fonts/`, so a viewer that loads that
font draws every word. Failing that, read the `folded` comparison instead,
which decomposes those letters back into an alef plus a combining vowel that
any Arabic font can draw; among general faces, recent Scheherazade New and Noto
Naskh Arabic cover the most of the range.

## The rasm is reconstructed, not transcribed from a manuscript

The `rasm` field is derived by normalising KFGQPC's vowelled text — dropping
dots, hamzah, vowels and the dagger alif. It is **not** a transcription of any
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
- **Hamzah is dropped entirely.** Correct for a rasm, but it means `النبي` and
  `النبيء` compare equal at the rasm level. The difference in qiraah survives in
  `pointed` and in `forms`, but not in the word's identity.

## Coverage

**Sixteen riwāyāt in two tiers, not twenty in one.** KFGQPC's data releases
provide Ḥafṣ and Shuʿbah (ʿĀṣim), Warsh and Qālūn (Nāfiʿ), Dūrī and Sūsī (Abū
ʿAmr), and Bazzī (Ibn Kathīr): tier 1, read as published. Nine more — Hishām
(Ibn ʿĀmir), Khalaf and Khallād (Ḥamzah), Abū al-Ḥārith (al-Kisāʾī), Ibn Wardān
and Ibn Jammāz (Abū Jaʿfar), Ruways and Rawḥ (Yaʿqūb), Isḥāq (Khalaf
al-ʿĀshir) — are tier 2: decoded from documents of unnamed authorship hosted by
islamweb, with the weaker provenance that implies stated in every file
(`docs/sources.md`, *Tier 2*). **Four riwāyāt are absent**: Qunbul, which
KFGQPC released in 2021 and which will be added from that package once it is
archived with a recorded origin; Ibn Dhakwān and al-Dūrī ʿan al-Kisāʾī, which
islamweb has only as page scans; and Idrīs, whose islamweb file is the Isḥāq
file under another name (`docs/known-issues.md` §17). Nothing here is a qirāʾāt comparison on
one footing: the tier-2 texts are decoded, not read, and a difference between a
tier-2 word and Ḥafṣ should be weighed against the decoder's measured accuracy
in `provenance.decoder` before it is cited.

**Tier-2 texts are decoded, not read.** Their words are table lookups from
glyph ids (`docs/method.md`, *Decoding*). The table was learned on the three
riwāyāt both sources carry and scored there; it was never scored on the nine
riwāyāt it is applied to, because nothing exists to score them against. What
can be said is that every glyph in them is one the table knows, and that the
documents' colouring of the letters that differ from Ḥafṣ agrees with the
decoded differences (`check_colors`). The notation is the 2022 KFGQPC one and
differs from the 2026 releases of tier 1 in the ways `docs/method.md` lists;
compare across tiers through `fold_notation`, as the word index does.

## Word boundaries follow the latest release, and that is a choice

Where a riwāyah ships two releases that disagree about a word boundary, this
build takes the later one. The 2026 Ḥafṣ separates `مَا لِيَ` at 27:20 and 36:22;
Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`, which is the traditional muṣḥaf
spelling. Publishing the newer convention is defensible — it is the publisher's
own latest word — but it is **not** a claim that the older spelling is wrong,
and a reader who wants the traditional joined form will not find it here. Both
spellings are visible in the *Source integrity* section of `data/reports/COMPARISON.md`.

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
boundaries should read `data/reports/COMPARISON.md` first.

## Numbers are stable across rebuilds, not across releases

The shared number is a position in the union of the seven texts. If KFGQPC
ships a release that adds or removes a word, every number after it shifts. Use
**`key`** (`sūrah:pointed#occurrence`) or the word index's Ḥafṣ coordinates
`{surah, ayah, position}` as the join key for anything long-lived — both are
derived from content, not from the running count. Neither identifier is a
KFGQPC identifier; they exist only in this repository.

Two words are written joined by some muṣḥafs — `وَأَلَّوِ` at 72:16, `أَلَّن` at
73:20 — and the numbering counts them as two words in every file, with the
joined muṣḥaf's one printed word covering both numbers. That these are joins
and not different words is a judgement declared in `sources/alignment/written-joined.json`,
not derived; 40:26 `أَوۡ أَن` / `وَأَنْ` is deliberately *not* on that list.

## What "identical" means

`status: identical` means identical **after notation folding** — the fold that
makes the 2022 sukūn `U+06E1` equal the 2026 `U+0652`. It is a claim about the
qiraah, not about bytes. The raw spelling of each riwāyah is always in `forms`;
compare those if you need byte equality.

The folding table itself is a judgement. It covers the mappings that could be
established with confidence by comparing two releases of the *same* riwāyah. It
deliberately does **not** attempt to equate the Arabic Extended-B attached-alif
letters (`U+0870–U+0879`, new in the 2026 Warsh/Qālūn/Sūsī files) with the
2022 spelling of alif-plus-marks, because doing so correctly needs KFGQPC's
specification for those codepoints, which is not in `sources/`. Consequence: those
differences are reported as `diacritic_variant` rather than `identical`, which
inflates the diacritic bucket and deflates the identical one. The rasm — and so
the alignment and the ID — is unaffected.

## The alignment is progressive, not optimal

Riwāyāt are folded into the alignment one at a time, Ḥafṣ first. A true multiple
sequence alignment could in principle place a disputed word better than this
does. At the observed level of agreement (99.0 %–99.99 % rasm identity, 19 words
total in the boundary and partial buckets) the difference is unlikely to matter,
but the order of `ORDER` in `pipeline/qurantext/build.py` is a parameter of the result
rather than a neutral choice.

## Not linguistically annotated

There is no root, lemma, part of speech, morphology or translation here, and no
tajwīd analysis. Waqf marks are preserved per riwāyah but not interpreted.
`plain` is a mechanical de-vowelling for search and diffing, not a
transliteration or the standard imlāʾī rasm — the Ḥafṣ v2 CSV ships a real
`aya_text_emlaey` column, which is loaded as metadata but not reconciled to the
word level.

## Verification is internal

The checks prove the index is faithful to the packages in `sources/` — round-trip
of every letter of every riwāyah, a numbering that tiles, and each edition's
āyah division matching a classical counting system once the documented khilāf
is set aside. They do **not** prove the packages are faithful to a printed
muṣḥaf. **No edition has an unexplained āyah end**: the last one — the Bazzī
edition counting 78:40 ﴿قريبًا﴾ — is cited to al-Qāḍī's *al-Farāʾid al-Ḥisān*,
which records khilāf inside the Makkī count at that word, and
`open-findings.json` is now empty. The 258 letter-level variants in `data/reports/rasm-variants.md` —
62 `rasm_variant` and 198 `alif_variant` — have not been checked against the
qirāʾāt literature one by one; spot checks against
well-known variants (9:101 Ibn Kathīr's `مِن`, 57:24 the Madanī rasm omitting
`هُوَ`, `مَٰلِكِ`/`مَلِكِ`, Bazzī's ṣilat al-mīm) all came out right, which is
evidence but not an audit.

**Before any use where correctness of the sacred text matters, this needs review
by someone qualified in qirāʾāt against printed maṣāḥif.**
