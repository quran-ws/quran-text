# Data sources

`sources/kfgqpc/` holds the King Fahd Glorious Qur'an Printing Complex (KFGQPC)
distributions the build reads; `sources/counting/` and `sources/alignment/` hold the
small data this repository adds. This is what each one contains and how it is
used.

## The short answer about word-level data

**None of these packages contain word-level data.** Every one of them is
āyah-level. This was checked exhaustively:

- the `*Data_v2-*` releases ship `id, jozz, page, sura_no, …, aya_no, aya_text`
  — one row per āyah, in CSV/JSON/XML/SQL/XLSX/TXT flavours of the same table;
- the v3.0 `.docx` releases ship one paragraph per sūrah with āyāt delimited by
  `U+06DD` + Arabic-Indic digits;
- `kfgqpc_hafs_smart_v8` looks like it might be word-level — its `aya_text` is
  space-separated groups — but the groups are **Private Use Area glyph codes**
  (`E8DB`, `E338`, …) meaningful only to the matching font, not readable text.

Word-level is therefore *derived* here, by tokenising āyah text and aligning
the riwāyāt. That derivation is the substance of this repository.

## Used as primary sources

Seven riwāyāt, one per qāriʾ pair, each parsed from a Word document.

| riwāyah | qāriʾ | file | dated |
|---|---|---|---|
| Ḥafṣ | ʿĀṣim al-Kūfī | `UthmanicHafs-v-3.0.zip :: UthmanicHafs-v-3.0.docx` | 2026-08 |
| Shuʿbah | ʿĀṣim al-Kūfī | `UthmanicShubah-v-3.0.zip :: …docx` | 2026-08 |
| Warsh | Nāfiʿ al-Madanī | `UthmanicWarsh-v-3.0.zip :: …docx` | 2026-08 |
| Qālūn | Nāfiʿ al-Madanī | `UthmanicQaloun-v-3.0.zip :: …docx` | 2026-08 |
| Sūsī | Abū ʿAmr al-Baṣrī | `UthmanicSousi-v-3.0.zip :: …docx` | 2026-08 |
| Bazzī | Ibn Kathīr al-Makkī | `UthmanicBazzi-v-3.0.zip :: …docx` | 2026-08 |
| Dūrī | Abū ʿAmr al-Baṣrī | `UthmanicDouri_V20.zip :: UthmanicDouri V20.docx` | 2022-04 |

**Bazzī exists only as a v3.0 `.docx`** — there is no `BazziData` release. Since
covering all the provided riwāyāt requires it, the `.docx` files are the primary
source for every riwāyah, which also keeps one parsing path for all seven.

**Dūrī has no v3.0 release.** Its 2022 document is used instead, which is why
Dūrī alone still carries the older notation (see `docs/method.md`).

## Used as cross-checks

The `*Data_v2-*` CSV releases, for the six riwāyāt that have them. They supply
juz'/page/line metadata and the Ḥafṣ imlāʾī text, and — more usefully — a second
opinion from the same publisher, which is the sharpest available check on each
document. What it turns up is recorded in `docs/known-issues.md`, as differences
rather than as defects — see the standing rule at the top of that file.

| riwāyah | cross-check file |
|---|---|
| Ḥafṣ | `UthmanicHafs_v2-0.zip :: …/hafsData_v2-0.csv` |
| Shuʿbah | `UthmanicShuba_v2-0.zip :: …/shubaData_v2-0.csv` |
| Warsh | `UthmanicWarsh_v2-1.zip :: …/warshData_v2-1.csv` |
| Qālūn | `UthmanicQaloun_v2-1.zip :: …/QalounData_v2-1.csv` |
| Dūrī | `UthmanicDouri_v2-0.zip :: …/DouriData_v2-0.csv` |
| Sūsī | `UthmanicSousi_v2-0.zip :: …/SousiData_v2-0.csv` |

## A printed muṣḥaf, read for what the packages omit

**This is the only source here that is not a KFGQPC package**, and it is used
for one thing the packages do not carry: the marginal division apparatus.

