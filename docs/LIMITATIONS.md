# Limitations

What this does not do, and where its output should not be trusted without
further work.

## Warsh, Qālūn and Sūsī will look blank in most viewers

Their v3.0 documents use **Arabic Extended-B** codepoints that Unicode only
added in 2021 (`U+0870`–`U+0882`, the alef-with-attached-vowel harfs) and the
open-tanwīn marks `U+08F0`–`U+08F2`. Almost no font ships glyphs for them, so
GitHub's JSON viewer, most editors and most terminals render them as blank
boxes or as nothing at all:

| riwayah | kalimahs containing at least one such codepoint |
|---|---|
| Warsh | 19,431 |
| Sūsī | 19,183 |
| Qālūn | 17,527 |
| Bazzī | 6,766 |
| Shuʿbah | 6,649 |
| Ḥafṣ | 6,643 |

**The text is not missing and not corrupt** — `len()` and a codepoint dump both
show it. It is a font-coverage problem at the point of display. Two ways round
it: read the `folded` comparison instead, which decomposes those harfs back
into an alef plus a combining vowel that any Arabic font can draw, or install a
font with Extended-B coverage. KFGQPC's own v3.0 fonts are the reference; among
freely available faces, recent Scheherazade New and Noto Naskh Arabic cover the
most of the range.

## The rasm is reconstructed, not transcribed from a manuscript

The `rasm` field is derived by normalising KFGQPC's vowelled text — dropping
dots, hamza, vowels and the dagger alif. It is **not** a transcription of any
Uthmani mushaf. Where the packages themselves disagree about a harf, the
disagreement is reported; where they agree, the result is only as good as the
reconstruction.

Two normalisation decisions are judgement calls that a different project could
reasonably make differently:

- **Plene against defective alif is reported, not resolved.** ḥadhf vs ithbāt
  al-alif is a real difference between the regional mushafs, and it is the one
  place where these sources cannot be taken at their kalimah: the two typesettings
  disagree about it in *both* directions, the Warsh/Qālūn set printing `هَارُوتَ`
  where the Kūfī set prints `هَٰرُوتَ` and `مُبَٰرَك` where it prints `مُبَارَك`.
  198 kalimahs are affected, and they get their own status, `alif_variant`, rather
  than being counted among the harfs the mushafs disagree about — because all
  198 divide the seven riwayahs along one line, Warsh+Qālūn against the rest,
  where the 62 real harf differences divide them fourteen ways. That is enough
  to say the class tracks the publisher; it is **not** enough to say which of
  the two hands is the mushaf's, or that no genuine ḥadhf khilāf is hiding inside
  the class. Deciding that needs a manuscript, not a font, and a project working
  from manuscripts should take these case by case.
- **Hamza is dropped entirely.** Correct for a rasm, but it means `النبي` and
  `النبيء` compare equal at the rasm level. The qira'ah difference survives in
  `pointed` and in `forms`, but not in the kalimah's identity.

## Coverage

**Seven riwayahs, not ten qira'ahs.** `data/` provides Ḥafṣ and Shuʿbah (ʿĀṣim),
Warsh and Qālūn (Nāfiʿ), Dūrī and Sūsī (Abū ʿAmr), and Bazzī (Ibn Kathīr). That
is four of the seven canonical qaris, and Ibn Kathīr is represented by only one
of his two riwayahs — **Qunbul is absent**. Ibn ʿĀmir, Ḥamzah and al-Kisāʾī are
absent entirely, as are the three completing the ten. Nothing here can be
described as a complete qira'ahs comparison; it is a complete comparison *of the
provided material*.

## Kalimah boundaries follow the latest release, and that is a choice

Where a riwayah ships two releases that disagree about a kalimah boundary, this
build takes the later one. The 2026 Ḥafṣ separates `مَا لِيَ` at 27:20 and 36:22;
Ḥafṣ's own 2022 CSV joins it as `مَالِيَ`, which is the traditional mushaf
spelling. Publishing the newer convention is defensible — it is the publisher's
own latest verdict — but it is **not** a claim that the older spelling is wrong,
and a reader who wants the traditional joined form will not find it here. Both
spellings are visible in the *Source integrity* section of `out/COMPARISON.md`.

