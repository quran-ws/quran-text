# Limitations

What this does not do, and where its output should not be trusted without
further work.

## Coverage

**Seven riwāyāt, not ten qirāʾāt.** `data/` provides Ḥafṣ and Shuʿbah (ʿĀṣim),
Warsh and Qālūn (Nāfiʿ), Dūrī and Sūsī (Abū ʿAmr), and Bazzī (Ibn Kathīr). That
is four of the seven canonical qāriʾs, and Ibn Kathīr is represented by only one
of his two riwāyāt — **Qunbul is absent**. Ibn ʿĀmir, Ḥamzah and al-Kisāʾī are
absent entirely, as are the three completing the ten. Nothing here can be
described as a complete qirāʾāt comparison; it is a complete comparison *of the
provided material*.

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
to a printed muṣḥaf. The 968 rasm variants in `out/rasm-variants.md` have not
been checked against the qirāʾāt literature one by one; spot checks against
well-known variants (9:101 Ibn Kathīr's `مِن`, 57:23 the Madanī rasm omitting
`هُوَ`, `مَٰلِكِ`/`مَلِكِ`, Bazzī's ṣilat al-mīm) all came out right, which is
evidence but not an audit.

**Before any use where correctness of the sacred text matters, this needs review
by someone qualified in qirāʾāt against printed maṣāḥif.**