| | |
|---|---|
| file | `القرآن الكريم - المصحف العادي.pdf` |
| from | [archive.org/details/quran-pdf-download-hafs](https://archive.org/details/quran-pdf-download-hafs) |
| sha256 | `1cd2a1544860791a0b795e904680f4ad51bee0f692c35c1f764dc833bd1fe5f8` |
| size | 243,640,743 bytes, 640 pages |
| internal title | `standard39.pdf`, produced on Esko Automation Engine, 2019 |

**Its provenance is weaker than the packages'**, and that is stated rather than
glossed: it is a scan hosted on archive.org, it does not name its printing or
year, and it is not published by KFGQPC as a data release. It is **not
committed** — it is 232 MB, far past GitHub's limit, and the build does not read
it.

**What it was used for.** The `.docx` releases encode the inline ۞ and nothing
else; the printed muṣḥaf also marks every rubu_al_hizb with a margin medallion reading
«الحِزْبُ N» or «رُبْعُ / نِصْفُ / ثَلَاثَةُ أَرْبَاعِ الحِزْبِ N». Thirteen of
those medallions were read to complete the 240 rubu_al_hizbs, which the packages alone
cannot supply. See `docs/known-issues.md` §7.

**It was verified against this repository before being trusted.** Its muṣḥaf
page *n* is its PDF page *n+3*, and on page 151 its thirteen text lines match
`data/mushaf/hafs.json` word for word, with the sūrah heading and the basmalah
each taking a ruled line — the same layout the line reconstruction produces
(§6). It has **no text layer**: every page is a 1344×1944 image, so nothing was
extracted mechanically and each medallion was read.

**Where it contradicts a package it is not silently preferred.** At juz 4 and
juz 11 its printed marks disagree with `hafsData_v2-0.csv`; §11 records the
disagreement and `juz_starts` still follows the CSV.

## Counting-system boundaries

`sources/counting/` holds two files copied verbatim from
[quranpedia/qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map)
(MIT) at a pinned commit — `book-boundary-primitives.json`, every disputed
āyah boundary with the counting systems that count it, and
`counting-systems.json` — with the commit and SHA-256 in `UPSTREAM.md` and in
the manifest. Beside them, this repository's own `khilaf.json` records the
disagreements *inside* a system between its authorities, cited from al-Dānī's
*al-Bayān fī ʿadd āy al-Qurʾān* and, at 78:40, al-Qāḍī's *al-Farāʾid al-Ḥisān*;
`open-findings.json` the divisions no source yet explains, which is now empty;
and `declared.json` what each edition states about its own count
(nothing, for the `.docx` releases). See `docs/format.md`, *Counting*.

`sources/alignment/written-joined.json` declares the two places where a muṣḥaf prints two
words as one; see *Numbering* in the same document.

## Deliberately unused

| file | why |
|---|---|
| `MuyassarGhareeb.docx` | word meanings — glossary, not text |
| `Tajweed_Muyassar.docx` | tajwīd rules — prose, not text |
| `hafs_tafseerMouaser_v3.zip` | tafsīr — commentary, not text |
| `kfgqpc_hafs_smart_4.zip` | PUA glyph codes, not readable text (see above) |
| `HafsNastaleeq-Ver10.zip` | a font plus a specimen document |
| `1441-AI-hafs.zip` | Adobe Illustrator page artwork, not text |
| `mumtaz-1.pdf` | a scanned muṣḥaf image PDF, not text |
| all `.ttf` files | fonts; the one beside each primary `.docx` is copied to `data/fonts/` and named in the muṣḥaf file's `font` block |

The brief was to ignore translations, meanings and similar; that is applied
here, plus the sources that are images or glyph codes rather than text.

## Not committed

Two inputs exceed GitHub's hard 100 MB per-file limit and are excluded by
`.gitignore`:

| file | size |
|---|---|
| `sources/kfgqpc/1441-AI-hafs.zip` | 466 MB |
| `sources/kfgqpc/mumtaz-1.pdf` | 360 MB |

Neither is used by the build, so the pipeline runs without them. Everything the
build reads **is** committed, so `python3 pipeline/build.py` reproduces `data/`
from a fresh clone.
