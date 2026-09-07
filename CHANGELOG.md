# Changelog

Notable changes to the published format and the data. The format is
`quran-mushaf 1.0`, declared in every file and specified in `docs/format.md`.

This project has not had a tagged release yet; everything below is unreleased.

## Unreleased

### Format

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
