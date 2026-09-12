# Changelog

Notable changes to the published format and the data. The format is
`quran-mushaf 1.0`, declared in every file and specified in `docs/format.md`.

This project has not had a tagged release yet; everything below is unreleased.

## Unreleased

### Format

- **A muṣḥaf file says what `words` is not.** `layers` gains a `text` block
  stating that `words[i]` carries no mark, that joining `words` with a space is
  neither the text the muṣḥaf prints nor what `/download` returns, and the two
  conventions that rebuild the printed text exactly: a mark whose `side` is
  `after` is appended to its word with no space, one whose `side` is `before` —
  ۞ — is written before it separated by a space. Both were true before and
  neither was written down where a consumer reading `words` would meet it;
  getting the second one wrong changes 199 āyāt in Ḥafṣ silently (#21).
- **The text is the release's, codepoint for codepoint.** The build no longer
  strips anything and no longer normalises. Three classes had been deleted on
  the reading that they are not text, and the reading did not survive the
  corpus:
  - **the kashida** `U+0640` is usually a *seat* — 535 of Ḥafṣ's 536 carry a
    hamzah, a small high yeh or a dagger alif that has no letter of its own.
    Deleting it left two marks in one run with nothing to say which belonged to
    the letter and which to the hamzah (9:120, 23:108, 30:10, 33:27, 48:25,
    53:31), let NFC compose `سَيِّـَٔاتِ` into `سَئَِّاتِ`, a spelling no muṣḥaf
    prints, and changed what the font draws;
  - **the invisible controls** — 14 in Warsh, one each in Dūrī and Sūsī — are
    kept for the same reason: they are in the package;
  - **NFC** is no longer applied. The releases write a shaddah before its
    vowel where NFC writes it after (22,000 of Ḥafṣ's 84,000 tokens) and write
    `ا` + `ٓ` where NFC composes `آ` (2,946 more). Every file now carries a
    `normalization` block saying `"applied": "none"` — **compare text across
    datasets by normalising both sides to NFC first**. The derived forms
    (`rasm`, `pointed`, `plain`, the search fold) are computed from the NFC
    form, so alignment, search and the word index are unchanged.

  **This changes 22,000–24,600 word strings per muṣḥaf**, every one of them
  back towards the package. `rasm` and `pointed` are unchanged in all 77,434
  words, the 277 published differences are unchanged, and 40 `plain` forms are
  corrected.
- **The ṣaḥḥa is a mark, not a deletion.** `U+08CC`, printed 9,950 times in the
  v3.0 Warsh document, was stripped because it reached the alignment key. It is
  now peeled like a waqf mark and published in `marks` as the kind **`sah`**
  (9,946 of them; the other four sit on basmalah words no edition publishes),
  with `raised_dot` for its `U+0888` companion. Both are dropped by every
  comparison form, which is where the problem actually was. The word index
  gains an optional `editorial` field, the six client libraries and the
  download service gain the two kinds, and `mark_signs` names both codepoints.
- **`build.py` now checks that nothing is dropped.** `check_nothing_dropped`
  compares every codepoint in each release against the codepoints in that
  muṣḥaf's published `words` and `marks`; anything in the package and in
  neither field fails the build unless it is declared — the āyah mark, its
  digits, and the space. Both deletions above were invisible to every existing
  check, because both sides of each comparison had been through the same
  stripping.
- Every name now follows the [Quran.ws terminology standard](https://github.com/quran-ws/guidelines):
  `sura`/`suras`/`sura_starts` are `surah`/`surahs`/`surah_starts`, the āyah <!-- terminology: ignore -->
  map's `ayat` is `ayahs`, the muṣḥaf's `imlaei` is `rasm_imlai`, the word <!-- terminology: ignore -->
  index's `uthmani` is `rasm_uthmani` and its `simple` is `plain`, `qari_en`/ <!-- terminology: ignore -->
  `qari_ar` are `qiraah_en`/`qiraah_ar`, `riwayat` is `riwayahs`, `pos` is <!-- terminology: ignore -->
  `position`, and the ۞ mark's kind is `division`.
- The riwāyah keys are `shubah`, `qalun`, `duri` and `susi`, so the muṣḥaf files
  are named for them.
- `counting.khilaf[]` entries carry `authorities_named`. `follows` and `against`
  are still always present; the flag says whether they are empty because the
  source does not name the two sides, rather than because there is no
  disagreement.
- The schema `$id` values resolve. They pointed at a GitHub path that serves
  nothing.
- **The sajdah line is a mark, not a letter.** The horizontal line drawn over
  the words that make the sajdah due — خط السجدة — is encoded by the releases
  as U+06E4 ARABIC SMALL HIGH MADDA at the end of each word it covers. It was
  published inside `words[i]`, where it read as a maddah the word does not
  have. It is now peeled off like a waqf mark and published in `marks` as the
  kind `sajdah_line`, with U+06E4 added to `mark_signs`. **This changes 26
  word strings** in each of Ḥafṣ, Shuʿbah, Bazzī, Dūrī and Sūsī (Warsh and
  Qālūn draw no such line and had none), and the word index gains an optional
  `sajdah_line` field beside `sajdah`. A consumer reading `words[i]` alone now
  gets the word without the line; re-attaching a word's `after` marks in the
  order `marks` lists them reproduces the printed token exactly. See
  `docs/format.md`, *Marks*.

### Data

- **Printed lines are exact for Ḥafṣ and Shuʿbah** — 6,236 of 6,236, up from
  6,131. A sūrah heading was being charged two lines rather than one; the error
  cancelled against the page-break reset for a page's first heading, so only
  pages carrying two or more headings were wrong. Warsh, Qālūn, Dūrī and Sūsī
  improve correspondingly. What remains is not reconstruction error
  (`docs/known-issues.md` §6).
- **No edition has an unexplained āyah end.** Bazzī counting 78:40 ﴿قريبًا﴾ is
  cited to al-Qāḍī's *al-Farāʾid al-Ḥisān*, which records khilāf inside the
  Makkī count at that word, and moves from `open-findings.json` to
  `khilaf.json`. `open-findings.json` is now empty (§1b).
- The 6,218 āyah total that this repository could not reconcile belongs to
  **Sūsī**, not Dūrī: KFGQPC moved the Sūsī division at 67:9 between its 2022
  and 2026 releases (§1).

### Documentation

- `docs/known-issues.md` §7 explains the ۞ counts rather than leaving them
  unreconciled: two conventions (240 rubu_al_hizbs and 480 thumns), 1:1 never
  markable, and every other absence at a sūrah opening, where the printed muṣḥaf
  states the division in a margin medallion the releases do not carry.
- §11 records that the Ḥafṣ v2 CSV's juz column disagrees with the muṣḥaf's own
  printed marks at juz 4 and juz 11. Recorded, not corrected.
- `docs/verify-in-print.md` lists what is still unknown and the page to look at.
- `docs/sources.md` adds a printed muṣḥaf, the only source here that is not a
  KFGQPC package, used for the marginal apparatus the packages omit.

### Project

- Moved to `quran-ws/quran-text`.
- **CC BY 4.0** over everything, including the six client libraries, which each
  bundle the dataset. `NOTICE.md` states what the licence cannot cover.
- CI runs the build, the tests, the service suite, the client library on the
  Python version it claims, and the terminology audit.
- `build.py` exits non-zero when its checks find anything.
