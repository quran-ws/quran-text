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

### The primary text packages have no recorded origin

**This is a real gap, and it is stated rather than papered over.** The seven
`.docx` packages under *Used as primary sources* — the six `-v-3.0` releases and
`UthmanicDouri_V20.zip` — are pinned here by name and SHA-256 and **by nothing
else**. No URL for any of them is recorded in this repository, in its history, or
in `quran-ws/kfgqpc-resources`, which does not hold them: searching that archive
for `-v-3.0`, for `UthmanicDouri_V20`, and for Bazzī in any form returns nothing,
and none of the seven digests appear in it.

They are therefore **verifiable but not re-fetchable**: we can prove the file we
have is the file we built from, and we cannot obtain it again, nor check it
against the publisher, nor tell when it is superseded.

No URL is guessed here to fill the gap. The `-v-3.0` family is not served from
the `/quran-dev/` page that supplies the cross-checks above — that page still
offered the v2 packages for all seven riwāyāt when the archive last captured it
on 2026-09-07 — so a plausible-looking `resources_dev/` URL would be wrong.
Where the file came from is an open question, tracked upstream.

**One consequence, recorded because it already cost someone a day.** KFGQPC's
own `release_info.version` field is a page-level counter, not the version in the
filename: the archive lists `UthmanicHafs_v2-0.zip` as "version 13.0" and both
`UthmanicDouri_v2-0.zip` and `UthmanicSousi_v2-0.zip` as "version 3.0". Read
carelessly, that field makes it look as though Dūrī has a 3.0 release. It does
not, and the sentence above about Dūrī still stands.

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

## Tier 2: riwāyāt decoded from the islamweb documents

**Everything above this heading is tier 1**: a data release by the muṣḥaf's
publisher, read as published. The ten riwāyāt KFGQPC does not publish —
Hishām; Khalaf and Khallād ʿan Ḥamzah; Abū al-Ḥārith ʿan al-Kisāʾī; Ibn
Wardān and Ibn Jammāz ʿan Abī Jaʿfar; Ruways and Rawḥ ʿan Yaʿqūb; Isḥāq ʿan
Khalaf al-ʿĀshir — come from somewhere else, and that somewhere is
weaker. (The ten riwāyāt KFGQPC lacks are these nine plus Idrīs, whose
islamweb file is the Isḥāq file under another name; see `docs/known-issues.md`
§17.) Every file derived from it says so: `provenance.tier` is `2`,
`provenance.authority` is `islamweb.net`, and the file carries what follows.

**What the documents are.** islamweb hosts one PDF per riwāyah at
`https://dl2.islamweb.net/Audio_Path/quran_list/<slug>/quran.pdf`. Each is a
Word document, 604 pages in the Madinah pagination, set in the King Fahd
Complex's 2005 "HQPB" symbol fonts and distilled to PDF between 2005 and 2018.
The author is not named in the document; the running header names only the
riwāyah. Words differing from Ḥafṣ are printed in colour, and the uṣūl of the
riwāyah (idghām, imālah, ṣilah, …) in further colours; the Warsh and Hishām
files print a legend for them, the others use the same palette unlabelled.
`sources/islamweb/<slug>/SOURCE.json` records each document's URL, SHA-256,
size, the PDF's own metadata and the date it was fetched. The PDFs themselves
are not committed; see `sources/islamweb/README.md`.

**Why the documents are decoded and not read.** Their text layer is not text.
The HQPB fonts are symbol fonts: a glyph is a letter form, a mark or a sign,
addressed by a glyph id, and the PDF's ToUnicode map is unusable — missing in
whole sections, and mapping two different glyphs to one character. So
`pipeline/tools/hqpb_extract.py` recovers from each PDF a *glyph stream*
(`glyphs.json.gz`: pages, lines, words, each glyph as *font, glyph id, colour*,
with āyah medallions, the basmalah ligature and ۞ recognised by glyph id), and
`pipeline/tools/hqpb_calibrate.py` learns a glyph → Unicode table from the
three riwāyāt both sources carry — Qālūn, Shuʿbah and Warsh — by aligning
their streams against the KFGQPC texts word by word. Signs those three never
print (Abū Jaʿfar's ṣilah wāw, the imālah dot of Ḥamzah's readers) are
identified the same way against the KFGQPC riwāyāt that do print them; what
alignment cannot settle is settled by outline identity with a known glyph, and
the last few dozen by the model reading boxed crops of the documents, each
recorded in `decoder/inspected.json` with the page and the word. Every table
entry records how it was identified and on how many distinct words.
`sources/islamweb/decoder/calibration.json` holds the measured accuracy of the
table on each calibration riwāyah, and `provenance.decoder` in every tier-2
file repeats it. The method is in `docs/method.md`, *Decoding*.

**What is and is not asserted.** A tier-2 word is a table lookup, glyph by
glyph; nothing is inferred from Ḥafṣ or from another riwāyah into the text. A
glyph the table does not know is emitted as U+FFFD and the build refuses to
publish the file (`check_decoder`). The āyah divisions are the document's own
medallions, numbered by position because the printed numbers carry typists'
slips, which `layers.derived.text.printed_ayah_number_slips` lists. The colours
are published as a layer (`colors`, `color_types`) with the legends' wording,
and `check_colors` tests the one claim they make that the data can test: a word
coloured as differing from Ḥafṣ must differ from Ḥafṣ.

**Where this stands below tier 1.** *Where a tier-2 text contradicts a tier-1
text it is not preferred* (`TIER_POLICY`): no tier-2 riwāyah duplicates a
tier-1 one, only the tier-1 editions vote when a counting anchor is ambiguous,
the plene/defective ā warrant is tested on tier 1 alone, and a tier-2 file's
unexplained āyah ends are listed but do not fail the build. The notation is the
2022 KFGQPC one, documented in the table file and in `layers.derived.text`.
The islamweb copies of Qālūn, Shuʿbah, Warsh and Qunbul are calibration
material only and are never published from here.

**What this route cannot reach.** islamweb's Ḥafṣ, Dūrī, Sūsī, Ibn Dhakwān and
al-Dūrī ʿan al-Kisāʾī files are page scans with no text layer, there is no
file for al-Bazzī, and the Idrīs file is the Isḥāq file. **Ibn Dhakwān,
al-Dūrī ʿan al-Kisāʾī and Idrīs are therefore absent**, Qunbul awaits its
KFGQPC package, and the dataset covers sixteen of the twenty riwāyāt.

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