The assumption is narrow on purpose: it applies only *within* one riwayah, where
a later file can reasonably be read as correcting an earlier one. Nothing is
assumed across riwayahs, and no difference between packages is treated as a
mistake by either. It also cannot discriminate for Dūrī, whose two packages are
both from 2022; there the differing spacing at 4:90, 10:26 and 11:77 is recorded
and left alone, because choosing between them would be an editorial judgement
rather than a build step.

## The kalimah index is derived, not authoritative

No source shipped kalimah boundaries. They come from the whitespace in KFGQPC's
own typesetting, which is a good authority but not a doctrinal one, and it is
demonstrably inconsistent between releases of the same riwayah (`مَالِيَ` joined
in the 2022 Ḥafṣ CSV, separated in the 2026 Ḥafṣ document). Twelve kalimahs are
re-segmented by this build. Any downstream use that depends on exact kalimah
boundaries should read `out/COMPARISON.md` first.

## IDs are stable across rebuilds, not across releases

`id` is a position. If KFGQPC ships a release that adds or removes a kalimah, every
`id` after it shifts. Use **`key`** (`surah:rasm#occurrence`) as the join key for
anything long-lived — it is derived from content, not position, and survives
insertions elsewhere in the surah. Neither identifier is a KFGQPC identifier;
they exist only in this repository.

## What "identical" means

`status: identical` means identical **after notation folding** — the fold that
makes the 2022 sukūn `U+06E1` equal the 2026 `U+0652`. It is a claim about the
qira'ah, not about bytes. The raw spelling of each riwayah is always in `forms`;
compare those if you need byte equality.

The folding table itself is a judgement. It covers the mappings that could be
established with confidence by comparing two releases of the *same* riwayah. It
deliberately does **not** attempt to equate the Arabic Extended-B attached-alif
harfs (`U+0870–U+0879`, new in the 2026 Warsh/Qālūn/Sūsī files) with the
2022 spelling of alif-plus-marks, because doing so correctly needs KFGQPC's
specification for those codepoints, which is not in `data/`. Consequence: those
differences are reported as `diacritic_variant` rather than `identical`, which
inflates the diacritic bucket and deflates the identical one. The rasm — and so
the alignment and the ID — is unaffected.

## The alignment is progressive, not optimal

Riwayahs are folded into the spine one at a time, Ḥafṣ first. A true multiple
sequence alignment could in principle place a disputed kalimah better than this
does. At the observed level of agreement (99.0 %–99.99 % rasm identity, 17 kalimahs
total in the boundary and partial buckets) the difference is unlikely to matter,
but the order of `ORDER` in `src/quranidx/build.py` is a parameter of the result
rather than a neutral choice.

## Not linguistically annotated

There is no root, lemma, part of speech, morphology or translation here, and no
tajwīd analysis. Pause marks are preserved per riwayah but not interpreted.
`simple` is a mechanical de-vowelling for search and diffing, not a
transliteration or a standard imlāʾī orthography — the Ḥafṣ v2 CSV ships a real
`aya_text_emlaey` column, which is loaded as metadata but not reconciled to the
kalimah level.

## Verification is internal

The checks prove the index is faithful to the packages in `data/` — round-trip
of every harf of every riwayah, contiguous IDs, ayah totals against the
classical counting traditions. They do **not** prove the packages are faithful
to a printed mushaf. The 260 harf-level variants in `out/rasm-variants.md` —
62 `rasm_variant` and 198 `alif_variant` — have not been checked against the
qira'ahs literature one by one; spot checks against
well-known variants (9:101 Ibn Kathīr's `مِن`, 57:23 the Madanī rasm omitting
`هُوَ`, `مَٰلِكِ`/`مَلِكِ`, Bazzī's ṣilat al-mīm) all came out right, which is
evidence but not an audit.

**Before any use where correctness of the sacred text matters, this needs review
by someone qualified in qira'ahs against printed maṣāḥif.**
