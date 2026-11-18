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


## Where these packages come from

**The publisher's site is geo-restricted.** Every KFGQPC package here was
published at `qurancomplex.gov.sa`, and that host does not answer requests from
outside Saudi Arabia: DNS resolves, and the connection then times out or is
refused. It is not a misconfiguration, it is not an outage, and retrying does
not help. If you are outside the Kingdom and a fetch hangs, this is why — stop
there rather than looking for a mirror that merely resembles the file.

The route that works is
[quran-ws/kfgqpc-resources](https://github.com/quran-ws/kfgqpc-resources), an
archive that keeps each published file byte-for-byte and records its official
URL, its dates and its checksums. Everything below was read from that archive at
commit `925b9434`. The official URL is the publisher's own; the reachable copy
is the same bytes, served from where they can be got.

Both URLs are formulaic, and every package below was checked to follow them:

```
official   https://download.qurancomplex.gov.sa/resources_dev/<file>
reachable  https://cdn.quran.ws/KFGQPC/resources/quran-dev/<slug>/<file>
```

| package | slug | sha256 |
|---|---|---|
| `UthmanicHafs_v2-0.zip` | `uthmanic-hafs` | `a7b0e559…fd72c` |
| `UthmanicShuba_v2-0.zip` | `uthmanic-shuba` | `977e64f3…2efcf` |
| `UthmanicWarsh_v2-1.zip` | `uthmanic-warsh` | `d847a7e7…88b47` |
| `UthmanicQaloun_v2-1.zip` | `uthmanic-qaloun` | `6988b782…b144d` |
| `UthmanicDouri_v2-0.zip` | `uthmanic-douri` | `84e55697…2cb0c1` |
| `UthmanicSousi_v2-0.zip` | `uthmanic-sousi` | `e912273b…5ce472` |

The full digests are in `data/manifest.json`. Each was verified twice: the
archive's recorded checksum matches the file committed here, and re-downloading
`UthmanicDouri_v2-0.zip` from the reachable copy reproduced
`84e5569790f96b05896b8f44ebe8d82d98377a929ac0e87dd8af4dbec52cb0c1` exactly.

### The primary text packages: from the publisher's site, with no file URL

The seven `.docx` packages under *Used as primary sources* — the six `-v-3.0`
releases and `UthmanicDouri_V20.zip` — were **obtained from the publisher's own
site, `qurancomplex.gov.sa`**, as the maintainer states in answer to #38. That is all that
is known. The URL of each file and the day it was fetched were not kept, and
`quran-ws/kfgqpc-resources` does not hold them: searching that archive for
`-v-3.0`, for `UthmanicDouri_V20`, and for Bazzī in any form returns nothing,
and none of the seven digests appear in it.

They are therefore **verifiable but not re-fetchable from a recorded address**:
we can prove the file we have is the file we built from, and we can name the
publisher's site it came from, but we cannot fetch it again from a known URL
nor tell from one when it is superseded. On 2026-11-15 the site's fonts section
listed its packages as «قريباً» ("coming soon") and offered no download. Each
file states this under `provenance.text.origin`: `recorded` is `false`, because
it means a URL, and `portal` names the site.

No URL is guessed here to fill the gap. The `-v-3.0` family is not served from
the `/quran-dev/` page that supplies the cross-checks above — that page still
offered the v2 packages for all seven riwāyāt when the archive last captured it
on 2026-09-07 — so a plausible-looking `resources_dev/` URL would be wrong.

**One consequence, recorded because it already cost someone a day.** KFGQPC's
own `release_info.version` field is a page-level counter, not the version in the
filename: the archive lists `UthmanicHafs_v2-0.zip` as "version 13.0" and both
`UthmanicDouri_v2-0.zip` and `UthmanicSousi_v2-0.zip` as "version 3.0". Read
carelessly, that field makes it look as though Dūrī has a 3.0 release. It does
not, and the sentence above about Dūrī still stands.

## The printed muṣḥafs, read for what the packages omit

**These are the only sources here that are not KFGQPC data packages**, and they
are used for one thing the packages do not carry: the division marks in the
margin.

| muṣḥaf | print | SHA-256 |
|---|---|---|
| Ḥafṣ | [`standard39-2.pdf`](https://cdn.quran.ws/KFGQPC/resources/quran-hafs/standard39-2/standard39-2.pdf) | `5c4297de1fb6b654f641eed33242408d89432cbecf8a96ff5d297cb45fea7f07` |
| Shuʿbah | [`shuba-1.pdf`](https://cdn.quran.ws/KFGQPC/resources/quran-qiraat/shuba-1/shuba-1.pdf) | `51cc438eb199ee3fa379dbd1ca35b4abcf2d1a4ad778f52dfdcdc9df1a564d05` |
| Warsh | [`warsh39-1.pdf`](https://cdn.quran.ws/KFGQPC/resources/quran-qiraat/warsh39-1/warsh39-1.pdf) | `f33a6e55530548d9cbf7e0ab6d8154ba46eea12d227208ce849915b808850074` |
| Qālūn | [`qaloun-1.pdf`](https://cdn.quran.ws/KFGQPC/resources/quran-qiraat/qaloun-1/qaloun-1.pdf) | `57386a907a400bbad0cbc16002acb314db08350b5c5aabd43a6362085fb306cc` |
| Dūrī | [`douri-1.pdf`](https://cdn.quran.ws/KFGQPC/resources/quran-qiraat/douri-1/douri-1.pdf) | `918f24f92104407712224ebb0f3172f8c18f33dbddd1db85d16c3705e4644ea0` |
| Sūsī | [`sousi-1.pdf`](https://cdn.quran.ws/KFGQPC/resources/quran-qiraat/sousi-1/sousi-1.pdf) | `265b50e718bedec3df1a9ece77480baeec22f73137fa3a01ab6efc071a65005a` |

All six are KFGQPC's own PDFs of its printed muṣḥafs, fetched from the
[Quran.ws mirror of KFGQPC files](https://quran-ws.github.io/kfgqpc-resources/),
whose `SHA256SUMS` lists each one. **None is committed**: each is over 200 MB,
far past GitHub's limit, and the build does not read them. What was read from
them is in `sources/divisions/`, and each evidence file names its print and
hash. There is **no Bazzī print** on the mirror, so Bazzī has no division
layer.

The Ḥafṣ print's internal title is `standard39.pdf`, produced on Esko
Automation Engine in 2019. The thirteen Ḥafṣ readings first recorded here were
taken from another copy of the same edition, hosted on
[archive.org](https://archive.org/details/quran-pdf-download-hafs) as
`القرآن الكريم - المصحف العادي.pdf` (SHA-256 `1cd2a154…e5f8`). All forty were
read again from KFGQPC's own file, and the two agree.

**What they were used for.** The `.docx` releases encode the inline ۞ and
nothing else. The printed muṣḥaf marks every division with a label in its outer
margin, including the ones that fall at a sūrah opening, where no ۞ is printed.
Those labels were read to complete the 240 rubu_al_hizbs or 480 thumns of each
muṣḥaf. See `docs/known-issues.md` §7 and `docs/format.md`, *Divisions*.

**How they were read.** The PDFs have **no text layer**: every page is an
image. In each, muṣḥaf page *n* is PDF page *n+3*. Every page was rendered, and
every label in the outer margin was located by its position on the page. The
label's row was then matched to the row the data gives the division: each
page has fifteen ruled rows, with a sūrah heading and a basmalah taking one
each. Every label fell on an inline ۞ or on a recorded margin entry, and none
was left over. The label at every ḥizb start and every margin-only label was
then read by eye.

**They were checked against this repository before being trusted.** On page 151
of the Ḥafṣ print the thirteen text lines match `data/mushaf/hafs.json` word
for word. In the Sūsī print the rows differ from the reconstruction on about
seventeen pages, where a sūrah heading stands at the foot of the preceding
page (`docs/known-issues.md` §7).

**Where a print contradicts a package it is not silently preferred.** Six juz
starts in the v2 CSVs are not where the prints put them. §11 records each, and
`juz_starts` still follows the CSV.

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
