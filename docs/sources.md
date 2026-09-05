# Data sources

`data/kfgqpc/` holds the King Fahd Glorious Qur'an Printing Complex (KFGQPC)
distributions the build reads; `data/counting/` and `data/alignment/` hold the
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
covering all the provided qirāʾāt requires it, the `.docx` files are the primary
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

## Counting-system boundaries

`data/counting/` holds two files copied verbatim from
[quranpedia/qiraat-ayah-map](https://github.com/quranpedia/qiraat-ayah-map)
(MIT) at a pinned commit — `book-boundary-primitives.json`, every disputed
āyah boundary with the counting systems that count it, and
`counting-systems.json` — with the commit and SHA-256 in `UPSTREAM.md` and in
the manifest. Beside them, this repository's own `khilaf.json` records the
disagreements *inside* a system between its authorities, cited from al-Dānī's
*al-Bayān fī ʿadd āy al-Qurʾān*, `open-findings.json` the divisions no source
yet explains, and `declared.json` what each edition states about its own count
(nothing, for the `.docx` releases). See `docs/format.md`, *Counting*.

`data/alignment/written-joined.json` declares the two places where a muṣḥaf prints two
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
| all `.ttf` files | fonts |

The brief was to ignore translations, meanings and similar; that is applied
here, plus the sources that are images or glyph codes rather than text.

## Not committed

Two inputs exceed GitHub's hard 100 MB per-file limit and are excluded by
`.gitignore`:

| file | size |
|---|---|
| `data/kfgqpc/1441-AI-hafs.zip` | 466 MB |
| `data/kfgqpc/mumtaz-1.pdf` | 360 MB |

Neither is used by the build, so the pipeline runs without them. Everything the
build reads **is** committed, so `python3 build.py` reproduces `out/` from a
fresh clone.
